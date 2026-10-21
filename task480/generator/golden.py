"""The golden deliverables: the intake county workbook (every county's 2027 NOx against the 10-ton line, with a
chart, the 2025 pilot's retirements and charges, and each county's in-county inspections) and the recommendation
memo for the CMAQ funding request, plus generator/figures.json."""
import json
import os

import asks as A
import methods as M
import world as W
from writeup import WORDS

HERE = os.path.dirname(os.path.abspath(__file__))


def r0(v):
    return int(v + 0.5) if v >= 0 else -int(-v + 0.5)


def figures(target):
    g = M.golden(target)
    R = M.routes(target)
    e = g["frame"]
    miles = e.groupby("county")["m27"].sum().reindex(W.NAMES)
    tons = g["tons"]
    q = M.designated(tons)
    pil = A.pilot_figures(target)
    pil_naive = A.pilot_figures(target, drop_reinstated=False, rate_card=False)
    vouch = {c: v["n"] for c, v in A.pilot_figures(target, drop_reinstated=False).items()}
    fam = ["golden", "ols3", "ols4", "ll4", "ll6", "bin1"]
    sets = {k: M.designated(v) for k, v in R.items()}
    return dict(
        call=dict(counties=q, n=len(q)), threshold=W.THRESHOLD_TONS, year=2027,
        counties={c: dict(no="%02d" % W.CNO[c], eligible=int(g["n"][c]), read=int(g["read"][c]),
                          miles_m=round(float(miles[c]) / 1e6, 1), tons_unrounded=round(float(tons[c]), 3),
                          tons=r0(float(tons[c])), qualifies=c in q) for c in W.NAMES},
        totals=dict(eligible=int(g["n"].sum()), read=int(g["read"].sum()), tons=r0(float(tons.sum())),
                    miles_m=round(float(miles.sum()) / 1e6, 1)),
        rungs={k: dict(set=sets[k], tons={c: round(float(R[k][c]), 2) for c in W.NAMES}) for k in R},
        r1_over_pct=r0(100.0 * (float(R["R1"].sum()) / float(tons.sum()) - 1)),
        family_range={c: [round(min(float(R[k][c]) for k in fam), 3), round(max(float(R[k][c]) for k in fam), 3)]
                      for c in W.NAMES},
        pilot={c: dict(vouchers=vouch[c], retired=pil[c]["n"], charges=int(round(pil[c]["charges"])),
                       naive_retired=pil_naive[c]["n"], naive_charges=int(round(pil_naive[c]["charges"])))
               for c in W.PILOT_COUNTIES},
        zone_charges=zone_charges(target),
        filed=dict(clauses=["2.1", "3.1", "3.2", "3.3", "3.4"], unusable_odometers=[0, 999999], age_from="1 January",
                   grams_per_short_ton="907,184.74"),
        dates=dict(snapshot="2026-07-01", memo="2026-10-26", guidelines="2026-09-08"),
        names={c: c for c in W.NAMES}, people={k: v[0] for k, v in W.PEOPLE.items()})


def zone_charges(target):
    """The charge per tow zone the two dismantlers who bill per vehicle put on their lines."""
    import pandas as pd
    inv = pd.read_csv(os.path.join(target, W.FILES["invoices"]), dtype=str)
    other = inv[inv["dismantler_licence"] != "D-2864"]
    return {z: int(float(a.iloc[0])) for z, a in other.groupby("tow_zone")["amount"]}


