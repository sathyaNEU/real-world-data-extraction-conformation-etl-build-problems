"""The golden deliverables, written from golden.compute(): the Board memo, the workbook and the chart. Every figure
they print is taken from the same computed values that go into figures.json."""
import datetime as dt
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import openpyxl
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt
from openpyxl.styles import Alignment, Font, PatternFill

import golden as G
import postprocess as PP

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October"]
MEMO = "cost_share_placement_2027.docx"
BOOK = "atrazine_sources_2026.xlsx"
CHART = "raw_water_atrazine_2026.png"
ORDER = ["FEN", "TES", "OXL", "DUN", "LAD"]
LOAD_MONTHS = (4, 5, 6, 7)


def summarise(res):
    days = res["days"]
    per = {k: len(v) for k, v in res["per"].items()}
    call = max(per, key=lambda k: per[k])
    by_month = {m: sum(1 for d in days if d.month == m) for m in range(4, 11)}
    loads = {k: int(round(v)) for k, v in res["loads"].items()}
    loads_m = {k: {m: int(round(v)) for m, v in mm.items()} for k, mm in res["loads_month"].items()}
    pac = {m: int(round(res["pac"].get(m, 0.0))) for m in (5, 6, 7, 8)}
    E = res["E"]
    strat = sorted(d for d, r in E.items() if not r["mixed"])
    # entry depths on the days the tributaries ran their storms, June and July, against the intake
    ev = {}
    for k in G.SUBS:
        zs = [E[d][k] for d in E if dt.date(2026, 6, 1) <= d <= dt.date(2026, 7, 31) and E[d].get(k) is not None
              and not E[d]["mixed"]]
        bottom = sum(1 for d in E if dt.date(2026, 6, 1) <= d <= dt.date(2026, 7, 31) and not E[d]["mixed"]
                     and k in E[d] and E[d][k] is None)
        ev[k] = dict(lo=round(min(zs), 1) if zs else None, hi=round(max(zs), 1) if zs else None, bottom_days=bottom)
    zi = [E[d]["zi"] for d in E if dt.date(2026, 6, 1) <= d <= dt.date(2026, 7, 31)]
    first_feed = res["setpoints"][0][0].date() if res["setpoints"] else None
    last_feed = [t for t, v in res["setpoints"] if v == 0.0][-1].date() if res["setpoints"] else None
    temps = {k: (round(min(res["T"][k][d] for d in res["T"][k] if dt.date(2026, 6, 1) <= d <= dt.date(2026, 7, 31)), 1),
                 round(max(res["T"][k][d] for d in res["T"][k] if dt.date(2026, 6, 1) <= d <= dt.date(2026, 7, 31)), 1))
             for k in G.SUBS}
    return dict(call=call, call_name=G.NAME[call], call_days=per[call], per=per, days_total=len(days),
                first_day=days[0], last_day=days[-1], by_month=by_month, loads=loads, loads_m=loads_m, pac=pac,
                strat_first=strat[0], strat_last=strat[-1], ev=ev, zi_lo=round(min(zi), 1), zi_hi=round(max(zi), 1),
                first_feed=first_feed, last_feed=last_feed, temps=temps,
                dun_offsets=[o for _, o in res["offsets"]["DUN"]], dun_step=res["offsets"]["DUN"][1][0],
                load_total=int(round(sum(res["loads"].values()))))


