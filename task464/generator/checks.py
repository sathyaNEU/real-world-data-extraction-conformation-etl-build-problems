#!/usr/bin/env python3
"""task464 architecture 3: the assertion module, written at stage 2 beside the ladder.

Every assertion here is named after the row of `DESIGN_NOTE.md` it carries, so a reader can walk the design
note and the code side by side. `run(truth)` takes the generator's clean truth and raises on the first
failure; `verify.py` runs the same bodies against a fresh unzip of the shipped bundle at stage 3.

`truth` is a mapping the generator fills:

    sites      a list of dicts, one per 2027 contract-intent site, with keys
               site, area, modality, attested, licensed, ceiling, sessions, turns, vol_2026,
               peak_week, ceiling_readings (record, yearly, monthly, q90, q95, q99),
               time_at_ceiling_share, min_turnover_minutes, coincident_endpoints,
               sessions_hist, plateau_minutes
    areas      a list of area codes, twelve of them
    required   area -> the required weekly slots, as a real and as the rounded integer
    growth     area -> the 2027 enrolment growth factor
    rungs      rung name -> area -> weekly slots, for R0, R1, R2 and R3
    variants   the readings each SF row enumerates, already computed by the generator

The decisive step is never filed anywhere in the shipped pack: these assertions prove the readings of a
site's deliverable positions converge on the data, which is why no sentence has to say how to compute one.
"""
FLOOR = 6.0          # per cent of an area's required figure, the C4 floor
RUNGS = ("R0", "R1", "R2", "R3")
GOLDEN = "R3"


def _fail(tag, msg):
    raise AssertionError("%s: %s" % (tag, msg))


# --------------------------------------------------------------------------- the semantic fork table
def SF1(truth):
    """Every reading of a site's deliverable positions returns the same integer (the hard plateau)."""
    for s in truth["sites"]:
        r = s["ceiling_readings"]
        want = s["ceiling"]
        for name in ("record", "q90", "q95", "q99"):
            if r[name] != want:
                _fail("SF1", "%s reading %s is %r, positions are %r" % (s["site"], name, r[name], want))
        if sorted(set(r["yearly"])) != [want] or sorted(set(r["monthly"])) != [want]:
            _fail("SF1", "%s has a year or a month whose maximum is not %r" % (s["site"], want))
        if len(r["monthly"]) != 48 or len(r["yearly"]) != 4:
            _fail("SF1", "%s does not carry 48 monthly and 4 yearly maxima" % s["site"])
        if r.get("time_above_ceiling", 0) != 0:
            _fail("SF1", "%s runs more than %r treatments at one time" % (s["site"], want))
        if s["time_at_ceiling_share"] < 0.10:
            _fail("SF1", "%s holds its ceiling for only %.3f of its treating hours, so a high quantile"
                         " could return less" % (s["site"], s["time_at_ceiling_share"]))


def SF2(truth):
    """No two of a site's intervals share an endpoint, so the endpoint convention cannot move the count."""
    for s in truth["sites"]:
        if s["min_turnover_minutes"] <= 0:
            _fail("SF2", "%s has a position with no turnover between successive treatments" % s["site"])
        if s["coincident_endpoints"] != 0:
            _fail("SF2", "%s has %d coincident endpoints" % (s["site"], s["coincident_endpoints"]))


def SF3(truth):
    """Cancelled and no-show encounters build no interval under any reading."""
    v = truth["variants"]["cancelled"]
    if v["dropped"] != v["instantaneous"]:
        _fail("SF3", "the ceiling moves when cancellations are read as instantaneous")
    if v["dropped_verdicts"] != v["instantaneous_verdicts"]:
        _fail("SF3", "an area verdict moves when cancellations are read as instantaneous")


def SF4(truth):
    """A site-level clock offset cancels inside a site, including across the fall-back hour."""
    v = truth["variants"]["clock"]
    if v["as_recorded"] != v["offset_applied"] or v["spanning_fallback_intervals"] != 0:
        _fail("SF4", "the ceiling moves under a site-level offset, or an interval spans the repeated hour")


def SF5(truth):
    for s in truth["sites"]:
        if s["roster_session_rows_at_asof"] != 1:
            _fail("SF5", "%s has %d roster rows current at the as-of date"
                  % (s["site"], s["roster_session_rows_at_asof"]))


def SF6(truth):
    v = truth["variants"]["week"]
    if v["52"] != v["52.143"]:
        _fail("SF6", "an area verdict moves between 52 and 52.143 weeks")


