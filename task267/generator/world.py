"""The clean truth of the 2026 season: venues and events, the adults screened (with whether each has undiagnosed
diabetes, which no file states), their screening values, the tablet's referrals and evaluation draw, the OGTTs that
followed, the analysers' runs and the laboratory's billing. Each part draws on its own random stream so a change to
an ask's records moves nothing the call reads."""
import datetime as dt

import numpy as np

import common as K

SEED = 285

# the season's process (the draw's simulation, kept)
P = dict(b0=-8.4, kb=0.085, lat=1.0, shape=1.6, s0=0.6, s1=0.06, dm_base=5.6, a_sev=0.55, g_sev=34, nd_mean=5.42,
         nd_sd=0.33, keep_rule=0.83, keep_eval=0.81, incomplete=0.03, repeat_share=0.026)

HOLIDAYS = {dt.date(2026, 5, 25), dt.date(2026, 7, 3), dt.date(2026, 9, 7), dt.date(2026, 11, 11)}
VENUE_TYPES = [("church", 0.38, (70, 175)), ("workplace", 0.20, (45, 130)), ("community centre", 0.18, (60, 160)),
               ("library", 0.08, (35, 90)), ("grocery store", 0.11, (50, 120)), ("county fair", 0.05, (260, 520))]


def streams(seed):
    ss = np.random.SeedSequence(seed)
    names = ["venues", "events", "adults", "measures", "referral", "ogtt", "typing", "analysers", "billing", "misc"]
    return {n: np.random.default_rng(s) for n, s in zip(names, ss.spawn(len(names)))}


def season_days():
    d, out = K.SEASON_START, []
    while d <= K.SEASON_END:
        if d.weekday() < 6 and d not in HOLIDAYS:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


VENUE_SYL = ["Grace", "Hope", "Calvary", "Trinity", "Bethel", "Zion", "New Life", "First Baptist", "St. Anne's",
             "St. Luke's", "Emmanuel", "Riverside", "Hillcrest", "Oak Street", "Maple Avenue", "Union", "Pine Ridge",
             "Lakeview", "Cedar", "Westgate", "Elm Park", "Harbor", "Mill Road", "Station Street", "Market Square"]
WORKPLACES = ["County Highway Department", "Regional Distribution Center", "Municipal Water Works", "School District "
              "Office", "Plastics Plant", "Food Processing Plant", "Bus Depot", "Hospital Facilities Building",
              "Sheriff's Office", "Credit Union Operations", "Warehouse Park", "Packaging Plant", "Call Center",
              "Public Works Yard", "Furniture Factory"]


def venues(R):
    rng = R["venues"]
    out = []
    for a, area in enumerate(K.AREAS):
        n = int(round(150 * K.AREA_W[a])) + 1
        for i in range(n):
            u = rng.random()
            acc = 0
            for vt, w, size in VENUE_TYPES:
                acc += w
                if u < acc:
                    break
            if vt == "church":
                name = "%s %s" % (VENUE_SYL[int(rng.integers(len(VENUE_SYL)))],
                                  ["Church", "Baptist Church", "Methodist Church", "Community Church", "AME Church"][
                                      int(rng.integers(5))])
            elif vt == "workplace":
                name = "%s %s" % (area, WORKPLACES[int(rng.integers(len(WORKPLACES)))])
            elif vt == "community centre":
                name = "%s Community Center" % ["North", "South", "East", "West", "Central", "Riverside", "Hilltop"][
                    int(rng.integers(7))]
            elif vt == "library":
                name = "%s Public Library" % area if rng.random() < .6 else "%s Branch Library" % ["North", "South",
                                                                                                   "East", "West"][
                    int(rng.integers(4))]
            elif vt == "grocery store":
                name = "%s Market" % ["Fresh Way", "Hometown", "Valley", "Corner", "Family Foods", "Save More"][
                    int(rng.integers(6))]
            else:
                name = "%s County Fairgrounds" % area
            out.append(dict(vid="V%03d" % (len(out) + 1), area=area, vtype=vt, name=name, size=size))
    # names are unique within an area
    seen = {}
    for v in out:
        k = (v["area"], v["name"])
        seen[k] = seen.get(k, 0) + 1
        if seen[k] > 1:
            v["name"] += " (%s)" % ["Annex", "Hall B", "Site 2", "East Lot"][min(seen[k] - 2, 3)]
    return out


