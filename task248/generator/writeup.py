"""task248 figures and write-up: every figure the goldens, figures.json and submission.md carry, computed once from the
shipped pack (solve.py), and the write-up drafted from them."""
import datetime as dt
import json

import numpy as np
import pandas as pd

import solve

WORD = {0: "none", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight",
        9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 18: "eighteen", 24: "twenty-four"}
SEASONS = {"December to February": (12, 1, 2), "June to August": (6, 7, 8)}


def _list(vals):
    vals = list(vals)
    return ", ".join(vals[:-1]) + " and " + vals[-1] if len(vals) > 1 else vals[0]


def ask_a_detail(pk):
    """each plant's hours of the year without a valid inlet flow reading, by what the historian holds for the hour"""
    import collections
    h = pk.h
    lo = pd.Timestamp(dt.datetime.combine(solve.ASK_A[0], dt.time(0)))
    hi = pd.Timestamp(dt.datetime.combine(solve.ASK_A[1], dt.time(23)))
    w = h[(h.ts >= lo) & (h.ts <= hi)]
    need = collections.Counter(pk.hours_window())
    out = {}
    for code in pk.codes:
        x = w[w.plant_code == code]
        have = collections.Counter(x.ts.dt.to_pydatetime())
        norow = sum(max(0, n - have.get(t, 0)) for t, n in need.items())
        out[code] = dict(no_row=int(norow), blank=int(x.flow.isna().sum()), held=int(x.held.sum()),
                         zero_or_below=int((x.flow <= 0).sum()))
    return out


def episode_list(lev):
    """each episode that opens in the winter: the week it opened and the week it closed"""
    out, start = [], None
    for w in sorted(lev):
        x = lev[w]
        if start is None and x >= 1.0:
            start = w
        elif start is not None and x < 0.5:
            if solve.WINTER[0] <= start <= solve.WINTER[1]:
                out.append([start.isoformat(), w.isoformat()])
            start = None
    return out


def figures(target, F):
    pk, par, rows = solve.solve(target, F)
    _, plev = pk.counts()
    _, slev = pk.counts(pk.shed_corr()[0])
    R, _ = pk.rungs()
    A = pk.ask_a()
    Ad = ask_a_detail(pk)
    Bf, Bd = pk.ask_b()
    j = pk.pairs()
    j["loss"] = -np.log10(j.n1_pl / j.n1_up)
    seasonal = {}
    for code in ("DNK", "NTL", "ADS", "CLF"):
        x = j[j.plant_code == code]
        seasonal[code] = {s: round(float(x[x.month.isin(m)].loss.mean()), 2) for s, m in SEASONS.items()}
        seasonal[code]["visits"] = {s: int(x.month.isin(m).sum()) for s, m in SEASONS.items()}
    k, _ = pk.fit()
    plants = []
    for r in rows:
        c = r["plant"]
        plants.append(dict(code=c, name=r["name"], tt=r["tt"], published=r["published"], shed=r["shed"],
                           change=r["change"], hours=A[c], hours_detail=Ad[c], flags=Bf[c],
                           flagged=[[d.isoformat(), v] for d, v in Bd[c]],
                           episodes_published=episode_list(plev[c][0]), episodes_shed=episode_list(slev[c][0])))
    moves = {p["code"]: p["change"] for p in plants if p["change"]}
    return dict(call=sum(p["shed"] for p in plants),
                totals=dict(published=sum(p["published"] for p in plants), shed=sum(p["shed"] for p in plants)),
                moves=moves, plants=plants,
                decay=dict(k20="%.3f" % par["k20"], theta="%.2f" % par["theta"], visits=int(len(j)),
                           theta_pct=int(round((par["theta"] - 1) * 100)),
                           k20_exact=round(par["k20"], 5), theta_exact=round(par["theta"], 5)),
                seasonal=seasonal,
                rungs={k_: sum(v.values()) for k_, v in R.items()},
                rung_moves={k_: {c: v[c] - R["published"][c] for c in pk.codes if v[c] != R["published"][c]}
                            for k_, v in R.items()},
                ask_a_total=sum(A.values()), ask_b_total=sum(Bf.values()),
                contract_factor=pk.contract_factor,
                contract_method=dict(sample_ml=100, resuspended_ml=2, aliquot_ul=200, eluted_ul=100),
                conventions=dict(high=1.0, low=0.5, percentile=10, reference=["2026-04-06", "2027-03-29"],
                                 winter=["2027-05-03", "2027-09-27"], ask_a=["2027-04-01", "2028-03-31"],
                                 ask_b=["2027-10-04", "2028-03-30"], check_log10=0.5, lookback_days=365,
                                 hold_run=4, real_hours=len(pk.hours_window()), load_factor=1000,
                                 methods_sections=[3, 4, 5, 6.1, 6.2, 6.3]))


def write_figures(path, fig):
    with open(path, "w") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")


def _names(fig, codes):
    nm = {p["code"]: p["name"] for p in fig["plants"]}
    return ["%s (%s)" % (nm[c], c) for c in codes]


