"""task490 shipped records: every csv, json and xlsx under target/, written from the clean truth in sim.py."""
import csv
import json
import os
import re
import zipfile
from datetime import date, datetime, timedelta

import numpy as np

import world as W
import sim

F_MOVES = "lock_counter_movements_2026.csv"
F_SITES = "counter_sites_2026.json"
F_KEEP = "tilsey_lock_keepers_log_2026.xlsx"
F_NOTICES = "navigation_notices_2026.csv"
F_LOCKS = "lock_register_2026.xlsx"
F_RET = "reservoir_returns_2026.xlsx"
F_COLD = "coldmere_outlet_15min_2026.csv"
F_LIC = "abstraction_licences_2026.xlsx"
F_READ = "abstraction_meter_readings_2026.csv"
F_WO = "works_orders_2026.csv"
F_BOATS = "boat_licence_register_extract_2026-11.csv"
F_STORE = "reservoir_storage_weekly_2026.csv"
MEMBER_TIME = (2026, 11, 3, 7, 12, 0)


def write_csv(target, name, header, rows):
    with open(os.path.join(target, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def normalise_zip(path, modified, app="Microsoft Excel", ver="16.0300"):
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    out = []
    for name, data in items:
        if name == "docProps/app.xml":
            data = re.sub(rb"<Application>[^<]*</Application>", ("<Application>%s</Application>" % app).encode(), data)
            data = re.sub(rb"<AppVersion>[^<]*</AppVersion>", ("<AppVersion>%s</AppVersion>" % ver).encode(), data)
        if name == "docProps/core.xml":
            data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                          b"\\g<1>" + modified.encode() + b"\\g<2>", data)
            data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)",
                          b"\\g<1>" + modified.encode() + b"\\g<2>", data)
        out.append((name, data))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in out:
            zi = zipfile.ZipInfo(name, date_time=MEMBER_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)


def wb_new(creator):
    from openpyxl import Workbook
    wb = Workbook()
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    return wb


def wb_save(wb, path, modified):
    wb.save(path)
    normalise_zip(path, modified)


# ------------------------------------------------------------------------------------------- the counters
def camera_events(cycles, boats):
    """every detection each tail camera made, before the export's formatting."""
    out = {}
    out_tilsey = W.TILSEY_CAMERA_OUT
    for spec in W.LOCKS:
        a = spec["asset"]
        r = sim.rng("camera:" + a)
        ev = []
        for c in cycles[a]:
            for b, t in zip(c["boats"], c["times"]):
                near_gap = a == "TC/L08" and any(abs((t - x).total_seconds()) < 7200 for x in out_tilsey)
                shown = b["vp"] if b["visitor"] else b["idx"]
                if r.random() < 0.041 and not near_gap:
                    shown = ""
                ev.append(dict(t=t, dir=c["direction"], cls="boat", idx=shown, conf=round(float(r.uniform(0.71, 0.99)), 2)))
                if shown and r.random() < 0.022:
                    ev.append(dict(t=t + timedelta(seconds=float(r.uniform(3, 40))), dir=c["direction"], cls="boat",
                                   idx=shown, conf=round(float(r.uniform(0.62, 0.93)), 2)))
        for d in W.DAYS:
            lam = {4: 0.5, 5: 0.9, 6: 1.3, 7: 1.8, 8: 2.2, 9: 1.1, 10: 0.4}[d.month]
            for _ in range(int(r.poisson(lam))):
                t = datetime(d.year, d.month, d.day) + timedelta(hours=float(r.uniform(9.3, 18.2)))
                ev.append(dict(t=t, dir="up" if r.random() < 0.5 else "down", cls="unpowered", idx="",
                               conf=round(float(r.uniform(0.44, 0.86)), 2)))
        if a == "TC/L08":
            ev = [e for e in ev if not (out_tilsey[0] <= e["t"] < out_tilsey[1])]
        ev.sort(key=lambda e: (e["t"], e["dir"], e["idx"]))
        out[a] = ev
    return out


