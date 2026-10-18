"""The 2026 population of trips parked in Brennick's long-stay lots and the card survey drawn from it."""
import datetime as dt

import numpy as np

import world as W


def quarter_of(d):
    return (d.month - 1) // 3 + 1


def dow_factor(d):
    # Departures by car peak Thursday to Sunday; Tuesday is quietest.
    return {0: 1.01, 1: 0.93, 2: 0.96, 3: 1.03, 4: 1.06, 5: 0.99, 6: 1.02}[d.weekday()]


def stays(rng, n, mean, shape):
    """Nights parked: a rounded gamma draw, capped at the lots' 28-day limit."""
    x = np.rint(rng.gamma(shape, mean / shape, size=n)).astype(int)
    bad = x > W.MAX_STAY
    while bad.any():       # a stay longer than the lots allow is not a parked trip: those travellers do not park
        x[bad] = np.rint(rng.gamma(shape, mean / shape, size=int(bad.sum()))).astype(int)
        bad = x > W.MAX_STAY
    return x


def party_size(u, mean):
    """1 plus a Poisson count of companions with mean (mean - 1), by inversion of one uniform."""
    lam = max(mean - 1.0, 0.0)
    k, p = 0, np.exp(-lam)
    cum = p
    while u > cum and k < 30:
        k += 1
        p *= lam / k
        cum += p
    return 1 + k


def lot_for(rng, n):
    """The lot a car parks in, by the lots' shares of entries, whatever the stay: the economy lots are cheaper and
    farther out, Long-Term a walk from the terminal."""
    p = [W.LOT_SHARE[l] for l in W.LOTS]
    return [W.LOTS[i] for i in rng.choice(3, size=n, p=p)]


def draw(seed=W.SEED):
    """Every 2026 trip by day and lot, the cards handed in the four waves and which of them came back by the last
    box collection. A card that could have come back but was not returned is kept in `held`."""
    rng = np.random.default_rng(seed)
    days = [dt.date(W.YEAR, 1, 1) + dt.timedelta(days=i) for i in range(365)]
    # Daily mean trips by group, shaped by day of week and normalised to each quarter's register entries.
    sa_q = {}
    for q in (1, 2, 3, 4):
        sa_q[q] = {m: v[1] * v[5][q - 1] / sum(v[5]) for m, v in W.MARKETS.items()}
    truth = {q: {m: 0 for m in W.MARKETS} for q in (1, 2, 3, 4)}
    entries = []          # (date, lot, n) for the register
    cards = []            # dicts, one per returned card
    held = []             # cards whose car left in time but whose card was not returned
    wave_days = {}
    for name, q, start in W.WAVES:
        for i in range(W.HAND_DAYS):
            wave_days[start + dt.timedelta(days=i)] = (name, q, i + 1, start)
    serial = {name: 0 for name, _, _ in W.WAVES}
    handout = []          # (wave, date, lot, first serial, last serial, handed)
    # each plaza's attendants on each handout day: the share of cars they reached moves with the staffing
    srng = np.random.default_rng([seed, 11])
    staffing = {(name, i + 1, l): float(np.clip(srng.normal(1.0, 0.035), 0.9, 1.06))
                for name, _, _ in W.WAVES for i in range(W.HAND_DAYS) for l in W.LOTS}
    for d in days:
        q = quarter_of(d)
        dows = sum(dow_factor(x) for x in days if quarter_of(x) == q)
        f = dow_factor(d) / dows
        lot_count = {l: 0 for l in W.LOTS}
        groups = [(m, sa_q[q][m] * f) for m in W.MARKETS]
        sa_total = sum(v for _, v in groups)
        groups.append(("NONSA", max(W.QUARTER_ENTRIES[q] * f - sa_total, 0.0)))
        in_wave = d in wave_days
        day_cards = {l: [] for l in W.LOTS}
        for g, mean in groups:
            n = rng.poisson(mean)
            if n == 0:
                continue
            if g == "NONSA":
                L = stays(rng, n, W.NONSA["nights"][q - 1], W.NONSA["shape"])
            else:
                spec = W.MARKETS[g]
                L = stays(rng, n, spec[2][q - 1], spec[3])
                truth[q][g] += n
            P = [0] * n           # the party: each card's own draw (answers)
            lots = lot_for(rng, n)
            for k in range(n):
                lot_count[lots[k]] += 1
                if in_wave:
                    day_cards[lots[k]].append((g, int(L[k]), int(P[k])))
        for l in W.LOTS:
            entries.append((d, l, lot_count[l]))
        if in_wave:
            wname, wq, t, start = wave_days[d]
            for l in W.LOTS:
                pool = day_cards[l]
                rng.shuffle(pool)
                u = rng.random((len(pool), 2))           # each car: handed a card? returned it?
                cover = min(0.99, W.HANDOUT_COVER[wq] * W.LOT_COVER[l] * staffing[(wname, t, l)])
                resp = W.RESPONSE[wq] * W.LOT_RESPONSE[l]
                first = serial[wname] + 1
                n_handed = 0
                for k, (g, L, P) in enumerate(pool):
                    if u[k, 0] >= cover:
                        continue
                    n_handed += 1
                    serial[wname] += 1
                    exit_day = t + L
                    if exit_day <= W.LAST_COLLECT:
                        c = dict(wave=wname, q=wq, t=t, date=d, lot=l, serial=serial[wname], group=g, nights=L,
                                 party=P, collected=start + dt.timedelta(days=exit_day - 1))
                        (cards if u[k, 1] < resp else held).append(c)
                handout.append((wname, d, l, first, serial[wname], n_handed))
    return dict(truth=truth, entries=entries, cards=cards, handout=handout, held=held, handed=dict(serial))