def SF7(truth):
    for s in truth["sites"]:
        if s["days_from_latest_attestation_to_asof"] < 30 or s["rows_in_current_cycle"] != 1:
            _fail("SF7", "%s does not have exactly one attestation row at least 30 days before the as-of date"
                  % s["site"])


def SF8(truth):
    for s in truth["sites"]:
        if s["licence_corporate_stations"] != s["licence_address_stations"]:
            _fail("SF8", "%s reads a different station count on the two licence grains" % s["site"])


def SF9(truth):
    if truth["contract_intent_rows_per_site"] != 1:
        _fail("SF9", "a site carries more than one 2027 contract-intent record")
    if len(truth["sites"]) != truth["declared_population_size"]:
        _fail("SF9", "the population the contract declares is not the population the golden reads")


def SF10(truth):
    for s in truth["sites"]:
        if s["modalities_present"] != 1:
            _fail("SF10", "%s carries both modalities, so the per-modality figure is ambiguous" % s["site"])


def SF11(truth):
    v = truth["variants"]["demand_window"]
    if v["contract_year_rows"] != v["calendar_2026_rows"]:
        _fail("SF11", "the 2026 contract year and calendar 2026 select different encounters")


def SF12(truth):
    worst = min(abs(truth["rungs"][r][a] - truth["required"][a]["int"]) / truth["required"][a]["int"] * 100.0
                for r in RUNGS for a in truth["areas"])
    if worst < FLOOR:
        _fail("SF12", "an area sits %.2f per cent from its line, under the %.1f per cent floor" % (worst, FLOOR))


def SF13(truth):
    for a in truth["areas"]:
        x = truth["required"][a]["real"]
        if abs(x - round(x)) > 0.45 or abs(abs(x - int(x)) - 0.5) < 0.05:
            _fail("SF13", "%s's required figure sits within 0.05 of a half treatment" % a)


def SF14(truth):
    for s in truth["sites"]:
        if s["areas_in_window"] != 1:
            _fail("SF14", "%s sits in more than one service area inside the window" % s["site"])


def SF15(truth):
    for s in truth["sites"]:
        r = s["ceiling_readings"]
        if not (r["last12"] == r["last24"] == r["record"] == s["ceiling"]):
            _fail("SF15", "%s returns a different ceiling on a shorter look-back" % s["site"])


def SF16(truth):
    v = truth["variants"]["site_key"]
    if v["tax_id_total"] == v["site_id_total"]:
        _fail("SF16", "the tax-identifier reading files the same network total, so the row is inert")
    if v["sites_merged_by_tax_id"] < 2:
        _fail("SF16", "no site is merged by the tax-identifier reading")
    if v["site_id_one_to_one"] is not True:
        _fail("SF16", "the directory's site identifier is not one to one with a site")


def SF17(truth):
    for s in truth["sites"]:
        want = s["ceiling"] * s["sessions"] * s["turns"]
        if s["weekly_slots"] != want:
            _fail("SF17", "%s's slots are not positions times sessions times the modality figure" % s["site"])


SEMANTIC_FORKS = [SF1, SF2, SF3, SF4, SF5, SF6, SF7, SF8, SF9, SF10,
                  SF11, SF12, SF13, SF14, SF15, SF16, SF17]


# ------------------------------------------------------------------------------------- the ladder
def ladder(truth):
    tot = {r: sum(truth["rungs"][r][a] for a in truth["areas"]) for r in RUNGS}
    g = tot[GOLDEN]
    if not tot["R1"] > tot["R0"] > tot["R3"] > tot["R2"]:
        _fail("ladder", "the four totals are not strictly ordered R1 > R0 > R3 > R2: %r" % tot)
    for i, x in enumerate(RUNGS):
        for y in RUNGS[i + 1:]:
            if abs(tot[x] - tot[y]) / g * 100.0 < FLOOR:
                _fail("ladder", "%s and %s sit under %.1f per cent of the golden apart" % (x, y, FLOOR))
    short = {r: {a for a in truth["areas"] if truth["rungs"][r][a] < truth["required"][a]["int"]}
             for r in RUNGS}
    if len({frozenset(short[r]) for r in RUNGS}) != 4:
        _fail("ladder", "two rungs name the same set of short areas: %r" % short)
    gold = short[GOLDEN]
    if len(gold - short["R2"]) < 2 or len(short["R2"] - gold) < 1:
        _fail("ladder", "the volume ceiling does not name its own short set: %r against %r" % (short["R2"], gold))
    flips = {a for a in truth["areas"]
             if truth["rungs"]["R0"][a] >= truth["required"][a]["int"] > truth["rungs"]["R3"][a]}
    if len(flips) != 3:
        _fail("ladder", "the flip set is %d areas, not three" % len(flips))


