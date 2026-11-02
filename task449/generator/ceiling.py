"""Pair ceiling on the cut pack: the cracker (on the call) and the mirror (off it, on the default list), each ask
figure scored by what that response's own handling computes from target/.

Rubric model (supplemental-stumping Part 0): 38 for the call and its components, 7 for instruction-following, 55
spread evenly over the twelve ask figures; a figure is kept when the response's value, at the asked rounding, equals
the golden's. Routes:

  referral route   the careful route through the referral logs: every hire on either platform at the start date its
                   referral records, the referral date on the record that shows the hire, a job ending before day 90
                   read from the job_end reports
  reports route    the starts read from the job_start reports at the posting's employer account (by its number, or
                   its operating or legal name as typed), the separations from the job_end reports at that account,
                   the referral date on the hire's own record
  ROE route        the reports route with separations from the Records of Employment instead (latest versions,
                   matched on the account's business number)
  full includer    every device found and handled: the golden

    python3 task449/generator/ceiling.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A     # noqa: E402
import asks as K         # noqa: E402
import golden as G       # noqa: E402

TGT = os.path.join(os.path.dirname(HERE), "target")
ROUTES = {
    "referral": dict(start_route="referral", sep_sources=("reports",), carry="record"),
    "reports": dict(start_route="account", sep_sources=("reports",), carry="record"),
    "roe": dict(start_route="account", sep_sources=("roe",), carry="record"),
    "full": dict(),
}


def ask_values(route, cache):
    r = K.compute(TGT, cache, **ROUTES[route])
    out = {}
    for k in range(4):
        out["starts_q%d" % (k + 1)] = r["starts"][k]
        out["retained_q%d" % (k + 1)] = r["retained"][k]
        out["avg_days_q%d" % (k + 1)] = "%.1f" % G.r1(r["avg_days"][k])
    return out


def score(figs, call_right, route, cache):
    vals = ask_values(route, cache)
    keys = sorted(vals)
    kept = [k for k in keys if vals[k] == figs[k]]
    return (38.0 if call_right else 0.0) + 7.0 + 55.0 * len(kept) / len(keys), len(kept), len(keys), kept, vals


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    gold = A.compute(TGT)
    live = A.compute(TGT, mode="live")
    call_cracker = gold["listed"] == figs["listed"]
    call_mirror = live["listed"] == figs["listed"]
    assert call_cracker and not call_mirror
    cache = {}
    rows = []
    for name, call, route in (("cracker (on the call, referral route)", call_cracker, "referral"),
                              ("mirror (default list, referral route)", call_mirror, "referral"),
                              ("cracker (on the call, reports route)", call_cracker, "reports"),
                              ("mirror (default list, reports route)", call_mirror, "reports"),
                              ("cracker (on the call, ROE route)", call_cracker, "roe"),
                              ("mirror (default list, ROE route)", call_mirror, "roe"),
                              ("full includer (every device handled)", call_cracker, "full")):
        s, n, N, kept, vals = score(figs, call, route, cache)
        rows.append((name, s, n, N, kept))
        print("%-40s %5.1f  asks kept %2d of %d %s" % (name, s, n, N, kept))
    for i, label in ((0, "referral route"), (2, "reports route"), (4, "ROE route")):
        print("pair ceiling, %s %.1f; mirror leakage %.1f per cent of ask weight"
              % (label, (rows[i][1] + rows[i + 1][1]) / 2, 100.0 * rows[i + 1][2] / rows[i + 1][3]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
