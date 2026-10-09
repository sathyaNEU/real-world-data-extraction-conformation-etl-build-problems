#!/usr/bin/env python3
"""task122 golden: write and execute carousel_slot_q1_2027.ipynb, which renders carousel_slot_q1_2027_cells.png.

    python3 task122/generator/golden.py [--out <dir>]      (default: task122/golden)

The notebook reads only the slot review folder (task122/target). Its code cells are defined once below. The
script runs them in-process first, so the opening sentence carries the computed call, then writes the notebook,
executes it top to bottom with a Jupyter kernel in the output folder (the last cell saves the PNG), checks that the
executed outputs show the same figures, asserts every graded figure against the build record, and prints the
critical components' figures.
"""
import argparse
import contextlib
import io
import os
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

HERE = Path(__file__).resolve().parent
TASK = HERE.parent
NB_NAME = "carousel_slot_q1_2027.ipynb"
PNG_NAME = "carousel_slot_q1_2027_cells.png"

# ------------------------------------------------------------------------------------------------ build record
# The figures the generator asserted at stage 3 (DESIGN_NOTE.md, Build record). Every one is recomputed by the
# notebook from target/ and checked here.
REC_CALL = {"answer": "HC-37", "lift": 5.697, "runner_up": "HC-33", "runner_up_lift": 3.303, "gap": 2.394}
REC_FEE = {   # EUR per 1,000 carousel sessions, cells app 0-29 ... web 730+
    "HC-31": [11.004, 10.810, 9.792, 8.510, 12.709, 8.297, 11.900, -2.215],
    "HC-33": [5.593, 11.605, 4.501, 3.709, 1.902, 6.814, 0.991, 2.410],
    "HC-34": [1.392, 16.500, 17.005, 17.914, 8.989, 15.698, 11.294, 16.691],
    "HC-36": [-8.687, -14.906, -14.388, -17.688, -9.810, -13.100, -15.614, -19.209],
    "HC-37": [8.896, 10.995, 9.798, 6.097, 7.615, 12.085, 9.108, 5.409],
    "HC-39": [5.994, 1.893, 1.813, 1.112, 1.489, -2.799, 0.701, 1.686],
}
REC_TOTALS = {   # extra orders, extra fee income (EUR), over the twelve weeks
    "HC-31": (17107.6, 22592.5), "HC-33": (8910.8, 12709.7), "HC-34": (25326.4, 38272.8),
    "HC-36": (13227.7, -39578.3), "HC-37": (15286.4, 22778.2), "HC-39": (3807.3, 3726.4),
}
REC_RUNGS = ["HC-36", "HC-31", "HC-34", "HC-33", "HC-37"]

# ------------------------------------------------------------------------------------------------ notebook cells
SETUP = r'''
import json
import os
import re
from datetime import date, datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

REVIEW_DIR = Path(os.environ.get("SLOT_REVIEW_DIR", "../target"))   # the slot review folder
pd.set_option("display.width", 220)
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_colwidth", 60)

# Experimentation charter v4 (home surfaces), section numbers in brackets
LIFT_BAR = 2.0            # 4(a): extra orders per 1,000 carousel sessions
GUARDRAIL_PCT = 1.5       # 4(b): carousel order rate in no cell more than 1.5% below the incumbent's
REPRODUCE_TOL = 0.25      # 5.2: an estimator must return each archived test's realised lift within 0.25
SLOT_SHARE = 0.10         # 6: a slot test takes 10% of logged-in carousel sessions on each platform
TENURE_EDGES = [30, 180, 730]
CELLS = ["app 0-29", "app 30-179", "app 180-729", "app 730+",
         "web 0-29", "web 30-179", "web 180-729", "web 730+"]

# Fresh-listing commitment 2026: 12 of every 100 tiles in positions 1 to 6 on listings under 48 hours old,
# counted once per served ranking
FRESH_FLOOR, FRESH_HOURS = 12, 48

# Test capacity note: Q1 2027 slot, 4 January to 28 March, traffic planned on the same ISO weeks one year earlier
SLOT_START, SLOT_WEEKS = date(2027, 1, 4), 12

# Lift is orders placed during the test (charter 2.2), not orders placed before the session ends. Each session
# is scored on every order its buyer places in the 21 days after it starts; the orders extract runs to
# 11 October, 21 days past the last logged session on 20 September.
FOLLOW_UP_DAYS = 21
'''