def build(seed=W.SEED, tune=True):
    """The population, the handout and the replies with each card's answers; the reply draw settled (calibrate.py)."""
    x = draw(seed)
    attach(x["cards"] + x["held"], seed, x["handed"])
    if tune:
        import calibrate
        calibrate.settle(x, seed)
    x["cards"].sort(key=lambda c: (c["wave"], c["serial"]))
    return x


def written_party(u, p, kind):
    """The party as the traveller wrote it, and the number the contractor's coding took from it (the first number
    written). u: three uniforms."""
    if p >= 2 and u[0] < W.COMPOUND[kind]:
        form = int(np.searchsorted(np.cumsum((0.45, 0.20, 0.20, 0.15)), u[1], side="right"))
        a = 1 + int(u[2] * (p - 1))
        if form == 0:
            return "%d+%d" % (a, p - a), a
        if form == 1:
            return "%d + %d" % (a, p - a), a
        if form == 2 and p >= 3:
            a = min(2, p - 1)
            return "%d adults %d kid%s" % (a, p - a, "" if p - a == 1 else "s"), a
        return "me + %d" % (p - 1), p - 1
    # the rest write the party's number, a few with a word on who it is (the coding keeps the number)
    if u[1] < (W.ANNOTATE_SINGLE if p == 1 else W.ANNOTATE[kind]):
        k = u[2]
        if p == 1:
            return ["1 (me)", "1 (just me)", "1 (myself)"][pick(np.array([0.52, 0.81, 1.0]), k)], 1
        if p == 2:
            return ["2 (me and my wife)", "2 (me and my husband)", "2 (me + 1)", "2 incl. me",
                    "2 including me"][pick(np.array([0.31, 0.52, 0.71, 0.88, 1.0]), k)], 2
        return ["%d (2 adults %d kid%s)" % (p, p - 2, "" if p == 3 else "s"), "%d incl. me" % p,
                "%d (me + %d)" % (p, p - 1)][pick(np.array([0.46, 0.76, 1.0]), k)], p
    return str(p), p


NONSA_MIX = {"TPA": 0.035, "PHX": 0.035, "RSW": 0.02, "ORL": 0.05, "FLL": 0.03, "LAS": 0.045, "MYR": 0.02,
             "SAN": 0.025, "DEN": 0.04, "BNA": 0.025, "WAS": 0.06, "NYC": 0.07, "BOS": 0.035, "DFW": 0.045,
             "HOU": 0.03, "CHI": 0.04, "CLT": 0.025, "DTT": 0.02, "OTH": 0.35}
