"""Write the golden deliverables into task180/golden/ from the shipped bundle alone: the unit's note to the
medicines safety committee (signal_refinement_note.docx) and the new-user table (new_users_by_year.csv)."""
import csv
import os
import sys

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as G         # noqa: E402
import postprocess as PP   # noqa: E402

TASK = os.path.dirname(HERE)
NOTE = "signal_refinement_note.docx"
TABLE = "new_users_by_year.csv"
INK = RGBColor(0x1F, 0x2A, 0x36)
GREY = RGBColor(0x55, 0x5E, 0x69)
ACCENT = RGBColor(0x8A, 0x2B, 0x1F)
PRODUCT = {"tasorexant": "Somnevo", "corinurad": "Uralexa", "velaglutide": "Gravera"}
EVENT_NAME = {"tasorexant": "falls", "corinurad": "acute kidney injury", "velaglutide": "acute pancreatitis"}
CODES = {"tasorexant": "N05CJ05", "corinurad": "M04AX02; M04AB06", "velaglutide": "A10BJ09"}
WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
         11: "eleven", 12: "twelve"}


def r2(x):
    return "%.2f" % x


def ci(t):
    return "%s (95%% CI %s to %s)" % (r2(t[0]), r2(t[1]), r2(t[2]))


def _cell(cell, text, bold=False, align=None, size=9, color=None):
    cell.text = ""
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.bold = bold
    if color is not None:
        run.font.color.rgb = color
    if align == "right":
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_after = Pt(0)


def _shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def _table(doc, header, rows, widths, right=(), bold_row=None):
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    for j, h in enumerate(header):
        _cell(t.rows[0].cells[j], h, bold=True, size=8.5, align="right" if j in right else None)
        _shade(t.rows[0].cells[j], "DDE3E9")
    for i, row in enumerate(rows):
        cells = t.add_row().cells
        for j, v in enumerate(row):
            _cell(cells[j], v, size=8.5, align="right" if j in right else None, bold=(bold_row == i))
    for row in t.rows:
        for j, w in enumerate(widths):
            row.cells[j].width = Cm(w)
    return t


def _para(doc, text, size=10, bold=False, italic=False, color=None, after=6, before=0):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color is not None:
        run.font.color.rgb = color
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.space_before = Pt(before)
    return p


def _heading(doc, text):
    return _para(doc, text, size=11, bold=True, color=INK, after=3, before=7)


def _page_field(paragraph):
    run = paragraph.add_run()
    for kind, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        if kind:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), kind)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = txt
        run._r.append(el)
    run.font.size = Pt(8)


def figures(D, g):
    """Every figure the note states, from the analysis."""
    f = dict(g)
    pre = g["pre"]
    f["tas_vs_matched"] = pre["tasorexant users"] / pre["tasorexant matched"]
    f["tas_vs_zop"] = pre["tasorexant users"] / pre["zopiclone users"]
    f["cor_vs_all"] = pre["corinurad users"] / pre["allopurinol users"]
    return f


