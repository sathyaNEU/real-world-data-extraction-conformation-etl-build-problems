"""Independent checks on the written bundle: everything here reads the files under target/ and nothing the
simulation holds, and proves the files agree with each other the way the sources' own systems would.

    python3 task113_ext/generator/checks.py [target]
"""
import datetime as dt
import json
import math
import os
import re
import subprocess
import sys
from collections import defaultdict
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calendar_us as C   # noqa: E402  (the exchange calendar, as public knowledge)
import world as W         # noqa: E402  (file names only)

NY = ZoneInfo("America/New_York")
RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append(bool(cond))
    print("%s  %s%s" % ("PASS" if cond else "FAIL", name, "" if cond or not detail else "  [%s]" % detail))


def run(target):
    del RESULTS[:]
    p = lambda k: os.path.join(target, W.FILES[k])
    _gates(target)
    _dashes(target)
    old = pd.read_csv(p("px_old"), dtype={"TICKER": str, "CLOSE_SRC": str})
    new = pd.read_parquet(p("px_new"))
    sm = pd.read_csv(p("secmaster"), dtype=str, keep_default_na=False)
    ca = json.load(open(p("ca"), encoding="utf-8"))["records"]
    events = _events(ca)
    _bars(old, new)
    px = _merged(old, new)
    _returns(old, new, events, px)
    _factors(old, new, events)
    _overlap(old, new)
    _master(sm, old, new)
    _delistings(p("delist"), px, sm)
    fund = pd.read_csv(p("fund"), dtype={"lp_id": str, "ticker": str, "cusip": str})
    _fundamentals(fund)
    _calendar(p("earn"), fund)
    _index(p("recon"), p("levels"), px, sm, events)
    _short_interest(p("si"), sm)
    _sweep(p("sweep"))
    _book(p("orders"), p("fills"), px, sm)
    good = all(RESULTS)
    print("checks: %d of %d pass" % (sum(RESULTS), len(RESULTS)))
    return good


# ---------------------------------------------------------------------------------------------- gates and text
def _rows(path):
    if path.endswith(".parquet"):
        import pyarrow.parquet as pq
        return pq.ParquetFile(path).metadata.num_rows
    if path.endswith((".csv", ".txt")):
        return sum(1 for _ in open(path, encoding="utf-8")) - 1
    if path.endswith(".jsonl"):
        return sum(1 for _ in open(path, encoding="utf-8"))
    return 0


def _gates(target):
    files = sorted(os.listdir(target))
    fmts = sorted(set(f.rsplit(".", 1)[-1] for f in files))
    big = max(files, key=lambda f: _rows(os.path.join(target, f)))
    check("gates: %d files (10 or more)" % len(files), len(files) >= 10)
    check("gates: %d formats %s (3 or more)" % (len(fmts), fmts), len(fmts) >= 3)
    check("gates: largest file %s with %d rows (25,000 or more)" % (big, _rows(os.path.join(target, big))),
          _rows(os.path.join(target, big)) >= 25000)


def _dashes(target):
    bad = []
    for f in sorted(os.listdir(target)):
        path = os.path.join(target, f)
        if f.endswith(".pdf"):
            txt = subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True).stdout
        elif f.endswith(".xlsx"):
            from openpyxl import load_workbook
            wb = load_workbook(path, read_only=True)
            txt = " ".join(str(c) for ws in wb.worksheets for row in ws.iter_rows(values_only=True) for c in row
                           if c is not None)
        elif f.endswith(".parquet"):
            continue
        else:
            txt = open(path, encoding="utf-8").read()
        if re.search("[\u2013\u2014]", txt):
            bad.append(f)
    check("text: no en or em dash in any file", not bad, bad)


# ---------------------------------------------------------------------------------------------- the CA feed
def _events(ca):
    """The standing revision of every event: the latest by revision, dropped when cancelled."""
    last = {}
    for r in ca:
        if r["ca_id"] not in last or r["revision"] > last[r["ca_id"]]["revision"]:
            last[r["ca_id"]] = r
    ev = defaultdict(list)
    for r in last.values():
        if r["status"] == "CANCEL":
            continue
        ev[r["security_id"]].append(r)
    check("ca: revisions of an event are numbered 1, 2, ... in publication order",
          all(_revs_ok([x for x in ca if x["ca_id"] == cid]) for cid in list(last)[:400]))
    return ev


def _revs_ok(rs):
    rs = sorted(rs, key=lambda r: r["published_utc"])
    return [r["revision"] for r in rs] == list(range(1, len(rs) + 1))


