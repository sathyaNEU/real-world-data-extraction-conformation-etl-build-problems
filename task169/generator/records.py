"""Operating records cut from the truth: summer outages, the maintenance job log, the May 2026 count week and the
volunteer sheets, the public dashboard's monthly series, and the two background files."""
import math
from datetime import date, datetime, timedelta

import numpy as np
from zoneinfo import ZoneInfo

import names as N
import world as W

# ------------------------------------------------------------------ summer outages in the counts exports
# segment counters' summer spells recording nothing (local wall clock, to the minute); the dashboard counters'
# spells are in SPELLS below. An hour losing 30 minutes or more is an hour the counter did not record; an hour losing
# less is recorded with the riders of the minutes it kept.
SUMMER_OUTAGES = [
    ("MS4", "2024-07-09 06:12", "2024-07-12 23:40", "loop cut by a utility trench"),
    ("TR4", "2024-06-18 10:06", "2024-06-18 11:48", "battery change"),
    ("WP3", "2024-08-22 23:10", "2024-08-24 00:20", "cabinet forced open"),
    ("SF2", "2025-07-14 08:05", "2025-07-22 16:50", "loop cut during gas main works"),
    ("EP4", "2025-08-05 04:20", "2025-08-06 19:45", "salt water in the logger"),
    ("BF3", "2025-06-24 11:04", "2025-06-24 12:51", "battery change"),
    ("BF3", "2025-08-12 11:09", "2025-08-12 12:40", "battery change"),
    ("WP3", "2026-08-10 07:15", "2026-08-12 15:35", "cabinet vandalised"),
    ("TR2", "2026-06-23 14:03", "2026-06-23 14:56", "battery change"),
    ("EP3", "2026-07-01 02:20", "2026-07-02 18:40", "cabinet flooded in the storm"),
]
# overnight logger sleep at SF2 in August 2024 (legacy only), and platform estimates for short night gaps
SF2_SLEEP_2024 = [date(2024, 8, d) for d in (3, 4, 10, 11, 17, 18)]
ESTIMATED = [("WP3", date(2025, 6, d), (2, 3)) for d in (7, 8, 21, 22)] + \
            [("MS4", date(2026, 7, d), (3, 4)) for d in (4, 5, 11, 12, 18, 19, 25, 26)] + \
            [("MS3", date(2025, 8, d), (15,)) for d in (6, 13, 20)]


def _spans_for(code):
    out = [(a, b) for c, a, b, why in SUMMER_OUTAGES if c == code]
    for sp in SPELLS:
        if sp["code"] == code:
            out.append((sp["a"], sp["b"]))
            if sp.get("recur"):
                out.append((sp["recur"]["a"], sp["recur"]["b"]))
    return out


def lost_fraction(code, y, days):
    """days x 24, the share of each local clock hour the counter was recording nothing"""
    f = np.zeros((len(days), 24))
    pos = {d: i for i, d in enumerate(days)}
    for a, b in _spans_for(code):
        A, B = _dt(a), _dt(b)
        t = A.replace(minute=0)
        while t < B:
            t1 = t + timedelta(hours=1)
            lo, hi = max(t, A), min(t1, B)
            if hi > lo and t.date() in pos and t.year == y:
                f[pos[t.date()], t.hour] += (hi - lo).total_seconds() / 3600.0
            t = t1
    if code == "SF2" and y == 2024:
        for d in SF2_SLEEP_2024:
            for h in (1, 2, 3):
                f[pos[d], h] = 1.0
    return np.clip(f, 0, 1)


def outage_mask(code, y, days):
    """bool days x 24, True where the counter did not record the hour (local hours)"""
    return lost_fraction(code, y, days) >= 0.5


def estimated_mask(code, y, days):
    m = np.zeros((len(days), 24), bool)
    pos = {d: i for i, d in enumerate(days)}
    for c, d, hs in ESTIMATED:
        if c == code and d.year == y:
            for h in hs:
                m[pos[d], h] = True
    return m


# ------------------------------------------------------------------ the maintenance job log, 2024 to 2026
LONDON = ZoneInfo("Europe/London")


