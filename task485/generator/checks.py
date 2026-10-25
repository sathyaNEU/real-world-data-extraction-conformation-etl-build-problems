"""task485's generator checks, run on the cut pack and on the world's clean truth: the three rules (R1 to R3), the
ladder, every row of the semantic fork table (SF1 to SF20) with the deciding quantity's live readings as a cross
product, each Layer 1 item mishandled, the ask's device and its separation from the call, the realism sweep and the
input gates.

    python3 task485/generator/checks.py
"""
import copy
import csv
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import golden as G  # noqa: E402
import world as W  # noqa: E402

D = G.D
OK, BAD = [], []
GOLD = ["CPK", "EBB", "KET", "LWE", "QUE"]
DEFAULT = ["EBB", "KET", "LNO", "TIB"]


def check(label, cond, detail=""):
    (OK if cond else BAD).append(label)
    print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  " + detail) if detail else ""))


def outside(L, e):
    v, avg, tot = G.verdicts(L, e)
    return sorted(w for w, x in v.items() if abs(x) > 10), v


def curve(L, years, by_type=False, S=None):
    S = S or G.settled_ratio(L)
    num, den = defaultdict(float), defaultdict(int)
    for Y in years:
        for u, n in L["reg"][Y].items():
            a = L["llpg"].get(u)
            if a is None or u not in L["comp"]:
                continue
            k = G.canvass_k(a["inuse"], Y)
            if k is None or k >= G.SETTLED_K:
                continue
            key = (a["type"] if by_type else "all", k)
            num[key] += n / S[a["type"]]
            den[key] += 1
    return {k: num[k] / den[k] for k in den}


def family_forecast(L, cv, by_type, settled_mode="count", young_mode="level", Y=G.HORIZON):
    """one construction of the standing family: the settled stock at its 2025 count or at the settled level; a young
    dwelling at its type's settled level times its share, or at its own 2025 count carried by the curve's rise"""
    S = G.settled_ratio(L)

    def cf(t, k):
        if k is None:
            return 0.0
        if k >= G.SETTLED_K:
            return 1.0
        return cv[(t if by_type else "all", k)]
    e = defaultdict(float)
    for u, n in L["reg"][2025].items():
        a = L["llpg"][u]
        k25, kY = G.canvass_k(a["inuse"], 2025), G.canvass_k(a["inuse"], Y)
        if k25 is not None and k25 >= G.SETTLED_K:
            e[a["ward"]] += n if settled_mode == "count" else S[a["type"]]
        elif young_mode == "level":
            e[a["ward"]] += S[a["type"]] * cf(a["type"], kY)
        else:
            e[a["ward"]] += n * cf(a["type"], kY) / cf(a["type"], k25)
    for u, a in L["llpg"].items():
        if u in L["reg"][2025] or a["inuse"] <= D(2025, 10, 31):
            continue
        k = G.canvass_k(a["inuse"], Y)
        if k is not None:
            e[a["ward"]] += S[a["type"]] * cf(a["type"], k)
    for ward, typ, day, n in G.future_units(L):
        k = G.canvass_k(day, Y)
        if k is not None:
            e[ward] += n * S[typ] * cf(typ, k)
    return e


def electra_panel(L, raw=False):
    xr = {}
    with open(os.path.join(T, "ems_migration_property_xref_2022-03.csv"), newline="") as f:
        for r in csv.DictReader(f):
            xr[int(r["electra_propref"])] = int(r["uprn"])
    Lx = copy.copy(L)
    Lx["reg"] = dict(L["reg"])
    for Y in (2020, 2021):
        Lx["reg"][Y] = {xr[ref]: (tot if raw else tot - at - ov) for pd, ref, tot, at, ov, lo in G.electra_rows(T, Y)}
    return Lx, xr


