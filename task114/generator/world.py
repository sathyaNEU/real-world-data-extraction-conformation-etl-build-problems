"""The world for task114: the firm calendar, the people, the rooms, who was in which office each day, the
meetings they held, and the room bookings each office's platform recorded.

Every quantity downstream is computed from what this module writes into target/, never from these objects.
"""
import datetime as dt
from collections import defaultdict

import numpy as np
from faker import Faker

D = dt.date
T = dt.datetime
START, END = D(2025, 10, 1), D(2026, 9, 30)
HOLIDAYS = {
    D(2025, 10, 13): "Thanksgiving", D(2025, 12, 25): "Christmas Day", D(2025, 12, 26): "Boxing Day",
    D(2026, 1, 1): "New Year's Day", D(2026, 2, 16): "Family Day", D(2026, 4, 3): "Good Friday",
    D(2026, 5, 18): "Victoria Day", D(2026, 7, 1): "Canada Day", D(2026, 8, 3): "Civic Holiday",
    D(2026, 9, 7): "Labour Day",
}
CLOSURE = {D(2025, 12, 24), D(2025, 12, 29), D(2025, 12, 30), D(2025, 12, 31), D(2026, 1, 2)}
DOMAIN = "harrowfield.ca"
OFFICES = {1: "Adelaide Street", 2: "Front Street"}

# legacy firm A (Adelaide Street): structures and civil; legacy firm B (Front Street): transportation
PRACTICES = {
    1: [("STR", "Structures", 5), ("BRG", "Bridges", 3), ("CIV", "Civil & Municipal", 5), ("WTR", "Water", 3),
        ("GEO", "Geotechnical", 2), ("BSV", "Building Services", 2), ("COR", "Corporate Services", 2)],
    2: [("TPL", "Transportation Planning", 5), ("TRF", "Traffic Engineering", 3), ("TRN", "Transit", 4),
        ("URB", "Urban Design", 2), ("ENV", "Environmental Assessment", 3), ("COR", "Corporate Services", 1),
        ("BDV", "Business Development", 1)],
}
ANCHORS = [(1, 3), (1, 2), (2, 3), (1, 3), (2, 3), (0, 2), (1, 2), (2, 4)]


def calendar():
    days = [START + dt.timedelta(d) for d in range((END - START).days + 1)]
    work = [d for d in days if d.weekday() < 5 and d not in HOLIDAYS and d not in CLOSURE]
    return days, work


