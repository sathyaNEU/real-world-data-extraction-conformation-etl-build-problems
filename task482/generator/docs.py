"""The pack's documents: draft Rule 18-4 (Printing and Converting Operations), the Department's information request of
12 January 2027, the Compliance Section's summary of the oxidizer performance test reports since 2017, and Cantrell Bend's
waste profile listing (all PDF)."""
from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors                                     # noqa: E402
from reportlab.lib.pagesizes import letter                           # noqa: E402
from reportlab.lib.styles import ParagraphStyle                      # noqa: E402
from reportlab.lib.units import inch                                 # noqa: E402
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W   # noqa: E402

BODY = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=13.6, spaceAfter=6)
SMALL = ParagraphStyle("sm", fontName="Times-Roman", fontSize=9.5, leading=12, spaceAfter=4)
HEAD = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10.5, leading=14, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=14, leading=18, spaceAfter=4)
SUB = ParagraphStyle("s", fontName="Helvetica", fontSize=9, leading=12, textColor=colors.HexColor("#444444"),
                     spaceAfter=10)
CELL = ParagraphStyle("c", fontName="Helvetica", fontSize=7.8, leading=9.4)
TH = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=7.6, leading=9.2)
ORG = "%s, %s" % (W.AGENCY, W.DIVISION)
GRID = TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 7.8), ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black),
                   ("LINEABOVE", (0, -1), (-1, -1), 0.4, colors.HexColor("#777777")),
                   ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2), ("TOPPADDING", (0, 0), (-1, -1), 1.8),
                   ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (2, 1), (-1, -1), "RIGHT")])


def _doc(path, title, org=ORG):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.85 * inch,
                          bottomMargin=0.85 * inch, title=title, author=org, creator=org, producer=org, subject=title)

    def frame(c, d_):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(0.9 * inch, 0.5 * inch, "%s  |  %s" % (org, title))
        c.drawRightString(letter[0] - 0.9 * inch, 0.5 * inch, "Page %d" % d_.page)
        c.restoreState()
    return d, frame