SESSIONS = r'''
register = json.loads((REVIEW_DIR / "ranking_policy_register.json").read_text(encoding="utf-8"))
INCUMBENT = next(p["policy_id"] for p in register["policies"] if p["status"] == "production")
POLICIES = [p["policy_id"] for p in register["policies"] if p["status"] == "registered"]
NAME = {p["policy_id"]: p["name"] for p in register["policies"]}
LABEL = {r: f"{NAME[r]} ({r})" for r in NAME}

renders = pd.read_csv(REVIEW_DIR / "home_carousel_render_log_2026-06-22_2026-09-20.csv",
                      dtype={"ordered_tiles": str}, keep_default_na=False)
renders["orders_in_session"] = renders.ordered_tiles.str.split().str.len()

g = renders.groupby("session_id", sort=True)
# the session is the draw unit: one ranker, one propensity and one ordered_tiles value per session
assert (g[["ranker", "propensity", "ordered_tiles"]].nunique() == 1).all().all()
sess = pd.DataFrame({"platform": g.platform.first(), "tenure_days": g.buyer_tenure_days.first(),
                     "ranker": g.ranker.first(), "propensity": g.propensity.first(),
                     "renders": g.size(), "y_in": g.orders_in_session.first()}).reset_index()
sess["cell"] = np.where(sess.platform == "app", 0, 4) + np.searchsorted(TENURE_EDGES, sess.tenure_days,
                                                                         side="right")
served = pd.read_parquet(REVIEW_DIR / "home_carousel_served_rankings_2026-06-22_2026-09-20.parquet")
sess = sess.merge(served, on="session_id", how="left", validate="one_to_one")
assert sess.buyer_id.notna().all() and sess.buyer_id.is_unique      # one logged session per buyer

# the render log's ordered tiles tie to the orders extract's carousel orders, session by session
orders = pd.read_parquet(REVIEW_DIR / "orders_enrolled_buyers_2026-06-01_2026-10-11.parquet")
carousel = orders[orders.channel == "carousel"].groupby("home_session_id").size()
assert (sess.session_id.map(carousel).fillna(0).astype(int) == sess.y_in).all()

print(f"{len(renders):,} renders in {len(sess):,} logged sessions ({len(renders) / len(sess):.2f} a session), "
      f"{sess.started_at.min():%d %b} to {sess.started_at.max():%d %b %Y}")
sess.groupby("ranker").agg(sessions=("session_id", "size"), renders=("renders", "sum"),
                           orders_in_session=("y_in", "sum"))
'''

ARCHIVE_MD = r'''
## Which estimator the charter lets us cite

Charter 5.2: an offline estimator counts against condition (a) only if it reproduces every archived test's
realised lift within 0.25. The logger draws one ranker per session and every render repeats that ranking, so the
candidates differ in what they treat as the unit: replaying the render rows unweighted, a propensity weight per
render row, or a propensity weight per session.
'''

ARCHIVE = r'''
def arm_rate(y, p, n, how, n_all):
    """Orders per session for one arm. y orders, p propensity, n renders; n_all sessions in the window."""
    if how == "replay, render rows":
        return (y * n).sum() / n.sum()
    if how == "weight per render":
        return (y * n / p).sum() / (n / p).sum()
    if how == "weight per session":
        return (y / p).sum() / n_all
    raise ValueError(how)

ESTIMATORS = ["replay, render rows", "weight per render", "weight per session"]

book = pd.read_excel(REVIEW_DIR / "carousel_experiment_archive.xlsx", sheet_name=None)
tests, logged = book["tests"], book["logged_sessions"]
rows = []
for t in tests.itertuples():
    d = logged[logged.test_id == t.test_id]
    arm = {a: d[d.arm == a] for a in ("test", "control")}
    row = {"test": t.test_id, "family": t.policy_family, "realised": t.realised_lift}
    for how in ESTIMATORS:
        lv = {a: arm_rate(x.in_session_orders.to_numpy(), x.propensity.to_numpy(), x.renders.to_numpy(), how,
                          len(d)) for a, x in arm.items()}
        row[how] = (lv["test"] - lv["control"]) * 1000
    rows.append(row)
backtest = pd.DataFrame(rows).set_index("test")
hits = {how: int(((backtest[how] - backtest.realised).abs() <= REPRODUCE_TOL).sum()) for how in ESTIMATORS}
assert hits["weight per session"] == len(backtest)
print("archived tests reproduced within 0.25:", ", ".join(f"{h} {k} of {len(backtest)}" for h, k in hits.items()))
backtest.round(2)
'''

INSESSION_MD = r'''
Only the per-session weight reproduces all nine (T7, a sequence model whose logging window had long sessions, is
the test the per-render weight misses by the widest margin). Every lift below is the per-session estimator: each
session counts once, weighted by the inverse of the propensity its ranker was drawn with.

On the render log's own outcome, orders placed before the session ends, the six policies read as follows.
'''

INSESSION = r'''
N = len(sess)
P_ = sess.propensity.to_numpy()

def lifts(y, how="weight per session"):
    """Extra orders per 1,000 carousel sessions against the incumbent, logged window 22 Jun to 20 Sep."""
    lv = {}
    for r in [INCUMBENT] + POLICIES:
        m = (sess.ranker == r).to_numpy()
        lv[r] = arm_rate(y[m], P_[m], sess.renders.to_numpy()[m], how, N)
    return {r: (lv[r] - lv[INCUMBENT]) * 1000 for r in POLICIES}

y_in = sess.y_in.to_numpy().astype(float)
by_estimator = pd.DataFrame({how: lifts(y_in, how) for how in ESTIMATORS})
by_estimator.index = [LABEL[r] for r in by_estimator.index]
by_estimator.round(2)
'''

WINDOW_MD = r'''
## Orders over the test, not orders in the session

The charter's lift (2.2) is the change in orders the arm's buyers place during the test. The render log only sees
orders placed from a tile before the session ends. Following each buyer through the orders extract, every channel,
for 1 to 21 days after the session starts:
'''

