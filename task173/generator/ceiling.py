"""The ask sheet as code on the cut pack: each ask route a competent response builds, scored cell by cell against the
golden (a hit is the golden whole number), then the cracker (the call landed, the hygiene battery, every filed rule),
the mirror (the most attractive wrong route, the PTL as shipped) and the full includer priced on the pair formula.

    python3 generator/ceiling.py [target]"""
from __future__ import annotations

import hashlib
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C    # noqa: E402

ASK_W, CALL_W, IF_W, OFF_CALL = 55.0, 38.0, 7.0, 5.0


def table(P, clocks, dedup):
    ers = dict(zip(P.ers.ubrn, pd.to_datetime(P.ers.referral_received)))
    tc = C.true_clocks(P) if clocks == "chain" else None
    out = {}
    for d in C.QDATES:
        s = P.ptl[P.ptl.snapshot_date == d].copy()
        if dedup == "patient_operation":
            s = s.sort_values(["date_added", "pathway_id"]).drop_duplicates(["patient", "opcs_code"], keep="last")
        elif dedup == "patient_hernia":
            h = s[s.opcs_code.isin(C.HERNIA)].sort_values("date_added").drop_duplicates(["patient"], keep="last")
            s = pd.concat([s[~s.opcs_code.isin(C.HERNIA)], h])
        elif dedup == "cross_site":
            s = s[~C.stale_moved(s)]
        D = pd.Timestamp(d)
        if clocks == "ptl":
            clk = pd.to_datetime(s.rtt_clock_start)
        elif clocks == "ers":
            clk = pd.Series([ers.get(u, pd.Timestamp(c)) if u else pd.Timestamp(c) for u, c in zip(s.ubrn, s.rtt_clock_start)], index=s.index)
        elif clocks == "added":
            clk = pd.to_datetime(s.date_added)
        else:
            clk = pd.Series([tc[(p, o, pd.Timestamp(a))] for p, o, a in zip(s.patient, s.opcs_code, s.date_added)], index=s.index)
        wait = (D - clk).dt.days.values
        for site in ("MGH", "FEN"):
            mk = (s.site2 == site).values
            out[("A", d, site)] = int(((wait >= 364) & mk).sum())
            out[("B", d, site)] = int((s.opcs_code.isin(C.HERNIA).values & mk).sum())
    return out


def main(tgt=None):
    P = C.Pack(tgt)
    digest = hashlib.sha256(open(os.path.join(P.t, "admitted_ptl_snapshots_2021_2026.parquet"), "rb").read()).hexdigest()[:16]
    gold = table(P, "chain", "cross_site")
    assert gold == C.ask_tables(P, "golden")
    routes = {"A0/B0 the PTL as shipped (mirror)": ("ptl", "none"),
              "A1/B1 battery: one row per patient and operation (cracker)": ("ptl", "patient_operation"),
              "A2 date added as the clock": ("added", "none"),
              "A3/B3 e-RS referral dates, one row per patient and operation (full includer)": ("ers", "patient_operation"),
              "A4 e-RS referral dates, moved rows out": ("ers", "cross_site"),
              "A5 re-listings chained, e-RS dates, one row per patient and operation": ("chain", "patient_operation"),
              "B2 one hernia row per patient": ("ptl", "patient_hernia")}
    res = {}
    print("pack digest (PTL) %s" % digest)
    for name, (ck, dd) in routes.items():
        t = table(P, ck, dd)
        hitA = sum(t[k] == gold[k] for k in gold if k[0] == "A")
        hitB = sum(t[k] == gold[k] for k in gold if k[0] == "B")
        res[name] = (hitA, hitB)
        print("%-80s Ask A %d of 8, Ask B %d of 8" % (name, hitA, hitB))
    n = 16.0
    cr = sum(res["A1/B1 battery: one row per patient and operation (cracker)"]) / n
    mi = sum(res["A0/B0 the PTL as shipped (mirror)"]) / n
    fi = sum(res["A3/B3 e-RS referral dates, one row per patient and operation (full includer)"]) / n
    C_ = CALL_W + IF_W + ASK_W * cr
    S_ = OFF_CALL + IF_W + ASK_W * mi
    F_ = CALL_W + IF_W + ASK_W * fi
    print("cracker keeps %.1f per cent of the ask weight (%.1f in all); mirror %.1f per cent (%.1f); full includer %.1f per cent (%.1f)"
          % (100 * cr, C_, 100 * mi, S_, 100 * fi, F_))
    print("pair ceiling %.1f (cracker with mirror); full includer with mirror %.1f" % ((C_ + S_) / 2, (F_ + S_) / 2))
    print("mirror leakage %.1f per cent of the ask weight" % (100 * mi))
    return res


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
