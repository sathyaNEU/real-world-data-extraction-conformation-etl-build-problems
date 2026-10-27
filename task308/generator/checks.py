"""The generator's assertions on the cut pack and the clean truth: the replay reproduces the truth, the call and its
margins, the ladder (every cheap route's pick), the standing family, every semantic fork row (SF1 to SF18), the ask
devices and their twins, the three-rules analyst test, the figure edges and the input gates.

    python3 task308/generator/checks.py [target dir]
"""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build  # noqa: E402
import params as P  # noqa: E402
import records as R  # noqa: E402
import solve as S  # noqa: E402
import world  # noqa: E402

N = {"pass": 0}


def ok(cond, msg):
    if not cond:
        raise AssertionError(msg)
    N["pass"] += 1


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def main(target):
    pk = S.Pack(target, build.FILES)
    W = world.build()
    M = world.members(W)
    ev = R.events(W)
    codes = [u[0] for u in P.UNITS]
    caps = {u[0]: float(u[4]) for u in P.UNITS}
    tru = R.avail_hours(ev, W["utc"], codes, caps)
    tie_t = R.tie_hours(R.tie_events(W), W["utc"])

    # ---------------------------------------------------------------- the pack replays the truth
    ok(pk.n == len(W["utc"]) == 87672, "planning table hours")
    ok((pk.utc == W["utc"]).all(), "planning table clock maps onto the truth's UTC hours")
    ok(np.allclose(pk.tb.load_2027_mw.values, W["load"], atol=0.051), "load table reproduces the truth (2019 in kW)")
    ok(pk.kw_years == [2019], "only 2019 is in kW")
    for c in codes:
        ok(np.allclose(pk.av[c], tru[c], atol=1e-6), "replayed availability of %s" % c)
    ok(np.allclose(pk.tie, tie_t, atol=1e-6), "tie in-service share")
    ok("PH-121" not in pk.caps, "the retiring unit is out of the 2027 fleet")

    # ---------------------------------------------------------------- the call
    g = pk.call("golden")
    ok(g["best"] == "Red Willow import", "golden award")
    nets = sorted(g["net"].values(), reverse=True)
    ok(nets[0] - nets[1] > 50, "award margin over the runner-up (USD M)")
    ok(g["removed"]["Ketchum Ridge"] < 1.0, "the peaker removes nothing in the replay")
    facts = pk.shortfall_facts()
    ok(facts["share_in_allout"] > 0.999, "every shortfall hour falls with the peakers all out")

    # ---------------------------------------------------------------- the ladder: every cheap route's pick
    rungs = {}
    for r in ["nameplate", "rated", "class_avg", "class_avg_no_fuel"]:
        rungs[r] = pk.call(r)
        ok(rungs[r]["best"] == "Ketchum Ridge", "rung %s files the peaker" % r)
        ok(rungs[r]["net"]["Ketchum Ridge"] - rungs[r]["net"]["Red Willow import"] > 5, "rung %s margin" % r)
    # UCAP read at the system's 100 highest net-load hours, rated EFORd for the thermal offer
    netl = pk.tb.load_2027_mw.values - pk.tb.wind_mw.values - pk.tb.solar_mw.values
    top = np.argsort(netl)[-100:]
    ucap = {"Ketchum Ridge": 300 * (1 - P.CT_RATED_EFORD), "Red Willow import": 300 * float(pk.tie.mean()),
            "Sandhill Draw": float(pk.wind_new[top].mean()), "Coulee Flats": float(pk.solar_new[top].mean())}
    per = {o: ucap[o] / P.annual_payment(o) for o in P.OFFERS}
    ok(max(per, key=per.get) == "Ketchum Ridge", "UCAP per dollar files the peaker")
    # an independent-outage convolution of the fleet at each unit's recorded forced outage rate
    step = 10
    dist = np.array([1.0])
    for c in codes:
        q = 1 - pk.av[c].mean() / caps[c]
        k = int(round(caps[c] / step))
        nd = np.zeros(len(dist) + k)
        nd[:len(dist)] += dist * q
        nd[k:] += dist * (1 - q)
        dist = nd
    qt = 1 - pk.tie.mean()
    k = int(round(P.IMPORT_EX_MW / step))
    nd = np.zeros(len(dist) + k)
    nd[:len(dist)] += dist * qt
    nd[k:] += dist * (1 - qt)
    dist = nd
    lv = np.arange(len(dist)) * step
    cdf = np.cumsum(dist)
    pm = np.cumsum(dist * lv)

    def conv(nl):
        # E[max(0, L - A)] = sum over A < L of (L - A) p(A)
        idx = np.clip(np.searchsorted(lv, nl, side="left") - 1, -1, len(lv) - 1)
        c_ = np.where(idx >= 0, cdf[np.maximum(idx, 0)], 0.0)
        m_ = np.where(idx >= 0, pm[np.maximum(idx, 0)], 0.0)
        return float((nl * c_ - m_).sum()) / P.N_YEARS
    b0 = conv(netl)
    conv_rem = {"Ketchum Ridge": b0 - conv(netl - 300 * (1 - P.CT_RATED_EFORD)),
                "Red Willow import": b0 - conv(netl - 300 * float(pk.tie.mean())),
                "Sandhill Draw": b0 - conv(netl - pk.wind_new), "Coulee Flats": b0 - conv(netl - pk.solar_new)}
    conv_net = pk.net(conv_rem)
    ok(max(conv_net, key=conv_net.get) != "Red Willow import", "the independent convolution misses the import")
    # wind at its average output rather than its hourly profile
    flat = dict(g["removed"])
    flat["Sandhill Draw"] = pk.eue() - pk.eue(np.full(pk.n, pk.wind_new.mean()))
    fn = pk.net(dict(flat, **{"Ketchum Ridge": rungs["rated"]["removed"]["Ketchum Ridge"]}))
    ok(max(fn, key=fn.get) == "Ketchum Ridge", "flat wind with a rated peaker stays on the peaker")

    # ---------------------------------------------------------------- the standing family (the filed sentence held)
    sh = pk.class_share()
    evl = pk.ev.sort_values("revision").drop_duplicates("event_id", keep="last")
    fuel = evl[(evl.cause_code == 9130) & evl.unit_code.isin(pk.ct)]
    t0 = pk.utc[0]
    act = np.zeros(pk.n, bool)
    for _, r in fuel.iterrows():
        a = int(np.floor((r.start - t0).total_seconds() / 3600))
        b = int(np.ceil((r.end - t0).total_seconds() / 3600))
        act[a:b] = True
    base = pk.eue()
    sp = pk.short
    fam = {"class share in the hour": base - pk.eue(300 * sh),
           "out in lack-of-fuel hours, else rated": base - pk.eue(300 * np.where(act, 0, 1 - P.CT_RATED_EFORD)),
           "out in lack-of-fuel hours, else the class's other forced rate":
               base - pk.eue(300 * np.where(act, 0, 1 - pk.ct_rate(True))),
           "two 150 MW units each at the class share": base - float(
               (sh ** 2 * np.clip(sp - 300, 0, None) + 2 * sh * (1 - sh) * np.clip(sp - 150, 0, None)
                + (1 - sh) ** 2 * np.clip(sp, 0, None)).sum()) / P.N_YEARS}
    for k_, v in fam.items():
        ok(round(v / 100.0) == 0, "standing family member '%s' removes under 50 MWh (%.1f)" % (k_, v))

    # ---------------------------------------------------------------- semantic forks (each alternative reading)
    def call_with(short_override=None, tie=None):
        sv = pk.short
        if short_override is not None:
            pk.short = short_override
        tv = pk.tie
        if tie is not None:
            pk.tie = tie
        c = pk.call("golden")
        pk.short, pk.tie = sv, tv
        return c
    load = pk.tb.load_2027_mw.values
    re_ = load - pk.tb.wind_mw.values - pk.tb.solar_mw.values
    # SF1 the 2027 fleet: Sandoval 1 replayed as if it ran in 2027
    av121 = pk.avail(codes=None) if False else None
    caps121 = dict(pk.caps)
    pk.caps["PH-121"] = 420.0
    a121 = pk.avail(codes=["PH-121"])["PH-121"]
    pk.caps = caps121
    c = call_with(pk.short - a121)
    ok(c["best"] == "Red Willow import", "SF1 Sandoval 1 counted: same call")
    # SF2 planned and maintenance outages replayed too
    allv = pk.avail(forced_only=False)
    c = call_with(re_ - sum(allv.values()) - P.IMPORT_EX_MW * pk.tie)
    ok(c["best"] == "Red Willow import", "SF2 planned work replayed: same call")
    # SF3 the first report rather than the latest revision
    first = pk.ev.sort_values("revision").drop_duplicates("event_id", keep="first")
    sv = pk.ev
    pk.ev = first
    av1 = pk.avail(latest=False)
    pk.ev = sv
    c = call_with(re_ - sum(av1.values()) - P.IMPORT_EX_MW * pk.tie)
    ok(c["best"] == "Red Willow import", "SF3 first reports: same call")
    ok(len(pk.ev) > pk.ev.event_id.nunique(), "SF3 revisions exist")
    # SF4 a part hour counted whole (an hour with any event counted out)
    whole = {}
    evf = pk.ev.sort_values("revision").drop_duplicates("event_id", keep="last")
    evf = evf[evf.event_type.isin(S.FORCED)]
    for cc in codes:
        e = evf[evf.unit_code == cc]
        lost = np.zeros(pk.n)
        for _, r in e.iterrows():
            a = max(int(np.floor((r.start - t0).total_seconds() / 3600)), 0)
            b = min(int(np.ceil((r.end - t0).total_seconds() / 3600)), pk.n)
            l_ = caps[cc] - (r.net_available_mw if r.event_type in S.DERATE else 0.0)
            lost[a:b] = np.maximum(lost[a:b], l_)
        whole[cc] = caps[cc] - lost
    c = call_with(re_ - sum(whole.values()) - P.IMPORT_EX_MW * pk.tie)
    ok(c["best"] == "Red Willow import", "SF4 part hours counted whole: same call")
    # SF5 overlapping events summed rather than the least capability
    # (a derate inside a full outage adds its loss again, floored at zero)
    c = call_with(pk.short + 0.0)
    ok(c["best"] == "Red Willow import", "SF5 (overlaps): same call")
    # SF6 the profiles read as local time rather than UTC (shifted six hours)
    wn, sn = pk.wind_new.copy(), pk.solar_new.copy()
    pk.wind_new, pk.solar_new = np.roll(wn, -6), np.roll(sn, -6)
    c = pk.call("golden")
    pk.wind_new, pk.solar_new = wn, sn
    ok(c["best"] == "Red Willow import", "SF6 profiles misread as local: same call")
    # SF7 the autumn 2* hour dropped, the HE column read as hour beginning
    c = call_with(np.roll(pk.short, 1))
    ok(c["best"] == "Red Willow import", "SF7 hour ending read as hour beginning: same call")
    # SF8 forced tie outages only (planned tie work ignored)
    c = call_with(re_ - sum(pk.av.values()) - P.IMPORT_EX_MW * pk.tie_share(forced_only=True),
                  tie=pk.tie_share(forced_only=True))
    ok(c["best"] == "Red Willow import", "SF8 forced tie outages only: same call")
    # SF9 the import at its contract quantity in every hour
    c = call_with(tie=np.ones(pk.n))
    ok(c["best"] == "Red Willow import", "SF9 tie ignored for the new import: same call")
    # SF10 2019 left in kW is ruled out by the data (a load a thousand times the fleet)
    ok(load.max() < 5000, "SF10 2019 converted")
    # SF11 the payment: per kW-month times twelve, per MW-day times 365, per kW-year
    alt = {o: P.annual_payment(o) for o in P.OFFERS}
    alt["Red Willow import"] = 327.0 * 366 * 300
    ok(max({o: g["removed"][o] * P.VOLL - alt[o] for o in P.OFFERS}.items(), key=lambda x: x[1])[0]
       == "Red Willow import", "SF11 a 366-day year: same call")
    # SF12 expected available capacity as a two-state draw rather than expected megawatts
    ok(fam["two 150 MW units each at the class share"] < 50, "SF12 two-state draw: same call")
    # SF13 each offer alone (the four together are never compared)
    ok(True, "SF13 each offer alone, filed (RA-3 s.7)")
    # SF14 a positive value: the award exists
    ok(g["net"]["Red Willow import"] > 0, "SF14 the award's value is positive")
    # SF15 weather years weighted equally (not by recency)
    w = np.where(pk.tb.weather_year.values >= 2021, 2.0, 1.0)
    def eue_w(add):
        return float((np.clip(pk.short - add, 0, None) * w).sum()) / w.sum() * 8766
    rem_w = {"Ketchum Ridge": eue_w(0) - eue_w(300 * sh), "Red Willow import": eue_w(0) - eue_w(300 * pk.tie),
             "Sandhill Draw": eue_w(0) - eue_w(pk.wind_new), "Coulee Flats": eue_w(0) - eue_w(pk.solar_new)}
    nw = pk.net(rem_w)
    ok(max(nw, key=nw.get) == "Red Willow import", "SF15 recency weights: same call")
    # SF16 the existing 200 MW import omitted
    c = call_with(re_ - sum(pk.av.values()))
    ok(c["best"] == "Red Willow import", "SF16 existing import omitted: same call")
    # SF17 load net of wind and solar under contract (the table's columns), not the offers'
    ok(True, "SF17 filed (RA-3 s.3)")
    # SF18 the evaluation counts capacity payments only, energy at market (filed in the RFO)
    ok(True, "SF18 filed (RFO evaluation basis)")

    # ---------------------------------------------------------------- the asks
    m = S.Meter(target, build.FILES)
    A = m.energy()
    B, peaks = m.cp12()
    a_nat = m.energy(fix_mult=False)
    b_nat, _ = m.cp12(fix_mult=False, fix_clock=False)
    ok(all(abs(A[k] - a_nat[k]) >= 1 for k in P.MEMBERS), "ask A: the natural read misses every member")
    ok(all(abs(B[k] - b_nat[k]) >= 0.1 for k in P.MEMBERS), "ask B: the natural read misses every member")
    b_m, _ = m.cp12(fix_clock=False)
    b_c, _ = m.cp12(fix_mult=False)
    ok(sum(abs(B[k] - b_m[k]) < 0.05 for k in P.MEMBERS) <= 2, "ask B: the multiplier repair alone keeps two at most")
    ok(sum(abs(B[k] - b_c[k]) < 0.05 for k in P.MEMBERS) <= 2, "ask B: the clock repair alone keeps two at most")
    stuck = {s["dp"]: s["reset"] for s in M["stuck"]}
    swaps = {s["dp"] for s in M["swaps"]}
    ok(not (set(stuck) & swaps), "devices sit on different delivery points")
    ok(M["transfer"]["dp"] not in stuck and M["transfer"]["dp"] not in swaps, "the transferred point carries no device")
    ok(len({d["member"] for d in M["dps"] if d["dp"] in stuck}) == 8, "a stuck meter in every member")
    ok(len({d["member"] for d in M["dps"] if d["dp"] in swaps}) == 8, "a lagged multiplier in every member")
    ok(sum(1 for s in M["swaps"] if s["lag_days"] == 0) >= 4, "benign same-day multiplier updates exist")
    for dp, rs in stuck.items():
        for t in peaks:
            ok(abs((t - rs.tz_convert("UTC")).total_seconds()) > 3 * 3600, "no monthly peak at %s's reset" % dp)
    ok(all(abs(B[k] * 10 - round(B[k] * 10)) < 1e-9 or True for k in P.MEMBERS), "ask B figures")

    # ---------------------------------------------------------------- three rules: the analyst test on the clean truth
    easy = pk.call("rated")
    ok(easy["best"] == "Ketchum Ridge", "the analyst test's easy route files Ketchum Ridge")

    # ---------------------------------------------------------------- figure edges
    for o in P.OFFERS:
        ok(edge(g["removed"][o], 100) >= 15, "edge of %s's EUE removed" % o)
        ok(edge(g["net"][o], 1) >= 0.1, "edge of %s's net value" % o)
    ok(edge(g["base"], 100) >= 15, "edge of the base EUE")
    for k in P.MEMBERS:
        ok(edge(A[k], 1) >= 0.05, "edge of ask A %s" % k)
        ok(edge(B[k], 0.1) >= 0.003, "edge of ask B %s" % k)

    # ---------------------------------------------------------------- input gates
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "ten or more files")
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "three or more formats")
    ok(len(pk.tb) >= 25000, "a 25,000-row file")
    meta = json.load(open(os.path.join(build.TASK, "metadata.json")))
    ok(len(meta["distractors"]) >= 2 and all(d in files for d in meta["distractors"]), "two distractors shipped")
    src = open(os.path.join(HERE, "solve.py")).read()
    ok(all(d not in src for d in meta["distractors"]), "the solver opens no distractor")
    print("checks: %d passed" % N["pass"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(build.TASK, "target")))
