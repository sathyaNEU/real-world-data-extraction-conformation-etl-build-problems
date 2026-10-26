"""The golden deliverables for task270, computed from the shipped pack: proxy_metric_scores_2027.xlsx (every
candidate's correlation under the standard, the first-quarter calendar's detectable effects and the 2025 holdout read)
and proxy_metric_review_2027.pptx (the review deck, with the chart), and generator/figures.json, which carries every
figure the write-up states."""
import io
import json
import os

import numpy as np

import analysis as A
import asks as S
import common as K

ACCENT = "0F6B4F"
NEUTRAL = "9AA5B1"
INK = "1F2328"
PP = S.PP


def two(x):
    return K.r(x, 2)


def fmt_unit(m, v):
    return ("%.2f" % v) if m in PP else ("%.3f" % v)


def unit_name(m):
    return {"active_days_d1_14": "days", "sessions_d1_14": "sessions", "first_purchase_d14": "percentage points",
            "items_saved_d1_14": "items", "push_opens_d1_14": "opens", "retained_m6": "percentage points"}[m]


def compute(target):
    r = A.main_call(target)
    d = r["data"]
    g = S.golden(d)
    corr = {m: two(v) for m, v in zip(K.CAND, r["golden"])}
    rho = {m: K.r(v, 2) for m, v in zip(K.CAND, r["hm"]["rho"])}
    order = sorted(K.CAND, key=lambda m: -r["golden"][K.CAND.index(m)])
    fig = {
        "call": {"proxy": r["proxy"], "proxy_name": K.LABEL[r["proxy"]], "runner_up": r["runner_up"],
                 "runner_up_name": K.LABEL[r["runner_up"]],
                 "sentence": "Kleerwissel should adopt first purchase within 14 days (first_purchase_d14) as its 2027 "
                             "proxy for six-month retention.",
                 "changes": r["n_changes"], "experiments": r["n_experiments"],
                 "proxy_correlation": corr[r["proxy"]], "runner_up_correlation": corr[r["runner_up"]],
                 "order": order},
        "correlations": corr,
        "components": {"holdout_users": int(r["hm"]["n"]), "user_level_correlation": rho},
        "asks": {"B": {"users_per_arm": g["B_users"], "detectable": g["B"]},
                 "C": g["C"]},
        "parameters": {"power_per_cent": 80, "alpha_per_cent": 5, "holdout_2027_per_cent": 3,
                       "holdout_2027_weekly_q1": 430,
                       "z_sum": "%.2f" % K.Z_POWER, "z_alpha": "1.96", "z_power": "0.84"},
    }
    return fig, r, g


