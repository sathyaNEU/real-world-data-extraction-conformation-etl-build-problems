"""The independent verifier: every owed figure recomputed from target/ by a second implementation (pandas frames,
normal equations, its own address parsing), compared with figures.json. Exit 1 on any difference."""
import json
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(HERE, "..", "target")
COLS = ["tid", "price", "date", "pc", "ptype", "new", "dur", "paon", "saon", "street", "loc", "town", "dist", "county",
        "cat", "status"]


def ppd(t):
    frames = [pd.read_csv(os.path.join(t, f), header=0, names=COLS, dtype=str, keep_default_na=False)
              for f in ("pp-harrowmere-2015-2025.csv", "pp-harrowmere-2026.csv")]
    base = pd.concat(frames).set_index("tid")
    up = pd.read_csv(os.path.join(t, "pp-monthly-update-2027-01.csv"), header=0, names=COLS, dtype=str,
                     keep_default_na=False).set_index("tid")
    keep = up[up.status.isin(["A", "C"])]
    base = pd.concat([base.drop(index=[i for i in keep.index if i in base.index]), keep])
    base = base.drop(index=[i for i in up[up.status == "D"].index if i in base.index])
    base = base.reset_index()
    base["price"] = base.price.astype(int)
    base["date"] = pd.to_datetime(base.date.str[:10])
    base["key"] = base.paon.str.upper().str.strip() + "|" + base.saon.str.upper().str.strip() + "|" + base.pc.str.upper().str.strip()
    return base


def wards(t):
    names = pd.read_csv(os.path.join(t, "ward_codes_names_2019_2023.csv"))
    nm = dict(zip(names.WD23CD, names.WD23NM))
    pcs = pd.read_csv(os.path.join(t, "harrowmere_postcode_directory_2026-11.csv"), dtype=str)
    return {pc: nm[c] for pc, c in zip(pcs.pcds, pcs.wd23cd)}


def pcnorm(x):
    x = re.sub(r"\s", "", str(x).upper())
    return x[:-3] + " " + x[-3:]


def register(t):
    xl = pd.ExcelFile(os.path.join(t, "hcc_building_control_completions_2015-2026.xlsx"))
    leg = xl.parse("Legacy 2015-2020", dtype=str, keep_default_na=False)
    uni = xl.parse("Uniform 2021-2026", dtype=str, keep_default_na=False)
    out = []
    for _, r in leg.iterrows():
        a = r["Site address"]
        m = re.search(r"(HW\d)\s?(\d[A-Z]{2})\s*$", a)
        pc = pcnorm(m.group(1) + m.group(2))
        rest = re.sub(r",?\s*Harrowmere,?\s*$", "", a[:m.start()].strip().rstrip(","), flags=re.I).strip().rstrip(",")
        flat = ""
        fm = re.match(r"(Flat \w+), (.*)", rest, re.I)
        if fm:
            flat, rest = fm.group(1), fm.group(2)
        if "," in rest:
            num = rest.split(",")[0].strip()
        else:
            nm = re.match(r"(\d+\w?)\s", rest)
            if nm:
                num = nm.group(1)
            else:   # a house name: every word before the street's first word that the street ends with a suffix
                words = rest.split()
                ends = [i for i, w in enumerate(words) if w.upper() in ("ROAD", "STREET", "AVENUE", "GROVE", "TERRACE",
                        "CLOSE", "CRESCENT", "DRIVE", "LANE", "PLACE", "GARDENS", "WAY", "COURT", "RD", "ST", "AVE",
                        "GR", "TER", "CL", "CRES", "DR", "LN", "PL", "GDNS", "CT", "MEWS")]
                e = ends[-1] if ends else len(words) - 1
                num = " ".join(words[:e - 1])
        out.append(dict(ref=r["Ref"], key=num.upper() + "|" + flat.upper() + "|" + pc,
                        done=pd.to_datetime(r["Completed"], format="%d/%m/%Y"), created=int(r["Units +"] or 0),
                        lost=int(r["Units -"] or 0), blank=False, pc=pc, cert=""))
    for _, r in uni.iterrows():
        num = str(r["House no/name"])
        flat = ""
        fm = re.match(r"(Flat \w+), (.*)", num, re.I)
        if fm:
            flat, num = fm.group(1), fm.group(2)
        out.append(dict(ref=r["Application"], key=num.upper() + "|" + flat.upper() + "|" + pcnorm(r["Postcode"]),
                        done=pd.to_datetime(r["Certificate date"]), created=int(r["Dwellings created"] or 0),
                        lost=int(r["Dwellings lost"] or 0), blank=r["Dwellings lost"] == "" and r["Work type"] == "Conversion",
                        pc=pcnorm(r["Postcode"]), cert=r["Certificate"]))
    return pd.DataFrame(out)


