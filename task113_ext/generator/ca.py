"""Merriden's corporate actions feed, every revision as its own record, and its delisting workbook's rows.

Dividends are announced some weeks before their ex-date (record date one business day after the ex-date until the
move to one-day settlement on 28 May 2024, the same day after it); a few pay dates are amended; some companies that
had declared a dividend in March 2020 cancelled it. Splits, reverse splits and spin-offs carry their terms. Deals
are announced, sometimes amended (raised terms, a later expected close), completed or, once, terminated. Listings,
delistings and changes of symbol, name and exchange close the set. Dividends already declared at the pull for
ex-dates after the store's last day are in the feed too."""
import datetime as dt

import numpy as np

import history as H
import universe as U
import world as W

T1_SETTLE = dt.date(2024, 5, 28)


def _bday(d, n):
    step = 1 if n >= 0 else -1
    k = 0
    while k != n:
        d += dt.timedelta(days=step)
        if d.weekday() < 5:
            k += step
    return d


def _ts(d, rng, lo=11, hi=23):
    """A publication stamp in UTC on day d."""
    h = int(rng.integers(lo, hi))
    return dt.datetime(d.year, d.month, d.day, h, int(rng.integers(0, 60)), int(rng.integers(0, 60)))


class Feed:
    def __init__(self):
        self.rows = []
        self.n = 0

    def new_id(self, year):
        self.n += 1
        return "MCA%d%06d" % (year % 100, 100000 + self.n * 7 % 900000)


