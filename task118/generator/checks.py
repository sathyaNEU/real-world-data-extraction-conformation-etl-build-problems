"""Every assertion the build makes, computed from the files as written to target/.

The generator's in-memory world is used only where a check is about generation itself (the realised
noise the change log was built with); every figure a solver can read is recomputed from the shipped bytes.
"""
import datetime as dt
import io
import json
import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize

import params as P
import asks as asks_mod
from build_pack import F, DISTRACTORS

SL = P.SHORTLIST
CUL = "CUL-N"
PLATFORM = set(P.SOURCES_PLATFORM)
BIN = 50_000


# ---------------------------------------------------------------------------------- the ledger of checks

class Ledger:
    def __init__(self):
        self.rows = []

    def check(self, name, ok, detail=""):
        self.rows.append((name, bool(ok), detail))
        return bool(ok)


def bin_round(x, step=BIN):
    return int(np.floor(x / step + 0.5) * step)


def bin_margin(x, step=BIN):
    """Distance from x to the nearest rounding boundary of its bin."""
    r = (x / step + 0.5) % 1.0
    return min(r, 1 - r) * step


# ---------------------------------------------------------------------------------- loading

def load(target):
    t = Path(target)
    D = {}
    D["spine"] = pd.read_parquet(t / F["spine"])
    D["arch"] = pd.read_csv(t / F["archive"])
    D["staff"] = pd.read_excel(t / F["staff"], sheet_name="Staff", dtype={"staff_id": str})
    D["plan"] = pd.read_excel(t / F["plan"], sheet_name="Plan 2027")
    D["chg"] = pd.read_excel(t / F["changelog"], sheet_name="Embeddings")
    D["desks"] = pd.read_csv(t / F["desks"])
    D["dash"] = pd.read_csv(t / F["dashboard"], skiprows=6)
    D["cms"] = pd.read_csv(t / F["cms"], keep_default_na=False, dtype=str)
    D["panel"] = pd.read_csv(t / F["panel"])
    D["sec_cur"] = pd.read_excel(t / F["panelwb"], sheet_name="Sections (current)", keep_default_na=False)
    D["sec_hist"] = pd.read_excel(t / F["panelwb"], sheet_name="Section history", keep_default_na=False)
    D["rel"] = pd.read_excel(t / F["panelwb"], sheet_name="Release log", keep_default_na=False)
    return D


def texts(target):
    """Plain text of every shipped file, for vocabulary and single-statement sweeps."""
    from pypdf import PdfReader
    import docx
    out = {}
    for p in sorted(Path(target).iterdir()):
        ext = p.suffix.lower()
        if ext in (".md", ".txt", ".eml", ".csv"):
            out[p.name] = p.read_text(encoding="utf-8")
        elif ext == ".pdf":
            out[p.name] = "\n".join(pg.extract_text() or "" for pg in PdfReader(str(p)).pages)
        elif ext == ".docx":
            out[p.name] = "\n".join(x.text for x in docx.Document(str(p)).paragraphs)
        elif ext == ".xlsx":
            xl = pd.read_excel(p, sheet_name=None, header=None, keep_default_na=False)
            out[p.name] = "\n".join("\t".join(str(v) for v in row) for df in xl.values() for row in df.values)
        else:
            out[p.name] = ""
    return out


# ---------------------------------------------------------------------------------- the estimator family

def packages(arch):
    """One row per variant package with its lift and sampling variance, keyed to its test."""
    a = arch.copy()
    a["ctr"] = a["clicks"] / a["impressions"]
    ctl = a[a["variant"] == "control"].set_index("test_id")[["ctr", "impressions", "clicks"]]
    v = a[a["variant"] != "control"].join(ctl, on="test_id", rsuffix="_c")
    r = v["ctr"] / v["ctr_c"]
    v["L"] = r - 1
    v["S2"] = r ** 2 * ((1 - v["ctr"]) / (v["impressions"] * v["ctr"]) + (1 - v["ctr_c"]) / (v["impressions_c"] * v["ctr_c"]))
    return v


def prior_mom(L, S2):
    return float(L.mean()), max(float(L.var(ddof=0) - S2.mean()), 0.0)


def prior_ml(L, S2):
    L = np.asarray(L, float)
    S2 = np.asarray(S2, float)
    m0 = prior_mom(L, S2)

    def nll(x):
        v = np.exp(x[1]) + S2
        return 0.5 * float(np.sum(np.log(v) + (L - x[0]) ** 2 / v))
    r = minimize(nll, [m0[0], np.log(max(m0[1], 1e-6))], method="Nelder-Mead",
                 options=dict(xatol=1e-10, fatol=1e-10, maxiter=4000))
    return float(r.x[0]), float(np.exp(r.x[1]))


def prior_dl(L, S2):
    L = np.asarray(L, float)
    S2 = np.asarray(S2, float)
    w = 1 / S2
    mw = np.sum(w * L) / np.sum(w)
    Q = np.sum(w * (L - mw) ** 2)
    tau2 = max(0.0, (Q - (len(L) - 1)) / (np.sum(w) - np.sum(w ** 2) / np.sum(w)))
    ws = 1 / (S2 + tau2)
    return float(np.sum(ws * L) / np.sum(ws)), float(tau2)


def test_table(arch, pk, prior):
    """One row per test: desk, article, owner, dates, shipped flag, raw and shrunk winning lift."""
    mu, tau2 = prior
    pk = pk.copy()
    pk["shr"] = mu + tau2 / (tau2 + pk["S2"]) * (pk["L"] - mu)
    first = arch.drop_duplicates("test_id").set_index("test_id")
    shipped = pk[pk["shipped"] == "Y"].set_index("test_id")
    t = first[["engine", "desk_code", "article_id", "owner_staff_id", "started_at", "concluded_at"]].copy()
    t["won"] = t.index.isin(shipped.index)
    t["raw"] = shipped["L"].reindex(t.index).fillna(0.0)
    t["shr"] = shipped["shr"].reindex(t.index).fillna(0.0)
    t["imp"] = arch.groupby("test_id")["impressions"].sum()
    t["clk"] = arch.groupby("test_id")["clicks"].sum()
    t["start"] = pd.to_datetime(t["started_at"].str.replace("Z", ""))
    t["end"] = pd.to_datetime(t["concluded_at"].str.replace("Z", ""))
    return t


def shrink_then_max(pk, prior, test_ids):
    mu, tau2 = prior
    s = mu + tau2 / (tau2 + pk["S2"]) * (pk["L"] - mu)
    m = s.groupby(pk["test_id"]).max().clip(lower=0)
    return float(m.reindex(test_ids).mean())


# ---------------------------------------------------------------------------------- the main ladder

def desk_click_tables(D, tests):
    sp = D["spine"]
    sp = sp.assign(plat=sp["source_code"].isin(PLATFORM), part=sp["source_code"].eq("partner_apps"))
    tested = set(tests["article_id"])
    won = set(tests.loc[tests["won"], "article_id"])
    sp["tested"] = sp["article_id"].isin(tested)
    sp["won"] = sp["article_id"].isin(won)
    out = {}
    for d in P.DESK:
        s = sp[sp["desk_code"] == d]
        pv = s["pageviews"]
        tot = int(pv.sum())
        plat = int(pv[s["plat"]].sum())
        part = int(pv[s["part"]].sum())
        arts = s.drop_duplicates("article_id")
        inwin = arts[(arts["published_date"] >= pd.Timestamp(P.WINDOW_START).date())]
        n_tested = int(arts["tested"].sum())
        out[d] = dict(
            total=tot, plat=plat, part=part, nonpart=tot - part,
            t_all=int(pv[s["tested"]].sum()), t_plat=int(pv[s["plat"] & s["tested"]].sum()),
            t_np=int(pv[~s["part"] & s["tested"]].sum()),
            w_all=int(pv[s["won"]].sum()), w_plat=int(pv[s["plat"] & s["won"]].sum()),
            w_np=int(pv[~s["part"] & s["won"]].sum()),
            n_art=len(arts), n_art_win=len(inwin), n_tested=n_tested,
            plat_old7=int(pv[s["plat"] & s["age_band"].eq("7d+")].sum()),
            plat_preart=int(pv[s["plat"] & ~s["tested"] & (s["published_date"] < pd.Timestamp(P.WINDOW_START).date())].sum()),
            first2h=int(pv[s["age_band"].eq("0-2h")].sum()),
        )
    return out


def cell(L, c, d, base, net):
    x = c[d]
    b = {"all": x["total"], "np": x["nonpart"], "plat": x["plat"]}[base]
    if net == "none":
        f = 1.0
    elif net == "click":
        f = 1 - {"all": x["t_all"], "np": x["t_np"], "plat": x["t_plat"]}[base] / b
    elif net == "count":
        f = 1 - x["n_tested"] / x["n_art"]
    else:
        f = 1 - {"all": x["w_all"], "np": x["w_np"], "plat": x["w_plat"]}[base] / b
    return L[d] * b * f


def lift_bases(D, tests):
    dash = dict(zip(D["dash"]["vertical"], D["dash"]["avg_winning_lift_pct"] / 100))
    desks = D["desks"].set_index("desk_code")
    web = tests[tests["engine"] == "web"]
    raw = web.groupby("desk_code")["raw"].mean().to_dict()
    shr = web.groupby("desk_code")["shr"].mean().to_dict()
    n = web.groupby("desk_code").size().to_dict()
    vert = {d: desks.loc[d, "vertical"] for d in P.WEB}
    pooled = {}
    for d in P.WEB:
        ds = [x for x in P.WEB if vert[x] == vert[d]]
        pooled[d] = sum(n[x] * shr[x] for x in ds) / sum(n[x] for x in ds)
    return {"dash": {d: dash[vert[d]] for d in P.WEB}, "raw": raw, "shr": shr, "pool": pooled}


def rank(vals):
    return sorted(vals, key=vals.get, reverse=True)


# ---------------------------------------------------------------------------------- asks: the CMS

CMS_COLS = ["doc_id", "desk_code", "doc_type", "parent_doc", "revision", "saved_at", "status", "publish_at",
            "headline_sha1", "correction_note", "restored_from_doc", "migrated_from"]


def cms_frames(D):
    c = D["cms"].copy()
    c["revision"] = c["revision"].astype(int)
    c["t"] = pd.to_datetime(c["saved_at"].str.replace("Z", ""))
    return c.sort_values(["doc_id", "revision"])


def cms_rows_of(c):
    return list(c[CMS_COLS].itertuples(index=False, name=None))


