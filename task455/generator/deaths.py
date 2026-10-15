"""The deaths behind the state's file: residents' drug overdose deaths by the medical examiner's drug class, certified
by the coroner's practice (every drug toxicology reports is listed; one certificate in eight names no drug), each
death's registered versions (a cause pending investigation amended when toxicology returns, later corrections, a
duplicate registration voided), out-of-state deaths received through the interstate exchange, and the all-cause
deaths around them."""
import datetime as dt
import math

import numpy as np

import world as W

D = dt.date
DAY = dt.timedelta(days=1)

OPIOIDS = {"fentanyl": "T40.4", "heroin": "T40.1", "oxycodone": "T40.2", "hydrocodone": "T40.2", "morphine": "T40.2",
           "methadone": "T40.3", "tramadol": "T40.4", "opioid, unspecified": "T40.6"}
STIMULANTS = {"methamphetamine": "T43.6", "amphetamine": "T43.6", "cocaine": "T40.5"}
OTHERS = {"alprazolam": "T42.4", "clonazepam": "T42.4", "diazepam": "T42.4", "gabapentin": "T42.6",
          "sertraline": "T43.2", "bupropion": "T43.2", "amitriptyline": "T43.0", "quetiapine": "T43.5",
          "diphenhydramine": "T45.0", "acetaminophen": "T39.1", "zolpidem": "T42.6", "trazodone": "T43.2",
          "ethanol": "T51.0", "delta-9-THC": "T40.7"}
CODE = {**OPIOIDS, **STIMULANTS, **OTHERS}
OPIOID_CODES = ("T40.0", "T40.1", "T40.2", "T40.3", "T40.4", "T40.6")
STIM_CODES = ("T40.5", "T43.6")


def rng(*keys):
    return np.random.default_rng([W.SEED] + [k if isinstance(k, int) else sum(ord(c) * (i + 1) for i, c in enumerate(k))
                                             for k in keys])


def xcat(code):
    """The X40-X44 group a drug code points the underlying cause to (ethanol does not)."""
    if code.startswith("T39"):
        return 0
    if code.startswith(("T42", "T43")):
        return 1
    if code.startswith("T40"):
        return 2
    if code.startswith("T44"):
        return 3
    if code.startswith("T51"):
        return None
    return 4


def underlying(intent, codes):
    cats = {xcat(c) for c in codes} - {None}
    k = cats.pop() if len(cats) == 1 else 4
    return {"Accident": "X4%d" % k, "Suicide": "X6%d" % k, "Could not be determined": "Y1%d" % k,
            "Homicide": "X85"}[intent]


def legacy(code):
    return code.replace(".", "")


# ---------------------------------------------------------------- the classes and their certificates

def cells_2025(cls):
    """2025's deaths of each class by (sex, band), each cell a whole multiple of eight."""
    n = W.CLASS_N[cls][2025]
    assert n % 8 == 0, (cls, n)
    units = n // 8
    cells = {k: 1 for k in W.PROFILE[cls]}          # every cell holds at least eight deaths of every class
    rest = _largest_remainder(units - len(cells), W.PROFILE[cls], 1)
    return {k: 8 * (cells[k] + rest[k]) for k in cells}


def _largest_remainder(n, profile, unit, scale=1):
    keys = sorted(profile)
    raw = {k: n * profile[k] for k in keys}
    base = {k: int(math.floor(raw[k])) for k in keys}
    left = n - sum(base.values())
    for k in sorted(keys, key=lambda k: (-(raw[k] - base[k]), k))[:left]:
        base[k] += 1
    return {k: v * scale for k, v in base.items()}


def _cells(cls, year):
    if year == 2025:
        return cells_2025(cls)
    return _largest_remainder(W.CLASS_N[cls][year], W.PROFILE[cls], 1)


def _pattern(cls):
    """The coroner's certificate categories in the order a run of eight deaths takes them."""
    r = W.RATE[cls]
    if cls == "O":
        return ["OL", "OL", "OL", "N", "OL", "OL", "OL", "OL"]
    if cls == "S":
        return ["OL", "SO", "OL", "N", "SO", "OL", "SO", "OL"]
    assert r["N"] == 8
    return ["N"] * 8


def _age(g, band):
    lo, hi = W.BANDS[band]
    if band == 3:
        return int(min(hi, lo + g.gamma(2.0, 5.5)))
    return int(g.integers(lo if lo > 15 else 18, hi + 1))


def _dod(g, year):
    doy = int(g.integers(0, 365 + (1 if year % 4 == 0 else 0)))
    return D(year, 1, 1) + doy * DAY


STIM_PATTERN = [1, 0, 1, 1, 0, 1, 0]       # an opioid death certified with an opioid lists a stimulant four times in seven
NODRUG_R = [0, 0, 0, 1, 0, 0, 0, 0]        # another drug death's certificate names no drug one time in eight


