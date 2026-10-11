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

NAVY = RGBColor(0x1F, 0x2A, 0x44)
GREY = RGBColor(0x55, 0x5B, 0x66)


def chart_png(s):
    ref = s["referrals"]
    order = sorted(PATCH_ORDER, key=lambda p: ref[p])
    names = [PATCH_NAMES[p] for p in order]
    vals = [ref[p] for p in order]
    colours = ["#1f5fa8" if p == s["pick"] else ("#8fb3dc" if p == s["runner_up"] else "#c9ced6") for p in order]
    fig, ax = plt.subplots(figsize=(8.6, 4.6), dpi=150)
    bars = ax.barh(names, vals, color=colours)
    for b, v, p in zip(bars, vals, order):
        lab = f"{v}"
        if p == s["pick"]:
            lab += "  team placed here"
        elif p == s["runner_up"]:
            lab += "  runner-up"
        ax.text(v + 0.8, b.get_y() + b.get_height() / 2, lab, va="center", fontsize=9)
    ax.set_xlabel("Supplies referred by the 7 December 2026 screening run")
    ax.set_xlim(0, max(vals) * 1.32)
    ax.spines[["top", "right"]].set_visible(False)
    gap = ref[s["pick"]] - ref[s["runner_up"]]
    ax.set_title(f"{PATCH_NAMES[s['pick']]} gets the field team for January to March,\n"
                 f"{ref[s['pick']]} referrals, {gap} ahead of {PATCH_NAMES[s['runner_up']]}",
                 fontsize=11, loc="left")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf


def write(s, outdir):
    os.makedirs(outdir, exist_ok=True)
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]
    ref, hist, cap = s["referrals"], s["history"], s["capacity"]
    pick, ru = s["pick"], s["runner_up"]

    sl = prs.slides.add_slide(blank)
    tb = sl.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(12), Inches(1.2)).text_frame
    tb.text = f"Field team, January to March 2027: {PATCH_NAMES[pick]}"
    tb.paragraphs[0].runs[0].font.size = Pt(26)
    tb.paragraphs[0].runs[0].font.bold = True
    tb.paragraphs[0].runs[0].font.color.rgb = NAVY
    p = tb.add_paragraph()
    p.text = (f"{ref[pick]} supplies referred by the 7 December screening run. "
              f"Runner-up {PATCH_NAMES[ru]} on {ref[ru]}, {s['margin']} behind.")
    p.runs[0].font.size = Pt(15)
    p.runs[0].font.color.rgb = GREY
    sl.shapes.add_picture(chart_png(s), Inches(0.9), Inches(1.75), width=Inches(11.3))
    nt = sl.shapes.add_textbox(Inches(0.6), Inches(7.0), Inches(12), Inches(0.4)).text_frame
    nt.text = "RP-07 v4 screen: each supply against its own 104 weeks, degree-day adjusted, 30% over the eight weeks to 6 Dec."
    nt.paragraphs[0].runs[0].font.size = Pt(10)
    nt.paragraphs[0].runs[0].font.color.rgb = GREY

    sl2 = prs.slides.add_slide(blank)
    tb2 = sl2.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(12), Inches(0.9)).text_frame
    tb2.text = "Every patch: this screen, the last three winters, and what the team could do in Q1"
    tb2.paragraphs[0].runs[0].font.size = Pt(20)
    tb2.paragraphs[0].runs[0].font.bold = True
    tb2.paragraphs[0].runs[0].font.color.rgb = NAVY
    hdr = ["Patch", "Referrals (Dec run)", "Winter visits with access", "Diversions confirmed",
           "Confirmation rate", "Q1 2027 visit capacity"]
    order = sorted(PATCH_ORDER, key=lambda q: -ref[q])
    rows, cols = len(order) + 1, len(hdr)
    tbl = sl2.shapes.add_table(rows, cols, Inches(0.6), Inches(1.4), Inches(12.1), Inches(4.6)).table
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
    ft = sl2.shapes.add_textbox(Inches(0.6), Inches(6.25), Inches(12), Inches(1.0)).text_frame
    ft.text = ("Winters are October to March, 2023/24 to 2025/26. Confirmation rate is confirmed diversions over "
               "visits with access, with findings overturned on appeal counted as no fault. Capacity is "
               f"{s['officer_days']} officer field days in Q1 at each patch's planned visits per day under FW-3.")
    ft.word_wrap = True
    ft.paragraphs[0].runs[0].font.size = Pt(10.5)
    ft.paragraphs[0].runs[0].font.color.rgb = GREY
    prs.core_properties.author = "RP analytics"
    prs.core_properties.title = "Field team placement Q1 2027"
    prs.save(os.path.join(outdir, "field_team_q1_2027.pptx"))

    with open(os.path.join(outdir, "patch_screen_q1_2027.csv"), "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["rp_patch", "patch_name", "referrals_run_2026_12_07", "winter_visits_with_access_2023_26",
                     "diversions_confirmed_2023_26", "confirmation_rate_pct", "q1_2027_visit_capacity"])
        for q in order:
            acc, conf, rate = hist[q]
            wr.writerow([q, PATCH_NAMES[q], ref[q], acc, conf, f"{rate:.1f}", cap[q]])
