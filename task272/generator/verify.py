"""The independent verifier: every graded figure recomputed from target/ by a second code path (pandas, merge_asof,
statsmodels-free least squares), compared with figures.json.

    python3 task272/generator/verify.py
"""
import json
import math
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")


def norm_sf(x):
    return 0.5 * math.erfc(x / math.sqrt(2.0))


def main(target=TARGET):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    master = pd.read_excel(os.path.join(target, "compounded_product_master.xlsx"))
    master.columns = ["code", "name", "container", "vol", "tol", "sg", "tare", "station", "every"]
    eq = pd.read_csv(os.path.join(target, "compounding_equipment_register.csv"))
    st = dict(zip(eq["serial"], eq["station"]))
    d = pd.read_parquet(os.path.join(target, "compounder_dose_log_2026.parquet"))
    d["t"] = pd.to_datetime(d["fill_end_time"]).dt.tz_localize("UTC")
    done = d[d["status"] == "COMPLETE"].copy()
    ev = pd.read_csv(os.path.join(target, "compounder_events_2026.csv"))
    su = ev[ev["event"] == "SET_UP"].copy()
    su["t"] = pd.to_datetime(su["event_time"], utc=True)
    su = su.sort_values("t").drop_duplicates(["compounder_sn", "set_lot"], keep="first")
    done = done.sort_values("t")
    su = su.sort_values("t")
    done = pd.merge_asof(done, su[["t", "compounder_sn", "set_lot"]].rename(columns={"t": "t_setup"}),
                         left_on="t", right_on="t_setup", by="compounder_sn", direction="backward")
    done = done.sort_values(["compounder_sn", "set_lot", "t"])
    done["L"] = done.groupby(["compounder_sn", "set_lot"])["programmed_ml"].cumsum() / 1000.0 - done["programmed_ml"] / 1000.0
    frames = []
    xl = pd.ExcelFile(os.path.join(target, "gravimetric_check_register_2026.xlsx"))
    for q, sh in enumerate(xl.sheet_names):
        x = xl.parse(sh)
        gross = x.columns[5].startswith("Gross")
        x = x.rename(columns={x.columns[5]: "wt"})
        x["q"] = q + 1
        x["gross"] = gross
        frames.append(x)
    ck = pd.concat(frames, ignore_index=True)
    ck = ck.merge(master[["name", "code", "vol", "sg", "tare", "tol"]], left_on="Product", right_on="name")
    ck["net"] = np.where(ck["gross"], ck["wt"] - ck["tare"], ck["wt"])
    ck["v"] = ck["net"] / ck["sg"]
    ck["dev"] = 100 * (ck["v"] / ck["vol"] - 1)
    ck = ck.merge(done[["batch_no", "dose_no", "compounder_sn", "set_lot", "L"]],
                  left_on=["Batch", "Dose no."], right_on=["batch_no", "dose_no"], how="left")
    bad = []
    rates = {}
    for code in fig["golden"]:
        c = ck[ck["code"] == code]
        g = c.groupby(["compounder_sn", "set_lot"])
        Lc = c["L"] - g["L"].transform("mean")
        vc = c["dev"] - g["dev"].transform("mean")
        b = float((Lc * vc).sum() / (Lc ** 2).sum()) if (Lc ** 2).sum() > 0 else 0.0
        a = g.apply(lambda s: (s["dev"] - b * s["L"]).mean(), include_groups=False)
        res = c["dev"] - b * c["L"] - c.set_index(["compounder_sn", "set_lot"]).index.map(a).values
        sig = math.sqrt(float((res ** 2).sum()) / (len(c) - len(a) - 1))
        mu = float(a.mean())
        kbar = float(g.size().mean())
        tau2 = max(0.0, float(a.var(ddof=1)) - sig ** 2 / max(1.0, kbar))
        s = math.sqrt(sig ** 2 + tau2)
        tol = float(master.loc[master["code"] == code, "tol"].iloc[0])
        dd = done[done["product_no"] == code]
        m = mu + b * dd["L"].values
        p = np.array([norm_sf((tol - x) / s) + norm_sf((tol + x) / s) for x in m])
        rates[code] = 1e5 * p.sum() / len(dd)
        if abs(rates[code] - fig["golden"][code]["rate"]) > 0.051 + 0.002 * rates[code]:
            bad.append(("rate", code, rates[code], fig["golden"][code]["rate"]))
    call = sorted(c for c, r in rates.items() if r > 10)
    if call != fig["call"]["products"]:
        bad.append(("call", call, fig["call"]["products"]))
    loc = done["t"].dt.tz_convert("America/Toronto")
    done["m"] = loc.dt.month
    done["st"] = done["compounder_sn"].map(st)
    a = done.groupby(["st", "m"]).size()
    for k, v in fig["ask_a"].items():
        s_, m = k.split()
        if int(a.get((s_, int(m)), 0)) != v:
            bad.append(("ask_a", k, int(a.get((s_, int(m)), 0)), v))
    first = done.sort_values("t").groupby(["compounder_sn", "set_lot"])["product_no"].first()
    nb = first.value_counts()
    for k, v in fig["ask_b"].items():
        if int(nb.get(k, 0)) != v:
            bad.append(("ask_b", k, int(nb.get(k, 0)), v))
    n = len(fig["golden"]) + 1 + len(fig["ask_a"]) + len(fig["ask_b"])
    print("verify: %d figures, %d mismatches" % (n, len(bad)))
    for x in bad[:20]:
        print("  ", x)
    print("PASS" if not bad else "FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
