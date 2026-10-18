"""Every rung, rival and construction variant of the main call, computed from the shipped files in target/.

Used by checks.py (assertions) and build.py (figures.json). The golden itself is calc.golden.
"""
import csv
import datetime as dt
import os
import sqlite3
from collections import defaultdict

import numpy as np
from openpyxl import load_workbook

import calc as C

LIN = "LIN"
BASES = ("LIN", "TRN", "VRN", "VCE", "BLQ")


# ------------------------------------------------------------------ readers for the other files
def read_ym3(target):
    con = sqlite3.connect(os.path.join(target, "ym3_leg_history_s24.sqlite"))
    cur = con.cursor()
    dcps = [int(x) for x in dict(cur.execute("select k, v from ym3_extract"))["dcp_set"].split(",")]
    legs = {}
    for lid, flt, dep, std, o, d, typ, cap in cur.execute("select * from legs"):
        legs[lid] = dict(flt=flt, dep=dt.datetime.strptime(dep, "%d/%m/%Y").date(), std=std, orig=o, dest=d, typ=typ,
                         cap=cap, bkd=np.zeros(len(dcps)), avl=[""] * len(dcps))
    pos = {t: k for k, t in enumerate(dcps)}
    for lid, dcp, bkd, avl in cur.execute("select leg_id, dcp, bkd, avl from bkg"):
        legs[lid]["bkd"][pos[dcp]] = bkd
        legs[lid]["avl"][pos[dcp]] = avl
    for lid, pax, inf in cur.execute("select leg_id, pax, inf from flown"):
        legs[lid]["pax"] = pax
        legs[lid]["inf"] = inf
    con.close()
    return dcps, list(legs.values())


def capacity_total(target):
    wb = load_workbook(os.path.join(target, "summer2026_capacity_plan_v3.xlsx"), data_only=False)
    ws = wb["Gauge changes"]
    for row in ws.iter_rows(values_only=True):
        if row[0] == "Nine Linate routes":
            return int(row[4])
    raise KeyError


def gauge_changes_s25(target):
    """Routes that changed gauge for summer 2025, from the schedule change log."""
    wb = load_workbook(os.path.join(target, "schedule_change_log.xlsx"))
    ws = wb["Log"]
    out = set()
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[1] == "IS25" and row[3] == "gauge":
            b, s = row[2].split("-")
            out.add((b, s))
    return out


def route_of(o, d):
    return (o, d) if o in BASES and not (d in BASES) else (d, o) if d in BASES and o not in BASES else (o, d)


# ------------------------------------------------------------------ rung 0: the 2025 upgauges' passengers per seat
def per_seat_response(target, rows=None, dcs=None):
    if rows is None:
        _, rows = C.read_rm(target)
    if dcs is None:
        dcs = C.read_dcs(target)
    past = gauge_changes_s25(target)
    _, legs24 = read_ym3(target)
    pax24 = defaultdict(int)
    seats24 = defaultdict(int)
    pax24_inf = defaultdict(int)
    for L in legs24:
        r = route_of(L["orig"], L["dest"])
        if r in past:
            pax24[r] += L["pax"] - L["inf"]
            pax24_inf[r] += L["pax"]
            seats24[r] += L["cap"]
    pax25 = defaultdict(int)
    seats25 = defaultdict(int)
    for r in rows:
        k = route_of(r["orig"], r["dest"])
        if k in past:
            d = dcs[(r["flt"], r["dep"].isoformat())]
            pax25[k] += int(d["pax_flown"])
            seats25[k] += r["cap"]
    dp = sum(pax25.values()) - sum(pax24.values())
    ds = sum(seats25.values()) - sum(seats24.values())
    dp_inf = sum(pax25.values()) - sum(pax24_inf.values())
    per_route = {k: (pax25[k] - pax24[k]) / (seats25[k] - seats24[k]) for k in past}
    return {"per_seat": dp / ds, "per_seat_infants_left_in": dp_inf / ds, "routes": per_route,
            "pax24": dict(pax24), "pax25": dict(pax25), "seats24": dict(seats24), "seats25": dict(seats25)}


def loo_per_seat(resp):
    """Leave-one-route-out error of the per-seat response on the 2025 upgauges."""
    errs = []
    ks = sorted(resp["routes"])
    for k in ks:
        others = [j for j in ks if j != k]
        dp = sum(resp["pax25"][j] - resp["pax24"][j] for j in others)
        ds = sum(resp["seats25"][j] - resp["seats24"][j] for j in others)
        pred = dp / ds * (resp["seats25"][k] - resp["seats24"][k])
        act = resp["pax25"][k] - resp["pax24"][k]
        errs.append(abs(pred - act) / act)
    return float(np.mean(errs)), errs


