"""How the quarter's reports come to exist, and the measures the run takes on them.

Every report is real. Nothing is planted. What makes the list hard is that one product holds two
fifths of the quarter's reports and its own reactogenicity sets the database's rate for the six
reactions it reports often, so every other product's ratio on those reactions is taken against a
background that is mostly that one product.
"""
import datetime as dt
import math
import random

import world as W

RB = {r: b for r, b, _ in W.REACTIONS}
SERIOUS = {r for r, _, s in W.REACTIONS if s}
RN = [r for r, _, _ in W.REACTIONS]


def _dates(rng, n):
    """receipt dates spread over the window, none on either boundary day"""
    span = (W.Q_TO - W.Q_FROM).days
    out = []
    for _ in range(n):
        d = W.Q_FROM + dt.timedelta(days=rng.randint(1, span - 1))
        out.append(d)
    return out


def _assign(cases, reaction, k, salt):
    """put a reaction on exactly k of these cases, so a product's own rate is not left to the draw"""
    pick = list(range(len(cases)))
    random.Random(W.SEED * 31 + salt).shuffle(pick)
    for i in pick[:k]:
        cases[i]["reactions"].add(reaction)


def draw():
    """the quarter's cases: one dict per case, with the reactions coded on it.

    Each product's own reactions are carried at its own rate and every other reaction at the rate the
    rest of the quarter's reports carry it. The booster's reports carry its reactogenicity on the six
    reactions the campaign produces and every other reaction at the rate of the reports that are not
    the campaign's, so a report of the booster says nothing about those reactions either way.
    """
    rng = random.Random(W.SEED * 17 + 5)
    bg = {r: RB[r] * W.BG_SCALE for r in RN}
    wts = [bg[r] for r in RN]
    cid = 480000
    cases = []
    by_code = {}

    def shell(code, name, d, cid):
        return {"case": "DK-ADR-%06d" % cid,
                "code": code, "product": name, "receipt": d,
                "lag": rng.choice([0, 1, 1, 2, 2, 3, 4, 5, 7, 9, 12, 18, 26]),
                "channel": rng.choices(W.CHANNELS, weights=[46, 24, 20, 10])[0],
                "reporter": rng.choices(W.REPORTERS, weights=[38, 22, 14, 20, 6])[0],
                "region": rng.choices(W.REGIONS, weights=[31, 23, 11, 15, 20])[0],
                "age": rng.choices(W.AGE_BANDS + [""], weights=[9, 28, 35, 25, 3])[0],
                "sex": rng.choices(["F", "M", ""], weights=[55, 43, 2])[0],
                "reactions": set()}

    plan = [(c, n, h, at, k, ex) for c, n, h, at, k, ex in W.PRODUCTS]
    for code, name, _h, _at, n, excess in plan:
        mine = []
        for d in _dates(rng, n):
            cid += 1
            c = shell(code, name, d, cid)
            for r in RN:
                if r in excess:
                    continue
                if rng.random() < bg[r]:
                    c["reactions"].add(r)
            mine.append(c)
        for r, p in sorted(excess.items()):
            _assign(mine, r, int(round(p * n)), sum(ord(x) for x in code + r))
        by_code[code] = mine
        cases += mine

    # the rate the reports that are not the campaign's carry each non-campaign reaction, taken off
    # the products that do not carry it at a rate of their own
    plain = [c for c in cases if not any(r in [x for x in W.PRODUCTS if x[0] == c["code"]][0][5]
                                         for r in [None])]
    clean = {}
    for r in RN:
        pool = [c for c in cases
                if r not in dict((x[0], x[5]) for x in W.PRODUCTS)[c["code"]]]
        clean[r] = sum(1 for c in pool if r in c["reactions"]) / len(pool)

    boost = []
    for d in _dates(rng, W.DOM_REPORTS):
        cid += 1
        boost.append(shell(W.DOMINANT, W.DOM_NAME, d, cid))
    for r, p in sorted(W.CAMPAIGN.items()):
        _assign(boost, r, int(round(p * W.DOM_REPORTS)), sum(ord(x) for x in "boost" + r))
    for r in RN:
        if r in W.CAMPAIGN:
            continue
        _assign(boost, r, int(round(clean[r] * W.DOM_REPORTS)),
                sum(ord(x) for x in "plain" + r))
    cases += boost

    for c in cases:
        if not c["reactions"]:
            c["reactions"].add(rng.choices(RN, weights=wts)[0])
        c["reactions"] = sorted(c["reactions"])
    cases.sort(key=lambda c: (c["receipt"], c["case"]))
    return cases


def pair_counts(cases):
    """reports per product code, and reports per (code, preferred term)"""
    npr, a = {}, {}
    for c in cases:
        npr[c["code"]] = npr.get(c["code"], 0) + 1
        for r in c["reactions"]:
            a[(c["code"], r)] = a.get((c["code"], r), 0) + 1
    return npr, a


def measure(npr, a, code, reaction, drop=()):
    """the proportional reporting ratio and the chi-square of the same table.

    `drop` is the set of product codes left out of what the ratio is taken against.
    """
    aa = a.get((code, reaction), 0)
    np_ = npr.get(code, 0)
    bb = np_ - aa
    cc = dd = 0
    for q, n in npr.items():
        if q == code or q in drop:
            continue
        x = a.get((q, reaction), 0)
        cc += x
        dd += n - x
    if aa == 0 or cc == 0 or np_ == 0:
        return None, None
    prr = (aa / np_) / (cc / (cc + dd))
    tot = aa + bb + cc + dd
    e = [(aa + bb) * (aa + cc) / tot, (aa + bb) * (bb + dd) / tot,
         (cc + dd) * (aa + cc) / tot, (cc + dd) * (bb + dd) / tot]
    chi = sum((o - x) ** 2 / x for o, x in zip((aa, bb, cc, dd), e))
    return prr, chi


def run(npr, a, drop=(), listed=True):
    """the pairs the standard's three criteria take forward.

    `drop` names the products left out of what every other product's ratio is taken against; a
    product is never left out of its own comparison. `listed` applies paragraph 3.3, which keeps a
    pair the product information already describes out of the run.
    """
    out = []
    for (code, reaction), aa in sorted(a.items()):
        if aa < W.N_MIN:
            continue
        if listed and reaction in W.LISTED.get(code, ()):
            continue
        prr, chi = measure(npr, a, code, reaction, tuple(q for q in drop if q != code))
        if prr is None:
            continue
        if prr >= W.PRR_MIN and chi >= W.CHI_MIN:
            out.append((code, reaction, prr, chi, aa))
    return out
