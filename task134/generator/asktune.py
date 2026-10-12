"""Ask-side tuning: small moves to individual residents' assessed contributions (the assessment in force on 31 December
2026 and those after it, or only the reviews completed in advance of January and February 2027, or a merged client's
superseded assessment) and to fee supplements, so that every ask figure sits mid-bin and every designed stop lands
off the golden by its margin. None of these columns or rows is read by the main call."""
import itertools

import numpy as np

import askcalc as AC
import world as W

LOC_I = {l: k for k, l in enumerate(W.LOCS)}
CARE_I = {"Residential": 0, "Nursing": 1}
CHART_TOP = None
CENTRE_W = [10.0]
SUBSETS = [s for n in range(1, 6) for s in itertools.combinations(["primary", "h1", "h2", "h3", "h4"], n)]


def composite(sub):
    kw = {}
    if "primary" in sub:
        kw["group"] = "team"
    if "h1" in sub:
        kw["contrib"] = "latest"
    if "h2" in sub:
        kw["refs"] = "one"
    if "h3" in sub:
        kw["active_only"] = True
    if "h4" in sub:
        kw["fee"] = "schedule"
    return kw


class Fast:
    """numpy form of askcalc.fast over the resident table"""

    def __init__(self, df):
        self.df = df
        n = len(df)
        self.care = np.array([CARE_I[c] for c in df["care"]])
        self.team = np.array([LOC_I[l] for l in df["team"]])
        self.home = np.array([LOC_I[l] if isinstance(l, str) else -1 for l in df["home"]])
        self.homea = np.array([LOC_I[l] if isinstance(l, str) else -1 for l in df["home_active"]])
        self.ptype = df["ptype"].values
        self.dead = df["dead_unread"].values.astype(bool)
        self.cols = {k: df[k].values.astype(float).copy() for k in ("c_in", "c_lat", "c_in1", "c_lat1", "fee", "sched")}
        self.n = n

    def stop(self, group="home", contrib="inforce", refs="all", active_only=False, fee="contract", types=("PERM",),
             use_deaths=True, drop_mismatch=False):
        m = np.isin(self.ptype, types)
        if use_deaths:
            m &= ~self.dead
        hl = self.homea if active_only else self.home
        if drop_mismatch:
            m &= hl == self.team
        loc = hl if group == "home" else self.team
        m &= loc >= 0
        key = loc * 2 + self.care
        col = {("inforce", "all"): "c_in", ("latest", "all"): "c_lat", ("inforce", "one"): "c_in1",
               ("latest", "one"): "c_lat1"}[(contrib, refs)]
        c = self.cols[col]
        f = self.cols["fee"] if fee == "contract" else self.cols["sched"]
        cnt = np.bincount(key[m], minlength=10)
        cs = np.bincount(key[m], weights=c[m], minlength=10)
        ns = np.bincount(key[m], weights=(f - c)[m], minlength=10)
        with np.errstate(invalid="ignore", divide="ignore"):
            return np.ravel(np.column_stack([cs / cnt, ns / cnt]))


def nth_largest(a, n):
    a = np.sort(np.abs(a))[::-1]
    return a[n - 1] if len(a) >= n else 0.0


