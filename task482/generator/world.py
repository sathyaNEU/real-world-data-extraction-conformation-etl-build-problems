"""task482 architecture 17: the truth. The item pool (fixed by POOL_SEED), the member schools, their Term 3
sequences and sitting days, the candidates, their responses, the entries register, the make-up sitting. Nothing
here is shipped as is; build.py writes the pack from it."""
import datetime as dt
import math

import numpy as np

import params as P
import rasch as RA

ONE = dt.timedelta(days=1)

SCHOOL_WORDS = ["Ashcombe", "Brenmoor", "Carrick Vale", "Dunholm", "Eastcliffe", "Fernlea", "Glenarvon", "Harrowgate",
                "Inchbury", "Jarvis Bay", "Kerrowdale", "Larchmont", "Marlow Heights", "Northbury", "Ormiston Park",
                "Pendleford", "Queensbury Hill", "Ravensworth", "Selwyn Downs", "Tarrant", "Ulverdale", "Valemount",
                "Westerleigh", "Yarrowby", "Aldmoor", "Belvoir Grove", "Clareston", "Drummond Hill", "Elmsworth",
                "Foxhaven", "Greystone Bay", "Hollingbrook", "Ivanhoe Ridge", "Kingsclere", "Lindenhurst",
                "Merrivale", "Netherby", "Oakmere", "Penrose Hill", "Rothbury", "Somerleigh", "Thornbury Vale",
                "Wexcombe", "Abbotsleigh", "Bramblewood", "Cranleigh Downs", "Dovercourt", "Evendale"]
SCHOOL_KINDS = ["College", "School", "Collegiate", "Grammar", "Academy", "College", "School", "College"]

SURNAMES = ["Smith", "Wilson", "Brown", "Taylor", "Williams", "Anderson", "Thompson", "Walker", "Harris", "Martin",
            "Clark", "White", "Young", "King", "Wright", "Robinson", "Campbell", "Mitchell", "Scott", "Stewart",
            "Morris", "Kelly", "Cooper", "Murray", "Bell", "Hall", "Turner", "Parker", "Edwards", "Collins",
            "Ngata", "Tipene", "Walker", "Paewai", "Rangi", "Tamatea", "Horomona", "Te Whata", "Kereama", "Pomare",
            "Faleolo", "Tuilagi", "Leota", "Sapolu", "Fonoti", "Vaifale", "Taufa", "Havili", "Latu", "Folau",
            "Chen", "Wang", "Li", "Zhang", "Liu", "Singh", "Patel", "Sharma", "Kim", "Park", "Nguyen", "Tran",
            "Reid", "Fraser", "McKenzie", "MacDonald", "Ross", "Grant", "Sinclair", "Henderson", "Duncan",
            "Gordon", "Mackay", "Cameron", "Fletcher", "Harvey", "Lawson", "Marsh", "Nash", "Pearce", "Quinn",
            "Rowe", "Shaw", "Tait", "Vincent", "Wallace", "Barker", "Chapman", "Dixon", "Ellis", "Ford", "Gibson",
            "Hughes", "Jenkins", "Knight", "Lloyd", "Mason", "Newton", "Owen", "Palmer", "Russell", "Spencer"]
FIRST_F = ["Olivia", "Charlotte", "Isla", "Amelia", "Ava", "Mia", "Harper", "Willow", "Sophie", "Grace", "Ella",
           "Ruby", "Emily", "Lily", "Zoe", "Hannah", "Aria", "Maia", "Anahera", "Kaia", "Mere", "Ngaio", "Aroha",
           "Leilani", "Sina", "Mele", "Ana", "Grace", "Chloe", "Jessica", "Georgia", "Madison", "Lucy", "Eva",
           "Holly", "Sienna", "Poppy", "Ivy", "Freya", "Jasmine", "Priya", "Mei", "Yuna", "Linh", "Sara", "Tessa"]
FIRST_M = ["Oliver", "Jack", "Noah", "Leo", "George", "Charlie", "Lucas", "William", "Thomas", "James", "Henry",
           "Hunter", "Max", "Mason", "Liam", "Ethan", "Samuel", "Harry", "Archie", "Finn", "Nikau", "Tama", "Wiremu",
           "Rawiri", "Manaia", "Ihaia", "Sione", "Tevita", "Losa", "Isaac", "Joshua", "Daniel", "Benjamin",
           "Ryan", "Caleb", "Logan", "Cooper", "Arlo", "Hugo", "Felix", "Arjun", "Wei", "Jun", "Minh", "Kai", "Toby"]


