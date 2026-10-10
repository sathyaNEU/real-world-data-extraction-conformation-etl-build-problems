"""The resident and nonresident population of the scaled state, TY2022 to TY2025.

A persistent panel of household entities (a federal filing unit and the people it claims) with
persistent TINs, kinds, counties and dependents; each year's own AGI comes from that year's
marginal by rank of a persistent latent score, so incomes are correlated year to year.

Everything the ladder needs is built here and asserted in build.py:
  * TY2025 floors pinned by construction (the rank-k unit and its neighbours sit inside
    [F - 250, F + 250) at a non-round offset, nothing in the gap),
  * dependents' own returns attached only through the claimant's schedule,
  * the trust group (TY2025: 1,475 households, 976 crossing the top-1% mark),
  * the conveyor (N households crossing $100K, $200K, $300K and $500K on their children's income,
    with the attached income of households that stay in each class balancing the boundary flows
    to the dollar, so filing units tie every class cell outside $500K to $1M),
  * the TY2024 twin pair (Kessler and Abington).
Internal labels live in columns that start with an underscore and are never shipped.
"""
import math

import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator

from common import (YEARS, k_top, stream, make_tins, make_itins)

# ------------------------------------------------------------------ fixed targets

N_HH_2025 = 582_544
N_SEP_2025, N_SEP_TOP_2025 = 41_862, 29_722
N_DEPRET_2025 = 94_807
N_DEPRET = {2022: 90_961, 2023: 92_247, 2024: 93_558, 2025: N_DEPRET_2025}
N_C2 = {2022: 22_917, 2023: 23_406, 2024: 23_958, 2025: 24_281}
N_C3 = {2022: 104_388, 2023: 106_271, 2024: 108_114, 2025: 109_453}
TRUST = {2022: (1_066, 1_684), 2023: (1_163, 1_837), 2024: (1_552, 2_453), 2025: (1_475, 2_350)}
TRUST_CROSS_2025 = 976
CONVEYOR_N = {2022: 23, 2023: 10, 2024: 30, 2025: 30}
YEAR_F = {2022: 0.948, 2023: 0.992, 2024: 1.061, 2025: 1.000}
BULK_MEDIAN = {2022: 8_900, 2023: 9_100, 2024: 9_800, 2025: 9_300}
RHO = 0.95
NR_MEDIAN, NR_SIGMA, NR_TAIL_P, NR_TAIL_A = 69_000, 0.46, 0.0068, 3.4

# entity churn (resident households): active spans
SPANS = [  # (first, last, count)
    (2022, 2025, 495_591), (2023, 2025, 27_384), (2024, 2025, 28_951), (2025, 2025, 30_618),
    (2022, 2024, 23_117), (2022, 2023, 21_846), (2022, 2022, 20_958), (2023, 2024, 1_203),
]

# TY2025 pinned floors: (floor, k, basis) with basis 'own' (household own AGI = filing unit AGI)
# or 'total' (household AGI with dependents' returns attached).
PIN_OWN = [(197_000, 67_736), (214_000, 58_255), (293_000, 33_868), (318_000, 29_128),
           (594_000, 6_774), (657_000, 5_826)]
PIN_742 = (742_000, 4_850)      # own pool count at or above $742,000; 976 trust crossers on top
ANSWER_PINS = (214_000, 318_000, 742_000)

# counties: twelve named (the appendix set) and sixty-three by code only
BIG12 = [  # name, code, share of resident households, affluence
    ("Marston", "071", 0.140, 1.30), ("Corwin", "089", 0.090, 1.55), ("Fenwick", "113", 0.070, 1.15),
    ("Brackett", "019", 0.055, 1.00), ("Hollowell", "097", 0.046, 1.22), ("Ellery", "045", 0.040, 0.92),
    ("Dunmore", "031", 0.036, 1.00), ("Kessler", "061", 0.033, 0.88), ("Abington", "003", 0.032, 0.86),
    ("Wexley", "135", 0.030, 1.08), ("Garrow", "053", 0.028, 0.90), ("Tillson", "127", 0.026, 0.80),
]
KESSLER, ABINGTON = "061", "003"
TWIN_FFU_500 = 287
TWIN_CROSS = {"061": 14, "071": 4, "089": 3, "113": 3, "097": 2}   # TY2024 $500K crossers by county
TWIN_CROSS_ELSEWHERE = 4
UNIVERSITY_COUNTIES = ("045", "119", "071", "017")

ALL_COUNTY_CODES = [f"{c:03d}" for c in range(1, 150, 2)]


def county_table():
    big = {c: (n, s, a) for n, c, s, a in BIG12}
    rng = stream("counties")
    others = [c for c in ALL_COUNTY_CODES if c not in big]
    rest_share = 1.0 - sum(s for _, _, s, _ in BIG12)
    w = rng.pareto(1.6, len(others)) + 0.35
    w = w / w.sum() * rest_share
    w = np.minimum(w, 0.0165)
    w = w / w.sum() * rest_share
    aff = np.clip(rng.normal(0.72, 0.12, len(others)), 0.45, 1.05)
    rows = []
    for c in ALL_COUNTY_CODES:
        if c in big:
            n, s, a = big[c]
            rows.append((c, n, s, a))
        else:
            i = others.index(c)
            rows.append((c, "", float(w[i]), float(aff[i])))
    return pd.DataFrame(rows, columns=["code", "name", "share", "aff"])


# ------------------------------------------------------------------ income pools

BODY_2025 = [  # x, S (households at or above x), TY2025
    (60_000_000, 1), (25_000_000, 14), (10_000_000, 98), (5_000_000, 277), (2_000_000, 1_096),
    (1_500_000, 1_687), (1_000_000, 3_100), (742_000, 4_850), (657_000, 5_826), (594_000, 6_774),
    (500_000, 10_093), (400_000, 16_822), (318_000, 29_128), (293_000, 33_868), (250_000, 44_470),
    (214_000, 58_255), (197_000, 67_736), (150_000, 99_200), (125_000, 127_400), (100_000, 163_500),
    (75_000, 228_000), (50_000, 318_000), (30_000, 405_000), (15_000, 478_000), (5_000, 545_000),
]
N_ZERO_2025, N_NEG_2025 = 1_212, 3_537