def score(F, detail=False):
    g = F.stop()
    v = {}
    pen = 0.0
    fr = np.abs(g - np.round(g))
    v["centre"] = np.clip(fr - 0.2, 0, None).sum() * CENTRE_W[0]
    need = {"s1": 1.6, "s2": 1.2, "s3": 1.5, "o1": 1.2, "lazy": 2.1}
    for k, t in need.items():
        d = F.stop(**AC.STOPS[k]) - g
        v[k] = np.clip(t - np.abs(d), 0, None).sum()
    d = (F.stop(**AC.STOPS["s5"]) - g)[1::2]
    v["s5"] = np.clip(1.5 - np.abs(d), 0, None).sum()
    d = F.stop(**AC.STOPS["s4"]) - g
    rer = [LOC_I["Braeburn"], LOC_I["Dunmorrow"]]
    idx = [l * 4 + j for l in rer for j in range(4)]
    v["s4"] = max(0, 1.2 - nth_largest(d[idx], 4))
    for k, n_ in (("crosswalk_one_ref", 6), ("deaths_unread", 2), ("definitions_interim_kept", 10), ("codes_unread", 10),
                  ("assessments_latest", 20)):
        d = F.stop(**AC.NECESSITY[k]) - g
        v[k] = max(0, 1.0 - nth_largest(d, n_))
    comp = 0.0
    for sub in SUBSETS:
        d = F.stop(**composite(sub)) - g
        if "primary" in sub:
            comp += np.clip(1.0 - np.abs(d), 0, None).sum()
        elif "h1" in sub:
            comp += max(0, 1.0 - nth_largest(d, 18))
    v["composed"] = comp
    # the chart: the dearest nursing locality changes under s1, s2 and o1; no two golden nursing figures within 1.5
    gn = g[3::4]
    top = int(np.argmax(gn))
    ch = 0.0
    if CHART_TOP is not None:
        t = LOC_I[CHART_TOP]
        ch += max(0, np.delete(gn, t).max() - gn[t] + 2.0)
        top = t
    for k in ("s1", "s2", "o1"):
        sn = F.stop(**AC.STOPS[k])[3::4]
        others = np.delete(sn, top)
        ch += max(0, sn[top] - others.max() + 1.0)
    srt = np.sort(gn)
    ch += np.clip(1.2 - np.diff(srt), 0, None).sum()
    v["chart"] = ch
    tot = sum(v.values())
    return (tot, v) if detail else tot


def optimise(F, levers, rng, iters=60000, verbose=False):
    """levers: list of (kind, resident index, bound info). kinds: 'A' contribution in force and after, 'B' reviews
    completed in advance only, 'C' fee supplement, 'D' merged client's superseded assessment"""
    cur = score(F)
    applied = np.zeros(len(levers))
    steps = np.array([0.37, 0.83, 1.71, 3.29, 6.13, 11.47])
    for it in range(iters):
        if cur <= 0:
            break
        j = int(rng.integers(len(levers)))
        kind, r, lo, hi = levers[j]
        delta = float(rng.choice(steps)) * (1 if rng.random() < 0.5 else -1)
        if kind == "C":
            delta = float(np.round(delta / 0.5) * 0.5) or 0.5
        if not (lo <= applied[j] + delta <= hi):
            continue
        saved = {k: F.cols[k][r] for k in F.cols}
        _do(F, kind, r, delta, levers[j])
        new = score(F)
        if new < cur - 1e-9:
            cur = new
            applied[j] += delta
        else:
            for k, val in saved.items():
                F.cols[k][r] = val
        if verbose and it % 5000 == 0:
            print("  ask tune", it, round(cur, 3), flush=True)
    return applied, cur


def _do(F, kind, r, delta, lever):
    flags = lever[4] if len(lever) > 4 else {}
    if kind == "A":
        F.cols["c_in"][r] += delta
        F.cols["c_lat"][r] += delta
        if flags.get("one_shares"):
            F.cols["c_in1"][r] += delta
            F.cols["c_lat1"][r] += delta
    elif kind == "B":
        F.cols["c_lat"][r] += delta
        if flags.get("one_shares_later"):
            F.cols["c_lat1"][r] += delta
    elif kind == "C":
        F.cols["fee"][r] += delta
    elif kind == "D":
        F.cols["c_in1"][r] += delta
        if flags.get("one_latest_is_inforce1"):
            F.cols["c_lat1"][r] += delta


class Person:
    def __init__(self, rows):
        self.rows = rows          # [effective, completed, is_main_ref, amount, index into O.assess]

    def values(self):
        def pick(rs, key):
            return rs[max(range(len(rs)), key=key)][3] if rs else 0.0
        inf_ = [x for x in self.rows if x[0] <= W.ASOF]
        main = [x for x in self.rows if x[2]]
        main_inf = [x for x in main if x[0] <= W.ASOF]
        return (pick(inf_, lambda k: (inf_[k][0], inf_[k][1])), pick(self.rows, lambda k: (self.rows[k][1], self.rows[k][0])),
                pick(main_inf, lambda k: (main_inf[k][0], main_inf[k][1])), pick(main, lambda k: (main[k][1], main[k][0])))


