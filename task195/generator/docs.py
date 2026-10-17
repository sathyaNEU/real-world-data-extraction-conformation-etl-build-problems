"""The laboratory's own documents: the validation protocol, the estimator's model card, the partner
laboratory's weekly reports and the method group's 2025 extraction platform validation."""
import os
import statistics

from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import world as W

SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Times-Roman", fontSize=9.5, leading=13,
                      alignment=TA_JUSTIFY, spaceAfter=5)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Times-Bold", fontSize=13, spaceAfter=7)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Times-Bold", fontSize=10.5, spaceAfter=4,
                    spaceBefore=8)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=10.5)
CELL = ParagraphStyle("c", fontName="Times-Roman", fontSize=8, leading=10)
CELLB = ParagraphStyle("cb", fontName="Times-Bold", fontSize=8, leading=10)
TBL = TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.Color(0.45, 0.45, 0.45)),
                  ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.90, 0.90, 0.88)),
                  ("VALIGN", (0, 0), (-1, -1), "TOP"),
                  ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                  ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6)])


def wrap(rows):
    return [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in row] for i, row in enumerate(rows)]


def _doc(path, title):
    return SimpleDocTemplate(path, pagesize=A4, title=title, author="", subject="", creator="",
                             leftMargin=18 * mm, rightMargin=18 * mm, topMargin=17 * mm,
                             bottomMargin=17 * mm)


def protocol(target):
    path = os.path.join(target, W.FILES["protocol"])
    d = _doc(path, "KVAL-07 method validation")
    cut_rows = [["Cutoff", "Mixture fraction at or above", "Listed since"]]
    for i, c in enumerate(W.CUTOFFS):
        cut_rows.append(["C%d" % (i + 1), "%.3f" % c, "issue 3, 2026-09-14"])
    f = [Paragraph("%s, %s: KVAL-07 method validation and method change" % (W.LAB, W.INSTITUTE), H1),
         Paragraph("Issue 4, approved %s by %s, quality manager. Sections 1, 2, 6 and 7 and annexes B "
                   "to E are not reproduced in this extract." % ("2027-02-19", W.PEOPLE["quality"]), SMALL),
         Paragraph("3 Verification of a replacement screen", H2),
         Paragraph("3.1 A replacement screen is verified on a parallel run. The parallel run for the "
                   "contamination screen covers specimens received on or after 1 March 2027 and on or "
                   "before 31 May 2027 under a cohort service project code. Specimens received under a "
                   "contract agreement are outside the validation scope.", BODY),
         Paragraph("3.2 A specimen is in the comparison when the quality-control export records an "
                   "accepted read for it, the v3.4 re-run of its archived read sets returns a mixture "
                   "fraction on the read set the laboratory accepted, and the identity panel register "
                   "holds a verdict of MIXED or CONCORDANT for it reported on or before 21 June 2027.", BODY),
         Paragraph("3.3 The identity panel is the reference standard for the validation. A confirmed "
                   "contamination event is a specimen whose verdict is MIXED.", BODY),
         Paragraph("3.4 Detection is counted per specimen. A screen detects a confirmed contamination "
                   "event when it flags that specimen. The screen in service flags a specimen when the "
                   "quality-control export records a FLAG call for its accepted read. The candidate screen "
                   "flags a specimen when the mixture fraction on its accepted read set is at or above "
                   "the cutoff.", BODY),
         Paragraph("3.5 The false-call rate of a screen is the specimens it flags among the comparison's "
                   "specimens whose verdict is CONCORDANT, as a share of those specimens.", BODY),
         Paragraph("4 The change decision", H2),
         Paragraph("4.1 The screen in service is replaced by the candidate screen at the highest cutoff "
                   "value listed in Table 2 at which both of the following hold on the parallel run: "
                   "(a) the increase in confirmed contamination events detected over the screen in "
                   "service is established with a 95 per cent interval above zero, and (b) the candidate "
                   "screen's false-call rate is not higher than the screen in service's. If no listed "
                   "cutoff meets both, the change is not made and the parallel run continues into the "
                   "next quarter.", BODY),
         Paragraph("4.2 The change takes effect at the start of the quarter following the decision. The "
                   "laboratory quality review takes the decision and records it in the validation file "
                   "before the quarter opens.", BODY),
         Paragraph("Table 2 Cutoffs listed for the candidate screen", H2),
         Table(wrap(cut_rows), colWidths=[22 * mm, 52 * mm, 42 * mm]),
         Spacer(1, 5 * mm),
         Paragraph("5 The validation file", H2),
         Paragraph("5.1 The validation file holds, for each listed cutoff, the confirmed contamination "
                   "events the candidate screen detects, its increase over the screen in service and its "
                   "false-call rate, with the decision 4.1 gives. It also holds the record of the screen "
                   "in service over the twelve reporting months before the parallel run, the quarter's "
                   "analytical sensitivity panel, and the identity panel's delivery record against the "
                   "partner laboratory's weekly reports.", BODY),
         Paragraph("5.2 Where the identity panel reports a verdict after the validation extract is "
                   "taken, the specimen is carried into the next parallel run and is not added to a "
                   "closed comparison.", BODY),
         Paragraph("Annex A Validation request", H2),
         Paragraph("A.1 The screening lead requested the verification on 4 June 2027. The autumn intake "
                   "quarter is the heaviest of the year and the confirmatory queue is set before it "
                   "opens, so a change to the contamination screen is decided at the June review or "
                   "left for the next quarter.", BODY),
         Paragraph("A.2 The screen in service is the per specimen heterozygosity-excess screen HETX. "
                   "The candidate screen is the mixture-fraction estimator introduced in %s, run over "
                   "the archived read sets of the same receipts." % W.PIPELINE, BODY),
         Paragraph("A.3 The identity panel types %d markers per specimen at the partner laboratory and "
                   "is reported two to three weeks behind the laboratory's own release, so it cannot gate a "
                   "release. A verdict of MIXED is returned where a second contributor's share is above "
                   "%.3f." % (W.PANEL_MARKERS, W.PANEL_LOD), BODY)]
    d.build(f)


