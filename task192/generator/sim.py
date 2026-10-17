"""The register's own world: the actions, the reports that record each of them on each access route,
the press classifier's reading of its own reports, and the coding desk's hand-coding rounds.

The action layer is drawn first, from its own stream, so its figures are the ones the design note
measured.
"""
import datetime as dt
import math
import random

import world as W

DAY0 = W.OPEN_DAY
NWIN = (W.PERIOD_TO - DAY0).days
XDAY = (W.EXTRACT - DAY0).days


def d(off):
    return DAY0 + dt.timedelta(days=int(off))


# ---------------------------------------------------------------- geography

def geography(rng):
    locs, muni = [], []
    n = 0
    for dist, ms in W.DISTRICTS.items():
        for m in ms:
            mcode = "%s%03d" % (dist[:2].upper(), len(muni) + 1)
            muni.append(dict(code=mcode, name=m, district=dist, region=W.REGION_OF[dist],
                             coastal=dist in W.COASTAL))
            k = rng.choice([3, 4, 4, 5, 5, 6])
            for p in rng.sample(W.LOC_PREFIX, k):
                n += 1
                locs.append(dict(code="L%05d" % n, name="%s (%s)" % (p, m), muni=mcode,
                                 district=dist, former=""))
    for loc in rng.sample(locs, W.RENAMES):
        loc["former"] = loc["name"].replace("Sao ", "S. ").replace("Santa ", "Sta. ")
        if loc["former"] == loc["name"]:
            loc["former"] = "Lugar de " + loc["name"]
    return muni, locs


# ---------------------------------------------------------------- the action layer

def actions(muni, locs):
    """Every action the register holds: one dispute theme at one locality on one calendar day, with
    the kind of action it was and whether the press classifier read it as a confrontation."""
    rng = random.Random(W.SEED)
    by_muni = {}
    for l in locs:
        by_muni.setdefault(l["muni"], []).append(l)
    themes = [(t, w) for t, _, w in W.THEMES]
    out, taken = [], set()
    for off in range(XDAY + 1):
        lam = W.ACTIONS_BASE * (W.ACTIONS_SURGE if d(off) >= W.SURGE_FROM else 1.0)
        limit, k, q = math.exp(-lam), 0, rng.random()
        while q > limit:
            k += 1
            q *= rng.random()
        for _ in range(k):
            m = rng.choice(muni)
            surge = d(off) >= W.SURGE_FROM
            theme = rng.choice(W.SURGE_THEMES) if (surge and rng.random() < 0.5) \
                else rng.choices([t for t, _ in themes], weights=[w for _, w in themes])[0]
            if theme == "PES" and not m["coastal"]:
                theme = "SMU"
            loc = rng.choice(by_muni[m["code"]])
            if (theme, loc["code"], off) in taken:
                continue
            taken.add((theme, loc["code"], off))
            weight = dict((t, w) for t, _, w in W.THEMES)[theme]
            conf = rng.random() < W.CONF_RATE * weight
            code = rng.choice(W.CONFRONTATIONAL) if conf else \
                rng.choices(W.ORDINARY, weights=[26, 18, 24, 12, 20])[0]
            # the press classifier reads its own report of the action
            if conf:
                seen = rng.random() < W.CLS_RECALL
            else:
                seen = rng.random() < W.CLS_FALSE_MARK
            cls_code = rng.choice(W.CONFRONTATIONAL) if seen else \
                rng.choices(W.ORDINARY, weights=[30, 20, 22, 10, 18])[0]
            out.append(dict(day=off, muni=m["code"], region=m["region"], district=m["district"],
                            theme=theme, loc=loc, conf=conf, code=code, cls_conf=seen,
                            cls_code=cls_code))
    out.sort(key=lambda a: (a["day"], a["loc"]["code"], a["theme"]))
    for i, a in enumerate(out, 1):
        a["ref"] = "A%06d" % i
    return out


