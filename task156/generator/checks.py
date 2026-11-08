"""task156's assertions: the three rules on the clean truth (R1 to R3c), Gate F counted on the clean truth, the
standing family, the margins over redraws, every semantic fork (SF1 to SF15), the asks and their devices, the
separation line, the input gates, the house fixes and the realism sweep. python3 task156/generator/checks.py [--fast]"""
import copy
import csv
import json
import os
import re
import subprocess
import sys
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A          # noqa: E402
import ceiling as CE      # noqa: E402
import estim as ES        # noqa: E402
import pack as PK         # noqa: E402
import parse as PA        # noqa: E402
import world as W         # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
FAILS = []
N = [0]


def ok(cond, msg):
    N[0] += 1
    print(("PASS  " if cond else "FAIL  ") + msg)
    if not cond:
        FAILS.append(msg)


def names(H, s):
    hub = {h["code"]: h["name"] for h in H["hubs"]}
    return sorted(hub[c] for c in s)


def margin(av):
    return min(abs(min(v) - 0.99) for v in av.values()) * 100


def main(fast=False):
    H = W.history()
    T27 = W.truth_2027(H, reps=300)
    truth = ES.side_set(T27)
    charges, salt = __import__("build").charges_clear(H)
    Rt = ES.from_truth(H, charges)
    Ct = ES.classify(Rt)
    Et = ES.estimates(Rt, Ct)
    Gt = ES.golden(Rt, Ct, Et)
    R = PA.read_pack(TARGET)
    G = ES.golden(R)
    C, E = G["C"], G["E"]
    golden = G["set"]
    naive_t = ES.side_set(ES.route_rates(Rt, Ct, Et))
    naive = ES.side_set(ES.route_rates(R, C, E))

    print("== the call")
    ok(len(golden) == 12 and golden == truth, "the golden from the pack is the truth's set (%d hubs: %s)" % (len(golden), ", ".join(names(H, golden))))
    ok(Gt["set"] == golden, "the golden from the clean truth equals the golden from the pack (every mess item neutral on the call)")
    ok(margin(T27) >= 0.4, "every hub's true 2027 side is at least 0.4 points from 99 (closest %.2f)" % margin(T27))
    ok(margin(G["av"]) >= 0.3, "SF4: no golden forecast within 0.3 points of 99, so strictly below and at or below agree (closest %.2f)" % margin(G["av"]))

    print("== R1 to R3c")
    ok(G["ev"].sum() >= 60 and int(np.nonzero(G["ev"])[0].min()) >= 75,
       "R1: the decisive computation reads the status history's own rows: %d hangs on record, none before day %d since power-up"
       % (G["ev"].sum(), int(np.nonzero(G["ev"])[0].min())))
    ok(G["expo"][60:75].sum() > 1000, "R1: the record carries %.0f unit-days at 60 to 75 days since power-up with no hang"
       % G["expo"][60:75].sum())
    heads = []
    for f in PK.FILES:
        p = os.path.join(TARGET, f)
        if f.endswith(".csv"):
            heads += open(p, encoding="utf-8").readline().strip().split(",")
        elif f.endswith(".xlsx"):
            import openpyxl
            wb = openpyxl.load_workbook(p, read_only=True)
            for ws in wb.worksheets:
                heads += [str(c) for c in next(ws.iter_rows(values_only=True))]
    bad = [h for h in heads if re.search(r"uptime|power.?up|pillar|restart|boot|reset|since", h, re.I)]
    ok(not bad, "R1: no shipped column holds the deciding quantity (no uptime, power-up, pillar or restart column): %s" % (bad or "none"))
    ok(naive_t == naive and len(naive) == 5 and naive != golden,
       "R3a: the default path on the clean truth files the named wrong answer, 5 hubs (%s)" % ", ".join(names(H, naive_t)))
    st = ES.standing(Rt, Ct, Et, reps=120)
    ok(all(ES.side_set(v) == golden for v in st.values()),
       "R3b: the default path with only the decisive step changed files the golden, in all %d standing constructions" % len(st))
    wo = ES.side_set(ES.rung_workorder_clock(Rt, Ct, Et))
    nr = ES.side_set(ES.rung_no_resets(Rt, Ct, Et))
    ok(wo != golden and nr != golden, "R3b: each lower rung's single correction stays wrong: the work-order clock files %d hubs, the "
       "status clock without the 2027 visits and interruptions files %d" % (len(wo), len(nr)))
    seqs = {}
    for k, rows in R["rows"].items():
        sig = tuple((rows[i + 1][0] - rows[i][0], rows[i][1]) for i in range(min(40, len(rows) - 1)))
        seqs.setdefault(sig, []).append(k)
    ok(all(len(v) == 1 for v in seqs.values()), "R3c: no unit's status record is a copy of another's (no copied or backfilled block)")

    print("== Gate F on the clean truth")
    fam = {"each unit's rates carried": ES.route_rates(Rt, Ct, Et), "rates shrunk to hub and fleet": ES.route_hier(Rt, Ct, Et),
           "the full-covariate Poisson model": ES.route_glm(Rt, Ct, Et)[0], "a regression tree": ES.route_tree(Rt, Ct, Et)[0],
           "the daily model on the RC50's recent jobs": ES.route_daily(Rt, Ct, Et)[0],
           "January to October 2026 carried": ES.route_last(Rt, Ct, Et), "each unit's monthly series smoothed": ES.route_smooth(Rt, Ct, Et)}
    reach = 0
    for k, v in fam.items():
        s = ES.side_set(v)
        reach += s == golden
        print("      %-42s %2d hubs, %d of the golden's 12, %d outside it" % (k, len(s), len(set(s) & set(golden)), len(set(s) - set(golden))))
    ok(reach == 0, "Gate F: cheap routes reaching the golden on the clean truth, %d of %d" % (reach, len(fam)))
    glm_set = ES.side_set(fam["the full-covariate Poisson model"])
    ok(len(set(glm_set) & set(golden)) <= 5, "Gate F: the full-covariate model with the RC50's work orders at 2027 values keeps the "
       "programme hubs off the list (%d hubs)" % len(glm_set))
    bt = ES.backtests(Rt, Ct, Et)
    ok(bt["2025"][0] < 0.4 and bt["2026"][0] < 0.4 and bt["loo"][0] < 0.2,
       "Back-test: the rate route validates on its own record: 2025 from 2023-24 mean error %.2f points (%d of %d units on their "
       "side), 2026 from 2023-25 %.2f (%d of %d), each unit left out %.2f (%d of %d)" % (bt["2025"] + bt["2026"] + bt["loo"]))
    ok(all(ES.side_set(v) == golden for v in st.values()), "Gate F: standing family after the step, %d of %d on the golden"
       % (sum(ES.side_set(v) == golden for v in st.values()), len(st)))
    if not fast:
        hits, mins = 0, []
        for s in range(1, 21):
            Hs = W.history(seed=1000 + s)
            Ts = ES.side_set(W.truth_2027(Hs, reps=120, seed=1000 + s))
            Rs = ES.from_truth(Hs)
            Gs = ES.golden(Rs, reps=100, seed=1000 + s)
            hits += (Gs["set"] == Ts == truth)
            mins.append(margin(Gs["av"]))
        ok(hits == 20, "Margins: over 20 redraws of the world the restart-clock golden files the same 12 hubs as the truth %d of 20 "
           "(closest forecast %.2f points from 99, median %.2f)" % (hits, min(mins), float(np.median(mins))))

    print("== semantic forks")
    def variant(**kw):
        R2 = copy.deepcopy(R)
        if "rows" in kw:
            R2["rows"] = kw["rows"](R2)
        if "prog" in kw:
            R2["programme"] = {}
        if "excl" in kw:
            for c in R2["visits"]:
                R2["visits"][c] = []
                R2["dso"][c] = R2["dso"][c] if kw["excl"] == "dso" else []
        C2 = ES.classify(R2)
        E2 = ES.estimates(R2, C2)
        if "att" in kw:
            m = float(np.mean(list(E2["att"].values())))
            E2["att"] = {c: m for c in E2["att"]}
        if "dso12" in kw:
            for c in E2["dso_rate"]:
                last = [x for x in R2["dso"][c] if x[0] >= W.HIST_END - 365 * W.DAY]
                E2["dso_rate"][c] = len(last)
        return ES.golden(R2, C2, E2, reps=120)
    ok(len(R["hubs"]) == 30 and set(golden) <= set(h["code"] for h in R["hubs"]), "SF1: every listed hub is a register hub, one per code")
    av = G["av"]
    no_new = {c: [x for x, (cc, k, new) in zip(v, [u for u in ES.units27(R) if u[0] == c]) if not new] for c, v in av.items()}
    ok(ES.side_set(no_new) == golden, "SF2: the existing units alone give the same set (the programme's new units included or not)")
    ok(ES.side_set({c: [float(np.mean(v))] for c, v in av.items()}) == golden, "SF6: a hub's mean HX150 gives the same set as its lowest")
    ok(W.from_local(2027, 1, 1) == W.Y27_START and W.from_local(2028, 1, 1) == W.Y27_END, "SF7: the contract year's bounds are the same "
       "instants in Irish time and UTC (both in winter time)")
    v8 = ES.side_set(variant(prog=True)["av"])
    ok(set(v8) == set(golden) - set(R["programme"]) , "SF8: on the register as at the extract (no programme) the set is the golden less "
       "the programme hubs (%d), so the filed asset base decides only where the programme acts" % len(v8))
    ok(ES.side_set(variant(rows=lambda R2: {k: [(t - 900 if s == "Offline" else t, s) for t, s in r] for k, r in R2["rows"].items()})["av"]) == golden,
       "SF9: Offline back-dated fifteen minutes to the drop gives the same set")
    raw = {}
    with open(os.path.join(TARGET, PK.F_STATUS), encoding="utf-8") as f:
        units, alias, serial, hubs = PA.read_register(TARGET)
        for r in csv.DictReader(f):
            raw.setdefault(alias[r["charge_point_id"]], []).append((PA.from_utc_iso(r["timestamp_utc"]), r["status"]))
    ok(ES.side_set(variant(rows=lambda R2: {k: sorted(raw.get(k, [])) for k in R2["rows"]})["av"]) == golden,
       "SF10: every re-sent row read as a change gives the same set")
    tail = W.EXCL_TAIL
    W.EXCL_TAIL = 0
    s11 = ES.side_set(ES.golden(R, reps=120)["av"])
    W.EXCL_TAIL = tail
    ok(s11 == golden, "SF11: without the half hour after each exclusion the set is the same")
    s3 = ES.side_set(ES.sim27(R, C, E, G["h"], reps=120, exclude=False))
    sched = re.sub(r"\s+", " ", subprocess.run(["pdftotext", os.path.join(TARGET, PK.F_SCHED), "-"], capture_output=True, text=True).stdout)
    ok("Excluded Events are (a) planned maintenance within a window notified to the Partnership" in sched and
       "includes the 30 minutes following" in sched,
       "SF3: Schedule 4.3 files the exclusions (positive control on the shipped text); counting visits and interruptions as downtime "
       "instead lists %d hubs (%s the golden), a reading the clause rules out" % (len(s3), "the same as" if s3 == golden else "not"))
    ok(ES.side_set(variant(dso12=True)["av"]) == golden, "SF12: interruptions at the last twelve months' rate give the same set")
    ok(ES.side_set(variant(att=True)["av"]) == golden, "SF13: the fleet's attendance at every hub gives the same set")
    s14 = ES.side_set(ES.sim27(R, C, E, G["h"], reps=120, new_start=W.Y27_START))
    ok(s14 == golden, "SF14: the new units' uptime counted from 1 January 2027 instead of the works date gives the same set")
    ok(ES.side_set(ES.sim27(R, C, E, G["h"], reps=120, stat="median")) == golden, "SF5: the median simulated year gives the same set "
       "as the expected availability")
    C15 = copy.deepcopy(C)
    for k, u in C15["units"].items():
        u["hangs"] = sorted(u["hangs"] + [(a - 750, b) for a, b, kd in u["kinds"] if kd == "comms" and b - a >= 3600])
    ok(ES.side_set(ES.sim27(R, C15, E, ES.hazard_binned(*ES.life_table(R, C15)), reps=120)) == golden,
       "SF15: every Offline spell over an hour read as a hang gives the same set")

    print("== the asks")
    gn, ge, gwh = A.golden(TARGET)
    hubs_codes = [h["code"] for h in H["hubs"]]
    tn = {h: 0 for h in hubs_codes}
    te = {h: 0 for h in hubs_codes}
    for c in charges:
        if c["model"] == "HX150" and not c["failed"] and c["m1"] > c["m0"] and A.WIN_A <= c["start"] < A.WIN_B:
            tn[c["hub"]] += 1
            te[c["hub"]] += c["m1"] - c["m0"]
    ok(tn == gn and all(abs(te[h] - gwh[h]) == 0 for h in hubs_codes), "Asks: the golden handling of the export reproduces the true "
       "charges and energy at every hub exactly")
    edges = [0.05 - abs(gwh[h] / 1e6 - round(gwh[h] / 1e6, 1)) for h in hubs_codes]
    ok(min(edges) >= 0.012, "Asks: every energy figure at least 0.012 MWh from its rounding edge (closest %.3f)" % min(edges))
    crn, cre = A.cracker(TARGET)
    fin, fie = A.full_includer(TARGET)
    ok(A.kept(crn, gn) == 0 and A.kept(cre, ge) == 0, "Asks: the cracker keeps %d of 30 charges and %d of 30 energy figures"
       % (A.kept(crn, gn), A.kept(cre, ge)))
    ok(A.kept(fin, gn) == 0, "Asks: the full includer (register merge) still misses every charges figure on the card continuations")
    d1 = [crn[h] - gn[h] for h in hubs_codes]
    d2 = [fin[h] - gn[h] for h in hubs_codes]
    ok(min(d1) >= 20 and min(d2) >= 5, "Asks: device mass: the cracker over by %d to %d charges, the full includer by %d to %d"
       % (min(d1), max(d1), min(d2), max(d2)))
    de = [ge[h] - cre[h] for h in hubs_codes]
    ok(min(de) >= 0.2, "Asks: the energy left in the gaps moves every hub by %.1f to %.1f MWh" % (min(de), max(de)))
    grp = A.connections(A.dedup(A.load(TARGET)[0]))
    jumps = [g[i]["m0"] - g[i - 1]["m1"] for g in grp for i in range(1, len(g)) if g[i]["m0"] > g[i - 1]["m1"]]
    gaps = [g[i]["a"] - g[i - 1]["b"] for g in grp for i in range(1, len(g)) if g[i]["m0"] == g[i - 1]["m1"]]
    ok(min(jumps) >= 300 and max(gaps) <= 5, "Asks: every resumed record opens at least %d Wh above its predecessor and every card "
       "continuation follows within %d s" % (min(jumps), max(gaps)))
    recs = A.dedup(A.load(TARGET)[0])
    pc = A.per_connector(recs)
    sep = []
    for key, lst in pc.items():
        for i in range(1, len(lst)):
            if lst[i]["m0"] == lst[i - 1]["m1"] and lst[i]["a"] - lst[i - 1]["b"] > 5:
                sep.append(lst[i]["a"] - lst[i - 1]["b"])
    ok(min(sep) >= 150, "Asks: genuine consecutive charges on a connector are at least %d s apart (a merge by time alone over-merges them)"
       % min(sep))
    ok(G["set"] == ES.golden(PA.read_pack(TARGET))["set"], "Separation: the call reads no session row (the golden is unchanged however "
       "the export is handled)")
    rt = copy.deepcopy(Rt)
    rt["cpd"] = {k: v * 1.04 for k, v in rt["cpd"].items()}
    ok(ES.side_set(ES.route_glm(rt, Ct, Et)[0]) == glm_set, "Separation: the default path's charges-a-day covariate read raw (every "
       "split record a charge) leaves its set where it was")
    cei = CE.main(TARGET, quiet=True)
    ok(cei["pair"] <= 60 and cei["leak"] < 50, "Ceiling: pair %.1f, mirror leakage %.1f per cent" % (cei["pair"], cei["leak"]))

    print("== input gates, house fixes, realism")
    ok(len(PK.FILES) >= 10 and all(os.path.exists(os.path.join(TARGET, f)) for f in PK.FILES) and sorted(os.listdir(TARGET)) == sorted(PK.FILES),
       "Input gates: %d files under target/, nothing else" % len(os.listdir(TARGET)))
    ok(len(set(f.rsplit(".", 1)[1] for f in PK.FILES)) >= 3, "Input gates: three formats (csv, xlsx, pdf)")
    nrows = sum(1 for _ in open(os.path.join(TARGET, PK.F_SESS))) - 1
    ok(nrows >= 25000, "Input gates: the session export holds %d rows" % nrows)
    md = json.load(open(os.path.join(TASK, "metadata.json")))
    ok(len(md["distractor_files"]) >= 2 and all(os.path.basename(d) in PK.FILES for d in md["distractor_files"]),
       "Input gates: %d distractors named in metadata.json" % len(md["distractor_files"]))
    src = open(os.path.join(HERE, "parse.py")).read() + open(os.path.join(HERE, "asks.py")).read()
    ok(all(os.path.basename(d) not in src for d in md["distractor_files"]), "Distractors: no route reads the survey or the tariff, so "
       "deleting either moves nothing")
    ok(not [f for f in os.listdir(TARGET) if re.search(r"readme|dictionary|notes|manifest|distractor", f, re.I)],
       "No file under target/ describes the data")
    libs = re.compile(rb"python-docx|openpyxl|pandas|pyarrow|reportlab|matplotlib", re.I)
    for f in PK.FILES + ["../golden/availability_plan_2027.pdf"]:
        p = os.path.join(TARGET, f)
        if f.endswith(".xlsx"):
            z = zipfile.ZipFile(p)
            app = z.read("docProps/app.xml")
            core = z.read("docProps/core.xml")
            sheets = re.findall(rb'<sheet name="([^"]+)"', z.read("xl/workbook.xml"))
            ok(b"<AppVersion>16.0300</AppVersion>" in app and all(b"<vt:lpstr>" + s + b"</vt:lpstr>" in app for s in sheets)
               and not libs.search(app + core), "H1: %s carries Excel's app.xml (16.0300, its sheets in TitlesOfParts), no library name" % f)
        elif f.endswith(".pdf"):
            info = subprocess.run(["pdfinfo", p], capture_output=True, text=True).stdout
            ok(re.search(r"Producer:\s+LibreOffice \d", info) and re.search(r"Creator:\s+Writer\n", info) and re.search(r"Author:\s+\S", info)
               and re.search(r"Subject:\s+\S", info) and not libs.search(open(p, "rb").read()),
               "H1: %s exported by LibreOffice Writer with its issuer as Author and a Subject, no library name" % os.path.basename(f))
    ids = []
    with open(os.path.join(TARGET, PK.F_SESS), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ids.append(int(r["session_id"]))
    d = np.diff(sorted(set(ids)))
    ok(len(set(d.tolist())) > 3, "Realism: session numbers are not an arithmetic sequence")
    order = [h["code"] for h in sorted(H["hubs"], key=lambda h: h["name"])]
    ok(order != sorted(order), "Realism: hub codes do not follow the hubs' alphabetical order")
    shapes = set(" ".join(h["name"].split()[1:]) for h in H["hubs"])
    ok(len(shapes) > 2, "Realism: hub names take %d shapes" % len(shapes))
    ok(len(set(gn.values())) == 30 and len(set(ge.values())) >= 28, "Realism: no two hubs share a charges figure")
    ok(all(v % 100 != 0 for v in gn.values()), "Realism: no round charges total")
    ok(len(set(u["serial"] for u in H["units"])) == len(H["units"]) and len(set(u["new_id"] for u in H["units"])) == len(H["units"]),
       "Realism: serials and IDs unique")
    pd_off = [x for c in C["clusters"] for x in [cc[1] - cc[0] for cc in C["clusters"][c]]]
    ok(len(set(pd_off)) > 50, "Realism: pillar power-downs reach the back office over a spread of minutes (%d distinct spreads)" % len(set(pd_off)))
    print("\n%d assertions, %d failed" % (N[0], len(FAILS)))
    if FAILS:
        sys.exit(1)


if __name__ == "__main__":
    main(fast="--fast" in sys.argv)
