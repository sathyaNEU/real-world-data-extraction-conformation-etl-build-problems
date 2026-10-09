"""Deterministic writers for every shipped data file."""
from __future__ import annotations

import math
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from datetime import timezone

from common import PST, QH, TZ, daterange, iso_local, lt_date
from world import BACKFED_POS, BACKFEED, GARAGES, N_UNITS, POS_PREFIX

SPINE = "session_intervals_2024-2026.parquet"
HEADER = "settled_sessions_2024-2026.csv"
DECISIONS = "restatement_decisions_2025.csv"
GATEWAY = "gateway_b_sessions_jan-apr2024.csv"
REGISTER = "station_register.csv"
SCHEDULE = "deck_panel_circuit_schedule.csv"
LOG = "deck_panel_meter_log_2024-2026.xlsx"
NAMEPLATES = "deck_submeter_nameplates.csv"
WORKORDERS = "facilities_work_orders_2026.csv"
PERMITS = "ev_permit_registry.csv"
CHECKS = "permit_vehicle_checks.csv"
REFERENCE = "vehicle_reference_list.csv"
FLEET = "city_fleet_roster.csv"
FLEETCARD = "fleet_card_ev_transactions_2024-2026.csv"
COURTESY = "curbline_courtesy_sessions_civic_decks_2024-2026.csv"
STATEMENTS = "ev_permit_charging_statements_2026.csv"
RATES = "nspl_schedule_26_ev_charging_service.pdf"
STANDARD = "fes-07_load_forecasting_standard_rev4.pdf"
GUIDE = "nspl_new_service_planning_guide_2026_sec7.pdf"
AGREEMENT = "civic_center_ev_service_agreement_draft.docx"
NOTES = "curbline_export_field_notes.txt"
SOURCES = "parking_services_data_sources.txt"
CAMPUS = "civic_center_campus_electric_statements_2024-2026.csv"
STATUS = "charger_status_events_2026.csv"
DISTRACTORS = [CAMPUS, STATUS]


def _csv(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False, lineterminator="\n")


def _d(x):
    if x is None or (isinstance(x, float) and math.isnan(x)) or x is pd.NaT:
        return ""
    return x.isoformat() if hasattr(x, "isoformat") else str(x)


# ------------------------------------------------------------------------------ settlement export
def write_header(w, path):
    r = w.rows[w.rows["in_ledger"]].copy()
    out = pd.DataFrame({
        "session_id": r["session_id"].astype("int64"),
        "version": r["version"].astype(int),
        "auth_code": r["auth_code"],
        "station_id": r["station_id"].astype("int64"),
        "plug_in": [iso_local(t) for t in r["start"]],
        "plug_out": [iso_local(t) for t in r["plug_out"]],
        "kwh_delivered": r["energy"].map(lambda x: f"{x:.3f}"),
        "account_type": r["acct"],
        "permit_no": r["permit_no"],
        "fleet_card": r["fleet_card"],
        "settled_on": [_d(x) for x in r["settled_on"]],
        "delivered_on": [_d(x) for x in r["delivered"]],
    })
    out = out.sort_values(["delivered_on", "session_id", "version"], kind="mergesort")
    _csv(out, path)
    return out


def write_spine(w, path):
    led_idx = w.rows.index[w.rows["in_ledger"].to_numpy()]
    rd = w.rd[w.rd["lrow"].isin(led_idx)]
    sid = w.rows["session_id"].to_numpy()
    ver = w.rows["version"].to_numpy()
    df = pd.DataFrame({"session_id": sid[rd["lrow"].to_numpy()].astype(np.int64),
                       "version": ver[rd["lrow"].to_numpy()].astype(np.int16),
                       "t": rd["interval_start"].to_numpy(np.int64), "kwh": rd["kwh"].to_numpy()})
    df = df.sort_values(["session_id", "version", "t"], kind="mergesort")
    table = pa.table({
        "session_id": pa.array(df["session_id"].to_numpy(), type=pa.int64()),
        "version": pa.array(df["version"].to_numpy(), type=pa.int16()),
        "interval_start": pa.array(df["t"].to_numpy() * 1000, type=pa.timestamp("ms", tz="America/Los_Angeles")),
        "kwh": pa.array(np.round(df["kwh"].to_numpy(), 3), type=pa.float64()),
    })
    pq.write_table(table, path, compression="zstd", compression_level=9, row_group_size=262144,
                   write_statistics=True)
    return len(df)


