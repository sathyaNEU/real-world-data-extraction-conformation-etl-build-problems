"""The simulation: every person registered in the in-play municipalities on 1 January 2026 with a full register
history; the national Register Coverage Audit 2026 (a simple random sample of the national register, each sampled
person verified in the field as living or not in the registered municipality on 1 January 2026); and the 2025
deregistration traffic the municipalities sent to the national hub (departures abroad, deaths, removals), with the
hub's acknowledgements and the records the municipalities keep of former residents living abroad."""
import datetime as dt

import numpy as np

import world as W

D0 = dt.date(1900, 1, 1)


def rng(seed, *parts):
    return np.random.default_rng([seed, *parts])


def ymd(d):
    return d.strftime("%Y%m%d")


def years_before(d, years, extra_days=0):
    """the date `years` calendar years and `extra_days` days before d (29 February falls back to the 28th)"""
    y = d.year - years
    try:
        out = d.replace(year=y)
    except ValueError:
        out = d.replace(year=y, day=28)
    return out - dt.timedelta(days=int(extra_days))


def completed_years(start, ref=W.REF):
    y = ref.year - start.year - ((ref.month, ref.day) < (start.month, start.day))
    return max(0, y)


class Keys:
    """pseudonymised person keys: nine digits passing the eleven test, unique across the whole world (each stream
    skips every key already issued by any stream; pools() starts the world and clears the record)"""
    issued = set()

    def __init__(self, seed):
        self.r = rng(seed, 1)

    def __call__(self):
        while True:
            d = [int(v) for v in self.r.integers(0, 10, 8)]
            if d[0] == 0:
                continue
            s = sum(x * w for x, w in zip(d, range(9, 1, -1)))
            last = s % 11
            if last == 10:
                continue
            k = "".join(map(str, d)) + str(last)
            if k not in Keys.issued:
                Keys.issued.add(k)
                return k


def pick(r, weights):
    keys = list(weights)
    p = np.array([weights[k] for k in keys], float)
    return keys[int(r.choice(len(keys), p=p / p.sum()))]


def _rand_date(r, a, b):
    """a uniformly random date in [a, b]"""
    span = (b - a).days
    return a + dt.timedelta(days=int(r.integers(0, max(span, 0) + 1)))


AGE_BANDS = [(0, 4, 5.0), (5, 14, 10.5), (15, 24, 11.5), (25, 34, 12.0), (35, 44, 12.0), (45, 54, 14.0),
             (55, 64, 13.5), (65, 74, 11.0), (75, 84, 7.0), (85, 99, 3.5)]


def native_age(r):
    w = np.array([b[2] for b in AGE_BANDS])
    a, b, _ = AGE_BANDS[int(r.choice(len(AGE_BANDS), p=w / w.sum()))]
    return int(r.integers(a, b + 1))


def arrival_age(r):
    u = r.random()
    return int(r.integers(0, 18)) if u < 0.15 else int(r.integers(18, 30)) if u < 0.60 else \
        int(r.integers(30, 45)) if u < 0.88 else int(r.integers(45, 65))


def other_municipality(r, code):
    """a municipality somewhere else in the country (four-digit code outside the in-play list)"""
    while True:
        c = "%04d" % int(r.integers(1, 400))
        if c != code and c not in W.CODES and c not in ("0731", "0744"):
            return c


def code_at(code, when):
    """the municipality's code on a date: Ravenmeer's events before 2026 carry its former municipality's code"""
    if code == W.MERGED[1] and when < W.REF:
        return None
    return code