def golden_content(fig):
    P_ = fig["plants"]
    down = [p["code"] for p in P_ if p["change"] < 0]
    up = [p["code"] for p in P_ if p["change"] > 0]
    d = fig["decay"]
    s = fig["seasonal"]["CLF"]
    pct = d["theta_pct"]
    lead = "Plan the desk for %d alert episodes this winter, not the %d the dashboard published for last winter." % (
        fig["call"], fig["totals"]["published"])
    paras = [
        "Read on the shed load, last winter's samples (May to September 2027) raise %d alert episodes against the %d "
        "the dashboard published. %s each lose an episode and %s gains one; the other %s plants keep their counts."
        % (fig["call"], fig["totals"]["published"], _list(_names(fig, down)), _list(_names(fig, up)),
           WORD[len(P_) - len(down) - len(up)]),
        "The paired upstream study shows the sewer destroying the RNA faster in warm water: at Cleaveland Flat, at the "
        "end of a %s-minute trunk sewer, the study's composites lost %.2f log10 between the trunk's head and the plant in "
        "December to February and %.2f in June to August. Fitted over all %d paired visits, the decay rate is %s an "
        "hour at 20 degrees and rises about %d per cent a degree. A plant's baseline is set in the summer lull, when its "
        "samples lose the most, so restoring each sample at the rate for its own water temperature lifts the baseline "
        "more than the winter samples at the long trunk sewers, and the winter rises there that came from the colder "
        "water alone fall away." % ("1,615", s["December to February"], s["June to August"], d["visits"], d["k20"], pct),
        "A correction that does not move over the year (one decay rate over each plant's travel time, or the samples "
        "divided by their PMMoV) lifts a plant's baseline and its winter samples alike and gives back the published %d."
        % fig["totals"]["published"],
        "From 1 May the desk also takes the historian's flow and the faecal-strength check: over the year to 31 March "
        "the historian had %s hours without a valid inlet flow reading across the 24 plants, and %d composites since "
        "October fail the check; both are by plant in the workbook." % ("{:,}".format(fig["ask_a_total"]),
                                                                       fig["ask_b_total"]),
    ]
    return dict(fig=fig, lead=lead, paras=paras,
                title="Verification desk, winter 2028: alert episodes to plan for",
                chart_title="Winter 2027 alert episodes by plant: published %d, shed load %d" % (
                    fig["totals"]["published"], fig["call"]),
                footnote="Episodes opening in the weeks starting 3 May to 27 September 2027 (methods note v4, sections "
                         "4 and 5). Published: each sample's N1 load per person. Shed load: each sample's load with the "
                         "RNA lost in the sewer restored at the paired study's decay rate for the composite's inlet "
                         "temperature over the plant's population-weighted travel time; baselines recomputed (section "
                         "6.1). Plants in order of travel time.",
                sources="Sources: Public Health Laboratory results export and notes; the contract laboratory's report "
                        "WL-2801; Southern Plains Water inlet historian export and note; site register; travel-time "
                        "memo (November 2025); paired upstream study, 2026; dashboard methods note v4.")


