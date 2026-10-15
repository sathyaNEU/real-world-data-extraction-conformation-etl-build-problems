"""task141 checks, run on every build: the three-rules block (R1 to R3c) on the clean truth and the pack, every rung
by name with its margins and the fork grid, every semantic fork row (SF1 to SF29), mess neutrality, the asks against
the clean truth with every stop and each figure's distance to its bin edge, the separation line, the distractors, the
input gates, the realism sweep and the containers. Any failure stops the build."""
from __future__ import annotations

import builtins
import datetime as dt
import glob
import io
import json
import math
import os
import re
import zipfile

import numpy as np
import pandas as pd

import calc as CA
import common as K
import truth as TR

GOLDEN = "R3 leniency gradient (golden)"
LENIENCY = [GOLDEN, "V ols", "V leave-out instrument", "V halves", "V quadratic", "V released-rate line",
            "V instrument, all scores", "V lenient fifth"]
RELEASED_FAMILY = ["R0 released defendants' rate", "R0b latest closed year", "R1 logistic on the released",
                   "R1b reweighted to the eligible"]
DAY = dt.timedelta(days=1)


class Checks:
    def __init__(self):
        self.res = []

    def __call__(self, label, ok, detail=""):
        self.res.append((label, bool(ok), detail))
        return ok

    def report(self):
        bad = [r for r in self.res if not r[1]]
        for lab, ok, det in self.res:
            if not ok:
                print("FAIL %s %s" % (lab, det))
        print("checks.py: %d assertions, %d failed" % (len(self.res), len(bad)))
        if bad:
            raise SystemExit(1)


def r10(x):
    return K.round_to(x, 10)


def edge(x, step):
    """Distance from a rounding edge as a share of the bin (0 on an edge, 0.5 mid-bin)."""
    q = x / step
    return abs(q - math.floor(q) - 0.5)


def tier(v):
    return CA.tier(v)


class Reads:
    """Record which pack files a computation opens."""

    def __init__(self, target):
        self.target = os.path.abspath(target)
        self.seen = set()

    def __enter__(self):
        self.orig = builtins.open
        self.orig_csv = pd.read_csv
        self.orig_xl = pd.read_excel
        import openpyxl
        self.orig_wb = openpyxl.load_workbook
        me = self

        def note(p):
            try:
                p = os.path.abspath(p)
                if p.startswith(me.target):
                    me.seen.add(os.path.basename(p))
            except TypeError:
                pass

        def o(p, *a, **k):
            note(p)
            return me.orig(p, *a, **k)

        def rc(p, *a, **k):
            note(p)
            return me.orig_csv(p, *a, **k)

        def rx(p, *a, **k):
            note(p)
            return me.orig_xl(p, *a, **k)

        def wb(p, *a, **k):
            note(p)
            return me.orig_wb(p, *a, **k)
        builtins.open, pd.read_csv, pd.read_excel, openpyxl.load_workbook = o, rc, rx, wb
        CA.openpyxl.load_workbook = wb
        return self

    def __exit__(self, *a):
        import openpyxl
        builtins.open, pd.read_csv, pd.read_excel, openpyxl.load_workbook = (self.orig, self.orig_csv, self.orig_xl,
                                                                             self.orig_wb)
        CA.openpyxl.load_workbook = self.orig_wb


# ---------------------------------------------------------------------------------------------------- helpers
def released_by_condition(fa):
    f = fa.copy()
    f["released24"] = f.cond.isin(["WRITTEN_PROMISE", "UNSECURED_BOND", "CUSTODY_RELEASE"]) & f.rel_t.notna()
    return f


def released_within(fa, hours):
    f = fa.copy()
    f["released24"] = f.rel_type.isin(CA.RELEASES) & (f.rel_t <= f.fa_t + pd.Timedelta(hours=hours))
    return f


def route(name, h):
    if name == "R0":
        return CA.safety(CA.naive(h))
    if name == "R0c":
        return CA.safety(CA.held_as_safe(h))
    if name == "R1":
        return CA.safety(CA.logistic_on_released(CA.add_features(h)))
    if name == "R3":
        return CA.safety(CA.leniency_wls(h))
    raise KeyError(name)


def last_year(h):
    return h[h.fa_t.dt.date >= K.HIST_LAST - dt.timedelta(days=364)]


