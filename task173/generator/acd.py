"""The contact centre's ACD and the outsourcer's paperwork for 2026: the ACD's user list, the agent-state detail of
the outsourcer's team, the English queue's contact detail for the deadline fortnight, the outsourcer's own onboarding
list, its time-and-attendance records and the weekly invoices built from them.

How the ACD records an agent. An agent signs in to a session and is in one state at a time: Available, On Contact,
After-Contact Work, or Not Ready with a reason. When a softphone freezes the ACD cannot hear from it, so the session
it held stays in its last state until the ACD's 90-minute session timeout ends it, while the agent restarts the
softphone and signs in again on a new session. When an agent's sign-in is locked, the service desk issues a new login
under its own naming convention and the agent works on that login from then on; the outsourcer's onboarding list keeps
the login it first issued.

How the ACD records a customer. Each time the queue offers a waiting customer to an expert it writes a row. An offer
the expert does not take is re-offered under the same contact, and the queue writes the re-offer with the time the
customer was put back in the queue. A video session that fails to connect after the expert accepts is queued again as
a new contact on the same session. The ACD's answer time is when the expert accepts; the conversation begins when the
media connects, which the CRM records as the interaction's start."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K
import world as W

F_USERS = "acd_users_2026-10-29.csv"
F_STATES = "acd_agent_state_detail_hcs_2026.csv"
F_CONTACTS = "acd_contact_detail_en_2026_deadline.csv"
F_ONBOARD = "hcs_agent_onboarding_2026.xlsx"

BILLABLE = ("Available", "On Contact", "After-Contact Work")
TIMEOUT_H = 1.5
DOMAIN_CLIENT = "ashdale.ca"
DOMAIN_VENDOR = "hillsboroughcs.ca"

FIRST = ["Aaron", "Abigail", "Adrian", "Aiden", "Alexa", "Alicia", "Allison", "Amanda", "Amelia", "Andre", "Angela",
         "Anna", "Annie", "Ashley", "Austin", "Ava", "Bailey", "Benjamin", "Bethany", "Blake", "Brandon", "Brenda",
         "Brett", "Brianna", "Brooke", "Caleb", "Cameron", "Carla", "Carmen", "Carter", "Cassandra", "Chantal",
         "Charlotte", "Chloe", "Christine", "Claire", "Colin", "Connor", "Courtney", "Crystal", "Curtis", "Dana",
         "Danielle", "Darren", "Dawn", "Denise", "Derek", "Diane", "Dominic", "Donna", "Dustin", "Dylan", "Elise",
         "Ella", "Emily", "Emma", "Eric", "Erica", "Ethan", "Evan", "Faith", "Felix", "Fiona", "Gabriel", "Gail",
         "Gavin", "Gina", "Grace", "Hailey", "Hannah", "Heather", "Holly", "Hunter", "Ian", "Isaac", "Isabelle",
         "Jacob", "Jade", "Janelle", "Jared", "Jasmine", "Jenna", "Jesse", "Joanne", "Joel", "Jordan", "Josee",
         "Julie", "Justin", "Kara", "Karen", "Katie", "Kayla", "Keith", "Kendra", "Kevin", "Kristen", "Kyle",
         "Laura", "Lauren", "Leah", "Liam", "Lindsay", "Logan", "Lucas", "Luke", "Mackenzie", "Madison", "Marc",
         "Marie", "Megan", "Melanie", "Melissa", "Mia", "Micheline", "Mitchell", "Monique", "Morgan", "Natalie",
         "Nathan", "Nicole", "Noah", "Olivia", "Owen", "Paige", "Patricia", "Pierre", "Rachel", "Rebecca", "Renee",
         "Riley", "Robin", "Ryan", "Samantha", "Sara", "Scott", "Shannon", "Shawn", "Sophie", "Spencer", "Stacey",
         "Stephanie", "Sylvie", "Tanya", "Taylor", "Tessa", "Travis", "Trevor", "Tristan", "Valerie", "Vanessa",
         "Victoria", "Wendy", "Wyatt", "Yvette", "Zachary", "Zoe"]
LAST = ["Abbott", "Allen", "Anderson", "Armstrong", "Bailey", "Baker", "Barnes", "Bell", "Bennett", "Bergeron",
        "Bishop", "Black", "Boyd", "Bradley", "Brooks", "Burke", "Burns", "Butler", "Cameron", "Carr", "Carter",
        "Chapman", "Clark", "Clarke", "Cole", "Coleman", "Cook", "Cooper", "Cox", "Crawford", "Cunningham", "Davidson",
        "Dawson", "Dixon", "Douglas", "Duncan", "Dunn", "Edwards", "Elliott", "Ellis", "Evans", "Ferguson", "Fisher",
        "Fleming", "Fletcher", "Ford", "Foster", "Fraser", "Gagnon", "Gibbs", "Gill", "Gordon", "Graham", "Grant",
        "Gray", "Green", "Hall", "Hamilton", "Hardy", "Harper", "Harrison", "Hart", "Harvey", "Hayes", "Henderson",
        "Henry", "Hill", "Holmes", "Hudson", "Hunt", "Hunter", "Jackson", "James", "Jenkins", "Jensen", "Johnston",
        "Jones", "Kelly", "Kennedy", "Kerr", "King", "Knight", "Lambert", "Lane", "Lawson", "Lee", "Lewis", "Lloyd",
        "Long", "Lynch", "MacKay", "MacKenzie", "MacLeod", "Marshall", "Mason", "Matthews", "McCarthy", "McDonald",
        "McKay", "McLean", "Miller", "Mills", "Mitchell", "Moore", "Morgan", "Morin", "Morris", "Morrison", "Murray",
        "Nelson", "Nicholson", "Noble", "Olson", "Owens", "Palmer", "Parker", "Patterson", "Payne", "Pearson",
        "Perry", "Peters", "Phillips", "Porter", "Powell", "Price", "Quinn", "Reid", "Reynolds", "Roberts",
        "Robertson", "Robinson", "Rogers", "Ross", "Russell", "Scott", "Shaw", "Simpson", "Sinclair", "Spencer",
        "Stewart", "Stone", "Sutherland", "Turner", "Wallace", "Walsh", "Ward", "Watson", "Webb", "Wells", "West",
        "Wheeler", "Williams", "Wood", "Wright", "Young"]
LAST_NB = ["Allain", "Arsenault", "Babineau", "Belliveau", "Boudreau", "Bourgeois", "Bourque", "Comeau", "Cormier",
           "Daigle", "Doiron", "Doucet", "Gallant", "Gaudet", "Goguen", "Hebert", "Landry", "LeBlanc", "Leger",
           "Maillet", "Melanson", "Poirier", "Richard", "Robichaud", "Savoie", "Thibodeau", "Vautour", "Bastarache",
           "Collette", "Cyr", "Duguay", "Fougere", "Gauvin", "Haché", "Losier", "Mazerolle", "Ouellette", "Pellerin",
           "Roy", "Surette", "Brideau", "Chiasson", "Despres", "Godin", "Leclerc", "MacLean", "Steeves", "Wilbur",
           "Colpitts", "Trites", "Wortman", "Geldart", "Jonah", "Keith", "Ryan", "Murphy", "Collins", "Kelly",
           "McGraw", "Taylor", "Smith", "Brown", "Wilson", "Thompson", "Martin", "White", "Campbell", "MacDonald"]


def _ascii(s):
    return s.replace("é", "e").replace("è", "e").replace("É", "E")


def draw_names(key, n, lasts, avoid):
    """n distinct full names, none sharing a first name or surname with the build's personas."""
    R = K.rng("names", key)
    bad_first = {p.split()[0] for p in K.PEOPLE.values()}
    bad_last = {p.split()[-1] for p in K.PEOPLE.values()}
    out, seen = [], set(avoid)
    while len(out) < n:
        f = FIRST[int(R.integers(0, len(FIRST)))]
        last = lasts[int(R.integers(0, len(lasts)))]
        if f in bad_first or last in bad_last or (f, last) in seen:
            continue
        seen.add((f, last))
        out.append((f, last))
    return out


