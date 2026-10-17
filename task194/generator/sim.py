"""The network's activity and complications, built forward: episodes first, then the expected complications
each unit-quarter carries under the specification's stratum rates, then the complications themselves.

A unit-quarter's standardised ratio is designed, never fitted afterwards. Each unit's quarterly ratios are
drawn around its own persistent ratio and then corrected block by block so that the pooled ratio over the
last four, the last eight and all ten closed quarters is the unit's persistent ratio: a unit's quarter swings
hard, its record does not drift. One random stream per unit and quarter, so a change in one quarter never
re-rolls another.
"""
import datetime as dt
import hashlib
import math

import numpy as np

import world as W

MONTH_SHAPE = {  # seasonal shape by calendar month for medical-weighted and surgical-weighted units
    "med": [0.96, 0.94, 0.97, 1.02, 1.06, 1.09, 1.08, 1.05, 1.01, 0.98, 0.95, 0.89],
    "surg": [1.02, 0.93, 1.05, 1.04, 1.03, 1.00, 1.01, 1.02, 1.03, 1.02, 1.04, 0.81],
}
MED_MIXES = {"gen_med", "resp", "renal", "aged", "neuro", "subacute"}
# how long a unit's multi-day episodes run, against the network's own shape
LOS_SCALE = {"aged": 1.92, "subacute": 2.35, "neuro": 1.34, "renal": 1.02, "gen_med": 0.94,
             "resp": 1.12, "ortho": 1.44, "gen_surg": 0.97, "colorectal": 1.26, "vasc": 1.18}
SAME_DAY_SHARE = 0.071          # episodes separated the day they were admitted
UNGROUPABLE_SHARE = 0.0118      # episodes the grouper could not assign a valid DRG
NONACUTE_CARE_SHARE = 0.0152    # acute units also report a few rehabilitation or maintenance episodes
BLANK_COMORBIDITY = 0.148       # the comorbidity score is not keyed for every episode
DIALYSIS_MIXES = {"renal", "gen_med", "subacute"}     # the units that separate same-day haemodialysis
# separations fall away over a weekend, hard on a surgical unit and less so on a medical one
WEEKDAY_SHAPE = {"med": [1.10, 1.07, 1.05, 1.08, 1.21, 0.76, 0.69],
                 "surg": [1.16, 1.12, 1.13, 1.18, 1.27, 0.46, 0.34]}
# the patient master index was issued in blocks as each site came onto it
MRN_BLOCK = {"H1": (1000000, 1399999), "H2": (1400000, 1649999),
             "H3": (1650000, 1849999), "H4": (1850000, 1899999)}


def unit_profile(code):
    """The rates a unit's own practice and recording sit at, around the network's."""
    r = rng("profile", code)
    return dict(same_day=SAME_DAY_SHARE * float(0.55 + 0.90 * r.random()),
                ungroup=UNGROUPABLE_SHARE * float(0.45 + 1.10 * r.random()),
                nonacute=NONACUTE_CARE_SHARE * float(0.40 + 1.25 * r.random()),
                blank=BLANK_COMORBIDITY * float(0.58 + 0.86 * r.random()))


def drg_weights(code, band, options):
    """A unit's own caseload inside a risk band: a few groups carry most of it."""
    r = rng("drgmix", code, band)
    w = np.sort(r.gamma(0.9, 1.0, len(options)))[::-1]
    w = w[r.permutation(len(options))] + 0.05
    return w / w.sum()


def rng(*parts):
    key = "|".join(str(p) for p in parts)
    return np.random.default_rng(int(hashlib.sha256(key.encode()).hexdigest()[:12], 16) ^ W.SEED)


def unit_rate(mix):
    """The mean stratum rate of a case-mix profile: the expected complications per in-scope episode."""
    total = 0.0
    for band, (weight, ages) in W.MIX[mix].items():
        total += weight * sum(a * W.STRATUM_RATE[(band, ab)] for a, ab in zip(ages, W.AGE_BANDS))
    return total


def quarters_for(unit):
    """The quarter indices a unit reports in."""
    code = unit[0]
    if code in W.MERGE_FROM:
        return [i for i, q in enumerate(W.QUARTERS) if q[2] < W.MERGE_DATE]
    if code == W.MERGE_INTO:
        return [i for i, q in enumerate(W.QUARTERS) if q[2] >= W.MERGE_DATE]
    return list(range(len(W.QUARTERS)))


