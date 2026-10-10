"""Generator assertions (dataset-generation 11.7, determinism-check B, supplemental-stumping Part 8).
Each assertion is recorded with its value; a failed one fails the build."""
import datetime as dt
import importlib.util
import json
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

import analysis as AN
import params as P

M = P.M
REPO = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "scrub", REPO / ".claude/skills/reduce-house-fixes/scripts/scrub_producer_metadata.py")
SCRUB = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(SCRUB)

# The main call's declared row population: the files and columns the decisive construction reads.
MAIN_ROWS = {
    "examination_dockets_FY2016_FY2026.parquet": ["docket_no", "docketed_on", "closed_on", "end_code"],
    "docket_links.csv": ["parent_docket", "child_docket", "link_type", "linked_on"],
    "office_actions_FY2016_FY2026.parquet": ["action_id", "docket_no", "action_code", "served_on"],
    "examiner_production_ledger_FY2016_FY2026.parquet": ["action_id", "credit_class"],
    "saravel_ipo_acknowledgements_FY2019-FY2022.xlsx": ["*"],
}
DEVICE_COLUMNS = {("examination_dockets_FY2016_FY2026.parquet", "tg"),
                  ("examination_dockets_FY2016_FY2026.parquet", "art_unit"),
                  ("docket_transfers.csv", "*"), ("art_unit_groups.csv", "*"),
                  ("examiner_roster_2026-09-30.csv", "*"), ("report_table_notes.docx", "*"),
                  ("annual_report_2025_tables_P1_P2.xlsx", "P2")}

# Sensitive phrases and the one file each may appear in (the pins table).
PIN_VOCAB = {
    "continuing": set(),
    "continuation": {"docketing_codebook.md"},
    "re-examination": {"examiner_production_standard_2019.pdf"},
    "same application": set(),
    "new application": set(),
    "credited once": {"examiner_production_standard_2019.pdf"},
    "same file": {"headline_section_thread.eml"},
}


class Rec:
    def __init__(self):
        self.items = []

    def ok(self, name, cond, value=None):
        self.items.append({"name": name, "ok": bool(cond), "value": value})


def pct(a, b):
    return 100.0 * (a / b - 1.0)


def doc_text(path):
    """Plain text of a shipped document, for the vocabulary sweeps."""
    p = Path(path)
    if p.suffix in (".md", ".eml", ".csv"):
        return p.read_text(encoding="utf-8")
    if p.suffix == ".docx" or p.suffix == ".xlsx":
        out = []
        with zipfile.ZipFile(p) as z:
            for n in z.namelist():
                if n.endswith(".xml") and ("word/" in n or "sharedStrings" in n or "worksheets" in n):
                    out.append(re.sub(r"<[^>]+>", " ", z.read(n).decode("utf-8")))
        return " ".join(out)
    if p.suffix == ".pdf":
        from pypdf import PdfReader
        return " ".join(pg.extract_text() for pg in PdfReader(str(p)).pages)
    return ""


