"""The golden: every owed figure computed from the cut pack (methods.py), written to generator/figures.json, and the two
deliverables, tamsett_spring_patching_sections_2027.csv and tamsett_spring_patching_task_orders_2027.pdf."""
import csv
import io
import json
import os

import methods as M

HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = {403: "Carrow Point", 407: "Elmscourt", 411: "Rushmead", 402: "Fenwick Gap", 409: "Thistlebank",
         405: "Marlpit", 412: "Stonebeck", 414: "Pyke Hill", 401: "Holloway Run", 406: "Kestrelton",
         413: "Norvelle", 404: "Grisholt", 408: "Halverton", 410: "Oxbrae"}
ORDER = sorted(NAMES)
CSV_NAME = "tamsett_spring_patching_sections_2027.csv"
WORDS = {3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}
PDF_NAME = "tamsett_spring_patching_task_orders_2027.pdf"


def whole(x):
    """Half up, the prompt's whole number."""
    return int(x + 0.5)


def compute(target):
    import csv as _csv
    with open(os.path.join(target, "maintenance_sections.csv"), encoding="utf-8", newline="") as fh:
        for r in _csv.DictReader(fh):
            assert NAMES[int(r["section"])] == r["section_name"], r
    p = M.load(target)
    g = M.golden(p)
    fam = M.family(p, g)
    pp, pass_rate = M.per_pass(p, g)
    a_n, a_lb = M.ask_patches(p)
    miles = M.ask_miles(p)
    est = g["est"]
    des = sorted([s for s in ORDER if est[s] >= M.LINE], key=lambda s: (-est[s], s))
    below = max((s for s in ORDER if s not in des), key=lambda s: est[s])
    lowest_in = min(des, key=lambda s: est[s])
    # the repeat rate a unit's own later days show
    rep = repeat_rate(p, g)
    f = {
        "call": {"designated": [NAMES[s] for s in des], "count": len(des), "of": len(ORDER)},
        "line": M.LINE,
        "sections": {NAMES[s]: {"section": s, "lane_miles": round(g["lm"][s], 1), "rate": whole(est[s]),
                                "crew": "Yes" if s in des else "No", "cold_patched": a_n.get(s, 0),
                                "cold_mix_lb": a_lb.get(s, 0), "camera_miles": whole(miles.get(s, 0.0))}
                     for s in ORDER},
        "components": {"lane_miles": round(sum(g["lm"].values()), 1), "confirmed": len(g["pots"]),
                       "turned_back": len(p["turnback"]), "find_rate_pct": round(100 * g["q"], 1),
                       "miss_rate": round(1 - g["q"], 3), "repeat_pct": round(100 * rep, 1),
                       "highest_below": {"name": NAMES[below], "rate": whole(est[below])},
                       "lowest_in": {"name": NAMES[lowest_in], "rate": whole(est[lowest_in])}},
        "default": {"designated": [NAMES[s] for s in ORDER if pp[s] >= M.LINE], "pass_rate_pct": round(100 * pass_rate)},
        "_unrounded": {NAMES[s]: round(est[s], 4) for s in ORDER},
        "_family": {k: {NAMES[s]: round(v[s], 4) for s in ORDER} for k, v in fam.items() if not k.startswith("_")},
        "_rates": {"pairs": round(fam["_rates"]["pairs"], 5), "mle": round(fam["_rates"]["mle"], 5)},
    }
    return p, g, f


def repeat_rate(p, g):
    from collections import defaultdict
    u = M.units(p)
    by_veh = defaultdict(list)
    for unit, (veh, grp, inst, rem) in u.items():
        by_veh[veh].append((unit, inst, rem))
    passdays = defaultdict(set)
    for t in p["trav"]:
        seg = int(t["segment_id"])
        if seg not in g["road"]:
            continue
        day = M._utc(t["enter_utc"]).astimezone(M.TZ).date()
        if day.month != 3:
            continue
        for unit, inst, rem in by_veh.get(t["vehicle_id"], []):
            if day >= inst and (rem is None or day < rem):
                passdays[(seg, unit)].add(day.isoformat())
    dup = {int(r["Defect ID"]): int(str(r["Reason"]).split()[-1]) for r in p["qa"]
           if (r["Reason"] or "").startswith("Duplicate of ")}
    dd = defaultdict(set)
    for d in p["det"]:
        did = dup.get(int(d["defect_id"]), int(d["defect_id"]))
        if did in g["pots"]:
            dd[(did, d["unit_serial"])].add(d["captured_local"][:10])
    a = b = 0
    for (did, unit), ds in dd.items():
        seg = g["pots"][did][0]
        first = min(ds)
        later = [x for x in passdays[(seg, unit)] if x > first]
        b += len(later)
        a += sum(1 for x in later if x in ds)
    return a / b


