"""The golden and every rung, computed from the world (design time) and, in verify.py, again from the shipped files.
Here the inputs are the world's own tables; calc_from_pack in verify.py reads only the bundle."""
from __future__ import annotations

import math

import numpy as np

import common as K


def placement(E, est=None, bar=K.STANDARD_LOAD, posts=K.NEW_POSTS):
    """BRK-STD-03: one post at a time to the gateway whose load (forecast monthly formal entries over its posts,
    the posts already placed counted) is highest, while that load exceeds the standard; the rest held."""
    est = dict(est or K.ESTABLISHMENT)
    placed = {g: 0 for g in E}
    order = []
    for _ in range(posts):
        load = {g: E[g] / (est[g] + placed[g]) for g in E}
        g = max(load, key=lambda x: (load[x], x))
        if load[g] > bar:
            placed[g] += 1
            order.append((g, load[g]))
        else:
            break
    held = posts - sum(placed.values())
    final = {g: E[g] / (est[g] + placed[g]) for g in E}
    return placed, held, final, order


def base_shipments(W, g):
    return sum(W.volume[(g, y, m)] for (y, m) in K.BASE_MONTHS)


def plan_shipments_k(W):
    """The 2027 network plan: each gateway's base-year month times the plan's growth, in thousands to one decimal."""
    out = {}
    for g in K.GATEWAYS:
        for (y, m) in K.BASE_MONTHS:
            out[(g, m)] = K.round_dp(W.volume[(g, y, m)] * (1 + K.PLAN_GROWTH[g]) / 1000.0, 1)
    return out


def plan_ratio(W, g, plan_k=None):
    plan_k = plan_k or plan_shipments_k(W)
    return sum(plan_k[(g, m)] for m in range(1, 13)) * 1000.0 / base_shipments(W, g)


def formal_at(W, g, rate_of, ogd_kept=True):
    """Base-year shipments at gateway g routed with the rate given by rate_of(shipment)."""
    n = 0
    for s in W.ships:
        if s.gw != g:
            continue
        if s.ogd and ogd_kept:
            n += 1
        elif s.ogd and not ogd_kept:
            n += int(s.value * rate_of(s) > K.LINE_CAD)
        else:
            n += int(K.round_dp(s.value * rate_of(s), 2) > K.LINE_CAD)
    return n


# ---------------------------------------------------------------------------------------------------- pass-through
def records(W):
    """The two years on file as the extracts carry them, one record per shipment (an amended shipment at its amended
    value): year 0 the twelve months to September 2025, year 1 the base."""
    amended = {id(s): nv for s, nv in W.amended}
    out = []
    for yr, ships in ((0, W.prior), (1, W.ships)):
        for s in ships:
            v = amended.get(id(s), s.value)
            cad = K.round_dp(v * s.rate, 2)
            out.append(dict(yr=yr, gw=s.gw, imp=s.importer, hs=s.hs, cur=s.cur, val=v, rate=s.rate, cad=cad,
                            ogd=bool(s.ogd), formal=bool(s.ogd) or cad > K.LINE_CAD, cad_priced=s.cad_priced,
                            local=s.local.date(), utc=s.utc.date(), seg=s.seg))
    return out


def seg_gc(r):
    return (r["gw"], r["cur"])


def k_inv(r):
    return (r["gw"], r["imp"], r["hs"], r["cur"], r["val"])


def k_cad(r):
    return (r["gw"], r["imp"], r["hs"], r["cur"], r["cad"])


