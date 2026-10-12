"""The independent verifier. It reads only the files under target/ and imports nothing from the generator: it
rebuilds each working weekday's trip from the probe exports and the route file, recomputes the departure and its
two counts, the riders (late requests mapped to employee numbers through the HR extract), the vehicles and seats
left empty, the deadhead miles in the release the operator's route was set up under, and each departure's late
staff arrivals and 2027 cost.

    python3 task254/generator/verify.py [target_dir]
"""
import datetime as dt
import glob
import math
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd
from openpyxl import load_workbook

WINDOW = (dt.date(2025, 10, 1), dt.date(2026, 9, 30))      # the prompt's twelve months to September 2026
BAR = 8 * 60
DEPS = [6 * 60 + 30 + 5 * i for i in range(11)]
ASK_DEPS = [d for d in DEPS if d >= 6 * 60 + 50]


def table(path, sheet, first):
    """A sheet's rows below its header row (the row whose first cell is `first`), blank rows dropped."""
    rows = list(load_workbook(path, read_only=True, data_only=True)[sheet].iter_rows(values_only=True))
    h = next(i for i, r in enumerate(rows) if r and r[0] == first)
    head = [str(x) for x in rows[h]]
    return [dict(zip(head, r)) for r in rows[h + 1:] if r and any(v is not None for v in r)]


def hhmm(v):
    """A start time in any of the three forms the pack writes: '08:00', '8:00 AM', 800."""
    if isinstance(v, (int, np.integer)):
        return int(v)
    s = str(v).strip().upper()
    m = re.fullmatch(r"(\d{1,2}):(\d{2})(?:\s*([AP])M)?", s)
    h, mi = int(m.group(1)), int(m.group(2))
    if m.group(3) == "P" and h != 12:
        h += 12
    if m.group(3) == "A" and h == 12:
        h = 0
    return 100 * h + mi


def working_days(target):
    hol = {r["Date"].date() for r in table(os.path.join(target, "hr_holiday_calendars.xlsx"), "2025-26", "Date")}
    out, d = [], WINDOW[0]
    while d <= WINDOW[1]:
        if d.weekday() < 5 and d not in hol:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def route(target):
    rows = table(os.path.join(target, "route_cedar_grove_to_brook_st.xlsx"), "Route", "Seq")
    rows.sort(key=lambda r: r["Seq"])
    legs = [r for r in rows if r["Type"] == "Leg"]
    codes = [r["TMC"] for r in rows if r["Type"] == "TMC"]
    assert rows[0]["Type"] == "Leg" and rows[-1]["Type"] == "Leg" and len(legs) == 2
    return float(legs[0]["Fixed minutes"]), codes, float(legs[1]["Fixed minutes"])


