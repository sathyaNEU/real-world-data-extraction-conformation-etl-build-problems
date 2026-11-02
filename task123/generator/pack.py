"""Writes the evidence pack under a target directory from the world in world.py."""
import json, os
from datetime import datetime, timedelta, date
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import world as Wd
from common import save_workbook, pdf_setup, write_csv

ENO = "Quaylight Energy Services Pty Ltd"
OC = "Owners Corporation 1, Plan of Subdivision PS431877Q"
COMPLEX = "Tannery Quay"
NEM12_NAME = "nem12_QUAYLIGHT_OC1PS431877Q_202607.csv"
PQ_NAME = "QES_PQ_hourly_V_20260712T0000Z-20260720T0000Z.csv"
EVENTS_NAME = "QES_PQ_events_2026-07.json"
READS_NAME = "QES_register_reads_2026-07.csv"
EXCH_NAME = "QES_meter_exchanges_2026.csv"
REG_NAME = "QES_child_meter_register_20261031.xlsx"
LOTS_NAME = "OC1_register_extract_lots_20260930.xlsx"
REMARK_NAME = "basement_remarking_schedule_March2025.xlsx"
APPS_NAME = "EV_charger_applications_2024-2026.xlsx"
WORKS_NAME = "OC1_2027_electrification_works_schedule.xlsx"
MSB_NAME = "MSB_upgrade_2019_rising_main_schedule.pdf"
STD_NAME = "OC1_electrification_capacity_standard_2026.pdf"
PARENT_NAME = "nem12_PARENT_6203117452_202607.csv"
COMMON_NAME = "common_property_submeters_2026-07.xlsx"
THERMAL_NAME = "switchboard_thermal_scan_June2025.pdf"
DISTRACTORS = [PARENT_NAME, COMMON_NAME, THERMAL_NAME]

JULY0 = date(2026, 7, 1)


def unit_label(a, style="plain"):
    tw, fl, pos = a["tower"], a["floor"], a["pos"]
    if style == "plain":
        return "%s%02d%02d" % (tw, fl, pos)
    if style == "dash":
        return "%s-%02d%02d" % (tw, fl, pos)
    if style == "slash":
        return "%02d%02d/%s" % (fl, pos, tw)
    if style == "words":
        return "Apt %d.%02d Tower %s" % (fl, pos, tw)
    raise ValueError(style)


def kwh_half(W, i):
    return W["load"][i] * 0.5


# ----------------------------------------------------------------------------------------------------- NEM12
def nem12(W, path):
    apts = W["apts"]
    gaps = dict(W["gaps"])
    est = {}
    for i, d in W["estimated"]:
        est.setdefault(i, set()).add(d)
    lines = ["100,NEM12,202608020530,QUAYLIGHT,OC1PS431877Q"]
    upd = "20260802053000"

    def dstr(d):
        return (JULY0 + timedelta(days=d - 1)).strftime("%Y%m%d")

    def fmt(vals):
        return ",".join("%.3f" % v for v in vals)

    def block(i, a, reg, serial, d_from, d_to, cut=None, part=None):
        cfg = "E1E2" if W["has_cl"][i] else "E1"
        rid, sfx, ds = ("1", "E1", "N1") if reg == "E1" else ("2", "E2", "N2")
        lines.append("200,%s,%s,%s,%s,%s,%s,KWH,30," % (a["nmi"], cfg, rid, sfx, ds, serial))
        src = W["load"][i] * 0.5 if reg == "E1" else W["cl"][i] * 0.5
        for d in range(d_from, d_to + 1):
            v = src[(d - 1) * 48:d * 48].copy()
            if cut is not None and d == cut[0]:
                hx = cut[1]
                if part == "old":
                    v[hx:] = 0.0
                    lines.append("300,%s,%s,V,,,%s," % (dstr(d), fmt(v), upd))
                    lines.append("400,1,%d,A,,," % hx)
                    lines.append("400,%d,48,N,,," % (hx + 1))
                else:
                    v[:hx] = 0.0
                    lines.append("300,%s,%s,V,,,%s," % (dstr(d), fmt(v), upd))
                    lines.append("400,1,%d,N,,," % hx)
                    lines.append("400,%d,48,A,,," % (hx + 1))
                continue
            if reg == "E1" and d in est.get(i, ()):
                v = like_day(W, i, d)
                lines.append("300,%s,%s,E51,,,%s," % (dstr(d), fmt(v), upd))
            else:
                lines.append("300,%s,%s,A,,,%s," % (dstr(d), fmt(v), upd))

    for i, a in enumerate(apts):
        last_day = gaps.get(i, 32) - 1
        regs = ["E1", "E2"] if W["has_cl"][i] else ["E1"]
        if "exchange" in a:
            dx, hx = a["exchange"]
            for reg in regs:
                block(i, a, reg, a["old_serial"], 1, dx, cut=(dx, hx), part="old")
            for reg in regs:
                block(i, a, reg, a["serial"], dx, last_day, cut=(dx, hx), part="new")
        else:
            for reg in regs:
                block(i, a, reg, a["serial"], 1, last_day)
    lines.append("900")
    with open(path, "w", newline="") as f:
        f.write("\r\n".join(lines) + "\r\n")


