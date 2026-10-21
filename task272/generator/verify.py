"""Independent verifier: recomputes the call and both asks from target/ alone with code that shares nothing with
analysis.py, pack.py or models.py (pandas readers, vectorised pair counts, a Monte Carlo reordering of every working day
in place of the closed-form benchmark), and compares them with generator/figures.json."""
import decimal
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SYSTEM = {"FA_PRESUMPTIVE", "BATCHPE", "PE-AUTOSCREEN"}


def load(target):
    f = {x: os.path.join(target, x) for x in os.listdir(target)}
    find = lambda stem: next(v for k, v in f.items() if k.startswith(stem))
    p = pd.read_csv(find("fac_determinations_2025_puget"), dtype=str, keep_default_na=False)
    w = pd.read_csv(find("fac_determinations_2025_willamette"), dtype=str, keep_default_na=False)
    c = pd.read_csv(find("fac_determinations_2025_columbia"), dtype=str, keep_default_na=False)
    a = pd.DataFrame({"hosp": p.hospital_code, "t": pd.to_datetime(p.determined_at), "user": p.user_id,
                      "app": p.application_id, "res": p.outcome.map({"APPROVED": "A", "DENIED": "D"}).fillna("O"),
                      "kind": p.determination_type, "why": p.denial_reason})
    b = pd.DataFrame({"hosp": w.HOSP_ID, "t": pd.to_datetime(w.DET_DATE + " " + w.DET_TIME, format="%m/%d/%Y %H:%M:%S"),
                      "user": w.USER_ID, "app": w.APPL_NO, "res": w.RESULT.where(w.RESULT.isin(["A", "D"]), "O"),
                      "kind": np.where(w.RECON == "Y", "RECONSIDERATION", "INITIAL"), "why": w.DENY_RSN})
    ct = pd.to_datetime(c.ts_utc, utc=True).dt.tz_convert("America/Los_Angeles").dt.tz_localize(None)
    d = pd.DataFrame({"hosp": c.facility, "t": ct, "user": c.staff_key, "app": c.app_ref,
                      "res": c.decision.map({"1": "A", "2": "A", "3": "D"}).fillna("O"),
                      "kind": c.kind.map({"new": "INITIAL", "recheck": "RECONSIDERATION", "screen": "PRESUMPTIVE"}),
                      "why": c.reason})
    log = pd.concat([a, b, d], ignore_index=True)
    return log, pd.read_csv(find("fac_assistance_adjustments"), dtype=str)


def contrast(g, rng=None):
    """Within-day pairs for one hospital's frame (sorted by user, date, time): observed pooled contrast and, with rng,
    the contrast after reordering every working day once."""
    y = (g.res == "A").astype(int).values
    day = g.day_key.values
    if rng is not None:
        order = np.lexsort((rng.random(len(y)), day))
        y = y[order]
        day = day[order]
    same = day[1:] == day[:-1]
    x, z = y[:-1][same], y[1:][same]
    return (((1 - x) * z).sum() / (1 - x).sum()) - ((x * z).sum() / x.sum())


def half_up(v, places):
    return float(decimal.Decimal(repr(float(v))).quantize(decimal.Decimal(1).scaleb(-places),
                                                          rounding=decimal.ROUND_HALF_UP))


def run(task):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    log, adj = load(os.path.join(task, "target"))
    det = log[(log.res != "O") & ~log.user.isin(SYSTEM) & (log.t.dt.year == 2025)].copy()
    det["date"] = det.t.dt.date
    det = det.sort_values(["hosp", "user", "date", "t"])
    det["day_key"] = det.groupby(["hosp", "user", "date"]).ngroup()
    bad = 0
    rng = np.random.default_rng(272)
    q_exact, q_mc = [], []
    for code, g in det.groupby("hosp"):
        obs = contrast(g)
        n = g.groupby("day_key").size()
        k = g.assign(a=(g.res == "A").astype(int)).groupby("day_key").a.sum()
        b11, b1 = (k * (k - 1) / n).sum(), ((n - 1) * k / n).sum()
        b01, b0 = (k * (n - k) / n).sum(), ((n - 1) * (n - k) / n).sum()
        exact = 100 * (obs - (b01 / b0 - b11 / b1))
        mc = 100 * (obs - np.mean([contrast(g, rng) for _ in range(120)]))
        if exact >= 6:
            q_exact.append(code)
        if mc >= 6:
            q_mc.append(code)
        ok = abs(exact - fig["measure"][code]) < 1e-3 and abs(mc - exact) < 0.6
        bad += not ok
        print("%s excess %7.3f  reordered %7.3f  figures %7.3f  %s" % (code, exact, mc, fig["measure"][code],
                                                                      "ok" if ok else "MISMATCH"))
    ok = q_exact == fig["call"]["qualify"] and q_mc == q_exact and len(q_exact) == fig["call"]["count"]
    bad += not ok
    print("call: %d %s (Monte Carlo %d)  %s" % (len(q_exact), q_exact, len(q_mc), "ok" if ok else "MISMATCH"))

    # Ask A: each counsellor approval's write-off once, every reversal, the twice-loaded lines once
    appr = det[det.res == "A"][["hosp", "app"]].drop_duplicates()
    adj = adj.drop_duplicates()
    adj["amount"] = adj.amount.astype(float)
    m = adj.merge(appr, left_on=["hospital_code", "application_id"], right_on=["hosp", "app"])
    wo = m[m.adjustment_code == "FAWO"].groupby(["hospital_code", "application_id"]).amount.first() \
        .groupby(level=0).sum()
    rv = m[m.adjustment_code == "FAWR"].groupby("hospital_code").amount.sum()
    net = wo.sub(rv, fill_value=0.0)
    for code in fig["ask_a"]:
        v = half_up(net.get(code, 0.0) / 1000.0, 1)
        ok = v == fig["ask_a"][code]
        bad += not ok
        if not ok:
            print("Ask A %s %.1f against %.1f MISMATCH" % (code, v, fig["ask_a"][code]))

    # Ask B: denials for documents not received, the reason list renumbered on 1 July 2025
    dn = det[det.res == "D"].copy()
    want = np.where(dn.t < pd.Timestamp("2025-07-01"), "2", "1")
    cnt = dn[dn.why.values == want].groupby("hosp").size()
    for code in fig["ask_b"]:
        ok = int(cnt.get(code, 0)) == fig["ask_b"][code]
        bad += not ok
        if not ok:
            print("Ask B %s %d against %d MISMATCH" % (code, int(cnt.get(code, 0)), fig["ask_b"][code]))
    print("asks: %d hospital figures each checked" % len(fig["ask_a"]))
    print("verify:", "PASS" if bad == 0 else "FAIL %d" % bad)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(run(os.path.dirname(HERE)))
