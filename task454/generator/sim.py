"""Simulates the world's records: the statistical areas and their population, the card scheme's research sample (one
row per sampled card, region and month of 2026), and the older program's grants, claims, payments and receipts."""
import numpy as np
from world import *

MONTHS = list(range(1, 13))


def geography(rng):
    """SA2 table: code, name, SA3 code and name, home region (the region holding most of it), ERP 2026 and 2025."""
    rows = []
    sa4 = 1
    for reg in CODES:
        for k, (sa3name, names) in enumerate(SA3S[reg]):
            sa3 = "4%02d%02d" % (sa4, k + 1)
            for j, nm in enumerate(names):
                rows.append({"sa2": sa3 + "%04d" % (1001 + j), "sa2_name": nm, "sa3": sa3, "sa3_name": sa3name, "region": reg})
        sa4 += 1
    # population: split each region's ERP over its SA2s (shared SA2s carry their schedule share in each region)
    by_reg = {r: [x for x in rows if x["region"] == r] for r in CODES}
    for reg in CODES:
        xs = by_reg[reg]
        w = rng.uniform(0.6, 1.6, len(xs))
        w = w / w.sum()
        for x, wi in zip(xs, w):
            x["w"] = wi
    # population of a shared SA2 contributes to two regions; solve each region's SA2 populations so totals hit ERP
    for yr, erp in (("erp26", ERP26), ("erp25", ERP25)):
        foreign = {r: 0.0 for r in CODES}
        pops = {}
        # first pass: shared SA2s get a population from their home region's weights
        for x in rows:
            if x["sa2_name"] in SHARED:
                tot = erp[x["region"]] * x["w"] * 1.6
                pops[x["sa2"]] = tot
                for r, s in SHARED[x["sa2_name"]].items():
                    if r != x["region"]:
                        foreign[r] += tot * s
        for reg in CODES:
            xs = by_reg[reg]
            own_shared = sum(pops[x["sa2"]] * SHARED[x["sa2_name"]][reg] for x in xs if x["sa2_name"] in SHARED)
            rest = erp[reg] - foreign[reg] - own_shared
            free = [x for x in xs if x["sa2_name"] not in SHARED]
            ws = np.array([x["w"] for x in free])
            ws = ws / ws.sum()
            vals = np.floor(ws * rest).astype(int)
            vals[0] += int(round(rest)) - int(vals.sum())
            for x, v in zip(free, vals):
                pops[x["sa2"]] = int(v)
        for x in rows:
            x[yr] = int(round(pops[x["sa2"]]))
    return rows


def region_erp(sa2s, key="erp26"):
    out = {r: 0.0 for r in CODES}
    for x in sa2s:
        if x["sa2_name"] in SHARED:
            for r, s in SHARED[x["sa2_name"]].items():
                out[r] += x[key] * s
        else:
            out[x["region"]] += x[key]
    return out


def publish_erp(rng, sa2s):
    """The statistics office's released figures: each region's areas carry the release's own level, so the region
    totals are whatever the areas sum to."""
    for x in sa2s:
        g = RELEASE[x["region"]]
        x["erp26"] = int(round(x["erp26"] * g))
        x["erp25"] = int(round(x["erp25"] * g * (1 + rng.uniform(-0.004, 0.004))))


def addresses(rng, cards, sa2s):
    """The statement SA2 a holder moved their statements to during 2026: an area of the region they live in."""
    by_reg = {}
    for x in sa2s:
        by_reg.setdefault(x["region"], []).append(x["sa2"])
    for c in cards:
        if c.sa2_change and c.sa2_change[1] is None:
            c.sa2_change = (c.sa2_change[0], by_reg[c.home][int(rng.integers(len(by_reg[c.home])))])


