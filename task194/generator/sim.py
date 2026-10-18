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
MED_MIXES = {"gen_med", "gen_med_district", "resp", "renal", "aged", "neuro", "subacute"}
# how long a unit's multi-day episodes run, against the network's own shape
LOS_SCALE = {"aged": 1.92, "subacute": 2.35, "neuro": 1.34, "renal": 1.02, "gen_med": 0.94,
             "gen_med_district": 0.88,
             "resp": 1.12, "ortho": 1.44, "gen_surg": 0.97, "colorectal": 1.26, "vasc": 1.18}
SAME_DAY_SHARE = 0.071          # episodes separated the day they were admitted
UNGROUPABLE_SHARE = 0.0118      # episodes the grouper could not assign a valid DRG
NONACUTE_CARE_SHARE = 0.0152    # acute units also report a few rehabilitation or maintenance episodes
BLANK_COMORBIDITY = 0.148       # the comorbidity score is not keyed for every episode
COMORBID_SHAPE = {"U50": 0.85, "50-64": 1.45, "65-79": 2.15, "80+": 2.75}   # older patients carry more
DIALYSIS_MIXES = {"renal", "gen_med", "subacute"}     # the units that separate same-day haemodialysis
# separations fall away over a weekend, hard on a surgical unit and less so on a medical one
WEEKDAY_SHAPE = {"med": [1.10, 1.07, 1.05, 1.08, 1.21, 0.76, 0.69],
                 "surg": [1.16, 1.12, 1.13, 1.18, 1.27, 0.46, 0.34]}
# how willing each kind of unit is to start an episode on a given weekday: a surgical list runs Monday to
# Thursday, a medical unit takes what the emergency department sends it
ADMIT_WEEKDAY = {m: ([0.97, 0.99, 0.97, 0.93, 0.74, 0.40, 0.36] if m in ("ortho", "gen_surg",
                                                                         "colorectal", "vasc")
                     else [0.95, 0.95, 0.94, 0.93, 0.90, 0.80, 0.78])
                 for m in ("ortho", "gen_surg", "colorectal", "vasc", "gen_med", "gen_med_district",
                           "resp", "renal", "aged", "neuro", "subacute")}
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


def path_mult(units, expected_net):
    """Each unit's designed level by quarter, normalised against its own expected numbers.

    A unit in `RATIO_PATH` runs at one level over the first part of the window and another over the last;
    the pair is scaled so the expected-weighted mean is one, which leaves the unit's pooled ratio over the
    ten closed quarters at its persistent ratio.
    """
    out = {}
    for u in units:
        code = u[0]
        if code not in W.RATIO_PATH:
            continue
        m1, m2 = W.RATIO_PATH[code]
        qs = [q for q in quarters_for(u) if (code, q) in expected_net]
        w = {q: expected_net[(code, q)] for q in qs}
        raw = {q: (m1 if q < W.PATH_SPLIT else m2) for q in qs}
        mean = sum(w[q] * raw[q] for q in qs) / sum(w[q] for q in qs)
        for q in qs:
            out[(code, q)] = raw[q] / mean
    return out


def unit_base(units, expected, expected_net, inscope):
    """The published standardised ratio each unit-quarter sits at before its own quarterly shock.

    A unit's complication rate in a risk band is the rate the network itself runs at in that band, which is
    the rate published with specification 4.0 times how far the network has moved in that band since the
    table was set, multiplied by the unit's own practice factor. The published ratio a unit therefore
    reports is its practice factor times the mix-weighted drift of its own patients, so two units with the
    same practice report different published ratios when their patients sit in different bands.
    """
    base = {}
    mult = path_mult(units, expected_net)
    for u in units:
        code, psi = u[0], u[5]
        for q in quarters_for(u):
            if (code, q) not in expected or expected[(code, q)] <= 0:
                continue
            if code == W.ADDITIVE_UNIT:
                # this unit runs at the network's own rate in every band plus a constant per episode, so
                # its excess over the network is the same whatever mix of patients it is sent
                target = expected_net[(code, q)] + W.ADDITIVE_C * inscope[(code, q)]
            else:
                target = expected_net[(code, q)] * psi * mult.get((code, q), 1.0)
            base[(code, q)] = target / expected[(code, q)]
    return base


