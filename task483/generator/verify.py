"""task483 independent verifier: recomputes every graded figure from target/ with its own reading of the files (no
code shared with analysis.py or golden.py) and compares it with generator/figures.json and the golden workbook."""
import csv
import datetime
import json
import os
import sys

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))


def day(s):
    s = s.strip()
    if s[2:3] == "/":
        return datetime.date(int(s[6:10]), int(s[3:5]), int(s[0:2]))
    return datetime.date.fromisoformat(s[:10])


def main(target, gdir):
    reg = openpyxl.load_workbook(os.path.join(target, "member_practice_register_2026.xlsx"), read_only=True)
    pcn, succ, hubs, order = {}, {}, set(), []
    for row in reg["Member practices"].iter_rows(min_row=4, values_only=True):
        if not row or not row[0]:
            continue
        if row[3] == "Federation-wide":
            hubs.add(row[0])
            continue
        pcn[row[0]] = row[3]
        if row[3] not in order:
            order.append(row[3])
        if row[6] and "Merged into" in row[6]:
            succ[row[0]] = row[6].split("Merged into ")[1].split()[0]
    cl = openpyxl.load_workbook(os.path.join(target, "uti_pathway_code_lists_2027-28.xlsx"), read_only=True)
    short = {"Nitrofurantoin": "N", "Trimethoprim": "T", "Pivmecillinam": "P", "Cefalexin": "C", "Co-amoxiclav": "A",
             "Fosfomycin": "F", "Amoxicillin": "X"}
    med = {r[0]: short[r[1]] for r in cl["Pathway antibacterials"].iter_rows(min_row=2, values_only=True) if r[0]}
    lower = {r[0] for r in cl["Lower UTI problems"].iter_rows(min_row=2, values_only=True) if r[1] == "Yes"}
    col = {"N": "NITR", "T": "TRIM", "P": "MECI", "C": "CEPH", "A": "COAM", "F": "FOSF", "X": "AMOX"}

    hist = {}
    with open(os.path.join(target, "gp_uti_antibacterial_issues_2024-2026.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            if r["MedicationName"] in med and r["LinkedProblem"] in lower:
                hist.setdefault(r["PatientPseudonym"], []).append(r)
    first = []
    for pid, rs in hist.items():
        rs.sort(key=lambda r: r["IssueDate"])
        dates = [day(r["IssueDate"]) for r in rs]
        for k, r in enumerate(rs):
            if r["IssueType"] != "Acute" or r["Sex"] != "F" or not 16 <= int(r["AgeAtIssue"]) <= 64:
                continue
            if any(1 <= (dates[k] - dd).days <= 28 for dd in dates[:k]):
                continue
            prac = succ.get(r["RegisteredPracticeCode"], r["RegisteredPracticeCode"])
            first.append((pid, dates[k], med[r["MedicationName"]], pcn[prac]))

    spec = {}
    with open(os.path.join(target, "urine_culture_results_2024-2026.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            s = spec.setdefault(r["LabNo"], {"pid": r["NHSNumberPseudo"], "sex": r["Sex"], "age": int(r["AgeYears"]),
                                             "c": day(r["DateCollected"]), "gp": r["GPPracticeCode"],
                                             "req": r["RequestingLocation"], "R": set(), "orgs": []})
            for k, c in col.items():
                if r[c] == "R":
                    s["R"].add(k)
            if r["OrganismCode"]:
                s["orgs"].append(r["OrganismCode"])
    by_pid = {}
    for lab, s in spec.items():
        if s["sex"] == "F" and 16 <= s["age"] <= 64:
            by_pid.setdefault(s["pid"], []).append((s["c"], lab))
    used = []
    for pid, d0, drug, net in first:
        hits = sorted((c, lab) for c, lab in by_pid.get(pid, []) if c == d0)
        if hits:
            used.append(hits[0][1])
    nres = {k: sum(k in spec[lab]["R"] for lab in used) for k in col}
    p = {k: nres[k] / len(used) for k in col}
    pool = {}
    for pid, d0, drug, net in first:
        if d0.year == 2026:
            pool[(net, drug)] = pool.get((net, drug), 0) + 1
    stop = {net: sum(pool.get((net, k), 0) * (p[k] - p["N"]) for k in col if k != "N") for net in order}
    ranked = sorted(stop, key=lambda k: -stop[k])

    comm = set(pcn) | set(succ) | hubs
    old = {"ENTE": "Enterococcus", "ENTC": "Enterobacter"}
    new = {"ENTC": "Enterococcus", "ECLO": "Enterobacter"}
    grid = {}
    for lab, s in spec.items():
        if s["c"].year != 2026 or s["req"] not in comm:
            continue
        if not ((s["sex"] == "F" and s["age"] >= 65) or (s["sex"] == "M" and s["age"] >= 16)):
            continue
        net = pcn[succ.get(s["gp"], s["gp"])]
        table = old if lab.startswith("H") else new
        for o in s["orgs"]:
            if o in table:
                grid.setdefault((net, table[o]), set()).add(s["pid"])

    F = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []
    if F["slate"] != ranked[:2] or F["runner_up"] != ranked[2]:
        bad.append("slate %s against %s" % (F["slate"], ranked[:3]))
    if F["presentation_cultures"] != len(used):
        bad.append("cultures %d against %d" % (F["presentation_cultures"], len(used)))
    m = {"N": "NIT", "T": "TMP", "P": "MEC", "C": "CEX", "A": "AMC", "F": "FOS", "X": "AMX"}
    for k, d in m.items():
        if F["chances"][d]["resistant"] != nres[k]:
            bad.append("resistant %s" % d)
    for r in F["networks"]:
        net = r["network"]
        if r["other"] != sum(pool.get((net, k), 0) for k in col if k != "N"):
            bad.append("pool %s" % net)
        if abs(r["stopped"] - stop[net]) > 0.0011:
            bad.append("stopped %s %.4f against %.4f" % (net, r["stopped"], stop[net]))
        for grp in ("Enterococcus", "Enterobacter"):
            if F["grid"][net][grp] != len(grid.get((net, grp), ())):
                bad.append("grid %s %s" % (net, grp))
    wb = openpyxl.load_workbook(os.path.join(gdir, "uti_pathway_placement_2027-28.xlsx"), read_only=True)
    shown = {row[0]: row for row in wb["Placement"].iter_rows(min_row=5, values_only=True) if row and row[0] in stop}
    for r in F["networks"]:
        if shown[r["network"]][3] != r["other"] or shown[r["network"]][10] != r["stopped_r10"]:
            bad.append("workbook %s" % r["network"])
    if bad:
        print("verify: FAIL", bad[:12])
        sys.exit(1)
    print("verify: every graded figure recomputes independently (%d first courses, %d cultures, slate %s, runner-up %s)"
          % (len(first), len(used), ranked[:2], ranked[2]))


if __name__ == "__main__":
    t = os.path.join(os.path.dirname(HERE), "target")
    main(t, os.path.join(os.path.dirname(HERE), "golden"))
