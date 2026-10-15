"""The county systems' exports, written from the clean world: the clerk's two first-appearance exports (the legacy
system to 3 March 2024, the new one from 4 March) and the new system's charge rows, Pretrial Services' screens, the
Sheriff's jail bookings (UTC), the state arrest extract, the court case index and the year's court events, the
monitoring vendor's invoice lines and Halsey County's board bills. Identifiers are issued in time order the way each
system issues them."""
from __future__ import annotations

import datetime as dt

import numpy as np

import catalog as C
import common as K

DAY = dt.timedelta(days=1)

FA_LEGACY_COLS = ["APPEARANCE_NO", "CASE_NOS", "DEF_LAST", "DEF_FIRST", "DEF_MI", "DOB", "SEX", "SID", "BOOKING_NO",
                  "APPEAR_DATE", "APPEAR_TIME", "MAG", "CHARGE_CODES", "HOLD_OTHER", "CONDITION", "BOND_AMT",
                  "PTS_SCREEN"]
FA_NEW_COLS = ["fa_id", "party_id", "defendant_last", "defendant_first", "defendant_middle", "dob", "sid",
               "booking_number", "appearance_at", "judicial_official_id", "lead_case_number", "detainer_agency",
               "release_condition", "bond_amount", "pts_screened"]
CHG_COLS = ["fa_id", "case_number", "charge_seq", "offense_code", "offense_description", "offense_class"]
SCREEN_COLS = ["screen_id", "booking_number", "screened_at", "sid", "last_name", "first_name", "dob",
               "age_22_or_under", "pending_charge", "prior_misd_conviction", "prior_felony_conviction",
               "prior_violent_conviction", "prior_incarceration", "nca_points", "nca_score", "prior_conviction",
               "fta_past_2_years", "fta_older", "fta_points", "fta_score", "screener"]
JAIL_COLS = ["booking_number", "booking_type", "sid", "inmate_name", "dob", "booked_utc", "released_utc",
             "release_type", "facility"]
ARREST_COLS = ["arrest_id", "sid", "last_name", "first_name", "dob", "arrest_date", "offense_date", "arrest_type",
               "offense_code", "offense_description", "arresting_agency", "arrest_county"]
CASE_COLS = ["case_number", "court", "filed_date", "party_id", "defendant_name", "dob", "disposition_date",
             "disposition_code", "district_case_ref"]
EVENT_COLS = ["event_id", "case_number", "event_date", "event_code", "courtroom"]
EM_COLS = ["invoice_month", "participant_no", "last_name", "first_name", "dob", "court_case", "enroll_date",
           "end_date", "billable_days", "daily_rate", "amount"]

AGENCIES = [("GARRISON PD", 0.42), ("DORRANCE CO SO", 0.27), ("MILLBROOK PD", 0.09), ("NC STATE HWY PATROL", 0.08),
            ("WESTFIELD PD", 0.06), ("DORRANCE CO ABC LAW ENF", 0.02), ("UNIVERSITY PD", 0.03), ("ASHBY PD", 0.03)]
OTHER_COUNTIES = [("WAKE", "RALEIGH PD"), ("DURHAM", "DURHAM PD"), ("GUILFORD", "GREENSBORO PD"),
                  ("HALSEY", "HALSEY CO SO"), ("JOHNSTON", "JOHNSTON CO SO"), ("ALAMANCE", "BURLINGTON PD"),
                  ("ORANGE", "CHAPEL HILL PD"), ("CHATHAM", "CHATHAM CO SO"), ("HARNETT", "HARNETT CO SO")]
DETAINERS = ["ICE", "US MARSHALS", "WAKE CO SO", "GUILFORD CO SO", "NC DAC (PROBATION)", "DURHAM CO SO"]
SCREENERS = ["AKB", "JLW", "TRM", "DCS", "MPH", "RNV", "SLG", "KEO", "BWJ"]
EM_RATE = 9.75
HALSEY_RATE = 68.00


class Ids:
    """Every identifier the systems issue, in time order."""


