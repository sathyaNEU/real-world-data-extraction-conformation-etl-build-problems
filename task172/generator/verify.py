"""Independent verifier: recomputes the call and every ask figure from target/ alone with its own parsing (pandas),
its own Cox fit (statsmodels PHReg, Efron ties, stratified), its own log-rank and its own projection, and compares
with the golden CSV, the golden PDF's text and figures.json.

    python3 task172/generator/verify.py
"""
import json
import math
import os
import re
import sys

import numpy as np
import pandas as pd
from pypdf import PdfReader
from scipy.stats import norm
from statsmodels.duration.hazard_regression import PHReg

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
G = os.path.join(TASK, "golden")
bad = []


def ok(name, cond, detail=""):
    print("%s  %s  %s" % ("PASS" if cond else "FAIL", name, detail), flush=True)
    if not cond:
        bad.append(name)


def f(n):
    return os.path.join(T, n)


sites = {s["site"]: s["time_zone"] for s in json.load(open(f("talon2_sites.json")))["sites"]}
rand = pd.read_csv(f("talon2_irt_randomisation_export.csv"))
utc = pd.to_datetime(rand["Randomisation Date/Time (UTC)"]).dt.tz_localize("UTC")
rand["rdate"] = [u.tz_convert(sites[s]).date() for u, s in zip(utc, rand["Site"])]
rand["arm"] = rand["Treatment Arm"].str.startswith("Ravolimab").astype(int)
rand["stratum"] = rand["Stratum: Disease Status"] + "|" + rand["Stratum: Primary Tumour Site"]
rand = rand.set_index("Randomisation Number")
bicr = pd.read_csv(f("talon2_bicr_timepoint_reads.csv"), parse_dates=["SCANDT"])
bicr["wk"] = bicr["TPT"].str.split().str[1].astype(int)
deaths = pd.read_excel(f("talon2_edc_subject_status.xlsx"), sheet_name="Deaths")
deaths = dict(zip(deaths["Subject"], pd.to_datetime(deaths["Date of death"]).dt.date))
disp = pd.read_excel(f("talon2_edc_subject_status.xlsx"), sheet_name="Disposition")
wdcol = "Date of withdrawal or loss to follow-up"
wd = {s: pd.Timestamp(d).date() for s, d in zip(disp["Subject"], disp[wdcol]) if pd.notna(d)}


def pfs(cut):
    out = []
    for sid, r in rand.iterrows():
        rs = bicr[(bicr["SUBJID"] == sid) & (bicr["SCANDT"].dt.date <= cut)].sort_values("SCANDT")
        last, ne, ev, has_pd = r["rdate"], 0, None, False
        for _, b in rs.iterrows():
            if b["BICR_OVRL_RESP"] == "NE":
                ne += 1
                continue
            if b["BICR_OVRL_RESP"] == "PD":
                has_pd = True
                ev = (last, False) if ne >= 2 else (b["SCANDT"].date(), True)
                break
            last, ne = b["SCANDT"].date(), 0
        dd = deaths.get(sid)
        if ev is None and dd is not None and dd <= cut:
            run = 0
            for _, b in rs.iterrows():
                if last < b["SCANDT"].date() < dd:
                    run = run + 1 if b["BICR_OVRL_RESP"] == "NE" else 0
            ev = (last, False) if run >= 2 else (dd, True)
        if ev is None:
            ev = (last, False)
        risk = (not ev[1]) and not has_pd and not (dd is not None and dd <= cut) and not (sid in wd and wd[sid] <= cut)
        out.append(dict(sid=sid, t=(ev[0] - r["rdate"]).days, e=ev[1], arm=r["arm"], s=r["stratum"], risk=risk,
                        fu=(cut - r["rdate"]).days))
    return pd.DataFrame(out)