def write_decisions(w, path, rng):
    led = w.rows[w.rows["in_ledger"]]
    v1 = led[(led["version"] == 1) & (led["frag"] != 1)]
    sid_of = v1.drop_duplicates("row").set_index("row")["session_id"]
    d = w.decisions.copy()
    reviewers = ["T. Pierce", "T. Pierce", "A. Warner"]
    out = pd.DataFrame({
        "session_id": d["row"].map(sid_of).astype("int64"),
        "version": d["version"].astype(int),
        "received_on": [_d(x) for x in d["received"]],
        "decision": np.where(d["accepted"], "ACCEPTED", "REJECTED"),
        "decided_on": [_d(x) for x in d["decided"]],
        "reviewed_by": [reviewers[int(rng.integers(len(reviewers)))] for _ in range(len(d))],
    })
    out = out.sort_values(["received_on", "session_id", "version"], kind="mergesort")
    _csv(out, path)
    return out


def write_gateway(w, path, rng):
    g = w.rows[w.rows["gateway_b"].fillna(False).astype(bool)].sort_values("start")
    txn = 7701000 + np.cumsum(rng.integers(1, 5, len(g)))

    def fmt(t):
        return datetime.fromtimestamp(int(t), TZ).strftime("%m/%d/%Y %H:%M:%S")
    out = pd.DataFrame({"Txn No": txn, "Station": g["station_id"].astype("int64").to_numpy(),
                        "Card": g["permit_no"].to_numpy(), "Start": [fmt(t) for t in g["start"]],
                        "Stop": [fmt(t) for t in g["plug_out"]],
                        "Energy (Wh)": np.round(g["energy"].to_numpy() * 1000).astype(np.int64),
                        "Auth Code": g["auth_code"].to_numpy()})
    _csv(out, path)
    return out


# ------------------------------------------------------------------------------ registers
def write_register(w, path):
    r = w.register.copy()
    r["in_service_from"] = [_d(x) for x in r["in_service_from"]]
    r["in_service_to"] = [_d(x) for x in r["in_service_to"]]
    r["rating_kw"] = r["rating_kw"].map(lambda x: f"{x:.1f}")
    r = r.sort_values(["garage", "position", "in_service_from"], kind="mergesort")
    _csv(r[["station_id", "garage", "position", "unit_model", "rating_kw", "in_service_from", "in_service_to"]], path)
    return r


def circuits():
    slots = []
    a, b = 1, 2
    for i in range(16):
        if i % 2 == 0:
            slots.append(f"{a}/{a + 2}")
            a += 4
        else:
            slots.append(f"{b}/{b + 2}")
            b += 4
    return slots


def write_schedule(path):
    rows = []
    slots = circuits()
    for panel, deck, inst, light in (("CP-N", "N", date(2020, 9, 14), 2400), ("CP-S", "S", date(2021, 3, 22), 2100)):
        for i, c in enumerate(slots, start=1):
            pos = f"{deck}-{i:02d}"
            if pos == BACKFED_POS:
                rows.append([panel, c, f"EVSE {pos}", 6600, inst, BACKFEED[0] - timedelta(days=1)])
                rows.append([panel, c, f"EVSE {pos}", 6600, BACKFEED[1] + timedelta(days=1), None])
            else:
                rows.append([panel, c, f"EVSE {pos}", 6600, inst, None])
        rows.append([panel, "33", "Roof level pole lights, photocell", light, inst, None])
        rows.append([panel, "34", "Spare", 0, inst, None])
        rows.append([panel, "35/37", "Spare", 0, inst, None])
        rows.append([panel, "36/38", "Space", 0, inst, None])
    hp = [("HP-N", "1/3/5", "Elevator 1", 15000), ("HP-N", "2/4/6", "Stair pressurization fan", 7500),
          ("HP-N", "7", "Stair and lobby lighting", 1200), ("HP-N", "8", "Exit signs, emergency lighting", 400),
          ("HP-N", "9", "Parking office receptacles", 1800), ("HP-N", "10", "Pay station power, level 1", 600),
          ("HP-N", "11/13", "Exhaust fan EF-1", 3700)]
    for p, c, desc, va in hp:
        rows.append([p, c, desc, va, date(2020, 9, 14), None])
    rows.append(["HP-N", "14/16", "Spare", 0, date(2020, 9, 14), BACKFEED[0] - timedelta(days=1)])
    rows.append(["HP-N", "14/16", f"EVSE {BACKFED_POS}, temporary feed (WO-26-0418)", 6600, BACKFEED[0], BACKFEED[1]])
    rows.append(["HP-N", "14/16", "Spare", 0, BACKFEED[1] + timedelta(days=1), None])
    df = pd.DataFrame(rows, columns=["panel", "circuit", "description", "load_va", "effective_from", "effective_to"])
    df["effective_from"] = [_d(x) for x in df["effective_from"]]
    df["effective_to"] = [_d(x) for x in df["effective_to"]]
    _csv(df, path)
    return df


