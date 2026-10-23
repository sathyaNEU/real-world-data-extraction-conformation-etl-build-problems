"""The ask cracker and mirror, run on the cut pack: the response that landed the call, ran the hygiene battery (key
uniqueness, exact duplicates, unmatched joins, fan-out) and executed every filed rule it points at (the analysis plan's
4.2 average and 5.1 response rates, the label units and serving sizes). Scores each ask figure against
generator/figures.json and prints the pair ceiling and the mirror's leakage.

    python3 task274/generator/cracker.py"""
from __future__ import annotations

import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as AS     # noqa: E402
import common as K    # noqa: E402
import pack as PK     # noqa: E402

REC, IF_, ASKW = 38.0, 7.0, 55.0
R_KEPT = 5.0          # recommendation weight a wrong call keeps


def battery(lines, status, scr):
    """What the hygiene battery finds in the asks' files: duplicate keys, exact duplicate rows, unmatched joins."""
    keys = collections.Counter((x["seqn"], x["line"]) for x in lines)
    exact = collections.Counter((x["seqn"], x["pid"], x["iu"], x["days"], x["qty"]) for x in lines)
    st_keys = collections.Counter(s["seqn"] for s in status)
    unmatched = [s for s in status if s["screener"] not in scr]
    return dict(dsq_key_dups=sum(v > 1 for v in keys.values()), dsq_exact_dups=sum(v > 1 for v in exact.values()),
                status_key_dups=sum(v > 1 for v in st_keys.values()), unmatched_screeners=len(unmatched))


def main():
    task = os.path.dirname(HERE)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    rd = PK.Read(os.path.join(task, "target"))
    lines = rd.supplements()
    status, scr = rd.status()
    print("battery on the asks' files:", battery(lines, status, scr))
    names = [n for _, n in K.COUNTIES]
    gold = dict(a1000=[fig["asks"]["supplements_1000"][n] for n in names],
                a2000=[fig["asks"]["supplements_2000"][n] for n in names],
                bi=[fig["asks"]["interview_rr"][n] for n in names], be=[fig["asks"]["exam_rr"][n] for n in names])
    a = AS.ask_a(status, lines, "cracker")
    b = AS.ask_b(status, scr, "cracker")
    crack = dict(a1000=a[1000.0], a2000=a[2000.0], bi=b["interview"], be=b["exam"])
    rows = []
    kept = 0
    total = 0
    for k, label in (("a1000", "A, at least 1,000 IU a day"), ("a2000", "A, at least 2,000 IU a day"),
                     ("bi", "B, interview response rate"), ("be", "B, examination response rate")):
        hit = sum(abs(x - y) < 0.05 for x, y in zip(crack[k], gold[k]))
        kept += hit
        total += len(names)
        off = [round(x - y, 1) for x, y in zip(crack[k], gold[k])]
        rows.append((label, hit, min(off), max(off)))
        print("%-32s cracker keeps %d of 8 (off %+.1f to %+.1f)" % (label, hit, min(off), max(off)))
    keep_c = kept / total
    # the mirror stops at the lot-and-analyzer rung on the call and takes the asks the cracker's way
    keep_m = keep_c
    C = REC + IF_ + ASKW * keep_c
    S = R_KEPT + IF_ + ASKW * keep_m
    print("cracker keeps %d of %d ask figures; mirror the same" % (kept, total))
    print("Pair ceiling: %.1f (cracker %.1f, mirror %.1f)" % ((C + S) / 2, C, S))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * keep_m))
    for mode in ("overclean",):
        a2 = AS.ask_a(status, lines, mode)
        b2 = AS.ask_b(status, scr, mode)
        h = sum(abs(x - y) < 0.05 for x, y in zip(a2[1000.0], gold["a1000"])) + \
            sum(abs(x - y) < 0.05 for x, y in zip(a2[2000.0], gold["a2000"])) + \
            sum(abs(x - y) < 0.05 for x, y in zip(b2["interview"], gold["bi"])) + \
            sum(abs(x - y) < 0.05 for x, y in zip(b2["exam"], gold["be"]))
        print("over-cleaner keeps %d of %d" % (h, total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