# ------------------------------------------------------------------------------------------------- logins and people
class Directory:
    """Every ACD login: in-house experts, the outsourcer's agents and team leads, the logins the service desk issued
    after a lockout."""

    def __init__(self, staff, vend_events):
        self.staff = staff
        en_fr = [i for i, e in enumerate(staff) if e.kind == "expert"]
        vend = [i for i, e in enumerate(staff) if e.kind == "vendor"]
        self.vend = vend
        nm_in = draw_names("inhouse", len(en_fr), LAST + LAST_NB[:20], set())
        nm_v = draw_names("hcs", len(vend) + 3, LAST_NB, set(nm_in))
        self.name = {}
        for i, nm in zip(en_fr, nm_in):
            self.name[i] = nm
        for i, nm in zip(vend, nm_v):
            self.name[i] = nm
        self.leads = [("HCS-TL%d" % (k + 1), nm_v[len(vend) + k]) for k in range(3)]
        self.login0 = {}
        for i, e in enumerate(staff):
            self.login0[i] = ("hcs" + e.emp.split("-")[1]) if e.kind == "vendor" else e.emp.lower()
        # the service desk's own convention for an external user: ext- and the person's initial and surname
        self.relogin = {}           # staff index -> (day ordinal, hour the new login was created, new login)
        used = set(self.login0.values())
        for kind, day, xi, at, hours in vend_events:
            if kind != "lock":
                continue
            f, last = self.name[xi]
            base = "ext-" + (f[0] + _ascii(last)).lower().replace(" ", "")
            lg, k = base, 2
            while lg in used:
                lg, k = base + str(k), k + 1
            used.add(lg)
            created = at + hours - float(K.rng("provision", xi).uniform(2.0, 6.0)) / 60
            self.relogin[xi] = (day, created, lg)
        self.lead_login = {code: "hcstl%02d" % (k + 1) for k, (code, _) in enumerate(self.leads)}

    def login_at(self, xi, day, hour):
        r = self.relogin.get(xi)
        if r and (day, hour) >= (r[0], r[1]):
            return r[2]
        return self.login0[xi]

    def email(self, xi):
        f, last = self.name[xi]
        dom = DOMAIN_VENDOR if self.staff[xi].kind == "vendor" else DOMAIN_CLIENT
        return ("%s.%s@%s" % (_ascii(f), _ascii(last).replace(" ", ""), dom)).lower()

    def display(self, xi):
        return "%s %s" % self.name[xi]


