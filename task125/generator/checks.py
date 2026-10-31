"""task125 generator checks, run on the cut pack in target/ against the generator's own truth.

    python3 task125/generator/checks.py

C: the conformed records equal the truth; the designation equals the truth's; the standing family files one set.
R: every route the ladder prices files its stated set (the analyst test on the clean truth included).
M: margins, the candidate pool, ties, rounding edges.
SF1 to SF22: the semantic fork table, each alternative shown to file the same call or figure, or ruled out.
D: the devices of the asks (the cracker misses every figure of asks A and B).
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

    # ------------------------------------------------------------------ asks
    ga, gb = A.asks(P)
    ra, rb = A.asks_raw(P)
    ca, cb = A.asks(P, by_district=True, naive_tour=True)
    check("D1", all(ga[k] != ca[k] for k in ga), "ask A: the cracker (tour by the dispatch's own date, wards by "
          "district) misses %d of 32" % sum(ga[k] != ca[k] for k in ga))
    na, _ = A.asks(P, by_district=False, naive_tour=True)
    check("D1b", sum(ga[k] != na[k] for k in ga) >= 24, "ask A: the tour dating alone moves %d of 32" %
          sum(ga[k] != na[k] for k in ga))
    da, _ = A.asks(P, by_district=True, naive_tour=False)
    check("D1c", sum(ga[k] != da[k] for k in ga) >= 24, "ask A: the districts alone move %d of 32" %
          sum(ga[k] != da[k] for k in ga))
    check("D2", all(gb[k] != cb[k] for k in gb), "ask B: the districts move %d of 8 medians (by %s)" %
          (sum(gb[k] != cb[k] for k in gb), ", ".join("%.1f" % (cb[k] - gb[k]) for k in sorted(gb))))
    edge_a = [k for k, v in ra.items() if abs((v % 1) - 0.5) < 0.01]
    edge_b = [k for k, v in rb.items() if abs(((v * 10) % 1) - 0.5) < 0.01]
    check("M4", not edge_a and not edge_b, "no ask figure within a hair of its rounding edge (%s %s)" %
          (edge_a, edge_b))
    officer = [r for r in P.cad if r["source"] == "OFFICER" and r["priority"] == "1"]
    check("SF12", len(officer) > 0, "officer-started priority 1 events exist and are not calls (Directive PO-14, section 2)")
    utc_year = sum(1 for r in P.cad if r["received_utc"].startswith("2027"))
    check("SF13", utc_year > 0, "calls received late on 31 December 2026 local carry 2027 UTC stamps (%d rows); a "
          "call's date is its local receipt date (Directive PO-14, section 2)" % utc_year)
    n25 = [r for r in P.roster if r["tour_date"] == "2025-12-31"]
    check("SF14", n25 and all(r["tour"] == "N" for r in n25), "the roster's only 2025 rows are the night tour of "
          "31 December, which covers 1 January 2026 from midnight: a night tour is dated by its start")
    twp = sum(1 for r in P.cad if r["segment_id"] and int(r["segment_id"]) not in P.segs)
    check("SF15", twp > 0, "%d CAD rows sit on segments outside the street file; a ward counts the calls at addresses in it "
          "(Directive PO-14, section 2)" % twp)
    check("SF16", all(r["priority"] in "1234" for r in P.cad), "priority is the dispatched priority (Directive PO-14, section 2)")
    crossing = 0
    for r in P.cad:
        if not r["unit"]:
            continue
        d0, d1 = A.parse_utc(r["dispatched_utc"]), A.parse_utc(r["cleared_utc"])
        if A.tour_of(d0) != A.tour_of(d1 - dt.timedelta(seconds=1)):
            crossing += 1
    check("SF22", crossing == 0, "no unit assignment runs across a tour change, so the crew at dispatch is the "
          "crew throughout")
    cb2 = A.ask_p1(P)
    check("SF17", all(abs(cb2[k] - rb[k]) < 1e-9 for k in rb), "the first arrival is the earliest onscene of any "
          "unit, sergeants included")
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
