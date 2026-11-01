"""task125 generator checks, run on the cut pack in target/ against the generator's own truth.

    python3 task125/generator/checks.py

C: the conformed records equal the truth; the designation equals the truth's; the standing family files one set.
R: every route the ladder prices files its stated set (the analyst test on the clean truth included).
M: margins, the candidate pool, ties, rounding edges.
SF1 to SF24: the semantic fork table, each alternative shown to file the same call or figure, or ruled out.
T: the CAD's clocks (rows forward in UTC, events in receipt order, tours read alike).
D: the device of the ask (the cracker misses every figure of ask A).
X: no generator pattern; each document's own save history."""
import collections
import datetime as dt
import json
import os
import re
import sys
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import build as B     # noqa: E402
import world as W     # noqa: E402

FAILS = []
N = [0]


def check(name, ok, detail=""):
    N[0] += 1
    print("%s  %-6s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        FAILS.append(name)


def roles_of(w):
    return w["role"]


def main():
    P = A.Pack(TARGET)
    S = A.solve(P)
    w = B.world()
    role = w["role"]
    ids, top = S["ids"], set(S["top"])
    fig = json.load(open(os.path.join(HERE, "figures.json")))

    # ------------------------------------------------------------------ C: truth
    truth = collections.Counter((s, d) for s, d, p in w["crimes"])
    got = collections.Counter(S["crimes"])
    check("C0", truth == got, "conformed founded patrol crimes equal the truth (%d)" % sum(got.values()))
    ev = w["ev"]
    gn = W.event_nights(ev, "G")
    ln = W.event_nights(ev, "L")
    check("C0b", set(gn) == {d for d in S["nights"]["G"] if d.year <= 2026} and
          set(ln) == {d for d in S["nights"]["L"] if d.year <= 2026}, "the register's venue nights are the calendar's")
    ng27, nl27 = A.calendar_2027(S["nights"])
    texp = {s: w["base"][s] + w["inc_g"].get(s, 0) * ng27 + w["inc_l"].get(s, 0) * nl27 for s in ids}
    ttop = set(sorted(ids, key=lambda s: -texp[s])[:20])
    check("C1", ttop == top, "the designation is the truth's top 20 at the 2027 calendar")
    cnt = collections.Counter(role.get(s, "-") for s in top)
    check("C1b", cnt == collections.Counter({"C": 14, "L": 5, "G": 1}), "designated: %s" % dict(cnt))
    fam = A.standing_family(S)
    standing = {k: v for k, v in fam.items() if "booked" not in k and int(k[:4]) <= 2024}
    sets = {frozenset(v[0]) for v in standing.values()}
    check("C2", sets == {frozenset(top)}, "standing family (replay and average calendars, fitted on three, four "
          "or five years, with and without day-of-week terms): %d members, %d distinct sets" % (len(standing),
                                                                                              len(sets)))
    thin = {k: v for k, v in fam.items() if "booked" not in k and int(k[:4]) > 2024}
    print("INFO   the same calendars fitted on 2025-2026 or 2026 alone: %d of %d members file the golden" %
          (sum(frozenset(v[0]) == frozenset(top) for v in thin.values()), len(thin)))
    booked = {k: v for k, v in fam.items() if "booked" in k and int(k[:4]) <= 2024}
    standing.update(booked)
    sets = {frozenset(v[0]) for v in standing.values()}
    check("C3", {frozenset(v[0]) for v in booked.values()} == {frozenset(top)},
          "the 2027 bookings alone as the calendar file the golden too (%d members)" % len(booked))
    short = {k: v for k, v in fam.items() if "booked" in k and int(k[:4]) > 2024}
    print("INFO   booked-only calendar on 2025-2026 or 2026 alone: %d of %d members file another set (a year "
          "with no event after the extract's bookings, outside the standing family)"
          % (sum(frozenset(v[0]) != frozenset(top) for v in short.values()), len(short)))

    # ------------------------------------------------------------------ R: the routes
    yr = S["yearly"]
    default = set(A.designate(ids, [yr[2026][s] for s in ids])[0])
    dcnt = collections.Counter(role.get(s, "-") for s in default)
    check("R0", dcnt == collections.Counter({"C": 14, "G": 6}), "the 2026 count designates %s" % dict(dcnt))
    routes = A.route_sets(S)
    for k in ("count 2025", "count 2026", "mean 2022-2026", "mean 2024-2026", "shrunk mean", "trend",
              "last 365 days"):
        check("R0", set(routes[k]) == default, "%s files the default set" % k)
    for k in ("2026 scaled by nights", "Gardens excess removed"):
        check("R1", set(routes[k]) != top, "%s files another set (%s)" %
              (k, dict(collections.Counter(role.get(s, "-") for s in routes[k]))))
    # the clean truth: the same easy route on the generator's true counts
    true_y = collections.Counter((s, d.year) for s, d, p in w["crimes"])
    tdef = set(sorted(ids, key=lambda s: (-true_y[(s, 2026)], s))[:20])
    check("R0t", tdef == default and tdef != top, "analyst test on the clean truth: the 2026 count files the default")
    # proximity: the Gardens six replaced by the six segments nearest the Lakeshore Centre
    segs = P.segs
    lk = next(s for s in w["segs"] if s["key"] == W.LAKESHORE["seg"])
    near = sorted(ids, key=lambda s: (float(segs[s]["x_utm17n"]) - lk["x"]) ** 2 +
                  (float(segs[s]["y_utm17n"]) - lk["y"]) ** 2)
    prox = {s for s in default if role.get(s) != "G"} | set(near[:6])
    check("R2", prox != top, "proximity swap files another set (%d of the golden)" % len(prox & top))
    back = len(set(routes["count 2025"]) & default)
    check("R3", back >= 18, "back-test: the 2025 ranking recovers %d of 2026's top 20" % back)
    # the shock test: the golden set is not the top 20 of any one shipped statistic
    base_e, eg, el = A.decompose(S["m"], S["nights"])
    gi = A.indicators(S["nights"], "G").astype(bool)
    li = A.indicators(S["nights"], "L").astype(bool)
    stats = {"2026 count": [yr[2026][s] for s in ids], "2025 count": [yr[2025][s] for s in ids],
             "five-year total": S["m"].sum(axis=1), "steady rate": base_e, "Gardens excess": eg,
             "Lakeshore excess": el, "crimes on Gardens nights": S["m"][:, gi].sum(axis=1),
             "crimes on Lakeshore nights": S["m"][:, li].sum(axis=1),
             "crimes on other nights": S["m"][:, ~(gi | li)].sum(axis=1)}
    hits = [k for k, v in stats.items() if set(A.designate(ids, np.asarray(v, float))[0]) == top]
    check("SHOCK", not hits, "the golden 20 is the top of no single statistic (%d sorted)" % len(stats))

    # ------------------------------------------------------------------ M: margins and pool
    order = S["order"]
    exp = S["exp"]
    gap = exp[order[19]] - exp[order[20]]
    check("M1", gap >= 8, "cut margin %.1f expected crimes (20th %.1f, 21st %.1f)" % (gap, exp[order[19]],
                                                                                      exp[order[20]]))
    check("M2", top <= set(S["pool"]), "the designated are candidates (pool %d)" % len(S["pool"]))
    outside = [s for s in ids if s not in S["pool"] and exp[s] >= exp[order[19]]]
    check("M3", not outside, "no segment outside the pool reaches the cut")
    check("SF10", set(A.designate(S["pool"], [exp[s] for s in S["pool"]])[0]) == top,
          "designating from the candidates or from every segment files the same 20")
    check("SF11", gap > 0.5, "no tie at the cut")

    # ------------------------------------------------------------------ SF: the fork table
    def call_under(crimes):
        ids2, m2 = A.daily_matrix(P, crimes)
        return set(A.designate(ids2, A.expected_2027(m2, S["nights"]))[0])

    latest, first = {}, {}
    for r in P.rms:
        k = r["occurrence_no"]
        v = int(r["version"])
        if k not in latest or v > int(latest[k]["version"]):
            latest[k] = r
        if k not in first or v < int(first[k]["version"]):
            first[k] = r

    def crimes_from(rows, unf_any=False, legacy=True, date_by="occ", all_versions=False):
        out = []
        unf = {r["occurrence_no"] for r in P.rms if r["status"] == "UNFOUNDED"} if unf_any else set()
        for r in rows:
            code = P.xwalk.get(r["offence_code"], r["offence_code"]) if legacy else r["offence_code"]
            if code not in A.PATROL or r["status"] == "UNFOUNDED" or not r["segment_id"]:
                continue
            if r["occurrence_no"] in unf:
                continue
            t = r["occurred_from"] or r["reported"] if date_by == "occ" else r["reported"]
            d = A.parse_t(t).date()
            if A.D0 <= d <= A.D1:
                out.append((int(r["segment_id"]), d))
        return out

    check("SF1", call_under(crimes_from(latest.values(), unf_any=True)) == top,
          "founded: dropping every occurrence unfounded on any version files the same call")
    legacy_codes = {r["offence_code"] for r in P.rms if not r["offence_code"].isdigit()}
    check("SF2", legacy_codes <= set(P.xwalk), "every legacy code in the export reads through the crosswalk "
          "(protocol section 3 files the reading); %d legacy codes" % len(legacy_codes))
    print("INFO   legacy-coded occurrences dropped instead: %s" %
          ("same call" if call_under(crimes_from(latest.values(), legacy=False)) == top else "another call"))
    check("SF3", call_under(crimes_from(P.rms)) == top, "every version counted files the same call")
    check("SF4", call_under(crimes_from(latest.values(), date_by="rep")) == top,
          "dated by the report date files the same call")
    fl = []
    for k, r in latest.items():
        f = first[k]
        rr = dict(r)
        rr["segment_id"] = f["segment_id"]
        fl.append(rr)
    check("SF5", call_under(crimes_from(fl)) == top, "the first version's segment files the same call")
    check("SF6", call_under(A.conform(P, legacy_dayfirst=False)) == top,
          "legacy dates read month first files the same call")
    check("SF7", sets == {frozenset(top)}, "the 2027 calendar replayed from 2026 or averaged over five years: "
          "same call (C2), and booked-only on three years or more (C3)")
    check("SF8", all(set(v[0]) == top for k, v in standing.items()), "fitting windows of three to five years")
    check("SF9", all(set(v[0]) == top for k, v in standing.items() if k.endswith("dow")),
          "day-of-week terms in the fit")

    # ------------------------------------------------------------------ the venue nights' conventions
    def call_nights(nights):
        return set(A.designate(ids, A.expected_2027(S["m"], nights))[0])

    hockey = {"G": set(S["nights"]["MG"]), "L": set(S["nights"]["ML"]), "MG": S["nights"]["MG"],
              "ML": S["nights"]["ML"]}
    hockey["G"] |= {d for d in S["nights"]["G"] if d.year == 2027}
    hockey["L"] |= {d for d in S["nights"]["L"] if d.year == 2027}
    l_hockey = sum(1 for d in S["nights"]["ML"] if d.year <= 2026)
    check("SF18", l_hockey == 0 and len({d for d in S["nights"]["L"] if d.year <= 2026}) > 40,
          "an event night is any EVENT duty at the venue: the Lakeshore Centre had %d hockey nights before 2027 and "
          "%d show nights, so the Mariners' games alone leave the Lakeshore excess unidentified (that model files %s)"
          % (l_hockey, len({d for d in S["nights"]["L"] if d.year <= 2026}),
             "the golden" if call_nights(hockey) == top else "another call"))
    new_layout = {k: {d for d in v if d.year >= 2024} for k, v in S["nights"].items()}
    ex = A.expected_2027(S["m"], new_layout, 2024, 2026)
    check("SF19", set(A.designate(ids, ex)[0]) == top, "the old layout's venue names (MEM GARDENS, LAKESHORE CTR) "
          "missed: the 2024 to 2026 fit on the Duty Desk sheets files the same call")
    both = S["nights"]["G"] & S["nights"]["L"]
    nb = {k: (v - both if k in ("G", "L") else v) for k, v in S["nights"].items()}
    check("SF20", call_nights(nb) == top, "%d nights with both venues busy, counted for both or for neither: same "
          "call" % len(both))

    # ------------------------------------------------------------------ the 2027 night counts the write-up names
    base_e, eg, el = A.decompose(S["m"], S["nights"])
    held = 0
    for nl in range(20, 61):
        for ng in range(0, 11):
            held += set(A.designate(ids, base_e * 365 + eg * ng + el * nl)[0]) == top
    check("C4", held == 41 * 11, "the same 20 for every 2027 count of 20 to 60 Lakeshore and 0 to 10 Gardens nights "
          "(%d of %d)" % (held, 41 * 11))

    # ------------------------------------------------------------------ the CAD's clocks
    neg = before = 0
    for r in P.cad:
        if not r["unit"]:
            continue
        rec, dsp = A.utc_of(r["received_utc"]), A.utc_of(r["dispatched_utc"])
        steps = [A.utc_of(r[c]) for c in ("dispatched_utc", "enroute_utc", "onscene_utc", "cleared_utc") if r[c]]
        neg += any(y < x for x, y in zip(steps, steps[1:]))
        before += dsp < rec
    check("T1", neg == 0 and before == 0, "every unit row runs forward: dispatch, en route, on scene, clear (%d rows "
          "out of order), and no unit is dispatched before its call's receipt (%d)" % (neg, before))
    stamps = [r for r in P.cad if r["unit"] and r["dispatched_utc"].endswith("Z") and r["cleared_utc"].endswith("Z")]
    check("SF23", len(stamps) == sum(1 for r in P.cad if r["unit"]) and neg == 0,
          "every unit stamp is UTC and runs forward, so a unit's hours are the elapsed time between its stamps on "
          "either side of a clock change")
    seen, back = [], 0
    for r in P.cad:
        if not seen or seen[-1][0] != r["event_no"]:
            seen.append((r["event_no"], A.utc_of(r["received_utc"])))
    back = sum(1 for x, y in zip(seen, seen[1:]) if y[1] < x[1])
    check("T2", back == 0, "events are numbered in the order they were received, through both clock changes (%d "
          "out of order)" % back)
    quiet = sum(1 for r in P.cad if r["unit"] and r["source"] != "OFFICER" and
                A.parse_utc(r["dispatched_utc"]).replace(tzinfo=None).strftime("%Y-%m-%d %H") == "2026-03-09 00")
    check("T3", quiet == 0, "no unit is dispatched to a call in the first hour of 9 March, where a night tour dated by "
          "a day of elapsed time lands on 7 March")
    cr = A.crews(P)
    calls = [r for r in P.cad if r["unit"] and r["source"] != "OFFICER"]
    apart, parted = 0, []
    for r in calls:
        d0 = A.parse_utc(r["dispatched_utc"])
        c0 = cr.get(A.tour_of(d0) + (r["unit"],))
        for name, f in A.TOUR_READINGS.items():
            if cr.get(f(d0) + (r["unit"],)) != c0:
                apart += 1
                parted.append((r["event_no"], r["unit"], name))
    check("SF24", apart == 0, "every unit on a call for service, the City's and Elmvale's, is crewed alike on every "
          "reading of its tour's date (%s): %d rows part%s" %
          (", ".join(A.TOUR_READINGS), apart, (" " + str(parted[:6])) if parted else ""))
    twelve = sum(1 for r in calls if A.tours_twelve_elapsed(A.parse_utc(r["dispatched_utc"])) !=
                 [A.tour_of(A.parse_utc(r["dispatched_utc"]))])
    check("T4", twelve == 0, "with each tour taken as twelve hours of elapsed time from its start, every unit on a call "
          "for service is dispatched in its own tour and no other (%d rows in none, two or another)" % twelve)
    two = lambda d: sum(1 for r in P.roster if r["tour_date"] == d and r["tour"] == "N" and r["officer_2"])
    print("INFO   two-officer cars on the night tours around the spring change: 7 March %d, 8 March %d, 9 March %d" %
          (two("2026-03-07"), two("2026-03-08"), two("2026-03-09")))

    # ------------------------------------------------------------------ the ask
    (ga,) = A.asks(P)
    (ra,) = A.asks_raw(P)
    (ca,) = A.asks(P, by_district=False, naive_tour=True)
    check("D1", all(ga[k] != ca[k] for k in ga), "ask A: the cracker (each unit crewed from the roster's tour of the "
          "dispatch's own date) misses %d of 32" % sum(ga[k] != ca[k] for k in ga))
    (rn,) = A.asks_raw(P, by_district=False, naive_tour=True)
    check("D1b", min(abs(rn[k] - ra[k]) for k in ra) >= 1.0, "ask A: crews from the dispatch's own date move every "
          "cell by at least an hour (smallest %.2f)" % min(abs(rn[k] - ra[k]) for k in ra))
    (da,) = A.asks(P, by_district=True, naive_tour=False)
    print("INFO   ask A: Elmvale's events read into the wards by their district would move %d of 32 (Directive "
          "PO-14 files that a call outside the City's wards belongs to none)" % sum(ga[k] != da[k] for k in ga))
    readings = {"keep": A.ask_officer_hours(P), "drop": A.ask_officer_hours(P, intervals="drop"),
                "clip": A.ask_officer_hours(P, intervals="clip")}
    for name, f in A.TOUR_READINGS.items():
        readings["tours dated " + name] = A.ask_officer_hours(P, tour=f)
    moved = {n: [k for k in ga if int(A.half_up(v[k])) != ga[k]] for n, v in readings.items()}
    check("D3", not any(moved.values()), "every cell holds at its rounding under %s (%s)" %
          (", ".join(readings), "; ".join("%s %d" % (n, len(m)) for n, m in moved.items())))
    spread = max(abs(v[k] - ra[k]) for v in readings.values() for k in ra)
    check("D4", spread < 1e-6, "the %d readings agree to %.2g hours in every cell" % (len(readings), spread))
    wh = A.ask_officer_hours(P, wall_hours=True)
    across = sum(1 for r in calls if A.tour_of(A.parse_utc(r["dispatched_utc"]))[0] in
                 (dt.date(2026, 3, 7), dt.date(2026, 10, 31)) and
                 A.parse_utc(r["cleared_utc"]).utcoffset() != A.parse_utc(r["dispatched_utc"]).utcoffset())
    check("D5", all(int(A.half_up(wh[k])) == ga[k] for k in ga), "a unit's hours read as the difference of its local "
          "wall-clock times hold every cell (%d unit rows on calls work across a change; largest cell shift %.2f)" %
          (across, max(abs(wh[k] - ra[k]) for k in ra)))
    keys = collections.Counter((r["tour_date"], r["tour"], r["unit"]) for r in P.roster)
    check("T5", max(keys.values()) == 1, "the roster holds one row per tour and unit (%d rows), so a join on the tour "
          "and the unit repeats no call" % len(P.roster))
    edge = min(abs((v % 1) - 0.5) for v in ra.values())
    check("M4", edge >= 0.25, "every officer-hours cell sits at least a quarter of an hour from its rounding edge "
          "(nearest %.3f)" % edge)
    officer = [r for r in P.cad if r["source"] == "OFFICER"]
    check("SF12", len(officer) > 0, "officer-started events exist and are not calls (Directive PO-14, section 2)")
    utc_year = sum(1 for r in P.cad if r["received_utc"].startswith("2027"))
    check("SF13", utc_year > 0, "calls received late on 31 December 2026 local carry 2027 UTC stamps (%d rows); a "
          "call's date is its local receipt date (Directive PO-14, section 2)" % utc_year)
    n25 = [r for r in P.roster if r["tour_date"] == "2025-12-31"]
    check("SF14", n25 and all(r["tour"] == "N" for r in n25), "the roster's only 2025 rows are the night tour of "
          "31 December, which covers 1 January 2026 from midnight: a night tour is dated by its start")
    twp = sum(1 for r in P.cad if r["segment_id"] and int(r["segment_id"]) not in P.segs)
    check("SF15", twp > 0, "%d CAD rows sit at addresses outside the City's street file; a call outside the City's "
          "wards belongs to none (Directive PO-14, section 2)" % twp)
    crossing = 0
    for r in P.cad:
        if not r["unit"]:
            continue
        d0, d1 = A.parse_utc(r["dispatched_utc"]), A.parse_utc(r["cleared_utc"])
        if A.tour_of(d0) != A.tour_of(d1 - dt.timedelta(seconds=1)):
            crossing += 1
    check("SF22", crossing == 0, "no unit assignment runs across a tour change, so the crew at dispatch is the "
          "crew throughout")
    check("SF21", abs(sum(ra.values()) - sum(ga.values())) < 32, "officer-hours are dispatch to clear times crew")

    # ------------------------------------------------------------------ X: patterns and documents
    sid = sorted(ids)
    steps = set(np.diff(sid).tolist())
    check("X1", len(steps) > 50, "segment ids carry no fixed step")
    nums = sorted(int(r["occurrence_no"][-6:]) for r in latest.values() if r["occurrence_no"].startswith("MP26"))
    check("X2", len(set(np.diff(nums).tolist())) > 3, "occurrence numbers carry gaps of several sizes")
    mins = collections.Counter(r["reported"][-2:] for r in P.rms)
    check("X3", len(mins) >= 55, "report times spread over the minutes of the hour")
    for fn in ("hot_spot_patrol_protocol_2027.pdf", "patrol_measures_directive_po14.pdf"):
        data = open(os.path.join(TARGET, fn), "rb").read()
        c = re.search(rb"/CreationDate \(D:(\d{14})", data).group(1)
        mo = re.search(rb"/ModDate \(D:(\d{14})", data).group(1)
        check("X4", c < mo and b"ReportLab" not in data, "%s saved after it was created, no toolchain string" % fn)
    with zipfile.ZipFile(os.path.join(TARGET, "mps_paid_duty_register_2022_2027.xlsx")) as z:
        core = z.read("docProps/core.xml").decode()
    cr = re.search(r"<dcterms:created[^>]*>([^<]+)<", core).group(1)
    mo = re.search(r"<dcterms:modified[^>]*>([^<]+)<", core).group(1)
    check("X5", cr < mo, "the register workbook saved after it was created (%s, %s)" % (cr, mo))
    rows = sum(1 for _ in open(os.path.join(TARGET, "mps_rms_occurrences_2022_2026.csv"))) - 1
    check("X6", rows >= 25000, "the occurrence export holds %d rows" % rows)
    check("X7", fig["designated"] == sorted(S["top"]), "figures.json carries the designation")
    print("%s  task125 checks: %d run, %d failed" % ("PASS" if not FAILS else "FAIL", N[0], len(FAILS)))
    return 1 if FAILS else 0


def _mins(x):
    return int(x[:2]) * 60 + int(x[3:])


if __name__ == "__main__":
    sys.exit(main())
