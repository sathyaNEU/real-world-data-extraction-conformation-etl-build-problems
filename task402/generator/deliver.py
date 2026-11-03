"""The golden deliverables (paper, workbook, chart), figures.json's content and metadata.json."""
import json, os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import docx
from docx.shared import Pt, Inches
import docs
from golden import CHANGES, QN, MONTHS

ORDER_NAMES = {"G": "SO-7 restoration switching revision (1 Dec 2025)", "R": "Heat pumps connected without a load study (1 Nov 2025)",
               "D": "Riser termination replacements suspended (1 Oct 2025)", "E": "Animal guard programme ended (1 Jan 2026)",
               "F": "Transformer supplier change (1 Feb 2026)"}


def r100(v):
    return int(round(v / 100.0) * 100)


def write(TASK, P, m, a, h, p):
    G = os.path.join(TASK, "golden")
    os.makedirs(G, exist_ok=True)
    costs = {k: r100(v) for k, v in m.items()}
    order = sorted(costs, key=lambda k: -m[k])
    win, run = order[0], order[1]
    gap = r100(m[win] - m[run])
    # ---- chart
    fig, ax = plt.subplots(figsize=(8.6, 4.2), dpi=150)
    names = [ORDER_NAMES[k] for k in order][::-1]
    vals = [costs[k] for k in order][::-1]
    cols = ["#1f4e79" if k == win else "#9db3c8" for k in order][::-1]
    ax.barh(names, vals, color=cols, height=0.62)
    for y, v in enumerate(vals):
        ax.text(v + max(vals) * 0.01, y, format(v, ","), va="center", fontsize=9)
    ax.set_xlabel("Sustained customer interruptions, fiscal 2026 (major event days excluded)", fontsize=9)
    ax.set_title("What each fiscal 2026 change cost members", fontsize=11, loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=8.5)
    ax.set_xlim(0, max(vals) * 1.12)
    fig.tight_layout()
    png = os.path.join(G, "fy2026_interruptions_by_change.png")
    fig.savefig(png, metadata={"Software": None})
    plt.close(fig)
    # ---- workbook
    xl = os.path.join(G, "interruption_costing_fy2026.xlsx")
    dists = ["North", "Lakes", "Prairie", "River"]
    with pd.ExcelWriter(xl, engine="openpyxl") as xw:
        pd.DataFrame({"Change": [ORDER_NAMES[k] for k in order],
                      "Sustained customer interruptions, FY2026": [costs[k] for k in order]}).to_excel(xw, sheet_name="Change costs", index=False)
        pd.DataFrame([[d] + [round(a[(d, q)], 2) for q in (1, 2, 3, 4)] for d in dists],
                     columns=["District"] + [QN[q] for q in (1, 2, 3, 4)]).to_excel(xw, sheet_name="MAIFIe by district", index=False)
        pd.DataFrame({"Month": MONTHS, "Callout hours": [int(round(x)) for x in h],
                      "Callout pay (USD)": [int(round(x)) for x in p]}).to_excel(xw, sheet_name="Restoration callouts", index=False)
        for ws in xw.book.worksheets:
            for col in ws.columns:
                ws.column_dimensions[col[0].column_letter].width = max(14, max(len(str(c.value or "")) for c in col) + 2)
    docs.scrub_xlsx(xl, "Kayla Dean", "2026-11-02T14:00:00Z", "2026-11-03T16:30:00Z", (2026, 11, 3, 10, 30, 0))
    # ---- paper
    F = P["F"]
    d = docx.Document()
    st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(11)
    def para(text, bold=False, size=None):
        q = d.add_paragraph(); r = q.add_run(text); r.bold = bold
        if size:
            r.font.size = Pt(size)
        return q
    para("2027 Reliability Work Plan: the one fix", True, 15)
    para("To the Board of Trustees, for the meeting of 24 November 2026. From Reliability Engineering, 3 November 2026.", size=9.5)
    para("Recommendation", True, 12)
    para("Fund the 2027 fix for the SO-7 restoration switching revision. Since 1 December 2025 the control centre has "
         "re-energised each section in one switching step. Sections restored that way after an hour or more without supply on "
         "a frost day often tripped again on overload within minutes, interrupting the same members a second time. That cost "
         "about %s sustained customer interruptions in fiscal 2026. The runner-up is the %s at about %s, a gap of about %s."
         % (format(costs[win], ","), ORDER_NAMES[run].split(" (")[0].lower(), format(costs[run], ","), format(gap, ",")))
    para("What each change cost in fiscal 2026", True, 12)
    t = d.add_table(rows=1, cols=2); t.style = "Table Grid"
    t.cell(0, 0).text = "Change (in place)"; t.cell(0, 1).text = "Sustained customer interruptions"
    for k in order:
        c = t.add_row().cells; c[0].text = ORDER_NAMES[k]; c[1].text = format(costs[k], ",")
    d.add_paragraph()
    d.add_picture(os.path.join(G, "fy2026_interruptions_by_change.png"), width=Inches(6.2))
    para("How each change was costed", True, 12)
    para("Each change is costed under Board Policy 407 section 3: the customer interruptions in fiscal 2026 that would not have "
         "occurred without it, unplanned records of five minutes or more, major event days excluded (IEEE 1366, threshold "
         "%.1f SAIDI minutes a day from fiscal 2021 to 2025)." % P["tmed"])
    para("SO-7 revision: every overload trip on a section that began within ten minutes of the same section's restoration from "
         "an interruption of an hour or more on a day averaging -3 C or colder, from 1 December 2025. In the fourteen months "
         "of stepped pickup before it (October 2024 to November 2025) no restoration was followed by such a trip, so nothing is "
         "netted off.")
    para("Heat pump connections: overload interruptions on the service transformers serving members connected under the "
         "waiver, after each connection. A load study checks the service transformer and secondary, so these are the "
         "interruptions a study would have prevented; the rebate goes only to homes already heated electrically, and "
         "sections with a waiver connection re-tripped after restoration no more often than other electrically heated "
         "sections.")
    para("Riser terminations: failures at the risers on the 2025 replacement list from 1 October 2025. Animal guards: animal "
         "contacts at the 2026 list's sites from 1 January 2026. Transformer supplier: failures of Brekke units fitted from "
         "1 February 2026.")
    para("The overload category as a whole rose by about %s customer interruptions on fiscal 2025. Most of that rise is the "
         "re-trips above, not heat pump load." % format(r100(_ovl_rise(P)), ","))
    para("Kayla Dean, Manager, Reliability Engineering", size=9.5)
    d.core_properties.author = "Kayla Dean"
    dp = os.path.join(G, "reliability_fix_2027.docx")
    d.save(dp)
    docs.scrub_docx(dp, "Kayla Dean", (2026, 11, 3, 10, 52, 0), "2026-11-03T16:52:00Z")
    figs = {"call": CHANGES[win], "runner_up": CHANGES[run], "costs": {CHANGES[k]: costs[k] for k in order},
            "costs_raw": {k: round(v, 1) for k, v in m.items()}, "gap": gap, "tmed": round(P["tmed"], 1),
            "ovl_rise": r100(_ovl_rise(P)),
            "maifi": {"%s|Q%d" % (d_, q): round(a[(d_, q)], 2) for d_ in dists for q in (1, 2, 3, 4)},
            "callout_hours": {MONTHS[i]: int(round(h[i])) for i in range(12)},
            "callout_pay": {MONTHS[i]: int(round(p[i])) for i in range(12)},
            "refs": {"policy": 407, "policy_section": "3.2", "standard": 1366, "beta": 2.5, "frost_c": -3, "window_min": 10,
                     "qualifying_min": 60, "chain_gap_min": 15, "minimum_hours": 2, "plan_year": 2027,
                     "article_callout": 14, "article_holidays": 18}}
    return figs


