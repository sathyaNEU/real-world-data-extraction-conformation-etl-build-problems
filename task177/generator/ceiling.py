"""The pair ceiling on the cut pack (supplemental-stumping Part 0), on the rubric weights 38 / 7 / 55.

The cracker lands the call and its components, reads every filed rule and runs the hygiene battery: on the guardrails
it maps Salandi's old code to its successor and Gandhamardan's correspondent portfolio to the bank by the directory, and
counts a loan once by its account number at its latest report. The mirror stops at the default path (it misses the
call, keeping about 5 of the 38) and reads the bureau's own consumer summary. Each ask figure is a hit when it
equals the golden at the asked rounding."""
from __future__ import annotations

import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
W_CALL, W_IF, W_ASK, R_MISS = 38.0, 7.0, 55.0, 5.0


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    names = sorted(os.listdir(T))
    pick = lambda s: os.path.join(T, next(n for n in names if s in n))
    pool = pd.read_csv(pick("pool_tape"))
    kyc = pd.read_csv(pick("member_kyc"))[["member_id", "cic_ref"]]
    cic = pd.read_csv(pick("cic_portfolio"))
    d = pd.read_csv(pick("member_directory")).fillna("")
    inst = dict(zip(d.member_code, d.institution))
    par = {r.member_code: (r.parent_code or r.member_code) for r in d.itertuples()}
    succ = {r.member_code: (r.successor_code or r.member_code) for r in d.itertuples()}
    pt = pool.merge(kyc, on="member_id")
    mf = cic[cic.account_type.isin(["JLG", "MFI-IND"]) & (cic.account_status == "ACTIVE")]
    # the cracker: institutions by the directory, a loan once by its account number
    once = mf.sort_values("date_reported").drop_duplicates(["inquiry_ref", "account_no"], keep="last")
    once = once.assign(ent=once.member_code.map(lambda c: inst[succ[par[c]]]))
    g = once.groupby("inquiry_ref").agg(lenders=("ent", "nunique"), debt=("current_balance", "sum"))
    c = pt.join(g, on="cic_ref")
    c["breach"] = (c.lenders >= 4) | (c.debt > 200000)
    # the mirror: the bureau's summary columns
    s = cic.groupby("inquiry_ref")[["summary_active_mfi_lenders", "summary_mfi_outstanding"]].first()
    m = pt.join(s, on="cic_ref")
    m["breach"] = (m.summary_active_mfi_lenders >= 4) | (m.summary_mfi_outstanding > 200000)
    rows = []
    for who, fr in (("cracker", c), ("mirror", m)):
        n = fr.groupby("branch_code").breach.sum()
        lk = (fr[fr.breach].groupby("branch_code").principal_outstanding_inr.sum() / 1e5).round(1)
        hits = []
        for b in n.index:
            hits.append(("count " + b, int(n[b]) == fig["ask_breach_%s" % b]))
            hits.append(("lakh " + b, float(lk.get(b, 0.0)) == fig["ask_lakh_%s" % b]))
        rows.append((who, hits))
    keep = {who: sum(h for _, h in hits) / len(hits) for who, hits in rows}
    C = W_CALL + W_IF + W_ASK * keep["cracker"]
    S = R_MISS + W_IF + W_ASK * keep["mirror"]
    for who, hits in rows:
        print("%-8s keeps %d of %d ask figures: %s" % (who, sum(h for _, h in hits), len(hits),
                                                      ", ".join(k for k, h in hits if h) or "none"))
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f per cent of ask weight"
          % (C, S, (C + S) / 2, 100 * keep["mirror"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
