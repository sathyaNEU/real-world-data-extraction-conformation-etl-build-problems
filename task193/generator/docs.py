"""The three governing documents, in their issuers' own voices: the Department's post-closure approval (2017), the
statistical analysis plan the District filed under it (revision 2, 2018), and the consultant's groundwater sampling
procedure (FS-03 revision 4, 2021). None of them describes the data files."""
import os

from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import world as W

SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Times-Roman", fontSize=10.5, leading=14,
                      alignment=TA_JUSTIFY, spaceAfter=6)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Times-Bold", fontSize=14, spaceAfter=6, leading=17)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Times-Bold", fontSize=11, spaceAfter=3, spaceBefore=8)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=9, leading=11.5)
LH = ParagraphStyle("lh", parent=BODY, fontName="Times-Bold", fontSize=10, leading=12, alignment=0, spaceAfter=4,
                    textColor=colors.Color(0.28, 0.28, 0.28))
CELL = ParagraphStyle("c", fontName="Times-Roman", fontSize=9, leading=11)
CELLB = ParagraphStyle("cb", fontName="Times-Bold", fontSize=9, leading=11)
TBL = TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.Color(0.4, 0.4, 0.4)),
                  ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.88)),
                  ("VALIGN", (0, 0), (-1, -1), "TOP"),
                  ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)])


def _table(head, rows, widths):
    data = [[Paragraph(h, CELLB) for h in head]] + [[Paragraph(str(c), CELL) for c in r] for r in rows]
    t = Table(data, colWidths=[w * inch for w in widths], repeatRows=1)
    t.setStyle(TBL)
    return t


def _doc(path, title):
    return SimpleDocTemplate(path, pagesize=letter, title=title, author="", subject="", creator="",
                             leftMargin=1.0 * inch, rightMargin=1.0 * inch, topMargin=0.9 * inch, bottomMargin=0.9 * inch)


class _Furnished(rl_canvas.Canvas):
    """a running header and a footer with 'Page n of N' on every page, drawn once the page count is known"""
    HEAD = ("", "")
    FOOT = ""

    def __init__(self, *a, **k):
        rl_canvas.Canvas.__init__(self, *a, **k)
        self._pages = []

    def showPage(self):
        self._pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        n = len(self._pages)
        for state in self._pages:
            self.__dict__.update(state)
            self.saveState()
            self.setFont("Times-Roman", 8)
            self.setFillColor(colors.Color(0.3, 0.3, 0.3))
            w, h = letter
            self.drawString(1.0 * inch, h - 0.55 * inch, self.HEAD[0])
            self.drawRightString(w - 1.0 * inch, h - 0.55 * inch, self.HEAD[1])
            self.setStrokeColor(colors.Color(0.55, 0.55, 0.55))
            self.setLineWidth(0.4)
            self.line(1.0 * inch, h - 0.6 * inch, w - 1.0 * inch, h - 0.6 * inch)
            self.line(1.0 * inch, 0.68 * inch, w - 1.0 * inch, 0.68 * inch)
            self.drawString(1.0 * inch, 0.52 * inch, self.FOOT)
            self.drawRightString(w - 1.0 * inch, 0.52 * inch, "Page %d of %d" % (self._pageNumber, n))
            self.restoreState()
            rl_canvas.Canvas.showPage(self)
        rl_canvas.Canvas.save(self)


def _furnished(head, foot):
    return type("Furnished", (_Furnished,), {"HEAD": head, "FOOT": foot})


def _sig(name):
    """an electronic signature as the firm's document system prints it: /s/ and the signer's initial and surname"""
    first, last = name.split(" ", 1)
    return "/s/ %s. %s" % (first[0], last)


def _signatures(rows):
    """the approval block: role, name and title, signature, date"""
    data = [[Paragraph(h, CELLB) for h in ("", "Name and title", "Signature", "Date")]]
    data += [[Paragraph(c, CELL) for c in r] for r in rows]
    t = Table(data, colWidths=[w * inch for w in (1.35, 3.0, 1.05, 1.1)])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.Color(0.4, 0.4, 0.4)),
                           ("LINEBELOW", (2, 1), (2, -1), 0.4, colors.Color(0.55, 0.55, 0.55)),
                           ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                           ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return t


