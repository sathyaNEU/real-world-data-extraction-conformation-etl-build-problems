"""The governing documents: the DMC charter, the statistical analysis plan and Schedule 2 of the Ashgrove funding
agreement, each set as its office issues it."""
import io

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import postprocess as PP  # noqa: E402

NAVY = colors.HexColor("#1D3557")
TEAL = colors.HexColor("#2A6F77")


def styles(accent):
    ss = getSampleStyleSheet()
    return dict(
        body=ParagraphStyle("b", parent=ss["Normal"], fontName="Times-Roman", fontSize=10.5, leading=14, spaceAfter=6),
        head=ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                            spaceBefore=8, spaceAfter=3, textColor=accent),
        title=ParagraphStyle("t", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=15, leading=19, spaceAfter=3,
                             textColor=accent),
        sub=ParagraphStyle("s", parent=ss["Normal"], fontName="Helvetica", fontSize=9, leading=12, spaceAfter=10,
                           textColor=colors.HexColor("#444444")),
        cell=ParagraphStyle("c", parent=ss["Normal"], fontName="Helvetica", fontSize=8.6, leading=10.6),
        cellb=ParagraphStyle("cb", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=8.6, leading=10.6),
    )


def table(rows, widths, st, accent):
    data = [[Paragraph(str(c), st["cellb"] if i == 0 else st["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA5B1")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6ECF2")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    return t


def build(path, title, author, items, foot, created, modified, accent=NAVY):
    st = styles(accent)
    story = []
    for kind, val in items:
        if kind == "table":
            story.append(table(val[0], val[1], st, accent))
            story.append(Spacer(1, 6))
        elif kind == "gap":
            story.append(Spacer(1, val))
        else:
            story.append(Paragraph(val, st[kind]))

    def deco(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(20 * mm, 12 * mm, foot)
        canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, "Page %d" % doc.page)
        canvas.restoreState()

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=20 * mm, title=title, author=author, creator=author, producer=author)
    doc.build(story, onFirstPage=deco, onLaterPages=deco)
    open(path, "wb").write(buf.getvalue())
    PP.normalize_pdf(path, created, modified, author)


def charter(path):
    items = [
        ("title", "TALON-2 Data Monitoring Committee Charter"),
        ("sub", "Version 3.0, 3 March 2026. Kesterton University Cancer Trials Unit (KUCTU). Approved by the DMC chair, "
                "Dr Jay O'Connor, and the Chief Investigator. Supersedes version 2.1 of 18 November 2025."),
        ("head", "1. Purpose"),
        ("body", "TALON-2 is a randomised, double-blind, placebo-controlled phase 3 trial of ravolimab, an investigational "
                 "immune checkpoint antibody supplied by Halvorsen Therapeutics, added to gemcitabine and cisplatin as "
                 "first-line treatment of advanced biliary tract cancer. The trial is sponsored by the University of "
                 "Kesterton, coordinated by KUCTU and funded by the Ashgrove Cancer Research Trust. The independent Data "
                 "Monitoring Committee (DMC) safeguards the interests of trial patients, reviews accumulating unblinded "
                 "safety and efficacy data and makes recommendations to the Trial Steering Committee (TSC). This charter "
                 "sets out how the DMC works, what it receives and the recommendations open to it."),
        ("head", "2. Membership and independence"),
        ("body", "The DMC has three voting members: an oncologist (chair), a second oncologist and a statistician, none of "
                 "whom has any involvement in the trial or any interest in its outcome. The unblinded independent "
                 "statistician at KUCTU, Dr Beverley Shaw, prepares the closed reports and attends closed sessions without "
                 "a vote. The trial management group, the Chief Investigator and the funder remain blind to results by "
                 "arm until the final analysis."),
        ("head", "3. Meetings and reports"),
        ("body", "The DMC meets every six months for safety review and once for the interim analysis. Open reports "
                 "(recruitment, data completeness, conduct) are prepared by the trial statistician; closed reports, by "
                 "arm, are prepared by the independent statistician from a database snapshot taken after the data cut. "
                 "Every closed report gives progression-free survival by arm with the stratified log-rank test and the "
                 "stratified hazard ratio defined in the statistical analysis plan, serious adverse events by arm and "
                 "system organ class, laboratory abnormalities of grade 3 or worse by arm, and exposure to study treatment "
                 "by arm."),
        ("head", "4. The interim analysis"),
        ("body", "One interim analysis is planned, for futility only, when 165 progression-free survival events confirmed "
                 "by the blinded independent central review (BICR) have been observed, half the 330 events of the final "
                 "analysis. The data cut-off for the interim analysis is the date of the 165th event. There is no early "
                 "stopping for efficacy, and the final analysis keeps its full one-sided significance level of 2.5 per "
                 "cent."),
        ("body", "4.1 At the interim analysis the independent statistician reports the conditional power of the final "
                 "analysis to the DMC. The conditional power is the probability that the final analysis, the stratified "
                 "log-rank test of BICR-assessed progression-free survival at its 330th event, rejects the null "
                 "hypothesis at the one-sided 2.5 per cent level, given the data at the interim analysis. It is computed "
                 "for the trial as it will run from the interim cut: every patient still at risk at the cut, and every "
                 "patient still to be randomised up to the planned 450, followed until the 330th event, with progression "
                 "in each arm over that remaining follow-up as the interim data estimate it. It is not computed under the "
                 "hazard ratio assumed for the sample size."),
        ("body", "4.2 The DMC compares the conditional power with the continuation bands of Schedule 2 of the Ashgrove "
                 "funding agreement (Appendix A) and recommends to the TSC one of: continue to the final analysis as "
                 "planned; continue with the final analysis extended as Schedule 2 provides; or stop for futility. The "
                 "DMC may depart from the bands only for a safety reason, which it records in the closed minutes."),
        ("body", "4.3 The chair reports to the TSC and, through the TSC, to the Trust only the recommendation and the band "
                 "the conditional power falls in. No estimate of the treatment effect leaves the closed session."),
        ("head", "5. Safety review"),
        ("body", "At every meeting the DMC reviews serious adverse events, deaths, grade 3 or worse laboratory "
                 "abnormalities and exposure by arm. It may recommend a protocol change, additional monitoring or a "
                 "pause in recruitment at any meeting on safety grounds."),
        ("head", "Appendix A. Continuation bands (from Schedule 2 of the funding agreement)"),
        ("table", ([["Conditional power at the interim analysis", "Recommendation"],
                    ["Below 20 per cent", "Stop for futility"],
                    ["20 per cent or more, and below 80 per cent", "Continue, with the final analysis extended to 420 events"],
                    ["80 per cent or more", "Continue to the final analysis at 330 events as planned"]],
                   [70 * mm, 95 * mm])),
    ]
    build(path, "TALON-2 DMC Charter v3.0", "Kesterton University Cancer Trials Unit", items,
          "TALON-2 DMC Charter v3.0 | KUCTU-TL2-DMC-003 | Confidential", b"D:20260303101422+00'00'",
          b"D:20260303164005+00'00'")


def sap(path):
    items = [
        ("title", "TALON-2 Statistical Analysis Plan"),
        ("sub", "Version 2.0, 9 February 2026. Kesterton University Cancer Trials Unit. Prepared by the trial statistics "
                "team; approved by the Chief Investigator and the Trial Steering Committee."),
        ("head", "1. Design"),
        ("body", "Patients with previously untreated, unresectable or recurrent biliary tract cancer are randomised 1:1 "
                 "to ravolimab 1,500 mg or placebo, each given with gemcitabine 1,000 mg/m<super>2</super> and cisplatin "
                 "25 mg/m<super>2</super> on days 1 and 8 of each 21-day cycle for up to eight cycles, then ravolimab "
                 "1,500 mg or placebo alone every 4 weeks until progression or unacceptable toxicity. Randomisation is by "
                 "the interactive response technology (IRT), in permuted blocks, stratified by disease status (initially "
                 "unresectable or recurrent) and primary tumour site (intrahepatic cholangiocarcinoma, extrahepatic "
                 "cholangiocarcinoma or gallbladder cancer). The planned sample size is 450 patients."),
        ("head", "2. Primary endpoint"),
        ("body", "Progression-free survival (PFS) is the time from randomisation to the earlier of disease progression "
                 "assessed by the blinded independent central review (BICR) under RECIST 1.1 and death from any cause. "
                 "Tumour assessments (CT or MRI) are scheduled every 6 weeks (plus or minus 7 days) from randomisation to "
                 "week 24 and every 8 weeks thereafter until BICR-confirmed progression. The date of progression is the "
                 "date of the scan at which the BICR records progressive disease."),
        ("table", ([["Situation", "PFS date", "Outcome"],
                    ["BICR progressive disease, or death with no BICR progression before it", "Scan date of progression, or date of death", "Event"],
                    ["No progression and no death", "Date of the last adequate BICR assessment (complete response, partial response or stable disease)", "Censored"],
                    ["No adequate assessment after randomisation, no death", "Date of randomisation", "Censored"],
                    ["Progression or death immediately after two or more consecutive assessments the BICR recorded as not evaluable", "Date of the last adequate assessment before them", "Censored"],
                    ["Assessments or deaths after the data cut-off", "Not used", ""]],
                   [62 * mm, 70 * mm, 38 * mm])),
        ("body", "The date of randomisation is the local date at the site at the moment of randomisation."),
        ("head", "3. Analysis populations"),
        ("body", "The intention-to-treat population is every randomised patient, analysed by the arm assigned. The safety "
                 "population is every randomised patient who received at least one dose of any study treatment "
                 "(ravolimab, placebo, gemcitabine or cisplatin), analysed by the arm assigned."),
        ("head", "4. Final analysis of the primary endpoint"),
        ("body", "The final analysis takes place when 330 BICR-confirmed PFS events have been observed. The two arms are "
                 "compared by the log-rank test stratified by the two stratification factors as recorded in the IRT at "
                 "randomisation, at the one-sided 2.5 per cent level. The hazard ratio is estimated by a Cox model "
                 "stratified by the same factors, with Efron's method for tied event times, and reported with its 95 per "
                 "cent confidence interval. Kaplan-Meier estimates are presented by arm."),
        ("body", "330 events give 90 per cent power to detect a hazard ratio of 0.70 at the one-sided 2.5 per cent level. "
                 "With 450 patients recruited over about 12 months, the final analysis was expected about 24 months after "
                 "the first patient was randomised."),
        ("head", "5. Interim analysis"),
        ("body", "A single interim analysis for futility takes place at 165 events. It is conducted by the independent "
                 "statistician for the DMC under the DMC charter, which defines the conditional power the DMC reviews and "
                 "the recommendations open to it. The interim analysis does not alter the significance level of the "
                 "final analysis."),
        ("head", "6. Safety"),
        ("body", "Adverse events are coded with MedDRA version 27.1 and graded with CTCAE version 5.0. Serious adverse "
                 "events are summarised from the pharmacovigilance safety database, the trial's record of serious "
                 "events, each event counted once in the arm the patient was randomised to; an event is included when it "
                 "began on or after randomisation and on or before the data cut-off, and is summarised under the "
                 "preferred term and system organ class of its latest report. A case nullified by pharmacovigilance is not "
                 "an event."),
        ("body", "Laboratory abnormalities are graded from central and local laboratory results against the upper limit of "
                 "normal of the laboratory that measured the sample. The baseline value is the last sample taken on or "
                 "before the day of the first dose; a value is on treatment when the sample was taken after the day of "
                 "the first dose."),
        ("body", "Exposure is summarised as the number of doses of ravolimab or placebo given and the number of cycles of "
                 "chemotherapy given."),
    ]
    build(path, "TALON-2 SAP v2.0", "Kesterton University Cancer Trials Unit", items,
          "TALON-2 Statistical Analysis Plan v2.0 | KUCTU-TL2-SAP-002", b"D:20260209092715+00'00'",
          b"D:20260211141950+00'00'", accent=TEAL)


def schedule(path):
    green = colors.HexColor("#2D5A27")
    items = [
        ("title", "Ashgrove Cancer Research Trust"),
        ("sub", "Research Funding Agreement AGR-2025-0417 with the University of Kesterton: TALON-2. Schedule 2, "
                "Continuation and Extension. Signed 14 October 2025."),
        ("head", "2.1 Tranches"),
        ("body", "The Trust funds the trial in two tranches. Tranche 1 (GBP 4.2 million) covers set-up, recruitment and "
                 "follow-up to the interim analysis. Tranche 2 (GBP 3.1 million) covers follow-up, treatment costs and "
                 "analysis from the interim analysis to the final analysis at 330 events."),
        ("head", "2.2 The continuation decision"),
        ("body", "Tranche 2 is released on the recommendation the Data Monitoring Committee makes at the interim "
                 "analysis. The Trust's Clinical Trials Committee receives the recommendation and the continuation band "
                 "below that the conditional power defined in the DMC charter falls in. The Trust does not receive, and "
                 "will not ask for, any estimate of the treatment effect."),
        ("table", ([["Band", "Conditional power", "What the Trust does"],
                    ["A", "Below 20 per cent", "Funding ends with tranche 1. The University closes the trial to further "
                     "treatment and follow-up and reports the interim results."],
                    ["B", "20 per cent or more, and below 80 per cent", "Tranche 2 is released with an extension grant of "
                     "GBP 0.9 million, and the final analysis is moved to 420 events so that the trial keeps a "
                     "reasonable chance of a conclusive result."],
                    ["C", "80 per cent or more", "Tranche 2 is released and the trial continues to its final analysis at "
                     "330 events as planned."]],
                   [14 * mm, 46 * mm, 110 * mm])),
        ("head", "2.3 Timing"),
        ("body", "The University informs the Trust of the band within 15 working days of the DMC meeting at which the "
                 "interim analysis is reviewed. Tranche 2, and any extension grant, is paid within 30 days of that "
                 "notice."),
        ("head", "2.4 Safety"),
        ("body", "Nothing in this Schedule limits the DMC's freedom to recommend a change to the trial on safety grounds "
                 "at any time."),
    ]
    build(path, "Funding Agreement AGR-2025-0417 Schedule 2", "Ashgrove Cancer Research Trust", items,
          "AGR-2025-0417 | Schedule 2 | Commercial in confidence", b"D:20251010151204+01'00'",
          b"D:20251014103318+01'00'", accent=green)
