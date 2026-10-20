"""task474's data files: the town, county and region codes, the Bureau's 2020-2024 B17001 extract the State Data Center
pulled for its towns and regions, the Department of Social Services' monthly SNAP participation by town, the Bureau's
county-to-region allocation factors, and the Fund's grants data system exports (the client services extract, the
profile audit trail and Corbin Community Action's client number conversion)."""
import csv
import datetime as dt
import math

import numpy as np

import asks as A
import sources as S
import world as W

STATE_ROW = "Statewide"
CONVERSION_DAY = A.MIGRATION
CUT = A.EXTRACT_CUT


# ---------------------------------------------------------------------------------------------- writers
def write_csv(path, cols, rows, crlf=False, delimiter=","):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=delimiter, lineterminator="\r\n" if crlf else "\n")
        w.writerow(cols)
        for r in rows:
            w.writerow(r)
    return len(rows)


# ---------------------------------------------------------------------------------------------- codes
CODES_COLS = ["town", "town_geoid_county_basis", "county_fips", "former_county", "town_geoid_region_basis",
              "region_fips", "planning_region", "council_of_governments"]


def geoid_county(t):
    return W.STATE_FIPS + W.county_code(t["county"]) + t["cousub"]


def geoid_region(t):
    return W.STATE_FIPS + W.region_code(t["region"]) + t["cousub"]


def codes_rows():
    rows = []
    for t in sorted(W.TOWNS, key=lambda t: t["name"]):
        rows.append([t["name"], geoid_county(t), W.STATE_FIPS + W.county_code(t["county"]), t["county"],
                     geoid_region(t), W.STATE_FIPS + W.region_code(t["region"]), t["region"], W.COUNCIL[t["region"]]])
    return rows


# ---------------------------------------------------------------------------------------------- the Bureau's table
AGE_LABELS = S.AGES
ACS_COLS = ["geo_id", "summary_level", "area_name", "table_line", "label", "estimate", "margin_of_error"]


def acs_lines():
    """(line id, label, kind) for the table's 59 lines in the Bureau's order."""
    below = "Total:!!Income in the past 12 months below poverty level:"
    above = "Total:!!Income in the past 12 months at or above poverty level:"
    out = [("B17001_001", "Total:", "universe"), ("B17001_002", below, "total"), ("B17001_003", below + "!!Male:", "total")]
    out += [("B17001_%03d" % (4 + i), below + "!!Male:!!" + a, "cell") for i, a in enumerate(AGE_LABELS)]
    out += [("B17001_017", below + "!!Female:", "total")]
    out += [("B17001_%03d" % (18 + i), below + "!!Female:!!" + a, "cell") for i, a in enumerate(AGE_LABELS)]
    out += [("B17001_031", above, "total"), ("B17001_032", above + "!!Male:", "total")]
    out += [("B17001_%03d" % (33 + i), above + "!!Male:!!" + a, "cell") for i, a in enumerate(AGE_LABELS)]
    out += [("B17001_046", above + "!!Female:", "total")]
    out += [("B17001_%03d" % (47 + i), above + "!!Female:!!" + a, "cell") for i, a in enumerate(AGE_LABELS)]
    assert len(out) == 59
    return out


def town_values(name):
    a = S.ACS[name]
    b, ab = a["below_cells"], a["above_cells"]
    vals = [a["universe"], a["below"], sum(b[0::2])] + b[0::2] + [sum(b[1::2])] + b[1::2]
    vals += [a["above"], sum(ab[0::2])] + ab[0::2] + [sum(ab[1::2])] + ab[1::2]
    assert len(vals) == 59 and vals[1] == vals[2] + vals[16] and vals[0] == vals[1] + vals[30]
    return vals


