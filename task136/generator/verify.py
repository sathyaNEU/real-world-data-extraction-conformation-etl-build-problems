"""Independent verifier for task136. Reads only the shipped bundle (target/) and the golden workbook, imports nothing
from the generator, and recomputes on its own code path (csv, openpyxl, pypdf; no pandas): the base forecast, the
seven campaigns and the yield carried on each suburb's own uptake, the 2026 campaigns, every feeder's excess, the
call, the default path, the textbook reflex and the window variants, and the four DER Register figures by feeder.
Exits non-zero on any disagreement with the golden.

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

BASE = dt.date(2026, 8, 31)             # NPP-114 3.1: the last day of the month before the forecast is prepared
YEARS = 3                               # 31 August 2026 to the 31 August 2029 design point
FYS = [(dt.date(y, 7, 1), dt.date(y + 1, 6, 30)) for y in (2023, 2024, 2025)]
LAST_FY = FYS[-1]
LIVE = {"Connected", "Removed"}
OPEN_2026 = dt.date(2026, 9, 1)         # the council's letter: sign-ups open 1 September 2026
SUBURBS_2026 = ("Bindarra Waters", "Wattleview")
PORTAL = dt.date(2024, 7, 1)

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


def one_dp(x):
    return half_up(x, 0.1)


# ------------------------------------------------------------------------------------------------------------------
# the bundle

def read(target):
    B = {}
    net = rows(one(target, "nmi_network_model_"))
    B["feeder"] = {r["nmi"]: r["feeder"] for r in net}
    B["tariff"] = {r["nmi"]: r["tariff_class"] for r in net}
    B["locality"] = {r["nmi"]: r["locality"] for r in net}
    B["feeders"] = sorted(set(B["feeder"].values()))
    legacy = {r["legacy_application_no"]: float(r["inverter_kw_ac_each"]) * int(r["inverter_count"])
              for r in rows(one(target, "legacy_inverter_equipment"))}
    apps = []
    for r in rows(one(target, "eg_connection_applications_")):
        if r["inverter_kw_ac"]:
            kw = float(r["inverter_kw_ac"])
        elif r["legacy_application_no"]:
            kw = legacy[r["legacy_application_no"]]
        else:
            assert r["status"] == "Withdrawn", r["application_id"]
            kw = None
        apps.append(dict(nmi=r["nmi"], type=r["application_type"], status=r["status"], received=day(r["received_date"]),
                         connected=day(r["connection_date"]), removed=day(r["removal_date"]), kw=kw,
                         program=r["program_ref"], battery=float(r["battery_kwh"]) if r["battery_kwh"] else 0.0))
    B["apps"] = apps
    B["xref"] = defaultdict(list)
    for r in rows(one(target, "nmi_property_xref_")):
        B["xref"][r["property_no"]].append(r["nmi"])
    B["rates"] = rows(one(target, "merindah_rates_roll_"))
    wb = openpyxl.load_workbook(one(target, "solar_streets_program_summary"), data_only=True)
    head, log = None, []
    for row in wb["Campaigns"].iter_rows(values_only=True):
        if row and row[0] == "Year":
            head = list(row)
        elif head and row and isinstance(row[0], (int, float)) and row[1]:
            log.append(dict(zip(head, row)))
    B["log"] = log
    text = pdf(one(target, "solar_streets_2026_letter"))
    B["letter_text"] = text
    B["letter"] = {}
    for s in SUBURBS_2026:
        m = re.search(s + r"[^.]*?([\d,]+) (?:residential )?addresses", text)
        B["letter"][s] = int(m.group(1).replace(",", ""))
    text = pdf(one(target, "yarrabin_hosting_capacity_assessment"))
    B["hc29"], B["hc26"] = {}, {}
    for m in re.finditer(r"(YRB2\d) [\d.]+ [\d,]+ ([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)", text):
        B["hc26"][m.group(1)], B["hc29"][m.group(1)] = float(m.group(4)), float(m.group(5))
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
        if n in feeder:
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
# the campaigns: each suburb's owner-occupied houses, their first applications, the pool at the opening

def first_dates(B, use="received"):
    first = {}
    for a in B["apps"]:
        if a["status"] == "Withdrawn":
            continue
        d = a["received"] if use == "received" else a["connected"]
        if d is not None and (a["nmi"] not in first or d < first[a["nmi"]]):
            first[a["nmi"]] = d
    return first


def oo_nmis(B, suburb):
    out = []
    for r in B["rates"]:
        if r["land_use_code"] == "02" and r["rating_category"] == "R1" and r["locality"] == suburb.upper():
            out.extend(B["xref"].get(r["property_no"], []))
    return out


def suburb_feeder(B, suburb):
    c = Counter(B["feeder"][n] for n, loc in B["locality"].items() if loc == suburb)
    assert len(c) == 1, (suburb, c)
    return next(iter(c))


def stats(B, name, opening, first, firstc):
    nm = oo_nmis(B, name)
    res = [n for n, loc in B["locality"].items() if loc == name and B["tariff"][n] == "Residential"]

    def count(f, nmis, days):
        return sum(1 for n in nmis if n in f and opening - dt.timedelta(days=days) <= f[n] < opening)
    out = dict(feeder=suburb_feeder(B, name), oo=len(nm), n365=count(first, nm, 365), n730=count(first, nm, 730) / 2.0,
               n1095=count(first, nm, 1095) / 3.0, conn=count(firstc, nm, 365), all=count(first, res, 365), res=len(res))
    out["untapped"] = sum(1 for n in nm if not (n in first and first[n] < opening))
    u365 = sum(1 for n in nm if not (n in first and first[n] < opening - dt.timedelta(days=365)))
    t0 = opening - dt.timedelta(days=365)
    pt = 0.0
    for n in nm:
        d = first.get(n)
        if d is None or d >= opening:
            pt += 1.0
        elif d >= t0:
            pt += (d - t0).days / 365.0
    out["rate"] = out["n365"] / u365 * out["untapped"]
    out["persontime"] = out["n365"] / pt * out["untapped"]
    return out


def campaigns(B, first, firstc):
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
        st = stats(B, name, opening, first, firstc)
        st.update(suburb=name, opening=opening, letterboxed=int(row["Homes letterboxed"]),
                  systems=len(refs[ref_suburb[name]]), systems_log=int(row["Systems installed"]))
        out.append(st)
    return out


def pools(B, first, firstc):
    out = {}
    for name in SUBURBS_2026:
        st = stats(B, name, OPEN_2026, first, firstc)
        st.update(letterboxed=B["letter"][name])
        out[name] = st
    return out


def pooled_lift(camps, pl, basis):
    """NPP-114 4.2: the past programs' total systems over their combined total of the quantity the rate is per."""
    rate = sum(c["systems"] for c in camps) / sum(c[basis] for c in camps)
    return rate, {k: rate * p[basis] for k, p in pl.items()}


