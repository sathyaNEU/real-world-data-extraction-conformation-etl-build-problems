"""The register's own world: the actions, the reports that record each of them on each access route,
the press classifier's reading of its own reports, and the coding desk's hand-coding rounds.

The action layer is drawn first, from its own stream, so its figures are the ones the design note
measured.
"""
import datetime as dt
import hashlib
import math
import random

import world as W

DAY0 = W.OPEN_DAY
NWIN = (W.PERIOD_TO - DAY0).days
XDAY = (W.EXTRACT - DAY0).days


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

def muni_weight(m):
    """How much of its district's contention a municipality carries: the district capital most, and
    a long tail of small ones. Fixed by the municipality's own code, so it does not move with a
    draw."""
    if m["name"] == m["district"]:
        return W.CAPITAL_SIZE
    h = int(hashlib.md5(m["code"].encode()).hexdigest()[:8], 16)
    return W.MUNI_SIZE[h % len(W.MUNI_SIZE)]


def ground(muni):
    """Each theme's weight over the municipalities: its district's standing contention, the
    municipality's own size and the territory the dispute falls on."""
    out = {}
    for theme in W.THEME_GROUND:
        w = []
        for m in muni:
            w.append(W.DISTRICT_INTENSITY[m["district"]] * muni_weight(m)
                     * W.THEME_GROUND[theme][W.DISTRICT_GROUP[m["district"]]])
        out[theme] = w
    return out


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
    where = ground(muni)
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
            surge = day >= W.SURGE_FROM
            theme = rng.choice(surge_pool) if (surge and rng.random() < 0.5) \
                else rng.choices([t for t, _ in pool], weights=[w for _, w in pool])[0]
            m = rng.choices(muni, weights=where[theme])[0]
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
    """The minute an action is reported to have started. A called action is called for the quarter
    hour and a spontaneous one is not, and either way the minute in the report is what somebody
    wrote down, so the quarter hour is the mode of a spread rather than a lattice with exceptions."""
    u = rng.random()
    if u < 0.44:
        return rng.choice([0, 15, 30, 45])
    if u < 0.66:
        return rng.choice([5, 10, 20, 25, 35, 40, 50, 55])
    if u < 0.88:
        anchor = rng.choice([0, 15, 30, 45])
        return (anchor + rng.choice([-4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7])) % 60
    return rng.randrange(0, 60)


def reports(acts, rng):
    """One report per route per action, and for the press monitor the items behind its report."""
    rows, seq = [], {"IMP": 0, "PAR": 0, "LIN": 0}
    for a in acts:
        for route in a["routes"]:
            seq[route] += 1
            ident = "%s-2026-%06d" % (route, seq[route])
            start_h = rng.choices(W.START_HOURS[route], weights=W.START_WEIGHTS[route])[0]
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

def desk_calendar(opened, close, rng):
    """The days the desk sat with a round's batch, from the day it opened the lot to the day it
    signed it off, and who sat on each of them. The association's holiday month thins the desk out
    rather than stopping it, and a long batch buys the odd catch-up Saturday."""
    out, day = [], opened
    while day <= close:
        if day.weekday() >= 5:
            worked = rng.random() < W.DESK_SATURDAY
        else:
            worked = rng.random() < W.DESK_WORKED[day.month]
        if worked:
            team = []
            for name, sits, pace, _style in W.CODERS:
                if rng.random() < sits * W.DESK_SIT:
                    load = rng.choices(W.CODER_PACE, weights=W.CODER_PACE_W)[0]
                    team.append((name, max(1, int(round(load * pace)))))
            if team:
                out.append((day, team))
        day += dt.timedelta(days=1)
    return out


def neighbour_of(code, rng):
    """A coder reading an ambiguous report as another code of the same kind, the near codes of the
    protocol's own order before the far ones."""
    pos = dict((c, i) for i, (c, _, _) in enumerate(W.ACTION_CODES))
    same = W.CONFRONTATIONAL if code in W.CONFRONTATIONAL else W.ORDINARY
    others = [c for c in same if c != code]
    w = [W.CLS_DECAY ** (-abs(pos[c] - pos[code])) for c in others]
    return rng.choices(others, weights=w)[0]