WINDOW = r'''
def window_orders(days):
    m = orders.merge(sess[["buyer_id", "session_id", "started_at"]].rename(columns={"session_id": "sid"}),
                     on="buyer_id", how="inner")
    dt = (m.ordered_at - m.started_at).dt.total_seconds()
    return m[(dt >= 0) & (dt <= days * 86400)]

def per_session(m, values=None):
    v = pd.Series(1.0 if values is None else values, index=m.index)
    return sess.session_id.map(v.groupby(m.sid).sum()).fillna(0.0).to_numpy()

sweep = {"in session": lifts(y_in)}
for days in (1, 2, 3, 4, 5, 6, 7, 10, 14, FOLLOW_UP_DAYS):
    sweep[f"{days} d"] = lifts(per_session(window_orders(days)))
sweep = pd.DataFrame(sweep)
# nothing moves after day 6: the 7 to 21 day windows give the same lift for every policy
assert (sweep[["7 d", "10 d", "14 d"]].sub(sweep[f"{FOLLOW_UP_DAYS} d"], axis=0).abs() < 1e-9).all().all()

follow = window_orders(FOLLOW_UP_DAYS)
y_test = per_session(follow)
lift_test = lifts(y_test)
sweep.index = [LABEL[r] for r in sweep.index]
sweep.round(2)
'''

WATCH_MD = r'''
Five policies keep their in-session lift. The velocity boost loses most of its lift in the first six days. It is
the one policy whose inputs include the buyer's listing saves (register), and its pinned tiles 1 and 2 are often
listings already on the buyer's watch list. Cross-check: net each policy's in-session watched-listing orders at the
rate buyers bought watched listings the session did not show within the follow-up window.
'''

WATCH = r'''
wl = []
tile_cols = [f"tile_{i}" for i in range(1, 7)]
for sid, bid, start, watched, *tiles in sess[["session_id", "buyer_id", "started_at", "watchlist_at_start"]
                                             + tile_cols].itertuples(index=False):
    if watched:
        shown = set(tiles)
        wl += [(sid, bid, start, int(x), int(x) in shown) for x in watched.split()]
wl = pd.DataFrame(wl, columns=["session_id", "buyer_id", "started_at", "listing_id", "shown"])
wm = wl.merge(orders[["buyer_id", "listing_id", "ordered_at", "channel", "home_session_id"]],
              on=["buyer_id", "listing_id"], how="left")
in_sess = (wm.channel == "carousel") & (wm.home_session_id == wm.session_id)
later = ~in_sess & (wm.ordered_at - wm.started_at).dt.total_seconds().between(1, FOLLOW_UP_DAYS * 86400)
anyway_rate = later[~wm.shown].mean()
watched_in_session = sess.session_id.map(wm[in_sess].groupby("session_id").size()).fillna(0).to_numpy()
netted = lifts(y_in - anyway_rate * watched_in_session)
assert all(abs(netted[r] - lift_test[r]) < 0.01 for r in POLICIES)

print(f"watched listings not shown in the session, bought by the watcher within {FOLLOW_UP_DAYS} days: "
      f"{anyway_rate:.1%}")
pd.DataFrame({"in session": lifts(y_in), "watched-listing orders in session": lifts(watched_in_session),
              "netted at that rate": netted, f"orders over {FOLLOW_UP_DAYS} days": lift_test},
             index=POLICIES).rename(index=LABEL).round(2)
'''

CONDITIONS_MD = r'''
## Launch conditions and the call

(a) lift at least 2.0 over the test; (b) in each of the charter's eight cells, the carousel order rate no more
than 1.5% below Blend v7's; (c) the fresh-listing commitment, counted once per served ranking. All three are point
rules (charter 4).

The carousel order rate (charter 2.4) counts the orders placed from the carousel tiles an arm served. The render
log's ordered_tiles only has the ones placed in the session. A buyer can leave the home screen open, let the
session close and come back to order from a tile that is still on screen. That order sits in the orders extract
under the new session it was placed in. The listing ties it back to its tile, because a listing shown on a buyer's
carousel is kept off it in their later sessions for seven days.
'''