def ladder(R, ctx):
    A = ctx["A"]
    rung, r3, r4 = AN.rungs(A)
    h = AN.headline(A, r4)
    g = AN.grid(A, r3, r4)
    ctx.update(rung=rung, r3=r3, r4=r4, h=h, g=g)
    ans = rung["R4"]
    vals = [AN.r1(rung[k]) for k in ("R0", "R1", "R2", "R3", "R4")]
    R.ok("rung figures pairwise distinct by at least 2.0 months",
         min(abs(a - b) for i, a in enumerate(vals) for b in vals[i + 1:]) >= 2.0, vals)
    R.ok("answer median sits at 880 days (28.9 under every day-count convention within one day)",
         h["median_days"] == 880 and {AN.r1(d / M) for d in (879, 880, 881)} == {28.9}, h["median_days"])
    R.ok("every quantile definition files the same headline tenth",
         {AN.r1(v / M) for v in h["median_alts"].values()} == {AN.r1(ans)}, h["median_alts"])
    R.ok("rung 0 at least 15 per cent below the answer", pct(rung["R0"], ans) <= -15, round(pct(rung["R0"], ans), 1))
    R.ok("rung 1 at least 20 per cent below the answer", pct(rung["R1"], ans) <= -20, round(pct(rung["R1"], ans), 1))
    R.ok("rung 2 at least 10 per cent below the answer", pct(rung["R2"], ans) <= -10, round(pct(rung["R2"], ans), 1))
    R.ok("rung 3 at least 12 per cent above the answer", pct(rung["R3"], ans) >= 12, round(pct(rung["R3"], ans), 1))
    R.ok("ladder direction: rung 1 < rung 0 < rung 2 < answer < rung 3",
         rung["R1"] < rung["R0"] < rung["R2"] < ans < rung["R3"], vals)
    R.ok("decisive rung worth at least 10 per cent of the rung-3 figure",
         (rung["R3"] - ans) / rung["R3"] >= 0.10, round((rung["R3"] - ans) / rung["R3"], 3))
    R.ok("undecided share and 36-month share at least 0.01 points from a rounding edge",
         all(abs((v * 10) % 1 - 0.5) >= 0.1 for v in (h["undecided_pct"], h["within36_pct"])),
         (round(h["undecided_pct"], 3), round(h["within36_pct"], 3)))
    R.ok("no FY2022 application finally decided 1,095 or 1,096 days after filing",
         h["dur_hist_1095_1096"] == 0, ctx["W"].hole_moved)
    R.ok("every undecided FY2022 application at least 48 months old at the extract",
         h["min_undecided_age"] >= 1461, h["min_undecided_age"])
    floors = {"chains_grant_end": 6.5, "split_grant_end": 6.5, "left_out": 6.5,
              "parents_chained_cont_added": 6.5, "benefit_dated": 6.5, "decided_only": 6.5,
              "family_chain": 6.5, "any_docket_cohort": 6.5}
    for k, f in floors.items():
        R.ok("grid cell %s at least %.1f per cent from the answer" % (k, f), abs(pct(g[k], ans)) >= f,
             (round(g[k], 2), round(pct(g[k], ans), 1)))
    for k in ("parent_at_close", "plain_median_undecided_at_extract"):
        R.ok("grid cell %s converges on the answer" % k, AN.r1(g[k]) == AN.r1(ans), round(g[k], 3))
    R.ok("calendar-year 2022 cohort converges or sits at least 6 per cent off",
         AN.r1(g["calendar_year_2022"]) == AN.r1(ans) or abs(pct(g["calendar_year_2022"], ans)) >= 6,
         round(g["calendar_year_2022"], 3))
    # lens swap: rung 3 and the answer are different populations
    s3, s4 = set(map(int, r3)), set(map(int, r4))
    R.ok("lens swap: the answer's population differs from rung 3's in membership",
         len(s4 - s3) > 5000 and len(s3 - s4) == 0, (len(s3), len(s4), len(s4 - s3)))


def corpus(R, ctx):
    A, C, q = ctx["A"], ctx["C"], ctx["quarters"]
    X = P.EXTRACT
    dec = C["e3"] <= X
    R.ok("corpus blind to the split: rungs 3 and 4 agree case by case", bool((C["e3"] == C["e4"]).all()),
         int(len(C["cases"])))
    R.ok("corpus blind to the split: no successor in a programme chain is a continuing application",
         C["n1n"] == 0, C["n1n"])
    R.ok("rung 3 reproduces every acknowledged decision (decided cases)", int(dec.sum()) > 4000, int(dec.sum()))
    W = ctx["W"]
    nfa = []
    for k, i in enumerate(C["cases"]):
        j = int(i)
        while W.child[j] >= 0:
            j = int(W.child[j])
            if W.fa[j] > P.EXTRACT:
                nfa.append(k)
    nfa = np.array(nfa, dtype=np.int64)
    R.ok("corpus: every file whose successor has no first action at the extract is waiting on the answer's rule "
         "(the split is made only on a positive 1N), and there are 4 of them",
         len(nfa) == 4 and bool((C["e4"][nfa] > X).all()), int(len(nfa)))
    alw = dec & (C["dtype"] == "A") & ~C["reex"] & (C["r0"] < AN.BIG)
    lag = (C["r0"] - C["e3"])[alw]
    R.ok("rung 0 misses every allowed single-docket case by the grant lag (97 to 180 days late)",
         bool(((lag >= 97) & (lag <= 184)).all()) and int(alw.sum()) > 1000, (int(alw.sum()), int(lag.min()), int(lag.max())))
    rx = dec & C["reex"]
    R.ok("rung 1 misses every decided re-examined case (ends at the first refusal, early)",
         bool((C["r1"][rx] < C["e3"][rx]).all()) and int(rx.sum()) > 1000, int(rx.sum()))
    R.ok("rung 2 leaves every decided re-examined case undecided", bool((C["r2"][rx] >= AN.BIG).all()), int(rx.sum()))
    single = dec & ~C["reex"]
    R.ok("rung 1 reproduces every decided single-docket case", bool((C["r1"][single] == C["e3"][single]).all()),
         int(single.sum()))
    q1 = AN.corpus_quarters(A, C, C["r1"])
    q2 = AN.corpus_quarters(A, C, C["r2"])
    q0 = AN.corpus_quarters(A, C, C["r0"])
    qd = AN.corpus_quarters(A, C, np.where(dec, C["e3"], -1))
    R.ok("16 filing quarters in the partner's medians", len(q) == 16, sorted(q))
    R.ok("rung 1 below the partner's median on all 16 quarters", all(q1[k] < q[k] for k in q),
         sum(q1[k] < q[k] for k in q))
    R.ok("rung 2 off the partner's median on all 16 quarters", all(q2[k] != q[k] for k in q),
         sum(q2[k] > q[k] for k in q))
    R.ok("rung 0 off the partner's median on all 16 quarters", all(q0[k] != q[k] for k in q),
         sum(q0[k] > q[k] for k in q))
    fy22q = [k for k in q if k >= "2021-Q4"]
    # decided only: drop the open cases instead of counting them as waiting
    qdo = {}
    for k in q:
        lab = np.array([AN.quarter_label(s) for s in A.start[C["cases"]]])
        a = (lab == k) & dec
        qdo[k] = AN.partner_median((C["e3"] - A.start[C["cases"]])[a])
    R.ok("decided-only medians miss at least three FY2022 quarters", sum(qdo[k] != q[k] for k in fy22q) >= 3,
         {k: (qdo[k], q[k]) for k in fy22q})
    ctx["corpus_q"] = dict(partner=q, r0=q0, r1=q1, r2=q2, decided_only=qdo)


