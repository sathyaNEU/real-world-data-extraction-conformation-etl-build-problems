"""November: the client forecast revisions (in each client's unit and calendar), the accepted revision the
plan of record is built from, the plan's daily key fields by stream, and the November roster."""
import datetime as dt
import math

import numpy as np
import pandas as pd

import world as W

DAY = dt.timedelta(days=1)
SAT_CLIENTS = {"NDS", "BMC", "WBH", "CIP", "HPY"}
CLOSED = {dt.date(2026, 11, 26): {"KBA", "NDS", "HPB"}}


def working(client, d):
    if d.weekday() == 6:
        return False
    if d.weekday() == 5 and client not in SAT_CLIENTS:
        return False
    if client in CLOSED.get(d, set()):
        return False
    return True


def week_start(client, d):
    """the client's forecast week containing d: US weeks run Sunday to Saturday; Australian fiscal weeks and UK
    weeks run Monday to Sunday"""
    if W.CLIENTS[client]["region"] == "US":
        return d - dt.timedelta(days=(d.weekday() + 1) % 7)
    return d - dt.timedelta(days=d.weekday())


def fiscal_week_au(d):
    """Wattlebird's and Coolabah's fiscal week number: FY27 week 1 is the Monday-to-Sunday week holding 1 July 2026"""
    w1 = dt.date(2026, 6, 29)
    return (d - w1).days // 7 + 1


def nov_weeks(client):
    out = []
    d = week_start(client, W.NOV[0])
    while d <= W.NOV[1]:
        out.append(d)
        d += dt.timedelta(days=7)
    return out


# accepted weekday documents a day per stream (the plan of record), and each revision's multiplier on it
REV = {  # client: list of (revision label, sent date, factor on the accepted volume); the accepted one has factor 1
    "KBA": [("R1", dt.date(2026, 9, 24), 0.955), ("R2", dt.date(2026, 10, 12), 1.0), ("R3", dt.date(2026, 10, 21), 1.062)],
    "NDS": [("v1", dt.date(2026, 9, 28), 1.047), ("v2", dt.date(2026, 10, 9), 1.0), ("v3", dt.date(2026, 10, 20), 0.938)],
    "BMC": [("Rev A", dt.date(2026, 9, 30), 0.951), ("Rev B", dt.date(2026, 10, 14), 1.0), ("Rev C", dt.date(2026, 10, 22), 1.071)],
    "HPB": [("1", dt.date(2026, 9, 25), 1.058), ("2", dt.date(2026, 10, 13), 1.0), ("3", dt.date(2026, 10, 19), 0.952)],
    "WBH": [("FC-11", dt.date(2026, 9, 29), 0.962), ("FC-12", dt.date(2026, 10, 13), 1.0), ("FC-13", dt.date(2026, 10, 21), 1.048)],
    "CIP": [("Oct-a", dt.date(2026, 10, 2), 1.066), ("Oct-b", dt.date(2026, 10, 14), 1.0), ("Oct-c", dt.date(2026, 10, 22), 0.941)],
    "WPC": [("1", dt.date(2026, 9, 30), 0.948), ("2", dt.date(2026, 10, 12), 1.0), ("3", dt.date(2026, 10, 20), 1.056)],
    "TCM": [("A", dt.date(2026, 10, 1), 1.052), ("B", dt.date(2026, 10, 15), 1.0), ("C", dt.date(2026, 10, 22), 0.938)],
    "HPY": [("1", dt.date(2026, 9, 18), 0.931), ("2", dt.date(2026, 10, 14), 1.0)],
}
ACCEPTED = {"KBA": "R2", "NDS": "v2", "BMC": "Rev B", "HPB": "2", "WBH": "FC-12", "CIP": "Oct-b", "WPC": "2", "TCM": "B", "HPY": "2"}
WEEK_WOBBLE = [1.000, 1.018, 0.991, 1.007, 0.984, 1.012]


def weekly_forecasts():
    """every revision's weekly volume for every stream, in the client's unit (H&P in bundles of 25 documents)"""
    rows = []
    for code, s in W.STREAMS.items():
        c = s["client"]
        for wi, ws in enumerate(nov_weeks(c)):
            wdays = [ws + dt.timedelta(days=i) for i in range(7)]
            base = 0.0
            for d in wdays:
                if working(c, d):
                    base += s["kf"] / W.kfpd(code, d)
            base *= WEEK_WOBBLE[wi % len(WEEK_WOBBLE)]
            for label, sent, f in REV[c]:
                v = base * f
                if code == "D6":
                    v = int(round(v / W.HP_BUNDLE))
                else:
                    v = int(round(v))
                rows.append(dict(code=code, client=c, revision=label, sent=sent, week_start=ws, units=v,
                                 accepted=(label == ACCEPTED[c])))
    return pd.DataFrame(rows)


def spread(units, wdays):
    """documents spread evenly over the week's working days, the remainder to the earliest days"""
    n = len(wdays)
    if n == 0:
        return {}
    q, r = divmod(units, n)
    return {d: q + (1 if i < r else 0) for i, d in enumerate(wdays)}


def plan_daily(fc):
    """the plan of record's documents and key fields by stream and shift-day, 1 to 30 November"""
    rows = []
    acc = fc[fc.accepted]
    for r in acc.itertuples():
        c = r.client
        wdays = [r.week_start + dt.timedelta(days=i) for i in range(7)]
        wdays = [d for d in wdays if working(c, d)]
        docs_total = r.units * (W.HP_BUNDLE if r.code == "D6" else 1)
        for d, n in spread(docs_total, wdays).items():
            if W.NOV[0] <= d <= W.NOV[1]:
                rows.append(dict(code=r.code, day=d, docs=n, kfpd=W.kfpd(r.code, d), kf=n * W.kfpd(r.code, d)))
    return pd.DataFrame(rows).sort_values(["day", "code"]).reset_index(drop=True)


def roster(P):
    """the November roster: experienced verifiers on days for the go-live, the October joiners and the
    least experienced of the rest on nights"""
    active = P[(P.leave.isna()) | (P.leave > dt.date(2026, 11, 30))].copy()
    active["ten"] = [(dt.date(2026, 11, 15) - h).days for h in active.hire]
    new = active[active.hire >= dt.date(2026, 10, 1)]
    rest = active[active.hire < dt.date(2026, 10, 1)].sort_values(["ten", "emp"], ascending=[False, True])
    n_day = 21
    day = rest.head(n_day)
    night = pd.concat([rest.iloc[n_day:], new])
    out = pd.concat([day.assign(queue="D"), night.assign(queue="N")])
    return out[["pid", "emp", "badge", "hire", "queue"]].reset_index(drop=True)


def days_in_nov():
    return [W.NOV[0] + DAY * i for i in range((W.NOV[1] - W.NOV[0]).days + 1)]
