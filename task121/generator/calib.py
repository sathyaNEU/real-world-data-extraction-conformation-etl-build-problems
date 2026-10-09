"""Calibration records: the close-outs of two closed partner campaigns and the release log's two
earlier flag-cohort releases. Records first; every booked or measured figure is computed from them."""
import datetime as dt

import numpy as np
import pandas as pd

TYPES = ["signed_in", "returning_guest", "new_visitor"]

CLOSEOUTS = {
    "margens": dict(partner="Festival Margens app", pre_start=dt.date(2025, 3, 31), start=dt.date(2025, 4, 28),
                    weeks=6, partner_weekly=1890, mix=(0.243, 0.036, 0.721),
                    pre_rates=(0.0455, 0.0226, 0.0138), store_weekly=(15200, 2320, 5300)),
    "kaiju": dict(partner="Kaiju Tuga link page", pre_start=dt.date(2025, 10, 6), start=dt.date(2025, 11, 3),
                  weeks=4, partner_weekly=1760, mix=(0.251, 0.035, 0.714),
                  pre_rates=(0.0462, 0.0218, 0.0141), store_weekly=(16100, 2390, 5480)),
}


def closeout_records(rng, key):
    c = CLOSEOUTS[key]
    rows = []
    got = {}
    exp = {}
    for wk in range(4 + c["weeks"]):
        ws = c["pre_start"] + dt.timedelta(days=7 * wk)
        vol = 1 + 0.04 * np.sin(wk * 1.3)
        for j, t in enumerate(TYPES):
            n = int(round(c["store_weekly"][j] * vol + rng.integers(-60, 60)))
            exp[t] = exp.get(t, 0.0) + n * c["pre_rates"][j]
            o = int(round(exp[t])) - got.get(t, 0)
            got[t] = got.get(t, 0) + o
            rows.append((ws.isoformat(), "rest", t, wk >= 4, n, o))
    pre = [r for r in rows if not r[3]]
    rate = {t: sum(r[5] for r in pre if r[2] == t) / sum(r[4] for r in pre if r[2] == t) for t in TYPES}
    e, g = 0.0, 0
    for wk in range(4, 4 + c["weeks"]):
        ws = c["pre_start"] + dt.timedelta(days=7 * wk)
        for j, t in enumerate(TYPES):
            m = int(round(c["partner_weekly"] * c["mix"][j] * (1 + 0.06 * np.cos(wk)) + rng.integers(-12, 12)))
            e += m * rate[t]
            o2 = int(round(e)) - g
            g += o2
            rows.append((ws.isoformat(), "partner", t, True, m, o2))
    df = pd.DataFrame(rows, columns=["week_start", "channel", "visitor_type", "campaign_week", "basket_sessions",
                                     "orders"])
    return df.sort_values(["week_start", "channel", "visitor_type"], kind="mergesort").reset_index(drop=True)


def closeout_bookings(df):
    """Rules swept against the booked line (orders lost to the campaign)."""
    pre = df[~df.campaign_week & (df.channel == "rest")]
    rate_t = (pre.groupby("visitor_type").orders.sum() / pre.groupby("visitor_type").basket_sessions.sum()).to_dict()
    rate_store = pre.orders.sum() / pre.basket_sessions.sum()
    p = df[df.channel == "partner"]
    out = {}
    out["visitor_type"] = float(sum(r.basket_sessions * rate_t[r.visitor_type] for r in p.itertuples()) - p.orders.sum())
    out["store_rate"] = float(p.basket_sessions.sum() * rate_store - p.orders.sum())
    out["all_new"] = float(p.basket_sessions.sum() * rate_t["new_visitor"] - p.orders.sum())
    out["partner_orders"] = int(p.orders.sum())
    out["partner_sessions"] = int(p.basket_sessions.sum())
    out["incremental"] = int(p[p.visitor_type == "new_visitor"].orders.sum())
    ret = p[p.visitor_type != "new_visitor"]
    out["signed_in_share_returning"] = float(100 * p[p.visitor_type == "signed_in"].basket_sessions.sum()
                                             / ret.basket_sessions.sum())
    rr = pre[pre.visitor_type != "new_visitor"]
    out["store_signed_in_share_returning"] = float(100 * pre[pre.visitor_type == "signed_in"].basket_sessions.sum()
                                                   / rr.basket_sessions.sum())
    out["partner_conversion"] = float(100 * p.orders.sum() / p.basket_sessions.sum())
    out["partner_new_share"] = float(100 * p[p.visitor_type == "new_visitor"].basket_sessions.sum()
                                     / p.basket_sessions.sum())
    return out


RELEASES = {
    "R-2026-02": dict(title="Basket page redesign", flag="basket.layout.v3", start=dt.date(2026, 1, 26),
                      waves=(4, 5, 6, 7), effect=0.0021, trend=-0.00045, owner="Duarte Cunha"),
    "R-2026-05": dict(title="Delivery options step: carrier choice and dates", flag="checkout.delivery.options_v2",
                      start=dt.date(2026, 4, 27), waves=(4, 5, 6, 7), effect=-0.0013, trend=0.00038,
                      owner="Raquel Pires"),
}


def release_records(rng, key):
    r = RELEASES[key]
    rows = []
    for wk in range(12):
        ws = r["start"] + dt.timedelta(days=7 * wk)
        for c in range(1, 13):
            wave = r["waves"][(c - 1) // 3]
            exposed = wk >= wave
            n = int(round(1450 + rng.integers(-110, 110)))
            p = 0.0405 + r["trend"] * wk + (r["effect"] if exposed else 0.0)
            o = int(round(n * p + rng.normal(0, 0.6)))
            rows.append((ws.isoformat(), c, bool(exposed), n, o))
    return pd.DataFrame(rows, columns=["week_start", "cohort", "flag_on", "basket_sessions", "orders"])


def release_effects(df):
    """Cohort exposure: exposed against not-yet-exposed cohorts in the same weeks. Calendar: after the
    first exposure against the four weeks before."""
    both = df.groupby("week_start").flag_on.agg(["any", "all"])
    mix = both[both["any"] & ~both["all"]].index
    d = df[df.week_start.isin(mix)]
    diffs = []
    for w, g in d.groupby("week_start"):
        e = g[g.flag_on]
        u = g[~g.flag_on]
        diffs.append(e.orders.sum() / e.basket_sessions.sum() - u.orders.sum() / u.basket_sessions.sum())
    cohort = float(np.mean(diffs))
    weeks = sorted(df.week_start.unique())
    pre = df[df.week_start.isin(weeks[:4])]
    post = df[df.week_start.isin(weeks[4:])]
    cal = float(post.orders.sum() / post.basket_sessions.sum() - pre.orders.sum() / pre.basket_sessions.sum())
    return {"cohort": cohort * 100, "calendar": cal * 100}