# ---------------------------------------------------------------- rooms
def rooms():
    """Room register rows. A room whose type or availability changed in the year has one row per spell."""
    R = []

    def add(code, office, floor, name, seats, rtype, frm=D(2019, 1, 1), to=None, comb=""):
        R.append(dict(room_code=code, office=OFFICES[office], floor=floor, room_name=name, seats=seats,
                      room_type=rtype, combinable_with=comb, valid_from=frm, valid_to=to))

    A = [("AD-3.01", "Brant", 4), ("AD-3.02", "Credit", 4), ("AD-3.03", "Don", 4), ("AD-4.01", "Etobicoke", 4),
         ("AD-4.02", "Grand", 4), ("AD-4.03", "Humber", 4), ("AD-5.01", "Mimico", 4), ("AD-5.02", "Rouge", 4),
         ("AD-5.03", "Saugeen", 4), ("AD-6.01", "Speed", 4), ("AD-6.02", "Thames", 4),
         ("AD-6.03", "Nottawasaga", 4), ("AD-3.04", "Bloor", 6), ("AD-3.05", "College", 6),
         ("AD-4.04", "Dundas", 6), ("AD-4.05", "Queen", 6), ("AD-5.04", "Richmond", 6), ("AD-5.05", "Sumach", 6),
         ("AD-6.04", "Wellesley", 6), ("AD-4.07", "Lambton", 8),
         ("AD-4.08", "Leaside", 8), ("AD-4.09", "Moore Park", 8), ("AD-5.10", "Parkdale", 12),
         ("AD-5.11", "Junction", 12), ("AD-6.14", "Distillery", 12)]
    for code, nm, seats in A:
        add(code, 1, int(code[3]), nm, seats, "meeting")
    add("AD-3.06", 1, 3, "Scarborough", 8, "meeting", comb="AD-3.07")
    add("AD-3.08", 1, 3, "Highland Creek", 4, "meeting", to=D(2026, 9, 30))
    add("AD-3.08", 1, 3, "Highland Creek", 4, "project room", frm=D(2026, 10, 1))
    add("AD-3.07", 1, 3, "Bluffs", 8, "meeting", comb="AD-3.06")
    add("AD-3.06+07", 1, 3, "Scarborough Bluffs (combined)", 18, "meeting", comb="AD-3.06;AD-3.07")
    add("AD-6.12", 1, 6, "Fort York", 12, "meeting", comb="AD-6.13")
    add("AD-6.13", 1, 6, "Garrison", 12, "meeting", comb="AD-6.12")
    add("AD-6.12+13", 1, 6, "Fort York Garrison (combined)", 26, "meeting", comb="AD-6.12;AD-6.13")
    add("AD-6.05", 1, 6, "Berczy", 6, "meeting", to=D(2026, 8, 30))
    add("AD-6.05", 1, 6, "Berczy", 6, "project room", frm=D(2026, 8, 31))
    add("AD-5.08", 1, 5, "Riverdale", 8, "meeting", to=D(2026, 5, 31))
    add("AD-5.08", 1, 5, "Riverdale", 8, "project room", frm=D(2026, 6, 1))
    add("AD-4.10", 1, 4, "Cabbagetown", 10, "meeting", to=D(2026, 2, 1))
    add("AD-4.10", 1, 4, "Cabbagetown", 10, "client", frm=D(2026, 2, 2))
    add("AD-7.01", 1, 7, "Boardroom", 16, "client")
    add("AD-7.02", 1, 7, "Ontario", 10, "client")
    add("AD-7.03", 1, 7, "Huron", 6, "client")
    add("AD-7.04", 1, 7, "Erie", 6, "client")
    add("AD-1.00", 1, 1, "Commons", 140, "event space")
    F = [("FR-3.01", "Spadina", 4), ("FR-3.02", "Bathurst", 4), ("FR-3.03", "Ossington", 4),
         ("FR-3.04", "Dufferin", 4), ("FR-3.05", "Lansdowne", 4), ("FR-4.01", "Keele", 4), ("FR-4.02", "Jane", 4),
         ("FR-4.03", "Kipling", 4), ("FR-4.04", "Islington", 4), ("FR-3.11", "Yonge", 6), ("FR-3.12", "Bay", 6),
         ("FR-3.13", "Church", 6), ("FR-4.11", "Jarvis", 6), ("FR-4.12", "Sherbourne", 6),
         ("FR-4.13", "Parliament", 6), ("FR-4.14", "Broadview", 6), ("FR-4.20", "Union", 8),
         ("FR-4.21", "St Andrew", 8), ("FR-4.22", "Osgoode", 8), ("FR-4.23", "Sackville", 8),
         ("FR-4.24", "Bellwoods", 8), ("FR-3.30", "Harbourfront", 12), ("FR-3.31", "Exhibition", 12),
         ("FR-3.32", "Liberty", 12), ("FR-3.34", "Waterfront", 16), ("FR-3.36", "Cherry Beach", 16), ("FR-3.35", "Lake Shore", 24), ("FR-4.35", "Riverside", 24)]
    for code, nm, seats in F:
        add(code, 2, int(code[3]), nm, seats, "meeting")
    add("FR-2.01", 2, 2, "Toronto Island", 8, "client", to=D(2026, 3, 31))
    add("FR-2.01", 2, 2, "Toronto Island", 8, "meeting", frm=D(2026, 4, 1))
    add("FR-2.02", 2, 2, "Ward's", 6, "client", to=D(2026, 3, 31))
    add("FR-2.02", 2, 2, "Ward's", 6, "meeting", frm=D(2026, 4, 1))
    add("FR-2.03", 2, 2, "Centre Island", 12, "client")
    add("FR-2.04", 2, 2, "Hanlan's", 8, "client")
    add("FR-2.05", 2, 2, "Algonquin", 6, "client", to=D(2026, 9, 30))
    add("FR-2.05", 2, 2, "Algonquin", 6, "meeting", frm=D(2026, 10, 1))
    add("FR-4.06", 2, 4, "Stockyards", 6, "meeting", frm=D(2026, 9, 14))
    add("FR-3.00", 2, 3, "Forum", 90, "event space")
    return R


