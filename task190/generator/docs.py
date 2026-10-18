"""The pack's documents: the operation-code workbook and the four PDFs. No document states how an
estimate's sampling error is computed, and none ranks the eight streams on the decision question."""
import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                    # noqa: E402
from reportlab.lib.pagesizes import A4                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet  # noqa: E402
from reportlab.lib.units import mm                                  # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import pack                                                         # noqa: E402
import world as W                                                   # noqa: E402

NUMWORD = {6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}


def _long(iso):
    """a date as a division memo writes it"""
    d = dt.date.fromisoformat(iso)
    return "%d %s %d" % (d.day, ["January", "February", "March", "April", "May", "June", "July",
                                 "August", "September", "October", "November",
                                 "December"][d.month - 1], d.year)

SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Times-Roman", fontSize=9.5, leading=13)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Times-Bold", fontSize=13, leading=16, spaceAfter=6)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Times-Bold", fontSize=10.5, leading=14, spaceBefore=8, spaceAfter=4)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=11, textColor=colors.HexColor("#444444"))
GRID = TableStyle([("FONT", (0, 0), (-1, 0), "Times-Bold", 8.5), ("FONT", (0, 1), (-1, -1), "Times-Roman", 8.5),
                   ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                   ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")),
                   ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2),
                   ("BOTTOMPADDING", (0, 0), (-1, -1), 2)])


def _doc(path, title):
    return SimpleDocTemplate(path, pagesize=A4, title=title, author="", subject="", creator="",
                             leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm, bottomMargin=20 * mm)


def plan_targets(path, targets):
    d = _doc(path, "Plano Nacional de Gestao de Residuos 2024-2030, quadro de metas")
    f = [Paragraph("%s" % W.PLAN, H1),
         Paragraph("Annex II, Table 4: recovery targets for business waste by statistical stream",
                   H2),
         Paragraph("The targets in this table are the recovery rates each statistical waste stream "
                   "is to reach in the reference year shown. They are fixed for the life of the plan "
                   "and are not revised between reference years. The stream definitions are those of "
                   "the waste statistics regulation and are set out in Annex I.", BODY),
         Spacer(1, 5)]
    rows = [["Statistical stream", "2026 target", "2028 target", "2030 target"]]
    for k, name, _p, _m, _c in W.STREAMS:
        t26 = targets[k] * 100.0
        rows.append([name, "%.1f per cent" % t26, "%.1f per cent" % (t26 + 3.5), "%.1f per cent" % (t26 + 7.0)])
    t = Table(rows, colWidths=[78 * mm, 29 * mm, 29 * mm, 29 * mm])
    t.setStyle(GRID)
    f.append(t)
    f.append(Spacer(1, 6))
    f.append(Paragraph("Attainment against these targets is reported annually by the %s in the "
                       "official waste statistics. The plan does not prescribe the form of that "
                       "report." % W.INSTITUTE, BODY))
    f.append(Spacer(1, 10))
    f.append(Paragraph("Approved 14 December 2023. Source: Diario da Republica, 1st series. "
                       "Reproduced under the open licence for public-sector information.", SMALL))
    d.build(f)


def sample_design(path, issued, resp):
    d = _doc(path, "Business Waste Survey 2026, sample design and weighting")
    f = [Paragraph("%s: sample design and weighting, 2026 round" % W.SURVEY, H1),
         Paragraph("1. Scope and frame", H2),
         Paragraph("The survey covers enterprises on the business register in the activity classes "
                   "listed in Annex A. The 2026 frame holds 36,735 such enterprises. The survey "
                   "collects the tonnage of waste arising at the enterprise during the reference "
                   "year, by statistical stream, whether that waste is treated on site or moved "
                   "off site.", BODY),
         Paragraph("2. Stratification and allocation", H2),
         Paragraph("The frame is stratified by employment size band. The 250-or-more band is "
                   "enumerated completely: every enterprise in it receives a questionnaire and "
                   "response is compulsory under article 11 of the statistics act, and the 2026 "
                   "round closed with a return from each of them. The three smaller bands are "
                   "sampled by simple random selection without replacement within the band, and "
                   "response in them is voluntary.", BODY),
         Spacer(1, 4)]
    rows = [["Stratum", "Size band", "Frame N", "Issued", "Out of scope", "Usable returns", "Design weight"]]
    w = [N / float(r) for _c, _l, N, r in W.STRATA]
    for i, (code, label, N, r) in enumerate(W.STRATA):
        rows.append([code, label, "%d" % N, "%d" % issued[code], "%d" % W.OUT_OF_SCOPE[code],
                     "%d" % r, "%.6f" % w[i]])
    t = Table(rows, colWidths=[14 * mm, 38 * mm, 19 * mm, 17 * mm, 21 * mm, 24 * mm, 24 * mm])
    t.setStyle(GRID)
    f += [t, Spacer(1, 5),
          Paragraph("3. Weighting", H2),
          Paragraph("Each usable return carries the design weight shown, the frame size of its "
                    "stratum over the number of usable returns in that stratum. The weight is "
                    "supplied on the micro-data file in the column design_weight. No calibration "
                    "or post-stratification is applied to the 2026 round.", BODY),
          Paragraph("4. Micro-data file", H2),
          Paragraph("bws_2026_microdata.csv holds one record per usable return. The arisings "
                    "columns carry the tonnage reported for each statistical stream, and a zero "
                    "where the enterprise reported that it produced none of that stream. Under "
                    "article 19 of the statistics act the released file identifies a record by its "
                    "survey record number only: it carries no business register number, no permit "
                    "number, no name, no address and no region, so a record cannot be traced to a "
                    "named enterprise.", BODY),
          Paragraph("5. Collection operations", H2),
          Paragraph("bws_2026_response_log.csv records the division's contacts with each issued "
                    "enterprise under the collection case opened for it, with the field days "
                    "attributed to the contact. Field work is organised by regional team. The "
                    "division books field work in field days of %s hours, and a team records the "
                    "time a contact took in the unit shown in the log's time_unit column."
                    % NUMWORD[W.FIELD_DAY_HOURS], BODY),
          Spacer(1, 10),
          Paragraph("%s, Business and Environment Statistics Division. Issued %s."
                    % (W.INSTITUTE, W.EXTRACT_SURVEY), SMALL)]
    d.build(f)


