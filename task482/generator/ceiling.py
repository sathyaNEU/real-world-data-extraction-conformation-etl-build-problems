"""Pair ceiling for task482 on the cut pack (supplemental-stumping Part 0, weights 38, 7 and 55).

The cracker lands the call, runs the hygiene battery and executes every filed rule; on ask A it joins each claim's
lines to the remittance register and counts the 0656 and 0655 units of every version with a net remitted payment (the
path stage 4's reader A took, which kept all 24 figures before the review device was sited). The mirror stops at the
default path on the call and takes the latest version of each claim chain (reader B's path). Each graded ask figure is
scored against generator/figures.json, a hit within half a unit of its stated rounding.

    python3 task482/generator/ceiling.py
"""
import collections
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
REC, INSTR, ASKS, R_MISS = 38.0, 7.0, 55.0, 5.0
PROGS = ("BRK", "COR", "DUN", "LIN", "PEN", "SAL", "WEX", "FAL")


def latest_versions():
    rows = list(csv.DictReader(open(os.path.join(TARGET, "wendleglen_claim_lines_fy2026.csv"))))
    head = {}
    for r in rows:
        head.setdefault(r["claim_key"], r)
    root = {}
    for k, r in head.items():
        root[k] = r["prior_claim_key"] or k
    latest = {}
    for k, r in head.items():
        ch = root[k]
        if ch not in latest or (r["submitted_on"], k) > (head[latest[ch]]["submitted_on"], latest[ch]):
            latest[ch] = k
    keep = {k for k in latest.values() if head[k]["type_of_bill"] != "0818"}
    gip, irc = collections.Counter(), collections.Counter()
    for r in rows:
        if r["claim_key"] in keep:
            if r["revenue_code"] == "0656":
                gip[r["provider_number"]] += int(r["units"])
            elif r["revenue_code"] == "0655":
                irc[r["provider_number"]] += int(r["units"])
    return gip, irc


def remitted_join():
    """Units at 0656 and 0655 on every claim key whose CLP rows net to a positive payment."""
    rows = list(csv.DictReader(open(os.path.join(TARGET, "wendleglen_claim_lines_fy2026.csv"))))
    net = collections.defaultdict(float)
    for r in csv.DictReader(open(os.path.join(TARGET, "remittance_register_fy2026.csv"))):
        if r["record_type"] == "CLP":
            net[r["patient_control_no"]] += float(r["paid_amount"]) + float(r["adj_carc_253"])
    gip, irc = collections.Counter(), collections.Counter()
    for r in rows:
        if net.get(r["claim_key"], 0.0) > 0.005:
            if r["revenue_code"] == "0656":
                gip[r["provider_number"]] += int(r["units"])
            elif r["revenue_code"] == "0655":
                irc[r["provider_number"]] += int(r["units"])
    return gip, irc


def days_of_care(ccns):
    import datetime as dt
    fy0, fy1 = dt.date(2025, 10, 1), dt.date(2026, 10, 1)
    out = collections.Counter()
    with open(os.path.join(TARGET, "medicare_hospice_benefit_periods_20270105.txt")) as f:
        for line in f:
            if line[0] != "D" or line[23:29] not in ccns:
                continue
            s = dt.date(int(line[29:33]), int(line[33:35]), int(line[35:37]))
            n = int(line[45:49])
            a, z = max(s, fy0), min(s + dt.timedelta(days=n), fy1)
            out[line[23:29]] += max(0, (z - a).days)
    return out


def score_ask(figs, gip, irc, days):
    kept = 0
    lines = []
    for p in PROGS:
        ccn = figs["provider_numbers"][p]
        want = figs["ask_a"][p]
        share = 100.0 * (gip[ccn] + irc[ccn]) / days[ccn]
        hits = [gip[ccn] == want["gip_days"], irc[ccn] == want["respite_days"], abs(share - want["share_pct"]) < 0.05]
        kept += sum(hits)
        lines.append("  %s general inpatient %d (%d) respite %d (%d) share %.2f (%.1f): %d of 3" % (
            p, gip[ccn], want["gip_days"], irc[ccn], want["respite_days"], share, want["share_pct"], sum(hits)))
    return kept, lines


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    days = days_of_care(set(figs["provider_numbers"].values()))
    total = 24
    gip, irc = remitted_join()
    kept_c, lines_c = score_ask(figs, gip, irc, days)
    gip, irc = latest_versions()
    kept_m, lines_m = score_ask(figs, gip, irc, days)
    print("ask A, the cracker's path (each claim's lines joined to the remittance register, net remitted payment):")
    print("\n".join(lines_c))
    print("ask A, the mirror's path (the latest version of each claim chain):")
    print("\n".join(lines_m))
    cracker = REC + INSTR + ASKS * kept_c / total
    mirror = R_MISS + INSTR + ASKS * kept_m / total
    print("cracker (lands the call)  ask A %d of %d  score %.1f" % (kept_c, total, cracker))
    print("mirror (default path)     ask A %d of %d  score %.1f" % (kept_m, total, mirror))
    print("Pair ceiling: %.1f" % ((cracker + mirror) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * kept_m / total))
    for k in (0, 6, 12, 18, 24):
        print("  both responses keeping %2d of 24: pair %.1f" % (k, (REC + INSTR + R_MISS + INSTR + 2 * ASKS * k / total) / 2))
    print("The asks consume nothing the call's construction produces (checks.py X1 to X3, AD1), and the two rows score "
          "two different readings of the claims.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
