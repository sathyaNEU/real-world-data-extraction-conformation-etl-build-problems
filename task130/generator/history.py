"""Ownership over time for the watch-list stock.

The 30 June 2026 state comes from the plan; history back to 1 July 2024 is generated backwards from
it, and the second half of 2026 (deeds to 30 September, agreements in force on 30 June 2026, the
agency's commitments) forwards. Owners are holder ids, 'p:<NIF>' for private owners and 'AG' for the
housing agency.

Every transfer is one event: {date, refs, before{ref: owner}, after{ref: owner}, price, agreement}.
An agreement is a sale a large holder had signed before completion; it is what the returns schedule.
"""
import datetime as dt
import random

from common import D, SEED, CLOCK, workday, dni
from plan import SECTIONS, SETTLED_COMMITS, SETTLED_EARLY, Q_AGREED, TWIN_DATE, TWIN_PRICE

FREEZE = D(2025, 6, 30)        # carried holders transact nothing after this date
CARRIED = sorted({h for s in SECTIONS for h in s["carried"]})
BASE_PRICE = {"4625001005": 168000, "4625001012": 159000, "4625002007": 214000, "4625002019": 196000,
              "4625011004": 142000, "4625011016": 131000, "4625012009": 138000, "4625005013": 149000,
              "4625013021": 155000, "0301401008": 152000, "0301402014": 118000, "0301405003": 109000,
              "1204001006": 104000, "1204003011": 92000}


def blackout(d):
    """Dates no deed, agreed date or completion falls on: weekends, holidays, 21 to 30 September (so
    every deed executed by 30 September is registered by then) and 22 December to 6 January."""
    if not workday(d):
        return True
    if d.month == 9 and d.day >= 21:
        return True
    return (d.month == 12 and d.day >= 22) or (d.month == 1 and d.day <= 6)


def rand_day(rng, a, b, ok=lambda d: True):
    span = (b - a).days
    for _ in range(2000):
        d = a + dt.timedelta(days=rng.randrange(span + 1))
        if not blackout(d) and ok(d):
            return d
    raise RuntimeError(f"no admissible day in {a}..{b}")


class People:
    """Private owners and buyers: never on the register, never holding more than three dwellings."""

    def __init__(self, used, seed):
        self.rng = random.Random(seed)
        self.used = used

    def new(self):
        while True:
            n = dni(self.rng.randrange(19000000, 79999999))
            if n not in self.used:
                self.used.add(n)
                return "p:" + n


def price(rng, section):
    b = BASE_PRICE.get(section, 118000)
    return int(round(b * rng.uniform(0.78, 1.25) / 500.0)) * 500


class Book:
    def __init__(self):
        self.events = []
        self.agreements = []
        self.commitments = []   # the agency's first-offer commitments (ledger D lines)

    def agreement(self, **kw):
        kw["id"] = len(self.agreements) + 1
        self.agreements.append(kw)
        return kw

    def event(self, date, before, after, price, agreement=None, title="compravenda"):
        e = {"date": date, "refs": sorted(before), "before": dict(before), "after": dict(after),
             "price": price, "agreement": agreement["id"] if agreement else None, "title": title}
        self.events.append(e)
        return e


