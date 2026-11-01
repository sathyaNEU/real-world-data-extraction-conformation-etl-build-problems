"""Design-time screen for the Shock and Back-test lines: what a solver sees ward by ward without the decisive step."""
import csv
import sys
from collections import defaultdict

import numpy as np

import solve as S


def main(t):
    D = S.solve(t, drop_works=False)
    ward_of = D["ward_of"]
    # every-pair annual changes, 2016 to 2026, against the official city index's annual change
    off = {}
    with open(S.os.path.join(t, "harrowmere_official_hpi_2015-2026.csv")) as f:
        rows = list(csv.DictReader(f))
    lv = defaultdict(list)
    for r in rows:
        lv[int(r["Date"][-4:])].append(float(r["Index"]))
    city = {y: 100 * (np.mean(lv[y]) / np.mean(lv[y - 1]) - 1) for y in range(2016, 2027)}
    print("official city change:", " ".join("%d %.1f" % (y, v) for y, v in city.items()))
    for w, lev in sorted(D["index"].items()):
        ch = [S.change(lev, y) for y in range(2016, 2027)]
        print("%-14s %s" % (w, " ".join("%5.1f" % c for c in ch)))
    # works completed per thousand houses, 2025 and 2026, by ward; additional entries 2024-2025 by ward
    reg = S.load_register(t)
    houses = defaultdict(set)
    for x in D["recs"]:
        if x["ptype"] in "DST":
            houses[ward_of.get(S.norm_pc(x["postcode"]))].add(S.addr_key(x["paon"], x["saon"], x["postcode"]))
    works = defaultdict(int)
    for w in reg:
        if w["completed"].year in (2025, 2026) and w["created"] == 0 and not w["lost"] and not w["lost_blank"]:
            works[ward_of.get(S.norm_pc(w["postcode"]))] += 1
    b = defaultdict(int)
    for x in D["recs"]:
        if x["cat"] == "B" and x["date"].year in (2024, 2025) and x["ptype"] in "DSTF":
            b[ward_of.get(S.norm_pc(x["postcode"]))] += 1
    print("works per 1,000 houses 2025-26 and additional entries 2024-25:")
    for w in sorted(works):
        print("  %-14s %6.1f %5d" % (w, 1000.0 * works[w] / max(1, len(houses[w])), b[w]))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else S.TARGET)
