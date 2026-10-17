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
    panel = defaultdict(lambda: dict(episodes=0, observed=0.0, expected=0.0, separations=0))
    sc = defaultdict(lambda: defaultdict(lambda: [0, 0]))   # (unit, q) -> stratum -> [episodes, with HAC]
    year2026 = defaultdict(lambda: dict(episodes=0, observed=0, expected=0.0))
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
                inscope_episode[row["episode_id"]] = (unit, sep, fy)
                if dt.date(2026, 1, 1) <= sep <= dt.date(2026, 12, 31):
                    site = facility[(unit, sep.replace(day=1).isoformat())]
                    y = year2026[site]
                    y["episodes"] += 1
                    y["expected"] += strata[(band, row["age_band"])]
                    y["observed"] += 1 if hac else 0
                if hac and row["hac_category_code"] and fy in ("2025-26", "2026-27"):
                    groups_by_year[fy]["principal:" + row["hac_category_code"]].add(row["episode_id"])
    return dict(units=units, bands=bands, strata=strata, plan=plan, placements=placements, peer=peer,
                sc={k: dict(v) for k, v in sc.items()},
                panel=dict(panel), year2026=dict(year2026), nonacute=stays(nonacute_rows),
                principal=dict(groups_by_year), facility=facility, summary=summary,
                inscope_episode=inscope_episode)


def stays(rows):
    """The separations the sub-acute and mental health units reported, by quarter.

    Two steps, and the second is the one the stated key cannot do. First, the feed's overlapping monthly
    load re-sends a record under a fresh episode identifier, so records are counted once on the separation
    key the dictionary states: unit, patient, admission date and diagnosis related group. Second, a stay
    whose care type changed inside it reaches the feed as two episode records, one ending and one beginning
    on the same day, and the patient left the hospital once: those episodes are chained into one stay,
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
        for r in eps:
            if chains and chains[-1][-1]["sep"] == r["adm"]:
                chains[-1].append(r)      # the care type changed inside the stay
            else:
                chains.append([r])
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


def unit_tally(b, code, qs):
    """A unit's observed, published-expected, episodes, separations and stratum counts over `qs`."""
    o = e = 0.0
    n = sp = 0
    strat = defaultdict(int)
    for q in qs:
        p = b["panel"].get((code, q))
        if p is None:
            continue
        o += p["observed"]
        e += p["expected"]
        n += p["episodes"]
        sp += p["separations"]
        for st, (cnt, _) in b["sc"].get((code, q), {}).items():
            strat[st] += cnt
    return o, e, n, sp, strat


def avoidable(b, code, qs, rates, denom="separations"):
    """Charter 4.3 carried onto the planned separations under specification 3.4.

    The complications the unit's own patients had, less the complications patients of the same risk band
    and age band ordinarily have, counted patient by patient and summed, then carried onto the quarter's
    planned separations at the unit's own rate per separation.
    """
    o, e, n, sp, strat = unit_tally(b, code, qs)
    if not sp:
        return 0.0
    expected_net = sum(cnt * rates[st] for st, cnt in strat.items())
    d = sp if denom == "separations" else n
    return (o - expected_net) * b["plan"][code] / d


def all_quarters(b):
    return sorted({q for (_, q) in b["panel"]})


def standings(b):
    """Every eligible unit on charter 4.3, and on the published basis beside it."""
    elig = eligible_units(b)
    rates, _ = net_rates(b)
    out = []
    for code in elig:
        qs = quarters(b["panel"], code)
        o, e, n, sp, strat = unit_tally(b, code, qs)
        expected_net = sum(cnt * rates[st] for st, cnt in strat.items())
        plan = b["plan"][code]
        k = plan / sp
        last = qs[-1]
        lp = b["panel"][(code, last)]
        out.append(dict(
            unit=code, name=b["units"][code]["unit_name"], hospital=b["units"][code]["hospital_code"],
            quarters=len(qs), observed=o, expected=e, expected_net=expected_net,
            episodes=n, separations=sp, plan=plan,
            avoidable=(o - expected_net) * k,
            published_excess=(o - e) * k,
            per_1000=(o - expected_net) / sp * 1000.0,
            expected_plan=e / sp * plan,
            ratio=o / e, ratio_net=o / expected_net,
            adjusted_rate=o / e * REF_RATE,
            se=math.sqrt(o) * k,
            last_ratio=lp["observed"] / lp["expected"],
            last_excess=(lp["observed"] - lp["expected"]) * lp["separations"] and
                        (lp["observed"] - lp["expected"]) * plan / lp["separations"]))
    out.sort(key=lambda d: -d["avoidable"])
    return out, rates


