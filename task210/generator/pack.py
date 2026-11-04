"""Write task210's target/ bundle from the clean truth and the records, then cut target.zip deterministically."""
import io
import json
import os
import zipfile
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import world as W
import simulate as S
import records as RC

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
FIXED_ZIP_TIME = (2026, 11, 2, 9, 0, 0)

FILES = {
    "edr": "edr_event_export_2026-04-01_2026-10-31.csv",
    "avl": "avl_section_passes_2026.parquet",
    "survey": "streetcar_track_survey_2025.geojson",
    "metar": "ash_awos_hourly_obs_2026.csv",
    "yard": "yard_block_sheets_2026.csv",
    "releases": "foundry_depot_releases_2026.csv",
    "runs": "run_sheets_2026.csv",
    "roster": "operator_roster_2026.csv",
    "cards": "badge_card_register.csv",
    "mms": "mms_defect_reports_2026.csv",
    "srm": "SRM-07_seasonal_restricted_speed_orders.pdf",
    "pick": "january_2027_pick_timetable.pdf",
    "normals": "ash_climate_normals_1991-2020.pdf",
    "dash": "rail_ops_dashboard_2026.xlsx",
    "peds": "downtown_pedestrian_counts_2026.csv",
    "arena": "ashcombe_arena_events_2026.csv",
    "track": "track_maintenance_log_2026.csv",
    "school": "school_district_calendar_2026-27.csv",
}
DISTRACTORS = ["peds", "arena", "track"]


def sky_string(cover, rng):
    if cover == "CLR":
        return "CLR"
    h = int(rng.choice([25, 35, 45, 60, 80, 100, 120, 150]))
    return f"{cover}{h:03d}"


def write_csv(df, name):
    df.to_csv(os.path.join(TARGET, name), index=False, lineterminator="\n")