def acs_rows():
    lines = acs_lines()
    town_v, town_m = {}, {}
    for t in W.TOWNS:
        v = town_values(t["name"])
        town_v[t["name"]] = v
        town_m[t["name"]] = [S.acs_moe(x, kind, t["name"] + lid) for x, (lid, _, kind) in zip(v, lines)]
    rows = []

    def emit(geo, level, name, vals, moes):
        for (lid, label, _), x, m in zip(lines, vals, moes):
            rows.append([geo, level, name, lid, label, x, m])

    def agg(names):
        vals = [sum(town_v[n][i] for n in names) for i in range(59)]
        moes = [int(round(math.sqrt(sum(town_m[n][i] ** 2 for n in names)))) for i in range(59)]
        return vals, moes
    emit("0400000US" + W.STATE_FIPS, "040", STATE_ROW, *agg([t["name"] for t in W.TOWNS]))
    for code, region in W.REGIONS:
        emit("0500000US" + W.STATE_FIPS + code, "050", "%s Planning Region" % region,
             *agg([t["name"] for t in W.TOWNS if t["region"] == region]))
    for t in sorted(W.TOWNS, key=geoid_region):
        kind = "city" if t["kind"] == "city" else "town"
        emit("0600000US" + geoid_region(t), "060", "%s %s, %s Planning Region" % (t["name"], kind, t["region"]),
             town_v[t["name"]], town_m[t["name"]])
    return rows


# ---------------------------------------------------------------------------------------------- DSS
SNAP_COLS = ["BENEFIT_MONTH", "TOWN", "HOUSEHOLDS", "RECIPIENTS"]


def dss_name(name):
    s = name.upper()
    for a, b in (("EAST ", "E "), ("NORTH ", "N "), ("WEST ", "W "), ("LOWER ", "LWR "), ("UPPER ", "UPR "),
                 (" CENTER", " CTR"), (" HILL", "-HILL")):
        s = s.replace(a, b)
    return s


def snap_months():
    return [(y, m) for y in range(2019, 2027) for m in range(1, 13) if (y, m) <= (2026, 6)]


def snap_rows():
    r = W.rng("dss_unknown")
    rows = []
    names = sorted(W.TOWNS, key=lambda t: dss_name(t["name"]))
    for y, m in snap_months():
        hh_tot = rec_tot = 0
        for t in names:
            v = S.SNAP[(t["name"], y, m)]
            rows.append(["%d%02d" % (y, m), dss_name(t["name"]), v["households"], v["recipients"]])
            hh_tot += v["households"]
            rec_tot += v["recipients"]
        unk_r = int(round(rec_tot * r.uniform(0.0021, 0.0037)))
        unk_h = int(round(unk_r / r.uniform(1.55, 1.85)))
        rows.append(["%d%02d" % (y, m), "UNKNOWN", unk_h, unk_r])
        rows.append(["%d%02d" % (y, m), "STATE TOTAL", hh_tot + unk_h, rec_tot + unk_r])
    return rows


# ---------------------------------------------------------------------------------------------- factors
FACTOR_COLS = ["county_fips", "county_name", "region_fips", "region_name", "pop2020_part", "afact_pop",
               "hu2020_part", "afact_hu"]


def factor_rows():
    rows = []
    for f in S.alloc_factors():
        rows.append([W.STATE_FIPS + W.county_code(f["county"]), f["county"] + " County",
                     W.STATE_FIPS + W.region_code(f["region"]), f["region"] + " Planning Region", f["pop"],
                     "%.4f" % f["afact"], f["hu"], "%.4f" % f["afact_hu"]])
    return rows


# ---------------------------------------------------------------------------------------------- the grants data system
EXTRACT_COLS = ["agency_code", "client_no", "household_no", "service_code", "service_date", "entered_on", "town",
                "amount_usd"]
AUDIT_COLS = ["agency_code", "client_no", "field", "old_value", "new_value", "effective_date", "changed_on",
              "changed_by"]