def issue_ids(W):
    I = Ids()
    eps = W.eps
    # jail bookings: the intake bookings, annex, return and order-for-arrest bookings, numbered by year in time order
    W.jail_rows = []
    for e in eps:
        for s in e["stays"]:
            if s["where"] == "DC":
                W.jail_rows.append(dict(kind="stay", e=e, s=s, t=s["start"]))
    for o in W.ofa_bookings:
        W.jail_rows.append(dict(kind="ofa", o=o, t=o["start"]))
    W.jail_rows.sort(key=lambda x: (x["t"], x["kind"], x.get("e", {}).get("eid", 0) if x["kind"] == "stay" else x["o"]["k"]))
    seq = {}
    for j in W.jail_rows:
        y = j["t"].year
        seq[y] = seq.get(y, 0) + 1
        j["bk"] = "B%02d-%06d" % (y % 100, seq[y] + 1200)
    for e in eps:
        e["booking_no"] = None
    for j in W.jail_rows:
        if j["kind"] == "stay" and j["s"]["btype"] == "NEW":
            j["e"]["booking_no"] = j["bk"]
    # district and superior case numbers by filing year
    order = sorted(W.cases, key=lambda c: (c["filed"], c["cid"]))
    seqd, seqs = {}, {}
    for c in order:
        y = c["filed"].year
        if c["court"] == "D":
            seqd[y] = seqd.get(y, 0) + 1
            c["no"] = "%02dCR%06d" % (y % 100, seqd[y] + 3000)
        else:
            seqs[y] = seqs.get(y, 0) + 1
            c["no"] = "%02dCRS%06d" % (y % 100, seqs[y] + 400)
    # party numbers: the new system's party record per person; superior court intake opens its own record for most
    r = K.rng("ids")
    pids = sorted({e["pid"] for e in eps})
    perm = r.permutation(len(pids))
    W.party = {pid: "P%07d" % (1800000 + 13 * int(perm[k]) + int(r.integers(0, 9))) for k, pid in enumerate(pids)}
    W.legacy_party = {pid: "%06d" % (410000 + 7 * int(perm[k]) + int(r.integers(0, 5))) for k, pid in enumerate(pids)}
    sup_seq = 0
    for c in order:
        if c["court"] == "S":
            if r.random() < 0.72:
                sup_seq += 1
                c["party"] = "P%07d" % (5600000 + 11 * sup_seq + int(r.integers(0, 7)))
            else:
                c["party"] = W.party[c["pid"]]
        else:
            c["party"] = W.party[c["pid"]]
    # appearance numbers
    fa_order = sorted(eps, key=lambda e: (e["fa_t"], e["eid"]))
    for k, e in enumerate(fa_order):
        e["fa_key"] = ("%07d" % (3150000 + k)) if e["fa_t"].date() < K.CMS_CHANGE else ("FA%09d" % (240000000 + 3 * k))
    # screens
    scr = sorted((e for e in eps if e["screened"]), key=lambda e: (e["screen_t"], e["eid"]))
    for k, e in enumerate(scr):
        e["screen_id"] = "S%08d" % (60100000 + 2 * k + int(r.integers(0, 2)))
    return I


def ofa_and_orders(W):
    """Orders for arrest after each failure to appear: most are served by an arrest within weeks (an arrest of type
    OFA in the state extract and a short jail booking), some are recalled when the defendant comes in, a few are
    returned unserved and reissued for the same date."""
    r = K.rng("ofa")
    W.ofa_bookings, W.orders = [], []
    for k, cd in enumerate(W.court):
        if not cd["fta"]:
            continue
        c = W.cases[cd["cid"]]
        o = dict(k=k, cid=cd["cid"], date=cd["date"], pid=cd["pid"], reissued=r.random() < 0.05)
        u = r.random()
        if u < 0.16:
            o["recalled"] = cd["date"] + dt.timedelta(days=int(r.integers(0, 15)))
            o["served"] = None
        else:
            o["recalled"] = None
            o["served"] = cd["date"] + dt.timedelta(days=int(min(200, r.exponential(18)) + 1))
        W.orders.append(o)
        if o["served"] and o["served"] <= K.EXTRACT_END:
            t = K.d2dt(o["served"], int(r.integers(0, 24)), int(r.integers(0, 60)))
            dur = dt.timedelta(hours=float(r.uniform(3, 30)))
            W.ofa_bookings.append(dict(k=len(W.ofa_bookings), pid=cd["pid"], start=t, end=t + dur,
                                       rtype=str(r.choice(["BOND", "WPA", "UNSEC"], p=[0.45, 0.35, 0.20])), cid=cd["cid"]))
            W.arrests.append(dict(pid=cd["pid"], t=t, offence_date=cd["date"], codes=[c["codes"][0]], type="OFA",
                                  county=K.COUNTY, ep=None))


