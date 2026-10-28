"""task179 reference solution, computed from the shipped files under target/ only.

The call: the people with an open Region 4 episode at the end of 31 December 2026, counted once, who are booked into
the Darrow or the Keswick County jail at least once in 2027 on a new charge Directive 26-07's Category V lists, while
still under Region 4 supervision; the golden forecasts it with a year-end risk model fitted on the 2018 to 2025 year
ends, each supervisee's own records joined to the city police's victim records by cleaned name and date of birth."""
from __future__ import annotations

import datetime as dt
import json
import os
import re
from collections import defaultdict
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

import codes as K
import common as C

TZ = ZoneInfo("America/Chicago")
OLD_TO_NEW = dict(K.OLD_TO_NEW)
SCHED_B = set(K.SCHEDULE_B)
FAMILY = dict(K.FAMILY)
YEARS = list(range(2018, 2026))          # training year ends; each one's outcome year is the next


# ------------------------------------------------------------------ loading
def load(target):
    d = {}
    d["epi"] = pd.read_csv(os.path.join(target, C.F_EPIS), dtype=str, keep_default_na=False)
    d["xw"] = pd.read_csv(os.path.join(target, C.F_XWALK), dtype=str, keep_default_na=False)
    d["ras"] = pd.read_csv(os.path.join(target, C.F_ASSESS), dtype=str, keep_default_na=False)
    d["dj"] = pd.read_csv(os.path.join(target, C.F_DARROW), dtype=str, keep_default_na=False)
    d["kj"] = pd.read_excel(os.path.join(target, C.F_KESWICK), dtype=object, keep_default_na=False, na_values=[])
    d["hpd"] = pd.read_csv(os.path.join(target, C.F_HPD), dtype=str, keep_default_na=False)
    d["gps"] = json.load(open(os.path.join(target, C.F_GPS)))
    return d


def new_code(s):
    s = str(s).strip()
    if s in SCHED_B or s in FAMILY:
        return s
    return OLD_TO_NEW.get(s, s)


# ------------------------------------------------------------------ supervision
class Supervision:
    """person-level Region 4 supervision from the case-management episodes; an episode is open from its start date
    through its close date (Directive 26-07, section 2), or, as the alternative reading, until its close date"""
    def __init__(self, epi, inclusive=True):
        e = epi.copy()
        e["start"] = pd.to_datetime(e["start_date"]).dt.date
        e["close"] = e["close_date"].map(lambda x: dt.date.fromisoformat(x) if x else None)
        e["exp"] = pd.to_datetime(e["expiration_date"]).dt.date
        self.e = e
        self.inclusive = inclusive
        self.by_person = defaultdict(list)
        for row in e.itertuples(index=False):
            self.by_person[row.cms_person_id].append(row)
        for k in self.by_person:
            self.by_person[k].sort(key=lambda r: r.start)
        self.sid_to_pid = dict(zip(e["sid"], e["cms_person_id"]))

    def _open(self, r, d):
        if r.start > d:
            return False
        if r.close is None:
            return True
        return r.close >= d if self.inclusive else r.close > d

    def open_on(self, pid, d):
        """episodes open at the end of day d"""
        return [r for r in self.by_person.get(pid, []) if self._open(r, d)]

    def supervised(self, pid, d):
        """under Region 4 supervision during day d (an episode open that day)"""
        return any(r.start <= d and (r.close is None or r.close >= d) for r in self.by_person.get(pid, []))

    def caseload(self, d, episodes=False):
        e = self.e
        if self.inclusive:
            m = (e["start"] <= d) & (e["close"].map(lambda c: c is None or c >= d))
        else:
            m = (e["start"] <= d) & (e["close"].map(lambda c: c is None or c > d))
        if episodes:
            return list(e.loc[m, "cms_person_id"])
        return sorted(set(e.loc[m, "cms_person_id"]))

    merge_transfers = True

    def spell_start(self, pid, d):
        """the start of the continuous Region 4 supervision that covers day d"""
        eps = [r for r in self.by_person[pid]]
        cur = None
        for r in eps:
            if r.start <= d and (r.close is None or r.close >= d):
                cur = r if cur is None or r.start < cur.start else cur
        if cur is None:
            return None
        s = cur.start
        changed = self.merge_transfers
        while changed:
            changed = False
            for r in eps:
                if r.close is not None and r.start < s and (s - r.close).days <= 1:
                    s = r.start
                    changed = True
        return s