def chart_png(path, f):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "svg.hashsalt": "t480"})
    ink, muted, hi, lo, line = "#0b0b0b", "#52514e", "#2a78d6", "#8c8b86", "#b03a2e"
    order = sorted(W.NAMES, key=lambda c: -f["counties"][c]["tons_unrounded"])
    vals = [f["counties"][c]["tons_unrounded"] for c in order]
    cols = [hi if f["counties"][c]["qualifies"] else lo for c in order]
    fig, ax = plt.subplots(figsize=(6.6, 3.6), dpi=150)
    xs = list(range(len(order)))
    ax.bar(xs, vals, color=cols, width=0.72, edgecolor="white", linewidth=1.0)
    for x_, c, v in zip(xs, order, vals):
        ax.text(x_, v + 0.25, "%d" % f["counties"][c]["tons"], ha="center", fontsize=7, color=ink)
    ax.axhline(W.THRESHOLD_TONS, color=line, lw=1.0, ls="--", zorder=0)
    ax.text(len(order) - 0.6, W.THRESHOLD_TONS + 0.25, "10 tons, guidelines 3.1", color=line, fontsize=7, ha="right",
            va="bottom")
    ax.set_xticks(xs)
    ax.set_xticklabels(order, fontsize=7, color=muted, rotation=35, ha="right")
    ax.set_ylabel("NOx in 2027, short tons", color=muted)
    ax.set_ylim(0, max(vals) + 2.0)
    ax.tick_params(axis="y", colors=muted, labelsize=7.5)
    ax.grid(axis="y", color="#e4e3df", lw=0.6)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#bdbcb7")
    ax.legend(handles=[Patch(color=hi, label="Intake events (10 tons or more)"), Patch(color=lo, label="Below 10 tons")],
              loc="upper right", frameon=False, fontsize=7.5)
    ax.set_title("%s counties' eligible vehicles reach 10 tons of NOx in 2027" % WORDS[f["call"]["n"]].capitalize(),
                 fontsize=9, loc="left", color=ink)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def write_workbook(path, f):
    from openpyxl import Workbook
    from openpyxl.chart import BarChart, LineChart, Reference
    from openpyxl.styles import Alignment, Font, PatternFill
    head, fill = Font(bold=True), PatternFill("solid", fgColor="DCE6F1")
    wb = Workbook()
    ws = wb.active
    ws.title = "Intake counties"
    hdr = ["County no.", "County", "Eligible vehicles", "With a usable reading", "2027 miles (millions)",
           "2027 NOx (short tons)", "10-ton line", "Intake events"]
    ws.append(hdr)
    order = sorted(W.NAMES, key=lambda c: -f["counties"][c]["tons_unrounded"])
    for c in order:
        x = f["counties"][c]
        ws.append([x["no"], c, x["eligible"], x["read"], x["miles_m"], x["tons"], W.THRESHOLD_TONS,
                   "Yes" if x["qualifies"] else "No"])
    t = f["totals"]
    ws.append([None, "Twelve counties", t["eligible"], t["read"], t["miles_m"], t["tons"], None, "%d counties" % f["call"]["n"]])
    for cell in ws[1]:
        cell.font, cell.fill = head, fill
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    for cell in ws[len(order) + 2]:
        cell.font = head
    for col, w in zip("ABCDEFGH", [10, 15, 11, 12, 12, 12, 9, 13]):
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=2, max_row=len(order) + 2):
        row[2].number_format = row[3].number_format = "#,##0"
        row[4].number_format = "0.0"
        row[5].number_format = "0"
        row[6].number_format = "0.0"
    ws.freeze_panes = "C2"
    bar = BarChart()
    bar.type = "col"
    bar.title = "2027 NOx of each county's eligible vehicles, short tons"
    bar.y_axis.title = "Short tons"
    bar.add_data(Reference(ws, min_col=6, min_row=1, max_row=len(order) + 1), titles_from_data=True)
    bar.set_categories(Reference(ws, min_col=2, min_row=2, max_row=len(order) + 1))
    ln = LineChart()
    ln.add_data(Reference(ws, min_col=7, min_row=1, max_row=len(order) + 1), titles_from_data=True)
    bar += ln
    bar.height, bar.width = 8.5, 17
    cs = wb.create_sheet("Chart")
    cs.add_chart(bar, "A1")
    ps = wb.create_sheet("Pilot 2025")
    ps.append(["County no.", "County", "Vouchers paid", "Vehicles retired", "Dismantler charges paid ($)"])
    for c in W.PILOT_COUNTIES:
        p = f["pilot"][c]
        ps.append(["%02d" % W.CNO[c], c, p["vouchers"], p["retired"], p["charges"]])
    ps.append([None, "Four counties", sum(f["pilot"][c]["vouchers"] for c in W.PILOT_COUNTIES),
               sum(f["pilot"][c]["retired"] for c in W.PILOT_COUNTIES),
               sum(f["pilot"][c]["charges"] for c in W.PILOT_COUNTIES)])
    for cell in ps[1]:
        cell.font, cell.fill = head, fill
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    for cell in ps[len(W.PILOT_COUNTIES) + 2]:
        cell.font = head
    for row in ps.iter_rows(min_row=2):
        row[2].number_format = row[3].number_format = "#,##0"
        row[4].number_format = "$#,##0"
    for col, w in zip("ABCDE", [10, 15, 11, 11, 16]):
        ps.column_dimensions[col].width = w
    ns = wb.create_sheet("Notes")
    notes = [
        "Intake counties: guidelines 3.1 to 3.4. Eligible vehicles are the ACTIVE records on the 1 July 2026 "
        "registration snapshot in a member county, gasoline or flex-fuel, model years %d to %d, GVWR class 1 or 2a." % W.ELIG_MY,
        "A vehicle's 2027 miles: its odometer at its completed 2024 to 2025 initial inspection, set against the cumulative "
        "miles the area's inspected vehicles had travelled by the same age (a quadratic in age fitted to every completed "
        "initial reading, age from 1 January of the model year), times that curve's rise from the vehicle's age on 1 "
        "January 2027 to its age on 1 January 2028. Vehicles without a usable reading take their county and model "
        "year's average (3.4).",
        "NOx: 2027 miles times the Table 2 running rate for the model year and program class, in short tons of 907,184.74 "
        "grams. Counties are compared with 10.0 tons before rounding; tons are shown to the nearest ton.",
        "Pilot 2025: a voucher whose vehicle is registered again (ACTIVE) at 1 July 2026 is not counted as retired. "
        "Dismantler charges are the program agreement's charge for each vehicle's tow zone; Oakhaven Salvage & Parts' "
        "invoice export repeats the invoice total on every line.",
        "Prepared by the Mobile Sources Section, 26 October 2026.",
    ]
    for n in notes:
        ns.append([n])
    ns.column_dimensions["A"].width = 120
    for row in ns.iter_rows():
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


