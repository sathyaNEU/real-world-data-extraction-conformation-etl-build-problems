"""Every graded figure, computed from the shipped files alone (target/), plus the routes the ladder and the ask
sheet name. The build writes the goldens and figures.json from here; checks.py asserts the ladder against it and
against the clean world; verify.py recomputes the graded figures on its own code path."""
from __future__ import annotations

import datetime as dt
import os
import re
import sqlite3

import numpy as np
import pandas as pd

import records as RC

YE = dt.date(2026, 10, 31)
EXTRACT_FROM = dt.date(2021, 11, 1)
FORMATS = ["Hardback", "Trade paperback", "Paperback"]
FMT_MAP = {"HB": "Hardback", "Hardback": "Hardback", "TPB": "Trade paperback", "Trade Paperback": "Trade paperback",
           "PB": "Paperback", "Paperback": "Paperback"}
CHANNELS = ["Chain", "Online", "Wholesale", "Supermarket", "Independent", "Export"]


def dnum(d):
    return (d - dt.date(2020, 11, 2)).days


def isbn_clean(s):
    return s.astype(str).str.replace("-", "", regex=False).str.strip()


# ----------------------------------------------------------------------------------------------------------------
# Loading


class Pack:
    def __init__(self, folder):
        self.folder = folder
        p = lambda f: os.path.join(folder, f)
        self.accounts = pd.read_csv(p(RC.F_ACCOUNTS), dtype=str)
        legacy = {r.legacy_account_no: r.account_code for r in self.accounts.itertuples() if isinstance(r.legacy_account_no, str)}
        self.channel = dict(zip(self.accounts.account_code, self.accounts.channel))
        self.terms = dict(zip(self.accounts.account_code, self.accounts.terms))
        con = sqlite3.connect(p(RC.F_LEDGER))
        inv = pd.read_sql("SELECT * FROM invoice_lines", con)
        cr = pd.read_sql("SELECT * FROM credit_lines", con)
        con.close()
        for df, dc in ((inv, "invoice_date"), (cr, "credit_date")):
            df["isbn"] = isbn_clean(df["isbn"])
            df["acct"] = df["account_ref"].map(lambda a: legacy.get(a, a))
            df["channel"] = df["acct"].map(self.channel)
            df["terms"] = df["acct"].map(self.terms)
            df["date"] = pd.to_datetime(df[dc]).dt.date
            df["day"] = df["date"].map(dnum)
        self.inv = inv
        self.cr = cr
        t = pd.read_excel(p(RC.F_TITLES), dtype={"isbn13": str})
        t["isbn"] = isbn_clean(t["isbn13"])
        t["fmt"] = t["format"].map(FMT_MAP)
        t["pub"] = pd.to_datetime(t["pub_date"], dayfirst=True).dt.date
        self.titles = t
        self.fmt = dict(zip(t.isbn, t.fmt))
        self.inv["fmt"] = self.inv.isbn.map(self.fmt)
        self.cr["fmt"] = self.cr.isbn.map(self.fmt)
        ra = pd.read_csv(p(RC.F_RA), dtype=str)
        ra["isbn"] = isbn_clean(ra["isbn"])
        ra["date"] = pd.to_datetime(ra["date_issued"]).dt.date
        ra["qty_authorised"] = ra.qty_authorised.astype(int)
        ra["channel"] = ra.customer_account.map(self.channel)
        self.ra = ra
        rec = pd.read_csv(p(RC.F_RECEIPTS), dtype=str)
        rec["isbn"] = isbn_clean(rec["isbn"])
        rec["date"] = pd.to_datetime(rec["received"], dayfirst=True).dt.date
        for c in ("qty_received", "grade_saleable", "grade_hurt", "grade_unsaleable"):
            rec[c] = rec[c].astype(int)
        rec["hurts_tote"] = rec["hurts_tote"].fillna("")
        self.rec = rec
        sheets = pd.read_excel(p(RC.F_REINSPECT), sheet_name=None, dtype={"tote": str, "isbn": str})
        ri = pd.concat([s.assign(sheet=k) for k, s in sheets.items()], ignore_index=True)
        ri["isbn"] = isbn_clean(ri["isbn"])
        ri["date"] = pd.to_datetime(ri["inspected"], dayfirst=True).dt.date
        self.ri = ri
        self.panel = pd.read_csv(p(RC.F_PANEL), dtype={"isbn13": str})


