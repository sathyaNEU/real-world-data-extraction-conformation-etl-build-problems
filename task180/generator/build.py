"""Build the task180 pack: python3 build.py  (writes ../target/ and ../target.zip is cut by ship.py)."""
import csv
import datetime as dt
import json
import os
import shutil
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W   # noqa: E402
import sim          # noqa: E402
import hist         # noqa: E402
import docs         # noqa: E402

TARGET = os.path.join(HERE, "..", "target")
F = {  # shipped file names
    "mart": "rp_mart_weekly_import_2023-12-04_2026-11-30.csv",
    "reads": "smart_daily_reads_2024-10-01_2026-12-07.parquet",
    "register": "supply_point_register_2026-12-07.xlsx",
    "cot": "change_of_occupier_events_2019-2026.csv",
    "measures": "heating_measures_completions_2023-2026.csv",
    "hdd": "station_degree_days_2023-12-01_2026-12-06.csv",
    "stations": "patch_weather_stations.json",
    "fl": "fieldlink_visits_2023-10-02_2024-11-17.csv",
    "fo": "fieldops_visits_2024-11-04_2026-11-30.csv",
    "appeals": "tamper_appeals_register.xlsx",
    "rota": "rp_field_rota_q1_2027.xlsx",
    "rp07": "RP-07_referral_and_placement.pdf",
    "fw3": "FW-3_field_working_standard.docx",
    "notes": "rp_extract_field_notes.md",
    "log": "extract_log_2026-12-07.txt",
    "vends": "prepayment_vends_2026-06-01_2026-11-30.csv",
    "losses": "dno_feeder_loss_estimates_2025-26.xlsx",
}
PATCH_NAME = {p[0]: p[1] for p in W.PATCHES}
PATCH_STATION = {p[0]: p[2] for p in W.PATCHES}


def fmt_date(d):
    return d.isoformat()


