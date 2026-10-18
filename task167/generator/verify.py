"""task167 independent verifier. Reads only the bundle under TARGET_DIR (and, beside it, the goldens, figures.json and
submission.md), imports no generator module, and recomputes on its own code path (pandas, a rule read from the policy
PDF wherever the policy files one): the call reserve, the expected calls by strategy, the out-of-sample record that
chooses the schedule, the easy routes' reserves, Ask A's nine net asset values and Ask B's six reserve-asset figures.
Every format the pack ships is read back through this file's own extractor, each with a positive control.

    python3 verify.py TARGET_DIR"""
from __future__ import annotations

import datetime as dt
import json
import math
import os
import re
import sys

import numpy as np
import pandas as pd
from docx import Document
from openpyxl import load_workbook
from pypdf import PdfReader

OUT = []
DIST_TYPES = {"Return of capital", "Realised gain", "Income"}
STRATS = ["Buyout", "Growth equity", "Venture capital", "Private credit"]
YEAR = 2027


def ok(label, cond, detail=""):
    OUT.append((label, bool(cond), detail))


def find(files, pattern):
    hit = [f for f in files if re.search(pattern, f)]
    if len(hit) != 1:
        raise SystemExit("verify: expected one file matching %s, found %s" % (pattern, hit))
    return hit[0]


def month_no(d):
    return d.year * 12 + d.month - 1


def as_date(x):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return None
    return pd.Timestamp(x).date()


def nearest(x, unit):
    return int(math.floor(x / unit + 0.5) * unit)


# ------------------------------------------------------------------------------------------------------- readers
def pdf_words(path):
    return " ".join(" ".join((pg.extract_text() or "") for pg in PdfReader(path).pages).split())


def docx_words(path):
    doc = Document(path)
    parts = [p.text for p in doc.paragraphs]
    for t in doc.tables:
        for row in t.rows:
            parts.extend(c.text for c in row.cells)
    return " ".join(" ".join(parts).split())


def sheet_rows(path, sheet):
    wb = load_workbook(path, read_only=True, data_only=True)
    return [list(r) for r in wb[sheet].iter_rows(values_only=True)]


def table_from(rows, first_col):
    i = next(k for k, r in enumerate(rows) if r and r[0] == first_col)
    head = rows[i]
    body = [r for r in rows[i + 1:] if r and r[0] not in (None, "")]
    return pd.DataFrame(body, columns=head)


class Bundle:
    def __init__(self, target):
        self.t = target
        fs = sorted(os.listdir(target))
        self.files = fs
        self.f_reg = find(fs, r"commitments_register\.xlsx$")
        self.f_act = find(fs, r"capital_activity.*\.csv$")
        self.f_leg = find(fs, r"^legacy_.*notices.*\.xlsx$")
        self.f_fx = find(fs, r"reference_rates.*\.csv$")
        self.f_pol = find(fs, r"policy.*\.pdf$")
        self.f_cap = find(fs, r"capital_account_summary.*\.xlsx$")
        self.f_pos = find(fs, r"custody_positions.*\.csv$")
        self.f_cact = find(fs, r"custody_activity.*\.csv$")
        self.f_dict = find(fs, r"dictionary\.xlsx$")
        self.f_man = find(fs, r"manifest\.csv$")
        self.f_docx = find(fs, r"\.docx$")
        self.f_perf = find(fs, r"performance.*\.csv$")
        p = lambda f: os.path.join(target, f)
        # xlsx through openpyxl
        reg_rows = sheet_rows(p(self.f_reg), "Commitments")
        self.reg = table_from(reg_rows, "Fund ID")
        self.leg = table_from(sheet_rows(p(self.f_leg), "Notices"), "Notice No.")
        cap_rows = sheet_rows(p(self.f_cap), "Summary")
        self.cap_header = " ".join(str(c) for r in cap_rows[:3] for c in r if c)
        self.cap = table_from(cap_rows, "Fund code")
        self.dict = table_from(sheet_rows(p(self.f_dict), "Fields"), "File")
        # csv through pandas
        self.act = pd.read_csv(p(self.f_act), dtype={"amount": float}, keep_default_na=False)
        self.fx = pd.read_csv(p(self.f_fx), parse_dates=["date"])
        self.pos = pd.read_csv(p(self.f_pos), dtype=str, keep_default_na=False)
        self.cact = pd.read_csv(p(self.f_cact), dtype=str, keep_default_na=False)
        self.man = pd.read_csv(p(self.f_man), dtype=str, keep_default_na=False)
        self.perf = pd.read_csv(p(self.f_perf), dtype=str, keep_default_na=False)
        # documents
        self.policy = pdf_words(p(self.f_pol))
        self.memo_docx = docx_words(p(self.f_docx))