# ------------------------------------------------------------------ bookings
def bookings(d, utc=True, group_rows=True):
    """one row per booking from both jails, local time, new-section charges (utc=False keeps Keswick's UTC clock;
    group_rows=False reads each Darrow charge row as a booking)"""
    dj = d["dj"]
    out = []
    groups = dj.groupby("booking_no", sort=False) if group_rows else ((k, dj.iloc[[k]]) for k in range(len(dj)))
    for bno, g in groups:
        r0 = g.iloc[0]
        booked = dt.datetime.strptime(r0["booked"], "%Y-%m-%d %H:%M")
        rel = dt.datetime.strptime(r0["released"], "%Y-%m-%d %H:%M") if r0["released"] else None
        ch = [new_code(s) for s in g["statute"] if s]
        typ = r0["booking_type"]
        out.append(dict(jail="D", bno=bno, sid=r0["sid"], booked=booked, released=rel, rel_reason=r0["release_reason"],
                        type="NEW ARREST" if typ == "NEW ARREST" else typ, agency=r0["arresting_agency"],
                        case=r0["agency_case_no"], charges=ch))
    kj = d["kj"]
    conv = (lambda t: t.replace(tzinfo=dt.timezone.utc).astimezone(TZ).replace(tzinfo=None)) if utc else (lambda t: t)
    for row in kj.itertuples(index=False):
        b = conv(pd.Timestamp(row[1]).to_pydatetime())
        rel = None
        if row[2] not in (None, ""):
            rel = conv(pd.Timestamp(row[2]).to_pydatetime())
        ch = []
        if isinstance(row[10], str) and row[10] != "PROB/PAROLE VIOLATION":
            for part in row[10].split(" | "):
                ch.append(new_code(part.split(" ")[0]))
        typ = {"NA": "NEW ARREST", "WT": "WARRANT", "PV": "VIOLATION", "RH": "RETURN FROM HOSPITAL"}[row[7]]
        out.append(dict(jail="K", bno=row[0], sid=row[4], booked=b, released=rel, rel_reason=row[3] or "",
                        type=typ, agency=row[8], case=str(row[9]), charges=ch))
    bk = pd.DataFrame(out)
    bk["date"] = bk["booked"].map(lambda t: t.date())
    bk["new"] = bk["type"] == "NEW ARREST"
    bk["schedb"] = bk["charges"].map(lambda cs: any(c in SCHED_B for c in cs))
    return bk


# ------------------------------------------------------------------ the police's victims
def norm_last(s):
    s = re.sub(r"\b(JR|SR|II|III|IV)\b\.?", " ", s.upper())
    return re.sub(r"[^A-Z]", "", s)


def norm_first(s):
    return re.sub(r"[^A-Z]", "", s.upper())


def victim_links(d, sup, use="occurred", fuzzy=False, clean=True):
    """person id -> sorted dates the city police recorded the person as an individual victim"""
    e = sup.e
    key = {}
    nl = norm_last if clean else (lambda x: x.upper().strip())
    nf = norm_first if clean else (lambda x: x.upper().strip())
    for row in e.drop_duplicates("cms_person_id").itertuples(index=False):
        # the police write a victim LAST, FIRST MIDDLE, so a two-word given name meets its first word
        given = row.first_name.split(" ")[0] if clean else row.first_name
        key[(nl(row.last_name), nf(given), row.date_of_birth)] = row.cms_person_id
    h = d["hpd"]
    h = h[(h["victim_type"] == "I") & (h["victim_name"] != "JUVENILE")]
    col = "occurred_date" if use == "occurred" else "report_date"
    out = defaultdict(set)
    nick = {}
    if fuzzy:
        import names as NM
        nick = {v.upper(): k.upper() for k, v in NM.NICKNAMES.items()}
    for nm, dob, dd in zip(h["victim_name"], h["victim_dob"], h[col]):
        if not dob:
            continue
        last, rest = nm.split(", ", 1)
        first = rest.split(" ")[0]
        dob_iso = "%s-%s-%s" % (dob[6:10], dob[0:2], dob[3:5])
        k = (nl(last), nf(first), dob_iso)
        pid = key.get(k)
        if pid is None and fuzzy and first in nick:
            pid = key.get((nl(last), nf(nick[first]), dob_iso))
        if pid is not None:
            out[pid].add(dt.date(int(dd[6:10]), int(dd[0:2]), int(dd[3:5])))
    return {k: sorted(v) for k, v in out.items()}


