"""The goldens for task264: gpi_2027_structure.xlsx (the structure and every figure) and gpi_2027_structure_paper.docx
(the case for the committee, with its chart), drafted from the golden path's figures, and generator/figures.json."""
from __future__ import annotations

import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt                                         # noqa: E402
from docx import Document                                               # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH                           # noqa: E402
from docx.shared import Cm, Pt, RGBColor                                 # noqa: E402
from openpyxl import Workbook                                           # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill                 # noqa: E402

import common as K                                                      # noqa: E402
import golden as G                                                      # noqa: E402
import postprocess as PP                                                # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
R1 = lambda x: float("%.1f" % (x + (1e-9 if x >= 0 else -1e-9)))
WORDS = {k: w for k, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen "
                                    "fourteen fifteen sixteen seventeen eighteen".split())}


def figures(R):
    v = R["verdicts"]
    cats = {}
    for c in K.CATS:
        cats[c] = dict(publish=bool(v[c]["publish"]), national=R1(v[c]["national"]),
                       gaps={f: R1(v[c]["gaps"][f]) for f in K.FORMATS}, largest=R1(v[c]["worst"]),
                       changes={f: R1(R["changes"][(c, f)]) for f in K.FORMATS}, promotion=R1(R["promo"][c]))
    rg = R["rungs"]
    four = R["four"]
    shift = [rg["store"]["changes"][(c, "convenience")] - R["changes"][(c, "convenience")] for c in four]
    left = [c for c in K.CATS if c not in R["published"]]
    return dict(call=dict(count=len(R["published"]), categories=R["published"]), categories=cats,
                takings={f: R1(R["takings"][f]) for f in K.FORMATS},
                takings_total=R1(sum(R["takings"].values())),
                continuous={c: int(R["continuous"][c]) for c in K.CHAIN_CODES},
                rungs={k: dict(count=len(x["published"]), categories=x["published"]) for k, x in rg.items()},
                store_match=dict(categories_dropped=four, shift_low=R1(-max(shift)), shift_high=R1(-min(shift)),
                                 slow_week_share=round(R["slow_sale_rate"], 2),
                                 rise_big=R1(R["line_rises"]["big"]), rise_other=R1(R["line_rises"]["other"])),
                closest=dict(category=max(R["published"], key=lambda c: v[c]["worst"]),
                             gap=R1(max(v[c]["worst"] for c in R["published"]))),
                constants=dict(tolerance=K.TOLERANCE, weeks=K.W, categories=len(K.CATS), chains=len(K.CHAIN_CODES),
                               weights=K.FORMAT_WEIGHTS),
                nearest_left=dict(category=min(left, key=lambda c: v[c]["worst"]),
                                  gap=R1(min(v[c]["worst"] for c in left)),
                                  miss=R1(min(v[c]["worst"] for c in left) - K.TOLERANCE)))


# ---------------------------------------------------------------------------------------------- the chart
def chart(path, F):
    cats = K.CATS[::-1]
    fig, ax = plt.subplots(figsize=(7.4, 6.6), dpi=150)
    ax.axvspan(-K.TOLERANCE, K.TOLERANCE, color="#e8eef3", zorder=0)
    ax.axvline(0, color="#9aa6b1", lw=0.8, zorder=1)
    marks = {"supermarket": ("o", "#1f4e79"), "neighbourhood": ("s", "#4f8a3c"), "convenience": ("D", "#b5651d"),
             "online": ("^", "#7a2e3b")}
    for i, c in enumerate(cats):
        g = F["categories"][c]["gaps"]
        lo, hi = min(g.values()), max(g.values())
        ax.plot([lo, hi], [i, i], color="#c3ccd4", lw=1.2, zorder=2)
        for f in K.FORMATS:
            m, col = marks[f]
            ax.scatter(g[f], i, marker=m, s=26, color=col, zorder=3, label=K.FORMAT_LABEL[f] if i == 0 else None)
    labels = [("%s  (own sub-index)" % c) if F["categories"][c]["publish"] else c for c in cats]
    ax.set_yticks(range(len(cats)))
    ax.set_yticklabels(labels, fontsize=8)
    for t, c in zip(ax.get_yticklabels(), cats):
        if F["categories"][c]["publish"]:
            t.set_fontweight("bold")
    ax.set_xlabel("Percentage points (shaded band: within 1.5 of the national change)", fontsize=8.5)
    ax.set_xlim(-3.6, 3.6)
    ax.tick_params(axis="x", labelsize=8)
    n = sum(1 for c in cats if F["categories"][c]["publish"])
    ax.set_title("%s categories keep all four formats within 1.5 points of the national change\n"
                 "Format change less national change, 52 retail weeks to 28 November 2026" % WORDS[n].capitalize(),
                 fontsize=9.5, loc="left")
    for x in (-K.TOLERANCE, K.TOLERANCE):
        ax.text(x, len(cats) - 0.35, "%+.1f" % x, ha="center", va="bottom", fontsize=7.5, color="#5f6870")
    ax.legend(fontsize=7.5, loc="upper center", bbox_to_anchor=(0.42, -0.085), frameon=False, ncol=4)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


