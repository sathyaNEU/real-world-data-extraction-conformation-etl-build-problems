"""task170 world: the clean truth before any file is written or any mess applied.

Every quantity is drawn here from fixed seeds, one stream per component, so a rebuild is byte-identical.

The mechanism. LulaNet R stops about four bites in five of those that reach a person in bed under it (Q), and
nothing else: a person indoors but not yet in bed, or outdoors, is bitten as if there were no net. So a trial's
protective efficacy at a site is Q times the share of its participants' exposure that arrives while they are in bed
(the site's in-bed share), and the share of a Ruvari resident's exposure the nets can reach is the overlap of the
county vector's hourly biting, indoors and outdoors, with the residents' hourly location. Cases are proportional to
bites received, so the cases a net user is spared are Q times that share."""
from __future__ import annotations

import math

import numpy as np

import common as C

Q = 0.80                                   # per-bite protection for a sleeper under the net

# ---------------------------------------------------------------------------------------------------- profiles
H = np.arange(12)
MID = H + 0.5                              # the half hour of each bin, in hours after 18:00


def vector_profile(peak, width, out_ratio, skew=0.0):
    b = np.exp(-0.5 * ((H + 0.5 - peak) / width) ** 2) * (1 + skew * (H - 6) / 6)
    b = np.clip(b, 1e-6, None)
    b = b / b.sum()
    return b, b * out_ratio


# county: An. ruvariensis bites from dusk and peaks between 20:00 and 22:00, more than half of it outdoors
COUNTY_VECTOR = dict(peak=3.15, width=2.35, out_ratio=1.636, skew=-0.05)
# the county's residents by age group: share of the population, time indoors for the night, bedtime, rising
# (hours after 18:00; mean and standard deviation)
COUNTY_PEOPLE = [
    ("under 5", 0.16, (1.95, 0.55), (2.70, 0.55), (11.80, 0.40)),
    ("5 to 14", 0.29, (2.45, 0.60), (3.25, 0.60), (11.75, 0.40)),
    ("15 and over", 0.55, (3.05, 0.80), (3.95, 0.75), (11.55, 0.45)),
]

# the five KINGA-5 sites: vector (peak, width, outdoor ratio), people (indoors, bed: mean and sd), and size
SITES = [
    ("Mabwe", (7.0, 2.0, 0.40), (2.55, 0.70, 3.55, 0.70), 3112.6, 0.548),
    ("Kisiriri", (6.0, 2.2, 0.80), (2.90, 0.80, 3.90, 0.80), 2887.4, 0.611),
    ("Kibondeni", (5.0, 2.3, 1.35), (4.30, 0.90, 4.75, 0.80), 2995.1, 0.502),
    ("Chibowa", (4.8, 2.3, 0.60), (2.70, 0.80, 3.80, 0.70), 2763.8, 0.587),
    ("Lukonde", (4.0, 2.4, 1.08), (3.00, 0.80, 3.90, 0.70), 3050.9, 0.534),
]
SITE_RISE = (11.60, 0.45)
SITE_RISES = {"Mabwe": (11.45, 0.40), "Kisiriri": (11.70, 0.45), "Kibondeni": (11.85, 0.50), "Chibowa": (11.55, 0.40),
              "Lukonde": (11.65, 0.50)}


def ncdf(x, m, s):
    return 0.5 * (1 + math.erf((x - m) / (s * math.sqrt(2))))


def table_shares(indoor, bed, rise=SITE_RISE):
    """Share of a population indoors (in bed or not) and in bed at each bin's half hour."""
    ind, inb = [], []
    for t in MID:
        up = 1 - ncdf(t, *rise)
        b = ncdf(t, *bed) * up
        i = max(ncdf(t, *indoor) * up, b)
        ind.append(i)
        inb.append(b)
    return np.array(ind), np.array(inb)


def in_bed_share(b_in, b_out, ind, inb):
    expo = b_in * ind + b_out * (1 - ind)
    return float((b_in * inb).sum() / expo.sum())


# ---------------------------------------------------------------------------------------------------- trial
def trial(rng):
    """The KINGA-5 site tables as the report prints them and the site outcomes drawn from them."""
    sites = []
    for name, (pk, w, orat), (im, isd, bm, bs), py, inc in SITES:
        b_in, b_out = vector_profile(pk, w, orat)
        nightly_in = float(rng.uniform(6.5, 11.0))
        b_in_t = np.round(b_in * nightly_in, 2)
        b_out_t = np.round(b_out * nightly_in, 2)
        ind, inb = table_shares((im, isd), (bm, bs), SITE_RISES[name])
        ind_t, inb_t = np.round(ind * 100), np.round(inb * 100)
        share = in_bed_share(b_in_t, b_out_t, ind_t / 100, inb_t / 100)
        py_c = round(py * rng.uniform(0.97, 1.03), 1)
        py_n = round(py * rng.uniform(0.97, 1.03), 1)
        cases_c = int(rng.poisson(py_c * inc))
        cases_n = int(rng.poisson(py_n * inc * (1 - Q * share)))
        sites.append(dict(site=name, b_in=b_in_t, b_out=b_out_t, ind=ind_t, inb=inb_t, share=share,
                          py_c=py_c, py_n=py_n, cases_c=cases_c, cases_n=cases_n))
    return sites


# ---------------------------------------------------------------------------------------------------- county people
def survey_people(rng, n_hh, round_no, prior=None):
    """Household members as the behaviour survey interviews them: the previous evening's times."""
    rows = []
    groups = [g[0] for g in COUNTY_PEOPLE]
    pshare = np.array([g[1] for g in COUNTY_PEOPLE])
    for hh in range(n_hh):
        size = int(rng.choice([2, 3, 4, 5, 6, 7, 8], p=[.09, .15, .21, .22, .17, .10, .06]))
        for p in range(size):
            g = int(rng.choice(3, p=pshare))
            _, _, ind, bed, rise = COUNTY_PEOPLE[g]
            t_in = rng.normal(*ind)
            t_bed = max(rng.normal(*bed), t_in + rng.uniform(0.05, 0.4))
            t_rise = rng.normal(*rise)
            rows.append(dict(hh=hh, person=p + 1, group=groups[g], t_in=t_in, t_bed=t_bed, t_rise=t_rise))
    return rows


def shares_from_people(rows):
    ind = np.zeros(12)
    inb = np.zeros(12)
    for r in rows:
        for h, t in enumerate(MID):
            up = t < r["t_rise"]
            ind[h] += (t >= r["t_in"]) and up
            inb[h] += (t >= r["t_bed"]) and up
    n = len(rows)
    return ind / n, inb / n


def county_population_shares(rng, n=60000):
    rows = []
    pshare = np.array([g[1] for g in COUNTY_PEOPLE])
    for _ in range(n):
        g = int(rng.choice(3, p=pshare))
        _, _, ind, bed, rise = COUNTY_PEOPLE[g]
        t_in = rng.normal(*ind)
        t_bed = max(rng.normal(*bed), t_in + rng.uniform(0.05, 0.4))
        rows.append(dict(t_in=t_in, t_bed=t_bed, t_rise=rng.normal(*rise)))
    return shares_from_people(rows)