def design_ratios(units, expected, expected_net, inscope):
    """Every unit's designed published standardised ratio by quarter.

    Each unit-quarter sits at its own base (`unit_base`) plus a quarterly shock sized so the count lands
    about `OVERDISPERSION` Pearson residuals from its expected number, which is what a real indicator does.
    The network's own quarterly position is then levelled, so what moves between quarters is where the
    complications sit rather than how many the network has. The unit whose patients move between quarters
    carries no shock at all, so its record shows a mix effect and nothing else.
    """
    base = unit_base(units, expected, expected_net, inscope)
    design = {}
    for u in units:
        code, _, _, mix, _, psi, sep, _, ylast, _, status = u
        qs = [q for q in quarters_for(u) if (code, q) in base]
        if not qs:
            continue
        if code == W.ADDITIVE_UNIT:
            design[code] = {q: base[(code, q)] for q in qs}
            continue
        e = [max(1.0, expected.get((code, q), 1.0)) for q in qs]
        sd = sum(W.OVERDISPERSION / (psi * x) ** 0.5 for x in e) / len(e)
        last = None if ylast is None else ylast / base[(code, qs[-1])] - 1.0
        dev = window_devs(sd, len(qs), last, (code,))
        design[code] = {qs[i]: base[(code, qs[i])] * (1 + dev[i]) for i in range(len(qs))}
    design = level_network(design, units, expected, base)
    return design


def level_network(design, units, expected, base):
    """Hold the network's own quarterly position flat.

    The network's complication rate does not move quarter to quarter in this period; what moves is where
    the complications sit. Each quarter's pooled deviation from the units' own bases is taken out of every
    unit's ratio in that quarter, which leaves each unit's own record where it was.
    """
    for q in range(len(W.QUARTERS)):
        rows = [(code, ratios[q] - base[(code, q)], expected[(code, q)])
                for code, ratios in design.items()
                if q in ratios and (code, q) in expected and code != W.ADDITIVE_UNIT]
        if len(rows) < 3:
            continue
        shift = sum(wt * d for _, d, wt in rows) / sum(wt for _, _, wt in rows)
        for code, ratios in design.items():
            if q in ratios and (code, q) in expected and code != W.ADDITIVE_UNIT:
                ratios[q] -= shift
    return design


def episodes(units):
    """Every episode row the extract carries, and the expected complications of each in-scope unit-quarter.

    Returns (rows, expected) where rows are dicts in separation order and expected maps (code, q) to the
    summed stratum rates of the unit-quarter's in-scope episodes.
    """
    rows, expected, expected_net, inscope = [], {}, {}, {}
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
            qmix = (W.MIX_SHIFT_PROFILE if code == W.MIX_SHIFT_UNIT and q in W.MIX_SHIFT_QUARTERS
                    else mix)
            wmix_q = {b: drg_weights(code, b, opts) for b, opts in drg_by_band.items() if b}
            exp_sum, exp_net, n_scope = 0.0, 0.0, 0
            recent = []
            for mi, month in enumerate(months):
                r = rng("eps", code, label, mi)
                blank_season = 1.0 + (0.22 if month.month in (1, 7, 12) else -0.07)
                drift = 1.0 + 0.045 * r.normal()
                n = int(round(sep / 3.0 * shape[month.month - 1] * drift))
                last = (month.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
                dayw = []
                for d in range(1, last.day + 1):
                    day = month.replace(day=d)
                    f = wshape[day.weekday()]
                    if (day.month, day.day) in W.PUBLIC_HOLIDAYS:
                        f *= 0.22
                    gf = W.EASTER.get(day.year)
                    if gf is not None and 0 <= (day - gf).days <= 3:
                        f *= 0.26
                    dayw.append(f)
                dayw = np.array(dayw)
                dayw = dayw / dayw.sum()
                for _ in range(n):
                    bands = list(W.MIX[qmix].items())
                    pick = r.random()
                    acc = 0.0
                    band = bands[-1][0]
                    for b, (wt, _) in bands:
                        acc += wt
                        if pick <= acc:
                            band = b
                            break
                    ages = W.MIX[qmix][band][1]
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
                    day = 1 + int(np.searchsorted(np.cumsum(dayw), r.random(), side="left"))
                    sep_date = month.replace(day=min(day, last.day))
                    if same_day:
                        los = 0
                        if mix in DIALYSIS_MIXES and r.random() < 0.46:
                            drg = "L61Z"
                    else:
                        los = int(1 + r.gamma(2.1, 2.3 * LOS_SCALE[mix]))
                        for _ in range(2):
                            adm_wd = (sep_date - dt.timedelta(days=los)).weekday()
                            if r.random() < ADMIT_WEEKDAY[mix][adm_wd]:
                                break
                            los = int(1 + r.gamma(2.1, 2.3 * LOS_SCALE[mix]))
                    if ungroup:
                        drg = "960Z" if r.random() < 0.6 else "961Z"
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
                        rate = W.STRATUM_RATE[(W.DRG_BAND[drg], age)]
                        exp_sum += rate
                        exp_net += rate * W.NETWORK_DRIFT[W.DRG_BAND[drg]]
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
                                     comorbidity=None if r.random() < prof["blank"] * blank_season else
                                     int(min(9, max(0, round(r.gamma(COMORBID_SHAPE[age], 1.15))))),
                                     hac=False, stay=None, rstream=float(r.random())))
            expected[(code, q)] = exp_sum
            expected_net[(code, q)] = exp_net
            inscope[(code, q)] = n_scope
    return rows, expected, expected_net, inscope


