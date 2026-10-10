"""Runs the generation stages in order and returns every internal frame the writers and the
assertions need. Seeded: the same SEED yields the same world."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

import ledger as L
import meters as M
import sessions as S
import world as W
from common import lt_date

SEED = 117_2027


@dataclass
class World:
    pos: pd.DataFrame
    register: pd.DataFrame
    veh: dict
    cal: dict
    reads: set
    b3: dict
    sessions: pd.DataFrame          # every generated session, accepted energy
    rows: pd.DataFrame              # ledger rows (all versions, re-deliveries) + gateway B rows
    decisions: pd.DataFrame
    rd: pd.DataFrame                # quarter-hour readings for every row in rows
    light: dict
    books: object
    read_times: dict
    read_report: dict
    log: pd.DataFrame
    fixes: pd.DataFrame = None
    corr: dict = None
    extra: dict = field(default_factory=dict)


def build_world(seed: int = SEED) -> World:
    rng = np.random.default_rng(seed)
    pos, register = W.build_stations(rng)
    veh = W.build_vehicles_and_permits(rng)
    b3 = S.choose_b3_parameters()
    gen = S.Generator(rng, pos, veh)
    cal, reads = S.plan_calendar(rng)
    S.generate_decks(gen, cal, reads, b3)
    S.generate_library_fast(gen)
    special = {d for d, t in cal.items() if t[0] in ("bind", "rung2", "b3")}
    S.generate_public(gen, pos, special)
    S.apply_rotation(gen, cal, veh["permits"])
    sess = gen.frame()

    df, led, gwb, decisions = L.build_ledger(rng, sess, pos, read_dec2025=None)
    read_dec2025 = M.meter_instant(pd.Timestamp("2025-12-31").date(), *M.DEC31_2025)
    exclude = set()
    led = L.add_redeliveries(rng, led, read_dec2025, exclude)
    led = L.assign_session_ids(rng, led)
    rows = pd.concat([led, gwb.assign(session_id=pd.NA)], ignore_index=True)
    rd = L.readings(rows)

    light = {p: M.Lighting(np.random.default_rng(seed + (1 if p == "CP-N" else 2)), p) for p in M.PANELS}
    books = M.PanelBooks(rows, rd, light)
    times, report, corr = M.choose_read_times(rng, books)
    log, fixes = M.build_log(books, times, rng, corr)
    return World(pos=pos, register=register, veh=veh, cal=cal, reads=reads, b3=b3, sessions=df, rows=rows,
                 decisions=decisions, rd=rd, light=light, books=books, read_times=times, read_report=report, log=log, fixes=fixes, corr=corr)
