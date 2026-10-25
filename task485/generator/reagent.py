"""Limestone: each scrubber has its own silo, filled by quarry trucks on a reorder policy and drawn by the absorber's
dosing (its operating ratio of calcium carbonate per mole of sulphur dioxide removed), so the limestone a scrubber
consumes over the year is set by the sulphur it removed. Purity is certified weekly by each quarry."""
import numpy as np

import world as W

SITE_QUARRY = {"S01": "Bromscar Quarry", "S02": "Molhope Lime and Stone", "S03": "Bromscar Quarry",
               "S04": "Molhope Lime and Stone", "S05": "Molhope Lime and Stone", "S06": "Bromscar Quarry",
               "S07": "Bromscar Quarry", "S08": "Molhope Lime and Stone", "S09": "Bromscar Quarry",
               "S10": "Bromscar Quarry", "S11": "Molhope Lime and Stone", "S12": "Bromscar Quarry",
               "S13": "Molhope Lime and Stone", "S14": "Molhope Lime and Stone", "S15": "Bromscar Quarry",
               "S16": "Molhope Lime and Stone"}


def weekly_purity(rng):
    """each quarry's certified calcium carbonate for each ISO week of 2026 (weeks 1 to 53), per cent as delivered"""
    out = {}
    for q, p in W.QUARRIES.items():
        walk = np.cumsum(rng.normal(0, p["sd"] * 0.35, 54))
        walk = walk - walk.mean()
        out[q] = np.round(np.clip(p["caco3"] + walk + rng.normal(0, p["sd"] * 0.4, 54), 90.5, 98.5), 1)
    return out


def iso_week(d):
    return W.day(d).isocalendar()[1]


def silos(w):
    w.purity = weekly_purity(np.random.default_rng(W.SEED + 31))
    tickets = []
    for b in w.B:
        rng = W.stream(31, *W.key(b))
        q = SITE_QUARRY[b["site"]]
        use = b["caco3_day"]
        mean = max(use[use > 0].mean(), 0.5)
        cap = 30.0 * int(np.ceil(mean * 12 / 30.0)) + 30.0
        stock = float(np.round(mean * rng.uniform(5, 9), 1))
        pur_silo = W.QUARRIES[q]["caco3"] / 100
        opening = stock
        stock_q = {}
        for d in range(W.DAYS):
            # morning delivery when the silo is low, then the day's dosing
            need_t = use[d] / pur_silo
            if stock - need_t < mean / pur_silo * 3.5 and use[d] > 0:
                while stock < cap - 32:
                    t = float(np.round(rng.uniform(26.0, 29.6), 2))
                    pur = w.purity[q][iso_week(d)] / 100
                    pur_silo = (pur_silo * stock + pur * t) / (stock + t)
                    stock += t
                    tickets.append(dict(site=b["site"], unit=b["unit"], boiler=b["id"], quarry=q, day=d, t=t))
            stock -= use[d] / pur_silo
            if stock < 0:
                raise RuntimeError("silo ran dry at %s day %d" % (b["id"], d))
            if d in (89, 180, 272, 364):
                stock_q[d] = stock
        b["silo"] = dict(opening=opening, stock_q=stock_q, cap=cap, quarry=q)
    w.tickets = sorted(tickets, key=lambda x: (x["day"], x["quarry"], x["boiler"]))
    return w.tickets