def model_card(target, estimates):
    path = os.path.join(target, W.FILES["modelcard"])
    d = _doc(path, "Mixture fraction estimator v3.4")
    vals = sorted(estimates)
    n = len(vals)
    q = lambda p: vals[min(n - 1, int(p * n))]
    rows = [["Statistic", "Value"],
            ["Read sets with an estimate", "%d" % n],
            ["Median", "%.4f" % statistics.median(vals)],
            ["90th percentile", "%.4f" % q(0.90)],
            ["99th percentile", "%.4f" % q(0.99)],
            ["Share below the limit of detection", "%.1f per cent" % (100.0 * sum(1 for v in vals if v < 0.008) / n)]]
    f = [Paragraph("Mixture fraction estimator, %s" % W.PIPELINE, H1),
         Paragraph("Bioinformatics group, %s. Version 3.4.1, refreshed 2027-06-11, owner: the "
                   "bioinformatics group lead. Scope: what the estimator is and what it returns on the "
                   "production archive. Screening cutoffs are set in KVAL-07." % W.LAB, SMALL),
         Paragraph("What the estimator returns", H2),
         Paragraph("The estimator fits a two-component allele-balance mixture over the markers of the "
                   "core panel and returns the share of a specimen's reads attributed to a second "
                   "contributor, as a fraction. It requires a mean depth of %d or more and at least "
                   "120,000 markers assessed; read sets below either floor return no estimate." % W.DEPTH_FLOOR, BODY),
         Paragraph("The estimate is computed from the read set alone. It does not use the specimen's "
                   "heterozygosity, the plate it sat on, or any call the quality-control pipeline "
                   "recorded.", BODY),
         Paragraph("Limit of detection", H2),
         Paragraph("On the vendor's reference series the estimator separates a second contributor from "
                   "background above a share of about 0.008. Below that the estimate is dominated by "
                   "allele-balance noise and the vendor reports no reliable recovery. The laboratory "
                   "repeats an analytical sensitivity panel each quarter.", BODY),
         Paragraph("What the estimator returned on the 2027 archive", H2),
         Table(wrap(rows), colWidths=[76 * mm, 40 * mm]),
         Spacer(1, 4 * mm),
         Paragraph("Computed on the accepted read sets of the March to May 2027 re-run, the file "
                   "%s. The table describes the estimator's output and states no verdict." % W.FILES["mf"], SMALL),
         Paragraph("Known behaviour", H2),
         Paragraph("Specimens from the same donor sequenced twice return estimates within about 0.002 "
                   "of each other at low shares. A depth top-up library typed from the same extraction "
                   "returns a slightly higher estimate than the first library at shares above 0.05, "
                   "because the top-up reads are drawn from the same contaminated extraction.", BODY)]
    d.build(f)


