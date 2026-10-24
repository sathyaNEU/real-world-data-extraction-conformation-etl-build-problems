"""Professional learning: the 2025-26 catalog and the scheduling system's session export, built from each district's
true delivered sessions. Every offering is scheduled in whole hours. Two things decide a session's hours and neither
is labelled: a series session's hours field carries the series' credit hours (the offering's total, on each of its
sessions), and a single session's field carries the time it actually ran the way the scheduling system takes it, hours
and minutes after the point (1.40 is an hour and forty minutes), so only the sessions that ran short or long carry
minutes."""
import datetime as dt

import numpy as np

import world as W

# code, title, delivery, sessions, planned hours per session
CATALOG = [
    ("LL-101", "Launch: Getting Started with Lumenfold", "Virtual live", 1, 2),
    ("LL-112", "Virtual Lab Routines", "Virtual live", 1, 1),
    ("LL-120", "Unit Planning Day", "On site", 1, 6),
    ("LL-131", "Science Notebooks in Practice", "On site", 1, 3),
    ("LL-144", "Reading the Class Dashboard", "Virtual live", 1, 1),
    ("LL-150", "Phenomenon of the Month", "Virtual live", 1, 1),
    ("LL-210", "Inquiry Labs Series", "Virtual live", 3, 1),
    ("LL-224", "Coaching Cycle: Discourse in Science", "On site", 2, 2),
    ("LL-233", "Assessment for Learning Series", "Virtual live", 2, 2),
    ("LL-301", "Summer Science Institute, Day 1", "On site", 1, 6),
    ("LL-302", "Summer Science Institute, Day 2", "On site", 1, 6),
    ("LL-401", "Recorded Webinar: Phenomena-Based Teaching", "Recorded webinar", 1, 1),
    ("LL-415", "On-Demand Course: Differentiation in Science", "On-demand course", 1, 4),
]
OFFER = {c[0]: c for c in CATALOG}
LIVE = ("Virtual live", "On site")
INSTITUTE = {2025: (dt.date(2025, 7, 15), dt.date(2025, 7, 16)), 2026: (dt.date(2026, 7, 14), dt.date(2026, 7, 15))}
SHORT = {60: (5, 10), 120: (20, 25)}   # minutes short by planned length; three hours and more below
SHORT_LONG = (30, 35, 40, 45)
LONG = (5, 10, 15)


def total_hours(code):
    o = OFFER[code]
    return o[3] * o[4]


def hmm(minutes):
    """A duration as the scheduling system writes it: hours and minutes after the point."""
    return "%d.%02d" % divmod(int(minutes), 60)


def read_hmm(s):
    h, m = s.split(".")
    return int(h) + int(m) / 60.0


def half_hours(hours):
    """Hours to the nearest half hour (the generator keeps every district's total off a quarter hour)."""
    return float(np.floor(hours * 2 + 0.5) / 2)


def _school_day(r, a, b):
    while True:
        d = a + dt.timedelta(days=int(r.integers(0, (b - a).days + 1)))
        if d.weekday() < 5:
            return d


def counts(x, dd):
    """A row counts toward the district's hours: a live session delivered inside its subscription term."""
    return x["status"] == "Delivered" and x["delivery"] in LIVE and dd["term_start"] <= x["session_date"] <= dd["term_end"]