# ------------------------------------------------------------------------------------------------- agent timelines
def _segments(acts, s_login, s_logout):
    """Fill a session from login to logout with the busy activities and Available between them."""
    out = []
    t = s_login
    for a0, a1, state, reason in acts:
        if a1 <= s_login or a0 >= s_logout:
            continue
        a0, a1 = max(a0, s_login), min(a1, s_logout)
        if a0 > t + 1e-9:
            out.append((t, a0, "Available", ""))
        out.append((a0, a1, state, reason))
        t = a1
    if s_logout > t + 1e-9:
        out.append((t, s_logout, "Available", ""))
    return out


def _merge(segs):
    """Join neighbouring segments in the same state and reason (the ACD writes a row per state change)."""
    out = []
    for s in segs:
        if out and out[-1][2] == s[2] and out[-1][3] == s[3] and abs(out[-1][1] - s[0]) < 1e-9:
            out[-1] = (out[-1][0], s[1], s[2], s[3])
        else:
            out.append(s)
    return out


def vendor_timelines(recs, atts, shifts, brks, staff, vend_events, D):
    """Every session of every outsourcer agent, as a list of (day, staff index, login, session key, segments,
    end reason), plus the time-and-attendance clock per shift. Hours are Eastern clock hours on the day."""
    vend = set(D.vend)
    f0, f1 = K.fortnight(K.SEASON_CRM)
    by = {}
    m = np.isin(recs["expert"], list(vend))
    for r in recs[m]:
        by.setdefault((int(r["day"]), int(r["expert"])), []).append(
            ("c", float(r["start"]), float(r["start"]) + float(r["talk"]) / 3600, float(r["end"])))
    for a in atts[np.isin(atts["expert"], list(vend))]:
        if a["result"] == 1:
            by.setdefault((int(a["day"]), int(a["expert"])), []).append(("rona", float(a["offered"]), float(a["ended"]), 0))
        elif a["result"] == 2:
            by.setdefault((int(a["day"]), int(a["expert"])), []).append(("vfail", float(a["offered"]), float(a["lost"]), 0))
    brk = {}
    for b in brks[np.isin(brks["expert"], list(vend))]:
        brk.setdefault((int(b["day"]), int(b["expert"])), []).append((float(b["start"]), float(b["end"]),
                                                                       "Meal" if b["kind"] == 1 else "Break"))
    locks = {(day, xi): (at, h) for kind, day, xi, at, h in vend_events if kind == "lock"}
    crashes = {}
    for kind, day, xi, at, h in vend_events:
        if kind == "crash":
            crashes.setdefault((day, xi), []).append((at, h))
    sessions, clocks = [], []
    for sh in shifts[np.isin(shifts["expert"], list(vend))]:
        day, xi, s0, s1 = int(sh["day"]), int(sh["expert"]), float(sh["start"]), float(sh["end"])
        R = K.rng("timeline", xi, day)
        acts = []
        for kind, a0, a1, a2 in by.get((day, xi), []):
            if kind == "c":
                acts.append((a0, a1, "On Contact", ""))
                acts.append((a1, a2, "After-Contact Work", ""))
            elif kind == "rona":
                acts.append((a1, a0 + 75 / 3600, "Not Ready", "No Answer"))
            else:
                acts.append((a0, a0 + a1, "On Contact", ""))
        for b0, b1, kind in brk.get((day, xi), []):
            acts.append((b0, b1, "Not Ready", kind))
        acts.sort()
        lock = locks.get((day, xi))
        start = s0 + (lock[1] if lock else 0.0)
        last_busy = max([a[1] for a in acts] + [s1])
        end = last_busy + float(R.uniform(5, 40)) / 3600
        # sessions: split at each crash; the frozen session keeps its last state until the timeout
        cuts = sorted(crashes.get((day, xi), []))
        bounds = []
        t = start - float(R.uniform(20, 90)) / 3600
        for at, gap in cuts:
            bounds.append((t, at, "crash"))
            t = at + gap - float(R.uniform(15, 45)) / 3600
        bounds.append((t, end, "end"))
        forgot = R.random() < 0.10
        for k, (b0, b1, why) in enumerate(bounds):
            login_t = b0
            ready_t = start if k == 0 else cuts[k - 1][0] + cuts[k - 1][1]
            segs = [(login_t, ready_t, "Not Ready", "Login")] + _segments(acts, ready_t, b1)
            segs = _merge(segs)
            # the ACD times a session out 90 minutes after the last heartbeat it heard (heartbeats every 30 seconds),
            # unless a team lead sees the stale session on the floor monitor first and forces it out
            tail = TIMEOUT_H + float(R.uniform(0, 30)) / 3600
            forced = R.random() < (0.45 if why == "crash" else 0.30)
            if forced:
                tail = float(R.uniform(10, 75) if why == "crash" else R.uniform(12, 60)) / 60
            if why == "crash":
                # the frozen session: the agent had just gone ready, and the ACD keeps it Available to the end
                segs = _merge(segs + [(b1, b1 + tail, "Available", "")])
                reason = "Forced" if forced else "Session timeout"
            elif forgot:
                segs.append((b1, b1 + tail, "Not Ready", "End of Shift"))
                reason = "Forced" if forced else "Session timeout"
            else:
                reason = "Agent logout"
            # an occasional Not Ready for personal time inside a long idle stretch of a live session
            if why == "end":
                out = []
                ghosts = [(at, at + TIMEOUT_H + 0.05) for at, _g in cuts]
                for s in segs:
                    clear = all(s[1] <= g0 or s[0] >= g1 for g0, g1 in ghosts)
                    if s[2] == "Available" and s[1] - s[0] > 0.2 and clear and R.random() < 0.18:
                        p0 = s[0] + float(R.uniform(1, 3)) / 60
                        p1 = min(p0 + float(R.uniform(2, 9)) / 60, s[1] - 0.5 / 60)
                        out += [(s[0], p0, "Available", ""), (p0, p1, "Not Ready", "Personal"), (p1, s[1], "Available", "")]
                    else:
                        out.append(s)
                segs = out
            login = D.login_at(xi, day, login_t + 1e-6)
            sessions.append(dict(day=day, xi=xi, login=login, segs=segs, reason=reason, crash=(why == "crash")))
        # the outsourcer's time clock, in Atlantic time at the Moncton site
        cin = s0 - float(R.uniform(4, 12)) / 60
        cout = last_busy + float(R.uniform(1, 6)) / 60
        sched_breaks = sum(0.5 if kind == "Meal" else 0.25 for _, _, kind in brk.get((day, xi), []))
        clocks.append(dict(day=day, xi=xi, cin=cin, cout=cout, sched=s1 - s0, breaks=sched_breaks))
    return sessions, clocks


