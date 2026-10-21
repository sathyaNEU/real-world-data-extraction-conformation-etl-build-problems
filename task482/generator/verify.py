"""An independent recomputation of every graded figure from the cut pack, written apart from bundle.py (pandas),
compared with generator/figures.json.

    python3 task482/generator/verify.py [target]"""
import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def main(target=None, gdir=None):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    reg = pd.read_csv(os.path.join(target, "sar_business_register_extract_2026-09-30.csv"))
    t = pd.to_datetime(reg.created_at_utc.str.replace("Z", ""))
    bst = (t >= "2026-03-29 01:00") & (t < "2026-10-25 01:00") | (t >= "2025-03-30 01:00") & (t < "2025-10-26 01:00")
    reg["local"] = t + pd.to_timedelta(bst.astype(int), unit="h")
    scr = pd.read_csv(os.path.join(target, "sar_register_risk_screen_referrals_2026-05.csv"))
    reg["flag"] = reg.record_id.isin(scr[scr.referred == "Y"].record_id)
    frame = reg[reg.local < "2026-05-01"]
    N = frame.groupby(["region", "flag"]).size()
    au = pd.read_csv(os.path.join(target, "sar_register_quality_audit_summer_2026.csv"), dtype={"outcome": str})
    au = au.merge(reg[["record_id", "region", "flag"]], on="record_id")
    au["err"] = au.outcome.isin(["FAIL", "1", "2", "3", "4"])
    e = au.groupby(["region", "flag"]).err.mean()
    rate = (N * e).groupby(level=0).sum() / N.groupby(level=0).sum()
    bad = int(sorted(rate[rate > 0.04].index) != fig["call"]["chosen"])
    q3 = reg[(reg.local >= "2026-07-01") & (reg.local < "2026-10-01")].groupby("region").size()
    gz = pd.read_csv(os.path.join(target, "ardmuir_gazette_company_notices_2026q3.csv"))
    gz = gz[gz.notice_type != "first notice"].sort_values(["gazette_date", "notice_id"])
    last = gz.groupby("record_id").notice_type.last()
    d = last[last == "struck off and dissolved"].index
    dis = reg[reg.record_id.isin(d)].groupby("region").size()
    for u in fig["ask_a"]:
        bad += int(q3.get(u, 0)) != fig["ask_a"][u]
        bad += int(dis.get(u, 0)) != fig["ask_b"][u]
    print("verify: %d figures differ from figures.json" % bad)
    return bad == 0


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else None) else 1)
