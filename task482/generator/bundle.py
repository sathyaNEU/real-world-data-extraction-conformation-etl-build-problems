"""Read the cut pack the way an analyst would and run every route the design names on it. Nothing here reads
world.py's truth; golden.py, checks.py, verify.py and ceiling.py all go through it.

    load(target)                      the bank, the forms, both platforms' attempts and responses conformed, the
                                      score reports, the crosswalk, the centres and the session review log
    responses(b, which)               the 2026 item responses as arrays (attempt, item, position, score)
    fit_position(b, method, which)    the Rasch position term (logits per position) and the free difficulties
    expected(b, theta, gamma, route)  Form 27A's expected raw score at an ability
    placement_scores(b, gamma, route) the two placement scores
    colleges(b, persons, college, sessions)  each college's 2026 placements, students placed and second sittings"""
import csv
import datetime as dt
import math
import os

import numpy as np

FILES = {
    "report": "qpi_technical_report_2027.pdf",
    "policy": "bpccs_mathematics_placement_policy_4-12.pdf",
    "pool": "itemstore_assembly_pool_2027-02-03.csv",
    "map27": "qpi_form_27A_assembly.csv",
    "layout26": "qpi_forms_26A_26B_layout.csv",
    "kts": "kts_qpi_attempts_2026-03-01_to_2026-06-30.csv",
    "ng_att": "northgate_attempts_2026-07-01_to_2027-01-31.csv",
    "ng_resp": "northgate_item_responses_2026-07-01_to_2027-01-31.csv",
    "reports": "qpi_score_reports_2026-03-01_to_2027-01-31.csv",
    "review": "qpi_session_review_log_2026.xlsx",
    "xwalk": "kts_to_northgate_student_crosswalk.csv",
    "centres": "qpi_testing_centres.csv",
}
STANDARDS = {"CA": 0.20, "CCA": -0.70}       # QPI-TR-2027 section 6
FT_POSITIONS = (61, 70)                      # QPI-TR-2027 section 3: the old platform's field-test section
FORM27_POSITIONS = (21, 70)                  # QPI-TR-2027 section 3: unique and field-test items shuffled
WINDOW = (dt.date(2026, 3, 1), dt.date(2027, 1, 31))
LEVEL_KTS = {"131": "CA", "131C": "CCA", "091": "DM"}
RANK = {"DM": 0, "CCA": 1, "CA": 2}
CODES = ["%02d" % i for i in range(1, 15)]


def _csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def logit(bu):
    return (float(bu) - 500.0) / 100.0


def central_offset(d):
    y = d.year
    m3 = dt.date(y, 3, 8)
    s = m3 + dt.timedelta(days=(6 - m3.weekday()) % 7)
    n1 = dt.date(y, 11, 1)
    e = n1 + dt.timedelta(days=(6 - n1.weekday()) % 7)
    return 5 if s <= d < e else 6


def to_local(z):
    t = dt.datetime.strptime(z, "%Y-%m-%dT%H:%M:%SZ")
    for off in (5, 6):
        loc = t - dt.timedelta(hours=off)
        if central_offset(loc.date()) == off:
            return loc
    return t - dt.timedelta(hours=6)


def mdy(s):
    m, d, y = s.split("/")
    return dt.date(int(y), int(m), int(d))


def slot_of(t):
    """The session an attempt started in: sessions start at 09:00, 13:00 and 17:30 and attempts begin within minutes."""
    return "17:30" if t.hour >= 17 else ("13:00" if t.hour >= 12 else "09:00")


