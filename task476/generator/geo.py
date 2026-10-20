"""The county's geography: 2010 tracts and block groups, the 2020 tracts and block groups the census drew from
them, and the blocks under both. Every structure is built once from world.py and the seed."""
import numpy as np

import world as W

PREFIX = W.STATE_FIPS + W.COUNTY_FIPS


def rng_for(*key):
    s = "|".join(str(k) for k in (W.SEED,) + key)
    h = 0
    for ch in s:
        h = (h * 1000003 + ord(ch)) % (2 ** 63)
    return np.random.default_rng(h)


class BG:
    """A 2010 block group: its universe and true poverty rates in both periods, and where its ground went in 2020."""
    def __init__(self, tract10, num, u1, p1, p2, cand):
        self.tract10, self.num, self.u1, self.p1, self.p2, self.cand = tract10, num, u1, p1, p2, cand
        self.u2 = int(round(u1 * W.GROWTH))
        self.tract20 = tract10       # set for split tracts
        self.num20 = num

    @property
    def geoid10(self):
        return PREFIX + self.tract10.replace(".", "") + str(self.num)

    @property
    def geoid20(self):
        return PREFIX + self.tract20.replace(".", "") + str(self.num20)


class Tract:
    def __init__(self, code10, bgs, children, nbhd):
        self.code10, self.bgs, self.children, self.nbhd = code10, bgs, children, nbhd


def tracts():
    """Every 2010 tract in the county, candidates first, with its block groups and 2020 children."""
    out = []
    for nb in W.NEIGHBOURHOODS:
        for code, bgs, kids in W.CANDIDATES[nb]:
            t = Tract(code, [BG(code, i + 1, u, p1, p2, True) for i, (u, p1, p2) in enumerate(bgs)], [], nb)
            if kids:
                for kcode, nums in kids:
                    for j, n in enumerate(nums):
                        b = t.bgs[n - 1]
                        b.tract20, b.num20 = kcode, j + 1
                    t.children.append((kcode, [t.bgs[n - 1] for n in nums]))
            else:
                t.children.append((code, list(t.bgs)))
            out.append(t)
    rng = rng_for("other")
    codes = []
    for series in ("01", "02", "07", "08", "09", "10", "11", "12"):
        for k in range(1, 8):
            codes.append("%s%02d.00" % (series, k))
    used = {t.code10 for t in out}
    codes = [c for c in codes if c not in used and not c.startswith(("02", "03", "04", "05", "06"))]
    for code in codes[:W.OTHER_TRACTS]:
        nbg = int(rng.choice([2, 3, 3, 4, 4, 5]))
        base = float(rng.uniform(0.04, 0.34))
        drift = float(rng.normal(0.0, 0.035))
        bgs = []
        for i in range(nbg):
            u = int(rng.integers(780, 1900))
            p1 = min(0.6, max(0.015, base + float(rng.normal(0, 0.04))))
            p2 = min(0.6, max(0.015, p1 + drift + float(rng.normal(0, 0.02))))
            bgs.append(BG(code, i + 1, u, p1, p2, False))
        t = Tract(code, bgs, [], None)
        if nbg >= 4 and sum(b.u1 for b in bgs) > 5600 and rng.random() < 0.6:
            half = nbg // 2
            k1, k2 = code[:4] + ".01", code[:4] + ".02"
            for j, b in enumerate(bgs):
                b.tract20, b.num20 = (k1, j + 1) if j < half else (k2, j - half + 1)
            t.children = [(k1, bgs[:half]), (k2, bgs[half:])]
        else:
            t.children = [(code, list(bgs))]
        out.append(t)
    return out


def tract20_list(ts):
    """Every 2020 tract: (code, its block groups)."""
    return [(code, bgs) for t in ts for code, bgs in t.children]


class Block:
    """A 2010 block and the 2020 block(s) its ground lies in: [(2020 geoid, land part, water part)]."""
    def __init__(self, bg, code10, pop10, land, water):
        self.bg, self.code10, self.pop10, self.land, self.water = bg, code10, pop10, land, water
        self.parts = []

    @property
    def geoid10(self):
        return PREFIX + self.bg.tract10.replace(".", "") + self.code10


def blocks(ts):
    """Every 2010 block, each with its 2020 parts. A 2010 block group's blocks keep to one 2020 block group (the
    splits follow block-group lines); a few blocks are cut by a 2020 line inside the same tract, and two empty blocks
    of 0405.00 go to 0404.00 (a boundary touch-up along a rebuilt road)."""
    out = []
    seq20 = {}
    for t in ts:
        for b in t.bgs:
            rng = rng_for("blocks", b.geoid10)
            n = int(rng.integers(9, 24))
            pop = b.u1 * float(rng.uniform(1.02, 1.07))
            w = rng.dirichlet([1.2] * n)
            counts = [int(x) for x in np.floor(w * pop)]
            counts[0] += int(round(pop)) - sum(counts)
            for k in range(n):
                empty = rng.random() < 0.12
                land = int(rng.integers(9000, 160000))
                water = int(rng.integers(0, 40000)) if rng.random() < 0.06 else 0
                blk = Block(b, "%d%03d" % (b.num, k + 1), 0 if empty else counts[k], land, water)
                out.append(blk)
            # put the empty blocks' people back on the others so the group's population holds
            lost = sum(c for blk, c in zip(out[-n:], counts) if blk.pop10 == 0)
            live = [blk for blk in out[-n:] if blk.pop10 > 0]
            live[0].pop10 += lost
    for blk in out:
        b = blk.bg
        key = (b.tract20, b.num20)
        rng = rng_for("parts", blk.geoid10)
        tract20, num20 = b.tract20, b.num20
        if b.tract10 == "0405.00" and b.num == 3 and blk.pop10 == 0 and len([p for p in out if p.bg is b and
                                                                             p.pop10 == 0 and p.parts]) < 2:
            tract20, num20 = "0404.00", 2
        def code20():
            k = (tract20, num20)
            seq20[k] = seq20.get(k, 0) + 1
            return PREFIX + tract20.replace(".", "") + "%d%03d" % (num20, seq20[k])
        if rng.random() < 0.08 and blk.land > 40000:
            cut = float(rng.uniform(0.25, 0.75))
            l1 = int(blk.land * cut)
            blk.parts = [(code20(), l1, blk.water), (code20(), blk.land - l1, 0)]
        else:
            blk.parts = [(code20(), blk.land, blk.water)]
    return out
