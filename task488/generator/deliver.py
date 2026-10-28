"""The three goldens: Corvane's import file, the pool summary workbook and the board memo with its one chart."""
from __future__ import annotations

import datetime as dt
import io
import os
import zipfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import openpyxl  # noqa: E402
from docx import Document  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.shared import Cm, Pt  # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side  # noqa: E402

import docs as DOCS  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402
import solve as S  # noqa: E402

CSV = "bank_import_2027-28.csv"
XLSX = "pool_summary_2027-28.xlsx"
DOCX = "low_band_commission_memo.docx"
WHEN = (2027, 4, 19, 16, 10, 0)
ORG = b"Quarrystone Regional Assessment Consortium"
INK = "#1f2933"
BAR = "#3b6e8f"


def n(x):
    return f"{int(x):,}"


def import_csv(imp, path):
    out = imp[["item_key", "grade", "difficulty", "reporting_domain", "enemy_set", "interaction_type"]].copy()
    out["difficulty"] = out.difficulty.map(lambda v: "%.1f" % v)
    out.to_csv(path, index=False, lineterminator="\n")


def workbook(F, imp, s, gold, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Commission"
    bold = Font(bold=True)
    head = Font(bold=True, color="FFFFFF")
    fill = PatternFill("solid", fgColor="3B6E8F")
    thin = Side(style="thin", color="BBBBBB")
    ws["A1"] = "Quarrystone Interim mathematics: items below the Approaching cut in each grade's July 2027 pool"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Corvane floor %d items per grade; workshop items at their 2025-26 calibration" % P.FLOOR
    hdr = ["Grade", "Approaching cut (QSS)", "Launch items below the cut", "Workshop items below the cut",
           "Items below the cut", "Floor", "New items to commission"]
    ws.append([])
    ws.append(hdr)
    r0 = ws.max_row
    for j in range(1, len(hdr) + 1):
        c = ws.cell(r0, j)
        c.font, c.fill = head, fill
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for g in P.GRADES:
        ws.append([g, F["cut_%d" % g], F["cal_low_%d" % g], F["wk_low_%d" % g], F["low_%d" % g], P.FLOOR,
                   F["commission_%d" % g]])
    ws.append(["Total", None, sum(F["cal_low_%d" % g] for g in P.GRADES), sum(F["wk_low_%d" % g] for g in P.GRADES),
               F["low_total"], None, F["call"]])
    for row in ws.iter_rows(min_row=r0 + 1, max_row=ws.max_row):
        for c in row:
            c.border = Border(bottom=thin)
            if c.column > 1:
                c.number_format = "#,##0"
    ws.cell(ws.max_row, 1).font = bold
    ws.cell(ws.max_row, 7).font = bold
    ws.freeze_panes = "A%d" % (r0 + 1)
    ws.row_dimensions[r0].height = 44
    ws.column_dimensions["A"].width = 9
    for col in "BCDEFG":
        ws.column_dimensions[col].width = 17
    d = wb.create_sheet("Domains")
    bands = {"lower": [c for c, _ in PK.FRAMEWORK["lower"]], "upper": [c for c, _ in PK.FRAMEWORK["upper"]]}
    d.append(["Imported items by grade and 2026 framework domain"])
    d["A1"].font = bold
    for bd, g_list in (("lower", [3, 4, 5]), ("upper", [6, 7, 8])):
        d.append([])
        d.append(["Grade"] + ["%s %s" % (c, nm) for c, nm in PK.FRAMEWORK[bd]] + ["Total"])
        rr = d.max_row
        for j in range(1, 8):
            d.cell(rr, j).font, d.cell(rr, j).fill = head, fill
            d.cell(rr, j).alignment = Alignment(wrap_text=True, vertical="top")
        d.row_dimensions[rr].height = 32
        for g in g_list:
            vals = [F["dom_%d_%s" % (g, c)] for c in bands[bd]]
            d.append([g] + vals + [sum(vals)])
    d.column_dimensions["A"].width = 9
    for col in "BCDEFG":
        d.column_dimensions[col].width = 18
    e = wb.create_sheet("Enemy sets")
    e.append(["Grade", "Enemy sets", "Items in sets"])
    for j in range(1, 4):
        e.cell(1, j).font, e.cell(1, j).fill = head, fill
    for g in P.GRADES:
        e.append([g, F["enemy_sets_%d" % g], F["enemy_items_%d" % g]])
    e.freeze_panes = "A2"
    for col, w in zip("ABC", (9, 14, 16)):
        e.column_dimensions[col].width = w
    w = wb.create_sheet("Workshop items")
    w.append(["Item key", "Grade", "Panel rating (QSS)", "Calibrated difficulty (QSS)", "Below the Approaching cut"])
    for j in range(1, 6):
        w.cell(1, j).font, w.cell(1, j).fill = head, fill
        w.cell(1, j).alignment = Alignment(wrap_text=True, vertical="top")
    w.row_dimensions[1].height = 30
    for g in P.GRADES:
        G = gold[g]["G"]
        for j, q in zip(G.wk, gold[g]["wk_qss"]):
            it = G.items.iloc[j]
            w.append([it.item_key, g, float(it.difficulty_qss), float(q), "yes" if q < G.cut else "no"])
    for row in w.iter_rows(min_row=2, max_row=w.max_row):
        row[2].number_format = "0"
        row[3].number_format = "0.0"
    w.freeze_panes = "A2"
    w.auto_filter.ref = "A1:E%d" % w.max_row
    for col, wd in zip("ABCDE", (11, 8, 16, 20, 14)):
        w.column_dimensions[col].width = wd
    b = wb.create_sheet("Basis")
    for line in [["Basis"],
                 ["Pool", "Operational items in each grade, one record per authored item under its current key "
                          "(Corvane specification 3.2, sections 1 and 2)"],
                 ["Difficulty", "Launch items at their 2021 values; workshop items estimated from the 2025-26 "
                                "operational responses with the launch items held at their values"],
                 ["Low band", "Difficulty below the grade's Approaching cut (scale note, section 3)"],
                 ["Domain", "The current version's 2026 framework code, otherwise the 2010 standard through the "
                            "consortium's crosswalk"],
                 ["Enemy sets", "Two or more items of one grade's pool (specification section 4)"]]:
        b.append(line)
    b["A1"].font = bold
    b.column_dimensions["A"].width = 14
    b.column_dimensions["B"].width = 110
    wb.properties.creator = "QRAC Assessment Office"
    wb.properties.lastModifiedBy = "QRAC Assessment Office"
    wb.properties.title = "July 2027 pool summary"
    wb.save(path)
    DOCS.fixed_xlsx(path, WHEN, ORG, b"QRAC Assessment Office")


def chart(F):
    g = P.GRADES
    low = [F["low_%d" % x] for x in g]
    fig, ax = plt.subplots(figsize=(6.4, 3.2), dpi=200)
    ax.bar([str(x) for x in g], low, width=0.58, color=BAR)
    ax.axhline(P.FLOOR, color="#52606d", linestyle="--", linewidth=1.1)
    ax.text(len(g) - 0.45, P.FLOOR + 2.5, "Corvane floor %d" % P.FLOOR, ha="right", va="bottom", fontsize=8.5,
            color="#52606d")
    for k, (lv, x) in enumerate(zip(low, g)):
        ax.text(k, lv + 2, "%d" % lv, ha="center", va="bottom", fontsize=8.5, color=INK)
        ax.text(k, lv / 2, "+%d" % F["commission_%d" % x], ha="center", va="center", fontsize=8.5, color="white")
    ax.set_ylim(0, P.FLOOR * 1.18)
    ax.set_xlabel("Grade", fontsize=8.5, color=INK)
    ax.set_ylabel("Items below the Approaching cut", fontsize=8.5, color=INK)
    ax.set_title("Every grade's pool falls short of the floor once the workshop items are calibrated", fontsize=9.5,
                 color=INK, loc="left")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color("#9aa5b1")
    ax.tick_params(colors="#52606d", labelsize=8)
    ax.yaxis.grid(True, color="#e4e7eb", linewidth=0.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def _field(par, instr):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    r = par.add_run()
    for kind, txt in (("begin", None), (None, instr), ("end", None)):
        if kind:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), kind)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = txt
        r._r.append(el)


