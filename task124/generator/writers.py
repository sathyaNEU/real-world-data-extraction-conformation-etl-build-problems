"""Deterministic writers for every shipped data file."""
from __future__ import annotations

import math
from datetime import date, datetime

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import desk as K
from common import BOOKS, CODE, EXTRACT, PEAKS, SUMMERS, daterange, nerc_holidays

SPINE = "idr_hourly_reads_summers_2017_2026.parquet"
SETTLED = "zone_settled_load_s17_s26.csv"
PEAKLIST = "ercot_summer_system_peaks.csv"
ENROL = "enrollment_extract_20270409.csv"
PREMISES = "premise_register_20270409.csv"
SWITCHES = "switch_confirms_spring_2027.csv"
POSITIONS = "hedge_positions_20270409.xlsx"
CREDITS = "bsaver_credits_2017_2026.csv"
ACCOUNTS = "billing_accounts.csv"
ROSTER = "bsaver_roster_2027.xlsx"
TERMS = "business_saver_terms.pdf"
POLICY = "summer_risk_policy_2027.docx"
MINUTE = "rc_minute_2027-03-19.pdf"
REPORT = "summer_2026_risk_report.pdf"
QUOTES = "option_quotes_s27.csv"
PECOS = "pecos_quote_sheet_apr2027.xlsx"
DECISIONS = "quote_decisions.csv"
CPTYS = "desk_counterparties.csv"
BOOKMAP = "book_zone_map.csv"
BLOTTER = "trade_blotter_s27.csv"
MATCHLOG = "confirm_match_log.csv"
PORTFOLIOS = "portfolio_books.csv"
CALENDAR = "trading_calendar_2027.csv"
PROCEDURES = "desk_procedures.docx"
TEMPS = "zone_daily_temps_2017_2026.csv"
OUTLOOK = "ercot_zone_peak_outlook_2027.xlsx"
NOTES = "field_notes.md"
LOG = "extract_log.md"
DISTRACTORS = [TEMPS, OUTLOOK]

ACCT_WORDS = ["Arrowhead", "Caliche", "Dalworth", "Flatrock", "Gulfgate", "Ironbridge", "Kingsway", "Pinecrest",
              "Quarry Hill", "Ridgeline", "Stonegate", "Upland", "Westfork", "Brushy Creek", "Cotton Belt",
              "Prairie Star", "Redbud", "Saddle Creek", "Twin Oaks", "Hackberry", "Mustang Draw", "Coyote Run",
              "Pecan Hollow", "Sandstone", "Lariat", "Sagebrush", "Windmill", "Blackland", "Post Oak Bend",
              "Three Forks", "Lone Elm", "Salt Flat", "Big Spring Road", "Highline", "Longhorn Yard", "Red Clay"]
ACCT_KIND = {"office": ["Office Park", "Plaza Partners", "Business Center", "Tower Partners"],
             "flat": ["Data Center", "Colocation Center"], "hospital": ["Medical Plaza", "Hotel & Suites", "Surgical Center"],
             "plant": ["Plastics", "Chemical Works", "Metal Fabrication", "Machine Works", "Components"],
             "warehouse": ["Distribution Center", "Logistics Park", "Industrial Supply"],
             "retail": ["Wholesale Club", "Shopping Center", "Home Center"]}
SUFFIX = ["LLC", "Inc", "LP", "Ltd"]


def _csv(df, path):
    df.to_csv(path, index=False, lineterminator="\n")


def _d(x):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return ""
    return x.isoformat()


# ------------------------------------------------------------------------------ reads and loads
def write_spine(w, path):
    r = pd.concat([w.mreads, w.ireads], ignore_index=True)
    r = r.sort_values(["esi_id", "date", "he"], kind="mergesort")
    table = pa.table({
        "esi_id": pa.array(r["esi_id"].to_numpy(), type=pa.string()),
        "read_date": pa.array(r["date"].to_numpy(), type=pa.date32()),
        "hour_ending": pa.array(r["he"].to_numpy().astype(np.int8), type=pa.int8()),
        "kwh": pa.array(r["kwh"].to_numpy().astype(np.float64), type=pa.float64()),
    })
    pq.write_table(table, path, compression="zstd", compression_level=9, row_group_size=262144,
                   write_statistics=True)
    return len(r)


