"""task501 build: data, documents, assertions, golden figures. Run from the generator folder."""
import json
import os
import subprocess
import sys
import time
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
import build_data
import docs
import solve
import pack as _pack

A = []


def ok(cond, msg):
    A.append((bool(cond), msg))
    if not cond:
        print("ASSERT FAIL:", msg)


def off_thousand(v):
    return abs(v / 1000 - round(v / 1000)) > 0.01 or abs(v) < 1


def main():
    t0 = time.time()
    funds, fx, cells, counts = build_data.run()
    p = solve.Pack()
    br_h1 = docs.write_all(counts, p)
    scrub = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "scrub_producer_metadata.py")
    subprocess.run([sys.executable, scrub, solve.T, "--apply", "--producer", "Pensionskasse Werdinsel", "--stamp", "2026-10-01", "--floor", "2024-11-01", "--ceiling", "2026-10-02"], check=True, capture_output=True)
    for f in ("fondsregister_2026-09-30.xlsx", "kapitalkonten_revidiert_2021-2025.xlsx", "richtlinie_liquiditaet_privatmarkt_RL-PM-04.docx"):
        _pack.fix_zip_times(os.path.join(solve.T, f))
    docs.write_manifest(counts)
    stamp = time.mktime((2026, 10, 1, 7, 40, 0, 0, 0, -1))
    for f in os.listdir(solve.T):
        os.utime(os.path.join(solve.T, f), (stamp, stamp))
    R = solve.RESERVE
    v = solve.Validation(p)
    # ---------------------------------------------------------------- the validation: honest and leaky
    WF = v.run("walk_forward")
    FW = v.run("full_window")
    IS = v.run("in_sample")
    m = lambda res, c: res["candidates"][c]["mape"]
    ok(WF["winner"] == "band", "walk-forward selects the band basis")
    ok(m(WF, "band") < 0.9 * m(WF, "strategy_band"), f"walk-forward: band {m(WF,'band'):.4f} beats strategy band {m(WF,'strategy_band'):.4f} by more than 10 per cent")
    ok(m(WF, "band") < 0.6 * m(WF, "fund_own"), f"walk-forward: band beats the manager basis {m(WF,'fund_own'):.4f} by more than 40 per cent")
    ok(FW["winner"] == "fund_own" and IS["winner"] == "fund_own", "fitting once on the whole window, or in sample, crowns the manager basis")
    ok(m(FW, "fund_own") < 0.7 * min(m(FW, "band"), m(FW, "strategy_band")), f"full-window: manager basis {m(FW,'fund_own'):.4f} beats the pooled bases {m(FW,'band'):.4f} / {m(FW,'strategy_band'):.4f} by more than 30 per cent")
    for c, d in WF["candidates"].items():      # the graded test table: the walk-forward figures
        pct = d["mape"] * 100
        ok(abs(pct * 10 - round(pct * 10)) > 0.08, f"walk-forward {c} test error {pct:.3f} not on a one-decimal boundary")
        for F in d["forecasts"]:
            ok(off_thousand(F), f"walk-forward {c} forecast {F:.0f} off a thousand boundary")
    for Aact in WF["actual"]:
        ok(off_thousand(Aact), f"actual {Aact:.0f} off a thousand boundary")
    # ---------------------------------------------------------------- the answer and the ladder
    b_wf = WF["candidates"]
    b_fw = FW["candidates"]
    T, _ = solve.main_call(p, v)
    WX = v.run("walk_forward_exclusive")
    ok(WX["winner"] == "band", "estimating up to the month before the origin (the other reading of s.5.3) selects the same basis")
    fx_excl = solve.facility(p, v, "band", WX["candidates"]["band"]["buffer"])
    ok(fx_excl["tranche"] == T["tranche"], f"the exclusive-origin reading lands on the same tranche (required {fx_excl['required']/1e6:.2f})")
    ok(all(p.first_call[fid] >= p.reg.loc[fid, "admission_date"] for fid in p.first_call), "no fund has a first call before its admission date (population reading convergent)")
    ok(T["tranche"] == 225, f"answer tranche {T['tranche']} is CHF 225m")
    ok(T["below"] == 200, "tranche below is 200")
    ok(min(abs(T["required"] - 200e6), abs(T["required"] - 225e6)) >= 9e6, f"answer required {T['required']/1e6:.3f} at least 9m inside its bin")
    ok(b_wf["band"]["buffer"] - b_wf["band"]["buffer_total"] >= 30e6, f"path buffer {b_wf['band']['buffer']/1e6:.1f} exceeds the end-of-horizon reading {b_wf['band']['buffer_total']/1e6:.1f} by 30m or more")
    ok(T["peak_month"] == 12, "peak month is December 2027")
    ok(all(r["net"] > 0 for r in T["facility"]), "net outflow positive in every facility month")
    ladder = {
        "R0_manager_no_buffer": (solve.facility(p, v, "fund_own", 0.0), 175, "no test run, the richest basis taken (the CIO's belief)"),
        "R1_full_window_manager_total": (solve.facility(p, v, "fund_own", b_fw["fund_own"]["buffer_total"]), 200, "rates fitted once on the whole window and scored on the past, the manager basis wins, buffer read at the end of each horizon"),
        "R1p_full_window_manager_path": (solve.facility(p, v, "fund_own", b_fw["fund_own"]["buffer"]), 250, "rates fitted once on the whole window, buffer on the path"),
        "R2_band_end_of_horizon": (solve.facility(p, v, "band", b_wf["band"]["buffer_total"]), 200, "the test run as filed, the buffer read at the end of each horizon instead of at any point (s.5.6)"),
        "band_no_buffer": (solve.facility(p, v, "band", 0.0), 125, "s.5.6 ignored"),
        "strategy_no_buffer": (solve.facility(p, v, "strategy_band", 0.0), None, "s.5.3 and s.5.6 ignored"),
        "strategy_path": (solve.facility(p, v, "strategy_band", b_wf["strategy_band"]["buffer"]), None, "s.5.3 selection misapplied (the runner-up basis, 24 per cent behind), buffer on the path"),
        "strategy_end_of_horizon": (solve.facility(p, v, "strategy_band", b_wf["strategy_band"]["buffer_total"]), None, "s.5.3 and s.5.6"),
        "band_leaky_total": (solve.facility(p, v, "band", b_fw["band"]["buffer_total"]), 175, "right basis, buffer from a full-window fit at the end of the horizon"),
        "in_sample_manager_total": (solve.facility(p, v, "fund_own", IS["candidates"]["fund_own"]["buffer_total"]), None, "rates fitted through each horizon (s.5.3)"),
        "reserve_ignored": (solve.facility(p, v, "band", b_wf["band"]["buffer"], reserve=0.0), None, "s.3, s.4"),
        "haircut_50": (solve.facility(p, v, "band", b_wf["band"]["buffer"], haircut=0.5), None, "s.4 one quarter"),
    }
    for k, (f, expect, rule) in ladder.items():
        if expect is not None:
            ok(f["tranche"] == expect, f"cell {k} lands on {f['tranche']} (expected {expect}), required {f['required']/1e6:.2f}")
        if k not in ("strategy_path", "strategy_end_of_horizon"):
            ok(f["tranche"] != 225, f"cell {k} off the answer tranche")
    for k in ("R1_full_window_manager_total", "R1p_full_window_manager_path", "R2_band_end_of_horizon", "band_no_buffer"):
        f = ladder[k][0]
        ok(min(abs(f["required"] - e * 1e6) for e in (200, 225)) >= 4.0e6, f"cell {k} required {f['required']/1e6:.2f} at least 4m from the answer bin's edges")
    # month figures off thousand boundaries; November clearance
    for r in T["facility"]:
        for kk in ("calls", "dists", "credited", "net", "cum"):
            ok(off_thousand(r[kk]), f"month {r['month']} {kk} off a thousand boundary")
    ok(off_thousand(T["buffer"]) and off_thousand(T["uncovered_below"]) and off_thousand(T["peak"]), "buffer, uncovered and peak off thousand boundaries")
    fp = T["first_past_below"]
    ok(fp is not None, "the plan passes the lower tranche inside the facility year")
    # ---------------------------------------------------------------- the ledger basis agrees to the audited cells (s.6.2, layer 1)
    aud = p.aud
    def misses(**kw):
        n = 0
        for _, a in aud.iterrows():
            C = a["commitment"]; fid = a["fund_id"]; fy = a["fy_end"]
            u = C - p.calls_to(fid, upto=fy) if kw.get("construction") == "naive" else C - p.calls_to(fid, upto=fy) + p.recallable(fid, upto=fy, **kw)
            if abs(u - a["unfunded_commitment"]) > 0.5:
                n += 1
        return n
    n_rule, n_naive = misses(), misses(construction="naive")
    ok(n_rule == 0, "the filed recycling term agrees the ledger basis to every audited cell")
    ok(n_naive >= 10, f"commitment less calls misses {n_naive} audited cells (the term is doing work)")
    inv = p.inv[p.inv["realisation_date"].notna()]
    holds = [(r - i).days for i, r in zip(inv["initial_investment_date"], inv["realisation_date"])]
    ok(all(not (515 <= h <= 585) for h in holds), "no realised hold within 515 to 585 days (every reading of 18 months agrees)")
    ok(all(p.calls_to(fid) <= p.reg.loc[fid, "commitment"] + 0.01 for fid in p.reg.index), "cumulative calls never exceed commitment")
    # ---------------------------------------------------------------- ask B and C (unchanged devices)
    B = p.nav_bridge()
    Bl = p.nav_bridge(fx_basis="booked", absent="skip")
    Bc = p.nav_bridge(absent="carry")
    Bs = p.nav_bridge(absent="skip")
    Bn = p.nav_bridge(flow_date="notice_date")
    for s in ("BO", "GR", "PC", "IN", "TOTAL"):
        ok(abs(B[s]["closing"] - Bl[s]["closing"]) > 5e5, f"ask B {s}: booked-rate closing differs from period-end closing by more than 0.5m")
        for k, vv in B[s].items():
            ok(off_thousand(vv), f"ask B {s} {k} off a thousand boundary")
    ok(all(abs(B[s]["closing"] - Bc[s]["closing"]) > 2e5 for s in ("BO", "PC", "IN")), "ask B: carrying the Q1 statement unadjusted moves BO, PC and IN")
    ok(all(abs(B[s]["closing"] - Bs[s]["closing"]) > 5e6 for s in ("BO", "PC", "IN")), "ask B: skipping the absent statements moves BO, PC and IN by more than 5m")
    ok(abs(B["TOTAL"]["dists"] - Bn["TOTAL"]["dists"]) > 1e6, "ask B: notice-date attribution of flows moves distributions")
    C, Cs = p.cash_2026()
    Cl, _ = p.cash_2026(date_col="notice_date", fx_col="notice_date", cash_only=False)
    for mth in C:
        ok(abs(C[mth]["calls"] - Cl[mth]["calls"]) > 1e5 or abs(C[mth]["dists"] - Cl[mth]["dists"]) > 1e5, f"ask C month {mth}: notice-basis differs from value-date basis")
        for k in ("calls", "dists", "net"):
            ok(off_thousand(C[mth][k]), f"ask C month {mth} {k} off a thousand boundary")
    ok(p.spine[(p.spine["line_type"] == "IN_KIND") & (p.spine["value_date"] >= date(2026, 1, 1))].shape[0] == 1, "one in-specie distribution inside the 2026 cash window")
    ok(p.spine[(p.spine["status"] == "CANCELLED") & (p.spine["notice_date"] >= date(2026, 1, 1))]["notice_id"].nunique() == 3, "three withdrawn notices in 2026")
    # ---------------------------------------------------------------- input gates
    files = [f for f in os.listdir(solve.T) if not f.startswith(".")]
    ok(len(files) >= 10, f"{len(files)} files")
    ok(len({f.rsplit('.', 1)[-1] for f in files}) >= 4, "4+ formats")
    ok(len(p.spine) > 10000, f"spine rows {len(p.spine)}")
    # ---------------------------------------------------------------- golden figures
    fee = 0.0045
    gold = dict(
        tranche=T["tranche"], below=T["below"], required=T["required"], peak=T["peak"], buffer=T["buffer"], buffer_share=T["buffer_share"], calls27=T["calls27"],
        uncovered_below=T["uncovered_below"], first_past_below=fp, peak_month=T["peak_month"], reserve=R,
        fee_sel=T["tranche"] * 1e6 * fee, fee_below=T["below"] * 1e6 * fee, buffer_total=b_wf["band"]["buffer_total"],
        months=[dict(year=r["year"], month=r["month"], calls=r["calls"], dists=r["dists"], credited=r["credited"], net=r["net"], cum=r["cum"]) for r in T["facility"]],
        validation=dict(origins=solve.ORIGINS, actual=WF["actual"], winner=WF["winner"],
                        candidates={c: dict(forecasts=d["forecasts"], mape=d["mape"], path_gaps=d["path_gaps"], total_gaps=d["total_gaps"], buffer=d["buffer"], buffer_total=d["buffer_total"]) for c, d in WF["candidates"].items()}),
        leaky=dict(full_window=dict(winner=FW["winner"], mape={c: d["mape"] for c, d in FW["candidates"].items()}, buffer={c: d["buffer"] for c, d in FW["candidates"].items()}, buffer_total={c: d["buffer_total"] for c, d in FW["candidates"].items()}),
                   in_sample=dict(winner=IS["winner"], mape={c: d["mape"] for c, d in IS["candidates"].items()})),
        ladder={k: dict(required=f["required"], tranche=f["tranche"], violates=rule, calls27=f["calls27"], buffer=f["buffer"]) for k, (f, e, rule) in ladder.items()},
        bridge=B, cash=C, cash_by_strategy=Cs, h1_2025=br_h1, audited_rule_misses=n_rule, audited_naive_misses=n_naive,
        unfunded_total_true=sum(max(0.0, p.unfunded(fid, "true")) * p.fx_rate(solve.PLAN_DATE, p.reg.loc[fid, "currency"]) for fid in p.reg.index),
    )
    with open(os.path.join(HERE, "golden_figures.json"), "w") as fh:
        json.dump(gold, fh, indent=1, default=str)
    nfail = sum(1 for c, _ in A if not c)
    print(f"assertions {len(A)}, failed {nfail}, {time.time()-t0:.1f}s")
    print("answer: tranche", T["tranche"], "required %.3f peak %.3f buffer %.3f (end-of-horizon %.3f) calls27 %.3f" % (T["required"] / 1e6, T["peak"] / 1e6, T["buffer"] / 1e6, b_wf["band"]["buffer_total"] / 1e6, T["calls27"] / 1e6))
    print("walk-forward mape", {c: round(d["mape"], 4) for c, d in WF["candidates"].items()}, "| full-window", {c: round(d["mape"], 4) for c, d in FW["candidates"].items()})
    print("ladder:", {k: (round(f["required"] / 1e6, 1), f["tranche"]) for k, (f, e, rule) in ladder.items()})
    return nfail


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
