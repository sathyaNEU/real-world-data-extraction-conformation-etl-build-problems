"""The golden deliverables from the shipped files alone (solve.py's path): the recall return and notification list
j26-1187_recall_uplifts.csv, and hydrant_resumption_plan.pdf with its schematic; and generator/figures.json, every
figure the write-up states, in the form it states it.

    python3 task488/generator/deliver.py
"""
import csv
import io
import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import names as N    # noqa: E402
import solve as S    # noqa: E402

AGENT = {"Corbel": N.CORBEL, "Northgarth": N.NORTHGARTH}
SECTION_NAMES = {"FARM": "Farm header", "MAIN": "Hydrant main", "A": "Pier A", "B": "Pier B",
                 "C": "International apron", "E": "Cargo apron", "F": "Remote stands", "G": "Maintenance base"}
CRITICAL = "#d03b3b"      # status: holds the recalled batch
INK2 = "#52514e"          # secondary ink: the clear network
MUTED = "#898781"
SURFACE = "#fcfcfb"


WORDS = {k: w for k, w in enumerate(["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
                                      "ten", "eleven", "twelve"])}


def comma(v):
    return "{:,}".format(v)


def compute(target):
    a = S.answer(target)
    tk = S.tickets(target)
    r0 = S.reckoning(target, a["hy"])
    rows = []
    for key, b in a["hy"]["took"].items():
        t = tk[key]
        rows.append([key, AGENT[t["agent"]], t["operator"], t["flight"], t["reg"], t["start_utc"], t["location"],
                     t["litres_15c"], S.rnd(b, 10)])
    for key, (b, airline, agent, unit, ut, v, tank) in a["rf"]["delivered"].items():
        t = tk[key]
        loc = tank if tank == unit else "%s (tractor %s)" % (tank, unit)
        rows.append([key, AGENT[agent], t["operator"], t["flight"], t["reg"], t["start_utc"], loc, v, S.rnd(b, 10)])
    rows.sort(key=lambda r: (r[5], r[0]))
    for r in rows:
        r[5] = r[5].strftime("%Y-%m-%dT%H:%MZ")
    net = a["hy"]["net"]
    segs = {}
    for seg, b in sorted(a["hy"]["segments"].items()):
        segs.setdefault(net.section_of[seg], []).append(seg)
    by_air_rows = {}
    for r in rows:
        if not r[6].startswith("P-"):
            by_air_rows[r[2]] = by_air_rows.get(r[2], 0) + r[8]
    for k, v in a["by_air_10"].items():
        assert S.rnd(by_air_rows[k], 10) == v, (k, by_air_rows[k], v)
    return a, rows, segs, r0


# ------------------------------------------------------------------------------------------------ the CSV
CSV_COLS = ["ticket_number", "into_plane_agent", "aircraft_operator", "flight", "registration", "uplift_start_utc",
            "location", "litres_delivered_15c", "litres_j26_1187_15c"]


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(CSV_COLS)
        w.writerows(rows)


