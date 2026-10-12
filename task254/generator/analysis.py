"""Every figure the build owes, computed on the generator's side from the world."""
import math

import numpy as np

import asks as A
import core

VARIANTS = ("entry", "mid", "exit", "interp")


def latest(counts, need):
    ok = [d for d in core.DEPARTURES if counts[d] >= need]
    return ok[-1] if ok else None


def on_time(arr):
    return int((arr <= core.BAR_TIME).sum())


def main_figures(W):
    work = W["work"]
    tt = W["route"][work]
    N = len(tt)
    need = math.ceil(0.9 * N)
    ff = float(sum(r[5] for r in core.ROUTE))
    out = {"N": N, "need": need, "bar": 0.9 * N}
    walked = {v: {d: on_time(core.walk(tt, d, v)) for d in core.DEPARTURES} for v in VARIANTS}
    out["walked"] = walked
    out["golden_counts"] = walked["entry"]
    out["call"] = latest(walked["entry"], need)
    out["R0_counts"] = {d: on_time(core.at_departure(tt, d)) for d in core.DEPARTURES}
    out["R2_counts"] = {d: on_time(core.at_midpoint(tt, ff, d)) for d in core.DEPARTURES}
    out["R0"] = latest(out["R0_counts"], need)
    out["R2"] = latest(out["R2_counts"], need)
    p90 = np.percentile(tt, 90, axis=0)
    p50 = np.percentile(tt, 50, axis=0)
    ok1 = [d for d in core.DEPARTURES if core.profile_at_departure(p90, d) <= core.BAR_TIME]
    ok3 = [d for d in core.DEPARTURES if core.profile_walk(p90, d) <= core.BAR_TIME]
    ok5 = [d for d in core.DEPARTURES if core.profile_walk(p50, d) <= core.BAR_TIME]
    out["R1"], out["R3"], out["P50"] = (ok1[-1] if ok1 else None), (ok3[-1] if ok3 else None), (ok5[-1] if ok5 else None)
    # grid and forks
    inc = W["incident"][work]
    sub = tt[~inc]
    need_sub = math.ceil(0.9 * len(sub))
    g = {}
    g["incidents_dropped_walk"] = latest({d: on_time(core.walk(sub, d)) for d in core.DEPARTURES}, need_sub)
    g["incidents_dropped_R0"] = latest({d: on_time(core.at_departure(sub, d)) for d in core.DEPARTURES}, need_sub)
    g["incidents_dropped_R2"] = latest({d: on_time(core.at_midpoint(sub, ff, d)) for d in core.DEPARTURES}, need_sub)
    allwk = W["route"][W["kind"] != "weekend"]
    hk = {d: on_time(core.walk(allwk, d)) for d in core.DEPARTURES}
    g["holidays_kept"] = latest(hk, math.ceil(0.9 * len(allwk)))
    g["holidays_kept_counts"] = hk
    g["weekdays_all"] = len(allwk)
    for cls, arr in (("class_all", W["route_all"][work]), ("class_freight", W["route_frt"][work])):
        g[cls] = latest({d: on_time(core.walk(arr, d)) for d in core.DEPARTURES}, need)
    g["strict"] = {d: int((core.walk(tt, d) < core.BAR_TIME).sum()) for d in core.DEPARTURES}
    g["p90_rule"] = [d for d in core.DEPARTURES
                     if np.percentile(core.walk(tt, d) - d, 90) <= core.BAR_TIME - d][-1]
    g["no_legs"] = latest({d: on_time(core.walk(tt, d, lot=0.0, stop=0.0)) for d in core.DEPARTURES}, need)
    out["grid"] = g
    # nearest arrivals to 8:00 under every variant at every departure (seconds)
    near = {}
    for d in core.DEPARTURES:
        near[d] = min(float(np.min(np.abs(core.walk(tt, d, v) - core.BAR_TIME))) * 60 for v in VARIANTS)
    out["nearest_seconds"] = near
    out["late"] = {k: {d: N - c for d, c in cnt.items()}
                   for k, cnt in (("walk", out["golden_counts"]), ("R0", out["R0_counts"]), ("R2", out["R2_counts"]))}
    out["walked_715"] = out["golden_counts"][7 * 60 + 15]
    k715 = W["kind"][work]
    mv = (core.at_departure(tt, 7 * 60 + 15) <= core.BAR_TIME) & (core.walk(tt, 7 * 60 + 15) > core.BAR_TIME)
    # how far into the trip the shuttle reaches the I-264 merge, and the queue segments' time read at departure
    # against the time met on the walk (school-term days, 7:15)
    sch = k715 == "school"
    t = np.full(len(tt), 7 * 60 + 15 + core.LOT_LEG)
    r = np.arange(len(tt))
    met = np.zeros(len(tt))
    qs = set(core.QUEUE_SEGS + [core.BOTTLENECK])
    for k in range(len(core.ROUTE)):
        if k == core.QUEUE_SEGS[0]:
            reach = t.copy()
        v = tt[r, core.ix(t), k]
        if k in qs:
            met += v
        t = t + v / 60.0
    at_dep = tt[:, core.ix(7 * 60 + 15), sorted(qs)].sum(1)
    out["merge_715"] = {"minutes_to_queue_p10": float(np.percentile(reach[sch] - 7 * 60 - 15, 10)),
                        "minutes_to_queue_p90": float(np.percentile(reach[sch] - 7 * 60 - 15, 90)),
                        "queue_minutes_at_departure": float(np.mean(at_dep[sch]) / 60.0),
                        "queue_minutes_met": float(np.mean(met[sch]) / 60.0)}
    out["moved_715"] = {"all": int(mv.sum()), "school": int((mv & (k715 == "school")).sum()),
                        "break": int((mv & (k715 == "break")).sum())}
    # the travel time read as length over the rounded speed (SF13) and from the all-vehicle class (SF5)
    out["walk_all_counts"] = {d: on_time(core.walk(W["route_all"][work], d)) for d in core.DEPARTURES}
    out["mean_trip_walk"] = {d: float(np.mean(core.walk(tt, d) - d)) for d in core.DEPARTURES}
    out["mean_trip_R0"] = {d: float(np.mean(core.at_departure(tt, d) - d)) for d in core.DEPARTURES}
    return out


