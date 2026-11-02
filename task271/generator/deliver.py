"""task271 goldens: stocking_tiers_2027.xlsx (the tiers with each lake's 2026 angler-hours per hectare, the 2026
releases and the July and August warm days) and stocking_board_note_2027.docx (one page with the chart), every figure
computed by analysis.py from target/ alone; then figures.json and submission.md."""
from __future__ import annotations

import io
import json
import math
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt                              # noqa: E402
import openpyxl                                              # noqa: E402
from docx import Document                                    # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH                # noqa: E402
from docx.shared import Cm, Pt, RGBColor                     # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill     # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A        # noqa: E402
import common as K          # noqa: E402
import postprocess as PP    # noqa: E402

F_TIERS = "stocking_tiers_2027.xlsx"
F_NOTE = "stocking_board_note_2027.docx"
# the precision every reading of the counts shares: each high-use lake above BAND_HIGH and each standard lake below
# BAND_STD angler-hours per hectare under all fifty presence readings (checks.py asserts it); the plain expansion
# puts its three general lakes above BAND_PLAIN_IN and the four fly-only lakes below BAND_PLAIN_OUT under each of its
# own readings
BAND_HIGH, BAND_STD = 550, 480
BAND_PLAIN_IN, BAND_PLAIN_OUT = 550, 460


def r10(x):
    return int(math.floor(x / 10.0 + 0.5) * 10)


def r100(x):
    return int(math.floor(x / 100.0 + 0.5) * 100)


def compute(target):
    M = A.main_call(target)
    reg = M["reg"]
    stocked = sorted(c for c, v in reg.items() if v["access"] != "walk-in")
    rel = A.releases(target)
    warm, _ = A.warm_days(target)
    import csv as _csv
    raw = {}
    for r in _csv.DictReader(open(os.path.join(target, "lake_temperature_loggers_2026.csv"))):
        raw.setdefault(r["Logger SN"], []).append((A.dt.datetime.strptime(r["Date Time"], "%Y-%m-%d %H:%M"),
                                                   float(r["Temp (C)"])))
    utc = sorted(s for s, o in A.logger_clock_offsets(raw).items() if o == -7)
    name = {c: reg[c]["name"] for c in reg}
    lakes = M["lakes"]
    high = [c for c in stocked if lakes[c]["golden"] >= K.THRESHOLD]
    fam = A.presence_family(target)
    nh, ns = {}, {}
    for k in fam[high[0]]:
        lo = min(high, key=lambda c: fam[c][k])
        hi = max((c for c in stocked if c not in high), key=lambda c: fam[c][k])
        nh[lo] = nh.get(lo, 0) + 1
        ns[hi] = ns.get(hi, 0) + 1
    nearest_high = sorted(nh, key=lambda c: (-nh[c], c))
    nearest_std = sorted(ns, key=lambda c: (-ns[c], c))
    f = {
        "call": {
            "high_use": [name[c] for c in high],
            "standard": [name[c] for c in stocked if c not in high],
            "high_use_codes": high,
            "count_high_use": len(high),
            "count_lakes": len(stocked),
        },
        "chart_bars_per_ha": {name[c]: r10(lakes[c]["golden"]) for c in stocked},
        "bands": {"high_use_above": BAND_HIGH, "standard_below": BAND_STD,
                  "plain_in_above": BAND_PLAIN_IN, "plain_out_below": BAND_PLAIN_OUT},
        "nearest_high": [name[c] for c in nearest_high],
        "nearest_standard": [name[c] for c in nearest_std],
        "anglers_per_boat": {name[c]: round(lakes[c]["apb"], 2) for c in stocked},
        "parties_interviewed": {name[c]: lakes[c]["n_parties"] for c in stocked},
        "area_ha": {name[c]: reg[c]["area"] for c in stocked},
        "tier": {name[c]: ("high use" if c in high else "standard") for c in stocked},
        "plain_expansion": {
            "set": [name[c] for c in stocked if lakes[c]["R1"] >= K.THRESHOLD],
        },
        "pooled_profile_set": [name[c] for c in stocked if lakes[c]["R2"] >= K.THRESHOLD],
        "releases_alive": {name[c]: r100(rel[c]) for c in sorted(rel)},
        "warm_days": {name[c]: warm[c] for c in sorted(warm)},
        "constants": {"threshold": K.THRESHOLD, "day_open": "05:00", "day_close": "22:00", "angling_day_hours": 17,
                      "line_c": 20, "release_rounding": 100, "logger_depth_m": 1},
        "utc_loggers": utc,
    }
    return M, f