def lead_sessions(D):
    """The outsourcer's three team leads sign in to watch the queue; they take no contacts."""
    out = []
    f0, f1 = K.fortnight(K.SEASON_CRM)
    v0 = f0 - dt.timedelta(7)
    for k, (code, nm) in enumerate(D.leads):
        R = K.rng("lead", k)
        d = v0
        while d <= f1:
            if (d.weekday() + k) % 7 not in (5, 6):
                s0 = 11.0 + 2.5 * k + float(R.uniform(-0.25, 0.25))
                s1 = s0 + 9.0
                if d.weekday() == 6:
                    s1 = min(s1, 23.0)
                meal = s0 + 4.5 + float(R.uniform(-0.3, 0.3))
                segs = [(s0, meal, "Not Ready", "Team Lead"), (meal, meal + 0.5, "Not Ready", "Meal"),
                        (meal + 0.5, s1, "Not Ready", "Team Lead")]
                out.append(dict(day=d.toordinal(), xi=None, login=D.lead_login[code], segs=segs, reason="Agent logout",
                                crash=False))
            d += dt.timedelta(1)
    return out


def _utc(day, hour):
    return K.to_utc(dt.datetime.combine(dt.date.fromordinal(day), dt.time(0)) + dt.timedelta(seconds=round(hour * 3600)), -5)


