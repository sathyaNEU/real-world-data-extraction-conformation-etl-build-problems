"""task179 ask ceiling, run on the cut pack: the cracker (a response on the call that runs the hygiene battery and
executes every rule Schedule C and Directive 26-07 file: it maps every client reference through the crosswalk, takes
custody from both jails in Merrow time, credits the days after a transfer, drops voided events, reads every report and
supplement, sets a household one zone, keeps a re-booked incident's zones and drops businesses, the public and victims
living outside the city) and the mirror (the strongest response off the call, which takes the vendor's export and the
incident extract as they read), scored cell by cell against the golden, then the pair arithmetic on
supplemental-stumping Part 0's weights (38 recommendation and components, 7 instruction-following, 55 asks; a missed
call keeps about 5). The cracker's two stops are the devices: it counts a client per vendor record, and it compares
residences as written once case and spacing are evened.

    python3 ceiling.py <target>"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
from collections import defaultdict

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc        # noqa: E402
import common as C  # noqa: E402

D = dt.date


def days(a, b):
    return {a + dt.timedelta(days=k) for k in range((b - a).days + 1)}


def gps(sol, by_person=True, custody=True, region=True):
    ev = calc.gps_events(sol)
    pid_to_sid = {v: k for k, v in sol.sup.sid_to_pid.items()}
    months = [0] * 12
    recs = []
    for ref, g in ev.groupby("client_ref"):
        h, s_ = calc._ref_days(g)
        recs.append((g["pid"].iloc[0], h, s_))
    if by_person:
        merged = defaultdict(lambda: [set(), set()])
        for p, h, s_ in recs:
            merged[p][0] |= h
            merged[p][1] |= s_
        recs = [(p, h, s_) for p, (h, s_) in merged.items()]
    for p, held, susp in recs:
        cust = calc.custody_days(sol.bk, pid_to_sid.get(p)) if custody and p in pid_to_sid else set()
        for x in held:
            if x.year == 2026 and x not in susp and x not in cust and (not region or sol.sup.supervised(p, x)):
                months[x.month - 1] += 1
    return months


def zones(sol, residences=True, per_incident=True, all_rows=True, addr_norm=True):
    h = sol.d["hpd"]
    if not all_rows:
        h = h[h["supplement_no"] == "0"]
    h = h[(h["victim_type"] == "I") & (h["victim_res_city"] == "HALVERTON") & (h["victim_residence"] != "")]
    res = defaultdict(set)
    for num, seq, a in zip(h["incident_number"], h["victim_seq"], h["victim_residence"]):
        res[num].add(calc.norm_addr(a) if (residences and addr_norm) else (" ".join(a.upper().split()) if residences else seq))
    nb = sol.panel.nb
    nb = nb[(nb["agency"] == "HPD") & nb["schedb"] & (nb["date"] >= D(2026, 1, 1)) & (nb["date"] <= C.RECORDS_END)].sort_values("booked")
    seen = set()
    cells = defaultdict(int)
    nb_all = sol.panel.nb
    nb_all = nb_all[(nb_all["agency"] == "HPD") & nb_all["schedb"]].sort_values("booked")
    for p, case, jail, d in zip(nb_all["pid"], nb_all["case"], nb_all["jail"], nb_all["date"]):
        num = calc.hpd_number(case, jail)
        if num is None:
            continue
        if per_incident:
            if (p, num) in seen:
                continue
            seen.add((p, num))
        if d.year == 2026:
            cells[d.month] += len(res.get(num, ()))
    return [cells[m] for m in range(1, 13)]


def main(target):
    sol = calc.Solution(target)
    gold_a, _ = calc.gps_days(sol)
    gold_b = calc.zones(sol)
    rows = []
    paths = {
        "cracker": dict(a=dict(by_person=False), b=dict(addr_norm=False)),
        "mirror": dict(a=dict(by_person=False, custody=False, region=False), b=dict(residences=False, per_incident=False)),
    }
    out = {}
    for who, p in paths.items():
        a = gps(sol, **p["a"])
        b = zones(sol, **p["b"])
        hit_a = sum(1 for m in range(12) if a[m] == gold_a[m])
        hit_b = sum(1 for m in range(12) if b[m] == gold_b[m])
        out[who] = dict(a=a, b=b, hit_a=hit_a, hit_b=hit_b)
    n = 12 + 12
    lc = (out["cracker"]["hit_a"] + out["cracker"]["hit_b"]) / n
    ls = (out["mirror"]["hit_a"] + out["mirror"]["hit_b"]) / n
    crack = 38 + 7 + 55 * lc
    mirror = 5 + 7 + 55 * ls
    print("golden A", gold_a)
    print("golden B", gold_b)
    for who in ("cracker", "mirror"):
        o = out[who]
        print("%-8s A %s hits %d of 12" % (who, o["a"], o["hit_a"]))
        print("%-8s B %s hits %d of 12" % (who, o["b"], o["hit_b"]))
    print("cracker keeps %.1f%% of ask weight, mirror %.1f%%" % (100 * lc, 100 * ls))
    print("pair ceiling %.1f (cracker %.1f, mirror %.1f)" % ((crack + mirror) / 2, crack, mirror))
    print("mirror leakage %.1f%%" % (100 * ls))
    return out


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
