"""The county EMS data system's patient care reports for calls with naloxone given, a poisoning, overdose,
intoxication, altered mental status or unresponsiveness impression, 2021 to 2026: one report per responding unit per
patient, a fire first response and the transport ambulance each filing their own under the incident's CAD number.
The fire districts' records system computes a patient's age from the birth year (the calendar year of the call less
the year of birth); the ambulance services' systems compute it from the date of birth. A unit that hands a patient to
another unit names the receiving unit as the destination."""
import collections
import datetime as dt

import numpy as np

import world as W

DAY = dt.timedelta(days=1)
MIN = dt.timedelta(minutes=1)
OPIOID_IMP = ["T40.601A", "T40.411A", "T40.1X1A", "T40.2X1A", "T40.691A"]
ADVERSE_IMP = [("T40.2X5A", .55), ("T40.415A", .20), ("T40.425A", .12), ("T40.3X5A", .08), ("T40.605A", .05)]
SECONDARY = [("T43.621A", .33), ("T40.5X1A", .14), ("F11.20", .15), ("F15.10", .08), ("T51.0X1A", .10), ("R40.4", .07),
             ("F10.129", .05), ("T42.4X1A", .05), ("R06.89", .03)]
POISON_IMP = [("T43.621A", .24), ("T40.5X1A", .18), ("T51.0X1A", .16), ("T42.4X1A", .14), ("T50.901A", .10),
              ("T39.1X1A", .07), ("T43.212A", .05), ("T42.6X1A", .04), ("T65.91XA", .02)]
FIRE = [("Wendmoor Fire District", "WFD", ["E%d" % k for k in range(11, 23)], .78),
        ("Tarrow Fire Department", "TFD", ["E%d" % k for k in range(1, 6)], .22)]
TRANSPORT = [("Wendmoor County EMS", "WCEMS", ["M%d" % k for k in range(1, 19)], .83),
             ("Wendmoor Valley Ambulance", "WVA", ["A%d" % k for k in range(1, 7)], .17)]
SUPERVISORS = ["EMS1", "EMS2", "EMS3"]
DEAD = ["Dead at Scene, Resuscitation Attempted (Without Transport)",
        "Dead at Scene, No Resuscitation Attempted (Without Transport)"]
TRANSFER = "Patient Treated, Transferred Care to Another EMS Unit"
TRANSPORTED = "Patient Treated, Transported by this EMS Unit"
REFUSED = "Patient Refused Evaluation/Care (Without Transport)"
RELEASED = "Patient Treated, Released (per protocol)"
DEST = ["Wendmoor General Hospital", "Ardemere Valley Medical Center", "Wendmoor General Hospital", "Tarrow Community Hospital"]
OPIOID_CATS = ("T400", "T401", "T402", "T403", "T404", "T406")


def rng(*keys):
    return np.random.default_rng([W.SEED, 77] + [k if isinstance(k, int) else sum(ord(c) * (i + 1) for i, c in enumerate(k))
                                                for k in keys])


def _pick(g, pairs):
    r, acc = g.random(), 0.0
    for v, p in pairs:
        acc += p
        if r < acc:
            return v
    return pairs[-1][0]


def quarters():
    out = []
    for y in range(W.EMS_START, W.TARGET + 1):
        for q in range(4):
            out.append((y, q + 1))
    return out


def _when(g, y, q):
    start = dt.date(y, 3 * q - 2, 1)
    end = dt.date(y + (q == 4), 1 if q == 4 else 3 * q + 1, 1)
    d = start + int(g.integers(0, (end - start).days)) * DAY
    hour = int(g.choice(24, p=np.array([3, 3, 2, 2, 1, 1, 1, 2, 3, 4, 4, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 5, 4]) / 98))
    return dt.datetime(d.year, d.month, d.day, hour, int(g.integers(0, 60)))


def _born(e):
    """A date of birth that makes the patient the drawn age on the day of the call (infants: the drawn months)."""
    h = rng("dob", *e["key"])
    c = e["call"].date()
    if e.get("months") is not None:
        b = c - int(e["months"] * 30.44 + h.integers(0, 28)) * DAY
    else:
        try:
            hi = c.replace(year=c.year - e["age"])
        except ValueError:
            hi = dt.date(c.year - e["age"], 2, 28)
        b = hi - int(h.integers(0, 365)) * DAY
    e["dob"] = b
    exact = c.year - b.year - ((c.month, c.day) < (b.month, b.day))
    assert e.get("months") is not None or exact == e["age"], (e["key"], exact, e["age"])
    e["fire_age"] = c.year - b.year


