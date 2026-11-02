"""task483 golden analysis, read only from the shipped files under target/.

The specification's courses and placement executed word for word, with each antibacterial's chance estimated on the
urine cultures sent at a first course's consultation (the day before, the day of or the day after its issue): the
cultures a first course's infection gives the laboratory before any course can have failed. The variants the checks
assert sit beside it (other windows, de-duplication, pregnancy, the hub, per isolate, inverse weighting by failure,
and the laboratory-wide constructions of the default path).
"""
import csv
import datetime as dt
import os
from collections import defaultdict

import openpyxl

DRUGS = ("NIT", "TMP", "MEC", "CEX", "AMC", "FOS", "AMX")
OFF = ("TMP", "MEC", "CEX", "AMC", "FOS", "AMX")
NAME2DRUG = {"Nitrofurantoin": "NIT", "Trimethoprim": "TMP", "Pivmecillinam": "MEC", "Cefalexin": "CEX",
             "Co-amoxiclav": "AMC", "Fosfomycin": "FOS", "Amoxicillin": "AMX"}
LABCOL = {"AMX": "AMOX", "AMC": "COAM", "CEX": "CEPH", "FOS": "FOSF", "MEC": "MECI", "NIT": "NITR", "TMP": "TRIM"}
DRUG_LABEL = {"NIT": "Nitrofurantoin", "TMP": "Trimethoprim", "MEC": "Pivmecillinam", "CEX": "Cefalexin",
              "AMC": "Co-amoxiclav", "FOS": "Fosfomycin", "AMX": "Amoxicillin"}
GO_LIVE = dt.date(2026, 9, 7)


def _date(s):
    s = s.strip()
    if "/" in s:
        d, m, y = s[:10].split("/")
        return dt.date(int(y), int(m), int(d))
    return dt.date(int(s[:4]), int(s[5:7]), int(s[8:10]))


