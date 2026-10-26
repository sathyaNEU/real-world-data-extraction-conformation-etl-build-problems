"""The ask sheet's measurement on the cut pack: the cracker (lands the call, runs the battery, executes every filed rule)
and the mirror (the call on the rides served), each scored figure by figure on the 38/7/55 weights, with every path
each ask offers a response that does not meet its device.

    python3 task308/generator/pair.py <target dir>
"""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as SV

REC, IF, ASK = 38.0, 7.0, 55.0
NETS = SV.NETS
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


def people_paths(target, T):
    A = pd.read_csv(os.path.join(target, SV.FN["accounts"]), dtype=str)
    A["home"] = A.home_area.str.strip().str.lower().map(SV.AREAS)
    home_new = dict(zip(A.account_id, A.home)); home_leg = dict(zip("L" + A.legacy_account_no.fillna("-"), A.home))
    R = T[~T["false"]]
    unm = pd.Series([home_new.get(x) or home_leg.get(x) for x in R.acct.unique()]).value_counts().to_dict()
    leg = dict(zip("L" + A.legacy_account_no.dropna(), A.account_id[A.legacy_account_no.notna()]))
    all_ids = T.acct.map(lambda x: leg.get(x, x)).unique()
    fs = A[A.account_id.isin(all_ids)].groupby("home").size().to_dict()
    return {"one person an account, legacy numbers mapped (the natural read)": SV.people(target, T, "accounts")[0],
            "one person a payment card (the over-repair)": SV.people(target, T, "cards")[0],
            "one person an id, legacy numbers left unmapped": unm,
            "accounts with any undock, false starts as rides": fs}


def energy_paths(target):
    C = pd.read_csv(os.path.join(target, SV.FN["charging"]))
    utc = C.groupby(pd.to_datetime(C.plug_out_utc).dt.month).energy_kwh.sum().to_dict()
    return {"every session summed (the natural read)": SV.charging(target, "all"),
            "a point's register must rise (the over-repair)": SV.charging(target, "monotone"),
            "every session by its UTC month": utc}


def workshop_paths(target, T, gold):
    J = pd.read_csv(os.path.join(target, SV.FN["workshop"]))
    J["op"] = SV._secs(pd.to_datetime(J.opened_utc)); J["cl"] = SV._secs(pd.to_datetime(J.closed_utc))
    J["typ"] = np.where(J.asset_class == "E-bike", "ebike", "classic")
    J["q_loc"] = (pd.to_datetime(J.opened_utc).dt.tz_convert(SV.TZ).dt.month - 1) // 3 + 1
    J["q_utc"] = (pd.to_datetime(J.opened_utc).dt.month - 1) // 3 + 1
    R = T[~T["false"]]
    rq = (pd.to_datetime(R.t0, unit="s", utc=True).dt.tz_convert(SV.TZ).dt.month - 1) // 3 + 1
    rq_all = (pd.to_datetime(T.t0, unit="s", utc=True).dt.tz_convert(SV.TZ).dt.month - 1) // 3 + 1

    def rate(jobs, qcol="q_loc", rides=(R, rq)):
        out = {}
        for typ in ("ebike", "classic"):
            for q in range(1, 5):
                nj = int(((jobs.typ == typ) & (jobs[qcol] == q)).sum())
                nr = int(((rides[0].ebike == (typ == "ebike")) & (rides[1] == q)).sum())
                out[(typ, q)] = 1e4 * nj / nr
        return out

    def window(hours):
        keep, last = [], {}
        for r in J.sort_values(["op", "job_no"]).itertuples():
            p = last.get(r.asset_tag)
            if p is not None and p[1] == r.fault_code and r.op - p[0] < hours * 3600:
                last[r.asset_tag] = (r.cl, r.fault_code)
                continue
            keep.append(r.Index); last[r.asset_tag] = (r.cl, r.fault_code)
        return J.loc[keep]

    return {"every job (the natural read)": rate(J),
            "one job a bike and fault within 30 days (the over-repair)": {k: v[2] for k, v in SV.workshop(target, T, "window30").items()},
            "same bike and fault reopened within 24 hours of the close dropped": rate(window(24)),
            "same bike and fault reopened within 48 hours of the close dropped": rate(window(48)),
            "every job, false starts counted as rides": rate(J, rides=(T, rq_all)),
            "every job, quarters by UTC": rate(J, "q_utc")}


def main(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    G = SV.solve(target)
    T = G["T"]
    call_n = 6
    mirror_call = sum(fig["recorded_route"][n] == fig["net_revenue"][n] for n in NETS)
    pa = people_paths(target, T)
    pb = energy_paths(target)
    pc = workshop_paths(target, T, G["workshop"])
    ha = {k: sum(1 for n in NETS if v.get(n) == fig["people"][n]) for k, v in pa.items()}
    hb = {k: sum(1 for m in range(1, 13) if int(round(v.get(m, 0))) == fig["energy_kwh"][MONTHS[m - 1]]) for k, v in pb.items()}
    hc = {k: sum(1 for (t, q) in v if round(v[(t, q)], 1) == fig["workshop_per_10000"][("E-bike" if t == "ebike" else "Classic") + " Q%d" % q])
          for k, v in pc.items()}
    print("ask A, people by home area (5 figures; Central, University, Riverside, Old Town, Hillcrest):")
    for k, v in ha.items():
        print("   %-78s %d of 5   %s" % (k, v, ", ".join(format(int(pa[k].get(n, 0)), ",") for n in NETS)))
    print("ask B, the pilot's charging energy by month (12 figures, January to December):")
    for k, v in hb.items():
        print("   %-78s %d of 12   %s" % (k, v, ", ".join("%d" % int(round(pb[k].get(m, 0))) for m in range(1, 13))))
    print("ask C, workshop jobs per 10,000 rides (8 figures, e-bikes Q1 to Q4 then classic Q1 to Q4):")
    for k, v in hc.items():
        print("   %-78s %d of 8   %s" % (k, v, ", ".join("%.1f" % pc[k][(t, q)] for t in ("ebike", "classic") for q in range(1, 5))))
    keep = max(ha.values()) + max(hb.values()) + max(hc.values())
    lc = ls = keep / 25.0
    cracker = REC + IF + ASK * lc
    r = REC * mirror_call / call_n
    mirror = r + IF + ASK * ls
    pair = (cracker + mirror) / 2
    print("cracker: the call (6 of 6) and the best path on each ask, %d of 25 ask figures: %.1f" % (keep, cracker))
    print("mirror: the call on the rides served (%d of 6: %s) and the same ask paths: %.1f"
          % (mirror_call, fig["recorded_route"], mirror))
    print("Pair ceiling: %.1f" % pair)
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * ls))
    print("(the asks read no file the call reads, so both responses take the same ask paths; separation is asserted in "
          "checks.py)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "target")))
