"""The independent verifier. It reads target/ and figures.json and nothing the generator holds: its own parse of
every file, the certificates read from their PDF, the LoRa gateway's UK clock converted through the Europe/London
zone rules, the decay-bound test written from its physics (a centred running median from pandas' own quantile,
the step tested on the excess), the procedure's rain screen written from its words, the kit's source rebuilt from
the register's entries, and the air drawn integrated from the controller's measured flow."""
import csv
import datetime as dt
import json
import os
import re
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from pypdf import PdfReader

LONDON = ZoneInfo("Europe/London")
UTC = dt.timezone.utc
Q0 = dt.datetime(2026, 7, 1, tzinfo=UTC)
NI = 92 * 144
N = [0]


def check(label, cond, detail=""):
    if not cond:
        raise AssertionError("verify %s FAILED %s" % (label, detail))
    N[0] += 1


def slot(stamp):
    t = dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    return int((t - Q0).total_seconds() // 600)


def local_to_utc(s, fmt):
    return dt.datetime.strptime(s, fmt).replace(tzinfo=LONDON).astimezone(UTC)


def sheet_rows(path, name):
    wb = load_workbook(path, read_only=True, data_only=True)
    rows = list(wb[name].iter_rows(values_only=True))
    wb.close()
    return rows[0], rows[1:]


def export(tgt):
    df = pd.read_csv(os.path.join(tgt, "mvgn_dose_rate_10min_2026Q3.csv"), dtype=str, keep_default_na=False)
    df = df.drop_duplicates()
    check("one row per station interval after exact duplicates", not df.duplicated(["station_code",
                                                                                   "interval_start_utc"]).any())
    val = {}; st = {}
    for code, grp in df.groupby("station_code"):
        v = np.full(NI, np.nan); s = np.full(NI, "", dtype="<U1")
        k = grp["interval_start_utc"].map(slot).values
        x = pd.to_numeric(grp["dose_rate"].replace("", np.nan)).values
        x = np.where(grp["dose_rate_unit"].values == "uSv/h", x * 1000.0, x)
        v[k] = x; s[k] = grp["status_code"].values
        val[code], st[code] = v, s
    return val, st


def excess(v, s):
    x = np.where(s == "V", v, np.nan)
    base = pd.Series(x).rolling(288, center=True, min_periods=60).quantile(0.5).bfill().ffill().values
    return x, x - base


def detections(val, st):
    out = {}
    for code in val:
        x, e = excess(val[code], st[code])
        days, peak = set(), -1
        for t in range(1, NI - 1):
            a, b, c = e[t - 1], e[t], e[t + 1]
            if np.isnan(a) or np.isnan(b) or np.isnan(c) or a < 30:
                continue
            if a - b > 0.5 * a and c < 0.5 * a:
                s0 = t - 1
                while s0 > 0 and not np.isnan(e[s0 - 1]) and e[s0 - 1] > 15:
                    s0 -= 1
                days.add((Q0 + dt.timedelta(minutes=10 * s0)).date())
                peak = max(peak, int(round(np.nanmax(x[s0:t]))))
        if days:
            out[code] = (sorted(days), peak)
    return out


def run(tgt, figures_path):
    N[0] = 0
    F = json.load(open(figures_path))
    val, st = export(tgt)
    det = detections(val, st)
    check("the stations notified", sorted(det) == sorted(F["call_stations"]), sorted(det))
    for code, (days, peak) in det.items():
        check("%s dates" % code, [d.strftime("%d/%m/%Y") for d in days] == F["call"][code]["dates"],
              (days, F["call"][code]["dates"]))
        check("%s highest value" % code, peak == F["call"][code]["peak"], (peak, F["call"][code]["peak"]))
    check("detection days", sum(len(d) for d, p in det.values()) == F["detection_days"])
    nat, art = 0.0, 2.0
    for code in val:
        x, e = excess(val[code], st[code])
        a, b = e[:-1], e[1:]
        good = (~np.isnan(a)) & (~np.isnan(b)) & (a >= 30)
        frac = np.where(good, (a - b) / np.where(a == 0, 1, a), np.nan)
        big = np.where(good & (frac > 0.5))[0]
        mask = np.zeros(NI - 1, dtype=bool)
        for k in big:
            if k + 2 < NI and e[k + 2] < 0.5 * a[k]:
                art = min(art, frac[k])
                lo = k
                while lo > 0 and not np.isnan(e[lo - 1]) and e[lo - 1] > 15:
                    lo -= 1
                mask[max(0, lo - 1):k + 2] = True
        keep = good & ~mask
        if keep.any():
            nat = max(nat, float(np.nanmax(frac[keep])))
    check("natural fall ceiling", int(np.ceil(100 * nat)) == F["nat_max_fall_pct"], nat)
    check("smallest detection fall", int(np.floor(100 * art)) == F["art_min_fall_pct"], art)

    # the procedure's screen: investigation-level periods cleared by rain at the nearest gauge within an hour
    cfg = json.load(open(os.path.join(tgt, "mvgn_alarm_config_2026Q3.json")))
    ref = {s["siteId"]: s["referenceLevel"] for s in cfg["sites"]}
    h, srows = sheet_rows(os.path.join(tgt, "mvgn_station_register.xlsx"), "Stations")
    pos = {r[0]: (r[3], r[4]) for r in srows}
    sites = pd.read_csv(os.path.join(tgt, "northvale_water_raingauge_sites.csv"))
    gauge = pd.read_csv(os.path.join(tgt, "northvale_water_raingauges_15min_2026Q3.csv"))
    gauge["utc"] = [local_to_utc(s, "%d/%m/%Y %H:%M") for s in gauge["Time (GMT/BST)"]]
    wet = {}
    for gid, grp in gauge[gauge["Rainfall (mm)"] > 0].groupby("Gauge ref"):
        wet[gid] = sorted(grp["utc"])
    near = {c: sites.loc[((sites.easting - e) ** 2 + (sites.northing - n) ** 2).idxmin(), "gauge_id"]
            for c, (e, n) in pos.items()}
    screened = set()
    for code in val:
        x = np.where(st[code] == "V", val[code], np.nan)
        inv = np.nan_to_num(x, nan=-1) >= ref[code] + 30
        t = 0
        while t < NI:
            if inv[t]:
                a = t
                while t < NI and inv[t]:
                    t += 1
                lo = Q0 + dt.timedelta(minutes=10 * (a - 6)) - dt.timedelta(minutes=15)
                hi = Q0 + dt.timedelta(minutes=10 * (t + 6))
                rain = [w for w in wet.get(near[code], []) if lo < w < hi]
                if not rain:
                    screened.add(code)
            else:
                t += 1
    check("the rain screen's count", len(screened) == F["default_path_count"], sorted(screened))

    # source checks: the kit's source on the day, rebuilt from the register's entries
    cert_text = "\n".join(p.extract_text() for p in PdfReader(os.path.join(tgt, "check_source_certificates.pdf")).pages)
    certs = {}
    for page in cert_text.split("Certificate of calibration ")[1:]:
        no = page.split()[0]
        serial = re.search(r"serial (CS-\d{4})", page).group(1)
        refd = dt.datetime.strptime(re.search(r"Reference date\s+(\d{1,2} \w+ \d{4})", page).group(1), "%d %B %Y").date()
        issued = dt.datetime.strptime(re.search(r"Date of issue\s+(\d{2}/\d{2}/\d{4})", page).group(1), "%d/%m/%Y").date()
        j1 = float(re.search(r"J1 clamp\s+(\d+)", page).group(1))
        j2 = float(re.search(r"J2 sleeve\s+(\d+)", page).group(1))
        half = float(re.search(r"half-life ([\d.]+) years", page).group(1))
        certs.setdefault(serial, []).append((issued, refd, {"J1": j1, "J2": j2}, half, no))
    kits = pd.read_csv(os.path.join(tgt, "field_kits_register.csv"))
    kit_src = dict(zip(kits.kit_id, kits.check_source)); kit_jig = dict(zip(kits.kit_id, kits.jig.str[:2]))
    reg = pd.read_csv(os.path.join(tgt, "sealed_source_register_2026.csv"))
    reg["d"] = pd.to_datetime(reg["entry_date"], format="%d/%m/%Y").dt.date
    reg = reg.rename(columns={"source_serial": "source", "entry_type": "entry", "held_at": "location"})
    mig = pd.read_csv(os.path.join(tgt, "station_code_migration_2025.csv"))
    old = dict(zip(mig.outstation_code, mig.platform_code))
    visits = os.path.join(tgt, "source_check_visits_2026Q3.xlsx")
    chk = {}
    h, rows = sheet_rows(visits, "J French")
    for r in rows:
        chk[r[2]] = (dt.datetime.strptime(r[0], "%d/%m/%Y").date(), r[4], r[5], float(r[7]) - float(r[6]))
    h, rows = sheet_rows(visits, "A Connolly")
    for r in rows:
        chk[old[r[2]]] = (dt.datetime.strptime(r[0], "%d/%m/%Y").date(), r[4], kit_jig[r[4]],
                          round(float(r[6]) * 1000) - round(float(r[5]) * 1000))
    for code, (day, kit, jig, net) in sorted(chk.items()):
        src = kit_src[kit]
        out = reg[(reg.source == src) & (reg.entry == "transfer out") & (reg.d <= day)]
        back = reg[(reg.source == src) & (reg.entry == "transfer in") & (reg.d > day)]
        if len(out) and len(back):
            seen = reg[(reg.location == kit) & (reg.d >= out.d.max()) & (reg.d < back.d.min())]
            src = seen.source.unique()[0]
        issued, refd, vals, half, no = [c for c in sorted(certs[src]) if c[0] <= day][-1]
        pct = net / (vals[jig] * 0.5 ** ((day - refd).days / 365.25 / half)) * 100
        check("check %s" % code, "%.1f" % pct == F["checks"][code]["pct"], (pct, F["checks"][code]))
        check("check %s result" % code, ("Pass" if abs(pct - 100) <= 10 else "Fail") == F["checks"][code]["result"])

    # air: the controller's measured flow integrated over the filter's time in the holder
    pump = pd.read_csv(os.path.join(tgt, "air_pump_controller_log_2026Q3.csv"))
    pump["t"] = pd.to_datetime(pump.timestamp_utc, utc=True)
    h, lrows = sheet_rows(os.path.join(tgt, "gross_beta_results_2026Q3.xlsx"), "Gross beta")
    lab = {}
    for r in lrows:
        if r[1] not in lab or r[8] > lab[r[1]][1]:
            lab[r[1]] = (float(r[5]), r[8])
    field = os.path.join(tgt, "air_sampler_field_sheets_2026Q3.xlsx")
    for sampler in ("AS1", "AS2", "AS3"):
        h, rows = sheet_rows(field, sampler)
        lg = pump[pump.sampler_id == sampler].sort_values("t").reset_index(drop=True)
        check("%s logs RUN rows with no measured flow (transmitter dropouts)" % sampler,
              bool((lg.measured_flow_m3_h.isna() & (lg.pump_state == "RUN")).any()) and
              not bool((lg.measured_flow_m3_h.isna() & (lg.pump_state != "RUN")).any()))
        lg["filled"] = lg.measured_flow_m3_h.interpolate(method="linear")
        for r in rows:
            on = local_to_utc(r[1], "%d/%m/%Y %H:%M"); off = local_to_utc(r[2], "%d/%m/%Y %H:%M")
            sel = lg[(lg.t > pd.Timestamp(on) - pd.Timedelta(minutes=15)) & (lg.t < pd.Timestamp(off))]
            vol = float((sel.filled * 0.25).sum())
            conc = lab[r[0]][0] / vol * 1000
            check("filter %s" % r[0], "%.2f" % conc == F["air"][r[0]]["conc"], (conc, F["air"][r[0]]))

    # timeliness: the earliest telemetry receipt of each interval holding a value, against the interval's end
    ing = pd.read_csv(os.path.join(tgt, "platform_ingest_log_2026Q3.csv"), dtype=str)
    first = {c: np.full(NI, np.inf) for c in val}
    for code, a, b, rec in zip(ing.station_code, ing.first_interval_start, ing.last_interval_start, ing.received_at):
        if rec.endswith("Z"):
            when = dt.datetime.strptime(rec, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
        else:
            when = local_to_utc(rec, "%d/%m/%Y %H:%M:%S")
        m = (when - Q0).total_seconds() / 60.0
        seg = first[code][slot(a):slot(b) + 1]
        np.minimum(seg, m, out=seg)
    ends = np.arange(NI) * 10.0 + 10.0
    for code in val:
        has = ~np.isnan(val[code])        # a test-mode value counts (agreement 2.3); a fault record has none
        pct = float((has & (first[code] - ends <= 60.0)).sum()) / NI * 100
        check("timeliness %s" % code, "%.1f" % pct == F["timely"][code], (pct, F["timely"][code]))
    return N[0]
