"""task231 architecture 2: write target/ from the world. Each file in the producing system's own layout."""
import csv
import datetime as dt
import io
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font

import params as P
import postprocess as PP
import world as Wd

STATUS_TABLE = {
    "3.4": {"dry": 1, "moist": 2, "wet": 3, "chemically wet": 4, "snow": 5, "ice warning": 6, "ice watch": 7, "frost": 8},
    "4.1": {"dry": 1, "moist": 2, "wet": 3, "chemically wet": 4, "ice warning": 5, "ice watch": 6, "frost": 7, "snow": 8},
}


def write_csv(path, header, rows):
    buf = io.StringIO(newline="")
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(header)
    w.writerows(rows)
    open(path, "w", encoding="utf-8", newline="").write(buf.getvalue())


def iso_z(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def utc_of_min(m):
    return P.WIN_START_UTC + dt.timedelta(minutes=float(m))


def local_str(u):
    l, z = Wd.local_of(u)
    return l.strftime("%Y-%m-%d %H:%M:%S") + " " + z


def obs_time(h):
    return P.WIN_START_UTC + dt.timedelta(hours=int(h) + 1)


def FW_MIN(ser):
    # the minute in the hour the technician's upgrade finished; the hour's reading carries the new code table
    return 7 + int(ser[2:]) % 46


def save_xlsx(wb, path, creator, last_by, created, modified):
    wb.save(path)
    PP.normalize_ooxml(path, creator, last_by, created, modified, excel=True, company=P.ORG)


def feed(W, path):
    rows = []
    kinds = {}
    for t, rec, kind, a, b, hs in W["msgs"]:
        for h in hs:
            kinds.setdefault((t, h), []).append("repoll" if kind == "REPOLL" else "scheduled")
    for i, t in enumerate(P.TAGS):
        for h in range(P.NH):
            ks = kinds.get((t, h))
            if not ks:
                continue
            v = W["read"][i, h]
            dew = W["dew"][i, h]
            dval = "1001" if (t == "G2" and 3600 <= h < 3790) else str(int(round(dew * 10)))
            row = [P.RPU[t], iso_z(obs_time(h)), str(int(round(v * 10))), dval, str(int(W["rh"][i, h])),
                   str(int(round(W["wind"][i, h] * 10))), str(int(W["wdir"][i, h]))]
            rows.append(row + [ks[0]])
            for k in ks[1:2]:
                rows.append(row + [k])
    write_csv(path, ["rpu_id", "obs_time_utc", "essAirTemperature", "essDewpointTemp", "essRelativeHumidity",
                     "essAvgWindSpeed", "essAvgWindDirection", "poll"], rows)
    return len(rows)


RELEASE_432 = dt.datetime(2027, 1, 12, 17, 0)      # QC release 4.3.2 went live (UTC)


def qc_log(W, path):
    """One row per reading a test withheld, logged at the QC run that checked it (20 minutes past each hour)."""
    rows = []
    for i, t in enumerate(P.TAGS):
        have = W["have"][i]
        prev = None
        for h in range(P.NH):
            if not have[h]:
                continue
            run = W["qc_run"][i, h]
            logged = utc_of_min(run) + dt.timedelta(seconds=4 + (h * 7919 + i * 104729) % 47)
            rel = "4.3.0" if logged < RELEASE_432 else "4.3.2"
            v = W["read"][i, h]
            ob = iso_z(obs_time(h))
            if prev is not None and prev == h - 1 and abs(v - W["read"][i, h - 1]) > P.STEP_LIMIT_C:
                rows.append((logged, P.SITE[t], [ob, "air_temperature", "step", "%.1f" % v, "%.1f" % W["read"][i, h - 1],
                                                 "%.1f" % (v - W["read"][i, h - 1]), rel, iso_z(logged)]))
            if W["spatial"][i, h]:
                est = W["est"][i, h]
                rows.append((logged, P.SITE[t], [ob, "air_temperature", "spatial", "%.1f" % v, "%.1f" % est,
                                                 "%.1f" % (v - est), rel, iso_z(logged)]))
            if t == "G2" and 3600 <= h < 3790:
                rows.append((logged, P.SITE[t], [ob, "dew_point", "range", "100.1", "", "", rel, iso_z(logged)]))
            prev = h
    rows.sort(key=lambda r: (r[0], r[1]))
    out = [[site] + rest for _, site, rest in rows]
    write_csv(path, ["site_code", "obs_time", "parameter", "test", "value_c", "estimate_c", "deviation_c",
                     "qc_release", "logged_at"], out)
    return len(out)


def register(W, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Sites"
    hdr = ["Site code", "RPU", "Site name", "Route", "Milepost", "Latitude", "Longitude", "Elevation (ft)",
           "Elevation (m)", "Air temperature sensor", "Maintenance section", "Commissioned"]
    ws.append(hdr)
    for c in ws[1]:
        c.font = Font(bold=True)
    comm = {t: dt.date(2014 + (k * 7) % 9, 1 + (k * 5) % 12, 1 + (k * 11) % 27) for k, t in enumerate(P.TAGS)}
    for s in sorted(P.STATIONS, key=lambda s: s[1]):
        t = s[0]
        lat = round(P.LAT0 + s[7] * P.KM_LAT, 5)
        lon = round(P.LON0 + s[6] * P.KM_LON, 5)
        ws.append([s[1], s[2], s[3], s[4], s[5], lat, lon, int(round(s[8] * 3.28084)), s[8],
                   "HMP155" if s[0] not in ("R2", "R6", "Q4") else "HMP110", s[10], comm[t]])
    ws2 = wb.create_sheet("Pavement sensors")
    ws2.append(["Site code", "RPU", "Port", "Lane", "Sensor serial", "Model", "Surface temperature reported in",
                "Installed", "Note"])
    for c in ws2[1]:
        c.font = Font(bold=True)
    installed_old = {}
    for (t, lane, ser, model, a, b, port) in W["sensors"]:
        if b < P.NH:
            installed_old[(t, lane)] = ser
    for (t, lane, ser, model, a, b, port) in W["sensors"]:
        if b < P.NH:
            continue
        units = "tenths of a degree C" if model == "IRS-31" else "degrees F"
        inst = (Wd.local_of(obs_time(a - 1))[0].date() if a > 0 else
                dt.date(2015 + (len(ser) + int(ser[-2:])) % 8, 1 + int(ser[-1]) % 12, 3 + int(ser[-3]) % 24))
        note = None
        if (t, lane) in installed_old:
            # the register is kept by sensor in service: a head that came out leaves only its work order behind
            note = "WO-27-%04d, %s" % (113 + 37 * P.TAGS.index(t) % 400, {"K3": "sensor head cracked by plow",
                                                                         "N2": "heater failure",
                                                                         "P3": "lightning damage",
                                                                         "Q1": "heater failure"}[t])
        elif lane == "bridge deck":
            note = "deck sensor, %s span" % ("north" if int(ser[-1]) % 2 else "south")
        ws2.append([P.SITE[t], P.RPU[t], port, lane, ser, model, units, inst, note])
    ws3 = wb.create_sheet("Firmware")
    ws3.append(["Sensor serial", "Firmware", "Applied"])
    for c in ws3[1]:
        c.font = Font(bold=True)
    for ser, h in sorted(W["fw_change"].items(), key=lambda kv: (kv[1], kv[0])):
        ws3.append([ser, "4.1", Wd.local_of(obs_time(h - 1) + dt.timedelta(minutes=FW_MIN(ser)))[0].strftime(
            "%Y-%m-%d %H:%M")])
    ws4 = wb.create_sheet("Status codes")
    ws4.append(["Code table", "Code", "Surface status"])
    for c in ws4[1]:
        c.font = Font(bold=True)
    for tab, label in (("3.4", "IRS-31 firmware 3.4; SCAN-16"), ("4.1", "IRS-31 firmware 4.1")):
        for name, code in sorted(STATUS_TABLE[tab].items(), key=lambda kv: kv[1]):
            ws4.append([label, code, name])
    for w_, widths in ((ws, [10, 9, 22, 8, 9, 10, 11, 14, 13, 22, 19, 13]), (ws2, [10, 9, 6, 12, 13, 9, 28, 11, 52]),
                       (ws3, [13, 9, 17]), (ws4, [30, 7, 18])):
        for k, wd in enumerate(widths):
            w_.column_dimensions[chr(65 + k)].width = wd
    save_xlsx(wb, path, P.PEOPLE["engineer"][0], P.PEOPLE["engineer"][0], "2019-04-02T16:20:00Z",
              "2027-05-11T22:41:00Z")


def messages(W, path, mpath):
    imei_at = {}
    rows = []
    mid = 4183000
    for k, (t, rec, kind, a, b, hs) in enumerate(W["msgs"]):
        mid += 1 + (k * 37 + a) % 4
        u = utc_of_min(rec)
        im = W["imei"][t]
        if t in W["swaps"] and a >= W["swaps"][t][0]:
            im = W["swaps"][t][1]
        if t in W["spare"] and W["spare"][t][0] <= a < W["spare"][t][1]:
            im = W["spare"][t][2]
        rows.append([str(mid), im, local_str(u), kind, iso_z(obs_time(a)), iso_z(obs_time(b)), str(len(hs))])
    write_csv(path, ["message_id", "modem_imei", "server_received", "kind", "first_obs_utc", "last_obs_utc",
                     "records"], rows)
    wb = Workbook()
    ws = wb.active
    ws.title = "Modems"
    ws.append(["IMEI", "Carrier", "Site code", "Installed", "Removed", "Note"])
    for c in ws[1]:
        c.font = Font(bold=True)
    lst = []
    for k, t in enumerate(P.TAGS):
        car = "Mountain West Wireless" if k % 3 else "Treasure State Cellular"
        if t in W["swaps"]:
            h, new = W["swaps"][t]
            day = Wd.local_of(obs_time(h - 1))[0].date()
            gone = Wd.local_of(obs_time(W["spare"][t][0] - 1))[0].date() if t in W["spare"] else day
            lst.append([W["imei"][t], car, P.SITE[t], dt.date(2020, 5, 4 + k % 20), gone, "antenna lead fault"])
            lst.append([new, car, P.SITE[t], day, None, None])
        else:
            lst.append([W["imei"][t], car, P.SITE[t], dt.date(2020, 5, 4 + k % 20), None, None])
    lst.append(["358713046622913", "Treasure State Cellular", None, dt.date(2024, 9, 17), None, "spare, Ashby yard"])
    lst.append(["359441205583076", "Mountain West Wireless", None, dt.date(2025, 6, 2), None, "spare, district shop"])
    for row in sorted(lst, key=lambda r: (r[3], r[0])):
        ws.append(row)
    for k, wd in enumerate([18, 24, 10, 12, 12, 22]):
        ws.column_dimensions[chr(65 + k)].width = wd
    save_xlsx(wb, mpath, P.PEOPLE["engineer"][0], P.PEOPLE["engineer"][0], "2020-05-01T15:02:00Z",
              "2027-04-28T19:13:00Z")
    return len(rows)


def outages(W, path):
    rows = []
    for k, (t, a, b, work) in enumerate(W["notices"]):
        rows.append(["SDHD-RW-%04d" % (311 + 9 * k + k * k % 5), P.SITE[t], P.NAME[t],
                     local_str(P.WIN_START_UTC + dt.timedelta(hours=a)), local_str(P.WIN_START_UTC + dt.timedelta(hours=b)),
                     work])
    write_csv(path, ["notice_no", "site_code", "site_name", "starts", "ends", "work"], rows)


def pavement(W, path):
    rows = []
    for (t, lane, ser, model, a, b, port) in W["sensors"]:
        sv = W["surf"][(t, lane)]
        st = W["status"][(t, lane)]
        fw_h = W["fw_change"].get(ser)
        for h in range(a, b):
            if not W["have"][P.TAGS.index(t), h]:
                continue
            tab = "4.1" if (model == "IRS-31" and fw_h is not None and h >= fw_h) else "3.4"
            code = STATUS_TABLE[tab][st[h]]
            stamp = local_str(obs_time(h))
            if model == "IRS-31":
                temp = str(int(round(sv[h] * 10)))
            else:
                temp = "%.1f" % (sv[h] * 9 / 5 + 32)
            row = [P.RPU[t], ser, str(port), stamp, temp, str(code)]
            # a re-polled or re-sent RPU message carries the pavement block again
            for k in range(min(2, W["deliveries"][P.TAGS.index(t), h])):
                rows.append((t, port, h, row))
    rows.sort(key=lambda r: (P.RPU[r[0]], r[1], r[2]))
    write_csv(path, ["rpu_id", "sensor_serial", "port", "obs_time", "surface_temperature", "surface_status_code"],
              [r[3] for r in rows])
    return len(rows)


def preseason(W, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Air temperature"
    ws.append(["Site code", "Site name", "Checked on", "Reference thermometer (C)", "Station sensor (C)",
               "Difference (C)", "Technician"])
    for c in ws[1]:
        c.font = Font(bold=True)
    tech = ["L. Dalton", "K. Phillips", "L. Dalton", "J. Howard", "K. Phillips"]
    for k, (t, day, ref, st) in enumerate(sorted(W["preseason"], key=lambda r: (r[1], P.SITE[r[0]]))):
        ws.append([P.SITE[t], P.NAME[t], day, ref, st, round(st - ref, 2), tech[(k * 3 + day.day) % 5]])
    for k, wd in enumerate([10, 22, 12, 24, 18, 14, 12]):
        ws.column_dimensions[chr(65 + k)].width = wd
    save_xlsx(wb, path, P.PEOPLE["engineer"][0], "Kathy Phillips", "2026-09-21T14:05:00Z", "2026-10-02T20:31:00Z")


def nwp(W, path):
    rows = []
    for h in range(0, P.NH, 3):
        v = obs_time(h)
        run = v - dt.timedelta(hours=6 + (v.hour % 6))
        for i, t in enumerate(P.TAGS):
            rows.append([iso_z(run), iso_z(v), P.SITE[t], "%.1f" % W["nwp"][i, h]])
    write_csv(path, ["run_utc", "valid_utc", "site_code", "t2m_c"], rows)


def traffic(W, path):
    rows = [[a, r, "%.1f" % m, d.isoformat(), str(v)] for a, r, m, d, v in W["atr"]]
    write_csv(path, ["atr_station", "route", "milepost", "date", "volume"], rows)


def write_all(W, target):
    os.makedirs(target, exist_ok=True)
    f = {k: os.path.join(target, v) for k, v in P.FILES.items()}
    n_feed = feed(W, f["feed"])
    qc_log(W, f["qc"])
    register(W, f["register"])
    n_msg = messages(W, f["messages"], f["modems"])
    outages(W, f["outages"])
    n_pav = pavement(W, f["pavement"])
    preseason(W, f["preseason"])
    nwp(W, f["nwp"])
    traffic(W, f["traffic"])
    return {"feed_rows": n_feed, "message_rows": n_msg, "pavement_rows": n_pav}
