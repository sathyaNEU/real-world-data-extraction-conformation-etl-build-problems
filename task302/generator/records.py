"""Ridgeway's own records of the two years to 30 June 2026: the stores, the lines, every code the tills have used for
a line, each store's daily sales of each line and the stock system's opening positions.

The tills moved from the chain's article numbers to the suppliers' GTINs on 3 March 2025, and two lines changed GTIN
when their suppliers changed the pack; the stock system keeps the article number throughout. A shopper's return is
put back on the shelf and booked at the till as negative units on the day it comes back. Two stores closed for a week
each for a refit and sold nothing those days.
"""
import numpy as np
import pandas as pd

import params as P
import stock

STORE_NO = list(range(201, 201 + P.NS))
SOUTH = {"Nelson Tasman", "Marlborough"}
CATEGORY = {"W": "Bottled water", "F": "Infant formula", "P": "Dry pet food", "G": "Gluten-free bakery"}
SUPPLIER = {
    "W": ["Kaimai Spring Ltd", "Kaimai Spring Ltd", "Kaimai Spring Ltd", "Te Puna Bottling", "Te Puna Bottling",
          "Southern Alps Beverages", "Southern Alps Beverages", "Ruahine Artesian", "Ruahine Artesian",
          "Te Puna Bottling"],
    "F": ["Arataki Nutrition"] * 8,
    "P": ["Huntaway Petfoods"] * 4 + ["Manawatu Pet Nutrition", "Blue Ridge Pet Co", "Feline Choice NZ",
                                      "Feline Choice NZ", "Feline Choice NZ", "Manawatu Pet Nutrition",
                                      "Blue Ridge Pet Co", "Feline Choice NZ"],
    "G": ["Bakehouse Gluten Free"] * 6 + ["Rangi Baking"] * 3,
}
# lines whose supplier changed the pack, so the tills took a new GTIN: (category, line index, from, new description)
REPACK = [("P", 0, pd.Timestamp("2025-11-10"), "Huntaway Adult Dog Beef 2.8kg"),
          ("W", 0, pd.Timestamp("2026-02-23"), "Kaimai Spring Still Water 1.5L")]
RETURN_RATE = 0.0012       # units a shopper brings back, per unit sold


def gtin(rng):
    body = "94" + "".join(str(int(x)) for x in rng.integers(0, 10, 10))
    s = sum(int(c) * (1 if i % 2 == 0 else 3) for i, c in enumerate(body))
    return body + str((10 - s % 10) % 10)


def price_2025(p):
    """Last year's shelf price: this year's less four per cent, to the cent ending in 9."""
    return round(np.floor(p * P.PRICE_FY2025 * 10) / 10 + 0.09, 2)


def stores():
    rows = []
    for no, (town, region) in zip(STORE_NO, P.TOWNS):
        rows.append((no, "Ridgeway " + town, town, region, "South" if region in SOUTH else "North", "07:00", "21:00"))
    return pd.DataFrame(rows, columns=["store_no", "store_name", "town", "region", "island", "opens", "closes"])


def lines(rng):
    rows, codes = [], []
    used = set()
    for c in ("W", "F", "P", "G"):
        for i, (desc, share, group, price) in enumerate(P.LINES[c]):
            while True:
                art = int(rng.integers(100000, 999999))
                if art not in used:
                    used.add(art)
                    break
            g1 = gtin(rng)
            rep = [r for r in REPACK if r[0] == c and r[1] == i]
            cur_desc, cur_gtin = desc, g1
            codes.append((str(art), "Article", art, "2019-07-01", "2025-03-02"))
            if rep:
                g2 = gtin(rng)
                _, _, when, new_desc = rep[0]
                codes.append((g1, "GTIN", art, "2025-03-03", (when - pd.Timedelta(days=1)).date().isoformat()))
                codes.append((g2, "GTIN", art, when.date().isoformat(), ""))
                cur_desc, cur_gtin = new_desc, g2
            else:
                codes.append((g1, "GTIN", art, "2025-03-03", ""))
            rows.append((art, cur_gtin, cur_desc, CATEGORY[c], SUPPLIER[c][i], stock.CASE[c][i],
                         price_2025(price), price, "Supplier direct" if c == "F" else "Distribution centre"))
    ln = pd.DataFrame(rows, columns=["article", "gtin", "description", "category", "supplier", "case_size",
                                     "shelf_price_fy2025", "shelf_price_fy2026", "supply"])
    ch = pd.DataFrame(codes, columns=["item_code", "code_type", "article", "valid_from", "valid_to"])
    return ln, ch


