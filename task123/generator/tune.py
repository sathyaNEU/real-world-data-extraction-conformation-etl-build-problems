"""Small whole-dollar nudges to the last quarter of a grantee's September window, so that every graded
figure sits clear of its rounding edge: fall per cent at least 0.02 from an x.x5 boundary, no two
dollar falls equal, and the struck rate clear of both step edges by NZ$25 or more."""
from common import SEPT_POT, offer_for

EDGE = 0.02


def edge_gap(pct):
    """Distance from pct to the nearest x.x5 rounding boundary."""
    x = pct * 10.0
    frac = x - int(x) if x >= 0 else x - int(x) + 1
    return abs(frac - 0.5) / 10.0 if True else 0


def needs(T, pot=SEPT_POT):
    rows = T["rows"]
    out = {}
    seen = {}
    for r in rows:
        if r["org"] in out:
            continue
        g = edge_gap(r["pct"])
        if g < EDGE + 0.004:
            # move the fall per cent by about 0.04 points away from the edge
            out[r["org"]] = ("edge", r)
        if r["fall"] in seen:
            out[r["org"]] = ("dup", r)
        seen[r["fall"]] = r["org"]
    elig = [r for r in rows if r["pct"] >= 10.0]
    rate = T["rate"]
    tot = sum(offer_for(rate, r["fall"]) for r in elig)
    nxt = sum(offer_for(rate + 1, r["fall"]) for r in elig)
    rem, over = pot - tot, nxt - pot
    return out, rem, over


def nudges_for(W):
    T = W["sept"]
    out, rem, over = needs(T)
    nud = {}
    for org, (why, r) in out.items():
        prior = r["prior"]
        # a fall per cent change of 0.045 points
        d = int(round(prior * 0.00045)) or 1
        nud[(org, r["end"])] = -d if why == "edge" else 7
    if rem < 25 or over < 25:
        # move an unclamped offer: shift its fall so the remainder lands mid-step
        elig = sorted([r for r in T["rows"] if r["offer"] and 15000 < r["offer"] < 150000],
                      key=lambda r: -r["fall"])
        r = elig[len(elig) // 2]
        step = rem + over
        want = step // 2
        dfall = int(round((rem - want) / (T["rate"] / 10000.0)))
        nud[(r["org"], r["end"])] = nud.get((r["org"], r["end"]), 0) - dfall
    return nud, rem, over