def survival_inverse(anchors, n_pos):
    """Tabulated survival function through the anchors: PCHIP in log x / log S at and above the
    $100,000 anchor (scaled for prior years) and in x / S below it. Returns (x grid ascending,
    S on the grid, strictly decreasing), exact at every anchor."""
    xs = np.array([a[0] for a in anchors] + [1.0], dtype=np.float64)
    ss = np.array([a[1] for a in anchors] + [n_pos], dtype=np.float64)
    order = np.argsort(xs)
    xs, ss = xs[order], ss[order]
    split = xs[np.argmin(np.abs(xs - 100_000 * xs.max() / 60_000_000))]
    hi = xs >= split
    lo = xs <= split
    f_hi = PchipInterpolator(np.log(xs[hi]), np.log(ss[hi]))
    f_lo = PchipInterpolator(xs[lo], ss[lo])

    def interior(grid):
        keep = np.ones(len(grid), bool)
        for x in xs:
            keep &= np.abs(grid - x) > 1e-6 * x
        return grid[keep]

    g_hi = interior(np.exp(np.linspace(np.log(split), np.log(xs.max()), 60_000)))
    g_hi = g_hi[(g_hi > split) & (g_hi < xs.max())]
    g_lo = interior(np.linspace(1.0, split, 60_000))
    g_lo = g_lo[(g_lo > 1.0) & (g_lo < split)]
    gx = np.concatenate([xs, g_hi, g_lo])
    gs = np.concatenate([ss, np.exp(f_hi(np.log(g_hi))), f_lo(g_lo)])
    o = np.argsort(gx)
    gx, gs = gx[o], gs[o]
    assert np.all(np.diff(gx) > 0)
    assert np.all(np.diff(gs) < 0), "survival not strictly decreasing"
    return gx, gs


def draw_pool(anchors, n, n_zero, n_neg, rng, neg_scale=1.0):
    """Descending integer AGI values for n households: exact counts at every anchor."""
    n_pos = n - n_zero - n_neg
    gx, gs = survival_inverse(anchors, n_pos)
    u = rng.random(n_pos)
    s = np.arange(1, n_pos + 1, dtype=np.float64) - u
    s[0] = max(s[0], 0.6)
    # x(s): gs is decreasing in gx; interpolate on reversed arrays (ascending s)
    x = np.interp(s, gs[::-1], gx[::-1])
    top = s < gs[-1]                      # above the top anchor: extend the last log slope
    if top.any():
        sl = (np.log(gx[-1]) - np.log(gx[-2])) / (np.log(gs[-1]) - np.log(gs[-2]))
        x[top] = np.exp(np.log(gx[-1]) + (np.log(s[top]) - np.log(gs[-1])) * sl)
    pos = np.floor(x).astype(np.int64)
    pos = np.maximum(pos, 1)
    neg = -np.minimum(np.round(np.exp(rng.normal(math.log(9_000 * neg_scale), 1.35, n_neg))), 2_400_000).astype(np.int64)
    neg = np.maximum(neg, -2_400_000)
    neg[neg == 0] = -1
    vals = np.concatenate([pos, np.zeros(n_zero, dtype=np.int64), np.sort(neg)[::-1]])
    return vals


def apply_pin(vals, F, k, rng, own_ranks_taken, gap=(36, 97)):
    """Pin the floor F at rank k (1-based, descending): ranks k-2..k inside (F, F+250), ranks
    k+1, k+2 inside [F-250, F), all distinct, at non-round offsets, and nothing in between. Values
    above and below are pushed out monotonically. Returns the five boundary values."""
    a = int(rng.integers(gap[0], gap[1]))
    b = int(rng.integers(gap[0], gap[1]))
    d1, d2, d3 = (int(x) for x in rng.integers(4, 23, 3))
    i = k - 1                                  # 0-based index of rank k
    vals[i] = F + a
    vals[i - 1] = F + a + d1
    vals[i - 2] = F + a + d1 + d2
    vals[i + 1] = F - b
    vals[i + 2] = F - b - d3
    assert vals[i - 2] < F + 250 and vals[i + 2] >= F - 250
    j = i - 3
    while j >= 0 and vals[j] <= vals[j + 1]:
        vals[j] = vals[j + 1] + 1
        j -= 1
    j = i + 3
    while j < len(vals) and vals[j] >= vals[j - 1]:
        vals[j] = vals[j - 1] - 1
        j += 1
    own_ranks_taken.update(range(k - 2, k + 3))
    return [int(vals[r - 1]) for r in range(k - 2, k + 3)]


def pool_2025(rng):
    vals = draw_pool(BODY_2025, N_HH_2025, N_ZERO_2025, N_NEG_2025, rng)
    for x, s in BODY_2025:
        assert (vals >= x).sum() == s, ("anchor", x, s, (vals >= x).sum())
    taken = set()
    pins = {}
    for F, k in PIN_OWN + [PIN_742]:
        pins[F] = apply_pin(vals, F, k, rng, taken)
    assert np.all(np.diff(vals) <= 0)
    return vals, pins


def pool_prior(year, n, rng):
    f = YEAR_F[year]
    sc = n / N_HH_2025
    anchors = []
    last = 0
    for x, s in BODY_2025:
        v = max(int(round(s * sc)), last + 1)
        anchors.append((x * f, v))
        last = v
    n_zero = int(round(N_ZERO_2025 * sc * 1.01))
    n_neg = int(round(N_NEG_2025 * sc * (1.0 + (2025 - year) * 0.03)))
    return draw_pool(anchors, n, n_zero, n_neg, rng, neg_scale=f)


# ------------------------------------------------------------------ the world


class World:
    pass


def active_mask(W, y):
    return (W.first <= y) & (W.last >= y)


def build_entities(W):
    rng = stream("entities")
    first, last = [], []
    for f, l, c in SPANS:
        first.append(np.full(c, f, np.int16))
        last.append(np.full(c, l, np.int16))
    W.first = np.concatenate(first)
    W.last = np.concatenate(last)
    perm = rng.permutation(len(W.first))
    W.first, W.last = W.first[perm], W.last[perm]
    W.n = len(W.first)
    W.z = rng.normal(0, 1, W.n)
    W.eps = {y: rng.normal(0, 1, W.n) for y in YEARS}
    for y in YEARS:
        pass
    W.n_hh = {y: int(active_mask(W, y).sum()) for y in YEARS}
    assert W.n_hh[2025] == N_HH_2025


def assign_incomes(W):
    W.own = {}
    W.rank = {}
    W.pins = None
    for y in YEARS:
        act = np.where(active_mask(W, y))[0]
        score = RHO * W.z[act] + math.sqrt(1 - RHO ** 2) * W.eps[y][act]
        order = act[np.argsort(-score, kind="stable")]
        if y == 2025:
            vals, pins = pool_2025(stream("pool2025"))
            W.pins = pins
        else:
            vals = pool_prior(y, len(act), stream(f"pool{y}"))
        own = np.zeros(W.n, dtype=np.int64)
        own[order] = vals
        rank = np.zeros(W.n, dtype=np.int64)
        rank[order] = np.arange(1, len(order) + 1)
        W.own[y] = own
        W.rank[y] = rank
    # TY2025 boundary households (by own rank): never special, never attached, no ask records
    W.boundary = {}
    r25 = W.rank[2025]
    by_rank = np.zeros(N_HH_2025 + 1, dtype=np.int64)
    a25 = np.where(active_mask(W, 2025))[0]
    by_rank[r25[a25]] = a25
    W.by_rank_2025 = by_rank
    for F, k in PIN_OWN + [PIN_742]:
        W.boundary[F] = [int(by_rank[r]) for r in range(k - 2, k + 3)]
    W.excluded_2025 = np.zeros(W.n, bool)
    for F in W.boundary:
        W.excluded_2025[W.boundary[F]] = True
    # a margin of ten ranks either side of each own pin stays clear of attached income too
    for F, k in PIN_OWN + [PIN_742]:
        W.excluded_2025[by_rank[max(1, k - 12):k + 13]] = True


