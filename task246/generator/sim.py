"""task246 simulation: the round as it happened. Clusters, households and their members, the children aged 6 to 59
months and their own arm circumference, each team's daily schedule, every MUAC reading the anthropometrist on duty
took, and the two standardisation sessions. The standardisation readings are drawn from each anthropometrist's own
offset and errors, then the draw is searched so the test's estimates sit near the design (TEST_TARGET), the way a real
test comes out near the measurer's habits. Team B4's anthropometrist changed at the refresher; the zone's clusters are
dealt to the two halves of the round so that the halves' children are alike."""
import datetime as dt
import zlib

import numpy as np

import params as P


def crng(*key):
    """a generator keyed on the entity, so a child's draw does not depend on anything drawn before it"""
    s = zlib.crc32(("|".join(str(k) for k in key)).encode())
    return np.random.default_rng([P.SEED, s])


def workdays(a, b):
    d, out = a, []
    while d <= b:
        if d.weekday() != 6:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def heap(x, rng, share):
    r = np.round(x)
    if share > 0:
        h = rng.random(np.shape(x)) < share
        r = np.where(h, np.round(np.asarray(x) / 5.0) * 5.0, r)
    return r


def anthropometrist(team, day):
    """the team's anthropometrist on a fieldwork day"""
    if team == "B4" and day >= P.SUBSTITUTION:
        return "B4s"
    return team


class World:
    pass


def clusters(rng):
    """twenty enumeration areas a zone, each with its own level; a zone shared by two teams has its clusters dealt
    to the teams so that the two halves have the same average level"""
    out = []
    for zi, (z, name, sub, mu, sdc, sdcl) in enumerate(P.ZONES):
        eff = rng.normal(0, sdcl, P.CLUSTERS_PER_ZONE)
        eff = eff - eff.mean()
        order = np.argsort(eff)
        teams = P.ALLOCATION[z]
        owner = {}
        if len(teams) == 1:
            owner = {int(k): teams[0][0] for k in range(P.CLUSTERS_PER_ZONE)}
        else:
            pattern = [0, 1, 1, 0]
            for r, k in enumerate(order):
                owner[int(k)] = teams[pattern[r % 4]][0]
        for k in range(P.CLUSTERS_PER_ZONE):
            code = (zi + 1) * 100 + k + 1
            out.append(dict(zone=z, cluster=code, level=mu + P.ZONE_SHIFT.get(z, 0.0) + eff[k], team=owner[k], sub=sub,
                            ea=int(rng.integers(1000, 9999)) + zi * 10000))
    return out


