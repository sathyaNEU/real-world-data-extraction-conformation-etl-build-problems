"""The conference's published Household Income Tables (TY2022 to TY2024), computed forward from
the return files on the household construction, and every construction's reproduction count."""
import numpy as np

import constructions as C
import world as Wm
from common import stream

EXPECTED_HITS = {
    ("code1", "ffu", "attached"): 69,
    ("code1", "ffu", "dropped"): 55,
    ("code1", "ffu", "separate"): 58,
    ("code1", "return", "attached"): 3,
    ("code1", "return", "dropped"): 0,
    ("code1", "return", "separate"): 3,
    ("all", "ffu", "attached"): 0,
    ("all", "ffu", "dropped"): 0,
    ("all", "ffu", "separate"): 0,
    ("all", "return", "attached"): 0,
    ("all", "return", "dropped"): 0,
    ("all", "return", "separate"): 0,
    C.PARTIAL: 66,
}


def appendix_codes(R2024):
    """The twelve counties with the most full-year resident returns processed for TY2024, largest
    first (the order the appendix prints them in)."""
    r = R2024[R2024.residency_code == 1]
    cnt = r.county_code.value_counts()
    cnt = cnt.sort_values(ascending=False, kind="stable")
    codes = [str(c) for c in cnt.index[:13]]
    assert cnt.iloc[11] > 1.15 * cnt.iloc[12], "twelfth and thirteenth counties too close"
    return codes[:12], [int(x) for x in cnt.iloc[:13]]


def published(R, S, app):
    return {y: C.published_cells(C.units(R[y], S[y], "code1", "ffu", "attached"), y, app) for y in (2022, 2023, 2024)}


def all_cells(R, S, app):
    out = {}
    for c in C.ALL_CONSTRUCTIONS:
        out[c] = {y: C.published_cells(C.units(R[y], S[y], *c), y, app) for y in (2022, 2023, 2024)}
    return out


def hit_table(cells, pub):
    hits, misses = {}, {}
    for c, by_year in cells.items():
        h, m = 0, []
        for y, pc in pub.items():
            for k, v in pc.items():
                if by_year[y][k] == v:
                    h += 1
                else:
                    m.append((y, k, by_year[y][k], v))
        hits[c], misses[c] = h, m
    return hits, misses


def settle_ties(W, frames_fn, max_rounds=12):
    """Rebuild prior-year frames and break any coincidental tie until every construction's hit
    count is the designed one. Only split shares of separately filed couples move (return-grain
    cells); filing units and households are untouched."""
    rng = stream("ties")
    for rnd in range(max_rounds):
        R, S = frames_fn(W, (2022, 2023, 2024))
        app, _ = appendix_codes(R[2024])
        pub = published(R, S, app)
        cells = all_cells(R, S, app)
        hits, misses = hit_table(cells, pub)
        bad = {c: hits[c] for c in hits if hits[c] != EXPECTED_HITS[c]}
        if not bad:
            return R, S, app, pub, cells, hits, misses, rnd
        fixed = False
        for c in bad:
            if c[1] != "return":
                continue
            for y, pc in pub.items():
                for k, v in pc.items():
                    if k[0] == "units" and cells[c][y][k] == v:
                        lab = k[1]
                        lo, hi = C.CLASSES[C.CLASS_LABELS.index(lab)]
                        Wm.break_return_tie(W, y, lo, hi, rng)
                        fixed = True
                    elif k[0] == "agi_k" and cells[c][y][k] == v and k[1] != "all":
                        lo, hi = C.CLASSES[C.CLASS_LABELS.index(k[1])]
                        Wm.break_return_tie(W, y, lo, hi, rng)
                        fixed = True
                    elif k[0] == "county_units_500k" and cells[c][y][k] == v:
                        Wm.break_return_tie(W, y, 500_000, None, rng, county=k[1])
                        fixed = True
        if not fixed:
            raise AssertionError(("unexpected hit counts", bad))
    raise AssertionError("ties did not settle")