# ------------------------------------------------------------------ panel
def assessments_by_person(d, xwalk=True, std_score=False):
    ras = d["ras"]
    if xwalk == "first":
        x = d["xw"][~d["xw"]["conversion_note"].str.contains("MERGED|DUPLICATE")]
        xw = dict(zip(x["legacy_offender_number"], x["cms_person_id"]))
    else:
        xw = dict(zip(d["xw"]["legacy_offender_number"], d["xw"]["cms_person_id"])) if xwalk else {}
    pid = ras["offender_ref"].map(lambda x: xw.get(x, x))
    a = pd.DataFrame({"pid": pid, "date": pd.to_datetime(ras["assessment_date"]).dt.date,
                      "score": ras["total_score"].astype(int), "inst": ras["instrument"]})
    if std_score:
        z = a.groupby("inst")["score"].transform(lambda x: (x - x.mean()) / x.std())
        a["score"] = 18 + 6 * z
    out = defaultdict(list)
    for r in a.itertuples(index=False):
        out[r.pid].append((r.date, r.score, r.inst))
    for k in out:
        out[k].sort()
    return out


def lead_family(code):
    c = new_code(code)
    return FAMILY.get(c, "OTHER")


class Panel:
    def __init__(self, d, sup, bk, links, ras, under_only=True, new_only=True, persons_once=True):
        self.d, self.sup, self.bk, self.links, self.ras = d, sup, bk, links, ras
        self.persons_once = persons_once
        b = bk.copy()
        b["pid"] = b["sid"].map(sup.sid_to_pid)
        b = b[b["pid"].notna()]
        # bookings while under Region 4 supervision
        b["under"] = [sup.supervised(p, dd) for p, dd in zip(b["pid"], b["date"])] if under_only else True
        self.b = b
        nb = b[(b["new"] | (not new_only)) & b["under"]]
        self.nb = nb
        self.nb_by = defaultdict(list)
        for p, dd, sb in zip(nb["pid"], nb["date"], nb["schedb"]):
            self.nb_by[p].append((dd, sb))

    def frame(self, Y, with_outcome=True):
        sup = self.sup
        o = dt.date(Y, 12, 31)
        pids = sup.caseload(o, episodes=not self.persons_once)
        rows = []
        for p in pids:
            eps = sup.open_on(p, o)
            main = [r for r in eps if r.lead_offense_statute]
            r0 = sorted(eps, key=lambda r: r.start)[0]
            dob = dt.date.fromisoformat(r0.date_of_birth)
            age = (o - dob).days / 365.25
            fam = lead_family(sorted(eps, key=lambda r: (r.start, r.episode_id))[0].lead_offense_statute)
            parole = any(r.supervision_type == "PAROLE" for r in eps)
            county = sorted(eps, key=lambda r: r.start)[-1].county
            city = any(r.residence_city == "Halverton" and r.county == "DARROW" for r in eps)
            exp = max(r.exp for r in eps)
            rem = min(12.0, max(0.0, (exp - o).days / 30.4375))
            s0 = sup.spell_start(p, o)
            tos = (o - s0).days / 30.4375 if s0 else 0.0
            pri = max(int(r.prior_felony_convictions) for r in eps)
            sc = [x for x in self.ras.get(p, []) if x[0] <= o]
            score = sc[-1][1] if sc else np.nan
            hist = self.nb_by.get(p, [])
            n12 = sum(1 for dd, sb in hist if o - dt.timedelta(days=365) < dd <= o)
            b12 = int(any(sb for dd, sb in hist if o - dt.timedelta(days=365) < dd <= o))
            vd = self.links.get(p, [])
            v12 = int(any(o - dt.timedelta(days=365) < x <= o for x in vd))
            v24 = int(any(o - dt.timedelta(days=730) < x <= o - dt.timedelta(days=365) for x in vd))
            vev = int(any(x <= o for x in vd))
            v6 = int(any(o - dt.timedelta(days=182) < x <= o for x in vd))
            v6_12 = int(any(o - dt.timedelta(days=365) < x <= o - dt.timedelta(days=182) for x in vd))
            vc12 = min(3, sum(1 for x in vd if o - dt.timedelta(days=365) < x <= o))
            y = np.nan
            if with_outcome:
                y = int(any(sb for dd, sb in hist if dt.date(Y + 1, 1, 1) <= dd <= dt.date(Y + 1, 12, 31)))
            rows.append(dict(pid=p, Y=Y, age=age, male=int(r0.sex == "M"), lpri=np.log1p(pri), fam=fam, parole=int(parole),
                             keswick=int(county == "KESWICK"), city=int(city), rem=rem, tos12=int(tos < 12), score=score,
                             n12=min(3, n12), b12=b12, v12=v12, v24=v24, vever=vev, v6=v6, v6_12=v6_12, vc12=vc12, y=y))
        f = pd.DataFrame(rows)
        for fm in ("VIOLENT", "WEAPON", "PROPERTY", "DRUG", "DUI"):
            f["f_" + fm] = (f["fam"] == fm).astype(int)
        f["score"] = f["score"].fillna(f["score"].median() if f["score"].notna().any() else 17.0)
        return f


