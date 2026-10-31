"""The generator's assertions on the cut pack: the golden call, the ladder's routes and margins, the reflex sweep
(every cheap route files a wrong set), the decisive family's convergence, the semantic fork table's rows (SF ids),
the shock and separation tests, and every ask device's stops.

    python3 task191/generator/checks.py
"""
import datetime as dt
import math
import os
import sys
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import estim as E   # noqa: E402

PASSED = []
FAILED = []


class Segments2025(E.Segments):
    """Red 2025's physical segments and the operated trips over each, for the months before the network change."""

    def __init__(self, D, w0, w1):
        st = D["stops"]
        lat0 = np.mean([v[0] for v in st.values()])
        self.kx = 111_320.0 * math.cos(math.radians(lat0))
        self.ky = 111_320.0
        self.lat0, self.lon0 = lat0, np.mean([v[1] for v in st.values()])
        self.periods = {k: [tuple(sorted((s[i], s[i + 1]))) for i in range(len(s) - 1)] for k, s in D["seq25"].items()}
        keys = set()
        for v in self.periods.values():
            keys.update(v)
        self.keys = sorted(keys)
        self.index = {k: i for i, k in enumerate(self.keys)}
        self.A = np.array([self.xy(*st[k[0]][:2]) for k in self.keys])
        self.B = np.array([self.xy(*st[k[1]][:2]) for k in self.keys])
        self.L = np.hypot(*(self.B - self.A).T)
        self.passes = np.zeros(len(self.keys))
        for r in D["return"]:
            day = E.dmy(r["fecha"])
            if w0 <= day <= w1 and (r["linea"], r["sentido"]) in self.periods:
                for sg in self.periods[(r["linea"], r["sentido"])]:
                    self.passes[self.index[sg]] += int(r["expediciones_realizadas"])
        self.new = np.zeros(len(self.keys), dtype=bool)


def check(name, ok, detail=""):
    (PASSED if ok else FAILED).append(name)
    print("%s  %s  %s" % ("ok  " if ok else "FAIL", name, detail))