def _split_factor(ev, sid, d):
    f = 1.0
    for r in ev.get(sid, []):
        if r["event_type"] in ("SPLIT", "REVERSE_SPLIT") and r["ex_date"] == d:
            f *= r["terms"]["new_shares"] / r["terms"]["old_shares"]
    return f


def _cash(ev, sid, d):
    return sum(r["terms"]["gross_amount"] for r in ev.get(sid, [])
               if r["event_type"] in ("DIV_CASH", "DIV_SPECIAL") and r["ex_date"] == d)


# ---------------------------------------------------------------------------------------------- prices
def _bars(old, new):
    for name, df, o, h, l_, c, src, vol, bid, ask in (
            ("legacy", old, "OPEN", "HIGH", "LOW", "CLOSE", "CLOSE_SRC", "VOLUME", "BID", "ASK"),
            ("current", new, "open_px", "high_px", "low_px", "close_px", "close_type", "volume", "closing_bid",
             "closing_ask")):
        traded = df[o].notna()
        okh = (df.loc[traded, h] + 1e-9 >= df.loc[traded, [o, c]].max(axis=1)).all()
        okl = (df.loc[traded, l_] - 1e-9 <= df.loc[traded, [o, c]].min(axis=1)).all()
        check("prices (%s): high and low bound the open and close on every traded row" % name, okh and okl)
        quiet = df[~traded]
        check("prices (%s): every untraded row has no volume and a quote-midpoint close (%d rows)" % (
            name, len(quiet)), (quiet[vol] == 0).all() and quiet[src].isin(["M", "MID"]).all() and
            (abs(quiet[c] - (quiet[bid] + quiet[ask]) / 2) < 0.0051).all())
        check("prices (%s): closing bid below ask, close positive" % name, (df[bid] < df[ask]).all() and
              (df[c] > 0).all())
    check("prices: one row per security and day in each file",
          not old.duplicated(["DATE", "SID"]).any() and not new.duplicated(["trade_date", "security_id"]).any())


def _merged(old, new):
    """Closes and the rest by security and day: the legacy file before the overlap, the current file from it."""
    a = old[old["DATE"] < 20231002].copy()
    a["date"] = pd.to_datetime(a["DATE"].astype(str)).dt.date
    a = a.rename(columns={"SID": "sid", "CLOSE": "close", "LOW": "low", "HIGH": "high", "RET": "ret",
                          "TICKER": "ticker"})[["sid", "date", "close", "low", "high", "ret", "ticker"]]
    b = new.rename(columns={"security_id": "sid", "trade_date": "date", "close_px": "close", "low_px": "low",
                            "high_px": "high", "total_return": "ret", "symbol": "ticker"})[
        ["sid", "date", "close", "low", "high", "ret", "ticker"]]
    m = pd.concat([a, b], ignore_index=True).sort_values(["sid", "date"]).reset_index(drop=True)
    return m


def _returns(old, new, ev, px):
    first_close = px.groupby("sid").first()["close"].to_dict()
    child_close = {}
    for sid, rs in ev.items():
        for r in rs:
            if r["event_type"] == "SPINOFF":
                child_close[(sid, r["ex_date"])] = r["terms"]["ratio"] * first_close[r["terms"]["distributed_security_id"]]
    for name, df, dcol, sidc, cc, rc, rxc, tol in (
            ("legacy", old, "DATE", "SID", "CLOSE", "RET", "RETX", 6e-7),
            ("current", new, "trade_date", "security_id", "close_px", "total_return", "price_return", 6e-8)):
        df = df.sort_values([sidc, dcol])
        dates = df[dcol].astype(str).str.replace(r"^(\d{4})(\d{2})(\d{2})$", r"\1-\2-\3", regex=True)
        prev = df.groupby(sidc)[cc].shift(1)
        bad = 0
        n = 0
        for sid, d, c, pc, r, rx in zip(df[sidc], dates, df[cc], prev, df[rc], df[rxc]):
            if pd.isna(pc):
                continue
            f = _split_factor(ev, sid, d)
            want = (c * f + _cash(ev, sid, d) + child_close.get((sid, d), 0.0)) / pc - 1
            want_x = c * f / pc - 1
            n += 1
            if abs(want - r) > tol + 1e-12 or abs(want_x - rx) > tol + 1e-12:
                bad += 1
        check("returns (%s): every total and price return recomputes from the closes and the corporate actions "
              "feed (%d rows)" % (name, n), bad == 0, "%d differ" % bad)


