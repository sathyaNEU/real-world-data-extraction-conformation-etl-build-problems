"""Writes task482's evidence pack from world.py and asks.py: the City's archive of Northlane's station status feed,
Northlane's trips, fleet moves and rider fault reports, the GBFS station information snapshot, the City's station
list, the pay-station vendor's sales export, alarm log, work orders and register, and the two distractors (the
documents are docs.py's)."""
import bisect
import csv
import datetime as dt
import json
import math
import os
from collections import defaultdict

import numpy as np

import asks as A
import docs as D
import world as W

FILES = {
    "status": "wellhaven_station_status_archive_2026q4.csv",
    "notes": "station_status_archive_notes.pdf",
    "trips": "northlane_trips_2026q4.csv",
    "moves": "northlane_fleet_moves_2026q4.csv",
    "reports": "northlane_rider_fault_reports_2026q4.csv",
    "gbfs": "gbfs_station_information_2027-01-11.json",
    "stations": "wellhaven_bike_share_station_list.xlsx",
    "agreement": "bike_share_operating_agreement_schedules.pdf",
    "sales": "paystation_sales_2026q4.csv",
    "alarms": "paystation_alarm_log_2026q4.csv",
    "workorders": "paystation_work_orders_2026q4.xlsx",
    "register": "paystation_register_2027-01-08.xlsx",
    "weather": "wellhaven_daily_weather_2026q4.csv",
    "report": "northlane_wellhaven_quarterly_report_2026q4.pdf",
}
LAT0, LON0 = 44.3012, -78.3197
KIND = {"core": "Downtown", "campus": "Campus", "hub": "Transit hub", "res": "Neighbourhood", "park": "Park"}
OPENED = {"core": dt.date(2019, 5, 17), "campus": dt.date(2019, 5, 17), "hub": dt.date(2019, 5, 17),
          "res": dt.date(2021, 6, 4), "park": dt.date(2022, 5, 13)}
TRIP0 = 4806000


