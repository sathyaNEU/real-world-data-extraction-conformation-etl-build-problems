"""The golden deliverables: line_patrol_2026-11-09.xlsx and reliability_2026.svg, written from golden.compute's results."""
import datetime as dt
import os
from xml.sax.saxutils import escape

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import postprocess as PP

NAMES = {"BLV": "Bluffview", "CTR": "Cotter Road", "MLR": "Millrace", "NYD": "North Yard", "SYC": "Sycamore"}


def r2(x):
    return float("%.2f" % x)


def r1(x):
    return float("%.1f" % x)


def day_text(d):
    return "%d %s" % (d.day, d.strftime("%B"))


def figures(res):
    """The figures the write-up and the workbook state, from the pack."""
    call, ru = res["call"], res["runner_up"]
    sc, sr = res["sep"][call], res["sep"][ru]
    F = dict(call=call, runner_up=ru, tmed=res["tmed"], nsys=res["nsys"],
             meds=[d.isoformat() for d in res["meds"]],
             stretch=dict(device=sc["device"], to=[z for z, _ in sc["zone_to"]], to_poles=[p for _, p in sc["zone_to"]]),
             ru_stretch=dict(device=sr["device"], from_pole=sr["pole"], to=[z for z, _ in sr["zone_to"]]),
             call_group=dict(n=sc["n"], phase=sc["phase"], lo=sc["lo"], hi=sc["hi"], first=sc["first"].isoformat(),
                             last=sc["last"].isoformat(), behind=sc["behind"], device=sc["device"]),
             ru_group=dict(n=sr["n"], phase=sr["phase"], lo=sr["lo"], hi=sr["hi"], first=sr["first"].isoformat(),
                           last=sr["last"].isoformat(), behind=sr["behind"], device=sr["device"]),
             others_max=max(res["best"][f][0] for f in res["best"] if f not in (call, ru)),
             feeders={})
    for f in sorted(res["idx"]):
        v = res["idx"][f]
        F["feeders"][f] = dict(nt=v["nt"], saidi=r1(v["saidi"]), maifi=r2(v["maifi"]), cemi=v["cemi"],
                               saidi_raw=v["saidi"], maifi_raw=v["maifi"])
    return F


THIN = Side(style="thin", color="FFBFBFBF")
HEAD = PatternFill("solid", fgColor="FFE4E9F0")
MARK = PatternFill("solid", fgColor="FFFCE7D9")
INK2 = "FF52514E"


def _head(ws, row, labels, widths=None):
    for j, h in enumerate(labels):
        c = ws.cell(row=row, column=j + 1, value=h)
        c.font = Font(bold=True)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="center")
        c.border = Border(bottom=THIN)
    if widths:
        for j, w in enumerate(widths):
            ws.column_dimensions[openpyxl.utils.get_column_letter(j + 1)].width = w


def _print(ws, landscape=True, repeat=None):
    ws.page_setup.orientation = "landscape" if landscape else "portrait"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    if repeat:
        ws.print_title_rows = repeat