def _factors(old, new, ev):
    for name, df, dcol, sidc, fc in (("legacy", old, "DATE", "SID", "ADJ_FACTOR"),
                                     ("current", new, "trade_date", "security_id", "px_adj_factor")):
        df = df.sort_values([sidc, dcol])
        dates = df[dcol].astype(str).str.replace(r"^(\d{4})(\d{2})(\d{2})$", r"\1-\2-\3", regex=True)
        prev = df.groupby(sidc)[fc].shift(1)
        bad = sum(1 for sid, d, f, pf in zip(df[sidc], dates, df[fc], prev)
                  if not pd.isna(pf) and abs(f / pf - _split_factor(ev, sid, d)) > 2e-5 * max(1, f / pf))
        last_ok = (df.groupby(sidc)[fc].last().round(6) == 1.0).all()
        check("factors (%s): the price factor steps by each split's ratio on its ex-date and is 1 on each "
              "security's last row" % name, bad == 0 and last_ok, "%d steps differ" % bad)


def _overlap(old, new):
    a = old[old["DATE"] >= 20231002].copy()
    a["date"] = pd.to_datetime(a["DATE"].astype(str)).dt.date
    b = new[new["trade_date"] <= dt.date(2023, 12, 29)]
    m = a.merge(b, left_on=["SID", "date"], right_on=["security_id", "trade_date"], how="outer", indicator=True)
    check("overlap: the two deliveries hold the same securities and days in Q4 2023 (%d rows)" % len(m),
          (m["_merge"] == "both").all())
    diff = (m["CLOSE"] - m["close_px"]).abs()
    check("overlap: closes agree but for late corrections of a few ticks (%d rows differ)" % int((diff > 1e-9).sum()),
          (diff <= 0.0301).all())
    check("overlap: legacy volume never above the current platform's, shares in thousands against units",
          (m["VOLUME"] <= m["volume"]).all() and (abs(m["SHROUT"] * 1000 - m["shares_outstanding"]) <= 500).all())


# ---------------------------------------------------------------------------------------------- security master
def _master(sm, old, new):
    sm = sm.copy()
    sm["security_id"] = sm["security_id"].astype(int)
    contiguous = True
    for sid, g in sm.groupby("security_id"):
        g = g.sort_values("effective_from")
        for a, b in zip(g.itertuples(), list(g.itertuples())[1:]):
            if (dt.date.fromisoformat(a.effective_to) + dt.timedelta(days=1)) > dt.date.fromisoformat(b.effective_from):
                contiguous = False
    check("master: each security's spells follow one another without overlap", contiguous)
    spells = defaultdict(list)
    for r in sm.itertuples():
        spells[r.security_id].append((r.effective_from, r.effective_to or "9999", r.ticker, r.exchange))
    ex_old = {"N": 1, "A": 2, "Q": 3}
    ex_new = {"N": "XNYS", "A": "XASE", "Q": "XNAS"}
    bad = 0
    seen = defaultdict(set)
    for sid, d, tk, ex in zip(old["SID"], old["DATE"].astype(str), old["TICKER"], old["EXCH"]):
        ds = "%s-%s-%s" % (d[:4], d[4:6], d[6:])
        sp = [s for s in spells[sid] if s[0] <= ds <= s[1]]
        if len(sp) != 1 or sp[0][2] != tk or ex_old[sp[0][3]] != ex:
            bad += 1
        seen[ds].add(tk)
    for sid, d, tk, ex in zip(new["security_id"], new["trade_date"].astype(str), new["symbol"], new["mic"]):
        sp = [s for s in spells[sid] if s[0] <= d <= s[1]]
        if len(sp) != 1 or sp[0][2] != tk or ex_new[sp[0][3]] != ex:
            bad += 1
    check("master: every price row's ticker and exchange is the master's spell in force that day", bad == 0,
          "%d rows" % bad)
    dup = old.groupby("DATE")["TICKER"].apply(lambda s: s.duplicated().any()).any() or \
        new.groupby("trade_date")["symbol"].apply(lambda s: s.duplicated().any()).any()
    check("master: no ticker names two securities on the same day", not dup)
    reused = sm.groupby("ticker")["security_id"].nunique()
    check("master: tickers reused by a later company after a delisting (%d)" % int((reused > 1).sum()),
          (reused > 1).sum() >= 1)


