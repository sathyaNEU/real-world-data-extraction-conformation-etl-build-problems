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

import numpy as np

import world as W

MONTH_SHAPE = {  # seasonal shape by calendar month for medical-weighted and surgical-weighted units
    "med": [0.96, 0.94, 0.97, 1.02, 1.06, 1.09, 1.08, 1.05, 1.01, 0.98, 0.95, 0.89],
    "surg": [1.02, 0.93, 1.05, 1.04, 1.03, 1.00, 1.01, 1.02, 1.03, 1.02, 1.04, 0.81],
}
MED_MIXES = {"gen_med", "resp", "renal", "aged", "neuro", "subacute"}
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

    Drawn first as ordinary quarters around each unit's persistent ratio, with the last closed quarter set
    to its designed value; then the network's own quarterly position is levelled (`level_network`); then
    each placement is written on top of the levelled record, so the fall a placement produces is the same
    whether it is read against the unit's own record, against the quarter the placement was decided on,
    against the quarter before it, or against what the rest of the network did over the same quarters.

    A placement writes the five quarters either side of itself; the comparison levelling moves only quarters
    no placement writes, so the two never undo each other. Each round re-reads a placed unit's standing from
    the quarters the levelling has moved, which settles after a couple of passes.
    """
    design = {}
    for u in units:
        code, _, _, mix, _, psi, sep, _, ylast, _, status = u
        qs = quarters_for(u)
        sd = 0.155 if sep < 700 else (0.118 if sep < 1500 else 0.088)
        dev = window_devs(sd, len(qs), None if ylast is None else ylast / psi - 1.0, (code,))
        design[code] = {qs[i]: psi * (1 + dev[i]) for i in range(len(qs))}
    design = level_network(design, units, expected)
    for _ in range(3):
        write_placements(design, units)
        level_comparisons(design, units, expected)
    return design


def placement_window(units):
    """The unit-quarters a placement writes: the two quarters it was taken on, its own quarter and the two
    quarters the unit holds the gain."""
    by_code = {u[0]: u for u in units}
    written = set()
    for k, code in W.EMBEDS.items():
        qs = quarters_for(by_code[code])
        pos = qs.index(k)
        written.update((code, q) for q in (k - 2, k - 1) if q in qs)
        written.update((code, qs[i]) for i in range(pos, min(pos + 1 + len(W.EMBED_RETAIN), len(qs))))
    return written


def write_placements(design, units):
    """Write each placement on top of the levelled record: the two quarters the placement was taken on sit
    at the unit's own standing, the assessment quarter at that standing less the programme's effect, and the
    quarters after it where the unit holds the gain."""
    by_code = {u[0]: u for u in units}
    for k, code in sorted(W.EMBEDS.items()):
        qs = quarters_for(by_code[code])
        pos = qs.index(k)
        pre = qs[:pos]
        quiet = [q for q in pre if q not in (k - 1, k - 2)]
        standing = sum(design[code][q] for q in quiet) / len(quiet)
        for q in (k - 2, k - 1):
            if q in design[code]:
                design[code][q] = standing
        noise = rng("embed", code).normal(0.0, 0.012, 3)
        design[code][k] = 1 + (1 - W.EMBED_EFFECT) * (standing - 1) + noise[0] * (standing - 1)
        for j, keep in enumerate(W.EMBED_RETAIN):
            if pos + 1 + j < len(qs):
                design[code][qs[pos + 1 + j]] = 1 + keep * (standing - 1) + noise[1 + j] * (standing - 1)
    return design



def level_comparisons(design, units, expected):
    """Hold the rest of the network still across each placement's own two quarters.

    A placement's fall has to read the same against the unit's own record and against what the other units
    did over the same two quarters, so for each placement quarter the units whose quarters no placement
    writes are shifted by one common amount that takes the movement of *every* other unit between the
    quarter before the placement and the quarter of the placement to zero, both as a mean across units and
    pooled over their expected complications. The shift is a few thousandths of a ratio. The two readings
    close together because the earlier cohorts' own partial recoveries, which fall inside later placements'
    comparison windows, are carried by the units that are free to move.
    """
    by_code = {u[0]: u for u in units}
    written = placement_window(units)
    acute = [u[0] for u in units if u[4] == "acute"]
    for _ in range(60):
        for k, placed in sorted(W.EMBEDS.items()):
            others = [c for c in acute if c != placed and (c, k) in expected and (c, k - 1) in expected]
            free = [c for c in others if (c, k) not in written]
            if not others or not free:
                continue
            d = {c: design[c][k - 1] - design[c][k] for c in others}
            e = {c: expected[(c, k)] for c in others}
            # the movement to take out: across all the other units, and pooled over their expected counts
            d1 = sum(d[c] for c in others)
            pooled = (sum(expected[(c, k - 1)] * design[c][k - 1] for c in others)
                      / sum(expected[(c, k - 1)] for c in others)
                      - sum(e[c] * design[c][k] for c in others) / sum(e[c] for c in others))
            d2 = pooled * sum(e[c] for c in others)
            n = len(free)
            se = sum(e[c] for c in free)
            see = sum(e[c] * e[c] for c in free)
            det = n * see - se * se
            if abs(det) < 1e-12:
                continue
            a = (d1 * see - se * d2) / det
            b = (n * d2 - se * d1) / det
            for c in free:
                design[c][k] += a + b * e[c]
    return design


def level_network(design, units, expected):
    """Hold the network's own quarterly position flat.

    The network's complication rate does not move quarter to quarter in this period; what moves is where
    the complications sit. Each quarter's mean deviation across the units no placement writes is taken out
    of every unit's ratio in that quarter, both unweighted and pooled over expected complications, which
    leaves each unit's own record where it was and leaves a placement's fall where it was against both its
    own record and the rest of the network.
    """
    written = placement_window(units)
    psi = {u[0]: u[5] for u in units}
    for q in range(len(W.QUARTERS)):
        rowsq = [(code, ratios[q] - psi[code], expected[(code, q)]) for code, ratios in design.items()
                 if q in ratios and (code, q) not in written and (code, q) in expected]
        if len(rowsq) < 3:
            continue
        n = len(rowsq)
        sw = sum(wt for _, _, wt in rowsq)
        sww = sum(wt * wt for _, _, wt in rowsq)
        sd = sum(d for _, d, _ in rowsq)
        swd = sum(wt * d for _, d, wt in rowsq)
        det = n * sww - sw * sw
        if abs(det) < 1e-9:
            continue
        a = (sd * sww - sw * swd) / det
        b = (n * swd - sw * sd) / det
        for code, ratios in design.items():
            if q in ratios and (code, q) in expected:
                ratios[q] -= a + b * expected[(code, q)]
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
                        los = int(1 + r.gamma(2.1, 2.3))
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


def record_targets(expected, allsep, design, units, plans, bins=True, fixed=None):
    """The complications each embed quarter records.

    The programme's effect is read off the closed record, so the record has to price the same programme
    however it is read. The designed counts are moved by at most two complications each, over every
    combination, until the share of standing excess a placement removes is the same under nine readings a
    careful analyst could take: the mean, the median and the expected-weighted mean of the placements' own
    shares, the pooled sums, least squares through the origin and with an intercept, the same pooled share
    measured against the unit's position in the quarter closed at the decision and in the quarter before
    the placement, and a difference against what the other units did over the same two quarters. The search
    runs on integers only and never touches a candidate unit.
    """
    import itertools

    embeds = sorted(W.EMBEDS.items())
    units_by = {u[0]: u for u in units}
    acute = [u[0] for u in units if u[4] == "acute"]

    def o_of(code, q):
        return int(round(expected[(code, q)] * design[code][q]))

    def ratio(code, qs):
        return sum(o_of(code, q) for q in qs) / sum(expected[(code, q)] for q in qs)

    # what every other unit did between the two quarters either side of each placement
    base, P, Pdec, Pprev, E_k, concurrent, concurrent_pooled = [], [], [], [], [], [], []
    for k, code in embeds:
        qs = quarters_for(units_by[code])
        pre = [q for q in qs if q < k]
        ek = expected[(code, k)]
        E_k.append(ek)
        P.append((ratio(code, pre) - 1) * ek)
        Pdec.append((ratio(code, [k - 2]) - 1) * ek)
        Pprev.append((ratio(code, [k - 1]) - 1) * ek)
        base.append(int(round(ek * design[code][k])))
        others = [c for c in acute if c != code and (c, k) in expected and (c, k - 1) in expected]
        moved = [(o_of(c, k - 1) / expected[(c, k - 1)]) - (o_of(c, k) / expected[(c, k)]) for c in others]
        concurrent.append(sum(moved) / len(moved) * ek)
        pooled_move = (sum(o_of(c, k - 1) for c in others) / sum(expected[(c, k - 1)] for c in others)
                       - sum(o_of(c, k) for c in others) / sum(expected[(c, k)] for c in others))
        concurrent_pooled.append(pooled_move * ek)
    P, Pdec, Pprev, E_k, concurrent, concurrent_pooled = (
        np.array(x) for x in (P, Pdec, Pprev, E_k, concurrent, concurrent_pooled))
    rate_base = P + E_k
    excess = []
    for u in units:
        if u[10] != "eligible":
            continue
        code = u[0]
        qs = quarters_for(u)
        e = sum(expected[(code, q)] for q in qs)
        n = sum(allsep[(code, q)] for q in qs)
        excess.append((ratio(code, qs) - 1) * plans[code] * e / n)
    excess = np.array(excess)

    best = None
    space = ([tuple(fixed[code] - base[i] for i, (k, code) in enumerate(embeds))] if fixed
             else itertools.product((0, 1, -1, 2, -2, 3, -3), repeat=len(embeds)))
    for deltas in space:
        O = np.array(base) + np.array(deltas)
        R = O - E_k
        fall = P - R
        shares = fall / P
        if not fixed and (shares.min() < 0.30 or shares.max() > 0.48
                          or shares.max() - shares.min() < 0.030):
            continue
        pm, pv = P.mean(), P.var()
        thetas = {
            "mean of the placements' shares": float(shares.mean()),
            "median of the shares": float(np.median(shares)),
            "expected-weighted mean of the shares": float((E_k * shares).sum() / E_k.sum()),
            "pooled sums": float(fall.sum() / P.sum()),
            "least squares through the origin": float((P * fall).sum() / (P * P).sum()),
            "least squares with an intercept": float(((P - pm) * (fall - fall.mean())).sum() / (pv * len(P))),
            "measured from the quarter closed at the decision": float((Pdec - R).sum() / Pdec.sum()),
            "measured from the quarter before the placement": float((Pprev - R).sum() / Pprev.sum()),
            "against what the other units did over the same quarters":
                float(((Pprev - R) - concurrent).sum() / P.sum()),
            "against the other units pooled over the same quarters":
                float(((Pprev - R) - concurrent_pooled).sum() / P.sum()),
        }
        if not fixed and min(thetas.values()) <= 0:
            continue
        theta = thetas["mean of the placements' shares"]
        lo, hi = min(thetas.values()), max(thetas.values())
        top = np.sort(excess)[::-1][:2]          # the recommendation and the closest unit
        ref = np.round(theta * top)
        clear = float(np.min(0.5 - np.maximum(np.abs(lo * top - ref), np.abs(hi * top - ref))))
        if bins:
            if any(not np.array_equal(ref, np.round(t * top)) for t in thetas.values()):
                continue
            if ref[0] - ref[1] != 6 or clear < 0.12:
                continue
        pred_e = theta * P
        theta_rate = float(fall.sum() / rate_base.sum())
        delta_vol = float(fall.sum() / E_k.sum())
        miss_e = float(np.max(np.abs(pred_e / fall - 1)))
        miss_r = float(np.max(np.abs(theta_rate * rate_base / fall - 1)))
        miss_v = float(np.max(np.abs(delta_vol * E_k / fall - 1)))
        if not fixed and (miss_e > 0.14 or miss_r < 0.55 or miss_v < 0.70):
            continue
        # the band every reading of the register leaves around a count is what has to be narrow, so the
        # record is chosen on the absolute range of the readings and the same way in both passes
        score = (round(hi - lo, 5), sum(abs(d) for d in deltas))
        if best is None or score < best[0]:
            best = (score, {code: int(O[i]) for i, (k, code) in enumerate(embeds)}, thetas, clear)
    if best is None:
        raise AssertionError("no embed-quarter record prices the programme the same way under every "
                             "reading; retune the design")
    return best[1], best[2]


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
            if 0.5 - max(abs(v_lo - n), abs(v_hi - n)) < 0.132:
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