def schooldays_between(a, b):
    """Weekdays in (a, b]."""
    n, d = 0, a
    while d < b:
        d += ONE
        if d.weekday() < 5:
            n += 1
    return n


def add_schooldays(a, k):
    d = a
    while k > 0:
        d += ONE
        if d.weekday() < 5:
            k -= 1
    return d


def monday(d):
    return d - dt.timedelta(days=d.weekday())


def week_of_term(d, term_start):
    return (monday(d) - monday(term_start)).days // 7 + 1


# ---------------------------------------------------------------- the item pool (fixed across redraws)
def pool():
    g = np.random.default_rng(P.POOL_SEED)
    items = []
    counts = {"U1": 27, "U2": 27, "U3": 27, "U4": 27, "U5": 16, "U6": 16}
    for code, name, strand, term in P.UNITS:
        for k in range(counts[code]):
            items.append(dict(unit=code, unit_name=name, strand=strand, term=term))
    n = len(items)
    codes = g.choice(np.arange(100, 1000), n, replace=False)
    cards = g.choice(np.arange(1040, 4990), n, replace=False)
    for it, c, k in zip(items, codes, cards):
        it["code"] = "S10-%04d" % c
        it["card"] = int(k)
        it["mc"] = bool(g.random() < 0.8)
    t12 = [i for i, it in enumerate(items) if it["term"] < 3]
    t3 = [i for i, it in enumerate(items) if it["term"] == 3]
    b = np.zeros(n)
    delta = np.zeros(n)
    b[t12] = g.normal(0, P.B_T12_SD, len(t12))
    b[t3] = g.normal(P.B_T3_MEAN, P.B_T3_SD, len(t3))
    delta[t3] = np.clip(g.normal(P.DELTA_MEAN, P.DELTA_SD, len(t3)), P.DELTA_LO, P.DELTA_HI)
    # anchors: five per Term 1 and 2 unit, centred so the anchor block's mean is the scale's zero
    anchors = []
    for u in ("U1", "U2", "U3", "U4"):
        idx = [i for i in t12 if items[i]["unit"] == u]
        anchors += list(g.choice(idx, P.ANCHORS_PER_UNIT, replace=False))
    anchors = sorted(int(a) for a in anchors)
    b -= b[anchors].mean()
    b = np.round(b, 3)
    for i, it in enumerate(items):
        it["anchor"] = i in anchors
    # forms: every anchor on every form, the rest dealt to one form each
    forms = {f: list(anchors) for f in range(P.N_FORMS)}
    for u, per in zip(("U1", "U2", "U3", "U4"), P.FORM_T12):
        rest = [i for i in t12 if items[i]["unit"] == u and i not in anchors]
        g.shuffle(rest)
        pos = 0
        for f in range(P.N_FORMS):
            k = per[f]
            forms[f] += rest[pos:pos + k]
            pos += k
        assert pos == len(rest)
    for u, per in zip(("U5", "U6"), P.FORM_T3):
        rest = [i for i in t3 if items[i]["unit"] == u]
        g.shuffle(rest)
        for f in range(P.N_FORMS):
            forms[f] += rest[f * per:(f + 1) * per]
    for f in forms:
        forms[f] = sorted(forms[f])
        assert len(forms[f]) == P.PAPER_LEN
    # the make-up paper (form M26, printed): its own 50 items' difficulties, for the make-up marks
    bm = g.normal(0.1, 0.9, P.PAPER_LEN)
    return dict(items=items, b=b, delta=delta, anchors=anchors, forms=forms, t12=t12, t3=t3, b_makeup=bm)