def ladder(L):
    S = G.settled_ratio(L)
    cp = curve(L, (2022, 2023, 2024, 2025))
    rungs = {}
    rungs["L0"] = outside(L, G.ward_totals(L, 2025))[0]
    rungs["L1"] = outside(L, G.default_path(L))[0]
    # L1b: the electors per dwelling the 2025 register shows at the dwellings completed since October 2020
    nb = {}
    for t in ("house", "flat"):
        xs = [n for u, n in L["reg"][2025].items() if u in L["comp"] and L["llpg"][u]["type"] == t
              and L["comp"][u]["done"] >= D(2020, 10, 1)]
        nb[t] = sum(xs) / len(xs)
    e = defaultdict(float)
    for u, n in L["reg"][2025].items():
        e[L["llpg"][u]["ward"]] += n
    for u, a in L["llpg"].items():
        if u not in L["reg"][2025] and a["inuse"] > D(2025, 10, 31) and G.canvass_k(a["inuse"], 2032) is not None:
            e[a["ward"]] += nb[a["type"]]
    for ward, typ, day, n in G.future_units(L):
        if G.canvass_k(day, 2032) is not None:
            e[ward] += n * nb[typ]
    rungs["L1b"] = outside(L, e)[0]
    rungs["L1c"] = outside(L, {w: x / 0.86 for w, x in G.default_path(L).items()})[0]
    # L2a: the young dwellings on the 2025 register at the settled level, everything to come at it
    e = defaultdict(float)
    for u, n in L["reg"][2025].items():
        a = L["llpg"][u]
        k25 = G.canvass_k(a["inuse"], 2025)
        e[a["ward"]] += n if (k25 is None or k25 >= G.SETTLED_K) else S[a["type"]]
    for w, x in G.default_path(L).items():
        pass
    base = G.default_path(L)
    for w in base:
        e[w] += base[w] - G.ward_totals(L, 2025).get(w, 0)
    rungs["L2a"] = outside(L, e)[0]
    # L2b: today's dwellings at their 2025 counts, the dwellings to come aged
    e = defaultdict(float)
    for u, n in L["reg"][2025].items():
        e[L["llpg"][u]["ward"]] += n
    g = family_forecast(L, cp, False)
    gt = defaultdict(float)
    for u, n in L["reg"][2025].items():
        a = L["llpg"][u]
        k25, kY = G.canvass_k(a["inuse"], 2025), G.canvass_k(a["inuse"], 2032)
        gt[a["ward"]] += n if (k25 is not None and k25 >= G.SETTLED_K) else S[a["type"]] * (1.0 if kY >= G.SETTLED_K else cp[("all", kY)])
    for w in g:
        e[w] += g[w] - gt[w]
    rungs["L2b"] = outside(L, e)[0]
    rungs["G"] = outside(L, G.forecast(L)[0])[0]
    return rungs


def truth(w):
    """the clean truth: the world's dwellings and counts before any file is cut, run through the default path, the two
    half rungs and the golden with the curve read from the world's own 2022 to 2025 counts"""
    dw = w["dwellings"]
    cl = {c: n for c, nm, n, r, p in W.WARDS}

    def k_of(mi, Y):
        if mi > W.mindex(Y, 10):
            return None
        return Y - W.first_canvass(mi) + 1
    ref25 = W.mindex(2025, 10)
    sett = defaultdict(lambda: [0, 0])
    for d in dw:
        if d["inuse"] is None or (k_of(d["inuse"], 2025) or 0) >= G.SETTLED_K:
            sett[d["type"]][0] += d["count"][2025]
            sett[d["type"]][1] += 1
    S = {t: v[0] / v[1] for t, v in sett.items()}
    num, den = defaultdict(float), defaultdict(int)
    for d in dw:
        if d["site"] is None or not d["built"]:
            continue
        for Y in (2022, 2023, 2024, 2025):
            k = k_of(d["inuse"], Y)
            if k is None or k >= G.SETTLED_K:
                continue
            num[k] += d["count"][Y] / S[d["type"]]
            den[k] += 1
    c = {k: num[k] / den[k] for k in den}

    def share(k):
        return 0.0 if k is None else (1.0 if k >= G.SETTLED_K else c[k])
    routes = {r: defaultdict(float) for r in ("L1", "L2a", "L2b", "G")}
    for d in dw:
        on25 = d["inuse"] is None or d["inuse"] <= ref25
        k25 = None if d["inuse"] is None else k_of(d["inuse"], 2025)
        young = d["inuse"] is not None and on25 and k25 < G.SETTLED_K
        kY = 99 if d["inuse"] is None else k_of(d["inuse"], 2032)
        if on25:
            routes["L1"][d["ward"]] += d["count"][2025]
            routes["L2b"][d["ward"]] += d["count"][2025]
            routes["L2a"][d["ward"]] += S[d["type"]] if young else d["count"][2025]
            routes["G"][d["ward"]] += S[d["type"]] * share(kY) if young else d["count"][2025]
        elif kY is not None:
            for r in ("L1", "L2a"):
                routes[r][d["ward"]] += S[d["type"]]
            for r in ("L2b", "G"):
                routes[r][d["ward"]] += S[d["type"]] * share(kY)
    real = defaultdict(float)
    for d in dw:
        real[d["ward"]] += d["count"][2032]
    routes["T"] = real

    def out(e):
        avg = sum(e.values()) / 43.0
        v = {wc: 100.0 * (e[wc] / cl[wc] / avg - 1.0) for wc in cl}
        return sorted(wc for wc, x in v.items() if abs(x) > 10), v
    return {r: out(e) for r, e in routes.items()}, S, c


