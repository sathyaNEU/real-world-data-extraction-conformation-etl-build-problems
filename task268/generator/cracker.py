"""The cracker's path on the cut pack (supplemental-stumping 1.1): a response that lands the call, runs the hygiene
battery (exact duplicates, key uniqueness on the accession, the registry identifier and the record number, unmatched
record numbers through the crosswalk), parses the out-of-range results, reads the release and diagnosis dates and
executes the registry manual's definitions, then answers the two asks on what it finds. Each ask figure is scored
against figures.json; every one must miss. The mirror takes the asks the same way. Exit 0 when every figure misses.

    python3 cracker.py <target>"""
import csv
import json
import os
import sys
from collections import Counter

T = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
fig = json.load(open(os.path.join(HERE, "figures.json")))


def rows(name, delim=","):
    with open(os.path.join(T, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=delim))


lab, pat, xw = rows("ntprobnp_results_2025.csv"), rows("hf_registry_patients.csv"), rows("mrn_crosswalk_2024.csv")
code = {"FEN": "Fennick General Hospital", "LIN": "Linmoor Hospital", "BRE": "Brenmoor Regional Medical Center",
        "BRN": "Brenmoor Regional Medical Center", "GUL": "Gullhaven Hospital", "WRE": "Wrenhaven Medical Center"}

# the hygiene battery: nothing for it to find
battery = {
    "lab exact duplicates": len(lab) - len({tuple(r.values()) for r in lab}),
    "lab accession repeats": len(lab) - len({r["accession"] for r in lab}),
    "registry identifier repeats": len(pat) - len({r["registry_id"] for r in pat}),
    "registry record number repeats": len(pat) - len({r["mrn"] for r in pat}),
    "crosswalk legacy repeats": len(xw) - len({r["legacy_mrn"] for r in xw}),
    "crosswalk new repeats": len(xw) - len({r["new_mrn"] for r in xw}),
}
known = {r["legacy_mrn"] for r in xw} | {r["new_mrn"] for r in xw}
battery["registry numbers unknown to the crosswalk"] = sum(1 for r in pat if r["mrn"].startswith("H") and r["mrn"] not in
                                                           known)
print("battery:", battery)


def value(t):
    return 1e9 if t.startswith(">") else (-1.0 if t.startswith("<") else float(t))


a = Counter()
a_hi = Counter()
for r in lab:
    if r["released"][:4] == "2025":
        a[code[r["performing_lab"]]] += 1
        a_hi[code[r["performing_lab"]]] += value(r["result"]) >= 400
b = Counter()
b_ip = Counter()
for r in pat:
    if r["diagnosis_date"][:4] == "2025":
        b[code[r["hospital"]]] += 1
        b_ip[code[r["hospital"]]] += r["diagnosis_setting"] in ("Inpatient", "INPT", "IP")

# the stage 4 reader's path on Ask B (round 1): every record number through the crosswalk, a 2025 enrolment of a patient
# enrolled before left out, the year read from the diagnosis date as shown
leg = {r["legacy_mrn"]: r["new_mrn"] for r in xw}
by_new = {}
for r in pat:
    by_new.setdefault(leg.get(r["mrn"], r["mrn"]), []).append(r)
rb, rb_ip = Counter(), Counter()
for r in pat:
    if r["diagnosis_date"][:4] == "2025" and not any(q is not r and q["diagnosis_date"] < r["diagnosis_date"]
                                                       for q in by_new[r["mrn"]]):
        rb[code[r["hospital"]]] += 1
        rb_ip[code[r["hospital"]]] += r["diagnosis_setting"] in ("Inpatient", "INPT", "IP")
reader_hits = sum((rb[h], rb_ip[h]) == (g["new"], g["inpatient"]) for h, g in fig["ask_b"].items())
print("the round-1 reader's Ask B path: %d of %d hospitals right" % (reader_hits, len(fig["ask_b"])))
hits, total = 0, 0
for h, g in fig["ask_a"].items():
    for got, want in ((a[h], g["tests"]), (a_hi[h], g["referral"])):
        total += 1
        hits += got == want
        print("  Ask A %-34s %6d against %6d %s" % (h, got, want, "HIT" if got == want else "miss"))
for h, g in fig["ask_b"].items():
    for got, want in ((b[h], g["new"]), (b_ip[h], g["inpatient"])):
        total += 1
        hits += got == want
        print("  Ask B %-34s %6d against %6d %s" % (h, got, want, "HIT" if got == want else "miss"))
# the pair: the cracker lands the call (recommendation and critical components 38, instruction-following 7) and keeps
# none of the ask weight; the mirror stops at Kaplan-Meier (the recommendation's residue, about 5, and 7) with the
# asks taken the same way
ask_kept = 55.0 * hits / total
cracker, mirror = 38 + 7 + ask_kept, 5 + 7 + ask_kept
print("cracker hits %d of %d ask figures; pair ceiling %.1f (cracker %.1f, mirror %.1f); mirror leakage %.0f%%"
      % (hits, total, (cracker + mirror) / 2, cracker, mirror, 100.0 * hits / total))
sys.exit(1 if hits or reader_hits else 0)
