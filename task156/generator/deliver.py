"""The golden deliverables, figures.json and submission.md, every figure computed from target/ by estim.py and asks.py.

    deliver.main(target, golden_dir, figures_path, submission_path)"""
from __future__ import annotations

import io
import json
import os

import numpy as np

import asks as AK
import estim as E
import postprocess as PP

F_XLSX = "ps03_ngaio_road_connection_2027.xlsx"
F_DOCX = "council_report_ngaio_road_2027.docx"
F_PNG = "replay_overflows_2004-2023.png"


def rnd(x):
    return int(np.floor(x + 0.5))


def compute(target):
    G = E.golden(target)
    V = E.validation(target)
    A = AK.ask_a(target)
    B = AK.ask_b(target)
    X = dict(G=G, V=V, A=A, B=B)
    M = G["model"]
    X["fig"] = dict(
        existing=rnd(G["existing"]["mean"]), with_sub=rnd(G["with_sub"]["mean"]), upgrade=rnd(G["with_upgrade"]["mean"]),
        existing_exact=G["existing"]["mean"], with_sub_exact=G["with_sub"]["mean"], upgrade_exact=G["with_upgrade"]["mean"],
        naive=rnd(G["naive_sub"]["mean"]), naive_exact=G["naive_sub"]["mean"], g=round(M["g"], 1), a=rnd(M["a"]),
        b=round(M["b"], 1), ls_meter_med=round(G["lsub_meter_median"], 1), ls_replay_med=round(G["lsub_replay_median"], 1),
        ls_max=rnd(G["lsub_meter_max"]), v_cond=round(V[("conditioned", "high river weeks", "bias")], 1) + 0.0,
        v_single=rnd(V[("single", "high river weeks", "bias")]),
        v_cond26=abs(round(V[("conditioned", "2026", "bias")], 1)) + 0.0,
        v_single26=round(V[("single", "2026", "bias")], 1) + 0.0,
        total_ex=int(G["existing"]["per_year"].sum()), total_sub=int(G["with_sub"]["per_year"].sum()),
        total_up=int(G["with_upgrade"]["per_year"].sum()), meter_logged=sum(G["existing"]["meter"]))
    X["a"] = {k: rnd(v) for k, v in A.items()}
    X["b"] = {k: rnd(v) for k, v in B.items()}
    return X


