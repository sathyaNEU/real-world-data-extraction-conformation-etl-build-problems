"""The golden deliverables and figures.json, every figure computed from target/ by analysis.py."""
import io
import json
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402
from pptx import Presentation  # noqa: E402
from pptx.dml.color import RGBColor  # noqa: E402
from pptx.util import Emu, Pt  # noqa: E402

import analysis as A  # noqa: E402
import io_util as IO  # noqa: E402

BOOK = "kaitanga_summer_test_2026-27.xlsx"
DECK = "borefield_plan_2026-27.pptx"
MLAB = {12: "Dec 2026", 1: "Jan 2027", 2: "Feb 2027", 3: "Mar 2027"}
QLAB = {1: "Jul-Sep 2025", 2: "Oct-Dec 2025", 3: "Jan-Mar 2026", 4: "Apr-Jun 2026"}


def half(v):
    return math.floor(v * 2 + 0.5) / 2.0


def compute(target):
    P = A.Pack(target)
    lev, coef, a9 = A.golden(P)
    fails = A.verdict(P, lev)
    energy = A.ask_energy(P)
    meters = A.ask_meters(P)
    q9 = P.plan[2]["PB9"]
    fig = {
        "call": {"holds": not fails, "failing": ["%s %s" % (i, A.MONTH_NAME[m]) for i, m in fails]},
        "lowest_level_m_bmp": {"%s %s" % (i, A.MONTH_NAME[m]): half(lev[(i, m)]) for i in A.EXISTING
                               for m in A.MONTHS},
        "min_operating_level_m_bmp": {i: float(P.mol[i]) for i in A.ALL},
        "pb9_drawdown_on_neighbour_m": {"PB3": half(a9["PB3"] * q9), "PB4": half(a9["PB4"] * q9)},
        "pb9_take_ml_d": q9,
        "constants": {"pb2_ct_multiplier": 40},
        "pb9_holds": all(lev[("PB9", m)] <= P.mol["PB9"] for m in A.MONTHS),
        "energy_kwh_per_ml": {"%s Q%d" % (i, q): int(round(v)) for (i, q), v in energy.items()},
        "permit_meter_ml": {"%s Q%d" % (i, q): int(round(v)) for (i, q), v in meters.items()},
        "raw": {"level": {"%s %d" % k: round(v, 4) for k, v in lev.items()},
                "a9": {k: round(v, 4) for k, v in a9.items()},
                "energy": {"%s Q%d" % k: round(v, 3) for k, v in energy.items()},
                "meters": {"%s Q%d" % k: round(v, 4) for k, v in meters.items()}},
    }
    return P, lev, fails, energy, meters, fig


# ---------------------------------------------------------------- workbook
HEAD = PatternFill("solid", fgColor="E3EAEF")
FAIL = PatternFill("solid", fgColor="F4D6D2")
THIN = Side(style="thin", color="B8C2C9")


def _head(ws, row, values):
    for k, v in enumerate(values, 1):
        c = ws.cell(row, k, v)
        c.font = Font(bold=True)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center" if k > 1 else "left")
        c.border = Border(bottom=THIN)


