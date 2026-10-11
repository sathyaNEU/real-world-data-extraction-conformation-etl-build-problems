"""Simulate the credit union's members, their cards and four months of card activity.

Activity is generated per card slot (a member's debit card, second debit card or credit card); a slot
can carry several card numbers over the period (renewal, loss, fraud reissue), which fraud.py maps once
every replacement is known. Deterministic for world.SEED.
"""
import datetime as dt

import numpy as np
import pandas as pd

import world as W
import places

D0 = W.SIM_START
ND = (W.SIM_END - W.SIM_START).days + 1          # 127 local days, 31 May .. 4 Oct
DAY = 86_400

ENTRY = ["05", "07", "80", "90", "91", "01", "81"]
E05, E07, E80, E90, E91, E01, E81 = range(7)
KIND = ["purchase", "pump", "atm", "balance", "refund", "cnp"]
K_PUR, K_PUMP, K_ATM, K_BAL, K_REF, K_CNP = range(6)


def day_of(d):
    return (d - D0).days


def date_of(i):
    return D0 + dt.timedelta(int(i))


DATES = [date_of(i) for i in range(ND)]
WEEKDAY = np.array([d.weekday() for d in DATES])
HOLIDAY = np.array([d in W.HOLIDAY_SET for d in DATES])
WORKDAY = (WEEKDAY < 5) & ~HOLIDAY

# category mix by card type (shares of local card-present and card-absent activity)
DEBIT_MIX = {"grocery": 0.20, "pharmacy": 0.06, "fuel": 0.07, "fuelshop": 0.03, "restaurant": 0.06,
             "fastfood": 0.09, "coffee": 0.085, "hardware": 0.03, "discount": 0.05, "liquor": 0.04,
             "clothing": 0.025, "convenience": 0.06, "bakery": 0.02, "homeimprove": 0.015, "auto": 0.006,
             "dental": 0.006, "salon": 0.01, "pet": 0.01, "sporting": 0.006, "electronics": 0.006,
             "books": 0.006, "florist": 0.004, "carwash": 0.004, "atm": 0.06, "parking": 0.005, "cnp": 0.045}
CREDIT_MIX = {"grocery": 0.14, "pharmacy": 0.05, "fuel": 0.09, "fuelshop": 0.01, "restaurant": 0.10,
              "fastfood": 0.05, "coffee": 0.03, "hardware": 0.04, "discount": 0.05, "liquor": 0.04,
              "clothing": 0.05, "convenience": 0.02, "bakery": 0.01, "homeimprove": 0.03, "auto": 0.015,
              "dental": 0.012, "salon": 0.012, "pet": 0.012, "sporting": 0.015, "electronics": 0.015,
              "books": 0.01, "florist": 0.006, "carwash": 0.003, "atm": 0.004, "parking": 0.01, "cnp": 0.18}
NEIGHBOURS = {
    "Smiths Falls": [("Perth", 0.25), ("Carleton Place", 0.12), ("Merrickville", 0.10), ("Ottawa", 0.28),
                     ("Kemptville", 0.08), ("Brockville", 0.10), ("Westport", 0.07)],
    "Perth": [("Smiths Falls", 0.30), ("Carleton Place", 0.18), ("Ottawa", 0.27), ("Lanark", 0.10),
              ("Kingston", 0.08), ("Westport", 0.07)],
    "Carleton Place": [("Ottawa", 0.55), ("Almonte", 0.15), ("Perth", 0.12), ("Smiths Falls", 0.12),
                       ("Kemptville", 0.06)],
    "Kemptville": [("Ottawa", 0.50), ("Merrickville", 0.14), ("Smiths Falls", 0.10), ("Brockville", 0.10),
                   ("Prescott", 0.16)],
    "Merrickville": [("Kemptville", 0.30), ("Smiths Falls", 0.30), ("Ottawa", 0.28), ("Perth", 0.12)],
    "Brockville": [("Kingston", 0.30), ("Prescott", 0.20), ("Ottawa", 0.18), ("Gananoque", 0.17),
                   ("Kemptville", 0.07), ("Smiths Falls", 0.08)],
    "Kingston": [("Gananoque", 0.25), ("Napanee", 0.25), ("Brockville", 0.20), ("Ottawa", 0.18),
                 ("Westport", 0.12)],
}
HOURS = {c: (v[3], v[4]) for c, v in places.CATS.items()}
OPT_PICK = np.array([0.10, 0.10, 0.12, 0.12, 0.16, 0.18, 0.11, 0.11])   # islands 3 (OPT 5, 6) face the building
HOURS["cnp"] = (0, 24)
HOURS["atm"] = (7, 23)