def write_moves(target, events):
    rows = []
    base = {"KC/L12": 418220, "KC/L13": 207915, "HN/L31": 931046, "HN/L32": 552870, "TC/L08": 774301,
            "TC/L09": 160488}
    n = 0
    for spec in W.LOCKS:
        a = spec["asset"]
        r = sim.rng("recno:" + a)
        no = base[a]
        for e in events[a]:
            no += 1 + int(r.geometric(0.62)) - 1 + (int(r.integers(1, 4)) if r.random() < 0.06 else 0)
            v2 = e["t"] >= spec["fw"]
            if v2:
                u = W.to_utc(e["t"])
                ts = u.strftime("%Y-%m-%dT%H:%M:%SZ")
                dr = "A>B" if e["dir"] == "up" else "B>A"
                cl = "VESSEL" if e["cls"] == "boat" else "NON_MOTOR"
                fw = "5.0.3"
            else:
                ts = e["t"].strftime("%d/%m/%Y %H:%M:%S")
                dr = "UP" if e["dir"] == "up" else "DOWN"
                cl = "BOAT" if e["cls"] == "boat" else "UNPOWERED"
                fw = "4.2.1"
            rows.append([spec["site"], no, ts, dr, cl, e["idx"], "%.2f" % e["conf"], fw])
            n += 1
    write_csv(target, F_MOVES, ["site_code", "record_no", "detected_at", "direction", "class", "index_read",
                                "confidence", "firmware"], rows)
    return n


def write_sites(target):
    sites = []
    for spec in W.LOCKS:
        fw_utc = W.to_utc(spec["fw"])
        sites.append({
            "site_code": spec["site"],
            "asset": spec["asset"],
            "lock_name": spec["name"],
            "waterway": spec["canal"],
            "camera": {"position": "tail, below the bottom gates, facing up the chamber",
                       "axis": {"A": "tail pound", "B": "lock chamber"}},
            "firmware": [
                {"version": "4.2.1", "installed": "2025-02-%02dT10:00:00Z" % (11 + W.LOCKS.index(spec)),
                 "detected_at": "outstation clock, UK local time, dd/mm/yyyy hh:mm:ss",
                 "direction": "UP or DOWN"},
                {"version": "5.0.3", "installed": fw_utc.strftime("%Y-%m-%dT%H:%M:00Z"),
                 "detected_at": "UTC, ISO 8601",
                 "direction": "A>B or B>A along the camera axis"},
            ],
        })
    doc = {"system": "LockCount Mk3 counter network", "owner": W.ORG, "contact": W.PEOPLE["counters"],
           "exported_at": "2026-11-03T07:12:00Z", "sites": sites}
    with open(os.path.join(target, F_SITES), "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")


# --------------------------------------------------------------------------------------- keepers' log
def staffed_day(d):
    if date(2026, 7, 25) <= d <= date(2026, 9, 6):
        return True
    if d in (date(2026, 4, 3), date(2026, 4, 6), date(2026, 5, 4), date(2026, 5, 25), date(2026, 8, 31)):
        return True
    return d.weekday() >= 5 and date(2026, 4, 4) <= d <= date(2026, 9, 27)


def keeper_entries(cycles):
    r = sim.rng("keepers")
    out = []
    for a, short in (("TC/L08", "Top"), ("TC/L09", "Engine")):
        for c in cycles[a]:
            t0 = c["entry"]
            if not staffed_day(c["start"].date()) or not (9 <= c["start"].hour < 18):
                continue
            for k, b in enumerate(c["boats"]):
                t = t0 + timedelta(seconds=40 * k)
                idx = b["vp"] if b["visitor"] else b["idx"]
                out_win = W.TILSEY_CAMERA_OUT
                near = a == "TC/L08" and any(abs((t - x).total_seconds()) < 7200 for x in out_win)
                if r.random() < 0.08 and not near:
                    idx = ""
                day_keepers = W.KEEPERS[(t0.toordinal() * 7 + (0 if short == "Top" else 3)) % len(W.KEEPERS)]
                note = ""
                if b.get("hire"):
                    note = "hire"
                elif b["type"] == "cruiser" and r.random() < 0.3:
                    note = "cruiser"
                out.append(dict(t=t, lock=short, asset=a, boat=b["name"], idx=idx,
                                dir="U" if c["direction"] == "up" else "D", keeper=day_keepers, note=note))
    out.sort(key=lambda e: (e["t"], e["lock"], e["boat"]))
    return out