def workbook(P, lev, fails, energy, meters, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Drought test"
    ws["A1"] = "Kaitanga bore field: 2026-27 summer plan under the design drought (SWS-03 rev 4, section 4)"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Result: the plan fails. PB3 falls below its minimum operating level in February and March once "
                "PB9 takes 4.40 ML/d beside it. All other bores, PB9 included, hold.")
    ws["A2"].font = Font(bold=True, color="9C2B1F")
    ws["A3"] = ("Lowest pumping water level in each month, m below measuring point, to the nearest 0.5 m, at the "
                "plan's takes with MB1 at its December 2019 to March 2020 levels.")
    _head(ws, 5, ["Bore", "Dec 2026", "Jan 2027", "Feb 2027", "Mar 2027", "Minimum operating level", "Result"])
    r = 6
    for i in A.EXISTING:
        ws.cell(r, 1, i)
        for k, m in enumerate(A.MONTHS):
            c = ws.cell(r, 2 + k, half(lev[(i, m)]))
            c.number_format = "0.0"
            if (i, m) in fails:
                c.fill = FAIL
                c.font = Font(bold=True)
        ws.cell(r, 6, float(P.mol[i])).number_format = "0.0"
        bad = [A.MONTH_NAME[m] for (j, m) in fails if j == i]
        ws.cell(r, 7, "fails " + " and ".join(bad) if bad else "holds")
        r += 1
    ws.cell(r, 1, "PB9")
    ws.cell(r, 6, float(P.mol["PB9"])).number_format = "0.0"
    ws.cell(r, 7, "holds" if all(lev[("PB9", m)] <= P.mol["PB9"] for m in A.MONTHS) else "fails")
    ws.cell(r, 2, "new bore, levels from the October 2026 test")
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
    r += 2
    a9 = {i: -c["PB9"] for i, c in A.fit_full(P, True).items()}
    ws.cell(r, 1, "PB9 drawdown on its neighbours at 4.40 ML/d (from the 7 to 14 October 2026 constant-rate "
                  "test, read in each bore's daily log): PB3 %.1f m, PB4 %.1f m"
            % (half(a9["PB3"] * 4.4), half(a9["PB4"] * 4.4)))
    r += 1
    ws.cell(r, 1, "Source: kaitanga_bores_daily_2014-2026.csv, MRC MB1 daily levels, PB9 test logger, bore "
                  "register, summer bore plan 28 Oct 2026.").font = Font(italic=True, size=9, color="5A656C")
    for k, wdt in enumerate([8, 11, 11, 11, 11, 13, 22], 1):
        ws.column_dimensions[get_column_letter(k)].width = wdt
    ws.freeze_panes = "B6"

    ws2 = wb.create_sheet("Pump energy")
    ws2["A1"] = "Pump electricity per megalitre pumped, year to 30 June 2026 (kWh/ML)"
    ws2["A1"].font = Font(bold=True, size=12)
    _head(ws2, 3, ["Bore"] + [QLAB[q] for q in range(1, 5)])
    for r, i in enumerate(A.EXISTING, 4):
        ws2.cell(r, 1, i)
        for q in range(1, 5):
            ws2.cell(r, 1 + q, int(round(energy[(i, q)]))).number_format = "#,##0"
    ws2.cell(13, 1, "ICP interval data from the metering provider; Bore 5 and Bore 6 share switchboard SB-3, split "
                    "by each pump's run hours times its motor rating. PB2's CT meter (from 11 Feb 2026) read at "
                    "x40.").font = Font(italic=True, size=9, color="5A656C")
    for k, wdt in enumerate([8, 14, 14, 14, 14], 1):
        ws2.column_dimensions[get_column_letter(k)].width = wdt
    ws2.freeze_panes = "B4"

    ws3 = wb.create_sheet("Permit meters")
    ws3["A1"] = "Take by bore as Matarae Regional Council's permit meters record it (ML)"
    ws3["A1"].font = Font(bold=True, size=12)
    _head(ws3, 3, ["Bore"] + [QLAB[q] for q in range(1, 5)] + ["Year"])
    for r, i in enumerate(A.EXISTING, 4):
        ws3.cell(r, 1, i)
        for q in range(1, 5):
            ws3.cell(r, 1 + q, int(round(meters[(i, q)]))).number_format = "#,##0"
        ws3.cell(r, 6, int(round(sum(meters[(i, q)] for q in range(1, 5))))).number_format = "#,##0"
    ws3.cell(13, 1, "15-minute totaliser readings (NZST) differenced and placed in NZ local quarters; Bore 4 includes "
                    "replacement meter WM-40958 from 17 Feb 2026.").font = Font(italic=True, size=9,
                                                                                color="5A656C")
    for k, wdt in enumerate([8, 14, 14, 14, 14, 12], 1):
        ws3.column_dimensions[get_column_letter(k)].width = wdt
    ws3.freeze_panes = "B4"
    wb.save(path)
    IO.repack_ooxml(path, "Megan Pickering", "Megan Pickering", "2026-11-03T20:12:00Z", "2026-11-05T01:48:00Z",
                    "Summer test 2026-27", "Ruawaro Dairy Co-operative Ltd")


# ---------------------------------------------------------------- deck
INK = RGBColor(0x1F, 0x2A, 0x30)
RED = "#B23A2B"


