"""task156: the members, worksites, delegates, online votes and protected action ballots, generated once and cached.

The generating process (never shipped): each member's chance of voting is a logistic in the ballot's own level, the
member's age, membership years and employment, the member's own propensity, the council's level, and a lift of GAMMA
where an elected delegate is active at the member's worksite on the ballot's close (elected for the term in force and
still a member). Council levels are set so that a March 2027 ballot run on the 2024-26 delegates would show each
council's base27 turnout; the 2026-28 delegates then give the truth."""
import datetime as dt
import functools
import math

import numpy as np

import world as W

AGE_EFF = [(30, -0.55), (45, -0.20), (60, 0.00), (200, 0.20)]
EMP_EFF = {"Full time": 0.0, "Part time": -0.10, "Casual": -0.45}


def expit(x):
    return 1.0 / (1.0 + np.exp(-x))


def years(a, b):
    return (b - a).days / 365.25


def age_eff(age):
    for lim, e in AGE_EFF:
        if age < lim:
            return e
    return 0.2


class Pop:
    pass


def _date(rng, a, b):
    span = (b - a).days
    return a + dt.timedelta(days=int(rng.integers(0, span + 1)))


@functools.lru_cache(maxsize=None)
def build():
    rng = np.random.default_rng(W.SEED)
    P = Pop()
    P.sites = []          # dicts: code, old, council, name, weight
    P.members = []        # dicts
    site_by_c = {}
    mno = 104000
    for ci, row in enumerate(W.COUNCILS):
        code, name, cand, n, ns = row[:5]
        kinds = list(W.SITE_KINDS)
        sites = []
        used = set()
        for k in range(ns):
            kind, wgt = kinds[k % len(kinds)]
            town = W.TOWNS[int(rng.integers(0, len(W.TOWNS)))]
            label = "%s %s" % (town, kind) if k >= 2 else kind
            while label in used:
                town = W.TOWNS[int(rng.integers(0, len(W.TOWNS)))]
                label = "%s %s" % (town, kind)
            used.add(label)
            s = {"code": "%s-%03d" % (code, 101 + k), "old": "%02d%02d" % (ci + 11, k + 1), "council": code,
                 "name": label, "weight": wgt * float(rng.uniform(0.6, 1.5))}
            sites.append(s)
        P.sites.extend(sites)
        site_by_c[code] = sites
        wts = np.array([s["weight"] for s in sites])
        wts = wts / wts.sum()
        # members ever, 2014 onward: roughly stationary; active on the extract close to n
        n_ever = int(n * 1.75)
        for i in range(n_ever):
            join = _date(rng, dt.date(1998, 1, 1), dt.date(2026, 9, 30))
            # recent joins more common (membership turns over)
            if rng.uniform() < 0.55:
                join = _date(rng, dt.date(2016, 1, 1), dt.date(2026, 9, 30))
            dur = float(rng.exponential(9.0))
            cease = join + dt.timedelta(days=int(dur * 365.25))
            if cease > W.EXTRACT:
                cease = None
            elif cease < dt.date(2019, 7, 1):
                continue
            by = int(rng.integers(1956, 2004))
            if join.year - by < 18:
                join = dt.date(by + 18, join.month, min(join.day, 28))
                if cease is not None and cease <= join:
                    continue
            dob = dt.date(by, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
            u = rng.uniform()
            emp = "Full time" if u < 0.62 else ("Part time" if u < 0.88 else "Casual")
            site = sites[int(rng.choice(len(sites), p=wts))]
            mno += int(rng.integers(1, 4))
            m = {"no": mno, "council": code, "site": site["code"], "dob": dob, "join": join, "cease": cease,
                 "emp": emp, "band": int(rng.choice([1, 2, 3, 4, 5, 6, 7, 8], p=[.06, .14, .2, .2, .16, .12, .08, .04])),
                 "gender": "F" if rng.uniform() < 0.58 else "M", "u": float(rng.normal(0, W.U_SD)),
                 "contact": "email" if rng.uniform() < 0.86 else ("sms" if rng.uniform() < 0.7 else "none"),
                 "pay": "payroll" if rng.uniform() < 0.83 else "direct debit"}
            P.members.append(m)
    P.site_by_c = site_by_c
    P.by_no = {m["no"]: m for m in P.members}
    P.by_site = {}
    for m in P.members:
        P.by_site.setdefault(m["site"], []).append(m)
    _delegates(P)
    _calibrate(P)
    _votes(P)
    _pabs(P)
    return P


def active(m, d):
    return m["join"] <= d and (m["cease"] is None or m["cease"] > d)


def _cov_target(code, term):
    row = [r for r in W.COUNCILS if r[0] == code][0]
    idx = {2018: 5, 2020: 5, 2022: 6, 2024: 7, 2026: 8}[term]
    return row[idx]


def _delegates(P):
    """Delegate sites per term with ordinary churn, then delegates drawn from the site's members at term start."""
    P.deleg = []          # rows: term, council, site, member, elected, term_end, role, status
    P.dsites = {}         # (term, site) -> list of delegate member numbers
    for ci, code in enumerate(W.CODES):
        rng = np.random.default_rng([W.SEED, 100 + ci])
        sites = P.site_by_c[code]
        prev = None
        for term in W.TERMS:
            start = dt.date(term, 7, 1)
            sizes = {s["code"]: sum(active(m, start) for m in P.by_site.get(s["code"], [])) for s in sites}
            tot = sum(sizes.values()) or 1
            target = _cov_target(code, term)
            order = [s["code"] for s in sites]
            if prev is None:
                rng.shuffle(order)
                chosen = []
                for c in sorted(order, key=lambda c: -sizes[c] * float(rng.uniform(0.5, 1.5))):
                    if sum(sizes[x] for x in chosen) / tot < target - 0.02:
                        chosen.append(c)
            else:
                chosen = list(prev)
                big = abs(target - _cov_target(code, term - 2)) > 0.15
                if not big:
                    # ordinary churn: a few sites lose their delegate, a few gain one
                    k = max(1, int(round(0.15 * len(sites))))
                    drop = [c for c in chosen if rng.uniform() < k / max(1, len(sites))]
                    chosen = [c for c in chosen if c not in drop]
                cur = sum(sizes[x] for x in chosen) / tot
                pool = [c for c in order if c not in chosen]
                rng.shuffle(pool)
                while cur < target - 0.02 and pool:
                    c = pool.pop()
                    chosen.append(c)
                    cur = sum(sizes[x] for x in chosen) / tot
                while cur > target + 0.03 and len(chosen) > 1:
                    c = chosen[int(rng.integers(0, len(chosen)))]
                    chosen.remove(c)
                    cur = sum(sizes[x] for x in chosen) / tot
            prev = list(chosen)
            for c in sorted(chosen):
                end = dt.date(term + 2, 6, 30)
                stay = rng.uniform() < 0.96
                cands = [m for m in P.by_site.get(c, []) if active(m, start) and years(m["join"], start) >= 1.0
                         and (not stay or m["cease"] is None or m["cease"] > end)]
                if not cands:
                    cands = [m for m in P.by_site.get(c, []) if active(m, start)]
                if not cands:
                    continue
                nd = 2 if sizes[c] >= 60 and rng.uniform() < 0.5 else 1
                picks = rng.choice(len(cands), size=min(nd, len(cands)), replace=False)
                lst = []
                for j, pi in enumerate(sorted(picks)):
                    m = cands[pi]
                    lst.append(m["no"])
                    P.deleg.append({"term": term, "council": code, "site": c, "member": m["no"],
                                    "elected": dt.date(term, 6, int(rng.integers(10, 28))),
                                    "start": start, "end": dt.date(term + 2, 6, 30),
                                    "role": "Senior delegate" if j == 0 and nd == 2 else "Delegate",
                                    "status": "Elected" if rng.uniform() < 0.35 else "Unopposed"})
                P.dsites[(term, c)] = lst


def D(P, site, d):
    """1 if an elected delegate for the term in force on d is still a member on d."""
    term = W.term_of(d)
    for no in P.dsites.get((term, site), []):
        if active(P.by_no[no], d):
            return 1.0
    return 0.0


def xb(m, d):
    age = years(m["dob"], d)
    ten = max(0.0, years(m["join"], d))
    return age_eff(age) + 0.18 * math.log(1 + ten) + EMP_EFF[m["emp"]]


def _calibrate(P):
    """Council level v so that a ballot on the 2024-26 delegates (as they stood at 30 June 2026) shows base27."""
    P.v = {}
    end24 = dt.date(2026, 6, 30)
    for row in W.COUNCILS:
        code, base = row[0], row[9]
        roll = [m for m in P.members if m["council"] == code and active(m, W.EXTRACT)]
        x = np.array([xb(m, W.BALLOT_CLOSE) + m["u"] for m in roll])
        d24 = np.array([D(P, m["site"], end24) for m in roll])
        lo, hi = -4.0, 4.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if expit(W.PAB_ALPHA + x + mid + W.GAMMA * d24).mean() < base:
                lo = mid
            else:
                hi = mid
        P.v[code] = (lo + hi) / 2


def prob(P, m, d, alpha, deleg=None):
    dd = D(P, m["site"], d) if deleg is None else deleg
    return float(expit(alpha + xb(m, d) + m["u"] + P.v[m["council"]] + W.GAMMA * dd))


def _votes(P):
    """Online vote invitations: every member active at the open with a contact on file."""
    P.inv = []
    seq = 0
    for vi, (vid, title, op, cl, off) in enumerate(W.VOTES):
        rng = np.random.default_rng([W.SEED, 200 + vi])
        d = cl.date()
        span = (cl - op).total_seconds()
        for m in P.members:
            if not active(m, op.date()) or m["contact"] == "none":
                continue
            seq += 1
            p = prob(P, m, d, W.VOTE_ALPHA[vid])
            voted = rng.uniform() < p
            cast = None
            if voted:
                # most votes in the first day and after the two reminders
                r = rng.uniform()
                if r < 0.45:
                    t = rng.uniform(0, 0.12)
                elif r < 0.75:
                    t = rng.uniform(0.40, 0.52)
                else:
                    t = rng.uniform(0.12, 0.999)
                cast = op + dt.timedelta(seconds=int(t * span))
            P.inv.append({"vote": vid, "seq": seq, "member": m["no"], "channel": m["contact"],
                          "sent_local": op + dt.timedelta(minutes=int(rng.integers(0, 50))),
                          "cast_local": cast, "off": off})


def _pabs(P):
    """Protected action ballots in the 2021 and 2023-24 rounds: the roll is every member employed at the council on
    the roll date; the declared turnout is drawn and then held within about half a point of its expectation."""
    P.pab = []
    for ci, row in enumerate(W.COUNCILS):
        code, hist = row[0], row[10]
        for rnd in hist.split():
            rng = np.random.default_rng([W.SEED, 300 + ci, int(rnd)])
            a, b = W.PAB_ROUNDS[rnd]
            close = _date(rng, a, b)
            close = close + dt.timedelta(days=(4 - close.weekday()) % 7)   # ballots close on a Friday
            rolld = close - dt.timedelta(days=int(rng.integers(30, 45)))
            roll = [m for m in P.members if m["council"] == code and active(m, rolld)]
            ps = np.array([prob(P, m, close, W.PAB_ALPHA) for m in roll])
            votes = rng.uniform(size=len(ps)) < ps
            want = ps.sum()
            # hold the count within 0.5 per cent of the roll of its expectation
            tol = max(1, int(0.005 * len(ps)))
            while votes.sum() > want + tol:
                idx = np.flatnonzero(votes)
                votes[idx[int(rng.integers(0, len(idx)))]] = False
            while votes.sum() < want - tol:
                idx = np.flatnonzero(~votes)
                votes[idx[int(rng.integers(0, len(idx)))]] = True
            nv = int(votes.sum())
            yes_share = float(rng.uniform(0.86, 0.97))
            informal = int(round(nv * float(rng.uniform(0.004, 0.015))))
            yes = int(round((nv - informal) * yes_share))
            P.pab.append({"round": rnd, "council": code, "roll_date": rolld, "close": close, "open": close -
                          dt.timedelta(days=14), "roll": len(roll), "returned": nv, "informal": informal,
                          "yes": yes, "no": nv - informal - yes, "expected": float(ps.mean())})