# ---------------------------------------------------------------------------------------------------- workbook
def write_xlsx(path, X):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    f = X["fig"]
    G = X["G"]
    wb = Workbook()
    bold = Font(bold=True)
    head = PatternFill("solid", fgColor="DDE4EA")
    title = Font(bold=True, size=13)

    def header(ws, row, cols, widths=None):
        for i, c in enumerate(cols, start=1):
            cell = ws.cell(row=row, column=i, value=c)
            cell.font = bold
            cell.fill = head
            cell.alignment = Alignment(wrap_text=True, vertical="top")
        if widths:
            for i, w in enumerate(widths):
                ws.column_dimensions[chr(65 + i)].width = w

    ws = wb.active
    ws.title = "Recommendation"
    ws["A1"] = "PS03 would overflow about %d times a year with Ngaio Road connected: hold the connection to the 2029 upgrade" % f["with_sub"]
    ws["A1"].font = title
    ws["A2"] = "Consent AUTH-2024-0418 conditions 6 to 8: wet weather overflows at EO-03, the 2004 to 2023 hourly record replayed each day as it occurred"
    header(ws, 4, ["Case", "Overflows in the 20 years", "Average a year", "Average a year (whole)", "Limit (condition 6)"],
           [46, 16, 14, 14, 14])
    rows = [("PS03 catchment as connected now", f["total_ex"], f["existing_exact"], f["existing"]),
            ("With Ngaio Road at full development (260 dwellings)", f["total_sub"], f["with_sub_exact"], f["with_sub"]),
            ("With Ngaio Road, after the 1,100 m3 storage upgrade", f["total_up"], f["upgrade_exact"], f["upgrade"])]
    for i, (c, t, m, w) in enumerate(rows, start=5):
        ws.cell(row=i, column=1, value=c)
        ws.cell(row=i, column=2, value=t)
        ws.cell(row=i, column=3, value=m).number_format = "0.00"
        ws.cell(row=i, column=4, value=w)
        ws.cell(row=i, column=5, value=2)
    ws["A9"] = "Recommendation: hold the Ngaio Road connection until the PS03 storage upgrade is commissioned (programme: June 2029)."
    ws["A9"].font = bold
    ws["A10"] = ("For comparison, one response per millimetre of rain fitted on the 2024 to 2026 meter, with the meter's own dry "
                 "weather flow, gives %.2f a year with the subdivision; it misses the June 2025 high-river weeks by %d L/s "
                 "on average when they are held out." % (f["naive_exact"], f["v_single"]))
    ws["A11"] = "Pumping capacity 112.0 L/s (2023 drawdown test) and 350 m3 to the weir crest (station data sheet, rev 4)."

    ws2 = wb.create_sheet("Replay by year")
    ws2["A1"] = "Overflows concentrate in the years the terrace water table stood high (2008, 2011, 2017)"
    ws2["A1"].font = title
    header(ws2, 3, ["Year", "As connected now", "With Ngaio Road", "With Ngaio Road and the upgrade"], [10, 18, 18, 30])
    for i, y in enumerate(range(2004, 2024)):
        ws2.cell(row=4 + i, column=1, value=y)
        ws2.cell(row=4 + i, column=2, value=int(G["existing"]["per_year"][i]))
        ws2.cell(row=4 + i, column=3, value=int(G["with_sub"]["per_year"][i]))
        ws2.cell(row=4 + i, column=4, value=int(G["with_upgrade"]["per_year"][i]))
    ws2.cell(row=24, column=1, value="Total").font = bold
    for c, k in ((2, "total_ex"), (3, "total_sub"), (4, "total_up")):
        ws2.cell(row=24, column=c, value=f[k]).font = bold

    ws3 = wb.create_sheet("Inflow model")
    ws3["A1"] = "Infiltration runs with the sewer length below the water table, which the meter years kept short"
    ws3["A1"].font = title
    header(ws3, 3, ["Quantity", "Value", "Unit"], [64, 12, 26])
    M = G["model"]
    items = [
        ("Infiltration for each km of PS03 sewer below the water table", f["g"], "L/s per km"),
        ("Fast response to rain (triangle, %g h to peak, %d h base)" % M["sf"], f["a"], "m3 per mm"),
        ("Slow response, scaled by the km below the water table (%g h to peak, %d h base)" % M["ss"], f["b"], "m3 per mm per km"),
        ("Sewer below the water table, median day, 2024 to October 2026", f["ls_meter_med"], "km"),
        ("Sewer below the water table, median day, 2004 to 2023", f["ls_replay_med"], "km"),
        ("Sewer below the water table, highest day (June 2025 and 2008 alike)", f["ls_max"], "km"),
        ("Held out, June 2025 high-river weeks: mean error, this model", f["v_cond"], "L/s"),
        ("Held out, June 2025 high-river weeks: mean error, one response per mm", f["v_single"], "L/s"),
        ("Held out, 2026: mean error, this model", f["v_cond26"], "L/s"),
        ("Held out, 2026: mean error, one response per mm", f["v_single26"], "L/s"),
    ]
    for i, (q, v, u) in enumerate(items, start=4):
        ws3.cell(row=i, column=1, value=q)
        ws3.cell(row=i, column=2, value=v)
        ws3.cell(row=i, column=3, value=u)
    ws3["A15"] = ("Fitted on the SCADA's good hours, 1 January 2024 to 31 October 2026, the hours at the weir crest set aside; the "
                  "held-out checks refit each model without the weeks scored.")

    ws4 = wb.create_sheet("Water use per dwelling")
    ws4["A1"] = "Residential use per dwelling peaks each summer quarter at about 450 to 480 litres a day"
    ws4["A1"].font = title
    header(ws4, 3, ["Quarter", "Litres per dwelling per day"], [14, 26])
    for i, (k, v) in enumerate(X["a"].items(), start=4):
        ws4.cell(row=i, column=1, value=k)
        ws4.cell(row=i, column=2, value=v)
    ws4["A16"] = ("Water Metering and Billing Policy section 4; dwellings dated from their code compliance certificates, so a "
                  "quarter counts only the dwellings that stood in it.")

    ws5 = wb.create_sheet("Other stations 2024-2025")
    ws5["A1"] = "PS02 and PS05 overflowed more than twice in both years; three emergency overflows a year across the network"
    ws5["A1"].font = title
    header(ws5, 3, ["Station", "Year", "Wet weather overflows", "Spill hours"], [10, 8, 22, 12])
    r = 4
    for s in AK.STATIONS_B:
        for y in AK.YEARS_B:
            ws5.cell(row=r, column=1, value=s)
            ws5.cell(row=r, column=2, value=y)
            ws5.cell(row=r, column=3, value=X["b"]["%s %d overflows" % (s, y)])
            ws5.cell(row=r, column=4, value=X["b"]["%s %d spill hours" % (s, y)])
            r += 1
    r += 1
    for y in AK.YEARS_B:
        ws5.cell(row=r, column=1, value="Network emergency overflows %d" % y).font = bold
        ws5.cell(row=r, column=3, value=X["b"]["network %d emergency overflows" % y])
        r += 1
    for w, cell in ((ws2, "A4"), (ws3, "A4"), (ws4, "A4"), (ws5, "A4")):
        w.freeze_panes = cell
    wn = wb.create_sheet("Notes")
    notes = [
        "Prepared by Three Waters, Network Operations, for the report to the Council meeting of 10 December 2026.",
        "Overflows: wet weather overflows at the engineered overflow points as discharge permit AUTH-2024-0418 "
        "condition 3 defines them; discharges less than 24 hours apart are one overflow.",
        "Replay: condition 7, every hour of the KRC 1187 rainfall record from 1 January 2004 to 31 December 2023, each day "
        "as it occurred, with the terrace bore's level for the day; averages are the twenty years' overflows over twenty.",
        "Ngaio Road: 260 dwellings at the Code of Practice's 2.7 persons and 200 litres a person a day, through Table 5.2.",
        "Station: 112.0 L/s with both pumps (drawdown test, 7 November 2023) and 350 m3 from the duty start to the weir "
        "crest; the upgrade adds a 1,100 m3 tank below the crest.",
        "Water use: Water Metering and Billing Policy section 4; meters supplying residential rating units only.",
        "Other stations: the overflow monitors' own clock (NZST); emergency overflows are those that began during an "
        "outage on the station's supply.",
        "Figures are computed unrounded and rounded once for reporting.",
    ]
    wn.column_dimensions["A"].width = 120
    for i, t in enumerate(notes, start=1):
        wn.cell(row=i, column=1, value=t).alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    PP.normalize_ooxml(path, "Network Operations", "Network Operations", "2026-11-05T01:12:00Z", "2026-11-12T04:36:00Z",
                       excel=True, title="PS03 Ngaio Road connection assessment 2027")


