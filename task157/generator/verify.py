"""task157 independent verifier: reads only the shipped bundle (target/) on its own code path (pandas), recomputes
the fund, the drivers expected to qualify, the components the write-up states, the default path and the nearest
rungs, the back-tests and both asks, and compares them with generator/figures.json and the goldens. No generator
module is imported.

    python3 task157/generator/verify.py <target>"""
from __future__ import annotations

import json
import math
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
FAIL = []


def ok(label, cond, detail=""):
    print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  [%s]" % detail) if detail != "" else ""))
    if not cond:
        FAIL.append(label)


def nearest(x, step):
    return step * math.floor(x / step + 0.5)


def central(ts):
    """UTC timestamps to Central time (US rules: CDT from the second Sunday of March to the first Sunday of
    November, 02:00 local)."""
    t = pd.to_datetime(ts, utc=True)
    return t.dt.tz_convert("America/Chicago").dt.tz_localize(None)


def main(target):
    p = lambda f: os.path.join(target, f)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    # ---------------------------------------------------------------- trips by driver and month
    leg = pd.read_csv(p("dispatch_legacy_driver_months_2021-05_2024-07.csv"))
    xw = pd.read_csv(p("dispatch_migration_driver_crosswalk.csv"))
    leg = leg.merge(xw, left_on="DRIVER_NO", right_on="legacy_driver_no", how="left")
    assert leg["driver_id"].notna().all()
    a = pd.DataFrame({"driver_id": leg["driver_id"], "month": leg["MONTH"], "trips": leg["COMPLETED_TRIPS"]})
    new = pd.read_csv(p("driver_activity_monthly_2024-07_2027-01.csv"))
    b = pd.DataFrame({"driver_id": new["driver_id"], "month": new["activity_month"].str[:7],
                      "trips": new["trips_completed"]})
    act = pd.concat([a, b]).groupby(["driver_id", "month"], as_index=False)["trips"].sum()
    act = act[act["trips"] > 0]
    piv = act.pivot(index="driver_id", columns="month", values="trips").fillna(0)
    months = sorted(piv.columns)
    first = act.groupby("driver_id")["month"].min()

    def has(ms):
        ms = [m for m in ms if m in piv.columns]
        return (piv[ms] > 0).any(axis=1) if ms else pd.Series(False, index=piv.index)

    def wave(y):
        S = has(["%d-%02d" % (y - 1, m) for m in (1, 2, 3)]) & ~has(["%d-%02d" % (y - 1, m) for m in range(5, 11)])
        back = S & has(["%d-11" % (y - 1), "%d-12" % (y - 1)])
        jan = S & ~back & has(["%d-01" % y])
        return S, back, jan

    # ---------------------------------------------------------------- last year's qualifiers
    r25 = pd.read_excel(p("winter_guarantee_2025_payout_run.xlsx"), sheet_name="Payouts")
    r26 = pd.read_csv(p("winter_guarantee_2026_payout_run.csv"))
    adj = pd.read_csv(p("guarantee_payout_adjustments_2025-2026.csv"))
    pay_year = dict(zip(r25["Payout ID"], [2025] * len(r25)))
    pay_year.update(dict(zip(r26["payout_id"], [2026] * len(r26))))
    late = adj[adj["adjustment_type"] == "late_credit"]
    for _, r in late.iterrows():
        pay_year[r["payout_id"]] = 2025 if r["program_code"] == "WG2025" else 2026
    paid = {2025: set(r25["Driver ID"]), 2026: set(r26["driver_id"])}
    for _, r in late.iterrows():
        paid[pay_year[r["payout_id"]]].add(r["driver_id"])
    for _, r in adj[adj["adjustment_type"] == "fraud_recovery"].iterrows():
        paid[pay_year[r["reverses_payout_id"]]].discard(r["driver_id"])
    q = {y: piv.index.isin(sorted(paid[y])) for y in (2025, 2026)}
    q = {y: pd.Series(v, index=piv.index) for y, v in q.items()}

    # ---------------------------------------------------------------- the fund
    S27, back27, jan27 = wave(2027)
    S26, back26, jan26 = wave(2026)
    dec26 = has(["2025-12"])
    dec27 = has(["2026-12"])
    edges = [0, 9, 19, 29, 39, 59, 10 ** 9]
    band26 = pd.cut(piv["2025-12"], edges, labels=False)
    band27 = pd.cut(piv["2026-12"], edges, labels=False)
    pool26 = dec26 & ~back26
    rate = q[2026][pool26].groupby(band26[pool26]).mean()
    nonwave = (dec27 & ~back27).groupby(band27[dec27 & ~back27]).sum()
    roster_part = float(sum(rate[k] * nonwave.get(k, 0) for k in rate.index))
    waves = {y: wave(y) for y in (2024, 2025, 2026)}
    nb = sum(int(waves[y][1].sum()) for y in waves)
    nj = sum(int(waves[y][2].sum()) for y in waves)
    g = nj / nb
    qD = q[2026][back26].mean()
    qJ = q[2026][jan26].mean()
    n_back = int(back27.sum())
    rest = n_back * g
    # other returners and new drivers
    apps = pd.read_csv(p("onboarding_applications_2025-06-02_2027-01-03.csv"))
    apps["dec_c"] = central(apps["decision_at_utc"])
    apps["ft_c"] = central(apps["first_trip_at_utc"])
    end26 = pd.Timestamp("2026-01-04 23:59:59")
    end27 = pd.Timestamp("2027-01-03 23:59:59")
    ft = apps.dropna(subset=["driver_id"]).groupby("driver_id")["ft_c"].min()
    new26 = pd.Series(piv.index.map(lambda d: d in ft.index and pd.notna(ft[d]) and ft[d] > end26), index=piv.index)
    other26 = ~dec26 & ~S26 & ~new26 & (first < "2026-01").reindex(piv.index)
    other = int((q[2026] & other26).sum())

    def apn(end):
        ap = apps[apps["status"].isin(["approved", "approval_lapsed"]) & (apps["dec_c"] <= end)]
        ap = ap[(end.normalize() - ap["dec_c"].dt.normalize()).dt.days <= 90]
        ap = ap[ap["ft_c"].isna() | (ap["ft_c"] > end)]
        return set(ap["driver_id"])
    a26, a27 = apn(end26), apn(end27)
    new_paid = len(a26 & paid[2026])
    new_part = len(a27) * new_paid / len(a26)
    drivers = roster_part + n_back * qD + rest * qJ + other + new_part
    total = drivers * 350
    fund = nearest(total, 50000)
    ok("V1 the fund recomputes on an independent path: %s (expected total $%s)" % (
        "${:,}".format(int(fund)), "{:,.0f}".format(total)), "${:,}".format(int(fund)) == figs["call"]["fund"])
    ok("V2 drivers expected to qualify: %s" % "{:,}".format(int(nearest(drivers, 100))),
       "{:,}".format(int(nearest(drivers, 100))) == figs["call"]["drivers"])
    ok("V3 components: back by 3 January %d (about %s), ratio %.3f (about %.1f), due back %.0f (about %s), last winter's "
       "qualifiers about %s" % (n_back, figs["components"]["back_by_asof"], g, nearest(g, 0.1), rest,
                                 figs["components"]["due_back"], figs["components"]["wave_qualifiers"]),
       "{:,}".format(int(nearest(n_back, 100))) == figs["components"]["back_by_asof"] and
       "%.1f" % nearest(g, 0.1) == figs["components"]["ratio"] and
       "{:,}".format(int(nearest(rest, 100))) == figs["components"]["due_back"] and
       "{:,}".format(int(nearest(n_back * qD + rest * qJ, 100))) == figs["components"]["wave_qualifiers"] and
       "{:,}".format(n_back) == figs["steps"]["back_count"] and "%.3f" % g == figs["steps"]["ratio_exact"])
    ok("V4 the step figures: roster about %s, %d and %d per cent, %d other returners, %d approved without a trip, %d of "
       "%d paid" % (figs["steps"]["roster_part"], round(100 * qD), round(100 * qJ), other, len(a27), new_paid, len(a26)),
       "{:,}".format(int(nearest(roster_part, 100))) == figs["steps"]["roster_part"] and
       str(int(nearest(100 * qD, 1))) == figs["steps"]["qD_pct"] and str(int(nearest(100 * qJ, 1))) ==
       figs["steps"]["qJ_pct"] and str(other) == figs["steps"]["other_returns"] and
       str(len(a27)) == figs["steps"]["approved_not_started"] and str(new_paid) == figs["steps"]["new_paid_2026"] and
       str(len(a26)) == figs["steps"]["approved_not_started_2026"])
    # ---------------------------------------------------------------- the default path and the nearest rungs
    rate_all = q[2026][dec26].groupby(band26[dec26]).mean()
    roster_all = dec27.groupby(band27[dec27]).sum()
    cont = float(sum(rate_all[k] * roster_all.get(k, 0) for k in rate_all.index))
    L26 = ~dec26 & has(["2025-%02d" % m for m in range(1, 12)])
    L27 = ~dec27 & has(["2026-%02d" % m for m in range(1, 12)])
    r0 = cont + new_part + L27.sum() * (q[2026] & L26).sum() / L26.sum()
    ok("V5 the default path files $%s (December's roster and the twelve-month lapsed pool at last January's rates)" %
       "{:,}".format(int(nearest(r0 * 350, 50000))), nearest(r0 * 350, 50000) <= fund - 150000)
    away26 = S26 & ~back26
    away27 = S27 & ~back27
    r1 = cont + new_part + other + away27.sum() * (q[2026] & away26).sum() / away26.sum()
    ok("V6 last winter's drivers away at last year's rate for the same pool files $%s" % "{:,}".format(
        int(nearest(r1 * 350, 50000))), nearest(r1 * 350, 50000) <= fund - 100000)
    hyb = cont + rest * qJ + other + new_part
    ok("V7 the rest of the wave developed but the drivers already back priced by December trips files $%s" %
       "{:,}".format(int(nearest(hyb * 350, 50000))), nearest(hyb * 350, 50000) == fund - 50000)
    # ---------------------------------------------------------------- back-tests
    for y in (2025, 2026):
        prev = [k for k in (2024, 2025) if k < y]
        gp = sum(waves[k][2].sum() for k in prev) / sum(waves[k][1].sum() for k in prev)
        dev = waves[y][1].sum() * gp
        prev_away = waves[y - 1][0] & ~waves[y - 1][1]
        pool = (waves[y][0] & ~waves[y][1]).sum() * waves[y - 1][2].sum() / prev_away.sum()
        act_ = waves[y][2].sum()
        ok("V8 back-test at the %d funding date: the ratio method %.0f, the pool rate %.0f, actual %d" % (
            y, dev, pool, act_), abs(dev / act_ - 1) < 0.03 and abs(pool / act_ - 1) > 0.10)
    # ---------------------------------------------------------------- Ask A
    ev = pd.read_csv(p("guarantee_payout_events_2025-2026.csv")).sort_values(["payout_id", "event_at_utc"])
    last = ev.groupby("payout_id")["event"].last()
    acc = pd.read_csv(p("driver_accounts_2027-01-03.csv"), keep_default_na=False)
    merged = {r["driver_id"]: r["merged_into"] for _, r in acc.iterrows() if r["merged_into"]}
    amount = dict(zip(r25["Payout ID"], r25["Amount (cents)"] / 100.0))
    amount.update(dict(zip(r26["payout_id"], r26["amount_usd"])))
    driver = dict(zip(r25["Payout ID"], r25["Driver ID"]))
    driver.update(dict(zip(r26["payout_id"], r26["driver_id"])))
    for _, r in late.iterrows():
        amount[r["payout_id"]] = r["amount_usd"]
        driver[r["payout_id"]] = r["driver_id"]
    rec = adj[adj["amount_usd"] < 0]
    reversed_ids = set(rec["reverses_payout_id"])
    for y in (2025, 2026):
        pids = [k for k, v in pay_year.items() if v == y]
        lost = [k for k in pids if last[k] == "returned"]
        never = sum(amount[k] for k in lost)
        main_ = sum(amount[k] for k in pids if k not in set(late["payout_id"]))
        later = sum(amount[k] for k in pids if k in set(late["payout_id"]))
        recovered = -rec[rec["reverses_payout_id"].map(pay_year) == y]["amount_usd"].sum()
        net = main_ + later - never - recovered
        people = {merged.get(driver[k], driver[k]) for k in pids if k not in set(lost) and k not in reversed_ids}
        A = figs["answers"]["ask_a"][str(y)]
        ok("V9 Ask A %d: never reached $%s, net $%s, %s drivers paid" % (y, "{:,.0f}".format(never),
                                                                          "{:,.0f}".format(net), len(people)),
           "${:,.0f}".format(never) == A["never_reached"] and "${:,.0f}".format(net) == A["net_cost"] and
           "{:,}".format(len(people)) == A["drivers_paid"] and "${:,.0f}".format(main_) == A["main_run"] and
           "${:,.0f}".format(later) == A["later_runs"] and "${:,.0f}".format(recovered) == A["recovered"])
    # ---------------------------------------------------------------- Ask B
    orders = pd.read_csv(p("background_check_orders_2025-06_2027-01.csv"))
    orders["t"] = central(orders["ordered_at"])
    firstsub = orders.groupby("candidate_id")["t"].min()
    app_of = apps.set_index("application_id")
    orders = orders.join(app_of[["status", "driver_id"]], on="client_reference")
    drove = set(piv.index)
    for m in range(6, 11):
        who = firstsub[(firstsub.dt.year == 2026) & (firstsub.dt.month == m)].index
        sub = orders[orders["candidate_id"].isin(who)]
        appr = sub[sub["status"].isin(["approved", "approval_lapsed"])]["candidate_id"].nunique()
        trip = sub[sub["driver_id"].isin(drove)]["candidate_id"].nunique()
        B = figs["answers"]["ask_b"][["", "", "", "", "", "", "June", "July", "August", "September", "October"][m]]
        ok("V10 Ask B 2026-%02d: %d applied, %d approved, %d first trip" % (m, len(who), appr, trip),
           "{:,}".format(len(who)) == B["applied"] and "{:,}".format(appr) == B["approved"] and
           "{:,}".format(trip) == B["first_trip"])
    # ---------------------------------------------------------------- the goldens carry the same figures
    gold = os.path.join(TASK, "golden")
    if os.path.isdir(gold):
        import openpyxl
        wb = openpyxl.load_workbook(os.path.join(gold, "guarantee_fund_jan2027.xlsx"), data_only=True)
        ws = wb["Fund"]
        ok("V11 the workbook states the fund and the drivers", ws["D5"].value == fund and
           ws["D6"].value == nearest(drivers, 100))
        w3 = wb["Guarantees 2025 and 2026"]
        vals = {(w3.cell(row=r, column=1).value, c): w3.cell(row=r, column=c).value for r in range(5, 11)
                for c in (2, 3)}
        ok("V12 the workbook's guarantee table carries Ask A", all(
            "${:,.0f}".format(abs(vals[(lab, c)])) == figs["answers"]["ask_a"][str(y)][key]
            for c, y in ((2, 2025), (3, 2026)) for lab, key in (
                ("Returned by the bank, never paid out again (never reached a driver)", "never_reached"),
                ("Net cost", "net_cost"))))
    print("\nverify: %d failed" % len(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")))
