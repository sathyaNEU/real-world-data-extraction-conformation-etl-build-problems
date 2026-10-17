"""task157 calc: the fund, its parts, the ladder, the back-tests, the convergent constructions and both asks, computed
from the shipped files alone (target/). build.py, deliver.py and checks.py import it; verify.py recomputes the graded
figures on its own code path.

The fund is the expected total the 2027 guarantee pays: $350 for every driver expected to complete 40 trips between
Monday 4 and Sunday 31 January 2027. Last year's qualifiers are the drivers the 2026 guarantee paid (main run and late
credits) less those whose payout was recovered because the trips were refunded as fraudulent."""
from __future__ import annotations

import csv
import datetime as dt
import math
import os

import numpy as np
import openpyxl

import common as K
import records as R

BANDS = [1, 10, 20, 30, 40, 60]
FUND_STEP = 50000
DRIVER_STEP = 100
FUNDING_DATE = {2025: dt.date(2025, 1, 5), 2026: dt.date(2026, 1, 4), 2027: dt.date(2027, 1, 3)}


class Pack:
    pass


def rd(target, f):
    with open(os.path.join(target, f), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def parse_utc(s):
    return dt.datetime.strptime(s[:19].replace("T", " "), "%Y-%m-%d %H:%M:%S")


def central(s):
    return K.from_utc(parse_utc(s))


def load(target):
    D = Pack()
    D.target = target
    xw = {int(r["legacy_driver_no"]): r["driver_id"] for r in rd(target, R.F_CROSSWALK)}
    acc = rd(target, R.F_ACCOUNTS)
    D.ids = [r["driver_id"] for r in acc]
    D.idx = {d: i for i, d in enumerate(D.ids)}
    D.acc = {r["driver_id"]: r for r in acc}
    D.months = K.months(K.LAUNCH, K.AS_OF)
    D.mi = {m: j for j, m in enumerate(D.months)}
    T = np.zeros((len(D.ids), len(D.months)), dtype=np.int32)
    online = np.zeros((len(D.ids), len(D.months)), dtype=bool)
    for r in rd(target, R.F_LEGACY):
        i = D.idx[xw[int(r["DRIVER_NO"])]]
        j = D.mi[(int(r["MONTH"][:4]), int(r["MONTH"][5:7]))]
        T[i, j] += int(r["COMPLETED_TRIPS"])
        online[i, j] = True
    for r in rd(target, R.F_ACTIVITY):
        i = D.idx[r["driver_id"]]
        j = D.mi[(int(r["activity_month"][:4]), int(r["activity_month"][5:7]))]
        T[i, j] += int(r["trips_completed"])
        online[i, j] = True
    D.T = T
    D.A = T > 0
    D.row = online
    D.first_m = np.where(D.A.any(1), D.A.argmax(1), 10 ** 6)
    # payouts (a file left out of the folder reads as empty: the call reads none of the 2025 run, the events or the
    # returns)
    have = lambda f: os.path.exists(os.path.join(target, f))
    run25 = []
    if have(R.F_RUN25):
        wb = openpyxl.load_workbook(os.path.join(target, R.F_RUN25), read_only=True)
        ws = wb["Payouts"]
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0]:
                run25.append(dict(payout_id=row[0], driver_id=row[1], cents=int(row[3])))
        wb.close()
    run26 = rd(target, R.F_RUN26)
    adj = rd(target, R.F_ADJ)
    D.adj = adj
    D.events = rd(target, R.F_EVENTS) if have(R.F_EVENTS) else []
    D.returns = rd(target, R.F_RETURNS) if have(R.F_RETURNS) else []
    D.run = {2025: {r["payout_id"]: (r["driver_id"], r["cents"] / 100.0) for r in run25},
             2026: {r["payout_id"]: (r["driver_id"], float(r["amount_usd"])) for r in run26}}
    D.payout_year = {}
    D.payout_driver = {}
    D.payout_amount = {}
    for y in (2025, 2026):
        for pid, (d, a) in D.run[y].items():
            D.payout_year[pid], D.payout_driver[pid], D.payout_amount[pid] = y, d, a
    D.late = {2025: [], 2026: []}
    for r in adj:
        if r["adjustment_type"] == "late_credit":
            y = 2025 if r["program_code"] == "WG2025" else 2026
            D.late[y].append(r)
            D.payout_year[r["payout_id"]] = y
            D.payout_driver[r["payout_id"]] = r["driver_id"]
            D.payout_amount[r["payout_id"]] = float(r["amount_usd"])
    D.recoveries = [r for r in adj if float(r["amount_usd"]) < 0]
    # applications and orders
    D.apps = rd(target, R.F_APPS)
    D.orders = rd(target, R.F_ORDERS) if have(R.F_ORDERS) else []
    return D