def write_tiers(path, M, f):
    reg = M["reg"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Tiers 2027"
    head = ["PPFS code", "Lake", "Regulation", "Area (ha)", "Parties interviewed", "Anglers per boat",
            "Angler-hours per ha, 2026", "Tier 2027"]
    ws.append(head)
    bands = f["bands"]
    for c in sorted(f["call"]["high_use_codes"] + [k for k, v in reg.items() if v["access"] != "walk-in"
                                                    and k not in f["call"]["high_use_codes"]]):
        n = reg[c]["name"]
        band = ("above %d" % bands["high_use_above"]) if f["tier"][n] == "high use" else ("below %d" % bands["standard_below"])
        ws.append([c, n, reg[c]["reg"], reg[c]["area"], f["parties_interviewed"][n], f["anglers_per_boat"][n],
                   band, f["tier"][n].capitalize()])
    widths = [10, 19, 30, 9, 11, 10, 14, 11]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
        cell = ws.cell(row=1, column=i)
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor="DCE6DE")
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    for r in range(2, ws.max_row + 1):
        ws.cell(row=r, column=4).number_format = "0.0"
        ws.cell(row=r, column=6).number_format = "0.00"
        if ws.cell(row=r, column=8).value == "High use":
            ws.cell(row=r, column=8).font = Font(bold=True)
    ws.freeze_panes = "C2"
    r = ws.max_row + 2
    ws.cell(row=r, column=1, value="High-use line: 500 angler-hours per ha (allocation policy 2.2). Angler-hours: "
                                   "each flight count over the share of that lake's interviewed angler-hours at the "
                                   "time of the count, averaged by survey day and expanded by weekday and weekend day "
                                   "each month; the bands hold however the count's time is read against the hours.")
    ws.cell(row=r, column=1).font = Font(italic=True, size=9)

    ws2 = wb.create_sheet("Releases 2026")
    ws2.append(["PPFS code", "Lake", "Catchables released alive (nearest 100)"])
    by_name = {v["name"]: k for k, v in reg.items()}
    for n, v in sorted(f["releases_alive"].items(), key=lambda kv: by_name[kv[0]]):
        ws2.append([by_name[n], n, v])
    for i, w in enumerate([10, 19, 22], start=1):
        ws2.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
        ws2.cell(row=1, column=i).font = Font(bold=True)
        ws2.cell(row=1, column=i).alignment = Alignment(wrap_text=True, vertical="top")
    for rr in range(2, ws2.max_row + 1):
        ws2.cell(row=rr, column=3).number_format = "#,##0"

    ws3 = wb.create_sheet("Warm days Jul-Aug")
    ws3.append(["PPFS code", "Lake", "Days above 20 C at 1 m"])
    for n, v in sorted(f["warm_days"].items(), key=lambda kv: by_name[kv[0]]):
        ws3.append([by_name[n], n, v])
    for i, w in enumerate([10, 19, 14], start=1):
        ws3.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
        ws3.cell(row=1, column=i).font = Font(bold=True)
        ws3.cell(row=1, column=i).alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    PP.normalize_ooxml(path, K.PEOPLE["creel"], K.PEOPLE["stocking"], "2026-10-26T16:05:00Z", "2026-10-26T21:37:00Z",
                       excel=True, company=K.SOCIETY)


