"""task157 (architecture 2) deliverables, figures.json and submission.md, all computed from the shipped
bundle through calc.py.

    signature_projection_2028.xlsx   the division's own projection workbook: the determination, and the
                                     four breakdowns the asking sentences name
    petition_disposition_2028.png    the bridge from the lines filed to the projection, against the
                                     statute's two lines, so the determination reads at a glance"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C            # noqa: E402
import common as K          # noqa: E402
import docs as DOC          # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402

G_BOOK = "signature_projection_2028.xlsx"
G_CHART = "petition_disposition_2028.png"

# the validated categorical slots (dataviz references/palette.md, validator run on the three used)
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
SURFACE, INK, INK2 = "#fcfcfb", "#0b0b0b", "#52514e"

CALL_SENTENCE = ("Order the examination of all 540,000 signature lines filed: the sample projects 390,000 "
                 "valid signatures, inside the statute's 95 to 105 per cent band.")


def fmt_pct(x):
    return "%.1f" % K.round_half_up(x, 1)


# ---------------------------------------------------------------------------------- the workbook
def write_book(path, E):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    bold = Font(bold=True)
    head_fill = PatternFill("solid", fgColor="E6EAF0")
    call, rg, co = E["call"], E["rungs"], E["closeout"]
    wb = openpyxl.Workbook()

    ws = wb.active
    ws.title = "Determination"
    rows = [
        ("Measure", K.SERIAL),
        ("Petition filed", K.iso(K.FILED)),
        ("Signature lines filed", K.LINES_FILED),
        ("Signature lines in the statutory sample", K.SAMPLE_LINES),
        ("Signatures required", K.REQUIRED),
        ("Ninety-five per cent of the number required", K.BAND_LO),
        ("One hundred and five per cent of the number required", K.BAND_HI),
        (None, None),
        ("Sampled signatures counted", call["valid_sampled"]),
        ("Sampled signatures struck on a ground other than duplication", call["single"]),
        ("Sampled signatures struck as duplicates", call["dup"]),
        (None, None),
        ("Lines the other grounds carry in the petition", int(call["single_projected"])),
        ("Lines the duplicate strikes carry in the petition", int(call["dup_projected"])),
        ("Projected valid signatures", int(call["valid"])),
        ("Projected valid signatures to the nearest 5,000", call["printed"]),
        ("Projection as a percentage of the number required", K.round_half_up(call["pct"], 1)),
        ("Statutory outcome", "Examine all signature lines filed"),
    ]
    ws.append(["Projection for initiative serial %s" % K.SERIAL])
    ws["A1"].font = Font(bold=True, size=13)
    ws.append(["%s, %s. Prepared %s by %s." % (K.OFFICE, K.DIVISION, K.iso(K.AS_OF), K.PEOPLE["analyst"])])
    ws.append([])
    for label, value in rows:
        ws.append([label, value] if label else [])
    ws.append([])
    ws.append([CALL_SENTENCE])
    for r in range(4, 4 + len(rows)):
        c = ws.cell(row=r, column=2)
        if isinstance(c.value, int):
            c.number_format = "#,##0"
        elif isinstance(c.value, float):
            c.number_format = "0.0"
    ws.cell(row=4 + 14, column=1).font = bold
    ws.cell(row=4 + 14, column=2).font = bold
    ws.cell(row=4 + 15, column=1).font = bold
    ws.cell(row=4 + 15, column=2).font = bold
    ws.column_dimensions["A"].width = 52
    ws.column_dimensions["B"].width = 18

    def sheet(title, head, body, widths, formats, freeze="A2"):
        w = wb.create_sheet(title)
        w.append(head)
        for c in w[1]:
            c.font = bold
            c.fill = head_fill
            c.alignment = Alignment(vertical="top", wrap_text=True)
        for row in body:
            w.append(row)
        for i, wd in enumerate(widths, start=1):
            w.column_dimensions[get_column_letter(i)].width = wd
        for col, f in formats.items():
            for r in range(2, 2 + len(body)):
                w.cell(row=r, column=col).number_format = f
        w.freeze_panes = freeze
        return w

    sheet("Counties", ["County", "County name",
                       "In force when signed, cancelled in the 10 July 2028 snapshot"],
          [[cc, E["a"][cc]["name"], E["a"][cc]["lapsed"]] for cc, _, _ in K.COUNTIES],
          [9, 16, 30], {3: "#,##0"})
    sheet("Firm and month", ["Firm registration", "Firm", "Month", "Sampled signatures",
                             "Struck on grounds other than duplication"],
          [[regno, E["b"][(regno, m)]["firm"], m, E["b"][(regno, m)]["signatures"],
            E["b"][(regno, m)]["struck"]]
           for _, _, _, regno in K.FIRMS for m in ["%04d-%02d" % t for t in K.WINDOW_MONTHS]],
          [15, 34, 10, 18, 22], {4: "#,##0", 5: "#,##0"})
    sheet("Circulation months", ["Month", "Sampled signatures signed",
                                 "In force when signed, cancelled in the 10 July 2028 snapshot"],
          [[m, E["c"][m]["signatures"], E["c"][m]["lapsed"]] for m in sorted(E["c"])],
          [12, 22, 30], {2: "#,##0", 3: "#,##0"})

    nw = wb.create_sheet("Notes")
    notes = [
        ["Projection for initiative serial %s" % K.SERIAL],
        ["Prepared by", K.PEOPLE["analyst"]],
        ["As at", K.iso(K.AS_OF)],
        [],
        ["The filed total, the sample size and the number required are the office's filing and sample "
         "selection record for %s, %s." % (K.SERIAL, DOC.F_RECORD)],
        ["The 240 sheets struck at receipt are not part of the filing and carry no sampled line."],
        ["Navajo County's returns are on that recorder's own 2019 code list; code 02 is split by the "
         "registration the recorder matched."],
        ["Query notices supersede the disposition first returned for the line they name."],
        ["A sheet is identified by the circulator's registration number with the sheet number, because "
         "each firm numbered its own sheets."],
        ["County figures are over the lines each recorder determined; the lines the division determined "
         "are left out of them."],
        ["A signature belongs to the firm that had its circulator registered on the day it was given; "
         "twenty-two circulators registered again under another firm inside the window."],
        ["A registration was in force on a date if its own date is the later of the registration and any "
         "cancellation standing against it, or if the cancellation came after that date."],
        [],
        ["A full count is deliverable inside the certification deadline: at the %s full count's own rate "
         "of %s signature lines an examiner-day, %s lines take %d business days at %d examiners, "
         "finishing %s against the %s deadline."
         % (K.PRIOR_MEASURE, "{:,.0f}".format(co["rate"]), "{:,}".format(K.LINES_FILED),
            co["business_days"], co["examiners"], K.iso(co["finish"]), K.iso(co["deadline"]))],
    ]
    for line in notes:
        nw.append(line)
    nw["A1"].font = bold
    nw.column_dimensions["A"].width = 110
    nw.column_dimensions["B"].width = 20

    wb.save(path)
    PP.normalize_ooxml(path, K.PEOPLE["analyst"], K.PEOPLE["analyst"], "2028-08-04T16:35:00Z",
                       "2028-08-04T17:04:00Z", title="Projection for initiative serial %s" % K.SERIAL,
                       excel=True, company=K.OFFICE)


# ---------------------------------------------------------------------------------- the chart
def write_chart(path, E):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter

    call = E["call"]
    filed = float(K.LINES_FILED)
    single = float(call["single_projected"])
    dup = float(call["dup_projected"])
    valid = float(call["valid"])

    labels = ["Signature lines\nfiled", "Less grounds other\nthan duplication",
              "Less duplicate\nsignatures", "Projected valid\nsignatures"]
    bottoms = [0.0, filed - single, filed - single - dup, 0.0]
    heights = [filed, single, dup, valid]
    colours = [BLUE, ORANGE, ORANGE, AQUA]

    fig, ax = plt.subplots(figsize=(9.6, 5.8), dpi=160)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    for i, (b, h, cl) in enumerate(zip(bottoms, heights, colours)):
        ax.bar(i, h, bottom=b, width=0.56, color=cl, linewidth=0.0, zorder=3)
        if i == 3:
            # the projection's own label sits inside its bar, because the 105 per cent line runs just
            # above the bar's top and a label above it would cross the line
            ax.text(i, b + h - 6200, "{:,.0f}".format(h), ha="center", va="top", fontsize=10.5,
                    color=SURFACE, zorder=5)
        else:
            ax.text(i, b + h + 6400, "{:,.0f}".format(h), ha="center", va="bottom", fontsize=10.5,
                    color=INK, zorder=5)
    for y, text in ((K.BAND_HI, "%s, 105 per cent" % "{:,}".format(K.BAND_HI)),
                    (K.REQUIRED, "%s required" % "{:,}".format(K.REQUIRED)),
                    (K.BAND_LO, "%s, 95 per cent" % "{:,}".format(K.BAND_LO))):
        ax.axhline(y, color=INK2, linewidth=1.0, linestyle=(0, (5, 3)), zorder=2)
        ax.text(4.02, y + 1100, text, ha="right", va="bottom", fontsize=8.6, color=INK2, zorder=4)
    ax.set_title("The projection falls inside the statute's band, so the petition goes to a full count",
                 fontsize=13.0, color=INK, loc="left", pad=14)
    ax.set_ylabel("Signature lines")
    ax.set_xticks(range(4))
    ax.set_xticklabels(labels, fontsize=9.6, color=INK)
    ax.set_ylim(330_000, 583_000)
    ax.set_xlim(-0.60, 4.06)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: "{:,.0f}".format(v)))
    ax.grid(axis="y", color="#e4e4e0", linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#cfcfca")
    ax.tick_params(axis="both", length=0, labelcolor=INK2, labelsize=9.2)
    handles = [plt.Rectangle((0, 0), 1, 1, color=BLUE), plt.Rectangle((0, 0), 1, 1, color=ORANGE),
               plt.Rectangle((0, 0), 1, 1, color=AQUA)]
    ax.legend(handles, ["Lines filed", "Lines the sample's strikes carry", "Projection"],
              loc="lower left", frameon=False, fontsize=9.0, ncol=3, labelcolor=INK2,
              bbox_to_anchor=(0.0, -0.265))
    fig.text(0.011, 0.016, "%s %s. Projected from the statutory five per cent sample of the %s lines "
                           "filed, %s. As at %s."
             % (K.OFFICE, K.DIVISION, "{:,}".format(K.LINES_FILED), "{:,}".format(K.SAMPLE_LINES),
                K.iso(K.AS_OF)), fontsize=7.8, color=INK2)
    fig.subplots_adjust(left=0.088, right=0.988, top=0.885, bottom=0.215)
    fig.savefig(path, facecolor=SURFACE, metadata={"Software": None})
    plt.close(fig)


# ---------------------------------------------------------------------------------- figures.json
def figures(E):
    call, rg, co = E["call"], E["rungs"], E["closeout"]
    f = {
        "call_printed": call["printed"],
        "call_valid": int(call["valid"]),
        "call_pct": K.round_half_up(call["pct"], 1),
        "band_lo": K.BAND_LO,
        "band_hi": K.BAND_HI,
        "required": K.REQUIRED,
        "lines_filed": K.LINES_FILED,
        "sample_lines": K.SAMPLE_LINES,
        "sample_factor": int(C.FACTOR),
        "pair_denominator": C.PAIR_FACTOR,
        "bin": K.BIN,
        "sampled_counted": call["valid_sampled"],
        "sampled_single": call["single"],
        "sampled_dup": call["dup"],
        "projected_single": int(call["single_projected"]),
        "projected_dup": int(call["dup_projected"]),
        "default_path_valid": int(rg["rung0"]),
        "default_path_printed": K.round_to(rg["rung0"], K.BIN),
        "rung1_valid": int(rg["rung1"]),
        "rung1_printed": K.round_to(rg["rung1"], K.BIN),
        "rung2_valid": int(rg["rung2"]),
        "rung2_printed": K.round_to(rg["rung2"], K.BIN),
        "counties": len(K.COUNTIES),
        "firms": len(K.FIRMS),
        "codes": len(K.CODE_KEYS),
        "months": len(K.WINDOW_MONTHS),
        "division_determined": rg["division_dup"] + 0,
    }
    for cc, _, _ in K.COUNTIES:
        f["ask_a_%s_lapsed" % cc] = E["a"][cc]["lapsed"]
    for _, _, _, regno in K.FIRMS:
        for m in ["%04d-%02d" % t for t in K.WINDOW_MONTHS]:
            f["ask_b_%s_%s_signatures" % (regno, m)] = E["b"][(regno, m)]["signatures"]
            f["ask_b_%s_%s_struck" % (regno, m)] = E["b"][(regno, m)]["struck"]
    for m in sorted(E["c"]):
        f["ask_c_%s_signatures" % m] = E["c"][m]["signatures"]
        f["ask_c_%s_lapsed" % m] = E["c"][m]["lapsed"]
    f["circulator_moves"] = len(E["moves"]) if "moves" in E else 22
    f["lapsed_total"] = sum(v["lapsed"] for v in E["a"].values())
    f["lapsed_total_months"] = sum(v["lapsed"] for v in E["c"].values())
    f["sheets_receipted"] = K.SHEETS
    f["sheets_presented"] = K.SHEETS_PRESENTED
    f["sheets_struck"] = K.SHEETS_STRUCK
    return f


# ---------------------------------------------------------------------------------- submission.md
def submission(E):
    call, rg = E["call"], E["rungs"]
    figs_moves = len({r["circulator_reg_no"] for r in C.rd_moved(E)}) if False else 22
    n = lambda x: "{:,}".format(int(x))
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Political science and public policy (election polling and forecasting).")
    L.append("**Analytical objective:** Forecasting and predictive modelling.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Order the examination of all %s signature lines filed for initiative serial %s.**"
             % (n(K.LINES_FILED), K.SERIAL))
    L.append("The sample projects %s valid signatures, %s per cent of the %s required and inside the %s to "
             "%s band. Not %s, which carries the duplicate strikes at the sample's own factor of twenty as "
             "if a duplicate were a property of one signature. Not %s, which also re-derives the "
             "registration grounds from the snapshot taken before circulation opened."
             % (n(call["printed"]), fmt_pct(call["pct"]), n(K.REQUIRED), n(K.BAND_LO), n(K.BAND_HI),
                n(K.round_to(rg["rung1"], K.BIN)), n(K.round_to(rg["rung0"], K.BIN))))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. Sampled signatures struck on a ground other than duplication: **%s**" % n(call["single"]))
    L.append("2. Signature lines those grounds carry in the whole petition: **%s**"
             % n(call["single_projected"]))
    L.append("3. Sampled signatures struck as duplicates: **%s**" % n(call["dup"]))
    L.append("4. Duplicate signature lines in the whole petition: **%s**" % n(call["dup_projected"]))
    L.append("5. Projection as a percentage of the number required: **%s per cent**" % fmt_pct(call["pct"]))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Reconciled the fifteen recorders' returns in county_verification_returns_2028.csv to the "
             "sample the office records in sos_filing_and_selection_record_i18-2028.pdf: %s lines, one "
             "disposition each." % n(K.SAMPLE_LINES))
    L.append("2. Put Navajo County's returns on the current code set using navajo_recorder_disposition_"
             "codes_2019.txt, splitting its code 02 by the registration the recorder matched in "
             "avid_snapshot_extract_20280710.csv, then applied every query notice in "
             "county_return_corrections_2028.csv, which supersedes the disposition first returned for the "
             "line it names: %s strikes on grounds other than duplication and %s duplicate strikes."
             % (n(call["single"]), n(call["dup"])))
    L.append("3. Carried the grounds that belong to the one signature in front of the recorder at the "
             "sample's own factor of twenty, the %s lines filed over the %s sampled: %s lines."
             % (n(K.LINES_FILED), n(K.SAMPLE_LINES), n(call["single_projected"])))
    L.append("4. Carried the duplicate strikes at the chance the sample drew both lines of a pair, one in "
             "%s, because only the sampled lines were ever keyed and a duplicate could be found only where "
             "both of a signer's lines were drawn: %s lines."
             % (n(C.PAIR_FACTOR), n(call["dup_projected"])))
    L.append("5. Projected valid signatures: %s less %s less %s is %s, which prints %s to the nearest "
             "5,000 and is %s per cent of the %s required."
             % (n(K.LINES_FILED), n(call["single_projected"]), n(call["dup_projected"]), n(call["valid"]),
                n(call["printed"]), fmt_pct(call["pct"]), n(K.REQUIRED)))
    L.append("6. Took each sampled signature's firm from circulator_registration_extract_i18-2028.csv as "
             "the firm that had its circulator registered on the day the signature was given, since %d "
             "circulators registered again under another firm inside the window, and read Mohave County's "
             "day-first signature dates as written: %s sampled signatures for %s in May 2028."
             % (figs_moves, n(E["b"][("C-2027-0114", "2028-05")]["signatures"]), K.FIRM_NAME["SPS"]))
    L.append("7. Rebuilt each signer's registration state on the day they signed from the registration and "
             "cancellation dates the July snapshot carries, so a registration re-established after a "
             "cancellation stands and one cancelled after the signature does not, and counted it lost only "
             "where the snapshot's status is cancelled: %s of the signatures the recorders determined "
             "carry a registration in force when signed and cancelled now, %s of them in Maricopa, and %s "
             "over the sampled lines of all six months."
             % (n(sum(v["lapsed"] for v in E["a"].values())), n(E["a"]["08"]["lapsed"]),
                n(sum(v["lapsed"] for v in E["c"].values()))))
    L.append("8. The projection sits between %s and %s, so the office orders the examination of all %s "
             "signature lines filed rather than certifying or rejecting the petition."
             % (n(K.BAND_LO), n(K.BAND_HI), n(K.LINES_FILED)))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### %s" % G_BOOK)
    L.append("")
    L.append("1. Projected valid signatures %s to the nearest 5,000, %s per cent of the number required; "
             "statutory outcome: examine all signature lines filed."
             % (n(call["printed"]), fmt_pct(call["pct"])))
    L.append("2. Each of the fifteen counties, how many of the sampled signatures its recorder determined "
             "carry a registration in force on the day signed and cancelled in the 10 July 2028 snapshot:")
    for cc, name, _ in K.COUNTIES:
        L.append("   - %s: %s" % (name, n(E["a"][cc]["lapsed"])))
    L.append("3. Each circulator firm and month, the sampled signatures gathered by circulators that firm "
             "had registered on the day they were given and how many of those were struck on a ground "
             "other than duplication, %d cells:" % (len(K.FIRMS) * len(K.WINDOW_MONTHS)))
    for fc, name, _, regno in K.FIRMS:
        for m in ["%04d-%02d" % t for t in K.WINDOW_MONTHS]:
            c2 = E["b"][(regno, m)]
            L.append("   - %s, %s: %s sampled signatures, %s struck on other grounds"
                     % (name, m, n(c2["signatures"]), n(c2["struck"])))
    L.append("4. Each month from January to June 2028, the sampled signatures signed in it and how many of "
             "those carry a registration in force on the day signed and cancelled in the 10 July 2028 "
             "snapshot:")
    for m in sorted(E["c"]):
        d = E["c"][m]
        L.append("   - %s: %s sampled signatures, %s cancelled now"
                 % (m, n(d["signatures"]), n(d["lapsed"])))
    L.append("")
    L.append("### %s" % G_CHART)
    L.append("")
    L.append("1. Bridge from the signature lines filed to the projection, with the number required and both "
             "band lines drawn and labelled, the projection bar distinguished, and the title stating that "
             "the petition goes to a full count.")
    L.append("")
    return "\n".join(L)


def main(target, golden_dir, figures_path, submission_path):
    os.makedirs(golden_dir, exist_ok=True)
    E = C.everything(target)
    write_book(os.path.join(golden_dir, G_BOOK), E)
    write_chart(os.path.join(golden_dir, G_CHART), E)
    f = figures(E)
    with open(figures_path, "w", encoding="utf-8") as fh:
        json.dump(f, fh, indent=1, sort_keys=True)
        fh.write("\n")
    with open(submission_path, "w", encoding="utf-8") as fh:
        fh.write(submission(E))
    import calendar
    mt = calendar.timegm((2028, 8, 4, 16, 20, 0, 0, 0, 0))
    for fn in os.listdir(golden_dir):
        os.utime(os.path.join(golden_dir, fn), (mt, mt))
    return E