# ------------------------------------------------------------------ the construction family and the rivals
def family(target, g=None):
    """The main call's figure under every construction the design note lists."""
    g = g or C.golden(target)
    rows, dcs, dcps = g["rows"], g["dcs"], g["dcps"]
    nn = lambda r: not C.is_nine(r["orig"], r["dest"])
    out = {"golden": g["gain"]}

    def run(cf, mode="exact"):
        return C.forecast(rows, dcs, dcps, cf, mode=mode)[0]

    cm = g["curves"]
    for mode in ("lastopen", "firstclosed", "datediff"):
        out["month_" + mode] = run(lambda r: cm[r["dep"].month], mode)
    past = gauge_changes_s25(target)
    pairs_past = {(a, b) for a, b in past} | {(b, a) for a, b in past}
    c_ref, _ = C.curves(rows, lambda r: r["dep"].month, keep=lambda r: nn(r) and (r["orig"], r["dest"]) not in pairs_past)
    out["month_ref_routes_only"] = run(lambda r: c_ref[r["dep"].month])
    c_past, _ = C.curves(rows, lambda r: r["dep"].month, keep=lambda r: (r["orig"], r["dest"]) in pairs_past)
    out["month_2025_upgauges_only"] = run(lambda r: c_past[r["dep"].month])
    c_all, _ = C.curves(rows, lambda r: r["dep"].month, keep=lambda r: True)
    out["month_all_open_incl_nine"] = run(lambda r: c_all[r["dep"].month])
    c_lin, _ = C.curves(rows, lambda r: r["dep"].month, keep=lambda r: nn(r) and LIN in (r["orig"], r["dest"]))
    out["month_linate_routes_only"] = run(lambda r: c_lin[r["dep"].month])
    hk = lambda r: (r["dep"].month, r["dep"].day > 15)
    c_h, _ = C.curves(rows, hk, keep=nn)
    out["half_month"] = run(lambda r: c_h[hk(r)])
    out["half_month_lastopen"] = run(lambda r: c_h[hk(r)], "lastopen")
    wk = lambda r: r["dep"].isocalendar()[1]
    c_w, _ = C.curves(rows, wk, keep=nn)
    out["iso_week"] = run(lambda r: c_w[wk(r)])
    out["iso_week_lastopen"] = run(lambda r: c_w[wk(r)], "lastopen")
    mdk = lambda r: (r["dep"].month, r["orig"] in BASES)
    c_md, _ = C.curves(rows, mdk, keep=nn)
    out["month_by_direction"] = run(lambda r: c_md[mdk(r)])
    mwk = lambda r: (r["dep"].month, r["dep"].weekday())
    c_mw, _ = C.curves(rows, mwk, keep=nn)
    out["month_by_weekday"] = run(lambda r: c_mw[mwk(r)])
    # centred windows of departure dates
    byday = defaultdict(list)
    for r in rows:
        if r["so"] == "" and nn(r) and r["bkd"][-1] > 0:
            byday[r["dep"]].append(r["bkd"] / r["bkd"][-1])
    dm = {d: (np.sum(v, axis=0), len(v)) for d, v in byday.items()}
    for w in (7, 15):
        cache = {}

        def cf(r, w=w, cache=cache):
            d = r["dep"]
            if d not in cache:
                s, n = 0, 0
                for k in range(-w, w + 1):
                    dd = d + dt.timedelta(days=k)
                    if dd in dm:
                        s = s + dm[dd][0]
                        n += dm[dd][1]
                cache[d] = s / n
            return cache[d]
        out["window_pm%d" % w] = run(cf)
        out["window_pm%d_lastopen" % w] = run(cf, "lastopen")
    # ratio of totals instead of mean of shares
    sums = defaultdict(lambda: 0)
    fin = defaultdict(float)
    for r in rows:
        if r["so"] == "" and nn(r) and r["bkd"][-1] > 0:
            sums[r["dep"].month] = sums[r["dep"].month] + r["bkd"]
            fin[r["dep"].month] += r["bkd"][-1]
    c_rt = {m: sums[m] / fin[m] for m in sums}
    out["month_ratio_of_totals"] = run(lambda r: c_rt[r["dep"].month])
    # the nine routes' own open departures by month, the nearest month where a month has none
    c_own, n_own = C.curves(rows, lambda r: r["dep"].month, keep=lambda r: C.is_nine(r["orig"], r["dest"]))

    def own(r):
        m = r["dep"].month
        if m in c_own:
            return c_own[m]
        return c_own[sorted(c_own, key=lambda k: (abs(k - m), k))[0]]
    out["month_nine_own_open"] = run(own)
    # no-shows applied before the cap, and each departure's own no-show share
    ns = C.noshow_by_leg(rows, dcs)
    a1, a2, base = 0.0, 0.0, 0
    for r in rows:
        if not C.is_nine(r["orig"], r["dest"]):
            continue
        d = dcs[(r["flt"], r["dep"].isoformat())]
        base += int(d["pax_flown"])
        D = C.demand(r, cm[r["dep"].month], dcps)
        a1 += min(D * (1 - ns[(r["orig"], r["dest"])]), C.seats_s26(r))
        a2 += min(D, C.seats_s26(r)) * int(d["pax_flown"]) / int(d["pax_booked"])
    out["noshow_before_cap"] = a1 - base
    out["noshow_by_departure"] = a2 - base
    out["_n_own_open_by_month"] = n_own
    return out


def rungs(target, g=None):
    g = g or C.golden(target)
    rows, dcs, dcps = g["rows"], g["dcs"], g["dcps"]
    nn = lambda r: not C.is_nine(r["orig"], r["dest"])
    added = capacity_total(target)
    resp = per_seat_response(target, rows, dcs)
    out = {"added_seats": added}
    out["rung0_per_seat"] = resp["per_seat"] * added
    out["rung0_per_seat_infants_left_in"] = resp["per_seat_infants_left_in"] * added
    out["per_seat"] = resp["per_seat"]
    out["loo_mae"] = loo_per_seat(resp)[0]
    # carried plus the turned-away requests, capped at the new seats departure by departure
    ta = defaultdict(int)
    so = {(r["flt"], r["dep"].isoformat()): r["so"] for r in rows}
    seen = set()
    nine_dep = {(r["flt"], r["dep"].isoformat()) for r in rows if C.is_nine(r["orig"], r["dest"])}
    for e in C.read_refusals(target):
        if (int(e["flight_no"]), e["dep_date"]) not in nine_dep:
            continue
        key = (e["session_ref"], e["flight_no"], e["dep_date"])
        if key in seen:
            continue
        seen.add(key)
        ta[(int(e["flight_no"]), e["dep_date"])] += int(e["pax"])
    ns = C.noshow_by_leg(rows, dcs)
    fc = 0.0
    base = 0
    for r in rows:
        if not C.is_nine(r["orig"], r["dest"]):
            continue
        d = dcs[(r["flt"], r["dep"].isoformat())]
        base += int(d["pax_flown"])
        dem = r["bkd"][-1] + (ta.get((r["flt"], r["dep"].isoformat()), 0) if r["so"] else 0)
        fc += min(dem, C.seats_s26(r)) * (1 - ns[(r["orig"], r["dest"])])
    out["rung1_carried_plus_turned_away"] = fc - base
    cp, _ = C.curves(rows, lambda r: 0, keep=nn)
    out["rung2_pooled_network"] = C.forecast(rows, dcs, dcps, lambda r: cp[0])[0]
    co, _ = C.curves(rows, lambda r: 0, keep=lambda r: C.is_nine(r["orig"], r["dest"]))
    out["rung2b_pooled_nine_own_open"] = C.forecast(rows, dcs, dcps, lambda r: co[0])[0]
    cm = g["curves"]
    # side errors on the golden construction
    out["side_noshows_ignored"] = C.forecast(rows, dcs, dcps, lambda r: cm[r["dep"].month],
                                             ns={k: 0.0 for k in ns})[0]
    out["side_switch_ignored"] = C.forecast(rows, dcs, dcps, lambda r: cm[r["dep"].month],
                                            s26=lambda r: 232)[0]
    out["side_infants_counted"] = C.forecast(rows, dcs, dcps, lambda r: cm[r["dep"].month], include_infants=True)[0]
    lf = sum(int(dcs[(r["flt"], r["dep"].isoformat())]["pax_flown"]) for r in rows if C.is_nine(r["orig"], r["dest"]))
    seats = sum(r["cap"] for r in rows if C.is_nine(r["orig"], r["dest"]))
    out["side_added_seats_at_s25_load"] = added * lf / seats
    return out