def text_of(path):
    if path.endswith(".pdf"):
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            return "\n".join(p.extract_text() or "" for p in pdf.pages)
    if path.endswith(".docx"):
        import docx
        d = docx.Document(path)
        parts = [p.text for p in d.paragraphs]
        for t in d.tables:
            for r in t.rows:
                parts.extend(c.text for c in r.cells)
        return "\n".join(parts)
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, data_only=True)
        out = []
        for ws in wb.worksheets:
            for row in ws.iter_rows(values_only=True):
                out.append(" ".join("" if v is None else str(v) for v in row))
        return "\n".join(out)
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


# ---------------------------------------------------------------------------------------------------- the run
def run(target, golden, W=None, meta_path=None):
    import world as WD
    ck = Checks()
    if W is None:
        W = WD.simulate()
    with Reads(target) as rd:
        fa, h = CA.everything(target)
        L = CA.ladder(fa, h)
    call_reads = set(rd.seen)
    g = L[GOLDEN]
    files = sorted(os.listdir(target))
    meta = json.load(open(meta_path)) if meta_path else {}

    # ------------------------------------------------------------------ the three rules
    st = TR.safety_truth(W)
    sel = TR.selection_by_score(W)
    # R3a: the easy route on the clean truth, every filed rule applied: the released defendants' own outcomes
    hist = TR.history_eps(W)
    offs = {}
    for a in W.arrests:
        if a["type"] == "NEW":
            offs.setdefault(a["pid"], []).append(a["offence_date"])
    naive_truth = {}
    for s in range(1, 7):
        rel = [e for e in hist if e["nca"] == s and e["released24"]]
        y = [any(e["rel_t"].date() < o <= min(e["rel_t"].date() + dt.timedelta(days=365), e["last_disp"])
                 for o in offs.get(e["pid"], [])) for e in rel]
        naive_truth[s] = 1 - sum(y) / len(y)
    ck("R3a analyst test: the released defendants' rate on the clean truth files scores 1 to 4",
       tier(naive_truth) == 4 and naive_truth[4] >= 0.865, naive_truth)
    ck("R3b decisive step alone: every eligible defendant's outcome on the clean truth files scores 1 to 3",
       tier(st) == 3 and st[4] <= 0.78 and st[3] >= 0.88, st)
    ck("R3b on the pack: the leniency gradient files scores 1 to 3", tier(g) == 3, {s: round(v, 4) for s, v in g.items()})
    for k in ("R0b latest closed year", "R0c held as not arrested", "R1 logistic on the released",
              "R1b reweighted to the eligible", "R2 held as arrested"):
        ck("R3b single correction %s stays off the golden" % k, tier(L[k]) != 3, tier(L[k]))
    ck("R3 the trait the magistrate sees: score 4's held defendants carry it, the released far less",
       sel[4][0] >= 0.25 and sel[4][1] <= 0.10, sel[4])
    # R1: the raw material ships; no column holds a release share, a safety rate or a full-release rate
    banned = re.compile(r"(safety|risk|release_share|share|rate_|_rate$|propensity|leniency|expected)", re.I)
    cols = []
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                cols += [(f, c) for c in fh.readline().strip().split(",")]
    bad = [fc for fc in cols if banned.search(fc[1]) and fc[1] != "daily_rate"]
    ck("R1 no shipped column holds a rate, share or risk", not bad, bad)
    mt = CA.mag_table(h, 4)
    ck("R1 the gradient reads row-level appearances: 25 or more magistrates with 100 or more score-4 appearances",
       (mt.n >= 100).sum() >= 25, int((mt.n >= 100).sum()))
    # R3c: no plant; no shipped text states a per-score rate
    texts = {f: text_of(os.path.join(target, f)) for f in files
             if not f.endswith(".csv") or os.path.getsize(os.path.join(target, f)) < 20000}
    found = []
    for s in range(1, 7):
        for v in (g[s], L["R0 released defendants' rate"][s]):
            x = "%.1f" % K.round1(100 * v)
            for f, t in texts.items():
                if re.search(r"(?<![\d.])%s ?(%%|percent|per cent)" % re.escape(x), t):
                    found.append((f, x))
    ck("R3c no shipped document states a per-score safety rate", not found, found)

    # repeated-block sweep (copied or backfilled blocks) on every CSV: no five consecutive rows repeat elsewhere
    reps = []
    for f in files:
        if not f.endswith(".csv"):
            continue
        with open(os.path.join(target, f), encoding="utf-8") as fh:
            lines = fh.read().splitlines()[1:]
        body = [",".join(x.split(",")[1:]) for x in lines]
        seen = {}
        for i in range(len(body) - 5):
            key = hash(tuple(body[i:i + 5]))
            if key in seen and seen[key] != i:
                reps.append((f, seen[key], i))
                break
            seen.setdefault(key, i)
    ck("R3c no block of five rows repeats in any extract", not reps, reps[:3])

    # R2: each mess item mishandled leaves the call and the components' shared bounds where they were
    def holds(v):
        return tier(v) == 3 and v[4] < 0.85 and v[3] >= 0.85
    h_new = h[h.fa_t.dt.date >= K.CMS_CHANGE]
    ck("R2 the legacy export left out (the new system's appearances only): same call", holds(route("R3", h_new)),
       route("R3", h_new))
    fa_u = fa.copy()
    jl = pd.read_csv(os.path.join(target, K.JAIL), dtype=str, keep_default_na=False)
    jn = jl[jl.booking_type == "NEW"].set_index("booking_number")
    ru = fa_u.booking.map(jn.released_utc)
    fa_u["rel_t"] = pd.to_datetime(ru.where(ru != "", None), format="%Y-%m-%dT%H:%M:%SZ")
    fa_u["released24"] = fa_u.rel_type.isin(CA.RELEASES) & (fa_u.rel_t <= fa_u.fa_t + pd.Timedelta(hours=24))
    h_u = CA.history(CA.attach_outcomes(target, fa_u))
    ck("R2 the jail's UTC times read as Eastern: same call", holds(route("R3", h_u)), route("R3", h_u))
    sc = pd.read_csv(os.path.join(target, K.SCREENS), dtype=str, keep_default_na=False)
    h_p = h[h.booking.isin(set(sc.booking_number))]
    ck("R2 paper screens exist in the history (no booking number)", len(h_p) < len(h), (len(h_p), len(h)))
    ck("R2 the paper screens left unmatched: same call", holds(route("R3", h_p)), route("R3", h_p))
    ar = pd.read_csv(os.path.join(target, K.ARRESTS), dtype=str, keep_default_na=False)
    ck("R2 the arrest extract's one row per charge: an arrest counted once or per row, same outcome (binary)",
       ar.arrest_id.duplicated().sum() > 0, int(ar.arrest_id.duplicated().sum()))
    # every arrest type counted (orders for arrest, warrants for earlier offences), by arrest date, same window
    ar2 = ar.drop_duplicates(["arrest_id"]).copy()
    ar2["d"] = pd.to_datetime(ar2.arrest_date).dt.date
    anyarr = ar2.groupby("sid").d.apply(lambda s: sorted(s))
    cases_ = pd.read_csv(os.path.join(target, K.CASES), dtype=str, keep_default_na=False)
    disp_ = dict(zip(cases_.case_number, cases_.disposition_date))
    yy = []
    for r in h.itertuples():
        if not r.released24:
            yy.append(np.nan)
            continue
        a = r.rel_t.date()
        e = a + dt.timedelta(days=365)
        ds = [disp_.get(c, "") for c in r.cases]
        if all(ds):
            e = min(e, max(dt.date.fromisoformat(x) for x in ds))
        yy.append(float(any(a < o <= e for o in anyarr.get(r.sid, []))))
    h_w = h.copy()
    h_w["y"] = yy
    h_w["A"] = np.where(h_w.released24, h_w.y.fillna(0.0), 0.0)
    t_w = tier(route("R3", h_w))
    ck("SF6 every arrest type counted moves the gradient's tier (ruled out by draft 2.4)", t_w != 3, t_w)
    ck("SF6 the arrest types: orders for arrest and warrants are in the extract beside new-offense arrests",
       {"NEW", "OFA", "WARRANT"} <= set(ar.arrest_type))
    h_m = h.copy()
    roster = pd.read_excel(os.path.join(target, K.ROSTER), sheet_name="Magistrates", header=4, dtype=str)
    emp2ini = dict(zip(roster["Employee no."], roster["Initials (legacy)"]))
    h_m["mag"] = np.where(h_m.fa_t.dt.date < K.CMS_CHANGE, "L-" + h_m.mag.map(emp2ini), h_m.mag)
    ck("SF12 the legacy and new keys as separate magistrates: same call", holds(route("R3", h_m)), route("R3", h_m))

    # ------------------------------------------------------------------ the ladder by name
    expect = {"R0 released defendants' rate": 4, "R0b latest closed year": 4, "R1 logistic on the released": 4,
              "R1b reweighted to the eligible": 4, "R2 held as arrested": 2}
    for k, v in expect.items():
        ck("ladder %s files scores 1 to %d" % (k, v), tier(L[k]) == v, tier(L[k]))
    ck("ladder R0c held as not arrested files a tier above scores 1 to 3", tier(L["R0c held as not arrested"]) >= 4,
       tier(L["R0c held as not arrested"]))
    for k in LENIENCY:
        ck("ladder %s files scores 1 to 3" % k, tier(L[k]) == 3, tier(L[k]))
        ck("margin %s: score 4 at least 4 points under the floor" % k, L[k][4] <= 0.81, round(L[k][4], 4))
        ck("margin %s: score 3 at least 3.5 points over the floor" % k, L[k][3] >= 0.885, round(L[k][3], 4))
    for k in RELEASED_FAMILY:
        ck("margin %s: score 4 at least 2.5 points over the floor" % k, L[k][4] >= 0.875, round(L[k][4], 4))
        ck("margin %s: score 5 under the floor" % k, L[k][5] < 0.85, round(L[k][5], 4))
    ck("anchor: the gradient's score 4 within 4.5 points of the clean truth", abs(g[4] - st[4]) <= 0.045,
       (round(g[4], 4), round(st[4], 4)))
    mt4 = CA.mag_table(h, 4)
    X4 = np.c_[np.ones(len(mt4)), mt4.R.values]
    w4 = np.sqrt(mt4.n.values)
    slope4 = float(np.linalg.lstsq(X4 * w4[:, None], mt4.A.values * w4, rcond=None)[0][1])
    rel4 = 1 - L["R0 released defendants' rate"][4]
    ck("the gradient at score 4: the line's slope is three times or more the released defendants' new-offense rate",
       slope4 >= 3 * rel4, (round(slope4, 3), round(rel4, 3)))
    shared = [k for k in LENIENCY if k != "V lenient fifth"]
    ck("shared bound: score 4 under 80 per cent on every construction of the gradient",
       all(L[k][4] < 0.80 for k in shared), {k: round(L[k][4], 4) for k in shared})
    ck("shared rounding: score 3 at 90 per cent to the nearest 5 on every construction of the gradient",
       all(K.round_to(100 * L[k][3], 5) == 90 for k in shared), {k: round(L[k][3], 4) for k in shared})
    ck("anchor: the gradient's score 3 within 1.5 points of the clean truth", abs(g[3] - st[3]) <= 0.015,
       (round(g[3], 4), round(st[3], 4)))
    # the fork grid: route x release definition x window x history, 32 cells
    fas = {("24h", "last"): fa, ("24h", "first"): CA.attach_outcomes(target, fa, cap="first"),
           ("cond", "last"): CA.attach_outcomes(target, released_by_condition(fa)),
           ("cond", "first"): CA.attach_outcomes(target, released_by_condition(fa), cap="first")}
    cells = {}
    for (rdef, win), f in fas.items():
        hh = CA.history(f)
        for hist_name, hx in (("four years", hh), ("last year", last_year(hh))):
            for rt in ("R0", "R0c", "R1", "R3"):
                cells[(rt, rdef, win, hist_name)] = tier(route(rt, hx))
    gold_cells = [k for k, v in cells.items() if v == 3]
    ck("grid: every R3 cell files scores 1 to 3", all(cells[k] == 3 for k in cells if k[0] == "R3"),
       {k: v for k, v in cells.items() if k[0] == "R3"})
    ck("grid: no other route's cell files scores 1 to 3", all(k[0] == "R3" for k in gold_cells), gold_cells)

    # ------------------------------------------------------------------ the semantic fork table
    ck("SF1 highest score with every lower meeting = highest meeting on its own, every leniency route",
       all(max([s for s in range(1, 7) if L[k][s] >= K.FLOOR]) == tier(L[k]) for k in LENIENCY))
    hf = h.copy()
    hf["nca"] = hf.fta.astype(int)
    ck("SF2 the failure-to-appear score read as the scale moves the call", tier(route("R3", hf)) != 3,
       tier(route("R3", hf)))
    code_class = {}
    xw = pd.read_excel(os.path.join(target, K.CROSSWALK), sheet_name="Offense codes", header=4, dtype=str)
    for _, r in xw.iterrows():
        code_class[r["New code"]] = (r["G.S."], r["Class"])
    fl = fa.copy()
    import catalog as C
    fl["eligible"] = fl.apply(lambda r: (not r.detainer) and code_class[r.codes[0]][1] in C.MISD_CLASSES
                              and not C.in_appendix_b(code_class[r.codes[0]][0]), axis=1)
    ck("SF3 eligibility on the lead charge only: same call", holds(route("R3", CA.history(fl))),
       route("R3", CA.history(fl)))
    ck("SF4 the released defendants as the tier's population moves the call (the default path)",
       tier(L["R0 released defendants' rate"]) == 4)
    ev = pd.read_csv(os.path.join(target, K.EVENTS), dtype=str, keep_default_na=False)
    ck("SF5 a success rate (no missed court date) is not computable on the history: court events start 1 October 2025",
       ev.event_date.min() >= K.FY26_START.isoformat(), ev.event_date.min())
    ck("SF7 the window to the first charge's disposition: same call", holds(route("R3", CA.history(fas[("24h", "first")]))))
    t_flat = tier(route("R3", CA.history(CA.attach_outcomes(target, fa, cap="none"))))
    ck("SF7 the window at 365 days flat moves the call (ruled out by draft 2.4, whichever comes first)", t_flat != 3, t_flat)
    f48 = CA.attach_outcomes(target, released_within(fa, 48))
    ck("SF8 released within 48 hours: same call", holds(route("R3", CA.history(f48))))
    ck("SF8 released by the condition set: same call", holds(route("R3", CA.history(fas[("cond", "last")]))))
    gap = fa[fa.rel_type.isin(CA.RELEASES) & (fa.rel_t > fa.fa_t + pd.Timedelta(hours=24))
             & (fa.rel_t <= fa.fa_t + pd.Timedelta(hours=48))]
    ck("SF8 no release between 24 and 48 hours after an appearance", len(gap) == 0, len(gap))
    two = h[h.fa_t.dt.date >= K.HIST_LAST - dt.timedelta(days=729)]
    ck("SF9 the last two closed years: same call", holds(route("R3", two)))
    ck("SF9 the last closed year: same call", holds(route("R3", last_year(h))))
    ck("SF11 the floor applies score by score: the latest closed year's appearances alone give the same verdicts",
       all((route("R3", last_year(h))[s_] >= K.FLOOR) == (g[s_] >= K.FLOOR) for s_ in range(1, 5)))
    allyrs = fa[fa.eligible & fa.nca.notna()].copy()
    allyrs["nca"] = allyrs.nca.astype(int)
    allyrs["A"] = np.where(allyrs.released24, allyrs.y.fillna(0.0), 0.0)
    ck("SF9 all five years with the open windows run as far as they go: same call", holds(route("R3", allyrs)))
    near = [(k, s, round(L[k][s], 4)) for k in LENIENCY + RELEASED_FAMILY for s in range(1, 7)
            if abs(L[k][s] - K.FLOOR) < 0.015]
    ck("SF10 no estimate of any score within 1.5 points of 85 on any route", not near, near)
    perdef = h.sort_values("fa_t").drop_duplicates("sid")
    ck("SF14 the first appearance per defendant only: same call", holds(route("R3", perdef)))
    bk = sc[sc.booking_number != ""].booking_number
    ck("SF15 one screen per booking (booking numbers unique among the screens)", bk.is_unique)
    ck("SF16 eligible appearances with no screen are outside the tier and few",
       0 < (fa.eligible & fa.nca.isna()).mean() < 0.05, round(float((fa.eligible & fa.nca.isna()).mean()), 4))
    # SF13: the rota balances caseloads across magistrates; released rates rise with leniency at score 4
    hh = h.copy()
    p0 = float((hh.nca >= 4).mean())
    grp = hh.groupby("mag").nca.agg(lambda s: (s >= 4).mean())
    nn = hh.groupby("mag").size()
    z = ((grp - p0) / np.sqrt(p0 * (1 - p0) / nn)).abs()
    ck("SF13 the rota: every magistrate's share of score-4-and-up appearances within 4 standard errors of the pooled",
       z.max() <= 4.0, round(float(z.max()), 2))
    lr = hh.groupby("mag").released24.mean().sort_values(ascending=False)
    n5 = len(lr) // 5
    top, bot = set(lr.index[:n5]), set(lr.index[-n5:])
    g4 = hh[(hh.nca == 4) & hh.released24]
    d_rate = g4[g4.mag.isin(top)].y.mean() - g4[g4.mag.isin(bot)].y.mean()
    ck("SF13 score 4: the most lenient fifth's released defendants show a new-offense rate 4 points or more above "
       "the strictest fifth's", d_rate >= 0.04, round(float(d_rate), 4))

    # ------------------------------------------------------------------ the asks against the clean truth
    ta, tb, tc = TR.ask_a_truth(W), TR.ask_b_truth(W), TR.ask_c_truth(W)
    A = {m: CA.ask_a(target, fa, m) for m in ("golden", "S1", "S2", "S3", "S4", "S5", "S6", "S7")}
    B = {m: CA.ask_b(target, fa, m) for m in ("golden", "S1", "S2")}
    Cc = {m: CA.ask_c(target, fa, m) for m in ("golden", "S1", "S2", "S3")}
    ck("Ask A golden equals the clean truth at every score", all(A["golden"].get(s) == ta.get(s) for s in range(1, 7)),
       (A["golden"], ta))
    ck("Ask B golden equals the clean truth at every score", all(tuple(B["golden"][s]) == tuple(tb[s]) for s in range(1, 7)),
       (B["golden"], tb))
    ck("Ask C golden equals the clean truth at every score", all(Cc["golden"].get(s) == tc.get(s) for s in range(1, 7)),
       (Cc["golden"], tc))
    for m in ("S1", "S2", "S3", "S4", "S5", "S6", "S7"):
        miss = sum(r10(A[m].get(s, 0)) != r10(A["golden"][s]) for s in range(1, 7))
        ck("Ask A stop %s misses all 6 figures" % m, miss == 6, (m, A[m]))
    for m in ("S1", "S2"):
        mc = sum(B[m][s][0] != B["golden"][s][0] for s in range(1, 7))
        ms = sum("%.1f" % K.round1(100 * B[m][s][0] / B[m][s][1]) != "%.1f" % K.round1(
            100 * B["golden"][s][0] / B["golden"][s][1]) for s in range(1, 7))
        ck("Ask B stop %s misses 5 or more of the 6 counts and of the 6 shares" % m, mc >= 5 and ms >= 5, (m, mc, ms))
    for m in ("S1", "S2", "S3"):
        miss = sum(r10(Cc[m].get(s, 0)) != r10(Cc["golden"][s]) for s in range(1, 7))
        ck("Ask C stop %s misses all 6 figures" % m, miss == 6, (m, Cc[m]))
    # SF17 to SF21 and SF25 to SF28 alternatives as computed stops
    ck("SF17 days or part of a day moves every Ask A figure", all(r10(A["S6"][s]) != r10(A["golden"][s]) for s in range(1, 7)))
    ck("SF18 the boarding read as a release moves every Ask A figure", all(r10(A["S1"][s]) != r10(A["golden"][s]) for s in range(1, 7)))
    ck("SF20 UTC midnights move every Ask A figure", all(r10(A["S4"][s]) != r10(A["golden"][s]) for s in range(1, 7)))
    ck("SF21 a boarding chained to the next booking moves every Ask A figure",
       all(r10(A["S2"][s]) != r10(A["golden"][s]) for s in range(1, 7)))
    ck("SF22 the appearance's own case numbers only move the Ask B figures", B["S1"] != B["golden"])
    evf = ev[ev.event_code == "FTA"]
    ck("SF23 every missed court date is an FTA event on the court date (one event per missed date)",
       not evf.duplicated(["case_number", "event_date"]).any())
    ck("SF25 billable days summed move every Ask C figure", all(r10(Cc["S1"][s]) != r10(Cc["golden"][s]) for s in range(1, 7)))
    ck("SF25 each enrollment counted on its own moves every Ask C figure",
       all(r10(Cc["S3"][s]) != r10(Cc["golden"][s]) for s in range(1, 7)))
    em = pd.read_csv(os.path.join(target, K.EM), dtype=str, keep_default_na=False)
    # SF19: the stay from booking, not from the appearance: some held appearances' bookings cross a midnight first
    yrA = fa[(fa.fa_t.dt.date >= K.FY26_START) & fa.eligible & fa.nca.notna() & ~fa.released24]
    jn2 = jl[jl.booking_type == "NEW"].set_index("booking_number")
    bk_loc = yrA.booking.map(jn2.booked_utc).apply(lambda x: K.utc_to_eastern(dt.datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ")))
    cross = int((bk_loc.apply(lambda t: t.date()) < yrA.fa_t.dt.date).sum())
    ck("SF19 held appearances whose booking crosses a midnight before the appearance exist (the stay runs from booking)",
       cross > 0, cross)
    # SF24: the unit is the release; some defendants have two releases in Ask B's period
    yrB = fa[(fa.fa_t.dt.date >= K.FY26_START) & (fa.fa_t.dt.date <= K.ASKB_LAST) & fa.released24 & fa.fta.notna()]
    twice = int((yrB.groupby("sid").size() >= 2).sum())
    ck("SF24 defendants released twice or more in Ask B's period exist (each release a unit)", twice > 0, twice)
    # SF26: every defendant released, not the eligible only
    c_el = CA.ask_c(target, fa, eligible_only=True)
    ck("SF26 Ask C on the eligible only moves every figure",
       all(r10(c_el.get(s, 0)) != r10(Cc["golden"][s]) for s in range(1, 7)))
    # SF27: enrollments open at 30 September 2026 are counted to that day
    sep = em[em.invoice_month == "2026-09"]
    ck("SF27 enrollments open at 30 September 2026 exist (no end date on the September line)", (sep.end_date == "").sum() > 0,
       int((sep.end_date == "").sum()))
    ck("SF28 vendor lines with no court case number exist (matched by name and date of birth)",
       0.05 < (em.court_case == "").mean() < 0.25, round(float((em.court_case == "").mean()), 3))
    # mid-bin: every graded ask figure 15 per cent of its bin or more from a rounding edge
    for s in range(1, 7):
        ck("mid-bin Ask A score %d" % s, edge(A["golden"][s], 10) >= 0.15, (A["golden"][s], edge(A["golden"][s], 10)))
        ck("mid-bin Ask C score %d" % s, edge(Cc["golden"][s], 10) >= 0.15, (Cc["golden"][s], edge(Cc["golden"][s], 10)))
        m, n = B["golden"][s]
        ck("mid-bin Ask B share, FTA score %d" % s, edge(1000.0 * m / n, 1) >= 0.15, (m, n, edge(1000.0 * m / n, 1)))
    ck("no round headline: no unrounded ask total is a multiple of 100",
       all(A["golden"][s] % 100 and Cc["golden"][s] % 100 for s in range(1, 7)))

    # ------------------------------------------------------------------ the separation line
    jl["b"] = pd.to_datetime(jl.booked_utc, format="%Y-%m-%dT%H:%M:%SZ")
    jl["e"] = pd.to_datetime(jl.released_utc.where(jl.released_utc != "", None), format="%Y-%m-%dT%H:%M:%SZ")
    n_dev = int((jl[jl.booking_type == "BI"].b.dt.date <= K.HIST_LAST).sum() +
                (jl[jl.release_type == "BO"].e.dt.date <= K.HIST_LAST).sum())
    ck("separation: no boarding or return booking before the history ends", n_dev == 0, n_dev)
    cases = pd.read_csv(os.path.join(target, K.CASES), dtype=str, keep_default_na=False)
    ind = set(cases[cases.disposition_code == "IND"].case_number)
    ck("separation: no eligible history appearance has an indicted case",
       sum(any(c in ind for c in cs) for cs in h.cases) == 0)
    ck("separation: the call reads no ask file", not ({K.EM, K.HALSEY, K.EVENTS} & call_reads), sorted(call_reads))
    ck("distractors: the call and the asks read neither distractor", not (set(K.DISTRACTORS) & call_reads))
    with Reads(target) as rd2:
        CA.ask_a(target, fa)
        CA.ask_b(target, fa)
        CA.ask_c(target, fa)
    ck("distractors: no ask reads a distractor", not (set(K.DISTRACTORS) & rd2.seen), sorted(rd2.seen))

    # ------------------------------------------------------------------ input gates
    rows_max = 0
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                rows_max = max(rows_max, sum(1 for _ in fh) - 1)
    ck("gate: 10 or more files", len(files) >= 10, len(files))
    ck("gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    ck("gate: a file of 25,000 rows or more", rows_max >= 25000, rows_max)
    if meta:
        ck("gate: two or more distractors declared, each shipped", len(meta["distractor_files"]) >= 2
           and all(d in files for d in meta["distractor_files"]))
    ck("gate: no file name says distractor", not any("distractor" in f.lower() for f in files))

    # ------------------------------------------------------------------ realism sweep and containers
    stamp = None
    for f in files:
        m = os.path.getmtime(os.path.join(target, f))
        stamp = m if stamp is None else stamp
        if m != stamp:
            stamp = -1
    ck("realism: every file carries the one export time", stamp != -1)
    tells = []
    for f in files + ["golden/" + x for x in os.listdir(golden)]:
        p = os.path.join(target, f) if not f.startswith("golden/") else os.path.join(golden, f[7:])
        if p.endswith((".docx", ".xlsx")):
            z = zipfile.ZipFile(p)
            for n in z.namelist():
                if n.startswith("docProps/"):
                    d = z.read(n)
                    if re.search(rb"python-docx|openpyxl|python|reportlab", d, re.I):
                        tells.append((f, n))
        if p.endswith(".pdf"):
            d = open(p, "rb").read()
            if re.search(rb"ReportLab|reportlab", d):
                tells.append((f, "pdf"))
        if p.endswith(".png"):
            d = open(p, "rb").read()
            if b"matplotlib" in d.lower() or b"Software" in d:
                tells.append((f, "png"))
    ck("realism: containers carry no library banner", not tells, tells)
    em_dash = [f for f in files if f.endswith((".txt", ".csv")) and "\u2014" in open(os.path.join(target, f), encoding="utf-8").read()]
    ck("realism: no em dash in a text extract", not em_dash, em_dash)
    cnt = h.groupby("mag").size()
    ck("realism: no caseload repeated across more than three magistrates", cnt.value_counts().max() <= 3)
    card = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                                       ".claude", "skills", "fingerprint", "cards", "task141.json")))
    ck("realism: every persona is a drawn name on the card", set(K.PEOPLE.values()) <= set(card["world"]["people"]))
    # the README registers every shipped file but itself; no record dated after the extract
    readme = texts.get(K.README, "")
    listed = {ln.strip() for ln in readme.splitlines() if ln.strip() in files}
    ck("register: the README lists every shipped file but itself", listed == set(files) - {K.README},
       sorted(set(files) - {K.README} - listed))
    late = []
    for f, cols in ((K.CASES, ["filed_date", "disposition_date"]), (K.EVENTS, ["event_date"]),
                    (K.ARRESTS, ["arrest_date", "offense_date"])):
        d = pd.read_csv(os.path.join(target, f), dtype=str, keep_default_na=False, usecols=cols)
        for c in cols:
            if (d[c] > K.EXTRACT_END.isoformat()).any():
                late.append((f, c, d[c].max()))
    ck("dates: no court or arrest record dated after 30 September 2026", not late, late)
    # each load-bearing sentence in one file
    floor_files = [f for f, t in texts.items() if re.search(r"85 ?(percent|per cent|%)", t)]
    ck("one file: the 85 percent floor stands in the draft only", floor_files == [K.DRAFT], floor_files)
    rota_files = [f for f, t in texts.items() if re.search(r"\brota\b", t)]
    ck("one file: the duty rota stands in the 2024 policy only", rota_files == [K.POLICY24], rota_files)
    ck("one file: the boarding code stands in the jail code list only",
       [f for f, t in texts.items() if "contract facility" in t] == [K.JAIL_CODES]
       if K.JAIL_CODES in texts else True)
    ck.report()
    return dict(L=L, A=A, B=B, C=Cc, st=st, cells=cells)