def window_devs(sd, n, fixed_last, seedparts, level_at=(), cap=0.0075, tail4_cap=None):
    """n quarterly deviations around a unit's persistent ratio: one draw per quarter, the last closed quarter
    set to its designed value where there is one, and one uniform shift across the free quarters so the
    unit's record over the specification period comes back to its persistent ratio. Nothing is corrected
    block by block, so a quarter says nothing about the next beyond what de-meaning a short record implies.
    """
    r = rng("ratio", *seedparts)
    free = n - (1 if fixed_last is not None else 0)
    for _ in range(4000):
        dev = r.normal(0.0, sd, n)
        if fixed_last is not None:
            dev[n - 1] = fixed_last
        shift = float(dev.mean()) * n / free
        for i in range(free):
            dev[i] -= shift
        if any(abs(dev[i]) > cap for i in level_at):
            continue
        if tail4_cap is not None and n >= 5 and abs(float(dev[-4:].mean())) > tail4_cap:
            continue
        return dev
    return dev


def design_ratios(units, expected):
    """Every unit's designed standardised ratio by quarter.

    A unit-quarter's ratio is its own persistent level plus a quarterly shock sized so the count sits about
    `OVERDISPERSION` Pearson residuals from its expected number, which is what a real indicator does: a
    quarter of a few hundred episodes carries more than sampling error. The network's own quarterly position
    is then levelled, and each placement is written on top: for a placed unit the quarters before the team
    arrived come back to the unit's persistent level as a block, so the unit's standing over that block is
    its level while no single quarter in it is, and the assessment quarter and the two after it carry the
    programme's effect.
    """
    design = {}
    for u in units:
        code, _, _, mix, _, psi, sep, _, ylast, _, status = u
        qs = quarters_for(u)
        e = [max(1.0, expected.get((code, q), 1.0)) for q in qs]
        sd = sum(W.OVERDISPERSION / (psi * x) ** 0.5 for x in e) / len(e)
        dev = window_devs(sd, len(qs), None if ylast is None else ylast / psi - 1.0, (code,))
        design[code] = {qs[i]: psi * (1 + dev[i]) for i in range(len(qs))}
    design = level_network(design, units, expected)
    for _ in range(3):
        write_placements(design, units, expected)
        level_comparisons(design, units, expected)
    # the amalgamated unit's predecessors were the same service under two cost centres, so the two wards
    # together stood where the amalgamated unit stands: pooling them changes no figure
    pre = [u[0] for u in units if u[10] == "merged_into"]
    into = W.MERGE_INTO
    if pre and into in design:
        qs = [q for q in design[into] if (into, q) in expected]
        target = (sum(expected[(into, q)] * design[into][q] for q in qs)
                  / sum(expected[(into, q)] for q in qs))
        num = sum(expected[(c, q)] * design[c][q] for c in pre for q in design[c] if (c, q) in expected)
        den = sum(expected[(c, q)] for c in pre for q in design[c] if (c, q) in expected)
        if den and num:
            k = target * den / num
            for c in pre:
                for q in design[c]:
                    design[c][q] *= k
    return design


def placement_window(units):
    """The unit-quarters a placement writes: its own quarter and the two quarters the unit holds the gain.
    The quarters before the team arrived are ordinary quarters and the levelling may move them."""
    by_code = {u[0]: u for u in units}
    written = set()
    for k, code in W.EMBEDS.items():
        qs = quarters_for(by_code[code])
        pos = qs.index(k)
        written.update((code, qs[i]) for i in range(pos, min(pos + 1 + len(W.EMBED_RETAIN), len(qs))))
    return written