# ---------------------------------------------------------------------------------------------------- formats
def name_upper(p):
    return p.last.upper(), p.first.upper(), p.middle[0].upper()


def us_date(d):
    return d.strftime("%m/%d/%Y")


def us_time12(t):
    h = t.hour % 12 or 12
    return "%02d/%02d/%04d %02d:%02d %s" % (t.month, t.day, t.year, h, t.minute, "AM" if t.hour < 12 else "PM")


def utc_iso(t_local):
    return K.eastern_to_utc(t_local).strftime("%Y-%m-%dT%H:%M:%SZ")


def legacy_case(no):
    return no[:4] + " " + no[4:]


def fa_rows(W):
    r = K.rng("fa_rows")
    P = W.persons
    legacy, new, charges = [], [], []
    cond_l = {"WRITTEN_PROMISE": "WPA", "UNSECURED": "UNSEC", "CUSTODY": "CUST", "SECURED": "SEC"}
    cond_n = {"WRITTEN_PROMISE": "WRITTEN_PROMISE", "UNSECURED": "UNSECURED_BOND", "CUSTODY": "CUSTODY_RELEASE",
              "SECURED": "SECURED_BOND"}
    for e in sorted(W.eps, key=lambda e: (e["fa_t"], e["eid"])):
        p = P[e["pid"]]
        cs = [W.cases[c] for c in e["cases"] if W.cases[c]["court"] == "D"]
        m = W.mags[e["mag"]]
        if e["fa_t"].date() < K.CMS_CHANGE:
            last, first, mi = name_upper(p)
            codes = []
            for c in e["codes"]:
                lc = C.BY_CODE[c][1]
                codes.append(lc[int(r.integers(0, len(lc)))] if len(lc) > 1 else lc[0])
            legacy.append({"APPEARANCE_NO": e["fa_key"], "CASE_NOS": ";".join(legacy_case(c["no"]) for c in cs),
                           "DEF_LAST": last, "DEF_FIRST": first, "DEF_MI": mi, "DOB": us_date(p.dob), "SEX": p.sex,
                           "SID": p.sid, "BOOKING_NO": e["booking_no"][1:3] + e["booking_no"][4:],
                           "APPEAR_DATE": us_date(e["fa_t"].date()), "APPEAR_TIME": e["fa_t"].strftime("%H:%M"),
                           "MAG": m["initials"], "CHARGE_CODES": ";".join(codes),
                           "HOLD_OTHER": "Y" if e["detainer"] else "N", "CONDITION": cond_l[e["cond"]],
                           "BOND_AMT": e["bond"] if e["bond"] else "", "PTS_SCREEN": "Y" if e["screened"] else "N"})
        else:
            new.append({"fa_id": e["fa_key"], "party_id": W.party[e["pid"]], "defendant_last": p.last,
                        "defendant_first": p.first, "defendant_middle": p.middle, "dob": p.dob.isoformat(),
                        "sid": p.sid, "booking_number": e["booking_no"],
                        "appearance_at": e["fa_t"].strftime("%Y-%m-%d %H:%M"), "judicial_official_id": m["empno"],
                        "lead_case_number": cs[0]["no"],
                        "detainer_agency": DETAINERS[int(r.integers(0, len(DETAINERS)))] if e["detainer"] else "",
                        "release_condition": cond_n[e["cond"]], "bond_amount": e["bond"] if e["bond"] else "",
                        "pts_screened": "TRUE" if e["screened"] else "FALSE"})
            seq = 0
            for c in cs:
                for code in c["codes"]:
                    seq += 1
                    o = C.BY_CODE[code]
                    charges.append({"fa_id": e["fa_key"], "case_number": c["no"], "charge_seq": seq,
                                    "offense_code": code, "offense_description": o[3], "offense_class": o[4]})
    return legacy, new, charges