def write_settled(w, path):
    s = w.settled.copy()
    s["code"] = s["book"].map(CODE)
    wide = s.pivot_table(index=["date", "he"], columns="code", values="mwh", aggfunc="first").reset_index()
    wide = wide.sort_values(["date", "he"], kind="mergesort")
    out = pd.DataFrame({"oper_day": [d.isoformat() for d in wide["date"]], "hour_ending": wide["he"].astype(int)})
    for b in BOOKS:
        out[CODE[b]] = wide[CODE[b]].map(lambda x: f"{x:.3f}")
    out["settlement"] = "TRUE-UP"
    _csv(out, path)
    return out


def write_peaks(path):
    rows = [{"summer": y, "peak_date": d.isoformat(), "hour_ending": h, "ercot_load_mw": mw}
            for y, (d, h, mw) in PEAKS.items()]
    _csv(pd.DataFrame(rows), path)


# ------------------------------------------------------------------------------ enrolment and premises
def write_enrolment(w, path):
    p = w.prem
    out = pd.DataFrame({
        "enrollment_id": p["enrollment_id"], "esi_id": p["esi_id"], "record_type": p["record_type"],
        "book": p["book"].map(CODE), "tdsp": p["tdsp"], "plan_code": p["plan"], "deposit_class": p["deposit"],
        "meter_type": p["meter"], "premise_age_band": p["age_band"],
        "max_demand_kw": p["md_kw"].map(lambda x: f"{x:.1f}"), "broker_code": p["broker"],
        "entered_on": [_d(x) for x in p["entered_on"]], "start_date": [_d(x) for x in p["start"]],
        "end_date": [_d(x) for x in p["end"]],
    })
    _csv(out, path)
    return out


def _profile(rng, comp, zone):
    if comp == "prof":
        t = str(rng.choice(["BUSLOLF", "BUSMEDLF", "BUSHILF", "BUSNODEM"], p=[0.38, 0.34, 0.2, 0.08]))
        return f"{t}_{zone}_NIDR_NOTOU_NODG"
    return f"BUSIDRRQ_{zone}_IDR_NOTOU_NODG"


def write_premises(w, path, rng):
    p = w.prem[w.prem["record_type"] == "NEW"].drop_duplicates("esi_id")
    active = set(p.loc[p["end"].isna(), "esi_id"])
    out = pd.DataFrame({
        "esi_id": p["esi_id"], "tdsp": p["tdsp"],
        "load_profile": [_profile(rng, c, CODE[b]) for c, b in zip(p["comp"], p["book"])],
        "naics_code": p["naics"],
        "service_voltage": [("PRIMARY" if (c != "prof" and rng.uniform() < 0.22) else "SECONDARY") for c in p["comp"]],
        "premise_status": ["ACTIVE" if e in active else "INACTIVE" for e in p["esi_id"]],
    })
    out = out.sort_values("esi_id", kind="mergesort")
    _csv(out, path)
    return out


def write_switches(w, path, rng):
    p = w.prem
    s = p[(p["record_type"] == "NEW") & (p["start"] >= date(2026, 10, 1)) & (p["start"] <= EXTRACT)].copy()
    s = s.sort_values(["start", "esi_id"], kind="mergesort")
    typ = np.where(s["comp"] == "centre", "MOVE-IN", np.where(rng.uniform(size=len(s)) < 0.12, "MOVE-IN", "SWITCH"))
    base = 908_441_200 + np.cumsum(rng.integers(1, 30, len(s)))
    req = [d - pd.Timedelta(days=int(k)).to_pytimedelta() for d, k in zip(s["start"], rng.integers(2, 12, len(s)))]
    out = pd.DataFrame({"tran_id": [f"{'MVI' if t == 'MOVE-IN' else 'SWI'}{x}" for t, x in zip(typ, base)],
                        "esi_id": s["esi_id"].to_numpy(), "tran_type": typ, "tdsp": s["tdsp"].to_numpy(),
                        "requested_date": [d.isoformat() for d in req],
                        "effective_date": [d.isoformat() for d in s["start"]]})
    _csv(out, path)
    return out