# ---------------------------------------------------------------- the schools
def schools(rng):
    out = []
    words = list(SCHOOL_WORDS)
    rng.shuffle(words)
    codes = rng.choice(np.arange(101, 999), sum(P.SCHOOLS_PER_REGION), replace=False)
    starts = [s for s, _ in P.TERM_STARTS]
    probs = np.array([p for _, p in P.TERM_STARTS])
    k = 0
    for reg, ns in zip(P.REGIONS, P.SCHOOLS_PER_REGION):
        for _ in range(ns):
            name = "%s %s" % (words[k], SCHOOL_KINDS[int(rng.integers(len(SCHOOL_KINDS)))])
            ts = starts[int(rng.choice(len(starts), p=probs))]
            first = "U5" if rng.random() < 0.5 else "U6"
            while True:
                span = int(rng.integers(P.SPAN_LO, P.SPAN_HI + 1))
                d0 = int(rng.integers(0, len(P.WINDOW) - span))
                start = P.WINDOW[d0]
                fridays = []
                d = start
                for _ in range(20):
                    d += ONE
                    if d.weekday() == 4:
                        sd = schooldays_between(start, d)
                        if P.END_LO <= sd <= P.END_HI and P.WEEK_LO <= week_of_term(d, ts) <= P.WEEK_HI:
                            fridays.append(d)
                if not fridays:
                    continue
                end1 = fridays[int(rng.integers(len(fridays)))]
                days = [w for w in P.WINDOW[d0:] if w != end1][:span]
                if len(days) == span:
                    break
            out.append(dict(code="C%03d" % codes[k], name=name, region=reg, term_start=ts,
                            term_end=P.TERM3_END[ts], first=first, second="U6" if first == "U5" else "U5",
                            end1=end1, days=days, week_end1=week_of_term(end1, ts)))
            k += 1
    return out


# ---------------------------------------------------------------- candidates, sittings and responses
def candidates(rng, sch, pl):
    used_nsn = set()
    people = []
    entry = 10000
    for s_i, s in enumerate(sch):
        n = int(rng.integers(P.SIZE_LO, P.SIZE_HI + 1))
        mu = P.THETA_MEAN + rng.normal(0, P.THETA_SD_SCHOOL)
        ncls = math.ceil(n / P.CLASS_SIZE)
        cls_day = [s["days"][int(i * len(s["days"]) / ncls)] for i in range(ncls)]
        rng.shuffle(cls_day)
        cls_period = [P.PERIODS[int(rng.integers(len(P.PERIODS)))] for _ in range(ncls)]
        for j in range(n):
            c = j % ncls
            while True:
                nsn = int(rng.integers(100000000, 160000000))
                if nsn not in used_nsn:
                    used_nsn.add(nsn)
                    break
            female = rng.random() < 0.5
            first = (FIRST_F if female else FIRST_M)[int(rng.integers(len(FIRST_F)))]
            dob = dt.date(2011, 1, 1) + dt.timedelta(days=int(rng.integers(0, 365)))
            entry += int(rng.integers(1, 4))
            people.append(dict(school=s_i, cls=c, day=cls_day[c], period=cls_period[c], nsn=nsn,
                               surname=SURNAMES[int(rng.integers(len(SURNAMES)))], first=first,
                               gender="F" if female else "M", dob=dob, entry="26-%05d" % entry,
                               theta=float(rng.normal(mu, P.THETA_SD)), form=None))
        # forms rotate through each class roster
        for c in range(ncls):
            members = [p for p in people if p["school"] == s_i and p["cls"] == c]
            off = int(rng.integers(P.N_FORMS))
            for k, p in enumerate(members):
                p["form"] = (k + off) % P.N_FORMS
    return people


def taught_state(p, s, unit):
    """True when the candidate's own school had finished `unit` before the candidate's sitting day."""
    return unit == s["first"] and p["day"] > s["end1"]


def sit(rng, sch, people, pl):
    items, b, delta = pl["items"], pl["b"], pl["delta"]
    absent = rng.random(len(people)) < P.ABSENT_RATE
    online = [p for p, a in zip(people, absent) if not a]
    away = [p for p, a in zip(people, absent) if a]
    N, I = len(online), len(items)
    R = np.zeros((N, I))
    M = np.zeros((N, I))
    T = np.ones((N, I), bool)
    unit = [it["unit"] for it in items]
    for r, p in enumerate(online):
        s = sch[p["school"]]
        f = pl["forms"][p["form"]]
        M[r, f] = 1
        for i in f:
            if items[i]["term"] == 3:
                T[r, i] = taught_state(p, s, unit[i])
        pr = RA.sig(p["theta"] - b[f] - delta[f] * (~T[r, f]))
        R[r, f] = (rng.random(len(f)) < pr).astype(float)
    return dict(online=online, away=away, R=R, M=M, T=T)