def submission(fig):
    P_ = fig["plants"]
    down = [p["code"] for p in P_ if p["change"] < 0]
    up = [p["code"] for p in P_ if p["change"] > 0]
    d = fig["decay"]
    se = fig["seasonal"]
    pct = d["theta_pct"]
    lines = []
    w = lines.append
    w("# task248 submission")
    w("")
    w("## Tags")
    w("")
    w("**Domain:** Epidemiology & Public Health (disease surveillance and outbreak detection: a regional public health "
      "service's wastewater surveillance of SARS-CoV-2 at 24 treatment plants and the verification desk that checks "
      "every alert episode its dashboard raises).")
    w("**Analytical objective:** Data Quality Monitoring & Alerting (how many alert episodes the dashboard raises once "
      "it reads every sample on the shed load, with the RNA lost in the sewer restored, and so how many the "
      "verification desk plans for).")
    w("")
    w("## 1. Final Recommendation")
    w("")
    w("**Plan the verification desk for %d alert episodes this winter.**" % fig["call"])
    w("")
    w("Last winter's samples (May to September 2027) raise %d alert episodes on the shed load against the %d the "
      "dashboard published: %s each have one episode fewer and %s one more; the other %s plants keep their counts." % (
          fig["call"], fig["totals"]["published"], _list(_names(fig, down)), _list(_names(fig, up)),
          WORD[len(P_) - len(down) - len(up)]))
    w("")
    w("Not the published %d, which any restoration that does not move over the year gives back (the paired study's "
      "single decay rate over each plant's travel time, or each sample divided by its PMMoV): it lifts a plant's "
      "winter samples and the samples that set its baseline alike. The RNA's decay rate rises with the water's "
      "temperature, so at the long trunk sewers the summer samples behind each baseline lost more than the winter "
      "samples, and restored at each composite's own temperature the winter rises that came from the colder water "
      "fall away. Not %d, restoring only the four plants of the paired study (Ardenmouth South and Cleaveland Flat "
      "move; Ardenmouth East, Ardenmouth West, Tarnbrook and Saltmarsh Point do not)." % (
          fig["totals"]["published"], fig["rungs"]["study plants only"]))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. Over its %d paired visits, the study's loss between the trunk's head and the plant fits first-order decay at "
      "**%s an hour at 20 degrees Celsius, rising about %d per cent a degree** (theta %s)." % (
          d["visits"], d["k20"], pct, d["theta"]))
    w("2. The loss moves with the season: at Cleaveland Flat (1,615 minutes) the composites lost **%.2f log10 in "
      "December to February and %.2f in June to August**; at Ardenmouth South (1,310 minutes) **%.2f and %.2f**." % (
          se["CLF"]["December to February"], se["CLF"]["June to August"], se["ADS"]["December to February"],
          se["ADS"]["June to August"]))
    w("3. A restoration constant over the year leaves every plant's count as published (**%d**)." %
      fig["rungs"]["constant"])
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    steps = [
        "Laboratory export: the accepted run of each sample and target (the export notes), the closure's composites "
        "from the contract laboratory's report; each sample's N1 load per person is the concentration times the "
        "composite's flow times 1,000 over the register's population served (methods note section 3).",
        "Weekly values by the week (Monday to Sunday) of the day the composite ended, the baseline the 10th percentile "
        "(PERCENTILE.INC) of the weekly values of the weeks starting 6 April 2026 to 29 March 2027, levels the weekly "
        "value less the baseline; an episode opens at 1.0 or more and closes below 0.5, and winter 2027's episodes open "
        "in the weeks starting 3 May to 27 September 2027 (sections 4 and 5): %d on the published basis, the dashboard's "
        "export." % fig["totals"]["published"],
        "Paired study: the three replicates of each point averaged, the loss the natural log of the plant's N1 over the "
        "upstream N1 (both in copies per millilitre), the travel time from the network memo in hours, the temperature the "
        "mean of the two points' readings; least squares of the loss on minus the travel time times k20 times "
        "theta^(T - 20) gives k20 %s an hour and theta %s." % (d["k20"], d["theta"]),
        "Historian: each composite's mean inlet temperature over its 24 hours (08:00 to 08:00 local, start-of-hour "
        "stamps); each sample's shed load per person is its load times exp(k(T) times the travel time in hours).",
        "Levels, baselines and episodes recomputed on the shed load per person (section 6.1): %d, with %s." % (
            fig["call"], _list(["%s %+d" % (c, v) for c, v in fig["moves"].items()])),
        "The same counts at every plant from a rate linear in temperature or fitted plant by plant, the plant's or the "
        "upstream reading or their mean, the composite's, the month's or the season's inlet temperature or that of the "
        "24 hours a travel time earlier, and the historian's flow in place of the form's.",
        "Historian hours, 1 April 2027 to 31 March 2028: the year's %s real local hours (the clock skips 02:00 on 26 "
        "September 2027 and repeats 02:00 on 4 April 2027), exact duplicate rows removed; an hour lacks a valid inlet "
        "flow reading when it has no row, a blank flow, a flow of zero or below, or a held reading (after the first of "
        "four or more identical consecutive readings), as the export note defines." % "{:,}".format(
            fig["conventions"]["real_hours"]),
        "Faecal-strength check (section 6.3): each composite's PMMoV load per person on the historian's inflow over its "
        "24 hours (the mean of its valid hourly readings times 24); the contract laboratory's extract (100 microlitres) "
        "holds the copies of 200 microlitres of the 2 millilitres of resuspended pellet from 100 millilitres of "
        "wastewater, so a copy per microlitre of extract is %s a litre; each composite against the median of the "
        "plant's composites of the 365 days before it, more than 0.5 log10 above or below failing." % "{:,}".format(
            int(fig["contract_factor"])),
    ]
    for k, st in enumerate(steps, 1):
        w("%d. %s" % (k, st))
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### winter_2027_episodes_shed_load.xlsx")
    w("")
    w("1. Winter 2027 alert episodes: **%d on the published basis and %d on the shed load**." % (
        fig["totals"]["published"], fig["call"]))
    w("2. Six plants' counts move: %s." % _list(["%s %+d" % (n, fig["moves"][c]) for n, c in
                                                zip(_names(fig, list(fig["moves"])), fig["moves"])]))
    w("3. Each plant's hours from 1 April 2027 to 31 March 2028 with no valid inlet flow reading in the historian:")
    for p in P_:
        w("   - %s %s: %d" % (p["code"], p["name"], p["hours"]))
    w("4. Each plant's composites from 4 October 2027 to 30 March 2028 that fail the faecal-strength check:")
    for p in P_:
        w("   - %s %s: %d" % (p["code"], p["name"], p["flags"]))
    w("")
    w("### verification_desk_winter_2028.docx")
    w("")
    w("- The number to plan for, %d alert episodes, and a chart of each plant's winter 2027 episodes on the published "
      "basis and on the shed load (%s lower by one, %s higher by one)." % (
          fig["call"], _list(down), _list(up)))
    w("")
    return "\n".join(lines)
