"""The pack's documents: the Implant Value Analysis Policy (VA-07), the registry's data dictionary, Schedule B of the
2022 to 2027 hip agreement, the registry's data-management log and the export manifest."""
from __future__ import annotations

import csv
import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from openpyxl import Workbook                                                       # noqa: E402
from openpyxl.styles import Alignment, Font                                          # noqa: E402
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import letter                                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import mm                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle      # noqa: E402

import common as K   # noqa: E402
import records as R  # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1d2326"), colors.HexColor("#5b646b"), colors.HexColor("#b7bec4")


def styles(font, accent):
    body = ParagraphStyle("b", fontName=font, fontSize=9.6, leading=13.4, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=font + "-B", fontSize=14, leading=18, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=font + "-B", fontSize=10.4, leading=14, textColor=INK, spaceBefore=7,
                          spaceAfter=2),
        meta=ParagraphStyle("m", fontName=font, fontSize=8.3, leading=11.2, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName=font, fontSize=8.3, leading=10.4, textColor=INK),
        cellb=ParagraphStyle("cb", fontName=font + "-B", fontSize=8.3, leading=10.4, textColor=INK),
        clause=ParagraphStyle("p", parent=body, leftIndent=22, firstLineIndent=-22))


def _frame(left, right, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 7.4)
        canvas.drawString(19 * mm, letter[1] - 11.5 * mm, left)
        canvas.drawRightString(letter[0] - 19 * mm, letter[1] - 11.5 * mm, right)
        canvas.drawRightString(letter[0] - 19 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=19 * mm, rightMargin=19 * mm, topMargin=20 * mm,
                             bottomMargin=17 * mm, title=title, author=author, subject="", creator="", producer="")


# ---------------------------------------------------------------------------------------------- the policy
def write_policy(path):
    S = styles("Serif", colors.HexColor("#1f4e79"))
    doc = _doc(path, "Implant Value Analysis Policy (VA-07)", K.SYSTEM)
    st = [Paragraph("Brennick Valley Health: Implant Value Analysis Policy", S["h1"]),
          Paragraph("Policy VA-07, revision 3. Owner: %s, Director of Value Analysis, Supply Chain. Approved by the "
                    "Value Analysis Committee on 11 February 2025; effective 1 March 2025. Replaces revision 2 "
                    "(April 2021)." % K.PEOPLE["value"], S["meta"])]
    P = lambda t: st.append(Paragraph(t, S["body"]))
    C = lambda n, t: st.append(Paragraph("%s&nbsp;&nbsp;%s" % (n, t), S["clause"]))
    st.append(Paragraph("1. Purpose", S["h2"]))
    P("This policy sets how Brennick Valley Health decides which implantable products are bought under system "
      "purchasing agreements for Brennick Valley Medical Center, Tollefson Lake Hospital and Kittelstad Orthopaedic "
      "Hospital, so that the products surgeons use are chosen on evidence of how they perform and on what they cost.")
    st.append(Paragraph("2. Scope", S["h2"]))
    P("The policy applies to implants on system agreements for hip and knee replacement, spine, trauma and sports "
      "medicine. Products used under a research protocol, and devices bought for a single named patient under the "
      "exception process (VA-11), are outside it. Revision 3 adds section 4, the evidence the committee uses for hip "
      "constructs at each renewal of the hip agreement.")
    st.append(Paragraph("3. The Value Analysis Committee", S["h2"]))
    P("The committee is chaired by the Director of Value Analysis and has surgeon members from each hospital, the "
      "perioperative nursing directors, a representative of Finance and the manager of the Brennick Valley Joint "
      "Registry. It reviews each agreement in the six months before it renews. Supply Chain provides use and spend for "
      "the agreement's products; the orthopaedic outcomes team provides the clinical evidence.")
    st.append(Paragraph("4. Hip constructs", S["h2"]))
    C("4.1", "A hip construct is one femoral stem family used with one acetabular cup family, whatever the sizes, "
             "femoral heads and liners used with them.")
    C("4.2", "At each renewal of the system's hip agreement a construct stays on the agreement only if its cumulative "
             "percent revision ten years after the operation is 5.0 per cent or less.")
    C("4.3", "The cumulative percent revision is estimated by Kaplan-Meier on the Brennick Valley Joint Registry for "
             "every primary total hip operation with the construct at a system hospital on the registry, the unit "
             "being the hip. A revision is any later operation on that hip that adds, removes or replaces a component, "
             "and only the first revision of a hip counts. Deaths and loss to follow-up are censored.")
    C("4.4", "The committee uses the registry extract taken at the end of the calendar year before the renewal, and "
             "the estimate is reported as a percentage to one decimal place.")
    C("4.5", "A construct that does not meet 4.2 comes off the agreement for primary operations at the renewal. Its "
             "components stay available under the agreement's revision schedule for patients who already have it.")
    st.append(Paragraph("5. Knees, spine, trauma and sports medicine", S["h2"]))
    P("For these categories the committee weighs registry or published evidence case by case under section 6 of "
      "revision 2, which continues to apply to them.")
    st.append(Paragraph("6. Records", S["h2"]))
    P("The committee's minutes record each decision, the evidence it relied on and the vote. Supply Chain keeps the "
      "evidence packs for ten years.")
    doc.build(st, onFirstPage=_frame(K.SYSTEM, "Policy VA-07", "Serif"), onLaterPages=_frame(K.SYSTEM, "Policy VA-07", "Serif"))


