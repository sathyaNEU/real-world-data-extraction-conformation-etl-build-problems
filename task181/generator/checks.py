"""Assertions over the built pack and the goldens: the call, every rung by name with its margin, the twin
pair, every grid cell and its robustness variants, the clean main path, both asks and every stop, the
decoupling, the leak-hygiene sweeps, the pack gates and the containers. Run after build.py and
deliver.py; everything is computed from target/ (and golden/) through golden.py, plus the simulated world
where an assertion is about the world itself."""
import csv
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

import numpy as np
import openpyxl
import pandas as pd
import pdfplumber

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs as D        # noqa: E402
import golden as G      # noqa: E402
import world as W       # noqa: E402

TASK = os.path.dirname(HERE)
REPO = os.path.dirname(TASK)
N_ASSERT = [0]
LOG = []


def ok(cond, msg):
    N_ASSERT[0] += 1
    if not cond:
        raise AssertionError(msg)


WAGGA, GRIFFITH, SNOWY = "Wagga Wagga", "Griffith", "Snowy Valleys"
EXPECT_N = {"Wagga Wagga": 9, "Griffith": 7, "Leeton": 1, "Narrandera": 1, "Murrumbidgee": 0, "Hay": 0, "Edward River": 1,
            "Junee": 0, "Cootamundra-Gundagai": 2, "Snowy Valleys": 7}
EXPECT_E = {"Wagga Wagga": 1.4, "Griffith": 1.4, "Leeton": 0.6, "Narrandera": 0.4, "Murrumbidgee": 0.2, "Hay": 0.2,
            "Edward River": 0.4, "Junee": 0.2, "Cootamundra-Gundagai": 0.6, "Snowy Valleys": 1.4}
EXPECT_A = {"Wagga Wagga": (63, 2, 3, 2, 1), "Griffith": (25, 3, 2, 1, 1), "Leeton": (11, 0, 1, 0, 1),
            "Narrandera": (5, 0, 1, 0, 0), "Murrumbidgee": (0, 0, 0, 0, 0), "Hay": (2, 0, 0, 0, 0),
            "Edward River": (7, 1, 1, 1, 0), "Junee": (3, 1, 1, 0, 1), "Cootamundra-Gundagai": (15, 2, 1, 1, 1),
            "Snowy Valleys": (9, 1, 1, 1, 0)}
A_KEYS = ("confirmed", "probable", "infants", "admitted", "vaccinated")
EXPECT_B = [("Banna Avenue Public School", "Griffith", 5), ("Wollundry Public School", "Wagga Wagga", 3),
            ("Blowering Road Public School", "Snowy Valleys", 2), ("Bolton Park High School", "Wagga Wagga", 2),
            ("Kooyoo Street Public School", "Griffith", 2)]
RUNG_MARGIN, ANSWER_MARGIN, POOLED_MARGIN = 1.25, 2.5, 1.2
BANNED = re.compile(r"\b(delay\w*|completeness|incomplete|backfill\w*|nowcast\w*|truncat\w*|in transit|lag|lags|lagged|"
                    r"lagging|still arriving|provisional|preliminary|pending|outstanding|awaiting|turnaround|courier\w*|"
                    r"batch\w*|arriv\w*|catch[- ]up|not yet (?:notified|reported|received)|reporting time|time to notification)\b",
                    re.I)
TOOLCHAIN = re.compile(r"python-docx|python-pptx|openpyxl|reportlab|matplotlib|pandas|numpy|pyarrow|distractor|"
                       r"\bclaude\b|anthropic|lorem|placeholder|\bseed\b", re.I)
ASOF = dt.date(2026, 10, 5)


def lead_ok(score, want, margin):
    f, s, m = G.lead(score)
    return f == want and m >= margin, (f, s, round(m, 3))


# ------------------------------------------------------------------ text of the shipped files

