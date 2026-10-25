"""The goldens: the memo to the Board of Commissioners (reappraisal_recommendation.docx) and the ratio study
workbook (ratio_study_2026_roll.xlsx), both computed from the shipped pack, and generator/figures.json, which the
write-up is drafted from."""
import json
import os
import shutil
import tempfile

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt   # noqa: E402
import numpy as np                # noqa: E402

import analysis as AN             # noqa: E402
import asks as AK                 # noqa: E402
import common as K                # noqa: E402
import pack as PK                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CHART = "value_change_2025_2026.png"
SOLD, UNSOLD, INK, GREY = "#b4532a", "#2f6690", "#1d2326", "#5b646b"


def r2(x):
    return float("%.2f" % (x + 1e-12))


def results(target):
    pk = PK.Pack(target)
    o = AN.main(pk)
    o["ask_a"] = AK.ask_a(pk, "golden")
    o["ask_b"] = AK.ask_b(pk, "golden")
    o["pk"] = pk
    r26, r25 = AN.sf_frames(pk)
    o["changes"] = AN.changes(pk, r26, r25)
    o["study"] = AN.q_sales(pk, r26)
    o["r25"] = r25
    return o


# ---------------------------------------------------------------------------------------------- figures.json
def figures(o):
    g, e = o["golden"], o["easy"]
    A, B = o["ask_a"], o["ask_b"]
    level, cod = round(g[0], 2), int(round(g[1]))
    fail = level < K.STANDARD["level_lo"] or cod > K.STANDARD["cod_max"]
    sentence = ("Accept the vendor's offer of the county-wide single-family reappraisal: the 2026 single-family roll "
                "fails Rule 18-7 on both tests, a median assessment ratio of %.2f against 0.900 to 1.100 and a "
                "coefficient of dispersion of %d against 15.0 or less." % (level, cod))
    areas = {str(a): dict(name=nm, parcels=B[a]["parcels"], value_off=B[a]["off"]) for a, nm in K.AREAS}
    return dict(
        call=dict(sentence=sentence, fails=bool(fail), level=level, cod=cod, level_raw=round(g[0], 4),
                  cod_raw=round(g[1], 3)),
        evidence=dict(sold_change_pct=round(100 * (o["chg_sold"] - 1), 1),
                      unsold_change_pct=round(100 * (o["chg_unsold"] - 1), 1),
                      reviewed_parcels=o["reviewed_n"], single_family_parcels=o["r1_n"],
                      reviewed_share_pct=round(100 * o["share"], 1), unsold_share_pct=round(100 * (1 - o["share"]), 1),
                      study_sales=o["study_n"], set_aside_sales=o["reviewed_n"] - o["study_n"]),
        default_path=dict(level=round(e[0], 2), cod=round(e[1], 1), level_raw=round(e[0], 4), cod_raw=round(e[1], 3)),
        routes=dict(rollfwd=[round(o["rollfwd"][0], 2), round(o["rollfwd"][1], 1)],
                    roll2025=[round(o["roll2025_study"][0], 2), round(o["roll2025_study"][1], 1)],
                    all_q=[round(o["easy_all_q"][0], 2), round(o["easy_all_q"][1], 1)]),
        family={k: [round(v[0], 4), round(v[1], 3)] for k, v in o["family"].items()},
        ask_a=dict(sales=A["n"], level=round(A["level"], 2), agg=round(A["agg"], 3), cod=round(A["cod"], 1),
                   prd=round(A["prd"], 3), level_raw=round(A["level"], 5), agg_raw=round(A["agg"], 5),
                   cod_raw=round(A["cod"], 4), prd_raw=round(A["prd"], 5)),
        ask_b=areas,
        ask_b_total=dict(parcels=sum(B[a]["parcels"] for a, _ in K.AREAS),
                         value_off=sum(B[a]["off"] for a, _ in K.AREAS)),
        standard=dict(level_lo=K.STANDARD["level_lo"], level_hi=K.STANDARD["level_hi"], cod_max=K.STANDARD["cod_max"],
                      prd_lo=K.STANDARD["prd_lo"], prd_hi=K.STANDARD["prd_hi"]),
        index=dict(jan2026=o["pk"].idx["2026-01"], jan2025=o["pk"].idx["2025-01"]),
        rounding=dict(value=100),
        cert_2025=K.CERT_2025.strftime("%-d %B %Y"),
        condo_meets=bool(K.STANDARD["level_lo"] <= round(A["level"], 2) <= K.STANDARD["level_hi"] and
                         round(A["cod"], 1) <= K.STANDARD["cod_max"]),
    )


