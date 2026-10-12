"""Sector configurations: the supervisors' configuration log for May to September 2026 (local time), the
configuration table in force from 14 July 2026 (revision 9, the current table file) and the table it replaced
(revision 8, in the operations manual of 26 March 2026). Revision 9 regrouped three day configurations."""
import datetime as dt

import numpy as np

import world as W

SEED = 18147
LOG_FROM = dt.date(2026, 5, 1)
LOG_TO = dt.date(2026, 9, 30)

SAME = {
    "C8": [["TRV"], ["MSB"], ["GRD"], ["LNM"], ["KRW"], ["LYS"], ["HAL"], ["SDV"]],
    "C7A": [["TRV"], ["MSB"], ["GRD", "KRW"], ["LNM"], ["LYS"], ["HAL"], ["SDV"]],
    "C7B": [["TRV"], ["MSB"], ["GRD"], ["LNM", "HAL"], ["KRW"], ["LYS"], ["SDV"]],
    "N3": [["TRV", "LYS", "GRD"], ["MSB", "SDV", "LNM"], ["KRW", "HAL"]],
    "N2": [["TRV", "LYS", "GRD", "KRW", "HAL"], ["MSB", "SDV", "LNM"]],
}
REV8 = dict(SAME, **{
    "C6A": [["TRV"], ["MSB"], ["GRD", "KRW"], ["LNM", "HAL"], ["LYS"], ["SDV"]],
    "C6B": [["TRV"], ["MSB", "SDV"], ["GRD"], ["LNM"], ["KRW", "HAL"], ["LYS"]],
    "C5": [["TRV", "LYS"], ["MSB"], ["GRD", "KRW"], ["LNM", "HAL"], ["SDV"]],
})
REV9 = dict(SAME, **{
    "C6A": [["TRV"], ["MSB"], ["GRD", "HAL"], ["LNM"], ["KRW"], ["LYS", "SDV"]],
    "C6B": [["TRV"], ["MSB", "LNM"], ["GRD", "KRW"], ["LYS"], ["HAL"], ["SDV"]],
    "C5": [["TRV"], ["MSB", "SDV"], ["GRD", "KRW", "HAL"], ["LNM"], ["LYS"]],
})
ORDER = ["C8", "C7A", "C7B", "C6A", "C6B", "C5", "N3", "N2"]
PURPOSE = {"C8": "full split, peak hours", "C7A": "Grendal and Karrow combined",
           "C7B": "Linmark and Hallin combined", "C6A": "morning and shoulder traffic",
           "C6B": "afternoon and evening shoulder", "C5": "early morning and late evening",
           "N3": "night, three positions", "N2": "night, two positions"}

REMARKS = [
    "Lysvik split early, eastbound wave building", "Handover briefing on Tarvik, no configuration change",
    "Mosby/Sandvik combined on request of SDV executive", "CB activity south, Sandvik kept open",
    "OJT on Grendal position", "Military area active, Karrow traffic rerouted", "FDPS degraded mode 10 min, no impact",
    "Staffing short on night shift", "Sector monitoring values exceeded on Lysvik", "Linmark opened for northbound wave",
    "Hallin combined early, light traffic", "Supervisor handover",
]


def alone(table, code):
    return {g[0] for g in table[code] if len(g) == 1}