def events(R, V):
    rng = R["events"]
    days = season_days()
    out = []
    fairs = [v for v in V if v["vtype"] == "county fair"]
    other = [v for v in V if v["vtype"] != "county fair"]
    w = np.array([K.AREA_W[K.AREAS.index(v["area"])] for v in other])
    w = w / w.sum()
    for d in days:
        k = 1 if rng.random() < 0.55 else 2
        if d.weekday() == 5:
            k = 2 if rng.random() < 0.6 else 1
        for _ in range(k):
            v = other[int(rng.choice(len(other), p=w))]
            out.append((d, v))
    # county fairs: a three-day run in late July or August per area with a fair ground
    for f in fairs:
        start = dt.date(2026, 7, 20) + dt.timedelta(days=int(rng.integers(0, 30)))
        for j in range(3):
            d = start + dt.timedelta(days=j)
            if d.weekday() == 6 or d in HOLIDAYS:
                d += dt.timedelta(days=1)
            out.append((d, f))
    out.sort(key=lambda x: (x[0], x[1]["vid"]))
    E = []
    for i, (d, v) in enumerate(out):
        lo, hi = v["size"]
        n = int(rng.integers(lo, hi + 1))
        start_h = 8 if v["vtype"] in ("workplace", "county fair") else (9 if d.weekday() < 5 else 10)
        hours = 6 if v["vtype"] != "county fair" else 9
        E.append(dict(eid="EV26-%04d" % (i + 1), date=d, vid=v["vid"], area=v["area"], vtype=v["vtype"],
                      venue=v["name"], n=n, start_h=start_h, hours=hours,
                      tablets=2 if n < 90 else (3 if n < 200 else 4)))
    return E


def adults(R, E):
    """Every encounter of the season: first screenings carry new adults; a share of adults return at a later event."""
    rng = R["adults"]
    rm = R["measures"]
    first = []
    for e in E:
        for j in range(e["n"]):
            first.append(e)
    N = len(first)
    age = np.clip(rng.normal(48, 14, N), 18, 88)
    male = rng.random(N) < 0.45
    bmi = np.clip(rng.lognormal(np.log(28.5), 0.18, N), 17, 60)
    fam = rng.random(N) < 0.30
    htn = rng.random(N) < np.clip(0.10 + 0.008 * (age - 40), 0.04, 0.7)
    inactive = rng.random(N) < 0.40
    gdm = (~male) & (rng.random(N) < 0.06)
    score = (np.where(age < 40, 0, np.where(age < 50, 1, np.where(age < 60, 2, 3))) + male + fam + htn + inactive + gdm
             + np.where(bmi < 25, 0, np.where(bmi < 30, 1, np.where(bmi < 40, 2, 3))))
    score = np.minimum(score, 10)
    lat = rng.normal(0, 1, N)
    lp = P["b0"] + 0.042 * age + P["kb"] * bmi + 0.5 * fam + 0.3 * htn + 0.2 * male + 0.9 * gdm + P["lat"] * lat
    dm = rng.random(N) < 1 / (1 + np.exp(-lp))
    sev = np.where(dm, rng.gamma(P["shape"], 0.5, N) * (P["s0"] + P["s1"] * score), 0)
    a1c = np.where(dm, P["dm_base"] + P["a_sev"] * sev + rm.normal(0, 0.26, N),
                   P["nd_mean"] + 0.006 * (age - 48) + 0.009 * (bmi - 28.5) + 0.05 * lat.clip(-2, 2)
                   + rm.normal(0, P["nd_sd"], N))
    a1c = np.clip(np.round(a1c, 1), 4.2, 13.9)
    glu = np.where(dm, 110 + P["g_sev"] * sev + rm.normal(0, 24, N), 98 + rm.normal(0, 17, N) + 0.25 * (bmi - 28.5))
    glu = np.clip(np.round(glu), 62, 398).astype(int)
    A = []
    for i in range(N):
        A.append(dict(i=i, event=first[i], age=int(age[i]), sex="M" if male[i] else "F", score=int(score[i]),
                      dm=bool(dm[i]), sev=float(sev[i]), a1c=float(a1c[i]), glu=int(glu[i]), bmi=float(bmi[i])))
    return A