def write_note(path, D, g):
    f = figures(D, g)
    a = g["answer"]
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    sec.left_margin = sec.right_margin = Cm(2.1)
    sec.top_margin, sec.bottom_margin = Cm(1.7), Cm(1.6)
    fp = sec.footer.paragraphs[0]
    fr = fp.add_run("The Agency, Pharmacovigilance Unit. Note to the Medicines Safety Committee, meeting of "
                    "22 October 2026.   Page ")
    fr.font.size = Pt(8)
    fr.font.color.rgb = GREY
    _page_field(fp)

    _para(doc, "THE AGENCY  |  PHARMACOVIGILANCE UNIT  |  NOTE TO THE MEDICINES SAFETY COMMITTEE", size=8.5,
          bold=True, color=GREY, after=3)
    meta = doc.add_table(rows=0, cols=2)
    meta.autofit = False
    for k, v in [("Meeting", "22 October 2026, signals from the Q3 2026 screen"),
                 ("From", "Iben Pedersen, pharmacoepidemiologist"),
                 ("Approved", "Helge Jørgensen, head of unit"),
                 ("Date", "16 October 2026"),
                 ("Data", "Registry extract PV-2026-117, data to 30 June 2026; SOP-PV-14 revision 3"),
                 ("For", "Decision: which signal to open a formal assessment on")]:
        cells = meta.add_row().cells
        _cell(cells[0], k, bold=True, size=9)
        _cell(cells[1], v, size=9)
    for row in meta.rows:
        row.cells[0].width, row.cells[1].width = Cm(2.6), Cm(14.2)
    _para(doc, "", after=1)
    _para(doc, "Open the formal assessment on %s (%s) and %s" % (a, PRODUCT[a], EVENT_NAME[a]), size=15, bold=True,
          color=ACCENT, after=5)

    _para(doc, "Of the three signals from the Q3 screen, the registries support one: acute kidney injury in the month "
               "after starting corinurad. In days 1 to 30 after a new user's first dispensing, admissions with acute "
               "kidney injury ran at %s times the rate in the same people's days 61 to 180 (95%% CI %s to %s). "
               "Among people who started corinurad in 2025, %d admissions with acute kidney injury fell in that "
               "month, and corinurad caused %d of them. Falls with tasorexant and acute pancreatitis with "
               "velaglutide are not supported: in the same comparison the month after the start carries no more "
               "events than later time on the medicine." % (r2(f["ratio"]), r2(f["lower"]), r2(f["upper"]),
                                                             f["events_2025"], f["caused"]), after=6)

    rows = []
    order = ["corinurad", "tasorexant", "velaglutide"]
    for s in order:
        t = g["sccs"][s]
        rows.append(["%s (%s)" % (s, PRODUCT[s]), EVENT_NAME[s], str(g["reports"][s]),
                     "%s (%s to %s)" % (r2(t[0]), r2(t[1]), r2(t[2])), "Yes" if s == a else "No"])
    _table(doc, ["Medicine", "Event", "Q3 cases", "Rate ratio, days 1 to 30 against 61 to 180", "Supported"], rows,
           [3.9, 3.4, 1.7, 5.6, 2.1], right=(2,), bold_row=0)
    _para(doc, "Q3 cases: spontaneous reports received July to September 2026 with the medicine suspected (screen of "
               "6 October). Rate ratio: each new user's admissions in days 1 to 30 after the first dispensing against "
               "the same person's days 61 to 180.", size=8, italic=True, color=GREY, after=6, before=2)

    _heading(doc, "Why the comparison is made within each person")
    _para(doc, "The new medicines are not started by people like everyone else. Tasorexant is prescribed to older "
               "people who already fall: in the year before they started it, new users were admitted for a fall at "
               "%s times the rate of the matched non-users drawn for them and at %s times the rate of people "
               "starting zopiclone. Comparing tasorexant starters with other people, matched or adjusted for every "
               "comorbidity the registries record, therefore shows an excess of falls after the start that was "
               "already there before it." % (r2(f["tas_vs_matched"]), r2(f["tas_vs_zop"])), after=4)
    _para(doc, "Corinurad goes the other way. It is avoided in kidney disease, so its starters are gout patients with "
               "healthy kidneys: in the year before the start their rate of kidney injury admissions was %s times "
               "that of people starting allopurinol, the gout medicine used in kidney disease. Set against "
               "allopurinol starters, corinurad's excess in the first month all but disappears." % r2(f["cor_vs_all"]),
          after=4)
    rise = ("about two and a half times" if 2.35 <= f["ratio"] < 2.65 else
            "more than twofold" if f["ratio"] < 2.35 else "between two and a half and three times")
    _para(doc, "Comparing each new user's first month with the same person's later months removes everything fixed "
               "about who is prescribed the medicine. On that comparison falls with tasorexant and pancreatitis with "
               "velaglutide sit at the level of later time on the medicine, and acute kidney injury with corinurad "
               "rises " + rise + ". The kidney injury excess is not explained by anti-inflammatory "
               "cover for gout flares: among corinurad starters with no NSAID dispensed in the first 30 days the "
               "rate ratio is %s (95%% CI %s to %s)." % (r2(f["nsaid_free"][0]), r2(f["nsaid_free"][1]),
                                                         r2(f["nsaid_free"][2])), after=6)

    _heading(doc, "Corinurad: figures for the committee")
    _table(doc, ["", "Figure"],
           [["Rate ratio, days 1 to 30 after the start (95% CI)",
             "%s (%s to %s)" % (r2(f["ratio"]), r2(f["lower"]), r2(f["upper"]))],
            ["Admissions with acute kidney injury in days 1 to 30, people starting in 2025", str(f["events_2025"])],
            ["Of which caused by corinurad", str(f["caused"])]],
           [11.0, 5.0], right=(1,))
    _para(doc, "New users, events and observation as SOP-PV-14 sections 4 to 7: new users after 365 days without "
               "corinurad under either of its ATC codes (M04AX02 to 2023, M04AB06 from 2024), resident for that year, "
               "returned dispensings not counted; inpatient admissions with acute kidney injury (DN17) as action "
               "diagnosis, transfers counted once; observation ends at death, emigration or 30 June 2026. Ratio by "
               "conditional Poisson regression, each start its own stratum, Wald interval. Admissions caused = "
               "admissions times (ratio - 1) / ratio, to the nearest whole admission (SOP-PV-14 8.2).",
          size=8, italic=True, color=GREY, after=6, before=2)
    _para(doc, "If the committee agrees, the unit will prepare the assessment request for corinurad and keep falls "
               "with tasorexant and pancreatitis with velaglutide on the quarterly screen.", after=0)
    cp = doc.core_properties
    cp.author = "Iben Pedersen"
    cp.title = "Signal refinement, Q3 2026"
    doc.save(path)
    PP.normalize_ooxml(path, "Iben Pedersen", "Helge Jørgensen", "2026-10-14T08:05:00Z", "2026-10-16T11:22:00Z",
                       title="Signal refinement, Q3 2026")


def write_table(path, g):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["substance", "product", "atc_codes", "calendar_year", "new_users"])
        for s in G.NEW:
            for y in (2022, 2023, 2024, 2025):
                w.writerow([s, PRODUCT[s], CODES[s], y, g["new_users"][(s, y)]])


def main(target=None, out=None):
    target = target or os.path.join(TASK, "target")
    out = out or os.path.join(TASK, "golden")
    os.makedirs(out, exist_ok=True)
    D, g = G.solve(target)
    write_note(os.path.join(out, NOTE), D, g)
    write_table(os.path.join(out, TABLE), g)
    return D, g


if __name__ == "__main__":
    main()
