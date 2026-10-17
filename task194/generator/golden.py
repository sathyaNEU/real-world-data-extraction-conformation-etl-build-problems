"""The answer, computed from the shipped bundle only.

Nothing here reads the generator's state: every figure comes out of the files under target/ the way a solver
would build it, so the goldens, the write-up and the verifier all stand on the bundle.
"""
import csv
import datetime as dt
import math
import os
from collections import OrderedDict, defaultdict

REF_RATE = 96.6                      # specification 3.2, read back from the bundle below
SPEC_START = dt.date(2024, 7, 1)
ASSESS_QUARTER = "2026-27 Q4"


def _read(target, name):
    with open(os.path.join(target, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _d(s):
    return dt.date.fromisoformat(s)


def fiscal(day):
    """(fiscal year label, quarter label) of a date, on 1 July to 30 June years."""
    fy = day.year if day.month >= 7 else day.year - 1
    qn = {7: 1, 8: 1, 9: 1, 10: 2, 11: 2, 12: 2, 1: 3, 2: 3, 3: 3, 4: 4, 5: 4, 6: 4}[day.month]
    label = "%d-%02d" % (fy, (fy + 1) % 100)
    return label, "%s Q%d" % (label, qn)


def load(target):
    """The bundle, conformed: the indicator panel, the registers and the plan."""
    units = {r["unit_code"]: r for r in _read(target, "unit_register.csv")}
    bands = {r["drg_code"]: r["risk_band"] for r in _read(target, "drg_risk_bands.csv")}
    strata = {(r["risk_band"], r["age_band"]): float(r["expected_rate"])
              for r in _read(target, "hac_stratum_rates.csv")}
    plan = {r["unit_code"]: int(r["planned_separations"]) for r in _read(target, "activity_plan_2027q4.csv")}
    placements = _read(target, "improvement_placements.csv")
    summary = _read(target, "activity_summary_monthly.csv")
    facility = {(r["unit_code"], r["month"]): r["facility"] for r in summary}

    peer = {r["hospital_code"]: r["peer_group"] for r in _read(target, "hospital_sites.csv")}
    panel = defaultdict(lambda: dict(episodes=0, observed=0.0, expected=0.0, separations=0))
    sc = defaultdict(lambda: defaultdict(lambda: [0, 0]))   # (unit, q) -> stratum -> [episodes, with HAC]
    year2026 = defaultdict(lambda: dict(episodes=0, observed=0, expected=0.0))
    nonacute = defaultdict(lambda: dict(seps=set(), hac=set()))
    groups_by_year = defaultdict(lambda: defaultdict(set))
    seen = set()
    inscope_episode = {}
    with open(os.path.join(target, "episode_outcomes_extract.csv"), newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            unit = row["unit_code"]
            u = units[unit]
            sep = _d(row["separation_date"])
            fy, q = fiscal(sep)
            key = (unit, row["patient_uid"], row["admission_date"], row["drg_code"])
            band = bands.get(row["drg_code"], "")
            in_scope = (row["care_type"] == "Acute" and int(row["los_days"]) >= 1 and band not in ("", "SAME-DAY")
                        and u["service_type"] == "Acute inpatient")
            hac = row["hac_recorded"] == "1"
            if u["service_type"] != "Acute inpatient":
                # the sub-acute feed re-sends a block of records, so a separation is counted once
                nonacute[q]["seps"].add(key)
                if hac:
                    nonacute[q]["hac"].add(key)
                continue
            if key in seen:
                raise AssertionError("repeated separation key in an acute unit: %s" % (key,))
            seen.add(key)
            p = panel[(unit, q)]
            p["separations"] += 1
            if in_scope:
                p["episodes"] += 1
                p["expected"] += strata[(band, row["age_band"])]
                p["observed"] += 1 if hac else 0
                cell = sc[(unit, q)][(band, row["age_band"])]
                cell[0] += 1
                cell[1] += 1 if hac else 0
                inscope_episode[row["episode_id"]] = (unit, sep, fy)
                if dt.date(2026, 1, 1) <= sep <= dt.date(2026, 12, 31):
                    site = facility[(unit, sep.replace(day=1).isoformat())]
                    y = year2026[site]
                    y["episodes"] += 1
                    y["expected"] += strata[(band, row["age_band"])]
                    y["observed"] += 1 if hac else 0
                if hac and row["hac_category_code"] and fy in ("2025-26", "2026-27"):
                    groups_by_year[fy]["principal:" + row["hac_category_code"]].add(row["episode_id"])
    return dict(units=units, bands=bands, strata=strata, plan=plan, placements=placements, peer=peer,
                sc={k: dict(v) for k, v in sc.items()},
                panel=dict(panel), year2026=dict(year2026), nonacute=dict(nonacute),
                principal=dict(groups_by_year), facility=facility, summary=summary,
                inscope_episode=inscope_episode)


def quarters(panel, unit):
    return sorted(q for (u, q) in panel if u == unit)


def pooled(panel, unit, qs):
    o = sum(panel[(unit, q)]["observed"] for q in qs)
    e = sum(panel[(unit, q)]["expected"] for q in qs)
    return (o / e) if e else 0.0, o, e


def eligible_units(b):
    """Charter 4.2: an acute inpatient unit with four or more closed quarters on the current specification,
    and no placement in the previous twelve closed quarters."""
    placed = {p["unit_code"] for p in b["placements"]}
    out = []
    for code, u in b["units"].items():
        if u["service_type"] != "Acute inpatient" or u["closed_date"]:
            continue
        qs = quarters(b["panel"], code)
        if len(qs) < 4 or code in placed:
            continue
        out.append(code)
    return sorted(out)


def record_share(b):
    """The share of a unit's persistent excess a placement removes, from the closed placement register.

    For each closed placement: what the unit stood at over its own closed quarters before the placement,
    the complications that standing carries over the assessment quarter, and what the unit actually
    recorded in it.
    """
    rows = []
    for p in b["placements"]:
        if p["status"] != "closed":
            continue
        unit, q = p["unit_code"], p["assessment_quarter"]
        qs = quarters(b["panel"], unit)
        if q not in qs:
            continue                      # placed before the specification period
        pre = [x for x in qs if x < q]
        ratio, _, _ = pooled(b["panel"], unit, pre)
        e = b["panel"][(unit, q)]["expected"]
        o = b["panel"][(unit, q)]["observed"]
        rows.append(dict(unit=unit, quarter=q, pre_ratio=ratio, expected=e, observed=o,
                         carried=(ratio - 1) * e, realised=o - e, pre_quarters=len(pre)))
    carried = sum(r["carried"] for r in rows)
    removed = sum(r["carried"] - r["realised"] for r in rows)
    return removed / carried, rows, carried, removed


def placement_record(b):
    """Each closed placement, measured from the shipped panel.

    For every closed placement whose assessment quarter is inside the specification period: the level the
    unit was running at over its closed quarters before the team arrived, the complications that level
    carries over the assessment quarter, what the unit recorded in it, and what every other unit did
    between the quarter before and the quarter of the placement.
    """
    panel = b["panel"]
    allq = sorted({q for (_, q) in panel})
    acute = sorted({u for (u, _) in panel})
    rows = []
    for p in b["placements"]:
        if p["status"] != "closed":
            continue
        unit, q = p["unit_code"], p["assessment_quarter"]
        qs = quarters(panel, unit)
        if q not in qs:
            continue
        i = allq.index(q)
        pre = [x for x in qs if x < q]
        e = panel[(unit, q)]["expected"]
        o = panel[(unit, q)]["observed"]
        prev = allq[i - 1]
        # the comparison is the units the team was not working on over those two quarters: a unit inside
        # its own placement's window is not a control for another placement
        treated = set()
        for p2 in b["placements"]:
            if p2["status"] != "closed" or p2["assessment_quarter"] not in allq:
                continue
            j = allq.index(p2["assessment_quarter"])
            treated.update((p2["unit_code"], allq[m]) for m in range(j, min(j + 3, len(allq))))
        others = [c for c in acute if c != unit and (c, prev) in panel and (c, q) in panel
                  and (c, prev) not in treated and (c, q) not in treated]
        pooled_move = (sum(panel[(c, prev)]["observed"] for c in others)
                       / sum(panel[(c, prev)]["expected"] for c in others)
                       - sum(panel[(c, q)]["observed"] for c in others)
                       / sum(panel[(c, q)]["expected"] for c in others))
        before = pooled(panel, unit, pre)[0]
        rows.append(dict(unit=unit, quarter=q, before=before, expected=e, observed=o,
                         carried=(before - 1) * e, realised=o - e,
                         counterfactual=before * e,
                         concurrent_pooled=pooled_move * e))
    return rows


def effect_models(b):
    """What the closed register says a placement does, under each shape the fall could take.

    Each shape is fitted to the seven or more closed placements by weighted least squares with the
    counterfactual count as the variance, which is the error a count of complications carries, and scored
    by the chi-square it leaves. The spread of standing across the register is what separates them: a share
    of standing excess scales with how far above its own level a unit was sitting, a constant drop in the
    standardised ratio does not, and a constant percent of the counterfactual tracks the unit's level.
    """
    rows = placement_record(b)
    n = len(rows)
    fall = [r["carried"] - r["realised"] for r in rows]
    V = [max(1.0, r["counterfactual"]) for r in rows]
    bases = OrderedDict([
        ("a share of the unit's standing excess", [r["carried"] for r in rows]),
        ("a constant drop in the standardised ratio", [r["expected"] for r in rows]),
        ("a constant percent of the counterfactual", [r["counterfactual"] for r in rows]),
        ("a constant number of complications", [1.0] * n),
    ])
    out = OrderedDict()
    for label, x in bases.items():
        num = sum(xi * f / v for xi, f, v in zip(x, fall, V))
        den = sum(xi * xi / v for xi, v in zip(x, V))
        c = num / den if den else 0.0
        chi = sum((f - c * xi) ** 2 / v for xi, f, v in zip(x, fall, V))
        out[label] = dict(parameter=c, chi_square=chi, df=n - 1)
    best = out["a share of the unit's standing excess"]["chi_square"]
    for label, d in out.items():
        d["likelihood_ratio"] = math.exp((d["chi_square"] - best) / 2.0)
    return rows, out


def share_readings(b):
    """The share of a unit's standing excess a placement removes, under every way of reading the register.

    Eight routes a careful analyst could take of the same closed placements: the pooled sums, the mean of
    the placements' own shares, the expected-weighted mean of them, their median, least squares through the
    origin and with an intercept, the variance-weighted fit a count of complications calls for, and the same
    pooled fall net of what the units the team was not working on did over the same two quarters. Every
    placement has a standing excess to take a share of, so every route can be formed; what separates the
    shapes the fall could take is the fit, not whether an estimator exists.
    """
    rows = placement_record(b)
    n = len(rows)
    P = [r["carried"] for r in rows]
    fall = [r["carried"] - r["realised"] for r in rows]
    V = [max(1.0, r["counterfactual"]) for r in rows]
    E = [r["expected"] for r in rows]
    sh = [f / p for f, p in zip(fall, P)]
    pm, fm = sum(P) / n, sum(fall) / n
    pv = sum((p - pm) ** 2 for p in P) / n
    return rows, OrderedDict([
        ("pooled sums", sum(fall) / sum(P)),
        ("the mean of the placements' shares", sum(sh) / n),
        ("the expected-weighted mean of the placements' shares",
         sum(e * s for e, s in zip(E, sh)) / sum(E)),
        ("the median of the placements' shares", sorted(sh)[n // 2]),
        ("least squares through the origin",
         sum(p * f for p, f in zip(P, fall)) / sum(p * p for p in P)),
        ("least squares with an intercept",
         sum((p - pm) * (f - fm) for p, f in zip(P, fall)) / (pv * n)),
        ("the variance-weighted fit",
         sum(p * f / v for p, f, v in zip(P, fall, V)) / sum(p * p / v for p, v in zip(P, V))),
        ("against what the other units did over the same quarters",
         sum(r["carried"] - r["realised"] - r["concurrent_pooled"] for r in rows) / sum(P)),
    ])


def compute(target):
    b = load(target)
    panel = b["panel"]
    share, record, carried, removed = record_share(b)
    _, readings = share_readings(b)
    _, models = effect_models(b)
    elig = eligible_units(b)
    units = []
    for code in elig:
        qs = quarters(panel, code)
        ratio, o, e = pooled(panel, code, qs)
        seps = sum(panel[(code, q)]["separations"] for q in qs)
        per_sep = e / seps                                   # specification 3.4
        e_plan = b["plan"][code] * per_sep
        last = qs[-1]
        y_last = panel[(code, last)]["observed"] / panel[(code, last)]["expected"]
        units.append(dict(
            unit=code, name=b["units"][code]["unit_name"], hospital=b["units"][code]["hospital_code"],
            quarters=len(qs), ratio=ratio, observed=o, expected=e, separations=seps,
            plan=b["plan"][code], expected_plan=e_plan, excess=(ratio - 1) * e_plan,
            avoided=share * (ratio - 1) * e_plan, adjusted_rate=ratio * REF_RATE,
            last_ratio=y_last, last_excess=(y_last - 1) * panel[(code, last)]["expected"],
            last_observed=panel[(code, last)]["observed"],
            expected_next=ratio * e_plan))
    units.sort(key=lambda d: -d["avoided"])
    answer, runner = units[0], units[1]

    # the rungs, for the generator's own assertions
    rung0 = max(units, key=lambda d: share * d["last_excess"])
    rung1 = max(units, key=lambda d: d["ratio"])
    rung2 = max(units, key=lambda d: d["expected_next"])

    # ask 2: the hospital year ended 31 December 2026
    sites = {r["hospital_code"]: r["hospital_name"] for r in _read(target, "hospital_sites.csv")}
    hosp = []
    for code in sorted(b["year2026"]):
        y = b["year2026"][code]
        hosp.append(dict(hospital=code, name=sites[code], episodes=y["episodes"],
                         complications=y["observed"],
                         rate=y["observed"] / y["expected"] * REF_RATE))

    # ask 3: the units outside the indicator, by quarter
    outside = []
    for q in sorted(b["nonacute"]):
        seps = len(b["nonacute"][q]["seps"])
        hac = len(b["nonacute"][q]["hac"])
        outside.append(dict(quarter=q, separations=seps, with_complication=hac,
                            per_1000=hac / seps * 1000))

    # ask 4: the complication groups, by fiscal year
    cat_group, group_names = {}, {}
    for r in _read(target, "hac_category_list.csv"):
        cat_group[(r["list_revision"], r["complication_code"])] = r["group_id"]
        group_names[r["group_id"]] = r["group_name"]
    found = defaultdict(lambda: defaultdict(set))
    detail_units = set()
    for r in _read(target, "hac_detail_extract.csv"):
        detail_units.add(r["unit_code"])
        eid = r["episode_id"]
        if eid not in b["inscope_episode"]:
            continue
        unit, sep, fy = b["inscope_episode"][eid]
        if fy not in ("2025-26", "2026-27"):
            continue
        rev = "2026" if sep >= dt.date(2026, 7, 1) else "2022"
        found[fy][cat_group[(rev, r["complication_code"])]].add(eid)
    # the detail extract covers the units on the clinical information system; the complications of the units
    # it does not reach are in the extract's own category column, one to an episode
    for fy, principal in b["principal"].items():
        if fy not in ("2025-26", "2026-27"):
            continue
        for key, eids in principal.items():
            code = key.split(":", 1)[1]
            for eid in eids:
                unit, sep, _ = b["inscope_episode"][eid]
                if unit in detail_units:
                    continue
                rev = "2026" if sep >= dt.date(2026, 7, 1) else "2022"
                found[fy][cat_group[(rev, code)]].add(eid)
    groups = []
    for gid in sorted(group_names):
        groups.append(dict(group=gid, name=group_names[gid],
                           fy2025=len(found["2025-26"][gid]), fy2026=len(found["2026-27"][gid])))

    return dict(units=units, answer=answer, runner=runner, share=share, record=record,
                carried=carried, removed=removed, rung0=rung0, rung1=rung1, rung2=rung2,
                hospitals=hosp, outside=outside, groups=groups, eligible=elig, readings=readings, models=models,
                gap=round(answer["avoided"]) - round(runner["avoided"]),
                margin=answer["avoided"] / runner["avoided"], bundle=b)


# Appendix B of the specification: the 2022 revision's codes and the groups they belong to. The 2026
# revision renumbered HAC03 to HAC06 and folded HAC13 into HAC03, so a code is read against the revision in
# force at separation.
LIST_2022_GROUPS = {"HAC01": "G1", "HAC02": "G1", "HAC03": "G2", "HAC04": "G3", "HAC05": "G4",
                    "HAC06": "G4", "HAC07": "G5", "HAC08": "G6", "HAC09": "G6", "HAC10": "G7",
                    "HAC11": "G8", "HAC12": "G8", "HAC13": "G1"}
