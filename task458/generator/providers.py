"""The clinicians and organisations behind the claims, and their NPPES records.

Practising behavioral-health prescribers (NP-31 section 2.3: a prescriber taxonomy as the primary taxonomy, an active
NPI and a practice location in the county on 1 November 2026, and at least one service to an adult member in the
contract year) sit in each county in the numbers world.COUNTIES sets. Around them NPPES carries what it always does:
prescribers whose listing outlived their practice, prescribers who practise elsewhere and keep a mailing address here,
NPIs deactivated (one reactivated in a weekly file), prescribers who moved or switched their primary taxonomy in the
weekly files, clinicians holding a prescriber taxonomy only as a secondary one, telehealth prescribers practising in
Spokane or Seattle, and the therapists, primary care clinicians, emergency physicians and organisations whose claims
fill the extract."""
import datetime as dt

import numpy as np

import world as W

D = dt.date


class Clin(dict):
    pass


# (county, kind, name, ZIP): behavioral health agencies and opioid treatment programs bill sub-capitated encounters;
# community health centers, emergency physician groups, psychiatric practices and the telepsychiatry group bill claims
ORGS = [
    ("Yakima", "bha", "Sagecrest Behavioral Health", "98902"), ("Yakima", "bha", "Lower Valley Wellness Center", "98944"),
    ("Yakima", "otp", "Naches Heights Treatment Center", "98902"), ("Yakima", "chc", "Bluebunch Health Clinic", "98948"),
    ("Yakima", "edg", "Shrub-Steppe Emergency Physicians", "98902"), ("Yakima", "psy", "Basalt Psychiatric Associates", "98908"),
    ("Benton", "bha", "Quailbrook Counseling Services", "99336"), ("Benton", "otp", "Columbia Point Treatment Services", "99352"),
    ("Benton", "chc", "Badger Canyon Health", "99337"), ("Benton", "edg", "Three Rivers Emergency Physicians", "99336"),
    ("Benton", "psy", "Horse Heaven Psychiatry", "99352"),
    ("Franklin", "bha", "Esquatzel Behavioral Health", "99301"), ("Franklin", "chc", "Ringold Family Health", "99301"),
    ("Franklin", "edg", "Pasco Emergency Group", "99301"), ("Franklin", "psy", "Juniper Dunes Psychiatric Care", "99301"),
    ("Grant", "bha", "Crab Creek Behavioral Health", "98837"), ("Grant", "otp", "Larson Ridge Treatment Services", "98837"),
    ("Grant", "chc", "Saddle Mountain Health", "99349"), ("Grant", "edg", "Basin Emergency Physicians", "98837"),
    ("Grant", "psy", "Potholes Psychiatric Associates", "98848"),
    ("Adams", "bha", "Lind Coulee Counseling", "99344"), ("Adams", "chc", "Cow Creek Health Clinic", "99169"),
    ("Chelan", "bha", "Squilchuck Counseling Center", "98801"), ("Chelan", "otp", "Wenatchee Heights Treatment Center", "98801"),
    ("Chelan", "chc", "Number Two Canyon Health", "98801"), ("Chelan", "edg", "Apple Valley Emergency Physicians", "98801"),
    ("Chelan", "psy", "Icicle Psychiatric Care", "98826"),
    ("Douglas", "bha", "Badger Mountain Clinic", "98802"),
    ("Kittitas", "bha", "Manastash Counseling", "98926"), ("Kittitas", "chc", "Swauk Prairie Health", "98926"),
    ("Okanogan", "bha", "Sinlahekin Behavioral Health", "98840"), ("Okanogan", "otp", "Omak Treatment Services", "98841"),
    ("Okanogan", "chc", "Tunk Valley Health", "98855"),
    ("Walla Walla", "bha", "Touchet Valley Counseling", "99362"), ("Walla Walla", "otp", "Mill Creek Treatment Services", "99362"),
    ("Walla Walla", "chc", "Dry Creek Health Center", "99362"), ("Walla Walla", "edg", "Blue Ridge Emergency Physicians", "99362"),
    ("Walla Walla", "psy", "Pioneer Park Psychiatry", "99362"),
    (None, "tele", "Puget Sound Telepsychiatry Group", "98101"),
]


