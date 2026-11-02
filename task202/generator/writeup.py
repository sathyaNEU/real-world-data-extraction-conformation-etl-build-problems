"""The goldens, submission.md, generator/figures.json and metadata.json, every figure carried from golden.py."""
import datetime as dt
import io
import json
import math
import os

import golden as G
import postprocess as PP
import world as W

NAMES = {"A": "Lenning farm infrastructure programme", "B": "Brathwick WwTW chemical phosphorus removal",
         "C": "Hollinsby WwTW tertiary filtration", "D": "Mill Beck outfall treatment wetland"}


def r0(x):
    return int(math.floor(x + 0.5))


def r1(x):
    return math.floor(x * 10 + 0.5) / 10.0


def fmt_int(n):
    return "{:,}".format(n)


def emitted(F, T):
    """The figures as every block and golden states them."""
    ins = G.insertion(T)
    E = {"call": "C", "runner_up": "D"}
    for y in W.SEASONS:
        for k in "ABCD":
            v = F.get("%s_%d" % (k, y), 0.0) if k != "A" else 0.0
            E["%s_%d" % (k, y)] = r0(v)
        E["dense_%d" % y] = ins[y]["dense"]
        E["days_%d" % y] = ins[y]["n"]
    for k in "ABCD":
        E["%s_mean" % k] = r0(F["%s_mean" % k])
    E["gap"] = E["C_mean"] - E["D_mean"]
    E["inflow_2023_24"] = r1(F["inflow_2023_24"])
    E["load_2023_24"] = int(math.floor(F["load_2023_24"] / 100.0 + 0.5)) * 100
    for y in (2025, 2026):
        E["tp_%d" % y] = r1(F["tp_%d" % y])
        E["chl_%d" % y] = r1(F["chl_%d" % y])
    for k in ("dw_found", "dw_fixed", "dw_open"):
        E[k] = int(F[k])
    E["credit_C"] = 71
    E["credit_D"] = 50
    return E


# ----------------------------------------------------------------------------------------------- chart
def chart_png(E):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6.8, 3.3), dpi=150)
    cols = ["#9bb7d4", "#4f7fb0", "#1f4e79"]
    x = range(4)
    w = 0.25
    for j, y in enumerate(W.SEASONS):
        vals = [E["%s_%d" % (k, y)] for k in "ABCD"]
        bars = ax.bar([i + (j - 1) * w for i in x], vals, w, label=str(y), color=cols[j])
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 3, str(v), ha="center", va="bottom", fontsize=6.5)
    ax.set_xticks(list(x))
    ax.set_xticklabels(["A  farms", "B  Brathwick works", "C  Hollinsby works", "D  Mill Beck wetland"], fontsize=7.5)
    ax.set_ylabel("kg phosphorus kept out of the\nsurface water, June to September", fontsize=7.5)
    ax.tick_params(axis="y", labelsize=7)
    ax.set_ylim(0, max(E["C_2024"], E["C_2025"], E["C_2026"]) * 1.27)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(fontsize=7, frameon=False, ncol=3, loc="upper left")
    ax.annotate("recommended", xy=(2, max(E["C_2024"], E["C_2025"], E["C_2026"]) * 1.13), ha="center", fontsize=7, color="#1f4e79", fontweight="bold")
    ax.set_title("Only the Hollinsby and Mill Beck programmes keep phosphorus out of the surface water in summer",
                 fontsize=8.5)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