def write_placements(design, units, expected):
    """Write each placement on top of the levelled record.

    The quarters before the team arrived keep their own shocks and are shifted as a block, weighted by each
    quarter's expected complications, so the unit's pooled standing over them is its persistent level and no
    single quarter equals that level. The assessment quarter sits at that standing less the programme's
    effect, and the two quarters after it at the shares of the standing excess the unit holds.
    """
    by_code = {u[0]: u for u in units}
    for k, code in sorted(W.EMBEDS.items()):
        u = by_code[code]
        qs = quarters_for(u)
        pos = qs.index(k)
        pre = qs[:pos]
        ew = {q: max(1.0, expected.get((code, q), 1.0)) for q in pre}
        o = sum(ew[q] * design[code][q] for q in pre)
        e = sum(ew[q] for q in pre)
        shift = u[5] - o / e                      # the block comes back to the unit's own level
        for q in pre:
            design[code][q] += shift
        standing = u[5]
        noise = rng("embed", code).normal(0.0, 0.010, 3)
        design[code][k] = 1 + (1 - W.EMBED_EFFECT) * (standing - 1) + noise[0] * max(0.12, standing - 1)
        for j, keep in enumerate(W.EMBED_RETAIN):
            if pos + 1 + j < len(qs):
                design[code][qs[pos + 1 + j]] = (1 + keep * (standing - 1)
                                                 + noise[1 + j] * max(0.12, standing - 1))
    return design


def level_comparisons(design, units, expected):
    """Hold the rest of the network still across each placement's own two quarters.

    A placement's fall has to read the same against the unit's own record and against what the units the
    team was not working on did over the same two quarters, so for each placement quarter the units no
    placement is acting on are shifted by one common amount that takes their pooled movement between the
    quarter before the placement and the quarter of the placement to zero. The shift is a few thousandths
    of a ratio and leaves each unit's own record where it was to three decimals.
    """
    by_code = {u[0]: u for u in units}
    written = placement_window(units)
    acute = [u[0] for u in units if u[4] == "acute"]
    for _ in range(40):
        for k, placed in sorted(W.EMBEDS.items()):
            others = [c for c in acute if c != placed and (c, k) in expected and (c, k - 1) in expected
                      and (c, k) not in written and (c, k - 1) not in written]
            if not others:
                continue
            e = {c: expected[(c, k)] for c in others}
            pooled = (sum(expected[(c, k - 1)] * design[c][k - 1] for c in others)
                      / sum(expected[(c, k - 1)] for c in others)
                      - sum(e[c] * design[c][k] for c in others) / sum(e[c] for c in others))
            shift = pooled * sum(e[c] for c in others) / sum(e[c] for c in others)
            for c in others:
                design[c][k] += shift
    return design


def level_network(design, units, expected):
    """Hold the network's own quarterly position flat.

    The network's complication rate does not move quarter to quarter in this period; what moves is where
    the complications sit. Each quarter's pooled deviation across the units no placement is acting on is
    taken out of every unit's ratio in that quarter, which leaves each unit's own record where it was and
    leaves a placement's fall where it was against both its own record and the rest of the network.
    """
    written = placement_window(units)
    psi = {u[0]: u[5] for u in units}
    for q in range(len(W.QUARTERS)):
        rowsq = [(code, ratios[q] - psi[code], expected[(code, q)]) for code, ratios in design.items()
                 if q in ratios and (code, q) not in written and (code, q) in expected]
        if len(rowsq) < 3:
            continue
        shift = sum(wt * d for _, d, wt in rowsq) / sum(wt for _, _, wt in rowsq)
        for code, ratios in design.items():
            if q in ratios and (code, q) in expected:
                ratios[q] -= shift
    return design


