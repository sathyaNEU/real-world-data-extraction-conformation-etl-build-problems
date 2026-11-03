"""Cut the evidence pack into target/: every file as the system that produces it writes it."""
import csv
import datetime as dt
import io
import os

import numpy as np

import docs as DOCS
import fund as F
import postprocess as PP
import records as R
import world as W
from world import D, DAYS, IDX

HOLLOWAY_ACC = {"V": ("THB-MRUKE-ASHC", "THORNBURY MR UK EQ - ASHCOMBE"),
                "G": ("THB-MRUKE-FENN", "THORNBURY MR UK EQ - FENNICK")}
NORTHCOTE_ACC = {"V": "NDS-0447118", "G": "NDS-0447126"}
CLASS_ISIN = {"B Acc": "GB00BQ7K2M41", "B Inc": "GB00BQ7K2N57", "C Acc": "GB00BQ7K2P71", "C Inc": "GB00BQ7K2Q88"}
LAST_HOLLOWAY = D(2026, 3, 31)


def write_csv(path, header, rows, crlf=False):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())


def m2(x):
    return "%.2f" % (round(x + 0.0, 2) + 0.0)


def dmy(d):
    return d.strftime("%d/%m/%Y")


def gbx(p):
    return "%.2f" % p if p >= 20 else "%.3f" % p


# ------------------------------------------------------------------------------------------------- identities
def dress(world):
    """nominal values, incorporation and the custodians' descriptions"""
    r = W.rng("dress")
    for s in world["secs"]:
        s["nominal"] = [1, 5, 10, 10, 20, 25, 25, 50, 100][int(r.integers(9))]
        inc = "GB"
        if s["name"] != "Penrose Bank plc" and r.random() < 0.06:
            inc = "JE" if r.random() < 0.6 else "GG"
        s["inc"] = inc
        if inc != "GB":
            body = inc + "00" + s["sedol"]
            s["isin"] = body + W.isin_check(body)
        nm = s["name"]
        base = nm.upper().replace(" PLC", "").replace(" LIMITED", "")
        tail = "PLC" if nm.endswith("plc") else "LTD"
        nom = ("%dP" % s["nominal"]) if s["nominal"] < 100 else "GBP1"
        s["hdesc"] = ("%s %s ORD %s" % (base, tail, nom))[:40]
        s["ndesc"] = "%s Ordinary %s" % (nm, ("%dp" % s["nominal"]) if s["nominal"] < 100 else "GBP1")
        s["industry_now"] = s["industry"]
    for sid, old, new in world["reclass"]:
        [x for x in world["secs"] if x["sid"] == sid][0]["industry_now"] = new


def close_px(world, act, sid, i):
    if sid == act["pen"] and DAYS[i] >= W.PENROSE_SUSPENDED:
        return world["closes"][sid][IDX[D(2026, 3, 13)]]
    return world["closes"][sid][i]


# ------------------------------------------------------------------------------------------------- custody
def holloway_positions(out, S):
    world, act, settled = S["world"], S["act"], S["settled"]
    secmap = {s["sid"]: s for s in world["secs"]}
    rows = []
    for i, d in enumerate(DAYS):
        if d > LAST_HOLLOWAY:
            break
        day = sorted(((tag, secmap[sid]["sedol"], sid, q) for (j, tag, sid), q in settled.items() if j == i))
        for tag, sedol, sid, q in day:
            p = close_px(world, act, sid, i)
            rows.append([dmy(d), HOLLOWAY_ACC[tag][0], HOLLOWAY_ACC[tag][1], sedol, secmap[sid]["hdesc"], q, gbx(p),
                         m2(q * p / 100)])
    write_csv(os.path.join(out, "holloway_safekeeping_positions_2025-26.csv"),
              ["Position Date", "Account", "Account Name", "SEDOL", "Security Description", "Settled Holding",
               "Price (GBX)", "Market Value (GBP)"], rows, crlf=True)
    return len(rows)


