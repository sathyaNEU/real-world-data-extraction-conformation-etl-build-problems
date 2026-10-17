"""The deposit population.

The size law is exact at the 250-dollar bin: every segment's own profile over
5,000 to 16,000 is log-linear, so the number of deposits the segment's ordinary
trade puts in any interval of that range is recoverable from the rest of it.
Deposits placed below the threshold on purpose are added on top, inside
9,000 to 10,000 and nowhere else.
"""
import datetime as dt
import math

import world as W

BLOCK = 500                 # the law is exact at this width, so every wider binning is an exact sum
HALF = 250                  # a 250 wide bin is exact; the scatter lives inside it
AMT_LO, AMT_HI = 500, 26000  # the stretch one shape covers, end to end
TAIL_HI = 60000
SCALE = 55000.0             # the density's own decay, the same shape in every segment
ROUND_SHARE = 0.45          # cash is counted in notes, so amounts pile on multiples of fifty
DISP = 0.0                  # how much of a Poisson record's scatter the block counts carry
GROWTH = 1.058              # the book's cash volume, prior year to reporting year


def shash(text):
    """A deterministic string hash: Python's own is salted per process."""
    h = 2166136261
    for ch in text:
        h = ((h ^ ord(ch)) * 16777619) & 0xFFFFFFFF
    return h


class Rng(object):
    """A small deterministic generator, so a rebuild is byte-identical."""

    def __init__(self, seed):
        self.s = (seed * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)

    def next(self):
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
        return (self.s >> 11) & ((1 << 53) - 1)

    def u(self):
        return self.next() / float(1 << 53)

    def below(self, n):
        return self.next() % n if n else 0

    def pick(self, seq):
        return seq[self.below(len(seq))]

    def shuffle(self, seq):
        for i in range(len(seq) - 1, 0, -1):
            j = self.below(i + 1)
            seq[i], seq[j] = seq[j], seq[i]
        return seq


def _z(key, i):
    """A standard normal drawn off a hashed stream, so the scatter is reproducible per block."""
    a = (shash("%s|%d|a" % (key, i)) + 1) / 4294967297.0
    b = shash("%s|%d|b" % (key, i)) / 4294967296.0
    return math.sqrt(-2.0 * math.log(a)) * math.cos(2.0 * math.pi * b)


def _law(level, x):
    """Deposits per 500 dollars at amount x. One shape from end to end: a gentle decay over the
    stretch the book's amounts cover, then a tail."""
    if x < AMT_HI:
        return level * math.exp(-(x - AMT_LO) / SCALE)
    tail = level * math.exp(-(AMT_HI - AMT_LO) / SCALE)
    return tail * (0.40 ** ((x - AMT_HI) / 1000.0))


def law_blocks(level, scale=1.0, key=""):
    """Deposit counts per 500 dollar block. The block count carries DISP of the scatter a
    Poisson record would show; at DISP 0 it is the law exactly."""
    out = []
    x = AMT_LO
    i = 0
    while x < TAIL_HI:
        mu = _law(level * scale, x + BLOCK / 2.0)
        n = mu + (DISP * math.sqrt(mu) * _z(key, i) if DISP and mu > 0 else 0.0)
        out.append((x, max(0, int(round(n)))))
        x += BLOCK
        i += 1
    return out


def _amounts(block_lo, n, rng):
    """A block's deposits, split exactly between its two halves and scattered inside each."""
    half = HALF
    a = _law(1.0, block_lo)
    b = _law(1.0, block_lo + BLOCK)
    mid = _law(1.0, block_lo + half)
    w1 = (a + mid) / 2.0
    w2 = (mid + b) / 2.0
    n1 = int(round(n * w1 / (w1 + w2)))
    return (_half_amounts(block_lo, n1, rng) +
            _half_amounts(block_lo + half, n - n1, rng))