# --------------------------------------------------------------------------------------------------- workbook
def write_book(path, fig, r, d):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = Workbook()
    head = Font(bold=True, color="FFFFFF")
    fill = PatternFill("solid", fgColor=ACCENT)
    bold = Font(bold=True)
    thin = Border(bottom=Side(style="thin", color="C3C9D0"))
    wrap = Alignment(wrap_text=True, vertical="top")

    sh = wb.active
    sh.title = "Proxy 2027"
    sh["A1"] = "Proxy for six-month retention, 2027: first purchase within 14 days"
    sh["A1"].font = Font(bold=True, size=13)
    sh["A2"] = ("Correlation, across %d past onboarding changes (%d experiments), between each change's effect on the "
                "candidate and its effect on retained_m6 (standard 2.2 to 2.4)." % (fig["call"]["changes"],
                                                                                  fig["call"]["experiments"]))
    sh.append([])
    sh.append(["Rank", "Candidate", "Metric key", "Correlation under the standard"])
    for c in sh[4]:
        c.font, c.fill = head, fill
    for i, m in enumerate(fig["call"]["order"], start=1):
        sh.append([i, K.LABEL[m][0].upper() + K.LABEL[m][1:], m, fig["correlations"][m]])
        sh.cell(sh.max_row, 4).number_format = "0.00"
        if i == 1:
            for c in sh[sh.max_row]:
                c.font = bold
    sh.append([])
    sh.append(["Changes read", fig["call"]["changes"]])
    sh.append(["Experiments", fig["call"]["experiments"]])
    for w, c in zip((7, 40, 22, 30), "ABCD"):
        sh.column_dimensions[c].width = w
    sh.freeze_panes = "A5"

    sb = wb.create_sheet("Detectable effects Q1")
    sb["A1"] = "Smallest effect each first-quarter 2027 onboarding experiment can detect (80% power, 5% two-sided)"
    sb["A1"].font = Font(bold=True, size=12)
    sb.append([])
    cols = ["Experiment", "Title", "Layer", "Platforms", "Arms", "Users per arm"] + \
           ["%s (%s)" % (K.SHORT[m], unit_name(m)) for m in K.CAND]
    sb.append(cols)
    for c in sb[3]:
        c.font, c.fill, c.alignment = head, fill, wrap
    cal = d["calendar"]
    for _, row in cal.iterrows():
        e = row["experiment_id"]
        vals = [fig["asks"]["B"]["detectable"][e][m] for m in K.CAND]
        sb.append([e, row["title"], row["layer"], row["platforms"], int(row["arms"]),
                   fig["asks"]["B"]["users_per_arm"][e]] + vals)
        rr = sb.max_row
        sb.cell(rr, 6).number_format = "#,##0"
        for j, m in enumerate(K.CAND):
            sb.cell(rr, 7 + j).number_format = "0.00" if m in PP else "0.000"
    for w, c in zip((11, 36, 13, 10, 6, 13, 15, 15, 17, 15, 15), "ABCDEFGHIJK"):
        sb.column_dimensions[c].width = w
    sb.row_dimensions[3].height = 32
    sb.freeze_panes = "C4"

    sc = wb.create_sheet("Holdout 2025")
    sc["A1"] = "2025 new consumer users outside the global holdout, less the holdout's users"
    sc["A1"].font = Font(bold=True, size=12)
    sc.append([])
    sc.append(["Metric", "Unit", "January to June", "July to December"])
    for c in sc[3]:
        c.font, c.fill = head, fill
    for m in K.CAND + [K.RET]:
        sc.append([K.SHORT[m], unit_name(m), fig["asks"]["C"]["H1"][m], fig["asks"]["C"]["H2"][m]])
        for j in (3, 4):
            sc.cell(sc.max_row, j).number_format = "0.00" if m in PP else "0.000"
    for w, c in zip((22, 20, 18, 18), "ABCD"):
        sc.column_dimensions[c].width = w

    sn = wb.create_sheet("Notes")
    notes = [
        "Sources: experiment_scorecards_2024_2026.csv (export of 23 October 2026), onboarding_experiments_2024_2026.csv, "
        "global_holdout_users_2025.csv, onboarding_calendar_2027q1.csv, new_user_forecast_2027.csv, "
        "signup_cohorts_2025.csv.",
        "Changes read: experiments started from 1 January 2024 whose six-month read closed by 23 October 2026, sample-"
        "ratio check passed; each treatment arm against its control is one change and counts once (standard 2.4).",
        "Scorecards: the latest computation of each arm and metric; keys before 3 March 2025 read through the "
        "catalogue's former keys.",
        "Correlations: each change's sampling variance, and the sampling covariance between its two effects (both "
        "measured on the same users), taken out of the moments across changes; the covariance uses each candidate's "
        "user-level correlation with retained_m6 among the 2025 holdout's users.",
        "Detectable effects: each ISO week's forecast taken once (the tool writes it on each day of the week); 3 per "
        "cent of new users to the 2027 holdout; each "
        "layer's users on a platform split evenly among its experiments live that week on that platform; arms split "
        "evenly; standard deviations of the 2025 holdout's users.",
        "Holdout 2025: the cohort table's accounts that signed up as consumers (those since upgraded to business "
        "accounts included), at their latest refresh, the holdout's own users taken out of the totals; halves by "
        "sign-up date.",
        "First purchase and retention in percentage points; other metrics in their own units.",
    ]
    for t in notes:
        sn.append([t])
        sn.cell(sn.max_row, 1).alignment = wrap
    sn.column_dimensions["A"].width = 120
    for sheet in (sh, sb, sc):
        for row in sheet.iter_rows(min_row=4 if sheet is sh else 4):
            for c in row:
                c.border = thin
    wb.save(path)


