"""The golden deliverables: the hotspot brief (PDF with its chart) and the response figures (CSV)."""
import io
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

from common import GOLDEN, TRIGGER, write_csv, set_mtime, scrub_pdf  # noqa: E402
from docs import ST, _fix_pdf_dates  # noqa: E402

BRIEF = "dengue_hotspots_mw41_44_2027.pdf"
CSV = "response_figures_2027.csv"
DORMS = ["Tabing-Ilog", "Pulong Bayabas", "Malinta", "Kanluran", "Burol", "Silangan"]


INK = "#1d2733"


def chart_png(names, place, hot):
    order = sorted(range(len(names)), key=lambda i: (-place[i], names[i]))
    fig, ax = plt.subplots(figsize=(7.2, 8.4), dpi=150)
    ys = list(range(len(order)))[::-1]
    vals = [place[i] for i in order]
    cols = ["#c0392b" if names[i] in hot else "#8a949c" for i in order]
    ax.barh(ys, vals, color=cols, height=0.7)
    ax.set_yticks(ys)
    ax.set_yticklabels([names[i] for i in order], fontsize=7.5, color=INK)
    ax.axvline(TRIGGER, color=INK, linewidth=1.0, linestyle=(0, (4, 3)))
    ax.text(TRIGGER + 5, ys[-1] - 0.3, "trigger, %d cases" % TRIGGER, fontsize=7.5, color=INK, va="center")
    for y, v, i in zip(ys, vals, order):
        if names[i] in hot:
            ax.text(v + 4, y, "%d" % round(v), fontsize=7.5, va="center", color=INK)
    ax.set_xlabel("Cases with onset in weeks 37 to 40, by barangay where infected (estimated)", fontsize=8, color=INK)
    ax.set_title("San Roque carries the window's infections; the barangays its workers live in fall under the trigger",
                 fontsize=8.8, loc="left", color=INK)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color="#c0392b", label="Hotspot response, weeks 41 to 44"),
                       Patch(color="#8a949c", label="No hotspot response")],
              loc="lower right", fontsize=7.5, frameon=False)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color("#b7bec4")
    ax.spines["bottom"].set_color("#b7bec4")
    ax.tick_params(axis="x", labelsize=7.5, colors=INK)
    ax.tick_params(axis="y", length=0)
    ax.xaxis.grid(True, color="#e3e7ea", linewidth=0.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#55606b"))
    canvas.drawString(18 * mm, 9 * mm, "CESU, City Health Office, Dalisay City   Hotspot response, weeks 41 to 44 of 2027")
    canvas.drawRightString(A4[0] - 18 * mm, 9 * mm, "Page %d of 2" % doc.page)
    canvas.restoreState()


def brief(fig, names, residence, place):
    hot = set(fig["call"]["hotspots"])
    path = os.path.join(GOLDEN, BRIEF)
    os.makedirs(GOLDEN, exist_ok=True)
    s = []
    s.append(Paragraph("MEMORANDUM", ST["h1"]))
    head = Table([["To", "John Figueroa, MD, City Health Officer"],
                  ["From", "Tammy Orozco, RN, City Epidemiology and Surveillance Unit"],
                  ["Date", "11 October 2027"],
                  ["Subject", "Hotspot response for morbidity weeks 41 to 44 (10 October to 6 November 2027)"]],
                 colWidths=[20 * mm, 150 * mm])
    head.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.8), ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8.8),
                              ("LINEBELOW", (0, -1), (-1, -1), 0.6, colors.black),
                              ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]))
    s.append(head)
    s.append(Spacer(1, 7))
    s.append(Paragraph(
        "<b>Send the hotspot response to San Roque, Bagumbayan and Maligaya, and to no other barangay.</b>", ST["p"]))
    s.append(Paragraph(
        "Counted by home address, %d barangays are over the plan's trigger of %d cases with onset in weeks 37 to "
        "40: Bagumbayan, Maligaya and the six barangays beside the Dalisay Industrial Estate (%s). Section 4.3 of "
        "the plan counts the cases infected in a barangay, and in those six the rise is in their working-age "
        "residents only, while their children and older residents are at their usual levels; they are the six "
        "barangays the CBMS 2025 place-of-work table shows sending the most workers to San Roque. Aedes aegypti bites by day, "
        "so those residents were infected where they work, at the estate." % (
            fig["over_trigger_by_home_address"], TRIGGER, ", ".join(DORMS)), ST["p"]))
    s.append(Paragraph(
        "Placing each barangay's working-age excess at the barangays its workers work in, by the pattern across "
        "barangays, puts about %d of the window's cases in San Roque, whose own residents account for %d. "
        "Bagumbayan and Maligaya have outbreaks at home, across every age, and stay over the trigger. Taking "
        "anything from half of a working resident's day to all of it as spent at work, the same three barangays "
        "reach the trigger and no other does." % (round(place[names.index("San Roque")]),
                                                   residence[names.index("San Roque")]), ST["p"]))
    s.append(Paragraph(
        "At San Roque the response should cover the estate's grounds as well as the village, with the estate's management and the locators' clinics told of the cluster among their "
        "workers. The six barangays beside the estate keep their routine search-and-destroy rounds.", ST["p"]))
    s.append(Spacer(1, 3))
    data = [["Barangay", "Cases by home address", "Cases infected there (est.)", "Response"]]
    order = sorted(range(len(names)), key=lambda i: (names[i] not in hot, -place[i], names[i]))
    for i in order:
        data.append([names[i], str(residence[i]), str(int(round(place[i]))), "In" if names[i] in hot else "Out"])
    t = Table(data, colWidths=[42 * mm, 34 * mm, 44 * mm, 22 * mm], repeatRows=1)
    style = [("FONT", (0, 0), (-1, -1), "Helvetica", 7.5), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 7.5),
             ("ALIGN", (1, 0), (-1, -1), "RIGHT"), ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
             ("LINEBELOW", (0, 3), (-1, 3), 0.4, colors.grey),
             ("TOPPADDING", (0, 0), (-1, -1), 1.0), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.0)]
    for k, i in enumerate(order, start=1):
        if names[i] in hot:
            style.append(("FONT", (0, k), (-1, k), "Helvetica-Bold", 7.5))
    t.setStyle(TableStyle(style))
    s.append(t)
    s.append(Spacer(1, 3))
    s.append(Paragraph(
        "Source: CESU dengue line list as notified by 08:00 on 11 October 2027 (notifications classified Not a "
        "case and residents of other towns left out, a patient notified by two units counted once, per plan "
        "section 4.1); CBMS 2025, Tables 1, 3 and 4.", ST["small"]))
    s.append(Paragraph(
        "Cases infected there are estimates: no record shows where a case was infected, so each barangay's "
        "working-age cases above its 2022 to 2026 age mix are placed where its employed residents work.",
        ST["small"]))
    s.append(PageBreak())
    s.append(Image(chart_png(names, place, hot), width=170 * mm, height=198 * mm))
    s.append(Paragraph(
        "Source: as page 1. Bars are the estimated cases infected in each barangay; the dashed line is the plan's "
        "trigger of %d cases." % TRIGGER, ST["small"]))
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=14 * mm,
                            bottomMargin=16 * mm, title="Hotspot response, weeks 41 to 44 of 2027",
                            author="CESU Dalisay City", creator="CESU Dalisay City", producer="CESU Dalisay City",
                            subject="", invariant=1)
    doc.build(s, onFirstPage=_footer, onLaterPages=_footer)
    _fix_pdf_dates(path)
    scrub_pdf(path)
    set_mtime(path)