CONDITIONS = r'''
tiles = sess.melt(id_vars=["session_id", "buyer_id", "ended_at"], value_vars=[f"tile_{i}" for i in range(1, 7)],
                  value_name="listing_id")
from_tiles = orders[orders.channel == "carousel"].merge(tiles, on=["buyer_id", "listing_id"], how="inner")
y_tiles = sess.session_id.map(from_tiles.groupby("session_id").size()).fillna(0).to_numpy()
after_close = from_tiles[from_tiles.ordered_at > from_tiles.ended_at].merge(sess[["session_id", "ranker"]],
                                                                            on="session_id")
hours_after = (after_close.ordered_at - after_close.ended_at).dt.total_seconds() / 3600
assert not after_close.home_session_id.isin(sess.session_id).any()

def carousel_rate_vs_incumbent(y):
    rate = {(r, c): y[((sess.ranker == r) & (sess.cell == c)).to_numpy()].mean() * 1000
            for r in [INCUMBENT] + POLICIES for c in range(8)}
    return pd.DataFrame({CELLS[c]: {r: 100 * (rate[(r, c)] / rate[(INCUMBENT, c)] - 1) for r in POLICIES}
                         for c in range(8)})

guard = carousel_rate_vs_incumbent(y_tiles)
guard_in_session = carousel_rate_vs_incumbent(y_in)

ages = sess[[f"tile_{i}_age_h" for i in range(1, 7)]].to_numpy()
fresh_tiles = (ages < FRESH_HOURS).sum(axis=1)
fresh = {r: 100 * fresh_tiles[(sess.ranker == r).to_numpy()].mean() / 6 for r in POLICIES}

screen = pd.DataFrame({
    "lift in session": lifts(y_in),
    "lift over the test": lift_test,
    "worst cell": guard.idxmin(axis=1),
    "worst cell vs Blend v7, %": guard.min(axis=1),
    "fresh tiles per 100": pd.Series(fresh),
})
screen["(a) lift"] = screen["lift over the test"] >= LIFT_BAR
screen["(b) guardrail"] = screen["worst cell vs Blend v7, %"] >= -GUARDRAIL_PCT
screen["(c) fresh listings"] = screen["fresh tiles per 100"] >= FRESH_FLOOR
screen["clears all three"] = screen[["(a) lift", "(b) guardrail", "(c) fresh listings"]].all(axis=1)

ranked = screen[screen["clears all three"]].sort_values("lift over the test", ascending=False)
CALL, RUNNER_UP = ranked.index[0], ranked.index[1]
call_lift, runner_lift = ranked["lift over the test"].iloc[:2]
gap = call_lift - runner_lift
breaches = [(r, c) for r in POLICIES for c in CELLS if guard.loc[r, c] < -GUARDRAIL_PCT]

print(f"{len(after_close)} orders were placed from a session's tiles after it closed, {hours_after.min() * 60:.0f} "
      f"minutes to {hours_after.max():.1f} hours later; by arm: "
      + ", ".join(f"{r} {n}" for r, n in after_close.ranker.value_counts().reindex([INCUMBENT] + POLICIES,
                                                                                  fill_value=0).items()))
print(f"{LABEL['HC-34']}, app 0-29: {guard_in_session.loc['HC-34', 'app 0-29']:.1f}% against Blend v7 on orders "
      f"placed in the session, {guard.loc['HC-34', 'app 0-29']:.1f}% on every order placed from its tiles.")
print(f"Call: {LABEL[CALL]}, {call_lift:.1f} extra orders per 1,000 carousel sessions.")
print(f"Closest policy clearing all three conditions: {LABEL[RUNNER_UP]}, {runner_lift:.1f}; gap {gap:.1f}.")
screen.rename(index=LABEL).round(1)
'''

FEE_MD = r'''
## Buyer-protection fee income by cell while the slot runs

Every covered purchase carries the fee: a fixed amount plus 5% of the price paid after any accepted offer
(terms 3). Only an item collected and paid to the seller in person is not covered (terms 2). The payments file is
the provider's card and iDEAL captures, so purchases paid from a Vouwlijn balance are not in it, but they are
covered and charged. Their price paid comes from the accepted-offer export. The register's January 2027 row
(KB-2027-01) was deferred to the Q2 2027 review on 6 October, so the September 2026 tariff stays in force through
the slot. Fee income is booked without the 21% VAT in the fee (Finance, account 8120). Check before using it: the
same rules reproduce Finance's July to September statement to the cent.
'''

FEE = r'''
tariffs = pd.read_csv(REVIEW_DIR / "kopersbescherming_tarieven.csv")
SLOT_TARIFF = "KB-2026-02"          # in force from 1 Sep 2026; KB-2027-01 deferred (pricing committee, 6 Oct)
slot_row = tariffs.set_index("tarief_id").loc[SLOT_TARIFF]
fixed_eur, pct = float(slot_row.vast_bedrag_eur), float(slot_row.percentage_van_artikelprijs) / 100
VAT = 0.21                          # in the fee buyers pay; booked to account 1630, not to fee income

payments = pd.read_parquet(REVIEW_DIR / "payments_buyer_protection_2026-06-01_2026-10-11.parquet")
offers = pd.read_csv(REVIEW_DIR / "offers_accepted_2026-05-25_2026-10-11.csv",
                     parse_dates=["offered_at", "accepted_at", "expires_at"])
in_force = tariffs[["ingangsdatum", "vast_bedrag_eur", "percentage_van_artikelprijs"]].copy()
in_force["start"] = pd.to_datetime(in_force.ingangsdatum).astype(payments.captured_at.dtype)
in_force = in_force.sort_values("start")

# control: each register row, from its start date, reproduces every fee the provider captured
chk = pd.merge_asof(payments.sort_values("captured_at"), in_force, left_on="captured_at", right_on="start")
chk_price = (chk.amount_eur - chk.shipping_eur - chk.buyer_protection_fee_eur).round(2)
assert np.allclose(chk.vast_bedrag_eur + chk.percentage_van_artikelprijs / 100 * chk_price,
                   chk.buyer_protection_fee_eur, atol=0.005)

def priced(o):
    """Price paid and cover for orders joined to their capture (if any)."""
    captured = o.payment_id.notna().to_numpy()
    x = o.merge(offers, on=["buyer_id", "listing_id"], how="left", validate="many_to_one")
    live = ((x.accepted_at <= x.ordered_at) & (x.expires_at >= x.ordered_at)).to_numpy()
    from_offers = np.where(live, x.offer_eur, x.asking_price_eur)
    from_capture = (o.amount_eur - o.shipping_eur - o.buyer_protection_fee_eur).round(2).to_numpy()
    assert np.allclose(from_offers[captured], from_capture[captured], atol=0.004)   # the two routes agree
    price = np.where(captured, from_capture, from_offers)
    covered = captured | (o.delivery != "pickup").to_numpy()
    return price, covered, captured

# control: Finance's fee income for July to September, by month and platform, to the cent
allo = orders.merge(payments, on="order_id", how="left", validate="one_to_one")
price_all, covered_all, captured_all = priced(allo)
fin = allo.assign(price=price_all, booked=np.where(captured_all, allo.captured_at, allo.ordered_at))[covered_all]
fin["booked"] = fin.booked.astype(in_force.start.dtype)
fin = pd.merge_asof(fin.sort_values("booked"), in_force, left_on="booked", right_on="start")
fin["fee_cents"] = (fin.vast_bedrag_eur * 100).round() + fin.percentage_van_artikelprijs * fin.price
fin["month"] = fin.booked.dt.strftime("%B %Y")
q3 = fin[fin.booked.dt.strftime("%Y-%m").isin(["2026-07", "2026-08", "2026-09"])]
ours = q3.groupby(["month", "platform"]).agg(orders=("order_id", "size"), fee_cents=("fee_cents", "sum"))
ours["fee income excl. VAT"] = (ours.fee_cents / 100 / (1 + VAT)).round(2)
stmt = pd.read_excel(REVIEW_DIR / "finance_buyer_protection_fee_income_2026Q3.xlsx", header=5).iloc[:6]
stmt = stmt.set_index(["Month", "Platform"])
assert (ours.loc[stmt.index, "orders"].to_numpy() == stmt["Protected orders"].to_numpy()).all()
assert np.allclose(ours.loc[stmt.index, "fee income excl. VAT"], stmt["Fee income excl. VAT (EUR)"], atol=0.005)
print(f"Finance's July to September fee income reproduced to the cent: EUR "
      f"{stmt['Fee income excl. VAT (EUR)'].sum():,.2f} on {int(stmt['Protected orders'].sum()):,} covered "
      f"purchases, {(~captured_all[covered_all]).mean():.1%} of them paid from a Vouwlijn balance.")

# the slot: every covered order in each session's 21 days, at the slot tariff, excl. VAT
o = follow.merge(payments, on="order_id", how="left", validate="one_to_one")
price, covered, _ = priced(o)
fee_session = per_session(o, np.where(covered, fixed_eur + pct * price, 0.0) / (1 + VAT))

def by_cell(v):
    out = {}
    for c in range(8):
        cm = (sess.cell == c).to_numpy()
        base = v[cm & (sess.ranker == INCUMBENT).to_numpy()].mean()
        out[CELLS[c]] = {r: (v[cm & (sess.ranker == r).to_numpy()].mean() - base) * 1000 for r in POLICIES}
    return pd.DataFrame(out)

fee_grid = by_cell(fee_session)        # EUR per 1,000 carousel sessions, policy x cell
orders_grid = by_cell(y_test)          # extra orders per 1,000 carousel sessions, policy x cell
fee_grid_view = fee_grid.rename(index=LABEL).round(1)
print(f"Tariff {SLOT_TARIFF}: EUR {fixed_eur:.2f} + {pct:.0%} of price paid, excl. {VAT:.0%} VAT. "
      "Change in fee income per 1,000 carousel sessions, EUR, against Blend v7:")
fee_grid_view
'''

