"""Write the golden deliverables: inspection_slate_2027-28.docx (the board paper) and
dga_fleet_review.csv (one row per transformer, for the engineers)."""
import csv
import datetime as dt
import os

from docx import Document
from docx.enum.section import WD_ORIENT  # noqa: F401
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

import world as W
import docs

NAVY = RGBColor(0x1F, 0x33, 0x52)
GREY = RGBColor(0x55, 0x5B, 0x63)
WINDOWS = ["12 April to 21 May 2027", "23 August to 1 October 2027", "31 January to 10 March 2028"]


def name(tid):
    code, pos = tid.split("-")
    return f"{W.SUB_NAME[code]} {pos}"


def sev(x):
    return f"{x:.2f}"


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
    elif align == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)


def _shade(cell, hexfill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexfill)
    tcPr.append(shd)


def _repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    trPr.append(el)


def _table(doc, header, rows, widths, aligns):
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    _repeat_header(t.rows[0])
    for j, h in enumerate(header):
        _cell(t.rows[0].cells[j], h, bold=True, align=aligns[j], size=8.5)
        _shade(t.rows[0].cells[j], "DCE3EA")
    for row in rows:
        cells = t.add_row().cells
        for j, v in enumerate(row):
            _cell(cells[j], v, align=aligns[j], size=8.5)
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
    return _para(doc, text, size=11.5, bold=True, color=NAVY, after=4, before=8)


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