def northcote_positions(out, S):
    world, act, settled = S["world"], S["act"], S["settled"]
    secmap = {s["sid"]: s for s in world["secs"]}
    rows = []
    for i, d in enumerate(DAYS):
        if d < W.CUSTODY_SWITCH:
            continue
        day = sorted(((NORTHCOTE_ACC[tag], secmap[sid]["isin"], sid, q) for (j, tag, sid), q in settled.items()
                      if j == i))
        for acc, isin, sid, q in day:
            p = round(close_px(world, act, sid, i) / 100, 4)
            rows.append([d.isoformat(), acc, isin, secmap[sid]["ndesc"], q, "%.4f" % p, m2(q * p)])
    write_csv(os.path.join(out, "northcote_positions_daily_2026.csv"),
              ["as_of_date", "account_id", "isin", "security_name", "quantity_settled", "price_gbp", "market_value_gbp"],
              rows)
    return len(rows)


def holloway_transactions(out, S):
    world, act = S["world"], S["act"]
    secmap = {s["sid"]: s for s in world["secs"]}
    r = W.rng("hollref")
    rows = []
    for t in act["trades"]:
        if t["settle"] > LAST_HOLLOWAY or t["settle"] < W.HIST_START:
            continue
        s = secmap[t["sid"]]
        acc = HOLLOWAY_ACC[t["sleeve"]][0]
        if t["side"] == "X":
            rows.append((t["settle"], acc, "CAPITAL REORG - SHARES CANCELLED", s["sedol"], s["hdesc"], -t["qty"], "", "0.00",
                         "0.00", "0.00", "0.00"))
            continue
        if t["side"] not in ("B", "S"):
            continue
        typ = "PURCHASE" if t["side"] == "B" else "SALE"
        net = t["cons"] + t["comm"] + t["sdrt"] if t["side"] == "B" else t["cons"] - t["comm"]
        rows.append((t["settle"], acc, typ, s["sedol"], s["hdesc"], t["qty"] if t["side"] == "B" else -t["qty"],
                     gbx(t["price"]), m2(t["cons"]), m2(t["comm"]), m2(t["sdrt"]),
                     m2(-net if t["side"] == "B" else net)))
    rows.sort(key=lambda x: (x[0], x[1], x[3], x[2]))
    out_rows = []
    ref = 7_310_000
    for x in rows:
        ref += int(r.integers(1, 30))
        out_rows.append([dmy(x[0])] + list(x[1:]) + ["HT%08d" % ref])
    write_csv(os.path.join(out, "holloway_settled_transactions_2025-26.csv"),
              ["Settlement Date", "Account", "Transaction Type", "SEDOL", "Security Description", "Quantity",
               "Price (GBX)", "Consideration (GBP)", "Commission (GBP)", "Stamp Duty (GBP)", "Net Amount (GBP)",
               "Holloway Ref"], out_rows, crlf=True)


def holloway_open_trades(out, S):
    world, act = S["world"], S["act"]
    secmap = {s["sid"]: s for s in world["secs"]}
    rows = []
    for t in act["trades"]:
        if t["side"] not in ("B", "S") or not (t["day"] <= LAST_HOLLOWAY < t["settle"]):
            continue
        s = secmap[t["sid"]]
        net = t["cons"] + t["comm"] + t["sdrt"] if t["side"] == "B" else t["cons"] - t["comm"]
        rows.append([dmy(t["day"]), dmy(W.settle_date(t["day"])), HOLLOWAY_ACC[t["sleeve"]][0], s["sedol"], s["hdesc"],
                     "BUY" if t["side"] == "B" else "SELL", t["qty"], gbx(t["price"]), m2(t["cons"]), m2(t["comm"]),
                     m2(t["sdrt"]), m2(net), "INSTRUCTION PASSED TO SUCCESSOR"])
    rows.sort(key=lambda x: (x[0][6:] + x[0][3:5] + x[0][:2], x[2], x[3]))
    write_csv(os.path.join(out, "holloway_open_trades_31mar2026.csv"),
              ["Trade Date", "Contractual Settlement Date", "Account", "SEDOL", "Security Description", "Buy/Sell",
               "Quantity", "Price (GBX)", "Consideration (GBP)", "Commission (GBP)", "Stamp Duty (GBP)",
               "Net Amount (GBP)", "Status"], rows, crlf=True)
    return len(rows)