def file_text(path):
    if path.endswith(".pdf"):
        with pdfplumber.open(path) as p:
            return "\n".join(pg.extract_text() or "" for pg in p.pages)
    if path.endswith(".xlsx"):
        wb = openpyxl.load_workbook(path, read_only=True)
        return "\n".join(str(v) for ws in wb.worksheets for row in ws.iter_rows(values_only=True) for v in row if v is not None) \
            + "\n" + "\n".join(ws.title for ws in wb.worksheets)
    if path.endswith(".parquet"):
        df = pd.read_parquet(path)
        return " ".join(df.columns) + "\n" + "\n".join(str(x) for c in df.columns if df[c].dtype == object for x in df[c].unique())
    if path.endswith(".csv"):
        df = pd.read_csv(path, dtype=str, keep_default_na=False)
        return " ".join(df.columns) + "\n" + "\n".join(str(x) for c in df.columns for x in df[c].unique())
    if path.endswith(".pptx"):
        from pptx import Presentation
        out = []
        for s in Presentation(path).slides:
            for sh in s.shapes:
                if sh.has_text_frame:
                    out.append(sh.text_frame.text)
                if getattr(sh, "has_table", False) and sh.has_table:
                    out += [c.text for r in sh.table.rows for c in r.cells]
        return "\n".join(out)
    return open(path, encoding="utf-8", errors="ignore").read()


# ------------------------------------------------------------------ the checks