def read_back(b):
    """one positive control per format and per document the call or an ask leans on"""
    ok("READ xlsx: the register's header and 194 vehicle rows", list(b.reg.columns[:4]) == ["Fund ID", "Fund", "Vehicle",
       "Administrator code"] and len(b.reg) == 194, "%d rows" % len(b.reg))
    calls = b.leg[["Investments", "Management Fees", "Fund Expenses", "Organisation Costs"]].sum(axis=1)
    dists = b.leg[["Return of Capital", "Capital Gains", "Income"]].sum(axis=1)
    ok("READ xlsx: every legacy notice's Net Amount is its calls less its distributions", (calls - dists - b.leg["Net Amount"]).abs().max() < 0.01,
       "%d notices" % len(b.leg))
    ok("READ xlsx: the capital account summary's header line", "Amounts in each fund's currency" in b.cap_header, "")
    ok("READ xlsx: the dictionary describes only shipped files", set(b.dict["File"]) <= set(b.files), "")
    ok("READ csv: the activity extract, 25,000 rows or more, every line Settled or Cancelled", len(b.act) >= 25000 and
       set(b.act["status"]) == {"Settled", "Cancelled"}, "%d rows" % len(b.act))
    ok("READ csv: the reference rates, one per business day", b.fx["date"].dt.weekday.max() <= 4 and b.fx["date"].is_unique, "")
    for acct in sorted(set(b.pos["account"])):
        rows = b.pos[(b.pos["account"] == acct) & (b.pos["description"] != "ACCOUNT TOTAL")]
        total = b.pos[(b.pos["account"] == acct) & (b.pos["description"] == "ACCOUNT TOTAL")]["market_value_usd"].astype(float)
        ok("READ csv: positions for %s tie to the custodian's account total" % acct, len(total) == 1 and
           abs(rows["market_value_usd"].astype(float).sum() - total.iloc[0]) < 0.01, "")
    ok("READ csv: the manifest lists every other shipped file", set(b.man["file"]) == set(b.files) - {b.f_man}, "")
    ok("READ csv: the performance extract's codes join the register", set(b.perf["fund_code"]) <= set(b.reg["Administrator code"]), "")
    ok("READ pdf: the policy's title and filed rules come through the extractor", "Liquidity and Reserve Policy" in b.policy and
       "2.2 The call reserve for a year" in b.policy and "Schedule 1" in b.policy, "")
    ok("READ docx: the grants memo's text comes through the extractor", "grants budget" in b.memo_docx.lower() and
       len(b.memo_docx) > 400, "%d characters" % len(b.memo_docx))


# ------------------------------------------------------------------------------------------------- the policy
def policy_rules(b):
    t = b.policy
    r = {}
    m = re.search(r"rounded up to the next \$(\d+) million", t)
    r["round_up_musd"] = int(m.group(1)) if m else None
    m = re.search(r"Approved money market fund: (.+?) \(all share classes\)", t)
    r["schedule1"] = m.group(1).strip() if m else None
    r["months_from_first_close"] = "counted in months from its first close" in t
    r["fees_in"] = "management fees, partnership expenses and organisational expenses" in t
    r["gross"] = "before any distribution a fund sets against a call" in t
    r["new_out"] = "are not part of the call reserve" in t
    r["rate_rule"] = "reference rate for the last business day of the prior year" in t
    r["settled"] = "at market value on a settled basis" in t
    r["bills_by_ye"] = "Treasury bills maturing on or before 31 December of the reserve year" in t
    r["roll"] = "adjusted for the contributions paid and distributions received after the date of that value" in t
    ok("POLICY the rules the call and the asks lean on are read from the PDF", r["round_up_musd"] == 50 and
       r["schedule1"] == "Ironvale Government Money Market Fund" and all(v for k, v in r.items()
                                                                      if k not in ("round_up_musd", "schedule1")), str(r))
    return r