# ------------------------------------------------------------------------------------------------- populations
def anyin(D, ms):
    cols = [D.mi[m] for m in ms if m in D.mi]
    return D.A[:, cols].any(1)


def wave(D, y, active=(1, 2, 3), blank=(5, 6, 7, 8, 9, 10), back_months=(11, 12), on_rows=False, break_months=None):
    """Last winter's drivers for guarantee year y: a trip in the winter months of y-1 and none through the summer;
    those back in November or December of y-1; the rest back in January of y. With break_months=k, the rival pool:
    every driver with no trip in the k months to October of y-1 and a trip before them."""
    if break_months:
        gap = [K.add_months((y - 1, 10), -j) for j in range(break_months)]
        S = (D.first_m < D.mi[gap[-1]]) & ~anyin(D, gap)
        back = S & anyin(D, [(y - 1, m) for m in back_months])
        jan = S & ~back & D.A[:, D.mi[(y, 1)]]
        return S, back, jan
    act = [(y - 1, m) if m <= 6 else (y - 2, m) for m in active]
    S = anyin(D, act)
    if on_rows:
        S &= ~D.row[:, [D.mi[(y - 1, m)] for m in blank]].any(1)
    else:
        S &= ~anyin(D, [(y - 1, m) for m in blank])
    back = S & anyin(D, [(y - 1, m) for m in back_months])
    jan = S & ~back & D.A[:, D.mi[(y, 1)]]
    return S, back, jan


def roster(D, y):
    return D.A[:, D.mi[(y - 1, 12)]]


def dec_trips(D, y):
    return D.T[:, D.mi[(y - 1, 12)]]


def band(x, bands=BANDS):
    return np.digitize(x, bands + [10 ** 9]) - 1


def qualified(D, y, drop_dups=False, main_only=False, kept=False):
    """Accounts the guarantee paid (main run and late credits), less those whose payout was recovered for refunded
    fraudulent trips. kept=True is the rival basis: only accounts that kept a payment (Ask A's drivers paid, a payout
    returned and never paid out again or recovered for any reason left out)."""
    if getattr(D, "qual_override", None) is not None:
        return D.qual_override[y].copy()
    if kept:
        last = {}
        for e in sorted(D.events, key=lambda e: (e["payout_id"], e["event_at_utc"])):
            last[e["payout_id"]] = e["event"]
        rec = {r["reverses_payout_id"] for r in D.recoveries}
        q = np.zeros(len(D.ids), dtype=bool)
        for pid, yy in D.payout_year.items():
            if yy == y and last.get(pid) != "returned" and pid not in rec:
                q[D.idx[D.payout_driver[pid]]] = True
        return q
    q = np.zeros(len(D.ids), dtype=bool)
    for pid, (d, a) in D.run[y].items():
        q[D.idx[d]] = True
    if not main_only:
        for r in D.late[y]:
            q[D.idx[r["driver_id"]]] = True
        for r in D.recoveries:
            ry = D.payout_year.get(r["reverses_payout_id"])
            if ry is None:
                # the 2025 run left out: a recovery's guarantee is the program of the payout it reverses, which the
                # 2025 run names; read it from the recovery's own run only if that run is the 2025 program's
                ry = 2025 if r["program_code"] == "WG2025" else None
            if ry != y:
                continue
            if r["adjustment_type"] == "fraud_recovery" or (drop_dups and r["adjustment_type"] == "duplicate_account"):
                q[D.idx[r["driver_id"]]] = False
    return q


