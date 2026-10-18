"""task167 custody: the reserve account's 2026 at the Foundation's custodian, settled activity and year-end
positions. The account pays every capital call by wire (euro calls at the custodian's spot rate), holds Treasury
bills, the approved government money market fund and cash, and on 31 December 2026 bought the 2027 bill ladder for
settlement on 4 January 2027. Positions are reported by trade date; cash is the settled ledger balance."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as C
import world as W

RESERVE_ACCT = "6011-2207"
OPERATING_ACCT = "6011-2215"
ACCT_NAME = {RESERVE_ACCT: "BF Reserve", OPERATING_ACCT: "BF Operating"}
GOV_MMF = "Ironvale Government Money Market Fund, Institutional Shares"
PRIME_MMF = "Ironvale Institutional Prime Obligations Fund"
YIELD = 0.0362           # the bill yield the custodian prices to at year end (discount basis)


def bill_price(par, d, maturity, y=YIELD):
    days = (maturity - d).days
    return round(par * (1.0 - y * days / 360.0), 2)


class Holding:
    def __init__(self, sid, desc, kind, qty, maturity=None):
        self.sid, self.desc, self.kind, self.qty, self.maturity = sid, desc, kind, qty, maturity


def _sid(rng, prefix):
    return "%s%07d" % (prefix, int(rng.integers(1000000, 9999999)))


def bill_desc(m):
    return "U.S. TREASURY BILL %s" % C.d_us(m)


def build(notices, fx):
    """settled activity rows, year-end positions rows, and the truth the asks are graded on"""
    rng = np.random.default_rng([W.SEED, 21])
    acts = []          # (settle, trade, acct, txn, sid, desc, qty, amount, ref)
    hold = {}          # sid -> Holding (settled), reserve account
    cash = 0.0

    def act(settle, trade, txn, sid, desc, qty, amount, ref=""):
        nonlocal cash
        cash = round(cash + amount, 2)
        acts.append((settle, trade, RESERVE_ACCT, txn, sid, desc, qty, round(amount, 2), ref))

    # opening position, 1 January 2026: the 2026 ladder, the government fund, a 2028 note and cash
    open_day = dt.date(2026, 1, 1)
    ladder26 = [(dt.date(2026, 3, 26), 45e6), (dt.date(2026, 6, 25), 45e6), (dt.date(2026, 9, 24), 45e6),
                (dt.date(2026, 12, 17), 45e6)]
    opening = []
    for mat, par in ladder26:
        sid = _sid(rng, "T")
        hold[sid] = Holding(sid, bill_desc(mat), "U.S. Treasury Bill", par, mat)
        opening.append((sid, hold[sid].desc, par, bill_price(par, open_day, mat, 0.0391)))
    note_sid = _sid(rng, "N")
    hold[note_sid] = Holding(note_sid, "U.S. TREASURY NOTE 3.875% 01/31/2028", "U.S. Treasury Note", 8e6,
                             dt.date(2028, 1, 31))
    opening.append((note_sid, hold[note_sid].desc, 8e6, round(8e6 * 0.9987, 2)))
    mmf_sid = _sid(rng, "M")
    hold[mmf_sid] = Holding(mmf_sid, GOV_MMF, "Money Market Fund", 21_604_388.17)
    opening.append((mmf_sid, GOV_MMF, 21_604_388.17, 21_604_388.17))
    for sid, desc, qty, mv in opening:
        acts.append((open_day, open_day, RESERVE_ACCT, "OPENING POSITION", sid, desc, qty, 0.0, ""))
    cash = 2_918_406.55
    acts.append((open_day, open_day, RESERVE_ACCT, "OPENING CASH BALANCE", "CASH", "U.S. DOLLAR", 0, cash, ""))

    def mmf_redeem(day, need):
        h = hold[mmf_sid]
        amt = min(h.qty, round(need, 2))
        if amt <= 0:
            return
        h.qty = round(h.qty - amt, 2)
        act(day, day, "REDEMPTION", mmf_sid, GOV_MMF, -amt, amt)

    def mmf_buy(day, amt):
        h = hold[mmf_sid]
        h.qty = round(h.qty + amt, 2)
        act(day, day, "PURCHASE", mmf_sid, GOV_MMF, amt, -amt)

    # the year's events: calls by wire, bill maturities, purchases, transfers, dividends
    events = []
    for n in notices:
        if n.status != "Settled" or not (dt.date(2026, 1, 1) <= n.value_date <= dt.date(2026, 12, 31)):
            continue
        amt = n.calls() - n.dists() if n.kind == "net" else (n.calls() if n.kind == "call" else 0.0)
        if amt <= 0:
            continue
        events.append((n.value_date, 1, "call", n, amt))
    for mat, par in ladder26:
        events.append((mat, 0, "mature", mat, par))
    purchases = [(dt.date(2026, 7, 9), dt.date(2027, 7, 8), 25e6), (dt.date(2026, 7, 30), dt.date(2027, 1, 28), 20e6),
                 (dt.date(2026, 10, 15), dt.date(2027, 4, 15), 15e6), (dt.date(2026, 11, 27), dt.date(2027, 2, 25), 12e6),
                 (dt.date(2026, 12, 3), dt.date(2027, 12, 2), 18e6)]
    for d, mat, par in purchases:
        events.append((d, 2, "buybill", mat, par))
    for d, mat, par, issuer in ((dt.date(2026, 9, 10), dt.date(2027, 3, 11), 10e6, "FEDERAL HOME LOAN BANK DISC NT"),
                                (dt.date(2026, 10, 22), dt.date(2027, 5, 20), 8e6, "FEDERAL FARM CREDIT BANK DISC NT"),
                                (dt.date(2026, 11, 12), dt.date(2027, 8, 12), 12e6, "FEDERAL HOME LOAN BANK DISC NT"),
                                (dt.date(2026, 12, 10), dt.date(2027, 11, 4), 9e6, "FEDERAL FARM CREDIT BANK DISC NT")):
        events.append((d, 2, "buyagency", (mat, issuer), par))
    events.append((dt.date(2026, 9, 17), 2, "buyprime", None, 6e6))
    events.append((dt.date(2026, 1, 8), 0, "transfer", None, 41_500_000.00))
    events.append((dt.date(2026, 7, 7), 0, "transfer", None, 60_000_000.00))
    events.append((dt.date(2026, 12, 15), 0, "transfer", None, 95_000_000.00))
    for mo in range(1, 13):
        last = dt.date(2026, mo, 28)
        events.append((C.roll_business(last), 3, "dividend", None, None))
    events.sort(key=lambda e: (e[0], e[1]))
    prime_sid = _sid(rng, "M")
    for day, _, kind, obj, val in events:
        if kind == "call":
            n = obj
            if n.vehicle.fund.ccy == "EUR":
                rate = round(fx[_rate_day(fx, day)] * 1.0012, 4)
                usd = round(val * rate, 2)
                desc = "WIRE OUT CAPITAL CALL %s EUR %s AT %.4f" % (n.vehicle.code, "{:,.2f}".format(val), rate)
            else:
                usd = round(val, 2)
                desc = "WIRE OUT CAPITAL CALL %s" % n.vehicle.code
            if cash < usd:
                mmf_redeem(day, usd - cash + 250_000.0)
            act(day, day, "WIRE OUT", "CASH", desc, 0, -usd, n.ref)
        elif kind == "mature":
            mat = obj
            sid = [s for s, h in hold.items() if h.kind == "U.S. Treasury Bill" and h.maturity == mat][0]
            par = hold[sid].qty
            del hold[sid]
            act(day, day, "MATURITY", sid, bill_desc(mat), -par, par)
        elif kind == "buybill":
            mat, par = obj, val
            cost = bill_price(par, day, mat, 0.0371)
            if cash < cost:
                mmf_redeem(day, cost - cash + 100_000.0)
            sid = _sid(rng, "T")
            hold[sid] = Holding(sid, bill_desc(mat), "U.S. Treasury Bill", par, mat)
            act(day, day, "PURCHASE", sid, bill_desc(mat), par, -cost)
        elif kind == "buyagency":
            (mat, issuer), par = obj, val
            cost = bill_price(par, day, mat, 0.0386)
            if cash < cost:
                mmf_redeem(day, cost - cash + 100_000.0)
            sid = _sid(rng, "A")
            hold[sid] = Holding(sid, "%s %s" % (issuer, C.d_us(mat)), "Agency Discount Note", par, mat)
            act(day, day, "PURCHASE", sid, hold[sid].desc, par, -cost)
        elif kind == "buyprime":
            if cash < val:
                mmf_redeem(day, val - cash + 100_000.0)
            hold[prime_sid] = Holding(prime_sid, PRIME_MMF, "Money Market Fund", val)
            act(day, day, "PURCHASE", prime_sid, PRIME_MMF, val, -val)
        elif kind == "transfer":
            act(day, day, "TRANSFER IN", "CASH", "TRANSFER FROM ENDOWMENT POOL 6011-1003", 0, val)
            if day.month == 12:
                mmf_buy(day, 60_000_000.00)
        elif kind == "dividend":
            for sid, rate in ((mmf_sid, 0.0348), (prime_sid, 0.0371)):
                if sid in hold and hold[sid].qty > 0:
                    dv = round(hold[sid].qty * rate / 12.0, 2)
                    hold[sid].qty = round(hold[sid].qty + dv, 2)
                    acts.append((day, day, RESERVE_ACCT, "DIVIDEND REINVEST", sid, hold[sid].desc, dv, 0.0, ""))
    # the year-end roll: four bills bought on 31 December for settlement on 4 January 2027 (not in settled activity)
    trade = dt.date(2026, 12, 31)
    pending = []
    for mat, par in ((dt.date(2027, 3, 25), 40e6), (dt.date(2027, 6, 24), 40e6), (dt.date(2027, 9, 23), 30e6),
                     (dt.date(2027, 12, 16), 30e6)):
        sid = _sid(rng, "T")
        pending.append(Holding(sid, bill_desc(mat), "U.S. Treasury Bill", par, mat))
    # positions at the close of 31 December 2026, valued at the custodian's year-end prices
    ye = dt.date(2026, 12, 31)
    pos = []
    for h in list(hold.values()) + pending:
        if h.kind in ("U.S. Treasury Bill", "Agency Discount Note"):
            mv = bill_price(h.qty, ye, h.maturity, YIELD if h.kind == "U.S. Treasury Bill" else 0.0377)
            pos.append((RESERVE_ACCT, h.sid, h.desc, "Government Bill", h.qty, round(mv / h.qty * 100, 6), mv, h.maturity))
        elif h.kind == "U.S. Treasury Note":
            mv = round(h.qty * 0.99938, 2)
            pos.append((RESERVE_ACCT, h.sid, h.desc, "Government Note", h.qty, 99.938, mv, h.maturity))
        else:
            pos.append((RESERVE_ACCT, h.sid, h.desc, h.kind, round(h.qty, 2), 1.0, round(h.qty, 2), None))
    pos.append((RESERVE_ACCT, "CASH", "U.S. DOLLAR", "Cash", round(cash, 2), 1.0, round(cash, 2), None))
    op_cash = 3_861_207.42
    op_bill_sid = _sid(rng, "T")
    op_mat = dt.date(2027, 2, 18)
    pos.append((OPERATING_ACCT, op_bill_sid, bill_desc(op_mat), "Government Bill", 25e6,
                round(bill_price(25e6, ye, op_mat) / 25e6 * 100, 6), bill_price(25e6, ye, op_mat), op_mat))
    pos.append((OPERATING_ACCT, "CASH", "U.S. DOLLAR", "Cash", op_cash, 1.0, op_cash, None))
    truth = dict(settled_bills=[h for h in hold.values() if h.kind == "U.S. Treasury Bill"], pending=pending,
                 mmf=hold[mmf_sid].qty, cash=round(cash, 2), prime=hold[prime_sid].qty,
                 positions=pos, opening_cash=2_918_406.55)
    return acts, pos, truth


def _rate_day(fx, d):
    while d not in fx:
        d -= dt.timedelta(days=1)
    return d