def desk_view(arts):
    out = {}
    for d in P.WEB:
        x = [a for a in arts.values() if a["desk"] == d]
        corr = [a for a in x if a["heads"]]
        mins = sorted(int((a["heads"][0] - a.get("go_first", a["go"])).total_seconds() // 60) for a in corr)
        out[d] = dict(count=sum(len(a["heads"]) for a in x), articles=len(x), corrected=len(corr),
                      median=float(np.median(mins)) if mins else float("nan"), mins=mins,
                      texts=sum(len(a["texts"]) for a in x))
    return out


def ask_corrections(rows, **kw):
    return desk_view(asks_mod.read_corrections(rows, **kw))


def off_median(m, g):
    """A median a response would file away from the golden whole minute (a .5 median can round either way)."""
    return abs(m - g) >= (1.5 if m % 1 else 1.0)


# ---------------------------------------------------------------------------------- asks: the panel

def panel_readers(D, mode="golden"):
    """Average monthly unique audience per desk, and the number of section-months it averages over.
    golden: a release's codes read on the section list it was issued on (the first release on the 2026 content
    taxonomy and every later release on the 2026 list), then the latest release per period and section.
    per_period: the rows of the latest release carrying each period (the round-3 path); per_site: the rows of the
    latest release carrying each period and site; per_code: the latest release per period, site and section code,
    then codes read on the list each release was issued on. careful: the latest release per period and code,
    codes read through the section history by period (the round-1 path). lazy: the latest release per period and
    code, read on the current section list. nohist / norestate: golden with the history release / the restated
    release left out. first: the first release per period and code, read by period. national: golden,
    Sport-metro from the national site."""
    p = D["panel"].copy()
    rel = D["rel"].copy()
    pub = dict(zip(rel["release"], pd.to_datetime(rel["published_on"])))
    first26 = pub[rel.loc[rel["note"].str.startswith("First release on the 2026"), "release"].iloc[0]]
    h = D["sec_hist"].copy()
    h["valid_from"] = pd.to_datetime(h["valid_from"])
    h["valid_to"] = pd.to_datetime(h["valid_to"].replace("", pd.NaT))
    lists = {"old": h[h["valid_to"].notna()].set_index(["site_code", "section_code"]),
             "new": h[h["valid_to"].isna()].set_index(["site_code", "section_code"])}
    cur = D["sec_cur"].set_index(["site_code", "section_code"])
    p["pub"] = p["release"].map(pub)
    if mode == "nohist":
        p = p[p["release"] != asks_mod.HISTORY_RELEASE]
    if mode == "norestate":
        p = p[p["release"] != "R26-07B"]
    by_issue = mode in ("golden", "nohist", "norestate", "national", "per_period", "per_site", "per_code")
    if by_issue:
        lst = np.where(p["pub"] >= first26, "new", "old")
        p["section"] = [lists[l].loc[(s, c), "section_name"] for l, s, c in zip(lst, p["site_code"], p["section_code"])]
        p["desk"] = [lists[l].loc[(s, c), "bightline_desk"] for l, s, c in zip(lst, p["site_code"], p["section_code"])]
    p = p.sort_values("pub", kind="stable")
    if mode in ("golden", "nohist", "norestate", "national"):
        p = p.drop_duplicates(["period", "site_code", "section"], keep="last")
    elif mode == "per_period":
        p = p[p["pub"] == p.groupby("period")["pub"].transform("max")]
    elif mode == "per_site":
        p = p[p["pub"] == p.groupby(["period", "site_code"])["pub"].transform("max")]
    else:
        p = p.drop_duplicates(["period", "site_code", "section_code"], keep="first" if mode == "first" else "last")
    if mode == "lazy":
        p["desk"] = [cur.loc[(s, c), "bightline_desk"] for s, c in zip(p["site_code"], p["section_code"])]
    elif not by_issue:
        start = pd.to_datetime(p["period"] + "-01")
        desk = []
        for st, s, c in zip(start, p["site_code"], p["section_code"]):
            x = h[(h["site_code"] == s) & (h["section_code"] == c) & (h["valid_from"] <= st)
                  & (h["valid_to"].isna() | (h["valid_to"] >= st))]
            desk.append(x["bightline_desk"].iloc[0])
        p["desk"] = desk
    out = {}
    for d in P.WEB:
        x = p[p["desk"] == d]
        out[d] = (float(x["unique_audience"].mean()), len(x))
    if mode == "national":
        x = p[(p["site_code"] == "BLN") & (p["section"] == "Sport")]
        out["SPT-M"] = (float(x["unique_audience"].mean()), len(x))
    return out


# ---------------------------------------------------------------------------------- run

def run(W, target, out):
    L_ = Ledger()
    D = load(target)
    T = texts(target)
    rec = {}

    # ----- estimator family on every package
    pk = packages(D["arch"])
    pr_ml = prior_ml(pk["L"], pk["S2"])
    pr_dl = prior_dl(pk["L"], pk["S2"])
    pr_mom = prior_mom(pk["L"], pk["S2"])
    rec["prior"] = dict(ml=pr_ml, dl=pr_dl, mom=pr_mom, packages=len(pk))
    tests = test_table(D["arch"], pk, pr_ml)
    L_.check("archive: one test per article", tests["article_id"].is_unique)
    L_.check("archive: every test has a control and at least one variant",
             (D["arch"].groupby("test_id")["variant"].apply(lambda v: (v == "control").sum() == 1 and len(v) >= 2)).all())
    L_.check("archive: exactly one shipped package per test",
             (D["arch"].groupby("test_id")["shipped"].apply(lambda v: (v == "Y").sum()) == 1).all())

    # ----- ownership and the staff list
    st = D["staff"].copy()
    st["start_date"] = pd.to_datetime(st["start_date"])
    st["end_date"] = pd.to_datetime(st["end_date"])
    sti = st.set_index("staff_id")
    tt = tests.join(sti[["team_code", "start_date", "end_date"]], on="owner_staff_id")
    L_.check("owners: every test owner resolves in the staff list", tt["team_code"].notna().all())
    app = tt[tt["desk_code"].isin(P.APP)]
    L_.check("owners: every app-desk test is owned by the headline squad", (app["team_code"] == "AUD-HS").all())
    sl = tt[tt["desk_code"].isin(SL)]
    L_.check("owners: no squad-owned test at a shortlisted desk", (sl["team_code"] != "AUD-HS").all())
    L_.check("owners: every shortlisted-desk test owner is on that desk's team", (sl["team_code"] == sl["desk_code"]).all())
    act = (tt["start_date"] <= tt["start"].dt.normalize() + pd.Timedelta(days=1)) & \
          (tt["end_date"].isna() | (tt["end_date"] >= tt["start"].dt.normalize() - pd.Timedelta(days=1)))
    L_.check("owners: every owner was on staff on the test date", act.all())
    L_.check("owners: no tester changed team (one team per staff id)", st["staff_id"].is_unique)
    web = tests[tests["engine"] == "web"]
    L_.check("web engine: history begins at the migration and every web test concluded inside the base year",
             (web["start"] >= pd.Timestamp("2025-10-01") - pd.Timedelta(hours=10)).all()
             and (web["end"] < pd.Timestamp("2026-10-01") - pd.Timedelta(hours=10)).all())
    L_.check("web tests conclude inside two hours of publication",
             ((web["end"] - web["start"]) <= pd.Timedelta(minutes=110)).all())

    # ----- clicks: the spine against the plan
    c = desk_click_tables(D, tests)
    plan = D["plan"][D["plan"]["desk_code"] != "Total"].set_index("desk_code")
    L_.check("spine totals per desk equal the plan's 2027 clicks to the click",
             all(c[d]["total"] == int(plan.loc[d, "plan_2027_clicks"]) == int(plan.loc[d, "clicks_oct25_sep26"])
                 for d in P.DESK))
    L_.check("plan total row equals the sum of desks", int(D["plan"].iloc[-1]["plan_2027_clicks"]) == sum(c[d]["total"] for d in P.DESK))
    L_.check("generation tell: no desk total and no plan total on a round thousand",
             all(c[d]["total"] % 1000 != 0 for d in P.DESK) and sum(c[d]["total"] for d in P.DESK) % 1000 != 0)
    L_.check("spine: over 25,000 rows", len(D["spine"]) >= 25_000, "%d rows" % len(D["spine"]))
    L_.check("spine: no duplicate article x source x age key",
             not D["spine"].duplicated(["article_id", "source_code", "age_band"]).any())
    L_.check("spine: every article has one desk", D["spine"].groupby("article_id")["desk_code"].nunique().max() == 1)
    L_.check("spine: every source code is one of the eleven dictionary codes, each in one class",
             set(D["spine"]["source_code"]) <= set(P.SOURCES) and not (PLATFORM & set(P.SOURCES_STORED)))
    appsp = D["spine"][D["spine"]["desk_code"].isin(P.APP)]
    L_.check("blindness: app desks draw platform surfaces only (platform share 1.000)", appsp["source_code"].isin(PLATFORM).all())
    for d in P.APP:
        L_.check("app desk %s: first-two-hours share of clicks at least 10%%" % d, c[d]["first2h"] / c[d]["total"] >= 0.10,
                 "%.3f" % (c[d]["first2h"] / c[d]["total"]))
    for d in P.DESK:
        if c[d]["plat"]:
            L_.check("%s: platform clicks older than 7 days under 1%% of platform clicks" % d,
                     c[d]["plat_old7"] / c[d]["plat"] < 0.01, "%.4f" % (c[d]["plat_old7"] / c[d]["plat"]))
    tgt = {d: __import__("spine").shares(d) for d in P.WEB}
    for d in SL:
        f = c[d]["plat"] / c[d]["total"]
        t = c[d]["t_plat"] / c[d]["plat"]
        L_.check("%s: platform share within 0.5 points of design target" % d, abs(f - P.F_PLAT[d]) <= 0.005, "%.4f" % f)
        L_.check("%s: desk-tested share of platform clicks within 0.5 points of design target" % d,
                 abs(t - P.T_TESTED[d]) <= 0.005 if d != CUL else (0.080 <= t <= 0.090), "%.4f" % t)
    # early traffic covers every test
    sp = D["spine"]
    win = sp[sp["published_date"] >= P.WINDOW_START]
    early = win[win["source_code"].isin(PLATFORM) & win["age_band"].eq("0-2h")].groupby("article_id")["pageviews"].sum()
    inspine = tests[tests["article_id"].isin(early.index)]
    L_.check("no test before the window sits on an article in the spine",
             not tests[(tests["start"] < pd.Timestamp("2025-10-01") - pd.Timedelta(hours=10))]["article_id"].isin(sp["article_id"]).any())
    L_.check("every base-year test's clicks fit inside its article's first-two-hours platform pageviews",
             (inspine["clk"].values <= early.reindex(inspine["article_id"]).values).all())
    L_.check("every web test sits on an article in the spine", tests[tests["engine"] == "web"]["article_id"].isin(early.index).all())

    # monthly coverage: no trend, every month within 4 points of the year
    sp_m = sp.assign(m=pd.to_datetime(sp["published_date"]).dt.to_period("M"))
    sp_m = sp_m[sp_m["source_code"].isin(PLATFORM) & (sp_m["published_date"] >= P.WINDOW_START)]
    sp_m["tested"] = sp_m["article_id"].isin(set(tests["article_id"]))
    worst, slope_max = 0.0, 0.0
    for d in SL:
        x = sp_m[sp_m["desk_code"] == d]
        g = x.groupby("m").apply(lambda q: q.loc[q["tested"], "pageviews"].sum() / q["pageviews"].sum())
        yr = c[d]["t_plat"] / c[d]["plat"]
        worst = max(worst, float(np.max(np.abs(g.values - yr))))
        slope_max = max(slope_max, abs(float(np.polyfit(np.arange(len(g)), g.values, 1)[0])))
    L_.check("coverage: every month's desk-tested share within 4 points of the year at every desk", worst <= 0.04, "%.4f" % worst)
    L_.check("coverage: no monthly trend (slope under 0.3 points a month at every desk)", slope_max < 0.003, "%.5f" % slope_max)

    # ----- the ladder
    LB = lift_bases(D, tests)
    rec["lifts"] = {k: {d: round(100 * v[d], 4) for d in SL} for k, v in LB.items()}
    rungs = {0: ("dash", "all", "none"), 1: ("raw", "all", "none"), 2: ("shr", "all", "none"),
             3: ("shr", "plat", "none"), 4: ("shr", "plat", "click")}
    want = {0: "POL-N", 1: "SPT-M", 2: "BUS-N", 3: "LOC-M", 4: CUL}
    rv = {}
    for k, (lb, b, n) in rungs.items():
        vals = {d: cell(LB[lb], c, d, b, n) for d in SL}
        o = rank(vals)
        rv[k] = vals
        margin = vals[o[0]] / vals[o[1]]
        L_.check("rung %d leader %s" % (k, want[k]), o[0] == want[k], "leader %s" % o[0])
        L_.check("rung %d margin at least %.2f" % (k, 1.45 if k == 4 else 1.20), margin >= (1.45 if k == 4 else 1.20), "%.3f" % margin)
        rec.setdefault("rungs", {})[k] = dict(order=[(d, round(vals[d])) for d in o], margin=round(margin, 4))
    L_.check("adjacent rungs name different desks", all(rank(rv[k])[0] != rank(rv[k + 1])[0] for k in range(4)))
    pos = {k: rank(rv[k]).index(CUL) + 1 for k in rv}
    rec["culture_rank"] = pos
    L_.check("position: Culture 4th or 5th on the natural pipeline (rung 0)", pos[0] in (4, 5), str(pos[0]))
    L_.check("position: Culture never 1st or 2nd at rungs 1 to 3", all(pos[k] > 2 for k in (1, 2, 3)), str(pos))
    r4 = rv[4]
    o4 = rank(r4)
    L_.check("runner-up Local·metro", o4[1] == "LOC-M", o4[1])
    L_.check("runner-up at least 1.15x over the third desk", r4[o4[1]] / r4[o4[2]] >= 1.15, "%.3f" % (r4[o4[1]] / r4[o4[2]]))
    L_.check("rung 4: adjacent desks at least 1.07x apart",
             all(r4[o4[i]] / r4[o4[i + 1]] >= 1.07 for i in range(5)),
             " ".join("%.3f" % (r4[o4[i]] / r4[o4[i + 1]]) for i in range(5)))
    # dominance
    unt = {d: 1 - c[d]["t_plat"] / c[d]["plat"] for d in SL}
    for rival in ("LOC-M", "BUS-N"):
        carried = rv[3][rival] / rv[3][CUL]
        edge = unt[CUL] / unt[rival]
        L_.check("dominance against %s at least 1.2" % rival, edge / carried >= 1.2,
                 "edge %.3f carried %.3f ratio %.3f" % (edge, carried, edge / carried))
        rec.setdefault("dominance", {})[rival] = dict(edge=round(edge, 3), carried=round(carried, 3), ratio=round(edge / carried, 3))

    # ----- the grid, cell by cell
    grid = {}
    for lb in ("dash", "raw", "shr", "pool"):
        for b in ("all", "np", "plat"):
            for n in ("none", "click", "count", "won"):
                vals = {d: cell(LB[lb], c, d, b, n) for d in SL}
                o = rank(vals)
                grid[(lb, b, n)] = (o[0], vals[o[0]] / vals[o[1]], vals[CUL], vals[o[0]] / vals[CUL], vals)
    rec["grid"] = {"/".join(k): (v[0], round(v[1], 3), round(v[2])) for k, v in grid.items()}
    cul_cells = [k for k, v in grid.items() if v[0] == CUL]
    L_.check("grid: 48 cells computed", len(grid) == 48)
    L_.check("grid: only the answer cell and the vertical-pooled click-netting platform cell name Culture",
             sorted(cul_cells) == sorted([("shr", "plat", "click"), ("pool", "plat", "click")]), str(cul_cells))
    L_.check("grid: the vertical-pooled cell carries the identical Culture figure",
             abs(grid[("pool", "plat", "click")][2] - grid[("shr", "plat", "click")][2]) < 0.5)
    others = [v[3] for k, v in grid.items() if k not in cul_cells]
    L_.check("grid: in every other cell Culture sits at least 1.15x behind the leader", min(others) >= 1.15, "%.3f" % min(others))
    expect = GRID_LEADERS
    bad = [("/".join(k), grid[k][0]) for k in grid if expect.get("/".join(k)) != grid[k][0]]
    L_.check("grid: every cell's leader matches the asserted table by name", not bad, str(bad[:6]))
    named = {("shr", "plat", "count"): "LOC-M", ("shr", "plat", "won"): "LOC-M", ("shr", "all", "click"): "BUS-N",
             ("shr", "np", "click"): "BUS-N", ("raw", "plat", "click"): "SPT-M", ("shr", "np", "none"): "BUS-N"}
    for k, v in named.items():
        L_.check("partial correction %s names %s" % ("/".join(k), v), grid[k][0] == v, grid[k][0])
    culfig = {k: v[2] for k, v in grid.items()}
    ans = grid[("shr", "plat", "click")][2]
    L_.check("Culture's answer figure is the minimum of its 48 cell figures", min(culfig.values()) >= ans - 0.5)
    wrong = sorted((abs(v / ans - 1), k, v) for k, v in culfig.items() if k not in cul_cells)
    near = wrong[0]
    L_.check("nearest wrong Culture figure at least 3.5% away, in another bin, in a cell naming another desk",
             near[0] >= 0.035 and bin_round(near[2]) != bin_round(ans) and grid[near[1]][0] != CUL,
             "%s %.0f (%.1f%%)" % ("/".join(near[1]), near[2], 100 * near[0]))
    rec["nearest_wrong_culture"] = ("/".join(near[1]), round(near[2]), round(100 * near[0], 2))

    # ----- graded figures mid-bin, and the admissible variants
    gap = r4[CUL] - r4["LOC-M"]
    L_.check("call figure at least 20,000 inside its 50,000 bin", bin_margin(r4[CUL]) >= 20_000, "%.0f" % bin_margin(r4[CUL]))
    for d in SL:
        L_.check("%s extra clicks at least 15,000 inside its bin" % d, bin_margin(r4[d]) >= 15_000,
                 "%.0f -> %d (%.0f)" % (r4[d], bin_round(r4[d]), bin_margin(r4[d])))
    L_.check("gap at least 15,000 inside its bin, and the rounded and unrounded gaps agree",
             bin_margin(gap) >= 15_000 and bin_round(gap) == bin_round(r4[CUL]) - bin_round(r4["LOC-M"]), "%.0f" % gap)
    golden_bins = {d: bin_round(r4[d]) for d in SL}
    rec["extra_clicks"] = {d: (round(r4[d]), golden_bins[d]) for d in SL}
    rec["gap"] = (round(gap), bin_round(gap))
    # DL prior (convergent), lifts rounded to two decimals, desk-owned netting, old-article and 7d+ edges
    variants = {}
    t_dl = test_table(D["arch"], pk, pr_dl)
    variants["DerSimonian-Laird prior"] = {d: r4[d] * t_dl[(t_dl.engine == "web") & (t_dl.desk_code == d)]["shr"].mean() / LB["shr"][d] for d in SL}
    variants["lifts rounded to two decimals"] = {d: round(100 * LB["shr"][d], 2) / 100 * c[d]["plat"] * unt[d] for d in SL}
    variants["netting on tests owned by the desk's own staff"] = {
        d: LB["shr"][d] * (c[d]["plat"] - sp[sp["desk_code"].eq(d) & sp["source_code"].isin(PLATFORM) & sp["article_id"].isin(
            set(tt.loc[tt["team_code"] == d, "article_id"]))]["pageviews"].sum()) for d in SL}
    variants["articles published before the window left out"] = {
        d: LB["shr"][d] * (c[d]["plat"] * unt[d] - c[d]["plat_preart"]) for d in SL}
    variants["platform clicks at 7 days and older left out"] = {
        d: LB["shr"][d] * (c[d]["plat"] - c[d]["t_plat"] - sp[sp["desk_code"].eq(d) & sp["source_code"].isin(PLATFORM) & sp["age_band"].eq("7d+")
                                                                & ~sp["article_id"].isin(set(tests["article_id"]))]["pageviews"].sum()) for d in SL}
    for name, v in variants.items():
        same = all(bin_round(v[d]) == golden_bins[d] for d in SL) and rank(v)[0] == CUL
        L_.check("admissible variant lands every desk in the same bin: %s" % name, same,
                 " ".join("%s %.0f" % (P.SHORT[d], v[d]) for d in SL))
    devs = {d: abs(variants["DerSimonian-Laird prior"][d] / r4[d] - 1) for d in SL}
    rec["dl_vs_ml_max_dev"] = {P.SHORT[d]: round(100 * v, 3) for d, v in devs.items()}
    L_.check("DerSimonian-Laird within 0.5% of maximum likelihood at every shortlisted desk but Sport·metro",
             all(devs[d] <= 0.005 for d in SL if d != "SPT-M"), str(rec["dl_vs_ml_max_dev"]))

    # ----- clean-data and lens-swap tests
    arch2 = D["arch"].merge(st[["staff_id", "team_code"]], left_on="owner_staff_id", right_on="staff_id", how="left")
    L_.check("clean-data test: owners pre-joined to teams select the same articles at every desk",
             all(set(arch2[(arch2.desk_code == d)]["article_id"]) == set(arch2[(arch2.desk_code == d) & (arch2.team_code == d)]["article_id"]) for d in SL))
    L_.check("clean-data test: answer and rung-3 read unchanged, and they differ", rank(rv[4])[0] == CUL and rank(rv[3])[0] == "LOC-M")
    sub = min(c[d]["t_plat"] / c[d]["plat"] for d in SL)
    L_.check("lens swap: the answer's base is a strict subset of rung 3's, at least 8% smaller at every desk", sub >= 0.08, "%.4f" % sub)

    # ----- the change log: back-test and rivals
    chg = D["chg"].copy()
    emb = []
    for _, r in chg.iterrows():
        y = pd.Timestamp(r["started"]).year
        tid = tests[(tests["desk_code"] == r["desk_code"]) & (tests["start"].dt.year == y) & (tests["engine"] == "app")]
        emb.append(dict(no=int(r["embedding"]), desk=r["desk_code"], year=y, ids=tid.index.tolist(),
                        planned=float(r["planned_clicks_m"]) * 1e6, real=float(r["realised_incremental_clicks"]),
                        lift=float(r["avg_winning_lift_pct"]), n=int(r["tests_run"])))
    L_.check("change log: tests_run and the observed lift reproduce from the archive",
             all(len(e["ids"]) == e["n"] and round(100 * tests.loc[e["ids"], "raw"].mean(), 1) == round(e["lift"], 1) for e in emb))

    def score(pred):
        err = np.array([pred[e["no"]] / e["real"] - 1 for e in emb])
        return int((np.abs(err) <= 0.02).sum()), int((np.abs(err) > 0.03).sum()), float(np.max(np.abs(err))), err

    def lift_of(ids, prior):
        return float(test_table(D["arch"], pk, prior).loc[ids, "shr"].mean())

    gold = {e["no"]: tests.loc[e["ids"], "shr"].mean() * e["planned"] for e in emb}
    h, m3, worst, _ = score(gold)
    L_.check("back-test: shrunk lift x planned clicks reproduces 7 of 7 within 2%, worst at most 1.6%", h == 7 and worst <= 0.016,
             "%d/7 worst %.2f%%" % (h, 100 * worst))
    rec["backtest"] = {"golden": (h, m3, round(100 * worst, 2))}
    raw = {e["no"]: tests.loc[e["ids"], "raw"].mean() * e["planned"] for e in emb}
    h, m3, worst, err = score(raw)
    L_.check("back-test: raw lift reproduces 0 of 7 and overstates every case by at least 1.25x", h == 0 and err.min() >= 0.25,
             "overstates %.2fx to %.2fx" % (1 + err.min(), 1 + err.max()))
    rec["backtest"]["raw"] = (h, m3, round(1 + err.min(), 2), round(1 + err.max(), 2))
    rivals = {}
    pdl = test_table(D["arch"], pk, pr_dl)
    rivals["DerSimonian-Laird prior (convergent)"] = {e["no"]: pdl.loc[e["ids"], "shr"].mean() * e["planned"] for e in emb}
    pmom = test_table(D["arch"], pk, pr_mom)
    rivals["pooled method-of-moments prior"] = {e["no"]: pmom.loc[e["ids"], "shr"].mean() * e["planned"] for e in emb}
    vert = dict(zip(D["desks"]["desk_code"], D["desks"]["vertical"]))
    pk_desk = pk["desk_code"]
    for scope, key in (("per-desk", lambda e: pk_desk == e["desk"]),
                       ("per-vertical", lambda e: pk_desk.map(vert) == vert[e["desk"]]),
                       ("per-embedding", lambda e: pk["test_id"].isin(e["ids"]))):
        for est_name, est in (("method of moments", prior_mom), ("maximum likelihood", prior_ml)):
            pred = {}
            for e in emb:
                sel = key(e)
                pri = est(pk.loc[sel, "L"], pk.loc[sel, "S2"])
                pred[e["no"]] = lift_of(e["ids"], pri) * e["planned"]
            rivals["%s prior (%s)" % (scope, est_name)] = pred
    rawp = np.array([raw[e["no"]] for e in emb])
    realv = np.array([e["real"] for e in emb])
    k = float(np.sum(rawp * realv) / np.sum(rawp ** 2))
    rivals["global haircut on raw lift (k=%.3f)" % k] = {e["no"]: k * raw[e["no"]] for e in emb}
    rivals["shrink every variant then take the maximum"] = {e["no"]: shrink_then_max(pk, pr_ml, e["ids"]) * e["planned"] for e in emb}
    rivals["impression-weighted desk mean"] = {e["no"]: np.average(tests.loc[e["ids"], "shr"], weights=tests.loc[e["ids"], "imp"]) * e["planned"] for e in emb}
    rivals["click-weighted desk mean"] = {e["no"]: np.average(tests.loc[e["ids"], "shr"], weights=tests.loc[e["ids"], "clk"]) * e["planned"] for e in emb}
    post = {d: 1 - c[d]["first2h"] / c[d]["total"] for d in P.APP}
    rivals["post-test clicks only"] = {e["no"]: gold[e["no"]] * post[e["desk"]] for e in emb}
    absp = {}
    a = D["arch"].copy()
    a["ctr"] = a["clicks"] / a["impressions"]
    for e in emb:
        g = a[a["test_id"].isin(e["ids"])]
        ctl = g[g["variant"] == "control"].set_index("test_id")["ctr"]
        shp = g[g["shipped"] == "Y"].set_index("test_id")["ctr"]
        absp[e["no"]] = float((shp - ctl).mean()) * e["planned"]
    rivals["absolute click-through points x clicks"] = absp
    rec["backtest"]["rivals"] = {}
    for name, pred in rivals.items():
        h, m3, worst, err = score(pred)
        rec["backtest"]["rivals"][name] = (h, m3, round(100 * worst, 1))
        if name.startswith("DerSimonian"):
            L_.check("back-test: %s reproduces 7 of 7 within 2%%" % name, h == 7, "%d/7" % h)
        elif name == "post-test clicks only":
            L_.check("back-test: post-test reading misses all 7 by at least 8%", (np.abs(err) >= 0.08).all(), "min %.1f%%" % (100 * np.abs(err).min()))
        else:
            L_.check("back-test refutes %s (at least 2 of 7 missed by more than 3%%)" % name, m3 >= 2, "%d hits, %d misses >3%%, worst %.1f%%" % (h, m3, 100 * worst))
        if name.startswith("per-desk"):
            L_.check("back-test: %s reproduces at most 3 of 7" % name, h <= 3, "%d/7" % h)
    L_.check("back-test: rival family swept", len(rivals) >= 12, "%d rules" % len(rivals))
    twins = [e for e in emb if e["no"] in (3, 6)]
    t3, t6 = twins
    same = (t3["n"] == t6["n"] and t3["lift"] == t6["lift"] and t3["planned"] == t6["planned"]
            and chg.loc[chg.embedding == 3, "distribution"].iloc[0] == chg.loc[chg.embedding == 6, "distribution"].iloc[0])
    ratio = t3["real"] / t6["real"]
    L_.check("twins #3 and #6 identical on tests, lift, planned clicks and distribution", same)
    L_.check("twins' realised gains 2.03x apart (plus or minus 0.05)", abs(ratio - 2.03) <= 0.05, "%.3f" % ratio)
    rec["twins"] = dict(ratio=round(ratio, 3), lift=t3["lift"], tests=t3["n"], planned=t3["planned"])
    sizes = {e["no"]: float(np.log10(a[a["test_id"].isin(e["ids"])]["impressions"].median())) for e in emb}
    ship = {e["no"]: float(tests.loc[e["ids"], "won"].mean()) for e in emb}
    bt = tests[(tests["desk_code"] == "BUS-N")]
    bsize = float(np.log10(a[a["test_id"].isin(bt.index)]["impressions"].median()))
    bship = float(bt["won"].mean())
    near_emb = min(emb, key=lambda e: (sizes[e["no"]] - bsize) ** 2 + (ship[e["no"]] - bship) ** 2)
    L_.check("resemblance: Business·national's test profile is nearest embedding #3, the largest realised gain",
             near_emb["no"] == 3 and max(emb, key=lambda e: e["real"])["no"] == 3,
             "nearest #%d" % near_emb["no"])
    ratios = [e["real"] / e["planned"] for e in sorted(emb, key=lambda e: e["year"])]
    mono = all(x <= y for x, y in zip(ratios, ratios[1:])) or all(x >= y for x, y in zip(ratios, ratios[1:]))
    L_.check("no time trend in realised over planned across the embeddings", not mono)
    L_.check("blindness: no app-desk test owned outside the squad, so every embedding's untested share is 1.000",
             (tt[tt["desk_code"].isin(P.APP)]["team_code"] == "AUD-HS").all())
    L_.check("maturity: the open 2026 embedding is absent from the change log", 2026 not in [e["year"] for e in emb])
    L_.check("generation: realised noise within 1.6%", max(abs(r["eps"]) for r in W.changelog) <= 0.016)

    # ----- figures the characters quote
    sq = st[(st["team_code"] == "AUD-HS") & st["end_date"].isna()]
    L_.check("the brief's squad of six (lead, three headline editors, a producer, a data analyst) is the staff list's "
             "current squad", sorted(sq["role"]) == sorted(["Headline squad lead", "Headline editor", "Headline editor",
                                                             "Headline editor", "Producer", "Data analyst"]),
             str(sorted(sq["role"])))
    zs = []
    for tid, g in D["arch"][D["arch"]["engine"] == "app"].groupby("test_id"):
        shp = g[g["shipped"] == "Y"].iloc[0]
        if shp["variant"] == "control":
            continue
        c0 = g[g["variant"] == "control"].iloc[0]
        p1, p0 = shp["clicks"] / shp["impressions"], c0["clicks"] / c0["impressions"]
        pb = (shp["clicks"] + c0["clicks"]) / (shp["impressions"] + c0["impressions"])
        zs.append((p1 - p0) / np.sqrt(pb * (1 - pb) * (1 / shp["impressions"] + 1 / c0["impressions"])))
    L_.check("Nina Franklin's line holds: every variant the squad shipped cleared 95 per cent (one-sided)",
             min(zs) > 1.645, "min z %.3f over %d shipped variants" % (min(zs), len(zs)))

    # ----- dashboard
    tests_v = tests.assign(v=tests["desk_code"].map(vert))
    lo, hi = pd.Timestamp("2025-10-01") - pd.Timedelta(hours=10), pd.Timestamp("2026-10-01") - pd.Timedelta(hours=10)
    ttm = tests_v[(tests_v["end"] >= lo) & (tests_v["end"] < hi)]
    ok = True
    for _, r in D["dash"].iterrows():
        x = ttm[ttm["v"] == r["vertical"]]
        ok &= len(x) == r["tests_concluded"] and int(x["won"].sum()) == r["tests_with_variant_shipped"] and \
            abs(round(100 * x["raw"].mean(), 2) - r["avg_winning_lift_pct"]) < 1e-9
    L_.check("dashboard reproduces from the archive to the last digit", ok)
    L_.check("dashboard reports verticals only, no desk rows (it ranks nothing on the decision question)",
             not set(D["dash"]["vertical"]) & set(D["desks"]["desk_name"]))

    # ----- the ask layer
    cms = cms_frames(D)
    rows = cms_rows_of(cms)
    GA = asks_mod.read_corrections(rows)
    G = desk_view(GA)
    arts = {d: G[d]["articles"] for d in P.WEB}
    L_.check("CMS articles equal the spine's articles published in the window, desk by desk",
             all(arts[d] == c[d]["n_art_win"] for d in P.WEB), str({P.SHORT[d]: (arts[d], c[d]["n_art_win"]) for d in P.WEB}))
    PR = {m: panel_readers(D, m) for m in ("golden", "per_period", "per_site", "per_code", "careful", "lazy", "nohist",
                                            "first", "norestate", "national")}
    readers = {d: v[0] for d, v in PR["golden"].items()}
    L_.check("readers: every desk's average runs over twelve months of record", all(v[1] == 12 for v in PR["golden"].values()))
    asks = {}
    for d in SL:
        cnt = G[d]["count"]
        asks[d] = dict(extra=r4[d], readers=readers[d], per_reader=r4[d] / readers[d], count=cnt,
                       rate=1000 * cnt / arts[d], median=G[d]["median"], corrected=G[d]["corrected"])
    rec["asks"] = {d: dict(extra=golden_bins[d], readers=int(round(asks[d]["readers"], -3)),
                           per_reader=round(asks[d]["per_reader"], 1), count=asks[d]["count"],
                           rate=round(asks[d]["rate"], 1), median=int(asks[d]["median"]),
                           articles=arts[d], corrected=asks[d]["corrected"],
                           unrounded=dict(readers=round(asks[d]["readers"], 2), per_reader=round(asks[d]["per_reader"], 4),
                                          rate=round(asks[d]["rate"], 4), median=asks[d]["median"]))
                   for d in SL}
    for d in SL:
        x = asks[d]
        L_.check("%s corrected-article count odd" % d, x["corrected"] % 2 == 1, str(x["corrected"]))
        rm = (x["readers"] / 1000 + 0.5) % 1
        L_.check("%s readers at least 150 inside the nearest-thousand bin" % d, min(rm, 1 - rm) * 1000 >= 150, "%.1f" % x["readers"])
        for nm, v, step, need in (("extra per reader", x["per_reader"], 0.1, 0.015), ("rate per 1,000", x["rate"], 0.1, 0.02)):
            q = (v / step + 0.5) % 1
            L_.check("%s %s at least %s inside its one-decimal bin" % (d, nm, need), min(q, 1 - q) * step >= need, "%.4f" % v)
        alt = bin_round(r4[d]) / round(x["readers"], -3)
        L_.check("%s extra per reader: rounded and unrounded paths agree" % d, round(alt, 1) == round(x["per_reader"], 1), "%.4f %.4f" % (alt, x["per_reader"]))
        L_.check("%s median minutes is a whole number (odd count, whole-minute stamps)" % d, float(x["median"]).is_integer())

    def one(v):
        return np.floor(v * 10 + 0.5) / 10

    # every reading that misses one or more of the corrections devices
    R1 = "round-1 path (every revision against the last, first live save, entries ignored, each note read on its own save)"
    R3 = "round-3 path (published states and scheduling handled, entries paired in the same minute, each note read on its own save)"
    READ = {
        R1: dict(published=False, scheduled=False, entries=False, lag=False),
        R3: dict(lag=False, entry_tol=0),
        "round-3 path with an entry's fix timed from the entry going live": dict(lag=False, entry_tol=0, entry_from_entry=True),
        "the story lag caught, entries paired in the same minute": dict(entry_tol=0),
        "the entry lag caught, each note read on its own save": dict(lag=False),
        "published states, scheduling and the story lag handled, entries ignored": dict(entries=False),
        "published states, entries and the story lag handled, first live save": dict(scheduled=False),
        "published states handled only": dict(scheduled=False, entries=False, lag=False),
        "scheduling, entries and the story lag handled, every revision against the last": dict(published=False),
        "scheduling handled only": dict(published=False, entries=False, lag=False),
        "entries handled only": dict(published=False, scheduled=False, lag=False),
    }
    views = {name: ask_corrections(rows, **kw) for name, kw in READ.items()}
    rec["corrections_readings"] = {}
    for name, v in views.items():
        kw = READ[name]
        counts_same = kw.get("published", True) and kw.get("entries", True) and kw.get("lag", True) \
            and kw.get("entry_tol", P.ENTRY_WINDOW) >= max(P.ENTRY_LAG_MINUTES)
        cm = [d for d in SL if v[d]["count"] != G[d]["count"]]
        rm = [d for d in SL if one(1000 * v[d]["count"] / v[d]["articles"]) != one(asks[d]["rate"])]
        mm = [d for d in SL if off_median(v[d]["median"], G[d]["median"])]
        rec["corrections_readings"][name] = {P.SHORT[d]: (v[d]["count"], round(1000 * v[d]["count"] / v[d]["articles"], 2),
                                                          v[d]["median"]) for d in SL}
        L_.check("reading lands off the golden median at every desk: %s" % name, len(mm) == len(SL), str(mm))
        if counts_same:
            L_.check("reading keeps every count and rate (it moves minutes only): %s" % name, not cm and not rm, str(cm))
        else:
            L_.check("reading moves every count and every rate out of its bin: %s" % name,
                     len(cm) == len(SL) and len(rm) == len(SL), "count %s rate %s" % (cm, rm))
        L_.check("reading files no correction at minute 0 or earlier: %s" % name,
                 all(min(v[d]["mins"]) >= 1 for d in P.WEB if v[d]["mins"]))
        L_.check("reading counts the same articles as the spine (the article check passes on it): %s" % name,
                 all(v[d]["articles"] == c[d]["n_art_win"] for d in P.WEB))
    ef_view = ask_corrections(rows, entry_from_entry=True)
    mm = [d for d in SL if off_median(ef_view[d]["median"], G[d]["median"])]
    rec["corrections_readings"]["golden with an entry's fix timed from the entry going live"] = {
        P.SHORT[d]: (ef_view[d]["count"], ef_view[d]["median"]) for d in SL}
    L_.check("timing an entry's fix from the entry, not the live blog, moves the median at five or more desks",
             len(mm) >= 5 and all(ef_view[d]["count"] == G[d]["count"] for d in SL), str(mm))

    # the other stops, ask by ask
    stops = {}
    lazy_cnt = {d: int((cms[cms.desk_code == d]["correction_note"] != "").sum()) for d in SL}
    all_docs = cms.drop_duplicates("doc_id").groupby("desk_code").size().to_dict()
    stops["count: noted revisions (lazy)"] = lazy_cnt
    stops["count: one per corrected article"] = {d: asks[d]["corrected"] for d in SL}
    for nm, kw in (("count: notes that name the headline", dict(by_text=("headline",))),
                   ("count: notes that name the headline, title or heading", dict(by_text=("headline", "title", "heading"))),
                   ("count: carried notes counted again", dict(s1=False)),
                   ("count: every new note a headline correction", dict(s2=False)),
                   ("count: an entry save of any kind pairs with the note", dict(entry_any=True)),
                   ("count: per document, restored and migrated copies kept", dict(merge=False, migrated=True, blank_start=True)),
                   ("count: migrated documents kept", dict(migrated=True, blank_start=True))):
        v = ask_corrections(rows, **kw)
        stops[nm] = {d: v[d]["count"] for d in SL}
    for name, s_ in stops.items():
        rec.setdefault("ask_stops", {})[name] = {P.SHORT[d]: s_[d] for d in SL}
        off = [d for d in SL if s_[d] != asks[d]["count"]]
        L_.check("ask stop lands outside the golden at every desk: %s" % name, len(off) == len(SL), str(off))
    rstops = {}
    rstops["rate: noted revisions over all documents (lazy)"] = {d: 1000 * lazy_cnt[d] / all_docs[d] for d in SL}
    n_posts = cms[cms.doc_type == "post"].drop_duplicates("doc_id")
    n_posts = n_posts[n_posts.restored_from_doc == ""].groupby("desk_code").size().to_dict()
    n_mig = cms[cms.migrated_from != ""].drop_duplicates("doc_id").groupby("desk_code").size().to_dict()
    rstops["rate: posts in the denominator"] = {d: 1000 * asks[d]["count"] / (arts[d] + n_posts.get(d, 0)) for d in SL}
    rstops["rate: migrated documents in the denominator"] = {d: 1000 * asks[d]["count"] / (arts[d] + n_mig.get(d, 0)) for d in SL}
    rstops["rate: every document in the denominator"] = {d: 1000 * asks[d]["count"] / all_docs[d] for d in SL}
    rstops["rate: one per corrected article"] = {d: 1000 * asks[d]["corrected"] / arts[d] for d in SL}
    v = ask_corrections(rows, merge=False, migrated=True, blank_start=True)
    rstops["rate: per document reading (restored and migrated kept)"] = {d: 1000 * v[d]["count"] / v[d]["articles"] for d in SL}
    for name, s_ in rstops.items():
        rec.setdefault("ask_stops", {})[name] = {P.SHORT[d]: round(s_[d], 2) for d in SL}
        off = [d for d in SL if one(s_[d]) != one(asks[d]["rate"])]
        L_.check("ask stop lands outside the golden at every desk: %s" % name, len(off) == len(SL), str(off))
    mstops = {}
    for nm, kw in (("minutes: first note of any kind", dict(s2=False)),
                   ("minutes: per document, restored and migrated copies kept", dict(merge=False, migrated=True, blank_start=True)),
                   ("minutes: migrated documents kept", dict(migrated=True, blank_start=True)),
                   ("minutes: a headline note timed at the note's own save", dict(by_text=("headline",))),
                   ("minutes: every scheduled article live at publish_at (hand-published ones too)", dict(scheduled_always=True))):
        v = ask_corrections(rows, **kw)
        mstops[nm] = {d: v[d]["median"] for d in SL}
    need_m = {"minutes: every scheduled article live at publish_at (hand-published ones too)": 3}
    for name, s_ in mstops.items():
        rec.setdefault("ask_stops", {})[name] = {P.SHORT[d]: s_[d] for d in SL}
        off = [d for d in SL if off_median(s_[d], asks[d]["median"])]
        L_.check("ask stop moves the median at %d or more desks: %s" % (need_m.get(name, 6), name),
                 len(off) >= need_m.get(name, 6), str(off))
    pnames = {"per_period": ("readers: the rows of the latest release carrying each month (the round-3 path)", set(SL)),
              "per_site": ("readers: the rows of the latest release carrying each month and site", {"BUS-N", "SPT-N"}),
              "per_code": ("readers: the latest release per month and section code, codes read on each release's own list",
                           {"BUS-N", "CUL-N"}),
              "careful": ("readers: latest release per code, codes read through the section history by period (the round-1 path)",
                          {"POL-N", "BUS-N", "CUL-N"}),
              "lazy": ("readers: latest release per code, read on the current section list", set(SL)),
              "nohist": ("readers: the history release left out", {"POL-N", "CUL-N"}),
              "first": ("readers: first release per code, read by period", {"POL-N", "SPT-M", "LOC-M", "CUL-N"}),
              "norestate": ("readers: the restated release left out", {"SPT-M", "LOC-M"}),
              "national": ("readers: national site for Sport-metro", {"SPT-M"})}
    for m, (name, need) in pnames.items():
        s_ = {d: PR[m][d][0] for d in SL}
        off = [d for d in SL if round(s_[d], -3) != round(asks[d]["readers"], -3)]
        prox = [d for d in SL if abs(s_[d] / asks[d]["readers"] - 1) > 0.005]
        moved = [d for d in SL if one(r4[d] / s_[d]) != one(asks[d]["per_reader"])]
        rec.setdefault("ask_stops", {})[name] = {P.SHORT[d]: int(round(s_[d], -3)) for d in SL}
        rec.setdefault("readers_months", {})[name] = {P.SHORT[d]: PR[m][d][1] for d in SL}
        rec.setdefault("per_reader_moves", {})[name] = [P.SHORT[d] for d in moved]
        L_.check("ask stop moves readers at %s, each by more than half a per cent: %s" % (
            ", ".join(sorted(P.SHORT[d] for d in need)), name), set(off) >= need and set(prox) >= need, str(off))
    L_.check("readers: the round-1 path moves extra per reader at one or more desks", len(rec["per_reader_moves"][pnames["careful"][0]]) >= 1)
    L_.check("readers: per period, per site and per code each leave a desk off its twelve single months (gaps or doubled "
             "months), and the golden reading alone files twelve at every desk",
             all(any(PR[m][d][1] != 12 for d in SL) for m in ("per_period", "per_site", "per_code"))
             and all(PR["golden"][d][1] == 12 for d in SL))

    # necessity matrix: each device alone mishandled, everything else read the golden way
    dev = {
        "a note on the save after its headline fix read on its own save (story lag)": dict(lag=False),
        "a live blog's note paired with its entry's fix only in the same minute (entry lag)": dict(entry_tol=0),
        "autosave drafts read as published states": dict(published=False),
        "scheduled articles live at their first live save": dict(scheduled=False),
        "entries ignored": dict(entries=False),
        "carried notes counted again": dict(s1=False),
        "every new note a headline correction": dict(s2=False),
        "restored copies as their own documents": dict(merge=False),
        "migrated documents kept, their opening notes counted": dict(migrated=True, blank_start=True),
        "posts as articles": dict(posts=True),
        "never-live documents kept": dict(never_live=True),
    }
    need = {"a note on the save after its headline fix read on its own save (story lag)": (6, 6, 6),
            "a live blog's note paired with its entry's fix only in the same minute (entry lag)": (6, 6, 6),
            "autosave drafts read as published states": (6, 6, 6), "scheduled articles live at their first live save": (0, 0, 6),
            "entries ignored": (6, 6, 6), "carried notes counted again": (6, 6, 0), "every new note a headline correction": (6, 6, 6),
            "restored copies as their own documents": (0, 2, 0), "migrated documents kept, their opening notes counted": (6, 6, 0),
            "posts as articles": (0, 6, 0), "never-live documents kept": (0, 1, 0)}
    for name, kw in dev.items():
        v = ask_corrections(rows, **kw)
        moved_c = [d for d in SL if v[d]["count"] != G[d]["count"]]
        moved_r = [d for d in SL if one(1000 * v[d]["count"] / v[d]["articles"]) != one(asks[d]["rate"])]
        moved_m = [d for d in SL if off_median(v[d]["median"], G[d]["median"])]
        rec.setdefault("necessity", {})[name] = dict(count=[P.SHORT[d] for d in moved_c], rate=[P.SHORT[d] for d in moved_r],
                                                     median=[P.SHORT[d] for d in moved_m])
        L_.check("necessity: %s moves its figures (count %d+, rate %d+, median %d+)" % ((name,) + need[name]),
                 len(moved_c) >= need[name][0] and len(moved_r) >= need[name][1] and len(moved_m) >= need[name][2],
                 "count %s rate %s median %s" % (moved_c, moved_r, moved_m))
    L_.check("necessity: the corrections and readers devices touch no main-path figure (rung 4 unchanged)", rank(rv[4])[0] == CUL)
    first_rows = cms.groupby("doc_id").head(1)
    L_.check("golden reading does not depend on how a document's first revision is compared (no golden chain opens "
             "with a note)", (first_rows[(first_rows["migrated_from"] == "") & (first_rows["restored_from_doc"] == "")]
                              ["correction_note"] == "").all())

    # the devices' structure, as shipped
    golive = {k: a["go"] for k, a in GA.items()}
    by_doc = {k: g_ for k, g_ in cms.groupby("doc_id")}
    sched_live, early, lb_sched, lb_entry_first, bad_sched = 0, 0, 0, 0, []
    posts_by_parent = cms[cms.doc_type == "post"].groupby("parent_doc")["t"].min().to_dict()
    for k, a in GA.items():
        g_ = by_doc[k]
        live = g_[g_.status == "live"]
        sch = g_[(g_.status == "scheduled") & (g_.revision < live["revision"].min())]
        if len(sch):
            pub_t = pd.to_datetime(sch.iloc[-1]["publish_at"].replace("Z", ""))
            first_live = live["t"].min()
            mid = g_[(g_.revision > sch.iloc[-1]["revision"]) & (g_["t"] < pub_t)]
            if pub_t < first_live:
                sched_live += 1
                if (mid.status == "draft").any() or (first_live - pub_t) < pd.Timedelta(minutes=1):
                    bad_sched.append(k)
                if a["type"] == "liveblog":
                    lb_sched += 1
                    if posts_by_parent.get(k, pd.Timestamp.max) < first_live:
                        lb_entry_first += 1
            else:
                early += 1
    L_.check("scheduling: every article the CMS published at publish_at has its first live save after it and no "
             "draft between its scheduled save and publish_at", not bad_sched, str(bad_sched[:3]))
    share = sched_live / len(GA)
    L_.check("scheduling: the CMS published between 20 and 35 per cent of articles at their publish_at, and editors "
             "published others early by hand", 0.20 <= share <= 0.35 and early > 0, "%.3f, early %d" % (share, early))
    L_.check("scheduling: an entry went live before the blog's first live save on at least 80 per cent of live blogs "
             "the CMS published at publish_at", lb_sched and lb_entry_first / lb_sched >= 0.8, "%d of %d" % (lb_entry_first, lb_sched))
    arts_docs = cms[(cms.doc_type != "post") & (cms.migrated_from == "") & (cms.restored_from_doc == "")]
    first_live_t = arts_docs[arts_docs.status == "live"].groupby("doc_id")["t"].min()
    after = arts_docs.join(first_live_t.rename("fl"), on="doc_id")
    late_drafts = after[(after.status == "draft") & (after["t"] > after["fl"])]
    with_auto = late_drafts.groupby("desk_code")["doc_id"].nunique() / arts_docs.drop_duplicates("doc_id").groupby("desk_code").size()
    L_.check("autosaves: at least 12 per cent of articles at every desk carry a draft saved after going live",
             (with_auto.reindex(P.WEB) >= 0.12).all(), str(with_auto.round(3).to_dict()))
    h_times = {(k, t_) for k, a in GA.items() for t_ in a["heads"]}
    ahead = 0
    for _, r in late_drafts.iterrows():
        if any((r["doc_id"], r["t"] + pd.Timedelta(minutes=m)) in h_times for m in range(1, 7)):
            ahead += 1
    L_.check("autosaves: drafts saved just ahead of a headline correction are under a quarter of drafts after going live",
             ahead / len(late_drafts) < 0.25, "%d of %d" % (ahead, len(late_drafts)))
    quiet_lo = pd.Timestamp(dt.datetime(*P.QUIET_FROM)) - pd.Timedelta(hours=10)
    quiet_hi = pd.Timestamp(dt.datetime(*P.QUIET_TO)) - pd.Timedelta(hours=10)
    HB = asks_mod.read_corrections(rows, **READ[R1])
    H3 = asks_mod.read_corrections(rows, **READ[R3])
    EN = asks_mod.read_corrections(rows, entries=False)
    NL = asks_mod.read_corrections(rows, lag=False)
    entry_fix = [(k, t_) for k, a in GA.items() for t_ in a["heads"] if t_ not in EN[k]["heads"]]
    story_lag = [(k, t_) for k, a in GA.items() for t_ in a["heads"] if t_ not in NL[k]["heads"]]
    L_.check("quiet span: no entry headline fix between %s and %s AEST" % (P.QUIET_FROM, P.QUIET_TO),
             not [x for x in entry_fix if quiet_lo <= x[1] < quiet_hi])
    L_.check("quiet span: no headline fix whose note arrived on a later save, in the quiet span",
             not [x for x in story_lag if quiet_lo - pd.Timedelta(hours=1) <= x[1] < quiet_hi + pd.Timedelta(hours=1)])
    per_desk_entry = {d: sum(1 for k, t_ in entry_fix if GA[k]["desk"] == d) for d in P.WEB}
    L_.check("entries: each desk's entry headline fixes equal its planned number", per_desk_entry == P.ENTRY_CORR, str(per_desk_entry))
    same_min = asks_mod.read_corrections(rows, entry_tol=0)
    lagged_entry = {d: sum(1 for k, t_ in entry_fix if GA[k]["desk"] == d and t_ not in same_min[k]["heads"]) for d in P.WEB}
    L_.check("entry lag: every desk has at least one entry headline fix whose blog note came minutes later, as planned",
             lagged_entry == P.ENTRY_LAG, str(lagged_entry))
    per_desk_lag = {d: sum(1 for k, t_ in story_lag if GA[k]["desk"] == d) for d in P.WEB}
    own_heads = {d: G[d]["count"] - per_desk_entry[d] for d in P.WEB}
    lag_share = {d: per_desk_lag[d] / own_heads[d] for d in SL}
    L_.check("story lag: at every shortlisted desk between 15 and 40 per cent of the desk's own headline corrections "
             "have their note on the save after the fix", all(0.15 <= v <= 0.4 for v in lag_share.values()),
             str({P.SHORT[d]: round(v, 3) for d, v in lag_share.items()}))
    # the note and the fix it records, read from the shipped saves
    lag_gaps, lag_named, stray_named = [], [], []
    sl_set = set(story_lag)
    for k, a in GA.items():
        g_ = by_doc[k].sort_values("revision")
        pubd = g_[g_.status == "live"]
        prev = None
        for _, r in pubd.iterrows():
            if prev is not None and r["correction_note"] and r["correction_note"] != prev["correction_note"] \
                    and r["headline_sha1"] == prev["headline_sha1"]:
                old_ = prev["correction_note"]
                nt = r["correction_note"][:len(r["correction_note"]) - len(old_)] if old_ and r["correction_note"].endswith(old_) else r["correction_note"]
                named_ = "headline" in nt.lower()
                if (k, prev["t"].to_pydatetime()) in sl_set:
                    lag_gaps.append(int((r["t"] - prev["t"]).total_seconds() // 60))
                    lag_named.append(named_)
                elif named_ and a["type"] != "liveblog":
                    stray_named.append(k)
            prev = r
    L_.check("story lag: every note that follows its fix comes 1 to 9 minutes after it, on the very next published save, "
             "and names the headline", lag_gaps and len(lag_gaps) == len(story_lag) and min(lag_gaps) >= 1 and max(lag_gaps) <= 9
             and all(lag_named), "%d notes, %s to %s minutes" % (len(lag_gaps), min(lag_gaps or [0]), max(lag_gaps or [0])))
    L_.check("story lag: no other new note on a story save that leaves the headline unchanged names the headline",
             not stray_named, str(stray_named[:3]))
    for N in (9, 10, 15, 20, 30, 45, 60):
        v = ask_corrections(rows, lag_struct=N)
        L_.check("note pairing converges: a note on an unchanged headline paired with the headline published without a "
                 "note up to %d minutes before it files the golden count and median at every desk" % N,
                 all(v[d]["count"] == G[d]["count"] and v[d]["median"] == G[d]["median"] for d in P.WEB))
    for tol in (9, 10, 15, 20, 30, 45, 60):
        v = ask_corrections(rows, entry_tol=tol)
        L_.check("entry pairing converges: a %d-minute window files the golden count and median at every desk" % tol,
                 all(v[d]["count"] == G[d]["count"] and v[d]["median"] == G[d]["median"] for d in P.WEB))
    for tol in (0, 1):
        v = ask_corrections(rows, entry_tol=tol)
        L_.check("entry pairing in the same minute (window %d) misses a lagged entry fix at every desk" % tol,
                 all(v[d]["count"] < G[d]["count"] for d in SL))
    ef = set(entry_fix)
    sl_ = set(story_lag)
    PU = asks_mod.read_corrections(rows, published=False, lag=False)
    auto_a = [(k, t_) for k, a in GA.items() for t_ in a["heads"] if (k, t_) not in ef and (k, t_) not in sl_
              and not any(t_ - pd.Timedelta(minutes=7) <= h_ <= t_ for h_ in PU[k]["heads"])]
    L_.check("quiet span: no headline fix whose autosave carried the headline before the note, in the quiet span",
             not [x for x in auto_a if quiet_lo <= x[1] < quiet_hi])
    per_desk_a = {d: sum(1 for k, t_ in auto_a if GA[k]["desk"] == d) for d in SL}
    L_.check("autosaves: every shortlisted desk has a headline fix whose autosave carried the headline before the note",
             all(v >= 1 for v in per_desk_a.values()), str(per_desk_a))
    rec["devices"] = dict(scheduled_by_cms=sched_live, early=early, entry_fixes=per_desk_entry, entry_lagged=lagged_entry,
                          story_lag={P.SHORT[d]: per_desk_lag[d] for d in P.WEB}, story_lag_share={P.SHORT[d]: round(v, 3) for d, v in lag_share.items()},
                          lag_minutes=(min(lag_gaps or [0]), max(lag_gaps or [0])), autosave_ahead=per_desk_a,
                          late_draft_share={k: round(v, 3) for k, v in with_auto.to_dict().items()})
    heads_notes = []
    for k, a in GA.items():
        g_ = by_doc[k].sort_values("revision")
        for t_ in a["heads"]:
            m = g_[(g_["t"] >= t_) & (g_["correction_note"] != "")]
            if len(m):
                heads_notes.append(m.iloc[0]["correction_note"])
    named = re.compile(r"\b(headline|title|heading)\b", re.I)
    plain = sum(1 for nt in heads_notes if not named.search(nt.split(". ")[0] + "."))
    L_.check("note wording: at least 25 per cent of headline corrections open with a note that names no headline, "
             "title or heading", plain / len(heads_notes) >= 0.25, "%d of %d" % (plain, len(heads_notes)))

    # hygiene battery on the wrong paths
    p_ = D["panel"]
    cur = p_.merge(D["sec_cur"], on=["site_code", "section_code"], how="left", indicator=True)
    L_.check("battery on the readers path: every code joins the current section list, no fan-out",
             (cur["_merge"] == "both").all() and len(cur) == len(p_))
    rep = int(p_.duplicated(["period", "site_code", "section_code"]).sum())
    L_.check("battery: the history and restated releases show as repeated period-site-code keys (24), which the "
             "latest-release rule resolves", rep == 24, str(rep))
    hist_ = D["sec_hist"].copy()
    hist_["valid_from"] = pd.to_datetime(hist_["valid_from"])
    hist_["valid_to"] = pd.to_datetime(hist_["valid_to"].replace("", pd.NaT))
    joined = 0
    for _, r in p_.iterrows():
        st_ = pd.Timestamp(r["period"] + "-01")
        joined += ((hist_["site_code"] == r["site_code"]) & (hist_["section_code"] == r["section_code"])
                   & (hist_["valid_from"] <= st_) & (hist_["valid_to"].isna() | (hist_["valid_to"] >= st_))).sum() == 1
    L_.check("battery: every panel row, the history release included, joins exactly one section-history row by period",
             joined == len(p_))
    sites_of = p_.groupby("release")["site_code"].apply(lambda x: sorted(set(x))).to_dict()
    secs_of = p_[p_.release == asks_mod.HISTORY_RELEASE].groupby("period").size()
    L_.check("partial releases: the history release carries three national sections a month and the restated release "
             "the Brisbane edition site only", sites_of.get(asks_mod.HISTORY_RELEASE) == ["BLN"] and (secs_of == 3).all()
             and sites_of.get("R26-07B") == ["BLB"], str({k: v for k, v in sites_of.items() if k in (asks_mod.HISTORY_RELEASE, "R26-07B")}))
    L_.check("battery on the CMS: (doc_id, revision) unique, every parent and restored source resolves",
             not cms.duplicated(["doc_id", "revision"]).any()
             and set(cms.loc[cms.parent_doc != "", "parent_doc"]) <= set(cms["doc_id"])
             and set(cms.loc[cms.restored_from_doc != "", "restored_from_doc"]) <= set(cms["doc_id"]))
    L_.check("battery on the CMS: publish_at is set on every scheduled revision and on no other",
             ((cms.status == "scheduled") == (cms.publish_at != "")).all())
    posts_share = {d: n_posts.get(d, 0) / arts[d] for d in SL}
    L_.check("HZ4: posts add 35% to 120% to every desk's document count",
             all(0.35 <= v <= 1.2 for v in posts_share.values()), str({P.SHORT[d]: round(v, 2) for d, v in posts_share.items()}))
    L_.check("lazy count overstates by at least 3x at every desk", all(lazy_cnt[d] >= 3 * asks[d]["count"] for d in SL),
             str({P.SHORT[d]: round(lazy_cnt[d] / asks[d]["count"], 1) for d in SL}))
    secs = [a for a in GA.values() if a["heads"]]
    share2 = {d: np.mean([len(a["heads"]) > 1 for a in secs if a["desk"] == d]) for d in SL}
    L_.check("over-cleaning stop: second corrections on 5% to 11% of corrected articles at every desk",
             all(0.05 <= v <= 0.11 for v in share2.values()), str({P.SHORT[d]: round(v, 3) for d, v in share2.items()}))

    # the referee: the bulletin's March figures reproduce, and the round-1 and round-3 paths tie to them too
    btxt = T[F["bulletin"]]
    m = re.search(r"logged (\d+) headline corrections and (\d+) corrections to article text", btxt)
    lo, hi = pd.Timestamp("2026-03-01") - pd.Timedelta(hours=10), pd.Timestamp("2026-04-01") - pd.Timedelta(hours=10)

    def march(A_):
        return (sum(lo <= t_ < hi for a in A_.values() for t_ in a["heads"]),
                sum(lo <= t_ < hi for a in A_.values() for t_ in a["texts"]))
    gm, hm, h3 = march(GA), march(HB), march(H3)
    L_.check("referee: the bulletin's March headline and text counts reproduce from the CMS export",
             m and (int(m.group(1)), int(m.group(2))) == gm, "%s vs %s" % (m.groups() if m else None, gm))
    L_.check("referee: the round-1 path ties to the bulletin's March figures as well (it validates on March)", hm == gm, "%s" % (hm,))
    L_.check("referee: the round-3 path ties to the bulletin's March figures as well (it validates on March)", h3 == gm, "%s" % (h3,))
    for nm_, name_ in (("round-1", R1), ("round-3", R3)):
        outside = {d: (G[d]["count"], views[name_][d]["count"]) for d in SL}
        L_.check("referee: outside March the %s path and the standards rule part at every desk" % nm_,
                 all(a_ != b_ for a_, b_ in outside.values()), str(outside))
    lazy_march = int(((cms["t"] >= lo) & (cms["t"] < hi) & (cms["correction_note"] != "")).sum())
    L_.check("referee: the lazy reading of March is at least 3x the bulletin", lazy_march >= 3 * gm[0], "%d" % lazy_march)
    edge = [t_ for A_ in (GA, HB, H3) for a in A_.values() for t_ in a["heads"] + a["texts"]
            if min(abs((t_ - lo).total_seconds()), abs((t_ - hi).total_seconds())) < 12 * 3600]
    L_.check("referee: no correction within 12 hours of a March boundary on any path (UTC and AEST agree)", not edge)

    full = golden_figures(target)
    # pair simulation
    readings = {
        "round-3 path": (views[R3], "per_period"),
        "round-1 path": (views[R1], "careful"),
        "catches the story lag only": (views["the story lag caught, entries paired in the same minute"], "per_period"),
        "catches the entry lag only": (views["the entry lag caught, each note read on its own save"], "per_period"),
        "catches the partial releases only": (views[R3], "golden"),
        "catches both lags, not the partial releases": (G, "per_period"),
    }
    pair = pair_simulation(asks, rv, r4, readings, PR, golden_bins)
    rec["pair"] = pair
    caps = {"round-3 path": 40, "round-1 path": 45, "catches the story lag only": 40, "catches the entry lag only": 40,
            "catches the partial releases only": 50}
    for label, x in pair.items():
        if label in caps:
            L_.check("pair simulation (%s): top-two average at or under %d" % (label, caps[label]), x["pair"] <= caps[label],
                     "%.1f" % x["pair"])
    main_files = {F[k] for k in ("spine", "archive", "staff", "plan", "changelog", "fieldref", "charter", "desks", "dashboard")}
    nomain = without(target, main_files)
    try:
        dec = (golden_figures(nomain, part="panel")["readers"] == full["readers"]
               and golden_figures(nomain, part="cms")["corrections"] == full["corrections"])
    except Exception:
        dec = False
    L_.check("pair simulation: the device asks recompute with every main-path file deleted, so no ask figure but "
             "extra clicks and extra per reader can move between the cracker and mirror sheets", dec)

    # ----- separation, single statements, vocabulary, dates, gates
    main_docs = [F["fieldref"], F["charter"], F["desks"], F["plan"], F["changelog"], F["staff"]]
    pat = re.compile(r"\b(revisions?|corrections?|posts?|restor\w*|panel|restat\w*|section codes?|autosav\w*|"
                     r"schedul\w*|taxonom\w*|live[- ]blog entr\w*)\b", re.I)
    hits_v = {f: pat.findall(T[f]) for f in main_docs}
    L_.check("separation: no main-path document carries the ask devices' vocabulary", not any(hits_v.values()),
             str({k: v[:3] for k, v in hits_v.items() if v}))
    L_.check("separation: zero CMS or panel rows in main-path files (different keys entirely)",
             not set(D["spine"]["article_id"].astype(str)) & set(cms["doc_id"]))
    single = {
        "pin": "judged on incremental article clicks in the twelve months after it embeds",
        "licensed basis": "average winning lift by vertical",
        "stored headline": "newsletters and alerts. Not included",
        "plan basis": "held at the twelve months to September 2026",
        "note persistence": "copies the\nnote to every later revision",
        "headline rule": "logged on the revision that publishes the corrected headline",
        "entry headline": "with a headline of its own",
        "publish time": "the time set for the CMS to publish the document",
        "history release": "rerun on the 2026 content taxonomy",
        "entry note": "the correction note is added to the live blog",
        "restatement": "These figures replace those published",
        "taxonomy": "2026 content taxonomy",
        "app only": "no web URL, feed entry, search listing",
        "control": "the headline the article was published with",
        "winning lift": "minus one, and zero when the control is kept",
    }
    for name, phrase in single.items():
        norm = lambda z: re.sub(r"\s+", " ", z)
        where = [f for f, txt in T.items() if norm(phrase) in norm(txt)]
        L_.check("single statement: %s appears in exactly one file" % name, len(where) == 1, str(where))
    author = re.compile(r"\b(traps?|decoys?|rungs?|stump\w*|golden|answer key|rubric|determinis\w+|the solver|"
                        r"synthetic|generated by|placeholder|lorem|distractor|python-docx|openpyxl|reportlab|"
                        r"matplotlib|pandas|numpy|faker|pyarrow|xlsxwriter|claude|anthropic)\b", re.I)
    bad = {f: author.findall(t) for f, t in T.items() if author.findall(t)}
    L_.check("no author or toolchain vocabulary anywhere in target/", not bad, str(bad)[:200])
    L_.check("no em dash anywhere in target/", not any("\u2014" in t for t in T.values()))
    late = {}
    for f, t in T.items():
        ds = [d for d in re.findall(r"\b(20\d\d-\d\d-\d\d)\b", t) if d > P.AS_OF.isoformat()]
        if ds:
            late[f] = ds[:3]
    L_.check("no ISO date after the as-of date in any file", not late, str(late))
    ann = re.compile(r"\b(note that|make sure|be sure|remember|be careful|watch out|keep in mind|the correct (basis|population|method)|"
                     r"the right (basis|population|method))\b", re.I)
    an = {f: ann.findall(T[f]) for f in T if f.endswith((".md", ".txt", ".pdf", ".docx", ".eml")) and ann.findall(T[f])}
    L_.check("no announcement sentences in the documents", not an, str(an))
    meta = json.loads((Path(out) / "metadata.json").read_text())
    files = sorted(p.name for p in Path(target).iterdir())
    fmts = sorted({Path(f).suffix for f in files})
    L_.check("gate: at least 10 files", len(files) >= 10, str(len(files)))
    L_.check("gate: at least 3 formats", len(fmts) >= 3, str(fmts))
    L_.check("gate: a file of 25,000 or more rows", len(D["spine"]) >= 25_000)
    L_.check("gate: at least 2 distractors named in metadata.json, each shipped",
             len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]))
    L_.check("gate: the word distractor appears nowhere in target/ or its file names",
             not any("distractor" in t.lower() for t in T.values()) and not any("distractor" in f for f in files))
    nod = golden_figures(without(target, {F[k] for k in DISTRACTORS}))
    L_.check("gate: the distractors are unused (every graded figure recomputes unchanged with both deleted)", full == nod)
    try:
        golden_figures(without(target, {F["cms"], F["cmsnotes"], F["policy"], F["bulletin"]}), part="panel")
        golden_figures(without(target, {F["panel"], F["panelwb"]}), part="cms")
        golden_figures(without(target, {F["cms"], F["panel"], F["panelwb"], F["policy"], F["bulletin"], F["cmsnotes"]}), part="main")
        disjoint = True
    except Exception as e:      # a needed file was missing
        disjoint = False
    L_.check("separation by file: the readers ask, the corrections ask and the main call each recompute without the "
             "others' device files", disjoint)
    L_.check("metadata.json: valid, deliverables two, every file listed with source, date and licence",
             len(meta["deliverables"]) == 2 and sorted(x["path"] for x in meta["files"]) == files
             and all(x["license"] and x["source"] and x["date"] for x in meta["files"]))
    log = pd.read_csv(Path(target) / F["exportlog"])
    L_.check("export log covers every shipped file but itself (set equality)", sorted(log["file"]) == sorted(f for f in files if f != F["exportlog"]))
    names = re.compile(r"(trap|decoy|distractor|naive|rung|stump|ladder|golden|answer|truth|hidden|secret|solution|"
                       r"clean(ed)?_|_fixed|correct(ed)?_|synthetic|generated|_seed|placeholder|dummy|sample_|test_|_v\d+\b|"
                       r"\bcopy\b|backup)", re.I)
    L_.check("no file name carries the author's vocabulary", not [f for f in files if names.search(f)])
    prompt = (Path(out) / "prompt.md").read_text() if (Path(out) / "prompt.md").exists() else (P_TASK / "prompt.md").read_text()
    L_.check("prompt: no input file name appears in it", not [f for f in files if f in prompt])
    L_.check("prompt: no trap word", not author.search(prompt))
    L_.check("prompt: the rounding convention sentence is present",
             "to the nearest 50,000" in prompt and "Click totals are to the nearest 50,000 throughout" in prompt)
    L_.check("container metadata: the producer audit is clean", "clean" in W.scrub_audit, W.scrub_audit[:120])
    hid = []
    for f in files:
        if f.endswith(".xlsx"):
            with zipfile.ZipFile(Path(target) / f) as z:
                wbx = z.read("xl/workbook.xml").decode()
                if "hidden" in wbx or "definedName" in wbx:
                    hid.append(f)
    L_.check("no hidden sheets or defined names in any workbook", not hid, str(hid))

    # ----- report
    n_ok = sum(1 for r in L_.rows if r[1])
    fails = [r for r in L_.rows if not r[1]]
    rec["assertions"] = dict(total=len(L_.rows), passed=n_ok)
    print(json.dumps(rec, indent=1, default=str))
    for name, ok, det in L_.rows:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  [%s]" % det) if det else ""))
    print("\n%d assertions, %d passed, %d failed" % (len(L_.rows), n_ok, len(fails)))
    (Path(out) / ".." ).exists()
    return 0 if not fails else 1


P_TASK = Path(__file__).resolve().parent.parent


def golden_figures(target, part="all"):
    """The graded figures computed from whatever files sit in target (raises if one it needs is absent)."""
    t = Path(target)
    out = {}
    if part in ("all", "main"):
        D = {"spine": pd.read_parquet(t / F["spine"]), "arch": pd.read_csv(t / F["archive"]),
             "desks": pd.read_csv(t / F["desks"]), "dash": pd.read_csv(t / F["dashboard"], skiprows=6)}
        pk = packages(D["arch"])
        tests = test_table(D["arch"], pk, prior_ml(pk["L"], pk["S2"]))
        c = desk_click_tables(D, tests)
        LB = lift_bases(D, tests)
        out["extra"] = {d: round(cell(LB["shr"], c, d, "plat", "click")) for d in SL}
    if part in ("all", "panel"):
        D = {"panel": pd.read_csv(t / F["panel"]),
             "sec_cur": pd.read_excel(t / F["panelwb"], sheet_name="Sections (current)", keep_default_na=False),
             "sec_hist": pd.read_excel(t / F["panelwb"], sheet_name="Section history", keep_default_na=False),
             "rel": pd.read_excel(t / F["panelwb"], sheet_name="Release log", keep_default_na=False)}
        out["readers"] = {d: round(v[0], 2) for d, v in panel_readers(D).items() if d in SL}
    if part in ("all", "cms"):
        cm = cms_frames({"cms": pd.read_csv(t / F["cms"], keep_default_na=False, dtype=str)})
        g = ask_corrections(cms_rows_of(cm))
        out["corrections"] = {d: (g[d]["count"], g[d]["articles"], g[d]["median"]) for d in SL}
    return out


def without(target, drop):
    """A scratch view of target with the named files left out (symlinks, nothing copied)."""
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="t118-"))
    for p in Path(target).iterdir():
        if p.name not in drop:
            (tmp / p.name).symlink_to(p.resolve())
    return tmp