CONVERSION_COLS = ["old_client_no", "new_client_no", "converted_on"]
LANGS = ["English", "Spanish", "Portuguese", "Haitian Creole", "Vietnamese", "Arabic", "Polish"]
INCOME = ["Wages", "Unemployment insurance", "Social Security", "SSI", "TANF", "Child support", "Pension", "No income"]


def _entry_dates(services):
    """A service is entered once, as one transaction for every member it covers: each event's rows take the
    earliest entry the generator drew for them."""
    first = {}
    for s in services:
        k = (s["hh"], s["svc"], s["date"])
        first[k] = min(first.get(k, s["entered"]), s["entered"])
    return {id(s): first[(s["hh"], s["svc"], s["date"])] for s in services}


def gds():
    """The grants data system's view of the FY2026 records: client and household numbers (Corbin's earlier
    numbers before its conversion on 1 January 2026), the record each service row was entered under, the town each
    record carried when the extract was cut (a closed record keeps the town it had when it closed), and the audit
    trail of profile edits."""
    r = W.rng("gds")
    D = A.DATA
    people, hhs, services = D["people"], D["households"], D["services"]
    mig = A.MIGRATING
    # client numbers: the statewide sequence; Corbin's clients got a block of it at the conversion
    others = [p["pid"] for p in people if p["agency"] != mig]
    corbin = [p["pid"] for p in people if p["agency"] == mig]
    no = {}
    n = 4_103_217
    for i in r.permutation(len(others)):
        n += int(r.integers(1, 23))
        no[others[i]] = n
    legacy = {}
    n = 1_618_406
    for pid in corbin:
        n += int(r.integers(1, 7))
        legacy[pid] = n
    n = max(no.values()) + int(r.integers(3000, 6000))
    for pid in corbin:
        n += 1
        no[pid] = n
    # household numbers
    hno, hlegacy = {}, {}
    n = 302_118
    for hi in r.permutation(len(hhs)):
        hi = int(hi)
        n += int(r.integers(1, 9))
        hno[hi] = n
    n = 47_220
    for hi, h in enumerate(hhs):
        if h["agency"] == mig:
            n += int(r.integers(1, 5))
            hlegacy[hi] = n
    # the profile edit for each move, keyed by household: the day it was keyed in
    keyed = {}
    for hi, h in enumerate(hhs):
        if h["move"]:
            keyed[hi] = h["move"][1] + dt.timedelta(days=int(min(r.geometric(0.16), 24)) - 1)
    entered = _entry_dates(services)

    def record(pid_or_hh, agency, day, legacy_map, new_map):
        """The record a row entered on `day` sits under: Corbin's earlier record before the conversion."""
        if agency == mig and day < CONVERSION_DAY:
            return legacy_map[pid_or_hh]
        return new_map[pid_or_hh]

    def town_of_record(hi, agency, old_record):
        h = hhs[hi]
        if not h["move"]:
            return h["home"]
        if agency == mig and old_record:
            return h["move"][0] if keyed[hi] < CONVERSION_DAY else h["home"]
        return h["move"][0]

    rows = []
    for s in services:
        ent = entered[id(s)]
        if not (A.ENTRY_FROM <= ent <= CUT):
            continue
        old = s["agency"] == mig and ent < CONVERSION_DAY
        cno = legacy[s["pid"]] if old else no[s["pid"]]
        hno_ = hlegacy[s["hh"]] if old else hno[s["hh"]]
        amt = ("%d.00" % s["amount"]) if s["svc"] in ("RA", "EA") else ""
        rows.append(dict(agency=s["agency"], client_no=cno, household_no=hno_, svc=s["svc"], date=s["date"],
                         entered=ent, town=town_of_record(s["hh"], s["agency"], old), amount=amt, truth=s))
    rows.sort(key=lambda x: (x["entered"], A.CODE[x["agency"]], x["household_no"], x["client_no"], x["date"],
                             x["svc"]))
    # Wexmoor's April 2026 upload was received a second time with May's
    ag, lo, hi_ = A.RESENT
    batch = [x for x in rows if x["agency"] == ag and lo <= x["entered"] <= hi_]
    pos = max(i for i, x in enumerate(rows) if x["entered"] <= dt.date(2026, 5, 4)) + 1
    rows = rows[:pos] + [dict(x, resent=True) for x in batch] + rows[pos:]
    # the audit trail: the town and street edits of every moving household's members, under the record open when
    # each was keyed, and the everyday profile edits
    audit = []
    workers = {c: ["%s%03d" % (A.CODE[c].lower()[:3], int(k)) for k in r.choice(np.arange(101, 999), 14,
                                                                                    replace=False)]
               for c in W.COUNTY_NAMES}
    for hi, h in enumerate(hhs):
        if not h["move"]:
            continue
        k = keyed[hi]
        who = workers[h["agency"]][int(r.integers(0, 14))]
        for pid in h["members"]:
            cno = record(pid, h["agency"], k, legacy, no)
            audit.append([A.CODE[h["agency"]], cno, "street_address", "(redacted)", "(redacted)",
                          h["move"][1].isoformat(), k.isoformat(), who])
            audit.append([A.CODE[h["agency"]], cno, "town", h["home"], h["move"][0], h["move"][1].isoformat(),
                          k.isoformat(), who])
    days = (CUT - A.ENTRY_FROM).days
    for p in people:
        if r.random() > 0.31:
            continue
        h = hhs[p["hh"]]
        for _ in range(int(r.integers(1, 4))):
            k = A.ENTRY_FROM + dt.timedelta(days=int(r.integers(0, days + 1)))
            who = workers[p["agency"]][int(r.integers(0, 14))]
            cno = record(p["pid"], p["agency"], k, legacy, no)
            f = r.choice(["phone", "phone", "email", "preferred_language", "household_size", "income_source",
                          "street_address"])
            if f == "phone" or f == "email":
                audit.append([A.CODE[p["agency"]], cno, f, "(redacted)", "(redacted)", "", k.isoformat(), who])
            elif f == "preferred_language":
                a, b = r.choice(len(LANGS), 2, replace=False)
                audit.append([A.CODE[p["agency"]], cno, f, LANGS[a], LANGS[b], "", k.isoformat(), who])
            elif f == "household_size":
                old = h["size"] + int(r.choice([-1, 1]))
                audit.append([A.CODE[p["agency"]], cno, f, str(max(old, 1)), str(h["size"]),
                              (k - dt.timedelta(days=int(r.integers(0, 40)))).isoformat(), k.isoformat(), who])
            elif f == "income_source":
                a, b = r.choice(len(INCOME), 2, replace=False)
                audit.append([A.CODE[p["agency"]], cno, f, INCOME[a], INCOME[b],
                              (k - dt.timedelta(days=int(r.integers(0, 25)))).isoformat(), k.isoformat(), who])
            else:
                audit.append([A.CODE[p["agency"]], cno, f, "(redacted)", "(redacted)",
                              (k - dt.timedelta(days=int(r.integers(0, 30)))).isoformat(), k.isoformat(), who])
    audit.sort(key=lambda a: (a[6], a[0], a[1], a[2]))
    conversion = [[legacy[pid], no[pid], CONVERSION_DAY.isoformat()] for pid in corbin]
    return dict(rows=rows, audit=audit, conversion=conversion, no=no, legacy=legacy, hno=hno, hlegacy=hlegacy,
                keyed=keyed)


_GDS = None


def grants():
    global _GDS
    if _GDS is None:
        _GDS = gds()
    return _GDS


def extract_rows():
    return [[A.CODE[x["agency"]], x["client_no"], x["household_no"], x["svc"], x["date"].isoformat(),
             x["entered"].isoformat(), x["town"], x["amount"]] for x in grants()["rows"]]


def audit_rows():
    return grants()["audit"]


def conversion_rows():
    return grants()["conversion"]