def run(target, golden_dir, world=None, meta_path=None, quiet=False):
    Dd, g = G.solve(target, with_grid=True)
    ll, cases, conc = Dd["ll"], Dd["cases"], Dd["conc"]
    rungs, E, N = g["rungs"], g["E"], g["N"]

    # ---------------------------------------------------------------- the call and the ladder
    ok(g["answer"] == GRIFFITH, "answer moved: %s" % g["answer"])
    ok(N == EXPECT_N, "notified counts moved: %s" % N)
    ok(all(abs(E[a] - EXPECT_E[a]) < 1e-9 for a in G.AREAS), "expected counts moved: %s" % E)
    ok(all(abs(E[a] * 5 - round(E[a] * 5)) < 1e-9 for a in G.AREAS), "expected counts are fifths of whole counts")
    for name, sc in rungs.items():
        want, margin = (GRIFFITH, ANSWER_MARGIN) if name.startswith("R4") else (WAGGA, RUNG_MARGIN)
        good, info = lead_ok(sc, want, margin)
        ok(good, "%s: %s" % (name, info))
        if not name.startswith("R4"):
            ok(G.ranking(sc)[0] != GRIFFITH, "%s puts Griffith first" % name)
        LOG.append("%s -> %s (%.2f over %s at %.2f; margin %.2f)" % (name, info[0], sc[info[0]], info[1], sc[info[1]], info[2]))
    r1 = rungs["R1 notified less expected (PR-07 4.2, 4.3)"]
    ok(G.lead(r1)[2] >= 1.25, "Wagga Wagga's notified excess beats the next area by 25 per cent")
    ok(all(G.ranking(sc).index(GRIFFITH) == 1 for n, sc in rungs.items() if not n.startswith("R4")),
       "Griffith sits second (tied with its twin) on every rung below the answer")

    # ---------------------------------------------------------------- the twin pair
    ok(N[GRIFFITH] == N[SNOWY] and E[GRIFFITH] == E[SNOWY], "twin pair: same notified and expected counts")
    for n in ("R0 notified cases, specimens in the fortnight", "R1 notified less expected (PR-07 4.2, 4.3)",
              "R2 notified over expected", "R1b notified by notification date less expected"):
        ok(abs(rungs[n][GRIFFITH] - rungs[n][SNOWY]) < 1e-9 or n.startswith("R1b"), "twin pair tie on %s" % n)
    lab_g = cases[(cases["area"] == GRIFFITH) & (cases["date"] >= G.FORTNIGHT[0]) & (cases["date"] <= G.LAST_DAY)]["lab"]
    lab_s = cases[(cases["area"] == SNOWY) & (cases["date"] >= G.FORTNIGHT[0]) & (cases["date"] <= G.LAST_DAY)]["lab"]
    ok((lab_s == G.HOSP).all(), "Snowy Valleys' fortnight goes through the hospital laboratory")
    ok((lab_g == G.PRIV).sum() >= 5, "Griffith's fortnight is mostly Inland Pathology")

    # ---------------------------------------------------------------- the grid, cell by cell
    cells = g["grid"]
    ok(len(cells) == 54, "grid size %d" % len(cells))
    route_min, pooled_min, twin_min = 99.0, 99.0, 99.0
    for cell, sc in sorted(cells.items()):
        est, m, st, b = cell
        if st == "pooled":
            good, info = lead_ok(sc, WAGGA, POOLED_MARGIN)
            ok(good, "pooled cell %s: %s" % (cell, info))
            ok(G.ranking(sc)[0] != GRIFFITH, "pooled cell %s puts Griffith first" % (cell,))
            pooled_min = min(pooled_min, info[2])
        else:
            good, info = lead_ok(sc, GRIFFITH, ANSWER_MARGIN)
            ok(good, "route-specific cell %s: %s" % (cell, info))
            route_min = min(route_min, info[2])
            twin = (sc[GRIFFITH] + E[GRIFFITH]) / (sc[SNOWY] + E[SNOWY])
            ok(twin >= 2.5, "twin pair separated in %s: %.2f" % (cell, twin))
            twin_min = min(twin_min, twin)
    LOG.append("grid: 36 route-specific cells Griffith (min margin %.2f, twin ratio min %.2f); 18 pooled cells Wagga Wagga "
               "(min margin %.2f); misses 0" % (route_min, twin_min, pooled_min))
    g["grid_summary"] = dict(route_min=route_min, pooled_min=pooled_min, twin_min=twin_min)
    var_min = 99.0
    for est in G.ESTIMATORS:
        for st in ("route", "area", "pooled"):
            for b in G.BINS:
                variants = [("drop2024", 24)] + [("caselevel", m) for m in G.WINDOWS]
                for v, m in variants:
                    nc = G.nowcast(ll, cases, est, m, st, b, drop_epidemic=v == "drop2024", case_level=v == "caselevel")
                    sc = {a: nc[a] - E[a] for a in G.AREAS}
                    want = WAGGA if st == "pooled" else GRIFFITH
                    good, info = lead_ok(sc, want, POOLED_MARGIN if st == "pooled" else ANSWER_MARGIN)
                    ok(good, "variant %s %s %s %s %s: %s" % (v, est, m, st, b, info))
                    if st != "pooled":
                        var_min = min(var_min, info[2])
    LOG.append("variants (2024 epidemic months out of the 24-month history; case-level delays): every cell unchanged, "
               "route-specific min margin %.2f" % var_min)
    g["variant_min"] = var_min
    h12 = G.history(ll, 12)
    for lab in (G.HOSP, G.PRIV):
        d = h12[h12["notifying_lab"] == lab]["delay"]
        LOG.append("%s, 12-month history: median %d days, 95th percentile %d, n %d" % (
            lab, np.median(d), np.percentile(d, 95), len(d)))
    dp = ll[ll["notifying_lab"] == G.PRIV]["delay"]
    dh = ll[ll["notifying_lab"] == G.HOSP]["delay"]
    ok(10 <= np.median(dp) <= 14 and 19 <= np.percentile(dp, 95) <= 28, "private route speed")
    ok(1 <= np.median(dh) <= 3 and np.percentile(dh, 95) <= 6, "hospital route speed")
    ok(ll["delay"].max() <= 42, "every notification within 42 days, so the history window is complete")
    ok(int((ll["recv_day"] == ASOF).sum()) == 0, "no notification on the extract day before 07:00")
    ok(ll["recv_local"].max() < pd.Timestamp(W.EXTRACT_LOCAL), "nothing received after the extract ran")

    # ---------------------------------------------------------------- the main path is clean (mess neutrality)
    main = cases[cases["area"].notna() & cases["date"].apply(lambda d: any(
        dt.date(y, 9, 21) <= d <= dt.date(y, 10, 4) for y in G.PRIOR + (2026,)))]
    ok((main["n_notifications"] == 1).all(), "no repeat notification inside the main call's windows")
    ok((main["status"] == "Confirmed").all(), "no probable case inside the main call's windows")
    split = {p for p, rows in conc.items() if len(rows) > 1}
    ok(not main["postcode"].isin(split).any(), "no split postcode inside the main call's windows")
    win_rows = ll[ll["spec"].apply(lambda d: any(dt.date(y, 9, 21) <= d <= dt.date(y, 10, 4) for y in G.PRIOR + (2026,)))]
    ok(all(G.allocate(conc, p) for p in win_rows["postcode"]), "no visitor notification inside the main call's windows")
    pids = set(main["person_id"])
    near = cases[cases["person_id"].isin(pids)].groupby("person_id").size()
    ok((near == 1).all(), "no person in the main windows has another case")
    for label, cs in (("episode rule ignored", G.episodes(ll, conc, rule=False)),
                      ("split postcodes by first row", G.episodes(ll, conc, alloc="first")),
                      ("split postcodes to any unit area", G.episodes(ll, conc, alloc="any_unit"))):
        ok(G.notified(cs) == N and G.expected(cs) == E, "main call moves when %s" % label)
    ok(G.notified(cases, statuses=("Confirmed",)) == N and G.expected(cases, statuses=("Confirmed",)) == E,
       "main call moves when probable cases are dropped")
    utc_day = pd.to_datetime(ll["received_utc"], utc=True).dt.date
    ok(int((utc_day != ll["recv_day"]).sum()) > 50, "UTC and local received dates differ on many rows (texture)")

    # ---------------------------------------------------------------- the asks
    adm, births, reg = G.load_links(target)
    A = g["ask_a"]
    for a in G.AREAS:
        ok(tuple(A[a][k] for k in A_KEYS) == EXPECT_A[a], "ask A %s moved: %s" % (a, A[a]))
    B = g["ask_b"]
    ok(B == EXPECT_B, "ask B moved: %s" % B)

    def moves_a(label, other):
        diff = [(a, k, A[a][k], other[a][k]) for a in G.AREAS for k in A_KEYS if A[a][k] != other[a][k]]
        ok(len(diff) > 0, "ask A stop '%s' moves nothing" % label)
        LOG.append("ask A stop, %s: %s" % (label, "; ".join("%s %s %d->%d" % x for x in diff)))

    cases_norule = G.episodes(ll, conc, rule=False)
    moves_a("episode rule ignored", G.ask_a(cases_norule, adm, births, reg))
    moves_a("probable cases not counted", G.ask_a(cases, adm, births, reg, statuses=("Confirmed",)))
    moves_a("admissions without the 14-day link", G.ask_a(cases, adm, births, reg, adm_window=None))
    moves_a("antenatal dTpa at any time before birth", G.ask_a(cases, adm, births, reg, vacc_rule="anytime"))
    moves_a("any antenatal vaccine", G.ask_a(cases, adm, births, reg, vacc_rule="any_vaccine"))
    moves_a("infants under twelve months", G.ask_a(cases, adm, births, reg, infant_months=12))
    moves_a("split postcodes by first row", G.ask_a(G.episodes(ll, conc, alloc="first"), adm, births, reg))
    moves_a("split postcodes to any unit area", G.ask_a(G.episodes(ll, conc, alloc="any_unit"), adm, births, reg))
    rosters = g["rosters"]

    def moves_b(label, other):
        ok(other != B, "ask B stop '%s' moves nothing" % label)
        LOG.append("ask B stop, %s: %s" % (label, "; ".join("%s %s %d" % x for x in other) or "no clusters"))

    moves_b("school names matched exactly", G.ask_b(cases, rosters, match="exact"))
    moves_b("staff counted", G.ask_b(cases, rosters, roles=("Student", "Staff")))
    moves_b("parents counted", G.ask_b(cases, rosters, roles=("Student", "Parent or carer")))
    moves_b("episode rule ignored", G.ask_b(cases, rosters, episode_cases=cases_norule))
    moves_b("probable cases not counted", G.ask_b(cases, rosters, statuses=("Confirmed",)))
    moves_b("window by notification date", G.ask_b(cases, rosters, window="notification"))
    moves_b("preschool merged into the school of the same name", G.ask_b(cases, rosters, match="fuzzy"))
    # convergence: the infant boundary, the admission window, the pregnancy window
    ask_cases = cases[cases["area"].notna() & (cases["date"] >= G.ASK[0]) & (cases["date"] <= G.ASK[1])]
    ages = [(d - b).days / 30.4375 for d, b in zip(ask_cases["date"], ask_cases["dob"])]
    ok(not any(5.7 <= x <= 6.3 for x in ages), "no case near six months of age (day and calendar-month readings agree)")
    inf = ask_cases[[d < G.add_months(b, 6) for d, b in zip(ask_cases["date"], ask_cases["dob"])]]
    adm_by = {}
    for m_, d_ in zip(adm["mrn"], adm["admit"]):
        adm_by.setdefault(int(m_), []).append(d_)
    gaps = [abs((x - d).days) for m_, d in zip(inf["mrn"], inf["date"]) for x in adm_by.get(int(m_), [])]
    ok(all(gp <= 3 or gp >= 30 for gp in gaps), "infant admissions sit within 3 days of the specimen or 30 or more away")
    bmap = {int(b["baby_mrn"]): b for _, b in births.iterrows()}
    reg2 = reg.assign(key=[re.sub(r"\D", "", c) + str(i) for c, i in zip(reg["medicare_card"], reg["irn"])])
    for m_ in inf["mrn"]:
        b = bmap[int(m_)]
        born = dt.date.fromisoformat(b["birth_date"])
        ds = [(born - pd.Timestamp(x).date()).days for x, ag in zip(reg2[reg2["key"] == b["mother_medicare_no"]]["dose_date"],
                                                                     reg2[reg2["key"] == b["mother_medicare_no"]]["antigen"]) if ag == "dTpa"]
        ok(all(x >= 56 or 7 <= x <= 13 or x >= 365 for x in ds), "maternal doses are clearly in or clearly out")
        ok(not any(60 <= x < 365 and x > 7 * int(b["gestation_weeks"]) for x in ds), "no dose between pregnancies")
    # the clusters' students are on their rosters, and no roster match is ambiguous
    wb = openpyxl.load_workbook(os.path.join(target, "school_rosters_term3_2026.xlsx"), read_only=True)
    roster_people = {}
    for ws in wb.worksheets:
        for row in ws.iter_rows(min_row=9, values_only=True):
            if row[0] is None:
                continue
            k = (row[3].date() if hasattr(row[3], "date") else row[3], row[4], str(row[5]))
            roster_people.setdefault(k, []).append(ws.title)
    stud = cases[(cases["role"] == "Student") & (cases["school"] != "")]
    names = {k: v["name"] for k, v in rosters.items()}
    for _, c in stud.iterrows():
        k = G.school_key(c["school"], names)
        if k is None:
            continue
        hits = roster_people.get((c["dob"], cases_sex(ll, c["person_id"]), c["postcode"]), [])
        ok(hits == [k], "student %s on roster %s: %s" % (c["person_id"], k, hits))

    # ---------------------------------------------------------------- decoupling
    ok(not ((cases["date"] >= G.ASK[0]) & (cases["date"] <= G.ASK[1]) & (cases["date"] >= G.FORTNIGHT[0])).any(),
       "ask A shares no row with the main call's fortnight")
    for est, m, st, b in (("aggregate", 6, "route", "weekly"), ("chainladder", 24, "pooled", "daily")):
        G.nowcast(ll, cases, est, m, st, b)
        ok(G.ask_a(cases, adm, births, reg) == A and G.ask_b(cases, rosters) == B,
           "the asks do not move with the nowcast")
    fort = cases[(cases["date"] >= G.FORTNIGHT[0]) & (cases["date"] <= G.LAST_DAY)]
    ok((fort["n_notifications"] == 1).all() and (fort["status"] == "Confirmed").all(),
       "no ask device (repeat notification, probable status) inside the fortnight")

    # ---------------------------------------------------------------- the world behind the extract
    if world is not None:
        truth = {}
        for c in world["cases"]:
            a = W.allocate(c["postcode"]) if c["area"] else None
            if a and G.FORTNIGHT[0] <= c["spec"].date() <= G.LAST_DAY:
                truth[a] = truth.get(a, 0) + 1
        ok(truth[GRIFFITH] >= 4 * N[GRIFFITH], "Griffith's fortnight is several times what has been notified")
        ok(truth[WAGGA] <= 1.3 * N[WAGGA] and truth[SNOWY] <= 1.2 * N[SNOWY], "the hospital-route fortnights are nearly all in")
        LOG.append("world: fortnight cases collected %s; notified %s" % (
            {a: truth.get(a, 0) for a in (GRIFFITH, WAGGA, SNOWY)}, {a: N[a] for a in (GRIFFITH, WAGGA, SNOWY)}))

    # ---------------------------------------------------------------- leak hygiene, every text-bearing file
    prompt = open(os.path.join(TASK, "prompt.md")).read()
    for f in sorted(os.listdir(target)) + ["../prompt.md"]:
        t = prompt if f == "../prompt.md" else file_text(os.path.join(target, f))
        hits = sorted(set(m.group(0).lower() for m in BANNED.finditer(t)))
        ok(not hits, "%s carries %s" % (f, hits))
        ok("\u2014" not in t, "%s carries an em dash" % f)
        if f != "../prompt.md":
            tc = sorted(set(m.group(0) for m in TOOLCHAIN.finditer(t)))
            ok(not tc, "%s carries toolchain or author words %s" % (f, tc))
    for f in os.listdir(golden_dir):
        ok("\u2014" not in file_text(os.path.join(golden_dir, f)), "golden %s carries an em dash" % f)
    notes = open(os.path.join(target, D.NOTES)).read()
    ok(not re.search(r"\b(recent|latest|so far|yet)\b", notes, re.I), "the line-list notes describe fields only")

    # ---------------------------------------------------------------- pack gates
    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    ok(10 <= len(files) <= 13, "file count %d" % len(files))
    ok(len(fmts) >= 5, "formats %s" % fmts)
    big = {f: n for f, n in ((f, rows_of(os.path.join(target, f))) for f in files) if n and n >= 25000}
    ok(len(big) >= 1, "a file of 25,000 rows or more")
    ok(not any(f.startswith(".") for f in files), "no dot files")
    if meta_path and os.path.exists(meta_path):
        meta = json.load(open(meta_path))
        dis = meta["distractor_files"]
        ok(len(dis) == 2 and all(d in files for d in dis), "two distractors named in metadata.json and shipped")
        ok(sorted(x["path"] for x in meta["files"]) == files, "metadata.json lists exactly the shipped files")
        for d in dis:
            tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
            try:
                for f in files:
                    if f != d:
                        shutil.copy(os.path.join(target, f), tmp)
                _, g2 = G.solve(tmp, with_grid=False)
                ok(g2["answer"] == g["answer"] and g2["ask_a"] == A and g2["ask_b"] == B, "the golden reads %s" % d)
            finally:
                shutil.rmtree(tmp)
    ok(sorted(os.listdir(golden_dir)) == ["pertussis_cases_by_lga.csv", "response_team_brief.pptx"], "the two deliverables")

    # ---------------------------------------------------------------- containers and dates
    sig = re.compile(rb"openpyxl|Openpyxl|ReportLab|reportlab|python-pptx|python-docx|matplotlib")
    for f in files + ["../golden/response_team_brief.pptx"]:
        p = os.path.join(target, f)
        if f.endswith((".xlsx", ".pptx")):
            with zipfile.ZipFile(p) as z:
                meta_b = b"".join(z.read(n) for n in z.namelist() if n.startswith("docProps/"))
                stamps = {i.date_time for i in z.infolist()}
            ok(not sig.search(meta_b), "%s carries a writer signature" % f)
            ok(stamps == {(1980, 1, 1, 0, 0, 0)}, "%s zip stamps" % f)
            for m in re.findall(rb"\d{4}-\d\d-\d\dT", meta_b):
                ok(b"2019" <= m[:4] <= b"2026", "%s stamp %s out of band" % (f, m))
        if f.endswith(".pdf"):
            b = open(p, "rb").read()
            ok(not sig.search(b), "%s carries a writer signature" % f)
            ok(all(b"2026" == m[2:6] for m in re.findall(rb"D:\d{14}", b)), "%s dates" % f)
    scrub = os.path.join(REPO, ".claude/skills/reduce-house-fixes/scripts/scrub_producer_metadata.py")
    out = subprocess.run([sys.executable, scrub, target, "--floor", "2019-01-01", "--ceiling", "2026-10-05"],
                         capture_output=True, text=True).stdout
    ok("clean" in out, "producer audit: %s" % out.strip()[:200])
    late = {}
    for f in files:
        if f.endswith((".csv", ".md", ".txt")):
            for m in re.finditer(r"\b(20\d\d-\d\d-\d\d)\b", open(os.path.join(target, f), errors="ignore").read()):
                if m.group(1) > ASOF.isoformat():
                    late.setdefault(f, set()).add(m.group(1))
    ok(not late, "dates after the setting: %s" % late)
    regp = pd.read_parquet(os.path.join(target, "antenatal_vaccinations_2019-2026.parquet"))
    for c in ("mother_dob", "dose_date"):
        ok(pd.to_datetime(regp[c]).max().date() <= ASOF, "register %s after the setting" % c)
    ok(pd.to_datetime(regp["estimated_due_date"]).max().date() > ASOF, "the register holds pregnancies in progress (allow-listed)")

    # ---------------------------------------------------------------- the documents' own figures
    rr = open(os.path.join(target, D.RUN_REPORT)).read()
    llp = os.path.join(target, G.LL)
    ok(hashlib.sha256(open(llp, "rb").read()).hexdigest() in rr, "run report checksum")
    ok(re.search(r"rows\s+%d\b" % len(ll), rr), "run report row count")
    fig = D.bulletin_figures(llp, os.path.join(target, "influenza_notifications_2026.csv"))
    bt = file_text(os.path.join(target, D.BULLETIN))
    ok("received %d pertussis notifications for residents this week and %d in the four weeks" % (
        fig["Pertussis"]["week"], fig["Pertussis"]["four"]) in " ".join(bt.split()), "bulletin summary recomputes")
    ok(max(fig["Influenza"]["weekly"]) > fig["Influenza"]["week"], "influenza has fallen from its peak by week 35")
    ids = list(ll["notification_id"]) + list(pd.read_csv(os.path.join(target, "influenza_notifications_2026.csv"),
                                                         dtype=str)["notification_id"])
    ok(len(ids) == len(set(ids)), "notification numbers unique across both extracts")
    ok(list(ll["notification_id"]) == sorted(ll["notification_id"]), "line list in notification order")
    ok(list(ll.sort_values("received_utc")["notification_id"]) == sorted(ll["notification_id"]),
       "notification numbers follow the order received")

    # ---------------------------------------------------------------- the goldens agree with the solve
    gcsv = list(csv.DictReader(open(os.path.join(golden_dir, "pertussis_cases_by_lga.csv"))))
    ok([r["lga"] for r in gcsv] == G.AREAS, "golden CSV row order")
    for r in gcsv:
        ok(tuple(int(r[c]) for c in ("confirmed_cases", "probable_cases", "infants_under_6_months",
                                     "infants_admitted_to_hospital", "infants_mother_vaccinated_14d_before_birth"))
           == EXPECT_A[r["lga"]], "golden CSV %s" % r["lga"])
    st = file_text(os.path.join(golden_dir, "response_team_brief.pptx"))
    ok("Send the response team to Griffith this week" in st, "slide names the call")
    for name, area, n in EXPECT_B:
        ok(name in st and area in st, "slide lists %s" % name)
    ph, pp = g["route_share"][G.HOSP][0], g["route_share"][G.PRIV][0]
    for x in (ph, pp):
        ok(x == 1.0 or abs((100 * x) % 1 - 0.5) >= 0.2, "route share %.4f sits within 0.3 points of a rounding edge" % x)
    ok("%d%%" % round(100 * pp) in st and "%d%%" % round(100 * ph) in st, "slide carries both route shares")
    ok(not re.search(r"\b(2[0-9]|3[0-9]|4[0-9])\s+(estimated|nowcast)", st), "slide states no nowcast figure")
    people = set(W.PEOPLE.values())
    sys.path.insert(0, os.path.join(REPO, ".claude/skills/fingerprint"))
    try:
        import business
        found = set()
        for f in files + ["../golden/response_team_brief.pptx", "../prompt.md"]:
            p = os.path.join(target, f)
            if f.endswith((".md", ".txt", ".pdf", ".pptx")):
                found |= {"%s %s" % x for x in business.people_in_text(file_text(p))}
        ok(found <= people, "personas outside the card: %s" % (found - people))
        LOG.append("personas in the pack: %s" % ", ".join(sorted(found)))
    except ImportError:
        pass

    sub = os.path.join(TASK, "submission.md")
    if os.path.exists(sub):
        check_submission(open(sub).read(), g, cases)
    if not quiet:
        for line in LOG:
            print("  " + line)
    print("checks: %d assertions passed" % N_ASSERT[0])
    return N_ASSERT[0], LOG, g