def overdose_deaths():
    """Every resident drug overdose death on the file at the extract (2025: at its close, the reviewed set), with
    its class, demographics, the drugs the medical examiner found and the coroner's certificate category. In 2025
    every (sex, age band) cell holds each class's rates exactly; in other years the categories run in a pattern over
    the class's deaths in date order, so every year's split stays within a death of the rates."""
    out = []
    for year in W.YEARS:
        for cls in ("O", "S", "R"):
            cells = _cells(cls, year)
            g = rng("od", year, cls)
            seq = 0
            members_by_cell = []
            for (sex, band) in sorted(cells):
                cell = []
                for i in range(cells[(sex, band)]):
                    d = {"year": year, "cls": cls, "sex": sex, "band": band, "age": _age(g, band),
                         "dod": _dod(g, year), "key": (year, cls, seq)}
                    seq += 1
                    cell.append(d)
                    out.append(d)
                members_by_cell.append(cell)
            groups = members_by_cell if year == 2025 else [sorted(sum(members_by_cell, []), key=lambda d: (d["dod"], d["key"]))]
            pat = _pattern(cls)
            for grp in groups:
                off = 0 if year == 2025 else int(g.integers(0, 8))
                for i, d in enumerate(grp):
                    d["cat"] = pat[(i + off) % 8]
                    d["nodrug"] = (d["cat"] == "N") if cls != "R" else bool(NODRUG_R[(i + off) % 8])
                ol = [d for d in grp if d["cat"] == "OL" and cls == "O"]
                off2 = 0 if year == 2025 else int(g.integers(0, 7))
                for j, d in enumerate(ol):
                    d["stim_listed"] = bool(STIM_PATTERN[(j + off2) % 7])
    g = rng("drugs")
    for d in out:
        _drugs(d, g)
    return out


def _drugs(d, g):
    cls, cat = d["cls"], d["cat"]
    contrib, present = [], []
    if cls == "O":
        r = g.random()
        main = "fentanyl" if r < .82 else ("heroin" if r < .88 else ("oxycodone" if r < .92 else ("methadone" if r < .96 else "hydrocodone")))
        contrib.append(main)
        if main == "fentanyl" and g.random() < .07:
            contrib.append("heroin")
        if d.get("stim_listed") or (cat == "N" and g.random() < W.POLY):
            stim = "methamphetamine" if g.random() < .74 else "cocaine"
            if d.get("stim_listed") and g.random() < .14:
                present.append("amphetamine" if stim == "methamphetamine" else stim)
            else:
                contrib.append(stim)
        if g.random() < .09:
            contrib.append(["alprazolam", "clonazepam", "gabapentin"][int(g.integers(0, 3))])
        if g.random() < .10:
            contrib.append("ethanol")
        if g.random() < .18:
            present.append("delta-9-THC")
    elif cls == "S":
        contrib.append("methamphetamine" if g.random() < .78 else "cocaine")
        if g.random() < .05:
            contrib.append("cocaine" if contrib[0] == "methamphetamine" else "methamphetamine")
        if g.random() < .06:
            contrib.append("ethanol")
        if cat == "OL":
            present.append("fentanyl")
        if g.random() < .16:
            present.append("delta-9-THC")
        if g.random() < .05:
            present.append("gabapentin")
    else:
        pool = ["alprazolam", "sertraline", "bupropion", "amitriptyline", "quetiapine", "diphenhydramine",
                "acetaminophen", "gabapentin", "zolpidem", "trazodone", "clonazepam", "diazepam"]
        k = 1 + (g.random() < .45) + (g.random() < .15)
        picks = list(dict.fromkeys(pool[int(g.integers(0, len(pool)))] for _ in range(k)))
        contrib.extend(picks)
        if g.random() < .22:
            contrib.append("ethanol")
        if g.random() < .08:
            present.append("delta-9-THC")
    d["contrib"], d["present"] = contrib, present
    # what the certificate lists: every drug the laboratory reported, unless it names no drug
    listed = [] if d["nodrug"] else list(dict.fromkeys(contrib + present))
    d["listed"] = listed
    u = g.random()
    d["intent"] = "Accident" if u < .905 else ("Suicide" if u < .955 else ("Could not be determined" if u < .992 else "Homicide"))
    if cls == "R" and g.random() < .25:
        d["intent"] = "Suicide"
    codes = [CODE[x] for x in listed] or ["T50.9"]
    d["ucod"] = underlying(d["intent"], [c for c in codes if c != "T51.0"] or ["T50.9"])
    extra = []
    if cls == "O" and g.random() < .22:
        extra.append("F11.2")
    if cls == "S" and d["age"] >= 50 and g.random() < .35:
        extra.append("I25.1")
    if cls == "S" and g.random() < .12:
        extra.append("F15.2")
    if "T50.9" not in codes and g.random() < .04:
        codes.append("T50.9")
    d["axis"] = [d["ucod"]] + list(dict.fromkeys(codes)) + extra


def certificate_category(axis):
    """OL an opioid listed, SO a stimulant and no opioid, N neither; codes with or without the decimal point."""
    cs = {c if "." in c or len(c) < 4 else c[:3] + "." + c[3:] for c in axis}
    if any(c.startswith(OPIOID_CODES) for c in cs):
        return "OL"
    if any(c.startswith(STIM_CODES) for c in cs):
        return "SO"
    return "N"


