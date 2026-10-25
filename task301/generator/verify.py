"""Independent verifier for task301: reads only target.zip and generator/figures.json, recomputes every figure the
write-up states by its own route, and exits 1 on any disagreement."""
import datetime as dt
import io
import json
import os
import sys
import zipfile

import numpy as np
import pandas as pd
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
CANDS = ["Coastal Hinterland", "Inner South", "Northern Corridor", "Western Plains"]
CUR = {"Daily smoker", "Weekly smoker", "Irregular smoker", "Smoker"}
BAD = []


def say(name, ok, detail=""):
    print("%-4s %s%s" % ("ok" if ok else "FAIL", name, (" :: " + detail) if detail else ""))
    if not ok:
        BAD.append(name)


def read(z, name, **kw):
    with z.open(name) as fh:
        data = fh.read()
    if name.endswith(".parquet"):
        return pd.read_parquet(io.BytesIO(data))
    return pd.read_csv(io.BytesIO(data), **kw)


def state(s):
    return 1 if s in CUR else (0 if s == "Ex-smoker" else (-1 if s in ("Never smoked", "Non-smoker") else None))


def main(zpath):
    BAD.clear()
    F = json.load(open(os.path.join(HERE, "figures.json")))
    z = zipfile.ZipFile(zpath)
    ext = read(z, "active_patients_2026-09-30.csv", dtype=str, keep_default_na=False)
    hist = read(z, "smoking_status_history_2012-2026.parquet")
    log = read(z, "quit_outreach_calls_eastern_shore_2025.csv", dtype=str, keep_default_na=False)
    sub = dict(zip(ext.patient_key, ext.sub_region))
    # lists
    lst = ext[ext.smoking_status.isin(CUR)]
    for g in CANDS:
        n = int((lst.sub_region == g).sum())
        say("listed %s" % g, n == F["listed"][g], "%d" % n)
    # day-level history: the last entry of each day, then consecutive pairs from a smoker or ex-smoker entry
    hs = hist.assign(day=hist.recorded_at.str[:10]).sort_values(["patient_key", "recorded_at"], kind="mergesort")
    hs = hs.drop_duplicates(["patient_key", "day"], keep="last")
    st = np.array([state(s) for s in hs.smoking_status.values])
    t = (pd.to_datetime(hs.day).values.astype("datetime64[D]").astype(np.int64)
         - np.datetime64("2012-01-01", "D").astype(np.int64)) / 365.25
    k = hs.patient_key.values
    same = k[1:] == k[:-1]
    s0, s1, dtv = st[:-1][same], st[1:][same], (t[1:] - t[:-1])[same]
    reg = np.array([sub.get(x) for x in k[:-1][same]])
    use = np.isin(s0, [0, 1]) & (dtv > 0)
    rates = {}
    for g in CANDS:
        m = use & (reg == g)
        a, b, d = s0[m] == 1, s1[m] == 1, dtv[m]

        def nll(x):
            q, r = np.exp(x)
            pi = r / (q + r)
            e = np.exp(-(q + r) * d)
            p = np.clip(np.where(a, pi + (1 - pi) * e, pi * (1 - e)), 1e-12, 1 - 1e-12)
            return -np.sum(np.where(b, np.log(p), np.log(1 - p)))
        res = minimize(nll, np.log([0.05, 0.01]), method="L-BFGS-B")
        rates[g] = np.exp(res.x)
        say("quit rate %s" % g, int(round(100 * rates[g][0])) == F["quit_rate_pct"][g], "%.4f" % rates[g][0])
    # conversion from the case log
    reached = int((log.outcome != "Not reached").sum())
    stopped = int((log.outcome == "Not a current smoker").sum())
    quits = int((log.four_week_status == "Not smoking").sum())
    kf = (reached / len(log)) * quits / (reached - stopped)
    say("case log counts", [len(log), reached, stopped, quits] ==
        [F["pilot"]["listed"], F["pilot"]["reached"], F["pilot"]["stopped"], F["pilot"]["quits"]])
    say("quits per 100 still smoking", int(round(100 * kf)) == F["quits_per100_still"], "%.4f" % kf)
    # expected quits: calls spread evenly through 2027
    y0 = np.datetime64("2027-01-01", "D")
    out = {}
    u = (np.arange(53) + 0.5) / 53
    for g in CANDS:
        lg = lst[lst.sub_region == g]
        age = (y0 - pd.to_datetime(lg.smoking_status_date).values.astype("datetime64[D]")).astype(float) / 365.25
        q, r = rates[g]
        pi = r / (q + r)
        still = np.mean([pi + (1 - pi) * np.exp(-(q + r) * (age + x)) for x in u], axis=0)
        out[g] = (still.sum() * kf, still.mean())
    win = max(out, key=lambda g: out[g][0])
    say("call", win == F["call_region"], win)
    say("quits to the nearest 50", int(round(out[win][0] / 50.0) * 50) == F["call_quits"], "%.1f" % out[win][0])
    say("share still smoking to the nearest 5", int(round(100 * out[win][1] / 5.0) * 5) == F["call_still_pct"],
        "%.3f" % out[win][1])
    # ask A: Quitline names matched to the register, by the register's sub-region
    q = read(z, "quitline_referrals_2023-2025.csv", dtype=str, keep_default_na=False)
    pr = read(z, "practices.csv", dtype=str, keep_default_na=False)

    def nm(s):
        s = " ".join(s.split()).lower()
        s = s.replace(" pty ltd", "").replace(" med centre", " medical centre")
        return s[:-3] + " general practice" if s.endswith(" gp") else s
    regmap = {nm(a): b for a, b in zip(pr.practice_name, pr.sub_region)}
    q["sr"] = [regmap[nm(x)] for x in q.referring_practice]
    q = q[q.month.str.startswith("2025")]
    for g in CANDS:
        val = int(q[q.sr == g].referrals.astype(int).sum())
        say("referrals %s" % g, val == F["ask_referrals"][g], "%d" % val)
    # asks B and C: a leg's record is written when its line is released; Transferred legs are the leg to Quitline
    d = read(z, "dialler_legs_2025.csv", dtype={"patient_key": str})
    d["e"] = pd.to_datetime(d.date_time)
    d["s"] = d.e - pd.to_timedelta(d.duration_s, unit="s")
    say("Transferred legs", int((d.result == "Transferred").sum()) == F["transfer_legs"],
        "%d" % int((d.result == "Transferred").sum()))
    c = d[(d.result != "Transferred") & (d.s.dt.hour >= 17)]
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
        e = c[c.s.dt.day_name() == day]
        got = [len(e), int(e[e.result == "Answered"].patient_key.nunique())]
        say("evening %s" % day, got == [F["ask_evening"][day]["calls"], F["ask_evening"][day]["reached"]],
            "%d calls, %d reached" % tuple(got))
    a = d[d.result == "Answered"]
    t = d[d.result == "Transferred"]
    for ag, months in F["ask_talk_min"].items():
        for mth, val in months.items():
            mi = dt.datetime.strptime(mth, "%B").month
            x = a[(a.s.dt.month == mi) & (a.agent_id == ag)]
            y = t[(t.s.dt.month == mi) & (t.agent_id == ag)]
            got = (x.duration_s.sum() - y.duration_s.sum()) / 60.0 / x.patient_key.nunique()
            say("talk %s %s" % (ag, mth), round(got, 1) == val, "%.3f" % got)
    print("%d failures" % len(BAD))
    return len(BAD)


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1]) else 0)
