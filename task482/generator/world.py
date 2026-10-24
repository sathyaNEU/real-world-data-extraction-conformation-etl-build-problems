"""The Wendleglen world for task482: eight Medicare hospice provider numbers' elections, every later election at any
hospice, and deaths. Day 0 is 2016-10-01 (the records begin with FY2017); arrivals start in October 2010 so the first
years hold patients already in care; lifetimes run ten years past the close so the truth is known.

The simulation is the stage 2 world (task482 design note, Ladder) and must reproduce it exactly: every draw here is in
the order the stage 2 prototype made it, from one generator seeded with SEED. Attributes the pack needs and the
simulation does not (identifiers, diagnosis codes, levels of care, claims) are drawn in records.py from other streams.
"""
import datetime as dt
import math

import numpy as np

SEED = 3
DAY0 = dt.date(2016, 10, 1)
D0 = -2192                      # 2010-10-01
FY = (3287, 3652)               # FY2026: 2025-10-01 to 2026-09-30
CLOSE = 3744                    # 2027-01-01; days on file run through 2026-12-31
END = CLOSE + 3650
CAP = 35361.44                  # FY2026 aggregate cap amount per beneficiary
SEQ = 0.02
GRP = ("C", "D", "P", "O")      # cancer, dementia, heart and lung, other
GROUP_NAME = {"C": "Cancer", "D": "Dementia", "P": "Heart and lung", "O": "Other"}

DEATH = {"C": (math.log(22), 1.15), "D": (math.log(120), 1.3), "P": (math.log(48), 1.3), "O": (math.log(58), 1.3)}
REELECT_SHIFT = math.log(0.75)  # a beneficiary who comes back is in decline: a re-election runs shorter
DAMP = 0.15                     # and seldom ends alive again
OUT_LOS = 1.2                   # stays at hospices outside the organisation
Q_REV = {"C": 0.07, "D": 0.06, "P": 0.08, "O": 0.07}
REV_MEAN = 40.0
Q_NLTI = {"C": 0.02, "D": 0.07, "P": 0.05, "O": 0.05}
Q_MOVE = 0.012
Q_TRANSFER = 0.02
_RR = 0.55
RET = {r: {"C": _RR * 0.7, "D": _RR, "P": _RR * 0.9, "O": _RR * 0.85} for r in ("revoked", "nlti", "moved")}
GAP = {r: (0.75, 15.0, 300.0) for r in ("revoked", "nlti", "moved")}
DEATH_OUT = {"C": 150.0 * 1.8, "D": 500.0 * 1.8, "P": 300.0 * 1.8, "O": 350.0 * 1.8}
REASONS = ("revoked", "nlti", "moved")

MIX = {"C": [0.45, 0.18, 0.22, 0.15], "M": [0.25, 0.38, 0.22, 0.15], "D": [0.12, 0.62, 0.12, 0.14]}
CODES = ("BRK", "COR", "DUN", "LIN", "PEN", "SAL", "WEX", "FAL")


class Prog:
    def __init__(self, code, lam, mix, m_rev, m_nlti, p_out, p_org, m_los):
        self.code, self.lam, self.mix = code, lam, mix
        self.m_rev, self.m_nlti, self.p_out, self.p_org, self.m_los = m_rev, m_nlti, p_out, p_org, m_los


PROGS = [Prog("BRK", 0.6, MIX["D"], 1, 1, 0.5, 0.06, 1.00), Prog("COR", 1.6, MIX["C"], 1, 1, 0.5, 0.06, 0.90),
         Prog("DUN", 0.9, MIX["M"], 1.5, 1.5, 0.5, 0.06, 1.10), Prog("LIN", 0.5, MIX["D"], 1, 1, 0.5, 0.06, 1.00),
         Prog("PEN", 1.4, MIX["C"], 1, 1, 0.5, 0.06, 0.85), Prog("SAL", 1.1, MIX["M"], 1, 1, 0.5, 0.06, 1.15),
         Prog("WEX", 0.6, MIX["M"], 1, 1, 0.5, 0.06, 1.25), Prog("FAL", 0.6, MIX["D"], 4.0, 3.0, 0.85, 0.02, 1.45)]
