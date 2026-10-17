"""The golden path from the shipped files alone: the main call (each line followed at the chain that prices it) and the
three asks, plus the wrong paths the checks and the design note quote. Every figure here is computed from target/."""
from __future__ import annotations

import datetime as dt
import os

import numpy as np
import pandas as pd

import analysis as A
import common as K

UPGRADE_WEEK = K.WEEKS[K.UPGRADE_T]          # the retail week holding the PC code's in-use date (2 August 2026)


def read_pack(target):
    f = lambda k: os.path.join(target, K.FILES[k])
    log = pd.read_csv(f("log"), dtype=str)
    reg = pd.read_csv(f("register"), dtype=str)
    items = pd.read_csv(f("items"), dtype=str)
    mv = pd.read_csv(f("movement"), dtype={"load_id": str, "store_id": str, "item_code": str, "promo_code": str})
    ss = pd.read_csv(f("totals"), dtype={"load_id": str, "store_id": str, "dept_code": str})
    partners = pd.read_excel(f("partners"), sheet_name="Chains", dtype=str)
    return dict(log=log, reg=reg, items=items, mv=mv, ss=ss, partners=partners)


def week_index(d):
    return (pd.to_datetime(d) - pd.Timestamp(K.WEEK1)).dt.days // 7


def movement(P, keep="accepted"):
    """The movement rows the index uses: accepted loads, codes as GTIN-14, with category, chain, format and week."""
    mv = P["mv"]
    st = P["log"].set_index("load_id")["status"]
    if keep == "accepted":
        mv = mv[mv["load_id"].map(st) == "accepted"]
    mv = mv.assign(item=mv["item_code"].str.zfill(14))
    mv = mv.merge(P["items"][["item_code", "category"]].rename(columns={"item_code": "item", "category": "cat"}),
                  on="item", how="left")
    mv = mv.merge(P["reg"][["store_id", "chain_code", "format", "store_name", "suburb", "postcode"]],
                  on="store_id", how="left")
    mv = mv.rename(columns={"store_id": "store", "chain_code": "chain", "format": "fmt", "sales_aud": "dollars"})
    mv["t"] = week_index(mv["week_ending"])
    mv["site"] = mv["chain"] + "|" + mv["store_name"] + "|" + mv["suburb"] + "|" + mv["postcode"]
    return mv


def main_call(df, grain="chain"):
    ch = A.changes(df, grain)
    v = A.verdicts(ch)
    return ch, v


# ---------------------------------------------------------------------------------------------- ask A: takings
def takings(P, repeated="detect", sunday="realign", loads="accepted", panel=True):
    ss = P["ss"].merge(P["reg"][["store_id", "chain_code", "format", "first_week_ending", "last_week_ending"]],
                       on="store_id", how="left")
    st = P["log"].set_index("load_id")["status"]
    if loads == "accepted":
        ss = ss[ss["load_id"].map(st) == "accepted"]
    elif loads == "latest":
        lt = P["log"].set_index("load_id")["received_utc"]
        ss = ss.assign(rec=ss["load_id"].map(lt)).sort_values("rec")
        ss = ss.drop_duplicates(["store_id", "week_ending", "dept_code"], keep="last")
    d = pd.to_datetime(ss["week_ending"])
    if sunday == "realign":
        d = d - pd.to_timedelta((d.dt.dayofweek == 6).astype(int), unit="D")
    ss = ss.assign(we=d)
    ss = ss[(ss["we"] >= pd.Timestamp(K.WEEK1)) & (ss["we"] <= pd.Timestamp(K.LAST))]
    if panel:
        first = pd.to_datetime(ss["first_week_ending"])
        last = pd.to_datetime(ss["last_week_ending"]).fillna(pd.Timestamp(K.LAST))
        ss = ss[(ss["we"] >= first) & (ss["we"] <= last)]
    g = ss.groupby(["chain_code", "store_id", "we"])["sales_aud"]
    if repeated == "detect":
        same = g.transform(lambda x: x.nunique() == 1 and len(x) > 1)
        rep = ss.assign(same=same).groupby("chain_code")["same"].all()
        rep_chains = set(rep[rep].index)
        one = ss[ss["chain_code"].isin(rep_chains)].groupby(["format", "store_id", "we"])["sales_aud"].first()
        rest = ss[~ss["chain_code"].isin(rep_chains)].groupby(["format", "store_id", "we"])["sales_aud"].sum()
        tot = pd.concat([one, rest]).groupby(level=0).sum()
    else:
        tot = ss.groupby("format")["sales_aud"].sum()
        rep_chains = set()
    return {f: float(tot.get(f, 0.0)) / 1e6 for f in K.FORMATS}, rep_chains


# ---------------------------------------------------------------------------------------------- ask B: continuity
def chain_weeks(P):
    """Each chain's weeks in the panel within the window: from its data agreement (or the window's first week)."""
    out = {}
    for r in P["partners"].itertuples(index=False):
        a = pd.Timestamp(r.data_agreement_from)
        first = max(0, int(np.ceil((a - pd.Timestamp(K.WEEK1)).days / 7)))
        out[r.chain_code] = set(range(first, K.W))
    return out


