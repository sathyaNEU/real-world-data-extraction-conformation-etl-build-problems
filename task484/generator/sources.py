"""The clean truth: every city's housing stock since the 2020 census, the buildings completed since (their units,
certificate-of-occupancy dates and how they filled), and the residents on the estimate date. Nothing here knows
about files or layouts."""
import datetime as dt

import numpy as np

import world as W


def months(a, b):
    """months from date a to date b."""
    return (b - a).days / 30.4375


def fill(m, tau, level):
    return level * (1 - np.exp(-max(m, 0.0) / tau)) if m > 0 else 0.0


def year_window(y):
    a = W.CENSUS if y == 2020 else dt.date(y, 1, 1)
    b = dt.date(2026, 3, 31) if y == 2026 else dt.date(y, 12, 31)
    return a, b


def city_world(rng, name):
    hu, occ, pph, gq, system, covered, mf, sf = W.CITIES[name]
    blds = []
    for i, units in enumerate(mf):
        y = 2020 + i
        a, b = year_window(y)
        left = units
        while left > 0:
            u = int(min(left, rng.integers(60, 321)))
            if left - u < 40:
                u = left
            left -= u
            co = a + dt.timedelta(int(rng.integers(0, (b - a).days + 1)))
            blds.append(dict(kind="MF", units=u, co=co, tau=float(rng.uniform(*W.FILL_MONTHS)),
                             level=float(rng.uniform(*W.FILL_LEVEL))))
    for i, units in enumerate(sf):
        y = 2020 + i
        a, b = year_window(y)
        n = 0
        while n < units:
            # most single-family homes alone, some townhouse rows of 4 to 8 on one permit
            k = 1 if rng.random() < .82 else int(rng.integers(4, 9))
            k = min(k, units - n)
            n += k
            co = a + dt.timedelta(int(rng.integers(0, (b - a).days + 1)))
            blds.append(dict(kind="TH" if k > 1 else "SF", units=k, co=co, tau=W.SF_FILL_MONTHS,
                             level=float(rng.uniform(.95, .985))))
    demo = []
    for _ in range(int(rng.integers(8, 30))):
        d = W.CENSUS + dt.timedelta(int(rng.integers(30, (W.EST - W.CENSUS).days)))
        demo.append(dict(date=d, units=int(rng.choice([1, 1, 1, 2, 4, 6, 12]))))
    stock_occ = float(occ * (1 + rng.normal(0, .004)))
    return dict(hu=hu, occ=occ, pph=pph, gq=gq, system=system, covered=covered, blds=blds, demo=demo,
                stock_occ=stock_occ)


def world(rng):
    return {c: city_world(rng, c) for c in W.CITIES}


def truth(x):
    """{city: residents on the estimate date}: the 2020 stock less demolitions at its 2026 occupancy, every building
    completed since at its own fill, times persons per household, plus group quarters."""
    out = {}
    for c, v in x.items():
        stock = v["hu"] - sum(d["units"] for d in v["demo"])
        occd = stock * v["stock_occ"]
        for b in v["blds"]:
            if b["co"] < W.EST:
                occd += b["units"] * fill(months(b["co"], W.EST), b["tau"], b["level"])
        out[c] = occd * v["pph"] + v["gq"]
    return out