# ------------------------------------------------------------------ the back-test on the 2025 upgauges
def backtest(target, g=None):
    """Forecast the 2025 upgauges' summer 2025 passengers from their summer 2024 records (YM3), as the plan for
    summer 2025 would have, under each completion; compare with summer 2025 as flown (DCS)."""
    g = g or C.golden(target)
    rows, dcs = g["rows"], g["dcs"]
    past = gauge_changes_s25(target)
    dcps, legs = read_ym3(target)
    arr = np.array(dcps)
    nine = lambda L: (L["orig"] == "LIN" and L["dest"] in C.NINE) or (L["dest"] == "LIN" and L["orig"] in C.NINE)
    is_past = lambda L: route_of(L["orig"], L["dest"]) in past
    sold = lambda L: L["bkd"][-1] >= L["cap"]

    def curves24(key, keep):
        acc = defaultdict(list)
        for L in legs:
            if not sold(L) and keep(L) and L["bkd"][-1] > 0:
                acc[key(L)].append(L["bkd"] / L["bkd"][-1])
        return {k: np.mean(v, axis=0) for k, v in acc.items()}

    keep_net = lambda L: not is_past(L) and not nine(L)
    c_month = curves24(lambda L: L["dep"].month, keep_net)
    c_pool = curves24(lambda L: 0, keep_net)
    c_own = curves24(lambda L: 0, is_past)
    # S25 seats and actual S25 carried on the 2025 upgauges, by flight-date 364 days on
    cap25 = {}
    act = 0
    for r in rows:
        k = route_of(r["orig"], r["dest"])
        if k in past:
            cap25[(r["orig"], r["dest"], r["dep"])] = r["cap"]
            act += int(dcs[(r["flt"], r["dep"].isoformat())]["pax_flown"])
    ns = defaultdict(lambda: [0, 0])
    for L in legs:
        if is_past(L):
            ns[(L["orig"], L["dest"])][0] += L["bkd"][-1]
            ns[(L["orig"], L["dest"])][1] += L["pax"] - L["inf"]
    nsr = {k: 1 - v[1] / v[0] for k, v in ns.items()}

    def fc(curve_for, point="lastopen"):
        tot = 0.0
        for L in legs:
            if not is_past(L):
                continue
            c = curve_for(L)
            if not sold(L):
                D = L["bkd"][-1]
            elif point == "lastopen":
                jj = int(np.nonzero(L["bkd"] < L["cap"])[0][-1])
                D = L["bkd"][jj] / c[jj]
            else:
                j = int(np.nonzero(L["bkd"] >= L["cap"])[0][0])
                D = L["cap"] / c[j]
            s25 = cap25[(L["orig"], L["dest"], L["dep"] + dt.timedelta(days=364))]
            tot += min(D, s25) * (1 - nsr[(L["orig"], L["dest"])])
        return tot

    out = {"actual_s25": act}
    out["month_lastopen"] = fc(lambda L: c_month[L["dep"].month])
    out["month_firstclosed"] = fc(lambda L: c_month[L["dep"].month], "firstclosed")
    out["pooled_lastopen"] = fc(lambda L: c_pool[0])
    out["own_open_pooled_lastopen"] = fc(lambda L: c_own[0])
    out["carried_s24"] = sum(L["pax"] - L["inf"] for L in legs if is_past(L))
    for k in list(out):
        if k not in ("actual_s25", "carried_s24"):
            out[k + "_err"] = out[k] / act - 1
    return out


# ------------------------------------------------------------------ sampling spread of the golden
def bootstrap(target, g=None, n=200, seed=168):
    """Resample the reference departures within month and the nine routes' departures; the golden's spread."""
    g = g or C.golden(target)
    rows, dcs, dcps = g["rows"], g["dcs"], g["dcps"]
    rng = np.random.default_rng(seed)
    nn = lambda r: not C.is_nine(r["orig"], r["dest"])
    refs = defaultdict(list)
    for r in rows:
        if r["so"] == "" and nn(r) and r["bkd"][-1] > 0:
            refs[r["dep"].month].append(r["bkd"] / r["bkd"][-1])
    refs = {m: np.array(v) for m, v in refs.items()}
    nine = [r for r in rows if C.is_nine(r["orig"], r["dest"])]
    ns = C.noshow_by_leg(rows, dcs)
    # per-departure contributions under a given curve set
    vals = []
    for b in range(n):
        cm = {m: v[rng.integers(0, len(v), len(v))].mean(axis=0) for m, v in refs.items()}
        idx = rng.integers(0, len(nine), len(nine))
        tot = 0.0
        base = 0
        for k in idx:
            r = nine[k]
            d = dcs[(r["flt"], r["dep"].isoformat())]
            base += int(d["pax_flown"])
            tot += min(C.demand(r, cm[r["dep"].month], dcps), C.seats_s26(r)) * (1 - ns[(r["orig"], r["dest"])])
        vals.append(tot - base)
    return float(np.std(vals)), vals


# ------------------------------------------------------------------ holdout: open departures censored at a lower cap
def pseudo_censor(target, g=None, share=0.85):
    """Every never-sold-out departure off the nine routes, censored at share of its final bookings, completed from
    each curve; the completed total against the actual total, by month. A completion that is right recovers the
    actual; the curve's own departures are left out of the curve that completes them (leave-one-route-out)."""
    g = g or C.golden(target)
    rows, dcps = g["rows"], g["dcps"]
    arr = np.array(dcps, float)
    nn = lambda r: not C.is_nine(r["orig"], r["dest"])
    refs = [r for r in rows if r["so"] == "" and nn(r) and r["bkd"][-1] >= 40]
    by_route_month = defaultdict(lambda: [0, 0])
    sums_m = defaultdict(lambda: 0)
    n_m = defaultdict(int)
    sums_p = 0
    n_p = 0
    for r in refs:
        sh = r["bkd"] / r["bkd"][-1]
        sums_m[r["dep"].month] = sums_m[r["dep"].month] + sh
        n_m[r["dep"].month] += 1
        sums_p = sums_p + sh
        n_p += 1
    out = defaultdict(lambda: defaultdict(float))
    for r in refs:
        sh = r["bkd"] / r["bkd"][-1]
        m = r["dep"].month
        cm = (sums_m[m] - sh) / (n_m[m] - 1)
        cp = (sums_p - sh) / (n_p - 1)
        cap = share * r["bkd"][-1]
        j = int(np.nonzero(r["bkd"] >= cap)[0][0])
        if j == 0:
            continue
        # the pseudo sell-out between snapshots j-1 and j, placed by linear interpolation of the bookings
        b0, b1 = r["bkd"][j - 1], r["bkd"][j]
        x = arr[j - 1] - (arr[j - 1] - arr[j]) * ((cap - b0) / (b1 - b0) if b1 > b0 else 1.0)
        for name, c in (("month", cm), ("pooled", cp)):
            out[m][name] += cap / C.interp(c, dcps, x)
        out[m]["actual"] += r["bkd"][-1]
        # additive pickup: the cap plus the month's mean bookings still to come from that point
        out[m]["additive"] += cap + float(np.mean([0]))
    res = {}
    for m in sorted(out):
        res[m] = {k: out[m][k] / out[m]["actual"] - 1 for k in ("month", "pooled")}
    return res


def transfer_holdout(target, g=None, share=0.85):
    """The nine routes' own open departures, censored at share of their final bookings and completed from the
    other routes' open departures of the same month: multiplicative (share of final on hand) against additive
    (bookings still to come, in passengers) pickup, and the pooled multiplicative curve. Returns the completed
    total's error against the actual total."""
    g = g or C.golden(target)
    rows, dcps = g["rows"], g["dcps"]
    arr = np.array(dcps, float)
    nn = lambda r: not C.is_nine(r["orig"], r["dest"])
    cm = g["curves"]
    cp, _ = C.curves(rows, lambda r: 0, keep=nn)
    pick = defaultdict(list)
    for r in rows:
        if r["so"] == "" and nn(r) and r["bkd"][-1] > 0:
            pick[r["dep"].month].append(r["bkd"][-1] - r["bkd"])
    pm = {m: np.mean(v, axis=0) for m, v in pick.items()}
    tot = defaultdict(float)
    n = 0
    for r in rows:
        if not (r["so"] == "" and C.is_nine(r["orig"], r["dest"]) and r["bkd"][-1] >= 40):
            continue
        cap = share * r["bkd"][-1]
        j = int(np.nonzero(r["bkd"] >= cap)[0][0])
        if j == 0:
            continue
        b0, b1 = r["bkd"][j - 1], r["bkd"][j]
        x = arr[j - 1] - (arr[j - 1] - arr[j]) * ((cap - b0) / (b1 - b0) if b1 > b0 else 1.0)
        m = r["dep"].month
        tot["multiplicative"] += cap / C.interp(cm[m], dcps, x)
        tot["pooled"] += cap / C.interp(cp[0], dcps, x)
        tot["additive"] += cap + float(np.interp(x, arr[::-1], pm[m][::-1]))
        tot["actual"] += r["bkd"][-1]
        n += 1
    return {k: tot[k] / tot["actual"] - 1 for k in ("multiplicative", "pooled", "additive")}, n


