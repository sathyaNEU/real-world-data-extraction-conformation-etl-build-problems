"""The golden deliverables: the conformed region file and the board paper with its chart."""
import csv, os, io, datetime as dt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
from docx import Document
from docx.shared import Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from world import *
import docs


def r0(x):
    return int(round(x))


def r1000(x):
    return int(round(x / 1000.0)) * 1000


def money(x):
    return "${:,.0f}".format(x)


def write_csv(G, gold, rpop):
    path = os.path.join(G, "regional_visitor_spend_2026.csv")
    rank = {r: i + 1 for i, r in enumerate(gold["order"])}
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["region_code", "region", "visitor_spend_q1_aud", "visitor_spend_q2_aud", "visitor_spend_q3_aud",
                    "visitor_spend_q4_aud", "visitor_spend_2026_aud", "estimated_resident_population",
                    "visitor_spend_per_resident_aud", "rank", "funded_2027"])
        for r in gold["order"]:
            q = gold["q"][r]
            w.writerow([r, NAME[r]] + [r1000(x) for x in q] + [r1000(sum(q)), r0(rpop[r]), r0(gold["per_resident"][r]),
                                                             rank[r], "yes" if r in gold["set"] else "no"])
    return path


def chart(gold, path):
    o = gold["order"][::-1]
    vals = [gold["per_resident"][r] for r in o]
    funded = [r in gold["set"] for r in o]
    fig, ax = plt.subplots(figsize=(7.2, 4.5), dpi=150)
    fig.patch.set_facecolor("white")
    bars = ax.barh([NAME[r] for r in o], vals, height=0.62, color=["#2a78d6" if f else "#a9aeb3" for f in funded])
    line = (gold["per_resident"][gold["fifth"]] + gold["per_resident"][gold["sixth"]]) / 2
    ax.axvline(line, color="#52514e", lw=1.1, ls=(0, (4, 3)))
    ax.text(line + 90, 0.15, "Funding line", color="#52514e", fontsize=8, va="bottom")
    for i, v in enumerate(vals):
        ax.text(v + 90, i, "${:,.0f}".format(round(v)), va="center", fontsize=7.5, color="#0b0b0b")
    ax.set_xlabel("Visitor spending per resident, 2026 ($)", fontsize=8.5, color="#52514e")
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: "{:,.0f}".format(x)))
    ax.tick_params(axis="both", labelsize=8, colors="#52514e", length=0)
    ax.set_title("Five regions clear the funding line", fontsize=10.5, loc="left", color="#0b0b0b")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#c9c9c4")
    ax.grid(axis="x", color="#e6e6e1", lw=0.6)
    ax.set_axisbelow(True)
    ax.set_xlim(0, max(vals) * 1.13)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color="#2a78d6", label="Funded in the 2027 round"), Patch(color="#a9aeb3", label="Below the line")],
              loc="lower right", fontsize=7.5, frameon=False)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def para(d, text, size=None, bold=False, italic=False, color=None, after=None):
    p = d.add_paragraph()
    run = p.add_run(text)
    run.bold, run.italic = bold, italic
    if size:
        run.font.size = Pt(size)
    if color:
        run.font.color.rgb = RGBColor(*color)
    if after is not None:
        p.paragraph_format.space_after = Pt(after)
    return p


def table(d, header, rows, widths, right=()):
    t = d.add_table(rows=1, cols=len(header))
    t.style = "Light List"
    for j, h in enumerate(header):
        t.rows[0].cells[j].text = h
    for row in rows:
        cells = t.add_row().cells
        for j, v in enumerate(row):
            cells[j].text = v
    for row in t.rows:
        for j, c in enumerate(row.cells):
            c.width = Mm(widths[j])
            for p in c.paragraphs:
                if j in right:
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                for r in p.runs:
                    r.font.size = Pt(9)
    return t