def room_type_on(R, code, day):
    for r in R:
        if r["room_code"] == code and r["valid_from"] <= day and (r["valid_to"] is None or day <= r["valid_to"]):
            return r["room_type"]
    return None


def bookable_rooms(R, office, day, rtype):
    out = []
    for r in R:
        if r["office"] != OFFICES[office] or r["room_type"] != rtype or "+" in r["room_code"]:
            continue
        if r["valid_from"] <= day and (r["valid_to"] is None or day <= r["valid_to"]):
            out.append(r)
    return out


# ---------------------------------------------------------------- people
class World:
    pass


def build_people(W, rng):
    fk = Faker("en_CA")
    fk.seed_instance(114)
    used_names = {("Claudia", "Hernandez"), ("Louis", "Thompson"), ("Kristie", "Morgan"), ("Caleb", "Walker"),
                  ("Debbie", "Jimenez"), ("Mary", "Hurst")}  # Mary Hurst is the architect, not staff
    used_upn = {"%s.%s" % (a.lower(), b.lower()) for a, b in used_names}
    teams = []
    for office, plist in PRACTICES.items():
        for code, pname, nteams in plist:
            for i in range(nteams):
                tc = "%s-%s%d" % ("A" if office == 1 else "F", code, i + 1)
                teams.append(dict(team=tc, office=office, practice=pname, size=int(rng.integers(14, 24)),
                                  anchor=ANCHORS[int(rng.integers(len(ANCHORS)))]))
    people = []
    emp = 230000
    for t in teams:
        for j in range(t["size"]):
            while True:
                fn, ln = fk.first_name(), fk.last_name()
                if (fn, ln) not in used_names:
                    break
            used_names.add((fn, ln))
            base = ("%s.%s" % (fn, ln)).lower().replace(" ", "").replace("'", "")
            upn = base
            n = 2
            while upn in used_upn:
                upn = "%s%d" % (base, n)
                n += 1
            used_upn.add(upn)
            emp += int(rng.integers(3, 41))
            grade = "Associate" if j == 0 else ("Senior" if j < 4 else ("Admin" if j == t["size"] - 1 else "Staff"))
            people.append(dict(pid=len(people), employee_no=str(emp), first=fn, last=ln,
                               upn="%s@%s" % (upn, DOMAIN), team=t["team"], office=t["office"],
                               practice=t["practice"], grade=grade, start=D(2014, 1, 6) + dt.timedelta(
                                   int(rng.integers(0, 4100))), end=None, part_time=bool(rng.random() < 0.08)))
    # joiners and leavers inside the year
    for p in people:
        r = rng.random()
        if r < 0.06:
            p["start"] = START + dt.timedelta(int(rng.integers(20, 330)))
        elif r < 0.12:
            p["end"] = START + dt.timedelta(int(rng.integers(30, 350)))
    # the people who appear by name in the pack's documents
    named = [("Claudia", "Hernandez", 1, "Associate"), ("Louis", "Thompson", 1, "Partner"),
             ("Kristie", "Morgan", 1, "Senior"), ("Caleb", "Walker", 1, "Senior"), ("Debbie", "Jimenez", 2, "Staff")]
    cor = {o: [p for p in people if p["practice"] == "Corporate Services" and p["office"] == o] for o in (1, 2)}
    taken = set()
    for fn, ln, o, grade in named:
        p = next(x for x in cor[o] if x["pid"] not in taken and x["grade"] != "Associate")
        taken.add(p["pid"])
        p.update(first=fn, last=ln, upn="%s.%s@%s" % (fn.lower(), ln.lower(), DOMAIN), grade=grade, end=None,
                 start=min(p["start"], D(2023, 5, 1)), part_time=False)
    # card ids in each office's system (every employee holds both since the merger)
    a_cards = rng.choice(np.arange(10230000, 10990000), size=len(people), replace=False)
    f_badges = rng.choice(np.arange(20100, 69900), size=len(people), replace=False)
    for p, a, f in zip(people, a_cards, f_badges):
        p["adelaide_card"] = "%08d" % a
        p["front_badge"] = "FS%05d" % f
    W.teams, W.people = teams, people
    W.by_team = defaultdict(list)
    for p in people:
        W.by_team[p["team"]].append(p["pid"])
    # managers: the team's associate and seniors manage; since the merger a share of reporting lines cross offices
    W.manager = {}
    mgrs = {1: [], 2: []}
    for t in teams:
        mem = W.by_team[t["team"]]
        for m in mem[:3]:
            mgrs[t["office"]].append(m)
    for t in teams:
        mem = W.by_team[t["team"]]
        local = mem[:3]
        for k, pid in enumerate(mem):
            if pid == mem[0]:
                continue
            if pid in local:
                W.manager[pid] = mem[0]
                continue
            if rng.random() < 0.46:
                other = 2 if t["office"] == 1 else 1
                W.manager[pid] = int(rng.choice(mgrs[other]))
            else:
                W.manager[pid] = int(local[1 + k % 2])
    # team leads report to a practice lead in the same office
    for t in teams:
        lead = W.by_team[t["team"]][0]
        peers = [W.by_team[u["team"]][0] for u in teams if u["office"] == t["office"] and u["team"] != t["team"]]
        W.manager[lead] = int(rng.choice(peers))
    # sector programmes since the merger: each draws from two Adelaide and two Front Street teams
    names = ["Rail stations programme", "Bridge rehabilitation framework", "Waterfront transit assessment",
             "Regional rapid transit design", "Water treatment upgrades", "Active transportation network",
             "Highway interchange renewals", "Transit maintenance facility", "Stormwater master plan",
             "Downtown streetscape", "Grade separation programme", "Airport access study",
             "Port lands flood protection", "Municipal asset management", "Hospital campus civil works",
             "Signal priority rollout", "School travel planning", "Corridor safety audits",
             "Tunnel ventilation review", "District energy connections"]
    W.programmes = []
    ateams = [t["team"] for t in teams if t["office"] == 1]
    fteams = [t["team"] for t in teams if t["office"] == 2]
    for g, nm in enumerate(names):
        ts = list(rng.choice(ateams, 2, replace=False)) + list(rng.choice(fteams, 2, replace=False))
        mem = []
        for tc in ts:
            pool = W.by_team[tc]
            mem += [int(x) for x in rng.choice(pool, min(len(pool), int(rng.integers(3, 7))), replace=False)]
        W.programmes.append(dict(name=nm, members=mem))
    W.prog_of = defaultdict(list)
    for g, pr in enumerate(W.programmes):
        for m in pr["members"]:
            W.prog_of[m].append(g)


