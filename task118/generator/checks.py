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
from build_pack import F, DISTRACTORS, EXPORT_STAMP
import docs as docs_mod
import world as world_mod

SL = P.SHORTLIST
CUL = "CUL-N"
BUS = "BUS-N"
HOUR, THREE = 60, 180          # the two marks the corrections ask counts against, in minutes
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
    D["pages"] = pd.read_csv(t / F["pages"])
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
    """Every lift basis on the grid; the dashboard basis (rung 0) only when the dashboard export is loaded."""
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
    out = {"raw": raw, "shr": shr, "pool": pooled}
    if "dash" in D:
        dash = dict(zip(D["dash"]["vertical"], D["dash"]["avg_winning_lift_pct"] / 100))
        out = {"dash": {d: dash[vert[d]] for d in P.WEB}, **out}
    return out


def rank(vals):
    return sorted(vals, key=vals.get, reverse=True)


# ---------------------------------------------------------------------------------- asks: the CMS

CMS_COLS = ["doc_id", "desk_code", "doc_type", "parent_doc", "revision", "saved_at", "status", "save_type",
            "publish_at_aest", "headline_sha1", "correction_note", "restored_from_doc", "migrated_from"]


def defaultdict_list():
    from collections import defaultdict
    return defaultdict(list)


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
                      hour=sum(m <= HOUR for m in mins), three=sum(m > THREE for m in mins),
                      texts=sum(len(a["texts"]) for a in x))
    return out


def ask_corrections(rows, **kw):
    return desk_view(asks_mod.read_corrections(rows, **kw))


def cuts(v, d):
    """The three graded cuts of a desk's first-correction minutes under a reading: median, within the hour, after more
    than three hours."""
    return (v[d]["median"], v[d]["hour"], v[d]["three"])


def cuts_off(v, G, d):
    """How many of a desk's three graded cuts a reading files away from the golden."""
    return int(off_median(v[d]["median"], G[d]["median"])) + int(v[d]["hour"] != G[d]["hour"]) + \
        int(v[d]["three"] != G[d]["three"])


def off_median(m, g):
    """A median a response would file away from the golden whole minute (a .5 median can round either way)."""
    return abs(m - g) >= (1.5 if m % 1 else 1.0)


# ---------------------------------------------------------------------------------- asks: the panel

def echo_rows(D):
    """Index of panel rows for a month their release did not publish: the release log gives each release its first
    and last month (the July file's April to June rows)."""
    p, rel = D["panel"], D["rel"]
    span = {r: (lo, hi) for r, lo, hi in zip(rel["release"], rel["first_month"], rel["last_month"])}
    return [i for i, r, per in zip(p.index, p["release"], p["period"]) if not span[r][0] <= per <= span[r][1]]