def repeat_counts(recs, seg=seg_gc, ki=k_inv, kc=k_cad, weight="shipment", both_years=False, tol=False):
    """By segment: the base year's foreign-currency shipments (OGD goods aside) that repeat a consignment of the year
    before on its invoice value, and those that repeat one on its CAD value. weight 'consignment' counts each repeated
    consignment once; both_years also matches the year before's shipments against the base; tol matches the CAD value
    within a cent (the conversion's rounding)."""
    fx = [r for r in recs if not r["ogd"] and r["cur"] != "CAD"]
    by_year = {0: [r for r in fx if r["yr"] == 0], 1: [r for r in fx if r["yr"] == 1]}
    n_inv, n_cad = {}, {}
    pairs = [(1, 0), (0, 1)] if both_years else [(1, 0)]

    def shifted(r, d):
        q = dict(r)
        q["cad"] = K.round_dp(r["cad"] + d, 2)
        return q
    for a, b in pairs:
        p_inv = {ki(r) for r in by_year[b]}
        p_cad = {kc(r) for r in by_year[b]}
        seen_i, seen_c = set(), set()
        for r in by_year[a]:
            sg = seg(r)
            if ki(r) in p_inv:
                if weight == "consignment":
                    if (a, ki(r)) in seen_i:
                        continue
                    seen_i.add((a, ki(r)))
                n_inv[sg] = n_inv.get(sg, 0) + 1
            elif kc(r) in p_cad or (tol and (kc(shifted(r, -0.01)) in p_cad or kc(shifted(r, 0.01)) in p_cad)):
                if weight == "consignment":
                    key = kc(dict(r, cad=K.round_to(r["cad"], 1))) if tol else kc(r)
                    if (a, key) in seen_c:
                        continue
                    seen_c.add((a, key))
                n_cad[sg] = n_cad.get(sg, 0) + 1
    return n_inv, n_cad


def shares(n_inv, n_cad):
    """Each segment's pass-through share: the repeat shipments that kept their invoice value over all repeats."""
    out = {}
    for sg in set(n_inv) | set(n_cad):
        a, b = n_inv.get(sg, 0), n_cad.get(sg, 0)
        out[sg] = a / (a + b)
    return out


def slope_shares(recs, seg=seg_gc, ki=k_inv, kc=k_cad):
    """Each segment's pass-through as a regression: within the consignments seen in both years (on the invoice value
    or on the CAD value), the log of the CAD value on the log of the day's rate, slope 1 for goods that keep their
    invoice prices and 0 for goods that keep their CAD prices."""
    fx = [r for r in recs if not r["ogd"] and r["cur"] != "CAD"]
    groups = {}
    for r in fx:
        groups.setdefault(("i",) + ki(r), []).append(r)
        groups.setdefault(("c",) + kc(r), []).append(r)
    sxx, sxy = {}, {}
    for v in groups.values():
        if len({r["yr"] for r in v}) < 2:
            continue
        lr = [math.log(r["rate"]) for r in v]
        lc = [math.log(r["cad"]) for r in v]
        mr, mc = sum(lr) / len(lr), sum(lc) / len(lc)
        sg = seg(v[0])
        sxx[sg] = sxx.get(sg, 0.0) + sum((a - mr) ** 2 for a in lr)
        sxy[sg] = sxy.get(sg, 0.0) + sum((a - mr) * (b - mc) for a, b in zip(lr, lc))
    return {sg: sxy[sg] / sxx[sg] for sg in sxx if sxx[sg] > 0}


def mixture_counts(recs, pi, seg=seg_gc, plan=None):
    """Each gateway's base-year shipments routed for 2027: OGD goods formal; goods invoiced in CAD on their value; in
    each other segment the pass-through share pi re-routed at the plan's rate on the invoice value, the rest keeping
    the CAD value (and the route) the base year gave them."""
    plan = plan or K.PLAN_RATE
    n = {g: 0.0 for g in K.GATEWAYS}
    for r in recs:
        if r["yr"] != 1:
            continue
        g = r["gw"]
        if r["ogd"] or r["cur"] == "CAD":
            n[g] += r["formal"]
            continue
        p = pi[seg(r)]
        n[g] += p * (K.round_dp(r["val"] * plan[r["cur"]], 2) > K.LINE_CAD) + (1.0 - p) * r["formal"]
    return n


def scale(W, n):
    return {g: n[g] * plan_ratio(W, g) / 12.0 for g in K.GATEWAYS}