STATE_COLS = ["Agent Login", "Agent Name", "Session ID", "State", "Reason Code", "Start (UTC)", "End (UTC)",
              "Duration (s)"]


def state_rows(sessions, D):
    """The ACD's agent-state detail for the logins in the outsourcer's team, one row per state."""
    order = sorted(range(len(sessions)), key=lambda k: (sessions[k]["day"], sessions[k]["segs"][0][0], sessions[k]["login"]))
    sid = 30418800
    R = K.rng("session_ids")
    rows = []
    lead_names = {D.lead_login[c]: "%s %s" % nm for c, nm in D.leads}
    for k in order:
        s = sessions[k]
        sid += 1 + int(R.integers(0, 40))
        s["sid"] = sid
        name = D.display(s["xi"]) if s["xi"] is not None else lead_names[s["login"]]
        for a0, a1, state, reason in s["segs"]:
            u0, u1 = _utc(s["day"], a0), _utc(s["day"], a1)
            secs = int(round((u1 - u0).total_seconds()))
            if secs <= 0:
                continue
            # the report runs day by day on Eastern dates: a state open at midnight is reported on each day it
            # touches, each row covering that day's part and carrying the state's length
            if a0 < 24.0 < a1:
                um = _utc(s["day"], 24.0)
                rows.append([s["login"], name, str(sid), state, reason, K.iso_z(u0), K.iso_z(um), secs])
                rows.append([s["login"], name, str(sid), state, reason, K.iso_z(um), K.iso_z(u1), secs])
            else:
                rows.append([s["login"], name, str(sid), state, reason, K.iso_z(u0), K.iso_z(u1), secs])
        u_end = _utc(s["day"], s["segs"][-1][1])
        rows.append([s["login"], name, str(sid), "Logged Out", s["reason"], K.iso_z(u_end), K.iso_z(u_end), 0])
    rows.sort(key=lambda r: (r[5], r[0], r[2]))
    return rows