def program_ids(R, A):
    rng = R["adults"]
    base = 100001
    order = list(range(len(A)))
    for k, i in enumerate(order):
        A[i]["pid"] = "SF-%07d" % (base + k)
    return A


def encounters(R, E, A):
    """The tablets' encounters: each adult's first screening, then the returns. A return carries the adult's
    program ID, fresh fingerstick values and no referral."""
    rng = R["adults"]
    rm = R["measures"]
    ev_by_date = {}
    for e in E:
        ev_by_date.setdefault(e["date"], []).append(e)
    later = sorted(ev_by_date)
    enc = []
    for a in A:
        enc.append(dict(a=a, event=a["event"], visit=1))
    n_rep = int(round(P["repeat_share"] * len(A)))
    cand = [a for a in A if a["event"]["date"] <= dt.date(2026, 10, 15)]
    pick = rng.choice(len(cand), size=n_rep, replace=False)
    for j in sorted(int(x) for x in pick):
        a = cand[j]
        gap = int(rng.integers(21, 140))
        d0 = a["event"]["date"] + dt.timedelta(days=gap)
        ds = [d for d in later if d >= d0]
        if not ds:
            continue
        same_area = [e for e in ev_by_date[ds[0]] if e["area"] == a["event"]["area"]]
        e = (same_area or ev_by_date[ds[0]])[0]
        enc.append(dict(a=a, event=e, visit=2, glu=int(np.clip(round(a["glu"] + rm.normal(0, 14)), 62, 398)),
                        a1c=float(np.clip(round(a["a1c"] + rm.choice([-0.1, 0.0, 0.0, 0.1]), 1), 4.2, 13.9))))
    # times inside each event, tablets round robin
    by_ev = {}
    for x in enc:
        by_ev.setdefault(x["event"]["eid"], []).append(x)
    out = []
    for e in E:
        xs = by_ev.get(e["eid"], [])
        rng.shuffle(xs)
        span = e["hours"] * 3600
        secs = np.sort(rng.integers(0, span, len(xs)))
        for k, (x, s) in enumerate(zip(xs, secs)):
            x["time"] = dt.datetime.combine(e["date"], dt.time(e["start_h"])) + dt.timedelta(seconds=int(s))
            x["tablet"] = "TB%02d" % (1 + (int(e["eid"][-4:]) * 3 + k % e["tablets"]) % 18)
            out.append(x)
    out.sort(key=lambda x: (x["time"], x["a"]["pid"]))
    for k, x in enumerate(out):
        x["enc"] = "E26-%06d" % (k + 1)
        if x["visit"] == 1:
            x["glu"], x["a1c"] = x["a"]["glu"], x["a"]["a1c"]
        x["score"] = x["a"]["score"]
    return out


def referrals(R, enc):
    """The tablet's 2026 referral at each adult's first screening: the 2026 rule, else the evaluation draw."""
    rng = R["referral"]
    for x in enc:
        if x["visit"] != 1:
            x["ref"] = "NONE"
            continue
        if x["score"] >= K.RULE_SCORE or x["glu"] >= K.RULE_GLUCOSE:
            x["ref"] = "RULE"
        else:
            x["ref"] = "EVAL" if rng.random() < K.EVAL_FRACTION else "NONE"
    return enc