EDGE_BAR = 0.15          # a graded figure sits at least this fraction of its rounding unit from the edge


def bin_edge(value, unit=0.1):
    """Distance from a printed cell's nearest edge: the unit's half less the distance to the cell centre.

    The two sum to the unit's half, so computing the distance to the centre and calling it clearance
    reports proximity as room. This returns the edge distance itself.
    """
    scale = round(1.0 / unit)
    centre = round(value * scale) / float(scale)
    return unit / 2.0 - abs(value - centre)


def centre_plans(plans, per_separation, graded, pick, expected_per_sep,
                 count_unit=1.0, rate_unit=0.1):
    """The planned separations of the eligible units, nudged by a few per cent.

    Every eligible unit's planned volume is moved to the nearest value inside a few per cent that leaves
    the avoidable complications its planned activity carries, stated to the nearest whole complication,
    and the complications its patients would be expected to have, stated to one decimal, at least
    EDGE_BAR of their own rounding unit from the edge of their printed cells. Nothing here is fitted:
    each figure is a sum over the record times a volume.
    """
    for code in graded:
        per = per_separation[code]
        epl = expected_per_sep[code]
        best = None
        for plan in range(int(plans[code] * 0.90), int(plans[code] * 1.10) + 1):
            if bin_edge(per * plan, count_unit) < EDGE_BAR * count_unit:
                continue
            if bin_edge(epl * plan, rate_unit) < EDGE_BAR * rate_unit:
                continue
            score = abs(plan - plans[code])
            if best is None or score < best[0]:
                best = (score, plan)
        if best is None:
            raise AssertionError("no planned volume centres %s's avoidable complications" % code)
        plans[code] = best[1]
    return plans


def quarter_index(day):
    """The index into W.QUARTERS of the quarter a date falls in, or None if it is outside the extract."""
    for i, (_, _, start, last, _) in enumerate(W.QUARTERS):
        if start <= day <= last:
            return i
    return None


def statistical_discharges(rows, units):
    """A care type changing inside a stay ends one episode and begins another on the same day.

    The sub-acute and mental health units see this constantly: a patient admitted for rehabilitation whose
    care type is reclassified is statistically discharged and readmitted the same day, so one stay reaches
    the warehouse as two episode records. The patient administration system counts one separation and the
    episode feed carries two, which is why the activity summary's separations for those units sit below the
    extract's rows however the rows are de-duplicated: the two episodes are two episodes. Acute units carry
    none of it, asserted.
    """
    by_code = {u[0]: u for u in units}
    # a stay is recovered from the feed by chaining an episode onto one that ended the same day under the
    # same diagnosis related group, so two genuinely separate stays must never look like that pair. A
    # patient discharged and readmitted on the same day is readmitted under a different group, which is
    # what a regrouping does; the one episode in the record that was not is moved to its band's next code.
    opts = {}
    for code, _, band in W.DRGS:
        if band:
            opts.setdefault(band, []).append(code)
    ends = {}
    for row in rows:
        if by_code[row["unit"]][4] == "acute":
            continue
        ends.setdefault((row["unit"], row["pid"], row["drg"]), set()).add(row["sep_date"])
    for row in rows:
        if by_code[row["unit"]][4] == "acute":
            continue
        key = (row["unit"], row["pid"], row["drg"])
        if row["adm_date"] in ends.get(key, ()):
            band = W.DRG_BAND.get(row["drg"])
            choices = [c for c in opts.get(band, []) if c != row["drg"]]
            if choices:
                row["drg"] = choices[0]
    out = []
    for i, row in enumerate(rows):
        row.setdefault("stay", None)
        if row["stay"] is None:
            row["stay"] = "S%06d" % i
        u = by_code[row["unit"]]
        if u[4] == "acute" or row["los"] < 3:
            out.append(row)
            continue
        rr = rng("statdis", row["unit"], row["sep_date"].isoformat(), i)
        if rr.random() >= 0.071:
            out.append(row)
            continue
        split = int(rr.integers(1, row["los"]))          # nights on the first care type
        first = dict(row)
        first["sep_date"] = row["adm_date"] + dt.timedelta(days=split)
        first["los"] = split
        first["month"] = first["sep_date"].replace(day=1)
        first["hac"] = False
        qi = quarter_index(first["sep_date"])
        if qi is None:
            out.append(row)                              # the split would fall outside the extract
            continue
        first["q"], first["qlabel"] = qi, W.QUARTERS[qi][0]
        second = dict(row)
        second["adm_date"] = first["sep_date"]
        second["los"] = row["los"] - split
        out.append(first)
        out.append(second)
    rows[:] = out
    return sum(1 for r in rows if r["stay"] is not None)


