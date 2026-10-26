"""Row-level tables cut from the world: the force's arrest records, the Criminal Justice Unit's remand files, the custody
healthcare provider's contact export, data.police.uk's street-level crime, the LSOA lookup and the ward allocation.
Each table is built the way its own system writes it; the mess here is the systems' own."""
import collections
import datetime as dt
import hashlib
from zoneinfo import ZoneInfo

import numpy as np

import world as WD

UK = ZoneInfo("Europe/London")
UTC = dt.timezone.utc
# suites closed in 2025-26 (local time): Wendle Cross for its cell refit, Eastmoor after a sprinkler flood in its cell
# corridor; the wards of a closed suite are booked into its host, and its healthcare team works there
CLOSURES = {"Wendle Cross": (dt.datetime(2025, 11, 3, 8, 0), dt.datetime(2026, 1, 30, 8, 0), "Southfields", .55),
            "Eastmoor": (dt.datetime(2025, 8, 14, 14, 20), dt.datetime(2025, 9, 2, 8, 0), "Northgate", .35)}
BANK_HOLIDAYS = [dt.date(2025, 1, 1), dt.date(2025, 4, 18), dt.date(2025, 4, 21), dt.date(2025, 5, 5),
                 dt.date(2025, 5, 26), dt.date(2025, 8, 25), dt.date(2025, 12, 25), dt.date(2025, 12, 26),
                 dt.date(2026, 1, 1), dt.date(2026, 4, 3), dt.date(2026, 4, 6), dt.date(2026, 5, 4),
                 dt.date(2026, 5, 25), dt.date(2026, 8, 31), dt.date(2026, 12, 25), dt.date(2026, 12, 28)]
HOURS = np.array([5, 4, 3, 2, 1.5, 1, 1, 1.5, 2.5, 3, 3.5, 4, 4.5, 4.5, 4.5, 5, 5.5, 6, 6, 6, 6.5, 6.5, 6.5, 6])
HOURS = HOURS / HOURS.sum()
AGES = ["10-17", "18-24", "25-34", "35-44", "45-54", "55 and over"]
AGE_P = np.array([.07, .24, .30, .20, .12, .07])
GROUP_SIZE = {"Violence and sexual offences": [.84, .11, .04, .01], "Public order": [.80, .13, .05, .02],
              "Drugs": [.80, .14, .05, .01], "Robbery": [.64, .24, .09, .03], "Possession of weapons": [.86, .10, .04, 0],
              "Criminal damage and arson": [.90, .08, .02, 0], "Shoplifting": [.92, .07, .01, 0],
              "Burglary": [.74, .19, .06, .01], "Vehicle crime": [.86, .11, .03, 0]}
CHARGE = dict(zip(WD.TYPES, [.35, .30, .30, .45, .55, .45, .25, .40, .35, .30, .35, .25, .30]))
REMAND = {"Violence and sexual offences": .15, "Robbery": .32, "Burglary": .26, "Possession of weapons": .22, "Drugs": .11}
OTHER_OUT = [("Released under investigation", .36), ("No further action", .29), ("Released on police bail", .13),
             ("Caution", .09), ("Community resolution", .06), ("Transferred to another force", .03), ("Other", .04)]
LONG = {"Violence and sexual offences": .11, "Robbery": .16, "Burglary": .12, "Drugs": .10, "Possession of weapons": .12}
SUITE_CODE = {"Northgate": "NG", "Eastmoor": "EM", "Southfields": "SF", "Wendle Cross": "WX"}
NEAR = {"Northgate": "Eastmoor", "Eastmoor": "Northgate", "Southfields": "Wendle Cross", "Wendle Cross": "Southfields"}
COURT = {"Northgate": "Calderwick Magistrates' Court", "Eastmoor": "Calderwick Magistrates' Court",
         "Southfields": "South Carvell Magistrates' Court", "Wendle Cross": "Wendlebury Magistrates' Court"}


def to_utc(t_local):
    return t_local.replace(tzinfo=UK).astimezone(UTC).replace(tzinfo=None)


