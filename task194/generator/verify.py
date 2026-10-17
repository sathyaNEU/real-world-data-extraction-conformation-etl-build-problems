"""The independent verifier: reads only the shipped bundle and generator/figures.json, on its own code path
(pandas against the generator's csv module), and recomputes every figure the write-up states."""
import datetime as dt
import json
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
    ok(ref == 96.5, "the specification's reference rate is 96.5 (%s)" % ref)

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

    # the share a placement removes, from the closed placements
    closed = placements[placements.status == "closed"]
    carried = removed = 0.0
    n_closed = 0
    for _, p in closed.iterrows():
        u, q = p.unit_code, p.assessment_quarter
        own = grp[grp.unit_code == u]
        if q not in set(own.quarter):
            continue
        pre = own[own.quarter < q]
        ratio = pre.observed.sum() / pre.expected.sum()
        row = own[own.quarter == q].iloc[0]
        carried += (ratio - 1) * row.expected
        removed += (ratio - 1) * row.expected - (row.observed - row.expected)
        n_closed += 1
    share = removed / carried
    ok(n_closed == fig["closed_placements"], "seven closed placements inside the specification period")

    # the register read ten ways: the same seven placements priced as a careful analyst could price them
    allq = sorted(grp.quarter.unique())
    rec = []
    for _, p in closed.iterrows():
        u, q = p.unit_code, p.assessment_quarter
        own = grp[grp.unit_code == u]
        if q not in set(own.quarter):
            continue
        i = allq.index(q)
        prev, dec = allq[i - 1], allq[i - 2]
        pre = own[own.quarter < q]
        row = own[own.quarter == q].iloc[0]
        rp = own[own.quarter == prev].iloc[0]
        rd = own[own.quarter == dec].iloc[0]
        oth = grp[(grp.unit_code != u) & (grp.quarter.isin([prev, q]))]
        wide = oth.pivot_table(index="unit_code", columns="quarter",
                               values=["observed", "expected"], aggfunc="sum").dropna()
        mv = (wide[("observed", prev)] / wide[("expected", prev)]
              - wide[("observed", q)] / wide[("expected", q)])
        pm = (wide[("observed", prev)].sum() / wide[("expected", prev)].sum()
              - wide[("observed", q)].sum() / wide[("expected", q)].sum())
        rec.append(dict(expected=row.expected, realised=row.observed - row.expected,
                        carried=(pre.observed.sum() / pre.expected.sum() - 1) * row.expected,
                        from_decision=(rd.observed / rd.expected - 1) * row.expected,
                        from_previous=(rp.observed / rp.expected - 1) * row.expected,
                        concurrent=float(mv.mean()) * row.expected,
                        concurrent_pooled=float(pm) * row.expected))
    nr = len(rec)
    P = [r["carried"] for r in rec]
    fl = [r["carried"] - r["realised"] for r in rec]
    sh = [f / p for f, p in zip(fl, P)]
    E = [r["expected"] for r in rec]
    pbar, fbar = sum(P) / nr, sum(fl) / nr
    pvar = sum((p - pbar) ** 2 for p in P) / nr
    readings = {
        "mean of the placements' shares": sum(sh) / nr,
        "median of the shares": sorted(sh)[nr // 2],
        "expected-weighted mean of the shares": sum(e * s for e, s in zip(E, sh)) / sum(E),
        "pooled sums": sum(fl) / sum(P),
        "least squares through the origin":
            sum(p * f for p, f in zip(P, fl)) / sum(p * p for p in P),
        "least squares with an intercept":
            sum((p - pbar) * (f - fbar) for p, f in zip(P, fl)) / (pvar * nr),
        "measured from the quarter closed at the decision":
            sum(r["from_decision"] - r["realised"] for r in rec) / sum(r["from_decision"] for r in rec),
        "measured from the quarter before the placement":
            sum(r["from_previous"] - r["realised"] for r in rec) / sum(r["from_previous"] for r in rec),
        "against what the other units did over the same quarters":
            sum(r["from_previous"] - r["realised"] - r["concurrent"] for r in rec) / sum(P),
        "against the other units pooled over the same quarters":
            sum(r["from_previous"] - r["realised"] - r["concurrent_pooled"] for r in rec) / sum(P),
    }
    ok(abs(readings["pooled sums"] - share) < 1e-9, "the golden share is the register's pooled sums")
    for label, want in fig["register_readings"].items():
        ok(abs(readings[label] - want) < 5e-5,
           "the register read as %s is %.5f (%.5f)" % (label, readings[label], want))
    ok(max(readings.values()) / min(readings.values()) - 1 < 0.035,
       "the register's readings sit within 3.5 per cent (%.2f%%)"
       % ((max(readings.values()) / min(readings.values()) - 1) * 100))

    tot = grp.groupby("unit_code").agg(observed=("observed", "sum"), expected=("expected", "sum"),
                                       separations=("separations", "sum"))
    plan_map = dict(zip(plan.unit_code, plan.planned_separations))
    avoided = {}
    for u in elig:
        t = tot.loc[u]
        ratio = t.observed / t.expected
        e_plan = plan_map[u] * t.expected / t.separations
        avoided[u] = share * (ratio - 1) * e_plan
        if u == fig["call_unit_code"]:
            ok(round(ratio, 2) == fig["pick_standardised_ratio"], "the pick's standardised ratio")
            ok(round(e_plan) == fig["pick_expected_complications"], "the pick's expected complications")
            ok(round((ratio - 1) * e_plan, 1) == fig["pick_excess_complications"], "the pick's excess")
            ok(plan_map[u] == fig["pick_planned_separations"], "the pick's planned separations")
    order = sorted(avoided, key=lambda u: -avoided[u])
    ok(order[0] == fig["call_unit_code"], "the call is %s" % fig["call_unit_code"])
    ok(order[1] == fig["runner_unit_code"], "the closest unit is %s" % fig["runner_unit_code"])
    ok(round(avoided[order[0]]) == fig["avoided_at_pick"], "the call's avoided complications")
    ok(round(avoided[order[1]]) == fig["avoided_at_runner"], "the closest unit's avoided complications")
    ok(round(avoided[order[0]]) - round(avoided[order[1]]) == fig["gap_complications"], "the gap")
    for u, v in avoided.items():
        ok(round(v) == fig["avoided_by_unit"][u], "the avoided count at %s" % u)
    # every reading of the register leaves every unit on the same whole complication
    for label, th in readings.items():
        for u in elig:
            t = tot.loc[u]
            alt = th * (t.observed / t.expected - 1) * plan_map[u] * t.expected / t.separations
            ok(round(alt) == fig["avoided_by_unit"][u],
               "%s leaves %s at %d avoided (%.3f)" % (label, u, fig["avoided_by_unit"][u], alt))

    # the rungs the brief names
    last_q = sorted(grp.quarter.unique())[-1]
    lastq = grp[grp.quarter == last_q].set_index("unit_code")
    r0 = fig["rung0_unit_code"]
    ok(round((lastq.loc[r0].observed / lastq.loc[r0].expected - 1) * lastq.loc[r0].expected)
       == fig["rung0_excess_now"], "the quarter's excess at the rung 0 unit")
    ok(round(tot.loc[r0].observed / tot.loc[r0].expected, 2) == fig["rung0_ratio_record"],
       "the rung 0 unit's standing")
    ok(round(lastq.loc[r0].observed / lastq.loc[r0].expected, 2) == fig["rung0_ratio_quarter"],
       "the rung 0 unit's quarter")
    ok(round(avoided[r0]) == fig["rung0_avoided"], "the rung 0 unit's avoided count")
    r1 = fig["rung1_unit_code"]
    ok(round(tot.loc[r1].observed / tot.loc[r1].expected, 2) == fig["rung1_ratio"], "the worst standing")
    ok(round(tot.loc[r1].observed / tot.loc[r1].expected * ref, 1) == fig["rung1_adjusted_rate"],
       "the worst standing's adjusted rate")
    r2 = fig["rung2_unit_code"]
    e2 = plan_map[r2] * tot.loc[r2].expected / tot.loc[r2].separations
    ok(round(tot.loc[r2].observed / tot.loc[r2].expected * e2) == fig["rung2_expected_next"],
       "the complications the harm route counts")

    # ask 2: the hospital year, on the site each unit reported under in the month
    summary["month_key"] = summary.month.dt.strftime("%Y-%m-%d")
    fac = dict(zip(zip(summary.unit_code, summary.month_key), summary.facility))
    y = scope[(scope.separation_date >= "2026-01-01") & (scope.separation_date <= "2026-12-31")].copy()
    y["site"] = [fac[(u, d.replace(day=1).strftime("%Y-%m-%d"))]
                 for u, d in zip(y.unit_code, y.separation_date)]
    hy = y.groupby("site").agg(episodes=("episode_id", "size"), complications=("hac_recorded", "sum"),
                               expected=("expected_rate", "sum"))
    for site, row in hy.iterrows():
        f = fig["hospital_year"][site]
        ok(int(row.episodes) == f["episodes"], "the hospital year's episodes at %s" % site)
        ok(int(row.complications) == f["complications"], "the hospital year's complications at %s" % site)
        ok(round(row.complications / row.expected * ref, 1) == f["adjusted_rate_per_1000"],
           "the hospital year's adjusted rate at %s" % site)

    # ask 3: the units outside the indicator, on distinct separations
    out = ep[ep.service_type != "Acute inpatient"].copy()
    out = out.drop_duplicates(["unit_code", "patient_uid", "admission_date", "drg_code"])
    oq = out.groupby("quarter").agg(separations=("episode_id", "size"),
                                    with_complication=("hac_recorded", "sum"))
    for q, f in fig["outside_indicator"].items():
        row = oq.loc[q]
        ok(int(row.separations) == f["separations"], "the separations outside the indicator in %s" % q)
        ok(int(row.with_complication) == f["with_complication"], "those with a complication in %s" % q)

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
    seen = {}
    for row in ws.iter_rows(min_row=5, values_only=True):
        if row[0] and str(row[0]).isdigit():
            seen[str(row[0])] = row[5]
    ok(seen == fig["avoided_by_unit"], "the workbook carries every unit's avoided count")
    hs = wb["Hospital year"]
    rates = {r[0]: r[3] for r in hs.iter_rows(min_row=5, values_only=True) if r[0]}
    ok(sorted(rates.values()) == sorted(v["adjusted_rate_per_1000"] for v in fig["hospital_year"].values()),
       "the workbook carries the hospital rates")
    return K


if __name__ == "__main__":
    import sys
    tgt = sys.argv[1]
    print("independent checks", run(tgt, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                      "figures.json")))