def build(secs, paths, bars, hist):
    rng = U.rng_for(7)
    f = Feed()
    sid = {s["k"]: s["sid"] for s in secs}

    def ident(k, i):
        sp = H.on(hist, k, min(max(i, secs[k]["first"]), (secs[k]["last"] if secs[k]["last"] is not None else U.T - 1)))
        return sp["ticker"], sp["cusip"]

    def rec(cid, rev, status, etype, k, i_ann, ann, pub, **kw):
        tk, cu = ident(k, i_ann)
        r = dict(ca_id=cid, revision=rev, status=status, event_type=etype, security_id=sid[k], symbol=tk, cusip=cu,
                 announce_date=ann.isoformat(), published_utc=pub.strftime("%Y-%m-%dT%H:%M:%SZ"))
        for key in ("ex_date", "record_date", "pay_date", "effective_date"):
            v = kw.pop(key, None)
            r[key] = v.isoformat() if v else None
        r["terms"] = kw.pop("terms", {})
        if kw.get("note"):
            r["note"] = kw.pop("note")
        f.rows.append(r)

    for s in secs:
        k = s["k"]
        p = paths[k]
        # cash and special dividends
        cancel_done = False
        for dv in p.divs:
            ex = U.DAYS[dv["ex"]]
            ann = _bday(ex, -int(rng.integers(10, 22)))
            record = ex if ex >= T1_SETTLE else _bday(ex, 1)
            pay = _bday(record, int(rng.integers(5, 21)))
            cid = f.new_id(ann.year)
            et = "DIV_CASH" if dv["kind"] == "CASH" else "DIV_SPECIAL"
            terms = dict(gross_amount=dv["amount"], currency="USD",
                         frequency="QUARTERLY" if dv["kind"] == "CASH" else "NON-RECURRING")
            pub = _ts(ann, rng)
            rec(cid, 1, "NEW", et, k, U.day_on_or_after(ann), ann, pub, ex_date=ex, record_date=record,
                pay_date=pay, terms=terms)
            if rng.random() < 0.03:
                pay2 = _bday(pay, int(rng.integers(1, 6)))
                rec(cid, 2, "AMEND", et, k, U.day_on_or_after(ann), ann, _ts(_bday(ann, int(rng.integers(1, 5))), rng),
                    ex_date=ex, record_date=record, pay_date=pay2, terms=terms, note="pay date revised")
        if getattr(p, "covid", False):
            sus = [i for i, what in p.divplan if what == "suspended"]
            if sus and rng.random() < 0.6:
                ex = U.DAYS[sus[0]]
                ann = dt.date(2020, 3, int(rng.integers(2, 11)))
                ann = ann if ann.weekday() < 5 else _bday(ann, 1)
                record = _bday(ex, 1)
                cid = f.new_id(2020)
                last_amt = [d["amount"] for d in p.divs if U.DAYS[d["ex"]] < dt.date(2020, 4, 1)]
                terms = dict(gross_amount=last_amt[-1] if last_amt else 0.1, currency="USD", frequency="QUARTERLY")
                rec(cid, 1, "NEW", "DIV_CASH", k, U.day_on_or_after(ann), ann, _ts(ann, rng), ex_date=ex,
                    record_date=record, pay_date=_bday(record, 14), terms=terms)
                cx = dt.date(2020, 3, int(rng.integers(20, 31)))
                cx = cx if cx.weekday() < 5 else _bday(cx, 1)
                rec(cid, 2, "CANCEL", "DIV_CASH", k, U.day_on_or_after(ann), ann, _ts(cx, rng), ex_date=ex,
                    record_date=record, pay_date=_bday(record, 14), terms=terms, note="dividend withdrawn by issuer")
        # splits and reverse splits
        for sp in p.splits:
            ex = U.DAYS[sp["ex"]]
            ann = U.DAYS[max(sp["announce"], s["first"])]
            if sp["F"] >= 1:
                new, old = {1.5: (3, 2), 2.0: (2, 1), 3.0: (3, 1)}[sp["F"]]
                et = "SPLIT"
                record = _bday(ex, -int(rng.integers(8, 14)))
                pay = _bday(ex, -1)
            else:
                new, old = 1, int(round(1 / sp["F"]))
                et = "REVERSE_SPLIT"
                record = pay = None
            cid = f.new_id(ann.year)
            rec(cid, 1, "NEW", et, k, sp["announce"], ann, _ts(ann, rng), ex_date=ex, record_date=record,
                pay_date=pay, terms=dict(new_shares=new, old_shares=old))
        # spin-offs
        for e in s["events"]:
            if e[0] == "spinoff":
                ex = U.DAYS[e[1]]
                ch = secs[e[2]]
                ann = _bday(ex, -int(rng.integers(30, 45)))
                cid = f.new_id(ann.year)
                ctk, ccu = ident(ch["k"], e[1])
                record = _bday(ex, -int(rng.integers(8, 12)))
                rec(cid, 1, "NEW", "SPINOFF", k, U.day_on_or_after(ann), ann, _ts(ann, rng), ex_date=ex,
                    record_date=record, pay_date=_bday(ex, -1),
                    terms=dict(distributed_security_id=ch["sid"], distributed_symbol=ctk, distributed_cusip=ccu,
                               ratio=p.spin_ratio))
        # deals
        d = s.get("deal")
        if d:
            a = U.DAYS[d["announce"]]
            cid = f.new_id(a.year)
            if d["kind"] == "stock":
                acq = secs[d["acquirer"]]
                atk, _ = ident(acq["k"], d["announce"])
                terms = dict(acquirer_name=H.on(hist, acq["k"], d["announce"])["name"], acquirer_security_id=acq["sid"],
                             acquirer_symbol=atk, shares_per_share=p.deal_K, cash_per_share=0.0)
                et = "MERGER_STOCK"
            else:
                terms = dict(acquirer_name=_buyer(rng, d["kind"]), cash_per_share=p.deal_K)
                et = "GO_PRIVATE" if d["kind"] == "private" else "MERGER_CASH"
            rec(cid, 1, "NEW", et, k, d["announce"], a, _ts(a, rng, 11, 14), terms=dict(terms))
            rev = 2
            if d["kind"] == "terminated":
                t = U.DAYS[d["terminate"]]
                rec(cid, rev, "CANCEL", et, k, d["announce"], a, _ts(t, rng), effective_date=None, terms=dict(terms),
                    note="merger agreement terminated")
            elif d.get("close"):
                if rng.random() < 0.35:
                    mid = U.DAYS[(d["announce"] + d["close"]) // 2]
                    rec(cid, rev, "AMEND", et, k, d["announce"], a, _ts(mid, rng), terms=dict(terms),
                        note="shareholder approval received; expected close %s" % U.DAYS[d["close"]].isoformat())
                    rev += 1
                eff = U.DAYS[d["close"]]
                rec(cid, rev, "COMPLETE", et, k, d["announce"], a, _ts(_bday(eff, -1), rng, 20, 23),
                    effective_date=eff, terms=dict(terms))
        # delisting for cause
        if s["fate"] == "cause":
            last = U.DAYS[s["last"]]
            ann = _bday(last, -int(rng.integers(3, 12)))
            eff = U.DAYS[s["last"] + 1] if s["last"] + 1 < U.T else _bday(last, 1)
            cid = f.new_id(ann.year)
            rec(cid, 1, "NEW", "DELISTING", k, U.day_on_or_after(ann), ann, _ts(ann, rng), effective_date=eff,
                terms=dict(reason="BANKRUPTCY" if s.get("bankrupt") else "CONTINUED_LISTING_STANDARDS",
                           successor_venue="OTC"))
        # listings
        if s["kind"] in ("ipo", "spin"):
            first = U.DAYS[s["first"]]
            ann = _bday(first, -int(rng.integers(1, 4)))
            cid = f.new_id(ann.year)
            terms = dict(listing_type="IPO" if s["kind"] == "ipo" else "SPIN-OFF")
            if s["kind"] == "ipo":
                terms["offer_price"] = s["ipo_offer"]
            rec(cid, 1, "NEW", "LISTING", k, s["first"], ann, _ts(ann, rng), effective_date=first, terms=terms)
        # symbol, name and exchange changes
        spells = hist[k]
        for (a0, a1, sp0), (b0, b1, sp1) in zip(spells, spells[1:]):
            eff = U.DAYS[b0]
            ann = _bday(eff, -int(rng.integers(3, 12)))
            for et, before, after in (("SYMBOL_CHANGE", sp0["ticker"], sp1["ticker"]),
                                      ("NAME_CHANGE", sp0["name"], sp1["name"]),
                                      ("EXCHANGE_CHANGE", W.MIC[sp0["exch"]], W.MIC[sp1["exch"]])):
                if before != after:
                    cid = f.new_id(ann.year)
                    rec(cid, 1, "NEW", et, k, a1, ann, _ts(ann, rng), effective_date=eff,
                        terms=dict(old_value=before, new_value=after))
    _future_dividends(secs, paths, f, rec, rng)
    f.rows.sort(key=lambda r: (r["published_utc"], r["ca_id"], r["revision"]))
    return f.rows


def _future_dividends(secs, paths, f, rec, rng):
    """Dividends declared by the pull with ex-dates after the store's last day."""
    for s in secs:
        p = paths[s["k"]]
        if s["last"] is not None or not p.divs or (s.get("deal") and s["deal"].get("close") is None):
            continue
        last = p.divs[-1]
        if last["kind"] != "CASH" or U.DAYS[last["ex"]] < dt.date(2026, 6, 1):
            continue
        ex = U.DAYS[last["ex"]] + dt.timedelta(days=91)
        while ex.weekday() >= 5:
            ex += dt.timedelta(days=1)
        ann = _bday(ex, -int(rng.integers(10, 22)))
        if ex <= W.END or ann > W.CA_PULLED:
            continue
        cid = f.new_id(ann.year)
        pay = _bday(ex, int(rng.integers(5, 21)))
        rec(cid, 1, "NEW", "DIV_CASH", s["k"], U.T - 1, ann, _ts(ann, rng), ex_date=ex, record_date=ex, pay_date=pay,
            terms=dict(gross_amount=last["amount"], currency="USD", frequency="QUARTERLY"))


BUYERS = ["Ridgeline Partners", "Calder Bay Capital", "Stonepath Equity", "Harland Industrial Group",
          "Mosswood Holdings", "Tessaly Capital Partners", "Overbrook Acquisition Corp.", "Fairhaven Capital",
          "Northvale Group", "Kingsbury Partners", "Westmarch Holdings", "Dunross Capital"]


def _buyer(rng, kind):
    return BUYERS[int(rng.integers(len(BUYERS)))]


def delistings(secs, paths, bars, hist):
    """The delisting workbook's rows: last exchange trade, consideration and the vendor's delisting return."""
    rng = U.rng_for(8)
    rows = []
    for s in secs:
        if s["last"] is None:
            continue
        k = s["k"]
        b = bars[k]
        sp = H.on(hist, k, s["last"])
        last_close = float(b["close"][-1])
        row = dict(security_id=s["sid"], last_symbol=sp["ticker"], issuer_name=sp["name"], cusip=sp["cusip"],
                   last_trading_date=U.DAYS[s["last"]], final_exchange_close=last_close, code=None, reason=None,
                   cash_per_share=None, shares_per_share=None, acquirer_security_id=None, otc_first_date=None,
                   otc_first_price=None, delisting_return=None, note=None)
        d = s.get("deal")
        if s["fate"] in ("cash", "private"):
            row.update(code="M1" if s["fate"] == "cash" else "P1",
                       reason="Merger: cash" if s["fate"] == "cash" else "Going private: cash",
                       cash_per_share=paths[k].deal_K)
            row["delisting_return"] = round(paths[k].deal_K / last_close - 1, 6)
        elif s["fate"] == "stock":
            acq = secs[d["acquirer"]]
            ab = bars[acq["k"]]
            acq_close = float(ab["close"][d["close"] - ab["i0"]])
            row.update(code="M2", reason="Merger: stock", shares_per_share=paths[k].deal_K,
                       acquirer_security_id=acq["sid"])
            row["delisting_return"] = round(paths[k].deal_K * acq_close / last_close - 1, 6)
        else:
            row.update(code="X2" if s.get("bankrupt") else "X1",
                       reason="Bankruptcy filing" if s.get("bankrupt") else "Continued listing standards")
            if rng.random() < 0.8:
                od = U.DAYS[min(U.T - 1, s["last"] + int(rng.integers(1, 5)))]
                op = last_close * float(rng.uniform(0.3, 0.7) if s.get("bankrupt") else rng.uniform(0.6, 0.95))
                op = round(op, 4)
                row.update(otc_first_date=od, otc_first_price=op, delisting_return=round(op / last_close - 1, 6))
            else:
                row["note"] = "No OTC trade within 10 trading days of delisting"
        rows.append(row)
    rows.sort(key=lambda r: (r["last_trading_date"], r["security_id"]))
    return rows
