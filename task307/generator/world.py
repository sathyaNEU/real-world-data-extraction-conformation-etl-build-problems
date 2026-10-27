"""The Merrimont subarea world: network, zones and the 2028 (and 2025 base) peak-hour trip tables."""
import numpy as np
import params as P
import net

ATTACH = {"W1": "A1", "W2": "A2", "W3": "A3", "W4": "A4", "W5": "F1", "W6": "F2",
          "Z_DT1": "DT1", "Z_DT2": "DT2", "Z_E": "EF", "Z_P": "C1"}


def zones():
    return {z: m for m, zs in P.SUBZONES.items() for z in zs}


def network():
    conn = [(str(z), ATTACH[m]) for z, m in zones().items()]
    p = dict(P.LANES, connectors=conn)
    return net.build_network(p)


def macro_am():
    tot = sum(P.W_SHARE.values())
    am = {}
    for w, s in P.W_SHARE.items():
        s = s / tot * 9000 * P.SCALE
        am[(w, "Z_DT1")] = s * P.DT_SHARE * 0.65
        am[(w, "Z_DT2")] = s * P.DT_SHARE * 0.35
        am[(w, "Z_E")] = s * (1 - P.DT_SHARE) * 0.7
        am[(w, "Z_P")] = s * (1 - P.DT_SHARE) * 0.3
    return am


def subzone_weights(rng):
    return {z: rng.uniform(0.6, 1.4) for z in zones()}


def trip_tables(seed_offset=0, growth=1.0):
    """Integer AM and PM peak-hour trip tables at subzone level, keyed by zone-number strings."""
    rng = np.random.default_rng(P.SEED + seed_offset)
    wz = subzone_weights(rng)
    tabs = {}
    for period in ("AM", "PM"):
        main = macro_am()
        mac = {}
        for (o, d), q in main.items():
            if period == "AM":
                mac[(o, d)] = mac.get((o, d), 0) + q
                mac[(d, o)] = mac.get((d, o), 0) + q * P.COUNTER
            else:
                mac[(d, o)] = mac.get((d, o), 0) + q * P.PM_FACTOR
                mac[(o, d)] = mac.get((o, d), 0) + q * P.PM_FACTOR * P.COUNTER
        for (o, d), q in P.LOCAL.items():
            mac[(o, d)] = mac.get((o, d), 0) + q
            mac[(d, o)] = mac.get((d, o), 0) + q
        od = {}
        for (mo, md), q in mac.items():
            zo = P.SUBZONES[mo]; zd = P.SUBZONES[md]
            w = np.array([[wz[a] * wz[b] for b in zd] for a in zo])
            w = w / w.sum() * q * growth
            for i, a in enumerate(zo):
                for j, b in enumerate(zd):
                    od[(str(a), str(b))] = od.get((str(a), str(b)), 0) + w[i, j]
        # integerise with largest remainder, deterministic
        keys = sorted(od)
        vals = np.array([od[k] for k in keys])
        fl = np.floor(vals)
        short = int(round(vals.sum() - fl.sum()))
        order = np.argsort(-(vals - fl), kind="stable")
        fl[order[:short]] += 1
        tabs[period] = {k: int(v) for k, v in zip(keys, fl) if v > 0}
    return tabs
