"""task170 deliverables: the golden workbook and chart, generator/figures.json and submission.md, all computed from the
shipped pack in target/ (calc.py)."""
from __future__ import annotations

import json
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import calc
import common as C
import postprocess as PP

F_XLSX = "ruvari_cases_averted_2027.xlsx"
F_PNG = "cases_averted_by_subcounty.png"
BOLD = Font(name="Calibri", size=11, bold=True)
BODY = Font(name="Calibri", size=11)
TITLE = Font(name="Calibri", size=13, bold=True, color="1F4E3D")
FILL = PatternFill("solid", fgColor="E2EFDA")


def r100(v):
    return int(round(v / 100.0)) * 100


def r1000(v):
    return int(round(v / 1000.0)) * 1000


def figures(target):
    G = calc.golden(target)
    nets = calc.nets_needed(target)
    cases = calc.reported_cases(target)
    bu = calc.averted_with(G, 1.0)
    F = {
        "call_cases_averted": r1000(G["total"]),
        "call_share_of_expected_pct": int(round(100 * G["share"])),
        "component_per_bite_protection": round(G["q"], 2),
        "component_in_bed_share": round(G["phi"], 2),
        "step_trial_pooled_efficacy_pct": round(100 * G["pooled"], 1),
        "step_expected_cases": int(G["base_total"]),
        "rival_trial_efficacy_cases_averted": r1000(bu * G["pooled"]),
    }
    for sc in C.SC_CODES:
        F["call_cases_averted_%s" % sc] = r100(G["by_sc"][sc])
    for sc in C.SC_CODES:
        F["ask_nets_%s" % sc] = nets[sc]
    for sc in C.SC_CODES:
        F["ask_reported_cases_2026_%s" % sc] = cases[sc]
    return F, G, nets, cases


def _w(ws, r, c, v, font=BODY, fmt=None):
    cell = ws.cell(row=r, column=c, value=v)
    cell.font = font
    if fmt:
        cell.number_format = fmt
    return cell