# ---------------------------------------------------------------- where each death happened and its registered versions

MARITAL = ["Never married", "Married", "Divorced", "Widowed", "Separated"]
EDUCATION = ["8th grade or less", "9th-12th grade, no diploma", "High school graduate or GED", "Some college, no degree",
             "Associate degree", "Bachelor's degree", "Master's degree", "Doctorate or professional degree"]
PLACES_OD = [("Decedent's home", .52), ("Other", .21), ("Hospital, inpatient", .07), ("Hospital, ER/outpatient", .12),
             ("Hospital, dead on arrival", .04), ("Other person's residence", .04)]
PLACES_NAT = [("Hospital, inpatient", .33), ("Decedent's home", .31), ("Nursing home/long term care", .17),
              ("Hospice facility", .08), ("Hospital, ER/outpatient", .06), ("Other", .05)]
COUNTY_CODE = dict(W.OTHER_COUNTIES + [(W.COUNTY, W.COUNTY_CODE)])


def _pick(g, pairs):
    r, acc = g.random(), 0.0
    for v, p in pairs:
        acc += p
        if r < acc:
            return v
    return pairs[-1][0]


def _lag(g, median, sigma, lo, hi):
    return int(min(hi, max(lo, round(median * math.exp(sigma * g.standard_normal())))))


MARITAL_BY_AGE = [(18, [1, 0, 0, 0, 0]), (25, [.86, .11, .02, 0, .01]), (35, [.52, .33, .11, .01, .03]),
                  (45, [.32, .38, .23, .02, .05]), (55, [.24, .40, .28, .04, .04]), (65, [.18, .44, .27, .08, .03]),
                  (75, [.10, .48, .20, .20, .02]), (200, [.06, .36, .12, .45, .01])]


def _marital_for(a, u):
    shares = next(p for top, p in MARITAL_BY_AGE if a < top)
    acc = 0.0
    for m, p in zip(MARITAL, shares):
        acc += p
        if u < acc:
            return m
    return MARITAL[int(np.argmax(shares))]


def _education_for(a, z):
    if a < 15:
        return EDUCATION[0]
    if a < 18:
        return EDUCATION[1]
    k = min(7, max(0, int(round(2.6 + 1.3 * z))))
    return EDUCATION[min(k, 3 if a < 22 else (5 if a < 25 else 7))]


def demographics(d, g):
    a = d["age"]
    if not (a < 28 and g.random() < .8):          # the place stream's draws, so its later draws keep their order
        g.integers(0, 5)
    g.normal(2.6, 1.3)
    h = rng("demog", *d["key"])
    d["marital"] = _marital_for(a, h.random())
    d["education"] = _education_for(a, h.standard_normal())


def place(d, g, kind=None, natural=False):
    d["place_kind"] = kind or _pick(g, list(W.PLACE.items()))
    d.setdefault("res_county", W.COUNTY)
    d.setdefault("res_state", "")
    if d["place_kind"] == "county":
        d["occ_county"], d["occ_state"] = W.COUNTY, ""
        d["certifier"] = "Physician" if natural and g.random() < .86 else "Coroner"
    elif d["place_kind"] == "state":
        d["occ_county"], d["occ_state"] = W.NEAR[int(g.integers(0, len(W.NEAR)))], ""
        d["certifier"] = "Physician" if natural and g.random() < .86 else ("Coroner" if g.random() < .6 else "Medical examiner")
    else:
        d["occ_county"], d["occ_state"] = "", W.OUT_STATES[int(g.integers(0, len(W.OUT_STATES)))]
        d["certifier"] = "Physician" if natural and g.random() < .86 else "Medical examiner"
    d["place"] = _pick(g, PLACES_NAT if natural else PLACES_OD)
    demographics(d, g)


def fields(d, **kw):
    f = {"ucod": d["ucod"], "axis": list(d["axis"]), "manner": d["manner"], "res_county": d["res_county"],
         "res_state": d["res_state"], "marital": d["marital"], "education": d["education"]}
    f.update(kw)
    return f


def versions(d, g, pending=False, delay=None, lag0=None, extra_amend=.08):
    """The death's registered versions, [registered, fields] (out-of-state deaths: [registered, fields, received])."""
    reg0 = d["dod"] + int(g.integers(3, 12)) * DAY
    if pending:
        amend = max(d["dod"] + (delay if delay is not None else _lag(g, 80, .5, 25, 430)) * DAY, reg0 + 9 * DAY)
        vs = [[reg0, fields(d, ucod="R99", axis=["R99"], manner="Pending investigation")], [amend, fields(d)]]
    else:
        vs = [[reg0, fields(d)]]
    if g.random() < extra_amend:
        last = vs[-1][0] + int(g.integers(40, 520)) * DAY
        if last < W.EXTRACT - 25 * DAY:
            if g.random() < .45:
                k = int(g.integers(0, 5))
                fix = {"marital": _marital_for(d["age"], (k + .5) / 5)}
            else:
                k = int(g.integers(0, 8))
                fix = {"education": _education_for(d["age"], (k - 2.6) / 1.3)}
            vs.append([last, dict(vs[-1][1], **fix)])
    if d["place_kind"] == "out":
        for i, v in enumerate(vs):
            lag = lag0 if (i == 0 and lag0 is not None) else _lag(g, 40, 1.0, 6, 420)
            v.append(v[0] + lag * DAY)
        for i in range(1, len(vs)):
            if vs[i][2] <= vs[i - 1][2]:
                vs[i][2] = vs[i - 1][2] + int(g.integers(1, 9)) * DAY
    return vs