def write_keepers(target, entries):
    wb = wb_new(W.PEOPLE["volunteers"])
    first = True
    for m, label in ((4, "Apr"), (5, "May"), (6, "Jun"), (7, "Jul"), (8, "Aug"), (9, "Sep")):
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = label
        ws.append(["Tilsey summit lock-keepers' log, %s 2026" % date(2026, m, 1).strftime("%B")])
        ws.append(["Volunteers on duty 09:00 to 18:00. Times as on the lock-keepers' watch."])
        ws.append([])
        ws.append(["Day", "Time", "At", "Boat", "Index no.", "Up/Down", "Keeper", "Notes"])
        for e in entries:
            if e["t"].month != m:
                continue
            ws.append([e["t"].strftime("%d/%m/%y"), e["t"].strftime("%H:%M"), e["lock"], e["boat"], e["idx"],
                       e["dir"], e["keeper"], e["note"]])
        for col, wdt in zip("ABCDEFGH", (10, 7, 8, 22, 12, 9, 8, 10)):
            ws.column_dimensions[col].width = wdt
    wb_save(wb, os.path.join(target, F_KEEP), "2026-11-04T16:20:00Z")


# ------------------------------------------------------------------------------------------- notices
def write_notices(target):
    rows = [
        ["CCT-N-2026-0084", "2026-03-20", "Kelsby Canal", "Kelsby flight, locks 1 to 13", "Reopening",
         "2026-04-01 08:00", "", "Winter works complete. The flight reopens at 08:00 on Wednesday 1 April 2026. "
         "All locks are left empty."],
        ["CCT-N-2026-0085", "2026-03-20", "Harnock Navigation", "Harnock locks 24 to 39", "Reopening",
         "2026-04-01 08:00", "", "Winter works complete. Harnock locks reopen at 08:00 on Wednesday 1 April 2026. "
         "All locks are left empty."],
        ["CCT-N-2026-0086", "2026-03-23", "Tilsey Canal", "Tilsey flight, locks 1 to 17", "Reopening",
         "2026-04-01 08:00", "", "Winter works complete, including new top gates at Engine Lock. The flight reopens "
         "at 08:00 on Wednesday 1 April 2026. All locks are left empty."],
        ["CCT-N-2026-0131", "2026-04-14", "Tilsey Canal", "Towpath, Mill Lane bridge to Engine Lock", "Advice",
         "2026-04-20 08:00", "2026-04-24 16:00", "Towpath resurfacing. Pedestrians and cyclists diverted by road."],
        ["CCT-N-2026-0177", "2026-05-05", "Harnock Navigation", "Steward's Lock (32)", "Stoppage",
         "2026-05-12 08:00", "2026-05-26 17:00", "Emergency stoppage to repair the offside bottom gate collar. "
         "No passage."],
        ["CCT-N-2026-0189", "2026-05-22", "Harnock Navigation", "Steward's Lock (32)", "Stoppage",
         "2026-05-12 08:00", "2026-05-29 17:00", "Extension to CCT-N-2026-0177. Collar casting delayed; the lock "
         "reopens at 17:00 on Friday 29 May. The lock is left empty."],
        ["CCT-N-2026-0203", "2026-05-27", "Kelsby Canal", "Kelsby summit, Feeder Bridge", "Advice",
         "2026-06-01 09:00", "2026-06-03 15:00", "Bridge parapet repairs. Navigation open; please follow the "
         "instructions of the contractor's banksman."],
        ["CCT-N-2026-0244", "2026-06-11", "Harnock Navigation", "Harnock summit", "Advice", "2026-06-13 07:00",
         "2026-06-13 13:00", "Angling match on the summit pound between Harnock Top Lock and Fox Bridge. Please "
         "keep to the centre of the channel and slow down."],
        ["CCT-N-2026-0301", "2026-07-02", "Tilsey Canal", "Tilsey summit, Hollow Wood", "Advice",
         "2026-07-06 08:00", "2026-07-10 16:00", "Tree works from the offside. Short delays to passage."],
        ["CCT-N-2026-0347", "2026-07-28", "Kelsby Canal", "Kelsby summit", "Advice", "2026-07-28 00:00", "",
         "Reservoir levels are below normal for the time of year. Water is being released to the summit; please "
         "report any lock paddle left open or gate left ajar to the Kelsby control room."],
        ["CCT-N-2026-0361", "2026-08-03", "Tilsey Canal", "Tilsey Top Lock (8)", "Restriction",
         "2026-08-03 12:00", "", "Restricted passage while lock-side equipment is repaired: passage 09:00 to 18:00 "
         "only, assisted by the volunteer lock-keepers. The lock is padlocked outside these hours."],
        ["CCT-N-2026-0402", "2026-08-23", "Tilsey Canal", "Tilsey Top Lock (8)", "Restriction lifted",
         "2026-08-23 15:30", "", "Repairs complete. CCT-N-2026-0361 is withdrawn and normal passage resumes from "
         "15:30 on Sunday 23 August."],
        ["CCT-N-2026-0415", "2026-08-27", "Harnock Navigation", "Harnock locks 24 to 30", "Advice",
         "2026-08-29 00:00", "2026-08-31 23:59", "Bank holiday weekend: expect queues at the Harnock flight."],
        ["CCT-N-2026-0458", "2026-09-14", "Kelsby Canal", "Kelsby Wharf", "Advice", "2026-09-19 08:00",
         "2026-09-19 18:00", "Wharf open day. Visitor moorings at the wharf closed for the day."],
        ["CCT-N-2026-0496", "2026-10-02", "Tilsey Canal", "Tilsey flight, locks 1 to 7", "Advice",
         "2026-10-05 08:00", "2026-10-09 16:00", "Offside vegetation cutting. Short delays."],
        ["CCT-N-2026-0533", "2026-10-21", "Kelsby Canal", "Kelsby flight, locks 1 to 13", "Stoppage",
         "2026-11-09 08:00", "2027-03-12 16:00", "Winter works 2026/27: lock gate replacement at locks 4 and 9 "
         "and chamber repairs at Wharf Lock (13). No passage."],
        ["CCT-N-2026-0537", "2026-10-22", "Harnock Navigation", "Harnock locks 24 to 39", "Stoppage",
         "2026-11-16 08:00", "2027-02-26 16:00", "Winter works 2026/27. No passage."],
    ]
    write_csv(target, F_NOTICES, ["notice_no", "issued", "waterway", "location", "notice_type", "starts",
                                  "ends", "summary"], rows)