def build(seed=W.SEED, T=None, Rr=None):
    os.makedirs(TARGET, exist_ok=True)
    for f in os.listdir(TARGET):
        os.remove(os.path.join(TARGET, f))
    T = S.simulate(seed=seed) if T is None else T
    Rr = RC.records(T, seed) if Rr is None else Rr
    rng = np.random.default_rng(seed + 11)
    geo = T["geo"]

    # 1 recorder export (UTC, per car)
    E = Rr["edr"]
    edr = pd.DataFrame({
        "event_id": E["event_id"].values,
        "car": E["car"].astype(int).values,
        "event_time_utc": E["t_utc"].dt.strftime("%Y-%m-%dT%H:%M:%SZ").values,
        "lat": E["lat"].map(lambda v: f"{v:.6f}").values,
        "lon": E["lon"].map(lambda v: f"{v:.6f}").values,
        "speed_mph": E["speed_mph"].map(lambda v: f"{v:.1f}").values,
        "decel_mps2": E["decel_mps2"].map(lambda v: "" if pd.isna(v) else f"{v:.2f}").values,
        "event_code": E["code"].values,
        "operator_badge": E["badge"].values,
    })
    write_csv(edr, FILES["edr"])

    # 2 AVL section passes (lead vehicle, local time)
    A = Rr["avl"].sort_values(["entry_local", "line", "dir", "section"]).reset_index(drop=True)
    trip_id = [f"{l}{int(t) % 100000:05d}" for l, t in zip(A["line"], A["trip"])]
    tbl = pa.table({
        "service_date": pa.array(A["date"].dt.date.values, pa.date32()),
        "line": pa.array(A["line"].map({"J": "JUN", "F": "FDY"}).values).dictionary_encode(),
        "direction": pa.array(A["dir"].map({"O": "OB", "I": "IB"}).values).dictionary_encode(),
        "trip_id": pa.array(trip_id),
        "block": pa.array(A["block"].values).dictionary_encode(),
        "vehicle": pa.array(A["lead_car"].astype("int16").values, pa.int16()),
        "section_id": pa.array(A["section"].values).dictionary_encode(),
        "enter_local": pa.array(A["entry_local"].values.astype("datetime64[s]"), pa.timestamp("s")),
        "exit_local": pa.array(A["exit_local"].values.astype("datetime64[s]"), pa.timestamp("s")),
    })
    pq.write_table(tbl, os.path.join(TARGET, FILES["avl"]), compression="zstd", compression_level=9,
                   use_dictionary=True, write_statistics=False)

    # 3 track survey (RFC 7946 lon, lat), lines run outbound in coordinate order
    feats = []
    for _, g in geo.iterrows():
        feats.append({"type": "Feature", "properties": {"section_id": g["section"], "line": W.LINES[g["line"]][0],
                      "from_stop": g["from_stop"], "to_stop": g["to_stop"], "track_type": g["track"],
                      "length_ft": int(round(g["length_m"] * RC.FT))},
                      "geometry": {"type": "LineString", "coordinates": [[round(g["lon1"], 6), round(g["lat1"], 6)],
                                                                          [round(g["lon2"], 6), round(g["lat2"], 6)]]}})
    stops = {}
    for _, g in geo.iterrows():
        stops.setdefault(g["from_stop"], (g["lon1"], g["lat1"]))
        stops.setdefault(g["to_stop"], (g["lon2"], g["lat2"]))
    for name, (lo, la) in stops.items():
        feats.append({"type": "Feature", "properties": {"stop_name": name}, "geometry": {"type": "Point", "coordinates": [round(lo, 6), round(la, 6)]}})
    with open(os.path.join(TARGET, FILES["survey"]), "w") as f:
        json.dump({"type": "FeatureCollection", "name": "ART streetcar track survey 2025", "features": feats}, f, indent=1)

    # 4 hourly airport observations (UTC, observed at :53)
    M = Rr["metar"].copy()
    M = M[(M["hour_local"] >= pd.Timestamp(W.OBS_START)) & (M["hour_local"] < pd.Timestamp(W.OBS_END) + pd.Timedelta(days=1))]
    t_obs = pd.DatetimeIndex(M["hour_local"] + pd.Timedelta(minutes=53)).tz_localize(W.TZ, ambiguous=True, nonexistent="shift_forward").tz_convert("UTC").tz_localize(None)
    temp = 55 + 18 * np.sin((M["hour_local"].dt.dayofyear.values - 105) / 365 * 2 * np.pi) + 9 * np.sin((M["hour_local"].dt.hour.values - 9) / 24 * 2 * np.pi)
    met = pd.DataFrame({"station": "ASH", "valid_utc": t_obs.strftime("%Y-%m-%d %H:%M"),
                        "tmpf": np.round(temp + rng.normal(0, 3, len(M)), 0).astype(int),
                        "sknt": rng.integers(0, 18, len(M)), "vsby": np.where(rng.random(len(M)) < 0.03, 5, 10),
                        "skyc": [sky_string(c, rng) for c in M["cover"].values]})
    drop = rng.random(len(met)) < 0.012
    met = met[~drop]
    write_csv(met, FILES["metar"])

    # 5 yard block sheets (cars per block per day)
    C = Rr["consist"]
    yard = pd.DataFrame({"sheet_date": C["date"].dt.strftime("%m/%d/%Y"), "block": C["block"],
                         "pullout_cars": [f"{int(a)}" if pd.isna(b) else f"{int(a)}+{int(b)}" for a, b in zip(C["lead_car"], C["trail_car"])]})
    write_csv(yard, FILES["yard"])

    # 6 Foundry depot releases
    R = Rr["releases"].sort_values("released_local")
    write_csv(pd.DataFrame({"released": R["released_local"].dt.strftime("%Y-%m-%d %H:%M"), "car": R["car"],
                            "work_order": R["work_order"], "work_type": R["work_type"],
                            "release_check": "running brake test on the depot loop, emergency application included"}), FILES["releases"])

    # 7 run sheets, 8 roster, 9 badge card register
    D = Rr["dispatch"]
    O = Rr["operators"]
    write_csv(pd.DataFrame({"service_date": D["date"].dt.strftime("%Y-%m-%d"), "run": D["run"], "block": D["block"],
                            "operator_no": D["emp"].astype(int), "duty": D["duty"],
                            "revenue_hours": D["revenue_hours"].map(lambda v: f"{v:.2f}")}),
              FILES["runs"])
    write_csv(pd.DataFrame({"operator_no": O["emp"], "training_class": O["cls"].replace("", "pre-2026"),
                            "qualified": O["qualified"].dt.strftime("%Y-%m-%d"), "status": "active"}), FILES["roster"])
    cards = []
    for _, o in O.iterrows():
        if o["qualified"] >= pd.Timestamp(W.BADGE_MIGRATION):
            cards.append((o["badge_new"], int(o["emp"]), o["qualified"].strftime("%Y-%m-%d"), ""))
        else:
            cards.append((o["badge_old"], int(o["emp"]), o["qualified"].strftime("%Y-%m-%d"), o["card_reissued"].strftime("%Y-%m-%d")))
            cards.append((o["badge_new"], int(o["emp"]), o["card_reissued"].strftime("%Y-%m-%d"), ""))
    write_csv(pd.DataFrame(cards, columns=["badge", "operator_no", "issued", "withdrawn"]).sort_values(["operator_no", "issued"]), FILES["cards"])

    # 10 the maintenance system's defect reports (operator cards and inspection findings)
    Mm = Rr["mms"]
    write_csv(pd.DataFrame({"wo_no": Mm["wo_no"], "created": Mm["created"].dt.strftime("%Y-%m-%d %H:%M"),
                            "reported": Mm["reported"].dt.strftime("%Y-%m-%d"), "source": Mm["source"],
                            "car": Mm["car"].astype(int), "block": Mm["block"], "defect_group": Mm["group"],
                            "defect": Mm["defect"], "status": "Closed"}), FILES["mms"])

    # 14 to 17 distractors and context
    _distractors(rng)
    import docs
    docs.write_documents(TARGET, FILES, T, Rr)
    return T, Rr