def account_frame(w, rng):
    """Billing accounts for every IDR premise: the members' and Harlan Ridge's accounts as filed, the general IDR
    premises grouped under customers."""
    p = w.prem[(w.prem["record_type"] == "NEW") & (w.prem["meter"] == "IDR")]
    rows = []
    used = set()
    for _, r in p[p["comp"] == "ref"].iterrows():
        rows.append((r["account"], r["esi_id"], r["customer"], r["start"], r["end"]))
        used.add(r["account"])
    cen = p[p["comp"] == "centre"]
    for _, r in cen.iterrows():
        rows.append(("SC-4497203", r["esi_id"], r["customer"], r["start"], None))
    gen = p[p["comp"] == "idr"].sort_values(["start", "esi_id"], kind="mergesort")
    nxt = [4420000]
    names = set()
    cur = None
    for _, r in gen.iterrows():
        if r["twin"]:
            rows.append(("SC-4410944", r["esi_id"], r["customer"], r["start"], r["end"]))
            continue
        if cur is None or rng.uniform() > 0.18 or cur[2] != r["family"]:
            while True:
                nm = f"{rng.choice(ACCT_WORDS)} {rng.choice(ACCT_KIND[r['family']])} {rng.choice(SUFFIX)}"
                if nm not in names:
                    names.add(nm)
                    break
            nxt[0] += int(rng.integers(40, 900))
            cur = (f"SC-{nxt[0]}", nm, r["family"])
        rows.append((cur[0], r["esi_id"], cur[1], r["start"], r["end"]))
    df = pd.DataFrame(rows, columns=["account_no", "esi_id", "account_name", "start", "end"])
    return df


def write_accounts(acc, path):
    out = pd.DataFrame({"account_no": acc["account_no"], "esi_id": acc["esi_id"], "account_name": acc["account_name"],
                        "bill_type": "IDR SUMMARY", "service_from": [_d(x) for x in acc["start"]],
                        "service_to": [_d(x) for x in acc["end"]]})
    out = out.sort_values(["account_no", "esi_id"], kind="mergesort")
    _csv(out, path)
    return out


def write_credits(w, path):
    c = w.credits.sort_values(["date", "account"], kind="mergesort")
    out = pd.DataFrame({"account_no": c["account"], "event_date": [d.isoformat() for d in c["date"]],
                        "window_start": "14:00", "window_end": "18:00", "credited_kwh": c["kwh"].astype(int),
                        "credit_usd": c["usd"].map(lambda x: f"{x:.2f}"),
                        "bill_month": [f"{d.year}-{d.month + 1:02d}" if d.month < 12 else f"{d.year + 1}-01" for d in c["date"]]})
    _csv(out, path)
    return out


# ------------------------------------------------------------------------------ desk files
def write_quotes(w, path):
    q = w.quotes[w.quotes["broker"] != "PPB"].sort_values(["sent", "qid", "rev"], kind="mergesort")
    out = pd.DataFrame({"quote_id": q["qid"].astype(int), "revision": q["rev"].astype(int),
                        "broker": q["broker"].map({"GEB": "Gulfline", "TBC": "Trinity Basin"}),
                        "cpty_code": q["cpty"], "load_zone": q["zone"],
                        "delivery_month": [f"2027-{m:02d}" for m in q["month"]], "strike": "250.00",
                        "premium": q["price"].map(lambda x: f"{x:.2f}"),
                        "sent_at": [t.strftime("%Y-%m-%d %H:%M:%S") for t in q["sent"]]})
    _csv(out, path)
    return out


def write_decisions(w, path, rng):
    q = w.quotes.copy()
    q["ref"] = [str(x) for x in q["qid"]]
    q = q.sort_values(["sent", "ref", "rev"], kind="mergesort")
    lag = rng.integers(4, 95, len(q))
    out = pd.DataFrame({"quote_ref": q["ref"], "revision": q["rev"].astype(int), "decision": q["decision"],
                        "decided_at": [(t + pd.Timedelta(minutes=int(k)).to_pytimedelta()).strftime("%Y-%m-%d %H:%M")
                                       for t, k in zip(q["sent"], lag)],
                        "trader": [str(rng.choice(["GS", "MR", "JT", "MR"])) for _ in range(len(q))]})
    _csv(out, path)
    return out