def log_rows():
    """The day's changes as the supervisors logged them (local time, to the minute)."""
    rng = np.random.default_rng(SEED)
    rows = []
    day = LOG_FROM - dt.timedelta(days=1)
    while day <= LOG_TO:
        wk = day.weekday()
        busy = W.MONTH[day.month] * W.WEEKDAY[wk]
        plan = []
        plan.append((5 * 60 + int(rng.integers(10, 50)), "C5"))
        plan.append((6 * 60 + int(rng.integers(30, 80)), "C6A" if rng.random() < 0.62 else "C6B"))
        if busy > 0.96:
            plan.append((8 * 60 + int(rng.integers(0, 95)), "C7A" if rng.random() < 0.5 else "C8"))
            plan.append((10 * 60 + int(rng.integers(30, 120)), "C8"))
        else:
            plan.append((9 * 60 + int(rng.integers(0, 90)), "C7A" if rng.random() < 0.55 else "C7B"))
        plan.append((14 * 60 + int(rng.integers(20, 130)), ["C7B", "C6A", "C7A"][int(rng.integers(3))]))
        if busy > 0.93:
            plan.append((17 * 60 + int(rng.integers(0, 110)), "C8" if rng.random() < 0.6 else "C7A"))
        plan.append((20 * 60 + int(rng.integers(0, 80)), "C6B"))
        plan.append((21 * 60 + 40 + int(rng.integers(0, 50)), "C5"))
        plan.append((23 * 60 + int(rng.integers(0, 50)), "N3" if busy > 0.9 or rng.random() < 0.5 else "N2"))
        last = None
        for minute, code in plan:
            if code == last:
                continue
            t = dt.datetime.combine(day, dt.time(0)) + dt.timedelta(minutes=minute)
            rem = REMARKS[int(rng.integers(len(REMARKS)))] if rng.random() < 0.08 else ""
            sup = ["JHL", "MKR", "TBS", "AVN", "SOE", "LKD"][(day.toordinal() + (minute > 14 * 60)) % 6]
            rows.append(dict(local=t, code=code, remark=rem, sup=sup))
            last = code
        day += dt.timedelta(days=1)
    # the revision taking effect: the supervisor re-enters the running configuration at 06:00 on 14 July
    switch = W.CONFIG_REV9.replace(tzinfo=None)
    before = [r for r in rows if r["local"] <= switch]
    running = before[-1]["code"]
    rows.append(dict(local=switch, code=running, sup="TBS",
                     remark="Configuration table revision 9 (OM Part 3 amdt 2026/2) in force from 0600"))
    rows.sort(key=lambda r: (r["local"], r["code"]))
    return clean_bins(rows, dt.datetime(2026, 6, 1), dt.datetime(2026, 9, 1))


def clean_bins(rows, start, end):
    """Nudge logged times by a minute or two (never the revision entry) until every sector's hours alone in the
    season sit away from a rounding edge at one decimal: whole minutes modulo 6 of 0, 1 or 5."""
    rng = np.random.default_rng(SEED + 7)

    def bad_of(rs):
        h = hours_alone(rs, start, end)
        return [s for s in W.SECTORS if int(round(h[s] * 60)) % 6 not in (0, 1, 5)]
    switch = W.CONFIG_REV9.replace(tzinfo=None)
    idx = [k for k in range(1, len(rows) - 1) if start <= rows[k]["local"] < end and rows[k]["local"] != switch]
    bad = bad_of(rows)
    for _ in range(400):
        if not bad:
            return rows
        k = idx[int(rng.integers(len(idx)))]
        for d in (1, -1, 2, -2):
            new = rows[k]["local"] + dt.timedelta(minutes=d)
            if not rows[k - 1]["local"] < new < rows[k + 1]["local"]:
                continue
            old = rows[k]["local"]
            rows[k]["local"] = new
            b2 = bad_of(rows)
            if len(b2) < len(bad):
                bad = b2
                break
            rows[k]["local"] = old
    raise SystemExit("configuration log hours did not settle mid-bin")


def table_for(t_local):
    return REV9 if t_local >= W.CONFIG_REV9.replace(tzinfo=None) else REV8


def hours_alone(rows, start, end, table_at=table_for):
    """Hours each sector was open on its own position between two local datetimes."""
    out = {s: 0.0 for s in W.SECTORS}
    for k, r in enumerate(rows):
        a = r["local"]
        b = rows[k + 1]["local"] if k + 1 < len(rows) else dt.datetime.combine(LOG_TO + dt.timedelta(days=1), dt.time(0))
        a2, b2 = max(a, start), min(b, end)
        if b2 <= a2:
            continue
        tab = table_at(a)
        for s in alone(tab, r["code"]):
            out[s] += (b2 - a2).total_seconds() / 3600.0
    return out
