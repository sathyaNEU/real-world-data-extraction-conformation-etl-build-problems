"""The clean truth behind the two asks: the return-to-work spells of fiscal 2026's DART cases (Ask A) and the WMS items
the programme DCs picked in fiscal 2026 weeks 1 to 44 with their case weights (Ask B). Nothing here is read by the
main call."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

import common as K

EXTRACT = dt.date(2026, 10, 31)          # the asks' cut: days and picks to Saturday 31 October 2026
FY26_START = K.FY_START[2026]


# ---------------------------------------------------------------------------------------------------- Ask A
def sister_dc(dcs, dn, r):
    st = dcs.set_index("dc_no").state[dn]
    same = [int(d) for d, s in zip(dcs.dc_no, dcs.state) if s == st and int(d) != dn]
    pool = same if same else [int(d) for d in dcs.dc_no if int(d) != dn]
    return pool[int(r.integers(0, len(pool)))]


def rtw_cases(W):
    """One row per fiscal 2026 case with a return-to-work file (every DART case, and the removed cases whose associate
    was off work before the determination), with its spells as the world knows them."""
    r = K.rng("rtw")
    C = W.cases
    sel = C[(C.date >= FY26_START) & (C.date <= EXTRACT) & (
        ((C.kind == "REC") & C.case_type.isin(["DAFW", "DJTR"])) | (C.kind == "REMOVED"))].copy()
    sel = sel.sort_values(["date", "dc_no", "employee_id"], kind="mergesort")
    rows = []
    for c in sel.itertuples():
        start = c.date + dt.timedelta(days=1)
        if c.kind == "REMOVED":
            if r.random() > 0.55:
                continue
            away, restr = 0, int(r.integers(3, 25))
            sep = -1
        else:
            away, restr, sep = int(c.away_true), int(c.restr_true), int(c.separated_after)
        spells = []
        d0 = start
        if away > 0:
            spells.append(("AWAY", d0, d0 + dt.timedelta(days=away - 1)))
            d0 = d0 + dt.timedelta(days=away)
        if restr > 0:
            kind = "TRANSFER" if r.random() < 0.18 else "RESTRICTED"
            spells.append((kind, d0, d0 + dt.timedelta(days=restr - 1)))
            d0 = d0 + dt.timedelta(days=restr)
        end_full = d0                                   # first day back at full duty
        moved_to, moved_on = None, None
        u_move = r.random()
        k = int(r.integers(2, max(restr - 2, 3)))
        to = sister_dc(W.dcs, int(c.dc_no), r)
        if restr >= 7 and c.kind == "REC" and u_move < 0.30:
            # transitional duty: the home DC has no modified work, so the associate works the restriction at a sister DC
            moved_on = spells[-1][1] + dt.timedelta(days=k)
            moved_to = to
        sep_on = None
        if sep >= 0 and sep < away + restr:
            sep_on = start + dt.timedelta(days=sep)
        rows.append(dict(dc_no=int(c.dc_no), date=c.date, employee_id=c.employee_id, kind=c.kind, case_type=c.case_type,
                         spells=spells, full_duty=end_full, moved_to=moved_to, moved_on=moved_on, sep_on=sep_on,
                         hour=c.hour, key=(c.date, int(c.dc_no), c.hour, c.minute, c.employee_id), restr=restr,
                         alt=(k, to)))
    # every programme DC places at least one restricted associate on transitional duty during the year: where the draw
    # gave a DC none, its longest restriction that started before the extract is the one placed
    for dn in W.prog:
        mine = [x for x in rows if x["dc_no"] == dn and x["kind"] == "REC"]
        if any(x["moved_on"] and x["moved_on"] <= EXTRACT and (x["sep_on"] is None or x["moved_on"] < x["sep_on"])
               for x in mine):
            continue
        cand = [x for x in mine if x["restr"] >= 7 and x["spells"][-1][0] != "AWAY" and x["sep_on"] is None
                and x["spells"][-1][1] + dt.timedelta(days=x["alt"][0]) <= EXTRACT]
        if cand:
            x = max(cand, key=lambda z: (z["restr"], z["date"]))
            x["moved_on"] = x["spells"][-1][1] + dt.timedelta(days=x["alt"][0])
            x["moved_to"] = x["alt"][1]
    return rows


def osha_days(row, upto=EXTRACT):
    """The days a case has carried to `upto` under EHS-RK-01 9: calendar days from the day after the injury, away and
    restricted or transferred, ending at full duty or separation, 180 days at most in total."""
    away = restr = 0
    for kind, a, b in row["spells"]:
        e = min(b, upto)
        if row["sep_on"] is not None:
            e = min(e, row["sep_on"] - dt.timedelta(days=1))
        if e < a:
            continue
        n = (e - a).days + 1
        if kind == "AWAY":
            away += n
        else:
            restr += n
    if away + restr > 180:
        if away >= 180:
            away, restr = 180, 0
        else:
            restr = 180 - away
    return away, restr


# ---------------------------------------------------------------------------------------------------- Ask B
SUBCATS = {
    "AMB": [("CEREAL", 9, 0.25, 12), ("PASTA", 18, 0.3, 8), ("CANNED VEG", 25, 0.2, 10), ("CANNED SOUP", 23, 0.2, 7),
            ("SNACKS", 7, 0.3, 10), ("BAKING", 22, 0.45, 6), ("FLOUR", 26, 0.55, 3), ("SUGAR", 30, 0.55, 3),
            ("RICE", 28, 0.5, 4), ("CONDIMENT", 19, 0.25, 9), ("COFFEE", 14, 0.3, 6), ("HBA", 11, 0.35, 12),
            ("PAPER", 13, 0.3, 5), ("JUICE SS", 27, 0.2, 5)],
    "CHL": [("MILK", 36, 0.12, 6), ("YOGURT", 16, 0.2, 10), ("CHEESE", 15, 0.35, 12), ("DELI", 13, 0.35, 10),
            ("PRODUCE", 28, 0.35, 14), ("EGGS", 47, 0.08, 3), ("MEAT FRESH", 34, 0.3, 8)],
    "FRZ": [("FRZ VEG", 22, 0.2, 10), ("FRZ MEALS", 15, 0.25, 12), ("ICE CREAM", 18, 0.2, 8), ("FRZ MEAT", 33, 0.35, 8),
            ("FRZ POTATO", 31, 0.25, 5), ("ICE", 41, 0.18, 2)],
    "HVB": [("WATER", 37, 0.15, 10), ("SODA", 29, 0.18, 12), ("SPORTS DRINK", 31, 0.12, 6), ("DOG FOOD", 41, 0.3, 9),
            ("CAT LITTER", 39, 0.25, 6), ("CHARCOAL", 25, 0.45, 3), ("SALT", 47, 0.12, 3), ("BULK PAPER", 22, 0.25, 6),
            ("LAUNDRY", 33, 0.25, 6), ("BEER", 34, 0.12, 6)],
}
BRANDS = ["OL", "HFM", "NGP", "PRM", "VAL", "BRD", "STR", "CDL", "AMS", "WST", "TLV", "KSL", "RST", "CYL", "FHV",
          "MHL", "LYL", "PNK", "HRG", "CDW"]


def _desc(sub, w, r):
    br = BRANDS[int(r.integers(0, len(BRANDS)))]
    if sub in ("FLOUR", "SUGAR", "RICE", "DOG FOOD", "CAT LITTER", "SALT", "CHARCOAL") and r.random() < 0.6:
        packs = [50, 40, 25, 20, 10, 5]
        lb = min(packs, key=lambda x: abs(x - w))
        if r.random() < 0.5:
            return "%s %s %dLB" % (br, sub, lb)
        n = max(1, int(round(w / lb)))
        return "%s %s %d/%dLB" % (br, sub, n, lb)
    pk = [6, 8, 12, 12, 24, 24, 4, 36][int(r.integers(0, 8))]
    sz = ["16OZ", "12OZ", "32OZ", "1GAL", "28OZ", "15OZ", "64OZ", "8CT", "20OZ", "16.9OZ"][int(r.integers(0, 10))]
    return "%s %s %d/%s" % (br, sub, pk, sz)


def items():
    """The network's items (current and replaced), each with its true case weight in pounds, cube, set-up source."""
    r = K.rng("items")
    rows = []
    sku_pool = r.choice(np.arange(100000, 999999), 30000, replace=False)
    k = 0
    for cat, subs in SUBCATS.items():
        for sub, mean_w, sd, share in subs:
            n = max(int(share * {"AMB": 70, "CHL": 45, "FRZ": 40, "HVB": 30}[cat]), 12)
            for _ in range(n):
                w = float(np.exp(r.normal(np.log(mean_w), sd)))
                if sub in ("FLOUR", "SUGAR", "RICE", "SALT", "DOG FOOD", "CAT LITTER") and r.random() < 0.18:
                    w = 50.0      # a 50 lb bag: exactly on the line
                w = round(min(max(w, 2.5), 92.0), 1)
                dens = float(np.exp(r.normal(np.log(17 if cat != "HVB" else 21), 0.22)))   # lb per cubic foot
                cube = round(w / dens, 2)
                src = r.choice(["CUBISCAN", "BUYER", "PORTAL"], p=[0.55, 0.33, 0.12])
                if src == "PORTAL" and abs(w - 50.0) < 0.5:
                    src = "BUYER"
                setup = dt.date(2008, 1, 1) + dt.timedelta(days=int(r.integers(0, 6200)))
                if src == "PORTAL":
                    setup = dt.date(2025, 3, 3) + dt.timedelta(days=int(r.integers(0, 560)))
                rows.append(dict(sku=int(sku_pool[k]), category=cat, sub=sub, desc=_desc(sub, w, r), weight_lb=w, cube=cube,
                                 source=str(src), setup=setup, pop=float(np.exp(r.normal(0, 1.1)))))
                k += 1
    I = pd.DataFrame(rows)
    I["version"] = 1
    I["eff_from"] = I.setup
    I["eff_to"] = pd.Series([None] * len(I), dtype=object)
    # reissued numbers: a discontinued item's number given to a new item during fiscal 2026
    reiss = I.sample(frac=0.022, random_state=int(r.integers(0, 2**31))).index
    news = []
    for ix in reiss:
        old = I.loc[ix]
        p_change = int(r.integers(3, 10))          # the new item from this period
        d_change = K.week_start(2026, K.period_weeks(2026, p_change)[0])
        I.loc[ix, "eff_to"] = d_change - dt.timedelta(days=1)
        cat = old.category
        subs = SUBCATS[cat]
        sub, mean_w, sd, _ = subs[int(r.integers(0, len(subs)))]
        w = round(float(np.exp(r.normal(np.log(mean_w), sd))), 1)
        dens = float(np.exp(r.normal(np.log(17 if cat != "HVB" else 21), 0.22)))
        src2 = str(r.choice(["CUBISCAN", "BUYER", "PORTAL"], p=[0.5, 0.3, 0.2]))
        if src2 == "PORTAL" and abs(w - 50.0) < 0.5:
            src2 = "BUYER"
        news.append(dict(sku=int(old.sku), category=cat, sub=sub, desc=_desc(sub, w, r), weight_lb=w, cube=round(w / dens, 2),
                         source=src2, setup=d_change,
                         pop=float(np.exp(r.normal(0, 1.1))), version=2, eff_from=d_change, eff_to=None,
                         reissue_period=p_change))
    I["reissue_period"] = 0
    I.loc[reiss, "reissue_period"] = [n_["reissue_period"] for n_ in news]
    I = pd.concat([I, pd.DataFrame(news)], ignore_index=True)
    # discontinued during fiscal 2026: kept in the master as DISCONTINUED, their last day in the history
    purge = I[(I.version == 1) & (I.reissue_period == 0)].sample(frac=0.012, random_state=int(r.integers(0, 2**31))).index
    I["purged_period"] = 0
    I.loc[purge, "purged_period"] = r.integers(2, 9, len(purge))
    return I


