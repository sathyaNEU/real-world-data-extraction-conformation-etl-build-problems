"""The independent verifier: reads only the shipped bundle and generator/figures.json, on its own code path
(pandas against the generator's csv module), and recomputes every figure the write-up states."""
import datetime as dt
import json
import math
import os
import re

import pandas as pd

K = 0


def ok(flag, label):
    global K
    K += 1
    assert flag, "VERIFY FAILED: %s" % label


def fiscal_year(s):
    return (s.dt.year - (s.dt.month < 7).astype(int)).astype(str).str.slice(2, 4).radd("20") + "-" + \
        ((s.dt.year - (s.dt.month < 7).astype(int) + 1) % 100).map("{:02d}".format)


def quarter_label(s):
    fy = fiscal_year(s)
    qn = s.dt.month.map({7: 1, 8: 1, 9: 1, 10: 2, 11: 2, 12: 2, 1: 3, 2: 3, 3: 3, 4: 4, 5: 4, 6: 4})
    return fy + " Q" + qn.astype(str)


def run(target, figures_path):
    global K
    K = 0
    fig = json.load(open(figures_path))
    ref = None
    try:
        import pypdf
        text = "".join(p.extract_text() for p in
                       pypdf.PdfReader(os.path.join(target, "hac_indicator_specification_v4.pdf")).pages)
        m = re.search(r"reference rate of ([\d.]+) complications per 1,000", text.replace("\n", " "))
        ref = float(m.group(1))
    except Exception:
        ref = None
    ok(ref == 96.6, "the specification's reference rate is 96.6 (%s)" % ref)

    ep = pd.read_csv(os.path.join(target, "episode_outcomes_extract.csv"),
                     parse_dates=["admission_date", "separation_date"], dtype={"unit_code": str})
    units = pd.read_csv(os.path.join(target, "unit_register.csv"), dtype=str)
    bands = pd.read_csv(os.path.join(target, "drg_risk_bands.csv"), dtype=str)
    strata = pd.read_csv(os.path.join(target, "hac_stratum_rates.csv"), dtype={"risk_band": str,
                                                                              "age_band": str})
    plan = pd.read_csv(os.path.join(target, "activity_plan_2027q4.csv"), dtype={"unit_code": str})
    placements = pd.read_csv(os.path.join(target, "improvement_placements.csv"), dtype=str)
    summary = pd.read_csv(os.path.join(target, "activity_summary_monthly.csv"),
                          parse_dates=["month"], dtype={"unit_code": str})

    ep = ep.merge(units[["unit_code", "service_type", "hospital_code"]], on="unit_code", how="left")
    ep = ep.merge(bands[["drg_code", "risk_band"]], on="drg_code", how="left")
    ep["quarter"] = quarter_label(ep["separation_date"])
    ep["fy"] = fiscal_year(ep["separation_date"])
    acute = ep[ep.service_type == "Acute inpatient"].copy()
    ok(not acute.duplicated(["unit_code", "patient_uid", "admission_date", "drg_code"]).any(),
       "no repeated separation in an acute unit")
    scope = acute[(acute.care_type == "Acute") & (acute.los_days >= 1) & acute.risk_band.notna()
                  & (acute.risk_band != "SAME-DAY")].copy()
    scope = scope.merge(strata, on=["risk_band", "age_band"], how="left")
    ok(scope.expected_rate.notna().all(), "every in-scope episode has a published stratum rate")

    grp = scope.groupby(["unit_code", "quarter"]).agg(
        episodes=("episode_id", "size"), observed=("hac_recorded", "sum"),
        expected=("expected_rate", "sum")).reset_index()
    seps = acute.groupby(["unit_code", "quarter"]).size().rename("separations").reset_index()
    grp = grp.merge(seps, on=["unit_code", "quarter"])

    series = pd.read_csv(os.path.join(target, "unit_indicator_series.csv"), dtype={"unit_code": str})
    chk = grp.merge(series, on=["unit_code", "quarter"])
    ok(len(chk) == len(series) == len(grp), "the series and the extract cover the same unit-quarters")
    ok((chk.episodes == chk.in_scope_episodes).all(), "the series' episode counts are the extract's")
    ok((chk.observed == chk.observed_complications).all(), "the series' complications are the extract's")
    ok((chk.expected - chk.expected_complications).abs().max() < 0.002, "the series' expected counts match")

    # charter 4.2
    placed = set(placements.unit_code)
    counts = grp.groupby("unit_code").quarter.nunique()
    open_units = units[(units.service_type == "Acute inpatient") & units.closed_date.isna()].unit_code
    elig = sorted(c for c in open_units if counts.get(c, 0) >= 4 and c not in placed)
    ok(len(elig) == fig["eligible_units"], "twelve eligible units")

    # ---- the observation process, recomputed from the close-out register's own shipped bytes ----
    # The register publishes each quarter when its coding closes and restates it at every close after
    # that. A quarter whose last two publications agree has stopped moving and carries its own ultimate,
    # so the growth from each earlier publication to that ultimate is an observed ratio. Nothing is
    # fitted here and no parameter is chosen.
    reg = pd.read_csv(os.path.join(target, "coding_close_out_register.csv"), dtype={"unit_code": str})
    ok(len(reg) > 200, "the close-out register ships %d rows" % len(reg))
    ok(set(reg.columns) == {"quarter", "published_date", "unit_code", "separations_with_complication"},
       "the register's columns are the four it declares (%s)" % sorted(reg.columns))
    reg = reg.sort_values(["quarter", "unit_code", "published_date"])
    cells = {}
    for (q, u), d in reg.groupby(["quarter", "unit_code"]):
        cells[(q, u)] = list(zip(d.published_date, d.separations_with_complication.astype(int)))
    finished = {k: v for k, v in cells.items() if len(v) >= 2 and v[-1][1] == v[-2][1]}
    ok(len(finished) > 50, "%d of the register's %d cells have stopped moving" % (len(finished), len(cells)))

    def factors(weighting="volume", quarters_from=None):
        num, den, rat = {}, {}, {}
        for (q, u), s_ in finished.items():
            if quarters_from is not None and q < quarters_from:
                continue
            final = s_[-1][1]
            for lag, (_, n) in enumerate(s_):
                if n <= 0:
                    continue
                num[(u, lag)] = num.get((u, lag), 0.0) + final
                den[(u, lag)] = den.get((u, lag), 0.0) + n
                rat.setdefault((u, lag), []).append(final / n)
        if weighting == "simple":
            return {k: sum(v) / len(v) for k, v in rat.items() if v}
        return {k: num[k] / den[k] for k in den if den[k]}

    # which quarters are still filling, and how many closes each has had, from the register alone
    pubs = reg.groupby("quarter").published_date.nunique()
    moving = sorted({q for (q, u), v in cells.items() if (q, u) not in finished})
    lags = {q: int(pubs[q]) - 1 for q in moving}
    ok(sorted(lags.values()) == [0, 1, 2, 3, 4],
       "the register shows five quarters at five stages of settling (%s)" % lags)
    ok(sorted(q for q, v in lags.items() if v > 0) == sorted(fig["quarters_still_moving"]),
       "the four quarters still filling are the ones figures.json names")

    F = factors()
    ok(abs(F[(fig["call_unit_code"], 0)] - fig["pick_factor_at_lag_0"]) < 5e-4,
       "the call's own development factor at lag 0 recomputes (%.4f)" % F[(fig["call_unit_code"], 0)])
    ok(abs(F[(fig["runner_unit_code"], 0)] - fig["runner_factor_at_lag_0"]) < 5e-4,
       "the runner-up's development factor at lag 0 recomputes (%.4f)"
       % F[(fig["runner_unit_code"], 0)])
    ok(F[(fig["call_unit_code"], 0)] > F[(fig["runner_unit_code"], 0)],
       "the call's quarters are further from settled than the runner-up's")
    for (u, l), v in F.items():
        ok(v >= 1.0, "no cost centre's quarter shrinks after its own close (%s lag %d)" % (u, l))

    allq = sorted(grp.quarter.unique())
    ok(len(allq) == 10, "the record carries ten closed quarters (%d)" % len(allq))
    gi = grp.set_index(["unit_code", "quarter"])
    pl = plan.set_index("unit_code").planned_separations

    def avoidable(develop=True, window=None, denom="separations", fac=None, netwide=False, fill_own=False):
        """Charter 4.3 carried onto the planned separations under specification 3.4, one reading.

        The expectation is the published stratum table of Appendix A, which specification 3.1 files and
        which every reading here shares; what the readings differ on is how the observed count of a
        quarter that is still filling is carried to what that quarter's patients had.
        """
        fac = F if fac is None else fac
        qs_ = list(window or allq)
        rows = {}
        for u in elig:
            o = e = sp = 0.0
            for q in qs_:
                if (u, q) not in gi.index:
                    continue
                row = gi.loc[(u, q)]
                e += float(row.expected)
                sp += float(row.separations)
                n = float(row.observed)
                if not develop or q not in lags:
                    o += n
                elif netwide:
                    o += n * netblend[lags[q]]
                elif fill_own:
                    o += n * own_ratio[u]
                else:
                    o += n * fac.get((u, lags[q]), 1.0)
            if not sp:
                continue
            d = sp if denom == "separations" else float(
                sum(gi.loc[(u, q)].episodes for q in qs_ if (u, q) in gi.index))
            rows[u] = (o - e) * int(pl[u]) / d
        return rows

    # one factor for the whole network at a lag, ignoring which cost centre the complications sat in
    netblend = {}
    for lag in range(5):
        a_ = b_ = 0.0
        for (q, u), s_ in finished.items():
            if lag >= len(s_) or s_[lag][1] <= 0:
                continue
            a_ += s_[-1][1]
            b_ += s_[lag][1]
        netblend[lag] = a_ / b_ if b_ else 1.0
    # each unit's own ratio over the quarters that have finished, applied to the short ones
    own_ratio = {}
    for u in elig:
        done = [q for q in allq if q not in lags and (u, q) in gi.index]
        shrt = [q for q in allq if q in lags and (u, q) in gi.index]
        o_done = sum(float(gi.loc[(u, q)].observed) for q in done)
        e_done = sum(float(gi.loc[(u, q)].expected) for q in done)
        own_ratio[u] = (o_done / e_done) if e_done else 1.0
        if shrt:
            o_s = sum(float(gi.loc[(u, q)].observed) for q in shrt)
            e_s = sum(float(gi.loc[(u, q)].expected) for q in shrt)
            own_ratio[u] = (own_ratio[u] * e_s / o_s) if o_s else 1.0

    base = avoidable()
    order = sorted(base, key=lambda u: -base[u])
    ok(order[0] == fig["call_unit_code"], "the call is the unit charter 4.3 puts first")
    ok(round(base[order[0]], 1) == fig["avoidable_at_pick"], "the call's avoidable complications")
    ok(round(base[order[1]], 1) == fig["avoidable_at_runner"], "the closest unit's avoidable complications")
    ok(order[1] == fig["runner_unit_code"], "the closest unit")
    ok(order[2] == fig["third_unit_code"], "the third unit")
    ok(round(round(base[order[0]], 1) - round(base[order[1]], 1), 1) == fig["gap_complications"],
       "the gap")
    for u, v in base.items():
        ok(round(v, 1) == fig["avoidable_by_unit"][u], "the avoidable count at %s" % u)
        ok(round(float(sum(gi.loc[(u, q)].expected for q in allq if (u, q) in gi.index))
                 / float(sum(gi.loc[(u, q)].separations for q in allq if (u, q) in gi.index))
                 * int(pl[u]), 1) == fig["expected_on_plan_by_unit"][u],
           "the expected count on the plan at %s" % u)

    # ---- rung 0: the record as it stands, which is what the series and the dashboard invite ----
    rec = avoidable(develop=False)
    r0 = max(rec, key=lambda u: rec[u])
    ok(r0 == fig["rung0_unit_code"], "rung 0 names %s" % r0)
    ok(r0 != fig["call_unit_code"], "rung 0 does not name the call")
    ok(round(rec[r0], 1) == fig["rung0_as_recorded"], "the rung 0 unit's figure as recorded")
    ok(sorted(rec, key=lambda u: -rec[u]).index(fig["call_unit_code"]) + 1
       == fig["recorded_rank_of_call"], "the call's rank on the record as it stands")
    for u, v in rec.items():
        ok(round(v, 1) == fig["as_recorded_by_unit"][u], "the recorded figure at %s" % u)

    # ---- the other rungs, each recomputed and each naming another unit ----
    rungs = {
        "R1": avoidable(develop=False, window=allq[-4:]),
        "R2": avoidable(develop=True, window=[q for q in allq if q not in lags]),
        "R3": avoidable(netwide=True),
        "R4": avoidable(fill_own=True),
    }
    for lab, r_ in rungs.items():
        w = max(r_, key=lambda u: r_[u])
        ok(w == fig["route_winners"][lab], "rung %s names %s" % (lab[1:], w))
        ok(w != fig["call_unit_code"], "rung %s does not name the call" % lab[1:])
        srt = sorted(r_, key=lambda u: -r_[u])
        ok(srt[1] != fig["call_unit_code"], "the call is not second on rung %s" % lab[1:])
        ok(r_[srt[0]] / r_[srt[1]] >= 1.15,
           "rung %s separates its own first two (%.3fx)" % (lab[1:], r_[srt[0]] / r_[srt[1]]))
    ok(sorted(rungs["R1"], key=lambda u: -rungs["R1"][u]).index(fig["call_unit_code"]) + 1 == len(elig),
       "the recency rung puts the call last of %d" % len(elig))

    # ---- each unit's own sampling error, and the lead measured against it ----
    se = {}
    for u in elig:
        dev = 0.0
        for q in allq:
            if (u, q) not in gi.index:
                continue
            n = float(gi.loc[(u, q)].observed)
            dev += n * F.get((u, lags[q]), 1.0) if q in lags else n
        sp = float(sum(gi.loc[(u, q)].separations for q in allq if (u, q) in gi.index))
        se[u] = math.sqrt(dev) * int(pl[u]) / sp
    se_gap = math.sqrt(se[order[0]] ** 2 + se[order[1]] ** 2)
    lead = (base[order[0]] - base[order[1]]) / se_gap
    ok(abs(se_gap - fig["standard_error_of_gap"]) < 0.05, "the standard error of the gap (%.2f)" % se_gap)
    ok(abs(lead - fig["standard_error_lead"]) < 0.05, "the lead in standard errors (%.2f)" % lead)
    ok(lead > 1.0, "the top two are not inside a standard error of each other (%.2f)" % lead)
    ok(abs(base[order[0]] / base[order[1]] - fig["margin"]) < 0.01, "the margin")

    # ---- C1 every reading of the development the register leaves open, recomputed independently ----
    readings = {
        "the finished quarters' ratios pooled over their counts": avoidable(),
        "the finished quarters' ratios averaged across the quarters": avoidable(fac=factors("simple")),
        "only the finished quarters from 2025-26 on": avoidable(fac=factors(quarters_from="2025-26")),
        "only the finished quarters from 2025-26 on, averaged":
            avoidable(fac=factors("simple", quarters_from="2025-26")),
    }
    for lab, r_ in readings.items():
        w = max(r_, key=lambda u: r_[u])
        srt = sorted(r_, key=lambda u: -r_[u])
        ok(w == fig["call_unit_code"], "C1 %s names the call (%s)" % (lab, w))
        ok(r_[srt[0]] / r_[srt[1]] >= 1.5,
           "C1 %s separates its first two (%.3fx)" % (lab, r_[srt[0]] / r_[srt[1]]))
    ok(len(readings) >= 4, "four or more readings of the development recomputed (%d)" % len(readings))
    spread = max(max(r_.values()) / sorted(r_.values())[-2] for r_ in readings.values()) \
        - min(max(r_.values()) / sorted(r_.values())[-2] for r_ in readings.values())
    ok(spread <= 0.15, "the readings' margins agree to within %.3f" % spread)

    # ---- the exposure the excess is carried on: both alternatives name the same unit ----
    per_ep = avoidable(denom="episodes")
    ok(max(per_ep, key=lambda u: per_ep[u]) == fig["call_unit_code"],
       "SF3 carrying on in-scope episodes names the same unit")

    # ---- every graded figure sits clear of its printed cell's edge, at the stated unit ----
    # the asking sentence states avoidable complications to one decimal, so the cell is 0.1 wide and the
    # distance to the nearest edge is 0.05 less the distance to the cell's centre. The distance is
    # recomputed from the shipped figure here rather than read out of figures.json.
    def edge(v, unit):
        sc = round(1.0 / unit)
        return unit / 2.0 - abs(v - round(v * sc) / float(sc))
    for u, v in base.items():
        ok(edge(v, 0.1) >= 0.03,
           "%s's avoidable count sits %.4f from the one-decimal edge" % (u, edge(v, 0.1)))
    av = sorted(base.values())
    ok(min(av[i + 1] - av[i] for i in range(len(av) - 1)) > 0.1,
       "the closest pair of adjacent graded units is %.4f apart, above the printed unit"
       % min(av[i + 1] - av[i] for i in range(len(av) - 1)))

    # ---- one readback assertion per shipped format, each with its own positive control ----
    # A search that cannot find what is there has not shown that anything is absent, so every absence
    # claim below runs after a control through the same extractor and the same parse.
    def pdf_text(name):
        import pypdf
        return " ".join(" ".join(p.extract_text() for p in
                                 pypdf.PdfReader(os.path.join(target, name)).pages).split())
    for name, control in (("hac_indicator_specification_v4.pdf",
                           "every closed quarter from 1 July 2024"),
                          ("improvement_partnership_charter_v3.pdf",
                           "counted patient by patient")):
        t = pdf_text(name)
        ok(len(t) > 1200, "%s extracts %d characters of text" % (name, len(t)))
        ok(control in t, "positive control: %s contains %r" % (name, control))
        for w in ("development factor", "completion factor", "incomplete", "provisional",
                  "coding backlog", "reports late", "not yet complete", "immature"):
            ok(w not in t.lower(), "%s does not name the decisive step (%s)" % (name, w))
    import openpyxl
    dash = openpyxl.load_workbook(os.path.join(target, "quality_dashboard_2026q2.xlsx"), data_only=True)
    ws = dash[dash.sheetnames[0]]
    cellvals = [[c for c in row] for row in ws.iter_rows(values_only=True)]
    flat = [str(c) for row in cellvals for c in row if c is not None]
    ok(len(flat) > 100, "the shipped dashboard reads back %d populated cells" % len(flat))
    ok(any("Standardised ratio" in s or "standardised_ratio" in s for s in flat),
       "positive control: the dashboard carries its standardised ratio column")
    ok(dash.sheetnames == ["Quarter position", "Notes"],
       "the dashboard ships the two sheets it declares (%s)" % dash.sheetnames)
    ok(all(dash[n].sheet_state == "visible" for n in dash.sheetnames),
       "no sheet of the dashboard is hidden")
    notes_ws = dash["Notes"]
    notes_flat = [str(c) for row in notes_ws.iter_rows(values_only=True) for c in row if c is not None]
    ok(len(notes_flat) >= 3, "the dashboard's Notes sheet reads back %d cells" % len(notes_flat))
    ok(any("quarter" in s.lower() for s in notes_flat),
       "positive control: the Notes sheet names the quarter it reports")
    for w in ("development", "incomplete", "provisional", "backlog", "restate", "still being coded"):
        ok(not any(w in s.lower() for s in flat + notes_flat),
           "the dashboard does not name the decisive step (%s)" % w)
    # Gate G: the dashboard must not rank the candidates on the decision question
    codes_in_order = [s for s in flat if s in set(elig)]
    ok(codes_in_order != [u for u in sorted(base, key=lambda x: -base[x]) if u in codes_in_order],
       "the dashboard does not carry the candidates in the decision's own order")
    ok(codes_in_order != [u for u in sorted(rec, key=lambda x: -rec[x]) if u in codes_in_order],
       "the dashboard does not carry the candidates in the record's own order either")
    notes = open(os.path.join(target, "placement_cycle_notes.txt"), encoding="utf-8").read()
    ok(len(notes) > 400, "the placement notes read back %d characters" % len(notes))
    ok("cycle" in notes.lower(), "positive control: the placement notes mention a cycle")
    for w in ("develop", "backlog", "incomplete", "still coding", "restate"):
        ok(w not in notes.lower(), "the placement notes do not name the decisive step (%s)" % w)

    # ask 2: the hospital year, on the site each unit reported under in the month
    summary["month_key"] = summary.month.dt.strftime("%Y-%m-%d")
    fac = dict(zip(zip(summary.unit_code, summary.month_key), summary.facility))
    # ask 2: what the indicator does not measure at each hospital, over every unit at the site. The
    # separations come from the system that counts them, the activity summary, and the ones the indicator
    # does not measure are those separations less the in-scope episodes it measured. The episode extract
    # is one row per record the warehouse received and is not the authority on separations: it runs short
    # where the day-procedure feed missed a window and long where one separation reached it as two
    # episode records.
    y = scope[(scope.separation_date >= "2026-01-01") & (scope.separation_date <= "2026-12-31")].copy()
    y["month"] = y.separation_date.values.astype("datetime64[M]")
    meas = y.groupby(["unit_code", "month"]).agg(
        episodes=("episode_id", "size"), observed=("hac_recorded", "sum")).reset_index()
    sa = summary[summary.month.dt.year == 2026].copy()
    sa = sa.merge(meas, left_on=["unit_code", "month"], right_on=["unit_code", "month"], how="left")
    sa[["episodes", "observed"]] = sa[["episodes", "observed"]].fillna(0)
    hy = sa.groupby("facility").apply(lambda d: pd.Series({
        "reported": int(d.separations.sum()),
        "measured": int(d.episodes.sum()),
        "excluded": int(d.separations.sum() - d.episodes.sum()),
        "excluded_hac": int(d.episodes_with_complication.sum() - d.observed.sum())}),
        include_groups=False)
    ok(len(hy) == 4, "the ask covers the four hospitals (%d)" % len(hy))
    for site, row in hy.iterrows():
        f = fig["hospital_year"][site]
        ok(int(row.reported) == f["separations_reported"],
           "the separations reported at %s (%d)" % (site, int(row.reported)))
        ok(int(row.measured) == f["episodes_measured"], "the episodes measured at %s" % site)
        ok(int(row.excluded) == f["separations_not_measured"],
           "the separations the indicator does not measure at %s" % site)
        ok(int(row.excluded_hac) == f["not_measured_with_a_complication"],
           "those separations with a complication at %s" % site)
        ok(int(row.reported) == int(row.measured) + int(row.excluded),
           "the three figures reconcile at %s" % site)
    # the two devices, measured: counting the extract's own rows is wrong at every site, and in both
    # directions, so neither device's absence would leave a figure reachable by the ordinary read
    ex = ep.copy()
    ex = ex[(ex.separation_date >= "2026-01-01") & (ex.separation_date <= "2026-12-31")].copy()
    ex["month"] = ex.separation_date.values.astype("datetime64[M]")
    ex["site"] = [fac[(u, d.strftime("%Y-%m-%d"))] for u, d in zip(ex.unit_code, ex.month)]
    inscope_ids = set(scope.episode_id)
    exo = ex[~ex.episode_id.isin(inscope_ids)]
    rowcount = exo.groupby("site").size()
    haccount = exo[exo.hac_recorded == 1].groupby("site").size()
    worst = []
    for s_ in hy.index:
        d_sep = int(rowcount.get(s_, 0)) - int(hy.loc[s_].excluded)
        d_hac = int(haccount.get(s_, 0)) - int(hy.loc[s_].excluded_hac)
        ok(abs(d_sep) >= 3,
           "counting the extract's own rows misses %s's separations by %d" % (s_, d_sep))
        ok(abs(d_hac) >= 3,
           "counting the extract's own rows misses %s's complications by %d" % (s_, d_hac))
        worst += [abs(d_sep), abs(d_hac)]
    ok(min(worst) >= 3,
       "the smallest gap between the ordinary read and the truth over the eight figures is %d, on a bin "
       "of half a separation" % min(worst))
    ok(len({1 if int(rowcount.get(s_, 0)) > int(hy.loc[s_].excluded) else 0 for s_ in hy.index}) == 2,
       "the ordinary read runs long at some sites and short at others, so one correction cannot fix it")

    # ask 3: the units outside the indicator, on distinct separations. Two steps: the overlapping monthly
    # load is collapsed on the separation key the dictionary states, then the episodes of a stay whose care
    # type changed inside it are chained, because the patient left the hospital once and the activity
    # summary counts the separation once
    out = ep[ep.service_type != "Acute inpatient"].copy()
    out = out.drop_duplicates(["unit_code", "patient_uid", "admission_date", "drg_code"])
    out = out.sort_values(["unit_code", "patient_uid", "drg_code", "admission_date", "separation_date"])
    chain = []
    ends = {}
    for rec in out.itertuples(index=False):
        k = (rec.unit_code, rec.patient_uid, rec.drg_code)
        j = ends.pop((k, rec.admission_date), None)
        if j is None:
            chain.append([rec.separation_date, bool(rec.hac_recorded)])
            j = len(chain) - 1
        else:
            chain[j][0] = max(chain[j][0], rec.separation_date)
            chain[j][1] = chain[j][1] or bool(rec.hac_recorded)
        ends[(k, rec.separation_date)] = j
    stay = pd.DataFrame(chain, columns=["separation_date", "hac"])
    stay["quarter"] = quarter_label(stay["separation_date"])
    oq = stay.groupby("quarter").agg(separations=("hac", "size"), with_complication=("hac", "sum"))
    for q, f in fig["outside_indicator"].items():
        row = oq.loc[q]
        ok(int(row.separations) == f["separations"], "the separations outside the indicator in %s" % q)
        ok(int(row.with_complication) == f["with_complication"], "those with a complication in %s" % q)
    # the device is fair: the stays reproduce the activity summary quarter by quarter, and the stated key
    # alone, which is the careful stop, lands clear above it
    sm = summary.merge(units[["unit_code", "service_type"]], on="unit_code", how="left")
    sm = sm[sm.service_type != "Acute inpatient"].copy()
    sm["quarter"] = quarter_label(sm["month"])
    sq = sm.groupby("quarter").separations.sum()
    for q in oq.index:
        ok(int(oq.loc[q].separations) == int(sq.loc[q]),
           "the chained stays tie to the activity summary in %s (%d)" % (q, int(sq.loc[q])))
    key_only = out.groupby("quarter").size()
    for q in oq.index:
        ok(int(key_only.loc[q]) > int(oq.loc[q].separations),
           "the stated key alone runs above the separations reported in %s (%d against %d)"
           % (q, int(key_only.loc[q]), int(oq.loc[q].separations)))

    # ask 4: the complication groups, by fiscal year
    det = pd.read_csv(os.path.join(target, "hac_detail_extract.csv"), parse_dates=["separation_date"],
                      dtype={"unit_code": str})
    cat = pd.read_csv(os.path.join(target, "hac_category_list.csv"), dtype=str)
    g26 = dict(zip(cat.complication_code, cat.group_id))
    g22 = {}
    for line in text.replace("\n", " ").split("HAC"):
        m = re.match(r"^(\d\d)\s*(.+?)\s*(G[1-8])\s", line)
        if m:
            key = "HAC" + m.group(1)
            if key not in g22:
                g22[key] = m.group(3)
    ok(len(g22) >= 12 and g22.get("HAC04") != g26.get("HAC04"),
       "the specification's appendix carries the 2022 revision, which numbers HAC04 differently")
    in_scope_ids = set(scope.episode_id)
    sid_fy = dict(zip(scope.episode_id, scope.fy))
    sid_sep = dict(zip(scope.episode_id, scope.separation_date))
    found = {}
    det = det[det.episode_id.isin(in_scope_ids)]
    for eid, code in zip(det.episode_id, det.complication_code):
        fy = sid_fy[eid]
        if fy not in ("2025-26", "2026-27"):
            continue
        table = g26 if sid_sep[eid] >= pd.Timestamp("2026-07-01") else g22
        found.setdefault((fy, table[code]), set()).add(eid)
    covered = set(det.unit_code)
    rest = scope[(scope.hac_recorded == 1) & (~scope.unit_code.isin(covered))
                 & scope.fy.isin(["2025-26", "2026-27"])]
    for eid, code, fy, sep in zip(rest.episode_id, rest.hac_category_code, rest.fy, rest.separation_date):
        table = g26 if sep >= pd.Timestamp("2026-07-01") else g22
        found.setdefault((fy, table[code]), set()).add(eid)
    for gid, f in fig["complication_groups"].items():
        ok(len(found.get(("2025-26", gid), set())) == f["fy2025_26"], "group %s in 2025-26" % gid)
        ok(len(found.get(("2026-27", gid), set())) == f["fy2026_27"], "group %s in 2026-27" % gid)

    # the goldens carry the same figures
    import openpyxl
    task = os.path.dirname(target)
    wb = openpyxl.load_workbook(os.path.join(task, "golden", "embed_placement_2027q4.xlsx"))
    ws = wb["Placement"]
    seen, recorded, ratios = {}, {}, {}
    for row in ws.iter_rows(min_row=5, values_only=True):
        if row[0] and str(row[0]).isdigit():
            seen[str(row[0])] = row[7]
            recorded[str(row[0])] = row[4]
            ratios[str(row[0])] = (row[5], row[6])
    ok(seen == fig["avoidable_by_unit"], "the workbook carries every unit's avoidable count")
    ok(recorded == fig["as_recorded_by_unit"],
       "the workbook carries every unit's figure on the record as it stands")
    # the workbook's own cells are read back at the precision the asking sentence states
    for u, v in seen.items():
        ok(abs(v - round(v, 1)) < 1e-9, "the workbook states %s's count to one decimal (%s)" % (u, v))
    ok(ratios[fig["call_unit_code"]] == (fig["pick_published_ratio"], fig["pick_developed_ratio"]),
       "the workbook carries the call's two standardised ratios")
    hs = wb["Hospital year"]
    hw = {r[0]: (r[1], r[2]) for r in hs.iter_rows(min_row=5, values_only=True) if r[0]}
    want = {v["name"]: (v["separations_not_measured"], v["not_measured_with_a_complication"])
            for v in fig["hospital_year"].values()}
    ok(hw == want, "the workbook carries what the indicator does not measure at each hospital")
    gi = wb["Outside the indicator"]
    outside = {r[0]: (r[1], r[2]) for r in gi.iter_rows(min_row=5, values_only=True) if r[0]}
    ok(outside == {k: (v["separations"], v["with_complication"])
                   for k, v in fig["outside_indicator"].items()},
       "the workbook carries the activity outside the indicator")
    cg = wb["Complication groups"]
    groups = {r[0]: (r[2], r[3]) for r in cg.iter_rows(min_row=5, values_only=True) if r[0]}
    ok(groups == {k: (v["fy2025_26"], v["fy2026_27"]) for k, v in fig["complication_groups"].items()},
       "the workbook carries the complication groups")
    try:
        import pypdf
        txt = " ".join(" ".join(pg.extract_text() for pg in pypdf.PdfReader(
            os.path.join(task, "golden", "embed_placement_brief.pdf")).pages).split())
        ok(len(txt) > 2000, "the brief extracts %d characters of text" % len(txt))
        ok("Clinical Improvement Partnership" in txt,
           "positive control: the brief carries its own kicker line")
        ok(str(fig["avoidable_at_pick"]) in txt and fig["call_unit_code"] in txt,
           "the brief states the call and its figure")
        ok("%.1f" % fig["gap_complications"] in txt, "the brief states the gap it claims")
        ok("%.1f" % fig["avoidable_at_runner"] in txt, "the brief states the closest unit's figure")
        ok("%.3f" % fig["pick_factor_at_lag_0"] in txt
           and "%.3f" % fig["runner_factor_at_lag_0"] in txt,
           "the brief states both development factors it compares")
        ok("%.0f" % fig["pick_uplift_complications"] in txt,
           "the brief states the uplift the development adds to the call's record")
        # the brief claims a range over the readings of the development; it is checked at both ends
        lo = min(fig["reading_margins"].values())
        hi = max(fig["reading_margins"].values())
        ok("%.2f" % lo in txt and "%.2f" % hi in txt,
           "the brief's robustness range is the measured range (%.2f to %.2f)" % (lo, hi))
        ok("standard error" not in txt.lower(),
           "the brief claims no figure the prompt did not ask for")
        ok(fig["rung0_unit_code"] in txt and fig["route_winners"]["R1"] in txt,
           "the brief names the unit the record as it stands points at and the recency rung's unit")
        ok("published stratum table expects" in txt,
           "the brief states the comparison as the published table the charter files")
        ok("%.1f" % fig["rung0_as_recorded"] in txt and "%.1f" % fig["route_first_values"]["R1"] in txt,
           "every rejected route the brief names carries the figure it recomputes to")
    except ImportError:
        pass
    return K


if __name__ == "__main__":
    import sys
    tgt = sys.argv[1]
    print("independent checks", run(tgt, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                      "figures.json")))