def main():
    D = E.load()
    c = E.call(D)
    ws, S, pl = c["ws"], c["S"], c["places"]
    gold = c["taken"]
    res = c["res"]
    check("G1 golden set", gold == ["San Lázaro"], str(gold))
    check("G2 closest depot left out", c["closest"] == "La Ribera", c["closest"])
    check("G3 four fixed false-trigger places", len(c["false"]) == 4,
          ", ".join("%d %.3f" % (p["n"], p["share"]) for p in c["false"]))
    slz = res["San Lázaro"]["ratio"]
    others = max(v["ratio"] for d, v in res.items() if d != "San Lázaro")
    check("M1 golden margin above the line", slz >= E.RATIO + 0.4, "%.4f" % slz)
    check("M2 golden margin below the line", others <= E.RATIO - 0.10, "%.4f" % others)
    # Rung 0: every collision warning.
    r0, f0, *_ = E.rates(ws)
    s0 = E.taken(r0)
    check("R0 the dashboard measure files Hornacho and Valdeolmos", s0 == ["Hornacho", "Valdeolmos"], str(s0))
    check("R0 margins", min(r0["Hornacho"]["ratio"], r0["Valdeolmos"]["ratio"]) >= 1.40
          and r0["San Lázaro"]["ratio"] <= 1.20, "HOR %.3f VDO %.3f SLZ %.3f" %
          (r0["Hornacho"]["ratio"], r0["Valdeolmos"]["ratio"], r0["San Lázaro"]["ratio"]))
    # Rung 1: the busiest places set aside, every k.
    busy = [p for p in pl if p["n"] >= 150]
    wrong_k = []
    for k in range(1, 9):
        drop = set().union(*[p["ids"] for p in busy[:k]])
        s = E.taken(E.rates(ws, drop)[0])
        wrong_k.append((k, s))
    check("R1 every top-k busiest-place cut files a wrong set", all(s != gold for _, s in wrong_k),
          "; ".join("k%d %s" % (k, "/".join(x[:3] for x in s)) for k, s in wrong_k))
    k5 = E.taken(E.rates(ws, set().union(*[p["ids"] for p in busy[:5]]))[0])
    r1 = E.rates(ws, set().union(*[p["ids"] for p in busy[:5]]))[0]
    check("R1 the five busiest out files La Ribera", k5 == ["La Ribera"], "%s %.3f" % (k5, r1["La Ribera"]["ratio"]))
    check("R1 margin", r1["La Ribera"]["ratio"] >= E.RATIO + 0.08, "%.4f" % r1["La Ribera"]["ratio"])
    # Rung 1b: places the drivers ignore set aside, every threshold.
    wrong_t = []
    for t100 in range(50, 100):
        t = t100 / 100.0
        drop = set().union(*[p["ids"] for p in busy if p["nobrake"] >= t]) if any(p["nobrake"] >= t for p in busy) else set()
        s = E.taken(E.rates(ws, drop)[0])
        wrong_t.append((t, s))
    check("R1b every ignored-place cut files a wrong set", all(s != gold for _, s in wrong_t),
          "distinct sets %s" % sorted({"/".join(x[:3] for x in s) for _, s in wrong_t}))
    plaza = [p for p in pl if p["share"] < 0.1 and p["nobrake"] > 0.9]
    check("R1b the Plaza is ignored more than every false place", plaza and min(p["nobrake"] for p in plaza) >
          max(p["nobrake"] for p in c["false"]) + 0.05, "plaza %s false max %.3f" %
          (["%.3f" % p["nobrake"] for p in plaza], max(p["nobrake"] for p in c["false"])))
    check("R1 the Plaza is busier than the smallest false place", plaza and plaza[0]["n"] > min(p["n"] for p in c["false"]) + 300,
          "plaza %d false min %d" % (plaza[0]["n"], min(p["n"] for p in c["false"])))
    # Type, speed and network-change cuts.
    for name, keep in [("PCW only", lambda w: w["pcw"]), ("FCW only", lambda w: not w["pcw"]),
                       ("below 25 km/h", lambda w: w["speed"] < 25), ("20 km/h and over", lambda w: w["speed"] >= 20)]:
        drop = {w["eid"] for w in ws if not keep(w)}
        s = E.taken(E.rates(ws, drop)[0])
        check("R2 %s files a wrong set" % name, s != gold, str(s))
    drop = {w["eid"] for w in ws if S.new[w["seg"]]}
    s = E.taken(E.rates(ws, drop)[0])
    check("R2 Red 2026's new segments set aside files a wrong set", s != gold, str(s))
    # Places that first fired in 2026: the Plaza is one of them.
    ws25 = E.collision_warnings(D, dt.date(2025, 10, 1), dt.date(2025, 12, 13))
    old_cells = set()
    for w in ws25:
        old_cells.add((round(w["lat"], 3), round(w["lon"], 3)))
    new_busy = [p for p in busy if not any((round(w["lat"], 3), round(w["lon"], 3)) in old_cells
                                         for w in ws if w["eid"] in list(p["ids"])[:20])]
    s = E.taken(E.rates(ws, set().union(*[p["ids"] for p in new_busy]) if new_busy else set())[0])
    check("R2 places new in 2026 set aside files a wrong set", s != gold, "%d places, %s" % (len(new_busy), s))
    # Decisive family: per-pass share at every threshold and bin size, and whole segments.
    fam = []
    for bin_m in (5.0, 10.0, 20.0):
        plb = E.places(ws, S, bin_m=bin_m)
        for th in (0.05, 0.08, 0.10, 0.15, 0.20, 0.24):
            fp = E.false_places(plb, th)
            drop = set().union(*[p["ids"] for p in fp]) if fp else set()
            rr = E.rates(ws, drop)[0]
            fam.append((bin_m, th, E.taken(rr), tuple(rr[d]["n"] for d in E.DEPOT_ORDER)))
    gold_n = tuple(res[d]["n"] for d in E.DEPOT_ORDER)
    check("C1 the decisive family files the golden set", all(f[2] == gold for f in fam),
          "%d members" % len(fam))
    check("C2 the decisive family files the golden counts", all(f[3] == gold_n for f in fam), "")
    seg_share = defaultdict(int)
    for w in ws:
        seg_share[w["seg"]] += 1
    whole = {i for i, n in seg_share.items() if S.passes[i] and n / S.passes[i] >= 0.10}
    drop = {w["eid"] for w in ws if w["seg"] in whole}
    rr = E.rates(ws, drop)[0]
    check("C3 SF9 whole segments at a share of 0.10 give the same set and counts",
          E.taken(rr) == gold and tuple(rr[d]["n"] for d in E.DEPOT_ORDER) == gold_n, str(sorted(whole)))
    # The gap: the smallest false-place share against the largest other place, overall and in the firing hours.
    others_pl = [p for p in pl if p not in c["false"]]
    gap = min(p["share"] for p in c["false"]) / max(p["share"] for p in others_pl)
    check("C4 share gap overall", gap >= 6.0, "%.2f" % gap)
    # Passes by hour for each place's segment, from the departures' spread: in-hours share needs the hour profile of
    # the trips, which the return does not hold; price it on the Plaza's market hours (08:00 to 15:00, Monday to
    # Saturday) against an even spread of the day's trips over 06:00 to 24:00.
    pz = plaza[0]
    frac_hours = (7 / 18.0) * (6 / 7.0)
    in_share = pz["share"] / frac_hours
    check("C5 share gap in the Plaza's market hours", min(p["share"] for p in c["false"]) >= 2.5 * in_share,
          "plaza in hours %.4f false min %.4f" % (in_share, min(p["share"] for p in c["false"])))
    # Semantic forks.
    raw = list(D["warnings"])
    D2 = dict(D)
    D2["warnings"] = raw
    # SF1: re-sent messages kept as warnings.
    seen = defaultdict(int)
    for r in raw:
        seen[r["event_id"]] += 1
    dup = sum(1 for v in seen.values() if v > 1)
    check("SF1 re-sent messages exist and one event is one warning", dup > 500, "%d events sent twice" % dup)
    # SF2: the window read on UTC dates.
    wsu = E.collision_warnings(D, utc_dates=True)
    S.snap(wsu)
    fpu = E.false_places(E.places(wsu, S))
    ru = E.rates(wsu, set().union(*[p["ids"] for p in fpu]))[0]
    check("SF2 the window read on UTC dates gives the same set", E.taken(ru) == gold,
          "%d warnings against %d" % (len(wsu), len(ws)))
    # SF3: depot by home allocation, ignoring loans.
    home = {}
    for fno, lst in D["alloc"].items():
        home[fno] = lst[0][2] if len(lst) < 3 else lst[0][2]
    ws_home = [dict(w, dep=home[w["fleet"]] if len(D["alloc"][w["fleet"]]) == 3 else w["dep"]) for w in ws]
    drop = set().union(*[p["ids"] for p in c["false"]])
    rr = E.rates(ws_home, drop)[0]
    check("SF3 a lent bus read at its home depot gives the same set", E.taken(rr) == gold, str(E.taken(rr)))
    # SF4: firmware 2.x brake within the capture window rather than two seconds.
    n2000 = sum(1 for r in raw if r["brake_reaction_ms"] == "2000")
    check("SF4 no reaction time sits at exactly 2,000 ms", n2000 == 0, str(n2000))
    late = {r["event_id"] for r in raw if r["brake_reaction_ms"] and int(r["brake_reaction_ms"]) > 2000}
    ws_cap = [dict(w, braked=w["braked"] or w["eid"] in late) for w in ws]
    rr = E.rates(ws_cap, drop)[0]
    check("SF4 a brake within the 3,000 ms capture read as braked gives the same set", E.taken(rr) == gold, str(E.taken(rr)))
    # SF5: headway warnings counted as collision warnings.
    D3 = dict(D)
    E.COLLISION.update({"HMW", "HEADWAY"})
    ws_h = E.collision_warnings(D3)
    E.COLLISION.difference_update({"HMW", "HEADWAY"})
    S.snap(ws_h)
    plh = E.places(ws_h, S)
    fph = E.false_places(plh)
    rr = E.rates(ws_h, set().union(*[p["ids"] for p in fph]))[0]
    check("SF5 headway warnings counted gives the same set", E.taken(rr) == gold, str(E.taken(rr)))
    # SF6: the fleet's rate as the mean of depot rates.
    mean_rate = sum(v["rate"] for v in res.values()) / len(res)
    s6 = sorted(d for d, v in res.items() if v["rate"] / mean_rate >= E.RATIO)
    check("SF6 the fleet's rate as a mean of depot rates gives the same set", s6 == gold, str(s6))
    # SF7: 1.3 inclusive.
    check("SF7 no depot within 0.05 of 1.3", all(abs(v["ratio"] - E.RATIO) > 0.05 for v in res.values()), "")
    # SF8: genuine read as the warnings drivers act on (places drivers ignore set aside): a different set, ruled out by
    # the terms' definition (a pedestrian in the shared space is in the path whether or not drivers brake).
    check("SF8 places drivers ignore set aside files another set", all(s != gold for _, s in wrong_t), "")
    # SF10: firmware 1.x rows carry Y or N.
    bad = sum(1 for r in raw if r["firmware"].startswith("1.") and r["warning_type"] in E.COLLISION and r["brake_2s"] not in ("Y", "N"))
    check("SF10 every firmware 1.x collision warning carries Y or N", bad == 0, str(bad))
    # SF11: the passes a place's share is read on: every operated trip of every line and direction over its segment
    # in the window (golden), against the trips programmed, one direction's trips, and the trips since the place first
    # fired. Each keeps the same places at or over the share of 0.10, so the same set and counts.
    by_day = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for r in D["return"]:
        day = E.dmy(r["fecha"])
        if not (E.W0 <= day <= E.W1):
            continue
        for (line, sentido, a, b), segs in S.periods.items():
            if line == r["linea"] and sentido == r["sentido"] and a <= day <= b:
                for sg in segs:
                    cell = by_day[S.index[sg]][day]
                    cell[0] += int(r["expediciones_realizadas"])
                    cell[1] += int(r["expediciones_programadas"])
                break
    first = {}
    for p in pl:
        first[id(p)] = min(w["day"] for w in ws if w["eid"] in p["ids"])
    gold_fp = sorted(id(p) for p in c["false"])
    alts = {}
    alts["operated, rebuilt"] = [p for p in pl if p["n"] / sum(v[0] for v in by_day[p["seg"]].values()) >= 0.10]
    alts["programmed"] = [p for p in pl if p["n"] / sum(v[1] for v in by_day[p["seg"]].values()) >= 0.10]
    alts["one direction"] = [p for p in pl if 2 * p["share"] >= 0.10]
    alts["since first fired"] = [p for p in pl if p["n"] / sum(v[0] for d, v in by_day[p["seg"]].items()
                                                                   if d >= first[id(p)]) >= 0.10]
    same = {k: sorted(id(p) for p in v) == gold_fp for k, v in alts.items()}
    top_other = max(max(2 * p["share"], p["n"] / sum(v[0] for d, v in by_day[p["seg"]].items() if d >= first[id(p)]))
                    for p in pl if p not in c["false"])
    check("SF11 the passes read programmed, one way or since a place first fired class the same places",
          all(same.values()), "%s; largest other place under any %.4f" % (same, top_other))
    # Back-test: on the months before Red 2026 (1 October to 13 December 2025) the textbook route validates: no place
    # fires on a tenth of the buses passing it, so the dashboard measure and the per-pass reading file the same set.
    b0, b1 = dt.date(2025, 10, 1), dt.date(2025, 12, 13)
    wb = E.collision_warnings(D, b0, b1)
    S25 = Segments2025(D, b0, b1)
    S25.snap(wb)
    for mc in (10, 30):
        plb = E.places(wb, S25, min_count=mc)
        fpb = E.false_places(plb)
        rb0 = E.taken(E.rates(wb)[0])
        rb3 = E.taken(E.rates(wb, set().union(*[p["ids"] for p in fpb]) if fpb else set())[0])
        check("B1 back-test before Red 2026 (places of %d or more): no place at a tenth of passes, both routes agree" % mc,
              not fpb and rb0 == rb3, "largest share %.4f, %s and %s" % (max(p["share"] for p in plb), rb0, rb3))
    # Shock: San Lázaro tops no simple statistic.
    stats = {}
    n_all = defaultdict(int)
    nb_all = defaultdict(int)
    pc = defaultdict(int)
    for w in ws:
        n_all[w["dep"]] += 1
        nb_all[w["dep"]] += 0 if w["braked"] else 1
        pc[w["dep"]] += 1 if w["pcw"] else 0
    stats["warnings"] = n_all
    stats["not braked"] = nb_all
    stats["no-brake share"] = {d: nb_all[d] / n_all[d] for d in n_all}
    stats["pedestrian share"] = {d: pc[d] / n_all[d] for d in n_all}
    tops = {k: max(v, key=v.get) for k, v in stats.items()}
    check("S1 San Lázaro tops no single depot statistic", all(t != "San Lázaro" for t in tops.values()), str(tops))
    # Ask devices.
    ga, _ = E.ask_a(D)
    for name, kw, need in [("DST", dict(dst=False), 7), ("relief overlap", dict(overlap=False), 28)]:
        a, _ = E.ask_a(D, **kw)
        moved = sum(1 for d in a for i in range(4) if a[d][i] != ga[d][i])
        check("A %s moves %d figures" % (name, need), moved >= need, str(moved))
    a, _ = E.ask_a(D, dst=False, overlap=False)
    kept = sum(1 for d in a for i in range(4) if a[d][i] == ga[d][i])
    check("A the cracker keeps no figure", kept == 0, str(kept))
    cb, pb, _ = E.ask_b(D)
    c1, p1, _ = E.ask_b(D, dedupe=False, chains=False)
    keep_b = sum(c1[d] == cb[d] for d in cb) + sum(p1[d] == pb[d] for d in pb)
    check("B the cracker keeps at most two figures", keep_b <= 2, str(keep_b))
    gc, _ = E.ask_c(D)
    c2, _ = E.ask_c(D, diversions=False)
    keep_c = sum(1 for d in c2 for i in range(4) if c2[d][i] == gc[d][i])
    check("C the cracker keeps at most two figures", keep_c <= 2, str(keep_c))
    print("\n%d checks, %d FAIL" % (len(PASSED) + len(FAILED), len(FAILED)))
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