def trips(target):
    lot, codes, stop = route(target)
    days = working_days(target)
    di = {d.isoformat(): i for i, d in enumerate(days)}
    ci = {c: k for k, c in enumerate(codes)}
    arr = np.full((len(days), 48, len(codes)), np.nan)
    for f in sorted(glob.glob(os.path.join(target, "trelvane_tmc_export_*.csv"))):
        df = pd.read_csv(f, usecols=["tmc_code", "measurement_tstamp", "travel_time_passenger"],
                         dtype={"tmc_code": str, "measurement_tstamp": str})
        df = df[df.tmc_code.isin(ci)]
        day = df.measurement_tstamp.str[:10]
        df = df[day.isin(di)]
        ts = df.measurement_tstamp
        mins = ts.str[11:13].astype(int) * 60 + ts.str[14:16].astype(int)
        e = ((mins - 330) // 5).to_numpy()
        assert (e >= 0).all() and (e < 48).all()
        arr[df.measurement_tstamp.str[:10].map(di).to_numpy(), e, df.tmc_code.map(ci).to_numpy()] = \
            df.travel_time_passenger.to_numpy(float)
    assert not np.isnan(arr).any(), "a route segment is missing a passenger value in a morning epoch"
    rows = np.arange(len(days))
    arrival = {}
    for dep in DEPS:
        t = np.full(len(days), dep + lot)
        for k in range(len(codes)):
            e = np.floor((t - 330) / 5).astype(int)
            assert (e >= 0).all() and (e < 48).all()
            t = t + arr[rows, e, k] / 60.0
        arrival[dep] = t + stop
    return days, arrival


def riders(target):
    wbp = os.path.join(target, "cedar_grove_reassignment_list.xlsx")
    permit = table(wbp, "Permit roll", "Permit")
    late = table(wbp, "Late requests", "Request")
    opt = {int(r["Employee no."]) for r in table(wbp, "Opt-outs", "Employee no.")}
    hr = pd.read_csv(os.path.join(target, "hr_staff_extract_2026-10-02.csv"), dtype={"payroll_id": str})
    pay = dict(zip(hr.payroll_id, hr.employee_no.astype(int)))
    people = {}
    for r in permit:
        if hhmm(r["Start"]) == 800:
            people[int(r["Employee no."])] = r["Department"]
    on_both = 0
    for r in late:
        if hhmm(r["Start"]) == 800:
            e = pay[str(r["Payroll ID"])]
            on_both += e in people
            people[e] = r["Department"]
    ride = {e: d for e, d in people.items() if e not in opt}
    by = {}
    for d in ride.values():
        by[d] = by.get(d, 0) + 1
    return len(ride), by, on_both


def charges(target):
    rows = table(os.path.join(target, "ridgeline_schedule_of_charges_2027.xlsx"), "Charges 2027", "Item")
    get = {r["Item"]: r["Amount"] for r in rows}
    return int(get["Seats per vehicle"]), float(get["Day charge, morning run"]), float(get["Deadhead to yard"])


def deadhead_miles(target):
    """The operator's deadhead route (set up October 2025) with each code's length in the network release in
    force then."""
    rows = table(os.path.join(target, "ridgeline_deadhead_route_brook_st_yard.xlsx"), "Deadhead", "Seq")
    tmc = pd.read_csv(os.path.join(target, "TMC_Identification.csv"), dtype={"tmc": str, "network_release": str})
    eff = tmc.groupby("network_release").effective_date.first()
    rel = max(r for r, d in eff.items() if d <= "2025-10-31")
    look = tmc[tmc.network_release == rel].set_index("tmc")
    miles = 0.0
    for r in rows:
        if r["Type"] == "Leg":
            miles += float(r["Leg miles"])
        else:
            miles += float(look.loc[r["TMC"], "miles"])
    return round(miles, 6), rel


def holdover(target):
    with zipfile.ZipFile(os.path.join(target, "shuttle_service_budget_note_2027.docx")) as z:
        x = re.sub(r"<[^>]+>", "", z.read("word/document.xml").decode("utf-8"))
    return float(re.search(r"costed at \$(\d+\.\d\d)", x).group(1))


def service_days_2027(target):
    hol = {r["Date"].date() for r in table(os.path.join(target, "hr_holiday_calendars.xlsx"), "2027", "Date")}
    d, n = dt.date(2027, 1, 1), 0
    while d.year == 2027:
        n += d.weekday() < 5 and d not in hol
        d += dt.timedelta(days=1)
    return n


def run(target):
    days, arrival = trips(target)
    N = len(days)
    need = math.ceil(0.9 * N)
    on = {d: int((arrival[d] <= BAR).sum()) for d in DEPS}
    call = [d for d in DEPS if on[d] >= need][-1]
    n_r, by, both = riders(target)
    seats, day_rate, mile_rate = charges(target)
    veh = -(-n_r // seats)
    miles, rel = deadhead_miles(target)
    hold = holdover(target)
    d27 = service_days_2027(target)
    late = {d: n_r * (N - on[d]) for d in ASK_DEPS}
    fixed_cents = round(veh * d27 * (day_rate + mile_rate * miles) * 100)
    cost = {d: (fixed_cents + round(hold * 100) * late[d]) / 100.0 for d in ASK_DEPS}
    near = min(float(np.min(np.abs(arrival[d] - BAR))) for d in DEPS) * 60
    return {"N": N, "need": need, "on_time": on, "call": call, "riders": n_r, "by_dept": by, "both_sheets": both,
            "vehicles": veh, "seats_empty": veh * seats - n_r, "miles": miles, "release": rel, "service_days": d27,
            "late_arrivals": late, "cost": cost, "nearest_seconds": near}


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                            "target")
    v = run(tgt)
    print("call %d:%02d a.m.: on time %d and %d of %d (bar %d)" % (v["call"] // 60, v["call"] % 60, v["on_time"][v["call"]],
                                                                 v["on_time"][v["call"] + 5], v["N"], v["need"]))
    print("riders %d (on both sheets %d), vehicles %d, seats left empty %d" % (v["riders"], v["both_sheets"],
                                                                          v["vehicles"], v["seats_empty"]))
    print("deadhead %.2f miles (release %s), %d service days in 2027" % (v["miles"], v["release"], v["service_days"]))
    for d in ASK_DEPS:
        print("  %d:%02d  late arrivals %6s  cost $%s" % (d // 60, d % 60, "{:,}".format(v["late_arrivals"][d]),
                                                       "{:,}".format(int(round(v["cost"][d])))))