def write_rule(path):
    title = "Draft Rule 18-4, Printing and Converting Operations"
    d, frame = _doc(path, title)
    s = [Paragraph("%s (%s)" % (W.RULE, W.RULE_TITLE), TITLE),
         Paragraph("%s. Draft for the %s's meeting of 25 March 2027, as revised 19 February 2027. Applies in the %s."
                   % (ORG, W.COUNCIL, W.AREA), SUB),
         Paragraph("18-4-1 Purpose", HEAD),
         Paragraph("This rule limits the volatile organic compounds that printing and converting plants in the %s "
                   "emit, as part of the State's plan to bring the area into attainment of the 2015 ozone standard."
                   % W.AREA, BODY),
         Paragraph("18-4-2 Definitions", HEAD),
         Paragraph("(a) <i>VOC</i> (volatile organic compound) has the meaning in the Department's general rules: any "
                   "compound of carbon that participates in atmospheric photochemical reactions, other than carbon "
                   "monoxide, carbon dioxide, carbonic acid, metallic carbides or carbonates and ammonium carbonate, and "
                   "other than the compounds the federal definition lists as having negligible photochemical "
                   "reactivity, among them methane, ethane and acetone.", BODY),
         Paragraph("(b) <i>Press</i> means a printing press, laminator or coater, with its dryers and the ducts that "
                   "carry its exhaust.", BODY),
         Paragraph("(c) <i>Press material</i> means an ink, coating or adhesive applied on a press, and a press wash "
                   "solvent used on a press to clean its blankets, plates, cylinders or anilox rolls in place.", BODY),
         Paragraph("(d) <i>Cleaning material</i> means a solvent used away from a press: in an ink or adhesive "
                   "kitchen, to clean press parts, rolls, cylinders, sleeves, containers or mixing equipment, and the "
                   "solvent in a parts washer.", BODY),
         Paragraph("(e) <i>Capture system</i> means the enclosures, hoods and ducts that collect VOC from a press and "
                   "carry it to a control device; <i>control device</i> means an oxidizer or other equipment that "
                   "destroys or removes VOC from the air it receives.", BODY),
         Paragraph("(f) <i>Ton</i> means 2,000 pounds.", BODY),
         Paragraph("18-4-3 Applicability", HEAD),
         Paragraph("(a) A printing and converting plant in the area is subject to sections 18-4-4 and 18-4-6 from "
                   "1 July 2027 if the VOC emitted from its presses in calendar year 2026 was 25 tons or more.", BODY),
         Paragraph("(b) The VOC emitted from a plant's presses is the VOC in the press materials used on its presses, "
                   "less the VOC that the plant's capture systems and control devices destroyed.", BODY),
         Paragraph("(c) The Department lists the plants subject to this rule in Appendix A, adopted with the rule, "
                   "from its 2026 inventory of the area's printing and converting plants. A plant that becomes subject "
                   "remains subject.", BODY),
         Paragraph("18-4-4 Presses at a subject plant", HEAD),
         Paragraph("From 1 July 2027 a subject plant shall reduce the VOC from each press by at least 90 per cent "
                   "overall, by capture and control, or use only press materials of 2.0 pounds of VOC per gallon or "
                   "less, less water and exempt compounds, as applied.", BODY),
         Paragraph("18-4-5 Cleaning materials at every plant", HEAD),
         Paragraph("(a) From 1 July 2027 no plant in the area shall use a cleaning material of more than 3.5 pounds of "
                   "VOC per gallon, and every plant shall keep cleaning materials, and the rags and wipes used with "
                   "them, in closed containers.", BODY),
         Paragraph("(b) Every plant shall record, for each calendar year, the VOC from its cleaning materials: the VOC "
                   "in the cleaning materials issued for use away from its presses, less the VOC in spent cleaning "
                   "materials shipped off site for recycling or disposal, and, for each parts washer, the VOC in the "
                   "solvent its service vendor added less the VOC in the spent solvent the vendor removed. The first "
                   "record is for 2026, with the plant's return to the Department's information request.", BODY),
         Paragraph("18-4-6 Records and reports", HEAD),
         Paragraph("A subject plant shall keep daily records of each press material used on each press, with its "
                   "safety data sheet, and the operating records of its capture systems and control devices, for five "
                   "years, and shall report its press VOC for each calendar year by 1 April of the next.", BODY)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def write_letter(path):
    title = "Information request, printing and converting plants, 2026"
    d, frame = _doc(path, title)
    items = [
        ("Press material use", "Every press material used on each of your presses in 2026, as your production system "
         "logs it: by shift, or by job with the job's start and end, with the quantity and unit logged. Job records "
         "carry the quantity used on the job, net of material returned to the ink or adhesive room."),
        ("Safety data sheets", "The current safety data sheet for each press material and cleaning material you used, "
         "and the revision history of each sheet."),
        ("Capture", "Your most recent capture determination for each capture system: a permanent total enclosure "
         "verification under EPA Method 204, or a capture efficiency test."),
        ("Oxidizer", "Your oxidizer's 2026 hourly historian record (operating mode, combustion chamber temperature, "
         "and exhaust flow or fan speed, as the historian logs them, with its time stamps), every performance test "
         "report since 1 January 2017, and the carbon content of your VOC (pounds of carbon per pound of VOC) from "
         "your most recent solvent analysis."),
        ("Cleaning materials", "Your 2026 stores issues of cleaning materials, the manifests and waste profiles for "
         "waste shipped off site, and your parts washer service records."),
        ("Purchases and stock", "Your 2026 statements from your ink, coating and adhesive suppliers, and your physical "
         "stock counts of 1 January 2026 and 31 December 2026."),
    ]
    rows = [[Paragraph("<b>Item</b>", CELL), Paragraph("<b>What to return</b>", CELL)]]
    for a, b in items:
        rows.append([Paragraph(a, CELL), Paragraph(b, CELL)])
    t = Table(rows, colWidths=[1.4 * inch, 5.2 * inch], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    s = [Paragraph(W.AGENCY, TITLE),
         Paragraph("%s, %s. 12 January 2027." % (W.DIVISION, W.SECTION), SUB),
         Paragraph("To the operators of the fourteen printing and converting plants in the %s." % W.AREA, BODY),
         Paragraph("Re: Information request for draft %s (%s) and the 2026 inventory" % (W.RULE, W.RULE_TITLE), HEAD),
         Paragraph("The Department is preparing draft %s for the %s's meeting of 25 March 2027. The rule's "
                   "applicability list (Appendix A) and the area's 2026 inventory of printing and converting plants "
                   "will be built from the records each plant returns. Under the Department's information request "
                   "authority, please return the following for calendar year 2026, local (Central) time, by 12 February 2027, "
                   "in the layouts your own systems produce." % (W.RULE, W.COUNCIL), BODY),
         t, Spacer(1, 8),
         Paragraph("Thameside Laminating (facility 0117) has been Kelvedon Laminates (facility 0142) since its "
                   "acquisition on 1 May 2026. Kelvedon Laminates returns the whole year for the plant, its records "
                   "before 1 May under the former name and facility number.", BODY),
         Paragraph("The Department compiles the returns into the area files of its 2026 inventory: the press material "
                   "use, the oxidizer historians, the stores issues and the safety data sheet master across all "
                   "plants, with each plant's facility number as returned.", BODY),
         Paragraph("Questions on the rule to %s, Rule Development; on the returns to me." % W.PEOPLE["rules"], BODY),
         Spacer(1, 10),
         Paragraph("%s<br/>Emissions Inventory Lead" % W.PEOPLE["inventory"], BODY)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def test_figures(t):
    """A test's runs in its firm's basis: ppmv and lb/hr as propane or as carbon, and destruction per cent."""
    basis = W.FIRMS[t["firm"]][1]
    div = 3.0 if basis == "propane" else 1.0
    kk = W.K_PROPANE if basis == "propane" else W.K
    out = []
    for r in t["runs"]:
        ci, co = r["ci"] / div, r["co"] / div
        mi = r["ci"] * r["qi"] * 60 * kk
        mo = r["co"] * r["qo"] * 60 * kk
        out.append(dict(run=r["run"], start=r["start"], ci=round(ci, 1), co=round(co, 2), qi=int(round(r["qi"], -1)),
                        qo=int(round(r["qo"], -1)), mi=round(mi, 2), mo=round(mo, 3),
                        dre=round(100 * (1 - mo / mi), 2)))
    return out, basis


def write_tests(path, e):
    title = "Oxidizer performance tests, 2017 to 2026"
    d, frame = _doc(path, title, org="%s, Compliance Section" % W.DIVISION)
    s = [Paragraph("Oxidizer performance tests at the Kestle Valley printing and converting plants, 2017 to 2026", TITLE),
         Paragraph("%s, Compliance Section. The summary tables of each test report received, as the testing firm "
                   "reported them. Compiled 2 February 2027 for the 2026 inventory." % W.AGENCY, SUB),
         Paragraph("Each test is three runs of about an hour at the oxidizer's inlet and outlet, total hydrocarbon by "
                   "EPA Method 25A. Marlow Stack Testing reports concentrations and mass rates as propane; Prairieline "
                   "Source Evaluation reports them as carbon. Destruction is the testing firm's, from the inlet and "
                   "outlet mass rates.", BODY)]
    for t in sorted(e["tests"], key=lambda x: (x["plant"], x["date"])):
        p = W.BY[t["plant"]]
        runs, basis = test_figures(t)
        firm = W.FIRMS[t["firm"]][0]
        fac = p.get("old_fac") if t["plant"] == "KEL" else p["fac"]
        if t["note"]:
            prod = "maximum production, %s" % t["note"]
        else:
            prod = "maximum production (%d per cent of rated press capacity, all presses)" % int(round(
                100 * W.rng_for("prod", t["no"]).uniform(0.94, 0.99)))
        u = "as %s" % basis
        head = [Paragraph(x, TH) for x in ("Run", "Start", "Inlet VOC, ppmv %s" % u, "Outlet VOC, ppmv %s" % u,
                                           "Inlet flow, scfm", "Outlet flow, scfm", "Inlet, lb/hr %s" % u,
                                           "Outlet, lb/hr %s" % u, "Destruction, %")]
        rows = [head]
        for r in runs:
            rows.append([str(r["run"]), r["start"], "%.1f" % r["ci"], "%.2f" % r["co"], "{:,}".format(r["qi"]),
                         "{:,}".format(r["qo"]), "%.2f" % r["mi"], "%.3f" % r["mo"], "%.2f" % r["dre"]])
        avg = lambda k: sum(r[k] for r in runs) / 3.0
        rows.append(["Average", "", "%.1f" % avg("ci"), "%.2f" % avg("co"), "{:,}".format(int(round(avg("qi"), -1))),
                     "{:,}".format(int(round(avg("qo"), -1))), "%.2f" % avg("mi"), "%.3f" % avg("mo"),
                     "%.2f" % avg("dre")])
        tb = Table(rows, colWidths=[0.42 * inch, 0.45 * inch] + [0.78 * inch] * 7, hAlign="LEFT", repeatRows=1)
        tb.setStyle(GRID)
        block = [Paragraph("%s (facility %s), %s. Test of %s by %s, report %s. Production during the test: %s."
                           % (t["name"], fac, t["tag"], t["date"].strftime("%d %B %Y").lstrip("0"), firm, t["report"],
                              prod), SMALL), tb, Spacer(1, 8)]
        s.append(KeepTogether(block))
    d.build(s, onFirstPage=frame, onLaterPages=frame)
    return len(e["tests"])


def write_profiles(path, e):
    title = "Waste profiles, Kestle Valley printing plants"
    d, frame = _doc(path, title, org=W.HAULER)
    rows = [[Paragraph(x, TH) for x in ("Profile", "Generator", "Waste", "Generating process", "VOC, % by weight",
                                        "Waste codes", "Form")]]
    for x in e["ask_a"]["profiles"]:
        rows.append([x["profile"], Paragraph("%s (%s)" % (x["plant"], x["fac"]), CELL), Paragraph(x["waste"], CELL),
                     x["source"], "%.1f" % x["voc"], x["code"], Paragraph(x["form"], CELL)])
    tb = Table(rows, colWidths=[0.85 * inch, 1.35 * inch, 1.75 * inch, 0.95 * inch, 0.6 * inch, 0.8 * inch,
                                0.7 * inch], hAlign="LEFT", repeatRows=1)
    tb.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 7.6), ("LINEBELOW", (0, 0), (-1, 0), 0.6,
                                                                           colors.black),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
    s = [Paragraph("Approved waste profiles, 2026", TITLE),
         Paragraph("%s. Profiles approved for the Kestle Valley printing and converting accounts, with the VOC "
                   "content each plant's waste analysis reported. Issued 8 January 2027." % W.HAULER, SUB), tb]
    d.build(s, onFirstPage=frame, onLaterPages=frame)
    return len(e["ask_a"]["profiles"])