class Sim:
    pass


def build_people(rng, cat):
    towns = [b[0] for b in W.BRANCHES]
    share = np.array([b[1] for b in W.BRANCHES])
    share = share / share.sum()
    n = W.N_MEMBERS
    town_idx = rng.choice(len(towns), size=n, p=share)
    ids = rng.choice(np.arange(1_002_000, 1_998_000), size=n, replace=False)
    members = pd.DataFrame({"member_id": ["%07d" % i for i in ids], "town": [towns[i] for i in town_idx]})
    since = [dt.date(1984, 1, 1) + dt.timedelta(int(x)) for x in rng.integers(0, 15_000, n)]
    members["member_since"] = [min(s, dt.date(2026, 5, 1)) for s in since]
    commute_p = {"Kemptville": 0.22, "Merrickville": 0.25, "Smiths Falls": 0.11, "Perth": 0.08}
    occ_p = {"Kemptville": 0.30, "Merrickville": 0.24, "Smiths Falls": 0.14, "Perth": 0.09, "Brockville": 0.17,
             "Carleton Place": 0.04, "Kingston": 0.10}
    lombard_p = {"Smiths Falls": 0.66, "Merrickville": 0.12, "Perth": 0.07}
    u = rng.random((n, 4))
    members["commuter"] = [u[i, 0] < commute_p.get(t, 0.0) for i, t in enumerate(members["town"])]
    members["occasional"] = [(not members["commuter"].iat[i]) and u[i, 1] < occ_p.get(t, 0.0)
                             for i, t in enumerate(members["town"])]
    members["lombard"] = [u[i, 2] < lombard_p.get(t, 0.0) for i, t in enumerate(members["town"])]
    members["traveller"] = u[:, 3] < 0.27
    return members


def build_slots(rng, members):
    rows = []
    for i, m in enumerate(members.itertuples()):
        kinds = []
        if rng.random() < 0.985:
            kinds.append(("Debit", 1.0))
        if rng.random() < 0.10:
            kinds.append(("Debit", 0.38))
        if rng.random() < 0.45 or not kinds:
            kinds.append(("Credit", 1.0))
        for k, (ctype, scale) in enumerate(kinds):
            if ctype == "Debit":
                rate = float(np.clip(rng.lognormal(np.log(0.565), 0.55), 0.05, 2.8)) * scale
            else:
                rate = float(np.clip(rng.lognormal(np.log(0.335), 0.70), 0.03, 2.2)) * scale
            rows.append({"slot": len(rows), "member": i, "member_id": m.member_id, "card_type": ctype,
                         "secondary": scale < 1.0, "rate": rate,
                         "nfc": rng.random() < 0.975, "p_tap": float(np.clip(rng.beta(9, 1.2), 0.3, 0.995)),
                         "acct": "10" if (ctype == "Debit" and rng.random() < 0.14) else "20"})
    slots = pd.DataFrame(rows)
    # primary card a member uses on the road (plaza, travel): debit if they hold one, mostly
    prim = {}
    by_member = {}
    for r in rows:
        by_member.setdefault(r["member"], []).append(r)
    for m in sorted(by_member):
        g = by_member[m]
        deb = [r for r in g if r["card_type"] == "Debit" and not r["secondary"]]
        cre = [r for r in g if r["card_type"] == "Credit"]
        if deb and (not cre or rng.random() < 0.74):
            prim[m] = deb[0]["slot"]
        else:
            prim[m] = cre[0]["slot"] if cre else g[0]["slot"]
    slots["road"] = [prim[m] == s for m, s in zip(slots.member, slots.slot)]
    comm = members.commuter.values[slots.member.values]
    slots.loc[slots.road & comm, "nfc"] = True
    return slots