def partial_applications(truth):
    """No partial application of the ceiling reproduces a golden-short area's verdict, and every cell of the
    grid sits outside the floor."""
    import itertools
    for a in truth["areas"]:
        con = [s for s in truth["sites"] if s["area"] == a and s["attested"] > s["ceiling"]]
        need = truth["required"][a]["int"]
        full = truth["rungs"]["R3"][a]
        base = truth["rungs"]["R0"][a]
        for k in range(len(con) + 1):
            for sub in itertools.combinations(range(len(con)), k):
                cap = base - sum((con[i]["attested"] - con[i]["ceiling"]) * con[i]["sessions"] * con[i]["turns"]
                                 for i in sub)
                if abs(cap - need) / need * 100.0 < FLOOR:
                    _fail("partial", "%s has a partial cell inside the floor" % a)
                if k != len(con) and a in {x for x in truth["areas"]
                                           if truth["rungs"]["R3"][x] < truth["required"][x]["int"]}:
                    if (cap >= need) == (full >= need):
                        _fail("partial", "%s reproduces its golden verdict on a partial application" % a)


def analyst_test(truth):
    """The easy route, with every field read and every rule applied, files the named wrong answer; changing
    the decisive step alone files the golden (dataset-generation section 7.1)."""
    tot = {r: sum(truth["rungs"][r][a] for a in truth["areas"]) for r in RUNGS}
    ratio = tot["R0"] / tot["R3"]
    if not 1.10 <= ratio <= 1.20:
        _fail("analyst test", "the attested reading is %.4f times the golden, outside the filed magnitude" % ratio)
    flips = [a for a in truth["areas"]
             if truth["rungs"]["R0"][a] >= truth["required"][a]["int"] > truth["rungs"]["R3"][a]]
    if len(flips) != 3:
        _fail("analyst test", "the easy route files %d areas wrongly above the standard, not three" % len(flips))


def separation_from_the_asks(truth):
    """Zero device and hazard rows inside the main call's declared population."""
    z = truth["separation"]
    for key in ("device_rows_in_main_population", "hazard_rows_in_main_population",
                "resubmission_pairs_in_main_population"):
        if z[key] != 0:
            _fail("separation", "%s is %d, not zero" % (key, z[key]))
    if z["call_figures_unchanged_without_devices"] is not True:
        _fail("separation", "deleting the ask devices moves a figure the call owes")


def hygiene_readings(truth):
    """What a solver's own capacity checks see: nothing impossible, and nothing pointing at the positions."""
    for s in truth["sites"]:
        app = (s["vol_2026"] / 52.0) / (s["attested"] * s["sessions"] * s["turns"])
        if app >= 1.0:
            _fail("hygiene", "%s's 2026 volume exceeds its attested weekly capacity" % s["site"])
        if s["peak_week"] / (s["attested"] * s["sessions"] * s["turns"]) > 1.05:
            _fail("hygiene", "%s's busiest week exceeds its attested weekly capacity by more than a twentieth"
                  % s["site"])


def oracles(truth):
    o = truth["oracles"]
    if o["state_filing_has_capacity_figure"] or o["state_filing_has_adequacy_verdict"]:
        _fail("oracles", "the 2026 state filing constructs a capacity figure or a verdict")
    if o["state_filing_station_column_ties_to_licence"] is not True:
        _fail("oracles", "the 2026 state filing's station column does not tie to the licence register")
    if o["state_filing_site_set_difference"] < 6:
        _fail("oracles", "the 2026 filing's site set is too close to the 2027 population to be out of window")
    if o["transmittal_ties_under_every_rung"] is not True:
        _fail("oracles", "the extract transmittal does not tie under every rung")
    if o["distractor_ordering_matches_golden_short_set"]:
        _fail("oracles", "a distractor ranks the areas the way the decision does (Gate G)")


def run(truth):
    for fn in SEMANTIC_FORKS:
        fn(truth)
    for fn in (ladder, partial_applications, analyst_test, separation_from_the_asks,
               hygiene_readings, oracles):
        fn(truth)
    return True


if __name__ == "__main__":
    print(__doc__.splitlines()[0])
    print("%d semantic fork assertions (SF1 to SF17) and %d structural assertions."
          % (len(SEMANTIC_FORKS), 6))
    print("Stage 3 wires run(truth) to the generator's clean truth and to verify.py on the shipped bundle.")
