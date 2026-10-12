"""The pack's data files, each as its source system exports it."""
import csv
import datetime as dt
import json

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font

import book as B
import climate as C
import world as W

DAILY = "ncs_daily_041391_19951101_20270827.csv"
REGISTER = "ncs_climatological_register_041207_1964_1995.xlsx"
PARALLEL = "ncs_parallel_observations_maxtemp.csv"
DISTRICT = "ncs_district_stations_monthly_mean_max.csv"
STATIONS = "ncs_station_list_merrin_district.json"
SCHEDULE = "policy_schedule_HC104_merrin_valley_2027-08-26.csv"
BLOCKS = "merrin_valley_block_register_2027-08.xlsx"
CLAIMS = "claims_register_heat_cover_2020_2027.csv"
LEDGER = "gl6120_weather_claims_payments_FY2020_FY2028.csv"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def rng(*key):
    return np.random.default_rng([W.SEED, 700] + [int(k) for k in key])


def winter_gaps(days, start, end, seed, per_year):
    """days with no reading: observer leave or a logger fault, kept out of every December to February"""
    g = rng(seed)
    gap = set()
    for y in range(start.year, end.year + 1):
        for _ in range(per_year):
            d = dt.date(y, int(g.integers(4, 11)), int(g.integers(1, 27)))
            for k in range(int(g.integers(1, 5))):
                gap.add(d + dt.timedelta(days=k))
    return {d for d in gap if start <= d <= end and W.season_of(d) is None}


def write_daily(path, mf):
    g = rng(1)
    gaps = winter_gaps(mf["days"], W.CHANGE, W.RECORD_END, 2, 2)
    rows = []
    for k, d in enumerate(mf["days"]):
        if d < W.CHANGE or d in gaps:
            continue
        q = "A" if d <= W.APPROVED_TO else "P"
        rain = 0.0 if g.random() < 0.72 else float(np.round(g.gamma(0.9, 6.0), 1))
        rows.append((W.NEW_ID, d.isoformat(), "TMAX", "%.1f" % mf["probe"][k], q))
        rows.append((W.NEW_ID, d.isoformat(), "TMIN", "%.1f" % mf["tmin"][k], q))
        rows.append((W.NEW_ID, d.isoformat(), "PRCP", "%.1f" % rain, q))
    # a re-sent July 2012 batch the portal keeps twice
    resend = [r for r in rows if r[1].startswith("2012-07-1")]
    rows += resend
    rows.sort(key=lambda r: (r[1], ["TMAX", "TMIN", "PRCP"].index(r[2])))
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["station_no", "obs_date", "element", "value", "quality"])
        w.writerows(rows)
    return len(rows)


def write_register(path, mf):
    gaps = winter_gaps(mf["days"], W.RECORD_START, W.CHANGE - dt.timedelta(days=1), 3, 3)
    by_day = {d: mf["glass"][k] for k, d in enumerate(mf["days"]) if d < W.CHANGE and d not in gaps}
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    bold = Font(bold=True)
    for y in range(W.RECORD_START.year, W.CHANGE.year + 1):
        ws = wb.create_sheet(str(y))
        ws["A1"] = "National Climate Service  Climatological register (digitised)"
        ws["A2"] = "Station %s  Merrin Flat (Research Station)   Maximum temperature, deg C   Year %d" % (W.OLD_ID, y)
        ws["A1"].font = bold
        ws.append([])
        ws.append(["Day"] + MONTHS)
        for c in ws[4]:
            c.font = bold
            c.alignment = Alignment(horizontal="center")
        for day in range(1, 32):
            row = [day]
            for m in range(1, 13):
                try:
                    d = dt.date(y, m, day)
                except ValueError:
                    row.append(None)
                    continue
                v = by_day.get(d)
                row.append(None if v is None else (int(v) if float(v).is_integer() else float(v)))
            ws.append(row)
        ws.column_dimensions["A"].width = 6
        for col in "BCDEFGHIJKLM":
            ws.column_dimensions[col].width = 7
        ws.freeze_panes = "B5"
    wb.save(path)
    return by_day


def write_parallel(path, pairs):
    names = {s[0]: (s[2], s[1]) for s in C.SITES}
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["site_no", "site_name", "obs_date", "max_glass_large_screen", "max_probe_small_shield"])
        for code, d, gl, pr in pairs:
            no, nm = names[code]
            w.writerow([no, nm, d.isoformat(), ("%.1f" % gl), ("%.1f" % pr)])
    return len(pairs)