def golden_E(W, recs=None):
    """The golden: each segment's pass-through share from the repeat consignments, the base year re-routed with it."""
    recs = recs or records(W)
    return scale(W, mixture_counts(recs, shares(*repeat_counts(recs))))


def full_repricing_E(W):
    """Rival (b): every foreign-currency shipment re-routed at the plan's rate on its invoice value (pass-through 1)."""
    return {g: formal_at(W, g, lambda s: K.PLAN_RATE[s.cur]) * plan_ratio(W, g) / 12.0 for g in K.GATEWAYS}


def pooled_share_E(W, recs=None):
    """Rival (c): one pass-through share for the network, pooled over the segments."""
    recs = recs or records(W)
    n_inv, n_cad = repeat_counts(recs, seg=lambda r: "all")
    p = shares(n_inv, n_cad)["all"]
    return scale(W, mixture_counts(recs, {sg: p for sg in {seg_gc(r) for r in recs}})), p


def by_key_E(W, keyf, recs=None):
    """The pass-through share estimated on another segmentation (by currency alone, by gateway alone, by origin)."""
    recs = recs or records(W)
    pi = shares(*repeat_counts(recs, seg=keyf))
    return scale(W, mixture_counts(recs, pi, seg=keyf)), pi


def consignment_level_E(W, recs=None):
    """Each base-year shipment that repeats a consignment of the year before routed as its own price behaves (a repeat
    on the invoice value re-routed at the plan's rate, a repeat on the CAD value kept), the rest at the segment's
    share."""
    recs = recs or records(W)
    pi = shares(*repeat_counts(recs))
    fx0 = [r for r in recs if r["yr"] == 0 and not r["ogd"] and r["cur"] != "CAD"]
    p_inv, p_cad = {k_inv(r) for r in fx0}, {k_cad(r) for r in fx0}
    n = {g: 0.0 for g in K.GATEWAYS}
    for r in recs:
        if r["yr"] != 1:
            continue
        g = r["gw"]
        if r["ogd"] or r["cur"] == "CAD":
            n[g] += r["formal"]
            continue
        at_plan = K.round_dp(r["val"] * K.PLAN_RATE[r["cur"]], 2) > K.LINE_CAD
        if k_inv(r) in p_inv:
            n[g] += at_plan
        elif k_cad(r) in p_cad:
            n[g] += r["formal"]
        else:
            p = pi[seg_gc(r)]
            n[g] += p * at_plan + (1 - p) * r["formal"]
    return scale(W, n)


def truth_E(W):
    """The world's own 2027 at the plan's rates: goods priced in the invoice currency re-routed at the plan's rate,
    goods priced in CAD at their CAD price (never computable from the pack: a shipment's pricing is not on file)."""
    amended = {id(s): nv for s, nv in W.amended}
    n = {g: 0 for g in K.GATEWAYS}
    for s in W.ships:
        v = amended.get(id(s), s.value)
        if s.ogd:
            n[s.gw] += 1
        elif s.cur == "CAD" or s.cad_priced:
            n[s.gw] += int(K.round_dp(v * s.rate, 2) > K.LINE_CAD)
        else:
            n[s.gw] += int(K.round_dp(v * K.PLAN_RATE[s.cur], 2) > K.LINE_CAD)
    return scale(W, n)


def default_E(W):
    return {g: sum(W.formal_hist[(g, y, m)] for (y, m) in K.BASE_MONTHS) * plan_ratio(W, g) / 12.0
            for g in K.GATEWAYS}


# ---------------------------------------------------------------------------------------------------- the rungs
def monthly_series(W, g):
    return np.array([W.formal_hist[(g, y, m)] for (y, m) in K.HIST_MONTHS], float), \
        np.array([W.volume[(g, y, m)] for (y, m) in K.HIST_MONTHS], float)


