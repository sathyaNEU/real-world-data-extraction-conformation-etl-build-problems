"""The ask sheet's cracker and mirror, run as code on the cut pack.

The cracker lands the call, runs the hygiene battery (the month-boundary repeats, the switch's legs, the test calls,
the number formats, the two export layouts, the payroll's two layouts), executes every filed rule (the policy's
calling hours, its count-once rule, its shift allocation and its training exclusion) and reads every document; it
takes each ask the careful way short of the reconstruction the ask's device needs:
  A  household state by the number dialed, then by the case number the dialer wrote from July, else the area code;
  B  the dialer's completed rows once per case number, plus the line's completed calls read on their first leg;
  C  the policy's allocation by talk and wrap time in each shift, the July to December payroll read as decimal hours.
The mirror stops at the most attractive wrong rung: area codes for any number the case record lacks with Arizona on
daylight time, the dialer's completed rows as invoiced, and payroll hours by the shift's project code.

    python3 task241/generator/ceiling.py [target]
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as S_

CALL, IF, MISS = 38.0, 7.0, 5.0      # the landed call, instruction following, the best miss off the call
ASKS = 55.0


def digest(target):
    h = hashlib.sha256()
    for root, _, files in sorted(os.walk(target)):
        for f in sorted(files):
            h.update(open(os.path.join(root, f), "rb").read())
    return h.hexdigest()[:12]


def main(target):
    S = S_.solve(target)
    c, inb, reg, cases, zones, jobs = S["calls"], S["inbound"], S["reg"], S["cases"], S["zones"], S["jobs"]
    ts_dec = S_.load_hours(target, hhmm=False)
    gold = {"A": S["askA"], "B": S["askB"], "C": S["askC"].map(lambda x: int(10 * x + 0.5) / 10)}
    crack = {"A": S_.calling_hours(c, cases, zones, jobs, route="cracker"),
             "B": S_.completes(c, inb, reg, cases, jobs, route="cracker"),
             "C": S_.hours(c, ts_dec, jobs).map(lambda x: int(10 * x + 0.5) / 10)}
    mirror = {"A": S_.calling_hours(c, cases, zones, jobs, route="mirror", arizona_dst=True),
              "B": S_.completes(c, inb, reg, cases, jobs, route="invoiced"),
              "C": S_.hours(c, ts_dec, jobs, route="by_code").map(lambda x: int(10 * x + 0.5) / 10)}
    tol = {"A": 0.5, "B": 0.5, "C": 0.05}
    total = kc = km = 0
    print("pack %s" % digest(target))
    print("%-4s %8s %8s" % ("ask", "cracker", "mirror"))
    for k in ("A", "B", "C"):
        hc = int(((crack[k] - gold[k]).abs() < tol[k]).sum())
        hm = int(((mirror[k] - gold[k]).abs() < tol[k]).sum())
        total += len(jobs)
        kc += hc
        km += hm
        print("%-4s %5d/%d %5d/%d" % (k, hc, len(jobs), hm, len(jobs)))
    lc, lm = kc / total, km / total
    pair = (CALL + IF + ASKS * lc + MISS + IF + ASKS * lm) / 2
    print("cracker keeps %.1f per cent of ask weight, mirror %.1f per cent" % (100 * lc, 100 * lm))
    print("pair ceiling %.1f" % pair)
    return dict(cracker=lc, mirror=lm, pair=pair)


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    main(t)