def person(r, keys, prof, code, origin, migrant=None):
    """One registered person on 1 January 2026 with a register history. `prof` is a composition from world.TYPES."""
    p = dict(key=keys(), mun=code, events=[], sex="M" if r.random() < 0.51 else "F", partial="")
    former = W.FORMER[int(r.integers(0, 2))][1] if code == W.MERGED[1] else None   # Ravenmeer's part

    def mun_on(d):
        return (former if former and d < W.REF else code)

    is_mig = (r.random() < prof["mig"]) if migrant is None else migrant
    if not is_mig:
        age = native_age(r)
        birth = years_before(W.REF, age, r.integers(1, 365))
        p.update(birth=birth, bcountry=W.HOME[0], nat=W.HOME[0], stay=None, left=0, first=None)
        born_here = r.random() < 0.55
        p["events"].append(("GEB", birth, mun_on(birth) if born_here else other_municipality(r, code), "", ""))
        if age >= 1 and r.random() < prof["nat_moved"]:
            since = _rand_date(r, max(birth + dt.timedelta(days=30), years_before(W.REF, 3)),
                               W.REF - dt.timedelta(days=2))
        elif age >= 5 and r.random() < 0.8:
            since = _rand_date(r, birth + dt.timedelta(days=200), years_before(W.REF, 4))
        else:
            since = birth
        if not born_here and since == birth:
            since = _rand_date(r, birth + dt.timedelta(days=200), W.REF - dt.timedelta(days=30)) \
                if (W.REF - birth).days > 260 else birth + dt.timedelta(days=int(r.integers(10, 40)))
        if since != birth:
            if born_here:
                p["events"].append(("ADR", since, mun_on(since), "", ""))
            else:
                p["events"].append(("VER", since, mun_on(since), "", other_municipality(r, code)))
        p["since"] = since
    else:
        band = int(r.choice(4, p=np.array(prof["stay"]) / sum(prof["stay"])))
        stay = 0 if band == 0 else int(r.integers(1, 5)) if band == 1 else int(r.integers(5, 10)) if band == 2 else \
            int(min(10 + r.geometric(0.09) - 1, 40))
        latest = years_before(W.REF, stay, r.integers(1, 365))
        left = int(r.random() < prof["left"][band])
        returning = left and r.random() < 0.25
        if returning:
            age_return = int(r.integers(22, 61))
            birth = years_before(latest, age_return, r.integers(0, 365))
            p.update(bcountry=W.HOME[0], nat=W.HOME[0])
            p["events"].append(("GEB", birth, other_municipality(r, code), "", ""))
            emi = _rand_date(r, years_before(latest, max(1, min(age_return - 18, 12))), latest - dt.timedelta(days=60))
            dest = pick(r, {c: 1 for c, _, g in W.COUNTRIES if g in ("EU", "EUR", "AME")})
            p["events"].append(("EMI", emi, other_municipality(r, code) if r.random() < 0.6 else mun_on(emi), dest, ""))
            p["events"].append(("IMM", latest, mun_on(latest), dest, ""))
            first = stay
        else:
            bc = pick(r, origin)
            gap = int(r.integers(prof["gap"][0], prof["gap"][1] + 1)) if left else 0
            first_date = years_before(latest, gap, r.integers(30, 330)) if left else latest
            birth = years_before(first_date, arrival_age(r), r.integers(0, 365))
            p.update(bcountry=bc, nat=bc)
            if left:
                p["events"].append(("IMM", first_date, other_municipality(r, code) if r.random() < 0.5
                                    else mun_on(first_date), bc, ""))
                emi = _rand_date(r, first_date + dt.timedelta(days=200), latest - dt.timedelta(days=45))
                p["events"].append(("EMI", emi, mun_on(emi) if r.random() < 0.5 else other_municipality(r, code),
                                    bc, ""))
            p["events"].append(("IMM", latest, mun_on(latest), bc, ""))
            first = completed_years(first_date)
            if stay >= 6 and r.random() < 0.45:
                when = _rand_date(r, years_before(latest, -5) if stay > 5 else latest, W.REF - dt.timedelta(days=20))
                when = min(when, W.REF - dt.timedelta(days=20))
                p["events"].append(("NAT", when, mun_on(when), "", ""))
                p["nat"] = W.HOME[0]
        p.update(birth=birth, stay=stay, left=left, first=first)
        if stay >= 1 and r.random() < prof["mig_moved"]:
            since = _rand_date(r, max(latest + dt.timedelta(days=30), years_before(W.REF, 3)), W.REF - dt.timedelta(days=2))
            if r.random() < 0.5:
                p["events"].append(("ADR", since, mun_on(since), "", ""))
            else:
                p["events"].append(("VER", since, mun_on(since), "", other_municipality(r, code)))
            # the arrival registered the person somewhere else first when the move was from another municipality
            if p["events"][-1][0] == "VER":
                ev = [e for e in p["events"] if e[0] == "IMM"][-1]
                i = p["events"].index(ev)
                p["events"][i] = ("IMM", ev[1], p["events"][-1][4], ev[3], "")
        else:
            since = latest
        p["since"] = since
        if p["bcountry"] != W.HOME[0] and r.random() < 0.08:
            p["partial"] = "Y" if r.random() < 0.6 else "M"     # birth day and month unknown, or the day only
    age = completed_years(p["birth"])
    if age >= 22 and r.random() < 0.52:
        when = _rand_date(r, years_before(p["birth"], -21), W.REF - dt.timedelta(days=10))
        p["events"].append(("HUW", when, mun_on(when) if when >= p["since"] else other_municipality(r, code), "", ""))
        p["marital"] = "H"
    else:
        p["marital"] = "O"
    p["events"].sort(key=lambda e: e[1])
    p["absent"] = bool(r.random() < W.p_absent(p["stay"], p["left"]))
    return p


