"""Simulate the census: addresses and households, self-response and the follow-up (visits, proxies from the third
visit, re-interviews, late self-responses), the receipt register, persons with occupation write-ins, the coding front,
the autocoder and the clerical coders, and the coding quality study.

structure() draws everything the coding parameters do not touch; coding() draws the write-ins and their codes from fixed
uniforms, so a parameter change moves only what it governs."""
from datetime import date, timedelta

import numpy as np

import params as P
import world as W

D0 = date(2026, 1, 1)


def dn(d):
    return (d - D0).days


def dd(n):
    return D0 + timedelta(days=int(n))


def structure(seed=P.SEED):
    ss = np.random.SeedSequence(seed)
    r_addr, r_nrfu, r_form, r_pers = [np.random.default_rng(x) for x in ss.spawn(4)]
    rng = r_addr
    eds = W.eds(rng)
    ed_code = np.array([e[0] for e in eds])
    ed_region = np.array([e[1] for e in eds])
    n_eds = len(eds)
    # addresses
    per_ed = rng.poisson(P.ADDR_PER_ED, n_eds)
    a_ed = np.repeat(np.arange(n_eds), per_ed)
    n_a = len(a_ed)
    u = rng.random(n_a)
    kind = np.where(u < P.VACANT, "VAC", np.where(u < P.VACANT + P.NONRES, "DEL", "OCC"))
    # self-response before the follow-up list
    u = rng.random(n_a)
    early = np.full(n_a, "", object)
    occ = kind == "OCC"
    early[occ & (u < P.EARLY_SR["O"])] = "O"
    early[occ & (u >= P.EARLY_SR["O"]) & (u < P.EARLY_SR["O"] + P.EARLY_SR["P"])] = "P"
    # receipt dates of early self-response
    rec = np.full(n_a, -1, int)
    m = early == "O"
    k = m.sum()
    mixu = rng.random(k)
    r_on = np.where(mixu < 0.24, rng.uniform(dn(P.ONLINE_OPEN), dn(P.CENSUS_DAY), k),
                    np.where(mixu < 0.95, dn(P.CENSUS_DAY) + rng.exponential(8.5, k),
                             rng.uniform(dn(P.CENSUS_DAY), dn(P.NRFU_LIST), k)))
    rec[m] = np.minimum(r_on.astype(int), dn(P.NRFU_LIST))
    m = early == "P"
    k = m.sum()
    rec[m] = np.minimum((dn(P.CENSUS_DAY) - 2 + rng.gamma(2.2, 6.5, k)).astype(int), dn(P.NRFU_LIST))
    # the follow-up: every address without a self-response by the list cut
    nrfu = early == ""
    idx = np.where(nrfu)[0]
    rng = r_nrfu
    visits = []      # (address, visit_no, day, minute, outcome, respondent)
    route = early.copy()
    final_day = rec.copy()
    reint = np.zeros(n_a, bool)
    first = (dn(P.NRFU_START) + rng.beta(1.25, 1.9, len(idx)) * (dn(P.FIRST_VISIT_BY) - dn(P.NRFU_START))).astype(int)
    late_u = rng.random(len(idx))
    for j, a in enumerate(idx):
        day = int(first[j])
        if kind[a] != "OCC":
            n_v = 1 if rng.random() < 0.72 else 2
            for v in range(n_v):
                out = kind[a] if v == n_v - 1 else "NC"
                visits.append((a, v + 1, day, _minute(rng), out, ""))
                day += 4 + int(rng.exponential(5))
            continue
        # late self-response closes the case administratively
        late = ""
        if late_u[j] < P.LATE_SR["O"]:
            late = "O"
        elif late_u[j] < P.LATE_SR["O"] + P.LATE_SR["P"]:
            late = "P"
        late_day = day + int(rng.gamma(1.3, 14)) if late else 10 ** 6
        done = False
        proxied = False
        for v in range(6):
            if day > dn(P.FIELD_CLOSE):
                break
            if late and late_day <= day:
                break
            hh = rng.random() < P.HH_P[v]
            if hh:
                visits.append((a, v + 1, day, _minute(rng), "HH", ""))
                if proxied:
                    reint[a] = True
                route[a] = "FS"
                final_day[a] = day
                done = True
                break
            if proxied:
                visits.append((a, v + 1, day, _minute(rng), "NC", ""))
                break
            mop = day >= dn(P.MOPUP)
            if v >= 2 and rng.random() < (P.PX_MOP[v] if mop else P.PX_P[v]):
                resp = rng.choice(["NEIGHBOUR", "LANDLORD", "RELATIVE ELSEWHERE", "BUILDING MANAGER"],
                                  p=[0.71, 0.13, 0.11, 0.05])
                visits.append((a, v + 1, day, _minute(rng), "PX", resp))
                route[a] = "FP"
                final_day[a] = day
                if rng.random() < P.REINTERVIEW and v < 5 and day < dn(P.REINTERVIEW_BY):
                    proxied = True
                    day += 3 + int(rng.exponential(4))
                    continue
                done = True
                break
            out = "RF" if rng.random() < P.REFUSE else "NC"
            visits.append((a, v + 1, day, _minute(rng), out, ""))
            if day >= dn(P.MOPUP):
                day += P.GAP_MOP[0] + int(rng.exponential(P.GAP_MOP[1]))
            else:
                day += P.GAP_MIN + int(rng.exponential(P.GAP_MEAN))
        if proxied and route[a] == "FP":
            done = True
        if not done and late and late_day <= dn(P.FIELD_CLOSE):
            route[a] = late
            final_day[a] = late_day
            visits.append((a, None, late_day, None, "SR", ""))
    rng = r_form
    # a field form reaches the receipt register when the tablet syncs (the same evening or the next day; every form is
    # in by the close of field operations); a late self-response is registered on the day it is received
    rec = np.where(np.isin(route, ["FS", "FP"]), np.minimum(final_day + rng.integers(0, 2, n_a), dn(P.FIELD_CLOSE)),
                   final_day)
    # forms received by the close of field operations
    has_form = (route != "") & (rec <= dn(P.FIELD_CLOSE))
    route = np.where(has_form, route, "")
    # batches: created on receipt (online, field) or after scanning (paper)
    lag = np.where(route == "P", rng.integers(5, 26, n_a), np.where(route == "O", 1, rng.integers(1, 3, n_a)))
    bdate = rec + lag
    # persons with a write-in, persons in employment, usual residents
    wv, wp = zip(*P.WRITEINS)
    n_w = rng.choice(wv, size=n_a, p=wp)
    n_w = np.where(has_form, n_w, 0)
    blank_p = np.array([P.BLANK.get(r, 0.0) for r in route])
    n_blank = rng.binomial(np.where(has_form, n_w + 1, 0), blank_p)
    n_emp = n_w + n_blank
    n_res = n_emp + rng.choice([0, 1, 2, 3], size=n_a, p=[0.42, 0.33, 0.17, 0.08])
    n_res = np.where(has_form, np.maximum(n_res, 1), 0)
    # persons
    rng = r_pers
    owner = np.repeat(np.arange(n_a), n_w)
    n_p = len(owner)
    sm = np.array(W.GROUPS)
    sh = np.array([W.SHARE[g] for g in W.GROUPS])
    g_i = rng.choice(len(sm), size=n_p, p=sh / sh.sum())
    mix = W.unit_mix()
    unit = np.empty(n_p, object)
    for gi, g in enumerate(sm):
        mm = np.where(g_i == gi)[0]
        us, w = mix[g]
        unit[mm] = np.array(us, object)[rng.choice(len(us), size=len(mm), p=w)]
    person_no = np.concatenate([np.arange(1, c + 1) for c in n_w[n_w > 0]]) if n_p else np.zeros(0, int)
    S = dict(n_a=n_a, a_ed=a_ed, ed_code=ed_code, ed_region=ed_region, kind=kind, route=route, rec=rec, bdate=bdate,
             has_form=has_form, reint=reint, visits=visits, n_w=n_w, n_emp=n_emp, n_res=n_res, owner=owner,
             p_route=route[owner], p_unit=unit, p_group=np.array([x[:2] for x in unit]), person_no=person_no,
             p_bdate=bdate[owner], early=early)
    S["coded"] = S["p_bdate"] <= dn(P.CUT)
    S["rng_state"] = rng.bit_generator.state
    return S


