"""Simulate the province's 2026 cremations and the crematoria's own operating records (controller cycles, abatement
plant logs, accounts receivable). One RNG stream per record family, so a change in one leaves the others' bytes."""
import datetime as dt
import math

import numpy as np

import world as W

D0 = dt.date(2025, 11, 12)
D1 = dt.date(2027, 1, 31)


def _rng(tag):
    return np.random.default_rng([W.SEED, sum(ord(c) * (i + 1) for i, c in enumerate(tag))])


def death_dates(rng, n):
    """Deaths over 1 Nov 2025 to 31 Jan 2027 with the winter excess."""
    days = (dt.date(2027, 1, 31) - dt.date(2025, 11, 1)).days + 1
    t = np.arange(days)
    doy = np.array([(dt.date(2025, 11, 1) + dt.timedelta(int(x))).timetuple().tm_yday for x in t])
    w = 1 + 0.16 * np.cos(2 * math.pi * (doy - 15) / 365.25)
    w = w / w.sum()
    pick = rng.choice(days, size=n, p=w)
    return [dt.date(2025, 11, 1) + dt.timedelta(int(x)) for x in pick]


def decedents():
    """Every cremation whose permit was returned in the extract window: one dict per cremation."""
    rng = _rng("decedents")
    rows = []
    for ci, c in enumerate(W.CREMATORIA):
        code, fac, name, op, ncrem, n2026, mu, sd, st, comm = c
        n = int(round(n2026 * 15.0 / 12.0 * 1.012))           # 15 months of deaths feed the window
        deaths = death_dates(rng, n)
        ages = rng.normal(mu, sd, n)
        young = rng.random(n) < 0.05
        ages = np.where(young, rng.uniform(30, 62, n), ages)
        child = rng.random(n) < 0.004
        ages = np.where(child, rng.integers(0, 18, n), ages)
        ages = np.clip(np.round(ages), 0, 104).astype(int)
        pf = np.clip(0.42 + (ages - 70) * 0.006, 0.40, 0.66)
        sex = np.where(rng.random(n) < pf, "F", "M")
        gap = np.clip(np.round(rng.lognormal(math.log(6.5), 0.45, n)), 2, 30).astype(int)
        for d, a, s, g in zip(deaths, ages, sex, gap):
            dc = d + dt.timedelta(int(g))
            if dc.weekday() == 6:
                dc += dt.timedelta(1)
            if not (D0 <= dc <= D1):
                continue
            rows.append({"ci": ci, "code": code, "age": int(a), "sex": str(s), "death": d, "cremation": dc})
    return rows


def abated(c, d):
    """Was the crematorium's abatement plant commissioned before the cremation date?"""
    st, comm = c[8], c[9]
    if st == "U":
        return False
    return d > dt.date.fromisoformat(comm)


# ---------------------------------------------------------------- cremator controller cycles (all crematoria)
def cycles(rows):
    """Each 2026 cremation charged into one of its crematorium's cremators. Local times (Eastern, DST)."""
    rng = _rng("cycles")
    by = {}
    for k, r in enumerate(rows):
        if r["cremation"].year == W.YEAR:
            by.setdefault((r["ci"], r["cremation"]), []).append(k)
    out = []
    for (ci, day), ks in sorted(by.items()):
        ncrem = W.CREMATORIA[ci][4]
        free = [dt.datetime.combine(day, dt.time(7, 0)) + dt.timedelta(minutes=int(rng.integers(5, 50)))
                for _ in range(ncrem)]
        if day.weekday() == 0:                       # a cold hearth after the weekend: each cremator is preheated
            for j in range(min(ncrem, len(ks))):
                s0 = dt.datetime.combine(day, dt.time(5, 50)) + dt.timedelta(minutes=int(rng.integers(0, 25)))
                out.append({"k": None, "ci": ci, "cremator": j + 1, "start": s0,
                            "end": s0 + dt.timedelta(minutes=int(rng.integers(48, 66))), "type": "PREHEAT",
                            "gas": round(float(rng.normal(14.0, 2.0)), 1), "tmax": int(rng.integers(815, 860))})
                free[j] = max(free[j], out[-1]["end"] + dt.timedelta(minutes=int(rng.integers(4, 15))))
        for k in ks:
            j = int(np.argmin([f.timestamp() for f in free]))
            start = free[j] + dt.timedelta(minutes=int(rng.integers(0, 12)))
            a = rows[k]["age"]
            dur = int(round(rng.normal(92 if a >= 18 else 48, 11)))
            dur = max(35 if a < 18 else 62, min(150, dur))
            end = start + dt.timedelta(minutes=dur)
            free[j] = end + dt.timedelta(minutes=int(rng.integers(18, 40)))       # cooling and raking out
            out.append({"k": k, "ci": ci, "cremator": j + 1, "start": start, "end": end, "type": "CREMATION",
                        "gas": round(float(rng.normal(31.0 if a >= 18 else 19.0, 4.2)), 1),
                        "tmax": int(rng.integers(862, 931))})
            rows[k]["cycle"] = len(out) - 1
    return out


