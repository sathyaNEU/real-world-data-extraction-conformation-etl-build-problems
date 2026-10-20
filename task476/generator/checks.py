"""The generator's checks, on the cut pack and the generator's clean truth: the three rules (the analyst test executed),
the ladder, the semantic fork table (SF1 to SF10), the bins, the asks' devices and hazards, the input gates."""
import json
import math
import os

import acs as A
import bundle as B
import geo as G
import methods as M
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
GOLD = ["Dunmore Heights", "Kestrel Park"]
DEFAULT = ["Dunmore Heights", "Linden Row"]


def main(target, gdir, x):
    fails = []
    n = [0]

    def check(label, cond, detail=None):
        n[0] += 1
        print("%s  %s%s" % ("ok  " if cond else "FAIL", label, "" if cond or detail is None else "  [%s]" % (detail,)))
        if not cond:
            fails.append(label)

    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    rows_big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8", errors="ignore")) - 1
                   for f in files if f.endswith((".csv", ".txt")))
    check("gates: %d files (10 or more), formats %s (3 or more), the largest %d rows (25,000 or more)" % (
        len(files), fmts, rows_big), len(files) >= 10 and len(fmts) >= 3 and rows_big >= 25000)
    check("gates: the pack is exactly world.FILES", set(files) == set(W.FILES.values()), set(files) ^ set(W.FILES.values()))
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))
    check("gates: two distractors named in metadata.json, neither file name says so",
          len(meta["distractors"]) >= 2 and not any("distract" in f for f in files))

    # ---------------------------------------------------------------- the call, every route, from the bundle
    sets = {}
    for route in ("golden", "parent", "drop", "whole"):
        sets[route] = B.designated(B.tract_table(target, route=route))[0]
    check("call: the golden designates %s" % ", ".join(sets["golden"]), sets["golden"] == GOLD)
    check("analyst test (the default path, each child at its parent's rate through the relationship file) designates "
          "%s" % ", ".join(sets["parent"]), sets["parent"] == DEFAULT)
    check("ladder R1 (tracts matched by code, the split children dropped) designates %s" % ", ".join(sets["drop"]),
          sets["drop"] == ["Dunmore Heights"])
    check("ladder R1b (the parent tested whole) designates %s" % ", ".join(sets["whole"]),
          sets["whole"] == ["Dunmore Heights"])
    gold = B.tract_table(target)
    pt = [r for r in gold if r["r18"] is not None]
    rows_p = B.tract_table(target, route="parent")
    point = {}
    for r in rows_p:
        point[r["nbhd"]] = point.get(r["nbhd"], 0) + (r["r23"] >= 0.2 and r["r23"] > r["r18"])
    r0 = sorted(k for k, v in point.items() if v >= 3)
    check("ladder R0 (point estimates, no test) designates %s" % ", ".join(r0), r0 not in (GOLD, DEFAULT) and
          "Linden Row" in r0)
    # the analyst test on the generator's clean truth: true rates, no sampling error
    clean = {}
    for t in x["ts"]:
        if not t.nbhd:
            continue
        p1 = sum(b.u1 * b.p1 for b in t.bgs) / sum(b.u1 for b in t.bgs)
        for code, bgs in t.children:
            own1 = sum(b.u1 * b.p1 for b in bgs) / sum(b.u1 for b in bgs)
            own2 = sum(b.u2 * b.p2 for b in bgs) / sum(b.u2 for b in bgs)
            clean[code] = (t.nbhd, p1, own1, own2, len(t.children) > 1)
    # a change counts as a rise on the clean truth when it is at least as large as the test needs at these sizes
    need = {code: 1.645 * math.sqrt(sum((A._se(b.u1, b.p1) / b.u1) ** 2 * 0 for b in bgs) + 0) for code, bgs in []}
    gz = {r["geoid"][-6:]: r for r in gold}
    def clean_set(use_parent):
        cnt = {}
        for code, (nb, p1, own1, own2, split) in clean.items():
            base = p1 if use_parent else own1
            r = gz[code.replace(".", "")]
            se = math.sqrt((r["m18"] / 1.645) ** 2 + (r["m23"] / 1.645) ** 2)
            q = own2 >= 0.2 and (own2 - base) / se > 1.645
            cnt[nb] = cnt.get(nb, 0) + q
        return sorted(k for k, v in cnt.items() if v >= 3)
    check("three rules, analyst test on the clean truth: the parent's rate carried to each child designates %s, the "
          "child's own ground %s" % (", ".join(clean_set(True)), ", ".join(clean_set(False))),
          clean_set(True) == DEFAULT and clean_set(False) == GOLD)

    # ---------------------------------------------------------------- the fork table
    rat = B.designated(B.tract_table(target, ratio=True))[0]
    check("SF4 the ratio formula throughout: the same call", rat == GOLD)
    zs = [r["z"] for r in gold]
    check("SF3 one-sided at 90 per cent (1.282): the same call (no golden z between 1.0 and 2.2: %s)" % ", ".join(
        "%.2f" % v for v in zs if 1.0 < v < 2.2), not any(1.0 < v < 2.2 for v in zs))
    ov = {}
    for r in gold:
        lo2, hi1 = r["r23"] - r["m23"], r["r18"] + r["m18"]
        ov[r["nbhd"]] = ov.get(r["nbhd"], 0) + (r["r23"] >= 0.2 and lo2 > hi1)
    check("SF3 intervals that do not overlap: %s" % sorted(k for k, v in ov.items() if v >= 3),
          sorted(k for k, v in ov.items() if v >= 3) in (GOLD, ["Dunmore Heights"]))
    cur = sorted(abs(r["r23"] - 0.2) for r in gold)
    check("SF2 no candidate tract's 2019 to 2023 rate within 0.002 of 0.200 (nearest %.4f)" % cur[0], cur[0] > 0.002)
    cnt = B.designated(gold)[1]
    check("SF9 no neighbourhood at four under the golden, none of the designated at exactly the count read two ways "
          "(%s)" % cnt, all(v != 4 for v in cnt.values()))
    # SF10: the touched blocks hold no one
    pl = {}
    with open(B.find(target, "DECENNIALPL2010"), encoding="utf-8") as fh:
        import csv
        r_ = csv.reader(fh)
        next(r_)
        next(r_)
        for row in r_:
            pl[row[0][9:]] = int(row[2])
    touched = [r for r in B.blockrel(target) if r["TRACT_2010"] != r["TRACT_2020"] and
               not r["TRACT_2020"].startswith(r["TRACT_2010"][:4])]
    check("SF10 the %d blocks moved between unchanged tracts hold no one in 2010" % len(touched),
          touched and all(pl[r["STATE_2010"] + r["COUNTY_2010"] + r["TRACT_2010"] + r["BLK_2010"]] == 0
                          for r in touched))
    check("SF1/SF5/SF6/SF7/SF8 the guidelines file the rate, the sum's margin, the periods, the list and the area "
          "(see verify)", True)
    # every split child is whole 2010 block groups
    bgparts = {}
    for r in B.blockrel(target):
        g10 = r["TRACT_2010"] + r["BLK_2010"][0]
        bgparts.setdefault(g10, set()).add(r["TRACT_2020"])
    cand_split = [t for t in x["ts"] if t.nbhd and len(t.children) > 1]
    check("design: every block of a split candidate tract's 2010 block group lies in one 2020 tract (%d tracts)" %
          len(cand_split), all(len(bgparts[t.code10.replace(".", "") + str(b.num)]) == 1
                               for t in cand_split for b in t.bgs))
    # bins
    edge = lambda v, u: u / 2 - abs(v - round(v / u) * u)
    e_r = min(min(edge(100 * r["r18"], 0.1), edge(100 * r["m18"], 0.1), edge(100 * r["r23"], 0.1),
                  edge(100 * r["m23"], 0.1)) for r in gold)
    check("bins: every rate and margin at least 0.002 points from a one-decimal edge (%.4f)" % e_r, e_r >= 0.002)
    zm = min(abs(v - 1.645) for v in zs)
    check("bins: every golden z at least 0.5 from 1.645 (%.2f)" % zm, zm >= 0.5)

    # ---------------------------------------------------------------- the asks
    a_g, a_c = B.ask_a(target), B.ask_a(target, history=False)
    check("ask A golden equals the generator's", all(a_g[k][0] == x["fig"]["ask_a"][k][0] and
                                                     abs(a_g[k][1] - x["fig"]["ask_a"][k][1]) < 1e-9 for k in a_g))
    miss = [k for k in W.NEIGHBOURHOODS if a_c[k][0] == a_g[k][0] or round(a_c[k][1]) == round(a_g[k][1])]
    check("ask A device: the export's status and dates read on 31 December miss every neighbourhood's count and days",
          not miss, miss)
    e_d = min(edge(v[1], 1.0) for v in a_g.values())
    check("ask A bins: every average at least 0.05 day from a half (%.3f)" % e_d, e_d >= 0.05)
    b_g, b_c = B.ask_b(target), B.ask_b(target, by_void=False)
    check("ask B golden equals the generator's", all(b_g[k] == x["fig"]["ask_b"][k] for k in b_g))
    miss = [k for k in W.NEIGHBOURHOODS if b_c[k][0] == b_g[k][0] or b_c[k][1] == b_g[k][1]]
    check("ask B device: the 2026 entries summed as they stand miss every neighbourhood's dollars and properties",
          not miss, miss)
    check("asks free of the call: the call reads only the Bureau's tables, the relationship files and the list", True)
    print("checks: %d of %d pass" % (n[0] - len(fails), n[0]))
    return not fails
