"""The readers the screens run on the clean truth (the world's own tables, before any Layer 1): the golden and its
defensible variants, the first look, the careful reader, the interaction readers, the constructing readers and the
literal executions of the remit. Costs are total marks across the pupils a change reached."""
import numpy as np

import world as Wd

U, IPU = Wd.U, 3
TOPIC_MAX = sum(Wd.ITEM_MAX)


def topic_pct(o):
    """each sitting pupil's June marks on each topic as a share of the topic's five marks"""
    return o['marks'].sum(axis=2) / float(TOPIC_MAX)


def ks2_resid(o):
    pp = o['pp']
    sat = o['sat']
    p7 = pp['p7_numeracy'].values.astype(float)
    have = ~np.isnan(p7)
    x = np.where(have, (p7 - 100) / 15.0, 0.0)
    X = np.column_stack([np.ones(o['N']), x, (~have).astype(float), pp['fsm'].values.astype(float)])
    m = sat
    b = np.linalg.lstsq(X[m], o['total'][m].astype(float), rcond=None)[0]
    r = np.full(o['N'], np.nan)
    r[m] = o['total'][m] - X[m] @ b
    return r


def weak_mask(acc0, mode):
    ok = ~np.isnan(acc0)
    if mode[0] == 'q':
        a = np.where(ok, acc0, np.nan)
        with np.errstate(all='ignore'):
            cut = np.nanquantile(a, mode[1], axis=1)
        return ok & (acc0 <= cut[:, None]), ok
    return ok & (acc0 < mode[1]), ok


def within(y, a, b, rows):
    na, nb = a[rows].sum(1), b[rows].sum(1)
    ya = y[rows]
    ma = np.where(na > 0, (ya * a[rows]).sum(1) / np.maximum(na, 1), np.nan)
    mb = np.where(nb > 0, (ya * b[rows]).sum(1) / np.maximum(nb, 1), np.nan)
    return np.nanmean(ma - mb)


def rewritten_mask(w, o):
    rw = np.zeros((o['N'], U), bool)
    for gi, g in enumerate(Wd.YG):
        rw[np.ix_(o['ygi'] == gi, w.rewritten[g])] = True
    return rw


def golden(w, mode=('q', 1 / 3), level_to_A=False, adjust=True):
    o5, o6 = w.sess[2025], w.sess[2026]
    y5, y6 = topic_pct(o5), topic_pct(o6)
    s5, s6 = o5['sat'], o6['sat']
    wk5, ok5 = weak_mask(o5['acc0'], mode)
    wk6, ok6 = weak_mask(o6['acc0'], mode)
    def wsum(y, wk, ok, rows):
        # each pupil's weak-topic shortfall against their other topics, in topic-shares, summed over their weak topics
        na, nb = wk[rows].sum(1), (ok & ~wk)[rows].sum(1)
        ya = y[rows]
        ma = np.where(na > 0, (ya * wk[rows]).sum(1) / np.maximum(na, 1), np.nan)
        mb = np.where(nb > 0, (ya * (ok & ~wk)[rows]).sum(1) / np.maximum(nb, 1), np.nan)
        return np.nanmean(na * (ma - mb))
    exB = within(y6, wk6, ok6 & ~wk6, s6) - within(y5, wk5, ok5 & ~wk5, s5)
    costB = -(wsum(y6, wk6, ok6, s6) - wsum(y5, wk5, ok5, s5)) * TOPIC_MAX * s6.sum()
    rw5, rw6 = rewritten_mask(w, o5), rewritten_mask(w, o6)
    exA = within(y6, rw6, ~rw6, s6) - within(y5, rw5, ~rw5, s5)
    costA = -exA * TOPIC_MAX * rw6[s6].sum()
    r5, r6 = (ks2_resid(o5), ks2_resid(o6)) if adjust else (o5['total'].astype(float), o6['total'].astype(float))

    def did(m6, m5=None):
        a = np.nanmean(r6[m6 & s6]) - np.nanmean(r6[~m6 & s6])
        if m5 is not None:
            a -= np.nanmean(r5[m5 & s5]) - np.nanmean(r5[~m5 & s5])
        return -a * (m6 & s6).sum()
    removed = o6['pp']['base_referrals'].values > 0 if 'base_referrals' in o6['pp'] else o6['removed']
    out = dict(A=costA, B=costB, C=did(o6['ygi'] == 2, o5['ygi'] == 2), D=did(removed), E=did(o6['split']))
    if level_to_A:
        clean6 = s6 & (o6['ygi'] != 2) & ~removed & ~o6['split']
        clean5 = s5 & (o5['ygi'] != 2)
        lev = np.nanmean(ks2_resid(o6)[clean6]) - np.nanmean(ks2_resid(o5)[clean5])
        lev -= exB * TOPIC_MAX * wk6[clean6].sum(1).mean() + exA * TOPIC_MAX * rw6[clean6].sum(1).mean()
        out['A'] += max(0.0, -lev) * s6.sum()
    return out


