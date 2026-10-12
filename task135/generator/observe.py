"""What the systems hold: the custodian's exports, Kestwick's published history, the index levels, the calendars and
the trust's grants and finance extracts, as frames written to the pack by files.py."""
import datetime as dt

import numpy as np
import pandas as pd

import world as W
import book as BK
import grants as GR

ASSET = {"stock": "Equity - UK", "cash": "Cash", "fund": "Collective investment scheme", "rights": "Rights"}


def names(B):
    nm = {c: B.info[c]["name"] for c in B.info}
    nm[BK.RIGHTS_CODE] = "Garrow Banking Group plc nil paid rights"
    nm[BK.CASH_CODE] = "Sterling cash"
    for f, (ci, ca) in B.fcode.items():
        nm[ci] = W.FUNDS[f]["name"] + " Income"
        nm[ca] = W.FUNDS[f]["name"] + " Accumulation"
    return nm


def asset_class(code, B):
    if code == BK.CASH_CODE:
        return ASSET["cash"]
    if code == BK.RIGHTS_CODE:
        return ASSET["rights"]
    if code.startswith("KWC"):
        return ASSET["fund"]
    return ASSET["stock"]


def valuation(B):
    nm = names(B)
    rec = []
    for d, s, c, lot, od, q, p, mv, ai in B.rows:
        if c == BK.CASH_CODE:
            qs = "%.2f" % q
        elif c.startswith("KWC"):
            qs = "%.3f" % q
        else:
            qs = "%d" % q
        rec.append((d.isoformat(), s, c, nm[c], lot, od.isoformat() if od else "", qs, "%.4f" % p, "%.2f" % mv, "%.2f" % ai,
                    asset_class(c, B)))
    df = pd.DataFrame(rec, columns=["valuation_date", "sub_account", "security_code", "security_name", "lot_id",
                                    "lot_open_date", "quantity", "price", "market_value_gbp", "accrued_income_gbp",
                                    "asset_class"])
    return df


def movements(B):
    rows = []
    for d, s, typ, amt, text, code in B.moves:
        rows.append((d.isoformat(), s, typ, "%.2f" % amt, text, code))
    df = pd.DataFrame(rows, columns=["date", "sub_account", "movement_type", "amount_gbp", "narrative", "security_code"])
    order = {"Dividend received": 0, "Cash in lieu": 1, "Takeover consideration": 2, "Contribution": 3, "Sale": 4,
             "Purchase": 5, "Rights subscription": 6, "Withdrawal": 7, "Management fee": 8}
    df["_o"] = df["movement_type"].map(order)
    df["amount_gbp"] = df["amount_gbp"].astype(str)
    df = df.sort_values(["date", "sub_account", "_o"], kind="stable").drop(columns="_o").reset_index(drop=True)
    return df


def corporate_events(B):
    co_ref, co_code, co_eff, co_ratio = W.CONSOLIDATION
    dm_ref, dm_code, dm_ex, dm_ratio, dm_share = W.DEMERGER
    ri_ref, ri_code, ri_ex, ri_take, ri_ratio, ri_disc = W.RIGHTS
    tk_ref, tk_code, tk_ann, tk_eff, tk_prem = W.TAKEOVER
    dm_credit = W.add_bdays(dm_ex, 1)
    rows = [
        (co_ref, co_code, "SPLR", co_eff.isoformat(), co_eff.isoformat(),
         "1 new ordinary share for every %d existing; fractions aggregated and sold, cash distributed" % co_ratio, ""),
        (dm_ref, dm_code, "SOFF", dm_ex.isoformat(), dm_credit.isoformat(),
         "1 Larkfield Land plc share for every %d Larkfield Housebuilders plc shares held at the record date; "
         "base cost apportioned %.1f:%.1f" % (dm_ratio, 100 * (1 - dm_share), 100 * dm_share), W.DEMERGED[0]),
        (ri_ref, ri_code, "RHTS", ri_ex.isoformat(), ri_take.isoformat(),
         "1 new share for every %d held at GBP %.2f per new share; nil paid rights %s, taken up in full"
         % (ri_ratio, B.ri_sub, BK.RIGHTS_CODE), BK.RIGHTS_CODE),
        (tk_ref, tk_code, "MRGR", tk_eff.isoformat(), tk_eff.isoformat(),
         "Scheme of arrangement: GBP %.2f in cash for each share; announced %s" % (B.offer, tk_ann.strftime("%d %b %Y")), ""),
    ]
    return pd.DataFrame(rows, columns=["event_ref", "security_code", "action_type", "ex_date", "effective_date", "terms",
                                       "new_security_code"])