# ---------------------------------------------------------------------------------------------- the dictionary
def write_dictionary(path):
    S = styles("Sans", colors.HexColor("#2f5d50"))
    doc = _doc(path, "Brennick Valley Joint Registry: data dictionary", K.PEOPLE["registry"])
    st = [Paragraph("Brennick Valley Joint Registry: data dictionary for the annual extract", S["h1"]),
          Paragraph("Version 4.2, January 2027. Prepared by %s, Registry Manager. Covers the extract of 31 December "
                    "2026." % K.PEOPLE["registry"], S["meta"])]
    P = lambda t: st.append(Paragraph(t, S["body"]))
    st.append(Paragraph("1. What the registry holds", S["h2"]))
    P("The registry records primary total hip replacements done at Brennick Valley Medical Center (BVMC), Tollefson "
      "Lake Hospital (TLH) and Kittelstad Orthopaedic Hospital (KOH), the later revisions of those hips, and the deaths "
      "and moves of the patients who have them.")
    P("From 1 January 2018 the registry captures each primary total hip operation at the three hospitals at the time "
      "of surgery from the surgeon's registry form. An operation whose form was not returned is not on the registry.")
    P("Hips replaced at the three hospitals from 1 January 2005 to 31 December 2017 were entered when the patient "
      "first attended a registry clinic, between 2018 and 2021: the clinic abstracted the operation and the components "
      "from the operative record. Legacy enrolment ran at Tollefson Lake in 2018 and 2019, at BVMC in 2019 and 2020 and "
      "at Kittelstad from July 2020 to December 2021, and closed on 31 December 2021.")
    P("Revisions of registry hips are recorded from the registry form when the revision is at one of the three "
      "hospitals, and from the quarterly linkage with the state's hospital discharge data when it is at another "
      "Wisconsin hospital. Deaths come from the Wisconsin death index linkage. The linkage covers Wisconsin hospitals "
      "and Wisconsin deaths only, so the registry loses follow-up of a hip when its patient moves out of the state, "
      "dated by the first address outside Wisconsin in the health record's address history (left_wisconsin_on).")
    st.append(Paragraph("2. Files in the extract", S["h2"]))
    rows = [["File", "One row per", "Fields"],
            [K.FILES["prosp"], "hip captured from 1 January 2018",
             "registry_hip_id, registry_patient_id, hospital_code, hospital_mrn, operation_date, side, "
             "stem_catalogue_no, cup_catalogue_no, head_diameter_mm, bearing, approach, surgeon_id, age_at_operation, "
             "sex, asa_grade, primary_diagnosis"],
            [K.FILES["legacy"], "hip entered at legacy enrolment",
             "Registry hip ID, Registry patient ID, Hospital, MRN, Side, Date of operation (month/day/year as abstracted), "
             "Stem and Cup catalogue no., Head (mm), Bearing, Approach, Surgeon, Age at operation, Sex, Enrolled on "
             "(the date of the clinic visit at which the hip was entered), Clinic, Abstracted by, Notes"],
            [K.FILES["revisions"], "revision of a registry hip",
             "revision_id, registry_hip_id, revision_date, revision_number (1 for the hip's first revision, 2 for the "
             "next), hospital_code (OTH: another Wisconsin hospital), components_changed, reason, source"],
            [K.FILES["deaths"], "registry patient who has died",
             "registry_patient_id, date_of_death (YYYY-MM-DD, or YYYY-MM where the certificate in the linkage gives "
             "the month only), linkage_match, linkage_run"],
            [K.FILES["status"], "registry patient",
             "registry_patient_id, residence_state, left_wisconsin_on (the first date the address history shows a "
             "home outside Wisconsin), address_source, last_verified"],
            [K.FILES["crosswalk"], "catalogue number",
             "Maker, Family, Component, Fixation, Size, Catalogue no., Catalogue no. before 1 July 2020 (Thorvik "
             "renumbered its hip catalogue on 1 July 2020; both numbers appear in the registry)"],
            [K.FILES["visits"], "registry clinic visit",
             "visit_id, registry_hip_id, clinic, visit_date, visit_type, radiograph, harris_hip_score"]]
    st.append(_table(S, rows, [64, 28, 86]))
    st.append(Paragraph("3. Codes", S["h2"]))
    P("Hospitals: BVMC, TLH, KOH. Side: R, L (Right, Left in the legacy workbook). Bearing: CoP ceramic on "
      "polyethylene, MoP metal on polyethylene, CoC ceramic on ceramic. Components changed at revision: Head and "
      "liner, Cup, Stem, All components. Revision source: Registry form, State discharge data.")
    P("hospital_mrn and MRN are the patient's medical record number at the operating hospital. Brennick Valley Medical "
      "Center and Tollefson Lake have always used system numbers, which begin E; Kittelstad numbers begin KO until "
      "Kittelstad moved to the system health record on 4 March 2024, and are system numbers from then. registry_patient_id is the registry's own number for the patient and is the same in "
      "every file; registry_hip_id is the same in every file for the hip.")
    st.append(Paragraph("4. Grain", S["h2"]))
    P("Each hip is one row in either the prospective export or the legacy workbook, never both. A patient with both "
      "hips replaced has two hip rows. A hip can have more than one revision row.")
    doc.build(st, onFirstPage=_frame(K.REGISTRY, "Data dictionary v4.2", "Sans"),
              onLaterPages=_frame(K.REGISTRY, "Data dictionary v4.2", "Sans"))