# ---------------------------------------------------------------------------------------------- the workbook
HEAD = Font(name="Calibri", bold=True, size=11)
TITLE = Font(name="Calibri", bold=True, size=13)
FILL = PatternFill("solid", fgColor="DCE4EC")
YES = PatternFill("solid", fgColor="E3EFDF")


def workbook(path, F):
    wb = Workbook()
    ws = wb.active
    ws.title = "Structure"
    ws.append(["%s of the 18 food categories hold within 1.5 points in every format: the proposed 2027 structure "
               "(Index Committee, 9 December 2026)" % WORDS[F["call"]["count"]].capitalize()])
    ws["A1"].font = TITLE
    ws.append(["Change over the 52 retail weeks to 28 November 2026 (average index of the last four weeks against the "
               "first four). A category is published on its own where its change in every store format is within "
               "1.5 points of its national change."])
    ws.append([])
    head = ["Category", "Own sub-index in 2027", "National change (%)", "Supermarket gap (pts)",
            "Neighbourhood gap (pts)", "Convenience gap (pts)", "Online gap (pts)", "Largest gap (pts)",
            "Spending on promotion (%)"]
    ws.append(head)
    for c in ws[4]:
        c.font = HEAD
        c.fill = FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for cat in K.CATS:
        x = F["categories"][cat]
        ws.append([cat, "Yes" if x["publish"] else "No (Other food)", x["national"]] +
                  [x["gaps"][f] for f in K.FORMATS] + [x["largest"], x["promotion"]])
        if x["publish"]:
            for c in ws[ws.max_row][:2]:
                c.fill = YES
    for row in ws.iter_rows(min_row=5, min_col=3, max_col=9):
        for c in row:
            c.number_format = "0.0"
    ws.append([])
    ws.append(["Published on their own: %d of 18" % F["call"]["count"]])
    ws[ws.max_row][0].font = HEAD
    ws.append(["; ".join(F["call"]["categories"])])
    widths = [26, 18, 13, 14, 15, 14, 12, 12, 15]
    for i, w in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = w
    ws.row_dimensions[4].height = 45
    ws.freeze_panes = "B5"

    ws2 = wb.create_sheet("Format changes")
    ws2.append(["Category", "Supermarket (%)", "Neighbourhood (%)", "Convenience (%)", "Online (%)", "National (%)"])
    for c in ws2[1]:
        c.font = HEAD
        c.fill = FILL
    for cat in K.CATS:
        x = F["categories"][cat]
        ws2.append([cat] + [x["changes"][f] for f in K.FORMATS] + [x["national"]])
    for row in ws2.iter_rows(min_row=2, min_col=2, max_col=6):
        for c in row:
            c.number_format = "0.0"
    ws2.append([])
    ws2.append(["National: the format changes weighted 59.6 supermarket, 16.3 neighbourhood, 7.1 convenience, 17.0 "
                "online (Index Committee 2026 weights). Gaps on the Structure sheet are taken before rounding."])
    for i, w in enumerate([26, 16, 18, 16, 12, 13]):
        ws2.column_dimensions[chr(65 + i)].width = w
    ws2.freeze_panes = "B2"

    ws3 = wb.create_sheet("Panel")
    ws3.append(["Panel stores' sales by format, 52 retail weeks to 28 November 2026, while in the panel"])
    ws3["A1"].font = HEAD
    ws3.append(["Store format", "Sales (A$ million, incl. GST)"])
    for c in ws3[2]:
        c.font = HEAD
        c.fill = FILL
    for f in K.FORMATS:
        ws3.append([K.FORMAT_LABEL[f], F["takings"][f]])
        ws3.cell(ws3.max_row, 2).number_format = "#,##0.0"
    ws3.append(["All formats", F["takings_total"]])
    ws3.cell(ws3.max_row, 2).number_format = "#,##0.0"
    ws3.append([])
    ws3.append(["Stores sending data in every week their chain was in the panel"])
    ws3[ws3.max_row][0].font = HEAD
    ws3.append(["Chain", "Banner", "Format", "Stores"])
    for c in ws3[ws3.max_row]:
        c.font = HEAD
        c.fill = FILL
    for ch in K.CHAIN_CODES:
        ws3.append([ch, K.CH[ch]["banner"], K.FORMAT_LABEL[K.CH[ch]["fmt"]], F["continuous"][ch]])
    for i, w in enumerate([18, 26, 15, 9]):
        ws3.column_dimensions[chr(65 + i)].width = w
    ws.print_title_rows = "4:4"
    ws4 = wb.create_sheet("Notes")
    notes = [
        "Prepared by Price Indices for the Index Committee meeting of 9 December 2026. Data as loaded by 4 December "
        "2026.",
        "Changes: each category's GEKS-Tornqvist index in each format (GPI methodology statement, 2026 edition, "
        "sections 5 and 6), each line followed at the chain that prices it: the chain's dollars over units across its "
        "stores in the format that week.",
        "National change: the four format changes weighted by the committee's 2026 format weights (terms of "
        "reference, Table 1). Gaps are each format's change less the national change, taken before rounding.",
        "Movement data: accepted loads only; the resubmitted April block replaces its four weekly loads. Item codes "
        "matched as GTIN-14.",
        "Sales: store sales feed, accepted loads, each store's weeks in the panel per the panel store register; "
        "chains whose export repeats the store's weekly total on each department row counted once a store-week; "
        "Sunday week-endings placed on the retail week ending the day before.",
        "Stores sending every week: store codes with the same trading name, suburb and postcode taken as one store; "
        "a chain's weeks run from its data agreement or the start of the year.",
        "Spending on promotion: sales at each chain's catalogue specials (feed dictionary, Terms). Store markdowns "
        "and register price checks excluded. Chain C2 coded its specials PC until the week ending 8 August 2026 and "
        "TPR from then; its earlier PC sales are counted as specials.",
    ]
    ws4.append(["Notes"])
    ws4["A1"].font = HEAD
    for n_ in notes:
        ws4.append([n_])
        ws4.cell(ws4.max_row, 1).alignment = Alignment(wrap_text=True, vertical="top")
    ws4.column_dimensions["A"].width = 120
    wb.save(path)


