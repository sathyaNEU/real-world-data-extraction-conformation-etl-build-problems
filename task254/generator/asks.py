"""The ask layer: the staff who will ride the morning shuttle, the vehicles it needs and the seats left empty
(Ask A), and at each departure from 6:50 to 7:20 the staff arrivals a year that would have been late and what
holding that departure would cost in 2027 (Ask B)."""
import datetime as dt

import numpy as np

import core

DEPTS = ["Nursing", "Imaging", "Laboratory", "Pharmacy", "Rehabilitation", "Support Services", "Administration"]
# riders by department (golden), the people on both sheets (R1), late requests only, opt-outs among 8:00 starters
GOLD = dict(zip(DEPTS, [150, 52, 46, 34, 31, 57, 40]))
DUP = dict(zip(DEPTS, [12, 5, 4, 3, 3, 4, 3]))
LATE_ONLY = dict(zip(DEPTS, [18, 7, 6, 5, 4, 8, 5]))
OPT_8 = dict(zip(DEPTS, [4, 2, 2, 1, 1, 2, 1]))
OTHER_STARTS = {730: 40, 830: 30, 900: 30}          # permit-roll rows with other starts
LATE_OTHER = {730: 12, 830: 11, 900: 10}
OPT_OTHER = 12

# the operator's 2027 schedule of charges and the finance budget note
DAY_RATE = 214.00         # per vehicle per service day, the morning run from pull-out to the Brook Street stop
MILE_RATE = 3.50          # per vehicle-mile, the deadhead back from the stop to the yard
HOLDOVER = 38.00          # per late staff arrival (the budget note's hold-over and lost-time cost)
SEATS = 28
LEG_MILES_IN, LEG_MILES_OUT = 0.8, 2.1     # stop to the I-65 S on-ramp; Exit 128 to the Fern Valley yard
ASK_DEPS = [d for d in core.DEPARTURES if d >= 6 * 60 + 50]          # 6:50 to 7:20


def staff_world(seed):
    """HR extract and the reassignment workbook's three sheets, laid so that the riders by department are GOLD.
    Permit-roll rows carry the employee number, late-request rows the payroll identifier; R1's people appear on
    both."""
    rng = np.random.default_rng([seed, 31])
    weights = np.array([0.46, 0.10, 0.09, 0.06, 0.06, 0.13, 0.10])
    n_hr = 1932
    dept = rng.choice(DEPTS, size=n_hr, p=weights)
    emp = rng.choice(np.arange(104000, 199999), size=n_hr, replace=False)
    pay = rng.choice(np.arange(3000000, 3999999), size=n_hr, replace=False)
    start = rng.choice([700, 730, 800, 830, 900, 1100, 1500, 1900], size=n_hr,
                       p=[0.20, 0.07, 0.36, 0.06, 0.06, 0.05, 0.05, 0.15])
    hr = [{"employee_no": int(e), "payroll_id": "P%07d" % p, "department": str(d), "start": int(s)}
          for e, p, d, s in zip(emp, pay, dept, start)]
    by = {d: {s: [h for h in hr if h["department"] == d and h["start"] == s] for s in (730, 800, 830, 900)}
          for d in DEPTS}
    used = set()

    def take(d, s, n):
        pool = [h for h in by[d][s] if h["employee_no"] not in used]
        assert len(pool) >= n, (d, s, n, len(pool))
        pick = [pool[i] for i in sorted(rng.choice(len(pool), size=n, replace=False))]
        for h in pick:
            used.add(h["employee_no"])
        return pick
    roll, req, opt, dup = [], [], [], []
    for d in DEPTS:
        r = take(d, 800, GOLD[d] + OPT_8[d] - LATE_ONLY[d])
        roll += r
        opt += r[:OPT_8[d]]
        rest = r[OPT_8[d]:]
        both = [rest[i] for i in sorted(rng.choice(len(rest), size=DUP[d], replace=False))]
        dup += both
        req += both + take(d, 800, LATE_ONLY[d])
    def any_dept(s):
        free = np.array([sum(h["employee_no"] not in used for h in by[d][s]) > 0 for d in DEPTS])
        w = weights * free
        return DEPTS[int(rng.choice(len(DEPTS), p=w / w.sum()))]
    for s, n in OTHER_STARTS.items():
        for _ in range(n):
            roll += take(any_dept(s), s, 1)
    for s, n in LATE_OTHER.items():
        for _ in range(n):
            req += take(any_dept(s), s, 1)
    others = [h for h in roll if h["start"] != 800]
    opt += [others[i] for i in sorted(rng.choice(len(others), size=OPT_OTHER, replace=False))]
    permit = [{"employee_no": h["employee_no"], "department": h["department"], "start": h["start"]} for h in roll]
    late = [{"payroll_id": h["payroll_id"], "department": h["department"], "start": h["start"]} for h in req]
    optout = [{"employee_no": h["employee_no"]} for h in opt]
    return {"hr": hr, "permit": permit, "late": late, "optout": optout,
            "dup": {h["employee_no"] for h in dup}}


