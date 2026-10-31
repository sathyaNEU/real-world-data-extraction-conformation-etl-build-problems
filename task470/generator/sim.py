"""The world behind the pack: every dwelling the cadastre holds in the county, who lived where in the reference
fortnight, the population register's people and its events, the land register's titles and transfers, the business
and shareholder registers, the meter data hub's metering points and their hourly electricity use.

Everything is drawn from one seeded generator in a fixed order, so two runs give the same world byte for byte."""
import datetime as dt
import numpy as np

import world as W

STREETS = ["Storgata", "Kirkeveien", "Skolegata", "Fjordveien", "Bakkeveien", "Strandgata", "Elvegata", "Granveien",
           "Bjørkeveien", "Furuveien", "Lyngveien", "Sjøgata", "Nordre gate", "Søndre gate", "Myrveien", "Haugveien",
           "Bekkeveien", "Steinsvingen", "Lia", "Bråtaveien", "Torget", "Havnegata", "Industriveien", "Kvernveien",
           "Fjellveien", "Engveien", "Solbakken", "Åsveien", "Tunveien", "Gårdsveien", "Dalveien", "Viksvingen"]
CABIN_ROADS = ["Hyttefeltvegen", "Fjellstølen", "Vardevegen", "Seterlia", "Tjernvegen", "Utsikten"]
INSTITUTIONS = ["omsorgssenter", "sykehjem"]


def day(d):
    return (d - W.FORTNIGHT_START).days


class World:
    pass


def build():
    rng = np.random.default_rng(W.SEED)
    w = World()
    w.rng = rng
    _temperature(w)
    _dwellings(w)
    _occupancy(w)
    _people(w)
    _events(w)
    _ownership(w)
    _meters(w)
    _loads(w)
    _outages(w)
    _prices(w)
    return w


# ---------------------------------------------------------------------------------------------- temperature
def _temperature(w):
    rng = w.rng
    hod = np.arange(W.HOURS) % 24
    w.temp = {}
    base = {"town": 0.5, "coast": 2.6, "suburb": 0.2, "industry": 0.0, "inland": -3.4, "mixed": -0.6}
    spell = np.concatenate([np.zeros(3), np.linspace(0, -5.5, 3), np.full(4, -6.0), np.linspace(-5, -1, 4)])
    for nr, name, kind, *_ in W.MUNICIPALITIES:
        d = base[kind] + spell * (0.6 if kind == "coast" else 1.0) + rng.normal(0, 0.9, W.DAYS).cumsum() * 0.35
        diurnal = 0.8 * np.cos((hod - 14) / 24 * 2 * np.pi)
        t = np.repeat(d, 24) + diurnal + rng.normal(0, 0.35, W.HOURS)
        w.temp[nr] = np.round(t, 1)