def ogtt(R, enc):
    """The OGTTs that followed the referrals: kept or not, complete or not, and the two glucose values, consistent
    with each adult's diabetes."""
    rng = R["ogtt"]
    tests = []
    for x in enc:
        if x["ref"] == "NONE":
            continue
        keep = rng.random() < (P["keep_rule"] if x["ref"] == "RULE" else P["keep_eval"])
        lag = int(rng.integers(6, 36))
        d = x["time"].date() + dt.timedelta(days=lag)
        while d.weekday() == 6 or d in HOLIDAYS:
            d += dt.timedelta(days=1)
        if not keep or d > K.EXTRACT:
            continue
        a = x["a"]
        if a["dm"]:
            s = a["sev"]
            fpg = 112 + 22 * s + rng.normal(0, 13)
            two = 196 + 46 * s + rng.normal(0, 28)
            if fpg < 126 and two < 200:
                two = 200 + abs(rng.normal(0, 18))
        else:
            fpg = min(125, 94 + rng.normal(0, 9))
            two = min(199, 118 + rng.normal(0, 30))
        complete = rng.random() >= P["incomplete"]
        tests.append(dict(x=x, date=d, fpg=int(round(fpg)), two=int(round(two)) if complete else None,
                          complete=complete, psc=["PSC-%s" % c for c in ("OC1", "OC2", "FW", "DR", "PM", "QS")][
                              min(5, K.AREAS.index(x["event"]["area"]) + (1 if rng.random() < .3 and
                                                                           x["event"]["area"] == K.AREAS[0] else 0))]))
    tests.sort(key=lambda t: (t["date"], t["x"]["enc"]))
    for k, t in enumerate(tests):
        t["acc"] = "TL%08d" % (40213500 + k * 3 + int(rng.integers(0, 3)))
    return tests


def typed_ids(R, tests):
    """The program ID as the patient service centre typed it from the referral slip."""
    rng = R["typing"]
    for t in tests:
        pid = t["x"]["a"]["pid"]
        u = rng.random()
        if u < 0.80:
            t["typed"] = pid
        elif u < 0.88:
            t["typed"] = pid.replace("-", "")
        elif u < 0.93:
            t["typed"] = pid.lower()
        elif u < 0.97:
            t["typed"] = "SF-" + str(int(pid[3:]))
        else:
            t["typed"] = pid[3:]
    return tests


def build(seed=SEED):
    R = streams(seed)
    V = venues(R)
    E = events(R, V)
    A = adults(R, E)
    program_ids(R, A)
    enc = encounters(R, E, A)
    referrals(R, enc)
    tests = ogtt(R, enc)
    typed_ids(R, tests)
    return dict(R=R, V=V, E=E, A=A, enc=enc, tests=tests, seed=seed)


# ---------------------------------------------------------------------------------------------- the clean truth's rungs
def first_screenings(T):
    return [x for x in T["enc"] if x["visit"] == 1]


def truth_rungs(T):
    """Every rung on the clean truth (no file mess): sensitivity per cent by construction and the rule each picks."""
    F = first_screenings(T)
    tested = {t["x"]["enc"]: t for t in T["tests"] if t["complete"]}
    score = np.array([x["score"] for x in F])
    glu = np.array([x["glu"] for x in F])
    a1c = np.array([x["a1c"] for x in F])
    dm = np.array([x["a"]["dm"] for x in F])
    ref = np.array([x["ref"] for x in F])
    ver = np.array([x["enc"] in tested for x in F])
    out = {}
    w = np.zeros(len(F))
    for g in ("RULE", "NOTRULE"):
        m = (ref == "RULE") if g == "RULE" else (ref != "RULE")
        w[m & ver] = m.sum() / (m & ver).sum()
    for r in K.RULE_IDS:
        f = K.flags(r, score, glu, a1c)
        out[r] = dict(
            share=100 * f.mean(),
            true=100 * (f & dm).sum() / dm.sum(),
            cc=100 * (f & dm & ver).sum() / (dm & ver).sum(),
            golden=100 * (w * (f & dm & ver)).sum() / (w * (dm & ver)).sum())
    return out


def pick(res, key, target=K.TARGET):
    ok = [r for r in K.RULE_IDS if res[r][key] >= target]
    return min(ok, key=lambda r: res[r]["share"]) if ok else "2026 rule"