def panel_readers(D, mode="golden", echo=False):
    """Average monthly unique audience and visits per desk, and the number of section-months they average over:
    {desk: (readers, months, visits)}.
    golden: releases before the release log's first release on the 2026 content taxonomy read on the earlier section
    list, that release and every later one (the history release included) on the 2026 list, then the latest release
    per period and section. echo=True keeps the July file's April to June rows (months the July release did not
    publish, carried in its file), which then win as the latest release. echo=False sets them aside, as the release
    log's months do.
    issue_date: each release read on the list in force on its issue date (the 2026 list from 1 March 2026, so R26-03
    on it). convention: each monthly release counted only for the month its name follows, the history release and
    the restatement for the months their notes name (converges on golden).
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
    if not echo:
        p = p.drop(index=echo_rows(D))
    if mode == "convention":
        noted = {"R26-04H": {"2025-11", "2025-12", "2026-01", "2026-02"}, "R26-07B": {"2026-04", "2026-05", "2026-06"}}

        def month_of(r):
            y, m = 2000 + int(r[1:3]), int(r[4:6])
            y, m = (y, m - 1) if m > 1 else (y - 1, 12)
            return {"%d-%02d" % (y, m)}
        p = p[[per in noted.get(r, month_of(r)) for r, per in zip(p["release"], p["period"])]]
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
    by_issue = mode in ("golden", "nohist", "norestate", "national", "per_period", "per_site", "per_code",
                        "issue_date", "convention")
    if by_issue:
        cut = h.loc[h["valid_to"].isna(), "valid_from"].min() if mode == "issue_date" else first26
        lst = np.where(p["pub"] >= cut, "new", "old")
        p["section"] = [lists[l].loc[(s, c), "section_name"] for l, s, c in zip(lst, p["site_code"], p["section_code"])]
        p["desk"] = [lists[l].loc[(s, c), "bightline_desk"] for l, s, c in zip(lst, p["site_code"], p["section_code"])]
    p = p.sort_values("pub", kind="stable")
    if mode in ("golden", "nohist", "norestate", "national", "issue_date", "convention"):
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
        out[d] = (float(x["unique_audience"].mean()), len(x), float(x["visits"].mean()))
    if mode == "national":
        x = p[(p["site_code"] == "BLN") & (p["section"] == "Sport")]
        out["SPT-M"] = (float(x["unique_audience"].mean()), len(x), float(x["visits"].mean()))
    return out


# ---------------------------------------------------------------------------------- the corrections readings

R1 = "round-1 path (every revision against the last, first live save, entries ignored, each note read on its own save)"
R3 = "round-3 path (published states and scheduling handled, entries paired in the same minute, each note read on its own save)"
R5 = ("round-5 path (a headline note paired with the headline fix up to 10 minutes before it, entries within 10 minutes, "
      "a note put back read as new)")
EF = "both loop-3 devices caught, an entry's fix timed from the entry going live"
AUTO = "the status column read alone (an autosave of a live article taken as published)"
SCHED = "a scheduled time read as going live whenever it precedes the first live save, whatever was saved after it"
READ = {
    SCHED: dict(sched_blind=True),
    AUTO: dict(autosaves=True),
    R1: dict(published=False, scheduled=False, entries=False, lag=False, readd=False),
    R3: dict(lag=False, entry_tol=0, readd=False),
    "round-3 path with an entry's fix timed from the entry going live": dict(lag=False, entry_tol=0, readd=False,
                                                                             entry_from_entry=True),
    R5: dict(lead=False, readd=False, entry_tol=10),
    "round-5 path with an entry's fix timed from the entry going live": dict(lead=False, readd=False, entry_tol=10,
                                                                             entry_from_entry=True),
    "the note before its fix caught, a note put back read as new": dict(readd=False),
    "a note put back caught, the note before its fix missed (pairing looks before the note only)": dict(lead=False),
    EF: dict(entry_from_entry=True),
    "every note on an unchanged headline read on its own save, otherwise golden": dict(lag=False),
    "a live blog's note paired with its entry's fix only in the same minute, otherwise golden": dict(entry_tol=0),
    "published states, scheduling and both pairings handled, entries ignored": dict(entries=False),
    "published states, entries and both pairings handled, first live save": dict(scheduled=False),
    "published states handled only": dict(scheduled=False, entries=False, lag=False, readd=False),
    "scheduling, entries and both pairings handled, every revision against the last": dict(published=False),
    "scheduling handled only": dict(published=False, entries=False, lag=False, readd=False),
    "entries handled only": dict(published=False, scheduled=False, lag=False, readd=False),
}




# ---------------------------------------------------------------------------------- the pages a shipped headline sits on

def page_name(desks, d, src):
    """The page analytics' name for the page a desk's click from one of Bightline's own surfaces starts on, from the
    desk register alone: the edition's home page, the desk's own front and tab, the one app feed, the related links."""
    r = desks.set_index("desk_code").loc[d]
    metro = r["edition"] == "Brisbane"
    name = r["desk_name"] if r["distribution"] == "app only" else r["vertical"]
    return {"home_web": "bightline.com.au/brisbane/" if metro else "bightline.com.au/",
            "section_web": "bightline.com.au/%s%s/" % ("brisbane/" if metro else "", name.lower()),
            "feed_app": "Home feed",
            "section_app": "Tab: %s%s" % ("Brisbane " if metro else "", name),
            "related_links": "Related stories (article pages)"}[src]


def page_rates(pages, how="year"):
    """Each page's click-through: article click-throughs over page views. year: the twelve months summed (the golden);
    monthly: the mean of the twelve monthly rates; median: their median."""
    pg = pages.assign(t=pages["article_clickthroughs"] / pages["page_views"])
    if how == "year":
        s = pg.groupby("page")[["page_views", "article_clickthroughs"]].sum()
        return (s["article_clickthroughs"] / s["page_views"]).to_dict()
    if how == "monthly":
        return pg.groupby("page")["t"].mean().to_dict()
    return pg.groupby("page")["t"].median().to_dict()


def source_tables(D, tested):
    """Per desk and own-page source: every click, and the clicks on articles no archive test covers."""
    sp = D["spine"]
    own = sp[sp["source_code"].isin(PLATFORM)]
    allc = own.groupby(["desk_code", "source_code"])["pageviews"].sum()
    unt = own[~own["article_id"].isin(tested)].groupby(["desk_code", "source_code"])["pageviews"].sum()
    out = {}
    for d in P.DESK:
        out[d] = dict(all={s: int(allc.get((d, s), 0)) for s in P.SOURCES_PLATFORM},
                      unt={s: int(unt.get((d, s), 0)) for s in P.SOURCES_PLATFORM})
    return out


def new_share(by_src, d, rates, desks, kind="page"):
    """The share of a desk's won clicks that is new to Bightline: one minus each page's click-through, weighted by
    where the desk's clicks start (kind page, the golden); or one rate for every page (kind a float)."""
    tot = sum(by_src.values())
    if isinstance(kind, float):
        return 1 - kind
    return sum(n * (1 - rates[page_name(desks, d, s)]) for s, n in by_src.items() if n) / tot


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
    L_.check("plan total row equals the sum of desks",
             int(D["plan"].iloc[-1]["plan_2027_clicks"]) == sum(c[d]["total"] for d in P.DESK))
    L_.check("generation tell: no desk total and no plan total on a round thousand",
             all(c[d]["total"] % 1000 != 0 for d in P.DESK) and sum(c[d]["total"] for d in P.DESK) % 1000 != 0)
    L_.check("spine: over 25,000 rows", len(D["spine"]) >= 25_000, "%d rows" % len(D["spine"]))
    L_.check("spine: no duplicate article x source x age key",
             not D["spine"].duplicated(["article_id", "source_code", "age_band"]).any())
    L_.check("spine: every article has one desk", D["spine"].groupby("article_id")["desk_code"].nunique().max() == 1)
    L_.check("spine: every source code is one of the eleven, each in one class",
             set(D["spine"]["source_code"]) <= set(P.SOURCES) and not (PLATFORM & set(P.SOURCES_STORED)))
    appsp = D["spine"][D["spine"]["desk_code"].isin(P.APP)]
    L_.check("app desks draw on Bightline's own pages only", appsp["source_code"].isin(PLATFORM).all())
    for d in P.DESK:
        if c[d]["plat"]:
            L_.check("%s: own-page clicks older than 7 days under 1%% of own-page clicks" % d,
                     c[d]["plat_old7"] / c[d]["plat"] < 0.01, "%.4f" % (c[d]["plat_old7"] / c[d]["plat"]))
    for d in SL:
        f = c[d]["plat"] / c[d]["total"]
        t = c[d]["t_plat"] / c[d]["plat"]
        L_.check("%s: own-page share within 0.5 points of design target" % d, abs(f - P.F_PLAT[d]) <= 0.005, "%.4f" % f)
        L_.check("%s: desk-tested share of own-page clicks within 0.5 points of design target" % d,
                 abs(t - P.T_TESTED[d]) <= 0.005 if d != CUL else (0.080 <= t <= 0.090), "%.4f" % t)
    sp = D["spine"]
    win = sp[sp["published_date"] >= P.WINDOW_START]
    early = win[win["source_code"].isin(PLATFORM) & win["age_band"].eq("0-2h")].groupby("article_id")["pageviews"].sum()
    inspine = tests[tests["article_id"].isin(early.index)]
    L_.check("no test before the window sits on an article in the spine",
             not tests[(tests["start"] < pd.Timestamp("2025-10-01") - pd.Timedelta(hours=10))]["article_id"].isin(sp["article_id"]).any())
    L_.check("every base-year test's clicks fit inside its article's first-two-hours own-page pageviews",
             (inspine["clk"].values <= early.reindex(inspine["article_id"]).values).all())
    L_.check("every web test sits on an article in the spine", tests[tests["engine"] == "web"]["article_id"].isin(early.index).all())
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

    # ----- the page analytics: every page that shows headlines, its views and the views that end in an article click
    pg = D["pages"]
    desks = D["desks"]
    rates = page_rates(pg)
    rates_m = page_rates(pg, "monthly")
    rates_md = page_rates(pg, "median")
    st_ = source_tables(D, set(tests["article_id"]))
    names_needed = {page_name(desks, d, s) for d in P.DESK for s in P.SOURCES_PLATFORM
                    if st_[d]["all"][s] > 0}
    L_.check("pages: every page a desk's own-page clicks start on is in the page analytics by the name the desk "
             "register gives it, and every page there is one of them", names_needed == set(pg["page"]),
             str(sorted(set(pg["page"]) ^ names_needed)))
    L_.check("pages: one row per page and month, twelve months each, click-throughs under views",
             not pg.duplicated(["month", "page"]).any() and (pg.groupby("page").size() == 12).all()
             and (pg["article_clickthroughs"] < pg["page_views"]).all())
    # the year's article click-throughs on each page equal the spine's own-page clicks that start there
    tie = {}
    for d in P.DESK:
        for s in P.SOURCES_PLATFORM:
            if st_[d]["all"][s]:
                k_ = page_name(desks, d, s)
                tie[k_] = tie.get(k_, 0) + st_[d]["all"][s]
    yr = pg.groupby("page")["article_clickthroughs"].sum().to_dict()
    L_.check("pages: each page's twelve months of article click-throughs equal, to the click, the spine's own-page "
             "clicks that start there (the home pages carry their edition's desks, the related links every desk)",
             all(yr[k_] == v for k_, v in tie.items()), str({k_: (yr[k_], v) for k_, v in tie.items() if yr[k_] != v}))
    dev = max(abs(rates[k_] / P.PAGE_T[k] - 1) for k, _, k_, _ in P.PAGES)
    L_.check("pages: each page's year click-through within 0.5 per cent of its level, every month within 2 per cent",
             dev <= 0.005 and all(abs(r_["article_clickthroughs"] / r_["page_views"] /
                                      P.PAGE_T[[k for k, _, n_, _ in P.PAGES if n_ == r_["page"]][0]] - 1) <= 0.02
                                  for _, r_ in pg.iterrows()), "%.4f" % dev)
    rec["page_rates"] = {k_: round(v, 4) for k_, v in sorted(rates.items())}

    # ----- the change log: the lift back-test (the shrunk winning lift against the realised holdback lift)
    chg = D["chg"].copy()
    emb = []
    for _, r in chg.iterrows():
        y = pd.Timestamp(r["started"]).year
        tid = tests[(tests["desk_code"] == r["desk_code"]) & (tests["start"].dt.year == y) & (tests["engine"] == "app")]
        emb.append(dict(no=int(r["embedding"]), desk=r["desk_code"], year=y, ids=tid.index.tolist(),
                        real=float(r["realised_holdback_lift_pct"]) / 100, lift=float(r["avg_winning_lift_pct"]),
                        n=int(r["tests_run"]), planned=int(r["planned_clicks"]), extra=int(r["extra_clicks_vs_holdback"]),
                        holdback=float(r["holdback_readers_pct"])))
    L_.check("change log: tests_run and the observed lift reproduce from the archive",
             all(len(e["ids"]) == e["n"] and round(100 * tests.loc[e["ids"], "raw"].mean(), 1) == round(e["lift"], 1) for e in emb))
    L_.check("change log: every embedding held back 5 per cent of readers", all(e["holdback"] == 5 for e in emb))

    def score(pred, key="real"):
        err = np.array([pred[e["no"]] / e[key] - 1 for e in emb])
        return int((np.abs(err) <= 0.02).sum()), int((np.abs(err) > 0.03).sum()), float(np.max(np.abs(err))), err

    gold_l = {e["no"]: tests.loc[e["ids"], "shr"].mean() for e in emb}
    h, m3, worst, _ = score(gold_l)
    L_.check("back-test: the shrunk lift reproduces 7 of 7 realised holdback lifts within 2%, worst at most 1.6%",
             h == 7 and worst <= 0.016, "%d/7 worst %.2f%%" % (h, 100 * worst))
    rec["backtest"] = {"lift": (h, m3, round(100 * worst, 2))}
    raw_l = {e["no"]: tests.loc[e["ids"], "raw"].mean() for e in emb}
    h, m3, worst, err = score(raw_l)
    L_.check("back-test: raw lift reproduces 0 of 7 and overstates every case by at least 1.25x", h == 0 and err.min() >= 0.25,
             "overstates %.2fx to %.2fx" % (1 + err.min(), 1 + err.max()))
    rec["backtest"]["raw"] = (h, m3, round(1 + err.min(), 2), round(1 + err.max(), 2))
    lrivals = {}
    for nm_, pri in (("DerSimonian-Laird prior (convergent)", pr_dl), ("pooled method-of-moments prior", pr_mom)):
        tx = test_table(D["arch"], pk, pri)
        lrivals[nm_] = {e["no"]: tx.loc[e["ids"], "shr"].mean() for e in emb}
    vert = dict(zip(D["desks"]["desk_code"], D["desks"]["vertical"]))
    for scope, key in (("per-desk", lambda e: pk["desk_code"] == e["desk"]),
                       ("per-embedding", lambda e: pk["test_id"].isin(e["ids"]))):
        pred = {}
        for e in emb:
            sel = key(e)
            tx = test_table(D["arch"], pk, prior_ml(pk.loc[sel, "L"], pk.loc[sel, "S2"]))
            pred[e["no"]] = tx.loc[e["ids"], "shr"].mean()
        lrivals["%s prior (maximum likelihood)" % scope] = pred
    rawp = np.array([raw_l[e["no"]] for e in emb])
    realv = np.array([e["real"] for e in emb])
    k_ = float(np.sum(rawp * realv) / np.sum(rawp ** 2))
    lrivals["global haircut on raw lift (k=%.3f)" % k_] = {e["no"]: k_ * raw_l[e["no"]] for e in emb}
    lrivals["shrink every variant then take the maximum"] = {e["no"]: shrink_then_max(pk, pr_ml, e["ids"]) for e in emb}
    lrivals["impression-weighted desk mean"] = {e["no"]: np.average(tests.loc[e["ids"], "shr"], weights=tests.loc[e["ids"], "imp"]) for e in emb}
    rec["backtest"]["lift_rivals"] = {}
    for name, pred in lrivals.items():
        h, m3, worst, err = score(pred)
        rec["backtest"]["lift_rivals"][name] = (h, m3, round(100 * worst, 1))
        if "(convergent)" in name:
            L_.check("back-test: %s reproduces 7 of 7 within 2%%" % name, h == 7, "%d/7 worst %.2f%%" % (h, 100 * worst))
        else:
            L_.check("back-test refutes %s (at least 2 of 7 missed by more than 3%%)" % name, m3 >= 2,
                     "%d hits, %d misses >3%%, worst %.1f%%" % (h, m3, 100 * worst))

    # ----- the change log: the clicks back-test (planned clicks x realised lift x the share new to Bightline against
    # the extra clicks the embedding measured against its holdback)
    mix_app = {d: st_[d]["all"] for d in P.APP}
    kept = {e["no"]: e["extra"] / (e["planned"] * e["real"]) for e in emb}
    avg_kept = float(np.mean(list(kept.values())))
    site_rate = float(pg["article_clickthroughs"].sum() / pg["page_views"].sum())
    own_app_pages = {page_name(desks, d, s) for d in P.APP for s in P.SOURCES_PLATFORM if mix_app[d][s]}
    app_rate = float(pg[pg["page"].isin(own_app_pages)]["article_clickthroughs"].sum()
                     / pg[pg["page"].isin(own_app_pages)]["page_views"].sum())
    # one factor per kind of page, fitted on the seven embeddings (feed, tab, related links)
    X = np.array([[mix_app[e["desk"]][s] / sum(mix_app[e["desk"]].values()) for s in ("feed_app", "section_app", "related_links")]
                  for e in emb])
    fac = np.linalg.lstsq(X, np.array([kept[e["no"]] for e in emb]), rcond=None)[0]
    FAC = {"home_web": fac[0], "feed_app": fac[0], "section_web": fac[1], "section_app": fac[1], "related_links": fac[2]}
    shares = {
        "each page's own click-through (golden)": lambda d, mix: new_share(mix, d, rates, desks),
        "each page's mean monthly click-through (convergent)": lambda d, mix: new_share(mix, d, rates_m, desks),
        "each page's median monthly click-through (convergent)": lambda d, mix: new_share(mix, d, rates_md, desks),
        "no share: every won click new": lambda d, mix: 1.0,
        "one share for every desk, the embeddings' average": lambda d, mix: avg_kept,
        "one click-through for every page, the site's": lambda d, mix: 1 - site_rate,
        "one click-through for every page, the app pages'": lambda d, mix: 1 - app_rate,
        "the home feed's click-through for every page": lambda d, mix: 1 - rates["Home feed"],
        "one factor per kind of page fitted on the embeddings": lambda d, mix: sum(mix[s] * FAC[s] for s in mix) / sum(mix.values()),
    }
    rec["backtest"]["clicks"] = {}
    click_pred = {}
    for name, fn in shares.items():
        pred = {e["no"]: e["planned"] * e["real"] * fn(e["desk"], mix_app[e["desk"]]) for e in emb}
        click_pred[name] = pred
        h, m3, worst, err = score(pred, "extra")
        rec["backtest"]["clicks"][name] = (h, m3, round(100 * worst, 1))
    gh = rec["backtest"]["clicks"]["each page's own click-through (golden)"]
    L_.check("back-test, clicks: planned clicks x realised lift x each page's share of views with no article click "
             "reproduces 7 of 7 embeddings' extra clicks against the holdback within 2%", gh[0] == 7, str(gh))
    for name in ("each page's mean monthly click-through (convergent)", "each page's median monthly click-through (convergent)"):
        L_.check("back-test, clicks: %s reproduces 7 of 7 within 2%%" % name, rec["backtest"]["clicks"][name][0] == 7,
                 str(rec["backtest"]["clicks"][name]))
    for name in ("no share: every won click new", "one share for every desk, the embeddings' average",
                 "one click-through for every page, the site's", "one click-through for every page, the app pages'",
                 "the home feed's click-through for every page"):
        x = rec["backtest"]["clicks"][name]
        L_.check("back-test, clicks: refutes %s (at least 4 of 7 missed by more than 3%%, worst at least 20%%)" % name,
                 x[1] >= 4 and x[2] >= 20, str(x))
    fx = rec["backtest"]["clicks"]["one factor per kind of page fitted on the embeddings"]
    rec["page_kind_factors"] = dict(feed=round(fac[0], 4), tab=round(fac[1], 4), related=round(fac[2], 4))
    L_.check("back-test, clicks: one factor per kind of page fitted on the seven embeddings (home pages read as the "
             "feed, fronts as the tabs) also fits every embedding within 3%, a second route to the same share",
             fx[1] == 0, str(fx))
    L_.check("generation: the embeddings' measured extra clicks within 1.2% of the pass-through they were built on",
             max(abs(r_["extra"] / (r_["planned"] * r_["realised_pct"] / 100 * r_["rho"]) - 1) for r_ in W.changelog) <= 0.0125)

    # ----- the ladder
    LB = lift_bases(D, tests)
    rec["lifts"] = {k: {d: round(100 * v[d], 4) for d in SL} for k, v in LB.items()}
    unt = {d: sum(st_[d]["unt"].values()) for d in SL}
    plat_ = {d: sum(st_[d]["all"].values()) for d in SL}
    L_.check("source tables tie to the click tables (own-page clicks and untested own-page clicks per desk)",
             all(plat_[d] == c[d]["plat"] and unt[d] == c[d]["plat"] - c[d]["t_plat"] for d in SL))
    share_g = {d: new_share(st_[d]["unt"], d, rates, desks) for d in SL}
    rungs = {
        0: {d: LB["dash"][d] * c[d]["total"] for d in SL},
        1: {d: LB["raw"][d] * c[d]["total"] for d in SL},
        2: {d: LB["shr"][d] * c[d]["total"] for d in SL},
        3: {d: LB["shr"][d] * plat_[d] for d in SL},
        4: {d: LB["shr"][d] * unt[d] for d in SL},
        5: {d: LB["shr"][d] * unt[d] * avg_kept for d in SL},
        6: {d: LB["shr"][d] * unt[d] * share_g[d] for d in SL},
    }
    want = {0: "POL-N", 1: "SPT-M", 2: BUS, 3: "LOC-M", 4: CUL, 5: CUL, 6: BUS}
    floor_ = {0: 1.2, 1: 1.2, 2: 1.2, 3: 1.2, 4: 1.45, 5: 1.45, 6: 1.2}
    for k, vals in rungs.items():
        o = rank(vals)
        margin = vals[o[0]] / vals[o[1]]
        L_.check("rung %d leader %s" % (k, want[k]), o[0] == want[k], "leader %s" % o[0])
        L_.check("rung %d margin at least %.2f" % (k, floor_[k]), margin >= floor_[k], "%.3f" % margin)
        rec.setdefault("rungs", {})[k] = dict(order=[(d, round(vals[d])) for d in o], margin=round(margin, 4))
    r6 = rungs[6]
    o6 = rank(r6)
    CALL, RUN = o6[0], o6[1]
    gap = r6[CALL] - r6[RUN]
    L_.check("call: Business·national, runner-up Local·metro", (CALL, RUN) == (BUS, "LOC-M"), "%s %s" % (CALL, RUN))
    L_.check("runner-up at least 1.15x over the third desk", r6[o6[1]] / r6[o6[2]] >= 1.15, "%.3f" % (r6[o6[1]] / r6[o6[2]]))
    L_.check("rungs 4 and 5 name the same desk (one share for every desk reorders nothing)", rank(rungs[4]) == rank(rungs[5]))
    L_.check("the decisive step moves the call: rung 5 names Culture·national, rung 6 Business·national",
             rank(rungs[5])[0] == CUL and CALL == BUS)
    pos = {k: rank(rungs[k]).index(BUS) + 1 for k in rungs}
    rec["business_rank"] = pos
    L_.check("position: Business·national third behind Culture·national on rungs 4 and 5 (the strong analyst's two "
             "stops)", pos[4] == 3 and pos[5] == 3, str(pos))
    L_.check("position: where Business·national leads below rung 6 (rung 2, every click on the plan) its figure is more "
             "than ten times the answer's, another bin and another runner-up",
             rungs[2][BUS] > 10 * r6[BUS] and rank(rungs[2])[1] != RUN, "%.0f" % rungs[2][BUS])
    for rival in (CUL, "LOC-M"):
        carried = rungs[4][rival] / rungs[4][BUS]
        edge = share_g[BUS] / share_g[rival]
        L_.check("dominance against %s at least 1.2 (edge on the share new to Bightline over the lead carried in)" % rival,
                 edge / carried >= 1.2, "edge %.3f carried %.3f ratio %.3f" % (edge, carried, edge / carried))
        rec.setdefault("dominance", {})[rival] = dict(edge=round(edge, 3), carried=round(carried, 3), ratio=round(edge / carried, 3))
    rec["share_new"] = {d: round(share_g[d], 4) for d in SL}
    L_.check("SF10 rounding: the call figure at least 15,000 inside its 50,000 bin, so rounding once at the end or the "
             "lift and the click-throughs first files the same figure", bin_margin(r6[CALL]) >= 15_000, "%.0f" % r6[CALL])
    L_.check("runner-up figure at least 15,000 inside its bin", bin_margin(r6[RUN]) >= 15_000, "%.0f" % r6[RUN])
    L_.check("gap at least 15,000 inside its bin, rounded before or after subtracting the same",
             bin_margin(gap) >= 15_000 and bin_round(gap) == bin_round(r6[CALL]) - bin_round(r6[RUN]), "%.0f" % gap)
    rec["call"] = dict(desk=CALL, figure=round(r6[CALL]), runner_up=RUN, runner_figure=round(r6[RUN]), gap=round(gap),
                       bins=(bin_round(r6[CALL]), bin_round(r6[RUN]), bin_round(gap)))
    rec["rung5_culture"] = (round(rungs[5][CUL]), bin_round(rungs[5][CUL]))

    # ----- the grid: lift basis x what the squad nets out x the share of a won click counted as new, cell by cell
    won_ids = set(tests.loc[tests["won"], "article_id"])
    own_ = sp[sp["source_code"].isin(PLATFORM)]
    wonc = own_[own_["article_id"].isin(won_ids)].groupby(["desk_code", "source_code"])["pageviews"].sum()

    def base_of(d, n):
        a_ = st_[d]["all"]
        if n == "none":
            return dict(a_)
        if n == "click":
            return dict(st_[d]["unt"])
        if n == "count":
            f_ = 1 - c[d]["n_tested"] / c[d]["n_art"]
            return {s: a_[s] * f_ for s in a_}
        return {s: a_[s] - int(wonc.get((d, s), 0)) for s in a_}

    PASS = {
        "none": lambda d, b: 1.0,
        "embeddings' average": lambda d, b: avg_kept,
        "site click-through": lambda d, b: 1 - site_rate,
        "app pages' click-through": lambda d, b: 1 - app_rate,
        "home feed's click-through": lambda d, b: 1 - rates["Home feed"],
        "page by page (year)": lambda d, b: new_share(b, d, rates, desks),
        "page by page (monthly mean)": lambda d, b: new_share(b, d, rates_m, desks),
        "page by page (monthly median)": lambda d, b: new_share(b, d, rates_md, desks),
        "one factor per kind of page": lambda d, b: sum(b[s] * FAC[s] for s in b) / sum(b.values()),
    }
    grid = {}
    for lb in ("dash", "raw", "shr", "pool"):
        for n in ("none", "click", "count", "won"):
            for pn, fn in PASS.items():
                vals = {}
                for d in SL:
                    b_ = base_of(d, n)
                    vals[d] = LB[lb][d] * sum(b_.values()) * fn(d, b_)
                o = rank(vals)
                grid[(lb, n, pn)] = dict(lead=o[0], fig=vals[o[0]], run=o[1], gap=vals[o[0]] - vals[o[1]], vals=vals,
                                         graded=(o[0], bin_round(vals[o[0]]), o[1], bin_round(vals[o[0]] - vals[o[1]])))
    gold_graded = (BUS, bin_round(r6[BUS]), "LOC-M", bin_round(gap))
    conv = [k for k, v in grid.items() if v["graded"] == gold_graded]
    want_conv = {(lb, "click", pn) for lb in ("shr", "pool") for pn in ("page by page (year)", "page by page (monthly mean)",
                                                                       "page by page (monthly median)",
                                                                       "one factor per kind of page")}
    rec["grid_leaders"] = {"/".join(k): (v["lead"], round(v["fig"]), v["run"]) for k, v in grid.items()}
    L_.check("grid: %d cells computed" % len(grid), len(grid) == 4 * 4 * len(PASS))
    L_.check("grid: exactly the page-by-page cells (each page's own rate, or one factor per kind of page fitted on the "
             "embeddings) on the shrunk or vertical-pooled lift with every tested headline netted reproduce the call, "
             "its figure, the runner-up and the gap",
             set(conv) == want_conv, str(sorted(set(conv) ^ want_conv)))
    L_.check("grid: the golden cell is the shrunk lift, every tested headline netted, page by page",
             grid[("shr", "click", "page by page (year)")]["graded"] == gold_graded)
    bus_cells = [k for k, v in grid.items() if v["lead"] == BUS and k not in want_conv]
    rec["business_elsewhere"] = {"/".join(k): (round(grid[k]["fig"]), grid[k]["run"], round(grid[k]["gap"])) for k in bus_cells}
    L_.check("grid: every other cell that names Business·national files another figure bin, another runner-up or "
             "another gap bin", all(grid[k]["graded"] != gold_graded for k in bus_cells))
    for k, v in (((("shr", "click", "embeddings' average")), CUL), (("shr", "click", "none"), CUL),
                 (("shr", "none", "page by page (year)"), "LOC-M"), (("shr", "won", "page by page (year)"), None),
                 (("shr", "count", "page by page (year)"), None), (("raw", "click", "page by page (year)"), None),
                 (("shr", "click", "site click-through"), CUL), (("shr", "click", "home feed's click-through"), CUL)):
            g_ = grid[k]
            if v is not None:
                L_.check("partial correction %s names %s" % ("/".join(k), v), g_["lead"] == v, g_["lead"])
            L_.check("partial correction %s misses the graded call" % "/".join(k), g_["graded"] != gold_graded,
                     str(g_["graded"]))
    fk = grid[("shr", "click", "one factor per kind of page")]
    rec["page_kind_route"] = dict(lead=fk["lead"], fig=round(fk["fig"]), run=fk["run"], gap=round(fk["gap"]))
    L_.check("the page-kind route converges: the same call, figure bin, runner-up and gap bin, its gap at least "
             "10,000 inside the bin", fk["graded"] == gold_graded and bin_margin(fk["gap"]) >= 10_000, str(fk["graded"]))

    # admissible variants: each lands the call, its figure, the runner-up and the gap in the golden bins
    variants = {}
    t_dl = test_table(D["arch"], pk, pr_dl)
    l_dl = t_dl[t_dl.engine == "web"].groupby("desk_code")["shr"].mean()
    variants["DerSimonian-Laird prior"] = {d: l_dl[d] * unt[d] * share_g[d] for d in SL}
    variants["lifts rounded to two decimals"] = {d: round(100 * LB["shr"][d], 2) / 100 * unt[d] * share_g[d] for d in SL}
    variants["click-throughs rounded to a whole per cent"] = {
        d: LB["shr"][d] * new_share(st_[d]["unt"], d, {k_: round(v, 2) for k_, v in rates.items()}, desks) * unt[d] for d in SL}
    own_ids = set(tt.loc[tt["team_code"].isin(SL), "article_id"])
    unt_own = own_[~own_["article_id"].isin(own_ids)].groupby(["desk_code", "source_code"])["pageviews"].sum()
    variants["netting on tests owned by the desk's own staff"] = {
        d: LB["shr"][d] * sum(int(unt_own.get((d, s), 0)) * (1 - rates[page_name(desks, d, s)]) for s in P.SOURCES_PLATFORM)
        for d in SL}
    old7 = own_[own_["age_band"].eq("7d+") & ~own_["article_id"].isin(set(tests["article_id"]))]
    old7 = old7.groupby(["desk_code", "source_code"])["pageviews"].sum()
    variants["own-page clicks at 7 days and older left out"] = {
        d: LB["shr"][d] * sum((st_[d]["unt"][s] - int(old7.get((d, s), 0))) * (1 - rates[page_name(desks, d, s)])
                              for s in P.SOURCES_PLATFORM) for d in SL}
    for name, v in variants.items():
        o = rank(v)
        same = (o[0], bin_round(v[o[0]]), o[1], bin_round(v[o[0]] - v[o[1]])) == gold_graded
        L_.check("admissible variant lands the call, its figure, the runner-up and the gap in the golden bins: %s" % name,
                 same, " ".join("%s %.0f" % (P.SHORT[d], v[d]) for d in SL))

    # ----- the semantic fork table (DESIGN_NOTE.md)
    brief_ = re.sub(r"\s+", " ", T[F["charter"]])
    pol_ = re.sub(r"\s+", " ", T[F["policy"]])
    flat_ = lambda z: re.sub(r"[^a-z]", "", z.lower())     # noqa: E731
    dname = dict(zip(D["desks"]["desk_code"], D["desks"]["desk_name"]))
    L_.check("SF1 shortlist: the brief's 2027 shortlist names the six desks the prompt names",
             all(flat_(dname[d]) in flat_(brief_) for d in SL), str([dname[d] for d in SL]))
    L_.check("SF2 window: the brief moves the squad to one desk each January for the calendar year",
             "Each January it moves to one desk for the calendar year" in brief_)
    L_.check("SF3 extra clicks: the brief judges the squad on the clicks readers make in its year that they would not "
             "have made without it, against a reader holdback, so the figure is Bightline's and not one headline's",
             "on the article clicks Bightline's readers make in its year that they would not have made without it, "
             "measured against a reader holdback" in brief_)
    L_.check("SF4 owning desk: every article carries one desk code on every spine row (C1)",
             int(D["spine"].groupby("article_id")["desk_code"].nunique().max()) == 1)
    post_ = own_[~own_["article_id"].isin(set(tests["article_id"])) & own_["age_band"].ne("0-2h")]
    post_ = post_.groupby(["desk_code", "source_code"])["pageviews"].sum()
    r6_post = {d: LB["shr"][d] * sum(int(post_.get((d, s), 0)) * (1 - rates[page_name(desks, d, s)])
                                     for s in P.SOURCES_PLATFORM) for d in SL}
    rec["post_test_reading"] = {P.SHORT[d]: round(r6_post[d]) for d in SL}
    L_.check("SF5 counting period: the brief counts clicks from each article's publication, its test hours included; "
             "the post-test reading moves the call figure out of its bin",
             "Clicks count from each article's publication, the hours its headline is under test included" in brief_
             and bin_round(r6_post[BUS]) != bin_round(r6[BUS]), str(rec["post_test_reading"]))
    L_.check("SF6 2027 base: the brief holds every desk at its base-year clicks and the plan's 2027 clicks equal them (C1)",
             "holds every desk at its clicks in the twelve months to September 2026" in brief_
             and all(int(plan.loc[d, "plan_2027_clicks"]) == int(plan.loc[d, "clicks_oct25_sep26"]) for d in SL))
    disc = own_.groupby("desk_code")["pageviews"].sum()
    sp_d = sp[sp["source_code"].eq("discover") & ~sp["article_id"].isin(set(tests["article_id"]))]
    disc_unt = sp_d.groupby("desk_code")["pageviews"].sum()
    r6_disc = {d: r6[d] + LB["shr"][d] * float(disc_unt.get(d, 0)) for d in SL}
    rec["discover_reading"] = {P.SHORT[d]: round(r6_disc[d]) for d in SL}
    L_.check("SF7 surfaces: the brief names the pages a shipped headline replaces the old one on and the surfaces that "
             "keep the stored headline, Discover-style cards among them; counting Discover as a Bightline page moves "
             "the call figure out of its bin",
             "the home pages, the section fronts, the app home feed and tabs, and the related-story links on article "
             "pages" in brief_ and "Search results, Discover-style cards, partner apps, social link cards, newsletters "
             "and alerts keep the headline stored at publication" in brief_
             and bin_round(r6_disc[BUS]) != bin_round(r6[BUS]), str(rec["discover_reading"]))
    L_.check("SF8 winning lift: the brief defines it as the shipped headline's click-through over the control's, minus "
             "one, and nil where the control is kept",
             "the shipped headline's click-through over the control's, minus one, and nil where the control is kept" in brief_)
    L_.check("SF9 runner-up and gap: rounding before or after subtracting files the same gap",
             bin_round(r6[CALL]) - bin_round(r6[RUN]) == bin_round(gap))
    a_ = D["arch"].copy()
    mix_ = a_.groupby("test_id").apply(lambda g: g["clicks"].sum() / g["impressions"].sum())
    a_["ctr"] = a_["clicks"] / a_["impressions"]
    ctl_ = a_[a_["variant"] == "control"].set_index("test_id")["ctr"]
    shp_ = pk[pk["shipped"] == "Y"].set_index("test_id")
    short_ = (shp_["L"] - (mix_ / ctl_ - 1.0).reindex(shp_.index)).dropna()
    L_.check("SF11 the rate during the test hours: the brief counts those clicks at the winning headline's lift, and "
             "the realised impression-weighted rate across every package shown is lower at every shipped test",
             "Clicks in those hours count at the winning headline's lift" in brief_ and len(short_) > 0
             and bool((short_ > 0).all()), "%d tests" % len(short_))
    L_.check("SF12 going live: the corrections standard times a correction from when the article was first published, "
             "by a live save or, for a scheduled article, when the CMS published it at its scheduled time",
             "Time to correction runs from when the article went live: when it was first published, by a live save or, "
             "for a scheduled article, when the CMS published it at its scheduled time" in pol_)
    cms_hdr = list(D["cms"].columns)
    L_.check("SF13 clocks: the CMS export names Brisbane time on the scheduled time's own column and every save time "
             "ends in Z (UTC)", "publish_at_aest" in cms_hdr
             and D["cms"]["saved_at"].str.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\dZ").all())
    L_.check("SF14 what tested covers: the brief has the squad take the headlines a desk has not put under test and the "
             "archive record every headline put under test whether or not a variant ships; netting only the tests "
             "that shipped a winner misses the call",
             "It takes the headlines the desk has not put under test itself" in brief_
             and "whether or not a variant ships" in brief_
             and grid[("shr", "won", "page by page (year)")]["graded"] != gold_graded)
    L_.check("SF15 page click-through: the twelve months summed, the mean of the monthly rates and their median file "
             "the same call, figure, runner-up and gap",
             all(grid[("shr", "click", p_)]["graded"] == gold_graded
                 for p_ in ("page by page (year)", "page by page (monthly mean)", "page by page (monthly median)")))
    L_.check("SF16 which home page: a desk's home-page clicks on its edition's home page tie to that page's article "
             "click-throughs to the click (asserted above), so no desk's clicks belong to the other edition's home page",
             all(yr[k_] == v for k_, v in tie.items()))

    # ----- characters and the dashboard
    sq = st[(st["team_code"] == "AUD-HS") & st["end_date"].isna()]
    L_.check("the brief's squad of six (lead, three headline editors, a producer, a data analyst) is the staff list's "
             "current squad", sorted(sq["role"]) == sorted(["Headline squad lead", "Headline editor", "Headline editor",
                                                             "Headline editor", "Producer", "Data analyst"]),
             str(sorted(sq["role"])))
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

    # ----- the ask layer: the corrections cuts (the CMS); the panel's readers are a declared distractor, and its
    # Layer 1 (two taxonomies, a history rerun, a restatement, the July file) is asserted below as the pack carries it
    cms = cms_frames(D)
    rows = cms_rows_of(cms)
    GA = asks_mod.read_corrections(rows)
    G = desk_view(GA)
    arts = {d: G[d]["articles"] for d in P.WEB}
    L_.check("CMS articles equal the spine's articles published in the window, desk by desk",
             all(arts[d] == c[d]["n_art_win"] for d in P.WEB), str({P.SHORT[d]: (arts[d], c[d]["n_art_win"]) for d in P.WEB}))
    MODES = ("golden", "per_period", "per_site", "per_code", "careful", "lazy", "nohist", "first", "norestate",
             "national", "issue_date", "convention")
    PR = {m: panel_readers(D, m) for m in MODES}
    PRE = {m: panel_readers(D, m, echo=True) for m in MODES}     # the July file's April to June rows kept
    readers = {d: v[0] for d, v in PR["golden"].items()}
    L_.check("readers: every desk's average runs over twelve months of record",
             all(v[1] == 12 for v in PR["golden"].values()))
    L_.check("readers: counting each monthly release only for the month its name follows (and the two "
             "reruns for the months their notes name) converges on the golden at every desk",
             all(PR["convention"][d] == PR["golden"][d] for d in P.WEB))
    asks = {}
    for d in SL:
        asks[d] = dict(median=G[d]["median"], hour=G[d]["hour"],
                       three=G[d]["three"], corrected=G[d]["corrected"])
    rec["asks"] = {d: dict(median=int(asks[d]["median"]), hour=asks[d]["hour"], three=asks[d]["three"],
                           corrected=asks[d]["corrected"]) for d in SL}
    for d in SL:
        x = asks[d]
        L_.check("SF18 %s corrected-article count odd, so the median is one article's whole minutes" % d,
                 x["corrected"] % 2 == 1 and float(x["median"]).is_integer(), str(x["corrected"]))
        L_.check("SF17 %s: no first headline correction within two minutes of the hour or of three hours, so within "
                 "and more than read one way" % d,
                 not any(HOUR - 2 <= m <= HOUR + 2 or THREE - 2 <= m <= THREE + 2 for m in G[d]["mins"]))
    L_.check("corrections cuts: no desk's count within the hour or after three hours is nil, and the two counts differ "
             "across desks (no constant response files more than two desks' counts)",
             all(asks[d]["hour"] > 0 for d in SL) and max(sum(asks[d]["hour"] == v for d in SL) for v in range(50)) <= 2
             and max(sum(asks[d]["three"] == v for d in SL) for v in range(50)) <= 2,
             str({P.SHORT[d]: (asks[d]["hour"], asks[d]["three"]) for d in SL}))

    def k1(v):
        return int(np.floor(v / 1000 + 0.5))

    # every corrections reading, figure by figure
    views = {name: ask_corrections(rows, **kw) for name, kw in READ.items()}
    rec["corrections_readings"] = {}
    for name, v in views.items():
        off = sum(cuts_off(v, G, d) for d in SL)
        rec["corrections_readings"][name] = dict(off=off, cuts={P.SHORT[d]: cuts(v, d) for d in SL})
        L_.check("reading files no correction at minute 0 or earlier: %s" % name,
                 all(min(v[d]["mins"]) >= 1 for d in P.WEB if v[d]["mins"]))
        L_.check("reading counts the same articles as the spine (the article check passes on it): %s" % name,
                 all(v[d]["articles"] == c[d]["n_art_win"] for d in P.WEB))
    off_auto = rec["corrections_readings"][AUTO]["off"]
    L_.check("SF19 an autosave publishes nothing, filed in the corrections standard 7.3, and the export types every "
             "such save autosave; the status column read alone files at least 12 of the 18 cuts away from the golden",
             off_auto >= 12 and "An autosave of an editor's working copy publishes nothing" in pol_
             and set(cms["save_type"]) == {"save", "autosave"}, str(off_auto))
    off_sched = rec["corrections_readings"][SCHED]["off"]
    L_.check("SF20 the silent device: a scheduled time read as going live whenever it precedes the first live save, a "
             "schedule set back to draft before its time taken as fired, files all 18 cuts away from the golden",
             off_sched == 18, str(rec["corrections_readings"][SCHED]["cuts"]))
    for name in (R1, R3, R5):
        L_.check("the earlier rounds' paths each file at least 12 of the 18 cuts away from the golden: %s" % name,
                 rec["corrections_readings"][name]["off"] >= 12, str(rec["corrections_readings"][name]["off"]))
    # necessity matrix: each device or hazard alone mishandled, everything else read the golden way
    dev_ = {
        "a schedule set back to draft before its time read as fired (the last scheduled time taken whenever it "
        "precedes the first live save)": (dict(sched_blind=True), 18),
        "the earliest scheduled time set taken as going live": (dict(sched_min=True), 18),
        "any draft saved after scheduling read as a schedule that never fired (the over-repair)": (dict(sched_drafted=True), 3),
        "an autosave of a live article taken as published (status read alone)": (dict(autosaves=True), 12),
        "a note before its headline fix read on its own save": (dict(lead=False), 6),
        "a note put back after a save that left it off read as a new correction": (dict(readd=False), 6),
        "a note on the save after its headline fix read on its own save": (dict(lag=False), 6),
        "scheduled articles live at their first live save": (dict(scheduled=False), 6),
        "every scheduled article live at its scheduled time (hand-published ones too)": (dict(scheduled_always=True), 3),
        "entries ignored": (dict(entries=False), 6),
        "every new note a headline correction": (dict(s2=False), 6),
        "a headline correction known by its note's wording": (dict(by_text=("headline", "title", "heading")), 6),
        "restored copies as their own documents": (dict(merge=False), 1),
        "publish times read on the saves' clock": (dict(clock="UTC"), 6),
    }
    for name, (kw, need) in dev_.items():
        v = ask_corrections(rows, **kw)
        off = sum(cuts_off(v, G, d) for d in SL)
        rec.setdefault("necessity", {})[name] = off
        L_.check("necessity: %s moves %d or more of the 18 cuts" % (name, need), off >= need, str(off))
    # the convergences the standards' sentences rely on
    for N in (9, 10, 15, 20, 30, 45, 60):
        v = ask_corrections(rows, lag_struct=N)
        L_.check("note pairing converges: a note on an unchanged headline paired with the headline change up to %d "
                 "minutes before it, else after it, files the golden cuts at every desk" % N,
                 all(cuts(v, d) == cuts(G, d) for d in P.WEB))
    for tol in (9, 10, 15, 20, 30, 45, 60):
        v = ask_corrections(rows, entry_tol=tol)
        L_.check("entry pairing converges: a %d-minute window files the golden cuts at every desk" % tol,
                 all(cuts(v, d) == cuts(G, d) for d in P.WEB))
    v = ask_corrections(rows, lag_struct=10, entry_tol=10, entry_after=10)
    L_.check("the standards' ten minutes read literally (a new note paired with a headline change on its own save or on "
             "a save up to ten minutes either side, an entry's included, whatever the note says) files the golden cuts",
             all(cuts(v, d) == cuts(G, d) for d in P.WEB))
    v = ask_corrections(rows, lag_struct=10 ** 6, entry_tol=10, entry_after=10)
    L_.check("the standards' ten minutes are load-bearing: a note paired with a headline change at any distance moves "
             "the cuts at three or more desks", sum(cuts(v, d) != cuts(G, d) for d in SL) >= 3)
    v = ask_corrections(rows, lag_struct=10, entry_tol=10, entry_after=10, readd=False)
    L_.check("the standards' put-back sentence is load-bearing: the pairing read literally with a note put back taken "
             "as new moves the cuts at three or more desks", sum(cuts(v, d) != cuts(G, d) for d in SL) >= 3)

    # the readers stops, with the July file's April to June rows kept and set aside
    pnames = {"golden": "the July file's April to June rows kept as the latest release (the natural path)",
              "per_period": "the rows of the latest release carrying each month",
              "per_site": "the rows of the latest release carrying each month and site",
              "per_code": "the latest release per month and section code, codes read on each release's own list",
              "careful": "latest release per code, codes read through the section history by period",
              "lazy": "latest release per code, read on the current section list",
              "nohist": "the history release left out",
              "first": "first release per code, read by period",
              "norestate": "the restated release left out",
              "national": "national site for Sport-metro",
              "issue_date": "each release read on the list in force on its issue date"}
    combo_in = []
    for m, name in pnames.items():
        r_ = {d: PRE[m][d][0] for d in SL}
        combo_in += [(name, "readers", P.SHORT[d]) for d in SL if k1(r_[d]) == k1(readers[d])]
    L_.check("readers: with the July file's April to June rows kept, every way of reading the releases lands the "
             "figure off the golden bin at every desk", not combo_in, str(combo_in[:6]))
    nat = {d: PRE["golden"][d] for d in SL}
    lo_r = {d: nat[d][0] / readers[d] - 1 for d in SL}
    rec["natural_readers"] = {P.SHORT[d]: (int(round(nat[d][0], -3)), round(100 * lo_r[d], 2)) for d in SL}
    L_.check("the July hazard on the readers path: the July file's rows taken as the latest release, the release "
             "log's months unread, file every desk's readers 1.0 to 3.0 per cent low, twelve months each",
             all(-0.03 <= lo_r[d] <= -0.01 and nat[d][1] == 12 for d in SL), str(rec["natural_readers"]))
    D_whole = dict(D)
    D_whole["panel"] = D["panel"][D["panel"]["release"] != P.ECHO_RELEASE]
    whole = panel_readers(D_whole)
    stop_reach = {}
    for m, name in list(pnames.items()) + [("whole", "the July release set aside whole, its own month included")]:
        if m == "golden":
            continue
        src = whole if m == "whole" else PR[m]
        stop_reach[m] = {d for d in SL if k1(src[d][0]) != k1(readers[d])}
    rec["stop_reach"] = {m: sorted(P.SHORT[d] for d in v) for m, v in stop_reach.items()}
    L_.check("readers: the July release set aside whole, the first release per code, the restatement left "
             "out and the current section list each land the figure off the golden bin at every desk; the history "
             "release left out at Politics·national and Culture·national; the national site at Sport·metro",
             all(stop_reach[m] == set(SL) for m in ("whole", "first", "norestate", "lazy"))
             and stop_reach["nohist"] >= {"POL-N", "CUL-N"} and stop_reach["national"] >= {"SPT-M"},
             str(rec["stop_reach"]))
    p_ = D["panel"]
    rlog_ = D["rel"]
    july = p_[(p_.release == P.ECHO_RELEASE) & (p_.period != "2026-07")]
    firsts = p_[p_.release.isin(["R26-05", "R26-06", "R26-07"])]
    same = july.merge(firsts, on=["period", "site_code", "section_code"], suffixes=("", "_f"))
    jl = rlog_[rlog_.release == P.ECHO_RELEASE].iloc[0]
    L_.check("July hazard: the July release's file carries April to June for both sites as first published, and the "
             "release log gives the July release July alone, so its months set exactly these 27 rows aside",
             len(july) == 27 and len(same) == 27 and (same.unique_audience == same.unique_audience_f).all()
             and (same.visits == same.visits_f).all()
             and list(rlog_.columns) == ["release", "published_on", "first_month", "last_month", "note"]
             and (jl.first_month, jl.last_month, jl.note) == ("2026-07", "2026-07", "")
             and list(p_.columns) == ["release", "period", "site_code", "section_code", "unique_audience", "visits"]
             and sorted(echo_rows(D)) == sorted(july.index), "%d rows" % len(july))

    # the autosaves as shipped (a hazard, filed in the standard): status live, save type autosave, never published
    auto_rows = cms[cms.save_type == "autosave"]
    L_.check("autosaves: every autosave row is a live article's, saved after it went live, and carries status live",
             (auto_rows.status == "live").all() and (auto_rows.doc_type != "post").all()
             and (auto_rows.migrated_from == "").all() and (auto_rows.restored_from_doc == "").all())
    arts_docs = cms[(cms.doc_type != "post") & (cms.migrated_from == "") & (cms.restored_from_doc == "")]
    with_auto = auto_rows.groupby("desk_code")["doc_id"].nunique() / arts_docs.drop_duplicates("doc_id").groupby("desk_code").size()
    L_.check("autosaves: at least 12 per cent of articles at every web desk carry one (benign ones far outnumber the "
             "ones saved just ahead of a headline correction)", (with_auto.reindex(P.WEB) >= 0.12).all(),
             str(with_auto.round(3).to_dict()))
    h_times = {(k, t_) for k, a in GA.items() for t_ in a["heads"]}
    ahead = sum(any((r["doc_id"], r["t"] + pd.Timedelta(minutes=m)) in h_times for m in range(1, 7))
                for _, r in auto_rows.iterrows())
    L_.check("autosaves: those saved just ahead of a headline correction are under a quarter of all autosaves",
             ahead / len(auto_rows) < 0.25, "%d of %d" % (ahead, len(auto_rows)))
    # the schedules set back to draft as shipped: the device rows on corrected stories, the benign ones on stories
    # never corrected, and the twins set again that the CMS published at the time set second
    by_doc = {k: g_.sort_values("revision") for k, g_ in cms.groupby("doc_id")}
    went_draft = [k for k, g_ in by_doc.items() if "live" in list(g_.status)
                  and "draft" in list(g_.status)[list(g_.status).index("live"):]]
    L_.check("no document is saved as a draft once it has gone live (a live article is withdrawn, never set back to "
             "draft), so a draft saved after a scheduled time means the CMS never published the article then",
             not went_draft, str(went_draft[:3]))
    aest_ = pd.Timedelta(hours=10)
    dev_ok, dev_n, base_n, twin_ok, twin_n = True, {}, {}, True, 0
    for d in P.WEB:
        tr = W.cms_truth[d]
        dev_n[d] = sum(i in tr["hc_first"] for i in tr["cancel"])
        base_n[d] = len(tr["cancel"]) - dev_n[d]
        for i, (was, c_t, r_t) in tr["cancel"].items():
            g_ = by_doc[asks_mod.doc_id("doc", d, i)]
            pre = g_[g_.status != "live"]
            first_live = g_[g_.status == "live"]["t"].min()
            sch_ = pre[pre.status == "scheduled"]
            was_t = pd.Timestamp(was)
            upto = pre[pre["t"] <= was_t]
            dev_ok &= (len(sch_) == 1 and pd.Timestamp(sch_.publish_at_aest.iloc[0]) - aest_ == was_t
                       and upto.status.iloc[-1] == "draft" and upto.publish_at_aest.iloc[-1] == ""
                       and ((pre["t"] > was_t) & (pre.status == "draft")).any() and first_live > was_t
                       and (first_live + aest_).date() == (was_t + aest_).date())
        for i in tr["resched"]:
            g_ = by_doc[asks_mod.doc_id("doc", d, i)]
            pre = g_[g_.status != "live"]
            sch_ = pre[pre.status == "scheduled"]
            twin_n += 1
            twin_ok &= (len(sch_) == 2 and list(pre.status)[-1] == "scheduled"
                        and (pre[(pre["t"] > sch_["t"].iloc[0]) & (pre["t"] < sch_["t"].iloc[1])].status == "draft").any()
                        and pd.Timestamp(sch_.publish_at_aest.iloc[0]) - aest_ < sch_["t"].iloc[1]
                        and g_[g_.status == "live"]["t"].min() > pd.Timestamp(sch_.publish_at_aest.iloc[1]) - aest_)
    L_.check("schedules set back to draft: on each, the save at or before the time first set is a draft with no "
             "scheduled time, a draft is saved after that time, and an editor publishes the article by hand later the "
             "same Brisbane day; two corrected stories a desk carry one and the stories never corrected carry at least "
             "twenty times as many", dev_ok and all(dev_n[d] == 2 for d in P.WEB)
             and all(base_n[d] >= 20 * dev_n[d] for d in P.WEB), str({P.SHORT[d]: (dev_n[d], base_n[d]) for d in P.WEB}))
    L_.check("schedules set back to draft and set again (benign twins, one corrected story a desk among them): the "
             "time first set passed while the article was a draft and the CMS published it at the time set second, "
             "before any live save", twin_ok and twin_n >= 100, str(twin_n))
    sp_ = D["spine"].drop_duplicates("article_id")
    sp_days = sp_.groupby(["desk_code", "published_date"]).size()

    def cms_days(A_):
        return pd.Series([(a["desk"], (pd.Timestamp(a["go"]) + aest_).date()) for a in A_.values()]).value_counts()
    days_g = cms_days(GA)
    days_s = cms_days(asks_mod.read_corrections(rows, **READ[SCHED]))
    sp_d = {(dk, pd.Timestamp(dd).date()): int(v) for (dk, dd), v in sp_days.items() if dk in P.WEB}
    L_.check("the spine's articles by desk and Brisbane publication date equal the CMS's under the golden reading and "
             "under a scheduled time read as going live whatever came after it (the spine settles nothing)",
             all(sp_d.get(k_, 0) == int(v) for k_, v in days_g.items()) and days_g.to_dict() == days_s.to_dict()
             and sum(days_g) == sum(v for (dk, dd), v in sp_d.items()
                                    if P.WINDOW_START <= dd <= P.WINDOW_END), "%d days" % len(days_g))
    L_.check("battery on the CMS: (doc_id, revision) unique, every parent and restored source resolves, a scheduled "
             "time on every scheduled revision and on no other",
             not cms.duplicated(["doc_id", "revision"]).any()
             and set(cms.loc[cms.parent_doc != "", "parent_doc"]) <= set(cms["doc_id"])
             and set(cms.loc[cms.restored_from_doc != "", "restored_from_doc"]) <= set(cms["doc_id"])
             and ((cms.status == "scheduled") == (cms.publish_at_aest != "")).all())

    # the referee: the bulletin's March figures reproduce, and the earlier rounds' paths tie to them too
    btxt = T[F["bulletin"]]
    m = re.search(r"logged (\d+) headline corrections and (\d+) corrections to article text", btxt)
    lo, hi = pd.Timestamp("2026-03-01") - pd.Timedelta(hours=10), pd.Timestamp("2026-04-01") - pd.Timedelta(hours=10)

    def march(A_):
        return (sum(lo <= t_ < hi for a in A_.values() for t_ in a["heads"]),
                sum(lo <= t_ < hi for a in A_.values() for t_ in a["texts"]))
    gm = march(GA)
    L_.check("referee: the bulletin's March headline and text counts reproduce from the CMS export",
             m and (int(m.group(1)), int(m.group(2))) == gm, "%s vs %s" % (m.groups() if m else None, gm))
    for nm_, kw in (("round-1", READ[R1]), ("round-3", READ[R3]), ("status alone", READ[AUTO]),
                    ("scheduled time whatever came after it", READ[SCHED])):
        L_.check("referee: the %s path ties to the bulletin's March figures as well (the bulletin settles nothing)" % nm_,
                 march(asks_mod.read_corrections(rows, **kw)) == gm)

    # ----- pair simulation: the cracker lands the call, runs the battery and executes every filed rule; the mirror
    # stops at rung 5 (Culture·national). The asks never read a main-path file, so both file the same ask figures.
    readings = {
        "cracker path (every filed rule executed, a scheduled time read as going live whatever came after it)": views[SCHED],
        "catches the schedules set back to draft": G,
    }
    pair = pair_simulation(asks, readings, G)
    rec["pair"] = pair
    xc = pair["cracker path (every filed rule executed, a scheduled time read as going live whatever came after it)"]
    L_.check("cracker sheet: the response that lands the call, runs the battery and executes every filed rule keeps at "
             "most 3 of the 18 ask figures, and the mirror files the same figures", xc["hits"] <= 3, str(xc))
    L_.check("pair ceiling: cracker and mirror average at or under 40 on the planning weights", xc["pair"] <= 40,
             "%.1f" % xc["pair"])
    full = golden_figures(target)
    main_files = {F[k] for k in ("spine", "archive", "staff", "plan", "changelog", "charter", "desks", "dashboard", "pages")}
    nomain = without(target, main_files)
    try:
        dec = golden_figures(nomain, part="cms")["corrections"] == full["corrections"]
    except Exception:
        dec = False
    L_.check("separation: every ask figure recomputes with every main-path file deleted", dec)
    L_.check("golden_figures reproduces the call from the pack", full["call"] == (CALL, bin_round(r6[CALL]), RUN, bin_round(gap)),
             str(full["call"]))

    # ----- separation, single statements, vocabulary, dates, gates
    main_docs = [F["charter"], F["desks"], F["plan"], F["changelog"], F["staff"], F["pages"]]
    pat = re.compile(r"\b(revisions?|corrections?|posts?|restor\w*|panel|restat\w*|section codes?|autosav\w*|"
                     r"schedul\w*|taxonom\w*|live[- ]blog entr\w*)\b", re.I)
    hits_v = {f: pat.findall(T[f]) for f in main_docs}
    L_.check("separation: no main-path document carries the ask devices' vocabulary", not any(hits_v.values()),
             str({k: v[:3] for k, v in hits_v.items() if v}))
    L_.check("separation: zero CMS or panel rows in main-path files (different keys entirely)",
             not set(D["spine"]["article_id"].astype(str)) & set(cms["doc_id"]))
    single = {
        "the squad's measure": "judged the way Experimentation closes each embedding",
        "the surfaces": "keep the headline stored at publication",
        "the plan's basis": "holds every desk at its clicks in the twelve months to September 2026",
        "what the squad takes": "It takes the headlines the desk has not put under test itself",
        "the test hours": "Clicks in those hours count at the winning headline's lift",
        "winning lift": "minus one, and nil where the control is kept",
        "note persistence": "stays on every later version until an editor clears it",
        "note put back": "that is the original correction, not a new one",
        "fix and note pairing": "on the same save or on a save no more than ten minutes before or after it",
        "headline rule": "logged on the version that publishes the corrected headline",
        "entry headline": "an entry is part of its live blog",
        "going live": "when the CMS published it at its scheduled time",
        "restore": "the recreated copy and the document it was recreated from are one article",
        "history release": "rerun on the 2026 content taxonomy",
        "restatement": "These figures replace those published",
    }
    for name, phrase in single.items():
        norm = lambda z: re.sub(r"\s+", " ", z)      # noqa: E731
        where = [f for f, txt in T.items() if norm(phrase) in norm(txt)]
        L_.check("single statement: %s appears in exactly one file" % name, len(where) == 1, str(where))
    describing = re.compile(r"(dictionary|field[_ ]?(notes|reference|guide)|readme|manifest|codebook|data[_ ]notes|"
                            r"definitions|schema)", re.I)
    files = sorted(p.name for p in Path(target).iterdir())
    L_.check("dataset-generation 3: no file describes the data, by name", not [f for f in files if describing.search(f)])
    sheets = {}
    for f in files:
        if f.endswith(".xlsx"):
            sheets[f] = pd.ExcelFile(Path(target) / f).sheet_names
    L_.check("dataset-generation 3: no sheet describes the data (no notes, definitions, about or readme sheet)",
             not any(re.search(r"^(notes?|definitions?|about|read ?me|glossary|fields?)$", s_, re.I)
                     for v in sheets.values() for s_ in v), str(sheets))
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
    leak_words = re.compile(r"\b(cannibali[sz]\w*|interference|taken from (the )?(headlines|stories) beside|"
                            r"would otherwise|new to (the site|Bightline)|zero[- ]sum|fixed slate|substitut\w*|"
                            r"pass[- ]through|holdback lift)\b", re.I)
    lk = {f: leak_words.findall(T[f]) for f in T if leak_words.findall(T[f])}
    L_.check("no shipped file names the decisive step (the clicks a winning headline takes from the ones beside it)",
             not lk, str(lk))
    meta = json.loads((Path(out) / "metadata.json").read_text())
    fmts = sorted({Path(f).suffix for f in files})
    L_.check("gate: at least 10 files", len(files) >= 10, str(len(files)))
    L_.check("gate: at least 3 formats", len(fmts) >= 3, str(fmts))
    L_.check("gate: a file of 25,000 or more rows", len(D["spine"]) >= 25_000)
    L_.check("gate: at least 2 distractors named in metadata.json, each shipped",
             len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]))
    L_.check("gate: the word distractor appears nowhere in target/ or its file names",
             not any("distractor" in t.lower() for t in T.values()) and not any("distractor" in f for f in files))
    nod = golden_figures(without(target, {F[k] for k in DISTRACTORS}))
    L_.check("gate: the distractors are unused (every graded figure recomputes unchanged with all of them deleted)", full == nod)
    L_.check("gate: metadata.json names exactly the declared distractors",
             sorted(meta["distractor_files"]) == sorted(F[k] for k in DISTRACTORS), str(meta["distractor_files"]))
    top_v = D["dash"].sort_values("avg_winning_lift_pct", ascending=False).iloc[0]["vertical"]
    dash_pick = [d for d in SL if P.DESK[d][2] == top_v]
    L_.check("wrong-basis distractor: the dashboard's top vertical carries rung 0's leader on the shortlist and neither "
             "the answer nor the strong analyst's wrong desk",
             dash_pick == [rank(rungs[0])[0]] and BUS not in dash_pick and CUL not in dash_pick, "%s %s" % (top_v, dash_pick))
    L_.check("wrong-basis distractor: ruled out by shipped facts (the brief judges the squad on Bightline's extra "
             "clicks; raw lift 0 of 7 on the change log)", rec["backtest"]["raw"][0] == 0)
    nodash = golden_figures(without(target, {F["dashboard"]}))
    L_.check("wrong-basis distractor: never the stump (with the dashboard deleted every graded figure recomputes "
             "unchanged)", nodash == full)
    try:
        golden_figures(without(target, {F["cms"], F["policy"], F["bulletin"]}), part="panel")
        golden_figures(without(target, {F["panel"], F["panelwb"]}), part="cms")
        golden_figures(without(target, {F["cms"], F["panel"], F["panelwb"], F["policy"], F["bulletin"]}), part="main")
        disjoint = True
    except Exception:
        disjoint = False
    L_.check("separation by file: the readers ask, the corrections ask and the main call each recompute without the "
             "others' device files", disjoint)
    L_.check("metadata.json: valid, deliverables two, every file listed with source, date and licence",
             len(meta["deliverables"]) == 2 and sorted(x["path"] for x in meta["files"]) == files
             and all(x["license"] and x["source"] and x["date"] for x in meta["files"]))

    # ----- timestamps and containers: each file carries the time it was written, none after the handover
    def core(name):
        with zipfile.ZipFile(Path(target) / name) as z:
            x = z.read("docProps/core.xml").decode()
            entry_times = {i.date_time for i in z.infolist()}
        get = lambda tag: re.search(r"<%s[^>]*>([^<]*)<" % tag, x).group(1)     # noqa: E731
        aest = lambda v: dt.datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ") + P.AEST     # noqa: E731
        return dict(creator=get("dc:creator"), last=get("cp:lastModifiedBy"), created=aest(get("dcterms:created")),
                    modified=aest(get("dcterms:modified")), entries=entry_times)

    def mtime(name):
        return dt.datetime(1970, 1, 1) + dt.timedelta(seconds=(Path(target) / name).stat().st_mtime) + P.AEST

    mt = {k: mtime(f) for k, f in F.items()}
    L_.check("mtimes: every file carries its own write time, all distinct and none after the handover",
             all(abs((mt[k] - W.stamp[k]).total_seconds()) < 1 for k in F) and len(set(mt.values())) == len(F)
             and max(mt.values()) <= EXPORT_STAMP, str(sorted((v, k) for k, v in mt.items())[-3:]))
    utc_aest = lambda col: pd.to_datetime(col.str.slice(0, 16)) + pd.Timedelta(hours=10)     # noqa: E731
    news = pd.read_csv(Path(target) / F["newsletter"])
    last_rec = {
        "spine": pd.Timestamp(D["spine"]["published_date"].max()) + pd.Timedelta(days=1),
        "archive": utc_aest(D["arch"]["concluded_at"]).max(),
        "cms": utc_aest(D["cms"]["saved_at"]).max(),
        "panel": pd.to_datetime(D["rel"]["published_on"]).max(),
        "pages": pd.Timestamp(2026, 10, 1),
        "newsletter": pd.to_datetime(news["week_starting"]).max() + pd.Timedelta(days=7),
        "dashboard": pd.Timestamp(2026, 10, 1, 6, 0),
        "staff": pd.to_datetime(D["staff"]["end_date"]).max(),
        "changelog": pd.to_datetime(D["chg"]["closed_on"]).max() + pd.Timedelta(days=1),
        "panelwb": pd.to_datetime(D["rel"]["published_on"]).max(),
    }
    L_.check("mtimes: no file is stamped before the latest record it carries",
             all(mt[k] >= last_rec[k].to_pydatetime() for k in last_rec),
             str({k: (str(mt[k]), str(last_rec[k])) for k in last_rec if mt[k] < last_rec[k].to_pydatetime()}))
    stated = {"plan": "9 October 2026", "charter": "12 October 2026"}
    L_.check("mtimes: a document that states its date was written on that date",
             all(mt[k].date() == dt.datetime.strptime(v, "%d %B %Y").date() for k, v in stated.items())
             and "12 October 2026" in brief_)
    wbs = {k: core(F[k]) for k in ("staff", "plan", "changelog", "panelwb")}
    L_.check("containers: every input workbook was created before its last save, saved at its file's time, by a person "
             "or team rather than the organisation, with Excel's 1980-01-01 entry times",
             all(c_["created"] < c_["modified"] == W.stamp[k] for k, c_ in wbs.items())
             and all(c_["creator"] != "Bightline News" and c_["last"] != "Bightline News" for c_ in wbs.values())
             and all(c_["entries"] == {(1980, 1, 1, 0, 0, 0)} for c_ in wbs.values()),
             str({k: (str(c_["created"]), str(c_["modified"]), c_["creator"]) for k, c_ in wbs.items()}))
    bl = core(F["bulletin"])
    L_.check("containers: the bulletin was created before its last save, saved at its file's time, Word's entry times",
             bl["created"] < bl["modified"] == W.stamp["bulletin"] and bl["entries"] == {(1980, 1, 1, 0, 0, 0)})
    from pypdf import PdfReader
    pdfmeta = {k: PdfReader(str(Path(target) / F[k])).metadata for k in ("charter", "policy", "agreement")}
    apps = {(c_, p__) for c_, p__, _ in docs_mod.PDF_APPS.values()}
    pdf_when = {k: dt.datetime.strptime(m_["/CreationDate"][2:16], "%Y%m%d%H%M%S") for k, m_ in pdfmeta.items()}
    raw_b = b"".join((Path(target) / F[k]).read_bytes() for k in pdfmeta)
    L_.check("containers: each PDF names the application it was written with, dated at its file's time, with no "
             "writing library's name anywhere in the file",
             all((m_.creator, m_.producer) in apps for m_ in pdfmeta.values())
             and all(pdf_when[k] == W.stamp[k] for k in pdfmeta) and b"reportlab" not in raw_b.lower(),
             str({k: (m_.creator, m_.producer) for k, m_ in pdfmeta.items()}))
    closed = pd.to_datetime(D["chg"]["closed_on"]).max().date()
    L_.check("dates: the change log was saved after its last embedding was signed off",
             closed < wbs["changelog"]["modified"].date() <= P.AS_OF)
    th = T[F["thread"]]
    when_last = dt.datetime.strptime(re.search(r"^Date: \w{3}, (.+?) \+1000$", th, re.M).group(1), "%d %b %Y %H:%M:%S")
    nb = re.search(r"On \w{3}, (\d+ \w{3} \d{4}) at (\d\d:\d\d), Natalie Benjamin", th)
    when_nb = dt.datetime.strptime("%s %s" % nb.groups(), "%d %b %Y %H:%M")
    named = ("spine", "archive", "staff", "plan", "changelog", "panel", "panelwb", "cms", "pages")
    L_.check("dates: the thread announces the exports after each named file was written, and was saved after its last "
             "message and before the handover",
             all(mt[k] <= when_nb for k in named) and when_last <= mt["thread"] <= EXPORT_STAMP,
             "announced %s, last message %s, saved %s" % (when_nb, when_last, mt["thread"]))

    # ----- the staff list's names
    names = list(D["staff"]["full_name"])
    sur = pd.Series([n.split()[-1] for n in names])
    L_.check("staff names: the personas among them, every name two words, Mc and O' surnames capitalised",
             all(p_n in names for p_n in world_mod.PERSONAS) and all(len(n.split()) == 2 for n in names)
             and not any(re.match(r"^Mc[a-z]|^O'[a-z]", x) for x in sur))
    L_.check("staff names: no placeholder identity, mascot, public figure or media-dynasty surname",
             not any(n.lower() in world_mod.NOT_STAFF_NAMES for n in names) and not set(sur) & world_mod.NOT_STAFF_SURNAMES)

    # ----- the prompt and the file names
    names_re = re.compile(r"(trap|decoy|distractor|naive|rung|stump|ladder|golden|answer|truth|hidden|secret|solution|"
                          r"clean(ed)?_|_fixed|correct(ed)?_|synthetic|generated|_seed|placeholder|dummy|sample_|test_|_v\d+\b|"
                          r"\bcopy\b|backup)", re.I)
    L_.check("no file name carries the author's vocabulary", not [f for f in files if names_re.search(f)])
    prompt = (P_TASK / "prompt.txt").read_text(encoding="utf-8")
    L_.check("prompt: no input file name appears in it", not [f for f in files if f in prompt])
    L_.check("prompt: no trap word and no word naming the decisive step", not author.search(prompt) and not leak_words.search(prompt))
    L_.check("prompt: the rounding sentence closes it and names every graded unit",
             prompt.rstrip().endswith("Round clicks to the nearest 50,000 and minutes to whole numbers."))
    L_.check("prompt: no prompt.md beside prompt.txt", not (P_TASK / "prompt.md").exists())
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
    return 0 if not fails else 1