def _dt(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M")


def elapsed_min(a, b):
    """real minutes between two local wall-clock times (Europe/London), across a clock change"""
    A = _dt(a).replace(tzinfo=LONDON)
    B = _dt(b).replace(tzinfo=LONDON)
    return int(round((B.timestamp() - A.timestamp()) / 60))


def hmm(minutes):
    return "%d:%02d" % (minutes // 60, minutes % 60)


# Every spell a dashboard counter recorded nothing, 2024 to 2026: the job that opened it (code, job type, start, end,
# who logged it), the follow-up visits that only checked the repair (days after, hour, minute, visit minutes), and a
# visit that found the counter down again, which is a spell of its own. A fault the unit could not clear itself
# (by="TMU+CON") is the unit's job for the whole spell and the contractor's own job for its attendance inside it.
# The unit enters downtime as h:mm, the contractor's job system as minutes.
SPELLS = [
    # Tolland Road, Cathedral Green
    dict(code="TR1", jt="battery", a="2024-03-19 10:10", b="2024-03-19 11:37", by="TMU"),
    dict(code="TR1", jt="battery", a="2025-04-08 09:40", b="2025-04-08 11:12", by="TMU"),
    dict(code="TR1", jt="download", a="2025-09-16 14:05", b="2025-09-16 14:52", by="TMU"),
    dict(code="TR1", jt="fault", a="2025-10-25 19:55", b="2025-10-27 08:20", by="TMU",
         note="Logger not reporting overnight, loop joint found broken and remade", checks=[(9, 10, 5, 35)],
         recur=dict(a="2025-11-02 21:15", b="2025-11-03 06:50",
                    note="Counts dropped out again overnight, loop joint remade")),
    dict(code="TR1", jt="battery", a="2026-05-19 09:00", b="2026-05-19 10:16", by="TMU"),
    # Brickfields, Station Square
    dict(code="BF1", jt="battery", a="2024-10-01 09:20", b="2024-10-01 10:49", by="TMU"),
    dict(code="BF1", jt="vandalism", a="2025-03-22 18:10", b="2025-03-23 08:41", by="TMU", checks=[(3, 11, 20, 25)]),
    dict(code="BF1", jt="battery", a="2025-05-28 10:15", b="2025-05-28 12:17", by="TMU", asset="CVC-1180"),
    dict(code="BF1", jt="download", a="2025-10-07 13:30", b="2025-10-07 14:04", by="TMU"),
    dict(code="BF1", jt="power", a="2025-11-04 05:30", b="2025-11-04 12:44", by="TMU", checks=[(5, 9, 40, 30)],
         recur=dict(a="2025-11-06 01:10", b="2025-11-06 07:38",
                    note="Logger off again, lighting circuit tripped overnight and reset")),
    # Estuary Path, Quayside
    dict(code="EP1", jt="fault", a="2024-11-12 07:00", b="2024-11-13 16:34", by="TMU+CON",
         con=dict(a="2024-11-12 10:05", b="2024-11-13 16:10", note="No counts from loop B, cable traced and repaired"),
         checks=[(6, 13, 0, 40)]),
    dict(code="EP1", jt="battery", a="2025-03-11 11:00", b="2025-03-11 12:13", by="TMU"),
    dict(code="EP1", jt="fault", a="2025-03-29 21:30", b="2025-03-31 09:00", by="TMU+CON",
         con=dict(a="2025-03-31 07:35", b="2025-03-31 08:50", note="Detector board fault, board swapped"),
         checks=[(4, 10, 0, 45), (11, 14, 30, 30)]),
    dict(code="EP1", jt="battery", a="2025-07-17 10:10", b="2025-07-17 11:41", by="TMU"),
    dict(code="EP1", jt="download", a="2025-10-07 10:20", b="2025-10-07 10:49", by="TMU"),
    dict(code="EP1", jt="fault", a="2025-12-02 15:30", b="2025-12-03 11:04", by="TMU", checks=[(7, 9, 15, 30)],
         note="Logger not reporting, modem replaced"),
    # Wardle Park, Exchange Street
    dict(code="WP1", jt="battery", a="2025-06-03 09:00", b="2025-06-03 10:02", by="TMU"),
    dict(code="WP1", jt="vandalism", a="2025-10-31 21:00", b="2025-11-01 19:05", by="TMU",
         recur=dict(a="2025-11-03 22:40", b="2025-11-04 08:15",
                    note="Cabinet forced again overnight, logger reset and cabinet chained")),
    dict(code="WP1", jt="power", a="2025-12-31 18:30", b="2026-01-01 11:34", by="TMU",
         note="Supply lost when the park lighting failed; logger off until reconnected"),
    dict(code="WP1", jt="fault", a="2026-02-09 06:30", b="2026-02-10 15:28", by="TMU+CON",
         con=dict(a="2026-02-09 11:10", b="2026-02-10 15:05", note="Loop feeder cable damaged, joint remade"),
         checks=[(8, 10, 0, 30)]),
    # Market Street, Corn Exchange (the replaced unit carries the old id until 21 March 2025)
    dict(code="MS1", jt="fault", a="2025-02-24 08:00", b="2025-02-25 22:08", by="TMU+CON",
         con=dict(a="2025-02-24 13:20", b="2025-02-25 21:40", note="No counts from loop B, cable traced and repaired"),
         checks=[(6, 9, 30, 30)]),
    dict(code="MS1", jt="battery", a="2025-08-19 07:50", b="2025-08-19 09:35", by="TMU"),
    dict(code="MS1", jt="download", a="2025-10-08 11:00", b="2025-10-08 11:32", by="TMU"),
    dict(code="MS1", jt="battery", a="2026-04-21 08:40", b="2026-04-21 10:09", by="TMU",
         note="Battery pack changed, logger restarted from laptop"),
    # Southfield, Southgate
    dict(code="SF1", jt="vandalism", a="2024-12-31 22:30", b="2025-01-01 10:31", by="TMU", checks=[(6, 11, 0, 25)]),
    dict(code="SF1", jt="battery", a="2025-02-05 10:30", b="2025-02-05 12:04", by="TMU"),
    dict(code="SF1", jt="vandalism", a="2025-04-14 06:45", b="2025-04-15 13:01", by="TMU", checks=[(7, 10, 45, 30)]),
    dict(code="SF1", jt="power", a="2025-09-09 04:00", b="2025-09-09 10:03", by="TMU"),
    dict(code="SF1", jt="battery", a="2025-12-09 09:30", b="2025-12-09 10:43", by="TMU"),
]
# loggers restarted from the technician's laptop kept its local clock until the summer round reset them
LOCAL_CLOCK = {"EP1": ("2026-03-17", "2026-05-29"), "MS1": ("2026-04-21", "2026-05-29")}
NOTES = {
    "battery": ["Battery pack changed, logger restarted", "Low battery alarm, pack replaced on site",
                "Battery swap; logger time checked against phone", "Pack changed and seal renewed"],
    "fault": ["Loop feeder cable damaged, joint remade", "No counts from loop B, cable traced and repaired",
              "Logger not reporting, modem replaced", "Detector board fault, board swapped"],
    "vandalism": ["Cabinet door forced, logger reseated and door welded", "Cabinet damaged overnight, unit reset",
                  "Cables pulled from cabinet, reconnected"],
    "power": ["Street lighting circuit off, logger without supply until restored",
              "Supply lost after lighting works, reconnected by electrician"],
    "download": ["Manual download, logger paused during transfer", "Manual data download, counting stopped while connected"],
    "visit": ["Follow-up visit to check repair", "Return visit, counts confirmed", "Second visit, cabinet resealed"],
}


def spell_minutes_in(sp, y):
    """real minutes of a spell inside local calendar year y"""
    a, b = sp["a"], sp["b"]
    lo, hi = "%d-01-01 00:00" % y, "%d-01-01 00:00" % (y + 1)
    a2 = max(a, lo)
    b2 = min(b, hi)
    return max(0, elapsed_min(a2, b2)) if a2 < b2 else 0


def all_spells():
    """the spells including recurrences, each with its code"""
    out = []
    for sp in SPELLS:
        out.append(dict(code=sp["code"], a=sp["a"], b=sp["b"]))
        if sp.get("recur"):
            out.append(dict(code=sp["code"], a=sp["recur"]["a"], b=sp["recur"]["b"]))
    return out


def outages_2025_truth():
    """per dashboard counter: real minutes recording nothing in 2025 and the separate spells behind them"""
    out = {c: [0, 0] for c in W.HEADLINE}
    for sp in all_spells():
        m = spell_minutes_in(sp, 2025)
        if m > 0:
            out[sp["code"]][0] += m
            out[sp["code"]][1] += 1
    return {c: (v[0], v[1]) for c, v in out.items()}


def build_log(rng):
    """rows of the maintenance job log, as the job system exports them: job numbers run in the order jobs were
    raised (a follow-up visit is raised when its job closes, a recurrence when it is reported)"""
    rows = []
    tmp = [0]

    def jobno(y):
        tmp[0] += 1
        return "tmp%05d" % tmp[0]

    def rec(job, parent, code, logged, jtype, rep, att, clo, dt_val, note, asset_override=None, created=None):
        rows.append(dict(job_no=job, parent_job=parent or "", asset_id=asset_override or N.COUNTER_IDS[code],
                         site=N.LEGACY_NAMES[code], logged_by=("Traffic Monitoring Unit" if logged == "TMU" else N.CONTRACTOR),
                         job_type=jtype, reported=rep, attended=att, closed=clo, downtime=dt_val, notes=note,
                         _created=created or rep))

    events = []
    seg = [c for c in N.COUNTER_IDS if c not in W.HEADLINE]
    for y in (2024, 2025, 2026):
        for c in seg:
            d0 = datetime(y, 5, 28 + int(rng.integers(0, 3)), 8 + int(rng.integers(0, 6)), int(rng.integers(0, 4)) * 15)
            events.append((d0, ("install", c, y, d0)))
            d1 = datetime(y, 9, 1 + int(rng.integers(0, 4)), 8 + int(rng.integers(0, 6)), int(rng.integers(0, 4)) * 15)
            events.append((d1, ("remove", c, y, d1)))
    for c, a, b, why in SUMMER_OUTAGES:
        events.append((_dt(a), ("summer_outage", c, a, b, why)))
    for sp in SPELLS:
        events.append((_dt(sp["a"]), ("spell", sp)))
    events.append((datetime(2026, 5, 13, 16, 5), ("bf1_download",)))
    events.append((datetime(2026, 3, 17, 6, 10), ("ep1_power",)))
    events.append((datetime(2025, 3, 12, 9, 0), ("ms1_replace",)))
    events.append((datetime(2025, 1, 6, 9, 0), ("migration",)))
    events.append((datetime(2026, 5, 29, 8, 30), ("summer_round",)))
    events.sort(key=lambda e: e[0])

    for when, ev in events:
        kind = ev[0]
        y = when.year
        if kind == "install":
            _, c, yy, d0 = ev
            rec(jobno(y), None, c, "CON", "install", d0.strftime("%Y-%m-%d %H:%M"), d0.strftime("%Y-%m-%d %H:%M"),
                (d0 + timedelta(minutes=int(rng.integers(35, 95)))).strftime("%Y-%m-%d %H:%M"), "",
                ["Summer counter installed for the cycleway monitoring season", "Seasonal counter fitted, loops tested",
                 "Counter installed and logger started", "Summer unit installed; test count taken"][int(rng.integers(0, 4))])
        elif kind == "remove":
            _, c, yy, d1 = ev
            rec(jobno(y), None, c, "CON", "removal", d1.strftime("%Y-%m-%d %H:%M"), d1.strftime("%Y-%m-%d %H:%M"),
                (d1 + timedelta(minutes=int(rng.integers(25, 70)))).strftime("%Y-%m-%d %H:%M"), "",
                ["Summer counter removed, data retrieved", "Seasonal counter taken out, final download done",
                 "Unit removed for winter storage", "Counter removed; logger data retrieved"][int(rng.integers(0, 4))])
        elif kind == "summer_outage":
            _, c, a, b, why = ev
            mins = elapsed_min(a, b)
            jt = "battery" if "battery" in why else ("vandalism" if ("forced" in why or "vandal" in why) else "fault")
            rep = _dt(a) + timedelta(minutes=int(rng.integers(25, 80)))
            if rep >= _dt(b):
                rep = _dt(a) + timedelta(minutes=max(1, mins // 3))
            rec(jobno(y), None, c, "TMU", jt, a, rep.strftime("%Y-%m-%d %H:%M"), b, hmm(mins), why[0].upper() + why[1:])
        elif kind == "spell":
            sp = ev[1]
            code, jt = sp["code"], sp["jt"]
            mins = elapsed_min(sp["a"], sp["b"])
            unit = "CON" if sp["by"] == "CON" else "TMU"
            dval = ("%d" % mins) if unit == "CON" else hmm(mins)
            att = _dt(sp["a"]) + timedelta(minutes=int(rng.integers(20, 140)))
            if att >= _dt(sp["b"]):
                att = _dt(sp["a"]) + timedelta(minutes=max(1, int(mins * 0.4)))
            asset = sp.get("asset")
            if code == "MS1" and _dt(sp["a"]) < datetime(2025, 3, 21):
                asset = N.MS1_OLD_ID
            if sp.get("note"):
                note = sp["note"]
            elif sp["by"] == "TMU+CON":
                note = "No counts from site, contractor called out"
            else:
                note = NOTES[jt][int(rng.integers(0, len(NOTES[jt])))]
            j = jobno(y)
            rec(j, None, code, unit, jt, sp["a"], att.strftime("%Y-%m-%d %H:%M"), sp["b"], dval, note, asset)
            parent_for_checks, check_by, check_dval = j, unit, dval
            if sp.get("con"):
                c = sp["con"]
                cm = elapsed_min(c["a"], c["b"])
                cj = jobno(_dt(c["a"]).year)
                rec(cj, None, code, "CON", jt, c["a"], c["a"], c["b"], "%d" % cm, c["note"], asset)
                parent_for_checks, check_by, check_dval = cj, "CON", "%d" % cm
            for (dd, hh, mm, dur) in sp.get("checks", []):
                vd = _dt(sp["b"]).replace(hour=hh, minute=mm) + timedelta(days=dd)
                closed_parent = sp["con"]["b"] if sp.get("con") else sp["b"]
                rec(jobno(vd.year), parent_for_checks, code, check_by, jt, vd.strftime("%Y-%m-%d %H:%M"),
                    vd.strftime("%Y-%m-%d %H:%M"), (vd + timedelta(minutes=dur)).strftime("%Y-%m-%d %H:%M"), check_dval,
                    NOTES["visit"][int(rng.integers(0, 3))], asset, created=closed_parent)
            if sp.get("recur"):
                r = sp["recur"]
                rm = elapsed_min(r["a"], r["b"])
                ra = _dt(r["a"]) + timedelta(minutes=int(rng.integers(30, 90)))
                rec(jobno(_dt(r["a"]).year), j, code, "TMU", jt, r["a"], ra.strftime("%Y-%m-%d %H:%M"), r["b"], hmm(rm),
                    r["note"], asset)
        elif kind == "bf1_download":
            rec(jobno(2026), None, "BF1", "TMU", "download", "2026-05-13 16:05", "2026-05-13 16:05", "2026-05-13 16:50",
                "0:45", "Manual download, logger paused during transfer")
        elif kind == "ep1_power":
            rec(jobno(2026), None, "EP1", "TMU", "power", "2026-03-17 06:10", "2026-03-17 09:30", "2026-03-17 11:40",
                "5:30", "Logger lost power after quayside lighting fault, reprogrammed from laptop and restarted")
        elif kind == "ms1_replace":
            rec(jobno(2025), None, "MS1", "CON", "replacement", "2025-03-12 09:00", "2025-03-12 09:00", "2025-03-21 15:30",
                "", "New unit CVC-1207 installed beside CVC-0388; old unit removed 21/03 after side-by-side check",
                N.MS1_OLD_ID)
        elif kind == "summer_round":
            t0 = datetime(2026, 5, 29, 8, 30)
            for k, c in enumerate(sorted(W.HEADLINE, key=lambda c: N.COUNTER_IDS[c])):
                t1 = t0 + timedelta(minutes=55 * k + int(rng.integers(0, 10)))
                t2 = t1 + timedelta(minutes=int(rng.integers(25, 45)))
                note = ("Summer round check: logger clock reset, seals and loop readings checked" if c in LOCAL_CLOCK
                        else "Summer round check: logger clock, seals and loop readings checked")
                rec(jobno(2026), None, c, "TMU", "inspection", t1.strftime("%Y-%m-%d %H:%M"), t1.strftime("%Y-%m-%d %H:%M"),
                    t2.strftime("%Y-%m-%d %H:%M"), "", note)
        elif kind == "migration":
            for c in W.HEADLINE:
                asset = N.MS1_OLD_ID if c == "MS1" else None
                rec(jobno(2025), None, c, "TMU", "firmware", "2025-01-06 09:00", "2025-01-06 09:00", "2025-01-06 17:00", "",
                    "Moved to the new counter platform; logger clock set to UTC", asset)
    for r in rows:
        if r["job_type"] == "install" and r["reported"].startswith("2026"):
            r["notes"] = r["notes"] + "; clocks checked"
    order = sorted(range(len(rows)), key=lambda i: (rows[i]["_created"], rows[i]["job_no"]))
    seq = {2024: 3, 2025: 7, 2026: 4}
    rename = {}
    for i in order:
        y = int(rows[i]["_created"][:4])
        seq[y] += int(rng.integers(1, 9))
        rename[rows[i]["job_no"]] = "TM-%02d-%04d" % (y % 100, seq[y])
    out = []
    for i in order:
        r = dict(rows[i])
        r["job_no"] = rename[r["job_no"]]
        r["parent_job"] = rename[r["parent_job"]] if r["parent_job"] else ""
        del r["_created"]
        out.append(r)
    return out


# ------------------------------------------------------------------ May 2026 count week (15-minute extract)
COUNT_WEEK = [date(2026, 5, d) for d in (11, 12, 13, 14, 15)]
CW_SPAN = [date(2026, 5, 10)] + COUNT_WEEK      # the evening before too: the export's first intervals fall on it
COUNT_DAYS = {"TR1": date(2026, 5, 12), "MS1": date(2026, 5, 12), "BF1": date(2026, 5, 13), "WP1": date(2026, 5, 13),
              "EP1": date(2026, 5, 14), "SF1": date(2026, 5, 14)}
WINDOWS = [(7, 10), (16, 19)]           # local hours, volunteers' AM and PM windows
BF1_GAP = (date(2026, 5, 13), 16)       # local hour whose four quarter hours the logger did not keep (paused 16:05-16:50)


def quarter_weights(h):
    """within-hour shape of 15-minute counts by local hour (a ramp in the peaks)"""
    ramps = {6: [.17, .22, .27, .34], 7: [.19, .23, .27, .31], 8: [.30, .28, .23, .19], 9: [.31, .26, .23, .20],
             15: [.21, .23, .26, .30], 16: [.22, .24, .26, .28], 17: [.28, .26, .24, .22], 18: [.30, .26, .23, .21],
             19: [.29, .26, .24, .21]}
    return np.array(ramps.get(h, [.25, .25, .25, .25]))


def lost_fraction_days(code, days):
    """days x 24 share of each local hour a dashboard counter recorded nothing, over any span of days"""
    f = np.zeros((len(days), 24))
    pos = {d: i for i, d in enumerate(days)}
    for a, b in _spans_for(code):
        A, B = _dt(a), _dt(b)
        t = A.replace(minute=0)
        while t < B:
            t1 = t + timedelta(hours=1)
            lo, hi = max(t, A), min(t1, B)
            if hi > lo and t.date() in pos:
                f[pos[t.date()], t.hour] += (hi - lo).total_seconds() / 3600.0
            t = t1
    return np.clip(f, 0, 1)


def build_count_week(T, rng):
    """15-minute riders (true, counted, kept) by direction for the six dashboard counters, 10 to 15 May 2026, local
    quarters. Overwrites the full-year hourly counts on those days with the kept quarters' sums so every file agrees."""
    out = {}
    allyear = T["fullyear"]["TR1"][0]
    pos = {d: i for i, d in enumerate(allyear)}
    for code in W.HEADLINE:
        days, lin, lout, nin, nout, comps = T["fullyear"][code]
        cap = W.CAPTURE[code]
        tr = {}
        for d in CW_SPAN:
            i = pos[d]
            for h in range(24):
                qw = quarter_weights(h)
                for q in range(4):
                    t_in = rng.poisson(lin[i, h] / cap * qw[q])
                    t_out = rng.poisson(lout[i, h] / cap * qw[q])
                    c_in = rng.binomial(t_in, cap)
                    c_out = rng.binomial(t_out, cap)
                    kept = not (code == "BF1" and (d, h) == BF1_GAP)
                    tr[(d, h, q)] = (t_in, t_out, c_in, c_out, kept)
            nin[i] = [sum(tr[(d, h, q)][2] for q in range(4) if tr[(d, h, q)][4]) for h in range(24)]
            nout[i] = [sum(tr[(d, h, q)][3] for q in range(4) if tr[(d, h, q)][4]) for h in range(24)]
        out[code] = tr
    return out


def build_volunteers(CW, rng):
    """volunteer tallies (track by direction, road) per site per local quarter in the two windows of its count day"""
    sheets = {}
    road_share = {"TR1": 0.035, "BF1": 0.06, "EP1": 0.01, "WP1": 0.02, "MS1": 0.05, "SF1": 0.07}
    for code, d in COUNT_DAYS.items():
        rows = []
        for a, b in WINDOWS:
            for h in range(a, b):
                for q in range(4):
                    t_in, t_out, c_in, c_out, kept = CW[code][(d, h, q)]
                    v_in = max(0, int(round(t_in * (1 - abs(rng.normal(0.004, 0.006))) + rng.normal(0, 0.6))))
                    v_out = max(0, int(round(t_out * (1 - abs(rng.normal(0.004, 0.006))) + rng.normal(0, 0.6))))
                    road = int(rng.poisson((t_in + t_out) * road_share[code]))
                    rows.append((h, q, v_in, v_out, road))
        sheets[code] = rows
    return sheets


def _quarters(d):
    out = []
    for h in range(24):
        for q in range(4):
            out.append((d, h, q))
    return out


def ask_a_values(CW, sheets, shift_local=0, shift_other=0, road=False, gap_both=True):
    """per site (counter riders, volunteers' track riders, shortfall %): the counter's quarters taken `shift` quarters
    earlier than the volunteers' (0 is the golden alignment), the BF1 gap left out on both sides or on the counter's
    side only, road riders in the volunteers' count or not"""
    out = {}
    for code, d in COUNT_DAYS.items():
        allq = _quarters(d - timedelta(days=1)) + _quarters(d)
        idx = {k: i for i, k in enumerate(allq)}
        shift = shift_local if code in LOCAL_CLOCK else shift_other
        C = V = 0
        for h, q, v_in, v_out, road_n in sheets[code]:
            k = allq[idx[(d, h, q)] - shift]
            t_in, t_out, c_in, c_out, kept = CW[code][k] if k in CW[code] else (0, 0, 0, 0, False)
            if not kept and gap_both:
                continue                  # an interval the counter did not keep is left out on both sides
            if kept:
                C += c_in + c_out
            V += v_in + v_out + (road_n if road else 0)
        out[code] = (C, V, 100.0 * (V - C) / V)
    return out


def ask_a_truth(CW, sheets):
    return ask_a_values(CW, sheets)


ASK_A_ROUTES = {"stamps read as starts, laptop clocks missed": dict(shift_local=5, shift_other=1),
                "stamps read as ends, laptop clocks missed": dict(shift_local=4, shift_other=0),
                "laptop clocks found, stamps read as starts": dict(shift_local=1, shift_other=1),
                "road riders in the volunteers' count": dict(road=True),
                "the Station Sq gap left in the volunteers' count": dict(gap_both=False)}


def edge(v, unit=0.1):
    """distance from v to the nearest edge of its printed cell at the given unit"""
    return unit / 2 - abs(v - round(v / unit) * unit)


def volunteers_ok(CW, sheets):
    g = ask_a_values(CW, sheets)
    for code, (C, V, sh) in g.items():
        if edge(sh) < 0.02:
            return False
    for name, kw in ASK_A_ROUTES.items():
        alt = ask_a_values(CW, sheets, **kw)
        for code in g:
            if code == "BF1" or name not in ("the Station Sq gap left in the volunteers' count",):
                pass
            if alt[code] == g[code]:
                continue          # this route does not touch the site
            if alt[code][0] != g[code][0] and abs(alt[code][0] - g[code][0]) < 1:
                return False
            if round(alt[code][2], 1) == round(g[code][2], 1) and alt[code][0] != g[code][0]:
                return False
    return True


# ------------------------------------------------------------------ the public dashboard's monthly series
def build_dashboard(T, rng):
    """monthly totals both directions for the six dashboard sites, January 2019 to September 2026, as published.
    2024 onward from the counts (estimates filled where a day was not recorded); 2019 to 2023 the legacy series."""
    rows = []
    for k, code in enumerate(W.HEADLINE):
        days, lin, lout, nin, nout, comps = T["fullyear"][code]
        lam = (lin + lout)
        f = lost_fraction_days(code, days)
        tot = (nin + nout).astype(float) * (1 - f) + lam * f       # hours not recorded carry the platform estimate
        bym = {}
        for i, d in enumerate(days):
            bym.setdefault((d.year, d.month), [0.0, 0])
            bym[(d.year, d.month)][0] += tot[i].sum()
        # the Corn Exchange: both units counted 12 to 20 March 2025 on the dashboard
        if code == "MS1":
            for i, d in enumerate(days):
                if date(2025, 3, 12) <= d <= date(2025, 3, 20):
                    bym[(2025, 3)][0] += tot[i].sum() * 0.97
        # legacy years: back from 2024 by the groups' trends with the pandemic years
        base24 = {m: bym[(2024, m)][0] for m in range(1, 13)}
        mix = np.array(T["base"][code]) / np.sum(T["base"][code])
        for y in range(2019, 2024):
            for m in range(1, 13):
                f = 0.0
                for pi, p in enumerate(W.PURP):
                    g = W.TREND[p] ** (y - 2024)
                    if p == "commute" and y in (2020, 2021):
                        g *= (0.62 if y == 2020 else 0.78)
                    if p == "commute" and y in (2022, 2023):
                        g *= (0.86 if y == 2022 else 0.93)
                    if p == "leisure" and y in (2020, 2021):
                        g *= (1.38 if y == 2020 else 1.22)
                    f += mix[pi] * g
                v = base24[m] * f * math.exp(rng.normal(0, 0.035))
                if y == 2020 and m == 4:
                    v *= 0.55
                rows.append(dict(site=code, year=y, month=m, total=int(round(v, -1)), source="legacy"))
        for (y, m), (v, _) in sorted(bym.items()):
            rows.append(dict(site=code, year=y, month=m, total=int(round(v)), source=("legacy" if y == 2024 else "platform")))
    return rows


# ------------------------------------------------------------------ background files (not used by the forecast)
EVENTS = [
    ("2024-06-15", "Calvermouth Half Marathon", "Quayside and Estuary Path", 9000),
    ("2024-07-06", "Harbour Festival (day 1)", "Quayside", 22000), ("2024-07-07", "Harbour Festival (day 2)", "Quayside", 18000),
    ("2024-07-20", "Wardle Park Proms", "Wardle Park", 6500), ("2024-08-10", "Food and Makers Market", "Corn Exchange", 4000),
    ("2024-08-24", "Calvermouth Pride", "Market Street", 12000),
    ("2025-06-14", "Calvermouth Half Marathon", "Quayside and Estuary Path", 9500),
    ("2025-07-05", "Harbour Festival (day 1)", "Quayside", 24000), ("2025-07-06", "Harbour Festival (day 2)", "Quayside", 19500),
    ("2025-07-19", "Wardle Park Proms", "Wardle Park", 7000), ("2025-08-09", "Food and Makers Market", "Corn Exchange", 4200),
    ("2025-08-23", "Calvermouth Pride", "Market Street", 13500), ("2025-06-28", "Cathedral Green Open Air Cinema", "Cathedral Green", 1800),
    ("2026-06-13", "Calvermouth Half Marathon", "Quayside and Estuary Path", 10000),
    ("2026-07-04", "Harbour Festival (day 1)", "Quayside", 26000), ("2026-07-05", "Harbour Festival (day 2)", "Quayside", 21000),
    ("2026-07-18", "Wardle Park Proms", "Wardle Park", 7500), ("2026-08-08", "Food and Makers Market", "Corn Exchange", 4500),
    ("2026-08-22", "Calvermouth Pride", "Market Street", 14000), ("2026-06-27", "Cathedral Green Open Air Cinema", "Cathedral Green", 2100),
    ("2026-09-12", "Heritage Open Days", "City centre", 15000), ("2025-09-13", "Heritage Open Days", "City centre", 14000),
]


def build_app_rides(T, rng):
    """monthly rides recorded by a fitness app's users across each cycleway's counted segments (a neighbouring measure)"""
    rows = []
    share = {"CW1": 0.021, "CW2": 0.012, "CW3": 0.068, "CW4": 0.046, "CW5": 0.016, "CW6": 0.034}
    for cw, cwname, segs in W.CYCLEWAYS:
        head = segs[0][0]
        days, lin, lout, nin, nout, comps = T["fullyear"][head]
        leis = comps[1]
        bym = {}
        for i, d in enumerate(days):
            if d < date(2024, 1, 1):
                continue
            bym.setdefault((d.year, d.month), 0.0)
            bym[(d.year, d.month)] += (lin[i] + lout[i]).sum() * 0.3 + leis[i].sum() * 0.7
        for (y, m), v in sorted(bym.items()):
            rows.append(dict(month="%04d-%02d" % (y, m), cycleway=cwname, rides=int(round(v * share[cw] * math.exp(rng.normal(0, 0.06)))),
                             athletes=int(round(v * share[cw] * 0.31 * math.exp(rng.normal(0, 0.05))))))
    return rows