def routes(acts, rng):
    """Which access routes recorded each action. An action no route recorded is not in the register,
    so every action keeps at least one."""
    for a in acts:
        got = []
        if rng.random() < W.P_PRESS:
            got.append("IMP")
        if rng.random() < W.P_PARTNER:
            got.append("PAR")
        if rng.random() < W.P_LINE:
            got.append("LIN")
        if not got:
            got.append("IMP")
        a["routes"] = got
        # the protocol keeps a filer's code where one exists, the classifier's otherwise
        a["pressed"] = "IMP" in got
        a["register_code"] = a["cls_code"] if a["pressed"] else a["code"]
    return acts


# ---------------------------------------------------------------- reports

def outlets_for(district):
    out = [o for o in W.OUTLETS if district in o[2] or "*" in o[2]]
    return out or [o for o in W.OUTLETS if "*" in o[2]]


def partner_for(region, rng):
    pool = [p for p in W.PARTNERS if p[2] == region]
    return rng.choice(pool) if pool else None


def reports(acts, rng):
    """One report per route per action, and for the press monitor the items behind its report."""
    rows, seq = [], {"IMP": 0, "PAR": 0, "LIN": 0}
    for a in acts:
        for route in a["routes"]:
            seq[route] += 1
            ident = "%s-2026-%06d" % (route, seq[route])
            start_h = rng.choices([8, 9, 10, 11, 14, 15, 16, 17, 18, 19],
                                  weights=[6, 9, 12, 10, 11, 12, 10, 9, 7, 4])[0]
            start_m = rng.choice([0, 5, 10, 15, 20, 30, 35, 40, 45, 50])
            lag = int(W.LAG_BASE[route] * (0.42 + 1.75 * rng.random() ** 1.7)) + 3
            src = "LIN"
            titles = []
            if route == "IMP":
                pool = [o for o in outlets_for(a["district"]) if o[0] != W.TWIN_FEED[1]]
                k = rng.choices([1, 2, 3], weights=[55, 32, 13])[0]
                w = [o[3] for o in pool]
                for _ in range(k):
                    o = rng.choices(pool, weights=w)[0]
                    if o[0] not in titles:
                        titles.append(o[0])
                if W.TWIN_FEED[0] in titles:
                    titles.append(W.TWIN_FEED[1])
                src = titles[0]
            elif route == "PAR":
                p = partner_for(a["region"], rng)
                src = p[0] if p else "P02"
                if src == W.MERGED[0] and d(a["day"]) >= dt.date(2026, 9, 8) and rng.random() < 0.5:
                    src = W.MERGED[1]
            rows.append(dict(route=route, src=src, titles=titles, action=a, ident=ident,
                             start_h=start_h, start_m=start_m, lag_min=lag,
                             code=a["cls_code"] if route == "IMP" else a["code"]))
    return rows


def double_coding(acts, reps, rng):
    """The coding desk's hand-coding rounds: a simple random sample of the press monitor's reports
    for the period, each one coded again by hand without the classifier's code in view."""
    press = [r for r in reps if r["route"] == "IMP"
             and W.PERIOD_FROM <= d(r["action"]["day"]) <= W.PERIOD_TO]
    press.sort(key=lambda r: r["ident"])
    rows = []
    taken = set()
    for round_day, size in W.SAMPLE_ROUNDS:
        pool = [r for r in press
                if d(r["action"]["day"]) < round_day and r["ident"] not in taken]
        pick = rng.sample(pool, min(size, len(pool)))
        for r in pick:
            taken.add(r["ident"])
            a = r["action"]
            coder = rng.choice(W.CODERS)
            # the round's date is the day the desk signed it off; the coders worked the batch in
            # the days before it, and never before the day after the action
            day = round_day - dt.timedelta(days=rng.randrange(0, 9))
            day = max(day, d(a["day"]) + dt.timedelta(days=1))
            rows.append(dict(report=r, round_day=round_day, coder=coder, coded_day=day,
                             machine=a["cls_code"], hand=a["code"]))
    rows.sort(key=lambda x: (x["round_day"], x["report"]["ident"]))
    return rows
