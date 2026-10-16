"""The golden's construction for fiscal 2028: each forecast late-shift hour a stationary queue, each month's
compliance the month's calls answered within 15 seconds over its calls presented less those abandoned within 5
seconds, over every late-shift hour of the nights that start in the month (each hour on that month's forecast)."""
from __future__ import annotations

import common as K
import erlang as E


def night_cells(y, m):
    """[(night date, [(dow of the clock hour, hour), ...])] for the month's Friday and Saturday nights; the
    6 November 2027 night lists 01:00 twice (the clock falls back), every other night four hours."""
    out = []
    for nd in K.late_nights(y, m):
        out.append((nd, [(h.weekday(), h.hour) for h in K.night_hours(nd)]))
    return out


def month_compliance(y, m, lam_of, mu, th, c=K.LATE_C_FY2028, model="A", excl=True):
    """lam_of(dow, hour) -> forecast calls per hour for month (y, m). Returns (compliance, presented, answered15,
    abandoned5) with the counts in expected calls."""
    num = den = pres = a5 = 0.0
    for nd, cells in night_cells(y, m):
        for dow, h in cells:
            lam = lam_of(dow, h)
            if model == "A":
                st, ab5 = E.erlang_a(lam, mu, th, c)[:2]
            else:
                st, ab5 = E.erlang_c(lam, mu, c), 0.0
            num += lam * st
            a5 += lam * ab5
            pres += lam
            den += lam * ((1 - ab5) if excl else 1.0)
    return num / den, pres, num, a5