# ------------------------------------------------------------------------------------------------ the schematic
def schematic(target, segs, standing):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    net = S.Net(target)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7.5, "svg.hashsalt": "task488"})
    red = {s for v in segs.values() for s in v}
    length = {}
    for r in S.sheet(os.path.join(target, S.F["register"]), "Segments"):
        length[r["Segment ID"]] = r["Length (m)"]
    pos = {"P": (0.0, 0.0), "N0": (0.9, 0.0), "J1": (3.6, 0.0), "J2": (5.4, 0.0), "J3": (6.9, 0.0)}
    up = {"A": 1, "G": -1, "B": 1, "E": -1, "C": 1, "F": -1}
    for sec in ("A", "B", "C", "E", "F", "G"):
        segs_sec = [s for s in net.order if net.section_of[s] == sec]
        x, y = pos[net.frm[segs_sec[0]]]
        for s in segs_sec:
            step = 0.30 + min(length[s], 1100) * 0.0011
            if net.to[s].endswith("X"):
                step = 0.22
            y += up[sec] * step
            pos[net.to[s]] = (x, y)
    fig, ax = plt.subplots(figsize=(7.2, 5.1), dpi=200)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    for s in net.order:
        (x0, y0), (x1, y1) = pos[net.frm[s]], pos[net.to[s]]
        hot = s in red
        ax.plot([x0, x1], [y0, y1], color=CRITICAL if hot else INK2, lw=4.2 if hot else 1.5,
                solid_capstyle="butt", zorder=3 if hot else 2)
    for p in net.points:
        x, y = pos[p["Node ID"]]
        if p["Stand no"]:
            ax.plot([x], [y], marker="o", ms=3.6, color="#0b0b0b", mec=SURFACE, mew=0.8, zorder=4)
            ax.text(x + 0.09, y, str(p["Stand no"]), va="center", ha="left", fontsize=5.6, color=MUTED)
        else:
            ax.plot([x], [y], marker="s", ms=3.2, color=MUTED, zorder=4)
    for name, (x, y) in (("Pump station", pos["P"]),):
        ax.text(x, y - 0.22, name, ha="left", va="top", fontsize=6.6, color=INK2)
    for j in ("J1", "J2", "J3"):
        x, y = pos[j]
        ax.text(x - 0.08, y + 0.08, j, ha="right", va="bottom", fontsize=5.8, color=MUTED)
    tip = {}
    for sec in ("A", "B", "C", "E", "F", "G"):
        end = sec + "X"
        tip[sec] = pos[end]
        x, y = pos[end]
        ax.text(x, y + up[sec] * 0.16, SECTION_NAMES[sec], ha="center", va="bottom" if up[sec] > 0 else "top",
                fontsize=7.2, color="#0b0b0b", fontweight="bold")
    for sec, seglist in segs.items():
        ys = [pos[net.to[s]][1] for s in seglist] + [pos[net.frm[s]][1] for s in seglist]
        x = pos[net.to[seglist[0]]][0]
        ax.text(x - 0.14, (min(ys) + max(ys)) / 2, "%s L" % comma(standing[sec]), ha="right", va="center",
                fontsize=7.4, color="#0b0b0b", fontweight="bold")
    ax.text(2.2, 0.10, "Hydrant main", ha="center", va="bottom", fontsize=6.6, color=INK2)
    handles = [Line2D([0], [0], color=CRITICAL, lw=4.2, label="holds J-26-1187 at the 05:30 suspension"),
               Line2D([0], [0], color=INK2, lw=1.5, label="clear of J-26-1187"),
               Line2D([0], [0], marker="o", ls="", color="#0b0b0b", ms=3.6, label="hydrant pit (stand number)"),
               Line2D([0], [0], marker="s", ls="", color=MUTED, ms=3.2, label="branch end low point drain")]
    ax.legend(handles=handles, loc="lower left", frameon=False, fontsize=6.4, bbox_to_anchor=(0.0, 0.0))
    xs = [v[0] for v in pos.values()]
    ys = [v[1] for v in pos.values()]
    ax.set_xlim(min(xs) - 0.3, max(xs) + 0.9)
    ax.set_ylim(min(ys) - 0.5, max(ys) + 0.5)
    ax.set_aspect("equal")
    ax.axis("off")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, facecolor=SURFACE, bbox_inches="tight", pad_inches=0.06,
                metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def facts(target, a):
    """The plan's prose facts, each read off the shipped files."""
    import datetime as dt
    hy = a["hy"]
    net = hy["net"]
    tue0, tue1 = dt.datetime(2026, 10, 13), dt.datetime(2026, 10, 14)
    tickets = [d for d in hy["draws"] if not d[0].startswith(("flush", "drain"))]
    f_tue = [d for d in tickets if net.section_of[net.into[net.node_of[d[1]]]] == "F" and tue0 <= d[2] < tue1]
    e_draws = sorted([d for d in tickets if net.section_of[net.into[net.node_of[d[1]]]] == "E" and d[2] >= tue0],
                     key=lambda d: d[2])
    first_e = [p["Point ID"] for p in net.points if p["Section code"] == "E" and p["Stand no"]][0]
    k = len(e_draws)
    while k > 0 and e_draws[k - 1][1] == first_e:
        k -= 1
    since = e_draws[k - 1][3].strftime("%H:%M") if k > 0 else "06:00"
    assert all(d[1] == first_e for d in e_draws[k:]) and k < len(e_draws)
    import re
    import pdfplumber
    with pdfplumber.open(os.path.join(target, S.F["shiftlog"])) as pdf:
        text = re.sub(r"\s+", " ", " ".join((pg.extract_text() or "") for pg in pdf.pages))
    pc = re.findall(r"(\d\d:\d\d) Product change check at P-A01", text)
    return {"f_draws_tue": len(f_tue), "e_since": since, "pc": pc}