# ---------------------------------------------------------------------------------------------------- chart
def chart_png(X):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    G = X["G"]
    f = X["fig"]
    yrs = np.arange(2004, 2024)
    fig, ax = plt.subplots(figsize=(10.5, 5.2), dpi=110)
    ax.bar(yrs - 0.2, G["existing"]["per_year"], width=0.4, color="#9aa6b2", label="PS03 as connected now")
    ax.bar(yrs + 0.2, G["with_sub"]["per_year"], width=0.4, color="#1f4e79", label="With Ngaio Road (260 dwellings)")
    ax.axhline(2, color="#c0392b", lw=1.6, ls="--")
    ax.text(2018.55, 2.25, "Consent limit: 2 a year on average", color="#c0392b", fontsize=9)
    ax.set_xticks(yrs)
    ax.set_xticklabels([str(y) for y in yrs], rotation=45, fontsize=8.5)
    ax.set_ylabel("Wet weather overflows at EO-03")
    ax.set_title("PS03 replayed through 2004 to 2023: %.1f a year with Ngaio Road against a limit of 2" % f["with_sub_exact"],
                 fontsize=11.5, loc="left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    fig.text(0.01, 0.01, "Consent AUTH-2024-0418 condition 7; inflow model fitted on the 2024 to 2026 SCADA record. Rauwhero "
             "District Council, Network Operations.", fontsize=7.5, color="#555555")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