def _control(rows):
    """the document control block: label and value pairs in a ruled two-column table"""
    t = Table([[Paragraph(a, CELLB), Paragraph(b, CELL)] for a, b in rows], colWidths=[1.6 * inch, 4.9 * inch])
    t.setStyle(TBL)
    return t


def sap(path):
    doc = _doc(path, "Statistical Analysis Plan, Marten Creek Landfill")
    P = W.PEOPLE
    f = [Paragraph("Kettle Prairie Solid Waste District", LH),
         Paragraph("Statistical Analysis Plan for Groundwater Detection Monitoring", H1),
         Paragraph("Marten Creek Landfill (closed), Kettle Prairie Solid Waste District", H2),
         _control([("Document", "MCL-GW-SAP, Revision 2"),
                   ("Issued", "16 March 2018"),
                   ("Prepared by", "Fieldstone Hydrogeology, LLC, for the District"),
                   ("Submitted under", "Condition 9 of the post-closure plan approval of 11 September 2017"),
                   ("Approved", "By the Department, 24 May 2018"),
                   ("Supersedes", "Revision 1, December 2016")]),
         Spacer(1, 4),
         Paragraph("1. Purpose", H2),
         Paragraph("This plan sets out how the District evaluates the results of each groundwater detection monitoring "
                   "event at the Marten Creek Landfill to decide whether any compliance well shows an increase over "
                   "background water quality that has to be verified, and how a verified increase is reported.", BODY),
         Paragraph("2. Monitoring network", H2),
         Paragraph("The background wells, MW-1, MW-2 and MW-3, were installed in June 2014 west of the waste, "
                   "hydraulically upgradient of it, to sample background water quality. The compliance wells, MW-4 to "
                   "MW-8 (installed 2014) and MW-9 to MW-11 (installed 2017), lie along the eastern, northern and "
                   "southern edges of the waste. Piezometers PZ-1 to PZ-4 are water level points only and are not "
                   "sampled. A replacement well takes the place in this plan of the well it replaces.", BODY),
         Paragraph("3. Events and indicator parameters", H2),
         Paragraph("Detection monitoring events are held each April and each October. Every well in the network is "
                   "sampled at each event, and water levels are measured at every well and piezometer before purging "
                   "begins. The indicator parameters evaluated under this plan are chloride, dissolved sodium and "
                   "dissolved boron. The other parameters of the monitoring program are reported with each event but "
                   "are not evaluated under this plan.", BODY),
         Paragraph("4. Background water quality", H2),
         Paragraph("Background water quality is the quality of groundwater that the landfill has not affected. For each "
                   "indicator parameter it is estimated from every routine sample of that groundwater collected at the "
                   "background wells in the detection monitoring events from April 2018 through the April event of the "
                   "year being evaluated, so that the evaluation of an October event uses the background results through "
                   "that year's April event. The result used for a sample is the laboratory's reportable result for the "
                   "primary sample. Field duplicates, verification samples and equipment, trip and laboratory "
                   "quality-control samples are not background results.", BODY),
         Paragraph("5. Upper prediction limit", H2),
         Paragraph("For each indicator parameter the upper prediction limit is computed from the natural logarithms of "
                   "its background results as UPL = exp( m + t &#215; s &#215; &#8730;(1 + 1/n) ), where n is the number of "
                   "background results, m and s are the mean and the standard deviation (divisor n &#8722; 1) of their "
                   "logarithms, and t is the 99th percentile of Student's t distribution with n &#8722; 1 degrees of "
                   "freedom. The limit is not rounded before a result is compared with it, and is reported to three "
                   "significant figures.", BODY),
         Paragraph("6. Comparison and verification", H2),
         Paragraph("A compliance well's routine result for an indicator parameter that is greater than that parameter's "
                   "upper prediction limit is an initial exceedance. Every compliance well with an initial exceedance for "
                   "any indicator parameter is resampled for the parameters that exceeded within 60 days of its routine "
                   "sample. An initial exceedance that the verification sample confirms is a statistically significant "
                   "increase, and the District notifies the Department of it within 14 days and begins assessment "
                   "monitoring at that well.", BODY),
         Paragraph("7. Reporting", H2),
         Paragraph("Each event's evaluation is reported with the event's results: the background results used for each "
                   "indicator parameter, the upper prediction limits, each compliance well's results against them and the "
                   "wells to be resampled. Results are compared at the precision the laboratory reports.", BODY),
         KeepTogether([
             Paragraph("Revision history", H2),
             _table(["Rev.", "Date", "Description"], [
                 ["0", "July 2014", "Issued with the detection monitoring network"],
                 ["1", "December 2016", "Reissued with the post-closure plan application"],
                 ["2", "March 2018", "Revised for the post-closure care period; submitted under condition 9 of the "
                                     "plan approval"]], [0.5, 1.2, 4.8])]),
         KeepTogether([
             Paragraph("Approval", H2),
             _signatures([
                 ["Prepared", "%s, P.G., Hydrogeologist, Fieldstone Hydrogeology, LLC" % P["hydrogeologist"],
                  _sig(P["hydrogeologist"]), "16 March 2018"],
                 ["Reviewed", "%s, P.G., Principal Hydrogeologist, Fieldstone Hydrogeology, LLC" % P["principal"],
                  _sig(P["principal"]), "19 March 2018"],
                 ["Accepted", "%s, Environmental Programs Manager, for the District" % P["manager"],
                  _sig(P["manager"]), "21 March 2018"]]),
             Spacer(1, 6),
             Paragraph("Distribution: the Department, Waste and Materials Management Program; District file MCL-GW.",
                       SMALL)])]
    doc.build(f, canvasmaker=_furnished(("Kettle Prairie Solid Waste District  ·  Marten Creek Landfill",
                                         "Statistical Analysis Plan, Revision 2"), "MCL-GW-SAP Rev. 2, March 2018"))


