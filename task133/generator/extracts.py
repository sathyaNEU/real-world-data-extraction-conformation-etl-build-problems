"""System extracts: the loan book at the reporting date, the hardship register, the development sample, write-offs."""
import datetime as dt
import math

import numpy as np
import pandas as pd

import sim as S
import world as W

STATES = ["NSW", "VIC", "QLD", "WA", "SA", "ACT", "TAS", "NT"]
STATE_P = [0.34, 0.26, 0.2, 0.09, 0.06, 0.02, 0.02, 0.01]
CHANNELS = ["Broker", "Online", "Direct"]


def annuity(amount, rate, n):
    i = rate / 12.0
    return amount * i / (1 - (1 + i) ** -n)


def sched_balance(amount, rate, term, paid):
    i = rate / 12.0
    p = annuity(amount, rate, term)
    return amount * (1 + i) ** paid - p * ((1 + i) ** paid - 1) / i


def v3_score(rng):
    return int(np.clip(rng.normal(620, 55), 420, 820))


def to_v4(v3):
    a, b = W.SCORE_MAP
    return int(round(a * v3 + b))


def book(rng, lo):
    """every loan in the book system at the reporting date: performing loans plus defaulted loans not yet
    written off (90 or more days past due, written off at 180)"""
    perf = lo[lo["status"] == "performing"].copy()
    recent_def = lo[(lo["status"] == "default") & (lo["mob"] - lo["end_mob"] <= 3)].copy()
    rows = []
    for _, r in pd.concat([perf, recent_def]).sort_values("loan_key").iterrows():
        if r.status == "performing":
            u = rng.random()
            dpd = 0 if u < 0.93 else (int(rng.integers(1, 30)) if u < 0.968 else (int(rng.integers(30, 60)) if u < 0.986 else int(rng.integers(60, 90))))
        else:
            dpd = int(90 + 30 * (r.mob - r.end_mob) + rng.integers(0, 28))
        missed = math.ceil(dpd / 30) if dpd else 0
        paid = max(0, min(r.mob, r.term) - missed)
        bal = round(sched_balance(r.amount, r.rate, r.term, paid) + W.TUNE.get(int(r.loan_key), 0.0), 2)
        if r.drawdown < W.SCORECARD_SWITCH:
            card, s0 = "v3", v3_score(rng)
            s0v4 = to_v4(s0)
        else:
            card = "v4"
            s0 = to_v4(v3_score(rng))
            s0v4 = s0
        drift = rng.normal(4, 22) if rng.random() > 0.085 else rng.normal(-85, 25)
        cur = int(np.clip(round(s0v4 + drift - (40 if dpd >= 30 else 0)), 380, 900))
        rows.append(dict(loan_key=r.loan_key, product=r["product"], risk_grade=r.grade, drawdown_date=r.drawdown,
                         first_repayment_date=r.first_rep, term_months=r.term, contract_rate=r.rate,
                         original_amount=r.amount, current_balance=bal, days_past_due=dpd,
                         origination_score=s0, origination_scorecard=card, current_score_v4=cur,
                         state=STATES[int(rng.choice(8, p=STATE_P))], channel=CHANNELS[int(rng.integers(3))]))
    bk = pd.DataFrame(rows)
    bk.insert(0, "loan_no", ["BPL%07d" % (3100000 + int(k) * 7 + int(k) % 5) for k in bk["loan_key"]])
    return bk


def hardship(rng, bk, lo):
    """hardship arrangements, past and present, for loans still on the book and some since closed"""
    rows = []
    for _, r in bk.iterrows():
        u = rng.random()
        if u < 0.026 and r.days_past_due < 90:
            start = W.REPORT - dt.timedelta(days=int(rng.integers(5, 150)))
            end = start + dt.timedelta(days=int(rng.choice([90, 180])))
            if end < W.REPORT:
                end = W.REPORT + dt.timedelta(days=int(rng.integers(10, 120)))
            rows.append((r.loan_no, start, end, "Active", "Reduced repayments"))
        elif u < 0.06:
            start = r.drawdown_date + dt.timedelta(days=int(rng.integers(60, 600)))
            if start > W.REPORT - dt.timedelta(days=60):
                continue
            end = start + dt.timedelta(days=int(rng.choice([60, 90, 180])))
            if end >= W.REPORT:
                end = W.REPORT - dt.timedelta(days=int(rng.integers(1, 30)))
            st = "Completed" if rng.random() < 0.8 else "Cancelled"
            rows.append((r.loan_no, start, end, st, "Repayment pause" if rng.random() < 0.5 else "Reduced repayments"))
        elif u < 0.068 and r.days_past_due < 30:
            # cancelled before it began: the customer withdrew the request
            start = W.REPORT - dt.timedelta(days=int(rng.integers(10, 60)))
            rows.append((r.loan_no, start, start + dt.timedelta(days=90), "Cancelled", "Repayment pause"))
    hd = pd.DataFrame(rows, columns=["loan_no", "arrangement_start", "arrangement_end", "arrangement_status", "arrangement_type"])
    hd.insert(0, "case_ref", ["HS-%05d" % (20000 + i) for i in range(len(hd))])
    return hd


def development_sample(lo):
    """the PD model's development data: loans drawn October 2019 to September 2023, outcome to June 2026"""
    d = lo[lo["drawdown"] < dt.date(2023, 10, 1)].copy()
    out = pd.DataFrame(dict(loan_key=d["loan_key"], product=d["product"], risk_grade=d["grade"],
                            drawdown_month=[x.strftime("%Y-%m") for x in d["drawdown"]],
                            term_months=d["term"], outcome=d["status"],
                            outcome_month_on_book=d["end_mob"].astype("Int64")))
    return out


def write_offs(rng):
    rows = []
    for m in pd.period_range("2025-07", "2026-09", freq="M"):
        n = int(rng.poisson(118))
        rows.append(dict(month=str(m), loans_written_off=n, gross_write_off_aud=round(n * float(rng.uniform(13500, 16500)), 2),
                         recoveries_aud=round(n * float(rng.uniform(1800, 2600)), 2)))
    return pd.DataFrame(rows)
