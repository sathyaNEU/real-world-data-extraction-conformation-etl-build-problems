"""Independent verifier: reads only the shipped bundle (target/ and golden/), on its own code path (csv and openpyxl,
no pandas, no calc.py), and recomputes the call, the default path's call and every graded figure."""
import collections
import csv
import datetime as dt
import json
import os
import statistics
import sys

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
CLASSES = ["Anticonvulsants", "Antipsychotics", "Dementia agents", "Antidepressants, SSRI", "Beta blockers",
           "Loop diuretics", "Benzodiazepines", "Antiparkinson agents", "Urinary antispasmodics",
           "Skeletal muscle relaxants", "Antiemetics", "Oral corticosteroids"]


def eleven(ten):
    a, b, c = ten.split("-")
    return a.zfill(5) + b.zfill(4) + c.zfill(2)


def sheet(path, name):
    wb = openpyxl.load_workbook(path, read_only=True)
    return [r for r in wb[name].iter_rows(values_only=True)]


def main(target, golden):
    f = {n: os.path.join(target, n) for n in os.listdir(target)}
    find = lambda pre: [p for n, p in f.items() if n.startswith(pre)][0]
    drug = sheet(find("state_drug_file"), "Drug file")
    hdr = drug[0]
    i_ndc, i_gpc, i_pkg = hdr.index("NDC"), hdr.index("GPC"), hdr.index("Package description")
    prod, pkg = {}, {}
    for r in drug[1:]:
        n = eleven(r[i_ndc])
        prod[n] = r[i_gpc]
        d = r[i_pkg].upper()
        pkg[n] = "carton" if ("UNIT-DOSE" in d or "BLISTER" in d) else "bottle"
    cl_rows = sheet(find("state_drug_class_list"), "Classes")
    start = [k for k, r in enumerate(cl_rows) if r and r[0] == "Class code"][0]
    cname = {r[0]: r[1] for r in cl_rows[start + 1:] if r and r[0]}
    klass = {r[0]: cname[r[4]] for r in sheet(find("state_drug_class_list"), "Products")[1:] if r and r[0]}
    # rates in effect by month
    month = lambda d: dt.date(d.year, d.month, 1)
    mons = [dt.date(2026 + (m > 12), (m - 1) % 12 + 1, 1) for m in range(4, 16)]
    rate = {}
    grp = collections.defaultdict(list)
    with open(find("state_aac_rates"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            e = dt.date.fromisoformat(r["effective_date"])
            x = dt.date.fromisoformat(r["end_date"]) if r["end_date"] else dt.date(2099, 1, 1)
            for m in mons:
                if e <= m <= x:
                    rate[(r["ndc"], m)] = float(r["aac_per_unit"])
                    grp[(prod[r["ndc"]], pkg[r["ndc"]], m)].append(float(r["aac_per_unit"]))
    ratios = [statistics.median(v) / statistics.median(grp[(g, "bottle", m)])
              for (g, k, m), v in grp.items() if k == "carton" and (g, "bottle", m) in grp]
    prem = statistics.median(ratios)
    gold, default = collections.Counter(), collections.Counter()
    with open(find("corvane_ffs_claims"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            n, m = r["ndc"], month(dt.date.fromisoformat(r["fill_date"]))
            q, paid = float(r["quantity_dispensed"]), float(r["ingredient_cost_paid"])
            c = klass[prod[n]]
            x = rate.get((n, m))
            if x is not None:
                gold[c] += paid - x * q
                default[c] += paid - x * q
                continue
            g, k = prod[n], pkg[n]
            same = grp.get((g, k, m))
            est = statistics.median(same) if same else statistics.median(grp[(g, "bottle", m)]) * prem
            gold[c] += paid - est * q
            anyp = grp.get((g, "bottle", m), []) + grp.get((g, "carton", m), [])
            default[c] += paid - statistics.median(anyp) * q
    rank = sorted(CLASSES, key=lambda c: -gold[c])
    drank = sorted(CLASSES, key=lambda c: -default[c])
    fails = []
    if rank[0] != "Anticonvulsants":
        fails.append("golden call %s" % rank[0])
    if drank[0] != "Antipsychotics":
        fails.append("default call %s" % drank[0])
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    for c in CLASSES:
        lo, hi = figs["classes"][c]["spread_range"]
        if not (lo <= gold[c] <= hi):
            fails.append("%s spread %.0f outside %s" % (c, gold[c], (lo, hi)))
    # the ask: FY2026 by the current class list
    summ = sheet(find("corvane_generic_utilization"), "Utilization")
    h = summ[0]
    tot = collections.defaultdict(lambda: [0, 0.0, 0.0])
    for r in summ[1:]:
        c = klass[prod[r[h.index("NDC")]]]
        t = tot[c]
        t[0] += r[h.index("Claims")]
        t[1] += r[h.index("Units")]
        t[2] += r[h.index("Ingredient cost paid")]
    gx = sheet(os.path.join(golden, "smac_candidate_classes_fy2026.xlsx"), "Candidate classes")
    for r in gx[2:]:
        c = r[1]
        if (r[2], r[3], r[4]) != (tot[c][0], int(round(tot[c][1])), int(round(tot[c][2]))):
            fails.append("ask %s %s against %s" % (c, r[2:5], tot[c]))
        fc = figs["classes"][c]
        if (fc["claims_fy26"], fc["units_fy26"], fc["ingredient_fy26"]) != (r[2], r[3], r[4]):
            fails.append("figures.json %s" % c)
    if fails:
        raise SystemExit("verify FAILED: %s" % "; ".join(fails))
    print("verify: from the bundle alone, costing each unpriced NDC from priced NDCs of the same product and package "
          "proposes %s (%.2f over %s), costing it at the product's rate proposes %s; carton premium %.2f; every "
          "spread inside its range and every FY2026 figure recomputes" % (rank[0], gold[rank[0]] / gold[rank[1]],
                                                                          rank[1], drank[0], prem))


if __name__ == "__main__":
    main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
