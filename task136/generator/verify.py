"""Independent verifier for task136. Reads only the shipped bundle (target/) and the golden workbook, imports nothing
from the generator, and recomputes on its own code path (csv, openpyxl, pypdf; no pandas): the base forecast, the
seven campaigns and the transfer, the 2027 campaigns, every feeder's excess, the call, the default path and every
refused transfer basis, and both asks. Exits non-zero on any disagreement with the golden.

    python3 task136/generator/verify.py [target] [golden]"""
from __future__ import annotations

import csv
import datetime as dt
import os
import re
import statistics
import sys
from collections import Counter, defaultdict

import openpyxl
from pypdf import PdfReader

BASE = dt.date(2026, 8, 31)             # NPP-114 3.1: the month before the forecast is prepared
YEARS = 3                               # 31 August 2026 to the 31 August 2029 design point
FYS = [(dt.date(y, 7, 1), dt.date(y + 1, 6, 30)) for y in (2023, 2024, 2025)]
LAST_FY = FYS[-1]
LIVE = {"Connected", "Removed"}

FAIL = []
PASSED = [0]


def check(cond, msg):
    if cond:
        PASSED[0] += 1
    else:
        FAIL.append(msg)


def one(target, prefix):
    hits = [f for f in os.listdir(target) if f.startswith(prefix)]
    assert len(hits) == 1, (prefix, hits)
    return os.path.join(target, hits[0])


