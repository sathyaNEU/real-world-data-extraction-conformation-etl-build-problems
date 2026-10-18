"""task245 records: the council's hourly export (PM10 at its seven stations, NO2 and NOx at six), the terminal operator's
quarterly PM10 workbook in local clock time, the port's met mast, the network's station register, the analysers'
service log, the operator's deposit-gauge results, and the two files the review does not use (the 2026 report's summary
tables and the background map extract). Every value comes from the simulated year (sim.py); how each system writes it
is drawn here, each from its own seeded stream."""
import datetime as dt

import numpy as np
import pandas as pd

import params as P
import sim

D, H = P.DAYS, P.HOURS
T0 = P.START
STATUS_COUNCIL = {"": "R", "F": "F", "X": "X", "S": "S", "P": "P", "G": "O"}
STATUS_OPERATOR = {"": "OK", "F": "FAULT", "X": "REJECTED", "S": "SERVICE", "P": "POWER", "G": "OFF"}
ALARM = ["Analyser stopped (TEOM status alarm); no data until restarted", "TEOM stopped on a status alarm; station not reporting",
         "Logger alarm: TEOM status, analyser stopped", "Analyser down on a status alarm; restart at the next visit"]
RESTART = ["Filter exchanged, analyser restarted; readings rejected to the end of the day while the mass baseline settles",
           "TEOM filter changed and analyser restarted; rest of the day rejected while the baseline settles",
           "Restarted after the status alarm, new filter fitted; data rejected to midnight",
           "Filter replaced, flows checked, analyser back in service; remainder of the day rejected"]
SERVICE = ["Quarterly service: inlet cleaned, flow and leak checks, %s",
           "Quarterly service; sample inlet cleaned, flow within 2 per cent of set point, leak check passed, %s",
           "Routine quarterly service: inlet, flow and leak checks done, %s"]
POWER = ["Power or telemetry lost at the enclosure", "Station not reporting (power)",
         "Telemetry dropout; logger recovered on its own"]
CALIB = ["NO2 zero and span check (certified span cylinder), within tolerance",
         "Fortnightly zero and span check: response within 2 per cent of the cylinder",
         "NO2 zero/span check against the certified cylinder; no adjustment needed"]
BST_ON = dt.datetime(2027, 3, 28, 1, 0)       # GMT
BST_OFF = dt.datetime(2027, 10, 31, 1, 0)     # GMT


def gmt_end(h):
    """the GMT time at the end of hour h"""
    return T0 + dt.timedelta(hours=int(h) + 1)


def uk_date_time(t):
    """dd/mm/yyyy and hh:mm with the day's last hour written 24:00 against the day it closes"""
    if t.hour == 0 and t.minute == 0:
        d = t - dt.timedelta(days=1)
        return d.strftime("%d/%m/%Y"), "24:00"
    return t.strftime("%d/%m/%Y"), t.strftime("%H:%M")