TOTALS_MD = r'''
## What the twelve weeks buy

Traffic is planned cell by cell on the same ISO weeks one year earlier (capacity note). Restatement R2 replaces
the first release of the weekly table for 2026-W01 to W26 (release log, 14 August). The web arm starts on
4 January; the app arm starts with the first app release on or after that date, because assignment ships in the
app build.
'''

TOTALS = r'''
ics = (REVIEW_DIR / "app_release_calendar_2026-2027.ics").read_text(encoding="utf-8")
releases = sorted(datetime.strptime(re.search(r"DTSTART;VALUE=DATE:(\d{8})", ev).group(1), "%Y%m%d").date()
                  for ev in ics.split("BEGIN:VEVENT")[1:] if "SUMMARY:App release" in ev)
app_start = min(d for d in releases if d >= SLOT_START)

first = pd.read_csv(REVIEW_DIR / "home_carousel_sessions_weekly_2025W01_2026W39.csv")
r2 = pd.read_csv(REVIEW_DIR / "home_carousel_sessions_weekly_R2_2026W01_2026W26.csv")
key = ["iso_week", "platform", "tenure_band"]
weekly = pd.concat([first[~first.set_index(key).index.isin(r2.set_index(key).index)], r2])
assert len(weekly) == len(first)

slot_weeks = [SLOT_START + timedelta(weeks=i) for i in range(SLOT_WEEKS)]
plan = []
for c, cell in enumerate(CELLS):
    platform, band = cell.split()
    weeks = [w for w in slot_weeks if platform == "web" or w + timedelta(days=6) >= app_start]
    labels = [f"{w.year - 1}-W{w.isocalendar()[1]:02d}" for w in weeks]
    m = weekly.iso_week.isin(labels) & (weekly.platform == platform) & (weekly.tenure_band == band)
    plan.append({"cell": cell, "weeks": f"{labels[0][-3:]} to {labels[-1][-3:]}",
                 "sessions, same weeks 2026": int(weekly.loc[m, "logged_in_sessions"].sum())})
plan = pd.DataFrame(plan).set_index("cell")
arm = SLOT_SHARE * plan["sessions, same weeks 2026"].to_numpy()
plan["arm sessions"] = np.floor(arm + 0.5).astype(int)

def nearest_hundred(v):
    return int(np.floor(v / 100 + 0.5) * 100)

totals = pd.DataFrame({
    "extra orders": orders_grid.to_numpy() @ arm / 1000,
    "extra fee income, EUR": fee_grid.to_numpy() @ arm / 1000,
}, index=POLICIES)
totals_view = pd.DataFrame({
    "extra orders": [f"{nearest_hundred(v):,}" for v in totals["extra orders"]],
    "extra fee income, EUR": [f"{nearest_hundred(v):,}" for v in totals["extra fee income, EUR"]],
}, index=[LABEL[r] for r in POLICIES])
print(f"App arm from {app_start:%d %B %Y} ({sum(1 for w in slot_weeks if w + timedelta(days=6) >= app_start)} of "
      f"{SLOT_WEEKS} weeks); {arm.sum():,.0f} arm sessions in all.")
display(plan)
totals_view
'''

