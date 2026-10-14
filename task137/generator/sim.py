"""The world: Kaimai Building Society's members, their term deposits from the cohorts that mature between January 2025
and March 2027, the seven closed maturity campaigns Harbourline worked (release, dials, conversations, close-outs), what
each listed deposit did at maturity (the account events and transfers), the January to March 2027 list, the holdings
view on 2 November 2026 and the legacy certificate platform with its migration batches.

Everything is forward: records first, every figure later computed from the written files (calc.py, asks.py)."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import world as W

# ---------------------------------------------------------------------------------------------------------------
# Volumes. Synthetic cohorts opened before 2025 that mature in the window, by (maturity quarter, term): all maturing
# deposits of that cohort (listed and not). New money opened in the window quarters, by (opening quarter, term).
SYN = {
    # maturity quarter: {term: count}
    "2025Q1": {1: 4560, 2: 1100, 3: 1500, 4: 1380, 5: 1860},
    "2025Q2": {1: 4740, 2: 2280, 3: 1500, 4: 1320, 5: 1800},
    "2025Q3": {1: 4620, 2: 2400, 3: 1560, 4: 1380, 5: 1800},
    "2025Q4": {1: 4440, 2: 2460, 3: 1620, 4: 1320, 5: 1860},
    "2026Q1": {2: 2340, 3: 1560, 4: 1380, 5: 1800},
    "2026Q2": {2: 2340, 3: 1620, 4: 1320, 5: 1800},
    "2026Q3": {2: 2400, 3: 1680, 4: 1380, 5: 1740},
    "2026Q4": {2: 2340, 3: 1620, 4: 1380, 5: 1800},
    "2027Q1": {3: 850, 4: 500, 5: 900},
}
SPECIAL_2023Q1 = 13400      # the 2023 four-year special's deposits (all maturing in 2027Q1)
NEW_MONEY = {("2025Q1", 1): 1800, ("2025Q2", 1): 1860, ("2025Q3", 1): 1800, ("2025Q4", 1): 1320,
             ("2026Q1", 1): 1300, ("2025Q1", 2): 250}

LIST_MIN = 25000.0


def qrange(a, b):
    out, q = [], a
    while q <= b:
        out.append(q)
        q = W.q_add(q, 1)
    return out


def add_years(d, n):
    try:
        return d.replace(year=d.year + n)
    except ValueError:              # 29 February
        return d.replace(year=d.year + n, day=28)


class World:
    pass


# ---------------------------------------------------------------------------------------------------------------
# Members and their phone numbers
MOBILE_PREFIX = ("021", "022", "027", "029", "020")
LAND_AREAS = (("07", ("57", "54", "52", "55", "56", "57", "57", "54")), ("07", ("84", "85", "83", "82")),
              ("09", ("48", "52", "44", "62")), ("06", ("35", "35", "86")), ("04", ("38", "47", "56")))


def _number(r, kind):
    if kind == "M":
        p = MOBILE_PREFIX[int(r.integers(0, len(MOBILE_PREFIX)))]
        n = int(r.integers(1000000, 9999999))
        return "0%s%07d" % (p[1:], n) if p != "020" else "020%08d" % int(r.integers(10000000, 99999999))
    area, pres = LAND_AREAS[int(r.choice(len(LAND_AREAS), p=[0.46, 0.22, 0.14, 0.10, 0.08]))]
    pre = pres[int(r.integers(0, len(pres)))]
    return "%s%s%05d" % (area, pre, int(r.integers(0, 100000)))


def _display(r, nat, kind):
    """The number as the member's record holds it: a mix of the forms the society's systems and branches typed."""
    d = nat
    u = float(r.random())
    if kind == "M":
        if d.startswith("020"):
            body = d
            forms = ["%s %s %s" % (body[:3], body[3:7], body[7:]), "+64 %s %s %s" % (body[1:3], body[3:7], body[7:]),
                     body, "+64" + body[1:]]
        else:
            forms = ["%s %s %s" % (d[:3], d[3:6], d[6:]), "+64 %s %s %s" % (d[1:3], d[3:6], d[6:]), d, "+64" + d[1:],
                     "(%s) %s %s" % (d[:3], d[3:6], d[6:])]
        w = [0.40, 0.22, 0.20, 0.10, 0.08][:len(forms)]
    else:
        forms = ["(%s) %s %s" % (d[:2], d[2:5], d[5:]), "%s %s %s" % (d[:2], d[2:5], d[5:]), d,
                 "+64 %s %s %s" % (d[1:2], d[2:5], d[5:]), "%s-%s %s" % (d[:2], d[2:5], d[5:])]
        w = [0.34, 0.26, 0.18, 0.12, 0.10]
    w = np.array(w) / sum(w)
    return forms[int(r.choice(len(forms), p=w))]


def make_customer(Wd, r, age):
    cno = Wd.next_cust
    Wd.next_cust += int(r.integers(3, 41))
    if age < 45:
        k = int(r.choice([1, 2, 3, 4], p=[0.46, 0.39, 0.13, 0.02]))
    elif age < 65:
        k = int(r.choice([1, 2, 3, 4], p=[0.30, 0.42, 0.22, 0.06]))
    else:
        k = int(r.choice([1, 2, 3, 4], p=[0.24, 0.44, 0.24, 0.08]))
    kinds = []
    first_mobile = r.random() < (0.92 if age < 65 else 0.74)
    kinds.append("M" if first_mobile else "H")
    while len(kinds) < k:
        # a member holds at most two mobiles, one home line and one work line
        opts = []
        if "H" not in kinds:
            opts.append(("H", 0.55 if age >= 60 else 0.35))
        if "W" not in kinds and age < 72:
            opts.append(("W", 0.45))
        if kinds.count("M") < 2:
            opts.append(("M", 0.20))
        if not opts:
            break
        w = np.array([x[1] for x in opts])
        kinds.append(opts[int(r.choice(len(opts), p=w / w.sum()))][0])
    phones = []
    for kind in kinds:
        nat = _number(r, kind)
        u = float(r.random())
        state = "D" if u < W.P_DEAD[kind] else ("X" if u < W.P_DEAD[kind] + W.P_WRONG[kind] else "V")
        added = dt.date(2011, 1, 1) + dt.timedelta(days=int(r.integers(0, 5300)))
        phones.append(dict(nat=nat, e164=W.e164(nat), kind=kind, state=state, added=added,
                           display=_display(r, nat, kind)))
    c = dict(cust=cno, age=int(age), phones=phones, branch=str(r.choice(
        ["0410", "0412", "0415", "0418", "0421", "0430", "0435", "0440"], p=[.26, .17, .12, .09, .08, .10, .09, .09])),
             savings=None)
    Wd.customers[cno] = c
    return c


def register_entries(Wd, stream="register", only=None):
    """The do-not-call register: numbers members asked the society not to call, with the date each was recorded and,
    for some, the date the member withdrew the request. Built per number across the whole membership (or, for the
    members added last, across those only)."""
    r = W.rng(stream)
    out = getattr(Wd, "register", [])
    for c in Wd.customers.values():
        if only is not None and c["cust"] not in only:
            continue
        for ph in c["phones"]:
            u = float(r.random())
            base = 0.075 + (0.025 if ph["kind"] == "H" else 0.0) + (0.02 if ph["kind"] == "W" else 0.0)
            if u < base:
                start = max(ph["added"], dt.date(2017, 3, 1))
                span = (dt.date(2026, 10, 30) - start).days
                if span <= 10:
                    continue
                added = start + dt.timedelta(days=int(r.integers(1, span)))
                removed = None
                if r.random() < 0.11:
                    rem = added + dt.timedelta(days=int(r.integers(30, 900)))
                    if rem < dt.date(2026, 10, 31):
                        removed = rem
                src = str(r.choice(["BRANCH", "ONLINE", "CONTACT CENTRE", "COMPLAINT"], p=[.38, .34, .22, .06]))
                ph["dnc"] = (added, removed)
                out.append(dict(e164=ph["e164"], added=added, removed=removed, source=src, cust=c["cust"]))
    out.sort(key=lambda x: (x["added"], x["e164"]))
    Wd.register = out


def callable_on(ph, day):
    if "dnc" not in ph:
        return True
    a, rm = ph["dnc"]
    if a <= day and (rm is None or rm > day):
        return False
    return True


# ---------------------------------------------------------------------------------------------------------------
# Deposits
def _open_day(r, q):
    a, b = W.q_start(q), W.q_end(q)
    while True:
        d = a + dt.timedelta(days=int(r.integers(0, (b - a).days + 1)))
        if W.business_day(d) and not (d.month == 2 and d.day == 29):
            return d


def _principal(r, special=False):
    mu = 10.75 if not special else 10.95
    x = float(np.exp(r.normal(mu, 0.78)))
    x = min(max(x, 5000.0), 1500000.0)
    u = float(r.random())
    if u < 0.42:
        return float(round(x / 1000.0) * 1000)
    if u < 0.70:
        return float(round(x / 100.0) * 100)
    return round(x, 2)


def _locked(r, q, term, special_rate=None, principal=0.0):
    if special_rate is not None:    # a special is one rate for every amount and takes no other offer
        return round(special_rate, 2)
    base = W.card(q, term)
    prem = 0.10 if principal >= 250000 else 0.0
    exc = 0.0
    if r.random() < 0.07:
        exc = float(r.choice([0.05, 0.10, 0.15], p=[.45, .35, .20]))
    return round(base + prem + exc, 2)


def new_deposit(Wd, r, holder, term, rate, principal, opened, kind, standing=None, chain_from=None):
    body = Wd.next_acct
    Wd.next_acct += int(r.integers(7, 97))
    suffix = str(r.choice(W.TD_SUFFIXES, p=[.55, .2, .1, .07, .05, .03]))
    d = dict(body=body, suffix=suffix, holder=holder, term=term, rate=rate, principal=principal, opened=opened,
             maturity=add_years(opened, term), kind=kind, standing=standing, chain_from=chain_from,
             interest=str(r.choice(["At maturity", "Quarterly", "Annually", "Monthly"], p=[.62, .20, .12, .06])),
             joint=None, status="open", history=[], special=(kind == "special"))
    d["acct"] = W.acct_plain(body, suffix)
    d["acct_dashed"] = W.acct_dashed(body, suffix)
    if r.random() < 0.16:
        d["joint"] = "pending"
    Wd.deposits[d["acct"]] = d
    return d


def _age_for(r, term, special):
    mean = 58 + 2.2 * (term - 1) + (5 if special else 0)
    return float(np.clip(r.normal(mean, 13.5), 21, 94))


def _holder(Wd, r, term, special, quarter):
    """A member for a new deposit: mostly a new member, sometimes one who already holds deposits (never one whose
    deposit matures in the same quarter, so a list carries one deposit per member as the procedure cuts it, apart from
    the planned members with two)."""
    if Wd.cust_pool and r.random() < 0.22:
        for _ in range(6):
            c = Wd.cust_pool[int(r.integers(0, len(Wd.cust_pool)))]
            if quarter not in Wd.cust_quarters.get(c, set()):
                Wd.cust_quarters.setdefault(c, set()).add(quarter)
                return c
    c = make_customer(Wd, r, _age_for(r, term, special))["cust"]
    Wd.cust_pool.append(c)
    Wd.cust_quarters.setdefault(c, set()).add(quarter)
    return c


SPECIAL_SALES = (0.184, 0.408, 0.408)     # the 2023 special's sales by month, January (from the 16th) to March


def seed_book(Wd):
    """Synthetic cohorts opened before 2025 that mature from 2025Q1 to 2027Q1, the specials among them, and the new
    money of the window quarters (one random stream for each, so the special's sales calendar moves nothing else)."""
    r = W.rng("book")
    for mq, terms in SYN.items():
        for term, n in terms.items():
            oq = W.q_add(mq, -4 * term)
            sp = W.SPECIALS.get((oq, term))
            for _ in range(n):
                special = sp is not None and r.random() < sp[1]
                pr = _principal(r, special)
                rate = _locked(r, oq, term, sp[0] if special else None, pr)
                standing = "PAY" if r.random() < 0.075 else None
                h = _holder(Wd, r, term, special, mq)
                new_deposit(Wd, r, h, term, rate, pr, _open_day(r, oq), "special" if special else "std", standing)
    # the 2023 four-year special, sold from its launch on 16 January to 31 March 2023
    rs = W.rng("book-special")
    days = {1: [], 2: [], 3: []}
    d = dt.date(2023, 1, 16)
    while d <= dt.date(2023, 3, 31):
        if W.business_day(d):
            days[d.month].append(d)
        d += dt.timedelta(days=1)
    w = np.array(SPECIAL_SALES)
    for _ in range(SPECIAL_2023Q1):
        pr = _principal(rs, True)
        rate = _locked(rs, "2023Q1", 4, 5.65, pr)
        standing = "PAY" if rs.random() < 0.06 else None
        h = _holder(Wd, rs, 4, True, "2027Q1")
        mth = 1 + int(rs.choice(3, p=w / w.sum()))
        day = days[mth][int(rs.integers(0, len(days[mth])))]
        new_deposit(Wd, rs, h, 4, rate, pr, day, "special", standing)
    rn = W.rng("book-new")
    for (oq, term), n in NEW_MONEY.items():
        sp = W.WINDOW_SPECIALS.get((oq, term))
        for _ in range(n):
            special = sp is not None and rn.random() < sp[1]
            pr = _principal(rn, special)
            rate = _locked(rn, oq, term, sp[0] if special else None, pr)
            standing = "PAY" if rn.random() < 0.07 else None
            h = _holder(Wd, rn, term, special, W.q_add(oq, 4 * term))
            new_deposit(Wd, rn, h, term, rate, pr, _open_day(rn, oq), "special" if special else "new", standing)


def second_deposits(Wd):
    """About one member in thirty on a list holds a second deposit maturing in the same quarter: the procedure lists the
    larger and the agent covers the other in the same conversation."""
    r = W.rng("second")
    by_q = {}
    for d in list(Wd.deposits.values()):
        by_q.setdefault(W.q_of(d["maturity"]), []).append(d)
    for q, ds in sorted(by_q.items()):
        if q not in W.PAST and q != W.FWD:
            continue
        picks = [d for d in ds if r.random() < 0.03]
        for d in picks:
            term = int(r.choice([1, 2, 3], p=[.5, .3, .2]))
            oq = W.q_add(q, -4 * term)
            if oq >= "2025Q1" and (oq, term) not in NEW_MONEY:
                continue
            opened = _open_day(r, oq)
            mat = add_years(opened, term)
            if W.q_of(mat) != q:
                continue
            pr = round(min(d["principal"] * float(r.uniform(0.15, 0.8)), d["principal"] - 100), 2)
            if pr < 5000:
                continue
            new_deposit(Wd, r, d["holder"], term, _locked(r, oq, term, None, pr), pr, opened, "second")


# ---------------------------------------------------------------------------------------------------------------
# A campaign: the list, release, dialling and close-out
def make_list(Wd, q):
    cut = W.CUTS[q]
    mat = [d for d in Wd.deposits.values() if d["status"] == "open" and W.q_of(d["maturity"]) == q]
    elig = [d for d in mat if d["principal"] >= LIST_MIN and d["standing"] is None]
    best = {}
    for d in elig:
        h = d["holder"]
        if h not in best or (d["principal"], d["acct"]) > (best[h]["principal"], best[h]["acct"]):
            best[h] = d
    listed = sorted(best.values(), key=lambda d: (d["maturity"], d["acct"]))
    return mat, listed


def _choose(r, pairs):
    u = float(r.random())
    acc = 0.0
    for k, p in pairs:
        acc += p
        if u < acc:
            return k
    return pairs[-1][0]


def run_case(Wd, r, dep, q, release, case_ref):
    """Dial one released case under the SOW's rules; returns the dial rows and the close-out."""
    cust = Wd.customers[dep["holder"]]
    nums = [ph for ph in cust["phones"] if callable_on(ph, release)]
    days = W.dialling_days(release, dep["maturity"])
    assert len(days) >= W.DIALS_PER_NUMBER, (dep["acct"], release, len(days))
    drop = round(dep["rate"] - W.card(q, dep["term"]), 2)
    open_ = [dict(ph=ph, slot=i + 1, fails=0, done=False) for i, ph in enumerate(nums)]
    dials, seq = [], 0
    outcome, closed_on, reason = None, None, None
    for day in days:
        if r.random() < W.WITHDRAW_PER_DAY:
            closed_on, reason = day, "WITHDRAWN"
            break
        live = [n for n in open_ if not n["done"]]
        if not live:
            break
        # first dial of the day between 9 am and late afternoon, numbers a few minutes apart
        local = dt.datetime.combine(day, dt.time(9, 0)) + dt.timedelta(minutes=int(r.integers(0, 540)))
        for n in live:
            seq += 1
            ph = n["ph"]
            if ph["state"] == "D":
                code, talk = W.DEAD_CODE, 0
                n["done"] = True
            else:
                answered = r.random() < W.P_ANSWER[ph["kind"]]
                if answered and ph["state"] == "X":
                    code, talk = W.WRONG_CODE, int(r.integers(25, 140))
                    n["done"] = True
                elif answered:
                    if r.random() < W.p_retention(drop, dep.get("special", False)):
                        code = "RTK" if r.random() < W.RETENTION_KEPT else "RTW"
                        talk = int(np.clip(r.normal(1020, 260), 420, 2400))
                    else:
                        code = _choose(r, W.PLAIN)
                        talk = int(np.clip(r.normal(330 if code != "DEC" else 120, 90), 40, 1100))
                else:
                    code, talk = _choose(r, W.NONANSWER), 0
                    n["fails"] += 1
                    if n["fails"] >= W.DIALS_PER_NUMBER:
                        n["done"] = True
            dials.append(dict(seq=seq, local=local, e164=ph["e164"], slot=n["slot"], code=code, talk=talk))
            local += dt.timedelta(minutes=int(r.integers(2, 9)))
            if code in W.CONVERSATION or code in W.RETENTION:
                outcome, closed_on, reason = code, day, "CONVERSATION"
                break
        if outcome:
            break
        if all(n["done"] for n in open_):
            closed_on, reason = day, "EXHAUSTED"
            break
    if reason is None:
        closed_on, reason = days[-1], "MATURED"
    return dials, dict(case_ref=case_ref, closed_on=closed_on, reason=reason, outcome=outcome,
                       callable=[(n["slot"], n["ph"]) for n in open_], drop=drop,
                       special=bool(dep.get("special", False)), term=dep["term"], rate=dep["rate"])


# ---------------------------------------------------------------------------------------------------------------
# What a deposit does at maturity
OUTCOME_P = {
    "RNW": (("SAME", 1.0),),
    "CHG": (("NEW", 0.85), ("PAY_SAV", 0.15)),
    "DEC": (("SAME", 0.75), ("NEW", 0.10), ("PAY_SAV", 0.10), ("PAY_EXT", 0.05)),
    "RTK": (("SAME", 0.70), ("NEW", 0.30)),
    "RTW": (("PAY_EXT", 0.65), ("PAY_SAV", 0.25), ("NEW", 0.10)),
    "NONE": (("SAME", 0.82), ("NEW", 0.06), ("PAY_SAV", 0.06), ("PAY_EXT", 0.06)),
    "INSTR": (("NEW", 0.35), ("PAY_SAV", 0.30), ("PAY_EXT", 0.20), ("SAME", 0.15)),
    "PAYSTAND": (("PAY_SAV", 0.55), ("PAY_EXT", 0.45)),
    "UNLISTED": (("SAME", 0.74), ("NEW", 0.08), ("PAY_SAV", 0.12), ("PAY_EXT", 0.06)),
}


def ext_account(r):
    bank = str(r.choice(["12", "01", "02", "03", "06", "38", "15", "30"], p=[.2, .2, .15, .15, .1, .1, .05, .05]))
    return "%s-%04d-%07d-%02d" % (bank, int(r.integers(1, 9999)), int(r.integers(1, 9999999)), int(r.integers(0, 99)))


def savings_of(Wd, r, cust):
    c = Wd.customers[cust]
    if c["savings"] is None:
        body = Wd.next_sav
        Wd.next_sav += int(r.integers(11, 131))
        c["savings"] = W.acct_plain(body, str(r.choice(W.SAV_SUFFIXES, p=[.7, .2, .1])))
    return c["savings"]


def settle(Wd, r, dep, cls, uplift=0.0, listed=False, mq=None):
    """Apply a maturity outcome: events, transfers, and the deposit carried on (same account or new)."""
    m = dep["maturity"]
    q = mq or W.q_of(m)
    ev, tr = Wd.events, Wd.transfers
    track = listed or dep["acct"] in Wd.tracked
    sav = savings_of(Wd, r, dep["holder"])
    interest = round(dep["principal"] * dep["rate"] / 100.0 * (dep["term"] if dep["interest"] == "At maturity" else
                                                                {"Quarterly": 0.25, "Annually": 1.0, "Monthly": 1 / 12.0}[dep["interest"]]), 2)
    if track:
        ev.append((dep["acct"], m, "MATURE", dep["principal"], "", "", ""))
    out = dict(cls=cls, same=None, new=[], amount_kept=0.0)
    if cls == "SAME":
        dep["special"] = False
        dep["rate"] = round(W.card(q, dep["term"]) + uplift, 2)
        dep["opened"] = m
        dep["maturity"] = add_years(m, dep["term"])
        dep["history"].append(("REINVEST", m))
        if track:
            ev.append((dep["acct"], m, "REINVEST", dep["principal"], dep["term"] * 12, "%.2f" % dep["rate"],
                       dep["maturity"].isoformat()))
        out["same"] = dep
        out["amount_kept"] = dep["principal"]
    elif cls == "NEW":
        full = r.random() < 0.55
        amt = dep["principal"] if full else round(dep["principal"] * float(r.uniform(0.4, 0.9)) / 100.0) * 100.0
        amt = min(amt, dep["principal"])
        t2 = dep["term"] if (not full and r.random() < 0.3) else int(r.choice([t for t in W.TERMS if t != dep["term"]]))
        rate = round(W.card(q, t2) + uplift, 2)
        nd = new_deposit(Wd, r, dep["holder"], t2, rate, amt, m, "reinvested", chain_from=dep["acct"])
        nd["joint"] = dep["joint"]
        top = 0.0
        if r.random() < 0.12:
            top = float(round(float(r.uniform(2000, 60000)) / 500.0) * 500.0)
            nd["principal"] = round(amt + top, 2)
        if track:
            Wd.tracked.add(nd["acct"])
            ev.append((dep["acct"], m, "PAYOUT", dep["principal"], "", "", ""))
            ev.append((dep["acct"], m, "CLOSE", 0.0, "", "", ""))
            ev.append((nd["acct"], m, "OPEN", nd["principal"], t2 * 12, "%.2f" % rate, nd["maturity"].isoformat()))
            tr.append((m, dep["acct"], nd["acct"], amt, "MATURITY PROCEEDS"))
            if dep["principal"] - amt > 0.005:
                tr.append((m, dep["acct"], sav, round(dep["principal"] - amt, 2), "MATURITY PROCEEDS"))
                out["partial"] = dict(ev_open=len(ev) - 1, tr_new=len(tr) - 2, tr_sav=len(tr) - 1, nd=nd, amt=amt,
                                      prin=dep["principal"])
            if top:
                r.integers(0, 2)        # (a draw kept so the outcome stream is unchanged; the top-up lands on the day)
                tr.append((m, ext_account(r), nd["acct"], top, "DEPOSIT"))
        dep["status"] = "closed"
        out["new"].append(nd)
        out["amount_kept"] = amt
    else:
        dest = sav if cls == "PAY_SAV" else ext_account(r)
        if track:
            ev.append((dep["acct"], m, "PAYOUT", dep["principal"], "", "", ""))
            ev.append((dep["acct"], m, "CLOSE", 0.0, "", "", ""))
            tr.append((m, dep["acct"], dest, dep["principal"], "MATURITY PROCEEDS"))
        dep["status"] = "closed"
    # a reinvested deposit broken early inside the month after maturity (days 3 to 24 only)
    kept = out["same"] or (out["new"][0] if out["new"] else None)
    if kept is not None and r.random() < 0.018:
        bday = m + dt.timedelta(days=int(r.integers(3, 25)))
        if track:
            ev.append((kept["acct"], bday, "BREAK", kept["principal"], "", "", ""))
            ev.append((kept["acct"], bday, "CLOSE", 0.0, "", "", ""))
            tr.append((bday, kept["acct"], sav, kept["principal"], "EARLY WITHDRAWAL"))
        kept["status"] = "closed"
        out["broken"] = bday
        out["amount_kept"] = 0.0
    return out


def nudge_kept(Wd, q, clear=150.0):
    """Keep a closed campaign's principal still on term deposit 30 days after maturity clear of a thousand-dollar
    rounding edge: if it sits within NZ$150 of one, the first partial change of term on the list (by account) that was
    not broken moves a multiple of NZ$100 between the new deposit and the savings payment (its rows rewritten)."""
    camp = Wd.campaigns[q]
    kept = sum(res["amount_kept"] for res in camp["outcomes"].values())

    def room(x):
        return abs((x % 1000.0) - 500.0)
    if room(kept) >= clear:
        return 0.0
    cands = sorted((a, res) for a, res in camp["outcomes"].items() if res.get("partial") and not res.get("broken"))
    for a, res in cands:
        pa = res["partial"]
        for s in sorted(range(-900, 901, 100), key=lambda x: (abs(x), x)):
            if s == 0 or not (500 <= pa["amt"] + s <= pa["prin"] - 500):
                continue
            if room(kept + s) < clear:
                continue
            ev, tr = Wd.events, Wd.transfers
            nd = pa["nd"]
            nd["principal"] = round(nd["principal"] + s, 2)
            e = list(ev[pa["ev_open"]])
            e[3] = nd["principal"]
            ev[pa["ev_open"]] = tuple(e)
            x = list(tr[pa["tr_new"]])
            x[3] = round(pa["amt"] + s, 2)
            tr[pa["tr_new"]] = tuple(x)
            y = list(tr[pa["tr_sav"]])
            y[3] = round(pa["prin"] - pa["amt"] - s, 2)
            tr[pa["tr_sav"]] = tuple(y)
            res["amount_kept"] = round(pa["amt"] + s, 2)
            pa["amt"] = round(pa["amt"] + s, 2)
            return float(s)
    raise AssertionError("no partial change of term clears campaign %s" % q)


def fresh_money(Wd, r, dep, m):
    """A member who opens a new term deposit with money from another bank around the maturity m of a listed deposit."""
    day = m + dt.timedelta(days=int(r.integers(-10, 26)))
    while not W.business_day(day):
        day += dt.timedelta(days=1)
    term = int(r.choice(W.TERMS, p=[.4, .25, .15, .08, .12]))
    pr = _principal(r)
    nd = new_deposit(Wd, r, dep["holder"], term, _locked(r, W.q_of(day), term, None, pr), pr, day, "fresh")
    Wd.tracked.add(nd["acct"])
    Wd.events.append((nd["acct"], day, "OPEN", pr, term * 12, "%.2f" % nd["rate"], nd["maturity"].isoformat()))
    Wd.transfers.append((day, ext_account(r), nd["acct"], pr, "DEPOSIT"))
    return nd


def top_up_2022_five_year(Wd, have):
    """The rest of the five-year deposits opened in January to March 2022 that mature in January to March 2027, with
    members new to the window: enough to put the coming list at its cut size, and the small and instructed deposits
    of the same cohort beside them."""
    r = W.rng("topup-2022-5y")
    need = W.FWD_LIST_SIZE - have
    assert need > 0, have
    new_c = set()
    made = 0
    while made < need:
        pr = _principal(r)
        standing = "PAY" if r.random() < 0.075 else None
        c = make_customer(Wd, r, _age_for(r, 5, False))["cust"]
        new_c.add(c)
        new_deposit(Wd, r, c, 5, _locked(r, "2022Q1", 5, None, pr), pr, _open_day(r, "2022Q1"), "std", standing)
        if pr >= LIST_MIN and standing is None:
            made += 1
    register_entries(Wd, stream="register-topup", only=new_c)
    Wd.register.sort(key=lambda x: (x["added"], x["e164"]))


# ---------------------------------------------------------------------------------------------------------------
def simulate():
    Wd = World()
    Wd.customers, Wd.deposits = {}, {}
    Wd.next_cust, Wd.next_acct, Wd.next_sav = 4000127, 101113, 205017
    Wd.cust_pool, Wd.cust_quarters = [], {}
    Wd.events, Wd.transfers, Wd.tracked = [], [], set()
    Wd.campaigns = {}
    seed_book(Wd)
    second_deposits(Wd)
    register_entries(Wd)
    rc = W.rng("campaigns")
    ro = W.rng("outcomes")
    rf = W.rng("fresh")
    case_no = {}
    for q in qrange("2025Q1", "2027Q1"):
        mat, listed = make_list(Wd, q)
        listed_ids = {d["acct"] for d in listed}
        camp = dict(q=q, listed=[], released=[], dials=[], closeouts=[], outcomes={})
        if q in W.PAST:
            for d in listed:
                snap = dict(acct=d["acct"], acct_dashed=d["acct_dashed"], holder=d["holder"], term=d["term"],
                            rate=d["rate"], principal=d["principal"], opened=d["opened"], maturity=d["maturity"],
                            interest=d["interest"], branch=Wd.customers[d["holder"]]["branch"])
                camp["listed"].append(snap)
            for d in listed:
                release = d["maturity"] - dt.timedelta(days=21)
                cust = Wd.customers[d["holder"]]
                nums = [ph for ph in cust["phones"] if callable_on(ph, release)]
                status, reason = "RELEASED", ""
                if not nums:
                    status, reason = "NOT RELEASED", "NO CALLABLE NUMBER"
                elif rc.random() < W.PRE_RELEASE_INSTRUCTED:
                    status, reason = "NOT RELEASED", "INSTRUCTED"
                rel = dict(acct=d["acct"], release=release, status=status, reason=reason,
                           numbers=[(i + 1, ph) for i, ph in enumerate(nums)])
                camp["released"].append(rel)
                if status == "RELEASED":
                    case_no[q] = case_no.get(q, 0) + 1
                    ref = "HL%s%s-%06d" % (q[2:4], q[-2:], 300000 + case_no[q] * 7 + int(rc.integers(0, 7)))
                    dials, co = run_case(Wd, rc, d, q, release, ref)
                    co["acct"], co["release"] = d["acct"], release
                    camp["dials"].append((ref, d["acct"], dials))
                    camp["closeouts"].append(co)
                    cls = co["outcome"] or ("INSTR" if co["reason"] == "WITHDRAWN" else "NONE")
                elif reason == "INSTRUCTED":
                    cls = "INSTR"
                else:
                    cls = "NONE"
                ckey = cls
                m0 = d["maturity"]
                uplift = 0.0
                if ckey == "RTK":
                    uplift = float(ro.choice([0.10, 0.15, 0.20, 0.25], p=[.2, .3, .3, .2])) if d["term"] <= 2 else \
                        float(ro.choice([0.05, 0.10, 0.15], p=[.3, .4, .3]))
                res = settle(Wd, ro, d, _choose(ro, OUTCOME_P[ckey]), uplift=uplift, listed=True, mq=q)
                res["case_class"] = ckey
                camp["outcomes"][d["acct"]] = res
                if rf.random() < 0.04:
                    fresh_money(Wd, rf, d, m0)
            for d in mat:
                if d["acct"] in listed_ids or d["status"] != "open":
                    continue
                cls = "PAYSTAND" if d["standing"] == "PAY" else "UNLISTED"
                settle(Wd, ro, d, _choose(ro, OUTCOME_P[cls]), listed=False, mq=q)
            Wd.campaigns[q] = camp
            nudge_kept(Wd, q)
        elif q == "2026Q4":
            for d in mat:
                if d["maturity"] > W.CUT_FWD or d["status"] != "open":
                    continue
                cls = "PAYSTAND" if d["standing"] == "PAY" else "UNLISTED"
                settle(Wd, ro, d, _choose(ro, OUTCOME_P[cls]), listed=False, mq=q)
        else:   # 2027Q1, the coming list: the 2022 five-year cohort completes it
            top_up_2022_five_year(Wd, len(listed))
            mat, listed = make_list(Wd, q)
            assert len(listed) == W.FWD_LIST_SIZE, len(listed)
            camp["listed"] = listed
            camp["maturing"] = mat
        Wd.campaigns[q] = camp
    return Wd
