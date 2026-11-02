"""task263 ask layer against the careful solver's routes, on the cut pack.

    python3 task263/generator/ceiling.py [pack]

pack is target.zip (the default, the archive that ships) or a folder holding the pack's files. The ask is the water
the listed systems' wells pumped in 2025, for each county and each quarter (16 figures, million gallons to one
decimal). A figure is kept when it is within half a unit of the stated rounding of figures.json's.

The cracker is the careful solver, never a narrowed one. It lands the call (the mass balance, analysis.golden) and
then takes the ask the careful way, written here apart from analysis.ask_a: the operating reports' lines for the
listed systems' facilities, wells only by the inventory's facility type (the emergency well that ran is a listed
system's well that pumped, so it stays; the interconnection's purchased water is not a well's), each field read by
its plain meaning (volume_gal is the gallons, days_in_service the days, report_month the month and so the quarter,
Table 6-1's county), and the hygiene battery run on every line: exact duplicates; near-exact duplicates (two
facilities of one system and month carrying the same readings and gallons); the meter register's shared meters,
each meter once a month; amount matching (two lines of one system and month with equal gallons); roll-ups (a line
equal to the sum of other lines at its entry point that month); reading continuity per facility (each month's
start reading the last month's end, a restart explained by a meter change in the register); anti-joins both ways
(report lines without an inventory facility, listed wells without twelve months); units from magnitudes (each
meter's median gallons per day in service per gallon a minute of rated capacity, against the band every meter in
the state sits in, so a meter registering in another unit shows as a constant factor). It executes no physics of a
pump beyond that, as the battery does not. Its handling is printed item by item.

The mirror stops at the default path on the call (R0) and, the ask being decoupled from the call, takes the ask as
the cracker does. Beside them, the routes a solver who modelled the pumps could take: the other well taken off only
in the months a wellhouse line goes beyond its pump (half-handled), only the overloaded well's line kept at its
entry point (over-cleaned), and the full includer (the other well taken off every month: analysis.ask_a, the
golden's own route), which has to give back figures.json exactly.

The pair is supplemental-stumping Part 0's, with the chart's parts beside it: the cracker 38 (recommendation and
components) + 7 (instructions) + 5 (the chart, drawn from the call's own levels) + 55 x its share of the ask; the
mirror 5 + 7 + 0 + 55 x its share. Exit 0 when the gate holds (the cracker keeps no ask figure, the pair at or
under 60, the mirror under half the ask weight, two careful responses on the call under 70, the control exact),
2 when it does not, 1 when a control fails. The script modifies nothing and never runs inside the build."""
from __future__ import annotations

import collections
import csv
import hashlib
import json
import os
import shutil
import statistics
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402  (the pack's readers and the ladder's routes)
import common as K     # noqa: E402

TASK = os.path.dirname(HERE)
COUNTIES = ("Granlund", "Engvall", "Hedstrom", "Sandholm")
W_CALL, W_INSTR, W_ASK, W_CHART, R_MIRROR = 38.0, 7.0, 55.0, 5.0, 5.0
GATE = 60.0


def pack_dir(arg):
    src = arg or os.path.join(TASK, "target.zip")
    if os.path.isdir(src):
        files = sorted(os.listdir(src))
        h = hashlib.sha256("".join(hashlib.sha256(open(os.path.join(src, f), "rb").read()).hexdigest()
                                   for f in files).encode()).hexdigest()
        return src, None, "folder %s (%d files, sha256 of the file digests %s)" % (src, len(files), h[:16])
    tmp = tempfile.mkdtemp(prefix="ceiling263-")
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    return os.path.join(tmp, "target"), tmp, "%s (md5 %s)" % (src, hashlib.md5(open(src, "rb").read()).hexdigest())