def employed(p, day):
    return p["start"] <= day and (p["end"] is None or day <= p["end"])


# ---------------------------------------------------------------- presence
def build_presence(W, rng):
    days, work = calendar()
    W.days, W.work = days, work
    wd = np.array([d.weekday() for d in work])
    N, Dn = len(W.people), len(work)
    pres = np.zeros((N, Dn), dtype=np.int8)
    team_anchor = {t["team"]: t["anchor"] for t in W.teams}
    # leave: three to four blocks a year, heavier in summer and at March break
    for p in W.people:
        anc = team_anchor[p["team"]]
        base = np.where(np.isin(wd, anc), 0.80, np.where((wd == 0) | (wd == 4), 0.10, 0.21))
        if p["part_time"]:
            base = np.where(wd == 4, 0.0, base)
        on = rng.random(Dn) < base
        for _ in range(int(rng.integers(3, 5))):
            s = int(rng.integers(0, Dn - 6))
            on[s:s + int(rng.integers(2, 9))] = False
        for i, d in enumerate(work):
            if not employed(p, d):
                on[i] = False
        pres[p["pid"], on] = p["office"]
    # visits: some days a person works from the other office (programme work)
    for p in W.people:
        if not W.prog_of.get(p["pid"]):
            continue
        idx = np.where(pres[p["pid"]] > 0)[0]
        k = rng.random(len(idx)) < 0.045
        pres[p["pid"], idx[k]] = 3 - p["office"]
    W.pres = pres
    W.wd = wd


# ---------------------------------------------------------------- meetings
ADHOC_RATE = 2.1
SLOTS = [8 * 60 + 30 + 30 * i for i in range(18)]  # 08:30 .. 17:00


