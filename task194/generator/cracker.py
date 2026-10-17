"""The cracker and the mirror, run on the cut pack.

Part 1.1 of `supplemental-stumping` defines the two responses, and they are scored here from different
readings rather than one reading twice.

The **cracker** landed the call: it rebuilt the comparison frequency from the record, so it holds all twelve
avoidable counts. On the asks it is the careful response: it runs the hygiene battery (key uniqueness,
unmatched joins, fan-out, count ties across grains) and executes every handling the dictionary and the
specification describe. A device a column description resolves is therefore free to it, and only an
inconsistency nothing in the pack invites costs it a figure.

The **mirror** stopped at the most attractive wrong rung, which is the published excess carried onto the
planned separations, so its twelve figures are published excesses and none of them is an avoidable count.
On the asks it is the ordinary response: it takes each ask the way its own file's grain leads, without the
cross-grain reconciliation or the dictionary's handling notes.

Prints one row per response, every ask contributing a scored figure to both rows, the weakest ask by figures
kept, the pair ceiling and the mirror's leakage. `checks.py` asserts the figures against the ask sheet.
"""
import collections
import csv
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import golden as G

REC, ASKS, INSTR = 38.0, 55.0, 7.0          # the rubric's three blocks
WRONG_CALL_KEEPS = 5.0                       # what a wrong call keeps of the recommendation block


def _hit(a, b, unit=1.0):
    """A hit is within half a unit of the stated rounding."""
    return abs(float(a) - float(b)) <= unit / 2.0