# ------------------------------------------------------------------------------------------------ the plan
def write_plan(path, target, a, rows, segs):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    import docs as DC      # the Operator's house style and fonts
    ink = colors.HexColor("#1c1f22")
    grey = colors.HexColor("#5d6369")
    body = ParagraphStyle("pb", fontName="LiberationSerif", fontSize=10, leading=13.6, textColor=ink, spaceAfter=6)
    h1 = ParagraphStyle("ph1", fontName="LiberationSans-Bold", fontSize=13, leading=16.5, textColor=DC.NAVY,
                        spaceAfter=4)
    h2 = ParagraphStyle("ph2", fontName="LiberationSans-Bold", fontSize=10, leading=13, textColor=ink, spaceBefore=7,
                        spaceAfter=3)
    memo = ParagraphStyle("pm", fontName="LiberationSans", fontSize=8.8, leading=11.6, textColor=ink)
    note = ParagraphStyle("pn", fontName="LiberationSans", fontSize=7.6, leading=9.8, textColor=grey)
    cell = DC.CELL
    cellb = DC.CELLB

    def table(data, widths, right=()):
        t = Table([[Paragraph(str(c), cellb if i == 0 else cell) for c in r] for i, r in enumerate(data)],
                  colWidths=widths, hAlign="LEFT", repeatRows=1)
        st = [("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#7d858c")),
              ("LINEBELOW", (0, 1), (-1, -1), 0.3, colors.HexColor("#c9ced2")),
              ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 3),
              ("RIGHTPADDING", (0, 0), (-1, -1), 3)]
        t.setStyle(TableStyle(st))
        return t

    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans-Bold", 8)
        canvas.setFillColor(DC.NAVY)
        canvas.drawString(18 * mm, LETTER[1] - 12 * mm, "%s  |  Fuel quality, Windrell" % N.OPERATOR)
        canvas.setFont("LiberationSans", 7.2)
        canvas.setFillColor(grey)
        canvas.drawString(18 * mm, 11 * mm, "J-26-1187 recall  |  resumption plan for the Fuel Quality Committee  |  "
                                            "14 October 2026")
        canvas.drawRightString(LETTER[0] - 18 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()

    doc = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=19 * mm,
                            bottomMargin=18 * mm, title="J-26-1187 hydrant resumption plan", author=N.OPERATOR,
                            subject="", creator="", producer="")
    secs = a["sections"]
    st = a["standing_100"]
    held = a["held_10"]
    n_h, n_r = a["hydrant_uplifts"], a["refueller_uplifts"]
    names = {s: SECTION_NAMES[s] for s in secs}
    s = [Paragraph("To: Fuel Quality Committee, %s<br/>From: %s, fuel quality manager, %s<br/>"
                   "Date: 14 October 2026, 07:55<br/>Subject: recalled batch J-26-1187, what is drained before "
                   "fuelling resumes<br/>References: QM-09 sections 3 and 4; %s notice RN-2026-031"
                   % (N.CORP, N.QM_MANAGER, N.OPERATOR, N.SUPPLIER), memo), Spacer(1, 8),
         Paragraph("J-26-1187 still stands in three hydrant sections and four refuellers; %d uplifts took it"
                   % (n_h + n_r), h1)]
    s.append(Paragraph(
        "At the 05:30 suspension fuel from J-26-1187 stood in %s (the pipe under stands 27 and 28, closed since "
        "15:00 yesterday), in the %s beyond its first pit and in the %s, %s, %s and %s of the batch, and in "
        "refuellers %s. "
        "The farm header, the main, Pier A, the international apron and the maintenance base hold none of it. "
        "Each section and refueller below is drained before it fuels again (QM-09 3.2); everything else can "
        "resume once the committee approves." % (
            names["B"], names["E"].lower(), names["F"].lower(), comma(st["B"]) + " L", comma(st["E"]) + " L",
            comma(st["F"]) + " L", ", ".join(a["refuellers"][:-1]) + " and " + a["refuellers"][-1]), body))
    fx = facts(target, a)
    s.append(Paragraph(
        "The batch went where the pits drew it. The hydrant is always full, so fuel in a branch moves only when a "
        "pit beyond it draws: Pier A, Pier B's open stands and the international apron took the batch soon after "
        "the main turned over and had drawn it out again on Tank 1 before the suspension, but the cargo apron's "
        "uplifts after %s were all at its first pit, the remote stands drew %s times all Tuesday, and nothing has "
        "drawn under stands 27 and 28 since they closed. The maintenance base drew nothing on Tuesday and never "
        "took the batch. One line fill through the pump station's meter, which is when the %s and %s product change "
        "checks at P-A01 were taken, turns over the main and the busy piers, not these branches; the densities in "
        "the agents' shift-start and idle-pit checks agree with this tracing at every pit and time they were "
        "taken." % (fx["e_since"], WORDS[fx["f_draws_tue"]], fx["pc"][0], fx["pc"][1]), body))
    s.append(Paragraph("Hydrant sections to drain", h2))
    data = [["Section", "Segments holding the batch", "Batch litres standing", "Drain point"]]
    for sec in secs:
        data.append([names[sec], ", ".join(segs[sec]), comma(st[sec]), "LPD-%s, section valve SV-%s shut" % (sec, sec)])
    s.append(table(data, [34 * mm, 56 * mm, 34 * mm, 52 * mm]))
    s.append(Paragraph("Source: hydrant network register (segment lengths and bores); both agents' tickets, 12 to 14 "
                       "October; the low point drain and idle-pit flush records. Nearest 100 L.", note))
    s.append(Paragraph("Refuellers to drain", h2))
    where = {"RF-23": "Corbel workshop (hose reel), since 13:06 yesterday",
             "RF-24": "Corbel, north apron",
             "T-31": "Northgarth workshop bay 2 (axle bearing), since 11:52 yesterday",
             "T-35": "Northgarth, coupled to tractor N-7 since 11:58 yesterday"}
    data = [["Refueller", "Agent", "Where it is", "Batch litres held"]]
    for k in a["refuellers"]:
        data.append([k, N.CORBEL if k.startswith("RF") else N.NORTHGARTH, where.get(k, ""), comma(held[k])])
    s.append(table(data, [22 * mm, 46 * mm, 76 * mm, 32 * mm]))
    s.append(Paragraph("Source: rack loading log; both agents' tickets; Corbel's equipment log (RF-23 pumped %s L to "
                       "RF-24 at 12:50 yesterday); Northgarth's vehicle log (couplings). Each tank taken as one mixed "
                       "body of fuel from the weekly dip of 12 October. Nearest 10 L." % comma(
                           next(int(r["qty_l"]) for r in S.rows_csv(os.path.join(target, S.F["corbel_equipment"]))
                                if r["event_code"] == "TRANSFER")), note))
    from reportlab.platypus import KeepTogether
    data = [["Airline", "Batch litres delivered by refuellers"]]
    for k in sorted(a["by_air_10"]):
        data.append([k, comma(a["by_air_10"][k])])
    s.append(KeepTogether([
        Paragraph("Aircraft operators to notify", h2),
        Paragraph("%d uplifts delivered fuel from the batch: %d through the hydrant and %d from refuellers, each listed "
                  "with its ticket, registration, flight, start in UTC, pit or refueller and litres in "
                  "j26-1187_recall_uplifts.csv, which is also the recall return. The refuellers' share by airline:"
                  % (n_h + n_r, n_h, n_r), body),
        table(data, [60 * mm, 60 * mm]),
        Paragraph("Nearest 10 L, from the unrounded litres of each uplift.", note)]))
    png = schematic(target, segs, st)
    from reportlab.lib.utils import ImageReader
    ir = ImageReader(io.BytesIO(png))
    iw, ih = ir.getSize()
    w = 176 * mm
    s.append(Spacer(1, 6))
    s.append(Paragraph("Where J-26-1187 stood at the 05:30 suspension", h2))
    s.append(Image(io.BytesIO(png), width=w, height=w * ih / iw))
    s.append(Paragraph("Schematic, not to scale. Litres of pipe at line temperature from the register; at 15 C each "
                       "section rounds to the same 100 L.", note))
    s.append(Spacer(1, 8))
    s.append(Paragraph("N. Daugherty, fuel quality manager, %s, for the Fuel Quality Committee meeting of 14 October "
                       "2026, 08:00." % N.OPERATOR, note))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------ figures.json