# ----------------------------------------------------------------------------------------------- memo
def memo_pdf(path, E, ins_rows):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    from reportlab.lib import colors
    st = ParagraphStyle("b", fontName="Helvetica", fontSize=9.4, leading=13, spaceAfter=5)
    h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=6)
    h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10, leading=13, spaceBefore=6, spaceAfter=3)
    sm = ParagraphStyle("s", fontName="Helvetica", fontSize=8, leading=10, textColor=colors.HexColor("#444444"))
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=16 * mm,
                            bottomMargin=16 * mm, title="Selwith Recovery Fund 2027: recommendation to trustees",
                            author="Debra Rose", subject="", creator="")
    png = chart_png(E)
    flow = [
        Paragraph("Selwith Water Trust  |  Paper for the trustees' meeting of 26 November 2026  |  Item 4  |  "
                  "Debra Rose, catchment programme manager, 12 November 2026", sm),
        Paragraph("Recovery Fund 2027: the Hollinsby tertiary filter keeps the most phosphorus out of the bloom water", h1),
        Paragraph("<b>Recommendation: back programme C, tertiary filtration at the Hollinsby works. Under the fund's "
                  "rules it keeps %d kg of phosphorus a season out of the lake's surface water. The runner-up is "
                  "programme D, the Mill Beck outfall wetland, at %d kg.</b>" % (E["C_mean"], E["D_mean"]), st),
        Paragraph("Programmes A (Lenning farms) and B (Brathwick works) both act on phosphorus carried by the River "
                  "Lenning, and the Lenning does not reach the surface water in summer. It is spring-fed and runs "
                  "colder than the lake's top 5 m on every day from June to September, so its water sinks below the "
                  "thermocline when it enters the lake. That held on %d of %d days in 2024, %d of %d in 2025 and "
                  "%d of %d in 2026 (river daily mean against the buoy's 0 to 5 m mean). The buoy's 10 m conductivity "
                  "rises through each summer with the river's water while the 1 m and 5 m readings stay level. "
                  "Brathwick's effluent and the farms' runoff therefore add nothing to the surface water before the "
                  "October overturn, and neither programme keeps any phosphorus out of it in the bloom season."
                  % (E["dense_2024"], E["days_2024"], E["dense_2025"], E["days_2025"], E["dense_2026"], E["days_2026"]), st),
        Paragraph("Hollinsby's effluent is warmer than the surface water in every month from June to September, so it "
                  "spreads in the water the blooms grow in. Applying the appraisal's credited reduction (71%%) to the "
                  "works' June-to-September loads in Fellmoor Water's returns gives %d, %d and %d kg for 2024 to 2026."
                  % (E["C_2024"], E["C_2025"], E["C_2026"]), st),
        Spacer(1, 4),
        Image(io.BytesIO(png), width=170 * mm, height=82.5 * mm),
        Spacer(1, 4),
        Paragraph("Figures by programme (kg a season, June to September)", h2),
    ]
    rows = [["Programme", "2024", "2025", "2026", "Average"]]
    for k in "ABCD":
        rows.append(["%s  %s" % (k, NAMES[k])] + [str(E["%s_%d" % (k, y)]) for y in W.SEASONS] + [str(E["%s_mean" % k])])
    t = Table(rows, hAlign="LEFT", colWidths=[86 * mm, 18 * mm, 18 * mm, 18 * mm, 20 * mm])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.6), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.6),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black), ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                           ("FONT", (0, 3), (-1, 3), "Helvetica-Bold", 8.6)]))
    flow += [t, Spacer(1, 3),
             Paragraph("Sources: Fellmoor Water monthly returns to September 2026; Lenning Foot station; Fellside buoy; "
                       "the trust's Mill Beck outfall monitoring; programme_appraisals_2027.xlsx.", sm),
             Spacer(1, 6),
             Paragraph("The farm programme would still cut what the Lenning delivers to the deep water and to the lake "
                       "after the overturn, and the trust should keep it on the list for the next round. It does not "
                       "change which programme does most for the 2027 blooms.", st),
             Paragraph("Workings, the 2023-24 winter inflow, the north basin results and the Connect Right tally are in "
                       "selwith_phosphorus_workings.xlsx.", sm),
             Spacer(1, 4),
             Paragraph("Note: figures follow the fund's rules 2.1 to 2.3, the appraisal's credited reduction applied to "
                       "what each source added to the 0 to 5 m surface water between 1 June and 30 September, the three "
                       "seasons averaged before rounding to the kilogram.", sm)]

    def _meta(c, d):
        c.setProducer("Microsoft\xae Word for Microsoft 365")
        c.setCreator("Microsoft\xae Word for Microsoft 365")
    doc.build(flow, onFirstPage=_meta, onLaterPages=_meta)
    PP.normalize_pdf(path, b"D:20261112151800+00'00'", b"D:20261112151800+00'00'")