def households(cl):
    """fifteen households a cluster. A household found absent is revisited before the team leaves the cluster; a
    dwelling found empty is not. Members on the day of the interview, and everyone who joined, was born, left or died
    in the recall period (whether a member was born in it is settled once the cluster's day is known)"""
    hh, members = [], []
    hid = 0
    pastoral = {z[0]: ("Pastoral" in z[1]) for z in P.ZONES}
    for c in cl:
        rng = crng("hh", c["cluster"])
        p_empty = 0.07 if pastoral[c["zone"]] else 0.025
        for j in range(P.HH_PER_CLUSTER):
            hid += 1
            u = rng.random()
            if u < p_empty:
                visits = ["empty"]
            elif u < p_empty + 0.012:
                visits = ["refused"]
            elif u < p_empty + 0.012 + 0.06:
                visits = ["absent", "completed" if rng.random() < 0.6 else "absent"]
            else:
                visits = ["completed"]
            h = dict(hh=hid, cluster=c["cluster"], zone=c["zone"], team=c["team"], number=j + 1, visits=visits,
                     outcome=visits[-1], sub=c["sub"])
            hh.append(h)
            if h["outcome"] != "completed":
                continue
            size = max(1, int(rng.poisson(7.6)))
            for k in range(size):
                r = rng.random()
                if r < 0.19:
                    age_m = rng.uniform(0, 60)
                elif r < 0.45:
                    age_m = rng.uniform(60, 180)
                elif r < 0.93:
                    age_m = rng.uniform(180, 600)
                else:
                    age_m = rng.uniform(600, 960)
                members.append(dict(hh=hid, line=k + 1, sex="F" if rng.random() < 0.51 else "M", age_m=age_m,
                                    status="present", joined=bool(rng.random() < 0.012), born=False,
                                    u_born=float(rng.random()), away=False))
            line = size
            for _ in range(int(rng.poisson(0.18))):
                line += 1
                members.append(dict(hh=hid, line=line, sex="F" if rng.random() < 0.5 else "M",
                                    age_m=rng.uniform(60, 600), status="left", joined=False, born=False, u_born=1.0,
                                    away=False))
            if rng.random() < 0.040:
                line += 1
                r = rng.random()
                if r < 0.13:
                    age_m, born = rng.uniform(0.1, 2.2), True          # a newborn of the recall period
                elif r < 0.36:
                    age_m, born = rng.uniform(3, 59), False
                else:
                    age_m, born = rng.uniform(60, 900), False
                sex = "F" if rng.random() < 0.5 else "M"
                if not born:
                    rng.random()                                     # the draw that once set where the death was
                where = crng("away", P.AWAY_SALT, hid, line).random()
                members.append(dict(hh=hid, line=line, sex=sex, age_m=age_m, status="died", joined=False, born=born,
                                    u_born=1.0, away=(not born) and bool(where < (0.6 if age_m < 60 else 0.3))))
            # children who left with their mother or to another caregiver (a mother often left with them); drawn on
            # their own generator so the members above do not move
            mv = crng("movers", P.MOVER_SALT, c["cluster"], j)
            for _ in range(int(mv.poisson(P.MOVE_EVENTS))):
                if mv.random() < 0.55:
                    line += 1
                    members.append(dict(hh=hid, line=line, sex="F", age_m=mv.uniform(216, 480), status="left",
                                        joined=False, born=False, u_born=1.0, away=False,
                                        why="household" if mv.random() < 0.6 else "work"))
                for _k in range(1 + int(mv.random() < 0.35)):
                    line += 1
                    age_m = mv.uniform(1, 60) if mv.random() < 0.75 else mv.uniform(60, 168)
                    members.append(dict(hh=hid, line=line, sex="F" if mv.random() < 0.5 else "M", age_m=age_m,
                                        status="left", joined=False, born=False, u_born=1.0, away=False,
                                        why="caregiver"))
    return hh, members


def children(cl, hh, members):
    """the children aged 6 to 59 months in each completed household, their own arm circumference, oedema and measles
    vaccination"""
    level = {c["cluster"]: c["level"] for c in cl}
    zsd = {z[0]: z[4] for z in P.ZONES}
    hinfo = {h["hh"]: h for h in hh}
    out = []
    cid = 0
    vac = {z: (0.50 + 0.03 * (i % 4), 0.24, 0.14 + 0.01 * (i % 3)) for i, z in enumerate(P.ZCODES)}
    for m in members:
        if m["status"] != "present" or not (6.0 <= m["age_m"] < 60.0):
            continue
        if crng("unmeasured", m["hh"], m["line"]).random() < 0.03:
            continue                       # on the roster, not measured: away with the mother, sick or refused
        h = hinfo[m["hh"]]
        cid += 1
        rng = crng("child", m["hh"], m["line"])
        girl = m["sex"] == "F"
        own = level[h["cluster"]] + P.AGE_SLOPE * (m["age_m"] - 33.0) + (P.GIRL if girl else 0.0) + rng.normal(0, zsd[h["zone"]])
        oed = bool(rng.random() < 0.0025)
        card, recall, novac = vac[h["zone"]]
        u = rng.random()
        if m["age_m"] < 9.0:
            measles = None
        elif u < card:
            measles = "card"
        elif u < card + recall:
            measles = "recall"
        elif u < card + recall + novac:
            measles = "no"
        else:
            measles = "dk"
        out.append(dict(child=cid, hh=m["hh"], line=m["line"], cluster=h["cluster"], zone=h["zone"], team=h["team"],
                        sex=m["sex"], age_m=m["age_m"], own=float(own), oedema=oed, measles=measles))
    return out


