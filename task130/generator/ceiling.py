"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files at the prompt's rounding
(cases and awards whole, hours and dollars to the unit, rates to two decimals), and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task130/generator/ceiling.py

Rows: the cracker lands the call and runs the battery: it stacks the two case systems, keeps each case's latest
revision, drops linked recurrences and mutual-aid work, places each case on the injured employee's crew on the day,
nets paid leave and holiday pay out of the hours, books each prior-period adjustment to the pay period it corrects
and nets payroll reversals; but it reads each hour in the district the timesheet row carries and each award line on
the crew the payroll report carries. The mirror stops at rung 0 on the call and handles the asks the same way,
since they carry nothing from the call. The full includer also places each hour on its crew's district and each
award line on the crew the member was on on the milestone date (a stress row, not the gate)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import analysis as AN   # noqa: E402
import world as W       # noqa: E402

TOL = {"cases": 0.5, "hours": 0.5, "rate": 0.005, "crew_rate": 0.005, "milestones": 0.5, "usd": 0.5}


def kept(resp, gold):
    return sum(abs(resp[dd][k] - gold[dd][k]) < TOL[k] for dd in W.DISTRICTS for k in TOL)


def main(target=TARGET):
    D = AN.load(target)
    cs = AN.attach(AN.new_cases(AN.cases(D)), D)
    H = AN.hours_by(D)
    gold = AN.asks(D, cs, H)
    n = len(W.DISTRICTS) * len(TOL)
    crack = kept(AN.asks(D, cs, H, report_codes=False, timesheet_district=True, case_location=True), gold)
    full = kept(gold, gold)
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    by = {k: sum(abs(AN.asks(D, cs, H, report_codes=False, timesheet_district=True, case_location=True)[dd][k] - gold[dd][k]) < TOL[k]
                 for dd in W.DISTRICTS) for k in TOL}
    print("cracker (lands the call, runs the battery; the timesheet row's district, the case record's district): keeps "
          "%d of %d ask criteria %s, response %.1f" % (crack, n, by, c))
    print("mirror (rung 0 on the call, same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
    print("full includer (each hour and each case on its crew's district on the day; stress row): keeps "
          "%d of %d, response %.1f" % (full, n, 38 + 7 + 55 * full / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return dict(crack=crack, n=n, pair=(c + s) / 2, leakage=100 * lc, by=by)


if __name__ == "__main__":
    main()
