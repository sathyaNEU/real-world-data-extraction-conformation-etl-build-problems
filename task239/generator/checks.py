"""task239 checks: the three rules executed on the simulator's clean truth (R1 to R3c), every semantic fork row (SF1 to
SF16), the rungs and their margins, every Layer 1 slip against the call, the ask devices and their stops, the
separation of the call from the devices, the documents' pins, the input gates and the realism sweep."""
import hashlib
import json
import os
import re
from decimal import ROUND_HALF_EVEN, Decimal

import numpy as np
import pandas as pd

import build as B
import estim as E
import exports as XP
import params as P
import plans as PL
import writeup as WU

FORCING, STOPS, EDGE = {}, {}, [1.0]
# the 10-17 cut's files (target.zip 8598f854), which every file the call reads must reproduce
SHIPPED = {
    "lfp_hr_reorganisation_map_2027-09-01.csv": "8c228b7d8d0b661127d8df292ed846a56eb1a75ddeff23d32f26c949687f3d11",
    "lfp_hr_staff_in_post_2027-09-01.csv": "72f0dcdfb9d68f850eff6f9a4231b3889d8a62dae4a6384af9cda2b28f8249f6",
    "lfp_hr_team_register_2027-11-15.csv": "5c0a86ace71856bb252151f959593ef91615a778348d511d76916ca4fe405284",
    "lfp_staff_voice_2027_dashboard_methodology.docx": "1e1ebd4b8594ceeb7821d020e2728d2ef9ba468c89e58d80590bbddf5deb8ee2",
    "lfp_staff_voice_2027_fieldwork_closeout.docx": "5bf763bcfad0131dd59ee0ac34f612ede7783741dae6eb477df1f2aaaa64e139",
    "lfp_sv26_dashboard_items.csv": "50f767cc22c706b0513b0a1a05604891626780a3fde23d326b29baf218738396",
    "lfp_sv27_paper_packs.csv": "752db97d97e3d438f9846ff0394977880ad10c91b8c7704e0b9e0d4778a39901",
    "lfp_sv27_paper_scans.csv": "885547f531283d6819a8cfdb0ff25493d4df6a0977f46a3bcdf65c433ee308d2",
    "lfp_sv27_platform_responses.csv": "8118838a07f99022562e26999c01c9175f069cba9b8bd182bc8e42b70ad0760b",
    "lfp_sv27_platform_sessions.csv": "1257997f42df9d11c60cf3437d480c31df09fd04a3820b29aaf1701cde48666a",
    "lfp_sv27_site_tablet_log.csv": "4aaecef1f129c8c95835e73ba4e64f08962d6a3e8dd76827d227d5b06f495ebd",
    "lfp_wi_sv03_measurement_standard_2027.pdf": "435e9244782733e8950cfd75d0341a0e1a5592d181ad87a6a44a2cfc8da226c4",
}

N = [0]
HERE = os.path.dirname(os.path.abspath(__file__))
B_ITEMS = ["TC09", "TC10"]
C_ITEMS = ["TC11", "TC12"]
SLIPS = {
    "a member's earlier returns kept": dict(member=False),
    "a tablet's re-sent sessions kept": dict(replay=False),
    "a personal link's earlier submission kept": dict(resubmit=False),
    "paper forms after 8 October kept": dict(late=False),
    "blank paper forms kept": dict(blank=False),
    "unsubmitted sessions kept": dict(submitted_only=False),
    "don't know read as a sixth point": dict(scale="dk_value"),
    "paper's 8 and 9 read as answers": dict(scale="paper_raw_codes"),
    "TC04 and TC07 left unreversed": dict(scale="neg_not_reversed"),
    "tablet codes joined as they stand": dict(site_rule="raw"),
    "every tablet code read through the map": dict(site_rule="map"),
    "paper codes joined as they stand": dict(paper_rule="raw"),
    "every slip at once": dict(member=False, replay=False, resubmit=False, late=False, blank=False,
                               submitted_only=False, site_rule="raw", paper_rule="raw"),
}


def ok(cond, label):
    assert cond, label
    N[0] += 1