def schedule(cl, kids, rng):
    """each team works one cluster a day, Monday to Saturday. Team B4's zone is split between the anthropometrist
    who started the round and the one who took over at the refresher, the split chosen so the two halves' children
    have the same average arm circumference"""
    days = workdays(P.FIELD_START, P.FIELD_END)
    by_team = {}
    for c in cl:
        by_team.setdefault(c["team"], []).append(c)
    for t, cs in sorted(by_team.items()):
        n = len(cs)
        if t == "B4":
            before = [d for d in days if d < P.SUBSTITUTION]
            after = [d for d in days if d >= P.SUBSTITUTION]
            own = {c["cluster"]: [k["own"] for k in kids if k["cluster"] == c["cluster"]] for c in cs}
            best = None
            r2 = np.random.default_rng(P.SEED + 44)
            for _ in range(6000):
                pick = set(r2.choice(n, n // 2, replace=False).tolist())
                a = [x for i, c in enumerate(cs) if i in pick for x in own[c["cluster"]]]
                b = [x for i, c in enumerate(cs) if i not in pick for x in own[c["cluster"]]]
                gap = abs(np.mean(a) - np.mean(b)) + 0.02 * abs(len(a) - len(b))
                if best is None or gap < best[0]:
                    best = (gap, pick)
            first = [c for i, c in enumerate(cs) if i in best[1]]
            second = [c for i, c in enumerate(cs) if i not in best[1]]
            rng.shuffle(first)
            rng.shuffle(second)
            pick = sorted(rng.choice(len(before), len(first), replace=False))
            for c, d in zip(first, [before[i] for i in pick]):
                c["date"] = d
            for c, d in zip(second, after[:len(second)]):
                c["date"] = d
            continue
        pick = sorted(rng.choice(len(days), n, replace=False))
        dates = [days[i] for i in pick]
        order = list(cs)
        rng.shuffle(order)
        if len({c["zone"] for c in cs}) > 1:
            # a team shared between two zones alternates between them, so each zone is worked through the round
            za, zb = sorted({c["zone"] for c in cs}, key=P.ZCODES.index)
            a = [c for c in order if c["zone"] == za]
            b = [c for c in order if c["zone"] == zb]
            order = [x for pair in zip(a, b) for x in pair] + a[len(b):] + b[len(a):]
        for c, d in zip(order, dates):
            c["date"] = d
    return cl


def settle(cl, hh, members, kids):
    """the day each cluster was worked fixes its households' interview day, which members were born in the recall
    period, and which anthropometrist read each child"""
    date = {c["cluster"]: c["date"] for c in cl}
    hd = {}
    for h in hh:
        h["date"] = date[h["cluster"]]
        h["recall_days"] = (h["date"] - P.RECALL_START[h["sub"]][0]).days
        hd[h["hh"]] = h
    for m in members:
        if m["status"] == "present":
            m["born"] = bool(m["age_m"] * 30.4375 < hd[m["hh"]]["recall_days"] and m["u_born"] < 0.9)
            if m["born"]:
                m["joined"] = False
    for k in kids:
        k["date"] = date[k["cluster"]]
    return hh, members, kids


def readings(kids):
    """each child's MUAC as the anthropometrist on duty read it: the child's own arm, the anthropometrist's offset, its
    error on that child and a repeat error, then rounded (to 5 mm on the share of readings a heaping anthropometrist
    rounds). An anthropometrist's child-to-child errors in a zone are drawn free of the children's own arms and sum to
    nothing there, as a placement habit does not depend on the child's size and its fixed part is the offset"""
    draws = {}
    for k in kids:
        a = anthropometrist(k["team"], k["date"])
        _, _, _, b, si, sr, hp = P.MEASURERS[a]
        rng = crng("read", k["hh"], k["line"])
        draws[id(k)] = (a, rng.normal(0, si), rng.normal(0, sr), rng.random())
    groups = {}
    for k in kids:
        groups.setdefault((draws[id(k)][0], k["zone"]), []).append(k)
    for (a, z), ks in groups.items():
        own = np.array([k["own"] for k in ks])
        inter = np.array([draws[id(k)][1] for k in ks])
        _, _, _, b, si, sr, hp = P.MEASURERS[a]
        if len(ks) > 2:
            d = own - own.mean()
            inter = inter - inter.mean()
            inter = inter - d * (inter @ d) / (d @ d)
            inter = inter / inter.std(ddof=1) * si
        for k, e in zip(ks, inter):
            x = k["own"] + b + e + draws[id(k)][2]
            k["measurer"] = a
            k["muac"] = float(np.round(x / 5.0) * 5.0 if draws[id(k)][3] < hp else np.round(x))
    return kids


def test_session(rng, n=10):
    kid = rng.normal(138.0, 11.5, n)
    sup = np.array([np.round(kid + rng.normal(0, P.SUPERVISOR[1], n)) for _ in range(2)])
    return kid, sup


def measurer_readings(kid, a, seed):
    """two readings of each test child: the child, the measurer's offset, the measurer's own error on that child
    (the same on both readings) and a repeat error"""
    r = np.random.default_rng(seed)
    _, _, _, b, si, sr, hp = P.MEASURERS[a]
    inter = r.normal(0, si, len(kid))
    out = []
    for _ in range(2):
        e = r.normal(0, sr, len(kid))
        out.append(heap(kid + b + inter + e, r, hp))
    return np.array(out)


def test_estimates(reads, refs):
    d = np.concatenate([(x - ref).ravel() for x, ref in zip(reads, refs)])
    return float(d.mean()), float(d.var(ddof=1)), [float((x - ref).mean()) for x, ref in zip(reads, refs)]


def standardisation(rng):
    """two sessions of ten children; every anthropometrist on duty reads each child twice, as does the supervisor.
    Each anthropometrist's draw is searched so the pooled offset and error sit near the design and neither session's
    offset strays far from the pooled one"""
    sessions = {1: test_session(rng), 2: test_session(rng)}
    out = {}
    for a in P.MEASURERS:
        present = [s for s in (1, 2) if not (a == "B4s" and s == 1) and not (a == "B4" and s == 2)]
        tb, tf = P.TEST_TARGET[a]
        best = None
        for trial in range(4000):
            seed = (P.SEED * 1000003 + zlib.crc32(a.encode()) % 997 * 7919 + trial) % (2 ** 32)
            reads = [measurer_readings(sessions[s][0], a, seed + 31 * s) for s in present]
            refs = [sessions[s][1].mean(0) for s in present]
            b, fe, per = test_estimates(reads, refs)
            tol_f = 0.06 * tf
            ok = abs(b - tb) < 0.12 and abs(fe - tf) < tol_f and all(abs(p - b) < 0.6 for p in per)
            score = abs(b - tb) / 0.12 + abs(fe - tf) / tol_f + max(0.0, max(abs(p - b) for p in per) - 0.6)
            if best is None or score < best[0]:
                best = (score, seed, reads, b, fe, per)
            if ok:
                break
        out[a] = dict(sessions=present, reads=best[2], b=best[3], fe=best[4], per=best[5], seed=best[1])
    return sessions, out


def make():
    rng = np.random.default_rng(P.SEED)
    W = World()
    W.clusters = clusters(rng)
    W.households, W.members = households(W.clusters)
    kids = children(W.clusters, W.households, W.members)
    schedule(W.clusters, kids, rng)
    W.households, W.members, kids = settle(W.clusters, W.households, W.members, kids)
    W.children = readings(kids)
    W.sessions, W.test = standardisation(np.random.default_rng(P.SEED + 1))
    return W
