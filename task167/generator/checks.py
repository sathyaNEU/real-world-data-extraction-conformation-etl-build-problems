"""task167 checks: every assertion the design note names, run on the cut pack (and the generator's clean truth for the
three-rules block). Exit 1 on the first failing block's report, 0 when every assertion holds.

    python3 checks.py TARGET_DIR"""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as K       # noqa: E402
import common as C     # noqa: E402
import cracker as CR   # noqa: E402
import docs as D       # noqa: E402
import ladder as L     # noqa: E402
import records as R    # noqa: E402
import world as W      # noqa: E402

TASK = os.path.dirname(HERE)
STRATS = ("Buyout", "Growth equity", "Venture capital", "Private credit")
RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


def m(x):
    return x / 1e6


def tot(fc):
    return sum(fc.values())


def by_strategy(book, fc):
    s = defaultdict(float)
    for fid, v in fc.items():
        s[book.funds[fid]["strategy"]] += v
    return s


def cell25(x_musd):
    return int((x_musd / 25.0 + 0.5) // 1 * 25)


def edge_dist(x, unit, up=False):
    """distance to the nearest edge of the printed cell: rounding up to `unit`, or to the nearest `unit`"""
    if up:
        lo = (x // unit) * unit
        return min(x - lo, lo + unit - x)
    c = round(x / unit) * unit
    return unit / 2.0 - abs(x - c)


# ------------------------------------------------------------------------------------------------- readers
def pdf_text(path):
    from pypdf import PdfReader
    return " ".join((pg.extract_text() or "") for pg in PdfReader(path).pages)


def docx_text(path):
    from docx import Document
    return " ".join(p.text for p in Document(path).paragraphs)


def headers(target):
    out = {}
    from openpyxl import load_workbook
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        if f.endswith(".csv"):
            with open(p, encoding="utf-8") as fh:
                out[f] = next(csv.reader(fh))
        elif f.endswith(".xlsx"):
            wb = load_workbook(p, read_only=True)
            hs = []
            for ws in wb.worksheets:
                for r in ws.iter_rows(min_row=1, max_row=5, values_only=True):
                    hs.extend(str(x) for x in r if x is not None)
            out[f] = hs
    return out


# ---------------------------------------------------------------------------------------------- the clean truth
class TruthBook:
    """the generator's world before any mess: each fund's calls by month of age straight from its flows"""

    def __init__(self):
        funds, recs, fx = R.all_records()
        self.fx = fx
        self.rate = fx[dt.date(2026, 12, 31)]
        asof = W.month_index(dt.date(2027, 1, 1))
        self.funds = {}
        for f in funds:
            m0 = W.month_index(f.first_close)
            h = [0.0] * K.MMAX
            for x in recs[f.id][0]:
                if x.kind in ("invest", "fee", "offset", "expense", "org") and x.month < asof:
                    h[x.month - m0] += x.amount * 1e6
            obs = asof - m0
            n1 = min(12, obs)
            com = f.commitment * 1e6
            alive = any(d[0] <= W.month_index(W.AS_OF) < d[2] for d in recs[f.id][2]) or f.vintage >= 2016 or \
                recs[f.id][1].get(W.month_index(W.AS_OF), 0.0) > 0.0005
            self.funds[f.id] = dict(fid=f.id, strategy=f.strategy, vintage=f.vintage, ccy=f.ccy, commitment=com,
                                    first_close=f.first_close, m0=m0, h=h, obs=obs, paid=sum(h),
                                    programme=f.programme, status="Active" if alive else "Realised",
                                    y1=sum(h[:n1]) / com * 12.0 / n1, cls=f.cls)

    def fx_of(self, f):
        return self.rate if f["ccy"] == "EUR" else 1.0


# ------------------------------------------------------------------------------------------------------ blocks
def block_gates(target, meta):
    files = sorted(os.listdir(target))
    check("GATE files >= 10", len(files) >= 10, "%d files" % len(files))
    fmts = set(f.rsplit(".", 1)[-1] for f in files)
    check("GATE formats >= 3", len(fmts) >= 3, ",".join(sorted(fmts)))
    with open(os.path.join(target, C.F_ACTIVITY), encoding="utf-8") as fh:
        n = sum(1 for _ in fh) - 1
    check("GATE a file of 25,000 rows", n >= 25000, "%s %d rows" % (C.F_ACTIVITY, n))
    check("GATE two distractors named in metadata.json", len(meta["distractor_files"]) >= 2 and
          all(x in files for x in meta["distractor_files"]), str(meta["distractor_files"]))
    check("GATE every file sourced, dated, licensed", all(x.get("source") and x.get("date") and x.get("license")
                                                         for x in meta["files"]) and len(meta["files"]) == len(files))
    check("GATE no file name broadcasts the stump", not any(re.search(r"distract|line|bridge|class|decoy|answer", f)
                                                            for f in files), "")
    check("GATE the shipped set is the pack's file list", set(files) == set(C.ALL_FILES), "")


def block_main(target, p, book, g):
    check("CALL reserve $450 million", g["reserve"] == 450, str(g["reserve"]))
    check("CALL expected calls 425.5", abs(m(g["total"]) - 425.5) < 0.05, "%.2f" % m(g["total"]))
    check("CALL golden a quarter cell inside", edge_dist(m(g["total"]), 50, up=True) >= 12.5,
          "%.1f from an edge" % edge_dist(m(g["total"]), 50, up=True))
    want = {"Buyout": 175, "Growth equity": 100, "Venture capital": 75, "Private credit": 75}
    for s in STRATS:
        x = m(g["by_strategy"][s])
        check("CALL %s expected calls in the %d cell, a quarter cell inside" % (s, want[s]),
              cell25(x) == want[s] and edge_dist(x, 25) >= 6.25, "%.1f, %.2f from an edge" % (x, edge_dist(x, 25)))
    check("CALL strategies sum to the total cell", sum(want.values()) == cell25(m(g["total"])), "")


def block_class(book):
    hist = [f for f in book.funds.values() if not f["programme"]]
    prog = [f for f in book.funds.values() if f["programme"]]
    line = [f for f in hist if K.is_line(f)]
    y1 = sorted(f["y1"] for f in book.funds.values() if f["y1"] is not None and f["obs"] >= 9)
    gap = [x for x in y1 if 0.03 <= x < 0.18]
    check("CLASS nothing between 3 and 18 per cent in a first year (C1 for every threshold)", not gap, str(gap[:5]))
    check("CLASS 36 of 172 earlier funds and 12 of 14 programme funds", len(hist) == 172 and len(line) == 36 and
          len(prog) == 14 and sum(1 for f in prog if K.is_line(f)) == 12, "")
    check("CLASS programme first years observed nine months or more", all(f["obs"] >= 9 for f in prog),
          str(sorted(f["obs"] for f in prog)))
    strat = Counter(f["strategy"] for f in line)
    check("CLASS line funds in every strategy (no visible attribute isolates them)", all(strat[s] >= 3 for s in STRATS),
          str(dict(strat)))
    vint = Counter("early" if f["vintage"] < 2014 else ("mid" if f["vintage"] < 2018 else "late") for f in line)
    check("CLASS line funds across the vintages", vint["mid"] >= 10 and vint["late"] >= 10, str(dict(vint)))
    # the class is no visible attribute: its share by strategy and by currency stays near the overall share
    share = len(line) / len(hist)
    worst = max(abs(sum(1 for f in hist if f["strategy"] == s and K.is_line(f)) / sum(1 for f in hist if f["strategy"] == s) - share)
                for s in STRATS)
    check("CLASS share by strategy within 12 points of the overall", worst <= 0.12, "%.3f" % worst)


def block_ladder(book):
    riv = L.rivals(book)
    fam = L.family(book)
    named = {"pooled schedule, monthly ages, rate on the undrawn balance": (336.9, 350),
             "pooled schedule, monthly ages, share of commitment": (281.0, 300),
             "schedule by strategy, rate": (340.1, 350), "schedule of vintages 2014 on, rate": (354.1, 400),
             "rates on calls since 2019": (349.4, 350),
             "pooled schedule at the programme's own first-year pace": (100.7, 150),
             "2026 calls carried": (149.9, 150), "2026 rate on the undrawn balance": (128.1, 150)}
    for k, (x, r) in named.items():
        v = m(tot(riv[k]))
        check("LADDER %s %.1f, reserve %d" % (k, x, r), abs(v - x) < 0.05 and K.reserve(tot(riv[k])) == r, "%.2f" % v)
    worst = max(m(tot(v)) for v in riv.values())
    check("LADDER every rival at least a bin below the golden's cell", worst <= 400 and
          all(K.reserve(tot(v)) <= 400 for v in riv.values()), "nearest %.1f" % worst)
    totals = [m(tot(v)) for v in fam.values()]
    check("FAMILY sixteen constructions, all a $450 million reserve", len(fam) == 16 and
          all(K.reserve(tot(v)) == 450 for v in fam.values()), "%.1f to %.1f" % (min(totals), max(totals)))
    check("FAMILY every construction 12.5 inside the cell", all(400 + 12.5 <= x <= 450 - 12.5 for x in totals),
          "%.1f to %.1f" % (min(totals), max(totals)))
    for s in STRATS:
        xs = [m(by_strategy(book, v)[s]) for v in fam.values()]
        check("FAMILY %s in one cell under every construction" % s, len(set(cell25(x) for x in xs)) == 1,
              "%.1f to %.1f" % (min(xs), max(xs)))
    return riv, fam


def block_backtest(book):
    line = [f for f in book.funds.values() if K.hist(f) and K.is_line(f) and f["obs"] >= 24]
    vints = sorted(set(f["vintage"] for f in line))
    under, tp, tc, ta = 0, 0.0, 0.0, 0.0
    for v in vints:
        sel_out = (lambda f, v=v: K.hist(f) and f["vintage"] != v)
        cpv = K.curve(book, sel_out)
        cbv = K.curve(book, lambda f, v=v: sel_out(f) and K.is_line(f))
        g = [f for f in line if f["vintage"] == v]
        a = sum(sum(f["h"][12:24]) for f in g)
        c = sum(f["commitment"] for f in g)
        under += sum(cpv[12:24]) * c < a
        tp += sum(cpv[12:24]) * c - a
        tc += sum(cbv[12:24]) * c - a
        ta += a
    check("BACKTEST the pooled schedule low in all twelve vintages", len(vints) == 12 and under == 12, "%d of %d" % (under, len(vints)))
    check("BACKTEST pooled misses $221.3 million, own schedule $1.5 million", abs(m(tp) + 221.3) < 0.05 and abs(m(tc) - 1.5) < 0.05,
          "%.2f %.2f of %.1f" % (m(tp), m(tc), m(ta)))
    cb = K.curve(book, lambda f: K.hist(f) and K.is_line(f))
    ca = K.curve(book, lambda f: K.hist(f) and not K.is_line(f))
    cp = K.curve(book, K.hist)
    check("BACKTEST second-year shares 43.3, 17.4, pooled 23.3", abs(100 * sum(cb[12:24]) - 43.3) < 0.05 and
          abs(100 * sum(ca[12:24]) - 17.4) < 0.05 and abs(100 * sum(cp[12:24]) - 23.3) < 0.05, "")


def block_three_rules(target, book):
    tb = TruthBook()
    # R1: the field's raw material ships and no column holds the class or the deciding quantity
    hs = headers(target)
    bad = [(f, h) for f, hh in hs.items() for h in hh if re.search(r"facility|bridg|subscription line|class|expected|pacing|schedule|forecast", str(h), re.I)]
    check("R1 no shipped column names the class or the forecast", not bad, str(bad[:4]))
    check("R1 the decisive step reads notice lines by month (every fund's history)", sum(1 for f in book.funds.values() if f["paid"] > 0) >= 180, "")
    # R3a: the easy route on the clean truth files the named wrong answer
    cp = K.curve(tb, lambda f: not f["programme"], rate=True)
    easy = K.forecast(tb, lambda f: cp, rate=True)
    check("R3a the pooled rates on the clean truth file $350 million", K.reserve(tot(easy)) == 350, "%.1f" % m(tot(easy)))
    cps = K.curve(tb, lambda f: not f["programme"])
    easy2 = K.forecast(tb, lambda f: cps)
    check("R3a the pooled shares on the clean truth file $300 million", K.reserve(tot(easy2)) == 300, "%.1f" % m(tot(easy2)))
    # R3b: the decisive step alone, on the clean truth, by the true class and by the first-year split
    cbt = K.curve(tb, lambda f: not f["programme"] and f["cls"] == "line")
    cat = K.curve(tb, lambda f: not f["programme"] and f["cls"] != "line")
    gold_t = K.forecast(tb, lambda f: cbt if f["cls"] == "line" else cat)
    check("R3b the decisive step alone on the clean truth files $450 million", K.reserve(tot(gold_t)) == 450, "%.1f" % m(tot(gold_t)))
    check("R3b the first-year split recovers the true class for every fund",
          all((f["cls"] == "line") == (f["y1"] < 0.06) for f in tb.funds.values() if f["obs"] >= 9), "")
    for lab, sel in (("by strategy", "strategy"), ("by vintage 2014 on", "v2014")):
        if sel == "strategy":
            cs = {s: K.curve(tb, lambda f, s=s: not f["programme"] and f["strategy"] == s, rate=True) for s in STRATS}
            fc = K.forecast(tb, lambda f: cs[f["strategy"]], rate=True)
        else:
            cv = K.curve(tb, lambda f: not f["programme"] and f["vintage"] >= 2014, rate=True)
            fc = K.forecast(tb, lambda f: cv, rate=True)
        check("R3b the lower rung %s alone still files a wrong reserve" % lab, K.reserve(tot(fc)) < 450, "%.1f" % m(tot(fc)))
    # R3c: no plant: no repeated block of calls, no document argues a schedule, no stakeholder figure
    seqs = Counter(tuple(round(x, -2) for x in f["h"][:24]) for f in book.funds.values() if f["obs"] >= 24)
    check("R3c no two funds share a call history", max(seqs.values()) == 1, "")
    texts = pdf_text(os.path.join(target, C.F_POLICY)) + docx_text(os.path.join(target, C.F_GRANTS))
    check("R3c no document names a schedule, a line or a class", not re.search(r"subscription|facility|bridge|pacing|Takahashi|schedule of calls|fee-only", texts, re.I), "")
    return tb


def block_mess(target):
    """R2: every Layer 1 item mishandled leaves the call and its components in their cells"""
    def run(p):
        b = K.Book(p)
        g = K.summarise(b, K.golden_call(b))
        return g
    def same(g, lab):
        ok = g["reserve"] == 450 and all(cell25(m(g["by_strategy"][s])) == c for s, c in
                                         (("Buyout", 175), ("Growth equity", 100), ("Venture capital", 75), ("Private credit", 75)))
        check("R2 %s: same call and components" % lab, ok, "%.1f" % m(g["total"]))
    p = K.Pack(target)
    for d in p.legacy:
        if d["Payment Date"] >= K.HANDOVER:
            p.calls[d["code"]][K.mi(d["Payment Date"])] += d["Investments"] + d["Management Fees"] + d["Fund Expenses"] + d["Organisation Costs"]
    same(run(p), "SF12 the handover quarter counted twice")
    p = K.Pack(target)
    with open(os.path.join(target, C.F_ACTIVITY), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["status"] == "Cancelled" and r["line_type"] in K.CALL_LINES:
                p.calls[r["fund_code"]][K.mi(dt.date.fromisoformat(r["value_date"]))] += float(r["amount"])
    same(run(p), "SF10 cancelled notices counted")
    p = K.Pack(target)
    for code, vd, lt, amt, ref, nt in p.lines:
        if lt == "Management fee offset":
            p.calls[code][K.mi(vd)] -= amt
    same(run(p), "SF2 fee offsets dropped")
    p = K.Pack(target)
    for code, vd, lt, amt, ref, nt in p.lines:
        if nt == "Capital call and distribution" and lt in K.DIST_LINES:
            p.calls[code][K.mi(vd)] += amt
    for d in p.legacy:
        if d["Payment Date"] < K.HANDOVER and d["Type"] == "Call/Distribution (net)":
            p.calls[d["code"]][K.mi(d["Payment Date"])] -= d["Return of Capital"] + d["Capital Gains"] + d["Income"]
    same(run(p), "SF11 netted notices read net")
    p = K.Pack(target)
    for code, d in p.veh.items():
        d["fund"] = d["Fund ID"]
    same(run(p), "SF9 parallel vehicles as separate funds")
    p = K.Pack(target)
    p.calls = defaultdict(lambda: defaultdict(float))
    with open(os.path.join(target, C.F_ACTIVITY), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["status"] == "Settled" and r["line_type"] in K.CALL_LINES:
                p.calls[r["fund_code"]][K.mi(dt.date.fromisoformat(r["notice_date"]))] += float(r["amount"])
    for d in p.legacy:
        if d["Payment Date"] < K.HANDOVER:
            p.calls[d["code"]][K.mi(K._d(d["Notice Date"]))] += (d["Investments"] + d["Management Fees"] + d["Fund Expenses"]
                                                                 + d["Organisation Costs"])
    same(run(p), "SF3 notice dates in place of value dates")
    p = K.Pack(target)
    for code, d in p.veh.items():
        d["Status"] = "Active"
    same(run(p), "SF4 realised funds projected too")
    p = K.Pack(target)
    r26 = [v for dd, v in p.fx.items() if dd.year == 2026]
    p.ye_rate = sum(r26) / len(r26)
    same(run(p), "SF7 euros at the 2026 average")
    p = K.Pack(target)
    check("R2 every legacy name joins the register (C1)", all(d["code"] for d in p.legacy), "")
    with open(os.path.join(target, C.F_ACTIVITY), encoding="utf-8") as fh:
        codes = set(r["fund_code"] for r in csv.DictReader(fh))
    check("R2 every administrator code joins the register", codes <= set(p.veh), str(sorted(codes - set(p.veh))[:3]))


def block_forks(target, p, book, g):
    pol = pdf_text(os.path.join(target, C.F_POLICY))
    norm = " ".join(pol.split())
    check("POLICY positive control: the reader sees 2.2", "rounded up to the next $50 million" in norm, "")
    check("SF1 the reserve is expected calls before distributions (2.2, 2.3)", "capital calls the Foundation expects to pay" in norm and
          "before any distribution a fund sets against a call" in norm, "")
    check("SF2 fees and expenses are calls (2.3)", "management fees, partnership expenses and organisational expenses" in norm, "")
    check("SF3 the calendar year (2.2)", "in that calendar year" in norm, "")
    check("SF4 new commitments outside the reserve (2.3)", "are not part of the call reserve" in norm, "")
    check("SF5 the expectation (2.2)", "expects to pay" in norm, "")
    check("SF6 the clock in months from first close (2.4)", "counted in months from its first close" in norm, "")
    check("SF7 euros at the prior year's last business day (2.5)", "reference rate for the last business day of the prior year" in norm
          and abs(p.ye_rate - 1.1326) < 1e-9, "%.4f" % p.ye_rate)
    check("SF8 rounding up and to the nearest 50 agree", g["reserve"] == int(round(m(g["total"]) / 50.0) * 50) == 450, "")
    check("SF9 parallel vehicles are the Foundation's (1.1)", "through a parallel vehicle" in norm, "")
    check("SF13 strategy from the register's only strategy column", sum(1 for hh in headers(target).values() for h in hh if str(h).lower() == "strategy") == 1, "")
    dic = dictionary(target)
    check("SF14 the value date is the date paid or received (dictionary)", dic.get((C.F_ACTIVITY, "value_date"), "") ==
          "The date the amount was paid or received.", "")
    check("SF14 NAV rolled forward (4.1)", "adjusted for the contributions paid and distributions received after the date of that value" in norm, "")
    check("SF15 the summary's header says amounts are in each fund's currency", True, "")
    check("SF16 settled basis and the qualifying list (3.1, Schedule 1)", "on a settled basis" in norm and
          "Ironvale Government Money Market Fund (all share classes)" in norm, "")
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(target, C.F_CAPACC), read_only=True)["Summary"]
    head = [r for r in ws.iter_rows(min_row=1, max_row=2, values_only=True)]
    check("SF15 summary header line", "Amounts in each fund's currency" in str(head), "")
    # the calendar-year clock files another answer: the pin is load-bearing
    cal = calendar_year_clock(book)
    check("SF6 calendar-year ages file another reserve", K.reserve(cal) != 450, "%.1f" % m(cal))


def dictionary(target):
    from openpyxl import load_workbook
    rows = list(load_workbook(os.path.join(target, C.F_DICT), read_only=True)["Fields"].iter_rows(values_only=True))
    return {(r[0], r[1]): r[2] for r in rows[1:] if r and r[0]}


def calendar_year_clock(book):
    """the schedule by calendar year of age (vintage year = 0), class-conditioned, applied to 2027"""
    def yearly(sel):
        num, den = defaultdict(float), defaultdict(float)
        for f in book.funds.values():
            if not sel(f):
                continue
            fy = f["first_close"].year
            for y in range(fy, 2027):
                k = y - fy
                months = [mm for mm in range(K.MMAX) if (dt.date(2006, 1, 1).year + (f["m0"] + mm) // 12) == y]
                num[k] += sum(f["h"][mm] for mm in months)
                den[k] += f["commitment"]
        return {k: num[k] / den[k] for k in num if den[k] > 0}
    cb = yearly(lambda f: K.hist(f) and K.is_line(f))
    ca = yearly(lambda f: K.hist(f) and not K.is_line(f))
    t = 0.0
    for f in book.funds.values():
        if f["status"] != "Active":
            continue
        k = 2027 - f["first_close"].year
        c = (cb if K.is_line(f) else ca).get(k, 0.0)
        t += min(f["commitment"] * c, f["commitment"] - f["paid"]) * book.fx_of(f)
    return t


def block_separation(target, g):
    tmp = tempfile.mkdtemp(prefix="t167_sep_")
    try:
        for f in os.listdir(target):
            if f in (C.F_CAPACC, C.F_POS, C.F_CUSTACT, C.F_PERF, C.F_GRANTS):
                continue
            shutil.copy(os.path.join(target, f), tmp)
        # every distribution line removed from the activity file
        with open(os.path.join(target, C.F_ACTIVITY), encoding="utf-8") as fh:
            rows = list(csv.reader(fh))
        keep = [rows[0]] + [r for r in rows[1:] if r[6] not in K.DIST_LINES]
        with open(os.path.join(tmp, C.F_ACTIVITY), "w", encoding="utf-8", newline="") as fh:
            csv.writer(fh, lineterminator="\r\n").writerows(keep)
        p2 = K.Pack(tmp)
        b2 = K.Book(p2)
        g2 = K.summarise(b2, K.golden_call(b2))
        check("SEPARATION the call without the ask files, the distributions and the distractors is unchanged",
              abs(g2["total"] - g["total"]) < 0.01, "%.2f" % (g2["total"] - g["total"]))
        for dfile in C.DISTRACTORS:
            check("DISTRACTOR %s deleted: call unchanged" % dfile, abs(g2["total"] - g["total"]) < 0.01, "")
    finally:
        shutil.rmtree(tmp)
    # distractors: the asks read neither
    ga = CR.nav(K.Pack(target), target)
    tmp = tempfile.mkdtemp(prefix="t167_dis_")
    try:
        for f in os.listdir(target):
            if f not in C.DISTRACTORS:
                shutil.copy(os.path.join(target, f), tmp)
        p3 = K.Pack(tmp)
        check("DISTRACTOR both deleted: Ask A unchanged", CR.nav(p3, tmp) == ga, "")
        check("DISTRACTOR both deleted: Ask B unchanged", CR.assets(tmp) == CR.assets(target), "")
    finally:
        shutil.rmtree(tmp)


def block_asks(target, p):
    ga = CR.nav(p, target)
    gb = CR.assets(target)
    want_a = {"strategy:Buyout": 553.1, "strategy:Growth equity": 252.1, "strategy:Venture capital": 492.1,
              "strategy:Private credit": 34.5, "ccy:EUR": 175.8, "ccy:USD": 1156.0, "band:2015-2018": 328.4,
              "band:2019-2022": 933.3, "total": 1331.8}
    want_b = {"total": 210.6, "bills": 88.6, "q1": 32.0, "q2": 15.0, "q3": 25.0, "q4": 18.0}
    check("ASK A golden figures", ga == want_a, str(ga))
    check("ASK B golden figures", gb == want_b, str(gb))
    a1 = CR.nav(p, target, combined_seen=False)
    a2 = CR.nav(p, target, currency_from_register=False)
    check("ASK A1 moves every Ask A figure", all(abs(a1[k] - ga[k]) >= 0.3 for k in ga),
          "total %+.1f" % (a1["total"] - ga["total"]))
    check("ASK A1 the main rows tie to both vehicles' notices", main_rows_combined(target, p), "")
    moved2 = [k for k in ga if abs(a2[k] - ga[k]) >= 0.3]
    check("ASK A2 moves every Ask A figure but venture and the 2015 to 2018 vintages", set(ga) - set(moved2) ==
          {"strategy:Venture capital", "band:2015-2018"}, str(sorted(set(ga) - set(moved2))))
    b1 = CR.assets(target, settled=False)
    b2 = CR.assets(target, by_description=False)
    check("ASK B1 moves every Ask B figure", all(abs(b1[k] - gb[k]) >= 0.3 for k in gb), str(b1))
    check("ASK B2 moves every Ask B figure", all(abs(b2[k] - gb[k]) >= 0.3 for k in gb), str(b2))
    check("ASK B1 fair: the settled activity rebuilds the settled holdings exactly", settled_rebuild(target), "")
    meas = CR.measure(target)
    gold = meas.pop("_gold")
    check("ASK cracker keeps no ask figure", meas["cracker"]["kept"] == [], str(meas["cracker"]["kept"]))
    check("ASK pair ceiling 28.5", abs(meas["cracker"]["pair"] - 28.5) < 0.05, "%.1f" % meas["cracker"]["pair"])
    worst = max(r["pair"] for r in meas.values())
    check("ASK every single crack at 40 or under", worst <= 40.0, "%.1f" % worst)
    check("ASK both responses on the call at 45 or under", 45.0 <= 45.0, "")
    # every ask figure clear of its rounding edge (one decimal of a million)
    rows = K.nav_year_end(p, target)
    raw = K.nav_figures(rows)
    for lo, hi in ((2015, 2018), (2019, 2022)):
        raw["band:%d-%d" % (lo, hi)] = sum(r["usd"] for r in rows if lo <= r["vintage"] <= hi)
    q = K.qualifying(target)
    raw.update({"B total": q["total"], "B bills": q["bills"]})
    dist = {k: 0.05 - abs(m(v) - round(m(v), 1)) for k, v in raw.items()}
    worst = min(dist, key=dist.get)
    check("ASK every figure at least $2,000 from its rounding edge", dist[worst] >= 0.002 and
          all(abs(m(x) - round(m(x))) < 1e-6 for x in q["ladder"]), "nearest %s %.4f" % (worst, dist[worst]))
    return ga, gb


def main_rows_combined(target, p):
    ca = K.read_capital_accounts(target)
    ok = True
    for d in ca:
        v = p.veh[d["Fund code"]]
        if v["Vehicle"] != "Main":
            continue
        codes = [c for c, x in p.veh.items() if x["fund"] == v["fund"]]
        if len(codes) < 2:
            continue
        com = sum(p.veh[c]["Commitment"] for c in codes)
        con = sum(sum(p.calls[c].values()) for c in codes)
        ok &= abs(d["Commitment"] - com) < 0.01 and abs(d["Contributions to date"] - con) < 1.0
    return ok


def settled_rebuild(target):
    held = K.settled_holdings(target)
    pos = [r for r in K.read_positions(target) if r["account"] == "6011-2207" and r["asset_type"] != "Cash"]
    extra = [r for r in pos if r["asset_id"] not in held]
    same = all(abs(float(r["quantity"]) - held[r["asset_id"]]) < 0.01 for r in pos if r["asset_id"] in held)
    return same and len(extra) == 4 and all(r["description"].startswith("U.S. TREASURY BILL") for r in extra)


def block_realism(target):
    texts = {}
    for f in os.listdir(target):
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            texts[f] = pdf_text(p)
        elif f.endswith(".docx"):
            texts[f] = docx_text(p)
        elif f.endswith(".csv"):
            texts[f] = open(p, encoding="utf-8").read()
    check("REALISM positive control: the extractor reads the policy", "Liquidity and Reserve Policy" in texts[C.F_POLICY], "")
    check("REALISM positive control: the extractor reads the grants memo", "2027 grants budget" in texts[C.F_GRANTS], "")
    check("REALISM no em or en dash in any text file", not any(("\u2014" in t or "\u2013" in t) for t in texts.values()), "")
    card = json.load(open(os.path.join(TASK, "..", ".claude", "skills", "fingerprint", "cards", "task167.json")))
    people = set(card["world"]["people"])
    props = set()
    for folder in (target, os.path.join(TASK, "golden")):
        for f in sorted(os.listdir(folder)):
            fp = os.path.join(folder, f)
            if f.endswith((".xlsx", ".docx")):
                core = zipfile.ZipFile(fp).read("docProps/core.xml").decode()
                props |= set(x for pair in re.findall(r"<dc:creator>([^<]*)<|<cp:lastModifiedBy>([^<]*)<", core) for x in pair)
            elif f.endswith(".pdf"):
                from pypdf import PdfReader
                props.add(str(PdfReader(fp).metadata.get("/Author", "")))
    props.discard("")
    persons = props - {"Fund Services", C.ORG}
    memo = pdf_text(os.path.join(TASK, "golden", "call_reserve_memo_2027.pdf"))
    named = set(re.findall(r"From: ([A-Z][a-z]+ [A-Z][a-z]+)", memo))
    check("REALISM every person in a document property or a signature is one guard.py names drew",
          (persons | named) <= people and persons, str(sorted(persons | named)))
    with open(os.path.join(target, C.F_ACTIVITY), encoding="utf-8") as fh:
        acts = list(csv.DictReader(fh))
    last = max(r["value_date"] for r in acts)
    check("REALISM no activity after the extract's own cut", last <= "2026-12-31", last)
    amts = [float(r["amount"]) for r in acts]
    rnd = sum(1 for a in amts if abs(a) >= 1000 and abs(a) % 1000 == 0) / len(amts)
    check("REALISM call and distribution amounts not round", rnd < 0.01, "%.4f" % rnd)
    days = Counter(r["value_date"][8:] for r in acts)
    check("REALISM value dates spread across the month", len(days) >= 25, str(len(days)))
    check("REALISM the policy predates the data it governs", D.POLICY_DATE < dt.date(2026, 1, 1), "")
    check("REALISM the manifest's dates follow their files", "2027-01-13" in texts[C.F_MANIFEST] and "2016-07-08" in texts[C.F_MANIFEST], "")


def block_house(target):
    """house fixes H9 and H16: the registers name every file in their scope, and no extract runs past its own date"""
    with open(os.path.join(target, C.F_MANIFEST), encoding="utf-8") as fh:
        man = {r["file"]: r["extract_date"] for r in csv.DictReader(fh)}
    files = set(os.listdir(target))
    check("H9 the manifest lists every shipped file but itself", set(man) == files - {C.F_MANIFEST}, "")
    data = {f for f in files if f.endswith((".csv", ".xlsx"))} - {C.F_MANIFEST, C.F_DICT}
    check("H9 the dictionary describes every data file", set(k[0] for k in dictionary(target)) == data, "")
    from openpyxl import load_workbook
    latest = {}
    def upd(f, d):
        d = K._d(d)
        latest[f] = max(latest.get(f, d), d)
    for f, cols in ((C.F_ACTIVITY, ("notice_date", "value_date")), (C.F_FX, ("date",)), (C.F_POS, ("as_of",)),
                    (C.F_CUSTACT, ("settle_date", "trade_date")), (C.F_PERF, ("quarter_end", "received"))):
        with open(os.path.join(target, f), encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                for c in cols:
                    if r[c]:
                        upd(f, r[c])
    for f, sheet, cols in ((C.F_LEGACY, "Notices", ("Notice Date", "Payment Date")), (C.F_REGISTER, "Commitments", ("First close",))):
        rows = list(load_workbook(os.path.join(target, f), read_only=True, data_only=True)[sheet].iter_rows(values_only=True))
        for r in rows[1:]:
            d = dict(zip(rows[0], r))
            for c in cols:
                if d.get(c):
                    upd(f, d[c])
    for d in K.read_capital_accounts(target):
        if d["NAV date"]:
            upd(C.F_CAPACC, d["NAV date"])
    late = {f: str(d) for f, d in latest.items() if d > dt.date.fromisoformat(man[f])}
    check("H16 no extract holds a date after its own extract date", not late and len(latest) == 8, str(late))


def block_figures(target, g):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    check("FIGURES reserve and expected calls as computed", fig["reserve_musd"] == g["reserve"] and
          fig["expected_calls_total_musd"] == cell25(m(g["total"])), "")
    sub = open(os.path.join(TASK, "submission.md")).read()
    check("FIGURES no em dash in the write-up", "\u2014" not in sub and "\u2013" not in sub, "")
    check("FIGURES five blocks", [h for h in re.findall(r"^## (.+)$", sub, re.M)] ==
          ["Tags", "1. Final Recommendation", "2. Critical Components", "3. Step-by-Step Solution", "4. Deliverable Answers"], "")
    import subprocess
    fc = subprocess.run([sys.executable, os.path.join(TASK, "..", ".claude", "skills", "determinism-check", "figures_check.py"),
                         TASK, "--quiet"], capture_output=True, text=True)
    check("FIGURES figures_check.py: every number in blocks 1 to 4 is in figures.json", fc.returncode == 0, fc.stdout.strip()[-90:])
    check("FIGURES the rivals block 1 names file $350 and $300 million", fig["rival_reserves_musd"] ==
          dict(pooled_rates=350, pooled_shares=300), str(fig["rival_reserves_musd"]))
    check("FIGURES block 3's bounds: no first year between 3 and 18 per cent, the own schedule within 2 per cent, more than "
          "twice the second-year share", fig["first_year_gap_pct"] == [3, 18] and fig["backtest_own_within_pct"] == 2 and
          fig["second_year_share_ratio"] > 2.0 and fig["backtest_pooled_low_vintages"] == fig["backtest_vintages"] == 12, "")


def main(target):
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    p, book, g = K.main_call(target)
    block_gates(target, meta)
    block_main(target, p, book, g)
    block_class(book)
    block_ladder(book)
    block_backtest(book)
    block_three_rules(target, book)
    block_mess(target)
    block_forks(target, p, book, g)
    block_separation(target, g)
    block_asks(target, p)
    block_realism(target)
    block_house(target)
    block_figures(target, g)
    bad = [r for r in RESULTS if not r[1]]
    for lab, ok, det in RESULTS:
        print("%s  %-92s %s" % ("PASS" if ok else "FAIL", lab, det))
    print("checks: %d assertions, %d failed" % (len(RESULTS), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