# ---------------------------------------------------------------- abatement plant logs (abated crematoria)
def plant_logs(rows, cyc):
    """Per plant: events and 10-minute inlet temperatures from commissioning (or 1 Jan) to 31 Dec. A differential-
    pressure alarm that does not clear within five minutes opens the bypass damper until the operator resets the
    plant; the damper's own movement is not logged, only the alarm, the reset and the inlet temperature."""
    rng = _rng("plant")
    plants = {}
    for ci, c in enumerate(W.CREMATORIA):
        if c[8] == "U":
            continue
        t0 = dt.datetime(W.YEAR, 1, 1) if c[8] == "A" else dt.datetime.combine(dt.date.fromisoformat(c[9]), dt.time(9, 0))
        t1 = dt.datetime(W.YEAR + 1, 1, 1)
        mine = sorted((x for x in cyc if x["ci"] == ci and x["start"] >= t0), key=lambda x: x["start"])
        firing = [(x["start"], x["end"]) for x in mine]
        crem_firing = [(x["start"], x["end"]) for x in mine if x["type"] == "CREMATION"]
        edges = sorted([s for s, e in firing] + [e for s, e in firing])

        def clear(t, pad=25):
            """No cycle starts or ends within pad minutes of t."""
            import bisect
            i = bisect.bisect_left(edges, t - dt.timedelta(minutes=pad))
            return not (i < len(edges) and edges[i] <= t + dt.timedelta(minutes=pad))

        def busy(t):
            return any(s <= t <= e for s, e in firing)
        events, bypass, manual = [], [], []
        quarters = [(dt.datetime(W.YEAR, m, 1), dt.datetime(W.YEAR + (m == 10), (m + 3 - 1) % 12 + 1, 1))
                    for m in (1, 4, 7, 10)]
        for q0, q1 in quarters:
            a0, a1 = max(q0, t0), q1
            if a0 >= a1:
                continue
            qfire = [x for x in crem_firing if a0 <= x[0] < a1]
            # automatic bypasses: alarm during a firing, cleared late, reset 45 to 200 minutes on
            n_auto = int(rng.integers(2, 5))
            tries = 0
            while n_auto and tries < 4000:
                tries += 1
                s, e = qfire[int(rng.integers(0, len(qfire)))]
                t_al = s + dt.timedelta(minutes=int(rng.integers(8, 70)))
                t_open = t_al + dt.timedelta(minutes=5)
                t_reset = t_open + dt.timedelta(minutes=int(rng.integers(70, 235)))
                if not (clear(t_open) and clear(t_reset) and clear(t_al, 10)):
                    continue
                if any(not (t_reset < b0 - dt.timedelta(hours=3) or t_al > b1 + dt.timedelta(hours=3)) for b0, b1 in bypass + manual):
                    continue
                bypass.append((t_open, t_reset))
                t_clr = t_al + dt.timedelta(minutes=int(rng.integers(9, 30)))
                events += [(t_al, "ALARM", "DP HIGH 1.9 kPa"), (t_clr, "ALARM CLEARED", "DP HIGH"),
                           (t_reset, "PLANT RESET", "operator")]
                n_auto -= 1
            # alarms that clear inside five minutes: no bypass
            for _ in range(int(rng.integers(3, 8))):
                s, e = qfire[int(rng.integers(0, len(qfire)))]
                t_al = s + dt.timedelta(minutes=int(rng.integers(10, 60)))
                if any(b0 - dt.timedelta(minutes=30) <= t_al <= b1 + dt.timedelta(minutes=30) for b0, b1 in bypass + manual):
                    continue
                events += [(t_al, "ALARM", "DP HIGH %.1f kPa" % float(rng.uniform(1.6, 2.1))),
                           (t_al + dt.timedelta(minutes=int(rng.integers(1, 5)), seconds=int(rng.integers(0, 59))),
                            "ALARM CLEARED", "DP HIGH")]
            # maintenance: manual bypass, logged, sometimes over a cremation
            for _ in range(int(rng.integers(1, 3))):
                for _t in range(500):
                    d = a0.date() + dt.timedelta(int(rng.integers(0, max(1, (a1 - a0).days - 1))))
                    on = dt.datetime.combine(d, dt.time(int(rng.integers(6, 15)), int(rng.integers(0, 60))))
                    off = on + dt.timedelta(minutes=int(rng.integers(70, 330)))
                    if a0 <= on and off < a1 and clear(on) and clear(off) and not any(
                            not (off < b0 - dt.timedelta(hours=3) or on > b1 + dt.timedelta(hours=3)) for b0, b1 in bypass + manual):
                        manual.append((on, off))
                        events += [(on, "MANUAL BYPASS ON", "maintenance"), (off, "MANUAL BYPASS OFF", "maintenance")]
                        break
            # routine
            for _ in range(int(rng.integers(2, 5))):
                d = a0 + dt.timedelta(minutes=int(rng.integers(0, int((a1 - a0).total_seconds() // 60) - 1)))
                events.append((d, "CARBON HOPPER FILLED", "%d kg" % int(rng.choice([25, 25, 50]))))
            if rng.random() < 0.6:
                d = a0 + dt.timedelta(minutes=int(rng.integers(0, int((a1 - a0).total_seconds() // 60) - 1)))
                events.append((d, "ALARM", "INLET TEMP HIGH 236 C"))
                events.append((d + dt.timedelta(minutes=int(rng.integers(2, 9))), "ALARM CLEARED", "INLET TEMP HIGH"))
        # weekend shutdowns: the plant is stopped after Saturday's last cycle and started before Monday's preheat
        stops = []
        sat = t0.date() + dt.timedelta((5 - t0.weekday()) % 7)
        while sat < t1.date() - dt.timedelta(days=2):
            if rng.random() < 0.22:
                last = max([e for s, e in firing if s.date() == sat] or [dt.datetime.combine(sat, dt.time(12, 0))])
                stop = max(last + dt.timedelta(minutes=int(rng.integers(35, 90))),
                           dt.datetime.combine(sat, dt.time(16, int(rng.integers(0, 60)))))
                start = dt.datetime.combine(sat + dt.timedelta(days=2), dt.time(4, int(rng.integers(30, 59))))
                if not any(s < start and e > stop for s, e in firing) and not any(
                        b0 < start + dt.timedelta(hours=3) and b1 > stop - dt.timedelta(hours=3) for b0, b1 in bypass + manual):
                    stops.append((stop, start))
                    events += [(stop, "PLANT STOP", "weekend"), (start, "PLANT START", "weekend")]
            sat += dt.timedelta(days=7)
        # inlet temperature every 10 minutes
        ticks = []
        t = t0.replace(minute=(t0.minute // 10) * 10, second=0)
        while t < t1:
            ticks.append(t)
            t += dt.timedelta(minutes=10)
        ts = np.array([x.timestamp() for x in ticks])
        fire = np.zeros(len(ts), bool)
        for s, e in firing:
            fire[np.searchsorted(ts, s.timestamp()):np.searchsorted(ts, e.timestamp(), side="right")] = True
        v = np.where(fire, 172.0, 137.0) + rng.normal(0, 6.5, len(ts))
        noise = rng.normal(0, 2.5, len(ts))
        rec = rng.normal(0, 8, len(ts))
        for b0, b1 in sorted(bypass + manual):
            i0 = np.searchsorted(ts, b0.timestamp())
            i1 = np.searchsorted(ts, b1.timestamp(), side="right")
            m = (ts[i0:i1] - b0.timestamp()) / 60.0
            v[i0:i1] = 30 + 120 * np.exp(-m / 6.0) + noise[i0:i1]
            j1 = np.searchsorted(ts, (b1 + dt.timedelta(minutes=12)).timestamp(), side="right")
            v[i1:j1] = 95 + rec[i1:j1]
        amb = rng.normal(0, 1.8, len(ts))
        for s0, s1 in stops:
            i0 = np.searchsorted(ts, s0.timestamp())
            i1 = np.searchsorted(ts, s1.timestamp(), side="right")
            m = (ts[i0:i1] - s0.timestamp()) / 60.0
            v[i0:i1] = 21 + 116 * np.exp(-m / 45.0) + amb[i0:i1]
            j1 = np.searchsorted(ts, (s1 + dt.timedelta(minutes=50)).timestamp(), side="right")
            m2 = (ts[i1:j1] - s1.timestamp()) / 60.0
            v[i1:j1] = 30 + 107 * (1 - np.exp(-m2 / 15.0)) + amb[i1:j1]
        temps = [(ticks[i], round(float(v[i]), 1)) for i in range(len(ts))]
        plants[ci] = {"events": sorted(events), "temps": temps, "auto": sorted(bypass), "manual": sorted(manual),
                      "stops": stops, "start": t0}
    return plants


# ---------------------------------------------------------------- accounts receivable (all crematoria)
FD_SURNAMES = ["Arbuckle", "Brennan", "Castellano", "Dufresne", "Eklund", "Fairweather", "Gauthier", "Halloran",
               "Iverson", "Jasinski", "Kowalchuk", "Lachance", "MacPhail", "Nadeau", "Ostrowski", "Pelletier",
               "Quinlan", "Rasmussen", "Sauvé", "Tremblay", "Ulrich", "Vandermeer", "Whitcombe", "Yaremko",
               "Zielinski", "Beaudoin", "Carrick", "Desrosiers", "Esposito", "Fitzhenry", "Grenier", "Hollingsworth",
               "Lindqvist", "McCrory", "Novak", "Paquette", "Redekop", "Strachan", "Thibodeau", "Wiebe"]
FD_SHAPES = ["%s Funeral Home", "%s & Sons Funeral Chapel", "%s Family Funeral Services", "%s Memorial Chapel",
             "%s-%s Funeral Home", "%s Funeral Home Ltd.", "%s & %s Funeral Directors"]
SERVICE_ITEMS = ("CHAP", "XTND", "ORGN", "WEBC", "MEMB", "SCAT", "CERT")
LAST_POSTING = dt.date(2027, 2, 19)          # every ledger and return carries postings to here at the extract
FIRST_POSTING = dt.date(2025, 12, 1)
INCLUDED = {code for code, _, inc in W.FEE_ITEMS if inc} | {"DIRC"}


def funeral_homes(rng):
    """The province's funeral homes (one pool; each crematorium serves some of them)."""
    out, seen = [], set()
    while len(out) < 74:
        sh = FD_SHAPES[int(rng.integers(0, len(FD_SHAPES)))]
        nm = sh % tuple(FD_SURNAMES[int(x)] for x in rng.choice(len(FD_SURNAMES), size=sh.count("%s"), replace=False))
        if nm.split(" ")[0] in {o.split(" ")[0] for o in out} and rng.random() < 0.7:
            continue
        if nm not in seen:
            seen.add(nm)
            out.append(nm)
    return out


def price_lists(rng):
    """One crematorium's fee schedule for 2025, 2026 and 2027; fees change on 1 January."""
    p = {"CREM": rng.uniform(820, 1150), "DIRC": rng.uniform(560, 720), "CHAP": rng.uniform(180, 320),
         "XTND": rng.uniform(32, 58), "ORGN": rng.uniform(85, 140), "WEBC": rng.uniform(75, 125),
         "MEMB": rng.uniform(60, 110), "SCAT": rng.uniform(70, 140), "CERT": rng.uniform(6, 11),
         "URN": rng.uniform(95, 450), "KEEP": rng.uniform(40, 180)}
    lists = {2025: {k: round(v * 20) / 20 for k, v in p.items()}}
    for y in (2026, 2027):
        rise = float(rng.choice([0.021, 0.025, 0.028, 0.031, 0.034, 0.037, 0.04, 0.045]))
        lists[y] = {k: round(max(v * (1 + rise), v + 0.05), 2) for k, v in lists[y - 1].items()}
    # a crematorium whose abatement plant entered service during 2026 charges a new schedule from the next day
    rise = float(rng.choice([0.012, 0.015, 0.018, 0.022]))
    lists["2026a"] = {k: round(max(v * (1 + rise), v + 0.05), 2) for k, v in lists[2026].items()}
    for y in lists:
        lists[y]["MREF"] = 35.0 if y != 2027 else 37.5          # the province sets the medical referee's fee
    return lists


def price_key(ci, d):
    c = W.CREMATORIA[ci]
    if d.year == 2026 and c[8] == "M" and abated(c, d):
        return "2026a"
    return d.year


def line_abated(ci, d):
    return abated(W.CREMATORIA[ci], d)


def _effects(cents, groups, kmax):
    """Every multiset of at most kmax lines (groups: list of (amount_cents, signature, count)) summing to cents:
    returns the set of their effects (signature -> cents) and how many there are."""
    groups = sorted(groups)
    eff, n = set(), 0

    def rec(start, left, k, acc):
        nonlocal n
        if left == 0:
            tot = {}
            for a, sig in acc:
                tot[sig] = tot.get(sig, 0) + a
            eff.add(tuple(sorted(tot.items())))
            n += 1
            return
        if k == 0:
            return
        for gi in range(start, len(groups)):
            a, sig, cnt = groups[gi]
            if a > left:
                break
            used = sum(1 for x in acc if x == (a, sig))
            if used >= cnt:
                continue
            rec(gi, left - a, k - 1, acc + [(a, sig)])
    rec(0, cents, kmax, [])
    return eff, n


def ledger(ci):
    """The receivables ledger a crematorium's fees sit in: an operator's own, or the crematorium's return."""
    return W.LEDGER_OF.get(W.CREMATORIA[ci][3], W.CREMATORIA[ci][0])


def account_window(lines, idx, key, posted, days=120, after=10):
    """The account's lines (one funeral home in one ledger) whose service fell in the days before the posting (and
    the few days after it, where a weekly return dates the credit by its week)."""
    import bisect
    lst = idx.get(key, [])
    dates = [lines[i]["date"] for i in lst]
    lo = bisect.bisect_left(dates, posted - dt.timedelta(days=days))
    hi = bisect.bisect_right(dates, posted + dt.timedelta(days=after))
    return lst[lo:hi]


def signature(ln):
    return (ln["ci"], ln["date"].year, line_abated(ln["ci"], ln["date"]), ln["item"] in INCLUDED)


def credit_effects(lines, window, cents, kmax=3):
    g = {}
    for i in window:
        ln = lines[i]
        key = (int(round(ln["amount"] * 100)), signature(ln))
        g[key] = g.get(key, 0) + 1
    return _effects(cents, [(a, s, c) for (a, s), c in g.items()], kmax)


def _levy(lines, credits, ci):
    """A crematorium's levy as the scheme rules set it, from the generator's records."""
    base = {False: 0, True: 0}
    for ln in lines:
        if ln["ci"] == ci and ln["posted"] >= FIRST_POSTING and ln["date"].year == W.YEAR and ln["item"] in INCLUDED:
            base[line_abated(ci, ln["date"])] += int(round(ln["amount"] * 100))
    for c in credits:
        for p in c["lines"]:
            ln = lines[p]
            if ln["ci"] == ci and ln["date"].year == W.YEAR and ln["item"] in INCLUDED:
                base[line_abated(ci, ln["date"])] -= int(round(ln["amount"] * 100))
    return int(np.floor((base[False] * W.LEVY_UNABATED + base[True] * W.LEVY_ABATED) / 100 + 0.5))


def receivables(rows):
    """Bookings, invoice lines and credits for every cremation from December 2025 to January 2027. A credit an
    operator allows after a funeral director queries a statement is posted to the account with no booking: its amount
    is the exact sum of the lines it reverses, which can sit on several of that funeral director's bookings."""
    rng = _rng("ar")
    homes = funeral_homes(rng)
    fds, books, lines, credits, prices = {}, [], [], [], {}
    for ci, c in enumerate(W.CREMATORIA):
        nfd = int(np.clip(round(c[5] / 110 + rng.normal(0, 2.5)), 5, 34))
        fds[ci] = [int(x) for x in rng.choice(len(homes), size=nfd, replace=False)]
        prices[ci] = price_lists(rng)
        share = rng.dirichlet(np.ones(nfd) * 1.3)
        for k, r in enumerate(rows):
            if r["ci"] != ci or r["cremation"] < dt.date(2025, 12, 1):
                continue
            pl = prices[ci][price_key(ci, r["cremation"])]
            fd = int(rng.choice(nfd, p=share))
            direct = rng.random() < 0.31 and r["age"] >= 18
            child = r["age"] < 18
            items = [("DIRC" if direct else "CREM", 1)]
            if not direct:
                items.append(("CHAP", 1))
                if rng.random() < 0.10: items.append(("XTND", int(rng.integers(1, 4))))
                if rng.random() < 0.17: items.append(("ORGN", 1))
                if rng.random() < 0.28: items.append(("WEBC", 1))
            if rng.random() < 0.08: items.append(("MEMB", 1))
            if rng.random() < 0.12: items.append(("SCAT", 1))
            if rng.random() < 0.22: items.append(("CERT", int(rng.integers(2, 7))))
            if rng.random() < 0.29: items.append(("URN", 1))
            if rng.random() < 0.05: items.append(("KEEP", 1))
            items.append(("MREF", 1))
            b = len(books)
            posted = r["cremation"] + dt.timedelta(int(rng.integers(-6, 4)))
            books.append({"b": b, "k": k, "ci": ci, "fd": fd, "home": fds[ci][fd], "date": r["cremation"],
                          "direct": direct, "posted": posted, "child": child})
            for code, q in items:
                amt = 0.0 if (child and code in ("CREM", "CHAP")) else round(pl[code] * q, 2)
                lines.append({"b": b, "ci": ci, "fd": fd, "home": fds[ci][fd], "date": r["cremation"], "item": code,
                              "qty": q,
                              "unit": 0.0 if amt == 0 and code in ("CREM", "CHAP") else pl[code], "amount": amt,
                              "posted": posted})
    idx = {}
    for i, ln in enumerate(lines):
        idx.setdefault((ledger(ln["ci"]), ln["home"]), []).append(i)
    for key in idx:
        idx[key].sort(key=lambda i: (lines[i]["date"], i))
    used = set()
    book_tot = {}
    for ln in lines:
        t = book_tot.setdefault(ln["b"], [0, 0, 0])
        cts = int(round(ln["amount"] * 100))
        t[0] += cts
        t[1] += cts if ln["item"] in INCLUDED else 0
        t[2] += cts if ln["item"] in SERVICE_ITEMS else 0

    def ok_multi(ci, fd, pick, posted, cents):
        key = (ledger(ci), fds[ci][fd])
        win = account_window(lines, idx, key, posted)
        if any(int(round(lines[i]["amount"] * 100)) == cents for i in win):
            return False                                     # a single line of the account equals it
        bks = {lines[i]["b"] for i in win}
        if any(cents in book_tot[b] for b in bks):
            return False                                     # a booking's total equals it
        true = {}
        for p in pick:
            s = signature(lines[p])
            true[s] = true.get(s, 0) + int(round(lines[p]["amount"] * 100))
        return unique_effect(key, posted, cents, {tuple(sorted(true.items()))})

    def unique_effect(key, posted, cents, want):
        """Every subset of the account's lines that sums to the credit has the credited lines' effect: up to four
        lines in the 120 and 200 days before it, up to three anywhere on the account."""
        for days, k in ((120, 4), (200, 4)):
            if credit_effects(lines, account_window(lines, idx, key, posted, days), cents, k)[0] != want:
                return False
        return credit_effects(lines, idx[key], cents, 3)[0] == want

    for ci, c in enumerate(W.CREMATORIA):
        mine = [i for i, ln in enumerate(lines) if ln["ci"] == ci]
        svc = [i for i in mine if lines[i]["item"] in SERVICE_ITEMS and lines[i]["amount"] > 0 and
               lines[i]["posted"] >= FIRST_POSTING]
        # credits raised on a booking: one line reversed, its booking and item carried
        for i in rng.choice([i for i in mine if lines[i]["item"] in SERVICE_ITEMS + ("URN", "KEEP") and
                             lines[i]["amount"] > 0], size=int(c[5] * 0.013), replace=False):
            i = int(i)
            ln = lines[i]
            posted = ln["date"] + dt.timedelta(int(rng.integers(2, 31)))
            if i in used or posted > LAST_POSTING:
                continue
            used.add(i)
            credits.append({"ci": ci, "fd": ln["fd"], "home": ln["home"], "posted": posted,
                            "amount": ln["amount"], "b": ln["b"], "item": ln["item"], "lines": [i], "kind": "booking"})
        # credits on the account, after a statement query: by the month of the services they reverse
        def make(yy, mm, posted_in, pool_used):
            pool = [i for i in svc if lines[i]["date"].year == yy and lines[i]["date"].month == mm and
                    i not in used and i not in pool_used]
            for _t in range(200):
                first = lines[int(rng.choice(pool))]
                same = [i for i in pool if lines[i]["fd"] == first["fd"] and
                        abs((lines[i]["date"] - first["date"]).days) <= 18]
                m = int(rng.choice([2, 2, 3]))
                if len({lines[i]["b"] for i in same}) < m:
                    continue
                pick, bs = [], set()
                for x in rng.permutation(same):
                    x = int(x)
                    if lines[x]["b"] not in bs:
                        pick.append(x)
                        bs.add(lines[x]["b"])
                    if len(pick) == m:
                        break
                last = max(lines[p]["date"] for p in pick)
                if posted_in is None:
                    nx = dt.date(yy + (mm == 12), mm % 12 + 1, 1)
                    posted = nx + dt.timedelta(int(rng.integers(6, 50)))
                else:
                    py, pm = posted_in
                    posted = dt.date(py, pm, int(rng.integers(5 if pm == 1 else 2, 29 if pm == 1 else 24)))
                posted = max(posted, last + dt.timedelta(days=9))
                if posted > LAST_POSTING or (posted_in and posted.month != posted_in[1]):
                    continue
                cents = sum(int(round(lines[p]["amount"] * 100)) for p in pick)
                if not ok_multi(ci, first["fd"], pick, posted, cents):
                    continue
                return {"ci": ci, "fd": first["fd"], "home": first["home"], "posted": posted, "amount": cents / 100,
                        "b": None, "item": None, "lines": pick, "kind": "account"}
            return None

        for mm in range(2, 12):
            for _ in range(int(rng.poisson(c[5] / 12 * 0.0042))):
                cr = make(2026, mm, None, set())
                if cr:
                    used.update(cr["lines"])
                    credits.append(cr)
        # the months either side of the year end
        for attempt in range(60):
            plan = [((2025, 12), (2026, 1), int(rng.integers(0, 2))), ((2025, 12), (2026, 2), int(rng.integers(0, 2))),
                    ((2026, 1), (2026, 2), int(rng.integers(0, 2))), ((2026, 12), (2027, 1), int(rng.integers(1, 3))),
                    ((2026, 12), (2027, 2), int(rng.integers(1, 3))), ((2027, 1), (2027, 2), int(rng.integers(1, 3)))]
            got, taken = [], set()
            for (yy, mm), pin, k in plan:
                for _ in range(k):
                    cr = make(yy, mm, pin, taken)
                    if cr:
                        taken.update(cr["lines"])
                        got.append(cr)
            # the plain routes for the account's credits must each miss the levy by five dollars or more
            def err(route):
                e = 0.0
                for cr in got + [x for x in credits if x["ci"] == ci and x["kind"] == "account"]:
                    p = cr["posted"]
                    if route == "posted":
                        d = p
                    elif route == "month_before":
                        d = p.replace(day=1) - dt.timedelta(days=1)
                    else:
                        d = dt.date(p.year - 1, 12, 15) if p.month in (1, 2) else p
                    for q in cr["lines"]:
                        ln = lines[q]
                        rt_g = W.LEVY_ABATED if line_abated(ci, ln["date"]) else W.LEVY_UNABATED
                        rt_w = W.LEVY_ABATED if line_abated(ci, d) else W.LEVY_UNABATED
                        e += ln["amount"] * ((ln["date"].year == 2026) * rt_g - (d.year == 2026) * rt_w)
                return e
            if all(abs(err(rt)) >= 5 for rt in ("posted", "month_before", "year_before")):
                break
        used.update(taken)
        credits.extend(got)
            # a single line credited on the account (a webcast refunded, an urn returned): one line equals it
        for i in rng.choice([i for i in mine if lines[i]["item"] in ("WEBC", "ORGN", "URN", "KEEP", "SCAT") and
                             i not in used and lines[i]["posted"] >= FIRST_POSTING],
                            size=max(1, int(c[5] * 0.003)), replace=False):
            i = int(i)
            ln = lines[i]
            posted = ln["date"] + dt.timedelta(int(rng.integers(12, 45)))
            if posted > LAST_POSTING:
                continue
            cents = int(round(ln["amount"] * 100))
            if not unique_effect((ledger(ci), ln["home"]), posted, cents, {((signature(ln), cents),)}):
                continue
            used.add(i)
            credits.append({"ci": ci, "fd": ln["fd"], "home": ln["home"], "posted": posted, "amount": ln["amount"], "b": None,
                            "item": None, "lines": [i], "kind": "account1"})
        # a levy that falls on a round hundred is moved off it by one more credit on a booking (every route nets it)
        while _levy(lines, credits, ci) % 100 == 0:
            pool = [i for i in mine if lines[i]["item"] in SERVICE_ITEMS and lines[i]["amount"] > 0 and i not in used
                    and lines[i]["date"].year == W.YEAR and lines[i]["date"].month in range(3, 11)]
            i = int(rng.choice(pool))
            used.add(i)
            ln = lines[i]
            credits.append({"ci": ci, "fd": ln["fd"], "home": ln["home"],
                            "posted": ln["date"] + dt.timedelta(int(rng.integers(2, 31))), "amount": ln["amount"],
                            "b": ln["b"], "item": ln["item"], "lines": [i], "kind": "booking"})
    return {"homes": homes, "fds": fds, "books": books, "lines": lines, "credits": credits, "prices": prices,
            "idx": idx}
