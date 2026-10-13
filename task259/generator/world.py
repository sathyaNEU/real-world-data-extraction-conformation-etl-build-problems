"""The world: Tallyband's respondents (every family, the data engineers among them) with the pay each reported and
when, the employers' level schemes and Tarnwick's crosswalk, the offers extract and OEWS wages beside them, and
Tarnwick's own HRIS job history, pay zones and ATS requisitions for the asks. The market's movement at a fixed level
and each person's merit inside a level are applied here and never shipped as figures."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd
from scipy.stats import norm

import common as K

# Level schemes employers use: the code for Tarnwick I to IV and Tallyband's normalised level for each
SCHEMES = {
    "L": (["L3", "L4", "L5", "L6"], ["L2", "L3", "L4", "L5"]),
    "E": (["E3", "E4", "E5", "E6"], ["L3", "L4", "L5", "L6"]),
    "IC": (["IC1", "IC2", "IC3", "IC4"], ["L2", "L3", "L4", "L5"]),
    "P": (["P2", "P3", "P4", "P5"], ["L3", "L3", "L4", "L5"]),
    "T": (["Engineer", "Engineer II", "Senior Engineer", "Staff Engineer"], ["L2", "L3", "L4", "L5"]),
    "G": (["G6", "G7", "G8", "G9"], ["L2", "L3", "L4", "L5"]),
}
STATES = [("CA", 0.22, 0.10), ("WA", 0.09, 0.08), ("NY", 0.09, 0.07), ("TX", 0.08, -0.03), ("MA", 0.05, 0.05),
          ("CO", 0.04, 0.00), ("IL", 0.04, -0.02), ("GA", 0.03, -0.04), ("NC", 0.03, -0.05), ("VA", 0.04, 0.00),
          ("NJ", 0.03, 0.03), ("OR", 0.03, 0.01), ("UT", 0.02, -0.04), ("FL", 0.04, -0.05), ("PA", 0.03, -0.03),
          ("MN", 0.02, -0.03), ("AZ", 0.02, -0.04), ("OH", 0.02, -0.06), ("MI", 0.02, -0.05), ("MD", 0.02, 0.00),
          ("WI", 0.01, -0.06), ("MO", 0.01, -0.07), ("TN", 0.01, -0.06), ("IN", 0.01, -0.07)]
WORDS_A = ("Quarry", "Lumen", "Harbor", "Cinder", "Ridge", "Marlin", "Copper", "Bramble", "Delta", "Ember", "Fjord",
           "Granite", "Heron", "Indigo", "Juniper", "Kestrel", "Lattice", "Meadow", "Nimbus", "Orchid", "Pioneer",
           "Quill", "Rook", "Sable", "Tundra", "Umber", "Vesper", "Willow", "Yarrow", "Zephyr", "Alder", "Basalt",
           "Cobalt", "Dune", "Estuary", "Falcon", "Glacier", "Hollow", "Iris", "Jasper")
WORDS_B = ("Labs", "Systems", "Data", "Cloud", "Software", "Analytics", "Health", "Logistics", "Pay", "Works",
           "Robotics", "Networks", "Bio", "Commerce", "Media", "Security", "Energy", "Mobility", "Foods", "Learning")
RELEVEL_EMPLOYER = "Quarry Systems"
FIRST = ("Basin", "Birch", "Bluff", "Boulder", "Bramble", "Breakwater", "Brook", "Canyon", "Channel", "Chestnut",
         "Cinder", "Cobble", "Coral", "Cove", "Crescent", "Crest", "Cypress", "Driftwood", "Dune", "Elm", "Ember",
         "Estuary", "Fable", "Fallow", "Fern", "Fieldstone", "Fjord", "Flint", "Foothill", "Garnet", "Glade", "Glen",
         "Grove", "Gull", "Harbor", "Hawthorn", "Hazel", "Heath", "Heron", "Hickory", "Hollow", "Inlet", "Ironwood",
         "Ivy", "Jasper", "Kestrel", "Lagoon", "Lantern", "Larch", "Laurel", "Linden", "Lodestar", "Magnolia",
         "Maple", "Marigold", "Marsh", "Meadow", "Moraine", "Moss", "Northgate", "Oakridge", "Orchard", "Osprey",
         "Palisade", "Pebble", "Plover", "Prairie", "Quill", "Raven", "Reef", "Riverbend", "Rook", "Rowan",
         "Saffron", "Sandstone", "Shale", "Shoal", "Silverleaf", "Sorrel", "Sparrow", "Spruce", "Stillwater",
         "Sycamore", "Tamarack", "Teal", "Thistle", "Thornbury", "Tidewater", "Timber", "Trillium", "Tundra",
         "Upland", "Verdant", "Wakefield", "Walnut", "Wayfarer", "Westbrook", "Wildflower", "Willow", "Windward",
         "Wren", "Yarrow", "Zephyr", "Amberly", "Bracken", "Brightwater", "Caldera", "Catalpa", "Chalk", "Cormorant",
         "Daybreak", "Dogwood", "Eastwind", "Elder", "Fennel", "Firth", "Gable", "Garland", "Glacier", "Heather",
         "Holloway", "Kettle", "Knoll", "Lakeshore", "Larkspur", "Loch", "Lowland", "Maplewood", "Marten",
         "Millbrook", "Nettle", "Oriole", "Outpost", "Peregrine", "Reedbank", "Ridgeline", "Saltmarsh", "Sandpiper",
         "Seabright", "Shoreline", "Skylark", "Solstice", "Stonebridge", "Sunridge", "Switchback", "Talon",
         "Terrace", "Thornfield", "Timberline", "Upstream", "Waypoint", "Whitewater", "Wildwood", "Windmill",
         "Woodland", "Alder", "Basalt", "Hollyhock", "Juncture", "Kelp", "Nimbus", "Quarrylight", "Rushmere",
         "Sable", "Tansy", "Umber", "Vesper", "Bellwether", "Bluebell", "Brambleton", "Cairn", "Coldwater",
         "Copperfield", "Dovetail", "Farrow", "Foxglove", "Greystone", "Halyard", "Harrier", "Inkwell", "Kittiwake",
         "Lindenwood", "Marshfield", "Mooring", "Nightjar", "Oxbow", "Pennant", "Puffin", "Quayside", "Redstart",
         "Rimrock", "Rushwood", "Seastack", "Sedge", "Shearwater", "Sloe", "Snowberry", "Stormfront", "Swale",
         "Tarn", "Thimble", "Torrent", "Turnstone", "Watershed", "Weir", "Whinchat", "Wicklow", "Larchmont",
         "Fairhaven", "Ashgrove", "Briarwood", "Deepwell", "Edgewater", "Fallowfield", "Glenhaven", "Highwater",
         "Kinross", "Longmeadow", "Mistwood", "Northfield", "Overbrook", "Pinecrest", "Rosewater", "Southwind",
         "Tallgrass", "Westwind", "Wintergreen", "Ambergate", "Blackthorn", "Castlemere", "Ashcombe", "Blythe",
         "Corrie", "Dunmore", "Eskdale", "Fernhill", "Glenmoor", "Hartwell", "Langdale", "Moorcroft", "Netherby",
         "Oakhurst", "Penrose", "Ravensworth", "Saltash", "Thornhill", "Underhill", "Yewdale", "Arnside",
         "Coldstream", "Kirkby", "Mossgiel", "Ottery", "Wendover", "Ashdown", "Bramblewood", "Coldharbour",
         "Dunstan", "Elmstead", "Fernlea", "Gorsefield", "Hartley", "Ingleby", "Kelso", "Lowther", "Merriwood",
         "Nethercote", "Oakleigh", "Pendle", "Redmire")
SURNAMES = ("Ashworth", "Barlow", "Calloway", "Ellery", "Fenwick", "Garrow", "Holcombe", "Jessop", "Kendrick",
            "Lindqvist", "Marlowe", "Nesbitt", "Osterman", "Pryor", "Quennell", "Radcliffe", "Thackeray", "Varga",
            "Whitlock", "Zeller", "Abernathy", "Brannigan", "Castellano", "Delacroix", "Eastman", "Fairbanks")
INITIALS = "BCDFGHJKLMNPQRSTVWXZ"
TRADE = ("Labs", "Systems", "Data", "Cloud", "Software", "Analytics", "Logistics", "Robotics", "Networks", "Commerce",
         "Media", "Mobility", "Learning", "Technologies", "Group", "Works", "Digital", "Interactive")
RELEVEL_DATE = dt.date(2025, 3, 3)
# each scheme's codes just below level I and just above level IV, which the crosswalk lists as out of scope
OUT_OF_SCOPE = {"L": ("L2", "L7"), "E": ("E2", "E7"), "IC": ("", "IC5"), "P": ("P1", "P6"),
                "T": ("Associate Engineer", "Principal Engineer"), "G": ("G5", "G10")}


def employers(n=260):
    r = K.stream("employers")
    names, out = set(), []
    while len(out) < n:
        nm = "%s %s" % (WORDS_A[int(r.integers(0, len(WORDS_A)))], WORDS_B[int(r.integers(0, len(WORDS_B)))])
        if nm in names:
            continue
        names.add(nm)
        scheme = list(SCHEMES)[int(r.choice(len(SCHEMES), p=(0.30, 0.15, 0.15, 0.12, 0.18, 0.10)))]
        out.append(dict(name=nm, scheme=scheme, size=float(r.pareto(1.3) + 1.0), effect=float(r.normal(0, 0.06))))
    if RELEVEL_EMPLOYER not in names:
        out[0]["name"] = RELEVEL_EMPLOYER
    for e in out:
        if e["name"] == RELEVEL_EMPLOYER:
            e["scheme"], e["size"] = "L", 6.0
    _arrivals(out)
    # the names employers trade under: a word each, a trade word on most
    rn = K.stream("employer_names")
    assert len(set(FIRST)) == len(FIRST) >= len(out)
    pick = rn.choice(len(FIRST), len(out), replace=False)
    sur = list(rn.permutation(len(SURNAMES)))
    for e, k in zip(out, pick):
        if e["name"] == RELEVEL_EMPLOYER:
            continue
        style = rn.random()
        word = TRADE[int(rn.integers(0, len(TRADE)))]
        if style < 0.08 and sur:
            e["name"] = "%s %s" % (SURNAMES[sur.pop()], word)
        elif style < 0.15:
            e["name"] = "%s %s" % ("".join(rn.choice(list(INITIALS), 3)), word)
        else:
            e["name"] = (FIRST[int(k)] + " " + word).strip() if rn.random() < 0.64 else FIRST[int(k)]
    assert len({e["name"] for e in out}) == len(out)
    return out


def _arrivals(emps):
    """When each employer's engineers began filing on Tallyband and what it pays at a fixed level: the employers
    already filing when the window opened (the larger ones more likely among them) and the ones that arrived through
    it, a later arrival paying less."""
    r = K.stream("arrivals")
    sizes = np.array([e["size"] for e in emps])
    rank = sizes.argsort().argsort() / (len(emps) - 1.0)
    p_early = np.clip(K.JOIN_EARLY_SHARE + 0.40 * (rank - 0.5), 0.05, 0.95)
    lo, hi = dt.date(2024, 7, 1), dt.date(2026, 6, 30)
    span = (hi - lo).days
    for e, pe in zip(emps, p_early):
        u = r.random()
        if e["name"] == RELEVEL_EMPLOYER or u < pe:
            e["joined"] = K.EXTRACT_FROM - dt.timedelta(days=int(r.integers(60, 1500)))
            e["premium"] = float(r.normal(*K.PREMIUM_EARLY))
        else:
            frac = float(r.random())
            e["joined"] = lo + dt.timedelta(days=int(frac * span))
            m0, fall, sd = K.PREMIUM_JOINER
            e["premium"] = float(r.normal(m0 + fall * frac, sd))
    return emps


def _flat_within(u, ages, emp, strata, iters=200):
    """u with every movement of its own inside an employer taken out: no slope on filing date within any employer
    in any stratum, nor across them with an intercept for each employer and each stratum."""
    u = np.asarray(u, float)
    cols = []
    for st in np.unique(strata):
        k = strata == st
        c = np.zeros(len(u))
        c[k] = ages[k] - pd.Series(ages[k]).groupby(emp[k]).transform("mean").to_numpy()
        cols.append(c)
    two = np.asarray(ages, float).copy()
    for _ in range(iters):
        two = two - pd.Series(two).groupby(emp).transform("mean").to_numpy()
        two = two - pd.Series(two).groupby(strata).transform("mean").to_numpy()
    cols.append(two)
    B = np.column_stack(cols)
    return u - B @ np.linalg.lstsq(B, u, rcond=None)[0]


def employer_weights(emps, on):
    """How likely a report filed on a date is to come from each employer: its size once its engineers file, ramping
    up over its first months on the platform."""
    w = np.empty(len(emps))
    for k, e in enumerate(emps):
        d = (on - e["joined"]).days
        w[k] = 0.0 if d < 0 else e["size"] * min(1.0, (d + 1) / K.JOIN_RAMP_DAYS)
    return w / w.sum()


def variant(name, r):
    """A respondent's own spelling of an employer name."""
    k = int(r.integers(0, 4))
    return (name + " Inc", name.lower(), name.replace(" ", ""), name + ", Inc.")[k]


