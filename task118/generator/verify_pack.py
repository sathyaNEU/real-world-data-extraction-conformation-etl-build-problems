"""Independent verifier for task118: python3 verify_pack.py <target_dir>

Reads only the shipped files in target_dir. It imports nothing from the generator, reads no seed, parameter
or side file, and recomputes every rung, every rival the change log refutes, every calibration outcome and
every graded figure on its own code path: DuckDB over the parquet with Bightline's own pages read from the brief's
list of the pages a shipped headline replaces the old one on; a profile-likelihood prior fit; each page's
click-through from the page analytics, a desk's pages named from the desk register; the change log's extra clicks
against the holdback back-tested page by page; a walk of each document's published states in the CMS revisions (an
autosave of a live article's working copy is not one) that skips a note put back after a save that left it off, as
the corrections standard says, and pairs a note on an unchanged headline with the bare headline change within the
standard's ten minutes before it, else after it, else with an entry's headline change within that window either
side, with a scheduled article live at the time its editor set if it was still scheduled then (one set back to draft
first went live when an editor published it), read on the Brisbane clock its column names; each
panel release read on the earlier section list up to the release before the release log's first on the 2026 content
taxonomy and on the 2026 list from that release on, a monthly release counted for the month its name follows and a
rerun for the months its note names, each section's month taken from the latest such release.
The CLAIMS block is the answer key it checks.
"""
import csv
import datetime as dt
import math
import re
import statistics
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

import duckdb
import numpy as np
from openpyxl import load_workbook
from scipy.optimize import minimize_scalar

CLAIMS = {
    "call": "BUS-N", "call_figure": 500_000, "runner_up": "LOC-M", "runner_up_figure": 400_000, "gap": 100_000,
    "rung_leaders": ["POL-N", "SPT-M", "BUS-N", "LOC-M", "CUL-N", "CUL-N", "BUS-N"],
    "extra": {"POL-N": 300_000, "SPT-M": 50_000, "BUS-N": 500_000, "SPT-N": 300_000, "LOC-M": 400_000,
              "CUL-N": 350_000},
    "median_minutes": {"POL-N": 86, "SPT-M": 55, "BUS-N": 89, "SPT-N": 47, "LOC-M": 102, "CUL-N": 119},
    "within_hour": {"POL-N": 14, "SPT-M": 9, "BUS-N": 10, "SPT-N": 23, "LOC-M": 12, "CUL-N": 1},
    "over_three_hours": {"POL-N": 7, "SPT-M": 2, "BUS-N": 6, "SPT-N": 2, "LOC-M": 6, "CUL-N": 5},
    "total_minutes": {"POL-N": 5231, "SPT-M": 1342, "BUS-N": 4109, "SPT-N": 2799, "LOC-M": 21693, "CUL-N": 2057},
    "backtest_hits": 7, "click_backtest_hits": 7,
    "bulletin_march": (11, 22),
}
SHORTLIST = ["POL-N", "SPT-M", "BUS-N", "SPT-N", "LOC-M", "CUL-N"]
PLATFORM = ("home_web", "section_web", "feed_app", "section_app", "related_links")

results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))


def r50k(x):
    return int(math.floor(x / 50_000 + 0.5) * 50_000)


def one_dp(x):
    return math.floor(x * 10 + 0.5) / 10