# ---------------------------------------------------------------------------------------------- the cadastre
def _dwellings(w):
    """Counted dwellings (in use before 1 November 2026), plus the units the regulation leaves out: holiday homes,
    dwellings taken into use after the register day, and non-dwelling units (care homes, shops)."""
    rng = w.rng
    w.units = []
    w.props = {}
    uid = 300000000
    for mi, (nr, name, kind, N, V, *_rest) in enumerate(W.MUNICIPALITIES):
        flats_share = W.MUNICIPALITIES[mi][9]
        gnr = 1
        made = 0
        streets = list(rng.permutation(STREETS)[:14])
        house_no = {s: 1 for s in streets}

        def addr():
            s = streets[int(rng.integers(0, len(streets)))]
            n = house_no[s]
            house_no[s] += int(rng.integers(1, 4))
            return s, n
        while made < N:
            r = rng.random()
            if r < flats_share and N - made >= 6:
                # a block of flats: one property, sections when it is a condominium
                floors = int(rng.integers(2, 6))
                per = int(rng.integers(2, 5))
                k = min(floors * per, N - made)
                s, n = addr()
                bnr = int(rng.integers(1, 400))
                owner_kind = rng.choice(["condo", "coop", "rental"], p=[0.45, 0.35, 0.20])
                heating = "central" if rng.random() < 0.72 else ("electric" if rng.random() < 0.6 else "heatpump")
                b_id = "B%s%05d" % (nr, len(w.props))
                prop = {"nr": nr, "gnr": gnr, "bnr": bnr, "kind": owner_kind, "units": [], "street": s, "no": n,
                        "building": b_id}
                w.props[(nr, gnr, bnr)] = prop
                idx = 0
                for f in range(1, floors + 1):
                    for d in range(1, per + 1):
                        if idx >= k:
                            break
                        uid += int(rng.integers(1, 9))
                        u = {"id": uid, "nr": nr, "gnr": gnr, "bnr": bnr,
                             "snr": idx + 1 if owner_kind == "condo" else 0, "street": s, "no": n, "letter": "",
                             "unit": "H%02d%02d" % (f, d), "type": "Leilighet", "category": "Bolig",
                             "heating": heating, "area": int(rng.integers(38, 110)), "in_use": _in_use(rng),
                             "building": b_id, "counted": True}
                        prop["units"].append(u)
                        w.units.append(u)
                        idx += 1
                made += k
                gnr += 1
            else:
                s, n = addr()
                two = rng.random() < 0.10 and N - made >= 2
                bnr = int(rng.integers(1, 400))
                b_id = "B%s%05d" % (nr, len(w.props))
                kindh = rng.choice(["Enebolig", "Rekkehus", "Tomannsbolig"], p=[0.7, 0.2, 0.1])
                heating = "electric" if rng.random() < 0.55 else ("heatpump" if rng.random() < 0.85 else "central")
                prop = {"nr": nr, "gnr": gnr, "bnr": bnr, "kind": "house", "units": [], "street": s, "no": n,
                        "building": b_id}
                w.props[(nr, gnr, bnr)] = prop
                for j in range(2 if two else 1):
                    uid += int(rng.integers(1, 9))
                    u = {"id": uid, "nr": nr, "gnr": gnr, "bnr": bnr, "snr": 0, "street": s, "no": n,
                         "letter": "", "unit": "H0101" if j == 0 else "U0101", "type": kindh, "category": "Bolig",
                         "heating": heating, "area": int(rng.integers(70, 220)) if j == 0 else int(rng.integers(35, 70)),
                         "in_use": _in_use(rng), "building": b_id, "counted": True}
                    prop["units"].append(u)
                    w.units.append(u)
                made += 2 if two else 1
                gnr += 1
        # left out by the regulation: holiday homes, taken into use after 1 November, non-dwelling units
        n_cabin = int(N * {"coast": 0.22, "inland": 0.30, "mixed": 0.14}.get(kind, 0.05))
        for i in range(n_cabin):
            uid += int(rng.integers(1, 9))
            road = CABIN_ROADS[int(rng.integers(0, len(CABIN_ROADS)))]
            u = {"id": uid, "nr": nr, "gnr": 200 + i // 3, "bnr": int(rng.integers(1, 300)), "snr": 0, "street": road,
                 "no": int(rng.integers(1, 90)), "letter": "", "unit": "H0101", "type": "Fritidsbolig",
                 "category": "Fritidsbolig", "heating": "electric", "area": int(rng.integers(40, 120)),
                 "in_use": dt.date(int(rng.integers(1975, 2024)), int(rng.integers(1, 13)), 1),
                 "building": "C%s%05d" % (nr, i), "counted": False}
            w.units.append(u)
        for i in range(max(3, int(N * 0.015))):
            uid += int(rng.integers(1, 9))
            s = streets[int(rng.integers(0, len(streets)))]
            late = rng.random() < 0.6
            u = {"id": uid, "nr": nr, "gnr": 300 + i, "bnr": int(rng.integers(1, 300)), "snr": 0, "street": s,
                 "no": int(rng.integers(100, 160)), "letter": "", "unit": "H0101", "type": "Enebolig",
                 "category": "Bolig", "heating": "heatpump", "area": int(rng.integers(80, 180)),
                 "in_use": (dt.date(2026, 11, 1) + dt.timedelta(days=int(rng.integers(3, 60)))) if late else None,
                 "building": "N%s%05d" % (nr, i), "counted": False}
            w.units.append(u)
        inst = INSTITUTIONS[mi % 2]
        uid += int(rng.integers(1, 9))
        w.units.append({"id": uid, "nr": nr, "gnr": 400, "bnr": 1, "snr": 0, "street": "%s %s" % (name, inst),
                        "no": 1, "letter": "", "unit": "H0101", "type": "Institusjon", "category": "Annet",
                        "heating": "central", "area": 2400, "in_use": dt.date(1988, 6, 1), "building": "I%s" % nr,
                        "counted": False})
    w.by_id = {u["id"]: u for u in w.units}


def _in_use(rng):
    y = int(rng.choice(np.arange(1950, 2026), p=None))
    return dt.date(y, int(rng.integers(1, 13)), int(rng.integers(1, 28)))


# ---------------------------------------------------------------------------------------------- who lived where
def _occupancy(w):
    """Each counted dwelling is lived in or vacant in the fortnight; the vacant split by how their electricity runs:
    heated (direct electric at a lowered thermostat), heat pump at a low setting, near-empty (fridge and standby)
    and switched off at the main fuse. The counts per municipality are the table in world.py, exactly."""
    rng = w.rng
    for mi, (nr, name, kind, N, V, heated, hp, tiny, off, *_r) in enumerate(W.MUNICIPALITIES):
        dws = [u for u in w.units if u["nr"] == nr and u["counted"]]
        assert len(dws) == N, (nr, len(dws), N)
        n_hp = int(round(V * hp))
        n_tiny = int(round(V * tiny))
        n_off = int(round(V * off))
        n_heat = V - n_hp - n_tiny - n_off
        order = list(rng.permutation(len(dws)))
        houses = [dws[i] for i in order if dws[i]["type"] != "Leilighet" and dws[i]["heating"] == "electric"]
        hpd = [dws[i] for i in order if dws[i]["heating"] == "heatpump"]
        cent = [dws[i] for i in order if dws[i]["heating"] == "central"]
        rest = [dws[i] for i in order]
        chosen = set()

        def take(pool, n, label):
            got = 0
            for u in pool:
                if got >= n:
                    break
                if u["id"] in chosen:
                    continue
                u["vacant"] = label
                chosen.add(u["id"])
                got += 1
            for u in rest:
                if got >= n:
                    break
                if u["id"] in chosen:
                    continue
                if label == "heated" and u["heating"] == "central":
                    continue
                u["vacant"] = label
                chosen.add(u["id"])
                got += 1
            assert got == n, (nr, label, got, n)
        take(houses, n_heat, "heated")
        take(hpd, n_hp, "heatpump")
        take(cent, n_tiny, "tiny")
        take(rest, n_off, "off")
        for u in dws:
            u.setdefault("vacant", None)
        assert sum(1 for u in dws if u["vacant"]) == V