NOTE_SEEN = ["titulo pouco claro", "duas pecas do mesmo dia", "local confirmado pelo gazeteiro",
             "relato sem hora da acao", "peca de agencia, sem detalhe de terreno",
             "a fotografia nao confirma o titulo", "numeros do relato muito acima dos da peca",
             "duvida entre dois codigos vizinhos", "relato encaminhado pela chefe de mesa"]
NOTE_DONE = ["codificado pelo corpo do texto", "codigo corrigido depois de ler a peca toda",
             "mantido o codigo do primeiro codificador", "confirmado com a segunda leitura",
             "prevaleceu a leitura do corpo da peca", "codigo mantido, nota para a proxima ronda"]
NOTE_NONE = ["sem elementos para fixar o codigo", "texto insuficiente para distinguir a acao",
             "peca sem descricao do que se passou", "relato sem corpo de texto utilizavel"]


def note_for(changed, coded, rng):
    """What a coder wrote in the margin: on the rows a second coder read, and on the rows nobody
    could code."""
    if not coded:
        return "%s; fica sem codificacao manual" % rng.choice(NOTE_NONE)
    done = [n for n in NOTE_DONE if ("corrig" in n or "prevaleceu" in n or "corpo" in n)
            == bool(changed)]
    return "%s; %s" % (rng.choice(NOTE_SEEN), rng.choice(done or NOTE_DONE))


def double_coding(acts, reps):
    """The coding desk's hand-coding rounds, on the desk's own stream.

    Twice per reporting period the desk draws a batch at random from the monitor's accepted reports
    entered since the previous round's cut and dated up to its own, and codes each one by hand
    without the classifier's code in view. The batch is as big as the days the desk had: it opens
    the lot the day after the previous round closed and works it, a few coders at a time, until it
    signs the lot off. A coder reads an ambiguous report as a neighbouring code of the same kind
    more or less often than the next coder does, and a report a coder could not fix at all stays in
    the worksheet with no manual code.
    """
    rng = random.Random(W.SEED_DESK)
    press = [r for r in reps if r["route"] == "IMP"]
    press.sort(key=lambda r: r["ident"])
    style = dict((c, st) for c, _, _, st in W.CODERS)
    rows, taken, seq = [], set(), 0
    for name, close, cut_from, cut_to, opened in W.SAMPLE_ROUNDS:
        pool = [r for r in press if cut_from <= d(r["action"]["day"]) <= cut_to]
        cal = desk_calendar(opened, close, rng)
        for day, team in cal:
            for coder, load in team:
                here = [r for r in pool
                        if r["ident"] not in taken and d(r["action"]["day"]) < day]
                if not here:
                    continue
                for r in rng.sample(here, min(load, len(here))):
                    taken.add(r["ident"])
                    seq += 1
                    a = r["action"]
                    hand = a["code"]
                    if rng.random() < style[coder]:
                        hand = neighbour_of(hand, rng)
                    coded = rng.random() >= W.UNCODABLE
                    machine = a["cls_code"]
                    apart = coded and ((hand in W.CONFRONTATIONAL)
                                       != (machine in W.CONFRONTATIONAL))
                    second, decision, changed = "", "", False
                    if coded and rng.random() < (W.ADJ_DISAGREE if apart else W.ADJ_AGREE):
                        second = rng.choice([c for c, _, _, _ in W.CODERS if c != coder])
                        changed = rng.random() < (W.ADJ_CHANGED_DISAGREE if apart
                                                  else W.ADJ_CHANGED_AGREE)
                        decision = "alterado" if changed else "mantido"
                    note = ""
                    if not coded:
                        note = note_for(False, False, rng)
                    elif second and rng.random() < W.NOTE_REVIEWED:
                        note = note_for(changed, True, rng)
                    rows.append(dict(report=r, round_name=name, round_day=close, coder=coder,
                                     coded_day=day, machine=machine,
                                     hand=hand if coded else "", second=second,
                                     decision=decision, note=note, seq=seq))
    rows.sort(key=lambda x: (x["round_name"], x["coded_day"], x["coder"], x["seq"]))
    return rows
