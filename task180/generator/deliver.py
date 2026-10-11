"""Write the golden deliverables: field_team_q1_2027.pptx and patch_screen_q1_2027.csv."""
import csv
import io
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from pptx import Presentation  # noqa: E402
from pptx.util import Inches, Pt  # noqa: E402
from pptx.dml.color import RGBColor  # noqa: E402

from golden import PATCH_ORDER, PATCH_NAMES  # noqa: E402

NAVY = RGBColor(0x1B, 0x2B, 0x48)
INK2 = RGBColor(0x4A, 0x52, 0x60)
MUTED = RGBColor(0x7A, 0x82, 0x90)
PICK, RUNNER, OTHER = "#1d4f91", "#7fa3d1", "#c4cad3"
SOURCE = ("Source: RP-07 v4 screening run of Monday 7 December 2026 on the smart daily register reads and the CIS "
          "supply point register; Met Office degree days. Prepared by RP analytics for the planning meeting.")


def chart_png(s):
    ref = s["referrals"]
    order = sorted(PATCH_ORDER, key=lambda p: ref[p])
    names = [PATCH_NAMES[p] for p in order]
    vals = [ref[p] for p in order]
    colours = [PICK if p == s["pick"] else (RUNNER if p == s["runner_up"] else OTHER) for p in order]
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, ax = plt.subplots(figsize=(9.2, 4.4), dpi=160)
    bars = ax.barh(names, vals, color=colours, height=0.62)
    for b, v, p in zip(bars, vals, order):
        lab = f"{v}"
        if p == s["pick"]:
            lab += "   team placed here"
        elif p == s["runner_up"]:
            lab += "   runner-up"
        ax.text(v + 0.7, b.get_y() + b.get_height() / 2, lab, va="center", fontsize=9.5, color="#2b2f36")
    ax.set_xlabel("Supplies referred by the 7 December 2026 screening run", fontsize=9.5, color="#4a5260")
    ax.set_xlim(0, max(vals) * 1.38)
    ax.tick_params(axis="both", labelsize=9.5, colors="#4a5260")
    ax.xaxis.get_major_locator().set_params(integer=True)
    ax.grid(axis="x", color="#e3e6ea", linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#b8bec7")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf


def _text(slide, x, y, w, h, text, size, color, bold=False):
    tf = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
    tf.word_wrap = True
    tf.text = text
    r = tf.paragraphs[0].runs[0]
    r.font.size, r.font.bold, r.font.color.rgb = Pt(size), bold, color
    return tf


def write(s, outdir):
    os.makedirs(outdir, exist_ok=True)
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]
    ref, hist, cap = s["referrals"], s["history"], s["capacity"]
    pick, ru = s["pick"], s["runner_up"]

    sl = prs.slides.add_slide(blank)
    _text(sl, 0.6, 0.35, 12.2, 0.9,
          f"{PATCH_NAMES[pick]} gets the field team from January to March: {ref[pick]} referrals, "
          f"{s['margin']} more than {PATCH_NAMES[ru]}", 24, NAVY, bold=True)
    _text(sl, 0.6, 1.2, 12.2, 0.5,
          f"Runner-up {PATCH_NAMES[ru]} on {ref[ru]}. Referred supplies by patch, credit-paying premises only, "
          "after the RP-07 exclusions for changes of occupier and heating changes.", 13, INK2)
    sl.shapes.add_picture(chart_png(s), Inches(0.9), Inches(1.85), width=Inches(11.0))
    _text(sl, 0.6, 6.85, 11.6, 0.45, SOURCE, 9, MUTED)
    _text(sl, 12.4, 6.95, 0.6, 0.3, "1", 9, MUTED)

    sl2 = prs.slides.add_slide(blank)
    _text(sl2, 0.6, 0.35, 12.2, 0.9,
          "Lochaber has the best confirmation record of the last three winters and the fewest referrals now",
          22, NAVY, bold=True)
    hdr = ["Patch", "Referrals, 7 Dec run", "Winter visits with access", "Diversions confirmed",
           "Confirmation rate", "Q1 2027 visit capacity"]
    order = sorted(PATCH_ORDER, key=lambda q: -ref[q])
    rows, cols = len(order) + 1, len(hdr)
    tbl = sl2.shapes.add_table(rows, cols, Inches(0.6), Inches(1.35), Inches(12.1), Inches(4.4)).table
    for j, h in enumerate(hdr):
        tbl.cell(0, j).text = h
    for i, q in enumerate(order, start=1):
        acc, conf, rate = hist[q]
        vals = [PATCH_NAMES[q], str(ref[q]), str(acc), str(conf), f"{rate:.1f}%", f"{cap[q]:,}"]
        for j, v in enumerate(vals):
            tbl.cell(i, j).text = v
    for i in range(rows):
        for j in range(cols):
            for para in tbl.cell(i, j).text_frame.paragraphs:
                for r in para.runs:
                    r.font.size = Pt(12)
    _text(sl2, 0.6, 5.95, 12.1, 0.8,
          "Winters run October to March, 2023/24 to 2025/26. Confirmation rate is confirmed diversions over visits "
          "with access (RP-07 section 8); findings overturned on appeal count as no fault found. FieldLink jobs "
          "re-created in FieldOps in November 2024 are counted once. Capacity is "
          f"{s['officer_days']} officer field days between 1 January and 31 March 2027 (Scottish public holidays, booked "
          "absences, the third officer from 15 February) at each patch's FW-3 visits per day.", 10.5, INK2)
    _text(sl2, 0.6, 6.95, 11.6, 0.4, "Source: FieldLink and FieldOps job extracts, tamper appeals register, "
          "Q1 2027 field rota, FW-3 issue 6.", 9, MUTED)
    _text(sl2, 12.4, 6.95, 0.6, 0.3, "2", 9, MUTED)
    prs.core_properties.author = "RP analytics"
    prs.core_properties.title = "Field team placement, January to March 2027"
    prs.save(os.path.join(outdir, "field_team_q1_2027.pptx"))

    with open(os.path.join(outdir, "patch_screen_q1_2027.csv"), "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["rp_patch", "patch_name", "referrals_run_2026_12_07", "winter_visits_with_access_2023_26",
                     "diversions_confirmed_2023_26", "confirmation_rate_pct", "q1_2027_visit_capacity"])
        for q in order:
            acc, conf, rate = hist[q]
            wr.writerow([q, PATCH_NAMES[q], ref[q], acc, conf, f"{rate:.1f}", cap[q]])