def assign_kinds(W):
    """Kinds: 0 single, 1 joint, 2 separate state returns, 3 head of household, 4 surviving
    spouse. Married and separate shares rise with income; the TY2025 separate count and its
    top-two-decile share are exact."""
    rng = stream("kinds")
    n = W.n
    # income quantile for the kind draw: TY2025 rank where active, else the latest year's rank
    q = np.zeros(n)
    for y in YEARS:
        act = active_mask(W, y)
        q[act] = 1.0 - (W.rank[y][act] - 1) / W.n_hh[y]
    p_married = np.interp(q, [0.0, 0.3, 0.5, 0.8, 0.95, 1.0], [0.22, 0.36, 0.50, 0.70, 0.80, 0.84])
    married = rng.random(n) < p_married
    kind = np.zeros(n, np.int8)
    kind[married] = 1
    # separate couples: exact for TY2025-active entities
    a25 = active_mask(W, 2025)
    n_ffu_2025 = N_HH_2025 + N_DEPRET_2025
    k20 = k_top(n_ffu_2025, 20)
    W.k20_2025 = k20
    top = a25 & (W.rank[2025] <= k20) & married
    low = a25 & (W.rank[2025] > k20) & married & (W.own[2025] > 15_000)
    top_i = np.where(top)[0]
    low_i = np.where(low)[0]
    # separate filing rises with income inside the top group
    wt = 0.5 + (k20 - W.rank[2025][top_i]) / k20
    sel_top = rng.choice(top_i, N_SEP_TOP_2025, replace=False, p=wt / wt.sum())
    sel_low = rng.choice(low_i, N_SEP_2025 - N_SEP_TOP_2025, replace=False)
    kind[sel_top] = 2
    kind[sel_low] = 2
    # entities not active in 2025: same propensity
    gone = (~a25) & married
    p_sep = np.interp(q[gone], [0.0, 0.8, 1.0], [0.03, 0.05, 0.27])
    gi = np.where(gone)[0]
    kind[gi[rng.random(len(gi)) < p_sep]] = 2
    W.kind = kind
    W.sep_share = np.clip(rng.uniform(0.52, 0.78, n), 0.5, 0.85)
    W.sep_share_y = {yy: np.clip(W.sep_share + stream(f"split{yy}").normal(0, 0.025, n), 0.5, 0.85)
                     for yy in YEARS}


def assign_dependents(W):
    rng = stream("dependents")
    n = W.n
    kind = W.kind
    unmarried = kind == 0
    q = np.zeros(n)
    for y in YEARS:
        act = active_mask(W, y)
        q[act] = 1.0 - (W.rank[y][act] - 1) / W.n_hh[y]
    # HOH among unmarried: more common at lower incomes
    p_hoh = np.interp(q, [0, 0.4, 0.8, 1.0], [0.33, 0.33, 0.16, 0.06])
    hoh = unmarried & (rng.random(n) < p_hoh)
    qss = unmarried & ~hoh & (rng.random(n) < 0.004)
    kind = kind.copy()
    kind[hoh] = 3
    kind[qss] = 4
    W.kind = kind
    married = (kind == 1) | (kind == 2)
    has = np.zeros(n, bool)
    p_kids = np.interp(q, [0.0, 0.5, 0.85, 0.97, 1.0], [0.52, 0.50, 0.56, 0.63, 0.66])
    has[married] = rng.random(married.sum()) < p_kids[married]
    has[(kind == 3) | (kind == 4)] = True
    single = kind == 0
    has[single] = rng.random(single.sum()) < 0.045
    nd = np.zeros(n, np.int64)
    nd[has] = 1 + np.minimum(rng.poisson(0.9, has.sum()), 4)
    nd[single & has] = 1
    W.dep_start = np.concatenate([[0], np.cumsum(nd)[:-1]])
    W.dep_n = nd
    tot = int(nd.sum())
    owner = np.repeat(np.arange(n), nd)
    W.dep_owner = owner
    # relationship: children for married/HOH/QSS, relatives for singles and a share of others
    rel = np.full(tot, "01", dtype="<U2")
    r = rng.random(tot)
    rel[r > 0.86] = "02"
    rel[(r > 0.93)] = "04"
    rel[(r > 0.955)] = "03"
    rel[(r > 0.965)] = "05"
    rel[(r > 0.985)] = "06"
    rel[(r > 0.993)] = "07"
    sing = kind[owner] == 0
    rs = rng.random(sing.sum())
    rel[sing] = np.where(rs < 0.55, "05", np.where(rs < 0.75, "07", np.where(rs < 0.9, "06", "08")))
    W.dep_rel = rel
    # birth years: children 2002-2025, parents and relatives earlier
    child = np.isin(rel, ["01", "02", "03", "04"])
    by = np.empty(tot, np.int64)
    by[child] = 2025 - np.floor(27 * rng.beta(1.3, 1.1, child.sum())).astype(np.int64)
    by[~child] = rng.integers(1928, 1990, (~child).sum())
    W.dep_by = by
    W.dep_side = (rng.random(tot) < 0.38).astype(np.int8)   # separate couples: spouse's return
    W.n_dep = tot


def make_tin_space(W):
    rng = stream("tins")
    n_need = W.n * 2 + W.n_dep + 400_000
    pool = make_tins(rng, n_need)
    i = 0
    W.tin_p = pool[i:i + W.n]; i += W.n
    W.tin_s = np.where((W.kind == 1) | (W.kind == 2), pool[i:i + W.n], 0); i += W.n
    W.dep_tin = pool[i:i + W.n_dep]; i += W.n_dep
    W.spare_tins = pool[i:]
    # a few residents file with ITINs
    it = make_itins(rng, 3_000, pool)
    sel = rng.choice(W.n, 3_000, replace=False)
    W.tin_p[sel] = it


def child_eligible(W, y, min_age):
    """Per dependent: a child of the claimant (codes 01-03), born by year y - min_age, already born."""
    return np.isin(W.dep_rel, ["01", "02", "03"]) & (W.dep_by <= y - min_age) & (W.dep_by >= y - 23)


def kids_of(W, e):
    s = W.dep_start[e]
    return np.arange(s, s + W.dep_n[e])


