"""The insurer's retirement income book as its own systems hold it, for the asks: the client register (pulled 12 January
2027), the Retirement Income Account pensions open at 31 December 2026 with their nominations, and the lifetime annuity
lives listing pulled 12 January 2027 for the 31 December valuation. Every person is drawn with the truth the records
only partly show: a partner who is not a client, a December death the fund learnt of in January, a January death, an
anniversary increase applied before the listing was pulled."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K

AS_AT = K.AS_AT
PULL = K.PULL
JAN_RATE = {"CPI": 0.031, "Fixed 2.5%": 0.025, "Level": 0.0}   # the increase on anniversaries from November 2026
OLDER = K.OLDER
MIN_DRAW = [(65, 0.04), (75, 0.05), (80, 0.06), (85, 0.07), (90, 0.09), (95, 0.11), (200, 0.14)]


def age_at(dob, d=AS_AT):
    return d.year - dob.year - ((d.month, d.day) < (dob.month, dob.day))


def rand_date(r, lo, hi):
    return lo + dt.timedelta(days=int(r.integers(0, (hi - lo).days + 1)))


def dob_for_age(r, age, d=AS_AT):
    """A date of birth giving this age at d."""
    hi = dt.date(d.year - age, d.month, d.day)
    lo = dt.date(d.year - age - 1, d.month, d.day) + dt.timedelta(days=1)
    return rand_date(r, lo, hi)


class Book:
    """Persons, households (truth), pension accounts, nominations and annuity contracts."""

    def __init__(self):
        self.P = []          # persons
        self.acc = []        # pension accounts open in the fund's system at 31 December 2026
        self.nom = []        # nominations current at 31 December 2026
        self.ann = []        # annuity contracts in the valuation listing
        self.hh_true = {}    # pid -> partner pid at 31 December 2026 (truth, living partners only)

    def person(self, r, age, sex, client, since=None, dod=None, notified=None, kind="retirement"):
        pid = len(self.P)
        self.P.append(dict(pid=pid, dob=dob_for_age(r, age), sex=sex, client=client, since=since, dod=dod,
                           notified=notified, kind=kind, hh=None, merged_from=None, name=None))
        return pid


def draw_age(r, n):
    ages = np.arange(56, 96)
    w = np.exp(-0.5 * ((ages - 69.5) / 7.8) ** 2) * np.where(ages < 60, 0.45, 1.0)
    return r.choice(ages, n, p=w / w.sum())


def build():
    r = K.rng("insurer-book")
    B = Book()
    since_lo, since_hi = dt.date(1998, 1, 1), dt.date(2026, 6, 30)
    N = 2700
    a1 = draw_age(r, N)
    for i in range(N):
        age1 = int(a1[i])
        sex1 = "M" if r.random() < 0.49 else "F"
        p1 = B.person(r, age1, sex1, True, rand_date(r, since_lo, since_hi))
        has_pen = r.random() < 0.86
        has_ann = r.random() < (0.30 if has_pen else 1.0)
        couple = r.random() < (0.66 if age1 < 75 else 0.48)
        partner, pcat = None, None
        if couple:
            u = r.random()
            pcat = "client" if u < 0.45 else ("named" if (u < 0.78 and has_pen) else "unrecorded")
            gap = int(round(r.normal(-1.0, 4.6)))
            if pcat == "unrecorded" and K.band_of(age1 + max(gap, 0)) != K.band_of(age1):
                gap = min(gap, 0)          # a partner the records never name never moves the placement
            age2 = int(np.clip(age1 + gap, 50, 97))
            sex2 = ("F" if sex1 == "M" else "M") if r.random() > 0.012 else sex1
            partner = B.person(r, age2, sex2, pcat == "client",
                               rand_date(r, since_lo, since_hi) if pcat == "client" else None)
            B.hh_true[p1] = partner
            B.hh_true[partner] = p1
        B.P[p1]["pcat"] = pcat
        if partner is not None:
            B.P[partner]["pcat"] = pcat
        if has_pen:
            add_pension(B, r, p1, partner, pcat)
        if has_ann:
            add_annuity(B, r, p1, partner, pcat)
        if partner is not None and B.P[partner]["client"] and age_at(B.P[partner]["dob"]) >= 57 and r.random() < 0.50:
            add_pension(B, r, partner, p1, "client")
    return B


def add_pension(B, r, owner, partner, pcat):
    age = age_at(B.P[owner]["dob"])
    ttr = age < 65 and r.random() < 0.22
    lvl = [330, 330, 330, 330, 300, 215][K.band_of(age)] * 1000
    bal = round(float(np.exp(np.log(lvl) + r.normal(0, 0.72))), 2)
    lo = dt.date(max(2007, B.P[owner]["dob"].year + 56), 1, 1)
    start = rand_date(r, min(lo, dt.date(2026, 1, 1)), dt.date(2026, 11, 30))
    rate = 0.07 if ttr else next(v for lim, v in MIN_DRAW if age_at(B.P[owner]["dob"], dt.date(2026, 7, 1)) < lim) \
        + float(r.choice([0, 0, 0.01, 0.02]))
    acc = dict(account=None, owner=owner, owner_id=None, type="TTR" if ttr else "ABP", commenced=start,
               balance=bal, freq=r.choice(["Monthly", "Fortnightly", "Quarterly", "Annually"], p=[.62, .18, .14, .06]),
               reverted_from=None, payment=round(bal * rate * 1.03, -1))
    B.acc.append(acc)
    k = len(B.acc) - 1
    # nominations: the partner where the records name one, else children, the estate or none
    if partner is not None and (pcat == "named" or (pcat == "client" and r.random() < 0.55)):
        kind = "Reversionary" if r.random() < 0.6 else r.choice(["Binding", "Non-lapsing binding", "Non-binding"])
        B.nom.append(dict(acc=k, kind=kind, person=partner, rel="Spouse" if r.random() < 0.8 else "De facto partner",
                          share=100))
    elif r.random() < 0.55:
        kids = int(r.integers(1, 4))
        kind = r.choice(["Binding", "Non-lapsing binding", "Non-binding"])
        for j in range(kids):
            B.nom.append(dict(acc=k, kind=kind, person=None, rel="Child",
                              child_age=int(np.clip(age - r.integers(24, 38), 18, 70)),
                              share=[100, 50, 34][kids - 1] if j == 0 else [0, 50, 33][kids - 1]))
    elif r.random() < 0.3:
        B.nom.append(dict(acc=k, kind="Binding", person=None, rel="Legal personal representative", share=100))
    return k


def add_annuity(B, r, life1, partner, pcat):
    age = age_at(B.P[life1]["dob"])
    rev = partner is not None and r.random() < 0.45
    if rev and not B.P[partner]["client"]:
        # the life company opens a client record for every life on a contract
        B.P[partner]["client"] = True
        B.P[partner]["since"] = None      # set from the contract below
        if B.P[life1].get("pcat") in ("named", "unrecorded"):
            B.P[life1]["pcat"] = "client"
    lo = dt.date(max(2008, B.P[life1]["dob"].year + 58), 1, 1)
    start = rand_date(r, min(lo, dt.date(2026, 1, 1)), dt.date(2026, 12, 20))
    if rev and B.P[partner]["since"] is None:
        B.P[partner]["since"] = start
    idx = r.choice(["CPI", "Fixed 2.5%", "Level"], p=[.55, .15, .30])
    amt = round(float(np.exp(np.log(17000) + r.normal(0, 0.55))), 2)
    pay_from = None
    if age <= 76 and r.random() < 0.11:
        # a deferred lifetime annuity: bought now, its income starts at 80 or 85
        pay_from = dt.date(B.P[life1]["dob"].year + int(r.choice([80, 85])), B.P[life1]["dob"].month, 1)
        amt = round(amt * 1.9, 2)
    B.ann.append(dict(contract=None, life1=life1, life2=partner if rev else None, commenced=start, index=idx,
                      freq=r.choice(["Monthly", "Quarterly", "Half-yearly", "Yearly"], p=[.66, .2, .06, .08]),
                      amount=amt, pct=int(r.choice(np.arange(50, 95, 5))) if rev else None, pay_from=pay_from))


# ---------------------------------------------------------------------------------------------- events
def alive(B, p, d=AS_AT):
    return B.P[p]["dod"] is None or B.P[p]["dod"] > d


def nominations_of(B, k):
    return [n for n in B.nom if n["acc"] == k]


def reversionary_of(B, k):
    rv = [n for n in B.nom if n["acc"] == k and n["kind"] == "Reversionary"]
    return rv[0] if rv else None


def events(B):
    """Deaths through 2026 and early January 2027 as the fund and the life company recorded them."""
    r = K.rng("insurer-events")
    used = set()

    def pick(cands, n):
        cands = [c for c in cands if c not in used]
        out = [cands[i] for i in r.permutation(len(cands))[:n]]
        used.update(out)
        return out

    owners = {}
    for k, a in enumerate(B.acc):
        owners.setdefault(a["owner"], []).append(k)
    single_acc = [k for k, a in enumerate(B.acc) if len(owners[a["owner"]]) == 1]
    rev_nc = [k for k in single_acc if reversionary_of(B, k) is not None and reversionary_of(B, k)["person"] is not None
              and not B.P[reversionary_of(B, k)["person"]]["client"]]
    rev_c = [k for k in single_acc if reversionary_of(B, k) is not None and reversionary_of(B, k)["person"] is not None
             and B.P[reversionary_of(B, k)["person"]]["client"]]
    no_rev = [k for k in single_acc if reversionary_of(B, k) is None]
    ann_owner = {c["life1"] for c in B.ann} | {c["life2"] for c in B.ann if c["life2"] is not None}

    def die(p, lo, hi, nlo, nhi):
        B.P[p]["dod"] = rand_date(r, lo, hi)
        B.P[p]["notified"] = max(B.P[p]["dod"] + dt.timedelta(days=3), rand_date(r, nlo, nhi))

    # 1. 2026 deaths the fund processed in 2026: a reversion opens the survivor's own account from the date of death
    for k in pick([x for x in rev_nc + rev_c if B.P[B.acc[x]["owner"]]["pid"] not in ann_owner], 46):
        o = B.acc[k]["owner"]
        die(o, dt.date(2026, 1, 10), dt.date(2026, 10, 31), dt.date(2026, 1, 20), dt.date(2026, 11, 30))
        sv = reversionary_of(B, k)["person"]
        if not B.P[sv]["client"]:
            B.P[sv]["client"] = True
            B.P[sv]["since"] = B.P[o]["notified"] + dt.timedelta(days=int(r.integers(5, 25)))
            B.P[sv]["joined_by_reversion"] = True
        a = B.acc[k]
        B.acc[k] = dict(a, owner=sv, commenced=B.P[o]["dod"], reverted_from=o)
        B.nom = [n for n in B.nom if n["acc"] != k]
    for k in pick([x for x in no_rev if B.acc[x]["owner"] not in ann_owner], 38):
        o = B.acc[k]["owner"]
        die(o, dt.date(2026, 1, 10), dt.date(2026, 10, 31), dt.date(2026, 1, 20), dt.date(2026, 11, 30))
        B.acc[k]["closed"] = True                       # paid as a death benefit before 31 December
    # 2. December 2026 deaths the fund learnt of in January 2027: still open under the deceased at 31 December
    pend = dict(rnc=pick([x for x in rev_nc if B.acc[x]["owner"] not in ann_owner], 9),
                rc=pick([x for x in rev_c if B.acc[x]["owner"] not in ann_owner], 5),
                db=pick([x for x in no_rev if B.acc[x]["owner"] not in ann_owner], 9))
    for grp, ks in pend.items():
        for k in ks:
            o = B.acc[k]["owner"]
            die(o, dt.date(2026, 12, 4), dt.date(2026, 12, 29), dt.date(2027, 1, 4), dt.date(2027, 1, 11))
            if grp == "rnc":
                sv = reversionary_of(B, k)["person"]
                B.P[sv]["client"] = True
                B.P[sv]["since"] = B.P[o]["notified"] + dt.timedelta(days=1)
                B.P[sv]["joined_by_reversion"] = True
    B.pending = pend
    # 3. January 2027 deaths, after the 31 December snapshot and before the pulls
    jan_owner = pick([a["owner"] for a in B.acc if not a.get("closed") and alive(B, a["owner"])
                      and a["owner"] not in ann_owner], 8)
    jan_partner = pick([p for p in B.hh_true if B.P[p]["client"] and p not in owners and p not in ann_owner
                        and alive(B, p) and alive(B, B.hh_true[p])
                        and age_at(B.P[p]["dob"]) > age_at(B.P[B.hh_true[p]]["dob"])], 5)
    for p in jan_owner + jan_partner:
        die(p, dt.date(2027, 1, 1), dt.date(2027, 1, 9), dt.date(2027, 1, 5), dt.date(2027, 1, 11))
    B.jan_deaths = jan_owner + jan_partner
    # 4. annuitants: deaths through 2026, a few in December learnt of in January, a few in January
    single = [c["life1"] for c in B.ann if c["life2"] is None]
    revl1 = [c["life1"] for c in B.ann if c["life2"] is not None]
    for p in pick(single, 30) + pick(revl1, 16):
        die(p, dt.date(2026, 1, 10), dt.date(2026, 11, 20), dt.date(2026, 1, 20), dt.date(2026, 12, 10))
    for p in pick(single, 3) + pick(revl1, 2):
        die(p, dt.date(2026, 12, 4), dt.date(2026, 12, 29), dt.date(2027, 1, 4), dt.date(2027, 1, 11))
    jan_ann = pick(single, 4) + pick(revl1, 4)
    for p in jan_ann:
        die(p, dt.date(2027, 1, 1), dt.date(2027, 1, 9), dt.date(2027, 1, 5), dt.date(2027, 1, 11))
    B.jan_ann = jan_ann
    # a nomination naming a client the fund knew had died by 31 December has lapsed and is off the register
    B.nom = [n for n in B.nom if n["person"] is None or B.P[n["person"]]["dod"] is None
             or B.P[n["person"]]["notified"] > AS_AT]


def new_business(B):
    """Lifetime annuities that began in January 2027, before the listing was pulled."""
    r = K.rng("insurer-newbiz")
    for _ in range(14):
        age = int(r.integers(62, 84))
        p = B.person(r, age, "M" if r.random() < .5 else "F", True, rand_date(r, dt.date(2026, 11, 1), dt.date(2027, 1, 8)))
        B.P[p]["pcat"] = None
        B.ann.append(dict(contract=None, life1=p, life2=None, commenced=rand_date(r, dt.date(2027, 1, 2), dt.date(2027, 1, 11)),
                          index=r.choice(["CPI", "Fixed 2.5%", "Level"], p=[.55, .15, .30]), freq="Monthly",
                          amount=round(float(np.exp(np.log(17000) + r.normal(0, 0.5))), 2), pct=None, pay_from=None))


# ---------------------------------------------------------------------------------------------- the client register
def register(B):
    """Client and household identifiers, other clients, marital status as last recorded, and the 2026 merges."""
    r = K.rng("insurer-register")
    # the rest of the register: accumulation members and life cover clients of every age
    for _ in range(4300):
        age = int(np.clip(r.normal(46, 13), 19, 92))
        p = B.person(r, age, "M" if r.random() < .5 else "F", True, rand_date(r, dt.date(1998, 1, 1), dt.date(2026, 12, 15)),
                     kind="other")
        B.P[p]["pcat"] = None
        if r.random() < 0.42:
            q = B.person(r, int(np.clip(age + round(r.normal(-1, 4.5)), 18, 95)), "F" if B.P[p]["sex"] == "M" else "M", True,
                         rand_date(r, dt.date(1998, 1, 1), dt.date(2026, 12, 15)), kind="other")
            B.P[q]["pcat"] = "client"
            B.P[p]["pcat"] = "client"
            B.hh_true[p], B.hh_true[q] = q, p
        if r.random() < 0.012:
            B.P[p]["dod"] = rand_date(r, dt.date(2019, 1, 1), dt.date(2026, 11, 30))
            B.P[p]["notified"] = B.P[p]["dod"] + dt.timedelta(days=int(r.integers(5, 60)))
    # a client record opens when the person first takes a product, from 18
    for p in B.P:
        if p["client"] and p["since"] is not None:
            adult = dt.date(p["dob"].year + 18, p["dob"].month, min(p["dob"].day, 28))
            if p["since"] < adult:
                p["since"] = adult + dt.timedelta(days=int(r.integers(0, 2000)))
                if p["since"] > dt.date(2026, 12, 15):
                    p["since"] = dt.date(2026, 12, 15) - dt.timedelta(days=int(r.integers(0, 300)))
    ids = r.permutation(np.arange(1000000, 9999999, 37))[:len(B.P) + 200]
    hids = r.permutation(np.arange(100000, 999999, 7))[:len(B.P) + 200]
    nh = iter(hids)
    for p in B.P:
        p["client_id"] = "C%07d" % ids[p["pid"]] if p["client"] else None
    for p in B.P:
        if not p["client"] or p["hh"] is not None:
            continue
        p["hh"] = "H%06d" % next(nh)
        q = B.hh_true.get(p["pid"])
        if q is not None and B.P[q]["client"] and not p.get("joined_by_reversion") and not B.P[q].get("joined_by_reversion"):
            B.P[q]["hh"] = p["hh"]
    # a survivor who joined when the fund processed a 2026 reversion is filed in the member's household; one who
    # joined in January 2027 gets a household of their own
    for p in B.P:
        if p.get("joined_by_reversion"):
            q = B.hh_true.get(p["pid"])
            if p["since"] is not None and p["since"] <= AS_AT and q is not None and B.P[q]["hh"]:
                p["hh"] = B.P[q]["hh"]
            elif p["hh"] is None:
                p["hh"] = "H%06d" % next(nh)
    # marital status as last recorded
    for p in B.P:
        if not p["client"]:
            continue
        q = B.hh_true.get(p["pid"])
        if q is None:
            p["marital"] = r.choice(["Single", "Widowed", "Divorced", "Separated"], p=[.35, .35, .2, .1]) \
                if age_at(p["dob"]) >= 55 else r.choice(["Single", "Divorced", "Separated"], p=[.7, .2, .1])
        elif B.P[q]["dod"] is not None and B.P[q]["notified"] is not None and B.P[q]["notified"] <= PULL:
            p["marital"] = "Widowed" if r.random() < 0.5 else "Married"
        else:
            p["marital"] = "Married" if r.random() < 0.82 else "De facto"
    # 2026 merges: a duplicate record raised when a second product was opened, retired into the original; the fund's
    # system still holds the retired number on the pension
    owners = [a["owner"] for a in B.acc if not a.get("closed")]
    pool = sorted(set(o for o in owners if B.P[o]["dod"] is None and not B.P[o].get("joined_by_reversion")))
    k = 0
    B.retired = []
    for o in [pool[i] for i in r.permutation(len(pool))[:26]]:
        old = dict(B.P[o])
        old.update(client_id="C%07d" % ids[len(B.P) + k], hh="H%06d" % next(nh), status="Merged",
                   merged_into=B.P[o]["client_id"], merged_on=rand_date(r, dt.date(2026, 2, 1), dt.date(2026, 11, 30)))
        B.retired.append(old)
        for a in B.acc:
            if a["owner"] == o:
                a["owner_id"] = old["client_id"]
        k += 1
    for a in B.acc:
        if a["owner_id"] is None:
            a["owner_id"] = B.P[a["owner"]]["client_id"]
    # numbers
    an = r.permutation(np.arange(4000000, 9999999, 61))
    for i, a in enumerate(B.acc):
        a["account"] = "RIA%07d" % an[i]
    cn = r.permutation(np.arange(100000, 999999, 13))
    for i, c in enumerate(B.ann):
        c["contract"] = "LA%06d" % cn[i]


# ---------------------------------------------------------------------------------------------- truth and routes
def jan_indexed(c):
    """The contract's January 2027 anniversary fell on or before the pull."""
    s = c["commenced"]
    return s.month == 1 and s.day <= PULL.day and s.year <= 2026