BASE = ["age", "male", "lpri", "f_VIOLENT", "f_WEAPON", "f_PROPERTY", "f_DRUG", "f_DUI", "parole", "keswick", "city",
        "rem", "tos12", "score", "n12", "b12"]
FORMS = {"own attributes": [], "victim 12 months": ["v12"], "victim 12 and 24 months": ["v12", "v24"],
         "victim 6 and 6-12 months": ["v6", "v6_12"], "victim count 12 months": ["vc12"], "victim ever": ["vever"],
         "victim 12, 24 and ever": ["v12", "v24", "vever"]}


def fit(train, feats):
    import statsmodels.api as sm
    X = sm.add_constant(train[feats].astype(float))
    m = sm.Logit(train["y"].astype(float), X).fit(disp=0, maxiter=200)
    return m


def predict(m, f, feats):
    import statsmodels.api as sm
    X = sm.add_constant(f[feats].astype(float), has_constant="add")
    return float(m.predict(X).sum())


class Solution:
    """the golden reading by default; each option is one alternative reading or one mess item mishandled"""
    def __init__(self, target, data=None, inclusive=True, utc=True, group_rows=True, new_only=True, xwalk=True,
                 std_score=False, persons_once=True, victim_date="occurred", fuzzy=False, under_only=True, years=None,
                 clean_names=True, merge_transfers=True):
        self.d = data if data is not None else load(target)
        self.sup = Supervision(self.d["epi"], inclusive=inclusive)
        self.sup.merge_transfers = merge_transfers
        self.bk = bookings(self.d, utc=utc, group_rows=group_rows)
        self.links = victim_links(self.d, self.sup, use=victim_date, fuzzy=fuzzy, clean=clean_names)
        self.ras = assessments_by_person(self.d, xwalk=xwalk, std_score=std_score)
        self.panel = Panel(self.d, self.sup, self.bk, self.links, self.ras, under_only=under_only, new_only=new_only,
                           persons_once=persons_once)
        self.years = years or YEARS
        self.frames = {Y: self.panel.frame(Y, with_outcome=(Y < 2026)) for Y in sorted(set(self.years) | set(YEARS)) + [2026]}
        self.train = pd.concat([self.frames[Y] for Y in self.years], ignore_index=True)
        self.f26 = self.frames[2026]

    def forecast(self, form, train=None, f=None):
        feats = BASE + FORMS[form]
        m = fit(self.train if train is None else train, feats)
        return predict(m, self.f26 if f is None else f, feats), m

    def all_forms(self):
        out = {}
        for k in FORMS:
            v, m = self.forecast(k)
            out[k] = (v, m.aic, m.llf)
        return out


# ------------------------------------------------------------------ ask A: Belvantis enrolment days owed, 2026
def custody_days(bk, sid):
    """the days person sid was held in either county jail for any part of the day, from both jails' records"""
    days = set()
    sel = bk["sid"] == sid
    for t, rl in zip(bk.loc[sel, "booked"], bk.loc[sel, "released"]):
        a = t.date()
        b = C.RECORDS_END if (rl is None or pd.isna(rl)) else rl.date()
        x = a
        while x <= b:
            days.add(x)
            x += dt.timedelta(days=1)
    return days


def _ref_days(g):
    """held and suspended days of one vendor record (one client reference), from its effective dates; Schedule C.2: a
    suspension runs from its effective date through the effective date of the resumption that answers it (the first
    one on or after it), so a suspension and a resumption on the same date suspend that one day"""
    held, susp = set(), set()
    on = None
    sus, res = [], []
    for e, d in zip(g["event"], g["eff"]):
        if e == "ENROL":
            if on is None:
                on = d
        elif e in ("END", "ACCOUNT_TRANSFER") and on is not None:
            x = on
            while x <= d:
                held.add(x)
                x += dt.timedelta(days=1)
            on = None
        elif e == "SUSPEND":
            sus.append(d)
        elif e == "RESUME":
            res.append(d)
    if on is not None:
        x = on
        while x <= C.RECORDS_END:
            held.add(x)
            x += dt.timedelta(days=1)
    res = sorted(res)
    used = [False] * len(res)
    for a in sorted(sus):
        j = next((j for j, r in enumerate(res) if not used[j] and r >= a), None)
        b = C.RECORDS_END
        if j is not None:
            used[j] = True
            b = res[j]
        x = a
        while x <= b:
            susp.add(x)
            x += dt.timedelta(days=1)
    return held, susp