# ----------------------------------------------------------------------------------------------- workbook
def workbook(path, E, F):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Programmes"
    ws.append(["Phosphorus kept out of the lake's surface water, June to September (kg)"])
    ws.append([])
    ws.append(["Programme", "Title", "2024", "2025", "2026", "Average", "Credited reduction (%)"])
    credits = {"A": 30, "B": 82, "C": 71, "D": 50}
    for k in "ABCD":
        ws.append([k, NAMES[k]] + [E["%s_%d" % (k, y)] for y in W.SEASONS] + [E["%s_mean" % k], credits[k]])
    ws.append([])
    ws.append(["Recommended", "C", None, None, None, E["C_mean"]])
    ws.append(["Runner-up", "D", None, None, None, E["D_mean"]])
    for c in ws[3]:
        c.font = Font(bold=True)
    ws["A1"].font = Font(bold=True, size=12)
    ws.freeze_panes = "A4"
    for col, w in zip("ABCDEFG", (11, 46, 8, 8, 8, 9, 22)):
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=4, max_row=9, min_col=3, max_col=7):
        for c in row:
            c.number_format = "#,##0"
    ws2 = wb.create_sheet("Lenning in summer")
    ws2.append(["Season", "Days the Lenning was denser than the 0-5 m water", "Days compared"])
    for y in W.SEASONS:
        ws2.append([y, E["dense_%d" % y], E["days_%d" % y]])
    for c in ws2[1]:
        c.font = Font(bold=True)
    ws2.column_dimensions["A"].width = 9
    ws2.column_dimensions["B"].width = 46
    ws2.column_dimensions["C"].width = 15
    ws3 = wb.create_sheet("Winter 2023-24")
    ws3.append(["River Lenning into the lake, 1 October 2023 to 30 April 2024"])
    ws3.append(["Inflow (million m3)", E["inflow_2023_24"]])
    ws3.append(["Phosphorus load (kg, nearest 100)", E["load_2023_24"]])
    ws3["A1"].font = Font(bold=True)
    ws3["B2"].number_format = "0.0"
    ws3["B3"].number_format = "#,##0"
    ws3.column_dimensions["A"].width = 34
    ws3.append([])
    ws3.append(["Station flow to 31 May 2024 is the Lenning Bridge feed; Brankell Beck at Howe added hour by hour."])
    ws4 = wb.create_sheet("North basin")
    ws4.append(["North basin surface water (0-5 m), June to September mean", "Total phosphorus (ug/l)", "Chlorophyll a (ug/l)"])
    for y in (2025, 2026):
        ws4.append([y, E["tp_%d" % y], E["chl_%d" % y]])
    for c in ws4[1]:
        c.font = Font(bold=True)
    for row in ws4.iter_rows(min_row=2, max_row=3, min_col=2, max_col=3):
        for c in row:
            c.number_format = "0.0"
    ws4.column_dimensions["A"].width = 56
    ws4.column_dimensions["B"].width = 22
    ws4.column_dimensions["C"].width = 20
    ws4.append([])
    ws4.append(["North basin site: NB to March 2025, SWL01 from April 2025 (NB now the Hollinsby Bay site)."])
    ws5 = wb.create_sheet("Connect Right")
    ws5.append(["Dwellings draining foul water to the surface-water drains", "Dwellings"])
    ws5.append(["Found by the survey", E["dw_found"]])
    ws5.append(["Confirmed fixed by 30 September 2026", E["dw_fixed"]])
    ws5.append(["Not fixed", E["dw_open"]])
    ws5["A1"].font = Font(bold=True)
    ws5.column_dimensions["A"].width = 56
    ws5.append([])
    ws5.append(["Flats on a block's shared stack counted one dwelling each; visits dated by their visit reference."])
    ws6 = wb.create_sheet("Notes")
    ws6.append(["Measure", "Fund rules 2.1 to 2.3: the appraisal's credited reduction applied to what each source added to "
                "the 0 to 5 m surface water, 1 June to 30 September, averaged over 2024 to 2026."])
    ws6.append(["Data to", "30 September 2026"])
    ws6.append(["Rounding", "Kilograms whole after averaging; the winter load to the nearest 100 kg; concentrations to one decimal."])
    ws6.column_dimensions["A"].width = 12
    ws6.column_dimensions["B"].width = 110
    for c in ws6["A"]:
        c.font = Font(bold=True)
    wb.save(path)
    PP.normalize_ooxml(path, "Debra Rose", "Debra Rose", "2026-11-11T09:05:00Z", "2026-11-12T15:02:00Z",
                       excel=True, company="Selwith Water Trust")


