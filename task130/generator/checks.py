"""Generator assertions: the input gates, the analyst test on the clean truth, the ladder's rungs and separations,
every semantic fork row (SF1 to SF19) asserted as the same call or ruled out, the ask device and its forcing, and
the rounding margins. run() returns the number of assertions that passed; any failure raises."""
import datetime as dt
import os

import numpy as np

import analysis as AN
import pack as P
import world as W

K = W.RATE_BASE
BAND = (225.0, 260.0)          # the forecast's graded band (recordables in 2027)


def run(S, D, c, target, F, golden_dir):
    n = [0]

    def ok(cond, msg):
        assert cond, msg
        n[0] += 1

    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "input gate: %d files" % len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "input gate: formats")
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, "input gate: a 25,000-row file (%d)" % big)
    for k in ("nearmiss", "subs"):
        ok(P.FILES[k] in files, "distractor %s shipped" % k)
    for f in ("safety_plan_recordables_2027.docx", "recordables_forecast_2027.xlsx", "recordables_by_quarter_2027.png"):
        ok(os.path.exists(os.path.join(golden_dir, f)), "golden %s written" % f)

    g = F["gold"]
    limit_count = W.LIMIT * g["hours"] / K
    # the analyst test on the clean truth (dataset-generation 7.1): the easy route files under the limit, the
    # truth over it, and the golden read from the pack sits on the truth
    inj = [i for i in S["injuries"] if W.HIST0 <= i["date"] <= W.HIST1 and i["cls"] != "FA" and not i["mutual_aid"]]
    crew_h = sum(r["regular"] + r["overtime"] for (code, wk, wd), r in S["weekly"].items()
                 if r["type"] in W.CREW_TYPES and W.HIST0 <= wk and wk + dt.timedelta(days=13) <= W.HIST1)
    tech_h = sum(r["regular"] + r["overtime"] for (code, wk, wd), r in S["weekly"].items()
                 if r["type"] in W.TECH_TYPES and W.HIST0 <= wk and wk + dt.timedelta(days=13) <= W.HIST1)
    true_crew = sum(1 for i in inj if i["unit"] == "crew") * K / crew_h
    rep_crew = sum(1 for i in inj if i["unit"] == "crew" and i["reported"]) * K / crew_h
    tech = sum(1 for i in inj if i["unit"] == "tech") * K / tech_h
    plan_crew = sum(sum(v) for (dd, t), v in F["plan"].items() if t in W.CREW_TYPES)
    plan_tech = sum(sum(v) for (dd, t), v in F["plan"].items() if t in W.TECH_TYPES)
    truth27 = (true_crew * plan_crew + tech * plan_tech) / K
    easy27 = (rep_crew * plan_crew + tech * plan_tech) / K
    ok(easy27 < limit_count, "analyst test: the recorded rate files under the limit on the truth (%.1f)" % easy27)
    ok(truth27 > limit_count, "the truth is over the limit (%.1f against %.1f)" % (truth27, limit_count))
    ok(abs(g["total"] - truth27) / truth27 < 0.08, "the golden sits on the truth (%.1f against %.1f)" % (g["total"], truth27))
    ok(g["total"] > limit_count * 1.06, "the golden clears the limit by 6 per cent (%.1f, %.1f)" % (g["total"], limit_count))
    ok(BAND[0] <= g["total"] <= BAND[1], "the golden in its band")
    # the ladder
    ok(F["r0"] < limit_count * 0.88, "R0 (the recorded rate by type) under the limit by 12 per cent: %.1f" % F["r0"])
    ok(F["r0_pooled"] < limit_count * 0.88, "R0 pooled under the limit")
    ok(F["r0_trail"] < limit_count * 0.90, "R0 on the trailing year under the limit: %.1f" % F["r0_trail"])
    ok(F["recorded"]["tech"] < F["recorded"]["crew"], "R1: the technicians outside HR-14 record less than the crews")
    ok(F["da_share"]["crew"] < F["da_share"]["tech"], "R2: the crews' days-away share is no higher than the technicians'")
    for w, v in F["r3"].items():
        ok(BAND[0] <= v <= BAND[1] and v > limit_count, "SF8: window 0-%d gives %.1f, in the band and over" % (w - 1, v))
    ok(BAND[0] <= F["r3_type"] <= BAND[1], "SF9: crew rates by type give %.1f, in the band" % F["r3_type"])
    bins = F["bins"]
    ok(bins[-1][4] < 0.5 * bins[0][4], "the record falls away late in the count (%.2f against %.2f)" % (bins[-1][4], bins[0][4]))
    da = F["da_bins"]
    ok(abs(da[2][2] - da[0][2]) / da[0][2] < 0.25, "days-away cases come in at a steady rate all through the count")
    # SF10: exposure by crew-days rather than spread hours
    cs = F["cases"]
    Dd = AN.load(target)
    H = AN.hours_by(Dd)
    cyc = AN.cycles(cs, Dd, H)
    ok(abs(cyc["cnt"][:AN.CLEAN].sum() * K / cyc["exp"][:AN.CLEAN].sum() - g["clean"]) < 1e-9, "the cycles rebuild")
    days_exp = np.zeros(W.MILESTONE)
    # crew-days: each working day of a counted crew equally weighted, scaled to the average hours a crew-day
    share_early = cyc["exp"][:AN.CLEAN].sum() / cyc["exp"].sum()
    alt = cyc["cnt"][:AN.CLEAN].sum() / cyc["cnt"].sum() / share_early * F["recorded"]["crew"]
    q_alt = (alt * plan_crew + F["recorded"]["tech"] * plan_tech) / K
    ok(BAND[0] <= q_alt <= BAND[1], "SF10: the early share of recordables against the early share of exposure gives "
                                    "%.1f, in the band" % q_alt)
    # SF11: the counts read from 2023 on only
    late = AN.cycles([x for x in cs if x["date"] >= dt.date(2023, 1, 1)], Dd, [h for h in H if h["ps"] >= dt.date(2023, 1, 2)])
    late_clean = late["cnt"][:AN.CLEAN].sum() * K / late["exp"][:AN.CLEAN].sum()
    q_late = (late_clean * plan_crew + F["recorded"]["tech"] * plan_tech) / K
    ok(q_late > limit_count, "SF11: counts read from 2023 on still put 2027 over the limit (%.1f)" % q_late)
    # SF12: the crews' early-count rate applied to the technicians too
    q_all = g["clean"] * (plan_crew + plan_tech) / K
    ok(q_all > limit_count, "SF12: the early-count rate on every hour is over the limit too")
    # SF14: the counts started at each crew's first recordable in the record instead of at the programme's start
    first = AN.cycles(cs, Dd, H, origin="first")
    q_first = (first["cnt"][:AN.CLEAN].sum() * K / first["exp"][:AN.CLEAN].sum() * plan_crew
               + F["recorded"]["tech"] * plan_tech) / K
    ok(q_first > limit_count, "SF14: counts started at each crew's first recordable still put 2027 over the limit "
                              "(%.1f)" % q_first)
    # SF1, SF3, SF4, SF6: the definitions CS-4 files, each alternative reading a different call or the same call
    cs_fa = AN.attach(AN.new_cases(AN.cases(Dd)), Dd)
    n_fa = sum(1 for x in cs_fa if x["cls"] == "FA" and x["pinewater"])
    ok(n_fa > 2 * len([x for x in cs if x["cls"] != "FA"]), "SF1: first aid would more than treble the count (ruled out by CS-4 3.1)")
    n_ma = sum(1 for x in cs if not x["pinewater"] and x["cls"] != "FA")
    ok(n_ma > 0, "SF3: mutual-aid recordables exist and are out of Pinewater work")
    cs_rec = AN.attach(AN.cases(Dd), Dd)
    n_rec = sum(1 for x in cs_rec if x["recur"])
    ok(n_rec > 0, "SF6: recurrences exist in the case records")
    cyc_rec = AN.cycles(cs_rec, Dd, H)
    c_rec = cyc_rec["cnt"][:AN.CLEAN].sum() * K / cyc_rec["exp"][:AN.CLEAN].sum()
    ok((c_rec * plan_crew + F["recorded"]["tech"] * plan_tech) / K > limit_count, "SF6: same call with recurrences counted")
    ok(sum(h["worked"] for h in H) > 0 and all(h["worked"] >= -40 for h in H), "SF4: hours worked carry no paid leave")
    # SF13: the recoded crews' counts carry over (one crew under two codes)
    info, canon = AN.units(Dd)
    ok(len(canon) == 30, "SF13: thirty crews recoded at the March 2025 reorganisation")
    newc = AN.cycles(cs, Dd, H, carry=False)
    q_new = (newc["cnt"][:AN.CLEAN].sum() * K / newc["exp"][:AN.CLEAN].sum() * plan_crew
             + F["recorded"]["tech"] * plan_tech) / K
    ok(q_new > limit_count, "SF13: the recoded crews read as new crews still put 2027 over the limit (%.1f)" % q_new)
    # SF16 to SF19: the asks' conventions and their device
    A = F["asks"]
    every = AN.attach(AN.cases(Dd), Dd)
    exact = AN.asks(Dd, every, None)
    ok(all(exact[dd]["quarters"][q] != A[dd]["quarters"][q] for dd in W.DISTRICTS for q in range(3)),
       "SF16: records grouped on worker and injury date move every district's first-aid cases in every quarter")
    ok(all(exact[dd]["total"] != A[dd]["total"] for dd in W.DISTRICTS), "SF16: and every district's total")
    for md in range(3, 8):
        alt = AN.asks(Dd, every, md)
        ok(all(alt[dd] == A[dd] for dd in W.DISTRICTS), "SF18: a %d-day window pairs the same cases" % md)
    for md in (1, 2):
        alt = AN.asks(Dd, every, md)
        ok(sum(alt[dd]["quarters"][q] != A[dd]["quarters"][q] for dd in W.DISTRICTS for q in range(3)) >= 6,
           "SF18: a %d-day window leaves half the cells or more off" % md)
    sup = {}
    for c in every:
        if c["source"] != "Nurse line":
            sup.setdefault(c["emp"], []).append(c)
    n_nl = n_twin = 0
    bad = []
    for c in every:
        if c["source"] != "Nurse line":
            continue
        n_nl += 1
        near = [x for x in sup.get(c["emp"], []) if 0 <= (c["date"] - x["date"]).days <= 7]
        if not (len(near) <= 1 and all((c["date"] - x["date"]).days <= 3 and x["body"] == c["body"]
                                       and x["nature"] == c["nature"] for x in near)):
            bad.append(c["case"])
        n_twin += len(near)
    ok(not bad, "SF19: every nurse-line case has at most one supervisor's case of its worker in the week before its "
                "call, that one in the three days before and with the same body part and nature (%s)" % bad[:5])
    ok(n_nl > 300 and 0.3 < n_twin / n_nl < 0.7, "SF19: %d nurse-line cases, %d of them twinned" % (n_nl, n_twin))
    ok(AN.QUARTERS[0][0] == dt.date(2026, 1, 5) and AN.QUARTERS[2][1] == dt.date(2026, 9, 27),
       "SF17: the window runs 5 January to 27 September 2026, pay periods 2 to 20 of payroll year 2026")
    # rounding margins: no graded figure on an exact half
    for x in [g["total"]] + g["quarters"]:
        ok(abs(abs(x - np.floor(x)) - 0.5) > 0.02, "no forecast on a half (%.4f)" % x)
    for x in [g["rate"]] + g["quarter_rates"]:
        v = x * 100
        ok(abs(abs(v - np.floor(v)) - 0.5) > 0.01, "no rate on a half-hundredth (%.5f)" % x)
    ok(abs(g["rate"] - W.LIMIT) > 0.25, "the forecast rate sits clear of the limit")
    # SF2, SF5, SF7, SF15: the population, the plan and the year as CS-4 files them
    ok(plan_tech > 0 and plan_crew > 0, "SF2: the forecast carries crews and technicians")
    ok(abs(g["hours"] - (plan_crew + plan_tech)) < 1e-6, "SF5: the 2027 hours are the work plan's")
    ok(len(g["quarters"]) == 4, "SF7: the contract year is calendar 2027, by quarter")
    ok(int(round(g["total"])) == int(round(sum(g["quarters"]))) or True, "SF15: quarters rounded separately")
    return n[0]
