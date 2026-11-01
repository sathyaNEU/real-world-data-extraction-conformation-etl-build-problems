"""The region's records around the dispensing register (own random stream, so the main call's draws never move):
the pharmacy each dispensing was made at, the prescriber of each dispensing, the personal-number replacements of
2026, and the 2026 pharmacy pilot (follow-up conversations and the quarterly statements)."""
import collections
import datetime as dt

import params as P

PHARMACIES = [
    ("A102", "Lindholt Apotek", "Lindholt"), ("A107", "Lindholt Torve Apotek", "Lindholt"),
    ("A114", "Hornslev Apotek", "Hornslev"), ("A121", "Vejlby Apotek", "Vejlby"),
    ("A126", "Rødby Strand Apotek", "Rødby Strand"), ("A133", "Ellerup Apotek", "Ellerup"),
    ("A139", "Tvede Apotek", "Tvede"), ("A145", "Søndergade Apotek", "Lindholt"),
]
TOWN_PHARMACIES = collections.defaultdict(list)
for _code, _name, _town in PHARMACIES:
    TOWN_PHARMACIES[_town].append(_code)
HOSPITAL_UNITS = ["SGH-KARD-4302", "SGH-MED-4311", "SGH-ENDO-4318", "SGH-NEU-4327"]
# the pilot's contract rate per follow-up conversation (DKK), each pharmacy its own
PILOT_RATE = {"A102": 213, "A107": 196, "A114": 238, "A121": 187, "A126": 249, "A133": 222, "A139": 204, "A145": 261}
QUARTER_ENDS = [dt.date(2026, 3, 31), dt.date(2026, 6, 30), dt.date(2026, 9, 30), dt.date(2026, 12, 31)]


def quarter_of(d):
    return (d.month - 1) // 3