P_TASK = Path(__file__).resolve().parent.parent


def golden_figures(target, part="all"):
    """The graded figures computed from whatever files sit in target (raises if one it needs is absent)."""
    t = Path(target)
    out = {}
    if part in ("all", "main"):
        # the main call never reads the dashboard export (a declared wrong-basis distractor)
        D = {"spine": pd.read_parquet(t / F["spine"]), "arch": pd.read_csv(t / F["archive"]),
             "desks": pd.read_csv(t / F["desks"]), "pages": pd.read_csv(t / F["pages"])}
        pk = packages(D["arch"])
        tests = test_table(D["arch"], pk, prior_ml(pk["L"], pk["S2"]))
        LB = lift_bases(D, tests)
        st_ = source_tables(D, set(tests["article_id"]))
        rates = page_rates(D["pages"])
        v = {d: LB["shr"][d] * sum(st_[d]["unt"].values()) * new_share(st_[d]["unt"], d, rates, D["desks"]) for d in SL}
        o = rank(v)
        out["call"] = (o[0], bin_round(v[o[0]]), o[1], bin_round(v[o[0]] - v[o[1]]))
    if part == "panel":         # the panel is a declared distractor: never part of the graded figures
        D = {"panel": pd.read_csv(t / F["panel"]),
             "sec_cur": pd.read_excel(t / F["panelwb"], sheet_name="Sections (current)", keep_default_na=False),
             "sec_hist": pd.read_excel(t / F["panelwb"], sheet_name="Section history", keep_default_na=False),
             "rel": pd.read_excel(t / F["panelwb"], sheet_name="Release log", keep_default_na=False)}
        out["readers"] = {d: (round(v[0], 2), round(v[2], 2)) for d, v in panel_readers(D).items() if d in SL}
    if part in ("all", "cms"):
        cm = cms_frames({"cms": pd.read_csv(t / F["cms"], keep_default_na=False, dtype=str)})
        g = ask_corrections(cms_rows_of(cm))
        out["corrections"] = {d: cuts(g, d) + (g[d]["articles"],) for d in SL}
    return out


def without(target, drop):
    """A scratch view of target with the named files left out (symlinks, nothing copied)."""
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="t118-"))
    for p in Path(target).iterdir():
        if p.name not in drop:
            (tmp / p.name).symlink_to(p.resolve())
    return tmp


def pair_simulation(asks, readings, G):
    """Two answer sheets per reading. The cracker lands the call; the mirror stops at rung 5 (Culture·national). The
    18 ask criteria (the three corrections cuts at six desks) never read a main-path file, so both sheets file the
    same ask figures under a reading. Planning weights 38 / 7 / 55 over the 18 ask criteria; r = 3 survives a wrong
    call."""
    w_ask = 55 / 18
    k1 = lambda v: int(np.floor(v / 1000 + 0.5))     # noqa: E731
    out = {}
    for label, V in readings.items():
        hits = sum(3 - cuts_off(V, G, d) for d in SL)
        cr, mi = 38 + 7 + w_ask * hits, 3 + 7 + w_ask * hits
        out[label] = dict(cracker=round(cr, 1), mirror=round(mi, 1), hits=hits, leakage=round(hits / 18, 3),
                          pair=round((cr + mi) / 2, 1))
    return out