def build_meetings(W, rng):
    """Calendar meetings, one dict per occurrence. Times are minutes after midnight, Toronto local."""
    M = []
    work, wd = W.work, W.wd
    di_of = {d: i for i, d in enumerate(work)}
    people = W.people

    def att_list(pids, org):
        out = []
        for q in pids:
            q = int(q)
            if q == org:
                out.append((q, "required", "organizer"))
                continue
            r = rng.random()
            resp = "accepted" if r < 0.60 else ("tentative" if r < 0.70 else ("none" if r < 0.80 else "declined"))
            typ = "optional" if rng.random() < 0.13 else "required"
            out.append((q, typ, resp))
        return out

    def emp_on(pids, day):
        return [q for q in pids if employed(people[q], day)]

    # team syncs, weekly on the first anchor day, slotted so big rooms never collide
    big_slots = defaultdict(int)
    for t in W.teams:
        mem = W.by_team[t["team"]]
        dow = t["anchor"][0]
        k = big_slots[(t["office"], dow)]
        big_slots[(t["office"], dow)] += 1
        st = [9 * 60, 10 * 60, 11 * 60, 13 * 60 + 30, 14 * 60 + 30, 15 * 60 + 30][k % 6]
        sid = "S%06d" % len(M)
        for i, d in enumerate(work):
            if wd[i] != dow:
                continue
            org = mem[0]
            att = emp_on(mem, d)
            if org not in att:
                continue
            M.append(dict(day=d, start=st, dur=60, org=org, att=att_list(att, org), kind="team", series=sid,
                          subject="%s weekly" % t["team"].split("-")[1][:3]))
    # team working sessions on anchor days
    for t in W.teams:
        mem = W.by_team[t["team"]]
        for i, d in enumerate(work):
            if wd[i] not in t["anchor"]:
                continue
            for _ in range(int(rng.integers(1, 3))):
                k = int(rng.integers(3, 7))
                pick = emp_on([int(x) for x in rng.choice(mem, k, replace=False)], d)
                if len(pick) < 2:
                    continue
                M.append(dict(day=d, start=int(rng.choice(SLOTS[:-2])), dur=int(rng.choice([30, 60, 60, 90])),
                              org=pick[0], att=att_list(pick, pick[0]), kind="work", series="",
                              subject="Working session"))
    # programme workstreams, weekly, across both offices
    for g, pr in enumerate(W.programmes):
        mem = pr["members"]
        for w in range(int(rng.integers(2, 5))):
            dow = int(rng.choice([1, 2, 3]))
            st = int(rng.choice(SLOTS[:-2]))
            ws = [int(x) for x in rng.choice(mem, min(len(mem), int(rng.integers(3, 8))), replace=False)]
            sid = "S%06d" % len(M)
            for i, d in enumerate(work):
                if wd[i] != dow:
                    continue
                att = emp_on(ws, d)
                if len(att) < 2:
                    continue
                M.append(dict(day=d, start=st, dur=60, org=att[0], att=att_list(att, att[0]), kind="prog",
                              series=sid, subject="%s: workstream %d" % (pr["name"], w + 1)))
    # one-to-ones, weekly
    reports = defaultdict(list)
    for pid, m in W.manager.items():
        reports[m].append(pid)
    for m, reps in reports.items():
        for r in reps[:7]:
            dow = int(rng.choice([1, 2, 3, 0, 1, 2, 3]))
            st = int(rng.choice(SLOTS))
            sid = "S%06d" % len(M)
            for i, d in enumerate(work):
                if wd[i] != dow:
                    continue
                att = emp_on([m, r], d)
                if len(att) < 2:
                    continue
                M.append(dict(day=d, start=st, dur=45 if st % 60 == 0 else 30, org=m, att=att_list(att, m),
                              kind="1:1", series=sid, subject="1:1"))
    # ad hoc meetings: mostly pairs, many across offices since the merger
    office = np.array([p["office"] for p in people])
    n_adhoc = int(len(people) * ADHOC_RATE * len(work) / 5)
    for _ in range(n_adhoc):
        i = int(rng.integers(len(work)))
        d = work[i]
        org = int(rng.integers(len(people)))
        if not employed(people[org], d):
            continue
        k = 1 if rng.random() < 0.70 else int(rng.choice([2, 2, 3]))
        if rng.random() < 0.70:
            pool = np.where(office != office[org])[0]
        else:
            pool = np.where(office == office[org])[0]
        others = emp_on([int(x) for x in rng.choice(pool, k, replace=False)], d)
        if not others:
            continue
        pick = [org] + [q for q in others if q != org]
        M.append(dict(day=d, start=int(rng.choice(SLOTS)), dur=int(rng.choice([30, 60, 60])), org=org,
                      att=att_list(pick, org), kind="adhoc", series="", subject="Catch-up"))
    # cancelled occurrences stay in the calendar flagged as cancelled; some series occurrences were moved
    for m in M:
        m["cancelled"] = bool(rng.random() < 0.035)
        m["noshow_draw"] = float(rng.random())
        m["pattern_start"] = None
        if m["series"] and not m["cancelled"] and rng.random() < 0.06:
            if 9 * 60 + 30 <= m["start"] <= 11 * 60 + 30:
                shift = int(rng.choice([120, 150, 180, 210]))
            else:
                shift = int(rng.choice([-120, -90, -60, 60, 90, 120]))
            ns = m["start"] + shift
            if SLOTS[0] <= ns <= SLOTS[-1] and ns + m["dur"] <= 18 * 60:
                m["pattern_start"] = m["start"]
                m["start"] = ns
    W.meetings = M