def classification(R, ctx):
    W, T = ctx["W"], ctx["T"]
    acts = T.acts
    first = {}
    cls_by_docket = defaultdict(list)
    for a in acts:
        if a[2] == "EXR" and a[0] not in first:
            first[a[0]] = a
        if a[4] in ("1N", "1R"):
            cls_by_docket[a[0]].append(a)
    R.ok("every first action on the merits carries exactly one 1N or 1R credit, and no other action does",
         all(len(cls_by_docket[i]) == 1 and cls_by_docket[i][0] is first[i] for i in first)
         and set(cls_by_docket) == set(first), len(first))
    bad = sum(1 for i, a in first.items() if W.kind[i] != 1 and a[4] != "1N")
    R.ok("every first docket and every CN or DV child is credited 1N", bad == 0, bad)
    bad = sum(1 for i, a in first.items() if W.kind[i] == 1 and a[4] != ("1N" if W.route[i] == 2 else "1R"))
    R.ok("every CX successor is credited 1N (continuing) or 1R (re-examination) by its route", bad == 0, bad)
    bad = sum(1 for i, a in first.items() if W.prog[i] and a[4] == "1N" and W.kind[i] == 1)
    R.ok("no programme successor is credited 1N", bad == 0, bad)
    shares = {}
    for i in T.ship:
        if W.kind[i] == 1:
            fy = P.fy_of(W.start[i])
            s = shares.setdefault(fy, [0, 0])
            s[0] += W.route[i] == 2
            s[1] += 1
    sh = {fy: round(a / b, 4) for fy, (a, b) in shares.items()}
    R.ok("continuing share of CX successors between 0.24 and 0.30 in every docketing year FY2017 to FY2026",
         all(0.24 <= sh[fy] <= 0.30 for fy in range(2017, 2027)), sh)
    ctx["cont_share"] = sh
    # no visible tell between the routes on any docket, action or link column
    g1 = [first[i][1] - W.start[i] for i in first if W.kind[i] == 1 and W.route[i] == 1 and not W.twin[i]
          and not W.prog[i]]
    g2 = [first[i][1] - W.start[i] for i in first if W.kind[i] == 1 and W.route[i] == 2 and not W.twin[i]]
    p_t = stats.ks_2samp(g1, g2).pvalue
    R.ok("successor first-action timing indistinguishable across 1N and 1R (KS p above 0.05)", p_t > 0.05, round(p_t, 3))
    d1 = [W.dec[i] - W.start[i] for i in T.ship if W.kind[i] == 1 and W.route[i] == 1 and W.status[i] in
          ("ALW", "REF", "ABN", "CX") and not W.prog[i] and not W.twin[i]]
    d2 = [W.dec[i] - W.start[i] for i in T.ship if W.kind[i] == 1 and W.route[i] == 2 and W.status[i] in
          ("ALW", "REF", "ABN", "CX") and not W.twin[i]]
    p_d = stats.ks_2samp(d1, d2).pvalue
    R.ok("successor decision timing indistinguishable across 1N and 1R (KS p above 0.05)", p_d > 0.05, round(p_d, 3))
    o1 = Counter(W.status[i] for i in T.ship if W.kind[i] == 1 and W.route[i] == 1 and not W.prog[i])
    o2 = Counter(W.status[i] for i in T.ship if W.kind[i] == 1 and W.route[i] == 2)
    keys = [k for k in ["ALW", "REF", "ABN", "CX", ""] if o1[k] + o2[k] > 0]
    p_o = stats.chi2_contingency([[o1[k] for k in keys], [o2[k] for k in keys]])[1]
    R.ok("successor end-code mix indistinguishable across 1N and 1R (chi-square p above 0.05)", p_o > 0.05,
         round(p_o, 3))
    same_ex = [W.ex_dock[i] == W.ex_close[W.parent[i]] for i in T.ship if W.kind[i] == 1]
    R.ok("every CX successor is docketed to the examiner holding the refused docket", all(same_ex), len(same_ex))
    ctx["tell_p"] = dict(timing=p_t, decision=p_d, endcodes=p_o)


