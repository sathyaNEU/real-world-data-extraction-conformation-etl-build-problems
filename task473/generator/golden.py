"""The golden deliverables, from the generator's figures: the county file and the Center's certification letter to the
GHSO with its chart. Also generator/figures.json, which submission.md is drafted from."""
import csv
import json
import os

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.graphics.shapes import Drawing, Line, Rect, String  # noqa: E402
from reportlab.lib import colors                                    # noqa: E402
from reportlab.lib.pagesizes import letter                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                     # noqa: E402
from reportlab.lib.units import inch                                # noqa: E402
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import bundle as B    # noqa: E402
import docs as DC     # noqa: E402
import lab as L       # noqa: E402
import methods as M   # noqa: E402
import world as W     # noqa: E402

CSV_COLS = ["county_fips", "county", "ai_driving_deaths_2023_2025", "vmt_2023_2025_100m", "ai_driving_rate_per_100m_vmt",
            "high_range_fy2028", "arrests_blood_specimen_2025", "pct_arrests_015_or_more_2025",
            "injury_crashes_drinking_driver_2025"]
INK = colors.HexColor("#1f2124")
GREY = colors.HexColor("#5b5e63")
HIGH = colors.HexColor("#eb6834")     # validated pair (dataviz validate_palette.js, light surface): high-range
LOW = colors.HexColor("#2a78d6")      # below the line
GRID = colors.HexColor("#e3e4e6")
MAROON = colors.HexColor("#6b1d2a")


def _r2(v):
    return "%.2f" % v


def figures(x):
    """The figures the golden and the write-up state, at the prompt's rounding."""
    fig = x["fig"]
    rows = []
    for r in fig["rows"]:
        rows.append(dict(fips=r["fips"], county=r["county"], deaths=int(round(r["deaths"])), vmt=_r2(r["vmt"] / 1e8),
                         rate=_r2(r["rate"]), high=r["high"], arrests=r["arrests"], pct15="%.1f" % r["pct15"],
                         crashes=r["crashes"]))
    high = sorted([r for r in rows if r["high"]], key=lambda r: -float(r["rate"]))
    below = sorted([r for r in rows if not r["high"]], key=lambda r: -float(r["rate"]))
    top_below = [r for r in below if r["rate"] == below[0]["rate"]]
    catch = fig["catch"]
    obs, vmt = x["obs"], x["vmt"]
    rates = {k: M.rate(M.route(obs, k), vmt) for k in ("R6", "R8")}
    rival = {k: sorted(W.NAMES[f] for f, v in rates[k].items() if v >= W.THRESHOLD) for k in rates}
    unarr = [d for cr in obs for d in M.drivers(cr) if d["complete"] and not d["killed"] and d["tested"]
             and not d["arrested"]]
    share = 100.0 * sum(1 for d in unarr if d["bac"] >= M.LO) / len(unarr)
    imp = [d for cr in obs for d in M.drivers(cr) if d["complete"] and not d["killed"] and d["tested"]
           and d["bac"] >= M.LO]
    one_catch = 100.0 * sum(1 for d in imp if d["arrested"]) / len(imp)
    tan = next(r for r in fig["rows"] if r["fips"] == "027")
    _, bt_ipw, bt_pool = B.backtest(obs)
    found = {}
    for cr in obs:
        if cr["fips"] != "027":
            continue
        for d in M.drivers(cr):
            if not d["killed"] and not d["complete"] and d["tested"] and d["bac"] >= M.LO:
                found[M.band(d["bac"])] = found.get(M.band(d["bac"]), 0) + 1
    missed_t = found.get(0, 0) * (1 / catch[0] - 1) + found.get(1, 0) * (1 / catch[1] - 1)
    scored = dict(call=sorted(r["county"] for r in high),
                  rates={r["county"]: round(float(r["rate"]), 2) for r in rows},
                  deaths={r["county"]: r["deaths"] for r in rows},
                  ask_a={r["county"]: {"arrests": r["arrests"], "pct15": round(float(r["pct15"]), 1)} for r in rows},
                  ask_b={r["county"]: r["crashes"] for r in rows})
    return dict(scored, rows=rows, high=[r["county"] for r in high],
                high_rates=[(r["county"], r["rate"]) for r in high],
                below_top=[r["county"] for r in top_below], below_top_rate=below[0]["rate"],
                catch_lo="%.1f" % (100 * catch[0]), catch_hi="%.1f" % (100 * catch[1]),
                weight_lo="%.1f" % (1 / catch[0]), weight_hi="%.3f" % (1 / catch[1]),
                rival_share=rival["R6"], share_pct="%.1f" % share, rival_one=rival["R8"],
                one_catch_pct="%.1f" % one_catch, bt_ipw="%.1f" % bt_ipw, bt_pool="%.1f" % bt_pool,
                tanager_found_lo=found.get(0, 0),
                tanager_found_hi=found.get(1, 0), tanager_missed="%.1f" % missed_t,
                tanager_rate=_r2(tan["rate"]), threshold="%.2f" % W.THRESHOLD, sections=DC.SECTIONS,
                window_days=DC.WINDOW_DAYS, leap_days=366, serum="%.2f" % L.SERUM)