def assign_complications(rows, expected, design, units, targets=None):
    """Set each in-scope unit-quarter's complication count to the designed ratio times its expected count,
    and flag exactly that many episodes, each drawn with probability proportional to its stratum rate."""
    by_uq = {}
    for i, row in enumerate(rows):
        if row["in_scope"]:
            by_uq.setdefault((row["unit"], row["q"]), []).append(i)
    observed = {}
    for (code, q), idx in sorted(by_uq.items()):
        exp = expected[(code, q)]
        ratio = design[code][q]
        target = int(round(exp * ratio))
        # which episodes carry the complications follows the frequency the network itself runs at in the
        # band, not the rate published with the specification, so the record's own stratum frequencies are
        # the network's and not the table's
        p = np.array([W.STRATUM_RATE[(W.DRG_BAND[rows[i]["drg"]], rows[i]["age"])]
                      * W.NETWORK_DRIFT[W.DRG_BAND[rows[i]["drg"]]]
                      * (1.0 + 0.145 * rows[i]["los"]) ** 0.78
                      * (1.0 + 0.11 * (rows[i]["comorbidity"] or 1.4)) for i in idx])
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


def settle_additive(rows, expected, design, units, passes=3):
    """Fix the demonstration unit against the frequency the record itself ends up carrying.

    One unit's own practice has to be flat by construction, so that when its case mix moves its avoidable
    count does not. Its complication count is therefore set to the complications the record's own stratum
    frequencies give its patients, plus one constant per episode, which is its own practice. Those
    frequencies depend on every unit's counts, including this one's, so the definition is a fixed point and
    is reached by iterating it: set the count, re-flag the record, re-measure the frequencies, repeat.
    """
    code = W.ADDITIVE_UNIT
    for _ in range(passes):
        num, den = {}, {}
        for r in rows:
            if not r["in_scope"]:
                continue
            st = (W.DRG_BAND[r["drg"]], r["age"])
            den[st] = den.get(st, 0) + 1
            num[st] = num.get(st, 0) + (1 if r["hac"] else 0)
        rate = {st: num[st] / den[st] for st in den}
        acc, cnt = {}, {}
        for r in rows:
            if r["unit"] == code and r["in_scope"]:
                acc[r["q"]] = acc.get(r["q"], 0.0) + rate[(W.DRG_BAND[r["drg"]], r["age"])]
                cnt[r["q"]] = cnt.get(r["q"], 0) + 1
        for q in acc:
            design[code][q] = (acc[q] + W.ADDITIVE_C * cnt[q]) / expected[(code, q)]
        for r in rows:
            r["hac"] = False
        observed = assign_complications(rows, expected, design, units)
    return observed


_GROUP_MIX_CACHE = {}