# ---------------------------------------------------------------------------------------- lock register
OTHER_LOCKS = [
    ("KC/L10", "Hollins Lock", "Kelsby Canal", False, 21.98, 2.15, 2.41, 10, ("72' 1\"", "7' 1\"", "7' 11\"")),
    ("KC/L11", "Brook Lock", "Kelsby Canal", False, 22.04, 2.17, 2.66, 11, ("72' 4\"", "7' 1\"", "8' 9\"")),
    ("KC/L14", "Wharf Bottom Lock", "Kelsby Canal", False, 21.93, 2.16, 2.37, 14, ("72' 0\"", "7' 1\"", "7' 9\"")),
    ("HN/L30", "Mill Lock", "Harnock Navigation", True, 22.31, 4.33, 2.02, 30, ("73' 2\"", "14' 2\"", "6' 8\"")),
    ("HN/L33", "Fox Lock", "Harnock Navigation", True, 22.18, 4.35, 1.71, 33, ("72' 9\"", "14' 3\"", "5' 7\"")),
    ("TC/L07", "Hollow Wood Lock", "Tilsey Canal", False, 21.88, 2.16, 2.24, 7, ("71' 9\"", "7' 1\"", "7' 4\"")),
    ("TC/L10", "Engine Bottom Lock", "Tilsey Canal", False, 21.97, 2.17, 1.98, 10, ("72' 1\"", "7' 1\"", "6' 6\"")),
]


