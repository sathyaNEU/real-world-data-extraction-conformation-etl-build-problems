"""task243 simulator: an individual-level projection of the Province of Kalinawan's household population from mid 2014
to the civil registry extract of 31 March 2023, month by month. Deaths follow each LGU's mortality, births each LGU's
fertility; the oldest residents of the farming and remote municipalities move to their children's households, most of
them out of the province, at rates that follow their own mortality (to the late seventies), young adults move for work,
families move at a low rate at every age, and movers arrive from other provinces. The two censuses enumerate each LGU's
residents with a coverage uniform by age; the 2020 census records where each person lived on 1 May 2015. Returns the
persons, the death and birth events and the census snapshots; records.py turns them into the pack."""
import datetime as dt

import numpy as np

import params as P

EPOCH = dt.date(1900, 1, 1)
OUT = 12          # outside the province, in the Philippines
DEAD = -1


def days(d):
    return (d - EPOCH).days


def year_frac(dd):
    return dd / 365.2425


def month_starts():
    out, y, m = [], P.START.year, P.START.month
    while dt.date(y, m, 1) <= P.END:
        out.append(dt.date(y, m, 1))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def hazard(age, male, mort, when):
    """Annual death hazard: a Siler curve, the senescent part scaled by the LGU's level and by sex, improving 1.2 per
    cent a year from 2015, with COVID-19's excess from June 2020."""
    a = np.maximum(age, 0.0)
    infant = 0.024 * np.exp(-3.2 * a)
    young = 0.0009 + 0.0003 * male
    sen = 0.000050 * np.exp(0.0915 * a) * mort * (1.0 + 0.32 * male)
    yr = when.year + (when.month - 1) / 12.0
    trend = np.exp(-0.012 * (yr - 2015.0))
    covid = 1.0
    if dt.date(2020, 6, 1) <= when < dt.date(2021, 1, 1):
        covid = 1.12
    elif dt.date(2021, 1, 1) <= when < dt.date(2022, 1, 1):
        covid = 1.30
    elif dt.date(2022, 1, 1) <= when < dt.date(2022, 7, 1):
        covid = 1.10
    return (infant + young + sen * covid) * trend


def rogers_castro(age):
    return np.exp(-((age - 22.0) / 5.5) ** 2) * (age >= 15) * (age <= 36)


def asfr(age, tfr):
    """Age-specific fertility with a peak in the late twenties, summing to the TFR over 15 to 49."""
    s = np.exp(-((age - 28.0) / 6.8) ** 2) * (age >= 15) * (age < 50)
    return s * tfr / 12.05


def initial_population(rng):
    """Persons alive on the start date, LGU by LGU: cohorts born into a population whose growth has slowed from 3.1 to
    1.5 per cent a year, survived with mortality a third above today's, shaped by past labour moves (young adults
    gained by the city and the peri-urban LGUs, lost by the rest) and by past moves of the oldest."""
    ages = np.arange(0, 101) + 0.5
    rows = []
    for li, code in enumerate(P.CODES):
        kind = P.KIND[code]
        mort = P.MORT[code]
        cohort_year = 2014.5 - ages
        g = np.where(cohort_year < 1972, 0.029, 0.029 - (cohort_year - 1972) * (0.015 / 42.5))
        logb = -np.concatenate([[0.0], np.cumsum(g)[:-1]])
        births = np.exp(logb)
        for male in (0, 1):
            h = hazard(ages, male, mort * 1.33, dt.date(2015, 1, 1))
            surv = np.exp(-np.cumsum(h) + h / 2)
            n = births * surv * (1.04 if male else 1.0)
            bump = np.exp(-((ages - 30.0) / 12.0) ** 2)
            if kind in ("city", "periurban"):
                n = n * (1 + 0.10 * bump)
            else:
                n = n * (1 - 0.06 * bump)
            old = np.clip((ages - 55) / 30, 0, 1)
            if P.KAPPA_OUT[code] > 0:
                n = n * (1 - 0.05 * old)
            if kind == "periurban":
                n = n * (1 + 0.04 * old)
            rows.append((li, male, n))
    tot = {li: sum(r[2].sum() for r in rows if r[0] == li) for li in range(len(P.CODES))}
    out = []
    for li, male, n in rows:
        code = P.CODES[li]
        target = P.POP2020[code] / np.exp(0.0155 * 5.85)
        cnt = np.floor(n * target / tot[li] + rng.random(n.size)).astype(int)
        for a, k in enumerate(cnt):
            if k:
                out.append((li, male, a, k))
    lgu = np.concatenate([np.full(k, li, np.int16) for li, m, a, k in out])
    sex = np.concatenate([np.full(k, m, np.int8) for li, m, a, k in out])
    age0 = np.concatenate([np.full(k, a, np.float64) for li, m, a, k in out])
    age0 = age0 + rng.random(age0.size)
    birth = days(P.START) - age0 * 365.2425
    return lgu, sex, birth