def write_nameplates(path):
    df = pd.DataFrame([
        ["SM-2231", "CP-N", "North Deck, level 1 electrical room", "Accuenergy", "Acuvim-L", "AL21-084417",
         "200:5", "2023-11-14", "Pacific Standard Time (UTC-08:00)", "Disabled", 15, "0.1 kWh"],
        ["SM-2232", "CP-S", "South Deck, level 1 electrical room", "Accuenergy", "Acuvim-L", "AL21-084452",
         "200:5", "2023-11-14", "Pacific Standard Time (UTC-08:00)", "Disabled", 15, "0.1 kWh"]],
        columns=["meter_id", "panel", "location", "make", "model", "serial_no", "ct_ratio", "installed",
                 "clock_time_base", "dst_adjustment", "demand_interval_min", "kwh_display_resolution"])
    _csv(df, path)
    return df


def write_work_orders(path):
    rows = [
        ["WO-26-0034", "2026-01-12", "2026-01-13", "City Hall", "AHU-3", "Replace supply fan belt", "Closed", "HVAC"],
        ["WO-26-0091", "2026-01-22", "2026-01-22", "Civic Center South Deck", "CP-S ckt 9/11",
         "EVSE S-05 tripping. Replaced GFCI breaker, tested OK", "Closed", "Electrical"],
        ["WO-26-0127", "2026-02-03", "2026-02-05", "Main Library", "Lighting", "Replace 6 failed LED troffers, stack level",
         "Closed", "Electrical"],
        ["WO-26-0188", "2026-02-24", "2026-02-24", "Civic Center North Deck", "HP-N ckt 7",
         "Stair 2 lights out levels 3-4. Reset breaker, replaced photocell sensor", "Closed", "Electrical"],
        ["WO-26-0215", "2026-03-09", "2026-03-11", "Civic Center North Deck", "Elevator 1", "Annual state elevator inspection",
         "Closed", "Contractor"],
        ["WO-26-0262", "2026-03-23", "2026-03-23", "Civic Center South Deck", "Pay station L1",
         "Pay station not printing. Replaced printer module", "Closed", "Parking"],
        ["WO-26-0301", "2026-04-08", "2026-04-09", "City Hall", "Generator", "Quarterly load bank test", "Closed",
         "Electrical"],
        ["WO-26-0347", "2026-04-27", "2026-04-27", "Civic Center South Deck", "CP-S ckt 33",
         "Roof pole light P-7 cycling. Replaced driver", "Closed", "Electrical"],
        ["WO-26-0418", "2026-05-28", "2026-07-13", "Civic Center North Deck", "CP-N ckt 21/23",
         "Branch conductor to EVSE N-11 damaged at level 3 cable tray. Refeed N-11 from HP-N ckt 14/16 until "
         "branch is replaced. 07/12: new branch pulled and terminated, N-11 restored to CP-N 21/23, HP-N 14/16 "
         "back to spare", "Closed", "Electrical"],
        ["WO-26-0455", "2026-06-15", "2026-06-16", "Main Library", "Roof", "Clear roof drains", "Closed", "Building"],
        ["WO-26-0503", "2026-07-06", "2026-07-06", "Civic Center North Deck", "Exhaust fan EF-1",
         "Noisy bearing. Lubricated, monitor", "Closed", "HVAC"],
        ["WO-26-0529", "2026-07-21", "2026-07-21", "Civic Center North Deck", "EVSE N-07",
         "Connector latch sticking. County fleet attendant reports it on swaps between pool cars. Replaced latch, "
         "tested OK", "Closed", "Electrical"],
        ["WO-26-0560", "2026-08-03", "2026-08-04", "City Hall", "Chiller 1", "Condenser tube cleaning", "Closed",
         "Contractor"],
        ["WO-26-0612", "2026-08-25", "2026-08-25", "Civic Center South Deck", "Signage",
         "Replace damaged EV parking sign, level 2", "Closed", "Parking"],
        ["WO-26-0671", "2026-09-17", "2026-09-18", "Civic Center North Deck", "CP-N", "Infrared scan of panel CP-N",
         "Closed", "Electrical"],
        ["WO-26-0672", "2026-09-17", "2026-09-18", "Civic Center South Deck", "CP-S", "Infrared scan of panel CP-S",
         "Closed", "Electrical"],
        ["WO-26-0738", "2026-10-12", "2026-10-12", "Main Library", "Elevator 2", "Door operator adjustment", "Closed",
         "Contractor"],
        ["WO-26-0790", "2026-11-02", "2026-11-03", "Civic Center North Deck", "CP-N ckt 33",
         "Roof pole lights on during day. Cleaned and re-aimed photocell", "Closed", "Electrical"],
        ["WO-26-0846", "2026-11-23", "2026-11-23", "City Hall", "Boiler 2", "Annual combustion test", "Closed", "HVAC"],
        ["WO-26-0901", "2026-12-14", "2026-12-15", "Civic Center South Deck", "Stair 1",
         "Handrail loose level 2. Re-anchored", "Closed", "Building"],
        ["WO-26-0937", "2026-12-28", None, "Civic Center North Deck", "EVSE replacement",
         "Pre-construction walk with contractor for unit replacement, both decks", "Open", "Electrical"],
    ]
    df = pd.DataFrame(rows, columns=["wo_no", "opened", "closed", "building", "asset", "description", "status",
                                     "shop"])
    df["closed"] = df["closed"].fillna("")
    _csv(df, path)
    return df