def figures(a, rows, segs, r0):
    held = a["held_10"]
    return {
        "call": {"sections": a["sections"], "section_names": {s: SECTION_NAMES[s] for s in a["sections"]},
                 "standing_100": a["standing_100"], "segments": segs, "hydrant_uplifts": a["hydrant_uplifts"],
                 "clear": [s for s in ("FARM", "MAIN", "A", "C", "G")]},
        "refuellers": {"set": a["refuellers"], "held_10": held, "refueller_uplifts": a["refueller_uplifts"],
                       "by_air_10": a["by_air_10"]},
        "csv": {"rows": len(rows), "hydrant_rows": a["hydrant_uplifts"], "refueller_rows": a["refueller_uplifts"]},
        "rung0": {"line_fill": r0["line_fill"], "edges": [r0["edges"][0].strftime("%H:%M"), r0["edges"][1].strftime("%H:%M")],
                  "uplifts": r0["uplifts"]},
        "transfer_litres": None,
        "rack_line_fill": a["hy"]["net"].rack_fill,
        "hydrant_tickets_by_section": {sec: [r[0] for r in rows if r[6].startswith("P-") and r[6][2] == sec]
                                       for sec in ("A", "B", "C", "E", "F", "G")},
        "refueller_rows": [[r[0], r[2], r[6], r[7], r[8]] for r in rows if not r[6].startswith("P-")],
    }