def municipality(seed, code, n=None):
    """the persons registered in an in-play municipality on 1 January 2026 (the first n of a fixed draw)"""
    typ = W.TYPE[code]
    r = rng(seed, 20, int(code))
    keys = Keys(seed * 1000 + int(code))
    n = n or W.COUNT[code]
    return [person(r, keys, W.TYPES[typ], code, W.ORIGIN_WEIGHTS[typ]) for _ in range(n)]


def audit_national(seed, n):
    """the audit's sampled persons registered outside the in-play municipalities"""
    r = rng(seed, 30)
    keys = Keys(seed * 1000 + 999)
    out = []
    for _ in range(n):
        code = other_municipality(r, "")
        out.append(person(r, keys, W.NATIONAL, code, W.ORIGIN_WEIGHTS["N"]))
    return out


def outcome(r, p):
    """the audit's final result for a sampled person: 10 at the address, 11 elsewhere in the municipality, 50 there on
    1 January and left later (present); 20 elsewhere in the country, 30 abroad, 40 died before 1 January (absent)"""
    if p["absent"]:
        if r.random() < W.ELSEWHERE_SHARE:
            return "20"
        old = completed_years(p["birth"]) >= 70
        return "40" if r.random() < (0.55 if old else 0.03) else "30"
    if r.random() < (0.016 if p["stay"] is not None and p["stay"] <= 4 else 0.002):
        return "50"
    return "11" if r.random() < 0.03 else "10"


POOL = 6600     # each in-play municipality's fixed draw; its register is the first COUNT persons of it


def pools(seed):
    """each in-play municipality's fixed draw, with each position's audit membership fixed once"""
    f = W.N_AUDIT / W.NATIONAL_REGISTER
    Keys.issued.clear()
    out = {}
    for code in W.CODES:
        people = municipality(seed, code, POOL)
        r = rng(seed, 50, int(code))
        for p in people:
            p["in_audit"] = bool(r.random() < f)
        out[code] = people
    return out


def register(seed, counts=None, pool=None):
    """the in-play register on 1 January 2026 and the national audit sample"""
    counts = counts or W.COUNT
    pool = pool or pools(seed)
    Keys.issued.update(p["key"] for people in pool.values() for p in people)
    reg = {code: pool[code][:counts[code]] for code in W.CODES}
    inplay_sampled = [p for code in W.CODES for p in reg[code] if p["in_audit"]]
    national = audit_national(seed, W.N_AUDIT - len(inplay_sampled))
    sample = national + inplay_sampled
    order = rng(seed, 60).permutation(len(sample))
    sample = [sample[i] for i in order]
    r = rng(seed, 61)
    for i, p in enumerate(sample):
        p["audit_no"] = "RCA26-%05d" % (i + 1)
        p["result"] = outcome(r, p)
    return reg, sample


def fieldwork(seed, sample):
    """visits per sampled person: earlier attempts with no contact (91), then the final result"""
    r = rng(seed, 40)
    rows = []
    for i, p in enumerate(sample):
        res = p["result"]
        tries = 1 if r.random() < 0.70 else 2 if r.random() < 0.75 else 3
        days = sorted(_rand_date(r, W.FIELD_START, W.FIELD_END) for _ in range(tries))
        for j, d in enumerate(days):
            last = j == tries - 1
            mode = ("R" if res in ("30", "40", "20") and r.random() < 0.55 else "V" if r.random() < 0.85 else "T") \
                if last else "V"
            rows.append(dict(audit=p["audit_no"], visit=j + 1, date=d, mode=mode, result=res if last else "91"))
    return rows