# ---------------------------------------------------------------------------------------------- Schedule B
PRICES = {"TA": 4385, "TS": 4910, "MF": 3640, "VS": 4290, "MS": 4475, "BP": 4120}


def write_schedule(path):
    S = styles("Serif", colors.HexColor("#4a3b2a"))
    doc = _doc(path, "Hip agreement 2022 to 2027: Schedule B", K.SYSTEM)
    st = [Paragraph("Hip Agreement 2022 to 2027, Schedule B: construct and component pricing", S["h1"]),
          Paragraph("Brennick Valley Health and the suppliers named below. Agreement term 1 July 2022 to 30 June 2027. "
                    "Prices in US dollars, delivered, consignment basis. Schedule B as amended 1 July 2025.", S["meta"])]
    P = lambda t: st.append(Paragraph(t, S["body"]))
    P("A construct price covers one femoral stem, one acetabular shell, one liner and one femoral head of the "
      "construct's families, any size, for a primary total hip. Screws, cement and ceramic-on-ceramic upgrades are "
      "billed at the component prices in Part 2. Construct prices for a stem and a shell from two suppliers are the "
      "sum of each supplier's construct share in Part 1.")
    rows = [["Construct", "Stem supplier", "Shell supplier", "Construct price (USD)", "Price from 1 July 2025 (USD)"]]
    for code, s, c in K.CONSTRUCTS:
        p = PRICES[code]
        rows.append([K.CNAME[code], K.MAKERS[K.FAM[s][2]], K.MAKERS[K.FAM[c][2]], "{:,}".format(p),
                     "{:,}".format(int(round(p * 1.021, -1)))])
    st.append(Paragraph("Part 1. Construct prices", S["h2"]))
    st.append(_table(S, rows, [34, 36, 36, 34, 36], right=(3, 4)))
    st.append(Paragraph("Part 2. Component prices", S["h2"]))
    rows = [["Item", "Price (USD)"], ["Cancellous bone screw, each", "118"], ["Bone cement, 40 g", "96"],
            ["Ceramic-on-ceramic upgrade (liner and head)", "640"], ["Dual-mobility liner upgrade", "715"],
            ["Revision stem (Holbrin revision, any length)", "3,960"], ["Multihole revision shell (Pellvoro)", "1,880"]]
    st.append(_table(S, rows, [120, 40], right=(1,)))
    st.append(Paragraph("Part 3. Rebates", S["h2"]))
    P("Each supplier credits 2.0 per cent of its construct revenue for the agreement year if the system's primary "
      "total hips with its constructs reach the volume in its tier letter, credited within 60 days of the agreement "
      "year's end.")
    doc.build(st, onFirstPage=_frame(K.SYSTEM, "Hip agreement Schedule B", "Serif"),
              onLaterPages=_frame(K.SYSTEM, "Hip agreement Schedule B", "Serif"))