def _manner(d):
    d["manner"] = d["intent"]


NATURAL = [("I25.1", 7.6), ("I21.9", 2.9), ("I50.9", 2.6), ("I11.9", 2.1), ("I48.9", 1.0), ("I63.9", 3.1), ("I64", 1.4),
           ("I71.9", .4), ("I26.9", .6), ("I42.9", .6), ("C34.9", 5.1), ("C18.9", 1.8), ("C50.9", 1.5), ("C61", 1.2),
           ("C25.9", 1.6), ("C22.0", .8), ("C71.9", .5), ("C80.9", 1.0), ("C16.9", .5), ("C67.9", .5), ("C64", .5),
           ("C56", .5), ("C90.0", .4), ("C85.9", .6), ("C91.1", .4), ("J44.9", 4.1), ("J44.1", 1.0), ("J18.9", 2.0),
           ("J69.0", .5), ("J84.1", .6), ("G30.9", 4.0), ("F03", 2.5), ("G20", 1.0), ("G12.2", .2), ("G35", .1),
           ("E11.9", 2.6), ("E14.9", .5), ("N18.9", 1.6), ("N17.9", .3), ("K70.3", 1.0), ("K74.6", .8), ("A41.9", 1.8),
           ("V89.2", 1.2), ("W19", 1.4), ("W18", .3), ("X70", .5), ("X74", .9), ("X95", .5), ("W69", .1), ("F10.2", .4),
           ("X45", .1), ("B20", .1), ("D69.6", .1), ("K92.2", .3), ("R54", .3)]
OLD_AGE = {"G30.9": 60, "F03": 60, "G20": 55, "R54": 80, "I25.1": 35, "I21.9": 35, "I50.9": 40, "I11.9": 35, "I48.9": 45,
           "I63.9": 35, "I64": 40, "I71.9": 50, "J44.9": 40, "J44.1": 40, "J84.1": 45, "E11.9": 30, "E14.9": 30,
           "N18.9": 30, "C61": 45, "C34.9": 35, "C18.9": 30, "C25.9": 35, "C22.0": 30, "C16.9": 30, "C67.9": 40,
           "C64": 30, "C56": 30, "C90.0": 40, "C50.9": 25, "K70.3": 25, "K74.6": 25, "F10.2": 25, "J69.0": 50,
           "G12.2": 30, "G35": 20, "D69.6": 20, "K92.2": 30, "A41.9": 18, "J18.9": 18, "I26.9": 18, "I42.9": 18}
CHILD = [("V89.2", 3.0), ("W69", 1.5), ("C71.9", 1.0), ("C91.0", 1.0), ("Q24.9", 1.0), ("G40.9", 1.0), ("X70", 1.0),
         ("X95", .8), ("J18.9", .5), ("G80.9", .7), ("W75", .4), ("R95", .4)]
YOUNG = [("V89.2", 4.0), ("X74", 2.5), ("X70", 2.0), ("X95", 2.0), ("K70.3", 1.0), ("C50.9", 1.0), ("I25.1", .8),
         ("E10.9", .5), ("G40.9", .6), ("W19", .4), ("A41.9", .5), ("B20", .3), ("I42.9", .5), ("C18.9", .5),
         ("W69", .4), ("I21.9", .4), ("C71.9", .4), ("J18.9", .4)]
CONTRIB_FROM = {"I10": 25, "E11.9": 30, "J44.9": 40, "N18.9": 30, "F17.2": 16, "I48.9": 45, "E78.5": 30, "F03": 60,
                "J96.0": 0, "I50.9": 40, "E66.9": 12, "I25.1": 35}
COVID = {2019: 0, 2020: .085, 2021: .11, 2022: .042, 2023: .012, 2024: .005, 2025: .004, 2026: .003}
CONTRIB = ["I10", "E11.9", "J44.9", "N18.9", "F17.2", "I48.9", "E78.5", "F03", "J96.0", "I50.9", "E66.9", "I25.1"]
INJURY = ("V", "W", "X7", "X9")


