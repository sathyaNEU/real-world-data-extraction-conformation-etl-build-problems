"""task179 exports: each file in the layout, clock and code set its own system writes."""
from __future__ import annotations

import datetime as dt
import os
from zoneinfo import ZoneInfo

import numpy as np

import codes as K
import common as C
import names as NM
import xlsx_writer as XW

TZ = ZoneInfo("America/Chicago")
UTC = dt.timezone.utc
TD = dt.timedelta
GPS_EXPORTED = dt.datetime(2027, 1, 4, 15, 12, 44, tzinfo=dt.timezone.utc)

CLOSE_TEXT = {"EXPIRED": "EXPIRATION OF SENTENCE", "DISCHARGED EARLY": "EARLY DISCHARGE",
              "REVOKED": "REVOKED - COMMITTED TO MDOC", "DECEASED": "DECEASED"}
NIBRS = {"13A": "AGGRAVATED ASSAULT", "13A-F": "AGGRAVATED ASSAULT", "13B": "SIMPLE ASSAULT", "13C": "INTIMIDATION",
         "120": "ROBBERY", "09A": "MURDER/NONNEGLIGENT MANSLAUGHTER", "11A": "RAPE", "100": "KIDNAPPING/ABDUCTION",
         "520": "WEAPON LAW VIOLATIONS"}
OLD_TITLE = {}
for _r in K.ROWS:
    OLD_TITLE[_r[0]] = _r[2]


def to_utc(t):
    return t.replace(tzinfo=TZ).astimezone(UTC)


SPELLED = {"ST": "STREET", "AVE": "AVENUE", "DR": "DRIVE", "RD": "ROAD", "LN": "LANE", "CT": "COURT", "PL": "PLACE",
           "BLVD": "BOULEVARD"}


NOTE_FORMS = {
    "SUSPEND": (["client in custody", "in custody", "custody", "jail hold per officer", "booked", "officer request", ""],
                [0.36, 0.15, 0.14, 0.07, 0.06, 0.05, 0.17]),
    "RESUME": (["released", "client released", ""], [0.12, 0.06, 0.82]),
    "VOID": (["duplicate entry", "entered twice", "dup", "duplicate", "keyed in error", ""], [0.42, 0.16, 0.1, 0.12, 0.08, 0.12]),
    "ACCOUNT_TRANSFER": (["moved to receiving region account", "transfer of supervision", "region transfer", ""],
                         [0.5, 0.2, 0.15, 0.15]),
    "DEVICE_ISSUE": (["replacement unit", ""], [0.08, 0.92]),
}


def gps_note(event, note, r):
    """the note column as the officers and the vendor's desk fill it: several wordings of one reason, often none"""
    if event == "DEVICE_RETURN":
        return note if r.random() < 0.88 else ""
    if event in NOTE_FORMS:
        forms, p = NOTE_FORMS[event]
        return forms[int(r.choice(len(forms), p=p))]
    return note


def retype(addr, r):
    """a residence as another officer types it: the unit mark or the street type written the other way"""
    toks = addr.split()
    unit = next((k for k, t in enumerate(toks) if t in ("APT", "UNIT") or t.startswith("#")), None)
    if unit is not None and r.random() < 0.6:
        t = toks[unit]
        if t.startswith("#"):
            toks[unit:unit + 1] = ["APT", t[1:]]
        else:
            toks[unit:unit + 2] = ["#" + (toks[unit + 1] if unit + 1 < len(toks) else "")]
        return " ".join(toks)
    back = {v: k for k, v in SPELLED.items()}
    for k in range(len(toks) - 1, 0, -1):
        if toks[k] in SPELLED:
            toks[k] = SPELLED[toks[k]]
            return " ".join(toks)
        if toks[k] in back:
            toks[k] = back[toks[k]]
            return " ".join(toks)
    return addr


def code_for(new, when, jail=None):
    """the section a record carries: the former section before the recodification took effect, or in the Keswick jail's
    charge table until its update of 1 April 2025"""
    cut = C.RECODIFIED if jail != "K" else dt.date(2025, 4, 1)
    if when < cut:
        return K.NEW[new][0]
    return new