def episodes(units):
    """Every episode row the extract carries, and the expected complications of each in-scope unit-quarter.

    Returns (rows, expected) where rows are dicts in separation order and expected maps (code, q) to the
    summed stratum rates of the unit-quarter's in-scope episodes.
    """
    rows, expected, inscope = [], {}, {}
    used = set()
    drg_by_band = {}
    for code, _, band in W.DRGS:
        drg_by_band.setdefault(band, []).append(code)
    for u in units:
        code, _, base, mix, service, _, sep, _, _, _, status = u
        medical = mix in MED_MIXES
        shape = MONTH_SHAPE["med" if medical else "surg"]
        wshape = WEEKDAY_SHAPE["med" if medical else "surg"]
        prof = unit_profile(code)
        mrn_lo, mrn_hi = MRN_BLOCK[base]
        wmix = {b: drg_weights(code, b, opts) for b, opts in drg_by_band.items() if b}
        for q in quarters_for(u):
            label, _, _, _, months = W.QUARTERS[q]
            exp_sum, n_scope = 0.0, 0
            recent = []
            for mi, month in enumerate(months):
                r = rng("eps", code, label, mi)
                drift = 1.0 + 0.045 * r.normal()
                n = int(round(sep / 3.0 * shape[month.month - 1] * drift))
                last = (month.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
                dayw = np.array([wshape[month.replace(day=d).weekday()] for d in range(1, last.day + 1)])
                dayw = dayw / dayw.sum()
                for _ in range(n):
                    bands = list(W.MIX[mix].items())
                    pick = r.random()
                    acc = 0.0
                    band = bands[-1][0]
                    for b, (wt, _) in bands:
                        acc += wt
                        if pick <= acc:
                            band = b
                            break
                    ages = W.MIX[mix][band][1]
                    age = W.AGE_BANDS[int(np.searchsorted(np.cumsum(ages), r.random(), side="left"))]
                    opts = drg_by_band[band]
                    drg = opts[int(np.searchsorted(np.cumsum(wmix[band]), r.random(), side="left"))]
                    same_day = r.random() < prof["same_day"]
                    ungroup = (not same_day) and r.random() < prof["ungroup"]
                    care = "Acute"
                    if service in ("rehabilitation", "psychiatric"):
                        care = "Rehabilitation" if service == "rehabilitation" else "Psychiatric"
                    elif r.random() < prof["nonacute"]:
                        care = "Maintenance" if r.random() < 0.35 else "Rehabilitation"
                    if same_day:
                        los = 0
                        if mix in DIALYSIS_MIXES and r.random() < 0.46:
                            drg = "L61Z"
                    else:
                        los = int(1 + r.gamma(2.1, 2.3 * LOS_SCALE[mix]))
                    if ungroup:
                        drg = "960Z" if r.random() < 0.6 else "961Z"
                    day = 1 + int(np.searchsorted(np.cumsum(dayw), r.random(), side="left"))
                    sep_date = month.replace(day=min(day, last.day))
                    pid = "MRN%07d" % int(r.integers(mrn_lo, mrn_hi + 1))
                    adm_date = sep_date - dt.timedelta(days=los)
                    # a patient admitted twice on one day for two different procedures, which happens
                    if recent and not same_day and r.random() < 0.016:
                        prev = recent[int(r.integers(len(recent)))]
                        shared = (sep_date - prev[1]).days
                        if 1 <= shared <= 60:
                            pid, adm_date, los = prev[0], prev[1], shared
                            while drg == prev[2]:
                                drg = opts[int(r.integers(len(opts)))]
                    in_scope = (care == "Acute" and los >= 1 and W.DRG_BAND.get(drg) not in (None, "SAME-DAY")
                                and service == "acute")
                    if in_scope:
                        exp_sum += W.STRATUM_RATE[(W.DRG_BAND[drg], age)]
                        n_scope += 1
                    while (code, pid, adm_date, drg) in used:
                        pid = "MRN%07d" % int(r.integers(mrn_lo, mrn_hi + 1))
                    used.add((code, pid, adm_date, drg))
                    recent.append((pid, adm_date, drg))
                    if len(recent) > 6:
                        recent.pop(0)
                    rows.append(dict(unit=code, q=q, qlabel=label, month=month, sep_date=sep_date, los=los,
                                     drg=drg, age=age, care=care, in_scope=in_scope, pid=pid,
                                     adm_date=adm_date,
                                     comorbidity=None if r.random() < prof["blank"] else
                                     int(min(9, max(0, round(r.gamma(1.9, 1.15))))),
                                     hac=False, rstream=float(r.random())))
            expected[(code, q)] = exp_sum
            inscope[(code, q)] = n_scope
    return rows, expected, inscope


def _panel(expected, design, units):
    """The integer complication count of every in-scope unit-quarter the design implies."""
    obs = {}
    for u in units:
        if u[4] != "acute":
            continue
        for q in quarters_for(u):
            if (u[0], q) in expected:
                obs[(u[0], q)] = int(round(expected[(u[0], q)] * design[u[0]][q]))
    return obs


def _register(obs, expected, units):
    """The closed register as `golden.placement_record` reads it, from an integer panel."""
    by_code = {u[0]: u for u in units}
    acute = [u[0] for u in units if u[4] == "acute"]
    rows = []
    for k, code in sorted(W.EMBEDS.items()):
        qs = [q for q in quarters_for(by_code[code]) if (code, q) in obs]
        pre = [q for q in qs if q < k]
        e = expected[(code, k)]
        before = sum(obs[(code, q)] for q in pre) / sum(expected[(code, q)] for q in pre)
        written = placement_window(units)
        others = [c for c in acute if c != code and (c, k) in obs and (c, k - 1) in obs
                  and (c, k) not in written and (c, k - 1) not in written]
        pm = (sum(obs[(c, k - 1)] for c in others) / sum(expected[(c, k - 1)] for c in others)
              - sum(obs[(c, k)] for c in others) / sum(expected[(c, k)] for c in others))
        rows.append(dict(code=code, q=k, before=before, expected=e, observed=obs[(code, k)],
                         carried=(before - 1) * e, realised=obs[(code, k)] - e,
                         counterfactual=before * e,
                         concurrent_pooled=pm * e))
    return rows


def _readings(rows):
    n = len(rows)
    P = [r["carried"] for r in rows]
    fall = [r["carried"] - r["realised"] for r in rows]
    V = [max(1.0, r["counterfactual"]) for r in rows]
    defined = [f / p for f, p in zip(fall, P) if abs(p) >= 5.0]
    pm, fm = sum(P) / n, sum(fall) / n
    pv = sum((p - pm) ** 2 for p in P) / n
    return {
        "pooled sums": sum(fall) / sum(P),
        "least squares through the origin":
            sum(p * f for p, f in zip(P, fall)) / sum(p * p for p in P),
        "least squares with an intercept":
            sum((p - pm) * (f - fm) for p, f in zip(P, fall)) / (pv * n),
        "the variance-weighted fit":
            sum(p * f / v for p, f, v in zip(P, fall, V)) / sum(p * p / v for p, v in zip(P, V)),
        "the median of the shares that are defined": sorted(defined)[len(defined) // 2],
        "against what the other units did over the same quarters":
            sum(r["carried"] - r["realised"] - r["concurrent_pooled"] for r in rows) / sum(P),
    }


def _models(rows):
    n = len(rows)
    fall = [r["carried"] - r["realised"] for r in rows]
    V = [max(1.0, r["counterfactual"]) for r in rows]
    out = {}
    for label, x in (("excess", [r["carried"] for r in rows]),
                     ("drop", [r["expected"] for r in rows]),
                     ("percent", [r["counterfactual"] for r in rows]),
                     ("constant", [1.0] * n)):
        den = sum(xi * xi / v for xi, v in zip(x, V))
        c = sum(xi * f / v for xi, f, v in zip(x, fall, V)) / den if den else 0.0
        out[label] = sum((f - c * xi) ** 2 / v for xi, f, v in zip(x, fall, V))
    return out


CHI_MIN, CHI_MAX = 2.6, 12.0           # the true shape's own fit, on n-1 degrees of freedom
LR_TARGET = {"drop": 200.0, "percent": 60.0, "constant": 60.0}


def record_targets(expected, allsep, design, units, plans, bins=True, fixed=None):
    """The complications each embed quarter records.

    The register has to do two things at once. It has to carry honest scatter, so the shape of the fall is
    read off a record that looks like counts of complications rather than a fitted line, and it has to
    separate the shapes the fall could take by well more than that scatter, which the spread of standing
    across the closed placements provides. The assessment-quarter counts are searched over the integers for
    a record whose own fit sits inside an ordinary chi-square band, whose likelihood against each competing
    shape clears its target, and on which every way of pooling the register lands on the same twelve
    whole complications.
    """
    obs = _panel(expected, design, units)
    base = {code: obs[(code, k)] for k, code in W.EMBEDS.items()}
    eligible = [u for u in units if u[10] == "eligible"]

    def excess_of():
        out = {}
        for u in eligible:
            code = u[0]
            qs = [q for q in quarters_for(u) if (code, q) in obs]
            e = sum(expected[(code, q)] for q in qs)
            n = sum(allsep[(code, q)] for q in qs)
            o = sum(obs[(code, q)] for q in qs)
            out[code] = (o / e - 1) * plans[code] * e / n
        return out

    excess = excess_of()
    top = sorted(excess.values(), reverse=True)

    def evaluate(cand):
        for code, v in cand.items():
            obs[(code, W.EMBED_Q[code])] = v
        rows = _register(obs, expected, units)
        rd = _readings(rows)
        md = _models(rows)
        lo, hi = min(rd.values()), max(rd.values())
        pen = 0.0
        chi = md["excess"]
        pen += 60.0 * max(0.0, CHI_MIN - chi) + 60.0 * max(0.0, chi - CHI_MAX)
        for key, target in LR_TARGET.items():
            lr = math.exp(min(60.0, (md[key] - chi) / 2.0))
            pen += 25.0 * max(0.0, math.log(target) - math.log(max(lr, 1e-9)))
        clear = 1.0
        for v in top:
            n0 = round(rd["pooled sums"] * v)
            clear = min(clear, 0.5 - max(abs(lo * v - n0), abs(hi * v - n0)))
        band = (hi - lo) * max(abs(v) for v in top)       # what the planned volumes have to fit in a bin
        if fixed is not None:
            pen += 300.0 * max(0.0, 0.14 - clear)
        else:
            pen += 300.0 * max(0.0, band - 0.62)
        soft = pen + 0.02 * sum(abs(cand[c] - base[c]) for c in cand) + 4.0 * band
        return pen, soft, clear, rd, md

    if fixed is not None:
        pen, soft, clear, rd, md = evaluate(dict(fixed))
        assert pen < 1e-6, ("the chosen record no longer satisfies the register's constraints "
                            "(penalty %.3f, clearance %.3f, chi2 %.2f, LR %s)"
                            % (pen, clear, md["excess"],
                               {k: round(math.exp(min(60.0, (md[k] - md["excess"]) / 2.0)), 1)
                                for k in LR_TARGET}))
        return dict(fixed), rd, md, clear

    best = dict(base)
    best_pen = evaluate(best)[1]
    codes = sorted(base)
    r = np.random.default_rng(W.SEED ^ 0x5EED)
    for start in range(14):
        cand = dict(best) if start == 0 else {c: int(base[c] + r.integers(-14, 15)) for c in codes}
        pen = evaluate(cand)[1]
        improved = True
        while improved:
            improved = False
            for c in codes:
                here = cand[c]
                for step in (-4, -3, -2, -1, 1, 2, 3, 4):
                    cand[c] = here + step
                    p = evaluate(cand)[1]
                    if p < pen - 1e-12:
                        pen, here, improved = p, here + step, True
                cand[c] = here
        if pen < best_pen:
            best_pen, best = pen, dict(cand)
    pen, soft, clear, rd, md = evaluate(best)
    if pen > 1e-6:
        raise AssertionError("no embed-quarter record separates the shapes and pools the same way "
                             "(penalty %.3f, clearance %.3f, chi2 %.2f, LR %s)"
                             % (pen, clear, md["excess"],
                                {k: round(math.exp(min(60.0, (md[k] - md["excess"]) / 2.0)), 1)
                                 for k in LR_TARGET}))
    return best, rd, md, clear


def centre_plans(plans, per_separation, thetas, pick, graded):
    """The planned separations of the eligible units, nudged by a few per cent.

    Every eligible unit's planned volume is moved to the nearest value inside a few per cent that leaves
    the complications a placement there would avoid clear of the whole complication's rounding edge under
    every reading of the closed register, and leaves the unit's expected complications for the quarter
    clear of the edge at the decimal it is shown to. The recommended unit's expected complications are
    cleared on the whole complication as well, which is the figure the write-up states.
    """
    lo, hi = min(thetas.values()), max(thetas.values())
    mid, w = (lo + hi) / 2.0, (hi - lo) * 1.15      # room for the shipped record's own rounding
    for code in graded:
        per = per_separation[code]
        epl = EXPECTED_PER_SEP[code]
        best = None
        for plan in range(int(plans[code] * 0.90), int(plans[code] * 1.10) + 1):
            x = per * plan
            v_lo, v_hi = (mid - w / 2) * x, (mid + w / 2) * x
            n = round(mid * x)
            if round(v_lo) != n or round(v_hi) != n:
                continue
            if 0.5 - max(abs(v_lo - n), abs(v_hi - n)) < 0.175:
                continue
            e = epl * plan
            if 0.05 - abs(e * 10 - round(e * 10)) / 10.0 < 0.0055:
                continue
            if code == pick and 0.5 - abs(e - round(e)) < 0.08:
                continue
            score = (abs(plan - plans[code]),)
            if best is None or score < best[0]:
                best = (score, plan)
        if best is None:
            raise AssertionError("no planned volume centres %s's avoided count" % code)
        plans[code] = best[1]
    return plans


EXPECTED_PER_SEP = {}


def assign_complications(rows, expected, design, units, targets=None):
    """Set each in-scope unit-quarter's complication count to the designed ratio times its expected count,
    and flag exactly that many episodes, each drawn with probability proportional to its stratum rate."""
    by_uq = {}
    for i, row in enumerate(rows):
        if row["in_scope"]:
            by_uq.setdefault((row["unit"], row["q"]), []).append(i)
    embed_q = {v: k for k, v in W.EMBEDS.items()}
    observed = {}
    for (code, q), idx in sorted(by_uq.items()):
        exp = expected[(code, q)]
        ratio = design[code][q]
        target = int(round(exp * ratio))
        if targets and code in targets and embed_q.get(code) == q:
            target = targets[code]
        p = np.array([W.STRATUM_RATE[(W.DRG_BAND[rows[i]["drg"]], rows[i]["age"])] for i in idx])
        r = rng("hac", code, q)
        chosen = r.choice(len(idx), size=min(target, len(idx)), replace=False, p=p / p.sum())
        for c in chosen:
            rows[idx[c]]["hac"] = True
        observed[(code, q)] = int(min(target, len(idx)))
    # a few complications are recorded on episodes the indicator leaves out: real, and outside its scope
    for i, row in enumerate(rows):
        if not row["in_scope"] and row["rstream"] < 0.052:
            rows[i]["hac"] = True
    return observed


def complications(rows, units):
    """Give every episode that recorded a complication its categories.

    One category for most, a second for about a quarter of them, drawn from the group mix of the unit's
    case-mix family and coded on the national list in force at separation. The episode extract carries the
    first category recorded; `hac_detail_extract.csv` carries one row per complication for the three
    hospitals on the clinical information system, and Carrowdean District Hospital, whose module records a
    single complication for an episode, reaches the warehouse only through the extract.
    """
    by_code = {u[0]: u for u in units}
    detail = []
    for i, row in enumerate(rows):
        if not row["hac"]:
            continue
        u = by_code[row["unit"]]
        family = W.MIX_FAMILY[u[3]]
        off_cis = row["unit"] in W.DETAIL_EXCLUDED
        r = rng("comp", row["unit"], row["sep_date"].isoformat(), i)
        mix = W.GROUP_MIX[family]
        groups = list(mix)
        weights = np.array([mix[g] for g in groups], dtype=float)
        weights = weights / weights.sum()
        n = 1
        if not off_cis:
            draw = r.random()
            n = 3 if draw < W.THIRD_COMPLICATION else (2 if draw < W.SECOND_COMPLICATION else 1)
        picked = list(r.choice(len(groups), size=n, replace=False, p=weights)) if n > 1 else \
            [int(r.choice(len(groups), p=weights))]
        table = W.LIST_2026 if row["sep_date"] >= W.CODESET_CHANGE else W.LIST_2022
        codes = []
        for gi in picked:
            g = groups[int(gi)]
            opts = [c for c, _, gg in table if gg == g]
            codes.append(opts[int(r.integers(len(opts)))])
        rows[i]["hac_codes"] = codes
        if not off_cis:
            for k, code in enumerate(codes):
                detail.append(dict(unit=row["unit"], sep_date=row["sep_date"], code=code, seq=k + 1,
                                   onset=row["sep_date"] - dt.timedelta(days=int(r.integers(0, max(1, row["los"])))),
                                   row=i))
    return detail


def add_replays(rows, units):
    """The sub-acute and mental health feed loads each month on an overlapping window, so the episodes
    separated in the last three days of a month arrive again in the next month's batch under fresh episode
    identifiers, with the patient, the admission date and the DRG kept. Acute units load on a closed window
    and carry none of it, asserted."""
    by_code = {u[0]: u for u in units}
    extra = []
    for i, row in enumerate(rows):
        u = by_code[row["unit"]]
        if u[4] == "acute":
            continue
        last = (row["sep_date"].replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
        if (last - row["sep_date"]).days <= 2:
            copy = dict(row)
            copy["replay_of"] = i
            extra.append(copy)
    return extra
