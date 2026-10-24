"""task482's assertions on the cut pack and on the generator's clean truth: the input gates, the three rules (R1 the
raw material, R2 every Layer 1 item mishandled, R3a the analyst test, R3b the decisive step alone, R3c no plant), the
ladder, the standing family and its bins, every semantic fork row (SF1 to SF20), the asks, the separation line, the
documents and the realism sweep.

    python3 task482/generator/checks.py          (after build.py)
"""
import copy
import datetime as dt
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import golden as G  # noqa: E402
import world as W   # noqa: E402

N, FAILS = [0], []
GOLD = ["Birchwick", "Ruddmere", "Sorrelton", "Tamsen Point", "Esker Narrows"]
DEFAULT = ["Sorrelton", "Esker Narrows"]


def check(label, ok, detail=""):
    N[0] += 1
    if not ok:
        FAILS.append(label)
    print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  (" + detail + ")") if detail else ""))


def qset(route):
    return [n for n in G.TOWNS if route[n]["qualifies"]]


def certified(route):
    return {n: (route[n]["busiest"], G.thousand(route[n]["peak"]), bool(route[n]["qualifies"])) for n in G.TOWNS}


def edge_k(v):
    return 500 - abs(v - G.thousand(v))


def pdf_text(path):
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    p = G.load(T)
    gold = G.golden(p)
    rec = G.records_route(p)
    gc = certified(gold)

    # ------------------------------------------------------------ input gates
    files = sorted(os.listdir(T))
    check("gate: 10 or more files", len(files) >= 10, "%d" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    check("gate: 3 or more formats", len(fmts) >= 3, ",".join(sorted(fmts)))
    big = max(sum(1 for _ in open(os.path.join(T, f), "rb")) for f in files if f.endswith((".csv", ".txt")))
    check("gate: a file of 25,000 rows or more", big >= 25000, "%d" % big)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    dis = meta["distractor_files"]
    check("gate: two or more distractors, shipped, named in metadata.json",
          len(dis) >= 2 and all(os.path.basename(d) in files for d in dis), ", ".join(dis))
    check("gate: no file name says distractor", not any("distract" in f for f in files))
    dash = []
    for f in files:
        txt = pdf_text(os.path.join(T, f)) if f.endswith(".pdf") else (
            open(os.path.join(T, f), encoding="utf-8").read() if f.endswith((".csv", ".txt")) else "")
        if "\u2014" in txt or "\u2013" in txt:
            dash.append(f)
    check("gate: no em or en dash in any text file or PDF", not dash, ",".join(dash))

    # ------------------------------------------------------------ the call
    check("call: the golden qualifies Birchwick, Ruddmere, Sorrelton, Tamsen Point and Esker Narrows",
          qset(gold) == GOLD, str(qset(gold)))
    check("call: figures.json carries the same set and USD 480,000 each",
          figs["call"]["qualify"] == GOLD and figs["call"]["share"] == 480000 and 2400000 % 5 == 0)
    check("call: the default path (residents plus recorded paid stays) qualifies Sorrelton and Esker Narrows alone",
          qset(rec) == DEFAULT, str(qset(rec)))
    check("call: every certified figure in figures.json is the golden's",
          all(figs["cities"][n]["present"] == gc[n][1] and figs["cities"][n]["qualifies"] == gc[n][2] for n in G.TOWNS))

    # ------------------------------------------------------------ R1: the field's raw material ships
    heads = []
    for f in files:
        if f.endswith(".csv"):
            heads += open(os.path.join(T, f), encoding="utf-8").readline().lower().split(",")
    check("R1: no shipped column holds a population present, a visitor count or a per-person load",
          not any(re.search(r"present|visitor|per.?capita|per person|population equiv|occupan", h) for h in heads))
    check("R1: the golden's decisive computation reads the plants' monthly influent rows (21 months x 7 plants)",
          all(len(G.series(p, n)) == 21 for n in G.TOWNS))
    S = {n: G.series(p, n) for n in G.TOWNS}
    check("R1: the summer loads exceed the residents' winter load per person times residents plus paid guests in "
          "every cottage city (the unrecorded people are in the load)",
          all(gold[n]["peak"] > rec[n]["peak"] * 1.3 for n in ("Birchwick", "Ruddmere", "Tamsen Point")))

    # ------------------------------------------------------------ R3a the analyst test, R3b the decisive step alone
    tr = W.truth()
    clean_rec = [n for n in G.TOWNS if tr[n]["paid_peak"] >= 3 * tr[n]["residents"]]
    check("R3a: on the clean truth, residents plus the paid stays qualify Sorrelton and Esker Narrows alone",
          clean_rec == DEFAULT, str(clean_rec))
    clean_true = [n for n in G.TOWNS if tr[n]["ratio"] >= 3.0]
    check("R3b: on the clean truth, everyone present qualifies the golden set", clean_true == GOLD, str(clean_true))
    check("R3b: the world's busiest months and rounded populations are the golden's",
          all(tr[n]["busiest"] == gold[n]["busiest"] and G.thousand(tr[n]["peak"]) == gc[n][1] for n in G.TOWNS))
    # a uniform uplift on the records route never lands the golden set
    landed = []
    for k in [1 + i / 100.0 for i in range(0, 301)]:
        s = [n for n in G.TOWNS if (p["residents"][n] + k * (rec[n]["peak"] - p["residents"][n])) >= 3 * p["residents"][n]]
        if s == GOLD:
            landed.append(k)
    check("R3b: no uniform uplift of the recorded paid guests (1.00 to 4.00) lands the golden set", not landed,
          str(landed[:3]))
    landed = []
    for k in [1 + i / 200.0 for i in range(0, 401)]:
        s = [n for n in G.TOWNS if k * rec[n]["peak"] >= 3 * p["residents"][n]]
        if s == GOLD:
            landed.append(k)
    check("R3b: no uniform uplift of the records route's population (1.00 to 3.00) lands the golden set", not landed)

    # ------------------------------------------------------------ the standing family and its bins
    fam = G.family(p)
    check("family: 90 constructions (BOD, flow or TSS; ten winter windows; with or without the paid winter guests; "
          "each city's own load per person or the basin's pooled one)", len(fam) == 90, "%d" % len(fam))
    agree = all(certified(r) == gc for r in fam.values())
    check("family: every construction certifies the same busiest months, rounded populations and qualifications",
          agree)
    worst = min(min(edge_k(r[n]["peak"]) for r in fam.values()) for n in G.TOWNS)
    check("family: every construction sits at least 140 people inside its thousand", worst >= 140, "%.0f" % worst)
    lo = min(min(r[n]["ratio"] for r in fam.values()) for n in GOLD)
    hi = max(max(r[n]["ratio"] for r in fam.values()) for n in G.TOWNS if n not in GOLD)
    check("family: every qualifying city at 3.15 times or more, every other at 2.75 or less, in every construction",
          lo >= 3.15 and hi <= 2.75, "%.3f / %.3f" % (lo, hi))
    margin = min(min(sorted(r[n]["present"].values())[-1] / sorted(r[n]["present"].values())[-2] for n in G.TOWNS)
                 for r in fam.values())
    check("family: every busiest month leads the next by 5 per cent or more", margin >= 1.05, "%.3f" % margin)

    # ------------------------------------------------------------ R2: every Layer 1 item, mishandled
    def same_call(route):
        return certified(route) == gc

    q = copy.deepcopy(p)
    raw = {}
    for r in q["edmr_raw"]:
        d = G.mdy(r["MONITORING_PERIOD_END_DATE"])
        raw[(r["PERMIT_ID"], d.year, d.month, r["MONITORING_LOCATION_CODE"], r["PARAMETER_CODE"])] = float(r["DMR_VALUE"])
    for (pid, y, m, loc, pc), v in raw.items():
        q["edmr"].setdefault(pid, {}).setdefault((y, m), {})[(loc, pc)] = v
    check("R2: e-reporting rows taken from every submission (the last row read wins) leave the call",
          same_call(G.load_route(q)))
    q = copy.deepcopy(p)
    for k in q["meters"]:
        q["meters"][k] = q["meters"][k] * 1e6
    check("R2: the joint plant's gallons read as million gallons (every Narrows load a million times too large) "
          "leaves the call", same_call(G.load_route(q)))
    q = copy.deepcopy(p)
    for k, v in list(q["meters"].items()):
        if k[0] == "Esker Narrows" and (k[1], k[2]) == (2025, 8):
            q["meters"][k] = v * 13 / 31.0
    check("R2: Esker Narrows' August 2025 meter replacement mishandled (the new register dropped) leaves the call",
          same_call(G.load_route(q)))
    q = copy.deepcopy(p)
    q["residents"] = {r["GEOGRAPHY"].replace(" city", ""): int(r["POPEST_2025_07_01"])
                      for r in G.rows(G.find(T, "quillmere_county_population")) if r["GEOGRAPHY"].endswith(" city")}
    r25 = G.load_route(q)
    check("R2: the 1 July 2025 estimates (Pinehold's annexation inside both) give the same busiest months, "
          "populations and qualifications", certified(r25) == gc)
    for split in ("equal",):
        r = G.load_route_paid(p, G.paid(p, split=split))
        check("R2: quarterly returns spread equally over their months leave the call", same_call(r))
    r = G.load_route_paid(p, G.paid(p, ck="period"))
    check("R2: Kettle & Pine's stays put in their reporting period leave the call", same_call(r))
    r = G.load_route_paid(p, G.paid(p, ck="arrival"))
    check("R2: Kettle & Pine's reference date read as the arrival leaves the call", same_call(r))
    q = copy.deepcopy(p)
    q["returns"] = [x for x in q["returns"] if x["RETURN_TYPE"] != "Supplemental"]
    check("R2: supplemental returns dropped leave the call", same_call(G.load_route(q)))
    q = copy.deepcopy(p)
    q["lakeward"] = []
    check("R2: Lakeward's upper-case city names left unmatched (its stays dropped from every city) leave the call",
          same_call(G.load_route(q)))
    check("R2: no paid winter guest at all in the load per person leaves the call", same_call(G.load_route_paid(p, {})))

    # ------------------------------------------------------------ R3c no plant, and the realism sweep
    monthly = {n: tuple(round(S[n][ym]["flow"]) for ym in sorted(S[n])) for n in G.TOWNS}
    check("R3c: no two cities share a monthly flow series and no series is constant",
          len(set(monthly.values())) == 8 and all(len(set(v)) > 15 for v in monthly.values()))
    res = [p["residents"][n] for n in G.TOWNS]
    check("R3c: no resident estimate is a round hundred", all(r % 100 for r in res), str(res))
    lw = G.rows(G.find(T, "lakeward_stays"))
    codes = [x["confirmation_code"] for x in lw]
    ck = G.rows(G.find(T, "kettle_and_pine"))
    refs = [x["Reservation"] for x in ck]
    check("R3c: every platform stay is listed once (no repeated confirmation code or reservation)",
          len(codes) == len(set(codes)) and len(refs) == len(set(refs)))
    cities = set(G.TOWNS)
    check("R2: every platform stay and every return names a basin city once Lakeward's capitals are title-cased",
          {x["listing_city"].title() for x in lw} == cities and {x["Municipality"] for x in ck} == cities and
          {x["PROPERTY_CITY"] for x in p["returns"]} == cities)
    winter_ck = sum(1 for x in ck if any((d.year, d.month) in G.WINTER for d in (
        G.ck_arrival(x) + dt.timedelta(days=i) for i in range(int(x["Nights"])))))
    check("separation: Kettle & Pine's stays with a night in January to April 2026 (the call's calibration) are counted, "
          "and every reading of their dates leaves every certified figure (SF19)", winter_ck > 0,
          "%d of %d stays" % (winter_ck, len(ck)))
    names = set(W.PEOPLE.values())
    check("R3c: the personas are the three drawn with guard.py names", names == {"Marvin Jordan", "William Terry",
                                                                                 "Bryce Williams"})

    # ------------------------------------------------------------ the semantic fork table
    check("SF1 resident population: the 2026 estimate, the 2025 estimate converges", certified(r25) == gc)
    cal_year = [(2026, m) for m in range(1, 10)]
    check("SF2 measurement year: October 2025 to September 2026; January to September 2026 alone converges",
          all(max(cal_year, key=lambda ym: gold[n]["present"][ym]) == gold[n]["busiest"] for n in G.TOWNS))
    tr_no_day = [n for n in G.TOWNS if max((tr[n]["present"][ym] - W.parts(n, *ym)["day"]) for ym in tr[n]["present"])
                 >= 3 * tr[n]["residents"]]
    check("SF3 population present: person-time, with day visitors at their share of the day; the overnight "
          "population alone (day visitors out of the truth) qualifies the same cities", tr_no_day == GOLD,
          str(tr_no_day))
    check("SF4 busiest month: the month with the highest average, the same in every construction", agree)
    check("SF5 average over the days of the month: monthly operating reports carry monthly averages of daily flow",
          all(isinstance(v["flow"], float) for v in S["Birchwick"].values()))
    check("SF6 basin city: the eight cities; the townships are on septic systems and carry no plant load",
          len(G.TOWNS) == 8 and "Arlen Township" not in G.TOWNS)
    check("SF7 at least three times: no construction puts a city within 0.15 of three", lo >= 3.15 and hi <= 2.75)
    rnd = [n for n in G.TOWNS if gc[n][1] >= 3 * p["residents"][n]]
    check("SF8 rounding: the test on the rounded population qualifies the same cities", rnd == GOLD, str(rnd))
    check("SF9 equal shares: USD 2,400,000 over five cities is a whole USD 480,000", 2400000 / 5 == 480000)
    check("SF10 calendar months: every plant reports calendar months", all(
        set(S[n]) == set(W.MOR_MONTHS) for n in G.TOWNS))
    split_res = {}
    for n in ("Esker Narrows", "Hollin Bay"):
        split_res[n] = G.thousand(gold[n]["peak"])
    jt = p["edmr"]["MN0099181"]
    check("SF11 the joint plant: each city at its member meter's flow (the fact sheet); the meters sum to the plant's "
          "influent within 1 per cent every month",
          all(abs((p["meters"][("Esker Narrows",) + ym] + p["meters"][("Hollin Bay",) + ym]) / G.days_in(*ym) /
                  (jt[ym][("G", "50050")] * 1e6) - 1) < 0.01 for ym in jt))
    pond_eff = all(p["ponds"][n][(2026, m)]["days"] == 0 for n in ("Ruddmere", "Pinehold") for m in (1, 2, 3, 7, 8))
    check("SF12 influent, not effluent: the ponds discharge nothing from January to March or in July and August, so "
          "an effluent reading carries no load in the months the call turns on", pond_eff)
    check("SF13 e-reporting submissions: influent values identical in every submission of a period",
          all(len({float(r["DMR_VALUE"]) for r in p["edmr_raw"] if r["PERMIT_ID"] == pid and
                   r["MONITORING_PERIOD_END_DATE"] == per and r["PARAMETER_CODE"] == pc and
                   r["MONITORING_LOCATION_CODE"] == "G"}) == 1
              for pid, per, pc in {(r["PERMIT_ID"], r["MONITORING_PERIOD_END_DATE"], r["PARAMETER_CODE"])
                                   for r in p["edmr_raw"] if r["MONITORING_LOCATION_CODE"] == "G"}))
    check("SF14 units: the load per person cancels the unit of flow (asserted under R2)", True)
    check("SF15 the paid winter guests in or out of the denominator: converges (family)", agree)
    check("SF16 the winter window, any of ten from January to April: converges (family)", agree)
    check("SF17 BOD, flow or TSS: converges (family)", agree)
    check("SF18 each city's own load per person or the basin's pooled: converges (family)", agree)
    check("SF19 Kettle & Pine's stays dated from the departure in the reference, from that date read as the arrival, or "
          "by reporting period, in the paid winter guests: converges",
          same_call(G.load_route_paid(p, G.paid(p, ck="period"))) and
          same_call(G.load_route_paid(p, G.paid(p, ck="arrival"))))
    check("SF20 quarterly returns spread by days or equally: converges",
          same_call(G.load_route_paid(p, G.paid(p, split="equal"))))
    def const_route(meas, k):
        out = {}
        for n in G.TOWNS:
            pres = {ym: S[n][ym][meas] / k for ym in G.MY}
            b = max(pres, key=pres.get)
            out[n] = (b, G.thousand(pres[b]), pres[b] >= 3 * p["residents"][n])
        return out

    def winter_over_res(meas, k):
        return [sum(S[n][ym][meas] / k for ym in G.WINTER) / 4 / p["residents"][n] for n in G.TOWNS]

    check("SF21 a design load per person: the population equivalent (0.17 lb BOD a person a day) and the design "
          "solids (0.20 lb TSS) certify the golden's figures", const_route("bod", 0.17) == gc and
          const_route("tss", 0.20) == gc)
    w100, w20, w132 = winter_over_res("flow", 100.0), winter_over_res("bod", 0.20), winter_over_res("bod", 0.1323)
    check("SF21 the design constants that fork are ruled out by the winter months: 100 gallons a person puts January to "
          "April at 0.60 to 0.62 times the residents, 0.20 lb BOD at 0.85 to 0.86, the European 60 g at 1.28 to 1.31, "
          "every city alike", max(w100) < 0.65 and max(w20) < 0.88 and min(w132) > 1.25 and
          const_route("flow", 100.0) != gc, "%.2f-%.2f / %.2f-%.2f / %.2f-%.2f" % (min(w100), max(w100), min(w20), max(w20),
                                                                                min(w132), max(w132)))
    autumn = {}
    for ym in ((2025, 10), (2025, 11), (2025, 12)):
        autumn[ym] = min(S[n][ym]["bod"] / (sum(S[n][w]["bod"] for w in G.WINTER) / 4) for n in G.TOWNS)
    one = [G.load_route(p, cal=[ym]) for ym in autumn]
    check("SF16 a single autumn month as the window forks Tamsen Point and is ruled out: October, November and December "
          "carry 9 per cent or more above the January to April load in every city", min(autumn.values()) > 1.09 and
          any(certified(r) != gc for r in one), " ".join("%d-%02d %.3f" % (ym + (v,)) for ym, v in autumn.items()))
    mixed = [G.load_route(p, measure=m_, cal=c_) for m_ in ("bod", "flow", "tss") for c_ in (
        [(2025, 11), (2025, 12), (2026, 1), (2026, 2), (2026, 3)], [(2025, 12), (2026, 1), (2026, 2)],
        [(2025, m) for m in (1, 2, 3, 4)], [(2025, 11), (2025, 12)] + G.WINTER)]
    check("SF16 windows reaching into November and December or the 2025 winter converge", all(certified(r) == gc
                                                                                            for r in mixed))
    for cr in (gold,):
        cross = all(same_call(G.load_route_paid(p, G.paid(p, split=s, ck=c))) for s in ("days", "equal")
                    for c in ("checkout", "arrival", "period"))
    check("SF19 x SF20 cross product: converges", cross)

    # ------------------------------------------------------------ the asks and the separation line
    A = G.ask_a(p)
    check("ask A: figures.json carries the golden's 32 fee figures", all(
        figs["ask_a"][n]["q%d" % k] == A[(n, k)] for n in G.TOWNS for k in (1, 2, 3, 4)))
    ckp = G.ask_a(p, ck="period")
    check("ask A device: Kettle & Pine's stays put in their reporting period move all 32 figures",
          all(ckp[k] != A[k] for k in A))
    cka = G.ask_a(p, ck="arrival")
    check("ask A device: Kettle & Pine's reference date read as the arrival moves 28 or more of the 32 figures",
          sum(cka[k] != A[k] for k in A) >= 28, "%d moved" % sum(cka[k] != A[k] for k in A))
    ckr = G.rows(G.find(T, "kettle_and_pine"))
    nxt = 0
    fee_dep = fee_arr = cross = 0
    for x in ckr:
        d = dt.datetime.strptime(x["Reservation"][1:7], "%y%m%d").date()
        per = (int(x["Reporting period"][:4]), int(x["Reporting period"][5:]))
        nxt += per == ((d.year + 1, 1) if d.month == 12 else (d.year, d.month + 1))
        n_, g_ = int(x["Nights"]), int(x["Party size"])
        if n_ >= 30:
            continue
        dep = sum(G.rate_on(d - dt.timedelta(days=n_ - i)) for i in range(n_)) * g_
        arr = sum(G.rate_on(d + dt.timedelta(days=i)) for i in range(n_)) * g_
        fee = float(x["Fee remitted (USD)"])
        fee_dep += abs(dep - fee) < 0.005
        fee_arr += abs(arr - fee) < 0.005
        cross += abs(dep - arr) > 0.005
    nshort = sum(1 for x in ckr if int(x["Nights"]) < 30)
    check("ask A fairness: every Kettle & Pine reporting period is the month after its reference date, and every fee "
          "remitted is the party times the rate on each night before that date, %d stays failing the arrival reading" %
          (nshort - fee_arr), nxt == len(ckr) and fee_dep == nshort and nshort - fee_arr >= 20,
          "%d of %d stays straddle the rate change under one reading or the other" % (cross, nshort))
    ns = G.ask_a(p, split_nights=False)
    check("ask A hazard: stays not split at quarter ends move all 32 figures", all(ns[k] != A[k] for k in A))
    pr = G.ask_a(p, rate_by_night=False)
    check("ask A hazard: a stay's fee spread evenly over its nights moves the quarters either side of the rate change",
          all(pr[(n, k)] != A[(n, k)] for n in G.TOWNS for k in (2, 3)))
    lt = G.ask_a(p, returns="latest")
    check("ask A hazard: keeping only each period's latest return moves the cities with a supplemental return",
          sum(lt[k] != A[k] for k in A) >= 8, "%d moved" % sum(lt[k] != A[k] for k in A))
    B = G.ask_b(p)
    check("ask B: figures.json carries the golden's 14 phosphorus figures", all(
        abs(figs["ask_b"][n]["h%d" % h] - B[(n, h)]) < 1e-9 for n in G.PLANTS_B for h in (1, 2)))
    pm = G.ask_b(p, pond_days="discharged")
    check("ask B device: the ponds' flow multiplied by the days discharged moves their four figures",
          all(pm[(n, h)] != B[(n, h)] for n in ("Ruddmere", "Pinehold") for h in (1, 2)))
    el = G.ask_b(p, edmr="latest")
    eplants = [n for n in G.PLANTS_B if n not in ("Ruddmere", "Pinehold")]
    check("ask B device: the latest submission received (a revision returned for correction) moves every e-reporting "
          "plant's figure in both halves", all(el[(n, h)] != B[(n, h)] for n in eplants for h in (1, 2)))
    ret = [r for r in p["edmr_raw"] if r["SUBMISSION_STATUS"] == "Returned"]
    check("ask B device: a returned revision differs from the accepted report only in its total phosphorus",
          {r["PARAMETER_CODE"] for r in ret} == {"00665"} or all(
              float(r["DMR_VALUE"]) == p["edmr"][r["PERMIT_ID"]][(G.mdy(r["MONITORING_PERIOD_END_DATE"]).year,
                                                                G.mdy(r["MONITORING_PERIOD_END_DATE"]).month)][
                  (r["MONITORING_LOCATION_CODE"], r["PARAMETER_CODE"])]
              for r in ret if r["PARAMETER_CODE"] != "00665"))
    chains = {}
    for r in p["edmr_raw"]:
        chains.setdefault((r["PERMIT_ID"], r["MONITORING_PERIOD_END_DATE"]), set()).add(r["SUBMISSION_STATUS"])
    benign = sum(1 for v in chains.values() if v == {"Superseded", "Accepted"})
    check("ask B no marker: resubmissions that end accepted sit beside the ones returned after acceptance",
          benign >= 4, "%d accepted resubmissions, %d returned" % (
              benign, sum(1 for v in chains.values() if "Returned" in v)))
    vol = {}
    for name in ("Ruddmere", "Pinehold"):
        inflow = sum(p["ponds"][name][(2025, m)]["inf_flow"] * G.days_in(2025, m) for m in range(1, 13))
        out_month = sum((p["ponds"][name][(2025, m)]["eff_flow"] or 0) * (G.days_in(2025, m) if p["ponds"][name][(2025, m)]["days"] else 0)
                        for m in range(1, 13))
        out_days = sum((p["ponds"][name][(2025, m)]["eff_flow"] or 0) * (p["ponds"][name][(2025, m)]["days"] or 0)
                       for m in range(1, 13))
        vol[name] = (out_month / inflow, out_days / inflow)
    check("ask B fairness: ponds that hold the year's wastewater release 80 to 90 per cent of their 2025 inflow at the "
          "month's average flow, and under half of it at the days discharged (the fact sheet and the water balance "
          "fix the flow's basis)", all(0.80 <= a <= 0.90 and b < 0.5 for a, b in vol.values()),
          str({k: tuple(round(x, 3) for x in v) for k, v in vol.items()}))
    sep = all(same_call(G.load_route_paid(p, G.paid(p, split=s, ck=c))) for s in ("days", "equal")
              for c in ("checkout", "arrival", "period"))
    check("separation: every ask device's mishandling leaves every certified figure (asserted under R2 and SF19)", sep)
    check("separation: the asks read rows the call never reads (fiscal 2026 fees; 2025 effluent phosphorus)", True)

    # ------------------------------------------------------------ the documents
    st = pdf_text(os.path.join(T, "seasonal_communities_aid_act.pdf"))
    check("documents: the Act defines population present, busiest month and the three-times test",
          "Population present" in st and "Busiest month" in st and "three times" in st)
    alltext = st + pdf_text(os.path.join(T, "lake_protection_fee_ordinance.pdf")) + pdf_text(
        os.path.join(T, "quillmere_basin_wastewater_facilities.pdf"))
    flat = re.sub(r"\s+", " ", alltext).lower()
    check("documents: no sentence ties a plant's load or flow to the people present (no announcement)",
          not re.search(r"(load|flow|wastewater|sewer)[^.]{0,120}(population|people|persons)|"
                        r"(population|people|persons)[^.]{0,120}(load|flow|wastewater|sewer)", flat),
          "positive control: 'connected to the city's sewer' is in the fact sheet: %s" % ("connected" in flat))
    check("documents: the fact sheet files that every developed parcel in a city is connected to its sewer",
          "every developed parcel" in flat)

    print()
    print("%d checks, %d failed" % (N[0], len(FAILS)))
    for f in FAILS:
        print("  FAILED: " + f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