class Card:
    __slots__ = ("cid", "stratum", "kind", "home", "rows", "sa2", "sa2_change")

    def __init__(self, cid, stratum, kind):
        self.cid, self.stratum, self.kind = cid, stratum, kind
        self.home = None
        self.rows = {}          # (region, month) -> [spend, transactions, days]
        self.sa2 = None
        self.sa2_change = None  # (month, new sa2) when the statement address changed during 2026

    def add(self, reg, m, days, per_day, rng, tx_per_day=(1.0, 2.2)):
        if days <= 0:
            return
        k = (reg, m)
        cur = self.rows.get(k)
        spend = round(days * per_day, 2)
        tx = max(days, int(round(days * rng.uniform(*tx_per_day))))
        if cur is None:
            self.rows[k] = [spend, tx, days]
        else:
            cur[0] = round(cur[0] + spend, 2); cur[1] += tx; cur[2] = min(cur[2] + days, 28 if m == 2 else 30)

    def months_in(self, reg):
        return [m for (r, m) in self.rows if r == reg]

    def days_in(self, reg):
        return sum(v[2] for (r, m), v in self.rows.items() if r == reg)


def sample(rng, sa2s):
    pop_cards = {r: int(round(ERP26[r] * CARDS_PER_RESIDENT)) for r in CODES}
    pop_cards["IS"] = INTERSTATE_CARDS
    n = {h: int(round(pop_cards[h] * SAMPLING_FRACTION[h])) for h in pop_cards}
    weight = {h: pop_cards[h] / n[h] for h in pop_cards}
    sa2_by_reg = {r: [x for x in sa2s if x["region"] == r or (x["sa2_name"] in SHARED and r in SHARED[x["sa2_name"]])]
                  for r in CODES}
    cards, cid = [], 0

    def pick_sa2(reg):
        xs = sa2_by_reg[reg]
        w = np.array([x["erp26"] * (SHARED[x["sa2_name"]][reg] if x["sa2_name"] in SHARED else 1.0) for x in xs], float)
        return xs[int(rng.choice(len(xs), p=w / w.sum()))]["sa2"]

    def interstate_sa2():
        st = int(rng.choice([1, 2, 3, 5, 6, 7, 8], p=[.34, .28, .2, .1, .03, .02, .03]))
        return "%d%02d%02d%04d" % (st, rng.integers(1, 20), rng.integers(1, 9), rng.integers(1001, 1099))

    # stratum composition: locals plus the routine-elsewhere kinds drawn from the stratum's statement addresses
    for h in list(CODES) + ["IS"]:
        kinds = []
        if h in FIFO:
            kinds += [("fifo", "GID")] * int(round(FIFO[h] * SAMPLING_FRACTION[h]))
        if h in STUDENTS:
            kinds += [("student", "CAR")] * int(round(STUDENTS[h] * SAMPLING_FRACTION[h]))
        for o, d, p in MOVERS:
            if o == h:
                kinds += [("mover", d)] * int(round(p * SAMPLING_FRACTION[h]))
        for o, d, p in COMMUTERS:
            if o == h:
                kinds += [("commuter", d)] * int(round(p * SAMPLING_FRACTION[h]))
        base = "visitor" if h == "IS" else "local"
        kinds += [(base, None)] * (n[h] - len(kinds))
        order = rng.permutation(len(kinds))
        for i in order:
            kind, dest = kinds[i]
            cid += 1
            c = Card(cid, h, kind)
            c.home = dest
            c.sa2 = interstate_sa2() if h == "IS" else pick_sa2(h)
            cards.append(c)
    return cards, n, weight, pop_cards


