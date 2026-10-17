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

    # ---- the comparison frequency charter 4.3 asks for, measured from the record itself ----
    # no file carries it: this is the frequency the acute record's own in-scope episodes show, by stratum
    def freq(df):
        t = df.groupby(["risk_band", "age_band"]).agg(
            n=("episode_id", "size"), o=("hac_recorded", "sum")).reset_index()
        t["r_net"] = t.o / t.n
        return t[["risk_band", "age_band", "r_net"]]

    allq = sorted(grp.quarter.unique())
    ok(len(allq) == 10, "the record carries ten closed quarters (%d)" % len(allq))
    net = freq(scope)
    ok(len(net) == 24, "twenty-four strata carry a comparison frequency (%d)" % len(net))

    def avoidable(window=None, freq_window=None, denom="separations", leave_out=False,
                  restrict=None):
        """Charter 4.3 carried onto the planned separations under specification 3.4, one reading."""
        f_src = scope if freq_window is None else scope[scope.quarter.isin(freq_window)]
        rows = {}
        for u in elig:
            w = scope[(scope.unit_code == u) & (scope.quarter.isin(window or allq))]
            if restrict == "hospital":
                src = f_src[f_src.hospital_code == units.set_index("unit_code").hospital_code[u]]
            elif restrict == "peer":
                peer = pd.read_csv(os.path.join(target, "hospital_sites.csv"), dtype=str)
                pmap = peer.set_index("hospital_code").peer_group
                mine = pmap[units.set_index("unit_code").hospital_code[u]]
                keep = set(pmap[pmap == mine].index)
                src = f_src[f_src.hospital_code.isin(keep)]
            elif leave_out:
                src = f_src[f_src.unit_code != u]
            else:
                src = f_src
            r = freq(src)
            if restrict:                       # a thin stratum falls back to the whole record
                wide = freq(f_src).set_index(["risk_band", "age_band"]).r_net
                cnt = src.groupby(["risk_band", "age_band"]).size()
                r = r.set_index(["risk_band", "age_band"]).r_net
                r = pd.Series({k: (r[k] if cnt.get(k, 0) >= 30 else wide[k]) for k in wide.index})
                r = r.rename("r_net").reset_index()
                r.columns = ["risk_band", "age_band", "r_net"]
            m = w.merge(r, on=["risk_band", "age_band"], how="left")
            o = m.hac_recorded.sum()
            en = m.r_net.sum()
            sp = len(acute[(acute.unit_code == u) & (acute.quarter.isin(window or allq))])
            d = sp if denom == "separations" else len(m)
            rows[u] = (o - en) * int(plan.set_index("unit_code").planned_separations[u]) / d
        return rows

    base = avoidable()
    order = sorted(base, key=lambda u: -base[u])
    ok(order[0] == fig["call_unit_code"], "the call is the unit charter 4.3 puts first")
    ok(round(base[order[0]]) == fig["avoidable_at_pick"], "the call's avoidable complications")
    ok(round(base[order[1]]) == fig["avoidable_at_runner"], "the closest unit's avoidable complications")
    ok(order[1] == fig["runner_unit_code"], "the closest unit")
    ok(round(base[order[0]]) - round(base[order[1]]) == fig["gap_complications"], "the gap")
    for u, v in base.items():
        ok(round(v) == fig["avoidable_by_unit"][u], "the avoidable count at %s" % u)

    # ---- each unit's own sampling error, and the lead measured against it ----
    se = {}
    for u in elig:
        w = scope[scope.unit_code == u]
        sp = len(acute[acute.unit_code == u])
        se[u] = math.sqrt(w.hac_recorded.sum()) * int(
            plan.set_index("unit_code").planned_separations[u]) / sp
    se_gap = math.sqrt(se[order[0]] ** 2 + se[order[1]] ** 2)
    lead = (base[order[0]] - base[order[1]]) / se_gap
    ok(abs(se_gap - fig["standard_error_of_gap"]) < 0.05, "the standard error of the gap (%.2f)" % se_gap)
    ok(abs(lead - fig["standard_error_lead"]) < 0.05, "the lead in standard errors (%.2f)" % lead)
    ok(lead > 1.0, "the top two are not inside a standard error of each other (%.2f)" % lead)
    ok(abs(base[order[0]] / base[order[1]] - fig["margin"]) < 0.01, "the margin")

    # ---- C1 every reading of charter 4.3 the text leaves open, recomputed independently ----
    w8, w4, w1 = allq[2:], allq[6:], allq[-1:]
    readings = {
        "the comparison frequency measured over the ten closed quarters of the specification period":
            avoidable(),
        "the comparison frequency measured over the eight most recent closed quarters":
            avoidable(freq_window=w8),
        "the comparison frequency measured over the four most recent closed quarters":
            avoidable(freq_window=w4),
        "the comparison frequency measured over the latest closed quarter alone":
            avoidable(freq_window=w1),
        "the unit's own patients left out of the comparison, frequency over the ten closed quarters "
        "of the specification period": avoidable(leave_out=True),
        "the unit's own patients left out of the comparison, frequency over the four most recent "
        "closed quarters": avoidable(freq_window=w4, leave_out=True),
        "the unit's rate taken per all separations in the record": avoidable(denom="separations"),
        "the unit's rate taken per in-scope episodes in the record": avoidable(denom="episodes"),
        "the unit's own record taken over the ten closed quarters of the specification period":
            avoidable(window=allq),
        "the unit's own record taken over the eight most recent closed quarters": avoidable(window=w8),
        "the unit's own record taken over the four most recent closed quarters": avoidable(window=w4),
        "the unit's own record taken over the latest closed quarter alone": avoidable(window=w1),
    }
    ok(len(readings) == fig["readings_of_clause_43"],
       "every reading of charter 4.3 is formed (%d)" % len(readings))
    named = 0
    for label, vec in readings.items():
        o2 = sorted(vec, key=lambda u: -vec[u])
        named += 1 if o2[0] == fig["call_unit_code"] else 0
        ok(o2[0] == fig["call_unit_code"], "C1 %s names the call (%s)" % (label, o2[0]))
        m = vec[o2[0]] / vec[o2[1]]
        ok(abs(m - fig["reading_margins"][label]) < 0.02,
           "C1 %s separates at %.2fx" % (label, m))
    ok(named == fig["readings_naming_the_call"], "every reading names the call (%d)" % named)

    # ---- the readings that do move the call, and the clause that rules each out ----
    moved = {"the comparison restricted to the unit's own hospital": avoidable(restrict="hospital"),
             "the comparison restricted to the hospital's peer group": avoidable(restrict="peer")}
    for label, vec in moved.items():
        o2 = sorted(vec, key=lambda u: -vec[u])
        ok(o2[0] != fig["call_unit_code"], "%s does move the call (to %s)" % (label, o2[0]))

    # ---- the three facts that force the comparison frequency ----
    bb = scope.groupby("risk_band").agg(o=("hac_recorded", "sum"), e=("expected_rate", "sum"))
    drift = (bb.o / bb.e)
    for band, v in drift.items():
        ok(abs(v - fig["band_drift"][band]) < 0.002, "the record's own frequency in %s (%.3f)" % (band, v))
    ok(abs(drift.min() - fig["band_drift_low"]) < 0.002
       and abs(drift.max() - fig["band_drift_high"]) < 0.002, "the frequency's span across the bands")
    ok(drift.min() < 0.95 and drift.max() > 1.05, "it crosses 1.00 in both directions")
    ok(abs(drift.max() / drift.min() - fig["band_drift_spread"]) < 0.02, "the span as a factor")
    sh = {}
    for u in elig:
        w = scope[scope.unit_code == u]
        sh[u] = float(w.risk_band.str.startswith("SURG").sum()) / len(w)
    nz = [v for v in sh.values() if v > 0.01]
    ok(abs(min(nz) - fig["surgical_share_low"]) < 0.002
       and abs(max(sh.values()) - fig["surgical_share_high"]) < 0.002,
       "the candidates' surgical share spans %.3f to %.3f" % (min(nz), max(sh.values())))
    ok(sum(1 for v in sh.values() if v <= 0.01) == fig["candidates_with_no_surgical_work"],
       "the candidates carrying no surgical work at all")

    # ---- the demonstration: a mix shift with the unit's own practice flat ----
    du = fig["demonstration_unit_code"]
    net_i = net.set_index(["risk_band", "age_band"]).r_net
    pub_q, net_q, sh_q = {}, {}, {}
    for q in allq:
        w = scope[(scope.unit_code == du) & (scope.quarter == q)]
        pub_q[q] = w.hac_recorded.sum() - w.expected_rate.sum()
        net_q[q] = w.hac_recorded.sum() - sum(
            net_i[(rb, ab)] for rb, ab in zip(w.risk_band, w.age_band))
        sh_q[q] = float(w.risk_band.str.startswith("SURG").sum()) / len(w)
    shifted = [q for q in allq if sh_q[q] > 0.25]
    ok(len(shifted) == 2, "the shift covers two closed quarters (%d)" % len(shifted))
    ok(abs(min(pub_q.values()) - fig["demonstration_published_low"]) < 0.05
       and abs(max(pub_q.values()) - fig["demonstration_published_high"]) < 0.05,
       "on the published basis its avoidable count runs %.1f to %.1f"
       % (min(pub_q.values()), max(pub_q.values())))
    ok(abs(max(pub_q.values()) / min(pub_q.values()) - fig["demonstration_published_multiple"]) < 0.2,
       "the published basis moves it by a factor of %.1f"
       % (max(pub_q.values()) / min(pub_q.values())))
    ok(abs(min(net_q.values()) - fig["demonstration_comparison_low"]) < 0.05
       and abs(max(net_q.values()) - fig["demonstration_comparison_high"]) < 0.05,
       "on the record's own frequency it runs %.1f to %.1f"
       % (min(net_q.values()), max(net_q.values())))
    ok(max(net_q.values()) - min(net_q.values()) <= 1.5,
       "the record's own frequency holds it inside %.2f of a complication"
       % (max(net_q.values()) - min(net_q.values())))
    ok(max(pub_q[q] for q in shifted) / max(pub_q[q] for q in allq if q not in shifted) > 3.0,
       "the shifted quarters stand well above the rest on the published basis only")

    # ---- the rungs the brief names ----
    pub_x, per_1000 = {}, {}
    for u in elig:
        w = scope[scope.unit_code == u]
        sp = len(acute[acute.unit_code == u])
        pl = int(plan.set_index("unit_code").planned_separations[u])
        pub_x[u] = (w.hac_recorded.sum() - w.expected_rate.sum()) * pl / sp
        per_1000[u] = base[u] / pl * 1000.0
    r0 = max(pub_x, key=lambda u: pub_x[u])
    r3 = max(per_1000, key=lambda u: per_1000[u])
    ok(r0 == fig["rung0_unit_code"], "rung 0 names %s" % r0)
    ok(r3 == fig["rung3_unit_code"], "rung 3 names %s" % r3)
    ok(r0 != fig["call_unit_code"] and r3 != fig["call_unit_code"], "neither rung names the call")
    ok(abs(pub_x[r0] - fig["rung0_published_excess"]) < 0.05, "the rung 0 unit's published excess")
    ok(round(base[r0]) == fig["rung0_avoidable"], "the rung 0 unit's own avoidable count")
    ok(base[r0] < 0, "the easy route files a unit carrying a negative avoidable count (%.1f)" % base[r0])
    ok(sorted(pub_x, key=lambda u: -pub_x[u]).index(fig["call_unit_code"]) + 1
       == fig["published_rank_of_call"], "the call's rank on the published excess")
    for u, v in pub_x.items():
        ok(abs(v - fig["published_excess_by_unit"][u]) < 0.05, "the published excess at %s" % u)

    # ---- every graded figure sits clear of its printed cell's edge ----
    def edge(v, unit):
        sc = round(1.0 / unit)
        return unit / 2.0 - abs(v - round(v * sc) / float(sc))
    for u, v in base.items():
        ok(edge(v, 1.0) >= 0.15, "%s's avoidable count sits %.3f from the edge" % (u, edge(v, 1.0)))

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
