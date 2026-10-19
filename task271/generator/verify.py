"""The independent verifier: every graded figure recomputed from target/ alone, with pandas, numpy and statsmodels
(none of the generator's modules), and compared with figures.json and the golden workbook."""
import json
import os
import sys
from decimal import ROUND_HALF_UP, Decimal

import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = os.path.dirname(os.path.abspath(__file__))
RES = {"0FBG0ZZ", "0FBG4ZZ", "0FTG0ZZ", "0FTG4ZZ"}


def hu(x, nd):
    return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))


def dot(c):
    c = c.strip()
    return c if (not c or "." in c or len(c) <= 3) else c[:3] + "." + c[3:]


def fixed(path, shift):
    rows = []
    for line in open(path, encoding="ascii"):
        line = line.rstrip("\r\n")
        p = 56 + shift
        dx = []
        for _ in range(9):
            c, poa = line[p - 1:p + 6].strip(), line[p + 6:p + 7].strip()
            p += 8
            if c:
                dx.append((dot(c), poa))
        px = []
        for _ in range(6):
            c = line[p - 1:p + 6].strip()
            p += 7
            if c:
                px.append(c)
        d0 = line[p - 1:p + 7].strip()
        rows.append(dict(hosp=line[10:14], key=line[14:30].strip(), admit=pd.Timestamp(line[34:42]),
                         discharge=pd.Timestamp(line[42:50]), px=px,
                         pxd=[pd.Timestamp(d0) if (i == 0 and d0) else pd.NaT for i in range(len(px))], dx=dx))
    return rows


def wide(path, era):
    t = pd.read_csv(path, dtype=str, keep_default_na=False)
    if era == 2:
        f, h, k, a, d, ty, pfx = "%m/%d/%Y", "hospital_no", "person_key", "admit_date", "discharge_date", "admit_type", \
            ("dx%02d", "poa%02d", "px%02d", "pxdate%02d")
        age = "age"
    else:
        f, h, k, a, d, ty, pfx = "%Y-%m-%d", "hosp_id", "link_key", "admission_date", "discharge_date", "adm_type", \
            ("diag_%d", "poa_%d", "proc_%d", "proc_date_%d")
        age = "age_years"
    rows = []
    recs = t.to_dict("records")
    for r in recs:
        dx = [(dot(r[pfx[0] % i]), r[pfx[1] % i]) for i in range(1, 26) if r[pfx[0] % i]]
        px = [r[pfx[2] % i] for i in range(1, 26) if r[pfx[2] % i]]
        pxd = [pd.to_datetime(r[pfx[3] % i], format=f) for i in range(1, 26) if r[pfx[2] % i]]
        rows.append(dict(rec=r[t.columns[0]], hosp=r[h], key=r[k], admit=pd.to_datetime(r[a], format=f),
                         discharge=pd.to_datetime(r[d], format=f), px=px, pxd=pxd, dx=dx, atype=r[ty],
                         age=int(r[age]), sex=r["sex"]))
    return rows


