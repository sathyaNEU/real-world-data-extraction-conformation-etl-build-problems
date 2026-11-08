"""The pack read back into the representation the routes run on, from target/ alone: the register's crosswalk,
the status export de-duplicated and re-keyed to the current IDs, the visit windows from both schedule layouts and the
2027 plan, the supply log in Irish time, the two contractors' job codes, the programme's table and the 2026 charges a
day. Shared by checks.py (on the cut pack) and verify.py's own recomputation of the call."""
import csv
import datetime as dt
import os
import re
import subprocess
from zoneinfo import ZoneInfo

import openpyxl

UTC = dt.timezone.utc
IE = ZoneInfo("Europe/Dublin")
T0 = dt.datetime(2023, 1, 1, tzinfo=UTC)
END = int((dt.datetime(2026, 11, 1, tzinfo=UTC) - T0).total_seconds())


def sec(d):
    return int((d - T0).total_seconds())


def from_utc_iso(s):
    return sec(dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC))


def from_irish(s, fmt):
    return sec(dt.datetime.strptime(s, fmt).replace(tzinfo=IE).astimezone(UTC))


def pdf_text(path):
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True).stdout


def read_register(target):
    wb = openpyxl.load_workbook(os.path.join(target, "charge_point_register.xlsx"), read_only=True)
    cp = list(wb["Charge points"].iter_rows(values_only=True))
    hubs = list(wb["Hubs"].iter_rows(values_only=True))
    units, alias, serial = {}, {}, {}
    for r in cp[1:]:
        ser, new, old, hub, bay, make, model, kw, con, comm, status = r
        units[new] = dict(hub=hub, model=model, commissioned=comm.date() if hasattr(comm, "date") else comm)
        alias[old] = new
        alias[new] = new
        serial[ser] = new
    hl = [dict(code=r[0], name=r[1], county=r[2], site=r[3]) for r in hubs[1:]]
    return units, alias, serial, hl


def read_pack(target):
    units, alias, serial, hubs = read_register(target)
    names = {h["name"]: h["code"] for h in hubs}
    R = dict(hubs=hubs, units={}, rows={}, visits={}, visits27={}, dso={}, wo=[], programme={}, cpd={}, end=END)
    raw = {}
    with open(os.path.join(target, "connector_status_history_2023-2026.csv"), encoding="utf-8") as f:
        rd = csv.DictReader(f)
        for r in rd:
            k = alias[r["charge_point_id"]]
            raw.setdefault(k, []).append((from_utc_iso(r["timestamp_utc"]), r["status"]))
    for k, u in units.items():
        rows = sorted(raw.get(k, []))
        out = []
        for t, st in rows:
            if out and out[-1][1] == st:
                continue          # a re-sent notification, or the unit's first report to the new back office
            out.append((t, st))
        R["rows"][k] = out
        c = u["commissioned"]
        start = max(0, sec(dt.datetime(c.year, c.month, c.day, 11, 0, tzinfo=IE).astimezone(UTC)))
        R["units"][k] = dict(hub=u["hub"], model={"HX150": "HX150", "RC50": "RC50"}[u["model"]], start=start)
    for h in hubs:
        R["visits"][h["code"]] = []
        R["visits27"][h["code"]] = []
        R["dso"][h["code"]] = []
    wb = openpyxl.load_workbook(os.path.join(target, "planned_maintenance_schedule.xlsx"), read_only=True)
    for name in wb.sheetnames:
        rows = list(wb[name].iter_rows(values_only=True))
        head = rows[0]
        if "Visit 1" in head:
            wcol = head.index("Window")
            for r in rows[1:]:
                a, b = r[wcol].split("-")
                for d in r[2:wcol]:
                    if d is None:
                        continue
                    d = d.date() if hasattr(d, "date") else d
                    R["visits"][r[0]].append((from_irish("%s %s" % (d.isoformat(), a), "%Y-%m-%d %H:%M"),
                                              from_irish("%s %s" % (d.isoformat(), b), "%Y-%m-%d %H:%M")))
        else:
            for r in rows[1:]:
                d = r[2].date() if hasattr(r[2], "date") else r[2]
                w = (from_irish("%s %s" % (d.isoformat(), r[3]), "%Y-%m-%d %H:%M"),
                     from_irish("%s %s" % (d.isoformat(), r[4]), "%Y-%m-%d %H:%M"))
                if name.startswith("2027"):
                    R["visits27"][r[0]].append(w)
                elif w[0] < END:
                    R["visits"][r[0]].append(w)
    with open(os.path.join(target, "supply_interruptions_2023-2026.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            R["dso"][r["hub_code"]].append((from_irish(r["interruption_start_irish_time"], "%Y-%m-%d %H:%M"),
                                            from_irish(r["supply_restored_irish_time"], "%Y-%m-%d %H:%M")))
    wb = openpyxl.load_workbook(os.path.join(target, "work_orders_2023-2026.xlsx"), read_only=True)
    kindA = {"PM1": "rc_service", "PM2": "visit"}
    for name in wb.sheetnames:
        rows = list(wb[name].iter_rows(values_only=True))
        head = rows[0]
        for r in rows[1:]:
            d = dict(zip(head, r))
            if "Job ref" in d:
                ser, hub = d["Charger serial"], names[d["Site"]]
                logged = from_irish("%s %s" % (d["Date logged"], d["Time logged"]), "%d/%m/%Y %H:%M")
                code = d["Job type"]
                arrive = from_irish(d["Arrived"], "%d/%m/%Y %H:%M") if d["Arrived"] else None
                done = from_irish(d["Completed"], "%d/%m/%Y %H:%M")
                model = units[serial[ser]]["model"] if ser else None
                if code in kindA:
                    kind = kindA[code]
                elif code == "R2":
                    kind = "hang"
                else:
                    kind = "rc_repair" if model == "RC50" else "fault"
            else:
                ser, hub = d["Asset"], d["Site code"]
                logged = from_irish(d["Logged"], "%d/%m/%Y %H:%M")
                arrive = from_irish(d["Attended"], "%d/%m/%Y %H:%M") if d["Attended"] else None
                done = from_irish(d["Closed"], "%d/%m/%Y %H:%M")
                kind = {"PM-SITE": "visit", "PM-RC50": "rc_service", "CM-RC50": "rc_repair", "CM-NR": "hang", "CM-HW": "fault"}[d["Code"]]
            R["wo"].append(dict(hub=hub, key=serial.get(ser) if ser else None, kind=kind, logged=logged, arrive=arrive, done=done))
    txt = pdf_text(os.path.join(target, "asset_renewal_programme_2027.pdf"))
    for m in re.finditer(r"^\s*(NM\d{3})\s+.+?\s+(\d{2}/\d{2}/\d{4})\s+(Yes|No)\b", txt, re.M):
        code, d, new = m.group(1), m.group(2), m.group(3)
        R["programme"][code] = dict(works=from_irish(d + " 09:30", "%d/%m/%Y %H:%M"), new_unit=new == "Yes")
    n = {}
    with open(os.path.join(target, "charging_sessions_2026.csv"), encoding="utf-8") as f:
        seen = set()
        for r in csv.DictReader(f):
            if r["session_id"] in seen:
                continue
            seen.add(r["session_id"])
            if float(r["energy_kwh"]) > 0:
                n[r["charge_point_id"]] = n.get(r["charge_point_id"], 0) + 1
    days = (END - sec(dt.datetime(2026, 1, 1, tzinfo=UTC))) / 86400.0
    for k, u in R["units"].items():
        if u["model"] == "HX150":
            R["cpd"][k] = n.get(k, 0) / days
    return R