def approval(path):
    doc = _doc(path, "Post-closure plan approval, Marten Creek Landfill")
    f = [Paragraph("Conditional Approval of the Post-Closure Plan", H1),
         Paragraph("Marten Creek Landfill, Kettle Prairie Solid Waste District", H2),
         Paragraph("Issued 11 September 2017 by the Department's Waste and Materials Management Program. The District "
                   "is the owner responsible for post-closure care for a period of 40 years from the date the final "
                   "cover was certified complete (30 June 2017).", SMALL),
         Paragraph("Conditions of approval (groundwater)", H2),
         _table(["No.", "Condition"], [
             ["7", "The owner shall monitor groundwater at the background and compliance wells shown in the approved plan, "
                   "and measure water levels at every monitoring point, in April and October of each year."],
             ["8", "Each monitoring event shall include the indicator parameters chloride, dissolved sodium and dissolved "
                   "boron, and the further parameters listed in Table 3 of the approved plan."],
             ["9", "The owner shall submit for approval a statistical analysis plan for detection monitoring that compares "
                   "each compliance well's indicator results with background water quality, and shall evaluate each "
                   "event under the approved plan within 30 days of receiving the laboratory's results."],
             ["10", "Where the evaluation shows an initial exceedance, the owner shall resample the well within 60 days of "
                    "the routine sample. A confirmed exceedance shall be reported to the Department within 14 days and "
                    "assessment monitoring shall begin at the well."],
             ["11", "Samples shall be collected and handled under a written sampling procedure that includes low-flow "
                    "purging and the stabilization of field parameters before a sample is collected."],
             ["12", "The owner shall submit an annual groundwater report by 1 March of each year."],
         ], [0.5, 5.9]),
         Spacer(1, 8),
         Paragraph("Failure to comply with a condition of this approval may result in enforcement under the state's solid "
                   "waste statutes. The owner may request a modification of a condition in writing.", SMALL)]
    doc.build(f)