# ---------------------------------------------------------------- encounters

def encounters(extra_adverse=None, pairs=None):
    """Every patient encounter with the facts behind its reports: kind, residence, outcome, birth date."""
    extra_adverse = extra_adverse or {}
    out = []
    for i, (y, q) in enumerate(quarters()):
        g = rng("enc", y, q)
        n_od = W.EMS_BASE[i]
        kinds = (["od_res"] * n_od + ["od_non"] * int(round(n_od * .12)) + ["od_fatal"] * int(round(n_od * .075)) +
                 ["empiric"] * int(42 + g.integers(-6, 7)) + ["poison"] * int(70 + g.integers(-9, 10)) +
                 ["oud"] * int(12 + g.integers(-3, 4)))
        kinds += ["adverse"] * (int(rng("adv", y, q).integers(5, 9)) + extra_adverse.get((y, q), 0))
        for k, kind in enumerate(kinds):
            e = {"y": y, "q": q, "kind": kind, "key": (y, q, k)}
            e["call"] = _when(g, y, q)
            if kind == "adverse":
                e["sex"] = "Male" if g.random() < .45 else "Female"
                e["age"] = int(g.integers(62, 93))
            else:
                e["sex"] = "Male" if g.random() < (.68 if kind.startswith("od") or kind == "oud" else .52) else "Female"
                e["age"] = int(g.integers(19, 62)) if kind.startswith("od") or kind in ("oud", "poison") else int(g.integers(24, 91))
            if kind == "poison":
                h = rng("child", y, q, k)
                u = h.random()
                if u < .02:
                    e["age"], e["months"] = 0, int(h.integers(3, 12))
                elif u < .08:
                    e["age"] = int(h.integers(1, 5))
            if kind == "od_non":
                e["county"], e["state"] = (W.OTHER_COUNTIES[int(g.integers(0, 6))][0], "") if g.random() < .7 else \
                                          ("", W.OUT_STATES[int(g.integers(0, len(W.OUT_STATES)))])
            else:
                e["county"], e["state"] = (W.COUNTY, "") if g.random() < (.92 if kind == "adverse" else .93) or kind == "od_res" else \
                                          (W.OTHER_COUNTIES[int(g.integers(0, 6))][0], "")
            e["fatal"] = kind == "od_fatal"
            e["opioid"] = kind.startswith("od")
            out.append(e)
    # a few incidents with two or three patients (people who used together): later encounters join an earlier
    # encounter's incident in the same quarter when their kind allows it
    for i, (y, q) in enumerate(quarters()):
        g = rng("multi", y, q)
        qs = [e for e in out if e["y"] == y and e["q"] == q and e["kind"] in ("od_res", "od_non", "od_fatal")]
        hosts = [qs[int(j)] for j in g.choice(len(qs), size=int(9 + g.integers(0, 6)), replace=False)]
        used = {id(h) for h in hosts}
        for h in hosts:
            m = 1 + (g.random() < .14)
            for _ in range(m):
                c = qs[int(g.integers(0, len(qs)))]
                if id(c) in used or c.get("host"):
                    continue
                if c["sex"] == h["sex"] and c["age"] == h["age"]:
                    continue
                used.add(id(c))
                c["host"] = h["key"]
                c["call"] = h["call"]
    by_key = {e["key"]: e for e in out}
    for hk, ck in (pairs or []):
        h, c = by_key[hk], by_key[ck]
        c["host"] = h.get("host") or h["key"]
        c["call"] = h["call"]
    for e in out:
        _born(e)
    return out


# ---------------------------------------------------------------- reports

