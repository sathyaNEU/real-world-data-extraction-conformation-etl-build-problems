"""The governing documents and the laboratories' quarterly reports."""
import datetime as dt
import os

from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle)

import world as W

CUTOFF = dt.date(2026, 1, 20)
SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Times-Roman", fontSize=9.5,
                      leading=13, alignment=TA_JUSTIFY, spaceAfter=5)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Times-Bold", fontSize=13, spaceAfter=8)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Times-Bold", fontSize=10.5, spaceAfter=4,
                    spaceBefore=8)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=10.5)
CELL = ParagraphStyle("cell", fontName="Times-Roman", fontSize=8, leading=10)
CELLB = ParagraphStyle("cellb", fontName="Times-Bold", fontSize=8, leading=10)


def P(text, bold=False):
    return Paragraph(str(text), CELLB if bold else CELL)


def wrap(rows):
    """every cell as a flowable, so a long definition wraps inside its column"""
    return [[P(c, bold=(i == 0)) for c in row] for i, row in enumerate(rows)]


TBL = TableStyle([("FONT", (0, 0), (-1, 0), "Times-Bold", 8),
                  ("FONT", (0, 1), (-1, -1), "Times-Roman", 8),
                  ("GRID", (0, 0), (-1, -1), 0.3, colors.Color(0.45, 0.45, 0.45)),
                  ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.90, 0.90, 0.88)),
                  ("VALIGN", (0, 0), (-1, -1), "TOP"),
                  ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                  ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6)])


def _doc(path, title, margin=18):
    return SimpleDocTemplate(path, pagesize=A4, title=title, author="", subject="", creator="",
                             leftMargin=margin * mm, rightMargin=margin * mm,
                             topMargin=margin * mm, bottomMargin=margin * mm)


def regulations(target):
    path = os.path.join(target, "surface_water_quality_regulations_2019.pdf")
    d = _doc(path, "Surface Water Quality Regulations 2019")
    f = []
    f.append(Paragraph("Surface Water Quality (Standards and Compliance Assessment) "
                       "Regulations 2019", H1))
    f.append(Paragraph("Consolidated to the amendment of 14 March 2024. Made by the Minister under "
                       "section 19 of the Water Environment Act. Binding on every river basin "
                       "district authority. Extract for compliance assessment: Parts 2, 3, 5, 6 and 8 "
                       "to 11, Schedule 1 and Schedules 4 to 7 are not reproduced.", SMALL))
    f.append(Paragraph("Part 1 Preliminary", H2))
    f.append(Paragraph("1.1 These Regulations apply to the surface water bodies in each river basin "
                       "district as entered in the district's water body register.", BODY))
    f.append(Paragraph("1.2 In these Regulations, authority means the river basin district authority "
                       "for the district, and the Office means the National Water Quality Office.", BODY))
    f.append(Paragraph("1.3 A substance listed in Schedule 2 is a listed substance and the figure "
                       "beside it is the standard for that substance.", BODY))
    f.append(Paragraph("1.4 The reporting year begins on 1 April and ends on 31 March following. A "
                       "reporting year is named for the two calendar years it falls across.", BODY))
    f.append(Paragraph("Part 4 Monitoring", H2))
    f.append(Paragraph("4.1 The authority shall maintain a monitoring programme for the district "
                       "setting out, for each water body, the sample points at which samples are to "
                       "be taken, the substances to be determined at each point, the number of "
                       "rounds required in a reporting year and the dates between which each point "
                       "is in the programme.", BODY))
    f.append(Paragraph("4.2 A sample taken under the programme at a point in the programme is a "
                       "compliance sample. A sample taken for quality control purposes, including a "
                       "blank, a duplicate and a spiked sample, is not a compliance sample and the "
                       "authority shall identify it as such in its records.", BODY))
    f.append(Paragraph("4.3 The authority shall have its compliance samples analysed by a laboratory "
                       "accredited for the method used, and shall record for every result the "
                       "method, the laboratory and the reporting limit the method achieved for the "
                       "sample.", BODY))
    f.append(Paragraph("4.4 The authority may include in its programme points operated with another "
                       "body under a catchment partnership agreement, and samples taken at those "
                       "points under the programme are compliance samples.", BODY))
    f.append(Paragraph("Part 7 Compliance assessment", H2))
    f.append(Paragraph("7.1 The authority shall assess every water body in its compliance programme "
                       "against every listed substance determined at the water body's points in the "
                       "reporting year.", BODY))
    f.append(Paragraph("7.2 A water body is non-compliant for a listed substance in a reporting year "
                       "where the average concentration of the substance in the water body in that "
                       "year exceeds the standard for the substance. The average is the mean of the "
                       "concentrations of the compliance samples the authority's monitoring "
                       "programme requires for the water body in the reporting year, one "
                       "concentration for each of those samples and each sample weighted equally. "
                       "Where the laboratory has reported no measured value for a sample, the "
                       "authority shall put that sample's own concentration at the figure the "
                       "results it holds support, and shall not report in place of the average any "
                       "property of a distribution fitted to them.", BODY))
    f.append(Paragraph("7.3 The standard for a listed substance is the figure set out beside it in "
                       "Schedule 2, expressed in the units given there.", BODY))
    f.append(Paragraph("7.4 A water body that is not non-compliant for a listed substance is "
                       "compliant for that substance.", BODY))
    f.append(Paragraph("7.5 An assessment shall use the result as approved by the laboratory. Where "
                       "a result has been issued provisionally and later approved, the approved "
                       "result is the result for the sample; where a result has been withdrawn, "
                       "there is no result for the sample.", BODY))
    f.append(Paragraph("7.6 The authority shall state in its annual return, for each water body in "
                       "its compliance programme and each listed substance, the number of compliance "
                       "samples the reporting year holds for the water body, the number of those "
                       "results reported below the reporting limit of the method used, and whether "
                       "the water body is compliant.", BODY))
    f.append(Paragraph("7.7 The return for a reporting year shall be made to the Office no later "
                       "than 30 November following the end of that year.", BODY))
    f.append(Paragraph("Schedule 2 Listed substances and standards", H2))
    rows = [["Substance", "Standard", "Units", "Basis"],
            ["MCPA", "0.05", "ug/l", "annual average"],
            ["2,4-D", "0.30", "ug/l", "annual average"],
            ["Mecoprop", "0.10", "ug/l", "annual average"],
            ["Triclopyr", "0.40", "ug/l", "annual average"],
            ["Ammonium as N", "0.065", "mg/l", "annual average"],
            ["Ortho-phosphate as P", "0.035", "mg/l", "annual average"]]
    t = Table(wrap(rows), colWidths=[55 * mm, 25 * mm, 25 * mm, 45 * mm])
    t.setStyle(TBL)
    f.append(t)
    f.append(Spacer(1, 4 * mm))
    f.append(Paragraph("Schedule 3 Form of the annual return", H2))
    f.append(Paragraph("The return shall be made in the form the Office publishes, one row for each "
                       "water body in the authority's compliance programme and each listed "
                       "substance, and shall state the number of water bodies the authority assesses "
                       "as non-compliant for each listed substance.", BODY))
    d.build(f)
    return path


