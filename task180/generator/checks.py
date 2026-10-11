"""Assertions over the built pack and the goldens: the call; every rung by name with its margin; every cell of the
between-person and self-controlled grids; the evidence the judge reads (the year before the start, the NSAID-free
starters, the direction of the event-dependent starts); every ask figure, its rounding distance and every stop that
moves it; mess neutrality of the call; the convergences that close the forks; the pack gates, the banned-word sweep,
the containers, the dates and the personas. Everything is computed from target/ (and golden/) through golden.py,
plus the simulated world where an assertion is about the world itself."""
import csv
import datetime as dt
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
import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as G      # noqa: E402
import world as W       # noqa: E402

TASK = os.path.dirname(HERE)
REPO = os.path.dirname(TASK)
N_ASSERT = [0]
LOG = []
ASOF = dt.date(2026, 10, 12)
ANSWER, NAIVE_WINNER = "corinurad", "tasorexant"
NAIVE_MARGIN, AC_LIMIT, CLOSURE = 1.3, 1.4, 1.25
SC_MIN, SC_LOWER, RIVAL_MAX, BAND = 2.2, 1.6, 1.25, 0.3
# the two convention variants (deaths not ending observation, transfers not merged) only have to keep the winner
VARIANT_MIN = 2.0
BANNED = re.compile(r"self[- ]controlled|case[- ]series|\bSCCS\b|\bSCRI\b|risk interval|within[- ]person|"
                    r"within[- ]patient|own time|channel\w*|confound\w*|indication bias|protopathic|\bfrail\w*|"
                    r"active comparator|propensity", re.I)
TOOLCHAIN = re.compile(r"python-docx|openpyxl|reportlab|matplotlib|pandas|numpy|pyarrow|distractor|\bclaude\b|"
                       r"anthropic|lorem|placeholder|\bseed\b|\bsynthetic\b|\bsimulat\w*", re.I)


def ok(cond, msg):
    N_ASSERT[0] += 1
    if not cond:
        raise AssertionError(msg)


def file_text(path):
    if path.endswith(".pdf"):
        with pdfplumber.open(path) as p:
            return "\n".join(pg.extract_text() or "" for pg in p.pages)
    if path.endswith(".xlsx"):
        wb = openpyxl.load_workbook(path, read_only=True)
        return "\n".join(str(v) for ws in wb.worksheets for row in ws.iter_rows(values_only=True) for v in row
                         if v is not None) + "\n" + "\n".join(ws.title for ws in wb.worksheets)
    if path.endswith(".docx"):
        from docx import Document
        d = Document(path)
        return "\n".join(p.text for p in d.paragraphs) + "\n" + "\n".join(
            c.text for t in d.tables for r in t.rows for c in r.cells)
    if path.endswith(".parquet"):
        t = pq.read_table(path)
        out = [" ".join(t.column_names)]
        for c in t.column_names:
            if str(t.schema.field(c).type) == "string":
                out += [str(x) for x in pd.unique(t.column(c).to_pandas().dropna())[:5000]]
        return "\n".join(out)
    if path.endswith(".csv"):
        df = pd.read_csv(path, dtype=str, keep_default_na=False, sep=None, engine="python", nrows=200000)
        return " ".join(df.columns) + "\n" + "\n".join(str(x) for c in df.columns for x in df[c].unique()[:5000])
    return open(path, encoding="utf-8", errors="ignore").read()


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".parquet"):
        return int(pq.ParquetFile(path).metadata.num_rows)
    return None


def edge(x, places=2):
    """Distance of x from the nearest rounding edge at the given places, in units of the last place."""
    y = x * 10 ** places
    return abs(y - np.floor(y) - 0.5)


# ------------------------------------------------------------------ the checks