def paper(G, gold, rpop, A, B, total, grant, scratch):
    png = os.path.join(scratch, "t454_chart.png")
    chart(gold, png)
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for s in d.sections:
        s.left_margin = s.right_margin = Mm(22)
        s.top_margin = s.bottom_margin = Mm(18)
        f = s.footer.paragraphs[0]
        f.text = "Tourism Commission  |  Board meeting 18 February 2027  |  Item 6"
        f.runs[0].font.size = Pt(8); f.runs[0].font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    names = [NAME[r] for r in gold["set"]]
    fifth, six = gold["fifth"], gold["sixth"]
    pr = {r: r0(gold["per_resident"][r]) for r in ELIGIBLE}
    para(d, "BOARD PAPER  |  ITEM 6  |  FOR DECISION", 8.5, bold=True, color=(0x55, 0x55, 0x55), after=2)
    para(d, "The 2027 round of the Regional Visitor Infrastructure Fund: %s, %s, %s, %s and %s" % tuple(names), 15, bold=True, after=4)
    para(d, "Meeting of 18 February 2027. Prepared by %s, Manager, Visitor Economy Research, with %s, Fund Manager, "
            "5 February 2027." % (PEOPLE["research"], PEOPLE["fund"]), 9, color=(0x55, 0x55, 0x55))
    d.add_heading("Recommendation", level=2)
    para(d, "That the board fund %s, %s, %s, %s and %s in the 2027 round, each region receiving %s." % (tuple(names) + (money(r0(grant)),)))
    d.add_heading("The ranking", level=2)
    para(d, "Section 4 of the round's guidelines funds the five eligible regions with the highest visitor spending per "
            "resident in 2026. %s is the first region below the line at %s per resident, %s short of %s at %s (Table 1, "
            "Figure 1)." % (NAME[six], money(pr[six]), money(pr[fifth] - pr[six]), NAME[fifth], money(pr[fifth])))
    ordw = {6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth", 10: "tenth", 11: "eleventh"}
    pg, pc = gold["order"].index("GID") + 1, gold["order"].index("CAR") + 1
    para(d, ("Gidgee Basin and Carisbrook Tablelands rank %s and %s although both take a great deal of card " % (ordw[pg], ordw[pc])) +
            "spending on cards whose statements go to other regions. Those cards belong to the basin's rostered mine "
            "workforce and, in Carisbrook, to university students, people who travel in from Mulga Plains for work and "
            "households that moved there with their card statements still going to their old address. They are in the "
            "region month after month, so the region is part of their holders' usual environment and what they spend "
            "there is not visitor spending.")
    rows = [[NAME[r], money(r1000(sum(gold["q"][r]))), money(pr[r]), "Funded" if r in gold["set"] else ""] for r in gold["order"]]
    para(d, "Table 1. Eligible regions ranked on visitor spending per resident, 2026", 9, bold=True, after=2)
    table(d, ["Region", "Visitor spending 2026", "Per resident", ""], rows, (58, 42, 30, 20), right=(1, 2))
    para(d, "Visitor spending is rounded to the nearest $1,000 and per-resident figures to the nearest dollar, each from "
            "unrounded spending. Residents: preliminary estimated resident population at 30 June 2026, shared areas at "
            "their Schedule 1 share.", 8, italic=True, color=(0x55, 0x55, 0x55))
    d.add_picture(png, width=Mm(160))
    para(d, "Figure 1. Visitor spending per resident, 2026, every eligible region. Source: Austral Payments Network "
            "research sample for 2026, raised by selection weight.", 8, italic=True, color=(0x55, 0x55, 0x55))
    d.add_heading("What each funded region receives", level=2)
    sumA = sum(r0(A[r]) for r in ELIGIBLE)
    sumB = sum(r0(B[r]) for r in ELIGIBLE)
    para(d, "The round starts from the 2027 appropriation of $12,000,000. The board's decision of 21 October 2026 closing "
            "the Regional Tourism Infrastructure Program adds the %s of unspent grant money councils returned to the program "
            "in 2026 and takes out the %s that remained at 31 December 2026 on the program's open agreements, which the "
            "Fund now pays (Table 2). The round's total is %s, shared equally among the five regions, so each receives %s."
         % (money(sumB), money(sumA), money(12_000_000 + sumB - sumA), money(r0(grant))))
    para(d, "Table 2. The closing program by region", 9, bold=True, after=2)
    rows = [[NAME[r], money(r0(A[r])), money(r0(B[r]))] for r in ELIGIBLE] + [["All regions", money(sumA), money(sumB)]]
    table(d, ["Region", "Remaining on open agreements at 31 December 2026", "Unspent money returned in 2026"], rows,
          (50, 55, 45), right=(1, 2))
    para(d, "Source: grants management system, agreements at 31 December 2026 and 2026 claims; accounts payable and "
            "receivable, 2026. Finance pays each council's approved claims in one weekly transfer quoting the agreement "
            "of the first claim, so each transfer is booked to the claims it paid. Claims approved in the last days of "
            "December, and a few approved earlier, had not been paid by 31 December 2026 and remain on their agreements. The "
            "20 March 2026 payments repeated the 19 March run. Money a council sent back for them is not unspent grant "
            "money, and some councils had not sent theirs back by 31 December 2026.", 8, italic=True, color=(0x55, 0x55, 0x55))
    d.add_heading("Basis of the visitor figures", level=2)
    para(d, "A card's spending in a region counts as a visitor's only where the region lies outside its holder's usual "
            "environment as the International Recommendations for Tourism Statistics 2008 define it. The usual "
            "environment is read from the card's own year in the sample: a region it is in month after month on many days "
            "is where its holder lives, works or studies, whatever address its statements go to, and a region it is in "
            "for a few days in one to three months is a trip.")
    docs.fix_docx_props(d, PEOPLE["research"], "The 2027 round of the Regional Visitor Infrastructure Fund")
    path = os.path.join(G, "rvif_2027_round_paper.docx")
    d.save(path)
    docs.rezip(path, dt.datetime(2027, 2, 3, 23, 8, 0), dt.datetime(2027, 2, 4, 22, 41, 0),
               app=docs.docx_app("Tourism Commission", 214), drop=("docProps/thumbnail.jpeg",))
    return path