class World:
    pass


def make():
    rng = np.random.default_rng(P.SEED)
    lgu, sex, birth = initial_population(rng)
    n = lgu.size
    cap = int(n * 1.45)

    W = World()
    W.lgu = np.full(cap, DEAD, np.int16)
    W.sex = np.zeros(cap, np.int8)
    W.birth = np.zeros(cap, np.float64)
    W.mother = np.full(cap, -1, np.int64)
    W.res2015 = np.full(cap, -2, np.int16)      # -2 not yet in the simulation on 1 May 2015, 13 another province
    W.arrived_from = np.full(cap, -1, np.int16)  # 13 another province (external in-mover), -1 born or initial
    W.lgu[:n], W.sex[:n], W.birth[:n] = lgu, sex, birth
    W.n = n
    W.deaths = []      # (person, date ordinal, lgu at death)
    W.births = []      # (child, mother, date ordinal, lgu)
    W.moves = []       # (person, date ordinal, from, to)
    W.census = {}
    mort = np.array([P.MORT[c] for c in P.CODES] + [1.0], np.float64)
    tfr = np.array([P.TFR[c] for c in P.CODES] + [2.6], np.float64)
    kappa = np.array([P.KAPPA_OUT[c] for c in P.CODES] + [0.0])
    labour = np.array([P.LABOUR[c] for c in P.CODES] + [0.0])
    pops = np.array([P.POP2020[c] for c in P.CODES], np.float64)

    def new_persons(k, li, sx, bdays, origin=-1, mother=-1):
        i0 = W.n
        W.lgu[i0:i0 + k] = li
        W.sex[i0:i0 + k] = sx
        W.birth[i0:i0 + k] = bdays
        W.arrived_from[i0:i0 + k] = origin
        W.mother[i0:i0 + k] = mother
        W.n += k
        return np.arange(i0, i0 + k)

    for ms in month_starts():
        dms = days(ms)
        nxt = dt.date(ms.year + (ms.month == 12), ms.month % 12 + 1, 1)
        span = days(nxt) - dms
        N = W.n
        alive = W.lgu[:N] != DEAD
        idx = np.nonzero(alive)[0]
        if ms == P.FIVE_YEARS_AGO:
            W.res2015[idx] = W.lgu[idx]
        if ms in (P.CENSUS1, P.CENSUS2):
            W.census[ms] = (idx.copy(), W.lgu[idx].copy(), W.sex[idx].copy(),
                            np.floor((dms - W.birth[idx]) / 365.2425).astype(int))
        age = (dms + span / 2 - W.birth[idx]) / 365.2425
        li = W.lgu[idx].astype(int)
        male = W.sex[idx].astype(float)
        # deaths
        h = hazard(age, male, mort[li], ms) / 12.0
        die = rng.random(idx.size) < 1 - np.exp(-h)
        dd = dms + np.floor(rng.random(die.sum()) * span)
        for p_, d_, l_ in zip(idx[die], dd.astype(int), li[die]):
            W.deaths.append((p_, d_, l_))
        W.lgu[idx[die]] = DEAD
        surv = ~die
        sidx, sage, sli, smale = idx[surv], age[surv], li[surv], male[surv]
        inprov = sli < OUT
        # the oldest residents' moves, at rates that follow their own mortality to the late seventies
        el = inprov & (kappa[sli] > 0) & (sage >= P.ELDER_MIN_AGE)
        hcap = hazard(np.minimum(sage[el], P.ELDER_CAP_AGE), smale[el], mort[sli[el]], ms)
        mv = rng.random(el.sum()) < kappa[sli[el]] * hcap / 12.0
        movers = sidx[el][mv]
        for p_ in movers:
            o = P.CODES[W.lgu[p_]]
            dests = list(P.ELDER_DEST[o].keys())
            pr = np.array(list(P.ELDER_DEST[o].values()))
            d_ = dests[rng.choice(len(dests), p=pr / pr.sum())]
            to = OUT if d_ == "OUT" else P.CODES.index(d_)
            W.moves.append((p_, dms + int(rng.random() * span), int(W.lgu[p_]), to))
            W.lgu[p_] = to
        # young adults' labour moves out of the farming, remote and town LGUs
        lab = inprov & (labour[sli] > 0) & (W.lgu[sidx] == sli)
        pr_l = P.LABOUR_PEAK * labour[sli[lab]] * rogers_castro(sage[lab]) / 12.0
        mvl = sidx[lab][rng.random(lab.sum()) < pr_l]
        dests = list(P.LABOUR_DEST.keys())
        prd = np.array(list(P.LABOUR_DEST.values()))
        for p_ in mvl:
            d_ = dests[rng.choice(len(dests), p=prd / prd.sum())]
            to = OUT if d_ == "OUT" else P.CODES.index(d_)
            W.moves.append((p_, dms + int(rng.random() * span), int(W.lgu[p_]), to))
            W.lgu[p_] = to
        # family moves between LGUs at every age
        bg = inprov & (W.lgu[sidx] == sli)
        mvb = sidx[bg][rng.random(bg.sum()) < P.BACKGROUND_MOVE / 12.0]
        w = pops / pops.sum()
        for p_ in mvb:
            o = int(W.lgu[p_])
            ww = w.copy()
            ww[o] = 0
            to = int(rng.choice(len(ww), p=ww / ww.sum()))
            W.moves.append((p_, dms + int(rng.random() * span), o, to))
            W.lgu[p_] = to
        # arrivals from other provinces: the oldest into the city, the peri-urban LGUs and the towns, young adults into the
        # city and the peri-urban LGUs
        for code, k_ in P.KAPPA_IN_EXT.items():
            dl = P.CODES.index(code)
            res = sidx[(sli == dl) & (sage >= P.ELDER_MIN_AGE)]
            if res.size == 0:
                continue
            ra = (dms - W.birth[res]) / 365.2425
            hh = hazard(np.minimum(ra, P.ELDER_CAP_AGE), W.sex[res].astype(float), mort[dl], ms) / 12.0
            k = rng.poisson(k_ * hh.sum())
            if k:
                pick = rng.choice(res.size, size=k, p=hh / hh.sum())
                new = new_persons(k, dl, W.sex[res[pick]], W.birth[res[pick]] + rng.normal(0, 200, k), origin=13)
                for p_ in new:
                    W.moves.append((p_, dms + int(rng.random() * span), 13, dl))
        for code, rate in P.EXT_YOUNG_IN.items():
            dl = P.CODES.index(code)
            res = sidx[(sli == dl) & (sage >= 16) & (sage < 30)]
            k = rng.poisson(rate * res.size / 12.0)
            if k:
                pick = rng.choice(res.size, size=k)
                new = new_persons(k, dl, W.sex[res[pick]], W.birth[res[pick]] + rng.normal(0, 300, k), origin=13)
                for p_ in new:
                    W.moves.append((p_, dms + int(rng.random() * span), 13, dl))
        # births to women resident in the province
        fem = inprov & (smale == 0) & (sage >= 15) & (sage < 50)
        mothers = sidx[fem]
        pb = asfr(sage[fem], tfr[sli[fem]]) / 12.0
        give = mothers[rng.random(mothers.size) < pb]
        if give.size:
            bd = dms + np.floor(rng.random(give.size) * span)
            kids = new_persons(give.size, W.lgu[give], (rng.random(give.size) < 0.512).astype(np.int8), bd)
            W.mother[kids] = give
            for k_, m_, b_ in zip(kids, give, bd.astype(int)):
                W.births.append((k_, m_, b_, int(W.lgu[m_])))
            # twins, about one birth in eighty
            tw = give[rng.random(give.size) < 0.0125]
            if tw.size:
                bt = W.birth[kids[np.isin(give, tw)]]
                k2 = new_persons(tw.size, W.lgu[tw], (rng.random(tw.size) < 0.512).astype(np.int8), bt)
                W.mother[k2] = tw
                for k_, m_, b_ in zip(k2, tw, bt.astype(int)):
                    W.births.append((k_, m_, b_, int(W.lgu[m_])))
    W.cap = cap
    return W