def ask_rows(target, g, careful):
    """Score the three asks on one reading. `careful` is the cracker's reading, otherwise the mirror's."""
    b = g["bundle"]
    rows = []

    # ---- A2 each hospital's adjusted complication rate for the year ended 31 December 2026 ----
    # the careful read counts an episode to the site its unit reported under in the month it separated,
    # which the dictionary describes; the ordinary read joins the register, which is the master at export
    reg = {c: u["hospital_code"] for c, u in b["units"].items()}
    bands = b["bands"]
    strata = b["strata"]
    acc = collections.defaultdict(lambda: [0, 0, 0.0])
    with open(os.path.join(target, "episode_outcomes_extract.csv"), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            eid = r["episode_id"]
            if eid not in b["inscope_episode"]:
                continue
            unit, sep, fy = b["inscope_episode"][eid]
            if not (dt.date(2026, 1, 1) <= sep <= dt.date(2026, 12, 31)):
                continue
            site = (b["facility"][(unit, sep.replace(day=1).isoformat())] if careful else reg[unit])
            cell = acc[site]
            cell[0] += 1
            cell[1] += 1 if r["hac_recorded"] == "1" else 0
            cell[2] += strata[(bands[r["drg_code"]], r["age_band"])]
    for h in g["hospitals"]:
        cell = acc[h["hospital"]]
        rate = cell[1] / cell[2] * G.REF_RATE if cell[2] else 0.0
        rows.append(("A2", "%s episodes" % h["hospital"], _hit(cell[0], h["episodes"])))
        rows.append(("A2", "%s complications" % h["hospital"], _hit(cell[1], h["complications"])))
        rows.append(("A2", "%s adjusted rate" % h["hospital"], _hit(rate, h["rate"], 0.1)))

    # ---- A3 the separations our sub-acute and mental health units reported, by quarter ----
    # the careful read de-duplicates on the separation key the dictionary states; the ordinary read counts
    # the extract's rows, so the overlapping monthly load is counted twice
    acute = {c for c, u in b["units"].items() if u["service_type"] == "Acute inpatient"}
    seen = collections.defaultdict(set)
    raw = collections.defaultdict(int)
    hac_seen = collections.defaultdict(set)
    hac_raw = collections.defaultdict(int)
    with open(os.path.join(target, "episode_outcomes_extract.csv"), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["unit_code"] in acute:
                continue
            q = G.fiscal(dt.date.fromisoformat(r["separation_date"]))[1]
            key = (r["unit_code"], r["patient_uid"], r["admission_date"], r["drg_code"])
            raw[q] += 1
            seen[q].add(key)
            if r["hac_recorded"] == "1":
                hac_raw[q] += 1
                hac_seen[q].add(key)
    for o in g["outside"]:
        q = o["quarter"]
        got = len(seen[q]) if careful else raw[q]
        goth = len(hac_seen[q]) if careful else hac_raw[q]
        rows.append(("A3", "%s separations" % q, _hit(got, o["separations"])))
        rows.append(("A3", "%s with a complication" % q, _hit(goth, o["with_complication"])))

    # ---- A4 the in-scope episodes recording a complication, by complication group and year ----
    # the careful read takes each code against the revision in force at separation, which the specification
    # states; the ordinary read takes the current revision throughout. Neither reaches the units the
    # clinical information system does not cover, whose complications are only in the extract's own
    # category column: that gap is visible only by reconciling the detail extract's counts against the
    # extract's own flag, across two grains, which nothing in the pack invites
    cat = {}
    for r in G._read(target, "hac_category_list.csv"):
        cat[(r["list_revision"], r["complication_code"])] = r["group_id"]
    found = collections.defaultdict(lambda: collections.defaultdict(set))
    for r in G._read(target, "hac_detail_extract.csv"):
        eid = r["episode_id"]
        if eid not in b["inscope_episode"]:
            continue
        unit, sep, fy = b["inscope_episode"][eid]
        if fy not in ("2025-26", "2026-27"):
            continue
        rev = ("2026" if sep >= dt.date(2026, 7, 1) else "2022") if careful else "2026"
        gid = cat.get((rev, r["complication_code"]))
        if gid:
            found[fy][gid].add(eid)
    for x in g["groups"]:
        rows.append(("A4", "%s 2025-26" % x["group"], _hit(len(found["2025-26"][x["group"]]), x["fy2025"])))
        rows.append(("A4", "%s 2026-27" % x["group"], _hit(len(found["2026-27"][x["group"]]), x["fy2026"])))
    return rows


def run(target):
    g = G.compute(target)
    units = g["units"]
    cr = ask_rows(target, g, careful=True)
    mi = ask_rows(target, g, careful=False)
    n_ask = len(cr)

    # the construction layer: the twelve avoidable counts the decisive construction produces
    construction = [("C", d["unit"], True) for d in units]
    mirror_construction = [("C", d["unit"], _hit(d["published_excess"], d["avoidable"]))
                           for d in units]
    n_con = len(construction)

    cr_keep = sum(1 for _, _, k in cr if k)
    mi_keep = sum(1 for _, _, k in mi if k)
    cr_con = sum(1 for _, _, k in construction if k)
    mi_con = sum(1 for _, _, k in mirror_construction if k)
    total = n_ask + n_con

    Lc = (cr_keep + cr_con) / float(total)
    Ls = (mi_keep + mi_con) / float(total)
    cracker = REC + INSTR + ASKS * Lc
    mirror = WRONG_CALL_KEEPS + INSTR + ASKS * Ls
    ceiling = (cracker + mirror) / 2.0
    leakage = 100.0 * Ls
    return dict(cracker_rows=cr, mirror_rows=mi, n_ask=n_ask, n_con=n_con,
                cracker_ask_kept=cr_keep, mirror_ask_kept=mi_keep,
                cracker_construction_kept=cr_con, mirror_construction_kept=mi_con,
                cracker_score=cracker, mirror_score=mirror, ceiling=ceiling, leakage=leakage,
                Lc=Lc, Ls=Ls)


def report(target):
    r = run(target)
    asks = sorted({a for a, _, _ in r["cracker_rows"]})
    print("the cracker landed the call; the mirror stopped at the published excess carried onto the plan")
    print()
    print("  %-4s %6s  %-28s %-28s" % ("ask", "figs", "cracker keeps", "mirror keeps"))
    weakest = None
    for a in asks:
        cr = [k for x, _, k in r["cracker_rows"] if x == a]
        mi = [k for x, _, k in r["mirror_rows"] if x == a]
        print("  %-4s %6d  %-28s %-28s" % (a, len(cr), "%d of %d" % (sum(cr), len(cr)),
                                           "%d of %d" % (sum(mi), len(mi))))
        if weakest is None or sum(cr) > weakest[1]:
            weakest = (a, sum(cr), len(cr))
    print("  %-4s %6d  %-28s %-28s" % ("C", r["n_con"],
                                       "%d of %d" % (r["cracker_construction_kept"], r["n_con"]),
                                       "%d of %d" % (r["mirror_construction_kept"], r["n_con"])))
    print()
    print("  the asks consume nothing the call's construction produces, so the two ask readings are")
    print("  scored from the two responses' own handling, not from the call; the separation assertions")
    print("  in checks.py are what prove the decoupling, and no row here is a duplicate of another")
    print()
    print("  weakest ask by figures the cracker keeps: %s, %d of %d" % weakest)
    print("  cracker  %.1f  (ask weight kept %.3f)" % (r["cracker_score"], r["Lc"]))
    print("  mirror   %.1f  (ask weight kept %.3f)" % (r["mirror_score"], r["Ls"]))
    print("  pair ceiling %.1f" % r["ceiling"])
    print("  mirror leakage %.1f per cent of ask weight" % r["leakage"])
    return r


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
    report(tgt)