def holloway_income(out, S):
    world, act = S["world"], S["act"]
    secmap = {s["sid"]: s for s in world["secs"]}
    rows = []
    for e in S["ent"]:
        if e["ex"] > LAST_HOLLOWAY or e["ex"] < W.HIST_START:
            continue
        if e["sid"] in S["scrip_offer"]:
            continue                  # elective events run through Holloway's voluntary events desk, not this report
        s = secmap[e["sid"]]
        status = "PAID" if e["pay"] <= LAST_HOLLOWAY else "DUE"
        rows.append((e["ex"], e["pay"], HOLLOWAY_ACC[e["sleeve"]][0], s["sedol"], s["hdesc"], e["shares"],
                     "%.4f" % e["pence"], m2(e["gbp"]), status))
    rows.sort(key=lambda x: (x[0], x[2], x[3]))
    write_csv(os.path.join(out, "holloway_income_entitlements_2025-26.csv"),
              ["Ex Date", "Pay Date", "Account", "SEDOL", "Security Description", "Entitled Holding", "Rate (GBX)",
               "Gross Amount (GBP)", "Status"],
              [[dmy(x[0]), dmy(x[1])] + list(x[2:]) for x in rows], crlf=True)


def northcote_statement(out, S):
    world, act, settled = S["world"], S["act"], S["settled"]
    secmap = {s["sid"]: s for s in world["secs"]}
    rows = []
    i31 = IDX[LAST_HOLLOWAY]
    for (j, tag, sid), q in settled.items():
        if j == i31:
            rows.append((W.CUSTODY_SWITCH, NORTHCOTE_ACC[tag], "RECEIVE FREE", secmap[sid]["isin"], secmap[sid]["ndesc"],
                         q, "", "", "", "", "0.00", ""))
    for t in act["trades"]:
        if t["settle"] < W.CUSTODY_SWITCH or t["settle"] > W.EXTRACT_END:
            continue
        s = secmap[t["sid"]]
        acc = NORTHCOTE_ACC[t["sleeve"]]
        if t["side"] == "SCRIP":
            ev = [e for e in S["ent"] if e["sid"] == t["sid"] and e["sleeve"] == t["sleeve"] and e["pay"] == t["day"]][0]
            rows.append((t["day"], acc, "SCRIP DIVIDEND", s["isin"], s["ndesc"], t["qty"], "", "", "", "", "0.00",
                         "%.6f" % (ev["pence"] / 100)))
            continue
        if t["side"] not in ("B", "S"):
            continue
        net = t["cons"] + t["comm"] + t["sdrt"] if t["side"] == "B" else t["cons"] - t["comm"]
        rows.append((t["settle"], acc, "BUY" if t["side"] == "B" else "SELL", s["isin"], s["ndesc"],
                     t["qty"] if t["side"] == "B" else -t["qty"], "%.4f" % (t["price"] / 100), m2(t["cons"]),
                     m2(t["comm"]), m2(t["sdrt"]), m2(-net if t["side"] == "B" else net), ""))
    scrip_keys = {(t["sleeve"], t["sid"], t["day"]) for t in act["trades"] if t["side"] == "SCRIP"}
    for e in S["ent"]:
        if e["never_paid"] or not (W.CUSTODY_SWITCH <= e["pay"] <= W.EXTRACT_END):
            continue
        if (e["sleeve"], e["sid"], e["pay"]) in scrip_keys:
            continue
        s = secmap[e["sid"]]
        rows.append((e["pay"], NORTHCOTE_ACC[e["sleeve"]], "DIVIDEND", s["isin"], s["ndesc"], e["shares"], "", "", "", "",
                     m2(e["gbp"]), "%.6f" % (e["pence"] / 100)))
    order = {"RECEIVE FREE": 0, "BUY": 1, "SELL": 2, "DIVIDEND": 3, "SCRIP DIVIDEND": 4}
    rows.sort(key=lambda x: (x[0], x[1], order[x[2]], x[3], str(x[5])))
    r = W.rng("ndsref")
    ref = 50_220_000
    out_rows = []
    for x in rows:
        ref += int(r.integers(1, 12))
        out_rows.append([x[0].isoformat()] + list(x[1:]) + ["NDS%09d" % ref])
    write_csv(os.path.join(out, "northcote_custody_statement_2026.csv"),
              ["value_date", "account_id", "transaction_type", "isin", "security_name", "quantity", "price_gbp",
               "gross_amount_gbp", "commission_gbp", "sdrt_gbp", "net_amount_gbp", "income_rate_gbp", "northcote_ref"],
              out_rows)