def sessions(rng, sch, online, pl, R):
    """The platform's sessions (UTC) and response rows; a dropped session resumes, and the items answered just
    before the drop are answered again in the resumed session (the later answer stands)."""
    sess, rows = [], []
    sid = 400000
    for r, p in enumerate(online):
        s = sch[p["school"]]
        h, m = p["period"]
        start = dt.datetime.combine(p["day"], dt.time(h, m), P.NZST) + dt.timedelta(minutes=int(rng.integers(0, 7)))
        dur = int(rng.integers(38, 59))
        f = list(pl["forms"][p["form"]])
        order = list(rng.permutation(f))
        sid += int(rng.integers(1, 3))
        if rng.random() < P.RECONNECT_RATE:
            k = int(rng.integers(10, 41))
            redo = int(rng.integers(1, P.REANSWER_MAX + 1))
            t1 = start + dt.timedelta(minutes=int(k * dur / 50))
            sid2 = sid + 1
            t2 = t1 + dt.timedelta(minutes=int(rng.integers(2, 13)))
            end = t2 + dt.timedelta(minutes=dur - int(k * dur / 50))
            sess.append(dict(sid=sid, entry=p["entry"], school=s["code"], form=p["form"], start=start, end=t1,
                             status="dropped"))
            sess.append(dict(sid=sid2, entry=p["entry"], school=s["code"], form=p["form"], start=t2, end=end,
                             status="submitted"))
            for j, i in enumerate(order):
                if j < k:
                    first_val = R[r, i]
                    if j >= k - redo:
                        # answered before the drop, then again after it: the earlier answer is the one replaced
                        first_val = R[r, i] if rng.random() < 0.6 else 1.0 - R[r, i]
                        rows.append((sid, p["entry"], i, first_val))
                        rows.append((sid2, p["entry"], i, R[r, i]))
                    else:
                        rows.append((sid, p["entry"], i, R[r, i]))
                else:
                    rows.append((sid2, p["entry"], i, R[r, i]))
            sid = sid2
        else:
            sess.append(dict(sid=sid, entry=p["entry"], school=s["code"], form=p["form"], start=start,
                             end=start + dt.timedelta(minutes=dur), status="submitted"))
            for i in order:
                rows.append((sid, p["entry"], i, R[r, i]))
    return sess, rows


def world(seed=P.SEED, pl=None, light=False):
    pl = pl or pool()
    rng = np.random.default_rng(seed)
    sch = schools(rng)
    people = candidates(rng, sch, pl)
    st = sit(rng, sch, people, pl)
    w = dict(seed=seed, pool=pl, schools=sch, people=people, **st)
    if light:
        return w
    w["sessions"], w["rows"] = sessions(rng, sch, st["online"], pl, st["R"])
    w["asks"] = asks(np.random.default_rng(seed + P.ASK_SEED_OFFSET), w)
    return w


# ---------------------------------------------------------------- the entries register and the make-up sitting
def _person(rng, school):
    female = rng.random() < 0.5
    return dict(school=school, nsn=int(rng.integers(160000000, 199999999)), gender="F" if female else "M",
                surname=SURNAMES[int(rng.integers(len(SURNAMES)))],
                first=(FIRST_F if female else FIRST_M)[int(rng.integers(len(FIRST_F)))],
                dob=dt.date(2011, 1, 1) + dt.timedelta(days=int(rng.integers(0, 365))))


