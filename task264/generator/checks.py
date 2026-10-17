"""Assertions for task264, run on every build: the three rules (R1 to R3c) on the clean truth and the pack, the ladder
and its variants, every semantic fork row, mess neutrality on the main call, the three asks' devices and hazards
against the cracker's path, the separation line, the input gates and the realism sweep."""
from __future__ import annotations

import json
import os
import re
import zipfile

import numpy as np
import pandas as pd

import analysis as A
import common as K
import golden as G

HERE = os.path.dirname(os.path.abspath(__file__))
GOLD = ["Bread and bakery", "Breakfast cereals", "Cheese", "Yoghurt and desserts", "Eggs", "Deli and cooked meats",
        "Fresh fruit", "Frozen foods", "Biscuits", "Chips and snacks"]
R0 = ["Breakfast cereals", "Cheese", "Deli and cooked meats", "Biscuits"]
R1 = ["Bread and bakery", "Breakfast cereals", "Cheese", "Eggs", "Deli and cooked meats", "Fresh fruit", "Biscuits",
      "Chips and snacks"]
R2 = ["Bread and bakery", "Yoghurt and desserts", "Eggs", "Fresh fruit", "Frozen foods", "Chips and snacks",
      "Coffee and tea"]
RESULTS = []


def ok(label, cond, detail=""):
    RESULTS.append((label, bool(cond), detail))
    print("%s  %-62s %s" % ("PASS" if cond else "FAIL", label, detail))


def pub(ch, w=None):
    return A.published(A.verdicts(ch, w))


def margin(ch, w=None):
    v = A.verdicts(ch, w)
    return min(abs(v[c]["worst"] - K.TOLERANCE) for c in K.CATS)


def r1(x):
    return float("%.1f" % (x + (1e-9 if x >= 0 else -1e-9)))


