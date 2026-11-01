"""The ask layer's cracker and mirror sheets, scored on the cut pack (task133/target by default).

Each ask has handling stops: complete pipelines a competent response files. The cracker lands the main call and
takes the best stop it reaches without the ask's silent device (it runs the hygiene battery: pairs the agency's
upload with its remittance, applies the filed WHAT on recoveries, walks grades through the override log, maps merged
customer numbers, reads both default registers). The mirror stops at the main call's most attractive wrong rung and
handles the asks the same way (the asks are decoupled from the call). Pair = mean of
C = 38 + 7 + 55 Lc and S = 5 + 7 + 55 Ls, where L is the share of ask figures kept.
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import results as R  # noqa: E402

ASK_W = 55.0


def a_cells(net):
    return {k: R.rhu(v / 1e3, 0) for k, v in net.items()}


def b_cells(raw):
    out = {}
    for k, (n, d) in raw.items():
        out[("k", k)] = d
        out[("share", k)] = R.rhu(100.0 * d / n, 1)
    return out


def stops(tdir):
    A = {
        "A0 natural read (every receipt row, before write-off too, personal cases unmatched)":
            dict(guarantors=False, agency_upload=True, pre_writeoff=True),
        "A1 battery run (agency upload paired off, receipts after write-off only, personal cases unmatched)":
            dict(guarantors=False, agency_upload=False, pre_writeoff=False),
        "A2 agency gross kept beside remittance, guarantors linked":
            dict(guarantors=True, agency_upload=True, pre_writeoff=False),
        "golden": dict(guarantors=True, agency_upload=False, pre_writeoff=False),
    }
    B = {
        "B0 natural read (model grade, business register, numbers as recorded)":
            dict(group_by_facility=False, rural=False, merges=False, overrides=False),
        "B1 battery run (overrides in force, both registers, merge log, numbers as recorded)":
            dict(group_by_facility=False, rural=True, merges=True, overrides=True),
        "B2 facilities mapped but the rural register left out":
            dict(group_by_facility=True, rural=False, merges=True, overrides=True),
        "golden": dict(group_by_facility=True, rural=True, merges=True, overrides=True),
    }
    a = {k: a_cells(R.ask_a_detail(tdir, **kw)["net"]) for k, kw in A.items()}
    b = {k: b_cells(R.ask_b_raw(tdir, **kw)) for k, kw in B.items()}
    return a, b


def score(cells, gold):
    return sum(1 for k in gold if cells[k] == gold[k]), len(gold)


def main(tdir):
    a, b = stops(tdir)
    ga, gb = a["golden"], b["golden"]
    print("ask A stops (12 figures):")
    for k, v in a.items():
        h, n = score(v, ga)
        print("  %-100s keeps %2d of %d" % (k, h, n))
    print("ask B stops (10 figures):")
    for k, v in b.items():
        h, n = score(v, gb)
        print("  %-100s keeps %2d of %d" % (k, h, n))
    ca, _ = score(a["A1 battery run (agency upload paired off, receipts after write-off only, personal cases unmatched)"], ga)
    cb, _ = score(b["B1 battery run (overrides in force, both registers, merge log, numbers as recorded)"], gb)
    tot = len(ga) + len(gb)
    lc = (ca + cb) / tot
    ls = lc
    C = 38 + 7 + ASK_W * lc
    S = 5 + 7 + ASK_W * ls
    print("cracker keeps %d of %d ask figures (%.1f per cent of ask weight); mirror the same" % (ca + cb, tot, 100 * lc))
    print("C = %.1f, S = %.1f, pair ceiling = %.1f; mirror leakage = %.1f per cent" % (C, S, (C + S) / 2, 100 * ls))
    # the best response that also finds one silent device
    best = max(score(a["golden"], ga)[0] + cb, ca + score(b["golden"], gb)[0])
    lc2 = best / tot
    C2 = 38 + 7 + ASK_W * lc2
    print("if the cracker also finds one silent device: keeps %d of %d, C = %.1f, pair = %.1f" % (best, tot, C2, (C2 + S) / 2))
    z = os.path.join(os.path.dirname(tdir.rstrip("/")), "target.zip")
    if os.path.exists(z):
        print("measured on target.zip sha256 %s" % hashlib.sha256(open(z, "rb").read()).hexdigest()[:16])
    return dict(pair=(C + S) / 2, mirror=100 * ls, cracker_keep=ca + cb, total=tot)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
