"""Independent verifier for task126: python3 verify_pack.py <target_dir> [--json out.json]

Reads only the shipped files in target_dir. It imports nothing from the generator and reads no seed, parameter or
side file. It rebuilds every construction from the docket, link, action and ledger extracts on its own code path
(pandas and pyarrow, its own Kaplan-Meier), and checks every rung, rival, corpus outcome, published table and graded
figure against the CLAIMS block, which is the answer key.
"""
import datetime as dt
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl import load_workbook

CLAIMS = {
    "rungs": {"R0": 23.1, "R1": 20.8, "R2": 25.4, "R3": 34.0, "R4": 28.9},
    "headline": {"median": 28.9, "lq": 19.7, "undecided_pct": 10.6, "within36_pct": 65.6, "n": 66186},
    "grid": {"chains_grant_end": 37.487, "split_grant_end": 32.033, "left_out": 30.949,
             "parents_chained_cont_added": 31.507, "benefit_dated": 32.756, "parent_at_close": 28.912,
             "decided_only": 26.842, "family_chain": 34.825, "any_docket_cohort": 39.556,
             "calendar_year_2022": 28.912},
    "groups": {"1600": [16.2, 23.4, 79.6], "1700": [17.5, 25.7, 74.1], "2100": [18.4, 26.8, 71.6],
               "2400": [19.8, 28.6, 66.1], "2600": [20.6, 30.0, 63.0], "2800": [21.0, 30.6, 62.5],
               "3600": [21.8, 31.9, 58.6], "3700": [24.0, 35.2, 51.6]},
    "twins": (("22-138479", "23-160047"), ("22-138427", "23-159894")),
}

MONTH = 30.4375
EXTRACT = pd.Timestamp("2026-09-30")
FY22 = (pd.Timestamp("2021-10-01"), pd.Timestamp("2022-09-30"))
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))


def half_up(x):
    return math.floor(x * 10 + 0.5) / 10


def km(days, decided, q):
    """Kaplan-Meier: the first decision time at which the share still waiting falls to 1-q or below."""
    d = np.asarray(days, dtype=float)
    e = np.asarray(decided, dtype=bool)
    times = np.unique(d[e])
    s = 1.0
    for t in times:
        n = np.sum(d >= t)
        k = np.sum((d == t) & e)
        s *= 1 - k / n
        if s <= 1 - q + 1e-12:
            return t
    return None


def fy_of(ts):
    return ts.year + (1 if ts.month >= 10 else 0)


