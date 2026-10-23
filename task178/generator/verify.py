"""task178 independent verifier: reads only the shipped bundle (target/, figures.json, submission.md, golden/) on its
own code path (pandas, a two-stage least squares, its own joins) and recomputes every graded figure.

    python3 task178/generator/verify.py task178/target"""
from __future__ import annotations

import json
import math
import os
import re
import sys

import numpy as np
import pandas as pd

OUT = []


def ok(label, cond, detail=""):
    OUT.append((label, bool(cond)))
    print(("PASS " if cond else "FAIL ") + label + ((": " + str(detail)) if detail else ""))


def find(target, prefix, ext):
    hits = [f for f in os.listdir(target) if f.startswith(prefix) and f.endswith(ext)]
    assert len(hits) == 1, (prefix, hits)
    return os.path.join(target, hits[0])


def hourly(target):
    reg = pd.read_csv(find(target, "bct_reporting_dealers", ".csv"), dtype=str).fillna("")
    to = {r.dealer_code: r.of_record_to for r in reg.itertuples()}
    fl = pd.read_csv(find(target, "dealer_customer_flows_hourly", ".csv"), dtype={"report_date": str})
    fl = fl[[not (to[c] and d > to[c]) for c, d in zip(fl.dealer_code, fl.report_date)]]
    fl = fl.sort_values("received_at").groupby(["report_date", "hour", "dealer_code"], as_index=False).last()
    fl["h"] = fl.hour.str[:2].astype(int)
    cust = fl.groupby(["report_date", "h"]).net_customer_usd_k.sum() / 1000.0
    op = pd.read_csv(find(target, "bct_spot_operations", ".csv"))
    op = op[op.status != "ANULADA"]
    t = pd.to_datetime(op.dealt_at)
    op = op.assign(report_date=t.dt.strftime("%Y-%m-%d"), h=t.dt.hour,
                   net=np.where(op.operation == "VENTA", op.amount_usd_k, -op.amount_usd_k) / 1000.0)
    bank = op.groupby(["report_date", "h"]).net.sum()
    md = pd.read_csv(find(target, "platform_hourly_mid", ".csv"), dtype={"session_date": str})
    md["h"] = md.hour_mark.str[:2].astype(int)
    rows = []
    for d, g in md.groupby("session_date"):
        marks = dict(zip(g.h, g.mid_tqp_per_usd))
        prev, fsum, isum = 8, 0.0, 0.0
        for hh in range(8, 16):
            fsum += float(cust.get((d, hh), 0.0))
            isum += float(bank.get((d, hh), 0.0))
            if hh + 1 in marks:
                rows.append((d, 100 * math.log(marks[hh + 1] / marks[prev]), fsum, isum))
                prev, fsum, isum = hh + 1, 0.0, 0.0
    h = pd.DataFrame(rows, columns=["d", "r", "f", "i"])
    close = md[md.h == 16].set_index("session_date").mid_tqp_per_usd.sort_index()
    return h, close


def two_stage(y, x, z):
    Z = np.column_stack([np.ones(len(z)), z])
    xhat = Z @ np.linalg.lstsq(Z, x, rcond=None)[0]
    X = np.column_stack([np.ones(len(xhat)), xhat])
    return float(np.linalg.lstsq(X, y, rcond=None)[0][1])


def vol_at(h, close, lam):
    bank_day = h.groupby("d").i.sum().reindex(close.index).fillna(0.0)
    ch = 100 * np.log(close / close.shift(1))
    adj = (ch + lam * bank_day).iloc[1:]
    return math.sqrt(252 * float((adj ** 2).mean()))


def ask_a(target):
    c = pd.read_csv(find(target, "platform_confirmations", ".csv"))
    c = c[c.status == "CONFIRMED"].copy()
    c["sg"] = np.where(c.side == "BUY", 1.0, -1.0)
    c["cost"] = c.usd_amount_k * c.sg * (c.price - (c.bid_at_arrival + c.ask_at_arrival) / 2)
    o = c.groupby(["trader", "side", "trade_time_utc"]).agg(size=("usd_amount_k", "sum"), cost=("cost", "sum")).reset_index()
    loc = pd.to_datetime(o.trade_time_utc.str.rstrip("Z")) - pd.Timedelta(hours=5)
    o["q"] = loc.dt.quarter
    o["band"] = pd.cut(o["size"], [0, 1000, 3000, 10000, 1e12], right=False,
                       labels=["under 1m", "1m to 3m", "3m to 10m", "10m and over"])
    t = o.groupby(["q", "band"], observed=True).agg(cost=("cost", "sum"), size=("size", "sum"))
    return {(int(q), str(b)): float(r["cost"] / r["size"]) for (q, b), r in t.iterrows()}


def ask_b(target):
    d = pd.read_excel(find(target, "cordillera_fx_forward_deals", ".xlsx"), sheet_name="Deals")
    cl = pd.read_csv(find(target, "cordillera_corporate_client_register", ".csv"))
    d = d.merge(cl[["client_no", "segment"]], left_on="Client No.", right_on="client_no", how="left")
    d = d[(d.Status != "ANULADA") & (d.Pair == "USD/TQP") & (d.segment != "TESORERIA")]
    w = d[d.Product == "WINDOW"]
    o = d[d.Product == "OUTRIGHT"]
    m = w.merge(o, on=["Client No.", "Client USD"], suffixes=("_w", "_o"))
    m = m[(abs(m["Forward rate_w"] - m["Forward rate_o"]) < 0.005) & (m["Maturity date_o"] >= m["Window opens_w"])
          & (m["Maturity date_o"] <= m["Maturity date_w"])]
    used = m.groupby("Deal No._w")["Notional_o"].sum()
    d = d.copy()
    d["due"] = d.Notional - d["Deal No."].map(used).fillna(0.0).where(d.Product == "WINDOW", 0.0)
    d = d[(d["Maturity date"].dt.year == 2027) & (d.due > 0.5)]
    d["q"] = d["Maturity date"].dt.quarter
    sell = d[(d.segment == "EXPORTADOR") & (d["Client USD"] == "VENDE")].groupby("q").due.sum() / 1e6
    buy = d[(d.segment == "IMPORTADOR") & (d["Client USD"] == "COMPRA")].groupby("q").due.sum() / 1e6
    return {q: float(sell.get(q, 0.0)) for q in range(1, 5)}, {q: float(buy.get(q, 0.0)) for q in range(1, 5)}