def asks(rng, w):
    sch, people, online, away = w["schools"], w["people"], w["online"], w["away"]
    codes = [s["code"] for s in sch]
    region_of = [s["region"] for s in sch]
    by_region = {r: [i for i, s in enumerate(sch) if s["region"] == r] for r in P.REGIONS}
    on_set = {p["entry"] for p in online}
    # no two candidates share a first name, surname and birth date (a birth date moves a day where two would)
    used = {}
    for p in people:
        while (p["first"], p["surname"], p["dob"]) in used:
            p["dob"] += ONE
        used[(p["first"], p["surname"], p["dob"])] = p["entry"]
    # twins: two candidates at one school share a surname and a birth date; their first names differ
    twins, taken = [], set()
    for r in P.REGIONS:
        k = int(rng.integers(P.TWINS_PER_REGION[0], P.TWINS_PER_REGION[1] + 1))
        pool_r = [p for p in people if region_of[p["school"]] == r]
        done = 0
        while done < k:
            a = pool_r[int(rng.integers(len(pool_r)))]
            if a["entry"] in taken:
                continue
            mates = [q for q in pool_r if q["school"] == a["school"] and q["entry"] != a["entry"]
                     and q["first"] != a["first"] and q["entry"] not in taken
                     and (q["first"], a["surname"], a["dob"]) not in used]
            if not mates:
                continue
            b = mates[int(rng.integers(len(mates)))]
            del used[(b["first"], b["surname"], b["dob"])]
            b["surname"], b["dob"] = a["surname"], a["dob"]
            used[(b["first"], b["surname"], b["dob"])] = b["entry"]
            twins.append((a, b))
            taken.update((a["entry"], b["entry"]))
            done += 1
    # entries: every candidate's own entry, uploaded by the school in May or June
    entries = []
    for p in people:
        entries.append(dict(entry=p["entry"], nsn=p["nsn"], surname=p["surname"], first=p["first"], dob=p["dob"],
                            gender=p["gender"], school=codes[p["school"]],
                            entered=dt.date(2026, 5, 18) + dt.timedelta(days=int(rng.integers(0, 40))),
                            source="school upload", status="E", person=p["entry"]))
    # late entries keyed by the office from a school's email or call: the office form has no NSN
    late = rng.random(len(entries)) < 0.012
    for e, flag in zip(entries, late):
        if flag:
            e.update(source="office", nsn=None,
                     entered=dt.date(2026, 7, 6) + dt.timedelta(days=int(rng.integers(0, 21))))
    # transfers inside a region: the candidate sat at the new school under an office entry, and the old school's
    # upload still stands
    transfers = []
    nxt = 90000
    for r in P.REGIONS:
        k = int(rng.integers(P.TRANSFERS_PER_REGION[0], P.TRANSFERS_PER_REGION[1] + 1))
        cand = [e for e in entries if region_of[codes.index(e["school"])] == r and e["entry"] in on_set
                and e["source"] == "school upload" and e["person"] not in taken]
        for j in rng.choice(len(cand), k, replace=False):
            e = cand[int(j)]
            olds = [codes[i] for i in by_region[r] if codes[i] != e["school"]]
            old = dict(e)
            nxt += int(rng.integers(3, 40))
            old.update(entry="26-%05d" % nxt, school=olds[int(rng.integers(len(olds)))],
                       entered=dt.date(2026, 5, 18) + dt.timedelta(days=int(rng.integers(0, 30))))
            e.update(source="office", nsn=None,
                     entered=dt.date(2026, 7, 13) + dt.timedelta(days=int(rng.integers(0, 12))))
            entries.append(old)
            transfers.append((old["entry"], e["entry"]))
            taken.add(e["person"])
    # withdrawals: entries a school withdrew before the sitting (never candidates)
    withdrawn = []
    for i, s in enumerate(sch):
        n = int(rng.binomial(max(1, sum(1 for p in people if p["school"] == i)), P.WITHDRAW_RATE))
        for _ in range(n):
            q = _person(rng, i)
            while (q["first"], q["surname"], q["dob"]) in used:
                q["dob"] += ONE
            used[(q["first"], q["surname"], q["dob"])] = None
            nxt += int(rng.integers(3, 40))
            entries.append(dict(entry="26-%05d" % nxt, nsn=q["nsn"], surname=q["surname"], first=q["first"],
                                dob=q["dob"], gender=q["gender"], school=s["code"],
                                entered=dt.date(2026, 5, 18) + dt.timedelta(days=int(rng.integers(0, 40))),
                                source="school upload", status="W", person=None))
            withdrawn.append(entries[-1]["entry"])
    # one school's upload re-sent in June: the same rows again
    resend = codes[int(rng.integers(len(sch)))]
    entries += [dict(e) for e in entries if e["school"] == resend and e["source"] == "school upload"
                and e["status"] == "E"]
    # the make-up sitting: absentees booked into a host centre in week 6, on paper
    # each school sends its absentees to its nearest host centre: the Northern host also takes four Central schools,
    # the Central host half of Capital, the Southern host the other half
    hN, hC, hS = by_region["Northern"][0], by_region["Central"][0], by_region["Southern"][0]
    host_of = {}
    for i in by_region["Northern"]:
        host_of[i] = hN
    for k, i in enumerate(by_region["Central"]):
        host_of[i] = hN if k in (1, 2, 3, 4) else hC
    cap = by_region["Capital"]
    for k, i in enumerate(cap):
        host_of[i] = hC if k < len(cap) // 2 else hS
    for i in by_region["Southern"]:
        host_of[i] = hS
    hosts = {"Northern": hN, "Central": hC, "Southern": hS}
    # booked absentees sit (or do not) on their booked day; the typed roster holds the booked list only. Unbooked
    # absentees who turned up on the day sat at the end of the room and were written onto the supervisor's sheet by
    # hand, which the office never typed: their scripts follow the booked ones and reach only the keyed file.
    roster, scripts, counter, sitters = [], [], {}, []
    unbooked = []
    for p in away:
        if rng.random() >= P.MAKEUP_TAKE:
            unbooked.append(p)
            continue
        h = host_of[p["school"]]
        day = P.MAKEUP_DAYS[int(rng.integers(len(P.MAKEUP_DAYS)))]
        attended = bool(rng.random() >= P.NOSHOW_RATE)
        roster.append(dict(host=h, day=day, entry=p["entry"], surname=p["surname"], first=p["first"],
                           home=p["school"], attended=attended, script="", mark=None, walkin=False, theta=p["theta"]))
    walk = []
    for r in P.REGIONS:
        cand = [p for p in unbooked if region_of[p["school"]] == r]
        k = min(len(cand), int(rng.integers(P.WALKINS_PER_REGION[0], P.WALKINS_PER_REGION[1] + 1)))
        for j in sorted(rng.choice(len(cand), k, replace=False)):
            p = cand[int(j)]
            walk.append(dict(host=host_of[p["school"]], day=P.MAKEUP_DAYS[int(rng.integers(len(P.MAKEUP_DAYS)))],
                             entry=p["entry"], surname=p["surname"], first=p["first"], home=p["school"],
                             attended=True, script="", mark=None, walkin=True, theta=p["theta"]))
    for x in sorted(roster, key=lambda x: (x["host"], x["day"])) + sorted(walk, key=lambda x: (x["host"], x["day"])):
        if not x["attended"]:
            continue
        h = x["host"]
        counter[h] = counter.get(h, 0) + 1
        x["script"] = "%s-%03d" % (codes[h], counter[h])
        x["mark"] = int((rng.random(P.PAPER_LEN) < RA.sig(x["theta"] - w["pool"]["b_makeup"])).sum())
        sitters.append(x)
    pct_host, pct_day = hosts["Central"], P.MAKEUP_DAYS[1]
    for x in sitters:
        pct = x["host"] == pct_host and x["day"] == pct_day
        if pct:
            keyed, by = dt.date(2026, 9, 2), "JT"
        else:
            keyed = x["day"] + dt.timedelta(days=int(rng.integers(6, 12)))
            by = ["MK", "RP", "JT"][int(rng.integers(3))]
            if by == "JT" and keyed == dt.date(2026, 9, 2):
                by = "MK"      # JT spent 2 September on the one batch
        # the office keys the cover's entry number where it cannot match a script to the typed roster, and RP keys it
        # from every cover
        entry_keyed = x["entry"] if (x["walkin"] or by == "RP") else ""
        scripts.append(dict(script=x["script"], school=codes[x["host"]], entry=entry_keyed,
                            keyed_mark=x["mark"] * 2 if pct else x["mark"], mark=x["mark"], keyed=keyed, by=by,
                            pct=pct, home=x["home"], walkin=x["walkin"]))
    scripts.sort(key=lambda s: (s["keyed"], s["script"]))
    # the figures
    person_region = {}
    for e in entries:
        if e["status"] == "E":
            person_region.setdefault(e["person"], region_of[codes.index(e["school"])])
    entered = {r: sum(1 for v in person_region.values() if v == r) for r in P.REGIONS}
    sat = {r: sum(1 for p in online if region_of[p["school"]] == r) for r in P.REGIONS}
    mk = {r: [] for r in P.REGIONS}
    for x in scripts:
        sat[region_of[x["home"]]] += 1
        mk[region_of[x["home"]]].append(x["mark"])
    return dict(entries=entries, twins=twins, transfers=transfers, withdrawn=withdrawn, resend=resend,
                hosts=hosts, host_of=host_of, roster=roster, walkins=walk, scripts=scripts, entered=entered, sat=sat,
                makeup_mean={r: (sum(v) / len(v) if v else None) for r, v in mk.items()},
                makeup_n={r: len(v) for r, v in mk.items()})