def load(target):
    p = lambda n: os.path.join(target, n)
    wb = openpyxl.load_workbook(p("member_practice_register_2026.xlsx"), read_only=True)
    net, order, hub = {}, [], None
    for r in wb["Member practices"].iter_rows(min_row=4, values_only=True):
        if not r or not r[0]:
            continue
        code, name, pcn, network, system, n, status = r[:7]
        if network == "Federation-wide":
            hub = code
            continue
        net[code] = network
        if network not in order:
            order.append(network)
    merged = {}
    for r in wb["Member practices"].iter_rows(min_row=4, values_only=True):
        if r and r[6] and str(r[6]).startswith("Merged into "):
            merged[r[0]] = str(r[6]).split()[2]
    wb = openpyxl.load_workbook(p("uti_pathway_code_lists_2027-28.xlsx"), read_only=True)
    prod = {r[0]: NAME2DRUG[r[1]] for r in wb["Pathway antibacterials"].iter_rows(min_row=2, values_only=True) if r[0]}
    lower = {r[0] for r in wb["Lower UTI problems"].iter_rows(min_row=2, values_only=True) if r[0] and r[1] == "Yes"}
    with open(p("gp_uti_antibacterial_issues_2024-2026.csv"), newline="", encoding="utf-8") as fh:
        issues = list(csv.DictReader(fh))
    with open(p("urine_culture_results_2024-2026.csv"), newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    specs = {}
    for r in rows:
        s = specs.get(r["LabNo"])
        if s is None:
            s = specs[r["LabNo"]] = {"lab": r["LabNo"], "pid": r["NHSNumberPseudo"], "sex": r["Sex"],
                                     "age": int(r["AgeYears"]), "gp": r["GPPracticeCode"],
                                     "req": r["RequestingLocation"], "type": r["SpecimenType"],
                                     "collected": _date(r["DateCollected"]), "received": _date(r["DateTimeReceived"]),
                                     "result": r["CultureResult"], "orgs": []}
        if r["OrganismCode"]:
            s["orgs"].append((r["OrganismCode"], {d: r[LABCOL[d]] for d in DRUGS}))
    return {"net": net, "order": order, "hub": hub, "merged": merged, "prod": prod, "lower": lower,
            "issues": issues, "specs": list(specs.values())}


def network_of(L, code):
    code = L["merged"].get(code, code)
    return L["net"].get(code)


def pathway_issues(L):
    """Issues of a pathway antibacterial linked to a lower UTI problem, by patient, in date order."""
    out = defaultdict(list)
    for i in L["issues"]:
        d = L["prod"].get(i["MedicationName"])
        if d is None or i["LinkedProblem"] not in L["lower"]:
            continue
        out[i["PatientPseudonym"]].append((_date(i["IssueDate"]), d, i))
    for v in out.values():
        v.sort(key=lambda t: t[0])
    return out


def first_courses(L, lookback=28, include_repeat=False):
    """2.1: acute issue, pathway antibacterial, lower UTI problem, woman aged 16 to 64 at issue, none in the 28 days
    before (any issue of a pathway antibacterial linked to a lower UTI problem)."""
    by = pathway_issues(L)
    fc = []
    for pid, lst in by.items():
        for k, (day, d, i) in enumerate(lst):
            if i["IssueType"] != "Acute" and not include_repeat:
                continue
            if i["Sex"] != "F" or not (16 <= int(i["AgeAtIssue"]) <= 64):
                continue
            if any(0 < (day - day0).days <= lookback for day0, _, _ in lst[:k]):
                continue
            fc.append({"pid": pid, "day": day, "drug": d, "net": network_of(L, i["RegisteredPracticeCode"]),
                       "issuer": i["IssuingOrganisationCode"]})
    return fc


def pool(fc, year=2026):
    n = defaultdict(int)
    for c in fc:
        if c["day"].year == year:
            n[(c["net"], c["drug"])] += 1
    return n


def resistant(s, d):
    return any(res.get(d) == "R" for _, res in s["orgs"])


def presentation(L, fc, lo=-1, hi=1, dedup_year=False, pregnant=False, hub=True):
    """The cultures sent at a first course's consultation: collected from the day `lo` to the day `hi` around the
    course's issue (one specimen per course, the first registered)."""
    by_pid = defaultdict(list)
    for c in fc:
        by_pid[c["pid"]].append(c)
    specs = defaultdict(list)
    for s in L["specs"]:
        if s["sex"] == "F" and 16 <= s["age"] <= 64:
            specs[s["pid"]].append(s)
    chosen = []
    for pid, cs in by_pid.items():
        for c in cs:
            if not hub and c["issuer"] == L["hub"]:
                continue
            cand = [s for s in specs.get(pid, []) if lo <= (s["collected"] - c["day"]).days <= hi]
            if cand:
                chosen.append(sorted(cand, key=lambda s: (s["collected"], s["lab"]))[0])
    if pregnant:
        preg = pregnant_cultures(L, lo, hi)
        chosen = chosen + preg
    if dedup_year:
        seen, keep = set(), []
        for s in sorted(chosen, key=lambda s: (s["collected"], s["lab"])):
            k = (s["pid"], s["collected"].year)
            if k in seen:
                continue
            seen.add(k)
            keep.append(s)
        chosen = keep
    return chosen


def pregnant_cultures(L, lo=-1, hi=1):
    out = []
    preg = defaultdict(list)
    for i in L["issues"]:
        if i["LinkedProblem"] == "Urinary tract infection in pregnancy" and i["IssueType"] == "Acute":
            preg[i["PatientPseudonym"]].append(_date(i["IssueDate"]))
    for s in L["specs"]:
        if s["sex"] == "F" and 16 <= s["age"] <= 64 and s["pid"] in preg and s["req"] in L["net"] or (
                s["pid"] in preg and s["req"] == L["hub"]):
            if any(lo <= (s["collected"] - d).days <= hi for d in preg[s["pid"]]):
                out.append(s)
    return out


def chances(specs, per_isolate=False):
    if per_isolate:
        rows = [res for s in specs for _, res in s["orgs"]]
        return {d: sum(r.get(d) == "R" for r in rows) / max(1, sum(r.get(d) in ("R", "S", "I") for r in rows))
                for d in DRUGS}
    n = len(specs)
    return {d: sum(resistant(s, d) for s in specs) / n for d in DRUGS}


def stopped(n, ch, order, floor=False):
    out = {}
    for net in order:
        v = 0.0
        for d in OFF:
            g = ch[d] - ch["NIT"]
            if floor:
                g = max(0.0, g)
            v += n[(net, d)] * g
        out[net] = v
    return out


def slate(st):
    rk = sorted(st, key=lambda k: (-st[k], k))
    return rk[:2], rk


def antibiogram(L, ages=(16, 64), sexes=("F",), first_isolate=True, ecoli_only=False, practices_only=True):
    """The laboratory's cumulative antibiogram (CLSI M39 style): community requests, first isolate per patient and
    organism a calendar year, each drug's resistant share of the isolates tested."""
    lab = sorted(L["specs"], key=lambda s: (s["collected"], s["lab"]))
    seen = set()
    iso = []
    community = set(L["net"]) | set(L["merged"]) | {L["hub"]}
    for s in lab:
        if s["sex"] not in sexes or not (ages[0] <= s["age"] <= ages[1]):
            continue
        if practices_only and s["req"] not in community:
            continue
        for org, res in s["orgs"]:
            if ecoli_only and org != "ECOL":
                continue
            k = (s["pid"], org, s["collected"].year)
            if first_isolate and k in seen:
                continue
            seen.add(k)
            iso.append(res)
    return {d: sum(r.get(d) == "R" for r in iso) / max(1, sum(r.get(d) in ("R", "S", "I") for r in iso))
            for d in DRUGS}, len(iso)


def second_course_rates(L, fc, window=28):
    """Each drug's share of first courses followed by another pathway course within `window` days."""
    by = pathway_issues(L)
    num, den = defaultdict(int), defaultdict(int)
    for c in fc:
        later = [d for d, _, _ in by[c["pid"]] if 0 < (d - c["day"]).days <= window]
        den[c["drug"]] += 1
        num[c["drug"]] += bool(later)
    return {d: num[d] / max(1, den[d]) for d in DRUGS}


def weighted_all_cultures(L, fc, lo=-1, hi=1, window=28):
    """Every culture tied to a first course's episode (at the consultation or after it, within `window` days),
    weighted by the inverse of the episode's chance of being cultured given whether a second course followed."""
    by = pathway_issues(L)
    specs = defaultdict(list)
    for s in L["specs"]:
        if s["sex"] == "F" and 16 <= s["age"] <= 64:
            specs[s["pid"]].append(s)
    cells = defaultdict(lambda: [0, 0])     # failed -> [episodes, cultured]
    rec = []
    for c in fc:
        failed = any(0 < (d - c["day"]).days <= window for d, _, _ in by[c["pid"]])
        cand = [s for s in specs.get(c["pid"], []) if lo <= (s["collected"] - c["day"]).days <= window]
        cells[failed][0] += 1
        if cand:
            cells[failed][1] += 1
            rec.append((failed, sorted(cand, key=lambda s: (s["collected"], s["lab"]))[0]))
    w = {f: cells[f][0] / max(1, cells[f][1]) for f in cells}
    tot = sum(cells[f][0] for f in cells)
    return {d: sum(w[f] * resistant(s, d) for f, s in rec) / tot for d in DRUGS}


# --- the ask: organisms in the 2026 cultures of women aged 65 and over and men aged 16 and over -----------------

GROUPS = ("Enterococcus", "Enterobacter")


def organism_group(code, new_system):
    if new_system:
        return {"ENTC": "Enterococcus", "ECLO": "Enterobacter"}.get(code)
    return {"ENTE": "Enterococcus", "ENTC": "Enterobacter"}.get(code)


def is_new_system(lab_no):
    return not lab_no.startswith("H")


def ask_grid(L, group_fn=None):
    group_fn = group_fn or (lambda code, lab: organism_group(code, is_new_system(lab)))
    community = set(L["net"]) | set(L["merged"]) | {L["hub"]}
    pats = defaultdict(set)
    for s in L["specs"]:
        if s["collected"].year != 2026 or s["req"] not in community:
            continue
        if not ((s["sex"] == "F" and s["age"] >= 65) or (s["sex"] == "M" and s["age"] >= 16)):
            continue
        net = network_of(L, s["gp"])
        for org, _ in s["orgs"]:
            g = group_fn(org, s["lab"])
            if g:
                pats[(net, g)].add(s["pid"])
    return {k: len(v) for k, v in pats.items()}


def golden(L):
    fc = first_courses(L)
    n = pool(fc)
    pres = presentation(L, fc)
    ch = chances(pres)
    st = stopped(n, ch, L["order"])
    two, rk = slate(st)
    return {"fc": fc, "pool": n, "pres": pres, "chances": ch, "stopped": st, "slate": two, "rank": rk,
            "grid": ask_grid(L)}