def twins(R, ctx):
    W, T = ctx["W"], ctx["T"]
    tw = {r: [i for i in range(W.n()) if W.twin[i] == r] for r in (1, 2)}
    drow = {r["docket_no"]: r for r in ctx["drows"]}

    def strip(i):
        d = dict(drow[T.no[i]])
        d.pop("docket_no")
        return d
    acts = defaultdict(list)
    for a in T.acts:
        if W.twin[a[0]]:
            acts[a[0]].append((a[1], a[2], a[3]))
    same = all(strip(a) == strip(b) and acts[a] == acts[b] for a, b in zip(tw[1], tw[2]))
    root = tw[1][0]
    d_reex = (W.dec[tw[1][1]] - W.start[root]) / M
    d_cont = (W.dec[tw[2][0]] - W.start[tw[2][0]]) / M
    cls = [a[4] for a in T.acts if a[0] in (tw[1][1], tw[2][1]) and a[4] in ("1N", "1R")]
    R.ok("twin pair identical on every docket, action and link column; 29.3 against 14.5 months; only the "
         "credit class differs", same and AN.r1(d_reex) == 29.3 and AN.r1(d_cont) == 14.5 and sorted(cls) == ["1N", "1R"],
         (round(d_reex, 2), round(d_cont, 2), [T.no[i] for i in tw[1] + tw[2]]))
    ctx["twins"] = {r: [T.no[i] for i in tw[r]] for r in tw}


def context_tables(R, ctx):
    A, p1, p2 = ctx["A"], ctx["p1"], ctx["p2"]
    rep = [fy for fy, r in p1.items() if r["reported"]]
    R.ok("P1 reports FY2006 onwards and never a year under 98 per cent closed, never FY2022",
         min(rep) == 2006 and 2022 not in rep and all(p1[fy]["closed_share"] >= 0.98 for fy in rep), rep)
    rec = {fy: AN.r1(p1[fy]["med26"]) for fy in rep if fy >= P.SHIP_FROM_FY}
    R.ok("P1 reproduces from the 2026 extract to the tenth for every year the extract covers",
         all(rec[fy] == p1[fy]["published"] for fy in rec) and len(rec) >= 4,
         {fy: (rec[fy], p1[fy]["published"]) for fy in rec})
    tg = Counter((r["tg"], P.fy_of(dt.date.fromisoformat(r["docketed_on"]).toordinal())) for r in ctx["drows"])
    R.ok("P2 ties exactly to a count of the docket table's tg column (the false clean)",
         all(p2[k] == tg[k] for k in p2), sum(p2.values()))
    cnt = [p1[fy]["n"] for fy in sorted(p1)]
    R.ok("P1 docket counts carry no burn-in ramp (each year within 12 per cent of the next)",
         all(abs(a / b - 1) < 0.12 for a, b in zip(cnt, cnt[1:])), cnt)


