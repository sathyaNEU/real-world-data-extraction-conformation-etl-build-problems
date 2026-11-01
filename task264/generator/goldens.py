"""The golden deliverables, computed from target/ through analysis.py: the placement schedule (csv) and the
board paper (docx, with its chart drawn by matplotlib)."""
import csv
import io
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Cm, RGBColor
from io_util import repack_ooxml

BOARD = "Quenmoor and Kirkbeck Integrated Care Board"


def rnd(x):
    return int(math.floor(x + 0.5))


def frame(res):
    """Every figure the deliverables and the write-up carry, computed once."""
    L = res["L"]
    prov = L["prov"]
    cur = {}
    for r in prov.itertuples():
        unit = L["site"][r.provider_code]
        if r.valid_to == "":
            cur[unit] = (r.provider_code, r.provider_name, r.ods_site_code)
    gold, place, cap = res["R"]["GOLD"], res["place"]["GOLD"], res["cap"]
    rows = []
    for u in gold:
        code, name, ods = cur[u]
        rows.append(dict(unit=u, code=code, name=name, ods=ods, outcome=gold[u], points=rnd(gold[u]),
                         offered=cap[u], placed=place[u]))
    rows.sort(key=lambda r: (-r["points"], -r["outcome"]))
    m = res["m"]
    F = dict(rows=rows, placed=sum(r["placed"] for r in rows), held=1250 - sum(r["placed"] for r in rows),
             funded=[r for r in rows if r["placed"] > 0], eligible=len(m), answered=int(m.resp.sum()),
             netE=res["netE"], n_flag=int(m.f90.sum()),
             resp_flag=100.0 * m[m.f90].resp.mean(), resp_rest=100.0 * m[~m.f90].resp.mean(),
             d_flag=m[m.resp & m.f90].d.mean(), d_rest=m[m.resp & ~m.f90].d.mean(),
             default=res["place"]["R2_casemix_imputation"], default_scores=res["R"]["R2_casemix_imputation"])
    A, B = res["askA"]["golden"], res["askB"]["golden"]
    names = {r["unit"]: r["name"] for r in rows}
    F["waits"] = sorted([dict(unit=u, name=names[u], waiting=A[u]["waiting"], over52=A[u]["over52"],
                              within18=rnd(A[u]["within18"]), within18_raw=A[u]["within18"]) for u in A],
                        key=lambda r: r["name"])
    F["part"] = sorted([dict(unit=u, name=names[u], part=rnd(B[u]), raw=B[u]) for u in B], key=lambda r: r["name"])
    return F


def write_csv(F, path):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(["provider", "provider_code", "ods_site_code", "outcome_points", "operations_placed"])
    for r in F["rows"]:
        w.writerow([r["name"], r["code"], r["ods"], r["points"], r["placed"]])
    w.writerow(["Not placed (held for in-year commissioning)", "", "", "", F["held"]])
    open(path, "w", encoding="utf-8", newline="").write(buf.getvalue())


def chart(F, path):
    rows = sorted(F["waits"], key=lambda r: r["waiting"])
    names = [r["name"].replace(" Hospital", "").replace(" Surgical Centre", "").replace(" Treatment Centre", "")
             .replace(" Spine Clinic", "").replace(" Royal Infirmary", " RI").replace(" General", "") for r in rows]
    under = [r["waiting"] - r["over52"] for r in rows]
    over = [r["over52"] for r in rows]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5})
    fig, ax = plt.subplots(figsize=(6.4, 3.9), dpi=150)
    y = range(len(rows))
    ax.barh(y, under, height=0.62, color="#86b6ef", edgecolor="white", linewidth=1.2, label="52 weeks or less")
    ax.barh(y, over, left=under, height=0.62, color="#184f95", edgecolor="white", linewidth=1.2,
            label="More than 52 weeks")
    for i, r in enumerate(rows):
        ax.text(r["waiting"] + 6, i, "%d (%d)" % (r["waiting"], r["over52"]), va="center", fontsize=7.5, color="#333333")
    ax.set_yticks(list(y))
    ax.set_yticklabels(names)
    ax.set_xlabel("Patients waiting on 31 March 2026")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#9a9a9a")
    ax.tick_params(colors="#444444")
    ax.set_xlim(0, max(r["waiting"] for r in rows) * 1.18)
    ax.legend(frameon=False, loc="lower right", fontsize=7.5)
    top = max(rows, key=lambda r: r["over52"])
    fig.text(0.015, 0.975, "%s carries the most waits over 52 weeks (%d patients)" % (top["name"], top["over52"]),
             ha="left", va="top", fontsize=9, color="#222222", weight="bold")
    fig.text(0.015, 0.925, "Waiting list on 31 March 2026; each bar labelled with patients waiting (more than 52 weeks)",
             ha="left", va="top", fontsize=8, color="#444444")
    fig.tight_layout(rect=(0, 0, 1, 0.88))
    fig.savefig(path, format="png", metadata={"Software": None})
    plt.close(fig)