# ----------------------------------------------------------------------------------------------- the call books
def call_frames(b):
    """settled calls and distributions by vehicle and month, the legacy file before the current file's first value date"""
    a = b.act[b.act["status"] == "Settled"].copy()
    a["vd"] = pd.to_datetime(a["value_date"])
    a["side"] = np.where(a["line_type"].isin(list(DIST_TYPES)), "dist", "call")
    a["amt"] = np.where(a["side"] == "dist", -a["amount"], a["amount"])
    cut = a["vd"].min()
    reg = b.reg.copy()
    key = lambda s: re.sub(r"[^A-Z0-9]", "", str(s).upper())
    by_name = {key(n): c for n, c in zip(reg["Former administrator name"], reg["Administrator code"]) if n}
    lg = b.leg.copy()
    lg["code"] = [by_name.get(key(n)) for n in lg["Fund"]]
    ok("JOIN every legacy notice joins the register through the former administrator name", lg["code"].notna().all(), "")
    ok("JOIN every activity line joins the register through the administrator code",
       set(b.act["fund_code"]) <= set(reg["Administrator code"]), "")
    lg["vd"] = pd.to_datetime(lg["Payment Date"])
    over = lg[lg["vd"] >= cut]
    lc = lg[["Investments", "Management Fees", "Fund Expenses", "Organisation Costs"]].sum(axis=1)
    ld = lg[["Return of Capital", "Capital Gains", "Income"]].sum(axis=1)
    lg_calls = pd.DataFrame(dict(code=lg["code"], vd=lg["vd"], side="call", amt=lc))
    lg_dists = pd.DataFrame(dict(code=lg["code"], vd=lg["vd"], side="dist", amt=ld))
    leg_long = pd.concat([lg_calls, lg_dists])
    leg_long = leg_long[leg_long["amt"] != 0]
    # the handover quarter: the current file re-keyed the former administrator's notices from its first value date
    a_over = a[(a["vd"] <= lg["vd"].max()) & (a["side"] == "call")].groupby("fund_code")["amt"].sum()
    l_over = leg_long[(leg_long["vd"] >= cut) & (leg_long["side"] == "call")].groupby("code")["amt"].sum()
    ok("HANDOVER the overlap's calls agree in both files, vehicle by vehicle", len(over) > 0 and
       (a_over.reindex(l_over.index).fillna(0) - l_over).abs().max() < 1.0, "%d legacy notices after %s" % (len(over), cut.date()))
    flows = pd.concat([pd.DataFrame(dict(code=a["fund_code"], vd=a["vd"], side=a["side"], amt=a["amt"])),
                       leg_long[leg_long["vd"] < cut]], ignore_index=True)
    return flows, cut


def fund_table(b, flows):
    reg = b.reg.copy()
    reg["fund"] = reg["Fund ID"].str.replace(r"P$", "", regex=True)
    reg["fc"] = [as_date(x) for x in reg["First close"]]
    main = reg[reg["Vehicle"] == "Main"].set_index("fund")
    com = reg.groupby("fund")["Commitment"].sum()
    funds = pd.DataFrame(dict(strategy=main["Strategy"], vintage=main["Vintage"], ccy=main["Currency"], fc=main["fc"],
                              status=main["Status"], commitment=com.reindex(main.index)))
    funds["m0"] = [month_no(d) for d in funds["fc"]]
    funds["obs"] = month_no(dt.date(YEAR, 1, 1)) - funds["m0"]
    funds["programme"] = [d >= dt.date(YEAR - 1, 1, 1) for d in funds["fc"]]
    code_fund = dict(zip(reg["Administrator code"], reg["fund"]))
    c = flows[(flows["side"] == "call") & (flows["vd"] < pd.Timestamp(YEAR, 1, 1))].copy()
    c["fund"] = c["code"].map(code_fund)
    c["age"] = [month_no(d) for d in c["vd"].dt.date] - c["fund"].map(funds["m0"])
    hist = c.groupby(["fund", "age"])["amt"].sum().unstack(fill_value=0.0)
    width = int(funds["obs"].max())
    hist = hist.reindex(index=funds.index, columns=range(width), fill_value=0.0).fillna(0.0)
    funds["paid"] = hist.sum(axis=1)
    n1 = funds["obs"].clip(upper=12)
    first = np.array([hist.loc[f].values[:int(n)].sum() for f, n in zip(funds.index, n1)])
    funds["y1"] = first / funds["commitment"] * 12.0 / n1
    return funds, hist


def split_threshold(funds):
    """the widest gap in the first-year pace of the funds observed nine months or more, among first years under a quarter
    of commitment: its midpoint splits the classes"""
    y = np.sort(funds.loc[(funds["obs"] >= 9) & (funds["y1"] < 0.25), "y1"].values)
    g = np.diff(y)
    k = int(np.argmax(g))
    return (y[k] + y[k + 1]) / 2.0, y[k], y[k + 1]