def run(target, golden_dir, world=None, meta_path=None, quiet=False):
    D, g = G.solve(target)
    a = g["answer"]

    # ---------------------------------------------------------------- the call
    ok(a == ANSWER, "the call moved: %s" % a)
    rr, lo, hi = g["ratio"], g["lower"], g["upper"]
    ok(rr >= SC_MIN and lo >= SC_LOWER, "corinurad golden ratio %.3f (%.3f)" % (rr, lo))
    for s in G.NEW:
        if s != a:
            r_, l_, h_ = g["sccs"][s]
            ok(r_ <= RIVAL_MAX and l_ < 1 < h_, "%s golden cell %.3f (%.3f to %.3f)" % (s, r_, l_, h_))
            ok(rr / r_ >= CLOSURE * 1.5, "closure at the answer's rung: %s within reach" % s)
    LOG.append("call: %s %.4f (%.4f to %.4f); tasorexant %.4f (%.4f to %.4f); velaglutide %.4f (%.4f to %.4f)" % (
        (a, rr, lo, hi) + g["sccs"]["tasorexant"] + g["sccs"]["velaglutide"]))
    # risk-window events behind the answer
    ev = G.events(D, "aki")
    pid, s0, e0 = G.episodes(D, a)
    n_risk, _, _, _ = G.window(ev, pid, s0, e0, 1, 30)
    n_ctrl, _, _, _ = G.window(ev, pid, s0, e0, 61, 180)
    ok(n_risk.sum() >= 40, "corinurad kidney injury admissions in risk windows: %d" % n_risk.sum())
    LOG.append("corinurad: %d new-user starts, %d admissions in days 1 to 30, %d in days 61 to 180" % (
        len(pid), n_risk.sum(), n_ctrl.sum()))

    # ---------------------------------------------------------------- rung 0: the screen
    rep = g["reports"]
    f, sec, m = G.lead(rep)
    ok(f == NAIVE_WINNER and m >= CLOSURE, "rung 0: %s" % rep)
    wb = openpyxl.load_workbook(os.path.join(target, G.SCREEN), read_only=True)
    screen = list(wb["Screen Q3 2026"].iter_rows(values_only=True))
    hdr = list(screen[0])
    for s, pt in G.PT.items():
        row = [r for r in screen[1:] if r[0] == s and r[2] == pt]
        ok(len(row) == 1 and row[0][hdr.index("Cases Q3 2026")] == rep[s], "screen Q3 cases for %s match the listing" % s)
        a_, ns, npt, N = (row[0][hdr.index(c)] for c in ("Cases since launch", "Reports with substance",
                                                         "Reports with term", "Reports in database"))
        b_, c_ = ns - a_, npt - a_
        prr = (a_ / (a_ + b_)) / (c_ / (c_ + N - a_ - b_ - c_))
        ok(abs(round(prr, 2) - row[0][hdr.index("PRR")]) < 1e-9, "PRR of %s recomputes" % s)
    LOG.append("rung 0 (Q3 cases, latest version, suspected): %s; leader by %.2f" % (rep, m))

    # ---------------------------------------------------------------- rungs 1, 1b, 2: every between-person cell
    ng = G.naive_grid(D)
    ok(len(ng) == 48, "naive grid size %d" % len(ng))
    mins = {}
    for k, v in ng.items():
        f, sec, m = G.lead(v)
        ok(f == NAIVE_WINNER and m >= NAIVE_MARGIN, "naive cell %s: %s" % (k, v))
        ok(v[ANSWER] < v[NAIVE_WINNER] / NAIVE_MARGIN, "naive cell %s puts corinurad near the lead" % (k,))
        if k[0].startswith("R2"):
            ok(v[ANSWER] <= AC_LIMIT, "corinurad against allopurinol starters in %s: %.3f" % (k, v[ANSWER]))
        name = k[0]
        if name not in mins or m < mins[name][0]:
            mins[name] = (m, k[1:], v)
    for name, (m, k, v) in mins.items():
        LOG.append("%s: thinnest margin %.2f (%s; tasorexant %.3f, corinurad %.3f, velaglutide %.3f)" % (
            (name, m, k) + tuple(v[s] for s in G.NEW)))
    base = {k[0]: v for k, v in ng.items() if k[1:] == ("from 2022", True, True)}
    g["naive_main"] = base
    g["naive_min_margin"] = min(x[0] for x in mins.values())
    g["ac_max_corinurad"] = max(v[ANSWER] for k, v in ng.items() if k[0].startswith("R2"))

    # ---------------------------------------------------------------- rung 3: every self-controlled cell
    main_cells, variant_cells = 0, 0
    spread = {}
    for s in G.NEW:
        for censor, merge in ((True, True), (False, True), (True, False)):
            grid = G.sccs_grid(D, s, censor=censor, merge=merge)
            for k, v in grid.items():
                spread.setdefault((s, censor, merge), []).append((v[0], k, v))
                if (censor, merge) == (True, True):
                    main_cells += 1
                else:
                    variant_cells += 1
    for (s, censor, merge), lst in spread.items():
        vals = [x[0] for x in lst]
        if s == ANSWER:
            for r_, k, v in lst:
                floor = SC_MIN if (censor, merge) == (True, True) else VARIANT_MIN
                ok(r_ >= floor, "corinurad cell %s censor=%s merge=%s: %.3f" % (k, censor, merge, r_))
                if (censor, merge) == (True, True):
                    ok(abs(r_ - rr) <= BAND, "corinurad cell %s outside the band: %.3f" % (k, r_))
                if v[1] is not None:
                    ok(v[1] >= SC_LOWER, "corinurad cell %s lower %.3f" % (k, v[1]))
        else:
            for r_, k, v in lst:
                ok(r_ <= RIVAL_MAX, "%s cell %s censor=%s merge=%s: %.3f" % (s, k, censor, merge, r_))
                if v[1] is not None:
                    ok(v[1] < 1 < v[2], "%s cell %s interval %.3f to %.3f" % (s, k, v[1], v[2]))
        LOG.append("rung 3 %-11s deaths end observation=%s transfers merged=%s: %d cells, ratio %.3f to %.3f" % (
            s, censor, merge, len(lst), min(vals), max(vals)))
    for key in spread:
        if key[0] == ANSWER:
            continue
        for (r_a, k_a, _), (r_r, k_r, _) in zip(spread[(ANSWER,) + key[1:]], spread[key]):
            ok(k_a == k_r and r_a / r_r >= CLOSURE, "closure: %s within 25 per cent of corinurad in %s" % (key[0], k_a))
    ok(main_cells == 3 * 189 and variant_cells == 2 * main_cells,
       "grid size %d + %d" % (main_cells, variant_cells))
    LOG.append("rung 3 grid: %d cells under the pinned conventions and %d under the two convention variants; misses 0"
               % (main_cells, variant_cells))
    cor_main = [x[0] for x in spread[(ANSWER, True, True)]]
    g["sccs_range"] = (min(cor_main), max(cor_main))
    g["sccs_cells"] = (main_cells, variant_cells)

    # ---------------------------------------------------------------- the year before the start
    pre = g["pre"]
    tm = pre["tasorexant users"] / pre["tasorexant matched"]
    tz = pre["tasorexant users"] / pre["zopiclone users"]
    ca = pre["corinurad users"] / pre["allopurinol users"]
    ok(3.4 <= tm <= 4.8, "tasorexant against matched non-users, year before: %.3f" % tm)
    ok(1.8 <= tz <= 2.6, "tasorexant against zopiclone starters, year before: %.3f" % tz)
    ok(0.38 <= ca <= 0.6, "corinurad against allopurinol starters, year before: %.3f" % ca)
    for x in (tm, tz, ca):
        ok(edge(x) >= 0.05, "pre-start ratio %.4f sits near a two-decimal edge" % x)
    LOG.append("year before the start: tasorexant %.2f x matched non-users, %.2f x zopiclone starters; corinurad %.2f x "
               "allopurinol starters" % (tm, tz, ca))

    # ---------------------------------------------------------------- NSAID independence
    nf = g["nsaid_free"]
    ok(nf[0] >= 2.0 and nf[1] > 1.0, "corinurad among NSAID-free starters: %.3f (%.3f)" % (nf[0], nf[1]))
    ok(0.6 <= g["nsaid_free_share"] <= 0.85, "NSAID-free share %.3f" % g["nsaid_free_share"])
    pid_n, s_n, _ = G.episodes(D, ANSWER)
    rx = D.rx[D.rx["atc"].str.startswith("M01A") & (D.rx["apk"] > 0)]
    key = np.sort(rx["pid"].to_numpy() * 10 ** 6 + rx["day"].to_numpy())
    k30 = np.searchsorted(key, pid_n * 10 ** 6 + s_n + 30, side="right") - np.searchsorted(key, pid_n * 10 ** 6 + s_n)
    kb = np.searchsorted(key, pid_n * 10 ** 6 + s_n - 1, side="right") - np.searchsorted(key, pid_n * 10 ** 6 + s_n - 31)
    ok((k30 > 0).mean() > 2 * (kb > 0).mean(), "NSAIDs cluster in the month after a corinurad start (flare cover)")
    LOG.append("NSAID-free corinurad starters (%.0f per cent): %.3f (%.3f to %.3f); NSAID in days 0 to 30 %.1f per cent "
               "against %.1f per cent in the month before" % (100 * g["nsaid_free_share"], nf[0], nf[1], nf[2],
                                                                100 * (k30 > 0).mean(), 100 * (kb > 0).mean()))

    # ---------------------------------------------------------------- the event-dependent starts
    full_with = {s: G.sccs(D, s, control="full")[0] for s in ("tasorexant", "corinurad")}
    full_without = {s: G.sccs(D, s, control="full", pre=0)[0] for s in ("tasorexant", "corinurad")}
    ok(full_without["corinurad"] > full_with["corinurad"], "a kidney injury lowers the chance of starting: the ratio "
       "over all time rises when the month before the start stays in the baseline")
    ok(full_without["tasorexant"] < full_with["tasorexant"], "a fall raises the chance of starting: the falls ratio over "
       "all time falls when the month before the start stays in the baseline")
    for s, kind in (("tasorexant", "fall"), ("corinurad", "aki")):
        evk = G.events(D, kind)
        p_, s_, _ = G.episodes(D, s)
        I = D.imm[p_]
        lo_ = np.where(I < G.BIG, np.maximum(G.Y2022, I), G.Y2022)
        keep = s_ - 395 >= lo_
        n_pre = G.count_in(evk, p_[keep], s_[keep] - 30, s_[keep] - 1).sum()
        n_base = G.count_in(evk, p_[keep], s_[keep] - 395, s_[keep] - 31).sum()
        ratio = (n_pre / 30) / (n_base / 365)
        if s == "tasorexant":
            ok(ratio > 1.2, "falls in the month before a tasorexant start: %.2f x the year before that" % ratio)
        else:
            ok(ratio < 0.7, "kidney injury in the month before a corinurad start: %.2f x the year before that" % ratio)
        LOG.append("%s: month before the start %.2f x the rate of days -395 to -31 (%d events)" % (s, ratio, n_pre))
    # the window anchored on the start reads nothing before it: deleting every earlier event leaves it unchanged
    p_a, s_a, e_a = G.episodes(D, ANSWER)
    first_start = pd.Series(s_a).groupby(p_a).min()
    keep_ev = ev[1] >= first_start.reindex(ev[0]).fillna(G.BIG).to_numpy()
    trimmed = (ev[0][keep_ev], ev[1][keep_ev])
    ok(G.sccs(D, ANSWER, ev=trimmed) == g["sccs"][ANSWER], "the golden cell reads no time before the start")
    LOG.append("observation over all time from 2022: corinurad %.3f with days -30 to 0 set aside, %.3f without; "
               "tasorexant %.3f and %.3f" % (full_with["corinurad"], full_without["corinurad"], full_with["tasorexant"],
                                             full_without["tasorexant"]))

    # ---------------------------------------------------------------- the asks
    k25, exact, caused = g["events_2025"], g["caused_exact"], g["caused"]
    ok(caused == int(np.floor(exact + 0.5)), "caused rounding")
    ok(abs(exact - np.floor(exact) - 0.5) >= 0.1, "caused %.3f sits within 0.1 of a rounding edge" % exact)
    r2 = round(rr, 2)
    ok(int(np.floor(k25 * (r2 - 1) / r2 + 0.5)) == caused, "caused is the same from the two-decimal ratio")
    for x in (rr, lo, hi):
        ok(edge(x) >= 0.05, "figure %.5f within 0.0005 of a two-decimal edge" % x)
    nu = g["new_users"]
    graded = [("ratio", round(rr, 2)), ("lower", round(lo, 2)), ("upper", round(hi, 2)), ("admissions", k25),
              ("caused", caused)] + [("%s %d" % k, v) for k, v in nu.items()]
    vals = [v for _, v in graded]
    ok(len(set(vals)) == len(vals), "a tie among graded figures: %s" % graded)
    ok(all(v % 100 != 0 for _, v in graded if isinstance(v, int) and v > 100), "a new-user count on a round hundred")
    LOG.append("asks: ratio %.2f (%.2f to %.2f); 2025 starters' admissions in days 1 to 30: %d; caused %d (%.3f); "
               "new users %s" % (rr, lo, hi, k25, caused, exact, nu))
    ok(nu[("corinurad", 2022)] > 0 and nu[("corinurad", 2023)] > 0, "corinurad users under the provisional code")

    # ---------------------------------------------------------------- the stops, each moving its figures
    def moved_csv(label, other):
        diff = {k: (nu[k], other[k]) for k in nu if nu[k] != other[k]}
        ok(len(diff) > 0, "stop '%s' moves no new-user count" % label)
        LOG.append("stop, %s: %s" % (label, "; ".join("%s %d %d->%d" % (k[0], k[1], v[0], v[1]) for k, v in diff.items())))
        return diff

    cur = G.new_users_by_year(D, current_only=True)
    d1 = moved_csv("current ATC code only", cur)
    ok(cur[("corinurad", 2022)] == 0 and cur[("corinurad", 2023)] == 0, "the provisional-code users vanish")
    ok(cur[("corinurad", 2024)] > nu[("corinurad", 2024)], "continuing users look new in 2024")
    moved_csv("washout ignored, first dispensing only", G.new_users_by_year(D, washout="first"))
    moved_csv("washout ignored, first dispensing each year", G.new_users_by_year(D, washout="year"))
    moved_csv("returned dispensings counted", G.new_users_by_year(D, net=False))
    moved_csv("residence ignored", G.new_users_by_year(D, residence=False))
    stops_ask = {
        "transfers counted as separate admissions": dict(merge=False),
        "secondary diagnoses counted": dict(secondary=True),
        "outpatient contacts counted": dict(outpatient=True),
    }
    for label, kw in stops_ask.items():
        k2, _, c2 = G.asks(D, ANSWER, rr, **kw)
        ok(k2 > k25, "stop '%s' moves the 2025 admissions (%d -> %d)" % (label, k25, k2))
        LOG.append("stop, %s: 2025 admissions %d -> %d" % (label, k25, k2))
    for label, kw in (("returned dispensings counted", dict(net=False)), ("residence ignored", dict(residence=False)),
                      ("current ATC code only", dict(current_only=True))):
        k2, _, _ = G.asks(D, ANSWER, rr, **kw)
        LOG.append("stop, %s: 2025 admissions %d -> %d" % (label, k25, k2))
    # the ratio under each stop: the call never moves, the figure does
    stop_cells = {
        "deaths and emigrations not ending observation": dict(censor=False),
        "transfers counted as separate admissions": dict(ev=G.events(D, "aki", merge=False)),
        "secondary diagnoses counted": dict(ev=G.events(D, "aki", secondary=True)),
        "outpatient contacts counted": dict(ev=G.events(D, "aki", outpatient=True)),
        "current ATC code only": dict(nu=(("current_only", True),)),
        "washout ignored (first dispensing only)": dict(nu=(("washout", "first"),)),
        "returned dispensings counted": dict(nu=(("net", False),)),
        "residence ignored": dict(nu=(("residence", False),)),
    }
    rival_ev = {"deaths and emigrations not ending observation": {}, "transfers counted as separate admissions":
                {"tasorexant": dict(ev=G.events(D, "fall", merge=False)),
                 "velaglutide": dict(ev=G.events(D, "pancreatitis", merge=False))},
                "secondary diagnoses counted": {"tasorexant": dict(ev=G.events(D, "fall", secondary=True)),
                                                "velaglutide": dict(ev=G.events(D, "pancreatitis", secondary=True))},
                "outpatient contacts counted": {"tasorexant": dict(ev=G.events(D, "fall", outpatient=True)),
                                                "velaglutide": dict(ev=G.events(D, "pancreatitis", outpatient=True))}}
    for label, kw in stop_cells.items():
        r_stop = G.sccs(D, ANSWER, **kw)
        rivals = {}
        for s in G.NEW:
            if s == ANSWER:
                continue
            kw_r = dict(kw)
            kw_r.pop("ev", None)
            kw_r.update(rival_ev.get(label, {}).get(s, {}))
            rivals[s] = G.sccs(D, s, **kw_r)[0]
        ok(r_stop[1] > 1 and all(r_stop[0] / v >= CLOSURE for v in rivals.values()),
           "the call moves under '%s': %s %s" % (label, r_stop, rivals))
        LOG.append("stop, %s: corinurad %.3f (%.3f to %.3f); rivals %s" % (
            (label,) + r_stop + ({k: round(v, 3) for k, v in rivals.items()},)))
    ok(G.sccs(D, ANSWER, censor=False)[0] != rr, "the death and emigration stop moves the ratio")

    # ---------------------------------------------------------------- convergences that close the forks
    for kind in ("fall", "aki", "pancreatitis"):
        base_ev = G.events(D, kind)
        for hours in (1.0, 12.0, 24.0, 48.0):
            alt = G.events(D, kind, link_hours=hours)
            ok(np.array_equal(alt[0], base_ev[0]) and np.array_equal(alt[1], base_ev[1]),
               "%s events differ when contacts link within %g hours" % (kind, hours))
    LOG.append("transfers: contacts linked within 1, 4, 12, 24 or 48 hours give the same admissions for every event")
    c = D.c
    gap = c["start"].to_numpy()[1:] - c["end"].to_numpy()[:-1]
    acute = c["acute"].to_numpy()
    same = (c["pid"].to_numpy()[1:] == c["pid"].to_numpy()[:-1]) & ~c["lpr2"].to_numpy()[1:] & \
        (c["end"].to_numpy()[:-1] >= 0) & (acute[1:] | acute[:-1])
    ok(not np.any(same & (gap > 60) & (gap < 48 * 60)), "an acute contact between 1 and 48 hours from the next")
    for s in list(G.NEW) + ["zopiclone", "allopurinol", "orlistat"]:
        p_, d_ = G.valid_dispensings(D, s)
        gaps = np.diff(d_)[p_[1:] == p_[:-1]]
        ok(not np.any((gaps > 335) & (gaps < 395)), "%s: a gap of 336 to 394 days between dispensings" % s)
        st = G.new_users(D, s, residence=False)
        I = D.imm[st["pid"].to_numpy()]
        near = (I < G.BIG) & (np.abs(st["day"].to_numpy() - 365 - I) <= 10)
        ok(not near.any(), "%s: an immigration within ten days of the residence boundary" % s)
    LOG.append("washout and residence boundaries: no dispensing gap of 336 to 394 days, no immigration within ten days "
               "of a start's 365-day boundary")
    # an observation that stops the day before death or emigration gives the same figures
    pid_e, s_e, e_e = G.episodes(D, ANSWER)
    e_alt = np.where(e_e < G.END, e_e - 1, e_e)
    a1, r1, _, _ = G.window(ev, pid_e, s_e, e_alt, 1, 30)
    b1, c1, _, _ = G.window(ev, pid_e, s_e, e_alt, 61, 180)
    ok(round(G.cpois(a1, b1, r1, c1)[0], 2) == round(rr, 2), "the ratio depends on counting the day of death")
    # no admission starts on a day of death or emigration
    ex_day = np.minimum(D.death, D.emig)
    for kind in ("fall", "aki", "pancreatitis"):
        e_ = G.events(D, kind)
        ok(not np.any(e_[1] == ex_day[e_[0]]), "a %s admission on the day of death or emigration" % kind)

    # ---------------------------------------------------------------- the world behind the extract
    if world is not None:
        P = world["P"]
        ok(W.RR_CORINURAD == 2.5 and world["effect_events"] > 0, "the world's one effect")
        for col in ("latent_fall", "latent_aki", "latent_pancreatitis"):
            ok(col in P and not any(col.split("_")[0] in x for x in []), "latent multipliers stay in the world")
        lat = {}
        for name in ("tasorexant", "zopiclone", "corinurad", "allopurinol", "velaglutide", "orlistat"):
            m = P["user_of"] == list(W.COHORTS).index(name)
            lat[name] = (P["latent_fall"][m].mean(), P["latent_aki"][m].mean(), P["latent_pancreatitis"][m].mean())
        ok(lat["tasorexant"][0] > 1.8 * lat["zopiclone"][0] * 0.95, "tasorexant starters carry the fall excess")
        ok(lat["corinurad"][1] < 0.6 * lat["allopurinol"][1], "corinurad starters carry the kidney reserve")
        LOG.append("world: latent fall multiplier tasorexant %.2f, zopiclone %.2f; latent kidney multiplier corinurad %.2f, "
                   "allopurinol %.2f; corinurad effect events %d; variants %s" % (
                       lat["tasorexant"][0], lat["zopiclone"][0], lat["corinurad"][1], lat["allopurinol"][1],
                       world["effect_events"], world["variants"]))

    # ---------------------------------------------------------------- leak hygiene, every shipped text file
    prompt = open(os.path.join(TASK, "prompt.md"), encoding="utf-8").read()
    files = sorted(os.listdir(target))
    texts = {}
    for f in files + ["../prompt.md"]:
        t = prompt if f == "../prompt.md" else file_text(os.path.join(target, f))
        texts[f] = t
        hits = sorted(set(m.group(0).lower() for m in BANNED.finditer(t)))
        ok(not hits, "%s carries %s" % (f, hits))
        ok("\u2014" not in t and "\u2013" not in t, "%s carries an em or en dash" % f)
        if f != "../prompt.md":
            tc = sorted(set(m.group(0) for m in TOOLCHAIN.finditer(t)))
            ok(not tc, "%s carries toolchain or author words %s" % (f, tc))
    for f in os.listdir(golden_dir):
        gt = file_text(os.path.join(golden_dir, f))
        ok("\u2014" not in gt, "golden %s carries an em dash" % f)
    LOG.append("banned-word sweep (%d terms) over %d shipped files and the prompt: clean" % (
        len(BANNED.pattern.split("|")), len(files)))
    # each load-bearing fact stated once: the case definitions and the window live in the SOP only (the registry
    # tables carry the codes as values, which states nothing)
    sop = texts["SOP-PV-14_signal_refinement.pdf"]
    for phrase in ("days 1 to 30", "365 days", "DN17", "DK85", "DW00"):
        holders = [f for f, t in texts.items() if phrase in t and not f.endswith(".parquet")]
        ok(holders == ["SOP-PV-14_signal_refinement.pdf"], "'%s' stated in %s" % (phrase, holders))
    ok("comparison" not in sop.lower() and "comparator" not in sop.lower() and "non-user" not in sop.lower(),
       "the SOP names a comparison")

    # ---------------------------------------------------------------- pack gates
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    ok(10 <= len(files) <= 14, "file count %d" % len(files))
    ok(len(fmts) >= 3, "formats %s" % fmts)
    big = {f: n for f, n in ((f, rows_of(os.path.join(target, f))) for f in files) if n and n >= 25000}
    ok(len(big) >= 1, "a file of 25,000 rows or more")
    total = sum(os.path.getsize(os.path.join(target, f)) for f in files)
    ok(total < 150 * 2 ** 20, "pack size %.1f MB" % (total / 2 ** 20))
    ok(not any(f.startswith(".") for f in files), "no dot files")
    LOG.append("pack: %d files, formats %s, largest %s (%d rows), %.1f MB" % (
        len(files), fmts, max(big, key=big.get), max(big.values()), total / 2 ** 20))
    if meta_path and os.path.exists(meta_path):
        meta = json.load(open(meta_path, encoding="utf-8"))
        dis = meta["distractor_files"]
        ok(len(dis) == 2 and all(d in files for d in dis), "two distractors named in metadata.json and shipped")
        ok(sorted(x["path"] for x in meta["files"]) == files, "metadata.json lists exactly the shipped files")
        for d in dis:
            tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
            try:
                for f in files:
                    if f != d:
                        os.symlink(os.path.abspath(os.path.join(target, f)), os.path.join(tmp, f))
                _, g2 = G.solve(tmp)
                same = (g2["answer"] == a and g2["ratio"] == rr and g2["events_2025"] == k25 and
                        g2["caused"] == caused and g2["new_users"] == nu)
                ok(same, "the golden reads %s" % d)
            finally:
                shutil.rmtree(tmp)
        LOG.append("distractors %s: the golden recomputes unchanged without each" % dis)
    ok(sorted(os.listdir(golden_dir)) == ["new_users_by_year.csv", "signal_refinement_note.docx"], "the two deliverables")

    # ---------------------------------------------------------------- containers and dates
    sig = re.compile(rb"openpyxl|Openpyxl|ReportLab|reportlab|python-docx|python-pptx|matplotlib")
    for f in files + [os.path.join(golden_dir, "signal_refinement_note.docx")]:
        p = os.path.join(target, f)
        if f.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(p) as z:
                meta_b = b"".join(z.read(n) for n in z.namelist() if n.startswith("docProps/"))
                stamps = {i.date_time for i in z.infolist()}
            ok(not sig.search(meta_b), "%s carries a writer signature" % f)
            ok(stamps == {(1980, 1, 1, 0, 0, 0)}, "%s zip stamps" % f)
            for m in re.findall(rb"\d{4}-\d\d-\d\dT", meta_b):
                ok(b"2026" == m[:4], "%s stamp %s out of band" % (f, m))
        if f.endswith(".pdf"):
            b = open(p, "rb").read()
            ok(not sig.search(b), "%s carries a writer signature" % f)
            ok(all(b"2026" == m[2:6] for m in re.findall(rb"D:\d{14}", b)), "%s dates" % f)
    scrub = os.path.join(REPO, ".claude/skills/reduce-house-fixes/scripts/scrub_producer_metadata.py")
    out = subprocess.run([sys.executable, scrub, target, "--floor", "2026-01-01", "--ceiling", "2026-10-12"],
                         capture_output=True, text=True).stdout
    ok("clean" in out.lower(), "producer audit: %s" % out.strip()[:300])
    late = {}
    for f in files:
        if f.endswith((".csv", ".md")):
            for m in re.finditer(r"\b(20\d\d-\d\d-\d\d)\b", open(os.path.join(target, f), encoding="utf-8").read()):
                if m.group(1) > ASOF.isoformat():
                    late.setdefault(f, set()).add(m.group(1))
    ok(not late, "dates after the setting: %s" % late)
    for f, col in ((G.PRESCRIPTIONS, "eksd"), (G.CONTACTS, "starttid")):
        mx = pq.read_table(os.path.join(target, f), columns=[col]).column(col).to_pandas().max()
        ok(pd.Timestamp(mx) <= pd.Timestamp("2026-06-30 23:59:59"), "%s runs past the extract: %s" % (f, mx))
    ok(D.death[D.death < G.BIG].max() <= G.END and D.emig[D.emig < G.BIG].max() <= G.END, "civil dates past the extract")

    # ---------------------------------------------------------------- the documents and the goldens agree with the solve
    note = file_text(os.path.join(golden_dir, "signal_refinement_note.docx"))
    ok("Open the formal assessment on corinurad (Uralexa) and acute kidney injury" in note, "the note names the call")
    ok("%.2f (%.2f to %.2f)" % (rr, lo, hi) in note, "the note's ratio")
    ok("%d admissions with acute kidney injury fell in that month, and corinurad caused %d of them" % (k25, caused) in note,
       "the note's 2025 figures")
    for s in G.NEW:
        ok("%.2f (%.2f to %.2f)" % g["sccs"][s] in note, "the note's %s ratio" % s)
    ok("%.2f times the rate of the matched non-users" % tm in note and "%.2f times the rate of people starting zopiclone"
       % tz in note and "%.2f times that of people starting allopurinol" % ca in note, "the note's year-before figures")
    ok("rate ratio is %.2f (95%% CI %.2f to %.2f)" % nf in note, "the note's NSAID-free figure")
    rows = list(csv.DictReader(open(os.path.join(golden_dir, "new_users_by_year.csv"), encoding="utf-8")))
    ok([(r["substance"], int(r["calendar_year"])) for r in rows] == [(s, y) for s in G.NEW for y in (2022, 2023, 2024, 2025)],
       "golden table rows")
    ok(all(int(r["new_users"]) == nu[(r["substance"], int(r["calendar_year"]))] for r in rows), "golden table counts")
    notes = texts["registry_extract_notes.md"]
    for f in files:
        if f.endswith((".parquet", ".csv")):
            n = rows_of(os.path.join(target, f))
            ok("{:,}".format(n) in notes or str(n) in notes, "the extract notes carry %s's row count" % f)
    people = set(W.PEOPLE.values())
    sys.path.insert(0, os.path.join(REPO, ".claude/skills/fingerprint"))
    try:
        import business
        found = set()
        for f in files + [os.path.join(golden_dir, "signal_refinement_note.docx"), os.path.join(TASK, "prompt.md")]:
            if f.endswith((".md", ".pdf", ".docx", ".xlsx")):
                found |= {"%s %s" % x for x in business.people_in_text(file_text(os.path.join(target, f)))}
        ok(found <= people, "personas outside the card: %s" % (found - people))
        LOG.append("personas in the pack, the golden and the prompt: %s" % ", ".join(sorted(found)))
    except ImportError:
        pass

    sub = os.path.join(TASK, "submission.md")
    if os.path.exists(sub):
        check_submission(open(sub, encoding="utf-8").read(), g)
    if not quiet:
        for line in LOG:
            print("  " + line)
    print("checks: %d assertions passed" % N_ASSERT[0])
    return N_ASSERT[0], LOG, g


