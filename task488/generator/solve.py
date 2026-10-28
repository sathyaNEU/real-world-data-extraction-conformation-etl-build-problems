"""Every route to the call, run on the shipped tables only (the bank export, the test events, the item responses and
the authoring catalog), as a solver would read them.

The golden: each workshop item's difficulty estimated by marginal maximum likelihood with the 2021 calibrated items
held at their bank values and each window's students a normal population with its own mean and spread, from every
scored response in complete and incomplete events. The rivals and the family are in rivals() and family()."""
from __future__ import annotations

import numpy as np
import pandas as pd

import params as P


def theta(qss):
    return (np.asarray(qss, float) - P.SCALE_A) / P.SCALE_B


def pc(t, b):
    return 1.0 / (1.0 + np.exp(-np.clip(t - b, -30, 30)))


def solve_b(fun, lo=-7.0, hi=7.0, n=45):
    for _ in range(n):
        mid = (lo + hi) / 2
        if fun(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


class Grade:
    """One grade's operational pool and its scored 2025-26 responses, indexed for the estimators."""

    def __init__(self, s, g, mess=False):
        bank, ev, rs = s["bank"], s["events"], s["responses"]
        items = bank[(bank.grade == g) & (bank.status == "operational")].reset_index(drop=True)
        ev = ev[(ev.grade == g) & ((ev.status != "invalidated") | mess)].reset_index(drop=True)
        if mess:      # invalidated events kept and every unscored re-delivery row read as a wrong answer
            r = rs[rs.event_id.isin(set(ev.event_id))].copy()
            r["score"] = r.score.fillna(0)
        else:
            r = rs[rs.event_id.isin(set(ev.event_id)) & rs.score.notna()]
            r = r.drop_duplicates(["event_id", "sequence"], keep="last")
        self.g = g
        self.items = items
        self.cut = P.CUT_QSS[g]
        self.ev = ev
        self.E = ev.reset_index().set_index("event_id")["index"].reindex(r.event_id).to_numpy()
        self.I = items.reset_index().set_index("item_key")["index"].reindex(r.item_key).to_numpy()
        self.X = r.score.astype(int).to_numpy()
        self.NE = len(ev)
        self.cal = (items.difficulty_basis == "launch calibration 2021").to_numpy()
        self.wk = np.where(~self.cal)[0]
        self.b0 = theta(items.difficulty_qss.to_numpy())
        self.win = ev.window.map({w[0]: i for i, w in enumerate(P.WINDOWS)}).to_numpy()
        self.rep = theta(pd.to_numeric(ev.scale_score, errors="coerce").to_numpy())
        order = np.argsort(self.I, kind="mergesort")
        bounds = np.searchsorted(self.I[order], np.arange(len(items) + 1))
        self.by_item = {j: order[bounds[j]:bounds[j + 1]] for j in range(len(items))}

    def loglik(self, b, grid, mask=None):
        m = slice(None) if mask is None else mask
        I, X, E = self.I[m], self.X[m], self.E[m]
        pg = pc(grid[None, :], b[I][:, None])
        v = np.where(X[:, None] == 1, np.log(pg), np.log1p(-pg))
        out = np.zeros((self.NE, grid.size))
        np.add.at(out, E, v)
        return out

    def fixed_theta(self, t, items=None):
        out = {}
        for j in (self.wk if items is None else items):
            r = self.by_item[j]
            ok = ~np.isnan(t[self.E[r]])
            tt, x = t[self.E[r]][ok], self.X[r][ok]
            out[j] = solve_b(lambda bb: (pc(tt, bb) - x).sum()) if x.size else np.nan
        return out


def posterior(ll, prior):
    w = np.exp(ll - ll.max(1, keepdims=True)) * prior
    return w / w.sum(1, keepdims=True)


def mml(G, grid=None, pop=True, tol=1e-4, iters=200, persons="marginal"):
    """Marginal maximum likelihood with the calibrated items fixed. persons: 'marginal' (EM), 'eap' (alternating
    EAP point estimates), 'mle' (joint maximum likelihood)."""
    grid = np.linspace(-5, 5, 81) if grid is None else grid
    b = G.b0.copy()
    nw = len(P.WINDOWS)
    pops = [(0.0, 1.0)] * nw
    for _ in range(iters):
        ll = G.loglik(b, grid)
        W = np.zeros_like(ll)
        for w in range(nw):
            m = G.win == w
            mu, sd = pops[w] if pop else (0.0, 1.0)
            pr = np.exp(-0.5 * ((grid - mu) / sd) ** 2)
            W[m] = posterior(ll[m], pr / pr.sum())
        if pop:
            pops = []
            for w in range(nw):
                ww = W[G.win == w].sum(0)
                mu = (ww * grid).sum() / ww.sum()
                pops.append((mu, float(np.sqrt((ww * (grid - mu) ** 2).sum() / ww.sum()))))
        nb = b.copy()
        if persons == "marginal":
            for j in G.wk:
                r = G.by_item[j]
                wq = W[G.E[r]].sum(0)
                xs = G.X[r].sum()
                nb[j] = solve_b(lambda bb: (wq * pc(grid, bb)).sum() - xs)
        else:
            t = (W * grid).sum(1) if persons == "eap" else grid[ll.argmax(1)]
            for j in G.wk:
                r = G.by_item[j]
                tt, x = t[G.E[r]], G.X[r]
                nb[j] = solve_b(lambda bb: (pc(tt, bb) - x).sum())
        done = np.abs(nb - b).max() < tol
        b = nb
        if done:
            break
    return b, W, pops


def qss(b):
    return np.round(P.SCALE_A + P.SCALE_B * np.asarray(b, float), 1)


def low_count(G, qss_wk):
    cal_low = int((G.items.difficulty_qss[G.cal] < G.cut).sum())
    return cal_low + int((np.asarray(qss_wk) < G.cut).sum())


def golden(s, mess=False):
    out = {}
    for g in P.GRADES:
        G = Grade(s, g, mess=mess)
        b, W, pops = mml(G)
        q = qss(b[G.wk])
        out[g] = dict(G=G, b=b, W=W, pops=pops, wk_qss=q, low=low_count(G, q),
                      commission=max(0, P.FLOOR - low_count(G, q)))
    return out


GRID_GOLD = np.linspace(-5, 5, 81)
PRIOR = np.exp(-GRID_GOLD ** 2 / 2)
PRIOR /= PRIOR.sum()


def rivals(s, gold, catalog=None):
    """Each named wrong route's low-band count per grade."""
    out = {k: {} for k in ("panel", "pvalue", "reported", "jml", "clean_mle", "clean_eap", "drop_lowp",
                           "no_multistep")}
    for g in P.GRADES:
        G = gold[g]["G"]
        cut = G.cut
        rating = G.items.difficulty_qss.to_numpy()[G.wk]
        out["panel"][g] = low_count(G, rating)
        # percent correct mapped through the calibrated items' own relation
        p = np.array([G.X[G.by_item[j]].mean() for j in range(len(G.items))])
        p = np.clip(p, 0.01, 0.99)
        lp = np.log(p / (1 - p))
        cal = np.where(G.cal & np.array([G.by_item[j].size >= 30 for j in range(len(G.items))]))[0]
        coef = np.polyfit(lp[cal], G.b0[cal], 1)
        out["pvalue"][g] = low_count(G, qss(np.polyval(coef, lp[G.wk])))
        rep = G.fixed_theta(G.rep)
        out["reported"][g] = low_count(G, qss([rep[j] for j in G.wk]))
        bj, _, _ = mml(G, persons="mle")
        out["jml"][g] = low_count(G, qss(bj[G.wk]))
        llc = G.loglik(G.b0, GRID_GOLD, mask=G.cal[G.I])
        tm = GRID_GOLD[llc.argmax(1)]
        te = (posterior(llc, PRIOR) * GRID_GOLD).sum(1)
        cm, ce = G.fixed_theta(tm), G.fixed_theta(te)
        out["clean_mle"][g] = low_count(G, qss([cm[j] for j in G.wk]))
        out["clean_eap"][g] = low_count(G, qss([ce[j] for j in G.wk]))
        keep = np.array([p[j] >= 0.30 for j in G.wk])
        out["drop_lowp"][g] = low_count(G, np.where(keep, rating, 999.0))
        if catalog is not None:
            multi = G.items.item_key.map(catalog).to_numpy()[G.wk] == "multi-step word problem"
            out["no_multistep"][g] = low_count(G, np.where(multi, 999.0, rating))
        gold[g]["rival_b"] = dict(reported=rep, jml=bj, clean_mle=cm, clean_eap=ce, theta_rep=G.rep,
                                  theta_jml=None, theta_clean_mle=tm, theta_clean_eap=te)
    return out


def family(s, gold):
    """The golden's licensed family: marginal likelihood under other grids and a fixed prior, and alternating
    posterior means. Returns each member's low-band count per grade and every member's nearest workshop item."""
    members = {"mml_fixed_prior": dict(pop=False), "mml_grid_41": dict(grid=np.linspace(-5, 5, 41)),
               "mml_grid_161": dict(grid=np.linspace(-6, 6, 161)), "alternating_eap": dict(persons="eap")}
    out = {k: {} for k in members}
    near = {k: {} for k in members}
    for g in P.GRADES:
        G = gold[g]["G"]
        for k, kw in members.items():
            b, _, _ = mml(G, **kw)
            q = qss(b[G.wk])
            out[k][g] = low_count(G, q)
            near[k][g] = float(np.min(np.abs(q - G.cut)))
    return out, near


def anchor_check(gold):
    """The calibrated items re-estimated from the same responses under each route's abilities: mean error (scale
    points) on calibrated items below 452 (more than 1.2 logits below the scale's centre) and in the middle."""
    out = {}
    for g in P.GRADES:
        G = gold[g]["G"]
        rv = gold[g]["rival_b"]
        cal = [j for j in np.where(G.cal)[0] if G.by_item[j].size >= 40]
        low = np.array([G.b0[j] < -1.2 for j in cal])
        res = {}
        bj, Wj, _ = mml(G, persons="mle")
        tj = GRID_GOLD[G.loglik(bj, GRID_GOLD).argmax(1)]
        for name, t in (("reported", G.rep), ("jml", tj), ("clean_mle", rv["theta_clean_mle"]),
                        ("clean_eap", rv["theta_clean_eap"])):
            est = G.fixed_theta(t, items=cal)
            err = np.array([est[j] - G.b0[j] for j in cal]) * P.SCALE_B
            res[name] = (round(float(err[low].mean()), 2), round(float(err[~low].mean()), 2))
        W = gold[g]["W"]
        err = []
        for j in cal:
            r = G.by_item[j]
            wq = W[G.E[r]].sum(0)
            xs = G.X[r].sum()
            err.append((solve_b(lambda bb: (wq * pc(GRID_GOLD, bb)).sum() - xs) - G.b0[j]) * P.SCALE_B)
        err = np.array(err)
        res["golden"] = (round(float(err[low].mean()), 2), round(float(err[~low].mean()), 2))
        res["n_low"] = int(low.sum())
        out[g] = res
    return out


# ---- the import's other fields: one record per item, rebuilt from the catalog's version history -------------

def current_records(s):
    """Each authored item's current record: its versions read in order, version 1 the full record and each later
    version changing only the fields its changed_fields lists (a listed field left blank is cleared), under the key of
    its latest version."""
    cat = s["catalog"].copy()
    fields = ("item_type", "skill_tag", "framework_code_2026", "enemy_group")
    for c in fields + ("changed_fields",):
        cat[c] = cat[c].fillna("").astype(str)
    cat = cat.sort_values(["authoring_id", "version"], kind="mergesort")
    rec = {}
    for aid, sub in cat.groupby("authoring_id", sort=True):
        cur = {}
        for v in sub.itertuples():
            if int(v.version) == 1:
                cur = {f: getattr(v, f) for f in fields}
                continue
            for f in (x.strip() for x in v.changed_fields.split(";")):
                if f in fields:
                    cur[f] = getattr(v, f)
        top = sub.iloc[-1]
        rec[aid] = dict(authoring_id=aid, item_key=top.item_key, grade=int(top.grade), status=top.status,
                        keys=set(sub.item_key), framework=cur["framework_code_2026"], skill=cur["skill_tag"],
                        enemy=[cur["enemy_group"]] if cur["enemy_group"] else [])
    return rec


def import_table(s, gold):
    """The rows Corvane receives: operational items, one per authored item under its current key."""
    rec = current_records(s)
    by_key = {}
    for r in rec.values():
        for k in r["keys"]:
            by_key[k] = r
    bank = s["bank"][s["bank"].status == "operational"]
    xw = s["crosswalk"].fillna("")
    rows = []
    seen = set()
    for b in bank.itertuples():
        r = by_key[b.item_key]
        if r["item_key"] != b.item_key or r["authoring_id"] in seen or r["status"] != "active":
            continue
        seen.add(r["authoring_id"])
        if r["framework"]:
            dom = r["framework"].split(".")[0]
        else:
            cand = xw[xw.standard_code_2010 == b.standard_code]
            if len(cand) > 1:
                want = "skill tag: %s" % r["skill"]
                hit = cand[cand.condition == want]
                cand = hit if len(hit) else cand[cand.condition == "other skill tags"]
            dom = cand.framework_domain_2026.iloc[0]
        rows.append(dict(item_key=b.item_key, grade=int(b.grade), difficulty=float(b.difficulty_qss),
                         basis=b.difficulty_basis, reporting_domain=dom, interaction_type=b.interaction_type,
                         _groups=r["enemy"]))
    imp = pd.DataFrame(rows)
    est = {}
    for g in P.GRADES:
        G = gold[g]["G"]
        for j, q in zip(G.wk, gold[g]["wk_qss"]):
            est[G.items.item_key.iloc[j]] = float(q)
    wk = imp.basis == "writing panel rating"
    imp.loc[wk, "difficulty"] = imp.loc[wk, "item_key"].map(est)
    # enemy sets: a group's imported items in one grade's pool, two or more to a set
    mem = {}
    for r in imp.itertuples():
        for gname in r._7:
            mem.setdefault((gname, r.grade), []).append(r.item_key)
    imp["enemy_set"] = ""
    sets = {g: [] for g in P.GRADES}
    for (gname, g) in sorted(mem):
        keep = mem[(gname, g)]
        if len(keep) >= 2:
            sets[g].append((gname, keep))
    for g in P.GRADES:
        for n, (gname, keep) in enumerate(sets[g], 1):
            imp.loc[imp.item_key.isin(keep), "enemy_set"] = "G%d-ES%02d" % (g, n)
    imp = imp.drop(columns=["_groups", "basis"]).sort_values(["grade", "item_key"], kind="mergesort").reset_index(drop=True)
    return imp