def convergence(b):
    """Every reading of charter 4.3 the text leaves open, computed on the record.

    The clause names whose patients, which strata, what is compared with what and over which window; it
    does not name the frequency's own window, whether the unit's own patients sit inside the comparison,
    or the denominator the rate is carried on. Each reading is formed and ranked here so a parameter change
    that breaks the convergence fails the build instead of passing quietly (C1, `determinism-check` 3).
    """
    allq = all_quarters(b)
    n = len(allq)
    windows = OrderedDict([
        ("the ten closed quarters of the specification period", set(allq)),
        ("the eight most recent closed quarters", set(allq[n - 8:])),
        ("the four most recent closed quarters", set(allq[n - 4:])),
        ("the latest closed quarter alone", {allq[-1]}),
    ])
    elig = eligible_units(b)
    readings = OrderedDict()

    def add(label, fn):
        v = {c: fn(c) for c in elig}
        order = sorted(v, key=lambda c: -v[c])
        first, second = order[0], order[1]
        readings[label] = dict(first=first, first_value=v[first], second=second,
                               second_value=v[second], margin=v[first] / v[second] if v[second] > 0 else None)

    for lab, qs in windows.items():
        rates = net_rates(b, qs=qs)[0]
        add("the comparison frequency measured over %s" % lab,
            lambda c, r=rates: avoidable(b, c, set(allq), r))
    for lab, qs in list(windows.items())[:1] + list(windows.items())[2:3]:
        add("the unit's own patients left out of the comparison, frequency over %s" % lab,
            lambda c, qs=qs: avoidable(b, c, set(allq), net_rates(b, qs=qs, exclude_unit=c)[0]))
    rates = net_rates(b)[0]
    for lab, denom in (("all separations in the record", "separations"),
                       ("in-scope episodes in the record", "episodes")):
        add("the unit's rate taken per %s" % lab,
            lambda c, d=denom: avoidable(b, c, set(allq), rates, denom=d))
    for lab, qs in windows.items():
        add("the unit's own record taken over %s" % lab,
            lambda c, qs=qs: avoidable(b, c, qs, rates))
    return readings


def routes(b):
    """The competing route definitions a careful analyst would try, each ranked on the record.

    Nine name a unit other than the answer and are the ladder's rungs and its measured near misses; four
    name the answer, so the call is robust to them. Every figure is a sum over the record: no functional
    form is chosen anywhere and there is no free parameter to estimate.
    """
    allq = all_quarters(b)
    rates = net_rates(b)[0]
    elig = eligible_units(b)
    last = {allq[-1]}
    four = set(allq[len(allq) - 4:])
    out = OrderedDict()

    def add(label, fn):
        v = {}
        for c in elig:
            o, e, n, sp, strat = unit_tally(b, c, set(allq))
            v[c] = fn(c, o, e, n, sp, strat)
        order = sorted(v, key=lambda c: -v[c])
        out[label] = dict(first=order[0], first_value=v[order[0]], second=order[1],
                          second_value=v[order[1]],
                          margin=v[order[0]] / v[order[1]] if v[order[1]] > 0 else None,
                          rank_of=lambda code, order=order: order.index(code) + 1,
                          order=order)

    add("R0 the published excess, carried onto the planned separations",
        lambda c, o, e, n, sp, st: (o - e) * b["plan"][c] / sp)
    add("R1 the published excess over the window, not carried",
        lambda c, o, e, n, sp, st: o - e)
    add("R2 the published standardised ratio",
        lambda c, o, e, n, sp, st: o / e)
    add("R3 the published adjusted rate, the ratio times the reference rate",
        lambda c, o, e, n, sp, st: o / e * REF_RATE)
    add("R4 the raw complication count over the window",
        lambda c, o, e, n, sp, st: o)
    add("R5 the crude complication rate per 1,000 in-scope episodes",
        lambda c, o, e, n, sp, st: 1000.0 * o / n)
    add("R6 the published excess on the latest closed quarter alone, carried",
        lambda c, o, e, n, sp, st: _window_excess(b, c, last, None))
    add("R7 the avoidable count on the latest closed quarter alone, carried",
        lambda c, o, e, n, sp, st: avoidable(b, c, last, rates))
    add("R8 the avoidable count over the window, not carried",
        lambda c, o, e, n, sp, st: o - sum(k * rates[s] for s, k in st.items()))
    add("R9 the standardised ratio against the comparison frequency",
        lambda c, o, e, n, sp, st: o / sum(k * rates[s] for s, k in st.items()))
    add("R10 the avoidable count as a rate per 1,000 separations, not as a count",
        lambda c, o, e, n, sp, st: 1000.0 * (o - sum(k * rates[s] for s, k in st.items())) / sp)
    add("R11 the avoidable count over the last four closed quarters, carried",
        lambda c, o, e, n, sp, st: avoidable(b, c, four, rates))
    add("R12 the avoidable count over the window, carried onto the planned separations",
        lambda c, o, e, n, sp, st: avoidable(b, c, set(allq), rates))
    return out