def like_day(W, i, d):
    """The operator's substitution: the meter's half-hourly profile over the seven days before (the seven after
    in the first week), the nearer days weighted more, each interval to the nearest Wh."""
    x = kwh_half(W, i)
    days = list(range(d - 1, d - 8, -1)) if d > 7 else list(range(d + 1, d + 8))
    w = np.arange(7, 0, -1, dtype=float)
    prof = np.sum([wt * x[(k - 1) * 48:k * 48] for wt, k in zip(w, days)], axis=0) / w.sum()
    return np.round(prof, 3)


# ------------------------------------------------------------------------------------------- power quality
def pq_hourly(W, path):
    apts = W["apts"]
    rng = np.random.default_rng(Wd.SEED + 111)
    V5 = W["V5"]
    s = 11 * 288 + 120               # 12 July 00:00 UTC is 12 July 10:00 market time
    rows = []
    t0 = datetime(2026, 7, 12, 0, 0)
    for i, a in enumerate(apts):
        series = []
        if a["three_phase"]:
            for e in range(3):
                series.append((str(e + 1), W["V5_3ph"][i][e]))
        else:
            series.append(("1", V5[i]))
        for el, x in series:
            seg = x[s:s + 192 * 12].astype(float).reshape(192, 12)
            for h in range(192):
                blk = seg[h]
                vmin = blk.min() - abs(rng.normal(0, 0.25))
                vmax = blk.max() + abs(rng.normal(0, 0.25))
                samples = 60 if rng.random() > 0.004 else int(rng.integers(52, 60))
                rows.append((a["serial"], el, (t0 + timedelta(hours=h)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                             "%.1f" % blk.mean(), "%.1f" % vmin, "%.1f" % vmax, samples))
    rows.sort(key=lambda r: (r[2], r[0], r[1]))
    write_csv(path, ["meter_serial", "element", "interval_start_utc", "v_avg", "v_min", "v_max", "samples"], rows, newline="\n")


def events(W):
    """Swell events from the five-minute record: a run of samples above 253.0 V is one event per element."""
    apts = W["apts"]
    rng = np.random.default_rng(Wd.SEED + 121)
    out = []
    t0 = datetime(2026, 6, 30, 14, 0)        # 1 July 00:00 market time in UTC
    for i, a in enumerate(apts):
        series = [("1", W["V5"][i])] if not a["three_phase"] else [(str(e + 1), W["V5_3ph"][i][e]) for e in range(3)]
        for el, x in series:
            above = x > 253.0
            k = 0
            n = len(x)
            while k < n:
                if above[k]:
                    k2 = k
                    while k2 + 1 < n and above[k2 + 1]:
                        k2 += 1
                    st = t0 + timedelta(seconds=k * 300 + int(rng.integers(0, 200)))
                    en = t0 + timedelta(seconds=(k2 + 1) * 300 - int(rng.integers(0, 200)))
                    if en <= st:
                        en = st + timedelta(seconds=40)
                    out.append({"i": i, "serial": a["serial"], "element": el, "start": st, "end": en,
                                "vpk": float(x[k:k2 + 1].max()) + abs(rng.normal(0, 0.3))})
                    k = k2 + 1
                else:
                    k += 1
    return out


def resent(W, evs):
    """The head-end's firmware push rebooted some concentrators early in the morning; each re-sent its meters'
    stored event logs from its last good upload around midnight.  The stored log keeps the meter's own clock,
    which runs on market time, and the head-end filed those times as UTC, so each re-sent record sits ten hours
    after the excursion it repeats, opened a little later and closed a little earlier on the stored log's
    one-second debounce, with the stored log's one-minute extreme; the head-end filed them as new events.
    The re-sent records fall in daylight hours when the meters' own hourly maxima are inside the limits."""
    rng = np.random.default_rng(Wd.SEED + 131)
    apts = W["apts"]
    # concentrator (tower, first floor, last floor) and the market-time date of the morning it rebooted
    zones = [("A", 2, 3, 15), ("A", 8, 9, 16), ("A", 12, 13, 19), ("A", 14, 15, 15), ("A", 20, 21, 16), ("A", 22, 23, 19),
             ("B", 4, 5, 16), ("B", 6, 7, 19), ("B", 10, 11, 15), ("B", 16, 17, 16), ("B", 18, 19, 19),
             ("C", 2, 3, 19), ("C", 6, 7, 15), ("C", 10, 11, 16), ("C", 16, 17, 19), ("C", 24, 25, 15)]
    extra = []
    for e in evs:
        a = apts[e["i"]]
        for tw, f0, f1, day in zones:
            lo = datetime(2026, 7, day - 1, 14, 0) - timedelta(minutes=25)       # last good upload, 23:35 market time
            hi = datetime(2026, 7, day - 1, 22, 0)                              # reboot, 08:00 market time
            if a["tower"] == tw and f0 <= a["floor"] <= f1 and lo <= e["start"] < hi:
                c = dict(e)
                c["start"] = e["start"] + timedelta(hours=10, seconds=int(rng.integers(4, 40)))
                c["end"] = e["end"] + timedelta(hours=10) - timedelta(seconds=int(rng.integers(4, 40)))
                c["vpk"] = e["vpk"] - float(rng.uniform(0.4, 1.6))
                c["resent"] = True
                if (c["end"] - c["start"]).total_seconds() >= 60:
                    extra.append(c)
                break
    return extra


def events_json(W, path):
    evs = events(W)
    evs = evs + resent(W, evs)
    rng = np.random.default_rng(Wd.SEED + 141)
    evs.sort(key=lambda e: (e["start"], e["serial"], e["element"]))
    ids = rng.choice(np.arange(4100000, 4999999), size=len(evs), replace=False)
    recs = []
    for e, eid in zip(evs, ids):
        recs.append({"event_id": "EV%d" % int(eid), "meter_serial": e["serial"], "element": e["element"],
                     "event": "VOLTAGE_SWELL", "threshold_v": 253.0,
                     "start_utc": e["start"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                     "end_utc": e["end"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                     "v_extreme": round(e["vpk"], 1)})
    doc = {"source": "Quaylight head-end, power quality event log", "site": "OC1 PS431877Q " + COMPLEX,
           "exported_utc": "2026-08-04T01:12:07Z", "period_utc": ["2026-06-30T14:00:00Z", "2026-07-31T14:00:00Z"],
           "events": recs}
    with open(path, "w") as f:
        json.dump(doc, f, indent=1)
    W["events_written"] = evs
    return evs


# ------------------------------------------------------------------------------------- reads and exchanges
def reads_csv(W, path):
    """The head-end's register reads export, with its own code descriptions beside each code."""
    apts = W["apts"]
    rdesc = {"E1": "General supply", "E2": "Controlled load"}
    tdesc = {"A": "Actual", "E": "Estimated"}
    rows = []
    for a in apts:
        for reg, key in (("E1", "reads"), ("E2", "reads_e2")):
            if key not in a:
                continue
            r = a[key]
            if "exchange" in a:
                rows.append((a["old_serial"], a["nmi"], reg, "2026-07-01 00:00", "%.2f" % r["old_jul"], "A"))
                rows.append((a["serial"], a["nmi"], reg, "2026-08-01 00:00", "%.2f" % r["new_aug"], "A"))
            else:
                rows.append((a["serial"], a["nmi"], reg, "2026-07-01 00:00", "%.2f" % r["jul"], "A"))
                rows.append((a["serial"], a["nmi"], reg, "2026-08-01 00:00", "%.2f" % r["aug"], "E" if a["aug_estimated"] else "A"))
                if "later_read" in a:
                    rows.append((a["serial"], a["nmi"], reg, "2026-08-01 " + a["later_read"]["time"],
                                 "%.2f" % a["later_read"]["e1" if reg == "E1" else "e2"], "A"))
    rows.sort(key=lambda x: (x[3], x[1], x[2]))
    rows = [(s_, n, g, rdesc[g], t, v, q, tdesc[q]) for s_, n, g, t, v, q in rows]
    write_csv(path, ["meter_serial", "nmi", "register", "register_desc", "read_local", "reading_kwh", "read_type", "read_type_desc"], rows)


def exchanges_csv(W, path):
    apts = W["apts"]
    rng = np.random.default_rng(Wd.SEED + 151)
    rows = []
    for x in W["exchanges"]:
        a = apts[x["i"]]
        when = datetime(2026, 7, x["day"], 0, 0) + timedelta(minutes=30 * x["hh"] - int(rng.integers(1, 25)))
        wo = "WO-%05d" % int(rng.integers(20000, 29999))
        e2 = a.get("reads_e2")
        rows.append((a["nmi"], x["old_serial"], x["new_serial"], when.strftime("%d/%m/%Y %H:%M"),
                     "%.2f" % a["reads"]["old_final"], "%.2f" % e2["old_final"] if e2 else "",
                     "%.2f" % a["reads"]["new_initial"], "%.2f" % e2["new_initial"] if e2 else "", wo,
                     str(rng.choice(["display fault", "comms module fault", "firmware recall batch QL2-24B"]))))
    rows.sort(key=lambda r: datetime.strptime(r[3], "%d/%m/%Y %H:%M"))
    write_csv(path, ["nmi", "old_meter_serial", "new_meter_serial", "exchanged_local", "old_final_E1_kwh", "old_final_E2_kwh",
                     "new_initial_E1_kwh", "new_initial_E2_kwh", "work_order", "reason"], rows)


# --------------------------------------------------------------------------------------------- registers
def meter_register(W, path):
    apts = W["apts"]
    rng = np.random.default_rng(Wd.SEED + 161)
    wb = Workbook()
    ws = wb.active
    ws.title = "Child meters"
    ws.append(["Quaylight Energy Services: child meter register, Tannery Quay embedded network (parent NMI 6203117452)"])
    ws.append(["As at 31/10/2026"])
    ws.append([])
    ws.append(["Child NMI", "Meter serial", "Comms module", "Lot", "Supply", "Board (as built 2004)", "Meter installed", "Status"])
    for a in sorted(apts, key=lambda a: a["nmi"]):
        if "exchange" in a:
            inst = "%02d/07/2026" % a["exchange"][0]
        else:
            inst = (date(2018, 3, 1) + timedelta(days=int(rng.integers(0, 900)))).strftime("%d/%m/%Y")
        ws.append([a["nmi"], a["serial"], a["module"], a["lot"], "3PH" if a["three_phase"] else "1PH",
                   a["board_2004"], inst, "Active"])
    for c, wdt in zip("ABCDEFGH", [14, 13, 13, 6, 7, 20, 14, 8]):
        ws.column_dimensions[c].width = wdt
    save_workbook(wb, path, "Quaylight Energy Services")


def lots_register(W, path):
    apts = W["apts"]
    rng = np.random.default_rng(Wd.SEED + 171)
    wb = Workbook()
    ws = wb.active
    ws.title = "Lots"
    ws.append([OC + ", " + COMPLEX + ": register extract, lots and accessory car spaces"])
    ws.append(["Extracted 30/09/2026 by the owners corporation manager"])
    ws.append([])
    ws.append(["Lot", "Unit", "Lot entitlement", "Lot liability", "Accessory car spaces"])
    for a in apts:
        ent = {"3B": 120, "2B": 95, "1B": 70}[a["type"]] + int(rng.integers(-4, 5)) + (60 if a["three_phase"] else 0)
        ws.append([a["lot"], unit_label(a, "plain"), ent, ent, ", ".join(a["spaces"])])
    for c, wdt in zip("ABCDE", [6, 8, 15, 13, 26]):
        ws.column_dimensions[c].width = wdt
    save_workbook(wb, path, "OC1 manager")


def remark_xlsx(W, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "B2 and B3 re-marking"
    ws.append(["Basement 2 and 3 line re-marking for the EV-ready bays: car space numbers before and after (works 10 to 14 March 2025)"])
    ws.append([])
    ws.append(["Space before", "Space after"])
    for old in sorted(W["remark"]):
        ws.append([old, W["remark"][old]])
    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 14
    save_workbook(wb, path, "OC1 manager")


def applications(W, path):
    """The by-law register of charger applications.  An application lapses when no installer is engaged within
    120 days of approval; a lapsed or declined request may be lodged again."""
    apts = W["apts"]
    rng = np.random.default_rng(Wd.SEED + 181)
    rows = []
    seq = {"24": 0, "25": 0, "26": 0}

    def nextno(yy):
        seq[yy] += 1
        return "EVC-%s-%03d" % (yy, seq[yy] * 3 + int(rng.integers(0, 3)))

    def unit_field(a, investor):
        if investor:
            street = str(rng.choice(["Hyde St", "Gordon St", "Albert St", "Pickett St", "Droop St", "Moore St"]))
            sub = str(rng.choice(["Yarraville", "Seddon", "Kensington", "Williamstown", "Brunswick", "Coburg"]))
            return "Lot %d, %d/%d %s, %s VIC" % (a["lot"], int(rng.integers(1, 9)), int(rng.integers(2, 140)), street, sub)
        return unit_label(a, str(rng.choice(["plain", "dash", "slash", "words"], p=[0.4, 0.3, 0.2, 0.1])))

    allrec = []
    for q in W["requests"]:
        a = apts[q["i"]]
        sp_new = q["space"]
        sp_old = W["remark_inv"].get(sp_new, sp_new)
        if q["relodged"]:
            d0 = date(2024, 8, 1) + timedelta(days=int(rng.integers(0, 200)))     # before the re-marking
            first = str(rng.choice(["Lapsed", "Declined"], p=[0.7, 0.3]))
            allrec.append(dict(d=d0, unit=unit_field(a, q["investor"]), space=sp_old, kw=7.4 if rng.random() < 0.7 else 11.0,
                               dec=first, dd=d0 + timedelta(days=int(rng.integers(20, 60))) if first == "Declined" else d0 + timedelta(days=int(rng.integers(150, 200)))))
            d1 = date(2025, 4, 1) + timedelta(days=int(rng.integers(0, 520)))
        else:
            d1 = date(2024, 9, 1) + timedelta(days=int(rng.integers(0, 760)))
        sp1 = sp_new if d1 >= date(2025, 3, 15) else sp_old
        if (not q["investor"]) and sp_new != sp_old and d1 >= date(2025, 3, 15) and rng.random() < 0.75:
            sp1 = sp_old
        dec = {"approved": "Approved", "declined": "Declined", "lapsed": "Lapsed", "pending": "Pending"}[q["outcome"]]
        dd = None if dec == "Pending" else d1 + timedelta(days=int(rng.integers(20, 75)))
        if dec == "Lapsed":
            dd = d1 + timedelta(days=int(rng.integers(150, 210)))
        if dd is not None and dd > date(2026, 10, 28):
            dd = date(2026, 10, 28) - timedelta(days=int(rng.integers(1, 30)))
            if dd < d1:
                dd = d1 + timedelta(days=5)
        if dec == "Pending" and d1 < date(2026, 7, 1):
            d1 = date(2026, 7, 1) + timedelta(days=int(rng.integers(0, 110)))
            sp1 = sp_new
        allrec.append(dict(d=d1, unit=unit_field(a, q["investor"]), space=sp1, kw=7.4 if rng.random() < 0.75 else 11.0, dec=dec, dd=dd))
    # the committee's own applications for the visitor bays, lodged by a member in the owners corporation's name
    members = [a for a in apts if a["type"] == "3B"]
    for k in range(3):
        a = members[int(rng.integers(0, len(members)))]
        d = date(2025, 10, 1) + timedelta(days=int(rng.integers(0, 300)))
        allrec.append(dict(d=d, unit=unit_label(a, "plain") + " (for the OC)", space="V-%02d" % (k + 2), kw=22.0,
                           dec="Pending" if k else "Approved", dd=None if k else d + timedelta(days=30)))
    allrec.sort(key=lambda r: r["d"])
    wb = Workbook()
    ws = wb.active
    ws.title = "Applications"
    ws.append(["Tannery Quay EV charging by-law (2024): register of applications"])
    ws.append(["Kept by the owners corporation manager; decisions of the committee"])
    ws.append([])
    ws.append(["Application", "Lodged", "Unit or owner address", "Car space", "Charger (kW)", "Committee decision", "Decision date"])
    for r in allrec:
        yy = r["d"].strftime("%y")
        ws.append([nextno(yy), r["d"].strftime("%d/%m/%Y"), r["unit"], r["space"], r["kw"], r["dec"],
                   r["dd"].strftime("%d/%m/%Y") if r["dd"] else ""])
    for c, wdt in zip("ABCDEFG", [13, 11, 36, 10, 12, 18, 13]):
        ws.column_dimensions[c].width = wdt
    save_workbook(wb, path, "OC1 manager")
    W["apps_written"] = allrec


def works_schedule(W, path):
    apts = W["apts"]
    rng = np.random.default_rng(Wd.SEED + 191)
    wb = Workbook()
    ws = wb.active
    ws.title = "Chargers"
    ws.append(["2027 electrification works: approved chargers (each connected to the supply of the unit shown)"])
    ws.append(["Issued 06/11/2026"])
    ws.append([])
    ws.append(["Unit", "Car space", "Charger", "Approval"])
    k = 0
    for i, a in enumerate(apts):
        if W["ev"][i] and a["spaces"]:
            k += 1
            ws.append([unit_label(a, "dash"), a["spaces"][0], "7.4 kW single-phase, load-managed to 16 A", "C-%03d" % (100 + k * 2)])
        elif W["ev"][i]:
            k += 1
            ws.append([unit_label(a, "dash"), "", "7.4 kW single-phase, load-managed to 16 A (wall unit at the unit's storage cage)", "C-%03d" % (100 + k * 2)])
    ws2 = wb.create_sheet("Cooktop conversions")
    ws2.append(["2027 gas network decommissioning: units converting from gas cooktops to induction"])
    ws2.append([])
    ws2.append(["Unit", "Gas meter", "Window"])
    for i, a in enumerate(apts):
        if W["cook"][i]:
            ws2.append([unit_label(a, "dash"), "G%s%02d%02d" % (a["tower"], a["floor"], a["pos"]),
                        str(rng.choice(["Feb 2027", "Mar 2027", "Apr 2027"]))])
    for wsx in (ws, ws2):
        for c in "ABCD":
            wsx.column_dimensions[c].width = 22
    save_workbook(wb, path, "Tannery Quay facilities")


# -------------------------------------------------------------------------------------------------- PDFs
def _pdf(path, title_lines, story_fn, producer_title):
    pdf_setup()
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate
    doc = SimpleDocTemplate(path, pagesize=A4, title=producer_title, author="", subject="", creator="",
                            leftMargin=50, rightMargin=50, topMargin=48, bottomMargin=48)
    doc.build(story_fn())


def _styles():
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=6)
    h = ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=12, leading=15, spaceAfter=8)
    h2 = ParagraphStyle("h2", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10, leading=13, spaceAfter=4, spaceBefore=6)
    small = ParagraphStyle("s", parent=body, fontSize=8, leading=10)
    return body, h, h2, small


def msb_pdf(W, path):
    from reportlab.platypus import Paragraph, Table, TableStyle, Spacer
    from reportlab.lib import colors
    body, h, h2, small = _styles()
    plan = W["plan"]
    cables = {160: "4c 70 mm2 Cu XLPE", 200: "4c 95 mm2 Cu XLPE", 250: "4c 120 mm2 Cu XLPE", 315: "4c 185 mm2 Cu XLPE"}

    def story():
        s = [Paragraph("Tannery Quay main switchboard replacement: rising main schedule", h),
             Paragraph("Prepared for the owners corporation by Brennand Electrical Contracting, 18 November 2019, at practical completion of the main switchboard replacement. The floor distribution boards were not altered by these works.", body),
             Paragraph("Each rising main below is a four-core main from the new main switchboard (MSB-1) to the floor distribution boards of the levels it serves. Ratings are per phase, at the installed derating.", body)]
        data = [["Rising main", "Former designation", "Levels served", "Cable", "Rating per phase (A)"]]
        old_names = {}
        for r in plan:
            k = int(r["riser"][1])
            old = "RM-%s%s" % (r["tower"], "ABCDEF"[k - 1])
            old_names[r["riser"]] = old
            data.append([r["riser"], old, "%d to %d" % (r["floors"][0], r["floors"][-1]), cables[r["rating_a"]], str(r["rating_a"])])
        t = Table(data, colWidths=[62, 88, 72, 140, 100])
        t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5), ("FONT", (0, 1), (-1, -1), "Helvetica", 8.5),
                               ("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
        s.append(t)
        s.append(Spacer(1, 8))
        s.append(Paragraph("Levels are the levels of the tower named by the main's first letter. Apartments are numbered by level and position: A1402 is level 14, position 02, Tower A. The house supply (lifts, car park ventilation, common lighting, pool plant) is fed from MSB-1 section 3 and is not on the rising mains.", body))
        s.append(Paragraph("Test results for each main (insulation resistance, continuity, phase rotation at MSB-1) are in the practical completion file held by the owners corporation manager.", small))
        return s
    _pdf(path, None, story, "Rising main schedule")


def standard_pdf(W, path):
    from reportlab.platypus import Paragraph, Spacer
    body, h, h2, small = _styles()

    def story():
        s = [Paragraph("Owners Corporation 1 PS431877Q (Tannery Quay)<br/>Electrification capacity standard for the 2027 works", h),
             Paragraph("Adopted by the committee on 14 October 2026 on the advice of the facilities manager. It sets how the capacity of the apartment rising mains is assessed before the 2027 chargers and cooktop conversions are connected, and the terms used in the facilities manager's reports to the committee.", body),
             Paragraph("1. Scope", h2),
             Paragraph("The rising mains in the 2019 rising main schedule, each supplying the apartments on the levels it serves. Ratings are those in that schedule, per phase, converted to kilowatts at %d V." % int(Wd.VNOM), body),
             Paragraph("2. Supplies", h2),
             Paragraph("Each apartment's supply is single-phase unless the child meter register records it as three-phase. A single-phase apartment draws its demand, existing and added, on the phase its supply is connected to. A three-phase apartment draws its demand equally on the three phases.", body),
             Paragraph("3. Phase demand", h2),
             Paragraph("A rising main's demand on a phase is the highest, over the half-hours beginning 17:00 to 20:30 market time on Monday 13 to Friday 17 July 2026, of the summed demand of the apartments drawing on that phase, each apartment's half-hourly demand being twice its metered kWh in the half-hour.", body),
             Paragraph("4. Added demand", h2),
             Paragraph("Each charger in the 2027 works schedule adds %.1f kW and each cooktop conversion adds %.1f kW, drawn by the unit the schedule names as in section 2." % (Wd.EV_KW, Wd.COOK_KW), body),
             Paragraph("5. When a rising main needs works", h2),
             Paragraph("A rising main needs re-phasing at its floor boards or a larger main before the 2027 works are connected where, on any of its phases, the phase demand plus the added demand on that phase exceeds %d per cent of its rating per phase." % int(round(Wd.LIMIT_SHARE * 100)), body),
             Paragraph("6. Supply voltage", h2),
             Paragraph("The statutory limits are 216 V to 253 V at the point of supply (Electricity Distribution Code of Practice). A three-phase supply is outside the limits while any one of its phases is outside them. An apartment's time outside the limits is the time its meter recorded its supply outside them.", body),
             Paragraph("7. Use", h2),
             Paragraph("An apartment's use over a period is the energy its meter registered over the period, general supply and controlled load together.", body),
             Paragraph("8. Charger requests", h2),
             Paragraph("A charger request is an owner's application under the EV charging by-law for a charger at one car space; an application lodged again for the same car space after a lapse or a decline continues that request. A charger connects to the supply of the apartment to which its car space is accessory.", body),
             Spacer(1, 6),
             Paragraph("Chair of the committee: Alan Herrera. Facilities manager: Kayla Hunt.", small)]
        return s
    _pdf(path, None, story, "Electrification capacity standard")


def thermal_pdf(W, path):
    from reportlab.platypus import Paragraph, Table, TableStyle
    from reportlab.lib import colors
    body, h, h2, small = _styles()
    rng = np.random.default_rng(Wd.SEED + 201)
    plan = W["plan"]

    def story():
        s = [Paragraph("Tannery Quay: annual thermographic survey of switchboards", h),
             Paragraph("Survey of 19 June 2025 under load (evening, 18:10 to 20:40). Findings are temperature rises above the reference component at the time of the scan; priority 1 is attend within one month, priority 2 at the next scheduled maintenance.", body)]
        data = [["Location", "Component", "Rise (K)", "Priority", "Action"]]
        locs = ["MSB-1 section 1", "MSB-1 section 2", "MSB-1 section 3"] + ["DB L%02d %s" % (int(rng.integers(2, 25)), str(rng.choice(["Tower A", "Tower B", "Tower C"]))) for _ in range(9)]
        for loc in locs:
            comp = str(rng.choice(["neutral link termination", "MCB line terminal", "busbar joint", "main switch line side", "DIN rail meter link"]))
            rise = round(float(rng.uniform(3.0, 24.0)), 1)
            pr = "1" if rise > 15 else "2"
            act = "re-torque and re-scan" if pr == "2" else "replace termination, re-scan"
            data.append([loc, comp, "%.1f" % rise, pr, act])
        t = Table(data, colWidths=[110, 140, 50, 50, 140])
        t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5), ("FONT", (0, 1), (-1, -1), "Helvetica", 8.5),
                               ("GRID", (0, 0), (-1, -1), 0.4, colors.grey)]))
        s.append(t)
        s.append(Paragraph("All priority 1 items were attended on 2 July 2025 and re-scanned clear.", small))
        return s
    _pdf(path, None, story, "Thermographic survey")