# ----------------------------------------------------------------------------------------------- submission
def submission(E):
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Physical and environmental sciences (pollution source attribution).")
    L.append("**Analytical objective:** Root-cause analysis.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Back programme C, tertiary filtration at the Hollinsby works: it keeps %d kg of phosphorus a season out of "
             "Selwith Water's surface water, %d kg more than the runner-up, programme D (the Mill Beck wetland, %d kg).** "
             "Not programme B at the Brathwick works, which carries the largest June-to-September load into the lake, nor "
             "programme A on the farms: both act on the River Lenning, which is denser than the surface water on every "
             "summer day and enters below the thermocline, so neither keeps any phosphorus out of the surface water.\n"
             % (E["C_mean"], E["gap"], E["D_mean"]))
    L.append("## 2. Critical Components\n")
    L.append("1. The Lenning's daily mean water was denser than the buoy's 0 to 5 m water on **%d of %d**, **%d of %d** "
             "and **%d of %d** June-to-September days in 2024, 2025 and 2026, so programmes A and B keep out **0 kg**."
             % (E["dense_2024"], E["days_2024"], E["dense_2025"], E["days_2025"], E["dense_2026"], E["days_2026"]))
    L.append("2. Hollinsby's effluent is warmer than the surface water in every season month, and programme C keeps out "
             "**%d**, **%d** and **%d kg** (2024 to 2026), **%d kg** on average." % (E["C_2024"], E["C_2025"], E["C_2026"], E["C_mean"]))
    L.append("3. Programme D keeps out **%d**, **%d** and **%d kg**, **%d kg** on average.\n"
             % (E["D_2024"], E["D_2025"], E["D_2026"], E["D_mean"]))
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Read lenning_foot_hourly_validated.csv over lenning_foot_hourly_provisional.csv where both hold an hour, "
             "moved the UK clock readings to UTC and took each day's mean water temperature.")
    L.append("2. Averaged the sensors down to 5 m in fellside_buoy_thermistor_daily.csv each day and compared water densities "
             "at the two temperatures: the river was denser on every June-to-September day, sinking below the thermocline, "
             "where fellside_buoy_sondes_daily.csv shows the 10 m conductivity rising through each summer.")
    L.append("3. Compared Hollinsby's monthly effluent temperature in fellmoor_wwtw_monthly_returns.xlsx with the surface "
             "water's monthly mean: warmer in every month June to September.")
    L.append("4. Applied the credited reductions in programme_appraisals_2027.xlsx (C 71%%, D 50%%) to Hollinsby's June-to-"
             "September TP loads in the returns and to the Mill Beck monthly loads, and averaged the seasons: C %d kg, D %d kg."
             % (E["C_mean"], E["D_mean"]))
    L.append("5. For 1 October 2023 to 30 April 2024 added the Brankell Beck at Howe hourly flow from regulator_gauged_flows_hourly.csv "
             "to the station's flow (the Lenning Bridge feed until 1 June 2024, above the Brankell Beck's confluence), and "
             "multiplied each hour's flow by the bottle that took its sub-sample, the storm bottles for the hours a day "
             "bottle's sub-sample count shows it skipped: %.1f million m3 and %s kg." % (E["inflow_2023_24"], fmt_int(E["load_2023_24"])))
    L.append("6. Took the north basin's 0-5 m results in fellside_lake_lab_results.csv under NB until 31 March 2025 and "
             "SWL01 from 1 April 2025 (NB then holds the Hollinsby Bay samples, with no 20 m bottle) and averaged June to September.")
    L.append("7. Counted each block's shared-stack visit in connect_right_visits_export.csv as every flat under that UPRN in "
             "hollinsby_address_register_extract.csv and dated each visit by its visit reference: %d found, %d fixed by "
             "30 September 2026, %d not." % (E["dw_found"], E["dw_fixed"], E["dw_open"]))
    L.append("8. Ranked the programmes on the fund's measure: C first, D second.\n")
    L.append("## 4. Deliverable Answers\n")
    L.append("### selwith_fund_recommendation_2027.pdf\n")
    L.append("1. Programme C, Hollinsby WwTW tertiary filtration: %d kg of phosphorus a season." % E["C_mean"])
    L.append("2. Runner-up: programme D, Mill Beck outfall treatment wetland, %d kg." % E["D_mean"])
    L.append("3. Bar chart of every programme's figure for 2024, 2025 and 2026 on page 1.\n")
    L.append("### selwith_phosphorus_workings.xlsx\n")
    L.append("1. Each programme's figure for 2024, 2025 and 2026 (kg):")
    for k in "ABCD":
        L.append("   - %s: %d, %d, %d" % (k, E["%s_2024" % k], E["%s_2025" % k], E["%s_2026" % k]))
    L.append("2. River Lenning into the lake, October 2023 to April 2024: inflow %.1f million m3, phosphorus load %s kg."
             % (E["inflow_2023_24"], fmt_int(E["load_2023_24"])))
    L.append("3. North basin June-to-September mean surface water: 2025 total phosphorus %.1f ug/l and chlorophyll a %.1f ug/l; "
             "2026 total phosphorus %.1f ug/l and chlorophyll a %.1f ug/l." % (E["tp_2025"], E["chl_2025"], E["tp_2026"], E["chl_2026"]))
    L.append("4. Connect Right: %d dwellings found draining foul water to the surface-water drains, %d confirmed fixed by "
             "30 September 2026, %d not." % (E["dw_found"], E["dw_fixed"], E["dw_open"]))
    return "\n".join(L) + "\n"