def index_change(st, reg, wmap, drop=True):
    st = st.sort_values(["key", "date", "tid"])
    st["prev_date"] = st.groupby("key").date.shift()
    st["prev_price"] = st.groupby("key").price.shift()
    pr = st.dropna(subset=["prev_date"]).copy()
    if drop:
        w = reg.groupby("key").done.apply(list).to_dict()
        pr["spans"] = [any(a < d < b for d in w.get(k, [])) for k, a, b in zip(pr.key, pr.prev_date, pr.date)]
        pr = pr[~pr.spans]
    pr["y1"], pr["y2"] = pr.prev_date.dt.year, pr.date.dt.year
    pr = pr[pr.y1 != pr.y2]
    pr["lr"] = np.log(pr.price / pr.prev_price)
    pr["ward"] = [wmap.get(pcnorm(p)) for p in pr.pc]
    out = {}
    years = list(range(2016, 2027))
    for wd, g in pr.groupby("ward"):
        X = np.zeros((len(g), len(years)))
        for j, y in enumerate(years):
            X[:, j] = (g.y2.values == y).astype(float) - (g.y1.values == y).astype(float)
        b = np.linalg.solve(X.T @ X, X.T @ g.lr.values)
        out[wd] = 100 * (np.exp(b[-1] - b[-2]) - 1)
    return out


def main(t=T):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    fails = []
    df = ppd(t)
    wmap = wards(t)
    reg = register(t)
    st = df[(df.cat == "A") & df.ptype.isin(list("DSTF"))].copy()
    ch = index_change(st, reg, wmap)
    for w, v in ch.items():
        if round(v + 1e-12, 1) != fig["change"][w]:
            fails.append("change %s %.3f against %s" % (w, v, fig["change"][w]))
    press = sorted(w for w, v in ch.items() if round(v, 1) > 5.0)
    if press != sorted(fig["call"]["pressured"]):
        fails.append("pressured %s" % press)
    pipe = pd.read_excel(os.path.join(t, "hvha_affordable_pipeline_2027-28.xlsx"), sheet_name="Pipeline")
    ok = pipe[pipe.Status.isin(["Approved", "In contract"]) & (pipe["Start on site (planned)"] >= "2027-04-01")
              & (pipe["Start on site (planned)"] <= "2028-03-31")]
    homes = ok.groupby("Ward").Homes.sum()
    tot = sum(homes[w] for w in press)
    for w in press:
        s = int(round(12_000_000 * homes[w] / tot))
        if s != fig["call"]["shares"][w]:
            fails.append("share %s %d" % (w, s))
    # Ask A: certified in 2026, each application once, blank losses read from the record
    dw = set(df[df.ptype.isin(list("DSTF"))].key)
    first = df[df.ptype.isin(list("DSTF"))].groupby("key").date.min().to_dict()
    r26 = reg[reg.done.dt.year == 2026].drop_duplicates("ref", keep="last")
    supply = {}
    for _, r in r26.iterrows():
        if r.created == 0 and r.lost == 0 and not r.blank:
            continue
        lost = (1 if (r.key in dw and first[r.key] < r.done) else 0) if r.blank else r.lost
        supply[wmap[r.pc]] = supply.get(wmap[r.pc], 0) + r.created - lost
    for w, v in fig["ask_a"].items():
        if supply.get(w, 0) != v:
            fails.append("ask A %s %d against %d" % (w, supply.get(w, 0), v))
    # Ask B: a price several times the ward's standard median on several same-day entries is paid once
    s26 = st[st.date.dt.year == 2026].copy()
    s26["ward"] = [wmap[pcnorm(p)] for p in s26.pc]
    med = s26.groupby("ward").price.median()
    b = df[(df.cat == "B") & df.ptype.isin(list("DSTF")) & (df.date.dt.year == 2026)].copy()
    b["ward"] = [wmap[pcnorm(p)] for p in b.pc]
    money = {}
    for (d, p), g in b.groupby(["date", "price"]):
        if len(g) >= 2 and p > 3 * med[g.ward.iloc[0]]:
            money[g.ward.iloc[0]] = money.get(g.ward.iloc[0], 0) + p
        else:
            for wd in g.ward:
                money[wd] = money.get(wd, 0) + p
    for w, v in fig["ask_b_money"].items():
        if money.get(w, 0) != v:
            fails.append("ask B %s %d against %d" % (w, money.get(w, 0), v))
    # Ask C: a later claim by another provider restating the same site's starts is not a start
    c = pd.read_csv(os.path.join(t, "hvha_start_on_site_claims_2025-2027.csv"), dtype=str)
    c["start"] = pd.to_datetime(c["Start on site"], format="%d/%m/%Y")
    c["sub"] = pd.to_datetime(c["Claim submitted"], format="%d/%m/%Y")
    c["homes"] = c.Homes.astype(int)
    c["pc"] = [pcnorm(p) for p in c["Site postcode"]]
    live = c[c["Claim status"].isin(["Paid", "Approved"])]
    starts = {}
    for i, r in live[live.start.dt.year == 2026].iterrows():
        o = live[(live.pc == r.pc) & (live.Provider != r.Provider) & (live.start >= r.start) & (live.start.dt.year == 2026)]
        if len(o) and o.homes.sum() == r.homes and r["sub"] > o["sub"].min():
            continue
        starts[wmap[r.pc]] = starts.get(wmap[r.pc], 0) + r.homes
    for w, v in fig["ask_c"].items():
        if starts.get(w, 0) != v:
            fails.append("ask C %s %d against %d" % (w, starts.get(w, 0), v))
    for f in fails:
        print("FAIL", f)
    print("verify: %d differences" % len(fails) if fails else "verify: every owed figure recomputed independently")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else T))