def write_lock_register(target):
    wb = wb_new(W.PEOPLE["asset"])
    ws = wb.active
    ws.title = "Chamber survey 2025"
    ws.append(["Coldmere Canals Trust: lock chamber survey 2025 (summit flights)"])
    ws.append([])
    ws.append(["Asset", "Lock name", "Waterway", "Pound above", "Chamber length (m)", "Chamber width (m)", "Rise (m)",
               "Lockful (m3)", "Filling (min)", "Emptying (min)", "Top gates", "Bottom gates",
               "Fall in 12 h, chamber full (mm)", "Surveyed"])
    r = sim.rng("survey")
    rows = []
    pounds = {"Kelsby": "Kelsby summit", "Harnock": "Harnock summit", "Tilsey": "Tilsey summit"}
    for spec in W.LOCKS:
        rows.append([spec["asset"], spec["name"], spec["canal"], pounds[spec["summit"]], spec["L"], spec["W"],
                     spec["R"], spec["lockful"], spec["fill"], spec["empty"],
                     {"TC/L09": 2026, "KC/L12": 2019, "KC/L13": 2021, "HN/L31": 2017, "HN/L32": 2020,
                      "TC/L08": 2018}[spec["asset"]],
                     {"TC/L09": 2015, "KC/L12": 2022, "KC/L13": 2016, "HN/L31": 2023, "HN/L32": 2026,
                      "TC/L08": 2019}[spec["asset"]],
                     int(r.integers(6, 22)), "2025-%02d-%02d" % (int(r.integers(9, 11)), int(r.integers(2, 28)))])
    for a, nm, canal, broad, L, Wd, R, no, ft in OTHER_LOCKS:
        above = {"KC/L10": "Brook pound", "KC/L11": "Hollins pound", "KC/L14": "Wharf pound",
                 "HN/L30": "Mill pound", "HN/L33": "Fox pound", "TC/L07": "Hollow Wood pound",
                 "TC/L10": "Engine pound"}[a]
        rows.append([a, nm, canal, above, L, Wd, R, round(L * Wd * R, 1), 8.5 if broad else 6.5,
                     7.5 if broad else 5.0, int(r.integers(2008, 2024)), int(r.integers(2008, 2024)),
                     int(r.integers(9, 60)), "2025-%02d-%02d" % (int(r.integers(9, 11)), int(r.integers(2, 28)))])
    rows.sort(key=lambda x: (x[2], x[0]))
    for row in rows:
        ws.append(row)
    ws2 = wb.create_sheet("1951 schedule")
    ws2.append(["Schedule of locks, 1951 (transcribed 2004)"])
    ws2.append([])
    ws2.append(["Waterway", "No.", "Name", "Length", "Width", "Rise"])
    sched = [(s["canal"], s["old_no"], s["name"], *s["ft"]) for s in W.LOCKS]
    sched += [(canal, no, nm, *ft) for a, nm, canal, broad, L, Wd, R, no, ft in OTHER_LOCKS]
    for row in sorted(sched, key=lambda x: (x[0], x[1])):
        ws2.append(list(row))
    wb_save(wb, os.path.join(target, F_LOCKS), "2026-01-19T11:04:00Z")
    return rows