def _minute(rng):
    """local minute of day of a doorstep visit: daytime, evening and Saturday-like spread"""
    return int(np.clip(rng.normal(15.3 * 60, 150), 9 * 60, 20 * 60 + 55))


def uniforms(S, seed=P.SEED + 7):
    rng = np.random.default_rng(seed)
    n = len(S["owner"])
    names = ["v", "ph", "txt", "sc", "sc2", "rec", "slip", "spec", "nat", "adj", "title", "cin", "cnat"]
    return {k: rng.random(n) for k in names}


def coding(S, U, prm=None):
    """write-ins and codes from fixed uniforms: vague or specific, the autocoder's suggestion and score, the clerical
    code, the production code under the old rule (coded so far) and under the new rule (the rest)"""
    prm = prm or dict(PHRASES=P.PHRASES, VAGUE=P.VAGUE, SELF_MULT=P.SELF_MULT, RECOVER=P.RECOVER, SLIP_MULT=P.SLIP_MULT)
    n = len(S["owner"])
    route = S["p_route"]
    unit = S["p_unit"]
    grp = S["p_group"]
    vague = np.zeros(n, bool)
    phrase = np.full(n, "", object)
    for g, (sv, pv, smx, pmx) in prm["VAGUE"].items():
        for r in P.ROUTES:
            m = (grp == g) & (route == r)
            rate = pv if r == "FP" else sv * prm["SELF_MULT"][r]
            mix = pmx if r == "FP" else smx
            hit = m & (U["v"] < rate)
            keys = list(mix)
            cum = np.cumsum([mix[k] for k in keys])
            cum = cum / cum[-1]
            pick = np.searchsorted(cum, U["ph"][hit], side="right")
            phrase[hit] = np.array(keys, object)[np.minimum(pick, len(keys) - 1)]
            vague[hit] = True
    # specific write-ins: suggestion and score; a slip puts the suggestion in a related unit group of another sub-major
    # group, a miss in another unit group of the same sub-major group
    sugg = unit.copy()
    score = np.zeros(n)
    spec = ~vague
    mix = W.unit_mix()
    pairs, pmult = slip_pairs(prm)
    has_pair = np.array([u_ in pairs for u_ in unit])
    m_u = np.array([pmult.get(u_, 1.0) for u_ in unit])
    s_u = U["spec"]
    slip = spec & has_pair & (s_u >= 1 - P.SPEC_SLIP * m_u)
    same = spec & ~slip & (s_u >= P.SPEC_RIGHT) & (s_u < 1 - P.SPEC_SLIP * m_u)
    for g in W.GROUPS:
        us, w = mix[g]
        m = np.where(same & (grp == g))[0]
        if len(us) > 1 and len(m):
            pos = np.array([us.index(x) for x in unit[m]])
            alt = np.minimum((U["nat"][m] * (len(us) - 1)).astype(int), len(us) - 2)
            alt = np.where(alt >= pos, alt + 1, alt)
            sugg[m] = np.array(us, object)[alt]
    sugg[slip] = np.array([pairs[x] for x in unit[slip]], object)
    right = spec & (sugg == unit)
    sc = U["sc"]
    score[right] = np.where(sc[right] < 0.84, 0.90 + 0.095 * U["sc2"][right],
                            np.where(sc[right] < 0.94, 0.80 + 0.10 * U["sc2"][right], 0.62 + 0.18 * U["sc2"][right]))
    wrong = spec & ~right
    score[wrong] = 0.70 + 0.25 * U["sc2"][wrong]
    for ph, (dflt, lo, hi) in prm["PHRASES"].items():
        m = phrase == ph
        sugg[m] = dflt
        score[m] = lo + (hi - lo) * U["sc"][m]
    score = np.round(score, 3)
    # clerical code (five-digit national code)
    rec_p = np.array([prm["RECOVER"][r] for r in route])
    cler_unit = np.where(vague & (U["rec"] >= rec_p), sugg, unit)
    cslip = spec & has_pair & (U["slip"] < P.CLER_SLIP * m_u)
    cler_unit[cslip] = np.array([pairs[x] for x in unit[cslip]], object)
    # clerical coders also slip inside the sub-major group (another unit group, or another national code of the unit)
    inside = spec & ~cslip & (U["cin"] < P.CLER_INSIDE)
    for g in W.GROUPS:
        us, w = mix[g]
        m = np.where(inside & (grp == g))[0]
        if len(us) > 1 and len(m):
            pos = np.array([us.index(x) for x in cler_unit[m]])
            alt = np.minimum((U["cnat"][m] * (len(us) - 1)).astype(int), len(us) - 2)
            alt = np.where(alt >= pos, alt + 1, alt)
            cler_unit[m] = np.array(us, object)[alt]
    nat_u = np.where(U["cnat"] < P.CLER_NATIONAL, U["cnat"] / P.CLER_NATIONAL, U["nat"])
    cler = np.array([_nat(x, v) for x, v in zip(cler_unit, nat_u)], object)
    ref = np.array([_nat(x, v) for x, v in zip(unit, U["nat"])], object)
    old_a = score >= P.OLD_ACCEPT
    new_a = score >= P.NEW_ACCEPT
    prod_old = np.where(old_a, sugg, cler)
    prod_new = np.where(new_a, sugg, cler)
    return dict(vague=vague, phrase=phrase, sugg=sugg, score=score, cler=cler, ref=ref, prod_old=prod_old,
                prod_new=prod_new, path_old=np.where(old_a, "A", "C"))


def slip_pairs(prm):
    """each unit group's related group across a sub-major boundary and the pair's slip-rate multiplier (a unit group in
    two pairs takes the later one)"""
    pairs, mult = {}, {}
    for k, (a, b) in enumerate(P.SLIP_PAIRS):
        m = prm.get("SLIP_MULT", {}).get(k, 1.0) if prm else 1.0
        pairs[a] = b
        pairs[b] = a
        mult[a] = m
        mult[b] = m
    return pairs, mult


_NAT = {}


def _nat(unit, u):
    if unit not in _NAT:
        _NAT[unit] = W.national_codes(unit)
    c = _NAT[unit]
    return c[min(int(u * len(c)), len(c) - 1)]