RIDER_SUBSETS = [(r1, k, a) for r1 in (False, True) for k in (False, True) for a in (False, True)]


def rider_key(r1, keep_opt, all_starts):
    parts = [n for n, f in (("R1", r1), ("H2", keep_opt), ("H3", all_starts)) if f]
    return "+".join(parts) or "golden"


def ask_figures(F, S):
    """The asks' figures under the golden read and under every subset of mishandlings: the rider reads (R1 the
    sheets added, H2 the opt-outs kept, H3 every start kept), the three late-day constructions (walked, at the
    departure period, at the midpoint) and the three deadhead lookups (the release in force at set-up, the
    current release, the reissued code dropped)."""
    riders = {rider_key(*f): sum(A.riders(S, r1=f[0], keep_opt=f[1], all_starts=f[2]).values())
              for f in RIDER_SUBSETS}
    miles = {k: A.deadhead_miles(k) for k in ("golden", "current", "drop")}
    gold = A.ask_figures(F["late"]["walk"], riders["golden"], miles["golden"])
    stops = {}
    for rk in riders:
        for lk in F["late"]:
            for mk in miles:
                stops[(rk, lk, mk)] = A.ask_figures(F["late"][lk], riders[rk], miles[mk])
    return {"riders": riders, "miles": miles, "gold": gold, "stops": stops,
            "by_dept": A.riders(S, "golden"), "by_dept_natural": A.riders(S, "natural"), "both_sheets": len(S["dup"]),
            "vehicle_charges": A.vehicles(riders["golden"]) * core.working_days_2027() *
            (A.DAY_RATE + A.MILE_RATE * miles["golden"])}


def nearest_composition(G):
    """The composed figure nearest its golden over every subset of mishandlings: (distance, subset, departure,
    figure)."""
    gold = G["gold"]
    near = []
    for (rk, lk, mk), s1 in G["stops"].items():
        if (rk, lk, mk) == ("golden", "walk", "golden"):
            continue
        for d in A.ASK_DEPS:
            if rk != "golden" or lk != "walk":
                near.append((abs(s1["late_arrivals"][d] - gold["late_arrivals"][d]), (rk, lk, mk), d, "late_arrivals"))
            near.append((abs(round(s1["cost"][d]) - round(gold["cost"][d])), (rk, lk, mk), d, "cost"))
    return min(near)
