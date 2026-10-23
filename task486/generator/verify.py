"""Independent verifier: recomputes every graded figure from the shipped bundle alone, with its own reader and its own
resolution, and compares them with the golden workbook. It imports nothing from the generator.

    python3 task486/generator/verify.py [target] [golden]       exit 0 when every figure agrees
"""
import collections
import csv
import datetime as dt
import json
import os
import sys

import openpyxl

FY = (dt.date(2025, 10, 1), dt.date(2026, 9, 30))
Q = [(dt.date(2025, 10, 1), dt.date(2025, 12, 31)), (dt.date(2026, 1, 1), dt.date(2026, 3, 31)),
     (dt.date(2026, 4, 1), dt.date(2026, 6, 30)), (dt.date(2026, 7, 1), dt.date(2026, 9, 30))]
CONT = ["HAL", "MEL", "OND", "PYR"]
NAME = {"Halvering City and County CoC": "HAL", "Melbray County CoC": "MEL", "Ondrava County CoC": "OND",
        "Pyrenna County CoC": "PYR", "Halvering Valley Coalition for Survivors": "DVC", "Region": "ALL"}


def rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def day(s):
    if not s:
        return None
    if "/" in s:
        m, d, y = s.split("/")
        return dt.date(int(y), int(m), int(d))
    return dt.date(int(s[:4]), int(s[5:7]), int(s[8:10]))


def people(T):
    reg = openpyxl.load_workbook(os.path.join(T, "partnership_project_register.xlsx"), read_only=True)
    ptype = {int(r[1]): int(r[3]) for r in list(reg["HMIS projects"].iter_rows(values_only=True))[1:]}
    site = {r[0]: r[2] for r in list(reg["Clinic sites"].iter_rows(values_only=True))[1:]}
    node = {}

    def nid(k):
        if k not in node:
            node[k] = len(node)
        return node[k]
    for r in rows(os.path.join(T, "hmis_client_fy2025_fy2026.csv")):
        nid(("HMIS-" + r["SourceCoC"], r["PersonalID"]))
    out = {}
    for r in rows(os.path.join(T, "hmis_exit_fy2025_fy2026.csv")):
        out[(r["SourceCoC"], r["EnrollmentID"])] = day(r["ExitDate"])
    info = collections.defaultdict(lambda: {"on": False, "h": None, "dv": False, "o": None})
    enr = []
    for r in rows(os.path.join(T, "hmis_enrollment_fy2025_fy2026.csv")):
        e = {"coc": r["SourceCoC"], "id": r["EnrollmentID"], "pid": r["PersonalID"], "t": ptype[int(r["ProjectID"])],
             "in": day(r["EntryDate"]), "out": out.get((r["SourceCoC"], r["EnrollmentID"])), "hh": r["HouseholdID"],
             "rel": int(r["RelationshipToHoH"]), "mi": day(r["MoveInDate"])}
        enr.append(e)
        k = nid(("HMIS-" + e["coc"], e["pid"]))
        if e["in"] <= FY[1] and (e["out"] is None or e["out"] >= FY[0]):
            a = info[k]
            a["on"] = True
            if a["h"] is None or e["in"] > a["h"][0]:
                a["h"] = (e["in"], e["coc"])
    wb = openpyxl.load_workbook(os.path.join(T, "dvc_comparable_db_export.xlsx"), read_only=True)
    for r in list(wb["Clients"].iter_rows(values_only=True))[1:]:
        nid(("DVC", r[0]))
    for r in list(wb["Stays"].iter_rows(values_only=True))[1:]:
        k = nid(("DVC", r[1]))
        s, e = r[3].date(), (r[4].date() if r[4] else None)
        if s <= FY[1] and (e is None or e > FY[0]):
            info[k]["on"] = True
            info[k]["dv"] = True
    for r in rows(os.path.join(T, "wsh_hch_encounters_fy2025_fy2026.csv")):
        k = nid(("WSH", r["PatientKey"]))
        d = day(r["EncounterDate"])
        if FY[0] <= d <= FY[1]:
            if r["HousingStatus"] in ("Street", "Homeless Shelter", "Transitional"):
                info[k]["on"] = True
            if info[k]["o"] is None or d > info[k]["o"][0]:
                info[k]["o"] = (d, site[r["Site"]])
    with open(os.path.join(T, "hot_field_app_contacts.jsonl"), encoding="utf-8") as fh:
        for line in fh:
            c = json.loads(line)
            k = nid(("HOT", c["client_key"]))
            d = day(c["contact_time"][:10])
            if FY[0] <= d <= FY[1]:
                info[k]["on"] = True
                if info[k]["o"] is None or d > info[k]["o"][0]:
                    info[k]["o"] = (d, "HAL")
    links = []
    for r in rows(os.path.join(T, "sdlu_linkage_pairs_run_20261008.csv")):
        if r["finding"] == "LINK":
            links.append((-float(r["score"]), nid((r["source_a"], r["record_a"])), nid((r["source_b"], r["record_b"]))))
    src = {v: k[0] for k, v in node.items()}
    up = list(range(len(node)))
    held = [{src[i]} for i in range(len(node))]

    def top(x):
        while up[x] != x:
            up[x] = up[up[x]]
            x = up[x]
        return x
    for s, a, b in sorted(links):
        ra, rb = top(a), top(b)
        if ra != rb and not (held[ra] & held[rb]):
            up[ra] = rb
            held[rb] |= held[ra]
    who = collections.defaultdict(list)
    for i in range(len(node)):
        who[top(i)].append(i)
    count = collections.Counter()
    for idx in who.values():
        if not any(info[i]["on"] for i in idx):
            continue
        hs = [info[i]["h"] for i in idx if info[i]["h"]]
        if hs:
            count[max(hs)[1]] += 1
        elif any(info[i]["dv"] for i in idx):
            count["DVC"] += 1
        else:
            count[max(info[i]["o"] for i in idx if info[i]["o"])[1]] += 1
    tot = sum(count.values())
    amt = {k: int(18000000 * count[k] / tot + 0.5) for k in CONT + ["DVC"]}
    return count, amt, enr