def load(target):
    f = lambda k: os.path.join(target, FILES[k])
    b = {}
    b["pool"] = {r["item_id"]: dict(r, logit=logit(r["difficulty_bu"])) for r in _csv(f("pool"))}
    m27 = _csv(f("map27"))
    b["anchors27"] = [(r["item_id"], int(r["position"])) for r in m27 if r["section"] == "anchor"]
    b["unique27"] = [r["item_id"] for r in m27 if r["section"] == "unique"]
    lay = _csv(f("layout26"))
    b["key"] = {r["item_id"]: r["key"] for r in lay}
    b["kts_item"] = {r["kts_item"]: r["item_id"] for r in lay if r["kts_item"]}
    pos = {}
    for r in lay:
        forms = [r["form"]] if r["form"] in ("26A", "26B") else ["FT%s" % r["form"].split("-")[1]]
        for fm in forms:
            for v, col in (("A", "kts_position_version_A"), ("B", "kts_position_version_B")):
                pos[(fm, v, int(r[col]))] = r["item_id"]
    b["kts_pos"] = pos
    b["anchor_ids"] = sorted(i for i, r in b["pool"].items() if r["status"] == "anchor")
    cen = _csv(f("centres"))
    b["centre_college"] = {r["centre"]: r["college"] for r in cen}
    b["site_centre"] = {r["kts_site"]: r["centre"] for r in cen}
    xw = {(r["kts_college"], r["kts_student_no"]): r["northgate_student_id"] for r in _csv(f("xwalk"))}
    atts = []
    for r in _csv(f("kts")):
        d = mdy(r["test_date"])
        hh, mm = r["start"].split(":")
        start = dt.datetime(d.year, d.month, d.day, int(hh), int(mm))
        centre = b["site_centre"][r["site"]]
        atts.append(dict(key=r["attempt_id"], platform="old", form=r["form"], version=r["version"],
                         ft_set=int(r["ft_set"]), start=start, date=d, centre=centre,
                         session=(centre, d, slot_of(start)), college=r["college"],
                         sid=xw.get((r["college"], r["student_no"])), kts_id=(r["college"], r["student_no"]),
                         dob=mdy(r["birth_date"]), sex=r["sex"], hs=r["hs_code"], registered=mdy(r["registered"]),
                         raw=int(r["raw_score"]), level=LEVEL_KTS[r["placement"]], responses=r["responses"]))
    for r in _csv(f("ng_att")):
        start = to_local(r["started_at"])
        c, dstr, hm = r["session_ref"][1:].split("-")
        sess = ("TC" + c, dt.date(int(dstr[:4]), int(dstr[4:6]), int(dstr[6:])), hm[:2] + ":" + hm[2:])
        atts.append(dict(key=r["attempt_ref"], platform="new", form=r["form"], version="", ft_set=int(r["ft_set"]),
                         start=start, date=start.date(), centre=r["centre"], session=sess, college=r["college"],
                         sid=r["student_id"], kts_id=None, dob=dt.date.fromisoformat(r["birth_date"]), sex=r["sex"],
                         hs=r["hs_code"], registered=dt.date.fromisoformat(r["registered"]), raw=int(r["raw_score"]),
                         level=r["placement"]))
    atts.sort(key=lambda a: (a["start"], a["key"]))
    b["attempts"] = atts
    b["by_key"] = {a["key"]: a for a in atts}
    reps = {}
    for r in _csv(f("reports")):
        reps.setdefault(r["attempt"], []).append(r)
    b["reports"] = reps
    b["review"] = review_log(f("review"))
    return b


def review_log(path):
    import openpyxl
    ws = openpyxl.load_workbook(path, read_only=True).active
    rows = [r for r in ws.iter_rows(min_row=5, values_only=True) if r and r[0]]
    out = []
    for logged, centre, sdate, sstart, plat, ref, decision, n, note in rows:
        sd = sdate.date() if isinstance(sdate, dt.datetime) else sdate
        out.append(dict(logged=logged, session=(centre, sd, str(sstart)), decision=decision))
    return out


def invalid_sessions(b, withdrawals=True):
    state = {}
    for r in sorted(b["review"], key=lambda r: r["logged"]):
        if r["decision"] == "Attempts invalidated":
            state[r["session"]] = True
        elif r["decision"] == "Invalidation withdrawn" and withdrawals:
            state[r["session"]] = False
    return {s for s, v in state.items() if v}


