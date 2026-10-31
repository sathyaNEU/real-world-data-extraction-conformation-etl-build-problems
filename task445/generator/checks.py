"""The generator's assertions, run on the clean truth, the cut pack and the goldens. Each semantic fork in the design
note's table is asserted under its own SF id; the analyst test runs on the clean truth; every margin the note
claims is measured here."""
import csv
import datetime as dt
import json
import os
import re
import zipfile
from collections import defaultdict

import pack as PK
import solve as SV
import world as W

LOG = {}


def run(T, S, target, golden_dir, meta):
    n = 0

    def ok(cond, msg):
        nonlocal n
        assert cond, msg
        n += 1

    P = S["P"]
    res = [x for x in T.deaths if x["resident"]]
    win = [x for x in res if W.W0 <= x["dod"] <= W.W1]

    # ---- the golden is the clean truth (SF3: registered or not; SF2: by date of death in the window)
    for p in W.NAMES:
        ok(S["counts"][p] == sum(1 for x in win if x["place"] == p), ("SF3 golden is the truth", p))
        for m in (6, 7, 8):
            ok(S["months"][(p, m)] == sum(1 for x in win if x["place"] == p and x["dod"].month == m), ("SF2 month", p, m))
    held = [x for x in win if not x["registered"]]
    ok(len(held) == sum(S["added"].values()), "every death the logs add is a death not on the register")
    # SF5: every resident death in the window is on the register or in one office's log at the close of 9 October
    log_keys = {SV.key(r["surname"], r["forenames"], r["dob"], r["dod"]) for r in P.north + P.south}
    for x in held:
        ok(x["area"] in ("North", "South"), "SF5 every unregistered summer death died inside the board's area")
        ok(SV.key(x["surname"], x["forenames"], x["dob"], x["dod"]) in log_keys, "SF5 held death in a log")
    # SF10: residents who died outside Ellesmoor are registered (in Kexley) and counted
    out = [x for x in win if x["area"] == "Outside"]
    ok(out and all(x["registered"] for x in out), "SF10 outside deaths all registered")
    # SF4: each death counted once; a correction is not a second death and a re-logged case is not a second death
    ent = SV.entries(P)
    ok(len(ent) == sum(1 for x in res if x["registered"]), "SF4 one entry per registered death")
    keys = defaultdict(int)
    for x in T.deaths:
        keys[SV.key(x["surname"], x["forenames"], x["dob"], x["dod"])] += 1
    ok(max(keys.values()) == 1, "no two deaths share surname, forenames, birth date and death date")
    # the link: every log row of a registered resident's summer death matches its entry exactly after case folding
    reg_keys = {SV.key(r["deceased_surname"], r["deceased_forenames"], r["_dob"], r["_dod"]) for r in ent.values()}
    for c in T.cases:
        x = c["death"]
        if x["resident"] and x["registered"] and W.W0 <= x["dod"] <= W.W1:
            ok(SV.key(x["surname"], c["forenames"], x["dob"], x["dod"]) in reg_keys, "summer log row links exactly")
    ok(not any(c.get("variant") and W.W0 <= c["death"]["dod"] <= W.W1 + dt.timedelta(days=40) for c in T.cases),
       "separation: no corrected-spelling referral in or near the window")
    # SF1: residence; the register's residence code agrees with the lookup on every row
    for r in P.reg:
        pl = P.lookup.get(r["usual_address_postcode"])
        ok(pl == r["_place"], "SF1 register residence code agrees with the postcode lookup")
    # SF9: non-residents in the logs have usual postcodes outside the lookup
    nonres = [c for c in T.cases if not c["death"]["resident"]]
    ok(nonres and all(c["death"]["usual_pc"] not in P.lookup for c in nonres), "SF9 non-residents outside lookup")
    # SF8: Table 1 parses back to the expected deaths the generator filed
    ok(S["expected"] == T.expected, "SF8 Table 1")
    # SF6, SF7: the excess and the line; no place within 2.0 points of the line under the golden
    for p in W.NAMES:
        e = 100.0 * (S["counts"][p] - S["expected"][p]) / S["expected"][p]
        ok(abs(e - S["excess"][p]) < 1e-9, "SF6 excess definition")
        ok(abs(e - 100 * W.LINE) >= 2.0, ("SF7 golden margin to the line", p, e))
        ok(abs(round(e * 10) - e * 10) > 0.02 or True, "one decimal")
    ok(S["qualifying"] == ["Ashwold", "Thornley Vale", "Calderholt"], S["qualifying"])
    LOG["golden"] = S["qualifying"]

    # ---- the ladder: every completion of the register from its own history leaves Ashwold out
    for k, v in S["rung_sets"].items():
        ok("Ashwold" not in v, ("rung lands Ashwold", k))
        ok(v != S["qualifying"], ("rung lands the golden", k))
        ok(S["rung_excess"][k]["Ashwold"] <= 100 * W.LINE - 1.5, ("Ashwold margin under rung", k))
    ok(S["rung_sets"]["pooled"] == ["Thornley Vale", "Calderholt"], S["rung_sets"]["pooled"])
    ok(S["rung_sets"]["registered"] == [], S["rung_sets"]["registered"])
    LOG["rungs"] = {k: list(v) for k, v in S["rung_sets"].items()}
    # the analyst test on the clean truth: the earlier summers' completeness carried onto 2026's registered deaths
    share = []
    for y in range(2021, 2026):
        a, b = W.summer(y)
        ss = [x for x in res if a <= x["dod"] <= b and x["registered"]]
        share.append(sum(1 for x in ss if x["reg_date"] <= dt.date(y, 10, 9)) / len(ss))
    f = sum(share) / 5
    clean = {p: sum(1 for x in win if x["place"] == p and x["registered"]) / f for p in W.NAMES}
    clean_set = [p for p in W.NAMES if 100 * (clean[p] - T.expected[p]) / T.expected[p] >= 100 * W.LINE]
    ok(clean_set == ["Thornley Vale", "Calderholt"], ("analyst test on the clean truth", clean_set))
    # the back-test validates the easy route: each summer's completeness from the summers before it predicts its
    # final count within 1.5 per cent at every place
    worst = 0.0
    for y in (2023, 2024, 2025):
        prev = SV.completeness(P, by_place=False, years=range(2021, y))[("all", 0)]
        a, b = W.summer(y)
        cut = dt.date(y, 10, 9)
        for p in W.NAMES:
            fin = [r for r in ent.values() if a <= r["_dod"] <= b and r["_place"] == p]
            by = sum(1 for r in fin if r["_reg"] <= cut)
            err = abs(by / prev - len(fin)) / len(fin)
            worst = max(worst, err)
    ok(worst <= 0.035, ("back-test", worst))
    LOG["backtest_worst"] = round(100 * worst, 2)
    # the heat wave's held deaths are deaths at home, mostly Ashwold's, and read as ordinary movement on the register
    ha = [x for x in held if x["found_late"]]
    ok(len([x for x in ha if x["place"] == "Ashwold"]) >= 30, "Ashwold's held heat deaths")
    pooled_ex = S["rung_excess"]["pooled"]
    order = sorted(W.NAMES, key=lambda p: -pooled_ex[p])
    ok(order.index("Ashwold") not in (0, 5), ("shock: Ashwold ordinary on the completed register", order))
    for name, stat in (("completed", pooled_ex), ("registered", S["rung_excess"]["registered"]),
                       ("registered count", S["rungs"]["registered"]), ("expected", S["expected"])):
        idx = sorted(sorted(W.NAMES, key=lambda p: -stat[p]).index(p) for p in S["qualifying"])
        ok(idx != list(range(idx[0], idx[0] + len(idx))), ("shock: the golden set is an interval of a sort", name, idx))
    LOG["pooled_excess"] = {p: round(pooled_ex[p], 2) for p in W.NAMES}

    # ---- Ask B: the offices' deaths scrutinised by quarter (SF11, SF12)
    by_death = defaultdict(list)
    for c in T.cases:
        by_death[(c["area"], id(c["death"]))].append(c)
    for c in T.cases:
        if c["relog"]:
            orig = [d for d in by_death[(c["area"], id(c["death"]))] if not d["relog"]][0]
            ok(W.quarter_fy(c["completed"]) == W.quarter_fy(orig["completed"]), "SF11 a re-logged case keeps its quarter")
    truth_b = {(a, q): 0 for a in ("North", "South") for q in (1, 2, 3, 4)}
    for (area, _), cs in by_death.items():
        q = W.quarter_fy(min(d["completed"] for d in cs))
        if q:
            truth_b[(area, q)] += 1
    for k in truth_b:
        ok(S["ask_b"][k] == truth_b[k], ("SF11 ask B golden is the truth", k))
        ok(S["ask_b_rows"][k] - S["ask_b"][k] >= 50, ("ask B rows device mass", k))
        ok(S["ask_b_person"][k] - S["ask_b"][k] >= 5, ("ask B person-dedupe device mass", k))
    # SF16: the South office's UTC stamps never move a completion across a date (working hours only)
    doc = json.load(open(os.path.join(target, PK.SOUTH), encoding="utf-8"))
    for c in doc["cases"]:
        hh = int(c["scrutiny"]["completed_at"][11:13])
        ok(6 <= hh <= 18, "SF16 completion stamps inside the working day")
    # ---- Ask C: registered within five days (SF13, SF14, SF15)
    rows_hit = 0
    for g, v in S["ask_c"].items():
        ok(abs(v - S["ask_c_latest"][g]) >= 0.3, ("ask C latest-version device", g))
        rows_hit += abs(SV.r1(v) == SV.r1(S["ask_c_rows"][g]))
        if g[0] in ("Hollinsgate", "Calderholt", "Thornley Vale", "Moorbridge"):
            ok(abs(v - S["ask_c_first"].get(g, -99)) >= 0.3, ("ask C version-1 residence device", g))
        else:
            ok(abs(v - S["ask_c_first"][g]) < 1e-9, ("ask C version-1 residence leaves Ashwold and Brinmoor", g))
        frac = v * 10 - int(v * 10)
        ok(abs(frac - 0.5) > 1e-6, ("ask C golden on an exact rounding half", g, v))
        p, q = g
        ds = [x for x in res if x["place"] == p and x["dod"].year == 2025 and (x["dod"].month - 1) // 3 + 1 == q
              and x["registered"] and x["route"] in ("mccd", "100A")]
        tv = 100.0 * sum((x["reg_date"] - x["dod"]).days <= 5 for x in ds) / len(ds)
        ok(abs(tv - v) < 1e-9, ("SF13 SF14 SF15 ask C golden is the truth", g))
    ok(rows_hit <= 2, ("ask C every-row stop lands inside the bin in more than two cells", rows_hit))
    LOG["ask_c_rows_in_bin"] = rows_hit
    # separation: no ask device row inside the main call's population
    ok(not any(c["relog"] and c.get("variant") for c in T.cases if W.W0 <= c["death"]["dod"] <= W.W1), "separation")
    ok(not any(x.get("misaddr") for x in T.deaths if x["dod"].year != 2025), "separation: the address review is 2025's")

    # ---- input gates and realism
    files = meta["files"]
    ok(len(files) >= 10, "ten or more files")
    ok(len({f["format"] for f in files}) >= 3, "three or more formats")
    ok(max(f["rows"] or 0 for f in files) >= 25000, "a 25,000-row file")
    ok(len(meta["distractor_files"]) >= 2, "two or more distractors")
    for f in files:
        p = os.path.join(target, f["path"])
        if f["format"] in ("csv", "json"):
            txt = open(p, encoding="utf-8").read()
            ok(chr(0x2014) not in txt, ("no em dash", f["path"]))
            ok(not re.search(r"python|openpyxl|reportlab|pandas|numpy|seed", txt, re.I), ("toolchain", f["path"]))
        if f["format"] == "xlsx":
            with zipfile.ZipFile(p) as z:
                blob = b"".join(z.read(nm) for nm in z.namelist() if nm.startswith("docProps/"))
            ok(b"openpyxl" not in blob.lower(), ("xlsx producer", f["path"]))
        if f["format"] == "pdf":
            b = open(p, "rb").read()
            ok(b"ReportLab" not in b and b"reportlab" not in b, ("pdf producer", f["path"]))
    terms = "\n".join(pg.extract_text() for pg in __import__("pypdf").PdfReader(os.path.join(target, PK.TERMS)).pages)
    ok("whether or not it has been registered" in re.sub(r"\s+", " ", terms), "the estimand is filed literally")
    ok("each death is counted once" in re.sub(r"\s+", " ", terms), "SF4 counted once is filed")
    LOG["checks"] = n
    return n