# ---------------------------------------------------------------------------------------------- the population register
def _people(w):
    """Households in the lived-in dwellings; registration on 1 November: most households registered where they live,
    some (students, contract workers, new tenants) registered elsewhere or abroad; some vacant dwellings still carry a
    registered resident (moved to care, emigrated without notice)."""
    rng = w.rng
    w.persons = []
    pid = 7100000
    for mi, (nr, name, kind, N, V, heated, hp, tiny, off, flats, unreg, regvac) in enumerate(W.MUNICIPALITIES):
        for u in [x for x in w.units if x["nr"] == nr and x["counted"]]:
            if u["vacant"]:
                u["household"] = 0
                n_reg = 0
                if rng.random() < regvac:
                    n_reg = 1 if rng.random() < 0.7 else 2
                    ages = rng.integers(68, 96, n_reg) if rng.random() < 0.75 else rng.integers(25, 70, n_reg)
                    for a in ages:
                        pid += int(rng.integers(1, 7))
                        w.persons.append(_person(rng, pid, u, int(a)))
                u["registered_nov1"] = n_reg
                continue
            size = int(rng.choice([1, 2, 3, 4, 5], p=[0.36, 0.32, 0.13, 0.13, 0.06]))
            if u["type"] == "Leilighet" and size > 3:
                size = 2
            u["household"] = size
            registered = rng.random() > unreg
            if not registered:
                u["registered_nov1"] = 0
                continue
            u["registered_nov1"] = size
            adults = max(1, size - int(rng.integers(0, max(1, size - 1))) if size > 2 else size)
            for k in range(size):
                if k < adults:
                    a = int(rng.integers(19, 95)) if size == 1 else int(rng.integers(24, 80))
                else:
                    a = int(rng.integers(0, 18))
                pid += int(rng.integers(1, 7))
                w.persons.append(_person(rng, pid, u, a))
    w.person_by_id = {p["id"]: p for p in w.persons}


def _person(rng, pid, u, age):
    ref = W.REGISTER_DAY
    born = ref - dt.timedelta(days=int(age * 365.25 + rng.integers(0, 365)))
    return {"id": pid, "born": born, "unit": u["id"], "nov1_unit": u["id"], "since": _since(rng, born, ref)}


def _since(rng, born, ref):
    lo = max(born, dt.date(1990, 1, 1))
    span = (ref - lo).days
    return lo + dt.timedelta(days=int(rng.integers(0, max(1, span))))