def workbook(res, F, out):
    from golden import local
    call, ru = F["call"], F["runner_up"]
    cg, rg = F["call_group"], F["ru_group"]
    first = lambda s: day_text(dt.date.fromisoformat(s))
    zone_to = ", ".join("%s at %s" % (z, p) for z, p in zip(F["stretch"]["to"], F["stretch"]["to_poles"]))
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Patrol assignment"
    ws["A1"] = "Line patrol from 9 November: %s, %s breaker to recloser %s" % (call, NAMES[call[:3]], F["stretch"]["to"][0])
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Distribution Reliability, assigned 4 November 2026 for the week of 9 November; records to 31 October 2026"
    ws["A2"].font = Font(italic=True, size=9, color=INK2)
    lines = [
        ("Patrol feeder", call),
        ("Stretch to walk", "%s main line from the %s feeder breaker %s to recloser %s, with the taps fused off it "
                            "(DRP-04 5.4)" % (call, NAMES[call[:3]], cg["device"], zone_to)),
        ("Why there", "%s's breaker has recorded %d momentary faults on phase %s at %s to %s A, each cleared on the "
                      "first reclose, on %d separate mornings from %s to %s: one place on the line failing again and "
                      "again" % (call, cg["n"], cg["phase"], "{:,}".format(cg["lo"]), "{:,}".format(cg["hi"]), cg["n"],
                                 first(cg["first"]), first(cg["last"]))),
        ("Customers behind that breaker", cg["behind"]),
        ("Second choice", ru),
        ("Second choice's record", "beyond recloser %s at %s: %d momentary faults on phase %s at %s to %s A from %s to %s"
         % (rg["device"], F["ru_stretch"]["from_pole"], rg["n"], rg["phase"], "{:,}".format(rg["lo"]),
            "{:,}".format(rg["hi"]), first(rg["first"]), first(rg["last"]))),
        ("Customers behind that recloser", rg["behind"]),
        ("What keeps it second", "fewer repeat faults at one current (%d against %d), over a shorter run (since %s "
                                "against %s, %s), behind a recloser zone of %s customers against the %s a failure "
                                "at %s's breaker locks out"
         % (rg["n"], cg["n"], first(rg["first"]), first(cg["first"]),
            ("both still recurring on %s" % first(cg["last"])) if cg["last"] == rg["last"]
            else ("%s's last on %s against %s" % (call, first(cg["last"]), first(rg["last"]))),
            "{:,}".format(rg["behind"]), "{:,}".format(cg["behind"]), call)),
        ("Every other feeder", "no more than %d momentary faults at one phase and one current since 1 August"
         % F["others_max"]),
    ]
    for i, (k, v) in enumerate(lines):
        a = ws.cell(row=4 + i, column=1, value=k)
        a.font = Font(bold=True)
        a.alignment = Alignment(vertical="top")
        b = ws.cell(row=4 + i, column=2, value=v)
        b.alignment = Alignment(wrap_text=True, vertical="top", horizontal="left")
        if isinstance(v, int):
            b.number_format = "#,##0"
        ws.row_dimensions[4 + i].height = 30 if isinstance(v, str) and len(v) > 95 else 16
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 100
    _print(ws)
    # the per-feeder table
    ws2 = wb.create_sheet("Feeders Jan-Oct 2026")
    ws2["A1"] = "Reliability by feeder, 1 January to 31 October 2026, major event days (%s) left out" % \
        " and ".join(day_text(dt.date.fromisoformat(d)) for d in F["meds"])
    ws2["A1"].font = Font(bold=True)
    _head(ws2, 3, ["Feeder", "Customers served 31 Oct", "Minutes of interruption per customer served (SAIDI)",
                   "Momentary interruption events per customer served (MAIFI-E)",
                   "Customers with more than two sustained interruptions (CEMI-2)"], [9, 13, 19, 20, 21])
    ws2.row_dimensions[3].height = 46
    fs = sorted(F["feeders"])
    for i, f in enumerate(fs):
        v = F["feeders"][f]
        for j, (x, fmt) in enumerate(((f, None), (v["nt"], "#,##0"), (v["saidi"], "0.0"), (v["maifi"], "0.00"),
                                      (v["cemi"], "#,##0"))):
            c = ws2.cell(row=4 + i, column=j + 1, value=x)
            if fmt:
                c.number_format = fmt
            if f == call:
                c.fill = MARK
    tot = 4 + len(fs)
    nt = sum(F["feeders"][f]["nt"] for f in fs)
    sys_saidi = sum(F["feeders"][f]["saidi_raw"] * F["feeders"][f]["nt"] for f in fs) / nt
    sys_maifi = sum(F["feeders"][f]["maifi_raw"] * F["feeders"][f]["nt"] for f in fs) / nt
    for j, (x, fmt) in enumerate((("System", None), (nt, "#,##0"), (round(sys_saidi, 1), "0.0"),
                                  (round(sys_maifi, 2), "0.00"), (sum(F["feeders"][f]["cemi"] for f in fs), "#,##0"))):
        c = ws2.cell(row=tot, column=j + 1, value=x)
        c.font = Font(bold=True)
        c.border = Border(top=THIN)
        if fmt:
            c.number_format = fmt
    ws2.cell(row=tot + 2, column=1, value="Patrol feeder shaded. System row from the unrounded feeder figures.").font = \
        Font(italic=True, size=9, color=INK2)
    ws2.freeze_panes = "B4"
    _print(ws2, landscape=False, repeat="3:3")
    # the record behind the call
    ws3 = wb.create_sheet("Repeat faults")
    ws3["A1"] = "Momentary operations since 1 August 2026: %s breaker %s and %s recloser %s" % (
        call, cg["device"], ru, rg["device"])
    ws3["A1"].font = Font(bold=True)
    _head(ws3, 3, ["Feeder", "Device", "Date", "Time (Central)", "Faulted phase", "Fault current (A)", "Trips",
                   "In the repeat group"], [9, 12, 12, 14, 13, 16, 8, 18])
    rows = sorted((r for r in res["recs"] if (r["feeder"], r["device"]) in ((call, cg["device"]), (ru, rg["device"]))),
                  key=lambda r: (r["feeder"] != call, r["t"]))
    for i, r in enumerate(rows):
        g = cg if r["feeder"] == call else rg
        inside = r["phases"] == g["phase"] and g["lo"] <= r["current"] <= g["hi"]
        l = local(r["t"])
        vals = [r["feeder"], r["device"], l.date(), l.strftime("%H:%M:%S"), r["phases"], r["current"], r["ops"],
                "yes" if inside else None]
        for j, x in enumerate(vals):
            c = ws3.cell(row=4 + i, column=j + 1, value=x)
            if j == 2:
                c.number_format = "yyyy-mm-dd"
            if j == 5:
                c.number_format = "#,##0"
            if inside:
                c.fill = MARK
    ws3.freeze_panes = "A4"
    ws3.auto_filter.ref = "A3:H%d" % (3 + len(rows))
    _print(ws3, landscape=False, repeat="3:3")
    # notes: what the figures are, from the procedure
    ws4 = wb.create_sheet("Notes")
    notes = [
        ("As of", "Records to 31 October 2026; assignment made 4 November 2026."),
        ("Customers served", "Service points each feeder supplies on 31 October 2026 (DRP-04 2.1)."),
        ("Sustained and momentary", "More than five minutes is sustained, five or less momentary, planned work "
                                    "included (DRP-04 2.2). Openings SCADA holds past five minutes are sustained "
                                    "whether or not the OMS ticketed them; times are the OMS's where it holds the "
                                    "interruption and the SCADA log's where it does not, and one with no ticket runs "
                                    "from the opening that locked out its breaker or recloser, as the OMS times "
                                    "those it records (DRP-04 2.7)."),
        ("Momentary events", "Counted per customer: a customer's momentary interruptions within five minutes of the "
                             "first are one event, and those ending in that customer's sustained interruption, one "
                             "the OMS shows beginning in the event's minute, are part of it (DRP-04 2.5)."),
        ("Major event days", "%s, over the %s-minute threshold for 2026 on %s customers (DRP-04 4); every "
                             "interruption that began on them is left out."
         % (" and ".join(day_text(dt.date.fromisoformat(d)) for d in F["meds"]), F["tmed"],
            "{:,}".format(F["nsys"]))),
        ("CEMI-2", "Customers served on 31 October with more than two sustained interruptions in the period, each "
                   "customer's interruptions counted wherever it was supplied from (DRP-04 3.1 and 3.2)."),
        ("Repeat faults", "A device's momentary faults on one phase since 1 August 2026 whose recorded currents lie "
                          "within plus or minus 2 per cent of the group's middle (the highest no more than 4 per cent "
                          "above the lowest), counted on separate days; breaker currents from the relay event records, "
                          "recloser currents from the control logs with terminals read through the register's phasing."),
        ("Stretch", "The recording device's zone: the line to the next protective devices beyond it, with the taps "
                    "fused off it (DRP-04 5.4)."),
    ]
    _head(ws4, 1, ["Item", "Note"], [22, 110])
    for i, (k, v) in enumerate(notes):
        ws4.cell(row=2 + i, column=1, value=k).font = Font(bold=True)
        c = ws4.cell(row=2 + i, column=2, value=v)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws4.row_dimensions[2 + i].height = 30 if len(v) > 105 else 16
    os.makedirs(os.path.dirname(out), exist_ok=True)
    wb.save(out)
    PP.normalize_ooxml(out, "Kelsey Sanford", "Kelsey Sanford", "2026-11-04T14:06:31Z", "2026-11-04T16:48:10Z",
                       excel=True)


