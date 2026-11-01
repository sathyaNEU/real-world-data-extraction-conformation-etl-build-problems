"""Design arithmetic on the clean truth: the true and recorded rates, year by year, the reporting curve by cycle day,
and the 2027 forecast the truth gives on the work plan, computed from the simulation."""
import datetime as dt
import sys

import numpy as np

import pack as P
import sim
import world as W

K = W.RATE_BASE


def rates(S, a=W.HIST0, b=W.HIST1):
    crew_h = sum(r["regular"] + r["overtime"] for (code, wk, _wd), r in S["weekly"].items()
                 if r["type"] in W.CREW_TYPES and a <= wk <= b)
    tech_h = sum(r["regular"] + r["overtime"] for (code, wk, _wd), r in S["weekly"].items()
                 if r["type"] in W.TECH_TYPES and a <= wk <= b)
    inj = [i for i in S["injuries"] if a <= i["date"] <= b and i["cls"] != "FA" and not i["mutual_aid"]]
    crew_true = sum(1 for i in inj if i["unit"] == "crew")
    crew_rep = sum(1 for i in inj if i["unit"] == "crew" and i["reported"])
    tech = sum(1 for i in inj if i["unit"] == "tech")
    return dict(crew_h=crew_h, tech_h=tech_h, crew_true=crew_true, crew_rep=crew_rep, tech=tech,
                crew_true_rate=crew_true * K / crew_h, crew_rep_rate=crew_rep * K / crew_h, tech_rate=tech * K / tech_h,
                all_true=(crew_true + tech) * K / (crew_h + tech_h), all_rep=(crew_rep + tech) * K / (crew_h + tech_h))


def curve(S):
    rep = np.zeros(W.MILESTONE)
    true = np.zeros(W.MILESTONE)
    for i in S["injuries"]:
        if i["unit"] == "crew" and i["cls"] != "FA" and not i["mutual_aid"] and i["date"] >= W.HIST0:
            true[i["cycle_day"]] += 1
            if i["reported"]:
                rep[i["cycle_day"]] += 1
    return rep, true, S["exposure"]


def main():
    S = sim.simulate()
    r = rates(S)
    plan = P.plan_hours(S)
    pc = sum(sum(v) for (d_, t), v in plan.items() if t in W.CREW_TYPES)
    pt = sum(sum(v) for (d_, t), v in plan.items() if t in W.TECH_TYPES)
    print("truth: crew true %.3f recorded %.3f; technicians %.3f; all true %.3f recorded %.3f"
          % (r["crew_true_rate"], r["crew_rep_rate"], r["tech_rate"], r["all_true"], r["all_rep"]))
    print("truth 2027 on the plan: %.1f recordables (rate %.3f); recorded-rate route %.1f"
          % ((r["crew_true_rate"] * pc + r["tech_rate"] * pt) / K, (r["crew_true_rate"] * pc + r["tech_rate"] * pt) / (pc + pt),
             (r["crew_rep_rate"] * pc + r["tech_rate"] * pt) / K))
    yr = {}
    for y in range(2021, 2027):
        a, b = dt.date(y, 1, 1), (dt.date(y, 12, 31) if y < 2026 else W.HIST1)
        yr[y] = round(rates(S, a, b)["all_rep"], 2)
    print("recorded rate by year", yr)
    rep, true, ex = curve(S)
    hidden = true.sum() - rep.sum()
    print("injuries 2021-2026 on Pinewater work by crews: %d, recorded %d, unrecorded %d (%.1f per cent)"
          % (true.sum(), rep.sum(), hidden, 100 * hidden / true.sum()))


if __name__ == "__main__":
    main()