def screen_rows(W):
    r = K.rng("screen_rows")
    P = W.persons
    out = []
    for e in sorted((e for e in W.eps if e["screened"]), key=lambda e: (e["screen_t"], e["eid"])):
        p = P[e["pid"]]
        it, ft = e["nca_items"], e["fta_items"]
        paper = r.random() < 0.03
        out.append({"screen_id": e["screen_id"], "booking_number": "" if paper else e["booking_no"],
                    "screened_at": us_time12(e["screen_t"]), "sid": p.sid, "last_name": p.last.upper(),
                    "first_name": p.first.upper(), "dob": us_date(p.dob),
                    "age_22_or_under": it["age_22_or_under"], "pending_charge": it["pending_charge"],
                    "prior_misd_conviction": it["prior_misd_conviction"],
                    "prior_felony_conviction": it["prior_felony_conviction"],
                    "prior_violent_conviction": it["prior_violent_conviction"],
                    "prior_incarceration": it["prior_incarceration"], "nca_points": e["nca_raw"],
                    "nca_score": e["nca"], "prior_conviction": ft["prior_conviction"],
                    "fta_past_2_years": ft["fta_past_2_years"], "fta_older": ft["fta_older"],
                    "fta_points": e["fta_raw"], "fta_score": e["fta"],
                    "screener": SCREENERS[int(r.integers(0, len(SCREENERS)))]})
    return out


def jail_rows(W):
    P = W.persons
    out = []
    end_t = K.d2dt(K.EXTRACT_END + DAY)
    for j in W.jail_rows:
        if j["kind"] == "stay":
            s, e = j["s"], j["e"]
            p = P[e["pid"]]
            btype, rtype = s["btype"], s["rtype"]
            start, stop = s["start"], s["end"]
        else:
            o = j["o"]
            p = P[o["pid"]]
            btype, rtype, start, stop = "OFA", o["rtype"], o["start"], o["end"]
        if start >= end_t:
            continue
        rel = utc_iso(stop) if stop < end_t else ""
        out.append({"booking_number": j["bk"], "booking_type": btype, "sid": p.sid,
                    "inmate_name": "%s, %s %s" % (p.last.upper(), p.first.upper(), p.middle[0].upper()),
                    "dob": p.dob.isoformat(), "booked_utc": utc_iso(start), "released_utc": rel,
                    "release_type": (rtype if rel else ""), "facility": j["s"]["fac"] if j["kind"] == "stay" else "DCDC"})
    return out


def arrest_rows(W):
    r = K.rng("arrest_rows")
    P = W.persons
    ag_names = [a for a, _ in AGENCIES]
    ag_w = np.array([w for _, w in AGENCIES])
    ag_w /= ag_w.sum()
    rows = []
    arr = sorted(W.arrests, key=lambda a: (a["t"], a["pid"]))
    end_t = K.d2dt(K.EXTRACT_END + DAY)
    n = 0
    for a in arr:
        if a["t"] >= end_t:
            continue
        n += 1
        p = P[a["pid"]]
        if a["county"] == K.COUNTY:
            agency, county = ag_names[int(r.choice(len(ag_names), p=ag_w))], "DORRANCE"
        else:
            county, agency = OTHER_COUNTIES[int(r.integers(0, len(OTHER_COUNTIES)))]
        aid = "%02d%07d" % (a["t"].year % 100, 1000000 + 37 * n)
        for code in a["codes"]:
            o = C.BY_CODE[code]
            rows.append({"arrest_id": aid, "sid": p.sid, "last_name": p.last.upper(), "first_name": p.first.upper(),
                         "dob": p.dob.isoformat(), "arrest_date": a["t"].date().isoformat(),
                         "offense_date": a["offence_date"].isoformat(), "arrest_type": a["type"],
                         "offense_code": code, "offense_description": o[3] if a["type"] != "OFA" else "FAILURE TO APPEAR - " + o[3],
                         "arresting_agency": agency, "arrest_county": county})
    return rows


def case_rows(W):
    P = W.persons
    out = []
    for c in sorted(W.cases, key=lambda c: (c["filed"], c["cid"])):
        if c["filed"].date() > K.EXTRACT_END:
            continue                # an indictment returned after the extract: not yet in the index
        p = P[c["pid"]]
        disposed = c["disposed"] if c["disposed"] <= K.EXTRACT_END else None
        out.append({"case_number": c["no"], "court": "DISTRICT" if c["court"] == "D" else "SUPERIOR",
                    "filed_date": c["filed"].date().isoformat(), "party_id": c["party"],
                    "defendant_name": "%s, %s %s" % (p.last.upper(), p.first.upper(), p.middle[0].upper()),
                    "dob": p.dob.isoformat(), "disposition_date": disposed.isoformat() if disposed else "",
                    "disposition_code": c["code"] if disposed else "",
                    "district_case_ref": W.cases[c["parent"]]["no"] if c["court"] == "S" else ""})
    return out


