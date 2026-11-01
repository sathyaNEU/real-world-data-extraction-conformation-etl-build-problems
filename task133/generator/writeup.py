"""Emits submission.md and generator/figures.json from target/ (every figure the write-up states comes from here)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import golden  # noqa: E402
import params as P  # noqa: E402
import results as R  # noqa: E402


def n0(x):
    return f"{x:,.0f}"


def rivals(F):
    why = "the short grades cannot get there because their bunks are full a few tonnes above today's payloads"
    tail = f" Not about {n0(F['r0_1000'])}, which adds six tonnes to the fleet's average payload."
    if F["r1_1000"] == F["r2_1000"]:
        return (f"Not about {n0(F['r1_1000'])}, where both mass-only routes land (every 50MAX unit's load raised to 50 "
                f"tonnes gross less its tare, or only the loads that sat at the 44-tonne limit raised that far): {why}." + tail)
    return (f"Not about {n0(F['r1_1000'])}, from raising every 50MAX unit's load to 50 tonnes gross less its tare: {why}. "
            f"Not about {n0(F['r2_1000'])}, which raises only the loads that sat at the 44-tonne limit that far." + tail)


def emit(tdir, task_dir):
    F = R.compute(tdir)
    g100 = F["grade_100"]
    L = []
    L += ["## Tags", "",
          "**Domain:** Urban & Regional Science (forecasting: a forestry company's FY2028 log truck loads to its export "
          "port once the 50MAX route limits apply).",
          "**Analytical objective:** Forecasting & Predictive Modeling.", ""]
    L += ["## 1. Final Recommendation", "",
          f"**The FY2028 harvest plan needs {n0(F['total_500'])} export log loads to Port Kowhai under the 50MAX route limits.**",
          "By grade: " + "; ".join(f"{P.GRADES[g]['name']} {n0(g100[g])}" for g in P.GRADE_ORDER) + " loads. " + rivals(F), ""]
    L += ["## 2. Critical Components", "",
          f"1. FY2026 port loads as recorded: **{n0(F['fy26_loads'])} loads** carrying **{n0(F['fy26_tonnes'])} tonnes**.",
          f"2. The FY2028 plan's export tonnes: **{n0(F['plan_total'])} tonnes**.",
          f"3. **{F['permit_share'] * 100:.0f} per cent** of FY2026 port loads were hauled by units holding a 50MAX permit.", ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Matched each ticket in weighbridge_tickets_port_kowhai_FY2026.csv to the scaling record in "
          "log_scaling_port_kowhai_FY2026.csv of the same truck within the following hour, giving each load's JAS volume "
          f"and density: {n0(F['fy26_loads'])} loads, {n0(F['fy26_tonnes'])} tonnes.",
          "2. Read each load's unit from fleet_register_2026-06-30.xlsx by registration (previous registrations included), "
          "with its tare, 50MAX permit and full-bunk volume for the grade's length in export_log_grade_specifications_2025.pdf.",
          "3. Set each load's FY2028 payload (cartage planning basis, RDC-2026-114) as the lesser of its unit's FY2028 "
          "gross limit (50 tonnes with a permit, 44 without) less tare and its full-bunk volume times the load's density.",
          "4. Divided harvest_plan_FY2028.xlsx's export tonnes for each grade by the grade's average FY2028 payload and "
          f"summed: {n0(F['total_500'])} loads to the nearest 500.",
          "5. Cartage: summed cartage_invoices_FY2026.csv lines, credit notes included, against the fleet register's carrier "
          "of the unit on each line's port weighbridge ticket (subcontracted units are billed under their head contractor's code).",
          "6. Domestic deliveries: summed gross less tare in mill_weighbridge_logs_FY2026.csv for loads carrying a Matiri "
          "docket (MFP), by quarter of the weigh-in date, the delivery date; mill_dockets_FY2026.csv dates loads when the "
          "docket was posted.",
          f"7. FY2028 needs {n0(F['total_500'])} export log loads under the 50MAX route limits.", ""]
    L += ["## 4. Deliverable Answers", "", f"### {golden.XLSX}", "",
          f"1. Export log loads needed in FY2028, nearest 500: {n0(F['total_500'])}.",
          "2. FY2028 loads by grade, nearest 100:"]
    for g in P.GRADE_ORDER:
        L.append(f"   - {P.GRADES[g]['name']}: {n0(g100[g])}")
    L.append("3. Per-load working: each FY2026 port load with its unit, tare, JAS volume, density, full-bunk volume and FY2028 payload.")
    L.append("4. Cartage paid for FY2026's loads by the carrier whose unit hauled the load, credit notes netted, NZD thousand:")
    for c in P.CARRIERS:
        L.append(f"   - {P.CARRIERS[c]}: {n0(F['ask_a_k'][c])}")
    L.append("5. FY2026 domestic deliveries by mill and quarter, tonnes, nearest 10:")
    for m in P.MILLS:
        L.append(f"   - {P.MILLS[m]}: " + ", ".join(f"{R.Q_LABEL[q]} {n0(F['ask_b_10'][(m, q)])}" for q in R.QUARTERS))
    L += ["", f"### {golden.PNG}", "",
          "1. Grouped bar chart of loads by grade, FY2026 recorded beside FY2028 needed, each FY2028 bar labelled with its "
          "rounded figure and the total in the title.", ""]
    md = "\n".join(L)
    open(os.path.join(task_dir, "submission.md"), "w", encoding="utf-8").write(md)
    figs = {
        "call": {"fy2028_loads_nearest_500": F["total_500"], "fy2028_loads_unrounded": round(F["total"], 1)},
        "loads_by_grade_nearest_100": {P.GRADES[g]["name"]: g100[g] for g in P.GRADE_ORDER},
        "rivals_nearest_1000": {"permit_units_to_new_limit": F["r1_1000"], "old_limit_loads_only": F["r2_1000"],
                                "fleet_average_plus_six": F["r0_1000"]},
        "components": {"fy2026_loads": F["fy26_loads"], "fy2026_tonnes": round(F["fy26_tonnes"]),
                       "plan_tonnes": F["plan_total"], "permit_share_pct": round(F["permit_share"] * 100)},
        "limits_t": [44, 50, 6],
        "rounding_steps": {"total_loads": 500, "grade_loads": 100, "mill_tonnes": 10, "rivals": 1000},
        "ask_a_cartage_nzd_k": {P.CARRIERS[c]: F["ask_a_k"][c] for c in P.CARRIERS},
        "ask_b_mill_tonnes": {f"{P.MILLS[m]} {q}": F["ask_b_10"][(m, q)] for m in P.MILLS for q in R.QUARTERS},
        "calendar": {"years": [2025, 2026, 2027, 2028], "fy": ["FY2026", "FY2028"]},
    }
    with open(os.path.join(task_dir, "generator", "figures.json"), "w", encoding="utf-8") as f:
        json.dump(figs, f, indent=1, ensure_ascii=False)
        f.write("\n")
    return F, md


if __name__ == "__main__":
    emit(sys.argv[1], sys.argv[2])
