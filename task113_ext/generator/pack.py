"""The simulation run end to end, and every data file written in its source's own layout.

Merriden's retired platform delivered one CSV of end-of-day history through 29 December 2023 (dates as yyyymmdd,
numeric exchange codes, shares in thousands, a price factor anchored at that file's last day). Its new platform
delivers Parquet from 2 October 2023, backfilling the old file's last quarter (shares in units, MIC codes, a factor
anchored at the delivery's last day, and the official closes and volumes the old file had before late corrections)."""
import csv
import datetime as dt
import io
import json
import math

import numpy as np

import bars as B
import ca as CA
import fiscal as F
import fund as FU
import history as H
import prices as PR
import side as SD
import universe as U
import world as W

EXCH_NUM = {"N": 1, "A": 2, "Q": 3}


def everything():
    secs = U.build()
    sched = F.schedule(secs)
    paths, factors = PR.simulate(secs, sched)
    bars = B.build(secs, paths, sched)
    hist = H.build(secs, paths)
    fund_rows, ids = FU.build(secs, sched, paths, bars, hist)
    x = dict(secs=secs, sched=sched, paths=paths, bars=bars, hist=hist, fund=fund_rows, ids=ids)
    x["ca"] = CA.build(secs, paths, bars, hist)
    x["delist"] = CA.delistings(secs, paths, bars, hist)
    x["earn"] = FU.calendar(secs, sched, hist, ids)
    x["recons"], x["changes"], x["levels"] = SD.index(secs, bars, hist)
    x["si"] = SD.short_interest(secs, bars, hist)
    x["sweep"] = SD.sweep()
    x["orders"], x["fills"] = SD.book(secs, paths, bars, hist, fund_rows, ids)
    x["listdates"] = _list_dates(secs)
    x["old_fix"] = _old_platform_differences(secs, bars)
    return x


def _list_dates(secs):
    rng = U.rng_for(16)
    out = {}
    for s in secs:
        if s["kind"] == "initial":
            y = int(rng.integers(1994, 2017))
            d = dt.date(y, int(rng.integers(1, 13)), int(rng.integers(1, 28)))
            while d.weekday() >= 5:
                d += dt.timedelta(days=1)
            if d >= W.START:
                d = dt.date(2016, 11, 15)
            out[s["k"]] = d
        else:
            out[s["k"]] = U.DAYS[s["first"]]
    return out


def _old_platform_differences(secs, bars):
    """In the overlap quarter the old file carries the closes and volumes as first published: a few closes later
    corrected by the consolidated tape, and volumes before late-reported trades were added."""
    rng = U.rng_for(17)
    a, b = U.DIDX[W.BACKFILL_FROM], U.DIDX[W.OLD_LAST]
    close_fix, vol_fix = {}, {}
    for s in secs:
        bb = bars[s["k"]]
        for i in range(max(a, bb["i0"] + 1), min(b, bb["i1"]) + 1):
            j = i - bb["i0"]
            if bb["ctype"][j] != "T":
                continue
            if rng.random() < 0.004:
                tick = 0.01 if bb["close"][j] >= 1 else 0.0001
                delta = float(rng.choice([-3, -2, -1, 1, 2, 3])) * tick
                old = round(float(bb["close"][j]) + delta, 4)
                if bb["low"][j] <= old <= bb["high"][j]:
                    close_fix[(s["k"], i)] = old
            if rng.random() < 0.08:
                vol_fix[(s["k"], i)] = int(bb["volume"][j] * rng.uniform(0.965, 0.996))
    return dict(close=close_fix, volume=vol_fix)