def _distractors(rng):
    days = pd.date_range(W.OBS_START, W.OBS_END, freq="D")
    rows = []
    for c, base in (("PC-1 Laurel and 4th", 140), ("PC-2 Market Square", 210), ("PC-3 Pike and Arsenal", 95)):
        for d in days:
            wk = d.weekday() < 5
            for h in range(6, 22):
                lam = base * (1.6 if wk and h in (8, 12, 17) else 1.0) * (0.7 if not wk else 1.0)
                rows.append((c, d.strftime("%Y-%m-%d"), f"{h:02d}:00", int(rng.poisson(lam))))
    write_csv(pd.DataFrame(rows, columns=["counter", "date", "hour_start", "pedestrians"]), FILES["peds"])
    ev = sorted(rng.choice(days, W.ARENA_EVENTS_N, replace=False))
    write_csv(pd.DataFrame({"event_date": [pd.Timestamp(e).strftime("%Y-%m-%d") for e in ev],
                            "doors_open": [str(rng.choice(["17:30", "18:00", "18:30", "19:00"])) for _ in ev],
                            "event_type": [str(rng.choice(["concert", "hockey", "basketball", "family show"])) for _ in ev],
                            "tickets_scanned": rng.integers(2400, 11800, len(ev))}), FILES["arena"])
    secs = [s[0] for s in W.SECTIONS]
    tm = []
    for k in range(64):
        d = pd.Timestamp(rng.choice(days))
        tm.append((d.strftime("%Y-%m-%d"), str(rng.choice(secs)), str(rng.choice(["rail grinding", "switch inspection", "OCS tensioning",
                   "track geometry run", "drainage clearing", "embedded rail sealant"])), str(rng.choice(["00:30-04:30", "01:00-05:00", "23:45-04:15"]))))
    write_csv(pd.DataFrame(sorted(tm), columns=["work_date", "section_id", "activity", "possession"]), FILES["track"])
    sd = []
    for d in pd.date_range("2026-08-01", "2027-06-04", freq="D"):
        term = any(pd.Timestamp(a) <= d <= pd.Timestamp(b) for a, b in W.SCHOOL_TERMS) and not any(pd.Timestamp(a) <= d <= pd.Timestamp(b) for a, b in W.SCHOOL_BREAKS)
        if d.weekday() < 5:
            sd.append((d.strftime("%Y-%m-%d"), "student day" if term else "no school"))
    write_csv(pd.DataFrame(sd, columns=["date", "day_type"]), FILES["school"])


def cut_zip(zip_path=None):
    zip_path = zip_path or os.path.join(TASK, "target.zip")
    names = sorted(os.listdir(TARGET))
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for n in names:
            zi = zipfile.ZipInfo("target/" + n, date_time=FIXED_ZIP_TIME)
            zi.external_attr = 0o644 << 16
            zi.compress_type = zipfile.ZIP_DEFLATED
            with open(os.path.join(TARGET, n), "rb") as f:
                z.writestr(zi, f.read(), compresslevel=9)
    return zip_path
