"""The golden deliverables, computed from the shipped bundle alone: the Government Statistician's determination
(trigger_restatement_determination_2027.pdf) and the regional series on the redesigned basis
(regional_unemployment_redesigned_basis_2024-2026.csv); and generator/figures.json, every figure the write-up states."""
import io
import json
import os

import numpy as np
import pandas as pd

import methods as M
import pack as P
import world as W


def read_cells(target):
    """both exports conformed to one month x region x rotation group table of weighted unemployed and labour force,
    regions on the 2025 classification"""
    conc = pd.read_csv(os.path.join(target, P.FILES["conc"]), dtype=str)
    to25 = dict(zip(conc["region_2019"], conc["region_2025"]))
    old = pd.read_csv(os.path.join(target, P.FILES["old"]), dtype={"REF_MTH": str, "REGION": str})
    old["month"] = old["REF_MTH"].str[:4] + "-" + old["REF_MTH"].str[4:]
    old["region"] = np.where(old["month"] < "2025-01", old["REGION"].map(to25), old["REGION"])
    piv = old.pivot_table(index=["month", "region", "ROTGRP"], columns="LFSTAT", values="WTD000", aggfunc="sum")
    o = pd.DataFrame({"une": piv[2] * 1000.0, "lab": (piv[1] + piv[2]) * 1000.0}).reset_index()
    o.columns = ["month", "region", "group", "une", "lab"]
    new = pd.read_csv(os.path.join(target, P.FILES["new"]), dtype={"region": str})
    n = new.groupby(["period", "region", "rotation_group"])[["unemployed", "employed"]].sum().reset_index()
    n = pd.DataFrame({"month": n["period"], "region": n["region"], "group": n["rotation_group"],
                      "une": n["unemployed"].astype(float), "lab": (n["unemployed"] + n["employed"]).astype(float)})
    allc = pd.concat([o, n], ignore_index=True)
    allc = allc.groupby(["month", "region", "group"])[["une", "lab"]].sum().reset_index()
    une = np.zeros((W.T, W.R, 6))
    lab = np.zeros((W.T, W.R, 6))
    for row in allc.itertuples(index=False):
        t, r, g = W.MONTHS.index(row.month), W.RCODE.index(row.region), W.GROUPS.index(row.group)
        une[t, r, g] += row.une
        lab[t, r, g] += row.lab
    return une, lab


def read_release(target):
    x = pd.read_excel(os.path.join(target, P.FILES["release"]), sheet_name=None, header=None)
    t1 = x["Table 1"].iloc[4:4 + W.T]
    t2 = x["Table 2"].iloc[4:4 + W.T]
    nat = t1.iloc[:, 4].astype(float).values
    reg = t2.iloc[:, 1:1 + W.R].astype(float).values
    return reg, nat


def read_fieldwork(target):
    f = pd.read_parquet(os.path.join(target, P.FILES["field"]))
    lk = pd.read_csv(os.path.join(target, P.FILES["psu"]), dtype=str)
    psu_region = dict(zip(lk["psu"], lk["region_2025"]))
    mi = {m: i for i, m in enumerate(W.MONTHS)}
    f["in_sample_from"] = [W.MONTHS[mi[m] - int(k) + 1] for m, k in zip(f["contact_month"], f["interview_no"])]
    rows = f.to_dict("records")
    return rows, psu_region


def compute(target):
    une, lab = read_cells(target)
    F = M.cells_from(une, lab)
    G, eff = M.golden_break(F)
    change = round(G + 1e-9, 1)
    trigger = M.restated(G)
    reg, nat = read_release(target)
    avg = M.averages_2026(reg)
    des = M.designated(avg, trigger)
    breg, bnat, add = M.back_series(reg, nat, change)
    rows, psu_region = read_fieldwork(target)
    q4 = M.dwellings_q4(rows, psu_region)
    return dict(G=G, eff=eff, change=change, trigger=trigger, reg=reg, nat=nat, avg=avg, designated=des,
                breg=breg, bnat=bnat, add=add, q4=q4, F=F, rows=rows, psu_region=psu_region)