def gps_events(sol):
    ev = pd.DataFrame(sol.d["gps"]["events"])
    voided = set(ev.loc[ev["event"] == "VOID", "voids_event_id"])
    ev = ev[(ev["event"] != "VOID") & ~ev["event_id"].isin(voided)].copy()
    ev["eff"] = pd.to_datetime(ev["effective_date"]).dt.date
    order = {"ENROL": 0, "DEVICE_RETURN": 1, "DEVICE_ISSUE": 2, "SUSPEND": 3, "RESUME": 4, "END": 5, "ACCOUNT_TRANSFER": 6}
    ev["o"] = ev["event"].map(order)
    xw = dict(zip(sol.d["xw"]["legacy_offender_number"], sol.d["xw"]["cms_person_id"]))
    ev["pid"] = ev["client_ref"].map(lambda x: xw.get(x, x))
    return ev.sort_values(["client_ref", "eff", "o"])


def gps_days(sol):
    """Schedule C: a day per client on which the client holds an assigned device, less suspended days, days in
    either jail and days the client was not under Region 4 supervision; two vendor records of one person are one
    client"""
    ev = gps_events(sol)
    sup = sol.sup
    pid_to_sid = {v: k for k, v in sup.sid_to_pid.items()}
    held_p, susp_p = defaultdict(set), defaultdict(set)
    for ref, g in ev.groupby("client_ref"):
        h, s_ = _ref_days(g)
        p = g["pid"].iloc[0]
        held_p[p] |= h
        susp_p[p] |= s_
    months = defaultdict(int)
    detail = {}
    for p, held in held_p.items():
        sid = pid_to_sid.get(p)
        cust = custody_days(sol.bk, sid) if sid is not None else set()
        bill = [x for x in held if x.year == 2026 and x not in susp_p[p] and x not in cust and sup.supervised(p, x)]
        for x in bill:
            months[x.month] += 1
        detail[p] = len(bill)
    return [months[m] for m in range(1, 13)], detail


# ------------------------------------------------------------------ ask B: exclusion zones, 2026
def hpd_number(case, jail):
    case = str(case).strip()
    m = re.fullmatch(r"(\d{2})-(\d{6})", case) if jail == "D" else re.fullmatch(r"HPD(\d{2})(\d{6})", case)
    if not m:
        return None
    return "HPD-%s-%s" % (m.group(1), m.group(2))


STREET_WORDS = {"STREET": "ST", "AVENUE": "AVE", "DRIVE": "DR", "ROAD": "RD", "LANE": "LN", "COURT": "CT",
                "PLACE": "PL", "BOULEVARD": "BLVD", "APARTMENT": "UNIT", "APT": "UNIT", "#": "UNIT"}


def norm_addr(a):
    """a residence as one key: case, spacing, the unit mark and the street type written alike"""
    a = a.upper().replace(",", " ").replace(".", " ").replace("#", " # ")
    return " ".join(STREET_WORDS.get(t, t) for t in a.split())


def zones(sol):
    """Directive 26-07 section 4: for each supervisee booked on a new Category V charge after a Halverton police arrest,
    one zone per Halverton residence of the incident's victims, once per supervisee and incident, in the month of the
    first booking on that incident (Merrow time), 2026 bookings"""
    h = sol.d["hpd"]
    h = h[(h["victim_type"] == "I") & (h["victim_res_city"] == "HALVERTON") & (h["victim_residence"] != "")]
    res = defaultdict(set)
    for num, a in zip(h["incident_number"], h["victim_residence"]):
        res[num].add(norm_addr(a))
    nb = sol.panel.nb
    nb = nb[(nb["agency"] == "HPD") & nb["schedb"]].sort_values("booked")
    seen = set()
    cells = defaultdict(int)
    for p, case, jail, d in zip(nb["pid"], nb["case"], nb["jail"], nb["date"]):
        num = hpd_number(case, jail)
        if num is None or (p, num) in seen:
            continue
        seen.add((p, num))
        if d.year != 2026:
            continue
        cells[d.month] += len(res.get(num, ()))
    return [cells[m] for m in range(1, 13)]