# ---------------------------------------------------------------------------------------------- chart
def chart(path, o, F):
    ch = o["changes"]
    sold = 100 * (ch.loc[ch["sold"], "chg"] - 1)
    unsold = 100 * (ch.loc[~ch["sold"], "chg"] - 1)
    bins = np.arange(-30, 61, 2.5)
    fig, ax = plt.subplots(figsize=(7.0, 3.3), dpi=150)
    wu = np.full(len(unsold), 100.0 / len(unsold))
    ws = np.full(len(sold), 100.0 / len(sold))
    ax.hist(np.clip(unsold, -30, 60), bins=bins, weights=wu, color=UNSOLD, alpha=.85, rwidth=.86,
            label="Not sold in 2025 (%s parcels)" % format(len(unsold), ","))
    ax.hist(np.clip(sold, -30, 60), bins=bins, weights=ws, color=SOLD, alpha=.80, rwidth=.86,
            label="Sold at arm's length in 2025 (%s parcels)" % format(len(sold), ","))
    ax.axvline(F["evidence"]["unsold_change_pct"], color=UNSOLD, lw=1.0, ls=":")
    ax.axvline(F["evidence"]["sold_change_pct"], color=SOLD, lw=1.0, ls=":")
    ax.text(F["evidence"]["unsold_change_pct"] + .8, ax.get_ylim()[1] * .92, "median %.1f%%" %
            F["evidence"]["unsold_change_pct"], fontsize=7, color=UNSOLD)
    ax.text(F["evidence"]["sold_change_pct"] + .8, ax.get_ylim()[1] * .55, "median %.1f%%" %
            F["evidence"]["sold_change_pct"], fontsize=7, color=SOLD)
    ax.set_xlabel("Change in assessed value, 2025 roll to 2026 roll (%)", fontsize=8)
    ax.set_ylabel("Share of parcels (%)", fontsize=8)
    ax.tick_params(labelsize=7.5)
    ax.set_xlim(-30, 60)
    ax.legend(fontsize=7, frameon=False, loc="upper right")
    ax.set_title("Single-family parcels sold in 2025 were revalued toward their prices", fontsize=8.8, loc="left",
                 color=INK)
    ax.grid(axis="y", color="#e6e9ec", lw=.6)
    ax.set_axisbelow(True)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    fig.subplots_adjust(left=.08, right=.98, top=.9, bottom=.15)
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


# ---------------------------------------------------------------------------------------------- workbook
def _head(ws, row, head, widths=None):
    from openpyxl.styles import Alignment, Font, PatternFill
    for j, h in enumerate(head):
        c = ws.cell(row=row, column=j + 1, value=h)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="2C3E57")
        c.alignment = Alignment(wrap_text=True, vertical="center")
    if widths:
        from openpyxl.utils import get_column_letter
        for j, wd in enumerate(widths):
            ws.column_dimensions[get_column_letter(j + 1)].width = wd