def write_cptys(path):
    lim = {"C0112": 40, "C0147": 25, "C0188": 15, "C0203": 30, "C0231": 20, "C0256": 25, "C0262": 10, "C0274": 20,
           "C0291": 15, "C0305": 10, "C0318": 20}
    rows = [{"cpty_code": c, "legal_name": n, "approved_from": f.isoformat(), "approved_to": _d(t),
             "credit_limit_musd": lim[c]} for c, n, f, t in K.CPTY]
    _csv(pd.DataFrame(rows), path)


def write_bookmap(path):
    rows = []
    for b in BOOKS:
        if b == "East":
            rows.append({"book": CODE[b], "load_zone": "LZ_NORTH", "effective_from": "2019-01-01", "effective_to": "2026-12-31"})
            rows.append({"book": CODE[b], "load_zone": "LZ_HOUSTON", "effective_from": "2027-01-01", "effective_to": ""})
        else:
            rows.append({"book": CODE[b], "load_zone": K.MAP_2027[b], "effective_from": "2019-01-01", "effective_to": ""})
    _csv(pd.DataFrame(rows), path)


def write_blotter(w, path):
    b = w.blotter.sort_values(["booked", "trade_id", "amend"], kind="mergesort")
    out = pd.DataFrame({"trade_id": b["trade_id"], "amendment_no": b["amend"].astype(int), "portfolio": b["portfolio"],
                        "cpty_code": b["cpty"], "product_code": b["product"],
                        "delivery_start": [d.isoformat() for d in b["start"]],
                        "delivery_end": [d.isoformat() for d in b["end"]], "mw": b["mw"].astype(int),
                        "fixed_price": b["price"].map(lambda x: f"{x:.2f}"),
                        "trade_date": [d.isoformat() for d in b["trade_date"]],
                        "booked_on": [d.isoformat() for d in b["booked"]]})
    _csv(out, path)
    return out


def write_matchlog(w, path):
    m = w.matching.sort_values(["status_date", "trade_id", "amend"], kind="mergesort")
    out = pd.DataFrame({"trade_id": m["trade_id"], "amendment_no": m["amend"].astype(int), "status": m["status"],
                        "status_date": [d.isoformat() for d in m["status_date"]]})
    _csv(out, path)
    return out


def write_portfolios(path):
    opened = {"HOU-CI": "2014-01-02", "HOU-LCI": "2018-07-01", "ETX-CI": "2015-03-02", "FWT-CI": "2016-05-02",
              "NTX-CI": "2016-05-02", "DFW-CI": "2014-01-02", "DFW-LCI": "2018-07-01", "CTX-CI": "2014-06-02",
              "CTX-LCI": "2021-01-04", "STX-CI": "2015-03-02", "WTX-CI": "2016-05-02"}
    rows = [{"portfolio": p, "book": CODE[b], "desk": "ERCOT Retail Hedge", "opened_on": opened[p]}
            for b, ps in K.PORTFOLIOS.items() for p in ps]
    _csv(pd.DataFrame(rows), path)


def write_calendar(path):
    names = {}
    for d in nerc_holidays(2027):
        names[d] = {1: "New Year's Day", 5: "Memorial Day", 7: "Independence Day (observed)", 9: "Labor Day",
                    11: "Thanksgiving Day", 12: "Christmas Day"}[d.month]
    rows = [{"date": d.isoformat(), "weekday": d.strftime("%a"), "nerc_holiday": "Y" if d in names else "N",
             "holiday_name": names.get(d, "")} for d in daterange(date(2027, 1, 1), date(2027, 12, 31))]
    _csv(pd.DataFrame(rows), path)


def write_temps(w, path, rng):
    rows = []
    base = {"Coast": 93, "East": 94, "Far West": 98, "North": 99, "North Central": 97, "South Central": 97,
            "Southern": 96, "West": 97}
    for y in SUMMERS:
        days = w.heat[y]["days"]
        for b in BOOKS:
            hb = w.heat[y]["book"][b]
            for d, h in zip(days, hb):
                tmax = base[b] + 14 * (h - 0.62) + rng.normal(0, 1.1)
                tmin = tmax - 20 - rng.normal(0, 2.0)
                rows.append({"date": d.isoformat(), "weather_zone": CODE[b], "tmax_f": f"{tmax:.0f}",
                             "tmin_f": f"{tmin:.0f}", "cdd": f"{max(0.0, (tmax + tmin) / 2 - 65):.1f}"})
    _csv(pd.DataFrame(rows), path)