def reports(encs, fire_county=None):
    """The reports each encounter produced, before numbering."""
    fire_county = fire_county or set()
    out = []
    for e in encs:
        g = rng("rep", *e["key"])
        kind = e["kind"]
        fire = g.random() < (.72 if kind != "adverse" else .6)
        amb = (not fire) or g.random() < .9
        nal_fire = fire and ((e["opioid"] and g.random() < .55) or (kind == "empiric" and g.random() < .5) or
                             (kind == "adverse" and g.random() < .1))
        nal_amb = amb and ((e["opioid"] and (g.random() < (.25 if nal_fire else .80))) or
                           (kind == "empiric" and not nal_fire) or (kind == "adverse" and not nal_fire and g.random() < .1))
        if kind == "empiric" and not (nal_fire or nal_amb):
            nal_amb = amb
            nal_fire = fire and not amb
        reps = []
        if fire:
            agency = FIRE[0] if g.random() < FIRE[0][3] else FIRE[1]
            if kind == "empiric":
                imp = ["E16.2", "R41.82", "R56.9", "I63.9"][int(g.integers(0, 4))]
            elif kind == "adverse":
                imp = _pick(g, [("R41.82", .6), ("R40.4", .25), ("R53.83", .15)])
            elif kind in ("poison", "oud"):
                imp = "T43.621A" if g.random() < .5 else "R41.82"
            else:
                imp = OPIOID_IMP[int(g.integers(0, 2))] if (e["opioid"] and g.random() < .4) else \
                      ("R41.82" if g.random() < .65 else "R40.20")
            if amb:
                disp, known = TRANSFER, (g.random() < .4) or e["key"] in fire_county
            else:
                disp, known = (DEAD[1] if e["fatal"] else (REFUSED if g.random() < .7 else RELEASED)), True
            reps.append({"role": "fire", "agency": agency, "naloxone": nal_fire, "imp1": imp, "imp2": "",
                         "county_known": known, "disp": disp, "delay": int(g.integers(4, 11))})
        if amb:
            agency = TRANSPORT[0] if g.random() < TRANSPORT[0][3] else TRANSPORT[1]
            imp2 = ""
            if kind == "od_fatal":
                imp, disp = OPIOID_IMP[int(g.integers(0, 2))] if g.random() < .6 else "I46.9", DEAD[0] if g.random() < .8 else DEAD[1]
            elif e["opioid"]:
                imp = OPIOID_IMP[int(g.integers(0, 5))] if g.random() < .84 else ("R41.82" if g.random() < .7 else "R06.89")
                disp = TRANSPORTED if g.random() < .78 else (REFUSED if g.random() < .85 else RELEASED)
                if imp.startswith("T40") and g.random() < .25:
                    imp2 = _pick(g, SECONDARY)
            elif kind == "empiric":
                imp = ["E16.2", "R41.82", "R56.9", "I63.9"][int(g.integers(0, 4))]
                disp = TRANSPORTED
            elif kind == "oud":
                imp = "F11.129" if g.random() < .7 else "F11.23"
                disp = TRANSPORTED if g.random() < .6 else REFUSED
            elif kind == "adverse":
                imp = _pick(g, ADVERSE_IMP)
                disp = TRANSPORTED if g.random() < .85 else (REFUSED if g.random() < .67 else RELEASED)
                if g.random() < .2:
                    imp2 = _pick(g, [("R41.0", .5), ("N18.9", .3), ("I10", .2)])
            else:
                imp = _pick(g, POISON_IMP)
                disp = TRANSPORTED if g.random() < .8 else REFUSED
                if g.random() < .12:
                    imp2 = "R45.851" if g.random() < .7 else "F32.9"
            reps.append({"role": "amb", "agency": agency, "naloxone": nal_amb, "imp1": imp, "imp2": imp2,
                         "county_known": True, "disp": disp, "delay": int(g.integers(6, 16))})
            if not e["fatal"] and g.random() < .04:
                reps.append({"role": "sup", "agency": TRANSPORT[0], "naloxone": False, "imp1": imp, "imp2": "",
                             "county_known": g.random() < .6, "disp": TRANSFER, "delay": int(g.integers(9, 22))})
        for r in reps:
            r["enc"] = e
            r["doses"] = (1 + (g.random() < .35)) if r["naloxone"] else 0
            r["response"] = ("Improved" if ((e["opioid"] or kind == "adverse") and not e["fatal"]) else ("Unchanged" if e["fatal"] else
                             ("Improved" if g.random() < .2 else "Unchanged"))) if r["naloxone"] else ""
            out.append(r)
    return out


# ---------------------------------------------------------------- the file's rows

