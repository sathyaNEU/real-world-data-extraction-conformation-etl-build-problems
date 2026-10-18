"""The golden: computed from the shipped pack alone (bundle.py reads it), then written as the workbook and the
committee note, with figures.json and submission.md emitted from the same objects."""
import csv
import io
import json
import math
import os
import re
from datetime import date, datetime, timedelta

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                   # noqa: E402
import numpy as np                                                # noqa: E402
import openpyxl                                                   # noqa: E402
from openpyxl import Workbook                                     # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill          # noqa: E402

import analysis as A                                              # noqa: E402
import docs as DOCS                                               # noqa: E402
import bundle as B                                                # noqa: E402
import names as N                                                 # noqa: E402
import postprocess as PP                                          # noqa: E402

GOLDEN = ("wkwe", "hour", "flagT", "ols")
CW_NAME = {"CW1": "Tolland Road", "CW2": "Brickfields", "CW3": "Estuary Path", "CW4": "Wardle Park",
           "CW5": "Market Street", "CW6": "Southfield"}
DT_WORDS = {"wk_term": "school-term weekdays", "wk_hol": "school-holiday weekdays", "we": "weekends and bank holidays"}
F_XLSX = "cycleway_widening_2027.xlsx"
F_NOTE = "widening_note_2027.pdf"


def r1(x):
    return float("%.1f" % (math.floor(x * 10 + 0.5) / 10.0))


# ---------------------------------------------------------------------------------------------- the main call
def main_call(P):
    fl, days, dts, wx, caps, cws = P["flows"], P["days"], P["dts"], P["weather"], P["caps"], P["cycleways"]
    fam = {}
    for m in A.FAMILY:
        fam[m] = A.golden(fl, days, dts, wx, caps, cws, *m)[0]
    res, G, sc = A.golden(fl, days, dts, wx, caps, cws, *GOLDEN)
    winner = max(res, key=res.get)
    assert all(max(v, key=v.get) == winner for v in fam.values()), "the family splits"
    seginfo = {s["segment_ref"]: s for s in P["inventory"]}
    per_seg = {}
    for cw, segs in cws.items():
        for s in segs:
            per_seg[s] = np.mean([A.crowded_by_counter(sc, caps, [s], y)[s] for y in A.YEARS])
    bind = max(cws[winner], key=lambda s: per_seg[s])
    cells = {}
    for y in A.YEARS:
        a = sc[bind][y]
        for i, d in enumerate(days[y]):
            for h in A.H_WINDOW:
                if a[i, h] > caps[bind]:
                    cells[(dts[y][i], h)] = cells.get((dts[y][i], h), 0) + 1
    hours = sorted({h for (t, h) in cells})
    dts_hit = sorted({t for (t, h) in cells}, key=lambda t: -sum(v for (tt, h), v in cells.items() if tt == t))
    # record facts about the binding segment and the summers' weather
    term8 = [fl[bind][2026][i, 8] for i, t in enumerate(dts[2026]) if t == "wk_term" and not np.isnan(fl[bind][2026][i, 8])]
    tot = {y: np.nansum(fl[bind][y]) for y in A.YEARS}
    wsum = {}
    for y in A.YEARS:
        tm = [wx[d][0] for d in days[y] if d in wx]
        wet = [wx[d][1] >= 1.0 for d in days[y] if d in wx]
        wsum[y] = (float(np.mean(tm)), 100.0 * float(np.mean(wet)), len(tm))
    growth_cell = {m: None for m in A.FAMILY}
    for m in A.FAMILY:
        Gm = A.cell_growth(fl, days, dts, wx, m[0], m[1], m[2], m[3])
        key = ("wk", 8) if m[0] == "wkwe" else ("wk_term", 8)
        growth_cell[m] = Gm[bind][key]
    return dict(res=res, fam=fam, G=G, sc=sc, winner=winner, per_seg=per_seg, bind=bind, cells=cells, hours=hours,
                dts_hit=dts_hit, seg=seginfo[bind], cap=caps[bind], term8_mean=float(np.mean(term8)), n_term8=len(term8),
                total_growth_2526=float(tot[2026] / tot[2025]), wsum=wsum, growth_cell=growth_cell,
                growth_golden=G[bind][("wk", 8)])