def pair_simulation(asks, rv, r4, readings, PR, golden_bins):
    """Two answer sheets per reading. The cracker lands the call; the mirror stops at rung 3 (Local-metro).
    Each reading is a way a strong response reads the ask files, as (corrections view, readers mode): the round-3
    path (published states and scheduling handled, entries paired in the same minute, each note read on its own
    save; the rows of the latest release carrying each month), the round-1 path, and the paths that catch one
    primary. Planning weights 38 / 7 / 55 over 42 ask criteria; r = 3 survives a wrong call."""
    w_ask = 55 / 42
    one = lambda v: np.floor(v * 10 + 0.5) / 10      # noqa: E731
    gold = {d: dict(extra=golden_bins[d], readers=round(asks[d]["readers"], -3), per_reader=one(asks[d]["per_reader"]),
                    count=asks[d]["count"], rate=one(asks[d]["rate"]), median=asks[d]["median"]) for d in SL}
    out = {}
    for label, (V, pm) in readings.items():
        rd = {d: PR[pm][d][0] for d in SL}
        sheets = {}
        for side in ("cracker", "mirror"):
            ex = {d: (r4[d] if side == "cracker" else rv[3][d]) for d in SL}
            hits_extra = sum(bin_round(ex[d]) == gold[d]["extra"] for d in SL)
            dev = sum(round(rd[d], -3) == gold[d]["readers"] for d in SL)
            dev += sum(one(ex[d] / rd[d]) == gold[d]["per_reader"] for d in SL)
            dev += sum(V[d]["count"] == gold[d]["count"] for d in SL)
            dev += sum(one(1000 * V[d]["count"] / V[d]["articles"]) == gold[d]["rate"] for d in SL)
            dev += sum(not off_median(V[d]["median"], gold[d]["median"]) for d in SL)
            rec_pts = 38 if side == "cracker" else 3
            chart = 5 if side == "cracker" else 1
            score = rec_pts + 7 + w_ask * (hits_extra + chart + 1 + dev)
            sheets[side] = dict(score=round(score, 1), extra_hits=hits_extra, device_hits=dev, leakage=round(dev / 30, 3))
        out[label] = dict(cracker=sheets["cracker"], mirror=sheets["mirror"],
                          pair=round((sheets["cracker"]["score"] + sheets["mirror"]["score"]) / 2, 1))
    return out