def run(task):
    t = os.path.join(task, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []

    def ok(label, cond, detail=""):
        print("%s  verify: %s %s" % ("PASS" if cond else "FAIL", label, detail))
        if not cond:
            bad.append(label)
    hd = pd.read_excel(os.path.join(t, "ulhdc_hospital_directory.xlsx"), sheet_name="Hospitals", header=2, dtype=str)
    name = {}
    for _, r in hd.iterrows():
        name[str(r["Hospital no. (to 2022)"]).zfill(4)] = r["Hospital"]
        name[str(r["Hospital ID (from 2023)"])] = r["Hospital"]
    npi = dict(zip(hd["NPI (facility)"].astype(str), hd["Hospital"]))
    eight = list(fig["ratio"])
    allr = []
    for y, sh in ((2016, 0), (2017, 0), (2018, 2)):
        allr += fixed(os.path.join(t, "ulhdc_hbp_discharges_%d.txt" % y), sh)
    allr += wide(os.path.join(t, "ulhdc_hbp_discharges_2019_2022.csv"), 2)
    main = wide(os.path.join(t, "ulhdc_hbp_discharges_2023_2025.csv"), 3)
    allr += main
    # each person's earlier operations on the pancreas or bile ducts, from the procedure classes
    cls = pd.read_csv(os.path.join(t, "ulhdc_procedure_classes.csv"), dtype=str)
    op_cls = set(cls.icd10pcs[cls.ulhdc_procedure_class.str.match(r"^(Pancreas: (excision|total|duct|debridement)|"
                                                                   r"Bile duct:)")])
    earlier = {}
    for r in allr:
        if not r["key"]:
            continue
        for c, dd in zip(r["px"], r["pxd"]):
            if c in op_cls:
                earlier.setdefault(r["key"], []).append(dd if not pd.isna(dd) else r["admit"])
    dl = pd.read_csv(os.path.join(t, "ulhdc_death_linkage_2016_2026.csv"), dtype=str, keep_default_na=False)
    dl = dl[dl.death_record_found == "Y"]
    death = dict(zip(dl.link_key, pd.to_datetime(dl.date_of_death)))
    rows = []
    for r in main:
        hn = name[r["hosp"]]
        dates = [d for c, d in zip(r["px"], r["pxd"]) if c in RES]
        if not dates or hn not in eight or r["age"] < 18:
            continue
        op = dates[0]
        if not (pd.Timestamp("2023-01-01") <= op <= pd.Timestamp("2025-12-31")):
            continue
        y = [c for c, p in r["dx"] if p == "Y"]
        has = lambda *pre: float(any(c.startswith(p) for c in y for p in pre))
        codes = set(r["px"])
        dd = death.get(r["key"])
        rows.append(dict(h=hn, age10=(r["age"] - 67) / 10, male=float(r["sex"] == "M"),
                         mal=float(r["dx"][0][0].startswith("C")), tot=float(bool(codes & {"0FTG0ZZ", "0FTG4ZZ"})),
                         whip=float("0DT90ZZ" in codes and not codes & {"0FTG0ZZ", "0FTG4ZZ"}),
                         urg=float(r["atype"] in ("1", "2")), wtloss=has("R63.4", "E43", "E44"), chf=has("I50"),
                         ckd=has("N18"), copd=has("J44"), liver=has("K70", "K74", "K76"), dm=has("E10", "E11"),
                         af=has("I48"), redo=float(any(e < r["admit"] for e in earlier.get(r["key"], []))),
                         dead=float(dd is not None and 0 <= (dd - op).days <= 90)))
    d = pd.DataFrame(rows)
    cols = ["age10", "male", "mal", "tot", "whip", "urg", "wtloss", "chf", "ckd", "copd", "liver", "dm", "af", "redo"]
    X = sm.add_constant(d[cols])
    mdl = sm.GLM(d.dead, X, family=sm.families.Binomial()).fit()
    d["e"] = mdl.predict(X)
    g = d.groupby("h")
    ratio = (g.dead.sum() / g.e.sum())
    ok("2,022 operations and 175 deaths", len(d) == fig["totals"]["operations"] and int(d.dead.sum()) ==
       fig["totals"]["deaths"], (len(d), int(d.dead.sum())))
    for hn in eight:
        ok("%s ratio %.1f" % (hn, fig["ratio"][hn]), hu(ratio[hn], 1) == fig["ratio"][hn], round(ratio[hn], 4))
        ok("%s operations and deaths" % hn, int(g.size()[hn]) == fig["operations"][hn] and
           int(g.dead.sum()[hn]) == fig["deaths"][hn])
        ok("%s expected deaths %.1f" % (hn, fig["expected"][hn]), hu(g.e.sum()[hn], 1) == fig["expected"][hn],
           round(g.e.sum()[hn], 3))
    centres = list(ratio.sort_values().index[:3])
    ok("the three centres", sorted(centres) == sorted(fig["call"]["centres"]), centres)
    ok("the first hospital below", ratio.sort_values().index[3] == fig["call"]["first_below"])
    # Ask A: the revised release, a stay sent twice (overlapping stays of one person at one hospital) once
    rv = wide(os.path.join(t, "ulhdc_hbp_2026q1q2_revised.csv"), 3)
    spans = {}
    for r in rv:
        hn = name[r["hosp"]]
        if hn in eight and set(r["px"]) & RES and pd.Timestamp("2026-01-01") <= r["discharge"] <= pd.Timestamp("2026-06-30"):
            spans.setdefault((r["key"], hn), []).append((r["admit"], r["discharge"]))
    cnt = {hn: 0 for hn in eight}
    for (k, hn), sp in spans.items():
        end = None
        for a, b in sorted(sp):
            if end is None or a > end:
                cnt[hn] += 1
                end = b
            else:
                end = max(end, b)
    for hn in eight:
        ok("Ask A %s: %d" % (hn, fig["ask_a"][hn]), cnt[hn] == fig["ask_a"][hn], cnt[hn])
    # Ask B: each claim's chain followed to the claim first received, its latest version; a stay's chains summed
    cl = pd.read_csv(os.path.join(t, "corrisbrook_facility_claims_pancreas_2023_2025.csv"), dtype=str,
                     keep_default_na=False)
    parent = dict(zip(cl.claim_id, cl.original_claim_id))

    def root(c):
        while parent.get(c):
            c = parent[c]
        return c
    cl["root"] = cl.claim_id.map(root)
    cl["amt"] = cl.allowed_amount.astype(float)
    cl["hn"] = cl.billing_npi.map(npi)
    dead_roots = set(cl.root[cl.bill_type == "0118"])
    live = cl[~cl.root.isin(dead_roots)].sort_values(["received_date", "claim_id"])
    cur = live.groupby("root").tail(1)
    stays = cur.groupby(["hn", "member_id", "admit_date"]).amt.sum()
    for hn in eight:
        v = stays.loc[hn]
        ok("Ask B %s: %d" % (hn, fig["ask_b"][hn]), int(hu(v.mean(), 0)) == fig["ask_b"][hn], round(v.mean(), 2))
    # the golden workbook carries the same figures
    wb = os.path.join(task, "golden", "pancreatic_centres_2027.xlsx")
    c1 = pd.read_excel(wb, sheet_name="Centres", header=3)
    c1 = c1[c1.Hospital.isin(eight)].set_index("Hospital")
    ok("workbook ratios", all(abs(c1.loc[hn, "Ratio (observed to expected)"] - fig["ratio"][hn]) < 1e-9 for hn in eight))
    ok("workbook centres", sorted(c1.index[c1["2027 centre"].eq("Yes")]) == sorted(fig["call"]["centres"]))
    a2 = pd.read_excel(wb, sheet_name="2026 so far", header=3).set_index("Hospital")
    ok("workbook Ask A", all(int(a2.loc[hn, "Resections"]) == fig["ask_a"][hn] for hn in eight))
    b2 = pd.read_excel(wb, sheet_name="Members", header=3).set_index("Hospital")
    ok("workbook Ask B", all(int(b2.loc[hn, "Average allowed per stay ($)"]) == fig["ask_b"][hn] for hn in eight))
    print("verify: %d failed" % len(bad))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run(os.path.dirname(HERE)))