def _window_excess(b, code, qs, _):
    o, e, n, sp, strat = unit_tally(b, code, qs)
    return (o - e) * b["plan"][code] / sp if sp else 0.0


def ruled_out(b):
    """The readings that do move the call, each with the sentence that rules it out.

    Charter 4.3 stratifies on a risk band and an age band and names no site, division or peer condition,
    and it names the strata at all, so a restricted comparison population and an unstratified comparison
    are both out on the clause's own words. They are measured here rather than argued: a reading ruled out
    by a sentence still has to be shown to be the reading the sentence excludes.
    """
    allq = set(all_quarters(b))
    elig = eligible_units(b)
    out = OrderedDict()

    def add(label, fn, sentence):
        v = {c: fn(c) for c in elig}
        order = sorted(v, key=lambda c: -v[c])
        out[label] = dict(first=order[0], first_value=v[order[0]], second=order[1],
                          second_value=v[order[1]],
                          margin=v[order[0]] / v[order[1]] if v[order[1]] > 0 else None,
                          sentence=sentence)

    clause = ("charter 4.3, 'the complications that patients of the same risk band and age band "
              "ordinarily have': it stratifies on a risk band and an age band and names no other condition")
    add("the comparison restricted to the unit's own hospital",
        lambda c: avoidable(b, c, allq,
                            net_rates(b, hospital=b["units"][c]["hospital_code"])[0]), clause)
    add("the comparison restricted to the hospital's peer group",
        lambda c: avoidable(b, c, allq,
                            net_rates(b, peer=b["peer"][b["units"][c]["hospital_code"]])[0]), clause)
    tot_o = sum(cell[1] for counts in b["sc"].values() for cell in counts.values())
    tot_n = sum(cell[0] for counts in b["sc"].values() for cell in counts.values())
    crude = tot_o / tot_n

    def unstratified(c):
        o, e, n, sp, strat = unit_tally(b, c, allq)
        return (o - n * crude) * b["plan"][c] / sp

    add("one crude network rate with no strata at all", unstratified, clause)
    return out


def forcing_facts(b):
    """The three facts that force the comparison frequency, measured from the bundle.

    One: the published table is a fixed vintage. Appendix A states it was derived from network activity in
    the year ended 30 June 2024 and specification 3.1 says the rates are not re-estimated between
    specifications. Two: the network's own frequency has since moved by different amounts in different risk
    bands, and in both directions. Three: the candidates' case mixes differ several-fold, so the direction
    and the size of the error differ unit by unit.
    """
    rates, den = net_rates(b)
    byband = defaultdict(lambda: [0.0, 0.0])
    for (unit, q), counts in b["sc"].items():
        for (band, age), (n, o) in counts.items():
            byband[band][0] += o
            byband[band][1] += n * b["strata"][(band, age)]
    drift = {band: o / e for band, (o, e) in byband.items() if e}
    elig = eligible_units(b)
    share = {}
    for c in elig:
        o, e, n, sp, strat = unit_tally(b, c, set(all_quarters(b)))
        surg = sum(cnt for (band, _), cnt in strat.items() if band.startswith("SURG"))
        share[c] = surg / n if n else 0.0
    nz = [v for v in share.values() if v > 0.01]
    return dict(drift=drift,
                drift_low=min(drift.values()), drift_high=max(drift.values()),
                drift_spread=max(drift.values()) / min(drift.values()),
                surgical_share=share, surgical_low=min(nz), surgical_high=max(share.values()),
                surgical_none=sum(1 for v in share.values() if v <= 0.01))


