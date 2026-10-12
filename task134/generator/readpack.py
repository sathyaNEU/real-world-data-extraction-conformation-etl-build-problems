"""Read the shipped extracts back into stays and awards: the crosswalk resolves old and merged client numbers,
placement episodes are stitched into stays, the death linkage closes stays and awards the systems had not yet ended.
Used by golden.py and checks.py; verify.py reads the bundle with its own code."""
import datetime as dt

import numpy as np
import pandas as pd

import world as W

ASOF = W.ASOF


def day(s):
    if s is None or (isinstance(s, float) and np.isnan(s)) or s == "":
        return np.inf
    return float((dt.date.fromisoformat(str(s)[:10]) - W.EPOCH).days)


def load(tdir):
    import os
    p = lambda f: os.path.join(tdir, f)
    pl = pd.read_csv(p("care_home_placements_2021-2026.csv"), dtype=str, keep_default_na=False)
    li = pd.read_csv(p("fpnc_payment_lines_2021-2026.csv"), dtype=str, keep_default_na=False)
    cw = pd.read_csv(p("client_id_crosswalk_2023.csv"), dtype=str, keep_default_na=False)
    dl = pd.read_csv(p("nrs_death_linkage_2027-01-15.tsv"), sep="\t", dtype=str, keep_default_na=False)
    return pl, li, cw, dl


def resolver(cw):
    to_new = {}
    for r in cw.itertuples(index=False):
        tgt = r.merged_into or r.client_id
        if r.legacy_client_no:
            to_new[r.legacy_client_no] = tgt
        to_new[r.client_id] = tgt
    deb = {}
    for r in cw.itertuples(index=False):
        if r.debtor_ref:
            deb[r.debtor_ref] = r.merged_into or r.client_id
    return to_new, deb


def stays(pl, cw, dl, types=("PERM",), stitch=True, use_crosswalk=True, use_deaths=True):
    to_new, _ = resolver(cw)
    death = {r.client_id: day(r.date_of_death) for r in dl.itertuples(index=False)}
    x = pl[pl["placement_type"].isin(types)].copy()
    x["cl"] = [to_new.get(c, c) if use_crosswalk else c for c in x["client_id"]]
    x["s"] = [day(v) for v in x["start_date"]]
    x["e"] = [day(v) for v in x["end_date"]]
    x = x.sort_values(["cl", "s"], kind="stable")
    out = []
    for cl, g in x.groupby("cl", sort=True):
        cur = None
        for r in g.itertuples(index=False):
            if cur is not None and stitch and r.s == cur["last_end"] + 1 and cur["reason"] in ("FEE", "MOVE", "SVC"):
                cur["last_end"] = r.e
                cur["reason"] = r.end_reason
                cur["rows"].append(r)
                continue
            if cur is not None:
                out.append(cur)
            cur = dict(cl=cl, admitted=day(r.admitted), entry=r.s, last_end=r.e, reason=r.end_reason, route=r.route,
                       rows=[r], ptype=r.placement_type)
        out.append(cur)
    res = []
    for c in out:
        if c["reason"] in ("DIED", "DISCH", "ENDED"):
            ex = c["last_end"]
        elif not stitch and c["reason"] in ("FEE", "MOVE", "SVC"):
            ex = c["last_end"] + 1
        else:
            ex = np.inf
            if use_deaths and c["cl"] in death and c["entry"] <= death[c["cl"]] <= ASOF:
                ex = death[c["cl"]]
        last = c["rows"][-1]
        res.append(dict(cl=c["cl"], admitted=c["admitted"], entry=c["entry"], exit=ex, route=c["route"],
                        care=1 if last.care_type == "Nursing" else 0, rows=c["rows"], ptype=c["ptype"]))
    return res


def awards(li, cw, dl, use_deaths=True):
    _, deb = resolver(cw)
    death = {r.client_id: day(r.date_of_death) for r in dl.itertuples(index=False)}
    g = li.groupby("debtor_ref", sort=True)
    first = g.first()
    nurs = set(li[li["line_type"] == "FNC"]["debtor_ref"].unique())
    out = []
    for ref, r in first.iterrows():
        a = day(r["admitted"])
        aend = day(r["award_end"])
        why = r["end_reason"]
        if why == "CF":
            end, reason = aend + 1, "CONV"
        elif why in ("DIED", "LEFT"):
            end, reason = aend, "EXIT"
        else:
            end, reason = np.inf, ""
            cl = deb.get(ref)
            if use_deaths and cl in death and death[cl] <= ASOF:
                end, reason = death[cl], "EXIT"
        out.append(dict(ref=ref, admit=a, award=day(r["award_start"]), end=end, reason=reason, care=int(ref in nurs)))
    return out


def inputs(pl, li, cw, dl, **kw):
    st = stays(pl, cw, dl, **{k: v for k, v in kw.items() if k in ("types", "stitch", "use_crosswalk", "use_deaths")})
    aw = awards(li, cw, dl, use_deaths=kw.get("use_deaths", True))
    I = dict(cf_admit=np.array([s["admitted"] if kw.get("cf_admit_col", True) else s["entry"] for s in st]),
             cf_entry=np.array([s["entry"] for s in st]), cf_exit=np.array([s["exit"] for s in st]),
             cf_care=np.array([s["care"] for s in st]), cf_route=np.array([s["route"] for s in st]),
             sf_admit=np.array([a["admit"] for a in aw]), sf_award=np.array([a["award"] for a in aw]),
             sf_entry=np.array([a["admit"] for a in aw]), sf_end=np.array([a["end"] for a in aw]),
             sf_reason=np.array([a["reason"] for a in aw]), sf_care=np.array([a["care"] for a in aw]))
    return I, st, aw


def census(st, ends):
    e = np.array([s["entry"] for s in st])
    x = np.array([s["exit"] for s in st])
    return [int(((e <= t) & (x > t)).sum()) for t in ends]


def month_ends(y0=2024, y1=2026):
    out = []
    for y in range(y0, y1 + 1):
        for m in range(1, 13):
            d = dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)
            out.append(W.dn(d))
    return out