def write_permits(w, path):
    permits = w.veh["permits"].copy()
    checks = w.veh["checks"]
    last = checks.groupby("permit_no")["checked_on"].max()
    out = pd.DataFrame({
        "permit_no": permits["permit_no"], "deck": permits["deck"], "holder": permits["holder"],
        "holder_type": permits["holder_type"], "issued": [_d(x) for x in permits["issued"]],
        "last_renewed": [_d(x) for x in permits["permit_no"].map(last)], "status": permits["status"]})
    out = out.sort_values("permit_no", kind="mergesort")
    _csv(out, path)
    return out


def write_checks(w, path):
    c = w.veh["checks"].copy().reset_index(drop=True)
    c.insert(0, "check_no", [f"VC-{40211 + 3 * i + (i % 3)}" for i in range(len(c))])
    c["checked_on"] = [_d(x) for x in c["checked_on"]]
    c["result"] = "MATCH"
    _csv(c, path)
    return c


def write_reference(path):
    from world import reference_frame
    r = reference_frame()
    r["onboard_charger_kw"] = r["onboard_charger_kw"].map(lambda x: f"{x:.1f}")
    r = r.rename(columns={"fuel": "fuel_type"})
    _csv(r, path)
    return r


def write_fleet(w, path):
    f = w.veh["fleet"].copy()
    f["in_service"] = [_d(x) for x in f["in_service"]]
    out = f[["unit_no", "fleet_card", "department", "make", "model", "trim", "model_year", "plate", "vin",
             "in_service"]]
    _csv(out, path)
    return out


SITE = {"CCN": "CURBLINE LARCH HBR CIVIC CTR NORTH", "CCS": "CURBLINE LARCH HBR CIVIC CTR SOUTH",
        "LIB": "CURBLINE LARCH HBR LIBRARY GAR", "FTG": "CURBLINE LARCH HBR FERRY TERM", "MSG": "CURBLINE LARCH HBR MARKET SQ",
        "CSG": "CURBLINE LARCH HBR CEDAR ST", "SWG": "CURBLINE LARCH HBR SEAWALL", "ETG": "CURBLINE LARCH HBR EASTSIDE TC"}