# ---------------------------------------------------------------------------------------------- the operations log
def write_log(path, T):
    wb = Workbook()
    ws = wb.active
    ws.title = "Log"
    ws.append(["Registry data-management log. What was done to the registry's data and when; not a record of "
               "outcomes. Owner: %s. Version 2026.4, refreshed 25 January 2027." % K.PEOPLE["registry"]])
    ws["A1"].font = Font(italic=True)
    ws.append([])
    ws.append(["Date", "Entry", "Detail", "By"])
    for c in ws[3]:
        c.font = Font(bold=True)
    for col, w in zip("ABCD", (12, 28, 96, 8)):
        ws.column_dimensions[col].width = w
    for d, e, detail, by in log_entries(T):
        ws.append([d, e, detail, by])
        ws.cell(ws.max_row, 1).number_format = "yyyy-mm-dd"
        ws.cell(ws.max_row, 3).alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


def log_entries(T):
    E = []
    E.append((dt.date(2018, 1, 1), "Registry start", "Prospective capture begins at BVMC, TLH and KOH: registry form "
              "completed in theatre for every primary total hip.", "MB"))
    for h in K.HOSP:
        a, b = K.CLINIC[h]
        E.append((a, "Legacy enrolment", "%s registry clinic opens for legacy enrolment (hips replaced 2005 to 2017)."
                  % K.HOSP_NAME[h], "MB"))
        E.append((b, "Legacy enrolment", "%s registry clinic: last legacy enrolment session." % K.HOSP_NAME[h], "MB"))
    E.append((K.PAUSE[0], "Clinics", "All registry clinics suspended (COVID-19). Prospective capture continues.", "MB"))
    E.append((K.PAUSE[1] + dt.timedelta(days=3), "Clinics", "Registry clinics resume at BVMC.", "MB"))
    E.append((dt.date(2020, 7, 9), "Crosswalk", "Thorvik catalogue renumbering effective 1 July 2020 added to the "
              "component crosswalk; forms from 1 July carry the new numbers.", "KL"))
    E.append((dt.date(2021, 12, 31), "Legacy enrolment", "Legacy enrolment closed.", "MB"))
    E.append((dt.date(2024, 3, 4), "Identifiers", "Kittelstad moves to the system health record; Kittelstad MRNs (KO) "
              "replaced by system MRNs on new forms.", "TD"))
    # quarterly discharge-data linkage runs and the death-index runs, counted from the shipped files
    q, runs = {}, {}
    for r in T["revisions"]:
        if r["source"] == "State discharge data":
            k = (r["date"].year, (r["date"].month - 1) // 3 + 1)
            q[k] = q.get(k, 0) + 1
    for y in range(2018, 2027):
        for qq in range(1, 5):
            run = dt.date(y + (1 if qq == 4 else 0), {1: 5, 2: 8, 3: 11, 4: 1}[qq], 4 + (y * 13 + qq * 7) % 15)
            runs[(y, qq)] = run
            E.append((run, "Linkage", "State hospital discharge data, Q%d %d discharges: %d revisions of registry hips "
                      "at other Wisconsin hospitals added." % (qq, y, q.get((y, qq), 0)), "KL"))
    for y in range(2018, 2027):
        E.append((runs[(y, 4)] + dt.timedelta(days=4 if y < 2026 else 9), "Extract",
                  "Annual extract of %d-12-31 taken for the outcomes team." % y, "MB"))
    E.append((dt.date(2027, 1, 22), "Linkage", "Wisconsin death index linkage, deaths to 31 December 2026, applied.",
              "KL"))
    E.sort(key=lambda x: (x[0], x[1]))
    return [x for x in E if x[0] <= dt.date(2027, 1, 26)]


def write_manifest(path, entries):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["file", "what it is", "source", "prepared", "rows or pages"])
        for e in entries:
            w.writerow(e)