def build(S, O, df):
    """the levers on each resident of the table, and the rows they move"""
    idx = {c: i for i, c in enumerate(O.cid)}
    rows_of = {}
    for k, a in enumerate(O.assess):
        if a["outcome"] == "SELF" or a["_i"] < 0:
            continue
        rows_of.setdefault(a["_i"], []).append(k)
    ep_of = {}
    for k, p in enumerate(O.placements):
        if p["_st"] <= W.ASOF and (not np.isfinite(p["_end"]) or p["_end"] >= W.ASOF):
            ep_of[p["_i"]] = k
    persons, levers = {}, []
    for r, row in enumerate(df.itertuples(index=False)):
        if row.ptype != "PERM":
            continue
        i = idx[row.cl]
        rs = [[O.assess[k]["effective"], O.assess[k]["completed"], O.assess[k]["_ref"] == O.debtor[i],
               O.assess[k]["amount"], k] for k in rows_of.get(i, [])]
        P = Person(rs)
        persons[r] = (i, P)
        inf_ = [x for x in rs if x[0] <= W.ASOF]
        if inf_ and max(inf_, key=lambda x: (x[0], x[1]))[3] > 0:
            levers.append(("A", r, -30.0, 30.0))
        if any(x[0] > W.ASOF for x in rs):
            levers.append(("B", r, -40.0, 40.0))
        if i in O.merged:
            levers.append(("D", r, -40.0, 40.0))
        if i in ep_of:
            fee = O.placements[ep_of[i]]["weekly_fee"]
            supp = round(fee - W.NCHC[2026][S.care[i]], 2)
            levers.append(("C", r, -supp, 175.0 - supp))
    return persons, levers, ep_of


def move(F, persons, kind, r, delta):
    i, P = persons[r]
    if kind == "C":
        F.cols["fee"][r] += delta
        return
    inf_ = [x for x in P.rows if x[0] <= W.ASOF]
    if kind == "A":
        e0 = max(inf_, key=lambda x: (x[0], x[1]))[0]
        for x in P.rows:
            if x[0] >= e0:
                x[3] += delta
    elif kind == "B":
        for x in P.rows:
            if x[0] > W.ASOF:
                x[3] += delta
    elif kind == "D":
        mi = [x for x in P.rows if x[2] and x[0] <= W.ASOF]
        if mi:
            max(mi, key=lambda x: (x[0], x[1]))[3] += delta
    v = P.values()
    for k, val in zip(("c_in", "c_lat", "c_in1", "c_lat1"), v):
        F.cols[k][r] = val


def construct_chart(F, persons, levers, applied):
    """the chart's top locality X is the golden's dearest nursing locality; residents of X's own team in X's homes are
    assessed a little higher, and residents placed in X's nursing homes from other teams carry a little more
    supplement, until X stops being the dearest when the placement's locality is used or those placed from other
    teams are dropped"""
    at = {(k, r): j for j, (k, r, lo, hi) in enumerate(levers)}
    g = F.stop()
    X = int(np.argmax(g[3::4]))
    locals_ = [r for r in range(F.n) if F.team[r] == X and F.home[r] == X and F.care[r] == 1 and F.ptype[r] == "PERM"
               and not F.dead[r] and ("A", r) in at]
    movers = [r for r in range(F.n) if F.home[r] == X and F.team[r] != X and F.care[r] == 1 and F.ptype[r] == "PERM"
              and not F.dead[r] and ("C", r) in at]
    for _ in range(40):
        o1 = F.stop(**AC.STOPS["o1"])[3::4]
        s1 = F.stop(**AC.STOPS["s1"])[3::4]
        s2 = F.stop(**AC.STOPS["s2"])[3::4]
        gn = F.stop()[3::4]
        need_lower = any(v[X] > np.delete(v, X).max() - 2.5 for v in (o1, s1, s2))
        need_lead = gn[X] < np.delete(gn, X).max() + 3.0
        if not need_lower and not need_lead:
            break
        if need_lower:
            for r in locals_:
                j = at[("A", r)]
                if applied[j] + 1.0 <= levers[j][3]:
                    move(F, persons, "A", r, 1.0)
                    applied[j] += 1.0
        if need_lead:
            for r in movers:
                j = at[("C", r)]
                if applied[j] + 2.0 <= levers[j][3]:
                    move(F, persons, "C", r, 2.0)
                    applied[j] += 2.0
    return X