def workbook(path, o, F):
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Summary"
    ws.append(["Tillford County: the 2026 roll on State Tax Commission Rule 18-7"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Budget and Policy Analysis, for the Board of Commissioners' work session of 6 October 2026"])
    ws["A2"].font = Font(italic=True, size=9, color="5B646B")
    ws.append([])
    _head(ws, 4, ["Class", "Median assessment ratio (level)", "Coefficient of dispersion", "Price-related differential",
                  "Sales", "Rule 18-7, 4.1", "Aggregate ratio"], [34, 18, 18, 18, 10, 16, 14])
    ws.append(["Single-family (R1), the roll as certified", F["call"]["level"], F["call"]["cod"], None,
               F["evidence"]["study_sales"], "Fails" if F["call"]["fails"] else "Meets", None])
    ws.cell(5, 2).number_format = "0.00"
    ws.cell(5, 3).number_format = "0"
    A = F["ask_a"]
    ws.append(["Condominium (R2)", A["level"], A["cod"], A["prd"], A["sales"],
               "Meets" if (K.STANDARD["level_lo"] <= A["level"] <= K.STANDARD["level_hi"] and
                           A["cod"] <= K.STANDARD["cod_max"]) else "Fails", A["agg"]])
    ws.cell(6, 7).number_format = "0.000"
    ws.cell(6, 2).number_format = "0.00"
    ws.cell(6, 3).number_format = "0.0"
    ws.cell(6, 4).number_format = "0.000"
    ws.append([])
    ev = F["evidence"]
    ws.append(["Single-family sales as they stand (2026 value over indexed price)", F["default_path"]["level"],
               F["default_path"]["cod"], None, ev["study_sales"], "not the roll"])
    ws.cell(8, 2).number_format = "0.00"
    ws.cell(8, 3).number_format = "0.0"
    ws.append([])
    ws.append(["Single-family parcels on the 2026 roll", ev["single_family_parcels"]])
    ws.append(["Of which sold at arm's length in 2025 and reviewed", ev["reviewed_parcels"]])
    ws.append(["Median change 2025 to 2026, sold parcels (%)", ev["sold_change_pct"]])
    ws.append(["Median change 2025 to 2026, all other parcels on both rolls (%)", ev["unsold_change_pct"]])
    for rr in (10, 11):
        ws.cell(rr, 2).number_format = "#,##0"
    for rr in (12, 13):
        ws.cell(rr, 2).number_format = "0.0"
    ws.freeze_panes = "A5"

    # the single-family study, sale by sale
    st = o["study"].sort_values(["deed_date", "pid26"])
    fac = o["factors"]
    ws2 = wb.create_sheet("Single-family sales")
    _head(ws2, 1, ["Parcel", "Neighbourhood", "Deed date", "Price (USD)", "Index carry", "Price at 1 Jan 2026",
                   "2025 value", "Neighbourhood factor", "Carried-forward value", "2026 value",
                   "Ratio, 2026 value", "Ratio, carried forward"], [12, 11, 11, 12, 10, 14, 12, 12, 14, 12, 11, 12])
    av25 = st["pid26"].map(o["r25"]["Total Assessed"])
    for (_, x), v25 in zip(st.iterrows(), av25):
        f = fac[x["nbhd"]]
        cf = round(v25 * f, -2)
        ws2.append([x["pid26"], x["nbhd"], x["deed_date"].date(), int(x["consideration"]), round(x["carry"], 6),
                    round(x["price_jan26"], 2), int(v25), round(f, 6), int(cf), int(x["av26"]),
                    round(x["av26"] / x["price_jan26"], 4), round(cf / x["price_jan26"], 4)])
    for row in ws2.iter_rows(min_row=2):
        row[2].number_format = "yyyy-mm-dd"
        for j in (3, 5, 6, 8, 9):
            row[j].number_format = "#,##0"
        row[4].number_format = "0.0000"
        row[7].number_format = "0.0000"
        row[10].number_format = "0.0000"
        row[11].number_format = "0.0000"
    ws2.freeze_panes = "A2"
    ws2.auto_filter.ref = "A1:L%d" % ws2.max_row

    # neighbourhood factors
    ws3 = wb.create_sheet("Neighbourhood factors")
    _head(ws3, 1, ["Neighbourhood", "Name", "Market area", "Parcels not sold (both rolls)", "Factor (median change)",
                   "Parcels sold", "Sold parcels' median change"], [13, 20, 12, 16, 14, 11, 16])
    ch = o["changes"]
    cw = o["pk"].crosswalk.set_index("nbhd_code")
    for code in sorted(fac):
        c = ch[ch["nbhd"] == code]
        ws3.append([code, cw.at[code, "nbhd_name"], int(cw.at[code, "market_area"]), int((~c["sold"]).sum()),
                    round(fac[code], 4), int(c["sold"].sum()), round(float(c.loc[c["sold"], "chg"].median()), 4)])
    ws3.freeze_panes = "A2"

    # Board of Review
    ws4 = wb.create_sheet("Board of Review")
    _head(ws4, 1, ["Market area", "Name", "Parcels reduced", "Value taken off the 2025 roll (USD)"], [12, 16, 15, 22])
    for a, nm in K.AREAS:
        b = F["ask_b"][str(a)]
        ws4.append([a, nm, b["parcels"], b["value_off"]])
    ws4.append(["Total", None, F["ask_b_total"]["parcels"], F["ask_b_total"]["value_off"]])
    ws4.cell(ws4.max_row, 1).font = Font(bold=True)
    for row in ws4.iter_rows(min_row=2):
        row[3].number_format = "#,##0"
    ws4.append([])
    ws4.append(["Appeals of the 2025 roll only: hearings from 2 June 2025 on an appeal from the parcel's certified 2025 "
                "value. Each parcel counts once, at the last decision in its case."])
    ws4.cell(ws4.max_row, 1).font = Font(italic=True, size=8.5, color="5B646B")
    ws4.freeze_panes = "A2"

    # notes
    ws5 = wb.create_sheet("Notes")
    notes = [
        "Rule 18-7, 2.1 and 2.2: the level is the median, over every parcel of the class on the certified roll, sold "
        "or not, of its assessed value over its market value on 1 January 2026; the COD is the average absolute "
        "difference from the level as a percentage of it.",
        "Rule 18-7, 3.1 and 3.2: market value is evidenced by the 2025 arm's-length sales (validation code Q), each "
        "price carried by the index for January 2026 (%.1f) over the index for the deed's month; sales are set aside "
        "where improvements or boundaries changed after the deed (%d single-family sales, permit work finaled after "
        "the sale)." % (F["index"]["jan2026"], F["evidence"]["set_aside_sales"]),
        "The %s parcels sold at arm's length in 2025 were reviewed and revalued for 2026; every other parcel moved by "
        "its neighbourhood's factor. A sold parcel's 2025 value times its neighbourhood's factor over its indexed price "
        "stands for the parcels that did not sell (%.1f per cent of the class), its 2026 value over its indexed price "
        "for the reviewed parcels (%.1f per cent); the level and COD are taken over the two together at those shares."
        % (format(F["evidence"]["reviewed_parcels"], ","), F["evidence"]["unsold_share_pct"],
           F["evidence"]["reviewed_share_pct"]),
        "Condominiums: Wexley Commons was re-declared on 1 July 2025; deeds signed and permits issued before then "
        "carry the old unit numbers and are read through the parcel change log. Sales of units combined, or "
        "remodelled under a permit finaled, after the deed are set aside.",
        "Sources: assessor_roll_2026_certified.csv, assessor_roll_2025_certified.xlsx, recorder_deeds_2025.csv, "
        "residential_price_index_tillford.csv, building_permits_2025.csv, parcel_change_log_2025.csv, "
        "board_of_review_hearings_2025.csv, neighborhood_crosswalk.csv.",
    ]
    ws5.column_dimensions["A"].width = 120
    for n in notes:
        ws5.append([n])
    wb.save(path)


# ---------------------------------------------------------------------------------------------- memo
def memo(path, o, F, png):
    import docx
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Mm, Pt, RGBColor
    GREYC = RGBColor(0x5B, 0x64, 0x6B)
    doc = docx.Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(9.5)
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(215.9), Mm(279.4)
    sec.left_margin = sec.right_margin = Mm(19)
    sec.top_margin, sec.bottom_margin = Mm(13), Mm(12)
    hp = sec.header.paragraphs[0]
    hp.text = "Tillford County | Office of the County Administrator | Board of Commissioners work session, 6 October 2026"
    hp.runs[0].font.size = Pt(7.5)
    hp.runs[0].font.color.rgb = GREYC

    def para(text="", size=None, bold=False, color=None, after=3, before=0):
        p = doc.add_paragraph()
        if text:
            r = p.add_run(text)
            r.bold = bold
            if size:
                r.font.size = Pt(size)
            if color:
                r.font.color.rgb = color
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.space_before = Pt(before)
        return p

    for k, v in (("To", "Board of Commissioners (Chair: %s)" % K.PEOPLE["board_chair"]),
                 ("Through", "%s, County Administrator" % K.PEOPLE["administrator"]),
                 ("From", "Budget and Policy Analysis"),
                 ("Date", "1 October 2026"),
                 ("Re", "The reappraisal offer: the 2026 residential roll under State Tax Commission Rule 18-7")):
        p = para(after=0)
        r = p.add_run("%s:\t" % k)
        r.bold = True
        p.add_run(v)
    ev, c = F["evidence"], F["call"]
    para("The 2026 single-family roll fails Rule 18-7; accept the reappraisal offer", 13, bold=True, before=8, after=4)
    p = para(after=4)
    p.add_run("Accept the vendor's offer of the county-wide single-family reappraisal before it lapses on 30 October. "
              "Measured over every single-family "
              "parcel on the certified 2026 roll, the median assessment ratio is %.2f against the rule's 0.900 to "
              "1.100 and the coefficient of dispersion is %d against 15.0 or less, so the class fails both tests and "
              "the Commission will order the reappraisal for the 1 January 2028 roll." % (c["level"], c["cod"])).bold = True
    para("Run the State's study the usual way, on the 2025 arm's-length sales against the 2026 values, and the roll "
         "appears to pass comfortably: a median of %.2f and a COD of %.1f. Those sales no longer measure the roll. The "
         "Assessor's office reviewed each single-family parcel that sold in 2025 and moved its 2026 value toward the "
         "price: the %s parcels sold rose a median %.1f per cent from the 2025 roll, while the other parcels moved by "
         "their neighbourhoods' trend factors, %.1f per cent at the median. A ratio study assumes the sold parcels were "
         "valued like the rest, and here they were not."
         % (F["default_path"]["level"], F["default_path"]["cod"], format(ev["reviewed_parcels"], ","),
            ev["sold_change_pct"], ev["unsold_change_pct"]), after=4)
    para("The roll was therefore measured with the parcels that did not sell represented by the sold parcels as they "
         "would have stood without the review: each sold parcel's 2025 value times its neighbourhood's factor (the "
         "median change of the neighbourhood's parcels that did not sell), over its price carried to 1 January 2026. "
         "Those ratios stand for the %.1f per cent of the class that did not sell; the reviewed parcels' own ratios "
         "stand for the other %.1f per cent. The %s sales left after Rule 18-7's set-asides carry both." %
         (ev["unsold_share_pct"], ev["reviewed_share_pct"], format(ev["study_sales"], ",")), after=4)
    doc.add_picture(png, width=Mm(172))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    A = F["ask_a"]
    meets = K.STANDARD["level_lo"] <= A["level"] <= K.STANDARD["level_hi"] and A["cod"] <= K.STANDARD["cod_max"]
    para("Condominiums", 10.5, bold=True, before=6, after=2)
    para("The condominium class %s the rule on its %d sales: a median ratio of %.2f, an aggregate ratio of %.3f, a "
         "COD of %.1f and a price-related differential of %.3f. The Assessor values condominiums by project and did not revalue sold "
         "units, so the sales measure this class as they stand, less the sales of units remodelled under a permit "
         "finaled after the sale. Wexley Commons' units were renumbered when the project was re-declared on 1 July "
         "2025; deeds signed and permits issued before then carry the old numbers and are matched through the "
         "Assessor's change log, and the sales of units combined afterwards are set aside."
         % ("meets" if meets else "fails", A["sales"], A["level"], A["agg"], A["cod"], A["prd"]), after=4)
    para("Board of Review reductions of the 2025 roll", 10.5, bold=True, before=6, after=2)
    tb = doc.add_table(rows=1, cols=4)
    tb.style = "Light List"
    for i, t in enumerate(["Market area", "", "Parcels reduced", "Value taken off (USD)"]):
        tb.rows[0].cells[i].text = t
    for a, nm in K.AREAS:
        b = F["ask_b"][str(a)]
        cells = tb.add_row().cells
        cells[0].text = str(a)
        cells[1].text = nm
        cells[2].text = "{:,}".format(b["parcels"])
        cells[3].text = "{:,}".format(b["value_off"])
        for i in (2, 3):
            cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    cells = tb.add_row().cells
    cells[0].text = "Total"
    cells[2].text = "{:,}".format(F["ask_b_total"]["parcels"])
    cells[3].text = "{:,}".format(F["ask_b_total"]["value_off"])
    for i in (2, 3):
        cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    para("Single-family and condominium parcels. The Board's 2025 hearing log also holds appeals of the 2024 roll "
         "heard from January to May 2025, before the 2025 roll was certified; they are not counted. A case heard a "
         "second time counts once, at its last decision.", 7.5, color=GREYC, before=2, after=4)
    para("Sources: the Assessor's certified 2025 and 2026 rolls and parcel change log, the Recorder's 2025 deed "
         "extract, Building Services' 2025 permits, the Board of Review's 2025 hearing log and the Division's price "
         "index for Tillford County (January 2026 = %.1f on January 2025 = 100). The workbook "
         "ratio_study_2026_roll.xlsx carries every sale." % F["index"]["jan2026"], 7.5, color=GREYC, after=0)
    doc.save(path)


def write(target, golden):
    os.makedirs(golden, exist_ok=True)
    o = results(target)
    F = figures(o)
    xp = os.path.join(golden, K.GOLDEN_BOOK)
    workbook(xp, o, F)
    tmp = tempfile.mkdtemp()
    png = os.path.join(tmp, CHART)
    chart(png, o, F)
    memo(os.path.join(golden, K.GOLDEN_MEMO), o, F, png)
    shutil.rmtree(tmp)
    res = {k: v for k, v in o.items() if k not in ("pk",)}
    return F, res


def write_figures(path, fig):
    with open(path, "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
        f.write("\n")