def field_procedure(path):
    doc = _doc(path, "FS-03 Groundwater sampling, low-flow")
    P = W.PEOPLE
    f = [Paragraph("Fieldstone Hydrogeology, LLC", LH),
         Paragraph("FS-03 Groundwater Sampling by Low-Flow Purging", H1),
         _control([("Procedure", "FS-03, field standard operating procedure"),
                   ("Revision", "4, effective 15 February 2021"),
                   ("Supersedes", "Revision 3, June 2018"),
                   ("Applies to", "The firm's monitoring programs, including the Marten Creek Landfill"),
                   ("Owner", "Quality Assurance")]),
         Spacer(1, 4),
         Paragraph("1. Water levels", H2),
         Paragraph("Measure the depth to water at every well and piezometer in the program from the surveyed reference "
                   "point on the top of the casing, to the nearest 0.01 foot, before any well is purged on the first "
                   "day of an event.", BODY),
         Paragraph("2. Purging", H2),
         Paragraph("Purge with a bladder or peristaltic pump at 100 to 500 millilitres a minute, with the intake at the "
                   "middle of the screen, and keep drawdown under 0.3 foot. The purge volume of a well is the volume of "
                   "water pumped from that well from the start of purging until its sample is collected, taken from the "
                   "pump controller's volume counter. Rinse water run through the pump and tubing between wells is not "
                   "purge water.", BODY),
         Paragraph("3. Field readings and stabilization", H2),
         Paragraph("Pass the pump discharge through a flow-through cell and record a set of field readings about every "
                   "three to five minutes. Purging is complete when three consecutive sets agree within 3 per cent for "
                   "specific conductance, 0.1 unit for pH, 10 per cent for dissolved oxygen above 0.5 mg/L and 10 per "
                   "cent or 1 NTU for turbidity. Collect the sample immediately after the last of those sets; the field "
                   "readings reported with a sample are that set's. Record the meter's serial number with the first set "
                   "of each day and whenever the meter is changed.", BODY),
         Paragraph("4. Specific conductance", H2),
         Paragraph("Specific conductance is reported in microsiemens per centimetre at 25 degrees Celsius: the "
                   "conductivity of the sample corrected to 25 degrees Celsius with a temperature coefficient of 1.91 per "
                   "cent per degree. Calibrate the meter each morning with a standard of known specific "
                   "conductance.", BODY),
         Paragraph("5. Sample handling", H2),
         Paragraph("Fill the containers in the order volatile organics, semivolatile organics, metals (field filtered at "
                   "0.45 micrometres for dissolved metals), then the remaining parameters; keep samples at 4 degrees "
                   "Celsius and ship them to the laboratory under chain of custody the day they are collected.", BODY),
         KeepTogether([
             Paragraph("Revision history", H2),
             _table(["Rev.", "Date", "Description"], [
                 ["3", "June 2018", "Periodic review"],
                 ["4", "February 2021", "Periodic review; reissued on the firm's procedure template"]], [0.5, 1.2, 4.8]),
             Paragraph("Approval", H2),
             _signatures([
                 ["Prepared", "%s, P.G., Hydrogeologist" % P["hydrogeologist"], _sig(P["hydrogeologist"]),
                  "2 February 2021"],
                 ["Approved", "%s, Quality Assurance Manager" % P["qa_manager"], _sig(P["qa_manager"]),
                  "5 February 2021"],
                 ["Approved", "%s, P.G., Principal Hydrogeologist" % P["principal"], _sig(P["principal"]),
                  "8 February 2021"]])])]
    doc.build(f, canvasmaker=_furnished(("Fieldstone Hydrogeology, LLC", "Field Standard Operating Procedure FS-03"),
                                        "FS-03 Rev. 4, effective 15 February 2021. Uncontrolled when printed."))


def build(tgt, files):
    sap(os.path.join(tgt, files["sap"]))
    approval(os.path.join(tgt, files["approval"]))
    field_procedure(os.path.join(tgt, files["fieldproc"]))