# ---------------------------------------------------------------------------------------------------- report
def write_docx(path, X, png):
    import docx
    from docx.shared import Cm, Pt
    f = X["fig"]
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    d.add_heading("Ngaio Road subdivision: connection to the PS03 Riverbank Road wastewater catchment", level=1)
    t = d.add_table(rows=0, cols=2)
    for k, v in (("To", "Council, meeting of 10 December 2026"), ("From", "Three Waters, Network Operations"),
                 ("Date", "13 November 2026"), ("File", "RM26-0187; AUTH-2024-0418; 3W-2029-04")):
        row = t.add_row().cells
        row[0].text = k
        row[1].text = v
    sec = d.sections[0]
    sec.footer.paragraphs[0].text = "Rauwhero District Council | Report to Council | Ngaio Road wastewater connection"
    d.add_heading("Recommendation", level=2)
    d.add_paragraph("That the Council defer the connection of the Ngaio Road subdivision (RM26-0187) to the public "
                    "wastewater network until the PS03 storage upgrade (project 3W-2029-04) is commissioned, and decline "
                    "the applicant's request to connect stage 1 from March 2027.")
    d.add_heading("Why", level=2)
    d.add_paragraph(
        "Condition 8 of the network discharge permit AUTH-2024-0418 lets the Council accept a connection of 50 or more "
        "dwellings only while the overflow frequency at the receiving station, assessed under condition 7, stays within "
        "two wet weather overflows a year. Run through every hour of the 2004 to 2023 record, each day as it occurred, "
        "PS03 overflows %d times in the twenty years as connected now (about %d a year) and %d times with Ngaio Road at "
        "full development (about %d a year). With the upgrade's 1,100 m3 of storage the station overflows %d times in "
        "the twenty years (about %d a year), inside the limit." % (f["total_ex"], f["existing"], f["total_sub"],
                                                                  f["with_sub"], f["total_up"], f["upgrade"]))
    d.add_paragraph(
        "The station's own record since 2024 (two overflows, both in 2026) understates this. Most of what reaches PS03 in a "
        "wet winter is groundwater entering the terrace sewers, and it rises by about %.1f L/s for every kilometre of "
        "sewer below the water table. In 2024 to 2026 the water table stood low: on the median day only %.1f km of sewer "
        "lay below it, against %.1f km over 2004 to 2023. The June 2025 high river put about %d km under water, as the "
        "wettest weeks of 2008 and 2017 did, which is how the effect can be measured on the meter." % (
            f["g"], f["ls_meter_med"], f["ls_replay_med"], f["ls_max"]))
    d.add_paragraph(
        "A model with one response per millimetre of rain and the meter's own dry weather flow reproduces the two 2026 "
        "overflows and gives about %d a year with the subdivision, but it misses the June 2025 high-river weeks by %d L/s "
        "on average when they are held out of its fit, where the model above is within %.1f L/s." % (
            f["naive"], f["v_single"], abs(f["v_cond"])))
    d.add_picture(io.BytesIO(png), width=Cm(16.5))
    d.add_paragraph("Overflows are counted as condition 3 of the permit counts them: discharges less than 24 hours "
                    "apart are one overflow. The station's figures are 112.0 L/s with both pumps and 350 m3 of storage "
                    "below the weir (data sheet revision 4).")
    d.add_heading("Supporting figures", level=2)
    d.add_paragraph("Residential water use in the PS03 catchment ran between %d and %d litres per dwelling per day in "
                    "2024 to 2026 (by quarter, in the assessment workbook), against the Code of Practice's design flow of "
                    "540 litres a dwelling." % (min(X["a"].values()), max(X["a"].values())))
    em = [X["b"]["network %d emergency overflows" % y] for y in AK.YEARS_B]
    d.add_paragraph("Across the network's other stations, PS02 and PS05 recorded more than two wet weather overflows in "
                    "both 2024 and 2025; the network had %d emergency overflows in 2024 and %d in 2025 (power failures). "
                    "Station by station figures are in the workbook." % (em[0], em[1]))
    d.add_heading("Next steps", level=2)
    d.add_paragraph("Advise the applicant of the deferral and the upgrade programme; bring the upgrade's concept design "
                    "to the Infrastructure Committee; reassess the connection under condition 8 when the tank is "
                    "commissioned.")
    d.save(path)
    PP.normalize_docx(path, "Network Operations", "Network Operations", "2026-11-09T20:10:00Z", "2026-11-13T02:55:00Z", 5,
                      188, seed="report", title="Ngaio Road connection report", company="Rauwhero District Council")


