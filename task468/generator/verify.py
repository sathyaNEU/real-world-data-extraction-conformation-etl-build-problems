"""task468 architecture 6: an independent recomputation of every owed figure from target/ (pandas, no generator code)."""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")
FIG = json.load(open(os.path.join(HERE, "figures.json")))
fails = 0


def same(label, a, b):
    global fails
    good = a == b
    fails += not good
    print("%s  %-46s %s" % ("PASS" if good else "FAIL", label, "" if good else "%s != %s" % (a, b)))


reg = pd.read_excel(os.path.join(T, "glw_trade_waste_agreements_register_2026.xlsx"), sheet_name="Agreements")
cross = pd.read_csv(os.path.join(T, "glw_sampling_point_crosswalk.csv"))
pt = dict(zip(reg["Sampling point"], reg["Customer"]))
leg = {a: pt[b] for a, b in zip(cross["legacy_site_code"], cross["point_id"])}
lim = {c: (v / 1000.0 if str(u).startswith("kg") else float(v))
       for c, v, u in zip(reg["Customer"], reg["COD limit"], reg["COD limit unit"])}

old = pd.read_csv(os.path.join(T, "glw_lims_trade_waste_results_2025-01_to_2026-02.csv"), dtype=str)
old["when"] = pd.to_datetime(old["Sampled"], format="%d/%m/%Y %H:%M")
old["v"] = old["Result"].astype(float)
old.loc[(old["Test"] == "SS") & (old["Qualifier"] == "<"), "v"] = 2.5
wide_old = old.pivot_table(index=["Sample No", "Site Code", "when"], columns="Test", values="v").reset_index()
wide_old["cust"] = wide_old["Site Code"].map(leg)

new = pd.read_csv(os.path.join(T, "glw_labware_trade_waste_results_2026.csv"), dtype=str)
new = new[~new["sample_id"].str.endswith("-D")].copy()
new["base"] = new["sample_id"].str.replace("-R$", "", regex=True)
new["rr"] = new["sample_id"].str.endswith("-R")
new["v"] = new["value"].astype(float)
new.loc[(new["analyte"] == "Suspended Solids") & (new["result_qualifier"] == "<"), "v"] = 2.5
new = new.sort_values(["base", "analyte", "rr"]).drop_duplicates(["base", "analyte"], keep="last")
new["when"] = pd.to_datetime(new["collected_utc"].str[:19]) + pd.Timedelta(hours=10)
wide_new = new.pivot_table(index=["base", "point_id", "when"], columns="analyte", values="v").reset_index()
wide_new["cust"] = wide_new["point_id"].map(pt)
wide_new = wide_new[wide_new["TOC (NPOC)"].notna()]   # compliance composites; inspection grabs carry SS and pH only

par = wide_old.dropna(subset=["TOC", "COD"])
X = np.c_[np.ones(len(par)), par["TOC"], par["CL"]]
beta = np.linalg.lstsq(X, par["COD"].values, rcond=None)[0]

tel = pd.read_csv(os.path.join(T, "glw_trade_waste_flow_telemetry_2026.csv"))
tel["t"] = pd.to_datetime(tel["reading_utc"].str[:19]) + pd.Timedelta(hours=10)
jobs = pd.read_excel(os.path.join(T, "glw_field_service_jobs_2026.xlsx"))
ex = jobs[jobs["Job type"] == "Meter exchange"]
reads = {m: dict(zip(g["t"], g["register"])) for m, g in tel.groupby("meter_serial")}


def cum_fn(c):
    cur = reg.loc[reg["Customer"] == c, "Flow meter"].iloc[0]
    e = ex[ex["Customer"] == c]
    if e.empty:
        r = reads[cur]
        t0 = r[pd.Timestamp("2026-01-01")]
        return lambda t: r[t] - t0
    e = e.iloc[0]
    ro, rn = reads[e["Asset removed"]], reads[e["Asset installed"]]
    off = pd.to_datetime(e["Started (local)"], format="%d/%m/%Y %H:%M")
    t0 = ro[pd.Timestamp("2026-01-01")]
    fin, opn = float(e["Removed final read (kL)"]), float(e["Installed opening read (kL)"])
    return lambda t: (ro[t] - t0) if t <= off else (fin - t0) + (rn[t] - opn)


bounds = [pd.Timestamp(x) for x in ("2026-01-01", "2026-04-01", "2026-07-01", "2026-10-01", "2027-01-01")]
cod, ssm, q = {}, {}, {}
for c in reg["Customer"]:
    f = cum_fn(c)
    q[c] = [int(round(f(bounds[i + 1]) - f(bounds[i]))) for i in range(4)]
    year = f(bounds[4])
    rows = []
    for _, r in wide_old[(wide_old["cust"] == c) & (wide_old["when"].dt.year == 2026)].iterrows():
        rows.append((r["when"].normalize(), r["COD"], r["SS"]))
    for _, r in wide_new[(wide_new["cust"] == c) & (wide_new["when"].dt.year == 2026)].iterrows():
        rows.append((r["when"].normalize(), beta[0] + beta[1] * r["TOC (NPOC)"] + beta[2] * r["Chloride"],
                     r["Suspended Solids"]))
    v = np.array([f(d + pd.Timedelta(days=1)) - f(d) for d, _, _ in rows])
    cod[c] = year * float(np.dot([x for _, x, _ in rows], v) / v.sum()) / 1e6
    ssm[c] = year * float(np.dot([x for _, _, x in rows], v) / v.sum()) / 1e6

log = pd.read_csv(os.path.join(T, "glw_liquid_waste_receival_2026.csv"), dtype=str)
log["t"] = pd.to_datetime(log["received"], format="%d/%m/%Y %H:%M")
log["v"] = log["volume_kl"].astype(float)
man = pd.read_excel(os.path.join(T, "qld_waste_tracking_manifests_glw_2026.xlsx"))
log = log[log["status"] == "Accepted"].merge(man[["Receival docket", "Waste code"]], how="left",
                                              left_on="docket", right_on="Receival docket")
log = log.sort_values(["truck_rego", "t", "docket"])
log["prev_t"] = log.groupby("truck_rego")["t"].shift()
log["prev_c"] = log.groupby("truck_rego")["Waste code"].shift()
second = log["Waste code"].isna() & ((log["t"] - log["prev_t"]) <= pd.Timedelta(hours=2))
log.loc[second, "Waste code"] = log.loc[second, "prev_c"]
log = log[log["t"].dt.year == 2026]
log["q"] = (log["t"].dt.month - 1) // 3
liq = {c: [int(round(log[(log["Waste code"] == c) & (log["q"] == i)]["v"].sum())) for i in range(4)]
       for c in ("GT", "SE", "PL", "LL")}

same("customers over their COD limits", sorted(c for c in cod if cod[c] > lim[c]), sorted(FIG["over"]))
same("ask A, tankered waste by type and quarter (kL)", liq, FIG["ask_a"])
same("ask B, suspended solids (t)", {c: "%.1f" % ssm[c] for c in ssm}, FIG["ask_b"])
print("verify: %d failed" % fails)
sys.exit(1 if fails else 0)