def write_xlsx(out, F, G, nets, cases):
    wb = Workbook()
    ws = wb.active
    ws.title = "Cases averted"
    _w(ws, 1, 1, "LulaNet R will avert about %s Ombeni fever cases among net users, April to December 2027"
       % "{:,}".format(F["call_cases_averted"]), TITLE)
    _w(ws, 2, 1, "Tulivu Health Partners M&E, for the Arnbridge Foundation grant review. Planning baseline run of "
                 "14 September 2026; use as planned in the operational plan v2.1.")
    _w(ws, 4, 1, "County", BOLD)
    _w(ws, 5, 1, "Cases averted (nearest 1,000)")
    _w(ws, 5, 2, F["call_cases_averted"], BOLD, "#,##0")
    _w(ws, 6, 1, "Share of expected cases, April to December 2027")
    _w(ws, 6, 2, F["call_share_of_expected_pct"] / 100, BOLD, "0%")
    _w(ws, 7, 1, "Expected cases without the campaign")
    _w(ws, 7, 2, F["step_expected_cases"], fmt="#,##0")
    head = ["Sub-county", "Expected cases", "Cases averted (nearest 100)", "Nets to distribute",
            "Confirmed cases reported, Jan to Sep 2026"]
    for j, h in enumerate(head):
        c = _w(ws, 9, j + 1, h, BOLD)
        c.fill = FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, sc in enumerate(C.SC_CODES):
        r = 10 + i
        _w(ws, r, 1, C.SC_NAME[sc])
        _w(ws, r, 2, sum(G["base"][(sc, m)] for (_, m) in C.WINDOW), fmt="#,##0")
        _w(ws, r, 3, F["call_cases_averted_%s" % sc], fmt="#,##0")
        _w(ws, r, 4, F["ask_nets_%s" % sc], fmt="#,##0")
        _w(ws, r, 5, F["ask_reported_cases_2026_%s" % sc], fmt="#,##0")
    r = 10 + len(C.SC_CODES)
    _w(ws, r, 1, "County", BOLD)
    _w(ws, r, 2, F["step_expected_cases"], BOLD, "#,##0")
    _w(ws, r, 4, sum(nets.values()), BOLD, "#,##0")
    _w(ws, r, 5, sum(cases.values()), BOLD, "#,##0")
    _w(ws, r + 2, 1, "Sub-county figures are rounded on their own and need not add to the county figure. Sub-counties "
                     "as realigned on 1 July 2026.")
    for j, wdt in enumerate([34, 16, 18, 18, 22]):
        ws.column_dimensions[get_column_letter(j + 1)].width = wdt
    ws.row_dimensions[9].height = 45
    ws.freeze_panes = "B10"
    ws.print_title_rows = "9:9"
    ws.page_setup.orientation = "landscape"

    m = wb.create_sheet("Protection")
    _w(m, 1, 1, "How much of a resident's exposure the nets reach", TITLE)
    _w(m, 3, 1, "Per-bite protection for a sleeper under the net, from the five KINGA-5 sites")
    _w(m, 3, 2, F["component_per_bite_protection"], BOLD, "0.00")
    _w(m, 4, 1, "Share of a Ruvari resident's bites that arrive while in bed (catches 2024 to 2026, survey 2025)")
    _w(m, 4, 2, F["component_in_bed_share"], BOLD, "0.00")
    _w(m, 5, 1, "KINGA-5 pooled protective efficacy (not the county's)")
    _w(m, 5, 2, F["step_trial_pooled_efficacy_pct"] / 100, fmt="0.0%")
    hd = ["Site", "Protective efficacy", "Share of bites in bed", "Efficacy per unit of in-bed share"]
    for j, h in enumerate(hd):
        c = _w(m, 7, j + 1, h, BOLD)
        c.fill = FILL
    for i, s in enumerate(G["sites"]):
        _w(m, 8 + i, 1, s["site"])
        _w(m, 8 + i, 2, round(s["E"], 3), fmt="0.0%")
        _w(m, 8 + i, 3, round(s["share"], 3), fmt="0.00")
        _w(m, 8 + i, 4, round(s["E"] / s["share"], 3), fmt="0.00")
    hr = 15
    for j, h in enumerate(["Hour", "Bites per hour indoors", "Bites per hour outdoors", "Residents indoors", "Residents in bed"]):
        c = _w(m, hr, j + 1, h, BOLD)
        c.fill = FILL
    labels = ["18:00", "19:00", "20:00", "21:00", "22:00", "23:00", "00:00", "01:00", "02:00", "03:00", "04:00", "05:00"]
    for h in range(12):
        _w(m, hr + 1 + h, 1, labels[h])
        _w(m, hr + 1 + h, 2, round(60 * float(G["b_in"][h]), 2), fmt="0.00")
        _w(m, hr + 1 + h, 3, round(60 * float(G["b_out"][h]), 2), fmt="0.00")
        _w(m, hr + 1 + h, 4, round(float(G["ind"][h]), 3), fmt="0%")
        _w(m, hr + 1 + h, 5, round(float(G["inb"][h]), 3), fmt="0%")
    for j, wdt in enumerate([70, 18, 20, 22, 18]):
        m.column_dimensions[get_column_letter(j + 1)].width = wdt
    n = wb.create_sheet("Notes")
    notes = [
        ("As of", "Files pulled 12 October 2026; planning baseline run of 14 September 2026."),
        ("Population", "Residents sleeping under a campaign net, at the planned use in Table 2 of the operational plan; "
                       "no cases are counted for residents who are not under a campaign net (plan section 5)."),
        ("Window", "April to December 2027."),
        ("Protection", "KINGA-5 site efficacies (final report, Table 1) against each site's share of bites arriving "
                       "in bed (Tables 2a to 3b); the county's share from the sentinel catches January 2024 to "
                       "September 2026 (An. ruvariensis, landings per minute collected) and both rounds of the 2025 "
                       "behaviour survey, read at the half hour."),
        ("Nets", "One net for every two usual members, rounded up, at most four a household (plan section 3); sync "
                 "replays counted once; mop-up registrations that repeat a main-round household's ward, dwelling "
                 "mark, usual members, under-fives and sleeping spaces counted once."),
        ("Reported cases", "MOH 705 confirmed Ombeni fever, all ages, January to September 2026, by the facility's "
                           "sub-county in the master facility list; the re-entered June 2026 Lwala ward returns "
                           "counted once; the sub-county hospitals' January to March 2026 returns net of their "
                           "outreach clinics, which reported under their own codes from January 2026."),
        ("Rounding", "County cases averted to the nearest 1,000, sub-counties to the nearest 100, each from unrounded "
                     "figures; the share to a whole per cent."),
    ]
    for i, (k, v) in enumerate(notes):
        _w(n, 1 + i, 1, k, BOLD)
        c = _w(n, 1 + i, 2, v)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        n.row_dimensions[1 + i].height = 15 * (1 + len(v) // 95)
    n.column_dimensions["A"].width = 16
    n.column_dimensions["B"].width = 100
    path = os.path.join(out, F_XLSX)
    wb.save(path)
    PP.normalize_ooxml(path, C.PEOPLE["me"], C.PEOPLE["me"], "2026-10-14T05:20:00Z", "2026-10-16T13:05:00Z",
                       excel=True, company=C.ORG)


def write_png(out, F):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker
    plt.rcParams["svg.hashsalt"] = "task170"
    names = [C.SC_NAME[sc] for sc in C.SC_CODES]
    vals = [F["call_cases_averted_%s" % sc] for sc in C.SC_CODES]
    fig, ax = plt.subplots(figsize=(7.6, 4.2), dpi=120)
    bars = ax.bar(names, vals, color="#2e6b4f", width=0.62)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 25, "{:,}".format(v), ha="center", va="bottom", fontsize=9)
    ax.set_ylabel("Cases averted among net users (nearest 100)")
    ax.set_title("LulaNet R averts about %s Ombeni fever cases among net users, April to December 2027"
                 % "{:,}".format(F["call_cases_averted"]), fontsize=10.5, loc="left")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: "{:,.0f}".format(v)))
    fig.text(0.01, 0.01, "Sub-counties as realigned 1 July 2026. Source: KINGA-5 final report; county sentinel catches "
             "2024 to 2026; behaviour survey 2025; planning baseline 2027.", fontsize=7, color="#5b6169")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(0, max(vals) * 1.15)
    plt.xticks(fontsize=9)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(os.path.join(out, F_PNG), metadata={"Software": None})
    plt.close(fig)