# ----------------------------------------------------------------------------------------------------------------
# The hardback to paperback link (title and contributor; no key joins the two editions)


def norm_contrib(c):
    c = str(c).strip()
    if "," in c:
        last, first = [x.strip() for x in c.split(",", 1)]
        c = "%s %s" % (first, last)
    return re.sub(r"\s+", " ", c.lower())


def title_core(t):
    t = str(t).lower().split(":")[0]
    t = t.replace("&", " and ")
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"^(the|a|an) ", "", t)
    return t


def link_editions(titles):
    """For every hardback, the paperback of the same book (same contributor, same title core, published after it)."""
    t = titles.assign(c=titles.contributor.map(norm_contrib), k=titles.title.map(title_core))
    hb = t[t.fmt == "Hardback"]
    pb = t[t.fmt == "Paperback"]
    m = hb.merge(pb, on=["c", "k"], suffixes=("_hb", "_pb"))
    m = m[m.pub_pb > m.pub_hb]
    m["months"] = m.apply(lambda r: (r.pub_pb - r.pub_hb).days / 30.44, axis=1)
    m = m.sort_values(["isbn_hb", "pub_pb"]).drop_duplicates("isbn_hb")
    return m[["isbn_hb", "isbn_pb", "pub_hb", "pub_pb", "months", "title_hb", "title_pb", "c"]]


# ----------------------------------------------------------------------------------------------------------------
# The allowance


def open_population(P, T, sor_only=True):
    inv = P.inv[(P.inv.day <= T) & (P.inv.day > T - 365)]
    if sor_only:
        inv = inv[inv.terms == "SOR"]
    return inv