def forecast(B, base, avg, pl, lift):
    fc = dict(base)
    add = {}
    for k, n in lift.items():
        fc[pl[k]["feeder"]] += n * avg[pl[k]["feeder"]]
        add[k] = n * avg[pl[k]["feeder"]] / 1000.0
    ex = {f: fc[f] / 1000.0 - B["hc29"][f] for f in B["feeders"]}
    order = sorted(B["feeders"], key=lambda f: -ex[f])
    return fc, ex, order, add


# ------------------------------------------------------------------------------------------------------------------
# the DER Register figures by feeder

def site_key(B, nmi):
    k = nmi.strip()
    if len(k) == 11:
        k = k[:10]
    return B["realloc"].get(k, k)


def der_figures(B):
    """Per feeder: active sites (an NMI with an active AC connection, placed by the network model), the sites whose
    first AC connection of any status was lodged in FY2025-26, the active connections' inverter capacity (a
    two-inverter connection from the older portal carries the connection's total on each row) and their battery
    storage (a Sungrow SBR stack carries the stack's total on each module row)."""
    conns = {}
    for r in B["der"]:
        c = conns.setdefault(r["ac_connection_id"], dict(key=site_key(B, r["nmi"]), status=r["ac_connection_status"],
                                                         reg=day(r["registered_date"]), inv=[], bat=[]))
        if r["device_type"] == "Inverter":
            c["inv"].append((r["model"], float(r["rated_power_kw"])))
        else:
            c["bat"].append((r["model"], float(r["storage_capacity_kwh"])))
    first = {}
    for c in conns.values():
        if c["key"] not in first or c["reg"] < first[c["key"]]:
            first[c["key"]] = c["reg"]
    sites, new, inv, bat = Counter(), Counter(), defaultdict(float), defaultdict(float)
    seen = set()
    for c in conns.values():
        if c["status"] != "Active" or c["key"] not in B["feeder"]:
            continue
        f = B["feeder"][c["key"]]
        if c["key"] not in seen:
            seen.add(c["key"])
            sites[f] += 1
            if LAST_FY[0] <= first[c["key"]] <= LAST_FY[1]:
                new[f] += 1
        rated = [kw for _, kw in c["inv"]]
        m = re.search(r"(\d+\.\d)$", c["inv"][0][0]) if c["inv"] else None
        if len(rated) > 1 and m and abs(rated[0] - float(m.group(1)) * len(rated)) < 0.011:
            inv[f] += rated[0]
        else:
            inv[f] += sum(rated)
        if c["bat"]:
            if c["bat"][0][0] == "SBR HV battery":
                bat[f] += c["bat"][0][1]
            else:
                bat[f] += sum(k for _, k in c["bat"])
    return sites, new, inv, bat