def fit_hour(code):
    """the first hour (GMT index) converted by the station's new logger"""
    return int((P.NO2_LOGGER_FIT[code] - T0).total_seconds() // 3600)


def local_begin(h):
    """the operator logger's stamp: the start of hour h in UK clock time"""
    t = T0 + dt.timedelta(hours=int(h))
    return t + dt.timedelta(hours=1) if BST_ON <= t < BST_OFF else t


class Records:
    def __init__(self, world):
        self.w = world
        self.X = world["X"]
        self.cause = world["cause"]

    # ---------------------------------------------------------------- the council's export
    def no2_cause(self, code):
        """the NO2 analyser's own hours lost: fortnightly zero and span checks, faults, the station's long outage"""
        i = P.CODES.index(code)
        r = sim.rng(7, i)
        c = np.full(H, "", dtype="<U1")
        for d in range(3 + int(r.integers(0, 4)), D, 14):
            h0 = d * 24 + 10 + int(r.integers(0, 3))
            c[h0:h0 + 2] = "S"
        for _ in range(int(r.integers(1, 4))):
            h0 = int(r.integers(0, H - 60))
            c[h0:h0 + int(r.integers(3, 40))] = "F"
        f = fit_hour(code)
        c[f:f + 2] = "S"                       # the logger change
        return c

    def council_hourly(self):
        rows = []
        stamp = [uk_date_time(gmt_end(h)) for h in range(H)]
        for i, st in enumerate(P.STATIONS):
            code, name, op = st[0], st[1], st[2]
            if op != "TBC":
                continue
            cz = self.cause[i]
            x = self.X[i]
            for h in range(H):
                ok = cz[h] == ""
                rows.append((code, name, "PM10", stamp[h][0], stamp[h][1], "%.1f" % x[h] if ok else "", "ug/m3",
                             STATUS_COUNCIL[cz[h]]))
            if code in P.NO2:
                v, nox = self.w["NO2"][code]
                cn = self.no2_cause(code)
                # the old loggers converted at 1.91; the new ones, from their fitting, at their default of 1.88
                scale = np.where(np.arange(H) >= fit_hour(code), P.NO2_LOGGER_FACTOR / P.NO2_PER_PPB, 1.0)
                block = []
                for pol, ser in (("NO2", v), ("NOx as NO2", nox)):
                    for h in range(H):
                        ok = cn[h] == ""
                        block.append((code, name, pol, stamp[h][0], stamp[h][1], "%.1f" % (ser[h] * scale[h]) if ok else "",
                                      "ug/m3", STATUS_COUNCIL[cn[h]]))
                if code in P.NO2_RESENT:
                    h0, nh = P.NO2_RESENT[code]
                    resent = block[h0:h0 + nh]
                    block = block[:h0 + nh] + resent + block[h0 + nh:]
                rows += block
        return pd.DataFrame(rows, columns=["site_code", "site_name", "pollutant", "date", "time_end", "value", "unit",
                                           "status"])

    def no2_truth(self):
        """each council NO2 station's true annual mean of valid hours (20 C), the ask's figure"""
        out = {}
        for code in P.NO2:
            v, nox = self.w["NO2"][code]
            cn = self.no2_cause(code)
            out[code] = float(v[cn == ""].mean())
        return out

    # ---------------------------------------------------------------- the operator's workbook
    def operator_frames(self):
        """one frame per quarter in the operator logger's clock time (hour beginning), a value and a status column per
        station"""
        ops = [(i, st) for i, st in enumerate(P.STATIONS) if st[2] == "TBT"]
        times = [local_begin(h) for h in range(H)]
        frames = []
        for q in range(4):
            lo = dt.datetime(2027, 3 * q + 1, 1)
            hi = dt.datetime(2027, 3 * q + 4, 1) if q < 3 else dt.datetime(2028, 1, 1)
            idx = [h for h in range(H) if lo <= times[h] < hi]      # the logger's quarters run on its own clock
            data = {"Date/time": [times[h].strftime("%d/%m/%Y %H:%M") for h in idx]}
            for i, st in ops:
                cz = self.cause[i]
                data["%s PM10" % st[1]] = [round(float(self.X[i][h]), 1) if cz[h] == "" else None for h in idx]
                data["%s status" % st[1]] = [STATUS_OPERATOR[cz[h]] for h in idx]
            frames.append(("Q%d 2027" % (q + 1), pd.DataFrame(data)))
        return frames

    # ---------------------------------------------------------------- the met mast
    def met(self):
        W = self.w["W"]
        r = sim.rng(8, 0)
        miss = np.zeros(H, bool)
        for _ in range(9):
            h0 = int(r.integers(0, H - 30))
            miss[h0:h0 + int(r.integers(1, 9))] = True
        rows = []
        for h in range(H):
            t = gmt_end(h).strftime("%Y-%m-%dT%H:%MZ")
            if miss[h]:
                rows.append((t, "", "", "", ""))
                continue
            sp = W["speed"][h]
            wd = "" if sp < 0.5 else "%d" % (int(round(W["theta"][h])) % 360 or 360)
            rows.append((t, wd, "%.1f" % sp, "%.1f" % W["rain"][h], "%.1f" % W["temp"][h]))
        return pd.DataFrame(rows, columns=["datetime_end_gmt", "wind_dir_deg", "wind_speed_ms", "rain_mm", "air_temperature_c"])

    # ---------------------------------------------------------------- the register
    def register(self):
        rows = []
        r = sim.rng(13, 0)
        for st in P.STATIONS:
            code, name, op, typ, x, y = st[:6]
            e = P.STOCKYARD_OS[0] + x + int(r.integers(-35, 36))
            n = P.STOCKYARD_OS[1] + y + int(r.integers(-35, 36))
            no2 = "Chemiluminescence (Teledyne T200)" if code in P.NO2 else ""
            pm = {"TEOM 1405": "TEOM 1405 (FDMS not fitted)", "TEOM 1405-F": "TEOM 1405-F (FDMS)", "Fidas 200": "Fidas 200",
                  "BAM 1020": "BAM 1020 (heated inlet)"}[st[8]]
            opname = "Thornmouth Borough Council" if op == "TBC" else "Thornmouth Bulk Terminal Ltd"
            rows.append((code, name, opname, typ, e, n, pm, no2, 2.5 if op == "TBC" else 3.0))
        return pd.DataFrame(rows, columns=["site_code", "site_name", "operator", "site_type", "easting", "northing",
                                           "pm10_analyser", "no2_analyser", "inlet_height_m"])

    # ---------------------------------------------------------------- deposit gauges
    def deposit_results(self):
        r = sim.rng(9, 0)
        rows = []
        ref = 27001
        for code, a, b, days, rate in self.w["dep"]:
            name = P.NAME[code]
            area = P.GAUGE_AREA_NEW if a >= P.GAUGE_SWITCH else P.GAUGE_AREA_OLD
            total = rate * area * days
            ins = total * r.uniform(0.70, 0.84)
            sol = total - ins
            void = (code == P.GAUGE_VOID[0] and a.month == P.GAUGE_VOID[1] and a.year == 2027)
            lab_rate = total / (P.GAUGE_AREA_OLD * days)
            rows.append(("DG-" + code[-1], name, a.strftime("%d/%m/%Y"), b.strftime("%d/%m/%Y"), days,
                         None if void else round(ins, 1), None if void else round(sol, 1), None if void else round(total, 1),
                         round(P.GAUGE_AREA_OLD, 4), None if void else int(round(lab_rate)), "TL/%d" % ref,
                         "VOID - gauge contaminated (bird)" if void else ""))
            ref += 1
        return pd.DataFrame(rows, columns=["Gauge", "Site", "Date on", "Date off", "Days exposed", "Insoluble (mg)",
                                           "Soluble (mg)", "Total deposit (mg)", "Collecting area (m2)",
                                           "Deposition rate (mg/m2/day)", "Lab ref", "Remarks"])

    def deposit_truth(self):
        """each operator station's true 2027 rate: periods that started in 2027, total deposit over area and days"""
        out = {}
        for code in [s[0] for s in P.STATIONS if s[2] == "TBT"]:
            num = den = 0.0
            for c, a, b, days, rate in self.w["dep"]:
                if c != code or a.year != 2027 or (c == P.GAUGE_VOID[0] and a.month == P.GAUGE_VOID[1]):
                    continue
                num += rate * days
                den += days
            out[code] = num / den
        return out

    # ---------------------------------------------------------------- the service log
    def service_log(self):
        """both technicians' visit records (council stations: council technician; terminal stations: the operator's), in
        UK clock time, one line per visit or call-out"""
        r = sim.rng(10, 0)
        rows = []

        def clock(h):
            t = T0 + dt.timedelta(hours=int(h))
            return t + dt.timedelta(hours=1) if BST_ON <= t < BST_OFF else t
        who = {"TBC": ["R. Slater", "B. Bryan"], "TBT": ["J. Khan", "M. Hussain"]}
        for i, st in enumerate(P.STATIONS):
            code, name, op = st[0], st[1], st[2]
            cz = self.cause[i]
            # faults and restarts
            h = 0
            while h < H:
                if cz[h] == "F" and (h == 0 or cz[h - 1] != "F"):
                    h0 = h
                    while h < H and cz[h] == "F":
                        h += 1
                    t0, t1 = clock(h0), clock(h)
                    rows.append((t0, code, name, "Alarm", "", ALARM[int(r.integers(0, len(ALARM)))]))
                    rows.append((t1, code, name, "Fault visit", who[op][int(r.integers(0, 2))],
                                 RESTART[int(r.integers(0, len(RESTART)))]))
                else:
                    h += 1
            # services
            h = 0
            while h < H:
                if cz[h] == "S" and (h == 0 or cz[h - 1] != "S"):
                    rows.append((clock(h), code, name, "Service", who[op][int(r.integers(0, 2))],
                                 SERVICE[int(r.integers(0, len(SERVICE)))] % ("filter exchanged" if "TEOM" in st[8] else
                                                                              "tape and nozzle checked")))
                h += 1
            # power and telemetry
            h = 0
            while h < H:
                if cz[h] == "P" and (h == 0 or cz[h - 1] != "P"):
                    rows.append((clock(h), code, name, "Alarm", "", POWER[int(r.integers(0, len(POWER)))]))
                h += 1
            if i in self.w["gaps"]:
                g0, gl = self.w["gaps"][i]
                a, b = clock(g0 * 24 + 9), clock((g0 + gl) * 24 + 10)
                if code == "TH5":
                    rows.append((a, code, name, "Site works", who[op][0],
                                 "PM10 inlet and BAM 1020 taken down for the Market Street resurfacing works (scaffold over "
                                 "the enclosure); NO2 analyser left running"))
                    rows.append((b, code, name, "Site works", who[op][0],
                                 "BAM 1020 and inlet refitted after the works; flow and zero checks passed"))
                else:
                    rows.append((a, code, name, "Repair", who[op][1],
                                 "BAM 1020 removed and returned to the supplier for repair (tape transport)"))
                    rows.append((b, code, name, "Repair", who[op][1],
                                 "BAM 1020 refitted after repair; flow and zero checks passed"))
        # the council's NO2 analysers: the logger change in June and the fortnightly checks
        for code in P.NO2:
            i = P.CODES.index(code)
            name = P.NAME[code]
            rows.append((clock(fit_hour(code)), code, name, "Logger", "R. Slater",
                         "New data logger fitted (telemetry upgrade). Channels: PM10 analyser output in ug/m3; NO2 and NOx "
                         "from the T200 in ppb, converted on the logger at 1.88 ug/m3 per ppb"))
            cn = self.no2_cause(code)
            h = 0
            while h < H:
                if cn[h] == "S" and (h == 0 or cn[h - 1] != "S"):
                    rows.append((clock(h), code, name, "Calibration", who["TBC"][int(r.integers(0, 2))],
                                 CALIB[int(r.integers(0, len(CALIB)))]))
                h += 1
        # the operator's deposit gauges
        for a, b in sim.deposit_periods():
            if a.year != 2027:
                continue
            for st in P.STATIONS:
                if st[2] != "TBT":
                    continue
                note = "Deposit gauge exchanged; bottle sent to the laboratory"
                if a == P.GAUGE_SWITCH:
                    note = "BS 1747 gauge taken down; Frisbee deposit gauge fitted on the same post; bottle sent to the laboratory"
                rows.append((dt.datetime(a.year, a.month, a.day, 10, 30), st[0], st[1], "Deposit gauge", who["TBT"][0], note))
        rows.sort(key=lambda x: (x[0], x[1]))
        return pd.DataFrame([(t.strftime("%d/%m/%Y"), t.strftime("%H:%M"), c, n, k, w, note) for t, c, n, k, w, note in rows],
                            columns=["Date", "Time (UK clock)", "Site", "Site name", "Type", "Engineer", "Notes"])

    # ---------------------------------------------------------------- the two files the review does not use
    def no2_2026(self):
        """last year's report: each council NO2 station's 2026 data capture and annual mean"""
        r = sim.rng(11, 0)
        out = {}
        for code in P.NO2:
            v, nox = self.w["NO2"][code]
            out[code] = (float(r.uniform(93.0, 99.2)), float(v.mean() * r.uniform(0.95, 1.07)))
        return out

    def background_map(self):
        """modelled 2027 annual mean background on the national grid's 1 km squares around the town, by source sector"""
        r = sim.rng(12, 0)
        rows = []
        e0, n0 = P.STOCKYARD_OS[0] // 1000 * 1000, P.STOCKYARD_OS[1] // 1000 * 1000
        for e in range(-10, 5):
            for n_ in range(-8, 5):
                xe, yn = e0 + e * 1000 + 500, n0 + n_ * 1000 + 500          # the square's centre
                ce, cn = (xe - P.STOCKYARD_OS[0]) / 1000.0, (yn - P.STOCKYARD_OS[1]) / 1000.0
                d_term = np.hypot(ce, cn)
                d_town = np.hypot(ce + 3.0, cn + 2.8)
                ind = 4.5 * np.exp(-d_term / 1.6) + 0.4
                road = 2.2 * np.exp(-d_town / 2.5) + 0.3
                dom = 1.1 * np.exp(-d_town / 3.5) + 0.4
                sec = 7.6 + 0.08 * cn + r.normal(0, 0.15)
                pm = ind + road + dom + sec
                no2_road = 6.0 * np.exp(-d_town / 2.2) + 1.0
                no2_other = 7.5 + 1.2 * np.exp(-d_term / 2.0) + r.normal(0, 0.2)
                rows.append(("%d" % xe, "%d" % yn, "%.2f" % pm, "%.2f" % ind, "%.2f" % road, "%.2f" % dom,
                             "%.2f" % sec, "%.2f" % (no2_road + no2_other), "%.2f" % no2_road, "%.2f" % no2_other))
        return pd.DataFrame(rows, columns=["x", "y", "pm10_total", "pm10_industrial", "pm10_road",
                                           "pm10_domestic", "pm10_secondary_other", "no2_total", "no2_road", "no2_other"])
