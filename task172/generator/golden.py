"""The golden deliverables (the independent statistician's recommendation to the DMC and the closed tables), the
write-up and figures.json, all computed from target/ through analysis.py."""
import csv
import io
import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from reportlab import rl_config  # noqa: E402

rl_config.invariant = 1
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import analysis as A  # noqa: E402
import postprocess as PP  # noqa: E402

PDF = "talon2_interim_recommendation.pdf"
CSV = "talon2_interim_tables.csv"
ARM = {0: "Placebo + GemCis", 1: "Ravolimab + GemCis"}
SOC_SHORT = {"Infections and infestations": "Infections and infestations", "Hepatobiliary disorders": "Hepatobiliary disorders",
             "Gastrointestinal disorders": "Gastrointestinal disorders",
             "Blood and lymphatic system disorders": "Blood and lymphatic system disorders"}


def compute(target):
    P = A.Pack(target)
    cut, nxt = A.find_cut(P)
    cp, I = A.conditional_power(P, cut)
    F = dict(P=P, cut=cut, next_event=nxt, cp=cp, I=I)
    F["band"] = A.band(cp)
    F["sae"] = A.ask_sae(P, cut)
    F["liver"] = A.ask_liver(P, cut)
    F["expo"] = A.ask_exposure(P, cut)
    d = I["d"]
    F["at_risk"] = int(d["atrisk"].sum())
    F["at_risk_past"] = int(np.sum(d["atrisk"] & (-d["rday"] > A.GOLDEN_BREAK)))
    F["events_arm"] = {a: int(d["event"][d["arm"] == a].sum()) for a in (0, 1)}
    F["n_arm"] = {a: int(np.sum(d["arm"] == a)) for a in (0, 1)}
    F["visits"] = I["by_visit"]
    early = A.S.interval_rates(d["time"], d["event"], d["arm"], [0, A.GOLDEN_BREAK, 1e9])
    F["pieces"] = early
    return F


def km(time, event):
    order = np.lexsort((~event, time))
    t, e = time[order], event[order]
    n = len(t)
    surv, out_t, out_s = 1.0, [0.0], [1.0]
    i = 0
    while i < n:
        j = i
        d = 0
        while j < n and t[j] == t[i]:
            d += e[j]
            j += 1
        if d:
            surv *= 1 - d / (n - i)
            out_t.append(t[i])
            out_s.append(surv)
        i = j
    return np.array(out_t), np.array(out_s)


def chart(F):
    d = F["I"]["d"]
    fig, ax = plt.subplots(figsize=(6.6, 3.3), dpi=150)
    for a, col in ((0, "#7A8B99"), (1, "#1D3557")):
        m = d["arm"] == a
        t, s = km(d["time"][m] / 30.4375, d["event"][m])
        ax.step(t, s, where="post", color=col, lw=1.6, label="%s (n=%d, %d events)" % (ARM[a], F["n_arm"][a], F["events_arm"][a]))
    ax.axvline(A.GOLDEN_BREAK / 30.4375, color="#B0B7BF", lw=0.8, ls=":")
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("Months from randomisation", fontsize=8)
    ax.set_ylabel("Progression-free (BICR)", fontsize=8)
    ax.tick_params(labelsize=7.5)
    ax.grid(axis="y", color="#E3E7EB", lw=0.6)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(fontsize=7.5, frameon=False, loc="lower left")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def pct(x):
    return "%d" % int(round(100 * x))


