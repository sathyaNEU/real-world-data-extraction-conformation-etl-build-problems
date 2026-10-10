"""Runs the generation stages in order. Seeded: the same SEED yields the same world."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

import desk as K
import loads as L
import world as W
from common import SEED, SUMMERS

CREDIT_RATE = {2017: 0.28, 2018: 0.28, 2019: 0.28, 2020: 0.31, 2021: 0.31, 2022: 0.31, 2023: 0.36, 2024: 0.36,
               2025: 0.36, 2026: 0.36}


@dataclass
class World:
    prem: pd.DataFrame
    heat: dict
    calls: dict
    mreads: pd.DataFrame
    temps: pd.DataFrame
    peak_heat_n: int
    temp_cut: dict
    ireads: pd.DataFrame
    u_star: float
    f: dict
    pieces: dict
    m27: pd.Series
    settled: pd.DataFrame
    credits: pd.DataFrame
    base_at_peak: dict
    quotes: pd.DataFrame
    blotter: pd.DataFrame
    matching: pd.DataFrame


def build_world(seed: int = SEED) -> World:
    rng = np.random.default_rng(seed)
    prem = W.build_premises(rng)
    prem = W.add_amendments(rng, prem)
    prem = W.assign_ids(rng, prem)
    heat = L.build_heat(np.random.default_rng(seed + 1))
    calls = L.choose_calls(np.random.default_rng(seed + 2), heat)
    mreads = L.member_reads(np.random.default_rng(seed + 3), prem, calls, heat)
    cr, base, mreads = L.credits(prem, mreads, calls, CREDIT_RATE)
    temps = L.build_temps(np.random.default_rng(seed + 9), heat)
    u_star, n_hot, cut = L.peak_heat_draw(prem, mreads, calls, temps)
    f, pieces, m27 = L.solve_factors(np.random.default_rng(seed + 4), prem, mreads, calls, u_star)
    ireads = L.idr_reads(np.random.default_rng(seed + 5), prem, heat, f)
    settled = L.settled(np.random.default_rng(seed + 6), prem, heat, f, mreads)
    quotes = K.build_quotes(np.random.default_rng(seed + 7))
    bl, ml = K.build_trades(np.random.default_rng(seed + 8))
    return World(prem=prem, heat=heat, calls=calls, mreads=mreads, temps=temps, peak_heat_n=n_hot, temp_cut=cut,
                 ireads=ireads, u_star=u_star, f=f, pieces=pieces,
                 m27=m27, settled=settled, credits=cr, base_at_peak=base, quotes=quotes, blotter=bl, matching=ml)