def schedule(funds, hist, sel, rate=False, equal=False):
    """share of commitment (or of the undrawn balance) called at each month of age, funds observed through that month;
    commitment-weighted, or each fund counted once (equal=True)"""
    f = funds[sel]
    h = hist.loc[f.index].values
    com = f["commitment"].values[:, None]
    seen = np.arange(h.shape[1])[None, :] < f["obs"].values[:, None]
    if rate:
        drawn_before = np.cumsum(h, axis=1) - h
        base = np.where(seen, com - drawn_before, 0.0)
    else:
        base = np.where(seen, com, 0.0)
    num = np.where(seen, h, 0.0)
    if equal:
        num, base = num / com, base / com
    num = num.sum(axis=0)
    den = base.sum(axis=0)
    return np.divide(num, den, out=np.zeros_like(num), where=den > 0)


def project(funds, sched_of, rate, rate_rule=False):
    """expected calendar-2027 calls by fund, in dollars at the year-end rate, capped at the undrawn commitment"""
    out = {}
    for fid, f in funds.iterrows():
        if f["status"] != "Active":
            out[fid] = 0.0
            continue
        s = sched_of(f)
        undrawn = f["commitment"] - f["paid"]
        got = 0.0
        for k in range(12):
            age = int(f["obs"]) + k
            r = s[age] if age < len(s) else 0.0
            amt = (undrawn - got) * min(r, 1.0) if rate_rule else f["commitment"] * r
            got += max(0.0, min(amt, undrawn - got))
        out[fid] = got * (rate if f["ccy"] == "EUR" else 1.0)
    return pd.Series(out)


def ceil_to(x_musd, unit):
    return int(math.ceil(x_musd / unit - 1e-9) * unit)


def the_call(b, rules, funds, hist, rate):
    thr, lo, hi = split_threshold(funds)
    ok("CLASS the first-year pace splits at a gap of 3 points or more, from under 8 to over 11 per cent", hi - lo > 0.03 and
       lo < 0.08 and hi > 0.11, "%.2f%% to %.2f%%" % (100 * lo, 100 * hi))
    funds["line"] = funds["y1"] < thr
    H = ~funds["programme"]
    hl, hs = H & funds["line"], H & ~funds["line"]
    s_line, s_steady = schedule(funds, hist, hl), schedule(funds, hist, hs)
    fc = project(funds, lambda f: s_line if f["line"] else s_steady, rate)
    total = float(fc.sum()) / 1e6
    by_s = {s: float(fc[funds["strategy"] == s].sum()) / 1e6 for s in STRATS}
    res = ceil_to(total, rules["round_up_musd"])
    # the easy routes, on the same books
    s_pool = schedule(funds, hist, H)
    r_pool = schedule(funds, hist, H, rate=True)
    easy_share = project(funds, lambda f: s_pool, rate).sum() / 1e6
    easy_rate = project(funds, lambda f: r_pool, rate, rate_rule=True).sum() / 1e6
    # the out-of-sample record: each vintage of first-year-fee-only funds left out in turn, second-year calls
    recs = {}
    for equal in (False, True):
        rec = []
        for v in sorted(funds.loc[hl & (funds["obs"] >= 24), "vintage"].unique()):
            out = H & (funds["vintage"] != v)
            sp = schedule(funds, hist, out, equal=equal)
            so = schedule(funds, hist, out & funds["line"], equal=equal)
            g = funds[hl & (funds["vintage"] == v) & (funds["obs"] >= 24)]
            actual = hist.loc[g.index].values[:, 12:24].sum()
            c = g["commitment"].sum()
            rec.append((v, actual, sp[12:24].sum() * c, so[12:24].sum() * c))
        recs[equal] = pd.DataFrame(rec, columns=["vintage", "actual", "pooled", "own"])
    rec = recs[False]
    # the first-year split read with and without annualising the programme's younger funds
    n1 = funds["obs"].clip(upper=12)
    raw = np.array([hist.loc[f].values[:int(n)].sum() for f, n in zip(funds.index, n1)]) / funds["commitment"]
    seen9 = funds["obs"] >= 9
    lo = math.ceil(100 * max(funds.loc[seen9 & funds["line"], "y1"].max(), raw[seen9 & funds["line"]].max()))
    hi = math.floor(100 * min(funds.loc[seen9 & ~funds["line"], "y1"].min(), raw[seen9 & ~funds["line"]].min()))
    ratio = min(schedule(funds, hist, hl, equal=e)[12:24].sum() / schedule(funds, hist, hs, equal=e)[12:24].sum()
                for e in (False, True))
    own_within = max(abs((r["own"] - r["actual"]).sum()) / r["actual"].sum() for r in recs.values())
    # the regression of second-year on first-year share (funds observed two years), applied to the programme
    seen24 = H & (funds["obs"] >= 24)
    x = funds.loc[seen24, "y1"].values
    y2 = hist.loc[funds.index[seen24]].values[:, 12:24].sum(axis=1) / funds.loc[seen24, "commitment"].values
    slope, icpt = np.polyfit(x, y2, 1)
    prog = funds[funds["programme"]]
    reg_p = sum(min((icpt + slope * f["y1"]) * f["commitment"], f["commitment"] - f["paid"]) * (rate if f["ccy"] == "EUR" else 1.0)
                for _, f in prog.iterrows()) / 1e6
    pooled_r = project(funds, lambda f: r_pool, rate, rate_rule=True)
    reg_total = reg_p + float(pooled_r[~funds["programme"]].sum()) / 1e6
    # the class misplaced at a round 15 per cent threshold
    l15 = funds["y1"] < 0.15
    s15l, s15o = schedule(funds, hist, H & l15), schedule(funds, hist, H & ~l15)
    mis15 = float(project(funds, lambda f: s15l if f["y1"] < 0.15 else s15o, rate).sum()) / 1e6
    return dict(total=total, by_s=by_s, reserve=res, easy_share=easy_share, easy_rate=easy_rate, rec=rec, recs=recs,
                reg_total=reg_total, mis15=mis15,
                gap=(lo, hi), ratio=ratio, own_within=own_within,
                n_hist=int(H.sum()), n_hist_line=int(hl.sum()), n_prog=int(funds["programme"].sum()),
                n_prog_line=int((funds["programme"] & funds["line"]).sum()),
                y2=dict(line=100 * s_line[12:24].sum(), steady=100 * s_steady[12:24].sum(), pooled=100 * s_pool[12:24].sum()),
                y1_line_max=100 * funds.loc[funds["line"], "y1"].max(), y1_steady_min=100 * funds.loc[~funds["line"] & funds["y1"].notna(), "y1"].min())