def _events(w):
    """Register events from 1 October 2026 to the snapshot on 5 January 2027. Before 1 November: ordinary moves,
    already in the 1 November state. After it: moves (inside a municipality, between them, to a care home or out of
    the county), deaths, emigrations, births and arrivals; and the cadastre's unit renumbering of some blocks, which
    the register records as each resident's move to the new unit number on the day the cadastre changed it."""
    rng = w.rng
    w.events = []
    counted = [u for u in w.units if u["counted"]]
    lived = [u for u in counted if not u["vacant"]]
    inst = {u["nr"]: u for u in w.units if u["category"] == "Annet"}

    def dt_after(lo, hi):
        return lo + dt.timedelta(days=int(rng.integers(0, (hi - lo).days)))
    # care home residents, registered at the home long before the register day
    pid = max(p["id"] for p in w.persons)
    for nr, *_r in W.MUNICIPALITIES:
        for i in range(int(rng.integers(14, 36))):
            pid += int(rng.integers(1, 7))
            p = _person(rng, pid, inst[nr], int(rng.integers(74, 99)))
            w.persons.append(p)
    w.person_by_id = {p["id"]: p for p in w.persons}
    # moves before the register day (history, already reflected and registered by 1 November)
    for p in [q for q in w.persons if not w.by_id[q["unit"]].get("vacant") and w.by_id[q["unit"]]["counted"]][::23]:
        src = lived[int(rng.integers(0, len(lived)))]
        d = dt_after(W.EVENTS_FROM, dt.date(2026, 10, 28))
        w.events.append({"pid": p["id"], "type": "Flytting", "date": d, "reg": d + dt.timedelta(days=int(rng.integers(0, 4))),
                         "from": src["id"], "to": p["unit"], "from_out": None, "to_out": None})
        p["since"] = max(p["since"], d)
    after_lo = W.REGISTER_DAY + dt.timedelta(days=1)
    hi = W.SNAPSHOT_DAY - dt.timedelta(days=2)
    persons = sorted(w.persons, key=lambda p: p["id"])
    order = rng.permutation(len(persons))
    k = 0

    def next_person():
        nonlocal k
        p = persons[order[k % len(persons)]]
        k += 1
        return p
    used = set()
    n = len(persons)
    plan = [("move_in", int(n * 0.011)), ("move_between", int(n * 0.007)), ("move_care", int(n * 0.0035)),
            ("move_out", int(n * 0.004)), ("death", int(n * 0.0022)), ("emigration", int(n * 0.0015))]
    for kind, count in plan:
        done = 0
        while done < count:
            p = next_person()
            if p["id"] in used or p["unit"] is None:
                continue
            if w.by_id[p["unit"]]["category"] == "Annet" and kind != "death":
                continue
            used.add(p["id"])
            src = w.by_id[p["unit"]]
            # a lone resident of a lived-in dwelling leaves after the fortnight has begun, so the dwelling was lived in
            alone = src["counted"] and not src.get("vacant") and src.get("household", 0) <= 1
            d = dt_after(W.FORTNIGHT_START if alone else after_lo, hi)
            reg = d + dt.timedelta(days=int(rng.integers(0, 8)))
            if kind == "move_in":
                same = [u for u in lived if u["nr"] == src["nr"] and u["id"] != src["id"]]
                dst = same[int(rng.integers(0, len(same)))]
                w.events.append({"pid": p["id"], "type": "Flytting", "date": d, "reg": reg, "from": src["id"],
                                 "to": dst["id"], "from_out": None, "to_out": None})
                p["unit"] = dst["id"]
            elif kind == "move_between":
                other = [u for u in lived if u["nr"] != src["nr"]]
                dst = other[int(rng.integers(0, len(other)))]
                w.events.append({"pid": p["id"], "type": "Flytting", "date": d, "reg": reg, "from": src["id"],
                                 "to": dst["id"], "from_out": None, "to_out": None})
                p["unit"] = dst["id"]
            elif kind == "move_care":
                dst = inst[src["nr"]]
                w.events.append({"pid": p["id"], "type": "Flytting", "date": d, "reg": reg, "from": src["id"],
                                 "to": dst["id"], "from_out": None, "to_out": None})
                p["unit"] = dst["id"]
            elif kind == "move_out":
                w.events.append({"pid": p["id"], "type": "Flytting", "date": d, "reg": reg, "from": src["id"],
                                 "to": None, "from_out": None, "to_out": "OUT"})
                p["unit"] = None
            elif kind == "death":
                w.events.append({"pid": p["id"], "type": "Dødsfall", "date": d, "reg": reg, "from": src["id"],
                                 "to": None, "from_out": None, "to_out": None})
                p["unit"] = None
            else:
                w.events.append({"pid": p["id"], "type": "Utvandring", "date": d, "reg": reg, "from": src["id"],
                                 "to": None, "from_out": None, "to_out": "ABROAD"})
                p["unit"] = None
            p["since"] = d
            done += 1
    # second moves after the register day for some movers (the 1 November address is the first move's origin)
    movers = [e for e in w.events if e["type"] == "Flytting" and e["date"] > W.REGISTER_DAY and e["to"] is not None
              and w.by_id[e["to"]]["category"] == "Bolig"]
    for e in movers[::9]:
        p = w.person_by_id[e["pid"]]
        cur = w.by_id[p["unit"]]
        same = [u for u in lived if u["nr"] == cur["nr"] and u["id"] != cur["id"]]
        dst = same[int(rng.integers(0, len(same)))]
        d = e["date"] + dt.timedelta(days=int(rng.integers(5, 25)))
        if d >= hi:
            continue
        w.events.append({"pid": p["id"], "type": "Flytting", "date": d, "reg": d + dt.timedelta(days=int(rng.integers(0, 5))),
                         "from": cur["id"], "to": dst["id"], "from_out": None, "to_out": None})
        p["unit"] = dst["id"]
        p["since"] = d
    # births and arrivals after the register day (in the snapshot, not on 1 November)
    pid = max(p["id"] for p in w.persons)
    for kind, count in (("birth", int(n * 0.0024)), ("arrival", int(n * 0.0030))):
        for i in range(count):
            u = lived[int(rng.integers(0, len(lived)))]
            d = dt_after(after_lo, hi)
            pid += int(rng.integers(1, 7))
            born = d if kind == "birth" else d - dt.timedelta(days=int(rng.integers(20, 60) * 365.25))
            p = {"id": pid, "born": born, "unit": u["id"], "nov1_unit": None, "since": d}
            w.persons.append(p)
            w.events.append({"pid": pid, "type": "Fødsel" if kind == "birth" else "Innvandring", "date": d,
                             "reg": d + dt.timedelta(days=int(rng.integers(1, 9))), "from": None, "to": u["id"],
                             "from_out": "ABROAD" if kind == "arrival" else None, "to_out": None})
    w.person_by_id = {p["id"]: p for p in w.persons}
    # the cadastre's renumbering of blocks whose residential floors were numbered from a ground floor of shops: from
    # the change the flats carry the floor above, and the population register records each resident of the block that
    # day as moving to the new unit number
    w.renumbered = {}
    timeline = {}
    for e in sorted(w.events, key=lambda e: (e["date"], e["reg"], e["pid"])):
        timeline.setdefault(e["pid"], []).append(e)

    def unit_at(p, day):
        u = p["nov1_unit"]
        for e in timeline.get(p["id"], []):
            if W.REGISTER_DAY < e["date"] <= day:
                u = e["to"]
        return u

    def band(p):
        a = _age_on(p["born"], W.REGISTER_DAY)
        return 0 if a <= 17 else (1 if a <= 66 else 2)
    nov1_by_unit = {}
    for p in w.persons:
        if p["nov1_unit"] is not None:
            nov1_by_unit.setdefault(p["nov1_unit"], []).append(p)
    for mi, (nr, *_r) in enumerate(W.MUNICIPALITIES):
        blocks = sorted({u["building"] for u in counted if u["nr"] == nr and u["type"] == "Leilighet"})
        pick, bands = [], set()
        for i in rng.permutation(len(blocks)):
            b = blocks[int(i)]
            ground = [u for u in counted if u["building"] == b and u["unit"].startswith("H01")]
            got = {band(p) for u in ground for p in nov1_by_unit.get(u["id"], [])}
            if not got - bands:
                continue
            pick.append(b)
            bands |= got
            if bands == {0, 1, 2} or len(pick) == 4:
                break
        if not pick:
            pick = [b for b in blocks if any(not u.get("vacant") for u in counted if u["building"] == b
                                             and u["unit"].startswith("H01"))][:1]
        # a small municipality's few blocks: the households on their ground floors take in a child, a lodger or a
        # parent, so every age band lives there on 1 November
        flats = sorted([u for u in counted if u["building"] in pick and u["unit"].startswith("H01")
                        and not u.get("vacant")], key=lambda u: u["id"])
        for miss in sorted({0, 1, 2} - bands):
            u = flats[int(rng.integers(0, len(flats)))]
            pid = max(p["id"] for p in w.persons) + int(rng.integers(1, 7))
            age = int(rng.integers(3, 16)) if miss == 0 else (int(rng.integers(25, 61)) if miss == 1 else
                                                             int(rng.integers(68, 86)))
            p = _person(rng, pid, u, age)
            w.persons.append(p)
            w.person_by_id[pid] = p
            u["household"] = u.get("household", 0) + 1
            u["registered_nov1"] = u.get("registered_nov1", 0) + 1
            bands.add(miss)
        for b in pick:
            d = dt.date(2026, 11, int(rng.integers(12, 28)))
            ids = set()
            for u in sorted([u for u in counted if u["building"] == b], key=lambda u: u["unit"]):
                old = u["unit"]
                u["unit_old"] = old
                u["unit"] = "H%02d%02d" % (int(old[1:3]) + 1, int(old[3:5]))
                w.renumbered[u["id"]] = (old, u["unit"], d)
                ids.add(u["id"])
            for p in sorted(w.persons, key=lambda q: q["id"]):
                at = unit_at(p, d)
                if at not in ids or any(e["date"] == d for e in timeline.get(p["id"], [])):
                    continue
                w.events.append({"pid": p["id"], "type": "Flytting", "date": d, "reg": d, "from": at, "to": at,
                                 "from_out": None, "to_out": None, "renumber": w.renumbered[at][:2]})
                if p["unit"] == at and p["since"] <= d:
                    p["since"] = d
    w.events.sort(key=lambda e: (e["reg"], e["pid"], e["date"]))