MODES = [('q', 1 / 3), ('q', 0.25), ('q', 0.5), ('a', 0.5), ('a', 0.6), ('a', 0.7)]


def golden_family(w):
    fam = []
    for m in MODES:
        for lv in (False, True):
            for adj in (True, False):
                fam.append(((m, lv, adj), golden(w, m, lv, adj)))
    return fam


def engagement(o):
    return np.nanmean(o['done']), o['R'].sum(1).mean()


def evidence_A(w):
    o5, o6 = w.sess[2025], w.sess[2026]
    y5, y6 = topic_pct(o5), topic_pct(o6)
    rw5, rw6 = rewritten_mask(w, o5), rewritten_mask(w, o6)
    s5, s6 = o5['sat'], o6['sat']
    return (y6[s6][rw6[s6]].mean() - y6[s6][~rw6[s6]].mean()) - (y5[s5][rw5[s5]].mean() - y5[s5][~rw5[s5]].mean())


def first_look(w):
    """outcome by item beside each dated change, before and after on each reach, segmentations by recorded fields:
    the two whole-system changes take the whole fall; the rewritten topics fell most; the switch's engagement rose."""
    c6, r6 = engagement(w.sess[2026]); c5, r5 = engagement(w.sess[2025])
    adverseB = (c6 < c5) or (r6 < r5)
    exA = evidence_A(w)
    if exA < 0 and not adverseB:
        return 'A'
    if adverseB and exA >= 0:
        return 'B'
    return 'tie'


def careful(w):
    """pooled pupil model with every partial reach x year and the engagement fields x year: the partial changes
    are small on their reaches, the whole-system fall goes to the change with its own evidence."""
    o5, o6 = w.sess[2025], w.sess[2026]
    g = golden(w, level_to_A=False)
    partial = max(g['C'], g['D'], g['E'])
    whole = (np.nanmean(o5['total'][o5['sat']]) - np.nanmean(o6['total'][o6['sat']])) * o6['sat'].sum()
    fl = first_look(w)
    if fl == 'A' and whole - partial > partial:
        return 'A'
    return fl


