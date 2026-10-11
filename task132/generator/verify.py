"""Independent check of every graded figure, from the shipped bytes only, on its own code path: integer month
indices instead of the estimators' date loops, the failed module found by the module in service on the first of
the reported month (not by the removal work order), the replacement recursion in numpy, scipy's Poisson."""
import os
import re
import sys

import numpy as np
import openpyxl
import pandas as pd
from scipy.stats import poisson

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
G = sys.argv[2] if len(sys.argv) > 2 else os.path.join(TASK, "golden")
EDGES = [0, 10, 15, 20, 25, 999]
MIG, H0 = 2021 * 12, 2026 * 12 + 9


def mk(d):
    return d.year * 12 + d.month - 1


def first(d):
    return mk(d) + (1 if d.day > 1 else 0)


def age(fit, m):
    y, mo = m // 12, m % 12 + 1
    return y - fit.year - (1 if (mo < fit.month or (mo == fit.month and fit.day > 1)) else 0)


def band(a):
    return int(np.digitize([a], EDGES)[0] - 1)


def main():
    reg = pd.read_csv(os.path.join(T, "protection_asset_register_2026-09-30.csv"), parse_dates=["install_date", "retired_date"])
    wo = pd.read_csv(os.path.join(T, "eam_work_orders_protection_2021-01_2026-09.csv"), parse_dates=["reported_date"])
    hi = pd.read_csv(os.path.join(T, "psu_rotating_item_history_2021-01_2026-09.csv"), parse_dates=["fitted_date", "removed_date"])
    subs = pd.read_csv(os.path.join(T, "substations.csv"))
    st = pd.read_csv(os.path.join(T, "spares_stock_2026-09-30.csv"))
    fl = reg[reg.model == "VPR-340"]
    hi["m0"] = [first(d) for d in hi.fitted_date]
    hi["m1"] = [first(d) if pd.notna(d) else H0 for d in hi.removed_date]
    # failures: the module in service on the first of the reported month
    f = wo[wo.asset_id.isin(fl.asset_id) & wo.work_type.isin(["CM", "EM"]) & (wo.failed_component == "PSU")
           & wo.status.isin(["COMP", "CLOSE"])]
    cnt = np.zeros(5)
    for a, d in zip(f.asset_id, f.reported_date):
        m = mk(d)
        h = hi[(hi.asset_id == a) & (hi.m0 <= m) & (hi.m1 > m)]
        assert len(h) == 1, (a, d)
        cnt[band(age(h.fitted_date.iloc[0], m))] += 1
    expo = np.zeros(5)
    for fit, m0, m1 in zip(hi.fitted_date, hi.m0, hi.m1):
        for m in range(max(m0, MIG), min(m1, H0)):
            expo[band(age(fit, m))] += 1
    rate = cnt / expo * 12.0
    # support end by bay from the approved programme
    wb = openpyxl.load_workbook(os.path.join(T, "protection_renewal_program_2026.xlsx"), data_only=True)
    plan = {}
    for row in wb["Approved 2026"].iter_rows(min_row=4, values_only=True):
        if not row or not row[2]:
            continue
        bays = set()
        for part in str(row[5]).replace(" ", "").split(","):
            g = re.fullmatch(r"F(\d+)(?:-F(\d+))?", part)
            if g:
                bays.update(range(int(g.group(1)), int(g.group(2) or g.group(1)) + 1))
        if not bays:
            continue
        v = row[7]
        end = 2036 * 12 if str(v).strip().lower().startswith("not in") else mk(pd.Timestamp(v) if not isinstance(v, str) else pd.to_datetime(v, format="%b %Y"))
        plan.setdefault(row[2], []).append((bays, end))

    def send(sub, bay):
        if sub not in plan:
            return 2036 * 12                      # AM-PC-014 4.2: no scheme in the program period
        b = int(bay[1:])
        hit = [e for bays, e in plan[sub] if b in bays]
        assert len(hit) == 1, (sub, bay, hit)
        return hit[0]

    live = fl[fl.status == "IN SERVICE"]
    cur = hi[hi.removed_date.isna()].set_index("asset_id")
    region = dict(zip(subs.sub_code, subs.region))
    lam, by_year, by_reg = 0.0, {}, {}
    for a, sub, bay in zip(live.asset_id, live.sub_code, live.bay):
        e = send(sub, bay)
        if e is None:
            continue
        ms = np.arange(H0, e)
        if not len(ms):
            continue
        fit = cur.loc[a, "fitted_date"]
        q = np.array([rate[band(age(fit, m))] for m in ms]) / 12.0
        surv = np.concatenate([[1.0], np.cumprod(1 - q)[:-1]])
        ef = surv * q + (1 - surv) * rate[0] / 12.0
        lam += ef.sum()
        for m, v in zip(ms, ef):
            by_year[m // 12] = by_year.get(m // 12, 0) + v
        by_reg[region[sub]] = by_reg.get(region[sub], 0) + ef.sum()
    psu = st[st.item_code == "VPR340-PSU-02"]
    avail = int(psu[psu.stock_state.isin(["SERVICEABLE", "AT REPAIR"])].quantity.sum())
    lots = next(n for n in range(0, 100) if poisson.cdf(avail + 25 * n, lam) >= 0.95)
    inserv = {y: int(sum((send(s, b) or 0) > y * 12 for s, b in zip(live.sub_code, live.bay))) for y in range(2027, 2036)}
    fails = []

    def chk(name, got, exp, tol=0.05):
        ok = got is not None and abs(float(got) - float(exp)) <= tol
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
    seen = 0
    for row in g["Lot settings"].iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        seen += 1
        chk("cover at %d lots" % row[0], row[3], round(100 * poisson.cdf(avail + 25 * row[0], lam), 1))
        chk("cost at %d lots" % row[0], row[4], row[0] * 25 * 1965, 0.5)
    chk("settings rows 8 to 22", seen, 15, 0)
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
