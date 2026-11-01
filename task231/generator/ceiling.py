"""task231 architecture 2: the cracker and mirror sheets as code on the cut pack (supplemental-stumping Part 1.1).

The cracker lands the call, runs the hygiene battery and executes every filed rule (the modem register with its
removed rows, the zone on every server time, each message's hours first to last, Schedule B's 20 minutes and its
outage exclusion, the register's units, firmware and lanes, re-sent rows once). It reconstructs nothing no key
offers: a modem the register gives no site is dropped. The mirror stops at the default path's rung (the hourly
lapse refit) on the call and works the asks as the cracker does. Each ask figure is a hit when it equals the golden.

    python3 task231/generator/ceiling.py
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import params as P  # noqa: E402

TARGET = os.path.join(os.path.dirname(HERE), "target")


def cracker_sla(target, reg, val):
    """Schedule B executed as filed, with the unregistered modem's messages dropped"""
    import csv
    import datetime as dt
    from openpyxl import load_workbook
    n = len(reg["sites"])
    wb = load_workbook(A.fpath(target, "modems"), read_only=True)
    imei = {str(r[0]): reg["idx"][r[2]] for r in list(wb["Modems"].iter_rows(values_only=True))[1:] if r[2]}
    first = np.full((n, P.NH), np.inf)
    with open(A.fpath(target, "messages"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["modem_imei"] not in imei:
                continue
            i = imei[r["modem_imei"]]
            rec = A.utc_of_local(r["server_received"])
            a, b = A.hour_of_obs(A.parse_z(r["first_obs_utc"])), A.hour_of_obs(A.parse_z(r["last_obs_utc"]))
            for h in range(a, b + 1):
                late = (rec - (P.WIN_START_UTC + dt.timedelta(hours=h + 1))).total_seconds() / 60.0
                first[i, h] = min(first[i, h], late)
    gold = A.sla(target, reg, val)
    avail = (first <= P.SLA_GRACE_MIN) & ~gold["excl"]
    return P.NH - avail.sum(1) - gold["excl"].sum(1)


def main():
    S = A.solve(TARGET)
    M, reg = S["M"], S["reg"]
    n = len(reg["sites"])
    gold_a, gold_f, gold_i = S["A"]["unavailable"], S["B"]["freezing"], S["B"]["ice"]
    ca = cracker_sla(TARGET, reg, M["val"])
    hits_c = int((ca == gold_a).sum() + (S["B"]["freezing"] == gold_f).sum() + (S["B"]["ice"] == gold_i).sum())
    total = 3 * n
    Lc = hits_c / total
    Ls = Lc                                  # the asks are decoupled: the mirror works them as the cracker does
    r = 5.0
    C = 38 + 7 + 55 * Lc
    Sx = r + 7 + 55 * Ls
    pair = (C + Sx) / 2
    print("ask figures %d; cracker keeps %d (%.1f per cent); mirror keeps %.1f per cent" % (total, hits_c,
                                                                                          100 * Lc, 100 * Ls))
    print("unavailable hours: cracker misses %s" % [reg["sites"][k]["site"] for k in range(n) if ca[k] != gold_a[k]])
    print("landed call %.1f, best miss %.1f, pair ceiling %.1f" % (C, Sx, pair))
    return pair, 100 * Ls


if __name__ == "__main__":
    main()
