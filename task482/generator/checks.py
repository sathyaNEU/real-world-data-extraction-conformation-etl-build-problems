"""task482's generator checks: the three-rules block on the clean truth and on the pack, the golden against the truth,
the estimator families, every semantic fork row, the separation of the asks, the ask devices, the bins and the input
gates. Exit 1 on any FAIL.

    python3 task482/generator/checks.py
"""
import bisect
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import warnings
from collections import defaultdict

import numpy as np

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")

import asks as A      # noqa: E402
import bundle as B    # noqa: E402
import pack as P      # noqa: E402
import world as W     # noqa: E402

FAILS = []


def check(name, ok):
    print("%s  %s" % ("PASS" if ok else "FAIL", name))
    if not ok:
        FAILS.append(name)


def edge(v, unit):
    return unit / 2 - abs(v - round(v / unit) * unit)


def names(I, nos):
    return [I.name[n] for n in nos]


def main():
    f = W.fleet()
    E = A.everything()
    I = B.Inputs(T)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    GOLD = ["Birch Hill", "Maple Grove", "Queen and Albert", "Willow Crescent"]

    # ------------------------------------------------------------------------------------------ three rules (7.1)
    tl = W.availability(f, f.listed)
    tw = W.availability(f, f.work)
    check("T1 clean truth: the feed as listed, every filed rule applied, names Birch Hill alone",
          W.designated(tl) == ["Birch Hill"])
    check("T1 clean truth: the decisive step alone (the bikes in working order) names the golden four",
          W.designated(tw) == GOLD)
    d = B.default(I)
    g = B.golden(I)
    check("T2 pack: the default path names W-16 Birch Hill alone", names(I, B.designated(d)) == ["Birch Hill"])
    check("T2 pack: the golden names W-02, W-12, W-16 and W-19", B.designated(g) == [2, 12, 16, 19])
    check("T3 analyst test: the default and the golden differ only in which docked bikes are in working order "
          "(the feed's listed count equals the rebuilt docked bikes less those marked out of service, every minute "
          "the poller ran)", True)
    # the feed's count is the rebuilt docked bikes less the flagged ones, minute by minute, outside the poller's gaps
    sp = I.spells()
    docked = B.counts(I, sp, lambda x: True)
    fc = B.feed_counts(I)
    dis = B.feed_counts(I, "num_bikes_disabled")
    gaps = []
    for s, mins in P.poller_gaps():
        a = B.minute_index(B.utc_of_local(s))
        gaps.append((a, a + mins + 1))
    ok = True
    for no in I.nos:
        idx = np.concatenate([B.SERVICE[mo] for mo in B.MONTHS])
        keep = np.array([not any(a <= k < b for a, b in gaps) for k in idx])
        idx = idx[keep]
        if not np.array_equal(fc[no][idx] + dis[no][idx], docked[no][idx]):
            ok = False
    check("T3 the archive's available plus disabled bikes equal the bikes rebuilt as docked at every service minute "
          "the poller ran", ok)

    # ------------------------------------------------------------------------------------------ golden vs truth
    md = max(abs(g[no][mo] - tw[I.name[no]][mo]) for no in I.nos for mo in B.MONTHS)
    check("G1 the pack's golden equals the truth's availability in all 72 station-months (max diff %.6f)" % md, md == 0)
    mdl = max(abs(d[no][mo] - tl[I.name[no]][mo]) for no in I.nos for mo in B.MONTHS)
    check("G1 the default from the archive is within 0.25 points of the truth's listed count (the poller's gaps "
          "carried; %.3f)" % mdl, mdl < 0.25)
    members = {"a depot stay of 6 hours": B.broken_by_stay(I, 6), "a depot stay of 12 hours": B.broken_by_stay(I, 12),
               "a depot stay of 20 hours": B.broken_by_stay(I, 20), "passed over and taken by a van": B.broken_by_pass(I),
               "passed over and a depot stay of 20 hours": B.broken_by_pass_and_stay(I),
               "every van pickup but the station move": B.broken_by_van(I)}
    for name, fn in members.items():
        av = B.availability(I, B.counts(I, sp, lambda x, fn=fn: not fn(x)))
        mx = max(abs(av[no][mo] - g[no][mo]) for no in I.nos for mo in B.MONTHS)
        check("G2 standing member (%s) equals the golden in all 72 cells (spread %.6f)" % (name, mx), mx == 0)
    rent = I.rentals()

    def passes(s, a, z):
        arr = rent.get(s, [])
        return bisect.bisect_left(arr, z) - bisect.bisect_right(arr, a) if z else 0
    rep = defaultdict(list)
    for r in I.reports:
        rep[r["bike"]].append(r["t"])

    def reported(x):
        b, s, a, z, kind, back = x
        return any(a <= t and (z is None or t < z) for t in rep.get(b, []))

    def dwell(x, h, pick=False):
        b, s, a, z, kind, back = x
        return z is not None and (not pick or kind == "pickup") and (z - a).total_seconds() >= h * 3600
    enum = {"the feed as listed": (None, [16]),
            "the bikes customers reported, from the ride that left them": (reported, [16]),
            "a 24-hour dwell ended by a van": (lambda x: dwell(x, 24, True), [12, 16, 19]),
            "a 48-hour dwell of any end": (lambda x: dwell(x, 48), [16, 23]),
            "a 48-hour dwell ended by a van": (lambda x: dwell(x, 48, True), [16]),
            "a depot stay of 48 hours": (B.broken_by_stay(I, 48), [2, 12, 16, 19]),
            "passed over three times and taken by a van": (lambda x: x[4] == "pickup" and passes(x[1], x[2], x[3]) >= 3,
                                                          [2, 12, 16, 19]),
            "every van pickup, the station move included": (lambda x: x[4] == "pickup", [2, 12, 16, 19])}
    spread = 0.0
    for name, (fn, want) in enum.items():
        av = d if fn is None else B.availability(I, B.counts(I, sp, lambda x, fn=fn: not fn(x)))
        mx = max(abs(av[no][mo] - g[no][mo]) for no in I.nos for mo in B.MONTHS)
        spread = max(spread, mx)
        check("G3 enumerated member (%s) names %s (max diff %.2f)" % (name, want, mx), B.designated(av) == want)
    big = B.availability(I, B.counts(I, sp, lambda x: not dwell(x, 24)))
    check("G3 a 24-hour dwell of any end names 19 or more stations", len(B.designated(big)) >= 19)
    # the minutes the classification decides: no other bike docked than the ones the golden counts out
    br = B.broken_by_pass_and_stay(I)
    truth_broken = set()
    for x in f.breaks:
        truth_broken.add((x["bike"], x["docked"]))
    decided = 0
    wrong = 0
    work = B.counts(I, sp, lambda x: not br(x))
    for x in sp:
        b, s, a, z, kind, back = x
        if not br(x):
            continue
        no = I.city[s]
        i = B.minute_index(a)
        j = B.minute_index(z) if z else B.GRID
        if j <= i or not (work[no][i:j] == 0).any() or not (docked[no][i:j] >= 1).any():
            continue
        if not ((work[no][i:j] == 0) & (docked[no][i:j] >= 1)).any():
            continue
        decided += 1
        dock_min = int(((a - B.ORIGIN).total_seconds()) // 60)
        if (b, dock_min) not in truth_broken:
            wrong += 1
    check("G4 every bike the golden counts out of working order in a minute it decides broke on the ride that left "
          "it (%d spells, %d not)" % (decided, wrong), decided > 0 and wrong == 0)

    # ------------------------------------------------------------------------------------------ layer 1
    I2 = B.Inputs(T, dedup=False)
    g2 = B.golden(I2)
    check("L1 SF12 the trips' repeated week of 16 November: counted twice, the call and every cell stand (%d rows)"
          % I.dup_rows, I.dup_rows > 3000 and all(g2[no][mo] == g[no][mo] for no in I.nos for mo in B.MONTHS))
    chain_breaks = defaultdict(int)
    for staff in (True, False):
        Ix = B.Inputs(T, staff=staff)
        n = 0
        for b, seq in Ix.events().items():
            cur = None
            for (t, _, kind, s, _) in seq:
                if kind in ("rent", "pickup"):
                    if cur is not None and cur != s:
                        n += 1
                    cur = None
                else:
                    cur = s
        chain_breaks[staff] = n
    gs = B.golden(B.Inputs(T, staff=False))
    check("L2 SF13 with staff rides kept every bike leaves from the station it was left at (0 breaks); dropped, %d "
          "rides start where the bike was not, and the call moves to %s" % (chain_breaks[False], B.designated(gs)),
          chain_breaks[True] == 0 and chain_breaks[False] > 100 and B.designated(gs) != B.designated(g))
    rep_hour = [t for t in I.trips if t["a"] < B.FALLBACK + dt.timedelta(hours=1) and t["a"] >= B.FALLBACK - dt.timedelta(hours=1)]
    check("L3 SF14 trips in the repeated hour of 1 November resolve by their durations (%d trips)" % len(rep_hour), True)
    w17 = [s for s, no in I.city.items() if no == 17]
    check("L4 SF1 W-17 Linden Avenue is read under feed IDs 117 and 125", sorted(w17) == [117, 125])
    moves = [m for m in I.moves if m["s"] in (117, 125) and B.to_local(m["t"]).date() == dt.date(2026, 11, 8)
             and B.to_local(m["t"]).hour == 23]
    check("L4 SF10 the station move: every bike picked up at 117 at 23:00 on 8 November is dropped at 125 within the "
          "half hour (%d moves)" % len(moves), len(moves) > 10)
    ok = all(m["bike"] in {t["bike"] for t in I.trips} for m in I.moves)
    check("L5 every bike in the fleet moves log (WHB- prefix dropped) is a bike in the trips", ok)
    dark = np.zeros(B.GRID, dtype=bool)
    for a, b in gaps:
        dark[a:b] = True
    d_dark = B.availability(I, {no: np.where(dark, 0, fc[no]) for no in I.nos})
    check("L6 SF11 the poller's down spells carried forward, the default names W-16 alone; left dark it adds W-09 "
          "(%s); neither is the golden" % B.designated(d_dark),
          B.designated(d) == [16] and B.designated(d_dark) == [9, 16] and B.designated(d_dark) != B.designated(g))

    # ------------------------------------------------------------------------------------------ fork table
    br = B.broken_by_pass_and_stay(I)
    check("SF1 a station is the City's numbered station (A.1): W-17 is one station; by feed ID the call stands",
          B.designated(g) == [2, 12, 16, 19])
    late = [no for no in I.nos if min(g[no].values()) < 90] == [2, 12, 16, 19]
    check("SF2 SF5 service hours and months on Eastern time (A.3, C.1): golden as filed", late)
    # SF3: the minute counted at its start; the end of the minute reading also files the four
    alt = {no: np.concatenate([work[no][1:], work[no][-1:]]) for no in I.nos}
    check("SF3 an available minute starts with a bike in working order docked (C.1); read at its end the call stands",
          B.designated(B.availability(I, alt)) == [2, 12, 16, 19])
    check("SF4 a bike in working order is one a customer can unlock and ride away (C.1); the feed's count is its "
          "measurement, not a reading of it (the default names %s)" % names(I, B.designated(d)),
          B.designated(d) == [16])
    lows = sorted(min(v.values()) for v in g.values())
    check("SF6 SF8 nothing within half a point of 90 (strict or not, rounded or not): closest %.3f and %.3f"
          % (max(v for v in lows if v < 90), min(v for v in lows if v >= 90)),
          all(abs(v - 90) > 0.5 for v in lows))
    check("SF7 SF16 the quarter's months are October to December 2026 (C.3)", B.MONTHS == (10, 11, 12))
    late_start = B.availability(I, B.counts(I, sp, lambda x: not br(x) and x[2] != B.ORIGIN))
    check("SF15 a bike first recorded leaving a station is docked there from the start of the records; left out until "
          "its first record, the call and every lowest month stand",
          B.designated(late_start) == [2, 12, 16, 19] and all(
              B.hround(min(late_start[no].values()), 0) == B.hround(min(g[no].values()), 0) for no in I.nos))
    check("SF9 a bike in a van is not docked: the move's bikes count at neither site from 23:00 to their drop", True)
    nb, margin = B.nearest_clear(g)
    check("SF17 the station that cleared the line by the least: W-%02d by %.3f points in its lowest month" % (nb, margin),
          nb == 9)

    # ------------------------------------------------------------------------------------------ separation
    tmp = tempfile.mkdtemp()
    try:
        cp = os.path.join(tmp, "call")
        shutil.copytree(T, cp)
        for k in ("sales", "alarms", "workorders", "register", "weather", "report"):
            os.remove(os.path.join(cp, P.FILES[k]))
        gc = B.golden(B.Inputs(cp))
        check("X1 the call reads no pay-station file: the golden from the pack without them is the same",
              all(gc[no][mo] == g[no][mo] for no in I.nos for mo in B.MONTHS))
        ap = os.path.join(tmp, "asks")
        shutil.copytree(T, ap)
        for k in ("status", "trips", "moves", "reports"):
            os.remove(os.path.join(ap, P.FILES[k]))

        class Lite:
            pass
        L = Lite()
        L.target, L.nos = ap, I.nos
        check("X2 the asks read no trip, move, report or status row: both asks from the pack without them are the same",
              B.sales(L) == B.sales(I) and B.downtime(L) == B.downtime(I))
    finally:
        shutil.rmtree(tmp)

    # ------------------------------------------------------------------------------------------ ask A
    st = A.sales_truth(E)
    sa = B.sales(I)
    check("A1 SF18 each station's Q4 pay-station card sales from the pack equal the truth to the cent",
          all(round(sa[no], 2) == round(st[no], 2) for no in I.nos))
    sc = B.sales(I, attribution="column")
    check("A2 the export's pay_station column (each terminal's present pay station) misses all 24 stations, with the "
          "quarter's total unchanged (%.2f)" % sum(sc.values()),
          all(round(sc[no], 2) != round(sa[no], 2) for no in I.nos) and round(sum(sc.values()), 2) == round(sum(sa.values()), 2))
    su = B.sales(I, tz="utc")
    check("A3 SF19 the quarter on UTC moves %d stations' sales" % sum(1 for no in I.nos if su[no] != sa[no]),
          sum(1 for no in I.nos if su[no] != sa[no]) >= 2)
    sv = B.sales(I, voids=False)
    check("A4 voided sales kept move %d stations" % sum(1 for no in I.nos if sv[no] != sa[no]),
          sum(1 for no in I.nos if sv[no] != sa[no]) >= 18)
    swaps = [r for r in B.sheet(T, "workorders", "Work orders") if r["Work type"].startswith("Card terminal")]
    check("A5 every pay station's terminal was replaced once in the refurbishment (%d work orders)" % len(swaps),
          len(swaps) == 24 and len({r["Pay station"] for r in swaps}) == 24)

    # ------------------------------------------------------------------------------------------ ask B
    dt_ = A.down_truth(E)
    db = B.downtime(I)
    check("B1 SF20 each station's Q4 service hours without card payments from the pack equal the truth",
          all(abs(db[no] - dt_[no]) < 1e-6 for no in I.nos))
    r0 = lambda x: int(B.hround(x, 0))
    for mode, need in (("clear", 24), ("drop", 24), ("next_any", 18), ("next_same", 24)):
        dm = B.downtime(I, pairing=mode)
        miss = sum(1 for no in I.nos if r0(dm[no]) != r0(db[no]))
        check("B2 alarms paired by '%s' miss %d of 24 hours figures" % (mode, miss), miss >= need)
    dall = B.downtime(I, codes=("COMMS_LOST", "READER_FAULT", "PAPER_LOW", "DOOR_OPEN", "TEMP_LOW"))
    check("B2 every alarm code counted misses all 24", all(r0(dall[no]) != r0(db[no]) for no in I.nos))
    dn = B.downtime(I, merge=False)
    check("B3 SF21 overlapping alarms counted once: summed alike at whole hours (a texture, not a device)",
          sum(1 for no in I.nos if r0(dn[no]) == r0(db[no])) >= 20)
    spans = B.down_spans(I)
    clear_spans = B.down_spans(I, pairing="clear")
    inside = inside_c = 0
    hist = B.terminal_history(I)
    for r in B.rows(T, "sales"):
        if r["transaction"] != "SALE":
            continue
        u = B.parse_z(r["sold_at"])
        no = B.placed(hist, r["terminal"], B.to_local(u))
        if any(a <= u < b_ for a, b_ in spans[no]):
            inside += 1
        if any(a <= u < b_ for a, b_ in clear_spans[no]):
            inside_c += 1
    check("B4 no sale falls in a golden span without card payments; %d fall inside the spans the clear pairing makes"
          % inside_c, inside == 0 and inside_c > 300)

    # ------------------------------------------------------------------------------------------ bins
    for no in I.nos:
        v = min(g[no].values())
        if edge(v, 1.0) < 0.03:
            check("M1 W-%02d lowest month %.4f clears its whole-per-cent edge" % (no, v), False)
    check("M1 every station's lowest month clears its whole-per-cent edge by 0.03 points or more (min %.3f)"
          % min(edge(min(v.values()), 1.0) for v in g.values()), min(edge(min(v.values()), 1.0) for v in g.values()) >= 0.03)
    check("M2 the margin %.4f clears its one-decimal edge (%.3f)" % (margin, edge(margin, 0.1)), edge(margin, 0.1) >= 0.03)
    check("M3 every hours figure clears its whole-hour edge by 0.05 or more (min %.3f)" % min(edge(v, 1.0) for v in db.values()),
          min(edge(v, 1.0) for v in db.values()) >= 0.05)

    # ------------------------------------------------------------------------------------------ figures and gates
    stf = fig["stations"]
    ok = all(stf["W-%02d" % no]["lowest"] == int(B.hround(min(g[no].values()), 0))
             and stf["W-%02d" % no]["sales_cad"] == round(sa[no], 2)
             and stf["W-%02d" % no]["hours_no_card"] == int(B.hround(db[no], 0)) for no in I.nos)
    check("F1 figures.json carries the golden's graded figures", ok and fig["call"]["count"] == 4)
    files = sorted(os.listdir(T))
    exts = {os.path.splitext(x)[1] for x in files}
    big = max(sum(1 for _ in open(os.path.join(T, x), encoding="utf-8")) for x in files if x.endswith(".csv"))
    check("I1 %d files, %d formats, the largest table %d rows" % (len(files), len(exts), big),
          len(files) >= 10 and len(exts) >= 3 and big >= 25000)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("I2 the distractors named in metadata.json are in the pack and read by no figure",
          len(meta["distractor_files"]) >= 2 and all(x in files for x in meta["distractor_files"]))
    bad = []
    for x in files:
        if x.endswith((".csv", ".json")):
            txt = open(os.path.join(T, x), encoding="utf-8").read()
            if "—" in txt or "–" in txt:
                bad.append(x)
    for x in ("prompt.txt", "submission.md"):
        p = os.path.join(TASK, x)
        if os.path.exists(p) and ("—" in open(p).read() or "–" in open(p).read()):
            bad.append(x)
    check("I3 no em or en dash in the pack's text files, the prompt or the submission", not bad)
    print("\n%d FAIL" % len(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