def rows(encs, reps):
    """Number the incidents and reports, assign the units and write each report's row."""
    g = rng("numbers")
    inc_no, seq = {}, {}
    for e in sorted(encs, key=lambda e: (e["call"], e["key"])):
        host = e.get("host") or e["key"]
        if host not in inc_no:
            yy = e["call"].year % 100
            seq[yy] = seq.get(yy, 0) + int(g.integers(9, 31))
            inc_no[host] = "WCC%02d-%07d" % (yy, 104000 + seq[yy])
        e["incident"] = inc_no[host]
    order = sorted(reps, key=lambda r: (r["enc"]["call"], r["enc"]["key"], r["role"]))
    engine, taken = {}, collections.defaultdict(set)
    for r in order:
        e = r["enc"]
        name, code, units, _ = r["agency"]
        if r["role"] == "fire":
            k = (e["incident"], code)
            if k not in engine:
                engine[k] = units[int(g.integers(0, len(units)))]
            r["unit"] = engine[k]
        elif r["role"] == "sup":
            r["unit"] = SUPERVISORS[int(g.integers(0, len(SUPERVISORS)))]
        else:
            free = [u for u in units if u not in taken[(e["incident"], code)]]
            r["unit"] = free[int(g.integers(0, len(free)))]
            taken[(e["incident"], code)].add(r["unit"])
            e["receiving"] = "%s %s" % (name, r["unit"])
    out, pcr = [], {}
    for r in order:
        e = r["enc"]
        name, code, units, _ = r["agency"]
        yy = e["call"].year
        pcr[(code, yy)] = pcr.get((code, yy), 0) + 1 + int(g.integers(0, 3))
        arrived = e["call"] + r["delay"] * MIN
        county = e["county"] if r["county_known"] else ""
        state = e["state"] if r["county_known"] else ""
        if r["disp"] == TRANSPORTED:
            dest = DEST[int(g.integers(0, len(DEST)))]
        elif r["disp"] == TRANSFER:
            dest = e["receiving"]
        else:
            dest = ""
        if r["role"] == "fire":
            age, units_ = e["fire_age"], "Years"
        elif e.get("months") is not None:
            age, units_ = e["months"], "Months"
        else:
            age, units_ = e["age"], "Years"
        out.append({
            "pcr_number": "%s-%d-%06d" % (code, yy, pcr[(code, yy)]),
            "agency_name": name, "unit": r["unit"], "incident_number": e["incident"],
            "psap_call_datetime": e["call"].strftime("%Y-%m-%d %H:%M"),
            "unit_arrived_datetime": arrived.strftime("%Y-%m-%d %H:%M"),
            "patient_age": age, "patient_age_units": units_, "patient_gender": e["sex"],
            "patient_home_county": county, "patient_home_state": state,
            "primary_impression": r["imp1"], "secondary_impression": r["imp2"],
            "naloxone_administered": "Yes" if r["naloxone"] else "No", "naloxone_doses": r["doses"] or "",
            "naloxone_response": r["response"], "disposition": r["disp"], "destination": dest})
    out.sort(key=lambda r: (r["psap_call_datetime"], r["incident_number"], r["pcr_number"]))
    return out


# ---------------------------------------------------------------- reading the rows (the golden and the stops)

def opioid_poisoning(code):
    """An ICD-10-CM poisoning code under T40.0 to T40.4 or T40.6 (sixth character 1 to 4: accidental, intentional
    self-harm, assault, undetermined; 5 is an adverse effect and 6 underdosing)."""
    c = code.replace(".", "")
    return c[:4] in OPIOID_CATS and len(c) >= 6 and c[5] in "1234"


def opioid_prefix(code):
    return code.replace(".", "")[:4] in OPIOID_CATS


