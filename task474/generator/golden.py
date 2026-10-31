"""The golden deliverables (the Board paper and the conformed 2026 record) and submission.md, from figures.json."""
import csv
import datetime as dt
import io
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.platypus import Image  # noqa: E402

import figs as F  # noqa: E402
import pack as K  # noqa: E402
import params as P  # noqa: E402
import routes as R  # noqa: E402
import world as W  # noqa: E402

PDF = "theory_pass_mark_2027.pdf"
CSV = "theory_results_2026.csv"
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September"]


def conformed_rows(target, mark):
    people, reg = F.load(target)
    venue_of = {}
    import json
    hg = json.load(open(os.path.join(target, K.FILES["harrowgate"]), encoding="utf-8"))["sittings"]
    latest = {}
    for pid, ss in people.items():
        latest[pid] = ss[-1]["board"]
    rows = []
    for pid, ss in people.items():
        for i, s in enumerate(ss):
            if not (dt.date(2026, 1, 1) <= s["date"] <= P.LAST_DAY):
                continue
            paper = "Brindle scaled score" if s["vendor"] == "old" else "Harrowgate raw mark"
            passed = s["score"] >= (P.OLD_PASS if s["vendor"] == "old" else mark)
            rows.append([latest[pid], s["board"], s["date"].isoformat(),
                         P.OLD_VENDOR if s["vendor"] == "old" else P.NEW_VENDOR, paper, s["score"], i + 1,
                         "yes" if i == 0 else "no", "pass" if passed else "fail"])
    rows.sort(key=lambda r: (r[2], r[0], r[3]))
    return rows


def write_csv(path, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["board_number", "board_number_at_sitting", "sitting_date", "provider", "result_scale", "mark",
                "attempt", "first_sitting", "result"])
    w.writerows(rows)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())


def chart(path_png, fig):
    xs = [int(k) for k in fig["chart"]]
    ys = [fig["chart"][str(k)] for k in xs]
    mark = fig["call"]["pass_mark"]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "svg.hashsalt": "task474"})
    f, ax = plt.subplots(figsize=(6.4, 3.3), dpi=150)
    ax.plot(xs, ys, color="#2f5d7c", lw=1.8)
    ax.axvline(mark, color="#b23a2e", lw=1.4, ls="--")
    ax.text(mark + 0.4, 92, "pass mark %d" % mark, color="#b23a2e", fontsize=8.5)
    ax.set_xlabel("Raw mark on the new paper (out of 60)")
    ax.set_ylabel("Candidates reaching it (%)")
    ax.set_ylim(0, 100)
    ax.set_xlim(xs[0], xs[-1])
    ax.grid(axis="y", color="#e3e6e8", lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    f.tight_layout()
    f.savefig(path_png, metadata={"Software": None})
    plt.close(f)


def write_pdf(path, fig, tmp_png):
    c = fig["call"]
    chart(tmp_png, fig)
    a, b = fig["ask_a"], fig["ask_b"]
    blocks = [
        ("t", "Theory paper: the pass mark on Harrowgate's paper"),
        ("s", "Paper to the Board, meeting of 4 November 2026. Laura Kay, Head of Qualifications, with Alan Clayton, "
              "Chief Examiner."),
        ("h", "Recommendation"),
        ("p", "Set the pass mark on Harrowgate's theory paper at <b>%d out of 60</b>, for the held results of April to "
              "September 2026 and for every 2027 sitting. It is the mark that holds the standard of 65 on Brindle's "
              "scale under AP-3." % c["pass_mark"]),
        ("h", "How the standard was carried"),
        ("p", "The candidates who failed their first sitting on Brindle's paper and sat Harrowgate's paper next are "
              "the one group measured on both. A second sitting reads higher than a first on any paper, so their "
              "Harrowgate marks were set against what the same candidates would have scored on a second Brindle "
              "sitting: Brindle's own resits of 2021 to 2025, matched on the first score, put %.1f per cent of them "
              "at 65 or more. %d is the lowest raw mark that no more than that share of them reach (%.1f per cent "
              "reach %d; %.1f per cent reach %d)." % (100 * c["p_equivalent"], c["pass_mark"],
                                                     100 * c["share_at_mark"], c["pass_mark"],
                                                     100 * c["share_below_mark"], c["pass_mark"] - 1)),
        ("p", "Carrying last year's first-time pass rate onto this year's first-time candidates would set a higher "
              "mark: this year's candidates are a stronger cohort, with more experienced gas engineers coming through "
              "the standard route since the autumn, and the summer sittings always draw a stronger mix than the "
              "winter ones."),
        ("h", "The figures the Board asked for"),
        ("table", [["Month of 2026", "Sitting for the first time", "Resitting"]] +
         [[MONTHS[i], "{:,}".format(a["2026-%02d" % (i + 1)]["first_time"]),
           "{:,}".format(a["2026-%02d" % (i + 1)]["resitting"])] for i in range(9)]),
        ("table", [["Year", "First sat Brindle's paper", "Passed at that sitting"]] +
         [[y, "{:,}".format(v["first_time"]), "{:,}".format(v["passed"])] for y, v in b.items()]),
    ]
    st = K._styles()
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    story = []
    for kind, val in blocks[:7]:
        story.append(Paragraph(val, st[kind]))
    story.append(Image(tmp_png, width=160 * mm, height=82.5 * mm))
    story.append(Paragraph("The share of the candidates who sat Harrowgate's paper reaching each raw mark, April to "
                           "September 2026, with the recommended pass mark.", st["s"]))
    for kind, val in blocks[7:]:
        if kind == "table":
            width = A4[0] - 40 * mm
            n = len(val[0])
            widths = [width * 0.55] + [width * 0.45 / (n - 1)] * (n - 1)
            rows = [[Paragraph(str(x).replace("&", "&amp;"), st["cell"]) for x in r] for r in val]
            t = Table(rows, colWidths=widths, hAlign="LEFT")
            t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#8a949c")),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            story += [t, Spacer(1, 6)]
        else:
            story.append(Paragraph(val, st[kind]))

    def page(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(20 * mm, 10 * mm, "%s  |  Board paper  |  4 November 2026" % P.ORG)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title="Theory paper pass mark 2027", author=P.ORG, creator=P.ORG,
                            producer=P.ORG, invariant=1)
    doc.build(story, onFirstPage=page, onLaterPages=page)
    import re
    data = open(path, "rb").read()
    data = re.sub(rb"/CreationDate \(D:[^)]*\)", b"/CreationDate (D:20261027101500+00'00')", data)
    data = re.sub(rb"/ModDate \(D:[^)]*\)", b"/ModDate (D:20261027163000+00'00')", data)
    for sig in (b"ReportLab Generated PDF document (opensource)", b"ReportLab generated PDF document -- digest (opensource)"):
        data = data.replace(sig, b" " * len(sig))
    open(path, "wb").write(data)
    os.remove(tmp_png)


def write_all(target, golden, fig):
    os.makedirs(golden, exist_ok=True)
    write_csv(os.path.join(golden, CSV), conformed_rows(target, fig["call"]["pass_mark"]))
    write_pdf(os.path.join(golden, PDF), fig, os.path.join(golden, "_chart.png"))