def lifecycle(rng, slots):
    """Issue dates, expiry and the replacements and closures due in the period (fraud reissues are
    added by fraud.py)."""
    n = len(slots)
    issued, expiry = [], []
    for s in slots.itertuples():
        u = rng.random()
        if s.card_type == "Debit" and u < 0.09:
            iss = dt.date(2023, 9, 1) + dt.timedelta(int(rng.integers(0, 28)))      # 2023 conversion wave
            exp = (2026, 9)
        elif s.card_type == "Debit" and u < 0.13:
            iss = dt.date(2023, 10, 2) + dt.timedelta(int(rng.integers(0, 26)))
            exp = (2026, 10)
        else:
            iss = dt.date(2023, 11, 1) + dt.timedelta(int(rng.integers(0, 940)))
            yrs = 3 if s.card_type == "Debit" else 4
            exp = (iss.year + yrs, iss.month)
            if exp <= (2026, 10):
                exp = (2027, iss.month)
        issued.append(iss)
        expiry.append(exp)
    slots["issued_on"] = issued
    slots["exp_y"] = [e[0] for e in expiry]
    slots["exp_m"] = [e[1] for e in expiry]
    events = []   # (slot, date, reason, gap_days)
    for s in slots.itertuples():
        if (s.exp_y, s.exp_m) == (2026, 9):
            d = dt.date(2026, 8, 10) + dt.timedelta(int(rng.integers(0, 52)))
            events.append((s.slot, d, "RN", 0))
        elif (s.exp_y, s.exp_m) == (2026, 10):
            d = dt.date(2026, 9, 8) + dt.timedelta(int(rng.integers(0, 34)))
            if d <= W.SIM_END:
                events.append((s.slot, d, "RN", 0))
        u = rng.random()
        if u < 0.0065:
            d = dt.date(2026, 6, 2) + dt.timedelta(int(rng.integers(0, 124)))
            events.append((s.slot, d, "LS", int(rng.integers(4, 9))))
        elif u < 0.0095:
            d = dt.date(2026, 6, 2) + dt.timedelta(int(rng.integers(0, 124)))
            events.append((s.slot, d, "DM", int(rng.integers(3, 8))))
        elif u < 0.0150:
            d = dt.date(2026, 6, 5) + dt.timedelta(int(rng.integers(0, 120)))
            events.append((s.slot, d, "CL", 0))
    ev = pd.DataFrame(events, columns=["slot", "date", "reason", "gap"]).sort_values(["slot", "date"])
    # one change per slot in the period keeps the chains readable; the earliest wins
    ev = ev.drop_duplicates("slot", keep="first").reset_index(drop=True)
    return ev


def build_trips(rng, members):
    trips = []
    dests = places.DESTINATIONS
    w = np.array([1.6 if d[2] == "US" else 1.0 for d in dests])
    w = w / w.sum()
    for i, m in enumerate(members.itertuples()):
        if not m.traveller:
            continue
        k = 1 + int(rng.random() < 0.22)
        for _ in range(k):
            di = int(rng.choice(len(dests), p=w))
            length = int(rng.integers(3, 12))
            start = int(rng.integers(day_of(dt.date(2026, 6, 5)), day_of(dt.date(2026, 9, 25))))
            trips.append((i, di, start, min(ND - 1, start + length - 1)))
    return trips