USER_COLS = ["Login", "Display Name", "Email", "Role", "Team", "Time Zone", "Created (UTC)", "Created By", "Status",
             "Deactivated (UTC)"]


def user_rows(D, people_teams):
    """The ACD's user list as the admin exported it on 29 October 2026."""
    staff = D.staff
    rows = []
    R = K.rng("users")
    season0 = K.season_open(K.SEASON_CRM)
    f0, f1 = K.fortnight(K.SEASON_CRM)
    v0 = f0 - dt.timedelta(7)
    end_v = dt.datetime.combine(f1 + dt.timedelta(1), dt.time(14, 10))
    for i, e in enumerate(staff):
        if e.kind == "expert":
            first_day = season0 if e.first < K.SEASON_CRM else (e.golive - dt.timedelta(28))
            created = dt.datetime.combine(first_day - dt.timedelta(int(R.integers(3, 12))), dt.time(13, 0)) + \
                dt.timedelta(minutes=int(R.integers(0, 240)))
            team = people_teams.get(e.emp, "")
            rows.append([D.login0[i], D.display(i), D.email(i), "Agent", team, "America/Toronto", K.iso_z(K.to_utc(created)),
                         "wfm.provisioning", "Active", ""])
        else:
            created = dt.datetime.combine(v0 - dt.timedelta(5), dt.time(10, 0)) + dt.timedelta(minutes=int(R.integers(0, 50)))
            relog = D.relogin.get(i)
            if relog:
                lock_day, lock_h, new = relog
                dis = dt.datetime.combine(dt.date.fromordinal(lock_day), dt.time(0)) + dt.timedelta(hours=lock_h - 0.02)
                rows.append([D.login0[i], D.display(i), D.email(i), "Agent", "HCS Moncton", "America/Moncton",
                             K.iso_z(K.to_utc(created)), "hcs.provisioning", "Disabled", K.iso_z(K.to_utc(dis))])
                cr = dt.datetime.combine(dt.date.fromordinal(lock_day), dt.time(0)) + dt.timedelta(hours=lock_h)
                rows.append([new, D.display(i), D.email(i), "Agent", "HCS Moncton", "America/Toronto", K.iso_z(K.to_utc(cr)),
                             "servicedesk", "Disabled", K.iso_z(K.to_utc(end_v))])
            else:
                rows.append([D.login0[i], D.display(i), D.email(i), "Agent", "HCS Moncton", "America/Moncton",
                             K.iso_z(K.to_utc(created)), "hcs.provisioning", "Disabled", K.iso_z(K.to_utc(end_v))])
    for code, (f, last) in D.leads:
        created = dt.datetime.combine(v0 - dt.timedelta(6), dt.time(15, 0)) + dt.timedelta(minutes=int(R.integers(0, 30)))
        email = ("%s.%s@%s" % (_ascii(f), _ascii(last), DOMAIN_VENDOR)).lower()
        rows.append([D.lead_login[code], "%s %s" % (f, last), email, "Supervisor", "HCS Moncton", "America/Moncton",
                     K.iso_z(K.to_utc(created)), "hcs.provisioning", "Disabled", K.iso_z(K.to_utc(end_v))])
    # the contact centre's own administrators and reporting accounts
    for lg, nm, role in (("wfm.provisioning", "WFM Provisioning", "Administrator"), ("servicedesk", "Service Desk",
                         "Administrator"), ("hcs.provisioning", "HCS Provisioning", "Administrator"),
                         ("rpt.export", "Reporting Export", "Reporting")):
        rows.append([lg, nm, "", role, "", "America/Toronto", "2025-11-03T15:12:40Z", "system", "Active", ""])
    rows.sort(key=lambda r: (r[6], r[0]))
    return rows


