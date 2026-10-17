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


def window_devs(sd, n, fixed_last, seedparts, level_at=None, cap=0.021, tail4_cap=None):
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
        if level_at is not None and abs(dev[level_at]) > cap:
            continue
        if tail4_cap is not None and n >= 5 and abs(float(dev[-4:].mean())) > tail4_cap:
            continue
        return dev
    return dev


def design_ratios(units):
    """Every unit's designed standardised ratio by quarter.

    Eligible units: deviations around the persistent ratio with the last closed quarter set to the designed
    value. Embedded units: the same over the quarters before the placement, the embed quarter at the
    persistent excess less the programme's effect, and the gain fading over the two quarters after it.
    """
    design = {}
    embed_by_unit = {v: k for k, v in W.EMBEDS.items()}
    for u in units:
        code, _, _, mix, _, psi, sep, _, ylast, _, status = u
        qs = quarters_for(u)
        sd = 0.155 if sep < 700 else (0.118 if sep < 1500 else 0.088)
        k = embed_by_unit.get(code)
        if status == "embedded" and k is not None:
            pos = qs.index(k)
            # the quarter the placement was decided on sits at the unit's own level, so a counterfactual
            # built from the unit's record before the placement does not turn on that one quarter
            dev_pre = window_devs(sd, pos, None, (code, "pre"), level_at=max(0, pos - 2),
                                  tail4_cap=0.024)
            ratios = {qs[i]: psi * (1 + dev_pre[i]) for i in range(pos)}
            noise = rng("embed", code).normal(0.0, 0.055, 3)
            ratios[qs[pos]] = 1 + (1 - W.EMBED_EFFECT) * (psi - 1) + noise[0] * (psi - 1)
            for j, share in enumerate(W.EMBED_RETAIN):
                if pos + 1 + j < len(qs):
                    ratios[qs[pos + 1 + j]] = 1 + share * (psi - 1) + noise[1 + j] * (psi - 1)
            tail = [i for i in range(pos + 1 + len(W.EMBED_RETAIN), len(qs))]
            if tail:
                dev_t = rng("tail", code).normal(0.0, sd, len(tail))
                for j, i in enumerate(tail):
                    ratios[qs[i]] = psi * (1 + dev_t[j])
            design[code] = ratios
            continue
        dev = window_devs(sd, len(qs), None if ylast is None else ylast / psi - 1.0, (code,))
        design[code] = {qs[i]: psi * (1 + dev[i]) for i in range(len(qs))}
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
        code, _, _, mix, service, _, sep, _, _, _, status = u
        shape = MONTH_SHAPE["med" if mix in MED_MIXES else "surg"]
        prate = unit_rate(mix)
        for q in quarters_for(u):
            label, _, _, _, months = W.QUARTERS[q]
            exp_sum, n_scope = 0.0, 0
            recent = []
            for mi, month in enumerate(months):
                r = rng("eps", code, label, mi)
                drift = 1.0 + 0.045 * r.normal()
                n = int(round(sep / 3.0 * shape[month.month - 1] * drift))
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
                    drg = drg_by_band[band][int(r.integers(len(drg_by_band[band])))]
                    same_day = r.random() < SAME_DAY_SHARE
                    ungroup = (not same_day) and r.random() < UNGROUPABLE_SHARE
                    care = "Acute"
                    if service in ("rehabilitation", "psychiatric"):
                        care = "Rehabilitation" if service == "rehabilitation" else "Psychiatric"
                    elif r.random() < NONACUTE_CARE_SHARE:
                        care = "Maintenance" if r.random() < 0.35 else "Rehabilitation"
                    if same_day:
                        los = 0
                        drg = "L61Z" if r.random() < 0.4 else drg
                    else:
                        los = int(1 + r.gamma(2.1, 2.3))
                    if ungroup:
                        drg = "960Z" if r.random() < 0.6 else "961Z"
                    last = (month.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
                    day = int(r.integers(1, last.day + 1))
                    sep_date = month.replace(day=day)
                    pid = "MRN%07d" % (1000000 + int(r.integers(0, 840000)))
                    adm_date = sep_date - dt.timedelta(days=los)
                    # a patient admitted twice on one day for two different procedures, which happens
                    if recent and r.random() < 0.016:
                        prev = recent[int(r.integers(len(recent)))]
                        pid, adm_date = prev[0], prev[1]
                        while drg == prev[2]:
                            drg = drg_by_band[band][int(r.integers(len(drg_by_band[band])))]
                    in_scope = (care == "Acute" and los >= 1 and W.DRG_BAND.get(drg) not in (None, "SAME-DAY")
                                and service == "acute")
                    if in_scope:
                        exp_sum += W.STRATUM_RATE[(W.DRG_BAND[drg], age)]
                        n_scope += 1
                    while (code, pid, adm_date, drg) in used:
                        pid = "MRN%07d" % (1000000 + int(r.integers(0, 840000)))
                    used.add((code, pid, adm_date, drg))
                    recent.append((pid, adm_date, drg))
                    if len(recent) > 6:
                        recent.pop(0)
                    rows.append(dict(unit=code, q=q, qlabel=label, month=month, sep_date=sep_date, los=los,
                                     drg=drg, age=age, care=care, in_scope=in_scope, pid=pid,
                                     adm_date=adm_date,
                                     comorbidity=None if r.random() < BLANK_COMORBIDITY else
                                     int(min(9, max(0, round(r.gamma(1.9, 1.15))))),
                                     hac=False, rstream=float(r.random())))
            expected[(code, q)] = exp_sum
            inscope[(code, q)] = n_scope
    return rows, expected, inscope


def record_targets(expected, allsep, design, units):
    """The complications each embed quarter records.

    The programme's effect is read off the closed record, so the record has to say one thing however it is
    pooled. The designed counts are moved by at most two complications each, over every combination, until
    the share of persistent excess the record implies is the same under pooling, a mean of the placements'
    own shares, their median, a least-squares fit through the origin and two other readings of each unit's
    record before its placement, while the placements' own shares still scatter as counts do. The search runs
    on integers only and never touches a candidate unit.
    """
    import itertools

    embeds = sorted(W.EMBEDS.items())
    units_by = {u[0]: u for u in units}
    base, P, Px, Pw4, E_k = [], [], [], [], []
    for k, code in embeds:
        qs = quarters_for(units_by[code])
        pre = [q for q in qs if q < k]
        o = sum(int(round(expected[(code, q)] * design[code][q])) for q in pre)
        e = sum(expected[(code, q)] for q in pre)
        ratio = o / e
        pre_x = [q for q in pre if q != k - 2]
        ox = sum(int(round(expected[(code, q)] * design[code][q])) for q in pre_x)
        ex = sum(expected[(code, q)] for q in pre_x)
        pre4 = pre[-4:]
        o4 = sum(int(round(expected[(code, q)] * design[code][q])) for q in pre4)
        e4 = sum(expected[(code, q)] for q in pre4)
        ek = expected[(code, k)]
        E_k.append(ek)
        P.append((ratio - 1) * ek)
        Px.append((ox / ex - 1) * ek)
        Pw4.append((o4 / e4 - 1) * ek)
        base.append(int(round(ek * design[code][k])))
    P, Px, Pw4, E_k = (np.array(x) for x in (P, Px, Pw4, E_k))
    rate_base = P + E_k                     # the unit's own expected position: a rival reads the fall off this
    excess = []                             # the candidates' avoidable excess at planned activity
    for u in units:
        if u[10] != "eligible":
            continue
        code, plan = u[0], u[7]
        qs = quarters_for(u)
        o = sum(int(round(expected[(code, q)] * design[code][q])) for q in qs)
        e = sum(expected[(code, q)] for q in qs)
        n = sum(allsep[(code, q)] for q in qs)
        excess.append((o / e - 1) * plan * e / n)
    excess = np.array(excess)

    best = None
    for deltas in itertools.product((0, 1, -1, 2, -2), repeat=len(embeds)):
        O = np.array(base) + np.array(deltas)
        R = O - E_k
        fall = P - R
        shares = fall / P
        if shares.min() < 0.27 or shares.max() > 0.52 or shares.max() - shares.min() < 0.06:
            continue
        thetas = [float(fall.sum() / P.sum()), float(shares.mean()), float(np.median(shares)),
                  float((P * fall).sum() / (P * P).sum()), float(fall.sum() / Px.sum()),
                  float(fall.sum() / Pw4.sum())]
        if min(thetas) <= 0:
            continue
        rounded = [np.round(t * excess) for t in thetas]
        if any(not np.array_equal(rounded[0], r) for r in rounded[1:]):
            continue
        clear = float(np.min(0.5 - np.abs(thetas[0] * excess - np.round(thetas[0] * excess))))
        if clear < 0.10:
            continue
        pred_e = thetas[0] * P
        theta_rate = float(fall.sum() / rate_base.sum())
        delta_vol = float(fall.sum() / E_k.sum())
        miss_e = float(np.max(np.abs(pred_e / fall - 1)))
        miss_r = float(np.max(np.abs(theta_rate * rate_base / fall - 1)))
        miss_v = float(np.max(np.abs(delta_vol * E_k / fall - 1)))
        if miss_e > 0.22 or miss_r < 0.60 or miss_v < 0.80:
            continue
        spread = max(abs(t / thetas[0] - 1) for t in thetas[1:])
        score = (sum(abs(d) for d in deltas), round(spread, 4), -round(clear, 3))
        if best is None or score < best[0]:
            best = (score, {code: int(O[i]) for i, (k, code) in enumerate(embeds)}, thetas, clear)
    if best is None:
        raise AssertionError("no embed-quarter record converges the effect estimators; retune the design")
    return best[1]


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
        n = 1 if off_cis else (2 if r.random() < W.SECOND_COMPLICATION else 1)
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