def rows(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def day(s):
    return dt.date.fromisoformat(s) if s else None


def pdf(path):
    return re.sub(r"\s+", " ", " ".join(pg.extract_text() or "" for pg in PdfReader(path).pages))


def half_up(x, unit):
    q = x / unit
    return int(q + 0.5) * unit if q >= 0 else -int(-q + 0.5) * unit


# ------------------------------------------------------------------------------------------------------------------
# the bundle

def read(target):
    B = {}
    net = rows(one(target, "nmi_network_model_"))
    B["feeder"] = {r["nmi"]: r["feeder"] for r in net}
    B["tariff"] = {r["nmi"]: r["tariff_class"] for r in net}
    B["locality"] = {r["nmi"]: r["locality"] for r in net}
    B["feeders"] = sorted(set(B["feeder"].values()))
    leg_rows = rows(one(target, "legacy_inverter_equipment"))
    legacy = {r["legacy_application_no"]: float(r["inverter_kw_ac_each"]) * int(r["inverter_count"]) for r in leg_rows}
    B["legacy_rows"], B["legacy_nos"], B["reg_legacy"] = len(leg_rows), set(legacy), []
    apps = []
    for r in rows(one(target, "eg_connection_applications_")):
        if r["legacy_application_no"]:
            B["reg_legacy"].append(r["legacy_application_no"])
        if r["inverter_kw_ac"]:
            kw = float(r["inverter_kw_ac"])
        elif r["legacy_application_no"]:
            kw = legacy[r["legacy_application_no"]]
        else:
            assert r["status"] == "Withdrawn", r["application_id"]
            kw = None
        apps.append(dict(nmi=r["nmi"], type=r["application_type"], status=r["status"], received=day(r["received_date"]),
                         connected=day(r["connection_date"]), removed=day(r["removal_date"]), kw=kw,
                         program=r["program_ref"]))
    B["apps"] = apps
    B["xref"] = defaultdict(list)
    for r in rows(one(target, "nmi_property_xref_")):
        B["xref"][r["property_no"]].append(r["nmi"])
    B["rates"] = rows(one(target, "merindah_rates_roll_"))
    wb = openpyxl.load_workbook(one(target, "solar_streets_program_summary"), data_only=True)
    ws = wb["Campaigns"]
    head, log = None, []
    for row in ws.iter_rows(values_only=True):
        if row and row[0] == "Year":
            head = list(row)
        elif head and row and isinstance(row[0], (int, float)) and row[1]:
            log.append(dict(zip(head, row)))
    B["log"] = log
    text = pdf(one(target, "solar_streets_2027_letter"))
    B["letter"] = {}
    for s in ("Bindarra Waters", "Wattleview"):
        m = re.search(s + r"[^.]*?([\d,]+) (?:residential )?addresses", text)
        B["letter"][s] = int(m.group(1).replace(",", ""))
    text = pdf(one(target, "yarrabin_hosting_capacity_assessment"))
    B["hc29"], B["hc26"], B["min_demand"] = {}, {}, {}
    for m in re.finditer(r"(YRB2\d) [\d.]+ [\d,]+ ([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)", text):
        B["hc26"][m.group(1)], B["hc29"][m.group(1)] = float(m.group(4)), float(m.group(5))
        B["min_demand"][m.group(1)] = (float(m.group(2)), float(m.group(3)))
    B["der"] = rows(one(target, "der_register_extract_"))
    B["realloc"] = {r["old_nmi"]: r["new_nmi"] for r in rows(one(target, "nmi_reallocations_"))}
    B["npp"] = pdf(one(target, "NPP-114"))
    return B


# ------------------------------------------------------------------------------------------------------------------
# NPP-114 2.2 and 3.2

def capacity(apps, feeder, when):
    latest = {}
    for a in apps:
        if a["status"] in LIVE and a["connected"] and a["connected"] <= when and not (a["removed"] and a["removed"] <= when):
            k = (a["connected"], 0 if a["type"] == "Alteration" else 1)
            if a["nmi"] not in latest or k > latest[a["nmi"]][0]:
                latest[a["nmi"]] = (k, a["kw"])
    out = defaultdict(float)
    for n, (_, kw) in latest.items():
        if n in feeder:                   # NPP-114 2.2: the NMIs the network model places on a feeder
            out[feeder[n]] += kw
    return out


def base_forecast(B):
    apps, feeder = B["apps"], B["feeder"]
    cap = capacity(apps, feeder, BASE)
    yearly = defaultdict(list)
    for s, e in FYS:
        c1, c0 = capacity(apps, feeder, e), capacity(apps, feeder, s - dt.timedelta(days=1))
        prog = defaultdict(float)
        for a in apps:
            if a["program"] and a["type"] == "New" and a["status"] in LIVE and s <= a["connected"] <= e and a["nmi"] in feeder:
                prog[feeder[a["nmi"]]] += a["kw"]
        for f in B["feeders"]:
            yearly[f].append(c1[f] - c0[f] - prog[f])
    trend = {f: sum(v) / len(v) for f, v in yearly.items()}
    return cap, trend, {f: cap[f] + YEARS * trend[f] for f in B["feeders"]}


def avg_new(B):
    s, e = LAST_FY
    by = defaultdict(list)
    for a in B["apps"]:
        if a["type"] == "New" and a["status"] in LIVE and s <= a["connected"] <= e and a["nmi"] in B["feeder"]:
            by[B["feeder"][a["nmi"]]].append(a["kw"])
    return {f: sum(v) / len(v) for f, v in by.items()}


# ------------------------------------------------------------------------------------------------------------------
# the campaigns

def first_application(B):
    first = {}
    for a in B["apps"]:
        if a["status"] != "Withdrawn":
            if a["nmi"] not in first or a["received"] < first[a["nmi"]]:
                first[a["nmi"]] = a["received"]
    return first


def oo_houses(B, suburb=None):
    out = []
    for r in B["rates"]:
        if r["land_use_code"] == "02" and r["rating_category"] == "R1" and (suburb is None or r["locality"] == suburb.upper()):
            out.append(r["property_no"])
    return out


def has_pv(B, first, prop, before, inclusive=False):
    for n in B["xref"].get(prop, []):
        d = first.get(n)
        if d is not None and (d <= before if inclusive else d < before):
            return True
    return False


def suburb_feeder(B, suburb):
    c = Counter(B["feeder"][n] for n, loc in B["locality"].items() if loc == suburb)
    assert len(c) == 1, (suburb, c)
    return next(iter(c))


def campaigns(B, first):
    refs = defaultdict(list)
    for a in B["apps"]:
        if a["program"] and a["type"] == "New" and a["status"] in LIVE:
            refs[a["program"]].append(a)
    ref_suburb = {}
    for ref, xs in refs.items():
        locs = Counter(B["locality"][a["nmi"]] for a in xs)
        assert len(locs) == 1, (ref, locs)
        ref_suburb[next(iter(locs))] = ref
    out = []
    for row in B["log"]:
        name = row["Suburb"]
        opening = row["Sign-ups opened"]
        opening = opening.date() if isinstance(opening, dt.datetime) else opening
        feeder = suburb_feeder(B, name)
        houses = oo_houses(B, name)
        untapped = sum(1 for p in houses if not has_pv(B, first, p, opening))
        systems = len(refs[ref_suburb[name]])
        res = [n for n, loc in B["locality"].items() if loc == name and B["tariff"][n] == "Residential"]
        udw = sum(1 for n in res if not (first.get(n) and first[n] < opening))
        feeder_houses = [p for p in oo_houses(B) if any(B["feeder"].get(n) == feeder for n in B["xref"].get(p, []))]
        feeder_unt = sum(1 for p in feeder_houses if not has_pv(B, first, p, opening))
        oo_nmis = {n for p in houses for n in B["xref"].get(p, [])}
        before12 = sum(1 for n in oo_nmis if first.get(n) and opening - dt.timedelta(days=365) <= first[n] < opening)
        out.append(dict(suburb=name, opening=opening, feeder=feeder, letterboxed=int(row["Homes letterboxed"]),
                        systems=systems, systems_log=int(row["Systems installed"]), oo=len(houses), untapped=untapped,
                        udw=udw, feeder_unt=feeder_unt, before12=before12, res=len(res)))
    return out


def pools(B, first):
    out = {}
    s, e = LAST_FY
    for name in ("Bindarra Waters", "Wattleview"):
        feeder = suburb_feeder(B, name)
        houses = oo_houses(B, name)
        unt_base = sum(1 for p in houses if not has_pv(B, first, p, BASE, inclusive=True))
        oo_nmis = {n for p in houses for n in B["xref"].get(p, [])}
        adopt = sum(1 for n in oo_nmis if first.get(n) and s <= first[n] <= e)
        res = [n for n, loc in B["locality"].items() if loc == name and B["tariff"][n] == "Residential"]
        udw = sum(1 for n in res if not (first.get(n) and first[n] <= BASE))
        feeder_houses = [p for p in oo_houses(B) if any(B["feeder"].get(n) == feeder for n in B["xref"].get(p, []))]
        feeder_unt = sum(1 for p in feeder_houses if not has_pv(B, first, p, BASE, inclusive=True))
        before12 = sum(1 for n in oo_nmis if first.get(n) and BASE - dt.timedelta(days=365) < first[n] <= BASE)
        out[name] = dict(feeder=feeder, letterboxed=B["letter"][name], oo=len(houses), untapped_base=unt_base,
                         adopt=adopt, untapped=unt_base - adopt, udw=udw, feeder_unt=feeder_unt, before12=before12,
                         res=len(res))
    return out


def transfer(camps, pl, basis):
    if basis == "none":
        return {k: 0.0 for k in pl}
    if basis == "count":
        m = statistics.fmean(c["systems"] for c in camps)
        return {k: m for k in pl}
    if basis == "ratio":
        m = statistics.fmean((c["systems"] + c["before12"]) / c["before12"] for c in camps)
        return {k: (m - 1) * p["before12"] for k, p in pl.items()}
    if basis == "untapped":
        rate = sum(c["systems"] for c in camps) / sum(c["untapped"] for c in camps)
        return {k: rate * p["untapped"] for k, p in pl.items()}
    m = statistics.fmean(c["systems"] / c[basis] for c in camps)
    return {k: m * p[basis] for k, p in pl.items()}


def forecast(B, base, avg, pl, lift):
    fc = dict(base)
    for k, n in lift.items():
        fc[pl[k]["feeder"]] += n * avg[pl[k]["feeder"]]
    ex = {f: fc[f] / 1000.0 - B["hc29"][f] for f in B["feeders"]}
    order = sorted(B["feeders"], key=lambda f: -ex[f])
    return fc, ex, order


# ------------------------------------------------------------------------------------------------------------------
# the asks

def n10(s):
    s = s.strip()
    return s[:10] if len(s) == 11 else s


def as_at_base(der):
    """The DER extract read as at 31 August 2026: later registrations dropped, later decommissionings undone."""
    out = []
    for r in der:
        if day(r["registered_date"]) > BASE:
            continue
        if r["ac_connection_status"] == "Decommissioned" and day(r["status_date"]) > BASE:
            r = dict(r, ac_connection_status="Active")
        out.append(r)
    return out


def ask_a(B):
    live = {}
    for a in B["apps"]:
        if a["status"] in LIVE and a["connected"] and a["connected"] <= BASE and not (a["removed"] and a["removed"] <= BASE):
            live[a["nmi"]] = True
    sites, any_rec = {}, set()
    for r in B["der"]:
        k = n10(r["nmi"])
        k = B["realloc"].get(k, k)
        any_rec.add(k)
        if r["ac_connection_status"] == "Active":
            sites.setdefault(k, r["feeder"])
    a, b = Counter(), Counter()
    for n in live:
        if n not in sites:
            a[B["feeder"][n]] += 1
    for k, f in sites.items():
        if k not in live:
            b[B["feeder"].get(k, f)] += 1
    only_dec = sum(1 for n in live if n not in sites and n in any_rec)
    return a, b, only_dec


def ask_b(B):
    conn = {}
    for r in B["der"]:
        if r["device_type"] == "Battery" and r["ac_connection_status"] == "Active":
            conn.setdefault(r["ac_connection_id"], (float(r["storage_capacity_kwh"]), r["feeder"], n10(r["nmi"])))
    by_col, by_net = defaultdict(float), defaultdict(float)
    for kwh, f, n in conn.values():
        by_col[f] += kwh
        n = B["realloc"].get(n, n)
        by_net[B["feeder"].get(n, f)] += kwh
    return by_col, by_net


# ------------------------------------------------------------------------------------------------------------------

def golden_book(golden):
    path = os.path.join(golden, "feeder_upgrade_2029.xlsx")
    wb = openpyxl.load_workbook(path, data_only=True)
    call = {wb["Call"].cell(row=i, column=1).value: wb["Call"].cell(row=i, column=2).value for i in range(4, 11)}
    fcs = {}
    ws = wb["Forecast"]
    for i in range(4, 12):
        fcs[ws.cell(row=i, column=1).value] = [ws.cell(row=i, column=j).value for j in range(2, 11)]
    der = {wb["DER Register check"].cell(row=i, column=1).value:
           (wb["DER Register check"].cell(row=i, column=2).value, wb["DER Register check"].cell(row=i, column=3).value)
           for i in range(4, 12)}
    bat = {wb["Battery storage"].cell(row=i, column=1).value: wb["Battery storage"].cell(row=i, column=2).value
           for i in range(4, 12)}
    return call, fcs, der, bat


def main(target, golden):
    FAIL.clear()
    PASSED[0] = 0
    B = read(target)
    feeders = B["feeders"]
    check(len(feeders) == 8 and set(B["hc29"]) == set(feeders), "eight feeders with a 2029 hosting capacity")
    same_day = Counter((a["nmi"], a["connected"]) for a in B["apps"] if a["status"] in LIVE)
    check(max(same_day.values()) == 1, "an NMI with two configurations connected on one day")
    check(all(a["kw"] <= 30.0 for a in B["apps"] if a["kw"] is not None), "a system above 30 kVA")
    check(B["legacy_rows"] == len(B["legacy_nos"]) and len(B["reg_legacy"]) == len(set(B["reg_legacy"]))
          and set(B["reg_legacy"]) == B["legacy_nos"], "legacy application numbers do not pair one to one")
    for f, (m26, m29) in B["min_demand"].items():
        dm, dh = m26 - m29, B["hc26"][f] - B["hc29"][f]
        check(min(0.6 * dm, 1.2 * dm) - 0.0051 <= dh <= max(0.6 * dm, 1.2 * dm) + 0.0051,
              "%s: the 2026 case is off the assessment's own sensitivity" % f)
    cap, trend, base = base_forecast(B)
    avg = avg_new(B)
    first = first_application(B)
    camps = campaigns(B, first)
    pl = pools(B, first)
    check(len(camps) == 7, "seven past campaigns")
    for c in camps:
        check(c["systems"] == c["systems_log"], "%s: program references %d, council log %d" % (c["suburb"], c["systems"], c["systems_log"]))
        check(c["letterboxed"] == c["res"], "%s: letterboxed %d, residential NMIs %d" % (c["suburb"], c["letterboxed"], c["res"]))
    for k, p in pl.items():
        check(p["letterboxed"] == p["res"], "%s: letter %d, residential NMIs %d" % (k, p["letterboxed"], p["res"]))

    # the transfer and the call
    rates = [c["systems"] / c["untapped"] for c in camps]
    rate = sum(c["systems"] for c in camps) / sum(c["untapped"] for c in camps)
    spread = statistics.pstdev(rates) / statistics.fmean(rates)
    check(spread < 0.01, "per untapped house spread %.4f" % spread)
    lift = transfer(camps, pl, "untapped")
    fc, ex, order = forecast(B, base, avg, pl, lift)
    w, ru = order[0], order[1]
    gap = ex[w] - ex[ru]
    check(w == "YRB24" and ru == "YRB22", "call %s, runner-up %s" % (w, ru))
    call, fcs, der_g, bat_g = golden_book(golden)
    gv = list(call.values())
    check(gv[0] == w, "golden feeder %s, verifier %s" % (gv[0], w))
    check(abs(gv[1] - round(ex[w], 1)) < 1e-9, "golden excess %s, verifier %.4f" % (gv[1], ex[w]))
    check(gv[2] == ru, "golden runner-up %s" % gv[2])
    check(abs(gv[3] - round(ex[ru], 1)) < 1e-9, "golden runner-up excess %s, verifier %.4f" % (gv[3], ex[ru]))
    check(abs(gv[4] - round(gap, 1)) < 1e-9, "golden gap %s, verifier %.4f" % (gv[4], gap))
    check(gv[5] == half_up(lift["Bindarra Waters"], 10), "golden Bindarra %s, verifier %.2f" % (gv[5], lift["Bindarra Waters"]))
    check(gv[6] == half_up(lift["Wattleview"], 10), "golden Wattleview %s, verifier %.2f" % (gv[6], lift["Wattleview"]))
    for f in feeders:
        row = fcs[f]
        check(abs(row[0] - cap[f]) <= 0.5 + 1e-6 and abs(row[2] - base[f]) <= 0.5 + 1e-6 and abs(row[5] - fc[f]) <= 0.5 + 1e-6,
              "%s forecast row %s against %.1f %.1f %.1f" % (f, row, cap[f], base[f], fc[f]))
        check(abs(row[7] - round(ex[f], 1)) < 1e-9 and row[8] == order.index(f) + 1, "%s excess and rank" % f)
    for x, unit, name in ((ex[w], 0.1, "excess"), (ex[ru], 0.1, "runner-up"), (gap, 0.1, "gap"),
                          (lift["Bindarra Waters"], 10, "Bindarra"), (lift["Wattleview"], 10, "Wattleview")):
        k = x / unit
        check(abs((k - int(k)) - 0.5) >= 0.07, "%s %.4f sits near a rounding edge" % (name, x))

    # the default path and every refused basis: each files YRB22, none lands a campaign figure
    for basis in ("none", "count", "letterboxed", "ratio", "oo", "udw", "feeder_unt"):
        lf = transfer(camps, pl, basis)
        _, e2, o2 = forecast(B, base, avg, pl, lf)
        check(o2[0] == "YRB22" and e2[o2[0]] / e2[o2[1]] >= 1.15, "basis %s files %s (margin %.2f)"
              % (basis, o2[0], e2[o2[0]] / e2[o2[1]]))
        if basis != "none":
            check(half_up(lf["Bindarra Waters"], 10) != gv[5] and half_up(lf["Wattleview"], 10) != gv[6],
                  "basis %s lands a campaign figure" % basis)
        if basis == "letterboxed":
            check(round(e2["YRB22"], 1) == 1.5 and o2.index("YRB24") + 1 in (4, 5), "default path %s at %.3f, YRB24 %d"
                  % (o2[0], e2[o2[0]], o2.index("YRB24") + 1))
        if basis != "none":
            if basis == "count":
                pred = [statistics.fmean(c["systems"] for c in camps)] * len(camps)
            elif basis == "ratio":
                m = statistics.fmean((c["systems"] + c["before12"]) / c["before12"] for c in camps)
                pred = [(m - 1) * c["before12"] for c in camps]
            else:
                m = statistics.fmean(c["systems"] / c[basis] for c in camps)
                pred = [m * c[basis] for c in camps]
            miss = max(abs(p - c["systems"]) / c["systems"] for p, c in zip(pred, camps))
            check(miss >= 0.25, "basis %s back-casts every campaign within %.2f" % (basis, miss))
    check(max(abs(rate * c["untapped"] - c["systems"]) for c in camps) <= 1.5, "the pooled rate back-casts each campaign")
    # estimators converge
    us = [c["untapped"] for c in camps]
    ss = [c["systems"] for c in camps]
    origin = sum(s * u for s, u in zip(ss, us)) / sum(u * u for u in us)
    for name, rr in (("mean", statistics.fmean(rates)), ("origin", origin), ("median", statistics.median(rates))):
        lf = {k: rr * p["untapped"] for k, p in pl.items()}
        _, e3, o3 = forecast(B, base, avg, pl, lf)
        check(o3[0] == w and round(e3[w], 1) == round(ex[w], 1) and half_up(lf["Bindarra Waters"], 10) == gv[5]
              and half_up(lf["Wattleview"], 10) == gv[6], "estimator %s moves a graded figure" % name)
    # "without PV" read as no live connected system at the date: the same graded figures
    def live_on(d):
        out = set()
        for a_ in B["apps"]:
            if a_["status"] in LIVE and a_["connected"] < d and not (a_["removed"] and a_["removed"] < d):
                out.add(a_["nmi"])
        return out
    def pool_live(name, d):
        lv = live_on(d)
        return sum(1 for p in oo_houses(B, name) if not any(n in lv for n in B["xref"].get(p, [])))
    camps_l = [dict(c, untapped=pool_live(c["suburb"], c["opening"])) for c in camps]
    pl_l = {k: dict(p, untapped=pool_live(k, BASE + dt.timedelta(days=1)) - p["adopt"]) for k, p in pl.items()}
    lf = transfer(camps_l, pl_l, "untapped")
    _, e5, o5 = forecast(B, base, avg, pl_l, lf)
    check(o5[0] == w and round(e5[w], 1) == round(ex[w], 1) and round(e5[w] - e5[o5[1]], 1) == round(gap, 1)
          and half_up(lf["Bindarra Waters"], 10) == gv[5] and half_up(lf["Wattleview"], 10) == gv[6],
          "the live-system reading of without PV moves a graded figure")
    # the 2026 case keeps the call; NPP-114 names the 2029 case
    _, e4, o4 = forecast(dict(B, hc29=B["hc26"]), base, avg, pl, lift)
    check(o4[0] == w, "the 2026 case files %s" % o4[0])
    check("at a residential or business NMI" in B["npp"] and "An alteration replaces the configuration it alters." in B["npp"],
          "NPP-114 2.1 and 2.2 sentences")

    # the asks
    a, b, only_dec = ask_a(B)
    check(only_dec == 0, "connected systems with only decommissioned DER records: %d" % only_dec)
    for f in feeders:
        check(der_g[f] == (a[f], b[f]), "%s DER Register check golden %s, verifier %s" % (f, der_g[f], (a[f], b[f])))
    mism = 0
    for r in B["der"]:
        k = n10(r["nmi"])
        k = B["realloc"].get(k, k)
        if k in B["feeder"] and B["feeder"][k] != r["feeder"]:
            mism += 1
    check(mism == 0, "the extract's feeder column differs from the network model on %d rows" % mism)
    a2, b2, _ = ask_a(dict(B, der=as_at_base(B["der"])))
    check(all((a2[f], b2[f]) == (a[f], b[f]) for f in feeders), "the DER Register as at 31 August 2026 moves a count")
    by_at, _ = ask_b(dict(B, der=as_at_base(B["der"])))
    by_col, by_net = ask_b(B)
    check(all(half_up(by_at[f], 10) == half_up(by_col[f], 10) for f in feeders), "storage as at 31 August 2026 moves")
    for f in feeders:
        check(abs(by_col[f] - by_net[f]) < 1e-9, "%s storage by the extract's feeder and the network model differ" % f)
        check(bat_g[f] == half_up(by_col[f], 10), "%s storage golden %s, verifier %.2f" % (f, bat_g[f], by_col[f]))
        k = by_col[f] / 10
        check(abs((k - int(k)) - 0.5) >= 0.07, "%s storage %.2f near a rounding edge" % (f, by_col[f]))
    check(os.path.getsize(os.path.join(golden, "yarrabin_pv_vs_hosting_2029.png")) > 20000, "the chart")

    if FAIL:
        for m in FAIL:
            print("VERIFY FAIL:", m)
        raise SystemExit(1)
    print("verify: %d checks passed from the bundle alone (%s %.3f MW above hosting capacity, runner-up %s %.3f, gap "
          "%.3f; Bindarra Waters %.1f and Wattleview %.1f systems; pooled %.3f per cent)"
          % (PASSED[0], w, ex[w], ru, ex[ru], gap, lift["Bindarra Waters"], lift["Wattleview"], 100 * rate))
    return PASSED[0]


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "target")
    g = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "golden")
    main(t, g)