def event_rows(W):
    """The court events of 1 October 2025 to 30 September 2026: each setting, each order for arrest for a failure to
    appear (and its recall, reissue or service), each disposition."""
    r = K.rng("event_rows")
    ev = []
    lo, hi = K.FY26_START, K.EXTRACT_END
    room = {}
    for cd in W.court:
        if lo <= cd["date"] <= hi:
            c = W.cases[cd["cid"]]
            if c["cid"] not in room:
                room[c["cid"]] = ("%dA" % int(r.integers(1, 6))) if c["court"] == "D" else ("%d" % int(r.integers(1, 4)))
            ev.append((cd["date"], c["no"], "SET", room[c["cid"]]))
    for o in W.orders:
        c = W.cases[o["cid"]]
        rm = room.get(c["cid"], "1A")
        if lo <= o["date"] <= hi:
            ev.append((o["date"], c["no"], "FTA", rm))
            if o["reissued"]:
                d2 = o["date"] + dt.timedelta(days=int(r.integers(20, 45)))
                if d2 <= hi:
                    ev.append((d2, c["no"], "OFARI", rm))
        if o["recalled"] and lo <= o["recalled"] <= hi:
            ev.append((o["recalled"], c["no"], "OFAR", rm))
        if o["served"] and lo <= o["served"] <= hi:
            ev.append((o["served"], c["no"], "OFAS", rm))
    for c in W.cases:
        if lo <= c["disposed"] <= hi:
            ev.append((c["disposed"], c["no"], "DISP", room.get(c["cid"], "1A" if c["court"] == "D" else "1")))
    ev.sort()
    rows = []
    for k, (d, no, code, rm) in enumerate(ev):
        rows.append({"event_id": "E%09d" % (510000000 + 4 * k), "case_number": no, "event_date": d.isoformat(),
                     "event_code": code, "courtroom": rm})
    return rows


def em_rows(W):
    """Sentry Point's monthly invoice lines: one line per enrollment per month it was active, billed a day or part of a
    day, the enrollment's own dates on every line."""
    r = K.rng("em_rows")
    P = W.persons
    lines = []
    ens = sorted(W.em, key=lambda x: (x["start"], x["eid"]))
    for k, en in enumerate(ens):
        en["participant"] = "SP%06d" % (318000 + 3 * k + int(r.integers(0, 3)))
        en["case_blank"] = r.random() < 0.12
    for en in ens:
        e = W.eps[en["eid"]]
        p = P[en["pid"]]
        dcase = [W.cases[c]["no"] for c in e["cases"] if W.cases[c]["court"] == "D"][0]
        end = en["end"] or K.EXTRACT_END
        m = dt.date(en["start"].year, en["start"].month, 1)
        while m <= end and m <= K.EXTRACT_END:
            m_end = (dt.date(m.year + (m.month == 12), 1 if m.month == 12 else m.month + 1, 1)) - DAY
            a = max(en["start"], m)
            b = min(end, m_end)
            days = (b - a).days + 1
            lines.append({"invoice_month": m.strftime("%Y-%m"), "participant_no": en["participant"],
                          "last_name": p.last, "first_name": p.first, "dob": us_date(p.dob),
                          "court_case": "" if en["case_blank"] else dcase,
                          "enroll_date": us_date(en["start"]),
                          "end_date": us_date(en["end"]) if en["end"] and en["end"] <= m_end else "",
                          "billable_days": days, "daily_rate": "%.2f" % EM_RATE, "amount": "%.2f" % (days * EM_RATE)})
            m = m_end + DAY
    lines.sort(key=lambda x: (x["invoice_month"], x["participant_no"]))
    return lines


def halsey_stays(W):
    """Halsey County's own record of every Dorrance defendant it boarded: its booking number, the dates in and out."""
    r = K.rng("halsey")
    out = []
    for e in W.eps:
        for s in e["stays"]:
            if s["where"] == "HC":
                out.append(dict(e=e, s=s))
    out.sort(key=lambda x: (x["s"]["start"], x["e"]["eid"]))
    for k, h in enumerate(out):
        h["hbk"] = "HC%02d%05d" % (h["s"]["start"].year % 100, 30100 + 7 * k + int(r.integers(0, 6)))
        h["ref_blank"] = r.random() < 0.3
    return out