def _age_on(born, day):
    return day.year - born.year - ((day.month, day.day) < (born.month, born.day))


# ---------------------------------------------------------------------------------------------- the land register
SURNAMES = ["HANSEN", "JOHANSEN", "OLSEN", "LARSEN", "ANDERSEN", "PEDERSEN", "NILSEN", "KRISTIANSEN", "JENSEN",
            "KARLSEN", "JOHNSEN", "PETTERSEN", "ERIKSEN", "BERG", "HAUGEN", "HAGEN", "JOHANNESSEN", "ANDREASSEN",
            "JACOBSEN", "DAHL", "JØRGENSEN", "HALVORSEN", "LUND", "SØRENSEN", "MOEN", "GUNDERSEN", "IVERSEN",
            "STRAND", "SOLBERG", "SVENDSEN", "EIDE", "KNUTSEN", "MARTINSEN", "PAULSEN", "BAKKEN", "KRISTOFFERSEN",
            "MATHISEN", "LIE", "AMUNDSEN", "NGUYEN", "RASMUSSEN", "BERGE", "MOE", "NYGÅRD", "FREDRIKSEN", "SOLHEIM",
            "HOLM", "LUNDE", "KNUDSEN", "AAS", "KLEPP", "HOLMEN", "BRATLIE", "VIK", "MYHRE", "TANGEN", "RUUD",
            "SKOG", "TVEIT", "HAUGLAND"]
NEUTRAL = ["FJORDHUS", "NORDLYS", "BRATTLI", "SKOGLY", "SOLTUN", "LIATUN", "HAVGLIMT", "FURULY", "BJØRKELY", "ELVETUN"]