# the cut: the 165th event
far = pfs(pd.Timestamp("2027-12-31").date())
far["edate"] = [rand.loc[s, "rdate"] + pd.Timedelta(days=int(t)) for s, t in zip(far["sid"], far["t"])]
cut = sorted(far.loc[far["e"], "edate"])[164]
d = pfs(cut)
ok("165 events at the cut", d["e"].sum() == 165, str(cut))


def lr(df):
    U = V = 0.0
    for _, g in df.groupby("s"):
        tt = np.sort(g.loc[g["e"], "t"].unique())
        for x in tt:
            atr = g[g["t"] >= x]
            n, n1 = len(atr), atr["arm"].sum()
            dd_ = ((g["t"] == x) & g["e"]).sum()
            d1 = ((g["t"] == x) & g["e"] & (g["arm"] == 1)).sum()
            U += dd_ * n1 / n - d1
            if n > 1:
                V += dd_ * (n1 / n) * (1 - n1 / n) * (n - dd_) / (n - 1)
    return U / math.sqrt(V)


z = lr(d)
mod = PHReg(d["t"].values.astype(float), d["arm"].values.astype(float)[:, None], status=d["e"].values.astype(int),
            strata=d["s"].values, ties="efron").fit()
hr = math.exp(mod.params[0])
b = z * math.sqrt(0.5)
cp_trend = 1 - norm.cdf((1.959964 - b - (b / 0.5) * 0.5) / math.sqrt(0.5))
figs = json.load(open(os.path.join(HERE, "figures.json")))
ok("stratified hazard ratio", "%.2f" % hr == figs["hr_stratified"], "%.4f" % hr)
ok("PH conditional power in band A", cp_trend < 0.20 and str(int(round(100 * cp_trend))) == figs["cp_trend"], "%.4f" % cp_trend)

# independent projection: per-arm rates before and after day 105, every patient at risk followed to the 330th event
rate = {}
for a in (0, 1):
    g = d[d["arm"] == a]
    for lo, hi in ((0, 105), (105, 1e9)):
        pt = np.clip(np.minimum(g["t"], hi) - lo, 0, None).sum()
        ev = (g["e"] & (g["t"] >= lo) & (g["t"] < hi)).sum()
        rate[(a, lo)] = ev / pt
drop = len([s for s in wd if wd[s] <= cut]) / float(np.maximum(d["t"], 0).sum())
rng = np.random.default_rng(99)
T0 = d["t"].values.astype(float)
E0 = d["e"].values.astype(bool)
ARM = d["arm"].values.astype(int)
FU = d["fu"].values.astype(float)
RISK = d["risk"].values.astype(bool)
SC = pd.factorize(d["s"])[0]
L0 = np.where(ARM == 1, rate[(1, 0)], rate[(0, 0)])
L1 = np.where(ARM == 1, rate[(1, 105)], rate[(0, 105)])


def lr_np(t, e, arm, s):
    U = V = 0.0
    for k_ in np.unique(s):
        m = s == k_
        tt, ee, aa = t[m], e[m], arm[m]
        o = np.argsort(-tt, kind="stable")
        tt, ee, aa = tt[o], ee[o], aa[o]
        n = np.arange(1, len(tt) + 1, dtype=float)
        n1 = np.cumsum(aa).astype(float)
        # group ties: take the at-risk counts at the last row of each tied time (largest n)
        last = np.r_[tt[1:] != tt[:-1], True]
        cum_e = np.cumsum(ee)
        cum_e1 = np.cumsum(ee & (aa == 1))
        idx = np.where(last)[0]
        de = np.diff(np.r_[0, cum_e[idx]])
        de1 = np.diff(np.r_[0, cum_e1[idx]])
        nn, nn1 = n[idx], n1[idx]
        k2 = de > 0
        U += np.sum(de[k2] * nn1[k2] / nn[k2] - de1[k2])
        q = nn[k2] > 1
        V += np.sum((de[k2] * (nn1[k2] / nn[k2]) * (1 - nn1[k2] / nn[k2]) * (nn[k2] - de[k2]) / np.maximum(nn[k2] - 1, 1))[q])
    return U / math.sqrt(V)


