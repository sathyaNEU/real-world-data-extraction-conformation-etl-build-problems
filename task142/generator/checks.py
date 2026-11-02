"""Generator checks for task142 (architecture 3) on the installed pack, the clean truth (world.py) and the golden.

    python3 task142/generator/checks.py          # exit 1 on any failed assertion

Blocks: G input gates, R1 to R3 the client's three rules on the clean truth, SF the semantic fork table, F the cheap
routes, B the graded figures' bin edges, M the call's population and the ask devices, A the ask layer, S realism.
"""
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from collections import Counter

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import ceiling as CE  # noqa: E402
import params as P  # noqa: E402
import world as W  # noqa: E402

TARGET = os.path.join(TASK, "target")
FAIL = []
N = [0]


def ok(label, cond, detail=""):
    N[0] += 1
    print("%-4s %-62s %s" % ("OK" if cond else "FAIL", label, detail))
    if not cond:
        FAIL.append(label)


def dist(x, u):
    r = x / u
    return u * (0.5 - abs(r - round(r)))


def main():
    F, M = A.figures(TARGET)
    T = M["T"]
    C = M["C"]
    r = M["routes"]
    w = W.build()
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    files = sorted(os.listdir(TARGET))
    prompt = open(os.path.join(TASK, "prompt.txt")).read()

    # ---------------------------------------------------------------- G: input gates
    ok("G1 ten or more files", len(files) >= 10, "%d files" % len(files))
    fm = Counter(f.rsplit(".", 1)[1] for f in files)
    ok("G2 three or more formats", len(fm) >= 3, dict(fm))
    ok("G3 a file of 25,000 rows or more", len(T["brp"]) >= 25000, "%d register rows" % len(T["brp"]))
    ok("G4 two or more distractors named in metadata", len(meta["distractor_files"]) >= 2 and
       all(f in files for f in meta["distractor_files"]), meta["distractor_files"])
    bad = [f for f in files if re.search(r"readme|dictionar|notes|manifest|schema|test_|trap|decoy|distract", f, re.I)]
    ok("G5 no file name describes the data or the author's intent", not bad, bad or "clean")
    import openpyxl
    sheets = [(f, s) for f in files if f.endswith(".xlsx") for s in openpyxl.load_workbook(os.path.join(TARGET, f)).sheetnames]
    ok("G6 no sheet describes the data", not [s for s in sheets if re.search(r"readme|toelichting|notes|uitleg|legend", s[1], re.I)],
       "%d sheets" % len(sheets))
    ok("G7 every file has source, date and licence", all(set(meta["files"][f]) >= {"source", "date", "license"} for f in files))
    ok("G8 one deliverable, named in the prompt", meta["deliverables"] == ["kwikstaart_leerlingenprognose_2027-2029.docx"]
       and meta["deliverables"][0] in prompt)

    # ---------------------------------------------------------------- R1: the raw material ships
    ok("R1a the register carries persons, households, birth dates and residence periods",
       set(T["brp"][0]) >= {"persoonsnummer", "huishoudnummer", "geboortedatum", "datum_adres", "datum_vertrek"})
    ok("R1b the roll carries every pupil at every count with birth date and address",
       set(T["roll"][0]) >= {"teldatum", "geboortedatum", "postcode", "huisnummer", "groep"})
    heads = list(T["brp"][0]) + list(T["roll"][0])
    ok("R1c no column holds a sibling, a circumstance or a share", not [h for h in heads if re.search(
        r"sib|broer|zus|omstandig|aandeel|share|kans", h, re.I)], heads[:4])
    ok("R1d no shared key between the register and the roll",
       not (set(T["brp"][0]) & {"leerlingnummer"}) and not (set(T["roll"][0]) & {"persoonsnummer", "huishoudnummer"}))
    truth_sib = {p["pid"]: bool(p.get("sib_at_entry")) for p in w["kids"] if p.get("sib_at_entry") is not None}
    ok("R1e the circumstance read from the pack is the clean truth's", M["tot"][True][0] == sum(
        1 for p in w["kids"] if p.get("sib_at_entry") and A.cohort(p["birth"]) in A.INTAKES and p["hh"]["wijk"] in
        ("Molenwijk", "Rietveld") and W.lives_in(p, dt.date(A.cohort(p["birth"]), 10, 1))), "%d" % M["tot"][True][0])

    # ---------------------------------------------------------------- R2: Layer 1 present and neutral
    ok("R2a dates in two formats (register dd-mm-yyyy, roll ISO)", re.fullmatch(r"\d\d-\d\d-\d{4}", T["brp"][0]["geboortedatum"])
       is not None and re.fullmatch(r"\d{4}-\d\d-\d\d", T["roll"][0]["geboortedatum"]) is not None)
    adds_roll = {x["toevoeging"] for x in T["roll"] if x["toevoeging"]}
    ok("R2b additions typed two ways", any("-" in a or a.islower() for a in adds_roll), sorted(adds_roll)[:5])
    ok("R2c the pupil administration changed numbering in 2023", {len(x["leerlingnummer"]) for x in T["roll"]
       if x["teldatum"].endswith("2022")} == {4} and all(x["leerlingnummer"].startswith("KW") for x in T["roll"]
                                                         if x["teldatum"].endswith("2023")))
    ok("R2d households left the district during the intakes", sum(1 for x in T["brp"] if x["datum_vertrek"]) > 500)

    # ---------------------------------------------------------------- R3: the three rules on the clean truth
    proc = A.pdf_text(os.path.join(TARGET, P.FILES["procedure"]))
    plan = T["plan"]
    named = [t for t in ("sibling list", "these children", "per cent", "share of") if t in plan.lower()]
    ok("R3a no document states a share or a forecast of the roll", not re.search(r"\d+\s*per cent", proc + plan) and
       "forecast" not in plan.lower().replace("it does not forecast pupils", ""), named or "none")
    ok("R3b analyst test: every default route files none", all(M["calls"][k] is None for k in ("pooled", "by_wijk", "trend",
                                                                                               "mean_yearly")),
       {k: M["calls"][k] for k in ("pooled", "by_wijk", "trend", "mean_yearly")})
    ok("R3b' the circumstance route files 2029-30", M["calls"]["golden"] == 2029)
    ok("R3b'' every child entering files 2028-29", M["calls"]["everyone"] == 2028)
    ok("R3c PV-2 names the circumstance and lists no child, share or join key",
       "same circumstance" in proc and "brother or sister from the same household" in proc and
       not re.search(r"\d+\s*per cent|birth date|postcode", proc))
    ok("R3d the circumstance is nameable without the outcome (newest lesson)",
       all(p["sib_at_entry"] == any(q is not p and q["child"] and q["birth"] < p["birth"] and W.on_roll(q, A.cohort(p["birth"]))
                                    for q in p["hh"]["members"])
           for p in w["kids"] if p.get("sib_at_entry") is not None))

    # ---------------------------------------------------------------- SF: the fork table
    ok("SF1 a count is the 1 October roll", "on the school's roll on 1 October" in proc.replace("  ", " "))
    ok("SF2 the intake: turned four in the twelve months to the count", "turned four in the twelve months to that 1 October"
       in proc.replace("  ", " "))
    ok("SF3 the mean of yearly shares gives the same call", M["calls"]["mean_yearly"] is None and
       abs(M["mean_yearly"] - M["pooled"]) < 0.02, "%.3f against %.3f" % (M["mean_yearly"], M["pooled"]))
    ok("SF4 the circumstance is filed as a brother or sister of the household on the roll at the first count",
       "on the school's roll at the count at which the child first counts" in proc.replace("  ", " "))
    alt = forecast_with_entering_siblings(M)
    ok("SF5 counting siblings who would enter in 2027-28 gives the same call", alt is not None and alt["call"] == 2029,
       "%.1f at 2029-30" % alt["p29"])
    ok("SF6 the intake's children live in the catchment on that 1 October", "living in the catchment on the 1 October of their"
       in proc.replace("  ", " "))
    ok("SF7 the catchment is 3841 and 3842", "3841" in plan and "3842" in plan)
    ok("SF8 out-of-catchment entrants at their five-intake average", "average over the last five intakes" in proc.replace("  ", " "))
    ok("SF9 the 2026 roll stays until group 8", "will not yet have completed group 8" in proc.replace("  ", " "))
    ok("SF10 the rounded forecast gives the same call", (F["pupils"]["2029"] > C) == (r["golden"][2029] > C) and
       (F["pupils"]["2028"] > C) == (r["golden"][2028] > C))
    ok("SF11 the household is the register's", "as the municipal population register records it" in proc.replace("  ", " "))
    ok("SF12 linking by birth date and postcode alone gives the same call", link_loose(T)["call"] == 2029)
    ok("SF13 gas school years at the 06:00 reads of 1 August exist", any(x["tijdstip"].startswith("2024-08-01T06:00")
                                                                         for x in T["gasreads"]))
    ok("SF14 both buildings' gas", len({m["ean"] for m in T["gas_meters"]}) == 3)
    dep = {x["locatiecode"] for x in T["bso_loc"] if x["adres"] == "Molenwiek 4"}
    ok("SF15 the dependance's locations are two codes at Molenwiek 4", dep == {"BSO-KWS", "BSO-MLW2"})
    ok("SF16 an attendance is one pupil: some family rows carry two children", any(int(x["aantal_kinderen"]) > 1 for x in T["bso"]))

    # ---------------------------------------------------------------- F: cheap routes
    land = [k for k in ("pooled", "by_wijk", "trend", "mean_yearly", "everyone") if M["calls"][k] == 2029]
    ok("F1 no cheap route lands 2029-30", not land, land or "none")
    ok("F2 margins: golden over at 2029-30 and under at 2028-29 by 15 or more, every default 25 or more under",
       r["golden"][2029] - C >= 15 and C - r["golden"][2028] >= 15 and all(C - r[k][2029] >= 25 for k in ("pooled", "by_wijk",
                                                                                                           "trend", "mean_yearly")),
       "%.1f over, %.1f under; defaults %s" % (r["golden"][2029] - C, C - r["golden"][2028],
                                               [round(C - r[k][2029], 1) for k in ("pooled", "by_wijk", "trend", "mean_yearly")]))

    # ---------------------------------------------------------------- B: bin edges
    for Y in A.FORE:
        ok("B1 pupils %d clear the nearest-10 edge" % Y, dist(r["golden"][Y], 10) >= 1.5, "%.1f, %.1f from the edge" %
           (r["golden"][Y], dist(r["golden"][Y], 10)))
    ok("B2 the shares clear their whole-per-cent edges", dist(100 * M["rates"][True], 1) >= 0.1 and
       dist(100 * M["rates"][False], 1) >= 0.1, "%.2f and %.2f" % (100 * M["rates"][True], 100 * M["rates"][False]))
    for sy, v in F["gas_m3_exact"].items():
        ok("B3 gas %s clears its edge" % sy, dist(v, 1000) >= 200, "%d m3, %.0f from the edge" % (v, dist(v, 1000)))

    # ---------------------------------------------------------------- M: the call's population and the devices
    tmp = tempfile.mkdtemp()
    for f in files:
        if not f.startswith(("gas_", "meterstam", "bso_")):
            shutil.copy(os.path.join(TARGET, f), tmp)
    try:
        Mx = A.main_call(tmp, A.load(tmp, main_only=True))
        same = Mx["calls"]["golden"] == M["calls"]["golden"] and abs(Mx["routes"]["golden"][2029] - r["golden"][2029]) < 1e-9
    finally:
        shutil.rmtree(tmp)
    ok("M1 the call reads no gas or after-school-care file", same)
    eans_plan = set(re.findall(r"8716\d{14}", plan))
    ok("M2 the re-registered EAN is absent from the plan", len(eans_plan) == 2 and len({str(g["ean"]) for g in T["gas_conn"]}) == 3)
    tele = {(x["meternummer"], x["soort"]) for x in T["gasreads"]}
    exch = [m for m in T["gas_meters"] if m["reden"] == "vervangingsprogramma"]
    ok("M3 exchanged meters' readings live in the master data only", len(exch) == 2 and
       all((str(m["meternummer"]), "E") not in tele for m in exch))
    kor = [x for x in T["bso"] if x["locatiecode"] == "BSO-MLW"]
    ok("M4 Molenwijk-location rows exist before the merger", len(kor) > 50 and all(A.dmy(x["datum"]) < dt.date(2026, 10, 12) for x in kor))

    # ---------------------------------------------------------------- A: the ask layer
    pair, leak, figs = CE.main(TARGET)
    ok("A1 the cracker misses every ask figure", not any(h for _, h in figs), "%d figures" % len(figs))
    ok("A2 the full includer hits every figure", all(A.rnd(v, 1000) == F["gas_m3"][s] for s, v in A.gas_by_year(T).items())
       and A.bso_by_weekday(T) == {int(k): v for k, v in F["bso"].items()})
    ok("A3 the gas and after-school-care truths match the pack", {str(k): v for k, v in w["bso_truth"].items()} == F["bso"]
       and all(abs(w["gas_truth"][int(s)] - v) < 3 for s, v in F["gas_m3_exact"].items()))
    ok("A4 pair ceiling at most 60, mirror leakage under 50", pair <= 60 and leak < 50, "%.1f, %.1f" % (pair, leak))

    # ---------------------------------------------------------------- S: realism
    ok("S1 the capacity is not a multiple of 5", C % 5 != 0, C)
    cnt = Counter(x["huishoudnummer"] for x in T["brp"])
    ok("S2 household sizes vary", len(set(cnt.values())) >= 4, dict(Counter(cnt.values())))
    sig = []
    for f in files:
        raw = open(os.path.join(TARGET, f), "rb").read()
        if f.endswith((".xlsx", ".docx")):
            z = zipfile.ZipFile(os.path.join(TARGET, f))
            raw = b"".join(z.read(n) for n in z.namelist() if n.startswith("docProps"))
        sig += [(f, s) for s in (b"openpyxl", b"python-docx", b"ReportLab", b"reportlab") if s in raw]
    ok("S3 containers scrubbed of the toolchain", not sig, sig or "clean")
    late = [x for x in T["brp"] if x["datum_adres"] and A.dmy(x["datum_adres"]) > dt.date(2026, 10, 1)]
    ok("S4 no register date after the extract", not late)
    ok("S5 the roll's counts vary year to year", len({sum(1 for x in T["roll"] if x["teldatum"].endswith(str(y)))
                                                       for y in range(2020, 2027)}) == 7)
    ok("S6 personas are the drawn names", set(P.PEOPLE.values()) == {"Jayda Tins", "Raf Romijn", "Norah Bresé"})
    ok("S7 no em dash in the write-up", "—" not in open(os.path.join(TASK, "submission.md")).read())
    print("%d checks, %d failed" % (N[0], len(FAIL)))
    return 1 if FAIL else 0