def fund_events(B, M):
    """each Kestwick distribution as the custodian books it: one line per designation (funds are not lot-tracked)"""
    out = []
    fidx = {d: k for k, d in enumerate(M["days"])}
    refno = 77310
    for f in W.FUNDS:
        fp = B.fp[f]
        for ex in fp["exd"]:
            if not (W.WIN_START < ex <= W.VAL_DATE):
                continue
            k = fidx[ex]
            refno += 37
            pay = ex + dt.timedelta(days=45 if f in ("GILT", "CORP") else 58)
            while not W.is_bday(pay, "UK"):
                pay += dt.timedelta(days=1)
            per_inc = fp["dist"][k]
            for s in W.SUB_ACCOUNTS:
                u = units_at(B, s, f, ex)
                if W.SUB_UNIT[s] == "inc":
                    amt = round(u * per_inc, 2)
                    typ, code = "Distribution", B.fcode[f][0]
                else:
                    per_acc = per_inc * fp["acc"][k] / (fp["inc"][k] + per_inc)
                    amt = round(u * per_acc, 2)
                    typ, code = "Accumulation", B.fcode[f][1]
                out.append(dict(sub=s, code=code, ref="KD%06d" % refno, type=typ, ex=ex, pay=pay, amount=amt, fund=f))
    return out


def units_at(B, s, f, d):
    """units held at the close before d (the record), from the valuation rows"""
    best = None
    for row in B.unit_hist[(s, f)]:
        if row[0] < d:
            best = row[1]
    return best


def entitlements(B, M):
    rows = []
    for e in B.ent:
        if not (W.REPORT_FROM <= e["ex"] <= W.VAL_DATE):
            continue
        typ = "Property income distribution" if e["type"] == "PID" else "Dividend"
        for lot_id, od, q in e["lots"]:
            rows.append((e["sub"], e["code"], e["ref"], typ, e["ex"].isoformat(), e["pay"].isoformat(), lot_id,
                         od.isoformat(), e["amount"]))
    for e in fund_events(B, M):
        if not (W.REPORT_FROM <= e["ex"] <= W.VAL_DATE):
            continue
        rows.append((e["sub"], e["code"], e["ref"], e["type"], e["ex"].isoformat(), e["pay"].isoformat(), "", "",
                     e["amount"]))
    df = pd.DataFrame(rows, columns=["sub_account", "security_code", "event_ref", "event_type", "ex_date", "pay_date",
                                     "lot_id", "lot_open_date", "entitlement_gbp"])
    df = df.sort_values(["ex_date", "sub_account", "security_code", "event_ref", "lot_id"], kind="stable")
    return df.reset_index(drop=True)


def isin_check(body):
    digits = "".join(str(int(ch, 36)) for ch in body)
    total = 0
    for i, ch in enumerate(reversed(digits)):
        v = int(ch)
        if i % 2 == 0:
            v *= 2
            v = v // 10 + v % 10
        total += v
    return str((10 - total % 10) % 10)


def sedol_check(s6):
    w = [1, 3, 1, 7, 3, 9]
    t = sum(int(ch, 36) * wt for ch, wt in zip(s6, w))
    return str((10 - t % 10) % 10)