def _natural_death(d, g, year):
    a = d["age"]
    if g.random() < COVID[year] * (.02 if a < 18 else (.2 if a < 45 else 1)):
        u = "U07.1"
    else:
        pool = CHILD if a < 18 else (YOUNG if a < 35 else [(c, w) for c, w in NATURAL if OLD_AGE.get(c, 0) <= a])
        codes, wts = zip(*pool)
        u = codes[int(np.searchsorted(np.cumsum(wts) / sum(wts), g.random()))]
    drawn = [CONTRIB[int(g.integers(0, len(CONTRIB)))] for _ in range(int(g.integers(0, 4)))]
    axis = [u] + ([c for c in drawn if CONTRIB_FROM.get(c, 0) <= a] if a >= 18 else [])
    if u == "U07.1":
        axis.insert(1, "J12.8")
    d["ucod"], d["axis"] = u, list(dict.fromkeys(axis))
    d["manner"] = ("Accident" if u.startswith(("V", "W", "X45")) else "Suicide" if u.startswith("X7")
                   else "Homicide" if u.startswith("X9") else "Natural")
    d["cls"] = None
    d["cat"] = None


def _age_natural(g):
    if g.random() < .9:
        return int(min(104, max(18, round(101 - g.gamma(3.0, 7.5)))))
    return int(round(60 * (g.uniform(0, 60) / 60) ** .55))


def _cap_to(d, day):
    """Keep only versions registered (and, out of state, received) on or before day."""
    keep = [v for v in d["vs"] if v[0] <= day and (len(v) < 3 or v[2] <= day)]
    d["vs"] = keep


def records():
    """Every death record in the extract's frame with its versions. Returns (recs, final): final lists the residents'
    drug overdose deaths on the file at the extract (2025: on the file at its close, the reviewed set)."""
    final = overdose_deaths()
    recs = []
    g = rng("place")
    for d in final:
        _manner(d)
        place(d, g)
    for year in W.YEARS:
        close = W.CLOSE[year]
        ds = sorted([d for d in final if d["year"] == year], key=lambda d: (d["dod"], d["key"]))
        gy = rng("versions", year)
        for d in ds:
            pend = d["cat"] != "N" and gy.random() < (.72 if d["place_kind"] != "out" else .25)
            delay, lag0 = None, None
            if year == 2025:                 # on the file, in its final form, by the close
                room = (close - d["dod"]).days - 6
                delay = min(_lag(gy, 80, .5, 25, 430), room)
                if d["place_kind"] == "out":
                    pend, lag0 = False, min(_lag(gy, 40, 1.0, 6, 420), room - 30)
            if year == 2026:                 # on the file, in its final form, by the extract
                room = (W.EXTRACT - d["dod"]).days - 4
                delay = min(_lag(gy, 80, .5, 25, 430), room)
                if d["place_kind"] == "out":
                    lag0 = min(_lag(gy, 40, 1.0, 6, 420), room - 20)
            d["pending"] = pend
            d["vs"] = versions(d, gy, pending=pend, delay=delay, lag0=lag0, extra_amend=.08)
            if d["place_kind"] == "out" and year in (2025, 2026):
                lim = close - 3 * DAY if year == 2025 else W.EXTRACT - 2 * DAY
                for v in d["vs"]:
                    v[2] = min(v[2], lim)
            recs.append(d)
        # the device behind the close-date counts: each year has at least one out-of-state death delivered after
        # the close; the exchange is slow for a death late in the year
        if year <= 2024:
            outs = [d for d in ds if d["place_kind"] == "out"]
            late = [d for d in outs if d["vs"][0][2] > close]
            if not late:
                d = max(outs, key=lambda d: (d["dod"], d["key"]))
                d["vs"][0][2] = close + int(gy.integers(9, 75)) * DAY
                for i in range(1, len(d["vs"])):
                    d["vs"][i][2] = max(d["vs"][i][2], d["vs"][i - 1][2] + int(gy.integers(1, 9)) * DAY)
            pend_late = [d for d in ds if d["pending"] and d["vs"][1][0] > close]
            if not pend_late:
                d = max([d for d in ds if d["pending"] and d["place_kind"] == "county"], key=lambda d: (d["dod"], d["key"]))
                d["vs"] = d["vs"][:2]
                d["vs"][1][0] = close + int(gy.integers(4, 40)) * DAY
    _check_final_order(final)
    recs += _resent(final)
    recs += _moved_in(final)
    recs += _added_2025(final)
    recs += _losses()
    recs += _pending_at_extract()
    recs += _nonresident_overdoses()
    recs += _duplicates(final)
    recs += _all_cause(final)
    closes = set(W.CLOSE.values())
    for d in recs:
        for v in d["vs"]:
            for k in ((0, 2) if len(v) > 2 else (0,)):
                if v[k] in closes:
                    v[k] = v[k] + DAY
    return recs, final


def _check_final_order(final):
    for d in final:
        vs = d["vs"]
        assert all(vs[i][0] <= vs[i + 1][0] for i in range(len(vs) - 1)), d["key"]


SEND_FMT = {"CA": "{y}{n:07d}", "NV": "{yy}-{n:05d}", "AZ": "1{yy}{n:06d}", "CO": "{y}{n:06d}", "TX": "{yy}{n:07d}",
            "WA": "{y}{n:06d}", "UT": "{yy}-{n:06d}", "NM": "{y}-{n:06d}", "FL": "{y}{n:06d}", "OR": "{yy}-{n:05d}",
            "MT": "{y}-{n:05d}", "NE": "{y}{n:05d}"}