def quarter(r):
    y, m = int(r["psap_call_datetime"][:4]), int(r["psap_call_datetime"][5:7])
    return "%dQ%d" % (y, (m - 1) // 3 + 1)


def linked(rows_):
    """Patients as the reports record them: every report that does not hand the patient over is a patient; a report
    that hands over joins the receiving unit's report on the same incident."""
    by_inc = collections.defaultdict(list)
    for r in rows_:
        by_inc[r["incident_number"]].append(r)
    out = []
    for inc, rs in by_inc.items():
        heads = {}
        for r in rs:
            if r["disposition"] != TRANSFER:
                heads.setdefault("%s %s" % (r["agency_name"], r["unit"]), []).append([r])
        groups = [grp for v in heads.values() for grp in v]
        for r in rs:
            if r["disposition"] == TRANSFER:
                tgt = heads[r["destination"]]
                assert len(tgt) == 1, (inc, r["destination"])
                tgt[0].append(r)
        out.extend(groups)
    return out


def grouped(rows_, key):
    g = collections.defaultdict(list)
    for r in rows_:
        g[key(r)].append(r)
    return list(g.values())


KEYS = {"linked": None,
        "incident, sex and age": lambda r: (r["incident_number"], r["patient_gender"], r["patient_age"], r["patient_age_units"]),
        "incident and sex": lambda r: (r["incident_number"], r["patient_gender"]),
        "incident": lambda r: r["incident_number"]}


def count(rows_, key="linked", codes=opioid_poisoning):
    groups = linked(rows_) if key == "linked" else grouped(rows_, KEYS[key])
    out = collections.Counter({"%dQ%d" % yq: 0 for yq in quarters()})
    for rs in groups:
        crit = any(r["naloxone_administered"] == "Yes" or codes(r["primary_impression"]) or codes(r["secondary_impression"])
                   for r in rs)
        res = any(r["patient_home_county"] == W.COUNTY and not r["patient_home_state"] for r in rs)
        alive = not any(r["disposition"].startswith("Dead at Scene") for r in rs)
        if crit and res and alive:
            out[quarter(rs[0])] += 1
    return dict(sorted(out.items()))


def cells(rows_):
    """Every way of grouping the reports, with the poisoning codes and with every T40 code."""
    out = {}
    for k in KEYS:
        for nm, fn in (("poisoning", opioid_poisoning), ("prefix", opioid_prefix)):
            out[(k, nm)] = count(rows_, k, fn)
    return out


def truth(encs, reps):
    """The measure from the encounters themselves."""
    crit = collections.defaultdict(bool)
    for r in reps:
        crit[r["enc"]["key"]] |= r["naloxone"] or opioid_poisoning(r["imp1"]) or opioid_poisoning(r["imp2"])
    out = collections.Counter({"%dQ%d" % yq: 0 for yq in quarters()})
    for e in encs:
        if crit[e["key"]] and e["county"] == W.COUNTY and not e["state"] and not e["fatal"]:
            out["%dQ%d" % (e["call"].year, (e["call"].month - 1) // 3 + 1)] += 1
    return dict(sorted(out.items()))


def build():
    """Encounters, reports and rows, adjusted until no other grouping or code reading lands on the measure in any
    quarter: an extra adverse-effect call where a reading that counts every T40 code would net to the measure, an
    address taken by a fire crew where the birth-year ages would, two patients of one sex at one incident where a
    grouping by incident and sex would."""
    extra, pairs, fire_county = collections.Counter(), [], set()
    for _ in range(12):
        encs = encounters(extra, pairs)
        reps = reports(encs, fire_county)
        rws = rows(encs, reps)
        gold = count(rws)
        cl = cells(rws)
        fixed = False
        for (k, nm), cnt in cl.items():
            if (k, nm) == ("linked", "poisoning"):
                continue
            for qk, v in cnt.items():
                if v != gold[qk]:
                    continue
                y, q = int(qk[:4]), int(qk[5])
                if nm == "prefix":
                    extra[(y, q)] += 1
                elif k == "incident, sex and age":
                    fire_county |= _split_fire(encs, reps, y, q, fire_county)
                else:
                    pairs.append(_same_sex_pair(encs, reps, y, q, pairs))
                fixed = True
        if not fixed:
            assert gold == truth(encs, reps)
            return encs, reps, rws
    raise SystemExit("EMS readings still collide")


def _counted(e, reps_by):
    return (e["county"] == W.COUNTY and not e["state"] and not e["fatal"] and
            any(r["naloxone"] or opioid_poisoning(r["imp1"]) or opioid_poisoning(r["imp2"]) for r in reps_by[e["key"]]))


def _split_fire(encs, reps, y, q, done):
    reps_by = collections.defaultdict(list)
    for r in reps:
        reps_by[r["enc"]["key"]].append(r)
    for e in sorted(encs, key=lambda e: e["key"]):
        if e["y"] != y or e["q"] != q or e["key"] in done or e.get("months") is not None or e["fire_age"] == e["age"]:
            continue
        fr = [r for r in reps_by[e["key"]] if r["role"] == "fire"]
        if fr and fr[0]["disp"] == TRANSFER and not fr[0]["county_known"] and _counted(e, reps_by) and \
                (fr[0]["naloxone"] or opioid_poisoning(fr[0]["imp1"])):
            return {e["key"]}
    raise SystemExit("no fire report to take an address in %dQ%d" % (y, q))


def _same_sex_pair(encs, reps, y, q, pairs):
    reps_by = collections.defaultdict(list)
    for r in reps:
        reps_by[r["enc"]["key"]].append(r)
    taken = {k for p in pairs for k in p}
    alone = [e for e in sorted(encs, key=lambda e: e["key"]) if e["y"] == y and e["q"] == q and e["kind"] == "od_res"
             and not e.get("host") and e["key"] not in taken and _counted(e, reps_by)]
    hosted = {e.get("host") for e in encs if e.get("host")}
    alone = [e for e in alone if e["key"] not in hosted]
    for i, h in enumerate(alone):
        for c in alone[i + 1:]:
            if c["sex"] == h["sex"] and abs(c["age"] - h["age"]) >= 3:
                return (h["key"], c["key"])
    raise SystemExit("no pair in %dQ%d" % (y, q))