def assign_counties(W):
    ct = county_table()
    W.county_table = ct
    rng = stream("county_assign")
    n = W.n
    q = np.zeros(n)
    cnt = np.zeros(n)
    for y in YEARS:
        act = active_mask(W, y)
        q[act] += 1.0 - (W.rank[y][act] - 1) / W.n_hh[y]
        cnt[act] += 1
    q = q / np.maximum(cnt, 1)
    codes = ct.code.to_numpy()
    share = ct.share.to_numpy()
    aff = ct.aff.to_numpy()
    county = np.empty(n, dtype="<U3")
    bins = np.minimum((q * 40).astype(int), 39)
    for b in range(40):
        idx = np.where(bins == b)[0]
        qq = (b + 0.5) / 40
        expo = max(0.0, (qq - 0.55) / 0.45) * 3.2
        w = share * aff ** expo
        w = w / w.sum()
        county[idx] = rng.choice(codes, len(idx), p=w)
    W.county = county
    # TY2024 twin: exactly 287 households at or above $500,000 in Kessler and in Abington
    y = 2024
    act = active_mask(W, y)
    hi = act & (W.own[y] >= 500_000)
    others = [c for c in codes if c not in TWIN_CROSS and c != ABINGTON]
    for c in (KESSLER, ABINGTON):
        cur = np.where(hi & (W.county == c))[0]
        if len(cur) > TWIN_FFU_500:
            mv = rng.choice(cur, len(cur) - TWIN_FFU_500, replace=False)
            W.county[mv] = rng.choice([o for o in others if o != KESSLER], len(mv))
        elif len(cur) < TWIN_FFU_500:
            pool = np.where(hi & ~np.isin(W.county, list(TWIN_CROSS) + [ABINGTON]))[0]
            mv = rng.choice(pool, TWIN_FFU_500 - len(cur), replace=False)
            W.county[mv] = c
    # TY2024 $500K crossers need candidates in their designated counties
    elig = child_eligible(W, y, 3)
    has_child = np.zeros(n, bool)
    np.logical_or.at(has_child, W.dep_owner[elig], True)
    band = act & (W.own[y] >= 482_000) & (W.own[y] < 499_600) & has_child & (W.kind != 2)
    for c, need in TWIN_CROSS.items():
        cur = np.where(band & (W.county == c))[0]
        want = need + 6
        if len(cur) < want:
            pool = np.where(band & ~np.isin(W.county, list(TWIN_CROSS) + [ABINGTON]))[0]
            mv = rng.choice(pool, want - len(cur), replace=False)
            W.county[mv] = c
    W.has_child_any = has_child


# ------------------------------------------------------------------ special groups per year

def pick(rng, cand, k, p=None):
    cand = np.asarray(cand)
    assert len(cand) >= k, ("not enough candidates", len(cand), k)
    if p is None:
        return np.sort(rng.choice(cand, k, replace=False))
    p = np.asarray(p, dtype=float)
    return np.sort(rng.choice(cand, k, replace=False, p=p / p.sum()))


def special_groups(W, y):
    """Trust households, conveyor crossers and balancing stayers for year y. Fills W.kid_agi[y]
    (per dependent, 0 = does not file) and W.special[y] (per entity label)."""
    rng = stream(f"special{y}")
    n = W.n
    own = W.own[y]
    act = active_mask(W, y)
    kid = np.zeros(W.n_dep, dtype=np.int64)
    label = np.zeros(n, dtype="<U12")
    excl = W.excluded_2025 if y == 2025 else np.zeros(n, bool)
    elig3 = child_eligible(W, y, 3)
    elig14 = child_eligible(W, y, 14)
    cnt3 = np.bincount(W.dep_owner[elig3], minlength=n)
    cnt14 = np.bincount(W.dep_owner[elig14], minlength=n)
    free = act & ~excl

    def kids(e, need, ages=3):
        ds = kids_of(W, e)
        ok = ds[(elig3 if ages == 3 else elig14)[ds]]
        return ok

    def set_kids(e, amounts, ages=3):
        ok = kids(e, len(amounts), ages)
        assert len(ok) >= len(amounts), (e, len(ok), len(amounts))
        ch = rng.choice(ok, len(amounts), replace=False)
        for d, a in zip(ch, amounts):
            kid[d] = int(a)

    # ---- conveyor crossers
    N = CONVEYOR_N[y]
    conv = {}
    bands = {500_000: (482_000, 499_600, 500_060, 513_500), 300_000: (295_200, 299_820, 300_040, 311_000),
             200_000: (198_300, 199_880, 200_030, 209_000), 100_000: (93_000, 99_850, 100_030, 109_000)}
    for T, (lo, hi, tlo, thi) in bands.items():
        cand_mask = free & (own >= lo) & (own < hi) & (cnt3 >= 1) & (label == "")
        if y == 2024 and T == 500_000:
            chosen = []
            for c, need in TWIN_CROSS.items():
                cc = np.where(cand_mask & (W.county == c))[0]
                chosen.append(pick(rng, cc, need))
            appendix = [b[1] for b in BIG12]
            cc = np.where(cand_mask & ~np.isin(W.county, appendix))[0]
            chosen.append(pick(rng, cc, TWIN_CROSS_ELSEWHERE))
            sel = np.sort(np.concatenate(chosen))
        else:
            sel = pick(rng, np.where(cand_mask)[0], N)
        tots = []
        for e in sel:
            target = int(rng.uniform(tlo, thi))
            need = target - own[e]
            m = 1 if (need < 18_000 or cnt3[e] == 1) else 2
            if m == 1:
                set_kids(e, [need])
            else:
                a = int(need * rng.uniform(0.35, 0.65))
                set_kids(e, [a, need - a])
            label[e] = f"cross{T // 1000}"
            tots.append(own[e] + need)
        conv[T] = (sel, np.array(tots, dtype=np.int64))
    W.conv = getattr(W, "conv", {})
    W.conv[y] = conv

    # ---- trust households
    n_trust, n_trust_kids = TRUST[y]
    cand = np.where(free & (own >= 520_000) & (own < 742_000) & (cnt3 >= 1) & (label == ""))[0]
    if y == 2025:
        trust, amts = _trust_2025(rng, cand, own, cnt3, n_trust, n_trust_kids)
    else:
        wts = 0.15 + ((own[cand] - 520_000) / 222_000.0) ** 1.6
        trust = pick(rng, cand, n_trust, wts)
        cap = np.minimum(cnt3[trust], 3)
        m = np.ones(n_trust, dtype=np.int64)
        extra = n_trust_kids - n_trust
        assert int(cap.sum()) >= n_trust_kids, (y, int(cap.sum()), n_trust_kids)
        while extra > 0:
            i = int(rng.integers(0, n_trust))
            if m[i] < cap[i]:
                m[i] += 1
                extra -= 1
        amts = {}
        for e, mm in zip(trust, m):
            a = [int(30_000 + 69_500 * rng.beta(2.2, 1.35)) for _ in range(mm)]
            if own[e] + sum(a) > 985_000:
                a = _spread(int(rng.uniform(own[e] + 30_000 * mm, min(985_000, own[e] + 99_500 * mm))) - own[e], mm, rng)
            amts[e] = a
    for e in trust:
        assert own[e] + sum(amts[e]) <= 990_000
        set_kids(e, amts[e])
        label[e] = "trust"
    W.trust = getattr(W, "trust", {})
    W.trust[y] = trust

    # ---- balancing stayers: attached income of households that stay in each class
    targets = {
        100_000: int(own[conv[200_000][0]].sum() - conv[100_000][1].sum()),
        200_000: int(own[conv[300_000][0]].sum() - conv[200_000][1].sum()),
        300_000: int(own[conv[500_000][0]].sum() - conv[300_000][1].sum()),
    }
    sbands = {100_000: (104_000, 186_000, 189_000), 200_000: (222_000, 284_000, 288_000),
              300_000: (326_000, 470_000, 478_000)}
    W.stay = getattr(W, "stay", {})
    W.stay[y] = {}
    for L, tgt in targets.items():
        lo, hi, top = sbands[L]
        assert tgt > 0, (y, L, tgt)
        cand_mask = free & (own >= lo) & (own < hi) & (cnt3 >= 1) & (label == "")
        chosen, amounts = [], []
        remaining = tgt
        if y == 2024 and L == 300_000:
            # Abington's comparable dependents: custodial income, claimed lower down
            ab = np.where(cand_mask & (W.county == ABINGTON) & (own < 440_000))[0]
            ks = conv[500_000][0][W.county[conv[500_000][0]] == KESSLER]
            ref = [int(kid[kids_of(W, e)].sum()) for e in ks]
            sel = pick(rng, ab, len(ref))
            for e, a in zip(sel, ref):
                a = int(a * rng.uniform(0.9, 1.1))
                chosen.append(int(e))
                amounts.append(a)
                remaining -= a
                label[e] = "stay_ab"
            cand_mask &= label == ""
        cand = np.where(cand_mask)[0]
        rng.shuffle(cand)
        ci = 0
        while remaining > 0:
            e = int(cand[ci])
            ci += 1
            room = int(top - own[e] - 50)
            a = int(min(room, np.exp(rng.normal(math.log(9_500), 0.6))))
            if a < 700:
                continue
            if a >= remaining:
                a = remaining
            elif remaining - a < 700:
                a = remaining - 700 if remaining - 700 >= 700 else remaining
                if a > room:
                    a = room
            chosen.append(e)
            amounts.append(a)
            label[e] = f"stay{L // 1000}"
            remaining -= a
        assert remaining == 0 and min(amounts) >= 300, (y, L, remaining, min(amounts))
        for e, a in zip(chosen, amounts):
            set_kids(e, [a])
            assert own[e] + a < top, (e, own[e], a)
        W.stay[y][L] = np.array(sorted(chosen))
    W.kid_agi = getattr(W, "kid_agi", {})
    W.kid_agi[y] = kid
    W.special = getattr(W, "special", {})
    W.special[y] = label