def method_schedule(target):
    path = os.path.join(target, "laboratory_method_schedule.pdf")
    d = _doc(path, "Laboratory method schedule")
    f = []
    f.append(Paragraph("%s: laboratory method schedule" % W.AUTHORITY, H1))
    f.append(Paragraph("Schedule of the accredited methods under which the district's compliance and "
                       "operational samples are determined, as held on 16 November 2026. Issued by "
                       "the authority's laboratory liaison office.", SMALL))
    rows = [["Method code", "Laboratory", "Determinands", "Technique", "Reporting limit",
             "Units", "In use from"]]
    for code in sorted(W.METHODS):
        m = W.METHODS[code]
        rl = ("%.3f" % m["rl"]) if m["rl"] else "not applicable"
        if code == "TAS-LC-PHX-04":
            rl = "0.005 (5 ng/l)"
        rows.append([code, W.LABS[m["lab"]]["name"], ", ".join(m["analytes"]), m["technique"], rl,
                     m["units"], m["from"].isoformat()])
    t = Table(wrap(rows), colWidths=[28 * mm, 29 * mm, 31 * mm, 28 * mm, 23 * mm, 14 * mm, 21 * mm])
    t.setStyle(TBL)
    f.append(t)
    f.append(Spacer(1, 4 * mm))
    f.append(Paragraph("Notes on scope", H2))
    f.append(Paragraph("TAS-LC-PHX-04 reports the phenoxy herbicides in ng/l. The reporting limit is "
                       "5 ng/l for each of the four determinands and the laboratory reports a result "
                       "below it with the qualifier shown in the export.", BODY))
    f.append(Paragraph("KGL-GC-PHX-07 is accredited to a reporting limit of 0.10 ug/l for each of "
                       "the four determinands and reports in ug/l. The laboratory has held the "
                       "method unchanged since its accreditation in 2014.", BODY))
    f.append(Paragraph("Both phenoxy methods are accredited by the national accreditation board, "
                       "Tirneevin under registration T-0184 and Kilgarron under T-0266, and both "
                       "took part in the 2025 round of the international proficiency scheme for "
                       "acid herbicides in water.", BODY))
    f.append(Paragraph("TAS-IC-ANI-02 determines nitrate as the nitrate ion. KGL-CF-NUT-03 "
                       "determines nitrate as nitrogen. The determinand code on each result says "
                       "which, and the field dictionary gives both.", BODY))
    d.build(f)
    return path