def static(B):
    nm = names(B)
    rows = []
    rng = np.random.default_rng(W.SEED + 77)
    sedols = {}
    for c in sorted(B.info):
        while True:
            s6 = "B" + "".join(rng.choice(list("0123456789BCDFGHJKLMNPQRSTVWXYZ"), 5))
            if s6 not in sedols.values():
                break
        sedols[c] = s6
        sed = s6 + sedol_check(s6)
        isin = "GB00" + sed
        isin += isin_check(isin)
        rows.append((c, isin, sed, nm[c], ASSET["stock"], "London Stock Exchange", "GBP"))
    r6 = "BRGT01"
    rows.append((BK.RIGHTS_CODE, "GB00" + r6 + sedol_check(r6) + isin_check("GB00" + r6 + sedol_check(r6)),
                 r6 + sedol_check(r6), nm[BK.RIGHTS_CODE], ASSET["rights"], "London Stock Exchange", "GBP"))
    for f, (ci, ca) in sorted(B.fcode.items()):
        for code, isin in ((ci, W.FUNDS[f]["isin_inc"]), (ca, W.FUNDS[f]["isin_acc"])):
            rows.append((code, isin, isin[4:11], nm[code], ASSET["fund"], "Kestwick Investment Management (dealing)", "GBP"))
    rows.append((BK.CASH_CODE, "", "", nm[BK.CASH_CODE], ASSET["cash"], "", "GBP"))
    return pd.DataFrame(rows, columns=["security_code", "isin", "sedol", "security_name", "asset_class", "listing",
                                       "price_currency"])


def fix_isins():
    """the Kestwick ISINs carry valid check digits"""
    for f, v in W.FUNDS.items():
        for k in ("isin_inc", "isin_acc"):
            body = v[k][:11]
            v[k] = body + isin_check(body)


def kestwick_history(B, M):
    out = {}
    days = M["days"]
    for f in W.FUNDS:
        fp = B.fp[f]
        rows = []
        for k, d in enumerate(days):
            if d < W.WIN_START or d > W.VAL_DATE:
                continue
            ex = fp["dist"][k] > 0
            rows.append((d, fp["inc"][k], fp["acc"][k], "XD" if ex else "", fp["dist"][k] if ex else None))
        out[f] = pd.DataFrame(rows, columns=["Date", "Income units (GBP)", "Accumulation units (GBP)", "Ex-dividend",
                                             "Distribution per income unit (GBP)"])
    return out


def calendars():
    rows = []
    d = dt.date(2024, 11, 1)
    while d <= dt.date(2027, 12, 31):
        for mkt, nmk in (("UK", "London"), ("US", "New York"), ("JP", "Tokyo")):
            hol = W.HOL[mkt].get(d.isoformat(), "")
            if d.weekday() >= 5:
                continue
            rows.append((d.isoformat(), nmk, "N" if hol else "Y", hol))
        d += dt.timedelta(days=1)
    return pd.DataFrame(rows, columns=["date", "market", "is_business_day", "holiday_name"])


INDEX_NAMES = {"UK": ("FTSE All-Share", 4371.62), "US": ("S&P 500", 6032.38), "EU": ("FTSE World Europe ex UK", 482.15),
               "JP": ("TOPIX", 2716.04), "GILT": ("FTSE Actuaries UK Conventional Gilts All Stocks", 2089.47),
               "CORP": ("iBoxx GBP Non-Gilts", 337.82)}


def index_levels(M):
    rows = []
    for k, (nm, lvl0) in INDEX_NAMES.items():
        days, v = M["index"][k]
        sel = [(d, x) for d, x in zip(days, v) if W.WIN_START <= d <= W.VAL_DATE]
        base = sel[0][1]
        for d, x in sel:
            rows.append((d.isoformat(), nm, round(lvl0 * np.exp(x - base), 2)))
    df = pd.DataFrame(rows, columns=["date", "index_name", "close"])
    return df.sort_values(["date", "index_name"], kind="stable").reset_index(drop=True)
