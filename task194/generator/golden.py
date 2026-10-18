"""The answer, computed from the shipped bundle only.

Nothing here reads the generator's state: every figure comes out of the files under target/ the way a solver
would build it, so the goldens, the write-up and the verifier all stand on the bundle.
"""
import csv
import datetime as dt
import math
import os
from collections import OrderedDict, defaultdict

REF_RATE = 96.6                      # specification 3.2, read back from the bundle below
SPEC_START = dt.date(2024, 7, 1)
ASSESS_QUARTER = "2026-27 Q4"


def _read(target, name):
    with open(os.path.join(target, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _d(s):
    return dt.date.fromisoformat(s)


def fiscal(day):
    """(fiscal year label, quarter label) of a date, on 1 July to 30 June years."""
    fy = day.year if day.month >= 7 else day.year - 1
    qn = {7: 1, 8: 1, 9: 1, 10: 2, 11: 2, 12: 2, 1: 3, 2: 3, 3: 3, 4: 4, 5: 4, 6: 4}[day.month]
    label = "%d-%02d" % (fy, (fy + 1) % 100)
    return label, "%s Q%d" % (label, qn)


def load(target):
    """The bundle, conformed: the indicator panel, the registers and the plan."""
    units = {r["unit_code"]: r for r in _read(target, "unit_register.csv")}
    bands = {r["drg_code"]: r["risk_band"] for r in _read(target, "drg_risk_bands.csv")}
    strata = {(r["risk_band"], r["age_band"]): float(r["expected_rate"])
              for r in _read(target, "hac_stratum_rates.csv")}
    plan = {r["unit_code"]: int(r["planned_separations"]) for r in _read(target, "activity_plan_2027q4.csv")}
    placements = _read(target, "improvement_placements.csv")
    summary = _read(target, "activity_summary_monthly.csv")
    facility = {(r["unit_code"], r["month"]): r["facility"] for r in summary}

    peer = {r["hospital_code"]: r["peer_group"] for r in _read(target, "hospital_sites.csv")}
    closeout = _read(target, "coding_close_out_register.csv")
    catgroup = {}
    groups_order = []
    for r in _read(target, "hac_category_list.csv"):
        catgroup[(r["list_revision"], r["complication_code"])] = r["group_id"]
        if r["group_id"] not in groups_order:
            groups_order.append(r["group_id"])
    groups_order.sort()
    panel = defaultdict(lambda: dict(episodes=0, observed=0.0, expected=0.0, separations=0))
    sc = defaultdict(lambda: defaultdict(lambda: [0, 0]))   # (unit, q) -> stratum -> [episodes, with HAC]
    monthly = defaultdict(lambda: [0, 0])      # (unit, month) -> [in-scope episodes, observed complications]
    ug = defaultdict(int)                      # (unit, q, group) -> episodes whose first complication is in it
    nonacute_rows = []
    groups_by_year = defaultdict(lambda: defaultdict(set))
    seen = set()
    inscope_episode = {}
    with open(os.path.join(target, "episode_outcomes_extract.csv"), newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            unit = row["unit_code"]
            u = units[unit]
            sep = _d(row["separation_date"])
            fy, q = fiscal(sep)
            key = (unit, row["patient_uid"], row["admission_date"], row["drg_code"])
            band = bands.get(row["drg_code"], "")
            in_scope = (row["care_type"] == "Acute" and int(row["los_days"]) >= 1 and band not in ("", "SAME-DAY")
                        and u["service_type"] == "Acute inpatient")
            hac = row["hac_recorded"] == "1"
            if u["service_type"] != "Acute inpatient":
                # the sub-acute feed re-sends a block of records on an overlapping window, so a record is
                # counted once on the separation key the dictionary states; and a stay whose care type
                # changed inside it reaches the feed as two episode records, which that key cannot see,
                # so the episodes are chained into stays below
                nonacute_rows.append(dict(unit=unit, pid=row["patient_uid"], adm=_d(row["admission_date"]),
                                          sep=sep, drg=row["drg_code"], hac=hac))
                continue
            if key in seen:
                raise AssertionError("repeated separation key in an acute unit: %s" % (key,))
            seen.add(key)
            p = panel[(unit, q)]
            p["separations"] += 1
            if in_scope:
                p["episodes"] += 1
                p["expected"] += strata[(band, row["age_band"])]
                p["observed"] += 1 if hac else 0
                cell = sc[(unit, q)][(band, row["age_band"])]
                cell[0] += 1
                cell[1] += 1 if hac else 0
                m = monthly[(unit, sep.replace(day=1).isoformat())]
                m[0] += 1
                m[1] += 1 if hac else 0
                if hac and row["hac_category_code"]:
                    rev = "2026" if sep >= dt.date(2026, 7, 1) else "2022"
                    ug[(unit, q, ("rev", rev, row["hac_category_code"]))] += 1
                inscope_episode[row["episode_id"]] = (unit, sep, fy)
                if hac and row["hac_category_code"] and fy in ("2025-26", "2026-27"):
                    groups_by_year[fy]["principal:" + row["hac_category_code"]].add(row["episode_id"])
    return dict(units=units, bands=bands, strata=strata, plan=plan, placements=placements, peer=peer,
                sc={k: dict(v) for k, v in sc.items()}, monthly_inscope=dict(monthly),
                unit_group_raw=dict(ug), closeout=closeout, catgroup=catgroup,
                groups_order=groups_order,
                panel=dict(panel), nonacute=stays(nonacute_rows),
                principal=dict(groups_by_year), facility=facility, summary=summary,
                inscope_episode=inscope_episode)


def excluded_activity(b, year=2026):
    """What the complication indicator leaves out at each hospital, in a calendar year.

    Specification 2.1 to 2.3 keep an acute inpatient episode of one night or more whose diagnosis related
    group the risk band map assigns to a band. A hospital's separations therefore divide into the episodes
    the indicator measures and the rest: same-day separations, episodes whose care type is not acute,
    episodes the grouper could not group, and every separation of a unit the indicator does not cover at
    all. The rest is counted over all of a site's activity, because the question is what the indicator
    leaves out of a hospital rather than what it leaves out of the units it reports on.

    The rest is not counted off the episode extract. The extract is one row per episode record the
    warehouse received, and the warehouse is not the system that counts separations: the activity summary
    is, and it counts every care type. So the excluded separations of a unit-month are the separations the
    activity summary reports less the in-scope episodes the indicator measured, and the excluded ones that
    recorded a complication are the summary's affected separations less the complications the indicator
    observed. Each unit-month is counted to the site that unit reported under in that month, which is the
    summary's own column.
    """
    inscope = b["monthly_inscope"]
    out = defaultdict(lambda: dict(reported=0, measured=0, separations=0, with_complication=0))
    for r in b["summary"]:
        month = r["month"]
        if int(month[:4]) != year:
            continue
        unit = r["unit_code"]
        n, o = inscope.get((unit, month), [0, 0])
        site = r["facility"]
        cell = out[site]
        cell["reported"] += int(r["separations"])
        cell["measured"] += n
        cell["separations"] += int(r["separations"]) - n
        cell["with_complication"] += int(r["episodes_with_complication"]) - o
    return dict(out)


def stays(rows):
    """The separations the sub-acute and mental health units reported, by quarter.

    Two steps, and the second is the one the stated key cannot do. First, the feed's overlapping monthly
    load re-sends a record under a fresh episode identifier, so records are counted once on the separation
    key the dictionary states: unit, patient, admission date and diagnosis related group. Second, a stay
    whose care type changed inside it reaches the feed as two episode records, one ending and one beginning
    on the same day under the same diagnosis related group, and the patient left the hospital once: those
    episodes are chained into one stay,
    which is what the activity summary counts and what the question asks for. The stay falls in the quarter
    its last episode separated in.
    """
    seen = set()
    rec = defaultdict(list)
    for r in rows:
        key = (r["unit"], r["pid"], r["adm"], r["drg"])
        if key in seen:
            continue                      # the overlapping load's second copy
        seen.add(key)
        rec[(r["unit"], r["pid"])].append(r)
    out = defaultdict(lambda: dict(seps=0, hac=0))
    for key, eps in rec.items():
        eps.sort(key=lambda r: (r["adm"], r["sep"]))
        chains = []
        ends = {}
        for r in eps:
            j = ends.pop((r["adm"], r["drg"]), None)
            if j is None:                 # a stay of this patient's begins here
                chains.append([r])
                j = len(chains) - 1
            else:                         # the care type changed inside a stay already open
                chains[j].append(r)
            ends[(r["sep"], r["drg"])] = j
        for chain in chains:
            q = fiscal(chain[-1]["sep"])[1]
            out[q]["seps"] += 1
            out[q]["hac"] += 1 if any(x["hac"] for x in chain) else 0
    return dict(out)


def quarters(panel, unit):
    return sorted(q for (u, q) in panel if u == unit)


def pooled(panel, unit, qs):
    o = sum(panel[(unit, q)]["observed"] for q in qs)
    e = sum(panel[(unit, q)]["expected"] for q in qs)
    return (o / e) if e else 0.0, o, e


def eligible_units(b):
    """Charter 4.2: an acute inpatient unit with four or more closed quarters on the current specification,
    and no placement in the previous twelve closed quarters."""
    placed = {p["unit_code"] for p in b["placements"]}
    out = []
    for code, u in b["units"].items():
        if u["service_type"] != "Acute inpatient" or u["closed_date"]:
            continue
        qs = quarters(b["panel"], code)
        if len(qs) < 4 or code in placed:
            continue
        out.append(code)
    return sorted(out)


def _closeout_series(rows):
    """Each cost centre's quarter as the register published and restated it, oldest publication first."""
    series = defaultdict(list)
    for r in rows:
        series[(r["quarter"], r["unit_code"])].append(
            (r["published_date"], int(r["separations_with_complication"])))
    for k in series:
        series[k].sort()
    return series


def development_factors(rows, weighting="volume", quarters_from=None):
    """What a quarter's complication count grows to after its own close, measured per cost centre.

    The close-out register publishes each quarter when its coding closes and restates it at every close
    after that, counted on the separations that carried a complication against the cost centre. A quarter
    that has stopped moving, its last two publications agreeing, carries its own ultimate, so the growth
    from each earlier publication to that ultimate is an observed ratio. Nothing is fitted and no parameter
    is chosen: `weighting` only says whether the ratios are pooled over the finished quarters or averaged
    across them, `quarters_from` only says whether the finished quarters are all of them or the later ones,
    and the readings are asserted to agree.
    """
    series = _closeout_series(rows)
    num = defaultdict(float)
    den = defaultdict(float)
    ratios = defaultdict(list)
    for (q, unit), s_ in series.items():
        if len(s_) < 2 or s_[-1][1] != s_[-2][1]:
            continue                       # the quarter is still moving, so it cannot measure its own
        if quarters_from is not None and q < quarters_from:
            continue
        final = s_[-1][1]
        for lag, (_, n) in enumerate(s_):
            if n <= 0:
                continue
            num[(unit, lag)] += final
            den[(unit, lag)] += n
            ratios[(unit, lag)].append(final / n)
    if weighting == "simple":
        return {k: sum(v) / len(v) for k, v in ratios.items() if v}
    return {k: num[k] / den[k] for k in den if den[k]}


def immature_lags(rows):
    """Which quarters are still short, and how many closes each has had, from the register alone."""
    pubs = defaultdict(set)
    moving = defaultdict(bool)
    series = _closeout_series(rows)
    for r in rows:
        pubs[r["quarter"]].add(r["published_date"])
    for (q, unit), s_ in series.items():
        if len(s_) < 2 or s_[-1][1] != s_[-2][1]:
            moving[q] = True
    return {q: len(pubs[q]) - 1 for q in pubs if moving.get(q)}


def blended_factor(rows, lag):
    """One factor for the whole network at a lag, ignoring which cost centre the complications sat in."""
    series = _closeout_series(rows)
    num = den = 0.0
    for (q, unit), s_ in series.items():
        if len(s_) < 2 or s_[-1][1] != s_[-2][1]:
            continue
        if lag >= len(s_) or s_[lag][1] <= 0:
            continue
        num += s_[-1][1]
        den += s_[lag][1]
    return num / den if den else 1.0


def unit_groups(b):
    """Each unit-quarter's affected episodes by the group of their first recorded complication.

    The code is read against the national list revision in force at separation, Appendix B, so an episode
    coded HAC13 before 1 July 2026 and one coded HAC03 after it fall in the same group.
    """
    out = defaultdict(int)
    for (unit, q, key), n in b["unit_group_raw"].items():
        _, rev, code = key
        g = b["catgroup"].get((rev, code))
        if g:
            out[(unit, q, g)] += n
    return dict(out)


def developed(b, code, qs, factors, lags, groups=None):
    """A unit's complications over `qs`, developed to what those quarters' patients had."""
    total = 0.0
    for q in qs:
        p = b["panel"].get((code, q))
        if p is None:
            continue
        if q not in lags:
            total += p["observed"]
            continue
        total += p["observed"] * factors.get((code, lags[q]), 1.0)
    return total


def avoidable(b, code, qs, factors, lags, groups=None, develop=True):
    """Charter 4.3 carried onto the planned separations under specification 3.4.

    The complications the unit's patients had, less the complications the published stratum rates of
    Appendix A give the same patients, counted patient by patient and summed, then carried onto the
    quarter's planned separations at the unit's own rate per separation.
    """
    o = sum(b["panel"][(code, q)]["observed"] for q in qs if (code, q) in b["panel"])
    e = sum(b["panel"][(code, q)]["expected"] for q in qs if (code, q) in b["panel"])
    sp = sum(b["panel"][(code, q)]["separations"] for q in qs if (code, q) in b["panel"])
    if not sp:
        return 0.0
    if develop:
        o = developed(b, code, qs, factors, lags, groups)
    return (o - e) * b["plan"][code] / sp


def all_quarters(b):
    return sorted({q for (_, q) in b["panel"]})


def standings(b):
    """Every eligible unit on charter 4.3, developed and as recorded."""
    elig = eligible_units(b)
    rows = _read_closeout(b)
    factors = development_factors(rows)
    lags = immature_lags(rows)
    groups = unit_groups(b)
    allq = set(all_quarters(b))
    out = []
    for code in elig:
        qs = {q for q in allq if (code, q) in b["panel"]}
        o = sum(b["panel"][(code, q)]["observed"] for q in qs)
        e = sum(b["panel"][(code, q)]["expected"] for q in qs)
        n = sum(b["panel"][(code, q)]["episodes"] for q in qs)
        sp = sum(b["panel"][(code, q)]["separations"] for q in qs)
        dev = developed(b, code, qs, factors, lags, groups)
        plan = b["plan"][code]
        k = plan / sp
        out.append(dict(
            unit=code, name=b["units"][code]["unit_name"], hospital=b["units"][code]["hospital_code"],
            quarters=len(qs), observed=o, developed=dev, expected=e, episodes=n, separations=sp, plan=plan,
            avoidable=(dev - e) * k,
            as_recorded=(o - e) * k,
            uplift=dev - o,
            completeness=o / dev if dev else 1.0,
            ratio=o / e, ratio_developed=dev / e,
            expected_plan=e / sp * plan,
            adjusted_rate=o / e * REF_RATE,
            se=math.sqrt(dev) * k))
    out.sort(key=lambda d: -d["avoidable"])
    return out, factors, lags, groups


def _read_closeout(b):
    return b["closeout"]


def stays(rows):
    """The separations the sub-acute and mental health units reported, by quarter.

    Two steps, and the second is the one the stated key cannot do. First, the feed's overlapping monthly
    load re-sends a record under a fresh episode identifier, so records are counted once on the separation
    key the dictionary states: unit, patient, admission date and diagnosis related group. Second, a stay
    whose care type changed inside it reaches the feed as two episode records, one ending and one beginning
    on the same day under the same diagnosis related group, and the patient left the hospital once: those
    episodes are chained into one stay,
    which is what the activity summary counts and what the question asks for. The stay falls in the quarter
    its last episode separated in.
    """
    seen = set()
    rec = defaultdict(list)
    for r in rows:
        key = (r["unit"], r["pid"], r["adm"], r["drg"])
        if key in seen:
            continue                      # the overlapping load's second copy
        seen.add(key)
        rec[(r["unit"], r["pid"])].append(r)
    out = defaultdict(lambda: dict(seps=0, hac=0))
    for key, eps in rec.items():
        eps.sort(key=lambda r: (r["adm"], r["sep"]))
        chains = []
        ends = {}
        for r in eps:
            j = ends.pop((r["adm"], r["drg"]), None)
            if j is None:                 # a stay of this patient's begins here
                chains.append([r])
                j = len(chains) - 1
            else:                         # the care type changed inside a stay already open
                chains[j].append(r)
            ends[(r["sep"], r["drg"])] = j
        for chain in chains:
            q = fiscal(chain[-1]["sep"])[1]
            out[q]["seps"] += 1
            out[q]["hac"] += 1 if any(x["hac"] for x in chain) else 0
    return dict(out)


def quarters(panel, unit):
    return sorted(q for (u, q) in panel if u == unit)


def pooled(panel, unit, qs):
    o = sum(panel[(unit, q)]["observed"] for q in qs)
    e = sum(panel[(unit, q)]["expected"] for q in qs)
    return (o / e) if e else 0.0, o, e


def eligible_units(b):
    """Charter 4.2: an acute inpatient unit with four or more closed quarters on the current specification,
    and no placement in the previous twelve closed quarters."""
    placed = {p["unit_code"] for p in b["placements"]}
    out = []
    for code, u in b["units"].items():
        if u["service_type"] != "Acute inpatient" or u["closed_date"]:
            continue
        qs = quarters(b["panel"], code)
        if len(qs) < 4 or code in placed:
            continue
        out.append(code)
    return sorted(out)


def net_rates(b, qs=None, exclude_unit=None, hospital=None, peer=None, floor=30):
    """The frequency patients of each stratum ordinarily have, measured from the record itself.

    Charter 4.3 asks for the complications that patients of the same risk band and age band ordinarily
    have. No file carries them: this is the sum over the acute record's own in-scope episodes, by stratum.
    `hospital` and `peer` restrict the comparison population, which charter 4.3 does not do; they are here
    so the readings that restrict it can be measured and shown to be ruled out rather than asserted to be.
    """
    num = defaultdict(float)
    den = defaultdict(float)
    for (unit, q), counts in b["sc"].items():
        if qs is not None and q not in qs:
            continue
        if exclude_unit is not None and unit == exclude_unit:
            continue
        h = b["units"][unit]["hospital_code"]
        if hospital is not None and h != hospital:
            continue
        if peer is not None and b["peer"][h] != peer:
            continue
        for st, (n, o) in counts.items():
            den[st] += n
            num[st] += o
    rates = {st: num[st] / den[st] for st in den if den[st] > 0}
    if hospital is not None or peer is not None:
        wide = net_rates(b, qs=qs)[0]           # a thin stratum falls back to the whole record
        rates = {st: (rates[st] if den.get(st, 0) >= floor else wide[st]) for st in wide}
    return rates, dict(den)


def _own_ratio_fill(b, code, qs, lags):
    """The short quarters filled at the unit's own standardised ratio over the quarters that have finished.

    A reading that takes the unit's position as settled: whatever ratio its finished quarters ran at, its
    short quarters ran at too, so the missing complications are the ones that ratio implies.
    """
    fin = [q for q in qs if q not in lags]
    o_f = sum(b["panel"][(code, q)]["observed"] for q in fin)
    e_f = sum(b["panel"][(code, q)]["expected"] for q in fin)
    r = (o_f / e_f) if e_f else 1.0
    o = o_f + sum(b["panel"][(code, q)]["expected"] * r for q in qs if q in lags)
    e = sum(b["panel"][(code, q)]["expected"] for q in qs)
    sp = sum(b["panel"][(code, q)]["separations"] for q in qs)
    return (o - e) * b["plan"][code] / sp if sp else 0.0


def routes(b, factors, lags, groups=None):
    """The route a response takes to the ranking, and the unit each one names.

    Every figure is a count the record carries or a count developed by a ratio the register prints. No
    functional form is chosen anywhere and there is no free parameter to estimate. Each rung is the same
    quantity in the same unit, complications on the quarter's planned separations, so the rungs' margins
    are comparable.
    """
    elig = eligible_units(b)
    allq = set(all_quarters(b))
    rows = b["closeout"]
    out = OrderedDict()

    def add(label, fn):
        v = {c: fn(c) for c in elig}
        order = sorted(v, key=lambda c: -v[c])
        out[label] = dict(first=order[0], first_value=v[order[0]], second=order[1],
                          second_value=v[order[1]],
                          margin=v[order[0]] / v[order[1]] if v[order[1]] > 0 else None, order=order)

    def qs(c):
        return {q for q in allq if (c, q) in b["panel"]}

    add("R0 the complications the record carries over the ten closed quarters",
        lambda c: avoidable(b, c, qs(c), factors, lags, develop=False))
    last4 = sorted(allq)[-4:]
    add("R1 the record as it stands over the four most recent closed quarters",
        lambda c: avoidable(b, c, {q for q in qs(c) if q in last4}, factors, lags, develop=False))
    add("R2 only the quarters whose coding has stopped moving",
        lambda c: avoidable(b, c, {q for q in qs(c) if q not in lags}, factors, lags, develop=False))
    one = {k: blended_factor(rows, v) for k, v in lags.items()}
    add("R3 one network factor at each lag, ignoring which cost centre the complications sat in",
        lambda c: _blended_avoidable(b, c, qs(c), one, lags))
    add("R4 the short quarters filled at the unit's own ratio over the quarters that have finished",
        lambda c: _own_ratio_fill(b, c, qs(c), lags))
    add("R5 the complications the quarters' patients had, developed on each cost centre's own record",
        lambda c: avoidable(b, c, qs(c), factors, lags))
    return out


def _blended_avoidable(b, code, qs, one, lags):
    o = e = sp = 0.0
    for q in qs:
        p = b["panel"][(code, q)]
        e += p["expected"]
        sp += p["separations"]
        o += p["observed"] * (one.get(q, 1.0) if q in lags else 1.0)
    return (o - e) * b["plan"][code] / sp if sp else 0.0


def convergence(b, groups):
    """Every reading of the development the register leaves open, each formed and ranked.

    The register says what each quarter carried at each publication; it does not say how to pool the
    finished quarters' ratios, how many of them to use, or whether to read the growth to the ultimate in
    one step or through the intervening publication. Each reading is formed here so a parameter change that
    breaks the convergence fails the build (C1, `determinism-check` section 3).
    """
    rows = b["closeout"]
    lags = immature_lags(rows)
    allq = set(all_quarters(b))
    elig = eligible_units(b)
    readings = OrderedDict()

    def add(label, factors, lg=None):
        v = {c: avoidable(b, c, {q for q in allq if (c, q) in b["panel"]}, factors, lg or lags, groups)
             for c in elig}
        order = sorted(v, key=lambda c: -v[c])
        readings[label] = dict(first=order[0], first_value=v[order[0]], second=order[1],
                               second_value=v[order[1]],
                               margin=v[order[0]] / v[order[1]] if v[order[1]] > 0 else None)

    add("the finished quarters' ratios pooled over their counts", development_factors(rows, "volume"))
    add("the finished quarters' ratios averaged across the quarters", development_factors(rows, "simple"))
    add("only the finished quarters from 2025-26 on",
        development_factors(rows, "volume", quarters_from="2025-26"))
    add("only the finished quarters from 2025-26 on, averaged",
        development_factors(rows, "simple", quarters_from="2025-26"))
    add("the growth read through the intervening publication rather than in one step",
        _chained_factors(rows))
    return readings


def _chained_factors(rows):
    """Each cost centre's development read step by step: the growth from one publication to the next,
    multiplied out to the ultimate, rather than read from a publication to the ultimate in one step."""
    series = _closeout_series(rows)
    num = defaultdict(float)
    den = defaultdict(float)
    for (q, unit), s_ in series.items():
        if len(s_) < 2 or s_[-1][1] != s_[-2][1]:
            continue
        for lag in range(len(s_) - 1):
            if s_[lag][1] <= 0:
                continue
            num[(unit, lag)] += s_[lag + 1][1]
            den[(unit, lag)] += s_[lag][1]
    step = {k: num[k] / den[k] for k in den if den[k]}
    out = {}
    units = {u for (u, _) in step}
    for u in units:
        lags = sorted(l for (uu, l) in step if uu == u)
        for l in lags:
            f = 1.0
            for m in lags:
                if m >= l:
                    f *= step[(u, m)]
            out[(u, l)] = f
    return out


def compute(target):
    b = load(target)
    units, factors, lags, groups = standings(b)
    answer, runner = units[0], units[1]
    third = units[2]
    rts = routes(b, factors, lags, groups)
    conv = convergence(b, groups)
    elig = eligible_units(b)
    by = {d["unit"]: d for d in units}
    rung0 = by[rts["R0 the complications the record carries over the ten closed quarters"]["first"]]
    rung1 = by[rts["R3 one network factor at each lag, ignoring which cost centre the complications sat in"]
               ["first"]]
    se_gap = math.sqrt(answer["se"] ** 2 + runner["se"] ** 2)
    se_gap3 = math.sqrt(answer["se"] ** 2 + third["se"] ** 2)

    # ask 2: what the indicator leaves out at each hospital, in the year ended 31 December 2026
    sites = {r["hospital_code"]: r["hospital_name"] for r in _read(target, "hospital_sites.csv")}
    exc = excluded_activity(b)
    hosp = []
    for code in sorted(exc):
        y = exc[code]
        hosp.append(dict(hospital=code, name=sites[code], reported=y["reported"],
                         measured=y["measured"], separations=y["separations"],
                         complications=y["with_complication"]))

    # ask 3: the units outside the indicator, by quarter
    outside = []
    for q in sorted(b["nonacute"]):
        seps = b["nonacute"][q]["seps"]
        hac = b["nonacute"][q]["hac"]
        outside.append(dict(quarter=q, separations=seps, with_complication=hac,
                            per_1000=hac / seps * 1000))

    # ask 4: the complication groups, by fiscal year
    cat_group, group_names = {}, {}
    for r in _read(target, "hac_category_list.csv"):
        cat_group[(r["list_revision"], r["complication_code"])] = r["group_id"]
        group_names[r["group_id"]] = r["group_name"]
    found = defaultdict(lambda: defaultdict(set))
    detail_units = set()
    for r in _read(target, "hac_detail_extract.csv"):
        detail_units.add(r["unit_code"])
        eid = r["episode_id"]
        if eid not in b["inscope_episode"]:
            continue
        unit, sep, fy = b["inscope_episode"][eid]
        if fy not in ("2025-26", "2026-27"):
            continue
        rev = "2026" if sep >= dt.date(2026, 7, 1) else "2022"
        found[fy][cat_group[(rev, r["complication_code"])]].add(eid)
    # the detail extract covers the units on the clinical information system; the complications of the units
    # it does not reach are in the extract's own category column, one to an episode
    for fy, principal in b["principal"].items():
        if fy not in ("2025-26", "2026-27"):
            continue
        for key, eids in principal.items():
            code = key.split(":", 1)[1]
            for eid in eids:
                unit, sep, _ = b["inscope_episode"][eid]
                if unit in detail_units:
                    continue
                rev = "2026" if sep >= dt.date(2026, 7, 1) else "2022"
                found[fy][cat_group[(rev, code)]].add(eid)
    groups_year = []
    for gid in sorted(group_names):
        groups_year.append(dict(group=gid, name=group_names[gid],
                           fy2025=len(found["2025-26"][gid]), fy2026=len(found["2026-27"][gid])))

    return dict(units=units, answer=answer, runner=runner, third=third, eligible=elig,
                factors=factors, lags=lags, groups=groups, routes=rts, convergence=conv,
                rung0=rung0, rung1=rung1, rung2=answer,
                hospitals=hosp, outside=outside, groups_by_year=groups_year,
                gap=answer["avoidable"] - runner["avoidable"],
                margin=answer["avoidable"] / runner["avoidable"],
                se_gap=se_gap, se_lead=(answer["avoidable"] - runner["avoidable"]) / se_gap,
                se_lead_third=(answer["avoidable"] - third["avoidable"]) / se_gap3,
                recorded_rank=[d["unit"] for d in sorted(units, key=lambda x: -x["as_recorded"])]
                .index(answer["unit"]) + 1,
                bundle=b)


# Appendix B of the specification: the 2022 revision's codes and the groups they belong to. The 2026
# revision renumbered HAC03 to HAC06 and folded HAC13 into HAC03, so a code is read against the revision in
# force at separation.
LIST_2022_GROUPS = {"HAC01": "G1", "HAC02": "G1", "HAC03": "G2", "HAC04": "G3", "HAC05": "G4",
                    "HAC06": "G4", "HAC07": "G5", "HAC08": "G6", "HAC09": "G6", "HAC10": "G7",
                    "HAC11": "G8", "HAC12": "G8", "HAC13": "G1"}