def dictionary(target):
    path = os.path.join(target, "lims_field_dictionary.pdf")
    d = _doc(path, "LIMS field dictionary")
    f = []
    f.append(Paragraph("%s: laboratory information system field dictionary" % W.AUTHORITY, H1))
    f.append(Paragraph("The fields of lims_results_export_2025_2026.csv, as the authority's data "
                       "management office maintains them.", SMALL))
    rows = [["Field", "Meaning"],
            ["lab_sample_id", "the laboratory's own identifier for the sample, unique within the "
                              "laboratory"],
            ["lab_code", "the laboratory that determined the result, TAS or KGL"],
            ["client_point_code", "the sample point as the submitting section coded it for that "
                                  "laboratory; monitoring_point_crosswalk.csv carries the authority's "
                                  "own code for it"],
            ["sample_date, sample_time", "the date and local time the sample was collected"],
            ["date_received", "the date the laboratory received the sample"],
            ["date_approved", "the date the laboratory approved the result; empty while a result is "
                              "provisional"],
            ["sample_type", "FIELD for a sample of the water; FIELD_BLANK, EQUIP_BLANK, FIELD_DUP, "
                            "LAB_DUP and MATRIX_SPIKE for the quality control samples the "
                            "laboratories run alongside it"],
            ["programme", "PEST pesticide suite, NUT nutrient suite, PHY physico-chemical suite, "
                          "ABS the raw water abstraction programme"],
            ["determinand_code", "the substance determined; NO3 is nitrate expressed as the nitrate "
                                 "ion and NO3N is nitrate expressed as nitrogen, so a result under "
                                 "NO3N is 4.4268 times smaller than the same water under NO3"],
            ["method_code", "the accredited method used; laboratory_method_schedule.pdf gives each"],
            ["result", "the value the laboratory reported, in the units of the units field"],
            ["units", "the units of the result and of the reporting limit on the same row"],
            ["qualifier", "a less-than sign where the determinand was not detected; the result field "
                          "is then empty and reporting_limit holds the limit the method achieved for "
                          "that sample"],
            ["reporting_limit", "the reporting limit the method achieved for the sample, in the "
                                "units of the units field"],
            ["result_status", "A approved, P provisional, V withdrawn"],
            ["version", "the version of the result for the sample and determinand; a later version "
                        "supersedes an earlier one"],
            ["batch_id", "the laboratory batch the result was reported in"]]
    t = Table(wrap(rows), colWidths=[32 * mm, 142 * mm])
    t.setStyle(TBL)
    f.append(t)
    f.append(Spacer(1, 4 * mm))
    f.append(Paragraph("Notes", H2))
    f.append(Paragraph("A row is one determinand on one sample at one version. A sample with several "
                       "determinands has one row for each.", BODY))
    f.append(Paragraph("The export holds every version the laboratories have issued up to the "
                       "extract date, including the provisional versions later approved and the "
                       "results later withdrawn.", BODY))
    f.append(Paragraph("The water services section and the catchment monitoring section submit "
                       "samples to the laboratories under their own client point codes. Both codes "
                       "appear in the crosswalk against the authority's sample point code, with the "
                       "section that submits under each.", BODY))
    d.build(f)
    return path


def quarterly_report(target, lab, rows):
    """the laboratory's contractual quarterly report, issued on a cut-off before every result was in"""
    name = {"TAS": "tirneevin", "KGL": "kilgarron"}[lab]
    path = os.path.join(target, "%s_quarterly_report_2025q3.pdf" % name)
    d = _doc(path, "%s quarterly report" % W.LABS[lab]["name"], margin=16)
    f = []
    f.append(Paragraph("%s" % W.LABS[lab]["name"], H1))
    f.append(Paragraph("Quarterly report to %s under contract ARW/LAB/2023. Quarter 3 of the "
                       "2025/26 reporting year, October to December 2025. Issued %s; results "
                       "approved after that date appear in the following quarter's report."
                       % (W.AUTHORITY, CUTOFF.strftime("%d %B %Y")), SMALL))
    f.append(Paragraph("Ortho-phosphate as P, results issued in the quarter", H2))
    sel = sorted([r for r in rows if r["lab_code"] == lab], key=lambda z: z["lab_sample_id"])
    head = ["Sample", "Client point", "Sampled", "Result mg/l", "Status"]
    body = [[r["lab_sample_id"], r["client_point_code"], r["sample_date"], r["result"],
             {"A": "approved", "P": "provisional", "V": "approved"}[r["result_status"]]] for r in sel]
    per = 34
    for i in range(0, len(body), per):
        t = Table(wrap([head] + body[i:i + per]),
                  colWidths=[30 * mm, 28 * mm, 24 * mm, 24 * mm, 24 * mm], repeatRows=1)
        t.setStyle(TBL)
        f.append(t)
        if i + per < len(body):
            f.append(PageBreak())
            f.append(Paragraph("Ortho-phosphate as P, results issued in the quarter (continued)", H2))
    f.append(Spacer(1, 3 * mm))
    f.append(Paragraph("Results listed: %d. Laboratory contact %s. This report lists the results "
                       "this laboratory had issued for the quarter at the date of issue and is not "
                       "a compliance assessment."
                       % (len(sel), W.LABS[lab]["contact"]), SMALL))
    d.build(f)
    return path