# ------------------------------------------------------------------ the 2026 responses
def responses(b, which="all", target=None):
    """Arrays over every 2026 response: attempt index, item id index, delivered position, score. which: all, valid,
    old or new. The old platform's responses are scored against the layout's keys at the positions its version
    gives; the new platform's carry their position (seq) and score."""
    cache = b.setdefault("_resp", {})
    if which in cache:
        return cache[which]
    bad = invalid_sessions(b)
    keep = []
    for i, a in enumerate(b["attempts"]):
        if which == "valid" and a["session"] in bad:
            continue
        if which in ("old", "new") and a["platform"] != which:
            continue
        keep.append(i)
    keepset = set(keep)
    A, I, X, Y = [], [], [], []
    items = {}

    def idx(iid):
        if iid not in items:
            items[iid] = len(items)
        return items[iid]
    for i in keep:
        a = b["attempts"][i]
        if a["platform"] != "old":
            continue
        for p in range(1, 71):
            fm = a["form"] if p <= 60 else "FT%d" % a["ft_set"]
            iid = b["kts_pos"][(fm, a["version"], p)]
            ch = a["responses"][p - 1]
            A.append(i)
            I.append(idx(iid))
            X.append(p)
            Y.append(1 if ch == b["key"][iid] else 0)
    if which != "old":
        tgt = b.get("_target")
        with open(os.path.join(tgt, FILES["ng_resp"]), newline="", encoding="utf-8") as fh:
            rd = csv.reader(fh)
            next(rd)
            att_index = {a["key"]: i for i, a in enumerate(b["attempts"])}
            for ref, iid, seq, resp, score, rt, served in rd:
                i = att_index[ref]
                if i not in keepset:
                    continue
                A.append(i)
                I.append(idx(iid))
                X.append(int(seq))
                Y.append(int(score))
    out = dict(A=np.array(A), I=np.array(I), X=np.array(X, float), Y=np.array(Y, float),
               items=sorted(items, key=items.get))
    cache[which] = out
    return out


def _L(x):
    return 1.0 / (1.0 + np.exp(-x))


