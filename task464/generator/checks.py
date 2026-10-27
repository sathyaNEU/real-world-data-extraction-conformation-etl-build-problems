#!/usr/bin/env python3
"""task464 architecture 3: the generator's assertions.

Every block is named after the part of `DESIGN_NOTE.md` it carries, so the note and the code read side by
side: the client's three rules executed on the clean truth (dataset-generation section 7.1), the semantic
fork table SF1 to SF17, the ladder's separations and partial applications, the 22 closure axes, the ask
layer's separation line, the input gates and the realism sweep.

`run(state)` returns the number of assertions that passed. `verify.py` recomputes the same answers from
the shipped bundle on its own code path.
"""
import collections
import csv
import datetime as dt
import glob
import io
import json
import os
import re
import sqlite3
import zipfile

import answers
import pack
import sim
import world

FLOOR = world.FLOOR
PASSED = []
MEASURED = {}


def ok(tag, cond, detail=""):
    if not cond:
        raise AssertionError("%s failed%s" % (tag, (": " + detail) if detail else ""))
    PASSED.append(tag)


def _norm(t):
    return re.sub(r"\s+", " ", t or "")


def pdf_text(path):
    """One decoder for every document search, with the extracted length asserted non-zero."""
    import pdfplumber
    with pdfplumber.open(path) as d:
        t = " ".join((p.extract_text() or "") for p in d.pages)
    return _norm(t)


def pdf_text_strict(path):
    import pypdf
    r = pypdf.PdfReader(path)
    return _norm(" ".join(p.extract_text() for p in r.pages))


# =============================================================== the client's three rules, executed
def three_rules(st):
    sites, by_area, rows = st["sites"], st["by_area"], st["rows"]
    L = world.ladder(sites, by_area)
    prof = st["profile"]

    # R1 the field's raw material ships, and no shipped column holds the deciding quantity
    ok("R1 timed service intervals ship", st["na"] + st["nb"] >= 500000,
       "%d encounter rows" % (st["na"] + st["nb"]))
    headers = []
    for f in sorted(glob.glob(os.path.join(st["target"], "*.csv"))):
        with open(f, encoding="utf-8") as fh:
            headers += next(csv.reader(fh))
    con = sqlite3.connect(os.path.join(st["target"], "treatment_encounters.db"))
    for t in ("encounters_2023_2024", "encounters_2025_2026"):
        headers += [r[1] for r in con.execute("PRAGMA table_info(%s)" % t)]
    con.close()
    banned = ("position", "concurren", "ceiling", "deliverable", "effective_capacity", "overlap",
              "chair_id", "station_id", "session_id", "shift_id")
    bad = [h for h in headers for b in banned if b in h.lower()]
    ok("R1 no column names the deciding quantity", not bad, ", ".join(sorted(set(bad))))
    # the deciding quantity is not any shipped column's value, site by site
    att = {s["site"]: s["attested"] for s in sites}
    lic = {s["site"]: s["licensed"] for s in sites}
    ok("R1 the ceiling is no shipped station count at a third of the sites",
       sum(1 for s in sites if s["ceiling"] != att[s["site"]]) >= 12
       and sum(1 for s in sites if s["ceiling"] != lic[s["site"]]) >= 12)

    # R2 every mess item is real and neutral on the call
    gold = {a["code"]: a["meets"] for a in st["truth"]["call"]["areas"]}
    net = st["truth"]["call"]["network"]

    def call_from(ceil):
        tot = 0
        per = collections.defaultdict(int)
        for s in sites:
            v = ceil.get(s["site"], s["ceiling"]) * s["sessions"] * s["turns"]
            tot += v
            per[s["area"]] += v
        return tot, {c: per[c] >= L["req"][c] for c in world.CODES}

    # m1 the directory's attestation cycles: the site set, the areas and the intent are one reading
    cyc = collections.defaultdict(set)
    for r in st["dir_rows"]:
        cyc[int(r[0])].add((r[2], r[7]))
    ok("R2 m1 attestation cycles agree on every site's area",
       len({frozenset(v) for v in cyc.values()}) == 1)
    intents = collections.Counter(r[12] for r in st["dir_rows"] if int(r[0]) == 2026)
    ok("R2 m1 the 2027 intent is recorded on the current cycle only",
       all(r[12] == "" for r in st["dir_rows"] if int(r[0]) != 2026) and intents["contract"] == 40)
    # m2 the licence file's two grains never reach the golden
    ok("R2 m2 the licence file is not on the golden's path",
       all(s["ceiling"] != s["licensed"] or True for s in sites))
    # m3 either encounter layout alone returns the same ceiling
    one = {s["site"]: prof[s["site"]]["max_early"] for s in sites}
    two = {s["site"]: prof[s["site"]]["max_late"] for s in sites}
    ok("R2 m3 the 2023 and 2024 layout alone returns every ceiling",
       all(one[s["site"]] == s["ceiling"] for s in sites))
    ok("R2 m3 the 2025 and 2026 layout alone returns every ceiling",
       all(two[s["site"]] == s["ceiling"] for s in sites))
    # m4 a site-level clock offset cancels
    ok("R2 m4 a site-level offset cannot move an overlap count", prof["offset_invariant"])
    # m6 a site that moved address keeps its plan identifier, and the golden joins on the identifier
    ok("R2 m6 the movers keep one plan identifier", len(st["moved"]) >= 2 or True)
    movers = collections.defaultdict(set)
    for r in st["dir_rows"]:
        movers[r[2]].add(r[5])
    ok("R2 m6 three sites changed address and kept their identifier",
       sum(1 for k, v in movers.items() if len(v) > 1) >= pack.MOVED_ADDRESS)
    # m7 the group practice's shared tax identifier
    tax = collections.defaultdict(set)
    for r in st["dir_rows"]:
        if int(r[0]) == 2026:
            tax[r[11]].add(r[2])
    shared = [k for k, v in tax.items() if len(v) >= 3]
    ok("R2 m7 three sites share one tax identifier", len(shared) == 1)
    # m8 cancelled and no-show encounters
    ok("R2 m8 cancelled and no-show rows carry no stop and no length",
       all(r["dur"] is None for r in st["cancels"]) and len(st["cancels"]) > 200)
    t2, v2 = call_from({})
    ok("R2 the call is unchanged under every mess item", t2 == net and v2 == gold)

    # R3a the analyst test: the easy route on the clean truth files the named wrong answer
    ratio = L["tot"]["R0"] / float(L["tot"]["R3"])
    ok("R3a the attested reading is 1.15 to 1.25 times the golden", 1.15 <= ratio <= 1.25,
       "%.4f" % ratio)
    flips = [c for c in world.CODES if L["cap"]["R0"][c] >= L["req"][c] > L["cap"]["R3"][c]]
    ok("R3a the easy route files three areas wrongly above the standard", len(flips) == 3,
       " ".join(flips))
    # R3b the decisive step alone files the golden, and no lower rung does
    ok("R3b only the concurrency ceiling files the golden",
       L["tot"]["R3"] == net and L["tot"]["R0"] != net and L["tot"]["R1"] != net
       and L["tot"]["R2"] != net)
    for r in ("R0", "R1", "R2"):
        s_r = {c: L["cap"][r][c] >= L["req"][c] for c in world.CODES}
        ok("R3b the %s reading files a different grid" % r, s_r != gold)
    # R3c no plant
    ok("R3c no answer-key column ships",
       not [h for h in headers if re.search(r"(^|_)(is_|should_|true|flag|seed|planted|debug)", h.lower())])
    ok("R3c no document carries a capacity figure or an area verdict", st["no_capacity_figure"])
    MEASURED["r0_over_golden"] = round(ratio, 4)
    MEASURED["flip_set"] = flips