def additive_pickup(target, g=None):
    g = g or C.golden(target)
    rows, dcs, dcps = g["rows"], g["dcs"], g["dcps"]
    arr = np.array(dcps, float)
    nn = lambda r: not C.is_nine(r["orig"], r["dest"])
    pick = defaultdict(list)
    for r in rows:
        if r["so"] == "" and nn(r) and r["bkd"][-1] > 0:
            pick[r["dep"].month].append(r["bkd"][-1] - r["bkd"])
    pm = {m: np.mean(v, axis=0) for m, v in pick.items()}
    ns = C.noshow_by_leg(rows, dcs)
    tot, base = 0.0, 0
    for r in rows:
        if not C.is_nine(r["orig"], r["dest"]):
            continue
        base += int(dcs[(r["flt"], r["dep"].isoformat())]["pax_flown"])
        if r["so"]:
            D = r["cap"] + float(np.interp(C.x_sellout(r), arr[::-1], pm[r["dep"].month][::-1]))
        else:
            D = r["bkd"][-1]
        tot += min(D, C.seats_s26(r)) * (1 - ns[(r["orig"], r["dest"])])
    return tot - base


# ------------------------------------------------------------------ the families a revenue analyst could reach for
BUCKETS = {
    "June to September against the rest": {3: 0, 4: 0, 5: 0, 6: 1, 7: 1, 8: 1, 9: 1, 10: 0},
    "July and August against the rest": {3: 0, 4: 0, 5: 0, 6: 0, 7: 1, 8: 1, 9: 0, 10: 0},
    "March to May, June to August, September and October": {3: 0, 4: 0, 5: 0, 6: 1, 7: 1, 8: 1, 9: 2, 10: 2},
    "March to June, July and August, September and October": {3: 0, 4: 0, 5: 0, 6: 0, 7: 1, 8: 1, 9: 2, 10: 2},
    "March to May, June to September, October": {3: 0, 4: 0, 5: 0, 6: 1, 7: 1, 8: 1, 9: 1, 10: 2},
    "March to May, June and July, August and September, October": {3: 0, 4: 0, 5: 0, 6: 1, 7: 1, 8: 2, 9: 2, 10: 3},
}


def month_holdout(target, g, mapping=None, share=0.85):
    """The open departures off the nine routes censored at share of their final bookings and completed from the
    build of their group of months (each departure left out of its own group's build); error of the completed
    total against the actual, by departure month. mapping None is the month itself; a constant is the pooled build."""
    rows, dcps = g["rows"], g["dcps"]
    arr = np.array(dcps, float)
    key = (lambda r: r["dep"].month) if mapping is None else (lambda r: mapping[r["dep"].month])
    refs = [r for r in rows if r["so"] == "" and not C.is_nine(r["orig"], r["dest"]) and r["bkd"][-1] >= 40]
    sums, cnt = defaultdict(lambda: 0), defaultdict(int)
    for r in refs:
        sums[key(r)] = sums[key(r)] + r["bkd"] / r["bkd"][-1]
        cnt[key(r)] += 1
    acc = defaultdict(lambda: [0.0, 0.0])
    for r in refs:
        cur = (sums[key(r)] - r["bkd"] / r["bkd"][-1]) / (cnt[key(r)] - 1)
        cap = share * r["bkd"][-1]
        j = int(np.nonzero(r["bkd"] >= cap)[0][0])
        if j == 0:
            continue
        b0, b1 = r["bkd"][j - 1], r["bkd"][j]
        x = arr[j - 1] - (arr[j - 1] - arr[j]) * ((cap - b0) / (b1 - b0) if b1 > b0 else 1.0)
        acc[r["dep"].month][0] += cap / C.interp(cur, dcps, x)
        acc[r["dep"].month][1] += r["bkd"][-1]
    return {m: v[0] / v[1] - 1 for m, v in sorted(acc.items())}


def buckets(target, g=None):
    """Each grouping of departure months: the call's figure and the holdout's error by month."""
    g = g or C.golden(target)
    rows, dcs, dcps = g["rows"], g["dcs"], g["dcps"]
    nn = lambda r: not C.is_nine(r["orig"], r["dest"])
    out = {}
    for name, mp in BUCKETS.items():
        c, _ = C.curves(rows, lambda r, mp=mp: mp[r["dep"].month], keep=nn)
        gain = C.forecast(rows, dcs, dcps, lambda r, mp=mp, c=c: c[mp[r["dep"].month]])[0]
        out[name] = (gain, month_holdout(target, g, mp))
    return out


def em_normal(x, c, iters=5000, tol=1e-8):
    """Expectation-maximisation for normal demand with right-censored observations (c True where x is the cap)."""
    from scipy.stats import norm
    mu = float(x.mean())
    sd = max(float(x.std()), 5.0)
    for _ in range(iters):
        z = (x - mu) / sd
        lam = norm.pdf(z) / np.maximum(norm.sf(z), 1e-12)
        e1 = np.where(c, mu + sd * lam, x)
        e2 = np.where(c, mu ** 2 + sd ** 2 + sd * (x + mu) * lam, x ** 2)
        mu2 = float(e1.mean())
        sd2 = float(np.sqrt(max(e2.mean() - mu2 ** 2, 1.0)))
        done = abs(mu2 - mu) < tol and abs(sd2 - sd) < tol
        mu, sd = mu2, sd2
        if done:
            break
    z = (x - mu) / sd
    lam = norm.pdf(z) / np.maximum(norm.sf(z), 1e-12)
    return np.where(c, mu + sd * lam, x)


def em_forecast(target, g, key):
    """The call's figure with each sold-out departure's demand from a normal EM on the final bookings of its cell;
    a cell with no departure below the seats keeps its departures at the seats."""
    rows, dcs = g["rows"], g["dcs"]
    ns = C.noshow_by_leg(rows, dcs)
    cells = defaultdict(list)
    for r in rows:
        if C.is_nine(r["orig"], r["dest"]):
            cells[key(r)].append(r)
    tot, base = 0.0, 0
    for k, rs in cells.items():
        x = np.array([r["bkd"][-1] for r in rs], float)
        c = np.array([r["so"] != "" for r in rs])
        e = em_normal(x, c) if (~c).any() else x
        for r, v in zip(rs, e):
            base += int(dcs[(r["flt"], r["dep"].isoformat())]["pax_flown"])
            tot += min(v, C.seats_s26(r)) * (1 - ns[(r["orig"], r["dest"])])
    return tot - base


