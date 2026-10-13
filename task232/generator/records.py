"""task232 records: the unit's childcare investigation files (register, contact follow-up, the centres' attendance
exports in three layouts, room bookings) and the Notifiable Conditions Platform's records for the district (ELR message
log, enteric case extract, interface incident log), all built from the simulated world.

The investigations come straight from sim.World. The platform layer adds every other notifiable condition the district's
six laboratory feeds report, the reports each test produces (preliminary, final, corrected; the reference laboratory's
typing of isolates others found), the feeds' outages and recoveries, and the case records the surveillance team keeps."""
import math
import random
from datetime import date, datetime, timedelta

import params as P
import sim as S
import world as W

MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]


def rng(*key):
    return random.Random("%d|records|" % P.REC_SEED + "|".join(str(k) for k in key))


def hhmm(h):
    m = int(round(h * 60))
    return "%02d:%02d" % (m // 60, m % 60)


def ampm(h):
    m = int(round(h * 60))
    hh, mm = m // 60, m % 60
    return "%d:%02d %s" % ((hh - 1) % 12 + 1, mm, "AM" if hh < 12 else "PM")


def dmy(d):
    return "%02d-%s-%d" % (d.day, MON[d.month - 1], d.year)


def local_iso(d, h):
    m = int(round(h * 60))
    return "%sT%02d:%02d:00" % (d.isoformat(), m // 60, m % 60)


def nsw(t):
    return t.astimezone(W.NSW)


# ================================================================================================ investigations
class Investigations:
    """The unit's own files on its childcare investigations."""

    def __init__(self, world):
        self.w = world
        self.invs = sorted(world.invs, key=lambda i: (i.received, i.onset, i.cond))
        seq = {}
        for i in self.invs:
            y = nsw(i.received).year
            seq[y] = seq.get(y, 0) + 1
            i.iid = "CC%02d-%03d" % (y % 100, seq[y])

    def register(self):
        rows = []
        for i in self.invs:
            rows.append(dict(
                investigation=i.iid, ncp_case=i.case_no, condition=P.COND[i.cond][0], service=i.centre["sid"],
                room=i.room["room"], index_role="Educator" if i.index["role"] == "educator" else "Child",
                index_person=i.index["pid"], onset=i.onset, inf_from=i.inf_days[0], inf_to=i.inf_days[-1],
                feed=W.FEED[i.feed]["name"], specimen=i.specimen, authorised=nsw(i.auth), received=nsw(i.received),
                call=nsw(i.call), followup_to=i.fu_to, status="Closed" if i.closed else "Open",
                closed=i.closed_on if i.closed else None))
        return rows

    def followup(self):
        """One row per room contact: every child and educator who attended the room on a day the index attended while
        infectious, with the illness the follow-up recorded."""
        rows = []
        for i in self.invs:
            r = rng("followup", i.iid)
            cases = {x["pid"]: x for x in i.cases}
            for pid in sorted(i.contacts):
                p = i.contacts[pid]
                x = cases.get(pid)
                if x is None:
                    rows.append([i.iid, pid, "Educator" if p["role"] == "educator" else "Child", "N", "", "", "", "",
                                 "", ""])
                    continue
                confirmed = x["status"] == "confirmed"
                approx = "Y" if (not confirmed and r.random() < 0.18 and self.steady(i, x["onset"])) else ""
                rows.append([i.iid, pid, "Educator" if p["role"] == "educator" else "Child", "Y", x["onset"].isoformat(),
                             approx, x["specimen"].isoformat() if confirmed else "", "Positive" if confirmed else
                             "Not tested", "Confirmed" if confirmed else "Probable", x["case_no"]])
        header = ["investigation_id", "contact_person_no", "contact_type", "ill", "onset_date", "onset_approximate",
                  "specimen_collected", "result", "case_status", "ncp_case_no"]
        return header, rows

    def steady(self, i, onset):
        """an onset whose place in the index's incubation window holds two days either side (a family's approximate
        date is recorded as given)"""
        lo, hi = P.COND[i.cond][1], P.COND[i.cond][2]
        inside = lambda o: (o - i.inf_days[0]).days >= lo and (o - i.inf_days[-1]).days <= hi
        return len({inside(onset + timedelta(days=k)) for k in range(-2, 3)}) == 1

    def people(self, i):
        """Everyone the room's export carries: the roster and the casual educators who covered absences."""
        return {p["pid"]: p for p in i.roster.people}

    def attendance(self, layout):
        """The room's attendance from 21 days before the index's onset to 14 days after the exclusion, as the centre's
        software exports it."""
        out = []
        for i in self.invs:
            if i.centre["layout"] != layout:
                continue
            ppl = self.people(i)
            recs = sorted(((d, pid), v) for (pid, d), v in i.att.items())
            out.append((i, [(d, pid, ppl[pid]["role"], a, b) for (d, pid), (a, b) in recs]))
        return out

    def bookings(self):
        header = ["investigation_id", "service_id", "room", "person_no", "person_type", "booked_days", "booked_from",
                  "booked_to"]
        rows = []
        for i in self.invs:
            for p in sorted(i.roster.people, key=lambda q: (q["role"] != "child", q["pid"])):
                if not p["days"]:
                    continue        # casual educators carry no booking
                rows.append([i.iid, i.centre["sid"], i.room["room"], p["pid"],
                             "Educator" if p["role"] == "educator" else "Child",
                             " ".join(DAYS[k] for k in sorted(p["days"])), hhmm(p["start"]), hhmm(p["end"])])
        return header, rows


# ================================================================================================ the platform
# Notifiable conditions in the message log (COVID-19 reaches the platform through the national gateway, not these feeds).
# key: (name, legacy code, 2025 code, cases a year in the district, season peak months, multiplier, group)
CONDITIONS = {
    "FLU": ("Influenza", "FLU", "RES-FLU", 3100, (6, 7, 8), 3.0, "RES"),
    "RSV": ("Respiratory syncytial virus infection", "RSV", "RES-RSV", 2050, (4, 5, 6, 7), 2.4, "RES"),
    "PER": ("Pertussis", "PERT", "VPD-PER", 170, (), 1.0, "RES"),
    "LEG": ("Legionellosis", "LEGI", "RES-LEG", 7, (), 1.0, "RES"),
    "MEN": ("Invasive meningococcal disease", "MENI", "VPD-MEN", 3, (7, 8, 9), 1.8, "VPD"),
    "CHL": ("Chlamydia trachomatis infection", "CHLAM", "STI-CHL", 1880, (), 1.0, "STI"),
    "GON": ("Gonococcal infection", "GONO", "STI-GON", 410, (), 1.0, "STI"),
    "SYP": ("Syphilis", "SYPH", "STI-SYP", 55, (), 1.0, "STI"),
    "HBV": ("Hepatitis B", "HEPB", "BBV-HBV", 70, (), 1.0, "STI"),
    "HCV": ("Hepatitis C", "HEPC", "BBV-HCV", 140, (), 1.0, "STI"),
    "CMP": ("Campylobacteriosis", "CAMPY", "ENT-CMP", 560, (11, 12, 1, 2), 1.5, "ENT"),
    "SAL": ("Salmonellosis", "SALM", "ENT-SAL", 260, (12, 1, 2, 3), 1.8, "ENT"),
    "SHIG": ("Shigellosis", "SHIGL", "ENT-SHG", 46, (12, 1, 2, 3), 1.4, "ENT"),
    "STEC": ("Shiga toxin-producing E. coli infection", "VTEC", "ENT-STC", 11, (), 1.0, "ENT"),
    "CRYP": ("Cryptosporidiosis", "CRYPT", "ENT-CRY", 125, (12, 1, 2, 3), 2.2, "ENT"),
    "ROT": ("Rotavirus infection", "ROTA", "ENT-ROT", 85, (8, 9, 10), 2.0, "ENT"),
    "HAV": ("Hepatitis A", "HEPA", "ENT-HAV", 5, (), 1.0, "ENT"),
    "LIS": ("Listeriosis", "LIST", "ENT-LIS", 2, (), 1.0, "ENT"),
    "RRV": ("Ross River virus infection", "RRV", "ARB-RRV", 210, (2, 3, 4), 3.0, "ARB"),
    "BFV": ("Barmah Forest virus infection", "BFV", "ARB-BFV", 36, (2, 3, 4), 2.5, "ARB"),
    "QFV": ("Q fever", "QFEV", "ZOO-QFV", 9, (), 1.0, "ARB"),
    "LEP": ("Leptospirosis", "LEPT", "ZOO-LEP", 6, (2, 3, 4), 2.0, "ARB"),
}
ENTERIC = ["CMP", "SAL", "SHIG", "STEC", "CRYP", "ROT", "HAV", "LIS"]
URGENT = ["SHIG", "STEC", "CRYP"]
GROUP_SHARE = {
    "RES": {"CRBH": 0.30, "LPG": 0.30, "HDN": 0.18, "KES": 0.10, "HPS": 0.12, "SERL": 0.0},
    "VPD": {"CRBH": 0.62, "LPG": 0.0, "HDN": 0.0, "KES": 0.0, "HPS": 0.0, "SERL": 0.38},
    "STI": {"CRBH": 0.10, "LPG": 0.42, "HDN": 0.26, "KES": 0.10, "HPS": 0.12, "SERL": 0.0},
    "ENT": {"CRBH": 0.15, "LPG": 0.37, "HDN": 0.26, "KES": 0.10, "HPS": 0.12, "SERL": 0.0},
    "ARB": {"CRBH": 0.05, "LPG": 0.36, "HDN": 0.24, "KES": 0.10, "HPS": 0.10, "SERL": 0.15},
}
STEC_SERL_FIRST = 0.16
TESTS = {
    # condition: list of (test code, result text, preliminary report first)
    "FLU": [("RESPCR", "Influenza A RNA detected", False)], "RSV": [("RESPCR", "RSV RNA detected", False)],
    "PER": [("BPPCR", "B. pertussis DNA detected", False)], "LEG": [("LEGUAG", "L. pneumophila sg1 antigen detected", False)],
    "MEN": [("NMPCR", "N. meningitidis DNA detected", False)], "CHL": [("CTPCR", "C. trachomatis DNA detected", False)],
    "GON": [("NGPCR", "N. gonorrhoeae DNA detected", False)], "SYP": [("TPSER", "T. pallidum antibody reactive", False)],
    "HBV": [("HBSAG", "HBsAg detected", False)], "HCV": [("HCVRNA", "HCV RNA detected", False)],
    "CMP": [("FAEPCR", "Campylobacter DNA detected", False), ("FAECUL", "Campylobacter jejuni", True)],
    "SAL": [("FAEPCR", "Salmonella DNA detected", False), ("FAECUL", "Salmonella species", True)],
    "SHIG": [("FAEPCR", "Shigella/EIEC DNA detected", False), ("FAECUL", "Shigella sonnei", True)],
    "STEC": [("FAEPCR", "stx1/stx2 detected", False), ("FAECUL", "E. coli, Shiga toxin-producing", True)],
    "CRYP": [("FAEPCR", "Cryptosporidium DNA detected", False)], "ROT": [("FAEPCR", "Rotavirus RNA detected", False)],
    "HAV": [("HAVIGM", "HAV IgM detected", False)], "LIS": [("BLDCUL", "Listeria monocytogenes", True)],
    "RRV": [("RRVIGM", "RRV IgM detected", False)], "BFV": [("BFVIGM", "BFV IgM detected", False)],
    "QFV": [("QFVSER", "C. burnetii phase II IgM detected", False)], "LEP": [("LEPPCR", "Leptospira DNA detected", False)],
}
TYPING = {"SAL": "Salmonella Typhimurium", "SHIG": "Shigella sonnei biotype g", "STEC": "E. coli O157:H7, stx2"}
PRELIM_LABS = {"CRBH", "LPG", "HDN"}       # laboratories that send a preliminary culture report before the final
HELD = {"CRBH": 0.004, "LPG": 0.005, "HDN": 0.006, "KES": 0.008, "HPS": 0.005, "SERL": 0.01}
LEGACY_UNTIL = date(2025, 6, 30)
HDN_LEGACY_UNTIL = date(2025, 11, 16)    # Halden's condition mapping moved to the 2025 code set on 17 November 2025


def accession(feed, r, d, seq):
    if feed == "CRBH":
        return "M%02d-%06d" % (d.year % 100, seq)
    if feed in ("LPG", "HPS") and (feed == "LPG" or d >= P.ACQUISITION):
        return ("L" if feed == "LPG" else "H") + "%d%06d" % (d.year % 10, seq % 1000000)
    if feed == "HPS":
        return "HF%07d" % seq
    if feed == "HDN":
        letters = "ABCDEFGHJKLMNPQRSTUVWXYZ"
        return "HD%06d%s" % (seq % 1000000, letters[(seq * 7) % 24])
    if feed == "KES":
        return "%06d" % (seq % 1000000)
    return "S%02d-%05d" % (d.year % 100, seq % 100000)


def namespaced(feed, acc, d):
    return "%s^%s" % (acc, W.facility_code(feed, d))


def hl7(t, feed):
    """OBR-22 / MSH-7 as each laboratory's system writes it: New South Wales laboratories in local time with the
    offset, the Queensland laboratory in Queensland time, the reference laboratory in UTC."""
    if feed == "KES":
        t = t.astimezone(W.QLD)
    elif feed == "SERL":
        t = t.astimezone(W.UTC)
    else:
        t = t.astimezone(W.NSW)
    off = t.utcoffset()
    mins = int(off.total_seconds() // 60)
    return "%s%s%02d%02d" % (t.strftime("%Y%m%d%H%M%S"), "+" if mins >= 0 else "-", abs(mins) // 60, abs(mins) % 60)


def f_name(code):
    for f in P.FEEDS:
        for c, _a, _b in W.FEED[f]["codes"]:
            if c == code:
                return W.FEED[f]["short"] if f not in ("CRBH", "SERL") else "the " + W.FEED[f]["short"]
    return code


OUTAGE_LEAD = ["No messages from {lab} for {hrs} hours; ", "Feed silent past the monitoring threshold. ",
               "Monitoring alert. ", "{Lab} feed silent. ", "Feed silent for {hrs} h. ", "No traffic from {lab}; "]
OUTAGE_CAUSE = [
    "the laboratory found its interface engine stopped, restarted it and released the queued results.",
    "network outage at the laboratory's core site; results queued and sent when the link was restored at {end}.",
    "the laboratory's LIS upgrade overran its window; interface restarted at {end}.",
    "certificate on the laboratory's VPN endpoint had expired; renewed at {end} and the queue released.",
    "laboratory interface server patched without notice; service resumed at {end}.",
    "disk full on the laboratory's interface server; space cleared and the queue released at {end}.",
    "a firewall change at the laboratory blocked the outbound port; rule restored at {end}.",
    "power work at the laboratory's data centre; interface back at {end}.",
    "outbound queue stalled on a message the engine could not parse; message pulled and queue released at {end}.",
    "carrier fault on the laboratory's link; restored at {end}.",
    "LIS database maintenance at the laboratory ran long; results released at {end}.",
    "interface engine service account locked out after a password change; unlocked at {end}.",
]
DR_TEXT = [
    "Primary interface engine failed; laboratory moved its outbound feed to the disaster-recovery engine at {dr}; "
    "primary engine restored at {end}.",
    "Laboratory failed over to its disaster-recovery interface engine at {dr} after the primary engine crashed; failed "
    "back at {end}.",
    "Hardware fault on the laboratory's primary interface engine. Outbound feed on the disaster-recovery engine from "
    "{dr}; back on the primary at {end}.",
]
REPLAY_TEXT = [
    "Laboratory interface engine stopped at {start}; restarted from its last checkpoint at {end}.",
    "Interface engine at the laboratory hung at {start}; restarted at {end} from its checkpoint.",
]


def _cap(t):
    return t[0].upper() + t[1:]


def utc_iso(t):
    return t.astimezone(W.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


class Platform:
    """The district's notifications on the platform: cases, the reports that notified them, and the feeds' incidents."""

    def __init__(self, world, inv):
        self.w, self.inv = world, inv
        self.cases = []        # dict(case_no?, cond, person, onset, status, setting, created, ...)
        self.reports = []      # dict(feed, case, test, status, auth, received, accession, patient, result, ...)
        self.msgs = []
        self.incidents = []
        self.persons = 0
        self.seq = {f: 100000 + rng("seq", f).randint(0, 50000) for f in P.FEEDS}
        self.build()

    # ------------------------------------------------------------------------------------------ people and cases
    def person(self):
        self.persons += 1
        return self.persons

    def patient_ref(self, feed, person, d):
        r = rng("patient", feed, person)
        if feed == "CRBH":
            return "CR%07d" % r.randint(1000000, 9899999)
        if feed == "LPG" or (feed == "HPS" and d >= P.ACQUISITION):
            return "LP%08d" % r.randint(10000000, 98999999)
        if feed == "HPS":
            return "HF%06d" % r.randint(100000, 989999)
        if feed == "HDN":
            return "HDP%06d" % r.randint(100000, 989999)
        if feed == "KES":
            return "KQ%07d" % r.randint(1000000, 9899999)
        return "SR%07d" % r.randint(1000000, 9899999)

    def first_feed(self, r, c, border=False):
        g = CONDITIONS[c][6]
        if c == "STEC" and r.random() < STEC_SERL_FIRST:
            return "SERL"
        sh = GROUP_SHARE[g]
        keys = [k for k in P.FEEDS if sh[k] > 0]
        return r.choices(keys, weights=[sh[k] for k in keys])[0]

    def tat(self, r, test):
        return r.choices([0, 1, 2, 3], weights=[0.1, 0.45, 0.3, 0.15])[0] if test.endswith("PCR") or test.endswith(
            "UAG") or test.endswith("SAG") else r.choices([1, 2, 3, 4], weights=[0.15, 0.4, 0.3, 0.15])[0]

    def add_case(self, **kw):
        kw.setdefault("status", "Confirmed")
        kw.setdefault("merged_into", None)
        kw.setdefault("setting", "")
        self.cases.append(kw)
        return kw

    def add_report(self, case, feed, test, status, auth, result, specimen, accession_no=None, person=None,
                   received=None, kind="original"):
        person = case["person"] if person is None else person
        if accession_no is None:
            self.seq[feed] += rng("acc-step", feed, self.seq[feed]).randint(3, 40)
            accession_no = accession(feed, None, auth.date(), self.seq[feed])
        rep = dict(case=case, feed=feed, test=test, status=status, auth=auth, result=result, specimen=specimen,
                   accession=accession_no, plain=accession_no, person=person, received=received, kind=kind)
        self.reports.append(rep)
        return rep

    # ------------------------------------------------------------------------------------------ build
    def build(self):
        self.index_and_contacts()
        self.background()
        self.merges_and_reinfections()
        self.deliver()
        self.incident_events()
        self.amended_finals()
        self.number_cases()
        self.messages()

    def lab_chain(self, r, case, feed, specimen, earliest=None, first_auth=None):
        """The reports one specimen produces at its laboratory, and the reference laboratory's typing of an isolate."""
        c = case["cond"]
        acc_seq = None
        reps = []
        for k, (test, text, prelim) in enumerate(TESTS[c]):
            if k > 0 and r.random() < 0.25:
                continue      # culture not requested or not grown
            if k == 0 and first_auth is not None:
                auth = first_auth
            else:
                d = specimen + timedelta(days=self.tat(r, test) + (1 if k > 0 else 0))
                if earliest is not None and d < earliest:
                    d = earliest
                auth = S.auth_time(r, feed, d)
                if (auth.minute % 15) == 0:
                    auth = auth - timedelta(minutes=1)
            if acc_seq is None:
                self.seq[feed] += r.randint(3, 40)
                acc_seq = self.seq[feed]
            acc = accession(feed, r, auth.date(), acc_seq)
            if prelim and feed in PRELIM_LABS:
                pa = S.auth_time(r, feed, (auth - timedelta(days=1)).date())
                if pa < auth - timedelta(hours=6) and (first_auth is None or pa > first_auth):
                    reps.append(self.add_report(case, feed, test, "P", pa, "Presumptive " + text.split(",")[0], specimen,
                                                acc))
            reps.append(self.add_report(case, feed, test, "F", auth, text, specimen, acc))
        if c in TYPING and feed != "SERL" and r.random() < (0.85 if c != "SAL" else 0.5):
            d = specimen + timedelta(days=r.randint(6, 13))
            ta = S.auth_time(r, "SERL", d)
            if (ta.minute % 15) == 0:
                ta -= timedelta(minutes=1)
            self.seq["SERL"] += r.randint(3, 40)
            reps.append(self.add_report(case, "SERL", "ISOTYP", "F", ta, TYPING[c], specimen,
                                        accession("SERL", r, ta.date(), self.seq["SERL"])))
        if r.random() < 0.012:
            base = reps[0] if reps else None
            if base is not None:
                ca = base["auth"] + timedelta(days=r.randint(1, 6), minutes=r.randint(5, 300))
                ca = ca.astimezone(W.NSW)
                if ca.minute % 15 == 0:
                    ca -= timedelta(minutes=1)
                reps.append(self.add_report(case, base["feed"], base["test"], "C", ca, base["result"] + " (corrected)",
                                            specimen, base["accession"]))
        return reps

    def index_and_contacts(self):
        """The childcare investigations' cases: each index case notified by the feed the simulation drew, and the room
        contacts' confirmed cases notified when tested."""
        for i in self.inv.invs:
            r = rng("index", i.iid)
            setting = "Childcare staff" if i.index["role"] == "educator" else "Childcare attendee"
            case = self.add_case(cond=i.cond, person=self.person(), onset=i.onset, created=i.received, setting=setting,
                                 investigation=i.iid, index=True, age=(r.randint(19, 58) if setting == "Childcare staff"
                                                                      else r.randint(0, 4)))
            case["first"] = i.feed
            reps = self.lab_chain(r, case, i.feed, i.specimen, first_auth=i.auth)
            first = min(reps, key=lambda x: x["auth"])
            first["received"] = i.received
            first["fixed"] = True
            i.case = case
            cases = {x["pid"]: x for x in i.cases}
            for pid in sorted(cases):
                x = cases[pid]
                rr = rng("contact", i.iid, pid)
                p = i.contacts[pid]
                cs = self.add_case(cond=i.cond, person=self.person(), onset=x["onset"], setting="Childcare staff" if
                                   p["role"] == "educator" else "Childcare attendee", investigation=i.iid,
                                   status="Confirmed" if x["status"] == "confirmed" else "Probable",
                                   age=rr.randint(19, 58) if p["role"] == "educator" else rr.randint(0, 5))
                x["case"] = cs
                if x["status"] == "confirmed":
                    # tested once the investigation asked: never before the index's notification
                    sp = max(x["onset"] + timedelta(days=rr.randint(0, 3)), nsw(i.received).date() + timedelta(days=rr.randint(0, 2)))
                    x["specimen"] = sp
                    feed = self.first_feed(rr, i.cond)
                    if i.centre["border"] and rr.random() < P.BORDER_KES:
                        feed = "KES"
                    if feed == "SERL":
                        feed = "CRBH"
                    cs["created_auth_floor"] = sp
                    self.lab_chain(rr, cs, feed, sp)
                else:
                    cs["created"] = datetime(x["onset"].year, x["onset"].month, x["onset"].day, 12, 0, tzinfo=W.NSW) \
                        if x["onset"] > nsw(i.received).date() else i.received + timedelta(hours=rr.randint(20, 70))

    def background(self):
        """Every other notified case in the district, October 2022 to October 2026."""
        start, end = date(2022, 9, 20), date(2026, 10, 31)
        for c, (name, _l, _n, per_year, peak, mult, group) in CONDITIONS.items():
            r = rng("background", c)
            norm = (len(peak) * mult + (12 - len(peak))) / 12.0
            d = start
            while d <= end:
                m = mult if d.month in peak else 1.0
                lam = per_year / 365.0 * m / norm
                if c == "PER" and date(2024, 3, 1) <= d <= date(2025, 2, 28):
                    lam *= 4.0      # the 2024 pertussis epidemic
                if c in URGENT:
                    lam *= 0.86     # the childcare cases come from the investigations
                n = 0
                L, p, k = math.exp(-lam), 1.0, 0
                while True:
                    p *= r.random()
                    if p < L:
                        break
                    k += 1
                n = k
                for _ in range(n):
                    self.background_case(r, c, d)
                d += timedelta(days=1)

    def background_case(self, r, c, onset_day):
        feed = self.first_feed(r, c)
        spec = onset_day + timedelta(days=r.choice([0, 1, 1, 2, 2, 3, 4, 6]))
        sex = r.choice(["F", "M"])
        age = self.age_for(r, c)
        case = self.add_case(cond=c, person=self.person(), onset=onset_day if r.random() < 0.72 else None, age=age,
                             sex=sex, setting=self.setting_for(r, c, age))
        case["first"] = feed
        self.lab_chain(r, case, feed, spec)
        if r.random() < 0.03:
            # a second positive specimen weeks later, sometimes at another laboratory
            f2 = feed if r.random() < 0.7 else self.first_feed(r, c)
            if f2 != "SERL":
                self.lab_chain(r, case, f2, spec + timedelta(days=r.randint(8, 30)))

    def age_for(self, r, c):
        g = CONDITIONS[c][6]
        if c in ("RSV", "ROT"):
            return r.choice([0, 0, 1, 1, 2, 3, 4, 67, 74, 81, 35])
        if g == "STI":
            return r.randint(16, 45)
        return r.randint(0, 88)

    def setting_for(self, r, c, age):
        if c not in ENTERIC:
            return ""
        if age <= 5 and r.random() < 0.22:
            return "Childcare attendee"
        if 18 <= age <= 65:
            u = r.random()
            if u < 0.05:
                return "Food handler"
            if u < 0.08:
                return "Health care worker"
        return ""

    # ------------------------------------------------------------------------------------------ the ask devices
    def index(self):
        self.by_case = {}
        for x in self.reports:
            self.by_case.setdefault(id(x["case"]), []).append(x)

    def of(self, cs):
        return self.by_case.get(id(cs), [])

    def year_urgent(self):
        self.index()
        out = []
        for cs in self.cases:
            if cs["cond"] in URGENT and not cs.get("investigation") and cs["status"] == "Confirmed":
                reps = self.of(cs)
                if reps:
                    t = min(x["auth"] for x in reps)
                    if date(2025, 10, 20) <= nsw(t).date() <= date(2026, 9, 10):
                        out.append((t, cs))
        out.sort(key=lambda x: (x[0], x[1]["person"]))
        return [cs for _t, cs in out]

    def merges_and_reinfections(self):
        """Duplicate cases: a patient's report from a second laboratory that the platform could not match to the
        existing case opened a new one; the surveillance team merged the earlier case into the later one, which carries
        the follow-up. Second episodes: a patient with two infections of the same condition in the year."""
        pairs = [("LPG", "CRBH", ("SHIG", "CRYP")), ("LPG", "KES", ("CRYP", "SHIG")), ("HDN", "LPG", ("CRYP", "SHIG")),
                 ("HDN", "HPS", ("SHIG", "CRYP")), ("CRBH", "HDN", ("CRYP", "SHIG")), ("CRBH", "SERL", ("STEC", "SHIG"))]
        pool = self.year_urgent()
        r = rng("merges")
        used = set()
        self.merge_log = []
        for x, y, conds in pairs:
            cand = []
            for c in conds:
                cand = [cs for cs in pool if cs["cond"] == c and cs["first"] == x and id(cs) not in used]
                if cand:
                    break
            if not cand:
                raise AssertionError(("no case for merge", x, y, conds))
            a = cand[r.randrange(len(cand))]
            used.add(id(a))
            reps = [z for z in self.reports if z["case"] is a]
            t0 = min(z["auth"] for z in reps)
            spec = max(min(z["specimen"] for z in reps) + timedelta(days=r.randint(1, 3)), nsw(t0).date())
            b = self.add_case(cond=c, person=a["person"], onset=a["onset"], age=a["age"], sex=a.get("sex"),
                              setting=a["setting"])
            b["first"] = y
            if y == "SERL":
                ta = S.auth_time(r, "SERL", spec + timedelta(days=r.randint(5, 8)))
                if ta.minute % 15 == 0:
                    ta -= timedelta(minutes=1)
                self.seq["SERL"] += r.randint(3, 40)
                self.add_report(b, "SERL", "ISOTYP", "F", ta, TYPING[c], spec, accession("SERL", r, ta.date(),
                                                                                       self.seq["SERL"]))
                # the typing on case a's isolate is what reached the reference laboratory: drop a's own typing report
                self.reports = [z for z in self.reports if not (z["case"] is a and z["feed"] == "SERL")]
            else:
                self.lab_chain(r, b, y, spec, earliest=nsw(t0).date() + timedelta(days=1))
                self.reports = [z for z in self.reports if not (z["case"] is b and z["auth"] <= t0 + timedelta(hours=1))]
            assert [z for z in self.reports if z["case"] is b]
            assert min(z["auth"] for z in self.reports if z["case"] is b) > t0
            a["status"] = "Merged"
            a["merged_into"] = b
            self.merge_log.append((a, b))
        self.reinfections = []
        for feed, c in (("LPG", "SHIG"), ("HDN", "CRYP"), ("KES", "CRYP")):
            cand = [cs for cs in pool if cs["cond"] == c and cs["first"] == feed and id(cs) not in used]
            first = sorted(cand, key=lambda cs: min(z["auth"] for z in self.reports if z["case"] is cs))
            a = first[0]
            used.add(id(a))
            t0 = min(z["auth"] for z in self.reports if z["case"] is a)
            d = nsw(t0).date() + timedelta(days=r.randint(120, 190))
            b = self.add_case(cond=c, person=a["person"], onset=d - timedelta(days=2), age=a["age"], sex=a.get("sex"),
                              setting=a["setting"])
            b["first"] = feed
            self.lab_chain(r, b, feed, d)
            self.reinfections.append((a, b))

    # ------------------------------------------------------------------------------------------ delivery
    def outages(self):
        """Each feed's interface outages: the laboratory's results queue and go when the interface is back."""
        out = []
        for f in P.FEEDS:
            r = rng("outages", f)
            d = date(2022, 10, 1)
            while d <= date(2026, 10, 31):
                if r.random() < 3.2 / 365.0:
                    start = datetime(d.year, d.month, d.day, tzinfo=W.NSW) + timedelta(hours=r.uniform(0, 24))
                    dur = r.choice([r.uniform(1.5, 6), r.uniform(4, 14), r.uniform(10, 40)])
                    out.append(dict(feed=f, start=start, end=start + timedelta(hours=dur), kind="outage"))
                d += timedelta(days=1)
        return out

    def deliver(self):
        self.down = self.outages()
        inv_auth = sorted(x["auth"] for x in self.reports if x["case"].get("investigation"))
        for o in self.recovery_plan():
            feeds = ("LPG", "HPS") if o["feed"] == "LPG+HPS" else (o["feed"],)
            mine = [x["auth"] for x in self.reports if x["case"].get("investigation") and x["feed"] in feeds]
            while any(o["start"] - timedelta(hours=o["checkpoint"] + 6) <= t <= o["end"] + timedelta(hours=2)
                      for t in mine):
                for k in ("start", "end", "dr_from"):
                    if k in o:
                        o[k] = o[k] + timedelta(days=7)    # the next week's same hour: no investigation in the window
            self.down.append(o)
        for rep in self.reports:
            if rep.get("fixed"):
                continue
            feed = rep["feed"]
            r = rng("deliver", feed, rep["accession"], rep["test"], rep["status"], rep["auth"].isoformat())
            lateness = S.deliver(r, feed if feed != "HPS" else "HPS", rep["auth"])
            if not rep["case"].get("investigation") and r.random() < HELD[feed]:
                lateness = r.uniform(26.0, 100.0)    # held in the laboratory's interface error queue, sent by hand
            t = W.add_hours(rep["auth"], lateness)
            for o in self.down:
                if o["feed"] in (feed, "LPG+HPS" if feed in ("LPG", "HPS") else None) and o["start"] <= t <= o["end"]:
                    if o["kind"] == "dr":
                        rep["via_dr"] = o
                        t = max(t, o["dr_from"]) + timedelta(minutes=r.uniform(1, 9))
                    else:
                        if o["kind"] == "replay":
                            rep["via_replay"] = o      # queued in the stopped engine, sent by its replay on restart
                        t = o["end"] + timedelta(minutes=r.uniform(2, 40))
            rep["received"] = t
        self.error_queue()

    def error_queue(self):
        """At a failover the laboratory's interface staff also release, through the disaster-recovery engine, the
        results the primary engine had been holding in its error queue since they were authorised."""
        for o in [x for x in self.down if x["kind"] == "dr" and P.YEAR_FROM <= nsw(x["start"]).date() <= P.YEAR_TO]:
            for feed in (("LPG", "HPS") if o["feed"] == "LPG+HPS" else (o["feed"],)):
                r = rng("error-queue", feed, o["start"].isoformat())
                pool = [x for x in self.reports if x["feed"] == feed and x["kind"] == "original" and x["status"] == "F"
                        and not x["case"].get("investigation") and x["case"]["cond"] not in URGENT
                        and x.get("received") and not x.get("via_dr")
                        and o["start"] - timedelta(hours=62) <= x["auth"] <= o["start"] - timedelta(hours=30)]
                pool.sort(key=lambda z: (z["auth"], z["accession"]))
                assert pool, (feed, o["start"])
                for x in r.sample(pool, min(len(pool), 1 + (r.random() < 0.5))):
                    x["received"] = o["dr_from"] + timedelta(minutes=r.uniform(4, 35))
                    x["via_dr"] = o

    def recovery_plan(self):
        """Disaster-recovery failovers and replays in the year to 30 September 2026 (and one of each kind earlier)."""
        plan = [
            # feed, failure (NSW), hours to failover, hours to restore, checkpoint hours, kind
            ("CRBH", datetime(2026, 2, 17, 4, 50, tzinfo=W.NSW), 0.9, 14.3, 46.0, "dr"),
            ("LPG+HPS", datetime(2025, 11, 26, 2, 35, tzinfo=W.NSW), 1.4, 20.6, 56.0, "dr"),
            ("HDN", datetime(2026, 6, 10, 3, 10, tzinfo=W.NSW), 0.7, 11.8, 47.0, "dr"),
            ("KES", datetime(2026, 3, 12, 2, 40, tzinfo=W.NSW), 0.0, 27.5, 52.0, "replay"),
            ("SERL", datetime(2025, 12, 11, 6, 20, tzinfo=W.NSW), 0.0, 30.0, 72.0, "replay"),
            ("LPG+HPS", datetime(2024, 8, 21, 3, 5, tzinfo=W.NSW), 1.1, 9.2, 30.0, "dr"),
            ("KES", datetime(2024, 5, 14, 22, 15, tzinfo=W.NSW), 0.0, 7.5, 24.0, "replay"),
        ]
        out = []
        for feed, fail, to_dr, restore, ckpt, kind in plan:
            o = dict(feed=feed, start=fail, end=fail + timedelta(hours=restore), kind=kind, checkpoint=ckpt)
            if kind == "dr":
                o["dr_from"] = fail + timedelta(hours=to_dr)
            out.append(o)
        return out

    def incident_events(self):
        """The copies a recovery makes: a disaster-recovery engine, or the replay tool a restarted engine runs, re-sends
        what was sent since its checkpoint under fresh message ids, writing the filler order number with its namespace."""
        r = rng("copies")
        protect = {id(x) for x in self.reports if x["case"].get("investigation")}
        for o in [x for x in self.down if x["kind"] in ("dr", "replay")]:
            feeds = ("LPG", "HPS") if o["feed"] == "LPG+HPS" else (o["feed"],)
            resend = o["dr_from"] if o["kind"] == "dr" else o["end"]
            since = o["start"] - timedelta(hours=o["checkpoint"])
            batch = [x for x in self.reports if x["feed"] in feeds and x["kind"] == "original" and x.get("received")
                     and since <= x["received"] < o["start"]]
            assert not [x for x in batch if id(x) in protect], ("an investigation report in a replay window", o)
            for k, x in enumerate(sorted(batch, key=lambda z: z["received"])):
                cp = dict(x)
                cp["kind"] = "copy"
                cp["original"] = x
                cp["received"] = resend + timedelta(seconds=20 + 11 * k + r.randint(0, 9))
                cp["accession"] = namespaced(x["feed"], x["plain"], x["auth"].date())
                if o["kind"] == "dr":
                    cp["via_dr"] = o
                self.reports.append(cp)
            for x in self.reports:
                if (x.get("via_dr") is o or x.get("via_replay") is o) and x["kind"] == "original":
                    x["accession"] = namespaced(x["feed"], x["accession"], x["auth"].date())

    def amended_finals(self):
        """Some laboratories issue an amended result as a new final report of the same test, re-authorised, rather than
        as a corrected report."""
        r = rng("amended")
        rate = {"CRBH": 0.004, "LPG": 0.004, "HDN": 0.005, "KES": 0.02, "HPS": 0.004, "SERL": 0.03}
        add = []
        for x in sorted(self.reports, key=lambda z: (z["auth"], z["feed"], z["accession"])):
            if x["kind"] != "original" or x["status"] != "F" or x["case"].get("investigation"):
                continue
            if r.random() < rate[x["feed"]]:
                na = x["auth"] + timedelta(hours=r.uniform(3, 70))
                na = na.astimezone(W.NSW)
                if na.minute % 15 == 0:
                    na -= timedelta(minutes=1)
                am = dict(x)
                am["accession"] = x["plain"]
                am.pop("via_dr", None)
                am["auth"] = na
                am["kind"] = "amended"
                am["result"] = x["result"] + "; amended"
                rr = rng("deliver-amended", x["feed"], x["accession"], na.isoformat())
                t = W.add_hours(na, S.deliver(rr, x["feed"], na))
                for o in self.down:
                    if o["feed"] in (x["feed"], "LPG+HPS" if x["feed"] in ("LPG", "HPS") else None) and o["start"] <= t <= o["end"]:
                        t = (o["dr_from"] if o["kind"] == "dr" else o["end"]) + timedelta(minutes=rr.uniform(2, 40))
                        if o["kind"] in ("dr", "replay"):
                            am["accession"] = namespaced(x["feed"], x["plain"], na.date())
                am["received"] = t
                add.append(am)
        # an amended report can sit in the laboratory's error queue like any other
        for feed in P.FEEDS:
            yr = sorted([a for a in add if a["feed"] == feed and P.YEAR_FROM <= nsw(a["auth"]).date() <= P.YEAR_TO],
                        key=lambda z: (z["auth"], z["accession"]))
            if yr:
                a = yr[len(yr) // 3]
                a["received"] = a["auth"] + timedelta(hours=30 + r.uniform(0, 30))
        # a result amended while the laboratory's interface was down goes when it comes back
        for o in [x for x in self.down if x["kind"] == "replay" and x["start"].date() >= P.YEAR_FROM]:
            feed = o["feed"]
            pick = [x for x in self.reports if x["feed"] == feed and x["kind"] == "original" and x["status"] == "F"
                    and not x["case"].get("investigation") and o["start"] - timedelta(days=4) <= x["auth"] <
                    o["start"] - timedelta(hours=6)]
            pick.sort(key=lambda z: (z["auth"], z["accession"]))
            x = pick[len(pick) // 2]
            am = dict(x)
            am["accession"] = x["plain"]
            am.pop("via_dr", None)
            na = (o["start"] + timedelta(minutes=37 + r.randint(0, 20))).astimezone(W.NSW)
            if na.minute % 15 == 0:
                na -= timedelta(minutes=1)
            am["auth"] = na
            am["kind"] = "amended"
            am["result"] = x["result"] + "; amended"
            am["received"] = o["end"] + timedelta(minutes=r.uniform(2, 20))
            am["accession"] = namespaced(feed, x["plain"], na.date())      # sent by the replay on restart
            add.append(am)
        self.reports.extend(add)

    # ------------------------------------------------------------------------------------------ numbering
    def number_cases(self):
        """Case numbers run statewide in the order cases are opened: a case opens on its first accepted report, or
        when the unit enters a probable case."""
        self.index()
        for cs in self.cases:
            reps = self.of(cs)
            if reps:
                cs["created"] = min(x["received"] for x in reps)
            cs["created"] = cs["created"]
        order = sorted(self.cases, key=lambda cs: (cs["created"], cs["person"], cs["cond"]))
        r = rng("case-numbers")
        cur = {}
        for cs in order:
            y = nsw(cs["created"]).year
            if y not in cur:
                cur[y] = r.randint(1000, 9000)
            cur[y] += r.randint(8, 34)
            cs["case_no"] = "C%02d-%06d" % (y % 100, cur[y])
        for i in self.inv.invs:
            i.case_no = i.case["case_no"]
            for x in i.cases:
                x["case_no"] = x["case"]["case_no"]

    # ------------------------------------------------------------------------------------------ the log
    def condition_code(self, c, feed, received):
        d = nsw(received).date()
        legacy = d <= LEGACY_UNTIL or (feed == "HDN" and d <= HDN_LEGACY_UNTIL)
        return CONDITIONS[c][1] if legacy else CONDITIONS[c][2]

    def messages(self):
        r = rng("message-ids")
        cnt = {f: r.randint(10 ** 6, 9 * 10 ** 6) for f in ("CRBH", "LKS", "HF", "HDN", "KES", "SERL")}
        rows = []
        lo, hi = datetime(2022, 10, 1, tzinfo=W.NSW), datetime(2026, 11, 1, tzinfo=W.NSW)
        reps = [x for x in self.reports if x.get("received") and lo <= x["received"] < hi]
        reps.sort(key=lambda x: (x["received"], x["feed"], x["accession"], x["test"], x["status"]))
        for x in reps:
            feed = x["feed"]
            engine = "LKS" if feed == "LPG" or (feed == "HPS" and nsw(x["auth"]).date() >= P.ACQUISITION) else (
                "HF" if feed == "HPS" else feed)
            cnt[engine] += r.randint(1, 7)
            n = cnt[engine]
            if engine == "CRBH":
                mid = "CRBH%012d" % n
            elif engine == "LKS":
                mid = "LKS-%010d" % n
            elif engine == "HF":
                mid = "HF%09d" % n
            elif engine == "HDN":
                h = "%032x" % rng("hdn-mid", n).getrandbits(128)
                mid = "%s-%s-%s-%s-%s" % (h[:8], h[8:12], h[12:16], h[16:20], h[20:])
            elif engine == "KES":
                mid = "KQ%010d" % n
            else:
                mid = "SERL.%09d" % n
            msh = x["received"] - timedelta(seconds=r.randint(4, 95))
            if x["kind"] == "copy" or x.get("via_dr"):
                msh = x["received"] - timedelta(seconds=r.randint(2, 30))
            rows.append(dict(msg_control_id=mid, received_utc=utc_iso(x["received"]),
                             sending_facility=W.facility_code(feed, nsw(x["auth"]).date()),
                             msh_datetime=hl7(msh, feed), accession_no=x["accession"],
                             patient_ref=self.patient_ref(feed, x["person"], nsw(x["auth"]).date()),
                             specimen_collected=x["specimen"].isoformat(), test_code=x["test"],
                             result_status=x["status"], result_text=x["result"], authorised_at=hl7(x["auth"], feed),
                             condition_code=self.condition_code(x["case"]["cond"], feed, x["received"]),
                             ncp_case_no=x["case"]["case_no"], _rep=x))
        self.msgs = rows

    # ------------------------------------------------------------------------------------------ incident log
    def incident_log(self):
        """The interface team's incident log: outages the platform's feed monitoring raised, disaster-recovery
        failovers and restarts, planned maintenance and mapping changes."""
        r = rng("incidents")
        rows = []
        n = 0
        events = sorted(self.down, key=lambda o: (o["start"], o["feed"]))
        for o in events:
            feeds = ["LARKSPUR", "LARKSPUR-HF"] if o["feed"] == "LPG+HPS" else [W.facility_code(o["feed"], nsw(o["start"]).date())]
            if o["kind"] == "outage":
                if (o["end"] - o["start"]).total_seconds() < 3 * 3600 and r.random() < 0.5:
                    continue      # short outages that cleared before the monitor's threshold
                opened = o["start"] + timedelta(hours=2.0 + r.uniform(0.05, 0.6))
                if opened >= o["end"]:
                    continue
                hrs = (o["end"] - o["start"]).total_seconds() / 3600.0
                lab = f_name(feeds[0])
                lead = OUTAGE_LEAD[r.randrange(len(OUTAGE_LEAD))].format(lab=lab, Lab=_cap(lab), hrs="%.1f" % hrs)
                cause = OUTAGE_CAUSE[r.randrange(len(OUTAGE_CAUSE))].format(end=nsw(o["end"]).strftime("%H:%M"))
                text = lead + (_cap(cause) if lead.endswith(". ") else cause)
                for f in feeds:
                    n += 1
                    rows.append(["INC%06d" % (40000 + 37 * n), f, "Interface outage", "NCP feed monitoring",
                                 utc_iso(opened), utc_iso(o["end"] + timedelta(minutes=r.randint(4, 50))), text])
            elif o["kind"] == "dr":
                text = DR_TEXT[r.randrange(len(DR_TEXT))].format(dr=nsw(o["dr_from"]).strftime("%H:%M"),
                                                                 end=nsw(o["end"]).strftime("%H:%M"))
                for f in feeds:
                    n += 1
                    rows.append(["INC%06d" % (40000 + 37 * n), f, "Disaster recovery failover", "Laboratory",
                                 utc_iso(o["start"] + timedelta(minutes=r.randint(10, 40))),
                                 utc_iso(o["end"] + timedelta(minutes=r.randint(10, 60))), text])
            else:
                text = REPLAY_TEXT[r.randrange(len(REPLAY_TEXT))].format(start=nsw(o["start"]).strftime("%H:%M"),
                                                                         end=nsw(o["end"]).strftime("%H:%M"))
                for f in feeds:
                    n += 1
                    rows.append(["INC%06d" % (40000 + 37 * n), f, "Interface outage", "NCP feed monitoring",
                                 utc_iso(o["start"] + timedelta(hours=2.0 + r.uniform(0.05, 0.5))),
                                 utc_iso(o["end"] + timedelta(minutes=r.randint(5, 45))), text])
        extra = [
            (datetime(2024, 3, 1, 6, 0, tzinfo=W.NSW), datetime(2024, 3, 1, 9, 30, tzinfo=W.NSW), "LARKSPUR-HF",
             "Change", "Highfield Pathology Services results now sent from the Larkspur laboratory system; sending "
             "facility HIGHFIELD retired, LARKSPUR-HF from 1 March 2024."),
            (datetime(2025, 7, 1, 0, 30, tzinfo=W.NSW), datetime(2025, 7, 1, 5, 0, tzinfo=W.NSW), "NCP",
             "Change", "Condition code set 2025 loaded; incoming results mapped to the 2025 codes."),
            (datetime(2025, 11, 17, 10, 0, tzinfo=W.NSW), datetime(2025, 11, 17, 11, 15, tzinfo=W.NSW), "HALDEN",
             "Change", "Halden test-to-condition mapping updated to the 2025 code set."),
            (datetime(2026, 5, 3, 1, 0, tzinfo=W.NSW), datetime(2026, 5, 3, 4, 0, tzinfo=W.NSW), "CRBH-MICRO",
             "Planned maintenance", "Base hospital laboratory interface engine patched (Sunday 01:00 to 04:00)."),
            (datetime(2025, 3, 9, 1, 0, tzinfo=W.NSW), datetime(2025, 3, 9, 3, 30, tzinfo=W.NSW), "HALDEN",
             "Planned maintenance", "Halden interface engine upgrade."),
        ]
        for a, b, f, cat, text in extra:
            n += 1
            rows.append(["INC%06d" % (40000 + 37 * n), f, cat, "NCP interface team", utc_iso(a), utc_iso(b), text])
        rows.sort(key=lambda x: (x[4], x[1]))
        header = ["incident_ref", "sending_facility", "category", "raised_by", "opened_utc", "resolved_utc", "summary"]
        return header, rows

    # ------------------------------------------------------------------------------------------ case extract
    def case_extract(self):
        """The enteric team's case extract: one row per case of an enteric condition, as the platform holds it; the
        notifying laboratory and date are the case's own first report when it was opened."""
        rows = []
        self.index()
        for cs in sorted(self.cases, key=lambda c: c["case_no"]):
            if cs["cond"] not in ENTERIC:
                continue
            reps = [x for x in self.of(cs) if x.get("received")]
            if reps:
                first = min(reps, key=lambda x: x["received"])
                lab = W.facility_code(first["feed"], nsw(first["auth"]).date())
                when = nsw(first["received"]).date()
            else:
                lab, when = "", nsw(cs["created"]).date()
            if not (date(2022, 10, 1) <= when <= date(2026, 10, 31)):
                continue
            r = rng("extract", cs["case_no"])
            age = cs.get("age")
            if age is None:
                age = r.randint(0, 80)
            band = "0-4" if age < 5 else "5-14" if age < 15 else "15-24" if age < 25 else "25-44" if age < 45 else \
                "45-64" if age < 65 else "65+"
            sex = cs.get("sex") or r.choice(["F", "M"])
            rows.append([cs["case_no"], CONDITIONS[cs["cond"]][0], cs["status"],
                         cs["merged_into"]["case_no"] if cs.get("merged_into") else "",
                         cs["onset"].isoformat() if cs.get("onset") else "", when.isoformat(), lab, band, sex,
                         cs.get("setting", "")])
        header = ["ncp_case_no", "condition", "case_status", "merged_into", "onset_date", "notified_date",
                  "notifying_facility", "age_group", "sex", "setting"]
        return header, rows