def fmt(v, d=1):
    return ("%.*f" % (d, v)).replace("-", "−")


def chart_png(X):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["font.family"] = "DejaVu Sans"
    k0 = W.MONTHS.index("2024-01")
    xs = np.arange(W.T - k0)
    pub = X["nat"][k0:]
    red = X["bnat"][k0:]
    fig, ax = plt.subplots(figsize=(7.0, 3.5), dpi=150)
    p0, p1 = W.PHASE - k0, W.PHASE - k0 + 4
    ax.axvspan(p0 - 0.5, p1 + 0.5, color="#e9eef3", lw=0)

    ax.plot(xs, pub, color="#8a96a3", lw=1.6, label="As published")
    ax.plot(xs, red, color="#0f4c5c", lw=2.0, label="On the redesigned basis")
    ax.axhline(W.TRIGGER, color="#9a9a9a", lw=1.0, ls=":")
    ax.axhline(X["trigger"], color="#b03a2e", lw=1.1, ls="--")
    ax.text(len(xs) - 0.6, W.TRIGGER + 0.03, "trigger before restatement, 6.0%", ha="right", va="bottom", fontsize=7,
            color="#6b6b6b")
    ax.text(len(xs) - 0.6, X["trigger"] + 0.03, "restated trigger, %s%%" % fmt(X["trigger"]), ha="right", va="bottom",
            fontsize=7, color="#b03a2e")
    ticks = [i for i in range(len(xs)) if W.MONTHS[k0 + i][5:] in ("01", "07")]
    ax.set_xticks(ticks)
    ax.set_xticklabels([pd.Timestamp(W.MONTHS[k0 + i] + "-01").strftime("%b %Y") for i in ticks], fontsize=7.5)
    ax.set_ylabel("Unemployment rate, original (%)", fontsize=8)
    ax.tick_params(axis="y", labelsize=7.5)
    lo = np.floor((min(pub.min(), red.min()) - 0.25) * 10) / 10
    ax.set_ylim(lo, 6.75)
    ax.text((p0 + p1) / 2.0, lo + 0.04, "both questionnaires\nin the field", ha="center", va="bottom", fontsize=7,
            color="#4a5560")
    ax.set_xlim(-0.6, len(xs) - 0.4)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(loc="lower right", fontsize=7.5, frameon=False)
    ax.set_title("The redesigned questionnaire puts the national rate %s points higher" % fmt(X["change"]),
                 fontsize=9.5, loc="left")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def write_pdf(X, path):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    import docs  # noqa: F401  (registers the fonts)
    INK, GREY, TEAL = colors.HexColor("#1b1d20"), colors.HexColor("#5b6067"), colors.HexColor("#0f4c5c")
    body = ParagraphStyle("b", fontName="LiberationSans", fontSize=9.6, leading=13.6, textColor=INK, spaceAfter=6)
    h1 = ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=14, leading=18, textColor=TEAL, spaceAfter=4)
    sub = ParagraphStyle("s", fontName="LiberationSans", fontSize=9, leading=12.5, textColor=GREY, spaceAfter=10)
    h2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.5, leading=14, textColor=TEAL,
                        spaceBefore=8, spaceAfter=3)
    cell = ParagraphStyle("c", fontName="LiberationSans", fontSize=8.6, leading=11, textColor=INK)
    cellb = ParagraphStyle("cb", parent=cell, fontName="LiberationSans-Bold")
    num = ParagraphStyle("num", parent=cell, alignment=2)
    numb = ParagraphStyle("numb", parent=cellb, alignment=2)
    note = ParagraphStyle("n", fontName="LiberationSans-Italic", fontSize=7.8, leading=10.5, textColor=GREY,
                          spaceBefore=3, spaceAfter=8)

    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(20 * mm, 12 * mm, "Determination 2027/1 under section 9 of the %s" % W.ACT)
        canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, "%d" % doc.page)
        canvas.restoreState()

    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=20 * mm, title="Determination 2027/1: restated trigger rate",
                            author=W.STATISTICIAN, subject="", creator="", producer="")
    des = set(X["designated"])
    names = ", ".join(W.RNAME[c] for c in X["designated"][:-1]) + " and " + W.RNAME[X["designated"][-1]]
    s = [Paragraph("The trigger rate is restated at %s per cent" % fmt(X["trigger"]), h1),
         Paragraph("Determination 2027/1 of the %s under section 9 of the %s. %s, 3 February 2027." %
                   (W.STATISTICIAN, W.ACT, W.OFFICE), sub),
         Paragraph("Determination", h2),
         Paragraph("The %s moved to its redesigned questionnaire with the rotation groups replaced from July 2025, and "
                   "every rotation group has answered it since December 2025. With the redesigned questionnaire in full "
                   "use, the national unemployment rate the survey publishes is <b>%s percentage points higher</b> than "
                   "the previous questionnaire would have published for the same months. Under section 9(2) the trigger "
                   "rate of 6.0 per cent is restated at <b>%s per cent</b>, and it applies to the designation that "
                   "takes effect on 1 April 2027 and to every later one." % (W.SURVEY, fmt(X["change"]), fmt(X["trigger"])),
                   body),
         Paragraph("On their twelve-month averages for 2026, every month of them measured on the redesigned "
                   "questionnaire, four regions are at or above the restated trigger: %s." % names, body),
         Paragraph("How the change was measured", h2),
         Paragraph("From July to November 2025 the dwellings entering the sample answered the redesigned questionnaire "
                   "while the dwellings already in it finished on the previous one, so in each of those months the two "
                   "questionnaires were answered by dwellings at different interviews: the redesign by dwellings on "
                   "their first few, the previous questionnaire by dwellings on their last. A first interview, conducted "
                   "face to face, has always found more people looking for work than the telephone interviews after it. "
                   "The change was therefore read interview by interview: each interview number on the redesigned "
                   "questionnaire against the same interview number on the previous questionnaire in the months before "
                   "July 2025, month and region held fixed. The redesign lowers the rate at a first interview and raises "
                   "it at the second to sixth, where dependent interviewing applies, and the change in the published "
                   "rate is the average of the six interview effects, as the published estimate averages the six "
                   "rotation groups.", body),
         Image(io.BytesIO(chart_png(X)), width=170 * mm, height=85 * mm),
         Paragraph("Months before July 2025 restated by the change as determined; July to November 2025, with both "
                   "questionnaires in the field, as published. Source: %s estimation cells (CAI 2014 and ICS) and the "
                   "December 2026 release." % W.SURVEY, note),
         PageBreak(), Paragraph("Regions designated for 2027", h2)]
    rows = [[Paragraph("<b>Region</b>", cell), Paragraph("<b>Twelve-month average, 2026 (%)</b>", num),
             Paragraph("<b>Designated</b>", cell)]]
    for i, c in enumerate(W.RCODE):
        st = cellb if c in des else cell
        rows.append([Paragraph("%s %s" % (c, W.RNAME[c]), st), Paragraph(fmt(X["avg"][i], 2), numb if c in des else num),
                     Paragraph("Yes" if c in des else "No", st)])
    t = Table(rows, colWidths=[62 * mm, 58 * mm, 30 * mm])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, TEAL), ("LINEBELOW", (0, -1), (-1, -1), 0.4, GREY),
                           ("ALIGN", (1, 1), (-1, -1), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
    s += [t, Paragraph("Averages are the means of the twelve monthly rates published to one decimal place (section 3).",
                       note),
          Paragraph("The survey behind the 2026 rates", h2),
          Paragraph("In the fourth quarter of 2026 the survey interviewed %s dwellings, each counted once whatever the "
                    "number of its interviews in the quarter; a dwelling counts when it gave a full or a partial "
                    "interview." % format(X["q4"]["all"], ","), body)]
    rows = [[Paragraph("<b>Region</b>", cell), Paragraph("<b>Responding dwellings, October to December 2026</b>", num)]]
    for c in W.RCODE:
        rows.append([Paragraph("%s %s" % (c, W.RNAME[c]), cell), Paragraph(format(X["q4"][c], ","), num)])
    rows.append([Paragraph("<b>All regions</b>", cell), Paragraph("<b>%s</b>" % format(X["q4"]["all"], ","), num)])
    t = Table(rows, colWidths=[62 * mm, 70 * mm])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, TEAL), ("LINEABOVE", (0, -1), (-1, -1), 0.4, GREY),
                           ("ALIGN", (1, 1), (-1, -1), "RIGHT"), ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
    s += [t, Spacer(1, 10),
          Paragraph("%s<br/>%s" % (W.PEOPLE["statistician"], W.STATISTICIAN), body)]
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


