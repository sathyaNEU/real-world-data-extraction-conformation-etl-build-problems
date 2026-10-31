"""The pack's data files, each written as the system that keeps it writes it."""
import csv
import datetime as dt
import io
import math
import os
import re
import zipfile

import numpy as np
import openpyxl
import pyarrow as pa
import pyarrow.parquet as pq

import world as W

FILES = {
    "master": "wealdmoor_security_master_2026-11-30.csv",
    "market": "lse_daily_market_data_2025-2026.parquet",
    "backtests": "research_backtests_2027_candidates.xlsx",
    "trades": "backtest_rebalance_trades_2025-2026.csv",
    "orders": "oms_orders_2025-2026.csv",
    "fills": "oms_fills_2025-2026.csv",
    "accounts": "trading_account_register.csv",
    "policy": "ic_capital_allocation_policy_2026.pdf",
    "tca": "tca_standard_rev4.pdf",
    "request": "cio_request_2026-12-01.eml",
    "commissions": "broker_commission_schedule_2026.xlsx",
    "esg": "esg_exclusions_2026.csv",
    "allocations": "oms_block_allocations_2025-2026.csv",
}
DISTRACTORS = ["commissions", "esg"]
EXPORT = dt.datetime(2026, 12, 1, 7, 15, 0)
BAND = {"L": "FTSE 100", "M": "FTSE 250", "S": "FTSE SmallCap"}
ACCOUNT = {"INC": "WM-INC-01", "MCG": "WM-MCG-01", "SMC": "WM-SMC-01"}


def _csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def _utc(d, hh, mm, ss=0):
    """London wall time to UTC: British Summer Time from the last Sunday of March to the last Sunday of October."""
    def last_sunday(y, m):
        x = dt.date(y, m, 31)
        return x - dt.timedelta(days=(x.weekday() + 1) % 7)
    bst = last_sunday(d.year, 3) <= d < last_sunday(d.year, 10)
    t = dt.datetime(d.year, d.month, d.day, hh, mm, ss) - dt.timedelta(hours=1 if bst else 0)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def account_of(o):
    if o["account"] == "BLOCK":
        return "WM-BLOCK-01"
    if o["account"] == "DYN":
        return "WM-DYN-02" if o["date"] >= W.DYN_CODE_CHANGE else "WM-DYN-01"
    if o["account"] == "TRN":
        return "WM-DYN-01"
    return ACCOUNT[o["account"]]


def fills_for(o, r, failover=None):
    """The order's fills: its filled quantity split across brokers' executions whose average sits at the price the
    order paid. A failover splits the order: the first part fills before it under the original order, the rest under
    the order the backup re-created."""
    vwap = o["arrival"] * (1 + o["side"] * o["cost"] / 1e4)
    n = 1 + int(r.poisson(1.6 if o["part"] < 0.02 else 4.0))
    qty = o["filled"]
    cuts = sorted(set(int(x) for x in r.integers(1, max(2, qty), size=n - 1))) if qty > n else []
    parts = [b - a for a, b in zip([0] + cuts, cuts + [qty]) if b - a > 0]
    disp = [float(r.normal(0, 0.0012)) for _ in parts]
    mean_d = sum(p * d for p, d in zip(parts, disp)) / sum(parts)
    prices = [vwap * (1 + d - mean_d) for d in disp]
    t0 = o["hh"] * 60 + o["mm"]
    span = 30 + int(min(o["part"], 0.6) * 420)
    out = []
    for k, (q, px) in enumerate(zip(parts, prices)):
        t = min(t0 + 2 + int(span * (k + 1) / (len(parts) + 1)), 16 * 60 + 29)
        out.append(dict(qty=q, px=px, minute=t, broker=W.BROKERS[int(r.integers(0, len(W.BROKERS)))]))
    return out


def write_allocations(orders, path):
    """The post-trade allocation of each block order to the portfolios it was placed for."""
    rows = []
    for o in orders:
        if o["account"] != "BLOCK":
            continue
        for acct, q in o["alloc"]:
            rows.append([o["order_id"], account_of(dict(o, account=acct)), q, o["date"].isoformat()])
    rows.sort()
    _csv(path, ["block_order_id", "account_code", "allocated_qty", "allocation_date"], rows)