def write_docx(g, path):
    coded, a, b = g["coded"], g["ask_a"], g["ask_b"]
    slate = g["slate"]
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    sec.left_margin = sec.right_margin = Cm(2.0)
    sec.top_margin, sec.bottom_margin = Cm(1.8), Cm(1.8)
    fp = sec.footer.paragraphs[0]
    fr = fp.add_run("Ellesmere Lines Limited. Board meeting 28 October 2026, item 6.3. In confidence.   Page ")
    fr.font.size = Pt(8)
    fr.font.color.rgb = GREY
    _page_field(fp)

    _para(doc, "ELLESMERE LINES LIMITED  |  BOARD PAPER", size=8.5, bold=True, color=GREY, after=2)
    meta = doc.add_table(rows=0, cols=2)
    meta.autofit = False
    for k, v in [("Meeting", "28 October 2026, item 6.3"),
                 ("Subject", "Zone substation transformer internal inspections, 2027/28"),
                 ("From", "Donna Carson, Network Asset Manager"),
                 ("With", "Barry Forbes, Zone Substation Engineer"),
                 ("Date", "21 October 2026"),
                 ("For", "Decision")]:
        cells = meta.add_row().cells
        _cell(cells[0], k, bold=True, size=9)
        _cell(cells[1], v, size=9)
        cells[0].width, cells[1].width = Cm(2.6), Cm(14.4)
    for c_, w_ in zip(meta.columns, (Cm(2.6), Cm(14.4))):
        c_.width = w_
    _para(doc, "", after=2)
    t1, t2, t3 = slate
    _para(doc, f"Inspect {name(t1)}, {name(t2)} and {name(t3)} in the three 2027/28 mobile substation "
               "windows", size=15, bold=True, color=NAVY, after=6)

    _heading(doc, "Recommendation")
    _para(doc, "That the Board approves internal inspections of the following three zone substation transformers "
               "in 2027/28, taken in this order in the three MSU-2 windows held for Ellesmere Lines.", after=4)
    gas_word = {g_: W.GAS_NAMES[g_] for g_ in W.GASES}
    rows = []
    for k, tid in enumerate(slate):
        c, s, gas, _ = coded[tid]
        rows.append([str(k + 1), tid, W.SUB_NAME[tid.split("-")[0]], WINDOWS[k], str(c), sev(s),
                     gas_word[gas].capitalize()])
    _table(doc, ["Order", "Transformer", "Substation", "MSU-2 window", "Code", "Severity", "Gas"], rows,
           [1.2, 2.0, 2.4, 4.6, 1.2, 1.6, 2.6], [None, None, None, None, "center", "right", None])
    _para(doc, "Code and severity score under ES-DGA-02 section 4 on the September 2026 round. The severity score "
               "is the gas's twelve-month increase divided by its rate limit.", size=8, italic=True,
          color=GREY, after=6, before=2)

    v_c, v_s, v_g, _ = coded[t1]
    a_c, a_s, a_g, _ = coded[t2]
    th_c, th_s, th_g, _ = coded[t3]
    rest = [t for t in sorted(coded, key=lambda x: -coded[x][1]) if coded[t][0] == 3 and t not in slate]
    _heading(doc, "Why these three")
    _para(doc, f"ES-DGA-02 gives the inspection outages to the transformers whose main-tank gases point to the most "
               f"severe faults in the main tank. {name(t1)} has the strongest: acetylene rising at "
               f"{sev(v_s)} times its rate limit, with hydrogen rising alongside it, which is arcing inside the tank. "
               f"It has a vacuum tap changer, so none of that acetylene comes from switching. {name(t2)} shows the "
               f"same kind of arcing at a lower rate ({sev(a_s)}). Its tap changer is an in-oil type, but its "
               f"acetylene does not follow the tap changer's operations and comes with hydrogen, so it is being "
               f"made in the main tank. {name(t3)} has a thermal fault in the oil, with ethylene, methane and "
               f"ethane all rising and ethylene at {sev(th_s)} times its limit.")
    if rest:
        rtxt = " and ".join(f"{name(t)} ({sev(coded[t][1])})" for t in rest)
        _para(doc, f"{rtxt} are also code 3 on thermal gases. They stay on monthly sampling and are first in line "
                   f"for 2028/29.")
    att = sorted(g["attributed"], key=lambda t: -g["naive"][t][1])
    if att:
        lc = g["latest_c2h2"]
        rank = sorted(W.IDS, key=lambda t: -lc[t])
        top_c = rank[0]
        level = [t for t in W.IDS if t != att[1] and abs(lc[t] - lc[att[1]]) < 1e-9]
        assert top_c == att[0] and lc[att[1]] == max(lc[t] for t in W.IDS if t != top_c)
        nm = " and ".join(name(t) for t in att)
        lvl = f", level with {name(level[0])}" if level else ""
        _heading(doc, f"{nm}")
        _para(doc, f"{name(att[0])} has the highest main-tank acetylene in the fleet and {name(att[1])} the next "
                   f"highest{lvl}, and both code 3 on the results as reported. In both, the acetylene has risen in "
                   "step with the tap changer's "
                   "operations from the first result that showed it, with almost no hydrogen alongside, and both "
                   "have in-oil arcing tap changers whose diverter compartments make exactly that gas in normal "
                   "switching. The acetylene is reaching the main tank from the tap changer, not from a fault in "
                   "the windings or core, and an internal inspection would not find it. On the gases generated in "
                   "their main tanks both are code 2. The work they need is on the tap changer, at their next "
                   "tap-changer outage.")
    _heading(doc, "Tap changers")
    _para(doc, "Operations since the last service for every in-oil tap changer, against the ES-DGA-02 annex B "
               "interval of 60,000 operations or seven years.", after=4)
    order = sorted(a, key=lambda t: (not a[t]["past"], -a[t]["ops"]))
    rows = [[t, W.SUB_NAME[t.split("-")[0]], f"{a[t]['last_service'].day} {a[t]['last_service']:%b %Y}", f"{a[t]['ops']:,}",
             "Yes" if a[t]["past"] else "No"] for t in order]
    _table(doc, ["Transformer", "Substation", "Last service", "Operations since", "Past interval"], rows,
           [2.4, 3.0, 3.0, 3.2, 2.6], [None, None, None, "right", "center"])
    _para(doc, "Operations to 16 October 2026 from the SCADA tap-change counters. Service dates are from the "
               "maintenance log (ES-DGA-02 section 6).", size=8, italic=True, color=GREY, after=6, before=2)
    wet = sorted([t for t in b if b[t]["rs"] > 30.0], key=lambda t: -b[t]["rs"])
    _heading(doc, "Wet transformers")
    words = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"}
    _para(doc, f"{words.get(len(wet), str(len(wet)))} transformers were above 30 per cent relative saturation at their latest sample and "
               "are proposed for oil processing in the 2027/28 maintenance programme.", after=4)
    rows = [[t, W.SUB_NAME[t.split("-")[0]], f"{b[t]['sampled'].day} {b[t]['sampled']:%b %Y}", f"{b[t]['rs']:.1f}"]
            for t in wet]
    _table(doc, ["Transformer", "Substation", "Sampled", "Relative saturation %"], rows,
           [2.4, 3.0, 3.0, 3.6], [None, None, None, "right"])
    _para(doc, "Relative saturation per ES-DGA-02 annex C at the September 2026 round, at the oil temperature on "
               "the sample label or, where none was written, the SCADA top-oil temperature for the hour of "
               "sampling.", size=8, italic=True, color=GREY, after=6, before=2)
    _heading(doc, "Next steps")
    _para(doc, "On approval, Aroha O'Brien will name the three sites against the MSU-2 bookings by 1 December 2026, "
               "and the inspection scopes will come to the Asset Committee in February 2027.")
    cp = doc.core_properties
    cp.author = W.PEOPLE["requester"]
    cp.last_modified_by = W.PEOPLE["requester"]
    cp.title = "Zone substation transformer internal inspections 2027/28"
    cp.subject = "Board paper, 28 October 2026"
    cp.revision = 4
    cp.created = dt.datetime(2026, 10, 21, 2, 20)
    cp.modified = dt.datetime(2026, 10, 21, 2, 20)
    cp.comments = ""
    cp.keywords = ""
    doc.save(path)
    docs.rewrite_ooxml(path, W.PEOPLE["requester"], stamp_iso="2026-10-21T02:20:00Z",
                       zip_time=(2026, 10, 21, 15, 20, 0))


def write_csv(g, path):
    coded, a, b, slate = g["coded"], g["ask_a"], g["ask_b"], g["slate"]
    with open(path, "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["transformer_id", "substation", "condition_code", "severity_score", "on_slate",
                     "oltc_operations_since_service", "relative_saturation_pct"])
        for tid in sorted(W.IDS):
            c, s, gas, _ = coded[tid]
            ops = a[tid]["ops"] if tid in a else ""
            wr.writerow([tid, W.SUB_NAME[tid.split("-")[0]], c, sev(s), "yes" if tid in slate else "no",
                         ops, f"{b[tid]['rs']:.1f}"])


def write(g, outdir):
    os.makedirs(outdir, exist_ok=True)
    write_docx(g, os.path.join(outdir, "inspection_slate_2027-28.docx"))
    write_csv(g, os.path.join(outdir, "dga_fleet_review.csv"))
    ts = dt.datetime(2026, 10, 21, 15, 20, tzinfo=W.TZ).timestamp()
    for fn in os.listdir(outdir):
        os.utime(os.path.join(outdir, fn), (ts, ts))
