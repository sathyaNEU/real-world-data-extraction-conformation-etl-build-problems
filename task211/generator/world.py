"""task211 world: Larkhaven Health's levetiracetam 500 mg tablets, the clean truth.

Day 0 is 2024-01-01. The review window is 2026-01-01 to 2026-06-30 (days 731 to 911). Every record is drawn from one
seed; nothing here is read by the golden, which works from target/ alone."""
import datetime as dt
import numpy as np
import pandas as pd

import os
SEED = int(os.environ.get('T211_SEED', '5007'))
D0 = dt.date(2024, 1, 1)
DAYS = 912
W0, W1 = 731, 911                       # 2026-01-01 .. 2026-06-30 inclusive
SHIP0 = 456                             # claims shipped from 2025-04-01
ENC0 = 547                              # encounters shipped from 2025-07-01

def day(d):
    return (d - D0).days

def date_of(n):
    return D0 + dt.timedelta(days=int(n))

# products: index 0 is the reference
PRODUCTS = [
    dict(key='LEV', name='Levaril', labeler='Avenmoor Pharmaceuticals', ndc='64871-0500-01', item='LHI204417'),
    dict(key='HAL', name='Halvorne', labeler='Halvorne Generics', ndc='69788-0231-01', item='LHI207733'),
    dict(key='PEL', name='Pellbrook', labeler='Pellbrook Pharmaceuticals', ndc='71336-0418-01', item='LHI209185'),
    dict(key='COR', name='Corwen', labeler='Corwen', ndc='70412-0155-10', item='LHI203962'),
    dict(key='TES', name='Tessard', labeler='Tessard Laboratories', ndc='72609-0507-01', item='LHI210548'),
    dict(key='WYN', name='Wynfield', labeler='Wynfield Pharma', ndc='68844-0362-01', item='LHI206271'),
]
NP_ = len(PRODUCTS)
DCS = ['Portland North', 'Vancouver', 'Portland South', 'Salem', 'Eugene', 'Medford', 'Bend']
# Halvorne's new-site supply reaches each distribution centre on these days (the manufacturer's letter)
DC_SWITCH = [day(dt.date(2025, 12, 1)), day(dt.date(2025, 12, 29)), day(dt.date(2026, 1, 26)), day(dt.date(2026, 2, 23)),
             day(dt.date(2026, 3, 23)), day(dt.date(2026, 4, 20)), day(dt.date(2026, 5, 18))]
COR_CHANGE = day(dt.date(2025, 9, 1))   # Corwen's film coat turns white
HAL_APPROVED = day(dt.date(2025, 9, 15))
TES_START = day(dt.date(2025, 7, 1))    # Tessard's persistent effect
# colours: 1 blue (Levaril, Corwen to August 2025), 2 white (Marrowby), 3 orange (Brennick), 4 pink (Halvorne's own site),
# 5 beige (Corwen's new coat); every same-coloured pair is one tablet in shape and debossing too
BACKORDERS = [(2, day(dt.date(2026, 2, 2)), day(dt.date(2026, 5, 4)), 1),    # Pellbrook out, pharmacies move to Halvorne
              (4, day(dt.date(2026, 2, 27)), day(dt.date(2026, 4, 10)), 5)]  # Tessard out, pharmacies move to Wynfield
ALT = {1: 2, 2: 1, 3: 0, 4: 5, 5: 4}
P = dict(N=60000, NP=620, brand_share=0.18, contract=[0.27, 0.22, 0.11, 0.25, 0.15], stockouts=2.5, p90=0.55,
         base=0.00075, rr_first=2.5, tes_rr=1.15, other_ed=0.0016)

def colour(p, dc, d):
    if p == 0:
        return 1
    if p == 1:
        return 4 if d >= DC_SWITCH[dc] else 2
    if p == 2:
        return 2
    if p == 3:
        return 1 if d < COR_CHANGE else 5
    return 3