# --------------------------------------------------------------------------------------------------------- Ask A
def ask_a(b, flows, rate):
    reg = b.reg.set_index("Administrator code")
    reg["fund"] = reg["Fund ID"].str.replace(r"P$", "", regex=True)
    vehicles = reg.groupby("fund").apply(lambda g: list(g.index), include_groups=False)
    com_fund = reg.groupby("fund")["Commitment"].sum()
    cap = b.cap.copy()
    cap["fund"] = cap["Fund code"].map(reg["fund"])
    cap["vehicle"] = cap["Fund code"].map(reg["Vehicle"])
    # a main vehicle's statement covers the fund when its commitment is the fund's, main and parallel together
    paired = cap[(cap["vehicle"] == "Main") & cap["fund"].map(lambda f: len(vehicles[f]) > 1)]
    combined = (paired["Commitment"] - paired["fund"].map(com_fund)).abs() < 0.01
    ok("ASK A the main vehicles' statements carry the parallel interest (commitment is the fund's)", len(paired) > 0 and
       combined.all(), "%d paired funds" % len(paired))
    rows = cap[cap["vehicle"] == "Main"]
    ye = pd.Timestamp(2026, 12, 31)
    vals = []
    for _, r in rows.iterrows():
        codes = vehicles[r["fund"]]
        nd = as_date(r["NAV date"])
        nav0 = 0.0 if r["Reported NAV"] is None or pd.isna(r["Reported NAV"]) else float(r["Reported NAV"])
        after = flows[flows["code"].isin(codes) & (flows["vd"] <= ye)]
        if nd is not None and r["Reported NAV"] is not None and not pd.isna(r["Reported NAV"]):
            after = after[after["vd"] > pd.Timestamp(nd)]
        con = after.loc[after["side"] == "call", "amt"].sum()
        dis = after.loc[after["side"] == "dist", "amt"].sum()
        ccy = reg.loc[codes[0], "Currency"] if reg.loc[codes[0], "Vehicle"] == "Main" else reg.loc[r["Fund code"], "Currency"]
        usd = (nav0 + con - dis) * (rate if ccy == "EUR" else 1.0)
        vals.append(dict(strategy=reg.loc[r["Fund code"], "Strategy"], vintage=int(reg.loc[r["Fund code"], "Vintage"]),
                         ccy=ccy, usd=usd, label=r["Currency"]))
    v = pd.DataFrame(vals)
    fig = {"strategy:" + s: v.loc[v["strategy"] == s, "usd"].sum() for s in STRATS}
    fig["ccy:EUR"] = v.loc[v["ccy"] == "EUR", "usd"].sum()
    fig["ccy:USD"] = v.loc[v["ccy"] == "USD", "usd"].sum()
    fig["band:2015-2018"] = v.loc[v["vintage"].between(2015, 2018), "usd"].sum()
    fig["band:2019-2022"] = v.loc[v["vintage"].between(2019, 2022), "usd"].sum()
    fig["total"] = v["usd"].sum()
    ok("ASK A every fund's statement row is a main vehicle's and the register's currency is used",
       len(v) == len(set(cap["fund"])), "%d funds, %d summary labels differ from the register" % (len(v), int((v["ccy"] != v["label"]).sum())))
    return {k: round(float(x) / 1e6, 1) for k, x in fig.items()}