def trend_E(W, g):
    """R0b: a log-linear trend with month-of-year effects on the gateway's monthly formal entries since January 2021,
    carried to 2027 (the shortcut that never looks at a value)."""
    f, _ = monthly_series(W, g)
    t = np.arange(len(f))
    mo = np.array([m for (_, m) in K.HIST_MONTHS])
    X = np.column_stack([np.ones(len(f)), t] + [(mo == k).astype(float) for k in range(2, 13)])
    b, *_ = np.linalg.lstsq(X, np.log(f), rcond=None)
    tf = np.arange(len(f) + 3, len(f) + 15)          # January to December 2027
    Xf = np.column_stack([np.ones(12), tf] + [(np.arange(1, 13) == k).astype(float) for k in range(2, 13)])
    return float(np.exp(Xf @ b).mean())


def holt_winters_E(W, g):
    """R0c: additive-trend, multiplicative-season exponential smoothing on the monthly formal entries."""
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    f, _ = monthly_series(W, g)
    fit = ExponentialSmoothing(f, trend="add", seasonal="mul", seasonal_periods=12,
                               initialization_method="estimated").fit()
    fc = fit.forecast(15)[3:]
    return float(np.mean(fc))


def share_regression_E(W, g):
    """R1: the formal share of shipments regressed on the month's US dollar and euro rates (month-of-year effects),
    evaluated at the plan's rates and carried on the plan's shipments."""
    f, v = monthly_series(W, g)
    share = f / v
    mo = np.array([m for (_, m) in K.HIST_MONTHS])
    usd = np.array([K.monthly_rate("USD", i) for i in range(len(f))])
    eur = np.array([K.monthly_rate("EUR", i) for i in range(len(f))])
    X = np.column_stack([np.ones(len(f)), usd, eur] + [(mo == k).astype(float) for k in range(2, 13)])
    b, *_ = np.linalg.lstsq(X, share, rcond=None)
    sh = []
    for k in range(1, 13):
        row = [1.0, K.PLAN_RATE["USD"], K.PLAN_RATE["EUR"]] + [1.0 if k == j else 0.0 for j in range(2, 13)]
        sh.append(float(np.dot(b, row)))
    plan_k = plan_shipments_k(W)
    return sum(sh[k - 1] * plan_k[(g, k)] * 1000.0 for k in range(1, 13)) / 12.0


def golden_shares(W, recs=None):
    recs = recs or records(W)
    return shares(*repeat_counts(recs))


def mixture_at(W, rate_of, recs=None, ogd_kept=True, cad_factor=1.0, inv_factor=1.0):
    """The golden's pass-through shares with another rate for the re-routed share: rate_of(record) is the rate a
    record's invoice value is converted at; OGD goods on value alone when ogd_kept is False; prices moved by a factor
    (cad_factor on the CAD-held share, inv_factor on the invoice-held share) for the price corridor."""
    recs = recs or records(W)
    pi = golden_shares(W, recs)
    n = {g: 0.0 for g in K.GATEWAYS}
    for r in recs:
        if r["yr"] != 1:
            continue
        g = r["gw"]
        if r["ogd"] and ogd_kept:
            n[g] += 1
            continue
        held = K.round_dp(r["cad"] * cad_factor, 2) > K.LINE_CAD
        if r["cur"] == "CAD":
            n[g] += held
            continue
        moved = K.round_dp(r["val"] * inv_factor * rate_of(r), 2) > K.LINE_CAD
        p = pi[seg_gc(r)]
        n[g] += p * moved + (1.0 - p) * held
    return scale(W, n)


def usd_only_E(W, recs=None):
    """R2c: the golden's pass-through, every foreign-currency value re-routed with the US dollar's change alone."""
    return mixture_at(W, lambda r: r["rate"] * K.PLAN_RATE["USD"] / W.rates["USD"][r["local"]], recs)


def eur_only_E(W, recs=None):
    """R2d: the golden's pass-through, only the euro shipments re-routed at the plan's euro rate."""
    return mixture_at(W, lambda r: K.PLAN_RATE["EUR"] if r["cur"] == "EUR" else r["rate"], recs)


