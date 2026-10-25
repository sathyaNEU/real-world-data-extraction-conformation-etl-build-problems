"""Dated alterations to the register around the old system's last two registers: when each elector at a dwelling was
added (determined) and deleted, consistent with every 1 December register the world counts. Electra published them as
monthly notices of alteration from January to September, and its last three in January to March 2022 before the
council replaced it; the register Electra held when it was switched off is the 2021 register with those three applied.

The world counts a household's electors on the register of year Y when the household is in residence in October Y
and each elector's register year is Y or earlier (world.count_on); here each such elector is given a determination
date inside the window that register year allows (after 31 October of the year before, by 31 October of the year
itself, and after the household arrived), and each departed household's electors a deletion date after it left and
by the 31 October before the next register."""
import datetime as dt

import numpy as np

import world as W

D = dt.date
WINDOW = (D(2020, 11, 1), D(2022, 2, 28))      # determinations Electra's notices of January 2021 to March 2022 carry
SWITCH_OFF = D(2022, 3, 4)                     # the register Electra held at the switch-off: the 1 March 2022 notice applied
NOTICE_DATES = {(2021, 1): D(2021, 1, 4), (2021, 2): D(2021, 2, 1), (2021, 3): D(2021, 3, 1), (2021, 4): D(2021, 4, 1),
                (2021, 5): D(2021, 5, 4), (2021, 6): D(2021, 6, 1), (2021, 7): D(2021, 7, 1), (2021, 8): D(2021, 8, 2),
                (2021, 9): D(2021, 9, 1), (2022, 1): D(2022, 1, 4), (2022, 2): D(2022, 2, 1), (2022, 3): D(2022, 3, 1)}
P_ROLL_REG = 0.40      # an elector's application determined between canvasses rather than at the canvass
P_ROLL_DEL = 0.40      # a departed elector deleted between canvasses (on notice from another registration officer)


def mstart(i):
    y, m = W.ym(i)
    return D(y, m, 1)


def mend(i):
    y, m = W.ym(i)
    return D(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)


def rand_day(rng, lo, hi):
    return lo + dt.timedelta(days=int(rng.integers(0, (hi - lo).days + 1)))


def notice_of(day):
    """the notice of alteration a determination on day is published in, or None (the canvass's revised register)"""
    if day.month >= 11:
        return NOTICE_DATES.get((day.year + 1, 1))
    if day.month <= 8:
        return NOTICE_DATES.get((day.year, day.month + 1))
    return None


def events(w, seed=W.SEED + 11):
    """every local government elector's addition and deletion determined inside WINDOW, with the attainers' and
    overseas electors' alterations Electra's notices also carry: (dwelling index, action, date, marker, entry key,
    date of attaining 18)"""
    rng = np.random.default_rng(seed)
    lo_i, hi_i = W.mindex(2019, 1), W.mindex(2022, 2)
    out = []
    for k, d in enumerate(w["dwellings"]):
        if d.get("old_ref") is None:
            continue
        marker = "K" if d["eu"] else ""
        for hi, h in enumerate(d["hh"]):
            if h.leave < lo_i or h.arrive > hi_i:
                continue
            arrive = mstart(h.arrive) + dt.timedelta(days=int(rng.integers(0, 28)))
            if hi == 0 and d["site"] is not None:
                arrive = max(arrive, d["inuse_date"])
            leave = mstart(h.leave) + dt.timedelta(days=int(rng.integers(0, 28)))
            for ai, a in enumerate(h.adults):
                if a is None:
                    continue
                lo = max(arrive, D(a - 1, 11, 1))
                hi_d = D(a, 10, 31)
                assert lo <= hi_d, (k, hi, ai)
                if rng.random() < P_ROLL_REG and lo <= D(a, 8, 31):
                    reg = rand_day(rng, lo, min(hi_d, D(a, 8, 31)))
                else:
                    reg = rand_day(rng, max(lo, D(a, 9, 1)), hi_d)
                if reg >= leave:
                    continue                      # left before applying: never registered here
                key = (k, hi, ai)
                if WINDOW[0] <= reg <= WINDOW[1]:
                    out.append((k, "A", reg, marker, key, None))
                yl = leave.year if leave.month <= 10 else leave.year + 1
                dlo, dhi = max(leave, reg + dt.timedelta(days=1)), D(yl, 10, 31)
                if dlo > dhi:
                    dlo = dhi
                cap = D(yl, 8, 31)
                if rng.random() < P_ROLL_DEL and dlo + dt.timedelta(days=20) <= cap:
                    dl = rand_day(rng, dlo + dt.timedelta(days=20), min(cap, dlo + dt.timedelta(days=150)))
                else:
                    dl = rand_day(rng, max(dlo, D(yl, 9, 1)), dhi)
                if WINDOW[0] <= dl <= WINDOW[1]:
                    out.append((k, "D", dl, marker, key, None))
    # attainers registering between canvasses and overseas electors' declarations, a few a month
    months = [(2020, 11), (2020, 12)] + [(2021, m) for m in range(1, 13)] + [(2022, 1), (2022, 2)]
    dw = w["dwellings"]
    for (y, m) in months:
        if m in (9, 10):
            continue
        for k, d in enumerate(dw):
            if d.get("old_ref") is None or d["count"][y] == 0:
                continue
            if rng.random() < 0.0016:
                day = rand_day(rng, D(y, m, 1), mend(W.mindex(y, m)))
                out.append((k, "A", day, "Y", (k, "att", y, m, len(out)), day + dt.timedelta(days=int(rng.integers(40, 360)))))
            if d["site"] is None and rng.random() < 0.00025:
                day = rand_day(rng, D(y, m, 1), mend(W.mindex(y, m)))
                out.append((k, "A", day, "F", (k, "ovs", y, m, len(out)), None))
    out.sort(key=lambda e: (e[2], e[0], str(e[4])))
    return out


def by_dwelling(ev):
    idx = {}
    for e in ev:
        idx.setdefault(e[0], []).append(e)
    return idx


def held_at(w, idx, k, Y, until):
    """local government electors, attainers, overseas electors and local-only electors at dwelling k on the register of
    year Y with every alteration determined after 31 October Y and published by until applied"""
    d = w["dwellings"][k]
    lg, at, ov = d["count"][Y], d["attainers"][Y], d["overseas"].get(Y, 0)
    lo = d["local_only"][Y]
    for (kk, act, day, mk, key, doa) in idx.get(k, []):
        if day <= D(Y, 10, 31):
            continue
        nd = notice_of(day)
        if nd is None or nd > until:
            continue
        s = 1 if act == "A" else -1
        if mk == "Y":
            at += s
        elif mk == "F":
            ov += s
        else:
            lg += s
            if mk == "K":
                lo += s
    return lg, at, ov, lo