# ---------------------------------------------------------------------------------------------- delistings
def _delistings(path, px, sm):
    d = pd.read_excel(path, sheet_name="Delistings")
    last = px.groupby("sid").agg(last_date=("date", "max"), n=("date", "size"))
    lastc = px.sort_values("date").groupby("sid")["close"].last()
    bad = []
    for r in d.itertuples():
        sid = int(r.security_id)
        ld = pd.Timestamp(r.last_trading_date).date()
        if last.loc[sid, "last_date"] != ld or abs(lastc[sid] - r.final_exchange_close) > 1e-9:
            bad.append(("last", sid))
            continue
        if r.code in ("M1", "P1"):
            want = r.cash_per_share / r.final_exchange_close - 1
        elif r.code == "M2":
            acq = px[px["sid"] == int(r.acquirer_security_id)]
            nxt = acq[acq["date"] > ld].iloc[0]
            want = r.shares_per_share * nxt["close"] / r.final_exchange_close - 1
        elif pd.isna(r.otc_first_price):
            want = None
        else:
            want = r.otc_first_price / r.final_exchange_close - 1
        got = None if pd.isna(r.delisting_return) else r.delisting_return
        if (want is None) != (got is None) or (want is not None and abs(want - got) > 6e-7):
            bad.append(("ret", sid))
    check("delistings: each last trading date and final close is the security's last price row, and each "
          "delisting return recomputes (%d delistings)" % len(d), not bad, bad[:5])
    gone = set(int(x) for x in d["security_id"])
    alive_last = px[~px["sid"].isin(gone)].groupby("sid")["date"].max()
    check("delistings: every security without one trades to the store's last day",
          (alive_last == W.END).all())


# ---------------------------------------------------------------------------------------------- fundamentals
def _fundamentals(f):
    check("fundamentals: no knowledge date after the pull (%s)" % W.FUND_PULLED,
          (f["knowledge_date"] <= W.FUND_PULLED.isoformat()).all())
    pr = f[f["source"] == "PRESS_RELEASE"].set_index(["lp_id", "period_end"])["knowledge_date"]
    filed = f[f["source"].isin(["10-Q", "10-K"])]
    late = sum(1 for r in filed.itertuples() if (r.lp_id, r.period_end) in pr.index and
               pr[(r.lp_id, r.period_end)] > r.knowledge_date)
    check("fundamentals: each period's press release comes no later than its filing", late == 0, late)
    check("fundamentals: 10-K rows carry the fiscal year (FY), every other row a quarter",
          (f.loc[f["source"].str.startswith("10-K"), "period_type"] == "FY").all() and
          (f.loc[~f["source"].str.startswith("10-K"), "period_type"] == "Q").all())
    unit = np.where(f["units"] == "millions", 1000.0, 1.0)
    implied = f["net_income"] * unit / f["shares_diluted"]
    ok = (abs(implied - f["eps_diluted"]) <= 0.011 + 0.03 * abs(f["eps_diluted"])) | f["eps_diluted"].isna()
    check("fundamentals: diluted EPS agrees with net income over diluted shares in the row's units (%d rows)" % len(f),
          ok.all(), int((~ok).sum()))
    q = f[(f["source"] == "10-Q")].sort_values(["lp_id", "fiscal_year", "fiscal_quarter"])
    grows = True
    for (lp, fy), g in q.groupby(["lp_id", "fiscal_year"]):
        if len(g) > 1 and (g["capex_ytd"].diff().dropna() > 0.5).any():
            grows = False
    check("fundamentals: capital expenditure year to date only accumulates within a fiscal year", grows)


