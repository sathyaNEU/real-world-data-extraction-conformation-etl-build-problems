"""Every graded figure from the shipped pack, read the way the golden reads it: the eight hospitals' 2023 to 2025
resections, each patient's condition before surgery with the earlier operation rebuilt from their earlier admissions,
the risk model on the eight hospitals together, each hospital's ratio and the three centres; then the two asks."""
import datetime as dt

import numpy as np
import pandas as pd

import common as K
import models as M

COMORB = {"chf": ("I50",), "ckd": ("N18",), "copd": ("J44",), "liver": ("K70", "K74", "K76"),
          "dm": ("E10", "E11"), "af": ("I48",), "wtloss": ("R63.4", "E43", "E44")}
BACKGROUND = {"htn": ("I10",), "lipid": ("E78.5",), "gerd": ("K21.9",), "obese": ("E66.9",), "smoke": ("Z87.891",),
              "osa": ("G47.33",), "thyroid": ("E03.9",), "depress": ("F32.A",)}
EARLIER = set(K.EARLIER_OPS)


def _res_date(rec):
    for c, d in rec["px"]:
        if c in K.RESECTION:
            return d
    return None


def operations(P):
    """The programme's population: every resection at the eight hospitals on an adult, 2023 to 2025."""
    rows = []
    for rec in P["discharges"]:
        d = _res_date(rec)
        if d is None or not (K.WINDOW[0] <= d <= K.WINDOW[1]) or rec["hosp"] not in K.ELIGIBLE or rec["age"] < 18:
            continue
        rows.append(rec)
    return rows


def history(P):
    """Each person's earlier operations on the pancreas or bile ducts, from every file, at any hospital."""
    h = {}
    for rec in P["discharges"]:
        if not rec["key"]:
            continue
        for c, d in rec["px"]:
            if c in EARLIER:
                h.setdefault(rec["key"], []).append(d or rec["admit"])
    return h


def frame(P):
    ops = operations(P)
    hist = history(P)
    rows = []
    for rec in ops:
        d = _res_date(rec)
        codes = {c for c, _ in rec["px"]}
        poa_y = [c for c, p in rec["dx"] if p == "Y"]
        x = dict(h=rec["hosp"], rec_id=rec["rec_id"], key=rec["key"], op=d, age=rec["age"], male=rec["sex"] == "M",
                 mal=rec["dx"][0][0].startswith("C"), tot=bool(codes & {"0FTG0ZZ", "0FTG4ZZ"}),
                 whip=("0DT90ZZ" in codes) and not (codes & {"0FTG0ZZ", "0FTG4ZZ"}), urg=rec["atype"] in ("1", "2"))
        for k, prefs in COMORB.items():
            x[k] = any(c.startswith(p) for c in poa_y for p in prefs)
        for k, prefs in BACKGROUND.items():
            x[k] = any(c == p or c.startswith(p) for c, _ in rec["dx"] for p in prefs)
        x["pdx"] = rec["dx"][0][0]
        x["redo"] = any(e < rec["admit"] for e in hist.get(rec["key"], []))
        x["comp"] = any(p == "N" for _, p in rec["dx"])
        dd = P["deaths"].get(rec["key"])
        x["dead"] = dd is not None and 0 <= (dd - d).days <= K.FOLLOW
        x["chole"] = False
        x["stent"] = False
        rows.append(x)
    df = pd.DataFrame(rows)
    # the harmless earlier procedures, for the family's wider forms
    ch, st = {}, {}
    for rec in P["discharges"]:
        for c, dd in rec["px"]:
            if c in K.CHOLE:
                ch.setdefault(rec["key"], []).append(dd or rec["admit"])
            if c == "0F798DZ":
                st.setdefault(rec["key"], []).append(dd or rec["admit"])
    adm = {rec["rec_id"]: rec["admit"] for rec in operations(P)}
    df["chole"] = [any(e < adm[r] for e in ch.get(k, [])) for k, r in zip(df.key, df.rec_id)]
    df["stent"] = [w and any(e < adm[r] for e in st.get(k, [])) for k, r, w in zip(df.key, df.rec_id, df.whip)]
    return df


def main_call(P):
    df = frame(P)
    d = M.prep(df)
    g, model = M.ratio(d, M.GOLDEN)
    o = d.groupby("h").dead.sum().reindex(M.H)
    n = d.groupby("h").size().reindex(M.H)
    e = o / g
    centres = sorted(g.sort_values().index[:3], key=lambda h: g[h])
    return dict(df=df, ratio=g, observed=o, operations=n, expected=e, centres=centres, model=model,
                redo_share=d.groupby("h").redo.mean().reindex(M.H))


def ask_a(P):
    """Each eligible hospital's resections discharged January to June 2026, from the revised release. Two records of the
    same person at the same hospital whose stays overlap are one stay sent twice, so one operation."""
    stays = {}
    for rec in P["revised"]:
        if rec["hosp"] not in K.ELIGIBLE or _res_date(rec) is None:
            continue
        if not (K.H1_2026[0] <= rec["discharge"] <= K.H1_2026[1]):
            continue
        stays.setdefault((rec["key"], rec["hosp"]), []).append((rec["admit"], rec["discharge"]))
    cnt = {h: 0 for h in K.ELIGIBLE}
    for (key, h), spans in stays.items():
        spans.sort()
        end = None
        for a, d in spans:
            if end is None or a > end:
                cnt[h] += 1
                end = d
            else:
                end = max(end, d)
    return cnt


def claim_chains(cl):
    """Each claim's chain, followed through original_claim_id to the claim first received, and each chain's current
    version (the one received last); a voided claim's chain and the void drop out."""
    orig = dict(zip(cl.claim_id, cl.original_claim_id))

    def root(c):
        while orig.get(c):
            c = orig[c]
        return c
    cl = cl.copy()
    cl["root"] = cl.claim_id.map(root)
    void_roots = set(cl.root[cl.bill_type == "0118"])
    live = cl[~cl.root.isin(void_roots)]
    return live.sort_values(["received_date", "claim_id"]).groupby("root").tail(1)


def ask_b(P):
    """The average allowed amount per stay of the cooperative's members' resection stays at each eligible hospital,
    discharged 2023 to 2025: each claim at its current version, a stay's claims (its interim claims) added together."""
    cur = claim_chains(P["claims"])
    stays = cur.groupby(["hosp", "member_id", "admit_date"]).agg(allowed=("allowed", "sum"),
                                                                 through=("statement_through", "max")).reset_index()
    stays = stays[stays.through.str[:4].isin(["2023", "2024", "2025"])]
    out = {}
    for h in K.ELIGIBLE:
        s_ = stays[stays.hosp == h]
        out[h] = (int(len(s_)), float(s_.allowed.sum() / len(s_)))
    return out
