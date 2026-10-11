"""The simulated truth: every personal loan originated since October 2019, month by month, to the reporting date."""
import datetime as dt
import math

import numpy as np
import pandas as pd

import world as W


def month_add(d, n):
    y, m = d.year + (d.month - 1 + n) // 12, (d.month - 1 + n) % 12 + 1
    return dt.date(y, m, min(d.day, 28))


def months_due(first_rep, report):
    """number of monthly repayments due on or before the reporting date"""
    if first_rep > report:
        return 0
    n = (report.year - first_rep.year) * 12 + (report.month - first_rep.month)
    if report.day >= first_rep.day:
        n += 1
    return n


def originations(rng):
    rows = []
    m = W.FIRST_ORIG
    k = 0
    lid = 0
    while m <= W.REPORT:
        vol = int(rng.poisson(780 * (1.011 ** k)))
        for _ in range(vol):
            lid += 1
            prod = "PL36" if rng.random() < 0.55 else "PL60"
            grade = W.GRADES[int(rng.choice(5, p=W.GRADE_MIX))]
            lo, hi = W.GRADE_RATE[grade]
            rate = round(float(rng.uniform(lo, hi)), 4)
            amt = float(np.round(rng.lognormal(math.log(16500 if prod == "PL36" else 23500), 0.42), -2))
            amt = min(max(amt, 3000.0), 60000.0)
            draw = dt.date(m.year, m.month, int(rng.integers(1, 29)))
            if draw > W.REPORT:
                continue
            rows.append(dict(loan_key=lid, product=prod, grade=grade, rate=rate, amount=amt, drawdown=draw,
                             first_rep=month_add(draw, 1), term=W.PRODUCTS[prod]))
        m = month_add(dt.date(m.year, m.month, 1), 1)
        k += 1
    return pd.DataFrame(rows)


def outcomes(rng, lo):
    """month-by-month default (90 days past due) and prepayment draws up to the reporting date"""
    status, end_mob = [], []
    for _, r in lo.iterrows():
        due = months_due(r.first_rep, W.REPORT)
        st, em = "performing", None
        for k in range(1, min(due, r.term) + 1):
            u = rng.random()
            h = W.hazard(k, r["product"]) * W.GRADE_MULT[r.grade]
            if u < h:
                st, em = "default", k
                break
            if u < h + W.PREPAY:
                st, em = "prepaid", k
                break
        if st == "performing" and due >= r.term:
            st, em = "matured", r.term
        status.append(st)
        end_mob.append(em)
    lo = lo.copy()
    lo["status"] = status
    lo["end_mob"] = end_mob
    lo["mob"] = [months_due(f, W.REPORT) for f in lo["first_rep"]]
    return lo


def curve(product, maxm=60):
    """the model team's cumulative default curve: a new loan's probability of defaulting by each month on
    book, pooled over grades at the development mix, prepayment not counted as an exit"""
    mix = dict(zip(W.GRADES, W.GRADE_MIX))
    s = {g: 1.0 for g in W.GRADES}
    out = [0.0]
    for k in range(1, maxm + 1):
        for g in W.GRADES:
            s[g] *= 1 - W.hazard(k, product) * W.GRADE_MULT[g]
        out.append(1 - sum(mix[g] * s[g] for g in W.GRADES))
    return [round(x, 6) for x in out]