def routine_rows(rng, cards):
    for c in cards:
        h = c.stratum
        if c.kind == "local":
            for m in MONTHS:
                c.add(h, m, int(rng.integers(8, 23)), rng.uniform(35, 75), rng)
        elif c.kind == "fifo":
            roster = rng.choice([(14, 7), (21, 7), (8, 6)])
            # camp meals are provided: half the workforce uses a card on site for little more than fuel and the tavern
            prop = rng.uniform(0.6, 0.9) if rng.random() < 0.6 else rng.uniform(1.3, 2.5)
            for m in MONTHS:
                on = int(rng.integers(12, 21)) if roster[0] >= 14 else int(rng.integers(10, 16))
                c.add("GID", m, on, prop * rng.uniform(12, 34), rng)
                if h != "IS":
                    c.add(h, m, int(rng.integers(6, 13)), rng.uniform(40, 70), rng)
        elif c.kind == "student":
            prop = rng.uniform(0.5, 0.8) if rng.random() < 0.5 else rng.uniform(1.0, 1.9)
            for m in range(2, 12):
                c.add("CAR", m, int(rng.integers(12, 21)) if m not in (2, 11) else int(rng.integers(6, 12)), prop * rng.uniform(16, 36), rng)
            if h != "IS":
                for m, lo, hi in ((1, 15, 25), (2, 3, 7), (4, 3, 7), (6, 4, 8), (7, 6, 11), (9, 3, 7), (11, 2, 6), (12, 15, 24)):
                    c.add(h, m, int(rng.integers(lo, hi)), rng.uniform(30, 55), rng)
        elif c.kind == "mover":
            for m in MONTHS:
                c.add(c.home, m, int(rng.integers(10, 23)), rng.uniform(45, 80), rng)
            for _ in range(int(rng.integers(0, 3))):
                c.add(h, int(rng.integers(1, 13)), int(rng.integers(1, 5)), rng.uniform(60, 140), rng)
            if rng.random() < 0.3 and h != "IS":
                # the holder updated the statement address during the year
                c.sa2_change = (int(rng.integers(3, 12)), None)
        elif c.kind == "commuter":
            for m in MONTHS:
                c.add(c.home, m, int(rng.integers(12, 21)), rng.uniform(18, 35), rng)
                c.add(h, m, int(rng.integers(8, 15)), rng.uniform(40, 65), rng)


def trips(rng, cards, weight, region_pop):
    """Genuine trips: each destination's visitor spending target is spread over its origin strata and laid on random
    cards from them as trips of one to ten days, at most three months and 21 days per card and destination."""
    pools = {}
    cycle = {"IS": []}
    for c in cards:
        if c.kind in ("local", "visitor", "fifo", "mover", "commuter"):
            pools.setdefault(c.stratum, []).append(c)
    for dest in ELIGIBLE:
        V = VISITOR_TARGET[dest] * region_pop[dest]
        share = dict(ORIGIN[dest])
        others = [r for r in CODES if r not in share and r != dest]
        rest = 1 - sum(share.values())
        for r in others:
            share[r] = rest / len(others)
        for o, s in share.items():
            need = V * s / weight[o]
            pool = pools[o]
            spent, guard = 0.0, 0
            while spent < need and guard < 200000:
                guard += 1
                if o == "IS":
                    # every interstate card in the sample spent in the state: draw them in turn before reusing any
                    if not cycle["IS"]:
                        cycle["IS"] = [pool[int(i)] for i in rng.permutation(len(pool))]
                    c = cycle["IS"].pop()
                else:
                    c = pool[int(rng.integers(len(pool)))]
                if c.home == dest or (c.kind != "visitor" and c.stratum == dest):
                    continue
                ms = c.months_in(dest)
                used = c.days_in(dest)
                if len(ms) >= 3 or used >= 21:
                    continue
                long = rng.random() < LONG_STAY.get(dest, 0.03)
                days = int(rng.integers(6, 11)) if long else int(rng.integers(1, 7))
                days = min(days, 21 - used)
                lo, hi = TRIP_SPEND.get(dest, TRIP_SPEND_DEFAULT)
                per = rng.uniform(300, 560) if long else rng.uniform(lo, hi)
                m = int(rng.integers(1, 13)) if len(ms) < 3 else int(rng.choice(ms))
                c.add(dest, m, days, per, rng)
                spent += days * per
    # highway stopovers: one day, small spend, cards from everywhere
    for dest, cardvisits in STOPOVERS.items():
        share = {"WST": 0.45, "IS": 0.30}
        others = [r for r in CODES if r not in share and r != dest]
        for r in others:
            share[r] = 0.25 / len(others)
        for o, s in share.items():
            k = int(round(cardvisits * s / weight[o]))
            pool = pools[o]
            done, guard = 0, 0
            while done < k and guard < 100000:
                guard += 1
                if o == "IS":
                    if not cycle["IS"]:
                        cycle["IS"] = [pool[int(i)] for i in rng.permutation(len(pool))]
                    c = cycle["IS"].pop()
                else:
                    c = pool[int(rng.integers(len(pool)))]
                if c.home == dest or (c.kind != "visitor" and c.stratum == dest):
                    continue
                if len(c.months_in(dest)) >= 3 or c.days_in(dest) >= 21:
                    continue
                c.add(dest, int(rng.integers(1, 13)), 1, rng.uniform(*STOP_SPEND), rng, (1.0, 1.6))
                done += 1