def forecast_with_entering_siblings(M):
    """SF5: a coming child also counts as having a sibling when an older sibling would enter in 2027 or 2028 (at that
    sibling's own circumstance share), the expected circumstance mixed by that probability."""
    T = M["T"]
    ps = A.persons(T)
    idx = A.roll_index(T)
    by = {}
    for p in ps:
        by.setdefault(p["hid"], []).append(p)
    base = idx[2026]
    day = dt.date(2026, 10, 1)
    rates = M["rates"]
    fut = [p for p in ps if 2027 <= A.cohort(p["birth"]) <= 2029 and A.lives(p, day) and p["pc"][:4] in A.CATCH]
    first = {}
    for p in sorted(fut, key=lambda q: q["birth"]):
        c = A.cohort(p["birth"])
        on26 = any(q is not p and q["birth"] < p["birth"] and A.lives(q, day) and A.key(q) in base and base[A.key(q)] + (c - 2026) <= 8
                   for q in by[p["hid"]])
        pr_sib = 1.0 if on26 else 0.0
        for q in by[p["hid"]]:
            if q is not p and q["pid"] in first and A.cohort(q["birth"]) < c:
                pr_sib = pr_sib + (1 - pr_sib) * first[q["pid"]]
        rate = pr_sib * rates[True] + (1 - pr_sib) * rates[False]
        first[p["pid"]] = rate
    out = {}
    for Y in A.FORE:
        stay = sum(1 for g in base.values() if g + (Y - 2026) <= 8)
        out[Y] = stay + sum(v for k, v in first.items() if A.cohort(next(p for p in fut if p["pid"] == k)["birth"]) <= Y) + \
            M["out_avg"] * (Y - 2026)
    call = next((Y for Y in A.FORE if out[Y] > M["C"]), None)
    return {"call": call, "p29": out[2029]}


def link_loose(T):
    """SF12: the register linked to the roll by birth date and postcode only."""
    orig = A.key
    try:
        A.key = lambda p: (p["birth"], p["pc"])
        idx0 = A.roll_index

        def loose_index(T_):
            out = idx0(T_)
            return {y: {(k[0], k[1]): g for k, g in d.items()} for y, d in out.items()}
        A.roll_index = loose_index
        M = A.main_call(None, T)
    finally:
        A.key = orig
        A.roll_index = idx0
    return {"call": M["calls"]["golden"]}


if __name__ == "__main__":
    sys.exit(main())
