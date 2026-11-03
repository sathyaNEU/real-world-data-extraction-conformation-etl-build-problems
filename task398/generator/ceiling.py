"""The pair ceiling on the cut pack. Shares no code with the generator: it reads target/ and figures.json only.

The cracker lands the call, runs the hygiene battery and executes every filed statement: it conforms SEDOL to ISIN
through the security master and pence to pounds, takes each custodian's own report for its own months, dedupes the
trades open at the change of custodian against Northcote's settlements, values scrip at the cash dividend, dates
dividends by their ex-dates from the corporate actions feed, and dates trades two weekdays before settlement. The
mirror stops on rung 1 (the linked attribution) and handles the asks the same way.
"""
import csv
import datetime as dt
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ISO = dt.date.fromisoformat
W_MAIN, W_IF, W_ASK = 38.0, 7.0, 55.0


def rows(t, fn):
    with open(os.path.join(t, fn), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def dmy(s):
    d, m, y = s.split("/")
    return dt.date(int(y), int(m), int(d))


def quarter(d):
    for a, b, q in ((dt.date(2025, 10, 1), dt.date(2025, 12, 31), "Q1"), (dt.date(2026, 1, 1), dt.date(2026, 3, 31), "Q2"),
                    (dt.date(2026, 4, 1), dt.date(2026, 6, 30), "Q3"), (dt.date(2026, 7, 1), dt.date(2026, 9, 30), "Q4")):
        if a <= d <= b:
            return q


def cracker_asks(t):
    master = rows(t, "thornbury_security_master_20261016.csv")
    s2i = {r["sedol"]: r["isin"] for r in master}
    seg = {r["isin"]: r["market_segment"] for r in master}
    acc_h = {"THB-MRUKE-ASHC": "V", "THB-MRUKE-FENN": "G"}
    acc_n = {"NDS-0447118": "V", "NDS-0447126": "G"}
    pos = {}
    for r in rows(t, "holloway_safekeeping_positions_2025-26.csv"):
        pos[(dmy(r["Position Date"]), acc_h[r["Account"]], s2i[r["SEDOL"]])] = (int(r["Settled Holding"]),
                                                                                 float(r["Market Value (GBP)"]))
    for r in rows(t, "northcote_positions_daily_2026.csv"):
        pos[(ISO(r["as_of_date"]), acc_n[r["account_id"]], r["isin"])] = (int(r["quantity_settled"]),
                                                                          float(r["market_value_gbp"]))
    feed = rows(t, "corporate_actions_feed_20261016.csv")
    by_pay = {(r["isin"], r["payment_date"]): r for r in feed if r["event_type"].startswith("CASH DIVIDEND")}
    inc = {}
    # Holloway's entitlement report for its own months, as the custodian booked them
    for r in rows(t, "holloway_income_entitlements_2025-26.csv"):
        q = quarter(dmy(r["Ex Date"]))
        if q:
            k = (acc_h[r["Account"]], q)
            inc[k] = inc.get(k, 0.0) + float(r["Gross Amount (GBP)"])
    # Northcote's receipts and scrip, dated by the feed's ex-date, for ex-dates from April
    for r in rows(t, "northcote_custody_statement_2026.csv"):
        if r["transaction_type"] not in ("DIVIDEND", "SCRIP DIVIDEND"):
            continue
        ev = by_pay.get((r["isin"], r["value_date"]))
        if ev is None:
            continue
        ex = ISO(ev["ex_date"])
        if ex < dt.date(2026, 4, 1):
            continue
        q = quarter(ex)
        if not q:
            continue
        tag = acc_n[r["account_id"]]
        if r["transaction_type"] == "DIVIDEND":
            amt = float(r["net_amount_gbp"])
        else:
            h = pos.get((ex, tag, r["isin"]), (0, 0))[0]
            amt = round(h * float(r["income_rate_gbp"]), 2)
        inc[(tag, q)] = inc.get((tag, q), 0.0) + amt
    # dividends of the year still unpaid at the extract, on the holding at the ex-date
    for r in feed:
        if not r["event_type"].startswith("CASH DIVIDEND") or ISO(r["payment_date"]) <= dt.date(2026, 10, 16):
            continue
        ex = ISO(r["ex_date"])
        q = quarter(ex)
        if not q:
            continue
        for tag in "VG":
            h = pos.get((ex, tag, r["isin"]))
            if h:
                inc[(tag, q)] = inc.get((tag, q), 0.0) + round(h[0] * float(r["gross_rate"]) / 100, 2)

    def back(d):
        k = 0
        while k < 2:
            d -= dt.timedelta(days=1)
            if d.weekday() < 5:
                k += 1
        return d
    cost = {}
    for r in rows(t, "holloway_settled_transactions_2025-26.csv"):
        if r["Transaction Type"] in ("PURCHASE", "SALE"):
            q = quarter(back(dmy(r["Settlement Date"])))
            if q:
                k = (acc_h[r["Account"]], q)
                cost[k] = cost.get(k, 0.0) + float(r["Commission (GBP)"]) + float(r["Stamp Duty (GBP)"])
    open_ = {}
    for r in rows(t, "holloway_open_trades_31mar2026.csv"):
        open_[(acc_h[r["Account"]], s2i[r["SEDOL"]], int(r["Quantity"]), r["Consideration (GBP)"])] = dmy(r["Trade Date"])
    for r in rows(t, "northcote_custody_statement_2026.csv"):
        if r["transaction_type"] in ("BUY", "SELL"):
            tag = acc_n[r["account_id"]]
            td = open_.pop((tag, r["isin"], abs(int(r["quantity"])), r["gross_amount_gbp"]), None) or back(ISO(r["value_date"]))
            q = quarter(td)
            if q:
                cost[(tag, q)] = cost.get((tag, q), 0.0) + float(r["commission_gbp"]) + float(r["sdrt_gbp"])
    aim = {}
    for q, qe in (("Q1", dt.date(2025, 12, 31)), ("Q2", dt.date(2026, 3, 31)), ("Q3", dt.date(2026, 6, 30)),
                  ("Q4", dt.date(2026, 9, 30))):
        tot = a = 0.0
        n = 0
        for (d, tag, isin), (h, mv) in pos.items():
            if d == qe and tag == "G":
                tot += mv
                if seg[isin] == "AIM":
                    a += mv
                    n += 1
        aim[q] = (n, round(a / tot * 100, 1))
    out = {}
    for (tag, q), v in inc.items():
        out["inc_%s_%s" % (tag, q)] = int(round(v / 1000) * 1000)
    for (tag, q), v in cost.items():
        out["cost_%s_%s" % (tag, q)] = int(round(v / 100) * 100)
    for q, (n, p) in aim.items():
        out["aim_n_" + q] = n
        out["aim_pct_" + q] = p
    return out


def mirror_main(t):
    """rung 1: the linked attribution's effects, each change priced at its component's effect"""
    val = rows(t, "thornbury_mruke_valuation_summary.csv")
    V = {ISO(r["valuation_date"]): {k: float(v) for k, v in r.items() if k.endswith("gbp")} for r in val}
    days = sorted(V)
    cls = {(ISO(r["valuation_date"]), r["share_class"]): float(r["price_gbx"])
           for r in rows(t, "thornbury_mruke_share_class_prices.csv")}
    ix = {ISO(r["date"]): float(r["level"]) for r in rows(t, "larkspur_index_levels_2025-26.csv")
          if r["index_code"] == "LKUKAS" and r["return_type"] == "TR" and r["calculation"] == "12:00"}
    mmf = {ISO(r["date"]): float(r["one_day_yield_annualised_pct"]) / 100
           for r in rows(t, "sterling_liquidity_fund_daily_yield.csv")}
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(t, "merrow_overlay_daily_monitor_2025-26.xlsx"), read_only=True).active
    mon = {}
    for row in ws.iter_rows(min_row=6, values_only=True):
        if row[0] is None:
            continue
        d = row[0].date()
        mon[d] = dict(code=row[7], n=int(row[8] or 0), mark=row[9], dd=row[4], state=row[5], marks={row[12]: row[13],
                                                                                                    row[14]: row[15]})
    y0, y1 = dt.date(2025, 9, 30), dt.date(2026, 9, 30)
    k0, k1 = days.index(y0), days.index(y1)
    eff = dict(A=0.0, B=0.0, C=0.0, D=0.0, E=0.0)
    within6 = False
    for j in range(k0 + 1, k1 + 1):
        d, dp = days[j], days[j - 1]
        nav0 = V[dp]["net_asset_value_gbp"]
        wv = (V[dp]["value_sleeve_gbp"] + V[dp]["value_sleeve_transfer_gbp"]) / nav0
        wg = (V[dp]["growth_sleeve_gbp"] + V[dp]["growth_sleeve_transfer_gbp"]) / nav0
        rb = ix[d] / ix[dp] - 1
        rv = V[d]["value_sleeve_gbp"] / (V[dp]["value_sleeve_gbp"] + V[dp]["value_sleeve_transfer_gbp"]) - 1
        rg = V[d]["growth_sleeve_gbp"] / (V[dp]["growth_sleeve_gbp"] + V[dp]["growth_sleeve_transfer_gbp"]) - 1
        m = mon[dp]
        pnl = m["n"] * (mon[d]["marks"].get(m["code"], mon[d]["mark"]) - m["mark"]) * 10 if m["n"] else 0.0
        eff["A"] -= wv * (rv - rb)
        eff["B"] -= wg * (rg - rb)
        eff["C"] -= pnl / nav0
        if m["state"] == "REDUCED" and m["dd"] <= 6.0:
            within6 = True
        if within6 and m["state"] == "REDUCED":
            eff["D"] -= pnl / nav0
        eff["E"] -= (1 - wv - wg) * (mmf[d] * (d - dp).days / 365 - rb)
    out = {c: v * 1e4 for c, v in eff.items()}
    r10 = lambda x: int((x / 10 + 0.5) // 1 * 10)
    rbacc = cls[(y1, "B Acc")] / cls[(y0, "B Acc")] - 1
    rbench = ix[y1] / ix[y0] - 1
    order = sorted(out, key=lambda c: -out[c])
    res = {"bp_" + c: r10(v) for c, v in out.items()}
    res.update(call=order[0], runner_up=order[1], gap_bp=r10(out[order[0]] - out[order[1]]),
               short_bp=r10((rbench - rbacc) * 1e4))
    return res


def main():
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    zp = os.path.join(TASK, "target.zip")
    stamp = hashlib.md5(open(zp, "rb").read()).hexdigest()[:8] if os.path.exists(zp) else "no zip"
    ask_keys = sorted(k for k in figs if k.startswith(("inc_", "cost_", "aim_")))
    main_keys = ["call", "runner_up", "gap_bp", "short_bp", "bp_A", "bp_B", "bp_C", "bp_D", "bp_E"]
    chart_parts = 3
    cr = cracker_asks(t)
    kept = [k for k in ask_keys if cr.get(k) == figs[k]]
    per_ask = {}
    for k in ask_keys:
        a = k.split("_")[0]
        per_ask.setdefault(a, [0, 0])
        per_ask[a][1] += 1
        per_ask[a][0] += k in kept
    mi = mirror_main(t)
    m_main = [k for k in main_keys if mi.get(k) == figs[k]]
    n_main = len(main_keys) + chart_parts
    cracker = W_MAIN + W_IF + W_ASK * len(kept) / len(ask_keys)
    mirror = W_MAIN * (len(m_main) + chart_parts) / n_main + W_IF + W_ASK * len(kept) / len(ask_keys)
    print("ceiling.py on %s (target.zip %s)" % (t, stamp))
    for a, (k, n) in per_ask.items():
        print("  ask %-5s cracker keeps %d of %d" % (a, k, n))
    for k in ask_keys:
        print("    %-12s golden %-10s cracker %s" % (k, figs[k], cr.get(k)))
    print("  mirror (rung 1) main side keeps %d of %d: %s" % (len(m_main) + chart_parts, n_main, ", ".join(m_main)))
    print("  mirror's call %s, runner-up %s, figures %s" % (mi["call"], mi["runner_up"],
                                                          {k: mi[k] for k in mi if k.startswith("bp_")}))
    print("  cracker %.1f, mirror %.1f, pair ceiling %.1f" % (cracker, mirror, (cracker + mirror) / 2))
    print("  mirror leakage %.1f per cent of ask weight" % (100.0 * len(kept) / len(ask_keys)))


if __name__ == "__main__":
    main()