# --------------------------------------------------------------------------------------------------------- Ask B
def ask_b(b, rules):
    acct_rows = b.pos[b.pos["account_name"].str.contains("Reserve")]
    acct = acct_rows["account"].iloc[0]
    ca = b.cact[b.cact["account"] == acct].copy()
    ca["q"] = pd.to_numeric(ca["quantity"], errors="coerce").fillna(0.0)
    ca["usd"] = pd.to_numeric(ca["amount_usd"], errors="coerce").fillna(0.0)
    held = ca[ca["asset_id"] != "CASH"].groupby("asset_id")["q"].sum().round(2)
    held = held[held.abs() > 0.005]
    cash_settled = round(ca["usd"].sum(), 2)
    pos = acct_rows[acct_rows["description"] != "ACCOUNT TOTAL"].copy()
    pos["q"] = pos["quantity"].astype(float)
    pos["mv"] = pos["market_value_usd"].astype(float)
    cash_row = pos[pos["asset_id"] == "CASH"]
    ok("ASK B the account's cash is its settled ledger (opening balance and every settled amount)",
       len(cash_row) == 1 and abs(cash_row["mv"].iloc[0] - cash_settled) < 0.01, "%.2f" % cash_settled)
    sec = pos[pos["asset_id"] != "CASH"]
    settled = sec[sec["asset_id"].map(lambda s: s in held.index)]
    pending = sec[~sec.index.isin(settled.index)]
    ok("ASK B every settled holding matches the positions report's quantity",
       all(abs(held[s] - q) < 0.01 for s, q in zip(settled["asset_id"], settled["q"])), "")
    ok("ASK B the positions report's securities not in the settled ledger are four Treasury bills traded 31 December",
       len(pending) == 4 and pending["description"].str.match(r"U\.S\. TREASURY BILL").all() and
       ((b.cact["trade_date"] == "2026-12-31") & b.cact["asset_id"].isin(pending["asset_id"])).sum() == 0, "")
    bills = settled[settled["description"].str.match(r"U\.S\. TREASURY BILL ") &
                    (pd.to_datetime(settled["maturity_date"], errors="coerce") <= pd.Timestamp(YEAR, 12, 31))]
    fund = settled[settled["description"].str.startswith(rules["schedule1"])]
    ok("ASK B the Schedule 1 fund is held, the other money market fund is not on Schedule 1",
       len(fund) == 1 and (sec["asset_type"] == "Money Market Fund").sum() == 2, "")
    quarter = (pd.to_datetime(bills["maturity_date"]).dt.month - 1) // 3
    fig = dict(total=bills["mv"].sum() + fund["mv"].sum() + cash_row["mv"].sum(), bills=bills["mv"].sum())
    for k in range(4):
        fig["q%d" % (k + 1)] = bills.loc[quarter == k, "q"].sum()
    return {k: round(float(x) / 1e6, 1) for k, x in fig.items()}


# ------------------------------------------------------------------------------------------------ the goldens
def golden_values(path, sheet, label_col=0, value_col=1):
    rows = sheet_rows(path, sheet)
    return {str(r[label_col]): r[value_col] for r in rows if r and r[label_col] is not None and len(r) > value_col}