def chart_png(f):
    items = sorted(f["chart_bars_per_ha"].items(), key=lambda kv: -kv[1])
    names = [n.replace(" Lake", "") for n, _ in items]
    vals = [v for _, v in items]
    cols = ["#2f6b3a" if f["tier"][n] == "high use" else "#a9b8ac" for n, _ in items]
    fig, ax = plt.subplots(figsize=(6.6, 3.0), dpi=150)
    ax.bar(range(len(vals)), vals, color=cols, width=0.72)
    ax.axhline(K.THRESHOLD, color="#8a2b1f", lw=1.1, ls="--")
    ax.text(len(vals) - 0.5, K.THRESHOLD + 25, "high-use line, 500", ha="right", va="bottom", fontsize=7.5,
            color="#8a2b1f")
    ax.set_xticks(range(len(vals)))
    ax.set_xticklabels(names, rotation=60, ha="right", fontsize=7)
    ax.set_ylabel("Angler-hours per ha, 2026", fontsize=8)
    ax.tick_params(axis="y", labelsize=7)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_xlim(-0.6, len(vals) - 0.4)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def write_note(path, M, f):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.59), Cm(27.94)
    sec.left_margin = sec.right_margin = Cm(2.0)
    sec.top_margin, sec.bottom_margin = Cm(1.6), Cm(1.5)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)
    h = doc.add_paragraph()
    run = h.add_run("2027 catchable tiers: lakes for the high-use tier")
    run.bold = True
    run.font.size = Pt(13)
    run.font.color.rgb = RGBColor(0x2E, 0x52, 0x33)
    p = doc.add_paragraph()
    p.add_run("Stocking plan 2027, item for the November meeting. Prepared 26 October 2026.").italic = True
    hi = [n.replace(" Lake", "") for n in f["call"]["high_use"]]
    doc.add_paragraph(
        "Recommendation. %s go into the high-use tier for 2027; every other lake that takes catchables stays "
        "standard. Each of these lakes was fished for more than 500 angler-hours per hectare between 15 May and "
        "31 August 2026." % (", ".join(hi[:-1]) + " and " + hi[-1]))
    out = [n.replace(" Lake", "") for n in f["plain_expansion"]["set"] if n not in f["call"]["high_use"]]
    came = [n.replace(" Lake", "") for n in f["call"]["high_use"] if n not in f["plain_expansion"]["set"]]
    doc.add_paragraph(
        "How the hours were counted. The survey flights pass each lake at the same point in each loop, between "
        "about 09:30 and 12:00 in the morning and 14:30 and 17:00 in the afternoon, which is when anglers crowd the "
        "general-regulation lakes and when the fly-only lakes are at their quietest. The interviews give the time "
        "every party started and finished, so for each lake we know what share of its angler-hours fall in each hour "
        "of the 05:00 to 22:00 day. Each count was divided by that lake's share for the hour it was made, then "
        "averaged by survey day and raised to the season by weekday and weekend day in each month.")
    doc.add_paragraph(
        "What this changes. Multiplying each count by the 17-hour day would have put %s in the tier and left %s out: "
        "the fly-only lakes' anglers are on the water at dawn and in the evening, hours no flight sees, while the "
        "general lakes' anglers are out in the hours the flights cover." %
        (", ".join(out[:-1]) + " and " + out[-1], ", ".join(came[:-1]) + " and " + came[-1]))
    doc.add_picture(io.BytesIO(chart_png(f)), width=Cm(16.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap = doc.add_paragraph()
    cap.add_run("Angler-hours per hectare, 15 May to 31 August 2026; dark bars are the lakes recommended for the "
                "high-use tier.").font.size = Pt(8.5)
    tot = sum(f["releases_alive"].values())
    doc.add_paragraph(
        "Also in the workbook: the catchables each lake received alive in 2026 (%s in all, rounded lake by lake) "
        "and, for the lakes with a logger at 1 m, the July and August days the water there averaged above 20 C."
        % "{:,}".format(tot))
    doc.save(path)
    PP.normalize_docx(path, K.PEOPLE["creel"], K.PEOPLE["stocking"], "2026-10-26T17:10:00Z", "2026-10-26T22:04:00Z",
                      4, 96, "t271-note", title="2027 catchable tiers", company=K.SOCIETY)


def main(target, golden, figures_path, submission_path):
    os.makedirs(golden, exist_ok=True)
    M, f = compute(target)
    write_tiers(os.path.join(golden, F_TIERS), M, f)
    write_note(os.path.join(golden, F_NOTE), M, f)
    f["releases_total"] = sum(f["releases_alive"].values())
    with open(figures_path, "w") as fh:
        json.dump(f, fh, indent=1, sort_keys=True)
        fh.write("\n")
    import writeup
    writeup.write(f, submission_path)
    return f


if __name__ == "__main__":
    T = os.path.dirname(HERE)
    main(os.path.join(T, "target"), os.path.join(T, "golden"), os.path.join(HERE, "figures.json"),
         os.path.join(T, "submission.md"))