def group_mix_for(unit):
    """The reporting groups a unit's complications fall in, given how old its patients are.

    The clinical family's own mix pulled towards the oldest band's profile by the share of the unit's
    episodes in that band, which is a property of the case mix the unit treats rather than a constant set
    per unit.
    """
    code = unit[0]
    if code in _GROUP_MIX_CACHE:
        return _GROUP_MIX_CACHE[code]
    mix = W.MIX[unit[3]]
    oldest = 0.0
    for band, (w, ages) in mix.items():
        oldest += w * ages[W.AGE_BANDS.index("80+")]
    a = min(0.92, W.OLDEST_PULL * oldest)
    base = W.GROUP_MIX[W.MIX_FAMILY[unit[3]]]
    out = {}
    for g in base:
        out[g] = (1.0 - a) * base[g] + a * W.GROUP_MIX_OLDEST.get(g, 0.0)
    tot = sum(out.values())
    out = {g: v / tot for g, v in out.items()}
    _GROUP_MIX_CACHE[code] = out
    return out


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
        mix = group_mix_for(u)
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


def electronic_share(unit, sep_date):
    """How much of a ward's recording sits on the clinical information system on a given day.

    Nothing before its wards were registered, then its own adoption, reached over the three quarters after
    registration as the devices and the practice catch up with each other.
    """
    reg = W.CIS_MIGRATION.get(unit)
    if reg is None or sep_date < reg:
        return 0.0
    settled = W.CIS_ADOPTION.get(unit, W.CIS_SETTLED)
    days = (sep_date - reg).days
    for cut, share in W.CIS_RAMP:
        if days < cut:
            return settled * share
    return settled


def maturity(q):
    """How many closes have passed since a quarter's own close, by the pull date."""
    return W.IMMATURE.get(q, W.LAG_COMPLETE)


def apply_coding_lag(rows, units):
    """Leave in the record only the complications coded by the pull date.

    A complication is coded from what the clinician wrote. Written at the point of care on the clinical
    information system it travels with the episode and is coded in the same cycle; written in the paper
    notes it is coded whenever the coder reaches that chart, so the quarter keeps growing after its own
    coding close. A quarter's shortfall therefore follows how its own wards were recording while its
    patients were in them, which moves quarter by quarter as the system's rollout reaches each ward.

    Returns the coded counts per unit-quarter, the ultimate counts, and the count each unit-quarter stood
    at at every close after its own, which is what the coding close-out register publishes.
    """
    ultimate = {}
    vintage = {}
    for i, row in enumerate(rows):
        if not row["hac"] or not row["in_scope"]:
            continue
        key = (row["unit"], row["q"])
        ultimate[key] = ultimate.get(key, 0) + 1
        e = electronic_share(row["unit"], row["sep_date"])
        r = rng("lag", row["unit"], row["sep_date"].isoformat(), i)
        curve = W.ELEC_COMPLETENESS if r.random() < e else W.PAPER_COMPLETENESS
        u = float(r.random())
        lag = W.LAG_COMPLETE
        for k, c in enumerate(curve):
            if u < c:
                lag = k
                break
        rows[i]["coding_lag"] = lag
        for k in range(lag, W.LAG_COMPLETE + 1):
            vintage[(row["unit"], row["q"], k)] = vintage.get((row["unit"], row["q"], k), 0) + 1
        if lag > maturity(row["q"]):
            rows[i]["hac"] = False          # documented, and coded, after the pull date
            rows[i]["hac_codes"] = []
    observed = {}
    for row in rows:
        if not row["in_scope"]:
            continue
        key = (row["unit"], row["q"])
        observed[key] = observed.get(key, 0) + (1 if row["hac"] else 0)
    return observed, ultimate, vintage


def add_replays(rows, units):
    """The sub-acute and mental health feed loads each month on an overlapping window, so the episodes
    separated in the last three days of a month arrive again in the next month's batch under fresh episode
    identifiers. The second load carries the same patient, the same admission and separation dates, the
    same stay and the same diagnosis related group, so the separation key the dictionary states collapses
    it exactly and the de-duplicated extract ties to the activity summary; what the second load sometimes
    loses is the comorbidity score, which the feed does not always carry. Acute units load on a closed
    window and carry none of it, asserted."""
    by_code = {u[0]: u for u in units}
    extra = []
    for i, row in enumerate(rows):
        u = by_code[row["unit"]]
        if u[4] == "acute":
            continue
        last = (row["sep_date"].replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
        if (last - row["sep_date"]).days <= 2:
            rr = rng("replay", row["unit"], row["sep_date"].isoformat(), i)
            for j in range(2 if rr.random() < 0.085 else 1):
                copy = dict(row)
                copy["replay_of"] = i
                if rr.random() < 0.14:
                    copy["comorbidity"] = None
                extra.append(copy)
    return extra
