"""Independent verifier: reads only target/ and the golden workbook, shares no code with the
generator, rebuilds the move-on lists and the run-off, and checks the golden against them."""
import os
import sys

import openpyxl
import pandas as pd

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(target=None, golden=None):
    t = target or os.path.join(TASK, "target")
    g = golden or os.path.join(TASK, "golden")
    cases = pd.read_csv(os.path.join(t, "homelessness_cases_2026-09-30.csv"), dtype=str).fillna("")
    place = pd.read_csv(os.path.join(t, "ta_placements_2018-04_2026-09.csv"), dtype=str).fillna("")
    reviews = pd.read_csv(os.path.join(t, "bedroom_need_reviews.csv"), dtype=str)
    lets = pd.read_csv(os.path.join(t, "moveon_lets_2018-04_2026-09.csv"), dtype=str)

    cut = "2026-09-30"
    duty = cases[(cases["decision"] == "Main duty accepted") & (cases["decision_date"] <= cut)
                 & ((cases["closed_date"] == "") | (cases["closed_date"] > cut))].copy()
    need = dict(zip(cases["case_ref"], cases["bedrooms_needed_at_decision"]))
    for _, r in reviews.sort_values("review_date").iterrows():
        if r["review_date"] <= cut:
            need[r["case_ref"]] = r["bedrooms_after"]
    duty["need"] = duty["case_ref"].map(need).astype(int)
    in_th = set(place[(place["accommodation_type"] == "Tenter House") & (place["placement_start"] <= cut)
                      & ((place["placement_end"] == "") | (place["placement_end"] > cut))]["case_ref"])

    ws = openpyxl.load_workbook(os.path.join(t, "moveon_plan_2026-27.xlsx"))["Revised 14 Sep 2026"]
    plan = {}
    for row in ws.iter_rows(min_row=5, max_row=8, values_only=True):
        plan[4 if row[0] == "4+" else int(row[0])] = list(row[7:13])

    run, start = {}, {}
    for s in (1, 2, 3, 4):
        lst = duty[duty["need"] == s].sort_values(["decision_date", "case_ref"])["case_ref"].tolist()
        start[s] = sum(1 for x in lst if x in in_th)
        run[s] = []
        reached = 0
        for k in plan[s]:
            reached += k
            run[s].append(sum(1 for x in lst[reached:] if x in in_th))
    units = {s: run[s][-1] for s in run}
    ws = openpyxl.load_workbook(os.path.join(t, "dps_lot2_lot3_price_schedule.xlsx"))["Rates"]
    rate = {}
    for row in ws.iter_rows(min_row=5, values_only=True):
        if row[0] == "3":
            rate[4 if row[3] == "4+" else int(row[3])] = row[5]
    cost = sum(units[s] * rate[s] for s in units)

    # the order the lets log follows, re-checked with plain loops: the lets of one size starting on one
    # day go to the households at the front of that size's list that day
    acc = cases[cases["decision"] == "Main duty accepted"].sort_values(["decision_date", "case_ref"])
    rv = reviews.sort_values("review_date")
    gone = set()
    ok = n = 0
    started = lets[lets["let_status"] == "Tenancy started"]
    for (day, beds), grp in started.groupby(["tenancy_start", "bedrooms"]):
        nd = dict(zip(acc["case_ref"], acc["bedrooms_needed_at_decision"]))
        for _, r in rv[rv["review_date"] <= day].iterrows():
            nd[r["case_ref"]] = r["bedrooms_after"]
        live = acc[(acc["decision_date"] <= day) & ((acc["closed_date"] == "") | (acc["closed_date"] >= day))
                   & ~acc["case_ref"].isin(gone)]
        front = [x for x in live["case_ref"] if str(nd[x]) == str(beds)][:len(grp)]
        ok += len(set(front) & set(grp["case_ref"]))
        n += len(grp)
        gone |= set(grp["case_ref"])

    print("Tenter House on the cut", start, "total", sum(start.values()))
    print("run-off", run)
    print("call-off", units, "total", sum(units.values()), "weekly cost %.2f" % cost)
    print("lets reproduced by the duty-date list: %d of %d" % (ok, n))

    good = ok == n
    wb = openpyxl.load_workbook(os.path.join(g, "tenter_house_replacement_units.xlsx"))
    co = wb["Call-off"]
    for r in range(5, 9):
        s = {"1 bed": 1, "2 bed": 2, "3 bed": 3, "4+ bed": 4}[co.cell(row=r, column=1).value]
        good &= co.cell(row=r, column=2).value == start[s]
        good &= co.cell(row=r, column=3).value == run[s][-1]
        good &= co.cell(row=r, column=4).value == units[s]
        good &= abs(co.cell(row=r, column=5).value - rate[s]) < 1e-9
    good &= co.cell(row=11, column=6).value == int(round(cost))
    ro = wb["Run-off"]
    for r in range(5, 9):
        s = {"1 bed": 1, "2 bed": 2, "3 bed": 3, "4+ bed": 4}[ro.cell(row=r, column=1).value]
        good &= ro.cell(row=r, column=2).value == start[s]
        good &= [ro.cell(row=r, column=j).value for j in range(3, 9)] == run[s]
    print("golden workbook matches the recomputation:", good)
    return good


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