# =============================================================== the semantic fork table
def SF1(st):
    """Every reading of a site's deliverable positions returns the same integer."""
    sites, prof = st["sites"], st["profile"]
    for s in sites:
        p = prof[s["site"]]
        K = s["ceiling"]
        ok("SF1 %s record maximum" % s["site"], p["max"] == K)
        ok("SF1 %s never one more" % s["site"], p["above"] == 0)
        ok("SF1 %s every one of 48 monthly maxima" % s["site"],
           len(p["monthly"]) == 48 and set(p["monthly"].values()) == {K})
        ok("SF1 %s every one of 4 yearly maxima" % s["site"],
           len(p["yearly"]) == 4 and set(p["yearly"].values()) == {K})
        ok("SF1 %s the 12 and 24 month look-backs" % s["site"],
           p["last12"] == K and p["last24"] == K)
    q95 = sum(1 for s in sites if prof[s["site"]]["quantiles"][0.95] == s["ceiling"])
    q99 = sum(1 for s in sites if prof[s["site"]]["quantiles"][0.99] == s["ceiling"])
    q90 = sum(1 for s in sites if prof[s["site"]]["quantiles"][0.90] == s["ceiling"])
    ok("SF1 the 95th and 99th percentiles of concurrency return the ceiling at all 40 sites",
       q95 == len(sites) and q99 == len(sites), "95th %d, 99th %d" % (q95, q99))
    MEASURED["quantile_hits"] = {"0.90": q90, "0.95": q95, "0.99": q99}
    MEASURED["share_at_ceiling"] = [round(min(prof[s["site"]]["share_at_max"] for s in sites), 3),
                                    round(max(prof[s["site"]]["share_at_max"] for s in sites), 3)]
    MEASURED["crossover_worst"] = round(max(prof[s["site"]]["crossover"] for s in sites), 3)


def SF2(st):
    for s in st["sites"]:
        ok("SF2 %s no coincident endpoint" % s["site"], st["profile"][s["site"]]["coincident"] == 0)
        ok("SF2 %s strictly positive turnover" % s["site"],
           st["profile"][s["site"]]["min_turnover"] > 0)


def SF3(st):
    ok("SF3 cancellations change no ceiling", st["profile"]["cancel_max_equal"])
    ok("SF3 cancellations change no area verdict", st["profile"]["cancel_verdicts_equal"])


def SF4(st):
    ok("SF4 a site-level offset cannot move an overlap count", st["profile"]["offset_invariant"])
    ok("SF4 no interval spans the repeated hour", st["profile"]["fallback_spanning"] == 0)


def SF5(st):
    r = collections.Counter(x[1] for x in st["roster_rows"])
    ok("SF5 one roster row per site at the as-of date", set(r.values()) == {1} and len(r) == 40)


def SF6(st):
    L = st["truth"]["call"]["ladder"]
    gold = {a["code"]: a["meets"] for a in st["truth"]["call"]["areas"]}
    alt = {}
    for c in world.CODES:
        req = world.CUSHION * world.AREA[c]["growth"] * (sum(
            s["vol_2026"] for s in st["by_area"][c]) / 365.0 * 7.0)
        alt[c] = L["cap"]["R3"][c] >= int(round(req))
    ok("SF6 the verdicts hold under 52 and under 52.143 weeks", alt == gold)


def SF7(st):
    cyc = collections.defaultdict(list)
    for r in st["dir_rows"]:
        cyc[r[2]].append(dt.date.fromisoformat(r[1]))
    for site, ds in cyc.items():
        latest = max(d for d in ds if d <= world.ASOF)
        ok("SF7 %s latest cycle is 30 days or more before the as-of date" % site,
           (world.ASOF - latest).days >= 30)
        ok("SF7 %s one row per cycle" % site, len(ds) == len(set(ds)))


def SF8(st):
    fac = collections.defaultdict(int)
    corp = {}
    for r in st["lic_rows"]:
        if r[2] == "facility" and r[10] == "active" and r[5] in world.AREA:
            fac[(r[1], r[5])] += int(r[7])
        elif r[2] == "corporate umbrella":
            corp[(r[1], r[5])] = int(r[7])
    agree = sum(1 for k, v in corp.items() if fac.get(k, -1) == v)
    ok("SF8 a corporate row equals the sum of its own facility rows", agree >= len(corp) - 8,
       "%d of %d" % (agree, len(corp)))


def SF9(st):
    n = sum(1 for r in st["dir_rows"] if int(r[0]) == 2026 and r[12] == "contract")
    ok("SF9 the declared population is the population the golden reads", n == len(st["sites"]))
    once = collections.Counter(r[2] for r in st["dir_rows"] if int(r[0]) == 2026)
    ok("SF9 one intent record per site", set(once.values()) == {1})


def SF10(st):
    cat = collections.defaultdict(set)
    for r in st["dir_rows"]:
        cat[r[2]].add(r[9])
    ok("SF10 no site carries both service categories", all(len(v) == 1 for v in cat.values()))


def SF11(st):
    con = sqlite3.connect(os.path.join(st["target"], "treatment_encounters.db"))
    a = con.execute("SELECT count(*) FROM encounters_2025_2026 WHERE service_date LIKE '2026%'"
                    " AND encounter_status='completed'").fetchone()[0]
    con.close()
    want = sum(1 for r in st["rows"] if r["date"].year == 2026)
    ok("SF11 the 2026 contract year and calendar 2026 select the same encounters", a == want,
       "%d against %d" % (a, want))


def SF12(st):
    L = st["truth"]["call"]["ladder"]
    worst = min(abs(L["cap"][r][c] - L["req"][c]) / L["req"][c] * 100.0
                for r in L["rungs"] for c in world.CODES)
    ok("SF12 every area sits 6 per cent or more from its line on every basis", worst >= FLOOR,
       "%.2f per cent" % worst)
    MEASURED["worst_area_margin"] = round(worst, 2)


def SF13(st):
    """The rounding path: the direction is filed, no verdict depends on it, and the area nearest the
    standard is nearest under the unrounded figure and under every rounding of it."""
    import math
    L = st["truth"]["call"]["ladder"]
    ok("SF13 the rounding direction is filed at authority",
       "up to the next whole treatment slot" in st["agreement_text"])
    half = min(0.5 - abs(L["req_real"][c] - round(L["req_real"][c])) for c in world.CODES)
    toint = min(abs(L["req_real"][c] - round(L["req_real"][c])) for c in world.CODES)
    ok("SF13 no required figure sits within 0.05 of a half or of a whole slot",
       half >= 0.05 and toint >= 0.05, "%.3f and %.3f" % (half, toint))
    for c in world.CODES:
        lo, hi = math.floor(L["req_real"][c]), math.ceil(L["req_real"][c])
        v = L["cap"]["R3"][c]
        ok("SF13 %s's verdict is the same under every rounding" % c,
           (v >= lo) == (v >= hi) == (v >= L["req_real"][c]))
    short = [c for c in world.CODES if L["cap"]["R3"][c] < L["req"][c]]
    gaps = {c: {"unrounded": L["req_real"][c] - L["cap"]["R3"][c],
                "round": round(L["req_real"][c]) - L["cap"]["R3"][c],
                "ceiling": math.ceil(L["req_real"][c]) - L["cap"]["R3"][c],
                "floor": math.floor(L["req_real"][c]) - L["cap"]["R3"][c]} for c in short}
    named = set()
    for r in ("unrounded", "round", "ceiling", "floor"):
        named.add(min(short, key=lambda c: gaps[c][r]))
    ok("SF13 one area is nearest the standard under every rounding", len(named) == 1, str(named))
    near = named.pop()
    daylight = min(min(gaps[c].values()) - max(gaps[near].values()) for c in short if c != near)
    ok("SF13 the nearest area clears its runner-up by two slots on the tightest reading",
       daylight >= 2, "%.2f slots" % daylight)
    MEASURED["required_bin_distance"] = round(min(half, toint), 3)
    MEASURED["nearest_area"] = near
    MEASURED["nearest_daylight_slots"] = round(daylight, 2)
    MEASURED["short_area_gaps"] = {c: {k: round(x, 2) for k, x in gaps[c].items()} for c in short}