CHART_MD = r'''
## For the deck

The grid above as a heatmap, saved as carousel_slot_q1_2027_cells.png beside this notebook. Hatched cells are the
two guardrail breaches from the screen; the outlined row is the policy taking the slot.
'''

CHART = r'''
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm, to_rgb
from matplotlib import font_manager
from matplotlib.patches import Patch, Rectangle

FONT = "Inter" if any(f.name == "Inter" for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
plt.rcParams.update({"font.family": FONT, "hatch.linewidth": 1.1, "hatch.color": "#3a3936"})
INK, INK_2, SURFACE = "#0b0b0b", "#52514e", "#fcfcfb"
fee_cmap = LinearSegmentedColormap.from_list(
    "fee", [(0.0, "#8f2524"), (0.25, "#e34948"), (0.43, "#f6c7c3"), (0.5, "#f0efec"),
            (0.57, "#cde2fb"), (0.78, "#5598e7"), (1.0, "#184f95")])
norm = TwoSlopeNorm(vmin=-20, vcenter=0, vmax=20)

status = {}
for r in POLICIES:
    s = screen.loc[r]
    status[r] = ("Chosen for the slot" if r == CALL else
                 "Clears all three conditions" if s["clears all three"] else
                 f"Breaks the guardrail, {s['worst cell']}" if not s["(b) guardrail"] else
                 "Below the fresh-listing floor" if not s["(c) fresh listings"] else
                 f"Lift under {LIFT_BAR:.1f}")

fig = plt.figure(figsize=(13.33, 7.5), dpi=150, facecolor=SURFACE)
ax = fig.add_axes([0.255, 0.20, 0.535, 0.56], facecolor=SURFACE)
vals = fee_grid.loc[POLICIES].to_numpy()
ax.pcolormesh(vals, cmap=fee_cmap, norm=norm, edgecolors=SURFACE, linewidth=3)
ax.set_xlim(0, 8)
ax.set_ylim(len(POLICIES), 0)
ax.axvline(4, color=SURFACE, linewidth=9, zorder=2)
hatched = {(POLICIES.index(r), CELLS.index(cell)) for r, cell in breaches}
for i, c in hatched:
    ax.add_patch(Rectangle((c + 0.04, i + 0.04), 0.92, 0.92, fill=False, hatch="///", linewidth=0, zorder=3))
for i, r in enumerate(POLICIES):
    for c in range(8):
        fc = fee_cmap(norm(vals[i, c]))
        rgb = to_rgb(fc)
        light = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2] > 0.45
        ax.text(c + 0.5, i + 0.5, f"{vals[i, c]:.1f}", ha="center", va="center", fontsize=12, zorder=4,
                color=INK if light else "white", fontweight="bold" if r == CALL else "normal",
                bbox=dict(boxstyle="round,pad=0.3", fc=fc, ec="none") if (i, c) in hatched else None)
i_call = POLICIES.index(CALL)
ax.add_patch(Rectangle((0.02, i_call + 0.02), 7.96, 0.96, fill=False, edgecolor=INK, linewidth=2.6, zorder=5))

ax.set_xticks([c + 0.5 for c in range(8)])
ax.set_xticklabels([c.split()[1] for c in CELLS], fontsize=10.5, color=INK_2)
ax.xaxis.tick_top()
ax.set_yticks([i + 0.5 for i in range(len(POLICIES))])
ax.set_yticklabels([LABEL[r].replace(" with ", " with\n") if len(LABEL[r]) > 34 else LABEL[r]
                    for r in POLICIES], fontsize=11.5, color=INK)
for t, r in zip(ax.get_yticklabels(), POLICIES):
    t.set_fontweight("bold" if r == CALL else "normal")
ax.tick_params(length=0, pad=6)
for side in ax.spines.values():
    side.set_visible(False)
for x0, name in ((0, "App, buyer tenure in days"), (4, "Web, buyer tenure in days")):
    ax.text(x0 + 2, -0.62, name, ha="center", va="bottom", fontsize=11.5, color=INK, fontweight="semibold")
    ax.plot([x0 + 0.08, x0 + 3.92], [-0.55, -0.55], color=INK_2, linewidth=0.8, clip_on=False)
for i, r in enumerate(POLICIES):
    ax.text(8.2, i + 0.5, status[r], ha="left", va="center", fontsize=10.5,
            color=INK if r == CALL else INK_2, fontweight="semibold" if r == CALL else "normal")

fig.text(0.035, 0.935, f"Q1 2027 carousel slot: {LABEL[CALL]}, +{call_lift:.1f} orders per 1,000 carousel "
         "sessions", fontsize=15, fontweight="bold", color=INK)
fig.text(0.035, 0.895, "Change in buyer-protection fee income per 1,000 carousel sessions while the slot runs, "
         "EUR, against Blend v7, by platform and buyer tenure", fontsize=11.5, color=INK_2)

cax = fig.add_axes([0.255, 0.115, 0.30, 0.025])
cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=fee_cmap), cax=cax, orientation="horizontal",
                  ticks=[-20, -10, 0, 10, 20])
cb.ax.set_xticklabels(["-20", "-10", "0", "+10", "+20"], fontsize=9.5, color=INK_2)
cb.outline.set_visible(False)
cb.ax.tick_params(length=0)
cb.set_label("EUR per 1,000 carousel sessions", fontsize=9.5, color=INK_2, labelpad=4)
fig.legend(handles=[Patch(facecolor="#f0efec", hatch="///", edgecolor="#3a3936", linewidth=0,
                          label=f"Carousel order rate more than {GUARDRAIL_PCT}% below Blend v7 (charter 4b)"),
                    Patch(facecolor="none", edgecolor=INK, linewidth=2.2, label="Policy taking the slot")],
           loc="lower left", bbox_to_anchor=(0.585, 0.075), frameon=False, fontsize=9.5, labelcolor=INK_2)
fig.text(0.035, 0.02, f"Orders over the {FOLLOW_UP_DAYS} days after each logged session, 22 Jun to 20 Sep 2026; "
         f"fee income excl. VAT at tariff {SLOT_TARIFF} (EUR {fixed_eur:.2f} + {pct:.0%} of price paid), none on "
         "items paid for in person. Guardrail on every order placed from an arm's tiles. Marketplace Science, "
         "October 2026.", fontsize=8.5, color=INK_2)
fig.savefig("carousel_slot_q1_2027_cells.png", dpi=150, facecolor=SURFACE, metadata={"Software": None})
plt.show()
'''