def main(target):
    t = Path(target)
    files = {p.name: p for p in t.iterdir()}

    def find(prefix):
        hit = [n for n in files if n.startswith(prefix)]
        assert len(hit) == 1, prefix
        return files[hit[0]]

    spine = find("pageviews_by_source_age")
    archive = find("headline_tests_archive")
    staff = find("newsroom_staff_list")
    plan = find("audience_plan_2027")
    changelog = find("headline_squad_change_log")
    desks_f = find("desk_register")
    dash_f = find("experimentation_dashboard_export")
    cms_f = find("cms_revisions_web_desks")
    panel_f = find("panel_monthly_audience")
    panelwb = find("panel_reference_workbook")

    # ------------------------------------------------------------------ desks, plan, staff
    desks = {r["desk_code"]: r for r in csv.DictReader(open(desks_f, encoding="utf-8"))}
    wb = load_workbook(plan, read_only=True, data_only=True)
    rows = list(wb["Plan 2027"].iter_rows(values_only=True))
    planned = {r[0]: int(r[4]) for r in rows[1:] if r[0] and r[0] != "Total"}
    wb = load_workbook(staff, read_only=True, data_only=True)
    srows = list(wb["Staff"].iter_rows(values_only=True))
    team = {r[0]: r[2] for r in srows[1:]}

    # ------------------------------------------------------------------ the archive, test by test
    tests = defaultdict(list)
    meta = {}
    for r in csv.DictReader(open(archive, encoding="utf-8")):
        tests[r["test_id"]].append(r)
        meta[r["test_id"]] = (r["engine"], r["desk_code"], int(r["article_id"]), r["owner_staff_id"],
                              r["started_at"], r["concluded_at"])
    L, S2, pkg_test = [], [], []
    per_test = {}
    for tid, pk in tests.items():
        ctl = [p for p in pk if p["variant"] == "control"][0]
        n0, c0 = int(ctl["impressions"]), int(ctl["clicks"])
        p0 = c0 / n0
        lifts = []
        for p in pk:
            if p["variant"] == "control":
                continue
            n, c = int(p["impressions"]), int(p["clicks"])
            pv = c / n
            rr = pv / p0
            s2 = rr * rr * ((1 - pv) / (n * pv) + (1 - p0) / (n0 * p0))
            L.append(rr - 1)
            S2.append(s2)
            pkg_test.append(tid)
            lifts.append((rr - 1, s2, p["shipped"] == "Y", pv - p0))
        per_test[tid] = lifts
    L, S2 = np.array(L), np.array(S2)

    def neg_profile(tau2):
        w = 1 / (tau2 + S2)
        mu = np.sum(w * L) / np.sum(w)
        return 0.5 * np.sum(np.log(tau2 + S2) + (L - mu) ** 2 * w)

    res = minimize_scalar(neg_profile, bounds=(1e-7, 0.05), method="bounded", options={"xatol": 1e-13})
    tau2 = float(res.x)
    w = 1 / (tau2 + S2)
    mu = float(np.sum(w * L) / np.sum(w))
    prior = (mu, tau2)
    mom = (float(L.mean()), float(L.var() - S2.mean()))

    def fit_profile(Lx, Sx):
        def neg(t2):
            wx = 1 / (t2 + Sx)
            return 0.5 * np.sum(np.log(t2 + Sx) + (Lx - np.sum(wx * Lx) / np.sum(wx)) ** 2 * wx)
        t2 = float(minimize_scalar(neg, bounds=(1e-7, 0.05), method="bounded", options={"xatol": 1e-13}).x)
        wx = 1 / (t2 + Sx)
        return float(np.sum(wx * Lx) / np.sum(wx)), t2

    # rival forms of the estimator: the log of the click-through ratio, and the ratio minus one with the
    # ratio-squared term dropped from its variance (both use the same variance, which is the log ratio's)
    V0 = S2 / (1 + L) ** 2
    pkg_engine = np.array([meta[x][0] for x in pkg_test])
    prior_log = fit_profile(np.log1p(L), V0)
    prior_nr = fit_profile(L, V0)
    prior_app = fit_profile(L[pkg_engine == "app"], S2[pkg_engine == "app"])
    prior_web = fit_profile(L[pkg_engine == "web"], S2[pkg_engine == "web"])

    def win_form(tid, pr, form):
        for l, s2, shipped, _ in per_test[tid]:
            if shipped:
                v0 = s2 / (1 + l) ** 2
                if form == "log":
                    return math.exp(pr[0] + pr[1] / (pr[1] + v0) * (math.log1p(l) - pr[0])) - 1
                return pr[0] + pr[1] / (pr[1] + v0) * (l - pr[0])
        return 0.0

    def win(tid, pr, shrink=True):
        for l, s2, shipped, _ in per_test[tid]:
            if shipped:
                return (pr[0] + pr[1] / (pr[1] + s2) * (l - pr[0])) if shrink else l
        return 0.0

    by_desk = defaultdict(list)
    for tid, m in meta.items():
        by_desk[m[1]].append(tid)
    web = {d: [x for x in by_desk[d] if meta[x][0] == "web"] for d in by_desk}
    raw = {d: np.mean([win(x, prior, False) for x in web[d]]) for d in SHORTLIST}
    shr = {d: np.mean([win(x, prior) for x in web[d]]) for d in SHORTLIST}
    check("one test per article", len({m[2] for m in meta.values()}) == len(meta))
    check("every shortlisted-desk test is owned by that desk's own staff",
          all(team.get(meta[x][3]) == meta[x][1] for d in SHORTLIST for x in by_desk[d]))
    check("every app-desk test is owned by the headline squad",
          all(team.get(m[3]) == "AUD-HS" for m in meta.values() if desks[m[1]]["distribution"] == "app only"))

    # ------------------------------------------------------------------ the pages a shipped headline sits on
    from pypdf import PdfReader
    brief = re.sub(r"\s+", " ", " ".join(pg.extract_text() or "" for pg in PdfReader(str(find("headline_squad_2027"))).pages))
    own_s = re.search(r"wherever Bightline sets the headline: (.+?)\. (.+?) keep the headline stored at publication", brief)
    own_txt, stored_txt = (own_s.group(1).lower(), own_s.group(2).lower()) if own_s else ("", "")
    own_words = {"home_web": "home pages", "section_web": "section fronts", "feed_app": "app home feed",
                 "section_app": "tabs", "related_links": "related-story links"}
    stored_words = {"search": "search", "discover": "discover", "partner_apps": "partner", "social": "social",
                    "newsletter": "newsletter", "alerts": "alert"}
    plat_codes = sorted(code for code, word in own_words.items() if word in own_txt)
    check("the brief names every page a shipped headline replaces the old one on, and every surface that keeps the "
          "stored headline", plat_codes == sorted(PLATFORM) and all(w_ in stored_txt for w_ in stored_words.values()),
          own_txt[:120])
    page_v, page_c = defaultdict(int), defaultdict(int)
    for r in csv.DictReader(open(find("page_performance_monthly"), encoding="utf-8")):
        page_v[r["page"]] += int(r["page_views"])
        page_c[r["page"]] += int(r["article_clickthroughs"])
    ctr = {k: page_c[k] / page_v[k] for k in page_v}

    def page(d, src):
        metro = desks[d]["edition"] == "Brisbane"
        nm = desks[d]["desk_name"] if desks[d]["distribution"] == "app only" else desks[d]["vertical"]
        return {"home_web": "bightline.com.au/brisbane/" if metro else "bightline.com.au/",
                "section_web": "bightline.com.au/%s%s/" % ("brisbane/" if metro else "", nm.lower()),
                "feed_app": "Home feed", "section_app": "Tab: %s%s" % ("Brisbane " if metro else "", nm),
                "related_links": "Related stories (article pages)"}[src]

    # ------------------------------------------------------------------ the spine, through DuckDB
    con = duckdb.connect()
    con.execute("CREATE TABLE pv AS SELECT * FROM read_parquet('%s')" % str(spine).replace("'", "''"))
    tested = {m[2] for m in meta.values()}
    con.execute("CREATE TABLE tested AS SELECT unnest(?::BIGINT[]) AS article_id", [sorted(tested)])
    plat_list = ",".join("'%s'" % s_ for s_ in plat_codes)
    q = """
      SELECT p.desk_code, sum(pageviews) AS total,
             sum(pageviews) FILTER (WHERE source_code IN ({pl})) AS plat,
             sum(pageviews) FILTER (WHERE t.article_id IS NOT NULL AND source_code IN ({pl})) AS t_plat,
             count(DISTINCT p.article_id) FILTER (WHERE published_date >= DATE '2025-10-01') AS n_win
      FROM pv p LEFT JOIN tested t USING (article_id) GROUP BY p.desk_code""".format(pl=plat_list)
    C = {r[0]: dict(zip(["total", "plat", "t_plat", "n_win"], [x or 0 for x in r[1:]])) for r in con.execute(q).fetchall()}
    by_src_all, by_src_unt = defaultdict(dict), defaultdict(dict)
    for d, src, n_all, n_unt in con.execute("""
            SELECT p.desk_code, source_code, sum(pageviews), sum(pageviews) FILTER (WHERE t.article_id IS NULL)
            FROM pv p LEFT JOIN tested t USING (article_id) WHERE source_code IN ({pl}) GROUP BY 1, 2""".format(pl=plat_list)).fetchall():
        by_src_all[d][src] = int(n_all)
        by_src_unt[d][src] = int(n_unt or 0)
    check("spine totals equal the plan's 2027 clicks for every desk", all(C[d]["total"] == planned[d] for d in planned))
    tie = defaultdict(int)
    for d in by_src_all:
        for src, n in by_src_all[d].items():
            tie[page(d, src)] += n
    check("every page's twelve months of article click-throughs equal the spine's own-page clicks that start there",
          dict(tie) == dict(page_c), str({k: (tie[k], page_c.get(k)) for k in tie if tie[k] != page_c.get(k)}))
    dash = {}
    lines = open(dash_f, encoding="utf-8").read().splitlines()
    hdr = lines.index("vertical,tests_concluded,tests_with_variant_shipped,avg_winning_lift_pct")
    for r in csv.reader(lines[hdr + 1:]):
        dash[r[0]] = float(r[3]) / 100
    lo, hi = dt.datetime(2025, 9, 30, 14), dt.datetime(2026, 9, 30, 14)
    okd = True
    for v, lift in dash.items():
        ids = [x for x, m in meta.items() if desks[m[1]]["vertical"] == v
               and lo <= dt.datetime.strptime(m[5], "%Y-%m-%dT%H:%M:%SZ") < hi]
        okd &= round(100 * np.mean([win(x, prior, False) for x in ids]), 2) == round(100 * lift, 2)
    check("dashboard reproduces from the archive", okd)

    vert = {d: desks[d]["vertical"] for d in desks}
    unt = {d: C[d]["plat"] - C[d]["t_plat"] for d in SHORTLIST}
    new = {d: sum(n * (1 - ctr[page(d, src)]) for src, n in by_src_unt[d].items()) / unt[d] for d in SHORTLIST}

    # ------------------------------------------------------------------ the change log: the share kept, page by page
    wb_c = load_workbook(changelog, read_only=True, data_only=True)
    crow_ = list(wb_c["Embeddings"].iter_rows(values_only=True))
    emb_ = [dict(zip(crow_[0], r)) for r in crow_[1:] if r[0] is not None]
    kept = []
    hits_c = 0
    for e in emb_:
        mix = by_src_all[e["desk_code"]]
        share = sum(n * (1 - ctr[page(e["desk_code"], src)]) for src, n in mix.items()) / sum(mix.values())
        won_ = e["planned_clicks"] * e["realised_holdback_lift_pct"] / 100
        kept.append(e["extra_clicks_vs_holdback"] / won_)
        hits_c += abs(won_ * share / e["extra_clicks_vs_holdback"] - 1) <= 0.02
    check("back-test, clicks: planned clicks x realised lift x the share of each page's views with no article click "
          "reproduces %d of 7 embeddings' extra clicks within 2%%" % CLAIMS["click_backtest_hits"],
          hits_c == CLAIMS["click_backtest_hits"], str(hits_c))
    avg_kept = float(np.mean(kept))
    avg_hits = sum(abs(k_ / avg_kept - 1) <= 0.02 for k_ in kept)
    check("back-test, clicks: one share for every embedding (their average) misses most of them", avg_hits <= 2,
          "%d of 7 within 2%%" % avg_hits)
    # the brief's sign-off: the working run unchanged on each closed embedding within 2 per cent of the lift and the
    # extra clicks it realised against its holdback (the lift half is the back-test below)
    signoff = re.search(r"Experimentation signs off that figure only if the working behind it, run unchanged on each "
                        r"closed embedding in the change log, comes within (\d+) per cent of what the embedding realised "
                        r"against its holdback: the lift, from the desk's tests in the year of the embedding, and the "
                        r"extra clicks, from its planned clicks at the lift it realised\.", brief)
    check("the brief files the sign-off at 2 per cent, its lift and its extra clicks, embedding by embedding",
          signoff is not None and signoff.group(1) == "2")
    raw_e = {}
    for e in emb_:
        ids_ = [x for x, m in meta.items() if m[0] == "app" and m[1] == e["desk_code"] and int(m[4][:4]) == e["started"].year]
        raw_e[e["embedding"]] = float(np.mean([win(x, prior, False) for x in ids_]))
    k_one = sum(e["extra_clicks_vs_holdback"] for e in emb_) / sum(e["planned_clicks"] * raw_e[e["embedding"]] for e in emb_)
    one_hits = sum(abs(e["planned_clicks"] * raw_e[e["embedding"]] * k_one / e["extra_clicks_vs_holdback"] - 1) <= 0.02
                   for e in emb_)
    check("the sign-off refutes each desk's raw winning lift scaled by one factor fitted on the change log (%.4f): "
          "its extra clicks within 2%% at %d of 7" % (k_one, one_hits), one_hits <= 2)

    rungs = [{d: dash[vert[d]] * C[d]["total"] for d in SHORTLIST},
             {d: raw[d] * C[d]["total"] for d in SHORTLIST},
             {d: shr[d] * C[d]["total"] for d in SHORTLIST},
             {d: shr[d] * C[d]["plat"] for d in SHORTLIST},
             {d: shr[d] * unt[d] for d in SHORTLIST},
             {d: shr[d] * unt[d] * avg_kept for d in SHORTLIST},
             {d: shr[d] * unt[d] * new[d] for d in SHORTLIST}]
    for k, vals in enumerate(rungs):
        o = sorted(vals, key=vals.get, reverse=True)
        check("rung %d leader %s, margin at least 1.2" % (k, CLAIMS["rung_leaders"][k]),
              o[0] == CLAIMS["rung_leaders"][k] and vals[o[0]] / vals[o[1]] >= 1.2,
              "%s %.3f" % (o[0], vals[o[0]] / vals[o[1]]))
    r6 = rungs[6]
    o6 = sorted(r6, key=r6.get, reverse=True)
    check("call: %s at %s" % (CLAIMS["call"], CLAIMS["call_figure"]), o6[0] == CLAIMS["call"]
          and r50k(r6[o6[0]]) == CLAIMS["call_figure"], "%.0f" % r6[o6[0]])
    check("runner-up, its figure and the gap", o6[1] == CLAIMS["runner_up"] and r50k(r6[o6[1]]) == CLAIMS["runner_up_figure"]
          and r50k(r6[o6[0]] - r6[o6[1]]) == CLAIMS["gap"], "%s %.0f %.0f" % (o6[1], r6[o6[1]], r6[o6[0]] - r6[o6[1]]))
    for d in SHORTLIST:
        check("extra clicks %s" % d, r50k(r6[d]) == CLAIMS["extra"][d], "%.0f" % r6[d])
    check("dominance over Culture·national and Local·metro at least 1.2 (the share new to Bightline over the lead carried "
          "into the last step)", all((new["BUS-N"] / new[x]) / (rungs[4][x] / rungs[4]["BUS-N"]) >= 1.2
                                     for x in ("CUL-N", "LOC-M")))

    # ------------------------------------------------------------------ the change log back-test
    wb = load_workbook(changelog, read_only=True, data_only=True)
    crow = list(wb["Embeddings"].iter_rows(values_only=True))
    hdrc = crow[0]
    emb = [dict(zip(hdrc, r)) for r in crow[1:] if r[0] is not None]
    with zipfile.ZipFile(changelog) as z:
        saved = re.search(r"<dcterms:modified[^>]*>(\d{4}-\d\d-\d\dT\d\d:\d\d)", z.read("docProps/core.xml").decode())
    saved = (dt.datetime.strptime(saved.group(1), "%Y-%m-%dT%H:%M") + dt.timedelta(hours=10)).date().isoformat()
    check("the change log was last saved after its last embedding was signed off",
          saved > max(e["closed_on"] for e in emb).date().isoformat(), saved)
    app_tests = defaultdict(list)
    for x, m in meta.items():
        if m[0] == "app":
            app_tests[(m[1], int(m[4][:4]))].append(x)
    imp = {x: sum(int(p["impressions"]) for p in tests[x]) for x in tests}
    clk = {x: sum(int(p["clicks"]) for p in tests[x]) for x in tests}

    def fit_mom(ids):
        sel = np.isin(np.array(pkg_test), ids)
        return float(L[sel].mean()), max(float(L[sel].var() - S2[sel].mean()), 0.0)

    preds = defaultdict(dict)
    real = {}
    for e in emb:
        ids = app_tests[(e["desk_code"], e["started"].year)]
        real[e["embedding"]] = float(e["realised_holdback_lift_pct"]) / 100
        plan_c = 1.0        # the log records a lift, so every prediction is a lift
        check("change log row %d: tests and observed lift reproduce" % e["embedding"],
              len(ids) == e["tests_run"] and round(100 * np.mean([win(x, prior, False) for x in ids]), 1) == round(e["avg_winning_lift_pct"], 1))
        g = np.mean([win(x, prior) for x in ids])
        preds["golden"][e["embedding"]] = g * plan_c
        preds["raw"][e["embedding"]] = np.mean([win(x, prior, False) for x in ids]) * plan_c
        preds["pooled MoM"][e["embedding"]] = np.mean([win(x, mom) for x in ids]) * plan_c
        desk_ids = [x for (dk, y), v in app_tests.items() if dk == e["desk_code"] for x in v]
        preds["per-desk MoM"][e["embedding"]] = np.mean([win(x, fit_mom(desk_ids)) for x in ids]) * plan_c
        preds["per-embedding MoM"][e["embedding"]] = np.mean([win(x, fit_mom(ids)) for x in ids]) * plan_c
        vids = [x for (dk, y), v in app_tests.items() if vert[dk] == vert[e["desk_code"]] for x in v]
        preds["per-vertical MoM"][e["embedding"]] = np.mean([win(x, fit_mom(vids)) for x in ids]) * plan_c
        sv = []
        for x in ids:
            best = max(prior[0] + prior[1] / (prior[1] + s2) * (l - prior[0]) for l, s2, _, _ in per_test[x])
            sv.append(max(0.0, best))
        preds["shrink then max"][e["embedding"]] = np.mean(sv) * plan_c
        wv = np.array([win(x, prior) for x in ids])
        preds["impression-weighted"][e["embedding"]] = np.average(wv, weights=[imp[x] for x in ids]) * plan_c
        preds["click-weighted"][e["embedding"]] = np.average(wv, weights=[clk[x] for x in ids]) * plan_c
        preds["absolute points"][e["embedding"]] = np.mean(
            [next((dp for _, _, sh, dp in per_test[x] if sh), 0.0) for x in ids]) * plan_c
        preds["log-scale shrinkage"][e["embedding"]] = np.mean([win_form(x, prior_log, "log") for x in ids]) * plan_c
        preds["variance without the ratio-squared term"][e["embedding"]] = \
            np.mean([win_form(x, prior_nr, "nr") for x in ids]) * plan_c
        preds["app-engine prior"][e["embedding"]] = np.mean([win(x, prior_app) for x in ids]) * plan_c
        preds["web-engine prior (convergent)"][e["embedding"]] = np.mean([win(x, prior_web) for x in ids]) * plan_c
    rawv = np.array([preds["raw"][k] for k in sorted(real)])
    realv = np.array([real[k] for k in sorted(real)])
    kcut = float(np.sum(rawv * realv) / np.sum(rawv ** 2))
    preds["global haircut"] = {k: kcut * preds["raw"][k] for k in real}
    for name, p in preds.items():
        err = [abs(p[k] / real[k] - 1) for k in real]
        hits = sum(e <= 0.02 for e in err)
        miss = sum(e > 0.03 for e in err)
        if name == "golden":
            check("back-test: the golden method gets %d of 7 within 2%%" % CLAIMS["backtest_hits"],
                  hits == CLAIMS["backtest_hits"], "worst %.2f%%" % (100 * max(err)))
        elif "(convergent)" in name:
            check("back-test: %s gets %d of 7 within 2%%" % (name, CLAIMS["backtest_hits"]),
                  hits == CLAIMS["backtest_hits"], "worst %.2f%%" % (100 * max(err)))
        else:
            check("back-test refutes %s (2 or more of 7 missed by over 3%%)" % name, miss >= 2,
                  "%d hits %d misses" % (hits, miss))
    t3 = [e for e in emb if e["embedding"] == 3][0]
    t6 = [e for e in emb if e["embedding"] == 6][0]
    check("twins identical on every change-log column a lookup sees, realised about 2x apart",
          all(t3[k] == t6[k] for k in ("tests_run", "avg_winning_lift_pct", "distribution"))
          and 1.95 <= real[3] / real[6] <= 2.1, "%.3f" % (real[3] / real[6]))

    # ------------------------------------------------------------------ corrections: a walk of the published states
    docs = defaultdict(list)
    info = {}
    for r in csv.DictReader(open(cms_f, encoding="utf-8")):
        # an autosave of a live article's working copy is saved while the article is live and publishes nothing
        status = "autosave" if r["save_type"] == "autosave" else r["status"]
        docs[r["doc_id"]].append((int(r["revision"]), r["saved_at"], status, r["publish_at_aest"], r["headline_sha1"],
                                  r["correction_note"]))
        info[r["doc_id"]] = (r["desk_code"], r["doc_type"], r["parent_doc"], r["restored_from_doc"], r["migrated_from"])
    copy_of = {v[3]: k for k, v in info.items() if v[3]}
    ts = lambda x: dt.datetime.strptime(x, "%Y-%m-%dT%H:%MZ")        # noqa: E731
    # an entry that publishes a changed headline, by the live blog it belongs to
    entry_fix = defaultdict(set)
    for did, (desk, typ, parent, restored, migrated) in info.items():
        if typ != "post" or restored:
            continue
        revs = sorted(docs[did]) + (sorted(docs[copy_of[did]]) if did in copy_of else [])
        shown = [r for r in revs if r[2] == "live"]
        blog = info[parent][3] or parent
        for a, b in zip(shown, shown[1:]):
            if b[4] != a[4]:
                entry_fix[blog].add(ts(b[1]))
    # the corrections standard: a fix and its note on one save or on saves up to ten minutes apart; a note put back is
    # the original correction; time to correction from when the article was first published
    std = re.sub(r"\s+", " ", " ".join(pg.extract_text() or "" for pg in PdfReader(str(find("editorial_standards"))).pages))
    pair = re.search(r"on the same save or on a save no more than (\w+) minutes before or after it", std)
    check("the corrections standard states the window a fix and its note are saved within", pair is not None)
    put_back = "that is the original correction, not a new one" in std
    check("the corrections standard says a note put back after a save that dropped it is the original correction", put_back)
    check("SF19 the corrections standard says an autosave of an editor's working copy publishes nothing",
          "An autosave of an editor's working copy publishes nothing" in std)
    check("SF12 the corrections standard times a correction from the article's first publication, by a live save or at "
          "the scheduled time the CMS published it",
          "when it was first published, by a live save or, for a scheduled article, when the CMS published it at its "
          "scheduled time" in std)
    hdr_cms = open(cms_f, encoding="utf-8").readline().strip().split(",")
    check("SF13 the CMS export names Brisbane time on the scheduled time's column, and its save times are UTC",
          "publish_at_aest" in hdr_cms and "saved_at" in hdr_cms)
    check("SF14 the brief has the squad take the headlines a desk has not put under test, and every headline put under "
          "test recorded whether or not a variant ships",
          "It takes the headlines the desk has not put under test itself" in brief and "whether or not a variant ships" in brief)
    # SF11's data half, independent of the brief's wording: the realised impression-weighted rate across every
    # package of a test is strictly below the shipped variant's, so crediting the under-test hours at the mixture
    # rate is strictly lower than crediting them at the winning lift, and the brief's sentence is load-bearing.
    # Scoped to the tests that HAVE a winning lift to credit: where the control is kept the shipped package is the
    # control and the lift is zero by the field reference's own definition, so there is no rate to argue about.
    mix_below, kept_control = [], 0
    for tid_, pk_ in tests.items():
        shp = [p for p in pk_ if p["shipped"] == "Y"]
        if not shp:
            continue
        if shp[0]["variant"] == "control":
            kept_control += 1
            continue
        imp = sum(int(p["impressions"]) for p in pk_)
        clk = sum(int(p["clicks"]) for p in pk_)
        s_ctr = int(shp[0]["clicks"]) / int(shp[0]["impressions"])
        mix_below.append((clk / imp) < s_ctr)
    check("SF11 at every test that shipped a variant (%d of them, the %d control-kept tests carrying no winning lift "
          "to credit), the realised impression-weighted click-through across every package is below the shipped "
          "variant's, so the mixture reading of the under-test hours is strictly lower than the winning lift the "
          "brief names and that sentence is load-bearing" % (len(mix_below), kept_control),
          bool(mix_below) and all(mix_below), "%d of %d below" % (sum(mix_below), len(mix_below)))
    W_ = dt.timedelta(minutes={"five": 5, "ten": 10, "fifteen": 15, "twenty": 20}[pair.group(1)])
    # (the scheduled time's clock is the one its column names: Brisbane, ten hours ahead of the UTC saves)
    count, arts, mins, march = defaultdict(int), defaultdict(int), defaultdict(list), [0, 0]
    m_lo, m_hi = dt.datetime(2026, 2, 28, 14), dt.datetime(2026, 3, 31, 14)      # March 2026, AEST
    for did, revs in docs.items():
        desk, typ, parent, restored, migrated = info[did]
        if restored or migrated or typ == "post":
            continue
        chain = sorted(revs)
        if did in copy_of:
            chain = chain + sorted(docs[copy_of[did]])
        live = [r for r in chain if r[2] == "live"]
        if not live:
            continue
        arts[desk] += 1
        states, golive = live, ts(live[0][1])
        sched = [r for r in chain if r[2] == "scheduled" and r[0] < live[0][0]]
        # publish_at is the time the editor set, on the newsroom's clock (AEST, no daylight saving): on that clock
        # every article the CMS published goes live minutes before its first live save
        set_at = dt.datetime.strptime(sched[-1][3], "%Y-%m-%dT%H:%M") - dt.timedelta(hours=10) if sched and sched[-1][3] \
            else None
        # the CMS publishes at that time only what is still scheduled then: the last save up to it must be that schedule
        # (an article set back to draft before its time went live when an editor published it)
        if set_at is not None and set_at < golive:
            last = [r for r in chain if r[0] < live[0][0] and ts(r[1]) <= set_at][-1]
            if last[2] == "scheduled" and last[3] == sched[-1][3]:
                states, golive = [sched[-1]] + live, set_at
        first, bare = None, None        # bare: a headline change published with no new note
        shown, taken = {states[0][5]}, set()
        for i in range(1, len(states)):
            a, b = states[i - 1], states[i]
            when = ts(b[1])
            repeat = put_back and b[5] in shown     # a note the document had already shown, put back
            shown.add(b[5])
            if not b[5] or b[5] == a[5] or repeat:
                bare = None if b[5] != a[5] else (when if b[4] != a[4] and i not in taken else bare)
                continue
            fixes = sorted(f for f in entry_fix.get(did, ()) if when - W_ <= f <= when + W_)
            after = None
            if b[4] == a[4] and not (bare is not None and when - bare <= W_):
                for j in range(i + 1, len(states)):
                    if ts(states[j][1]) - when > W_ or states[j][5] != states[j - 1][5]:
                        break
                    if states[j][4] != states[j - 1][4]:
                        after = j
                        break
            # a note on an unchanged headline records the bare headline change just before it, or just after it, or
            # an entry's fix
            if b[4] != a[4]:
                at = when
            elif bare is not None and when - bare <= W_:
                at = bare
            elif after is not None:
                at = ts(states[after][1])
                taken.add(after)
            else:
                at = fixes[0] if fixes else None
            bare = None
            if at is not None:
                count[desk] += 1
                march[0] += m_lo <= at < m_hi
                first = at if first is None or at < first else first
            else:
                march[1] += m_lo <= when < m_hi
        if first is not None:
            mins[desk].append(int((first - golive).total_seconds() // 60))
    for d in SHORTLIST:
        check("articles %s equal the spine's base-year articles" % d, arts[d] == C[d]["n_win"], "%d %d" % (arts[d], C[d]["n_win"]))
        check("median minutes to first headline correction %s" % d,
              len(mins[d]) % 2 == 1 and statistics.median(mins[d]) == CLAIMS["median_minutes"][d],
              "%s over %d articles" % (statistics.median(mins[d]), len(mins[d])))
        check("total minutes to first headline correction %s" % d, sum(mins[d]) == CLAIMS["total_minutes"][d],
              str(sum(mins[d])))
        check("first corrections within an hour and after more than three hours %s" % d,
              sum(m_ <= 60 for m_ in mins[d]) == CLAIMS["within_hour"][d]
              and sum(m_ > 180 for m_ in mins[d]) == CLAIMS["over_three_hours"][d]
              and not any(58 <= m_ <= 62 or 178 <= m_ <= 182 for m_ in mins[d]),
              "%d %d" % (sum(m_ <= 60 for m_ in mins[d]), sum(m_ > 180 for m_ in mins[d])))
    bull = find("standards_bulletin")
    with zipfile.ZipFile(bull) as z:
        text = re.sub(r"<[^>]+>", " ", z.read("word/document.xml").decode("utf-8"))
    mm = re.search(r"logged (\d+) headline corrections and (\d+) corrections to article text", re.sub(r"\s+", " ", text))
    check("the bulletin's March figures reproduce under the standards rule",
          mm is not None and (int(mm.group(1)), int(mm.group(2))) == tuple(march) == CLAIMS["bulletin_march"],
          "%s %s" % (mm.groups() if mm else None, march))

    # ------------------------------------------------------------------ the bundle as a record (house checks)
    aest = dt.timedelta(hours=10)
    handover = dt.datetime(2026, 10, 16, 9, 0)
    mt = {n: dt.datetime(1970, 1, 1) + dt.timedelta(seconds=p.stat().st_mtime) + aest for n, p in files.items()}
    last_cms = max(r["saved_at"] for r in csv.DictReader(open(cms_f, encoding="utf-8")))
    last_test = max(m[5] for m in meta.values())
    last_pub = con.execute("SELECT max(published_date) FROM pv").fetchone()[0]
    check("no file is written after the handover, and none of the three big extracts before its latest record",
          max(mt.values()) <= handover
          and mt[cms_f.name] >= dt.datetime.strptime(last_cms[:16], "%Y-%m-%dT%H:%M") + aest
          and mt[archive.name] >= dt.datetime.strptime(last_test[:16], "%Y-%m-%dT%H:%M") + aest
          and mt[spine.name].date() > last_pub, "%s %s %s" % (last_cms, last_test, last_pub))
    bad_wb = []
    for n in files:
        if n.endswith(".xlsx"):
            with zipfile.ZipFile(files[n]) as z:
                core = z.read("docProps/core.xml").decode()
            c = re.search(r"<dcterms:created[^>]*>([^<]+)<", core).group(1)
            m_ = re.search(r"<dcterms:modified[^>]*>([^<]+)<", core).group(1)
            if not c < m_ or "openpyxl" in core or "xlsxwriter" in core.lower():
                bad_wb.append(n)
    raw_pdf = b"".join(files[n].read_bytes() for n in files if n.endswith(".pdf"))
    producers = set(re.findall(rb"/Producer \(([^)]*)\)", raw_pdf))
    check("every input workbook was created before its last save; every PDF names a real producer and no writing "
          "library", not bad_wb and b"ReportLab" not in raw_pdf and producers
          and not any(b"Bightline" in x for x in producers), "%s %s" % (bad_wb, producers))
    surnames = [str(r[1]).split()[-1] for r in srows[1:] if r[1]]
    check("staff surnames carry their capitals (McDonald, O'Brien), none lowercased after Mc or O'",
          not any(re.match(r"^Mc[a-z]|^O'[a-z]", x) for x in surnames), str([x for x in surnames if x[:2] == "Mc"][:6]))

    n_ok = sum(1 for r in results if r[1])
    for name, ok, det in results:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  [%s]" % det) if det else ""))
    print("\nverifier: %d checks, %d passed, %d failed" % (len(results), n_ok, len(results) - n_ok))
    return 0 if n_ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parent.parent / "target")))
