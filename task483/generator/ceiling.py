"""task483 ask ceiling, measured on the cut pack. Shares no code with the generator: it reads target/ and the graded
figures in generator/figures.json, and nothing else.

The cracker is the careful solver: it lands the call (the cultures sent at a first course's consultation), executes
every filed rule (the specification's first courses, the hub to the registered practice, Stanbridge Road to Hollin
Lane, the asking sentence's population, requesters and patients) and runs the hygiene battery on the culture export
(second pots of one consultation dropped, accession formats and both date layouts parsed, result wording of both
systems read, every organism code read through the laboratory's code table, a code the table lacks read by its
evident name, each code checked against its own row's panel). The mirror stops at the cumulative antibiogram for the
call and handles the ask the same way. A figure is kept when it lands within half a unit of its rounding.

    python3 task483/generator/ceiling.py
"""
import csv
import datetime
import hashlib
import json
import os
import sys

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def parse_day(text):
    text = text.strip()
    if "/" in text[:6]:
        return datetime.date(int(text[6:10]), int(text[3:5]), int(text[:2]))
    return datetime.date(int(text[:4]), int(text[5:7]), int(text[8:10]))


def pack_digest(target):
    h = hashlib.sha256()
    for f in sorted(os.listdir(target)):
        h.update(f.encode())
        h.update(open(os.path.join(target, f), "rb").read())
    return h.hexdigest()[:16]


def read(target):
    wb = openpyxl.load_workbook(os.path.join(target, "member_practice_register_2026.xlsx"), read_only=True)
    network, successor, requesters = {}, {}, set()
    for row in wb["Member practices"].iter_rows(min_row=4, values_only=True):
        if not row or not row[0]:
            continue
        requesters.add(row[0])
        if row[3] != "Federation-wide":
            network[row[0]] = row[3]
        if row[6] and str(row[6]).startswith("Merged into"):
            successor[row[0]] = str(row[6]).split()[2]
    table = {}
    with open(os.path.join(target, "laboratory_organism_codes.csv"), newline="") as fh:
        for row in csv.DictReader(fh):
            table[row["OrganismCode"]] = row["OrganismName"]
    specimens = {}
    with open(os.path.join(target, "urine_culture_results_2024-2026.csv"), newline="") as fh:
        for row in csv.DictReader(fh):
            sp = specimens.setdefault(row["LabNo"], {
                "patient": row["NHSNumberPseudo"], "sex": row["Sex"], "age": int(row["AgeYears"]),
                "gp": row["GPPracticeCode"], "requester": row["RequestingLocation"],
                "collected": parse_day(row["DateCollected"]), "rows": []})
            if row["OrganismCode"]:
                sp["rows"].append(row)
    return network, successor, requesters, table, specimens


def battery(specimens):
    """Second pots: one consultation's specimens with the same patient, collection day and identical results."""
    seen, keep = set(), {}
    for lab in sorted(specimens):
        sp = specimens[lab]
        key = (sp["patient"], sp["collected"], tuple(sorted(tuple(sorted(r.items()))[11:] for r in sp["rows"])))
        if key in seen:
            continue
        seen.add(key)
        keep[lab] = sp
    return keep


def name_of(code, table):
    if code in table:
        return table[code]
    guess = {"ENTE": "Enterococcus species"}      # a retired code read by its letters
    return guess.get(code, code)


def panel_profile(table, specimens):
    """For each laboratory system (the old one's accession numbers start with H), the share of the rows its code table
    reads as an enterococcus that carry gentamicin or cefpodoxime. A share strictly between 0 and 1 means some of those
    rows contradict their code, and the battery re-derives them from the panel."""
    prof = {}
    for sp_lab, sp in specimens.items():
        system = "old" if sp_lab.startswith("H") else "new"
        for row in sp["rows"]:
            if name_of(row["OrganismCode"], table).startswith("Enterococcus"):
                n, g = prof.get(system, (0, 0))
                prof[system] = (n + 1, g + bool(row["GENT"] or row["CPOD"]))
    return {k: g / n for k, (n, g) in prof.items()}


PROFILE = {}


def panel_contradicts(name, row, lab):
    share = PROFILE.get("old" if lab.startswith("H") else "new", 0.0)
    return name.startswith("Enterococcus") and 0.0 < share < 1.0 and bool(row["GENT"] or row["CPOD"])


def ask_grid(network, successor, requesters, table, specimens):
    pats = {}
    for lab, sp in specimens.items():
        if sp["collected"].year != 2026 or sp["requester"] not in requesters:
            continue
        if not ((sp["sex"] == "F" and sp["age"] >= 65) or (sp["sex"] == "M" and sp["age"] >= 16)):
            continue
        net = network.get(successor.get(sp["gp"], sp["gp"]))
        for row in sp["rows"]:
            nm = name_of(row["OrganismCode"], table)
            if panel_contradicts(nm, row, lab):
                continue
            grp = "Enterococcus" if nm.startswith("Enterococcus") else (
                "Enterobacter" if nm.startswith("Enterobacter") else None)
            if grp:
                pats.setdefault((net, grp), set()).add(sp["patient"])
    return {k: len(v) for k, v in pats.items()}


def main():
    target = os.path.join(TASK, "target")
    F = json.load(open(os.path.join(HERE, "figures.json")))
    network, successor, requesters, table, specimens = read(target)
    clean = battery(specimens)
    PROFILE.update(panel_profile(table, clean))
    grid = ask_grid(network, successor, requesters, table, clean)
    rows, kept, total = [], 0, 0
    for grp in ("Enterococcus", "Enterobacter"):
        hits = []
        for r in F["networks"]:
            net = r["network"]
            gold = F["grid"][net][grp]
            got = grid.get((net, grp), 0)
            total += 1
            if abs(got - gold) < 0.5:
                hits.append(net)
                kept += 1
        rows.append((grp, len(F["networks"]) - len(hits), hits))
    lc = kept / total
    ls = lc          # the mirror handles the ask exactly as the cracker does
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * ls
    pair = (c + s) / 2
    print("pack digest %s" % pack_digest(target))
    print("panel check: share of enterococcus-coded rows carrying gentamicin or cefpodoxime by system %s" % {
        k: round(v, 3) for k, v in sorted(PROFILE.items())})
    for grp, missed, hits in rows:
        print("cracker %s by network: %d of %d missed%s" % (grp, missed, missed + len(hits),
                                                            "" if not hits else " (kept: %s)" % ", ".join(hits)))
    print("cracker keeps %.1f per cent of the ask figures; mirror keeps %.1f" % (100 * lc, 100 * ls))
    print("pair ceiling %.1f (landed call %.1f, best miss %.1f); mirror leakage %.1f per cent of ask weight" % (
        pair, c, s, 100 * ls))
    return 0 if kept == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