def build_client_and_events(W, rng):
    """Client meetings in each office's client suite; monthly town halls in both event spaces; solo calls."""
    C = []
    for i, d in enumerate(W.work):
        for office in (1, 2):
            staff = [p["pid"] for p in W.people if p["office"] == office and W.pres[p["pid"], i] == office]
            for _ in range(int(rng.integers(3, 7) if office == 2 else rng.integers(4, 8))):
                if len(staff) < 3:
                    break
                k = int(rng.integers(1, 4))
                pick = [int(x) for x in rng.choice(staff, k, replace=False)]
                C.append(dict(day=d, start=int(rng.choice(SLOTS[1:-4])), dur=int(rng.choice([60, 90, 120])),
                              org=pick[0], att=[(q, "required", "organizer" if q == pick[0] else "accepted")
                                                for q in pick], office=office,
                              ext=int(rng.integers(1, 4)), kind="client", series="", cancelled=False,
                              subject="Client meeting"))
    W.client = C
    # town halls: first Wednesday of each month at noon, in both event spaces
    E = []
    for i, d in enumerate(W.work):
        if d.weekday() == 2 and d.day <= 7:
            E.append(dict(day=d, start=12 * 60, dur=60, org=W.by_team[W.teams[0]["team"]][0],
                          att=[(p["pid"], "required", "accepted") for p in W.people if employed(p, d)],
                          kind="townhall", series="", cancelled=False, subject="Town hall"))
    W.events = E
    # solo calls: Front Street people book a room through Outlook for a call, some on a standing weekly call;
    # Adelaide people mostly use the app, and some book the room through Outlook
    S = []
    for i, d in enumerate(W.work):
        here = np.where(W.pres[:, i] > 0)[0]
        pick = rng.choice(here, int(len(here) * 0.10), replace=False)
        for q in pick:
            q = int(q)
            o = int(W.pres[q, i])
            S.append(dict(day=d, start=int(rng.choice(SLOTS)), dur=int(rng.choice([30, 30, 60])), org=q,
                          office=o, kind="solo", series="", pattern_start=None,
                          outlook=(o == 2) or (rng.random() < 0.32)))
    standing = [p["pid"] for p in W.people if p["office"] == 2 and rng.random() < 0.18]
    W.standing = {}
    for q in standing:
        dow = int(rng.choice([1, 2, 3]))
        st = int(rng.choice([9 * 60 + 30, 10 * 60, 10 * 60 + 30, 11 * 60, 11 * 60 + 30, 13 * 60 + 30, 14 * 60]))
        sid = "C%06d" % q
        W.standing[sid] = dict(org=q, dow=dow, start=st)
        for i, d in enumerate(W.work):
            if W.wd[i] != dow or W.pres[q, i] != 2:
                continue
            ps = None
            start = st
            if rng.random() < 0.07:
                ps, start = st, st + int(rng.choice([180, 210, 240]))
            S.append(dict(day=d, start=start, dur=30, org=q, office=2, kind="solo", series=sid, pattern_start=ps,
                          outlook=True))
    W.solo = S
