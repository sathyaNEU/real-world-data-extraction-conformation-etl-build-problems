"""task183 calc: every golden figure computed from the shipped files in target/ the way a solver has to, plus the
default path and the rival readings the checks compare it with. Reads only target/ (and nothing from sim)."""
from __future__ import annotations

import csv
import datetime as dt
import os
from collections import defaultdict

from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal

import numpy as np
import openpyxl

REVIEW_START = dt.date(2025, 10, 1)
REVIEW_END = dt.date(2026, 9, 30)
LINE = 40000.0

F = dict(
    acct="business_account_transactions_2025-01_2026-09.csv",
    ms="merchant_services_daily_trade_2025-01_2026-09.csv",
    mreg="merchant_register_2026-10.xlsx",
    seg="cash_segment_review_list_2025-26.xlsx",
    till="till_service_daily_totals_2025-01_2026-09.csv",
)


def _rows(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _xlsx(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    it = ws.iter_rows(values_only=True)
    head = None
    out = []
    for r in it:
        if head is None:
            if r and r[0] is not None and isinstance(r[0], str) and r.count(None) < len(r) - 2:
                head = [str(x) for x in r]
            continue
        if all(v is None for v in r):
            continue
        out.append(dict(zip(head, ["" if v is None else v for v in r])))
    return out


def dmy(s):
    return dt.datetime.strptime(s, "%d/%m/%Y").date()


class Pack:
    def __init__(self, target):
        self.t = target
        p = lambda k: os.path.join(target, F[k])
        raw = _rows(p("acct"))
        seen, self.acct = set(), []
        self.dupes = 0
        for r in raw:
            if r["Transaction Ref"] in seen:
                self.dupes += 1
                continue
            seen.add(r["Transaction Ref"])
            self.acct.append(r)
        self.seg = _xlsx(p("seg"))
        self.mreg = _xlsx(p("mreg"))
        self.ms = _rows(p("ms"))
        self.till = _rows(p("till"))
        self.cust = {s["Customer ID"]: s for s in self.seg}
        self.acct_to_cid = {}
        for s in self.seg:
            for k in ("Current account", "Second account"):
                if s.get(k):
                    self.acct_to_cid[str(s[k]).split()[-1]] = s["Customer ID"]
        self.mid_to_cid = {str(m["MID"]): m["Customer ID"] for m in self.mreg}
        self.till_cids = {s["Customer ID"] for s in self.seg if s["Till service"] == "Yes"}

    # ---- lodgements, dated by the day the cash was handed in (BCR-3 3.2) ----------------------------------------
    def lodgements(self, by="counter"):
        out = defaultdict(list)
        for r in self.acct:
            if r["Type"] != "LDG":
                continue
            cid = self.acct_to_cid.get(r["Account"])
            if cid is None:
                continue
            posted = dmy(r["Posting Date"])
            amt = float(r["Credit"])
            if r["Description"] == "AN POST LODGEMENT":
                _, office, ddmm, hhmm = r["Reference"].split()
                d, m = int(ddmm[:2]), int(ddmm[3:5])
                y = posted.year if m <= posted.month else posted.year - 1
                counter = dt.date(y, m, d)
                ch = "post"
            else:
                counter = posted
                ch = "branch"
                hhmm = r["Reference"].split()[1]
            day = counter if by == "counter" else posted
            out[cid].append(dict(day=day, amount=amt, channel=ch, time=hhmm, posted=posted, acct=r["Account"]))
        for cid in out:
            out[cid].sort(key=lambda x: (x["day"], x["time"]))
        return out

    # ---- card trade by trading day (gross less refunds, all of a customer's terminals) --------------------------
    def card_by_day(self, basis="trading", net_of_refunds=True):
        out = defaultdict(lambda: defaultdict(float))
        for r in self.ms:
            cid = self.mid_to_cid.get(r["mid"])
            if cid is None:
                continue
            g = int(r["gross_sales_cent"]) - (int(r["refunds_cent"]) if net_of_refunds else 0)
            d = dt.date.fromisoformat(r["trading_date"] if basis == "trading" else r["settlement_date"])
            out[cid][d] += g / 100.0
        return out

    def till_cash(self):
        out = defaultdict(lambda: defaultdict(float))
        for r in self.till:
            out[r["customer_id"]][dt.date.fromisoformat(r["trading_date"])] += float(r["cash_sales"])
        return out


def windows(lods, card, include_day=False):
    """Each lodgement's window: the trading days after the previous lodgement's day up to the day before it (the
    lodgements are morning lodgements of the takings since the last one). Returns (lodgement, window card) pairs."""
    out = []
    prev = None
    for L in lods:
        if prev is not None:
            a = prev + dt.timedelta(days=0 if not include_day else 1)
            b = L["day"] - dt.timedelta(days=1 if not include_day else 0)
            x = 0.0
            d = a
            while d <= b:
                x += card.get(d, 0.0)
                d += dt.timedelta(days=1)
            out.append((L, x, (b - a).days + 1))
        prev = L["day"]
    return out


def fit(pairs, kind="ols"):
    y = np.array([L["amount"] for L, _, _ in pairs])
    x = np.array([w for _, w, _ in pairs])
    n = np.array([k for _, _, k in pairs], float)
    if kind == "origin":
        s = float((x * y).sum() / (x * x).sum())
        return 0.0, s, y, x
    X = np.column_stack([np.ones_like(x), x])
    if kind == "ols":
        b = np.linalg.lstsq(X, y, rcond=None)[0]
    elif kind == "wls":
        w = np.sqrt(1.0 / n)
        b = np.linalg.lstsq(X * w[:, None], y * w, rcond=None)[0]
    elif kind == "huber":
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        for _ in range(60):
            r = y - X @ b
            sc = np.median(np.abs(r - np.median(r))) / 0.6745 + 1e-9
            u = np.abs(r / sc)
            w = np.where(u <= 1.345, 1.0, 1.345 / u)
            sw = np.sqrt(w)
            b = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)[0]
    elif kind == "days":
        Xd = np.column_stack([np.ones_like(x), x, n])
        b3 = np.linalg.lstsq(Xd, y, rcond=None)[0]
        return float(b3[0] + 0), float(b3[1]), y, x
    else:
        raise ValueError(kind)
    return float(b[0]), float(b[1]), y, x


def in_year(L):
    return REVIEW_START <= L["day"] <= REVIEW_END


def unexplained(P, kind="ols", fit_on="year", include_day=False, card_basis="trading", lod_by="counter",
                net_refunds=True):
    """The golden family: each customer's cash lodged in the review year less the cash that moves with its own card
    trade lodgement by lodgement, at the customer's own ratio, with a part that does not move allowed."""
    lods = P.lodgements(by=lod_by)
    card = P.card_by_day(basis=card_basis, net_of_refunds=net_refunds)
    out = {}
    for cid in P.cust:
        pairs_all = windows(lods.get(cid, []), card.get(cid, {}), include_day=include_day)
        pairs_year = [p for p in pairs_all if in_year(p[0])]
        pairs_fit = pairs_year if fit_on == "year" else [p for p in pairs_all if p[0]["day"] <= REVIEW_END]
        a, s, _, _ = fit(pairs_fit, kind)
        y = sum(L["amount"] for L, _, _ in pairs_year)
        x = sum(w for _, w, _ in pairs_year)
        out[cid] = y - s * x
    return out


def till_figures(P):
    """BCR-3 4.2: for a till customer, the cash lodged in the review year beyond the cash sales its till recorded
    in the review year."""
    lods = P.lodgements()
    tc = P.till_cash()
    out = {}
    for cid in P.till_cids:
        y = sum(L["amount"] for L in lods.get(cid, []) if in_year(L))
        c = sum(v for d, v in tc[cid].items() if REVIEW_START <= d <= REVIEW_END)
        out[cid] = y - c
    return out


def golden(P):
    fam = unexplained(P, "ols")
    tf = till_figures(P)
    fig = {}
    for cid in P.cust:
        fig[cid] = tf[cid] if cid in P.till_cids else fam[cid]
    referred = sorted([c for c in fig if fig[c] > LINE], key=lambda c: -fig[c])
    return fig, referred


def default_path(P, stat="median"):
    """The field's AML screen: cash intensity against the trade's peers; the cash its trading took read as its card
    takings at the peer ratio (till customers by their till, as BCR-3 4.2 files)."""
    lods = P.lodgements()
    card = P.card_by_day()
    tf = till_figures(P)
    cash, cardy = {}, {}
    for cid in P.cust:
        cash[cid] = sum(L["amount"] for L in lods.get(cid, []) if in_year(L))
        cardy[cid] = sum(v for d, v in card.get(cid, {}).items() if REVIEW_START <= d <= REVIEW_END)
    ratio = {c: cash[c] / cardy[c] for c in P.cust}
    trades = defaultdict(list)
    for c, s in P.cust.items():
        trades[s["Trade"]].append(ratio[c])
    agg = {t: (float(np.median(v)) if stat == "median" else float(np.mean(v)) if stat == "mean" else None)
           for t, v in trades.items()}
    if stat == "pooled":
        num, den = defaultdict(float), defaultdict(float)
        for c, s in P.cust.items():
            num[s["Trade"]] += cash[c]
            den[s["Trade"]] += cardy[c]
        agg = {t: num[t] / den[t] for t in num}
    fig = {}
    for c, s in P.cust.items():
        fig[c] = tf[c] if c in P.till_cids else cash[c] - cardy[c] * agg[s["Trade"]]
    referred = sorted([c for c in fig if fig[c] > LINE], key=lambda c: -fig[c])
    return fig, referred, dict(cash=cash, card=cardy, ratio=ratio, peer=agg)


# ---- the asks -------------------------------------------------------------------------------------------------
F.update(ap="an_post_business_lodgements_2025-10_2026-09.csv", tlog="till_service_z_report_log_2025-10_2026-10.csv")
MONTHS = ["2025-10", "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06",
          "2026-07", "2026-08", "2026-09"]
AP_FEE_PER, AP_FEE_RATE = 1.15, 0.00065


def _five(x):
    return abs(x / 5.0 - round(x / 5.0)) < 1e-9


def ap_rows(target):
    seen, out = set(), []
    for r in _rows(os.path.join(target, F["ap"])):
        if r["ap_ref"] in seen:
            continue
        seen.add(r["ap_ref"])
        out.append(r)
    return out


def ap_cash(r, mode="golden"):
    notes, coin = float(r["notes_eur"]), float(r["coin_eur"])
    if mode == "golden":
        return notes if not _five(notes) else round(notes + coin, 2)      # banknotes come in fives
    if mode == "notes_only":
        return notes
    return round(notes + coin, 2)


def ap_fee(cash, rounding="half_up"):
    """Schedule 2: EUR 1.15 and 0.065 per cent of the lodgement's cash, rounded to the cent, a half cent up (1.2)."""
    exact = Decimal("1.15") + Decimal("0.00065") * Decimal("%.2f" % cash)
    if rounding == "float":
        return round(float(exact), 2)
    rule = ROUND_HALF_UP if rounding == "half_up" else ROUND_HALF_EVEN
    return float(exact.quantize(Decimal("0.01"), rounding=rule))


def ap_figures(target, mode="golden", rounding="half_up"):
    """Each month's business lodgements at post office counters, the cash in them and Schedule 2's fees."""
    out = {m: [0, Decimal("0"), Decimal("0")] for m in MONTHS}
    for r in ap_rows(target):
        m = r["counter_date"][:7]
        if m not in out:
            continue
        cash = ap_cash(r, mode)
        out[m][0] += 1
        out[m][1] += Decimal("%.2f" % cash)
        out[m][2] += Decimal("%.2f" % ap_fee(cash, rounding))
    return {m: (v[0], float(v[1]), float(v[2])) for m, v in out.items()}


def tlog_rows(target):
    return _rows(os.path.join(target, F["tlog"]))


def till_days(P, rows, mode="golden"):
    """Each Z-report's trading day. golden: the day the till's own card terminal took the same card sales, in Z
    order after the till's previous Z. The others are the routes a reader without the terminal takes."""
    by = defaultdict(list)
    for r in rows:
        by[r["till_account"]].append(r)
    card = P.card_by_day() if mode in ("golden", "terminal_count") else None
    out = []
    for t, zs in by.items():
        zs.sort(key=lambda r: int(r["z_no"]))
        cid = zs[0]["customer_id"]
        if mode in ("golden", "terminal_count"):
            days = sorted(d for d, v in card.get(cid, {}).items() if v > 0)
            batches = defaultdict(list)
            for r in zs:
                batches[r["received_at"]].append(r)
            prev = None
            for at_s in sorted(batches):
                g = sorted(batches[at_s], key=lambda r: int(r["z_no"]))
                at = dt.datetime.strptime(at_s, "%Y-%m-%d %H:%M:%S")
                bound = at.date() - dt.timedelta(days=1) if at.hour < 12 else at.date()   # a Z follows its day
                lo = prev if prev is not None else bound - dt.timedelta(days=30)
                cand = [d for d in days if lo < d <= bound]
                if mode == "golden":
                    i, take = 0, []
                    for r in g:
                        want = round(float(r["card_sales"]), 2)
                        while i < len(cand) and round(card[cid][cand[i]], 2) != want:
                            i += 1
                        if i >= len(cand):
                            raise ValueError("Z %s of %s received %s meets none of its terminal's days" % (
                                r["z_no"], t, at_s))
                        take.append(cand[i])
                        i += 1
                else:
                    take = cand[-len(g):]                       # the terminal's last days, one per Z
                out.extend(zip(g, take))
                prev = take[-1]
        else:
            groups = defaultdict(list)
            for r in zs:
                groups[r["received_at"]].append(r)
            for at_s, g in groups.items():
                at = dt.datetime.strptime(at_s, "%Y-%m-%d %H:%M:%S")
                g.sort(key=lambda r: int(r["z_no"]))
                if mode == "received":
                    out.extend((r, at.date()) for r in g)
                    continue
                # the reader's own reconstruction: a Z sent after midnight or in the morning closes yesterday, an
                # evening Z closes today, and a batch fills the days back from there one Z a day
                end = at.date() - dt.timedelta(days=1) if at.hour < 12 else at.date()
                for k, r in enumerate(reversed(g)):
                    out.append((r, end - dt.timedelta(days=k)))
    return out


def till_figures_ask(P, target, mode="golden"):
    """Each month's cash sales and paid-outs the till service recorded for its customers, by trading day (with the
    count of Z-reports kept for the checks)."""
    out = {m: [0, 0.0, 0.0] for m in MONTHS}
    for r, d in till_days(P, tlog_rows(target), mode):
        m = d.isoformat()[:7]
        if m not in out:
            continue
        out[m][0] += 1
        out[m][1] += float(r["cash_sales"])
        out[m][2] += float(r["paid_outs"])
    return {m: (v[0], round(v[1], 2), round(v[2], 2)) for m, v in out.items()}
