"""The register's own world: dispute episodes, the actions inside them, and the reports that record
each action on each access route.

The episode layer is drawn first, from its own stream, so its figures are the ones the design note
measured: 635 episodes opened in the reporting period, 89 with a confrontational action recorded by
the extract, 312 closed quietly, 234 still open.
"""
import datetime as dt
import math
import random
import unicodedata

import world as W

DAY0 = W.OPEN_DAY
NWIN = (W.PERIOD_TO - DAY0).days            # last day an episode may open, as an offset
XDAY = (W.EXTRACT - DAY0).days              # the extract, as an offset


def d(off):
    return DAY0 + dt.timedelta(days=int(off))


def ascii_fold(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


# ---------------------------------------------------------------- the episode layer

def _h1(t, em):
    if t < 2 or t > W.H1TMAX:
        return 0.0
    x = (t - 2) / W.H1PEAK
    return W.H1MAX * em * x * math.exp(1 - x)


def _phase(t):
    return 0 if t <= 10 else (1 if t <= 30 else 2)


def episodes():
    """Every episode the register opens in the reporting period: opening day, class, fate and the day
    the fate falls on. fate 1 is a first confrontational action, fate 2 a quiet close."""
    rng = random.Random(W.SEED)
    opens = []
    for off in range(NWIN + 1):
        lam = W.OPEN_BASE * (W.OPEN_SURGE if d(off) >= W.SURGE_FROM else 1.0)
        limit, k, q = math.exp(-lam), 0, rng.random()
        while q > limit:
            k += 1
            q *= rng.random()
        opens.extend([off] * k)
    names = list(W.CLASSES)
    out = []
    for off in opens:
        u, acc, cls = rng.random(), 0.0, names[-1]
        for n in names:
            acc += W.CLASSES[n]["w"]
            if u < acc:
                cls = n
                break
        c = W.CLASSES[cls]
        fate, T = None, None
        for t in range(1, 400):
            a1, a2 = _h1(t, c["em"]), c["h2"][_phase(t)]
            u = rng.random()
            if u < a1:
                fate, T = 1, t
                break
            if u < a1 + a2:
                fate, T = 2, t
                break
        if fate is None:
            fate, T = 2, 400
        out.append(dict(open=off, cls=cls, fate=fate, T=T))
    return out


def observed(ep):
    """(time, cause) as the record at the extract shows the episode. cause 1 a confrontational
    action, 2 closed with none, 0 still open."""
    age = XDAY - ep["open"]
    if ep["fate"] == 1 and ep["T"] <= age:
        return ep["T"], 1
    if ep["fate"] == 2 and ep["T"] + W.QUIET_DAYS <= age:
        return ep["T"], 2
    return age, 0


# ---------------------------------------------------------------- geography

def geography(rng):
    """Settlements with their municipality, district and region, plus the 2024 renames kept on file."""
    locs, muni = [], []
    n = 0
    for dist, ms in W.DISTRICTS.items():
        for m in ms:
            mcode = "%s%03d" % (ascii_fold(dist)[:2].upper(), len(muni) + 1)
            muni.append(dict(code=mcode, name=m, district=dist, region=W.REGION_OF[dist],
                             coastal=dist in W.COASTAL))
            k = rng.choice([3, 4, 4, 5, 5, 6])
            picks = rng.sample(W.LOC_PREFIX, k)
            for p in picks:
                n += 1
                locs.append(dict(code="L%05d" % n, name="%s (%s)" % (p, m), muni=mcode,
                                 district=dist, former=""))
    for loc in rng.sample(locs, W.RENAMES):
        loc["former"] = loc["name"].replace("Sao ", "S. ").replace("Santa ", "Sta. ")
        if loc["former"] == loc["name"]:
            loc["former"] = "Lugar de " + loc["name"]
    return muni, locs


# ---------------------------------------------------------------- assignment, actions, reports

GAP_MEAN = {"flare": 2.6, "campaign": 4.2, "standing": 8.5}


def plan(eps, rng):
    """Draw every episode's action days before the municipalities are handed out, so the peace
    interval between two episodes of one municipality and theme is measured on the real last day."""
    for ep in sorted(eps, key=lambda e: (e["open"], e["T"], e["cls"])):
        days, conf = act_days(ep, rng)
        ep["days"] = [o for o in days if ep["open"] + o <= XDAY]
        ep["conf_day"] = conf if (conf is not None and ep["open"] + conf <= XDAY) else None
        ep["last_seen"] = ep["open"] + max(ep["days"])
    return eps


def assign(eps, muni, rng):
    """Give every episode a municipality and a dispute theme, so that no two episodes of one
    municipality and theme are close enough in time for the protocol's peace interval to join them."""
    last = {}
    by_code = {m["code"]: m for m in muni}
    themes = [t for t, _ in W.THEMES]
    for ep in sorted(eps, key=lambda e: e["open"]):
        surge = d(ep["open"]) >= W.SURGE_FROM
        chosen = None
        for _ in range(400):
            m = rng.choice(muni)
            theme = rng.choice(W.SURGE_THEMES) if (surge and rng.random() < 0.55) \
                else rng.choice(themes)
            if theme == "PES" and not m["coastal"]:
                continue
            prev = last.get((m["code"], theme))
            if prev is not None and ep["open"] - prev <= W.QUIET_DAYS + 1:
                continue
            chosen = (m, theme)
            break
        if chosen is None:                       # fall back to the first slot the interval allows
            for m in muni:
                for theme in themes:
                    if theme == "PES" and not m["coastal"]:
                        continue
                    prev = last.get((m["code"], theme))
                    if prev is None or ep["open"] - prev > W.QUIET_DAYS + 1:
                        chosen = (m, theme)
                        break
                if chosen:
                    break
        m, theme = chosen
        ep["muni"], ep["theme"] = m["code"], theme
        ep["region"], ep["district"] = m["region"], m["district"]
        last[(m["code"], theme)] = ep["last_seen"]
    return eps


def act_days(ep, rng):
    """The days the episode acts on, as offsets from its opening day, and which of them is the first
    confrontational action. The last day is the day the fate falls on, so the register reproduces the
    episode layer exactly."""
    mean = GAP_MEAN[ep["cls"]]
    horizon = XDAY - ep["open"] + 30            # a month past the extract, then the rest is unseen
    stop = min(ep["T"], horizon)
    days = [0]
    while True:
        g = min(20, 1 + int(rng.expovariate(1.0 / mean)))
        nxt = days[-1] + g
        if nxt >= stop:
            break
        days.append(nxt)
    if stop > 0:
        days.append(stop)
    conf = ep["T"] if ep["fate"] == 1 else None
    if ep["fate"] == 1:                         # the episode goes on past the confrontation
        t = stop
        while True:
            g = min(20, 1 + int(rng.expovariate(1.0 / mean)))
            t += g
            if t > horizon or rng.random() < 0.22:
                break
            days.append(t)
    return sorted(set(days)), conf


def actions(eps, locs, rng):
    """One row per action: the protocol's grain, one theme at one locality on one calendar day."""
    by_muni = {}
    for l in locs:
        by_muni.setdefault(l["muni"], []).append(l)
    out = []
    for ep in sorted(eps, key=lambda e: (e["open"], e["muni"], e["theme"])):
        pool = by_muni[ep["muni"]]
        home = rng.choice(pool)
        days, conf = ep["days"], ep["conf_day"]
        for off in days:
            loc = home if rng.random() < 0.72 else rng.choice(pool)
            if off == conf:
                code = rng.choice(W.CONFRONTATIONAL)
            elif conf is not None and off > conf and rng.random() < 0.18:
                code = rng.choice(W.CONFRONTATIONAL)
            else:
                code = rng.choices(W.ORDINARY, weights=[26, 18, 24, 12, 20])[0]
            out.append(dict(ep=ep, day=ep["open"] + off, loc=loc, code=code, theme=ep["theme"],
                            muni=ep["muni"], region=ep["region"], district=ep["district"]))
    out.sort(key=lambda a: (a["day"], a["loc"]["code"], a["theme"]))
    for i, a in enumerate(out, 1):
        a["ref"] = "A%06d" % i
    return out


def outlets_for(district):
    out = [o for o in W.OUTLETS if district in o[3] or "*" in o[3]]
    return out or [o for o in W.OUTLETS if "*" in o[3]]


def partner_for(region, rng):
    pool = [p for p in W.PARTNERS if p[2] == region]
    return rng.choice(pool) if pool else None


def reports(acts, rng):
    """Every report of every action, on each access route. Each action is reported at least once, so
    the register's action set is the world's action set."""
    rows = []
    seq = {"IMP": 0, "PAR": 0, "LIN": 0}
    for a in acts:
        got = []
        pool = outlets_for(a["district"])
        # the press monitor: one to three titles, with the Atlantic group's two language editions
        if rng.random() < 0.78:
            k = rng.choices([1, 2, 3], weights=[58, 31, 11])[0]
            pick = [o for o in pool if o[0] != W.TWIN_FEED[1]]   # the second edition never stands alone
            w = [o[4] for o in pick]
            titles = []
            for _ in range(k):
                o = rng.choices(pick, weights=w)[0]
                if o[0] not in titles:
                    titles.append(o[0])
            if W.TWIN_FEED[0] in titles and W.TWIN_FEED[1] not in titles:
                titles.append(W.TWIN_FEED[1])
            for t in titles:
                got.append(("IMP", t))
        # the partner network, inside its own region
        p = partner_for(a["region"], rng)
        if p and rng.random() < 0.46:
            code = p[0]
            if p[0] == W.MERGED[0] and d(a["day"]) >= dt.date(2026, 9, 8) and rng.random() < 0.5:
                code = W.MERGED[1]
            got.append(("PAR", code))
        # the public line
        if rng.random() < 0.3:
            got.append(("LIN", "LIN"))
        if not got:
            got.append(("IMP", rng.choice([o for o in pool if o[0] != W.TWIN_FEED[1]])[0]))
        for route, src in got:
            seq[route] += 1
            start_h = rng.choices([8, 9, 10, 11, 14, 15, 16, 17, 18, 19],
                                  weights=[6, 9, 12, 10, 11, 12, 10, 9, 7, 4])[0]
            start_m = rng.choice([0, 5, 10, 15, 20, 30, 35, 40, 45, 50])
            base = W.LAG_BASE[route]
            lag = int(base * (0.42 + 1.75 * rng.random() ** 1.7)) + 3
            rows.append(dict(route=route, src=src, action=a,
                             ident="%s-2026-%06d" % (route, seq[route]),
                             start_h=start_h, start_m=start_m, lag_min=lag))
    return rows