# The asserted leader of every grid cell, by name (lift basis / click base / netting).
GRID_LEADERS = {
    "dash/all/none": "POL-N", "dash/all/click": "POL-N", "dash/all/count": "POL-N", "dash/all/won": "POL-N",
    "dash/np/none": "POL-N", "dash/np/click": "POL-N", "dash/np/count": "POL-N", "dash/np/won": "POL-N",
    "dash/plat/none": "LOC-M", "dash/plat/click": "POL-N", "dash/plat/count": "POL-N", "dash/plat/won": "POL-N",
    "raw/all/none": "SPT-M", "raw/all/click": "SPT-M", "raw/all/count": "SPT-M", "raw/all/won": "SPT-M",
    "raw/np/none": "SPT-M", "raw/np/click": "SPT-M", "raw/np/count": "SPT-M", "raw/np/won": "SPT-M",
    "raw/plat/none": "SPT-M", "raw/plat/click": "SPT-M", "raw/plat/count": "SPT-M", "raw/plat/won": "SPT-M",
    "shr/all/none": "BUS-N", "shr/all/click": "BUS-N", "shr/all/count": "BUS-N", "shr/all/won": "BUS-N",
    "shr/np/none": "BUS-N", "shr/np/click": "BUS-N", "shr/np/count": "BUS-N", "shr/np/won": "BUS-N",
    "shr/plat/none": "LOC-M", "shr/plat/click": "CUL-N", "shr/plat/count": "LOC-M", "shr/plat/won": "LOC-M",
    "pool/all/none": "BUS-N", "pool/all/click": "BUS-N", "pool/all/count": "BUS-N", "pool/all/won": "BUS-N",
    "pool/np/none": "BUS-N", "pool/np/click": "BUS-N", "pool/np/count": "BUS-N", "pool/np/won": "BUS-N",
    "pool/plat/none": "LOC-M", "pool/plat/click": "CUL-N", "pool/plat/count": "LOC-M", "pool/plat/won": "LOC-M",
}