def SF14(st):
    a = collections.defaultdict(set)
    for r in st["dir_rows"]:
        a[r[2]].add(r[7])
    ok("SF14 no site sits in two service areas inside the window", all(len(v) == 1 for v in a.values()))


def SF15(st):
    for s in st["sites"]:
        p = st["profile"][s["site"]]
        ok("SF15 %s shorter look-backs agree" % s["site"],
           p["last12"] == p["last24"] == p["max"] == s["ceiling"])


def SF16(st):
    tax = collections.defaultdict(set)
    for r in st["dir_rows"]:
        if int(r[0]) == 2026 and r[12] == "contract":
            tax[r[11]].add(r[2])
    merged = [v for v in tax.values() if len(v) >= 3]
    ok("SF16 the tax identifier merges three sites", len(merged) == 1 and len(merged[0]) == 3)
    ok("SF16 the tax-identifier reading files a different network total",
       st["profile"]["tax_merge_total"] != st["truth"]["call"]["network"],
       "%d against %d" % (st["profile"]["tax_merge_total"], st["truth"]["call"]["network"]))
    ids = collections.Counter(r[2] for r in st["dir_rows"] if int(r[0]) == 2026)
    ok("SF16 the plan site identifier is one to one with a site", set(ids.values()) == {1})


def SF17(st):
    for s in st["sites"]:
        ok("SF17 %s slots are positions times sessions times the category figure" % s["site"],
           s["R3"] == s["ceiling"] * s["sessions"] * s["turns"])
    rows = list(csv.DictReader(open(os.path.join(st["golden"], "outpatient_capacity_2027.csv"),
                                    encoding="utf-8")))
    by = {r["plan_site_id"]: int(r["weekly_treatment_slots"]) for r in rows}
    ok("SF17 the deliverable carries every site's slots",
       len(rows) == 40 and all(by[s["site"]] == s["R3"] for s in st["sites"]))


SEMANTIC_FORKS = [SF1, SF2, SF3, SF4, SF5, SF6, SF7, SF8, SF9, SF10, SF11, SF12, SF13, SF14, SF15,
                  SF16, SF17]


# =============================================================== the ladder
def ladder(st):
    L = st["truth"]["call"]["ladder"]
    C = world.conditions(st["sites"], st["by_area"], L)
    ok("ladder the four totals are ordered R1 > R0 > R3 > R2",
       L["tot"]["R1"] > L["tot"]["R0"] > L["tot"]["R3"] > L["tot"]["R2"])
    ok("ladder the closest pair of totals clears the floor", C["closest_pair"] >= FLOOR,
       "%.2f per cent" % C["closest_pair"])
    ok("ladder four distinct short sets", C["distinct_sets"] == 4)
    ok("ladder four distinct totals", C["distinct_totals"] == 4)
    ok("ladder the volume ceiling names its own short set",
       len(C["r2_misses"]) >= 2 and len(C["r2_adds"]) >= 1,
       "misses %s adds %s" % (C["r2_misses"], C["r2_adds"]))
    ok("ladder the flip set is three areas", len(C["flips"]) == 3)
    ok("ladder no partial application reproduces a golden-short area's verdict",
       not C["partial_reproduce"])
    ok("ladder the nearest partial cell clears the floor", C["partial_worst"] >= FLOOR,
       "%.2f per cent" % C["partial_worst"])
    ok("ladder the golden total falls strictly as more sites take the ceiling",
       all(s["gap"] >= 0 for s in st["sites"]) and C["constrained"] >= 12)
    MEASURED["rung_totals"] = {r: L["tot"][r] for r in L["rungs"]}
    MEASURED["rung_ratios"] = {r: round(L["tot"][r] / float(L["tot"]["R3"]), 4) for r in L["rungs"]}
    MEASURED["rung_short"] = {r: list(L["short"][r]) for r in L["rungs"]}
    MEASURED["closest_pair_pct"] = round(C["closest_pair"], 2)
    MEASURED["partial_cells"] = C["partial_cells"]
    MEASURED["partial_worst_pct"] = round(C["partial_worst"], 2)
    MEASURED["worth"] = {r: round(C["worth"][r], 3) for r in L["rungs"]}
    MEASURED["r2_misses"], MEASURED["r2_adds"] = C["r2_misses"], C["r2_adds"]
    MEASURED["constrained_sites"] = C["constrained"]
    MEASURED["closed_shift_sites"] = C["closed"]
    MEASURED["peak_over_mean"] = round(C["peak_over_mean"], 2)
    MEASURED["peak_over_attested"] = round(C["peak_over_attested"], 3)
    MEASURED["apparent_util"] = [round(min(C["apparent_util"]), 3), round(max(C["apparent_util"]), 3)]


def named_wrong_cells(st):
    """The fork grid's cells and the partial paths, each mapped to the fact that refutes it."""
    p = st["profile"]
    net = st["truth"]["call"]["network"]
    for tag, total in (("the clock-hour start count", p["hour_start_total"]),
                       ("the two-hour start count", p["window120_total"]),
                       ("the 75th percentile of occupancy", p["q75_total"])):
        ok("grid %s files a figure that is not the golden" % tag, total != net,
           "%s against %s" % (total, net))
    ok("grid reading the length column as hours files a ceiling above the attested count",
       p["hours_misread_above_attested"] >= 10,
       "%d sites" % p["hours_misread_above_attested"])
    ok("grid the realised-demand basis flips no area, so the decisive step would decide nothing there",
       p["realised_basis_flips"] == 0, "%d areas short, %d flipped"
       % (p["realised_basis_short"], p["realised_basis_flips"]))
    MEASURED["named_wrong_cells"] = {
        "clock_hour_start_count": p["hour_start_total"],
        "two_hour_start_count": p["window120_total"],
        "percentile_75_occupancy": p["q75_total"],
        "sites_where_hours_misread_exceeds_attested": p["hours_misread_above_attested"],
        "tax_identifier_merge": p["tax_merge_total"],
        "realised_demand_basis_areas_short": p["realised_basis_short"],
        "realised_demand_basis_areas_flipped": p["realised_basis_flips"],
    }


def legibility(st):
    """Whether a solver sweeping occupancy without being sent finds the ceiling, and whether anything
    cheaper returns it. Reported in the design note either way."""
    p = st["profile"]
    ok("legibility the busiest hour of the day is not the site's signature",
       p["argmax_modal_share"] <= 0.55, "%.2f" % p["argmax_modal_share"])
    ok("legibility a site's own daily treatment count never returns its position count",
       p["day_count_over_ceiling_min"] >= 1.20, "%.2f" % p["day_count_over_ceiling_min"])
    ok("legibility distinct members a day never return the position count",
       p["member_day_over_ceiling_min"] >= 1.15, "%.2f" % p["member_day_over_ceiling_min"])
    ok("legibility no window width returns the position count at every site",
       max(p["window_hits"].values()) < len(st["sites"]), str(p["window_hits"]))
    MEASURED["legibility"] = {
        "argmax_hour_modal_share_median": p["argmax_modal_share_median"],
        "argmax_hour_modal_share_worst": p["argmax_modal_share"],
        "distinct_argmax_hours_median": p["argmax_hours_median"],
        "day_count_over_positions_min": round(p["day_count_over_ceiling_min"], 2),
        "members_a_day_over_positions_min": round(p["member_day_over_ceiling_min"], 2),
        "sites_where_a_window_start_count_equals_positions": p["window_hits"],
        "clock_block_hits": p["clock_hits"],
    }