def _trust_2025(rng, cand, own, cnt3, n_trust, n_kids):
    """TY2025 trust group: n_trust households, n_kids children with trust and investment income of
    $30,000 to $99,500 each, exactly 976 households crossing $742,000 on it. Every crosser's total
    sits in [$744,000, $989,000] and every other trust total at or under $738,000, so no trust
    total comes near the window around the floor."""
    cap = np.minimum(cnt3[cand], 3)
    need = np.ceil((746_000 - own[cand]) / 99_500).astype(int)       # children a crosser needs
    can_cross = need <= cap
    w_cross = np.where(can_cross, 0.2 + ((own[cand] - 520_000) / 222_000.0) ** 1.2, 0.0)
    cross = rng.choice(cand, TRUST_CROSS_2025, replace=False, p=w_cross / w_cross.sum())
    rest_pool = np.setdiff1d(cand, cross)
    rest_pool = rest_pool[own[rest_pool] + 30_000 <= 738_000]
    w_rest = 0.3 + ((own[rest_pool] - 520_000) / 222_000.0) ** 1.6
    stay = rng.choice(rest_pool, n_trust - TRUST_CROSS_2025, replace=False, p=w_rest / w_rest.sum())
    trust = np.sort(np.concatenate([cross, stay]))
    pos = {int(e): i for i, e in enumerate(cand)}
    m = {}
    for e in cross:
        m[int(e)] = int(need[pos[int(e)]])
    for e in stay:
        m[int(e)] = 1
    extra = n_kids - sum(m.values())
    assert extra >= 0, extra
    order = list(rng.permutation(trust))
    guard = 0
    while extra > 0:
        e = int(order[guard % len(order)])
        guard += 1
        c = int(cap[pos[e]])
        if m[e] < c and (e in set(cross.tolist()) or own[e] + 30_000 * (m[e] + 1) <= 738_000):
            if rng.random() < 0.5:
                m[e] += 1
                extra -= 1
        assert guard < 200_000, "trust children could not be placed"
    amts = {}
    cross_set = set(int(e) for e in cross)
    for e in trust:
        e = int(e)
        k = m[e]
        if e in cross_set:
            hi = min(989_000, own[e] + 99_500 * k)
            lo = max(744_000, own[e] + 30_000 * k)
            tgt = int(lo + (hi - lo) * rng.beta(1.3, 2.2))
        else:
            hi = min(738_000, own[e] + 99_500 * k)
            lo = own[e] + 30_000 * k
            tgt = int(lo + (hi - lo) * rng.beta(2.0, 1.6))
        amts[e] = _spread(tgt - int(own[e]), k, rng)
    return trust, amts


def _spread(total, m, rng):
    """Split total over m children, each between $30,000 and $99,500."""
    assert 30_000 * m <= total <= 99_500 * m, (total, m)
    if m == 1:
        return [int(total)]
    for _ in range(200):
        w = rng.dirichlet(np.ones(m) * 4)
        a = [int(30_000 + (total - 30_000 * m) * x) for x in w]
        a[-1] = int(total - sum(a[:-1]))
        if all(30_000 <= v <= 99_500 for v in a):
            return a
    base = total // m
    a = [base] * m
    a[-1] = total - base * (m - 1)
    return a


def bulk_dependents(W, y, target_total=None):
    """Filing dependents outside the designed groups: children aged 14 to 23 in households whose
    own AGI and total both stay under $100,000 (realism debt 1)."""
    rng = stream(f"bulk{y}")
    kid = W.kid_agi[y]
    act = active_mask(W, y)
    own = W.own[y]
    label = W.special[y]
    elig = child_eligible(W, y, 14) & (kid == 0)
    owner = W.dep_owner
    ok_hh = act & (label == "") & (own < 96_000)
    if y == 2025:
        ok_hh &= ~W.excluded_2025
    cand = np.where(elig & ok_hh[owner])[0]
    age = y - W.dep_by[cand]
    p = np.interp(age, [14, 15, 16, 17, 18, 19, 20, 21, 22, 23], [0.25, 0.42, 0.62, 0.78, 0.86, 0.86, 0.8, 0.74, 0.66, 0.55])
    n_special = int((kid > 0).sum())
    want = (target_total - n_special) if target_total else int(len(cand) * 0.66)
    # draw an order of filing, then accept while each household stays under $100,000
    keys = rng.random(len(cand)) / p
    order = cand[np.argsort(keys, kind="stable")]
    agi = np.round(np.exp(rng.normal(math.log(BULK_MEDIAN[y]), 0.78, len(order)))).astype(np.int64)
    agi = np.clip(agi, 310, 46_000)
    room = (99_400 - own).astype(np.int64)
    taken = 0
    for d, a in zip(order, agi):
        e = owner[d]
        if a <= room[e]:
            kid[d] = a
            room[e] -= a
            taken += 1
            if taken == want:
                break
    assert taken == want, (y, taken, want)


