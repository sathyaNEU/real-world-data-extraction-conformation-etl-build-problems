"""The data files as the Office and the Authority export them: the two final annual trip files, the eight provisional
2026 monthly drops, the 2023 origin-destination archive and the Office's three registers."""
import csv
import datetime as dt

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import sim as S
import world as W

V2 = {"rid": "record_id", "vendor": "vendor_id", "vehicle": "vehicle_id", "brokerage_label": "brokerage_id",
      "meter_on": "pickup_datetime", "meter_off": "dropoff_datetime", "pu": "pickup_zone", "do": "dropoff_zone",
      "pax": "passenger_count", "km": "trip_distance_km", "fare": "fare_amount", "fee": "airport_fee",
      "tip": "tip_amount", "total": "total_amount", "pay": "payment_type", "sf": "store_and_fwd_flag"}
V3 = {"rid": "record_id", "vendor": "vendor_id", "vehicle": "vehicle_id", "brokerage_label": "brokerage_id",
      "meter_on": "meter_on", "meter_off": "meter_off", "pu": "pu_zone", "do": "do_zone", "pax": "passengers",
      "km": "distance_km", "fare": "fare", "fee": "airport_fee", "tip": "tip", "total": "total",
      "pay": "payment_type", "sf": "sf_flag"}
INTS = {"rid": pa.int64(), "vendor": pa.int8(), "brokerage_label": pa.int8(), "pu": pa.int16(), "do": pa.int16(),
        "pax": pa.int8(), "pay": pa.int8()}


def zones_cols(recs):
    """Pickup and drop-off zone from the direction: a pickup leaves zone 1 for its zone, a drop-off arrives from it."""
    pick = (recs["dir"] == "P").to_numpy()
    z = recs["zone"].to_numpy()
    return np.where(pick, W.AIRPORT, z), np.where(pick, z, W.AIRPORT)


def local_date(s):
    return pd.to_datetime(s).to_numpy().astype("datetime64[D]")


def file_2024(x):
    r = x["recs"]
    d = local_date(r["meter_on"])
    sel = (d >= np.datetime64("2024-01-01")) & (d <= np.datetime64("2024-12-31")) & r["kind"].isin(
        ["trip", "void", "reversal"]).to_numpy()
    return labelled(r[sel], x, W.FILE_2024_BUILT).sort_values(["meter_on", "rid"], kind="stable")


def file_2025(x):
    r = x["recs"]
    d = local_date(r["meter_on"])
    sel = (d >= np.datetime64("2025-01-01")) & (d <= np.datetime64("2025-12-31")) & (r["kind"] == "trip").to_numpy()
    return labelled(r[sel], x, W.FILE_2025_BUILT).sort_values(["meter_on", "rid"], kind="stable")


def labelled(r, x, built):
    """An annual file joins each trip to the vehicle register as it stands the day the file is built."""
    by = {v["vid"]: v for v in x["lic"]}
    r = r.copy()
    r["brokerage_label"] = [S.latest_brokerage(by[v], built) for v in r["vehicle"]]
    return r


def drop_2026(x, month):
    """The records the Office received in a 2026 month, trips begun in 2026 only (a closed year's late records go to
    its annual file), in the order received, each trip's brokerage that day."""
    r = x["recs"]
    rec = local_date(r["received"])
    on = local_date(r["meter_on"])
    a = np.datetime64(dt.date(2026, month, 1))
    b = np.datetime64(dt.date(2026 + (month == 12), month % 12 + 1, 1))
    sel = (rec >= a) & (rec < b) & (on >= np.datetime64("2026-01-01"))
    out = r[sel].copy()
    out["brokerage_label"] = out["brokerage"]
    # a Corvane unit on firmware 8.1 writes a trip it sends from memory with its meter times to the minute
    log = ((out["kind"] == "trip") & (out["vendor"] == 2) & (out["sf"] == "Y")).to_numpy()
    for c in ("meter_on", "meter_off"):
        out.loc[log, c] = pd.to_datetime(out.loc[log, c]).dt.floor("min").to_numpy()
    return out.sort_values("rid", kind="stable")