def build():
    """Session rows (one per district per session, joint sessions sharing a session id) and each district's true
    live minutes delivered in its subscription term."""
    r = np.random.default_rng(W.SEED + 21)
    rows = []
    sess_no = [5100]
    book_no = [880000]

    def new_session():
        sess_no[0] += int(r.integers(1, 9))
        return "PLS-%d" % sess_no[0]

    def ran(code):
        """Minutes a delivered live session actually ran: most to time, some short, a few long."""
        planned = OFFER[code][4] * 60
        u = r.random()
        if u < 0.50:
            return planned - int(r.choice(SHORT.get(planned, SHORT_LONG)))
        if u < 0.55:
            return planned + int(r.choice(LONG))
        return planned

    def book(dd, code, day, status, sid=None, start="15:30", fac=None, teachers=None, minutes=None):
        book_no[0] += int(r.integers(1, 40))
        o = OFFER[code]
        series = o[3] > 1
        if minutes is None:
            minutes = ran(code) if status == "Delivered" and o[2] in LIVE and not series else o[4] * 60
        # a series session's hours field holds the series' credit hours, the offering's total, and its time is not
        # logged (series sessions run to their schedule); a single session's field holds the time it ran
        shown = o[3] * o[4] * 60 if series else minutes
        rows.append(dict(booking_id="BK%d" % book_no[0], session_id=sid or new_session(), offering_code=code,
                         offering_title=o[1], partner_id=dd["partner_id"], account_name=dd["crm_name"],
                         session_date=day, start_time=start, delivery=o[2], status=status, minutes=int(minutes),
                         hours=hmm(shown), facilitator=fac or "PLF-%02d" % int(r.integers(1, 23)),
                         teachers=teachers if teachers is not None else int(r.integers(4, 31))))
        return rows[-1]

    institute_minutes = {}
    for dd in W.DISTRICTS:
        planned = 0
        H = dd["pd_hours"]
        short = r.random() < 0.55
        target = max(3, H - int(r.choice([1, 2, 3, 4]))) if short else H + int(r.choice([0, 0, 0, 1, 2, 3]))
        in_term = lambda day: dd["term_start"] <= day <= dd["term_end"]
        # every district launches in August or September
        day = _school_day(r, dt.date(2025, 8, 18), dt.date(2025, 9, 26))
        book(dd, "LL-101", day, "Delivered", start=r.choice(["15:30", "16:00", "13:00"]))
        planned += 2
        # the summer institute: the July 2025 cohort or the July 2026 cohort, for some districts
        if H >= 12 and r.random() < 0.55:
            year = 2025 if r.random() < 0.5 else 2026
            for code, day in zip(("LL-301", "LL-302"), INSTITUTE[year]):
                key = (year, dd["state"], code)
                if key not in institute_minutes:                 # one institute day, one length, for every district
                    institute_minutes[key] = ran(code)
                book(dd, code, day, "Delivered", sid="PLS-SSI%d-%s-%s" % (key[0], key[1], key[2][-1]), start="08:30",
                     minutes=institute_minutes[key])
            if in_term(INSTITUTE[year][0]):
                planned += 12
        # a series for almost every district (two for the larger contracts), then single sessions up to the plan
        order = [("LL-210", "LL-224", "LL-233")[i] for i in r.permutation(3)]
        plan = [order[0]] if r.random() < 0.93 else []
        if plan and H >= 18 and r.random() < 0.5:
            plan.append(order[1])
        target = max(target, planned + sum(total_hours(c) for c in plan))
        guard = 0
        while planned + sum(total_hours(c) for c in plan) < target and guard < 40:
            guard += 1
            need = target - planned - sum(total_hours(c) for c in plan)
            singles = [c for c in ("LL-112", "LL-120", "LL-131", "LL-144", "LL-150") if total_hours(c) <= need]
            if not singles:
                break
            plan.append(singles[int(r.integers(len(singles)))])
        for code in plan:
            o = OFFER[code]
            first = _school_day(r, dt.date(2025, 9, 15), dt.date(2026, 3, 20))
            gap = 21 if o[2] == "Virtual live" else 28
            start = "15:30" if o[2] == "Virtual live" else "08:30" if o[4] >= 6 else "12:30"
            for k in range(o[3]):
                day = first + dt.timedelta(days=gap * k)
                while day.weekday() >= 5:
                    day += dt.timedelta(days=1)
                book(dd, code, day, "Delivered", start=start)
            planned += o[3] * o[4]
    # joint regional sessions: a virtual single session shared by two to four districts of a state
    by_state = {}
    for dd in W.DISTRICTS:
        by_state.setdefault(dd["state"], []).append(dd)
    for st, dds in by_state.items():
        for _ in range(3):
            k = int(r.integers(2, 5))
            who = [dds[i] for i in r.choice(len(dds), k, replace=False)]
            code = ("LL-144", "LL-150", "LL-112")[int(r.integers(3))]
            day = _school_day(r, dt.date(2025, 10, 1), dt.date(2026, 5, 15))
            sid = new_session()
            fac = "PLF-%02d" % int(r.integers(1, 23))
            m = ran(code)
            for dd in who:
                book(dd, code, day, "Delivered", sid=sid, start="16:00", fac=fac, minutes=m)
    # cancellations, reschedules, make-ups in July 2026, recorded and on-demand
    for dd in W.DISTRICTS:
        u = r.random()
        if u < 0.25:
            code = ("LL-131", "LL-112", "LL-144")[int(r.integers(3))]
            book(dd, code, _school_day(r, dt.date(2025, 11, 3), dt.date(2026, 4, 24)), "Cancelled", teachers=0)
        elif u < 0.45:
            code = ("LL-131", "LL-150", "LL-120")[int(r.integers(3))]
            day = _school_day(r, dt.date(2025, 10, 6), dt.date(2026, 3, 13))
            book(dd, code, day, "Rescheduled", teachers=0)
            later = _school_day(r, day + dt.timedelta(days=14), day + dt.timedelta(days=60))
            book(dd, code, later, "Delivered", start="12:30" if OFFER[code][2] == "On site" else "15:30")
        if r.random() < 0.2:
            day = _school_day(r, dt.date(2026, 7, 6), dt.date(2026, 7, 24))
            code = ("LL-112", "LL-144", "LL-150")[int(r.integers(3))]
            book(dd, code, day, "Delivered", start="10:00")
        if r.random() < 0.6:
            code = ("LL-401", "LL-415")[int(r.integers(2))]
            book(dd, code, _school_day(r, dt.date(2025, 9, 1), dt.date(2026, 5, 29)), "Delivered", start="",
                 fac="", teachers=int(r.integers(3, 40)))
    # keep every district's total off a quarter hour, so rounding to the half hour has no ties: shorten one of its
    # own (not joint) sessions that already ran off time by five minutes, or else one that ran to time
    shared = {}
    for x in rows:
        shared.setdefault(x["session_id"], set()).add(x["partner_id"])
    for dd in W.DISTRICTS:
        for _ in range(12):
            mine = [x for x in rows if x["partner_id"] == dd["partner_id"] and counts(x, dd)]
            if sum(x["minutes"] for x in mine) % 30 != 15:
                break
            own = [x for x in mine if len(shared[x["session_id"]]) == 1 and OFFER[x["offering_code"]][3] == 1]
            off = [x for x in own if x["minutes"] != OFFER[x["offering_code"]][4] * 60]
            x = (off or own)[0]
            x["minutes"] -= 5
            x["hours"] = hmm(x["minutes"])
    truth = {dd["partner_id"]: sum(x["minutes"] for x in rows if x["partner_id"] == dd["partner_id"] and counts(x, dd))
             for dd in W.DISTRICTS}
    rows.sort(key=lambda x: (x["session_date"], x["start_time"], x["session_id"], x["partner_id"]))
    return rows, truth


def crm_names():
    """The CRM's account names, which shorten the districts' legal names."""
    short = {"County Schools": "County Schools", "City Schools": "City Schools", "Local School District": "Local SD",
             "City School District": "City SD", "Exempted Village School District": "EVSD",
             "County School District": "County SD", "Special School District": "SSD",
             "Unified School District": "USD", "Elementary School District": "ESD"}
    for dd in W.DISTRICTS:
        nm = dd["name"]
        for k, v in short.items():
            if nm.endswith(k):
                nm = nm[: -len(k)] + v
                break
        dd["crm_name"] = nm.replace("School District RE-", "SD RE-").replace("School District ", "SD ")