def write_csv(path, f):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(CSV_COLS)
        for r in f["rows"]:
            w.writerow([r["fips"], r["county"], r["deaths"], r["vmt"], r["rate"], "Y" if r["high"] else "N",
                        r["arrests"], r["pct15"], r["crashes"]])


def _bar(d, x0, y0, w, h, fill):
    """A bar with a rounded data end and a square base on the axis."""
    r = min(2.2, h / 2.0)
    d.add(Rect(x0, y0, w, h, rx=r, ry=r, fillColor=fill, strokeColor=None))
    d.add(Rect(x0, y0, w, min(h, r + 0.5), fillColor=fill, strokeColor=None))


def chart(f, width=6.6 * inch, height=3.05 * inch):
    rows = sorted(f["rows"], key=lambda r: (-float(r["rate"]), r["county"]))
    below = [r for r in rows if not r["high"]]
    label = {r["county"] for r in rows if r["high"]} | {below[0]["county"]}
    d = Drawing(width, height)
    left, bottom, top = 34, 40, 30
    pw, ph = width - left - 8, height - bottom - top
    vmax = 0.80
    slot = pw / len(rows)
    bw = slot - 4.0
    for k in range(0, 9):
        v = k * 0.10
        y = bottom + ph * v / vmax
        d.add(Line(left, y, left + pw, y, strokeColor=GRID, strokeWidth=0.5))
        d.add(String(left - 5, y - 2.6, "%.1f" % v, fontName="LiberationSans", fontSize=6.6, fillColor=GREY,
                     textAnchor="end"))
    for i, r in enumerate(rows):
        v = float(r["rate"])
        x0 = left + i * slot + 2.0
        h = ph * v / vmax
        _bar(d, x0, bottom, bw, h, HIGH if r["high"] else LOW)
        if r["county"] in label and r["high"]:
            d.add(String(x0 + bw / 2, bottom + h + 3, r["rate"], fontName="LiberationSans-Bold", fontSize=6.8,
                         fillColor=INK, textAnchor="middle"))
        elif r["county"] in label:
            d.add(String(x0 + bw / 2, bottom + h - 9, r["rate"], fontName="LiberationSans-Bold", fontSize=6.8,
                         fillColor=colors.white, textAnchor="middle"))
        d.add(String(x0 + bw / 2, bottom - 9.5, r["county"], fontName="LiberationSans", fontSize=6.4,
                     fillColor=INK, textAnchor="middle"))
    y = bottom + ph * W.THRESHOLD / vmax
    d.add(Line(left, y, left + pw, y, strokeColor=INK, strokeWidth=1.0, strokeDashArray=[3, 2]))
    d.add(String(left + pw, y + 3.2, "High-range line, 0.60", fontName="LiberationSans-Bold", fontSize=6.8,
                 fillColor=INK, textAnchor="end"))
    d.add(String(0, height - 10, "Four counties at or above 0.60 alcohol-impaired-driving deaths per 100 million "
                 "vehicle miles, 2023 to 2025", fontName="LiberationSans-Bold", fontSize=8.2, fillColor=INK))
    d.add(String(0, height - 21, "Deaths per 100 million vehicle miles; labels on the high-range counties and the "
                 "nearest below the line", fontName="LiberationSans", fontSize=6.8, fillColor=GREY))
    d.add(Rect(left, 10, 8, 6, fillColor=HIGH, strokeColor=None))
    d.add(String(left + 11, 10.5, "High-range (0.60 or more)", fontName="LiberationSans", fontSize=6.6, fillColor=INK))
    d.add(Rect(left + 112, 10, 8, 6, fillColor=LOW, strokeColor=None))
    d.add(String(left + 123, 10.5, "Below 0.60", fontName="LiberationSans", fontSize=6.6, fillColor=INK))
    return d