def with_returns(res, closed, rng):
    """Net units at the till: a shopper's return comes back one to six days after the sale, on a day the line is on
    the shelf and the store open, and goes back on the shelf."""
    out = {}
    for c, T in res.items():
        U = T["units"].astype(np.int64)
        O = T["oos"]
        back = np.zeros_like(U)
        k = rng.binomial(U, RETURN_RATE)
        for s, i, d in zip(*np.nonzero(k)):
            dd = d + int(rng.integers(1, 7))
            while dd < P.ND and (O[s, i, dd] or closed[s, dd]):
                dd += 1
            if dd < P.ND:
                back[s, i, dd] += k[s, i, d]
        T2 = dict(T)
        T2["units"] = U - back
        T2["returns"] = back
        out[c] = T2
    return out


def till_code(ln, ch):
    """The code the tills used for each article on each day."""
    codes = {}
    for a in ln.article:
        rows = ch[ch.article == a]
        arr = np.empty(P.ND, dtype=object)
        for r in rows.itertuples():
            lo = (pd.Timestamp(r.valid_from) - P.D0).days
            hi = (pd.Timestamp(r.valid_to) - P.D0).days if r.valid_to else P.ND - 1
            arr[max(lo, 0):min(hi, P.ND - 1) + 1] = r.item_code
        codes[a] = arr
    return codes


def pos(res, ln, ch):
    """One row per store, trading day and till code with units sold, net of returns, and the till value at the year's
    shelf price."""
    codes = till_code(ln, ch)
    fy26 = np.asarray(P.DAYS >= P.BASE_LO)
    frames = []
    k = 0
    for c in ("W", "F", "P", "G"):
        U = res[c]["units"]
        for i in range(U.shape[1]):
            r = ln.iloc[k]
            k += 1
            pr = np.where(fy26, r.shelf_price_fy2026, r.shelf_price_fy2025)
            s_idx, d_idx = np.nonzero(U[:, i, :] != 0)
            u = U[s_idx, i, d_idx]
            frames.append(pd.DataFrame({
                "store_no": np.array(STORE_NO)[s_idx],
                "trade_date": P.DAYS[d_idx].date,
                "item_code": codes[r.article][d_idx],
                "units": u.astype(np.int32),
                "net_sales_nzd": np.round(u * pr[d_idx], 2)}))
    df = pd.concat(frames, ignore_index=True)
    return df.sort_values(["trade_date", "store_no", "item_code"], kind="stable").reset_index(drop=True)


def stock_file(pos_, ln):
    """The stock system's opening position, deliveries received before opening and adjustments booked, for every
    store, line and day."""
    frames = []
    k = 0
    for c in ("W", "F", "P", "G"):
        on, dl, adj = pos_[c]["on_hand"], pos_[c]["delivered"], pos_[c]["adjustment"]
        S, L, N = on.shape
        for i in range(L):
            a = int(ln.article.iloc[k])
            k += 1
            frames.append(pd.DataFrame({
                "store_no": np.repeat(STORE_NO, N),
                "date": np.tile(P.DAYS.date, S),
                "article": a,
                "on_hand_open": on[:, i, :].ravel().astype(np.int32),
                "delivered": dl[:, i, :].ravel().astype(np.int32),
                "adjustment": adj[:, i, :].ravel().astype(np.int32)}))
    df = pd.concat(frames, ignore_index=True)
    return df.sort_values(["date", "store_no", "article"], kind="stable").reset_index(drop=True)