def first_trip_after(D, when):
    """Accounts whose first trip is after the end of the given day (Central): from the onboarding tool's first trip
    time where it has one, else the extract's first month."""
    out = np.zeros(len(D.ids), dtype=bool)
    end = dt.datetime.combine(when, dt.time(23, 59, 59))
    seen = set()
    for a in D.apps:
        if a["driver_id"] and a["first_trip_at_utc"]:
            seen.add(a["driver_id"])
            if central(a["first_trip_at_utc"]) > end:
                out[D.idx[a["driver_id"]]] = True
    fm = D.first_m
    nxt = D.mi.get(K.add_months(K.ym(when), 1), 10 ** 6)
    for i, d in enumerate(D.ids):
        if d not in seen and fm[i] < 10 ** 6 and fm[i] >= nxt:
            out[i] = True
    return out


def approved_not_started(D, when, lapse=90, include_lapsed=False):
    """Applications approved by the end of the day (Central) whose driver had not taken a first trip by then, the
    approval not yet lapsed (an approval lapses 90 days after it is given)."""
    end = dt.datetime.combine(when, dt.time(23, 59, 59))
    out = set()
    for a in D.apps:
        if a["status"] not in ("approved", "approval_lapsed") or not a["decision_at_utc"]:
            continue
        dec = central(a["decision_at_utc"])
        if dec > end:
            continue
        if not include_lapsed and (when - dec.date()).days > lapse:
            continue
        ft = a["first_trip_at_utc"]
        if ft and central(ft) <= end:
            continue
        out.add(a["driver_id"])
    return out


# ------------------------------------------------------------------------------------------------- the fund
class Fund:
    pass


def band_rates(D, y_ref, exclude_back=True, bands=BANDS, wave_kw=None, kept=False):
    q = qualified(D, y_ref, kept=kept)
    dec = roster(D, y_ref)
    S, back, jan = wave(D, y_ref, **(wave_kw or {}))
    pool = dec & ~back if exclude_back else dec
    b = band(dec_trips(D, y_ref), bands)
    rates = {}
    for k in range(len(bands)):
        m = pool & (b == k)
        rates[k] = (q & m).sum() / max(1, m.sum())
    return rates


def fund(D, g_years=(2024, 2025, 2026), q_years=(2026,), bands=BANDS, exclude_back=True, wave_kw=None,
         other_as_rate=False, new_mode="pool", drop_dups=False, back_in_bands=False, g_mean=False, kept=False):
    """The golden: December's roster less last winter's drivers already back, at last January's rates by December
    trips; last winter's drivers already back at their own January qualification last year; the rest of their wave at
    the ratio of January returns to November and December returns the earlier waves kept, at the wave's own January
    qualification; the other returners and the new drivers at last year's."""
    wk = wave_kw or {}
    F = Fund()
    y = 2027
    S, back, jan = wave(D, y, **wk)
    dec = roster(D, y)
    nonwave = dec & ~back
    rates = band_rates(D, 2026, exclude_back=exclude_back and not back_in_bands, bands=bands, wave_kw=wk, kept=kept)
    b = band(dec_trips(D, y), bands)
    pool = nonwave if not back_in_bands else dec
    F.nonwave = sum(rates[k] * (pool & (b == k)).sum() for k in range(len(bands)))
    waves = {k: wave(D, k, **wk) for k in (2024, 2025, 2026)}
    F.g_by_year = {k: waves[k][2].sum() / waves[k][1].sum() for k in waves}
    F.g = sum(waves[k][2].sum() for k in g_years) / sum(waves[k][1].sum() for k in g_years)
    if g_mean:
        F.g = float(np.mean([F.g_by_year[k] for k in g_years]))
    qs = {k: qualified(D, k, drop_dups=drop_dups, kept=kept) for k in q_years}
    F.qD = sum((qs[k] & waves[k][1]).sum() for k in q_years) / sum(waves[k][1].sum() for k in q_years)
    F.qJ = sum((qs[k] & waves[k][2]).sum() for k in q_years) / sum(waves[k][2].sum() for k in q_years)
    F.n_back = int(back.sum())
    F.n_rest = F.n_back * F.g
    F.back = 0.0 if back_in_bands else F.n_back * F.qD
    F.rest = F.n_rest * F.qJ
    # other returners and new drivers, from last year
    q26 = qualified(D, 2026, drop_dups=drop_dups, kept=kept)
    S26, back26, jan26 = waves[2026]
    new26 = first_trip_after(D, FUNDING_DATE[2026])
    other26 = ~roster(D, 2026) & ~S26 & ~new26 & (D.first_m < D.mi[(2026, 1)])
    if other_as_rate:
        lapsed26 = other26 & anyin(D, [(2025, m) for m in range(1, 12)])
        lapsed27 = ~dec & ~S & anyin(D, [(2026, m) for m in range(1, 12)])
        F.other = lapsed27.sum() * (q26 & lapsed26).sum() / max(1, lapsed26.sum())
    else:
        F.other = float((q26 & other26).sum())
    apn26 = approved_not_started(D, FUNDING_DATE[2026])
    apn27 = approved_not_started(D, FUNDING_DATE[2027])
    F.apn26, F.apn27 = len(apn26), len(apn27)
    F.new26 = int((q26 & new26).sum())
    F.new26_from_pool = int(sum(q26[D.idx[d]] for d in apn26))
    if new_mode == "pool":
        F.new = F.apn27 * F.new26_from_pool / F.apn26
    elif new_mode == "ratio":
        F.new = F.apn27 * F.new26 / F.apn26
    else:
        F.new = float(F.new26)
    F.drivers = F.nonwave + F.back + F.rest + F.other + F.new
    F.total = F.drivers * K.AMOUNT
    F.fund = K.round_to(F.total, FUND_STEP)
    F.drivers_rounded = int(K.round_to(F.drivers, DRIVER_STEP))
    # one sigma of the timing ratio, from the earlier waves' returns (binomial on the January share)
    nb = sum(waves[k][1].sum() for k in g_years)
    nj = sum(waves[k][2].sum() for k in g_years)
    p = nj / (nb + nj)
    sp = math.sqrt(p * (1 - p) / (nb + nj))
    F.g_sigma = sp / (1 - p) ** 2
    return F