def write_letter(path, f):
    body = ParagraphStyle("b", fontName="LiberationSerif", fontSize=10.4, leading=14.2, textColor=INK, spaceAfter=7)
    small = ParagraphStyle("s", fontName="LiberationSans", fontSize=7.8, leading=9.8, textColor=INK)
    smallr = ParagraphStyle("sr", parent=small, alignment=2)
    smallb = ParagraphStyle("sb", fontName="LiberationSans-Bold", fontSize=7.8, leading=9.8, textColor=INK)
    smallbr = ParagraphStyle("sbr", parent=smallb, alignment=2)
    head = ParagraphStyle("h", fontName="LiberationSans-Bold", fontSize=11.5, leading=14, textColor=MAROON)
    sub = ParagraphStyle("hs", fontName="LiberationSans", fontSize=8, leading=10.5, textColor=GREY)
    cap = ParagraphStyle("c", fontName="LiberationSans", fontSize=7.8, leading=10, textColor=GREY, spaceAfter=6)
    note = ParagraphStyle("n", fontName="LiberationSans", fontSize=7.6, leading=9.8, textColor=GREY, spaceAfter=4)
    coord, title = W.PEOPLE["coordinator"]
    ghso_name, ghso_title = W.PEOPLE["ghso"]
    hi = f["high_rates"]
    below = f["below_top"]
    sec = f["sections"]

    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.3)
        canvas.setFillColor(GREY)
        if doc.page > 1:
            canvas.drawString(0.95 * inch, letter[1] - 0.55 * inch, "%s, %s  |  14 April 2027" % (ghso_name, W.GHSO))
        canvas.drawRightString(letter[0] - 0.95 * inch, 0.55 * inch, "Page %d of 2" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.95 * inch, rightMargin=0.95 * inch,
                          topMargin=0.7 * inch, bottomMargin=0.8 * inch, title="FY2028 high-range certification",
                          author=W.CENTER, subject="", creator="", producer="")
    story = [Paragraph(W.UNIVERSITY.upper(), head),
             Paragraph("Center for Transportation Safety  |  410 Linden Hall, Kessington", sub), Spacer(1, 14),
             Paragraph("14 April 2027", body),
             Paragraph("%s<br/>%s<br/>%s" % (ghso_name, ghso_title, W.GHSO), body),
             Paragraph("<b>Re: Four counties certified high-range for the FY2028 County Impaired Driving Task Force "
                       "grants</b>", body),
             Paragraph("Dear %s," % ghso_name, body),
             Paragraph("Under section 2.1 of the FY2028 program guidelines, the Center certifies %s (%s alcohol-"
                       "impaired-driving fatalities per 100 million vehicle miles, 2023 to 2025), %s (%s), %s (%s) "
                       "and %s (%s) as high-range for FY2028. The other ten counties are below 0.60; the nearest is "
                       "%s, at %s." % (hi[0][0], hi[0][1], hi[1][0], hi[1][1], hi[2][0], hi[2][1], hi[3][0],
                                        hi[3][1], " and ".join(below), f["below_top_rate"]), body),
             Paragraph("Tanager is on the list because most of its surviving drivers were never tested. The State "
                       "Patrol and the Corwin and Ossian sheriffs draw blood from every surviving driver; the county "
                       "and city agencies draw it only after an arrest at the scene. Where every driver is tested, "
                       "officers arrested %s per cent of the drivers between .08 and .149 and %s per cent of those "
                       "at .15 or more, so each arrested driver found at .08 or more elsewhere stands for %s drivers "
                       "in the lower band and %s in the higher. Tanager's county and city agencies arrested %d such "
                       "drivers in the lower band and %d in the higher, which puts %s impaired surviving drivers "
                       "there untested." % (f["catch_lo"], f["catch_hi"], f["weight_lo"], f["weight_hi"],
                                            f["tanager_found_lo"], f["tanager_found_hi"], f["tanager_missed"]), body),
             Spacer(1, 4), chart(f),
             Paragraph("Figure 1. Each county's 2023 to 2025 rate against the 0.60 line (guidelines %s); Table 1 "
                       "gives every county's figures." % sec["rate"], cap),
             PageBreak()]
    hdr = ["County", "Deaths, 2023 to 2025", "Vehicle miles (100 million)", "Rate", "High-range",
           "Arrests with a blood specimen, 2025", "At .15 or more", "Injury crashes, drinking driver, 2025"]
    t = [[Paragraph(h, smallb if i == 0 else smallbr) for i, h in enumerate(hdr)]]
    for r in sorted(f["rows"], key=lambda r: r["county"]):
        vals = (r["county"], r["deaths"], r["vmt"], r["rate"], "Yes" if r["high"] else "No",
                format(r["arrests"], ","), r["pct15"] + "%", r["crashes"])
        t.append([Paragraph(str(v), small if i == 0 else smallr) for i, v in enumerate(vals)])
    tab = Table(t, colWidths=[0.8 * inch, 0.7 * inch, 0.84 * inch, 0.45 * inch, 0.7 * inch, 0.95 * inch,
                              0.6 * inch, 0.92 * inch], repeatRows=1, hAlign="LEFT")
    tab.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.7, INK), ("LINEBELOW", (0, -1), (-1, -1), 0.5, GREY),
                             ("VALIGN", (0, 0), (-1, 0), "BOTTOM"), ("VALIGN", (0, 1), (-1, -1), "TOP"),
                             ("TOPPADDING", (0, 0), (-1, -1), 1.8), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8)]))
    story += [Spacer(1, 6),
              Paragraph("<b>Table 1. Rates and 2025 baselines by county</b>", body), tab, Spacer(1, 4),
              Paragraph("Sources: Fatal Crash Census, 2023, 2024 and 2025 files; DOT county daily vehicle miles "
                        "2023 to 2025; State Toxicology Laboratory specimen extract of 12 March 2027; Crash Records "
                        "System extract of 8 March 2027.", note),
              Paragraph("Deaths are the number expected from the census records under guidelines %s, rounded to "
                        "whole deaths; each rate is computed from the unrounded count and compared with 0.60 before "
                        "rounding. Vehicle miles are the DOT's daily miles times 365 days, 366 in 2024." %
                        sec["estimand"], note), Spacer(1, 8),
              Paragraph("The baselines in Table 1 are the three section %s figures each task force application "
                        "states: the county's 2025 impaired-driving arrests with a blood specimen at the laboratory "
                        "and the per cent of them at .15 or more, and its 2025 injury crashes in which no one died "
                        "within %d days and an officer reported a driver had been drinking." % (
                            sec["baselines"], f["window_days"]), body),
              Paragraph("Sincerely,", body), Spacer(1, 16),
              Paragraph("%s<br/>%s, %s" % (coord, title, W.CENTER_SHORT), body),
              Paragraph("cc: %s, %s" % W.PEOPLE["records"], body)]
    d.build(story, onFirstPage=frame, onLaterPages=frame)


def main(target, gdir, fig_path, x):
    os.makedirs(gdir, exist_ok=True)
    f = figures(x)
    write_csv(os.path.join(gdir, W.GOLDEN["csv"]), f)
    write_letter(os.path.join(gdir, W.GOLDEN["letter"]), f)
    import postprocess as PP
    PP.normalize_pdf(os.path.join(gdir, W.GOLDEN["letter"]), b"D:20270414093512-05'00'", b"D:20270414101847-05'00'")
    with open(fig_path, "w", encoding="utf-8") as fh:
        json.dump(f, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return f