def _pdf_text(path):
    from pypdf import PdfReader
    return " ".join(" ".join(pg.extract_text().split()) for pg in PdfReader(path).pages)


def _docx_text(path):
    import docx
    return " ".join(p.text for p in docx.Document(path).paragraphs)


def variant(D, **kw):
    sr = kw.pop("site_rule", "switch")
    pr = kw.pop("paper_rule", "map")
    R = E.resolve(D, E.counted(D, **kw), site_rule=sr, paper_rule=pr)
    R, rep = E.population(R)
    return R, rep


def stays(lam):
    return E.verdict(np.abs(lam))


# ------------------------------------------------------------------ the clean truth: each member's own answers
def clean(W):
    """one return per responding member (their first), every item answered, the member's true September team"""
    first = {}
    for r in W.rets:
        if r.get("blank"):
            continue
        m = r["member"]
        if m not in first or r["time"] < first[m]["time"]:
            first[m] = r
    ms = sorted(first)
    Y = np.array([first[m]["scored"] for m in ms], dtype=float)
    g = W.m_team[np.array(ms)]
    cnt = np.bincount(g, minlength=W.T)
    keep = cnt[g] >= 5
    return Y[keep], g[keep]


def run(target, golden, o, X):
    W, Rc = o["W"], o["R"]
    D, R = X["D"], X["R"]
    lam = X["lam"]
    gold = stays(X["golden"])
    golden_set = [c for c in E.ITEM_CODES if c not in C_ITEMS]
    ok(gold == golden_set, "golden: ten items stay, TC11 and TC12 withdrawn (%s)" % gold)

    # ---------------------------------------------------------------- R1: the field's raw material ships
    for f in os.listdir(target):
        if f.endswith(".csv"):
            cols = pd.read_csv(os.path.join(target, f), nrows=1).columns
            ok(not any(re.search(r"loading|icc|team_mean|between|within|factor", c, re.I) for c in cols),
               "R1 no shipped column holds a loading, an ICC, a team mean or a variance part (%s)" % f)
    ok(len(D["answers"]) > 100000 and "response" in D["answers"].columns,
       "R1 member-level answers ship, one row per question per session")
    ok(R["used"].sum() > 8 * len(X["reported"]),
       "R1 the check reads member returns, several per team, not team summaries")

    # ---------------------------------------------------------------- R3: the analyst test on the clean truth
    Yc, gc = clean(W)
    cl = {h: E.loadings(Yc, gc, h) for h in ("pooled", "within", "means", "means_w", "disatt", "muml_paf",
                                             "muml_ml", "crosshalf")}
    ok(stays(cl["means"]) == [c for c in E.ITEM_CODES if c not in B_ITEMS + C_ITEMS],
       "R3a the easy route on the clean truth (one factor on team means) files eight items (%s)" % stays(cl["means"]))
    ok(stays(cl["muml_paf"]) == golden_set and stays(cl["muml_ml"]) == golden_set,
       "R3b the decisive step alone (between-team covariance net of the pooled within-team covariance) files the ten")
    ok(len(stays(cl["pooled"])) < 4 and len(stays(cl["within"])) < 4,
       "R3b the member-level rungs on the clean truth withdraw most items (%d, %d stay)"
       % (len(stays(cl["pooled"])), len(stays(cl["within"]))))
    ok(stays(cl["disatt"]) != golden_set, "R3b the reliability-corrected team means stay wrong on the clean truth")
    tm = R[R["used"]]
    rows = tm[E.ITEM_CODES].round(0).astype(int).astype(str).agg("".join, axis=1)
    blocks = rows.groupby(tm["team"]).apply(lambda s: s.duplicated().sum()).sum()
    ok(blocks < 0.03 * len(tm), "R3c no copied block: identical answer rows within a team are rare (%d)" % blocks)

    # ---------------------------------------------------------------- the rungs on the cut pack
    means_routes = ["means", "means_pca", "means_w", "means_n10", "blup"]
    for h in means_routes:
        ok(stays(lam[h]) == [c for c in E.ITEM_CODES if c not in B_ITEMS + C_ITEMS],
           "rung 0 (%s): eight items stay, TC09 to TC12 withdrawn" % h)
        b = max(lam[h][E.ITEM_CODES.index(c)] for c in B_ITEMS)
        need = 0.05 if h == "means" else 0.0
        ok(b < E.LINE - need, "rung 0 (%s): the practice items sit under the line by %.2f or more (%.3f)" % (h, need, b))
        ok(stays(lam[h]) != golden_set, "rung 0 (%s) never files the golden" % h)
    a_min = min(lam["means"][:8])
    ok(a_min >= E.LINE + 0.01, "rung 0: every climate item sits at least 0.01 over the line on team means (%.3f)" % a_min)
    ok(stays(E.loadings(*E.scores(R), "disatt_h")) != golden_set, "rung 2 with the harmonic team size: still wrong")
    ok(stays(lam["disatt"]) != golden_set and any(c not in stays(lam["disatt"]) for c in B_ITEMS),
       "rung 2 (team means corrected for unreliability) withdraws a practice item: %s"
       % [c for c in E.ITEM_CODES if c not in stays(lam["disatt"])])
    ok(len(stays(lam["pooled"])) <= 2 and len(stays(lam["within"])) <= 2,
       "floor rungs: member-level fits withdraw nearly every item")
    for h in E.GOLDEN_ROUTES:
        ok(stays(lam[h]) == golden_set, "golden route %s: ten items stay" % h)
        kept = min(lam[h][E.ITEM_CODES.index(c)] for c in golden_set)
        gone = max(abs(lam[h][E.ITEM_CODES.index(c)]) for c in C_ITEMS)
        ok(kept >= WU.KEEP_BAND and gone < WU.DROP_BAND,
           "golden route %s inside the bands (kept %.3f, withdrawn %.3f)" % (h, kept, gone))
    ok(X["golden"][E.ITEM_CODES.index("TC09")] - lam["means"][E.ITEM_CODES.index("TC09")] > 0.2
       and X["golden"][E.ITEM_CODES.index("TC10")] - lam["means"][E.ITEM_CODES.index("TC10")] > 0.2,
       "the decisive move lifts both practice items by more than 0.2")

    # ---------------------------------------------------------------- R2: every Layer 1 slip leaves the call and the rung
    for name, kw in SLIPS.items():
        Rv, rep = variant(D, **dict(kw))
        Y, g = E.scores(Rv)
        lg = E.loadings(Y, g, "muml_paf")
        lm = E.loadings(Y, g, "means")
        ok(stays(lg) == golden_set, "R2 %s: the call stays at ten" % name)
        ok(stays(lm) != golden_set and all(c not in stays(lm) for c in B_ITEMS),
           "R2 %s: the default path still withdraws the practice items" % name)
        kept = min(abs(lg[E.ITEM_CODES.index(c)]) for c in golden_set)
        gone = max(abs(lg[E.ITEM_CODES.index(c)]) for c in C_ITEMS)
        ok(kept >= WU.KEEP_BAND and gone < WU.DROP_BAND, "R2 %s: the components stay inside their bands" % name)

    # ---------------------------------------------------------------- semantic forks on the main call
    Y, g = E.scores(R)
    d = E.decompose(Y, g)
    SigB = (d["SB"] - d["SPW"]) / d["c"]
    staff = pd.read_csv(os.path.join(target, X["files"]["staff"])).set_index("team_code")["staff_in_post"]
    nt = staff.reindex(sorted(set(g))).values
    fin = SigB + d["SPW"] * np.mean(1.0 / nt)
    SF1 = stays(E.paf(fin))
    ok(SF1 != golden_set and stays(E.paf(SigB)) == golden_set,
       "SF1 the team level read as the mean of the team's current staff files another call (%d stay), ruled out by "
       "4.1 (a level that stays the same as staff come and go)" % len(SF1))
    tot = np.sqrt(np.diag(SigB) / (np.diag(SigB) + np.diag(d["SPW"])))
    ok(len(stays(E.paf(SigB) * tot)) == 0, "SF2 loadings standardised on the whole answer withdraw every item, ruled out "
                                           "by 4.2's standardisation across teams")
    w, v = np.linalg.eigh(SigB / np.sqrt(np.outer(np.diag(SigB), np.diag(SigB))))
    two = v[:, -2:] * np.sqrt(w[-2:])
    from numpy.linalg import svd
    # varimax of the two-factor solution: the climate factor is the one the practice items load on
    def varimax(L, it=200):
        p, k = L.shape
        Rm = np.eye(k)
        for _ in range(it):
            Lr = L @ Rm
            u, s, vt = svd(L.T @ (Lr ** 3 - Lr @ np.diag(np.diag(Lr.T @ Lr)) / p))
            Rm = u @ vt
        return L @ Rm
    rot = varimax(two)
    clim = np.argmax(np.abs(rot[E.ITEM_CODES.index("TC09")]))
    lc = np.abs(rot[:, clim])
    ok(all(lc[E.ITEM_CODES.index(c)] < 0.4 for c in C_ITEMS) and all(lc[:10] > 0.75),
       "SF3 a second team-level factor leaves TC11 and TC12 off the climate factor: same call")
    ok(all(abs(x - E.LINE) > 0.05 for x in X["golden"]), "SF4 no item within 0.05 of the 0.75 line: inclusive or not, "
                                                           "same call")
    cnt = R[R["complete"] & R["team"].notna()].groupby("team").size()
    rep5 = set(cnt[cnt >= 5].index)
    Rv = R.copy()
    Rv["used"] = Rv["team"].isin(rep5) & Rv["complete"]
    Y5, g5 = E.scores(Rv)
    ok(stays(E.loadings(Y5, g5, "muml_paf")) == golden_set, "SF5 teams counted on complete returns: same call")
    pr = R[R["reported"]]
    Yp = pr[E.ITEM_CODES].values.astype(float)
    gp = pr["team"].values
    mask = ~np.isnan(Yp)
    J = Yp.shape[1]
    S_pw, S_b = np.zeros((J, J)), np.zeros((J, J))
    for a in range(J):
        for b in range(J):
            mm = mask[:, a] & mask[:, b]
            dd = E.decompose(np.column_stack([Yp[mm, a], Yp[mm, b]]), gp[mm])
            sb = (dd["SB"] - dd["SPW"]) / dd["c"]
            S_b[a, b] = sb[0, 1] if a != b else sb[0, 0]
    ok(stays(E.paf((S_b + S_b.T) / 2)) == golden_set, "SF6 pairwise returns instead of complete ones: same call")
    Yb = (Y >= 4).astype(float)
    ok(stays(E.loadings(Yb, g, "muml_paf")) == golden_set, "SF7 answers scored favourable or not: same call")
    ok(True, "SF8 the bureau's marks more than one box and no mark scored as answers: same call (asserted in R2)")
    ok(True, "SF9 a member's returns across channels: same call (asserted in R2)")
    ok(True, "SF10 a tablet's re-sent session: same call (asserted in R2)")
    ok(True, "SF11 July codes and the reissued codes, however joined: same call (asserted in R2)")
    for h in ("muml_paf", "muml_ml", "muml_pca"):
        ok(stays(lam[h]) == golden_set, "SF12 one-factor estimator %s: same call" % h)
    for h in ("unweighted", "crosshalf"):
        ok(stays(lam[h]) == golden_set, "SF13 between-team covariance estimator %s: same call" % h)
    sub = D["sessions"][D["sessions"]["status"] == "submitted"]
    ok(sub["submitted_utc"].max() < "2027-10-04T20:59:59Z",
       "SF14 the close read in UK time or in UTC: no submission within two hours of either, same returns, same call")
    late = pd.to_datetime(D["paper"]["scanned_at"]).dt.date > __import__("datetime").date(2027, 10, 8)
    ok(late.sum() > 0, "SF15 late forms exist in the scan file")
    ok(True, "SF15 the survey's returns with late forms kept: same call (asserted in R2)")
    ok(stays(-X["golden"]) == golden_set, "SF16 loadings read as magnitudes: same call")

    # ---------------------------------------------------------------- the files the call reads: the shipped bytes
    sha = lambda b: hashlib.sha256(b).hexdigest()
    F = X["files"]
    for k in ("standard", "sessions", "packs", "register", "reorg", "tablets", "staff", "items26", "close"):
        ok(sha(open(os.path.join(target, F[k]), "rb").read()) == SHIPPED[F[k]],
           "shipped bytes: %s is the 10-17 file" % F[k])
    raw = pd.read_csv(os.path.join(target, F["answers"]), dtype=str, keep_default_na=False)
    ok(sha(XP.platform_codes(raw).to_csv(index=False, lineterminator="\n").encode()) == SHIPPED[F["answers"]],
       "shipped bytes: the platform's export, its tags and labels read back to codes, is the 10-17 file")
    raw = pd.read_csv(os.path.join(target, F["paper"]), dtype=str, keep_default_na=False)
    ok(sha(XP.bureau_codes(raw).to_csv(index=False, lineterminator="\n").encode()) == SHIPPED[F["paper"]],
       "shipped bytes: the bureau's file, its tags, labels and clock-named column read back, is the 10-17 file")
    gone = {"README.md", "DATA_DICTIONARY.md", "lfp_staff_voice_2027_codebook.xlsx"}
    now = set(os.listdir(target))
    ok(not gone & now and now - set(SHIPPED) == {F["plans"]},
       "the pack: the readme, the dictionary and the codebook gone, the plans export the one new file")
    lam_call = E.loadings(*E.scores(E.call(target, F)[1]), "muml_paf")
    ok(np.allclose(lam_call, X["golden"]), "separation: the call computed from its own files alone is the golden")
    ok(F["plans"] not in [F[k] for k in B.CALL_FILES], "separation: the call reads no plans row")

    # ---------------------------------------------------------------- the plans ask: the device, its forcing, its stops
    pl = E.read_plans(os.path.join(target, F["plans"]))
    rep = X["reported"]
    pages = PL.team_pages(R, rep)
    ok(set(pl["team_code"]) <= set(rep), "plans: every plan is a reported team's")
    ok(pl.groupby("plan_ref")["team_code"].nunique().max() == 1
       and pl.groupby("team_code")["plan_ref"].nunique().max() == 1,
       "plans: one plan per team, its versions under one reference")
    tcols = ["target_1", "target_2", "target_3"]
    isnum = lambda v: isinstance(v, (int, float, np.integer, np.floating)) and v == v
    pre = pl["saved_at_local"] < pd.Timestamp(PL.RELEASE)
    num = pl[tcols].map(isnum)
    txt = pl[tcols].map(lambda v: isinstance(v, str))
    ok(num[pre].any(axis=1).all() and not txt[pre].values.any(), "plans: every target saved before the release is a number")
    ok(txt[~pre].any(axis=1).all() and not num[~pre].values.any(), "plans: every target saved from the release is a code")
    ok(all(1 <= int(v) <= 12 for v in pl[tcols].values[num.values]), "plans: every number is a row of a twelve-item page")
    last = pl.sort_values(["plan_ref", "version"]).drop_duplicates("plan_ref", keep="last")
    ok((last["status"] != "Replaced").all() and (pl.drop(last.index)["status"] == "Replaced").all(),
       "plans: the latest version of each plan is the only one not replaced")
    newest = pl.groupby("plan_ref")["saved_at_local"].max()
    ok((last.set_index("plan_ref")["saved_at_local"] == newest.reindex(last["plan_ref"])).all(),
       "plans: the latest version is the last saved")
    # the forcing: plans first saved before the release and saved again after it
    rows_items = lambda r: sorted(pages[r["team_code"]][int(v) - 1] for v in r[tcols] if isnum(v))
    nums_items = lambda r: sorted("TC%02d" % int(v) for v in r[tcols] if isnum(v))
    codes = lambda r: sorted(v for v in r[tcols] if isinstance(v, str))
    pairs = same_rows = same_nums = one_off = 0
    for ref, grp in pl.sort_values("version").groupby("plan_ref"):
        g0 = grp[grp["saved_at_local"] < pd.Timestamp(PL.RELEASE)]
        g1 = grp[grp["saved_at_local"] >= pd.Timestamp(PL.RELEASE)]
        if len(g0) and len(g1):
            pairs += 1
            a_r, a_n, b = rows_items(g0.iloc[-1]), nums_items(g0.iloc[-1]), codes(g1.iloc[0])
            same_rows += a_r == b
            same_nums += a_n == b
            one_off += a_r != b and len(a_r) == len(b) and len(set(a_r) & set(b)) == len(b) - 1
    ok(pairs >= 100 and same_rows == pairs and one_off == 0 and same_nums <= 0.05 * pairs,
       "forcing: of %d plans saved before the release and again after it, %d name the same items when the earlier "
       "numbers are read as rows of the team's page; read as item numbers, %d" % (pairs, same_rows, same_nums))
    FORCING.update(pairs=pairs, same_rows=same_rows, one_off=one_off, same_nums=same_nums)

    def low3(frame, read):
        n = h = 0
        for _, r in frame.iterrows():
            for v in r[tcols]:
                if isinstance(v, str):
                    it = v
                elif isnum(v):
                    it = pages[r["team_code"]][int(v) - 1] if read == "rows" else "TC%02d" % int(v)
                else:
                    continue
                n += 1
                h += it in pages[r["team_code"]][:3]
        return h / n
    s_post, s_rows, s_nums = low3(pl[~pre], "rows"), low3(pl[pre], "rows"), low3(pl[pre], "numbers")
    ok(abs(s_post - s_rows) < 0.05 and s_nums < s_post - 0.25,
       "forcing: targets among the team's three lowest items: %.3f from the release, %.3f before it read as page rows, "
       "%.3f read as item numbers" % (s_post, s_rows, s_nums))
    FORCING.update(low3_post=round(s_post, 3), low3_rows=round(s_rows, 3), low3_numbers=round(s_nums, 3))
    # the page order does not turn on how the shown figure is rounded
    fav, base = PL.team_counts(R, rep)
    for mode in ("even", "exact"):
        diff = 0
        for t in rep:
            f_, b_ = fav.loc[t].values, base.loc[t].values
            if mode == "exact":
                vals = [(int(f) / int(b), k) for k, (f, b) in enumerate(zip(f_, b_))]
            else:
                vals = [(float((Decimal(100 * int(f)) / Decimal(int(b))).quantize(Decimal("0.1"),
                                                                                 rounding=ROUND_HALF_EVEN)), k)
                        for k, (f, b) in enumerate(zip(f_, b_))]
            diff += [E.ITEM_CODES[k] for v, k in sorted(vals)] != pages[t]
        ok(diff == 0, "pages: every team's page order is the same with the figure rounded half up or %s (%d differ)"
           % ("half to even" if mode == "even" else "unrounded", diff))
    # the golden is the generator's truth, and every wrong read lands off every figure
    truth = {c: dict(targets=0, agreed=0) for c in E.ITEM_CODES}
    for p in o["plans"]:
        v = p["versions"][-1]
        for it in v["items"]:
            truth[it]["targets"] += 1
            truth[it]["agreed"] += int(v["status"] == "Agreed")
    ok(truth == X["plans"], "plans golden: the file read as the golden reads it gives the generator's own targets")
    flat = lambda d: [d[c][k] for k in ("targets", "agreed") for c in E.ITEM_CODES]
    gold = flat(X["plans"])
    stops = {"the cracker: each plan's latest version, a number read as the item it numbers in Table 1": ("number", False),
             "each plan's latest version, numbers dropped": ("drop", False),
             "every version counted, a number read as the item it numbers": ("number", True),
             "every version counted, numbers dropped": ("drop", True),
             "a number read as a row of the company page": ("company", False)}
    for name, (read, every) in stops.items():
        got = flat(E.plan_targets(dict(plans=pl), R, rep, read=read, every=every))
        gap = min(abs(a_ - b_) for a_, b_ in zip(got, gold))
        ok(gap >= (8 if read == "number" and not every else 5),
           "stop, %s: every one of the 24 plan figures off, by %d or more" % (name, gap))
        STOPS[name] = got
    ok(all(v > 0 for v in gold) and len(set(gold[:12])) == 12, "realism: every item targeted, the item counts distinct")
    ok(sum(gold[:12]) % 10 != 0, "realism: the targets total is not round (%d)" % sum(gold[:12]))
    ok(0.5 < len(last) / len(rep) < 0.8, "realism: about two thirds of reported teams have a plan (%d of %d)"
       % (len(last), len(rep)))
    ok(pl["saved_at_local"].dt.weekday.max() <= 4 and pl["saved_at_local"].dt.hour.between(8, 17).all(),
       "realism: plans are saved on working days in working hours")
    ok(pl["saved_at_local"].max() < pd.Timestamp(PL.EXPORT), "realism: no plan is saved after the export's own time")
    steps = np.diff(sorted(int(r.split("-")[1]) for r in set(pl["plan_ref"])))
    ok(len(set(steps)) > 1 and steps.min() >= 1, "realism: plan references are no arithmetic sequence (gaps from deleted plans)")
    ok(1 < pl["version"].max() and (pl["status"] == "Agreed").sum() < len(last) and len(set(pl["status"])) == 4,
       "realism: versions, the agreed share and the four statuses vary")
    ok(pre.mean() < 0.5, "realism: the earlier saves are a minority of the export's rows (%.2f)" % pre.mean())
    # the plan figures under every reading of the five reused July codes, personal links read as July codes included
    reused = sorted(set(D["reorg"]["old_code"]) & set(D["register"]["team_code"]) - {""})
    ok(len(reused) == 5, "the reused July codes: %s" % reused)
    readings = {"tablet codes as they stand": dict(site_rule="raw"),
                "every tablet code through the map": dict(site_rule="map"),
                "paper codes as they stand": dict(paper_rule="raw"),
                "every code as it stands": dict(site_rule="raw", paper_rule="raw")}
    for name, kw in readings.items():
        Rv, repv = variant(D, **dict(kw))
        ok(set(pl["team_code"]) <= set(repv) and E.plan_targets(dict(plans=pl), Rv, repv) == X["plans"],
           "plans under the reused codes read as %s: every plan's team reported, the 24 figures unchanged" % name)
    Rv = R.copy()
    Rv.loc[Rv["code"].isin(reused), "team"] = None
    Rv, repv = E.population(Rv)
    lost = sorted(set(pl["team_code"]) - set(repv))
    ok(all(not isnum(v) for v in last[last["team_code"].isin(lost)][tcols].values.ravel())
       and E.plan_targets(dict(plans=pl[~pl["team_code"].isin(lost)]), Rv, repv) == E.plan_targets(
           dict(plans=pl[~pl["team_code"].isin(lost)]), R, rep),
       "plans with every reused code read as its July team: the %d plans whose team is then unreported are code-held "
       "(no page needed) and every other plan reads the same" % len(lost))
    # drafts: the note files that a plan stands from the leader's first save; without it the targets would move
    nodraft = E.plan_targets(dict(plans=pl[pl["status"] != "Draft"]), R, rep)
    ok(sum(nodraft[c]["targets"] != X["plans"][c]["targets"] for c in E.ITEM_CODES) >= 10
       and all(nodraft[c]["agreed"] == X["plans"][c]["agreed"] for c in E.ITEM_CODES),
       "drafts: leaving them out would move the targets and never the agreed counts, so the note's sentence carries it")
    # the loadings at one decimal: every deterministic estimator files the golden; the split-half estimator does not
    for h in WU.FIGURE_ROUTES:
        for c, l in zip(E.ITEM_CODES, lam[h]):
            one_ = WU.one_decimal(l)
            if c in golden_set:
                edge = 0.05 - abs(l - 0.9)
                EDGE[0] = min(EDGE[0], edge)
                ok(one_ == 0.9 and edge >= 0.008,
                   "loading at one decimal, %s, %s: 0.9, %.3f from the nearer edge of its bin (%.3f)" % (h, c, edge, l))
            else:
                ok(WU.WITHDRAWN_1DP[0] <= one_ <= WU.WITHDRAWN_1DP[1] and abs(l) < WU.DROP_BAND,
                   "loading at one decimal, %s, %s: inside the withdrawn band, either sign (%.3f)" % (h, c, l))
    splits = np.array([E.paf(E.crosshalf(Y, g, seed=s)) for s in range(20)])
    ok(np.abs(splits[:, 10:]).max() < WU.DROP_BAND and splits[:, :10].min() >= WU.KEEP_BAND,
       "the split-half estimator over 20 splits keeps the call and both bands (kept %.3f to %.3f, withdrawn under %.3f), "
       "its own split noise wider than one decimal" % (splits[:, :10].min(), splits[:, :10].max(),
                                                         np.abs(splits[:, 10:]).max()))
    # each distractor deleted: the golden and every ask unchanged
    import shutil
    import tempfile
    for k in B.DISTRACTORS:
        tmp = tempfile.mkdtemp(dir=os.environ.get("TMPBUILD"))
        for f in os.listdir(target):
            if f != F[k]:
                shutil.copy(os.path.join(target, f), tmp)
        Xd = E.solve(tmp, {kk: vv for kk, vv in F.items() if kk != k})
        shutil.rmtree(tmp)
        ok(Xd["stay"] == X["stay"] and np.allclose(Xd["golden"], X["golden"]) and Xd["plans"] == X["plans"],
           "distractor %s deleted: the call, its loadings and the plan figures unchanged" % F[k])

    # ---------------------------------------------------------------- documents and pins
    std = _pdf_text(os.path.join(target, F["standard"]))
    ok("a member of the team is expected to give" in std and std.count("0.75") == 2,
       "the standard files the team level once and the line in 4.3 only")
    ok("five or more returns that count" in std, "the standard files the reporting floor")
    ok("the return received last counts" in std, "the standard files the member rule")
    ok(not re.search(r"team mean|between-team|within-team|pooled|multilevel|two-level|MUML", std, re.I),
       "the standard names no estimator")
    note = _docx_text(os.path.join(target, F["note"]))
    ok("lowest figure to its highest" in note and "in the order of Table 1" in note and "replaces the earlier one" in note,
       "the dashboard note files the page order, its ties and the plan a team holds")
    ok("holds a plan from the leader's first save" in note and "a draft until the leader sends it" in note
       and "agreed once they have" in note, "the dashboard note files that a draft is a plan, and what agreed means")
    ok(not re.search(r"\brows?\b|release|8 November|item code|number", note, re.I),
       "the dashboard note says nothing of how the plans module saves a target")
    ok("factor" not in note and "loading" not in note, "the dashboard note carries nothing the call reads")
    close = _docx_text(os.path.join(target, F["close"]))
    ok(not re.search(r"twice|duplicate|team list|re-sent|resent|sync", close, re.I), "the close-out narrates no device")

    # ---------------------------------------------------------------- input gates and realism
    files = os.listdir(target)
    ok(len(files) >= 10 and len({f.rsplit(".", 1)[1] for f in files}) >= 3, "input gates: files and formats")
    big = max(sum(1 for _ in open(os.path.join(target, f))) for f in files if f.endswith(".csv"))
    ok(big >= 25000, "input gates: a file of 25,000 rows or more (%d)" % big)
    meta = json.load(open(os.path.join(os.path.dirname(HERE), "metadata.json")))
    ok(len(meta["distractor_files"]) >= 2, "input gates: two distractors declared")
    for f in meta["distractor_files"]:
        ok(not re.search("distract", f), "distractor %s not named as one" % f)
    ok("0.75" not in meta["subdomain"] and "0.75" not in meta["prompt_shape"], "metadata: no line figure in the shape")
    ok(sorted(os.listdir(golden)) == sorted(["lfp_tci_items_2028.pptx", "lfp_tci_structure_check_2027.xlsx"]),
       "golden: the two deliverables")
    S = D["sessions"]
    ok(S["session_id"].is_unique and S["started_utc"].min() >= "2027-09-06T07:00:00Z", "sessions start at the opening")
    sub = S[S["status"] == "submitted"]
    ok(sub["submitted_utc"].max() <= "2027-10-04T22:59:59Z", "no submission after the close")
    gap = S[(S["link_type"] == "site") & (S["started_utc"] >= "2027-09-13T05:00:00Z")
            & (S["started_utc"] < "2027-09-13T06:20:00Z")]
    ok(len(gap) == 0, "no tablet session while the tablets were offline on 13 September")
    return N[0]
