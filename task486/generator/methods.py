"""The routes from the release to each provider area's counts, each a complete pipeline.

    block_sum        add the area's block counts (the default path)
    drop_empty       the same, leaving out blocks with no housing units and no group quarters facility
    drop_rake        drop those blocks, then spread each block group's count over its remaining blocks by their counts
    bg_hu            the golden: whole block groups take their own count; a block group the boundary cuts is split by
                     census-day housing units
    tract_hu         the same at tract level: whole tracts take their count, a cut tract is split by housing units
    bg_pop           cut block groups split by the blocks' published total population
    bg_points        cut block groups split by the county's 2026 address points
"""
import collections

import numpy as np

import world as W

ROUTES = ["block_sum", "drop_empty", "drop_rake", "bg_hu", "tract_hu", "bg_pop", "bg_points"]


def ages(cells, which):
    idx = W.A60 if which == "60" else W.A75
    return sum(cells[s * 23 + a] for s in (0, 1) for a in idx)


def area_counts(blocks, rel, route, which, points=None):
    """{area: count} for one route; which is '60' or '75'."""
    pub = rel["block"]
    out = collections.Counter()
    by_bg = collections.defaultdict(list)
    by_tr = collections.defaultdict(list)
    for i, b in enumerate(blocks):
        by_bg[b["bg"]].append(i)
        by_tr[b["tract"]].append(i)
    if route in ("block_sum", "drop_empty"):
        for i, b in enumerate(blocks):
            if route == "drop_empty" and b["hu"] == 0 and b["gq"] is None:
                continue
            out[b["area"]] += ages(pub[i], which)
        return out
    if route == "drop_rake":
        for g, idx in by_bg.items():
            keep = [i for i in idx if not (blocks[i]["hu"] == 0 and blocks[i]["gq"] is None)]
            total = ages(rel["block_group"][g], which)
            w = np.array([ages(pub[i], which) for i in keep], float)
            if w.sum() == 0:
                w = np.ones(len(keep))
            for i, x in zip(keep, w / w.sum() * total):
                out[blocks[i]["area"]] += x
        return out
    if route == "tract_hu":
        for t, idx in by_tr.items():
            total = ages(rel["tract"][t], which)
            areas = {blocks[i]["area"] for i in idx}
            if len(areas) == 1:
                out[areas.pop()] += total
                continue
            hu = np.array([blocks[i]["hu"] for i in idx], float)
            for i, x in zip(idx, hu / hu.sum() * total):
                out[blocks[i]["area"]] += x
        return out
    for g, idx in by_bg.items():       # bg_hu, bg_pop, bg_points
        total = ages(rel["block_group"][g], which)
        areas = {blocks[i]["area"] for i in idx}
        if len(areas) == 1:
            out[areas.pop()] += total
            continue
        if route == "bg_hu":
            w = np.array([blocks[i]["hu"] for i in idx], float)
        elif route == "bg_pop":
            w = np.array([pub[i].sum() for i in idx], float)
        else:
            w = np.array([points[i] for i in idx], float)
        for i, x in zip(idx, w / w.sum() * total):
            out[blocks[i]["area"]] += x
    return out


def truth(blocks, which):
    out = collections.Counter()
    for b in blocks:
        out[b["area"]] += ages(b["cells"], which)
    return out


def r10(x):
    """Nearest ten, halves up (never reached: every graded figure sits clear of a half)."""
    return int(np.floor(x / 10.0 + 0.5) * 10)


def edge10(x):
    """Distance from x to the nearest edge of its nearest-ten cell."""
    return 5.0 - abs(x - r10(x))