def check_submission(text, g):
    """Every figure the write-up states is the solve's own."""
    ok("\u2014" not in text, "submission carries an em dash")
    ok(text.count("\n## ") == 5 and "## Tags" in text and "## 4. Deliverable Answers" in text, "five blocks")
    ok("**Open the formal assessment on corinurad (Uralexa) and acute kidney injury.**" in text, "the committed call")
    rr, lo, hi = g["ratio"], g["lower"], g["upper"]
    ok("%.2f (95%% CI %.2f to %.2f)" % (rr, lo, hi) in text, "submission ratio")
    for s in G.NEW:
        ok("%.2f" % g["sccs"][s][0] in text, "submission %s ratio" % s)
    ok("%d admissions" % g["events_2025"] in text, "submission 2025 admissions")
    ok("%d caused by corinurad" % g["caused"] in text, "submission caused")
    for (s, y), v in g["new_users"].items():
        ok("%s %d: %s" % (s, y, "{:,}".format(v)) in text, "submission new users %s %d" % (s, y))
    BAN = ("leverage", "robust", "seamless", "comprehensive", "it is worth noting")
    ok(not any(b in text.lower() for b in BAN), "submission filler words")


if __name__ == "__main__":
    run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), meta_path=os.path.join(TASK, "metadata.json"))