def write_orders_fills(orders, path_o, path_f):
    r = W.rng("fills")
    orows, frows = [], []
    eid = 7_300_000
    recovery = []
    for o in orders:
        fl = fills_for(o, r)
        fo = o["date"] in W.FAILOVER_DAYS and o["account"] not in ("TRN", "BLOCK") and o["part"] < 0.03 \
            and len(fl) >= 2 \
            and 9 <= o["hh"] <= 13
        status = "CANCELLED" if o["cancelled"] else "FILLED"
        if fo:
            # the failover at 13:58 London time: fills after it move to the order the backup re-created
            cut = max(1, len(fl) // 2)
            before, after = fl[:cut], fl[cut:]
            f1 = sum(f["qty"] for f in before)
            status = "TERMINATED"
            remaining = o["qty"] - f1
            moved = sum(f["qty"] * f["px"] for f in before) / f1
            rec_id = "WM%d" % (int(o["order_id"][2:]) + 900_000)
            recovery.append(dict(order_id=rec_id, acct=account_of(o), sedol=o["sedol"], side=o["side"],
                                 qty=remaining, created=_utc(o["date"], 14, 2 + int(r.integers(0, 6))),
                                 mid=moved, status="CANCELLED" if o["cancelled"] else "FILLED"))
            for f in before:
                eid += int(r.integers(1, 9))
                frows.append(_fill_row(eid, o["order_id"], f, o["date"]))
            for f in after:
                eid += int(r.integers(1, 9))
                f = dict(f, minute=max(f["minute"], 14 * 60 + 5))
                frows.append(_fill_row(eid, rec_id, f, o["date"]))
        else:
            for f in fl:
                eid += int(r.integers(1, 9))
                frows.append(_fill_row(eid, o["order_id"], f, o["date"]))
        orows.append([o["order_id"], account_of(o), o["sedol"], "BUY" if o["side"] > 0 else "SELL", o["qty"],
                      _utc(o["date"], o["hh"], o["mm"]), "%.2f" % o["arrival"], status, "DESK"])
    for rc in recovery:
        orows.append([rc["order_id"], rc["acct"], rc["sedol"], "BUY" if rc["side"] > 0 else "SELL", rc["qty"],
                      rc["created"], "%.2f" % rc["mid"], rc["status"], "BACKUP-RECOVERY"])
    orows.sort(key=lambda x: (x[5], x[0]))
    # the re-sent batch: after the outage of 9 June 2026 the OMS sent that day's fills again, unchanged
    day = W.RESENT_DAY.isoformat()
    again = [list(x) for x in frows if x[6].startswith(day)]
    frows = frows + again
    frows.sort(key=lambda x: (x[6], x[0]))
    _csv(path_o, ["order_id", "account_code", "sedol", "side", "order_qty", "created_utc", "arrival_mid_gbx",
                  "status", "source"], orows)
    _csv(path_f, ["exec_id", "order_id", "broker", "fill_qty", "fill_price", "price_unit", "exec_utc"], frows)
    return len(frows)


def _fill_row(eid, order_id, f, d):
    gbp = f["broker"] == W.GBP_BROKER
    px = "%.4f" % (f["px"] / 100.0) if gbp else "%.2f" % f["px"]
    return ["X%d" % eid, order_id, f["broker"], f["qty"], px, "GBP" if gbp else "GBX",
            _utc(d, f["minute"] // 60, f["minute"] % 60, 0)]


def write_market(mkt, univ, path):
    sed, dates, close, vol = [], [], [], []
    for s in sorted(univ, key=lambda x: x["sedol"]):
        for d, px, shares, _v in mkt[s["sedol"]]:
            sed.append(s["sedol"])
            dates.append(d)
            close.append(round(px, 2))
            vol.append(shares)
    t = pa.table({"sedol": pa.array(sed, pa.string()), "trade_date": pa.array(dates, pa.date32()),
                  "close_gbx": pa.array(close, pa.float64()), "volume_shares": pa.array(vol, pa.int64())})
    pq.write_table(t, path, compression="snappy", use_dictionary=True, write_statistics=False,
                   coerce_timestamps=None)
    return len(sed)


def write_master(univ, cons, path):
    rows = []
    for s in sorted(univ, key=lambda x: x["sedol"]):
        note = ""
        if s["sedol"] in cons:
            note = "Share consolidation 10 for 1 effective %s" % cons[s["sedol"]].strftime("%d/%m/%Y")
        rows.append([s["sedol"], s["isin"], s["name"], BAND[s["tier"]], s["sector"], "LSE Main Market", note])
    _csv(path, ["sedol", "isin", "security_name", "index_band", "icb_industry", "listing", "corporate_action_note"],
         rows)


def write_trades(cands, path):
    rows = []
    for code in sorted(cands):
        for t in cands[code]:
            rows.append([code, t["date"].isoformat(), t["isin"], "%.6f" % t["weight"]])
    rows.sort(key=lambda x: (x[0], x[1], x[2]))
    _csv(path, ["strategy_code", "rebalance_date", "isin", "traded_weight"], rows)


def write_accounts(path):
    rows = [["WM-INC-01", "UK Equity Income", "2016-02-01", ""],
            ["WM-MCG-01", "UK Mid Cap Growth", "2018-09-03", ""],
            ["WM-SMC-01", "UK Smaller Companies", "2020-01-06", ""],
            ["WM-DYN-01", "UK Dynamic", "2019-04-01", "2026-06-30"],
            ["WM-DYN-02", "UK Dynamic", "2026-07-01", ""],
            ["WM-DYN-01", "Pension transition (Severnvale)", "2026-08-17", "2026-11-13"],
            ["WM-BLOCK-01", "Desk block account (allocated post-trade)", "2017-05-02", ""]]
    _csv(path, ["account_code", "account_name", "opened", "closed"], rows)


def write_esg(univ, path):
    r = W.rng("esg")
    pick = sorted(univ, key=lambda s: s["sedol"])
    rows = []
    for k in r.permutation(len(pick))[:23]:
        s = pick[int(k)]
        rows.append([s["isin"], s["name"], ["Thermal coal", "Controversial weapons", "Tobacco production",
                                            "UN Global Compact breach"][int(r.integers(0, 4))], "2026-01-15"])
    rows.sort()
    _csv(path, ["isin", "issuer", "exclusion_reason", "effective"], rows)


def xlsx(path, sheets, creator, created, modified):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for title, rows, widths in sheets:
        ws = wb.create_sheet(title)
        for row in rows:
            ws.append(list(row))
        for col, wd in zip("ABCDEFGHIJ", widths):
            ws.column_dimensions[col].width = wd
        for c in ws[1]:
            c.font = openpyxl.styles.Font(bold=True)
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = created
    wb.properties.modified = modified
    buf = io.BytesIO()
    wb.save(buf)
    src = zipfile.ZipFile(io.BytesIO(buf.getvalue()))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename == "docProps/app.xml":
                data = (b'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
                        b'<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity>'
                        b'<ScaleCrop>false</ScaleCrop><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
                        b'<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>')
            if info.filename == "docProps/core.xml":
                data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                              b"\\g<1>" + modified.strftime("%Y-%m-%dT%H:%M:%SZ").encode() + b"\\g<2>", data)
                data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)",
                              b"\\g<1>" + created.strftime("%Y-%m-%dT%H:%M:%SZ").encode() + b"\\g<2>", data)
            zi = zipfile.ZipInfo(info.filename, date_time=modified.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)