# ---------------------------------------------------------------------------------------------- ask A: the count week
LAPTOP_CLOCK = ("CVC-1112", "CVC-1207")     # restarted from a laptop on local time (17 March, 21 April), reset 29 May


def read_count_week(target, ep1_local=True, end_labels=True):
    """counter -> {local quarter start: riders both directions}"""
    out = {}
    with open(os.path.join(target, "count_week_15min_2026-05-11_15.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            ts = datetime.strptime(r["timestamp_utc"], "%Y-%m-%dT%H:%M:%SZ")
            if r["counter_id"] in LAPTOP_CLOCK and ep1_local:
                local = ts
            else:
                local = ts + timedelta(hours=1)
            start = local - timedelta(minutes=15) if end_labels else local
            d = out.setdefault(r["counter_id"], {})
            d[start] = d.get(start, 0) + int(r["count"])
    return out


def read_volunteers(target):
    wb = openpyxl.load_workbook(os.path.join(target, "volunteer_count_may2026.xlsx"), read_only=True)
    sheets = {}
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        cid = re.search(r"(CVC-\d{4})", rows[1][1]).group(1)
        day = datetime.strptime(rows[2][1], "%A %d %B %Y").date()
        recs = []
        for r in rows:
            if r[0] and re.match(r"^\d\d:\d\d-\d\d:\d\d$", str(r[0])):
                a, b = r[0].split("-")
                s = datetime.combine(day, datetime.strptime(a, "%H:%M").time())
                e = datetime.combine(day, datetime.strptime(b, "%H:%M").time())
                recs.append((s, e, int(r[1]), int(r[2]), int(r[3])))
        sheets[cid] = dict(tab=ws.title, day=day, rows=recs)
    return sheets


def ask_a(target, ep1_local=True, end_labels=True, road=False, drop_gap=True):
    cw = read_count_week(target, ep1_local, end_labels)
    vs = read_volunteers(target)
    out = {}
    for cid, v in vs.items():
        cnt = cw[cid]
        C = V = 0
        n = 0
        for s, e, vi, vo, rd in v["rows"]:
            qs = []
            t = s
            while t < e:
                qs.append(t)
                t += timedelta(minutes=15)
            have = all(q in cnt for q in qs)
            if not have and drop_gap:
                continue
            C += sum(cnt.get(q, 0) for q in qs)
            V += vi + vo + (rd if road else 0)
            n += len(qs)
        out[cid] = dict(C=C, V=V, short=100.0 * (V - C) / V, quarters=n, tab=v["tab"], day=v["day"])
    return out


# ---------------------------------------------------------------------------------------------- ask B: the log
def parse_downtime(s, contractor):
    if not s:
        return None
    if ":" in s:
        h, m = s.split(":")
        return int(h) * 60 + int(m)
    return int(s) if contractor else int(round(float(s) * 60))


def read_log(target):
    with open(os.path.join(target, "counter_maintenance_log_2024-2026.csv"), newline="") as fh:
        return list(csv.DictReader(fh))


def _ldt(s):
    return datetime.strptime(s, "%d/%m/%Y %H:%M")


def minutes_in_year(a, b, y):
    lo, hi = datetime(y, 1, 1), datetime(y + 1, 1, 1)
    a2, b2 = max(a, lo), min(b, hi)
    if a2 >= b2:
        return 0
    return B_elapsed(a2, b2)


def B_elapsed(a, b):
    from zoneinfo import ZoneInfo
    L = ZoneInfo("Europe/London")
    return int(round((b.replace(tzinfo=L).timestamp() - a.replace(tzinfo=L).timestamp()) / 60))


def stoppages(target, P=None):
    """every spell a dashboard counter recorded nothing, from the log: (counter, start, end, minutes logged)"""
    rows = read_log(target)
    reg = B.read_register(target)
    dash = {r["counter_id"]: r for r in reg if r["type"] == "dashboard"}
    site_to_cid = {}
    for r in reg:
        if r["type"] == "dashboard" and not r["unit_of_record_to"]:
            site_to_cid[r["legacy_site_name"]] = r["counter_id"]
    by_job = {r["job_no"]: r for r in rows}
    out = []
    for r in rows:
        cid = site_to_cid.get(r["site"])
        if cid is None:
            continue
        con = r["logged_by"] != "Traffic Monitoring Unit"
        m = parse_downtime(r["downtime"], con)
        if m is None:
            continue
        if r["parent_job"]:
            par = by_job[r["parent_job"]]
            if r["downtime"] == par["downtime"]:
                continue                     # a visit that checked the repair: the parent's downtime written again
        a, b = _ldt(r["reported"]), _ldt(r["closed"])
        assert B_elapsed(a, b) == m, (r["job_no"], B_elapsed(a, b), m)
        out.append(dict(cid=cid, a=a, b=b, minutes=m, job=r["job_no"]))
    # the contractor's job for a fault lies inside the unit's job for the same stoppage: one stoppage, the union
    merged = []
    for cid in sorted({s["cid"] for s in out}):
        sp = sorted([s for s in out if s["cid"] == cid], key=lambda s: s["a"])
        cur = None
        for s in sp:
            if cur and s["a"] <= cur["b"]:
                cur["b"] = max(cur["b"], s["b"])
                cur["jobs"].append(s["job"])
            else:
                cur = dict(cid=cid, a=s["a"], b=s["b"], jobs=[s["job"]])
                merged.append(cur)
    return merged


def ask_b(target, year=2025):
    st = stoppages(target)
    reg = B.read_register(target)
    cids = sorted({r["counter_id"] for r in reg if r["type"] == "dashboard" and not r["unit_of_record_to"]})
    out = {c: dict(minutes=0, n=0) for c in cids}
    for s in st:
        m = minutes_in_year(s["a"], s["b"], year)
        if m > 0:
            out[s["cid"]]["minutes"] += m
            out[s["cid"]]["n"] += 1
    for c in out:
        out[c]["hours"] = out[c]["minutes"] / 60.0
    return out


# ---------------------------------------------------------------------------------------------- the workbook
HEAD = PatternFill("solid", fgColor="DDE7F0")
PICK = PatternFill("solid", fgColor="FCE9C8")


def _hdr(ws, row, labels, widths=None):
    for j, t in enumerate(labels, 1):
        c = ws.cell(row=row, column=j, value=t)
        c.font = Font(bold=True)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")
    if widths:
        for j, w in enumerate(widths, 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w


def workbook(g, path):
    mc, aa, bb, P = g["main"], g["ask_a"], g["ask_b"], g["P"]
    seg = mc["seg"]
    wb = Workbook()
    ws = wb.active
    ws.title = "Recommendation"
    ws["A1"] = "Widen Tolland Road: Tolland Bridge crowds between 08:00 and 09:00 on weekday mornings"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Cycleway Capacity Fund 2026-27, forecast for 1 June to 31 August 2027 (AT-POL-07)"
    ws["A2"].font = Font(italic=True, color="555555")
    rows = [("Cycleway to widen", "%s (%s)" % (CW_NAME[mc["winner"]], mc["winner"])),
            ("Segment that crowds it", "%s (%s), %.1f m at its narrowest, %d cyclists an hour both ways" % (
                seg["segment_name"], mc["bind"], float(seg["min_width_m"]), mc["cap"])),
            ("Hours it crowds", "08:00 to 09:00 on weekday mornings, %d of its %d crowded mornings in school term" % (
                mc["cells"].get(("wk_term", 8), 0), sum(mc["cells"].values())))]
    for i, (k, v) in enumerate(rows, 4):
        ws.cell(row=i, column=1, value=k).font = Font(bold=True)
        ws.cell(row=i, column=2, value=v)
    _hdr(ws, 8, ["Cycleway", "Name", "Forecast crowded days, summer 2027", "Segment that crowds it", "Capacity (cyclists an hour)",
                 "Hour it crowds most often"], [12, 18, 18, 32, 14, 30])
    order = sorted(mc["res"], key=lambda c: -mc["res"][c])
    seginv = {s["segment_ref"]: s for s in P["inventory"]}
    r = 9
    for cw in order:
        segs = P["cycleways"][cw]
        b = max(segs, key=lambda s: mc["per_seg"][s])
        hit = mc["per_seg"][b] > 0
        cells = {}
        if hit:
            for y in A.YEARS:
                a = mc["sc"][b][y]
                for i, d in enumerate(P["days"][y]):
                    for h in A.H_WINDOW:
                        if a[i, h] > P["caps"][b]:
                            k = ("weekend" if P["dts"][y][i] == "we" else "weekday", h)
                            cells[k] = cells.get(k, 0) + 1
        hh = max(cells, key=cells.get) if cells else None
        vals = [cw, CW_NAME[cw], round(mc["res"][cw]), "%s (%s)" % (seginv[b]["segment_name"], b) if hit else "none",
                P["caps"][b] if hit else None,
                ("%s %02d:00 to %02d:00" % (hh[0], hh[1], hh[1] + 1)) if hh is not None else ""]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=r, column=j, value=v)
            if cw == mc["winner"]:
                c.fill = PICK
        r += 1
    ws.cell(row=r + 1, column=1, value="Forecast crowded days are the mean over the summers of 2024, 2025 and 2026 replayed at "
                                       "2027 numbers (policy 3.4); a day counts once however many hours or segments crowd.")
    ws.cell(row=r + 1, column=1).font = Font(italic=True, size=9, color="555555")
    ws.freeze_panes = "A9"

    w2 = wb.create_sheet("Growth by segment")
    _hdr(w2, 1, ["Segment", "Name", "Cycleway", "Capacity", "Day group", "Hour", "Growth a year, weather held fixed",
                 "Forecast crowded days (mean of three summers)"], [11, 30, 10, 10, 12, 8, 18, 18])
    r = 2
    for cw in sorted(P["cycleways"]):
        for s in P["cycleways"][cw]:
            best = max(((g_, h) for g_ in ("wk", "we") for h in A.H_WINDOW),
                       key=lambda k: np.nanmean([np.nanmean(mc["sc"][s][y][[i for i, (d, t) in enumerate(zip(P["days"][y], P["dts"][y]))
                                                                              if A.daygroup(d, t, "wkwe") == k[0]], k[1]])
                                                 for y in A.YEARS]))
            vals = [s, seginv[s]["segment_name"], cw, P["caps"][s], "weekdays" if best[0] == "wk" else "weekends",
                    "%02d:00" % best[1], mc["G"][s][best], round(mc["per_seg"][s], 1)]
            for j, v in enumerate(vals, 1):
                c = w2.cell(row=r, column=j, value=v)
                if j == 7:
                    c.number_format = "0.000"
                if s == mc["bind"]:
                    c.fill = PICK
            r += 1
    w2.cell(row=r + 1, column=1, value="Growth is each counter's own, for its busiest hour and day group, from a log-linear fit "
                                       "on the three summers with a wet-day flag (1.0 mm or more) and the day's maximum temperature.")
    w2.cell(row=r + 1, column=1).font = Font(italic=True, size=9, color="555555")
    w2.freeze_panes = "A2"

    w3 = wb.create_sheet("Volunteer count check")
    _hdr(w3, 1, ["Site", "Counter", "Count day", "Quarter hours compared", "Riders the counter recorded",
                 "Volunteers' riders on the track", "Counter shortfall (% of volunteers' count)"], [26, 10, 14, 12, 16, 16, 18])
    r = 2
    for cid in sorted(aa, key=lambda c: (aa[c]["day"], c)):
        v = aa[cid]
        site = [x for x in P["register"] if x["counter_id"] == cid][0]["legacy_site_name"]
        for j, val in enumerate([site, cid, v["day"].strftime("%d %b %Y"), v["quarters"], v["C"], v["V"], r1(v["short"])], 1):
            c = w3.cell(row=r, column=j, value=val)
            if j in (5, 6):
                c.number_format = "#,##0"
            if j == 7:
                c.number_format = "0.0"
        r += 1
    notes3 = ["Intervals compared: the quarter hours both the volunteers and the counter recorded in 07:00 to 10:00 and 16:00 "
              "to 19:00 on each site's count day. The interval export stamps each quarter at its end; the Quayside (CVC-1112) "
              "and Corn Exchange (CVC-1207) loggers kept local time from their laptop restarts on 17 March and 21 April 2026 "
              "to the summer round clock reset on 29 May 2026.",
              "Station Sq: the logger kept nothing from 16:00 to 17:00 on 13 May (manual download), so that hour is left out "
              "on both sides. Road riders are not in the volunteers' track count."]
    for k, t in enumerate(notes3):
        w3.cell(row=r + 1 + k, column=1, value=t).font = Font(italic=True, size=9, color="555555")
    w3.freeze_panes = "A2"

    w4 = wb.create_sheet("Counter downtime 2025")
    _hdr(w4, 1, ["Counter", "Site", "Hours recording nothing in 2025", "Separate stoppages"], [11, 30, 16, 12])
    r = 2
    for cid in sorted(bb):
        site = [x for x in P["register"] if x["counter_id"] == cid][0]["legacy_site_name"]
        for j, val in enumerate([cid, site, r1(bb[cid]["hours"]), bb[cid]["n"]], 1):
            c = w4.cell(row=r, column=j, value=val)
            if j == 3:
                c.number_format = "0.0"
        r += 1
    notes4 = ["From the maintenance log: each stoppage's real time from report to close, the part inside 2025 (local time). "
              "Follow-up visits that only checked a repair repeat their job's downtime and are not stoppages; a visit that "
              "found the counter down again is. The contractor's job for a fault falls inside the unit's job for the same "
              "stoppage and is counted once. Contractor downtime is in minutes, the unit's in hours and minutes.",
              "Corn Exchange includes the February 2025 fault on the old unit CVC-0388; Station Sq includes the 28 May battery "
              "job keyed to asset CVC-1180."]
    for k, t in enumerate(notes4):
        w4.cell(row=r + 1 + k, column=1, value=t).font = Font(italic=True, size=9, color="555555")
    w4.freeze_panes = "A2"

    w5 = wb.create_sheet("Notes")
    w5.column_dimensions["A"].width = 120
    notes = ["Sources: counter exports (legacy archive for summer 2024, platform for 2025 and 2026), counter register, Path "
             "Inventory, Cycle Design Guide Table 4.3, weather station CVM-WX1, published term dates, maintenance log, count "
             "week interval export and the Cycle Forum's sheets.",
             "Counts: both directions, local clock hours; platform hours converted from UTC; hours not recorded (no_data, "
             "estimated, legacy blanks) left out, never counted as crowded.",
             "Growth: for each counter and each weekday or weekend hour, a log-linear fit of the hour's riders on year, a "
             "wet-day flag and the day's maximum temperature over the three summers; each recorded day is carried to 2027 "
             "at its own hour's growth and keeps its own weather and calendar.",
             "Crowded: any hour from 06:00 to 22:00 above the segment's Table 4.3 capacity on any counted segment (policy 3.3)."]
    for i, t in enumerate(notes, 1):
        w5.cell(row=i, column=1, value=t).alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    PP.normalize_ooxml(path, N.PEOPLE["atl"][0], N.PEOPLE["atl"][0], "2026-10-12T08:40:00Z", "2026-10-12T15:25:00Z",
                       excel=True, company=N.COUNCIL)


# ---------------------------------------------------------------------------------------------- chart and note
def chart_png(mc):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "svg.hashsalt": "task169"})
    fig, ax = plt.subplots(figsize=(6.2, 2.6), dpi=150)
    order = sorted(mc["res"], key=lambda c: -mc["res"][c])
    vals = [mc["res"][c] for c in order]
    cols = ["#c8641e" if c == mc["winner"] else "#8fa7bd" for c in order]
    bars = ax.barh([CW_NAME[c] for c in order][::-1], vals[::-1], color=cols[::-1], zorder=2)
    for b_, v in zip(bars, vals[::-1]):
        ax.text(v + 0.6, b_.get_y() + b_.get_height() / 2, "%d" % round(v), va="center", fontsize=7.5, color="#333333")
    ax.set_xlabel("Forecast crowded days, 1 June to 31 August 2027 (of 92)", color="#444444")
    ax.set_xlim(0, max(vals) * 1.18)
    ax.grid(axis="x", color="#e3e3e3", linewidth=0.6, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title("Tolland Road crowds on the most days next summer", fontsize=9, loc="left")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def note(g, path):
    """the one-page committee note, as the committee pack carries it (PDF), written with reportlab and re-serialised
    through pypdf with the officer as author and the note's date (H1, H25)"""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    mc = g["main"]
    seg = mc["seg"]
    base = ParagraphStyle("b", fontName="Helvetica", fontSize=9.8, leading=13.2, spaceAfter=5)
    small = ParagraphStyle("s", parent=base, fontSize=7.8, leading=10, textColor=colors.HexColor("#555555"))
    head = ParagraphStyle("h", parent=base, fontName="Helvetica-Bold", fontSize=10.2, textColor=colors.HexColor("#1F4E79"),
                          spaceBefore=4, spaceAfter=2)
    title = ParagraphStyle("t", parent=base, fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    bold = ParagraphStyle("bb", parent=base, fontName="Helvetica-Bold")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=21 * mm, rightMargin=21 * mm, topMargin=15 * mm,
                            bottomMargin=14 * mm, title="Cycleway widening 2026-27", author=N.PEOPLE["atl"][0],
                            creator=N.COUNCIL, producer=N.COUNCIL, invariant=1)
    s = []
    s.append(Paragraph(N.COUNCIL, ParagraphStyle("o", parent=small, fontName="Helvetica-Bold",
                                                 textColor=colors.HexColor("#1F4E79"), fontSize=8.6)))
    s.append(Paragraph("Transport and Environment Committee, 26 October 2026", title))
    meta = [["Subject", "Cycleway Capacity Fund 2026-27: the widening to build before summer 2027"],
            ["From", "%s, %s" % N.PEOPLE["atl"]], ["Date", "12 October 2026"]]
    t = Table(meta, colWidths=[22 * mm, 140 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([("FONT", (0, 0), (0, -1), "Helvetica-Bold", 9.4), ("FONT", (1, 0), (1, -1), "Helvetica", 9.4),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                           ("TOPPADDING", (0, 0), (-1, -1), 1)]))
    s.append(t)
    s.append(Spacer(1, 6))
    s.append(Paragraph("Recommendation", head))
    s.append(Paragraph("That the committee allocate the 2026-27 widening to Tolland Road (CW1), at Tolland Bridge, where the "
                       "cycleway crowds between 08:00 and 09:00 on weekday mornings.", bold))
    s.append(Paragraph("Why Tolland Road", head))
    s.append(Paragraph(
        "Tolland Bridge is %.1f m wide at its narrowest, which the Cycle Design Guide rates at %d cyclists an hour in both "
        "directions. It overflows in one hour, 08:00 to 09:00 on weekday mornings, and that hour is commuting traffic, the "
        "fastest-growing riding we count: with each day's weather held fixed, the bridge's 08:00 weekday flow has grown by "
        "about %d per cent a year over the last three summers, faster than the bridge's daily total, half of which is "
        "midday riding that is flat or falling. Replaying the summers of 2024 to 2026 at 2027 numbers, as AT-POL-07 sets "
        "out, Tolland Road is crowded on about %d of next summer's 92 days, more than any other cycleway (Brickfields, "
        "next, about %d)." % (float(seg["min_width_m"]), mc["cap"], round(100 * (mc["growth_golden"] - 1)),
                               round(mc["res"]["CW1"]), round(mc["res"]["CW2"])), base))
    s.append(Paragraph(
        "Estuary Path looks busiest if last year's rise in each counter's total is carried forward, but that rise came "
        "with the hot, dry summer of 2026 (a mean daily maximum of %.1f C and rain on %d per cent of days, against %.1f C "
        "and %d per cent in 2024). Leisure riding on the path follows the weather and, once the weather is held fixed, "
        "has been easing back. Market Street comes out first only if each cycleway's dashboard counter stands for all of "
        "its segments." % (mc["wsum"][2026][0], round(mc["wsum"][2026][1]), mc["wsum"][2024][0],
                           round(mc["wsum"][2024][1])), base))
    img = Image(io.BytesIO(chart_png(mc)), width=160 * mm, height=160 * mm * 2.6 / 6.2)
    s.append(img)
    s.append(Paragraph("Counter checks", head))
    s.append(Paragraph("The Cycle Forum's May 2026 count and the 2025 maintenance log are summarised in "
                       "cycleway_widening_2027.xlsx, with the forecast by segment.", base))
    s.append(Paragraph("Forecast from the council's counters (legacy archive 2024, counter platform 2025 and 2026), the Path "
                       "Inventory, Table 4.3 of the Cycle Design Guide and weather station CVM-WX1. A day counts as crowded "
                       "once, however many hours overflow.", small))
    pages = []

    def count(canvas, d):
        pages.append(d.page)
    doc.build(s, onFirstPage=count, onLaterPages=count)
    assert len(pages) == 1, pages
    DOCS._reserialise(path, b"D:20261012160500+01'00'", N.PEOPLE["atl"][0], "Cycleway widening 2026-27")


# ---------------------------------------------------------------------------------------------- figures and write-up
def figures(g):
    mc, aa, bb, P = g["main"], g["ask_a"], g["ask_b"], g["P"]
    f = dict(call=mc["winner"], call_name=CW_NAME[mc["winner"]], segment=mc["bind"], segment_name=mc["seg"]["segment_name"],
             width_m=float(mc["seg"]["min_width_m"]), capacity=mc["cap"], hour_from="08:00", hour_to="09:00",
             family_size=len(A.FAMILY), clause_crowded=DOCS.CLAUSE_CROWDED, clause_replay=DOCS.CLAUSE_REPLAY,
             table_capacity=DOCS.TABLE_CAPACITY, wet_mm=A.WET_MM, growth_pct=round(100 * (mc["growth_golden"] - 1)),
             growth_lo_pct=int(math.floor(100 * (min(mc["growth_cell"].values()) - 1))),
             growth_hi_pct=int(math.ceil(100 * (max(mc["growth_cell"].values()) - 1))),
             total_growth_2526_pct=r1(100 * (mc["total_growth_2526"] - 1)),
             term8_mean_2026=round(mc["term8_mean"]), n_term8=mc["n_term8"],
             tmax_2024=r1(mc["wsum"][2024][0]), tmax_2025=r1(mc["wsum"][2025][0]), tmax_2026=r1(mc["wsum"][2026][0]),
             wet_2024=round(mc["wsum"][2024][1]), wet_2025=round(mc["wsum"][2025][1]), wet_2026=round(mc["wsum"][2026][1]),
             forecast={c: r1(v) for c, v in mc["res"].items()},
             forecast_days={c: int(round(v)) for c, v in mc["res"].items()},
             term_mornings=mc["cells"].get(("wk_term", 8), 0), crowded_mornings=int(sum(mc["cells"].values())),
             family_min_call=r1(min(v[mc["winner"]] for v in mc["fam"].values())),
             family_max_call=r1(max(v[mc["winner"]] for v in mc["fam"].values())),
             family_max_other=r1(max(max(x for c, x in v.items() if c != mc["winner"]) for v in mc["fam"].values())))
    f["ask_a"] = {cid: dict(counter=v["C"], volunteers=v["V"], shortfall=r1(v["short"]), quarters=v["quarters"],
                            site=[x for x in P["register"] if x["counter_id"] == cid][0]["legacy_site_name"],
                            day=v["day"].isoformat()) for cid, v in aa.items()}
    f["ask_b"] = {cid: dict(hours=r1(v["hours"]), stoppages=v["n"], minutes=v["minutes"],
                            site=[x for x in P["register"] if x["counter_id"] == cid][0]["legacy_site_name"])
                  for cid, v in bb.items()}
    return f


def submission(f, path):
    aa = f["ask_a"]
    bb = f["ask_b"]
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Urban and regional science (forecasting).")
    L.append("**Analytical objective:** Forecasting and predictive modelling.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Widen %s (%s): it will be crowded on more days of summer 2027 than any other cycleway, every one of them at "
             "%s between %s and %s on a weekday morning, where an average school-term weekday in summer 2026 already carried "
             "%d riders in that hour against a capacity of %d, a flow growing %d to %d per cent a year.** Not Estuary Path, "
             "which leads only when each counter's 2025 to 2026 growth in total riders is carried forward, a growth the hot, "
             "dry summer of 2026 inflated; not Market Street, which leads only when each cycleway's dashboard counter stands "
             "for all of its segments; not Brickfields, whose Gasworks Lane crowds on fewer mornings." % (
                 f["call_name"], f["call"], f["segment_name"], f["hour_from"], f["hour_to"], f["term8_mean_2026"],
                 f["capacity"], f["growth_lo_pct"], f["growth_hi_pct"]))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. %s (%s) is **%.1f m** at its narrowest, a capacity of **%d** cyclists an hour both ways (Table %s)." % (
        f["segment_name"], f["segment"], f["width_m"], f["capacity"], f["table_capacity"]))
    L.append("2. With each day's rain and maximum temperature held fixed, %s's 08:00 weekday riders grow by **%d to %d per cent** "
             "a year." % (f["segment_name"], f["growth_lo_pct"], f["growth_hi_pct"]))
    L.append("3. %s is the only segment of %s that crowds, and only in the hour from **%s**." % (
        f["segment_name"], f["call_name"], f["hour_from"]))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Put counts_summer2024_legacy.csv (local hours, Ch1 plus Ch2) and counts_summer2025_2026.parquet (UTC to "
             "Europe/London, in plus out) on each counted segment's local clock hours through counter_register.xlsx, leaving "
             "no_data, estimated and blank hours out (policy %s)." % f["clause_crowded"])
    L.append("2. Took each counted segment's capacity from its minimum width in cycleway_path_inventory_2026.xlsx and Table 4.3 "
             "%s of cycle_design_guide_2023_section4.pdf: %s carries %d an hour." % (f["table_capacity"], f["segment_name"],
                                                                         f["capacity"]))
    L.append("3. Fitted, for each counter, each of weekdays and weekends (with bank holidays) and each clock hour, a line of the "
             "log of the hour's riders on year, a wet-day flag (%.1f mm or more) and the day's maximum temperature from "
             "weather_station_daily_2024-01-01_2026-09-30.csv over the three summers: %s's 08:00 weekday riders grow %d to %d "
             "per cent a year." % (f["wet_mm"], f["segment_name"], f["growth_lo_pct"], f["growth_hi_pct"]))
    L.append("4. Carried every recorded hour of 2024, 2025 and 2026 to 2027 at its own counter, day group and hour's growth, "
             "keeping each day's weather and calendar (policy %s), and counted the days any counted segment exceeds its "
             "capacity in an hour from 06:00 to 22:00: %s is crowded on the most days, all of them at %s from %s." % (
                 f["clause_replay"], f["call_name"], f["segment_name"], f["hour_from"]))
    L.append("5. %s still leads with school-holiday weekdays as a day group of their own or with the hours grouped into "
             "periods." % f["call_name"])
    L.append("6. Matched count_week_15min_2026-05-11_15.csv (each quarter stamped at its end, in UTC, except CVC-1112 and "
             "CVC-1207, on local time from their laptop restarts to the 29 May clock reset in the maintenance log) to the "
             "quarter hours in volunteer_count_may2026.xlsx that both recorded, track riders only.")
    L.append("7. Took each dashboard counter's stoppages from counter_maintenance_log_2024-2026.csv by site, leaving out "
             "follow-up visits that repeat their job's downtime and counting a contractor job inside the unit's job once, and "
             "summed the real time inside 2025.")
    L.append("8. Recommend widening %s at %s." % (f["call_name"], f["segment_name"]))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### cycleway_widening_2027.xlsx")
    L.append("")
    L.append("1. Cycleway to widen: %s (%s)." % (f["call_name"], f["call"]))
    L.append("2. Segment that crowds it: %s (%s)." % (f["segment_name"], f["segment"]))
    L.append("3. Hours it crowds: %s to %s on weekday mornings." % (f["hour_from"], f["hour_to"]))
    L.append("4. May 2026 volunteer count, riders the counter recorded over the intervals both counted, and the counter's "
             "shortfall against the volunteers' track count:")
    for cid in sorted(aa, key=lambda c: (aa[c]["day"], c)):
        v = aa[cid]
        L.append("   - %s (%s): %s riders, shortfall %.1f per cent" % (v["site"], cid, "{:,}".format(v["counter"]), v["shortfall"]))
    L.append("5. Dashboard counters in 2025, hours recording nothing and separate stoppages:")
    for cid in sorted(bb):
        v = bb[cid]
        L.append("   - %s (%s): %.1f hours, %d stoppages" % (cid, v["site"], v["hours"], v["stoppages"]))
    L.append("")
    L.append("### widening_note_2027.pdf")
    L.append("")
    L.append("1. One-page note to the Transport and Environment Committee recommending Tolland Road (CW1) at Tolland Bridge, "
             "08:00 to 09:00 on weekday mornings, with a bar chart of each cycleway's forecast crowded days.")
    open(path, "w").write("\n".join(L) + "\n")


def compute(target):
    P = B.load(target)
    mc = main_call(P)
    return dict(P=P, main=mc, ask_a=ask_a(target), ask_b=ask_b(target))


def main(target, golden_dir, fig_path, sub_path):
    os.makedirs(golden_dir, exist_ok=True)
    g = compute(target)
    workbook(g, os.path.join(golden_dir, F_XLSX))
    note(g, os.path.join(golden_dir, F_NOTE))
    f = figures(g)
    with open(fig_path, "w") as fh:
        json.dump(f, fh, indent=1, sort_keys=True, default=str)
        fh.write("\n")
    submission(f, sub_path)
    return g, f