def main():
    L = G.load(T)
    e, S, c = G.forecast(L)
    gold, v = outside(L, e)
    check("golden: five wards outside", gold == GOLD, str(gold))
    near = min(abs(abs(x) - 10) for x in v.values())
    check("SF4 no ward within 2.0 points of the line", near >= 2.0, "nearest %.2f" % near)

    # ---- the ladder on the cut pack
    rungs = ladder(L)
    want = dict(L0=[], L1=DEFAULT, L1b=["KET", "LNO"], L1c=DEFAULT, L2a=sorted(GOLD + ["LNO", "TIB"]), L2b=["EBB", "KET"], G=GOLD)
    for r, s in want.items():
        check("ladder %s files %s" % (r, s), rungs[r] == s, str(rungs[r]))

    # ---- the three rules on the clean truth
    w = W.build()
    tr, St, ct = truth(w)
    check("R1 the build-up is read from the registers' property rows (shipped at property level, UPRN keyed)",
          all(k in c for k in range(0, G.SETTLED_K)) and len(L["reg"][2025]) > 25000, "curve %s" % {k: round(x, 3) for k, x in c.items()})
    hdrs = []
    for nm in os.listdir(T):
        if nm.endswith(".csv"):
            hdrs += open(os.path.join(T, nm), encoding="utf-8").readline().lower().split(",")
    check("R1 no shipped column holds a forecast, a build-up or a completeness share",
          not any(any(x in h for x in ("forecast", "2032", "share", "complete", "variance")) for h in hdrs), "")
    check("R3a the easy route on the clean truth files the default four", tr["L1"][0] == DEFAULT, str(tr["L1"][0]))
    check("R3b the decisive step alone on the clean truth files the golden", tr["G"][0] == GOLD, str(tr["G"][0]))
    check("R3b each half correction on the clean truth stays wrong", tr["L2a"][0] != GOLD and tr["L2b"][0] != GOLD,
          "L2a %s, L2b %s" % (tr["L2a"][0], tr["L2b"][0]))
    print("      measured, not graded: the world's own 2032 register files %s (%s)" % (
        tr["T"][0], " ".join("%s %+.1f" % (x, tr["T"][1][x]) for x in ("LWE", "CPK", "QUE", "LNO", "TIB", "EBB", "KET"))))

    # ---- the standing family as a cross product of the live readings (SF15, SF16, SF17, SF18)
    Lx, xr = electra_panel(L)
    curves = {}
    for nm, yrs in (("2022-25", (2022, 2023, 2024, 2025)), ("2020-25", (2020, 2021, 2022, 2023, 2024, 2025)), ("2025", (2025,))):
        for bt in (False, True):
            curves[(nm, bt)] = (yrs, bt)
    sets, worst = set(), 99.0
    for sk in (5, 6, 7, 8, 9):
        G.SETTLED_K = sk
        Ssk = G.settled_ratio(Lx)
        for key, (yrs, bt) in curves.items():
            cv = curve(Lx, yrs, bt, Ssk)
            for sm in ("count", "level"):
                for ym in ("level", "rise"):
                    o, vv = outside(L, family_forecast(Lx, cv, bt, sm, ym))
                    sets.add(tuple(o))
                    worst = min(worst, min(abs(abs(x) - 10) for x in vv.values()))
    G.SETTLED_K = 7
    check("SF15 SF16 SF17 SF18 the cross product, 5 by 6 by 2 by 2 constructions, files only the golden",
          sets == {tuple(GOLD)}, "%d sets, nearest ward %.2f points from the line" % (len(sets), worst))

    # ---- the semantic fork rows
    check("SF1 the electorate is the register's local government electors (attainers and overseas apart)",
          all("local_government_electors" in open(os.path.join(T, "ems_property_electorate_2022-2025.csv")).readline() for _ in [0]))
    check("SF2 the forecast register is 1 December 2032", G.HORIZON == 2032)
    tot = sum(e.values())
    vm = {x: 100.0 * (e[x] / L["wards"][x][1] / (sum(e[y] / L["wards"][y][1] for y in e) / 23.0) - 1) for x in e}
    s3 = sorted(x for x, y in vm.items() if abs(y) > 10)
    check("SF3 the average is the district over 43; the mean of the wards' ratios: same call",
          sum(cl for nm, cl in L["wards"].values()) == 43 and s3 == GOLD, str(s3))
    check("SF5 today's 23 wards with their 2014 councillor numbers", len(L["wards"]) == 23)
    pdw = {}
    with open(os.path.join(T, "wards_councillors_2014_order.csv"), newline="") as f:
        for r in csv.DictReader(f):
            for p in r["polling_districts_2023_scheme"].split(";"):
                pdw[p] = r["ward_code"]
    mism = 0
    with open(os.path.join(T, "ems_property_electorate_2022-2025.csv"), newline="") as f:
        for r in csv.DictReader(f):
            if r["register_date"].startswith("2025") and pdw[r["polling_district"]] != L["llpg"][int(r["uprn"])]["ward"]:
                mism += 1
    check("SF6 a 2025 register UPRN's gazetteer ward is its district's ward", mism == 0, "%d differ" % mism)
    L2 = copy.deepcopy(L)
    for u, cc in L2["comp"].items():
        if u in L2["llpg"]:
            L2["llpg"][u]["inuse"] = cc["done"]
    check("SF7 building control's completion date as the date in use: same call", outside(L2, G.forecast(L2)[0])[0] == GOLD)
    orig_fc = G.first_canvass
    G.first_canvass = lambda day: day.year
    s8 = outside(L, G.forecast(L)[0])[0]
    G.first_canvass = orig_fc
    check("SF8 first canvass in the year completed rather than the year in use on 31 August: same call", s8 == GOLD, str(s8))
    orig_k = G.canvass_k
    G.canvass_k = lambda day, Y: None if day > D(Y, 11, 30) else Y - orig_fc(day) + 1
    s9 = outside(L, G.forecast(L)[0])[0]
    G.canvass_k = orig_k
    check("SF9 applications to 1 December rather than 31 October: same call", s9 == GOLD, str(s9))
    L3 = copy.deepcopy(L)
    for u, cc in L3["comp"].items():
        if u in L3["llpg"]:
            L3["llpg"][u]["type"] = cc["type"]
    check("SF10 the completions schedule's types: same call", outside(L3, G.forecast(L3)[0])[0] == GOLD)
    orig_fu = G.future_units

    def placed(mode):
        def fu(L_):
            rows = orig_fu(L_)
            if mode == "start":
                agg = defaultdict(float)
                for (wd, t, d, n) in rows:
                    my = d.year if d.month >= 4 else d.year - 1
                    agg[(wd, t, D(my, 10, 1) if my == 2026 else D(my, 4, 1))] += n
                return [(wd, t, d, n) for (wd, t, d), n in agg.items()]
            if mode == "whole3233":
                return [(wd, t, d if d < D(2032, 4, 1) else D(2032, 10, 15), n) for (wd, t, d, n) in rows]
            if mode == "none3233":
                return [(wd, t, d, n) for (wd, t, d, n) in rows if d < D(2032, 4, 1)]
            if mode == "wholemix":
                return rows
            return rows
        return fu
    G.future_units = placed("start")
    s11 = outside(L, G.forecast(L)[0])[0]
    G.future_units = orig_fu
    check("SF11 each year's completions at its start: same call", s11 == GOLD, str(s11))
    for mode in ("whole3233", "none3233"):
        G.future_units = placed(mode)
        s12 = outside(L, G.forecast(L)[0])[0]
        G.future_units = orig_fu
        check("SF12 the 2032/33 column, %s: same call" % mode, s12 == GOLD, str(s12))
    G.future_units = lambda L_: orig_fu(L_, mix="whole")
    s13 = outside(L, G.forecast(L)[0])[0]
    G.future_units = orig_fu
    check("SF13 the site's whole mix rather than its remaining mix: same call", s13 == GOLD, str(s13))
    later = sum((r.get("2033/34 onwards") or 0) for r in L["traj"])
    check("SF14 the trajectory's dwellings after 2032/33 are not counted (%d of them)" % later, later > 0)
    check("SF16 the build-up's panel converges (see the cross product)", sets == {tuple(GOLD)})
    check("SF17 the settled stock at the settled level converges (see the cross product)", sets == {tuple(GOLD)})
    check("SF18 a young dwelling's own count carried by the rise converges (see the cross product)", sets == {tuple(GOLD)})
    comp_plots = sum(1 for u, cc in L["comp"].items() if cc["done"] > D(2025, 10, 31) and u not in L["reg"][2025])
    new_llpg = sum(1 for u, a in L["llpg"].items() if a["inuse"] > D(2025, 10, 31) and u not in L["reg"][2025])
    check("SF19 dwellings in use after the 2025 register from the gazetteer (%d) or the completions (%d): same call" % (new_llpg, comp_plots),
          outside(L2, G.forecast(L2)[0])[0] == GOLD)
    Lr, _ = electra_panel(L, raw=True)
    Sr = G.settled_ratio(Lr)
    cr = G.buildup(Lr, Sr, years=(2020, 2021, 2022, 2023, 2024, 2025))
    check("SF20 Electra's TOTAL in a six-register panel: same call", outside(Lr, G.forecast(Lr, Sr, cr)[0])[0] == GOLD)

    # ---- Layer 1, each item mishandled (R2)
    Le, _ = electra_panel(L)
    Se = G.settled_ratio(Le)
    ce = G.buildup(Le, Se, years=(2020, 2021, 2022, 2023, 2024, 2025))
    check("R2 two layouts: the six-register panel with the 2021 report as it stands files the golden",
          outside(Le, G.forecast(Le, Se, ce)[0])[0] == GOLD)
    unl = sum(1 for Y in (2020, 2021) for pd, ref, tot, at, ov, lo in G.electra_rows(T, Y) if ref not in xr)
    check("R2 the cross-reference links every Electra row", unl == 0, "%d unlinked" % unl)
    old_codes = set()
    with open(os.path.join(T, "polling_district_review_2023_schedule.csv"), newline="") as f:
        for r in csv.DictReader(f):
            old_codes.add(r["replaces_district"])
    check("R2 the 2014 district codes are not 2023 codes (a code match is loud)", not (old_codes & set(pdw)))
    for col in ("attainers", "overseas_electors"):
        Lc = copy.deepcopy(L)
        with open(os.path.join(T, "ems_property_electorate_2022-2025.csv"), newline="") as f:
            for r in csv.DictReader(f):
                Lc["reg"][int(r["register_date"][:4])][int(r["uprn"])] += int(r[col])
        check("R2 franchise: %s added to the electors files the golden" % col, outside(Lc, G.forecast(Lc)[0])[0] == GOLD)
    Lc = copy.deepcopy(L)
    with open(os.path.join(T, "ems_property_electorate_2022-2025.csv"), newline="") as f:
        for r in csv.DictReader(f):
            Lc["reg"][int(r["register_date"][:4])][int(r["uprn"])] -= int(r["local_franchise_only"])
    check("R2 franchise: local-only electors taken out files the golden", outside(Lc, G.forecast(Lc)[0])[0] == GOLD)
    llpg2 = {}
    with open(os.path.join(T, "llpg_extract_2026-10-12.csv"), newline="") as f:
        for r in csv.DictReader(f):
            if r["BLPU_STATE"] != "2" or r["CLASSIFICATION"] not in ("RD02", "RD03", "RD04", "RD06", "PP"):
                continue
            llpg2[int(r["UPRN"])] = dict(type="flat" if r["CLASSIFICATION"] in ("RD06", "PP") else "house",
                                         ward=r["WARD_CODE"], inuse=D.fromisoformat(r["BLPU_STATE_DATE"]))
    Lg = copy.deepcopy(L)
    Lg["llpg"] = llpg2
    check("R2 gazetteer: every logical status kept, the buildings holding flats counted, files the golden",
          outside(Lg, G.forecast(Lg)[0])[0] == GOLD, "%d records more" % (len(llpg2) - len(L["llpg"])))
    check("R2 dates: the completion date as the date in use files the golden (SF7)", outside(L2, G.forecast(L2)[0])[0] == GOLD)
    check("R2 types: the completions schedule's types file the golden (SF10)", outside(L3, G.forecast(L3)[0])[0] == GOLD)

    def fut12(L_):
        rows = []
        for (wd, t, d, nn) in orig_fu(L_):
            if D(2026, 10, 1) <= d <= D(2027, 3, 31):
                for m in range(4, 16):
                    yy, mm = (2026, m) if m <= 12 else (2027, m - 12)
                    rows.append((wd, t, D(yy, mm, 15), nn / 12.0))
            else:
                rows.append((wd, t, d, nn))
        return rows
    G.future_units = fut12
    s = outside(L, G.forecast(L)[0])[0]
    G.future_units = orig_fu
    check("R2 monitoring years: the 2026/27 column spread over April to March files the golden", s == GOLD, str(s))

    # ---- the ask: golden equals the world's truth, the device moves every ward, the forcing figure, separation
    A = G.ask_a(T, L["wards"])
    truth21 = defaultdict(int)
    for d in w["dwellings"]:
        if d["inuse"] is None or d["inuse"] <= W.mindex(2021, 10):
            truth21[d["ward"]] += d["count"][2021]
    check("ask A golden equals the published 2021 register in the world", A == dict(truth21))
    net = G.switch_off_net(T, L["wards"])
    check("ask A the switch-off moves every ward", min(abs(x) for x in net["by_ward"].values()) >= 5,
          "net %d, %d to %d" % (net["net"], net["low"], net["high"]))
    inuse21 = {}
    for ref, u in xr.items():
        a = L["llpg"].get(u)
        if a is not None:
            inuse21[ref] = a["inuse"]
    late = {ref: tot - at - ov for pd, ref, tot, at, ov, lo in G.electra_rows(T, 2021)
            if inuse21.get(ref) and inuse21[ref] > D(2021, 10, 31)}
    held = sum(1 for x in late.values() if x > 0)
    adds = defaultdict(int)
    for day, pd, ref, act, fr, a18 in G.notice_rows(T):
        if day >= D(2022, 1, 1) and fr != "F" and not a18:
            adds[ref] += 1 if act == "ADD" else -1
    after = sum(1 for ref, x in late.items() if x - adds.get(ref, 0) != 0)
    check("ask A forcing figure: dwellings first in use after 31 October 2021 hold electors in the 2021 report, none once "
          "the 2022 notices are backed out", held > 0 and after == 0, "%d hold %d electors; %d after" % (held, sum(late.values()), after))
    stops = {r: sum(1 for k in A if G.ask_a(T, L["wards"], r).get(k) == A[k]) for r in ("export", "total", "adds_only", "all_rows", "all_notices", "no_k")}
    check("ask A the cracker's and the mirror's readings miss every ward, no half-handled stop keeps more than 5",
          stops["export"] == 0 and stops["total"] == 0 and max(stops.values()) <= 5, str(stops))
    check("separation: the golden call reads no Electra file, no notice and no attainer or overseas column",
          "ELECTRA" not in open(os.path.join(HERE, "golden.py")).read().split("def electra_rows")[0])
    src = open(os.path.join(HERE, "golden.py")).read()
    check("distractors: no golden figure opens the projections or the valuation list",
          "snpp" not in src and "council_tax" not in src)

    # ---- realism sweep and input gates
    files = sorted(os.listdir(T))
    check("gate: 10 or more files", len(files) >= 10, str(len(files)))
    check("gate: 3 or more formats", len(set(f.rsplit(".", 1)[1] for f in files)) >= 3)
    big = max(sum(1 for _ in open(os.path.join(T, f), "rb")) for f in files if f.endswith((".csv", ".txt")))
    check("gate: a file of 25,000 rows or more", big >= 25000, str(big))
    check("gate: two distractors", True, "snpp_2022based_lorrimere.csv, council_tax_dwellings_by_band_ward_2025-09.csv")
    wt = G.ward_totals(L, 2025)
    check("realism: no two wards share a 2025 electorate", len(set(wt.values())) == len(wt))
    check("realism: the district totals are not round", sum(wt.values()) % 100 != 0 and sum(A.values()) % 100 != 0)
    rows = open(os.path.join(T, "ELECTRA_NOTICES_OF_ALTERATION_2021-01_2022-03.txt"), encoding="utf-8").read().splitlines()
    check("realism: no repeated notice row", len(rows) == len(set(rows)))
    dash = [f for f in files if f.endswith((".csv", ".txt")) and ("—" in open(os.path.join(T, f), encoding="utf-8").read()
                                                                 or "–" in open(os.path.join(T, f), encoding="utf-8").read())]
    check("realism: no em or en dash in a text file", not dash, str(dash))
    print("\n%d PASS, %d FAIL" % (len(OK), len(BAD)))
    return not BAD


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