def write_mart(w):
    """Analytics mart rp.weekly_import: one row per metering system per ISO week, keyed by the
    metering system's primary supply number; kWh is the metering system's import (all its meters)."""
    weeks = [W.MART_START + dt.timedelta(weeks=k) for k in range((W.EXTRACT_DATE - W.MART_START).days // 7)]
    rows = []
    for prem in w["premises"]:
        total = sum(s["kwh"] for s in prem["supplies"])
        key = prem["supplies"][0]["mpan"]
        for wk in weeks:
            s = sim.day_index(wk)
            rows.append((key, prem["patch"], fmt_date(wk), round(float(total[s:s + 7].sum()), 2)))
    rows.sort(key=lambda r: (r[2], r[0]))
    with open(os.path.join(TARGET, F["mart"]), "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["mpan_core", "rp_patch", "week_commencing", "kwh_import"])
        wr.writerows(rows)
    return len(rows)


def write_reads(w, rng):
    """Cumulative midnight register reads per supply, with comms gaps and meter exchanges."""
    r0 = sim.day_index(W.READS_START)
    nread = (W.EXTRACT_DATE - W.READS_START).days + 1          # reads dated READS_START..EXTRACT_DATE
    read_dates = [W.READS_START + dt.timedelta(i) for i in range(nread)]
    protect = set()
    d = dt.date(2026, 9, 28)
    while d <= W.EXTRACT_DATE:
        if d.weekday() == 0:
            protect.add(d)
        d += dt.timedelta(1)
    protect |= {W.ASSESS_START - dt.timedelta(1), W.ASSESS_START, W.ASSESS_START + dt.timedelta(1),
                W.BASELINE_START, W.BASELINE_START + dt.timedelta(1), W.EXTRACT_DATE,
                W.EXTRACT_DATE - dt.timedelta(1)}
    exchanges = []
    cols = {"mpan_core": [], "meter_serial": [], "read_date": [], "register_id": [],
            "cumulative_kwh": [], "read_type": []}
    for s in w["supplies"]:
        kwh = s["kwh"]
        # consumption on day index (r0 + i - 1) is what read i closes; read 0 is the opening read
        cum0 = float(rng.uniform(2_000, 48_000))
        daily = kwh[r0 - 1:r0 - 1 + nread]                       # day before each read date
        cum = cum0 + np.concatenate([[0.0], np.cumsum(daily[1:])])
        serials = [s["serial"]] * nread
        values = cum.copy()
        if rng.random() < 0.028:
            # meter exchange on a weekday between Jan 2025 and Jun 2026
            while True:
                ex = dt.date(2025, 1, 6) + dt.timedelta(int(rng.integers(0, 520)))
                if ex.weekday() < 5 and ex not in protect:
                    break
            ei = (ex - W.READS_START).days
            frac = float(rng.uniform(0.3, 0.6))
            day_kwh = float(kwh[r0 - 1 + ei + 1])                  # consumption on the exchange day
            final_old = cum[ei] + frac * day_kwh
            init_new = round(float(rng.uniform(0.0, 12.0)), 1)
            new_serial = s["serial"][:3] + f"{int(rng.integers(1_000_000, 9_999_999)):07d}"
            for j in range(ei + 1, nread):
                serials[j] = new_serial
                values[j] = init_new + (cum[j] - cum[ei] - frac * day_kwh)
            exchanges.append({"mpan_core": s["mpan"], "removed_serial": s["serial"],
                              "exchange_date": ex, "final_read_kwh": round(final_old, 1),
                              "fitted_serial": new_serial, "initial_read_kwh": init_new})
            s["current_serial"] = new_serial
        else:
            s["current_serial"] = s["serial"]
        keep = np.ones(nread, bool)
        # comms gaps: runs of 1 to 4 missing midnight reads
        for _ in range(int(rng.poisson(3.2))):
            st = int(rng.integers(1, nread - 6))
            ln = int(rng.integers(1, 5))
            span = [read_dates[k] for k in range(st, st + ln)]
            if any(x in protect for x in span):
                continue
            keep[st:st + ln] = False
        for j in np.nonzero(keep)[0]:
            cols["mpan_core"].append(s["mpan"])
            cols["meter_serial"].append(serials[j])
            cols["read_date"].append(read_dates[j])
            cols["register_id"].append("1")
            cols["cumulative_kwh"].append(round(float(values[j]), 1))
            cols["read_type"].append("A")
    df = pd.DataFrame(cols)
    df["read_date"] = pd.to_datetime(df["read_date"]).dt.date
    df.to_parquet(os.path.join(TARGET, F["reads"]), index=False, compression="snappy")
    return len(df), exchanges


def write_cot(w, rng):
    rows = []
    seq = iter(range(552_100, 999_999, 3))
    for prem in w["premises"]:
        accts = prem["accounts"]
        for k in range(1, len(accts)):
            prev, cur = accts[k - 1], accts[k]
            if cur[3] == "occupier":
                rows.append((f"COT{next(seq):06d}", prem["uprn"], "Move out", cur[1], prev[0], cur[0]))
            else:
                rows.append((f"COT{next(seq):06d}", prem["uprn"], "Move in", cur[1], prev[0], cur[0]))
    rows.sort(key=lambda r: (r[3], r[0]))
    with open(os.path.join(TARGET, F["cot"]), "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["cot_ref", "uprn", "event", "event_date", "closing_account", "opening_account"])
        for r in rows:
            wr.writerow([r[0], r[1], r[2], r[3].strftime("%d/%m/%Y"), r[4], r[5]])
    return len(rows)


def add_old_occupiers(w, rng):
    """Older changes of occupier, before the screening windows: realistic account turnover."""
    acct_seq = iter(range(30_100_000, 39_999_999, 11))
    for prem in w["premises"]:
        if prem["role"] != "ordinary" or rng.random() > 0.14:
            continue
        when = dt.date(2019, 6, 1) + dt.timedelta(int(rng.integers(0, 1900)))
        if when >= dt.date(2024, 9, 1):
            continue
        a0 = prem["accounts"][0]
        prem["accounts"] = [(f"CE{next(acct_seq):08d}", dt.date(2016, 1, 1), when - dt.timedelta(1), "named"),
                            (a0[0], when, None, "named")]
    w["accounts"] = [{"account_ref": a[0], "uprn": p["uprn"], "start": a[1], "end": a[2], "kind": a[3]}
                     for p in w["premises"] for a in p["accounts"]]


def write_measures(w, rng):
    rows = []
    seq = iter(range(71_020, 99_999, 7))
    for prem in w["premises"]:
        r = prem["role"]
        if r in ("retrofit", "histretro"):
            rows.append((prem["uprn"], "Air source heat pump", prem["hp_day"], "Replaces electric storage heating"))
        elif r == "ordinary" and prem["heat"] and rng.random() < 0.05:
            d = dt.date(2023, 5, 1) + dt.timedelta(int(rng.integers(0, 1200)))
            rows.append((prem["uprn"], "High heat retention storage heaters", d, "Like-for-like on the heating circuit"))
        elif r in ("ordinary", "whole", "heatdiv") and rng.random() < 0.035 and r == "ordinary":
            d = dt.date(2023, 4, 1) + dt.timedelta(int(rng.integers(0, 1250)))
            m = ["Loft insulation", "Cavity wall insulation", "Solar PV (3.2 kWp)", "Draught proofing"][int(rng.integers(0, 4))]
            rows.append((prem["uprn"], m, d, ""))
    rows.sort(key=lambda r: r[2])
    with open(os.path.join(TARGET, F["measures"]), "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["completion_ref", "uprn", "measure", "commissioned_on", "installer_note", "scheme"])
        for r in rows:
            wr.writerow([f"WH-{next(seq):05d}", r[0], r[1], r[2].strftime("%d %b %Y"), r[3],
                         "ECO4" if r[1] != "Air source heat pump" else "Warmer Homes Scotland"])
    return len(rows)


def write_hdd(w):
    rows = []
    for st, v in w["hdd"].items():
        for d, t, h in zip(v["days"], v["tmean"], v["hdd"]):
            rows.append((st, d.isoformat(), f"{t:.1f}", f"{h:.1f}"))
    with open(os.path.join(TARGET, F["hdd"]), "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["station", "date", "mean_air_temperature_c", "hdd_15_5c"])
        wr.writerows(rows)
    return len(rows)


def write_stations():
    out = {"source": "Met Office daily mean temperature, station nearest each field patch",
           "base_temperature_c": W.HDD_BASE_C,
           "patches": [{"rp_patch": p[0], "patch_name": p[1], "station": p[2]} for p in W.PATCHES]}
    with open(os.path.join(TARGET, F["stations"]), "w") as fh:
        json.dump(out, fh, indent=2)


def write_visits(visits, rng):
    fl, fo = [], []
    for v in visits:
        oc = v["outcome"]
        if "legacy_job" in v:
            fl.append([v["legacy_job"], v["date"].strftime("%d/%m/%Y"), v["prem"]["uprn"], v["mpan"],
                       v["officer"], {"CONF": "CONF", "CONF_OVER": "CONF", "NFF": "NFF", "NOACC": "NOACC"}[oc],
                       "" if v["assessed"] is None else int(v["assessed"])])
        if "new_job" in v:
            t = dt.datetime.combine(v["date"], dt.time(int(rng.integers(8, 16)), int(rng.integers(0, 60))))
            # FieldOps stamps UTC; BST runs to 25 Oct 2026 and from 29 Mar 2026 / 30 Mar 2025
            bst = (dt.date(2025, 3, 30) <= v["date"] < dt.date(2025, 10, 26)) or \
                  (dt.date(2026, 3, 29) <= v["date"] < dt.date(2026, 10, 25))
            t_utc = t - dt.timedelta(hours=1 if bst else 0)
            fo.append([v["new_job"], v.get("legacy_job", ""), t_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
                       v["prem"]["uprn"], v["mpan"], v["officer"],
                       {"CONF": "DIV-CONFIRMED", "CONF_OVER": "DIV-CONFIRMED", "NFF": "NO-FAULT",
                        "NOACC": "NO-ACCESS"}[oc],
                       "" if v["assessed"] is None else f"{v['assessed']:.0f}",
                       "SCREEN" if rng.random() < 0.7 else ["METER-READER", "TIP-OFF"][int(rng.integers(0, 2))]])
    with open(os.path.join(TARGET, F["fl"]), "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["JobNo", "VisitDate", "UPRN", "MPAN", "Officer", "Outcome", "AssessedKWh"])
        wr.writerows(fl)
    with open(os.path.join(TARGET, F["fo"]), "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["job_id", "legacy_job_no", "visit_start_utc", "uprn", "mpan_core", "officer",
                     "outcome", "assessed_kwh", "referral_source"])
        wr.writerows(fo)
    return len(fl), len(fo)


def appeals_rows(visits, rng):
    rows = []
    seq = iter(range(2_310, 9_999, 3))
    for v in visits:
        if v["outcome"] == "CONF_OVER":
            dec = "Overturned"
        elif v["outcome"] == "CONF" and rng.random() < 0.28:
            dec = ["Upheld", "Upheld", "Withdrawn"][int(rng.integers(0, 3))]
        else:
            continue
        # an appeal is lodged against the job number of the system that recorded the finding
        ref = v["legacy_job"] if "legacy_job" in v else v["new_job"]
        lodged = v["date"] + dt.timedelta(int(rng.integers(10, 40)))
        decided = lodged + dt.timedelta(int(rng.integers(30, 120)))
        rows.append([f"TA/{lodged.year}/{next(seq):04d}", ref, v["prem"]["uprn"], lodged, dec, decided])
    rows.sort(key=lambda r: r[3])
    return rows


def main():
    if os.path.isdir(TARGET):
        shutil.rmtree(TARGET)
    os.makedirs(TARGET)
    rng = np.random.default_rng(W.SEED + 7)
    w = sim.build_world()
    hrng = np.random.default_rng(W.SEED + 11)
    visits = hist.build_history(w, hrng)
    hist.apply_history_to_consumption(w, visits)
    add_old_occupiers(w, rng)
    n_mart = write_mart(w)
    n_reads, exchanges = write_reads(w, rng)
    n_cot = write_cot(w, rng)
    n_meas = write_measures(w, rng)
    n_hdd = write_hdd(w)
    write_stations()
    n_fl, n_fo = write_visits(visits, rng)
    apps = appeals_rows(visits, rng)
    docs.write_register(os.path.join(TARGET, F["register"]), w, exchanges)
    docs.write_appeals(os.path.join(TARGET, F["appeals"]), apps)
    docs.write_rota(os.path.join(TARGET, F["rota"]))
    docs.write_rp07(os.path.join(TARGET, F["rp07"]))
    docs.write_fw3(os.path.join(TARGET, F["fw3"]))
    docs.write_notes(os.path.join(TARGET, F["notes"]), F)
    docs.write_vends(os.path.join(TARGET, F["vends"]), w, rng)
    docs.write_losses(os.path.join(TARGET, F["losses"]), rng)
    counts = {"mart": n_mart, "reads": n_reads, "cot": n_cot, "measures": n_meas, "hdd": n_hdd,
              "fl": n_fl, "fo": n_fo, "appeals": len(apps), "exchanges": len(exchanges),
              "supplies": len(w["supplies"]), "premises": len(w["premises"])}
    docs.write_log(os.path.join(TARGET, F["log"]), F, counts)
    docs.scrub_metadata(TARGET)
    import subprocess
    scrub = os.path.join(HERE, "..", "..", ".claude", "skills", "reduce-house-fixes", "scripts",
                         "scrub_producer_metadata.py")
    subprocess.run([sys.executable, scrub, TARGET, "--apply", "--producer", "Corran Energy",
                    "--stamp", "2026-12-07"], check=True, capture_output=True)
    docs.scrub_metadata(TARGET, zips=False)
    print(json.dumps(counts))


if __name__ == "__main__":
    main()