# ------------------------------------------------------------------ nonresidents

def nonresidents(W):
    """Part-year (code 2, a new set every year) and nonresident (code 3, persistent commuters)
    returns: single-return units, no separately filed spouses and no filing dependents."""
    rng = stream("nonres")
    out = {}
    pool3 = make_tins(stream("tins_nr"), 620_000)
    pool3 = pool3[~np.isin(pool3, np.concatenate([W.tin_p, W.tin_s, W.dep_tin]))]
    n3_ent = 150_000
    tins3 = pool3[:n3_ent]
    spouse3 = pool3[n3_ent:2 * n3_ent]
    rest = pool3[2 * n3_ent:]
    z3 = rng.normal(0, 1, n3_ent)
    # spans for commuters: about 9 per cent turnover a year
    first3 = rng.choice([2022, 2023, 2024, 2025], n3_ent, p=[0.76, 0.08, 0.08, 0.08])
    last3 = np.where(rng.random(n3_ent) < 0.84, 2025, rng.choice([2022, 2023, 2024], n3_ent))
    last3 = np.maximum(last3, first3)
    ri = 0
    for y in YEARS:
        f = YEAR_F[y]
        act3 = np.where((first3 <= y) & (last3 >= y))[0]
        need3 = N_C3[y]
        if len(act3) >= need3:
            act3 = np.sort(rng.choice(act3, need3, replace=False))
        else:
            raise AssertionError(("commuter pool short", y, len(act3), need3))
        n2 = N_C2[y]
        n = need3 + n2
        agi = np.exp(rng.normal(math.log(NR_MEDIAN * f), NR_SIGMA, n))
        agi = np.minimum(agi, 480_000 * f)
        tail = rng.random(n) < NR_TAIL_P
        agi[tail] = 500_000 * f * (1 + rng.pareto(NR_TAIL_A, tail.sum()))
        agi[tail] = np.minimum(agi[tail], 990_000 * f)
        agi = np.round(agi).astype(np.int64)
        # every published class at $1M and over holds at least two nonresident returns
        cls = [(1_000_000, 1_500_000), (1_500_000, 2_000_000), (2_000_000, 5_000_000), (5_000_000, 10_000_000), (10_000_000, 40_000_000)]
        slots = rng.choice(np.where(~tail)[0], 2 * len(cls), replace=False)
        for j, (lo, hi) in enumerate(cls):
            for s in slots[2 * j:2 * j + 2]:
                agi[s] = int(rng.uniform(lo * 1.02, hi * 0.97))
        neg = rng.random(n) < 0.004
        agi[neg] = -np.round(np.exp(rng.normal(math.log(6_000), 1.2, neg.sum()))).astype(np.int64)
        res = np.concatenate([np.full(need3, 3, np.int8), np.full(n2, 2, np.int8)])
        tin = np.concatenate([tins3[act3], rest[ri:ri + n2]])
        ri += n2
        married = rng.random(n) < 0.46
        stin = np.where(married, np.concatenate([spouse3[act3], rest[ri:ri + n2]]), 0)
        ri += n2
        status = np.where(married, 2, np.where(rng.random(n) < 0.12, 4, 1)).astype(np.int8)
        county = np.where(res == 3, "000", "000")
        in_state = (res == 2) & (rng.random(n) < 0.55)
        ct = W.county_table
        county = county.astype("<U3")
        county[in_state] = rng.choice(ct.code.to_numpy(), in_state.sum(), p=(ct.share / ct.share.sum()).to_numpy())
        if y == 2024:
            big = [b[1] for b in BIG12]
            hi500 = (res == 2) & (agi >= 500_000)
            county[hi500 & np.isin(county, big)] = "000"
            pool_lo = np.where((res == 2) & (agi >= 120_000) & (agi < 400_000) & (county == "000"))[0]
            pick_i = rng.choice(pool_lo, len(big), replace=False)
            for i, c in zip(pick_i, big):
                agi[i] = int(rng.uniform(505_000, 760_000))
                county[i] = c
        ndep = np.where(rng.random(n) < 0.22, 1 + np.minimum(rng.poisson(0.7, n), 4), 0)
        out[y] = dict(tin=tin, spouse=stin, agi=agi, res=res, status=status, county=county, ndep=ndep)
    W.nonres = out
    dp = make_tins(stream("tins_nrdep"), 300_000)
    used = np.concatenate([W.tin_p, W.tin_s, W.dep_tin, pool3])
    W.nonres_dep_pool = dp[~np.isin(dp, used)]


# ------------------------------------------------------------------ assembly

def build_world():
    W = World()
    build_entities(W)
    assign_incomes(W)
    assign_kinds(W)
    assign_dependents(W)
    make_tin_space(W)
    assign_counties(W)
    for y in YEARS:
        special_groups(W, y)
        bulk_dependents(W, y, N_DEPRET[y])
    twin_adjust(W)
    nonresidents(W)
    return W


def twin_adjust(W):
    """TY2024: Kessler and Abington carry the same count of resident returns at or above $500,000,
    and their dependents' own returns sit within 2 per cent of each other."""
    y = 2024
    rng = stream("twin_adjust")
    act = active_mask(W, y)
    s = W.sep_share_y[y]
    own = W.own[y]

    def returns_500(c):
        e = np.where(act & (W.county == c))[0]
        sep = W.kind[e] == 2
        p = np.where(sep, np.round(own[e] * s[e]), own[e])
        q = np.where(sep, own[e] - np.round(own[e] * s[e]), -1)
        return int((p >= 500_000).sum() + (q >= 500_000).sum())

    def n500(e):
        p = np.round(own[e] * s[e])
        return int(p >= 500_000) + int(own[e] - p >= 500_000)

    for _ in range(400):
        rk, ra = returns_500(KESSLER), returns_500(ABINGTON)
        if rk == ra:
            break
        hi_c = KESSLER if rk > ra else ABINGTON
        lo_c = ABINGTON if rk > ra else KESSLER
        base = act & (W.kind == 2) & (W.special[y] == "")
        done = False
        # lower the larger county by one
        for e in np.where(base & (W.county == hi_c) & (own >= 500_000) & (own < 3_300_000))[0]:
            n0 = n500(e)
            if n0 == 1 and own[e] < 998_000:
                s[e] = 0.5 + (499_000 / own[e] - 0.5) * rng.uniform(0.2, 0.9)
            elif n0 == 2 and own[e] >= 1_000_000:
                s[e] = 1.0 - (499_000 - int(rng.integers(1_000, 60_000))) / own[e]
            else:
                continue
            if 0.5 <= s[e] <= 0.85 and n500(e) == n0 - 1:
                done = True
                break
        if done:
            continue
        # or raise the smaller county by one
        for e in np.where(base & (W.county == lo_c) & (own >= 590_000) & (own < 1_700_000))[0]:
            n0 = n500(e)
            if n0 == 0 and own[e] < 1_000_000:
                s[e] = min(0.85, (500_000 + int(rng.integers(1_000, 30_000))) / own[e])
            elif n0 == 1 and own[e] >= 1_002_000:
                s[e] = 0.5
            else:
                continue
            if 0.5 <= s[e] <= 0.85 and n500(e) == n0 + 1:
                done = True
                break
        if not done:
            raise AssertionError("twin: no couple to adjust")
    assert returns_500(KESSLER) == returns_500(ABINGTON)
    # dependents' returns within 2 per cent (claimant's county)
    kid = W.kid_agi[y]
    for _ in range(4000):
        k = int(((kid > 0) & (W.county[W.dep_owner] == KESSLER)).sum())
        a = int(((kid > 0) & (W.county[W.dep_owner] == ABINGTON)).sum())
        if abs(k - a) <= 0.01 * max(k, a):
            break
        lo_c = KESSLER if k < a else ABINGTON
        hi_c = ABINGTON if k < a else KESSLER
        # move one bulk filer: drop one in the larger county, add one in the smaller
        hi_d = np.where((kid > 0) & (W.county[W.dep_owner] == hi_c) & (W.special[y][W.dep_owner] == ""))[0]
        d = int(rng.choice(hi_d))
        kid[d] = 0
        own_ = W.own[y]
        room = 99_400 - own_ - np.bincount(W.dep_owner, weights=kid, minlength=W.n).astype(np.int64)
        elig = child_eligible(W, y, 14) & (kid == 0) & (W.county[W.dep_owner] == lo_c) & act[W.dep_owner] & (W.special[y][W.dep_owner] == "") & (own_[W.dep_owner] < 96_000)
        cand = np.where(elig & (room[W.dep_owner] > 2_000))[0]
        d2 = int(rng.choice(cand))
        kid[d2] = int(min(room[W.dep_owner[d2]] - 100, max(400, np.exp(rng.normal(math.log(8_000), 0.7)))))