# ------------------------------------------------------------------------------------------------- the ladder
def _roster_part(D, y=2027, ref=2026):
    rates = band_rates(D, ref, exclude_back=False)
    b = band(dec_trips(D, y))
    dec = roster(D, y)
    return sum(rates[k] * (dec & (b == k)).sum() for k in range(len(BANDS)))


def _new_part(D):
    F = fund(D)
    return F.new


def ladder(D):
    out = {}
    q26 = qualified(D, 2026)
    cont = _roster_part(D)
    new = _new_part(D)
    dec26, dec27 = roster(D, 2026), roster(D, 2027)
    # R0b: one ratio on December's roster
    out["R0b"] = q26.sum() / dec26.sum() * dec27.sum()
    # R0 default: the twelve-month lapsed pool at last January's return-and-qualify rate
    L26 = ~dec26 & anyin(D, [(2025, m) for m in range(1, 12)])
    L27 = ~dec27 & anyin(D, [(2026, m) for m in range(1, 12)])
    out["R0"] = cont + new + L27.sum() * (q26 & L26).sum() / L26.sum()
    # R1: last winter's drivers away at last year's rate for the same pool, other returners at last year's count
    S26, b26, j26 = wave(D, 2026)
    S27, b27, j27 = wave(D, 2027)
    new26 = first_trip_after(D, FUNDING_DATE[2026])
    other26 = ~dec26 & ~S26 & ~new26 & (D.first_m < D.mi[(2026, 1)])
    oth = float((q26 & other26).sum())
    a26, a27 = S26 & ~b26, S27 & ~b27
    r_s = (q26 & a26).sum() / a26.sum()
    out["R1"] = cont + new + oth + a27.sum() * r_s
    # R2a: the campaign's recruits at the organic first-winter recruits' share
    camp = np.array([D.acc[d]["signup_channel"] == "campaign_winter26" for d in D.ids])
    org = np.array([D.acc[d]["signup_channel"] in ("app", "referral") for d in D.ids])
    first_winter = (D.first_m >= D.mi[(2024, 11)]) & (D.first_m <= D.mi[(2025, 3)])
    r_org = (q26 & a26 & org & first_winter).sum() / (a26 & org & first_winter).sum()
    out["R2a"] = cont + new + oth + (a27 & camp).sum() * r_org + (a27 & ~camp).sum() * r_s
    out["r_org"], out["r_s"] = r_org, r_s
    # R2b: by the last month driven before the summer
    def last_winter_month(y):
        cols = [D.mi[(y - 1, m)] for m in (1, 2, 3, 4)]
        sub = D.A[:, cols]
        return np.where(sub.any(1), 4 - np.argmax(sub[:, ::-1], 1), 0)
    lm26, lm27 = last_winter_month(2026), last_winter_month(2027)
    r2b = cont + new + oth
    for mm in (1, 2, 3, 4):
        d26 = a26 & (lm26 == mm)
        r2b += (a27 & (lm27 == mm)).sum() * (q26 & d26).sum() / max(1, d26.sum())
    out["R2b"] = r2b
    # R2c: a logistic propensity on recency, tenure, lifetime trips and last January's trips, fitted on the twelve-month
    # lapsed pool of the 2026 funding date
    def feats(y):
        dec = D.mi[(y - 1, 12)]
        act = D.A[:, :dec + 1]
        last = np.where(act.any(1), dec - np.argmax(act[:, ::-1], 1), -1)
        rec = np.minimum(dec - last, 24)
        ten = np.log1p(np.maximum(dec - D.first_m, 0))
        life = np.log1p(D.T[:, :dec + 1].sum(1))
        lj = np.log1p(D.T[:, D.mi[(y - 1, 1)]])
        return np.column_stack([np.ones(len(rec)), rec, ten, life, lj])
    X26, X27 = feats(2026)[L26], feats(2027)[L27]
    yv = q26[L26].astype(float)
    beta = np.zeros(X26.shape[1])
    for _ in range(40):
        pr = 1 / (1 + np.exp(-X26 @ beta))
        H = X26.T @ (X26 * (pr * (1 - pr) + 1e-9)[:, None])
        step = np.linalg.solve(H, X26.T @ (yv - pr))
        beta = beta + step
        if np.abs(step).max() < 1e-10:
            break
    out["R2c"] = cont + new + float((1 / (1 + np.exp(-X27 @ beta))).sum())
    out["beta"] = beta
    # R2d: one ratio of January returners to November and December returners over every driver back after a break
    def back_any(y):
        away = ~D.A[:, D.mi[(y - 1, 10)]] & (D.first_m < D.mi[(y - 1, 10)])
        b = away & anyin(D, [(y - 1, 11), (y - 1, 12)])
        j = away & ~b & D.A[:, D.mi[(y, 1)]]
        return b, j
    bb26, jj26 = back_any(2026)
    bb27, jj27 = back_any(2027)
    out["R2d"] = cont + new + bb27.sum() * jj26.sum() / bb26.sum() * (q26 & jj26).sum() / jj26.sum()
    out["back_any"] = {y: tuple(int(v.sum()) for v in back_any(y)) for y in (2025, 2026, 2027)}
    out["back_any_24"] = tuple(int(v.sum()) for v in back_any(2024))
    return out