def release_2025(path, cv_2025, nat_total, prior):
    d = _doc(path, "Estatisticas dos residuos 2025, versao revista")
    f = [Paragraph("Business waste statistics, reference year 2025", H1),
         Paragraph("Revised release, 30 September 2026. This release supersedes the preliminary "
                   "release of 31 March 2026 in full.", BODY),
         Paragraph("Table 1: recovery rate by statistical stream, 2025", H2)]
    rows = [["Statistical stream", "Arisings (t)", "Recovered (t)", "Recovery rate"]]
    for k, name, _p, _m, _c in W.STREAMS:
        a, r = prior[k]
        rows.append([name, "%d" % a, "%d" % r, "%.1f per cent" % (100.0 * r / a)])
    t = Table(rows, colWidths=[78 * mm, 29 * mm, 29 * mm, 29 * mm])
    t.setStyle(GRID)
    f += [t, Spacer(1, 5),
          Paragraph("Table 2: arisings by activity class, 2025", H2),
          Paragraph("Table 2 is published in the accompanying data file and is not reproduced here.", BODY),
          Paragraph("Methodological note", H2),
          Paragraph("The arisings estimates are produced from the %s. Total business waste arising "
                    "in 2025 is estimated at %s tonnes, and the coefficient of variation of that "
                    "estimated national total in the 2025 round is %.1f per cent. Precision "
                    "measures for the activity class breakdown, which is the survey's publication "
                    "domain, are given in the quality report; the statistical stream breakdown is "
                    "published without them."
                    % (W.SURVEY, "{:,}".format(sum(a for a, _r in prior.values())), cv_2025 * 100),
                    BODY),
          Paragraph("Recovered tonnage is taken from the %s and covers movements of controlled "
                    "waste only. Waste treated on the producer's own site does not appear in the "
                    "register and is estimated from the survey alone. The register column in "
                    "Table 1 is as extracted on %s, the extract this release was compiled from. "
                    "The register goes on receiving treatment confirmations for consignments "
                    "despatched in earlier reference years, and the published series is not "
                    "revised for them." % (W.REGISTER, _long(W.PRIOR_EXTRACT)), BODY),
          Spacer(1, 10),
          Paragraph("%s. Reproduced under the open licence for public-sector information."
                    % W.INSTITUTE, SMALL)]
    d.build(f)