def allocate_june26(stock, people):
    """Owner of every watch dwelling on 30 June 2026, from the plan's holdings."""
    sections, buildings, dwellings = stock
    rng = random.Random(SEED * 13 + 5)
    state, reserved = {}, {}
    for s in SECTIONS:
        code = s["code"]
        parcels = list(sections[code]["parcels"])
        rng.shuffle(parcels)
        free = {p: list(buildings[p]["units"]) for p in parcels}
        if s["role"] == "U":
            big = next(p for p in parcels if len(free[p]) >= 18)
            reserved["U_building"] = free[big][:18]
            free[big] = free[big][18:]
        for h, n in sorted(s["hold"].items(), key=lambda kv: (-kv[1], kv[0])):
            k = s["carried"].get(h)
            if k:
                need = -(-n // k)
                pick = [p for p in parcels if len(free[p]) >= need][:k]
                assert len(pick) == k, (code, h)
                for i, p in enumerate(pick):
                    m = n // k + (1 if i < n % k else 0)
                    for ref in free[p][:m]:
                        state[ref] = h
                    free[p] = free[p][m:]
                continue
            left = n
            for p in parcels:
                if not left:
                    break
                tk = min(left, len(free[p]), rng.choice([2, 3, 4, 6, 8, 10, 12, 16]))
                for ref in free[p][:tk]:
                    state[ref] = h
                free[p] = free[p][tk:]
                left -= tk
            while left:
                p = next(p for p in parcels if free[p])
                state[free[p].pop(0)] = h
                left -= 1
        rest = [r for p in parcels for r in free[p]]
        rng.shuffle(rest)
        i = 0
        while i < len(rest):
            if rng.random() < 0.012:
                state[rest[i]] = "AG"
                i += 1
                continue
            o = people.new()
            m = 2 if rng.random() < 0.12 else 1
            for ref in rest[i:i + m]:
                state[ref] = o
            i += m
        if s["role"] == "U":
            sellers = [people.new() for _ in range(9)]
            for j, ref in enumerate(reserved["U_building"]):
                state[ref] = sellers[j // 2]
    return state, reserved


def settled_purchases(book, state, stock, people, rng, reserved=None):
    """The agency's 27 settled first-offer purchases of privately owned watch dwellings: committed
    January to May 2026, deed 120 days later (four of them before the notified date). Returns the refs (owned by 'AG' from the deed)."""
    sections, buildings, dwellings = stock
    pool = sorted(r for r, o in state.items() if o.startswith("p:"))
    rng.shuffle(pool)
    out = []
    for c in SETTLED_COMMITS:
        ref = pool.pop()
        deed = c + dt.timedelta(days=CLOCK)
        assert not blackout(deed), deed
        while True:
            notified = c + dt.timedelta(days=rng.randrange(38, 112))
            if not blackout(notified) and abs((notified - deed).days) >= 9:
                break
        pr = price(rng, dwellings[ref]["section"])
        seller = state[ref]
        book.commitments.append({"ref": ref, "commit": c, "notified": notified, "price": pr, "seller": seller,
                                 "lh": False, "deed": deed})
        out.append((ref, seller, deed, pr))
        if deed <= D(2026, 6, 30):
            state[ref] = "AG"
    # settled purchases whose notified date lay beyond day 120: executed on day 120 all the same
    rng2 = random.Random(SEED * 61 + 17)
    taken = set((reserved or {}).get("U_building", []))
    for c in SETTLED_EARLY:
        ref = pool.pop()
        while ref in taken:
            ref = pool.pop()
        deed = c + dt.timedelta(days=CLOCK)
        assert not blackout(deed) and deed > D(2026, 6, 30), deed
        while True:
            notified = c + dt.timedelta(days=rng2.randrange(131, 178))
            if not blackout(notified) and (notified - deed).days >= 11:
                break
        pr = price(rng2, dwellings[ref]["section"])
        seller = state[ref]
        book.commitments.append({"ref": ref, "commit": c, "notified": notified, "price": pr, "seller": seller,
                                 "lh": False, "deed": deed})
        out.append((ref, seller, deed, pr))
    return out


def backward_history(book, state, stock, people, rng, settled):
    """History from 1 July 2024 to 30 June 2026, generated backwards from the 30 June 2026 state.
    Returns the state on 30 June 2024."""
    sections, buildings, dwellings = stock
    cur = dict(state)
    touch = {}           # ref -> earliest later event date already generated
    forced = [(deed, ref, seller, pr) for ref, seller, deed, pr in settled if deed <= D(2026, 6, 30)]
    plan_dates = []
    for s in SECTIONS:
        n_ev = max(12, s["N"] // 42)
        for _ in range(n_ev):
            plan_dates.append((rand_day(rng, D(2024, 7, 8), D(2026, 6, 26)), s["code"]))
    for deed, ref, seller, pr in forced:
        plan_dates.append((deed, ("forced", ref, seller, pr)))
    plan_dates.sort(key=lambda x: (x[0], str(x[1])), reverse=True)
    for t, what in plan_dates:
        if isinstance(what, tuple):
            _, ref, seller, pr = what
            book.event(t, {ref: seller}, {ref: "AG"}, pr)
            cur[ref] = seller
            touch[ref] = t
            continue
        code = what
        s = next(x for x in SECTIONS if x["code"] == code)
        q4_25 = D(2025, 10, 1) <= t <= D(2025, 12, 31)
        kind = rng.choice(["sale", "sale", "sale", "buy", "buy", "swap"] if not q4_25 else ["sale", "sale", "swap"])
        active = sorted(h for h in s["hold"] if not (h in CARRIED and t > FREEZE - dt.timedelta(days=170)))
        free = lambda r: touch.get(r, D(2100, 1, 1)) > t + dt.timedelta(days=60)
        refs = [r for r in sorted(cur) if dwellings[r]["section"] == code and free(r)]
        if kind == "sale":
            cands = [r for r in refs if cur[r].startswith("p:")]
        else:
            cands = [r for r in refs if cur[r] in active]
        if not cands or not active:
            continue
        first = rng.choice(cands)
        same = [r for r in cands if dwellings[r]["parcel"] == dwellings[first]["parcel"]
                and (kind == "sale" or cur[r] == cur[first])]
        m = rng.choice([1, 1, 1, 2, 2, 3, 4]) if kind != "swap" else rng.choice([2, 3, 4, 6])
        group = [first] + [r for r in same if r != first][:m - 1]
        after = {r: cur[r] for r in group}
        if kind == "sale":
            seller = rng.choice(active)
            before = {r: seller for r in group}
        elif kind == "buy":
            p = people.new()
            before = {r: p for r in group}
        else:
            others = [h for h in active if h != cur[first]]
            if not others:
                continue
            seller = rng.choice(others)
            before = {r: seller for r in group}
        pr = price(rng, code)
        agr = None
        if kind in ("sale", "swap"):
            lo = max(D(2024, 4, 1), t - dt.timedelta(days=170))
            hi = t - dt.timedelta(days=35)
            if q4_25:
                lo, hi = D(2025, 3, 3), D(2025, 6, 27)
            elif rng.random() < 0.25:
                lo = max(lo, t - dt.timedelta(days=40))   # some sales are agreed and completed in one quarter
                hi = t - dt.timedelta(days=12)
            made = lo + dt.timedelta(days=rng.randrange(max(1, (hi - lo).days)))
            buyer = "private" if kind == "sale" else after[first]
            agr = book.agreement(seller=seller, buyer=buyer, buyers=[after[r] for r in group], refs=group,
                                 made=made, agreed=t, price=pr, takeover=None, section=code)
        book.event(t, before, after, pr, agr)
        for r in group:
            cur[r] = before[r]
            touch[r] = agr["made"] if agr else t
    return cur


def forward_2026(book, state, stock, people, reserved, settled, rng):
    """From 1 July 2026: plan deeds and purchases to 30 September, agreements in force on 30 June,
    the agency's commitments, and the settled purchases whose deeds fall after 30 June."""
    sections, buildings, dwellings = stock
    used = set()

    def take(code, holder, n):
        refs = sorted(r for r, o in state.items() if o == holder and dwellings[r]["section"] == code and r not in used)
        rng.shuffle(refs)
        assert len(refs) >= n, (code, holder, n)
        used.update(refs[:n])
        return sorted(refs[:n])

    def made_q2(lo=D(2026, 4, 6), hi=D(2026, 6, 26)):
        return rand_day(rng, lo, hi)

    for ref, seller, deed, pr in settled:
        if deed > D(2026, 6, 30):
            book.event(deed, {ref: seller}, {ref: "AG"}, pr)
    for s in SECTIONS:
        code = s["code"]
        for f in s["flows"]:
            if f[0] == "deed":
                _, month, seller, n, scheduled = f
                refs = take(code, seller, n)
                day = rand_day(rng, D(2026, month, 6), D(2026, month, 28 if month != 9 else 18))
                made = made_q2() if scheduled else day - dt.timedelta(days=rng.randrange(6, 20))
                if not scheduled:
                    made = max(made, D(2026, 7, 1))
                pr = price(rng, code)
                buyers = [people.new() for _ in refs]
                agr = book.agreement(seller=seller, buyer="private", buyers=buyers, refs=refs, made=made,
                                     agreed=day, price=pr, takeover=None, section=code)
                book.event(day, {r: seller for r in refs}, dict(zip(refs, buyers)), pr, agr)
            elif f[0] == "swap":
                _, month, seller, n, buyer, scheduled = f
                refs = take(code, seller, n)
                day = rand_day(rng, D(2026, month, 6), D(2026, month, 28 if month != 9 else 18))
                made = made_q2() if scheduled else max(D(2026, 7, 1), day - dt.timedelta(days=rng.randrange(6, 20)))
                pr = price(rng, code)
                agr = book.agreement(seller=seller, buyer=buyer, buyers=[buyer] * n, refs=refs, made=made,
                                     agreed=day, price=pr, takeover=None, section=code)
                book.event(day, {r: seller for r in refs}, {r: buyer for r in refs}, pr, agr)
            elif f[0] == "buy":
                _, month, buyer, n = f
                refs = sorted(reserved["U_building"][:n])
                used.update(refs)
                book.event(D(2026, 8, 6), {r: state[r] for r in refs}, {r: buyer for r in refs}, price(rng, code))
            elif f[0] == "sched":
                _, agreed, seller, n, buyer = f
                refs = take(code, seller, n)
                twin = agreed == TWIN_DATE
                pr = TWIN_PRICE if twin else price(rng, code)
                buyers = [people.new() if buyer == "private" else buyer for _ in refs]
                book.agreement(seller=seller, buyer=buyer, buyers=buyers, refs=refs,
                               made=D(2026, 5, 19) if twin else made_q2(), agreed=agreed, price=pr,
                               takeover=None, section=code)
            elif f[0] == "tk":
                _, case, seller, n, buyer, commits, agreed = f
                refs = take(code, seller, n)
                agreed_list = list(Q_AGREED) if agreed is None else [agreed] * n
                made = made_q2(D(2026, 5, 4) if s["role"] == "P" else D(2026, 4, 6), D(2026, 6, 19))
                pr0 = price(rng, code)
                for i, r in enumerate(refs):
                    ag = agreed_list[i]
                    twin = ag == TWIN_DATE and s["role"] == "Q"
                    pr = TWIN_PRICE if twin else (pr0 if s["role"] in ("P", "S") else price(rng, code))
                    b = people.new() if buyer == "private" else buyer
                    a = book.agreement(seller=seller, buyer=buyer, buyers=[b], refs=[r],
                                       made=D(2026, 5, 19) if twin else made, agreed=ag, price=pr, section=code,
                                       takeover={"commit": commits[i], "case": case,
                                                 "completion": commits[i] + dt.timedelta(days=CLOCK)})
                    book.commitments.append({"ref": r, "commit": commits[i], "notified": ag, "price": pr,
                                             "seller": seller, "lh": True, "agreement": a["id"]})
    # the agency's commitments to buy privately owned watch dwellings since 30 June (not yet settled)
    done = {ref for ref, *_ in settled}
    pool = sorted(r for r, o in state.items() if o.startswith("p:") and r not in used and r not in done)
    rng.shuffle(pool)
    for _ in range(19):
        ref = pool.pop()
        c = rand_day(rng, D(2026, 7, 6), D(2026, 9, 29), ok=lambda d: d.weekday() < 4)
        notified = c + dt.timedelta(days=rng.randrange(40, 115))
        while blackout(notified):
            notified += dt.timedelta(days=1)
        book.commitments.append({"ref": ref, "commit": c, "notified": notified,
                                 "price": price(rng, dwellings[ref]["section"]), "seller": state[ref], "lh": False})
    return used