def memo(F, ex, path):
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    sec = d.sections[0]
    sec.left_margin = sec.right_margin = Cm(2.2)
    fp = sec.footer.paragraphs[0]
    fp.text = "Quarrystone Regional Assessment Consortium, Assessment Office. Board papers, 22 April 2027. Page "
    _field(fp, "PAGE")
    fp.runs[0].font.size = Pt(8)
    t = d.add_table(rows=5, cols=2)
    for i, (a, b) in enumerate([("To", "Board of the Quarrystone Regional Assessment Consortium"),
                                ("From", "Assessment Office"), ("Date", "19 April 2027"), ("Item", "Paper 6"),
                                ("Subject", "Summer 2027 item-writing commission for the Corvane pools")]):
        t.cell(i, 0).text = a
        t.cell(i, 1).text = b
        t.cell(i, 0).paragraphs[0].runs[0].bold = True
        t.cell(i, 0).width = Cm(2.4)
        t.cell(i, 1).width = Cm(14)
    d.add_paragraph()
    r = d.add_paragraph().add_run("Commission %s new items below the Approaching cut for the July pools" % n(F["call"]))
    r.bold = True
    r.font.size = Pt(13)
    gtxt = ", ".join("grade %d %d" % (g, F["commission_%d" % g]) for g in P.GRADES)
    p = d.add_paragraph()
    p.add_run("Corvane opens a grade's pool only when it holds at least %d items whose difficulty is below the grade's "
              "Approaching cut." % P.FLOOR)
    p.add_run("1").font.superscript = True
    p.add_run(" With the 2024 and 2025 workshop items calibrated, no grade reaches it. The summer workshop should "
              "write %s items for the low band: %s." % (n(F["call"]), gtxt))
    p = d.add_paragraph()
    p.add_run("Why the bank's values cannot be loaded as they stand. ").bold = True
    p.add_run("Tessaline ran the workshop items at the writing panel's ratings, and every student's reported score "
              "was computed with those ratings. Reading an item against those scores returns the rating it started "
              "from, so we estimated each workshop item's difficulty from the 2025-26 responses together with the "
              "students' abilities, holding the launch items at their 2021 values. Estimated the same way, the launch "
              "items come back at their own values; read against the reported scores, the low launch items come back "
              "several points too easy. The panel placed several multi-step word problems well below the cut that "
              "the students' answers put above it, which is most of the gap between the panel's count and ours.")
    tab = d.add_table(rows=1, cols=5)
    tab.style = "Light List"
    for j, h in enumerate(["Grade", "Launch items below the cut", "Workshop items below the cut", "Items below the cut",
                           "To commission"]):
        tab.rows[0].cells[j].text = h
    for g in P.GRADES:
        c = tab.add_row().cells
        for j, v in enumerate([g, F["cal_low_%d" % g], F["wk_low_%d" % g], F["low_%d" % g], F["commission_%d" % g]]):
            c[j].text = str(v)
    c = tab.add_row().cells
    c[0].text = "Total"
    c[3].text = n(F["low_total"])
    c[4].text = n(F["call"])
    src = d.add_paragraph("Source: Tessaline close-out export of 31 March 2027 (bank, events and item responses, "
                          "2025-26); consortium authoring catalog of 15 March 2027; cut scores from the 2021 scale "
                          "note.")
    src.runs[0].font.size = Pt(8.5)
    d.add_picture(io.BytesIO(chart(F)), width=Cm(15.5))
    d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = d.add_paragraph()
    p.add_run("The import file. ").bold = True
    p.add_run("The import carries every operational item once, under its current key, with its difficulty, its 2026 "
              "framework domain and its enemy set; the pool summary gives the domain counts and the enemy sets by "
              "grade. Revised items that Tessaline re-keyed are loaded under the new key only.")
    fn = d.add_paragraph()
    fr = fn.add_run("1")
    fr.font.superscript = True
    fr.font.size = Pt(8)
    fn.add_run(" Corvane Item Pool Import Specification 3.2, section 5. A grade's pool opens once its commission is "
               "confirmed.").font.size = Pt(8)
    cp = d.core_properties
    cp.author = "QRAC Assessment Office"
    cp.last_modified_by = "QRAC Assessment Office"
    cp.title = "Summer 2027 item-writing commission"
    cp.comments = ""
    cp.created = dt.datetime(*WHEN)
    cp.modified = dt.datetime(*WHEN)
    cp.revision = 1
    d.save(path)
    _fix_docx(path)


def _fix_docx(path):
    with zipfile.ZipFile(path) as z:
        items = [(i, z.read(i.filename)) for i in z.infolist()]
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for info, data in items:
            if info.filename == "docProps/app.xml":
                data = (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.'
                        b'openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.'
                        b'openxmlformats.org/officeDocument/2006/docPropsVTypes"><Template>Normal.dotm</Template>'
                        b'<TotalTime>41</TotalTime><Application>Microsoft Office Word</Application><DocSecurity>0'
                        b'</DocSecurity><Company>Quarrystone Regional Assessment Consortium</Company><AppVersion>16.0000'
                        b'</AppVersion></Properties>')
            zi = zipfile.ZipInfo(info.filename, date_time=WHEN)
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)


def build(F, ex, s, tb, folder):
    os.makedirs(folder, exist_ok=True)
    gold = ex["gold"]
    imp = S.import_table(s, gold)
    import_csv(imp, os.path.join(folder, CSV))
    workbook(F, imp, s, gold, os.path.join(folder, XLSX))
    memo(F, ex, os.path.join(folder, DOCX))