SEND_CAP = {"CA": 290000, "TX": 220000, "FL": 240000, "WA": 64000, "AZ": 70000, "CO": 45000, "OR": 41000, "NV": 30000,
            "UT": 21000, "NM": 21000, "MT": 11000, "NE": 18000}


def _send_no(d, bump=0):
    """The certificate number the sending state gave the death, in that state's own format."""
    h = rng("sendno", *d["key"])
    st = d["occ_state"]
    y = d["vs"][0][0].year
    n = 40 + (int(h.integers(0, SEND_CAP[st] - 40)) + 7 * bump) % (SEND_CAP[st] - 40)
    return SEND_FMT[st].format(y=y, yy=y % 100, n=n)


def _resent(final):
    """A resident's out-of-state death the sending state sent again as a new record some months after the year's
    close, the office voiding the first copy as a duplicate (one a year, 2019 to 2024). Both copies carry the
    sending state's certificate number."""
    g = rng("resent")
    out = []
    for year in range(2019, 2025):
        close = W.CLOSE[year]
        cands = sorted([d for d in final if d["year"] == year and d["place_kind"] == "out"
                        and all(v[0] < close - 20 * DAY and v[2] < close - 20 * DAY for v in d["vs"])],
                       key=lambda d: d["key"])
        d = cands[int(g.integers(0, len(cands)))]
        old = dict(d)
        old["key"] = (year, "resent", 0)
        sent = close + int(g.integers(25, 210)) * DAY
        void = sent + int(g.integers(9, 75)) * DAY
        last = d["vs"][-1][1]
        old["vs"] = [list(v) for v in d["vs"]] + [[void, dict(last, void=True)]]
        d["send_no"] = old["send_no"] = _send_no(d)
        d["vs"] = [[d["vs"][0][0], dict(last), sent]]
        d["resent"] = sent
        old["duplicate_of"] = d["key"]
        out.append(old)
    return out


def _moved_in(final):
    """A resident first recorded at a neighbouring county's address, the residence corrected later (the death is
    in the final set; one a year from 2019 to 2024, about half of the corrections after the close)."""
    g = rng("movedin")
    for year in range(2019, 2025):
        cands = sorted([d for d in final if d["year"] == year and d["place_kind"] == "state" and not d["pending"]],
                       key=lambda d: d["key"])
        d = cands[int(g.integers(0, len(cands)))]
        frm = W.NEAR[int(g.integers(0, len(W.NEAR)))]
        when = max(W.CLOSE[year] + int(g.integers(-120, 160)) * DAY, d["vs"][-1][0] + 15 * DAY)
        first = d["vs"][0]
        d["vs"] = [[v[0], dict(v[1], res_county=frm)] for v in d["vs"]] + [[when, dict(d["vs"][-1][1], res_county=W.COUNTY)]]
        d["vs"].sort(key=lambda v: v[0])
        d["moved_in"] = when
        del first
    return []


def _class_draw(g, year):
    n = {c: W.CLASS_N[c][year] for c in "OSR"}
    tot = sum(n.values())
    r = g.random() * tot
    return "O" if r < n["O"] else ("S" if r < n["O"] + n["S"] else "R")


def _cat_draw(g, cls):
    r = W.RATE[cls]
    u = g.random() * 8
    return "OL" if u < r["OL"] else ("SO" if u < r["OL"] + r["SO"] else "N")


def _new_overdose(g, year, key, cls=None, sex=None, band=None):
    cls = cls or _class_draw(g, year)
    prof = W.PROFILE[cls]
    sb = list(prof)
    sex, band = sb[int(np.searchsorted(np.cumsum([prof[k] for k in sb]), g.random()))] if sex is None else (sex, band)
    d = {"year": year, "cls": cls, "sex": sex, "band": band, "age": _age(g, band), "dod": _dod(g, year),
         "cat": _cat_draw(g, cls), "key": key}
    d["nodrug"] = d["cat"] == "N" if cls != "R" else g.random() < 1 / 8
    d["stim_listed"] = cls == "O" and d["cat"] == "OL" and g.random() < 4 / 7
    _drugs(d, g)
    _manner(d)
    return d


def _added_2025(final):
    """2025 deaths that became residents' overdose deaths on the file only after its close (none reviewed): a cause
    pending at the close and two out-of-state deaths the exchange delivered late."""
    g = rng("added2025")
    close = W.CLOSE[2025]
    out = []
    for i, kind in enumerate(["county", "county", "county", "out", "out", "state"]):
        d = _new_overdose(g, 2025, (2025, "add", i))
        d["dod"] = D(2025, 10, 1) + int(g.integers(0, 92)) * DAY
        place(d, g, kind)
        if kind == "out":
            d["vs"] = versions(d, g, pending=False, lag0=(close - d["dod"]).days + int(g.integers(10, 80)), extra_amend=0)
        else:
            if d["cat"] == "N":
                d["cat"] = "OL" if d["cls"] != "R" else "N"
                _drugs(d, g)
                _manner(d)
            d["vs"] = versions(d, g, pending=True, delay=(close - d["dod"]).days + int(g.integers(5, 120)), extra_amend=0)
        d["added_after_close"] = True
        out.append(d)
    return out