# The 2025 deregistration traffic of each in-play municipality. Messages are those its register sent to the national
# hub in calendar 2025; the hub accepts or rejects each one. Departures abroad, deaths and removals concern people no
# longer registered on 1 January 2026, except the residents who left and came back within the year.
EXTRA = {"G": dict(remove=0.0060, former=0.055), "U": dict(remove=0.0040, former=0.070),
         "O": dict(remove=0.0015, former=0.080), "S": dict(remove=0.0012, former=0.050),
         "T": dict(remove=0.0015, former=0.060)}
DEATH_RATE = {"G": 0.0071, "U": 0.0058, "O": 0.0097, "S": 0.0104, "T": 0.0093}   # by age structure
REASONS = {"E03": "destination country missing or not on the country table",
           "E07": "date before the person's settlement at the address",
           "E12": "date later than the date the message was sent",
           "E21": "person not registered in the sending municipality"}
YEAR0, YEAR1 = dt.date(2025, 1, 1), dt.date(2025, 12, 31)


def _departed_person(r, keys, code, typ, when):
    """someone who lived in the municipality and left the register: birth, sex, origin and nationality"""
    mig = r.random() < (0.85 if typ in ("G", "U") else 0.45)
    bc = pick(r, W.ORIGIN_WEIGHTS[typ]) if mig else W.HOME[0]
    age = (int(r.integers(19, 46)) if typ in ("G", "U") else int(r.integers(18, 70))) if mig else int(r.integers(18, 80))
    return dict(key=keys(), birth=years_before(when, age, r.integers(1, 365)), sex="M" if r.random() < 0.55 else "F",
                bcountry=bc, nat=bc, origin=bc)


