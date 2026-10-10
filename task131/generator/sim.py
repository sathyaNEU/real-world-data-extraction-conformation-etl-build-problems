"""Simulation of the Talwerk summer 2026 offer test, card by card and week by week.

The offer engine allocated cards, 20 per cent to each cell. A membership's cards buy from one
household budget; a card carrying an offer pulls part of the household's baskets off the
membership's cards that carry a different cell. At a full rollout every card carries the offer and
nothing moves, so the rollout effect is what memberships whose cards share one cell show.
"""
import hashlib
import numpy as np
import pandas as pd

import world as W

N_MEMB = 24_000
SIZE_P = [0.58, 0.31, 0.09, 0.02]          # cards per membership: 1, 2, 3, 4

# Designed rollout effect per active card-week in net margin (CHF), run-rate weeks, by 2027 region.
# These are the targets the cells of memberships whose cards share one cell are forced to.
EFFECT = {
    "SGS": {"A": 0.5704, "B": 0.3121, "C": 0.2266, "D": 0.4229},
    "FUE": {"A": 0.4178, "B": 0.2018, "C": 0.0830, "D": 0.2524},
    "RHT": {"A": 0.4114, "B": 0.1883, "C": 0.0871, "D": 0.2824},
    "TGO": {"A": 0.4670, "B": 0.2382, "C": 0.1470, "D": 0.3024},
    "TOG": {"A": 0.4510, "B": 0.2681, "C": 0.1333, "D": 0.3224},
    "APZ": {"A": 0.5873, "B": 0.3383, "C": 0.2474, "D": 0.4170},
    # areas whose members moved region on 1 July: between the region they left and the one they joined
    "ROR": {"A": 0.4899, "B": 0.2479, "C": 0.1569, "D": 0.3432},
    "DEG": {"A": 0.5070, "B": 0.2716, "C": 0.1675, "D": 0.3353},
}
# Control change from baseline to run-rate weeks per active card-week (summer), by area.
CONTROL = {"SGS": -2.0137, "FUE": -1.9862, "RHT": -2.0063, "TGO": -1.9938, "TOG": -1.9847, "APZ": -2.0154,
           "ROR": -2.0091, "DEG": -1.9908}


def area_of(branch):
    if branch in ("3107", "3112", "3115"):
        return "ROR"
    if branch == "2209":
        return "DEG"
    return W.region_2027(branch)


# Offer mechanics, as effective rates on the card's spend and relative uplifts on its own spend.
OFFER_RATE = {"A": 0.019, "B": 0.013, "C": 0.0, "D": 0.022}      # C pays a voucher instead
VOUCHER_C = 15.0
VOUCHER_C_THRESHOLD = 250.0
UPLIFT = {"A": 0.112, "B": 0.071, "C": 0.118, "D": 0.115}         # own spend uplift, run-rate
NOVELTY = {"A": 1.10, "B": 2.60, "C": 1.60, "D": 1.05}            # early test weeks multiplier
# Share of a sibling card's spend a card carrying the offer pulls onto itself, by offer.
PULL = {"A": 0.0025, "B": 0.010, "C": 0.016, "D": 0.0215}
PULL_NOVELTY = {"A": 1.0, "B": 1.6, "C": 1.1, "D": 1.0}

SEASON = np.array([1.00, 1.01, 0.99, 1.02, 1.00, 0.98, 1.01, 1.00,      # W15..W22
                   0.98, 0.97, 0.97, 0.96, 0.93, 0.92,                   # W23..W28
                   0.90, 0.89, 0.89, 0.90, 0.91, 0.93])                  # W29..W34
REGION_SEASON = {"SGS": 0.985, "FUE": 0.995, "RHT": 0.992, "TGO": 1.000, "TOG": 1.006, "APZ": 0.990}


def card_number(rng, n, legacy_share=0.18):
    """13-digit Talwerk card numbers: 2 7660 xxxxxxx check digit; legacy cards 0 4180 ..."""
    out = set()
    nums = []
    while len(nums) < n:
        legacy = rng.random() < legacy_share
        body = ("04180" if legacy else "27660") + f"{rng.integers(0, 10**7):07d}"
        digits = [int(c) for c in body]
        chk = (10 - (sum(d * (3 if i % 2 else 1) for i, d in enumerate(digits)) % 10)) % 10
        num = body + str(chk)
        if num not in out:
            out.add(num)
            nums.append(num)
    return nums


