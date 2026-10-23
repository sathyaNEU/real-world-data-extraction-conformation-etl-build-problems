"""The pair ceiling, run on the cut pack: the cracker lands the call and works every ask the way a careful solver
executing every filed sentence would; the mirror stops at the first-year analog on the call and works the asks the
same way (the asks read nothing the call's construction produces, so its ask rows equal the cracker's by
construction; calc.connections_fy26 and calc.fees_fy26 never read the call's rows). Weights 38, 7, 55
(supplemental-stumping Part 0); every ask figure is one criterion, a hit only when exact at the stated rounding.

    python3 ceiling.py <target>"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc                 # noqa: E402

PHASES = ["Core", "1", "2", "3", "4"]


def main(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    P = calc.Pack(target)
    grid, naive, stored = calc.connections_fy26(target, P)
    fees, lines = calc.fees_fy26(target)
    golden_ask, cracker_ask, cracker2_ask = [], [], []
    for ph in PHASES:
        for q in (1, 2, 3, 4):
            golden_ask.append(grid[(ph, q)])
            cracker_ask.append(naive[(ph, q)])        # every install counted, phase from the schedule
    # the stored-phase reader: installs counted, phase from the premise's UEP_PHASE
    import csv
    prem = {r["PREMISE_ID"]: r["UEP_PHASE"] for r in csv.DictReader(open(os.path.join(target, calc.C.F_PREM)))}
    from collections import defaultdict
    st = defaultdict(int)
    for r in csv.DictReader(open(os.path.join(target, calc.C.F_AMI))):
        d = calc._iso(r["INSTALL_DATE"]); fy, q = calc.C.fq(d)
        if fy == 2026:
            ph = "Core" if prem[r["PREMISE_ID"]] == "00" else str(int(prem[r["PREMISE_ID"]]))
            st[(ph, q)] += 1
    for ph in PHASES:
        for q in (1, 2, 3, 4):
            cracker2_ask.append(st[(ph, q)])
    for q in (1, 2, 3, 4):
        golden_ask.append(round(fees[q])); cracker_ask.append(round(lines[q])); cracker2_ask.append(round(lines[q]))
    # chart: one criterion per labelled segment (20) folds into the connection cells; scored once as the cells
    n = len(golden_ask)
    keep1 = sum(1 for a, b in zip(golden_ask, cracker_ask) if a == b)
    keep2 = sum(1 for a, b in zip(golden_ask, cracker2_ask) if a == b)
    keep = max(keep1, keep2)
    Lc = keep / n
    Ls = keep / n
    r_wrong = 5.0
    C_score = 38 + 7 + 55 * Lc
    S_score = r_wrong + 7 + 55 * Ls
    pair = (C_score + S_score) / 2
    mirror_leak = 100.0 * Ls
    print("ask figures %d; cracker keeps %d (installs counted, schedule phases), %d (installs counted, stored phases)"
          % (n, keep1, keep2))
    for k, (a, b, c) in enumerate(zip(golden_ask, cracker_ask, cracker2_ask)):
        print("   figure %2d golden %10s cracker %10s stored-phase %10s %s" % (k + 1, a, b, c, "miss" if (a != b and a != c) else "HIT"))
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f per cent of ask weight" % (C_score, S_score, pair, mirror_leak))
    print("separation: the asks read %s, %s, %s and %s, which the call never reads, and the roll only to place a premise "
          "in its plat unit; no device row sits in the roll or the permit files" % (calc.C.F_AMI, calc.C.F_ACCT, calc.C.F_PREM, calc.C.F_FEES))
    return pair, mirror_leak


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