CSV_NAME = "regional_unemployment_redesigned_basis_2024-2026.csv"
PDF_NAME = "trigger_restatement_determination_2027.pdf"


def basis_word(t):
    if t < W.PHASE:
        return "previous questionnaire (restated)"
    if t < W.PHASE + 5:
        return "both questionnaires (as published)"
    return "redesigned questionnaire"


def write_csv(X, path):
    import csv
    k0 = W.MONTHS.index("2024-01")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["month", "region", "region_name", "published_rate", "redesigned_basis_rate", "collected_on"])
        for t in range(k0, W.T):
            for i, c in enumerate(W.RCODE):
                w.writerow([W.MONTHS[t], c, W.RNAME[c], "%.1f" % X["reg"][t, i], "%.1f" % X["breg"][t, i],
                            basis_word(t)])
    return (W.T - k0) * W.R


def figures(X):
    return {
        "trigger_in_force_pct": W.TRIGGER,
        "restated_trigger_pct": X["trigger"],
        "change_points": X["change"],
        "change_points_unrounded": round(X["G"], 4),
        "designated": [W.RNAME[c] for c in X["designated"]],
        "not_designated": [W.RNAME[c] for c in W.RCODE if c not in X["designated"]],
        "average_2026": {W.RNAME[c]: round(float(X["avg"][i]), 2) for i, c in enumerate(W.RCODE)},
        "q4_responding_dwellings": {(W.RNAME[c] if c != "all" else "all"): X["q4"][c] for c in W.RCODE + ["all"]},
        "csv_rows": (W.T - W.MONTHS.index("2024-01")) * W.R,
        "arm_gap_points": round(M.arm_gap(X["F"]), 1),
        "arm_gap_trigger_pct": M.restated(M.arm_gap(X["F"])),
        "single_effect_triggers_pct": sorted({M.restated(v) for v in M.wrong_routes(X["F"], X["nat"])["R2 one effect"].values()}),
        "first_interview_excess_points": round(first_excess(X["F"]), 1),
        "north_coast_shortfall_points": round(X["trigger"] - float(X["avg"][W.RCODE.index("03")]), 2),
    }


def first_excess(F):
    """before July 2025: the first interview's rate less the average of the six interviews, month and region fixed"""
    use = F["t"] < W.PHASE
    b = M.fe(F, [(F["m"] == j).astype(float) for j in range(2, 7)], use, True, mis_fe=False)
    prof = np.concatenate([[0.0], b])
    return float(prof[0] - prof.mean())


def main(target, out_dir, fig_path):
    os.makedirs(out_dir, exist_ok=True)
    X = compute(target)
    write_pdf(X, os.path.join(out_dir, PDF_NAME))
    write_csv(X, os.path.join(out_dir, CSV_NAME))
    import postprocess as PP
    PP.normalize_pdf(os.path.join(out_dir, PDF_NAME), b"D:20270203101544+13'00'", b"D:20270203104219+13'00'")
    with open(fig_path, "w") as f:
        json.dump(figures(X), f, indent=1, sort_keys=False)
        f.write("\n")
    return X