# ------------------------------------------------------------------------------------------- reservoirs
def keeper_return_lines(name, sched, session_totals=False):
    """one line per water day (the 24 hours ending 09:00 on the line's date)."""
    r = sim.rng("ret:" + name)
    lines = []
    d = date(2026, 3, 30)
    level = float(r.uniform(0.05, 0.25))
    turns_per = {"Upper Kelsby Reservoir": 1.38, "Lower Kelsby Reservoir": 1.62, "Tilsey Reservoir": 1.47}[name]
    while d <= date(2026, 11, 2):
        a = datetime(d.year, d.month, d.day, 9) - timedelta(days=1)
        b = a + timedelta(days=1)
        vol = sim.volume_between(sched, a, b)
        rate_now = 0.0
        for s, e, rt in sched:
            if s <= b < e:
                rate_now = rt
        remarks = []
        for s, e, rt in sched:
            if a < s <= b:
                remarks.append("%s valve opened to %.1f turns (%.1f Ml/d)" % (s.strftime("%H:%M"), rt / turns_per, rt))
            if a < e <= b and not any(abs((e - s2).total_seconds()) < 60 for s2, e2, rt2 in sched):
                remarks.append("%s valve shut" % e.strftime("%H:%M"))
        if session_totals:
            # this keeper books each release on the day the valve is shut, from the valve sheet's total
            tot = None
            for s, e, rt in sched:
                if a < e <= b:
                    tot = sim.volume_between(sched, s, e)
            vol = tot
        m = d.month
        level += {3: -0.004, 4: 0.002, 5: 0.008, 6: 0.017, 7: 0.024, 8: 0.021, 9: 0.006, 10: -0.012,
                  11: -0.02}[m] * float(r.uniform(0.4, 1.6))
        level = max(0.0, level)
        lines.append([d.strftime("%d/%m/%Y"), round(level, 2), round(rate_now / turns_per, 1) if rate_now else 0,
                      round(rate_now, 1), None if vol is None else round(vol, 1), "; ".join(remarks)])
        d += timedelta(days=1)
    return lines


def write_returns(target, scheds):
    wb = wb_new("Coldmere Canals Trust")
    keepers = {"Upper Kelsby Reservoir": "M. Okafor", "Lower Kelsby Reservoir": "M. Okafor",
               "Tilsey Reservoir": "S. Brennan"}
    first = True
    out = {}
    for name, sheet in (("Upper Kelsby Reservoir", "Upper Kelsby"), ("Lower Kelsby Reservoir", "Lower Kelsby"),
                        ("Tilsey Reservoir", "Tilsey")):
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = sheet
        ws.append(["Coldmere Canals Trust: reservoir daily return"])
        ws.append(["Site", name])
        ws.append(["Keeper", keepers[name]])
        ws.append(["Water day ends 09:00. Level below top water level read at 09:00."])
        ws.append([])
        ws.append(["Date", "Level below TWL (m)", "Valve (turns)", "Rate (Ml/d)", "Released (Ml)", "Remarks"])
        lines = keeper_return_lines(name, scheds[name], session_totals=(name == "Lower Kelsby Reservoir"))
        for ln in lines:
            ws.append(ln)
        ws.column_dimensions["F"].width = 48
        out[name] = lines
    wb_save(wb, os.path.join(target, F_RET), "2026-11-02T10:31:00Z")
    return out


def coldmere_series(sched):
    """15-minute means at the outlet weir, periods ending at the stamp (UTC), head and the outstation's flow."""
    r = sim.rng("coldmere")
    t = datetime(2026, 3, 31, 0, 15)
    end = datetime(2026, 11, 1, 6, 0)
    rows = []
    while t <= end:
        mid_local = W.to_local(t - timedelta(minutes=7, seconds=30))
        rate = 0.0
        for s, e, rt in sched:
            if s <= mid_local < e:
                rate = rt
        q = rate * 1000.0 / 86400.0
        b_phys = W.COLDMERE_OLD_B if t <= W.COLDMERE_PLATE_UTC else W.COLDMERE_NEW_B
        lo, hi = 0.0, 1.5
        for _ in range(60):
            mid = (lo + hi) / 2
            if W.weir_q(b_phys, mid) < q:
                lo = mid
            else:
                hi = mid
        h = round(lo * 1000 + float(r.normal(0, 0.25)), 1) if q > 0 else 0.0
        b_store = W.COLDMERE_OLD_B if t <= W.COLDMERE_RATING_LOADED_UTC else W.COLDMERE_NEW_B
        flow = round(1000.0 * W.weir_q(b_store, h / 1000.0), 1)
        rows.append([t, h, flow, b_phys])
        t += timedelta(minutes=15)
    return rows