def write_memo(path, f, png):
    from docx import Document
    from docx.shared import Inches, Pt
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    q = f["call"]["counties"]
    doc.add_heading("%s counties qualify for 2027 intake events" % WORDS[len(q)].capitalize(), level=1)
    for k, v in (("To", "%s, %s" % W.PEOPLE["director"]), ("From", "%s, %s" % W.PEOPLE["chief"]),
                 ("Date", "26 October 2026"), ("Re", "Intake counties for the 2027 Vehicle Retirement Program CMAQ request")):
        p = doc.add_paragraph()
        p.add_run("%s: " % k).bold = True
        p.add_run(v)
    c = f["counties"]
    names = ", ".join("%s (%d tons)" % (x, c[x]["tons"]) for x in q[:-1]) + " and %s (%d tons)" % (q[-1], c[q[-1]]["tons"])
    below = sorted((x for x in W.NAMES if x not in q), key=lambda x: -c[x]["tons_unrounded"])
    doc.add_paragraph(
        "%s of the twelve member counties qualify for intake events in 2027: %s. Their eligible gasoline cars and light "
        "trucks of model years %d to %d will emit 10 short tons of NOx or more in 2027 under guidelines 3.1 to 3.4. "
        "The nearest county below the line is %s at %d tons." % ((WORDS[len(q)].capitalize(), names) + W.ELIG_MY +
                                                                     (below[0], c[below[0]]["tons"])))
    doc.add_paragraph(
        "Each vehicle's 2027 miles come from its own odometer at its first inspection of the 2024 to 2025 cycle, as the "
        "guidelines require, but not as the reading divided by the vehicle's age: that is the average of every year the "
        "car has been on the road, and older cars are driven less each year. I set each reading against the cumulative "
        "miles the area's inspected vehicles had covered by the same age and took that curve's rise over 2027, so a car "
        "keeps its own level (Elkhollow's and Marlbank's drivers cover far more ground than Wexmoor's) and travels the "
        "miles its age now carries. Dividing the reading by the age instead overstates the eligible fleet's 2027 NOx by %d "
        "per cent and would put %s counties over the line." % (f["r1_over_pct"], WORDS[len(f["rungs"]["R1"]["set"])]))
    doc.add_picture(png, width=Inches(6.3))
    t = doc.add_table(rows=1, cols=5)
    t.style = "Light Grid Accent 1"
    for cell, h in zip(t.rows[0].cells, ("County", "Eligible vehicles", "With a reading", "2027 NOx, tons", "Intake events")):
        cell.text = h
    for x in sorted(W.NAMES, key=lambda x: -c[x]["tons_unrounded"]):
        r = t.add_row().cells
        r[0].text = x
        r[1].text = "{:,}".format(c[x]["eligible"])
        r[2].text = "{:,}".format(c[x]["read"])
        r[3].text = "%d" % c[x]["tons"]
        r[4].text = "Yes" if c[x]["qualifies"] else "No"
    p = f["pilot"]
    doc.add_paragraph(
        "The 2025 pilot retired %s vehicles in Elkhollow, %s in Dunmarsh, %s in Larkhaven and %s in Kinnard; %d of the "
        "vouchers paid went to vehicles their owners took back before they were crushed, which are registered again. "
        "The Department paid the dismantlers $%s, $%s, $%s and $%s for the retired vehicles at the agreement's charges."
        % (p["Elkhollow"]["retired"], p["Dunmarsh"]["retired"], p["Larkhaven"]["retired"], p["Kinnard"]["retired"],
           sum(p[x]["vouchers"] - p[x]["retired"] for x in W.PILOT_COUNTIES),
           "{:,}".format(p["Elkhollow"]["charges"]), "{:,}".format(p["Dunmarsh"]["charges"]),
           "{:,}".format(p["Larkhaven"]["charges"]), "{:,}".format(p["Kinnard"]["charges"])))
    src = doc.add_paragraph(
        "Sources: registration snapshot of 1 July 2026; Enhanced Inspection Program tests, 2024 and 2025; Table 2 "
        "(15 April 2026); pilot voucher register and dismantler invoices. NOx is running exhaust only; counties are compared with the line before rounding.")
    for run in src.runs:
        run.font.size = Pt(8.5)
        run.italic = True
    sec = doc.sections[0]
    fp = sec.footer.paragraphs[0]
    fp.text = "State %s | %s | 2027 Vehicle Retirement Program" % (W.STATE_AGENCY, W.SECTION)
    for run in fp.runs:
        run.font.size = Pt(8)
    doc.core_properties.author = W.PEOPLE["chief"][0]
    doc.save(path)


def build(gdir, target=None, figs=None):
    import postprocess as PP
    target = target or os.path.join(os.path.dirname(gdir), "target")
    figs = figs or os.path.join(HERE, "figures.json")
    os.makedirs(gdir, exist_ok=True)
    f = figures(target)
    json.dump(f, open(figs, "w", encoding="utf-8"), indent=1, sort_keys=True, ensure_ascii=False)
    write_workbook(os.path.join(gdir, W.GOLDEN["workbook"]), f)
    png = os.path.join(gdir, ".chart.png")
    chart_png(png, f)
    write_memo(os.path.join(gdir, W.GOLDEN["memo"]), f, png)
    os.remove(png)
    who = W.PEOPLE["chief"][0]
    PP.normalize_ooxml(os.path.join(gdir, W.GOLDEN["memo"]), who, who, "2026-10-23T14:10:00Z", "2026-10-26T16:42:00Z",
                       company="State %s" % W.STATE_AGENCY)
    PP.normalize_ooxml(os.path.join(gdir, W.GOLDEN["workbook"]), who, who, "2026-10-22T18:05:00Z", "2026-10-26T15:58:00Z",
                       excel=True, company="State %s" % W.STATE_AGENCY)
    return f