def run(target, T):
    RESULTS.clear()
    clean = A.movement_frame(T)
    R = G.compute(target)
    P, df = R["P"], R["df"]

    # ------------------------------------------------------------------------------------------ the three rules
    ok("R1a the pack ships store x line x week movement rows", len(P["mv"]) >= 25000 and
       {"units", "sales_aud", "store_id", "item_code", "week_ending"} <= set(P["mv"].columns), "%d rows" % len(P["mv"]))
    cols = " ".join(" ".join(map(str, P[k].columns)) for k in ("mv", "ss", "reg", "items", "log"))
    ok("R1b no shipped column holds a price, an index or a change", not re.search(r"price|index|change|gap", cols,
                                                                                    re.I), cols[:60])
    ch_clean = A.changes(clean, "chain")
    ok("R1c the golden reads the movement rows: pack equals clean truth", pub(ch_clean) == R["published"] == GOLD,
       "%d" % len(R["published"]))
    gap = max(abs(R["changes"][k] - ch_clean[k]) for k in ch_clean)
    ok("R1d pack and clean-truth changes agree to 0.001 points", gap < 1e-3, "%.2e" % gap)
    both = G.movement(P, keep="all")
    ok("R2a mess: the resubmitted block kept beside its originals, same call", pub(A.changes(both, "chain")) == GOLD)
    raw = df[df["item_code"].str.len() == 14]
    ok("R2b mess: the 13-digit codes left unmatched (rows dropped), same call", pub(A.changes(raw, "chain")) == GOLD,
       "%d rows dropped" % (len(df) - len(raw)))
    md = df[~df["promo_code"].fillna("").isin(["RC", "MD", "CLR"])]
    ok("R2c mess: store markdown rows dropped, same call", pub(A.changes(md, "chain")) == GOLD)
    ok("R2d mess: the July chain left out, same call", pub(A.changes(df[df["chain"] != "S5"], "chain")) == GOLD)
    kgc = df.assign(units=np.where(df["units"] % 1 != 0, df["units"] * 1000, df["units"]))
    ok("R2e mess: kilograms read in grams for weighed lines, same call", pub(A.changes(kgc, "chain")) == GOLD)
    ok("R3a analyst test: the easy route on the clean truth files 4 categories", pub(A.changes(clean, "pooled")) == R0)
    ok("R3b the decisive step alone (pooled to chain) files the golden", pub(ch_clean) == GOLD)
    ok("R3b' each lower rung's single correction stays wrong (8 and 7)",
       pub(A.changes(clean[clean["chain"] != "S5"], "pooled")) == R1 and pub(A.changes(clean, "store")) == R2)
    docs_text = pdf_text(target)
    ok("R3c no plant: no document states a category change, sub-index result or list",
       not re.search(r"Breakfast|Biscuits|Cheese|sub-index (for|of) [A-Z]", docs_text), "")

    # ------------------------------------------------------------------------------------------ the ladder
    rg = R["rungs"]
    ok("ladder R0 (pooled over the format's stores) = 4 named", rg["pooled"]["published"] == R0)
    ok("ladder R1 (pooled, the July chain left out) = 8 named", rg["pooled_without_july_chain"]["published"] == R1)
    ok("ladder R1' (balanced panel of store codes) = the same 8", pub(A.changes(df, "balanced")) == R1)
    ok("ladder R2 (line matched store by store) = 7 named", rg["store"]["published"] == R2)
    ok("ladder R2' (store codes linked into sites) = the same 7", pub(A.changes(df, "site")) == R2)
    ok("ladder R3 (line at the chain that prices it) = the golden 10", R["published"] == GOLD)
    sets = [tuple(R0), tuple(R1), tuple(R2), tuple(GOLD)]
    ok("separation: four rungs, four different sets and counts", len(set(sets)) == 4 and
       len({len(s) for s in sets}) == 4)
    m = {k: margin(x["changes"]) for k, x in rg.items()}
    m["golden"] = margin(R["changes"])
    ok("margins: golden at least 0.3 points from 1.5", m["golden"] >= 0.3, "%.2f" % m["golden"])
    ok("margins: every rung at least 0.15 points from 1.5", min(m.values()) >= 0.15,
       ", ".join("%s %.2f" % kv for kv in m.items()))
    ok("worth: the golden keeps the 4 R2 drops and drops R2's one wrong keep",
       set(GOLD) - set(R2) == set(R0) and set(R2) - set(GOLD) == {"Coffee and tea"})

    # ------------------------------------------------------------------------------------------ convergence
    for name, ch in (("each chain's own GEKS combined by spending", A.chain_each(df)),
                     ("store level, an unsold week at the chain's price", A.store_imputed(df))):
        ok("converge: %s" % name, pub(ch) == GOLD, "margin %.2f" % margin(ch))
    lvl = geometric_ends(df)
    ok("converge (SF3): geometric four-week means", pub(lvl) == GOLD)
    tot = df.groupby("fmt")["dollars"].sum()
    pw = {f: 100 * tot[f] / tot.sum() for f in K.FORMATS}
    ok("converge (SF5): the panel's own spending shares as format weights", pub(R["changes"], pw) == GOLD)
    geo = {}
    for c in K.CATS:
        nat = 100 * (np.exp(sum(K.FORMAT_WEIGHTS[f] / 100 * np.log(1 + R["changes"][(c, f)] / 100)
                                for f in K.FORMATS)) - 1)
        geo[c] = max(abs(R["changes"][(c, f)] - nat) for f in K.FORMATS) <= K.TOLERANCE
    ok("converge (SF5): a geometric national combination", [c for c in K.CATS if geo[c]] == GOLD)
    hh = pd.read_excel(os.path.join(target, K.FILES["household"]), sheet_name="Format split")
    hcall = []
    for r_ in hh.itertuples(index=False):
        w = {"supermarket": r_.supermarket_pct, "neighbourhood": r_.neighbourhood_pct,
             "convenience": r_.convenience_pct, "online": r_.online_pct}
        if A.verdicts(R["changes"], w)[r_.category]["publish"]:
            hcall.append(r_.category)
    ok("distractor: the household panel's category format splits as weights give the same call",
       [c for c in K.CATS if c in hcall] == GOLD)

    # ------------------------------------------------------------------------------------------ semantic forks
    v = R["verdicts"]
    ok("SF1 the eighteen categories are the item master's, every movement line joins one",
       sorted(P["items"]["category"].unique()) == sorted(K.CATS) and df["cat"].notna().all())
    wk = pd.to_datetime(P["mv"]["week_ending"])
    ok("SF2 the movement table covers exactly the 52 weeks to 28 November 2026",
       wk.min() == pd.Timestamp(K.WEEK1) and wk.max() == pd.Timestamp(K.LAST) and wk.nunique() == K.W)
    ok("SF3 the methodology files the four-week averages", "average of its index over the year's last four weeks"
       in docs_text.replace("\n", " "))
    ok("SF4 every store code has one chain and one format; every chain one format",
       P["reg"]["store_id"].is_unique and P["reg"].groupby("chain_code")["format"].nunique().max() == 1)
    ok("SF6 no category's largest gap within 0.15 of 1.5, unrounded or rounded",
       m["golden"] >= 0.15 and all((max(abs(r1(g)) for g in v[c]["gaps"].values()) <= K.TOLERANCE) == v[c]["publish"]
                                   for c in K.CATS))
    ok("SF7 every category sells in all four formats", df.groupby("cat")["fmt"].nunique().min() == 4)
    kgl = set(P["items"].loc[P["items"]["unit_of_sale"] == "kg", "item_code"])
    ok("SF8 weighed lines carry kilograms (fractional units), packed lines whole units",
       (df.loc[df["item"].isin(kgl), "units"] % 1 != 0).mean() > 0.9 and
       (df.loc[~df["item"].isin(kgl), "units"] % 1 == 0).all())
    ok("SF9 = R2a (the resubmission kept twice gives the same call)", RESULTS[[r[0] for r in RESULTS].index(
        "R2a mess: the resubmitted block kept beside its originals, same call")][1])
    ok("SF10 = R2d (the July chain in or out gives the same call)", pub(A.changes(df[df["chain"] != "S5"], "chain"))
       == GOLD)
    j = P["mv"]["item_code"].isin(P["items"]["item_code"])
    ok("SF11 raw codes leave one chain's rows unmatched; zero-padded, every row joins",
       (~j).sum() > 0 and P["mv"]["item_code"].str.zfill(14).isin(P["items"]["item_code"]).all(),
       "%d unmatched raw" % (~j).sum())
    ok("SF12 every pair of weeks shares products at the chain level in every cell", every_pair(df))
    ok("SF13 the methodology files the Tornqvist comparison and GEKS", "Tornqvist" in docs_text and "GEKS" in docs_text)
    site = df.groupby("site")[["chain", "fmt"]].nunique()
    ok("SF14 a re-coded store keeps its chain and format under both codes", (site.max() == 1).all() and
       (df.groupby("site")["store"].nunique() > 1).sum() >= 14)

    # ------------------------------------------------------------------------------------------ separation
    swap = df.assign(store=df["site"])
    same = max(abs(A.changes(swap, "chain")[k] - R["changes"][k]) for k in R["changes"])
    ok("separation: the call is identical with store codes replaced by sites", same < 1e-12, "%.1e" % same)
    ok("separation: the call reads no store sales, promotion code or log note",
       pub(A.changes(df.drop(columns=["promo_code", "load_id"]), "chain")) == GOLD)

    # ------------------------------------------------------------------------------------------ ask A: takings
    tk = R["takings"]
    crack = G.takings(P, repeated="sum")[0]
    ok("A golden: the four repeated-total chains detected", R["repeated"] == sorted(K.VENDOR_CHAINS), R["repeated"])
    ok("A cracker (every department row summed) misses all four formats",
       all(r1(crack[f]) != r1(tk[f]) for f in K.FORMATS), str({f[:3]: r1(crack[f] - tk[f]) for f in K.FORMATS}))
    lat = G.takings(P, loads="latest")[0]
    ok("A hazard H1: the latest load (the rejected resend) moves supermarkets", r1(lat["supermarket"]) !=
       r1(tk["supermarket"]), "%.1f" % (lat["supermarket"] - tk["supermarket"]))
    bf = G.takings(P, panel=False)[0]
    ok("A hazard H2: weeks before a store's panel start kept moves supermarkets", r1(bf["supermarket"]) !=
       r1(tk["supermarket"]), "%.1f" % (bf["supermarket"] - tk["supermarket"]))
    sun = G.takings(P, sunday="raw")[0]
    ok("A hazard H3: Sunday week-endings filtered raw moves convenience", r1(sun["convenience"]) !=
       r1(tk["convenience"]), "%.2f" % (sun["convenience"] - tk["convenience"]))
    ok("A golden takings are not round", all(abs(tk[f] - round(tk[f])) > 0.02 for f in K.FORMATS))

    # ------------------------------------------------------------------------------------------ ask B: continuity
    cs, codes = R["continuous"], G.continuous(df, P, "store")
    ok("B cracker (store codes with every week) misses all fourteen chains",
       all(codes[c] != cs[c] for c in K.CHAIN_CODES), str({c: codes[c] - cs[c] for c in K.CHAIN_CODES}))
    over = overlink(df, P)
    ok("B over-linker (gaps ignored once codes are linked) misses the refurbishment chains",
       sum(over[c] != cs[c] for c in K.CHAIN_CODES) >= 5, str({c: over[c] - cs[c] for c in K.CHAIN_CODES}))
    ss_weeks = store_sales_weeks(P)
    mv_weeks = df.groupby("store")["t"].agg(lambda x: set(x))
    ok("B the two feeds agree on which store sent data in which panel week",
       all(ss_weeks.get(s, set()) >= w for s, w in mv_weeks.items()))

    # ------------------------------------------------------------------------------------------ ask C: promotions
    ps = R["promo"]
    chk = G.promo_share(df, "check")
    ok("C cracker (the current code list: PC a price check) misses all eighteen categories",
       all(r1(chk[c]) != r1(ps[c]) for c in K.CATS), "min %.2f" % min(abs(chk[c] - ps[c]) for c in K.CATS))
    ev = G.promo_share(df, "every")
    nev = sum(r1(ev[c]) != r1(ps[c]) for c in K.CATS)
    ok("C hazard: every coded row counted (markdowns, price checks) moves most categories", nev >= 9, "%d moved" % nev)
    b2 = G.promo_share(both, "split")
    ok("C hazard: the resubmitted block counted twice moves some categories", sum(r1(b2[c]) != r1(ps[c])
                                                                                for c in K.CATS) >= 1,
       "%d moved" % sum(r1(b2[c]) != r1(ps[c]) for c in K.CATS))
    pre = df[(df["chain"] == K.UPGRADE_CHAIN) & (pd.to_datetime(df["week_ending"]) < pd.Timestamp(G.UPGRADE_WEEK))]
    ok("C device: no TPR before the upgrade week, PC rows chain-wide at a cut price before it",
       (pre["promo_code"] == "TPR").sum() == 0 and (pre["promo_code"] == "PC").sum() > 1000)

    # ------------------------------------------------------------------------------------------ gates and realism
    files = sorted(os.listdir(target))
    ok("gate: 10 or more files", len(files) >= 10, "%d" % len(files))
    ok("gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    meta = json.load(open(os.path.join(os.path.dirname(HERE), "metadata.json")))
    ok("gate: two distractors in metadata.json, present in target",
       len(meta["distractor_files"]) >= 2 and all(os.path.exists(os.path.join(os.path.dirname(target), p))
                                                  for p in meta["distractor_files"]))
    ok("gate: no file name says distractor", not any("distract" in f for f in files))
    per = df.groupby(["store", "t"]).size()
    ok("realism: rows per store-week vary (no constant counts)", per.nunique() > 50, "%d distinct" % per.nunique())
    cents = (P["ss"]["sales_aud"] * 100 % 100 == 0).mean()
    ok("realism: store sales are not round", cents < 0.02, "%.3f" % cents)
    text = all_text(target)
    ok("realism: no em or en dash anywhere in the pack", "—" not in text and "–" not in text)
    ok("realism: no built-pack wording (H24)", not re.search(r"fictional|fictitious|this exercise|invented|constructed",
                                                            text, re.I))
    ok("realism: the two personas appear, no placeholder names",
       K.PEOPLE["head"] in text and K.PEOPLE["feeds"] in text and not re.search(r"John Doe|Acme|Company A", text))
    last_rec = max(pd.to_datetime(P["log"]["received_utc"]).max().tz_localize(None),
                   pd.to_datetime(P["ss"]["week_ending"]).max(), pd.to_datetime(P["mv"]["week_ending"]).max())
    ok("realism H16: no feed or log date after the pull of 4 December 2026", last_rec <= pd.Timestamp(K.PULL),
       str(last_rec))
    mt = {os.path.getmtime(os.path.join(target, f)) for f in files}
    ok("realism: one export time on every file", len(mt) == 1)
    import names as NM
    ref = NM.reference()
    invented = [K.FIRM] + [K.CH[c]["banner"] for c in K.CHAIN_CODES]
    clash = {n: NM.clashes(n, ref) for n in invented}
    ok("realism H21: the firm and every banner clear Australian places and grocery names by three edits",
       not any(clash.values()), str({k: v[:3] for k, v in clash.items() if v}))
    graded = [x for c in K.CATS for x in [R["verdicts"][c]["national"], R["promo"][c]] +
              list(R["verdicts"][c]["gaps"].values())] + list(R["takings"].values())
    edge = min(abs(abs(x) * 10 % 1 - 0.5) for x in graded)
    near = sum(abs(abs(x) * 10 % 1 - 0.5) < 0.05 for x in graded)
    ok("bins: no graded figure within 0.0001 of a one-decimal rounding edge", edge >= 0.001,
       "closest %.4f of a step; %d of %d within 0.005" % (edge, near, len(graded)))
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    ok("figures.json carries the call and every graded figure", figs["call"]["count"] == len(GOLD) and
       len(figs["categories"]) == 18 and len(figs["takings"]) == 4 and len(figs["continuous"]) == 14)
    bad = [r for r in RESULTS if not r[1]]
    print("%d checks, %d failed" % (len(RESULTS), len(bad)))
    assert not bad, [r[0] for r in bad]


# ---------------------------------------------------------------------------------------------- helpers
def geometric_ends(df):
    out = {}
    for k, (P_, Q) in A.matrices(df, ["chain"]).items():
        ok_ = (Q > 0) & np.isfinite(P_)
        n = P_.shape[1]
        E = np.where(ok_, P_ * Q, 0.0)
        L = np.where(ok_, np.log(np.where(ok_, P_, 1.0)), 0.0)
        lnB = np.zeros((n, n))
        for a in range(n):
            mm = ok_[:, a:a + 1] & ok_
            Ea, Eb = np.where(mm, E[:, a:a + 1], 0.0), np.where(mm, E, 0.0)
            with np.errstate(invalid="ignore", divide="ignore"):
                w = 0.5 * (Ea / Ea.sum(0) + Eb / Eb.sum(0))
            lnB[a] = np.nansum(np.where(mm, w * (L - L[:, a:a + 1]), 0.0), axis=0)
        lvl = (lnB[0][:, None] + lnB).mean(axis=0)
        out[k] = 100 * (np.exp(lvl[-4:].mean() - lvl[:4].mean()) - 1)
    return out


def every_pair(df):
    for k, (P_, Q) in A.matrices(df, ["chain"]).items():
        ok_ = (Q > 0)
        shared = ok_.T.astype(int) @ ok_.astype(int)
        if (shared == 0).any():
            return False
    return True


def overlink(df, P):
    """Every code linked to its site and counted as continuous from its first to its last week, gaps ignored."""
    cw = G.chain_weeks(P)
    out = {}
    for c in K.CHAIN_CODES:
        d = df[df["chain"] == c]
        n = 0
        for _, g in d.groupby("site"):
            if g["t"].min() <= min(cw[c]) and g["t"].max() == K.W - 1:
                n += 1
        out[c] = n
    return out


def store_sales_weeks(P):
    ss = P["ss"]
    st = P["log"].set_index("load_id")["status"]
    ss = ss[ss["load_id"].map(st) == "accepted"]
    d = pd.to_datetime(ss["week_ending"])
    d = d - pd.to_timedelta((d.dt.dayofweek == 6).astype(int), unit="D")
    t = (d - pd.Timestamp(K.WEEK1)).dt.days // 7
    return ss.assign(t=t).groupby("store_id")["t"].agg(lambda x: set(x)).to_dict()


def pdf_text(target):
    import subprocess
    out = []
    for f in sorted(os.listdir(target)):
        if f.endswith(".pdf"):
            out.append(subprocess.run(["pdftotext", "-layout", os.path.join(target, f), "-"], capture_output=True,
                                      text=True).stdout)
    return "\n".join(out)


def all_text(target):
    out = [pdf_text(target)]
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        if f.endswith(".csv"):
            out.append(open(p, encoding="utf-8").read(2_000_000))
        elif f.endswith(".xlsx"):
            with zipfile.ZipFile(p) as z:
                for n in z.namelist():
                    if n.endswith(".xml"):
                        out.append(z.read(n).decode("utf-8", "ignore"))
    return "\n".join(out)