def metadata(T):
    files = sorted(os.listdir(T))
    prov = {}
    src = "synthetic, generated by task202/generator from seed 202 (an invented lake, catchment and organisations)"
    for f in files:
        prov["target/" + f] = dict(source=src, date="2026-11-09", licence="CC BY 4.0")
    return {
        "task": "task202",
        "decision": "which shortlisted phosphorus programme the Selwith Recovery Fund backs for the 2027 bloom season",
        "deliverables": ["selwith_fund_recommendation_2027.pdf", "selwith_phosphorus_workings.xlsx"],
        "distractor_files": ["target/hollinsby_beach_bathing_results.csv", "target/lenning_farm_yard_survey_2025.xlsx"],
        "files": prov,
    }


def write_all(TASK, T, S, F):
    E = emitted(F, T)
    gold = os.path.join(TASK, "golden")
    if os.path.isdir(gold):
        for f in os.listdir(gold):
            os.remove(os.path.join(gold, f))
    os.makedirs(gold, exist_ok=True)
    memo_pdf(os.path.join(gold, "selwith_fund_recommendation_2027.pdf"), E, None)
    workbook(os.path.join(gold, "selwith_phosphorus_workings.xlsx"), E, F)
    with open(os.path.join(TASK, "submission.md"), "w") as f:
        f.write(submission(E))
    with open(os.path.join(TASK, "generator", "figures.json"), "w") as f:
        json.dump(E, f, indent=1, sort_keys=True)
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(metadata(T), f, indent=1)
    return E