class Builder:
    """Collects (slot, day, merchant[, hour, terminal]) draws, then finalizes amounts, times, terminals
    and entry modes in one vectorized pass."""

    def __init__(self, cat, members, slots, trips, rng):
        self.cat, self.members, self.slots, self.trips, self.rng = cat, members, slots, trips, rng
        M = cat.merchants
        self.m_cat = np.array([m["cat"] for m in M])
        self.m_country = np.array([m["country"] for m in M])
        self.m_role = np.array([m["role"] for m in M])
        self.m_first_term = np.array([m["terminals"][0] if m["terminals"] else -1 for m in M])
        self.m_nterm = np.array([len(m["terminals"]) for m in M])
        cats = sorted(places.CATS) + ["cnp"]
        self.cat_list = cats
        self.cat_id = {c: i for i, c in enumerate(cats)}
        self.m_catid = np.array([self.cat_id[c] for c in self.m_cat])
        self.t_tap = np.array([t["tap"] for t in cat.terminals])
        self.m_surcharge = np.array([m.get("surcharge", 0.0) for m in M])
        self.cnp_idx = [m["idx"] for m in M if m["cat"] == "cnp"]
        self.by_town_cat = cat.by_town_cat
        self.dest_cand = {}
        for m in M:
            if m["role"] == "ordinary":
                self.dest_cand.setdefault(m["town"], []).append(m["idx"])
        self.ottawa_cand = [m["idx"] for m in M if m["town"] == "Ottawa" and m["role"] == "ordinary"
                            and m["cat"] in ("fastfood", "coffee", "restaurant", "parking", "convenience",
                                             "pharmacy")]
        self.parts = []   # (slot, days, merch, hour or None, term or None)
        self._home_cache, self._away_cache, self._profiles = {}, {}, {}

    def _home(self, town, c):
        key = (town, c)
        if key not in self._home_cache:
            self._home_cache[key] = [h for h in self.by_town_cat.get(key, [])
                                     if self.cat.merchants[h]["role"] in ("ordinary", "branch_atm", "lombard")]
        return self._home_cache[key]

    def _away(self, town, c):
        key = (town, c)
        if key not in self._away_cache:
            self._away_cache[key] = [h for h in self.by_town_cat.get(key, []) if self.cat.merchants[h]["role"] == "ordinary"]
        return self._away_cache[key]

    def profile(self, member, rng):
        """Per member, per category: merchants and their weights within the category (sum to 1)."""
        key = member.Index
        if key in self._profiles:
            return self._profiles[key]
        town = member.town
        nb = NEIGHBOURS[town]
        prof = {}
        for c in DEBIT_MIX:
            ms, ps = [], []
            if c == "cnp":
                pick = rng.choice(len(self.cnp_idx), size=int(rng.integers(3, 8)), replace=False)
                for j in sorted(pick.tolist()):
                    ms.append(self.cnp_idx[j]); ps.append(1.0 / len(pick))
                prof[c] = (ms, ps)
                continue
            home = self._home(town, c)
            if c == "atm":
                own = [h for h in home if self.cat.merchants[h]["role"] == "branch_atm"]
                other = [h for h in home if self.cat.merchants[h]["role"] != "branch_atm"]
                if own:
                    ms.append(own[0]); ps.append(0.72)
                for h in other:
                    ms.append(h); ps.append(0.18 / len(other))
                for t, wt in nb[:2]:
                    for h in self.by_town_cat.get((t, "atm"), [])[:1]:
                        ms.append(h); ps.append(0.10 * wt)
                prof[c] = (ms, ps)
                continue
            w = 1.0
            if c == "carwash" and town == "Kemptville":
                ms.append(self.cat.wash["idx"]); ps.append(0.75 * 1.15)
                w = 0.25 * 1.15
            if c == "grocery" and member.lombard:
                ms.append(self.cat.lombard["idx"]); ps.append(0.78)
                w = 0.22
                home = [h for h in home if h != self.cat.lombard["idx"]]
            local = 0.86 if home else 0.0
            if home:
                order = [home[j] for j in rng.permutation(len(home))]
                favw = [0.62, 0.24, 0.14][:len(order)]
                tot = sum(favw)
                for h, f in zip(order[:3], favw):
                    ms.append(h); ps.append(w * local * 0.9 * f / tot)
                for h in order:
                    ms.append(h); ps.append(w * local * 0.1 / len(order))
            rest = w * (1 - local)
            for t, wt in nb:
                cand = self._away(t, c)
                if not cand:
                    continue
                k = min(len(cand), 2)
                sel = [cand[j] for j in rng.permutation(len(cand))[:k]]
                for h in sel:
                    ms.append(h); ps.append(rest * wt / k)
            prof[c] = (ms, ps)
        self._profiles[key] = prof
        return prof

    def local_menu(self, member, card_type, rng):
        mix = DEBIT_MIX if card_type == "Debit" else CREDIT_MIX
        prof = self.profile(member, rng)
        ms, ps = [], []
        for c, wc in mix.items():
            m_, p_ = prof[c]
            ms.extend(m_)
            ps.extend([wc * x for x in p_])
        ms = np.array(ms)
        ps = np.array(ps, dtype=float)
        return ms, ps / ps.sum()

    def add(self, slot, days, merch, hour=None, term=None):
        days = np.asarray(days, np.int64)
        if not len(days):
            return
        self.parts.append((slot, days, np.asarray(merch, np.int32),
                           None if hour is None else np.asarray(hour, np.float64),
                           None if term is None else np.asarray(term, np.int32)))

    # per-slot activity -----------------------------------------------------------------------------
    def run_slot(self, s, member, trips_m, rng):
        dayw = np.array([0.92, 0.92, 0.95, 1.0, 1.18, 1.22, 0.81])[WEEKDAY].copy()
        for (_, di, a, b) in trips_m:
            dayw[a:b + 1] = 0.04
        menu_m, menu_p = self.local_menu(member, s.card_type, rng)
        n = rng.poisson(s.rate * dayw.sum())
        days = rng.choice(ND, size=n, p=dayw / dayw.sum())
        merch = rng.choice(menu_m, size=n, p=menu_p)
        self.add(s.slot, days, merch)
        for (_, di, a, b) in trips_m:
            dest = places.DESTINATIONS[di]
            cand = self.dest_cand[dest[0]]
            per_day = 2.3 if s.road else 0.45 * s.rate
            k = rng.poisson(per_day * (b - a + 1))
            if k:
                self.add(s.slot, rng.integers(a, b + 1, k), rng.choice(cand, size=k))

    def run_plaza(self, s, member, rng, commuter):
        fuel, coffee, wash = self.cat.fuel, self.cat.coffee, self.cat.wash
        opt = np.array(fuel["terminals"])
        stops = []
        if commuter:
            s_rate = float(np.clip(rng.beta(2.4, 3.6), 0.08, 0.85))
            vac = int(rng.integers(day_of(dt.date(2026, 6, 22)), day_of(dt.date(2026, 8, 24))))
            vac_len = int(rng.choice([5, 9, 12, 16]))
            u = rng.random(ND)
            for d in range(ND):
                if WORKDAY[d] and not (vac <= d < vac + vac_len) and u[d] < s_rate:
                    stops.append((d, "am" if rng.random() < 0.72 else "pm"))
            u2 = rng.random(ND)
            for d in range(ND):
                if WEEKDAY[d] >= 5 and u2[d] < 0.05:
                    stops.append((d, "day"))
            p_f, p_c_am, p_c_pm, p_w = 0.43, 0.78, 0.34, 0.016
        else:
            k = 1 + int(rng.poisson(0.65))
            wts = np.where(WEEKDAY >= 4, 2.0, 1.0) * np.where(HOLIDAY, 2.5, 1.0)
            for d in rng.choice(ND, size=k, replace=False, p=wts / wts.sum()):
                stops.append((int(d), "day"))
            p_f, p_c_am, p_c_pm, p_w = 0.62, 0.50, 0.50, 0.035
        D_, M_, H_, T_ = [], [], [], []
        for d, when in stops:
            if when == "am":
                h0 = 5.8 + 2.6 * rng.random()
            elif when == "pm":
                h0 = 16.2 + 2.9 * rng.random()
            else:
                h0 = 8.5 + 10.5 * rng.random()
            if rng.random() < p_f:
                pos = int(rng.choice(8, p=OPT_PICK))
                if pos == 5 and (d == day_of(W.PUMP_OUT_OF_SERVICE) or
                                 day_of(W.PUMP_DISPENSER_REPAIR[0]) <= d <= day_of(W.PUMP_DISPENSER_REPAIR[1])):
                    pos = 4 if rng.random() < 0.5 else 6
                D_.append(d); M_.append(fuel["idx"]); H_.append(h0); T_.append(opt[pos])
                h0 += 0.12 + 0.05 * rng.random()
            pc = p_c_am if when == "am" else p_c_pm
            if rng.random() < pc and 5.6 <= h0 <= 20.8:
                D_.append(d); M_.append(coffee["idx"]); H_.append(h0); T_.append(coffee["terminals"][0])
                h0 += 0.05
            if rng.random() < p_w and 7.0 <= h0 <= 20.8:
                D_.append(d); M_.append(wash["idx"]); H_.append(h0 + 0.1); T_.append(wash["terminals"][0])
        self.add(s.slot, D_, M_, H_, T_)

    def run_ottawa(self, s, member, rng):
        fav = rng.choice(self.ottawa_cand, size=8, replace=False)
        u = rng.random(ND)
        days = [d for d in range(ND) if WORKDAY[d] and u[d] < 0.30]
        if not days:
            return
        merch = rng.choice(fav, size=len(days), p=[.25, .2, .15, .12, .1, .08, .05, .05])
        hrs = 11.4 + 2.2 * rng.random(len(days))
        self.add(s.slot, days, merch, hrs)

    # finalize --------------------------------------------------------------------------------------
    def finalize(self, rng):
        slot = np.concatenate([np.full(len(p[1]), p[0], np.int32) for p in self.parts])
        days = np.concatenate([p[1] for p in self.parts])
        merch = np.concatenate([p[2] for p in self.parts])
        hour = np.concatenate([p[3] if p[3] is not None else np.full(len(p[1]), np.nan) for p in self.parts])
        term = np.concatenate([p[4] if p[4] is not None else np.full(len(p[1]), -2, np.int32) for p in self.parts])
        n = len(slot)
        S = self.slots
        credit = (S.card_type.values == "Credit")[slot]
        nfc = S.nfc.values[slot]
        p_tap = S.p_tap.values[slot]
        cats = self.m_cat[merch]
        catid = self.m_catid[merch]
        # amounts and kinds
        amount = np.zeros(n)
        kind = np.full(n, K_PUR, np.int8)
        for c in sorted(set(cats.tolist())):
            sel = np.nonzero(cats == c)[0]
            k = len(sel)
            if c == "atm":
                vals = rng.choice([20, 40, 60, 80, 100, 120, 140, 160, 200, 240, 300, 400],
                                  size=k, p=[.08, .14, .12, .09, .17, .06, .04, .05, .12, .03, .07, .03])
                amount[sel] = vals + self.m_surcharge[merch[sel]]
                kind[sel] = K_ATM
                bal = sel[rng.random(k) < 0.07]
                amount[bal] = 0.0
                kind[bal] = K_BAL
            elif c == "cnp":
                amount[sel] = rng.lognormal(np.log(38.0), 0.9, k)
                kind[sel] = K_CNP
            elif c == "fuel":
                amount[sel] = np.clip(rng.lognormal(np.log(61.0), 0.28, k), 12, 148)
                kind[sel] = K_PUMP
            else:
                spec = places.CATS[c]
                mult = np.where(credit[sel], 1.15, 1.0) * np.where(merch[sel] == self.cat.lombard["idx"], 1.6, 1.0)
                amount[sel] = rng.lognormal(np.log(spec[1]), spec[2], k) * mult
                if c not in ("grocery", "dental", "auto", "salon", "parking", "carwash", "hotel"):
                    ref = sel[rng.random(k) < 0.008]
                    kind[ref] = K_REF
        amount = np.round(np.where(kind == K_BAL, 0.0, np.maximum(amount, 1.25)), 2)
        # terminals
        need = term == -2
        has = self.m_nterm[merch] > 0
        pick = need & has
        term[pick] = self.m_first_term[merch[pick]] + (rng.random(int(pick.sum())) * self.m_nterm[merch[pick]]).astype(np.int32)
        term[need & ~has] = -1
        lom = need & (merch == self.cat.lombard["idx"])
        if lom.any():
            pos = rng.choice(10, size=int(lom.sum()), p=[0.13, 0.12, 0.11, 0.09] + [0.55 / 6] * 6)
            term[lom] = self.cat.lombard["terminals"][0] + pos
        # plaza fuel drawn from the menu (Kemptville members fuelling at the plaza is not in the menu)
        # times
        lo = np.array([HOURS[c][0] for c in self.cat_list])[catid]
        hi = np.array([HOURS[c][1] for c in self.cat_list])[catid]
        h = np.where(np.isnan(hour), lo + (hi - lo) * rng.beta(2.2, 2.2, n), hour)
        t = days * DAY + np.floor(h * 3600).astype(np.int64)
        # entry modes
        e = np.full(n, E05, np.int8)
        limit = np.where(credit, 250.0, 100.0)
        hold = np.where(credit, 150.0, 100.0)
        tap_ok = np.where(term >= 0, self.t_tap[np.maximum(term, 0)], False)
        opt6 = self.cat.fuel["terminals"][5]
        tap_ok = tap_ok | ((term == opt6) & (days > day_of(W.PUMP_OUT_OF_SERVICE)))
        amt_lim = np.where(kind == K_PUMP, hold, amount)
        # pay-at-pump and coffee: tapping is habitual
        p_eff = np.where(kind == K_PUMP, 1 - (1 - p_tap) * 0.12, np.where(cats == "coffee", 1 - (1 - p_tap) * 0.45, p_tap))
        tap = tap_ok & nfc & (amt_lim <= limit) & (rng.random(n) < p_eff) & (kind != K_ATM) & (kind != K_BAL) & \
            (kind != K_REF)
        e[tap] = E07
        us = self.m_country[merch] == "US"
        swipe = us & ~tap & (rng.random(n) < np.where(kind == K_ATM, 0.12, 0.06))
        e[swipe] = E90
        fb = (~tap) & (~us) & (rng.random(n) < 0.0028) & (kind != K_ATM) & (kind != K_BAL)
        e[fb] = E80
        kd = (~tap) & (~us) & (~fb) & (rng.random(n) < 0.0009) & (kind == K_PUR)
        e[kd] = E01
        cnp = kind == K_CNP
        e[cnp] = np.where(rng.random(int(cnp.sum())) < 0.86, E81, E01)
        ev = pd.DataFrame({"slot": slot, "t": t, "merch": merch, "term": term, "kind": kind,
                           "amount": amount, "entry": e})
        return ev