def asks(R, ctx):
    A = ctx["A"]
    res, conv, _ = AN.ask_cells(A, ctx["r3"], ctx["r4"])
    ans = AN.rounded(res["answer"])

    def moved(k):
        v = AN.rounded(res[k])
        return sum(1 for g in P.GROUPS for z in range(3) if v[g][z] != ans[g][z])
    mv = {k: moved(k) for k in res if k != "answer"}
    ctx["ask_cells"] = {k: AN.rounded(v) for k, v in res.items()}
    ctx["ask_moved"] = mv
    R.ok("every answer cell converges across six quantile definitions",
         all(len(x) == 1 for v in conv.values() for x in v), [g for g, v in conv.items() if any(len(x) > 1 for x in v)])
    divs = (P.M, 30.44, 30.437, 30.438)
    R.ok("every answer month cell files the same tenth under the charter divisor however it is rounded",
         all(len({AN.r1(x * P.M / d) for d in divs}) == 1 for v in res["answer"].values() for x in v[:2]),
         [(g, [round(x, 4) for x in v[:2]]) for g, v in res["answer"].items()])
    R.ok("every answer share cell at least 0.005 points from a rounding edge",
         all(abs((v[2] * 10) % 1 - 0.5) >= 0.05 for v in res["answer"].values()),
         [(g, round(v[2], 4)) for g, v in res["answer"].items()])
    R.ok("S1 (tg column) and S2 (as-of join on the docketing art unit) file identical cells (false clean)",
         AN.rounded(res["S1_tg_column"]) == AN.rounded(res["S2_asof_docketing_au"]), mv["S1_tg_column"])
    R.ok("lazy path S1 moves at least 20 of 24 cells", mv["S1_tg_column"] >= 20, mv["S1_tg_column"])
    R.ok("hazard alone (current group of the art unit at close) moves at least 16 of 24 cells",
         mv["S3_current_group_art_unit_column"] >= 16, mv["S3_current_group_art_unit_column"])
    R.ok("both devices mishandled (as-of join on the art unit column) moves at least 16 of 24 cells",
         mv["S2b_asof_art_unit_column"] >= 16, mv["S2b_asof_art_unit_column"])
    R.ok("over-corrected stop (roster home art unit) moves at least 16 of 24 cells",
         mv["S4_roster_home_au"] >= 16, mv["S4_roster_home_au"])
    R.ok("construction layer: rung-3 applications move at least 20 of 24 cells", mv["rung3_answer_groups"] >= 20,
         mv["rung3_answer_groups"])
    # decoupling: no stop moves the headline or the undecided share (they never read a group column)
    h = ctx["h"]
    R.ok("separation: the main call's declared rows carry no device or hazard column",
         not any((f, c) in DEVICE_COLUMNS or (f, "*") in DEVICE_COLUMNS for f, cs in MAIN_ROWS.items() for c in cs)
         and h["n"] == sum(v[3] for v in res["answer"].values()), h["n"])