def write_csv(path, head, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(head)
        n = 0
        for r in rows:
            w.writerow(r)
            n += 1
    return n


def epoch(t):
    return int(t.timestamp())


def iso_z(t):
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def local_str(t):
    return W.to_local(t).strftime("%Y-%m-%d %H:%M:%S")


def latlon(x, y):
    return (round(LAT0 + y / 111.0, 6), round(LON0 + x / (111.32 * math.cos(math.radians(LAT0))), 6))


def station_name(f, sid):
    return f.st[sid]["name"]


# ------------------------------------------------------------------------------------------------- the feed archive
def poller_gaps():
    """the spells the City's poller was down (local start, minutes)"""
    r = np.random.default_rng([W.SEED, 9])
    out = []
    while len(out) < 7:
        day = W.DAY0 + dt.timedelta(days=int(r.integers(3, 105)))
        start = dt.datetime(day.year, day.month, day.day) + dt.timedelta(minutes=int(r.integers(0, 24 * 60)))
        mins = int(r.integers(16, 150))
        if any(abs((start - s).total_seconds()) < 3 * 86400 for s, _ in out):
            continue
        if day in (dt.date(2026, 11, 1), dt.date(2026, 11, 2), dt.date(2026, 11, 9), dt.date(2026, 11, 23)):
            continue
        out.append((start, mins))
    return sorted(out)


def event_instants(E):
    """each station's status-changing instants (aware UTC), sorted"""
    f, sec = E["f"], E["sec"]
    ev = defaultdict(list)
    for t in f.trips:
        ev[t["start_station"]].append(A.utc_s(t["start_minute"], sec[t["start_seq"]]))
        if "end_seq" in t:
            ev[t["end_station"]].append(A.utc_s(t["end_minute"], sec[t["end_seq"]]))
    for mv in f.moves:
        ev[mv["station"]].append(A.utc_s(mv["minute"], sec[mv["seq"]]))
    for fl in f.flags:
        ev[fl["station"]].append(A.utc_s(fl["minute"], sec[fl["seq"]]))
    for s in ev:
        ev[s].sort()
    return ev


def status_rows(E):
    """one row per station each time a poll finds its status changed, and every station at the first poll after
    a spell the poller was down; polls run at the top of each minute (UTC epoch seconds)"""
    f = E["f"]
    ev = event_instants(E)
    gaps = [(W.minute_of(s), W.minute_of(s) + m) for s, m in poller_gaps()]
    down = np.zeros(W.NMIN + 1, dtype=bool)
    for a, b in gaps:
        down[a:b] = True
    ids = list(f.public)
    last = {}
    rows = []
    for m in range(1, W.NMIN):
        if down[m]:
            continue
        full = m == 1 or down[m - 1]
        t = A.utc_s(m)
        for s in ids:
            if not f.active[s][m - 1]:
                continue
            v = (int(f.listed[s][m - 1]), int(f.disabled[s][m - 1]), int(f.docks[s][m - 1]))
            if full or last.get(s) != v:
                lst = ev.get(s, [])
                i = bisect.bisect_left(lst, t)
                beat = epoch(t) - 1 - ((epoch(t) - 1 - (s * 47) % 300) % 300)      # the station's 5-minute heartbeat
                lr = max(epoch(lst[i - 1]) if i else 0, beat)
                rows.append([epoch(t), s, v[0], v[1], v[2], 0, 1, 1, 1, lr])
                last[s] = v
    return rows


# ------------------------------------------------------------------------------------------------- trips and moves
def trip_rows(E):
    f, sec, rtype = E["f"], E["sec"], E["rtype"]
    rows = []
    for t in f.trips:
        if "end_seq" not in t:
            continue
        a = A.utc_s(t["start_minute"], sec[t["start_seq"]])
        b = A.utc_s(t["end_minute"], sec[t["end_seq"]])
        if b >= W.END:
            continue
        rows.append([TRIP0 + t["trip"], t["bike"], local_str(a), t["start_station"], station_name(f, t["start_station"]),
                     local_str(b), t["end_station"], station_name(f, t["end_station"]), int((b - a).total_seconds()),
                     rtype[t["trip"]]])
    # Northlane's export appended the week of 16 November a second time when that week was re-run
    wk = [r for r in rows if "2026-11-16" <= r[2][:10] <= "2026-11-22"]
    return rows + wk


def move_rows(E):
    f, sec = E["f"], E["sec"]
    acts = {"pickup": "Pick up", "drop": "Drop off"}
    rows = []
    for mv in sorted(f.moves, key=lambda x: x["seq"]):
        t = A.utc_s(mv["minute"], sec[mv["seq"]])
        rows.append([local_str(t), mv["van"], mv["station"], acts[mv["action"]], "WHB-%04d" % mv["bike"]])
    return rows


CATS = (("Flat tire", 0.34), ("Chain", 0.18), ("Brakes", 0.20), ("Gears", 0.10), ("Seat or seat post", 0.08),
        ("Other", 0.10))


def report_rows(E):
    f = E["f"]
    r = np.random.default_rng([W.SEED, 10])
    rows = []
    for k, rep in enumerate(f.reports):
        t = A.utc_s(rep["minute"], int(r.integers(25, 59)) if rep["how"] == "seen" else 0)
        if rep["how"] == "ride":
            t = t + dt.timedelta(seconds=int(r.integers(70, 300)))
        u = r.random()
        acc, cat = 0.0, CATS[-1][0]
        for c, p in CATS:
            acc += p
            if u < acc:
                cat = c
                break
        rows.append([iso_z(t), rep["bike"], rep["station"], cat])
    rows.sort()
    return [["FR-%05d" % (20410 + i)] + row for i, row in enumerate(rows)]


# ------------------------------------------------------------------------------------------------- stations
def gbfs_json(f):
    stations = []
    for sid in sorted(f.public):
        if not f.st[sid].get("open", True):
            continue
        a = f.st[sid]
        lat, lon = latlon(a["x"], a["y"])
        stations.append({"station_id": str(sid), "name": a["name"], "lat": lat, "lon": lon, "capacity": a["cap"],
                         "rental_methods": ["KEY", "CREDITCARD", "APPLEPAY", "ANDROIDPAY"],
                         "is_virtual_station": False})
    stations.sort(key=lambda x: int(x["station_id"]))
    return {"last_updated": epoch(W.END), "ttl": 60, "version": "2.3", "data": {"stations": stations}}


def _book():
    import openpyxl
    return openpyxl.Workbook()


def _style(ws, widths, header=1):
    import openpyxl
    from openpyxl.styles import Alignment, Font
    for c in ws[header]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, wd in enumerate(widths):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wd
    ws.freeze_panes = ws.cell(row=header + 1, column=1).coordinate


def write_stations(path, f):
    wb = _book()
    ws = wb.active
    ws.title = "Stations"
    ws.append(["Station", "Name", "Area", "Feed station ID", "In service from", "In service to", "Docks",
               "Pay station", "Notes"])
    for s in W.STATIONS:
        sid, name, kind = s[0], s[1], s[2]
        no = sid - 100
        cap = f.st[sid]["cap"]
        if sid == W.RELOCATION["old"]:
            ws.append(["W-%02d" % no, name, KIND[kind], sid, OPENED[kind], dt.date(2026, 11, 8), cap, "Yes",
                       "South side of Linden Ave at Hale St; moved across the street on the evening of 8 Nov 2026"])
            ws.append(["W-%02d" % no, name, KIND[kind], W.RELOCATION["new"], dt.date(2026, 11, 8), None, cap, "Yes",
                       "North side of Linden Ave at Hale St (sidewalk widening on the south side)"])
            continue
        note = None
        if sid in W.EXPANSIONS:
            when, c = W.EXPANSIONS[sid]
            note = "Expanded from %d to %d docks %s" % (W.STATIONS[[x[0] for x in W.STATIONS].index(sid)][5], c,
                                                       when.strftime("%-d %b %Y"))
        ws.append(["W-%02d" % no, name, KIND[kind], sid, OPENED[kind], None, cap, "Yes", note])
    for row in ws.iter_rows(min_row=2):
        for c in (row[4], row[5]):
            c.number_format = "yyyy-mm-dd"
    _style(ws, (9, 20, 14, 10, 12, 12, 7, 9, 60))
    wb.save(path)
    return ws.max_row - 1


# ------------------------------------------------------------------------------------------------- pay stations
def sales_rows(E):
    lab = {}
    final = E["final"]
    for no, ser in final.items():
        lab[ser] = no
    stock = {ser for ser, _ in E["stock"]}
    for s in E["swaps"]:
        if s["removed"] in stock:
            lab[s["removed"]] = s["no"]
    names = {s[0] - 100: s[1] for s in W.STATIONS}
    rows = []
    for i, s in enumerate(E["sales"]):
        no = lab[s["terminal"]]
        rows.append((s["when"], ["", iso_z(s["when"]), s["terminal"], "W-%02d" % no, names[no], s["product"],
                                 "%.2f" % s["amount"], "SALE", ""], i))
    vo = {}
    for v in E["voids"]:
        s = E["sales"][v["of"]]
        no = lab[s["terminal"]]
        rows.append((v["when"], ["", iso_z(v["when"]), s["terminal"], "W-%02d" % no, names[no], s["product"],
                                 "-%.2f" % s["amount"], "VOID", v["of"]], None))
    rows.sort(key=lambda x: (x[0], 0 if x[2] is not None else 1))
    ids = {}
    for k, (t, row, i) in enumerate(rows):
        if i is not None:
            ids[i] = "PS%07d" % (3301120 + k)
    final_rows = []
    k = 0
    for (t, row, i) in rows:
        row = list(row)
        row[0] = "PS%07d" % (3301120 + k)
        if row[7] == "VOID":
            row[8] = ids[row[8]]
        final_rows.append(row)
        k += 1
    return final_rows


DETAIL = {"COMMS_LOST": "Modem: no network registration", "COMMS_RESTORED": "Modem: network registered",
          "READER_FAULT": "Card reader: no response", "READER_OK": "Card reader: ready",
          "PAPER_LOW": "Receipt printer: paper low", "PAPER_OK": "Receipt printer: paper loaded",
          "TEMP_LOW": "Cabinet below 0 C: heater on", "TEMP_OK": "Cabinet temperature normal: heater off",
          "DOOR_OPEN": "Service door opened", "DOOR_CLOSED": "Service door closed"}


def alarm_rows(E):
    rows = []
    swaps = {A.W.utc_of_local(s["restart"]): s for s in E["swaps"]}
    for no in range(1, 25):
        evs = E["events"][no]
        for k, e in enumerate(evs):
            t, code = e[0], e[1]
            if code == "RESTART":
                if t in swaps:
                    det = "Restart after service"
                else:
                    loc = W.to_local(t)
                    det = "Scheduled restart" if loc.hour == 3 and loc.minute <= 1 else "Watchdog restart (no network 60 min)"
            else:
                det = DETAIL[code]
                if code == "READER_FAULT" and any(abs((t - W.utc_of_local(s["start"])).total_seconds()) < 1
                                                  for s in E["swaps"] if s["no"] == no):
                    det = "Card reader: not detected"
            rows.append((t, no, k, ["W-%02d" % no, iso_z(t), code, det]))
    rows.sort(key=lambda x: (x[0], x[1], x[2]))
    return [["AL%07d" % (880400 + k)] + r[3] for k, r in enumerate(rows)]


def write_workorders(path, E):
    import openpyxl  # noqa: F401
    names = {s[0] - 100: s[1] for s in W.STATIONS}
    r = np.random.default_rng([W.SEED, 11])
    items = []
    for s in E["swaps"]:
        items.append((s["start"] - dt.timedelta(minutes=int(r.integers(4, 12))), s["restart"] + dt.timedelta(minutes=int(r.integers(3, 9))),
                      s["no"], "Card terminal replacement (refurbishment program)", s["removed"], s["installed"],
                      "Tech %02d" % (10 + s["tech"]), "Refurbished terminal installed; pay station restarted"))
    for no in range(1, 25):
        for (t, kind) in E["visits"][no]:
            loc = W.to_local(t)
            if kind == "reader":
                items.append((loc - dt.timedelta(minutes=int(r.integers(12, 35))), loc + dt.timedelta(minutes=int(r.integers(2, 8))),
                              no, "Card reader fault", None, None, "Tech %02d" % (11 + int(r.integers(0, 4))),
                              "Reader reseated and tested" if r.random() < 0.6 else "Reader cable replaced"))
            else:
                items.append((loc - dt.timedelta(minutes=int(r.integers(2, 6))), loc + dt.timedelta(minutes=int(r.integers(2, 5))),
                              no, "Receipt paper", None, None, "Tech %02d" % (11 + int(r.integers(0, 4))), "Paper roll replaced"))
    items.sort(key=lambda x: x[0])
    wb = _book()
    ws = wb.active
    ws.title = "Work orders"
    ws.append(["WO", "Pay station", "Station", "Opened", "Closed", "Work type", "Terminal removed", "Terminal installed",
               "Technician", "Notes"])
    for k, it in enumerate(items):
        o, c, no, wt, rm, ins, tech, note = it
        ws.append(["WO-26-%05d" % (31207 + k), "W-%02d" % no, names[no], o.replace(second=0, microsecond=0),
                   c.replace(second=0, microsecond=0), wt, rm, ins, tech, note])
    for row in ws.iter_rows(min_row=2):
        for c in (row[3], row[4]):
            c.number_format = "yyyy-mm-dd hh:mm"
    _style(ws, (13, 10, 20, 16, 16, 44, 15, 15, 10, 50))
    wb.save(path)
    return len(items)


def write_register(path, E):
    names = {s[0] - 100: s[1] for s in W.STATIONS}
    inst = {s["no"]: s["install"].date() for s in E["swaps"]}
    wb = _book()
    ws = wb.active
    ws.title = "Pay stations"
    ws.append(["Pay station", "Station", "Model", "Card terminal", "Terminal model", "Terminal installed", "Firmware"])
    for no in range(1, 25):
        ws.append(["W-%02d" % no, names[no], A.MODEL, E["final"][no], A.TERMINAL_MODEL, inst[no], "4.18.2"])
    for row in ws.iter_rows(min_row=2):
        row[5].number_format = "yyyy-mm-dd"
    _style(ws, (11, 20, 24, 15, 13, 16, 9))
    ws2 = wb.create_sheet("Terminals in stock")
    ws2.append(["Card terminal", "Terminal model", "Status", "Last pay station", "Received from workshop"])
    last = {s["removed"]: s["no"] for s in E["swaps"]}
    for ser, ready in E["stock"]:
        no = last.get(ser)
        ws2.append([ser, A.TERMINAL_MODEL, "In stock, refurbished", "W-%02d" % no if no else None, ready.date()])
    for row in ws2.iter_rows(min_row=2):
        row[4].number_format = "yyyy-mm-dd"
    _style(ws2, (15, 13, 22, 15, 20))
    ws3 = wb.create_sheet("Alarm codes")
    ws3.append(["Code", "Meaning", "Card payments"])
    for code, mean, pay in (("COMMS_LOST", "The modem has lost its network registration", "Stopped"),
                            ("COMMS_RESTORED", "The modem has registered on the network", "Resumed"),
                            ("READER_FAULT", "The card reader does not respond, or no card reader is detected", "Stopped"),
                            ("READER_OK", "The card reader responds and is ready", "Resumed"),
                            ("PAPER_LOW", "Receipt paper is low or out (receipts are optional)", "Not affected"),
                            ("PAPER_OK", "Receipt paper loaded", "Not affected"),
                            ("DOOR_OPEN", "The service door has been opened", "Not affected"),
                            ("DOOR_CLOSED", "The service door has been closed", "Not affected"),
                            ("TEMP_LOW", "The cabinet is below 0 C and its heater is on", "Not affected"),
                            ("TEMP_OK", "The cabinet temperature is back to normal", "Not affected"),
                            ("RESTART", "The pay station has restarted", None)):
        ws3.append([code, mean, pay])
    _style(ws3, (16, 62, 14))
    wb.save(path)
    return 24 + len(E["stock"])


# ------------------------------------------------------------------------------------------------- distractors
def weather_rows(E):
    return [[d.isoformat(), "%.1f" % w[0], "%.1f" % w[1], "%.1f" % w[2], "%.1f" % w[3]] for d, w in sorted(A.WEATHER.items())]


def build_pack(out, E):
    f = E["f"]
    p = lambda k: os.path.join(out, FILES[k])
    n = {}
    n["status"] = write_csv(p("status"), ["polled_at", "station_id", "num_bikes_available", "num_bikes_disabled",
                                          "num_docks_available", "num_docks_disabled", "is_installed", "is_renting",
                                          "is_returning", "last_reported"], status_rows(E))
    n["trips"] = write_csv(p("trips"), ["trip_id", "bike_id", "start_time", "start_station_id", "start_station_name",
                                        "end_time", "end_station_id", "end_station_name", "duration_s", "rider_type"],
                           trip_rows(E))
    n["moves"] = write_csv(p("moves"), ["logged_at", "vehicle", "station_id", "action", "bike"], move_rows(E))
    n["reports"] = write_csv(p("reports"), ["report_id", "reported_at", "bike_id", "station_id", "category"],
                             report_rows(E))
    with open(p("gbfs"), "w", encoding="utf-8") as fh:
        json.dump(gbfs_json(f), fh, indent=1)
        fh.write("\n")
    n["gbfs"] = len(gbfs_json(f)["data"]["stations"])
    n["stations"] = write_stations(p("stations"), f)
    n["sales"] = write_csv(p("sales"), ["sale_id", "sold_at", "terminal", "pay_station", "pay_station_name", "product",
                                        "amount", "transaction", "original_sale"], sales_rows(E))
    n["alarms"] = write_csv(p("alarms"), ["event_id", "pay_station", "event_time", "event", "detail"], alarm_rows(E))
    n["workorders"] = write_workorders(p("workorders"), E)
    n["register"] = write_register(p("register"), E)
    n["weather"] = write_csv(p("weather"), ["Date/Time", "Max Temp (\u00b0C)", "Min Temp (\u00b0C)", "Total Rain (mm)",
                                            "Total Snow (cm)"], weather_rows(E))
    D.write_notes(p("notes"), poller_gaps())
    D.write_agreement(p("agreement"))
    D.write_report(p("report"), E)
    n["notes"] = n["agreement"] = n["report"] = 1
    return n
