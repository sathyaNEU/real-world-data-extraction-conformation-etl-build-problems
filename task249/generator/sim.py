"""The examination's world: an item bank written from item models (case and single items), six 2026 forms and ten
2027 forms, trial blocks, four-hour sittings worked in delivery order with each item's seconds, resits in later
windows on a form not sat before, results reviews, and the truth: each resit sitting's gain from what earlier
sittings and reviews showed the candidate, split into the excess on the items it reached anyway (direct) and the
correct answers on the items it reached only in the time recognised items freed (reach).   W = sim.world()"""
import numpy as np

import params as P

FORMS = P.F26 + P.F27


def bank(rs):
    nm = 3600
    size = rs.choice([1, 2, 3], nm, p=[0.62, 0.27, 0.11])
    model = np.repeat(np.arange(nm), size)
    n = len(model)
    mcase = rs.uniform(size=nm) < 0.32
    bm = rs.normal(-0.95, 0.80, nm) + 0.15 * mcase
    b = bm[model] + rs.normal(0, 0.22, n)
    a = rs.uniform(0.75, 1.30, n)
    area = rs.integers(0, 8, nm)[model]
    case = mcase[model]
    tm = np.where(case, np.log(P.T_CASE), np.log(P.T_SHORT)) + rs.normal(0, P.T_SD, n)
    members = {}
    for j in range(n):
        members.setdefault(int(model[j]), []).append(j)
    return dict(model=model, b=b, a=a, area=area, case=case, tm=tm, members=members, n=n, nm=nm)