def mix_shift_demo(b):
    """The unit whose patients moved while its own practice did not, quarter by quarter, on both bases.

    This is the measurement that forces the comparison frequency. One unit treated the same number of
    patients in every closed quarter and changed nothing it does; for two of them its case mix moved. On
    the published basis its avoidable count moves by a multiple; on the record's own frequency it does not
    move at all. A count that moves when only the patients change is not a count of complications a unit
    carries as avoidable.
    """
    rates, _ = net_rates(b)
    allq = all_quarters(b)
    best = None
    for code in sorted({u for (u, _) in b["panel"]}):
        qs = quarters(b["panel"], code)
        if len(qs) < len(allq):
            continue
        rows = []
        for q in qs:
            p = b["panel"][(code, q)]
            strat = b["sc"].get((code, q), {})
            en = sum(cnt * rates[st] for st, (cnt, _) in strat.items())
            surg = sum(cnt for (band, _), (cnt, _) in strat.items() if band.startswith("SURG"))
            rows.append(dict(quarter=q, episodes=p["episodes"], observed=p["observed"],
                             expected=p["expected"], expected_net=en,
                             published=p["observed"] - p["expected"],
                             internal=p["observed"] - en,
                             ratio=p["observed"] / p["expected"],
                             surgical_share=surg / p["episodes"] if p["episodes"] else 0.0))
        sh = [r["surgical_share"] for r in rows]
        swing = max(sh) - min(sh)
        pub = [r["published"] for r in rows]
        net = [r["internal"] for r in rows]
        pub_swing = (max(pub) / min(pub)) if min(pub) > 0 else 0.0
        net_swing = max(net) - min(net)
        score = (swing > 0.25, pub_swing, -net_swing)
        if swing > 0.25 and (best is None or score > best[0]):
            best = (score, dict(unit=code, name=b["units"][code]["unit_name"], rows=rows,
                                mix_swing=swing, published_multiple=pub_swing,
                                internal_spread=net_swing,
                                shifted=[r["quarter"] for r in rows if r["surgical_share"] > 0.25],
                                published_low=min(pub), published_high=max(pub),
                                internal_low=min(net), internal_high=max(net)))
    assert best is not None, "no unit in the record carries a case-mix shift to demonstrate on"
    return best[1]


def compute(target):
    b = load(target)
    units, rates = standings(b)
    answer, runner = units[0], units[1]
    third = units[2]
    conv = convergence(b)
    rts = routes(b)
    rout = ruled_out(b)
    facts = forcing_facts(b)
    demo = mix_shift_demo(b)
    elig = eligible_units(b)

    # the three rungs the ladder claims, each named on the record rather than chosen
    by = {d["unit"]: d for d in units}
    rung0 = by[rts["R0 the published excess, carried onto the planned separations"]["first"]]
    rung3 = by[rts["R10 the avoidable count as a rate per 1,000 separations, not as a count"]["first"]]
    rung4 = answer
    se_gap = math.sqrt(answer["se"] ** 2 + runner["se"] ** 2)
    se_gap3 = math.sqrt(answer["se"] ** 2 + third["se"] ** 2)

    # ask 2: the hospital year ended 31 December 2026
    sites = {r["hospital_code"]: r["hospital_name"] for r in _read(target, "hospital_sites.csv")}
    hosp = []
    for code in sorted(b["year2026"]):
        y = b["year2026"][code]
        hosp.append(dict(hospital=code, name=sites[code], episodes=y["episodes"],
                         complications=y["observed"],
                         rate=y["observed"] / y["expected"] * REF_RATE))

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
    groups = []
    for gid in sorted(group_names):
        groups.append(dict(group=gid, name=group_names[gid],
                           fy2025=len(found["2025-26"][gid]), fy2026=len(found["2026-27"][gid])))

    return dict(units=units, answer=answer, runner=runner, third=third, eligible=elig,
                net_rates=rates, convergence=conv, routes=rts, ruled_out=rout,
                facts=facts, demo=demo,
                rung0=rung0, rung3=rung3, rung4=rung4,
                hospitals=hosp, outside=outside, groups=groups,
                gap=answer["avoidable"] - runner["avoidable"],
                margin=answer["avoidable"] / runner["avoidable"],
                se_gap=se_gap, se_lead=(answer["avoidable"] - runner["avoidable"]) / se_gap,
                se_lead_third=(answer["avoidable"] - third["avoidable"]) / se_gap3,
                published_rank=[d["unit"] for d in sorted(units, key=lambda x: -x["published_excess"])]
                .index(answer["unit"]) + 1,
                bundle=b)


# Appendix B of the specification: the 2022 revision's codes and the groups they belong to. The 2026
# revision renumbered HAC03 to HAC06 and folded HAC13 into HAC03, so a code is read against the revision in
# force at separation.
LIST_2022_GROUPS = {"HAC01": "G1", "HAC02": "G1", "HAC03": "G2", "HAC04": "G3", "HAC05": "G4",
                    "HAC06": "G4", "HAC07": "G5", "HAC08": "G6", "HAC09": "G6", "HAC10": "G7",
                    "HAC11": "G8", "HAC12": "G8", "HAC13": "G1"}