def value_only_E(W, recs=None):
    """R2e: the golden's pass-through, OGD goods routed on their value alone."""
    return mixture_at(W, lambda r: K.PLAN_RATE[r["cur"]], recs, ogd_kept=False)


def latest_quarter_E(W, g):
    """R0d: the formal share of the last three months, carried on the plan."""
    last = K.BASE_MONTHS[-3:]
    f = sum(W.formal_hist[(g, y, m)] for (y, m) in last)
    v = sum(W.volume[(g, y, m)] for (y, m) in last)
    plan_k = plan_shipments_k(W)
    return f / v * sum(plan_k[(g, k)] for k in range(1, 13)) * 1000.0 / 12.0


def pooled_E(W):
    """R0e: the network's formal share of the base year carried on each gateway's plan."""
    f = sum(W.formal_hist[(g, y, m)] for g in K.GATEWAYS for (y, m) in K.BASE_MONTHS)
    v = sum(W.volume[(g, y, m)] for g in K.GATEWAYS for (y, m) in K.BASE_MONTHS)
    plan_k = plan_shipments_k(W)
    return {g: f / v * sum(plan_k[(g, k)] for k in range(1, 13)) * 1000.0 / 12.0 for g in K.GATEWAYS}


def spot_E(W, recs=None):
    """R0f: the golden's pass-through at the last customs rate on file (30 September 2026) instead of the plan's."""
    last = {c: W.rates[c][K.HIST_END] for c in K.CURRENCIES}
    return mixture_at(W, lambda r: last[r["cur"]], recs)


def inflated_E(W, f, recs=None):
    """The price corridor: every price moved by a factor f between the base year and 2027 (invoice-currency prices
    before the plan's rates, CAD prices as they stand)."""
    return mixture_at(W, lambda r: K.PLAN_RATE[r["cur"]], recs, cad_factor=f, inv_factor=f)


def diff_slope_shares(recs, seg=seg_gc):
    """Each segment's pass-through as a regression of the change in the log CAD value on the change in the log rate,
    through the origin, over each base-year repeat and the latest shipment of its consignment the year before."""
    fx = [r for r in recs if not r["ogd"] and r["cur"] != "CAD"]
    last_inv, last_cad = {}, {}
    for r in sorted((r for r in fx if r["yr"] == 0), key=lambda r: r["local"]):
        last_inv[k_inv(r)] = r
        last_cad[k_cad(r)] = r
    sxx, sxy = {}, {}
    for r in fx:
        if r["yr"] != 1:
            continue
        q = last_inv.get(k_inv(r)) or last_cad.get(k_cad(r))
        if q is None:
            continue
        dr = math.log(r["rate"]) - math.log(q["rate"])
        dc = math.log(r["cad"]) - math.log(q["cad"])
        sg = seg(r)
        sxx[sg] = sxx.get(sg, 0.0) + dr * dr
        sxy[sg] = sxy.get(sg, 0.0) + dr * dc
    return {sg: sxy[sg] / sxx[sg] for sg in sxx if sxx[sg] > 0}


# ---------------------------------------------------------------------------------------------------- the asks
OT_CODES = ("OT15", "OT20")


