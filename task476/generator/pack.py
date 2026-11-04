"""Write the pack under target/ from the simulated truth: the utility's two exports, the register, the totalizer reads,
the logger files and their download log, the pump test reports, the agency's notice and template, the tariff and the
rate letter, and the two distractors. Each file is written the way its producing system writes it."""
import csv
import datetime as dt
import io
import math
import os

import numpy as np

import world as W
import sim as S

QMIN = dt.timedelta(minutes=15)


def _rows_csv(path, header, rows, crlf=False, pre=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    buf = io.StringIO()
    if pre:
        for line in pre:
            buf.write(line + ("\r\n" if crlf else "\n"))
    wr = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    if header:
        wr.writerow(header)
    n = 0
    for r in rows:
        wr.writerow(r)
        n += 1
    open(path, "w", newline="", encoding="utf-8").write(buf.getvalue())
    return n


def qtime(q):
    return W.T0 + q * QMIN


def q_index(t):
    return int((t - W.T0).total_seconds() // 900)


# ----------------------------------------------------------------------------------------------- utility exports
def power_old(x, path):
    """Hourly usage in local prevailing time, START and END TIME on the clock face: the fall-back hour appears twice,
    the spring-forward hour not at all. Estimated hours carry the utility's estimate (the mean of the same hour on the
    two days either side)."""
    rng = np.random.default_rng(W.SEED + 301)
    rows = []
    q0 = q_index(dt.datetime(2025, 9, 1, tzinfo=W.LA).astimezone(W.PST))
    q1 = q_index(W.CUTOVER_UTC.astimezone(W.PST))
    est_days = {w: set(int(d) for d in rng.choice(np.arange(10, 200), size=int(rng.integers(0, 3)), replace=False))
                for w in W.WELLS}
    for w in W.WELLS:
        k = x[w]["kwh_q"].reshape(-1)
        for q in range(q0, q1, 4):
            t_loc = qtime(q).astimezone(W.LA)
            kwh = float(k[q:q + 4].sum())
            note = ""
            day = (q - q0) // 96
            if day in est_days[w] and 9 <= t_loc.hour <= 14:
                prev = float(k[q - 96 * 2:q - 96 * 2 + 4].sum()) if q - 192 >= 0 else kwh
                nxt = float(k[q + 192:q + 196].sum()) if q + 196 < len(k) else kwh
                kwh, note = (prev + nxt) / 2.0, "Estimated"
            rows.append((W.SA_OLD[w], "Electric usage", t_loc.strftime("%Y-%m-%d"), t_loc.strftime("%H:%M"),
                         t_loc.strftime("%H") + ":59", "%.2f" % kwh, "kWh", note))
    pre = ["Name,OCHRE FLATS FARMING CO", "Address,\"6120 W SALLOW PLAINS RD, OCHRE FLATS CA\"",
           "Account Number,7735102846", "Service,Agricultural electric (all service agreements)", ""]
    return _rows_csv(path, ["SERVICE AGREEMENT", "TYPE", "DATE", "START TIME", "END TIME", "USAGE", "UNITS", "NOTES"],
                     rows, crlf=True, pre=pre)


def power_new(x, path):
    """Fifteen-minute energy in watt-hours from the new customer portal, interval start in UTC."""
    rows = []
    q0 = q_index(W.CUTOVER_UTC.astimezone(W.PST))
    q1 = q_index(W.T1)
    rng = np.random.default_rng(W.SEED + 302)
    for w in W.WELLS:
        k = x[w]["kwh_q"].reshape(-1)
        gap = int(rng.integers(q0 + 96 * 20, q1 - 96 * 20)) if rng.random() < 0.5 else -1
        for q in range(q0, q1):
            t_utc = qtime(q).astimezone(W.UTC)
            wh = int(round(k[q] * 1000))
            qual = "EST" if gap <= q < gap + 8 else "ACT"
            rows.append((W.SA_NEW[w], t_utc.strftime("%Y-%m-%dT%H:%M:%SZ"), 900, wh, qual))
    return _rows_csv(path, ["service_agreement_id", "interval_start", "interval_seconds", "energy_wh", "quality"], rows)


# ----------------------------------------------------------------------------------------------- loggers
def logger_files(x, out):
    """One file per logger serial, as each instrument's software exports it, every 15 minutes on Pacific standard
    time; the shop barologger on the same schedule, its clock on UTC."""
    n = {}
    q0 = q_index(W.PACK_START)
    QH = 4 * W.NH
    serials = {}
    for w in W.WELLS:
        for q in range(q0, QH):
            s = W.logger_at(w, qtime(q))
            serials.setdefault(s, []).append((q, w))
    baro = x["_baro"]
    for s, pts in sorted(serials.items()):
        pts.sort()
        absolute = any(w in W.METERED for _, w in pts)
        if absolute:
            first_w = pts[0][1]          # the location field set at launch, not changed when the logger moved
            pre = ["Serial_number:", s, "Project ID:", "Ochre Flats", "Location:", W.P[first_w]["name"].split(" (")[0],
                   "LEVEL", "UNIT: ft", "Offset: 0.000000 ft", "Density: 1.000 kg/L", "TEMPERATURE", "UNIT: Deg C"]
            rows = []
            for q, w in pts:
                p = W.P[w]
                dtw_mp = x[w]["lvl"][q] + p["stick"]
                level = (p["sensor"] - dtw_mp) + baro[q]
                t = qtime(q)
                rows.append((t.strftime("%Y/%m/%d"), t.strftime("%H:%M:%S"), 0, "%.4f" % level,
                             "%.3f" % (18.6 + 1.2 * math.sin(2 * math.pi * q / 35064.0))))
            n[s] = _rows_csv(os.path.join(out, W.logger_file(s)), ["Date", "Time", "ms", "LEVEL", "TEMPERATURE"],
                             rows, crlf=True, pre=pre)
        else:
            w = pts[0][1]
            p = W.P[w]
            pre = ["Log File Name : OF_%s_2026-11-01" % p["name"].split(" (")[0].replace(" ", ""),
                   "Report Date : 11/1/2026 9:42:17 AM", "Report User Name : mwalter",
                   "Device : Level TROLL 500 Vented", "Serial Number : %s" % s,
                   "Site : %s" % p["name"].split(" (")[0],
                   "Time Zone : (UTC-08:00) Pacific Standard Time, daylight saving not applied",
                   "Level Reference : Depth to Water below top of sounding tube, set 2025-03-12 from manual sounding",
                   ""]
            rows = []
            for q, ww in pts:
                t = qtime(q)
                rows.append((t.strftime("%Y-%m-%d %H:%M:%S"), "%.2f" % (x[ww]["lvl"][q] + W.P[ww]["stick"]),
                             "%.2f" % (21.4 + 0.6 * math.sin(2 * math.pi * q / 35064.0))))
            n[s] = _rows_csv(os.path.join(out, W.logger_file(s)),
                             ["Date Time", "Depth to Water (ft) (%s)" % s, "Temperature (C) (%s)" % s], rows, pre=pre)
    pre = ["Serial_number:", W.BARO, "Project ID:", "Ochre Flats", "Location:", "Shop barologger", "LEVEL",
           "UNIT: ft", "Offset: 0.000000 ft", "Altitude: 245 ft", "TEMPERATURE", "UNIT: Deg C"]
    rows = []
    for q in range(q0, QH):
        t = qtime(q).astimezone(W.UTC)
        rows.append((t.strftime("%Y/%m/%d"), t.strftime("%H:%M:%S"), 0, "%.4f" % baro[q], "%.3f" % 22.0))
    n[W.BARO] = _rows_csv(os.path.join(out, W.FILES["baro"]), ["Date", "Time", "ms", "LEVEL", "TEMPERATURE"], rows,
                          crlf=True, pre=pre)
    return n


def download_log(x, path):
    """The ranch technician's download visits: each logger read out, a manual sounding from the top of the sounding
    tube with the pump state at the time, and the June 2026 swap of the two Levelogger 5 units at Pumps 2 and 5."""
    rng = np.random.default_rng(W.SEED + 303)
    rows = []
    visits = [dt.datetime(2025, 9, 1, 8, tzinfo=W.PST) + dt.timedelta(days=int(d)) for d in
              (0, 47, 96, 152, 196, 230, 282, 330, 372, 425)]
    swap_day = W.SWAP_DATE.date()
    if all(v.date() != swap_day for v in visits):
        visits.append(W.SWAP_DATE.replace(hour=8))
    visits.sort()
    for v in visits:
        for i, w in enumerate(W.WELLS):
            t = v + dt.timedelta(minutes=14 * i)
            q = int((t - W.T0).total_seconds() // 900)
            if q >= 4 * W.NH:
                continue
            s = W.logger_at(w, t)
            running = bool(x[w]["on"][q])
            sound = x[w]["lvl"][q] + W.P[w]["stick"] + rng.normal(0, 0.05)
            action = "downloaded, relaunched"
            note = "clock set from field laptop, PST (UTC-08:00), no daylight saving"
            if t.date() == swap_day and w in W.SWAP:
                other = W.SWAP[1] if w == W.SWAP[0] else W.SWAP[0]
                s_new = W.LOGGER_NOW[w]
                action = "downloaded; logger moved to %s; %s installed from %s" % (
                    W.P[other]["name"].split(" (")[0], s_new, W.P[other]["name"].split(" (")[0])
                note = "relaunched at new site, location field not changed; clock set from field laptop, PST " \
                       "(UTC-08:00), no daylight saving"
            rows.append((t.astimezone(W.LA).strftime("%Y-%m-%d %H:%M"), "J. Cox", W.P[w]["name"].split(" (")[0], s,
                         action, "%.2f" % sound, "running" if running else "off", note))
        tb = v + dt.timedelta(minutes=14 * len(W.WELLS) + 25)
        if int((tb - W.T0).total_seconds() // 3600) < W.NH:
            rows.append((tb.astimezone(W.LA).strftime("%Y-%m-%d %H:%M"), "J. Cox", "Shop", W.BARO,
                         "downloaded at office PC, relaunched", "", "",
                         "barologger clock synced to office PC (UTC)"))
    return _rows_csv(path, ["visit_local", "tech", "site", "logger_sn", "action", "manual_dtw_ft_below_mp",
                            "pump_at_sounding", "note"], rows)


# ----------------------------------------------------------------------------------------------- meters
METER_UNITS = {"W-01": ("21-40977", "acre-feet", 1.0), "W-02": ("21-40983", "gal x 1000", W.AF_GAL / 1000.0),
               "W-03": ("3118842", "gal x 100", W.AF_GAL / 100.0), "W-04": ("22-01155", "acre-feet", 1.0)}
NEW_W03 = ("3302157", "gal x 1000", W.AF_GAL / 1000.0)
REPLACE_W03 = dt.datetime(2026, 6, 17, 10, 20, tzinfo=W.LA)


def meter_reads(x):
    """Monthly reads on the first of the month by the ranch's irrigator, the totalizer registering within about a
    per cent of the water; six-digit registers roll over; W-03's meter exchanged in June 2026."""
    rng = np.random.default_rng(W.SEED + 501)
    rows = []
    start_reg = {"W-01": 1843.27, "W-02": 912_455, "W-03": 731_208, "W-04": 1295.61}
    for w in W.METERED:
        sn, unit, per_af = METER_UNITS[w]
        reg_f = float(rng.uniform(0.988, 1.008))
        cum = np.cumsum(x[w]["af_q"].reshape(-1)) * reg_f
        reads = [dt.datetime(2025, 9, 1, tzinfo=W.LA)]
        while reads[-1] < dt.datetime(2026, 10, 1, tzinfo=W.LA):
            r = reads[-1]
            reads.append(dt.datetime(r.year + (r.month == 12), r.month % 12 + 1, 1, tzinfo=W.LA))
        q_x = q_index(REPLACE_W03.astimezone(W.PST))
        for day in reads:
            t = day.replace(hour=int(rng.integers(7, 10)), minute=int(rng.integers(0, 60)))
            q = min(q_index(t.astimezone(W.PST)), len(cum) - 1)
            vol = float(cum[q])
            if w == "W-03" and t >= REPLACE_W03:
                v_new = (vol - float(cum[q_x])) * NEW_W03[2]
                rows.append((w, NEW_W03[0], t.strftime("%Y-%m-%d"), t.strftime("%H:%M"), int(round(v_new)), NEW_W03[1],
                             "AR", ""))
                continue
            if per_af == 1.0:
                val = round(start_reg[w] + vol, 2)
            else:
                val = int(round(start_reg[w] + vol * per_af)) % 1_000_000
            rows.append((w, sn, t.strftime("%Y-%m-%d"), t.strftime("%H:%M"), val, unit, "AR", ""))
            if w == "W-03" and day.month == 6 and day.year == 2026:
                fin = int(round(start_reg[w] + float(cum[q_x]) * per_af)) % 1_000_000
                rows.append((w, sn, REPLACE_W03.strftime("%Y-%m-%d"), REPLACE_W03.strftime("%H:%M"), fin, unit, "JC",
                             "final read, meter removed (register failing)"))
                rows.append((w, NEW_W03[0], REPLACE_W03.strftime("%Y-%m-%d"), REPLACE_W03.strftime("%H:%M"), 0,
                             NEW_W03[1], "JC", "new meter installed"))
    rows.sort(key=lambda r: (r[2], r[3], r[0]))
    return rows


# ----------------------------------------------------------------------------------------------- distractors
def district(path):
    rng = np.random.default_rng(W.SEED + 601)
    rows = []
    months = [(2025, m) for m in (10, 11, 12)] + [(2026, m) for m in range(1, 10)]
    for tn, share in (("ASWD-14A", 0.42), ("ASWD-14B", 0.33), ("ASWD-22C", 0.25)):
        for y, m in months:
            base = {10: 120, 11: 40, 12: 0, 1: 0, 2: 25, 3: 160, 4: 310, 5: 420, 6: 380, 7: 300, 8: 210, 9: 150}[m]
            ordered = round(base * share * rng.uniform(0.85, 1.15), 1)
            deliv = round(ordered * rng.uniform(0.93, 1.0), 1) if ordered else 0.0
            rows.append(("OCHRE FLATS FARMING CO", tn, "%d-%02d" % (y, m), ordered, deliv,
                         "Class 1" if m in (3, 4, 5, 6) else "Class 2"))
    return _rows_csv(path, ["water_user", "turnout", "month", "ordered_af", "delivered_af", "allotment_class"], rows)


def cimis(path):
    rng = np.random.default_rng(W.SEED + 602)
    rows = []
    d = dt.date(2025, 9, 1)
    while d <= dt.date(2026, 10, 31):
        doy = d.timetuple().tm_yday
        eto = max(0.02, 0.17 + 0.14 * math.cos(2 * math.pi * (doy - 182) / 365.25) + rng.normal(0, 0.012))
        tmax = 76 + 22 * math.cos(2 * math.pi * (doy - 200) / 365.25) + rng.normal(0, 4)
        tmin = tmax - 26 + rng.normal(0, 3)
        pr = round(max(0.0, rng.normal(-0.25, 0.22)) if d.month in (11, 12, 1, 2, 3) else 0.0, 2)
        rows.append((247, "Sallow Plains West", "%d/%d/%d" % (d.month, d.day, d.year), doy, "%.2f" % eto, "",
                     "%.2f" % pr, "", "%.1f" % tmax, "", "%.1f" % tmin, "", "%.1f" % (4 + rng.gamma(2, 1.1)), ""))
        d += dt.timedelta(days=1)
    return _rows_csv(path, ["Stn Id", "Stn Name", "Date", "Jul", "ETo (in)", "qc", "Precip (in)", "qc",
                            "Max Air Temp (F)", "qc", "Min Air Temp (F)", "qc", "Avg Wind Speed (mph)", "qc"], rows)


MONTHS = ["oct_2025", "nov_2025", "dec_2025", "jan_2026", "feb_2026", "mar_2026", "apr_2026", "may_2026", "jun_2026",
          "jul_2026", "aug_2026", "sep_2026"]
RETURN_HEAD = ["agency_well_id", "state_well_no", "apn", "aquifer", "method"] + ["%s_af" % m for m in MONTHS] + \
    ["wy2026_af", "spring_2026_static_dtw_ft", "fall_2026_static_dtw_ft"]


def template(path):
    rows = [[W.P[w]["gid"], W.P[w]["swn"], W.P[w]["apn"], W.P[w]["aq"].upper()] + [""] * (len(RETURN_HEAD) - 4)
            for w in sorted(W.WELLS, key=lambda k: W.P[k]["gid"])]
    return _rows_csv(path, RETURN_HEAD, rows, crlf=True)


# ----------------------------------------------------------------------------------------------- the whole pack
def build_pack(out, x):
    import shutil
    import docs as D
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    for k in W.FILES:
        os.makedirs(os.path.dirname(f(k)), exist_ok=True)
    os.makedirs(os.path.join(out, "pump_tests"), exist_ok=True)
    n = {}
    n["power_old"] = power_old(x, f("power_old"))
    n["power_new"] = power_new(x, f("power_new"))
    n.update({"logger_%s" % k: v for k, v in logger_files(x, out).items()})
    n["download_log"] = download_log(x, f("download_log"))
    n["district"] = district(f("district"))
    n["cimis"] = cimis(f("cimis"))
    n["template"] = template(f("template"))
    stamps = []
    for w in W.WELLS:
        t = x["_tests"][w]
        path = os.path.join(out, W.test_file(t["job"]))
        (D.write_test_a if t["tester"] == W.TESTER_A else D.write_test_b)(path, w, t, W.SA_OLD[w])
        stamps.append((path, (t["t"] + dt.timedelta(days=6)).astimezone(W.LA)))
    for w, t in D.superseded_tests().items():
        path = os.path.join(out, W.test_file(t["job"]))
        (D.write_test_a if t["tester"] == W.TESTER_A else D.write_test_b)(path, w, t, "%010d" % (int(W.SA_OLD[w]) - 17),
                                                                          superseded=True)
        stamps.append((path, (t["t"] + dt.timedelta(days=5)).astimezone(W.LA)))
    D.write_notice(f("notice"), None)
    stamps.append((f("notice"), dt.datetime(2026, 10, 15, 14, 22, 9, tzinfo=W.LA)))
    D.write_tariff(f("tariff"))
    stamps.append((f("tariff"), dt.datetime(2026, 2, 18, 9, 4, 51, tzinfo=W.LA)))
    D.write_rate_letter(f("rate_letter"))
    stamps.append((f("rate_letter"), dt.datetime(2026, 5, 14, 11, 37, 2, tzinfo=W.LA)))
    for path, when in stamps:
        off = "-07'00'" if when.utcoffset() == dt.timedelta(hours=-7) else "-08'00'"
        s = (when.strftime("D:%Y%m%d%H%M%S") + off).encode()
        PP.normalize_pdf(path, s, s)
    D.write_register(f("register"))
    PP.normalize_ooxml(f("register"), W.WATER_MANAGER, W.WATER_MANAGER, "2024-03-11T17:20:00Z", "2026-10-28T22:41:13Z",
                       excel=True, company=W.COMPANY)
    reads = meter_reads(x)
    D.write_meters(f("meters"), reads)
    PP.normalize_ooxml(f("meters"), W.WATER_MANAGER, W.WATER_MANAGER, "2025-09-02T16:05:00Z", "2026-11-02T16:48:30Z",
                       excel=True, company=W.COMPANY)
    n["meters"] = len(reads)
    return n