# ------------------------------------------------------------------ return files and schedules

STATUS_OF_KIND = np.array([1, 2, 3, 4, 5], dtype=np.int8)   # single, joint, separate, HOH, QSS
STD_DED = {1: 3_250, 2: 6_500, 3: 3_250, 4: 4_800, 5: 6_500}
EXEMPTION = 2_350


def _processed_dates(rng, y, n, early_share):
    """Processing dates for TY y returns: late January to the October extension deadline."""
    start = np.datetime64(f"{y + 1}-01-27")
    days = np.where(rng.random(n) < early_share,
                    rng.gamma(2.2, 13.0, n),
                    np.where(rng.random(n) < 0.86, rng.gamma(3.0, 17.0, n), 190 + rng.gamma(4.0, 9.0, n)))
    days = np.clip(days, 0, 266).astype(np.int64)
    d = start + days.astype("timedelta64[D]")
    wd = (d.astype("datetime64[D]").view("int64") - 4) % 7     # 0 = Monday
    d = np.where(wd == 5, d + np.timedelta64(2, "D"), np.where(wd == 6, d + np.timedelta64(1, "D"), d))
    return d


def returns_frame(W, y):
    rng = stream(f"assemble{y}")
    act = np.where(active_mask(W, y))[0]
    own = W.own[y]
    kind = W.kind[act]
    s = W.sep_share_y[y]
    rows = {}
    # households: one return, or two for separate state returns
    sep = kind == 2
    agi_p = np.where(sep, np.round(own[act] * s[act]).astype(np.int64), own[act])
    agi_s = own[act] - agi_p
    ent = np.concatenate([act, act[sep]])
    role = np.concatenate([np.full(len(act), "H"), np.full(sep.sum(), "S")])
    filer = np.concatenate([W.tin_p[act], W.tin_s[act][sep]])
    spouse = np.concatenate([np.where(kind == 1, W.tin_s[act], 0), np.zeros(sep.sum(), np.int64)])
    fed = np.concatenate([W.tin_p[act], W.tin_p[act][sep]])
    status = np.concatenate([STATUS_OF_KIND[kind], np.full(sep.sum(), 3, np.int8)])
    agi = np.concatenate([agi_p, agi_s[sep]])
    county = np.concatenate([W.county[act], W.county[act][sep]])
    dep = np.full(len(ent), -1, np.int64)
    # dependents' own returns
    kid = W.kid_agi[y]
    d_idx = np.where(kid > 0)[0]
    d_owner = W.dep_owner[d_idx]
    d_age = y - W.dep_by[d_idx]
    away = (d_age >= 18) & (stream(f"away{y}").random(len(d_idx)) < 0.28)
    d_county = W.county[d_owner].copy()
    d_county[away] = stream(f"awayc{y}").choice(list(UNIVERSITY_COUNTIES), away.sum())
    ent = np.concatenate([ent, d_owner])
    role = np.concatenate([role, np.full(len(d_idx), "D")])
    filer = np.concatenate([filer, W.dep_tin[d_idx]])
    spouse = np.concatenate([spouse, np.zeros(len(d_idx), np.int64)])
    fed = np.concatenate([fed, W.dep_tin[d_idx]])
    status = np.concatenate([status, np.ones(len(d_idx), np.int8)])
    agi = np.concatenate([agi, kid[d_idx]])
    county = np.concatenate([county, d_county])
    dep = np.concatenate([dep, d_idx])
    res = np.ones(len(ent), np.int8)
    # nonresidents
    nr = W.nonres[y]
    m = len(nr["tin"])
    ent = np.concatenate([ent, np.full(m, -1)])
    role = np.concatenate([role, np.full(m, "N")])
    filer = np.concatenate([filer, nr["tin"]])
    spouse = np.concatenate([spouse, nr["spouse"]])
    fed = np.concatenate([fed, nr["tin"]])
    status = np.concatenate([status, nr["status"]])
    agi = np.concatenate([agi, nr["agi"]])
    county = np.concatenate([county, nr["county"]])
    dep = np.concatenate([dep, np.full(m, -1)])
    res = np.concatenate([res, nr["res"]])
    n = len(ent)
    # processing order: separately filed spouses arrive in one envelope, dependents early
    early = np.where(role == "D", 0.7, 0.35)
    pdate = _processed_dates(rng, y, n, early)
    # spouse returns take their primary's date
    hh_ret = {int(e): i for i, e in enumerate(ent[:len(act)])}
    sp = np.where(role == "S")[0]
    pdate[sp] = pdate[[hh_ret[int(e)] for e in ent[sp]]]
    tie = rng.random(n)
    tie[sp] = tie[[hh_ret[int(e)] for e in ent[sp]]] + 1e-9
    order = np.lexsort((tie, pdate))
    gaps = rng.integers(1, 4, n)
    rid = (y % 100) * 100_000_000 + 1_000_000 + int(rng.integers(0, 90_000)) + np.cumsum(gaps)
    return_id = np.empty(n, np.int64)
    return_id[order] = rid
    # state taxable income: AGI less the standard deduction and exemptions on this return
    nclaim = np.zeros(n, np.int64)
    sched = schedule_links(W, y)
    hh_i = {int(e): i for i, e in enumerate(ent[:len(act)])}
    sp_i = {int(e): i for i, e in zip(ent[sp], sp)}
    for e, side in zip(sched["owner"], sched["side"]):
        i = sp_i[e] if (side == 1 and e in sp_i) else hh_i[e]
        nclaim[i] += 1
    nr_claim = nr["ndep"]
    nclaim[len(ent) - m:] = nr_claim
    ded = np.array([STD_DED[int(v)] for v in range(1, 6)])[status - 1]
    pers = np.where(status == 2, 2, 1) * EXEMPTION
    pers = np.where(role == "D", 0, pers)
    taxable = np.maximum(0, agi - ded - pers - nclaim * EXEMPTION)
    df = pd.DataFrame({
        "return_id": return_id,
        "tax_year": np.full(n, y, np.int16),
        "filer_tin": filer.astype(np.int64),
        "spouse_tin": spouse.astype(np.int64),
        "federal_primary_tin": fed.astype(np.int64),
        "filing_status": status,
        "residency_code": res,
        "county_code": county,
        "federal_agi": agi.astype(np.int64),
        "state_taxable_income": taxable.astype(np.int64),
        "overpayment_credit_elect": np.zeros(n, np.int64),
        "processed_date": pdate.astype("datetime64[D]"),
        "_ent": ent.astype(np.int64), "_role": role, "_dep": dep,
    })
    df = df.sort_values("return_id", kind="stable").reset_index(drop=True)
    return df