def write_fleet_card(w, path, rng):
    """The fleet card processor's transaction file: every fleet card charge at a Curbline station, 2024 to 2026."""
    r = w.rows
    f = r[(r["acct"] == "FLEET") & r["true_row"] & ~r["redelivered"]].copy()
    f = f[(f["day"] >= date(2024, 1, 1)) & (f["day"] <= date(2026, 12, 31))].sort_values(["settled_on", "start"])
    roster = w.veh["fleet"].set_index("fleet_card")
    tid = 50318000 + np.cumsum(rng.integers(3, 41, len(f)))

    def ts(t):
        # the processor posts START and END on its own clock, UTC
        return datetime.fromtimestamp(int(t), timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    price = np.where(f["day"].to_numpy() < date(2025, 7, 1), 0.214, 0.229)
    out = pd.DataFrame({
        "TRANS_ID": tid,
        "POST_DATE": [x.strftime("%m/%d/%Y") for x in f["settled_on"]],
        "CARD_NO": f["fleet_card"].to_numpy(),
        "UNIT_NO": f["fleet_card"].map(roster["unit_no"]).to_numpy(),
        "DEPT": f["fleet_card"].map(roster["department"]).str.upper().to_numpy(),
        "MERCHANT_SITE": f["garage"].map(SITE).to_numpy(),
        "STATION": f["station_id"].astype("int64").to_numpy(),
        "START": [ts(t) for t in f["start"]],
        "END": [ts(t) for t in f["plug_out"]],
        "KWH": f["energy"].map(lambda x: f"{x:.3f}").to_numpy(),
        "AMOUNT": [f"{round(e * p + 1e-9, 2):.2f}" for e, p in zip(f["energy"], price)],
        "NETWORK_REF": f["auth_code"].to_numpy(),
    })
    _csv(out, path)
    return out


# ------------------------------------------------------------------------------ the electricians' log
def write_log(w, path):
    import xlsxwriter
    log = w.log.copy()
    wb = xlsxwriter.Workbook(path, {"constant_memory": False})
    wb.set_properties({"title": "Civic Center deck charging panels, monthly reads", "author": "Facilities Electrical",
                       "company": "City of Larch Harbor", "created": datetime(2027, 1, 4, 8, 12, 0)})
    ws = wb.add_worksheet("Reads")
    bold = wb.add_format({"bold": True})
    hdr = wb.add_format({"bold": True, "bottom": 1, "text_wrap": True, "valign": "bottom"})
    datef = wb.add_format({"num_format": "yyyy-mm-dd"})
    num1 = wb.add_format({"num_format": "#,##0.0"})
    ws.write(0, 0, "Civic Center decks, EV charging panel sub-meters: monthly reads", bold)
    ws.write(1, 0, "Reads for panel loading checks. kWh and max demand as displayed on the meter. Max demand is the "
                   "highest 15-minute demand since the last reset, all hours; demand is reset at each monthly read. "
                   "Where a meter is read more than once in a day, the later reading stands.")
    heads = ["Read date", "Read time (meter)", "Meter", "Panel", "kWh register", "Max demand (kW)", "Demand reset",
             "Read by"]
    for j, h in enumerate(heads):
        ws.write(3, j, h, hdr)
    for i, r in enumerate(log.itertuples(index=False), start=4):
        ws.write_datetime(i, 0, datetime(r.read_date.year, r.read_date.month, r.read_date.day), datef)
        ws.write_string(i, 1, r.read_time)
        ws.write_string(i, 2, r.meter)
        ws.write_string(i, 3, r.panel)
        ws.write_number(i, 4, float(r.kwh), num1)
        if r.max_kw is None or (isinstance(r.max_kw, float) and math.isnan(r.max_kw)):
            ws.write_blank(i, 5, None)
        else:
            ws.write_number(i, 5, float(r.max_kw), num1)
        ws.write_string(i, 6, r.reset)
        ws.write_string(i, 7, r.by)
    ws.set_column(0, 0, 11)
    ws.set_column(1, 1, 10)
    ws.set_column(2, 3, 9)
    ws.set_column(4, 5, 13)
    ws.set_column(6, 7, 8)
    ws.freeze_panes(4, 0)
    wc = wb.add_worksheet("Corrections")
    wc.write(0, 0, "Corrected reads", bold)
    wc.write(1, 0, "A corrected reading replaces the reading logged for that date on the Reads sheet.")
    cheads = ["Read date", "Meter", "Panel", "kWh as logged", "kWh corrected", "Corrected on", "By", "Note"]
    for j, h in enumerate(cheads):
        wc.write(3, j, h, hdr)
    for i, r in enumerate(w.fixes.itertuples(index=False), start=4):
        wc.write_datetime(i, 0, datetime(r.read_date.year, r.read_date.month, r.read_date.day), datef)
        wc.write_string(i, 1, r.meter)
        wc.write_string(i, 2, r.panel)
        wc.write_number(i, 3, float(r.kwh_logged), num1)
        wc.write_number(i, 4, float(r.kwh_corrected), num1)
        wc.write_datetime(i, 5, datetime(r.corrected_on.year, r.corrected_on.month, r.corrected_on.day), datef)
        wc.write_string(i, 6, r.by)
        wc.write_string(i, 7, r.note)
    wc.set_column(0, 0, 11)
    wc.set_column(1, 2, 9)
    wc.set_column(3, 5, 13)
    wc.set_column(6, 6, 6)
    wc.set_column(7, 7, 26)
    wc.freeze_panes(4, 0)
    wb.close()


# ------------------------------------------------------------------------------ distractors
def write_campus(w, path, rng):
    """NSPL statements for the Civic Center campus service (City Hall, Main Library and, until the new
    service, the two decks' charging panels). Meter-read billing cycles of 27 to 34 days."""
    from meters import PANELS
    books = w.books
    reads = [date(2023, 12, 28)]
    while True:
        nxt = reads[-1] + timedelta(days=int(rng.integers(27, 35)))
        if nxt > date(2026, 12, 31):
            break
        reads.append(nxt)
    rows = []
    for a, b in zip(reads[:-1], reads[1:]):
        ta, tb = lt_date(a, 7), lt_date(b, 7)
        deck = sum(float(books.c[(False, False, False, False)][p][(tb - books_t0()) // QH]
                         - books.c[(False, False, False, False)][p][(ta - books_t0()) // QH]) for p in PANELS)
        days = (b - a).days
        winter = b.month in (11, 12, 1, 2, 3)
        base = days * (5650 if winter else 6100) * float(rng.uniform(0.96, 1.04))
        total = base + deck
        onpk = total * float(rng.uniform(0.47, 0.53))
        bd = float(rng.uniform(560, 650) if winter else rng.uniform(640, 760))
        amount = 412.0 + 9.85 * 800 + 0.1281 * onpk + 0.0874 * (total - onpk)
        rows.append({"account_no": "4410-2209-17", "service": "Civic Center campus, 600 Harbor Ave",
                     "statement_date": (b + timedelta(days=4)).isoformat(), "period_start": a.isoformat(),
                     "period_end": b.isoformat(), "days": days, "kwh_on_peak": int(round(onpk)),
                     "kwh_off_peak": int(round(total - onpk)), "kwh_total": int(round(total)),
                     "billing_demand_kw": round(bd, 1), "contract_demand_kw": 800,
                     "power_factor_pct": round(float(rng.uniform(91.5, 96.8)), 1), "amount_usd": f"{amount:.2f}"})
    df = pd.DataFrame(rows)
    df = df[df["period_end"] >= "2024-01-01"]
    _csv(df, path)
    return df


def books_t0():
    from common import GRID_T0
    return GRID_T0


def write_status(w, path, rng):
    """Station status events, 2026: overnight firmware windows by garage, communication drops, and a few
    faults, all at times the station had no vehicle charging."""
    rows = w.rows[(w.rows["in_ledger"] | w.rows["courtesy"].fillna(False).astype(bool)) & w.rows["true_row"]]
    busy = {}
    for sid, st, en in zip(rows["station_id"], rows["start"], rows["plug_out"]):
        busy.setdefault(int(sid), []).append((int(st), int(en)))
    reg = w.register
    cur = reg[reg["in_service_to"].isna()]
    events = []

    def free(sid, a, b):
        return all(b <= s or a >= e for s, e in busy.get(sid, []))

    fw_days = {g: [] for g in cur["garage"].unique()}
    for g in fw_days:
        for m in (2, 5, 8, 11):
            d = date(2026, m, int(rng.integers(3, 25)))
            while d.weekday() >= 5:
                d += timedelta(days=1)
            fw_days[g].append(d)
    for _, r in cur.sort_values(["garage", "position"]).iterrows():
        sid = int(r["station_id"])
        for d in fw_days[r["garage"]]:
            a = lt_date(d + timedelta(days=1), 1, int(rng.integers(5, 40)))
            b = a + int(rng.integers(18, 55)) * 60
            if free(sid, a - 600, b + 600):
                events.append((a, sid, "UNAVAILABLE", "FIRMWARE_UPDATE"))
                events.append((b, sid, "AVAILABLE", ""))
        for _ in range(int(rng.poisson(3))):
            d = date(2026, 1, 1) + timedelta(days=int(rng.integers(0, 365)))
            a = lt_date(d, int(rng.integers(0, 23)), int(rng.integers(0, 59)))
            b = a + int(rng.integers(3, 95)) * 60
            events.append((a, sid, "OFFLINE", "COMMUNICATION_LOSS"))
            events.append((b, sid, "ONLINE", ""))
        if rng.random() < 0.18:
            for _ in range(60):
                d = date(2026, 1, 1) + timedelta(days=int(rng.integers(0, 365)))
                a = lt_date(d, int(rng.integers(0, 23)), int(rng.integers(0, 59)))
                b = a + int(rng.integers(40, 400)) * 60
                if free(sid, a - 900, b + 900):
                    events.append((a, sid, "FAULTED", rng.choice(["GROUND_FAULT", "CONNECTOR_LOCK_FAILURE",
                                                                   "OVER_TEMPERATURE"]).item()))
                    events.append((b, sid, "AVAILABLE", ""))
                    break
    ev = pd.DataFrame(events, columns=["t", "station_id", "status", "reason"]).sort_values(["t", "station_id"],
                                                                                            kind="mergesort")
    ev = ev[(ev["t"] >= lt_date(date(2026, 1, 1))) & (ev["t"] < lt_date(date(2027, 1, 1)))]
    out = pd.DataFrame({"event_id": np.arange(880211, 880211 + len(ev)), "station_id": ev["station_id"].to_numpy(),
                        "event_time": [iso_local(t) for t in ev["t"]], "status": ev["status"].to_numpy(),
                        "reason": ev["reason"].to_numpy()})
    _csv(out, path)
    return out


# ------------------------------------------------------------------------------ courtesy sessions and statements
def write_courtesy(w, path, rng):
    """Curbline's courtesy-session report for the two decks: charging on Saturdays, Sundays and the Schedule 26
    holidays, which is free to permit holders and is not settled, so it never reaches the settlement export."""
    c = w.rows[w.rows["courtesy"].fillna(False).astype(bool)].sort_values(["start", "garage", "position"])
    ref = 61200400 + np.cumsum(rng.integers(1, 6, len(c)))

    def ts(t):
        return datetime.fromtimestamp(int(t), TZ).strftime("%Y-%m-%d %H:%M:%S")
    out = pd.DataFrame({"Courtesy Ref": [f"CT{x}" for x in ref], "Station": c["station_id"].astype("int64").to_numpy(),
                        "Permit": c["permit_no"].to_numpy(), "Connected": [ts(t) for t in c["start"]],
                        "Disconnected": [ts(t) for t in c["plug_out"]],
                        "Energy (kWh)": c["energy"].map(lambda x: f"{x:.3f}").to_numpy()})
    _csv(out, path)
    return out


SESSION_FEE, ENERGY_RATE = 0.50, 0.218


def write_statements(w, path):
    """Parking Services' monthly EV charging statements to Civic Center permit holders, 2026: each charge billed
    a session fee plus the energy delivered."""
    r = w.rows
    t = r[r["in_ledger"] & r["true_row"] & ~r["redelivered"] & r["garage"].isin(["CCN", "CCS"])
          & (r["acct"] == "PERMIT") & (r["day"] >= date(2026, 1, 1)) & (r["day"] <= date(2026, 12, 31))].copy()
    t["period"] = [f"{d.year}-{d.month:02d}" for d in t["day"]]
    g = t.groupby(["permit_no", "period"]).agg(charges=("row", "nunique"), kwh=("energy", "sum")).reset_index()
    g = g.sort_values(["period", "permit_no"], kind="mergesort").reset_index(drop=True)
    fees = np.round(SESSION_FEE * g["charges"].to_numpy() + 1e-9, 2)
    energy = np.round(ENERGY_RATE * g["kwh"].to_numpy() + 1e-9, 2)
    out = pd.DataFrame({"statement_no": [f"EVP-26{p[5:]}-{i:04d}" for i, p in enumerate(g["period"], start=1)],
                        "permit_no": g["permit_no"], "period": g["period"], "charges": g["charges"].astype(int),
                        "kwh": g["kwh"].map(lambda x: f"{x:.3f}"), "session_fees": [f"{x:.2f}" for x in fees],
                        "energy_charge": [f"{x:.2f}" for x in energy],
                        "amount_due": [f"{a + b:.2f}" for a, b in zip(fees, energy)]})
    _csv(out, path)
    return out