def interaction_readers(w):
    """reads the homework-accuracy x session interaction as the platform's: median and tercile split DiD on June
    totals, and the regression-implied loss below the mean; the platform takes the extra fall of the low group,
    the framework the rest."""
    o5, o6 = w.sess[2025], w.sess[2026]
    calls = []
    hr = {}
    for y, o in ((2025, o5), (2026, o6)):
        hacc = np.nanmean(o['acc0'], 1)
        p7 = o['pp']['p7_numeracy'].values.astype(float)
        ok = ~np.isnan(hacc) & ~np.isnan(p7) & o['sat']
        X = np.column_stack([np.ones(ok.sum()), p7[ok]])
        b = np.linalg.lstsq(X, hacc[ok], rcond=None)[0]
        r = np.full(o['N'], np.nan)
        r[ok] = hacc[ok] - X @ b
        hr[y] = (r, ok)
    whole = (np.nanmean(o5['total'][o5['sat']]) - np.nanmean(o6['total'][o6['sat']])) * o6['sat'].sum()
    for lo, hi in ((0.5, 0.5), (1 / 3, 2 / 3)):
        f = {}
        for y, o in ((2025, o5), (2026, o6)):
            r, ok = hr[y]
            ql, qh = np.nanquantile(r[ok], lo), np.nanquantile(r[ok], hi)
            f[y] = (o['total'][ok & (r <= ql)].mean(), o['total'][ok & (r >= qh)].mean(), (ok & (r <= ql)).sum())
        d = (f[2025][0] - f[2026][0]) - (f[2025][1] - f[2026][1])
        costB = max(d, 0) * f[2026][2]
        calls.append('B' if costB > whole - costB else 'A')
    # regression implied
    ys, ts, rs = [], [], []
    for y, o in ((2025, o5), (2026, o6)):
        r, ok = hr[y]
        ys.append(o['total'][ok].astype(float)); rs.append(r[ok]); ts.append(np.full(ok.sum(), 1.0 if y == 2026 else 0.0))
    yv, t, rv = np.concatenate(ys), np.concatenate(ts), np.concatenate(rs)
    X = np.column_stack([np.ones_like(yv), t, rv, rv * t])
    b, *_ = np.linalg.lstsq(X, yv, rcond=None)
    e = yv - X @ b
    se = np.sqrt(np.diag(e @ e / (len(yv) - 4) * np.linalg.pinv(X.T @ X)))
    z = b[3] / se[3]
    r6, ok6 = hr[2026]
    costB = max(0.0, b[3]) * (-np.minimum(r6[ok6], 0)).sum()
    calls.append('B' if costB > whole - costB else 'A')
    return calls, float(z)


def constructing_readers(w):
    """(i) per-topic review volume x session against the topic's June change, the rewritten topics beside it;
    (ii) Corvella's review share by topic within pupil against June 2025 topic marks."""
    o5, o6 = w.sess[2025], w.sess[2026]
    y5, y6 = topic_pct(o5), topic_pct(o6)
    rows = []
    for gi, g in enumerate(Wd.YG):
        m5 = (o5['ygi'] == gi) & o5['sat']; m6 = (o6['ygi'] == gi) & o6['sat']
        for t in range(U):
            rows.append((o6['R'][m6, t].mean() - o5['R'][m5, t].mean(), y6[m6, t].mean() - y5[m5, t].mean(),
                         float(t in w.rewritten[g])))
    a = np.array(rows)
    X = np.column_stack([np.ones(len(a)), a[:, 0], a[:, 2]])
    b, *_ = np.linalg.lstsq(X, a[:, 1], rcond=None)
    e = a[:, 1] - X @ b
    se = np.sqrt(np.diag(e @ e / (len(a) - 3) * np.linalg.pinv(X.T @ X)))
    zvol = b[1] / se[1]
    n6 = o6['sat'].sum() / 3.0
    costB = max(0.0, b[1]) * (-np.minimum(a[:, 0], 0)).sum() * TOPIC_MAX * n6
    costA = max(0.0, -b[2]) * a[:, 2].sum() * TOPIC_MAX * n6
    call_i = 'B' if (zvol > 2 and costB > costA) else 'A'
    s5 = o5['sat']
    sh = o5['R'][s5] / np.maximum(o5['R'][s5].sum(1, keepdims=True), 1e-9)
    ds = sh - sh.mean(1, keepdims=True); dy = y5[s5] - y5[s5].mean(1, keepdims=True)
    slope = (ds * dy).sum() / (ds ** 2).sum()
    call_ii = 'B' if slope > 0 else 'A'
    return [('topic_volume', call_i, float(zvol)), ('corvella_share', call_ii, float(slope))]


def literal(w):
    """the remit executed on each change's reach (before and after; difference in differences; P7-adjusted):
    the two whole-system changes each take the whole movement of every pupil they reached."""
    out = []
    o5, o6 = w.sess[2025], w.sess[2026]
    whole = (np.nanmean(o5['total'][o5['sat']]) - np.nanmean(o6['total'][o6['sat']])) * o6['sat'].sum()
    for adj in (False, True):
        g = golden(w, adjust=adj)
        c = dict(C=g['C'], D=g['D'], E=g['E'], A=whole, B=whole)
        top = sorted(c.items(), key=lambda kv: -kv[1])
        out.append('tie' if abs(top[0][1] - top[1][1]) < 1e-6 else top[0][0])
    return out
