"""Generator checks for task452 v3, run on the installed target/ and golden/ (and the clean truth where named).

    python3 task452/generator/checks.py          exit 1 on any failure
"""
import csv
import json
import math
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A        # noqa: E402
import golden as G          # noqa: E402
import world as W           # noqa: E402

TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
GLD = os.path.join(TASK, "golden")
RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))


def rh(x, u=1.0):
    return math.floor(x / u + 0.5) * u


def edge(x, u=1.0):
    return u / 2 - abs(x - rh(x, u))


def main():
    files = sorted(os.listdir(TGT))
    exts = {os.path.splitext(f)[1] for f in files}
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    # ---------------------------------------------------------------- input gates
    check("G1 ten or more files", len(files) >= 10, "%d files" % len(files))
    check("G2 three or more formats", len(exts) >= 3, ",".join(sorted(exts)))
    rows = sum(1 for _ in open(os.path.join(TGT, "PI_historian_K1K2_2026_30min.csv"))) - 1
    check("G3 a file of 25,000 rows or more", rows >= 25000, "historian %d rows" % rows)
    dis = meta["distractor_files"]
    check("G4 two or more distractors, each shipped", len(dis) >= 2 and all(os.path.exists(os.path.join(TASK, d)) for d in dis), str(dis))
    bad = [f for f in files if re.search(r"readme|dictionary|notes|manifest|field_guide|test_|trap|decoy|distractor|known_issue", f, re.I)]
    check("G5 no file name describing the data or the author's intent", not bad, str(bad))
    from openpyxl import load_workbook
    sheets = []
    for f in files:
        if f.endswith(".xlsx"):
            wb = load_workbook(os.path.join(TGT, f))
            sheets += [(f, ws.title, ws.sheet_state) for ws in wb.worksheets]
    check("G6 no notes, readme or method sheet in any workbook",
          not [s for s in sheets if re.search(r"note|readme|method|dictionary|how to", s[1], re.I)], str(sheets))
    check("G7 no hidden sheet", all(s[2] == "visible" for s in sheets), str([s for s in sheets if s[2] != "visible"]))
    # ---------------------------------------------------------------- documents read back (positive controls)
    lic = " ".join(A.pdf_text(os.path.join(TGT, "IEL-1186-03_conditions_consolidated_2026.pdf")))
    check("D1 licence PDF read back (positive control)", "From 1 January 2028 the mass of mercury" in lic and len(lic) > 500, "%d chars" % len(lic))
    check("D2 licence files the load and counts both operating modes",
          "shall not exceed %d kg" % G.LIMIT_KG in lic and "in compound operation and in direct operation" in lic)
    check("D3 licence files the hours the annual report states", "Hours of operation: the time during which a kiln is producing clinker" in lic)
    check("SF13 licence files hours as elapsed time, not a count of clock hours", "elapsed time from the start to the end of each period, summed" in lic)
    tests_txt = A.pdf_text(os.path.join(TGT, "stack_tests_Hg_2024-2026.pdf"))
    check("D4 test reports read back (positive control)", any("AEM-2026-A1-1-Hg" in w for w in tests_txt))
    check("D5 every test run with the raw mill in operation", tests_txt.count("in operation") == 18, "%d" % tests_txt.count("in operation"))
    stump_words = re.compile(r"mass balance|conservation|direct operation releases|mill[- ]off|mercury cycle|dust shuttl", re.I)
    check("D6 no shipped document narrates the decisive relation", not stump_words.search(lic + " ".join(tests_txt)))
    # ---------------------------------------------------------------- the call and the ladder
    hg = A.mercury(TGT)
    k1, k2 = hg["K1"]["release"], hg["K2"]["release"]
    works = k1 + k2
    check("C1 kiln 1 release recomputes to figures.json", rh(k1) == figs["hg_K1_kg"], "%.3f" % k1)
    check("C2 kiln 2 release recomputes to figures.json", rh(k2) == figs["hg_K2_kg"], "%.3f" % k2)
    check("C3 works total and margin recompute", rh(works) == figs["hg_works_kg"] and rh(works) - G.LIMIT_KG == figs["over_by_kg"])
    check("C4 SF8 works rounded once equals the sum of the rounded kilns", rh(works) == rh(k1) + rh(k2))
    for name, x in (("kiln 1", k1), ("kiln 2", k2), ("works", works)):
        check("B1 %s mercury mid-bin (0.3 kg or more from the edge)" % name, edge(x) >= 0.3, "%.3f" % edge(x))
    dflt = A.default_route(TGT)
    r0 = dflt["K1"]["r0"] + dflt["K2"]["r0"]
    r0b = dflt["K1"]["r1_per_clinker"] + dflt["K2"]["r1_per_clinker"]
    r0c = dflt["K1"]["r0_three_year"] + dflt["K2"]["r0_three_year"]
    check("R3a the easy route (2026 tested rate x kiln hours) files the works under the load", r0 < G.LIMIT_KG, "%.1f kg" % r0)
    check("R3a the per-tonne-of-clinker and three-year variants also file it under", max(r0b, r0c) < G.LIMIT_KG, "%.1f, %.1f" % (r0b, r0c))
    check("R3a the easy route's figure is far from the golden", abs(r0 - works) > 40, "%.1f vs %.1f" % (r0, works))
    nod = A.mercury(TGT, "no_dust")
    wet = A.mercury(TGT, "moisture_again")
    check("R3b the decisive step alone (the year's mercury in less what left) files the golden", rh(works) == figs["hg_works_kg"])
    check("R3b rung: the balance without kiln 1's dust lands elsewhere",
          rh(nod["K1"]["release"]) != rh(k1) and rh(nod["K1"]["release"] + nod["K2"]["release"]) != rh(works),
          "%.1f" % (nod["K1"]["release"] + nod["K2"]["release"]))
    check("R3b over-correction: moisture taken off dry tonnes lands elsewhere",
          rh(wet["K1"]["release"] + wet["K2"]["release"]) != rh(works), "%.1f" % (wet["K1"]["release"] + wet["K2"]["release"]))
    # ---------------------------------------------------------------- semantic forks
    am = A.mercury(TGT, "annual_mean")
    check("SF4 composites applied month by month or as annual means: same figures",
          rh(am["K1"]["release"]) == rh(k1) and rh(am["K2"]["release"]) == rh(k2) and rh(am["K1"]["release"] + am["K2"]["release"]) == rh(works))
    si = A.mercury(TGT, "silo")
    check("SF5 the meal silo's stock change counted or not: same figures",
          rh(si["K1"]["release"]) == rh(k1) and rh(si["K2"]["release"]) == rh(k2) and rh(si["K1"]["release"] + si["K2"]["release"]) == rh(works))
    ds = A.mercury(TGT, "dust_shipped")
    check("SF6 kiln 1's dust as bled to S7 (ledger) or as shipped (weighbridge): same figures",
          rh(ds["K1"]["release"]) == rh(k1) and rh(ds["K1"]["release"] + ds["K2"]["release"]) == rh(works))
    # SF7: the H2 clinker transfer row read as clinker made
    led = A.read_ledger(TGT)
    lab = A.read_lab(TGT)
    alt = {}
    for k in ("K1", "K2"):
        d = sum((led.get((k, "clinker_out", m), led[(k, "clinker", m)]) - led[(k, "clinker", m)]) * float(lab[("clinker_" + k, m)]["Hg mg/kg"]) / 1000.0 for m in A.MONTHS)
        alt[k] = hg[k]["release"] - d
    check("SF7 clinker made or clinker to cement mills: same mercury figures", rh(alt["K1"]) == rh(k1) and rh(alt["K2"]) == rh(k2))
    reg = load_workbook(os.path.join(TGT, "site_register_2026.xlsx"))["Emission points"]
    regmap = {r[0]: r[1] for r in reg.iter_rows(min_row=2, values_only=True)}
    check("SF3 emission points map to kilns in the register", regmap["A1-1"].startswith("Kiln 1") and regmap["A1-2"].startswith("Kiln 2"))
    check("SF2 the ledger's months are the calendar year the licence files (1.7)", "Irish local time" in lic and len({m for (_, _, m) in led}) == 12)
    labhdr = [c.value for c in load_workbook(os.path.join(TGT, "QC_lab_composites_2026.xlsx"))["Results"][1]]
    check("SF11 every composite states its basis (dry for raw materials, as received for fuels)", "Basis" in labhdr)
    check("SF1 the tested rate covers one mode only: the journal holds direct-operation hours for both kilns",
          sum(A.ask1(TGT)["K1"]["quarters"]) > 500 and sum(A.ask1(TGT)["K2"]["quarters"]) > 500)
    check("SF9 the call is the same under any reading of keeping under: %d against %d" % (rh(works), G.LIMIT_KG), rh(works) > G.LIMIT_KG and r0 < G.LIMIT_KG)
    check("SF10 the comparison is the 2026 release itself (prompt), no forward projection licensed", "if it releases what it released in 2026" in open(os.path.join(TASK, "prompt.txt")).read())
    # SF14: the fuels' mercury from the suppliers' certificates instead of the as-fired composites
    for v in ("certificates_monthly", "certificates_annual", "certificates_plain"):
        cv = A.mercury(TGT, v)
        check("SF14 fuel mercury from the certificates (%s): every kg figure unchanged" % v,
              rh(cv["K1"]["release"]) == rh(k1) and rh(cv["K2"]["release"]) == rh(k2) and
              rh(cv["K1"]["release"] + cv["K2"]["release"]) == rh(works), "%.2f %.2f %.2f" % (cv["K1"]["release"], cv["K2"]["release"], cv["K1"]["release"] + cv["K2"]["release"]))
    # SF13: the clock-hour readings the filed definition rules out
    ivd = A.direct_intervals(TGT)
    ivf = A.direct_intervals(TGT, want="feed")
    import datetime as _dt
    grid = {}
    for name, iv in (("direct", ivd), ("feed", ivf)):
        for k in ("K1", "K2"):
            hours = {"any": 0, "full": 0, "majority": 0}
            t = _dt.datetime(2026, 1, 1, tzinfo=_dt.timezone.utc)
            end = _dt.datetime(2027, 1, 1, tzinfo=_dt.timezone.utc)
            spans = iv[k]
            j = 0
            while t < end:
                t2 = t + _dt.timedelta(hours=1)
                ov = A.overlap_hours(spans, t, t2)
                hours["any"] += ov > 0
                hours["full"] += ov >= 0.9999
                hours["majority"] += ov >= 0.5
                t = t2
            grid[(name, k)] = hours
    a1g = A.ask1(TGT)
    ex_d = {k: sum(a1g[k]["quarters"]) for k in a1g}
    check("SF13 the clock-hour counts differ from the elapsed hours, so 1.8 is what fixes the reading",
          all(abs(grid[("direct", k)][r] - ex_d[k]) >= 1 for k in ex_d for r in ("any", "full")),
          "; ".join("%s %s %s" % (k, {r: grid[("direct", k)][r] for r in grid[("direct", k)]}, round(ex_d[k], 1)) for k in ex_d))
    # SF12: sand and slag quarterly composites read as covering only their first month
    q = dict(hg)
    miss = {}
    for k in ("K1", "K2"):
        lost = 0.0
        for mat in ("sand", "steel_slag"):
            if (k, mat, 1) not in led:
                continue
            for m in A.MONTHS:
                if m % 3 != 1:
                    lost += led[(k, mat, m)] * float(lab[(mat, m)]["Hg mg/kg"]) / 1000.0
        miss[k] = hg[k]["release"] - lost
    check("SF12 quarterly composites applied to every month or only to their first: same figures",
          rh(miss["K1"]) == rh(k1) and rh(miss["K2"]) == rh(k2) and rh(miss["K1"] + miss["K2"]) == rh(works))
    # ---------------------------------------------------------------- R1 and R2
    check("R1 the decisive computation reads ledger tonnages against laboratory composites (the field's raw material)",
          len([1 for (k, it, m) in led if it in ("limestone", "shale", "fly_ash")]) == 60)
    allcsv = ""
    for f in files:
        if f.endswith(".csv") or f.endswith(".txt"):
            allcsv += open(os.path.join(TGT, f), encoding="utf-8").read()[:200000]
    check("R1 no shipped column holds a mercury mass to air", not re.search(r"Hg (kg|mass).*(year|annual)", allcsv, re.I))
    # R2: each Layer 1 item mishandled leaves the call and the critical components (or moves only its ledgered ask)
    h1 = {it for (k, it, m) in led if m <= 6}
    h2 = {it for (k, it, m) in led if m >= 7} - {"clinker_out"}
    check("R2a ledger layout drift: every first-half item has its second-half counterpart", h1 == h2, str(h1 ^ h2))
    check("R2b clinker transfer row (H2) mishandled: call and components unchanged", rh(alt["K1"]) == rh(k1))
    check("R2c quarterly composites mishandled: call and components unchanged", rh(miss["K1"] + miss["K2"]) == rh(works))
    a1 = A.ask1(TGT)
    hi = A.ask1_historian(TGT)
    nd = A.ask1_naive_dst(TGT)
    check("R2d historian UTC and its May hole touch only ask 1 and ask 2 (the call never opens the historian)", True)
    check("R2e journal clock changes mishandled move only ask 1 (kiln 1 Q4 by one hour)",
          abs((a1["K1"]["quarters"][3] - nd["K1"][3]) - 1.0) < 0.05 and rh(nd["K1"][3]) != rh(a1["K1"]["quarters"][3]))
    a2 = A.ask2(TGT)
    a2n = A.ask2(TGT, convert=False)
    a2p = A.ask2(TGT, use_logger=False, prorate=True)
    a2a = A.ask2_append(TGT)
    check("R2f logger overlap appended moves only the NOx ask", all(rh(a2a[k]) != rh(a2[k]["total"]) for k in a2))
    wbp = A.mercury(TGT, "dust_shipped")
    check("R2g weighbridge voids and reprints (distractor) cannot move the call", rh(wbp["K1"]["release"] + wbp["K2"]["release"]) == rh(works))
    # R3c: no plant
    hist_rows = list(csv.reader(open(os.path.join(TGT, "PI_historian_K1K2_2026_30min.csv"))))[1:]
    seq = {}
    rep = 0
    for k in ("K1", "K2"):
        vals = [r[6] for r in hist_rows if r[1] == k]
        blocks = {}
        for i in range(0, len(vals) - 24, 24):
            b = tuple(vals[i:i + 24])
            if b in blocks and any(v != "0.0" for v in b):
                rep += 1
            blocks[b] = i
    check("R3c no copied or repeated block in the historian", rep == 0, "%d" % rep)
    check("R3c no duplicate historian rows", len(hist_rows) == len({tuple(r) for r in hist_rows}))
    check("R3c no memo, draft or stakeholder figure ships", not [f for f in files if re.search(r"memo|draft|briefing|email", f, re.I)])
    # ---------------------------------------------------------------- asks
    for k in ("K1", "K2"):
        for qq in range(4):
            x = a1[k]["quarters"][qq]
            check("A1 %s Q%d recomputes and sits 0.1 h or more from its edge" % (k, qq + 1),
                  rh(x) == figs["direct_h_%s_Q%d" % (k, qq + 1)] and edge(x) >= 0.1, "%.2f edge %.2f" % (x, edge(x)))
    check("A1 device: the historian's half-hour status misses every quarter by two hours or more",
          all(abs(hi[k][qq] - a1[k]["quarters"][qq]) >= 1.5 for k in hi for qq in range(4)))
    for k in ("K1", "K2"):
        check("A3 %s NOx recomputes and sits 0.3 t from its edge" % k, rh(a2[k]["total"]) == figs["nox_t_%s" % k] and edge(a2[k]["total"]) >= 0.3, "%.2f" % a2[k]["total"])
        check("A3 %s device: the historian's May hole is covered only by the logger" % k, a2[k]["missing"] == 432 and a2[k]["logger_cover"] == 432)
        check("A3 %s rungs: unconverted, pro-rated and appended all miss" % k,
              len({rh(a2[k]["total"]), rh(a2n[k]["total"]), rh(a2p[k]["total"]), rh(a2a[k])}) == 4)
    fe = A.ask_feed(TGT)
    fen = A.ask_feed(TGT, burner_trip_stops_feed=False)
    a1n = A.ask1(TGT, burner_trip_stops_feed=False)
    for k in ("K1", "K2"):
        for qq in range(4):
            x = fe[k][qq]
            check("A2 %s Q%d hours on feed recompute and sit 0.1 h or more from the edge" % (k, qq + 1),
                  "{:,}".format(int(rh(x))) == figs["feed_h_%s_Q%d" % (k, qq + 1)] and edge(x) >= 0.1, "%.2f edge %.2f" % (x, edge(x)))
    check("A2 device: burner trips read as no stop put every quarter's hours on feed off by an hour or more",
          all(abs(fen[k][qq] - fe[k][qq]) >= 1.0 for k in fe for qq in range(4)))
    check("A1 device: burner trips read as no stop put every quarter's direct-operation hours off by an hour or more",
          all(abs(a1n[k]["quarters"][qq] - a1[k]["quarters"][qq]) >= 1.0 for k in a1 for qq in range(4)))
    jl0 = open(os.path.join(TGT, "DCS_event_journal_2026.txt"), encoding="utf-8").read()
    trips = len(re.findall(r"MAIN BURNER\s+TRIP", jl0))
    offs = len(re.findall(r"KILN \d FEED\s+OFF", jl0))
    check("A1 and A2 organ: unplanned stops are logged as burner trips, the planned shutdowns as feed off", trips >= 10 and offs == 2, "%d trips, %d feed off" % (trips, offs))
    a2c = A.ask2(TGT, logger_converted_again=True)
    check("A3 device: the logger's concentrations read as if at 10 per cent oxygen miss both kilns",
          all(rh(a2c[k]["total"]) != rh(a2[k]["total"]) for k in a2))
    # ---------------------------------------------------------------- separation and distractors
    tmp = tempfile.mkdtemp()
    try:
        shutil.copytree(TGT, os.path.join(tmp, "t"))
        for d in dis:
            os.remove(os.path.join(tmp, "t", os.path.basename(d)))
        hgd = A.mercury(os.path.join(tmp, "t"))
        check("S1 golden unchanged with every distractor deleted",
              rh(hgd["K1"]["release"]) == rh(k1) and rh(hgd["K2"]["release"]) == rh(k2))
        check("S2 asks unchanged with every distractor deleted",
              A.ask1(os.path.join(tmp, "t")) == a1 and A.ask_feed(os.path.join(tmp, "t")) == fe)
        for f in ("PI_historian_K1K2_2026_30min.csv", "DCS_event_journal_2026.txt", "CEMS_logger_A1-1_A1-2_May2026.csv",
                  "stack_tests_Hg_2024-2026.pdf"):
            os.remove(os.path.join(tmp, "t", f))
        hge = A.mercury(os.path.join(tmp, "t"))
        check("S3 the call never reads a device file: golden unchanged with the historian, journal, logger and tests deleted",
              rh(hge["K1"]["release"]) == rh(k1) and rh(hge["K2"]["release"]) == rh(k2))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    # ---------------------------------------------------------------- realism sweep
    rep_in_item = 0
    for (k, it) in {(k, it) for (k, it, m) in led}:
        vals = [v for (kk, ii, m), v in led.items() if kk == k and ii == it]
        rep_in_item += len(vals) - len(set(vals))
    same_across = sum(1 for (k, it, m), v in led.items() if k == "K1" and led.get(("K2", it, m)) == v)
    check("X1 at most one chance repeat of a monthly tonnage, none matching across kilns", rep_in_item <= 1 and same_across == 0,
          "%d repeat(s)" % rep_in_item)
    tick = [int(r["Ticket"]) for r in csv.DictReader(open(os.path.join(TGT, "weighbridge_byproducts_2026.csv")))]
    steps = {b - a for a, b in zip(sorted(set(tick)), sorted(set(tick))[1:])}
    check("X2 ticket numbers are not an arithmetic sequence", len(steps) > 5, "%d distinct steps" % len(steps))
    totals = [round(sum(led[(k, it, m)] for m in A.MONTHS)) for (k, it) in {(k, it) for (k, it, m) in led if it not in ("silo", "clinker_out")}]
    check("X3 no round annual totals in the ledger", not [t for t in totals if t % 1000 == 0], str([t for t in totals if t % 1000 == 0]))
    memo = " ".join(A.pdf_text(os.path.join(GLD, "kiln_mercury_memo_2026.pdf")))
    check("X4 golden memo read back (positive control)", "Kilcarrow Works - memo" in memo)
    card = json.load(open(os.path.join(TASK, "..", ".claude", "skills", "fingerprint", "cards", "task452.json")))
    people = set(card["world"]["people"])
    named = set(re.findall(r"From: ([A-Z][a-z]+ [A-Z][a-z]+)", memo))
    check("X5 every persona in the goldens is drawn (card world.people)", named and named <= people, str(named))
    check("X6 no em or en dash in the goldens, prompt or write-up",
          not re.search("[–—]", memo + open(os.path.join(TASK, "prompt.txt")).read() + open(os.path.join(TASK, "submission.md")).read()))
    jl = open(os.path.join(TGT, "DCS_event_journal_2026.txt"), encoding="utf-8").read()
    check("X7 the journal states every status at the start of the log", jl.count("(state at start of log)") == 4)
    check("X8 no document dated after the as-of date (2027-01-11)", "4 January 2027" in jl and "2027-01-1" not in jl)
    # ---------------------------------------------------------------- report
    fails = [r for r in RESULTS if not r[1]]
    for name, ok, detail in RESULTS:
        print("%s  %s  %s" % ("PASS" if ok else "FAIL", name, detail))
    print("%d checks, %d failed" % (len(RESULTS), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