def write_csv(path, f):
    cols = ["section", "section_name", "state_lane_miles", "potholes_per_10_lane_miles", "dedicated_crew",
            "cold_patched_potholes_mar", "cold_mix_lb_mar", "camera_miles_mar"]
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(cols)
    for name, x in sorted(f["sections"].items(), key=lambda kv: kv[1]["section"]):
        w.writerow([x["section"], name, "%.1f" % x["lane_miles"], x["rate"], x["crew"], x["cold_patched"],
                    x["cold_mix_lb"], x["camera_miles"]])
    open(path, "w", encoding="utf-8", newline="").write(buf.getvalue())


def write_pdf(path, f):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.graphics.shapes import Drawing, Line, Rect, String
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    ink, ink2 = colors.HexColor("#0b0b0b"), colors.HexColor("#52514e")
    body = ParagraphStyle("b", fontName="Helvetica", fontSize=9.4, leading=12.4, spaceAfter=5, textColor=ink)
    note = ParagraphStyle("n", fontName="Helvetica", fontSize=7.6, leading=9.6, spaceAfter=3, textColor=ink2)
    head = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10.2, leading=13, spaceBefore=7, spaceAfter=3, textColor=ink)
    title = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=13.5, leading=16.5, spaceBefore=6, spaceAfter=5, textColor=ink)
    org = "Tamsett District Maintenance"
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.8 * inch, rightMargin=0.8 * inch, topMargin=0.65 * inch,
                            bottomMargin=0.7 * inch, title="Spring Patching Program 2027: designated sections and March close-out",
                            author=org, creator=org, producer=org, subject="Spring Patching Program 2027")

    def frame(c, d_):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.setFillColor(ink2)
        c.drawString(0.8 * inch, 0.45 * inch, "Tamsett District Maintenance | Spring Patching Program 2027 | internal")
        c.drawRightString(letter[0] - 0.8 * inch, 0.45 * inch, "Page %d" % d_.page)
        c.restoreState()

    secs = sorted(f["sections"].items(), key=lambda kv: (-f["_unrounded"][kv[0]], kv[1]["section"]))
    des = f["call"]["designated"]
    c = f["components"]
    # the chart: one bar per section, the program's line, the designated sections in blue
    W, H = 6.9 * inch, 3.05 * inch
    d = Drawing(W, H)
    left, bottom, top = 1.05 * inch, 0.42 * inch, H - 0.3 * inch
    scale = (W - left - 0.3 * inch) / 10.0
    bh = (top - bottom) / len(secs)
    blue, amber = colors.HexColor("#256abf"), colors.HexColor("#eda100")
    d.add(String(0, H - 0.12 * inch, "March 2027 potholes per ten lane-miles of state roadway, by section",
                 fontName="Helvetica-Bold", fontSize=8.4, fillColor=ink))
    for t in range(0, 11, 2):
        d.add(Line(left + t * scale, bottom, left + t * scale, top, strokeColor=colors.HexColor("#e6e5e0"), strokeWidth=0.5))
    for i, (name, x) in enumerate(secs):
        y = top - (i + 1) * bh + bh * 0.2
        v = f["_unrounded"][name]
        d.add(Rect(left, y, v * scale, bh * 0.6, fillColor=blue if name in des else amber, strokeColor=None))
        d.add(String(left - 5, y + bh * 0.14, "%s %d" % (name, x["section"]), fontName="Helvetica", fontSize=7.3,
                     textAnchor="end", fillColor=ink))
        d.add(String(left + v * scale + 4, y + bh * 0.14, "%d" % x["rate"], fontName="Helvetica-Bold", fontSize=7.3,
                     fillColor=ink))
    xl = left + f["line"] * scale
    d.add(Line(xl, bottom - 2, xl, top + 3, strokeColor=ink, strokeWidth=0.9, strokeDashArray=[3, 2]))
    d.add(String(xl + 3, top + 4, "program line, %.1f" % f["line"], fontName="Helvetica", fontSize=7, fillColor=ink))
    for t in range(0, 11, 2):
        d.add(String(left + t * scale, bottom - 10, str(t), fontName="Helvetica", fontSize=7, textAnchor="middle",
                     fillColor=ink2))
    d.add(Line(left, bottom, left + 10 * scale, bottom, strokeColor=ink2, strokeWidth=0.5))
    d.add(String(left + 5 * scale, bottom - 21, "potholes per ten lane-miles (bar labels to the whole number)",
                 fontName="Helvetica", fontSize=7, textAnchor="middle", fillColor=ink2))
    lx = W - 1.95 * inch
    d.add(Rect(lx, bottom + 0.3 * inch, 8, 8, fillColor=blue, strokeColor=None))
    d.add(String(lx + 12, bottom + 0.3 * inch + 1, "dedicated crew", fontName="Helvetica", fontSize=7, fillColor=ink))
    d.add(Rect(lx, bottom + 0.12 * inch, 8, 8, fillColor=amber, strokeColor=None))
    d.add(String(lx + 12, bottom + 0.12 * inch + 1, "section crews and shared crew", fontName="Helvetica", fontSize=7,
                 fillColor=ink))

    rows = [["Section", "Lane-miles", "Potholes per\nten lane-miles", "Dedicated\ncrew", "Cold patched\nin March",
             "Cold mix\n(lb)", "Camera miles,\nMarch"]]
    ordered = sorted(f["sections"].items(), key=lambda kv: kv[1]["section"])
    for name, x in ordered:
        rows.append(["%d %s" % (x["section"], name), "{:,.1f}".format(x["lane_miles"]), str(x["rate"]), x["crew"],
                     str(x["cold_patched"]), "{:,}".format(x["cold_mix_lb"]), "{:,}".format(x["camera_miles"])])
    t = Table(rows, colWidths=[1.5 * inch, 0.78 * inch, 0.95 * inch, 0.72 * inch, 0.86 * inch, 0.74 * inch, 0.95 * inch],
              repeatRows=1)
    st = [("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 7.4), ("FONT", (0, 1), (-1, -1), "Helvetica", 7.6),
          ("TEXTCOLOR", (0, 0), (-1, -1), ink), ("ALIGN", (1, 0), (-1, -1), "RIGHT"), ("ALIGN", (3, 1), (3, -1), "CENTER"),
          ("LINEBELOW", (0, 0), (-1, 0), 0.6, ink), ("VALIGN", (0, 0), (-1, 0), "BOTTOM"),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8), ("TOPPADDING", (0, 0), (-1, -1), 1.8)]
    for i, (name, x) in enumerate(ordered, 1):
        if x["crew"] == "Yes":
            st.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#e9f0f9")))
    t.setStyle(TableStyle(st))
    memo = Table([["To:", "Nancy Hansen, P.E., District Maintenance Engineer"],
                  ["From:", "Andrew Greene, Maintenance Management Systems"],
                  ["Date:", "12 April 2027"],
                  ["Subject:", "Spring Patching Program 2027: designated sections and the March close-out"],
                  ["Reference:", "On-call pavement repair contract 26-OC-1187, task orders of 19 April 2027"]],
                 colWidths=[0.85 * inch, 5.9 * inch], hAlign="LEFT")
    memo.setStyle(TableStyle([("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8.6), ("FONT", (1, 0), (1, -1), "Helvetica", 8.6),
                              ("TEXTCOLOR", (0, 0), (-1, -1), ink), ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                              ("TOPPADDING", (0, 0), (-1, -1), 1), ("LINEBELOW", (0, -1), (-1, -1), 0.6, ink)]))
    names = ", ".join(des[:-1]) + " and " + des[-1]
    story = [
        Paragraph("TAMSETT DISTRICT MAINTENANCE: MEMORANDUM", ParagraphStyle("o", fontName="Helvetica-Bold", fontSize=8,
                                                                          textColor=ink2, spaceAfter=4)),
        memo,
        Paragraph("Seven sections get a dedicated spring patching crew", title),
        Paragraph("<b>%s get the dedicated crews.</b> Each held 6.0 or more potholes per ten lane-miles of state roadway "
                  "in March, counting the potholes no camera unit recorded; of the other seven, %s comes closest at %d. "
                  "The task orders can issue on 19 April as drafted for these seven." % (names, c["highest_below"]["name"],
                                                                                        c["highest_below"]["rate"]), body),
        d,
        Paragraph("Bars at the unrounded estimate; Holloway Run, Kestrelton, Norvelle, Fenwick Gap and Thistlebank are "
                  "on the list only because the count includes the potholes no unit recorded.", note),
        Paragraph("How the March count was made", head),
        Paragraph("The program counts every pothole on a section's roadway, recorded or not (program 2.2), and Kerbline's "
                  "list is not every defect on the roads the units drove (scope of work 3). The question is how much the "
                  "list misses, and the units' own records answer it. A unit that recorded a pothole recorded it again on "
                  "%.1f per cent of its later days on that segment, so its repeat passes add nothing: whatever it missed on "
                  "the first pass it kept missing. Another unit driving the same segment found it %.1f per cent of the "
                  "time. The chances that matter are therefore the distinct units that drove a segment, not the passes, "
                  "and each confirmed pothole stands for one over the chance that at least one of those units found it, "
                  "one minus %.3f raised to the number of units." % (c["repeat_pct"], c["find_rate_pct"], c["miss_rate"]),
                  body),
        Paragraph("Metro segments see the section patrol, the freeway service patrol or the sweepers and a crew truck now "
                  "and then, and their lists are close to complete. The rural and outer suburban roads are driven every "
                  "week by their own patrol pickup and little else, so close to half their potholes are on no list. "
                  "Counted pass by pass, as if each pass were a fresh look, only Carrow Point and Elmscourt clear the line.",
                  body),
        Paragraph("Inputs: {:,.1f} lane-miles of state roadway as at 31 March<super>1</super> and {:,} potholes the review "
                  "queue confirmed on it, after folding the reviewer's duplicates.".format(c["lane_miles"], c["confirmed"]),
                  body),
        Paragraph("Sections", head),
        t,
        Paragraph("Source: Kerbline detections and review export (2 April), fleet telematics traversals, 2026 road inventory, "
                  "MMS work orders (PCOLD). Cold patched counts a pothole once even where the crew came back to it, "
                  "including the potholes whose first order carries the number Kerbline used before its 17 March "
                  "renumbering; cold mix counts a mobile-app order's pounds once rather than on every line; camera miles "
                  "count each March pass by an installed unit at the segment's inventory length, without the telematics "
                  "provider's re-run of 12 to 13 March.", note),
        Spacer(1, 6),
        Paragraph("<super>1</super> Program 2.4. The five SR 11 segments in Elmscourt that passed to the City on 15 March "
                  "(route turnback notice of 1 March) are not state roadway at 31 March and are left out, potholes and "
                  "lane-miles alike.", note),
    ]
    doc.build(story, onFirstPage=frame, onLaterPages=frame)
    import postprocess as PP
    PP.normalize_pdf(path, b"D:20270412164012-04'00'", b"D:20270412164012-04'00'")


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    p, g, f = compute(target)
    json.dump(f, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    out = os.path.join(os.path.dirname(HERE), "golden")
    os.makedirs(out, exist_ok=True)
    write_csv(os.path.join(out, CSV_NAME), f)
    write_pdf(os.path.join(out, PDF_NAME), f)
    return f


if __name__ == "__main__":
    import sys
    f = main(sys.argv[1] if len(sys.argv) > 1 else None)
    print(json.dumps({k: v for k, v in f.items() if not k.startswith("_")}, indent=1)[:3000])