def traffic(seed, reg):
    """messages (one per message sent), acknowledgements and the non-resident records, by in-play municipality"""
    msgs, nonres = [], []
    for code in W.CODES:
        typ = W.TYPE[code]
        r = rng(seed, 70, int(code))
        keys = Keys(seed * 10000 + 5000 + int(code))
        n = len(reg[code])
        part = {}
        ours = (code,) + ((W.FORMER[0][1], W.FORMER[1][1]) if code == W.MERGED[1] else ())

        def former_of(p):
            if code != W.MERGED[1]:
                return code
            if p["key"] not in part:
                part[p["key"]] = W.FORMER[int(r.integers(0, 2))][1]
            return part[p["key"]]

        def send(kind, p, when, country, sent=None, extra=None, sender=None):
            """a message the register sends in the night after it registers the event (`sent` is that registration
            date); one registered after 31 December is in the hub's 2026 log, not this one"""
            sent = sent or when + dt.timedelta(days=int(r.integers(0, 12)))
            if sent > YEAR1:
                return None
            msgs.append(dict(mun=code, sender=sender or former_of(p), key=p["key"], kind=kind, date=when,
                             country=country, sent=sent, **(extra or {})))
            return msgs[-1]

        def part_of(q):
            """the code a registered person's 2025 events carry (Ravenmeer's residents: their former municipality)"""
            for e in reversed(q["events"]):
                if e[2] in ours:
                    return e[2] if code == W.MERGED[1] and e[1] < W.REF else code
            return former_of(q)

        # departures abroad: leavers, of whom some left twice; plus residents who left and came back within 2025
        n_dep = int(r.poisson(W.TYPES[typ]["dep"] * n))
        n_twice = max(3, int(round(W.TYPES[typ]["repeat"] * n_dep)))
        n_dead = 1 if typ in ("T", "S", "O") else int(r.integers(2, 4))
        leavers = []
        for i in range(n_dep):
            when = _rand_date(r, YEAR0, YEAR1 - dt.timedelta(days=8))
            p = _departed_person(r, keys, code, typ, when)
            twice = i < n_twice
            if twice:
                first = _rand_date(r, YEAR0, dt.date(2025, 5, 31))
                when = _rand_date(r, dt.date(2025, 8, 1), YEAR1 - dt.timedelta(days=8))
                send("EMI", p, first, p["origin"] if p["origin"] != W.HOME[0] else "5012")
            dest = p["origin"] if p["origin"] != W.HOME[0] else pick(r, {"5012": 2, "5010": 2, "6001": 1, "5013": 1})
            m = send("EMI", p, when, dest)
            p["dest"] = dest
            leavers.append((p, when, m["sent"] if m else YEAR1 + dt.timedelta(days=int(r.integers(1, 12)))))
        if not any(e[0] == "EMI" and YEAR0 <= e[1] <= YEAR1 and e[2] in ours for q in reg[code] for e in q["events"]):
            # a resident who left in 2025 and came back: the golden reads only whether a resident left before the
            # latest settlement, never when or from where, so the earlier departure can be dated into 2025
            cand = [q for q in reg[code] if q["stay"] == 0 and q["left"] and
                    [e for e in q["events"] if e[0] == "IMM"][-1][1] >= dt.date(2025, 2, 20)]
            if cand:
                q = cand[0]
                latest = [e for e in q["events"] if e[0] == "IMM"][-1]
                i = [k for k, e in enumerate(q["events"]) if e[0] == "EMI"][-1]
                e = q["events"][i]
                here = latest[2] if latest[2] in ours else former_of(q)
                q["events"][i] = ("EMI", _rand_date(r, YEAR0, latest[1] - dt.timedelta(days=45)), here, e[3], e[4])
                q["events"].sort(key=lambda e: e[1])
            else:
                # a stay that began in 2025 after an earlier one in the municipality that ended abroad in 2025
                cand = [q for q in reg[code] if q["stay"] == 0 and not q["left"] and not q.get("in_audit")
                        and [e for e in q["events"] if e[0] == "IMM"][-1][1] >= dt.date(2025, 4, 1)
                        and not any(e[0] in ("VER", "ADR") for e in q["events"])]
                q = cand[int(r.integers(0, len(cand)))]
                latest = [e for e in q["events"] if e[0] == "IMM"][-1]
                here = latest[2]
                first = years_before(latest[1], int(r.integers(1, 4)), r.integers(30, 300))
                left_on = _rand_date(r, dt.date(2025, 1, 10), latest[1] - dt.timedelta(days=45))
                q["events"] += [("IMM", first, here, latest[3], ""), ("EMI", left_on, here, latest[3], "")]
                q["events"].sort(key=lambda e: e[1])
                q["left"], q["first"] = 1, completed_years(first)
        quiet = [q for q in reg[code] if max(e[1] for e in q["events"]) <= dt.date(2025, 9, 30)
                 and not any(e[0] in ("IMM", "EMI") and e[1] >= dt.date(2024, 7, 1) for e in q["events"])]
        for i in r.choice(len(quiet), size=1 + int(r.random() < 0.4), replace=False):
            q = quiet[int(i)]
            last = max(e[1] for e in q["events"])
            d = _rand_date(r, max(last + dt.timedelta(days=30), dt.date(2025, 1, 20)), dt.date(2025, 10, 31))
            here = part_of(q)
            dest = q["bcountry"] if q["bcountry"] != W.HOME[0] else pick(r, {"5012": 2, "5010": 2, "6001": 1})
            q.setdefault("annulled", []).append(("EMI", d, here, dest, ""))
            q.setdefault("ann_dates", {})[("EMI", d)] = d + dt.timedelta(days=int(r.integers(18, 61)))
            send("EMI", q, d, dest, sent=d + dt.timedelta(days=int(r.integers(0, 5))), extra=dict(void=True),
                 sender=here)
        for p in reg[code]:
            for e in p["events"]:
                if e[0] == "EMI" and YEAR0 <= e[1] <= YEAR1 and e[2] in ours:
                    send("EMI", p, e[1], e[3], sent=min(e[1] + dt.timedelta(days=int(r.integers(0, 6))),
                                                      YEAR1), extra=dict(back=True), sender=e[2])
        back = sum(1 for m in msgs if m["mun"] == code and m.get("back"))
        late_dec = sum(1 for m in msgs if m["mun"] == code and m["kind"] == "EMI" and m["sent"] == YEAR1)
        extra = int(r.choice([k for k in (1, 2, 3) if late_dec + k not in (back, n_twice)]))
        for _ in range(extra):   # contracts that end with the year: registered on 31 December
            when = _rand_date(r, dt.date(2025, 12, 15), dt.date(2025, 12, 30))
            p = _departed_person(r, keys, code, typ, when)
            dest = p["origin"] if p["origin"] != W.HOME[0] else pick(r, {"5012": 2, "5010": 2, "6001": 1})
            send("EMI", p, when, dest, sent=YEAR1)
            p["dest"] = dest
            leavers.append((p, when, YEAR1))
        # deaths of residents, and removals after an address investigation
        dead = []

        def resident_death(when, sent=None):
            p = dict(key=keys(), birth=years_before(when, int(r.integers(55, 99)), r.integers(1, 365)),
                     sex="M" if r.random() < 0.49 else "F", bcountry=W.HOME[0], nat=W.HOME[0])
            m = send("OVL", p, when, W.HOME[0] if r.random() < 0.97 else "5012", sent=sent)
            dead.append(p)
            return m

        ovl = [resident_death(_rand_date(r, YEAR0, YEAR1 - dt.timedelta(days=6)))
               for _ in range(int(r.poisson(DEATH_RATE[typ] * n)))]
        # deaths recorded for the wrong person (a namesake at the same address, a hospital's notice matched to the
        # wrong record) and annulled within weeks: the message was sent and accepted, the person is still registered
        older = [q for q in reg[code] if completed_years(q["birth"]) >= 45
                 and max(e[1] for e in q["events"]) <= dt.date(2025, 9, 30) and not q.get("annulled")]
        for i in r.choice(len(older), size=1 + int(r.random() < 0.3), replace=False):
            q = older[int(i)]
            last = max(e[1] for e in q["events"])
            d = _rand_date(r, max(last + dt.timedelta(days=30), dt.date(2025, 1, 20)), dt.date(2025, 10, 31))
            here = part_of(q)
            q.setdefault("annulled", []).append(("OVL", d, here, "", ""))
            q.setdefault("ann_dates", {})[("OVL", d)] = d + dt.timedelta(days=int(r.integers(6, 41)))
            send("OVL", q, d, W.HOME[0], sent=d + dt.timedelta(days=int(r.integers(0, 4))), extra=dict(void=True),
                 sender=here)
        for _ in range(1 + int(r.random() < 0.35)):   # the holiday deaths, registered on 31 December
            resident_death(_rand_date(r, dt.date(2025, 12, 22), dt.date(2025, 12, 30)), sent=YEAR1)
        for _ in range(int(r.integers(1, 3))):
            # December 2024 deaths registered in January
            when = _rand_date(r, dt.date(2024, 12, 20), dt.date(2024, 12, 31))
            resident_death(when, sent=_rand_date(r, dt.date(2025, 1, 2), when + dt.timedelta(days=12)))
        removed = []
        for _ in range(max(2, int(round(EXTRA[typ]["remove"] * n)))):
            when = _rand_date(r, YEAR0, YEAR1 - dt.timedelta(days=20))
            p = _departed_person(r, keys, code, typ, when)
            send("VOW", p, when, "0000")
            removed.append((p, when))
        # former residents abroad: departed before 2025; some died abroad in 2025 and the municipality recorded it
        n_former = int(round(EXTRA[typ]["former"] * n))
        for i in range(n_former):
            dep = _rand_date(r, dt.date(1990, 1, 1), dt.date(2024, 12, 31))
            p = _departed_person(r, keys, code, typ, dep)
            p["birth"] = years_before(dep, int(r.integers(19, 66)), r.integers(1, 365))
            status, sdate = "A", dep
            age_now = completed_years(p["birth"])
            if i < max(2, int(round(0.012 * n_former))) or (age_now >= 70 and r.random() < 0.05):
                status, sdate = "O", _rand_date(r, YEAR0, YEAR1 - dt.timedelta(days=10))
                send("OVL", p, sdate, p["origin"] if p["origin"] != W.HOME[0] else "5012")
            elif age_now >= 60 and r.random() < 0.10:
                status, sdate = "O", _rand_date(r, max(dep, dt.date(1995, 1, 1)), dt.date(2024, 12, 20))
            last = former_of(p)
            nonres.append(dict(key=p["key"], last=last, dep=dep, country=p["origin"] if p["origin"] != W.HOME[0]
                               else "5012", status=status, sdate=sdate, birth=p["birth"], sex=p["sex"], mun=code))
        # late reports: departures and deaths dated December 2024 that the register sent in January 2025
        for _ in range(int(r.choice([k for k in (1, 2, 3) if k != back]))):
            when = _rand_date(r, dt.date(2024, 12, 2), dt.date(2024, 12, 31))
            p = _departed_person(r, keys, code, typ, when)
            dest = p["origin"] if p["origin"] != W.HOME[0] else "5012"
            send("EMI", p, when, dest, sent=_rand_date(r, dt.date(2025, 1, 2), dt.date(2025, 1, 24)))
            nonres.append(dict(key=p["key"], last=former_of(p), dep=when, country=dest, status="A",
                               sdate=when, birth=p["birth"], sex=p["sex"], mun=code))
        # the 2025 leavers and the removed become non-resident records (removals to an unknown country)
        for p, when, registered in leavers:
            if registered > W.EXTRACT_DATE - dt.timedelta(days=1):
                continue
            nonres.append(dict(key=p["key"], last=former_of(p), dep=when, country=p["dest"], status="A", sdate=when,
                               birth=p["birth"], sex=p["sex"], mun=code))
        for p, when in removed:
            last = former_of(p)
            nonres.append(dict(key=p["key"], last=last, dep=when, country="0000", status="A", sdate=when,
                               birth=p["birth"], sex=p["sex"], mun=code))
        # departure messages for people the register had already removed or recorded as dead: rejected, never resent
        gone = [p for p, _ in removed] + dead
        for k in range(n_dead):
            prior = [m for m in msgs if m["key"] in {q["key"] for q in gone} and m["sent"] <= dt.date(2025, 11, 30)]
            if not prior:
                continue
            prior = prior[int(r.integers(0, len(prior)))]
            when = prior["date"] + dt.timedelta(days=int(r.integers(5, 30)))
            send("EMI", dict(key=prior["key"]), when, "5017" if typ == "G" else "5012",
                 sent=when + dt.timedelta(days=int(r.integers(0, 6))), extra=dict(dead_end=True),
                 sender=prior["sender"])
    return msgs, nonres