# ---------------------------------------------------------------------------------------------------- figures and write-up
def figures(X):
    f = X["fig"]
    return dict(
        call=dict(with_sub=f["with_sub"], existing=f["existing"], upgrade=f["upgrade"], limit=2, naive=f["naive"],
                  meter_logged=f["meter_logged"], with_sub_exact="%.2f" % f["with_sub_exact"]),
        components=dict(g=f["g"], ls_meter_med=f["ls_meter_med"], ls_replay_med=f["ls_replay_med"], ls_max=f["ls_max"],
                        v_cond=f["v_cond"], v_single=f["v_single"]),
        steps=dict(a=f["a"], b=f["b"], qp="112.0", store=350, dwellings=260, occ="2.7", lpd=200, upgrade_m3="1,100",
                   total_ex=f["total_ex"], total_sub=f["total_sub"], total_up=f["total_up"], hours72=72,
                   v_cond26=f["v_cond26"], v_single26=f["v_single26"], dry_years="24", wet_hours=24, replay_years=20,
                   table="5.2"),
        answers=dict(ask_a=X["a"], ask_b=X["b"]))


def submission(X):
    f = X["fig"]
    a = X["a"]
    b = X["b"]
    L = []
    L += ["## Tags", "", "**Domain:** Physical and environmental sciences (hydrology and flood frequency).",
          "**Analytical objective:** Forecasting and predictive modelling.", ""]
    L += ["## 1. Final Recommendation", "",
          "**Hold the Ngaio Road connection until the PS03 storage upgrade is commissioned: replayed through 2004 to 2023 "
          "each day as it occurred, PS03 overflows about %d times a year with the subdivision, above the consent's limit "
          "of 2.**" % f["with_sub"],
          "Not the station's own record of %d overflows since 2024, nor one response per millimetre fitted on the meter "
          "(about %d a year): both carry the meter's low water table into years when it stood far higher. After the "
          "upgrade the station overflows about %d a year with the subdivision." % (f["meter_logged"], f["naive"],
                                                                                  f["upgrade"]), ""]
    L += ["## 2. Critical Components", "",
          "1. PS03's dry weather infiltration rises by **%.1f L/s** for each kilometre of its sewer below the water table." % f["g"],
          "2. The median day had **%.1f km** of sewer below the water table in 2024 to 2026 against **%.1f km** in 2004 to "
          "2023, with about **%d km** at the wettest in both." % (f["ls_meter_med"], f["ls_replay_med"], f["ls_max"]),
          "3. The station overflows about **%d** times a year as connected now, **%d** with Ngaio Road and **%d** with "
          "Ngaio Road after the upgrade." % (f["existing"], f["with_sub"], f["upgrade"]),
          "4. Held out of each fit, the June 2025 high-river weeks are missed by **%d L/s** on average by one response "
          "per millimetre and by **%.1f L/s** by the conditioned model." % (f["v_single"], f["v_cond"]), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Averaged the SCADA export's good 15-minute inflow into UTC hours, setting aside hours with the wet well at the "
          "weir crest, beside the climate station's hourly rain (archive NZST hour ending, 2026 provisional 15-minute UTC).",
          "2. Turned bore 72_1043's depth below its measuring point into the water level and, against the asset "
          "register's PS03 in-service mains, into each day's kilometres of sewer below it: medians %.1f km (2024 to 2026) "
          "and %.1f km (2004 to 2023)." % (f["ls_meter_med"], f["ls_replay_med"]),
          "3. Fitted the dry hours (no rain in the previous 72 hours) as a weekly domestic pattern plus %.1f L/s per km below "
          "the water table, then the rest as a fast rain response (%d m3 per mm) and a slow one scaled by those kilometres "
          "(%.1f m3 per mm per km)." % (f["g"], f["a"], f["b"]),
          "4. Refitted both models without the June 2025 high-river weeks and scored them there and on 2026: mean errors "
          "%.1f and %.1f L/s for the conditioned model, %d and %.1f L/s for one response per millimetre." % (
              f["v_cond"], f["v_cond26"], f["v_single"], f["v_single26"]),
          "5. Ran the model through every hour of 2004 to 2023, each day with its own water table, at the data sheet's 112.0 "
          "L/s and 350 m3, counting overflows under consent condition 3: %d in 20 years as connected now, %d with the "
          "subdivision's 260 dwellings at the code of practice's 2.7 persons, 200 litres and Table 5.2, %d after adding "
          "the upgrade's 1,100 m3." % (f["total_ex"], f["total_sub"], f["total_up"]),
          "6. Water use per dwelling per the billing policy's section 4, each rating unit's dwellings dated by the building "
          "consents' code compliance certificates rather than carried back from the 31 October 2026 rating snapshot.",
          "7. Other stations from the monitors' own NZST message times, each serial placed by the monitor installation "
          "history, an overflow emergency where it began inside an outage at any ICP the council's electricity site list "
          "gives the station's address.",
          "8. With the subdivision the replay averages %.2f overflows a year against condition 6's limit of 2, so condition "
          "8 bars the connection until the upgrade, which brings it to about %d." % (f["with_sub_exact"], f["upgrade"]), ""]
    L += ["## 4. Deliverable Answers", "", "### ps03_ngaio_road_connection_2027.xlsx", "",
          "1. Average wet weather overflows a year over the consent's 2004 to 2023 replay, whole numbers:",
          "   - Without the subdivision: %d" % f["existing"],
          "   - With the subdivision: %d" % f["with_sub"],
          "   - With the subdivision after the upgrade: %d" % f["upgrade"],
          "2. Residential water use per dwelling per day, litres:"]
    for k, v in a.items():
        L.append("   - %s: %d" % (k, v))
    L.append("3. Other stations' wet weather overflows and spill hours (whole hours):")
    for s in AK.STATIONS_B:
        for y in AK.YEARS_B:
            L.append("   - %s %d: %d overflows, %d spill hours" % (s, y, b["%s %d overflows" % (s, y)],
                                                                    b["%s %d spill hours" % (s, y)]))
    L.append("4. Network emergency overflows: 2024: %d; 2025: %d" % (b["network 2024 emergency overflows"],
                                                                    b["network 2025 emergency overflows"]))
    L += ["", "### council_report_ngaio_road_2027.docx", "",
          "1. Recommends deferring the Ngaio Road connection until the PS03 storage upgrade is commissioned, with the three "
          "replay figures (about %d, %d and %d a year) and the chart." % (f["existing"], f["with_sub"], f["upgrade"]),
          "", "### replay_overflows_2004-2023.png", "",
          "1. Bars for each year 2004 to 2023, PS03 as connected now and with Ngaio Road, the consent limit of 2 drawn "
          "across, titled with the %.1f a year the subdivision brings." % f["with_sub_exact"], ""]
    return "\n".join(L)


def main(target, golden, fig_path, sub_path):
    os.makedirs(golden, exist_ok=True)
    X = compute(target)
    write_xlsx(os.path.join(golden, F_XLSX), X)
    png = chart_png(X)
    open(os.path.join(golden, F_PNG), "wb").write(png)
    write_docx(os.path.join(golden, F_DOCX), X, png)
    json.dump(figures(X), open(fig_path, "w"), indent=2)
    open(sub_path, "w").write(submission(X))
    return X