def simulate():
    rng = np.random.default_rng(W.SEED)
    cat = places.build_catalog()
    members = build_people(rng, cat)
    slots = build_slots(rng, members)
    lc = lifecycle(np.random.default_rng(W.SEED + 3), slots)
    trips = build_trips(np.random.default_rng(W.SEED + 5), members)
    trips_by_member = {}
    for tr in trips:
        trips_by_member.setdefault(tr[0], []).append(tr)
    b = Builder(cat, members, slots, trips, rng)
    arng = np.random.default_rng(W.SEED + 11)
    mem = list(members.itertuples())
    for s in slots.itertuples():
        m = mem[s.member]
        b.run_slot(s, m, trips_by_member.get(s.member, []), arng)
        if s.road and (m.commuter or m.occasional):
            b.run_plaza(s, m, arng, commuter=bool(m.commuter))
        if s.road and m.commuter:
            b.run_ottawa(s, m, arng)
    ev = b.finalize(np.random.default_rng(W.SEED + 13))
    ev = ev.sort_values(["t", "slot", "merch"], kind="mergesort").reset_index(drop=True)
    sim = Sim()
    sim.cat, sim.members, sim.slots, sim.lifecycle, sim.trips, sim.ev, sim.builder = cat, members, slots, lc, trips, ev, b
    return sim


if __name__ == "__main__":
    import time
    t0 = time.time()
    s = simulate()
    print(len(s.ev), "events", round(time.time() - t0, 1), "s")
    print(s.slots.card_type.value_counts())
    print(s.members[["commuter", "occasional", "lombard", "traveller"]].sum())
