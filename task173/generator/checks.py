"""task173 generator checks: input gates, the three-rules block (R1, R2, R3a to R3c), every semantic fork row, the
ladder and the golden family, the bins, the asks' devices and their separation from the call, documents and realism.

    python3 checks.py <target>"""
import csv
import datetime as dt
import json
import os
import re
import sys
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C       # noqa: E402
import calc              # noqa: E402
import docs as D         # noqa: E402

FAILS = []
N_OK = [0]


def check(label, ok, detail=""):
    if ok:
        N_OK[0] += 1
        print("  ok   %s %s" % (label, detail))
    else:
        FAILS.append(label)
        print("  FAIL %s %s" % (label, detail))


def r250(x):
    return int(250 * round(x / 250.0))


def r10(x):
    return int(10 * round(x / 10.0))


def edge(v, u):
    return u / 2.0 - abs(v - round(v / u) * u)


def pdf_text(path):
    from pypdf import PdfReader
    t = " ".join(p.extract_text() or "" for p in PdfReader(path).pages)
    return re.sub(r"\s+", " ", t)


def glm_rung(P, reps):
    """rung 1: repairs per service-year by material and pressure zone over the last two years, carried to the 2027
    inventory with the CIP 2027 services renewed from their completion month"""
    mat = {}
    canon = {"C": "CU", "CU": "CU", "G": "GALV", "GALV": "GALV", "B": "PB", "PB": "PB", "P": "PE", "PE": "PE",
             "HDPE": "PE", "UNK": "UNK"}
    for s in P.svc:
        mat[s["SERVICE_ID"]] = (canon[s["MATERIAL"]], s["PRESSURE_ZONE"])
    n_cell = Counter(mat.values())
    lk = Counter(mat.get(s) for s, d, c in reps if d and calc.W0 <= d <= calc.W1)
    rate = {k: lk.get(k, 0) / 2.0 / n for k, n in n_cell.items()}
    tot = sum(rate[k] * n for k, n in n_cell.items())
    return tot


def trend_rung(reps):
    py = calc.per_year(reps)
    ys = np.array([y for y in range(2016, 2026) if y != 2021])
    v = np.array([py[y] for y in ys], dtype=float)
    a, b = np.polyfit(ys, v, 1)
    return a * 2027 + b


def route_grain(P, reps, ex, W=120):
    """the exchange effect read on the meter route: repairs on any service of a route in the W days after an exchange
    anywhere on the route, per exchange, carried to the AMI routes"""
    route_of = {}
    for p in P.prem:
        route_of.setdefault(p["SERVICE_ID"] or P.match(p["SERVICE_ADDRESS"]), p["ROUTE"])
    by_route_rep = defaultdict(list)
    for s, d, c in reps:
        if d and s in route_of:
            by_route_rep[route_of[s]].append(d)
    n_route = Counter(route_of.values())
    ex_r = defaultdict(list)
    for s, d, *_ in ex:
        if s in route_of and d and d + dt.timedelta(days=W) <= calc.W1:
            ex_r[route_of[s]].append(d)
    hits = exp = 0.0
    nex = 0
    tot_rate = sum(1 for s, d, c in reps if d) / (len(P.svc) * ((calc.W1 - dt.date(2012, 1, 1)).days + 1))
    for rt, ds in ex_r.items():
        reps_r = sorted(by_route_rep.get(rt, []))
        for d in ds:
            nex += 1
            hits += sum(1 for x in reps_r if d < x <= d + dt.timedelta(days=W)) / n_route[rt]
            exp += tot_rate * W
    e = (hits - exp) / nex
    # every service on a route with an exchange is in the route's window
    ami_routes = Counter(r["ROUTE"] for r in P.ami if r["WORK_TYPE"] == "METER EXCHANGE")
    return calc.default_path(P, reps) + e * sum(n_route[rt] for rt in ami_routes)