# ------------------------------------------------------------------------------------------- distractors
def parent_nem12(W, path):
    apts = W["apts"]
    rng = np.random.default_rng(Wd.SEED + 211)
    tot = W["load"].sum(0) * 0.5
    hh = W["hh"]
    common = 38.0 + 12.0 * ((hh >= 12) & (hh <= 44)) + rng.normal(0, 1.5, len(hh))
    total = tot * 1.012 + common * 0.5
    q = np.repeat(total / 2.0, 2)
    lines = ["100,NEM12,202608030610,CITIPWR,QUAYLIGHT", "200,6203117452,E1Q1,E1,E1,N1,0911743,KWH,15,"]
    for d in range(31):
        vals = q[d * 96:(d + 1) * 96] * (1 + rng.normal(0, 0.002, 96))
        lines.append("300,%s,%s,A,,,20260803061000," % ((JULY0 + timedelta(days=d)).strftime("%Y%m%d"), ",".join("%.3f" % v for v in vals)))
    lines.append("900")
    with open(path, "w", newline="") as f:
        f.write("\r\n".join(lines) + "\r\n")


def common_xlsx(W, path):
    rng = np.random.default_rng(Wd.SEED + 221)
    wb = Workbook()
    ws = wb.active
    ws.title = "Daily kWh"
    ws.append(["House supply sub-meters (MSB-1 section 3), daily kWh, July 2026"])
    ws.append([])
    names = ["Lifts Tower A", "Lifts Tower B", "Lifts Tower C", "Car park ventilation", "Common lighting", "Pool plant", "Gym"]
    ws.append(["Date"] + names)
    base = [rng.uniform(80, 120), rng.uniform(70, 110), rng.uniform(80, 120), rng.uniform(150, 260), rng.uniform(90, 140), rng.uniform(60, 130), rng.uniform(15, 35)]
    for d in range(31):
        dd = JULY0 + timedelta(days=d)
        wk = dd.weekday() < 5
        row = [dd.strftime("%d/%m/%Y")]
        for b in base:
            row.append(round(float(b * (1.08 if wk else 0.9) * rng.uniform(0.9, 1.1)), 1))
        ws.append(row)
    save_workbook(wb, path, "Tannery Quay facilities")


def write_pack(W, out):
    os.makedirs(out, exist_ok=True)
    nem12(W, os.path.join(out, NEM12_NAME))
    pq_hourly(W, os.path.join(out, PQ_NAME))
    events_json(W, os.path.join(out, EVENTS_NAME))
    reads_csv(W, os.path.join(out, READS_NAME))
    exchanges_csv(W, os.path.join(out, EXCH_NAME))
    meter_register(W, os.path.join(out, REG_NAME))
    lots_register(W, os.path.join(out, LOTS_NAME))
    remark_xlsx(W, os.path.join(out, REMARK_NAME))
    applications(W, os.path.join(out, APPS_NAME))
    works_schedule(W, os.path.join(out, WORKS_NAME))
    msb_pdf(W, os.path.join(out, MSB_NAME))
    standard_pdf(W, os.path.join(out, STD_NAME))
    parent_nem12(W, os.path.join(out, PARENT_NAME))
    common_xlsx(W, os.path.join(out, COMMON_NAME))
    thermal_pdf(W, os.path.join(out, THERMAL_NAME))
    return W


if __name__ == "__main__":
    import sys
    W = Wd.build_all()
    write_pack(W, sys.argv[1] if len(sys.argv) > 1 else "/tmp/t123pack")