def submission(F):
    sc_lines = "\n".join("   - %s: %s" % (C.SC_NAME[sc], "{:,}".format(F["call_cases_averted_%s" % sc])) for sc in C.SC_CODES)
    nets_lines = "\n".join("   - %s: %s" % (C.SC_NAME[sc], "{:,}".format(F["ask_nets_%s" % sc])) for sc in C.SC_CODES)
    case_lines = "\n".join("   - %s: %s" % (C.SC_NAME[sc], "{:,}".format(F["ask_reported_cases_2026_%s" % sc])) for sc in C.SC_CODES)
    return f"""## Tags

**Domain:** Epidemiology and public health (health burden and impact modelling).
**Analytical objective:** Forecasting and predictive modelling.

## 1. Final Recommendation

**The March 2027 LulaNet R campaign will avert about {F['call_cases_averted']:,} Ombeni fever cases among the people sleeping under its nets in Ruvari County from April to December 2027, {F['call_share_of_expected_pct']} per cent of the {F['step_expected_cases']:,} the county expects.**
It rests on a per-bite protection of {F['component_per_bite_protection']:.2f} against the {F['component_in_bed_share']:.2f} of a resident's bites that arrive in bed. Not the trial's pooled {F['step_trial_pooled_efficacy_pct']:.1f} per cent efficacy (about {F['rival_trial_efficacy_cases_averted']:,} cases averted), which was measured where most bites arrived after people were in bed.

## 2. Critical Components

1. The per-bite protection the five KINGA-5 sites share is **{F['component_per_bite_protection']:.2f}**.
2. The share of a Ruvari resident's exposure that arrives in bed is **{F['component_in_bed_share']:.2f}**.

## 3. Step-by-Step Solution

1. Read each KINGA-5 site's protective efficacy from Table 1 of kinga5_final_report_2024.pdf (pooled {F['step_trial_pooled_efficacy_pct']:.1f} per cent) and its share of bites in bed from Tables 2a to 3b (bites indoors at each hour times members in bed, over bites indoors times members indoors plus bites outdoors times members outdoors).
2. Fitted each site's efficacy as a multiple of its in-bed share through the origin, weighted by the inverse variance of the site's efficacy: a per-bite protection of {F['component_per_bite_protection']:.2f}.
3. Built the county's An. ruvariensis landings per minute collected by hour and position from hlc_sentinel_2024_2026.csv (re-keyed sheets counted once, rows with no catch dropped).
4. Read members indoors and in bed at each half hour from both rounds of human_behaviour_survey_2025.xlsx, and computed the county's in-bed share the same way as the sites': {F['component_in_bed_share']:.2f}.
5. Multiplied each sub-county's expected cases by month in obf_planning_baseline_2027.xlsx by the planned use in Table 2 of lulanet_r_distribution_plan_2027.docx and by the per-bite protection times the in-bed share: {F['call_cases_averted']:,} cases averted, {F['call_share_of_expected_pct']} per cent of {F['step_expected_cases']:,}.
6. Nets from nets_registration_2026.parquet under the plan's allocation rule, with replayed records counted once and each mop-up registration matching a main-round household on its ward, dwelling mark, usual members, under-fives and sleeping spaces counted as that household.
7. Confirmed cases January to September 2026 from khis_moh705_obf_2024_2026.csv by each facility's sub-county in facility_list_2026.csv, the June 2026 re-entry of the realigned ward's returns counted once, and the parent hospitals' January to March 2026 returns marked as including outreach net of their outreach clinics' own returns.
8. The campaign will avert about {F['call_cases_averted']:,} Ombeni fever cases among net users from April to December 2027.

## 4. Deliverable Answers

### ruvari_cases_averted_2027.xlsx

1. Cases averted among net users, April to December 2027, county: {F['call_cases_averted']:,}
2. Share of the county's expected cases in the period: {F['call_share_of_expected_pct']} per cent
3. Cases averted by sub-county, to the nearest hundred:
{sc_lines}
4. Nets the campaign will hand out by sub-county:
{nets_lines}
5. Confirmed Ombeni fever cases reported by each sub-county's facilities, January to September 2026:
{case_lines}

### cases_averted_by_subcounty.png

1. One bar per sub-county, labelled with its cases averted to the nearest hundred, the county figure in the title.
"""


def deliver(target, golden_dir, figures_path, submission_path):
    os.makedirs(golden_dir, exist_ok=True)
    F, G, nets, cases = figures(target)
    write_xlsx(golden_dir, F, G, nets, cases)
    write_png(golden_dir, F)
    with open(figures_path, "w") as fh:
        json.dump(F, fh, indent=1, sort_keys=False)
        fh.write("\n")
    open(submission_path, "w").write(submission(F))
    return F, G