def continuous(df, P, by="site"):
    """For each chain, how many of its stores (sites, or store codes) have data in every week it was in the panel."""
    cw = chain_weeks(P)
    weeks = df.groupby(["chain", by])["t"].agg(lambda x: set(x))
    out = {}
    for c in K.CHAIN_CODES:
        need = cw[c]
        out[c] = int(sum(1 for (cc, _), w in weeks.items() if cc == c and need <= w))
    return out


# ---------------------------------------------------------------------------------------------- ask C: promotions
CATALOGUE = {"S1": {"SPECIAL"}, "S2": {"PROMO"}, "S3": {"TPR"}, "S4": {"SALE"}, "S5": {"OFFER"}, "N1": {"P"},
             "N2": {"PROMO"}, "N3": {"SPC"}, "C1": {"PR"}, "C2": {"TPR"}, "C3": {"DEAL"}, "O1": {"SALE"},
             "O2": {"PROMO"}, "O3": {"SPECIAL"}}


def promo_share(df, pc="split"):
    """Per category, spending at catalogue specials over all spending in the window, per cent. pc: split (the upgrade
    chain's PC is its catalogue special before the upgrade week and a price check after), check (PC never a special,
    the current code list read back), every (every coded row counted)."""
    code = df["promo_code"].fillna("")
    if pc == "every":
        on = code != ""
    else:
        on = pd.Series([c in CATALOGUE.get(ch, ()) for ch, c in zip(df["chain"], code)], index=df.index)
        if pc == "split":
            pre = pd.to_datetime(df["week_ending"]) < pd.Timestamp(UPGRADE_WEEK)
            on = on | ((df["chain"] == K.UPGRADE_CHAIN) & (code == "PC") & pre)
    s = df.assign(on=on, d=df["dollars"] * on)
    g = s.groupby("cat")[["d", "dollars"]].sum()
    return {c: float(100 * g.loc[c, "d"] / g.loc[c, "dollars"]) for c in K.CATS}


# ---------------------------------------------------------------------------------------------- everything
def slow_sale_rate(df, P):
    """Share of convenience store-weeks with a sale of each slow line the store ranges, over the window: the slow
    lines are the category's lines outside its three biggest sellers by units."""
    conv = df[df["fmt"] == "convenience"]
    units = df.groupby(["cat", "item"])["units"].sum().reset_index().sort_values(["cat", "units"], ascending=[True, False])
    fast = set(units.groupby("cat").head(3)["item"])
    slow = conv[~conv["item"].isin(fast)]
    weeks = conv.groupby("store")["t"].nunique()
    sold = slow.groupby(["store", "item"])["t"].nunique().reset_index()
    sold["weeks"] = sold["store"].map(weeks)
    return float(sold["t"].sum() / sold["weeks"].sum())


def line_rises(df, cats):
    """For the given categories: the average change, last four weeks against the first four, of the chain-level price
    of the three biggest sellers and of the other lines, per cent."""
    units = df.groupby(["cat", "item"])["units"].sum().reset_index().sort_values(["cat", "units"], ascending=[True, False])
    fast = set(units.groupby("cat").head(3)["item"])
    d = df[df["cat"].isin(cats)]
    g = d.groupby(["item", "chain", "t"])[["dollars", "units"]].sum()
    p = (g["dollars"] / g["units"]).rename("p").reset_index()
    a = p[p["t"] < 4].groupby(["item", "chain"])["p"].mean()
    b = p[p["t"] >= K.W - 4].groupby(["item", "chain"])["p"].mean()
    r = (b / a - 1).rename("rise").dropna().reset_index()
    r["fast"] = r["item"].isin(fast)
    return {"big": float(100 * r.loc[r["fast"], "rise"].mean()), "other": float(100 * r.loc[~r["fast"], "rise"].mean())}


def compute(target, rungs=True):
    P = read_pack(target)
    df = movement(P)
    ch, v = main_call(df, "chain")
    tk, rep = takings(P)
    cont = continuous(df, P, "site")
    ps = promo_share(df, "split")
    out = dict(P=P, df=df, changes=ch, verdicts=v, published=A.published(v), takings=tk, repeated=sorted(rep),
               continuous=cont, promo=ps)
    if rungs:
        out["rungs"] = {}
        for name, d, grain in (("pooled", df, "pooled"), ("pooled_without_july_chain", df[df["chain"] != "S5"],
                                                           "pooled"), ("store", df, "store")):
            c2, v2 = main_call(d, grain)
            out["rungs"][name] = dict(changes=c2, verdicts=v2, published=A.published(v2))
        out["slow_sale_rate"] = slow_sale_rate(df, P)
        out["four"] = [c for c in K.CATS if c in out["published"] and c not in out["rungs"]["store"]["published"]]
        out["line_rises"] = line_rises(df, out["four"])
    return out