def to_local(t_utc):
    return t_utc.replace(tzinfo=UTC).astimezone(UK).replace(tzinfo=None)


def fy_local(t):
    return t.year if t.month >= 4 else t.year - 1


def pick(rng, table):
    p = np.array([x[1] for x in table])
    return table[int(rng.choice(len(table), p=p / p.sum()))][0]


def sitting_day(d):
    """Remand courts sit Monday to Saturday, not on bank holidays."""
    return d.weekday() != 6 and d not in BANK_HOLIDAYS


def first_hearing(charged):
    """A defendant charged and kept in custody goes to the next remand court: the same day when charged before
    06:30 on a sitting day, otherwise the next sitting day."""
    d = charged.date()
    if not (sitting_day(d) and charged.time() < dt.time(6, 30)):
        d = d + dt.timedelta(days=1)
        while not sitting_day(d):
            d = d + dt.timedelta(days=1)
    return d


def wards_codes():
    return {w: "E05%06d" % (14000 + 37 * i) for i, w in enumerate(WD.WARDS)}


# ---------------------------------------------------------------------------------------------------------------
def lsoa_frame(W, rng):
    """LSOA codes, names, centroids and data.police.uk map points."""
    cnt = collections.Counter()
    streets = STREETS
    for i, l in enumerate(W["lsoas"]):
        la = WD.DISTRICT[l["ward"]]
        cnt[la] += 1
        l["code"] = "E01%06d" % (31000 + 29 * i)
        l["name"] = "%s %03d%s" % (la, (cnt[la] - 1) // 5 + 1, "ABCDE"[(cnt[la] - 1) % 5])
        wi = WD.WARDS.index(l["ward"])
        if l["ward"] in WD.CITY:
            ang = 2 * np.pi * wi / 24
            rad = 0.006 if l["ward"] in WD.HUB else 0.04
            c = (52.9134 + rad * np.sin(ang) + rng.normal(0, 0.006), -1.4762 + 1.6 * rad * np.cos(ang) + rng.normal(0, 0.009))
        else:
            ang = 2 * np.pi * (wi - 24) / 100
            c = (52.9134 + 0.20 * np.sin(ang) + rng.normal(0, 0.035), -1.4762 + 0.32 * np.cos(ang) + rng.normal(0, 0.055))
        l["ll"] = c
        names = rng.choice(len(streets), int(rng.integers(6, 11)), replace=False)
        l["pts"] = [("On or near " + streets[j], round(c[0] + rng.normal(0, 0.0016), 6), round(c[1] + rng.normal(0, 0.0024), 6))
                    for j in names]


STREETS = ["High Street", "Market Place", "Castle Street", "Church Lane", "Mill Lane", "Park Road", "Queen Street",
           "King Street", "Bridge Street", "London Road", "Victoria Road", "The Green", "Abbey Road", "Cathedral Close",
           "Sheep Street", "Union Street", "Albert Street", "Priory Road", "Chapel Street", "Mount Pleasant", "Grove Road",
           "Church Street", "Manor Road", "School Lane", "North Street", "West Street", "New Road", "Orchard Close",
           "The Crescent", "Springfield Road", "Windsor Road", "York Road", "Moor Lane", "Brook Street", "Hill Rise",
           "Supermarket", "Shopping Area", "Parking Area", "Petrol Station", "Sports/Recreation Area", "Nightclub",
           "Pedestrian Subway", "Further/Higher Educational Building", "Hospital", "Conference/Exhibition Centre",
           "Theatre/Concert Hall", "Bus/Coach Station", "Police Station"]


def shut(suite, t, close=None):
    if suite not in CLOSURES:
        return False
    c = (close or {}).get(suite, CLOSURES[suite][0])
    return c <= t < CLOSURES[suite][1]


def booking_suite(home, t_book, rng, close=None):
    """The ward's suite; the nearest when the ward's suite is full, and the host while the ward's suite is closed (a
    closed suite takes nobody's overflow)."""
    full = rng.random() < 0.006
    if shut(home, t_book, close):
        return CLOSURES[home][2]
    if full:
        return home if shut(NEAR[home], t_book, close) else NEAR[home]
    return home


def detention_draw(rng, gname, remanded):
    """The PACE clock in whole minutes, from detention being authorised to release, charge or transfer."""
    if remanded:
        h = min(float(np.exp(rng.normal(np.log(13.0), 0.45))), 70.0)
    elif rng.random() > LONG.get(gname, .05):
        h = min(float(np.exp(rng.normal(np.log(9.5), 0.62))), 95.5)
    else:
        h = float(rng.uniform(24.2, 70))
    return max(20, int(round(h * 60)))


def arrests(W, C, rng):
    """The force's arrest records: one row per arrest by a Calderwick officer, with co-arrests booked minutes apart,
    the booking suite (diverted when a suite is full, Wendle Cross's wards at Southfields during its refit), the
    PACE clock and the outcome. Returns the rows and the incidents (for the remand files)."""
    wc = wards_codes()
    groups = WD.TYPES + [WD.WARRANT_GROUP]
    rows, incidents = [], []
    for i, l in enumerate(W["lsoas"]):
        home = WD.SUITE_NOW[l["ward"]]
        travel_med = 35 if l["ward"] in WD.CITY else 50
        for k, (y, m) in enumerate(WD.MONTHS):
            ndays = (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.date(y, m, 1)).days
            counts = list(C["ar"][i][k]) + [int(C["wa"][i][k])]
            for gname, c in zip(groups, counts):
                left = int(c)
                while left > 0:
                    p = GROUP_SIZE.get(gname, [.95, .04, .01, 0]) if gname != WD.WARRANT_GROUP else [1, 0, 0, 0]
                    s = min(left, 1 + int(rng.choice(4, p=np.array(p) / sum(p))))
                    left -= s
                    t0 = dt.datetime(y, m, int(rng.integers(1, ndays + 1)), int(rng.choice(24, p=HOURS)),
                                     int(rng.integers(0, 60)))
                    lead_charge = None
                    inc = []
                    for j in range(s):
                        t_book = t0 + dt.timedelta(minutes=int(np.exp(rng.normal(np.log(travel_med), 0.35)))
                                                   + j * int(rng.integers(8, 26)))
                        suite = booking_suite(home, t_book, rng)
                        if j > 0 and inc:
                            suite = inc[0]["suite"]
                        age = AGES[int(rng.choice(6, p=AGE_P))]
                        sex = "M" if rng.random() < .84 else "F"
                        if gname == WD.WARRANT_GROUP:
                            out = "Produced at court on warrant" if rng.random() < .55 else "Handed to prison escort"
                            mins = max(30, int(round(float(np.exp(rng.normal(np.log(14.0), 0.5))) * 60)))
                        else:
                            if j > 0 and inc and inc[0]["out"] == "Charged - remanded in custody" and rng.random() < .8:
                                charged, rem = True, True
                            else:
                                # the courts remand more often where several were arrested together
                                charged = rng.random() < CHARGE[gname]
                                rem = charged and rng.random() < REMAND.get(gname, .06) * (2.4 if s > 1 else 1.0)
                            if charged:
                                out = "Charged - remanded in custody" if rem else "Charged - bailed to court"
                            else:
                                out = pick(rng, OTHER_OUT)
                            mins = detention_draw(rng, gname, rem)
                        rec = dict(lsoa=i, ward=l["ward"], ward_code=wc[l["ward"]], group=gname, t_arrest=t0,
                                   t_book=t_book, suite=suite, age=age, sex=sex, out=out, mins=mins)
                        inc.append(rec)
                    # co-defendants kept for court together go on the first-named defendant's file, each charged
                    # in turn after them
                    rem_ = [r for r in inc if r["out"] == "Charged - remanded in custody"]
                    if len(rem_) >= 2 and rng.random() < .85:
                        lead = rem_[0]
                        t_ch = charge_utc(lead)
                        for r in rem_[1:]:
                            t_ch = t_ch + dt.timedelta(minutes=int(rng.integers(6, 45)))
                            r["mins"] = int((t_ch - to_utc(r["t_book"])).total_seconds() // 60)
                            r["is_codef"] = True
                        lead["codefs"] = rem_[1:]
                    rows.extend(inc)
                    incidents.append(inc)
    rows.sort(key=lambda r: (r["t_arrest"], r["t_book"], r["lsoa"]))
    return rows, incidents


def arrest_refs(rows, rng):
    seq = collections.Counter()
    # the 2021 sequence carries on from January to March, before the extract starts
    seq[21] = sum(1 for r in rows if r["t_arrest"].year == 2022 and r["t_arrest"].month <= 3) + int(rng.integers(-60, 61))
    for r in rows:
        yy = r["t_arrest"].year % 100
        seq[yy] += 1
        r["ref"] = "ARR-%02d-%06d" % (yy, seq[yy])


def charge_utc(r):
    """The PACE clock is elapsed time, so the charge is the booking in UTC plus the clock."""
    return to_utc(r["t_book"]) + dt.timedelta(minutes=r["mins"])


def charge_time(r):
    return to_local(charge_utc(r))


CJU_FROM, CJU_TO = dt.datetime(2025, 3, 1), dt.datetime(2026, 5, 1)
REARREST = .12          # files keyed to the case's first arrest, the person having been released and arrested again


def remand_files(rows, rng):
    """The Criminal Justice Unit's remand files: one per case file prepared for a remand court, charges from
    1 March 2025 to 30 April 2026. A file carries the first-named defendant's charge time and the case's arrest
    reference: the arrest the person was charged on, or, where the person had been released under investigation or
    on bail and was arrested again before charge, the first arrest in the case."""
    files = [r for r in rows if r["out"] == "Charged - remanded in custody" and not r.get("is_codef")
             and CJU_FROM <= charge_time(r) < CJU_TO]
    earlier = collections.defaultdict(list)
    for r in rows:
        if r["out"] in ("Released under investigation", "Released on police bail"):
            earlier[(r["ward"], r["group"])].append(r)
    used = set()
    out = []
    for r in sorted(files, key=lambda r: charge_utc(r)):
        t_ch = charge_time(r)
        d = first_hearing(t_ch)
        lo, hi = (405, 470) if r["suite"] in ("Northgate", "Eastmoor") else (390, 450)
        hand = dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=int(rng.integers(lo, hi)))
        t_last = max([t_ch] + [charge_time(cd) for cd in r.get("codefs", [])])
        if hand <= t_last + dt.timedelta(minutes=40):
            hand = t_last + dt.timedelta(minutes=int(rng.integers(45, 90)))
        r["handover"] = hand
        for cd in r.get("codefs", []):
            cd["handover"] = hand
        r["linked"] = r["ref"]
        if not r.get("codefs") and rng.random() < REARREST:
            cands = [e for e in earlier[(r["ward"], r["group"])] if e["ref"] not in used
                     and dt.timedelta(days=7) <= r["t_arrest"] - e["t_arrest"] <= dt.timedelta(days=150)]
            if cands:
                e = cands[int(rng.integers(len(cands)))]
                used.add(e["ref"])
                r["linked"] = e["ref"]
        out.append(r)
    return out


# ---------------------------------------------------------------------------------------------------------------
def moves(own):
    """A closed suite took its last detainee before its closure; its team and the detainees still in its cells moved to
    the host suite the minute after that booking."""
    return {s: max(r["t_book"] for r in own if r["suite"] == s and r["t_book"] < c[0]) + dt.timedelta(minutes=1)
            for s, c in CLOSURES.items()}


def btp_detainees(W, C, rng, close):
    """The detainees British Transport Police officers book into the force's suites: the station's ward's suite.
    They are in the healthcare provider's export and in no force record."""
    out = []
    for name, ward, f in WD.STATIONS:
        home = WD.SUITE_NOW[ward]
        for k, (y, m) in enumerate(WD.MONTHS):
            ndays = (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.date(y, m, 1)).days
            for _ in range(int(C["ba"][name][k])):
                t = dt.datetime(y, m, int(rng.integers(1, ndays + 1)), int(rng.choice(24, p=HOURS)),
                                int(rng.integers(0, 60))) + dt.timedelta(minutes=int(rng.integers(20, 50)))
                out.append(dict(suite=booking_suite(home, t, rng, close), t_book=t))
    return out


CLIN = {"Northgate": (1001, 1024), "Eastmoor": (2001, 2016), "Southfields": (3001, 3022), "Wendle Cross": (4001, 4020)}
REF_RATE = {"Northgate": .44, "Eastmoor": .40, "Southfields": .38, "Wendle Cross": .41}


def _clinician(rng, team, role):
    lo, hi = CLIN[team]
    return "%s %d" % (role, int(rng.integers(lo, hi)))


def healthcare(own, btp, rng, close):
    """The custody healthcare provider's contact export, contacts from 1 April 2025 to 31 March 2026 (local time):
    one row per clinician contact, the suite column being the clinician's team base. A closed suite's team works at
    the host suite with the detainees moved there, and sees a share of the host's own detainees, until the suite
    reopens. An initial assessment running across the 07:00 or 19:00 handover is closed by the outgoing clinician and
    finished by the incoming one on a new line. A detainee back from the emergency department is assessed again."""
    lo, hi = dt.datetime(2025, 3, 31, 0, 0), dt.datetime(2026, 4, 1, 0, 0)
    dets = [dict(suite=r["suite"], t_book=r["t_book"]) for r in own if lo <= r["t_book"] < hi] + \
           [d for d in btp if lo <= d["t_book"] < hi]
    dets.sort(key=lambda d: (d["t_book"], d["suite"]))
    rows = []
    ep = 3_210_000 + int(rng.integers(0, 5000))
    for d in dets:
        if rng.random() > REF_RATE[d["suite"]]:
            continue
        ep += 1
        u = rng.random()                       # at a host suite, seen by the closed suite's team when u < its share
        role = "RN" if rng.random() < .72 else ("Paramedic" if rng.random() < .7 else "FME")
        start = d["t_book"] + dt.timedelta(minutes=int(np.exp(rng.normal(np.log(48), 0.5))))
        dur = int(rng.integers(14, 38))
        lines = [(start, dur, "Initial health assessment")]
        t = start + dt.timedelta(minutes=dur)
        hospital = rng.random() < .03
        if hospital:
            back = t + dt.timedelta(minutes=int(rng.integers(150, 420)))
            lines.append((back, int(rng.integers(14, 30)), "Initial health assessment"))
            t = back + dt.timedelta(minutes=30)
        if rng.random() < .30:
            lines.append((t + dt.timedelta(minutes=int(rng.integers(60, 360))), int(rng.integers(5, 15)), "Medication"))
        if rng.random() < .15:
            lines.append((t + dt.timedelta(minutes=int(rng.integers(240, 720))), int(rng.integers(8, 20)), "Review"))
        if rng.random() < .10:
            lines.append((t + dt.timedelta(minutes=int(rng.integers(90, 600))), int(rng.integers(10, 25)), "Fitness to interview"))
        clin = {}
        for n, (s, du, kind) in enumerate(sorted(lines)):
            e = s + dt.timedelta(minutes=du)
            place = d["suite"]
            if place in CLOSURES and shut(place, s, close):
                place = CLOSURES[place][2]          # moved with the team when the suite closed
            team = place
            for cs, (c0, c1, host, share) in CLOSURES.items():
                if place == host and shut(cs, s, close) and (u < share or d["suite"] == cs):
                    team = cs
            if kind == "Initial health assessment" and n == 0 and hospital:
                outcome = "Conveyed to emergency department"
            elif kind == "Initial health assessment":
                outcome = "Fit to detain" if rng.random() < .8 else "Fit to detain with care plan"
            elif kind == "Fitness to interview":
                outcome = "Fit to interview" if rng.random() < .88 else "Not fit to interview"
            elif kind == "Medication":
                outcome = "Medication given"
            else:
                outcome = "Advice given"
            if team not in clin:
                clin[team] = _clinician(rng, team, role)
            split = None
            for hh in (7, 19):
                cut = s.replace(hour=hh, minute=0)
                if s < cut < e and kind == "Initial health assessment":
                    split = cut
            base = dict(ep=ep, team=team, place=place, kind=kind, outcome=outcome, booked=d["suite"], t_book=d["t_book"],
                        hospital=hospital)
            if split is not None:
                inc = clin[team]
                while inc == clin[team]:
                    inc = _clinician(rng, team, role)
                rows.append(dict(base, clin=clin[team], start=s, end=split, part=1))
                rows.append(dict(base, clin=inc, start=split, end=e, part=2))
            else:
                rows.append(dict(base, clin=clin[team], start=s, end=e, part=0))
    rows = [r for r in rows if lo + dt.timedelta(days=1) <= r["start"] < hi]
    rows.sort(key=lambda r: (r["start"], r["team"], r["ep"]))
    n = 40_118_000 + int(rng.integers(0, 900))
    for r in rows:
        n += int(rng.integers(1, 4))
        r["ref"] = "HC%08d" % n
    return rows


# ---------------------------------------------------------------------------------------------------------------
PO_SUSPECT = [("Unable to prosecute suspect", .30), ("Investigation complete; no suspect identified", .16),
              ("Awaiting court outcome", .11), ("Court result unavailable", .07), ("Local resolution", .08),
              ("Offender given a caution", .05), ("Further investigation is not in the public interest", .05),
              ("Formal action is not in the public interest", .03), ("Action to be taken by another organisation", .04),
              ("Under investigation", .11)]
PO_NOSUSPECT = [("Investigation complete; no suspect identified", .62), ("Unable to prosecute suspect", .15),
                ("Under investigation", .09), ("Awaiting court outcome", .04), ("Court result unavailable", .03),
                ("Local resolution", .03), ("Further investigation is not in the public interest", .04)]
PO_DRUGS = [("Local resolution", .24), ("Offender given a drugs possession warning", .12), ("Awaiting court outcome", .14),
            ("Court result unavailable", .10), ("Unable to prosecute suspect", .14), ("Offender given a caution", .08),
            ("Formal action is not in the public interest", .06), ("Under investigation", .12)]
NOSUSPECT = {"Burglary", "Criminal damage and arson", "Theft from the person", "Other theft", "Vehicle crime", "Bicycle theft"}


def street_crime(W, C, rng):
    """data.police.uk street-level crime in the force area, April 2025 to March 2026: Calderwick Police's rows and
    British Transport Police's at the stations, anti-social behaviour removed, as the partnership stacks it."""
    crow = []
    for i, l in enumerate(W["lsoas"]):
        for k in WD.K25:
            for t, c in zip(WD.TYPES, C["fc"][i][k]):
                crow.extend([("Calderwick Police", k, l, t, None)] * int(c))
    st = {l["station"]: l for l in W["lsoas"] if "station" in l}
    for name, ward, f in WD.STATIONS:
        l = st[name]
        pt = ("On or near %s (station)" % name, round(l["ll"][0] + rng.normal(0, 0.0012), 6),
              round(l["ll"][1] + rng.normal(0, 0.0018), 6))
        for k in WD.K25:
            for t, c in zip(WD.TYPES, C["bc"][name][k]):
                crow.extend([("British Transport Police", k, l, t, pt)] * int(c))
    pol = []
    for rep, k, l, t, pt in crow:
        y, m = WD.MONTHS[k]
        if pt is None:
            pt = l["pts"][int(rng.integers(len(l["pts"])))]
        tab = PO_DRUGS if t == "Drugs" else (PO_NOSUSPECT if t in NOSUSPECT else PO_SUSPECT)
        oc = pick(rng, tab)
        if k >= 57 and oc != "Investigation complete; no suspect identified" and rng.random() < 0.35:
            oc = "Under investigation"
        pol.append(("%064x" % int.from_bytes(hashlib.sha256(rng.bytes(16)).digest(), "big"), "%d-%02d" % (y, m), rep, rep,
                    pt[2], pt[1], pt[0], l["code"], l["name"], t, oc, ""))
    pol.sort(key=lambda r: (r[1], r[2], r[7]))
    return pol