def summary_md(ns):
    lab = ns["LABEL"]
    call, ru = ns["CALL"], ns["RUNNER_UP"]
    return (
        "# Q1 2027 home carousel test slot\n\n"
        f"**The slot from 4 January to 28 March 2027 goes to the {lab[call][0].lower() + lab[call][1:]}, which gives "
        f"us {ns['call_lift']:.1f} extra orders per 1,000 carousel sessions.**\n\n"
        f"The closest policy that still clears our launch conditions is the {lab[ru][0].lower() + lab[ru][1:]} at "
        f"{ns['runner_lift']:.1f}, {ns['gap']:.1f} behind.\n\n"
        "The session-sequence model has the largest lift but fails the guardrail in app 0-29 once every order "
        "placed from its tiles is counted. The render log only sees orders placed in the session, and buyers who "
        "leave the home screen open come back to order from the incumbent's tiles but not from its. The two-tower "
        "personaliser fails it in web 730+, the local pickup boost serves too few fresh listings for our commitment "
        "to sellers, and the seller-diversity re-ranker is under the 2.0 bar. The velocity boost clears all three "
        "on its in-session orders, but most of what it adds there is listings its buyers were already watching and "
        "would have bought within days, so over the test it keeps a little over two fifths of that lift.\n\n"
        "Fee income is net of VAT and includes purchases paid from a Vouwlijn balance; the same rules reproduce "
        "Finance's July to September statement to the cent.\n\n"
        "Saar Dries, Marketplace Science. Prepared for the product leadership team's planning meeting on "
        "28 October 2026 from the slot review folder (extracts pulled 12 October). Set `SLOT_REVIEW_DIR` to rerun "
        "against another copy of the folder; a full run takes about a minute."
    )


CELLS_SRC = [("md", None), ("code", SETUP), ("code", SESSIONS), ("md", ARCHIVE_MD), ("code", ARCHIVE),
             ("md", INSESSION_MD), ("code", INSESSION), ("md", WINDOW_MD), ("code", WINDOW), ("md", WATCH_MD),
             ("code", WATCH), ("md", CONDITIONS_MD), ("code", CONDITIONS), ("md", FEE_MD), ("code", FEE),
             ("md", TOTALS_MD), ("code", TOTALS), ("md", CHART_MD), ("code", CHART)]


def run_in_process(review_dir):
    """Run every analysis cell (not the chart) in one namespace and return it."""
    ns = {"display": lambda *a, **k: None}
    os.environ["SLOT_REVIEW_DIR"] = str(review_dir)
    for kind, src in CELLS_SRC:
        if kind == "code" and src is not CHART:
            with contextlib.redirect_stdout(io.StringIO()):
                exec(compile(src, "<cell>", "exec"), ns)
    return ns


def check_record(ns):
    import numpy as np
    bad = []
    lt = ns["lift_test"]
    if ns["CALL"] != REC_CALL["answer"] or ns["RUNNER_UP"] != REC_CALL["runner_up"]:
        bad.append(("call", ns["CALL"], ns["RUNNER_UP"]))
    for k, x in (("lift", ns["call_lift"]), ("runner_up_lift", ns["runner_lift"]), ("gap", ns["gap"])):
        if abs(x - REC_CALL[k]) > 0.001:
            bad.append((k, x))
    if abs(lt["HC-37"] - REC_CALL["lift"]) > 0.001:
        bad.append(("lift_test", lt["HC-37"]))
    fg = ns["fee_grid"]
    for r, row in REC_FEE.items():
        for c, want in enumerate(row):
            got = fg.loc[r].iloc[c]
            if abs(got - want) > 0.001 or round(got, 1) != round(want, 1):
                bad.append(("fee", r, c, got, want))
    tot = ns["totals"]
    for r, (o_, f_) in REC_TOTALS.items():
        if abs(tot.loc[r, "extra orders"] - o_) > 0.06 or abs(tot.loc[r, "extra fee income, EUR"] - f_) > 0.06:
            bad.append(("total", r, tot.loc[r].tolist(), (o_, f_)))
    if sorted(ns["breaches"]) != [("HC-31", "web 730+"), ("HC-34", "app 0-29")]:
        bad.append(("breaches", ns["breaches"]))
    hits = ns["hits"]
    if (hits["weight per session"], hits["weight per render"], hits["replay, render rows"]) != (9, 6, 3):
        bad.append(("archive", hits))
    q = ns["screen"]
    if list(q.index[q["clears all three"]]) != ["HC-33", "HC-37"]:
        bad.append(("qualifiers", list(q.index[q["clears all three"]])))
    if not np.isfinite(ns["anyway_rate"]):
        bad.append(("anyway", ns["anyway_rate"]))
    return bad


