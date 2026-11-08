"""The scan provider's four-weekly point-of-sale units and dollars for the watched products' UPCs."""
import datetime as dt
import numpy as np
import sim
import world

CHANNELS = [("Drug", 0.46), ("Food", 0.27), ("Mass", 0.21), ("Dollar", 0.06)]
PRICE = {"FKJ": 7.49, "DOZ": 8.99, "GUM": 11.99, "EYE": 5.79, "NIC": 31.99, "IBC": 7.29, "VAP": 8.49, "CGH": 7.99,
         "FKI": 9.49, "ALC": 9.99, "IBT": 9.79, "FER": 6.49}
PRELIM_PERIODS = 1      # the latest four-week period ships as a preliminary release


def periods():
    """(start, end, label) of every 28-day period from the first Sunday of 2008 to the last one ending by END."""
    out = []
    start = sim.DAY0
    year_count = {}
    while start + dt.timedelta(days=27) <= sim.END:
        end = start + dt.timedelta(days=27)
        year_count[end.year] = year_count.get(end.year, 0) + 1
        out.append((start, end, "%d P%02d" % (end.year, year_count[end.year])))
        start = end + dt.timedelta(days=1)
    return out


def build(truth, seed):
    rng = np.random.default_rng(seed)
    per = periods()
    revised, prelim = [], []
    totals = {}       # product -> list of (start, end, units) summed over UPCs and channels (what a solver rebuilds)
    for p in sim.PRODUCTS:
        code = p["code"]
        buys = truth[code]["buys"]
        packs = world.META[code]["packs"]
        tot = []
        for k, (a, b, label) in enumerate(per):
            ia, ib = sim.day_index(a), sim.day_index(b)
            units = int(round(buys[ia:ib + 1].sum()))
            tot.append((a, b, units))
            if units == 0:
                continue
            ushare = np.array([x[3] for x in packs])
            cshare = np.array([c[1] for c in CHANNELS])
            cells = rng.multinomial(units, (ushare[:, None] * cshare[None, :]).ravel() / ushare.sum())
            cells = cells.reshape(len(packs), len(CHANNELS))
            for u, (upc, desc, _, _) in enumerate(packs):
                for c, (ch, _) in enumerate(CHANNELS):
                    n = int(cells[u, c])
                    if n == 0:
                        continue
                    price = PRICE[code] * (1 + 0.012 * (b.year - 2008)) * (0.93 if ch in ("Mass", "Dollar") else 1.0)
                    if u == 1 and code in ("DOZ", "GUM", "IBT", "NIC", "VAP"):
                        price *= 1.38 if code != "NIC" else 0.36
                    dollars = n * price * (1 + rng.normal(0, 0.01))
                    row = [b.isoformat(), label, upc, desc, ch, str(n), "%.2f" % dollars]
                    (prelim if k >= len(per) - PRELIM_PERIODS else revised).append((row, n))
        totals[code] = tot
    # the preliminary release under-reads the latest periods (late store files), the revision is the history
    prelim_rows = []
    for row, n in prelim:
        pn = int(round(n * (0.962 + 0.03 * rng.random())))
        r = list(row)
        r[5] = str(pn)
        r[6] = "%.2f" % (float(row[6]) * pn / n)
        prelim_rows.append(r)
    return [r for r, _ in revised], prelim_rows, totals, per
