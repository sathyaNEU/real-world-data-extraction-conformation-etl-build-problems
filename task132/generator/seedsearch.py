"""Search world seeds for a draw whose ladder separates cleanly; prints one JSON line per seed.

    python3 seedsearch.py FIRST LAST [WORKERS]
"""
import datetime as dt
import json
import os
import sys
import tempfile
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W

KEYS = ["window_no_renewal", "install_renewal", "install_no_renewal", "relay_age_window_no_renewal", "trailing_rate",
        "station_first_stage", "station_last_stage", "plan_2025", "all_psu_wos", "window_hold_band_no_renewal",
        "window_hold_band_renewal", "module_rates_relay_ageing_no_renewal", "no_programme", "pooled_window"]


def score(sd):
    import build as B
    import estimators as E
    import openpyxl
    import pandas as pd
    W.SEED = sd
    W.TUNE = ()
    tmp = os.path.join(tempfile.gettempdir(), "seedsearch_%d" % os.getpid())
    B.build(tmp, docs=False)
    s = E.solve(tmp)
    r, avail = E.rungs(tmp)
    lam, L = s["lam"], s["lots"]
    lo, hi = lam, lam
    while E.lots_needed(lo, avail) == L:
        lo -= 0.05
    while E.lots_needed(hi, avail) == L:
        hi += 0.05
    reg, wo, hist, subs, stock, plan = E.load(tmp)
    fl = E.fleet(reg)
    in25 = E.in_service_jan1(fl, plan["2025 plan (superseded)"])
    p26 = plan["Approved 2026"]
    first = {sub: min((w or E.month_add(W.PROGRAMME_END, 1)) for _, w in rows) for sub, rows in p26.items()}
    live = fl[fl["status"] == "IN SERVICE"]
    by_st = {y: int(sum(1 for sub in live["sub_code"] if sub in first and first[sub] > dt.date(y, 1, 1))) for y in range(2027, 2036)}
    # repaired modules that failed within months of refit, and those Veldtek saw again
    rows = list(openpyxl.load_workbook(os.path.join(tmp, "veldtek_rma_log_vpr340_psu.xlsx")).active.iter_rows(min_row=2, values_only=True))
    back = {}
    for x in rows:
        if x[7] is not None:
            back.setdefault(x[2], []).append(x[7].date())
    early = again = 0
    seen = {}
    for x in rows:
        seen[x[2]] = seen.get(x[2], 0) + 1
    for sn, fit, rem, why in zip(hist["serial_no"], hist["fitted"], hist["removed"], hist["removal_reason"]):
        if why == "FAILED" and any(b < fit for b in back.get(sn, [])) and (rem - fit).days < 200:
            early += 1
            again += seen.get(sn, 0) >= 2
    young = sum(1 for a in E.failures(wo, fl, hist)["age"] if a < 6)
    out = dict(seed=sd, lam=round(lam, 2), lots=L, avail=avail, open=s["at_repair"], lo=round(100 * (lam - lo) / lam, 2),
               hi=round(100 * (hi - lam) / lam, 2), counts=[int(c) for c in s["counts"]], young=young, early=early,
               again=again, diff25=sum(in25[y] != s["in_service"][y] for y in in25),
               diffst=sum(by_st[y] != s["in_service"][y] for y in by_st),
               rungs={k: [round(r[k][0], 1), r[k][1]] for k in KEYS})
    gap = r["window_no_renewal"][1] - L
    clash = [k for k in KEYS if r[k][1] == L]
    out["ok"] = (gap >= 4 and r["window_no_renewal"][0] >= 1.25 * lam and not clash and out["lo"] >= 3 and out["hi"] >= 3
                 and r["install_renewal"][0] <= 0.88 * lam and r["relay_age_window_no_renewal"][0] <= 0.88 * lam
                 and r["trailing_rate"][0] <= 0.80 * lam and out["diff25"] >= 6 and out["diffst"] >= 5 and again >= 1)
    out["ok"], out["gap"], out["clash"] = bool(out["ok"]), int(gap), clash
    out["again"] = int(again)
    return out


def main(first, last, workers=4):
    with Pool(workers) as pool:
        for o in pool.imap(score, range(first, last)):
            print(json.dumps(o), flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 4)