# ------------------------------------------------------------------------------------------------- the contact detail
def sess_id(s):
    """The ACD's session identifier: 16 hex digits."""
    return K.token("session", s, n=16)


CONTACT_COLS = ["Contact ID", "Session ID", "Queue", "Channel", "Queued (UTC)", "Offered (UTC)", "Agent Login",
                "Result", "Answered (UTC)", "Ended (UTC)", "CRM Interaction"]


def contact_rows(atts, recs, crm_ids, D, staff):
    """The English queue's ACD contact detail for the customers who joined the queue in the 2026 deadline
    fortnight. crm_ids maps a CRM record's index to its Interaction ID."""
    f0, f1 = K.fortnight(K.SEASON_CRM)
    a = atts[(atts["queue"] == 0)]
    # the customer's first time in the queue on the session decides whether the session is in the fortnight
    first_q = {}
    for r in a:
        s = int(r["session"])
        q = (int(r["day"]), float(r["queued"]))
        if s not in first_q or q < first_q[s]:
            first_q[s] = q
    keep = {s for s, (dd, q) in first_q.items() if f0.toordinal() <= dd <= f1.toordinal()}
    rec_key = {}
    en = np.where(recs["queue"] == 0)[0]
    for i in en:
        rec_key[(int(recs["day"][i]), int(recs["expert"][i]), round(float(recs["start"][i]) * 3600))] = int(i)
    Rch = K.rng("abandon_channel")
    chw = np.array([c[1] for c in W.CHANNELS])
    rows = []
    for r in a:
        if int(r["session"]) not in keep:
            continue
        day, res = int(r["day"]), int(r["result"])
        xi = int(r["expert"])
        q = K.iso_z(_utc(day, float(r["queued"])))
        cid = str(4417000000 + 3 * int(r["acd_contact"]))
        sid = sess_id(int(r["session"]))
        if res == 3:
            ch = W.CHANNELS[int(Rch.choice(3, p=chw))][0] if r["channel"] < 0 else W.CHANNELS[int(r["channel"])][0]
            rows.append([cid, sid, "Live Experts EN", ch, q, "", "", "Abandoned", "",
                         K.iso_z(_utc(day, float(r["ended"]))), ""])
            continue
        t = float(r["offered"])
        login = D.login_at(xi, day, t)
        if res == 1:
            # the channel of a re-offered contact is the one the answering row carries; fill it after
            rows.append([cid, sid, "Live Experts EN", None, q, K.iso_z(_utc(day, t)),
                         login, "No answer", "", K.iso_z(_utc(day, float(r["ended"]))), ""])
        elif res == 2:
            rows.append([cid, sid, "Live Experts EN", "Video", q, K.iso_z(_utc(day, t)),
                         login, "Answered", K.iso_z(_utc(day, t)), K.iso_z(_utc(day, t + float(r["lost"]))), ""])
        else:
            i = rec_key[(day, xi, round(t * 3600))]
            ch = W.CHANNELS[int(recs["channel"][i])][0]
            talk_end = float(recs["start"][i]) + float(recs["talk"][i]) / 3600
            rows.append([cid, sid, "Live Experts EN", ch, q, K.iso_z(_utc(day, t)),
                         login, "Answered", K.iso_z(_utc(day, t)), K.iso_z(_utc(day, talk_end)), crm_ids[i]])
    # a contact's re-offer carries its channel
    ch_of = {}
    for row in rows:
        if row[3] is not None:
            ch_of.setdefault(row[0], row[3])
    for row in rows:
        if row[3] is None:
            row[3] = ch_of.get(row[0], "Chat")
    rows.sort(key=lambda r: (r[4], r[0], r[5] or ""))
    return rows