def allocation_bucket(card_no):
    return int(hashlib.sha1(("ST26|" + card_no).encode()).hexdigest()[:8], 16) % 100


def bucket_cell(b):
    return W.ARMS[b // 20]


def simulate(seed=W.SEED):
    rng = np.random.default_rng(seed)
    branches = [b[0] for b in W.BRANCHES]
    fmt_w = {"S": 0.6, "M": 1.0, "L": 1.6}
    bw = np.array([fmt_w[b[5]] for b in W.BRANCHES])
    bw = bw / bw.sum()

    # memberships
    size = rng.choice([1, 2, 3, 4], size=N_MEMB, p=SIZE_P)
    home = rng.choice(branches, size=N_MEMB, p=bw)
    reg = np.array([W.region_2027(b) for b in home])
    base_by_size = {1: 92.0, 2: 163.0, 3: 214.0, 4: 247.0}
    budget = np.array([base_by_size[s] for s in size]) * rng.lognormal(0, 0.38, N_MEMB)
    mrate = rng.uniform(0.246, 0.318, N_MEMB)
    memb_no = rng.choice(np.arange(10_000_000, 99_999_999), size=N_MEMB, replace=False).astype(str)
    joined = pd.to_datetime("1985-01-01") + pd.to_timedelta(
        (rng.beta(1.6, 1.1, N_MEMB) * (pd.Timestamp("2026-03-31") - pd.Timestamp("1985-01-01")).days).astype(int), unit="D")

    # cards
    m_idx = np.repeat(np.arange(N_MEMB), size)
    pos = np.concatenate([np.arange(s) for s in size])
    n_cards = len(m_idx)
    cards = card_number(rng, n_cards)
    raw_share = np.where(pos == 0, rng.uniform(2.2, 4.0, n_cards), rng.uniform(0.6, 1.6, n_cards))
    share = raw_share / np.bincount(m_idx, weights=raw_share)[m_idx]
    pvisit = np.where(pos == 0, rng.uniform(0.78, 0.95, n_cards), rng.uniform(0.38, 0.72, n_cards))
    cell = np.array([bucket_cell(allocation_bucket(c)) for c in cards])

    nw = len(W.WEEKS)
    reg_c = reg[m_idx]
    season = SEASON[None, :] * np.array([REGION_SEASON[r] for r in reg_c])[:, None] ** (np.arange(nw)[None, :] >= 8)
    mu = (budget[m_idx] * share)[:, None] * season
    visit = rng.random((n_cards, nw)) < pvisit[:, None]
    # every allocated card bought at least once in the baseline weeks (allocation took cards active since 6 April)
    none_base = ~visit[:, W.BASE].any(axis=1)
    fix_w = rng.integers(0, 8, n_cards)
    visit[none_base, fix_w[none_base]] = True
    noise = rng.lognormal(-0.32 ** 2 / 2, 0.32, (n_cards, nw))
    spend = np.where(visit, mu / pvisit[:, None] * noise, 0.0)

    # own uplift from the offer, in the test weeks
    test_mask = np.zeros(nw, bool); test_mask[W.TEST] = True
    early_mask = np.zeros(nw, bool); early_mask[W.EARLY] = True
    upl = np.zeros((n_cards, nw))
    for x in W.OFFERS:
        sel = cell == x
        mult = np.where(early_mask, NOVELTY[x], 1.0) * test_mask
        upl[sel] = UPLIFT[x] * mult[None, :]
    spend_own = spend * (1 + upl)

    # pulls between cards of one membership that carry different cells
    pull = np.zeros((n_cards, nw))
    out_of = np.zeros((n_cards, nw))
    first = np.concatenate([[0], np.cumsum(size)[:-1]])
    multi = np.where(size > 1)[0]
    for m in multi:
        idx = np.arange(first[m], first[m] + size[m])
        for c in idx:
            x = cell[c]
            if x == "K":
                continue
            rate = PULL[x] * np.where(early_mask, PULL_NOVELTY[x], 1.0) * test_mask
            for j in idx:
                if j == c or cell[j] == x:
                    continue
                pull[c] += rate * spend_own[j]
                out_of[j] += rate * spend_own[j]
    # never take more than 60 per cent of a card's own spend
    cap = np.where(out_of > 0.6 * spend_own, 0.6 * spend_own / np.maximum(out_of, 1e-9), 1.0)
    # scale each pull by the sender's cap (approximate: apply the cap of the most-capped sibling)
    final = spend_own - out_of * cap + pull * 1.0
    final = np.maximum(final, 0.0)
    # a pull can create a basket on a card that had none that week
    gm_rate = mrate[m_idx][:, None] * rng.lognormal(0, 0.045, (n_cards, nw))
    margin = final * gm_rate

    # reward cost: 1 point per whole franc at CHF 0.01, plus the offer
    reward = np.floor(final) * 0.01
    for x in ("A", "B", "D"):
        sel = cell == x
        reward[sel] += (final[sel] * OFFER_RATE[x]) * test_mask[None, :]
    selc = np.where(cell == "C")[0]
    # monthly voucher on the card's own spend: the week the calendar month total crosses CHF 250
    wmonth = np.array([(W.WEEK_START[w] + pd.Timedelta(days=3)).month for w in W.WEEKS])
    for mth in sorted(set(wmonth[W.TEST])):
        cols = [i for i in W.TEST if wmonth[i] == mth]
        cum = np.cumsum(final[np.ix_(selc, cols)], axis=1)
        crossed = (cum >= VOUCHER_C_THRESHOLD)
        firstcross = np.where(crossed.any(axis=1), crossed.argmax(axis=1), -1)
        for k, ci in enumerate(selc):
            if firstcross[k] >= 0:
                reward[ci, cols[firstcross[k]]] += VOUCHER_C

    sim = dict(rng=rng, size=size, home=home, reg=reg, memb_no=memb_no, joined=joined, mrate=mrate,
               m_idx=m_idx, pos=pos, cards=np.array(cards), cell=cell, spend=final, margin=margin,
               reward=reward, visit=(final > 0), first=first)
    return sim


def pure_mask(sim):
    cell, m_idx, size = sim["cell"], sim["m_idx"], sim["size"]
    df = pd.DataFrame({"m": m_idx, "cell": cell})
    n_cells = df.groupby("m")["cell"].nunique().to_numpy()
    return (n_cells == 1)[m_idx]


def force_cells(sim):
    """Force the run-rate change of same-cell memberships to the designed value in every
    (2027 region, cell, cards-per-membership) group, by moving gross margin in the run-rate weeks.
    Every estimator built on same-cell memberships (single-card only, all same-cell, by card or by
    membership) then lands on the same figure."""
    pure = pure_mask(sim)
    reg_c = np.array([area_of(h) for h in sim["home"]])[sim["m_idx"]]
    size_c = sim["size"][sim["m_idx"]]
    net = sim["margin"] - sim["reward"]
    delta = net[:, W.RUN].mean(axis=1) - net[:, W.BASE].mean(axis=1)
    run_rows = (sim["spend"][:, W.RUN] > 0)
    nrun = run_rows.sum(axis=1)
    for r in CONTROL:
        for x in W.ARMS:
            target = CONTROL[r] + (EFFECT[r][x] if x != "K" else 0.0)
            for s in (1, 2, 3, 4):
                g = np.where(pure & (reg_c == r) & (sim["cell"] == x) & (size_c == s))[0]
                if len(g) == 0:
                    continue
                d = target - delta[g].mean()
                adj = g[nrun[g] > 0]
                run_tot = sim["spend"][np.ix_(adj, W.RUN)].sum(axis=1)
                card_shift = d * len(g) * run_tot / run_tot.sum()   # change in each card's run-rate mean
                for ci, shift in zip(adj, card_shift):
                    cols = [W.RUN[i] for i in np.where(run_rows[ci])[0]]
                    sp = sim["spend"][ci, cols]
                    sim["margin"][ci, cols] += shift * len(W.RUN) * sp / sp.sum()
    return sim


def round_cents(sim):
    for k in ("spend", "margin", "reward"):
        sim[k] = np.round(sim[k], 2)
    sim["margin"] = np.where(sim["spend"] > 0, sim["margin"], 0.0)
    sim["reward"] = np.where(sim["spend"] > 0, sim["reward"], 0.0)
    return sim