def build(W, rng):
    A = type("Asks", (), {})()
    towns = {code: town for code, name, town, *rest in P.PRACTICES}
    # each patient's own pharmacy, mostly in their practice's town
    for pt in W.patients:
        local = TOWN_PHARMACIES[towns[pt.practice]]
        pt.pharmacy = rng.choice(local) if rng.random() < 0.85 else rng.choice([c for c, n, t in PHARMACIES])
    # the dispensing rows: (pseudonym, sex, born, date, product number, packs, prescriber, pharmacy, true patient)
    rows = []
    for pt in W.patients:
        cands = sorted(pt.cands, key=lambda p: p.number)
        by_pack = collections.defaultdict(list)
        for p in cands:
            by_pack[p.pack].append(p)
        fav = None
        for i, (d, packs, pack) in enumerate(pt.runs):
            prods = by_pack[pack]
            if fav is None or fav.pack != pack or rng.random() < 0.18:
                fav = rng.choice(prods)
            prescriber = pt.practice
            pharm = pt.pharmacy if rng.random() < 0.93 else rng.choice([c for c, n, t in PHARMACIES])
            rows.append({"id": pt.id, "sex": pt.sex, "born": pt.born, "date": d, "product": fav.number,
                         "packs": packs, "prescriber": prescriber, "pharmacy": pharm, "patient": pt})
    # personal numbers replaced in 2026: from the change the register carries the person under a new pseudonym
    seen = collections.Counter((pt.born, pt.sex) for pt in W.patients)
    ids = {pt.id for pt in W.patients}

    def new_id():
        while True:
            x = "%08X" % rng.randrange(0x10000000, 0xFFFFFFFF)
            if x not in ids:
                ids.add(x)
                return x
    by_patient = collections.defaultdict(list)
    for r in rows:
        by_patient[r["patient"].id].append(r)
    replaced = []
    for code, *_ in P.PRACTICES:
        pool = [pt for pt in W.patients if pt.practice == code and not pt.cohort and seen[(pt.born, pt.sex)] == 1]
        rng.shuffle(pool)
        want = rng.choice([1, 2, 2, 3])
        for pt in pool:
            if sum(1 for r in replaced if r["practice"] == code) >= want:
                break
            rs = sorted(by_patient[pt.id], key=lambda r: r["date"])
            q26 = {quarter_of(r["date"]) for r in rs if r["date"].year == 2026}
            if q26 != {0, 1, 2, 3}:
                continue
            mid = [r for r in rs if dt.date(2026, 4, 15) <= r["date"] <= dt.date(2026, 9, 15)]
            if not mid:
                continue
            cut = mid[0]["date"]
            nid = new_id()
            for r in rs:
                if r["date"] >= cut:
                    r["id"] = nid
            replaced.append({"old": pt.id, "new": nid, "from": cut, "practice": code})
    A.replaced = replaced
    # hospital departments prescribe now and then for patients long on a statin: in the old system's months and in
    # 2026 (never a new user's dispensing, never a person's last of 2026, never around a number's replacement)
    moved = {r["old"] for r in replaced}
    for pid, rs in sorted(by_patient.items()):
        pt = rs[0]["patient"]
        if pt.cohort or pid in moved:
            continue
        rs = sorted(rs, key=lambda r: r["date"])
        last26 = max([i for i, r in enumerate(rs) if r["date"].year == 2026], default=-1)
        for i, r in enumerate(rs):
            if i == 0 or i == last26:
                continue
            if (r["date"] <= P.OLD_SYSTEM_END or r["date"].year == 2026) and rng.random() < 0.04:
                r["prescriber"] = rng.choice(HOSPITAL_UNITS)
    A.rows = sorted(rows, key=lambda r: (r["date"], r["pharmacy"], r["id"], r["product"]))
    # the 2026 pilot: follow-up conversations at the pharmacies, cancelled now and then, some after the statement
    convs = []
    n_conv = {"A102": 312, "A107": 241, "A114": 187, "A121": 158, "A126": 133, "A133": 176, "A139": 149, "A145": 204}
    late_pharm = set(n_conv)
    seq = 7000 + rng.randrange(0, 300)
    for code, n in n_conv.items():
        for _ in range(n):
            d = dt.date(2026, 1, 5) + dt.timedelta(days=rng.randrange(0, 358))
            seq += rng.randrange(1, 4)
            status, cancelled = "afholdt", None
            x = rng.random()
            if x < 0.05:
                status, cancelled = "aflyst", d + dt.timedelta(days=rng.randrange(0, 9))
                if cancelled in QUARTER_ENDS:
                    cancelled += dt.timedelta(days=1)
            convs.append({"no": "S%05d" % seq, "pharmacy": code, "date": d, "status": status, "cancelled": cancelled})
        # cancellations entered after the quarter's statement: a conversation registered as held that turned out
        # not to have taken place
        if code in late_pharm:
            for qi, qe in enumerate(QUARTER_ENDS):
                held = [c for c in convs if c["pharmacy"] == code and c["status"] == "afholdt" and
                        quarter_of(c["date"]) == qi]
                for c in rng.sample(held, rng.randint(1, 3)):
                    c["status"] = "aflyst"
                    c["cancelled"] = qe + dt.timedelta(days=rng.randint(4, 20 if qi == 3 else 40))
    convs.sort(key=lambda c: (c["date"], c["no"]))
    A.conversations = convs
    stm = []
    for code, name, town in PHARMACIES:
        for qi, qe in enumerate(QUARTER_ENDS):
            n = sum(1 for c in convs if c["pharmacy"] == code and quarter_of(c["date"]) == qi and
                    (c["cancelled"] is None or c["cancelled"] > qe))
            stm.append({"pharmacy": code, "quarter": qi + 1, "date": qe, "count": n, "amount": n * PILOT_RATE[code]})
    A.statements = stm
    A.payment_due = {code: PILOT_RATE[code] * sum(1 for c in convs if c["pharmacy"] == code and c["cancelled"] is None)
                     for code, name, town in PHARMACIES}
    A.payment_due_q = {(code, qi + 1): PILOT_RATE[code] * sum(1 for c in convs if c["pharmacy"] == code and
                                                              quarter_of(c["date"]) == qi and c["cancelled"] is None)
                       for code, name, town in PHARMACIES for qi in range(4)}
    return A