def simulate(seed=SEED):
    rng = np.random.default_rng(seed)
    N, NPH = P['N'], P['NP']
    # pharmacies, each in one distribution centre's area
    ph_dc = rng.choice(len(DCS), size=NPH, p=[0.19, 0.12, 0.17, 0.16, 0.14, 0.11, 0.11])
    ph_contract = rng.choice([1, 2, 3, 4, 5], size=NPH, p=P['contract'])
    ph_prod = np.repeat(ph_contract[:, None], DAYS, axis=1).astype(np.int8)
    stockouts = []
    for ph in range(NPH):
        for _ in range(rng.poisson(P['stockouts'])):
            s = int(rng.integers(0, DAYS - 20)); L = int(rng.integers(14, 60))
            ph_prod[ph, s:s + L] = ALT[ph_contract[ph]]
            stockouts.append((ph, s, s + L))
    for (p, s, e, sub) in BACKORDERS:
        blk = ph_prod[:, s:e]
        blk[blk == p] = sub
        ph_prod[:, s:e] = blk
    # members
    home = rng.integers(0, NPH, size=N)
    brand_only = rng.random(N) < P['brand_share']
    ageband = rng.choice([0, 1, 2], size=N, p=[0.15, 0.60, 0.25])
    resistant = rng.random(N) < 0.22
    cycle = np.where(rng.random(N) < P['p90'], 90, 30)
    start = np.full(N, -1)
    late_start = rng.random(N) < 0.10
    start[late_start] = rng.integers(SHIP0, W1 - 30, size=late_start.sum())
    stop = np.full(N, DAYS + 1000)
    early_stop = rng.random(N) < 0.08
    stop[early_stop] = rng.integers(SHIP0 + 60, W1, size=early_stop.sum())
    # fills: (member, day, pharmacy, product, days_supply)
    F = []
    big = 10**6
    cover_prod = np.full((N, DAYS), -1, dtype=np.int8)
    since_change = np.full((N, DAYS), big, dtype=np.int32)
    first_new = np.zeros((N, DAYS), dtype=bool)          # days covered by the first fill after a change of tablet
    lastf = {}
    ar = np.arange(DAYS)
    for i in range(N):
        d = int(rng.integers(-cycle[i], 0)) if start[i] < 0 else int(start[i])
        prev_c = None; last_change = -big
        fills = []
        prev_end = -big
        while d < DAYS and d < stop[i]:
            ph = home[i] if rng.random() > 0.05 else int(rng.integers(0, NPH))
            dd = max(d, 0)
            p = 0 if brand_only[i] else int(ph_prod[ph, dd])
            c = colour(p, ph_dc[ph], dd)
            changed = prev_c is not None and c != prev_c
            if changed:
                last_change = dd
            fills.append((d, ph, p, cycle[i], last_change, changed))
            prev_c = c
            jit = int(rng.choice([-3, -2, -1, 0, 0, 1, 1, 2, 3, 5, 9, 16], p=[.04, .06, .08, .2, .2, .12, .1, .07, .05, .04, .02, .02]))
            d = d + cycle[i] + jit
        for k, (fd, ph, p, ds, lc, ch) in enumerate(fills):
            s, e = max(fd, 0), min(fd + ds, DAYS)
            lastf[i] = (fd, p, ds, prev_end)
            prev_end = fd + ds
            if e <= s:
                continue
            cover_prod[i, s:e] = p          # a later fill overwrites the overlap: the later fill's product counts
            first_new[i, s:e] = ch
            if lc > -big:
                since_change[i, s:e] = ar[s:e] - lc
            if fd >= SHIP0 - 100:
                F.append((i, fd, ph, p, ds))
    # every generic's patient-months in the window sits clear of a ten-month edge: where one does not, a member whose last
    # fill is a 90-day supply of that generic wholly inside the window, clear of the fill before it, stops before it
    dropped = set()
    for p in range(1, 6):
        for _ in range(5):
            v = (cover_prod[:, W0:W1 + 1] == p).sum() / 30.4375
            if 5 - abs(v - round(v / 10.0) * 10) >= 1.0:
                break
            cand = sorted(i for i, (fd, pp, ds, pe) in lastf.items() if pp == p and ds == 90 and W0 <= fd <= W1 - 90
                          and pe <= fd and i not in dropped)
            i = cand[0]
            fd = lastf[i][0]
            cover_prod[i, fd:fd + 90] = -1
            first_new[i, fd:fd + 90] = False
            since_change[i, fd:fd + 90] = big
            dropped.add(i)
    F = [f for f in F if not (f[0] in dropped and f[1] == lastf[f[0]][0])]
    # daily seizure-visit rate
    lam = P['base'] * np.array([1.2, 1.0, 0.9])[ageband][:, None] * np.where(resistant, 2.5, 1.0)[:, None]
    lam = np.broadcast_to(lam, (N, DAYS)).copy()
    tes = (cover_prod == 4) & (ar[None, :] >= TES_START)
    lam[tes] *= P['tes_rr']
    lam *= np.where((cover_prod >= 0) & first_new, P['rr_first'], 1.0)
    ev = rng.poisson(lam[:, ENC0:])
    other = rng.poisson(np.full((N, DAYS - ENC0), P['other_ed']))
    fills = pd.DataFrame(F, columns=['m', 'day', 'ph', 'p', 'days_supply'])
    return dict(rng=rng, ph_dc=ph_dc, ph_contract=ph_contract, home=home, brand_only=brand_only, ageband=ageband,
                resistant=resistant, cycle=cycle, fills=fills, cover_prod=cover_prod, since_change=since_change, first_new=first_new,
                ev=ev, other=other, lam=lam, stockouts=stockouts)