def figures_csv(fig):
    rows = []
    for w, v in sorted(fig["dmc_admissions"].items(), key=lambda kv: int(kv[0])):
        rows.append(["dengue_admissions", "Dalisay Medical Center", w, v])
    for w, v in sorted(fig["ddh_admissions"].items(), key=lambda kv: int(kv[0])):
        rows.append(["dengue_admissions", "Dalisay Doctors' Hospital", w, v])
    for b, v in sorted(fig["house_index"].items()):
        rows.append(["house_index_september_2027", b, "", "%.1f" % v])
    for w, v in sorted(fig["first_positive_ns1"].items(), key=lambda kv: int(kv[0])):
        rows.append(["patients_first_positive_ns1", "City Health Office Laboratory", w, v])
    for w, v in sorted(fig["first_positive_igm"].items(), key=lambda kv: int(kv[0])):
        rows.append(["patients_first_positive_igm", "City Health Office Laboratory", w, v])
    write_csv(os.path.join(GOLDEN, CSV), ["figure", "item", "morbidity_week", "value"], rows, newline="\n")


def make(fig, L):
    names = L["names"]
    residence = [int(L["res"][i].sum()) for i in range(len(names))]
    place = [fig["placement_by_inversion"][n] for n in names]
    brief(fig, names, residence, place)
    figures_csv(fig)