def development(P, T, seg, mature_lag=425, start=EXTRACT_FROM, max_age=70, keep_dit=False, years=None):
    """The returns triangle: the share of invoiced copies credited as returns, quoting the invoice, by weeks from the
    invoice to the credit; seg maps an invoice line (a row of P.inv) to its segment key. Returns the allowance at T
    (the credit still to come on open invoice lines, at each line's own net price) and its parts by segment."""
    inv = P.inv[P.inv.terms == "SOR"].copy()
    inv["seg"] = seg(inv)
    inv["price"] = inv.net_value / inv.qty
    cr = P.cr[(P.cr.day <= T) & ((P.cr.reason_code == "RET") | keep_dit)]
    lo = (start - dt.date(2020, 11, 2)).days
    if years:
        lo = max(lo, T - mature_lag - int(365.25 * years))
    mat = inv[(inv.day >= lo) & (inv.day <= T - mature_lag)]
    c = cr.merge(mat[["invoice_no", "day", "seg"]].rename(columns={"day": "iday"}), left_on="against_invoice", right_on="invoice_no")
    c["age"] = np.clip((c.day - c.iday) // 7, 0, max_age)
    tot = mat.groupby("seg").qty.sum()
    curves = {}
    for k, g in c.groupby("seg"):
        h = np.bincount(g.age.values, weights=g.qty.values, minlength=max_age + 1)
        curves[k] = np.cumsum(h) / tot[k]
    for k in tot.index:
        curves.setdefault(k, np.zeros(max_age + 1))
    op = inv[(inv.day <= T) & (inv.day > T - 365)].copy()
    op["a"] = np.clip((T - op.day) // 7, 0, max_age)
    parts = {}
    total = 0.0
    for k, g in op.groupby("seg"):
        cv = curves.get(k)
        if cv is None:
            continue
        rem = cv[max_age] - cv[g.a.values]
        v = float((g.qty.values * rem * g.price.values).sum())
        parts[k] = v
        total += v
    return total, parts, curves


def seg_fmt_channel(df):
    return df.fmt + "|" + df.channel


def seg_fmt(df):
    return df.fmt


def make_quick_seg(P, threshold=8.0, with_channel=True):
    L = link_editions(P.titles)
    quick = set(L[L.months <= threshold].isbn_hb)

    def seg(df):
        q = df.isbn.isin(quick) & (df.fmt == "Hardback")
        base = df.fmt + ("|" + df.channel if with_channel else "")
        return base + np.where(q, "|paperback within %g months" % threshold, "")
    return seg


def allowance_by_format(parts):
    out = {f: 0.0 for f in FORMATS}
    for k, v in parts.items():
        out[k.split("|")[0]] += v
    return out


def golden_allowance(P, T=None):
    T = dnum(YE) if T is None else T
    tot, parts, _ = development(P, T, make_quick_seg(P, 8.0, True))
    return tot, allowance_by_format(parts)


def default_allowance(P, T=None):
    T = dnum(YE) if T is None else T
    tot, parts, _ = development(P, T, seg_fmt_channel)
    return tot, allowance_by_format(parts)


def trailing_rate_allowance(P, T=None):
    """Rung 0: the auditor's check, a trailing twelve months' return rate by format and channel applied to the open
    invoices, phased by the share of a year's returns that arrive after each line's age."""
    T = dnum(YE) if T is None else T
    tot, parts, curves = development(P, T, seg_fmt_channel, years=1)
    return tot, allowance_by_format(parts)


def family(P, T=None):
    """The routes a competent analyst builds, with and without the step."""
    T = dnum(YE) if T is None else T
    rows = []
    for name, seg in (("format x channel", seg_fmt_channel), ("format", seg_fmt)):
        for ml in (400, 425, 450):
            for yrs in (None, 3, 2):
                v, parts, _ = development(P, T, seg, mature_lag=ml, years=yrs)
                rows.append(dict(route="no step", seg=name, mature_lag=ml, years=yrs, threshold=None, value=v,
                                 hb=allowance_by_format(parts)["Hardback"]))
    for thr in (6.0, 7.0, 8.0, 9.0, 10.0):
        for wc in (True, False):
            for ml in (400, 425, 450):
                for yrs in (None, 3):
                    v, parts, _ = development(P, T, make_quick_seg(P, thr, wc), mature_lag=ml, years=yrs)
                    rows.append(dict(route="step", seg="format x channel" if wc else "format", mature_lag=ml, years=yrs,
                                     threshold=thr, value=v, hb=allowance_by_format(parts)["Hardback"]))
    return pd.DataFrame(rows)


def backtest(P, years=(2024, 2025)):
    """The default route struck at earlier year ends against the credits that followed on the copies then invoiced."""
    out = {}
    for y in years:
        T = dnum(dt.date(y, 10, 31))
        est, _ = default_allowance(P, T)
        inv = open_population(P, T)
        f = P.cr[(P.cr.day > T) & (P.cr.reason_code == "RET") & P.cr.against_invoice.isin(inv.invoice_no)]
        out[y] = (est, float(f.net_value.sum()))
    return out


# ----------------------------------------------------------------------------------------------------------------
# The asks


def fy_quarter(d):
    return {11: 1, 12: 1, 1: 1, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 4, 9: 4, 10: 4}[d.month]


def in_fy2026(d):
    return dt.date(2025, 11, 1) <= d <= YE


def receipts_clean(P):
    """The copies of our titles that really came in: one day's export sent twice comes out (its rows are exact
    copies), other publishers' copies come out (their ISBNs are not on our title master), and so does a delivery
    booked in a second time: a delivery reference whose lines repeat, line for line (authorisation, ISBN, copies and
    grades), a delivery booked before it, and which takes each of those authorisation lines past its authorised
    copies by at least the copies it repeats. Copies sent beyond an authorisation stay: they came in."""
    rec = P.rec.drop_duplicates()                                   # the re-sent export
    ours = set(P.titles.isbn)
    rec = rec[rec.isbn.isin(ours)].copy()
    auth = P.ra.groupby(["ra_number", "isbn"]).qty_authorised.sum()
    tot = rec.groupby(["ra_ref", "isbn"]).qty_received.sum()
    excess = {k: v - auth[k] for k, v in tot.items() if k in auth.index}
    rec = rec.sort_values(["date", "delivery_ref"])
    sig = {}
    for dl, g in rec.groupby("delivery_ref", sort=False):
        sig[dl] = tuple(sorted(zip(g.ra_ref, g.isbn, g.qty_received, g.grade_saleable, g.grade_hurt, g.grade_unsaleable)))
    seen = set()
    drop = set()
    for dl in dict.fromkeys(rec.delivery_ref):
        s = sig[dl]
        if s in seen and all(excess.get((a, b), 0) >= q for a, b, q, *_ in s):
            drop.add(dl)
            for a, b, q, *_ in s:
                excess[(a, b)] -= q
            continue
        seen.add(s)
    rec = rec[~rec.delivery_ref.isin(drop)]
    rachan = dict(zip(P.ra.ra_number, P.ra.channel))
    rec["channel"] = rec.ra_ref.map(rachan)
    rec["fmt"] = rec.isbn.map(P.fmt)
    return rec, drop


def ask_received(P, rec=None):
    rec = receipts_clean(P)[0] if rec is None else rec
    f = rec[rec.date.map(in_fy2026)]
    g = f.groupby(["channel", f.date.map(fy_quarter)]).qty_received.sum()
    return {(c, q): int(g.get((c, q), 0)) for c in CHANNELS for q in (1, 2, 3, 4)}


def reinspection_final(P, rec):
    """Each tote's re-inspection as it stands, read against the hurts the clean deliveries put into it: rows that add up
    to the tote's hurts are sessions of one inspection; a row repeating the tote's full quantity later is a recount and
    stands in place of the earlier count."""
    ri = P.ri[P.ri.date <= YE].sort_values(["tote", "date"])
    H = rec[rec.hurts_tote != ""].groupby("hurts_tote").grade_hurt.sum()
    out, unresolved = [], []
    for tote, g in ri.groupby("tote"):
        q = g.qty_inspected.values
        h = H.get(tote)
        if len(g) == 1:
            out.append((tote, int(q[0]), int(g.pulped.iloc[0])))
        elif h is not None and q.sum() == h:
            out.append((tote, int(q.sum()), int(g.pulped.sum())))
        elif h is not None and (q == h).all():
            out.append((tote, int(q[-1]), int(g.pulped.iloc[-1])))
        else:
            unresolved.append(tote)
            out.append((tote, int(q[-1]), int(g.pulped.iloc[-1])))
    df = pd.DataFrame(out, columns=["tote", "inspected", "pulped"])
    df.attrs["unresolved"] = unresolved
    return df


def ask_scrapped(P, rec=None):
    """Of the copies of our titles received back in FY2026, the share scrapped by the year end: graded unsaleable on
    receipt, or graded hurt and pulped at re-inspection, a tote's pulped copies shared among the deliveries whose
    hurts went into it in proportion to those hurts."""
    rec = receipts_clean(P)[0] if rec is None else rec
    f = rec[rec.date.map(in_fy2026)].copy()
    fin = reinspection_final(P, rec).set_index("tote")
    hurts_by_tote = rec[rec.hurts_tote != ""].groupby("hurts_tote").grade_hurt.sum()
    def pulped_share(row):
        if not row.hurts_tote or row.hurts_tote not in fin.index:
            return 0.0
        h = hurts_by_tote.get(row.hurts_tote, 0)
        return float(fin.loc[row.hurts_tote, "pulped"]) * row.grade_hurt / h if h else 0.0
    f["pulped"] = f.apply(pulped_share, axis=1)
    f["scrapped"] = f.grade_unsaleable + f.pulped
    by_ch = f.groupby("channel").agg(s=("scrapped", "sum"), q=("qty_received", "sum"))
    by_f = f.groupby("fmt").agg(s=("scrapped", "sum"), q=("qty_received", "sum"))
    ch = {c: round(100 * by_ch.loc[c, "s"] / by_ch.loc[c, "q"], 1) for c in CHANNELS if c in by_ch.index}
    fm = {x: round(100 * by_f.loc[x, "s"] / by_f.loc[x, "q"], 1) for x in FORMATS if x in by_f.index}
    raw = dict(ch={c: 100 * by_ch.loc[c, "s"] / by_ch.loc[c, "q"] for c in by_ch.index},
               fm={x: 100 * by_f.loc[x, "s"] / by_f.loc[x, "q"] for x in by_f.index})
    return ch, fm, raw