def write_coldmere(target, rows):
    out = [["COLDMERE RES OUTLET WEIR", t.strftime("%Y-%m-%dT%H:%M:%SZ"), "%.1f" % h, "%.1f" % f, "G"]
           for t, h, f, b in rows]
    write_csv(target, F_COLD, ["site", "period_end_utc", "head_mm_mean", "flow_ls_mean", "quality"], out)


def write_storage(target, scheds):
    r = sim.rng("storage")
    rows = []
    cap = {"Upper Kelsby Reservoir": 1180, "Lower Kelsby Reservoir": 2410, "Coldmere Reservoir": 6950,
           "Tilsey Reservoir": 1730}
    pct = {k: float(r.uniform(91, 99)) for k in cap}
    d = date(2026, 4, 5)
    while d <= date(2026, 11, 1):
        for k in sorted(cap):
            drop = {4: 0.6, 5: 1.4, 6: 2.6, 7: 3.4, 8: 3.0, 9: 0.8, 10: -1.9}.get(d.month, -2.5)
            pct[k] = min(100.0, max(18.0, pct[k] - drop * float(r.uniform(0.6, 1.4)) + float(r.normal(0, 0.4))))
            rows.append([d.isoformat(), k, cap[k], "%.1f" % pct[k]])
        d += timedelta(days=7)
    write_csv(target, F_STORE, ["week_ending", "reservoir_name", "capacity_ml", "storage_pct"], rows)


# ------------------------------------------------------------------------------------------- abstraction
def write_abstraction(target, meters):
    wb = wb_new("Coldmere Canals Trust")
    ws = wb.active
    ws.title = "Licences"
    ws.append(["Coldmere Canals Trust: water abstraction agreements, summit pounds (licence year 1 April to "
               "31 March)"])
    ws.append([])
    ws.append(["Licence", "Holder", "Pound", "Abstraction point", "Use", "Licensed (m3 a year)",
               "Meter serial", "Meter dials", "Last inspected"])
    r = sim.rng("lic")
    for lic in W.LICENCES:
        m = meters[lic["ref"]]
        ws.append([lic["ref"], lic["holder"], lic["summit"] + " summit", lic["point"],
                   {"irrigation": "Spray irrigation", "greens": "Golf course irrigation", "marina": "Boat wash and dock",
                    "fishery": "Fish farm, through-flow", "process": "Brewing process water",
                    "lake": "Ornamental lake top-up", "dust": "Dust suppression"}[lic["use"]],
                   lic["annual"], m["serial_now"], lic["digits"],
                   "2026-%02d-%02d" % (int(r.integers(1, 10)), int(r.integers(1, 28)))])
    ws.column_dimensions["B"].width = 34
    wb_save(wb, os.path.join(target, F_LIC), "2026-10-12T14:46:00Z")
    rows = []
    for lic in W.LICENCES:
        m = meters[lic["ref"]]
        for serial, t, reading in m["rows"]:
            rows.append([serial, lic["point"], t.strftime("%d/%m/%Y"), t.strftime("%H:%M"),
                         ("%0" + str(lic["digits"]) + "d") % reading,
                         "Holder return" if lic["use"] != "fishery" else "CCT inspector"])
    rows.sort(key=lambda x: (datetime.strptime(x[2], "%d/%m/%Y"), x[1]))
    write_csv(target, F_READ, ["meter_serial", "point_ref", "read_date", "read_time", "reading_m3", "read_by"], rows)


