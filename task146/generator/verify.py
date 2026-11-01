"""task146 architecture 2: an independent recomputation of every graded figure from target/ with pandas."""
import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
FIG = json.load(open(os.path.join(HERE, "figures.json")))
FAMS = ["Easy Saver", "Loyalty Saver", "Easy Access Cash ISA", "Young Saver"]


def fam(code, d):
    if code.startswith("LS"):
        return "Loyalty Saver"
    if code == "ES02":
        return "Easy Saver" if d < pd.Timestamp("2025-07-01") else "Young Saver"
    return {"ES01": "Easy Saver", "IS01": "Easy Access Cash ISA", "YS01": "Young Saver"}[code]


b = pd.read_csv(os.path.join(T, "ia_month_end_balances_2021-2026.csv"), parse_dates=["month_end"])
b["ym"] = b["month_end"].dt.year * 12 + b["month_end"].dt.month - 1
b["t"] = b["ym"] - b["ym"].min()
b["fam"] = [fam(c, d) for c, d in zip(b["product_code"], b["month_end"])]
e = pd.read_csv(os.path.join(T, "ia_account_events_2021-2026.csv"))
e["local"] = pd.to_datetime(e["event_utc"], utc=True).dt.tz_convert("Europe/London").dt.date
op = e[e.event == "OPEN"].groupby(["local", "amount_pence"])["account_no"].apply(list).to_dict()
succ, taken = {}, set()
for r in e[e.event == "CLOSE"].itertuples():
    c = [x for x in op.get((r.local, r.amount_pence), []) if x != r.account_no and x not in taken]
    if len(c) == 1:
        succ[r.account_no] = c[0]
        taken.add(c[0])
B = {(a, t): v for a, t, v in zip(b["account_no"], b["t"], b["balance_gbp"])}
n = int(b["t"].max()) + 1
starts = {t: b[(b.t == t) & (b.balance_gbp > 0)][["account_no", "balance_gbp", "fam"]].values for t in range(0, n, 12)}
now = b[b.t == n - 1].groupby("fam")["balance_gbp"].sum()
fails = 0
for k in (12, 24, 36):
    kept = dict.fromkeys(FAMS, 0.0)
    held = dict.fromkeys(FAMS, 0.0)
    for s in range(0, n - k, 12):
        for a, b0, f in starts[s]:
            low, cur = b0, a
            for t in range(s + 1, s + k + 1):
                while (cur, t) not in B and cur in succ:
                    cur = succ[cur]
                v = B.get((cur, t), 0.0)
                if v == 0.0 and cur in succ and B.get((succ[cur], t), 0.0) > 0:
                    cur = succ[cur]
                    v = B[(cur, t)]
                low = min(low, v)
            kept[f] += low
            held[f] += b0
    tot = 0.0
    for f in FAMS:
        st = now.get(f, 0.0) * kept[f] / held[f]
        tot += st
        if round(st / 1e6) != FIG["stable_m"][str(k)][f]:
            fails += 1
            print("FAIL stable", k, f, round(st / 1e6), FIG["stable_m"][str(k)][f])
    ok = round(tot / 1e6) == FIG["stable_m"][str(k)]["total"]
    fails += 0 if ok else 1
    print("%s  stable %d months, total %d million" % ("ok  " if ok else "FAIL", k, round(tot / 1e6)))
for f in FAMS:
    if round(now.get(f, 0.0) / 1e6) != FIG["now_m"][f]:
        fails += 1
        print("FAIL balance", f)
print("verify: %d failures" % fails)
sys.exit(1 if fails else 0)