def _ownership(w):
    """Title holders per property or condominium section; the municipalities' housing held directly (some of it under
    titles from before the business register, in the municipality's name of the day and with no organisation number),
    through a municipal enterprise (KF), through a company the municipality owns with its holding company, or through
    a wholly owned company; private companies in a municipality's name, an inter-municipal company, and the 2026
    transfers, some registered after 1 November."""
    rng = w.rng
    w.orgs = []
    w.shareholders = []
    w.titles = []
    w.transfers = []
    orgno = [910000000]

    def new_org(name, form, nr, parent=None):
        orgno[0] += int(rng.integers(1000, 90000))
        o = {"orgnr": orgno[0], "name": name, "form": form, "parent": parent, "nr": nr}
        w.orgs.append(o)
        return o
    w.muni_org, w.muni_holders, w.muni_legal, w.namesakes, w.landlord, w.private = {}, {}, {}, {}, {}, {}
    for mi, (nr, name, kind, *_r) in enumerate(W.MUNICIPALITIES):
        up = name.upper()
        m = new_org("%s KOMMUNE" % up, "KOMM", nr)
        w.muni_org[nr] = m
        holders = [m["orgnr"]]
        style = mi % 3
        if style == 0:
            kf = new_org("%s KOMMUNALE BOLIGER KF" % up, "KF", nr, parent=m["orgnr"])
            holders.append(kf["orgnr"])
        elif style == 1:
            hold = new_org("%s EIENDOM AS" % up, "AS", nr)
            rent = new_org("%s UTLEIE AS" % NEUTRAL[mi], "AS", nr)
            w.shareholders.append({"company": hold["orgnr"], "holder": m["orgnr"], "n": 1000, "total": 1000})
            w.shareholders.append({"company": rent["orgnr"], "holder": hold["orgnr"], "n": 600, "total": 1000})
            w.shareholders.append({"company": rent["orgnr"], "holder": m["orgnr"], "n": 400, "total": 1000})
            holders += [hold["orgnr"], rent["orgnr"]]
        else:
            hb = new_org("%s BOLIGSELSKAP AS" % up, "AS", nr)
            w.shareholders.append({"company": hb["orgnr"], "holder": m["orgnr"], "n": 100, "total": 100})
            holders.append(hb["orgnr"])
        w.muni_holders[nr] = holders
        w.landlord[nr] = holders[-1]
        # the municipality's name on titles from before the business register
        w.muni_legal[nr] = {"town": ["%s BYKOMMUNE" % up, "%s KOMMUNE V/RÅDMANNEN" % up]}.get(
            kind, ["%s HERREDSKOMMUNE" % up, "%s KOMMUNE V/RÅDMANNEN" % up])
        if nr in W.OLD_NUMBER:
            w.muni_legal[nr] = ["%s KOMMUNE V/EIENDOMSFORVALTNINGEN" % up]
        # private companies in the municipality's name that it does not own
        w.namesakes[nr] = []
        for suffix in ("BYGG AS", "UTLEIE OG EIENDOM AS", "BOLIGUTVIKLING AS"):
            o = new_org("%s %s" % (up, suffix), "AS", nr)
            w.shareholders.append({"company": o["orgnr"], "holder": "P%08d" % (60000000 + int(rng.integers(0, 9999999))),
                                   "n": 100, "total": 100})
            w.namesakes[nr].append(o["orgnr"])
        # private landlords
        w.private[nr] = []
        for j in range(6):
            sur = SURNAMES[(mi * 6 + j) % len(SURNAMES)]
            o = new_org("%s %s" % (sur, ("EIENDOM AS", "UTLEIE AS", "BOLIGER AS", "INVEST AS")[j % 4]), "AS", nr)
            w.shareholders.append({"company": o["orgnr"], "holder": "P%08d" % (60000000 + int(rng.integers(0, 9999999))),
                                   "n": 30, "total": 30})
            w.private[nr].append(o["orgnr"])
    # an inter-municipal company two municipalities own between them
    iks = new_org("BREKKEVOLL OG RAVNSUND BOLIGSELSKAP IKS", "IKS", "5801")
    w.iks = iks["orgnr"]
    for key in sorted(w.props):
        if w.props[key]["kind"] == "coop":
            prop = w.props[key]
            prop["coop"] = new_org("BORETTSLAGET %s %d" % (prop["street"].upper(), prop["no"]), "BRL", prop["nr"])

    def person_holder():
        return "P%08d" % (60000000 + int(rng.integers(0, 9999999)))

    def title(nr, gnr, bnr, snr, hid, name, reg):
        w.titles.append({"nr": nr, "gnr": gnr, "bnr": bnr, "snr": snr, "holder": str(hid) if hid else "",
                         "name": name, "reg": reg})
    org_name = {o["orgnr"]: o["name"] for o in w.orgs}
    for key in sorted(w.props):
        prop = w.props[key]
        nr = prop["nr"]
        holders = w.muni_holders[nr]
        if prop["kind"] == "rental":
            r = rng.random()
            if r < 0.55:
                h = w.landlord[nr]
            elif r < 0.65:
                h = w.namesakes[nr][1]
            elif r < 0.70 and nr in ("5801", "5806"):
                h = w.iks
            else:
                h = w.private[nr][int(rng.integers(0, len(w.private[nr])))]
            title(nr, prop["gnr"], prop["bnr"], 0, h, org_name[h],
                  dt.date(int(rng.integers(1995, 2026)), int(rng.integers(1, 13)), 1))
        elif prop["kind"] == "coop":
            title(nr, prop["gnr"], prop["bnr"], 0, prop["coop"]["orgnr"], prop["coop"]["name"],
                  dt.date(int(rng.integers(1980, 2020)), 6, 1))
        elif prop["kind"] == "condo":
            dev = rng.random() < 0.12
            for u in prop["units"]:
                r = rng.random()
                if r < 0.08:
                    h = holders[int(rng.integers(0, len(holders)))]
                elif dev and r < 0.40:
                    h = w.namesakes[nr][2]
                else:
                    h = None
                reg = dt.date(int(rng.integers(1998, 2026)), int(rng.integers(1, 13)), 1)
                if h is None:
                    title(nr, prop["gnr"], prop["bnr"], u["snr"], person_holder(), "", reg)
                else:
                    title(nr, prop["gnr"], prop["bnr"], u["snr"], h, org_name[h], reg)
        else:
            reg = dt.date(int(rng.integers(1990, 2026)), int(rng.integers(1, 13)), 1)
            r = rng.random()
            if r < 0.025:
                h = holders[int(rng.integers(0, len(holders)))]
                title(nr, prop["gnr"], prop["bnr"], 0, h, org_name[h], reg)
            elif r < 0.035:
                h = w.namesakes[nr][0]
                title(nr, prop["gnr"], prop["bnr"], 0, h, org_name[h], reg)
            else:
                title(nr, prop["gnr"], prop["bnr"], 0, person_holder(), "", reg)
    by_key = {(t["nr"], t["gnr"], t["bnr"], t["snr"]): t for t in w.titles}
    # the inter-municipal company's blocks, one in each of its two owners
    for nr in ("5801", "5806"):
        if not any(t["holder"] == str(w.iks) for t in w.titles if t["nr"] == nr):
            pr = [k for k in sorted(by_key) if k[0] == nr and w.props[k[:3]]["kind"] == "rental"
                  and by_key[k]["holder"] in {str(x) for x in w.private[nr]}]
            t = by_key[pr[int(rng.integers(0, len(pr)))]]
            t["holder"], t["name"] = str(w.iks), org_name[w.iks]
    # titles from before the business register: the municipality's own houses and blocks under its name of the day
    w.old_titles = set()
    for nr, *_r in W.MUNICIPALITIES:
        houses = [k for k in sorted(by_key) if k[0] == nr and w.props[k[:3]]["kind"] == "house"
                  and by_key[k]["holder"].startswith("P")]
        rentals = [k for k in sorted(by_key) if k[0] == nr and w.props[k[:3]]["kind"] == "rental"
                   and by_key[k]["holder"] == str(w.landlord[nr])]
        pick = [houses[int(i)] for i in rng.choice(len(houses), size=int(rng.integers(3, 7)), replace=False)]
        if rentals and rng.random() < 0.6:
            pick.append(rentals[int(rng.integers(0, len(rentals)))])
        for k in pick:
            t = by_key[k]
            t["holder"] = ""
            t["name"] = w.muni_legal[nr][int(rng.integers(0, len(w.muni_legal[nr])))]
            t["reg"] = dt.date(int(rng.integers(1968, 1990)), int(rng.integers(1, 13)), int(rng.integers(1, 28))) \
                if nr not in W.OLD_NUMBER else dt.date(2024, 1, 1)
            w.old_titles.add(k)
    # the 2026 transfers; those registered after 1 November change the snapshot's holder
    keys = sorted(by_key)
    w.title_nov1 = {k: by_key[k]["holder"] or by_key[k]["name"] for k in keys}
    muni_ids = {nr: {str(x) for x in hs} for nr, hs in w.muni_holders.items()}

    def transfer(k, new, new_name, reg, doc):
        t = by_key[k]
        w.transfers.append({"nr": k[0], "gnr": k[1], "bnr": k[2], "snr": k[3], "from": t["holder"],
                            "from_name": t["name"], "to": str(new) if new else "", "to_name": new_name,
                            "reg": reg, "doc": doc})
        if reg <= W.REGISTER_DAY:
            w.title_nov1[k] = str(new)
        t["holder"] = str(new)
        t["name"] = new_name
        t["reg"] = reg
    free = [k for k in keys if k not in w.old_titles and w.props[k[:3]]["kind"] != "coop"]
    taken = set()
    for i in rng.choice(len(free), size=int(len(free) * 0.05), replace=False):
        k = free[int(i)]
        taken.add(k)
        reg = dt.date(2026, 1, 5) + dt.timedelta(days=int(rng.integers(0, 290)))
        transfer(k, person_holder(), "", reg, reg - dt.timedelta(days=int(rng.integers(8, 40))))
    # after 1 November: each municipality's housing bought and sold, the deed often signed before the register day
    for mi, (nr, *_r) in enumerate(W.MUNICIPALITIES):
        mine = [k for k in free if k[0] == nr and k not in taken and by_key[k]["holder"] in muni_ids[nr]]
        other = [k for k in free if k[0] == nr and k not in taken and by_key[k]["holder"].startswith("P")]
        n_sell = int(rng.integers(1, 4))
        n_buy = int(rng.integers(0, 3))
        if n_sell == n_buy:
            n_buy += 1 if mi % 2 else -1
        n_buy = max(n_buy, 0)
        for j, k in enumerate([mine[int(i)] for i in rng.choice(len(mine), size=min(n_sell, len(mine)), replace=False)]):
            taken.add(k)
            reg = dt.date(2026, 11, 2) + dt.timedelta(days=int(rng.integers(0, 50)))
            doc = dt.date(2026, 10, 30) - dt.timedelta(days=int(rng.integers(0, 25))) if j == 0 else \
                reg - dt.timedelta(days=int(rng.integers(3, 9)))
            transfer(k, person_holder(), "", reg, min(doc, reg - dt.timedelta(days=3)))
        for j, k in enumerate([other[int(i)] for i in rng.choice(len(other), size=n_buy, replace=False)]):
            taken.add(k)
            h = w.landlord[nr]
            reg = dt.date(2026, 11, 3) + dt.timedelta(days=int(rng.integers(0, 50)))
            transfer(k, h, org_name[h], reg, reg - dt.timedelta(days=int(rng.integers(3, 9))))
    w.transfers.sort(key=lambda x: (x["reg"], x["nr"], x["gnr"], x["bnr"], x["snr"]))