def backtest(D):
    """At each earlier funding date: January's returners of last winter's wave predicted from the part back by
    December at the ratio of the waves before it, against the pool rate on the drivers still away, and against the
    one ratio over every driver back after a break."""
    out = {}
    w = {k: wave(D, k) for k in (2024, 2025, 2026)}
    for y in (2025, 2026):
        prev = [k for k in (2024, 2025) if k < y]
        g = sum(w[k][2].sum() for k in prev) / sum(w[k][1].sum() for k in prev)
        dev = w[y][1].sum() * g
        a_prev = w[y - 1][0] & ~w[y - 1][1]
        pool = (w[y][0] & ~w[y][1]).sum() * w[y - 1][2].sum() / a_prev.sum()
        def back_any(yy):
            away = ~D.A[:, D.mi[(yy - 1, 10)]] & (D.first_m < D.mi[(yy - 1, 10)])
            b = away & anyin(D, [(yy - 1, 11), (yy - 1, 12)])
            j = away & ~b & D.A[:, D.mi[(yy, 1)]]
            return b, j
        b0, j0 = back_any(y - 1)
        b1, j1 = back_any(y)
        out[y] = dict(actual=int(w[y][2].sum()), development=float(dev), pool=float(pool),
                      all_ratio_pred=float(b1.sum() * j0.sum() / b0.sum()), all_ratio_actual=int(j1.sum()))
    return out


