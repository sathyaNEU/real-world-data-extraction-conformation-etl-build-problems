"""task244 ask layer against the careful solver's routes, on the cut pack.

    python3 task244/generator/ceiling.py [pack]

pack is target.zip (the default, the archive that ships) or a folder holding the pack's files. The asks give 36
figures: Ask A, each district's match rate (per cent, one decimal) and the persons it is based on (whole numbers), over
the year's four quarter pairs (methodology note 8.2); Ask B, each district's mean days from interview to reinterview
(one decimal) for the interviews of 2027 (8.3). A figure is kept when it equals figures.json's at the prompt's rounding.

The cracker is the careful solver, never a narrowed one. It lands the call (the reconciled reinterview's error taken out
of Table F1 at both quarters), runs the hygiene battery on the five person files and the fieldwork log (exact duplicate
rows; key uniqueness; rows identical in every field but one; one person per sex and month and year of birth in a
dwelling's quarter, the attributes section 8.2's own link reads; each dwelling's visits rising one a quarter; the codes
against the gazetteer; both clocks on a log row, with their weekday profile; the log's dates against the protocol's
14-day window, which every result in the results file is inside; one completing call a household), executes every
filed rule as worded (section 6's districts as from 1 April 2027, 8.2's link and each person once, 8.3's population,
anchor and quarters, protocol 5's window) and takes each ask on its natural read. Its code is written here, apart from
solve.py. The mirror stops at the default path (the two recorded statuses' predictive values multiplied, every rate at
18.1 per cent, no warning) and, the asks being decoupled from the call, takes them as the cracker does. The full includer
is solve.py's golden route and has to give back figures.json exactly (the route code's control). The stage-3 cracker of
pair.py (identical rows once, the call's date as the log records it) is printed beside it for the record: it skips one
battery item on each ask.

The pair is the ask sheet's formula: 38 recommendation and components, 7 instruction following, 55 asks over the 36
figures, the response off the call keeping r of the 38, measured from the per-rate criteria the default path keeps (the
eleven rates it rightly leaves unwarned) and printed beside the comparable r = 5; Pair ceiling is the worse. Exit 0 when
the gate holds (the cracker keeps no ask figure, the pair at or under 60, the mirror under half the ask weight and two
careful responses on the call under 70), 2 when it does not, 1 when a control fails. The script modifies nothing and
never runs inside the build."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B      # noqa: E402  (file names only)
import solve           # noqa: E402  (the full includer: the golden route)
import verify as V     # noqa: E402  (the bundle-only call reader)

TASK = os.path.dirname(HERE)
PAIR_GATE = 60.0
QUARTERS = ["2026Q4", "2027Q1", "2027Q2", "2027Q3", "2027Q4"]
DCODES = ["D%02d" % i for i in range(1, 13)]
WINDOW = 14                                      # protocol section 5
REC, INS, ASK = 38.0, 7.0, 55.0


# ------------------------------------------------------------------ the pack
def pack_dir(arg):
    src = arg or os.path.join(TASK, "target.zip")
    if os.path.isdir(src):
        files = sorted(os.listdir(src))
        h = hashlib.sha256("".join(hashlib.sha256(open(os.path.join(src, f), "rb").read()).hexdigest()
                                   for f in files).encode()).hexdigest()
        return src, None, "folder %s (%d files, sha256 of the file digests %s)" % (src, len(files), h[:16])
    tmp = tempfile.mkdtemp(prefix="ceiling244-")
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    inner = os.path.join(tmp, "target")
    folder = inner if os.path.isdir(inner) else tmp
    md5 = hashlib.md5(open(src, "rb").read()).hexdigest()
    return folder, tmp, "%s (%d files, md5 %s)" % (src, len(os.listdir(folder)), md5)


# ------------------------------------------------------------------ the careful solver's reads
def person_files(folder):
    fs = [B.FILES["persons_" + q.lower()] for q in QUARTERS]
    return pd.concat([pd.read_csv(os.path.join(folder, f), dtype={"dwelling": str}) for f in fs], ignore_index=True)


def gazetteer(folder):
    gz = pd.read_csv(os.path.join(folder, B.FILES["gazetteer"]))
    moved = gz[gz.district_before.notna()]
    return {(r.district_before, int(r.ea_before)): (r.district, dt.date.fromisoformat(r.effective))
            for r in moved.itertuples()}


def districts_2027(df, gz):
    """section 6: a record dated before the boundary change carries the codes then in force; the gazetteer maps them"""
    out = []
    for d, e, day in zip(df.district, df.ea, df.int_date):
        m = gz.get((d, int(e)))
        out.append(m[0] if m and dt.date.fromisoformat(day) < m[1] else d)
    return out


def battery(df, log, results, gz):
    """the hygiene battery a careful analyst runs before counting; each line is (check, what it finds), and the frame
    the asks are then taken on"""
    lines = []
    n0 = len(df)
    ex = df.drop_duplicates(ignore_index=True)
    lines.append(("exact duplicate rows", "%d rows repeat another exactly (%s), dropped" % (
        n0 - len(ex), ", ".join("%s %s area %s" % k for k in sorted(set(zip(
            df[df.duplicated()].quarter, df[df.duplicated()].district, df[df.duplicated()].ea.astype(str))))))))
    key = ["quarter", "dwelling", "hh", "line"]
    lines.append(("key uniqueness (quarter, dwelling, household, line)",
                  "%d keys repeat after the exact duplicates go" % int(ex.duplicated(key).sum())))
    # rows identical in every field but one: each field left out in turn
    hits = {}
    for c in ex.columns:
        rest = [x for x in ex.columns if x != c]
        k = int(ex.duplicated(rest).sum())
        if k:
            hits[c] = k
    lines.append(("rows identical in every field but one", "; ".join("%d differ only in %s" % (v, k) for k, v in
                                                                      sorted(hits.items())) or "none"))
    person = ["quarter", "dwelling", "sex", "birth_year", "birth_month"]
    dup = ex[ex.duplicated(person, keep=False)]
    lines.append(("one person per sex and month and year of birth in a dwelling's quarter (8.2's own attributes)",
                  "%d records in %d dwellings break it, every pair in two households of one dwelling, one household "
                  "number never seen at another visit" % (len(dup), dup.dwelling.nunique())))
    # keep, of each such pair, the record whose household the dwelling's other visits carry
    seen = ex.groupby(["dwelling", "hh"]).quarter.nunique()
    ex = ex.assign(_other=[seen.get((d, h), 0) > 1 for d, h in zip(ex.dwelling, ex.hh)])
    ex = ex.sort_values(person + ["_other", "hh"], ascending=[True] * 5 + [False, True], kind="mergesort")
    clean = ex.drop_duplicates(person).sort_index().drop(columns="_other").reset_index(drop=True)
    lines.append(("  the copies taken once", "%d records dropped, %d kept" % (len(ex) - len(clean), len(clean))))
    qi = clean.quarter.map({q: i for i, q in enumerate(QUARTERS)})
    clean = clean.assign(qi=qi)
    jumps = 0
    for (dw, hh), g in clean.groupby(["dwelling", "hh"]):
        v = g.drop_duplicates("qi").sort_values("qi")
        jumps += int(((v.visit.diff() != v.qi.diff()) & v.qi.diff().notna()).sum())
    lines.append(("each household's visit rising one a quarter", "%d breaks" % jumps))
    clean = clean.assign(d27=districts_2027(clean, gz))
    lines.append(("district codes against the gazetteer (section 6)", "%d records dated before 1 April 2027 under the "
                                                                      "codes then in force, mapped to the 2027 districts"
                  % int((clean.d27 != clean.district).sum())))
    ad = log.attempt_date.map(dt.date.fromisoformat)
    vd = log.visit_start.str[:10].map(dt.date.fromisoformat)
    same = ad == vd
    first_off = log.assign(vd=vd)[~same].groupby("supervisor").vd.min()
    last_on = log.assign(vd=vd)[same].groupby("supervisor").vd.max()
    lines.append(("both clocks on a log row (the call's date and the form's start)",
                  "they agree on %d calls and differ on %d; each supervisor's calls agree up to a date and differ from "
                  "the next (%s); every differing call's attempt_date is a %s, %d to %d days after its visit_start" % (
                      int(same.sum()), int((~same).sum()),
                      ", ".join("%s to %s, from %s" % (s, last_on[s], first_off[s]) for s in sorted(first_off.index)),
                      "Friday" if set(d.weekday() for d in ad[~same]) == {4} else "mix of weekdays",
                      int(min((a - v).days for a, v in zip(ad[~same], vd[~same]))),
                      int(max((a - v).days for a, v in zip(ad[~same], vd[~same]))))))
    done = log[log.result == "completed"].assign(ad=ad, vd=vd)
    per = done.groupby(["quarter", "dwelling", "hh"]).size()
    lines.append(("one completing call a household", "%d households with more than one" % int((per > 1).sum())))
    rr = results.merge(clean[["quarter", "dwelling", "hh", "line", "int_date"]], on=["quarter", "dwelling", "hh", "line"])
    rr = rr.merge(done[["quarter", "dwelling", "hh", "ad", "vd"]], on=["quarter", "dwelling", "hh"])
    iday = rr.int_date.map(dt.date.fromisoformat)
    by_a = sum((a - i).days > WINDOW for a, i in zip(rr.ad, iday))
    by_v = sum((v - i).days > WINDOW for v, i in zip(rr.vd, iday))
    lines.append(("the log against protocol 5's window (every result is a reinterview inside it)",
                  "of the %d results, %d fall outside 14 days by the call's date as the log records it, %d by the form's "
                  "start" % (len(rr), by_a, by_v)))
    return lines, clean


# ------------------------------------------------------------------ the asks, the careful solver's own code
def match_rates(df):
    """8.2 as worded: of the persons interviewed in a quarter in a dwelling due another visit (its first, second or
    third), those interviewed again at the dwelling's next visit, found on the dwelling, household and line numbers or,
    in a household new to the dwelling, on sex and month and year of birth; each person once in each pair"""
    out = {d: [0, 0] for d in DCODES}
    for qi in range(len(QUARTERS) - 1):
        a = df[(df.qi == qi) & (df.visit <= 3)]
        b = df[df.qi == qi + 1]
        lines = set(zip(b.dwelling, b.hh, b.line))
        before = set(zip(df[df.qi == qi].dwelling, df[df.qi == qi].hh))
        nb = b[[(d, h) not in before for d, h in zip(b.dwelling, b.hh)]]
        births = set(zip(nb.dwelling, nb.sex, nb.birth_year, nb.birth_month))
        for d, dw, hh, ln, sx, by, bm in zip(a.d27, a.dwelling, a.hh, a.line, a.sex, a.birth_year, a.birth_month):
            out[d][0] += ((dw, hh, ln) in lines) or ((dw, sx, by, bm) in births)
            out[d][1] += 1
    return {d: (100.0 * v[0] / v[1], v[1]) for d, v in out.items()}


def mean_days(df, log, clock="visit_start"):
    """8.3 as worded: for the persons whose household reinterview was completed, in the window or after it, for the
    interviews of 2027Q1 to 2027Q4, the days from each person's own interview to the supervisor's completing visit"""
    done = log[(log.result == "completed") & log.quarter.isin(QUARTERS[1:])].sort_values("attempt")
    done = done.groupby(["quarter", "dwelling", "hh"]).tail(1)
    day = done.visit_start.str[:10] if clock == "visit_start" else done.attempt_date
    done = done.assign(vday=day.map(dt.date.fromisoformat))
    p = df.merge(done[["quarter", "dwelling", "hh", "vday"]], on=["quarter", "dwelling", "hh"])
    p = p.assign(days=[(v - dt.date.fromisoformat(i)).days for v, i in zip(p.vday, p.int_date)])
    g = p.groupby("d27").days.mean()
    return {d: float(g[d]) for d in DCODES}


def route(df, log, clock="visit_start"):
    m, dd = match_rates(df), mean_days(df, log, clock)
    out = {}
    for d in DCODES:
        out[("A rate", d)] = round(m[d][0], 1)
        out[("A persons", d)] = m[d][1]
        out[("B days", d)] = round(dd[d], 1)
    return out


def gold_figures():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    g = {}
    for x in figs["match"]:
        g[("A rate", x["district"])] = x["rate"]
        g[("A persons", x["district"])] = x["due"]
    for x in figs["days"]:
        g[("B days", x["district"])] = x["mean"]
    return figs, g


def kept(fig, gold):
    by = {}
    for k in gold:
        by.setdefault(k[0], 0)
        by[k[0]] += abs(fig.get(k, -1e9) - gold[k]) < 1e-9
    return by, sum(by.values())


def show(name, fig, gold):
    by, k = kept(fig, gold)
    print("  %-86s %2d of %d  (rates %d, persons %d, days %d)" % (name, k, len(gold), by["A rate"], by["A persons"],
                                                                   by["B days"]))
    return k


def pair(kc, km, n, r):
    c = REC + INS + ASK * kc / n
    s = r + INS + ASK * km / n
    return c, s, (c + s) / 2.0


# ------------------------------------------------------------------ the run
def main(arg=None):
    folder, scratch, stamp = pack_dir(arg)
    try:
        return run(folder, stamp)
    finally:
        if scratch:
            shutil.rmtree(scratch)


def run(folder, stamp):
    print("pack: " + stamp)
    figs, gold = gold_figures()
    n = len(gold)
    # the call
    shares, published, C, M = V.call(folder)
    warned = sorted(k for k, v in shares.items() if v >= 1 / 3)
    cells = {(c["district"], c["key"]): c for c in figs["cells"]}
    on_call = warned == sorted(k for k, c in cells.items() if c["warning"]) and all(
        abs(round(100 * shares[k], 1) - cells[k]["not_real"]) < 1e-9 for k in cells)
    ppv = np.diag(C) / C.sum(0)
    r0 = {k: 1 - ppv[0] * ppv[1] for k in cells}
    m_warned = sorted(k for k, v in r0.items() if v >= 1 / 3)
    print("cracker's call (the error taken out at both quarters): %d of 24 rates warned, every share the golden's (%s)"
          % (len(warned), "lands" if on_call else "MISSES"))
    print("mirror's call (the default path, the predictive values multiplied): every rate at %.1f per cent, %d warned "
          "(%s)" % (100 * list(r0.values())[0], len(m_warned), "off the call" if m_warned != warned else "ON THE CALL"))
    if not on_call or m_warned == warned:
        print("CONTROL FAILED: the rows below assume the cracker on the call and the mirror off it")
        return 1
    right = sum((k in m_warned) == (k in warned) for k in cells)
    same = sum(round(100 * r0[k], 1) == round(100 * shares[k], 1) for k in cells)
    r_meas = round(REC * 0.75 * (right + same) / 48.0, 1)
    print("  the mirror keeps %d of the 24 warnings (the rates it rightly leaves clear) and %d of the 24 shares: r = %.1f"
          % (right, same, r_meas))

    # the full includer
    from types import SimpleNamespace
    A = solve.answer(folder, B.FILES)
    full = {}
    for d in DCODES:
        full[("A rate", d)] = round(A["match"][d][1], 1)
        full[("A persons", d)] = A["match"][d][2]
        full[("B days", d)] = round(A["days"][d][1], 1)
    bad = [k for k in gold if abs(full[k] - gold[k]) > 1e-9]
    if bad:
        print("CONTROL FAILED: the full includer does not reproduce figures.json at %s" % bad)
        return 1
    print("full includer (solve.py's golden route): reproduces figures.json exactly, %d of %d" % (n, n))

    # the battery
    df = person_files(folder)
    log = pd.read_csv(os.path.join(folder, B.FILES["reint_log"]), dtype={"dwelling": str})
    results = pd.read_csv(os.path.join(folder, B.FILES["reint_results"]), dtype={"dwelling": str})
    gz = gazetteer(folder)
    lines, clean = battery(df, log, results, gz)
    print("\nthe careful solver's hygiene battery:")
    for check, found in lines:
        print("  %s: %s" % (check, found))

    # the routes
    print("\nroutes, ask figures kept of %d:" % n)
    cracker = route(clean, log, "visit_start")
    kc = show("cracker: on the call, the battery, every filed rule as worded, each ask's natural read", cracker, gold)
    km = show("mirror: the default path on the call, the asks read as the cracker reads them", cracker, gold)
    exact = df.drop_duplicates(ignore_index=True)
    exact = exact.assign(qi=exact.quarter.map({q: i for i, q in enumerate(QUARTERS)}), d27=districts_2027(exact, gz))
    print("  the stage-3 cracker (pair.py) and its halves, each a battery item skipped:")
    k_old = show("    identical rows once, the call's date as the log records it (pair.py's cracker)",
                 route(exact, log, "attempt_date"), gold)
    show("    identical rows once, the form's start", route(exact, log, "visit_start"), gold)
    show("    the copies taken once, the call's date as the log records it", route(clean, log, "attempt_date"), gold)
    raw = df.assign(qi=df.quarter.map({q: i for i, q in enumerate(QUARTERS)}), d27=districts_2027(df, gz))
    show("    the rows as received, the form's start", route(raw, log, "visit_start"), gold)

    print("\nthe cracker's figures against figures.json (stated, golden):")
    for k in gold:
        print("  %-10s %-4s %-10s %-10s %s" % (k[0], k[1], cracker[k], gold[k],
                                              "kept" if abs(cracker[k] - gold[k]) < 1e-9 else "miss"))
    worst, both = [], []
    for name, r in (("measured r = %.1f" % r_meas, r_meas), ("comparable r = 5", 5.0)):
        c, s, p = pair(kc, km, n, r)
        worst.append(p)
        both.append(c)
        print("\nthe sheet's formula (38, 7, 55 over %d figures), %s: cracker %.1f, mirror %.1f, pair %.1f; two careful "
              "responses on the call %.1f each" % (n, name, c, s, p, c))
        print("  (pair.py's narrowed cracker, %d of %d, would give %.1f)" % (k_old, n, pair(k_old, k_old, n, r)[2]))
    leak = 100.0 * km / n
    pc = max(worst)
    print("\nCracker keeps: %d of %d ask figures" % (kc, n))
    print("Mirror leakage: %.1f per cent of ask weight" % leak)
    print("Pair ceiling: %.1f (the worse of the measured pair on either r)" % pc)
    ok = kc == 0 and pc <= PAIR_GATE and leak < 50.0 and max(both) < 70.0
    print("gate %s: it needs the cracker to keep no ask figure, the pair at or under %.0f, the mirror's leakage under 50 "
          "per cent and two careful responses on the call under 70" % ("HOLDS" if ok else "FAILS", PAIR_GATE))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
