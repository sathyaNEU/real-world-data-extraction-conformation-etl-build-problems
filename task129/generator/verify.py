"""task129 independent verifier.

    python3 task129/generator/verify.py <target dir> [--record build_record.json]

Reads only the shipped files under <target dir>. Imports nothing from the generator, reads every
date and rule it needs from the shipped documents and logs, recomputes every rung, rival read,
calibration outcome and graded figure, checks the ladder's shape and every figure's rounding bin,
and (with --record) checks agreement with the generator's build record."""
import argparse
import json
import os
import re
import sys

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

CZ = "Europe/Copenhagen"
RESULTS = []


def check(name, cond, info=""):
    RESULTS.append((name, bool(cond), info))
    print(("PASS " if cond else "FAIL ") + name + (f"  {info}" if info != "" else ""))


def to_utc(series):
    return pd.to_datetime(series, utc=True).dt.tz_convert(None)


def pdf_text(path):
    from pypdf import PdfReader
    return " ".join(" ".join(p.extract_text().split()) for p in PdfReader(path).pages)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--record", default=None)
    a = ap.parse_args()
    T = a.target
    f = {n: os.path.join(T, n) for n in os.listdir(T)}
    find = lambda pat: next(p for n, p in f.items() if re.search(pat, n))

    # ---------------------------------------------------------------- the filed rules
    sla = pdf_text(find(r"service_level"))
    pay = pdf_text(find(r"paywall"))
    m = re.search(r"exceeds ([0-9.]+) seconds", sla)
    line_ms = float(m.group(1)) * 1000
    win_days = int(re.search(r"the (\d+) days either side", sla).group(1))
    check("rules.read_from_sla", line_ms == 4000 and win_days == 28, (line_ms, win_days))
    check("rules.adfree_from_paywall", "ad-free layout on every template" in pay)

    reg = pd.read_csv(find(r"device_registry"), dtype=str)
    rel = pd.read_csv(find(r"release_train"), dtype=str, keep_default_na=False)
    ro = pd.read_csv(find(r"rollout"), dtype=str, keep_default_na=False)
    subs = pd.read_csv(find(r"subscription_register"), dtype=str, keep_default_na=False)
    eds = pd.read_csv(find(r"edition_register"), dtype=str, keep_default_na=False)
    chg = pd.read_excel(find(r"change_register"), header=3, dtype=str)
    letters = {"A": "Header-bidding", "B": "Image pipeline", "C": "Bølge front end",
               "D": "Consent banner", "E": "Brand web fonts"}
    cid = {k: chg[chg.Name.str.startswith(v)].Change.iloc[0] for k, v in letters.items()}
    deploys = np.sort(to_utc(rel.deployed_at).values)

    def rel_time(*pats):
        mm = np.ones(len(rel), bool)
        for p_ in pats:
            mm &= rel.notes.str.contains(p_, regex=False).values
        assert mm.sum() == 1, pats
        return to_utc(rel.deployed_at[mm]).iloc[0]
    t_dated = {k: rel_time(cid[k]) for k in "EBD"}
    t_puz = rel_time(cid["A"], "Spil")
    ads = ro[ro.layout == "ad-supported"]
    cohorts = list(ads.template_groups)
    t_coh = {r.template_groups: to_utc(pd.Series([r.switched_on])).iloc[0] for r in ads.itertuples()}
    t_sub = to_utc(ro[ro.layout != "ad-supported"].switched_on).iloc[0]

    # ---------------------------------------------------------------- the beacon frame
    tbl = pq.read_table(find(r"\.parquet$")).to_pandas()
    tbl = tbl.sort_values("beacon_id").drop_duplicates("pv_id")
    phone = reg[reg.form_factor == "phone"].set_index("device_model").perf_band
    x = tbl[tbl.device_model.isin(phone.index)].copy()
    x["pc"] = x.device_model.map(phone)
    x["t"] = x.ts_utc.dt.tz_convert(None)
    lt = x.ts_utc.dt.tz_convert(CZ)
    x["mon"] = lt.dt.month
    x["day"] = lt.dt.tz_localize(None).dt.normalize()
    x["sc"] = x.lcp_ms.notna()
    x["ov"] = x.lcp_ms.fillna(0) > line_ms
    x["w"] = x.sample_weight.astype(float)
    x["ed"] = x.url_path.str.extract(r"^/lokal/([^/]+)/")[0]
    cur = eds[eds.valid_to == ""].set_index("edition_slug").masthead
    x["mast"] = np.where(x.ed.notna(), x.ed.map(cur), x.title)
    # state: the device's first view since the latest deploy (shift-based, not array diff)
    x = x.sort_values(["device_key", "t"], kind="mergesort")
    x["dep"] = np.searchsorted(deploys, x.t.values, side="right")
    prev_dev = x.device_key.shift(1)
    prev_dep = x.dep.shift(1)
    x["first"] = (prev_dev != x.device_key) | (prev_dep != x.dep)
    # subscribers at view time
    s2 = subs.assign(st=pd.to_datetime(subs.start_date),
                     en=pd.to_datetime(subs.end_date.replace("", "2099-12-31")))
    j = x[["account_key", "day"]].reset_index().merge(s2[["account_key", "st", "en"]], on="account_key")
    j = j[(j.day >= j.st) & (j.day <= j.en)]
    x["sub"] = x.index.isin(j["index"].unique())
    tp = x.template
    x["grp"] = np.select([tp.isin(cohorts) & x["sub"], tp.isin(cohorts), (tp == "spil") & ~x["sub"]],
                         ["sub", "base", "puz"], "other")
    xs = x[x.sc]

    def rate(d, keys):
        g = d.assign(o=d.w * d.ov).groupby(keys)[["o", "w"]].sum()
        return g.o / g.w

    W = pd.Timedelta(days=win_days)

    def eff(grp, keys):
        d = xs[xs.grp == grp]
        if grp == "base":
            pre = pd.concat([d[(d.template == c) & (d.t >= t_coh[c] - W) & (d.t < t_coh[c])] for c in cohorts])
            post = pd.concat([d[(d.template == c) & (d.t >= t_coh[c]) & (d.t < t_coh[c] + W)] for c in cohorts])
        else:
            t0 = t_puz if grp == "puz" else t_sub
            pre, post = d[(d.t >= t0 - W) & (d.t < t0)], d[(d.t >= t0) & (d.t < t0 + W)]
        if not keys:
            return (post.w * post.ov).sum() / post.w.sum() - (pre.w * pre.ov).sum() / pre.w.sum()
        return rate(post, keys) - rate(pre, keys)

    aug = xs[xs.mon == 8]

    def value(d, e, keys):
        if not keys:
            return d.w.sum() * e
        vol = d.groupby(keys).w.sum()
        return float((vol * e.reindex(vol.index)).sum())

    B_, S_, Z_ = aug[aug.grp == "base"], aug[aug.grp == "sub"], aug[aug.grp == "puz"]
    out = {}
    for name, keys in (("raw", []), ("phone", ["pc"]), ("state", ["pc", "first"])):
        eA, eC = eff("puz", keys), eff("sub", keys)
        out[name] = {"A": value(B_, eA, keys) + value(Z_, eA, keys),
                     "C": value(B_, eC, keys) + value(S_, eC, keys)}
        if name == "state":
            out["grid"] = {c: {"A": value(B_[B_.template == c], eA, keys),
                               "C": value(B_[B_.template == c], eC, keys) + value(S_[S_.template == c], eC, keys)}
                           for c in cohorts}
            out["eA"], out["eC"] = eA, eC
    A4, C4 = out["state"]["A"], out["state"]["C"]
    A3, C3 = out["phone"]["A"], out["phone"]["C"]

    # ---------------------------------------------------------------- dated changes by title
    hero = set(cohorts) | {"arkiv"}
    titles = {"ST": "Sønderå Tidende", "LA": "Lindå Avis", "KD": "Kærby Dagblad"}
    Tv = {}
    for k in "DBE":
        d = xs if k != "B" else xs[xs.template.isin(hero)]
        d = d.assign(cls=np.where(d.ed.notna(), "local", "other"))
        t0 = t_dated[k]
        pre, post, au = d[(d.t >= t0 - W) & (d.t < t0)], d[(d.t >= t0) & (d.t < t0 + W)], d[d.mon == 8]
        Tv[k] = {}
        for ti in titles:
            e = rate(post[post.mast == ti], ["cls"]) - rate(pre[pre.mast == ti], ["cls"])
            Tv[k][ti] = value(au[au.mast == ti], e, ["cls"])
    tot = {k: sum(Tv[k].values()) for k in "DBE"}
    pz = xs[xs.grp == "puz"]
    a_puz = aug[aug.grp == "puz"].w.sum() * (
        rate(pz[(pz.t >= t_puz) & (pz.t < t_puz + W)].assign(k=1), ["k"]).iloc[0]
        - rate(pz[(pz.t >= t_puz - W) & (pz.t < t_puz)].assign(k=1), ["k"]).iloc[0])

    # ---------------------------------------------------------------- the ladder
    r2 = {"D": tot["D"], "B": tot["B"], "E": tot["E"], "A": a_puz}
    o2 = sorted(r2, key=r2.get, reverse=True)
    check("rung2.D_leads", o2[0] == "D" and r2["D"] / r2[o2[1]] >= 1.15, {k: round(v) for k, v in r2.items()})
    check("rung3raw.A_leads", out["raw"]["A"] > out["raw"]["C"], out["raw"])
    r3 = {"A": A3, "C": C3, **tot}
    o3 = sorted(r3, key=r3.get, reverse=True)
    check("rung3.A_leads_C_second", o3[:2] == ["A", "C"] and A3 / C3 >= 1.2, (round(A3), round(C3)))
    r4 = {"A": A4, "C": C4, **tot}
    o4 = sorted(r4, key=r4.get, reverse=True)
    check("rung4.C_leads_A_second", o4[:2] == ["C", "A"] and C4 / A4 >= 1.5, (round(C4), round(A4)))
    check("grid.sums", abs(sum(g["C"] for g in out["grid"].values()) - C4) < 1e-3)

    # ---------------------------------------------------------------- lab weight
    cr = pd.read_csv(find(r"crawl_requests"), dtype=str)
    cfg = json.load(open(find(r"crawl_config")))
    ar = pd.read_csv(find(r"asset_register"), dtype=str, keep_default_na=False)
    inv = {v: k for k, v in cid.items()}
    cr["host"] = cr.request_url.str.split("/").str[2]
    cr["path"] = "/" + cr.request_url.str.split("/", n=3).str[3].fillna("")
    cr["b"] = cr.transfer_bytes.astype(float)
    best = pd.Series("", index=cr.index)
    blen = pd.Series(-1, index=cr.index)
    for r in ar.itertuples():
        mm = (cr.host == r.host) & cr.path.str.startswith(r.path_prefix) & (len(r.path_prefix) > blen)
        best[mm] = inv.get(r.change_id, "")
        blen[mm] = len(r.path_prefix)
    cr["own"] = best
    first, last = cfg["crawls"][0]["crawl_date"], cfg["crawls"][-1]["crawl_date"]

    def labw(matched, by_title):
        c = cr[cr.run_status == "complete"]
        fF, fA = c[c.crawl_date == first], c[c.crawl_date == last]
        if matched:
            u = set(fF.page_url) & set(fA.page_url)
            fF, fA = fF[fF.page_url.isin(u)], fA[fA.page_url.isin(u)]
        res = {}
        for ti in (titles if by_title else ["all"]):
            ff = fF if ti == "all" else fF[fF.masthead == ti]
            aa = fA if ti == "all" else fA[fA.masthead == ti]
            for k in "ABCDE":
                res[(ti, k)] = (aa[aa.own == k].b.sum() / aa.page_url.nunique()
                                - ff[ff.own == k].b.sum() / ff.page_url.nunique()) / 1000
        return res
    l0, l1, Lv = labw(False, False), labw(True, False), labw(True, True)
    o0 = sorted("ABCDE", key=lambda k: -l0[("all", k)])
    o1 = sorted("ABCDE", key=lambda k: -l1[("all", k)])
    check("rung0.B_leads_C_low", o0[0] == "B" and o0.index("C") >= 3, o0)
    check("rung1.E_leads_C_low", o1[0] == "E" and o1.index("C") >= 3, o1)

    # ---------------------------------------------------------------- image delivery
    cdn = pd.read_csv(find(r"image_cdn_delivery"))
    agent = cfg["user_agent"].split("/")[0]
    cdn = cdn[(cdn.device_class == "smartphone") & (cdn.ua_family != agent)].copy()
    cdn["bytes"] = np.where(cdn.vendor == "fallback", cdn.bytes_served * 1000.0, cdn.bytes_served)
    cdn["req"] = cdn.edge_hits + cdn.origin_fills
    cdn["m"] = cdn.log_date.str[:7]
    co = pd.read_excel(find(r"closeout"), sheet_name="By title", header=3)
    mv = co.groupby("Month")["Mobile page views"].sum()
    Iv = {m: (cdn[cdn.m == m].req.sum() / mv[m], cdn[cdn.m == m].bytes.sum() / 1000 / mv[m])
          for m in sorted(cdn.m.unique()) if "2026-03" <= m <= "2026-08"}
    # close-out reproduces from the beacons
    for ti, name in titles.items():
        for mo in range(2, 9):
            d = x[(x.mon == mo) & (x.mast == ti)]
            row = co[(co.Month == f"2026-{mo:02d}") & (co.Title == name)].iloc[0]
            if mo in (2, 8):
                check(f"closeout.reproduces[{ti},{mo}]", int(row["Mobile page views"]) == int(d.w.sum())
                      and int(row["Over-line views"]) == int((d.w * (d.sc & d.ov)).sum()))

    # ---------------------------------------------------------------- calibration roster
    rs = pd.read_excel(find(r"closed_fixes"), header=2)
    good = 0
    for r in rs.itertuples(index=False):
        if round((r[5] / r[4] - r[7] / r[6]) * r[9]) == int(r[10]):
            good += 1
    check("roster.11_of_11", good == 11 == len(rs), good)

    # ---------------------------------------------------------------- bins
    def edge(v_, b):
        q = v_ / b - np.floor(v_ / b)
        return b * abs(q - 0.5)
    check("bin.C", edge(C4, 1e4) >= 1500, round(C4))
    check("bin.A", edge(A4, 1e4) >= 1500, round(A4))
    for c, g in out["grid"].items():
        check(f"bin.grid[{c}]", edge(g["A"], 1e4) >= 1000 and edge(g["C"], 1e4) >= 1000,
              (round(g["A"]), round(g["C"])))
    for k in "DBE":
        for ti in titles:
            check(f"bin.T[{k},{ti}]", edge(Tv[k][ti], 1e4) >= 1500, round(Tv[k][ti]))
    for key, val in Lv.items():
        check(f"bin.L[{key}]", edge(val, 0.1) >= 0.01, round(val, 3))
    for mo, (rq, kb) in Iv.items():
        check(f"bin.I[{mo}]", edge(rq, 0.1) >= 0.01 and edge(kb, 0.1) >= 0.01, (round(rq, 3), round(kb, 3)))

    figs = {"C": C4, "A": A4, "grid": out["grid"], "T": Tv, "L": {f"{a}|{b}": v for (a, b), v in Lv.items()},
            "I": Iv, "rung3": {"A": A3, "C": C3}, "raw": out["raw"], "D": tot["D"], "B": tot["B"],
            "E": tot["E"], "lab0": {k[1]: v for k, v in l0.items()}, "lab1": {k[1]: v for k, v in l1.items()}}
    if a.record:
        rec = json.load(open(a.record))
        rf = rec["figures"]
        check("record.C", abs(rf["C"] - C4) < 0.5, (rf["C"], C4))
        check("record.A", abs(rf["A"] - A4) < 0.5, (rf["A"], A4))
        for c in cohorts:
            check(f"record.grid[{c}]", abs(rf["grid"][c]["A"] - out["grid"][c]["A"]) < 0.5 and
                  abs(rf["grid"][c]["C"] - out["grid"][c]["C"]) < 0.5)
        for k in "DBE":
            for ti in titles:
                check(f"record.T[{k},{ti}]", abs(rf["T"][k][ti] - Tv[k][ti]) < 0.5)
        for key, val in figs["L"].items():
            check(f"record.L[{key}]", abs(rec["L"][key] - val) < 1e-6)
        for mo, (rq, kb) in Iv.items():
            check(f"record.I[{mo}]", abs(rec["I"][mo][0] - rq) < 1e-9 and abs(rec["I"][mo][1] - kb) < 1e-6)
    n_ok = sum(1 for r in RESULTS if r[1])
    print(f"verify: {n_ok} of {len(RESULTS)} checks pass")
    print(json.dumps({"C": round(C4), "A": round(A4)}, ensure_ascii=False))
    sys.exit(0 if n_ok == len(RESULTS) else 1)


if __name__ == "__main__":
    main()
