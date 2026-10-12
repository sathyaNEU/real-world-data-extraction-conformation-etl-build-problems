"""Files supplied with the run that the forecast and the cost averages do not use: care at home hours by locality,
and the latest inspection grades of Strathallan's care homes."""
import datetime as dt

import numpy as np
import pandas as pd

import world as W


def homecare(rng):
    rows = []
    base = {"Allanvale": 9150, "Braeburn": 6020, "Carsefield": 7480, "Dunmorrow": 6610, "Kirkhallam": 5230}
    clients = {"Allanvale": 612, "Braeburn": 401, "Carsefield": 507, "Dunmorrow": 446, "Kirkhallam": 352}
    for y in (2024, 2025, 2026):
        for m in range(1, 13):
            days = (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.date(y, m, 1)).days
            for loc in W.LOCS:
                trend = 1 + 0.018 * (y - 2024 + (m - 1) / 12)
                season = 1 + 0.035 * np.cos(2 * np.pi * (m - 1) / 12)
                planned = base[loc] * trend * season * days / 30.4 * rng.normal(1, 0.012)
                gap = rng.uniform(0.02, 0.075) * (1.3 if m in (12, 1, 2) else 1.0)
                delivered = planned * (1 - gap)
                cl = int(round(clients[loc] * trend * rng.normal(1, 0.015)))
                rows.append(dict(month="%d-%02d" % (y, m), locality=loc, people_receiving=cl,
                                 planned_hours="%.1f" % planned, delivered_hours="%.1f" % delivered,
                                 unmet_hours="%.1f" % (planned - delivered)))
    return pd.DataFrame(rows)


def grades(reg, rng):
    rows = []
    cur = reg[reg["cancelled"] == ""]
    for r in cur.itertuples(index=False):
        reg_d = dt.date.fromisoformat(r.registered)
        insp = dt.date(2026, 1, 5) + dt.timedelta(days=int(rng.integers(0, 330)))
        if reg_d > dt.date(2025, 1, 1):
            insp = max(insp, reg_d + dt.timedelta(days=int(rng.integers(150, 300))))
        insp = min(insp, dt.date(2026, 12, 9) - dt.timedelta(days=int(rng.integers(0, 40))))
        g = lambda: int(np.clip(round(rng.normal(4.1, 0.8)), 2, 6))
        rows.append(dict(service_no=r.service_no, service_name=r.service_name, inspection_date=insp.isoformat(),
                         wellbeing=g(), leadership=g(), staff_team=g(), setting=g(), care_planning=g(),
                         complaints_upheld_12m=int(rng.poisson(0.6))))
    df = pd.DataFrame(rows)
    return df.sort_values("service_name", kind="stable").reset_index(drop=True)