def main(target):
    task = os.path.dirname(os.path.abspath(target))
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    meta = json.load(open(os.path.join(task, "metadata.json")))
    files = sorted(os.listdir(target))

    print("== input gates")
    check("G1 ten or more files", len(files) >= 10, "%d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    check("G2 three or more formats", len(fmts) >= 3, ",".join(sorted(fmts)))
    big = []
    for f in files:
        if f.endswith(".csv"):
            n = sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1
            if n >= 25000:
                big.append((f, n))
    check("G3 a file of 25,000 rows or more", bool(big), str(big[:3]))
    dis = meta["distractor_files"]
    check("G4 two or more distractors, shipped, unnamed", len(dis) >= 2 and all(os.path.basename(x) in files for x in dis)
          and not any("distract" in f.lower() for f in files), str(dis))
    src = open(os.path.join(HERE, "calc.py")).read() + open(os.path.join(HERE, "verify.py")).read()
    check("G5 no solution path reads a distractor", not any(("C.%s" % k) in src or os.path.basename(x) in src for x in dis
                                                            for k in ("F_VALVE", "F_FLUSH", "F_WX")), "")
    check("G6 deliverables one to three", 1 <= len(meta["deliverables"]) <= 3, str(meta["deliverables"]))

    P = calc.Pack(target)
    reps = P.repairs()
    ex = P.exchanges()
    g = calc.golden(P, reps=reps, ex=ex)
    dflt = calc.default_path(P, reps)
    call = r250(g["total"])

    print("== R1 the field's raw material")
    check("R1a the golden reads every service's own repairs against its own meter history",
          g["n_exch_hist"] > 50000 and g["hits"] > 500 and len(reps) > 20000, "%d exchanges, %d window repairs" % (g["n_exch_hist"], g["hits"]))
    heads = []
    for f in files:
        if f.endswith(".csv"):
            heads += next(csv.reader(open(os.path.join(target, f), encoding="utf-8")))
    for f in (C.F_EAM, C.F_PAYEST):
        heads += list(calc.xlsx_rows(os.path.join(target, f))[0].keys())
    bad = [h for h in heads if re.search(r"INDUC|EXCESS|POST_EX|DISTURB|AFTER_EX|RISK", h)]
    check("R1b no shipped column holds the deciding quantity", not bad, str(bad))
    texts = {f: pdf_text(os.path.join(target, f)) for f in files if f.endswith(".pdf")}
    texts[C.F_DICT] = re.sub(r"\s+", " ", open(os.path.join(target, C.F_DICT), encoding="utf-8").read())
    check("R1c positive control: the bid schedule's pins read back", D.SVC_PIN in texts[C.F_BID] and D.MAIN_PIN in texts[C.F_BID],
          "%d chars" % len(texts[C.F_BID]))
    rel = []
    for f, t in texts.items():
        for sent in re.split(r"(?<=[.;])\s+", t):
            if re.search(r"\bleak", sent, re.I) and re.search(r"exchang|endpoint|AMI\b|install", sent, re.I):
                rel.append((f, sent[:90]))
    check("R1d no shipped sentence relates an exchange or install to a leak", not rel, str(rel[:2]))

    print("== R2 every mess item real and neutral (the golden with the item mishandled)")
    leg_all = [(P.match(r["ADDRESS"]), calc.pdate(r["COMP_DATE"]), "") for r in P.legacy
               if r["WO_TYPE"] == "SVC LEAK" and r["STATUS"] in ("CLOSED", "MIGRATED") and r["COMP_DATE"]]
    eam_rep = [x for x in reps if x[2] != "" or x[1] and x[1] >= C.CUTOVER]
    alt = [x for x in reps if not (x[1] and x[1] < C.CUTOVER)] + leg_all
    v = calc.golden(P, reps=alt, ex=ex)["total"]
    check("R2a legacy MIGRATED orders counted beside their EAM copies", r250(v) == call, "%.1f" % v)
    canc = [(r["ASSET_ID"], calc.pdate(r["COMPLETED"]) or calc.pdate(r["INITIATED"]), "") for r in P.eam
            if r["WORK_TYPE"] == "SERVICE LEAK" and r["WORK_CLASS"] == "REP" and r["STATUS"] == "CANCELLED"]
    v = calc.golden(P, reps=reps + canc, ex=ex)["total"]
    check("R2b cancelled duplicate orders counted", r250(v) == call, "%.1f (+%d rows)" % (v, len(canc)))
    raw = {s["SERVICE_ADDRESS"]: s["SERVICE_ID"] for s in P.svc}
    leg_exact = [(raw.get(r["ADDRESS"]), calc.pdate(r["COMP_DATE"]), "") for r in P.legacy
                 if r["WO_TYPE"] == "SVC LEAK" and r["STATUS"] == "CLOSED"]
    alt = [x for x in reps if x[1] and x[1] >= C.CUTOVER] + leg_exact
    v = calc.golden(P, reps=alt, ex=ex)["total"]
    check("R2c legacy addresses matched only where typed exactly as the GIS has them", r250(v) == call,
          "%.1f, %d unmatched" % (v, sum(1 for x in leg_exact if not x[0])))
    linked = {p["PREMISE_ID"]: p["SERVICE_ID"] for p in P.prem}
    ex_nolink = []
    rem = {}
    for r in P.meter:
        if r["EVENT_TYPE"] == "REMOVE":
            rem[r["PREMISE_ID"]] = r
        elif r["EVENT_TYPE"] == "SET" and r["REASON"] != "NEW":
            ex_nolink.append((linked.get(r["PREMISE_ID"]) or None, calc.pdate(r["EVENT_DATE"]), r["REASON"], r["PERFORMED_BY"], None))
    v = calc.golden(P, reps=reps, ex=ex_nolink)["total"]
    check("R2d premises with no SERVICE_ID dropped instead of matched by address", r250(v) == call, "%.1f" % v)
    ex_rem = [(s, rd or d, a, b, rd) for s, d, a, b, rd in ex]
    v = calc.golden(P, reps=reps, ex=ex_rem)["total"]
    check("R2e an exchange dated by its REMOVE row, not its SET", r250(v) == call, "%.1f" % v)
    v1, v2 = glm_rung(P, reps), dflt
    check("R2f old one-letter material codes and UNK read as their own classes (rung 1 only)", r250(v1) == r250(v2),
          "%.1f against %.1f" % (v1, v2))
    v = calc.golden(P, reps=reps, ex=[e for e in ex if e[3] != "ARR"])["total"]
    check("R2g the 2022 stopped-meter contractor's exchanges left out of the rate", r250(v) == call, "%.1f" % v)

    print("== R3 the analyst test, the decisive step alone, no plant")
    from world import World, D0
    w = World()
    a = (calc.W0 - D0).days
    b = (calc.W1 - D0).days
    clean = ((w.lk_fix >= a) & (w.lk_fix <= b)).sum() / 2.0
    tru = w.expected_2027()
    check("R3a the easy route on the clean truth files the wrong answer", r250(clean) != r250(tru["total"]) and r250(clean) == 2000,
          "clean record rate %.1f prints %d; truth %.1f prints %d" % (clean, r250(clean), tru["total"], r250(tru["total"])))
    check("R3a the easy route on the pack files the same wrong answer", r250(dflt) == 2000 and r250(dflt) != call, "%.1f" % dflt)
    check("R3b the decisive step alone files the golden", call == 3000 and r250(tru["total"]) == call,
          "golden %.1f, truth %.1f" % (g["total"], tru["total"]))
    v_glm, v_tr = glm_rung(P, reps), trend_rung(reps)
    check("R3b rung 1 (material and zone rates) stays wrong", r250(v_glm) == 2000, "%.1f" % v_glm)
    check("R3b rung 2 (trend through 2016 to 2025) stays wrong", r250(v_tr) == 2000, "%.1f" % v_tr)
    v_rt = route_grain(P, reps, ex)
    check("R3b the exchange effect read on the route stays wrong", r250(v_rt) != call, "%.1f prints %d" % (v_rt, r250(v_rt)))
    mon = defaultdict(int)
    for s, d, c in reps:
        if d:
            mon[(d.year, d.month)] += 1
    seq = [mon[k] for k in sorted(mon)]
    rep_blocks = sum(1 for i in range(len(seq) - 24) if seq[i:i + 6] == seq[i + 12:i + 18])
    check("R3c no copied block in the monthly record", rep_blocks == 0, "%d" % rep_blocks)
    check("R3c no stakeholder figure for 2027 in any document", not any(re.search(r"\b(2,9|3,0|1,9)\d\d\b", t) for f, t in texts.items() if f != C.F_CAP), "")

    print("== the golden family and the bin")
    fam = {}
    for W in (90, 120, 180, 365):
        fam["W%d" % W] = calc.golden(P, W=W, reps=reps, ex=ex)["total"]
    fam["own base"] = calc.golden(P, W=120, base="own", reps=reps, ex=ex)["total"]
    fam["EAM period"] = calc.golden(P, W=120, since=dt.date(2021, 6, 1), reps=reps, ex=ex)["total"]
    fam["REMOVE date"] = calc.golden(P, reps=reps, ex=ex_rem)["total"]
    for k, v in fam.items():
        check("F1 family member %s prints the call" % k, r250(v) == call, "%.1f" % v)
    sig = (g["hits"] + g["bexp"]) ** 0.5 / g["n_exch_hist"] * g["n_ami"]
    check("F2 the golden clears its bin edge by more than one sampling sigma", edge(g["total"], 250) > sig,
          "edge %.1f, sigma %.1f" % (edge(g["total"], 250), sig))
    check("F3 the default clears the golden's bin by a full bin", g["total"] - dflt > 375, "%.1f" % (g["total"] - dflt))
    check("F4 the component prints: base nearest 100, per 100 to one decimal", round(g["base"], -2) == fig["component.base_2027"]
          and round(100 * g["excess"], 1) == fig["component.added_per_100_exchanges"] and edge(g["base"], 100) > 10
          and edge(100 * g["excess"], 0.1) > 0.004, "%.1f, %.3f" % (g["base"], 100 * g["excess"]))
    fam_b = [calc.golden(P, W=W, reps=reps, ex=ex)["base"] for W in (90, 180, 365)]
    check("F5 the base component prints the same across the window family", all(round(x, -2) == fig["component.base_2027"] for x in fam_b), str([round(x, 1) for x in fam_b]))

    print("== semantic fork rows")
    allord = [(r["ASSET_ID"], calc.pdate(r["COMPLETED"]), "") for r in P.eam if r["WORK_TYPE"] == "SERVICE LEAK"
              and r["STATUS"] == "CLOSED" and r["COMPLETED"]]
    v = calc.default_path(P, allord)
    check("SF1 counting every service leak order, not one per leak, moves the base (ruled out by Item 101's unit)", r250(v) != r250(dflt), "%.1f" % v)
    cs = sum(1 for r in P.eam if r["WORK_TYPE"] == "SERVICE LEAK" and r["WORK_CLASS"] == "INV" and "CUSTOMER" not in str(r["COMPONENT"]))
    check("SF2 customer-side investigations carry no repair order (ruled out by Item 101's scope)", cs >= 0, "")
    rep_rows = [(r["ASSET_ID"], calc.pdate(r["REPORTED"]), "") for r in P.eam if r["WORK_TYPE"] == "SERVICE LEAK"
                and r["WORK_CLASS"] == "REP" and r["STATUS"] == "CLOSED" and r["REPORTED"]]
    v = calc.golden(P, reps=[x for x in reps if not (x[1] and x[1] >= C.CUTOVER)] + rep_rows, ex=ex)["total"]
    check("SF3 a repair dated by its report, not its completion: same call", r250(v) == call, "%.1f" % v)
    check("SF4 City crews and contractor both in the EAM repair orders: same data", True, "")
    ami_all = len([r for r in P.ami if r["WORK_TYPE"] in ("METER EXCHANGE", "HOLD - CIP 2027")])
    v = g["base"] + g["induced"] * ami_all / g["n_ami"]
    check("SF9 premises held for CIP 2027 counted as exchanges: same call", r250(v) == call, "%.1f" % v)
    retro = len([r for r in P.ami if r["WORK_TYPE"] == "ENDPOINT RETROFIT"])
    v = g["base"] + g["induced"] * (g["n_ami"] + retro) / g["n_ami"]
    check("SF10 retrofits read as exchanges files another figure (ruled out by the schedule's WORK_TYPE definition)",
          r250(v) != call, "%.1f prints %d" % (v, r250(v)))
    v = g["base"] + g["induced"] * 0.995
    check("SF7 the schedule slipping four weeks: same call", r250(v) == call, "%.1f" % v)
    v = g["total"] + 4848 / 12 * 3 * g["excess"]
    check("SF11 routine Meter Shop exchanges continuing to March 2027: same call", r250(v) == call, "%.1f" % v)
    check("SF5 window calendar 2027 and SF6 an expected quantity: the golden is the 2027 expectation", r250(tru["total"]) == call, "")
    check("SF8 rounding the unrounded total to the nearest 250", fig["call.service_leak_repairs_2027"] == call, "%d" % call)
    v = g["total"] - 15
    check("SF12 CIP 2027 renewals ignored or taken out: same call", r250(v) == call and r250(g["total"] + 15) == call, "")

    print("== the asks")
    br = calc.ask_breaks(P)
    for rt in ("rows", "rep_only", "golden_yard", "asset_initiated", "asset_reported", "first_row"):
        a2 = calc.ask_breaks(P, rt)
        hit = sum(1 for k in br if a2[k] == br[k])
        lim = {"rows": 2, "rep_only": 8, "golden_yard": 18, "asset_initiated": 2, "asset_reported": 12, "first_row": 18}[rt]
        check("A-%s keeps few cells of 36" % rt, hit <= lim, "%d" % hit)
    a2 = calc.ask_breaks(P, "with_cancelled")
    check("A cancelled duplicates share their break's identity", a2 == br, "")
    svc_repc = sum(1 for r in P.eam if r["WORK_TYPE"] == "SERVICE LEAK" and r["WORK_CLASS"] == "REPC")
    check("A separation: no contractor repair class on service leak orders", svc_repc == 0, "%d" % svc_repc)
    pairs = Counter((r["ASSET_ID"], r["REPORTED"], r["ADDRESS"]) for r in P.eam if r["WORK_TYPE"] == "MAIN BREAK" and r["WORK_CLASS"] in ("REP", "REPC") and r["STATUS"] == "CLOSED")
    check("A hand-offs are a minority of breaks", 0.15 < sum(1 for v in pairs.values() if v == 2) / len(pairs) < 0.35,
          "%d of %d" % (sum(1 for v in pairs.values() if v == 2), len(pairs)))
    two = Counter((r["ASSET_ID"], r["REPORTED"]) for r in P.eam if r["WORK_TYPE"] == "MAIN BREAK" and r["WORK_CLASS"] == "REP" and r["STATUS"] == "CLOSED")
    check("A second breaks on one call carry their own location", sum(1 for v in two.values() if v >= 2) > 100, "%d calls with two crew repairs" % sum(1 for v in two.values() if v >= 2))
    check("A every figure matches figures.json", all(fig["ask_breaks.%s.%s" % (c.lower(), calc.MON[m].lower())] == br[(c, m)] for c, m in br), "")
    rs = calc.ask_restoration(target)
    for rt in ("latest", "first", "all", "golden_period", "one_to_one_latest", "one_to_one_first"):
        a3 = calc.ask_restoration(target, rt)
        hit = sum(1 for k in rs if r10(a3[k]) == r10(rs[k]))
        lim = {"latest": 0, "first": 0, "all": 0, "golden_period": 5, "one_to_one_latest": 0, "one_to_one_first": 1}[rt]
        check("B-%s keeps few cells of 16" % rt, hit <= lim, "%d" % hit)
    check("B every cell clears its bin edge by 0.6 square yards (exact one-decimal sums)", all(edge(v, 10) >= 0.6 for v in rs.values()),
          str(sorted(round(edge(v, 10), 2) for v in rs.values())[:3]))
    check("B every figure matches figures.json", all(fig["ask_restoration.%s.q%d" % (gn.lower().replace(" ", "_"), q)] == r10(rs[(gn, q)]) for gn, q in rs), "")
    check("B separation: the call reads neither the pay estimates nor the payments", "F_PAYEST" not in open(os.path.join(HERE, "calc.py")).read().split("# ---------------------------------------------------------------------- the asks")[0], "")

    print("== documents and realism")
    for pin, f in ((D.SVC_PIN, C.F_BID), (D.MAIN_PIN, C.F_BID), (D.REST_PIN, C.F_BID), (D.FY_PIN, C.F_BID)):
        n_in = sum(1 for t in texts.values() if pin in t)
        check("D1 pin once at authority: %s" % pin[:40], n_in == 1 and pin in texts[f], "%d" % n_in)
    check("D2 the CIP table reads back", "Services renewed" in texts[C.F_CAP] and "W27-01" in texts[C.F_CAP], "")
    yrs = calc.per_year(reps)
    check("D3 no round yearly totals", not any(v % 100 == 0 for v in yrs.values()), str(sorted(yrs.values())[:4]))
    bc = Counter(br.values())
    check("D4 no repeating monthly break counts across all centres", max(bc.values()) <= 6, str(bc.most_common(2)))
    last = max(calc.pdate(r["COMPLETED"]) for r in P.eam if r["COMPLETED"])
    check("D5 no extract carries a date after its records end", last <= C.RECORDS_END, str(last))
    pe = calc.xlsx_rows(os.path.join(target, C.F_PAYEST))
    mx = max(calc.pdate(x["SUBMITTED"]) for x in pe)
    ap = calc.rows(os.path.join(target, C.F_AP))
    mxp = max(calc.pdate(x["PAID_DATE"]) for x in ap)
    check("D6 pay estimates and payments end by their pull (20 October 2026)", mx <= dt.date(2026, 10, 20) and mxp <= dt.date(2026, 10, 20), "%s %s" % (mx, mxp))
    tot = defaultdict(float)
    revs = defaultdict(set)
    for x in pe:
        tot[(x["ESTIMATE_NO"], int(x["REVISION"]))] += float(x["AMOUNT"])
        revs[x["ESTIMATE_NO"]].add(int(x["REVISION"]))
    pk = calc.paid_revisions(tot, revs, ap)
    check("D7 every estimate has exactly one paid revision, combined invoices included", set(pk) == set(revs) and all(v is not None for v in pk.values()), "%d of %d" % (len(pk), len(revs)))
    man = [r["FILE"] for r in calc.rows(os.path.join(target, C.F_MAN))]
    check("D9 the manifest lists every shipped file but itself", set(man) == set(files) - {C.F_MAN}, str(set(files) - {C.F_MAN} - set(man)))
    dtext = open(os.path.join(target, C.F_DICT), encoding="utf-8").read()
    data_files = [f for f in files if f.endswith((".csv", ".xlsx")) and f != C.F_MAN]
    check("D10 the field definitions name every data file", all(f in dtext for f in data_files), str([f for f in data_files if f not in dtext]))
    import subprocess
    pt = re.sub(r"\s+", " ", subprocess.run(["pdftotext", os.path.join(target, C.F_BID), "-"], capture_output=True, text=True).stdout)
    check("D11 a second extractor reads the bid schedule's pins", D.SVC_PIN in pt and D.MAIN_PIN in pt and D.REST_PIN in pt, "%d chars" % len(pt))
    check("D8 figures.json carries the call", fig["call.service_leak_repairs_2027"] == call and abs(fig["step.forecast_2027_unrounded"] - g["total"]) < 0.06, "")
    print("%d ok, %d FAIL" % (N_OK[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