BY = {p.code: p for p in PROGS}


def recerts():
    b, out = 90, []
    while b < 6000:
        out.append(b)
        b += 90 if len(out) < 2 else 60
    return out


RECERT = recerts()


def date_of(day):
    return DAY0 + dt.timedelta(days=int(day))


def episode(rng, g, prog, reelect):
    """Length and end of one election at one provider number (the stage 2 draw order)."""
    mu, sg = DEATH[g]
    mu += math.log(prog.m_los if prog is not None else OUT_LOS)
    if reelect:
        mu += REELECT_SHIFT
    td = max(1, int(round(rng.lognormal(mu, sg))))
    mr = prog.m_rev if prog else 1.0
    mn = prog.m_nlti if prog else 1.0
    damp = DAMP if reelect else 1.0
    ends = [(td, "death")]
    if rng.random() < Q_REV[g] * mr * damp:
        ends.append((1 + int(rng.exponential(REV_MEAN)), "revoked"))
    q = Q_NLTI[g] * mn * damp
    for b in RECERT:
        if b >= td:
            break
        if rng.random() < q:
            ends.append((b + int(rng.integers(0, 15)), "nlti"))
            break
    if rng.random() < Q_MOVE:
        ends.append((1 + int(rng.integers(0, td)), "moved"))
    if rng.random() < Q_TRANSFER:
        ends.append((1 + int(rng.integers(0, td)), "transfer"))
    L, why = min(ends)
    return L, why


def simulate(seed=SEED):
    """Beneficiaries as (admitting program, group, episodes, dod). An episode is (start, end, provider, why) with the
    provider a program code or "OUT"; days billed are end - start (a live discharge's day not counted, the day of death
    counted); dod is the day after death (death on dod - 1), None if alive at END."""
    rng = np.random.default_rng(seed)
    codes = list(CODES)
    bens = []
    for p in PROGS:
        n = rng.poisson(p.lam * (CLOSE - D0))
        starts = np.sort(rng.integers(D0, CLOSE, n))
        groups = rng.choice(4, n, p=p.mix)
        for s, gi in zip(starts, groups):
            g = GRP[gi]
            eps, t, h, reelect, dod = [], int(s), p.code, False, None
            while t < END:
                L, why = episode(rng, g, BY.get(h), reelect)
                eps.append((t, t + L, h, why))
                t += L
                if why == "death":
                    dod = t
                    break
                if why == "transfer":
                    h = "OUT" if rng.random() < 0.5 or h not in codes else str(rng.choice([c for c in codes if c != h]))
                    continue
                pr = RET[why][g]
                if rng.random() >= pr:
                    dod = t + 1 + int(rng.exponential(DEATH_OUT[g]))
                    break
                fast, m1, m2 = GAP[why]
                gap = rng.exponential(m1) if rng.random() < fast else rng.exponential(m2)
                t += 1 + int(gap)
                src = BY[p.code]
                v = rng.random()
                if why == "moved" or v < src.p_out:
                    h = "OUT"
                elif v < src.p_out + src.p_org:
                    h = str(rng.choice([c for c in codes if c != p.code]))
                else:
                    h = eps[-1][2] if eps[-1][2] in codes else p.code
                reelect = True
            bens.append((p.code, g, eps, dod))
    return bens


def state_at_close(eps, dod):
    """('open', days so far, provider) | ('out', days out, reason) | ('dead',) | ('none',) as known at the close."""
    seen = [e for e in eps if e[0] < CLOSE]
    if not seen:
        return ("none",)
    last = seen[-1]
    if last[1] > CLOSE:
        return ("open", CLOSE - last[0], last[2])
    if last[3] == "death" or (dod is not None and dod <= CLOSE):
        return ("dead",)
    if last[3] == "transfer":
        return ("open", 0, last[2])
    return ("out", CLOSE - last[1], last[3])


def fy_days(eps, code):
    return sum(max(0, min(e[1], FY[1]) - max(e[0], FY[0])) for e in eps if e[2] == code)


def known_days(eps):
    return sum(max(0, min(e[1], CLOSE) - e[0]) for e in eps if e[0] < CLOSE)


def total_days(eps):
    return sum(e[1] - e[0] for e in eps)