# ------------------------------------------------------------------------------------------------- reference data
def corporate_actions(out, S):
    world, act = S["world"], S["act"]
    r = W.rng("corpact")
    scrip_offer = S["scrip_offer"]
    scrip_ref = {(sid, ex): ref for (tag, sid, ex), ref in act["scrip"].items()}
    rows = []
    for s in world["secs"]:
        if s["name"] == "Penrose Bank plc":
            continue
        for ev in world["divs"][s["sid"]]:
            if ev.get("pence", 0) <= 0:
                continue
            ann = ev["ex"] - dt.timedelta(days=int(r.integers(16, 52)))
            typ = "CASH DIVIDEND"
            det = "Interim" if ev["frac"] < 0.5 else "Final"
            if s["sid"] in scrip_offer:
                typ = "CASH DIVIDEND WITH SCRIP ALTERNATIVE"
                ref = scrip_ref.get((s["sid"], ev["ex"]))
                if ref is None:
                    j = IDX.get(ev["ex"])
                    ref = round(float(np.mean(world["prices"][s["sid"]][j:j + 5])) / 100, 4) if j is not None else None
                if ref is not None:
                    det += "; scrip reference price %.2fp" % (ref * 100)
            status = "PAID" if ev["pay"] <= W.EXTRACT_END else "CONFIRMED"
            rows.append([s["isin"], s["sedol"], s["name"], typ, ann.isoformat(), ev["ex"].isoformat(),
                         W.settle_date(ev["ex"], 1).isoformat(), ev["pay"].isoformat(), "", "%.4f" % ev["pence"], "GBX",
                         det, status])
    for sid, (eff, new, old) in world["moves"].items():
        s = [x for x in world["secs"] if x["sid"] == sid][0]
        ann = eff - dt.timedelta(days=24)
        rows.append([s["isin"], s["sedol"], s["name"], "LISTING TRANSFER", ann.isoformat(), "", "", "", eff.isoformat(),
                     "", "", "Admission of ordinary shares to the Official List (premium) and to trading on the Main "
                     "Market; cancellation of admission to trading on AIM", "COMPLETE"])
    rows.sort(key=lambda x: (x[5] or x[8], x[0], x[3]))
    rid = 880_000
    out_rows = []
    for x in rows:
        rid += int(r.integers(1, 40))
        out_rows.append(["CA%07d" % rid] + x)
    write_csv(os.path.join(out, "corporate_actions_feed_20261016.csv"),
              ["event_id", "isin", "sedol", "issuer", "event_type", "announcement_date", "ex_date", "record_date",
               "payment_date", "effective_date", "gross_rate", "rate_currency", "details", "event_status"], out_rows)


def security_master(out, S):
    world = S["world"]
    rows = []
    for s in sorted(world["secs"], key=lambda s: s["sedol"]):
        seg = W.market_on(s, W.EXTRACT_END, world["moves"])
        status = "ACTIVE"
        if s["name"] == "Penrose Bank plc":
            status = "CANCELLED 2026-03-23"
            seg = "Main Market"
        rows.append([s["sedol"], s["isin"], s["tidm"], s["name"], s["industry_now"], seg, s["inc"], status])
    write_csv(os.path.join(out, "thornbury_security_master_20261016.csv"),
              ["sedol", "isin", "tidm", "issuer_name", "larkspur_industry", "market_segment", "country_of_incorporation",
               "status"], rows)


