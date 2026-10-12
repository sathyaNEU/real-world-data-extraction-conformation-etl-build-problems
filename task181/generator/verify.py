"""Independent verifier: reads only the shipped bundle (target/) and the goldens, on its own code path (pandas joins
by half-hour bucket for the pairs, its own interval and report arithmetic), and recomputes the call, every sector's
forecast rate, the record the rate rests on, the close-out table and the three summer 2026 measures, then compares
them with the golden workbook and figures.json."""
import datetime as dt
import json
import os
import re
import sys

import numpy as np
import pandas as pd
import pdfplumber

HERE = os.path.dirname(os.path.abspath(__file__))
UTC0 = pd.Timestamp("1970-01-01", tz="UTC")


def secs(col):
    return ((pd.to_datetime(col, utc=True) - UTC0) // pd.Timedelta(seconds=1)).astype("int64")


def local_season(year):
    a = pd.Timestamp("%d-06-01" % year, tz="Europe/Copenhagen").tz_convert("UTC")
    b = pd.Timestamp("%d-09-01" % year, tz="Europe/Copenhagen").tz_convert("UTC")
    return int((a - UTC0).total_seconds()), int((b - UTC0).total_seconds())


def pairs(df):
    """Pairs of traversals in one sector at once, by a self-join on half-hour buckets (a traversal lasts well under
    half an hour, so a partner that entered while it was in the sector entered in its bucket or the next)."""
    out = []
    for sec, d in df.groupby("sector"):
        d = d.reset_index(drop=True)
        d["k"] = np.arange(len(d))
        d["bk"] = d["t0"] // 1800
        left = d[["k", "bk", "t0", "t1", "a", "b"]]
        right = pd.concat([d.assign(bk=d["bk"] - 1), d])[["k", "bk", "t0", "t1", "a", "b"]]
        m = left.merge(right, on="bk", suffixes=("_i", "_j"))
        m = m[((m["t0_j"] > m["t0_i"]) | ((m["t0_j"] == m["t0_i"]) & (m["k_j"] > m["k_i"]))) & (m["t0_j"] < m["t1_i"])]
        m = m.drop_duplicates(["k_i", "k_j"])
        lo = m["t0_j"].to_numpy(float)
        hi = np.minimum(m["t1_i"].to_numpy(float), m["t1_j"].to_numpy(float))
        keep = hi > lo
        m, lo, hi = m[keep], lo[keep], hi[keep]

        def lev(p, t):
            a, b = m["a_" + p].to_numpy(float), m["b_" + p].to_numpy(float)
            t0, t1 = m["t0_" + p].to_numpy(float), m["t1_" + p].to_numpy(float)
            return a + (b - a) * (t - t0) / (t1 - t0)
        dlo, dhi = lev("i", lo) - lev("j", lo), lev("i", hi) - lev("j", hi)
        cross = dlo * dhi < 0
        tx = lo + (hi - lo) * np.where(cross, dlo / np.where(cross, dlo - dhi, 1), 0)
        out.append(pd.DataFrame({"sector": sec, "tx": tx[cross]}))
    return pd.concat(out, ignore_index=True)


def main(target, golden):
    reg = json.load(open(os.path.join(target, "sector_register.json")))
    tv = {s["traffic_volume"]: s["code"] for s in reg["sectors"]}
    name = {s["code"]: s["name"] for s in reg["sectors"]}
    code = {v: k for k, v in name.items()}
    fd = pd.read_parquet(os.path.join(target, "fdps_sector_traversals_2025-01_2026-09.parquet"))
    rec = pd.DataFrame({"sector": fd["sector"], "t0": secs(fd["entry_time_utc"]), "t1": secs(fd["exit_time_utc"]),
                        "a": fd["entry_fl"].astype(int), "b": fd["exit_fl"].astype(int), "ifplid": fd["ifplid"]})
    pl = pd.read_csv(os.path.join(target, "planning_traffic_summer2027_issue1.csv"))
    plan = pd.DataFrame({"sector": pl["tv"].map(tv), "t0": secs(pl["t_in"]), "t1": secs(pl["t_out"]),
                         "a": pl["fl_in"], "b": pl["fl_out"]})
    occ = pd.read_csv(os.path.join(target, "occurrence_export_2025-01_2026-09.csv"), dtype=str, keep_default_na=False)
    occ["ts"] = secs(occ["occurrence_date"] + " " + occ["time_utc"])
    occ["code"] = occ["sector"].map(code)
    atm = occ[(occ["occurrence_type"] == "SMI") & occ["atm_contribution"].isin(["D", "I"])]
    # the rate per pair, pooled over the record
    pr = pairs(rec)
    lo_all, hi_all = int(pd.Timestamp("2025-01-01", tz="UTC").timestamp()), int(pd.Timestamp("2026-10-01", tz="UTC").timestamp())
    pr = pr[(pr["tx"] >= lo_all) & (pr["tx"] < hi_all)]
    lam = len(atm) / len(pr)
    a27, b27 = local_season(2027)
    p27 = pairs(plan)
    p27 = p27[(p27["tx"] >= a27) & (p27["tx"] < b27)]
    c27 = p27.groupby("sector").size()
    fh27 = ((plan["t1"] - plan["t0"]) / 3600).groupby(plan["sector"]).sum()
    rate = {s: lam * c27[s] / fh27[s] * 1e5 for s in name}
    over = sorted(name[s] for s, v in rate.items() if v > 40.0)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    assert over == fig["sectors_over_tolerance"] == ["Tarvik"], over
    for s in name:
        assert "%.1f" % rate[s] == fig["forecast_rate_s27"][name[s]], (s, rate[s], fig["forecast_rate_s27"][name[s]])
        assert int(c27[s]) == fig["crossings_s27"][name[s]], s
    assert "%.2f" % (lam * 1e4) == fig["losses_per_10000_crossings"]
    print("verify: call Tarvik alone over 40.0 (%s); every forecast rate, pair count and the pooled rate reproduce" %
          ", ".join("%s %.1f" % (name[s], rate[s]) for s in name))
    # the summer 2026 close-out
    a26, b26 = local_season(2026)
    a25, b25 = local_season(2025)
    with pdfplumber.open(os.path.join(target, "HACC_summer2026_safety_closeout.pdf")) as pdf:
        text = "\n".join(pg.extract_text() or "" for pg in pdf.pages)
    for s in name:
        l26 = int(((atm["code"] == s) & (atm["ts"] >= a26) & (atm["ts"] < b26)).sum())
        l25 = int(((atm["code"] == s) & (atm["ts"] >= a25) & (atm["ts"] < b25)).sum())
        m = (rec["sector"] == s) & (rec["t0"] >= a26) & (rec["t0"] < b26)
        fh = float((rec["t1"][m] - rec["t0"][m]).sum()) / 3600
        row = re.search(r"^%s (\d+) (\d+) ([\d,]+) ([\d.]+)$" % name[s], text, re.M)
        assert row and (int(row.group(1)), int(row.group(2)), int(row.group(3).replace(",", "")), row.group(4)) == (
            l25, l26, round(fh), "%.1f" % (l26 / fh * 1e5)), (s, row.groups() if row else None)
    print("verify: the summer 2026 close-out reproduces from the record, every sector")
    # ask 1
    slots = pd.read_csv(os.path.join(target, "nm_slot_allocations_2026-05_2026-09.csv"), dtype={"ifplid": str})
    regs = pd.read_csv(os.path.join(target, "nm_regulations_2026-05_2026-09.csv")).drop_duplicates("regulation_id")
    rk = dict(zip(regs["regulation_id"], zip(regs["location_type"], regs["traffic_volume"])))
    insea = rec[(rec["t0"] >= a26) & (rec["t0"] < b26)]
    den = insea.groupby("sector")["ifplid"].nunique()
    fl = slots[slots["ifplid"].isin(set(rec["ifplid"]))]
    top = fl.loc[fl.groupby("ifplid")["slot_delay_min"].idxmax()]
    top = top.assign(kind=top["regulation_id"].map(lambda x: rk[x][0]),
                     sector=top["regulation_id"].map(lambda x: tv.get(rk[x][1])))
    top = top[top["kind"] == "En-route"]
    j = top.merge(insea[["ifplid", "sector"]], on=["ifplid", "sector"])
    num = j.groupby("sector")["slot_delay_min"].sum()
    delay = {s: float(num.get(s, 0)) / den[s] for s in name}
    for s in name:
        assert "%.2f" % delay[s] == fig["delay_per_flight_s26_min"][name[s]], (s, delay[s])
    print("verify: ask 1 delay per flight reproduces (%s)" % ", ".join("%s %.2f" % (name[s], delay[s]) for s in name))
    # ask 2
    log = pd.read_csv(os.path.join(target, "sector_configuration_log_2026-05_2026-09.csv"), keep_default_na=False)
    cur = pd.read_csv(os.path.join(target, "sector_configurations_current.csv"))
    alone9 = {k: {r for r in g["sectors"] if "+" not in r} for k, g in cur.groupby("configuration")}
    with pdfplumber.open(os.path.join(target, "HACC_OM_part3_ch4_sector_configuration.pdf")) as pdf:
        om = "\n".join(pg.extract_text() or "" for pg in pdf.pages)
    alone8 = {}
    for line in om.splitlines():
        mm = re.match(r"^(C8|C7A|C7B|C6A|C6B|C5|N3|N2) (\d) (.+)$", line.strip())
        if mm:
            alone8[mm.group(1)] = {code[x] for x in mm.group(3).split(", ") if "+" not in x}
    t = pd.to_datetime(log["log_time_local"])
    switch = t[log["remarks"].str.contains("revision 9")].iloc[0]
    s0, s1 = pd.Timestamp("2026-06-01"), pd.Timestamp("2026-09-01")
    hours = {s: 0.0 for s in name}
    nxt = list(t[1:]) + [pd.Timestamp("2026-10-01")]
    for k in range(len(t)):
        a_, b_ = max(t[k], s0), min(nxt[k], s1)
        if b_ > a_:
            for s in (alone9 if t[k] >= switch else alone8)[log["configuration"][k]]:
                hours[s] += (b_ - a_).total_seconds() / 3600
    for s in name:
        assert "%.1f" % hours[s] == fig["hours_open_alone_s26"][name[s]], (s, hours[s])
    print("verify: ask 2 hours open alone reproduce (%s)" % ", ".join("%s %.1f" % (name[s], hours[s]) for s in name))
    # ask 3
    ra = occ[(occ["occurrence_type"] == "ACAS RA") & (occ["ts"] >= a26) & (occ["ts"] < b26)].copy()
    ra["pair"] = [tuple(sorted(x)) for x in zip(ra["ac1_callsign"], ra["ac2_callsign"])]
    ra = ra.sort_values("ts")
    ra["gap"] = ra.groupby(["code", "pair"])["ts"].diff()
    enc = ra[ra["gap"].isna() | (ra["gap"] > 600)].groupby("code").size()
    for s in name:
        assert int(enc.get(s, 0)) == fig["acas_ra_encounters_s26"][name[s]], (s, enc.get(s, 0))
    print("verify: ask 3 encounters reproduce (%s)" % ", ".join("%s %d" % (name[s], enc.get(s, 0)) for s in name))
    # the goldens carry the same figures: the deck's forecast table and the measures CSV
    from pptx import Presentation
    prs = Presentation(os.path.join(golden, "summer2027_safety_forecast.pptx"))
    rows = {}
    for shape in prs.slides[1].shapes:
        if shape.has_table:
            tb = shape.table
            for r in range(1, len(tb.rows)):
                rows[tb.cell(r, 0).text] = tb.cell(r, 4).text
    assert all(rows[name[s]] == fig["forecast_rate_s27"][name[s]] for s in name), rows
    ms = pd.read_csv(os.path.join(golden, "summer2026_sector_measures.csv"), dtype=str)
    for r in ms.itertuples():
        assert r.enroute_atfm_delay_per_flight_min == fig["delay_per_flight_s26_min"][r.sector]
        assert r.hours_open_on_own == fig["hours_open_alone_s26"][r.sector]
        assert int(r.acas_ra_encounters) == fig["acas_ra_encounters_s26"][r.sector]
    print("verify: the deck and the measures file carry every figure")

if __name__ == "__main__":
    task = os.path.dirname(HERE)
    main(os.path.join(task, "target"), os.path.join(task, "golden"))