# ------------------------------------------------------------------------------------------------------- chart
def chart_png(fig):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["svg.hashsalt"] = "task270"
    order = fig["call"]["order"]
    vals = [fig["correlations"][m] for m in order]
    labels = [K.SHORT[m] for m in order]
    fg, ax = plt.subplots(figsize=(9.2, 4.3), dpi=150)
    colors = ["#" + ACCENT if m == fig["call"]["proxy"] else "#" + NEUTRAL for m in order]
    y = np.arange(len(order))[::-1]
    ax.barh(y, vals, color=colors, height=0.56, edgecolor="white", linewidth=2)
    for yi, v in zip(y, vals):
        ax.text(v + (0.012 if v >= 0 else -0.012), yi, "%.2f" % v, va="center", ha="left" if v >= 0 else "right",
                fontsize=11, color="#" + INK)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=11, color="#" + INK)
    ax.axvline(0, color="#56616c", linewidth=0.8)
    ax.set_xlim(-0.2, 0.7)
    ax.set_xlabel("Correlation of the changes' effects with their effects on six-month retention", fontsize=10,
                  color="#56616c")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#c3c9d0")
    ax.tick_params(axis="x", colors="#56616c", labelsize=9)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#e6e9ec", linewidth=0.8)
    ax.set_axisbelow(True)
    fg.tight_layout()
    buf = io.BytesIO()
    fg.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fg)
    return buf.getvalue()