def assemble(B, rs):
    model, members, case = B["model"], B["members"], B["case"]
    order = {c: [m for m in rs.permutation(B["nm"]) if bool(case[members[m][0]]) == c] for c in (False, True)}
    fresh_log = []

    def fresh(k, kc=None):
        """k items from models not used before, kc of them case items (None: the bank's own mix)"""
        out = []
        if kc is None:
            kc = int(round(k * 0.30))
        for c, kk in ((True, kc), (False, k - kc)):
            for _ in range(kk):
                m = order[c].pop()
                out.append(members[m][0])
        fresh_log.extend(out)
        return out

    forms = {}
    live26 = fresh(420, int(round(420 * 0.265)))
    for f in P.F26:
        cs = [j for j in live26 if case[j]]
        ss = [j for j in live26 if not case[j]]
        kc = int(round(P.NOP * P.CASE_SHARE[f]))
        items = list(rs.choice(cs, kc, replace=False)) + list(rs.choice(ss, P.NOP - kc, replace=False))
        forms[f] = [int(items[k]) for k in rs.permutation(P.NOP)]
    trial = {}
    for w in range(4):
        for fi in P.W_FORMS[w]:
            trial[(w, FORMS[fi])] = fresh(P.NTR)
    trial26 = [j for (w, f), v in trial.items() for j in v]
    live26 = sorted(set(j for f in P.F26 for j in forms[f]))
    h1_items = []
    for f in P.F27:
        d = P.DESIGN[f]
        h2 = f >= "CC27-F"
        src_live = live26 if not h2 else h1_items
        src_trial = trial26 if not h2 else trial26 + [j for (w, ff), v in trial.items() if w in (4, 5) for j in v]
        if d.get("rcase"):
            src_live = [j for j in src_live if case[j]]
        if d.get("easy"):
            src_live = sorted(src_live, key=lambda j: B["b"][j])[: len(src_live) // 3]
        taken = set()
        it_r = []
        for j in rs.permutation(src_live):
            if len(it_r) >= d["reuse"]:
                break
            if model[j] in taken:
                continue
            it_r.append(int(j)); taken.add(model[j])
        sib_pool = [members[int(model[j])] for j in src_live]
        it_s = []
        for grp in rs.permutation(len(sib_pool)):
            if len(it_s) >= d["sib"]:
                break
            mem = sib_pool[grp]
            m = model[mem[0]]
            if m in taken:
                continue
            spare = [k for k in mem if k not in src_live and k not in h1_items]
            if not spare:
                continue
            it_s.append(int(spare[0])); taken.add(m)
        it_t = []
        for j in rs.permutation(src_trial):
            if len(it_t) >= d["trial"]:
                break
            if model[j] in taken:
                continue
            it_t.append(int(j)); taken.add(model[j])
        have = it_r + it_s + it_t
        kc = int(round(P.NOP * d["case"])) - int(sum(case[j] for j in have))
        k = P.NOP - len(have)
        rest = fresh(k, max(0, min(k, kc)))
        items = have + rest
        forms[f] = [int(items[q]) for q in rs.permutation(len(items))]
        if not h2:
            h1_items += items
    for w in range(4, 8):
        for fi in P.W_FORMS[w]:
            trial[(w, FORMS[fi])] = fresh(P.NTR)
    return forms, trial


def layout(forms, trial, f, w):
    """delivery order: the form's scored items in order with the window's trial items at the trial slots"""
    seq, kind = [], []
    sc = iter(forms[f]); tr = iter(trial[(w, f)])
    for pos in range(1, P.NOP + P.NTR + 1):
        if pos in P.TRIAL_SLOTS:
            seq.append(next(tr)); kind.append("T")
        else:
            seq.append(next(sc)); kind.append("S")
    return np.array(seq), np.array(kind)


def exposure(B, prev, seq, w):
    """the logit lift and the time multiplier on each delivered item from the candidate's earlier sittings and held
    reviews: the same item reached at an earlier sitting, or an item written from the same item model"""
    model = B["model"]
    bump = np.zeros(len(seq)); spd = np.ones(len(seq)); src = np.zeros(len(seq), int)   # 1 same item, 2 sibling
    for h in prev:
        gap = w - h["w"]
        d = np.exp(-(gap - 1) / P.DECAY)
        pos = {int(j): i for i, j in enumerate(h["seq"])}
        mpos = {}
        for i, j in enumerate(h["seq"]):
            mpos.setdefault(int(model[j]), i)
        for i, j in enumerate(seq):
            j = int(j)
            if j in pos:
                q = pos[j]; share, s0 = 1.0, None
            elif int(model[j]) in mpos:
                q = mpos[int(model[j])]; share, s0 = P.M_SIB, P.S_SIB
            else:
                continue
            if not h["reach"][q]:
                continue
            wr = h["x"][q] == 0
            rv = wr and h["review_held"] and h["kind"][q] == "S"
            e = share * (P.M_REVIEW if rv else (P.M_WRONG if wr else P.M_RIGHT)) * d
            s = 1 - (1 - (s0 if s0 is not None else (P.S_REVIEW if rv else P.S_SEEN))) * d
            if e > bump[i]:
                bump[i] = e; src[i] = 1 if s0 is None else 2
            spd[i] = min(spd[i], s)
    return bump, spd, src


def sittings(B, forms, trial, rs):
    b, a, c, tm = B["b"], B["a"], P.C_GUESS, B["tm"]
    cands, rows, pending = [], [], []
    for w in range(8):
        new = list(range(len(cands), len(cands) + P.NFT))
        for _ in new:
            th = rs.normal(0, 1)
            tau = P.TAU_RHO * P.TAU_SD * th + np.sqrt(1 - P.TAU_RHO ** 2) * P.TAU_SD * rs.normal()
            cands.append(dict(th=th, tau=tau, hist=[]))
        back = [k for (k, ww) in pending if ww == w]
        pending = [(k, ww) for (k, ww) in pending if ww != w]
        for k in new + back:
            C = cands[k]
            prev = list(C["hist"])
            sat = {h["form"] for h in prev}
            allowed = [FORMS[fi] for fi in P.W_FORMS[w] if FORMS[fi] not in sat]
            f = allowed[int(rs.integers(0, len(allowed)))]
            seq, kind = layout(forms, trial, f, w)
            th = C["th"] + (P.LEARN * len(prev) + rs.normal(0, P.LEARN_SD) if prev else 0.0)
            bump, spd, src = exposure(B, prev, seq, w)
            z = a[seq] * (th - b[seq])
            p0 = c + (1 - c) / (1 + np.exp(-z))
            p1 = c + (1 - c) / (1 + np.exp(-(z + bump)))
            u = rs.uniform(size=len(seq))
            x1 = (u < p1).astype(int); x0 = (u < p0).astype(int)
            t0f = np.exp(tm[seq] + C["tau"] + rs.normal(0, P.EPS_SD, len(seq)))
            t0 = np.maximum(4000.0, np.round(t0f * 1000))          # milliseconds
            t1 = np.maximum(3000.0, np.round(t0f * spd * 1000))
            r1 = np.cumsum(t1) <= P.LIMIT * 1000
            r0 = np.cumsum(t0) <= P.LIMIT * 1000
            x = x1 * r1
            sc = kind == "S"
            raw = int(x[sc].sum())
            passed = raw >= P.PASS_RAW
            booked = (not passed) and rs.uniform() < P.P_REVIEW
            held = booked and rs.uniform() < P.P_REVIEW_HELD
            direct = float(((x1 - x0) * r0 * sc).sum())
            reach = float((x1 * (r1 & ~r0) * sc).sum())
            rec = dict(w=w, form=f, seq=seq, kind=kind, x=x, reach=r1, ms=np.where(r1, t1, 0.0), raw=raw,
                       passed=passed, review_booked=booked, review_held=held, n_prev=len(prev), cand=k,
                       gain=direct + reach, direct=direct, spill=reach, src=src, spd=spd,
                       egain=float(((p1 - p0) * r0 * sc).sum() + (p1 * (r1 & ~r0) * sc).sum()))
            C["hist"].append(rec)
            rows.append(rec)
            if not passed and rs.uniform() < P.P_RESIT:
                g = int(rs.choice([1, 2, 3], p=[P.GAP_P[1], P.GAP_P[2], P.GAP_P[3]]))
                if w + g < 8:
                    pending.append((k, w + g))
    return cands, rows


def pretest_quality(B, forms, trial, rs):
    """new items come to trial with the faults new items have: about a quarter barely separate strong from weak
    candidates and some are too easy; the items promoted to the 2027 forms passed their trial"""
    promoted = set(j for f in P.F27 for j in forms[f])
    for (w, f), items in sorted(trial.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        for j in items:
            if j in promoted:
                continue
            u = rs.uniform()
            if u < 0.24:
                B["a"][j] = rs.uniform(0.02, 0.32)
            elif u < 0.31:
                B["b"][j] = rs.uniform(-4.2, -3.0)


def world(seed=P.SEED):
    ss = np.random.SeedSequence(seed)
    r1, r2, r3, r4 = [np.random.default_rng(s) for s in ss.spawn(4)]
    B = bank(r1)
    forms, trial = assemble(B, r2)
    pretest_quality(B, forms, trial, r4)
    cands, rows = sittings(B, forms, trial, r3)
    return dict(B=B, forms=forms, trial=trial, cands=cands, rows=rows)


def truth(W):
    """each 2027 form's gain per resit sitting, its direct part and its reach part, and the resit sittings"""
    out = {}
    for f in P.F27:
        R = [r for r in W["rows"] if r["form"] == f and r["n_prev"] > 0]
        out[f] = dict(n=len(R), gain=float(np.mean([r["gain"] for r in R])),
                      direct=float(np.mean([r["direct"] for r in R])), reach=float(np.mean([r["spill"] for r in R])),
                      egain=float(np.mean([r["egain"] for r in R])))
    return out