def title_for(code):
    if code in K.NEW:
        return K.NEW[code][2]
    return OLD_TITLE[code]


def proper(s):
    out = []
    for part in s.split("-"):
        if part.startswith("O'"):
            out.append("O'" + part[2:].capitalize())
        else:
            out.append(part.capitalize())
    return "-".join(out)


class Pack:
    def __init__(self, w, ev):
        self.w, self.ev = w, ev
        self.r = C.stream("layout")

    # ------------------------------------------------------------------ case management
    def write_episodes(self, out):
        w, ev, r = self.w, self.ev, self.r
        rows = []
        epid = r.choice(np.arange(10_000_000, 99_999_999), size=len(ev.episodes), replace=False)
        self.episode_rows = []
        for k, e in enumerate(sorted(ev.episodes, key=lambda x: (x["start"], x["p"]))):
            if e["start"] > C.RECORDS_END or (e["end"] is not None and e["end"] < C.RECORDS_START):
                continue
            i = e["p"]
            end = e["end"] if (e["end"] is not None and e["end"] <= C.RECORDS_END) else None
            why = ""
            if end is not None:
                if e["why"] == "TRANSFERRED - COUNTY":
                    why = "TRANSFER - %s COUNTY" % ("KESWICK" if e["county"] == 0 else "DARROW")
                elif e["why"] == "TRANSFER OUT":
                    why = "TRANSFER - REGION %d" % [1, 2, 3, 5, 6][int(r.integers(5))]
                else:
                    why = CLOSE_TEXT.get(e["why"], "EXPIRATION OF SENTENCE")
            county = "DARROW" if e["county"] == 0 else "KESWICK"
            if e["county"] == 0 and w.city[i]:
                office = "HALVERTON NORTH" if w.dist[i] in (1, 2) else "HALVERTON SOUTH"
                rescity = "Halverton"
            elif e["county"] == 0:
                office = "DARROW RURAL"
                rescity = ev.addr[i][4] if ev.addr[i][4] != "Halverton" else "Pell Junction"
            else:
                office = "KESWICK"
                rescity = ev.addr[i][4] if ev.addr[i][4] in NM.TOWNS_KESWICK else "Keswick"
            lead = e["lead"]
            conv = e["start"] if e["first_seg"] else e["start"]
            code = code_for(lead, conv)
            legacy = ev.oms.get(i, [""])[0] if e["start"] < C.MIGRATION else ""
            pri = int(w.priors[i]) + sum(1 for x in ev.person_eps[i] if x["start"] < e["start"] and x["first_seg"]
                                          and not x.get("concurrent") and x["why"] == "REVOKED")
            eth = "H" if w.hispanic[i] else "N"
            race = ["W", "B", "W", "A"][int(w.race[i])]
            rows.append([int(ev.pid[i]), ev.sid[i], ev.last[i], ev.first[i], ev.middle[i], ev.suffix[i],
                         ev.dob[i].isoformat(), "M" if w.male[i] else "F", race, eth, "E%d" % int(epid[k]), e["case"],
                         "PAROLE" if e["parole"] else "PROBATION", county, office, rescity, e["start"].isoformat(),
                         (e["expires"] - TD(days=1)).isoformat(), C.iso(end), why, code, title_for(code), pri, legacy])
            self.episode_rows.append((e, rows[-1]))
        head = ["cms_person_id", "sid", "last_name", "first_name", "middle_name", "name_suffix", "date_of_birth", "sex",
                "race", "ethnicity", "episode_id", "court_case_number", "supervision_type", "county", "supervising_office",
                "residence_city", "start_date", "expiration_date", "close_date", "close_reason", "lead_offense_statute",
                "lead_offense_description", "prior_felony_convictions", "legacy_offender_number"]
        return C.write_csv(os.path.join(out, C.F_EPIS), head, rows)

    def write_crosswalk(self, out):
        ev, r = self.ev, self.r
        rows = []
        rn = C.stream("xwalk_notes")
        merged = ["MERGED DUPLICATE", "MERGED DUPLICATE - SAME SID", "DUPLICATE OMS RECORD MERGED", "MERGED INTO SURVIVING RECORD"]
        kept = ["NAME CORRECTED", "DOB CORRECTED", "MANUAL MATCH", "SID ADDED AT CONVERSION"]
        shown = set(e["p"] for e, _ in self.episode_rows)
        for i, nums in sorted(self.ev.oms.items(), key=lambda kv: kv[1][0]):
            if i not in shown:
                continue
            for j, n in enumerate(nums):
                d = dt.date(2022, 6, 11) if r.random() < 0.6 else dt.date(2022, 6, 12)
                if j > 0:
                    note = merged[int(rn.choice(4, p=[0.55, 0.2, 0.15, 0.1]))]
                else:
                    u = rn.random()
                    note = kept[int(rn.integers(4))] if u < 0.09 else ""
                rows.append([n, int(ev.pid[i]), d.isoformat(), note])
        rows.sort(key=lambda x: x[0])
        return C.write_csv(os.path.join(out, C.F_XWALK), ["legacy_offender_number", "cms_person_id", "converted_on",
                                                           "conversion_note"], rows)

    def write_assessments(self, out):
        ev, r = self.ev, self.r
        rows = []
        ids = r.choice(np.arange(3_000_000, 8_999_999), size=len(ev.assessments), replace=False)
        assessors = ["R4-%03d" % x for x in r.choice(np.arange(100, 999), size=64, replace=False)]
        for k, a in enumerate(sorted(ev.assessments, key=lambda x: (x["date"], x["p"]))):
            if a["date"] > C.RECORDS_END:
                continue
            i = a["p"]
            if a["date"] < C.MIGRATION:
                nums = ev.oms.get(i)
                if not nums:
                    continue
                ref = nums[-1] if (len(nums) > 1 and r.random() < 0.5) else nums[0]
            else:
                ref = str(int(ev.pid[i]))
            tot = a["total"]
            if a["v2"]:
                lvl = "LOW" if tot <= 12 else ("MODERATE" if tot <= 20 else ("HIGH" if tot <= 28 else "VERY HIGH"))
                inst = "MRAS-CS 2.0"
            else:
                lvl = "LOW" if tot <= 10 else ("MODERATE" if tot <= 18 else ("HIGH" if tot <= 26 else "VERY HIGH"))
                inst = "MRAS-CS 1.3"
            ov = ""
            if r.random() < 0.015:
                order = ["LOW", "MODERATE", "HIGH", "VERY HIGH"]
                j = order.index(lvl)
                ov = order[min(3, j + 1)] if r.random() < 0.7 else order[max(0, j - 1)]
                if ov == lvl:
                    ov = ""
            rows.append(["A%d" % int(ids[k]), ref, a["date"].isoformat(), inst] + a["parts"] + [tot, lvl, ov,
                                                                                                 assessors[int(r.integers(64))]])
        head = ["assessment_id", "offender_ref", "assessment_date", "instrument", "criminal_history",
                "education_employment", "family_social", "neighborhood", "substance_use", "peer_associations",
                "criminal_attitudes", "total_score", "risk_level", "override_level", "assessor"]
        return C.write_csv(os.path.join(out, C.F_ASSESS), head, rows)

    # ------------------------------------------------------------------ jails
    def _in_window(self, b):
        return C.RECORDS_START <= b["booked"].date() <= C.RECORDS_END

    def write_darrow(self, out):
        ev, r = self.ev, self.r
        rows = []
        for b in ev.bookings:
            if b["jail"] != "D" or not self._in_window(b):
                continue
            i = b["p"]
            when = b["booked"].date()
            case = b["case"]
            if isinstance(case, tuple):
                case = "%02d-%06d" % (case[1], case[2])
            out_by_extract = b["release"] is not None and b["release"].date() <= C.RECORDS_END
            rel = b["release"].strftime("%Y-%m-%d %H:%M") if out_by_extract else ""
            typ = {"NEW ARREST": "NEW ARREST", "WARRANT": "WARRANT - FTA", "RETURN FROM HOSPITAL": "RETURN FROM HOSPITAL",
                   "PROBATION/PAROLE VIOLATION": "SUPERVISION VIOLATION HOLD"}[b["type"]]
            base = [b["bid"], b["booked"].strftime("%Y-%m-%d %H:%M"), rel, b["release_reason"] if out_by_extract else "", ev.sid[i],
                    ev.last[i].upper(), ev.first[i].upper(), C.mdy(ev.dob[i]), typ, b["agency"], case]
            if b["type"] == "PROBATION/PAROLE VIOLATION" or not b["charges"]:
                rows.append(base + [1, "", "PROBATION/PAROLE VIOLATION", ""])
                continue
            for j, c in enumerate(b["charges"], 1):
                code = code_for(c, when, "D")
                rows.append(base + [j, code, title_for(code).upper(), K.LEVEL[c]])
        head = ["booking_no", "booked", "released", "release_reason", "sid", "last_name", "first_name", "dob",
                "booking_type", "arresting_agency", "agency_case_no", "charge_seq", "statute", "charge_description",
                "charge_level"]
        return C.write_csv(os.path.join(out, C.F_DARROW), head, rows)

    def write_keswick(self, out):
        ev = self.ev
        rows = []
        for b in ev.bookings:
            if b["jail"] != "K" or not self._in_window(b):
                continue
            i = b["p"]
            when = b["booked"].date()
            case = b["case"]
            if isinstance(case, tuple):
                case = "HPD%02d%06d" % (case[1], case[2])
            code = {"NEW ARREST": "NA", "WARRANT": "WT", "PROBATION/PAROLE VIOLATION": "PV", "RETURN FROM HOSPITAL": "RH"}[b["type"]]
            if b["type"] == "PROBATION/PAROLE VIOLATION" or not b["charges"]:
                ch = "PROB/PAROLE VIOLATION"
                lvl = ""
            else:
                parts = []
                for c in b["charges"]:
                    cc = code_for(c, when, "K")
                    parts.append("%s %s" % (cc, title_for(cc)))
                ch = " | ".join(parts)
                lv = [K.LEVEL[c] for c in b["charges"]]
                lvl = sorted(lv, key=lambda x: (x[0] != "F", int(x[1:])))[0]
            booked = to_utc(b["booked"]).replace(tzinfo=None)
            out_by_extract = b["release"] is not None and b["release"].date() <= C.RECORDS_END
            rel = to_utc(b["release"]).replace(tzinfo=None) if out_by_extract else None
            nm = ev.last[i].upper() + ", " + ev.first[i].upper() + ((" " + ev.middle[i][0].upper()) if ev.middle[i] else "")
            rows.append([b["bid"], booked, rel, b["release_reason"].title() if (b["release_reason"] and out_by_extract) else None, ev.sid[i],
                         nm, ev.dob[i], code, b["agency"], case, ch, lvl])
        head = ["Booking Number", "Booked (UTC)", "Released (UTC)", "Release Type", "SID", "Inmate Name", "DOB",
                "Reason", "Agency", "Agency Case", "Charges", "Top Level"]
        XW.write_table(os.path.join(out, C.F_KESWICK), "Bookings", head, rows,
                       widths=[13, 18, 18, 18, 12, 28, 11, 7, 7, 14, 70, 9], creator="Keswick County Sheriff's Office",
                       datetime_cols=(1, 2))
        return len(rows)

    # ------------------------------------------------------------------ Halverton police
    def victim_name(self, i, r):
        ev = self.ev
        last = ev.last[i].upper()
        if "-" in last and r.random() < 0.5:
            last = last.replace("-", " ")
        if last.startswith("O'") and r.random() < 0.5:
            last = last.replace("'", "")
        if ev.suffix[i] and r.random() < 0.7:
            last = last + " " + ev.suffix[i]
        first = ev.first[i].upper()
        if r.random() < 0.015 and ev.first[i] in NM.NICKNAMES:
            first = NM.NICKNAMES[ev.first[i]].upper()
        mid = ev.middle[i].upper() if ev.middle[i] else ""
        u = r.random()
        if mid and len(mid) > 1:
            mid = mid if u < 0.40 else (mid[0] if u < 0.75 else "")
        elif mid and u < 0.3:
            mid = ""
        return last + ", " + first + ((" " + mid) if mid else "")

    def write_hpd(self, out):
        ev, w = self.ev, self.w
        r = C.stream("hpd_layout")
        rt = C.stream("hpd_reentry")
        rows = []
        self.hpd_sup_rows = []
        for inc in ev.incidents:
            yy, n = inc["number"]
            num = "HPD-%02d-%06d" % (yy, n)
            offs = [("13A" if o == "13A-F" else o) for o in inc["offenses"]]
            vrows = []
            seq = 0
            home = {}
            for v in inc["victims"]:
                seq += 1
                if v["kind"] == "society":
                    vrows.append([seq, "S", "SOCIETY/PUBLIC", "", "", "", "", "", "", "", ""])
                    continue
                if v["kind"] == "business":
                    vrows.append([seq, "B", v["name"], "", "", "", "", "", "", "", ""])
                    continue
                if v["kind"] == "sup":
                    i = v["p"]
                    d = inc["occurred"].date()
                    age = (d - ev.dob[i]).days // 365
                    name = self.victim_name(i, r)
                    dob = C.mdy(ev.dob[i]) if r.random() >= 0.02 else ""
                    num_, st, t, unit = ev.addr[i][:4]
                    addr = "%d %s %s%s" % (num_, st.upper(), t.upper(), (" " + unit) if unit else "")
                    sex = "M" if w.male[i] else "F"
                    race = ["W", "B", "W", "A"][int(w.race[i])]
                    eth = "H" if w.hispanic[i] else "N"
                    city = "HALVERTON"
                    self.hpd_sup_rows.append((num, i, name, dob))
                else:
                    age = v["age"]
                    if age < 18:
                        vrows.append([seq, "I", "JUVENILE", "", age, "M" if v["male"] else "F", v["race"],
                                      "H" if v["hisp"] else "N", self._injury(offs[0], r), "", ""])
                        continue
                    mid = v["middle"].upper()
                    if mid and len(mid) > 1 and r.random() < 0.4:
                        mid = mid[0]
                    last = v["last"].upper() + ((" " + v["suffix"]) if v["suffix"] else "")
                    name = last + ", " + v["first"].upper() + ((" " + mid) if mid else "")
                    dob = C.mdy(v["dob"]) if r.random() >= 0.03 else ""
                    num_, st, t, unit = v["addr"]
                    if v.get("household_of") is not None:
                        h = inc["victims"][v["household_of"]]
                        if h.get("kind") == "gen":
                            num_, st, t, unit = h["addr"]
                            u2 = r.random()
                            if unit and u2 < 0.45:
                                unit = unit.replace("APT ", "#").replace("UNIT ", "#")
                            elif u2 < 0.75:
                                t = {"ST": "STREET", "AVE": "AVENUE", "DR": "DRIVE", "RD": "ROAD", "LN": "LANE",
                                     "CT": "COURT", "PL": "PLACE", "BLVD": "BOULEVARD"}.get(t.upper(), t)
                            v["city"] = h["city"]
                    addr = "%d %s %s%s" % (num_, st.upper(), t.upper(), (" " + unit) if unit else "") if v["city"] else ""
                    sex = "M" if v["male"] else "F"
                    race = v["race"]
                    eth = "H" if v["hisp"] else "N"
                    city = v["city"]
                vrows.append([seq, "I", name, dob, age, sex, race, eth, self._injury(offs[0], r), addr, city])
            reps = [(0, inc["report"])]
            if inc["supplement"]:
                d2 = inc["report"] + TD(days=int(r.integers(3, 41)))
                if d2 <= C.RECORDS_END:
                    reps.append((1, d2))
            added = set(k + 1 for k, v in enumerate(inc["victims"]) if v.get("added"))
            for sup, rd in reps:
                if sup:
                    # the supplement's officer re-enters each victim's residence in the RMS form
                    vrows = [vr[:9] + [retype(vr[9], rt) if (vr[1] == "I" and vr[9] and rt.random() < 0.7) else vr[9]] + vr[10:]
                             for vr in vrows]
                for o in offs:
                    for vr in vrows:
                        if sup == 0 and vr[0] in added:
                            continue
                        rows.append([num, sup, C.mdy(rd), C.mdy(inc["occurred"].date()), inc["occurred"].strftime("%H:%M"),
                                     NM.DISTRICT_NAMES[inc["dist"]].upper(), "%d%s%d" % (inc["dist"], "NECSW"[inc["dist"] - 1], inc["beat"]),
                                     o, NIBRS[o], inc["weapon"] if o != "520" else "FIREARM"] + vr)
        head = ["incident_number", "supplement_no", "report_date", "occurred_date", "occurred_time", "district", "beat",
                "nibrs_code", "offense", "weapon", "victim_seq", "victim_type", "victim_name", "victim_dob", "victim_age",
                "victim_sex", "victim_race", "victim_ethnicity", "injury", "victim_residence", "victim_res_city"]
        return C.write_csv(os.path.join(out, C.F_HPD), head, rows)

    def _injury(self, off, r):
        if off == "09A":
            return "DECEASED"
        if off in ("13A",):
            return "SERIOUS" if r.random() < 0.4 else ("MINOR" if r.random() < 0.85 else "NONE")
        if off in ("13B", "11A", "100"):
            return "MINOR" if r.random() < 0.6 else "NONE"
        if off == "120":
            return "NONE" if r.random() < 0.6 else ("MINOR" if r.random() < 0.9 else "SERIOUS")
        return "NONE"

    # ------------------------------------------------------------------ Belvantis
    def write_gps(self, out):
        ev = self.ev
        r = C.stream("gps_layout")
        events = []
        for en in ev.enrolments:
            last = None
            for x in en["events"]:
                last = x["d"]
            if last is not None and last < C.GPS_LOG_START:
                continue
            i = en["p"]
            nm = "%s, %s" % (ev.last[i], ev.first[i])
            cms = str(int(ev.pid[i]))
            ref = cms
            plan = [(cms, x) for x in en["events"]]
            if i in ev.oms and r.random() < 0.60:
                ref = ev.oms[i][0]
                plan = [(ref, x) for x in en["events"]]
                s, e = en["events"][0]["d"], min(en["end"], C.RECORDS_END)
                if (e - s).days > 75 and r.random() < 0.85 and s < dt.date(2026, 10, 1):
                    # re-registered under the case-management id at a device service; the vendor closes a record
                    # with no activity for six months at its next half-year batch, so the legacy record stays open,
                    # still showing the device it last held, until then or until the enrolment ends
                    X = s + TD(days=int(r.integers(20, (e - s).days - 40)))
                    held, s0 = [], None
                    for x in en["events"]:
                        if x["t"] == "SUSPEND" and s0 is None:
                            s0 = x["d"]
                        elif x["t"] == "RESUME" and s0 is not None:
                            held.append((s0, x["d"]))
                            s0 = None
                    if s0 is not None:
                        held.append((s0, e))
                    for a, b in held:
                        if a <= X <= b:
                            X = b + TD(days=1)
                    if X < e - TD(days=20):
                        idle = X + TD(days=183)
                        qe = dt.date(idle.year, 6, 30) if idle.month <= 6 else dt.date(idle.year, 12, 31)
                        newdev = "BV%07d" % int(r.integers(1_000_000, 9_999_999))
                        cur = None
                        plan = []
                        for x in en["events"]:
                            if x["d"] < X:
                                if x["t"] in ("ENROL", "DEVICE_ISSUE"):
                                    cur = x["dev"]
                                plan.append((ref, x))
                            else:
                                y = dict(x)
                                if y.get("dev") == cur:
                                    y["dev"] = newdev
                                plan.append((cms, y))
                        plan.append((cms, dict(t="ENROL", d=X, dev=newdev)))
                        plan.append((ref, dict(t="END", d=min(en["end"], qe), dev=cur)))
                        plan.sort(key=lambda t: (t[1]["d"], ["ENROL", "DEVICE_RETURN", "DEVICE_ISSUE", "SUSPEND", "RESUME",
                                                             "END", "ACCOUNT_TRANSFER"].index(t[1]["t"])))
            for ref_x, x in plan:
                if x["d"] > C.RECORDS_END:
                    continue
                late = 0
                if x["t"] == "END" and r.random() < 0.15:
                    late = int(r.integers(5, 26))
                elif r.random() < 0.25:
                    late = int(r.integers(1, 3))
                ld = x["d"] + TD(days=late)
                hh = int(r.integers(8, 18))
                lt = dt.datetime(ld.year, ld.month, ld.day, hh, int(r.integers(0, 60)), int(r.integers(0, 60)))
                lu = to_utc(lt)
                e = dict(logged=lu, effective=x["d"], ref=ref_x, name=nm, serial=x["dev"], event=x["t"],
                         note=x.get("note", ""))
                events.append(e)
                if x["t"] in ("ENROL", "DEVICE_ISSUE") and r.random() < 0.02:
                    dup = dict(e)
                    dup["logged"] = lu + TD(minutes=int(r.integers(2, 90)))
                    dup["dup"] = True
                    events.append(dup)
        events.sort(key=lambda e: e["logged"])
        ids = r.choice(np.arange(100_000_000, 999_999_999), size=len(events) + 200, replace=False)
        k = 0
        out_ev = []
        voids = []
        for e in events:
            e["id"] = "BVE%d" % int(ids[k])
            k += 1
            if e.get("dup"):
                vd = e["logged"] + TD(days=int(r.integers(0, 6)), hours=int(r.integers(1, 6)))
                voids.append(dict(logged=vd, effective=e["effective"], ref=e["ref"], name=e["name"], serial=None,
                                  event="VOID", voids=e["id"], note="duplicate entry"))
        for v in voids:
            v["id"] = "BVE%d" % int(ids[k])
            k += 1
        allev = [e for e in sorted(events + voids, key=lambda e: e["logged"]) if e["logged"] <= GPS_EXPORTED]
        rn = C.stream("gps_notes")
        for e in allev:
            e["note"] = gps_note(e["event"], e["note"], rn)
        for e in allev:
            out_ev.append({"event_id": e["id"], "logged_utc": e["logged"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                           "effective_date": e["effective"].isoformat(), "client_ref": e["ref"], "client_name": e["name"],
                           "serial_no": e["serial"], "event": e["event"], "voids_event_id": e.get("voids"),
                           "note": e["note"] or None})
        obj = {"account": "MDOC-R4", "account_name": "Merrow DOC Community Supervision Region 4",
               "account_time_zone": "US/Central",
               "export": {"exported_utc": GPS_EXPORTED.strftime("%Y-%m-%dT%H:%M:%SZ"), "from": "2025-01-01", "to": "2026-12-31",
                          "scope": "events for enrolments active on or after 2025-01-01"},
               "events": out_ev}
        C.write_json(os.path.join(out, C.F_GPS), obj)
        self.gps_events_written = allev
        return len(out_ev)

    # ------------------------------------------------------------------ programmes (distractor)
    def write_programs(self, out):
        ev = self.ev
        r = C.stream("prog_layout")
        provs = {"T4C": "Region 4 Programs Unit", "MRT": "Region 4 Programs Unit", "SUD-IOP": "Bridgeway Recovery",
                 "SUD-OP": "Bridgeway Recovery", "EMPLOY": "Darrow Workforce Partners", "ANGER MGMT": "Keswick Family Services"}
        rows = []
        ids = r.choice(np.arange(400_000, 999_999), size=len(ev.referrals), replace=False)
        for k, x in enumerate(sorted(ev.referrals, key=lambda x: x["date"])):
            if x["date"] > C.RECORDS_END:
                continue
            rows.append(["RF%d" % int(ids[k]), int(ev.pid[x["p"]]), x["prog"], x["date"].isoformat(), C.iso(x["start"]),
                         C.iso(x["end"]), x["outcome"], provs[x["prog"]]])
        head = ["referral_id", "cms_person_id", "program", "referral_date", "start_date", "discharge_date",
                "discharge_status", "provider"]
        return C.write_csv(os.path.join(out, C.F_PROG), head, rows)
