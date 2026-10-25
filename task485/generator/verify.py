"""An independent recomputation of every graded figure from target/ alone, written without golden.py: the 2025
register, the build-up, each ward's 2032 forecast and finding, and the 2021 register by ward; compared with
generator/figures.json at the write-up's rounding.

    python3 task485/generator/verify.py
"""
import csv
import datetime as dt
import json
import os
from collections import defaultdict

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")
D = dt.date
RES = ("RD02", "RD03", "RD04", "RD06")


def tp(n):
    return os.path.join(T, n)


def k_on(day, Y):
    """canvasses by the 1 December Y register of a dwelling in use from day (None: not in use by 31 October Y)"""
    if day > D(Y, 10, 31):
        return None
    first = day.year if day <= D(day.year, 8, 31) else day.year + 1
    return Y - first + 1


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    ok = []

    def same(label, a, b):
        ok.append(a == b)
        print("%s  %s  %s %s" % ("PASS" if a == b else "FAIL", label, a, "" if a == b else "against %s" % (b,)))
    wards = {}
    for r in csv.DictReader(open(tp("wards_councillors_2014_order.csv"), newline="")):
        wards[r["ward_code"]] = (r["ward_name"], int(r["councillors"]))
    gaz = {}
    for r in csv.DictReader(open(tp("llpg_extract_2026-10-12.csv"), newline="")):
        if r["LOGICAL_STATUS"] == "1" and r["BLPU_STATE"] == "2" and r["CLASSIFICATION"] in RES:
            gaz[int(r["UPRN"])] = (r["WARD_CODE"], "flat" if r["CLASSIFICATION"] == "RD06" else "house",
                                   D.fromisoformat(r["BLPU_STATE_DATE"]))
    reg = defaultdict(dict)
    for r in csv.DictReader(open(tp("ems_property_electorate_2022-2025.csv"), newline="")):
        reg[int(r["register_date"][:4])][int(r["uprn"])] = int(r["local_government_electors"])
    new, done_by_site = set(), defaultdict(lambda: [0, 0])
    ws = openpyxl.load_workbook(tp("housing_completions_monitoring_2014-2026.xlsx"), read_only=True)["Completions"]
    for i, r in enumerate(ws.iter_rows(values_only=True)):
        if i >= 4 and r[0]:
            new.add(int(r[5]))
            done_by_site[r[0]][1 if r[7] in ("Flat", "Maisonette") else 0] += 1
    same("2025 register's local government electors", "{:,}".format(sum(reg[2025].values())), f["components"]["electors_2025"])
    # settled level and build-up
    num, den = defaultdict(float), defaultdict(int)
    for u, n in reg[2025].items():
        w, t, day = gaz[u]
        if k_on(day, 2025) >= 7:
            num[t] += n
            den[t] += 1
    S = {t: num[t] / den[t] for t in den}
    same("settled level", {t: round(x, 2) for t, x in S.items()}, f["settled"])
    bn, bd = defaultdict(float), defaultdict(int)
    for Y in (2022, 2023, 2024, 2025):
        for u, n in reg[Y].items():
            if u not in new:
                continue
            w, t, day = gaz[u]
            k = k_on(day, Y)
            if k is not None and k < 7:
                bn[k] += n / S[t]
                bd[k] += 1
    c = {k: bn[k] / bd[k] for k in bd}
    same("build-up", {str(k): round(x, 2) for k, x in sorted(c.items())}, f["buildup"])

    def share(k):
        return 0.0 if k is None else (1.0 if k >= 7 else c[k])
    e = defaultdict(float)
    for u, n in reg[2025].items():
        w, t, day = gaz[u]
        e[w] += n if k_on(day, 2025) >= 7 else S[t] * share(k_on(day, 2032))
    for u, (w, t, day) in gaz.items():
        if u not in reg[2025] and day > D(2025, 10, 31):
            e[w] += S[t] * share(k_on(day, 2032))
    rows = list(openpyxl.load_workbook(tp("housing_trajectory_2026-09-30.xlsx"), read_only=True)["Trajectory"].iter_rows(values_only=True))
    hdr = list(rows[3])
    name2code = {v[0]: k for k, v in wards.items()}
    traj_dw = 0
    for r in rows[4:]:
        if not r[0]:
            continue
        rec = dict(zip(hdr, r))
        dh, df = done_by_site.get(rec["Site ref"], (0, 0))
        rh, rf = (rec["Houses"] or 0) - dh, (rec["Flats"] or 0) - df
        sf = rf / float(rh + rf) if rh + rf else 0.0
        for col in hdr[10:]:
            if col.startswith("2033"):
                continue
            n = rec[col] or 0
            y0 = int(col[:4])
            if y0 <= 2031:
                traj_dw += n
            months = [(y0, m) for m in range(10 if y0 == 2026 else 4, 13)] + [(y0 + 1, m) for m in range(1, 4)]
            for yy, mm in months:
                k = k_on(D(yy, mm, 15), 2032)
                for t, sh in (("house", 1 - sf), ("flat", sf)):
                    e[name2code[rec["Ward"]]] += n * sh / len(months) * S[t] * share(k)
    same("trajectory dwellings 2026/27 to 2031/32", "{:,}".format(traj_dw), f["components"]["trajectory_dwellings"])
    tot = sum(e.values())
    avg = tot / 43.0
    v = {w: 100.0 * (e[w] / wards[w][1] / avg - 1.0) for w in wards}
    same("2032 total", "{:,}".format(round(tot)), f["forecast"]["total"])
    same("2032 average", "{:,}".format(round(avg)), f["forecast"]["average_whole"])
    same("variances", {wards[w][0]: round(v[w], 1) for w in wards}, f["forecast"]["variance"])
    same("wards outside", [wards[w][0] for w in wards if abs(v[w]) > 10], f["call"]["fail"])
    # the 2021 register: Electra's switch-off report less the 2022 notices' local government entries
    oldw = {}
    for r in csv.DictReader(open(tp("polling_district_review_2023_schedule.csv"), newline="")):
        oldw[r["replaces_district"]] = name2code[r["ward"]]
    a = defaultdict(int)
    lines = open(tp("ELECTRA_PROPERTY_ELECTORATE_REV_2021.txt"), encoding="utf-8").read().splitlines()
    for ln in lines[lines.index([x for x in lines if x.startswith("PD|")][0]) + 1:]:
        p = ln.split("|")
        a[oldw[p[0]]] += int(p[4]) - int(p[5]) - int(p[6])
    lines = open(tp("ELECTRA_NOTICES_OF_ALTERATION_2021-01_2022-03.txt"), encoding="utf-8").read().splitlines()
    for ln in lines[lines.index([x for x in lines if x.startswith("NOTICE|")][0]) + 1:]:
        p = ln.split("|")
        if p[0].endswith("2022") and p[6] != "F" and not p[7]:
            a[oldw[p[1]]] += -1 if p[5] == "ADD" else 1
    same("2021 register by ward", {wards[w][0]: a[w] for w in wards}, f["ask_a"])
    same("2021 register district", "{:,}".format(sum(a.values())), f["ask_a_total"])
    print("%d of %d PASS" % (sum(ok), len(ok)))
    return all(ok)


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