def index_levels(out, S):
    ix = S["world"]["ix"]
    rows = []
    series = [("LKUKAS", "Larkspur UK All-Share", "TR", "12:00", "tr_noon"), ("LKUKAS", "Larkspur UK All-Share", "TR",
                                                                                "CLOSE", "tr_close"),
              ("LKUKAS", "Larkspur UK All-Share", "PR", "CLOSE", "pr_close"),
              ("LK100", "Larkspur 100", "PR", "12:00", "l100_noon"), ("LK100", "Larkspur 100", "PR", "CLOSE", "l100_close"),
              ("LKUKV", "Larkspur UK Value", "TR", "CLOSE", "val_close"),
              ("LKUKG", "Larkspur UK Growth", "TR", "CLOSE", "gro_close")]
    for i, d in enumerate(DAYS):
        for code, name, typ, when, key in series:
            v = ix[key][i]
            rows.append([d.isoformat(), code, name, typ, when, ("%.1f" % v) if code == "LK100" else ("%.2f" % v)])
    write_csv(os.path.join(out, "larkspur_index_levels_2025-26.csv"),
              ["date", "index_code", "index_name", "return_type", "calculation", "level"], rows)


def liquidity_fund(out, S):
    rows = []
    price = 1.004817
    for i, d in enumerate(DAYS):
        rate = W.mmf_rate(d)
        if i:
            cal = (d - DAYS[i - 1]).days
            price = price * (1 + rate * cal / 365)
        rows.append([d.isoformat(), "%.4f" % (rate * 100), "%.6f" % price])
    write_csv(os.path.join(out, "sterling_liquidity_fund_daily_yield.csv"),
              ["date", "one_day_yield_annualised_pct", "nav_per_unit_gbp"], rows)


# ------------------------------------------------------------------------------------------------- administrator
def fund_valuation(out, S):
    rec = S["act"]["rec"]
    rows = []
    for i, d in enumerate(DAYS):
        rows.append([d.isoformat(), "12:00", m2(rec["V"][i]), m2(rec["G"][i]), m2(rec["C"][i]), m2(rec["L"][i]),
                     m2(rec["NAV"][i]), m2(rec["TV"][i]), m2(rec["TG"][i]), m2(rec["TC"][i])])
    write_csv(os.path.join(out, "thornbury_mruke_valuation_summary.csv"),
              ["valuation_date", "valuation_point", "value_sleeve_gbp", "growth_sleeve_gbp", "liquidity_sleeve_gbp",
               "distributions_payable_gbp", "net_asset_value_gbp", "value_sleeve_transfer_gbp",
               "growth_sleeve_transfer_gbp", "liquidity_sleeve_transfer_gbp"], rows)


def class_prices(out, S):
    act = S["act"]
    rec = act["rec"]
    r = W.rng("grossdeal")
    rows = []
    for i, d in enumerate(DAYS):
        for k in F.CLASSES:
            u = rec["units"][k][i]
            du = u - rec["units"][k][i - 1] if i else 0.0
            gross = abs(du) * float(r.uniform(0.3, 1.6)) if i else 0.0
            created = gross + max(du, 0.0)
            cancelled = gross + max(-du, 0.0)
            xd = rec["dist"].get((d, k), "")
            rows.append([d.isoformat(), k, CLASS_ISIN[k], "%.2f" % rec["price"][k][i], "%.3f" % u,
                         "%.3f" % created, "%.3f" % cancelled, ("%.4f" % xd) if xd != "" else ""])
    write_csv(os.path.join(out, "thornbury_mruke_share_class_prices.csv"),
              ["valuation_date", "share_class", "class_isin", "price_gbx", "units_in_issue", "units_created",
               "units_cancelled", "xd_distribution_gbx"], rows)