# ------------------------------------------------------------------------------------------------- the outsourcer's paperwork
ONBOARD_COLS = ["HCS Agent ID", "Agent Name", "Email", "ACD Login", "Team Lead", "First Shift", "Site"]
LEAD_COLS = ["Team Lead ID", "Name", "Email", "ACD Login", "Agents"]
RATE = 38.50                 # Canadian dollars per billed agent hour, deadline period 2026
HST = 0.15                   # New Brunswick harmonized sales tax
INVOICES = [                 # number, week starting, issued
    ("HCS-26-0417", dt.date(2026, 4, 13), dt.date(2026, 4, 20)),
    ("HCS-26-0431", dt.date(2026, 4, 20), dt.date(2026, 4, 27)),
    ("HCS-26-0446", dt.date(2026, 4, 27), dt.date(2026, 5, 4)),
]
REVISED = ("HCS-26-0478", dt.date(2026, 4, 27), dt.date(2026, 5, 19), "HCS-26-0446")


def onboarding_rows(D):
    f0, _ = K.fortnight(K.SEASON_CRM)
    v0 = f0 - dt.timedelta(7)
    lead_of = {}
    rows = []
    for k, xi in enumerate(D.vend):
        code, (lf, ll) = D.leads[k % 3]
        lead_of.setdefault(code, 0)
        lead_of[code] += 1
        rows.append([D.staff[xi].emp, D.display(xi), D.email(xi), D.login0[xi], "%s %s" % (lf, ll), v0, "Moncton"])
    leads = []
    for code, (f, last) in D.leads:
        leads.append([code, "%s %s" % (f, last), ("%s.%s@%s" % (_ascii(f), _ascii(last), DOMAIN_VENDOR)).lower(),
                      D.lead_login[code], lead_of.get(code, 0)])
    return rows, leads


def invoice_lines(clocks, D):
    """Each invoice's lines: agent ID and hours. The outsourcer bills each agent's time-and-attendance hours on the
    program, less meal and rest breaks; its first week-3 invoice was billed from the schedule while the time clock's
    export was down, less rest breaks only, and the revised invoice replaced it."""
    by = {}
    for c in clocks:
        d = dt.date.fromordinal(c["day"])
        wk = K.monday(d)
        emp = D.staff[c["xi"]].emp
        tc = (c["cout"] - c["cin"]) - c["breaks"]
        meal = 0.5 if c["breaks"] >= 0.5 else 0.0
        sched = c["sched"] - (c["breaks"] - meal)
        o = by.setdefault((wk, emp), [0.0, 0.0])
        o[0] += tc
        o[1] += sched
    out = {}
    for no, wk, issued in INVOICES:
        lines = sorted((emp, round(v[1] if no == "HCS-26-0446" else v[0], 2)) for (w, emp), v in by.items() if w == wk)
        out[no] = lines
    no, wk, issued, _rep = REVISED
    out[no] = sorted((emp, round(v[0], 2)) for (w, emp), v in by.items() if w == wk)
    return out