def _pick(r, weighted):
    items = [x for x, _ in weighted]
    w = np.array([x for _, x in weighted], dtype=float)
    return items[int(r.choice(len(items), p=w / w.sum()))]


def _address(r, county=None, z=None):
    if z is None:
        z = W.ZIPS[county][int(r.integers(len(W.ZIPS[county])))]
        while z in W.SPLIT:
            z = W.ZIPS[county][int(r.integers(len(W.ZIPS[county])))]
    street = "%d %s" % (int(r.integers(100, 4800)), W.STREETS[int(r.integers(len(W.STREETS)))])
    suite = W.SUITES[int(r.integers(len(W.SUITES)))]
    return {"line1": street, "line2": suite, "city": W.CITY.get(z, ""), "state": "WA", "zip": z}


def build():
    """Every clinician and organisation, with the NPPES record each file shows. Returns (clinicians, orgs)."""
    r = np.random.default_rng([W.SEED, 10])
    ff, fm, ll = W.first_last_pools()
    names = set()
    npis = set()

    def person_name():
        while True:
            fem = r.random() < 0.55
            first = (ff if fem else fm)[int(r.integers(len(ff if fem else fm)))]
            last = ll[int(r.integers(len(ll)))]
            if (first, last) not in names:
                names.add((first, last))
                return first, last, "F" if fem else "M"

    def new_npi():
        while True:
            n = W.npi(r)
            if n not in npis:
                npis.add(n)
                return n

    clins = []

    def clin(kind, county, tax, **kw):
        first, last, sex = person_name()
        c = Clin(npi=new_npi(), kind=kind, county=county, first=first, last=last, sex=sex, tax=tax,
                 cred=W.CREDENTIAL.get(tax, {"207Q00000X": "MD", "207R00000X": "MD", "363LF0000X": "FNP-C",
                                             "363LA2200X": "AGNP-C", "363A00000X": "PA-C", "103T00000X": "PhD",
                                             "101YM0800X": "LMHC", "1041C0700X": "LICSW", "101YA0400X": "SUDP",
                                             "207P00000X": "MD", "208D00000X": "DO"}.get(tax, "")),
                 enumerated=D(int(r.integers(2006, 2025)), int(r.integers(1, 13)), int(r.integers(1, 29))),
                 practice=_address(r, county) if county in W.COUNTIES else None, events=[], secondary=None)
        c["mailing"] = dict(c["practice"]) if c["practice"] else None
        c["last_update"] = max(c["enumerated"], D(int(r.integers(2019, 2027)), int(r.integers(1, 10)), int(r.integers(1, 29))))
        c.update(kw)
        clins.append(c)
        return c

    # the special practising prescribers (weekly-file changes and deactivations) and the counties NP-31 counts them in
    special_in = {"Adams": 1, "Grant": 1, "Benton": 1, "Chelan": 1, "Franklin": 1, "Kittitas": 1}
    # practising behavioral-health prescribers, county by county, so each county's count on 1 November is its target
    for cname, cty in sorted(W.COUNTIES.items()):
        for _ in range(cty["prescribers"] - special_in.get(cname, 0)):
            clin("prescriber", cname, _pick(r, W.PRESCRIBER_MIX))
    # a Bridgeport practice (ZIP 98813, whose business addresses lie mostly in Okanogan County and homes mostly in Douglas)
    # and a Royal City practice (ZIP 99357, businesses mostly in Grant County, homes mostly in Adams)
    for cname, z in (("Okanogan", "98813"), ("Grant", "99357")):
        c = [x for x in clins if x["kind"] == "prescriber" and x["county"] == cname][0]
        c["practice"] = _address(r, cname, z)
        c["mailing"] = dict(c["practice"])
    # mailing addresses: a post office box in the practice's town for some, and for a few the home address in another
    # of the plan's counties (NPPES keeps both; NP-31 reads the practice location)
    pres = [x for x in clins if x["kind"] == "prescriber"]
    for c in pres:
        if r.random() < 0.12:
            c["mailing"] = dict(c["practice"], line1="PO Box %d" % int(r.integers(100, 9900)), line2="")
    for frm, to, z in (("Yakima", "Benton", "99352"), ("Yakima", "Benton", "99353"), ("Chelan", "Douglas", "98802"),
                       ("Benton", "Walla Walla", "99362"), ("Kittitas", "Yakima", "98942")):
        cand = [x for x in pres if x["county"] == frm and x["mailing"] == x["practice"]]
        c = cand[int(r.integers(len(cand)))]
        c["mailing"] = _address(r, to, z)
        c["mailing"]["line2"] = ""
    # telehealth prescribers practising outside the plan's counties who see its members
    for city, z in [("Spokane", "99201"), ("Spokane", "99204"), ("Seattle", "98104"), ("Spokane", "99201"),
                    ("Bellevue", "98004"), ("Seattle", "98122")]:
        c = clin("tele", None, _pick(r, W.PRESCRIBER_MIX))
        c["practice"] = {"line1": "%d %s" % (int(r.integers(100, 2400)), ["N Monroe St", "W Riverside Ave", "2nd Ave",
                         "E Pine St", "NE 8th St"][int(r.integers(5))]), "line2": "Suite %d" % int(r.integers(100, 900)),
                         "city": city, "state": "WA", "zip": z}
        c["mailing"] = dict(c["practice"])
    # listings that outlived the practice: a prescriber taxonomy, an active NPI, a practice address in a county, and no
    # service in the contract year (retired, left the state, or never saw the plan's members)
    dark = {"Okanogan": 4, "Douglas": 3, "Adams": 2, "Grant": 3, "Franklin": 3, "Yakima": 1, "Benton": 4, "Chelan": 3,
            "Walla Walla": 3, "Kittitas": 2}
    for cname, n in sorted(dark.items()):
        for _ in range(n):
            c = clin("dark", cname, _pick(r, W.PRESCRIBER_MIX))
            c["last_update"] = D(int(r.integers(2011, 2021)), int(r.integers(1, 13)), int(r.integers(1, 29)))
            c["enumerated"] = min(c["enumerated"], c["last_update"])
    # prescribers practising elsewhere who keep a mailing address in the plan's counties (no service to its members)
    for cname in ["Yakima", "Benton", "Chelan", "Okanogan", "Grant", "Walla Walla"]:
        c = clin("mail_only", cname, _pick(r, W.PRESCRIBER_MIX))
        city, st, z = W.OUT_OF_STATE[int(r.integers(len(W.OUT_OF_STATE)))]
        c["mailing"] = dict(c["practice"])
        c["practice"] = {"line1": "%d %s" % (int(r.integers(100, 3000)), "SW Main St"), "line2": "", "city": city,
                         "state": st, "zip": z}
    # NPIs deactivated: one in March 2026 (a listing whose practice had already closed); one in June 2026 and
    # reactivated in a weekly file on 20 October; one on 21 October (before 1 November) and one on 5 November (after it)
    for cname, when, react, kind in [("Yakima", D(2026, 3, 14), None, "deact"),
                                     ("Chelan", D(2026, 6, 2), D(2026, 10, 20), "react"),
                                     ("Benton", D(2026, 10, 21), None, "deact_late_before"),
                                     ("Franklin", D(2026, 11, 5), None, "deact_late_after")]:
        clin(kind, cname, _pick(r, W.PRESCRIBER_MIX), deactivated=when, reactivated=react)
    # practice location moves in the weekly files, and one dated after 1 November
    for frm, to, when in [("Okanogan", "Spokane", D(2026, 10, 16)), ("Grant", "Adams", D(2026, 10, 23)),
                          ("Yakima", "Benton", D(2026, 10, 29)), ("Kittitas", "Seattle", D(2026, 11, 2))]:
        clin("mover", frm, _pick(r, W.PRESCRIBER_MIX), moved_to=to, moved_on=when)
    # a family nurse practitioner who switched her primary taxonomy to psychiatric-mental health on 22 October
    clin("switch", "Grant", "363LF0000X", switched_to="363LP0808X", switched_on=D(2026, 10, 22), secondary="363LP0808X")
    # clinicians holding a prescriber taxonomy only as a secondary one (family practice first)
    for cname in ["Franklin", "Adams", "Okanogan", "Yakima", "Douglas"]:
        c = clin("secondary", cname, "363LF0000X" if r.random() < 0.6 else "207Q00000X")
        c["secondary"] = "363LP0808X" if c["tax"] == "363LF0000X" else "207QA0401X"
    # new enumerations in the weekly files (no service in the contract year)
    for cname in ["Yakima", "Grant", "Benton"]:
        c = clin("new", cname, _pick(r, W.PRESCRIBER_MIX))
        c["enumerated"] = D(2026, 10, int(r.integers(13, 30)))
        c["last_update"] = c["enumerated"]
    # therapists, case managers, primary care and emergency clinicians
    for cname, cty in sorted(W.COUNTIES.items()):
        n = max(3, int(round(cty["prescribers"] * 1.6)))
        for _ in range(n):
            clin("therapist", cname, _pick(r, [("103T00000X", 2), ("101YM0800X", 4), ("1041C0700X", 4),
                                                 ("101YA0400X", 2)]))
        for _ in range(max(2, int(round(cty["prescribers"] * 0.8)))):
            clin("pcp", cname, _pick(r, [("207Q00000X", 5), ("207R00000X", 2), ("363LF0000X", 4), ("363A00000X", 2)]))
        for _ in range(max(2, int(round(cty["prescribers"] * 0.3)))):
            clin("ed", cname, "207P00000X")
    # organisations: behavioral health agencies (sub-capitated), opioid treatment programs (sub-capitated), community
    # health centers, emergency physician groups and psychiatric practices (fee-for-service)
    orgs = []
    psy_tax = {"Basalt Psychiatric Associates": "2084P0800X", "Horse Heaven Psychiatry": "193400000X",
               "Juniper Dunes Psychiatric Care": "261QM0801X", "Potholes Psychiatric Associates": "193400000X",
               "Icicle Psychiatric Care": "2084P0800X", "Pioneer Park Psychiatry": "193400000X"}
    for cname, kind, nm, z in ORGS:
        tax = psy_tax[nm] if kind == "psy" else {"bha": "261QM0801X", "otp": "261QM2800X", "chc": "261QF0400X",
                                                  "edg": "207P00000X", "tele": "193400000X"}[kind]
        if kind == "tele":
            addr = {"line1": "1201 3rd Ave", "line2": "Suite 2210", "city": "Seattle", "state": "WA", "zip": "98101"}
        else:
            addr = _address(r, cname, z)
        orgs.append({"npi": new_npi(), "name": nm.upper(), "county": cname, "kind": kind, "tax": tax,
                     "practice": addr, "mailing": dict(addr),
                     "enumerated": D(int(r.integers(2006, 2016)), int(r.integers(1, 13)), int(r.integers(1, 28))),
                     "last_update": D(int(r.integers(2020, 2027)), int(r.integers(1, 10)), int(r.integers(1, 28)))})
    return clins, orgs


def located_on(c, day):
    """The county of a clinician's practice location on a day (None outside the ten counties)."""
    if c["kind"] == "mover" and day >= c["moved_on"]:
        return c["moved_to"] if c["moved_to"] in W.COUNTIES else None
    return c["county"]


def active_on(c, day):
    d = c.get("deactivated")
    if d is None or day < d:
        return True
    rd = c.get("reactivated")
    return rd is not None and day >= rd


def primary_on(c, day):
    if c["kind"] == "switch" and day >= c["switched_on"]:
        return c["switched_to"]
    return c["tax"]


def renders(c):
    """Whether the clinician renders services to the plan's members in the contract year."""
    return c["kind"] in ("prescriber", "tele", "react", "deact_late_before", "deact_late_after", "mover", "switch",
                         "secondary", "therapist", "pcp", "ed")


def practising(clins, day=W.AS_OF):
    """The prescribers NP-31 counts, by construction: county -> [npi]."""
    out = {c: [] for c in W.COUNTIES}
    for c in clins:
        if not renders(c) or not active_on(c, day) or primary_on(c, day) not in W.BH_TAXONOMY:
            continue
        k = located_on(c, day)
        if k in W.COUNTIES:
            out[k].append(c["npi"])
    return out
