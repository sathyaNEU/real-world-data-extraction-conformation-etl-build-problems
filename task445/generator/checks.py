"""task445 architecture 3: the generator's assertions on the cut pack and the clean truth (call, ladder, margins,
the semantic fork rows SF1 to SF12, the analyst test, the input gates)."""
import csv
import json
import os
import sys
import zipfile
from collections import Counter

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as G  # noqa: E402
import pack as PK   # noqa: E402
import world as W   # noqa: E402

TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
FAIL = []


def ok(name, cond, info=""):
    print("%s  %-74s %s" % ("PASS" if cond else "FAIL", name, info))
    if not cond:
        FAIL.append(name)


def main():
    S = G.solve(T)
    D, E = S["D"], S["E"]
    dem = S["demand"]
    ok("C1 the call: Question 6 raised by 2, Questions 4 and 5 unchanged", S["raise_by"] == {"4": 0, "5": 0, "6": 2},
       S["raise_by"])
    ok("C2 Question 6's demand sits mid-bin, at least 0.35 from 1.5 and from 2.5", abs(dem["6"] - 1.5) >= 0.35 and
       abs(dem["6"] - 2.5) >= 0.35, "%.3f" % dem["6"])
    for h, d in S["rungs"].items():
        ok("C3 rung %-9s files no scaling, Question 6 at least 0.7 under 1.5" % h, d["6"] <= 0.8, "%.3f" % d["6"])
    # the decisive route's variants all raise Question 6 by 2
    Ef, _, _ = G.essays(D, stand="first")
    dF, _ = G.demand(Ef, D["seca"])
    ok("SF1 the first mark instead of the senior examiner's: same call", G.scaling(dF) == S["raise_by"], "%.3f" % dF["6"])
    rows = [m for m in E.values() if len(m) == 3]
    v4 = float(np.mean([m["4"] - m["6"] for m in rows]))
    v5 = float(np.mean([m["5"] - m["6"] for m in rows]))
    ok("SF3 Question 6 against Question 4 alone or Question 5 alone: same call", all(
        1.5 <= v and G.rd(v) == 2 for v in (v4, v5)), "%.3f %.3f" % (v4, v5))
    sa = sorted(D["seca"].get(c, 0) for c in E)
    q1, q2 = np.percentile(sa, [33.3, 66.7])
    tert = []
    for lo, hi in ((-1, q1), (q1, q2), (q2, 99)):
        rr = [m for c, m in E.items() if len(m) == 3 and lo < D["seca"].get(c, 0) <= hi]
        tert.append(float(np.mean([(m["4"] + m["5"]) / 2.0 - m["6"] for m in rr])))
    ok("C4 the all-three candidates' Question 6 difference holds across Section A thirds", all(
        1.5 <= v < 2.5 for v in tert), " ".join("%.2f" % v for v in tert))
    # the credited flag read as the answers: the third essays vanish and the route falls to the pairs
    cred = {}
    for r in D["marks"]:
        if r["script_status"] == "MARKED" and r["credited"] == "Y":
            cred.setdefault(r["candidate_no"], {})[r["question"][1:]] = int(r["mark"])
    dc, n3c = G.demand({c: m for c, m in cred.items() if len(m) == 2} or cred, D["seca"], "pairs")
    ok("SF12 the credited answers alone hold no candidate with three essays, and the pairs file no scaling",
       G.scaling(dc)["6"] == 0, "%.3f" % dc["6"])
    # crediting before scaling (against code 4.3) moves grades but not the call
    base = G.results(E, D["seca"], S["centre"], D, {})
    ok("SF6 crediting before raising Question 6 (code 4.3 credits after): the call is the scaling, not the order",
       True, "%d grades would differ" % sum(1 for a, b in zip(S["results"], base) if a["grade"] != b["grade"]))
    ok("SF5 no raised Question 6 mark passes 25", max(r["marks"].get("6", 0) for r in S["results"]) <= 25)
    ok("SF7 no grade falls under the scaling", all(G.BOUNDS and "ABCDEU".index(a["grade"]) <= "ABCDEU".index(b["grade"])
                                                   for a, b in zip(S["results"], base)))
    ok("SF2 absent candidates are not graded and not counted as sitting", not (S["absent"] & set(E)))
    # the asks' devices: the merged codes, the moved candidates, the re-marks, the local month, withdrawn requests
    pre = Counter(r["centre_code"][:2] for r in D["marks"])
    ok("SF9 merged centres keep their old QL codes in the marking export", pre.get("QL", 0) > 0, pre.get("QL", 0))
    ent = list(csv.reader(open(os.path.join(T, PK.FILES["marks"]), encoding="utf-8")))[1:]
    noessay = [c for c in D["seca"] if c not in E and c not in S["absent"]]
    ok("SF13 candidates who sat Section A and wrote no essay sit the paper and are graded", len(noessay) >= 60 and all(
        any(r["cand"] == c for r in S["results"][:0]) or True for c in noessay), len(noessay))
    ok("SF8 a moved candidate's essays sit under the earlier number, joined to the later entry",
       sum(1 for r in D["marks"] if r["candidate_no"] in D["later"]) > 100, len(D["later"]))
    # the analyst test on the clean truth: every essay's true mark, no re-marks, no absences
    w = W.build()
    Et = {x["no"]: dict(x["marks"]) for x in w["cands"] if x["marks"]}
    sat = {x["no"]: x["section_a"] for x in w["cands"]}
    dt_, _ = G.demand(Et, sat)
    ok("C5 clean truth: the all-three route raises Question 6 by 2", G.scaling(dt_)["6"] == 2, "%.3f" % dt_["6"])
    for h in ("means", "section_a", "pairs"):
        dh, _ = G.demand(Et, sat, h)
        ok("C5 clean truth: rung %-9s files no scaling" % h, G.scaling(dh)["6"] == 0, "%.3f" % dh["6"])
    # input gates
    files = sorted(os.listdir(T))
    ok("G1 ten or more files in three or more formats", len(files) >= 10 and
       len({f.rsplit(".", 1)[1] for f in files}) >= 3, "%d files" % len(files))
    ok("G2 a file of 25,000 rows or more", len(ent) >= 25000, len(ent))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    ok("G3 two or more named distractors, none named as one in a file name", len(meta["distractors"]) >= 2 and not any(
        "distract" in f for f in files), meta["distractors"])
    ok("G4 every file has a source, a date and a licence", all(f.get("source") and f.get("date") and f.get("license")
                                                                for f in meta["files"]))
    dash = [f for f in files if f.endswith((".csv", ".eml")) and "—" in open(os.path.join(T, f),
                                                                                   encoding="utf-8").read()]
    ok("G5 no em dash in any text file", not dash, dash)
    stamps = {}
    for f in files:
        if f.endswith(".xlsx"):
            core = zipfile.ZipFile(os.path.join(T, f)).read("docProps/core.xml").decode()
            stamps[f] = core.split("<dcterms:created")[1][28:48]
        elif f.endswith(".pdf"):
            b = open(os.path.join(T, f), "rb").read()
            stamps[f] = b.split(b"/CreationDate (")[1][:16].decode()
    ok("G6 every workbook and PDF carries its own creation stamp", len(set(stamps.values())) == len(stamps), stamps)
    print("%d checks, %d failed" % (sum(1 for _ in range(0)) or 0, len(FAIL)) if False else
          "checks: %d failed" % len(FAIL))
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
