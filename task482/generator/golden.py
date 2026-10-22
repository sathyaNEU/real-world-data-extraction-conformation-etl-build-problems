"""The golden: Form 27A's two placement scores with the expected raw score each rests on, each college's 2026
placements, the conversion the new platform loads, and the expected-score curve. Every figure comes from bundle.py
reading the cut pack; figures.json carries them for the write-up and the checks."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TASK = os.path.dirname(HERE)

import numpy as np   # noqa: E402

import bundle as B   # noqa: E402

COURSE = {"CA": "MATH 131", "CCA": "MATH 131 with MATH 031", "DM": "MATH 091"}
LEVEL_NAME = {"CA": "College Algebra", "CCA": "Corequisite College Algebra", "DM": "Developmental Mathematics"}
NAMES = {"01": "Ashgrove", "02": "Bramblewood", "03": "Calder Flats", "04": "Dellwood", "05": "Embervale",
         "06": "Fennimore Ridge", "07": "Gorseway", "08": "Hartmoor Creek", "09": "Iverton Prairie",
         "10": "Juniper Lake", "11": "Knollwood", "12": "Lowland Mesa", "13": "Marlow Fork", "14": "Nettlefield"}


def r1(x):
    return float("%.1f" % (x + 1e-9))


def compute(target, fast=False):
    b = B.open_pack(target)
    g = B.fit_position(b, "mml", "all")
    F = {}
    e_ca = B.expected(b, B.STANDARDS["CA"], g)
    e_cca = B.expected(b, B.STANDARDS["CCA"], g)
    sc = B.placement_scores(b, g)
    f_ca = B.expected(b, B.STANDARDS["CA"], 0.0, "filed")
    f_cca = B.expected(b, B.STANDARDS["CCA"], 0.0, "filed")
    fs = B.placement_scores(b, 0.0, "filed")
    F["call"] = {"college_algebra_score": sc["CA"], "corequisite_score": sc["CCA"]}
    F["components"] = {"expected_raw_ca": r1(e_ca), "expected_raw_cca": r1(e_cca),
                       "position_effect_logits": float("%.4f" % g), "carry_logits": float("%.2f" % (20 * g)),
                       "unique_items_carried": len(b["unique27"]),
                       "unique_mean_position": 45.5, "field_test_mean_position": 65.5}
    F["rivals"] = {"filed_expected_ca": r1(f_ca), "filed_expected_cca": r1(f_cca),
                   "filed_ca_score": fs["CA"], "filed_cca_score": fs["CCA"]}
    cols = B.colleges(b)
    F["colleges"] = {c: dict(cols[c], name=NAMES[c], code=c) for c in B.CODES}
    F["system"] = {k: sum(cols[c][k] for c in B.CODES) for k in ("placed", "CA", "CCA", "twice")}
    F["conversion"] = {str(r): lv for r, lv in B.conversion(sc)}
    F["standards"] = {"CA": B.STANDARDS["CA"], "CCA": B.STANDARDS["CCA"]}
    F["form"] = {"scored_items": 60, "unique_positions_from": 21, "unique_positions_to": 70,
                 "field_test_positions_from": 61, "field_test_positions_to": 70}
    F["courses"] = {"CA": "MATH 131", "CCA": "MATH 131 with MATH 031", "DM": "MATH 091"}
    F["_unrounded"] = {"gamma": g, "expected_ca": e_ca, "expected_cca": e_cca, "filed_ca": f_ca, "filed_cca": f_cca}
    return F, b


def write_csv(path, F):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("form,raw_score,placement,course\n")
        for r in range(61):
            lv = F["conversion"][str(r)]
            fh.write("27A,%d,%s,%s\n" % (r, lv, COURSE[lv]))


def write_xlsx(path, F):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Form 27A"
    navy = PatternFill("solid", fgColor="1F3D6B")
    thin = Side(style="thin", color="9AA3AF")
    ws["A1"] = "Form 27A placement scores for approval, 18 February 2027"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Brackett Plains Community College System, Office of Assessment and Placement. Form 27A goes live on "
                "Northgate Assess on 1 March 2027.")
    ws.append([])
    ws.append(["Placement", "Standard (logits)", "Expected raw score at the standard", "Placement score",
               "With the bank difficulties as filed"])
    for c in ws[4]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = navy
        c.alignment = Alignment(wrap_text=True, vertical="top")
    C, R = F["components"], F["rivals"]
    ws.append(["College Algebra (MATH 131)", F["standards"]["CA"], C["expected_raw_ca"],
               F["call"]["college_algebra_score"], R["filed_expected_ca"]])
    ws.append(["Corequisite College Algebra (MATH 131 with MATH 031)", F["standards"]["CCA"], C["expected_raw_cca"],
               F["call"]["corequisite_score"], R["filed_expected_cca"]])
    for row in ws.iter_rows(min_row=5, max_row=6):
        row[1].number_format = "0.00"
        row[2].number_format = "0.0"
        row[3].number_format = "0"
        row[4].number_format = "0.0"
        row[3].font = Font(bold=True)
        for c in row:
            c.border = Border(bottom=thin)
    ws.append([])
    ws.append(["Field-test section (mean position 65.5) to Form 27A (mean 45.5), logits", C["carry_logits"]])
    ws.cell(row=ws.max_row, column=2).number_format = "0.00"
    ws.append(["Unique items carried from the field-test section", C["unique_items_carried"]])
    ws.append([])
    notes = [
        "A placement score is the lowest whole raw score at or above the raw score a student exactly at the standard "
        "is expected to reach on the form's 60 scored items (QPI-TR-2027, section 7).",
        "Form 27A's 40 unique items carry the difficulties of their field tests, in the old platform's field-test "
        "section (positions 61 to 70). Fitted to the 2026 attempts, the Rasch model with a position term puts an item "
        "%.2f logits harder at the section's mean position, 65.5, than at 45.5, the mean of the positions 21 to 70 it "
        "can take on Northgate Assess, so each unique item is carried to each of those positions. The anchor block "
        "keeps its bank difficulties: it was calibrated where it sits." % C["carry_logits"],
        "With the bank difficulties as filed the expected raw scores are %.1f and %.1f, placement scores %d and %d."
        % (R["filed_expected_ca"], R["filed_expected_cca"], R["filed_ca_score"], R["filed_cca_score"])]
    for n in notes:
        ws.append([n])
        ws.cell(row=ws.max_row, column=1).alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=ws.max_row, start_column=1, end_row=ws.max_row, end_column=5)
        ws.row_dimensions[ws.max_row].height = 58
    for col, w in zip("ABCDE", (50, 17, 22, 15, 22)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"

    w2 = wb.create_sheet("Colleges 2026")
    w2["A1"] = "QPI placements by college, 1 March 2026 to 31 January 2027"
    w2["A1"].font = Font(bold=True, size=13)
    w2["A2"] = ("Each student once, at the college that placed them on their placing sitting (Policy 4.12, section 3); "
                "attempts in invalidated sessions are not sittings (section 4).")
    w2.append([])
    w2.append(["College", "College name", "Students placed", "College Algebra", "Corequisite College Algebra",
               "Students who sat twice"])
    for c in w2[4]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = navy
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for code in B.CODES:
        r = F["colleges"][code]
        w2.append([code, r["name"] + " Community College", r["placed"], r["CA"], r["CCA"], r["twice"]])
    s = F["system"]
    w2.append([None, "System", s["placed"], s["CA"], s["CCA"], s["twice"]])
    for c in w2[w2.max_row]:
        c.font = Font(bold=True)
        c.border = Border(top=thin)
    for row in w2.iter_rows(min_row=5, max_row=w2.max_row):
        for c in row[2:]:
            c.number_format = "#,##0"
    for col, w in zip("ABCDEF", (9, 36, 16, 16, 18, 16)):
        w2.column_dimensions[col].width = w
    w2.freeze_panes = "C5"
    w2.auto_filter.ref = "A4:F%d" % (w2.max_row - 1)

    w3 = wb.create_sheet("Notes")
    rows = [["Item", "Note"],
            ["As at", "Pack of 5 February 2027: Itemstore assembly pool of 3 February 2027; QPI attempts to 31 January "
             "2027."],
            ["Ability scale", "QPI bank scale, logits; bank units are 500 plus 100 times the logit."],
            ["Students", "One student is one person across both platforms and both student identifiers, matched on "
                         "birth date, sex, high school code and QPI registration date."],
            ["Placing college", "The college the placing sitting's automatic score report went to: the college the "
                                "student was registered through when they sat."],
            ["Sessions", "Attempts in sessions the Office invalidated are left out; sessions whose invalidation was "
                         "withdrawn count."],
            ["Rounding", "Expected raw scores to one decimal; students as whole numbers."]]
    for r in rows:
        w3.append(r)
    for c in w3[1]:
        c.font = Font(bold=True)
    w3.column_dimensions["A"].width = 18
    w3.column_dimensions["B"].width = 100
    for row in w3.iter_rows(min_row=2):
        row[1].alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


def write_svg(path, F, b):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams["svg.hashsalt"] = "task482"
    matplotlib.rcParams["svg.fonttype"] = "none"
    matplotlib.rcParams["font.family"] = "DejaVu Sans"
    g = F["_unrounded"]["gamma"]
    th = np.linspace(-3, 3, 241)
    carried = [B.expected(b, t, g) for t in th]
    filed = [B.expected(b, t, 0.0, "filed") for t in th]
    ink, ink2, blue, grey = "#0b0b0b", "#52514e", "#2a78d6", "#8c8b86"
    fig, ax = plt.subplots(figsize=(8.6, 5.4), dpi=100)
    fig.patch.set_facecolor("#fcfcfb")
    ax.set_facecolor("#fcfcfb")
    ax.plot(th, filed, color=grey, lw=1.6, ls=(0, (5, 3)), zorder=2)
    ax.plot(th, carried, color=blue, lw=2.2, zorder=3)
    for lv, lab in (("CA", "College Algebra"), ("CCA", "Corequisite College Algebra")):
        t = F["standards"][lv]
        e = F["components"]["expected_raw_ca" if lv == "CA" else "expected_raw_cca"]
        s = F["call"]["college_algebra_score" if lv == "CA" else "corequisite_score"]
        ax.axvline(t, color=ink2, lw=0.8, zorder=1)
        ax.axhline(s, xmin=0, xmax=(t + 3) / 6.0, color=blue, lw=0.9, ls=(0, (2, 2)), zorder=1)
        ax.plot([t], [e], marker="o", ms=8, color=blue, mec="#fcfcfb", mew=2, zorder=4)
        xy_text = (0.55, 21.0) if lv == "CA" else (-2.88, 23.6)
        ax.annotate("%s standard %.2f\nexpected raw score %.1f, placement score %d" % (lab, t, e, s), xy=(t, e),
                    xytext=xy_text, fontsize=8.8, color=ink, ha="left",
                    arrowprops=dict(arrowstyle="-", color=ink2, lw=0.7, shrinkA=2, shrinkB=5))
    ax.text(0.92, 45.5, "Form 27A as delivered", color=blue, fontsize=9, ha="right")
    ax.text(1.75, 36.5, "bank difficulties as filed", color=ink2, fontsize=9, ha="left")
    ax.set_xlim(-3, 3)
    ax.set_ylim(0, 60)
    ax.set_yticks(range(0, 61, 10))
    ax.set_xlabel("Ability on the QPI bank scale (logits)", color=ink2, fontsize=9.5)
    ax.set_ylabel("Expected raw score (of 60 scored items)", color=ink2, fontsize=9.5)
    ax.grid(True, color="#e3e2de", lw=0.6)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color("#b9b8b2")
    ax.tick_params(colors=ink2, labelsize=8.5)
    fig.suptitle("Form 27A: College Algebra from a raw score of %d, Corequisite College Algebra from %d"
                 % (F["call"]["college_algebra_score"], F["call"]["corequisite_score"]), x=0.07, ha="left",
                 fontsize=11.5, color=ink, fontweight="bold")
    ax.set_title("Expected raw score by ability, each unique item at the positions it can take on Northgate Assess;\n"
                 "dashed: the bank difficulties as filed (%.1f and %.1f at the standards)"
                 % (F["rivals"]["filed_expected_ca"], F["rivals"]["filed_expected_cca"]), loc="left", fontsize=8.4,
                 color=ink2, wrap=True)
    fig.text(0.07, 0.025, "Source: Itemstore assembly pool, 3 February 2027; QPI attempts, 1 March 2026 to 31 January "
             "2027; QPI-TR-2027. Office of Assessment and Placement.", fontsize=7.4, color=ink2)
    fig.subplots_adjust(left=0.08, right=0.97, top=0.84, bottom=0.16)
    fig.savefig(path, format="svg", metadata={"Date": None, "Creator": None})
    plt.close(fig)
    svg = open(path, encoding="utf-8").read()
    svg = svg.replace('id="matplotlib.', 'id="').replace("<!-- Created with matplotlib (https://matplotlib.org/) -->\n", "")
    import re as _re
    svg = _re.sub(r"\s*<metadata>.*?</metadata>", "", svg, flags=_re.S)
    assert "matplotlib" not in svg.lower()
    open(path, "w", encoding="utf-8").write(svg)


def main(target=None):
    target = target or os.path.join(TASK, "target")
    F, b = compute(target)
    out = os.path.join(TASK, "golden")
    os.makedirs(out, exist_ok=True)
    for fn in os.listdir(out):
        os.remove(os.path.join(out, fn))
    write_xlsx(os.path.join(out, "qpi_placement_review_2027.xlsx"), F)
    write_csv(os.path.join(out, "qpi_form27a_score_conversion.csv"), F)
    write_svg(os.path.join(out, "qpi_form27a_expected_score_curve.svg"), F, b)
    import postprocess as PP
    PP.normalize_ooxml(os.path.join(out, "qpi_placement_review_2027.xlsx"), "Breanna Graham", "Breanna Graham",
                       "2027-02-06T15:20:00Z", "2027-02-09T16:38:04Z", excel=True,
                       company="Brackett Plains Community College System")
    pub = {k: v for k, v in F.items() if not k.startswith("_")}
    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(pub, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("golden: scores %s, expected %.3f / %.3f (gamma %.5f); filed %s" % (
        F["call"], F["_unrounded"]["expected_ca"], F["_unrounded"]["expected_cca"], F["_unrounded"]["gamma"],
        F["rivals"]))
    return F


if __name__ == "__main__":
    main()