def capacity_note(path, targets):
    """The head of collection operations' memo to the division director. It is the division's own
    note: what the establishment leaves for 2027, why the choice cannot wait, and the quantity the
    division commits to measuring. It states no method and ranks no stream."""
    d = _doc(path, "Collection capacity, 2027 round")
    p = W.PEOPLE
    f = [Paragraph("Memorandum", H1),
         Spacer(1, 2)]
    head = [["To", "%s, Division Director" % p["division_director"]],
            ["From", "%s, Head of Collection Operations" % p["head_collection"]],
            ["Date", _long(W.NOTE_DATE)],
            ["Subject", "2027 collection capacity, and where the supplementary module goes"]]
    t = Table(head, colWidths=[18 * mm, 148 * mm])
    t.setStyle(TableStyle([("FONT", (0, 0), (0, -1), "Times-Bold", 9.5),
                           ("FONT", (1, 0), (1, -1), "Times-Roman", 9.5),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 1),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.6, colors.HexColor("#999999"))]))
    f += [t, Spacer(1, 7),
          Paragraph("We go into 2027 with the five regional teams at their 2026 complement. Once "
                    "the core rounds are covered the establishment leaves room for one "
                    "supplementary module of %d field days, and I would attach it to the %s "
                    "collection round. One module is what there is: a second would come out of "
                    "field days the core rounds need." % (W.MODULE_DAYS, W.SURVEY), BODY),
          Spacer(1, 4),
          Paragraph("What makes the choice urgent is the Council. The %s wrote to us on %s about "
                    "the statistical stream figures in the waste statistics, and the complaints "
                    "procedure has us answering substantively by %s. My answer is the module: it "
                    "is committed to the one stream where the 2026 attainment figures establish a "
                    "shortfall against the plan, and it goes back to the enterprises whose "
                    "arisings make that stream up to collect the reasons for it."
                    % (W.COUNCIL, _long(W.COMPLAINT_DATE), _long(W.RESPONSE_DUE)), BODY),
          Spacer(1, 4),
          Paragraph("So that we are all measuring the same thing, the quantity is this. For the "
                    "2026 reference year a stream's recovery rate is the tonnage of that stream "
                    "despatched by its producer during the 2026 calendar year and confirmed "
                    "received at a recovery operation, counted once at the producer's despatch "
                    "leg, over the total tonnage of that stream arising during 2026 at every "
                    "enterprise in the %s frame whether sampled or not, as estimated from the 2026 "
                    "survey. A stream is established below target where its 2026 recovery rate is "
                    "below its %s target at the 95 per cent level. The module goes to the one "
                    "stream so established." % (W.SURVEY, W.PLAN), BODY),
          Spacer(1, 4),
          Paragraph("The figures come off the extracts we hold: the register extract of %s, which "
                    "carries every leg of a consignment despatched in the reference year, and the "
                    "2026 survey round as at %s. The agency moved system in July and reissued both "
                    "the operation-code list and the waste code list on %s; its own mappings came "
                    "with the extract." % (_long(W.EXTRACT_REGISTER), _long(W.EXTRACT_SURVEY),
                                           _long(W.CODE_REVISION)), BODY),
          Spacer(1, 4),
          Paragraph("Two other things for the release while I have your attention. The mid-term "
                    "review quotes the prior reference year's recovered tonnage, and we take that "
                    "out of the register on the same basis as 2026. The municipal series goes out "
                    "beside this one: it carries the tonnage the municipalities return as "
                    "collected, each municipality's collected tonnage counted once, against what "
                    "the licensed facilities record receiving.", BODY),
          Spacer(1, 6),
          Paragraph("The table is what the 2027 plan allows each team against its establishment. "
                    "These are plan figures and not the 2026 outturn: the outturn is in the "
                    "collection operations log.", BODY),
          Spacer(1, 4)]
    rows = [["Regional team", "Establishment (FTE)", "Core rounds (field days)"]]
    est = {"Norte": 3.0, "Centro": 2.0, "Lisboa": 2.5, "Alentejo": 1.0, "Algarve": 1.0}
    core = {"Norte": 214, "Centro": 143, "Lisboa": 178, "Alentejo": 71, "Algarve": 69}
    for r in W.REGIONS:
        rows.append(["EQ-%s (%s)" % (r[:3].upper(), r), "%.1f" % est[r], "%d" % core[r]])
    t = Table(rows, colWidths=[72 * mm, 40 * mm, 48 * mm])
    t.setStyle(GRID)
    f += [t, Spacer(1, 10),
          Paragraph("%s, Business and Environment Statistics Division. Our reference "
                    "DEA/2027/014. Register queries go to %s at the %s."
                    % (W.INSTITUTE, p["register_liaison"], W.AGENCY), SMALL)]
    d.build(f)


def operation_codes(path):
    """The agency's treatment operation list, with the 1 July 2026 revision."""
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Operation codes"
    hdr = ["operation_code", "operation_kind", "description", "valid_from", "valid_to", "replaces"]
    ws.append(hdr)
    for c in ws[1]:
        c.font = Font(bold=True)
    for code, kind, desc in pack.OPS:
        ws.append([code, kind, desc, "2014-01-01", "", ""])
    ws2 = wb.create_sheet("Waste code revision")
    ws2.append(["superseded_code", "replacement_code", "effective_from"])
    for c in ws2[1]:
        c.font = Font(bold=True)
    for key in pack.CODES:
        for base, repl in pack.CODES[key]:
            if repl:
                ws2.append([base, repl, W.CODE_REVISION])
    ws3 = wb.create_sheet("Notes")
    for line in ["%s, treatment operation list." % W.AGENCY,
                 "operation_kind distinguishes a recovery operation, a disposal operation and an",
                 "interim operation. An interim operation is storage pending a later operation; the",
                 "later operation is confirmed on the consignment the holding site forwards.",
                 "The list was reissued on %s with the waste code revision on the second sheet." % W.CODE_REVISION]:
        ws3.append([line])
    for ws_ in (ws, ws2, ws3):
        for col, wd in zip("ABCDEF", (18, 16, 62, 14, 12, 12)):
            ws_.column_dimensions[col].width = wd
    wb.save(path)