def build_notebook(ns):
    nb = nbformat.v4.new_notebook()
    cells = []
    for i, (kind, src) in enumerate(CELLS_SRC):
        if kind == "md":
            c = nbformat.v4.new_markdown_cell(summary_md(ns) if src is None else src.strip())
        else:
            c = nbformat.v4.new_code_cell(src.strip())
        c["id"] = f"cell-{i:02d}"
        cells.append(c)
    nb["cells"] = cells
    nb["metadata"] = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                      "language_info": {"name": "python"}}
    return nb


def outputs_text(nb):
    txt = []
    for c in nb.cells:
        for o in c.get("outputs", []):
            if o.get("output_type") == "stream":
                txt.append(o["text"])
            elif "data" in o and "text/plain" in o["data"]:
                txt.append(o["data"]["text/plain"])
    return "\n".join(txt)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(TASK / "golden"))
    ap.add_argument("--target", default=str(TASK / "target"))
    a = ap.parse_args()
    out, tgt = Path(a.out).resolve(), Path(a.target).resolve()
    out.mkdir(parents=True, exist_ok=True)

    ns = run_in_process(tgt)
    bad = check_record(ns)
    if bad:
        raise SystemExit(f"golden: figures disagree with the build record: {bad[:6]}")

    nb = build_notebook(ns)
    for stale in (out / NB_NAME, out / PNG_NAME):
        if stale.exists():
            stale.unlink()
    env_dir = os.path.relpath(tgt, out)
    os.environ["SLOT_REVIEW_DIR"] = env_dir if env_dir == "../target" else str(tgt)
    NotebookClient(nb, timeout=900, kernel_name="python3", record_timing=False,
                   resources={"metadata": {"path": str(out)}}).execute()
    for c in nb.cells:
        for o in c.get("outputs", []):
            if o.get("output_type") == "error" or (o.get("output_type") == "stream" and o.get("name") == "stderr"):
                raise SystemExit(f"golden: notebook cell {c['id']} wrote an error or a warning: {o}")
    nbformat.write(nb, out / NB_NAME)

    # the executed notebook shows the same figures as the in-process run
    text = outputs_text(nb)
    ru = ns["LABEL"][ns["RUNNER_UP"]]
    must = [f"Call: {ns['LABEL'][ns['CALL']]}, {ns['call_lift']:.1f} extra orders per 1,000 carousel sessions.",
            f"Closest policy clearing all three conditions: {ru}, {ns['runner_lift']:.1f}; gap {ns['gap']:.1f}.",
            repr(ns["fee_grid_view"]), repr(ns["totals_view"])]
    missing = [m for m in must if m not in text]
    if missing:
        raise SystemExit(f"golden: executed notebook does not show {missing}")
    if not (out / PNG_NAME).exists():
        raise SystemExit("golden: the notebook did not write the PNG")
    stray = sorted(p.name for p in out.iterdir() if p.name not in (NB_NAME, PNG_NAME))
    if stray:
        raise SystemExit(f"golden: unexpected files in {out}: {stray}")

    # ------------------------------------------------------------------ the critical components' figures
    L = ns["LABEL"]
    lin, lt, q = ns["lifts"](ns["y_in"]), ns["lift_test"], ns["screen"]
    print("golden: wrote", NB_NAME, "and", PNG_NAME, "to", out)
    print(f"archive back-test (within 0.25 of realised): " + ", ".join(f"{k} {v} of 9" for k, v in ns["hits"].items()))
    for r, c in ns["breaches"]:
        print(f"guardrail breach: {L[r]} {c} {ns['guard'].loc[r, c]:.1f}%")
    print(f"fresh tiles per 100, per served ranking: {L['HC-36']} {q.loc['HC-36', 'fresh tiles per 100']:.1f}")
    print(f"lift over the test under the bar: {L['HC-39']} {lt['HC-39']:.1f}")
    print(f"velocity boost: in session {lin['HC-33']:.1f}, over the test {lt['HC-33']:.1f}")
    print(f"CALL {L[ns['CALL']]} {ns['call_lift']:.1f} (unrounded {ns['call_lift']:.4f}); runner-up "
          f"{L[ns['RUNNER_UP']]} {ns['runner_lift']:.1f} ({ns['runner_lift']:.4f}); gap {ns['gap']:.1f} "
          f"({ns['gap']:.4f})")
    print("fee grid (EUR per 1,000 carousel sessions):")
    print(ns["fee_grid_view"].to_string())
    print("twelve-week totals:")
    print(ns["totals_view"].to_string())
    print("golden: every figure agrees with the build record")


if __name__ == "__main__":
    sys.exit(main())
