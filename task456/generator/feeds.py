"""The three feeds as their systems record them, built from each hospital-day's flags (latent.flags): the daily
census survey (counts at 07:00, corrections resubmitted), the bed-status board's event log (every unit's status
changes in UTC, the facility codes renumbered on 8 December, emergency departments' Divert retired on 5 January)
and the transfer center's calls (two systems, the cut-over on 5 January carrying open cases across)."""
import datetime as dt
from zoneinfo import ZoneInfo

import numpy as np

import latent as LT
import roster as RO
import world as W

TZ = {"Eastern": ZoneInfo("America/New_York"), "Central": ZoneInfo("America/Chicago")}
UTC = dt.timezone.utc
CT = TZ["Central"]


def to_utc(local_naive, tz):
    return local_naive.replace(tzinfo=TZ[tz]).astimezone(UTC).replace(tzinfo=None)


def local_date(utc_naive, tz):
    return utc_naive.replace(tzinfo=UTC).astimezone(TZ[tz]).date()


def ct_to_local_date(ct_naive, tz):
    return ct_naive.replace(tzinfo=CT).astimezone(TZ[tz]).date()


# ---------------------------------------------------------------------------------------------- census survey
def survey(hosp, F):
    """one row per submission: (licence, date, submitted local datetime, staffed, patients, vent, boarders, peds
    staffed, peds patients, med-surg staffed, med-surg patients, corrected flag); the latest submission of a hospital
    and date is its report"""
    rng = np.random.default_rng(W.SEED + 20)
    late = np.random.default_rng(W.SEED + 21)           # when a slip's first submission went in
    out = []
    for h in hosp:
        base = h["beds"]
        drift = 0
        has_picu = rng.random() < (0.45 if h["beds"] >= 16 else 0.08)
        ms_base = int(base * rng.uniform(4.0, 7.0))
        for d in LT.days():
            if rng.random() < 0.06:
                drift = int(np.clip(drift + rng.choice([-1, 1]), -2, 2))
            a = F[(h["licence"], d)][0]
            if a is None:
                continue
            staffed = max(3, base + drift)
            if a == 1:
                patients = staffed + (1 if rng.random() < 0.08 else 0)
            else:
                free = int(min(staffed, 1 + rng.poisson(0.22 * staffed)))
                patients = staffed - free
            vent = int(rng.binomial(patients, rng.uniform(0.40, 0.62)))
            boarders = int(rng.poisson(0.35 + 0.05 * staffed / 8)) if patients >= staffed else 0
            ps = int(rng.integers(4, 13)) if has_picu else 0
            pp = int(rng.integers(0, ps + 1)) if has_picu else 0
            mss = ms_base + int(rng.integers(-4, 5))
            msp = int(min(mss, rng.binomial(mss, 0.86)))
            t_final = dt.datetime.combine(d, dt.time(7, 25)) + dt.timedelta(minutes=int(rng.integers(0, 215)))
            row = dict(licence=h["licence"], date=d, staffed=staffed, patients=patients, vent=vent, boarders=boarders,
                       picu_staffed=ps, picu_patients=pp, ms_staffed=mss, ms_patients=msp)
            if rng.random() < 0.05:
                # a first submission with a keying slip, corrected later the same day
                first = dict(row)
                slip = rng.choice(["staffed", "patients", "vent"])
                if slip == "staffed":
                    first["staffed"] = staffed + int(rng.choice([-2, -1, 1, 10]))
                elif slip == "patients":
                    first["patients"] = max(0, patients + int(rng.choice([-1, 1, 2])))
                else:
                    first["vent"] = min(patients, vent + 1)
                first["submitted"] = t_final - dt.timedelta(minutes=int(rng.integers(40, 160)))
                floor = dt.datetime.combine(d, dt.time(7, 3))
                if first["submitted"] < floor + dt.timedelta(minutes=4):
                    span = max(1, int((t_final - floor).total_seconds() // 60) - 12)
                    first["submitted"] = floor + dt.timedelta(minutes=int(late.integers(1, span + 1)))
                out.append(first)
                row["submitted"] = t_final + dt.timedelta(minutes=int(rng.integers(30, 240)))
            else:
                row["submitted"] = t_final
            out.append(row)
    return out


# ------------------------------------------------------------------------------------------------ the board
ICU_LABELS = ["Adult ICU", "ICU", "MICU/SICU", "Critical Care Unit", "Adult Critical Care", "Intensive Care"]
OTHER_UNITS = [("Emergency Department", 1.0), ("Med/Surg", 1.0), ("PICU", 0.0), ("NICU", 0.30),
               ("Behavioral Health", 0.25), ("Labor & Delivery", 0.5)]


def _units(h, rng):
    units = [("ICU", ICU_LABELS[int(rng.integers(0, len(ICU_LABELS)))])]
    for name, p in OTHER_UNITS:
        if name == "PICU":
            p = 0.45 if h["beds"] >= 16 else 0.05
        if rng.random() < p:
            label = {"Emergency Department": ["Emergency Department", "ED", "Emergency Dept"],
                     "Med/Surg": ["Med/Surg", "Medical-Surgical", "Med Surg 4W"], "PICU": ["PICU", "Pediatric ICU"],
                     "NICU": ["NICU", "Neonatal ICU"], "Behavioral Health": ["Behavioral Health", "BHU"],
                     "Labor & Delivery": ["Labor & Delivery", "L&D"]}[name]
            units.append((name, label[int(rng.integers(0, len(label)))]))
    return units


def _icu_timeline(h, F, rng, first=dt.datetime(2025, 10, 31, 14, 5)):
    """the adult ICU line's status changes in local time: Closed at some time on exactly the days the board flags"""
    D = LT.days()
    ev = [(first, "Open", "")]
    carry_until = None
    for i, d in enumerate(D):
        b = F[(h["licence"], d)][1]
        nxt = F[(h["licence"], D[i + 1])][1] if i + 1 < len(D) else 0
        day0 = dt.datetime.combine(d, dt.time(0, 0))
        if carry_until is not None:
            ev.append((carry_until, "Open" if rng.random() < 0.8 else "Limited", ""))
            if ev[-1][1] == "Limited":
                ev.append((carry_until + dt.timedelta(minutes=int(rng.integers(40, 300))), "Open", ""))
            last_end = ev[-1][0]
            carry_until = None
        else:
            last_end = day0
        if b == 1:
            if last_end > day0 and rng.random() < 0.6:
                continue                    # the carried closure was the day's closure
            lo = max(last_end + dt.timedelta(minutes=25), day0 + dt.timedelta(hours=5))
            start = lo + dt.timedelta(minutes=int(rng.integers(0, max(1, int((day0 + dt.timedelta(hours=22, minutes=30)
                                                                              - lo).total_seconds() // 60)))))
            if rng.random() < 0.45:
                ev.append((start - dt.timedelta(minutes=int(rng.integers(20, 90))), "Limited", ""))
            rng.integers(0, 6)                       # (a draw kept so the timelines stay as built)
            ev.append((start, "Closed", ""))
            end = start + dt.timedelta(minutes=int(rng.integers(80, 600)))
            midnight = day0 + dt.timedelta(days=1)
            if end >= midnight - dt.timedelta(minutes=5):
                if nxt == 1 and rng.random() < 0.7:
                    carry_until = midnight + dt.timedelta(minutes=int(rng.integers(30, 540)))
                    if midnight.date() == W.BOARD_MIGRATION_UTC.date():
                        # the board's migration ran at 03:00 Central on 8 December with every adult ICU line open
                        carry_until = min(carry_until, midnight + dt.timedelta(hours=2, minutes=40))
                    continue
                end = midnight - dt.timedelta(minutes=int(rng.integers(6, 45)))
            ev.append((end, "Open" if rng.random() < 0.7 else "Limited", ""))
            if ev[-1][1] == "Limited" and end < midnight - dt.timedelta(minutes=70):
                ev.append((end + dt.timedelta(minutes=int(rng.integers(20, 60))), "Open", ""))
        else:
            if rng.random() < 0.35:
                s = max(last_end + dt.timedelta(minutes=30), day0 + dt.timedelta(hours=int(rng.integers(8, 20))))
                e = s + dt.timedelta(minutes=int(rng.integers(45, 360)))
                if e < day0 + dt.timedelta(hours=23, minutes=50):
                    ev.append((s, "Limited", ""))
                    ev.append((e, "Open", ""))
    # drop a status that repeats the one before it
    clean = []
    for t, s, r in sorted(ev, key=lambda x: x[0]):
        if clean and clean[-1][1] == s:
            continue
        clean.append((t, s, r))
    return clean


ED_REASONS = ["high volume", "boarding", "CT down", "staffing", "awaiting inpatient beds", "lab delay"]


def _ed_words(h):
    """how a hospital's charge nurses write an ordinary advisory's reason (their own wording, from their own stream)"""
    rng = np.random.default_rng([W.SEED + 36, int(h["licence"])])
    forms = {"high volume": ["high volume", "High volume", "volume", "high census"],
             "boarding": ["boarding", "boarding %d", "%d boarders", "boarding pts"],
             "CT down": ["CT down", "CT down until %d00", "CT scanner down", "CT maint"],
             "staffing": ["staffing", "RN staffing", "short staffed", "staffing - call outs"],
             "awaiting inpatient beds": ["awaiting inpatient beds", "holds awaiting beds", "waiting on IP beds"],
             "lab delay": ["lab delay", "lab down", "lab TAT", "lab analyzer down"]}

    def say(why):
        form = forms[why][int(rng.integers(0, len(forms[why])))]
        if "%d00" in form:
            return form % int(rng.integers(12, 23))
        if "%d" in form:
            return form % int(rng.integers(3, 14))
        return form
    return say


def _ed_timeline(h, rng, first=dt.datetime(2025, 10, 31, 14, 7), say=None):
    """an emergency department's statuses: Open, Advisory with a reason, and diversion: Divert until the board's
    5 January change, Advisory with the reason EMS diversion after it"""
    ev = [(first, "Open", "")]
    rate_div = 0.10 + 0.05 * (h["beds"] >= 16)
    switch_local = W.ED_SWITCH_UTC.replace(tzinfo=UTC).astimezone(TZ[h["tz"]]).replace(tzinfo=None)
    for d in LT.days():
        day0 = dt.datetime.combine(d, dt.time(0, 0))
        cursor = day0 + dt.timedelta(hours=7)
        if rng.random() < 0.22:
            s = cursor + dt.timedelta(minutes=int(rng.integers(0, 600)))
            e = s + dt.timedelta(minutes=int(rng.integers(60, 420)))
            why = ED_REASONS[int(rng.integers(0, len(ED_REASONS)))]
            ev.append((s, "Advisory", say(why) if say else why))
            ev.append((e, "Open", ""))
            cursor = e + dt.timedelta(minutes=30)
        if rng.random() < rate_div:
            s = max(cursor, day0 + dt.timedelta(hours=int(rng.integers(10, 21)), minutes=int(rng.integers(0, 60))))
            e = s + dt.timedelta(minutes=int(rng.integers(45, 300)))
            if s < switch_local:
                ev.append((s, "Divert", "EMS diversion" if rng.random() < 0.3 else ""))
            else:
                ev.append((s, "Advisory", "EMS diversion"))
            ev.append((e, "Open", ""))
    clean = []
    for t, s, r in sorted(ev, key=lambda x: x[0]):
        if clean and clean[-1][1] == s and clean[-1][2] == r:
            continue
        clean.append((t, s, r))
    return clean


def _other_timeline(rng, closable, first=dt.datetime(2025, 10, 31, 14, 9)):
    ev = [(first, "Open", "")]
    for d in LT.days():
        if rng.random() < 0.18:
            day0 = dt.datetime.combine(d, dt.time(0, 0))
            s = day0 + dt.timedelta(hours=int(rng.integers(7, 21)), minutes=int(rng.integers(0, 60)))
            st = "Closed" if (closable and rng.random() < 0.3) else "Limited"
            ev.append((s, st, ""))
            ev.append((s + dt.timedelta(minutes=int(rng.integers(60, 420))), "Open", ""))
    clean = []
    for t, s, r in sorted(ev, key=lambda x: x[0]):
        if clean and clean[-1][1] == s:
            continue
        clean.append((t, s, r))
    return clean


SET_BY = ["house supervisor", "charge nurse", "bed manager", "nursing supervisor"]


def _roles(h, kind):
    """the roles that set a unit's status at a hospital, and how often each does: small hospitals have no bed
    manager, and emergency departments are set mostly by their charge nurses"""
    rng = np.random.default_rng([W.SEED + 33, int(h["licence"]), len(kind)])
    a = np.array([2.0, 3.0, 1.5, 1.0]) if kind != "Emergency Department" else np.array([0.8, 6.0, 0.6, 0.5])
    if h["beds"] < 12:
        a[2] = 1e-9
    p = rng.dirichlet(a)
    p[p < 0.02] = 0.0
    return rng, p / p.sum()


def _with_confirmations(tl, rng):
    """the board asks each unit to confirm its status at least every eight hours; a confirmation logs the status
    the unit already has (and its reason) again"""
    out = []
    end = dt.datetime(2026, 1, 20, 6, 0)
    for i, (t0, s, r) in enumerate(tl):
        out.append((t0, s, r))
        t1 = tl[i + 1][0] if i + 1 < len(tl) else end
        c = t0 + dt.timedelta(minutes=int(rng.integers(240, 480)))
        while c < t1 - dt.timedelta(minutes=10):
            out.append((c, s, r))
            c += dt.timedelta(minutes=int(rng.integers(240, 480)))
    return out


def board(hosp, F):
    """every status event of every unit line: (utc datetime, facility code as logged, unit label, status, reason,
    set by, licence, unit kind); each hospital's units and each unit line draw from their own random streams"""
    rows = []
    kinds = ["ICU"] + [k for k, _ in OTHER_UNITS]
    for h in hosp:
        units = _units(h, np.random.default_rng([W.SEED + 30, int(h["licence"])]))
        for kind, label in units:
            rng = np.random.default_rng([W.SEED + UNIT_STREAM, int(h["licence"]), kinds.index(kind)])
            t0 = np.random.default_rng([W.SEED + 34, int(h["licence"]), kinds.index(kind)])
            first = dt.datetime(2025, 10, 31, 6, 0) + dt.timedelta(minutes=int(t0.integers(0, 960)))
            if kind == "ICU":
                tl = _icu_timeline(h, F, rng, first)
            elif kind == "Emergency Department":
                tl = _ed_timeline(h, np.random.default_rng([W.SEED + ED_STREAM, int(h["licence"])]), first,
                                  _ed_words(h))
            else:
                tl = _other_timeline(rng, kind in ("PICU", "NICU", "Behavioral Health"), first)
            tl = _with_confirmations(tl, rng)
            rr, rp = _roles(h, kind)
            last = None
            for t_local, status, reason in tl:
                u = to_utc(t_local, h["tz"])
                if u > dt.datetime(2026, 1, 20, 11, 59):
                    break
                if last is not None and last < W.BOARD_MIGRATION_UTC <= u:
                    rows.append((W.BOARD_MIGRATION_UTC, h["board_code"], label, cur, "", "system migration",
                                 h["licence"], kind))
                code = h["board_code_old"] if u < W.BOARD_MIGRATION_UTC else h["board_code"]
                rng.integers(0, 4)                   # (a draw kept so the streams stay as built)
                rows.append((u, code, label, status, reason, SET_BY[int(rr.choice(4, p=rp))], h["licence"], kind))
                last, cur = u, status
            if last is not None and last < W.BOARD_MIGRATION_UTC:
                rows.append((W.BOARD_MIGRATION_UTC, h["board_code"], label, cur, "", "system migration",
                             h["licence"], kind))
    rows.sort(key=lambda r: (r[0], r[1], r[2]))
    return rows


ED_STREAM = 39
UNIT_STREAM = 106


# ------------------------------------------------------------------------------------------ the transfer center
REASONS_OLD = {"bed": "NB", "staff": "NS", "svc": "SP", "pt": "OT", "oth": "OT"}
REASONS_NEW = {"bed": "CAP", "staff": "CAP", "svc": "SVC", "pt": "PT", "oth": "OTH"}


def transfers(hosp, F):
    """the center's requests and calls in one list: each request dict with its calls; the exports are cut from it"""
    rng = np.random.default_rng(W.SEED + 40)
    by_lic = {h["licence"]: h for h in hosp}
    nonm = RO.nonmembers()
    region_strain = {r[0]: r[4] for r in W.REGIONS}
    members = list(hosp)
    D = LT.days()
    # the hospital-days the transfer center must show declined for no staffed bed
    need = {(h["licence"], d) for h in hosp for d in D if F[(h["licence"], d)][2] == 1}
    requests = []
    pat_seq = rng.permutation(np.arange(1000000, 9999999, 37))[:20000]
    pi = 0
    req_no = 250000
    for d in D:
        strain = LT.season_shape(d)
        n_icu = int(rng.poisson(16 + 22 * strain))
        n_sd = int(rng.poisson(5 + 3 * strain))
        n_pd = int(rng.poisson(1.5))
        for kind, n in (("Adult ICU", n_icu), ("Step-down", n_sd), ("Pediatric ICU", n_pd)):
            for _ in range(n if d < W.SEASON_END else n // 2):
                if rng.random() < 0.42:
                    s = nonm[int(rng.integers(0, len(nonm)))]
                    sender = dict(fid=s["fid"], tz=s["tz"], region=s["region"], member=False)
                else:
                    w = np.array([0.5 + 2.5 * region_strain[h["region"]] for h in members])
                    h = members[int(rng.choice(len(members), p=w / w.sum()))]
                    sender = dict(fid=h["licence"], tz=h["tz"], region=h["region"], member=True)
                minute = int(rng.choice(np.arange(0, 1440), p=_day_shape()))
                opened = dt.datetime.combine(d, dt.time(0, 0)) + dt.timedelta(minutes=minute)   # Central
                requests.append(dict(no=req_no, opened=opened, sender=sender, kind=kind,
                                     patient="P%07d" % int(pat_seq[pi]), calls=[]))
                req_no += int(rng.integers(1, 4))
                pi += 1
    requests.sort(key=lambda r: r["opened"])
    # keep adult ICU requests clear of the window's edges at the sending hospital
    for r in requests:
        tz = r["sender"]["tz"]
        loc = r["opened"].replace(tzinfo=CT).astimezone(TZ[tz]).replace(tzinfo=None)
        for edge in (dt.datetime.combine(W.WINDOW_START, dt.time(0, 0)),
                     dt.datetime.combine(W.WINDOW_END + dt.timedelta(days=1), dt.time(0, 0))):
            if abs((loc - edge).total_seconds()) < 2 * 3600:
                r["opened"] += dt.timedelta(hours=4) if loc >= edge else -dt.timedelta(hours=4)
    requests.sort(key=lambda r: (r["opened"], r["no"]))
    icu_targets = [h for h in members]
    for r in requests:
        t = r["opened"] + dt.timedelta(minutes=int(rng.integers(4, 25)))
        placed = False
        tried = set([r["sender"]["fid"]])
        ncalls = 0
        while not placed and ncalls < 7:
            # the center calls the sending region's hospitals first, then the larger units elsewhere
            same = [h for h in icu_targets if h["region"] == r["sender"]["region"] and h["licence"] not in tried]
            other = [h for h in icu_targets if h["licence"] not in tried]
            pool = same if (same and rng.random() < 0.55) else other
            if r["kind"] == "Adult ICU":
                due = [h for h in pool if (h["licence"], ct_to_local_date(t, h["tz"])) in need]
                if due and rng.random() < 0.75:
                    pool = due
            w = np.array([1.0 + h["beds"] / 10 for h in pool])
            tgt = pool[int(rng.choice(len(pool), p=w / w.sum()))]
            tried.add(tgt["licence"])
            ld = ct_to_local_date(t, tgt["tz"])
            c = F[(tgt["licence"], ld)][2] if ld <= W.SEASON_END else 0
            if r["kind"] == "Adult ICU" and c == 1:
                ans, why = "Declined", ("bed" if rng.random() < 0.7 else "staff")
                need.discard((tgt["licence"], ld))
            elif r["kind"] == "Adult ICU":
                if rng.random() < 0.62:
                    ans, why = "Accepted", ""
                else:
                    ans, why = "Declined", ("svc" if rng.random() < 0.6 else ("pt" if rng.random() < 0.5 else "oth"))
            else:
                u = rng.random()
                ans, why = ("Accepted", "") if u < 0.55 else ("Declined", ["bed", "svc", "pt"][int(rng.integers(0, 3))])
            r["calls"].append(dict(t=t, to=tgt["licence"], answer=ans, why=why))
            ncalls += 1
            placed = ans == "Accepted"
            t = t + dt.timedelta(minutes=int(rng.integers(6, 45)))
        r["placed"] = placed
        if placed and rng.random() < 0.06:
            r["calls"].append(dict(t=t + dt.timedelta(minutes=int(rng.integers(50, 360))), to=r["calls"][-1]["to"],
                                   answer="Cancelled", why=""))
            r["cancelled"] = True
        else:
            r["cancelled"] = False
        if not placed:
            r["calls"].append(dict(t=t + dt.timedelta(minutes=10), to="", answer="No placement", why=""))
    # every hospital-day the center must show declined gets its call on an open adult ICU request that day
    icu_reqs = [r for r in requests if r["kind"] == "Adult ICU"]
    for lic, d in sorted(need):
        h = by_lic[lic]
        day_start = dt.datetime.combine(d, dt.time(6, 30)).replace(tzinfo=TZ[h["tz"]]).astimezone(CT).replace(tzinfo=None)
        cands = [r for r in icu_reqs if day_start <= r["opened"] <= day_start + dt.timedelta(hours=14)
                 and r["sender"]["fid"] != lic and all(c["to"] != lic for c in r["calls"])]
        r = cands[int(rng.integers(0, len(cands)))]
        first = r["calls"][0]["t"]
        t = max(r["opened"] + dt.timedelta(minutes=3), first - dt.timedelta(minutes=int(rng.integers(5, 30))))
        if ct_to_local_date(t, h["tz"]) != d:
            t = first + dt.timedelta(minutes=1)
        assert ct_to_local_date(t, h["tz"]) == d
        r["calls"].insert(0, dict(t=t, to=lic, answer="Declined", why="bed" if rng.random() < 0.7 else "staff"))
        r["calls"].sort(key=lambda c: c["t"])
    # a patient placed and later moved on from the accepting hospital asks again from there
    extra = []
    for r in requests:
        if r["kind"] == "Adult ICU" and r["placed"] and not r["cancelled"] and rng.random() < 0.03:
            acc = [c for c in r["calls"] if c["answer"] == "Accepted"][-1]
            h = by_lic[acc["to"]]
            opened = acc["t"] + dt.timedelta(hours=int(rng.integers(30, 140)))
            if opened > dt.datetime(2026, 1, 19, 12, 0):
                continue
            extra.append(dict(no=None, opened=opened, sender=dict(fid=h["licence"], tz=h["tz"], region=h["region"],
                              member=True), kind="Adult ICU", patient=r["patient"], calls=[], repeat=True))
    for r in extra:
        t = r["opened"] + dt.timedelta(minutes=int(rng.integers(5, 20)))
        while True:
            pool = [h for h in icu_targets if h["licence"] != r["sender"]["fid"] and h["beds"] >= 16]
            tgt = pool[int(rng.integers(0, len(pool)))]
            ld = ct_to_local_date(t, tgt["tz"])
            if ld <= W.SEASON_END and F[(tgt["licence"], ld)][2] == 1:
                r["calls"].append(dict(t=t, to=tgt["licence"], answer="Declined", why="bed"))
            elif any(c["to"] == tgt["licence"] for c in r["calls"]):
                pass
            else:
                r["calls"].append(dict(t=t, to=tgt["licence"], answer="Accepted", why=""))
                break
            t += dt.timedelta(minutes=int(rng.integers(8, 30)))
        r["placed"], r["cancelled"] = True, False
    requests = sorted(requests + extra, key=lambda r: r["opened"])
    no = 250000
    for r in requests:
        if r.get("no") is None or r.get("repeat"):
            pass
        r["no"] = no
        no += int(rng.integers(1, 4))
    return requests


_SHAPE = None


def _day_shape():
    global _SHAPE
    if _SHAPE is None:
        m = np.arange(1440)
        w = 0.4 + np.exp(-((m - 900) / 260.0) ** 2) + 0.5 * np.exp(-((m - 1260) / 120.0) ** 2)
        _SHAPE = w / w.sum()
    return _SHAPE