def memo(F, path):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)
    p = doc.add_paragraph()
    r = p.add_run("CITY OF BRENNICK WATER DEPARTMENT")
    r.bold = True
    p.add_run("\nMerrin Water Treatment Plant")
    t = doc.add_paragraph()
    t.add_run("MEMORANDUM").bold = True
    hdr = [("To", "Board of Water Commissioners"), ("From", "Carl Newman, Water Production Superintendent"),
           ("Prepared with", "Brandi Dougherty, Source Water Protection Coordinator"), ("Date", "November 3, 2026"),
           ("Re", "2027 atrazine cost-share program: Fennick Creek sub-watershed")]
    for a, b in hdr:
        q = doc.add_paragraph()
        q.paragraph_format.space_after = Pt(0)
        q.add_run(a + ": ").bold = True
        q.add_run(b)
    doc.add_paragraph()
    q = doc.add_paragraph()
    q.add_run("Recommendation. ").bold = True
    q.add_run("Place the 2027 cost-share program in the %s sub-watershed." % F["call_name"])
    bm = F["by_month"]
    doc.add_paragraph(
        "In the 2026 season the raw water was above the 3.0 ug/L carbon-feed trigger on %d days: %d in May, %d in June "
        "and %d in July. %s's atrazine was behind all %d of them. Without it the raw water would have stayed at or "
        "below the trigger on each of those days, and no other sub-watershed's water entered the lake at the intake's depth on any of "
        "them." % (F["days_total"], bm[5], bm[6], bm[7], F["call_name"], F["call_days"]))
    tbl = doc.add_table(rows=1, cols=2)
    tbl.style = "Light Grid Accent 1"
    hd = tbl.rows[0].cells
    hd[0].text = "Sub-watershed"
    hd[1].text = "2026 days above the trigger its atrazine caused"
    for k in ORDER:
        c = tbl.add_row().cells
        c[0].text = G.NAME[k]
        c[1].text = "%d" % F["per"][k]
    note = doc.add_paragraph()
    nr = note.add_run("Days counted by plan SWP-01 5.1 and 5.2 on the day's raw-water result of SOP-WQ-07 2.3 (the GC/MS "
                      "confirmation where one was run, otherwise the ELISA screen). Sources: plant laboratory records, "
                      "dam buoy DB-1, stations TR-01 to LB-05, Merrin Dam daily log.")
    nr.font.size = Pt(8.5)
    doc.add_paragraph()
    q = doc.add_paragraph()
    q.add_run("Why Fennick Creek and not the Tessel. ").bold = True
    ev = F["ev"]
    tf = F["temps"]
    q.add_run(
        "The Tessel River carried more atrazine past its station than any other sub-watershed in every month from "
        "April to July, and a load comparison points there. The lake, though, was layered by temperature from %s to "
        "%s, and a tributary's water "
        "goes into a layered lake at the depth where the lake is as warm as the tributary. The intake, at elevation "
        "829.0 ft NGVD29, drew from %.1f to %.1f m below the water surface in June and July. In those months Fennick "
        "Creek ran at %.1f to %.1f C and its water entered at %.1f to %.1f m, the intake's own layer. The Tessel "
        "(%.1f to %.1f C) and Oxley Creek (%.1f to %.1f C) entered in the top %.1f m and their storm water left over "
        "the spillway; Dunmore Creek entered at %.1f to %.1f m; Ladd Branch was colder than the lake's bottom water and "
        "ran to the bottom outlet. The lake mixed again in October with its atrazine well below the trigger."
        % (F["strat_first"].strftime("%B %-d"),
           F["strat_last"].strftime("%B %-d"), F["zi_lo"], F["zi_hi"], tf["FEN"][0], tf["FEN"][1], ev["FEN"]["lo"],
           ev["FEN"]["hi"], tf["TES"][0], tf["TES"][1], tf["OXL"][0], tf["OXL"][1],
           max(ev["TES"]["hi"], ev["OXL"]["hi"]), ev["DUN"]["lo"], ev["DUN"]["hi"]))
    q = doc.add_paragraph()
    q.add_run("Carbon. ").bold = True
    pac = F["pac"]
    q.add_run("The plant fed powdered activated carbon from %s to %s: %s lb in May, %s lb in June, %s lb in July and "
              "%s lb in August." % (F["first_feed"].strftime("%B %-d"), F["last_feed"].strftime("%B %-d"),
                                    "{:,}".format(pac[5]), "{:,}".format(pac[6]), "{:,}".format(pac[7]),
                                    "{:,}".format(pac[8])))
    doc.add_paragraph("Sign-up for the Fennick Creek program opens December 1 so that changed practices are in place "
                      "before the April applications (plan section 4.2).")
    doc.add_paragraph()
    sig = doc.add_table(rows=3, cols=3)
    sig.style = "Table Grid"
    for n, row in enumerate([("", "Name", "Signature and date"), ("Prepared", "Brandi Dougherty", ""),
                             ("Submitted", "Carl Newman", "")]):
        for j, v in enumerate(row):
            sig.rows[n].cells[j].text = v
    fp = doc.sections[0].footer.paragraphs[0]
    fp.text = "Merrin Water Treatment Plant | Source water protection | Page "
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    run = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = "1"
    run.append(t)
    fld.append(run)
    fp._p.append(fld)
    for r_ in fp.runs:
        r_.font.size = Pt(8)
    doc.core_properties.author = "Carl Newman"
    doc.save(path)
    PP.normalize_ooxml(path, "Carl Newman", "Brandi Dougherty", "2026-11-02T21:14:00Z", "2026-11-03T15:42:00Z",
                       title="2027 cost-share placement")