def nights(T, enr):
    seen = collections.defaultdict(set)
    for e in enr:
        if e["t"] in (0, 8):
            end = e["out"] or (FY[1] + dt.timedelta(days=1))
            d = max(e["in"], FY[0])
            while d < min(end, FY[1] + dt.timedelta(days=1)):
                seen[e["coc"]].add((e["pid"], d))
                d += dt.timedelta(days=1)
    for r in rows(os.path.join(T, "hmis_services_fy2025_fy2026.csv")):
        d = day(r["DateProvided"])
        if r["RecordType"] == "200" and FY[0] <= d <= FY[1]:
            seen[r["SourceCoC"]].add((r["PersonalID"], d))
    return {c: [sum(1 for p, d in seen[c] if a <= d <= b) for a, b in Q] for c in CONT}


def waits(enr):
    rrh = [e for e in enr if e["t"] == 13]
    left = collections.defaultdict(list)
    for e in rrh:
        if e["out"]:
            left[(e["coc"], e["pid"], e["out"])].append(e)
    kid = {(e["coc"], e["hh"]) for e in enr if e["rel"] == 2}
    w = collections.defaultdict(list)
    for e in rrh:
        if e["rel"] != 1 or not e["mi"] or not FY[0] <= e["mi"] <= FY[1]:
            continue
        cur, first = e, e["in"]
        while True:
            back = [x for x in left.get((cur["coc"], cur["pid"], first), []) if x["id"] != cur["id"]]
            if not back:
                break
            cur, first = back[0], back[0]["in"]
        t = (e["coc"], e["hh"]) in kid
        w[(e["coc"], t)].append((e["mi"] - first).days)
        w[("ALL", t)].append((e["mi"] - first).days)
    return {k: int(10 * sum(v) / len(v) + 0.5) / 10 for k, v in w.items()}


def golden_values(G):
    wb = openpyxl.load_workbook(os.path.join(G, "halvering_2027_fund_allocation.xlsx"), data_only=True)
    a = {}
    for r in wb["Allocation 2027"].iter_rows(min_row=5, max_row=9, values_only=True):
        a[NAME[r[0]]] = (r[1], r[3])
    n = {}
    for r in wb["Shelter nights"].iter_rows(min_row=5, max_row=8, values_only=True):
        n[NAME[r[0]]] = list(r[1:5])
    wt = {}
    for r in wb["Rapid re-housing"].iter_rows(min_row=5, max_row=14, values_only=True):
        wt[(NAME[r[0]], r[1] == "Households with children")] = r[3]
    return a, n, wt


def main(T=None, G=None):
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    T = T or os.path.join(here, "target")
    G = G or os.path.join(here, "golden")
    count, amt, enr = people(T)
    nt = nights(T, enr)
    wt = waits(enr)
    ga, gn, gw = golden_values(G)
    bad = []
    for k in CONT + ["DVC"]:
        if ga[k] != (count[k], amt[k]):
            bad.append("allocation %s: verifier %s, golden %s" % (k, (count[k], amt[k]), ga[k]))
    for c in CONT:
        if gn[c] != nt[c]:
            bad.append("nights %s: verifier %s, golden %s" % (c, nt[c], gn[c]))
    for k, v in wt.items():
        if abs(gw[k] - v) > 1e-9:
            bad.append("waits %s: verifier %s, golden %s" % (k, v, gw[k]))
    print("verify: %d people, %s; %d night cells; %d waits" % (sum(count.values()), dict(amt), 16, len(wt)))
    for b in bad:
        print("MISMATCH", b)
    print("verify: %s" % ("every graded figure agrees" if not bad else "%d mismatches" % len(bad)))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main(*(sys.argv[1:3])))