def rd(target, key):
    with open(os.path.join(target, K.FILES[key]), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ------------------------------------------------------------------------------------------------ the careful solver
def careful(target, D):
    """The cracker's ask route and its battery, as described in the module docstring."""
    county = {p["pws"]: p["county"] for p in D["plan"]}
    inv = {f["facility_id"]: f for f in D["inv"]}
    rows = [r for r in rd(target, "mor") if r["pws_id"] in county]
    met = rd(target, "meters")
    log = []
    orphan = [r for r in rows if r["facility_id"] not in inv]
    log.append(("anti-join: report lines with no inventory facility", not orphan, "%d" % len(orphan)))
    wells = [r for r in rows if r["facility_id"] in inv and inv[r["facility_id"]]["facility_type"] == "Well"]
    months = collections.Counter(r["facility_id"] for r in wells)
    short = [f for f, n in months.items() if n != 12]
    listed_wells = [f for f, x in inv.items() if x["pws_id"] in county and x["facility_type"] == "Well" and
                    x["status"] in ("Active", "Emergency")]
    log.append(("anti-join: every listed well has twelve monthly lines", not short and set(listed_wells) == set(months),
                "%d wells" % len(months)))
    full = collections.Counter(tuple(r.values()) for r in wells)
    log.append(("exact duplicate lines", max(full.values()) == 1, "%d lines" % len(wells)))
    near = collections.defaultdict(list)
    for r in wells:
        near[(r["pws_id"], r["report_month"], r["meter_start"], r["meter_end"], r["volume_gal"])].append(r)
    twins = {k: v for k, v in near.items() if len(v) > 1}
    log.append(("near-exact duplicates (two facilities, one system and month, the same readings and gallons)", True,
                "%d pairs, all on one header meter the register lists on both facilities" % len(twins)))
    shared = {}
    for m in met:
        fs = m["facility_ids"].split(";")
        if len(fs) > 1:
            for f in fs:
                shared[f] = frozenset(fs)
    on_shared = all(all(r["facility_id"] in shared for r in v) for v in twins.values())
    log.append(("the register's shared meters, each meter once a month", on_shared,
                "%d meter(s) listed on two facilities" % len({v for v in shared.values()})))
    amounts = collections.defaultdict(list)
    for r in wells:
        amounts[(r["pws_id"], r["report_month"], r["volume_gal"])].append(r["facility_id"])
    eq = [k for k, v in amounts.items() if len(v) > 1 and not all(f in shared for f in v)]
    log.append(("amount matching: equal gallons on two lines of one system and month, off a shared meter", not eq,
                "%d" % len(eq)))
    ep = {f: (x["pws_id"], x["entry_point"]) for f, x in inv.items()}
    bym = collections.defaultdict(dict)
    for r in wells:
        bym[(ep[r["facility_id"]], r["report_month"])][r["facility_id"]] = int(r["volume_gal"])
    roll = 0
    for g in bym.values():
        for f, v in g.items():
            others = [u for o, u in g.items() if o != f]
            if len(others) >= 2 and v > 0 and v == sum(others):
                roll += 1
    log.append(("roll-ups: a line equal to the sum of the other lines at its entry point", roll == 0, "%d" % roll))
    restarts, unexplained = 0, 0
    changed = {m["facility_ids"] for m in met if m["removed"]}
    seq = collections.defaultdict(list)
    for r in wells:
        seq[r["facility_id"]].append(r)
    for f, rr in seq.items():
        rr.sort(key=lambda r: r["report_month"])
        for a, b in zip(rr, rr[1:]):
            if a["meter_end"] != b["meter_start"]:
                restarts += 1
                unexplained += f not in changed
    log.append(("reading continuity per facility (a restart only where the register shows a meter change)",
                unexplained == 0, "%d restart(s), %d unexplained" % (restarts, unexplained)))
    off = [r for r in wells if int(r["meter_end"]) - int(r["meter_start"]) != int(r["volume_gal"])]
    log.append(("readings against gallons on each line (they differ only in a meter-change month; volume_gal kept)",
                all(r["facility_id"] in changed for r in off), "%d line(s), each in a meter-change month" % len(off)))
    allrows = rd(target, "mor")
    ratio = [int(r["volume_gal"]) / (int(inv[r["facility_id"]]["rated_capacity_gpm"]) * int(r["days_in_service"]))
             for r in allrows if r["facility_id"] in inv and inv[r["facility_id"]]["facility_type"] == "Well" and
             int(r["days_in_service"]) > 0]
    med = statistics.median(ratio)
    log.append(("units from magnitudes: volume_gal read as gallons against the file's magnitudes (the state's median "
                "well-month)", 100 < med < 1440, "%.0f gallons a day in service per gpm of rated capacity, inside "
                "the 1,440 of a day at rated capacity; no line set off by a unit factor" % med))
    log.append(("labels: Well, Emergency and Interconnection read as written (the emergency well that ran stays)", True,
                "%d emergency well line(s) with gallons" % sum(1 for r in wells if inv[r["facility_id"]]["status"] ==
                                                              "Emergency" and int(r["volume_gal"]) > 0)))
    done, out = set(), collections.defaultdict(float)
    for r in wells:
        g = shared.get(r["facility_id"])
        if g:
            if (g, r["report_month"]) in done:
                continue
            done.add((g, r["report_month"]))
        out[(county[r["pws_id"]], A.quarter(r["report_month"]))] += int(r["volume_gal"])
    res = {}
    for (c, q), v in out.items():
        res.setdefault(c, {})[q] = round(v / 1e6, 1)
    return res, log


def kept(route, gold):
    return sum(abs(route.get(c, {}).get(q, -1e9) - gold[c][q]) < 0.05 for c in gold for q in A.QUARTERS)


def deltas(route, gold):
    return [round(route.get(c, {}).get(q, 0.0) - gold[c][q], 1) for c in COUNTIES for q in A.QUARTERS]


def score(target):
    """(cracker keeps, mirror keeps, figures, pair, control exact) on a pack folder: the checks' entry point."""
    F = json.load(open(os.path.join(HERE, "figures.json")))
    gold = F["ask_a"]
    D = A.load(target)
    cr, _log = careful(target, D)
    n = sum(len(v) for v in gold.values())
    kc = kept(cr, gold)
    lc = ls = kc / float(n)
    cracker = W_CALL + W_INSTR + W_CHART + W_ASK * lc
    mirror = R_MIRROR + W_INSTR + W_ASK * ls
    return kc, kc, n, (cracker + mirror) / 2.0, A.ask_a(D, target) == gold


def main(arg=None):
    target, scratch, stamp = pack_dir(arg)
    try:
        return run(target, stamp)
    finally:
        if scratch:
            shutil.rmtree(scratch)


def run(target, stamp):
    print("pack: " + stamp)
    F = json.load(open(os.path.join(HERE, "figures.json")))
    gold = F["ask_a"]
    D = A.load(target)
    G = A.golden(D)
    name = {p["pws"]: p["name"] for p in D["plan"]}
    on = (len(G["funded"]), name[G["stop"]], G["left"]) == (F["call"]["systems_reached"],
                                                           F["call"]["first_not_reached"], F["call"]["left"])
    r0 = A.route(D, A.presence(D))
    off = len(r0["funded"]) != F["call"]["systems_reached"]
    print("cracker's call (the mass balance): %d systems, stops at %s, $%s left (%s)" % (
        len(G["funded"]), name[G["stop"]], "{:,}".format(G["left"]), "lands the golden" if on else "MISSES"))
    print("mirror's call (R0, the average of the samples a well ran in): %d systems, stops at %s (%s)" % (
        len(r0["funded"]), name[r0["stop"]], "off" if off else "ON THE CALL"))
    if not (on and off):
        return 1

    cr, log = careful(target, D)
    print("\nthe cracker's battery on the listed systems' 2025 operating-report lines:")
    for item, ok, detail in log:
        print("  %-4s %s (%s)" % ("ok" if ok else "FLAG", item, detail))
    lines = A.mor_lines(D, target)
    over = [l for l in lines if l["type"] == "Well" and A.beyond(l)]
    sh = A.shared_meters(target)
    print("not in the battery, a solver who modelled each pump (gallons beyond rated capacity for 24 hours of every "
          "day in service): %d listed well-month lines, %d on the register's shared header, %d on four wellhouse "
          "meters" % (len(over), sum(1 for l in over if l["fid"] in sh), sum(1 for l in over if l["fid"] not in sh)))
    full = A.ask_a(D, target)
    n = sum(len(v) for v in gold.values())
    print("\nfull includer (control, the golden's own route): %d of %d" % (kept(full, gold), n))
    if full != gold:
        print("CONTROL FAILED: the route code does not reproduce figures.json")
        return 1
    routes = [("cracker (lands the call, battery run, every field by its plain meaning)", cr),
              ("mirror (R0, off the call; the ask as the cracker)", cr),
              ("stop: every line as written (no meter once)", A.ask_a(D, target, "every_row")),
              ("stop: every line, the interconnection's purchase in", A.ask_a(D, target, "every_row_all")),
              ("stop: the golden's reading with active wells only", A.ask_a(D, target, "active_only")),
              ("stop: the golden's reading from the meter readings", A.ask_a(D, target, "readings")),
              ("pump modelled: the other well off only where a line is beyond its pump", A.ask_a(D, target, "half")),
              ("pump modelled: only the overloaded well's line at its entry point", A.ask_a(D, target, "over")),
              ("pump modelled: the other well's own line left out (the golden's rival link)",
               A.ask_a(D, target, "drop_child")),
              ("full includer (control)", full)]
    print("\nper route, figures kept of %d (county by quarter), and the deltas in million gallons:" % n)
    for lab, rt in routes:
        print("  %-78s %2d  %s" % (lab, kept(rt, gold), deltas(rt, gold)))
    kc = kept(cr, gold)
    lc = ls = kc / float(n)
    cracker = W_CALL + W_INSTR + W_CHART + W_ASK * lc
    mirror = R_MIRROR + W_INSTR + W_ASK * ls
    pair = (cracker + mirror) / 2.0
    print("\ncracker %.1f, mirror %.1f; two careful responses on the call %.1f each" % (cracker, mirror, cracker))
    print("  if the cracker alone modelled the pumps and kept all %d: pair %.1f" % (
        n, (W_CALL + W_INSTR + W_CHART + W_ASK + mirror) / 2.0))
    print("  if both responses modelled the pumps: pair %.1f" % (
        (W_CALL + W_INSTR + W_CHART + W_ASK + R_MIRROR + W_INSTR + W_ASK) / 2.0))
    print("\nCracker keeps: %d of %d ask figures" % (kc, n))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * ls))
    print("Pair ceiling: %.1f" % pair)
    held = kc == 0 and pair <= GATE and ls < 0.5 and cracker < 70.0
    print("gate: %s" % ("HOLDS" if held else "SPENT (the cracker keeps ask figures or the pair is over 60)"))
    return 0 if held else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