ok("own log-rank matches", abs(lr_np(T0, E0, ARM, SC) - z) < 1e-9, "%.6f %.6f" % (lr_np(T0, E0, ARM, SC), z))
rej = 0
NS = 600
need = 330 - int(E0.sum())
for k in range(NS):
    u = rng.exponential(size=len(T0))
    cap = np.where(T0 < 105, L0 * (105 - T0), 0.0)
    early = (T0 < 105) & (u < cap)
    t_ev = np.where(early, T0 + u / L0, np.maximum(T0, 105) + (u - cap) / L1)
    t_dr = T0 + rng.exponential(1 / drop, size=len(T0))
    nt = np.where(RISK, np.minimum(t_ev, t_dr), T0)
    ne = np.where(RISK, t_ev <= t_dr, E0)
    cal = nt - FU
    fut = np.sort(cal[RISK & ne])
    fcut = fut[need - 1]
    fu2 = FU + fcut
    obs = np.minimum(nt, fu2)
    e2 = ne & (nt <= fu2)
    rej += lr_np(obs, e2, ARM, SC) > 1.959964
cpv = rej / float(NS)
ok("independent projection: band C and the 100 per cent bin", cpv >= 0.95, "%.4f over %d runs" % (cpv, NS))

# golden CSV against independent asks
gold = pd.read_csv(os.path.join(G, "talon2_interim_tables.csv"))
gv = {(r["Measure"], r["Arm"]): int(r["Value"]) for _, r in gold.iterrows()}
armname = {0: "Placebo + GemCis", 1: "Ravolimab + GemCis"}

# ask A
pv = pd.read_excel(f("talon2_pv_sae_line_listing.xlsx"))
pv["v"] = pv["Report version"].map(lambda s: 0 if s == "Initial" else int(s.split()[-1]))
pv = pv.sort_values(["Case number", "v"]).groupby("Case number").tail(1)
pv = pv[pv["Case status"] != "Nullified"]
scr = pd.read_csv(f("talon2_screening_log.csv"))
s2r = dict(zip(rand["Screening Number"], rand.index))
key = lambda r: (r["Site"], r["Sex"], r["Year of Birth"], r["Initials"])
rk = {key(r): r for _, r in scr[scr["Screening No"].isin(s2r)].iterrows()}
for _, r in scr[scr["Outcome"] == "Screen failure"].iterrows():
    if key(r) in rk:
        s2r[r["Screening No"]] = s2r[rk[key(r)]["Screening No"]]
pv["sid"] = pv["Patient (screening number)"].map(s2r)
pv = pv[pv["sid"].notna()]
pv["on"] = pd.to_datetime(pv["Onset date"]).dt.date
pv = pv[[(o >= rand.loc[s, "rdate"]) and (o <= cut) for o, s in zip(pv["on"], pv["sid"])]]
pv["arm"] = pv["sid"].map(rand["arm"])
for a in (0, 1):
    g = pv[pv["arm"] == a]
    ok("ask A patients, %s" % armname[a], gv[("Patients with a serious adverse event", armname[a])] == g["sid"].nunique())
    ok("ask A events, %s" % armname[a], gv[("Serious adverse events, all", armname[a])] == len(g))
    for soc in ("Infections and infestations", "Hepatobiliary disorders", "Gastrointestinal disorders",
                "Blood and lymphatic system disorders"):
        ok("ask A %s, %s" % (soc, armname[a]), gv[(soc, armname[a])] == int((g["MedDRA system organ class"] == soc).sum()))

# ask B
expo = pd.read_csv(f("talon2_edc_exposure.csv"))
expo["d"] = pd.to_datetime(expo["Date administered"], dayfirst=True).dt.date
irt = pd.read_csv(f("talon2_irt_drug_administration.csv"))
irt["d"] = pd.to_datetime(irt["Transaction Date"]).dt.date
adm = irt[irt["Kit Status"] == "Administered"]
first = pd.concat([expo[["Subject", "d"]].rename(columns={"Subject": "sid"}),
                   adm[["Randomisation Number", "d"]].rename(columns={"Randomisation Number": "sid"})]).groupby("sid")["d"].min()