def fit_position(b, method="mml", which="all", nodes=41, positions=None):
    """The Rasch model with a position term, the anchor block fixed at its bank difficulties (it sat in place when
    calibrated, as on every form) and every other item's difficulty free: logit P = theta - d_i - gamma * position.
    method: mml (normal ability, Gauss-Hermite EM), jml, or marginal (no ability term: a population-averaged slope).
    positions (jml only): keep the free items' responses at positions lo to hi. Returns gamma in logits per position."""
    r = responses(b, which)
    ids = r["items"]
    nI = len(ids)
    anchor = np.array([i in b["pool"] and b["pool"][i]["status"] == "anchor" for i in ids])
    bank = np.array([b["pool"][i]["logit"] if anchor[k] else 0.0 for k, i in enumerate(ids)])
    A, I, X, Y = r["A"], r["I"], r["X"], r["Y"]
    att, inv = np.unique(A, return_inverse=True)
    N = len(att)
    Xc = np.where(anchor[I], 0.0, X)
    if method == "marginal":
        m = ~anchor[I]
        Iv, Xv, Yv = I[m], X[m], Y[m]
        bi, g = np.zeros(nI), 0.0
        for _ in range(80):
            p = _L(-(bi[Iv] + g * Xv)); w = p * (1 - p); res = Yv - p
            bi += np.bincount(Iv, -res, nI) / np.maximum(np.bincount(Iv, w, nI), 1e-9)
            p = _L(-(bi[Iv] + g * Xv)); w = p * (1 - p); res = Yv - p
            xc = Xv - np.bincount(Iv, w * Xv, nI)[Iv] / np.maximum(np.bincount(Iv, w, nI)[Iv], 1e-9)
            g += np.sum(-res * xc) / np.sum(w * xc * xc)
        return float(g)
    if method == "jml":
        if positions:
            k = anchor[I] | ((X >= positions[0]) & (X <= positions[1]))
            I, X, Y, Xc, inv = I[k], X[k], Y[k], Xc[k], inv[k]
        th = np.zeros(N); bfree = bank.copy(); g = 0.0; m = ~anchor[I]
        for _ in range(400):
            d = bfree[I] + g * Xc; p = _L(th[inv] - d); w = p * (1 - p); res = Y - p
            th += np.clip(np.bincount(inv, res, N) / np.maximum(np.bincount(inv, w, N), 1e-9), -1, 1)
            d = bfree[I] + g * Xc; p = _L(th[inv] - d); w = p * (1 - p); res = Y - p
            u = np.bincount(I, -res, nI) / np.maximum(np.bincount(I, w, nI), 1e-9); u[anchor] = 0
            bfree += np.clip(u, -1, 1)
            d = bfree[I] + g * Xc; p = _L(th[inv] - d); w = p * (1 - p); res = Y - p
            xc = Xc - np.bincount(I, w * Xc, nI)[I] / np.maximum(np.bincount(I, w, nI)[I], 1e-9)
            g += np.clip(np.sum(-res[m] * xc[m]) / np.sum(w[m] * xc[m] ** 2), -0.005, 0.005)
        return float(g)
    # MML: rows are attempts; build a dense attempts x 70 layout
    order = np.lexsort((X, inv))
    Ia, Xa, Ya = I[order].reshape(N, -1), Xc[order].reshape(N, -1), Y[order].reshape(N, -1)
    q0, wq = np.polynomial.hermite_e.hermegauss(nodes)
    wq = wq / wq.sum()
    mu, sd = 0.0, 1.0
    bfree = bank.copy()
    g = 0.0
    free = ~anchor
    for _ in range(300):
        q = mu + sd * q0
        d = bfree[Ia] + g * Xa
        lp = np.stack([(Ya * np.log(_L(t - d)) + (1 - Ya) * np.log(1 - _L(t - d))).sum(1) for t in q], 1) + np.log(wq)
        lp -= lp.max(1, keepdims=True)
        post = np.exp(lp)
        post /= post.sum(1, keepdims=True)
        mu = float((post * q).sum(1).mean())
        sd = float(np.sqrt((post * (q[None, :] - mu) ** 2).sum(1).mean()))
        q = mu + sd * q0
        gb = np.zeros(nI); hb = np.zeros(nI); cr = np.zeros(nI); gg = 0.0; hg = 0.0
        for j, t in enumerate(q):
            p = _L(t - d); res = (Ya - p) * post[:, [j]]; w = p * (1 - p) * post[:, [j]]
            gb += np.bincount(Ia.ravel(), (-res).ravel(), nI); hb += np.bincount(Ia.ravel(), w.ravel(), nI)
            cr += np.bincount(Ia.ravel(), (w * Xa).ravel(), nI); gg += float((-res * Xa).sum())
            hg += float((w * Xa * Xa).sum())
        fr = free & (hb > 0)
        hgs = hg - np.sum(cr[fr] ** 2 / hb[fr])
        dg = (gg - np.sum(cr[fr] * gb[fr] / hb[fr])) / hgs
        db = np.zeros(nI)
        db[fr] = (gb[fr] - cr[fr] * dg) / hb[fr]
        bfree += db
        g += dg
        if abs(dg) < 1e-8 and np.abs(db).max() < 1e-7:
            break
    return float(g)


# ------------------------------------------------------------------ Form 27A
def form27(b):
    anc = [(i, p, b["pool"][i]["logit"]) for i, p in b["anchors27"]]
    uni = [(i, b["pool"][i]["logit"]) for i in b["unique27"]]
    return anc, uni


