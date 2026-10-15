"""The quarterly reports and the wage records, read off the spells: monthly employment is the count of spells
active on the 12th; wages are paid by calendar day within each quarter (final pay after a closure lands in the next
quarter); taxable wages stop at the state's wage base per worker, account and year."""
import datetime as dt
from collections import defaultdict

import numpy as np

import econ as E
import world as W

QS = W.QUARTERS
QIDX = {q: i for i, q in enumerate(QS)}


def county_code(a, y, q):
    """The county a quarterly row carries: the ZIP's county before geocoding took effect, the worksite's after."""
    if (y, q) < W.GEOCODE_FROM:
        return W.CODE[a.zip_county]
    return W.CODE[a.county]


def derive(world, S):
    A = world.accts
    rng = np.random.default_rng(W.SEED + 7)
    n = len(S.acct)
    acct = np.array(S.acct)
    st = np.array([s.toordinal() for s in S.start])
    en = np.array([e.toordinal() for e in S.end])
    # monthly employment: active on the 12th
    emp = np.zeros((len(A), len(E.MONTHS)), dtype=np.int32)
    for m, t in enumerate(E.TWELFTHS):
        o = t.toordinal()
        act = (st <= o) & (en >= o)
        np.add.at(emp[:, m], acct[act], 1)
    # wages by spell and quarter
    items = defaultdict(float)             # (worker, account, qi) -> wages
    daily = np.array(S.wage) * 12.0 / 365.25
    noise = rng.uniform(0.965, 1.035, size=(n, len(QS)))
    for qi, (y, q) in enumerate(QS):
        q0, q1 = E.qstart(y, q).toordinal(), E.qend(y, q).toordinal()
        lo = np.maximum(st, q0)
        hi = np.minimum(en, q1)
        days = hi - lo + 1
        idx = np.nonzero(days > 0)[0]
        amt = daily[idx] * days[idx] * noise[idx, qi]
        for i, v in zip(idx.tolist(), amt.tolist()):
            items[(int(S.worker[i]), int(acct[i]), qi)] += v
    # final pay after a closure: the workers on the last day paid again the next quarter
    final = 0
    for a in A:
        if not a.final_pay or a.last is None:
            continue
        ly, lq = E.qof(a.last)
        nq = E.nextq(ly, lq)
        if nq not in QIDX:
            continue
        on_last = [i for i in world.by_acct[a.idx] if S.end[i] == a.last]
        for i in on_last:
            if rng.random() < 0.85:
                items[(int(S.worker[i]), a.idx, QIDX[nq])] += float(S.wage[i]) * float(rng.uniform(0.12, 0.55))
                final += 1
    wage_rows = sorted(((wk, ac, qi, round(v, 2)) for (wk, ac, qi), v in items.items() if v >= 1.0),
                       key=lambda r: (r[2], r[1], r[0]))
    # quarterly totals and taxable wages (by worker, account and calendar year)
    tot = defaultdict(float)
    taxable = defaultdict(float)
    ytd = defaultdict(float)
    for wk, ac, qi, v in sorted(wage_rows, key=lambda r: (r[0], r[1], r[2])):
        y = QS[qi][0]
        left = max(0.0, W.TAXABLE_BASE - ytd[(wk, ac, y)])
        tx = min(v, left)
        ytd[(wk, ac, y)] += v
        tot[(ac, qi)] += v
        taxable[(ac, qi)] += tx
    # report span: from the registration quarter (or the extract's first) to the inactivation quarter (or the last)
    qrows = []
    for a in A:
        reg_q = E.qof(a.reg) if a.reg >= W.WIN0 else QS[0]
        end_date = a.inact if (a.inact is not None and a.inact <= W.EXTRACT) else None
        last_q = E.qof(end_date) if end_date is not None and end_date <= W.WIN1 else QS[-1]
        if end_date is not None and end_date < W.WIN0:
            continue
        for qi, (y, q) in enumerate(QS):
            if (y, q) < reg_q or (y, q) > last_q:
                continue
            m = emp[a.idx, 3 * qi: 3 * qi + 3]
            qrows.append({"acct": a.idx, "qi": qi, "county": county_code(a, y, q), "m1": int(m[0]), "m2": int(m[1]),
                          "m3": int(m[2]), "wages": round(tot.get((a.idx, qi), 0.0), 2),
                          "taxable": round(taxable.get((a.idx, qi), 0.0), 2)})
    return {"emp": emp, "wage_rows": wage_rows, "qrows": qrows, "final_items": final}