def gates(R, ctx):
    tgt, meta = ctx["tgt"], ctx["meta"]
    names = sorted(p.name for p in tgt.iterdir())
    R.ok("input gate: 10 or more files", len(names) >= 10, len(names))
    fmts = {Path(n).suffix for n in names}
    R.ok("input gate: 3 or more formats", len(fmts) >= 3, sorted(fmts))
    R.ok("input gate: a file of 25,000 or more rows", meta["input_gates"]["largest_file_rows"] >= 25000,
         meta["input_gates"]["largest_file_rows"])
    R.ok("input gate: two distractors named in metadata.json, shipped, and named nowhere in target/",
         len(meta["distractor_files"]) >= 2 and all(d in names for d in meta["distractor_files"])
         and not any("distractor" in n.lower() for n in names), meta["distractor_files"])
    R.ok("1 to 3 deliverables", 1 <= len(meta["deliverables"]) <= 3, meta["deliverables"])
    R.ok("extract notes list exactly the shipped files (manifest set equality)",
         set(re.findall(r"^\| ([^ |]+\.[a-z]+) \|", (tgt / "extract_notes.md").read_text(), re.M))
         == set(names) - {"extract_notes.md"}, len(names))
    texts = {n: doc_text(tgt / n) for n in names if Path(n).suffix in (".md", ".eml", ".pdf", ".docx", ".xlsx")
             and n != "saravel_ipo_acknowledgements_FY2019-FY2022.xlsx"}
    texts["examiner_roster_2026-09-30.csv"] = ""
    bad = []
    for phrase, allowed in PIN_VOCAB.items():
        hits = {n for n, t in texts.items() if phrase in t.lower()}
        if not hits <= allowed or (allowed and not hits):
            bad.append((phrase, sorted(hits)))
    R.ok("pin vocabulary: each sensitive phrase only in the one file the pins table names", not bad, bad)
    named = [(n, m) for n, t in texts.items() for m in names
             if m in t and n not in ("extract_notes.md", "docketing_codebook.md") and m != n]
    R.ok("no input file named in any document beside the codebook and the extract notes", not named, named)
    for n in texts:
        texts[n] = texts[n]
    R.ok("no em dash in any shipped text", not any("\u2014" in t for t in texts.values()), None)
    # generation tells
    rows = [r for r in ctx["rows"].values() if r]
    R.ok("no uniform row counts across the data files", len(set(rows)) == len(rows), sorted(rows))
    # distractor answer exclusion
    import workbooks as WB
    vals = {v for row in WB.INTERNATIONAL for v in row[2:4]}
    rv = {AN.r1(ctx["rung"][k]) for k in ctx["rung"]}
    R.ok("the international comparison files no rung figure", not (vals & rv), sorted(vals))
    # dates: nothing in an extract file after the extract; no document after the as-of date
    mx = max(max(r["docketed_on"] for r in ctx["drows"]), max(r["closed_on"] for r in ctx["drows"]),
             max(ctx["arows"]["served_on"]), max(r["linked_on"] for r in ctx["links"]),
             max(r["transferred_on"] for r in ctx["xf"]))
    R.ok("no extract date after 30 September 2026", mx <= "2026-09-30", mx)
    import os
    mt = max(os.stat(tgt / n).st_mtime for n in names)
    R.ok("every file time on or before the as-of date and after 2018",
         dt.datetime.fromtimestamp(mt).date() <= P.AS_OF and min(os.stat(tgt / n).st_mtime for n in names)
         >= dt.datetime(2018, 1, 1).timestamp(), None)
    issues = []
    for n in names:
        if Path(n).suffix in (".docx", ".xlsx", ".pdf"):
            meta_ = SCRUB.read_meta(str(tgt / n)) if hasattr(SCRUB, "read_meta") else {}
            blob = json.dumps(meta_, default=str).lower()
            for tok in ("python-docx", "openpyxl", "xlsxwriter", "reportlab", "matplotlib"):
                if tok in blob:
                    issues.append((n, tok))
            for y in re.findall(r"(20\d\d)-\d\d-\d\d", blob):
                if not 2018 <= int(y) <= 2026:
                    issues.append((n, y))
    R.ok("producer metadata scrubbed and container dates in band on every binary", not issues, issues)


def run(ctx):
    R = Rec()
    for f in (ladder, corpus, classification, twins, context_tables, asks, gates):
        f(R, ctx)
    failed = [i["name"] + " :: " + str(i["value"]) for i in R.items if not i["ok"]]
    h = ctx["h"]
    record = {
        "assertions": R.items,
        "rungs": {k: round(v, 3) for k, v in ctx["rung"].items()},
        "headline": {k: (round(v, 4) if isinstance(v, float) else v) for k, v in h.items()},
        "grid": {k: round(v, 3) for k, v in ctx["g"].items()},
        "ask_cells": ctx.get("ask_cells"), "ask_moved": ctx.get("ask_moved"),
        "corpus": {"cases": int(len(ctx["C"]["cases"])), "decided": int((ctx["C"]["e3"] <= P.EXTRACT).sum()),
                   "reexamined": int(ctx["C"]["reex"].sum())},
        "corpus_quarters": ctx.get("corpus_q"), "cont_share": ctx.get("cont_share"), "tell_p": ctx.get("tell_p"),
        "twins": ctx.get("twins"), "rows": ctx["rows"],
        "counts": {"fy22_dockets": int(ctx["A"].infy.sum()), "rung3_apps": int(len(ctx["r3"])),
                   "answer_apps": int(len(ctx["r4"])),
                   "fy22_cx_successors": int((ctx["A"].infy & (ctx["A"].kind == 1)).sum()),
                   "fy22_continuing": int((ctx["A"].infy & (ctx["A"].route == 2)).sum())},
        "p1": {fy: (r["n"], round(r["closed_share"], 4), r["published"]) for fy, r in ctx["p1"].items()},
    }
    return record, failed