def pdf(F, path):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.3, leading=12.4, spaceAfter=5)
    head = ParagraphStyle("h", parent=body, fontName="Helvetica-Bold", fontSize=9.8, spaceBefore=5, spaceAfter=2,
                          textColor=colors.HexColor("#1D3557"))
    title = ParagraphStyle("t", parent=body, fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=1)
    small = ParagraphStyle("s", parent=body, fontSize=7.6, leading=9.6, textColor=colors.HexColor("#555555"))
    cell = ParagraphStyle("c", parent=body, fontSize=8, leading=9.8, spaceAfter=0)
    I = F["I"]
    v = F["visits"]
    pc = F["pieces"]
    hr_e = (pc[0][4] / pc[0][5]) / (pc[0][2] / pc[0][3])
    hr_l = (pc[1][4] / pc[1][5]) / (pc[1][2] / pc[1][3])
    labels = ["Week 6", "Week 12", "Week 18", "Week 24", "Week 32 onward"]
    rows = [["Assessment", "Placebo: events / patient-months", "Ravolimab: events / patient-months", "Rate ratio"]]
    for lab, r in zip(labels, v):
        rr = (r[4] / r[5]) / (r[2] / r[3]) if r[2] and r[5] else float("nan")
        rows.append([lab, "%d / %.0f" % (r[2], r[3] / 30.4375), "%d / %.0f" % (r[4], r[5] / 30.4375), "%.2f" % rr])
    t1 = Table([[Paragraph(c, cell) for c in r] for r in rows], colWidths=[30 * mm, 46 * mm, 46 * mm, 22 * mm])
    t1.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#A7B1BB")),
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EDF2")),
                            ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story = [
        Paragraph("TALON-2 interim analysis: recommendation to the DMC", title),
        Paragraph("Closed session, 9 December 2026. Prepared by Dr Beverley Shaw, independent statistician, KUCTU. "
                  "Data cut-off %s (the 165th BICR-confirmed event); database snapshot %s." %
                  (F["cut"].strftime("%-d %B %Y"), "1 December 2026"), small),
        Spacer(1, 4),
        Paragraph("Recommendation", head),
        Paragraph("<b>Continue TALON-2 to its final analysis at 330 events as planned (Schedule 2, band C).</b> "
                  "The conditional power of the final analysis is %s per cent to the nearest 10 per cent (above 99 per "
                  "cent in the projection), well above the band's 80 per cent." % ("100" if F["cp"] >= 0.95 else pct(round(F["cp"], 1))), body),
        Paragraph("Interim data", head),
        Paragraph("All %d patients were randomised by the cut. %d of the 165 events are on placebo and %d on ravolimab. "
                  "The stratified hazard ratio is %.2f (95 per cent CI %.2f to %.2f), stratified log-rank z %.2f. "
                  "Carried into the remaining follow-up as a single ratio, that estimate gives a conditional power of "
                  "about %s per cent, which would fall in band A." %
                  (F["n_arm"][0] + F["n_arm"][1], F["events_arm"][0], F["events_arm"][1], I["hr"], I["ci"][0], I["ci"][1],
                   I["z"], pct(I["cp_trend"])), body),
        Paragraph("The single ratio averages two different periods. Through the week-12 assessment ravolimab patients "
                  "progressed slightly faster than placebo patients (rate ratio %.2f); from the week-18 assessment onward "
                  "they progressed at %.2f times the placebo rate. Most of the interim events fell in the first period, "
                  "because most patients have short follow-up; %d of the %d patients still at risk at the cut are past "
                  "the week-12 assessment, so most of the events still to come fall in the second." %
                  (hr_e, hr_l, F["at_risk_past"], F["at_risk"]), body),
        t1,
        Spacer(1, 4),
        Image(chart(F), width=150 * mm, height=75 * mm),
        Paragraph("Figure 1. Kaplan-Meier estimates of BICR progression-free survival by arm at the interim cut. The "
                  "dotted line marks the gap between the week-12 and week-18 assessments.", small),
        Paragraph("Conditional power", head),
        Paragraph("As the charter defines it (section 4.1): each patient still at risk at the cut was followed forward "
                  "from the last adequate assessment on the arm's progression rate before and after the week-12/week-18 "
                  "gap, with withdrawal at the observed rate, until the 330th event, and the final stratified log-rank "
                  "test was recomputed in %s simulated continuations; it rejects in %s of them. Under the sample-size "
                  "hazard ratio, which the charter excludes, the figure would be about %s per cent." %
                  ("{:,}".format(A.NSIM), "{:,}".format(int(round(F["cp"] * A.NSIM))), pct(I["cp_design"])), body),
        Paragraph("Safety and exposure", head),
        Paragraph("Serious adverse events (pharmacovigilance database), liver test elevations after the first dose and "
                  "exposure are in talon2_interim_tables.csv. Hepatic events are more frequent on ravolimab, as expected "
                  "for the class; none of the tables calls for a safety recommendation.", body),
    ]
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=15 * mm,
                            bottomMargin=16 * mm, title="TALON-2 interim recommendation", author="Beverley Shaw",
                            creator="Beverley Shaw", producer="Beverley Shaw")

    def deco(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawString(18 * mm, 9 * mm, "TALON-2 | DMC closed report | Interim analysis | CONFIDENTIAL")
        canvas.drawRightString(A4[0] - 18 * mm, 9 * mm, "Page %d" % doc.page)
        canvas.restoreState()

    doc.build(story, onFirstPage=deco, onLaterPages=deco)
    open(path, "wb").write(buf.getvalue())
    PP.normalize_pdf(path, b"D:20261203154210+00'00'", b"D:20261204092633+00'00'", "Beverley Shaw")
    return hr_e, hr_l


def table_rows(F):
    rows = []
    for a in (0, 1):
        rows.append(["Serious adverse events", "Patients with a serious adverse event", ARM[a], F["sae"][(a, "patients")]])
        rows.append(["Serious adverse events", "Serious adverse events, all", ARM[a], F["sae"][(a, "events")]])
        for soc in A.SOCS:
            rows.append(["Serious adverse events", soc, ARM[a], F["sae"][(a, soc)]])
    for a in (0, 1):
        rows.append(["Liver tests", "Patients with ALT above 5 x ULN", ARM[a], F["liver"][(a, "ALT")]])
        rows.append(["Liver tests", "Patients with AST above 5 x ULN", ARM[a], F["liver"][(a, "AST")]])
        rows.append(["Liver tests", "Patients with total bilirubin above 3 x ULN", ARM[a], F["liver"][(a, "TBIL")]])
    for a in (0, 1):
        rows.append(["Exposure", "Patients who received study treatment", ARM[a], F["expo"][(a, "safety_population")]])
        rows.append(["Exposure", "Ravolimab or placebo doses given", ARM[a], F["expo"][(a, "doses")]])
    return rows


def write_csv(F, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["Table", "Measure", "Arm", "Value"])
        for r in table_rows(F):
            w.writerow(r)


def submission(F, hr_e, hr_l, path):
    I = F["I"]
    s, l, e = F["sae"], F["liver"], F["expo"]
    lines = [
        "## Tags", "",
        "**Domain:** Biomedical & Clinical Research (survival and time-to-event analysis).",
        "**Analytical objective:** Forecasting & Predictive Modeling.", "",
        "## 1. Final Recommendation", "",
        "**Continue TALON-2 to its final analysis at 330 events as planned: the conditional power is 100 per cent to the "
        "nearest 10 per cent, in Schedule 2's band C (80 per cent or more).** The deciding figure is the final stratified "
        "log-rank test projected over the follow-up still to come at each arm's own progression rate before and after the "
        "week-12 to week-18 assessments. Not the stratified hazard ratio of %.2f carried forward, which gives about %s per "
        "cent and a futility stop, because it averages the early period that holds most interim events with the later "
        "period that holds most of the events still to come." % (I["hr"], pct(I["cp_trend"])), "",
        "## 2. Critical Components", "",
        "1. The interim cut is %s, the date of the 165th BICR-confirmed event; all %d patients were randomised by then "
        "and %d are still at risk." % (F["cut"].strftime("%-d %B %Y"), F["n_arm"][0] + F["n_arm"][1], F["at_risk"]),
        "2. The stratified hazard ratio is **%.2f** (95 per cent CI %.2f to %.2f), and as a single ratio carried forward it "
        "gives a conditional power of about **%s** per cent." % (I["hr"], I["ci"][0], I["ci"][1], pct(I["cp_trend"])),
        "3. Ravolimab patients progress at about **%.1f** times the placebo rate through the week-12 assessment and about "
        "**%.1f** times from the week-18 assessment on, and %d of the %d patients still at risk are past the week-12 "
        "assessment." % (hr_e, hr_l, F["at_risk_past"], F["at_risk"]),
        "4. Projected patient by patient on those rates to the 330th event, the final test rejects in more than 99 per cent "
        "of continuations: conditional power **100** per cent to the nearest 10 per cent.", "",
        "## 3. Step-by-Step Solution", "",
        "1. Converted each randomisation time in talon2_irt_randomisation_export.csv from UTC to the site's time zone in "
        "talon2_sites.json and took the local date as the randomisation date.",
        "2. Built BICR progression-free survival from talon2_bicr_timepoint_reads.csv and the Deaths sheet of "
        "talon2_edc_subject_status.xlsx under the SAP's censoring table, found the cut as the date of the 165th event, and "
        "dropped every read and death after it.",
        "3. Ran the log-rank test and the Cox model (Efron ties) stratified by the IRT strata, then compared each arm's "
        "event rate per patient-month at each assessment visit.",
        "4. Fitted each arm's progression rate before and after the gap between the week-12 and week-18 assessments, "
        "followed every patient still at risk forward from the last adequate assessment (withdrawal at the observed rate) "
        "to the 330th event in %s simulated continuations, and counted those where the final stratified log-rank test "
        "rejects at one-sided 2.5 per cent." % "{:,}".format(A.NSIM),
        "5. For the serious adverse events, took each case's latest report in talon2_pv_sae_line_listing.xlsx, dropped "
        "nullified cases and events outside randomisation to the cut, and linked each case to its patient through the "
        "screening number, resolving the earlier screen-failure numbers of re-screened patients in "
        "talon2_screening_log.csv by site, sex, year of birth and initials.",
        "6. For the liver tests, dated every central sample by its collection date in "
        "talon2_edc_central_lab_kit_log.csv (the Melbourne laboratory's transfer carries the date it received the sample), "
        "added the local results with their own upper limits, and counted patients above 5 or 3 times the upper limit "
        "after the day of the first dose.",
        "7. For exposure, counted the ravolimab or placebo doses the IRT records as administered by the cut, with the EDC "
        "exposure pages, and the patients with any dose.",
        "8. Compared the conditional power with Schedule 2's bands and recommended continuing as planned.", "",
        "## 4. Deliverable Answers", "",
        "### talon2_interim_recommendation.pdf", "",
        "1. Recommendation: continue to the final analysis at 330 events as planned (band C).",
        "2. Conditional power, nearest 10 per cent: 100.", "",
        "### talon2_interim_tables.csv", "",
    ]
    k = 3
    for a in (0, 1):
        lines.append("%d. %s:" % (k, ARM[a]))
        k += 1
        lines.append("   - Patients with a serious adverse event: %d" % s[(a, "patients")])
        lines.append("   - Serious adverse events, all: %d" % s[(a, "events")])
        for soc in A.SOCS:
            lines.append("   - %s: %d" % (soc, s[(a, soc)]))
        lines.append("   - Patients with ALT above 5 x ULN: %d" % l[(a, "ALT")])
        lines.append("   - Patients with AST above 5 x ULN: %d" % l[(a, "AST")])
        lines.append("   - Patients with total bilirubin above 3 x ULN: %d" % l[(a, "TBIL")])
        lines.append("   - Patients who received study treatment: %d" % e[(a, "safety_population")])
        lines.append("   - Ravolimab or placebo doses given: %d" % e[(a, "doses")])
    open(path, "w").write("\n".join(lines) + "\n")


def figures(F, hr_e, hr_l):
    I = F["I"]
    fig = {
        "call": "continue as planned (band C)",
        "cp_golden": "100",
        "cp_golden_unrounded": "%.4f" % F["cp"],
        "cp_above": "99",
        "band_threshold": "80",
        "events_final": "330",
        "events_interim": "165",
        "hr_stratified": "%.2f" % I["hr"],
        "hr_ci": ["%.2f" % I["ci"][0], "%.2f" % I["ci"][1]],
        "logrank_z": "%.2f" % I["z"],
        "cp_trend": pct(I["cp_trend"]),
        "cp_design": pct(I["cp_design"]),
        "rate_ratio_early": ["%.2f" % hr_e, "%.1f" % hr_e],
        "rate_ratio_late": ["%.2f" % hr_l, "%.1f" % hr_l],
        "randomised": str(F["n_arm"][0] + F["n_arm"][1]),
        "events_by_arm": [str(F["events_arm"][0]), str(F["events_arm"][1])],
        "at_risk": str(F["at_risk"]),
        "at_risk_past": str(F["at_risk_past"]),
        "nsim": "{:,}".format(A.NSIM),
        "one_sided_alpha": "2.5",
        "sae": {"%s|%s" % (a, k): str(v) for (a, k), v in F["sae"].items()},
        "liver": {"%s|%s" % (a, k): str(v) for (a, k), v in F["liver"].items()},
        "exposure": {"%s|%s" % (a, k): str(v) for (a, k), v in F["expo"].items()},
        "thresholds": ["5", "3"],
        "ci_level": "95",
        "rejections": "{:,}".format(int(round(F["cp"] * A.NSIM))),
    }
    return fig


def write_all(target, golden, base):
    os.makedirs(golden, exist_ok=True)
    F = compute(target)
    hr_e, hr_l = pdf(F, os.path.join(golden, PDF))
    write_csv(F, os.path.join(golden, CSV))
    submission(F, hr_e, hr_l, os.path.join(base, "submission.md"))
    fig = figures(F, hr_e, hr_l)
    fig["band"] = F["band"]
    return fig