def _calendar(path, f):
    rows = [json.loads(line) for line in open(path, encoding="utf-8")]
    latest = {}
    for r in rows:
        key = (r["lp_id"], r["period_end"])
        if key not in latest or r["updated_utc"] > latest[key]["updated_utc"]:
            latest[key] = r
    pr = f[f["source"] == "PRESS_RELEASE"]
    bad = 0
    for r in pr.itertuples():
        e = latest.get((r.lp_id, r.period_end))
        if e is None or e["status"] != "CONFIRMED":
            bad += 1
            continue
        t = dt.datetime.strptime(e["event_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=ZoneInfo("UTC"))
        if t.astimezone(NY).date().isoformat() != r.knowledge_date:
            bad += 1
    check("calendar: every press release's date is its period's latest confirmed event in New York time (%d)" %
          len(pr), bad == 0, bad)


# ---------------------------------------------------------------------------------------------- the benchmark
def _index(recon_path, levels_path, px, sm, ev):
    levels = pd.read_csv(levels_path)
    xl = pd.read_excel(recon_path, sheet_name=None)
    sheets = {k: v for k, v in xl.items() if k.startswith("Jun")}
    okw = all(abs(v["Weight (%)"].sum() - 100) < 0.02 and v["Weight (%)"].max() <= 4.0001 for v in sheets.values())
    check("index: each reconstitution's weights add to 100 and none exceeds 4 per cent (%d sheets)" % len(sheets), okw)
    days = sorted(px["date"].unique())
    check("index: a level for every trading day", list(pd.to_datetime(levels["date"]).dt.date) == days)
    cus = {}
    for r in sm.itertuples():
        cus.setdefault(r.cusip, []).append((r.effective_from, r.effective_to or "9999", int(r.security_id)))

    def sid_of(cusip, d):
        for a, b, sid in cus.get(cusip, []):
            if a <= d <= b:
                return sid
        return None

    recon_day = {}
    for y in range(2018, 2027):
        d = C.nth_weekday(y, 6, 4, 4)
        while d not in set(days):
            d -= dt.timedelta(days=1)
        recon_day[d] = "Jun%d" % y
    changes = xl["Interim Changes"]
    chg = defaultdict(list)
    for r in changes.itertuples():
        chg[pd.Timestamp(r[1]).date()].append((r.Action, r.CUSIP, r[7]))
    close = {(s, d): c for s, d, c in zip(px["sid"], px["date"], px["close"])}
    ret = {(s, d): r for s, d, r in zip(px["sid"], px["date"], px["ret"])}
    first_close = px.groupby("sid").first()["close"].to_dict()
    spin = {}
    for sid, rs in ev.items():
        for r in rs:
            if r["event_type"] == "SPINOFF":
                spin[(sid, r["ex_date"])] = r["terms"]["ratio"] * first_close[r["terms"]["distributed_security_id"]]

    def load(label, d):
        return {sid_of(r.CUSIP, d.isoformat()): float(r._6) for r in sheets[label].itertuples()}

    q = load("Jun2017", days[0])
    worst_p = worst_t = 0.0
    lp, lt = levels["price_return_level"].values, levels["total_return_level"].values
    for n, d in enumerate(days):
        if n:
            ds = d.isoformat()
            num_p = num_t = den = 0.0
            for sid, qk in list(q.items()):
                pc = close[(sid, days[n - 1])]
                c = close[(sid, d)]
                f = _split_factor(ev, sid, ds)
                den += qk * pc
                num_p += qk * (c * f + spin.get((sid, ds), 0.0))
                num_t += qk * pc * (1 + ret[(sid, d)])
                if f != 1.0:
                    q[sid] = qk * f
            worst_p = max(worst_p, abs(lp[n] / lp[n - 1] - num_p / den))
            worst_t = max(worst_t, abs(lt[n] / lt[n - 1] - num_t / den))
        for action, cu, shares in chg.get(d, []):
            sid = sid_of(cu, d.isoformat())
            if action == "DELETE":
                q.pop(sid, None)
            else:
                q[sid] = float(shares)
        if d in recon_day:
            q = load(recon_day[d], d)
    check("index: every day's price and total return levels recompute from the constituents' index shares, closes, "
          "splits, spin-offs and returns (worst daily gap %.1e, %.1e)" % (worst_p, worst_t),
          worst_p < 2e-5 and worst_t < 2e-5)


# ---------------------------------------------------------------------------------------------- short interest
def _short_interest(path, sm):
    si = pd.read_csv(path, sep="|", dtype={"Symbol": str, "RevisionFlag": str}, keep_default_na=False)
    cur = si["CurrentShortQuantity"].astype(float)
    adv = si["AverageDailyVolume"].astype(float)
    dtc = np.where(adv > 0, np.minimum(999.99, (cur / adv.replace(0, np.nan)).round(2)), 999.99)
    check("short interest: days to cover is the short position over average daily volume (%d rows)" % len(si),
          np.allclose(si["DaysToCover"].astype(float), dtc, atol=0.0051))
    prev = pd.to_numeric(si["PreviousShortQuantity"], errors="coerce")
    has = prev > 0
    chg = ((cur - prev) / prev * 100).round(2)
    check("short interest: change per cent from the previous position",
          np.allclose(si.loc[has, "ChangePercent"].astype(float), chg[has], atol=0.0051))
    rev = si[si["RevisionFlag"] == "R"]
    orig = si[si["RevisionFlag"] == ""].set_index(["SettlementDate", "Symbol"])["PublicationDate"]
    ok = all((r.SettlementDate, r.Symbol) in orig.index and orig[(r.SettlementDate, r.Symbol)] < r.PublicationDate
             for r in rev.itertuples())
    check("short interest: each revised row follows an original row for the same settlement and symbol (%d)" %
          len(rev), ok)


# ---------------------------------------------------------------------------------------------- sweep
def _sweep(path):
    s = pd.read_csv(path)
    d = pd.to_datetime(s["value_date"]).dt.date
    full = [dt.date(2018, 1, 1) + dt.timedelta(days=i) for i in range((W.SWEEP_LAST - dt.date(2018, 1, 1)).days + 1)]
    check("sweep: one row for every calendar day to %s" % W.SWEEP_LAST, list(d) == full)
    want = np.maximum(0.01, s["reference_rate_pct"] - s["spread_bp"] / 100.0)
    check("sweep: the sweep rate is the reference less the spread", np.allclose(s["sweep_rate_pct"], want,
                                                                              atol=0.00011))


# ---------------------------------------------------------------------------------------------- the live book
def _book(opath, fpath, px, sm):
    o = pd.read_csv(opath, dtype=str, keep_default_na=False)
    f = pd.read_csv(fpath, dtype=str, keep_default_na=False)
    dead = set(f.loc[f["exec_type"].isin(["X", "C"]), "ref_exec_id"])
    live = f[f["exec_type"].isin(["F", "C"]) & ~f["exec_id"].isin(dead)].copy()
    live["qty"] = live["qty"].astype(int)
    live["price"] = live["price"].astype(float)
    g = live.groupby("client_order_id").apply(lambda x: pd.Series({"q": x["qty"].sum(),
                                                                   "v": (x["qty"] * x["price"]).sum()}))
    o = o.set_index("order_id")
    oq = o["filled_qty"].astype(int)
    filled = oq[oq > 0]
    okq = (g.loc[filled.index, "q"] == filled).all()
    avg = (g.loc[filled.index, "v"] / g.loc[filled.index, "q"]).round(4)
    oka = np.allclose(avg, o.loc[filled.index, "avg_price"].astype(float), atol=0.00011)
    check("book: each order's filled quantity and average price are its standing executions' (%d orders)" % len(o),
          okq and oka)
    spells = defaultdict(list)
    for r in sm.itertuples():
        spells[r.ticker].append((r.effective_from, r.effective_to or "9999", int(r.security_id)))
    rng_ = {(s, d): (lo, hi) for s, d, lo, hi in zip(px["sid"], px["date"], px["low"], px["high"])}
    out = 0
    for r in f.itertuples():
        d = dt.datetime.strptime(r.trade_date, "%Y%m%d").date()
        sid = [x[2] for x in spells[r.symbol] if x[0] <= d.isoformat() <= x[1]]
        lo, hi = rng_[(sid[0], d)]
        if not (lo - 1e-9 <= float(r.price) <= hi + 1e-9) and r.exec_type != "C":
            out += 1
    check("book: every fill's price lies within its security's high and low that day (%d fills)" % len(f), out == 0,
          out)
    rate = np.where(f["trade_date"] >= W.FEE_CHANGE.strftime("%Y%m%d"), 0.010, 0.015)
    q = f["qty"].astype(int)
    okc = np.allclose(f["commission_usd"].astype(float), np.round(q * rate + 1e-9, 2), atol=0.0051) and \
        np.allclose(f["clearing_fee_usd"].astype(float), np.round(q * 0.00025 + 1e-9, 2), atol=0.0051)
    check("book: commissions follow the schedule in force on the trade date, clearing at $0.00025 a share", okc)
    bad_s = 0
    for td, sd in set(zip(f["trade_date"], f["settle_date"])):
        t = dt.datetime.strptime(td, "%Y%m%d").date()
        want = C.settle_date(t, 1 if t >= dt.date(2024, 5, 28) else 2)
        if want.strftime("%Y%m%d") != sd:
            bad_s += 1
    check("book: settlement on the second business day before 28 May 2024 and the first after", bad_s == 0, bad_s)
    early = 0
    for cu, rd in zip(o["created_utc"], o["rebalance_date"]):
        t = dt.datetime.strptime(cu, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=ZoneInfo("UTC")).astimezone(NY)
        if t.date().isoformat() != rd or t.time() >= dt.time(9, 30):
            early += 1
    check("book: every order was created before the open on its rebalance day in New York time", early == 0, early)


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    raise SystemExit(0 if run(target) else 1)