lab = pd.read_csv(f("talon2_central_lab_transfer.csv"))
lab = lab[lab["TEST_CODE"].isin(["ALT", "AST", "TBIL"])]
trk = pd.read_csv(f("talon2_edc_central_lab_kit_log.csv"))
cd = dict(zip(trk["Kit accession number"], pd.to_datetime(trk["Date sample collected"], dayfirst=True).dt.date))
lab["sid"] = lab["SCREENING_NO"].map(s2r)
lab["d"] = lab["ACCESSION"].map(cd)
lab = lab[lab["sid"].isin(first.index)]
lab = lab[[(x > first[s]) and (x <= cut) for x, s in zip(lab["d"], lab["sid"])]]
lab["hit"] = lab["RESULT"] > np.where(lab["TEST_CODE"] == "TBIL", 3.0, 5.0) * lab["REF_HIGH"]
loc = pd.read_csv(f("talon2_edc_local_labs.csv"))
loc["d"] = pd.to_datetime(loc["Sample date"], dayfirst=True).dt.date
loc["code"] = loc["Test"].map({"Alanine aminotransferase": "ALT", "Aspartate aminotransferase": "AST", "Bilirubin, total": "TBIL"})
loc = loc[loc["Subject"].isin(first.index)]
loc = loc[[(x > first[s]) and (x <= cut) for x, s in zip(loc["d"], loc["Subject"])]]
loc["hit"] = loc["Result"] > np.where(loc["code"] == "TBIL", 3.0, 5.0) * loc["Upper limit of normal"]
hits = pd.concat([lab.loc[lab["hit"], ["sid", "TEST_CODE"]].rename(columns={"TEST_CODE": "code"}),
                  loc.loc[loc["hit"], ["Subject", "code"]].rename(columns={"Subject": "sid"})]).drop_duplicates()
hits["arm"] = hits["sid"].map(rand["arm"])
label = {"ALT": "Patients with ALT above 5 x ULN", "AST": "Patients with AST above 5 x ULN",
         "TBIL": "Patients with total bilirubin above 3 x ULN"}
for a in (0, 1):
    for c in ("ALT", "AST", "TBIL"):
        ok("ask B %s, %s" % (c, armname[a]), gv[(label[c], armname[a])] == int(((hits["arm"] == a) & (hits["code"] == c)).sum()))

# ask C
given = set(zip(adm.loc[adm["d"] <= cut, "Randomisation Number"], adm.loc[adm["d"] <= cut, "d"]))
ev = expo[(expo["Treatment"] == "Ravolimab/placebo") & (expo["d"] <= cut)]
given |= set(zip(ev["Subject"], ev["d"]))
treated = set(expo.loc[expo["d"] <= cut, "Subject"]) | set(adm.loc[adm["d"] <= cut, "Randomisation Number"])
for a in (0, 1):
    ok("ask C safety population, %s" % armname[a],
       gv[("Patients who received study treatment", armname[a])] == sum(1 for s in treated if rand.loc[s, "arm"] == a))
    ok("ask C doses, %s" % armname[a],
       gv[("Ravolimab or placebo doses given", armname[a])] == sum(1 for s, _d in given if rand.loc[s, "arm"] == a))

# the golden PDF states the call, the band and the figures
txt = " ".join(p.extract_text() for p in PdfReader(os.path.join(G, "talon2_interim_recommendation.pdf")).pages)
txt = re.sub(r"\s+", " ", txt)
ok("golden PDF states the call", "Continue TALON-2 to its final analysis at 330 events as planned" in txt)
ok("golden PDF states the conditional power", "100 per cent to the nearest 10 per cent" in txt)
ok("golden PDF states the stratified ratio", figs["hr_stratified"] in txt)
print("verify: %d failures" % len(bad))
sys.exit(1 if bad else 0)