# ------------------------------------------------------------------------------------------------------------------

def golden_book(golden):
    wb = openpyxl.load_workbook(os.path.join(golden, "feeder_upgrade_2029.xlsx"), data_only=True)
    ws = wb["Call"]
    call = [ws.cell(row=i, column=2).value for i in range(4, 11)]
    fcs = {}
    ws = wb["Forecast"]
    for i in range(4, 12):
        fcs[ws.cell(row=i, column=1).value] = [ws.cell(row=i, column=j).value for j in range(2, 11)]
    ws = wb["DER Register"]
    der = {ws.cell(row=i, column=1).value: tuple(ws.cell(row=i, column=j).value for j in range(2, 6)) for i in range(4, 12)}
    return call, fcs, der


def main(target, golden):
    FAIL.clear()
    PASSED[0] = 0
    B = read(target)
    feeders = B["feeders"]
    check(len(feeders) == 8 and set(B["hc29"]) == set(feeders), "eight feeders with a 2029 hosting capacity")
    check("A rate taken from past programs is their total systems divided by their combined total of the quantity the "
          "rate is expressed per." in B["npp"], "NPP-114 4.2")
    check("1 September 2026" in B["letter_text"], "the letter's opening date")
    cap, trend, base = base_forecast(B)
    avg = avg_new(B)
    first, firstc = first_dates(B), first_dates(B, "connected")
    camps = campaigns(B, first, firstc)
    pl = pools(B, first, firstc)
    check(len(camps) == 7, "seven past campaigns")
    for c in camps:
        check(c["systems"] == c["systems_log"], "%s: program references %d, council log %d" % (c["suburb"], c["systems"], c["systems_log"]))
        check(c["letterboxed"] == c["res"], "%s: letterboxed %d, residential NMIs %d" % (c["suburb"], c["letterboxed"], c["res"]))
    for k, p in pl.items():
        check(p["letterboxed"] == p["res"], "%s: letter %d, residential NMIs %d" % (k, p["letterboxed"], p["res"]))

    # the basis: the seven campaigns agree only per first application in the year before
    def cv(basis):
        v = [c["systems"] / c[basis] for c in camps]
        return statistics.stdev(v) / statistics.fmean(v)
    cv_up = cv("n365")
    check(0.06 <= cv_up <= 0.12, "uplift spread %.3f" % cv_up)
    for basis in ("letterboxed", "oo", "untapped"):
        check(cv(basis) >= 5 * cv_up, "basis %s spreads only %.3f" % (basis, cv(basis)))

    # the call
    rate, lift = pooled_lift(camps, pl, "n365")
    fc, ex, order, add = forecast(B, base, avg, pl, lift)
    w, ru = order[0], order[1]
    gap = ex[w] - ex[ru]
    check(w == "YRB27" and ru == "YRB24", "call %s, runner-up %s" % (w, ru))
    call, fcs, der_g = golden_book(golden)
    check(call[0] == w and call[2] == ru, "golden feeders %s %s" % (call[0], call[2]))
    for got, want, name in ((call[1], ex[w], "excess"), (call[3], ex[ru], "runner-up excess"), (call[4], gap, "gap"),
                            (call[5], add["Bindarra Waters"], "Bindarra Waters MW"),
                            (call[6], add["Wattleview"], "Wattleview MW")):
        check(abs(got - one_dp(want)) < 1e-9, "golden %s %s, verifier %.4f" % (name, got, want))
        k = want * 10
        check(abs((k - int(k)) - 0.5) >= 0.3, "%s %.4f sits near a rounding edge" % (name, want))
    for f in feeders:
        row = fcs[f]
        check(abs(row[0] - cap[f]) <= 0.5 + 1e-6 and abs(row[2] - base[f]) <= 0.5 + 1e-6 and abs(row[5] - fc[f]) <= 0.5 + 1e-6,
              "%s forecast row %s against %.1f %.1f %.1f" % (f, row, cap[f], base[f], fc[f]))
        check(abs(row[7] - one_dp(ex[f])) < 1e-9 and row[8] == order.index(f) + 1, "%s excess and rank" % f)

    # the window, the date and the population of the uplift converge on every graded figure
    graded = (w, ru, one_dp(ex[w]), one_dp(ex[ru]), one_dp(gap), one_dp(add["Bindarra Waters"]), one_dp(add["Wattleview"]))
    for basis in ("n730", "n1095", "conn", "all", "rate", "persontime"):
        _, lf = pooled_lift(camps, pl, basis)
        _, e2, o2, a2 = forecast(B, base, avg, pl, lf)
        g2 = (o2[0], o2[1], one_dp(e2[o2[0]]), one_dp(e2[o2[1]]), one_dp(e2[o2[0]] - e2[o2[1]]),
              one_dp(a2["Bindarra Waters"]), one_dp(a2["Wattleview"]))
        check(g2 == graded, "uplift variant %s files %s" % (basis, g2))
    # the default path and the reflex
    _, lf = pooled_lift(camps, pl, "letterboxed")
    _, e0, o0, _ = forecast(B, base, avg, pl, lf)
    check(o0[0] == "YRB24" and e0["YRB24"] / e0[o0[1]] >= 1.15 and o0.index("YRB27") + 1 in (4, 5),
          "default path files %s (YRB27 %d)" % (o0[0], o0.index("YRB27") + 1))
    _, lf = pooled_lift(camps, pl, "untapped")
    _, e1, o1, _ = forecast(B, base, avg, pl, lf)
    check(o1[0] == "YRB24" and e1["YRB24"] / e1[o1[1]] >= 1.15, "the reflex files %s" % o1[0])
    _, lf = pooled_lift(camps, pl, "oo")
    _, e3, o3, _ = forecast(B, base, avg, pl, lf)
    check(o3[0] != "YRB27", "per owner-occupied house files %s" % o3[0])
    # NPP-114 5.1 and the prompt name the design year's case; the 2026 case beside it is another quantity
    check("for the design year's spring minimum-demand case" in B["npp"], "NPP-114 5.1")
    _, e4, o4, _ = forecast(dict(B, hc29=B["hc26"]), base, avg, pl, lift)
    check(o4[0] != w or abs(e4[w] - ex[w]) > 0.05, "the 2026 case gives the 2029 figures")

    # the DER Register figures
    sites, new, inv, bat = der_figures(B)
    for f in feeders:
        want = (sites[f], new[f], half_up(inv[f], 10), half_up(bat[f], 10))
        check(tuple(der_g[f]) == want, "%s DER Register row golden %s, verifier %s" % (f, der_g[f], want))
        for x, name in ((inv[f], "inverter"), (bat[f], "storage")):
            k = x / 10
            check(abs((k - int(k)) - 0.5) >= 0.07, "%s %s %.2f near a rounding edge" % (f, name, x))
    check(os.path.getsize(os.path.join(golden, "yarrabin_pv_vs_hosting_2029.png")) > 20000, "the chart")

    if FAIL:
        for m in FAIL:
            print("VERIFY FAIL:", m)
        raise SystemExit(1)
    print("verify: %d checks passed from the bundle alone (%s %.3f MW above hosting capacity, runner-up %s %.3f, gap "
          "%.3f; Bindarra Waters %.3f MW and Wattleview %.3f MW; %.3f systems per first application)"
          % (PASSED[0], w, ex[w], ru, ex[ru], gap, add["Bindarra Waters"], add["Wattleview"], rate))
    return PASSED[0]


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "target")
    g = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "golden")
    main(t, g)
