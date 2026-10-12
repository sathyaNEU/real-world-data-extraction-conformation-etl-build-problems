"""Tullan's funding claims on Delahunt's 2026 deals, the debit note register and the island returns."""
import datetime as dt
import math
from collections import defaultdict

import numpy as np

import world as W

LATE_WEEK1 = 3          # stores whose week-one file arrived after the first billing run
WRONG_RATE = 41         # Premium stores billed on the Core price in weeks two and three
ISLANDS = ("0412", "0415")


def island_returns(stores, seed):
    """Monthly returns from the two island stores that send no scan data: tea units by item, with the
    units sold on each Big Deals cycle split out."""
    rng = np.random.default_rng(seed * 13 + 5)
    out = []
    months = [dt.date(2026, m, 1) for m in range(1, 10)]
    for s in [x for x in stores if x["no"] in ISLANDS]:
        for item in ("211401", "211402", "300812", "300813", "208117", "209332"):
            for m in months:
                reg = W.price(item, s["pfile"], m)
                lvl = {"211401": 3.5, "211402": 7.0, "300812": 9.0, "300813": 20.0, "208117": 14.0,
                       "209332": 8.0}[item] * s["size"] / 0.35
                units = int(rng.poisson(lvl * 4.33))
                deal_units, ref, dp = 0, "", ""
                for code, start, it, kind, val, label in W.EVENTS:
                    if it != item or start.year != 2026 or start.month != m.month:
                        continue
                    dpv = W.deal_price(reg, kind, val)
                    deal_units = int(rng.poisson(lvl * 3 * (1 + W.lift(W.depth(reg, kind, val)))))
                    units += deal_units - int(round(lvl * 3))
                    ref, dp = code, dpv
                out.append({"store_no": s["no"], "month": m.strftime("%Y-%m"), "item_no": item, "units": units,
                            "deal_ref": ref, "deal_units": deal_units, "regular_price_eur": reg,
                            "deal_price_eur": dp})
    return out


def build_claims(rows, stores, returns, seed):
    """Claim lines, debit notes. rows are the scan feed tuples (week, store, item, units, reg, dp, ref)."""
    rng = np.random.default_rng(seed * 17 + 9)
    pfile = {}
    for s in stores:
        pfile[s["no"]] = s["pfile"]
        if s.get("renumbered_to"):
            pfile[s["renumbered_to"]] = s["pfile"]
    # the new Swords store reuses 0119; from August its price file is its own
    sw = next(s for s in stores if s["no"] == "0119" and s.get("reissued"))
    lines = []
    n = [0]

    def add(dn, cycle, store, week, units, allowance):
        n[0] += 1
        lines.append({"line_id": "FL%06d" % (418200 + n[0]), "debit_note": dn, "cycle": cycle, "store_no": store,
                      "week_commencing": week.isoformat(), "item_no": W.DEL160, "deal_units": units,
                      "allowance_per_unit_eur": round(allowance, 2), "line_amount_eur": round(units * allowance, 2)})

    feed = defaultdict(dict)
    for (w, sid, item, u, reg, dp, ref) in rows:
        if item == W.DEL160:
            feed[(sid, w)] = (u, reg, dp, ref)
    # BD26-04: every store-week on deal, plus Finglas, which traded through its refit without the cycle
    ev = next(e for e in W.EVENTS if e[0] == "BD26-04")
    wk04 = [ev[1] + dt.timedelta(days=7 * k) for k in range(3)]
    for w in wk04:
        for (sid, ww), (u, reg, dp, ref) in sorted(feed.items()):
            if ww != w:
                continue
            if dp is not None:
                add("DN-26-0311", "BD26-04", sid, w, u, reg - dp)
            elif sid == "0256":
                add("DN-26-0311", "BD26-04", sid, w, u, reg - W.deal_price(reg, "pct", 0.20))
    for r in returns:
        if r["deal_ref"] == "BD26-04" and r["item_no"] == W.DEL160:
            add("DN-26-0311", "BD26-04", r["store_no"], wk04[0], r["deal_units"],
                r["regular_price_eur"] - r["deal_price_eur"])
    # BD26-13: first run misses three late week-one files and bills 41 Premium stores in weeks two and
    # three on the Core price; the re-issue bills those store-weeks again on the right price and adds
    # the late files, and the first run's lines for them are never credited
    ev = next(e for e in W.EVENTS if e[0] == "BD26-13")
    wk13 = [ev[1] + dt.timedelta(days=7 * k) for k in range(3)]
    on = sorted({sid for (sid, w), v in feed.items() if w in wk13 and v[2] is not None})
    prem = [s for s in on if pfile.get(s) == "P" and s not in ("0119",)]
    rng.shuffle(prem)
    wrong = sorted(prem[:WRONG_RATE])
    rest = [s for s in on if s not in wrong]
    rng.shuffle(rest)
    late = sorted(rest[:LATE_WEEK1])
    core = W.PRICE[W.DEL160]["C"][1]
    for w in wk13:
        for sid in on:
            u, reg, dp, ref = feed[(sid, w)]
            if w == wk13[0] and sid in late:
                continue
            if w != wk13[0] and sid in wrong:
                add("DN-26-0947", "BD26-13", sid, w, u, core - W.deal_price(core, "pct", 0.25))
            else:
                add("DN-26-0947", "BD26-13", sid, w, u, reg - dp)
    for r in returns:
        if r["deal_ref"] == "BD26-13" and r["item_no"] == W.DEL160:
            add("DN-26-0947", "BD26-13", r["store_no"], wk13[0], r["deal_units"],
                r["regular_price_eur"] - r["deal_price_eur"])
    for w in wk13:
        for sid in on:
            u, reg, dp, ref = feed[(sid, w)]
            if (w == wk13[0] and sid in late) or (w != wk13[0] and sid in wrong):
                add("DN-26-1022", "BD26-13", sid, w, u, reg - dp)
    nets = defaultdict(float)
    for l in lines:
        nets[l["debit_note"]] += l["line_amount_eur"]
    notes = [
        ("DN-26-0311", "BD26-04", dt.date(2026, 4, 8), "Spring Big Deals funding, Delahunt Original 160s Save 20%",
         "Issued", ""),
        ("DN-26-0947", "BD26-13", dt.date(2026, 10, 5), "Big Deals funding, Delahunt Original 160s Save 25%",
         "Issued", "Part re-issued by DN-26-1022"),
        ("DN-26-1022", "BD26-13", dt.date(2026, 10, 7), "Big Deals funding, Delahunt Original 160s Save 25% "
         "(re-issue)", "Issued", "Re-issue of DN-26-0947 lines for 41 stores, weeks 2 and 3; adds 3 week 1 files "
         "received late"),
    ]
    dn = []
    for no, cyc, d, desc, status, note in notes:
        net = round(nets[no], 2)
        vat = round(net * 0.23, 2)
        dn.append({"Debit note": no, "Cycle": cyc, "Issued": d, "Description": desc, "Net (EUR)": net,
                   "VAT 23% (EUR)": vat, "Gross (EUR)": round(net + vat, 2), "Status": status, "Note": note,
                   "Credited (EUR)": 0.0})
    meta = {"wrong": wrong, "late": late, "core_allowance": core - W.deal_price(core, "pct", 0.25)}
    return lines, dn, meta
