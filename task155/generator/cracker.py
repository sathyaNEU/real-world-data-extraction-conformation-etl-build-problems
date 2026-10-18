"""The cracker sheet, measured: both cracker paths run on the cut pack (target/) and scored figure by figure against
the goldens in figures.json, with the mirror leakage, the pair ceiling on each path and the blind-response test.

    python3 task155/generator/cracker.py            prints the sheet (checks.py runs it on every build)

The cracker landed the call, ran the hygiene battery and executed every filed rule. It folds each shift's daily
call-ins one of two ways: on the shift's identity (store, date, times, reason and absent payroll number), or by
telling each re-raise by its 07:00 raise, an absence's two reports one shift as the notes say. Either way it voids a
given-back fill, reads store dates and paid hours, and takes a filler's home store from the payroll cost centre on the
shift date, starting from the payroll number KWS holds and going to an earlier one only when that number has no row
for the date. A third row, for the record, runs the round-2 judge's own route (open lines counted from the day's
postings, give-backs looked for on open-line fills, the home store from the first payroll row covering the date). The
mirror stops at the most attractive wrong rung (R2, Werribee) and runs the same ask paths, so it keeps what the cracker
keeps."""
from __future__ import annotations

import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A    # noqa: E402
import calc as C    # noqa: E402

PATHS = (("the shift-identity fold", dict(dedup="keysdrops"), dict(dedup="keysdrops", home_rule="newest")),
         ("the 07:00 re-raise chain", dict(dedup="raise"), dict(dedup="raise", home_rule="newest")))
RECORD = (("the round-2 judge's route", dict(dedup="raise", gb_opn_only=True),
           dict(dedup="raise", gb_opn_only=True, home_rule="first_row")),)


def _key(name):
    return name.lower().replace(" ", "_")


def golden_vectors(B, F):
    names = {l: B.loc_store[l] for l in B.locs}
    ga = [F["A_%s_%s" % (k, _key(names[l]))] for l in B.locs for k in ("put_out", "covered", "uncovered")]
    gb = [F["B_%s_%s" % (k, _key(names[l]))] for l in B.locs for k in ("imports", "exports")]
    return ga, gb


def kept(v, g):
    return sum(abs(x - y) < 0.05 for x, y in zip(v, g))


def measure(task=None):
    task = task or os.path.dirname(HERE)
    B = C.load(os.path.join(task, "target"))
    F = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    ga, gb = golden_vectors(B, F)
    out = collections.OrderedDict()
    for label, ka_, kb_ in PATHS + RECORD:
        a = A.ask_a(B, **ka_)
        b = A.ask_b(B, **kb_)
        va = [round(a[l][k], 1) for l in B.locs for k in ("put_out", "covered", "uncovered")]
        vb = [round(b[l][k], 1) for l in B.locs for k in ("imports", "exports")]
        ka, kb = kept(va, ga), kept(vb, gb)
        cols = [kept(va[j::3], ga[j::3]) for j in range(3)]
        lk = (ka + kb) / 40.0
        c_ = 38 + 7 + 55 * lk
        s_ = 5 + 7 + 55 * lk
        out[label] = dict(A=ka, B=kb, A_cols=cols, kept=ka + kb, mirror=100.0 * lk, C=c_, S=s_, pair=(c_ + s_) / 2,
                          record=label in dict((r[0], 1) for r in RECORD))
    # the blind-response test on the widest graded component (Table 1) and on Table 2
    win = A.WINDOW
    hrs = collections.Counter()
    fil = collections.Counter()
    cnt = collections.Counter()
    for x in A._reg(B):
        if win[0] <= x["d"] <= win[1]:
            h = C.paid_min(x["span"]) / 60.0
            hrs[x["loc"]] += h
            cnt[x["loc"]] += 1
            fil[x["loc"]] += x["outcome"] == "FILLED"
    flat = []
    for l in B.locs:
        share = fil[l] / cnt[l] if cnt[l] else 0.0
        flat += [round(hrs[l], 1), round(hrs[l] * share, 1), round(hrs[l] * (1 - share), 1)]
    blind = dict(rate_A=kept(flat, ga), nil_A=kept([0.0] * 24, ga), nil_B=kept([0.0] * 16, gb),
                 const_A=max(kept([v] * 24, ga) for v in ga), const_B=max(kept([v] * 16, gb) for v in gb))
    return out, blind


def sheet(task=None):
    out, blind = measure(task)
    lines = ["Cracker sheet, measured on the cut pack by generator/cracker.py", ""]
    for label, r in out.items():
        lines.append("%-27s Ask A kept %2d of 24 (put out %d, covered %d, uncovered %d); Ask B kept %2d of 16; "
                     "%2d of 40, mirror leakage %.1f per cent; C %.1f, S %.1f, pair %.1f%s"
                     % (label, r["A"], r["A_cols"][0], r["A_cols"][1], r["A_cols"][2], r["B"], r["kept"], r["mirror"],
                        r["C"], r["S"], r["pair"], " (for the record)" if r["record"] else ""))
    lines.append("")
    lines.append("blind responses: one register rate on the register's row hours %d of 24; every cell nil %d of 24 and "
                 "%d of 16; the best constant %d of 24 and %d of 16"
                 % (blind["rate_A"], blind["nil_A"], blind["nil_B"], blind["const_A"], blind["const_B"]))
    text = "\n".join(lines) + "\n"
    return out, blind, text


if __name__ == "__main__":
    print(sheet()[2], end="")