# ---------------------------------------------------------------------------------------------- the meter data hub
def _meters(w):
    """The household metering points the data agreement covers: one per dwelling from the day it was taken into use
    (a dwelling still being built draws on the builder's construction supply, outside the agreement), communal points
    in the blocks, and no holiday homes; some dwellings changed meter in the fortnight (a new metering point from the
    change)."""
    rng = w.rng
    w.meters = []
    mp = 707057500100000000
    for u in sorted(w.units, key=lambda x: x["id"]):
        if u["category"] != "Bolig" or u["in_use"] is None:
            continue
        mp += int(rng.integers(11, 977))
        m = {"mp": mp, "unit": u["id"], "from": dt.date(int(rng.integers(2016, 2025)), int(rng.integers(1, 13)), 1),
             "to": None, "type": "privat"}
        if u["in_use"] > W.REGISTER_DAY:
            m["from"] = u["in_use"]
        w.meters.append(m)
        u["meters"] = [m]
        if u["counted"] and rng.random() < 0.012:
            change = W.FORTNIGHT_START + dt.timedelta(days=int(rng.integers(2, 12)))
            m["to"] = change
            mp += int(rng.integers(11, 977))
            m2 = {"mp": mp, "unit": u["id"], "from": change, "to": None, "type": "privat"}
            w.meters.append(m2)
            u["meters"].append(m2)
    for nr, *_r in W.MUNICIPALITIES:
        for i in range(6):
            mp += int(rng.integers(11, 977))
            w.meters.append({"mp": mp, "unit": None, "from": dt.date(2015, 1, 1), "to": None, "type": "felles",
                             "nr": nr})