SURF, INK1, INK2S, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e1", "#a8a7a2"
S1, S2 = "#2a78d6", "#eb6834"


def chart(F, out):
    """Each feeder's SAIDI against its MAIFI-E, the patrol's feeder labelled."""
    W_, H_ = 780, 560
    L_, R_, T_, B_ = 78, 34, 90, 96
    xs = [v["maifi"] for v in F["feeders"].values()]
    ys = [v["saidi"] for v in F["feeders"].values()]
    xmax = max(10, (int(max(xs) / 10) + 1) * 10)
    ymax = max(50, (int(max(ys) / 50) + 1) * 50)
    px = lambda x: L_ + (W_ - L_ - R_) * x / xmax
    py = lambda y: H_ - B_ - (H_ - T_ - B_) * y / ymax
    call = F["call"]
    cv = F["feeders"][call]
    rank_s = sorted(F["feeders"], key=lambda f: -F["feeders"][f]["saidi"]).index(call) + 1
    rank_m = sorted(F["feeders"], key=lambda f: -F["feeders"][f]["maifi"]).index(call) + 1
    meds = " and ".join(day_text(dt.date.fromisoformat(d)) for d in F["meds"])
    o = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
         'font-family="Helvetica, Arial, sans-serif" role="img" aria-labelledby="t d">' % (W_, H_, W_, H_),
         '<title id="t">%s, the patrol feeder for the week of 9 November, sits mid-pack on both indices</title>' % call,
         '<desc id="d">Sixteen feeders: minutes of interruption per customer served against momentary interruption '
         'events per customer served, January to October 2026, major event days left out.</desc>',
         '<rect width="%d" height="%d" fill="%s"/>' % (W_, H_, SURF),
         '<text x="%d" y="30" font-size="16" font-weight="bold" fill="%s">%s, the patrol feeder for the week of 9 November, sits mid-pack '
         'on both indices</text>' % (L_, INK1, call),
         '<text x="%d" y="50" font-size="11.5" fill="%s">Minutes of interruption against momentary interruption events, '
         'per customer served, 1 January to 31 October 2026,</text>' % (L_, INK2S),
         '<text x="%d" y="66" font-size="11.5" fill="%s">major event days (%s) left out</text>' % (L_, INK2S, meds)]
    k = 0
    while k <= xmax:
        x = px(k)
        o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1"/>' % (x, T_, x, H_ - B_, GRID))
        o.append('<text x="%.1f" y="%d" font-size="11" text-anchor="middle" fill="%s">%d</text>' % (x, H_ - B_ + 17, INK2S, k))
        k += 10
    k = 0
    while k <= ymax:
        y = py(k)
        o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1"/>' % (L_, y, W_ - R_, y, GRID))
        o.append('<text x="%d" y="%.1f" font-size="11" text-anchor="end" fill="%s">%d</text>' % (L_ - 8, y + 4, INK2S, k))
        k += 50
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s"/>' % (L_, H_ - B_, W_ - R_, H_ - B_, AXIS))
    o.append('<text x="%.1f" y="%d" font-size="12" text-anchor="middle" fill="%s">MAIFI-E, momentary interruption '
             'events per customer served</text>' % ((L_ + W_ - R_) / 2, H_ - B_ + 40, INK1))
    o.append('<text x="20" y="%.1f" font-size="12" text-anchor="middle" fill="%s" transform="rotate(-90 20 %.1f)">'
             'SAIDI, minutes per customer served</text>' % ((T_ + H_ - B_) / 2, INK1, (T_ + H_ - B_) / 2))
    placed = [(px(v["maifi"]) - 8, py(v["saidi"]) - 8, px(v["maifi"]) + 8, py(v["saidi"]) + 8)
              for v in F["feeders"].values()]
    pts = sorted(F["feeders"], key=lambda f: (f == call, f))
    for f in pts:
        v = F["feeders"][f]
        x, y = px(v["maifi"]), py(v["saidi"])
        tip = "%s: SAIDI %.1f minutes, MAIFI-E %.2f events, CEMI-2 %s customers" % (f, v["saidi"], v["maifi"],
                                                                                  "{:,}".format(v["cemi"]))
        if f == call:
            o.append('<circle cx="%.1f" cy="%.1f" r="7.5" fill="%s" stroke="%s" stroke-width="2"><title>%s</title>'
                     '</circle>' % (x, y, S2, SURF, escape(tip)))
            continue
        o.append('<circle cx="%.1f" cy="%.1f" r="5" fill="%s" stroke="%s" stroke-width="2"><title>%s</title></circle>'
                 % (x, y, S1, SURF, escape(tip)))
        own = (x - 8, y - 8, x + 8, y + 8)
        lx, ly = x + 8, y + 4
        for dx, dy in ((0, 0), (0, -12), (0, 12), (-52, 0), (0, -24), (0, 24)):
            box = (lx + dx, ly + dy - 9, lx + dx + 40, ly + dy + 2)
            if not any(b != own and not (box[2] < b[0] or box[0] > b[2] or box[3] < b[1] or box[1] > b[3])
                       for b in placed):
                lx, ly = lx + dx, ly + dy
                placed.append(box)
                break
        o.append('<text x="%.1f" y="%.1f" font-size="10.5" fill="%s">%s</text>' % (lx, ly, INK2S, f))
    x, y = px(cv["maifi"]), py(cv["saidi"])
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>'
             % (x - 4, y + 6, x - 14, y + 20, INK2S))
    o.append('<text x="%.1f" y="%.1f" font-size="12" font-weight="bold" text-anchor="end" fill="%s">%s, patrol from '
             '9 November</text>' % (x - 16, y + 30, INK1, call))
    o.append('<text x="%.1f" y="%.1f" font-size="10.5" text-anchor="end" fill="%s">SAIDI %.1f (%s of 16), MAIFI-E '
             '%.2f (%s of 16)</text>' % (x - 16, y + 44, INK2S, cv["saidi"], _ord(rank_s), cv["maifi"], _ord(rank_m)))
    o.append('<text x="%.1f" y="%.1f" font-size="10.5" text-anchor="end" fill="%s">sent for its repeat faults, not '
             'its indices</text>' % (x - 16, y + 57, INK2S))
    o.append('<text x="%d" y="%d" font-size="10" fill="%s">Source: OMS outage history, SCADA sequence of events, '
             'recloser control logs and the GIS service points; DRP-04 rev 6.</text>' % (L_, H_ - 26, INK2S))
    o.append('<text x="%d" y="%d" font-size="10" fill="%s">Distribution Reliability, 4 November 2026.</text>'
             % (L_, H_ - 12, INK2S))
    o.append('</svg>')
    with open(out, "w") as fh:
        fh.write("\n".join(o) + "\n")


def _ord(n):
    return {1: "1st", 2: "2nd", 3: "3rd"}.get(n, "%dth" % n)


def write(res, gdir):
    F = figures(res)
    workbook(res, F, os.path.join(gdir, "line_patrol_2026-11-09.xlsx"))
    chart(F, os.path.join(gdir, "reliability_2026.svg"))
    return F