def _losses():
    """Overdose deaths the file counted as residents' at a year's close and no longer does: an address corrected to
    a neighbouring county, or a cause the medical examiner later found natural."""
    g = rng("losses")
    out = []
    kinds = {2019: ["moved", "cause"], 2020: ["moved"], 2021: ["moved", "cause"], 2022: ["moved", "cause"],
             2023: ["cause"], 2024: ["moved", "cause"]}
    for year in range(2019, 2025):
        close = W.CLOSE[year]
        for j, kind in enumerate(kinds[year]):
            d = _new_overdose(g, year, (year, "loss", j))
            d["dod"] = D(year, 1, 1) + int(g.integers(0, 330)) * DAY
            place(d, g, "county")
            d["vs"] = versions(d, g, pending=False, extra_amend=0)
            when = close + int(g.integers(12, 250)) * DAY
            if kind == "moved":
                to = W.NEAR[int(g.integers(0, len(W.NEAR)))]
                d["vs"].append([when, dict(d["vs"][-1][1], res_county=to)])
                d["res_county"] = to
            else:
                nat = "I11.9" if d["cls"] == "S" else "I25.1"
                d["vs"].append([when, dict(d["vs"][-1][1], ucod=nat, axis=[nat, "I10"] + [c for c in d["axis"][1:] if c.startswith("T")][:1],
                                           manner="Natural")])
            d["lost"] = kind
            out.append(d)
    return out


def _pending_at_extract():
    """2026 deaths still pending investigation at the extract (toxicology outstanding)."""
    g = rng("pendx")
    out = []
    for i in range(6):
        d = {"year": 2026, "key": (2026, "pend", i), "sex": "M" if g.random() < .7 else "F", "band": 0, "age": 0,
             "dod": D(2026, 11, 3) + int(g.integers(0, 58)) * DAY, "cls": None, "cat": None}
        d["age"] = int(g.integers(22, 61))
        d["ucod"], d["axis"], d["manner"] = "R99", ["R99"], "Pending investigation"
        place(d, g, "county")
        d["vs"] = [[d["dod"] + int(g.integers(4, 12)) * DAY, fields(d)]]
        out.append(d)
    return out


def _nonresident_overdoses():
    g = rng("nonres_od")
    out = []
    for year in W.YEARS:
        n = int(round(.083 * sum(W.CLASS_N[c][year] for c in "OSR")))
        for i in range(n):
            d = _new_overdose(g, year, (year, "nonres", i))
            if g.random() < .7:
                d["res_county"], d["res_state"] = W.OTHER_COUNTIES[int(g.integers(0, 6))][0], ""
            else:
                d["res_county"], d["res_state"] = "", W.OUT_STATES[int(g.integers(0, len(W.OUT_STATES)))]
            place(d, g, "county")
            pend = d["cat"] != "N" and g.random() < .7
            room = (W.EXTRACT - d["dod"]).days - 4
            d["vs"] = versions(d, g, pending=pend, delay=min(_lag(g, 80, .5, 25, 430), room), extra_amend=.06)
            out.append(d)
    return out


def _duplicates(final):
    """A death registered twice (two funeral homes), the second registration voided before the year's close."""
    g = rng("dups")
    out = []
    for year in W.YEARS:
        cands = sorted([d for d in final if d["year"] == year and d["place_kind"] == "county" and not d["pending"]
                        and year != 2025], key=lambda d: d["key"])
        for k in range(2 if cands else 0):
            src = cands[int(g.integers(0, len(cands)))]
            d = dict(src)
            d["key"] = (year, "dup", k)
            reg = src["dod"] + int(g.integers(14, 45)) * DAY
            void = min(reg + int(g.integers(20, 160)) * DAY, W.CLOSE[year] - 5 * DAY, W.EXTRACT - 5 * DAY)
            d["vs"] = [[reg, fields(src)], [void, dict(fields(src), void=True)]]
            d["duplicate_of"] = src["key"]
            out.append(d)
    return out