def _half_amounts(block_lo, n, rng):
    """Place a block's deposits along the law's own slope across the block, a share of them on the
    multiples of fifty a counted cash take lands on. The block's count is exact, so any binning
    wider than a block is an exact sum and any narrower one follows the same curve."""
    if n <= 0:
        return []
    a = _law(1.0, block_lo)
    b = _law(1.0, block_lo + HALF)
    out = []
    fifties = [block_lo + 50 * i for i in range(HALF // 50)]
    # the same number on every multiple of fifty in the half block, so the pile on round figures
    # reads the same at any width a reader bins at and no sub-block edge cuts it unevenly
    per = int(n * ROUND_SHARE) // len(fifties)
    n_round = per * len(fifties)
    for v in fifties:
        for _ in range(per):
            out.append(float(v))
    for i in range(n - n_round):
        u = (i + 0.5) / float(n - n_round)
        if abs(b - a) < 1e-12 * a:
            t = u
        else:
            t = (math.sqrt(a * a + (b * b - a * a) * u) - a) / (b - a)
        cents = int(t * HALF * 20) * 5
        out.append(round(block_lo + min(cents, HALF * 100 - 5) / 100.0, 2))
    rng.shuffle(out)
    return out


def dates(lo, hi):
    a = dt.date(*[int(v) for v in lo.split("-")])
    b = dt.date(*[int(v) for v in hi.split("-")])
    out = []
    while a <= b:
        out.append(a)
        a += dt.timedelta(days=1)
    return out


# How a segment's customers trade: the share of deposits that land on a day the
# customer already paid in, and how much cash a trading day is worth.
TRADE = {
    "GRO": dict(pair=0.72, weekend=0.84, machine=0.58),
    "HOS": dict(pair=0.61, weekend=0.92, machine=0.44),
    "TRA": dict(pair=0.24, weekend=0.21, machine=0.31),
    "CON": dict(pair=0.19, weekend=0.14, machine=0.26),
    "RUR": dict(pair=0.27, weekend=0.33, machine=0.22),
    "FUE": dict(pair=0.78, weekend=0.88, machine=0.63),
    "PER": dict(pair=0.22, weekend=0.47, machine=0.35),
    "CLB": dict(pair=0.34, weekend=0.74, machine=0.29),
}


def customers(seed=19027):
    """The business banking book: one row per customer, with its own trading weight."""
    rng = Rng(seed)
    out = []
    n = 0
    for key, name, level, ratio, ncust, plant, pplant in W.SEGMENTS:
        for i in range(ncust):
            n += 1
            # a skewed trading weight: a few customers pay in many times, most rarely
            u = rng.u()
            weight = 0.25 + 7.5 * (u ** 3.2)
            br = rng.pick([b[0] for b in W.BRANCHES])
            opened = dt.date(2016, 1, 4) + dt.timedelta(days=rng.below(3800))
            out.append(dict(cust="AB%06d" % (100000 + n * 7 + rng.below(5)),
                            seg=key, branch=br, weight=weight,
                            opened=opened.isoformat(),
                            pair=TRADE[key]["pair"], machine=TRADE[key]["machine"],
                            weekend=TRADE[key]["weekend"]))
    seen, uniq = set(), []
    for c in out:
        while c["cust"] in seen:
            c["cust"] = "AB%06d" % (int(c["cust"][2:]) + 1)
        seen.add(c["cust"])
        uniq.append(c)
    return uniq


def _slots(custs, days, total, rng):
    """Deal `total` deposit slots out over customers and days, skewed by trading weight."""
    wsum = sum(c["weight"] for c in custs)
    slots = []
    for c in custs:
        share = c["weight"] / wsum
        k = int(total * share)
        if rng.u() < total * share - k:
            k += 1
        for _ in range(k):
            d = rng.pick(days)
            while d.weekday() >= 5 and rng.u() > c["weekend"]:
                d = rng.pick(days)
            slots.append([c["cust"], d, "machine" if rng.u() < c["machine"] else "counter"])
    # the pairing habit: a share of slots is moved onto a day the customer already used
    byc = {}
    for s in slots:
        byc.setdefault(s[0], []).append(s)
    pair = {c["cust"]: c["pair"] for c in custs}
    for cust, ss in byc.items():
        used = sorted({s[1] for s in ss})
        if not used:
            continue
        for s in ss:
            if rng.u() < pair[cust]:
                s[1] = used[rng.below(len(used))]
    rng.shuffle(slots)
    return slots


def build(seed=4471):
    """Every cash deposit of both reporting years, and the planted structuring events."""
    custs = customers()
    bycust = {c["cust"]: c for c in custs}
    byseg = {}
    for c in custs:
        byseg.setdefault(c["seg"], []).append(c)

    rows = []           # dicts: cust, date, channel, amount, year, planted
    truth = {}          # (year, seg) -> planted count
    for year, (lo, hi), scale in (("2027", (W.YEAR_LO, W.YEAR_HI), 1.0),
                                  ("2026", (W.PRIOR_LO, W.PRIOR_HI), 1.0 / GROWTH)):
        days = dates(lo, hi)
        for key, name, level, ratio, ncust, plant, pplant in W.SEGMENTS:
            rng = Rng(seed + shash(key + year) % 100000)
            amts = []
            for block_lo, n in law_blocks(level, scale, key + year):
                amts.extend(_amounts(block_lo, n, rng))
            rng.shuffle(amts)
            slots = _slots(byseg[key], days, len(amts), rng)
            while len(slots) < len(amts):
                c = rng.pick(byseg[key])
                slots.append([c["cust"], rng.pick(days), "counter"])
            for amt, (cust, day, chan) in zip(amts, slots):
                rows.append(dict(cust=cust, date=day, channel=chan, amount=amt,
                                 year=year, planted=0))
            truth[(year, key)] = plant if year == "2027" else pplant

    # Plant the structuring events. Each is one deposit inside 9,000 to 10,000 added to a
    # day on which the customer already paid cash in, so the day's cash reaches the
    # threshold while no single deposit does. Nothing is added anywhere else, so each
    # segment's profile away from the band is its ordinary trade and nothing else.
    # where a split take is paid in: round figures just under the threshold, and ragged ones
    PILES = [(9900.0, 0.21), (9950.0, 0.15), (9800.0, 0.11), (9500.0, 0.08), (9750.0, 0.05),
             (9700.0, 0.04), (9600.0, 0.03), (9850.0, 0.03)]
    byday = {}
    for r in rows:
        byday.setdefault((r["cust"], r["year"]), {}).setdefault(r["date"], []).append(r["amount"])
    planted_rows = []
    for year in ("2027", "2026"):
        for key, name, level, ratio, ncust, plant, pplant in W.SEGMENTS:
            want = plant if year == "2027" else pplant
            rng = Rng(seed + 991 + shash(key + year + "p") % 100000)
            # the customers who split are cash-heavy ones: the quartile that pays in most
            heavy = sorted(byseg[key], key=lambda c: (-c["weight"], c["cust"]))
            cand = []
            picked = []
            for frac in (3, 2, 1):
                pool = heavy[:max(24, len(heavy) // frac)]
                nstr = max(24, want // 2)
                strs = [pool[(i * 7919 + shash(key) % 1009) % len(pool)] for i in range(nstr * 5)]
                seen2 = {c["cust"] for c in picked}
                for c in strs:
                    if c["cust"] not in seen2:
                        seen2.add(c["cust"])
                        picked.append(c)
                    if len(picked) >= nstr * (4 - frac):
                        break
                cand = []
                for c in picked:
                    for day, amts in sorted(byday.get((c["cust"], year), {}).items()):
                        tot = sum(amts)
                        if tot >= 500 and all(x < W.THRESHOLD for x in amts):
                            cand.append((c["cust"], day, tot))
                if len(cand) >= want * 3:
                    break
            rng.shuffle(cand)
            made = 0
            for cust, day, tot in cand:
                if made >= want:
                    break
                u = rng.u()
                acc, amt = 0.0, None
                for v, w in PILES:
                    acc += w
                    if u <= acc:
                        amt = v
                        break
                if amt is None:                       # the ragged third of them
                    amt = round(9000 + rng.below(1000 * 20) * 5 / 100.0, 2)
                if tot + amt < W.THRESHOLD:
                    continue
                planted_rows.append(dict(cust=cust, date=day,
                                         channel="machine" if rng.u() < 0.3 else "counter",
                                         amount=amt, year=year, planted=1))
                made += 1
            truth[(year, key)] = made
    rows.extend(planted_rows)
    rows.sort(key=lambda r: (r["year"], r["date"], r["cust"], r["amount"]))
    return custs, bycust, rows, truth