# -------------------------------------------------------------------------------------------- formatting helpers
def f4(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return ""
    return "%.4f" % v


def f6(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return ""
    return "%.6f" % v


def write_csv(path, header, rows, crlf=False, delimiter=","):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n", delimiter=delimiter)
    w.writerow(header)
    n = 0
    for r in rows:
        w.writerow(["" if v is None else v for v in r])
        n += 1
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    return n


def _anchor(bb, anchor_i):
    """Price factor per row: multiply a price by it to express it in shares as of the anchor day (the security's
    last row when it ends earlier)."""
    last = min(anchor_i, bb["i1"]) - bb["i0"]
    return bb["S"] / bb["S"][last]


# -------------------------------------------------------------------------------------------- end-of-day prices
OLD_COLS = ["DATE", "SID", "TICKER", "EXCH", "OPEN", "HIGH", "LOW", "CLOSE", "CLOSE_SRC", "VOLUME", "BID", "ASK",
            "SHROUT", "ADJ_FACTOR", "RET", "RETX"]


def old_rows(x):
    secs, bars, hist, fix = x["secs"], x["bars"], x["hist"], x["old_fix"]
    last_i = U.DIDX[W.OLD_LAST]
    per_day = {}
    for s in secs:
        bb = bars[s["k"]]
        if bb["i0"] > last_i:
            continue
        fac = _anchor(bb, last_i)
        hi = min(bb["i1"], last_i)
        closes = {}
        for i in range(bb["i0"], hi + 1):
            j = i - bb["i0"]
            closes[i] = fix["close"].get((s["k"], i), float(bb["close"][j]))
        for i in range(bb["i0"], hi + 1):
            j = i - bb["i0"]
            sp = H.on(hist, s["k"], i)
            c = closes[i]
            if j == 0:
                ret = retx = ""
            else:
                pc = closes[i - 1]
                ret = f6((c * bb["F"][j] + bb["D"][j] + bb["V"][j]) / pc - 1)
                retx = f6(c * bb["F"][j] / pc - 1)
            vol = fix["volume"].get((s["k"], i), int(bb["volume"][j]))
            per_day.setdefault(i, []).append([
                U.DAYS[i].strftime("%Y%m%d"), s["sid"], sp["ticker"], EXCH_NUM[sp["exch"]], f4(bb["open"][j]),
                f4(bb["high"][j]), f4(bb["low"][j]), f4(c), bb["ctype"][j], vol, f4(bb["bid"][j]), f4(bb["ask"][j]),
                int(round(bb["shares"][j] / 1000)), "%.6f" % fac[j], ret, retx])
    for i in sorted(per_day):
        for r in sorted(per_day[i], key=lambda r: r[1]):
            yield r


def new_table(x):
    import pyarrow as pa
    secs, bars, hist = x["secs"], x["bars"], x["hist"]
    a = U.DIDX[W.BACKFILL_FROM]
    end_i = U.T - 1
    cols = {k: [] for k in ("trade_date", "security_id", "symbol", "mic", "open_px", "high_px", "low_px", "close_px",
                            "close_type", "volume", "closing_bid", "closing_ask", "shares_outstanding",
                            "px_adj_factor", "total_return", "price_return")}
    recs = []
    for s in secs:
        bb = bars[s["k"]]
        if bb["i1"] < a:
            continue
        fac = _anchor(bb, end_i)
        for i in range(max(a, bb["i0"]), bb["i1"] + 1):
            j = i - bb["i0"]
            sp = H.on(hist, s["k"], i)
            recs.append((i, s["sid"], sp, bb, j, fac[j]))
    recs.sort(key=lambda r: (r[0], r[1]))
    nan = float("nan")
    for i, sid, sp, bb, j, fc in recs:
        cols["trade_date"].append(U.DAYS[i])
        cols["security_id"].append(sid)
        cols["symbol"].append(sp["ticker"])
        cols["mic"].append(W.MIC[sp["exch"]])
        for c, key in (("open_px", "open"), ("high_px", "high"), ("low_px", "low")):
            v = float(bb[key][j])
            cols[c].append(None if math.isnan(v) else v)
        cols["close_px"].append(float(bb["close"][j]))
        cols["close_type"].append("TRADE" if bb["ctype"][j] == "T" else "MID")
        cols["volume"].append(int(bb["volume"][j]))
        cols["closing_bid"].append(float(bb["bid"][j]))
        cols["closing_ask"].append(float(bb["ask"][j]))
        cols["shares_outstanding"].append(int(bb["shares"][j]))
        cols["px_adj_factor"].append(round(float(fc), 8))
        r = float(bb["ret"][j])
        rx = float(bb["retx"][j])
        cols["total_return"].append(None if math.isnan(r) else round(r, 8))
        cols["price_return"].append(None if math.isnan(rx) else round(rx, 8))
    schema = pa.schema([("trade_date", pa.date32()), ("security_id", pa.int64()), ("symbol", pa.string()),
                        ("mic", pa.string()), ("open_px", pa.float64()), ("high_px", pa.float64()),
                        ("low_px", pa.float64()), ("close_px", pa.float64()), ("close_type", pa.string()),
                        ("volume", pa.int64()), ("closing_bid", pa.float64()), ("closing_ask", pa.float64()),
                        ("shares_outstanding", pa.int64()), ("px_adj_factor", pa.float64()),
                        ("total_return", pa.float64()), ("price_return", pa.float64())])
    return pa.table(cols, schema=schema)


def write_parquet(path, table):
    import pyarrow.parquet as pq
    pq.write_table(table, path, compression="zstd", use_dictionary=["symbol", "mic", "close_type"],
                   write_statistics=True, row_group_size=50000)
    return table.num_rows


# -------------------------------------------------------------------------------------------- security master
SM_COLS = ["security_id", "effective_from", "effective_to", "ticker", "issuer_name", "exchange", "cusip",
           "sector_code", "sector", "industry", "share_type", "list_date", "delist_date", "delist_code"]


def secmaster_rows(x):
    secs, hist = x["secs"], x["hist"]
    codes = {r["security_id"]: r["code"] for r in x["delist"]}
    out = []
    for s in secs:
        spells = hist[s["k"]]
        delist = U.DAYS[s["last"]] if s["last"] is not None else None
        for n, (d0, d1, sp) in enumerate(spells):
            frm = x["listdates"][s["k"]] if n == 0 else U.DAYS[d0]
            to = U.DAYS[d1] if (n + 1 < len(spells) or s["last"] is not None) else None
            sec = W.SECTORS[sp["sector"]]
            desc = sp.get("desc_class") or sp["desc"]
            ind = W.INDUSTRY.get(desc) or W.INDUSTRY[sec[2][0]]
            out.append([s["sid"], frm.isoformat(), to.isoformat() if to else "", sp["ticker"], sp["name"],
                        sp["exch"], sp["cusip"], sec[0], sec[1], ind, "Common Stock",
                        x["listdates"][s["k"]].isoformat(), delist.isoformat() if delist else "",
                        codes.get(s["sid"], "")])
    out.sort(key=lambda r: (r[0], r[1]))
    return out


# -------------------------------------------------------------------------------------------- the CA feed
def write_ca(path, rows):
    clean = []
    for r in rows:
        r = dict(r)
        r["terms"] = {k: (float(v) if isinstance(v, (np.floating,)) else int(v) if isinstance(v, np.integer) else v)
                      for k, v in r["terms"].items()}
        clean.append(r)
    head = dict(feed="Merriden Corporate Actions", feed_version="3.2", extract_utc="2026-10-06T06:12:44Z",
                coverage="US listed common stock: Pellbrook research universe (security list PBK-RU-01)",
                record_count=len(clean))
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("{\n")
        for k, v in head.items():
            f.write("  %s: %s,\n" % (json.dumps(k), json.dumps(v)))
        f.write('  "records": [\n')
        for n, r in enumerate(clean):
            f.write("    " + json.dumps(r, separators=(",", ":")) + ("," if n + 1 < len(clean) else "") + "\n")
        f.write("  ]\n}\n")
    return len(clean)


# -------------------------------------------------------------------------------------------- fundamentals, calendar
FUND_COLS = ["lp_id", "ticker", "cusip", "company_name", "fiscal_year", "fiscal_quarter", "period_type", "period_end",
             "source", "knowledge_date", "currency", "units", "revenue", "operating_income", "net_income",
             "eps_diluted", "shares_diluted", "total_assets", "total_liabilities", "total_equity",
             "cash_and_equivalents", "total_debt", "operating_cash_flow_ytd", "capex_ytd"]


def fund_rows(x):
    for r in x["fund"]:
        row = []
        for c in FUND_COLS:
            v = r.get(c)
            if c == "eps_diluted" and v is not None:
                v = "%.2f" % float(v)
            elif isinstance(v, float) and r["units"] == "millions" and c not in ("eps_diluted",):
                v = "%.1f" % v
            row.append(v)
        yield row


def write_jsonl(path, rows):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, separators=(",", ":")) + "\n")
    return len(rows)