def em_holdout(target, g=None):
    """The other routes' open departures, each route direction and month censored so that the share of its
    departures held at the cap equals the nine routes' sold-out share in that month; for the censored departures,
    the demand above the cap completed by a normal EM on the cell's final bookings and by the month build from the
    moment the bookings reached the cap (each departure left out of its month's build), against the actual."""
    g = g or C.golden(target)
    rows, dcps = g["rows"], g["dcps"]
    arr = np.array(dcps, float)
    sold = defaultdict(lambda: [0, 0])
    for r in rows:
        if C.is_nine(r["orig"], r["dest"]):
            sold[r["dep"].month][0] += r["so"] != ""
            sold[r["dep"].month][1] += 1
    f = {m: v[0] / v[1] for m, v in sold.items()}
    refs = [r for r in rows if r["so"] == "" and not C.is_nine(r["orig"], r["dest"]) and r["bkd"][-1] > 0]
    sums, cnt = defaultdict(lambda: 0), defaultdict(int)
    cells = defaultdict(list)
    for r in refs:
        sums[r["dep"].month] = sums[r["dep"].month] + r["bkd"] / r["bkd"][-1]
        cnt[r["dep"].month] += 1
        cells[((r["orig"], r["dest"]), r["dep"].month)].append(r)
    acc = defaultdict(lambda: defaultdict(float))
    for (od, m), rs in sorted(cells.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        rs = sorted(rs, key=lambda r: (r["bkd"][-1], r["dep"], r["flt"]))
        n = len(rs)
        u = max(1, int(round((1 - f[m]) * n)))
        if u >= n:
            continue
        x = np.array([r["bkd"][-1] for r in rs], float)
        cap = (x[u - 1] + x[u]) / 2.0
        c = np.arange(n) >= u
        e = em_normal(np.where(c, cap, x), c)
        for r, cc, ee in zip(rs, c, e):
            if not cc:
                continue
            cur = (sums[m] - r["bkd"] / r["bkd"][-1]) / (cnt[m] - 1)
            j = int(np.nonzero(r["bkd"] >= cap)[0][0])
            if j == 0:
                pr = r["bkd"][-1]
            else:
                b0, b1 = r["bkd"][j - 1], r["bkd"][j]
                xx = arr[j - 1] - (arr[j - 1] - arr[j]) * ((cap - b0) / (b1 - b0) if b1 > b0 else 1.0)
                pr = cap / C.interp(cur, dcps, xx)
            a = acc[m]
            a["em"] += ee
            a["month"] += pr
            a["actual"] += r["bkd"][-1]
            a["cap"] += cap
            a["n"] += 1
    out = {}
    tot = defaultdict(float)
    for m, a in sorted(acc.items()):
        sp = a["actual"] - a["cap"]
        out[m] = {"censored_share": f[m], "departures": int(a["n"]), "em": (a["em"] - a["cap"]) / sp - 1,
                  "month": (a["month"] - a["cap"]) / sp - 1}
        for k in ("em", "month", "actual", "cap"):
            tot[k] += a[k]
    sp = tot["actual"] - tot["cap"]
    out["summer"] = {"em": (tot["em"] - tot["cap"]) / sp - 1, "month": (tot["month"] - tot["cap"]) / sp - 1}
    return out


def additive(target, g, key, keep, point="exact"):
    """Additive pickup: the seats plus the mean bookings still to come, in passengers, of the open departures of the
    key's group, from the moment the departure sold out (or its bookings at the last snapshot before it did)."""
    rows, dcs, dcps = g["rows"], g["dcs"], g["dcps"]
    arr = np.array(dcps, float)
    pick = defaultdict(list)
    for r in rows:
        if r["so"] == "" and keep(r) and r["bkd"][-1] > 0:
            pick[key(r)].append(r["bkd"][-1] - r["bkd"])
    pm = {k: np.mean(v, axis=0) for k, v in pick.items()}
    ns = C.noshow_by_leg(rows, dcs)
    tot, base = 0.0, 0
    for r in rows:
        if not C.is_nine(r["orig"], r["dest"]):
            continue
        base += int(dcs[(r["flt"], r["dep"].isoformat())]["pax_flown"])
        if not r["so"]:
            D = r["bkd"][-1]
        elif point == "exact":
            D = r["cap"] + float(np.interp(C.x_sellout(r), arr[::-1], pm[key(r)][::-1]))
        else:
            jj = int(np.nonzero(arr > C.x_sellout(r))[0][-1])
            D = r["bkd"][jj] + pm[key(r)][jj]
        tot += min(D, C.seats_s26(r)) * (1 - ns[(r["orig"], r["dest"])])
    return tot - base


def methods(target, g=None):
    """The standard unconstraining methods outside the golden's family."""
    g = g or C.golden(target)
    nn = lambda r: not C.is_nine(r["orig"], r["dest"])
    own = lambda r: C.is_nine(r["orig"], r["dest"])
    return {
        "additive, month, other routes": additive(target, g, lambda r: r["dep"].month, nn),
        "additive, pooled, other routes": additive(target, g, lambda r: 0, nn),
        "additive, pooled, every open departure": additive(target, g, lambda r: 0, lambda r: True),
        "additive, pooled, nine routes' own": additive(target, g, lambda r: 0, own),
        "additive, pooled, nine routes' own, last open snapshot": additive(target, g, lambda r: 0, own, "lastopen"),
        "additive, pooled, every open departure, last open snapshot": additive(target, g, lambda r: 0,
                                                                              lambda r: True, "lastopen"),
        "EM, flight and month": em_forecast(target, g, lambda r: (r["flt"], r["dep"].month)),
        "EM, route direction": em_forecast(target, g, lambda r: (r["orig"], r["dest"])),
        "EM, route direction and month": em_forecast(target, g, lambda r: (r["orig"], r["dest"], r["dep"].month)),
    }


def local_members(target, g=None):
    """Time-local constructions on the nine routes' own open departures and on the whole network, as an analyst
    holding the reference to the same flight or to nearby dates would build them."""
    g = g or C.golden(target)
    rows, dcs, dcps = g["rows"], g["dcs"], g["dcps"]
    open_ = [r for r in rows if r["so"] == "" and r["bkd"][-1] > 0]
    by_flt = defaultdict(list)
    by_dir = defaultdict(list)
    by_day = defaultdict(list)
    for r in open_:
        sh = r["bkd"] / r["bkd"][-1]
        by_flt[r["flt"]].append((r["dep"], sh))
        by_dir[(r["orig"], r["dest"])].append((r["dep"], sh))
        by_day[r["dep"]].append(sh)
    cm_all, _ = C.curves(rows, lambda r: r["dep"].month, keep=lambda r: True)
    out = {}

    def near(lst, d, k):
        v = [sh for dd, sh in lst if abs((dd - d).days) <= k]
        return np.mean(v, axis=0) if v else None

    for k in (7, 14, 21, 28, 35):
        cache = {}

        def cf(r, k=k, cache=cache):
            key = (r["flt"], r["dep"])
            if key not in cache:
                c = near(by_flt[r["flt"]], r["dep"], k)
                if c is None:
                    c = near(by_dir[(r["orig"], r["dest"])], r["dep"], k)
                if c is None:
                    c = cm_all[r["dep"].month]
                cache[key] = c
            return cache[key]
        out["same flight within %d days" % k] = C.forecast(rows, dcs, dcps, cf)[0]
    c_dm, _ = C.curves(rows, lambda r: (r["orig"], r["dest"], r["dep"].month), keep=lambda r: C.is_nine(r["orig"], r["dest"]))
    out["route direction and month, own open"] = C.forecast(
        rows, dcs, dcps, lambda r: c_dm.get((r["orig"], r["dest"], r["dep"].month), cm_all[r["dep"].month]))[0]
    cache30 = {}

    def w30(r):
        if r["dep"] not in cache30:
            v = []
            for k in range(-30, 31):
                v.extend(by_day.get(r["dep"] + dt.timedelta(days=k), []))
            cache30[r["dep"]] = np.mean(v, axis=0)
        return cache30[r["dep"]]
    out["every open departure within 30 days"] = C.forecast(rows, dcs, dcps, w30)[0]
    med = defaultdict(list)
    for r in rows:
        if r["so"] == "" and not C.is_nine(r["orig"], r["dest"]) and r["bkd"][-1] > 0:
            med[r["dep"].month].append(r["bkd"] / r["bkd"][-1])
    cmed = {m: np.median(v, axis=0) for m, v in med.items()}
    out["month, median share"] = C.forecast(rows, dcs, dcps, lambda r: cmed[r["dep"].month])[0]
    return out


def selection_holdout(target, g=None, windows=(7, 14, 21, 28, 35)):
    """The other routes' open departures censored cell by cell to the nine routes' sold-out share of the month (as
    em_holdout); the departures held at the cap completed from the same flight's departures that stayed under it
    within k days (the same route direction's, then the month build, where none), and from the month build of
    every open departure off the nine routes (each departure left out); error in the demand above the cap."""
    g = g or C.golden(target)
    rows, dcps = g["rows"], g["dcps"]
    arr = np.array(dcps, float)
    sold = defaultdict(lambda: [0, 0])
    for r in rows:
        if C.is_nine(r["orig"], r["dest"]):
            sold[r["dep"].month][0] += r["so"] != ""
            sold[r["dep"].month][1] += 1
    f = {m: v[0] / v[1] for m, v in sold.items()}
    refs = [r for r in rows if r["so"] == "" and not C.is_nine(r["orig"], r["dest"]) and r["bkd"][-1] > 0]
    sums, cnt = defaultdict(lambda: 0), defaultdict(int)
    cells = defaultdict(list)
    for r in refs:
        sums[r["dep"].month] = sums[r["dep"].month] + r["bkd"] / r["bkd"][-1]
        cnt[r["dep"].month] += 1
        cells[((r["orig"], r["dest"]), r["dep"].month)].append(r)
    cap_of, held = {}, {}
    for (od, m), rs in cells.items():
        rs = sorted(rs, key=lambda r: (r["bkd"][-1], r["dep"], r["flt"]))
        n = len(rs)
        u = max(1, int(round((1 - f[m]) * n)))
        if u >= n:
            continue
        x = np.array([r["bkd"][-1] for r in rs], float)
        cap = (x[u - 1] + x[u]) / 2.0
        for k, r in enumerate(rs):
            cap_of[(r["flt"], r["dep"])] = cap
            held[(r["flt"], r["dep"])] = k >= u
    by_flt, by_dir = defaultdict(list), defaultdict(list)
    for r in refs:
        key = (r["flt"], r["dep"])
        if key in held and not held[key]:
            sh = r["bkd"] / r["bkd"][-1]
            by_flt[r["flt"]].append((r["dep"], sh))
            by_dir[(r["orig"], r["dest"])].append((r["dep"], sh))

    def near(lst, d, k):
        v = [sh for dd, sh in lst if abs((dd - d).days) <= k]
        return np.mean(v, axis=0) if v else None

    acc = defaultdict(lambda: defaultdict(float))
    for r in refs:
        key = (r["flt"], r["dep"])
        if not held.get(key):
            continue
        cap = cap_of[key]
        j = int(np.nonzero(r["bkd"] >= cap)[0][0])
        if j == 0:
            continue
        b0, b1 = r["bkd"][j - 1], r["bkd"][j]
        xx = arr[j - 1] - (arr[j - 1] - arr[j]) * ((cap - b0) / (b1 - b0) if b1 > b0 else 1.0)
        m = r["dep"].month
        mb = (sums[m] - r["bkd"] / r["bkd"][-1]) / (cnt[m] - 1)
        est = {"month": cap / C.interp(mb, dcps, xx)}
        for k in windows:
            c = near(by_flt[r["flt"]], r["dep"], k)
            if c is None:
                c = near(by_dir[(r["orig"], r["dest"])], r["dep"], k)
            if c is None:
                c = mb
            est["same flight within %d days" % k] = cap / C.interp(c, dcps, xx)
        for name, v in est.items():
            acc[name]["est"] += v
            acc[name]["actual"] += r["bkd"][-1]
            acc[name]["cap"] += cap
    return {name: (a["est"] - a["cap"]) / (a["actual"] - a["cap"]) - 1 for name, a in acc.items()}


# ------------------------------------------------------------------ censored-distribution fits: EM and Tobit
def em_grouped(x, c, gid, log=False, iters=5000, tol=1e-8):
    """EM for normal (or lognormal) demand with right-censored observations (c True where x is the cap), fitted
    separately in every group of gid at once; a censored unit is completed at its expected demand given that the
    demand exceeds its cap. A group with no uncensored unit keeps its units at the cap."""
    from scipy.special import log_ndtr, ndtr
    y = np.log(np.maximum(x, 0.5)) if log else np.asarray(x, float)
    levels, g = np.unique(gid, return_inverse=True)
    G = len(levels)
    n = np.bincount(g, minlength=G).astype(float)
    fit = np.bincount(g, ~c, G) > 0
    mu = np.bincount(g, y, G) / n
    sd = np.sqrt(np.maximum(np.bincount(g, y ** 2, G) / n - mu ** 2, 0.0))
    sd = np.maximum(sd, 0.05 if log else 5.0)
    floor = 1e-4 if log else 1.0

    def lam_of(z):
        if log:
            return np.exp(-0.5 * z * z - LOG_SQRT_2PI - log_ndtr(-z))
        return np.exp(-0.5 * z * z) / SQRT_2PI / np.maximum(ndtr(-z), 1e-12)

    active = fit.copy()
    for _ in range(iters):
        m, s = mu[g], sd[g]
        z = (y - m) / s
        lam = lam_of(z)
        e1 = np.where(c, m + s * lam, y)
        e2 = np.where(c, m ** 2 + s ** 2 + s * (y + m) * lam, y ** 2)
        mu2 = np.bincount(g, e1, G) / n
        sd2 = np.sqrt(np.maximum(np.bincount(g, e2, G) / n - mu2 ** 2, floor))
        done = (np.abs(mu2 - mu) < tol) & (np.abs(sd2 - sd) < tol)
        mu = np.where(active, mu2, mu)
        sd = np.where(active, sd2, sd)
        active &= ~done
        if not active.any():
            break
    m, s = mu[g], sd[g]
    z = (y - m) / s
    if log:
        ev = np.exp(m + s ** 2 / 2 + log_ndtr(-(z - s)) - log_ndtr(-z))
    else:
        ev = m + s * lam_of(z)
    return np.where(c & fit[g], ev, x)


SQRT_2PI = float(np.sqrt(2 * np.pi))
LOG_SQRT_2PI = float(np.log(SQRT_2PI))


def tobit(x, c, effects, log=False):
    """Censored normal (or lognormal) regression by maximum likelihood with a common sigma, the mean an intercept
    plus one fixed effect for every level of each key in effects but its first; a censored unit is completed at
    its expected demand given that the demand exceeds its cap."""
    from scipy.optimize import minimize
    from scipy.special import log_ndtr
    y = np.log(np.maximum(x, 0.5)) if log else np.asarray(x, float)
    idx, sizes = [], []
    for key in effects:
        levels, inv = np.unique(np.asarray(key), return_inverse=True)
        idx.append(inv)
        sizes.append(len(levels))
    k = 1 + sum(n - 1 for n in sizes)
    u = ~c

    def mean(p):
        mu = np.full(len(y), p[0])
        o = 1
        for inv, n in zip(idx, sizes):
            mu += np.r_[0.0, p[o:o + n - 1]][inv]
            o += n - 1
        return mu

    def nll(p):
        s = np.exp(p[k])
        z = (y - mean(p)) / s
        lc = log_ndtr(-z[c])
        lam = np.exp(-0.5 * z[c] ** 2 - LOG_SQRT_2PI - lc)
        g_mu = np.zeros(len(y))
        g_mu[u] = z[u] / s
        g_mu[c] = lam / s
        g_ls = np.where(u, z ** 2 - 1, 0.0)
        g_ls[c] = lam * z[c]
        f = -((-0.5 * z[u] ** 2 - p[k]).sum() - LOG_SQRT_2PI * u.sum() + lc.sum())
        grad = [g_mu.sum()]
        for inv, n in zip(idx, sizes):
            grad.extend(np.bincount(inv, g_mu, n)[1:])
        grad.append(g_ls.sum())
        return f, -np.array(grad)

    p0 = np.zeros(k + 1)
    p0[0] = float(y.mean())
    p0[k] = np.log(max(float(y.std()), 1e-3))
    res = minimize(nll, p0, jac=True, method="L-BFGS-B", options={"maxiter": 20000, "maxfun": 40000,
                                                                     "ftol": 1e-14, "gtol": 1e-9})
    mu = mean(res.x)
    s = float(np.exp(res.x[k]))
    z = (y - mu) / s
    if log:
        ev = np.exp(mu + s ** 2 / 2 + log_ndtr(-(z - s)) - log_ndtr(-z))
    else:
        ev = mu + s * np.exp(-0.5 * z * z - LOG_SQRT_2PI - log_ndtr(-z))
    return np.where(c, ev, x)


FITS = ("EM, route direction and month", "EM, route direction", "Tobit, route direction and month effects")


def _fit(name, x, c, dirs, months, log):
    """One censored-distribution fit over a set of departures: x the final bookings (the cap where censored)."""
    x = np.array(x, float)
    if name.startswith("EM"):
        key = ["%s|%02d" % (a, b) for a, b in zip(dirs, months)] if name.endswith("and month") else list(dirs)
        return em_grouped(x, c, np.array(key), log)
    return tobit(x, c, (dirs, months), log)


def censored_fits(target, g=None):
    """The call's figure under EM by route direction and month, EM by route direction and a Tobit with route
    direction and month fixed effects, each normal and lognormal, fitted to the nine routes' final bookings (a
    sold-out departure censored at its seats)."""
    g = g or C.golden(target)
    rows, dcs = g["rows"], g["dcs"]
    ns = C.noshow_by_leg(rows, dcs)
    nine = [r for r in rows if C.is_nine(r["orig"], r["dest"])]
    x = np.array([r["bkd"][-1] for r in nine], float)
    c = np.array([r["so"] != "" for r in nine])
    dirs = ["%s-%s" % (r["orig"], r["dest"]) for r in nine]
    months = [r["dep"].month for r in nine]
    base = sum(int(dcs[(r["flt"], r["dep"].isoformat())]["pax_flown"]) for r in nine)
    out = {}
    for log in (False, True):
        for name in FITS:
            e = _fit(name, x, c, dirs, months, log)
            tot = sum(min(v, C.seats_s26(r)) * (1 - ns[(r["orig"], r["dest"])]) for r, v in zip(nine, e))
            out[("lognormal " if log else "normal ") + name] = tot - base
    return out


def peak_cells(rows):
    """The nine routes' departures that never sold out, per route direction, in each month."""
    out = defaultdict(lambda: defaultdict(int))
    tot = defaultdict(lambda: defaultdict(int))
    for r in rows:
        if C.is_nine(r["orig"], r["dest"]):
            od = "%s-%s" % (r["orig"], r["dest"])
            tot[r["dep"].month][od] += 1
            out[r["dep"].month][od] += r["so"] == ""
    return {m: {od: (out[m][od], tot[m][od]) for od in tot[m]} for m in tot}


def nine_weights(rows):
    """The nine routes' sold-out departures by month: the weight each month's error carries in the call."""
    w = defaultdict(int)
    for r in rows:
        if C.is_nine(r["orig"], r["dest"]) and r["so"]:
            w[r["dep"].month] += 1
    return dict(w)


def profile(err, w):
    """A method's holdout error by month summarised: the worst month, and the mean and root mean square weighted
    by the nine routes' sold-out departures of each month."""
    ms = [m for m in err if m in w]
    tw = sum(w[m] for m in ms)
    return {"worst": max(abs(err[m]) for m in ms),
            "mean_w": sum(w[m] * err[m] for m in ms) / tw,
            "rms_w": float(np.sqrt(sum(w[m] * err[m] ** 2 for m in ms) / tw))}


def fit_holdouts(target, g=None):
    """The other routes' open departures censored two ways, and the demand above the cap completed by the month
    build (projection from the moment the bookings reached the cap, each departure left out of its month's build)
    and by every censored-distribution fit; error on the demand above the cap by departure month, and over the
    summer.

    per cell      each route direction and month censored so that the share held at the cap equals the nine
                  routes' sold-out share in that month (em_holdout's censoring)
    constant cap  one cap per route direction, at the quantile of its final bookings that holds the nine routes'
                  summer sold-out share above it, so the censored share rises with the month's demand as the nine
                  routes' does
    """
    g = g or C.golden(target)
    rows, dcps = g["rows"], g["dcps"]
    arr = np.array(dcps, float)
    sold = defaultdict(lambda: [0, 0])
    for r in rows:
        if C.is_nine(r["orig"], r["dest"]):
            sold[r["dep"].month][0] += r["so"] != ""
            sold[r["dep"].month][1] += 1
    f = {m: v[0] / v[1] for m, v in sold.items()}
    share = sum(v[0] for v in sold.values()) / sum(v[1] for v in sold.values())
    refs = [r for r in rows if r["so"] == "" and not C.is_nine(r["orig"], r["dest"]) and r["bkd"][-1] > 0]
    sums, cnt = defaultdict(lambda: 0), defaultdict(int)
    for r in refs:
        sums[r["dep"].month] = sums[r["dep"].month] + r["bkd"] / r["bkd"][-1]
        cnt[r["dep"].month] += 1
    w = nine_weights(rows)

    def per_cell():
        cells = defaultdict(list)
        for r in refs:
            cells[((r["orig"], r["dest"]), r["dep"].month)].append(r)
        sel, cap, held = [], [], []
        for (od, m), rs in sorted(cells.items(), key=lambda kv: (kv[0][0], kv[0][1])):
            rs = sorted(rs, key=lambda r: (r["bkd"][-1], r["dep"], r["flt"]))
            n = len(rs)
            u = max(1, int(round((1 - f[m]) * n)))
            if u >= n:
                continue
            x = np.array([r["bkd"][-1] for r in rs], float)
            cp = (x[u - 1] + x[u]) / 2.0
            for k, r in enumerate(rs):
                sel.append(r)
                cap.append(cp)
                held.append(k >= u)
        return sel, np.array(cap), np.array(held)

    def constant():
        by = defaultdict(list)
        for r in refs:
            by[(r["orig"], r["dest"])].append(r)
        sel, cap, held = [], [], []
        for od, rs in sorted(by.items()):
            rs = sorted(rs, key=lambda r: (r["dep"], r["flt"]))
            x = np.array([r["bkd"][-1] for r in rs], float)
            cp = float(np.floor(np.quantile(x, 1 - share))) + 0.5
            for r, v in zip(rs, x):
                sel.append(r)
                cap.append(cp)
                held.append(v > cp)
        return sel, np.array(cap), np.array(held)

    res = {"_share": share, "_weights": w}
    for label, build in (("per cell", per_cell), ("constant cap", constant)):
        sel, cap, held = build()
        x = np.array([r["bkd"][-1] for r in sel], float)
        xc = np.where(held, cap, x)
        dirs = ["%s-%s" % (r["orig"], r["dest"]) for r in sel]
        months = [r["dep"].month for r in sel]
        est = {}
        proj = x.copy()
        ok = held.copy()
        for i, r in enumerate(sel):
            if not held[i]:
                continue
            j = int(np.nonzero(r["bkd"] >= cap[i])[0][0])
            if j == 0:
                ok[i] = False
                continue
            b0, b1 = r["bkd"][j - 1], r["bkd"][j]
            xx = arr[j - 1] - (arr[j - 1] - arr[j]) * ((cap[i] - b0) / (b1 - b0) if b1 > b0 else 1.0)
            m = r["dep"].month
            cur = (sums[m] - r["bkd"] / r["bkd"][-1]) / (cnt[m] - 1)
            proj[i] = cap[i] / C.interp(cur, dcps, xx)
        est["month build"] = proj
        for log in (False, True):
            for name in FITS:
                est[("lognormal " if log else "normal ") + name] = _fit(name, xc, held, dirs, months, log)
        # not a fit a solver can run: the cells with every departure at the cap handed their true final bookings
        key = np.array(["%s|%02d" % (a, b) for a, b in zip(dirs, months)])
        lv, inv = np.unique(key, return_inverse=True)
        empty = (np.bincount(inv, ~held, len(lv)) == 0)[inv]
        est["_EM, route direction and month, empty cells at the truth"] = np.where(
            empty, x, est["normal EM, route direction and month"])
        mo = np.array(months)
        out = {}
        for name, e in est.items():
            err = {}
            for m in sorted(set(months)):
                mm = ok & (mo == m)
                if mm.sum():
                    err[m] = float((e[mm] - cap[mm]).sum() / (x[mm] - cap[mm]).sum() - 1)
            summer = float((e[ok] - cap[ok]).sum() / (x[ok] - cap[ok]).sum() - 1)
            out[name] = {"months": err, "summer": summer, **profile(err, w)}
        cs = {m: float(held[mo == m].mean()) for m in sorted(set(months))}
        out["_empty_cell_departures"] = int((empty & held).sum())
        out["_censored_share"] = cs
        out["_departures"] = int(len(sel))
        out["_held"] = int(held.sum())
        out["_projected"] = int(ok.sum())
        res[label] = out
    return res


def selection_holdout_uniform(target, g=None, share=0.85, windows=(7, 14, 21, 28, 35)):
    """The holdout a solver builds first: every open departure off the nine routes with 40 or more final bookings
    censored at share of them, completed from the same flight's other open departures within k days (the same
    route direction's, then the month build, where none) and from the month build (each departure left out); error
    in the demand above the cap."""
    g = g or C.golden(target)
    rows, dcps = g["rows"], g["dcps"]
    arr = np.array(dcps, float)
    refs = [r for r in rows if r["so"] == "" and not C.is_nine(r["orig"], r["dest"]) and r["bkd"][-1] > 0]
    sh = np.array([r["bkd"] / r["bkd"][-1] for r in refs])
    day = np.array([r["dep"].toordinal() for r in refs])
    mon = np.array([r["dep"].month for r in refs])
    sums = {m: sh[mon == m].sum(axis=0) for m in set(mon)}
    cnt = {m: int((mon == m).sum()) for m in set(mon)}
    by_flt, by_dir = defaultdict(list), defaultdict(list)
    for i, r in enumerate(refs):
        by_flt[r["flt"]].append(i)
        by_dir[(r["orig"], r["dest"])].append(i)
    by_flt = {k: np.array(v) for k, v in by_flt.items()}
    by_dir = {k: np.array(v) for k, v in by_dir.items()}

    def near(ix, i, k):
        m = (np.abs(day[ix] - day[i]) <= k) & (ix != i)
        return sh[ix[m]].mean(axis=0) if m.any() else None

    acc = defaultdict(lambda: defaultdict(float))
    for i, r in enumerate(refs):
        if r["bkd"][-1] < 40:
            continue
        cap = share * r["bkd"][-1]
        j = int(np.nonzero(r["bkd"] >= cap)[0][0])
        if j == 0:
            continue
        b0, b1 = r["bkd"][j - 1], r["bkd"][j]
        xx = arr[j - 1] - (arr[j - 1] - arr[j]) * ((cap - b0) / (b1 - b0) if b1 > b0 else 1.0)
        m = mon[i]
        mb = (sums[m] - sh[i]) / (cnt[m] - 1)
        est = {"month": cap / C.interp(mb, dcps, xx)}
        for k in windows:
            c = near(by_flt[r["flt"]], i, k)
            if c is None:
                c = near(by_dir[(r["orig"], r["dest"])], i, k)
            if c is None:
                c = mb
            est["same flight within %d days" % k] = cap / C.interp(c, dcps, xx)
        for name, v in est.items():
            acc[name]["est"] += v
            acc[name]["actual"] += r["bkd"][-1]
            acc[name]["cap"] += cap
    return {name: (a["est"] - a["cap"]) / (a["actual"] - a["cap"]) - 1 for name, a in acc.items()}