def search(F, persons, levers, applied, rng, steps, iters, verbose=False):
    cur = score(F)
    for it in range(iters):
        if cur <= 0:
            break
        j = int(rng.integers(len(levers)))
        kind, r, lo, hi = levers[j]
        delta = float(rng.choice(steps)) * (1 if rng.random() < 0.5 else -1)
        if kind == "C":
            delta = float(np.round(delta / 0.5) * 0.5) or 0.5
        if not (lo <= applied[j] + delta <= hi):
            continue
        i, P = persons[r]
        saved_rows = [x[3] for x in P.rows]
        saved = {k: F.cols[k][r] for k in F.cols}
        move(F, persons, kind, r, delta)
        if kind != "C" and any(x[3] < 0 for x in P.rows):
            new = np.inf
        else:
            new = score(F)
        if new < cur - 1e-9:
            cur = new
            applied[j] += delta
        else:
            for x, a in zip(P.rows, saved_rows):
                x[3] = a
            for k, val in saved.items():
                F.cols[k][r] = val
        if verbose and it % 4000 == 0:
            print("  ask tune", it, round(cur, 3), flush=True)
    return cur


def centre_pass(F, persons, levers, applied):
    """every golden ask figure onto a whole pound: one resident's contribution and one resident's fee supplement in
    each cell, both residents placed by their own locality team"""
    at = {(k, r): j for j, (k, r, lo, hi) in enumerate(levers)}
    for cell in range(10):
        loc, care = cell // 2, cell % 2
        m = (F.home == loc) & (F.care == care) & (F.ptype == "PERM") & ~F.dead
        n = int(m.sum())
        rs = [r for r in np.where(m)[0] if F.team[r] == loc]
        off = (0.04 + 0.013 * cell) * (1 if cell % 3 else -1)       # a few pence off the whole pound
        c = F.cols["c_in"][m].mean()
        dc = (np.round(c) + off - c) * n
        for r in sorted(rs, key=lambda r: -F.cols["c_in"][r]):
            j = at.get(("A", r))
            if j is not None and levers[j][2] <= applied[j] + dc <= levers[j][3]:
                move(F, persons, "A", r, dc)
                applied[j] += dc
                break
        net = (F.cols["fee"][m] - F.cols["c_in"][m]).mean()
        df_ = (np.round(net) - off * 0.8 - net) * n
        for r in sorted(rs, key=lambda r: -(F.cols["fee"][r] - F.cols["sched"][r])):
            j = at.get(("C", r))
            if j is not None and levers[j][2] <= applied[j] + df_ <= levers[j][3]:
                move(F, persons, "C", r, df_)
                applied[j] += df_
                break


def run(S, O, df, seed, iters=80000, verbose=False):
    rng = np.random.default_rng(seed)
    F = Fast(df)
    persons, levers, ep_of = build(S, O, df)
    steps = np.array([0.37, 0.83, 1.71, 3.29, 6.13, 11.47, 19.31])
    applied = np.zeros(len(levers))
    construct_chart(F, persons, levers, applied)
    CENTRE_W[0] = 0.0
    search(F, persons, levers, applied, rng, steps, iters, verbose)
    CENTRE_W[0] = 10.0
    centre_pass(F, persons, levers, applied)
    cur = search(F, persons, levers, applied, rng, steps, iters // 3, verbose)
    # write back: assessment amounts and the episode fees
    for r, (i, P) in persons.items():
        for x in P.rows:
            O.assess[x[4]]["amount"] = round(x[3], 2)
    for j, (kind, r, lo, hi) in enumerate(levers):
        if kind == "C" and applied[j] != 0:
            i = persons[r][0]
            O.placements[ep_of[i]]["weekly_fee"] = round(O.placements[ep_of[i]]["weekly_fee"] + applied[j], 2)
    return cur, score(F, detail=True)[1]