def program(rng):
    """The older program's agreements and its 2026 claims, payments and receipts. Finance pays approved claims in the
    Thursday run at least four days after approval, one transfer per council per run quoting the agreement of the run's
    first claim; a payment held for checks waits for a run in January 2027. A retention is released through a retention
    claim once an agreement is acquitted. The 19 March retention run went to the bank twice and councils sent the repeat
    back, some in the same transfer as another agreement's unspent money. A council returns unspent money some weeks
    after an acquittal under budget, so returns cross the year ends. The program's last approvals were made in the week
    it closed and were paid in January 2027."""
    import datetime as dt
    D = dt.date
    agreements, claims, receipts = [], [], []
    words = {}

    def locality(name):
        s = name
        for t in ("Shire of ", "City of "):
            s = s.replace(t, "")
        for t in (" Shire Council", " Regional Council", " City Council", " Council"):
            s = s.replace(t, "")
        return s

    def new_ag(name, reg, rd):
        used = words.setdefault(name, [])
        free = [w for w in PROJECT_WORDS if w not in used]
        w = free[int(rng.integers(len(free)))]
        used.append(w)
        a = {"agreement": None, "council": name, "region": reg, "round": rd,
             "approved": int(round(rng.uniform(120_000, 560_000), -3)), "project": "%s %s" % (locality(name), w),
             "signed": wday(rd, int(rng.integers(3, 11)), 1, 27), "status": "Open",
             "acquitted": None, "final_cost": None, "paid_before": 0.0}
        agreements.append(a)
        return a

    def money(x):
        return round(float(x), 2)

    def cents(x):
        return round(int(round(x)) + int(rng.integers(0, 100)) / 100.0, 2)

    def wk(d):
        """Offices record approvals, acquittals and receipts on working days."""
        while d.weekday() >= 5:
            d += dt.timedelta(days=1)
        return d

    def rand_date(lo, hi):
        days = [lo + dt.timedelta(days=k) for k in range((hi - lo).days + 1)]
        days = [d for d in days if d.weekday() < 5] or [wk(lo)]
        return days[int(rng.integers(len(days)))]

    def wday(y, m, d0, d1):
        return rand_date(D(y, m, d0), D(y, m, d1))

    def run_after(d):
        d = d + dt.timedelta(days=4)
        while d.weekday() != 3:
            d += dt.timedelta(days=1)
        return d

    def claim(a, label, amt, appr, lag, hold=False):
        c = {"claim": None, "ag": a, "agreement": None, "council": a["council"], "milestone": label,
             "claimed": round(amt * float(rng.choice([1.0, 1.0, 1.0, 1.035])), 2), "approved_amt": amt,
             "approved_on": appr, "lodged": appr - dt.timedelta(days=int(lag)), "hold": hold, "paid": None, "run": None}
        claims.append(c)
        return c

    def receipt(name, amount, when, parts):
        receipts.append({"receipt": None, "on": when, "payer": name, "amount": round(amount, 2), "parts": parts})

    def settle_under(a, lo, hi):
        a["status"] = "Acquitted"
        a["paid_before"] = float(a["approved"])
        a["final_cost"] = money(a["approved"] * (1 - rng.uniform(lo, hi)))
        return money(a["paid_before"] - a["final_cost"])

    regions = sorted({c[1] for c in COUNCILS})
    later = [c[0] for c in COUNCILS if c[2] > 2020]
    slow = {later[int(i)] for i in rng.permutation(len(later))[:3]}
    cross = {regions[int(i)] for i in rng.permutation(len(regions))[:8]} | {c[1] for c in COUNCILS if c[0] in slow}
    held_regions = {regions[int(i)] for i in rng.permutation(len(regions))[:8]}
    wd_names, seen = [], set()
    for i in rng.permutation(len(COUNCILS)):
        name, reg, first = COUNCILS[int(i)]
        if reg not in seen and len(wd_names) < 3:
            seen.add(reg); wd_names.append(name)
    opens_of, mains, withdrawn = {}, {}, []
    for name, reg, first in COUNCILS:
        main = first <= 2020
        # agreements acquitted before 2026; under budget, the council returned the difference within weeks
        k = int(rng.integers(1, 3)) if main else (1 if first <= 2021 else 0)
        for rd in sorted(int(x) for x in rng.choice(list(range(first, 2022)), size=min(k, 2022 - first), replace=False)):
            o = new_ag(name, reg, rd)
            o["acquitted"] = rand_date(D(rd + 1, 6, 1), D(2025, 10, 31))
            if rng.random() < 0.5:
                settle_under(o, 0.03, 0.10)
            else:
                o["status"] = "Acquitted"
                o["final_cost"] = money(o["approved"] * (1 - rng.uniform(0.0, 0.02)))
                o["paid_before"] = o["final_cost"]
        if main:
            F = new_ag(name, reg, first)                 # an early project acquitted late in 2026 with its retention
            F["paid_before"] = money(0.95 * F["approved"])
            X = new_ag(name, reg, 2021)                  # paid in full, acquitted under budget in mid 2026
            X["paid_before"] = float(X["approved"])
            mains[name] = (F, X)
        Y = new_ag(name, reg, 2022)                      # acquitted early in 2026, its retention in the 19 March run
        Y["paid_before"] = money(0.95 * Y["approved"])
        opens = [new_ag(name, reg, rd) for rd in sorted(int(x) for x in rng.choice([2023, 2024, 2025], size=2, replace=False))]
        for a in opens:
            f = rng.uniform(0.15, 0.45) if a["round"] <= 2024 else rng.uniform(0.0, 0.2)
            a["paid_before"] = money(a["approved"] * f) if f >= 0.04 else 0.0
        opens_of[name] = opens
        Y["status"] = "Acquitted"
        Y["acquitted"] = wday(2026, int(rng.choice([2, 3])), 2, 11)
        Y["final_cost"] = money(Y["approved"] * (1 - rng.uniform(0.0, 0.02)))
        cy = claim(Y, "Retention", money(Y["final_cost"] - Y["paid_before"]), Y["acquitted"], 0)
        cy["run"] = D(2026, 3, 19)
        # milestone claims on the open agreements through the year, in milestone order
        wd = [a for a in opens if a["paid_before"] > 0][:1] if name in wd_names else []
        withdrawn += wd
        for a in opens:
            hi = 6 if wd and a is wd[0] else 13
            a["_dates"] = sorted(wday(2026, int(rng.integers(1, hi)), 1, 27) for _ in range(int(rng.integers(2, 4))))
        keep = [a for a in opens if not (wd and a is wd[0])]
        if main and not any(7 <= d.month <= 11 for a in keep for d in a["_dates"]):
            a = keep[0]
            a["_dates"] = sorted(a["_dates"][:-1] + [wday(2026, 9, 1, 24)])
        for a in opens:
            left = a["approved"] - a["paid_before"]
            a["_next"] = 2 if a["paid_before"] > 0 else 1
            for d in a["_dates"]:
                claim(a, "M%d" % a["_next"], cents(left * rng.uniform(0.10, 0.22)), d, rng.integers(3, 25))
                a["_next"] += 1

    live = {name: [a for a in opens_of[name] if not any(a is w for w in withdrawn)] for name in opens_of}

    def add_claim(a, d, hold=False):
        c = claim(a, "M%d" % a["_next"], cents((a["approved"] - a["paid_before"]) * rng.uniform(0.08, 0.16)), d, rng.integers(5, 20), hold)
        a["_next"] += 1
        return c

    # payments held for checks (paid in January 2027), one council in each of eight regions: a claim approved after
    # its agreement's last milestone and before another agreement's milestone was paid
    for reg in sorted(held_regions):
        names = [c[0] for c in COUNCILS if c[1] == reg]
        options = []
        for name in names:
            for a in live[name]:
                later = [d for b in live[name] if b is not a for d in b["_dates"] if d <= D(2026, 12, 27)]
                lo = a["_dates"][-1] + dt.timedelta(days=5)
                hi = max(later, default=lo) - dt.timedelta(days=5)
                if hi >= lo and hi.year == 2026:
                    options.append((a, lo, hi))
        if not options:
            continue
        a, lo, hi = options[int(rng.integers(len(options)))]
        add_claim(a, rand_date(lo, hi), hold=True)
    # the program's last approvals, in the week it closed
    for name, reg, first in COUNCILS:
        if rng.random() < 0.6:
            a = live[name][int(rng.integers(len(live[name])))]
            add_claim(a, D(2026, 12, int(rng.integers(29, 31))))
    for reg in regions:
        names = [c[0] for c in COUNCILS if c[1] == reg]
        if not any(c["hold"] or c["approved_on"] >= D(2026, 12, 28) for c in claims if c["council"] in names):
            name = names[int(rng.integers(len(names)))]
            add_claim(live[name][int(rng.integers(len(live[name])))], D(2026, 12, int(rng.integers(29, 31))))
    # main councils: the 2021 agreement acquitted under budget between April and June; the early agreement acquitted in
    # the second half, its retention approved with a milestone of an open agreement and so paid in the same run
    for name, (F, X) in mains.items():
        X["status"] = "Acquitted"
        X["acquitted"] = wday(2026, int(rng.integers(4, 7)), 1, 27)
        X["final_cost"] = money(X["approved"] * (1 - rng.uniform(0.04, 0.12)))
        host = [c for c in claims if c["council"] == name and c["milestone"] != "Retention" and not c["hold"]
                and any(c["ag"] is a for a in opens_of[name]) and 7 <= c["approved_on"].month <= 11]
        h = host[int(rng.integers(len(host)))]
        F["status"] = "Acquitted"
        F["acquitted"] = h["approved_on"]
        F["final_cost"] = money(F["approved"] * (1 - rng.uniform(0.0, 0.015)))
        claim(F, "Retention", money(F["final_cost"] - F["paid_before"]), F["acquitted"], 0)
    # an agreement settled across a year end in eight regions: acquitted under budget late in 2025 with the money back in
    # January 2026, or acquitted in December 2026 with the money back in January 2027
    late_returns = []
    for reg in sorted(cross):
        names = [c[0] for c in COUNCILS if c[1] == reg]
        name = names[int(rng.integers(len(names)))]
        if any(n in slow for n in names):
            name = [n for n in names if n in slow][0]
        first = [c[2] for c in COUNCILS if c[0] == name][0]
        if rng.random() < 0.5 or name in slow:
            z = new_ag(name, reg, max(first, 2021))
            z["acquitted"] = rand_date(D(2025, 11, 10), D(2025, 12, 19))
            back = settle_under(z, 0.03, 0.10)
            receipt(name, back, rand_date(D(2026, 1, 6), D(2026, 2, 6)), [("unspent", z, back)])
        else:
            z = new_ag(name, reg, max(first, 2022))
            z["acquitted"] = rand_date(D(2026, 12, 1), D(2026, 12, 18))
            back = settle_under(z, 0.03, 0.10)
            late_returns.append((z, back))
    # payments: one transfer per council per run, quoting the agreement of its first claim
    for c in claims:
        if c["run"] is None:
            c["run"] = D(2027, 1, 14) if c["hold"] else run_after(c["approved_on"])
    num = 2206
    for c in sorted(claims, key=lambda c: (c["lodged"], c["council"], c["approved_on"])):
        num += int(rng.integers(1, 6))
        c["claim"] = "CL-%05d" % num
    by_run = {}
    for c in claims:
        if c["run"].year == 2026:
            by_run.setdefault((c["run"], c["council"]), []).append(c)
    pays = []
    for (run, name), cs in sorted(by_run.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        cs.sort(key=lambda c: (c["approved_on"], c["claim"]))
        pays.append({"payment": None, "paid_on": run, "payee": name, "amount": round(sum(c["approved_amt"] for c in cs), 2),
                     "ref_ag": cs[0]["ag"], "claims": cs})
        for c in cs:
            c["paid"] = run
    # the 19 March run, sent to the bank again on 20 March
    for p in [p for p in pays if p["paid_on"] == D(2026, 3, 19)]:
        q = dict(p)
        q["paid_on"] = D(2026, 3, 20); q["claims"] = []; q["repeat_of"] = p
        pays.append(q)
    # receipts: a main council sends the repeat back with its 2021 agreement's unspent money in one transfer; the others
    # send the repeat alone
    for name, reg, first in COUNCILS:
        rep = [p for p in pays if p.get("repeat_of") and p["payee"] == name]
        if name in mains:
            X = mains[name][1]
            unspent = money(X["paid_before"] - X["final_cost"])
            when = wk(max(X["acquitted"], D(2026, 4, 1)) + dt.timedelta(days=int(rng.integers(10, 30))))
            receipt(name, unspent + sum(p["amount"] for p in rep), when, [("unspent", X, unspent)] + [("repeat", p, p["amount"]) for p in rep])
        elif name not in slow:
            for p in rep:
                receipt(name, p["amount"], wday(2026, int(rng.integers(4, 6)), 1, 27), [("repeat", p, p["amount"])])
    # the withdrawn agreements: the council returns what it was paid and did not spend
    for a in withdrawn:
        paid26 = sum(c["approved_amt"] for c in claims if c["ag"] is a and c["paid"])
        a["status"] = "Withdrawn"
        a["acquitted"] = wday(2026, int(rng.integers(6, 11)), 1, 27)
        spent = money((a["paid_before"] + paid26) * rng.uniform(0.3, 0.7))
        a["final_cost"] = spent
        back = money(a["paid_before"] + paid26 - spent)
        receipt(a["council"], back, wk(a["acquitted"] + dt.timedelta(days=int(rng.integers(10, 35)))), [("unspent", a, back)])
    # identifiers: agreements numbered within each round in signing order, payments and receipts in the order the
    # finance system raised them, among the Commission's other payments and receipts
    for rd in sorted({a["round"] for a in agreements}):
        k = 0
        for a in sorted([a for a in agreements if a["round"] == rd], key=lambda a: (a["signed"], a["council"])):
            k += int(rng.integers(1, 4))      # numbers given to applications the round did not fund are not reused
            a["agreement"] = "RTIP-%d-%03d" % (rd, k)
    pays.sort(key=lambda p: (p["paid_on"], p["payee"]))
    num, last = 40870, None
    for p in pays:
        num += int(rng.integers(1, 7)) if p["paid_on"] == last else int(rng.integers(25, 140))
        last = p["paid_on"]
        p["payment"] = "AP%06d" % num
        p["run"] = "PR%d-%02d" % (p["paid_on"].isocalendar()[0], p["paid_on"].isocalendar()[1])
    receipts.sort(key=lambda r: (r["on"], r["payer"]))
    num = 7261
    for r in receipts:
        num += int(rng.integers(1, 30))
        r["receipt"] = "RC%05d" % num
    for c in claims:
        c["agreement"] = c["ag"]["agreement"]
    for p in pays:
        p["ref"] = p["ref_ag"]["agreement"]
        p["claims"] = [c["claim"] for c in p["claims"]]
        if p.get("repeat_of"):
            p["repeat_of"] = p["repeat_of"]["payment"]
    for r in receipts:
        r["parts"] = [(k, x["agreement"] if k == "unspent" else x["payment"], amt) for k, x, amt in r["parts"]]
    for c in claims:
        del c["ag"]
    for p in pays:
        del p["ref_ag"]
    for a in agreements:
        a.pop("_dates", None); a.pop("_next", None)
    late = [(z["agreement"], back) for z, back in late_returns]
    owed = [(p["payee"], p["payment"], p["amount"]) for p in pays if p.get("repeat_of") and p["payee"] in slow]
    return agreements, claims, pays, receipts, {"returned_2027": late, "repeat_owed_at_year_end": owed}