# ------------------------------------------------------------------------------------------------- Ask A
def ask_a(D, net_every_return=False, book_by_run=False, by_account=False, later_subtracted=False):
    """Each guarantee from its main run to its net cost: what later runs added, what the bank returned and was never
    paid out again, what was recovered (each booked to the guarantee of the payout it reverses), and the people it
    paid."""
    ev = {}
    for e in D.events:
        ev.setdefault(e["payout_id"], []).append(e)
    final = {}
    for pid, es in ev.items():
        es.sort(key=lambda e: e["event_at_utc"])
        final[pid] = es[-1]["event"]
    rets = [r for r in D.returns if r["individual_id"] in D.payout_year]
    out = {}
    merged = {d: r["merged_into"] for d, r in D.acc.items() if r["merged_into"]}
    for y in (2025, 2026):
        main = sum(a for pid, (d, a) in D.run[y].items())
        later = sum(float(r["amount_usd"]) for r in D.late[y])
        pids = [p for p, yy in D.payout_year.items() if yy == y]
        if net_every_return:
            never = sum(float(r["amount"]) for r in rets if D.payout_year[r["individual_id"]] == y)
            lost = {r["individual_id"] for r in rets if D.payout_year[r["individual_id"]] == y}
        else:
            lost = {p for p in pids if final.get(p) == "returned"}
            never = sum(D.payout_amount[p] for p in lost)
        if book_by_run:
            rec_lines = [r for r in D.recoveries if r["program_code"] == ("WG2025" if y == 2025 else "WG2026")]
        else:
            rec_lines = [r for r in D.recoveries if D.payout_year.get(r["reverses_payout_id"]) == y]
        recovered = -sum(float(r["amount_usd"]) for r in rec_lines)
        rec_ids = {r["reverses_payout_id"] for r in D.recoveries}
        kept = [p for p in pids if p not in lost and p not in rec_ids]
        if by_account:
            people = {D.payout_driver[p] for p in kept}
        else:
            people = {merged.get(D.payout_driver[p], D.payout_driver[p]) for p in kept}
        net = (main - later if later_subtracted else main + later) - never - recovered
        out[y] = dict(main=main, later=later, never=never, recovered=recovered, net=net, drivers=len(people))
    return out


# ------------------------------------------------------------------------------------------------- Ask B
def ask_b(D, month_from="order", tz="central", persons="candidate", approved=("approved", "approval_lapsed")):
    """For each month from June to October 2026, the people who first applied in it (Central time), how many of them
    were approved on any of their applications, and how many of them had taken a first trip by the extract's run."""
    app = {a["application_id"]: a for a in D.apps}
    order_of = {o["client_reference"]: o for o in D.orders}
    first = {}
    for aid, a in app.items():
        o = order_of.get(aid)
        who = o["candidate_id"] if (persons == "candidate" and o) else aid
        if month_from == "order" and o:
            t = parse_utc(o["ordered_at"])
        else:
            t = parse_utc(a["submitted_at_utc"])
        t = K.from_utc(t) if tz == "central" else t
        first.setdefault(who, []).append((t, aid))
    out = {}
    for m in range(6, 11):
        ppl = [who for who, lst in first.items() if (min(lst)[0].year, min(lst)[0].month) == (2026, m)]
        appr = trip = 0
        for who in ppl:
            aids = [aid for _, aid in first[who]]
            if any(app[a]["status"] in approved for a in aids):
                appr += 1
            ids = [app[a]["driver_id"] for a in aids if app[a]["driver_id"]]
            if any(D.A[D.idx[d]].any() for d in ids if d in D.idx):
                trip += 1
        out[m] = dict(applied=len(ppl), approved=appr, first_trip=trip)
    return out


def all_figures(D):
    F = fund(D)
    return dict(F=F, ladder=ladder(D), backtest=backtest(D), A=ask_a(D), B=ask_b(D))