def acknowledge(seed, msgs, nonres=()):
    """the hub's answer to every message; a rejected message is usually corrected and sent again within two weeks"""
    r = rng(seed, 80)
    out, acks = [], []
    by_mun = {}
    for m in msgs:
        by_mun.setdefault(m["mun"], []).append(m)
    for code in W.CODES:
        ms = sorted(by_mun.get(code, []), key=lambda m: (m["sent"], m["key"], m["kind"]))
        former = {x["key"] for x in nonres if x["mun"] == code}
        must = {}
        for kind in ("EMI", "OVL"):
            pool = [m for m in ms if m["kind"] == kind and not m.get("back") and not m.get("dead_end")
                    and not m.get("void")
                    and m["key"] not in (former if kind == "OVL" else ()) and m["date"].year == 2025
                    and m["sent"] <= dt.date(2025, 12, 12)]
            must[kind] = id(pool[int(r.integers(0, len(pool)))])
        for m in ms:
            if m.get("dead_end"):
                out.append(m)
                acks.append((m, "REJECTED", "E21"))
                continue
            p_rej = {"EMI": 0.06, "OVL": 0.03, "VOW": 0.04}[m["kind"]]
            eligible = not (m.get("back") or m.get("void")) and m["sent"] <= dt.date(2025, 12, 12) \
                and m["date"].year == 2025
            rej = id(m) in must.values() or (eligible and r.random() < p_rej)
            if rej:
                reason = "E03" if m["kind"] == "EMI" and r.random() < 0.5 else ("E12" if r.random() < 0.5 else "E07")
                bad = dict(m)
                if reason == "E12":   # a date after sending, still within the year
                    bad["date"] = m["sent"] + dt.timedelta(days=int(r.integers(1, max(2, min(30, (YEAR1 - m["sent"]).days)))))
                elif reason == "E03":
                    bad["country"] = ""
                out.append(bad)
                acks.append((bad, "REJECTED", reason))
                again = dict(m, sent=m["sent"] + dt.timedelta(days=int(r.integers(1, 15))))
                out.append(again)
                acks.append((again, "ACCEPTED", ""))
            else:
                out.append(m)
                acks.append((m, "ACCEPTED", ""))
    return out, acks