def expected(b, theta, gamma=0.0, route="carried"):
    """Form 27A's expected raw score at theta. route: carried (each unique item from the field-test section's mean
    position to every position it can take on Form 27A, averaged over the shuffle); filed (the bank difficulties as
    they stand); mean_position (each unique item moved to Form 27A's mean position only); all_items (every item,
    the anchor block too, moved by the field-test section's offset); position_one (unique items moved to position 1)."""
    anc, uni = form27(b)
    lo, hi = FORM27_POSITIONS
    ft_mean = (FT_POSITIONS[0] + FT_POSITIONS[1]) / 2.0
    pos = np.arange(lo, hi + 1)
    e = sum(_L(theta - d) for _, _, d in anc)
    if route == "all_items":
        e = sum(_L(theta - (d - gamma * (ft_mean - p))) for _, p, d in anc)
    for _, d in uni:
        if route == "filed" or gamma == 0.0:
            e += _L(theta - d)
        elif route in ("carried", "all_items"):
            e += float(_L(theta - (d - gamma * (ft_mean - pos))).mean())
        elif route == "mean_position":
            e += _L(theta - (d - gamma * (ft_mean - pos.mean())))
        elif route == "position_one":
            e += _L(theta - (d - gamma * (ft_mean - 1)))
    return float(e)


def placement_scores(b, gamma=0.0, route="carried"):
    return {lv: int(math.ceil(expected(b, STANDARDS[lv], gamma, route) - 1e-12)) for lv in ("CA", "CCA")}


def conversion(scores):
    return [(r, "CA" if r >= scores["CA"] else ("CCA" if r >= scores["CCA"] else "DM")) for r in range(61)]


# ------------------------------------------------------------------ the asks
def person_keys(b, how="four_fields"):
    """A person key per attempt. four_fields: birth date, sex, high school code and registration date; ids: the
    old platform's student number through the crosswalk, the new platform's student id as it stands; raw_ids: each
    platform's own identifier; three_fields: birth date, sex and high school code."""
    out = {}
    for a in b["attempts"]:
        if how == "four_fields":
            out[a["key"]] = (a["dob"], a["sex"], a["hs"], a["registered"])
        elif how == "three_fields":
            out[a["key"]] = (a["dob"], a["sex"], a["hs"])
        elif how == "ids":
            out[a["key"]] = a["sid"] if a["sid"] else ("kts",) + a["kts_id"]
        elif how == "raw_ids":
            out[a["key"]] = ("kts",) + a["kts_id"] if a["platform"] == "old" else a["sid"]
    return out


def college_of(b, a, how="reports"):
    """The college that placed the student on this sitting. reports: the automatic score report's college (the
    college the student was registered through when they sat); export: the attempt record's college column;
    centre: the testing centre's college; any_report: every college a report went to (first)."""
    if how == "reports":
        auto = [r for r in b["reports"].get(a["key"], []) if r["report"] == "automatic"]
        return auto[0]["sent_to"]
    if how == "export":
        return a["college"]
    if how == "centre":
        return b["centre_college"][a["centre"]]
    raise ValueError(how)


def colleges(b, persons="four_fields", college="reports", sessions="review", window=True):
    """Each college's students placed (in all, into College Algebra, into Corequisite College Algebra) and of them
    those who sat twice, each student once at the college that placed them on their placing sitting (Policy 4.12)."""
    keys = person_keys(b, persons)
    bad = set() if sessions == "ignore" else invalid_sessions(b, withdrawals=(sessions == "review"))
    groups = {}
    for a in b["attempts"]:
        if a["session"] in bad:
            continue
        if window and not (WINDOW[0] <= a["date"] <= WINDOW[1]):
            continue
        groups.setdefault(keys[a["key"]], []).append(a)
    out = {c: dict(placed=0, CA=0, CCA=0, twice=0) for c in CODES}
    for k in sorted(groups, key=str):
        v = groups[k]
        best = max(v, key=lambda a: (RANK[a["level"]], a["start"]))
        c = college_of(b, best, college)
        out[c]["placed"] += 1
        if best["level"] in ("CA", "CCA"):
            out[c][best["level"]] += 1
        if len(v) >= 2:
            out[c]["twice"] += 1
    return out


def open_pack(target):
    b = load(target)
    b["_target"] = target
    return b