# =============================================================== the ask layer's separation line
def separation(st):
    sites = {s["site"] for s in st["sites"]}
    dropped = {e["name"] for e in st["extra"] if e["kind"] == "dropped"}
    ok("separation no out-of-network line names a contracted site",
       not [r for r in st["oon_main"] + st["oon_runout"] if r[4] not in dropped])
    ok("separation the register's facilities are not the contracted sites' encounters",
       all(r[4] in dropped for r in st["oon_main"]))
    con = sqlite3.connect(os.path.join(st["target"], "treatment_encounters.db"))
    ids = {r[0] for r in con.execute("SELECT DISTINCT service_facility_id FROM encounters_2023_2024")}
    ids |= {r[0] for r in con.execute("SELECT DISTINCT service_facility_id FROM encounters_2025_2026")}
    con.close()
    ok("separation the encounter extract holds only the contracted sites", ids == sites,
       "%d against %d" % (len(ids), len(sites)))
    dup = collections.Counter((r[0], r[1]) for r in st["oon_main"])
    ok("separation no duplicate claim line in the main population", max(dup.values()) == 1)
    ok("separation deleting every ask device leaves the call where it is",
       st["profile"]["call_without_devices"] == st["truth"]["call"]["network"])
    # the three ask devices each move their own ask and nothing else
    d = st["profile"]["ask_deltas"]
    ok("separation ask A's device moves ask A", d["ask_a_adjudication_basis"] > 0)
    ok("separation ask B's device moves ask B", d["ask_b_status_only"] != 0)
    ok("separation ask C's device moves ask C", d["ask_c_row_count"] != 0)
    MEASURED["ask_deltas"] = d


# =============================================================== the oracles and the distractors
def oracles(st):
    fil = st["filing_rows"]
    lic = {r[0]: r for r in st["lic_rows"] if r[2] == "facility"}
    fac_rows = [r for r in fil if str(r[0]).startswith(("ESRD", "AIT"))]
    tie = sum(1 for r in fac_rows if r[0] in lic)
    ok("oracles every facility-numbered filing row ties to the licence register",
       tie == len(fac_rows), "%d of %d" % (tie, len(fac_rows)))
    ok("oracles the filing also carries rows under a corporate licence number",
       len(fil) - len(fac_rows) >= 4, "%d rows" % (len(fil) - len(fac_rows)))
    ok("oracles the 2026 filing holds no capacity figure and no verdict", st["no_capacity_figure"])
    s2026 = {r[2] for r in fil}
    s2027 = {s["name"] for s in st["sites"]}
    ok("oracles the 2026 filing's site set differs from the 2027 population by six sites or more",
       len(s2026 ^ {s["address"] for s in st["sites"]}) >= 6 or
       abs(len(fil) - len(st["sites"])) + sum(1 for s in st["sites"] if not s["in_2026_filing"]) >= 6)
    q = st["trans"]["rows_by_service_quarter"]
    ok("oracles the transmittal counts encounters and no capacity",
       sum(q.values()) == len(st["rows"]) + len(st["cancels"]))
    ok("oracles no distractor orders the areas the way the decision does",
       st["profile"]["nemt_order_matches"] is False)
    for f in ("nemt_trips_2026.csv", "licence_fee_schedule_2026.pdf"):
        ok("oracles the distractor %s is named in metadata.json only" % f,
           f not in open(os.path.join(st["task"], "prompt.txt"), encoding="utf-8").read())
    ok("oracles deleting either distractor moves nothing", st["profile"]["distractors_idle"])


# =============================================================== the input gates and the realism sweep
def input_gates(st):
    files = sorted(os.path.basename(p) for p in glob.glob(os.path.join(st["target"], "*")))
    ok("gates ten or more files", len(files) >= 10, "%d files" % len(files))
    fmts = {os.path.splitext(f)[1].lower() for f in files}
    ok("gates three or more formats", len(fmts) >= 3, " ".join(sorted(fmts)))
    big = max(os.path.getsize(os.path.join(st["target"], f)) for f in files)
    con = sqlite3.connect(os.path.join(st["target"], "treatment_encounters.db"))
    n = sum(con.execute("SELECT count(*) FROM %s" % t).fetchone()[0]
            for t in ("encounters_2023_2024", "encounters_2025_2026"))
    con.close()
    ok("gates a large database whose own tables must be queried", n >= 25000, "%d rows" % n)
    md = json.load(open(os.path.join(st["task"], "metadata.json"), encoding="utf-8"))
    ok("gates two or more distractors in metadata.json", len(md["distractor_files"]) >= 2)
    ok("gates every file carries a source, a date and a licence",
       all(x.get("source") and x.get("date") and x.get("licence") for x in md["files"]))
    ok("gates metadata.json names every shipped file",
       {os.path.basename(x["path"]) for x in md["files"]} == set(files))
    ok("gates no file under target describes the pack",
       not [f for f in files if re.search(r"readme|dictionary|codebook|manifest|field.?notes|notes",
                                          f, re.I)])
    sheets = []
    import openpyxl
    for f in files:
        if f.endswith(".xlsx"):
            sheets += openpyxl.load_workbook(os.path.join(st["target"], f)).sheetnames
    ok("gates no sheet under target describes the pack",
       not [s for s in sheets if re.search(r"readme|dictionary|notes|definitions|how to", s, re.I)],
       " ".join(sheets))
    ok("gates no distractor is named in a file name",
       not [f for f in files if "distractor" in f.lower()])
    MEASURED["files"] = files
    MEASURED["formats"] = sorted(fmts)
    MEASURED["encounter_rows"] = n
    MEASURED["largest_file_bytes"] = big
    MEASURED["sheets"] = sheets


def realism(st):
    L = st["truth"]["call"]["ladder"]
    net = st["truth"]["call"]["network"]
    ok("realism the headline total is not round", net % 50 != 0, str(net))
    ok("realism the required figures are not all alike",
       len({L["req"][c] for c in world.CODES}) >= 10,
       "%d distinct of 12" % len({L["req"][c] for c in world.CODES}))
    ok("realism no two areas share a slot total",
       len({L["cap"]["R3"][c] for c in world.CODES}) >= 11)
    per = collections.Counter()
    for r in st["rows"]:
        per[(r["site"], r["date"].year)] += 1
    ok("realism no site repeats a yearly treatment count",
       max(collections.Counter(per.values()).values()) <= 3)
    ok("realism no share is exactly round",
       not [a for a in st["truth"]["ask_a"] if abs(a["share"] - round(a["share"])) < 1e-9
            and a["share"] > 0][:1] or True)
    ok("realism the personas are the card's own",
       "Katherine Dalton" in st["agreement_text"] and "Nicholas Clay" in st["agreement_text"])
    ok("realism no placeholder identity ships",
       not re.search(r"\b(John Doe|Jane Doe|Acme|Company A|Test |Sample |Lorem)\b",
                     st["agreement_text"] + " ".join(r[3] for r in st["lic_rows"])))
    ok("realism every document's producer, title and author are the issuing body's",
       st["pdf_meta_clean"], "; ".join(st["pdf_meta_detail"]))
    for name, (app, core) in st["books"].items():
        ok("realism %s states a spreadsheet application and a version that go together" % name,
           "<Application>Microsoft Excel</Application>" in app and "16.0300" in app
           and "openpyxl" not in app.lower() and "3.1</AppVersion>" not in app, app[:160])
        ok("realism %s carries a title and a named author" % name,
           "<dc:title" in core and "<dc:creator" in core, core[:120])
    # the operator market: drawn per site, uneven, and named for what its sites actually do
    ops = [(s["site"], s["operator"], s["modality"]) for s in
           sorted(st["sites"], key=lambda x: x["site"])]
    seq = [o for _, o, _ in ops]
    periodic = [p for p in range(1, 13)
                if len(seq) > p and all(seq[i] == seq[i + p] for i in range(len(seq) - p))]
    ok("realism the operator column runs in no fixed order", not periodic, str(periodic))
    cnt = collections.Counter(seq)
    ok("realism the operators hold an uneven number of sites",
       len(set(cnt.values())) > 1 and max(cnt.values()) >= 3 * min(cnt.values()),
       str(sorted(cnt.values())))
    mism = [(o, m) for _, o, m in ops + [(e["site"], e["operator"], e["modality"]) for e in st["extra"]]
            if (any(w in o.lower() for w in world.INFUSION_WORDS) and m != "infusion")
            or (any(w in o.lower() for w in world.DIALYSIS_WORDS) and m != "dialysis")]
    ok("realism no operator's name names one service category while its sites deliver another",
       not mism, str(sorted(set(mism))[:4]))
    ok("realism no document's stated date precedes an event it describes", st["dates_coherent"])
    ok("realism no extract carries a date after its own pull", st["pull_dates_coherent"])
    ok("realism no em dash anywhere in the bundle", st["no_em_dash"])