def write_works(target, meters):
    r = sim.rng("works")
    cats = [("Vegetation", "Offside vegetation cut back"), ("Lock gates", "Gate paddle gear seized, freed and greased"),
            ("Lock gates", "Balance beam end cap replaced"), ("Towpath", "Pothole repair"),
            ("Bridges", "Parapet coping stone reset"), ("Culverts", "Culvert inlet cleared of debris"),
            ("Moorings", "Mooring ring replaced"), ("Signage", "Lock number plate replaced"),
            ("Water", "Bywash weir board adjusted"), ("Water", "Feeder grille cleared"),
            ("Buildings", "Lock cottage gutter repair"), ("Lock gates", "Collar bolts tightened"),
            ("Vandalism", "Graffiti removed from lock beam"), ("Towpath", "Fallen tree cleared")]
    locs = ["Kelsby flight", "Kelsby summit", "Kelsby Wharf", "Harnock flight", "Harnock summit", "Fox Bridge",
            "Tilsey flight", "Tilsey summit", "Engine Lock", "Upper Kelsby Reservoir", "Coldmere Reservoir",
            "Tilsey Reservoir", "Mill Lane"]
    rows = []
    no = 26004817
    d = date(2026, 1, 5)
    while d <= date(2026, 10, 30):
        for _ in range(int(r.poisson(1.15))):
            no += int(r.integers(3, 41))
            cat, desc = cats[int(r.integers(len(cats)))]
            loc = locs[int(r.integers(len(locs)))]
            done = d + timedelta(days=int(r.integers(0, 21)))
            rows.append([str(no), d.isoformat(), done.isoformat() if done <= date(2026, 11, 2) else "", loc, "",
                         cat, desc, "Complete." if done <= date(2026, 11, 2) else ""])
        d += timedelta(days=1)
    for lic in W.LICENCES:
        ex = meters[lic["ref"]]["exchange"]
        if not ex:
            continue
        raised = ex["time"].date() - timedelta(days=int(r.integers(9, 26)))
        note = ("Meter SN %s removed, final reading %06d. New meter SN %s fitted and sealed, reading %06d at "
                "%s. Holder informed." % (ex["old"], ex["removed"], ex["new"], ex["installed"],
                                           ex["time"].strftime("%H:%M")))
        no_ex = str(26004817 + int(r.integers(1000, 9000)))
        rows.append([no_ex, raised.isoformat(), ex["time"].date().isoformat(), lic["summit"] + " summit",
                     lic["point"], "Water", "Abstraction meter failed register test; replace meter (%s)" % lic["ref"],
                     note])
    rows.sort(key=lambda x: (x[1], x[0]))
    write_csv(target, F_WO, ["wo_number", "raised", "completed", "location", "asset", "category", "description",
                             "completion_note"], rows)


def write_boats(target, boats, fleet):
    r = sim.rng("boatreg")
    rows = []
    moorings = ["Kelsby Wharf", "Harnock Basin", "Tilsey Marina", "Fox Bridge moorings", "Ludford Cut",
                "Mill Lane moorings", "Hollins Farm", "continuous cruiser", "Ashdown Marina", "Brook End"]
    for b in boats + fleet:
        if b["visitor"]:
            continue
        lt = "Business (hire)" if b.get("hire") else ("Private" if r.random() < 0.93 else "Business (trade)")
        rows.append([b["idx"], b["name"], b["type"], b["length"], "%.1f" % b["beam"],
                     "Kelsby Wharf" if b.get("hire") else moorings[int(r.integers(len(moorings)))], lt,
                     (date(2026, 4, 1) + timedelta(days=int(r.integers(0, 365)))).isoformat()])
    rows.sort(key=lambda x: x[0])
    write_csv(target, F_BOATS, ["index_no", "boat_name", "craft_type", "length_ft", "beam_ft", "home_mooring",
                                "licence_type", "licence_expires"], rows)