def sku_picks(W, I):
    """Cases picked by programme DC, SKU and fiscal 2026 period (period 11 is week 44 only), allocated from the WMS
    weekly cases by category so every DC-period-category total ties to the weekly file."""
    r = K.rng("picks")
    h = W.hist
    out = []
    for dn in W.prog:
        rr = K.rng("picks", dn)
        hd = h[(h.dc_no == dn) & (h.fy == 2026)]
        carry = {}
        for cat in K.CATS:
            pool = I[(I.category == cat)]
            m = rr.random(len(pool)) < 0.36
            carry[cat] = pool[m]
        for p in range(1, 12):
            wks = [w for w in K.period_weeks(2026, p) if w <= K.LAST_WEEK]
            hp = hd[hd.wk.isin(wks)]
            p_end = K.week_start(2026, wks[-1]) + dt.timedelta(days=6)
            for cat in K.CATS:
                tot = int(round(hp["c_" + cat].round().sum()))
                cp = carry[cat]
                live = []
                for it in cp.itertuples():
                    if it.setup > p_end:
                        continue                     # not set up yet
                    if it.version == 1 and it.reissue_period and p >= it.reissue_period:
                        continue
                    if it.version == 2 and p < it.reissue_period:
                        continue
                    if it.purged_period and p >= it.purged_period:
                        continue
                    live.append(it)
                wts = np.array([it.pop for it in live]) * np.exp(rr.normal(0, 0.25, len(live)))
                alloc = rr.multinomial(tot, wts / wts.sum())
                for it, n in zip(live, alloc):
                    if n:
                        out.append(dict(dc_no=dn, per=p, sku=int(it.sku), version=int(it.version), cases=int(n),
                                        weight_lb=it.weight_lb))
    return pd.DataFrame(out)