def table(df, names, utc=False, fee_name=None):
    pu, do = zones_cols(df)
    df = df.assign(pu=pu, do=do)
    cols, arrays = [], []
    for k, name in names.items():
        if k == "fee" and fee_name:
            name = fee_name
        v = df[k]
        if k in ("meter_on", "meter_off"):
            loc = pd.to_datetime(v)
            if utc:
                loc = loc.dt.tz_localize(W.TZ, ambiguous="NaT", nonexistent="shift_forward").dt.tz_convert("UTC")
                arr = pa.array(loc, type=pa.timestamp("us", tz="UTC"))
            else:
                arr = pa.array(loc, type=pa.timestamp("us"))
        elif k in INTS:
            arr = pa.array(v.to_numpy().astype("int64"), type=INTS[k])
        elif k == "km":
            arr = pa.array(np.round(v.to_numpy().astype(float), 2), type=pa.float64())
        elif k in ("fare", "fee", "tip", "total"):
            arr = pa.array(np.round(v.to_numpy().astype(float), 2), type=pa.float64())
        else:
            arr = pa.array(v.astype(str).tolist(), type=pa.string())
        cols.append(name)
        arrays.append(arr)
    return pa.Table.from_arrays(arrays, names=cols)


DELTA = ("record_id", "meter_on", "meter_off", "pickup_datetime", "dropoff_datetime")


def write_parquet(path, tbl):
    tbl = tbl.replace_schema_metadata(None)
    enc = {c: "DELTA_BINARY_PACKED" for c in tbl.column_names if c in DELTA}
    pq.write_table(tbl, path, compression="zstd", compression_level=9,
                   use_dictionary=[c for c in tbl.column_names if c not in enc], column_encoding=enc,
                   write_statistics=True, data_page_size=1 << 20, row_group_size=1 << 17)
    return tbl.num_rows


def write_annual(path, df, names):
    return write_parquet(path, table(df, names))


def write_drop(path, df, month):
    fee_name = "Airport_Fee" if (2026, month) >= W.FEE_COL_RENAMED else None
    return write_parquet(path, table(df, V3, utc=True, fee_name=fee_name))


def archive_rows(x):
    """The Office's daily origin-destination archive for 2023: trips (voided trips not counted) by local start date."""
    t = S.truth(x)
    d = local_date(t["meter_on"])
    t = t[(d >= np.datetime64("2023-01-01")) & (d <= np.datetime64("2023-12-31"))]
    pu, do = zones_cols(t)
    g = pd.DataFrame({"trip_date": local_date(t["meter_on"]).astype(str), "pu_zone": pu, "do_zone": do})
    g = g.groupby(["trip_date", "pu_zone", "do_zone"]).size().reset_index(name="trips")
    return [[r.trip_date, int(r.pu_zone), int(r.do_zone), int(r.trips)] for r in g.itertuples()]


ARCHIVE_COLS = ["trip_date", "pu_zone", "do_zone", "trips"]
ZONE_COLS = ["zone_id", "zone_name", "district"]
BROKERAGE_COLS = ["brokerage_id", "brokerage_name", "brokerage_licence", "licensed_since", "status"]
AFFIL_COLS = ["vehicle_id", "brokerage_id", "effective_from", "effective_to", "reason"]


def zone_rows():
    return [[z, name, district] for z, name, district, _ in W.ZONES]


def brokerage_rows():
    since = {1: "1994-04-01", 2: "2001-09-17", 3: "1988-01-11", 4: "1979-06-30", 5: "2009-03-02", 6: "2014-11-20"}
    return [[b, W.BROKERAGES[b], "VFH-B-%03d" % (100 + 17 * b), since[b], "Active"] for b in W.BROKERAGES]


def affiliation_rows(x):
    """Each licence's spells with a brokerage, as the Office's register held them when pulled (9 October 2026)."""
    rows = []
    for v in sorted(x["lic"], key=lambda v: v["vid"]):
        for i, (b, a, z) in enumerate(v["spells"]):
            if z is not None and z < dt.date(2022, 1, 1):
                continue
            why = "Licence issued" if i == 0 else "Annual renewal" if (a.month, a.day) == (1, 1) else "Mid-term transfer"
            rows.append([v["vid"], b, a.isoformat(), z.isoformat() if z else "", why])
    return rows


def write_csv(path, cols, rows):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(cols)
        w.writerows(rows)
    return len(rows)
