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
    for e in C.read_refusals(target):
        if not C.is_nine(e["orig"], e["dest"]):
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
