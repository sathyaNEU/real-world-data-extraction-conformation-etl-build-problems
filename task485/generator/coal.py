"""Coal: each site's yard takes its suppliers' trucks and trains on a call-off and is fired well mixed, so the sulphur
a boiler fires on a day is its yard's blend that day. Every lot carries its supplier laboratory's analysis."""
import numpy as np

import world as W


PRE = 31   # the collation reaches back to lots dispatched from 1 December 2025
TRUCK = (27.5, 31.5)
WAGON = (54.0, 60.0)


def _analysis(rng, p):
    return dict(s=float(np.round(max(0.25, rng.normal(p["s"], p["sd"])), 2)),
                tm=float(np.round(max(4.0, rng.normal(p["tm"], 0.8)), 1)),
                ash=float(np.round(max(6.0, rng.normal(p["ash"], 0.9)), 1)),
                c=float(np.round(rng.normal(p["c"], 0.7), 1)), gcv=float(np.round(rng.normal(p["gcv"], 0.35), 2)))


def deliveries(w):
    """one row per truck or wagon received at a site. Trucks run Monday to Saturday on a daily call-off that holds
    the yard near its target stock; Ostmouth's trains run Monday to Friday when its share of the call-off fills a
    train. A supplier's laboratory analyses each day's dispatch to a customer as one lot (a train is one lot), so the
    trucks or wagons of one dispatch share a certificate."""
    lots = []
    lot_no = [0]
    w.yard = {}
    by_site = {}
    for b in w.B:
        by_site.setdefault(b["site"], []).append(b)
    for site in sorted(by_site):
        rng = W.stream(21, int(site[1:]))
        bs = by_site[site]
        burn = sum(b["coal_day"] for b in bs)
        mean = burn[burn > 0].mean()
        # December 2026's firing stands in for December 2025's, so the yard enters 2026 as it ran
        full = np.concatenate([burn[W.DAYS - PRE:], burn])
        segs = bs[0]["mix"]
        target = mean * rng.uniform(10, 14)
        stock = float(np.round(target * rng.uniform(0.9, 1.1)))
        s_yard = sum(sh * W.SUPPLIERS[s]["s"] for s, sh in segs[0][1].items()) / 100
        g_yard = sum(sh * W.SUPPLIERS[s]["gcv"] for s, sh in segs[0][1].items())
        s_day = np.zeros(W.DAYS)
        g_day = np.zeros(W.DAYS)
        stock_q = {}
        opening = None
        train = int(np.clip(round(mean * rng.uniform(5, 7) / 57.0), 4, 16))
        for i in range(PRE + W.DAYS):
            d = i - PRE
            if d == 0:
                opening = stock
            mix = [m for d0, m in segs if d0 <= max(d, 0)][-1]
            dow = W.day(d).weekday()
            recent = float(np.mean(full[max(0, i - 7):i])) if i else mean
            call = max(0.0, recent * 7 / 6 + 0.18 * (target - stock)) if dow < 6 else 0.0
            for sup in sorted(mix):
                share = mix[sup]
                p = W.SUPPLIERS[sup]
                if sup == "Ostmouth Coal Imports":
                    n = train if (dow < 5 and 1.1 * target - stock >= share * train * 57.0) else 0
                    lag = int(rng.integers(2, 5))
                    size = WAGON
                else:
                    n = int(np.floor(share * call / 29.5 + rng.random()))
                    lag = int(rng.integers(0, 2))
                    size = TRUCK
                if n == 0:
                    continue
                a = _analysis(rng, p)
                lot_no[0] += 1
                for _ in range(n):
                    t = float(np.round(rng.uniform(*size), 2))
                    lots.append(dict(site=site, supplier=sup, received=d, dispatched=d - lag, t=t,
                                     rail=size == WAGON, lot=lot_no[0], **a))
                    s_yard = (s_yard * stock + a["s"] / 100 * t) / (stock + t)
                    g_yard = (g_yard * stock + a["gcv"] * t) / (stock + t)
                    stock += t
            if d >= 0:
                s_day[d] = s_yard
                g_day[d] = g_yard
            stock -= full[i]
            if stock < 0:
                raise RuntimeError("yard ran out at %s day %d" % (site, d))
            if d in (89, 180, 272, 364):
                stock_q[d] = stock
        for b in bs:
            b["s_day"] = s_day
            b["gcv_day"] = g_day
        w.yard[site] = dict(opening=opening, stock_q=stock_q, s_day=s_day)
    # lots dispatched before the collation's first day are not in it
    lots = [x for x in lots if x["dispatched"] >= -PRE]
    # a few dispatches in the last days of 2026 arrive in 2027 and are not 2026 receipts
    late = []
    for site in sorted(by_site):
        rng = W.stream(22, int(site[1:]))
        for _ in range(int(rng.integers(0, 3))):
            sup = sorted(by_site[site][0]["mix"][-1][1])[0]
            p = W.SUPPLIERS[sup]
            rail = sup == "Ostmouth Coal Imports"
            a = _analysis(rng, p)
            lot_no[0] += 1
            disp = int(rng.integers(361, 365))
            rec = int(rng.choice([366, 368]))        # Saturday 2 or Monday 4 January 2027
            for _ in range(int(rng.integers(2, 6))):
                late.append(dict(site=site, supplier=sup, received=rec, dispatched=disp,
                                 t=float(np.round(rng.uniform(*(WAGON if rail else TRUCK)), 2)), rail=rail,
                                 lot=lot_no[0], **a))
    # a laboratory re-issues a certificate after a check sample: the ash, carbon and calorific value move, the
    # sulphur never does
    seen = {}
    for x in lots + late:
        if x["lot"] not in seen:
            seen[x["lot"]] = bool(W.stream(23, int(x["site"][1:]), x["lot"]).random() < 0.021)
        x["reissued"] = seen[x["lot"]]
    w.lots = sorted(lots + late, key=lambda x: (x["received"], x["site"], x["supplier"]))
    return w.lots