# ---------------------------------------------------------------------------------------------- hourly loads
def _loads(w):
    """Hourly kWh per metering point over the fortnight in Norwegian time. A lived-in dwelling: appliances, its
    heating against the outdoor temperature at a lived-in setting, and the household's own day (showers and
    breakfast in the morning, cooking, light and washing in the evening) on the days someone was at home. A vacant
    dwelling: its heating at the setting it was left on, a fridge or nothing, never a household's day."""
    rng = w.rng
    hod = np.arange(W.HOURS) % 24
    dow = (np.arange(W.HOURS) // 24) % 7
    w.load = {}
    for u in sorted(w.units, key=lambda x: x["id"]):
        if u["category"] == "Annet" or not u.get("meters"):
            continue
        T = w.temp[u["nr"]]
        area = u["area"]
        kind = u.get("vacant") if u["counted"] else None
        if not u["counted"]:
            # taken into use after 1 November: its household moved in on the day its meter began
            u["household"] = int(rng.choice([1, 2, 3, 4], p=[0.3, 0.35, 0.2, 0.15]))
        Hk = area * rng.uniform(0.0010, 0.0016) if u["type"] != "Leilighet" else area * rng.uniform(0.0006, 0.0010)
        cop = 1.0 if u["heating"] == "electric" else (rng.uniform(2.4, 3.4) if u["heating"] == "heatpump" else None)
        load = np.zeros(W.HOURS)
        if kind is None:
            tset = rng.uniform(19.5, 22.0)
            if cop is not None:
                load += np.maximum(0, tset - T) * Hk / cop
            base = rng.uniform(0.10, 0.28)
            load += base
            present = rng.random(W.DAYS) < rng.choice([0.97, 0.9, 0.75, 0.55], p=[0.55, 0.25, 0.15, 0.05])
            if present.sum() < 3:
                present[rng.choice(W.DAYS, 3, replace=False)] = True
            scale = (0.6 + 0.25 * u["household"]) * rng.uniform(0.75, 1.3)
            for d in range(W.DAYS):
                if not present[d]:
                    continue
                s = d * 24
                wk = (d % 7) >= 5
                m0 = int(rng.integers(6, 8)) + (1 if wk else 0)
                load[s + m0:s + m0 + 2] += rng.uniform(1.2, 2.5) * scale
                e0 = int(rng.integers(16, 18))
                e1 = int(rng.integers(21, 23))
                load[s + e0:s + e1] += rng.uniform(0.6, 1.5) * scale
                load[s + e0 + 1:s + e0 + 3] += rng.uniform(0.4, 1.2) * scale
                if rng.random() < 0.35:
                    w0 = int(rng.integers(18, 21))
                    load[s + w0:s + w0 + 2] += rng.uniform(0.6, 1.4)
        elif kind == "heated":
            tset = rng.uniform(8.0, 14.0)
            load += np.maximum(0, tset - T) * Hk * 0.7
            load += rng.uniform(0.02, 0.07)
        elif kind == "heatpump":
            tset = rng.uniform(9.0, 14.0)
            load += np.maximum(0, tset - T) * Hk / (cop or 2.8)
            load += rng.uniform(0.02, 0.06)
        elif kind == "tiny":
            load += rng.uniform(0.015, 0.06) + np.maximum(0, 4 - T) * rng.uniform(0.0, 0.004)
        elif kind == "off":
            pass
        noise = rng.normal(0, 0.012, W.HOURS) + load * rng.normal(0, 0.03, W.HOURS)
        load = np.round(np.maximum(load + noise, 0.0), 3)
        if kind == "off":
            load[:] = 0.0
        w.load[u["id"]] = load
    for m in w.meters:
        if m["unit"] is None:
            T = w.temp[m["nr"]]
            w.load[("felles", m["mp"])] = np.round(0.4 + 0.02 * np.maximum(0, 10 - T) + rng.normal(0, 0.01, W.HOURS), 3)


def _outages(w):
    """The grid company's outages in the fortnight: a few hours with no supply to one area of a municipality, the
    meters reading nothing for those hours."""
    rng = w.rng
    w.outages = []
    for nr in ("5801", "5805", "5810"):
        d = int(rng.integers(2, 12))
        h0 = int(rng.integers(9, 13))
        dur = int(rng.integers(2, 5))
        ids = sorted(u["id"] for u in w.units if u["nr"] == nr and u["id"] in w.load)
        pick = sorted(ids[int(i)] for i in rng.choice(len(ids), size=min(len(ids), int(rng.integers(80, 220))),
                                                       replace=False))
        for uid in pick:
            w.load[uid][d * 24 + h0:d * 24 + h0 + dur] = 0.0
        w.outages.append({"nr": nr, "day": d, "h0": h0, "dur": dur, "customers": len(pick)})


def _prices(w):
    """The power exchange's day-ahead prices for the price area, by hour of Norwegian time: a morning and an evening
    peak on working days, higher through the cold spell."""
    rng = w.rng
    hod = np.arange(W.HOURS) % 24
    d = np.arange(W.HOURS) // 24
    level = 62 + 38 * np.exp(-((d - 7.5) / 2.6) ** 2) + rng.normal(0, 4, W.DAYS).cumsum()[d] * 0.6
    shape = 1 + 0.28 * np.exp(-((hod - 8) / 1.6) ** 2) + 0.34 * np.exp(-((hod - 18) / 2.0) ** 2) - \
        0.18 * np.exp(-((hod - 3) / 2.2) ** 2)
    weekend = np.isin(d % 7, (5, 6))
    shape = np.where(weekend, 1 + (shape - 1) * 0.45, shape)
    w.prices = np.round(level * shape + rng.normal(0, 2.5, W.HOURS), 2)