# -------------------------------------------------------------------------------------------- index levels
LEVEL_COLS = ["date", "index_code", "price_return_level", "total_return_level", "constituents",
              "index_market_cap_usd_mn"]


def level_rows(x):
    for r in x["levels"]:
        yield [r["date"].isoformat(), W.INDEX_CODE, "%.2f" % r["pr"], "%.2f" % r["tr"], r["n"], "%.1f" % r["mcap"]]


# -------------------------------------------------------------------------------------------- short interest
SI_COLS = ["SettlementDate", "Symbol", "IssueName", "Market", "CurrentShortQuantity", "PreviousShortQuantity",
           "ChangePercent", "AverageDailyVolume", "DaysToCover", "RevisionFlag", "PublicationDate"]


def si_rows(x):
    for r in x["si"]:
        prev = r["previous"]
        chg = "" if not prev else "%.2f" % (100.0 * (r["short"] - prev) / prev)
        dtc = "999.99" if r["adv"] == 0 else "%.2f" % min(999.99, r["short"] / r["adv"])
        yield [r["settlement"].strftime("%Y%m%d"), r["symbol"], r["issue"], r["market"], r["short"],
               "" if prev is None else prev, chg, r["adv"], dtc, r["revised"], r["published"].strftime("%Y%m%d")]


