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


def _row(ask, label, got, want, unit=1.0):
    """One scored figure: what the response computed, what the rubric owes, and the distance between them.

    The distance is printed for every row of both responses, so a row that scores a miss because the
    response attempted nothing is visible as such instead of hiding inside a count.
    """
    return (ask, label, _hit(got, want, unit), float(got), float(want), unit)


def ask_rows(target, g, careful):
    """Score the three asks on one reading. `careful` is the cracker's reading, otherwise the mirror's."""
    b = g["bundle"]
    rows = []

    # ---- A2 what the complication indicator excludes at each hospital, year ended 31 December 2026 ----
    # the careful read takes the separations from the system that counts them, the activity summary, and
    # the excluded ones as the summary's separations less the episodes the indicator measured; the ordinary
    # read counts the episode extract's own rows, which is one row per record the warehouse received
    # The ask does not point at the activity summary, and nothing in the pack says the episode extract is
    # short of any separation, so both responses count the extract's own rows and apply specification 2.1
    # to 2.3 to them. The two columns therefore agree on this ask by construction: it has one natural path
    # and a truth that only a reconciliation across the two files' grains reaches. That is stated here
    # rather than printed as two measurements.
    units_reg = b["units"]
    acute = {c for c, u in units_reg.items() if u["service_type"] == "Acute inpatient"}
    exc = collections.defaultdict(int)
    exh = collections.defaultdict(int)
    bands = b["bands"]
    with open(os.path.join(target, "episode_outcomes_extract.csv"), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["unit_code"] not in acute:
                continue
            sep = dt.date.fromisoformat(r["separation_date"])
            if not (dt.date(2026, 1, 1) <= sep <= dt.date(2026, 12, 31)):
                continue
            band = bands.get(r["drg_code"], "")
            if r["care_type"] == "Acute" and int(r["los_days"]) >= 1 and band not in ("", "SAME-DAY"):
                continue                       # the indicator measures this one
            site = b["facility"][(r["unit_code"], sep.replace(day=1).isoformat())]
            exc[site] += 1
            exh[site] += 1 if r["hac_recorded"] == "1" else 0
    for h in g["hospitals"]:
        c = h["hospital"]
        rows.append(_row("A2", "%s excluded" % c, exc[c], h["separations"]))
        rows.append(_row("A2", "%s excluded with a complication" % c, exh[c], h["complications"]))

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
        rows.append(_row("A3", "%s separations" % q, got, o["separations"]))
        rows.append(_row("A3", "%s with a complication" % q, goth, o["with_complication"]))

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
        rows.append(_row("A4", "%s 2025-26" % x["group"], len(found["2025-26"][x["group"]]), x["fy2025"]))
        rows.append(_row("A4", "%s 2026-27" % x["group"], len(found["2026-27"][x["group"]]), x["fy2026"]))
    return rows


def run(target):
    g = G.compute(target)
    units = g["units"]
    cr = ask_rows(target, g, careful=True)
    mi = ask_rows(target, g, careful=False)
    n_ask = len(cr)

    # the construction layer: the twelve avoidable counts the decisive construction produces
    construction = [_row("C", d["unit"], d["avoidable"], d["avoidable"]) for d in units]
    mirror_construction = [_row("C", d["unit"], d["published_excess"], d["avoidable"]) for d in units]
    n_con = len(construction)

    cr_keep = sum(1 for r in cr if r[2])
    mi_keep = sum(1 for r in mi if r[2])
    cr_con = sum(1 for r in construction if r[2])
    mi_con = sum(1 for r in mirror_construction if r[2])
    total = n_ask + n_con

    Lc = (cr_keep + cr_con) / float(total)
    Ls = (mi_keep + mi_con) / float(total)
    cracker = REC + INSTR + ASKS * Lc
    mirror = WRONG_CALL_KEEPS + INSTR + ASKS * Ls
    ceiling = (cracker + mirror) / 2.0
    leakage = 100.0 * Ls
    return dict(cracker_rows=cr, mirror_rows=mi, construction=construction,
                mirror_construction=mirror_construction, n_ask=n_ask, n_con=n_con,
                cracker_ask_kept=cr_keep, mirror_ask_kept=mi_keep,
                cracker_construction_kept=cr_con, mirror_construction_kept=mi_con,
                cracker_score=cracker, mirror_score=mirror, ceiling=ceiling, leakage=leakage,
                Lc=Lc, Ls=Ls)


def report(target, verbose=True):
    r = run(target)
    asks = sorted({x[0] for x in r["cracker_rows"]})
    print("the cracker landed the call; the mirror stopped at the published excess carried onto the plan")
    print()
    print("  %-4s %6s  %-16s %-16s" % ("ask", "figs", "cracker keeps", "mirror keeps"))
    weakest = None
    for a in asks:
        cr = [x for x in r["cracker_rows"] if x[0] == a]
        mi = [x for x in r["mirror_rows"] if x[0] == a]
        print("  %-4s %6d  %-16s %-16s" % (a, len(cr), "%d of %d" % (sum(1 for x in cr if x[2]), len(cr)),
                                           "%d of %d" % (sum(1 for x in mi if x[2]), len(mi))))
        if weakest is None or sum(1 for x in cr if x[2]) > weakest[1]:
            weakest = (a, sum(1 for x in cr if x[2]), len(cr))
    print("  %-4s %6d  %-16s %-16s" % ("C", r["n_con"],
                                       "%d of %d" % (r["cracker_construction_kept"], r["n_con"]),
                                       "%d of %d" % (r["mirror_construction_kept"], r["n_con"])))
    if verbose:
        print()
        print("  every figure both responses attempt, what each computed and what the rubric owes. A row")
        print("  where the two columns carry the same value is a figure the response got right; a row where")
        print("  they differ is a figure it attempted and missed. No row is scored unattempted.")
        print()
        print("    %-4s %-28s %12s %12s %10s %6s %6s"
              % ("ask", "figure", "cracker", "mirror", "owed", "unit", "verdict"))
        byk = {}
        for x in r["mirror_rows"]:
            byk[(x[0], x[1])] = x
        for x in r["cracker_rows"]:
            m = byk[(x[0], x[1])]
            v = ("both" if x[2] and m[2] else "cracker" if x[2] else "mirror" if m[2] else "neither")
            print("    %-4s %-28s %12.2f %12.2f %10.2f %6.2f %6s"
                  % (x[0], x[1][:28], x[3], m[3], x[4], x[5], v))
        mb = {x[1]: x for x in r["mirror_construction"]}
        for x in r["construction"]:
            m = mb[x[1]]
            v = ("both" if x[2] and m[2] else "cracker" if x[2] else "mirror" if m[2] else "neither")
            print("    %-4s %-28s %12.2f %12.2f %10.2f %6.2f %6s"
                  % ("C", x[1], x[3], m[3], x[4], x[5], v))
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
