"""The pair ceiling, run on the cut pack (supplemental-stumping Part 0 weights: 38, 7, 55). The asks are the 36 cells of
fiscal 2026 main break repairs by service centre and month (Item 201) and the 16 cells of fiscal 2026 restoration by
surface type and quarter (Items 301 to 305), 52 ask figures; a hit only when exact at the stated rounding.

  cracker   lands the call; cancelled orders out, every REP and REPC row a break (Item 201); every estimate
            reconciled one to one to the gross amount paid, the latest (or first) revision where no voucher matches
  mirror    the record's rate (misses the call); every REP and REPC row; the latest revision of each estimate
  readers   the other routes priced: crew REP rows only, the crew yard for the centre, one break per asset and
            reported time, the crew's completion date, per asset and initiated date; the first revision, every
            revision, the estimate's month for the quarter

    python3 ceiling.py <target>"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc                 # noqa: E402


def r10(x):
    return int(10 * round(x / 10.0))


def keep(P, target, a_route, b_route, gA, gB):
    a = calc.ask_breaks(P, a_route)
    b = calc.ask_restoration(target, b_route)
    ka = sum(1 for k in gA if a[k] == gA[k])
    kb = sum(1 for k in gB if r10(b[k]) == r10(gB[k]))
    return ka, kb


def main(target):
    P = calc.Pack(target)
    gA = calc.ask_breaks(P)
    gB = calc.ask_restoration(target)
    n = len(gA) + len(gB)
    rows = {
        "cracker": ("rows", "one_to_one_latest"),
        "cracker, first revision where no voucher matches": ("rows", "one_to_one_first"),
        "mirror": ("rows", "latest"),
        "reader: crew REP rows, latest revision": ("rep_only", "latest"),
        "reader: crew yard centre, latest revision": ("golden_yard", "latest"),
        "reader: asset and reported time, latest revision": ("asset_reported", "latest"),
        "reader: crew completion date, first revision": ("first_row", "first"),
        "reader: asset and initiated date, every revision": ("asset_initiated", "all"),
        "reader: every row, estimate month quarter": ("rows", "golden_period"),
    }
    res = {}
    for k, (ra, rb) in rows.items():
        ka, kb = keep(P, target, ra, rb, gA, gB)
        res[k] = (ka, kb)
        print("%-52s Item 201 %2d of %d, Items 301-305 %2d of %d" % (k, ka, len(gA), kb, len(gB)))
    Lc = max(sum(res["cracker"]), sum(res["cracker, first revision where no voucher matches"])) / n
    Ls = sum(res["mirror"]) / n
    C_score = 38 + 7 + 55 * Lc
    S_score = 5 + 7 + 55 * Ls
    pair = (C_score + S_score) / 2
    print("cracker keeps %d of %d (%.1f), mirror keeps %d of %d (%.1f): pair ceiling %.1f, mirror leakage %.1f per cent of ask weight"
          % (round(Lc * n), n, C_score, sum(res["mirror"]), n, S_score, pair, 100.0 * Ls))
    return pair


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