def ask_a(staff, lines, mode="golden"):
    """Overtime hours worked at each desk in each fiscal quarter of 2025-26.
    golden: OT lines at their hours, call-backs at the time between punches, the October overlap once, each line on
    the desk the employee was assigned to on the work date.
    s1: the line's home cost centre as the export stamped it; s2: call-backs at paid hours; s3: the migration week
    twice; cracker: all three; s5: the HR staff file's current desk for every line."""
    import field as FD
    by_k = {s.k: s for s in staff}
    out = {(g, q): 0.0 for g in K.GATEWAYS for q in (1, 2, 3, 4)}
    for ln in lines:
        if not (K.FY_START <= ln.day <= K.FY_END):
            continue
        if ln.code not in OT_CODES + ("CB",):
            continue
        s = by_k[ln.emp]
        if mode in ("s1", "cracker"):
            if ln.day <= FD.TA_LEGACY_END:
                desk = s.desk_on(FD.TA_LEGACY_PULL) if (s.left is None or s.left > FD.TA_LEGACY_PULL) else s.desk_on(s.left)
            else:
                desk = s.desk_on(FD.TA_NEW_PULL) if (s.left is None or s.left > FD.TA_NEW_PULL) else s.desk_on(s.left)
        elif mode == "s5":
            desk = s.desk_on(FD.HR_PULL) if s.left is None else s.desk_on(s.left)
        else:
            desk = s.desk_on(ln.day)
        if ln.code == "CB":
            h = ln.hours if mode in ("s2", "cracker") else ln.worked
        else:
            h = ln.hours
        mult = 2 if (mode in ("s3", "cracker") and FD.TA_NEW_FROM <= ln.day <= FD.TA_LEGACY_END) else 1
        out[(desk, K.fiscal_quarter(ln.day))] += h * mult
    return out


def ask_b(stmts, mode="golden"):
    """What Brandmoor charged before tax for the entries it transmitted for each desk in each fiscal quarter.
    golden: each statement's net (its entry charges and minimum adjustment once) on its transmissions' month, the
    re-issue in place of the original. s1 (cracker): the AP register by posting date, both statements of the dispute;
    s2: the statements by their titled month (the re-issue in place); s3: the portal by transmission date, the
    minimum adjustment on every line, March 2026 absent; s4: the portal by transmission date, the adjustment once,
    March 2026 absent; s5: the statements on their transmissions' month, the disputed original kept beside its
    re-issue."""
    out = {(g, q): 0.0 for g in K.GATEWAYS for q in (1, 2, 3, 4)}
    replaced = {s.reissue_of for s in stmts if s.reissue_of}
    for st in stmts:
        tm = st.month
        im = (st.issued.year, st.issued.month)
        if mode == "golden":
            if st.number in replaced:
                continue
            d = dt_date(*tm)
            if K.FY_START <= d <= K.FY_END:
                out[(st.gw, K.fiscal_quarter(d))] += st.net
        elif mode == "s1":
            post = st.issued       # posted within days of issue, same month (asserted in checks)
            if K.FY_START <= post <= K.FY_END:
                out[(st.gw, K.fiscal_quarter(post))] += st.net
            if st.credit_memo and K.FY_START <= st.credit_memo[1] <= K.FY_END:
                out[(st.gw, K.fiscal_quarter(st.credit_memo[1]))] -= st.net
        elif mode == "s5":
            d = dt_date(*tm)
            if K.FY_START <= d <= K.FY_END:
                out[(st.gw, K.fiscal_quarter(d))] += st.net
        elif mode == "s2":
            if st.number in replaced:
                continue
            lab = dt_date(st.month[0] + (st.month[1] == 12), st.month[1] % 12 + 1)
            if K.FY_START <= lab <= K.FY_END:
                out[(st.gw, K.fiscal_quarter(lab))] += st.net
        elif mode in ("s3", "s4"):
            if st.number in replaced:
                continue
            lab = dt_date(st.month[0] + (st.month[1] == 12), st.month[1] % 12 + 1)
            if not (dt_date(2025, 4, 1) <= lab <= dt_date(2026, 3, 1)):
                continue
            std_r, ogd_r, rush_r = st.portal_rates
            for e in st.entries:
                d = e.t.date()
                if not (K.FY_START <= d <= K.FY_END):
                    continue
                fee = std_r if e.service == "STD" else ogd_r
                v = fee + (rush_r if e.rush else 0.0)
                if mode == "s3":
                    v += st.minimum_adj
                out[(st.gw, K.fiscal_quarter(d))] += v
            if mode == "s4":
                d = dt_date(*tm)
                if K.FY_START <= d <= K.FY_END:
                    out[(st.gw, K.fiscal_quarter(d))] += st.minimum_adj
    return out


def dt_date(y, m, d=1):
    import datetime as _dt
    return _dt.date(y, m, d)