# ------------------------------------------------------------------------------------------------- overlay manager
def overlay_report(out, S):
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment
    act, world = S["act"], S["world"]
    rec, marks = act["rec"], world["marks"]
    wb = Workbook()
    ws = wb.active
    ws.title = "Daily monitor"
    ws["A1"] = "Merrow Overlay Services LLP"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Thornbury Managed Risk UK Equity Fund: drawdown overlay, daily monitor at the fund's valuation point"
    ws["A3"] = "Client portfolio manager: Julia Parry. Marks are Larkspur 100 index futures at 12:00 UK time; " \
               "contract value GBP 10 per index point."
    hdr = ["Date", "Fund NAV (GBP)", "B Acc price (p)", "Highest B Acc price, 63 valuation points (p)",
           "Drawdown from high (%)", "Overlay state", "Physical equity (% NAV)", "Contract held", "Contracts held",
           "Mark of contract held", "Futures notional (GBP)", "Equity exposure (% NAV)", "Nearest contract",
           "Nearest contract mark", "Next contract", "Next contract mark"]
    ws.append([])
    ws.append(hdr)
    for c in ws[5]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, d in enumerate(DAYS):
        code = rec["code"][i]
        n = int(rec["ncon"][i])
        mark = marks[code][d] if code else None
        front, fexp = [(c, e) for c, e in W.CONTRACTS if e >= d][0]
        nxt = [c for c, e in W.CONTRACTS if e > fexp][0]
        notional = n * mark * F.MULT if code else 0.0
        ws.append([d, round(rec["NAV"][i], 2), round(rec["price"]["B Acc"][i], 2), round(rec["high"][i], 2),
                   round(rec["dd"][i] * 100, 2), rec["state"][i], round(rec["phys"][i] * 100, 2), code or None, n,
                   mark, round(notional, 2), round(rec["expo"][i] * 100, 2), front,
                   marks[front][d], nxt, marks[nxt][d]])
        ws.cell(row=ws.max_row, column=1).number_format = "dd/mm/yyyy"
    widths = [11, 16, 12, 16, 12, 11, 12, 11, 10, 11, 16, 12, 11, 11, 11, 11]
    for j, w in enumerate(widths):
        ws.column_dimensions[chr(65 + j)].width = w
    ws.freeze_panes = "B6"
    p = os.path.join(out, "merrow_overlay_daily_monitor_2025-26.xlsx")
    wb.save(p)
    PP.normalize_ooxml(p, "Julia Parry", "Julia Parry", "2025-06-02T07:41:00Z", "2026-10-16T13:22:00Z", excel=True,
                       company="Merrow Overlay Services LLP")


def futures_blotter(out, S):
    act = S["act"]
    r = W.rng("blotter")
    rows = []
    tid = 3_300_410
    for t in act["fut_trades"]:
        d = t["day"]
        off = W.uk_offset_hours(d)
        q = t["qty"]
        n = abs(q)
        fills = [n] if n <= 60 else list(np.diff(np.r_[0, np.sort(r.choice(np.arange(1, n), size=min(5, n - 1),
                                                                             replace=False)), n]))
        base = dt.datetime(d.year, d.month, d.day, 12, 0, 0) - dt.timedelta(hours=off)
        stamps = sorted(base + dt.timedelta(seconds=int(x)) for x in r.integers(-150, 240, size=len(fills)))
        for ts, f in zip(stamps, fills):
            rows.append([ts.strftime("%Y-%m-%dT%H:%M:%SZ"), None, t["code"], "SELL" if q < 0 else "BUY",
                         int(f), "%.1f" % t["price"], "Kestle Futures", m2(int(f) * F.FUT_COMMISSION), t["kind"].upper()])
    rows.sort(key=lambda x: x[0])
    for x in rows:
        tid += int(r.integers(1, 9))
        x[1] = "MOS-%d" % tid
    write_csv(os.path.join(out, "merrow_futures_blotter_2026.csv"),
              ["timestamp_utc", "trade_id", "contract", "side", "contracts", "price", "executing_broker",
               "commission_gbp", "order_reason"], rows)


# ------------------------------------------------------------------------------------------------- the cut
def cut(out, S):
    os.makedirs(out, exist_ok=True)
    counts = {}
    counts["holloway_positions"] = holloway_positions(out, S)
    counts["northcote_positions"] = northcote_positions(out, S)
    holloway_transactions(out, S)
    counts["open_trades"] = holloway_open_trades(out, S)
    holloway_income(out, S)
    northcote_statement(out, S)
    corporate_actions(out, S)
    security_master(out, S)
    index_levels(out, S)
    liquidity_fund(out, S)
    fund_valuation(out, S)
    class_prices(out, S)
    overlay_report(out, S)
    futures_blotter(out, S)
    DOCS.write_all(out, S)
    return counts