class Pack:
    def __init__(self, target):
        t = Path(target)
        self.t = t
        self.dk = pd.read_parquet(t / "examination_dockets_FY2016_FY2026.parquet")
        self.dk["docketed_on"] = pd.to_datetime(self.dk["docketed_on"])
        self.dk["closed_on"] = pd.to_datetime(self.dk["closed_on"])
        self.dk = self.dk.set_index("docket_no", drop=False)
        self.ln = pd.read_csv(t / "docket_links.csv", dtype=str)
        self.ac = pd.read_parquet(t / "office_actions_FY2016_FY2026.parquet")
        self.ac["served_on"] = pd.to_datetime(self.ac["served_on"])
        self.lg = pd.read_parquet(t / "examiner_production_ledger_FY2016_FY2026.parquet")
        self.xf = pd.read_csv(t / "docket_transfers.csv", dtype=str)
        self.au = pd.read_csv(t / "art_unit_groups.csv", dtype=str, keep_default_na=False)
        self.ro = pd.read_csv(t / "examiner_roster_2026-09-30.csv", dtype=str)
        # decision notice and grant per docket
        fin = self.ac[self.ac["action_code"].isin(["NOA", "REF", "ABN"])]
        assert not fin["docket_no"].duplicated().any()
        self.notice = fin.set_index("docket_no")["served_on"]
        self.notice_code = fin.set_index("docket_no")["action_code"]
        self.grant = self.ac[self.ac["action_code"] == "GRT"].set_index("docket_no")["served_on"]
        # first action on the merits and its credit class
        exr = self.ac[self.ac["action_code"] == "EXR"].sort_values(["served_on", "action_id"])
        first = exr.drop_duplicates("docket_no")
        cls = self.lg[self.lg["credit_class"].isin(["1N", "1R"])].set_index("action_id")["credit_class"]
        self.first_cls = first.set_index("docket_no")["action_id"].map(cls)
        self.first_action = first.set_index("docket_no")["action_id"]
        cx = self.ln[self.ln["link_type"] == "CX"]
        self.cx_child = dict(zip(cx["parent_docket"], cx["child_docket"]))
        self.cx_parent = dict(zip(cx["child_docket"], cx["parent_docket"]))
        self.kids = defaultdict(list)
        for p, c in zip(self.ln.loc[self.ln["link_type"].isin(["CN", "DV"]), "parent_docket"],
                        self.ln.loc[self.ln["link_type"].isin(["CN", "DV"]), "child_docket"]):
            self.kids[p].append(c)
        self.start = self.dk["docketed_on"].to_dict()
        self.not_ = self.notice.to_dict()
        self.gr = self.grant.to_dict()
        self.cls = self.first_cls.to_dict()

    # ---------------------------------------------------------------------------- unit constructions
    def chain_last(self, d):
        while d in self.cx_child:
            d = self.cx_child[d]
        return d

    def end_chain(self, d, grant=False):
        last = self.chain_last(d)
        return self.end_docket(last, grant)

    def end_docket(self, d, grant=False):
        if grant and self.notice_code.get(d) == "NOA":
            return self.gr.get(d)
        return self.not_.get(d)

    def end_app(self, d, grant=False, at_close=False):
        """Split at 1N: follow a CX edge unless the successor's first action is credited 1N."""
        while d in self.cx_child:
            c = self.cx_child[d]
            if self.cls.get(c) != "1N":      # split only where the successor's first action is credited 1N
                d = c
                continue
            return self.dk.at[d, "closed_on"] if at_close else self.not_.get(d)
        return self.end_docket(d, grant)

    def apps(self, lo, hi):
        """Applications filed in [lo, hi]: dockets not opened on a transferred file, and successors whose first
        action is credited 1N."""
        s = self.dk[(self.dk["docketed_on"] >= lo) & (self.dk["docketed_on"] <= hi)]["docket_no"]
        return [d for d in s if d not in self.cx_parent or self.cls.get(d) == "1N"]

    def roots(self, lo, hi):
        s = self.dk[(self.dk["docketed_on"] >= lo) & (self.dk["docketed_on"] <= hi)]["docket_no"]
        return [d for d in s if d not in self.cx_parent]


def durations(starts, ends):
    starts = pd.to_datetime(pd.Series(starts))
    ends = pd.to_datetime(pd.Series(ends))
    dec = ends.notna() & (ends <= EXTRACT)
    days = np.where(dec, (ends - starts).dt.days, (EXTRACT - starts).dt.days)
    return days.astype(float), dec.to_numpy()


def med(starts, ends, q=0.5):
    d, e = durations(starts, ends)
    k = km(d, e, q)
    return k / MONTH


def ladder(pk):
    dk = pk.dk
    lo, hi = FY22
    fy = dk[(dk["docketed_on"] >= lo) & (dk["docketed_on"] <= hi)]
    out = {}
    close = fy["closed_on"].where(fy["closed_on"] <= EXTRACT)
    out["R0"] = med(fy["docketed_on"], close)
    notice = fy["docket_no"].map(pk.not_)
    out["R1"] = med(fy["docketed_on"], notice)
    d, e = durations(fy["docketed_on"], notice)
    e2 = e & (fy["end_code"].to_numpy() != "CX")
    out["R2"] = km(d, e2, 0.5) / MONTH
    roots = pk.roots(lo, hi)
    out["R3"] = med([pk.start[r] for r in roots], [pk.end_chain(r) for r in roots])
    apps = pk.apps(lo, hi)
    ends = [pk.end_app(a) for a in apps]
    out["R4"] = med([pk.start[a] for a in apps], ends)
    return out, roots, apps, ends