def _all_cause(final):
    """Residents' other deaths wherever they occurred, and non-residents' deaths in the county."""
    g = rng("allcause")
    out = []
    for year in W.YEARS:
        n_od = sum(1 for d in final if d["year"] == year)
        n_res = W.ALL_CAUSE[year] - n_od
        n_non = int(round(W.NONRES_OCC * W.ALL_CAUSE[year])) - int(round(.083 * n_od))
        for i in range(n_res + n_non):
            res = i < n_res
            d = {"year": year, "key": (year, "nat", i), "sex": "M" if g.random() < .51 else "F", "dod": _dod(g, year)}
            d["age"] = _age_natural(g)
            _natural_death(d, g, year)
            if not res:
                if g.random() < .75:
                    d["res_county"], d["res_state"] = W.OTHER_COUNTIES[int(g.integers(0, 6))][0], ""
                else:
                    d["res_county"], d["res_state"] = "", W.OUT_STATES[int(g.integers(0, len(W.OUT_STATES)))]
                kind = "county"
            else:
                kind = _pick(g, list(W.PLACE.items()))
            place(d, g, kind, natural=True)
            # drugs named on injury deaths and opioid use disorder as the underlying cause: not overdoses
            if d["ucod"].startswith(INJURY) and g.random() < .045:
                d["axis"] = d["axis"] + [["T40.4", "T43.6", "T40.1", "T42.4"][int(g.integers(0, 4))]]
            if res and g.random() < .0009:
                d["ucod"], d["axis"], d["manner"] = "F11.2", ["F11.2", "I25.1"][:1 + int(g.random() < .4)], "Natural"
            pend = d["ucod"] != "R99" and d["certifier"] != "Physician" and g.random() < .3
            room = (W.EXTRACT - d["dod"]).days - 4
            d["vs"] = versions(d, g, pending=pend, delay=min(_lag(g, 60, .6, 20, 400), room), extra_amend=.07)
            if kind == "out":
                for v in d["vs"]:
                    v[2] = min(v[2], W.EXTRACT - 2 * DAY)
            out.append(d)
    return out


# ---------------------------------------------------------------- the file's rows

def _fmt_axis(axis, registered):
    if registered < W.NEW_SYSTEM:
        return " ".join(legacy(c) for c in axis)
    return " ".join(axis)


def _resident_status(res_county, res_state, occ_county, occ_state):
    if res_state:
        return 3
    if occ_state:
        return 3
    return 1 if occ_county == res_county else 2


def number(recs):
    """State file numbers: in-state deaths by data year in order of registration; out-of-state deaths received
    through the exchange numbered in the order the exchange delivered them. Both series run over every county's
    deaths, so a county's numbers step unevenly."""
    seq = {}
    g = rng("numbers")
    for d in sorted([d for d in recs if d["place_kind"] != "out"], key=lambda d: (d["year"], d["vs"][0][0], str(d["key"]))):
        k = ("S", d["year"])
        seq[k] = seq.get(k, 0) + 1 + int(g.integers(0, 14))
        d["sfn"] = "%d-%06d" % (d["year"], seq[k] + 1000)
    taken = {d["send_no"] for d in recs if d.get("send_no")}
    for d in sorted([d for d in recs if d["place_kind"] == "out" and not d.get("send_no")], key=lambda d: str(d["key"])):
        bump = 0
        while _send_no(d, bump) in taken:
            bump += 1
        d["send_no"] = _send_no(d, bump)
        taken.add(d["send_no"])
    gx = rng("xnumbers")
    for d in sorted([d for d in recs if d["place_kind"] == "out"], key=lambda d: (d["year"], d["vs"][0][2], str(d["key"]))):
        k = ("X", d["year"])
        seq[k] = seq.get(k, 0) + 1 + int(gx.integers(0, 9))
        d["sfn"] = "X%d-%05d" % (d["year"], seq[k] + 100)


def death_rows(recs):
    rows, receipts = [], []
    for d in sorted(recs, key=lambda d: d["sfn"]):
        for k, v in enumerate(d["vs"]):
            reg, f = v[0], v[1]
            if reg > W.EXTRACT or (len(v) > 2 and v[2] > W.EXTRACT):
                continue
            void = f.get("void")
            status = "Void" if void else ("Original" if k == 0 else "Amendment")
            res_code = COUNTY_CODE.get(f["res_county"], "") if not f["res_state"] else ""
            occ_code = COUNTY_CODE.get(d["occ_county"], "") if not d["occ_state"] else ""
            rows.append({
                "state_file_no": d["sfn"], "record_version": k, "record_status": status,
                "registered_date": reg.isoformat(), "date_of_death": d["dod"].isoformat(), "sex": d["sex"],
                "age_years": d["age"], "marital_status": f["marital"], "education": f["education"],
                "residence_county": f["res_county"], "residence_county_code": res_code, "residence_state": f["res_state"],
                "occurrence_county": d["occ_county"], "occurrence_county_code": occ_code, "occurrence_state": d["occ_state"],
                "resident_status": _resident_status(f["res_county"], f["res_state"], d["occ_county"], d["occ_state"]),
                "place_of_death": d["place"], "manner_of_death": f["manner"], "certifier": d["certifier"],
                "underlying_cause": legacy(f["ucod"]) if reg < W.NEW_SYSTEM else f["ucod"],
                "record_axis": _fmt_axis(f["axis"], reg)})
            if len(v) > 2:
                receipts.append({"state_file_no": d["sfn"], "record_version": k, "sending_state": d["occ_state"],
                                 "sending_state_file_no": d["send_no"],
                                 "transaction": "New record" if k == 0 else "Amendment", "received_date": v[2].isoformat()})
    return rows, receipts
