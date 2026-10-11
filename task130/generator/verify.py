"""Independent verifier: reads only target/ and the golden workbook, shares no code with the
generator, rebuilds the move-on lists round by round and the run-off, and checks the golden against them."""
import datetime as dt
import itertools
import os
import sys

import openpyxl
import pandas as pd

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def age(born, day):
    years = day.year - born.year
    if (day.month, day.day) < (born.month, born.day):
        years -= 1
    return years


def can_share(a, b):
    return (a[0] < 10 and b[0] < 10) or a[1] == b[1]


def best_pairs(kids):
    """brute force: the largest set of disjoint sharing pairs"""
    if len(kids) < 2:
        return 0
    first, rest = kids[0], kids[1:]
    best = best_pairs(rest)
    for i, other in enumerate(rest):
        if can_share(first, other):
            best = max(best, 1 + best_pairs(rest[:i] + rest[i + 1:]))
    return best


def bedrooms(people, day):
    rooms = 1
    kids = []
    for rel, sex, born in people:
        if rel in ("Applicant", "Partner") or born > day:
            continue
        a = age(born, day)
        if a >= 16:
            rooms += 1
        else:
            kids.append((a, sex))
    return rooms + len(kids) - best_pairs(kids)


def third_monday_before(month_start):
    y, m = month_start.year, month_start.month - 1
    if m == 0:
        y, m = y - 1, 12
    d = dt.date(y, m, 1)
    mondays = [d + dt.timedelta(days=i) for i in range(31)
               if (d + dt.timedelta(days=i)).month == m and (d + dt.timedelta(days=i)).weekday() == 0]
    return mondays[2]


def main(target=None, golden=None):
    t = target or os.path.join(TASK, "target")
    g = golden or os.path.join(TASK, "golden")
    cases = pd.read_csv(os.path.join(t, "homelessness_cases_2026-09-30.csv"), dtype=str).fillna("")
    place = pd.read_csv(os.path.join(t, "ta_placements_2018-04_2026-09.csv"), dtype=str).fillna("")
    members = pd.read_csv(os.path.join(t, "household_members_2026-09-30.csv"), dtype=str)
    lets = pd.read_csv(os.path.join(t, "moveon_lets_2018-04_2026-09.csv"), dtype=str)

    cut = "2026-09-30"
    duty = cases[(cases["decision"] == "Main duty accepted") & (cases["decision_date"] <= cut)
                 & ((cases["closed_date"] == "") | (cases["closed_date"] > cut))]
    duty = duty.sort_values(["decision_date", "case_ref"])
    order = duty["case_ref"].tolist()
    people = {}
    for _, r in members.iterrows():
        people.setdefault(r["case_ref"], []).append(
            (r["relationship"], r["sex"], dt.date.fromisoformat(r["date_of_birth"])))
    in_th = set(place[(place["accommodation_type"] == "Tenter House") & (place["placement_start"] <= cut)
                      & ((place["placement_end"] == "") | (place["placement_end"] > cut))]["case_ref"])
    april = dt.date(2027, 4, 1)
    unit = {x: min(bedrooms(people[x], april), 4) for x in in_th}

    ws = openpyxl.load_workbook(os.path.join(t, "moveon_plan_2026-27.xlsx"))["Revised 14 Sep 2026"]
    plan = {}
    for row in ws.iter_rows(min_row=5, max_row=9, values_only=True):
        plan[5 if row[0] == "5 or more" else int(row[0])] = list(row[7:13])

    # October: the lets accepted in the September round
    done = set(lets.loc[lets["let_status"] == "Accepted, tenancy to start", "case_ref"])
    month_end = []

    def tally():
        out = {s: 0 for s in (1, 2, 3, 4)}
        for x in in_th:
            if x not in done:
                out[unit[x]] += 1
        month_end.append(out)
    tally()
    for k, (y, m) in enumerate([(2026, 11), (2026, 12), (2027, 1), (2027, 2), (2027, 3)], 1):
        day = third_monday_before(dt.date(y, m, 1))
        need = {x: bedrooms(people[x], day) for x in order if x not in done}
        for s in (1, 2, 3, 4, 5):
            n = plan[s][k]
            front = [x for x in order if x not in done and need[x] == s][:n]
            done |= set(front)
        tally()
    run = {s: [me[s] for me in month_end] for s in (1, 2, 3, 4)}
    units = {s: run[s][-1] for s in run}
    start = {s: sum(1 for x in in_th if unit[x] == s) for s in (1, 2, 3, 4)}

    ws = openpyxl.load_workbook(os.path.join(t, "dps_lot2_lot3_price_schedule.xlsx"))["Rates"]
    rate = {}
    for row in ws.iter_rows(min_row=5, values_only=True):
        if row[0] == "3":
            rate[4 if row[3] == "4+" else int(row[3])] = row[5]
    cost = sum(units[s] * rate[s] for s in units)

    # the September round, re-checked with plain loops: each home went to the first household on the list
    # for its bedrooms on 21 September, the need worked out from the people on the application
    sept = dt.date(2026, 9, 21)
    acc = lets[lets["let_status"] == "Accepted, tenancy to start"]
    on_list = [x for x in order if x in people]
    ok = 0
    for beds, grp in acc.groupby("bedrooms"):
        b = int(beds)
        front = [x for x in on_list if bedrooms(people[x], sept) == b][:len(grp)]
        ok += len(set(front) & set(grp["case_ref"]))

    print("Tenter House on the cut, by unit on 1 April", start, "total", sum(start.values()))
    print("run-off", run)
    print("call-off", units, "total", sum(units.values()), "weekly cost %.2f" % cost)
    print("September round lets reproduced from the application: %d of %d" % (ok, len(acc)))

    good = ok == len(acc)
    wb = openpyxl.load_workbook(os.path.join(g, "tenter_house_replacement_units.xlsx"))
    co = wb["Call-off"]
    lab = {"1 bed": 1, "2 bed": 2, "3 bed": 3, "4+ bed": 4}
    for r in range(5, 9):
        s = lab[co.cell(row=r, column=1).value]
        good &= co.cell(row=r, column=2).value == start[s]
        good &= co.cell(row=r, column=3).value == run[s][-1]
        good &= co.cell(row=r, column=4).value == units[s]
        good &= abs(co.cell(row=r, column=5).value - rate[s]) < 1e-9
    good &= co.cell(row=11, column=6).value == int(round(cost))
    ro = wb["Run-off"]
    for r in range(5, 9):
        s = lab[ro.cell(row=r, column=1).value]
        good &= ro.cell(row=r, column=2).value == start[s]
        good &= [ro.cell(row=r, column=j).value for j in range(3, 9)] == run[s]
    print("golden workbook matches the recomputation:", good)
    return good


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