def code_for(emp, level_idx, filed_on):
    """The employer's level code for Tarnwick level index 0..3 on a filing date (Quarry Systems re-levelled: from
    3 March 2025 its L5 is Tarnwick IV and L4 is III)."""
    codes, tally = SCHEMES[emp["scheme"]]
    if emp["name"] == RELEVEL_EMPLOYER and filed_on >= RELEVEL_DATE:
        codes = ["L2", "L3", "L4", "L5"]
        tally = ["L2", "L3", "L4", "L5"]
    return codes[level_idx], tally[level_idx]


def _quarter_edges():
    out, d = [], K.EXTRACT_FROM
    while d < K.BENCHMARK:
        nxt = (pd.Timestamp(d) + pd.DateOffset(months=3)).date()
        out.append((d, min(nxt, K.BENCHMARK)))
        d = nxt
    return out


def _filing_dates(r, n):
    """Filing dates over the 36 months to the benchmark date, denser recently as the platform grew."""
    span = (K.BENCHMARK - K.EXTRACT_FROM).days
    u = r.random(n)
    x = (np.sqrt(1 + 3.0 * u) - 1) / 1.0          # density rising linearly from 1 to 2 across the span
    x = x / x.max() if x.max() > 0 else x
    return [K.EXTRACT_FROM + dt.timedelta(days=int(v * (span - 1))) for v in x]


