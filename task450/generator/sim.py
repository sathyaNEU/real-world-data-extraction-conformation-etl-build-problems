"""Simulate Coraza ISD's two grade-5 mathematics administrations and the records around them.

Students answer items under a Rasch model. The 2025 form and the 2026 form share 25 items in the same positions;
the 2026 form's other 25 items are harder, and the 2026 cohort (the first taught the district's new curriculum
from grade 3) is stronger. The new curriculum teaches simplifying numerical expressions a year earlier, so the three
shared items written to that standard are far easier for the 2026 cohort than its ability elsewhere implies. The 2025-26 enrollment history lives in the new student information system, which went
live on 5 January 2026: students then mid-transfer were carried over at their old campus under one new id and
registered at their new campus under another, and the duplicate ids were merged in August 2026."""
import datetime as dt

import numpy as np
from scipy.stats import norm

import world as W

LETTERS = np.array(list("ABCD"))


def _smooth(rng, n, shift, sd=0.9, jit=0.15):
    q = norm.ppf((np.arange(n) + 0.5) / n)
    return rng.permutation(q * sd + shift + rng.normal(0, jit, n))


def forms(rng, hard):
    """Item difficulties and keys for both forms; anchor items sit at the same positions on both."""
    na = len(W.ANCHOR_POS)
    anchor = _smooth(rng, na, 0.0)
    u25 = _smooth(rng, W.N_ITEMS - na, -0.10)
    u26 = _smooth(rng, W.N_ITEMS - na, hard)
    pos_u = [p for p in range(1, W.N_ITEMS + 1) if p not in W.ANCHOR_POS]
    b25 = np.zeros(W.N_ITEMS)
    b26 = np.zeros(W.N_ITEMS)
    for i, p in enumerate(W.ANCHOR_POS):
        b25[p - 1] = b26[p - 1] = anchor[i]
    for i, p in enumerate(pos_u):
        b25[p - 1] = u25[i]
        b26[p - 1] = u26[i]
    # the shared items the new curriculum teaches a year earlier answer far more often for the 2026 cohort
    order = sorted((b25[p - 1], p) for p in W.ANCHOR_POS)
    mid = len(order) // 2
    drift = sorted(p for _, p in order[mid - W.DRIFT_N // 2: mid - W.DRIFT_N // 2 + W.DRIFT_N])
    for p in drift:
        b26[p - 1] = b25[p - 1] - W.DRIFT_LOGITS
    key25 = LETTERS[rng.integers(0, 4, W.N_ITEMS)]
    key26 = key25.copy()
    for p in pos_u:
        key26[p - 1] = LETTERS[rng.integers(0, 4)]
    # item ids: the bank's six-digit numbers; anchors keep theirs
    ids25 = ["M5%05d" % x for x in rng.choice(np.arange(20000, 29999), W.N_ITEMS, replace=False)]
    ids26 = list(ids25)
    new = ["M5%05d" % x for x in rng.choice(np.arange(41000, 47999), len(pos_u), replace=False)]
    for i, p in enumerate(pos_u):
        ids26[p - 1] = new[i]
    return dict(b25=b25, b26=b26, key25=key25, key26=key26, ids25=ids25, ids26=ids26, pos_u=pos_u, drift=drift)


def respond(rng, theta, b, key, nr_rate=0.0):
    """Letter responses: correct with the Rasch probability, otherwise a distractor; a few omits and, for weaker
    students, items not reached at the end of the second session."""
    n, k = len(theta), len(b)
    p = 1.0 / (1.0 + np.exp(-(theta[:, None] - b[None, :])))
    right = rng.random((n, k)) < p
    out = np.empty((n, k), dtype=object)
    for j in range(k):
        others = [x for x in "ABCD" if x != key[j]]
        w = rng.dirichlet(np.ones(3) * 2.5)
        wrong = np.array(others)[rng.choice(3, size=n, p=w)]
        out[:, j] = np.where(right[:, j], key[j], wrong)
    omit = rng.random((n, k)) < 0.006
    out[omit] = ""
    if nr_rate:
        # not reached: the last few items of the second session, more often for weaker students
        pr = nr_rate / (1.0 + np.exp(1.6 * (theta + 0.9)))
        stop = rng.random(n) < pr
        last = rng.integers(1, 6, n)
        for i in np.where(stop)[0]:
            out[i, k - last[i]:] = ""
    multi = rng.random((n, k)) < 0.0015
    out[multi] = "*"
    return out


def score(resp, key):
    return (resp == np.asarray(key)[None, :]).astype(int)


def campuses(rng):
    """Codes and attributes. The legacy system numbered campuses in the order they opened; the new system takes the
    state campus numbers, assigned in name order when the district re-registered its campuses."""
    names = [c for c, _ in W.CAMPUSES]
    # the old system numbered the campuses open in 2024-25 in the order they opened; Vereda opened in August 2025
    old = [c for c in names if c != "Vereda Elementary"]
    legacy = {c: "%03d" % (101 + i) for i, c in enumerate(old)}
    # the new system carries the campus numbers on the state's records (its own stream, so the draws below hold)
    perm = np.random.default_rng(W.SEED + 99).permutation(len(names))
    nums = {c: "%03d" % (101 + int(k)) for c, k in zip(names, perm)}
    community = {c: k for c, k in W.CAMPUSES}
    eff = {"North": 0.18, "Central": 0.05, "East": -0.10, "South": -0.20, "West": 0.06}
    mu = {c: eff[community[c]] + rng.normal(0, 0.36) for c in names}
    size = {c: int(rng.integers(62, 176)) for c in names}
    size["Vereda Elementary"] = 12          # opened in August 2025 with a single grade-5 class
    return dict(names=names, legacy=legacy, new=nums, community=community, mu=mu, size=size)


def _abbrev(name):
    n = name.upper().replace(" ELEMENTARY", " EL")
    for a, b in (("AVENUE", "AVE"), ("STREET", "ST"), ("ROAD", "RD"), ("TERRACE", "TER"), ("CROSSING", "XING"),
                 ("PRAIRIE", "PR"), ("HOLLOW", "HOLW"), ("MEADOW", "MDW"), ("CANYON", "CYN")):
        n = n.replace(a, b)
    return n


def cohort_2025(rng, C, F):
    """Spring 2025 grade-5 test takers on the 2025 form, with the legacy campus code and the vendor's name."""
    rows, th = [], []
    for c in C["names"]:
        n = max(8, int(C["size"][c] * rng.uniform(0.94, 1.05)))
        t = rng.normal(C["mu"][c], 0.95, n)
        th.append(t)
        rows += [c] * n
    theta = np.concatenate(th)
    resp = respond(rng, theta, F["b25"], F["key25"], nr_rate=0.10)
    # a campus that opened in August 2025 had no spring 2025 test takers (its draws are made and set aside, so the
    # stream that follows is unchanged)
    keep = np.array(rows) != "Vereda Elementary"
    return dict(campus=np.array(rows)[keep], theta=theta[keep], resp=resp[keep])


def cohort_2026(rng, C, F, gain):
    """The 2025-26 grade-5 cohort: enrollment spells under the new system's ids, tests in the April window, the
    vendor's test-taker ids, and the duplicate ids the migration made for students moving over the winter break."""
    names = C["names"]
    pick = lambda c: names[int(rng.integers(len(names)))]
    stu = []
    for c in names:
        for _ in range(C["size"][c]):
            stu.append(dict(campus=c, theta=rng.normal(C["mu"][c] + gain, 0.95), spells=[]))
    for s in stu:
        c = s["campus"]
        u = rng.random()
        if u < 0.050:
            # entered after the fall snapshot, from outside the district
            d = W.SNAPSHOT + dt.timedelta(days=int(rng.integers(3, 150)))
            s["spells"] = [(c, d, None)]
            s["kind"] = "late"
        elif u < 0.084:
            # moved between the district's campuses during the year (not over the winter break)
            other = pick(c)
            while other in (c, "Vereda Elementary"):
                other = pick(c)
            d = W.SNAPSHOT + dt.timedelta(days=int(rng.integers(10, 165)))
            while dt.date(2025, 12, 8) <= d <= dt.date(2026, 1, 23):
                d = W.SNAPSHOT + dt.timedelta(days=int(rng.integers(10, 165)))
            s["spells"] = [(other, W.YEAR_START, d - dt.timedelta(days=int(rng.integers(1, 4)))), (c, d, None)]
            s["kind"] = "moved"
        elif u < 0.094:
            # moved over the winter break: withdrew in December, entered the new campus in January
            other = pick(c)
            while other in (c, "Vereda Elementary"):
                other = pick(c)
            out_d = dt.date(2025, 12, int(rng.integers(8, 20)))
            in_d = dt.date(2026, 1, int(rng.integers(6, 24)))
            s["spells"] = [(other, W.YEAR_START, out_d), (c, in_d, None)]
            s["kind"] = "winter"
            # the withdrawal was still pending when the old system's records were converted
            s["pending"] = rng.random() < 0.72
        elif u < 0.118:
            # left the district before the window
            d = W.YEAR_START + dt.timedelta(days=int(rng.integers(20, (W.WINDOW[0] - W.YEAR_START).days - 2)))
            s["spells"] = [(c, W.YEAR_START, d)]
            s["kind"] = "left"
        else:
            s["spells"] = [(c, W.YEAR_START, None)]
            s["kind"] = "stay"
    theta = np.array([s["theta"] for s in stu])
    resp = respond(rng, theta, F["b26"], F["key26"], nr_rate=0.10)
    for s in stu:
        s["tested"] = s["kind"] != "left" and rng.random() > 0.017
    # ids: the new system numbers students on conversion and on registration
    ids = rng.choice(np.arange(2600000, 2699999), size=len(stu) + 400, replace=False)
    nxt = iter(ids)
    merges = []
    for s in stu:
        s["id"] = "%07d" % next(nxt)
        if s["kind"] == "winter" and s["pending"]:
            # converted at the old campus with the withdrawal missing, registered again at the new campus
            old_c, start, _ = s["spells"][0]
            new_c, in_d, _ = s["spells"][1]
            s["ghost"] = "%07d" % next(nxt)
            s["ghost_spell"] = (old_c, start, None)
            s["spells"] = [(new_c, in_d, None)]
            merges.append((s["ghost"], s["id"], dt.date(2026, 8, int(rng.integers(10, 22)))))
    vend = rng.choice(np.arange(10000000, 99999999), size=len(stu) + 400, replace=False)
    vn = iter(vend)
    for s in stu:
        s["vendor"] = "T%08d" % next(vn)
        if "ghost" in s:
            s["ghost_vendor"] = "T%08d" % next(vn)
    return dict(stu=stu, theta=theta, resp=resp, merges=merges)


def _rated(B, F):
    """Per campus as rated for 2026-27: (tested full-academic-year students, at or above 25, at or above 27)."""
    import calc
    sc = calc.score(B["resp"], F["key26"]).sum(1)
    agg = {}
    for i, st in enumerate(B["stu"]):
        if not st["tested"]:
            continue
        c = calc.fay(st["spells"])
        if c is None:
            continue
        for key in (c, "rated:" + calc.rated_campus(c)):
            n, a, b = agg.get(key, (0, 0, 0))
            agg[key] = (n + 1, a + int(sc[i] >= 25), b + int(sc[i] >= 27))
    return agg


def _clear(agg, margin=2.0):
    """Campuses within the margin of the line at either passing raw score, as rated for 2026-27, plus the closed
    campus's and the new campus's conditions."""
    bad = []
    for key, (n, a, b) in agg.items():
        if not key.startswith("rated:") or n < W.N_MIN:
            continue
        c = key[6:]
        if min(abs(a - W.LINE * n), abs(b - W.LINE * n)) < margin:
            bad.append(c)
    closed, into = W.CLOSED
    n, a, b = agg.get(closed, (0, 0, 0))
    if not (n and a <= W.LINE * n - margin):
        bad.append(closed)
    n, a, b = agg.get(into, (0, 0, 0))
    if not (n and a >= W.LINE * n + margin):
        bad.append(into)
    # rated with the closed campus's students, the receiving campus falls under the line
    n, a, b = agg.get("rated:" + into, (0, 0, 0))
    if not (n and a <= W.LINE * n - margin):
        bad.append(into)
    n, a, b = agg.get("Vereda Elementary", (0, 0, 0))
    if not (6 <= n < W.N_MIN and a < W.LINE * n):
        bad.append("Vereda Elementary")
    return sorted(set(bad))


def _redraw(B, F, C, campus, sub, gain):
    rng = np.random.default_rng(sub)
    idx = [i for i, st in enumerate(B["stu"]) if st["campus"] == campus]
    for i in idx:
        B["stu"][i]["theta"] = rng.normal(C["mu"][campus] + gain, 0.95)
    th = np.array([B["stu"][i]["theta"] for i in idx])
    B["resp"][idx] = respond(rng, th, F["b26"], F["key26"], nr_rate=0.10)
    B["theta"][idx] = th
    if campus == "Vereda Elementary":
        # a campus opened in August 2025: some of its first grade-5 students arrived after the fall snapshot
        for j, i in enumerate(idx):
            st = B["stu"][i]
            st["tested"] = True
            if j < 3:
                st["kind"] = "late"
                st["spells"] = [(campus, W.SNAPSHOT + dt.timedelta(days=int(rng.integers(5, 60))), None)]
            elif st["kind"] != "stay":
                st["kind"] = "stay"
                st["spells"] = [(campus, W.YEAR_START, None)]


def _shares_2025(A, F, C):
    import calc
    raw = calc.score(A["resp"], F["key25"]).sum(1)
    out = {}
    for c, r in zip(A["campus"], raw):
        k = C["community"][calc.rated_campus(c)]
        n, m = out.get(k, (0, 0))
        out[k] = (n + 1, m + int(r >= 27))
    return {k: 100.0 * m / n for k, (n, m) in out.items()}


def _shape_2025(A, F, C, seed):
    """Keep each learning community's 2025 share off a round value and clear of a rounding edge, redrawing one of its
    campuses' 2025 test takers when it is not."""
    for tries in range(200):
        bad = [k for k, v in _shares_2025(A, F, C).items()
               if round(v, 1) * 10 % 50 == 0 or abs(v * 10 - round(v * 10)) > 0.3]
        if not bad:
            return
        for k in bad:
            rng = np.random.default_rng(seed * 7919 + tries * 31 + W.COMMUNITIES.index(k))
            cs = [c for c in C["names"] if C["community"][c] == k and c != W.CLOSED[0]]
            c = cs[int(rng.integers(len(cs)))]
            idx = np.where(A["campus"] == c)[0]
            th = rng.normal(C["mu"][c], 0.95, len(idx))
            A["theta"][idx] = th
            A["resp"][idx] = respond(rng, th, F["b25"], F["key25"], nr_rate=0.10)
    raise SystemExit("sim: a 2025 community share stays on a round value or an edge")


def simulate(seed=W.SEED, gain=0.11, hard=0.42):
    rng = np.random.default_rng(seed)
    F = forms(rng, hard)
    C = campuses(rng)
    # the closed campus was small and drew its students from the district's lowest-income streets
    C["mu"][W.CLOSED[0]] = -0.62
    C["size"][W.CLOSED[0]] = 74
    C["mu"][W.CLOSED[1]] = -0.08
    C["size"][W.CLOSED[1]] = 128
    C["size"]["Vereda Elementary"] = 11
    A = cohort_2025(rng, C, F)
    B = cohort_2026(rng, C, F, gain)
    _shape_2025(A, F, C, seed)
    tries = 0
    while True:
        bad = _clear(_rated(B, F))
        if not bad:
            break
        tries += 1
        if tries > 400:
            raise SystemExit("sim: campuses still on the line: %s" % bad)
        for c in bad:
            _redraw(B, F, C, c, seed * 100003 + tries * 101 + C["names"].index(c), gain)
    return dict(F=F, C=C, A=A, B=B, seed=seed, gain=gain, hard=hard, redraws=tries)