def check_goldens(task, call, a, b_, fig):
    gold = os.path.join(task, "golden")
    book = os.path.join(gold, "call_reserve_2027.xlsx")
    memo = os.path.join(gold, "call_reserve_memo_2027.pdf")
    res = golden_values(book, "Reserve")
    want = {"Call reserve for 2027 (policy 2.2, rounded up to the next $50 million)": call["reserve"],
            "Capital calls expected in 2027, all funds": nearest(call["total"], 25)}
    for s in STRATS:
        want["Capital calls expected in 2027, %s" % s.lower()] = nearest(call["by_s"][s], 25)
    ok("GOLDEN workbook Reserve sheet: the reserve and the five expected-call cells", all(res.get(k) == v for k, v in want.items()),
       str({k[:40]: res.get(k) for k in want}))
    nav = golden_values(book, "NAV")
    names = {"strategy:" + s: s for s in STRATS}
    names.update({"ccy:EUR": "Euro funds", "ccy:USD": "Dollar funds", "band:2015-2018": "Vintages 2015 to 2018",
                  "band:2019-2022": "Vintages 2019 to 2022", "total": "Total"})
    ok("GOLDEN workbook NAV sheet: the nine values", all(abs(nav.get(names[k], -1) - a[k]) < 1e-9 for k in a),
       str({names[k]: nav.get(names[k]) for k in a}))
    ra = golden_values(book, "Reserve assets")
    labs = {"total": "Qualifying assets", "bills": "of which Treasury bills",
            "q1": "Bills maturing January to March 2027, face value", "q2": "Bills maturing April to June 2027, face value",
            "q3": "Bills maturing July to September 2027, face value", "q4": "Bills maturing October to December 2027, face value"}
    ok("GOLDEN workbook Reserve assets sheet: the six values", all(abs(ra.get(labs[k], -1) - b_[k]) < 1e-9 for k in b_), "")
    t = pdf_words(memo)
    ok("GOLDEN memo positive control: the extractor reads the memo", "Call reserve for 2027" in t, "")
    e = {s: nearest(call["by_s"][s], 25) for s in STRATS}
    ok("GOLDEN memo states the reserve and the expected calls", "The call reserve for 2027 is $%d million." % call["reserve"] in t and
       ("call $%d million in 2027: buyout $%d million, growth equity $%d million, venture capital $%d million and private credit $%d million"
        % (nearest(call["total"], 25), e["Buyout"], e["Growth equity"], e["Venture capital"], e["Private credit"])) in t, "")
    ok("GOLDEN memo states the pooled schedule's reserve", "would set the reserve at $%d million" % ceil_to(call["easy_rate"], 50) in t, "")
    ok("GOLDEN memo states the qualifying assets, the bills and the transfer", ("held $%.1f million of qualifying assets" % b_["total"]) in t and
       ("$%.1f million of them Treasury bills" % b_["bills"]) in t and ("shortfall of $%.1f million" % round(call["reserve"] - b_["total"], 1)) in t, "")
    sub = open(os.path.join(task, "submission.md"), encoding="utf-8").read()
    lines = ["Call reserve for 2027: $%d million." % call["reserve"],
             "all funds %d; buyout %d; growth equity %d; venture capital %d; private credit %d." % (
                 nearest(call["total"], 25), e["Buyout"], e["Growth equity"], e["Venture capital"], e["Private credit"])]
    lines += ["   - %s: %.1f" % (names[k], a[k]) for k in a]
    lines += ["   - Qualifying assets: %.1f" % b_["total"], "   - Treasury bills among them: %.1f" % b_["bills"]]
    ok("GOLDEN submission.md block 4 carries every recomputed figure", all(x in sub for x in lines),
       str([x for x in lines if x not in sub][:3]))
    ok("FIGURES figures.json agrees with every recomputed figure", fig["reserve_musd"] == call["reserve"] and
       fig["expected_calls_total_musd"] == nearest(call["total"], 25) and
       abs(fig["expected_calls_total_unrounded_musd"] - round(call["total"], 1)) < 1e-9 and
       all(fig["expected_calls_by_strategy_musd"][s] == e[s] for s in STRATS) and fig["nav_musd"] == a and
       fig["assets_musd"] == b_ and fig["history_line_funds"] == call["n_hist_line"] and
       fig["programme_line_funds"] == call["n_prog_line"] and fig["history_funds"] == call["n_hist"] and
       fig["programme_funds"] == call["n_prog"] and fig["first_year_gap_pct"] == list(call["gap"]) and
       fig["backtest_vintages"] == len(call["rec"]) and fig["backtest_pooled_low_vintages"] == len(call["rec"]) and
       fig["rival_reserves_musd"] == dict(pooled_rates=ceil_to(call["easy_rate"], 50), pooled_shares=ceil_to(call["easy_share"], 50)) and
       abs(fig["transfer_musd"] - round(call["reserve"] - b_["total"], 1)) < 1e-9, "")
    ok("CLAIM block 3: no fund's first year between the stated percentages, read with or without annualising",
       call["gap"][0] < call["gap"][1] and fig["first_year_gap_pct"] == list(call["gap"]), str(call["gap"]))
    ok("CLAIM blocks 1 and 3: the fee-only funds' second-year share more than twice the others', either weighting",
       call["ratio"] > 2.0, "%.2f" % call["ratio"])
    ok("CLAIM block 3: the pooled schedule low in every left-out vintage and the own schedule within the stated per cent, "
       "either weighting", all((r["pooled"] < r["actual"]).all() for r in call["recs"].values()) and
       100 * call["own_within"] <= fig["backtest_own_within_pct"], "own %.2f%%" % (100 * call["own_within"]))
    ok("CLAIM block 1: the rival reserves as stated", ("Not $%d million, the reserve from Takahashi-Alexander rates on the "
       "undrawn balance pooled over every earlier fund ($%d million from shares" % (ceil_to(call["easy_rate"], 50),
                                                                                  ceil_to(call["easy_share"], 50))) in sub, "")