def headline(pk, apps, ends):
    d, e = durations([pk.start[a] for a in apps], ends)
    h = {"n": len(apps), "median_days": km(d, e, 0.5), "lq_days": km(d, e, 0.25)}
    h["median"] = half_up(h["median_days"] / MONTH)
    h["lq"] = half_up(h["lq_days"] / MONTH)
    h["undecided_pct"] = half_up(100 * (~e).sum() / len(e))
    h["within36_pct"] = half_up(100 * ((d <= 1095) & e).sum() / len(e))
    h["min_undecided_age_days"] = int(d[~e].min())
    h["at_1095_1096"] = int((((d == 1095) | (d == 1096)) & e).sum())
    alt = {half_up(np.quantile(np.where(e, d, 1e9), 0.5, method=m) / MONTH)
           for m in ("lower", "higher", "midpoint", "linear")}
    h["quantile_definitions_agree"] = alt == {h["median"]}
    # every CX successor on an FY2022 application's chain has a credited first action
    miss = 0
    for a in apps:
        x = a
        while x in pk.cx_child:
            c = pk.cx_child[x]
            miss += c not in pk.cls or pk.cls[c] not in ("1N", "1R")
            if pk.cls.get(c) != "1R":
                break
            x = c
    h["unclassified_successors"] = miss
    return h


def grid(pk, roots, apps):
    lo, hi = FY22
    st = pk.start
    g = {}
    g["chains_grant_end"] = med([st[r] for r in roots], [pk.end_chain(r, grant=True) for r in roots])
    g["split_grant_end"] = med([st[a] for a in apps], [pk.end_app(a, grant=True) for a in apps])
    g["left_out"] = med([st[r] for r in roots], [pk.end_app(r) for r in roots])
    cont = [a for a in apps if a in pk.cx_parent]
    g["parents_chained_cont_added"] = med([st[r] for r in roots] + [st[c] for c in cont],
                                          [pk.end_chain(r) for r in roots] + [pk.end_app(c) for c in cont])
    allcont = [d for d in pk.dk["docket_no"] if d in pk.cx_parent and pk.cls.get(d) == "1N"]
    ben_s, ben_e = [], []
    for c in allcont:
        r = c
        while r in pk.cx_parent:
            r = pk.cx_parent[r]
        if r in st and lo <= st[r] <= hi:
            ben_s.append(st[r])
            ben_e.append(pk.end_app(c))
    g["benefit_dated"] = med([st[r] for r in roots] + ben_s, [pk.end_app(r) for r in roots] + ben_e)
    g["parent_at_close"] = med([st[a] for a in apps], [pk.end_app(a, at_close=True) for a in apps])
    d, e = durations([st[a] for a in apps], [pk.end_app(a) for a in apps])
    g["decided_only"] = float(np.quantile(d[e], 0.5, method="lower")) / MONTH

    def fam_end(x):
        ends = [pk.end_chain(x)]
        y = x
        while True:
            for k in pk.kids.get(y, []):
                ends.append(fam_end(k))
            if y in pk.cx_child:
                y = pk.cx_child[y]
            else:
                break
        return None if any(v is None for v in ends) else max(ends)
    cndv = set(pk.ln.loc[pk.ln["link_type"].isin(["CN", "DV"]), "child_docket"])
    orig = [r for r in roots if r not in cndv]
    g["family_chain"] = med([st[r] for r in orig], [fam_end(r) for r in orig])
    fyd = pk.dk[(pk.dk["docketed_on"] >= lo) & (pk.dk["docketed_on"] <= hi)]["docket_no"]
    anyr = set()
    for x in fyd:
        while x in pk.cx_parent:
            x = pk.cx_parent[x]
        anyr.add(x)
    anyr = sorted(r for r in anyr if r in st)
    g["any_docket_cohort"] = med([st[r] for r in anyr], [pk.end_chain(r) for r in anyr])
    cy = pk.apps(pd.Timestamp("2022-01-01"), pd.Timestamp("2022-12-31"))
    g["calendar_year_2022"] = med([st[a] for a in cy], [pk.end_app(a) for a in cy])
    return g