def _ovl_rise(P):
    import ladder as L
    return L.category_rise(P["F"], P["med"], "OVLD")


def metadata(TASK):
    src = "Synthetic records generated for this task by its generator (no real utility's data); CC0 1.0."
    files = {
        "outage_events_fy2022-fy2026.csv": ("Outage management system extract, fiscal 2022 to 2026", "2026-10-05"),
        "restoration_steps_fy2025-fy2026.csv": ("Outage management system restoration step table", "2026-10-05"),
        "scada_reclosing_operations_fy2026.csv": ("SCADA historian export, recloser and breaker operations", "2026-10-06"),
        "hq_substation_temperature_hourly.csv": ("SCADA temperature point at the headquarters substation", "2026-10-06"),
        "daily_reliability_fy2021-fy2026.xlsx": ("Daily reliability series, legacy and current outage systems", "2026-10-05"),
        "system_register_2026-09-30.xlsx": ("GIS system register as at 30 September 2026", "2026-10-01"),
        "heat_pump_rebates_fy2024-fy2026.xlsx": ("Member Services rebate register", "2026-10-02"),
        "asset_programme_lists_2022-2026.xlsx": ("Operations programme lists", "2026-09-28"),
        "transformer_units.parquet": ("Asset management transformer unit history", "2026-10-03"),
        "crew_time_overtime_fy2026.csv": ("Timekeeping export, overtime and callout entries", "2026-10-07"),
        "labor_agreement_2024-2027_extract.pdf": ("Labor agreement extract", "2025-10-06"),
        "board_policy_407_reliability_work_plan.docx": ("Board policy", "2025-02-12"),
        "reliability_review_fy2026.docx": ("Reliability review for the October 2026 meeting of the trustees", "2026-10-21"),
        "heat_pump_rebate_terms_2025-26.docx": ("Member Services rebate terms", "2025-10-30"),
        "ivr_calls_fy2026.csv": ("Call centre IVR log", "2026-10-08"),
        "wholesale_power_bills_fy2022-fy2026.xlsx": ("Wholesale power bills by month", "2026-10-09"),
    }
    md = {"task": "task402", "organisation": "Norvale Electric Cooperative (invented)",
          "files": [{"file": f, "description": d, "date": dt, "source": src, "license": "CC0-1.0"} for f, (d, dt) in files.items()],
          "distractors": [{"file": "ivr_calls_fy2026.csv", "why": "member calls follow interruptions and could be read as a measure of harm; the policy counts customer interruptions from the outage system"},
                          {"file": "wholesale_power_bills_fy2022-fy2026.xlsx", "why": "winter peak demand reads as a load story for the heat pumps; no change is costed on it"}],
          "wrong_basis_distractors": [],
          "deliverables": ["reliability_fix_2027.docx", "interruption_costing_fy2026.xlsx", "fy2026_interruptions_by_change.png"]}
    json.dump(md, open(os.path.join(TASK, "metadata.json"), "w"), indent=1)