def check_submission(text, g, cases):
    """Every figure the write-up states is the solve's own."""
    ok("\u2014" not in text, "submission carries an em dash")
    ok(text.count("## ") == 5 + 2 and "## Tags" in text and "## 4. Deliverable Answers" in text, "five blocks")
    ok("**Send the response team to Griffith this week.**" in text, "the committed call")
    N, E = g["N"], g["E"]
    for a in (WAGGA, GRIFFITH, SNOWY):
        ok("%s **%d**" % (a, N[a]) in text, "component: %s notified" % a)
    ok("**%.1f** for each of Wagga Wagga, Griffith and Snowy Valleys" % E[GRIFFITH] in text
       and E[WAGGA] == E[GRIFFITH] == E[SNOWY], "component: expected counts")
    fort = cases[(cases["date"] >= G.FORTNIGHT[0]) & (cases["date"] <= G.LAST_DAY)]
    n_priv = int(((fort["area"] == GRIFFITH) & (fort["lab"] == G.PRIV)).sum())
    ok("**%d** of Griffith's %d notified cases came through Inland Pathology" % (n_priv, N[GRIFFITH]) in text, "component: route")
    ok((fort[fort["area"].isin([WAGGA, SNOWY])]["lab"] == G.HOSP).all(), "component: hospital route for the other two")
    pp, ph = g["route_share"][G.PRIV][0], g["route_share"][G.HOSP][0]
    ok("Inland Pathology **%d%%**, hospital laboratory **%d%%**" % (round(100 * pp), round(100 * ph)) in text, "component: speeds")
    ok("Inland Pathology notified %d%% within 14 days and the hospital laboratory %d%%" % (round(100 * pp), round(100 * ph)) in text,
       "step 4: speeds")
    ok("Wagga Wagga 9, Griffith 7, Snowy Valleys 7, Cootamundra-Gundagai 2, Edward River, Leeton and Narrandera 1 each" in text
       and N["Cootamundra-Gundagai"] == 2 and N["Edward River"] == N["Leeton"] == N["Narrandera"] == 1
       and N["Hay"] == N["Junee"] == N["Murrumbidgee"] == 0, "step 2: counts")
    for name, area, n in g["ask_b"]:
        ok("   - %s, %s, %d" % (name, area, n) in text, "block 4 cluster %s" % name)
    ok(text.count("   - ") == len(g["ask_b"]) + len(G.AREAS), "block 4 holds every cluster and every area, nothing else")
    for a in G.AREAS:
        r = g["ask_a"][a]
        ok("   - %s: %d, %d, %d, %d, %d" % (a, r["confirmed"], r["probable"], r["infants"], r["admitted"], r["vaccinated"])
           in text, "block 4 %s" % a)


def cases_sex(ll, pid):
    return ll[ll["person_id"] == pid]["sex"].iloc[0]


def rows_of(path):
    if path.endswith(".csv"):
        with open(path) as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".parquet"):
        return len(pd.read_parquet(path))
    return None


if __name__ == "__main__":
    run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), meta_path=os.path.join(TASK, "metadata.json"))