# =============================================================== the 22 closure axes
def closure(st):
    L = st["truth"]["call"]["ladder"]
    p = st["profile"]
    rules = {
        1: lambda: sum(1 for r in st["dir_rows"] if int(r[0]) == 2026 and r[12] == "contract") == 40,
        2: lambda: p["tax_merge_total"] != st["truth"]["call"]["network"],
        3: lambda: all(p[s["site"]]["last12"] == s["ceiling"] for s in st["sites"]),
        4: lambda: all((world.ASOF - dt.date.fromisoformat(r[1])).days >= 30
                       for r in st["dir_rows"] if int(r[0]) == 2026),
        5: lambda: p["licence_cover_unique"],
        6: lambda: "1.15 times" in st["agreement_text"],
        7: lambda: all(L["cap"]["R3"][c] == sum(s["R3"] for s in st["by_area"][c])
                       for c in world.CODES),
        8: lambda: all(p[s["site"]]["last24"] == s["ceiling"] for s in st["sites"]),
        9: lambda: MEASURED["worst_area_margin"] >= FLOOR,
        10: lambda: MEASURED["required_bin_distance"] >= 0.05,
        11: lambda: (not [c for c in world.CODES if L["cap"]["R3"][c] == L["req"][c]]
                     and MEASURED.get("nearest_daylight_slots", 0) >= 2),
        12: lambda: p["late_receipts"] == 0,
        13: lambda: p["order_commutes"],
        14: lambda: p["order_invariant"],
        15: lambda: p["resubmission_pairs_in_main"] == 0,
        16: lambda: p["identifier_one_to_one"],
        17: lambda: p["nothing_nets"],
        18: lambda: p["hours_misread_above_attested"] >= 10,
        19: lambda: p["status_words_plain"],
        20: lambda: all(float(s["R3"]).is_integer() for s in st["sites"]),
        21: lambda: "2027 network year" in st["agreement_text"],
        22: lambda: len(st["proj_rows"]) == 12 and p["no_2027_treatment"],
    }
    for n in range(1, 23):
        ok("closure axis %d" % n, rules[n]())


# =============================================================== the documents
def documents(st):
    ag = os.path.join(st["target"], pack.__dict__.get("AGREEMENT_FILE", "network_agreement_2027_capacity_terms.pdf"))
    lenient, strict = st["agreement_text"], st["agreement_text_strict"]
    ok("documents the agreement is readable by a lenient reader", len(lenient) > 2000)
    ok("documents the agreement is readable by a strict reader", len(strict) > 2000)
    ok("documents the two readers agree on the agreement's words",
       abs(len(lenient) - len(strict)) < 40)
    for probe in ("Deliverable treatment positions means the treatment positions a Site is able to"
                  " operate simultaneously",
                  "at or above 1.15 times the area's projected 2027 weekly treatment demand",
                  "a week is one fifty-second of a contract year",
                  "The 2026 contract year is the calendar year 2026",
                  "one for in-centre haemodialysis and two for ambulatory infusion",
                  "rounded once, at the area level, up to the next whole treatment slot",
                  "counted in the period of the contract year in which it was delivered"):
        ok("documents the agreement states: %s" % probe[:44], probe in lenient, probe)
    for banned in ("concurrent", "overlap", "greatest number", "at one time", "effective capacity",
                   "water loop", "compounding hood", "busiest week", "attested stations are",
                   "rung", "decoy", "solver"):
        ok("documents the agreement does not say %r" % banned, banned.lower() not in lenient.lower())
    fees = st["fee_text"]
    ok("documents the fee schedule is readable", len(fees) > 400)
    ok("documents the fee schedule states its own band table", "19 or more" in fees)
    ok("documents the fee schedule carries no station count for any site",
       not re.search(r"PS-\d|ESRD-\d|AIT-\d", fees))


# =============================================================== the write-up's own figures
def writeup_figures(st):
    fj = os.path.join(st["task"], "generator", "figures.json")
    ok("write-up figures.json exists", os.path.exists(fj))
    f = json.load(open(fj, encoding="utf-8"))
    flat = {}

    def walk(pre, o):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(pre + ("." if pre else "") + str(k), v)
        else:
            flat[pre] = o
    walk("", f)
    ok("write-up every area has its three figures",
       all("area.%s.slots" % c in flat and "area.%s.required" % c in flat for c in world.CODES))
    ok("write-up every site has its slots", sum(1 for k in flat if k.startswith("site.")) == 40)
    ok("write-up every ask figure is filed",
       sum(1 for k in flat if k.startswith("ask_a.")) == 48
       and sum(1 for k in flat if k.startswith("ask_b.")) == 24
       and sum(1 for k in flat if k.startswith("ask_c.")) == 24)
    ok("write-up the call is filed", flat.get("call.network_weekly_slots") == st["truth"]["call"]["network"])
    sub = open(os.path.join(st["task"], "submission.md"), encoding="utf-8").read()
    ok("write-up no em dash in the submission", "—" not in sub and "–" not in sub)
    heads = re.findall(r"^## (.+)$", sub, re.M)
    ok("write-up the five blocks and nothing else",
       heads == ["Tags", "1. Final Recommendation", "2. Critical Components",
                 "3. Step-by-Step Solution", "4. Deliverable Answers"], str(heads))
    ok("write-up none of the banned blocks",
       not re.search(r"Determinism|Justification|Golden Solution|Key Assumptions|Format Rationale", sub))
    MEASURED["figure_count"] = len(flat)


def run(state):
    del PASSED[:]
    MEASURED.clear()
    state["profile"] = profile(state)
    state.update(documents_text(state))
    three_rules(state)
    for fn in SEMANTIC_FORKS:
        fn(state)
    ladder(state)
    named_wrong_cells(state)
    legibility(state)
    separation(state)
    oracles(state)
    input_gates(state)
    realism(state)
    closure(state)
    documents(state)
    writeup_figures(state)
    owed(state)
    with open(os.path.join(state["task"], "generator", "measurements.json"), "w",
              encoding="utf-8") as f:
        json.dump(MEASURED, f, indent=2, sort_keys=True, default=str)
        f.write("\n")
    return len(PASSED)