def main(target):
    task = os.path.dirname(os.path.abspath(target))
    figs = json.load(open(os.path.join(task, "generator", "figures.json")))
    sub = open(os.path.join(task, "submission.md")).read()
    h, close = hourly(target)
    lam = two_stage(h.r.values, (h.f - h.i).values, h.f.values)
    v = vol_at(h, close, lam)
    ok("verify: two-stage impact recomputed from the bundle", 0.5 <= lam * 100 <= 0.6, round(lam * 100, 4))
    ok("verify: expected volatility inside the filed band", figs["call"]["expected_volatility_band_pct"][0] < v
       <= figs["call"]["expected_volatility_band_pct"][1], round(v, 3))
    ok("verify: the setting", math.ceil(v) == figs["call"]["pricing_volatility_pct"] == 12)
    rec = vol_at(h, close, 0.0)
    ok("verify: the recorded volatility as the write-up states it", round(rec, 1) == figs["rivals"]["record_vol_pct"], round(rec, 3))
    X = np.column_stack([np.ones(len(h)), (h.f - h.i).values])
    ols_net = float(np.linalg.lstsq(X, h.r.values, rcond=None)[0][1])
    X = np.column_stack([np.ones(len(h)), h.f.values])
    rf = float(np.linalg.lstsq(X, h.r.values, rcond=None)[0][1])
    ok("verify: the net-flow rival", round(vol_at(h, close, ols_net), 1) == figs["rivals"]["net_flow_impact_vol_pct"])
    ok("verify: the customer-flow rival", round(vol_at(h, close, rf), 1) == figs["rivals"]["customer_flow_impact_vol_pct"])
    a = ask_a(target)
    ok("verify: ask A, 16 cells as figures.json", len(a) == 16 and all(
        round(a[(q, b)], 1) == figs["ask_a_hedging_cost_tqp_per_usd"]["Q%d" % q][b] for (q, b) in a))
    s, b = ask_b(target)
    ok("verify: ask B, 8 figures as figures.json", all(
        round(s[q], 1) == figs["ask_b_forwards_due_2027_usd_mn"]["Q%d" % q]["exporters_sell"] and
        round(b[q], 1) == figs["ask_b_forwards_due_2027_usd_mn"]["Q%d" % q]["importers_buy"] for q in range(1, 5)))
    # the write-up carries the same figures
    for q in range(1, 5):
        cells = figs["ask_a_hedging_cost_tqp_per_usd"]["Q%d" % q]
        line = "Q%d 2026: under 1 million %.1f; 1 to 3 million %.1f; 3 to 10 million %.1f; 10 million and over %.1f" % (
            q, cells["under 1m"], cells["1m to 3m"], cells["3m to 10m"], cells["10m and over"])
        ok("verify: write-up ask A line Q%d" % q, line in sub)
        bb = figs["ask_b_forwards_due_2027_usd_mn"]["Q%d" % q]
        ok("verify: write-up ask B line Q%d" % q, "Q%d 2027: exporters sell %.1f; importers buy %.1f" % (
            q, bb["exporters_sell"], bb["importers_buy"]) in sub)
    ok("verify: write-up call sentence", "**Price the 2027 one-year dollar options at 12 per cent.**" in sub)
    # every format read back, with a positive control on the same path
    from pypdf import PdfReader
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            t = " ".join((pg.extract_text() or "") for pg in PdfReader(p).pages)
            ok("verify: %s extracts text" % f, len(t) > 500 and ("Banco" in t))
        elif f.endswith(".xlsx"):
            x = pd.read_excel(p, sheet_name=None)
            ok("verify: %s reads" % f, sum(len(v) for v in x.values()) > 10)
        elif f.endswith(".csv"):
            ok("verify: %s reads" % f, len(pd.read_csv(p)) > 5)
    pol = " ".join((pg.extract_text() or "") for pg in PdfReader(find(target, "cordillera_fx_options_pricing_policy", ".pdf")).pages)
    pol = re.sub(r"\s+", " ", pol)
    ok("verify: the policy files the counterfactual and the convention",
       "had the Banco Central not operated in the spot market" in pol and "rounded up to the next whole per cent" in pol
       and "at 252 sessions a year" in pol)
    golden = os.path.join(task, "golden")
    gb = pd.read_excel(os.path.join(golden, "usd_options_vol_2027.xlsx"), sheet_name=None, header=None)
    ok("verify: golden workbook carries the call", any("12%" in str(v) for v in gb["Pricing vol 2027"].values.ravel()))
    ok("verify: golden chart exists and is a PNG", open(os.path.join(golden, "free_float_vol_2027.png"), "rb").read(8)
       == b"\x89PNG\r\n\x1a\n")
    bad = [o for o in OUT if not o[1]]
    print("\n%d verifications, %d failed" % (len(OUT), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