# -------------------------------------------------------------------------------------------------------- deck
def write_deck(path, fig, d):
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.util import Emu, Pt

    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    blank = prs.slide_layouts[6]
    W = prs.slide_width

    def text(slide, x, y, w, h, s, size=14, bold=False, color=INK):
        tb = slide.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = s
        p.font.size, p.font.bold = Pt(size), bold
        p.font.name = "Calibri"
        p.font.color.rgb = RGBColor.from_string(color)
        return tf

    def footer(slide, n, src):
        text(slide, 457200, 6400800, 9800000, 300000, src, 9, False, "5B6470")
        text(slide, 11300000, 6400800, 500000, 300000, str(n), 9, False, "5B6470")

    def table(slide, rows, x, y, widths, size=11, num_cols=()):
        shp = slide.shapes.add_table(len(rows), len(rows[0]), Emu(x), Emu(y), Emu(sum(widths)),
                                     Emu(360000 * len(rows)))
        t = shp.table
        for j, w in enumerate(widths):
            t.columns[j].width = Emu(w)
        for i, row in enumerate(rows):
            for j, v in enumerate(row):
                cell = t.cell(i, j)
                cell.text = str(v)
                p = cell.text_frame.paragraphs[0]
                p.font.size = Pt(size)
                p.font.name = "Calibri"
                p.font.bold = i == 0
                from pptx.enum.text import PP_ALIGN
                if j in num_cols:
                    p.alignment = PP_ALIGN.RIGHT
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor.from_string(ACCENT if i == 0 else ("F3F5F7" if i % 2 else "FFFFFF"))
                p.font.color.rgb = RGBColor.from_string("FFFFFF" if i == 0 else INK)
        return t

    c = fig["call"]
    # 1. the call
    s = prs.slides.add_slide(blank)
    text(s, 457200, 1600000, 11000000, 1300000, "First purchase within 14 days becomes the 2027 onboarding proxy",
         34, True, ACCENT)
    text(s, 457200, 3000000, 11000000, 1400000,
         "Across %d onboarding changes since January 2024, first purchase within 14 days is the candidate whose "
         "effects track the same changes' effects on six-month retention most closely (%.2f), well ahead of sessions "
         "in days 1 to 14 (%.2f). Every 2027 onboarding experiment is read on it at two weeks."
         % (c["changes"], c["proxy_correlation"], c["runner_up_correlation"]), 18, False, INK)
    text(s, 457200, 5600000, 11000000, 400000, "Proxy metric review 2027 · Growth · %s, Head of Experimentation · "
         "30 October 2026" % K.HEAD_EXP, 12, False, "5B6470")
    # 2. the chart
    s = prs.slides.add_slide(blank)
    text(s, 457200, 300000, 11200000, 900000, "Changes that move first purchase move retention; changes that move "
         "sessions mostly do not", 24, True, INK)
    png = chart_png(fig)
    s.shapes.add_picture(io.BytesIO(png), Emu(457200), Emu(1250000), width=Emu(10400000))
    footer(s, 2, "%d changes in %d onboarding experiments, January 2024 to April 2026; each change's sampling error, "
                 "and the covariance its two effects share, taken out." % (c["changes"], c["experiments"]))
    # 3. how they were judged
    s = prs.slides.add_slide(blank)
    text(s, 457200, 300000, 11200000, 900000, "Measured on the same users, a change's two effects share their noise",
         24, True, INK)
    tf = text(s, 457200, 1300000, 6000000, 4600000,
              "Each experiment measures a candidate and six-month retention on the same users, so their two "
              "estimates err together wherever the candidate and retention go together user by user.", 15, False, INK)
    for line in ("Active days and sessions follow retention user by user in the 2025 holdout (%.2f and %.2f), so "
                 "their measured effects co-move with retention's partly by noise." %
                 (fig["components"]["user_level_correlation"]["active_days_d1_14"],
                  fig["components"]["user_level_correlation"]["sessions_d1_14"]),
                 "First purchase barely does (%.2f): what its effects share with retention's is the change itself." %
                 fig["components"]["user_level_correlation"]["first_purchase_d14"],
                 "The correlation the standard asks for is taken after each change's sampling error and that shared "
                 "covariance come out."):
        p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(15)
        p.font.name = "Calibri"
        p.font.color.rgb = RGBColor.from_string(INK)
        p.space_before = Pt(10)
    rows = [["Candidate", "Correlation"]] + [[K.SHORT[m], "%.2f" % fig["correlations"][m]] for m in c["order"]]
    table(s, rows, 7000000, 1400000, [2800000, 1500000], 13, num_cols=(1,))
    footer(s, 3, "Standard 2.2 to 2.4; scorecard export of 23 October 2026; global_holdout_users_2025.csv (%s users)."
           % "{:,}".format(fig["components"]["holdout_users"]))
    # 4. detectable effects
    s = prs.slides.add_slide(blank)
    text(s, 457200, 300000, 11200000, 900000, "The single-platform tests can detect only about twice the effect of the "
         "full tests", 24, True, INK)
    text(s, 457200, 1000000, 11200000, 400000, "Smallest effect a treatment arm can detect against its control: "
         "days, sessions, items and opens in their own units, first purchase in percentage points.", 13, False, "5B6470")
    cal = d["calendar"]
    rows = [["Experiment", "Users per arm"] + [K.SHORT[m] for m in K.CAND]]
    for _, row in cal.iterrows():
        e = row["experiment_id"]
        rows.append([e, "{:,}".format(fig["asks"]["B"]["users_per_arm"][e])] +
                    [fmt_unit(m, fig["asks"]["B"]["detectable"][e][m]) for m in K.CAND])
    table(s, rows, 457200, 1500000, [1450000, 1350000, 1700000, 1700000, 1900000, 1700000, 1700000], 12,
          num_cols=(1, 2, 3, 4, 5, 6))
    footer(s, 4, "80 per cent power, two-sided test at 5 per cent; onboarding_calendar_2027q1.csv and "
                 "new_user_forecast_2027.csv; 3 per cent 2027 holdout; standard deviations of the 2025 holdout's users.")
    # 5. the 2025 holdout read
    s = prs.slides.add_slide(blank)
    text(s, 457200, 300000, 11200000, 900000, "In 2025 the shipped onboarding lifted first purchase and retention "
         "against the holdout", 24, True, INK)
    rows = [["Metric", "Unit", "January to June", "July to December"]]
    for m in K.CAND + [K.RET]:
        rows.append([K.SHORT[m], unit_name(m), fmt_unit(m, fig["asks"]["C"]["H1"][m]),
                     fmt_unit(m, fig["asks"]["C"]["H2"][m])])
    table(s, rows, 457200, 1300000, [3000000, 2400000, 2100000, 2100000], 13, num_cols=(2, 3))
    footer(s, 5, "2025 new consumer users outside the global holdout less the holdout's users, by sign-up date; "
                 "signup_cohorts_2025.csv at its latest refresh.")
    prs.save(path)
    _bullets(path)


def _bullets(path):
    """the default master's second-level bullet glyph is an en dash; the house template uses a round bullet"""
    import zipfile
    with zipfile.ZipFile(path) as z:
        items = [(i, z.read(i.filename)) for i in z.infolist()]
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for i, data in items:
            if i.filename.endswith(".xml"):
                data = data.replace("\u2013".encode("utf-8"), "\u2022".encode("utf-8"))
            z.writestr(i, data)


def write(target, golden):
    os.makedirs(golden, exist_ok=True)
    fig, r, g = compute(target)
    write_book(os.path.join(golden, K.BOOK), fig, r, r["data"])
    write_deck(os.path.join(golden, K.DECK), fig, r["data"])
    return fig, r


def write_figures(path, fig):
    with open(path, "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
        f.write("\n")