def _cell(c, text, bold=False, align=None, size=9):
    c.text = ""
    p = c.paragraphs[0]
    run = p.add_run(str(text))
    run.bold = bold
    run.font.size = Pt(size)
    if align == "r":
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT


def _table(doc, head, body, widths, right=()):
    t = doc.add_table(rows=1, cols=len(head))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    for i, h in enumerate(head):
        _cell(t.rows[0].cells[i], h, bold=True, align="r" if i in right else None)
    for row in body:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            _cell(cells[i], v, bold=False, align="r" if i in right else None)
    for row in t.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = Cm(w)
    return t


def para(doc, text, bold=False, size=10, after=6, italic=False):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold, r.italic = bold, italic
    r.font.size = Pt(size)
    p.paragraph_format.space_after = Pt(after)
    return p


def footer(doc):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    p = doc.sections[0].footer.paragraphs[0]
    r = p.add_run("Quenmoor and Kirkbeck ICB | Board meeting held in public, 12 November 2026 | Item 11 | Page ")
    r.font.size = Pt(8)
    run = p.add_run()
    run.font.size = Pt(8)
    for kind, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if kind:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), kind)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = text
        run._r.append(el)


def write_docx(F, path, png):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10)
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2.2)
        s.top_margin = s.bottom_margin = Cm(2.0)
    para(doc, BOARD, bold=True, size=13, after=2)
    para(doc, "Board meeting held in public, 12 November 2026", size=10, after=8)
    meta = [("Agenda item", "11"),
            ("Report title", "2027-28 additional lumbar spinal operations: five providers clear the outcome floor"),
            ("Executive lead", "Maureen Thompson, Director of Planned Care"),
            ("Report author", "Iain Kaur, Senior Analyst, Planned Care"),
            ("Purpose", "Decision")]
    t = doc.add_table(rows=0, cols=2)
    t.style = "Table Grid"
    for k, v in meta:
        c = t.add_row().cells
        _cell(c[0], k, bold=True)
        _cell(c[1], v)
        c[0].width, c[1].width = Cm(4.0), Cm(12.6)
    para(doc, "", after=2)
    fund = F["funded"]
    para(doc, "1. Recommendation", bold=True, size=11, after=4)
    para(doc, "In September the board approved the contracting policy for the 1,250 additional lumbar decompression "
              "and discectomy operations it will commission in 2027-28. The policy places the volume on the outcomes "
              "patients reported a year after the same operations in 2023-24 and 2024-25, case-mix adjusted, with "
              "a floor of 14.5 points.")
    para(doc, "The board is asked to approve placing %s operations with the five providers in Table 1 that clear the "
              "floor, each up to the volume it offered, and to hold the remaining %d for in-year commissioning."
         % (format(F["placed"], ","), F["held"]), bold=True)
    para(doc, "Table 1. 2027-28 placement by provider (outcome: case-mix adjusted mean change in the Oswestry "
              "Disability Index a year after the operation, in points)", italic=True, size=9, after=3)
    body = [[r["name"] + ("\u00b9" if r["code"] != r["unit"] else ""), r["points"], r["offered"], r["placed"]]
            for r in F["rows"]]
    body.append(["Total placed", "", "", format(F["placed"], ",")])
    _table(doc, ["Provider", "Outcome", "Offered", "Placed"], body, [8.2, 2.6, 2.6, 2.6], right=(1, 2, 3))
    para(doc, "Source: Mossgill Outcomes questionnaire extracts and the board's hospital episode extract to 30 September "
              "2026; providers' capacity returns, version 1.2. Outcomes are shown in whole points; the floor is applied "
              "to the unrounded outcome.", size=8, after=2)
    pen = [r for r in F["rows"] if r["code"] != r["unit"]][0]
    para(doc, "\u00b9 Reported for 2023-24 and 2024-25 under provider code %s (Penderwick House Hospital); renamed and "
              "re-coded %s when Corriemoor Healthcare completed its purchase on 1 April 2025." % (pen["unit"], pen["code"]),
         size=8, after=8)
    para(doc, "2. How the outcomes were measured", bold=True, size=11, after=4)
    para(doc, "Each outcome is the policy measure over all %s eligible operations, not only the %s whose patients "
              "returned the 12-month questionnaire. Patients readmitted as an emergency within 90 days of discharge "
              "returned it far less often (%d%% against %d%% of other patients), and those who did return it reported "
              "a change %.1f points below the case-mix expectation. A missing 12-month score was therefore estimated "
              "from the patients at the same provider with the same readmission status, not from the pre-operative "
              "case-mix, on which those who returned the questionnaire and those who did not look alike."
         % (format(F["eligible"], ","), format(F["answered"], ","), rnd(F["resp_flag"]), rnd(F["resp_rest"]),
            abs(F["d_flag"])))
    para(doc, "Read from the returned questionnaires alone, Ormsbrook Spine Clinic and Thistledene Hospital would clear "
              "the floor and all 1,250 operations would go to seven providers; a larger share of their patients was "
              "readmitted as an emergency than at any other provider, and on the full measure both sit below 14.5 points.")
    para(doc, "3. Waiting list on 31 March 2026", bold=True, size=11, after=4)
    para(doc, "Waits are counted under section 5 of the policy: from the day the musculoskeletal triage service received "
              "the referral where the patient came through it, with the clock kept running across the board's "
              "mutual-aid moves, and each patient counted once at the provider responsible on 31 March.")
    doc.add_picture(png, width=Cm(16.0))
    para(doc, "Figure 1. Patients waiting by provider, split at 52 weeks.", italic=True, size=9, after=6)
    para(doc, "Table 2. Waits on 31 March 2026", italic=True, size=9, after=3)
    _table(doc, ["Provider", "Waiting more than 52 weeks", "Waited 18 weeks or less (%)"],
           [[r["name"], r["over52"], r["within18"]] for r in F["waits"]], [8.2, 4.0, 4.4], right=(1, 2))
    para(doc, "Source: providers' month-end waiting list submissions and removals; community MSK triage service "
              "referral log.", size=8, after=8)
    para(doc, "4. Pre-operative questionnaire participation, 2025-26", bold=True, size=11, after=4)
    para(doc, "Participation is the share of each provider's 2025-26 index operations whose patient completed a scored "
              "pre-operative questionnaire in the 90 days up to and including the day of the operation (policy "
              "section 6), dated from the hospital record.")
    _table(doc, ["Provider", "Participation (%)"], [[r["name"], r["part"]] for r in F["part"]], [8.2, 4.0], right=(1,))
    para(doc, "Source: hospital episode extract; Mossgill Outcomes questionnaire extracts and NHS number link.", size=8,
         after=8)
    para(doc, "5. Next steps", bold=True, size=11, after=4)
    para(doc, "Contract variations will go to the five providers once the board approves. The %d operations held back "
              "will be offered through in-year commissioning on the same measure. Providers below the floor will be "
              "offered a meeting with the clinical lead to go through their results." % F["held"])
    footer(doc)
    doc.save(path)
    repack_ooxml(path, "Iain Kaur", "Maureen Thompson", "2026-10-05T08:40:00Z", "2026-10-06T16:05:00Z",
                 "Placing the 2027-28 additional elective lumbar spinal operations", BOARD)


def write_all(res, golden_dir, work_dir):
    os.makedirs(golden_dir, exist_ok=True)
    os.makedirs(work_dir, exist_ok=True)
    F = frame(res)
    write_csv(F, os.path.join(golden_dir, "spinal_volume_2027-28.csv"))
    png = os.path.join(work_dir, "waiting_list_2026-03-31.png")
    chart(F, png)
    write_docx(F, os.path.join(golden_dir, "spinal_volume_board_paper.docx"), png)
    return F