def main(target, gdir, fig_path):
    os.makedirs(gdir, exist_ok=True)
    a, rows, segs, r0 = compute(target)
    write_csv(os.path.join(gdir, N.GOLDEN["csv"]), rows)
    write_plan(os.path.join(gdir, N.GOLDEN["pdf"]), target, a, rows, segs)
    import postprocess as PP
    PP.normalize_pdf(os.path.join(gdir, N.GOLDEN["pdf"]), b"D:20261014075500-07'00'", b"D:20261014075500-07'00'")
    fig = figures(a, rows, segs, r0)
    fig["transfer_litres"] = next(int(r["qty_l"]) for r in S.rows_csv(os.path.join(target, S.F["corbel_equipment"]))
                                  if r["event_code"] == "TRANSFER")
    import re
    import pdfplumber
    import datetime as dt
    with pdfplumber.open(os.path.join(target, S.F["shiftlog"])) as pdf:
        text = re.sub(r"\s+", " ", " ".join((pg.extract_text() or "") for pg in pdf.pages))
    ron, roff = S.rack_lineups(target)
    couple = next(dt.datetime.strptime(r["time_utc"], "%Y-%m-%dT%H:%MZ") - S.UTC_OFF
                  for r in S.rows_csv(os.path.join(target, S.F["ng_vehicles"]))
                  if r["event_code"] == "COUPLE" and "T-35" in r["remarks"])
    fig["times"] = {"stands_closed": re.search(r"(\d\d:\d\d) Airport Operations: stands 27 and 28 closed", text).group(1),
                    "hydrant_on": a["hy"]["on"].strftime("%H:%M"), "hydrant_off": a["hy"]["off"].strftime("%H:%M"),
                    "rack_on": ron.strftime("%H:%M"), "rack_off": roff.strftime("%H:%M"),
                    "coupling_t35": couple.strftime("%H:%M")}
    fig["hydrant_counts_by_section"] = {k: len(v) for k, v in fig["hydrant_tickets_by_section"].items()}
    bands = S.row_bands(target, a["hy"])
    fig["partial_rows"] = [[k, bands[k]["batch_10"], bands[k]["litres_15c"], bands[k]["band"]] for k in sorted(bands)]
    fig["row_band_whole_l"] = 10
    fig["rounding_litres"] = {"hydrant_standing": 100, "refuellers_and_rows": 10}
    with open(fig_path, "w", encoding="utf-8") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
        f.write("\n")
    return fig


if __name__ == "__main__":
    root = os.path.dirname(HERE)
    main(os.path.join(root, "target"), os.path.join(root, "golden"), os.path.join(HERE, "figures.json"))
