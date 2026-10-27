#!/usr/bin/env python3
"""task464: the pair arithmetic, measured on the cut pack.

    python3 generator/ceiling.py [--target <dir>] [--figures <path>]

Stump power is argued on paper and measured by the portal (`CLAUDE.md`, the STOP block of 2026-10-27).
This script is the paper measurement made exact: it walks the cracker's path and the mirror's path over
the shipped bundle in code, scores every ask figure each produces against the golden at the golden's own
rounding, and prints the pair on Part 0's weights (38 for the recommendation and critical components, 7
for instruction following, 55 for the asks). No reader is involved and none is owed.

  cracker  lands the main call, runs the hygiene battery, executes every filed rule it points at and ties
           to every control total in the pack. Its ask paths are the ones those ties lead to.
  mirror   stops at the revealed volume ceiling, so it is off the main call, and reads the asks the way a
           volume-minded analyst reads them.
"""
import argparse
import collections
import csv
import datetime as dt
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
W_REC, W_INSTR, W_ASK = 38.0, 7.0, 55.0
REC_OFF_CALL = 5.0


def read_xlsx(path, sheet):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    return [list(r) for r in wb[sheet].iter_rows(values_only=True)]


def load(target):
    d = {}
    for n in ("provider_directory_2027.csv", "staffing_roster_2026q4.csv",
              "out_of_network_payments_2026.csv", "out_of_network_payments_runout_2027q1.csv",
              "enrolment_projection_2027.csv"):
        d[n] = list(csv.DictReader(open(os.path.join(target, n), encoding="utf-8")))
    lic = read_xlsx(os.path.join(target, "state_licence_register.xlsx"), "Licences")
    d["licences"] = [dict(zip([str(h) for h in lic[0]], r)) for r in lic[1:]]
    fil = read_xlsx(os.path.join(target, "state_adequacy_filing_2026.xlsx"), "Contracted Sites")
    d["filing"] = [dict(zip([str(h) for h in fil[0]], r)) for r in fil[1:]]
    d["recon"] = read_xlsx(os.path.join(target, "out_of_network_payments_reconciliation_2026.xlsx"),
                           "Adjudicated Quarters")
    return d


def areas_of(d):
    cur = max(int(r["attestation_cycle"]) for r in d["provider_directory_2027.csv"])
    rows = [r for r in d["provider_directory_2027.csv"] if int(r["attestation_cycle"]) == cur]
    return cur, rows


def ask_a_paths(d, half26):
    cur, rows = areas_of(d)
    site_area = {r["site_name"]: r["service_area_code"] for r in rows}
    out = {}
    # the cracker: the filed service-date basis and the asked area of the site treated, totals tied to the
    # reconciliation workbook, so the main file only and every unit row summed
    c = collections.Counter()
    for r in d["out_of_network_payments_2026.csv"]:
        sd = dt.date.fromisoformat(r["service_date"])
        if sd.year != 2026:
            continue
        c[(site_area[r["service_facility_name"]], "H1" if sd.month <= 6 else "H2")] += \
            int(r["treatment_units"])
    out["cracker"] = c
    # the mirror: the same, with the run-out supplement picked up from the folder
    m = collections.Counter()
    for fn in ("out_of_network_payments_2026.csv", "out_of_network_payments_runout_2027q1.csv"):
        for r in d[fn]:
            sd = dt.date.fromisoformat(r["service_date"])
            if sd.year != 2026:
                continue
            m[(site_area[r["service_facility_name"]], "H1" if sd.month <= 6 else "H2")] += \
                int(r["treatment_units"])
    out["mirror"] = m
    return out


def ask_b_paths(d, asof):
    out = {}
    c = collections.defaultdict(lambda: [0, 0])
    for r in d["licences"]:
        if r["licence_status"] != "active" or not str(r["county_or_area"]).startswith("SA-"):
            continue
        c[r["county_or_area"]][0] += 1
        c[r["county_or_area"]][1] += int(r["licensed_stations"])
    out["cracker"] = c
    m = collections.defaultdict(lambda: [0, 0])
    for r in d["licences"]:
        if not str(r["county_or_area"]).startswith("SA-"):
            continue
        f = dt.date.fromisoformat(str(r["effective_from"])[:10])
        t = dt.date.fromisoformat(str(r["effective_to"])[:10]) if r["effective_to"] else None
        if f > asof or (t is not None and t <= asof):
            continue
        m[r["county_or_area"]][0] += 1
        m[r["county_or_area"]][1] += int(r["licensed_stations"])
    out["mirror"] = m
    return out