# ---------------------------------------------------------------------------------------------- the paper
def paper(path, F, png):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2.2)
        s.top_margin = s.bottom_margin = Cm(2.0)

    def para(text, bold=False, size=None, color=None, after=4):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.bold = bold
        p.paragraph_format.keep_with_next = bool(bold)
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
        p.paragraph_format.space_after = Pt(after)
        return p

    pub = F["call"]["categories"]
    other = [c for c in K.CATS if c not in pub]
    cat = F["categories"]
    para("INDEX COMMITTEE  |  Meeting of 9 December 2026  |  Paper IC 26/12-03  |  For decision", size=8.5,
         color="5F6870", after=2)
    para("%s food categories hold in every store format and should publish on their own in 2027"
         % WORDS[len(pub)].capitalize(), bold=True, size=15, color="7A2E3B", after=2)
    para("The 2027 GPI publication structure. From %s, Head of Price Indices, %s. Circulated 7 December 2026."
         % (K.PEOPLE["head"], K.FIRM), size=9, color="5F6870", after=10)
    footer = doc.sections[0].footer.paragraphs[0]
    footer.text = "Index Committee, 9 December 2026. Paper IC 26/12-03, page "
    _page_field(footer)
    for r_ in footer.runs:
        r_.font.size = Pt(8)
        r_.font.color.rgb = RGBColor.from_string("5F6870")

    para("Recommendation", bold=True, size=11.5)
    para("Publish %d of the eighteen food categories as stand-alone sub-indices in 2027: %s. The other %d (%s) "
         "go into Other food. Each of the %d holds in every store format: over the 52 retail weeks to 28 November "
         "2026 its change in supermarkets, neighbourhood stores, convenience stores and online is within 1.5 points "
         "of its national change, and none of the other %d meets that in all four formats."
         % (len(pub), ", ".join(pub[:-1]) + " and " + pub[-1], len(other), ", ".join(other[:-1]) + " and " + other[-1],
            len(pub), len(other)))

    para("How the changes were measured", bold=True, size=11.5)
    para("Each category's change in each format is the GPI's GEKS-Tornqvist index rebuilt from the movement table "
         "(accepted loads, the April resubmission in place of the four weekly loads it replaced), comparing the "
         "average of the last four weeks with the first four. The partner register is the starting point: every "
         "chain sets one shelf price for a line across all its stores in a format and runs its specials in every "
         "store. So a line's price at a chain in a week is known whenever any of its stores sold it, and we follow "
         "each line at the chain that prices it, the chain's dollars over units across its stores that week.")
    para("Two shortcuts give a different structure, and neither measures the prices shoppers paid:")
    sm = F["store_match"]
    four = sm["categories_dropped"]
    para("Matching each line store by store treats a week a store sold none of a line as a missing price. A "
         "convenience store sold one of its slower lines in %d per cent of weeks, so a store-level match keeps a "
         "chain's price for such a line only in the pairs of weeks the same store sold it in both, about one pair "
         "in %d, and the convenience index follows the big sellers. In %s the slower lines rose by %.1f per cent on "
         "average against %.1f per cent for the three biggest sellers, so the store-level match puts their "
         "convenience change %.1f to %.1f points too low and drops all four; in Coffee and tea it pulls convenience "
         "back inside the band. That route publishes %d categories, not %d."
         % (round(100 * sm["slow_week_share"]), round(1 / sm["slow_week_share"] ** 2),
            ", ".join(four[:-1]) + " and " + four[-1], sm["rise_other"], sm["rise_big"], sm["shift_low"],
            sm["shift_high"], F["rungs"]["store"]["count"], len(pub)))
    para("Averaging each line over all of a format's stores turns shoppers' moves between chains into price "
         "changes: the value chain that joined the panel in July and the steady shift of supermarket spending "
         "toward the discount chain both lower the supermarket average price with no shelf price falling. That "
         "route publishes %d categories, and leaving out the July chain still publishes only %d."
         % (F["rungs"]["pooled"]["count"], F["rungs"]["pooled_without_july_chain"]["count"]))

    para("Results", bold=True, size=11.5)
    doc.add_picture(png, width=Cm(15.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.LEFT
    t = doc.add_table(rows=1, cols=4)
    t.style = "Light Grid Accent 1"
    hdr = t.rows[0].cells
    for i, h in enumerate(["Category", "National change (%)", "Largest format gap (pts)", "2027"]):
        hdr[i].text = h
    for c in sorted(K.CATS, key=lambda c: (not cat[c]["publish"], cat[c]["largest"])):
        row = t.add_row().cells
        row[0].text = c
        row[1].text = "%.1f" % cat[c]["national"]
        row[2].text = "%.1f" % cat[c]["largest"]
        row[3].text = "Own sub-index" if cat[c]["publish"] else "Other food"
    for r in t.rows:
        for c in r.cells:
            for p in c.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(9)
    para("Source: movement table, retail year 2026, accepted loads; committee 2026 format weights. Categories "
         "ordered by largest gap within each group.", size=8, color="5F6870", after=6)
    worst = F["closest"]["category"]
    wf = max(K.FORMATS, key=lambda f: abs(cat[worst]["gaps"][f]))
    by = {}
    for c in other:
        fs = [f for f in K.FORMATS if abs(cat[c]["gaps"][f]) > K.TOLERANCE]
        by.setdefault(" and ".join(K.FORMAT_LABEL[f].lower() for f in fs), []).append(c)
    parts = ["%s for %s" % (k, ", ".join(v[:-1]) + " and " + v[-1] if len(v) > 1 else v[0]) for k, v in by.items()]
    para("The closest of the %d is %s at %.1f points (%s). The %d left out miss by %.1f points or more, each on the "
         "formats named: %s." % (len(pub), worst, F["closest"]["gap"], K.FORMAT_LABEL[wf].lower(), len(other),
                                 F["nearest_left"]["miss"], "; ".join(parts)))

    para("The panel behind the figures", bold=True, size=11.5)
    tk = F["takings"]
    para("Panel stores took A$%.1f million in supermarkets, A$%.1f million in neighbourhood stores, A$%.1f million "
         "in convenience stores and A$%.1f million online over the 52 weeks while they were in the panel. Four chains' "
         "store sales rows carry the store's weekly total on each department row (Food and Non-food show the same "
         "figure every week); those are counted once a store a week. The July chain's store sales from before its agreement, the "
         "rejected April resend and the Sunday week-endings of one convenience chain are handled as the delivery "
         "log and partner register set out." % (tk["supermarket"], tk["neighbourhood"], tk["convenience"],
                                                 tk["online"]))
    cs = F["continuous"]
    para("Stores sending data in every week their chain was in the panel: %s. A store re-coded after a refit is "
         "counted once, by its trading name and address; stores closed for a refurbishment, opened or closed during "
         "the year are not counted." % "; ".join("%s %d" % (K.CH[c]["banner"], cs[c]) for c in K.CHAIN_CODES))

    para("Promotions", bold=True, size=11.5)
    ps = {c: cat[c]["promotion"] for c in K.CATS}
    hi, lo = max(ps, key=ps.get), min(ps, key=ps.get)
    para("Between %.1f per cent (%s) and %.1f per cent (%s) of each category's spending was at catalogue specials. "
         "Store markdowns and register price checks are not counted. One convenience chain coded its specials PC "
         "until the week ending 8 August 2026 and TPR from then, PC since marking price check overrides as its code "
         "list supplied on 3 August 2026 has it; its earlier PC sales are counted as specials. Each category's share is on the Structure sheet "
         "of the workbook." % (ps[lo], lo, ps[hi], hi))
    para("Notes", bold=True, size=9.5, after=2)
    para("1. Gaps are each format's change less the national change, taken before rounding; the national change "
         "weights the formats 59.6 supermarket, 16.3 neighbourhood, 7.1 convenience and 17.0 online (terms of "
         "reference, Table 1).", size=8.5, after=2)
    para("2. The July chain's stores enter the supermarket index from their first week in the panel, the week ending "
         "4 July 2026; its store sales from before its agreement are left out of the panel's sales.", size=8.5,
         after=2)
    para("3. The figures by category, format and chain are in gpi_2027_structure.xlsx.", size=8.5, after=2)
    doc.core_properties.author = K.PEOPLE["head"]
    doc.core_properties.title = "Paper 3: the 2027 GPI publication structure"
    doc.save(path)


def _page_field(p):
    """A PAGE field, as Word writes it, at the end of paragraph p."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    run = p.add_run()
    for kind, text in (("begin", None), (None, "PAGE"), ("separate", None), (None, None), ("end", None)):
        if kind:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), kind)
            run._r.append(el)
        elif text:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = " %s " % text
            run._r.append(el)
        else:
            el = OxmlElement("w:t")
            el.text = "1"
            run._r.append(el)


def write(target, golden_dir, T=None):
    os.makedirs(golden_dir, exist_ok=True)
    R = G.compute(target)
    F = figures(R)
    xl = os.path.join(golden_dir, K.DELIVERABLES[0])
    dx = os.path.join(golden_dir, K.DELIVERABLES[1])
    png = os.path.join(HERE, ".chart.png")
    chart(png, F)
    workbook(xl, F)
    paper(dx, F, png)
    os.remove(png)
    PP.COMPANY = K.FIRM
    PP.normalize_ooxml(xl, K.PEOPLE["head"], K.PEOPLE["head"], "2026-12-03T22:05:11Z", "2026-12-06T20:48:37Z",
                       excel=True)
    PP.normalize_ooxml(dx, K.PEOPLE["head"], K.PEOPLE["head"], "2026-12-04T03:12:40Z", "2026-12-06T21:19:02Z")
    json.dump(F, open(os.path.join(HERE, "figures.json"), "w"), indent=1)
    meta = {"distractor_files": ["target/" + K.FILES[k] for k in K.DISTRACTORS]}
    json.dump(meta, open(os.path.join(os.path.dirname(HERE), "metadata.json"), "w"), indent=2)
    print("goldens:", K.DELIVERABLES, "call", F["call"]["count"])
    return R, F
