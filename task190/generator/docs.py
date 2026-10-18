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
                    "attributed to the contact. Field work is organised by regional team.", BODY),
          Spacer(1, 10),
          Paragraph("%s, Business and Environment Statistics Division. Issued %s."
                    % (W.INSTITUTE, W.EXTRACT_SURVEY), SMALL)]
    d.build(f)


def release_2025(path, nat_cv, nat_total, prior):
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
          Paragraph("The arisings estimates are produced from the %s. The coefficient of variation "
                    "of the estimated national total of business waste arising is 3.9 per cent for "
                    "the 2026 round and 4.1 per cent for 2025. Precision measures for the activity "
                    "class breakdown, which is the survey's publication domain, are given in the "
                    "quality report; the statistical stream breakdown is published without them."
                    % W.SURVEY, BODY),
          Paragraph("Recovered tonnage is taken from the %s and covers movements of controlled "
                    "waste only. Waste treated on the producer's own site does not appear in the "
                    "register and is estimated from the survey alone." % W.REGISTER, BODY),
          Spacer(1, 10),
          Paragraph("%s. Reproduced under the open licence for public-sector information."
                    % W.INSTITUTE, SMALL)]
    d.build(f)


def capacity_note(path, targets):
    d = _doc(path, "Collection capacity, 2027 round")
    p = W.PEOPLE
    f = [Paragraph("Collection capacity note, 2027 round", H1),
         Paragraph("Business and Environment Statistics Division. Prepared for the division "
                   "director's weekly review.", BODY),
         Paragraph("1. Capacity for 2027", H2),
         Paragraph("The division's field establishment for 2027 is five regional teams at the 2026 "
                   "complement. After the core rounds the establishment leaves room for one "
                   "supplementary module of 46 field days, to be attached to the %s collection "
                   "round. One module only: a second would take field days the core rounds need."
                   % W.SURVEY, BODY),
         Paragraph("2. What forces the choice now", H2),
         Paragraph("The %s wrote to the institute on %s about the statistical stream figures in "
                   "the waste statistics, and the institute's complaints procedure requires a "
                   "substantive answer by %s. The division's answer is the module: it is committed "
                   "to the one stream where the 2026 attainment figures establish a shortfall "
                   "against the plan, and the module collects the reasons for that shortfall from "
                   "the enterprises whose arisings make it up."
                   % (W.COUNCIL, W.COMPLAINT_DATE, W.RESPONSE_DUE), BODY),
         Paragraph("3. The quantity the choice runs on", H2),
         Paragraph("For the 2026 reference year a stream's recovery rate is the tonnage of that "
                   "stream despatched by its producer during the 2026 calendar year and confirmed "
                   "received at a recovery operation, counted once at the producer's despatch leg, "
                   "over the total tonnage of that stream arising during 2026 at every enterprise "
                   "in the %s frame whether sampled or not, as estimated from the 2026 survey. A "
                   "stream is established below target where its 2026 recovery rate is below its "
                   "%s target at the 95 per cent level. The module goes to the one stream so "
                   "established." % (W.SURVEY, W.PLAN), BODY),
         Paragraph("4. Sources as at the extract dates", H2),
         Paragraph("The register extract is as at %s and covers every leg of a consignment "
                   "despatched in the reference year. The survey file is the 2026 round as at %s. "
                   "The agency's operation-code list was revised on %s and the waste code list on "
                   "the same date; the agency's own mappings ship with the extract."
                   % (W.EXTRACT_REGISTER, W.EXTRACT_SURVEY, W.CODE_REVISION), BODY),
         Paragraph("5. Field days by team, 2026 round", H2)]
    rows = [["Regional team", "Establishment (FTE)", "Core rounds (field days)"]]
    est = {"Norte": 3.0, "Centro": 2.0, "Lisboa": 2.5, "Alentejo": 1.0, "Algarve": 1.0}
    core = {"Norte": 214, "Centro": 143, "Lisboa": 178, "Alentejo": 71, "Algarve": 69}
    for r in W.REGIONS:
        rows.append(["EQ-%s (%s)" % (r[:3].upper(), r), "%.1f" % est[r], "%d" % core[r]])
    t = Table(rows, colWidths=[72 * mm, 40 * mm, 48 * mm])
    t.setStyle(GRID)
    f += [t, Spacer(1, 5),
          Paragraph("The core-round figures are the 2027 plan, not the 2026 outturn; the 2026 "
                    "outturn is in the collection operations log.", BODY),
          Spacer(1, 8),
          Paragraph("Prepared by %s, Head of Collection Operations. For %s, Division Director. "
                    "Register queries to %s at the %s."
                    % (p["head_collection"], p["division_director"], p["register_liaison"], W.AGENCY), SMALL)]
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