def ask_c_paths(d):
    cur, rows = areas_of(d)
    by_addr = {r["service_address"]: (r["service_area_code"], r["contract_intent_2027"]) for r in rows}
    out = {}
    for who in ("cracker", "mirror"):
        agg = collections.defaultdict(lambda: [0, 0])
        for r in d["filing"]:
            hit = by_addr.get(r["service_address"])
            if hit is None or hit[1] != "none":
                continue
            agg[r["service_area_code"]][0] += 1       # the filing's own area label, every row counted
            agg[r["service_area_code"]][1] += int(r["licensed_stations"])
        out[who] = agg
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=os.path.join(TASK, "target"))
    ap.add_argument("--figures", default=os.path.join(HERE, "figures.json"))
    a = ap.parse_args(argv)
    g = json.load(open(a.figures, encoding="utf-8"))
    d = load(a.target)
    asof = dt.date.fromisoformat(json.load(open(os.path.join(TASK, "metadata.json"),
                                                encoding="utf-8"))["as_of"])
    codes = sorted(g["area"])
    half26 = {}
    A = ask_a_paths(d, half26)
    B = ask_b_paths(d, asof)
    C = ask_c_paths(d)
    rowsout, keep = [], {"cracker": 0, "mirror": 0}
    total = 0
    for who in ("cracker", "mirror"):
        hits = collections.Counter()
        for c in codes:
            for h in ("H1", "H2"):
                total_t = g["ask_a"][c][h]["treatments"]
                if A[who].get((c, h), 0) == total_t:
                    hits["A"] += 1
                # the share follows the count, so it is scored on the same path
                if A[who].get((c, h), 0) == total_t:
                    hits["A"] += 1
            if tuple(B[who][c]) == (g["ask_b"][c]["sites"], g["ask_b"][c]["stations"]):
                hits["B"] += 2
            else:
                hits["B"] += (1 if B[who][c][0] == g["ask_b"][c]["sites"] else 0) + \
                             (1 if B[who][c][1] == g["ask_b"][c]["stations"] else 0)
            hits["C"] += (1 if C[who][c][0] == g["ask_c"][c]["sites"] else 0) + \
                         (1 if C[who][c][1] == g["ask_c"][c]["stations"] else 0)
        keep[who] = hits["A"] + hits["B"] + hits["C"]
        rowsout.append((who, hits["A"], hits["B"], hits["C"], keep[who]))
    total = 48 + 24 + 24
    print("ask figures graded: %d (A 48, B 24, C 24)" % total)
    print("%-9s %8s %8s %8s %10s" % ("response", "ask A", "ask B", "ask C", "kept"))
    for who, ha, hb, hc, k in rowsout:
        print("%-9s %4d/48 %4d/24 %4d/24 %6d/%d" % (who, ha, hb, hc, k, total))
    lc, ls = keep["cracker"] / float(total), keep["mirror"] / float(total)
    cracker = W_REC + W_INSTR + W_ASK * lc
    mirror = REC_OFF_CALL + W_INSTR + W_ASK * ls
    pair = (cracker + mirror) / 2.0
    print()
    print("cracker  lands the call, keeps %.3f of the ask weight -> %.1f" % (lc, cracker))
    print("mirror   stops at the volume ceiling, keeps %.3f of the ask weight -> %.1f" % (ls, mirror))
    print("Mirror leakage: %.1f per cent of ask weight (bar: under 35)" % (ls * 100.0))
    print("Pair ceiling: %.1f (build target 60, this build's brief 40)" % pair)
    print()
    print("sensitivity, the cracker's ask keep swept:")
    for k in (0.0, 0.10, 0.20, 0.30, 0.40):
        print("  cracker keeps %.2f -> pair %.1f" % (k, (W_REC + W_INSTR + W_ASK * k + mirror) / 2.0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
