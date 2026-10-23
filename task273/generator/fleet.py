"""Who runs the vehicles: the commission's licensed operators and their fleet returns, the platforms' quarterly
reports, and the motor vehicle registrations. None of them counts miles."""
import datetime as dt

import numpy as np

import common as K
import events as EV
import world as W

MPV = {"TX": 42000, "RH": 11000, "LM": 26000, "AS": 48000, "PT": 28000, "PD": 21000, "AD": 6500, "PV": 10200}
FLEET_USES = ("TX", "LM", "AS", "PT", "PD")
PLATFORM_USES = ("RH", "AD")


def use_miles(u, y):
    if u == "PV":
        tot = W.VMT_TOTAL[y]
        return tot * (1.0 - sum(W.SHARE[x][y] for x in W.SHARE))
    return W.SHARE[u][y] * W.VMT_TOTAL[y]


def operators(seed=K.SEED):
    rng = np.random.default_rng(seed * 1000 + 53)
    rows, ids = [], {}
    n = 0
    for u in K.CODES:
        for name, variants, share in EV.OPERATORS[u]:
            n += 1
            oid = "OP%04d" % (100 + n * 3)
            ids[name] = oid
            start = dt.date(2009 + int(rng.integers(0, 12)), int(rng.integers(1, 13)), 1)
            if u in PLATFORM_USES:
                start = dt.date(2016 + int(rng.integers(0, 3)), int(rng.integers(1, 13)), 1)
            lic = "%s-%05d" % ({"TX": "TXI", "RH": "TNC", "LM": "LIM", "AS": "SHU", "PT": "PAR", "PD": "PCL",
                                "AD": "DNC"}[u], 1000 + n * 37)
            rows.append([oid, name, K.LABEL[u], lic, start, dt.date(2027, 6, 30), "; ".join([name] + variants)])
    return rows, ids


def fleet_returns(seed=K.SEED):
    rng = np.random.default_rng(seed * 1000 + 59)
    _, ids = operators(seed)
    rows = []
    for u in FLEET_USES:
        for name, variants, share in EV.OPERATORS[u]:
            for y in range(2020, 2026):
                miles = 0.5 * (use_miles(u, max(2021, y)) + use_miles(u, min(2025, y + 1)))
                v = miles / MPV[u] * share * float(np.exp(rng.normal(0, 0.04)))
                rows.append([ids[name], name, K.LABEL[u], "%d-%02d" % (y, (y + 1) % 100), int(round(v))])
    return rows


def platform_quarters(seed=K.SEED):
    rng = np.random.default_rng(seed * 1000 + 61)
    head = ["PLATFORM", "SERVICE", "QUARTER", "ACTIVE_VEHICLES", "ACTIVE_DRIVERS", "TRIPS"]
    rows = []
    trip = {"RH": 6.4, "AD": 3.9}
    for u in PLATFORM_USES:
        for name, variants, share in EV.OPERATORS[u]:
            for y in K.YEARS:
                for q in range(1, 5):
                    miles = use_miles(u, y) / 4.0 * share * float(np.exp(rng.normal(0, 0.03)))
                    veh = miles / (MPV[u] / 4.0) * 1.35        # vehicles with any trip in the quarter
                    drv = veh * (1.06 + 0.02 * rng.random())
                    trips = miles * 0.62 / trip[u]
                    label = "%dQ%d" % (y, q)
                    if name == "Basketrun":                     # reports by quarter end date
                        label = (dt.date(y, 3 * q, 1) + dt.timedelta(days=31)).replace(day=1) - dt.timedelta(days=1)
                        label = label.isoformat()
                    rows.append([name.upper(), "ride-hail" if u == "RH" else "delivery", label, int(round(veh)),
                                 int(round(drv)), int(round(trips, -2))])
    return head, rows


def registrations(seed=K.SEED):
    rng = np.random.default_rng(seed * 1000 + 67)
    blocks = {}
    for y in K.YEARS:
        pv = use_miles("PV", y) / MPV["PV"]
        mix = [("Passenger cars", 0.43), ("Sport utility vehicles", 0.33), ("Pickups", 0.16), ("Vans", 0.08)]
        out = []
        for name, s in mix:
            a = int(round(pv * s * float(np.exp(rng.normal(0, 0.01)))))
            b = int(round(a * {"Passenger cars": 0.004, "Sport utility vehicles": 0.006, "Pickups": 0.09,
                               "Vans": 0.12}[name]))
            c = int(round(a * {"Passenger cars": 0.0012, "Sport utility vehicles": 0.0006, "Pickups": 0.0,
                               "Vans": 0.004}[name]))
            d = int(round(a * 0.006))
            out.append((name, a, b, c, d))
        out.append(("Motorcycles", int(round(pv * 0.052)), 0, 0, int(round(pv * 0.0002))))
        out.append(("Trucks over 10,000 lb", int(round(pv * 0.004)), int(round(pv * 0.021)), 0,
                    int(round(pv * 0.002))))
        out.append(("Buses", 12, int(round(pv * 0.0004)), int(round(pv * 0.0009)), int(round(pv * 0.0011))))
        blocks[y] = out
    return blocks