def chart(P, lev):
    fig, ax = plt.subplots(figsize=(7.6, 3.9), dpi=150)
    xs = range(len(A.MONTHS))
    for i in A.EXISTING:
        ys = [P.mol[i] - lev[(i, m)] for m in A.MONTHS]
        col = RED if i == "PB3" else "#9AA7B0"
        ax.plot(xs, ys, marker="o", color=col, lw=2.4 if i == "PB3" else 1.1, zorder=3 if i == "PB3" else 2)
        ax.annotate(i, (3, ys[-1]), xytext=(6, 0), textcoords="offset points", va="center", fontsize=8,
                    color=col)
    ax.axhline(0, color="#1F2A30", lw=1)
    ax.text(0.02, 0.08, "minimum operating level", fontsize=8, color="#1F2A30")
    ax.set_xticks(list(xs))
    ax.set_xticklabels([MLAB[m] for m in A.MONTHS])
    ax.set_ylabel("Water above minimum operating level (m)")
    ax.set_title("PB3 drops below its minimum in Feb and Mar under the drought test", fontsize=10, loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#E3E8EB", lw=0.8)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def deck(P, lev, fails, path):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    blank = prs.slide_layouts[6]

    def text(slide, x, y, w, h, s, size=14, bold=False, color=INK):
        tb = slide.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h))
        tf = tb.text_frame
        tf.word_wrap = True
        for k, line in enumerate(s.split("\n")):
            p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
            p.text = line
            p.font.size = Pt(size)
            p.font.bold = bold
            p.font.color.rgb = color
        return tb

    s1 = prs.slides.add_slide(blank)
    text(s1, 600000, 380000, 11000000, 900000, "The 2026-27 bore plan fails the drought test at PB3 in February "
         "and March", 26, True)
    text(s1, 600000, 1350000, 5200000, 4600000,
         "With PB9 taking 4.40 ML/d from December, PB3's lowest level reaches 35.5 m below measuring point in "
         "February and March against a minimum operating level of 35.0 m.\n\n"
         "PB9 sits in the same gravel channel as PB3: its October test drew PB3 down by about 0.66 m for each "
         "ML/d it pumped, 3.0 m at the planned take. PB4, closer on the map, moved 0.5 m.\n\n"
         "Every other bore, PB9 included, stays above its minimum in all four months.\n\n"
         "Ask: do not adopt the plan as drafted; bring back a revision that takes PB3 or PB9 down in February "
         "and March (SWS-03 section 5).", 14)
    s1.shapes.add_picture(io.BytesIO(chart(P, lev)), Emu(5900000), Emu(1350000), width=Emu(5900000))
    text(s1, 600000, 6250000, 11000000, 400000, "Site drought committee, 6 November 2026. Source: SCADA daily log "
         "2014-2026, MRC MB1, PB9 test logger, summer bore plan (28 Oct).", 9, color=RGBColor(0x5A, 0x65, 0x6C))

    s2 = prs.slides.add_slide(blank)
    text(s2, 600000, 380000, 11000000, 700000, "Lowest level in each month under the design drought (m bmp, "
         "nearest 0.5 m)", 22, True)
    rows, cols = len(A.EXISTING) + 2, 6
    tbl = s2.shapes.add_table(rows, cols, Emu(600000), Emu(1250000), Emu(10500000), Emu(4600000)).table
    hdr = ["Bore", "Dec 2026", "Jan 2027", "Feb 2027", "Mar 2027", "Minimum"]
    for k, h in enumerate(hdr):
        tbl.cell(0, k).text = h
    for r, i in enumerate(A.EXISTING, 1):
        tbl.cell(r, 0).text = i
        for k, m in enumerate(A.MONTHS, 1):
            tbl.cell(r, k).text = "%.1f%s" % (half(lev[(i, m)]), " *" if (i, m) in fails else "")
        tbl.cell(r, 5).text = "%.1f" % P.mol[i]
    r = len(A.EXISTING) + 1
    tbl.cell(r, 0).text = "PB9"
    tbl.cell(r, 1).text = "holds in every month"
    tbl.cell(r, 5).text = "%.1f" % P.mol["PB9"]
    for rr in range(rows):
        for k in range(cols):
            for p in tbl.cell(rr, k).text_frame.paragraphs:
                p.font.size = Pt(12)
    text(s2, 600000, 6050000, 11000000, 500000, "* below minimum operating level. Takes as the 28 October plan; "
         "aquifer at MB1's December 2019 to March 2020 levels.", 10, color=RGBColor(0x5A, 0x65, 0x6C))
    prs.core_properties.author = "Megan Pickering"
    prs.save(path)
    IO.repack_ooxml(path, "Megan Pickering", "Megan Pickering", "2026-11-04T19:30:00Z", "2026-11-05T02:05:00Z",
                    "Bore plan 2026-27", "Ruawaro Dairy Co-operative Ltd")


def write_all(target, golden_dir, gen_dir):
    os.makedirs(golden_dir, exist_ok=True)
    P, lev, fails, energy, meters, fig = compute(target)
    workbook(P, lev, fails, energy, meters, os.path.join(golden_dir, BOOK))
    deck(P, lev, fails, os.path.join(golden_dir, DECK))
    json.dump(fig, open(os.path.join(gen_dir, "figures.json"), "w"), indent=1, sort_keys=True)
    return P, lev, fails, fig
