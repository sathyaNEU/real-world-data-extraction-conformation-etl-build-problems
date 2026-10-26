"""The two supplemental asks for task270, each read from files the main call never opens:

Ask B: the smallest effect on each candidate each experiment on the 2027 first-quarter onboarding calendar can detect
with 80 per cent power in a two-sided test at the 5 per cent level, with each candidate's standard deviation among the
2025 holdout's users and each arm's users from the 2027 new-user forecast, the 2027 holdout and the platform's split
of each layer's new users among its live experiments (the calendar, the forecast and the platform guide).

Ask C: how far the 2025 new consumer users outside the global holdout ended up from the holdout's users on each
candidate and on retained_m6, in each half of 2025 (the 2025 sign-up cohort table and the holdout's rows).

Each function takes its handling as arguments, so the ask ladder's stops are the same code with one argument changed."""
import datetime as dt
import math

import numpy as np
import pandas as pd

import common as K
import analysis as A

PP = {"first_purchase_d14", "retained_m6"}      # reported in percentage points


def unit_round(m, v):
    return K.r(100 * v, 2) if m in PP else K.r(v, 3)


# ------------------------------------------------------------------------------------------------------- Ask B
def arm_users(d, weekly="once", holdout=K.HOLDOUT_2027, split="platform", per="arm"):
    """users per arm of each calendar experiment.
    weekly: "once" takes each ISO week's forecast once (the tool writes the week's figure on each of its days); "lines"
    sums the daily lines as they stand.
    split: "platform" splits a layer's users on each platform among the experiments live that week on that platform;
    "layer" among all the layer's live experiments whatever their platform; "none" gives each experiment every user
    of its platforms; "all" splits them among every live experiment on the platform whatever its layer."""
    f = d["forecast"].copy()
    f["date"] = pd.to_datetime(f["date"]).dt.date
    cal = d["calendar"].copy()
    cal["start"] = pd.to_datetime(cal["start_date"]).dt.date
    cal["end"] = pd.to_datetime(cal["end_date"]).dt.date
    if weekly == "once":
        f["monday"] = f["date"].map(lambda x: x - dt.timedelta(days=x.weekday()))
        wk = f.groupby(["monday", "platform"])["new_consumer_users_forecast"].first()
        daily = {(m + dt.timedelta(days=i), p): v / 7.0 for (m, p), v in wk.items() for i in range(7)}
    else:
        daily = {(x, p): float(v) for x, p, v in f[["date", "platform", "new_consumer_users_forecast"]]
                 .itertuples(index=False)}
    users = {e: 0.0 for e in cal["experiment_id"]}
    day = cal["start"].min()
    while day <= cal["end"].max():
        for plat in ("ios", "android"):
            n = daily[(day, plat)] * (1 - holdout)
            for layer, g in cal.groupby("layer"):
                live = g[(g["start"] <= day) & (g["end"] >= day)]
                elig = live[live["platforms"].isin(["all", plat])]
                if not len(elig):
                    continue
                k = {"platform": len(elig), "layer": len(live), "none": 1}.get(split)
                if split == "all":
                    k = int(((cal["start"] <= day) & (cal["end"] >= day) & cal["platforms"].isin(["all", plat])).sum())
                for eid in elig["experiment_id"]:
                    users[eid] += n / k
        day += dt.timedelta(days=1)
    arms = dict(zip(cal["experiment_id"], cal["arms"]))
    return {e: (u / arms[e] if per == "arm" else u) for e, u in users.items()}


def detectable(d, z=K.Z_POWER, sd_from="holdout", **kw):
    h = d["holdout"]
    sd = h[K.CAND].std(ddof=1)
    if sd_from == "population":
        sd = h[K.CAND].std(ddof=0)
    n = arm_users(d, **kw)
    out = {}
    for e, na in n.items():
        out[e] = {m: unit_round(m, z * sd[m] * math.sqrt(2.0 / na)) for m in K.CAND}
    return out, {e: int(round(v)) for e, v in n.items()}


# ------------------------------------------------------------------------------------------------------- Ask C
HALVES = {"H1": (dt.date(2025, 1, 1), dt.date(2025, 6, 30)), "H2": (dt.date(2025, 7, 1), dt.date(2025, 12, 31))}
COHORT_COLS = {"active_days_d1_14": "active_days_total", "sessions_d1_14": "sessions_total",
               "first_purchase_d14": "first_purchases", "items_saved_d1_14": "items_saved_total",
               "push_opens_d1_14": "push_opens_total", "retained_m6": "retained_m6_users"}


def holdout_gap(d, remove_holdout=True, business=False, refresh="latest", type_col="signup_account_type"):
    """each half's mean over consumer sign-ups outside the holdout less the holdout's mean, per metric.
    type_col: "signup_account_type" counts every account that signed up as a consumer (the holdout's population);
    "account_type" the accounts that are consumers at the table's refresh"""
    c = d["cohorts"].copy()
    if not business:
        c = c[c[type_col] == "consumer"]
    keys = ["signup_date", "platform", "country", "account_type", "signup_account_type"]
    if refresh == "latest":
        c = c.sort_values("refreshed_at").drop_duplicates(keys, keep="last")
    elif refresh == "first":
        c = c.sort_values("refreshed_at").drop_duplicates(keys, keep="first")
    c["date"] = pd.to_datetime(c["signup_date"]).dt.date
    h = d["holdout"].copy()
    h["date"] = pd.to_datetime(h["signed_up_on"]).dt.date
    out = {}
    for half, (a, b) in HALVES.items():
        cc = c[(c["date"] >= a) & (c["date"] <= b)]
        hh = h[(h["date"] >= a) & (h["date"] <= b)]
        n_all, n_h = cc["new_users"].sum(), len(hh)
        res = {}
        for m in K.CAND + [K.RET]:
            s_all, s_h = cc[COHORT_COLS[m]].sum(), hh[m].sum()
            outside = (s_all - s_h) / (n_all - n_h) if remove_holdout else s_all / n_all
            res[m] = unit_round(m, outside - s_h / n_h)
        out[half] = res
    return out


def golden(d):
    b, users = detectable(d)
    return dict(B=b, B_users=users, C=holdout_gap(d))


def stops(d):
    return dict(
        B_daily_lines_summed=detectable(d, weekly="lines")[0],
        B_no_2027_holdout=detectable(d, holdout=0.0)[0],
        B_holdout_at_5=detectable(d, holdout=0.05)[0],
        B_layer_split_ignoring_platform=detectable(d, split="layer")[0],
        B_no_split=detectable(d, split="none")[0],
        B_split_across_layers=detectable(d, split="all")[0],
        B_z_rounded=detectable(d, z=2.8)[0],
        B_population_sd=detectable(d, sd_from="population")[0],
        C_type_at_refresh=holdout_gap(d, type_col="account_type"),
        C_holdout_left_in=holdout_gap(d, remove_holdout=False),
        C_business_counted=holdout_gap(d, business=True),
        C_both_refreshes=holdout_gap(d, refresh="both"),
        C_first_refresh=holdout_gap(d, refresh="first"),
    )