# -------------------------------------------------------------------------------------------- sweep rate
SWEEP_COLS = ["value_date", "reference_rate", "reference_rate_pct", "spread_bp", "sweep_rate_pct", "day_count"]


def sweep_rows(x):
    for r in x["sweep"]:
        yield [r["date"].isoformat(), r["reference"], "%.4f" % r["reference_rate"], int(round(r["spread"] * 100)),
               "%.4f" % r["sweep_rate"], r["accrual_basis"]]


# -------------------------------------------------------------------------------------------- the live book
ORDER_COLS = ["order_id", "created_utc", "rebalance_date", "account", "symbol", "cusip", "side", "order_qty",
              "order_type", "algo", "tif", "status", "filled_qty", "avg_price", "arrival_price"]


def order_rows(x):
    for o in x["orders"]:
        yield [o["order_id"], o["created_utc"], o["rebalance_date"].isoformat(), o["account"], o["symbol"],
               o["cusip"], o["side"], o["order_qty"], o["order_type"], o["algo"], o["tif"], o["status"],
               o["filled_qty"], "" if o["avg_price"] is None else "%.4f" % o["avg_price"], "%.4f" % o["arrival_price"]]


FILL_COLS = ["exec_id", "exec_type", "ref_exec_id", "client_order_id", "broker_order_id", "symbol", "side",
             "exec_time_et", "qty", "price", "venue", "liquidity", "commission_usd", "clearing_fee_usd", "trade_date",
             "settle_date"]


def fill_rows(x):
    for f_ in x["fills"]:
        yield [f_["exec_id"], f_["exec_type"], f_["ref_exec_id"], f_["client_order_id"], f_["broker_order_id"],
               f_["symbol"], f_["side"], f_["exec_time"], f_["qty"], "%.4f" % f_["price"], f_["venue"],
               f_["liquidity"], "%.2f" % f_["commission"], "%.2f" % f_["clearing_fee"],
               f_["trade_date"].strftime("%Y%m%d"), f_["settle_date"].strftime("%Y%m%d")]