def schedule_links(W, y):
    """Claimed dependents of resident households in year y: every child aged 0 to 23 and every
    other dependent while the household files."""
    act = active_mask(W, y)
    owner = W.dep_owner
    child = np.isin(W.dep_rel, ["01", "02", "03", "04"])
    age = y - W.dep_by
    ok = act[owner] & np.where(child, (age >= 0) & (age <= 23), True)
    d = np.where(ok)[0]
    side = np.where(W.kind[owner[d]] == 2, W.dep_side[d], 0)
    return {"dep": d, "owner": owner[d], "side": side}


def schedule_frame(W, y, ret):
    rng = stream(f"sched{y}")
    sl = schedule_links(W, y)
    h = ret[ret._role == "H"]
    s = ret[ret._role == "S"]
    hmap = dict(zip(h._ent.to_numpy(), h.return_id.to_numpy()))
    smap = dict(zip(s._ent.to_numpy(), s.return_id.to_numpy()))
    claim = np.array([smap[e] if (side == 1 and e in smap) else hmap[e] for e, side in zip(sl["owner"], sl["side"])], dtype=np.int64)
    df = pd.DataFrame({"claimant_return_id": claim, "dependent_tin": W.dep_tin[sl["dep"]].astype(np.int64),
                       "relationship_code": W.dep_rel[sl["dep"]], "dependent_birth_year": W.dep_by[sl["dep"]].astype(np.int16),
                       "_dep": sl["dep"]})
    # nonresident claimants' dependents (never filers in this file)
    nr = ret[ret._role == "N"]
    nd = W.nonres[y]["ndep"]
    nr_ids = nr.set_index("filer_tin").return_id
    tins = W.nonres[y]["tin"]
    claim_nr = np.repeat(nr_ids.loc[tins].to_numpy(), nd)
    k = len(claim_nr)
    pool = W.nonres_dep_pool
    off = {2022: 0, 2023: 1, 2024: 2, 2025: 3}[y] * 70_000
    dtins = pool[off:off + k]
    assert len(dtins) == k
    rel = rng.choice(["01", "02", "04", "05", "07"], k, p=[0.8, 0.07, 0.03, 0.07, 0.03])
    by = np.where(np.isin(rel, ["01", "02", "04"]), y - rng.integers(0, 22, k), rng.integers(1930, 1975, k))
    df2 = pd.DataFrame({"claimant_return_id": claim_nr, "dependent_tin": dtins.astype(np.int64), "relationship_code": rel,
                        "dependent_birth_year": by.astype(np.int16), "_dep": np.full(k, -1)})
    out = pd.concat([df, df2], ignore_index=True)
    out = out.sort_values(["claimant_return_id", "dependent_birth_year", "dependent_tin"], kind="stable").reset_index(drop=True)
    return out


def break_return_tie(W, y, lo, hi, rng, county=None):
    """Return-grain cells tie a published class cell only by coincidence (separately filed spouses
    moving in and out of the class netting to zero). Move one couple's split so the return-grain
    count of the class changes by one; split shares move return-grain cells only, never a filing
    unit or a household."""
    own = W.own[y]
    act = active_mask(W, y)
    s = W.sep_share_y[y]
    base = act & (W.kind == 2) & (W.special[y] == "") & ~np.isin(W.county, [KESSLER, ABINGTON])
    if county is not None:
        base &= W.county == county
    if y == 2025:
        base &= ~W.excluded_2025
    hi_ = hi if hi else 10 ** 12
    cand = np.where(base & (own >= lo / 0.85) & (own < hi_))[0]
    rng.shuffle(cand)
    for e in cand:
        p = round(own[e] * s[e])
        if p < lo:
            new = (lo + 1 + int(rng.integers(0, max(1, int(own[e] * 0.85) - lo)))) / own[e]
            new = min(0.85, max(0.5, new))
            if round(own[e] * new) >= lo and own[e] - round(own[e] * new) < lo:
                s[e] = new
                return int(e)
    raise AssertionError(("no couple to break the tie", y, lo, hi))


def clear_rounding_edge(W, y, B, width=70):
    """Move every unit-level AGI that sits within `width` of the rounding edge B out of the window:
    households without attached income (own AGI), separately filed spouses (split share) and
    nonresidents. Used only where an unpinned construction's floor would otherwise sit on a
    half-thousand edge."""
    rng = stream(f"edge{y}_{B}")
    act = active_mask(W, y)
    own = W.own[y]
    kid = W.kid_agi[y]
    att = np.bincount(W.dep_owner, weights=kid, minlength=W.n).astype(np.int64)
    ok = act & (W.special[y] == "") & (att == 0)
    if y == 2025:
        ok &= ~W.excluded_2025
    moved = 0
    win = ok & (own >= B - width) & (own <= B + width)
    for e in np.where(win)[0]:
        own[e] = (B - width - int(rng.integers(1, 40))) if own[e] < B else (B + width + int(rng.integers(1, 40)))
        moved += 1
    s = W.sep_share_y[y]
    sep = act & (W.kind == 2) & (W.special[y] == "")
    if y == 2025:
        sep &= ~W.excluded_2025
    for e in np.where(sep)[0]:
        for _ in range(50):
            p = round(own[e] * s[e])
            q = own[e] - p
            if abs(p - B) > width and abs(q - B) > width:
                break
            s[e] = min(0.85, max(0.5, s[e] + rng.uniform(-0.01, 0.01)))
            moved += 1
    nr = W.nonres[y]["agi"]
    w = np.where((nr >= B - width) & (nr <= B + width))[0]
    for i in w:
        nr[i] = (B - width - int(rng.integers(1, 40))) if nr[i] < B else (B + width + int(rng.integers(1, 40)))
        moved += 1
    return moved
