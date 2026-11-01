"""The generator's assertions on the cut pack and the world's clean truth (task138, architecture 3).

    python3 task138/generator/checks.py
"""
import glob
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import io_util as IO  # noqa: E402
import pack as PK  # noqa: E402
import params as PR  # noqa: E402
import world as W  # noqa: E402

ROWS = []


def check(label, ok, detail=""):
    ROWS.append((label, bool(ok), detail))


def call_of(B, r, filed):
    rows = A.planning(B, r, filed)
    return [x["transfer"] for x in rows], [int(round(x["peak"])) for x in rows]


def edge_mw(x):
    return abs((x % 1.0) - 0.5)


def edge_block(x, firm=104.0, block=0.5):
    e = (x - firm) / block
    return abs(e - round(e)) * block


def main():
    S = A.solve(TARGET)
    f, wn, rr = S["filed"], S["wn"], S["relief"]
    loads, obs = S["loads"], S["obs"]
    gold = S["plans"]["golden"]
    G_TR = [x["transfer"] for x in gold]
    G_PK = [int(round(x["peak"])) for x in gold]
    P = rr["P"]
    hot = (P.tmax >= 99) & (P.hour >= 16) & (P.hour <= 20)

    # ------------------------------------------------------------- filed values read from the pack
    check("filed: Dunraith firm 104.0 MW, design 101 F, block 0.5 MW, threshold 85 F, base growth 0.95 per cent",
          (f.firm, f.design, f.block, f.threshold, round(f.growth, 4)) == (104.0, 101.0, 0.5, 85.0, 0.0095))
    check("filed: pilot feeders DUN-2, DUN-5, DUN-7 from the test plan", f.pilot == ["DUN-2", "DUN-5", "DUN-7"])

    # ------------------------------------------------------------- R block: the three rules on the clean truth
    n_scada = sum(1 for _ in open(os.path.join(TARGET, PK.FILES["scada_new"]))) - 1
    check("R1 raw material: hourly feeder loads for three summers in the new historian, 70,272 rows", n_scada == 70272,
          str(n_scada))
    heads = []
    for p in glob.glob(os.path.join(TARGET, "*.csv")):
        heads += open(p).readline().lower().split(",")
    check("R1 no shipped column holds the deciding quantity (relief, CVR factor, planning peak)",
          not any(w in h for h in heads for w in ("relief", "cvr_factor", "planning", "savings")))
    check("R1 the golden's relief reads pilot hours from the shipped rows (hot afternoons: %d CVR, %d normal)"
          % (rr["n_hot_on"], rr["n_hot_off"]), rr["n_hot_on"] >= 40 and rr["n_hot_off"] >= 40)

    # R3a: the analyst test on the world's clean truth (loads and temperatures before any file is written)
    Sw = W.simulate()
    ld, wx = Sw["ld"], Sw["wx"]
    tot = ld.groupby("local")["mw"].sum()
    dmax = tot.groupby(tot.index.normalize()).max()
    txw = wx.set_index("local")["temp_f"]
    t53 = []
    for yy in PR.SUMMERS:
        s_ = txw[txw.index.year == yy]
        v_ = s_.values
        t53.append(pd.Series(v_ + (np.append(v_[1:], v_[-1]) - v_) * 53 / 60.0, index=s_.index))
    t53 = pd.concat(t53)
    tmw = t53.groupby(t53.index.normalize()).max()
    dfw = pd.DataFrame({"L": dmax, "T": tmw}).dropna()
    hw = dfw[dfw["T"] >= 85]
    bw = np.polyfit(hw["T"], hw["L"], 1)
    Bw = float(np.polyval(bw, 101.0))
    p25 = ld[ld.local.dt.year == 2025]
    piv = p25.pivot(index="local", columns="feeder", values="mw")
    cvw = p25.pivot(index="local", columns="feeder", values="cvr")
    Rw = piv[f.pilot].sum(axis=1) / piv[f.comparison].sum(axis=1)
    onw, offw = cvw[f.pilot].all(axis=1), ~cvw[f.pilot].any(axis=1)
    win = pd.Series(piv.index >= pd.Timestamp(PR.PILOT_START), index=piv.index)
    TXw = pd.Series(tmw.reindex(piv.index.normalize()).values, index=piv.index)
    hrw = pd.Series(piv.index.hour, index=piv.index)

    def effw(m):
        return 1 - Rw[m & onw & win].mean() / Rw[m & offw & win].mean()
    e_all_w = effw(pd.Series(True, index=piv.index))
    e_hot_w = effw((TXw >= 99) & (hrw >= 16) & (hrw <= 20))
    d_tr, _ = call_of(Bw, e_all_w, f)
    g_tr, g_pk = call_of(Bw, e_hot_w, f)
    check("R3a analyst test on the clean truth: the pilot's all-hours relief (%.2f per cent) files %s, not the golden"
          % (100 * e_all_w, d_tr), d_tr != G_TR and d_tr[0] == 0.0)
    check("R3a the golden route on the clean truth files the golden transfers %s" % g_tr, g_tr == G_TR and g_pk == G_PK)
    tru = W.truth_relief_at_design()
    check("R3a the world's relief at the design afternoon (%.2f per cent) sits with the golden estimate (%.2f)"
          % (100 * tru, 100 * rr["golden"]), abs(tru - rr["golden"]) < 0.0015)
    # R3b: the decisive step alone
    one = call_of(wn["B"], rr["golden"], f)[0]
    check("R3b the default path with only the relief read at the planning peak's conditions files the golden",
          one == G_TR)
    check("R3b each lower rung's single correction stays wrong: no CVR %s, all hours %s, each day's peak hour %s"
          % (S["plans"]["R0_no_cvr"][0]["transfer"], S["plans"]["R1_all_hours"][0]["transfer"],
             S["plans"]["R2_daily_peak_hour"][0]["transfer"]),
          len({tuple(x["transfer"] for x in v) for v in S["plans"].values()}) == 4)
    # R3c: no plant
    docs_txt = " ".join(re.sub(r"\s+", " ", IO.pdf_text(p)) for p in sorted(glob.glob(os.path.join(TARGET, "*.pdf"))))
    check("R3c no shipped document states a voltage-cut effect or a CVR factor",
          not re.search(r"(per cent|%)[^.]{0,60}(reduc|saving|relief)|cvr factor|savings of", docs_txt, re.I))
    blocks = loads.dropna().round(3)
    day_sig = blocks.groupby(blocks.index.normalize()).apply(lambda x: hash(tuple(x.values.ravel()[:48])))
    check("R3c no day of the historian repeats another day's readings", day_sig.is_unique)

    # ------------------------------------------------------------- rungs and margins
    tr27 = {k: v[0]["transfer"] for k, v in S["plans"].items()}
    check("rungs: 2027 transfers no CVR 2.0, all hours 0.0, each day's peak hour 0.5, golden 1.0",
          tr27 == {"R0_no_cvr": 2.0, "R1_all_hours": 0.0, "R2_daily_peak_hour": 0.5, "golden": 1.0}, str(tr27))
    check("golden transfers 1.0 to 5.0 MW and planning peaks 105 to 109 MW",
          G_TR == [1.0, 2.0, 3.0, 4.0, 5.0] and G_PK == [105, 106, 107, 108, 109])
    m_pk = min(edge_mw(x["peak"]) for x in gold)
    m_bl = min(edge_block(x["peak"]) for x in gold)
    check("bin edges: every planning peak at least 0.15 MW from a half-MW edge (%.3f)" % m_pk, m_pk >= 0.15)
    check("bin edges: every excess at least 0.15 MW from a switching-block edge (%.3f)" % m_bl, m_bl >= 0.15)
    for k in ("R1_all_hours", "R2_daily_peak_hour"):
        m = min(edge_block(x["peak"]) for x in S["plans"][k])
        check("rung %s sits %.3f MW from a block edge in every summer" % (k, m), m >= 0.05)

    # ------------------------------------------------------------- the fork grid (SF rows)
    def same(B, r):
        return call_of(B, r, f) == (G_TR, G_PK)
    yrs = [d.year for d in S["days"].index]
    days_used = wn["top_days"]
    check("SF1 summer is June to September: the line reads only those months",
          set(pd.DatetimeIndex(days_used.index).month) <= {6, 7, 8, 9})
    lo = A.weather_normal(TARGET, f, loads, obs)
    check("SF2 the five most recent complete summers are 2022 to 2026, each in the line",
          set(loads.index.year) == {2022, 2023, 2024, 2025, 2026} and lo["n_days"] == wn["n_days"])
    wu = A.weather_normal(TARGET, f, loads, obs, clock="lst")
    Pu = A.pilot_frame(TARGET, f, loads, obs, clock="lst")
    ru = A.relief(Pu, (Pu.tmax >= 99) & (Pu.hour >= 16) & (Pu.hour <= 20))
    check("SF3 daily maximum by the export's standard-time day in the line and the hot-day pick: same call "
          "(%.2f MW, %.2f per cent)" % (wu["B"], 100 * ru), same(wu["B"], ru))
    ww = A.weather_normal(TARGET, f, loads, obs, whole_f=True)
    check("SF4 Celsius readings rounded to whole F before the line: same call (%.2f MW)" % ww["B"],
          same(ww["B"], rr["golden"]))
    lo2 = A.feeder_loads(TARGET, old_shift=False)
    w5 = A.weather_normal(TARGET, f, lo2, obs)
    check("SF5 the old historian's hour-ending labels read as hour-beginning: same call (%.2f MW)" % w5["B"],
          same(w5["B"], rr["golden"]))
    w6a = A.weather_normal(TARGET, f, loads, obs, drop_pilot_on=True)
    w6b = A.weather_normal(TARGET, f, loads, obs, add_back=rr["golden"])
    w6c = A.weather_normal(TARGET, f, loads, obs, add_back=rr["all_hours"])
    check("SF6 pilot CVR days in the line as run, dropped, or with the relief added back: same call "
          "(%.2f, %.2f, %.2f MW)" % (w6a["B"], w6b["B"], w6c["B"]),
          same(w6a["B"], rr["golden"]) and same(w6b["B"], rr["golden"]) and same(w6c["B"], rr["golden"]))
    crit = re.sub(r"\s+", " ", IO.pdf_text(os.path.join(TARGET, PK.FILES["criteria"])))
    check("SF7 the line stands for the middle summer of the five (filed)", "stands for the middle summer" in crit)
    check("SF8 growth compounded yearly (filed)", "compounded yearly" in crit)
    check("SF9 the base case growth rate (filed)", "base case growth rate" in crit)
    Ps = A.pilot_frame(TARGET, f, loads, obs, schedule=True)
    rs = A.relief(Ps, (Ps.tmax >= 99) & (Ps.hour >= 16) & (Ps.hour <= 20))
    check("SF10 CVR weeks from the test plan's schedule instead of the regulator log: same call (%.2f per cent)"
          % (100 * rs), same(wn["B"], rs))
    ev = A.switch_events(TARGET)
    idx = P.index
    s0 = np.all([A.feeder_state(ev, x, idx) for x in f.pilot], axis=0)
    P11 = P.copy()
    P11["on"] = s0
    P11["off"] = ~np.any([A.feeder_state(ev, x, idx) for x in f.pilot], axis=0)
    r11 = A.relief(P11, (P11.tmax >= 99) & (P11.hour >= 16) & (P11.hour <= 20))
    check("SF11 hours with a switch inside them counted by the setting at the hour's start: same call", same(wn["B"], r11))
    fam = {"days 99 F, 16:00-21:00": hot,
           "days 98 F, 17:00-21:00": (P.tmax >= 98) & (P.hour >= 17) & (P.hour <= 20),
           "days 100 F, 16:00-21:00": (P.tmax >= 100) & (P.hour >= 16) & (P.hour <= 20),
           "days 99 F, 15:00-22:00": (P.tmax >= 99) & (P.hour >= 15) & (P.hour <= 21),
           "hourly 98 F, 15:00-21:00": (P.t >= 98) & (P.hour >= 15) & (P.hour <= 20),
           "days 99 F, weekdays": hot & (P.dow < 5),
           "days 99 F, each day's peak hour": A.daily_peak_mask(P, loads) & (P.tmax >= 99)}
    vals = {k: A.relief(P, m) for k, m in fam.items()}
    check("SF12 the hot-afternoon window: every reading of the planning peak's conditions files the golden (%s)"
          % ", ".join("%.2f" % (100 * v) for v in vals.values()), all(same(wn["B"], v) for v in vals.values()))
    regs = []
    for thr in (85, 90, 95):
        m = (P.tmax >= thr) & (P.hour >= 16) & (P.hour <= 20) & (P.on | P.off)
        X = np.column_stack([np.ones(m.sum()), P.on[m].astype(float), P.tmax[m], P.on[m].astype(float) * P.tmax[m]])
        cc = np.linalg.lstsq(X, (P.pil / P.com)[m].values, rcond=None)[0]
        regs.append(-(cc[1] + 101 * cc[3]) / (cc[0] + 101 * cc[2]))
    dr = (P.pil / P.com)[hot]
    dd = dr.groupby(dr.index.normalize()).mean()
    on_d = P.on[hot].groupby(P.on[hot].index.normalize()).mean() > 0.5
    r_days = 1 - dd[on_d].mean() / dd[~on_d].mean()
    check("SF13 relief as a line in the day's maximum read at 101 F (%s) or a mean of daily ratios (%.2f): same call"
          % (", ".join("%.2f" % (100 * x) for x in regs), 100 * r_days),
          all(same(wn["B"], x) for x in regs) and same(wn["B"], r_days))
    rounded = [max(0.0, np.ceil(round((p - f.firm) / f.block, 9)) * f.block) for p in G_PK]
    check("SF14 the transfer worked from the planning peak rounded to the nearest MW: same transfers", rounded == G_TR)
    plan = re.sub(r"\s+", " ", IO.pdf_text(os.path.join(TARGET, PK.FILES["opplan"])))
    check("SF15 CVR runs on every Dunraith feeder from 1 June 2027, at all hours (filed in the operating plan)",
          "every Dunraith feeder from 1 June 2027, at all hours" in plan)
    filled = loads.copy().ffill()
    w16 = A.weather_normal(TARGET, f, filled, obs)
    P16 = A.pilot_frame(TARGET, f, filled, obs)
    r16 = A.relief(P16, (P16.tmax >= 99) & (P16.hour >= 16) & (P16.hour <= 20))
    check("SF16 Bad hours filled from the hour before instead of left out: same call", same(w16["B"], r16))
    o17 = obs[obs.kind == "FM-15"]
    w17 = A.weather_normal(TARGET, f, loads, o17)
    check("SF17 routine observations only: same call", same(w17["B"], rr["golden"]))
    e = S["energy"]
    e18 = A.feeder_energy(TARGET, prorate_june30=True)
    check("SF18 Ask A: the minutes after 23:27 on 30 June pro-rated to the new feeders: same figures",
          [round(x, -1) for x in e18] == [round(x, -1) for x in e])
    days, eleventh = A.hottest_days(TARGET, obs=obs)
    days_u, _ = A.hottest_days(TARGET, clock="lst", obs=obs)
    check("SF19 Ask B: the tenth hottest day stands %.2f F above the eleventh, and standard-time days pick the same ten"
          % (days.iloc[-1] - eleventh), days.iloc[-1] - eleventh >= 0.3 and set(days.index) == set(days_u.index))
    pk = S["peaks"]
    pk20 = A.demand_peaks(TARGET, days, ending=False)
    check("SF20 Ask B: each day's peak falls in the evening, so the day an interval ending at midnight belongs to "
          "never matters", all(16 <= t.hour <= 21 for _, t in pk.values()) and
          all(round(pk20[d][0], 1) == round(pk[d][0], 1) for d in days.index))
    mv = A.mv90(TARGET)
    est = mv[mv.STATUS.fillna("") == "E"]
    est_local = est["end"] - A.CDT
    check("SF21 Ask B: the supplier's estimated intervals sit overnight, away from every hot day's peak",
          len(est) > 0 and est_local.dt.hour.between(0, 5).all() and
          not set(est_local.dt.normalize()) & set(days.index))
    tx_reg, dev = A.register(TARGET)
    md = pd.read_csv(os.path.join(TARGET, PK.FILES["mdms"]))
    md["date"] = pd.to_datetime(md.READ_DATE, format="%m/%d/%Y")
    up = tx_reg[(pd.to_datetime(tx_reg.METER_SET) >= pd.Timestamp("2026-06-01")) & (tx_reg.METER_MULT == 20)]
    ok22 = len(up) == 3
    for t, sd in zip(up.XFMR_ID, pd.to_datetime(up.METER_SET)):
        s_ = md[md.XFMR_ID == t].set_index("date").KWH
        ok22 &= s_.loc[sd] < s_.loc[sd - pd.Timedelta(days=1)] / 10
    check("SF22 Ask A: on each meter set in June on CT metering the day's kWh falls twentyfold on the set day itself",
          ok22)

    # ------------------------------------------------------------- Layer 1 neutrality (R2), one per item
    check("R2 mess: old historian in kW labelled at the hour's end (SF5) leaves the call", same(w5["B"], rr["golden"]))
    check("R2 mess: airport clock in local standard time (SF3) leaves the call", same(wu["B"], ru))
    check("R2 mess: airport readings in Celsius (SF4) leave the call", same(ww["B"], rr["golden"]))
    check("R2 mess: a late and a missed pilot switch (SF10) leave the call", same(wn["B"], rs))
    check("R2 mess: overnight Bad hours (SF16) leave the call", same(w16["B"], r16))
    check("R2 mess: special observations (SF17) leave the call", same(w17["B"], rr["golden"]))

    # ------------------------------------------------------------- asks: devices bite, truth reproduced, margins
    r10 = lambda x: int(round(x / 10.0)) * 10  # noqa: E731
    G_A = [r10(x) for x in e]
    nr = [r10(x) for x in A.feeder_energy(TARGET, reassign=False)]
    sh = [r10(x) for x in A.feeder_energy(TARGET, depth=1)]
    me = [r10(x) for x in A.feeder_energy(TARGET, mult_from_set=False)]
    nm = [r10(x) for x in A.feeder_energy(TARGET, use_mult=False)]
    moved_idx = [PR.FEEDERS.index(x) for x in ("DUN-1", "DUN-2", "DUN-3", "DUN-4", "DUN-6", "DUN-8")]
    check("Ask A device: feeder labels taken as recorded move every feeder the reconfiguration touched",
          all(nr[i] != G_A[i] for i in moved_idx))
    check("Ask A device: tracing only one level below the opened switches moves the same feeders",
          all(sh[i] != G_A[i] for i in moved_idx))
    check("Ask A device: the register's multiplier on every day moves DUN-5 and DUN-7",
          me[4] != G_A[4] and me[6] != G_A[6])
    check("Ask A hazard: no multiplier moves every feeder", all(a != b for a, b in zip(nm, G_A)))
    truth_e = Sw["mdms"].merge(Sw["tx"][["tx"]], on="tx")
    t_feed = []
    tx_w = Sw["tx"].set_index("tx")
    for x in PR.FEEDERS:
        sel = truth_e[((truth_e.date < W.RECONFIG_DATE.normalize()) &
                       (truth_e.tx.map(tx_w.feeder_built) == x)) |
                      ((truth_e.date >= W.RECONFIG_DATE.normalize()) & (truth_e.tx.map(tx_w.feeder_now) == x))]
        t_feed.append(sel.kwh_true.sum() / 1000.0)
    check("Ask A truth: the golden reproduces the world's energy by feeder within 0.5 MWh",
          max(abs(a - b) for a, b in zip(t_feed, e)) < 0.5)
    m_a = min(abs((x % 10) - 5) for x in e)
    check("Ask A bin edges: every feeder at least 1.0 MWh from a rounding edge (%.2f)" % m_a, m_a >= 1.0)
    G_B = [round(pk[d][0], 1) for d in days.index]

    def kept(dd_):
        return sum(round(dd_[d][0], 1) == g for d, g in zip(days.index, G_B))
    k_nr = kept(A.demand_peaks(TARGET, days, realign=False, dedupe=True))
    k_gr = kept(A.demand_peaks(TARGET, days, meters=("41-2207", "41-2208", "41-2391")))
    k_ut = kept(A.demand_peaks(TARGET, days, clock="utc"))
    check("Ask B device: the T2 recorder's stamps left as written keep %d of 10" % k_nr, k_nr == 0)
    check("Ask B hazard: the 69 kV line terminal summed in keeps %d of 10" % k_gr, k_gr == 0)
    check("Ask B hazard: UTC days keep %d of 10" % k_ut, k_ut <= 6)
    gt = Sw["gt"][Sw["gt"].meter.isin(["41-2207", "41-2208"])].copy()
    gt["kwh"] = gt.kwh.round(1)
    q = gt.groupby("end_utc_true")["kwh"].sum() * 4 / 1000.0
    st = q.index - pd.Timedelta(hours=5) - pd.Timedelta(minutes=15)
    qs = pd.Series(q.values, index=st)
    tpk = qs.groupby(qs.index.normalize()).max()
    check("Ask B truth: the golden reproduces the world's ten daily peaks", [round(tpk[d], 1) for d in days.index] == G_B)
    m_b = min(abs(((pk[d][0] * 10) % 1) - 0.5) / 10 for d in days.index)
    check("Ask B bin edges: every peak at least 0.01 MW from a rounding edge (%.3f)" % m_b, m_b >= 0.01)

    # ------------------------------------------------------------- separation line and distractors
    tmp = tempfile.mkdtemp()
    for fn in os.listdir(TARGET):
        if fn not in (PK.FILES["mdms"], PK.FILES["register"], PK.FILES["so"], PK.FILES["mv90"], PK.FILES["dpsched"]):
            shutil.copy(os.path.join(TARGET, fn), tmp)
    f2 = A.Filed(tmp)
    l2, o2 = A.feeder_loads(tmp), A.observations(tmp)
    w2 = A.weather_normal(tmp, f2, l2, o2)
    r2 = A.relief_rungs(tmp, f2, l2, o2)["golden"]
    check("separation: the call computes with every ask-only file deleted", call_of(w2["B"], r2, f2) == (G_TR, G_PK))
    shutil.rmtree(tmp)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    tmp = tempfile.mkdtemp()
    for fn in os.listdir(TARGET):
        if fn not in meta["distractor_files"]:
            shutil.copy(os.path.join(TARGET, fn), tmp)
    S3 = A.solve(tmp)
    same_all = ([x["transfer"] for x in S3["plans"]["golden"]] == G_TR and
                [r10(x) for x in S3["energy"]] == G_A and
                [round(S3["peaks"][d][0], 1) for d in days.index] == G_B)
    check("distractors: deleting %s leaves the call and every ask" % ", ".join(meta["distractor_files"]), same_all)
    shutil.rmtree(tmp)

    # ------------------------------------------------------------- input gates and realism sweep
    files = sorted(os.listdir(TARGET))
    check("input gate: 10 or more files (%d)" % len(files), len(files) >= 10)
    check("input gate: 3 or more formats", len({os.path.splitext(x)[1] for x in files}) >= 3)
    check("input gate: a file of 25,000 rows or more (%s)" % meta["largest_file"]["name"],
          meta["largest_file"]["rows"] >= 25000)
    check("input gate: two or more distractors named in metadata.json", len(meta["distractor_files"]) >= 2)
    check("input gate: every file carries source, date and licence",
          all(set(v) >= {"source", "date", "license"} for v in meta["files"].values()) and
          set(meta["files"]) == set(files))
    check("realism: no file name says test, trap, decoy, distractor, answer, golden or readme",
          not any(re.search(r"test_|trap|decoy|distract|answer|golden|readme", x, re.I) for x in files))
    em = False
    for p in glob.glob(os.path.join(TARGET, "*")):
        if p.endswith(".pdf"):
            em |= "—" in IO.pdf_text(p)
        elif p.endswith(".csv"):
            em |= "—" in open(p, encoding="utf-8").read()
    check("realism: no em dash in any shipped text", not em)
    pdf_ok, dates_ok = True, True
    for p in glob.glob(os.path.join(TARGET, "*.pdf")):
        raw = open(p, "rb").read()
        pdf_ok &= b"ReportLab" not in raw
        for d in re.findall(rb"/(?:CreationDate|ModDate) \(D:(\d{8})", raw):
            dates_ok &= d.decode() <= PR.AS_OF.replace("-", "")
    check("realism: PDFs carry no toolkit signature", pdf_ok)
    for p in glob.glob(os.path.join(TARGET, "*.xlsx")):
        core = zipfile.ZipFile(p).read("docProps/core.xml").decode()
        for d in re.findall(r"<dcterms:\w+ [^>]*>(\d{4}-\d{2}-\d{2})", core):
            dates_ok &= d <= PR.AS_OF
        dates_ok &= "openpyxl" not in core
    check("realism: every document dated on or before the review (%s)" % PR.AS_OF, dates_ok)
    last = max(pd.to_datetime(pd.read_csv(os.path.join(TARGET, PK.FILES["outages"])).START_LOCAL))
    check("realism: no record after the review date", last <= pd.Timestamp(PR.AS_OF) and
          obs.local.max() < pd.Timestamp("2026-10-01"))
    check("PDF positive control: every shipped PDF yields text through the shared extractor",
          all(len(IO.pdf_text(p)) > 300 for p in glob.glob(os.path.join(TARGET, "*.pdf"))))

    # ------------------------------------------------------------- goldens agree with figures.json
    F = json.load(open(os.path.join(HERE, "figures.json")))
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(TASK, "golden", "dunraith_planning.xlsx"), read_only=True)
    cr = [r for r in wb["Capacity review"].iter_rows(min_row=5, max_row=9, values_only=True)]
    check("golden workbook: transfers and planning peaks equal figures.json",
          [r[6] for r in cr] == G_TR and [r[3] for r in cr] == G_PK)
    fe = {r[0]: r[1] for r in wb["Feeder energy 2026"].iter_rows(min_row=4, max_row=11, values_only=True)}
    check("golden workbook: feeder energy equals figures.json", fe == F["feeder_energy_mwh"])
    hd = {r[0]: r[2] for r in wb["Hottest days 2026"].iter_rows(min_row=4, max_row=13, values_only=True)}
    check("golden workbook: hot-day peaks equal figures.json", hd == {k: v["peak_mw"] for k, v in F["hot_days"].items()})
    zb = zipfile.ZipFile(os.path.join(TASK, "golden", "dunraith_planning.xlsx"))
    check("golden workbook carries its chart sheet of planning peaks against the firm rating",
          any(n.startswith("xl/charts/chart") for n in zb.namelist()) and "Chart" in wb.sheetnames)

    bad = [r for r in ROWS if not r[1]]
    for label, ok, detail in ROWS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [%s]" % detail) if detail and not ok else ""))
    print("%d assertions, %d failed" % (len(ROWS), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