def write_backtests(path):
    r = W.rng("backtests")
    years = list(range(2015, 2027))
    summ = [["Strategy code", "Strategy", "Benchmark", "Holdings", "Rebalance", "Annualised gross alpha, 2015 to 2026",
             "Tracking error", "Information ratio (gross)"]]
    annual = [["Year"] + [c[1] for c in W.CANDIDATES]]
    series = {}
    for code, name, tier, hold, freq, swap, alpha in W.CANDIDATES:
        te = {"S": 0.058, "M": 0.041, "L": 0.027}[tier]
        xs = [float(r.normal(alpha, te)) for _ in years]
        shift = alpha - (math.prod(1 + x for x in xs) ** (1 / len(xs)) - 1)
        xs = [x + shift for x in xs]
        series[code] = xs
        bm = {"S": "FTSE SmallCap (ex investment trusts)", "M": "FTSE 250 (ex investment trusts)",
              "L": "FTSE 100"}[tier]
        summ.append([code, name, bm, hold, "Monthly" if freq == "M" else "Quarterly", "%.2f%%" % (alpha * 100),
                     "%.1f%%" % (te * 100), "%.2f" % (alpha / te)])
    for i, y in enumerate(years):
        annual.append([y if y < 2026 else "2026 (to 30 Nov, annualised)"] +
                      ["%.1f%%" % (series[c[0]][i] * 100) for c in W.CANDIDATES])
    notes = [["Note"],
             ["Gross alpha is each strategy's return over its benchmark before any trading cost, from monthly "
              "simulated portfolios on the Research team's point-in-time data."],
             ["Every simulated portfolio applies the firm's ESG exclusion list in force at each date."],
             ["Prepared by Quantitative Research for the 2027 allocation round."]]
    xlsx(path, [("Summary", summ, (14, 34, 36, 10, 11, 22, 14, 18)), ("Annual alpha", annual, (26, 22, 22, 22)),
                ("Notes", notes, (120,))], "Wealdmoor Quantitative Research",
         dt.datetime(2026, 11, 9, 10, 41), dt.datetime(2026, 11, 26, 16, 5))
    return series


def write_commissions(path):
    rows = [["Broker", "Tier", "Monthly commission band (GBP)", "Rate (bps of value)", "Research component (bps)"]]
    for b, base in zip(W.BROKERS, (4.0, 5.0, 3.5, 4.5)):
        for k, band in enumerate(["0 to 250,000", "250,000 to 1,000,000", "over 1,000,000"]):
            rows.append([b, k + 1, band, "%.1f" % (base - 0.8 * k), "%.1f" % (1.5 - 0.3 * k)])
    xlsx(path, [("2026 schedule", rows, (28, 8, 30, 18, 24))], "Wealdmoor Dealing",
         dt.datetime(2026, 1, 6, 9, 12), dt.datetime(2026, 3, 30, 11, 47))