def corpus(pk):
    wb = load_workbook(pk.t / "saravel_ipo_acknowledgements_FY2019-FY2022.xlsx", read_only=True)
    ws = wb["Acknowledgements"]
    rows = list(ws.iter_rows(min_row=5, values_only=True))
    cases = []
    for r in rows:
        if r[1] is None:
            continue
        cases.append({"no": r[1], "filed": pd.Timestamp(r[2]), "status": r[3], "decision": r[4],
                      "date": pd.Timestamp(r[5]) if r[5] is not None else None})
    qs = {}
    for r in list(wb["Quarterly medians"].iter_rows(min_row=5, values_only=True)):
        if r[0]:
            qs[r[0]] = float(r[3])
    out = {"n": len(cases), "decided": sum(c["status"] == "Decided" for c in cases)}
    code = {"NOA": "Allowance", "REF": "Refusal", "ABN": "Abandonment"}

    def reading(c, how):
        d = c["no"]
        if how == "R3":
            return pk.end_chain(d)
        if how == "R4":
            return pk.end_app(d)
        if how == "R0":
            v = pk.dk.at[d, "closed_on"]
            return None if pd.isna(v) else v
        if how == "R1":
            return pk.not_.get(d)
        if how == "R2":
            return None if pk.dk.at[d, "end_code"] == "CX" else pk.not_.get(d)

    def matches(how):
        hit = 0
        for c in cases:
            v = reading(c, how)
            if c["status"] == "Decided":
                hit += v is not None and v == c["date"]
            else:
                hit += v is None
        return hit
    out["match"] = {h: matches(h) for h in ("R0", "R1", "R2", "R3", "R4")}
    out["types_ok"] = all(code.get(pk.notice_code.get(pk.chain_last(c["no"]))) == c["decision"]
                          for c in cases if c["status"] == "Decided")
    out["blind"] = all(reading(c, "R3") == reading(c, "R4") for c in cases)
    out["n1n_in_chains"] = 0
    for c in cases:
        x = c["no"]
        while x in pk.cx_child:
            x = pk.cx_child[x]
            out["n1n_in_chains"] += pk.cls.get(x) == "1N"

    def qmed(how):
        by = defaultdict(list)
        for c in cases:
            f = c["filed"]
            lab = "%d-Q%d" % (f.year, (f.month - 1) // 3 + 1)
            v = reading(c, how)
            by[lab].append((v - f).days if v is not None else 1e12)
        res = {}
        for lab, v in by.items():
            v = sorted(v)
            n = len(v)
            res[lab] = v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2
        return res
    out["quarters"] = {h: qmed(h) for h in ("R0", "R1", "R2", "R3")}
    out["partner_quarters"] = qs
    return out


def groups(pk, apps, ends):
    au = pk.au
    cur = au[au["valid_to"] == ""].set_index("art_unit")["tg"].to_dict()
    first_x = pk.xf.sort_values(["transferred_on", "docket_no"]).drop_duplicates("docket_no")
    dock_au = first_x.set_index("docket_no")["from_au"].to_dict()

    def asof(a, when):
        rows = au[(au["art_unit"] == a)]
        for _, r in rows.iterrows():
            if pd.Timestamp(r["valid_from"]) <= when and (r["valid_to"] == "" or when <= pd.Timestamp(r["valid_to"])):
                return r["tg"]
    asof_cache = {}

    def asof_c(a, when):
        k = (a, when < pd.Timestamp("2023-10-01"))
        if k not in asof_cache:
            asof_cache[k] = asof(a, when)
        return asof_cache[k]
    home = pk.ro.set_index("examiner_id")["home_art_unit"].to_dict()
    d, e = durations([pk.start[a] for a in apps], ends)
    labs = {
        "answer": [cur[dock_au.get(a, pk.dk.at[a, "art_unit"])] for a in apps],
        "S1_tg_column": [pk.dk.at[a, "tg"] for a in apps],
        "S2b_asof_art_unit_column": [asof_c(pk.dk.at[a, "art_unit"], pk.start[a]) for a in apps],
        "S3_current_group_art_unit_column": [cur[pk.dk.at[a, "art_unit"]] for a in apps],
        "S4_roster_home_au": [cur[home[pk.dk.at[a, "examiner_id"]]] for a in apps],
    }
    out = {}
    for k, lab in labs.items():
        lab = np.array(lab)
        cells = {}
        for g in sorted(set(lab)):
            m = lab == g
            cells[g] = [half_up(km(d[m], e[m], 0.25) / MONTH), half_up(km(d[m], e[m], 0.5) / MONTH),
                        half_up(100 * ((d[m] <= 1095) & e[m]).sum() / m.sum())]
        out[k] = cells
    return out


def tables(pk):
    wb = load_workbook(pk.t / "annual_report_2025_tables_P1_P2.xlsx", read_only=True)
    p1 = {}
    for r in wb["P1"].iter_rows(min_row=6, values_only=True):
        if r[0] and str(r[0]).startswith("FY"):
            p1[int(r[0][2:])] = (r[1], r[2], r[3])
    rec = {}
    dk = pk.dk
    for fy, (n, sh, v) in p1.items():
        if fy < 2016 or not isinstance(v, (int, float)):
            continue
        lo, hi = pd.Timestamp(fy - 1, 10, 1), pd.Timestamp(fy, 9, 30)
        s = dk[(dk["docketed_on"] >= lo) & (dk["docketed_on"] <= hi)]
        rec[fy] = (half_up(med(s["docketed_on"], s["closed_on"])), v, len(s) == n)
    p2 = {}
    years = [c for c in next(wb["P2"].iter_rows(min_row=4, max_row=4, values_only=True))[1:] if c]
    for r in wb["P2"].iter_rows(min_row=5, values_only=True):
        if r[0] and r[0][:4].isdigit():
            for y, v in zip(years, r[1:]):
                p2[(r[0][:4], int(y[2:]))] = v
    fyc = dk["docketed_on"].map(fy_of)
    cnt = dk.groupby([dk["tg"], fyc]).size().to_dict()
    tie = all(cnt.get(k, 0) == v for k, v in p2.items())
    reported = sorted(fy for fy, (n, sh, v) in p1.items() if isinstance(v, (int, float)))
    return {"p1_reproduced": rec, "p2_ties": tie, "p1_reported": reported}


def ledger_integrity(pk):
    lg = pk.lg
    first_ids = set(pk.first_action)
    cls_rows = lg[lg["credit_class"].isin(["1N", "1R"])]
    out = {"one_credit_per_first_action": bool(cls_rows["action_id"].is_unique and set(cls_rows["action_id"]) == first_ids),
           "credits_join_actions": bool(lg["action_id"].isin(pk.ac["action_id"]).all())}
    not_cx = [d for d in pk.first_action.index if d not in pk.cx_parent]
    out["non_successors_all_1N"] = all(pk.cls.get(d) == "1N" for d in not_cx)
    succ = [d for d in pk.first_action.index if d in pk.cx_parent]
    share = defaultdict(lambda: [0, 0])
    for d in succ:
        y = fy_of(pk.start[d])
        share[y][0] += pk.cls.get(d) == "1N"
        share[y][1] += 1
    out["continuing_share_by_year"] = {y: round(a / b, 3) for y, (a, b) in sorted(share.items())}
    return out


def twins(pk, pair):
    def cols(d):
        r = pk.dk.loc[d].drop("docket_no").to_dict()
        acts = pk.ac[pk.ac["docket_no"] == d][["action_code", "served_on"]].sort_values("served_on")
        return r, [tuple(x) for x in acts.to_numpy()]
    (a1, s1), (a2, s2) = pair
    same = cols(a1) == cols(a2) and cols(s1) == cols(s2)
    reex_end = (pk.end_app(a1) - pk.start[a1]).days / MONTH
    cont_parent_end = (pk.end_app(a2) - pk.start[a2]).days / MONTH
    return {"identical": same, "reex_months": half_up(reex_end), "cont_parent_months": half_up(cont_parent_end),
            "classes": (pk.cls.get(s1), pk.cls.get(s2))}


def gates(pk, meta_path):
    names = sorted(p.name for p in pk.t.iterdir())
    out = {"files": len(names), "formats": sorted({Path(n).suffix for n in names}),
           "largest_rows": max(len(pk.ac), len(pk.lg), len(pk.dk))}
    if meta_path and Path(meta_path).exists():
        meta = json.load(open(meta_path))
        out["distractors_shipped"] = all(d in names for d in meta["distractor_files"]) and len(meta["distractor_files"]) >= 2
    return out


def main():
    target = sys.argv[1]
    jpath = sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv else None
    pk = Pack(target)
    rung, roots, apps, ends = ladder(pk)
    h = headline(pk, apps, ends)
    g = grid(pk, roots, apps)
    c = corpus(pk)
    grp = groups(pk, apps, ends)
    tb = tables(pk)
    li = ledger_integrity(pk)
    meta = Path(target).parent / "metadata.json"
    ga = gates(pk, meta)
    tw = twins(pk, CLAIMS["twins"]) if CLAIMS else None
    found = {"rungs": {k: round(v, 3) for k, v in rung.items()}, "headline": h,
             "grid": {k: round(v, 3) for k, v in g.items()}, "corpus_match": c["match"], "corpus_n": c["n"],
             "groups": grp, "tables": tb, "ledger": li, "gates": ga, "twins": tw}
    if jpath:
        with open(jpath, "w") as fh:
            json.dump(found, fh, indent=1, default=str)
    if not CLAIMS:
        print(json.dumps(found, indent=1, default=str))
        return
    K = CLAIMS
    ans = rung["R4"]
    for k, v in K["rungs"].items():
        check("rung %s reproduces %.1f" % (k, v), half_up(rung[k]) == v, round(rung[k], 3))
    check("rung 2 at least 10% below and rung 3 at least 12% above the answer",
          rung["R2"] <= ans * 0.90 and rung["R3"] >= ans * 1.12)
    for k in ("median", "lq", "undecided_pct", "within36_pct", "n"):
        check("headline %s = %s" % (k, K["headline"][k]), h[k] == K["headline"][k], h[k])
    check("headline median at 880 days, robust to one day either way", h["median_days"] == 880)
    check("quantile definitions agree on the headline", h["quantile_definitions_agree"])
    check("no FY2022 decision at 1,095 or 1,096 days", h["at_1095_1096"] == 0)
    check("every undecided FY2022 application at least 48 months old", h["min_undecided_age_days"] >= 1461)
    check("every CX successor on an FY2022 application's chain is classified", h["unclassified_successors"] == 0)
    for k, v in K["grid"].items():
        check("grid %s reproduces %.2f" % (k, v), abs(g[k] - v) < 0.005, round(g[k], 3))
    n = c["n"]
    check("corpus: rungs 3 and 4 reproduce every acknowledgement", c["match"]["R3"] == n and c["match"]["R4"] == n,
          c["match"])
    check("corpus: rungs 0, 1 and 2 each miss more than 1,000 cases",
          all(n - c["match"][k] > 1000 for k in ("R0", "R1", "R2")), c["match"])
    check("corpus: decision types reproduce", c["types_ok"])
    check("corpus: blind to the split", c["blind"] and c["n1n_in_chains"] == 0)
    pq = c["partner_quarters"]
    check("corpus: rung 3 reproduces all 16 quarterly medians",
          len(pq) == 16 and all(c["quarters"]["R3"][q] == pq[q] for q in pq))
    for k in ("R0", "R1", "R2"):
        check("corpus: %s misses all 16 quarterly medians" % k, all(c["quarters"][k][q] != pq[q] for q in pq))
    check("group cells reproduce", grp["answer"] == K["groups"], grp["answer"])
    for k in ("S1_tg_column", "S2b_asof_art_unit_column", "S3_current_group_art_unit_column", "S4_roster_home_au"):
        mv = sum(1 for gg in K["groups"] for z in range(3) if grp[k][gg][z] != K["groups"][gg][z])
        check("stop %s moves at least 16 of 24 cells" % k, mv >= 16, mv)
    check("P1 reproduces from the extract for every year it covers",
          all(v[0] == v[1] and v[2] for v in tb["p1_reproduced"].values()) and len(tb["p1_reproduced"]) >= 4,
          tb["p1_reproduced"])
    check("P1 never reports FY2022", 2022 not in tb["p1_reported"])
    check("P2 ties to the tg column", tb["p2_ties"])
    check("ledger: one 1N or 1R credit on every first action and on no other",
          li["one_credit_per_first_action"] and li["credits_join_actions"])
    check("ledger: every docket not opened on a transferred file is credited 1N", li["non_successors_all_1N"])
    check("ledger: continuing share between 0.24 and 0.30 every year FY2017 to FY2026",
          all(0.24 <= v <= 0.30 for y, v in li["continuing_share_by_year"].items() if y >= 2017))
    check("twin pair identical, 29.3 against 14.5 months, 1R against 1N",
          tw["identical"] and tw["reex_months"] == 29.3 and tw["cont_parent_months"] == 14.5
          and tw["classes"] == ("1R", "1N"), tw)
    check("input gates: 10+ files, 3+ formats, 25,000+ rows, two distractors",
          ga["files"] >= 10 and len(ga["formats"]) >= 3 and ga["largest_rows"] >= 25000
          and ga.get("distractors_shipped", False), ga)
    bad = [r for r in results if not r[1]]
    for name, ok, det in results:
        print("%s  %s  %s" % ("PASS" if ok else "FAIL", name, det if not ok else ""))
    print("checks: %d, failed: %d" % (len(results), len(bad)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
