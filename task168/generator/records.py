"""Flight numbering, tails and the record layers every pack file is written from."""
import datetime as dt

import numpy as np

import world as W
import sim
from network import build_season

BASE_BLOCK_NEW = {"LIN": 2100, "TRN": 2300, "VRN": 2400, "VCE": 2500, "BLQ": 2600}
BASE_BLOCK_OLD = {"LIN": 400, "TRN": 500, "VRN": 600, "VCE": 700, "BLQ": 800}


def route_list():
    """Every route (base, station, kind) in a fixed order: the nine Linate routes, the 2025 upgauges, the rest."""
    out = [("LIN", st, "target") for st, *_ in W.TARGETS]
    out += [(b, st, "past") for b, st, *_ in W.PAST]
    out += [(b, st, "ref") for b, st, *_ in W.REF]
    return out


def flight_blocks():
    """Route -> (new block start, old block start). Ten numbers per route, outbound odd, return even."""
    nxt_new = dict(BASE_BLOCK_NEW)
    nxt_old = dict(BASE_BLOCK_OLD)
    lin_other_new = 2700
    out = {}
    for b, st, kind in route_list():
        if b == "LIN" and kind != "target":
            n_new = lin_other_new
            lin_other_new += 10
        else:
            n_new = nxt_new[b]
            nxt_new[b] += 10
        n_old = nxt_old[b]
        nxt_old[b] += 10
        out[(b, st)] = (n_new, n_old)
    return out


BLOCKS = flight_blocks()


def flight_number(base, st, outbound, rot, season):
    n_new, n_old = BLOCKS[(base, st)]
    start = n_new if season in ("S25", "S26") else n_old
    return start + 2 * rot + (1 if outbound else 2)


def leg_base_station(leg):
    if leg.orig in BASE_BLOCK_NEW and (leg.orig, leg.dest) in BLOCKS:
        return leg.orig, leg.dest, True
    return leg.dest, leg.orig, False


def flights_for_leg(leg):
    b, st, outbound = leg_base_station(leg)
    return [flight_number(b, st, outbound, leg.rot[i], leg.season) for i in range(leg.n)]


class Seasons:
    """The simulated seasons, built once per build."""

    def __init__(self):
        self.S24 = build_season("S24")
        self.S25 = build_season("S25")
        for L in self.S24 + self.S25:
            L.flt = flights_for_leg(L)
            L.base, L.station, L.outbound_ = leg_base_station(L)

    def legs(self, season, kind=None):
        legs = self.S24 if season == "S24" else self.S25
        return [L for L in legs if kind is None or L.kind == kind]