def district_series():
    """the other six sites' monthly mean maxima, each on glass until its own changeover and the probe after"""
    out = []
    g = rng(4)
    for i, site in enumerate(C.SITES):
        if i == 0:
            continue
        code, name, no, _, _, _, _, d0, _ = site
        days = C.days_between(dt.date(1965, 1, 1), dt.date(2027, 7, 31))
        t = C.true_max(i, days)
        gl, pr = C.glass(i, t), C.probe(i, t)
        by_month = {}
        for k, d in enumerate(days):
            v = pr[k] if d >= d0 else gl[k]
            by_month.setdefault((d.year, d.month), []).append(float(v))
        for (y, m), vals in sorted(by_month.items()):
            if g.random() < 0.012:
                continue
            short = int(g.integers(0, 3)) if g.random() < 0.05 else 0
            vals = vals[:len(vals) - short] if short else vals
            out.append((no, name, y, m, "%.1f" % float(np.mean(vals)), len(vals)))
    return out


def write_district(path):
    rows = district_series()
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["station_no", "station_name", "year", "month", "mean_max_c", "days_in_mean"])
        w.writerows(rows)
    return len(rows)


def write_stations(path):
    st = [{"station_no": W.OLD_ID, "name": "Merrin Flat (Research Station)", "network": "cooperative",
           "opened": "1964-07-01", "closed": "1995-10-31", "successor": W.NEW_ID, "lat": -34.212, "lon": 140.871,
           "elevation_m": 61}]
    coords = {"MF": (-34.212, 140.871, 61), "BR": (-34.511, 140.402, 74), "CW": (-33.868, 141.335, 58),
              "HG": (-34.640, 141.102, 92), "PN": (-35.103, 140.890, 103), "TB": (-34.380, 141.020, 66),
              "WK": (-33.947, 140.519, 70)}
    for code, name, no, *_ , d0, d1 in C.SITES:
        lat, lon, el = coords[code]
        if code == "MF":
            st.append({"station_no": no, "name": "Merrin Flat AWS", "network": "automatic", "opened": "1995-11-01",
                       "closed": None, "successor": None, "predecessor": W.OLD_ID, "lat": lat, "lon": lon, "elevation_m": el})
        else:
            st.append({"station_no": no, "name": name, "network": "automatic", "opened": "1964-01-01" if code != "PN" else "1967-05-01",
                       "closed": None, "successor": None, "automatic_from": d0.isoformat(), "lat": lat, "lon": lon,
                       "elevation_m": el})
    json.dump({"service": W.SERVICE, "district": "Merrin and Murrow valleys", "exported": "2027-08-27T08:14:00+09:30",
               "stations": st}, open(path, "w"), indent=1)


def write_schedule(path, mem, bl):
    g = rng(5)
    pol = {m["coop_no"]: m for m in mem}
    rows = []
    for b in sorted(bl, key=lambda b: (b.member, b.no)):
        if b.first_cover is None:
            continue
        m = pol[b.member]
        incept = dt.date(b.first_cover, 11, 1)
        for variety, _ in b.varieties:
            rows.append([m["policy_no"], "MV-%04d" % b.member, m["name"], b.no, variety, B.stored_district(b),
                         "%.1f" % b.area, incept.isoformat(), b.endorsed.isoformat() if b.endorsed else "",
                         b.cancel.isoformat() if b.cancel else ""])
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["policy_no", "grower_ref", "grower_name", "block_no", "variety", "sub_district", "insured_ha",
                    "inception", "last_endorsement", "cancelled_from"])
        w.writerows(rows)
    return len(rows)


def write_blocks(path, mem, bl):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Blocks"
    ws["A1"] = W.COOP
    ws["A2"] = "Block register at 1 August 2027 (planted area by variety)"
    ws["A1"].font = Font(bold=True)
    ws.append([])
    ws.append(["Member no", "Member", "Block", "Sub-district", "Variety", "Planted ha", "Year planted"])
    for c in ws[4]:
        c.font = Font(bold=True)
    name = {m["coop_no"]: m["name"] for m in mem}
    for b in sorted(bl, key=lambda b: (b.member, b.no)):
        for variety, ha in b.varieties:
            ws.append([b.member, name[b.member], b.no, b.district_new, variety, round(ha, 2), b.planted])
    for col, wd in zip("ABCDEFG", (11, 30, 7, 14, 20, 11, 12)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A5"
    wb.save(path)


def write_claims(path, reg):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["claim_no", "season", "grower_ref", "block_no", "lodged", "channel", "assessed_amount"])
        for r in reg:
            w.writerow([r["claim_no"], r["season"], "MV-%04d" % r["grower_ref"], r["block_no"], r["lodged"].isoformat(),
                        r["source"], "%.2f" % r["assessed_amount"]])
    return len(reg)


def write_ledger(path, ledger):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["payment_id", "posting_date", "fin_year", "gl_account", "reference", "payee", "amount"])
        for r in sorted(ledger, key=lambda r: (r["posting_date"], r["payment_id"])):
            w.writerow([r["payment_id"], r["posting_date"].strftime("%d/%m/%Y"), r["fin_year"], "6120",
                        r["claim_no"], r["payee"], "%.2f" % r["amount"]])
    return len(ledger)