READS = {"golden": (False, False, False), "natural": (True, False, False), "keep_opt": (False, True, False),
         "all_starts": (False, False, True)}


def riders(S, read="golden", r1=None, keep_opt=None, all_starts=None):
    """Riders by department: 8:00 starters on either sheet of the reassignment workbook, less opt-outs, each person
    once (late requests mapped to employee numbers through HR). The mishandlings, alone or together: r1 (natural)
    the two sheets added, each sheet's rows taken as distinct people; keep_opt the opt-outs not applied; all_starts
    every start time kept."""
    d1, d2, d3 = READS[read]
    r1 = d1 if r1 is None else r1
    keep_opt = d2 if keep_opt is None else keep_opt
    all_starts = d3 if all_starts is None else all_starts
    opted = set() if keep_opt else {h["employee_no"] for h in S["optout"]}
    pay2emp = {h["payroll_id"]: h["employee_no"] for h in S["hr"]}
    ok = (lambda r: True) if all_starts else (lambda r: r["start"] == 800)
    out = {d: 0 for d in DEPTS}
    if r1:
        for r in S["permit"]:
            if ok(r) and r["employee_no"] not in opted:
                out[r["department"]] += 1
        for r in S["late"]:
            if ok(r):
                out[r["department"]] += 1
        return out
    seen = set()
    for r in S["permit"] + S["late"]:
        e = r["employee_no"] if "employee_no" in r else pay2emp[r["payroll_id"]]
        if e in seen or not ok(r) or e in opted:
            continue
        seen.add(e)
        out[r["department"]] += 1
    return out


def vehicles(n):
    return -(-n // SEATS)


# ------------------------------------------------------------------------------------------------ the budget
def deadhead_miles(lookup="golden"):
    """The deadhead route's miles: the fixed legs and each listed code's length. golden: the stretch the route
    runs on (1.21 miles, under the 2025 code or the two 2026 codes that replaced it); current: every listed code
    looked up in the 2026 release, which puts 121N04637 on the I-264 collector ramp; drop: the reissued code left
    out."""
    miles = LEG_MILES_IN + LEG_MILES_OUT
    for i, r in enumerate(core.DEADHEAD):
        if i == core.T1_INDEX and lookup == "current":
            miles += core.RAMP[3]
        elif i == core.T1_INDEX and lookup == "drop":
            continue
        else:
            miles += r[4]
    return miles


def cost(late_days, n_riders, n_veh, miles):
    """The 2027 cost of holding a departure: the vehicles' day charges and deadhead mileage over the 2027 service
    days, and the hold-over cost of each late staff arrival (late working weekdays of the evidence year, each
    carrying every rider, taken as 2027's)."""
    days = core.working_days_2027()
    return n_veh * days * (DAY_RATE + MILE_RATE * miles) + HOLDOVER * n_riders * late_days


def ask_figures(late, n_riders, miles):
    """late: {departure: late working weekdays}. Returns the asks' figures."""
    v = vehicles(n_riders)
    return {"riders": n_riders, "vehicles": v, "seats_empty": v * SEATS - n_riders,
            "late_arrivals": {d: n_riders * late[d] for d in ASK_DEPS},
            "cost": {d: cost(late[d], n_riders, v, miles) for d in ASK_DEPS}}
