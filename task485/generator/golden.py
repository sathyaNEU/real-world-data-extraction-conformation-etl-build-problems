"""The golden and every route on the ladder, computed from the records as the pack ships them (the returns' coal
burned, the 2026 receipts' delivered-weighted sulphur, the quarry tickets and certificates, the silo stocks, the
tests and the permits), never from the world's daily truth. balance() takes every convention as an option, so the
fork table and the Layer 1 handlings run through one computation."""
import numpy as np

import world as W

M = W.MSO2 / W.MS


def iso_week(d):
    return W.day(d).isocalendar()[1]


def site_sulphur(lots, weighted=True, window="received", skip=None):
    """each site's sulphur, per cent as received: weighted by tonnes (guidance 4.2) or a plain mean over rows; lots
    received in 2026 (guidance 4.2), dispatched in 2026, or every row in the collation"""
    out = {}
    for site in sorted(set(x["site"] for x in lots)):
        if window == "received":
            xs = [x for x in lots if x["site"] == site and 0 <= x["received"] <= 364]
        elif window == "dispatched":
            xs = [x for x in lots if x["site"] == site and 0 <= x["dispatched"] <= 364]
        else:
            xs = [x for x in lots if x["site"] == site]
        if skip:
            xs = [x for x in xs if x["lot"] not in skip]
        if weighted:
            out[site] = sum(x["t"] * x["s"] for x in xs) / sum(x["t"] for x in xs)
        else:
            out[site] = float(np.mean([x["s"] for x in xs]))
    return out


def coal_burned(rets, gas_oil=False):
    out = {}
    for r in rets:
        out[r["boiler"]] = out.get(r["boiler"], 0) + r["coal_burned"] + (r["oil"] if gas_oil and r["quarter"] >= 3 else 0)
    return out


def coal_from_receipts(lots, rets):
    """receipts in 2026 less the yard's stock change, a two-boiler site's yard split by the returns' coal burned"""
    cb = coal_burned(rets)
    out = {}
    for site in sorted(set(r["site"] for r in rets)):
        rec = sum(x["t"] for x in lots if x["site"] == site and 0 <= x["received"] <= 364)
        first = [r for r in rets if r["site"] == site and r["unit"] == 1]
        q1 = [r for r in first if r["quarter"] == 1][0]
        q4 = [r for r in first if r["quarter"] == 4][0]
        burned = rec - (q4["coal_close"] - q1["coal_open"])
        bs = sorted(b for b in cb if b.startswith(site + "-"))
        tot = sum(cb[b] for b in bs)
        for b in bs:
            out[b] = burned * cb[b] / tot
    return out


def limestone(rets, tickets, purity, stock_change=True, purity_mode="weekly", moisture=None):
    """calcium carbonate each scrubber consumed in 2026, t: tickets less the silo's stock change, each ticket at its
    ISO week's certified purity as delivered (or the year's plain mean, or weeks counted from 1 January, or with the
    week's moisture taken off as if the purity were dry)"""
    cons, caco3 = {}, {}
    for b in sorted(set(r["boiler"] for r in rets)):
        ts = [x for x in tickets if x["boiler"] == b]
        tons = sum(x["t"] for x in ts)
        q = ts[0]["quarry"]
        pur_t = 0.0
        for x in ts:
            if purity_mode == "weekly":
                p = purity[q][iso_week(x["day"])]
            elif purity_mode == "jan1":
                p = purity[q][min(53, x["day"] // 7 + 1)]
            else:
                p = float(np.mean(purity[q][1:54]))
            if moisture is not None:
                p = p * (1 - moisture[q][iso_week(x["day"])] / 100)
            pur_t += x["t"] * p / 100
        q1 = [r for r in rets if r["boiler"] == b and r["quarter"] == 1][0]
        q4 = [r for r in rets if r["boiler"] == b and r["quarter"] == 4][0]
        dstock = (q4["ls_close"] - q1["ls_open"]) if stock_change else 0.0
        used = tons - dstock
        cons[b] = used
        caco3[b] = pur_t / tons * used
    return cons, caco3


def balance(w, rets, tickets, permits, lots=None, purity=None, *, weighted=True, window="received", skip=None,
            coal="returns", gas_oil=False, stock_change=True, purity_mode="weekly", moisture=None, ratio_one=False,
            as_caco3=False, mcaco3=W.MCACO3, mratio=M):
    """each boiler's sulphur dioxide leaving the stack over 2026, t, on the reagent balance: the sulphur fired less the
    ash's share, less the sulphur dioxide removed (the calcium carbonate consumed over the scrubber's moles per mole
    removed). Returns {boiler: dict(formed, removed, so2, s_gas, caco3, cons)}."""
    lots = w.lots if lots is None else lots
    purity = w.purity if purity is None else purity
    S = site_sulphur(lots, weighted, window, skip)
    cb = coal_burned(rets, gas_oil) if coal == "returns" else coal_from_receipts(lots, rets)
    per = {p["boiler"]: p for p in permits}
    cons, caco3 = limestone(rets, tickets, purity, stock_change, purity_mode, moisture)
    out = {}
    for b in sorted(cb):
        p = per[b]
        s_gas = cb[b] * S[b.split("-")[0]] / 100 * (1 - p["ash_ret"])
        reagent = cons[b] if as_caco3 else caco3[b]
        removed = reagent / mcaco3 / (1.0 if ratio_one else p["ratio"]) * W.MS * mratio
        formed = s_gas * mratio
        out[b] = dict(formed=formed, removed=removed, so2=formed - removed, s_gas=s_gas, caco3=caco3[b], cons=cons[b])
    return out


def routes(w, rets, tickets, tests, permits):
    """every route's 2026 sulphur dioxide per boiler, t"""
    S = site_sulphur(w.lots)
    cb = coal_burned(rets)
    per = {p["boiler"]: p for p in permits}
    tst = {x["boiler"]: x for x in tests}
    hours = {}
    for r in rets:
        hours[r["boiler"]] = hours.get(r["boiler"], 0) + r["hours"]
    gold = balance(w, rets, tickets, permits)
    alt = dict(golden_no_stock=balance(w, rets, tickets, permits, stock_change=False),
               golden_mean_purity=balance(w, rets, tickets, permits, purity_mode="mean"),
               golden_mean_sulphur=balance(w, rets, tickets, permits, weighted=False),
               golden_ratio_one=balance(w, rets, tickets, permits, ratio_one=True),
               golden_limestone_as_caco3=balance(w, rets, tickets, permits, as_caco3=True))
    out = {}
    for b in sorted(cb):
        p = per[b]
        s_gas = cb[b] * S[b.split("-")[0]] / 100 * (1 - p["ash_ret"])
        x = tst[b]
        test_rate = x["so2_out"] * x["flow"] / 1e9      # t per hour: mg/Nm3 times Nm3/h, both at the report's oxygen
        out[b] = dict(none=s_gas * M, design=s_gas * (1 - p["design"]) * M, tested=s_gas * (1 - x["removal"] / 100) * M,
                      test_rate=test_rate * hours[b], golden=gold[b]["so2"], s_gas=s_gas, caco3=gold[b]["caco3"],
                      cons=gold[b]["cons"])
        for k, v in alt.items():
            out[b][k] = v[b]["so2"]
    return out


def listed(rt, key, line=W.LINE):
    return sorted(b for b in rt if rt[b][key] >= line)


def listed_of(bal, line=W.LINE):
    return sorted(b for b in bal if bal[b]["so2"] >= line)
