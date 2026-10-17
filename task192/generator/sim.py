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
START_HOURS = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
START_WEIGHTS = [2, 6, 9, 12, 10, 5, 4, 11, 12, 10, 9, 7, 5, 3, 2]


def d(off):
    return DAY0 + dt.timedelta(days=int(off))


def conf_rate(day):
    """The share of that day's actions that were confrontational."""
    if day <= W.CONF_RAMP_FROM:
        return W.CONF_RATE_HI
    if day >= W.CONF_RAMP_TO:
        return W.CONF_RATE_LO
    span = (W.CONF_RAMP_TO - W.CONF_RAMP_FROM).days
    f = (day - W.CONF_RAMP_FROM).days / float(span)
    return W.CONF_RATE_HI + (W.CONF_RATE_LO - W.CONF_RATE_HI) * f


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
    the kind of action it was and the code the press classifier put on its own report of it."""
    rng = random.Random(W.SEED)
    conf_matrix = W.confusion()
    by_muni = {}
    for l in locs:
        by_muni.setdefault(l["muni"], []).append(l)
    conf_weight = dict((t, cw) for t, _, _, cw, _ in W.THEMES)
    opens_on = dict((t, o) for t, _, _, _, o in W.THEMES)
    out, taken = [], set()
    for off in range(XDAY + 1):
        day = d(off)
        lam = W.ACTIONS_BASE * (W.ACTIONS_SURGE if day >= W.SURGE_FROM else 1.0) \
            * W.WEEKDAY_FACTOR[day.weekday()]
        limit, k, q = math.exp(-lam), 0, rng.random()
        while q > limit:
            k += 1
            q *= rng.random()
        pool = [(t, w) for t, _, w, _, o in W.THEMES if o is None or day >= o]
        surge_pool = [t for t in W.SURGE_THEMES if opens_on[t] is None or day >= opens_on[t]]
        for _ in range(k):
            m = rng.choice(muni)
            surge = day >= W.SURGE_FROM
            theme = rng.choice(surge_pool) if (surge and rng.random() < 0.5) \
                else rng.choices([t for t, _ in pool], weights=[w for _, w in pool])[0]
            if theme == "PES" and not m["coastal"]:
                theme = "SMU"
            loc = rng.choice(by_muni[m["code"]])
            if (theme, loc["code"], off) in taken:
                continue
            taken.add((theme, loc["code"], off))
            rate = min(0.62, conf_rate(day) * conf_weight[theme])
            conf = rng.random() < rate
            code = rng.choices(list(W.CONF_MIX), weights=list(W.CONF_MIX.values()))[0] if conf \
                else rng.choices(list(W.CODE_MIX), weights=list(W.CODE_MIX.values()))[0]
            # the press classifier reads its own report of the action and assigns a code
            codes, row = conf_matrix[code]
            cls_code = rng.choices(codes, weights=row)[0]
            out.append(dict(day=off, muni=m["code"], region=m["region"], district=m["district"],
                            theme=theme, loc=loc, conf=conf, code=code,
                            cls_conf=cls_code in W.CONFRONTATIONAL, cls_code=cls_code))
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


def start_minute(rng):
    """Action start times cluster on the quarter hour without being confined to it."""
    u = rng.random()
    if u < 0.52:
        return rng.choice([0, 15, 30, 45])
    if u < 0.78:
        return rng.choice([5, 10, 20, 25, 35, 40, 50, 55])
    return rng.randrange(0, 60)


def reports(acts, rng):
    """One report per route per action, and for the press monitor the items behind its report."""
    rows, seq = [], {"IMP": 0, "PAR": 0, "LIN": 0}
    for a in acts:
        for route in a["routes"]:
            seq[route] += 1
            ident = "%s-2026-%06d" % (route, seq[route])
            start_h = rng.choices(START_HOURS, weights=START_WEIGHTS)[0]
            start_m = start_minute(rng)
            lag = int(W.LAG_BASE[route] * math.exp(W.LAG_SIGMA[route] * rng.gauss(0, 1))) + 4
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
                if src == W.MERGED[0] and d(a["day"]) >= W.MERGED[2] and rng.random() < 0.5:
                    src = W.MERGED[1]
            rows.append(dict(route=route, src=src, titles=titles, action=a, ident=ident,
                             start_h=start_h, start_m=start_m, lag_min=lag,
                             code=a["cls_code"] if route == "IMP" else a["code"]))
    return rows


# ---------------------------------------------------------------- the coding desk

def desk_calendar(close, rng, span=34):
    """The working days the desk had before a round closed, with the lumpy daily load a small desk
    actually turns in: some days nothing, some days a long shift."""
    days = []
    for back in range(span, 0, -1):
        day = close - dt.timedelta(days=back)
        if day.weekday() >= 5:
            if rng.random() < 0.12:                 # the occasional catch-up Saturday
                days.append((day, rng.choice([0.4, 0.6])))
            continue
        days.append((day, rng.choices([0.0, 0.45, 0.8, 1.0, 1.35, 1.7],
                                      weights=[14, 16, 22, 20, 17, 11])[0]))
    days = [(day, w) for day, w in days if w > 0]
    return days


def double_coding(acts, reps, rng):
    """The coding desk's hand-coding rounds. Twice per reporting period the desk draws a batch at
    random from the monitor's accepted reports that arrived since the previous round closed, and
    codes each one by hand without the classifier's code in view."""
    press = [r for r in reps if r["route"] == "IMP"]
    press.sort(key=lambda r: r["ident"])
    rows, taken = [], set()
    coder_names = [c for c, _ in W.CODERS]
    coder_share = [s for _, s in W.CODERS]
    notes = ["titulo pouco claro, codificado pelo corpo do texto",
             "duas pecas do mesmo dia, uma acao",
             "local confirmado pelo gazeteiro",
             "relato sem hora, hora do registo",
             "peca de agencia, sem detalhe de terreno",
             "fotografia nao confirma o que o titulo diz",
             "codigo alterado depois de rever o texto completo"]
    for name, close, fa, fb, size in W.SAMPLE_ROUNDS:
        pool = [r for r in press if fa <= d(r["action"]["day"]) <= fb and r["ident"] not in taken]
        pick = rng.sample(pool, min(size, len(pool)))
        pick.sort(key=lambda r: (r["action"]["day"], r["ident"]))
        cal = desk_calendar(close, rng)
        weight = sum(w for _, w in cal)
        # the batch is spread over the desk's own days, and each day has its coder on the rota
        plan = []
        for i, (day, w) in enumerate(cal):
            n = int(round(len(pick) * w / weight))
            plan.append([day, n])
        short = len(pick) - sum(n for _, n in plan)
        for i in range(abs(short)):
            plan[i % len(plan)][1] += 1 if short > 0 else -1
        rota = []
        for i, (day, _) in enumerate(cal):
            rota.append(rng.choices(coder_names, weights=coder_share)[0])
        pos = 0
        for (day, n), coder in zip(plan, rota):
            room = max(0, n)
            while room and pos < len(pick):
                r = pick[pos]
                a = r["action"]
                if d(a["day"]) >= day:          # the desk cannot code a report before it arrives
                    break
                pos += 1
                room -= 1
                taken.add(r["ident"])
                coded = day
                second, decision = "", ""
                if rng.random() < W.ADJUDICATED:
                    other = [c for c in coder_names if c != coder]
                    second = rng.choice(other)
                    decision = rng.choices(["mantido", "alterado"], weights=[78, 22])[0]
                note = rng.choice(notes) if rng.random() < 0.045 else ""
                rows.append(dict(report=r, round_name=name, round_day=close, coder=coder,
                                 coded_day=coded, machine=a["cls_code"], hand=a["code"],
                                 second=second, decision=decision, note=note))
        last = cal[-1][0] if cal else close - dt.timedelta(days=1)
        while pos < len(pick):                   # whatever is left is cleared on the last day
            r = pick[pos]
            pos += 1
            a = r["action"]
            taken.add(r["ident"])
            coder = rng.choices(coder_names, weights=coder_share)[0]
            second, decision = "", ""
            if rng.random() < W.ADJUDICATED:
                second = rng.choice([c for c in coder_names if c != coder])
                decision = rng.choices(["mantido", "alterado"], weights=[78, 22])[0]
            note = rng.choice(notes) if rng.random() < 0.045 else ""
            rows.append(dict(report=r, round_name=name, round_day=close, coder=coder,
                             coded_day=max(last, d(a["day"]) + dt.timedelta(days=1)),
                             machine=a["cls_code"], hand=a["code"], second=second,
                             decision=decision, note=note))
    rows.sort(key=lambda x: (x["round_name"], x["coded_day"], x["report"]["ident"]))
    return rows