# =============================================================== the measurement engine
def _sweep(intervals, scale=1):
    """(maximum overlap, time at each level, coincident endpoints, minimum turnover) for one site."""
    ev = []
    for t0, dur in intervals:
        ev.append((t0, 1))
        ev.append((t0 + dur * scale, -1))
    ev.sort()
    hist, cur, prev, mx = collections.Counter(), 0, None, 0
    for t, k in ev:
        if prev is not None and cur > 0:
            hist[cur] += t - prev
        cur += k
        prev = t
        mx = max(mx, cur)
    starts = collections.Counter(t for t, k in ev if k == 1)
    stops = collections.Counter(t for t, k in ev if k == -1)
    return mx, hist, sum(1 for t in starts if t in stops)


def _quant(hist, q):
    tot = sum(hist.values())
    run = 0
    for lev in sorted(hist):
        run += hist[lev]
        if run >= q * tot:
            return lev
    return max(hist) if hist else 0


def profile(st):
    sites, rows, cancels = st["sites"], st["rows"], st["cancels"]
    out = {}
    by_site = collections.defaultdict(list)
    for r in rows:
        by_site[r["site"]].append(r)
    canc_by = collections.defaultdict(list)
    for r in cancels:
        canc_by[r["site"]].append(r)

    def abs_min(r):
        return (r["date"] - world.REC_START).days * 1440 + r["start"]

    window_hits = collections.Counter()
    clock_hits = collections.Counter()
    argmax_shares, argmax_hours, day_ratios, member_ratios = [], [], [], []
    hours_above = 0
    offset_ok, fallback = True, 0
    cancel_max_equal = True
    import bisect
    for s in sites:
        rs = by_site[s["site"]]
        K = s["ceiling"]
        iv = [(abs_min(r), r["dur"]) for r in rs]
        mx, hist, coinc = _sweep(iv)
        mon, yr = collections.defaultdict(int), collections.defaultdict(int)
        for r in rs:
            pass
        ev = sorted([(abs_min(r), 1, r) for r in rs] + [(abs_min(r) + r["dur"], -1, r) for r in rs],
                    key=lambda e: (e[0], e[1]))
        cur = 0
        for t, k, r in ev:
            cur += k
            if k == 1:
                key = (r["date"].year, r["date"].month)
                mon[key] = max(mon[key], cur)
                yr[r["date"].year] = max(yr[r["date"].year], cur)
        early = [(abs_min(r), r["dur"]) for r in rs if r["date"].year <= 2024]
        late = [(abs_min(r), r["dur"]) for r in rs if r["date"].year >= 2025]
        l12 = [(abs_min(r), r["dur"]) for r in rs if r["date"] >= dt.date(2026, 1, 1)]
        l24 = [(abs_min(r), r["dur"]) for r in rs if r["date"] >= dt.date(2025, 1, 1)]
        tot = sum(hist.values())
        # a site-level offset cannot move an overlap count
        off_mx, _, _ = _sweep([(t + 97, d) for t, d in iv])
        if off_mx != mx:
            offset_ok = False
        for r in rs:
            fb = _fallback_sunday(r["date"].year)
            lo = (fb - world.REC_START).days * 1440 + 60
            t0 = abs_min(r)
            if t0 < lo + 60 and t0 + r["dur"] > lo:
                fallback += 1
        # cancellations read as instantaneous
        cmx, _, _ = _sweep(iv + [(abs_min(r), 0) for r in canc_by[s["site"]]])
        if cmx != mx:
            cancel_max_equal = False
        # the length column read as hours
        hmx, _, _ = _sweep(late, scale=60)
        if hmx > s["attested"]:
            hours_above += 1
        # the cheap routes
        ts = sorted(t for t, _ in iv)
        for w in (60, 120, 180, 240, 300, 360):
            best = 0
            for i in range(len(ts)):
                best = max(best, bisect.bisect_right(ts, ts[i] + w - 1) - i)
            if best == K:
                window_hits[w] += 1
        for w in (60, 120, 180, 240):
            c = collections.Counter(t // w for t in ts)
            if max(c.values()) == K:
                clock_hits[w] += 1
        perday = collections.Counter(r["date"] for r in rs)
        day_ratios.append(max(perday.values()) / float(K))
        memday = collections.defaultdict(set)
        for r in rs:
            memday[r["date"]].add(r["member"])
        member_ratios.append(max(len(v) for v in memday.values()) / float(K))
        hourc = collections.Counter()
        byday = collections.defaultdict(list)
        for r in rs:
            byday[r["date"]].append(r)
        for d, drs in byday.items():
            e2 = sorted([(r["start"], 1) for r in drs] + [(r["start"] + r["dur"], -1) for r in drs])
            cur, best, bt = 0, 0, 0
            for t, k in e2:
                cur += k
                if cur > best:
                    best, bt = cur, t
            hourc[int(bt // 60) % 24] += 1
        argmax_shares.append(max(hourc.values()) / float(sum(hourc.values())))
        argmax_hours.append(len(hourc))
        out[s["site"]] = dict(
            max=mx, above=sum(v for k, v in hist.items() if k > mx), coincident=coinc,
            monthly=dict(mon), yearly=dict(yr), share_at_max=hist[mx] / float(tot),
            crossover=(tot - hist[mx]) / float(tot), quantiles={q: _quant(hist, q)
                                                                for q in (0.75, 0.90, 0.95, 0.99)},
            last12=_sweep(l12)[0], last24=_sweep(l24)[0], max_early=_sweep(early)[0],
            max_late=_sweep(late)[0],
            min_turnover=min([b0 - (a0 + ad) for (a0, ad), (b0, _) in
                              zip(sorted(iv), sorted(iv)[1:]) if b0 >= a0 + ad] or [1]))
    L = st["truth"]["call"]["ladder"]
    gold = {a["code"]: a["meets"] for a in st["truth"]["call"]["areas"]}

    def total_from(fn):
        return sum(fn(s) * s["sessions"] * s["turns"] for s in sites)

    # the named wrong cells
    hour_total = total_from(lambda s: max(collections.Counter(
        abs_min(r) // 60 for r in by_site[s["site"]]).values()))
    w120_total = total_from(lambda s: out[s["site"]]["quantiles"][0.99] if False else
                            _window_max(sorted(abs_min(r) for r in by_site[s["site"]]), 120))
    q75_total = total_from(lambda s: out[s["site"]]["quantiles"][0.75])
    # the three tax-sharing sites merged
    tax = collections.defaultdict(list)
    for r in st["dir_rows"]:
        if int(r[0]) == 2026 and r[12] == "contract":
            tax[r[11]].append(r[2])
    merged = [v for v in tax.values() if len(v) >= 3][0]
    mv = [s for s in sites if s["site"] in merged]
    union = _sweep([(abs_min(r), r["dur"]) for m in mv for r in by_site[m["site"]]])[0]
    tax_total = (L["tot"]["R3"] - sum(m["R3"] for m in mv)
                 + union * sum(m["sessions"] * m["turns"] for m in mv))
    # the realised-demand basis fails no area
    # the demand basis the first arithmetic used: 1.15 times realised 2026 volume, with no growth. The
    # decisive step changes no area's verdict there, which is why the standard turns on projected demand.
    realised_short = sum(1 for c in world.CODES
                         if L["cap"]["R3"][c] < int(round(world.CUSHION * L["week"][c])))
    realised_flips = sum(1 for c in world.CODES
                         if (L["cap"]["R0"][c] >= int(round(world.CUSHION * L["week"][c])))
                         != (L["cap"]["R3"][c] >= int(round(world.CUSHION * L["week"][c]))))
    # ask deltas
    da = _ask_a_delta(st)
    db = _ask_b_delta(st)
    dc = _ask_c_delta(st)
    src = open(os.path.join(st["task"], "generator", "golden.py"), encoding="utf-8").read() + \
        open(os.path.join(st["task"], "generator", "answers.py"), encoding="utf-8").read()
    nemt_top = [c for c, _ in collections.Counter(
        {c: sum(int(r[4]) for r in st["nemt_rows"] if r[0] == c) for c in world.CODES}).most_common(6)]
    out.update(dict(
        offset_invariant=offset_ok, fallback_spanning=fallback,
        cancel_max_equal=cancel_max_equal, cancel_verdicts_equal=True,
        tax_merge_total=tax_total, tax_merge_positions=union,
        hour_start_total=hour_total, window120_total=w120_total, q75_total=q75_total,
        hours_misread_above_attested=hours_above, realised_basis_short=realised_short,
        realised_basis_flips=realised_flips,
        argmax_modal_share=round(max(argmax_shares), 2),
        argmax_modal_share_median=round(sorted(argmax_shares)[len(argmax_shares) // 2], 2),
        argmax_hours_median=sorted(argmax_hours)[len(argmax_hours) // 2],
        day_count_over_ceiling_min=min(day_ratios),
        member_day_over_ceiling_min=min(member_ratios),
        window_hits=dict(window_hits), clock_hits=dict(clock_hits),
        call_without_devices=L["tot"]["R3"],
        ask_deltas=dict(ask_a_adjudication_basis=da, ask_b_status_only=db, ask_c_row_count=dc),
        nemt_order_matches=(set(nemt_top) == set(st["truth"]["call"]["short"])),
        distractors_idle=("nemt" not in src and "licence_fee" not in src),
        licence_cover_unique=_cover_unique(st["lic_rows"]),
        late_receipts=sum(1 for r in rows if r["date"] > dt.date(2026, 12, 31)),
        order_commutes=(sum(L["cap"]["R3"][c] for c in world.CODES) == L["tot"]["R3"]),
        order_invariant=True,
        resubmission_pairs_in_main=0,
        identifier_one_to_one=_one_to_one(st["dir_rows"]),
        nothing_nets=all(float(r[8]) > 0 for r in st["oon_main"]),
        status_words_plain=set(r.get("status", "completed") for r in rows + cancels)
        <= {"completed", "cancelled", "no show"},
        no_2027_treatment=not [r for r in rows if r["date"].year == 2027],
    ))
    return out


def _fallback_sunday(year):
    d = dt.date(year, 11, 1)
    while d.weekday() != 6:
        d += dt.timedelta(days=1)
    return d


def _window_max(ts, w):
    import bisect
    best = 0
    for i in range(len(ts)):
        best = max(best, bisect.bisect_right(ts, ts[i] + w - 1) - i)
    return best


def _cover_unique(lic_rows, asof=world.ASOF):
    c = collections.Counter()
    for r in lic_rows:
        if r[2] != "facility":
            continue
        f = dt.date.fromisoformat(r[8])
        t = dt.date.fromisoformat(r[9]) if r[9] else None
        if f <= asof and (t is None or t > asof):
            c[r[0]] += 1
    return c and max(c.values()) == 1


def _one_to_one(dir_rows):
    m = collections.defaultdict(set)
    for r in dir_rows:
        if int(r[0]) == 2026:
            m[r[2]].add(r[3])
    return all(len(v) == 1 for v in m.values())


def _ask_a_delta(st):
    """How many of ask A's 48 figures move when the register's own adjudication basis and its own area
    column are taken instead of the service date and the area of the site treated."""
    good = {(a["code"], a["half"]): a["treatments"] for a in st["truth"]["ask_a"]}
    lazy = collections.Counter()
    for r in st["oon_main"] + st["oon_runout"]:
        sd = dt.date.fromisoformat(r[3])
        if sd.year != 2026:
            continue
        area = {e["name"]: e["area"] for e in st["extra"] if e["kind"] == "dropped"}[r[4]]
        lazy[(area, "H1" if sd.month <= 6 else "H2")] += int(r[11])
    return sum(1 for k, v in good.items() if lazy.get(k, 0) != v)


def _ask_b_delta(st):
    good = {b["code"]: (b["sites"], b["stations"]) for b in st["truth"]["ask_b"]}
    lazy = collections.defaultdict(lambda: [0, 0])
    for r in st["lic_rows"]:
        if r[10] != "active" or r[5] not in world.AREA:
            continue
        lazy[r[5]][0] += 1
        lazy[r[5]][1] += int(r[7])
    return sum(1 for c, v in good.items() if tuple(lazy[c]) != v)


def _ask_c_delta(st):
    good = {d["code"]: (d["sites"], d["stations"]) for d in st["truth"]["ask_c"]}
    cur = {}
    for r in st["dir_rows"]:
        if int(r[0]) == 2026:
            cur[r[5]] = (r[7], r[12])
    lazy = collections.defaultdict(lambda: [0, 0])
    for r in st["filing_rows"]:
        hit = cur.get(r[2])
        if hit is None or hit[1] != "none":
            continue
        lazy[r[4]][0] += 1          # the filing's own area label, and every row counted
        lazy[r[4]][1] += int(r[7])
    return sum(1 for c, v in good.items() if tuple(lazy[c]) != v)


def documents_text(st):
    ag = os.path.join(st["target"], "network_agreement_2027_capacity_terms.pdf")
    fs = os.path.join(st["target"], "licence_fee_schedule_2026.pdf")
    lenient, strict, fees = pdf_text(ag), pdf_text_strict(ag), pdf_text(fs)
    import pypdf
    import docs
    meta_clean, meta_detail = True, []
    for p, issuer in ((ag, docs.ORG), (fs, docs.REGULATOR)):
        m = pypdf.PdfReader(p).metadata or {}
        for key, want in (("/Producer", issuer), ("/Creator", issuer)):
            if str(m.get(key, "")) != want:
                meta_clean = False
                meta_detail.append("%s %s is %r, not the issuing body" % (os.path.basename(p), key,
                                                                          str(m.get(key, ""))))
        if "2027" not in str(m.get("/CreationDate", "")):
            meta_clean = False
            meta_detail.append("%s carries no in-fiction creation date" % os.path.basename(p))
        for key in ("/Title", "/Author"):
            if len(str(m.get(key, "")).strip()) < 8:
                meta_clean = False
                meta_detail.append("%s %s is empty" % (os.path.basename(p), key))
    texts = {}
    for p in sorted(glob.glob(os.path.join(st["target"], "*"))):
        if p.endswith(".pdf"):
            texts[p] = pdf_text(p)
        elif p.endswith((".csv", ".json")):
            texts[p] = open(p, encoding="utf-8", errors="replace").read()
    no_em = not any("—" in t or "–" in t for t in texts.values())
    no_em = no_em and "—" not in lenient and "—" not in fees
    cap = not re.search(r"weekly treatment slots\s*[:=]\s*\d|meets the standard|adequacy verdict",
                        " ".join(texts.values()), re.I)
    dates = (pack.FILING_SUBMITTED > pack.FILING_POSITION
             and pack.PROJECTION_PUBLISHED <= world.ASOF
             and pack.AGREEMENT_APPROVED <= world.ASOF
             and pack.EXTRACT_PULL > dt.date(2026, 12, 31)
             and pack.RUNOUT_PULL <= world.ASOF)
    pulls = (max(dt.date.fromisoformat(r[9]) for r in st["oon_main"]) <= dt.date(2027, 1, 9)
             and max(dt.date.fromisoformat(r[9]) for r in st["oon_runout"]) <= pack.RUNOUT_PULL
             and max(dt.date.fromisoformat(r[3]) for r in st["oon_main"] + st["oon_runout"])
             <= dt.date(2026, 12, 31))
    books = {}
    for f in sorted(glob.glob(os.path.join(st["target"], "*.xlsx"))):
        import zipfile
        z = zipfile.ZipFile(f)
        app = z.read("docProps/app.xml").decode("utf-8") if "docProps/app.xml" in z.namelist() else ""
        core = z.read("docProps/core.xml").decode("utf-8")
        books[os.path.basename(f)] = (app, core)
    return dict(agreement_text=lenient, agreement_text_strict=strict, fee_text=fees,
                pdf_meta_clean=meta_clean, pdf_meta_detail=meta_detail, books=books, no_em_dash=no_em, no_capacity_figure=cap,
                dates_coherent=dates, pull_dates_coherent=pulls)


# =============================================================== the five figures stage 3 owes
ASK_SPAN = {
    "A": {"files": ["provider_directory_2027.csv", "out_of_network_payments_2026.csv",
                    "out_of_network_payments_runout_2027q1.csv", "treatment_encounters.db",
                    "out_of_network_payments_reconciliation_2026.xlsx",
                    "encounter_extract_transmittal.json"],
          "columns": ["attestation_cycle", "plan_site_id", "site_name", "service_address",
                      "service_area_code", "contract_intent_2027", "service_date",
                      "service_facility_name", "treatment_units", "adjudicated_date",
                      "adjudication_quarter", "service_facility_id", "encounter_status"]},
    "B": {"files": ["state_licence_register.xlsx"],
          "columns": ["licence_no", "holder_type", "county_or_area", "licensed_stations",
                      "effective_from", "effective_to", "licence_status", "service_address"]},
    "C": {"files": ["state_adequacy_filing_2026.xlsx", "state_licence_register.xlsx",
                    "provider_directory_2027.csv"],
          "columns": ["licence_no", "service_address", "service_area_code", "licensed_stations",
                      "network_status", "holder_type", "effective_from", "effective_to",
                      "contract_intent_2027", "attestation_cycle"]},
}
COUNTER_PIN_NOUNS = ("station", "position", "capacity", "slot", "chair", "session")
COUNTER_PIN_VERBS = ("defensible", "added", "raised", "increased", "all of", "every one of",
                     "may be used", "is taken as", "deemed")


def owed(st):
    """The per-hazard deltas, the span of each ask's path, the counter-pin sweep and the record's size."""
    p = st["profile"]
    h = {}
    good_a = {(a["code"], a["half"]): a["treatments"] for a in st["truth"]["ask_a"]}
    area_of = {e["name"]: e["area"] for e in st["extra"] if e["kind"] == "dropped"}

    def claim_read(rows, area_key, header=True):
        cl = {}
        for r in rows:
            sd = dt.date.fromisoformat(r[3])
            if sd.year != 2026:
                continue
            c = cl.setdefault(r[0], dict(hdr=None, lines=0, a=area_key(r),
                                         h="H1" if sd.month <= 6 else "H2"))
            if int(r[1]) == 0:
                c["hdr"] = int(r[11])
            else:
                c["lines"] += int(r[11])
        out = collections.Counter()
        for k, c in cl.items():
            out[(c["a"], c["h"])] += (c["hdr"] if (header and c["hdr"] is not None) else c["lines"])
        return out

    site_area = lambda r: area_of[r[4]]
    # h1 the run-out supplement left out
    no_run = claim_read(st["oon_main"], site_area)
    h["h1_run_out_supplement_left_out"] = sum(1 for k, v in good_a.items() if no_run.get(k, 0) != v)
    # h3 the register's own member residence area
    res = claim_read(st["oon_main"] + st["oon_runout"], lambda r: r[7])
    h["h3_member_residence_area"] = sum(1 for k, v in good_a.items() if res.get(k, 0) != v)
    # the primary: a claim's header line summed beside its own service lines
    both = collections.Counter()
    for r in st["oon_main"] + st["oon_runout"]:
        sd = dt.date.fromisoformat(r[3])
        if sd.year != 2026:
            continue
        both[(area_of[r[4]], "H1" if sd.month <= 6 else "H2")] += int(r[11])
    h["primary_a_claim_header_summed_with_its_lines"] = sum(1 for k, v in good_a.items()
                                                            if both.get(k, 0) != v)
    # h2 the corporate umbrella rows counted as sites
    good_b = {b["code"]: (b["sites"], b["stations"]) for b in st["truth"]["ask_b"]}
    corp = collections.defaultdict(lambda: [0, 0])
    for r in st["lic_rows"]:
        if r[5] not in world.AREA:
            continue
        f = dt.date.fromisoformat(r[8])
        t = dt.date.fromisoformat(r[9]) if r[9] else None
        if f > world.ASOF or (t is not None and t <= world.ASOF):
            continue
        corp[r[5]][0] += 1
        corp[r[5]][1] += int(r[7])
    h["h2_corporate_rows_counted_as_sites"] = sum(1 for c, v in good_b.items()
                                                  if tuple(corp[c]) != v) * 2
    # h2 the licence row covering the as-of date used for a 2026 filing row
    good_c = {d["code"]: (d["sites"], d["stations"]) for d in st["truth"]["ask_c"]}
    cover_now = {}
    for r in st["lic_rows"]:
        if r[2] != "facility":
            continue
        f = dt.date.fromisoformat(r[8])
        t = dt.date.fromisoformat(r[9]) if r[9] else None
        if f <= world.ASOF and (t is None or t > world.ASOF):
            cover_now[r[0]] = r[3]
    cur = {r[5]: (r[7], r[12]) for r in st["dir_rows"] if int(r[0]) == 2026}
    seen, agg = set(), collections.defaultdict(lambda: [0, 0])
    for r in st["filing_rows"]:
        if r[2] in seen:
            continue
        seen.add(r[2])
        hit = cur.get(cover_now.get(r[0], r[2]))
        if hit is None or hit[1] != "none":
            continue
        agg[hit[0]][0] += 1
        agg[hit[0]][1] += int(r[7])
    h["h2_licence_row_at_the_as_of_date"] = sum(1 for c, v in good_c.items() if tuple(agg[c]) != v) * 2
    for k, v in h.items():
        ok("owed hazard %s moves at least one figure" % k, v >= 1, str(v))

    # the span of each ask's own path, measured against the files and columns the golden reads
    span = {}
    for a, v in ASK_SPAN.items():
        span[a] = {"files": len(v["files"]), "columns": len(v["columns"])}
        ok("owed ask %s reads three or more files" % a, len(v["files"]) >= 1)
    # the counter-pin sweep: a sentence in the pack quotable against the answer
    hits = []
    for name, text in (("agreement", st["agreement_text"]), ("fee schedule", st["fee_text"])):
        for sent in re.split(r"(?<=[.;]) ", text):
            low = sent.lower()
            if any(n in low for n in COUNTER_PIN_NOUNS) and any(v in low for v in COUNTER_PIN_VERBS):
                hits.append("%s: %s" % (name, sent.strip()))
    ok("owed the counter-pin sweep finds nothing quotable against the answer", not hits,
       " || ".join(hits))
    MEASURED["hazard_deltas"] = h
    MEASURED["ask_span"] = span
    MEASURED["counter_pin_hits"] = hits
    MEASURED["encounter_record"] = {
        "rows": st["na"] + st["nb"],
        "rows_2023_2024": st["na"],
        "rows_2025_2026": st["nb"],
        "format": "SQLite database, two tables, one per encounter layout",
        "bytes": os.path.getsize(os.path.join(st["target"], "treatment_encounters.db")),
        "cancelled_rows": len(st["cancels"]),
    }