def book(F, res, path):
    wb = openpyxl.Workbook()
    hfont = Font(bold=True)
    fill = PatternFill("solid", fgColor="DDEBF7")

    def head(ws, row, n):
        for c in range(1, n + 1):
            cell = ws.cell(row=row, column=c)
            cell.font = hfont
            cell.fill = fill
            cell.alignment = Alignment(wrap_text=True, vertical="top")

    ws = wb.active
    ws.title = "Placement"
    ws.append(["2027 atrazine cost-share program: placement"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Program goes to", F["call_name"]])
    ws.append(["2026 season days above the 3.0 ug/L trigger", F["days_total"]])
    ws.append([])
    ws.append(["Sub-watershed", "Days above the trigger its atrazine caused"])
    head(ws, 5, 2)
    for k in ORDER:
        ws.append([G.NAME[k], F["per"][k]])
    ws.column_dimensions["A"].width = 44
    ws.column_dimensions["B"].width = 26
    ws.column_dimensions["C"].width = 26

    ws.freeze_panes = "A6"
    ws = wb.create_sheet("Days above trigger")
    ws.append(["Date", "Raw-water result (ug/L)", "Result from"])
    head(ws, 1, 3)
    for d in res["days"]:
        ws.append([d, res["results"][d], "GC/MS confirmation" if d in res["conf"] else "ELISA screen"])
        ws.cell(row=ws.max_row, column=1).number_format = "yyyy-mm-dd"
        ws.cell(row=ws.max_row, column=2).number_format = "0.00"
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = "A1:C%d" % ws.max_row
    ws.column_dimensions["A"].width = 12
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 20

    ws = wb.create_sheet("By month")
    ws.append(["Month (2026)", "Days above the trigger"])
    head(ws, 1, 2)
    for m in range(4, 11):
        ws.append([MONTHS[m - 1], F["by_month"][m]])
    ws.append(["Season", F["days_total"]])
    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 22

    ws = wb.create_sheet("Station atrazine")
    ws.append(["Atrazine past each station by month, 2026 (kg); 15-minute flows times sample concentrations "
               "interpolated linearly in time"])
    ws["A1"].font = Font(bold=True)
    ws.append(["Sub-watershed", "Station"] + [MONTHS[m - 1] for m in LOAD_MONTHS])
    head(ws, 2, 2 + len(LOAD_MONTHS))
    stn = dict(TES="TR-01", FEN="FC-02", OXL="OC-03", DUN="DC-04", LAD="LB-05")
    for k in ORDER:
        if k in F["loads_m"]:
            ws.append([G.NAME[k], stn[k]] + [F["loads_m"][k][m] for m in LOAD_MONTHS])
            for col in range(3, 3 + len(LOAD_MONTHS)):
                ws.cell(row=ws.max_row, column=col).number_format = "#,##0"
        else:
            ws.append([G.NAME[k], stn[k], "not sampled"])
    ws.column_dimensions["A"].width = 16
    ws.column_dimensions["B"].width = 9
    for col in "CDEF":
        ws.column_dimensions[col].width = 11

    ws = wb.create_sheet("Carbon fed")
    ws.append(["Month (2026)", "Powdered activated carbon fed (lb)"])
    head(ws, 1, 2)
    for m in (5, 6, 7, 8):
        ws.append([MONTHS[m - 1], F["pac"][m]])
        ws.cell(row=ws.max_row, column=2).number_format = "#,##0"
    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 32

    ws = wb.create_sheet("Entry depths")
    ws.append(["Date", "Intake depth below surface (m)"] + ["%s entry depth (m)" % G.NAME[k] for k in ORDER])
    head(ws, 1, 7)
    E = res["E"]
    for d in sorted(E):
        if not (dt.date(2026, 5, 1) <= d <= dt.date(2026, 9, 30)):
            continue
        r = E[d]
        row = [d, round(r["zi"], 2)]
        for k in ORDER:
            if r["mixed"]:
                row.append("mixed")
            elif k not in r:
                row.append("")
            elif r[k] is None:
                row.append("bottom")
            else:
                row.append(round(r[k], 2))
        ws.append(row)
        ws.cell(row=ws.max_row, column=1).number_format = "yyyy-mm-dd"
    ws.column_dimensions["A"].width = 12
    for col in "BCDEFG":
        ws.column_dimensions[col].width = 17
    ws.freeze_panes = "B2"
    ws = wb.create_sheet("Notes")
    for line in [
            ["Notes"],
            ["Prepared 3 November 2026 from the 2026 records as exported on 2 November 2026."],
            ["Days above the trigger: the day's raw-water result (SOP-WQ-07 2.3) above 3.0 ug/L, 15 April to 31 October."],
            ["Days caused: a day counts for a sub-watershed when the raw water would have stayed at or below the trigger "
             "without its atrazine (plan SWP-01 5.1)."],
            ["Station atrazine: each 15-minute discharge times the concentration interpolated linearly in time between "
             "the samples either side of it, by local month. A storm bottle's time is its autosampler sample time; a "
             "grab's is its logged time. State Hygienic Laboratory result used where both laboratories ran a bottle; "
             "not detected counted as zero (plan 3.2)."],
            ["DC-04 discharge from gage height through the rating in force; gage height is the logger level plus the "
             "staff-gage offset from the field visits, %.2f ft to %s and %.2f ft after."
             % (F["dun_offsets"][0], F["dun_step"].strftime("%-d %B %H:%M"), F["dun_offsets"][1])],
            ["Ladd Branch is not sampled for atrazine (plan 3.1); LB-05 records flow and temperature."],
            ["Carbon fed: dose setpoint x the plant day's raw water (MGD) x 8.34 (SOP-WQ-07 3.2), minute by minute, "
             "leaving out the minutes the feeder was stopped on a motor overload or had an empty hopper."],
            ["Entry depth: the depth at which the day's buoy profile is as warm as the tributary's daily mean "
             "temperature; 'bottom' where the tributary was colder than the deepest sensor."]]:
        ws.append(line)
    ws["A1"].font = Font(bold=True)
    ws.column_dimensions["A"].width = 120
    for row in ws.iter_rows(min_row=2):
        row[0].alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    PP.normalize_ooxml(path, "Brandi Dougherty", "Brandi Dougherty", "2026-11-02T19:05:00Z", "2026-11-03T14:58:00Z",
                       excel=True)


def chart(F, res, path):
    days = sorted(d for d in res["results"] if G.SEASON[0] <= d <= G.SEASON[1])
    x = [dt.datetime.combine(d, dt.time(12)) for d in days]
    y = [res["results"][d] for d in days]
    above = [(xx, yy) for xx, yy, d in zip(x, y, days) if yy > G.TRIGGER]
    plt.rcParams["svg.hashsalt"] = "task398"
    fig, ax = plt.subplots(figsize=(10, 4.6), dpi=150)
    fig.patch.set_facecolor("#fcfcfb")
    ax.set_facecolor("#fcfcfb")
    ax.plot(x, y, color="#2a78d6", lw=1.6, label="Daily raw-water result")
    ax.scatter([a for a, _ in above], [b for _, b in above], s=22, color="#2a78d6", edgecolor="#fcfcfb", lw=0.8,
               zorder=3, label="Above the trigger (%d days)" % F["days_total"])
    ax.axhline(G.TRIGGER, color="#52514e", lw=1.0, ls=(0, (5, 3)))
    ax.text(x[-1], G.TRIGGER + 0.12, "3.0 ug/L carbon-feed trigger", ha="right", va="bottom", fontsize=8.5,
            color="#52514e")
    ax.set_ylabel("Atrazine, ug/L", color="#0b0b0b", fontsize=9.5)
    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(0, max(y) * 1.12)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.grid(axis="y", color="#e4e3df", lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#a9a8a3")
    ax.tick_params(colors="#52514e", labelsize=8.5)
    ax.set_title("Merrin plant raw water, 15 April to 31 October 2026: %d days above the trigger, %s to %s"
                 % (F["days_total"], F["first_day"].strftime("%-d %B"), F["last_day"].strftime("%-d %B")),
                 loc="left", fontsize=10.5, color="#0b0b0b")
    ax.legend(frameon=False, fontsize=8.5, loc="upper right")
    fig.text(0.01, 0.01, "Day's result per SOP-WQ-07 2.3 (GC/MS confirmation where run, otherwise the ELISA screen). "
             "Source: Merrin WTP laboratory records.", fontsize=7, color="#52514e")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, facecolor=fig.get_facecolor(), metadata={"Software": None})
    plt.close(fig)


def write(res, outdir):
    F = summarise(res)
    memo(F, os.path.join(outdir, MEMO))
    book(F, res, os.path.join(outdir, BOOK))
    chart(F, res, os.path.join(outdir, CHART))
    out = dict(call=F["call_name"], call_key=F["call"], call_days=F["call_days"], days_total=F["days_total"],
               per_sub={G.NAME[k]: F["per"][k] for k in G.SUBS}, days_by_month={MONTHS[m - 1]: F["by_month"][m]
                                                                                 for m in range(4, 11)},
               loads_kg={G.NAME[k]: F["loads"][k] for k in F["loads"]}, load_total_kg=F["load_total"],
               loads_month_kg={G.NAME[k]: {MONTHS[m - 1]: F["loads_m"][k][m] for m in LOAD_MONTHS} for k in F["loads_m"]},
               pac_lb={MONTHS[m - 1]: F["pac"][m] for m in (5, 6, 7, 8)},
               first_day=F["first_day"].isoformat(), last_day=F["last_day"].isoformat(),
               strat_first=F["strat_first"].isoformat(), strat_last=F["strat_last"].isoformat(),
               intake_depth_m=[F["zi_lo"], F["zi_hi"]], entry_m={G.NAME[k]: F["ev"][k] for k in G.SUBS},
               temps_jun_jul_c={G.NAME[k]: list(F["temps"][k]) for k in G.SUBS},
               first_feed=F["first_feed"].isoformat(), last_feed=F["last_feed"].isoformat(),
               rungs={"r0_load_kg": {G.NAME[k]: round(float(v), 1) for k, v in res["rungs"]["r0_load"].items()},
                      "r1_mixed30_days": {G.NAME[k]: v for k, v in res["rungs"]["r1_mixed30"].items()},
                      "r1_mixed14_days": {G.NAME[k]: v for k, v in res["rungs"]["r1_mixed14"].items()},
                      "r1_mixed45_days": {G.NAME[k]: v for k, v in res["rungs"]["r1_mixed45"].items()}},
               pac_no_downtime_lb={MONTHS[m - 1]: int(round(res["pac_nodown"].get(m, 0.0))) for m in (5, 6, 7, 8)},
               dun_offsets_ft=[round(o, 2) for _, o in res["offsets"]["DUN"]],
               dun_step_ft=round(res["offsets"]["DUN"][0][1] - res["offsets"]["DUN"][1][1], 2),
               dun_step_at=res["offsets"]["DUN"][1][0].isoformat(),
               cited=dict(sop_day_result="2.3", sop_pounds_formula="3.2", plan_sections=["5.1", "5.2", "3.2"],
                          buoy_sensor_depths_m=[0.5, 15.5, 1.0, 16.0], intake_centreline_navd88_ft=G.INTAKE_NAVD,
                          navd88_minus_ngvd29_ft=G.NAVD_MINUS_NGVD, look_back_days=30, layer_half_width_m=2.0,
                          lb_per_mg_per_mgl=8.34))
    return out
