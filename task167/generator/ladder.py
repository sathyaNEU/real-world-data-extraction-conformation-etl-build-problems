"""task167 ladder: the main call under every construction the design note names, from the shipped files.

    python3 ladder.py TARGET_DIR      prints every rung, the golden family and the Layer 1 mishandlings"""
from __future__ import annotations

import datetime as dt
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as K   # noqa: E402

STRATS = ("Buyout", "Growth equity", "Venture capital", "Private credit")


def family(book):
    """the golden family: every construction that reads each fund's call schedule from the funds whose first year
    looked like its own, at any age resolution, on either base, with any threshold in the gap and any vintage cut"""
    out = {}
    for step, nm in ((1, "monthly"), (3, "quarterly"), (12, "annual")):
        for rate in (False, True):
            out["class schedule, %s ages, %s" % (nm, "rate on the undrawn balance" if rate else "share of commitment")] = \
                K.golden_call(book, step, rate)
    for thr in (0.04, 0.09, 0.12):
        out["class schedule, first-year threshold %.0f per cent" % (thr * 100)] = K.golden_call(book, thr=thr)
    for v0 in (2012, 2014, 2016, 2018):
        out["class schedule, line funds of vintages %d on" % v0] = K.golden_call(book, line_from=v0)
    out["class schedule, funds equally weighted"] = K.golden_call(book, weight="equal")
    # the programme read by class, the earlier book on the pooled schedule
    cb = K.curve(book, lambda f: K.hist(f) and K.is_line(f))
    ca = K.curve(book, lambda f: K.hist(f) and not K.is_line(f))
    cp = K.curve(book, K.hist)
    out["class schedule for the programme, pooled for the earlier funds"] = \
        K.forecast(book, lambda f: (cb if K.is_line(f) else ca) if f["programme"] else cp)
    # each line fund's own analogue: the line funds of its strategy
    cbs = {s: K.curve(book, lambda f, s=s: K.hist(f) and K.is_line(f) and f["strategy"] == s) for s in STRATS}
    cas = {s: K.curve(book, lambda f, s=s: K.hist(f) and not K.is_line(f) and f["strategy"] == s) for s in STRATS}
    out["class schedule by strategy"] = K.forecast(book, lambda f: cbs[f["strategy"]] if K.is_line(f) else cas[f["strategy"]])
    return out


def rivals(book):
    out = {}
    for step, nm in ((1, "monthly"), (3, "quarterly"), (12, "annual")):
        for rate in (False, True):
            cp = K.curve(book, K.hist, step, rate)
            out["pooled schedule, %s ages, %s" % (nm, "rate on the undrawn balance" if rate else "share of commitment")] = \
                K.forecast(book, lambda f, cp=cp: cp, step, rate)
    for rate in (False, True):
        cs = {s: K.curve(book, lambda f, s=s: K.hist(f) and f["strategy"] == s, 3, rate) for s in STRATS}
        out["schedule by strategy, %s" % ("rate" if rate else "share")] = K.forecast(book, lambda f, cs=cs: cs[f["strategy"]], 3, rate)
    for v0 in (2014, 2017, 2019):
        for rate in (False, True):
            cv = K.curve(book, lambda f, v0=v0: K.hist(f) and f["vintage"] >= v0, 3, rate)
            out["schedule of vintages %d on, %s" % (v0, "rate" if rate else "share")] = K.forecast(book, lambda f, cv=cv: cv, 3, rate)
    for y0 in (2019, 2022):
        cc = K.curve(book, K.hist, 3, True, m_from=K.mi(dt.date(y0, 1, 1)))
        out["rates on calls since %d" % y0] = K.forecast(book, lambda f, cc=cc: cc, 3, True)
    # the programme's own first year carried forward: pooled schedule scaled by the programme's pace against it
    cp = K.curve(book, K.hist)
    prog = [f for f in book.funds.values() if f["programme"]]
    exp = sum(f["commitment"] * sum(cp[:f["obs"]]) for f in prog)
    got = sum(f["paid"] for f in prog)
    own = got / exp
    out["pooled schedule at the programme's own first-year pace"] = \
        K.forecast(book, lambda f: [x * own for x in cp] if f["programme"] else cp)
    # 2026's calls carried, and 2026's rate on the undrawn balance
    m26 = K.mi(dt.date(2026, 1, 1))
    c26 = 0.0
    u26 = 0.0
    u27 = 0.0
    for f in book.funds.values():
        a26 = m26 - f["m0"]
        r = book.fx_of(f)
        c26 += sum(f["h"][max(0, a26):f["obs"]]) * r
        if a26 >= 0:
            u26 += (f["commitment"] - sum(f["h"][:a26])) * r
        elif f["obs"] > 0:
            u26 += f["commitment"] * r
        if f["status"] == "Active":
            u27 += (f["commitment"] - f["paid"]) * r
    out["2026 calls carried"] = {"_": c26}
    out["2026 rate on the undrawn balance"] = {"_": c26 / u26 * u27}
    return out


def tot(fc):
    return sum(fc.values())


def by_strategy(book, fc):
    s = defaultdict(float)
    for fid, v in fc.items():
        if fid in book.funds:
            s[book.funds[fid]["strategy"]] += v
    return dict(s)


def report(target):
    p = K.Pack(target)
    book = K.Book(p)
    fam = family(book)
    riv = rivals(book)
    g = K.golden_call(book)
    print("golden total %.1f reserve %d" % (tot(g) / 1e6, K.reserve(tot(g))))
    print("family:")
    for k, v in fam.items():
        bs = by_strategy(book, v)
        print("  %-78s %7.1f  %s" % (k, tot(v) / 1e6, " ".join("%6.1f" % (bs.get(s, 0) / 1e6) for s in STRATS)))
    print("rivals:")
    for k, v in riv.items():
        bs = by_strategy(book, v) if "_" not in v else {}
        print("  %-78s %7.1f  reserve %d  %s" % (k, tot(v) / 1e6, K.reserve(tot(v)), " ".join("%6.1f" % (bs.get(s, 0) / 1e6) for s in STRATS)))
    return p, book, fam, riv


if __name__ == "__main__":
    report(sys.argv[1])
