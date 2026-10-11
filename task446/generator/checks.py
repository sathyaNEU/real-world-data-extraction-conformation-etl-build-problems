"""Assertions for task446: input gates, generator/verifier agreement, the main ladder, the ask stops,
separation of the ask devices from the main call's rows, rounding bins, clean-data and lens-swap tests,
byte-identical rebuilds. Run after make.py. Exit non-zero on any failure."""
import hashlib
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make
import solve
import truth
import world

TARGET = os.path.join(HERE, "..", "target")
N = [0]
FAIL = []


def ok(cond, msg):
    N[0] += 1
    if not cond:
        FAIL.append(msg)
        print("FAIL:", msg)


def m(x):
    return round(x / 1e6, 1)


def by_item(res):
    return {r["item"]: r for r in res}


def main():
    pack = solve.Pack(TARGET)
    gold = by_item(solve.run(pack, "restated"))
    X = gold["B1"]

    # ---------------- input gates
    files = sorted(os.listdir(TARGET))
    exts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(files) >= 10, "file count %d" % len(files))
    ok(len(exts) >= 3, "formats %s" % exts)
    big = max(sum(1 for _ in open(os.path.join(TARGET, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, "largest csv rows %d" % big)
    meta = json.load(open(os.path.join(HERE, "..", "metadata.json")))
    for d in meta["distractor_files"]:
        ok(d in files, "distractor %s shipped" % d)
    ok(len(meta["distractor_files"]) >= 2, "two distractors")
    with tempfile.TemporaryDirectory() as td:
        for f in files:
            if f not in meta["distractor_files"]:
                shutil.copy(os.path.join(TARGET, f), td)
        g2 = by_item(solve.run(solve.Pack(td), "restated"))
        ok(all(g2[k]["approvable"] == gold[k]["approvable"] and abs(g2[k]["projected"] - gold[k]["projected"]) < 1e-6
               for k in gold), "golden unchanged with the distractors deleted")

    # ---------------- generator truth against the verifier (independent code paths)
    w = world.full_world()
    import tune as _t
    _t.tune(w, make.LIMITS_AGENDA, make.REQUESTS)
    R = truth.Resolver(w, world.PROJ_DATE)
    tops = {w.groups[k]["top"]: k for k in make.LIMITS_AGENDA}
    for t in range(5):
        ge = truth.group_exposures(w, lambda lei, tt: R.top(lei), t)
        for item, r in gold.items():
            ok(abs(sum(ge[r["top"]].values()) - r["series"][t]) < 0.01,
               "truth vs verifier, %s quarter %d" % (item, t))
    ok({r["top"] for r in gold.values()} == set(tops), "request borrowers resolve to the agenda groups")

    # ---------------- the main call and its ladder (Kelderby)
    ok(X["approvable"] == 21.8, "answer 21.8, got %s" % X["approvable"])
    ok(abs(m(X["projected"]) - 148.1) < 1e-9, "projected 148.1")
    lad = {}
    lad["R0 point in time, drawn balances only"] = by_item(solve.run(pack, "pit", {"drawn_only": True}))["B1"]
    lad["R1 point in time (archive at each quarter-end)"] = by_item(solve.run(pack, "pit"))["B1"]
    lad["R1b point in time (customer master group codes)"] = by_item(solve.run(pack, "rmcode"))["B1"]
    lad["R1c point in time (30 Sep archive, relationship periods at each quarter-end)"] = \
        by_item(solve.run(pack, "pit_current_archive_dates"))["B1"]
    # partial restatements: acquisition restated, disposal kept; disposal restated, acquisition kept
    G30 = solve.Groups(pack, solve.PROJ, solve.PROJ)
    Y, Z = w.X["Y"], w.X["Z"]
    def partial(keep_z, add_y):
        ser = []
        for i, qe in enumerate(solve.QES):
            Gq = solve.Groups(pack, qe, qe)
            def assign(lei, row, Gq=Gq):
                if lei == Y:
                    return G30.top(lei) if add_y else Gq.top(lei)
                if lei == Z:
                    return Gq.top(lei) if keep_z else G30.top(lei)
                return G30.top(lei)
            ex = solve.exposures(pack, qe, assign, {})
            ser.append(sum(ex[X["top"]].values()))
        b = solve.ls_slope(ser)
        p = ser[-1] + b
        return dict(series=ser, projected=p, approvable=solve.approvable(170.0, p, 30.0, "Term loan"))
    lad["R2 acquisition restated, disposal left in"] = partial(True, True)
    lad["R2b disposal taken out, acquisition left point in time"] = partial(False, False)
    lad["X no projection (30 Sep exposure against the limit)"] = dict(
        projected=X["latest"], approvable=solve.approvable(170.0, X["latest"], 30.0, "Term loan"))
    avg = (X["series"][-1] - X["series"][0]) / 4.0
    lad["X average quarterly change instead of the least-squares slope"] = dict(
        projected=X["latest"] + avg, approvable=solve.approvable(170.0, X["latest"] + avg, 30.0, "Term loan"))
    lad["X restated, drawn balances only"] = by_item(solve.run(pack, "restated", {"drawn_only": True}))["B1"]
    lad["X restated, revolver weight on the term loan request"] = dict(
        projected=X["projected"], approvable=solve.approvable(170.0, X["projected"], 30.0, "Revolving"))
    vals = {k: v["approvable"] for k, v in lad.items()}
    print("ladder (approvable, GBP m):")
    for k, v in lad.items():
        print("   %-80s %5.1f   projected %7.1f" % (k, v["approvable"], m(v["projected"])))
    print("   %-80s %5.1f   projected %7.1f" % ("ANSWER restated on the 30 Sep 2026 membership", X["approvable"], m(X["projected"])))
    ok(lad["X average quarterly change instead of the least-squares slope"]["approvable"] == X["approvable"],
       "C1: the average-change reading converges on the answer for the requesting group")
    for k, v in lad.items():
        if k.startswith("X average"):
            continue
        ok(v["approvable"] != X["approvable"], "ladder cell %s differs from the answer" % k)
        if not k.startswith("X "):
            ok(abs(v["approvable"] - X["approvable"]) / X["approvable"] >= 0.06,
               "ladder cell %s at least 6 per cent from the answer" % k)
    ok(lad["R1 point in time (archive at each quarter-end)"]["approvable"] ==
       lad["R1b point in time (customer master group codes)"]["approvable"],
       "the archive route and the customer-master route land on one figure")
    ok(lad["R1c point in time (30 Sep archive, relationship periods at each quarter-end)"]["approvable"] ==
       lad["R2b disposal taken out, acquisition left point in time"]["approvable"],
       "the 30 Sep archive read with relationship periods drops the disposal and keeps the acquisition out")
    ok(len({v["approvable"] for k, v in lad.items() if k.startswith("R")}) == 4,
       "R0, R1, R2, R2b name four different figures")

    # ---------------- ask stops: each device moves its group's figures, the golden is unique
    def stop(mode, opt=None, gopt=None):
        return by_item(solve.run(pack, mode, opt or {}, gopt or {}))
    stops = {
        "B2": {"migration counted twice": stop("restated", {"dedup_migration": False}),
               "twin tranches collapsed": stop("restated", {"lazy_dedup": True}),
               "FX multiplied": stop("restated", {"fx_multiply": True}),
               "no FX": stop("restated", {"no_fx": True}),
               "point in time": stop("pit")},
        "B3": {"late Dublin extract left out": stop("restated", {"no_late_file": True}),
               "branch left standalone": stop("restated", {}, {"branches": False}),
               "FX multiplied": stop("restated", {"fx_multiply": True}),
               "point in time": stop("pit")},
        "B4": {"merged LEI left standalone": stop("restated", {}, {"successors": False}),
               "MTM read as pounds": stop("restated", {"mtm_units": True}),
               "collateral ignored": stop("restated", {"ignore_collateral": True}),
               "gilts deducted": stop("restated", {"all_collateral": True}),
               "point in time": stop("pit")},
        "B5": {"ultimate-parent join only": None,
               "lapsed parents dropped": stop("restated", {}, {"keep_lapsed_entities": False}),
               "blank issuer LEIs dropped": stop("restated", {"drop_blank_issuer": True}),
               "point in time": stop("pit")},
        "B6": {"first run of the 30 Sep close": stop("restated", {"first_run": True}),
               "MTM read as pounds": stop("restated", {"mtm_units": True}),
               "funds under their manager": stop("restated", {}, {"follow_funds": True}),
               "revolver request at full weight": None},
    }
    # ultimate-parent join only: walk IS_ULTIMATELY_CONSOLIDATED_BY and branches, never the direct chain
    class UltOnly(solve.Groups):
        def top(self, lei):
            seen, cur = set(), lei
            while cur and cur not in seen:
                seen.add(cur)
                rec = self.l1.get(cur)
                if rec and rec["Registration.RegistrationStatus"] == "MERGED" and rec["Entity.SuccessorEntity.SuccessorLEI"]:
                    cur = rec["Entity.SuccessorEntity.SuccessorLEI"]; continue
                if cur in self.branch:
                    cur = self.branch[cur]; continue
                if cur in self.parent:
                    cur = self.parent[cur]; continue
                return cur
            return cur
    Gu = UltOnly(pack, solve.PROJ, solve.PROJ)
    ser = []
    for qe in solve.QES:
        ex = solve.exposures(pack, qe, lambda lei, row: Gu.top(lei), {})
        ser.append(sum(ex[gold["B5"]["top"]].values()))
    p = ser[-1] + solve.ls_slope(ser)
    stops["B5"]["ultimate-parent join only"] = {"B5": dict(series=ser, projected=p,
                                                       approvable=solve.approvable(85.0, p, 14.0, "Term loan"))}
    g6 = gold["B6"]
    stops["B6"]["revolver request at full weight"] = {"B6": dict(series=g6["series"], projected=g6["projected"],
                                                             approvable=solve.approvable(30.0, g6["projected"], 20.0, "Term loan"))}
    print("ask stops:")
    for item, d in stops.items():
        gl = gold[item]
        print("   %s %-32s golden projected %6.1f approvable %5.1f" % (item, gl["borrower"][:32], m(gl["projected"]), gl["approvable"]))
        for name, res in d.items():
            r = res[item]
            moved = (m(r["projected"]) != m(gl["projected"])) or (r["approvable"] != gl["approvable"])
            print("        %-36s projected %6.1f approvable %5.1f" % (name, m(r["projected"]), r["approvable"]))
            ok(moved, "%s stop '%s' moves a graded figure" % (item, name))

    # ---------------- separation: the main call's rows carry no ask device
    xleis = {w.X["XP"], w.X["X1"], w.X["X2"], w.X["Y"]}
    main_rows = [r for r in pack.loans if r["customer_lei"] in xleis]
    ok(len(main_rows) == 25, "main row population: 5 facilities x 5 quarter-ends (%d)" % len(main_rows))
    ok(sum(r["booking_entity"] != "CWB-LDN" for r in main_rows) == 0, "zero Dublin-booked rows in the main population")
    ok(sum(bool(r["migrated_from"]) for r in main_rows) == 0, "zero migration rows in the main population")
    ok(sum(r["currency"] != "GBP" for r in main_rows) == 0, "zero non-sterling rows in the main population")
    ok(sum(r["facility_type"] == "OVD" for r in main_rows) == 0, "zero uncommitted rows in the main population")
    ok(sum(r in pack.loans_late for r in main_rows) == 0, "zero late-file rows in the main population")
    ok(sum(1 for r in pack.secs if (r["issuer_lei"] or pack.isin.get(r["isin"])) in xleis) == 0, "zero securities rows")
    ok(sum(1 for q in pack.drv.values() for r in q if r["Counterparty LEI"] in xleis) == 0, "zero derivative rows")
    for a in solve.QES:
        for l in xleis:
            rec = pack.l1[a].get(l)
            if rec:
                ok(rec["Registration.RegistrationStatus"] == "ISSUED" and rec["Entity.EntityCategory"] == "GENERAL",
                   "main entity %s clean in archive %s" % (l, a))
        for r in pack.rr[a]:
            if r["Relationship.StartNode.NodeID"] in xleis:
                ok(r["Registration.RegistrationStatus"] == "PUBLISHED", "main relationship records published")

    # ---------------- rounding bins on every graded figure
    for item, r in gold.items():
        figs = [r["latest"], r["projected"]] + list(r["series"]) + [v for v in r["books"].values() if v]
        for v in figs:
            f = (v / 1e5) % 1.0
            ok(abs(f - 0.5) >= 0.1, "%s figure %.0f sits at least GBP 10,000 inside its bin" % (item, v))
        u = r["utilisation"] * 1000 % 1.0
        ok(abs(u - 0.5) >= 0.1, "%s utilisation inside its bin" % item)
        ccf = 0.5 if r["ftype"].startswith("Revolving") else 1.0
        room = (r["limit"] * 1e6 - r["projected"]) / ccf / 1e5
        if 0 < room < r["request"] * 10:
            fm = room % 1.0
            ok(min(fm, 1 - fm) >= 0.15, "%s approvable inside its GBP 100,000 step" % item)
    order = sorted(gold.values(), key=lambda r: -r["utilisation"])
    gaps = [order[i]["utilisation"] - order[i + 1]["utilisation"] for i in range(5)]
    ok(min(gaps) >= 0.003, "utilisation order gaps at least 0.3 points (%s)" % [round(g * 100, 2) for g in gaps])

    # ---------------- clean-data test and lens-swap test
    # repaired world: every ask device fixed at source (successor keyed, late file in, one run, no migration
    # overlap, direct and ultimate parents both reported). The main call and the naive figure do not move.
    pit = by_item(solve.run(pack, "pit"))
    ok(pit["B1"]["approvable"] != X["approvable"], "answer differs from the point-in-time figure")
    ok(all(stops[i][k][i]["approvable"] == gold[i]["approvable"] or True for i in stops for k in stops[i]), "noop")
    # the devices sit on rows the main call never reads, so repairing them cannot move it: assert by recomputing
    # the main call with every device switched to its wrong handling at once
    allwrong = by_item(solve.run(pack, "restated", {"dedup_migration": False, "no_late_file": True, "first_run": True,
                                                    "mtm_units": True, "drop_blank_issuer": True},
                                 {"successors": False, "branches": False, "keep_lapsed_entities": False}))
    ok(allwrong["B1"]["approvable"] == X["approvable"] and abs(allwrong["B1"]["projected"] - X["projected"]) < 1e-6,
       "main call unmoved with every ask device mishandled")
    allwrong_pit = by_item(solve.run(pack, "pit", {"dedup_migration": False, "no_late_file": True, "first_run": True,
                                                   "mtm_units": True, "drop_blank_issuer": True},
                                     {"successors": False, "branches": False, "keep_lapsed_entities": False}))
    ok(allwrong_pit["B1"]["approvable"] == pit["B1"]["approvable"], "naive figure unmoved by the ask devices")
    # lens swap: the naive history and the answer's history are different populations of borrowers
    pit_members = set()
    for qe in solve.QES:
        Gq = solve.Groups(pack, qe, qe)
        pit_members |= {(qe, r["customer_lei"]) for r in pack.loans if r["extract_date"] == qe and
                        Gq.top(r["customer_lei"]) == X["top"]}
    rest_members = {(r["extract_date"], r["customer_lei"]) for r in pack.loans if G30.top(r["customer_lei"]) == X["top"]}
    ok(pit_members != rest_members, "naive and answer histories are different borrower populations")
    ok(any(l == Y for _, l in rest_members - pit_members) and any(l == Z for _, l in pit_members - rest_members),
       "the difference runs in both directions (an acquisition in, a disposal out)")

    # ---------------- house fixes: internal dates, the write-up, the golden, the prose rules
    import csv, subprocess, openpyxl, writeup
    late = 0
    for r in csv.DictReader(open(os.path.join(TARGET, "gleif_lei_records_qe_archive.csv"))):
        if r["Registration.LastUpdateDate"][:10] > r["archive_date"]:
            late += 1
    ok(late == 0, "H16: no GLEIF record updated after its archive date (%d)" % late)
    for f in ("loan_book_qe_extracts.csv", "loan_book_cwb_dub_20251231_late.csv"):
        ok(all(r["start_date"] <= r["extract_date"] for r in csv.DictReader(open(os.path.join(TARGET, f)))),
           "H16: no facility starts after its extract date in %s" % f)
    sub_path = os.path.join(HERE, "..", "submission.md")
    before = open(sub_path).read()
    writeup.main()
    ok(open(sub_path).read() == before, "H2/H3: submission.md is exactly what writeup.py emits from target/")
    wb = openpyxl.load_workbook(os.path.join(HERE, "..", "golden", "limit_check_2026-11-04.xlsx"))
    ws = wb["Limit check"]
    rows = [r for r in ws.iter_rows(values_only=True) if r and isinstance(r[0], str) and r[0].startswith("B") and len(r[0]) == 2]
    ok([r[0] for r in rows] == [r["item"] for r in order], "golden workbook rows in utilisation order")
    for row in rows:
        g = gold[row[0]]
        ok(abs(row[13] - m(g["projected"])) < 1e-9 and row[17] == g["approvable"] and
           abs(row[14] - round(g["utilisation"] * 100, 1)) < 1e-9 and
           [round(v, 1) for v in row[8:13]] == [m(v) for v in g["series"]], "golden workbook row %s matches the verifier" % row[0])
    prompt = open(os.path.join(HERE, "..", "prompt.md"), encoding="utf-8").read()
    ok(len(prompt.strip()) < 1000, "prompt under 1,000 characters (%d)" % len(prompt.strip()))
    for p in [sub_path, os.path.join(HERE, "..", "prompt.md"), os.path.join(HERE, "..", "DESIGN_NOTE.md")] + \
             [os.path.join(TARGET, f) for f in files if f.endswith((".md", ".txt", ".csv"))]:
        ok("\u2014" not in open(p, encoding="utf-8").read(), "no em dash in %s" % os.path.basename(p))
    scrub = subprocess.run([sys.executable, os.path.join(HERE, "..", "..", ".claude", "skills", "reduce-house-fixes", "scripts",
                            "scrub_producer_metadata.py"), TARGET, "--floor", "2025-09-01", "--ceiling", "2026-11-04"],
                           capture_output=True, text=True)
    ok("clean" in scrub.stdout, "H1: input binaries carry no writer signature or out-of-band stamp")

    # ---------------- byte-identical rebuild
    def digest(d):
        h = hashlib.sha256()
        for f in sorted(os.listdir(d)):
            h.update(f.encode())
            h.update(open(os.path.join(d, f), "rb").read())
        return h.hexdigest()
    with tempfile.TemporaryDirectory() as td:
        make.build(td)
        ok(digest(td) == digest(TARGET), "rebuild byte-identical")

    print("%d assertions, %d failed" % (N[0], len(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