def anniversary_2027(c):
    return dt.date(2027, 1, c["commenced"].day) if jan_indexed(c) else None


def amount_at_pull(c, dod=None):
    """The listed annual amount: the January 2027 anniversary increase applies when the life was still alive on it."""
    ann = anniversary_2027(c)
    if ann is None or (dod is not None and dod <= ann):
        return round(c["amount"], 2)
    return round(c["amount"] * (1 + JAN_RATE[c["index"]]), 2)


def placed(B, members):
    return int(K.band_of(max(age_at(B.P[m]["dob"]) for m in members)))


def golden(B):
    """The asks on the generator's truth: holders at 31 December 2026, households of the holder and their living
    partner, placed by the older; the annuity in payment at 31 December at its 31 December rate."""
    A = {g: dict(hh=set(), bal=0.0, rev=set(), pay=0.0) for g in range(6)}
    for k, a in enumerate(B.acc):
        if a.get("closed"):
            continue
        o = a["owner"]
        rv = reversionary_of(B, k)
        if alive(B, o):
            holder, has_rev = o, rv is not None
        elif rv is not None and rv["person"] is not None and alive(B, rv["person"]):
            holder, has_rev = rv["person"], False
        else:
            continue
        q = B.hh_true.get(holder)
        mem = [holder] + ([q] if q is not None and alive(B, q) else [])
        g = placed(B, mem)
        key = frozenset(mem)
        A[g]["hh"].add(key)
        A[g]["bal"] += a["balance"]
        A[g]["pay"] += a["payment"]
        if has_rev:
            A[g]["rev"].add(key)
    Bn = {g: 0.0 for g in range(6)}
    Bh = {g: set() for g in range(6)}
    for c in B.ann:
        if c["commenced"] > AS_AT or (c["pay_from"] is not None and c["pay_from"] > AS_AT):
            continue
        l1, l2 = c["life1"], c["life2"]
        if alive(B, l1):
            pay, amt = l1, c["amount"]
            q = l2 if (l2 is not None and alive(B, l2)) else B.hh_true.get(l1)
        elif l2 is not None and alive(B, l2):
            pay, amt = l2, round(c["amount"] * c["pct"] / 100, 2)
            q = None
        else:
            continue
        mem = [pay] + ([q] if q is not None and alive(B, q) else [])
        Bn[placed(B, mem)] += amt
        Bh[placed(B, mem)].add(frozenset(mem))
    return A, Bn, Bh