def tallyband():
    """Every respondent's current report. Matched data engineers' pay is built per level and filing quarter so
    each quarter's distribution sits exactly on the market's path; everyone else's is ordinary."""
    r = K.stream("tallyband")
    emps = employers()
    sizes = np.array([e["size"] for e in emps])
    fam_p = np.array([f[1] for f in K.FAMILIES])
    fam = np.array([f[0] for f in K.FAMILIES])[r.choice(len(K.FAMILIES), K.N_RESPONDENTS, p=fam_p / fam_p.sum())]
    st_p = np.array([s[1] for s in STATES])
    rows = []
    for i in range(K.N_RESPONDENTS):
        rows.append(dict(i=i, family=fam[i]))
    df = pd.DataFrame(rows)
    n = len(df)
    df["employer_idx"] = r.choice(len(emps), n, p=sizes / sizes.sum())
    df["level_idx"] = r.choice(4, n, p=(0.18, 0.30, 0.32, 0.20))
    df["state_idx"] = r.choice(len(STATES), n, p=st_p / st_p.sum())
    df["filed_on"] = _filing_dates(r, n)
    re_ = K.stream("employer_by_date")
    emp_of = np.empty(n, dtype=int)
    for d, idx in df.groupby("filed_on").indices.items():
        emp_of[idx] = re_.choice(len(emps), len(idx), p=employer_weights(emps, d))
    df["employer_idx"] = emp_of
    de = df.family == "Data Engineering"
    focus = np.array([f[0] for f in K.DE_FOCUS])[r.choice(len(K.DE_FOCUS), n, p=[f[1] for f in K.DE_FOCUS])]
    df["focus"] = np.where(de, focus, "")
    # employment and location: a few respondents outside the United States or not full time
    df["country"] = np.where(r.random(n) < 0.004, np.where(r.random(n) < 0.6, "CA", "GB"), "US")
    df["employment_type"] = np.where(r.random(n) < 0.004, np.where(r.random(n) < 0.5, "part_time", "contract"),
                                     "full_time")
    df["tenure"] = r.uniform(0.0, 4.0, n)
    df["noise"] = r.normal(0.0, 1.0, n)
    df["age"] = [K.years_to_benchmark(d) for d in df.filed_on]
    df["quarter"] = [int((d - K.EXTRACT_FROM).days // 91.3125) for d in df.filed_on]
    base = np.zeros(n)
    loc = np.array([STATES[k][2] for k in df.state_idx])
    prem = np.array([emps[k]["premium"] for k in df.employer_idx])
    score = loc + K.MERIT * (df.tenure - 2.0) + 0.06 * df.noise
    matched = de & (df.focus == K.DE_FOCUS[0][0]) & (df.country == "US") & (df.employment_type == "full_time")
    # the matched data engineers: the market's path within an employer, the employer's premium and each person's place
    # about their employer, drawn per level and filing quarter
    rs = K.stream("strata")
    quarters = np.array(sorted(df.quarter.unique()))
    wobble = {}
    for li, lv in enumerate(K.LEVELS):
        # each quarter's sample sits a little off the path, the wobble carrying no trend of its own
        w = rs.normal(0.0, 0.0008, len(quarters))
        A = np.c_[np.ones(len(quarters)), quarters]
        w = w - A @ np.linalg.lstsq(A, w, rcond=None)[0]
        wobble[li] = dict(zip(quarters, w))
        for q in quarters:
            idx = np.flatnonzero(matched & (df.level_idx == li) & (df.quarter == q))
            if not len(idx):
                continue
            k = len(idx)
            z = norm.ppf((np.arange(k) + rs.uniform(0.2, 0.8, k)) / k)
            z = z + K.SKEW[lv] * (z * z - 1.0)
            order = np.argsort(score.to_numpy()[idx], kind="mergesort")
            zz = np.empty(k)
            zz[order] = z
            base[idx] = zz
    # a person's place carries no movement of its own inside an employer: at each level, the within-employer slope of
    # the places on filing date is taken out, so the market's movement inside every employer is the path's
    ages = df.age.to_numpy()
    mm = matched.to_numpy()
    rows_ = np.flatnonzero(mm)
    base[rows_] = _flat_within(base[rows_], ages[rows_], df.employer_idx.to_numpy()[rows_],
                               df.level_idx.to_numpy()[rows_])
    for i in np.flatnonzero(mm):
        li = int(df.level_idx.iat[i])
        base[i] = K.MARKET_MEDIAN[K.LEVELS[li]] * np.exp(-K.MOVEMENT * ages[i] + wobble[li][df.quarter.iat[i]] +
                                                          prem[i] + K.SPREAD[K.LEVELS[li]] * base[i])
    # everyone else: the same levels, the family's own pay, an ordinary spread
    fam_mult = {"Software Engineering": 1.04, "Data Engineering": 1.0, "Machine Learning Engineering": 1.10,
                "Data Science": 0.98, "Product Management": 1.06, "Design": 0.86, "Site Reliability": 1.02,
                "Security Engineering": 1.03}
    other = ~matched
    lv_med = np.array([K.MARKET_MEDIAN[K.LEVELS[k]] for k in df.level_idx])
    fstep = np.array([fam_mult[f] for f in df.family])
    focus_step = np.array([dict((f[0], f[2]) for f in K.DE_FOCUS).get(f, 0.0) for f in df.focus])
    u = (score - score.mean()).to_numpy() + 0.05 * r.normal(0.0, 1.0, n)
    orow = np.flatnonzero(~mm)
    strata = np.array(["%s|%d|%s" % x for x in zip(df.family, df.level_idx, df.focus)])
    u[orow] = _flat_within(u[orow], ages[orow], df.employer_idx.to_numpy()[orow], strata[orow])
    oth = lv_med * fstep * np.exp(focus_step - K.MOVEMENT * df.age + prem + u)
    base = np.where(other, oth, base)
    # outside the United States: pay in US dollars at the filing date's rate, well below; part time paid as worked
    base = np.where(df.country != "US", base * r.uniform(0.62, 0.78, n), base)
    base = np.where(df.employment_type == "part_time", base * r.uniform(0.55, 0.75, n), base)
    base = np.where(df.employment_type == "contract", base * r.uniform(1.05, 1.25, n), base)
    df["base"] = base
    # previous reports: 30 per cent updated; a fifth of those were promoted into their level since
    rp = K.stream("previous")
    upd = rp.random(n) < 0.30
    gap = rp.uniform(0.5, 2.0, n)
    prom = upd & (rp.random(n) < 0.20) & (df.level_idx > 0)
    eps = rp.normal(0.0, 0.025, n)
    prev = np.where(prom, df.base * np.exp(-(K.MOVEMENT + K.MERIT) * gap - K.PROMOTION_STEP + eps),
                    df.base * np.exp(-(K.MOVEMENT + K.MERIT) * gap + eps))
    joined = np.array([emps[k]["joined"] for k in df.employer_idx])
    prev_on = np.array([d - dt.timedelta(days=int(round(g * 365.25))) for d, g in zip(df.filed_on, gap)])
    upd = upd & (prev_on >= joined)
    prom = prom & upd
    df["updated"], df["gap"], df["promoted"], df["prev_base"] = upd, gap, prom, prev
    # codes, titles, names, experience
    codes, tally, prev_codes, names, titles, yoe = [], [], [], [], [], []
    rt = K.stream("text")
    for row in df.itertuples():
        e = emps[row.employer_idx]
        c, t = code_for(e, row.level_idx, row.filed_on)
        codes.append(c)
        tally.append(t)
        prev_on = row.filed_on - dt.timedelta(days=int(round(row.gap * 365.25)))
        if row.updated:
            pc, _ = code_for(e, row.level_idx - 1 if row.promoted else row.level_idx, prev_on)
        else:
            pc = ""
        prev_codes.append(pc)
        names.append(variant(e["name"], rt) if rt.random() < 0.05 else e["name"])
        titles.append(_title(row.family, row.focus, row.level_idx, rt))
        lo, hi = ((1, 3), (3, 6), (5, 9), (8, 14))[row.level_idx]
        yoe.append(int(rt.integers(lo, hi + 1)))
    df["level_code"], df["tallyband_level"], df["previous_level_code"] = codes, tally, prev_codes
    df["employer"], df["title"], df["years_experience"] = names, titles, yoe
    df["employer_canonical"] = [emps[k]["name"] for k in df.employer_idx]
    df["state"] = np.where(df.country == "US", [STATES[k][0] for k in df.state_idx], "")
    df["previous_filed_on"] = [(d - dt.timedelta(days=int(round(g * 365.25)))) if u else None
                               for d, g, u in zip(df.filed_on, df.gap, df.updated)]
    df["respondent_id"] = ["TB-%s" % K.hexid("respondent", i, n=10).upper() for i in df.i]
    df["matched_truth"] = matched
    # reports Tallyband withdrew before the extract because they could identify a person
    rw = K.stream("withdrawn")
    gone = (df.family != "Data Engineering").to_numpy() & (rw.random(n) < 0.0051)
    df = df[~gone].reset_index(drop=True)
    return df, emps


def _title(family, focus, li, r):
    if family == "Data Engineering":
        if focus == "machine learning infrastructure":
            base = ("ML Infrastructure Engineer", "ML Platform Engineer", "Data Engineer, ML Platform")
        elif focus == "analytics engineering":
            base = ("Analytics Engineer", "Data Engineer, Analytics", "BI Engineer")
        else:
            base = ("Data Engineer", "Data Platform Engineer", "Data Pipeline Engineer")
        b = base[int(r.integers(0, len(base)))]
        pre = ("", "", "Senior ", "Staff ")[li]
        suf = ("", " II", "", "")[li] if b == "Data Engineer" and r.random() < 0.5 else ""
        return pre + b + suf
    short = {"Software Engineering": "Software Engineer", "Machine Learning Engineering": "Machine Learning Engineer",
             "Data Science": "Data Scientist", "Product Management": "Product Manager", "Design": "Product Designer",
             "Site Reliability": "Site Reliability Engineer", "Security Engineering": "Security Engineer"}[family]
    return ("", "", "Senior ", "Staff ")[li] + short


def crosswalk(emps):
    """Tarnwick's level crosswalk: every employer's engineering level codes to Tarnwick's levels, Quarry Systems
    effective-dated around its re-levelling."""
    rows = []
    rx = K.stream("crosswalk_extra")
    first = dt.date(2019, 1, 7)
    for e in sorted(emps, key=lambda e: e["name"]):
        codes, _ = SCHEMES[e["scheme"]]
        since = (first + dt.timedelta(days=7 * int(rx.integers(0, 130)))).isoformat()
        if e["name"] == RELEVEL_EMPLOYER:
            for c, lv in zip(codes, K.LEVELS):
                rows.append((e["name"], c, lv, since, (RELEVEL_DATE - dt.timedelta(days=1)).isoformat()))
            for c, lv in zip(["L2", "L3", "L4", "L5"], K.LEVELS):
                rows.append((e["name"], c, lv, RELEVEL_DATE.isoformat(), ""))
            rows.append((e["name"], "L6", "out of scope", RELEVEL_DATE.isoformat(), ""))
        else:
            below, above = OUT_OF_SCOPE[e["scheme"]]
            if below and rx.random() < 0.22:
                rows.append((e["name"], below, "out of scope", since, ""))
            for c, lv in zip(codes, K.LEVELS):
                rows.append((e["name"], c, lv, since, ""))
            if rx.random() < 0.41:
                rows.append((e["name"], above, "out of scope", since, ""))
    return pd.DataFrame(rows, columns=["employer", "level_code", "tarnwick_level", "effective_from", "effective_to"])


def offers(emps):
    """Tallyband's offers extract: what new hires were offered, by family and level (a distractor)."""
    r = K.stream("offers")
    n = 5163
    sizes = np.array([e["size"] for e in emps])
    fam_p = np.array([f[1] for f in K.FAMILIES])
    rows, parts = [], []
    re_ = K.stream("offers_employer")
    for i in range(n):
        r.choice(len(emps), p=sizes / sizes.sum())
        fam = K.FAMILIES[int(r.choice(len(K.FAMILIES), p=fam_p / fam_p.sum()))][0]
        li = int(r.choice(4, p=(0.25, 0.32, 0.28, 0.15)))
        d = K.EXTRACT_FROM + dt.timedelta(days=int(r.integers(0, (K.BENCHMARK - K.EXTRACT_FROM).days)))
        ek = int(re_.choice(len(emps), p=employer_weights(emps, d)))
        e = emps[ek]
        c, t = code_for(e, li, d)
        st = STATES[int(r.choice(len(STATES), p=np.array([s[1] for s in STATES]) / sum(s[1] for s in STATES)))]
        noise = 0.08 * r.normal()
        rows.append(["OF-%s" % K.hexid("offer", i, n=10).upper(), e["name"], _title(fam, "data pipelines and platforms"
                     if fam == "Data Engineering" else "", li, r), fam, c, t, st[0], d.isoformat(), 0])
        parts.append((ek, fam, li, K.years_to_benchmark(d), st[2] + e["premium"], noise))
    ek_, fam_, li_, age_, eff_, u_ = (np.array(x) for x in zip(*parts))
    u_ = _flat_within(u_, age_, ek_, np.array(["%s|%d" % x for x in zip(fam_, li_)]))
    for row, li, a, ef, u in zip(rows, li_, age_, eff_, u_):
        pay = K.MARKET_MEDIAN[K.LEVELS[int(li)]] * 1.06 * np.exp(-K.MOVEMENT * a + ef + u)
        row[-1] = int(round(pay / 500.0) * 500)
    rows = [tuple(x) for x in rows]
    return pd.DataFrame(rows, columns=["offer_id", "employer", "title", "family", "level_code", "tallyband_level",
                                       "state", "offered_on", "base_offered_usd"])


def oews():
    """OEWS-style annual wages for database architects (SOC 15-1243) by state, May 2025 (a distractor)."""
    r = K.stream("oews")
    rows = [("U.S.", "00", 64_850, 141_900)]
    for code, share, eff in STATES:
        rows.append((code, "%02d" % int(r.integers(1, 57)), int(round(64_850 * share * r.uniform(0.85, 1.15), -1)),
                     141_900 * np.exp(eff + r.normal(0, 0.02))))
    out = []
    for area, fips, emp, med in rows:
        out.append((area, "15-1243", "Database Architects", emp, int(round(med * 1.04, -1)),
                    int(round(med * 0.68, -1)), int(round(med * 0.82, -1)), int(round(med, -1)),
                    int(round(med * 1.22, -1)), int(round(med * 1.45, -1))))
    return pd.DataFrame(out, columns=["area", "occ_code", "occ_title", "tot_emp", "a_mean", "a_pct10", "a_pct25",
                                      "a_median", "a_pct75", "a_pct90"])


# Tarnwick's work locations and their pay zones: the map in force from 2019 and the map from 1 July 2026
CITIES = [("San Francisco", 1, 1), ("Seattle", 1, 1), ("New York", 1, 1), ("Boston", 1, 1), ("Los Angeles", 2, 1),
          ("Washington", 2, 1), ("Denver", 2, 1), ("Austin", 2, 2), ("Chicago", 2, 2), ("Portland", 2, 3),
          ("Atlanta", 3, 2), ("Raleigh", 3, 2), ("Salt Lake City", 3, 3), ("Minneapolis", 3, 3), ("Phoenix", 3, 3),
          ("Columbus", 3, 3), ("Pittsburgh", 3, 3)]
CITY_WEIGHT = np.array([4, 3, 3, 2, 3, 3, 3, 2, 2, 2, 3, 2, 1, 1, 1, 1, 1], float)
ZONES_FROM = dt.date(2019, 1, 1)
ZONE_SWITCH = dt.date(2026, 7, 1)
ZMAP = {c: (a, b) for c, a, b in CITIES}
JOB_FAMILIES = {"DE": ("Data Engineer", 4), "MLE": ("Machine Learning Engineer", 4), "AE": ("Analytics Engineer", 3)}
ROMAN = ("I", "II", "III", "IV")
ENTERED_TO = dt.date(2026, 11, 16)           # changes entered ahead reach this far past the export


def zone(city, on):
    old, new = ZMAP[city]
    return new if on >= ZONE_SWITCH else old


def pay_zones():
    rows = []
    for c, a, b in CITIES:
        if a == b:
            rows.append((c, a, ZONES_FROM.isoformat(), ""))
        else:
            rows.append((c, a, ZONES_FROM.isoformat(), (ZONE_SWITCH - dt.timedelta(days=1)).isoformat()))
            rows.append((c, b, ZONE_SWITCH.isoformat(), ""))
    return pd.DataFrame(rows, columns=["work_location", "pay_zone", "effective_from", "effective_to"])


def _cycles():
    """Promotion cycles: the first Monday of May and of November."""
    out = []
    for y in range(2019, 2027):
        for m in (5, 11):
            d = dt.date(y, m, 1)
            out.append(d + dt.timedelta(days=(7 - d.weekday()) % 7))
    return out


def _off_benchmark(d):
    return d + dt.timedelta(days=1) if d == K.BENCHMARK else d


def hris():
    """Tarnwick's HRIS job history for its data, machine-learning and analytics engineers: one row per job record
    (hire, promotion, transfer, leave, return, termination), each a full copy of the job as it stood from its
    effective date, with the pay zone recorded on it; changes already agreed are entered ahead. Returns the rows and,
    for each worker, the job held on the benchmark date (the world's own answer)."""
    r = K.stream("hris")
    cycles = _cycles()
    rows, truth = [], []
    pid = {"employee": 10000, "contingent": 70000}
    plan = [("DE", 262, "employee"), ("MLE", 84, "employee"), ("AE", 52, "employee"), ("DE", 30, "contingent")]
    for fam, count, wtype in plan:
        nlev = JOB_FAMILIES[fam][1]
        for _ in range(count):
            pid[wtype] += int(r.integers(1, 9))
            eid = ("E%05d" if wtype == "employee" else "C%05d") % pid[wtype]
            lo = dt.date(2019, 1, 7) if wtype == "employee" else dt.date(2024, 3, 4)
            hire = _off_benchmark(lo + dt.timedelta(days=int(r.integers(0, (dt.date(2026, 9, 28) - lo).days))))
            p_start = (0.40, 0.32, 0.21, 0.07)[:nlev]
            li = int(r.choice(nlev, p=np.array(p_start) / sum(p_start)))
            city = CITIES[int(r.choice(len(CITIES), p=CITY_WEIGHT / CITY_WEIGHT.sum()))][0]
            ev = [(hire, 0, "hire", li, city, "active")]
            if wtype == "employee":
                since, lv = hire, li
                for cd in cycles:
                    if cd <= since or lv >= nlev - 1 or (cd - since).days < 540:
                        continue
                    if r.random() < (0.30, 0.21, 0.09)[lv]:
                        lv += 1
                        since = cd
                        ev.append((cd, 2, "promotion", lv, None, None))
                if r.random() < 0.13:
                    td = hire + dt.timedelta(days=int(r.integers(120, 2600)))
                    c2 = CITIES[int(r.choice(len(CITIES), p=CITY_WEIGHT / CITY_WEIGHT.sum()))][0]
                    if c2 != city:
                        ev.append((_off_benchmark(td), 1, "transfer", None, c2, None))
                if r.random() < 0.05:
                    ls = hire + dt.timedelta(days=int(r.integers(200, 2400)))
                    ev.append((_off_benchmark(ls), 3, "leave_start", None, None, "leave"))
                    ev.append((_off_benchmark(ls + dt.timedelta(days=int(r.integers(40, 200)))), 4, "leave_end", None,
                               None, "active"))
                if r.random() < 0.075:
                    ls = dt.date(2026, 5, 18) + dt.timedelta(days=int(r.integers(0, 128)))
                    ev.append((_off_benchmark(ls), 3, "leave_start", None, None, "leave"))
                    if r.random() < 0.55:
                        ev.append((_off_benchmark(ls + dt.timedelta(days=int(r.integers(50, 170)))), 4, "leave_end",
                                   None, None, "active"))
                term = hire + dt.timedelta(days=int(r.exponential(2700)))
            else:
                term = hire + dt.timedelta(days=int(r.integers(120, 720)))
            ev.append((_off_benchmark(term), 5, "termination", None, None, "terminated"))
            ev.sort(key=lambda e: (e[0], e[1]))
            cur = dict(level=li, city=city, status="active")
            out = []
            for ed, _, act, lv2, c2, st in ev:
                if ed > ENTERED_TO:
                    break
                if cur["status"] == "terminated":
                    break
                if act == "leave_end" and cur["status"] != "leave":
                    continue
                if act == "leave_start" and cur["status"] == "leave":
                    continue
                if lv2 is not None:
                    cur["level"] = lv2
                if c2 is not None:
                    cur["city"] = c2
                if st is not None:
                    cur["status"] = st
                out.append((ed, act, cur["level"], cur["city"], cur["status"]))
            for ed, act, lv2, c2, st in out:
                rows.append((eid, ed, act, "%s%d" % (fam, lv2 + 1), "%s %s" % (JOB_FAMILIES[fam][0], ROMAN[lv2]), c2,
                             zone(c2, ed), st, wtype))
            on = [o for o in out if o[0] <= K.BENCHMARK]
            if on and on[-1][4] in ("active", "leave"):
                truth.append((eid, fam, wtype, ROMAN[on[-1][2]], on[-1][3], zone(on[-1][3], K.BENCHMARK),
                              zone(on[-1][3], on[-1][0]), on[-1][4]))
    df = pd.DataFrame(rows, columns=["employee_id", "effective_date", "action", "job_code", "job_title",
                                     "work_location", "pay_zone", "status", "worker_type"])
    order = {"hire": 0, "transfer": 1, "promotion": 2, "leave_start": 3, "leave_end": 4, "termination": 5}
    df["_o"] = df.action.map(order)
    df = df.sort_values(["employee_id", "effective_date", "_o"], kind="mergesort").drop(columns="_o")
    return df.reset_index(drop=True), pd.DataFrame(truth, columns=["employee_id", "family", "worker_type", "level",
                                                                   "work_location", "zone", "zone_recorded", "status"])


def ats():
    """Tarnwick's ATS requisitions at posting grain: each requisition once per city it is posted in, with the date it
    opened, the date a hire closed it, and its status as of the export with the date that status took effect.
    Returns the rows and the requisitions open on the benchmark date (the world's own answer)."""
    r = K.stream("ats")
    rows, truth = [], []
    rid = 0
    lo, hi = dt.date(2025, 6, 2), dt.date(2026, 10, 12)
    for fam, count in (("DE", 86), ("MLE", 32), ("AE", 19)):
        nlev = JOB_FAMILIES[fam][1]
        for _ in range(count):
            rid += int(r.integers(1, 6))
            req = "R-%05d" % (31000 + rid)
            opened = _off_benchmark(lo + dt.timedelta(days=int(r.integers(0, (hi - lo).days))))
            p = (0.22, 0.34, 0.30, 0.14)[:nlev]
            li = int(r.choice(nlev, p=np.array(p) / sum(p)))
            end = _off_benchmark(opened + dt.timedelta(days=int(r.integers(25, 170))))
            outcome = "filled" if r.random() < 0.79 else "cancelled"
            if end > K.HR_EXPORT:
                closed, status, sdate = None, "open", opened
            elif outcome == "filled":
                closed, status, sdate = end, "filled", end
            else:
                closed, status, sdate = None, "cancelled", end
            k = int(r.choice(4, p=(0.45, 0.30, 0.17, 0.08))) + 1
            cities = r.choice(len(CITIES), k, replace=False)
            for j, c in enumerate(cities):
                rows.append((req, "%s-%d" % (req, j + 1), "%s%d" % (fam, li + 1), "%s %s" % (JOB_FAMILIES[fam][0],
                             ROMAN[li]), CITIES[c][0], opened, closed, status, sdate))
            truth.append((req, fam, ROMAN[li], opened, end if status != "open" else None, status, closed))
    df = pd.DataFrame(rows, columns=["requisition_id", "posting_id", "job_code", "job_title", "posting_city",
                                     "opened_on", "closed_on", "status", "status_date"])
    tr = pd.DataFrame(truth, columns=["requisition_id", "family", "level", "opened_on", "ended_on", "status",
                                      "closed_on"])
    return df, tr


def build():
    tb, emps = tallyband()
    hr, hr_truth = hris()
    req, req_truth = ats()
    return dict(tb=tb, emps=emps, crosswalk=crosswalk(emps), offers=offers(emps), oews=oews(), hris=hr,
                hris_truth=hr_truth, ats=req, ats_truth=req_truth, zones=pay_zones())