_MK = list(NONSA_MIX)
_MP = np.cumsum([NONSA_MIX[m] for m in _MK]) / sum(NONSA_MIX.values())
_OW = np.cumsum([x[3] for x in W.OTHER_AIRPORTS]) / sum(x[3] for x in W.OTHER_AIRPORTS)
_CO = list(W.COUNTIES)
_CP = np.cumsum([W.COUNTIES[c][1] for c in _CO]) / sum(W.COUNTIES[c][1] for c in _CO)
NU = 15


def pick(cum, u):
    return min(int(np.searchsorted(cum, u, side="right")), len(cum) - 1)


def destination(u, market):
    """The airport the party flew to, what the traveller wrote and the code the contractor's coder gave it."""
    if market == "OTH":
        code, city, name, _ = W.OTHER_AIRPORTS[pick(_OW, u[0])]
        k = pick(np.array([0.6, 0.85, 1.0]), u[1])
        written = [city, code, (city + " " + ["Intl", "airport"][int(u[2] * 2)])][k]
        return code, written, code
    name, airports = W.CITY_MARKETS[market]
    ap = airports[pick(np.cumsum([s for _, s in airports]), u[0])][0]
    if market in W.METRO and u[3] < W.CITY_ONLY[market]:
        metro = W.METRO[market]
        return ap, W.WRITTEN[metro][written_pick(u[1], len(W.WRITTEN[metro]))], metro
    return ap, W.WRITTEN[ap][written_pick(u[1], len(W.WRITTEN[ap]))], ap


def written_pick(u, n):
    """Which way of writing a place a traveller used: the plain name most often, the rarer forms less and less."""
    w = 0.62 ** np.arange(n)
    return pick(np.cumsum(w) / w.sum(), u)


def home_zip(u, sa):
    if sa:
        zips = W.COUNTIES[_CO[pick(_CP, u[0])]][0]
        cum = np.cumsum([W.ZIP_WEIGHT.get(z, 1.0) for z in zips])
        return zips[pick(cum / cum[-1], u[1])]
    k = 0
    while True:
        z = W.NONSA_PREFIXES[int(u[0] * len(W.NONSA_PREFIXES))] + "%02d" % (1 + int(u[1 + k % 2] * 99))
        if z not in W.SA_ZIPS:
            return z
        u = (u[0], (u[1] * 7.31) % 1.0, (u[2] * 3.17) % 1.0)
        k += 1


def answers(c, u):
    """Each card's answers from its own row of uniforms, so a card's answers do not depend on which other cards
    came back."""
    g = c["group"]
    kind = W.KIND.get(g, "leisure") if g != "NONSA" else ("business" if c["nights"] <= 3 else "leisure")
    c["party"] = party_size(u[14], W.NONSA["party"] if g == "NONSA" else W.MARKETS[g][4])
    c["purpose"] = "BLVO"[pick(np.cumsum(W.PURPOSE[kind]), u[0])]
    c["party_written"], c["party_keyed"] = written_party(u[1:4], c["party"], kind)
    c["market"] = g if g != "NONSA" else _MK[pick(_MP, u[4])]
    c["airport"], c["dest_written"], c["dest_code"] = destination(u[5:9], c["market"])
    c["zip"] = home_zip(u[9:12], g != "NONSA")
    # the ZIP as keyed: a few travellers write ZIP+4, a few keyed entries carry a leading space
    c["zip_keyed"] = c["zip"]
    if u[12] < W.ZIP_FORMS[0]:
        c["zip_keyed"] = "%s-%04d" % (c["zip"], 1000 + int(u[13] * 8999))
    elif u[12] < W.ZIP_FORMS[1]:
        c["zip_keyed"] = "%s%04d" % (c["zip"], 1000 + int(u[13] * 8999))
    elif u[12] < W.ZIP_FORMS[2]:
        c["zip_keyed"] = " " + c["zip"]
    return c


def uniforms(seed, handed):
    return {w: np.random.default_rng([seed, 7, i + 1]).random((n + 1, NU)) for i, (w, n) in enumerate(sorted(handed.items()))}


def attach(cards, seed, handed):
    U = uniforms(seed, handed)
    for c in cards:
        answers(c, U[c["wave"]][c["serial"]])
