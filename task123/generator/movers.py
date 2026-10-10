"""Generic corpus movers: the grantees whose calendar-year income fell far enough to be offered in
one of the six March rounds, beyond the designed September cast. Each mover's dip sits in the
calendar year before its round and recovers the year after, so it is clear of the line at every
other census."""
import numpy as np

from common import SEED
from roster import Q, yr_quarters

GENERIC = {2021: 9, 2022: 10, 2023: 8, 2024: 10, 2025: 9, 2026: 2}
# a cap-sized mover in 2021 and 2024, a floor-sized mover in 2022 and 2024
CAP_ROUNDS = {2021, 2024}
FLOOR_ROUNDS = {2022, 2024}
EXCLUDE_ROLES = {"unfiled_steady", "young"}


def eligible_pool(orgs, round_year):
    out = []
    for o in orgs:
        if o.role not in ("steady", "deadline_steady", "entrant", "exit"):
            continue
        if o.short_form:
            continue
        # scored at the round: first return by the prior window's start, grant still current
        if o.first_q > Q(round_year - 2, 3):
            continue
        if o.last_q < Q(round_year, 3) + 1:
            continue
        if o.role == "exit" and o.last_q < Q(round_year, 6):
            continue
        out.append(o)
    return out


def assign_movers(orgs):
    rng = np.random.default_rng([SEED, 11])
    used_years = {}
    for ry in sorted(GENERIC):
        pool = [o for o in eligible_pool(orgs, ry)
                if all(abs(ry - y) >= 2 for y in used_years.get(o.key, []))]
        pool.sort(key=lambda o: o.key)
        n = GENERIC[ry]
        picks = []
        if ry in CAP_ROUNDS:
            big = sorted([o for o in pool if o.income > 2_200_000], key=lambda o: o.key)
            if not big:
                big = sorted(pool, key=lambda o: -o.income)[:1]
            picks.append((big[int(rng.integers(0, len(big)))], "cap"))
        if ry in FLOOR_ROUNDS:
            small = sorted([o for o in pool if 190_000 < o.income < 290_000 and o not in
                            [p for p, _ in picks]], key=lambda o: o.key)
            picks.append((small[int(rng.integers(0, len(small)))], "floor"))
        rest = [o for o in pool if o not in [p for p, _ in picks]
                and 500_000 < o.income < 1_500_000]
        idx = rng.permutation(len(rest))
        for j in idx[: n - len(picks)]:
            picks.append((rest[int(j)], "mid"))
        for o, kind in picks:
            if kind == "cap":
                depth = float(rng.uniform(0.26, 0.30))
            elif kind == "floor":
                depth = float(rng.uniform(0.17, 0.19))
            else:
                depth = float(rng.uniform(0.17, 0.31))
            for q in yr_quarters(ry - 1):
                o.dips[q] = o.dips.get(q, 1.0) * (1 - depth)
            o.notes.append(f"corpus mover {ry} ({kind}, {depth:.3f})")
            if o.role == "steady" or o.role == "deadline_steady" or o.role == "entrant" or o.role == "exit":
                o.sigma = min(o.sigma, 0.012)
            used_years.setdefault(o.key, []).append(ry)
    return orgs


def assign_short_form(orgs):
    """Small steady grantees that file the short form (total and two lines)."""
    rng = np.random.default_rng([SEED, 12])
    cands = sorted([o for o in orgs if o.role in ("steady", "entrant", "deadline_steady")
                    and o.income < 330_000 and not o.notes], key=lambda o: o.key)
    pick = rng.permutation(len(cands))[:25]
    for j in pick:
        cands[int(j)].short_form = True
    return orgs