def weekly_reports(target, panel):
    """The partner laboratory's weekly reports, as the laboratory scans them on receipt."""
    path = os.path.join(target, W.FILES["weekly"])
    d = _doc(path, "Identity panel weekly reports 2027")
    counts, dates = {}, {}
    for r in panel:
        counts[r[3]] = counts.get(r[3], 0) + 1
        dates[r[3]] = r[4]
    refs = sorted(counts)
    f = [Paragraph("%s: identity panel weekly reports" % W.PARTNER, H1),
         Paragraph("Framework agreement AVT-2025-088 with %s, %s. Each report covers the results "
                   "issued in the week ending on the report date. Scanned on receipt by the "
                   "laboratory's reception desk." % (W.LAB, W.INSTITUTE), SMALL)]
    for ref in refs:
        rows = [["Report", "Issued", "Week ending", "Results issued"],
                [ref, dates[ref], dates[ref], "%d" % counts[ref]]]
        f.append(Paragraph("Report %s" % ref, H2))
        f.append(Table(wrap(rows), colWidths=[30 * mm, 30 * mm, 30 * mm, 30 * mm]))
        f.append(Spacer(1, 2.5 * mm))
        if ref == "BA-2027-W19":
            f.append(Paragraph("Issued two working days late; the courier returned the week's batch to "
                               "the depot on the Thursday.", SMALL))
    f.append(Paragraph("A result is issued per specimen and aliquot typed. Where a report is re-sent, "
                       "the week's count includes the results sent again.", SMALL))
    d.build(f)


def platform(target):
    path = os.path.join(target, W.FILES["platform"])
    d = _doc(path, "Extraction platform validation 2025")
    rows = [["Method", "Specimens", "Median yield (ug)", "Median A260/A280", "Failures"],
            ["magnetic bead", "384", "6.4", "1.84", "7"],
            ["silica column", "192", "4.9", "1.79", "11"],
            ["salting out", "96", "8.1", "1.72", "4"]]
    f = [Paragraph("%s: extraction platform validation, 2025" % W.LAB, H1),
         Paragraph("Method group report MG-2025-14, 20 November 2025. Approved for the cohort service's "
                   "routine extraction from January 2026.", SMALL),
         Paragraph("Scope", H2),
         Paragraph("The report compares the three extraction methods the laboratory runs, on yield, "
                   "purity and failure rate, over the 2025 verification specimens. It does not cover "
                   "sequencing, quality-control screening or the identity panel.", BODY),
         Paragraph("Results", H2),
         Table(wrap(rows), colWidths=[34 * mm, 24 * mm, 34 * mm, 34 * mm, 20 * mm]),
         Spacer(1, 4 * mm),
         Paragraph("Conclusion", H2),
         Paragraph("The magnetic bead method is retained as the default for the cohort service. The "
                   "silica column method is kept for specimens below 200 microlitres and the salting "
                   "out method for the biobank's archived blood clots.", BODY)]
    d.build(f)
