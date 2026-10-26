"""The independent verifier. It reads only the shipped bundle under <task>/target and the claims in
generator/figures.json, and recomputes every graded figure from the files a solver gets.

Nothing here imports the world, the ledger or the asks: the point is to reach the same answers from the
pack alone, the way the judge does.

    python3 task184/generator/verify.py
"""
import csv
import datetime as dt
import json
import os
import sqlite3
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
UBIN, GBIN = 100, 1_000
MONITORED = ("EPOS", "ROUTE_DOCKET", "ROUTE_VAN", "AP_BATCH", "MANUAL")
N = [0]
FAIL = []


def ok(tag, cond, msg):
    N[0] += 1
    if not cond:
        FAIL.append("%s  %s" % (tag, msg))


def rows(name):
    with open(os.path.join(TARGET, name), encoding="utf-8") as fh:
        return [tuple(r) for r in csv.reader(fh)][1:]


def unit_map():
    """The twelve current unit codes, and the former codes the register and FY25 files carry."""
    m = {}
    for code, name, kind, county, former, eff, _note in rows("trading_unit_register.csv"):
        m[code] = code
        m[former] = code
    return m


def recover(k, f):
    """The per-posting rate that maximises the per-entry likelihood of 1 - (1 - r) ** k."""
    k = np.asarray(k, dtype=np.float64)
    f = np.asarray(f, dtype=np.int64)
    sizes, inv = np.unique(k.astype(np.int64), return_inverse=True)
    s = sizes.astype(np.float64)
    n = np.bincount(inv, minlength=s.size).astype(np.float64)
    hit = np.bincount(inv, weights=f, minlength=s.size)
    if hit.sum() == 0:
        return 0.0

    def score(r):
        q = (1.0 - r) ** s
        return float((hit * s * q / (np.maximum(1.0 - q, 1e-300) * (1.0 - r))).sum()
                     - ((n - hit) * s / (1.0 - r)).sum())

    lo, hi = 1e-10, 0.9
    for _ in range(72):
        mid = (lo + hi) / 2
        if -score(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main():
    claims = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    um = unit_map()

    # ------------------------------------------------ the call, from the extract and the register
    con = sqlite3.connect(os.path.join(TARGET, "drumcondra_gl_fy26.sqlite"))
    ent = con.execute("SELECT entry_no, unit_code, item_count FROM journal_entries").fetchall()
    flagged = {int(r[1]) for r in rows("monitoring_exceptions_fy26.csv")}
    by_unit = {}
    for entry_no, code, items in ent:
        u = um[code]
        d = by_unit.setdefault(u, {"k": [], "f": []})
        d["k"].append(int(items))
        d["f"].append(1 if entry_no in flagged else 0)
    ok("V1", len(by_unit) == 12, "the extract resolves to %d units, not twelve" % len(by_unit))

    raw_total = 0.0
    for u in sorted(by_unit):
        k, f = np.array(by_unit[u]["k"]), np.array(by_unit[u]["f"])
        v = recover(k, f) * k.sum()
        raw_total += v
        graded = int(round(v / UBIN) * UBIN)
        want = claims["call"]["unit_postings_tripped"][u]
        ok("V2", graded == want, "%s recomputes to %d, figures.json claims %d" % (u, graded, want))
        ok("V3", int(f.sum()) == claims["call"]["unit_entries_raised"][u],
           "%s raised %d entries, figures.json claims %d"
           % (u, int(f.sum()), claims["call"]["unit_entries_raised"][u]))
    group = int(round(raw_total / GBIN) * GBIN)
    ok("V4", group == claims["call"]["group_postings_tripped"],
       "the group figure recomputes to %d, figures.json claims %d"
       % (group, claims["call"]["group_postings_tripped"]))
    ok("V5", len(flagged) == claims["call"]["entries_raised_as_exceptions"],
       "the register holds %d entries, figures.json claims %d"
       % (len(flagged), claims["call"]["entries_raised_as_exceptions"]))
    ok("V6", sum(int(r[2]) for r in ent) == claims["call"]["postings_in_window"],
       "the extract holds %d postings, figures.json claims %d"
       % (sum(int(r[2]) for r in ent), claims["call"]["postings_in_window"]))
    ok("V7", len(ent) == claims["call"]["entries_in_window"],
       "the extract holds %d entries, figures.json claims %d"
       % (len(ent), claims["call"]["entries_in_window"]))
    # the rounded unit figures sum to the group's own rounded figure
    ok("V8", sum(claims["call"]["unit_postings_tripped"].values()) == group,
       "the rounded unit figures do not sum to the group figure")

    # the rungs, recomputed from the pack
    n, T = len(ent), sum(int(r[2]) for r in ent)
    nf = len(flagged)
    ok("V9", abs(claims["rungs"]["rung0_flagged_entries"] - nf) < 0.5, "rung 0 does not recompute")
    ok("V10", abs(claims["rungs"]["rung1_entry_rate_grossed_up"] - nf / n * T) < 1.0,
       "rung 1 does not recompute")
    kbar, p = T / n, nf / n
    ok("V11", abs(claims["rungs"]["rung2_inversion_on_mean_entry_size"]
                  - (1.0 - (1.0 - p) ** (1.0 / kbar)) * T) < 1.0, "rung 2 does not recompute")

    # ------------------------------------------------ ask 1
    accr = rows("payables_accruals_fy25.csv")
    superseded = {r[6] for r in accr if r[6]}
    sub, led = {}, {}
    for ref, unit, _p, _d, _s, amt, restates, posted in accr:
        if ref in superseded:
            continue
        sub[um[unit]] = sub.get(um[unit], 0.0) + float(amt)
        led[um[posted]] = led.get(um[posted], 0.0) + float(amt)
    for unit, acc, grni, total in rows("payables_control_account_fy25.csv"):
        u = um[unit]
        want = claims["asks"]["ask1"]["%s|subledger" % u]
        ok("V12", abs(round(sub.get(u, 0.0), 2) - want) < 0.02,
           "%s subledger recomputes to %.2f, figures.json claims %.2f" % (u, sub.get(u, 0.0), want))
        wd = claims["asks"]["ask1"]["%s|difference" % u]
        ok("V13", abs(round(float(total) - sub.get(u, 0.0), 2) - wd) < 0.02,
           "%s difference recomputes to %.2f, figures.json claims %.2f"
           % (u, float(total) - sub.get(u, 0.0), wd))

    # ------------------------------------------------ ask 2
    cal = {}
    for fy, p, a, b, _d, _w in rows("period_calendar.csv"):
        if fy == "FY25":
            cal[int(p)] = (dt.date.fromisoformat(a), dt.date.fromisoformat(b))
    def period_of(d):
        for p, (a, b) in cal.items():
            if a <= d <= b:
                return p
        return None
    takings = {}
    for unit, _till, bdate, _txn, val in rows("epos_till_takings_fy25.csv"):
        p = period_of(dt.date.fromisoformat(bdate))
        if p is None:
            continue
        key = (um[unit], (p - 1) // 3 + 1)
        takings[key] = takings.get(key, 0.0) + float(val)
    posted = {}
    for unit, p, val in rows("sales_control_account_fy25.csv"):
        key = (um[unit], (int(p) - 1) // 3 + 1)
        posted[key] = posted.get(key, 0.0) + float(val)
    for (u, q), t in sorted(takings.items()):
        gap = round(t - posted.get((u, q), 0.0), 2)
        want = claims["asks"]["ask2"]["%s-Q%d|gap" % (u, q)]
        ok("V14", abs(gap - want) < 0.02,
           "%s Q%d gap recomputes to %.2f, figures.json claims %.2f" % (u, q, gap, want))

    # ------------------------------------------------ ask 3
    scope = {}
    for unit, p, stream, entries, _post, _val in rows("gl_period_summary_fy25.csv"):
        if stream in MONITORED:
            key = (um[unit], int(p))
            scope[key] = scope.get(key, 0) + int(entries)
    ev = {}
    for unit, p, _runs, evald, _c, _v, _h in rows("monitoring_run_log_fy25.csv"):
        ev[(um[unit], int(p))] = int(evald)
    for key, s in sorted(scope.items()):
        u, p = key
        got = max(s - ev.get(key, 0), 0)
        want = claims["asks"]["ask3"]["%s-P%02d" % (u, p)]
        ok("V15", got == want,
           "%s P%02d recomputes to %d, figures.json claims %d" % (u, p, got, want))

    # ------------------------------------------------ the input gates, on the shipped folder
    files = sorted(os.listdir(TARGET))
    ok("V16", len(files) >= 10, "the pack has %d files" % len(files))
    ok("V17", len({os.path.splitext(f)[1].lower() for f in files}) >= 3,
       "the pack has fewer than three formats")
    ok("V18", len(ent) >= 25000, "no shipped file carries 25,000 rows")
    md = json.load(open(os.path.join(TARGET, "metadata.json"), encoding="utf-8"))
    ok("V19", len(md.get("distractors", [])) >= 2, "metadata.json declares fewer than two distractors")
    for d in md.get("distractors", []):
        ok("V20", d in files, "declared distractor %s is not in the pack" % d)
    ok("V21", md["provenance"]["licence"].startswith("CC0"), "no licence recorded")

    print("task184 verify: %d assertions, %d FAIL" % (N[0], len(FAIL)))
    for f in FAIL:
        print("  FAIL %s" % f)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
