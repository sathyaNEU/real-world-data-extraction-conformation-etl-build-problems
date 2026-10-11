"""Independent check of every graded figure, from the shipped bytes only, on its own code path
(pandas month arithmetic instead of the estimators' date loops, scipy's Poisson instead of a log sum)."""
import os
import sys

import numpy as np
import openpyxl
import pandas as pd
from scipy.stats import poisson

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(TASK, "target")
G = os.path.join(TASK, "golden")
EDGES = [0, 10, 15, 20, 25, 30, 999]


def mk(y, m):
    return y * 12 + (m - 1)


def main():
    reg = pd.read_csv(os.path.join(T, "protection_asset_register_2026-09-30.csv"), parse_dates=["install_date", "retired_date"])
    wo = pd.read_csv(os.path.join(T, "eam_work_orders_protection_2021-01_2026-09.csv"), parse_dates=["reported_date"])
    subs = pd.read_csv(os.path.join(T, "substations.csv"))
    st = pd.read_csv(os.path.join(T, "spares_stock_2026-09-30.csv"))
    fl = reg[reg.model == "VPR-340"].copy()
    # first month in service on its first day
    fl["m0"] = [mk(d.year, d.month) + (1 if d.day > 1 else 0) for d in fl.install_date]
    fl["mend"] = [mk(d.year, d.month) if pd.notna(d) else mk(2026, 10) for d in fl.retired_date]
    MIG, END = mk(2021, 1), mk(2026, 10)

    def ages(inst, m):
        y, mo = m // 12, m % 12 + 1
        return y - inst.year - ((mo < inst.month) | ((mo == inst.month) & (1 < inst.day)))

    rows = []
    for _, r in fl.iterrows():
        ms = np.arange(max(r.m0, MIG), r.mend)
        if len(ms):
            a = np.array([ages(r.install_date, m) for m in ms])
            rows.append(np.bincount(np.digitize(a, EDGES) - 1, minlength=6))
    expo = np.sum(rows, axis=0) / 12.0
    f = wo[wo.asset_id.isin(fl.asset_id) & wo.work_type.isin(["CM", "EM"]) & (wo.failed_component == "PSU")
           & wo.status.isin(["COMP", "CLOSE"])]
    inst = dict(zip(fl.asset_id, fl.install_date))
    fa = [ages(inst[a], mk(d.year, d.month)) for a, d in zip(f.asset_id, f.reported_date)]
    cnt = np.bincount(np.digitize(fa, EDGES) - 1, minlength=6)
    rate = cnt / expo
    wb = openpyxl.load_workbook(os.path.join(T, "protection_renewal_programme_2026.xlsx"), data_only=True)
    plan = {}
    for row in wb["Approved 2026"].iter_rows(min_row=4, values_only=True):
        if row and row[1]:
            v = row[5]
            plan[row[1]] = mk(2036, 1) if v == "Not in programme period" else mk(pd.to_datetime(v).year, pd.to_datetime(v).month)
    live = fl[fl.status == "IN SERVICE"]
    region = dict(zip(subs.sub_code, subs.region))
    lam, by_year, by_reg = 0.0, {}, {}
    for _, r in live.iterrows():
        for m in range(mk(2026, 10), plan[r.sub_code]):
            b = int(np.digitize([ages(r.install_date, m)], EDGES)[0] - 1)
            e = rate[b] / 12.0
            lam += e
            by_year[m // 12] = by_year.get(m // 12, 0) + e
            by_reg[region[r.sub_code]] = by_reg.get(region[r.sub_code], 0) + e
    psu = st[st.item_code == "VPR340-PSU-02"]
    avail = int(psu[psu.stock_state.isin(["SERVICEABLE", "AT REPAIR"])].quantity.sum())
    lots = next(n for n in range(0, 100) if poisson.cdf(avail + 25 * n, lam) >= 0.95)
    inserv = {y: int(sum(plan[s] > mk(y, 1) for s in live.sub_code)) for y in range(2027, 2036)}
    fails = []

    def chk(name, got, exp, tol=0.05):
        ok = abs(float(got) - float(exp)) <= tol
        print(("OK  " if ok else "FAIL"), name, got, exp)
        if not ok:
            fails.append(name)

    g = openpyxl.load_workbook(os.path.join(G, "vpr340_psu_final_buy.xlsx"), data_only=True)
    b = g["Buy"]
    chk("lots", b["B4"].value, lots, 0)
    chk("modules", b["B5"].value, lots * 25, 0)
    chk("cost", b["B6"].value, lots * 25 * 1965, 0.5)
    chk("expected failures", b["B7"].value, round(lam, 1))
    chk("available", b["B8"].value, avail, 0)
    chk("cover", b["B9"].value, round(100 * poisson.cdf(avail + 25 * lots, lam), 1))
    for row in g["Lot settings"].iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        chk("cover at %d lots" % row[0], row[3], round(100 * poisson.cdf(avail + 25 * row[0], lam), 1))
        chk("cost at %d lots" % row[0], row[4], row[0] * 25 * 1965, 0.5)
    for row in g["Outlook by year"].iter_rows(min_row=2, values_only=True):
        if row[0] in (None, "Total"):
            continue
        y = 2026 if str(row[0]).startswith("2026") else int(row[0])
        chk("failures %s" % y, row[1], round(by_year[y], 1))
        if y in inserv:
            chk("supported 1 Jan %d" % y, row[2], inserv[y], 0)
    for row in g["By region"].iter_rows(min_row=2, values_only=True):
        if row[0]:
            chk("region %s" % row[0], row[1], round(by_reg[row[0]], 1))
    print("VERIFY", "FAIL" if fails else "PASS", len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