def main(target):
    task = os.path.dirname(os.path.abspath(target))
    b = Bundle(target)
    read_back(b)
    rules = policy_rules(b)
    ye = b.fx[b.fx["date"] <= pd.Timestamp(2026, 12, 31)].sort_values("date").iloc[-1]
    rate = float(ye["usd_per_eur"])
    ok("FX the last business day of 2026 and its rate", ye["date"].date() == dt.date(2026, 12, 31) and abs(rate - 1.1326) < 1e-9,
       "%s %.4f" % (ye["date"].date(), rate))
    flows, cut = call_frames(b)
    funds, hist = fund_table(b, flows)
    call = the_call(b, rules, funds, hist, rate)
    ok("CALL the reserve is $450 million", call["reserve"] == 450, "%.2f expected" % call["total"])
    ok("CALL expected calls to the nearest 25 are 425, a quarter cell from the rounding edges", nearest(call["total"], 25) == 425 and
       400 + 12.5 <= call["total"] <= 450 - 12.5, "%.2f" % call["total"])
    ok("CALL by strategy 175, 100, 75, 75", [nearest(call["by_s"][s], 25) for s in STRATS] == [175, 100, 75, 75],
       str({s: round(call["by_s"][s], 1) for s in STRATS}))
    ok("CALL the classes: 36 of 172 earlier funds, 12 of 14 programme funds", (call["n_hist_line"], call["n_hist"],
       call["n_prog_line"], call["n_prog"]) == (36, 172, 12, 14), "")
    ok("RIVAL the pooled share-of-commitment schedule files $300 million", ceil_to(call["easy_share"], 50) == 300, "%.1f" % call["easy_share"])
    ok("RIVAL the pooled rate-on-undrawn schedule files $350 million", ceil_to(call["easy_rate"], 50) == 350, "%.1f" % call["easy_rate"])
    rec = call["rec"]
    ok("BACKTEST the pooled schedule puts every left-out vintage's second year low", len(rec) == 12 and (rec["pooled"] < rec["actual"]).all(),
       "%d vintages" % len(rec))
    err_p = (rec["pooled"] - rec["actual"]).sum() / 1e6
    err_o = (rec["own"] - rec["actual"]).sum() / 1e6
    ok("BACKTEST the own-class schedule misses by under a tenth of the pooled schedule's miss", abs(err_o) < 0.1 * abs(err_p),
       "pooled %.1f, own %.1f of %.1f" % (err_p, err_o, rec["actual"].sum() / 1e6))
    a = ask_a(b, flows, rate)
    ok("ROUTE the regression of second-year on first-year share files a reserve a bin below", ceil_to(call["reg_total"], 50) == 400,
       "%.1f" % call["reg_total"])
    ok("ROUTE a 15 per cent class threshold files a reserve a bin below", ceil_to(call["mis15"], 50) == 400, "%.1f" % call["mis15"])
    ok("ASK A nine figures", a == {"strategy:Buyout": 617.8, "strategy:Growth equity": 242.2, "strategy:Venture capital": 508.1,
                                   "strategy:Private credit": 43.1, "ccy:EUR": 185.7, "ccy:USD": 1225.6,
                                   "band:2015-2018": 326.4, "band:2019-2022": 960.2, "total": 1411.2}, str(a))
    bb = ask_b(b, rules)
    ok("ASK B six figures", bb == {"total": 161.0, "bills": 88.6, "q1": 32.0, "q2": 15.0, "q3": 25.0, "q4": 18.0}, str(bb))
    fig = json.load(open(os.path.join(task, "generator", "figures.json")))
    check_goldens(task, call, a, bb, fig)
    bad = [r for r in OUT if not r[1]]
    for lab, good, det in OUT:
        print("%s  %-100s %s" % ("PASS" if good else "FAIL", lab, det))
    print("verify: %d assertions, %d failed" % (len(OUT), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
