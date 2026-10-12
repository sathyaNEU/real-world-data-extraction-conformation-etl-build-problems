"""The Ask A devices, decided on the simulated bookings before the exports are written.

A1  Adelaide Street: a checked-in booking given back early at the room panel. The export keeps status Confirmed and
    carries the give-back time in released_at.
A2  Adelaide Street: from the platform upgrade a combined booking is one row for the combined room; before it the
    platform also wrote a hold for each half (/1, /2).
F1  Front Street: a cancelled occurrence of a series is an exception row, and the series row for its slot stays in the
    series' room. Standing calls are cancelled on some of the days their owner was not in.
F2  Front Street: a moved occurrence's series row stays at the old slot in the series' usual room, which is not always
    the room the moved occurrence took.
C1  Both offices: a client meeting held in a meeting room when the client suite was full. It held the meeting room,
    and the brief sends client meetings to the client suite, so it is out of the room count the bookings justify.
S1  Both offices: a personal focus block held in a meeting room. One person booked the room, as for a call, but the
    calendar item is the focus block, not a call, so its hours are out of the hours one person booked for a call.
G1  Both offices: a call with someone outside the firm on the line. One person from the firm booked the room and took
    the call there; the outside party is on the invite, so Adelaide Street's headcount reads two (the booker counted
    the person on the line) and Front Street's attendee_count reads three. It is a call taken by one person, so it is
    in the call hours and out of the room count, which a headcount read of one person gets the wrong way round.

The legacy reading is the convention set the portal's top responses filed: release keyed on status, combined rows
dropped, cancelled rows filtered before exceptions are folded, the fold keyed on the room, people on a booking read from
its headcount, and every non-call booking in a meeting room counted toward the room count. A device row is kept only
if each quarter's close-out busiest moment (value and date, meeting and client rooms) stays the same on the legacy
reading as on the correct one, so the close-outs certify both readings and point at neither. Where a quarter's
meeting-room peak sits on that busiest moment, client meetings are re-timed off it or an ordinary client meeting earlier
in the quarter takes the busiest moment first.
"""
from collections import Counter, defaultdict

import numpy as np

import world
from world import D

ADL, FRT = 1, 2
QUARTERS = [("Q1", D(2025, 10, 1), D(2025, 12, 31)), ("Q2", D(2026, 1, 1), D(2026, 3, 31)),
            ("Q3", D(2026, 4, 1), D(2026, 6, 30)), ("Q4", D(2026, 7, 1), D(2026, 9, 30))]
UPGRADE = D(2026, 5, 19)          # Adelaide platform 6.2: a combined booking is written as one row from this date
GIVE_BACK_RATE = {"meeting": 0.07, "solo": 0.09}   # checked-in bookings given back early at the panel
STANDING_CANCEL_RATE = 0.40       # standing-call occurrences cancelled on a day their owner was out
STANDING_MOVE_RATE = 0.10         # standing-call occurrences moved later that day into another room
CLIENT_IN_MEETING_ROOM = 0.03     # client meetings put in a free meeting room
FOCUS_IN_ROOM = 0.30              # focus blocks, on a day their owner was in, held in a meeting room
GUEST_CALL_RATE = {1: 0.17, 2: 0.06}   # single Outlook calls with an outside party on the line (Adelaide's Outlook
                                       # calls are the scheduled ones; Front Street books every call through Outlook)
GUEST_DOMAINS = ["metrolinx-partner.ca", "cityworks.ca", "regionplan.ca", "hydrotek.ca"]   # the client meetings' guests
GUEST_SUBJECTS = ["Catch-up", "Catch-up", "Check-in", "Sync", "Design coordination", "Design review", "Progress update",
                  "Scope review", "Data request", "Quick check-in"]
GUEST_CALL_SUBJECTS = ["Client call", "Teams call", "Call re scope"]
GUEST_MARGIN = 3                  # days lifted beyond the thirteen the headcount read needs, so that dropping combined
                                  # bookings or tentative holds as well cannot take the count back to the answer
READINGS = ("true", "legacy")
RULE_DAYS = 12
MAIN_COUNT = 31                   # the new office's count (frozen in asserts.py); no reading of the two offices' own
                                  # counts may add up to it
# which meeting-room bookings count toward the room count the bookings justify: own on each reading (the correct one
# leaves client meetings out, as the brief sends them to the client suite), and ownc, the correct reading with the
# client meetings left in, which is what a solver who reads every other device right but keeps them files
# ownf is the correct reading with the focus blocks left in, which must land on the same room count: a one-person
# booking is out of the count whether it was a call or a focus block
# owng is the correct reading with the calls that had an outside party on the line counted as meetings (people read
# from the headcount), and owncg the same with the client meetings left in as well; gcall is such a call's hold
OWN = {("true", "own"): lambda kind: kind not in ("solo", "focus", "client", "townhall", "gcall"),
       ("true", "ownc"): lambda kind: kind not in ("solo", "focus", "townhall", "gcall"),
       ("true", "ownf"): lambda kind: kind not in ("solo", "client", "townhall", "gcall"),
       ("true", "owng"): lambda kind: kind not in ("solo", "focus", "client", "townhall"),
       ("true", "owncg"): lambda kind: kind not in ("solo", "focus", "townhall"),
       ("legacy", "own"): lambda kind: kind not in ("solo", "focus", "townhall")}


def quarter(day):
    for q, a, b in QUARTERS:
        if a <= day <= b:
            return q
    return None


class Grid:
    """Rooms held minute by minute, per reading, office, scope and day. Scopes: meet (meeting rooms), all (meeting and
    client rooms, the close-outs' scope) and own (meeting-room bookings that count toward the room count)."""

    def __init__(self, W):
        self.W = W
        self.c = {}
        self._type = {}
        self.qdays = {q: [d for d in W.work if a <= d <= b] for q, a, b in QUARTERS}

    def rtype(self, code, day):
        k = (code, day)
        if k not in self._type:
            self._type[k] = world.room_type_on(self.W.rooms, code, day)
        return self._type[k]

    def arr(self, reading, office, scope, day):
        k = (reading, office, scope, day)
        if k not in self.c:
            self.c[k] = np.zeros(1440, dtype=np.int16)
        return self.c[k]

    def hold(self, readings, office, code, day, s, e, sign=1, kind="meeting"):
        t = self.rtype(code, day)
        for rd in readings:
            if t == "meeting":
                scopes = ("all", "meet") + tuple(sc for (r, sc), f in OWN.items() if r == rd and f(kind))
            elif t == "client":
                scopes = ("all",)
            else:
                scopes = ()
            for sc in scopes:
                self.arr(rd, office, sc, day)[s:e] += sign

    def qmax(self, reading, office, scope, q):
        best, when = -1, None
        for day in self.qdays[q]:
            a = self.c.get((reading, office, scope, day))
            if a is None:
                continue
            m = int(a.max())
            if m > best:
                best, when = m, day
        return best, when

    def own(self, reading, office, scope="own"):
        vals = sorted((int(self.c[(reading, office, scope, d)].max()) if (reading, office, scope, d) in self.c else 0)
                      for d in self.W.work)
        return vals[::-1][RULE_DAYS]

    def referee_ok(self, office, q):
        return self.qmax("true", office, "all", q) == self.qmax("legacy", office, "all", q)

    def peak_moved(self, office, q):
        return self.qmax("true", office, "meet", q)[0] != self.qmax("legacy", office, "meet", q)[0]

    def moved_peaks(self):
        return {(o, q) for o in (ADL, FRT) for q, _, _ in QUARTERS if self.peak_moved(o, q)}


class Planner:
    def __init__(self, W, seed):
        self.W = W
        self.seed = seed
        self.rng = np.random.default_rng([seed, 23])
        self.G = Grid(W)
        self.held = W.rooms_held.held
        self.ghost_held = defaultdict(list)       # (room, day) -> [(s, e)] series rows already placed
        self.log = Counter()
        W.ghosts = []                             # Front Street series rows left at a superseded slot
        W.standing_cancelled = []                 # standing-call occurrences cancelled on a day their owner was out
        W.boosts = []

    # ------------------------------------------------------------------ helpers
    def free(self, room, day, s, e):
        return all(e <= a or b <= s for a, b in self.held.get((room, day), [])) and \
            all(e <= a or b <= s for a, b in self.ghost_held[(room, day)])

    def try_change(self, office, day, apply, undo):
        apply()
        if self.G.referee_ok(office, quarter(day)):
            return True
        undo()
        return False

    def runs(self, office, reading, scope, day, level):
        """Maximal runs of minutes at `level` on one day, as (t0, t1)."""
        a = self.G.c.get((reading, office, scope, day))
        if a is None:
            return []
        idx = np.where(a == level)[0]
        out = []
        if len(idx):
            start = prev = int(idx[0])
            for t in idx[1:]:
                t = int(t)
                if t != prev + 1:
                    out.append((start, prev + 1))
                    start = t
                prev = t
            out.append((start, prev + 1))
        return out

    def qruns(self, office, reading, q, level):
        return [(day, a, b) for day in self.G.qdays[q] for a, b in self.runs(office, reading, "meet", day, level)]

    def usual_rooms(self):
        """Each Front Street series' rooms, most used first; the first is the room its series rows name."""
        c = defaultdict(Counter)
        for b in self.W.bookings:
            if b["office"] == FRT and b["series"] and b["kind"] in ("meeting", "solo"):
                c[b["series"]][b["room"]] += 1
        self.series_rooms = {sid: [r for r, _ in sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))]
                             for sid, cnt in c.items()}
        return {sid: rs[0] for sid, rs in self.series_rooms.items()}

    def meeting_room_for(self, office, day, s, e, n, exclude=()):
        rooms = sorted((r for r in world.bookable_rooms(self.W.rooms, office, day, "meeting")
                        if r["seats"] >= n and r["room_code"] not in exclude),
                       key=lambda r: (r["seats"], r["room_code"]))
        return next((r["room_code"] for r in rooms if self.free(r["room_code"], day, s, e)), None)

    # ------------------------------------------------------------------ base and the upgrade
    def base(self):
        for b in self.W.bookings:
            if b["kind"] == "cancelled":
                continue
            e = b["released"] if b["kind"] == "noshow" else b["e"]
            for r in (b["halves"] or [b["room"]]):
                self.G.hold(READINGS, b["office"], r, b["day"], b["s"], e, kind=b["kind"])

    def upgrade(self):
        for b in self.W.bookings:
            if b["office"] == ADL and b["halves"] and b["kind"] != "cancelled" and b["day"] >= UPGRADE:
                b["one_row"] = True
                e = b["released"] if b["kind"] == "noshow" else b["e"]
                for h in b["halves"]:
                    self.G.hold(("legacy",), ADL, h, b["day"], b["s"], e, -1, b["kind"])
                self.log["A2 combined bookings without half rows"] += 1
        for q, _, _ in QUARTERS:
            if not self.G.referee_ok(ADL, q):
                lvl, day = self.G.qmax("true", ADL, "all", q)
                assert self.boost(ADL, q, lvl, day) and self.G.referee_ok(ADL, q), ("upgrade moves a close-out", q)

    # ------------------------------------------------------------------ client meetings
    def boost(self, office, q, level, by_day):
        """Add ordinary client meetings so that a moment on a day no later than by_day holds `level` meeting and client
        rooms on both readings. Returns True when the moment exists afterwards."""
        G = self.G
        best = None
        for day in G.qdays[q]:
            if day > by_day:
                break
            t = G.c.get(("true", office, "all", day))
            lg = G.c.get(("legacy", office, "all", day))
            if t is None or lg is None:
                continue
            clients = [r["room_code"] for r in world.bookable_rooms(self.W.rooms, office, day, "client")]
            for m in range(9 * 60 + 30, 16 * 60, 30):
                wt, wl = t[m:m + 60], lg[m:m + 60]
                if not (wt == wl).all() or int(wt.max()) >= level:
                    continue
                need = level - int(wt.max())
                rooms = [r for r in clients if self.free(r, day, m, m + 60)]
                if len(rooms) < need:
                    continue
                key = (need, -int(wt.max()), day, m)
                if best is None or key < best[0]:
                    best = (key, day, m, rooms[:need])
        if best is None:
            return False
        _, day, m, rooms = best
        i = self.W.work.index(day)
        staff = [p["pid"] for p in self.W.people if self.W.pres[p["pid"], i] == office]
        for r in rooms:
            k = len(self.W.client)
            pick = [int(x) for x in self.rng.choice(staff, int(self.rng.integers(1, 3)), replace=False)]
            c = dict(day=day, start=m, dur=60, org=pick[0], office=office, ext=int(self.rng.integers(1, 4)),
                     att=[(x, "required", "organizer" if x == pick[0] else "accepted") for x in pick],
                     kind="client", series="", cancelled=False, subject="Client meeting")
            self.W.client.append(c)
            self.W.bookings.append(dict(day=day, office=office, room=r, halves=[], s=m, e=m + 60, kind="client",
                                        n=len(pick) + c["ext"], org=pick[0], meeting=k, series="", pattern=None,
                                        released=None))
            self.held[(r, day)].append((m, m + 60))
            G.hold(READINGS, office, r, day, m, m + 60, kind="client")
            self.W.boosts.append((office, day, m, r))
            self.log["client meetings added at a busiest moment"] += 1
        return True

    def move_client(self, b, room, s):
        """Re-time or re-room a client meeting on its own day."""
        o, day, dur = b["office"], b["day"], b["e"] - b["s"]
        self.held[(b["room"], day)].remove((b["s"], b["e"]))
        self.G.hold(READINGS, o, b["room"], day, b["s"], b["e"], -1, "client")
        b["room"], b["s"], b["e"] = room, s, s + dur
        self.W.client[b["meeting"]]["start"] = s
        self.held[(room, day)].append((s, s + dur))
        self.G.hold(READINGS, o, room, day, s, s + dur, kind="client")

    def unblock(self, office, q, runs):
        """Move client meetings in client rooms off the minutes of a meeting-room peak, so that the quarter's busiest
        moment on the meeting and client rooms is reached somewhere else."""
        moved = 0
        for day, t0, t1 in runs:
            clients = [r["room_code"] for r in world.bookable_rooms(self.W.rooms, office, day, "client")]
            for b in [b for b in self.W.bookings if b["office"] == office and b["day"] == day and b["kind"] == "client"
                      and b["room"] in clients and b["s"] < t1 and t0 < b["e"]]:
                dur, old = b["e"] - b["s"], (b["room"], b["s"])
                for s in range(9 * 60, 17 * 60 - dur + 1, 30):
                    if s < t1 and t0 < s + dur:
                        continue
                    self.held[(b["room"], day)].remove((b["s"], b["e"]))
                    rooms = [r for r in [b["room"]] + clients if self.free(r, day, s, s + dur)]
                    self.held[(b["room"], day)].append((b["s"], b["e"]))
                    if not rooms:
                        continue
                    self.move_client(b, rooms[0], s)
                    if self.G.referee_ok(office, q):
                        moved += 1
                        self.log["client meetings re-timed off a meeting-room peak"] += 1
                        break
                    self.move_client(b, *old)
        return moved

    def client_rooms_full(self):
        """C1 baseline: some client meetings were put in a free meeting room at their own time."""
        W = self.W
        for b in sorted((b for b in W.bookings if b["kind"] == "client"), key=lambda b: (b["day"], b["s"], b["room"])):
            if self.rng.random() >= CLIENT_IN_MEETING_ROOM:
                continue
            self.client_to_meeting_room(b)

    def client_to_meeting_room(self, b, keep=None):
        room = self.meeting_room_for(b["office"], b["day"], b["s"], b["e"], b["n"])
        if room is None:
            return False
        self.move_client(b, room, b["s"])
        if keep is not None and not keep <= self.G.moved_peaks():
            return "undo"
        b["in_meeting_room"] = True
        self.log["C1 client meetings in a meeting room"] += 1
        return True

    def lift_own_counts(self):
        """C1 at the threshold: client meetings in meeting rooms on the days that set the room count, until the count
        with the client meetings left in stands above the correct one at each office, and so does the legacy count."""
        W, G = self.W, self.G
        for office in (ADL, FRT):
            for _ in range(60):
                vt = G.own("true", office)
                if G.own("true", office, "ownc") != vt and G.own("legacy", office) != vt:
                    break
                v = G.own("true", office, "ownc")
                keep = G.moved_peaks()
                done = False
                for day in W.work:
                    a = G.c.get(("true", office, "ownc", day))
                    if a is None or int(a.max()) != v:
                        continue
                    clients = [r["room_code"] for r in world.bookable_rooms(W.rooms, office, day, "client")]
                    for t0, t1 in self.runs(office, "true", "ownc", day, v):
                        for b in [b for b in W.bookings if b["office"] == office and b["day"] == day
                                  and b["kind"] == "client" and b["room"] in clients and b["s"] < t1 and t0 < b["e"]]:
                            old = (b["room"], b["s"])
                            r = self.client_to_meeting_room(b, keep)
                            if r == "undo":
                                self.move_client(b, *old)
                                continue
                            if r:
                                self.log["C1 client meetings in a meeting room at the room-count threshold"] += 1
                                done = True
                                break
                        if done:
                            break
                    if done:
                        break
                if not done:
                    done = self.new_client_at_threshold(office, v, keep)
                if not done:
                    break

    def new_client_at_threshold(self, office, v, keep):
        """Where no client meeting sits on a threshold day's peak, book an ordinary client meeting into a free meeting
        room across it (the client suite full), kept only if the close-outs and the moved peaks stand."""
        W, G = self.W, self.G
        for day in W.work:
            a = G.c.get(("true", office, "ownc", day))
            if a is None or int(a.max()) != v:
                continue
            i = W.work.index(day)
            staff = [p["pid"] for p in W.people if W.pres[p["pid"], i] == office]
            for t0, t1 in self.runs(office, "true", "ownc", day, v):
                s0 = max(9 * 60, (t0 // 30) * 30)
                for st in (s0, s0 - 30):
                    room = self.meeting_room_for(office, day, st, st + 60, 3)
                    if room is None or not (st < t1 and t0 < st + 60) or len(staff) < 2:
                        continue
                    G.hold(READINGS, office, room, day, st, st + 60, kind="client")
                    if G.referee_ok(office, quarter(day)) and keep <= G.moved_peaks():
                        k = len(W.client)
                        pick = [int(x) for x in self.rng.choice(staff, 2, replace=False)]
                        c = dict(day=day, start=st, dur=60, org=pick[0], office=office, ext=int(self.rng.integers(1, 3)),
                                 att=[(x, "required", "organizer" if x == pick[0] else "accepted") for x in pick],
                                 kind="client", series="", cancelled=False, subject="Client meeting")
                        W.client.append(c)
                        W.bookings.append(dict(day=day, office=office, room=room, halves=[], s=st, e=st + 60,
                                               kind="client", n=2 + c["ext"], org=pick[0], meeting=k, series="",
                                               pattern=None, released=None, in_meeting_room=True))
                        self.held[(room, day)].append((st, st + 60))
                        self.log["C1 client meetings in a meeting room"] += 1
                        self.log["C1 client meetings in a meeting room at the room-count threshold"] += 1
                        return True
                    G.hold(READINGS, office, room, day, st, st + 60, -1, "client")
        return False

    # ------------------------------------------------------------------ S1: focus blocks in meeting rooms
    def focus_rooms(self):
        """Hold some focus blocks in a free meeting room, on days their owner was in. Each is kept only where every
        quarter's close-out still reads the same on both readings and the room count does not move when the focus
        blocks are counted in it."""
        import pack
        W, G = self.W, self.G
        W.focus_blocks = [b for b in pack.texture_blocks(W, np.random.default_rng([self.seed, 7])) if b[0] == "f"]
        for _, i, q, d, st in W.focus_blocks:
            o = int(W.pres[q, i])
            if o == 0 or self.rng.random() >= FOCUS_IN_ROOM:
                continue
            room = self.meeting_room_for(o, d, st, st + 120, 1)
            if room is None:
                continue
            G.hold(READINGS, o, room, d, st, st + 120, kind="focus")
            if not (G.referee_ok(o, quarter(d)) and G.own("true", o, "ownf") == G.own("true", o)):
                G.hold(READINGS, o, room, d, st, st + 120, -1, "focus")
                continue
            self.held[(room, d)].append((st, st + 120))
            W.bookings.append(dict(day=d, office=o, room=room, halves=[], s=st, e=st + 120, kind="focus", n=1, org=q,
                                   meeting=("f", i, q), series="", pattern=None, released=None, outlook=True))
            self.log["S1 focus blocks held in a meeting room"] += 1

    # ------------------------------------------------------------------ G1: calls with an outside party on the line
    def comb(self, scope):
        """Both offices' meeting-room bookings on one timeline (the booking rung): the thirteenth-highest daily peak."""
        vals = []
        for d in self.W.work:
            a = self.G.c.get(("true", ADL, scope, d))
            f = self.G.c.get(("true", FRT, scope, d))
            if a is None and f is None:
                vals.append(0)
                continue
            vals.append(int(((a if a is not None else 0) + (f if f is not None else 0)).max()))
        return sorted(vals, reverse=True)[RULE_DAYS]

    def guest_ok(self):
        """Reading people from the headcount must leave the booking rung where it is, and no reading of each office's
        own bookings may add up, across the two offices, to the new office's count."""
        if self.comb("owng") != self.comb_own:
            return False
        G = self.G
        sets = {o: {G.own("true", o, sc) for sc in ("own", "ownc", "owng", "owncg")} | {G.own("legacy", o)}
                for o in (ADL, FRT)}
        return all(a + f != MAIN_COUNT for a in sets[ADL] for f in sets[FRT])

    def eligible_calls(self, office, day=None):
        """Single calls booked through Outlook into a meeting room (a standing call's series is left alone)."""
        W = self.W
        return [b for b in W.bookings if b["office"] == office and b["kind"] == "solo" and b.get("outlook")
                and not b.get("guests") and not b["halves"] and not W.solo[b["meeting"]]["series"]
                and (day is None or b["day"] == day) and self.G.rtype(b["room"], b["day"]) == "meeting"]

    def guest_meta(self, targeted):
        dom = GUEST_DOMAINS[int(self.grng.integers(len(GUEST_DOMAINS)))]
        pool = GUEST_SUBJECTS + ([] if targeted else GUEST_CALL_SUBJECTS)
        return pool[int(self.grng.integers(len(pool)))], dom, (1 if self.grng.random() < 0.8 else 2)

    def convert_guest(self, b, meta, sign=1):
        """Put an outside party on a call's invite (sign 1) or take them off again (sign -1). The hold is unchanged;
        only the readings that take people from the headcount see a meeting."""
        G, o, d, s = self.G, b["office"], b["day"], b["s"]
        e_true = b["gave_back"] if b.get("gave_back") is not None else b["e"]
        old, new = ("solo", "gcall") if sign > 0 else ("gcall", "solo")
        for rd, e in (("true", e_true), ("legacy", b["e"])):
            G.hold((rd,), o, b["room"], d, s, e, -1, old)
            G.hold((rd,), o, b["room"], d, s, e, 1, new)
        so = self.W.solo[b["meeting"]]
        if sign > 0:
            subj, dom, n = meta
            b.update(guests=n, n=1 + n)
            so.update(guests=n, subject=subj, domain=dom)
        else:
            b.pop("guests", None)
            b["n"] = 1
            for k in ("guests", "subject", "domain"):
                so.pop(k, None)

    def guest_calls(self):
        """G1 baseline: a share of single Outlook calls had someone outside the firm on the line."""
        self.grng = np.random.default_rng([self.seed, 29])
        self.comb_own = self.comb("own")
        for b in sorted((b for o in (ADL, FRT) for b in self.eligible_calls(o)),
                        key=lambda b: (b["day"], b["s"], b["room"])):
            if self.grng.random() >= GUEST_CALL_RATE[b["office"]]:
                continue
            self.convert_guest(b, self.guest_meta(False))
            if self.guest_ok():
                self.log["G1 calls with an outside party on the line"] += 1
            else:
                self.convert_guest(b, None, -1)

    def threshold_runs(self, o, lvl):
        """Days whose busiest minute, people read from the headcount, sits at lvl, with the minutes it is reached."""
        out = []
        for day in self.W.work:
            a = self.G.c.get(("true", o, "owng", day))
            if a is not None and int(a.max()) == lvl:
                out.append((day, self.runs(o, "true", "owng", day, lvl)))
        return out

    def guest_convert_at(self, o, lvl):
        for day, runs in self.threshold_runs(o, lvl):
            for b in self.eligible_calls(o, day):
                e_true = b["gave_back"] if b.get("gave_back") is not None else b["e"]
                if not any(b["s"] < t1 and t0 < e_true for t0, t1 in runs):
                    continue
                self.convert_guest(b, self.guest_meta(True))
                if self.guest_ok():
                    b["g1_threshold"] = True
                    self.log["G1 calls with an outside party at the room-count threshold"] += 1
                    return True
                self.convert_guest(b, None, -1)
        return False

    def guest_add_at(self, o, lvl):
        """Book a call with an outside party into a free meeting room across a threshold day's busiest minute, kept only
        if every quarterly busiest moment (meeting rooms, and meeting and client rooms), the close-outs and the moved
        peaks stand."""
        W, G = self.W, self.G
        keep = G.moved_peaks()
        for day, runs in self.threshold_runs(o, lvl):
            q = quarter(day)
            before = {(rd, sc): G.qmax(rd, o, sc, q) for rd in READINGS for sc in ("meet", "all")}
            i = W.work.index(day)
            here = [p["pid"] for p in W.people if W.pres[p["pid"], i] == o]
            if not here:
                continue
            for t0, t1 in runs:
                for st, dur in (((t0 // 30) * 30, 30), ((t0 // 30) * 30, 60), ((t0 // 30) * 30 - 30, 60)):
                    if st < 8 * 60 + 30 or st + dur > 18 * 60:
                        continue
                    room = self.meeting_room_for(o, day, st, st + dur, 1)
                    if room is None:
                        continue
                    G.hold(READINGS, o, room, day, st, st + dur, kind="gcall")
                    after = {(rd, sc): G.qmax(rd, o, sc, q) for rd in READINGS for sc in ("meet", "all")}
                    if after == before and keep <= G.moved_peaks() and G.referee_ok(o, q) and self.guest_ok():
                        k = len(W.solo)
                        org = int(here[int(self.grng.integers(len(here)))])
                        subj, dom, n = self.guest_meta(True)
                        W.solo.append(dict(day=day, start=st, dur=dur, org=org, office=o, kind="solo", series="",
                                           pattern_start=None, outlook=True, guests=n, subject=subj, domain=dom))
                        W.bookings.append(dict(day=day, office=o, room=room, halves=[], s=st, e=st + dur, kind="solo",
                                               n=1 + n, org=org, meeting=k, series="", pattern=None, released=None,
                                               outlook=True, guests=n, g1_threshold=True, g1_booked=True))
                        self.held[(room, day)].append((st, st + dur))
                        self.log["G1 calls with an outside party booked at the room-count threshold"] += 1
                        self.log["G1 calls booked at the threshold, %s" % world.OFFICES[o]] += 1
                        return True
                    G.hold(READINGS, o, room, day, st, st + dur, -1, "gcall")
        return False

    def lift_guest_counts(self):
        """G1 at the threshold: calls with an outside party held across the busiest minute of the days that set each
        office's room count, until the count with people read from the headcount stands one above the correct one on
        GUEST_MARGIN more days than the rule needs."""
        G, W = self.G, self.W
        for o in (ADL, FRT):
            v = G.own("true", o)
            for _ in range(80):
                above = sum(1 for d in W.work if ("true", o, "owng", d) in G.c
                            and int(G.c[("true", o, "owng", d)].max()) > v)
                if above >= RULE_DAYS + 1 + GUEST_MARGIN:
                    break
                if not (self.guest_convert_at(o, v) or self.guest_add_at(o, v)):
                    break

    # ------------------------------------------------------------------ A1: give-backs at the panel
    def give_back_candidates(self):
        return [b for b in self.W.bookings if b["office"] == ADL and b["kind"] in ("meeting", "solo")
                and b["e"] - b["s"] >= 30 and all(self.G.rtype(r, b["day"]) == "meeting" for r in (b["halves"] or [b["room"]]))]

    def apply_give_back(self, b, g, sign=-1):
        for r in (b["halves"] or [b["room"]]):
            self.G.hold(("true",), ADL, r, b["day"], g, b["e"], sign, b["kind"])

    def give_backs(self):
        for b in sorted(self.give_back_candidates(), key=lambda b: (b["day"], b["s"], b["room"])):
            if self.rng.random() >= GIVE_BACK_RATE[b["kind"]]:
                continue
            g = int(self.rng.integers(b["s"] + 10 if b["kind"] == "solo" else b["s"] + 12, b["e"] - 4))
            if self.try_change(ADL, b["day"], lambda: self.apply_give_back(b, g), lambda: self.apply_give_back(b, g, 1)):
                b["gave_back"] = g
                self.log["A1 give-backs"] += 1

    def target_give_backs(self, q):
        """Give back, before each minute the true meeting-room peak is reached, one booking held across it, a combined
        booking from before the upgrade first where one is held there."""
        if self._give_back_runs(q):
            return
        lvl, _ = self.G.qmax("true", ADL, "meet", q)
        if self.unblock(ADL, q, self.qruns(ADL, "true", q, lvl)):
            self._give_back_runs(q)

    def _give_back_runs(self, q):
        G = self.G
        if G.peak_moved(ADL, q):
            return True
        lvl, _ = G.qmax("true", ADL, "meet", q)
        runs = self.qruns(ADL, "true", q, lvl)
        cands = self.give_back_candidates()
        done = []
        for day, t0, t1 in runs:
            taken = {id(x) for x, _ in done}
            pool = [b for b in cands if b["day"] == day and "gave_back" not in b and id(b) not in taken
                    and b["s"] + 12 <= t0 and b["e"] >= t1]
            if not pool:
                break
            pre = [b for b in pool if b["halves"] and not b.get("one_row")]
            b = (pre or pool)[int(self.rng.integers(len(pre or pool)))]
            g = int(self.rng.integers(max(b["s"] + 12, t0 - 20), t0 + 1))
            self.apply_give_back(b, g)
            done.append((b, g))
        if len(done) == len(runs) and G.peak_moved(ADL, q):
            if not G.referee_ok(ADL, q):
                lv, by = G.qmax("legacy", ADL, "all", q)
                self.boost(ADL, q, lv, by)
            if G.referee_ok(ADL, q):
                for b, g in done:
                    b["gave_back"] = g
                    self.log["A1 give-backs at a meeting-room peak" + (" (combined)" if b["halves"] else "")] += 1
                return True
        for b, g in done:
            self.apply_give_back(b, g, 1)
        return False

    # ------------------------------------------------------------------ Front Street series rows
    def add_ghost(self, gh, kind):
        def apply():
            self.G.hold(("legacy",), FRT, gh["room"], gh["day"], gh["s"], gh["e"], kind=kind)

        def undo():
            self.G.hold(("legacy",), FRT, gh["room"], gh["day"], gh["s"], gh["e"], -1, kind)
        ok = self.try_change(FRT, gh["day"], apply, undo) if gh["legacy_keeps"] else True
        if ok:
            gh["kind"] = kind
            self.W.ghosts.append(gh)
            self.ghost_held[(gh["room"], gh["day"])].append((gh["s"], gh["e"]))
        return ok

    def drop_ghost(self, gh):
        self.W.ghosts.remove(gh)
        self.ghost_held[(gh["room"], gh["day"])].remove((gh["s"], gh["e"]))
        if gh["legacy_keeps"]:
            self.G.hold(("legacy",), FRT, gh["room"], gh["day"], gh["s"], gh["e"], -1, gh["kind"])

    def moved_ghosts(self, usual):
        for b in sorted((b for b in self.W.bookings if b["office"] == FRT and b["kind"] in ("meeting", "solo")
                         and b["pattern"] is not None), key=lambda b: (b["day"], b["s"], b["room"])):
            ps, pe = b["pattern"], b["pattern"] + b["e"] - b["s"]
            u = usual.get(b["series"])
            for room in ([u] if u else []) + [b["room"]]:
                if room and self.free(room, b["day"], ps, pe):
                    gh = dict(day=b["day"], room=room, s=ps, e=pe, src=b, why="moved", legacy_keeps=(room != b["room"]))
                    if self.add_ghost(gh, b["kind"]):
                        self.log["F2 moved-occurrence rows in another room" if gh["legacy_keeps"]
                                 else "moved-occurrence rows in the same room"] += 1
                        break

    def cancelled_ghosts(self, usual):
        for b in sorted((b for b in self.W.bookings if b["office"] == FRT and b["kind"] == "cancelled" and b["series"]),
                        key=lambda b: (b["day"], b["s"], b["room"])):
            u = usual.get(b["series"])
            if not u:
                continue
            b["room"] = u                                   # the cancelled exception names the series' room
            if self.free(u, b["day"], b["s"], b["e"]):
                gh = dict(day=b["day"], room=u, s=b["s"], e=b["e"], src=b, why="cancelled", legacy_keeps=True)
                if self.add_ghost(gh, "meeting"):
                    self.log["F1 cancelled-occurrence rows (meetings)"] += 1

    def standing_cancellations(self, usual):
        W = self.W
        done = {(c["sid"], c["day"]) for c in W.standing_cancelled}
        for sid in sorted(W.standing):
            sp = W.standing[sid]
            q = sp["org"]
            p = W.people[q]
            u = usual.get(sid)
            for i, day in enumerate(W.work):
                if W.wd[i] != sp["dow"] or W.pres[q, i] == FRT or not world.employed(p, day) or (sid, day) in done:
                    continue
                if self.rng.random() >= STANDING_CANCEL_RATE:
                    continue
                s, e = sp["start"], sp["start"] + 30
                c = dict(sid=sid, org=q, day=day, s=s, e=e, room=u, ghost=False)
                W.standing_cancelled.append(c)
                if u and self.free(u, day, s, e):
                    gh = dict(day=day, room=u, s=s, e=e, src=c, why="standing", legacy_keeps=True)
                    if self.add_ghost(gh, "solo"):
                        c["ghost"] = True
                        self.log["F1 cancelled-occurrence rows (standing calls)"] += 1

    def move_call(self, b, s2, r2, sign=1):
        """Move a standing call's occurrence to a later slot in another room; its series row stays at the old slot."""
        G, day = self.G, b["day"]
        if sign > 0:
            old_room, s, e = b["room"], b["s"], b["e"]
            self.held[(old_room, day)].remove((s, e))
            self.held[(r2, day)].append((s2, s2 + 30))
            G.hold(("true",), FRT, old_room, day, s, e, -1, "solo")
            G.hold(READINGS, FRT, r2, day, s2, s2 + 30, kind="solo")
            b.update(room=r2, s=s2, e=s2 + 30, pattern=s, moved_from=old_room)
            self.W.solo[b["meeting"]].update(start=s2, pattern_start=s)
            gh = dict(day=day, room=old_room, s=s, e=e, src=b, why="moved", legacy_keeps=True, kind="solo")
            self.W.ghosts.append(gh)
            self.ghost_held[(old_room, day)].append((s, e))
            return gh
        old_room, s = b["moved_from"], b["pattern"]
        e = s + 30
        self.held[(b["room"], day)].remove((b["s"], b["e"]))
        self.held[(old_room, day)].append((s, e))
        G.hold(READINGS, FRT, b["room"], day, b["s"], b["e"], -1, "solo")
        G.hold(("true",), FRT, old_room, day, s, e, kind="solo")
        self.W.solo[b["meeting"]].update(start=s, pattern_start=None)
        b.update(room=old_room, s=s, e=e, pattern=None)
        del b["moved_from"]
        gh = next(g for g in self.W.ghosts if g["src"] is b)
        self.W.ghosts.remove(gh)
        self.ghost_held[(old_room, day)].remove((s, e))

    def standing_moves(self):
        """F2 at a baseline: some standing-call occurrences moved later that day into another room, each leaving its
        series row at the old slot."""
        W, G = self.W, self.G
        for b in sorted((b for b in W.bookings if b["office"] == FRT and b["kind"] == "solo" and b["series"] in W.standing
                         and b["pattern"] is None), key=lambda b: (b["day"], b["s"], b["room"])):
            if self.rng.random() >= STANDING_MOVE_RATE:
                continue
            for shift in (180, 210, 240):
                s2 = b["s"] + shift
                if s2 + 30 > 18 * 60:
                    continue
                r2 = self.meeting_room_for(FRT, b["day"], s2, s2 + 30, 1, exclude=(b["room"],))
                if r2:
                    self.move_call(b, s2, r2)
                    if G.referee_ok(FRT, quarter(b["day"])):
                        self.log["F2 standing calls moved later into another room"] += 1
                    else:
                        self.move_call(b, None, None, sign=-1)
                    break

    def target_moves(self, q):
        """Lower the true meeting-room peak by one: at each minute it is reached, a standing call held across that
        minute moved later that day into another room, leaving its series row behind."""
        G, W = self.G, self.W
        if G.peak_moved(FRT, q):
            return
        lvl, _ = G.qmax("true", FRT, "meet", q)
        runs = self.qruns(FRT, "true", q, lvl)
        done = []
        for day, t0, t1 in runs:
            pool = [b for b in W.bookings if b["office"] == FRT and b["kind"] == "solo" and b["day"] == day
                    and b["series"] in W.standing and b["pattern"] is None and b["s"] <= t0 and b["e"] >= t1
                    and all(x is not b for x, _ in done)]
            moved = None
            for b in pool:
                for shift in (180, 210, 240):
                    s2 = b["s"] + shift
                    if s2 + 30 > 18 * 60:
                        continue
                    r2 = self.meeting_room_for(FRT, day, s2, s2 + 30, 1, exclude=(b["room"],))
                    if r2:
                        moved = (b, self.move_call(b, s2, r2))
                        break
                if moved:
                    break
            if not moved:
                break
            done.append(moved)
        if len(done) == len(runs) and G.peak_moved(FRT, q):
            if not G.referee_ok(FRT, q):
                self.unblock(FRT, q, runs)
            if not G.referee_ok(FRT, q):
                lv, by = G.qmax("legacy", FRT, "all", q)
                self.boost(FRT, q, lv, by)
            if G.referee_ok(FRT, q) and G.peak_moved(FRT, q):
                self.log["F2 standing calls moved off a meeting-room peak"] += len(done)
                return
        for b, gh in reversed(done):
            self.move_call(b, None, None, sign=-1)

    def target_ghosts(self, q, usual, against="legacy"):
        """Put the series rows of standing calls cancelled on a day their owners were out into one slot, until the
        reading named by `against` (plus these rows) passes the true meeting-room peak, in a slot with room under the
        quarter's busiest moment. Against the legacy reading it moves the peak; against the true reading it makes the
        peak wrong for a fold that crosses rooms but filters cancelled rows first."""
        G, W = self.G, self.W
        if against == "legacy" and G.peak_moved(FRT, q):
            return
        lvl, _ = G.qmax("true", FRT, "meet", q)
        done = {(c["sid"], c["day"]) for c in W.standing_cancelled}
        cands = []
        for day in G.qdays[q]:
            i = W.work.index(day)
            ref = G.c.get((against, FRT, "meet", day))
            if ref is None:
                continue
            for st in sorted({sp["start"] for sp in W.standing.values()}):
                k = lvl + 1 - int(ref[st:st + 30].max())
                if not 1 <= k <= (3 if against == "legacy" else 1):
                    continue
                src, rooms = [], set()
                for sid in sorted(W.standing):
                    sp = W.standing[sid]
                    if (sp["start"] != st or W.wd[i] != sp["dow"] or W.pres[sp["org"], i] == FRT or (sid, day) in done
                            or not world.employed(W.people[sp["org"]], day)):
                        continue
                    u = next((r for r in self.series_rooms.get(sid, []) if r not in rooms
                              and self.free(r, day, st, st + 30)), None)
                    if u is None:
                        continue
                    src.append((sid, u))
                    rooms.add(u)
                if len(src) >= k:
                    cands.append((k, day, st, src[:k]))
        keep = G.moved_peaks()
        for k, day, st, src in sorted(cands, key=lambda x: (x[0], x[1], x[2])):
            top, top_day = G.qmax("true", FRT, "all", q)
            la = G.c[("legacy", FRT, "all", day)]
            if int(la[st:st + 30].max()) + k > top - (1 if day < top_day else 0):
                self.unblock(FRT, q, [(day, st, st + 30)])
                top, top_day = G.qmax("true", FRT, "all", q)
                need = int(la[st:st + 30].max()) + k
                if need > top - (1 if day < top_day else 0):
                    self.boost(FRT, q, need, day)
            added = []
            for sid, u in src:
                sp = W.standing[sid]
                if not self.free(u, day, st, st + 30):
                    break
                c = dict(sid=sid, org=sp["org"], day=day, s=st, e=st + 30, room=u, ghost=True)
                gh = dict(day=day, room=u, s=st, e=st + 30, src=c, why="standing", legacy_keeps=True)
                if not self.add_ghost(gh, "solo"):
                    break
                added.append((c, gh))
            ok = len(added) == k and keep <= G.moved_peaks()
            if against == "legacy":
                ok = ok and G.peak_moved(FRT, q)
            if ok:
                for c, gh in added:
                    W.standing_cancelled.append(c)
                    self.log["F1 cancelled standing calls at a meeting-room peak" if against == "legacy"
                             else "F1 cancelled standing calls at the true peak"] += 1
                return
            for c, gh in added:
                self.drop_ghost(gh)

    # ------------------------------------------------------------------ the whole plan
    def run(self):
        self.base()
        self.upgrade()
        self.focus_rooms()
        self.client_rooms_full()
        self.give_backs()
        for q, _, _ in QUARTERS:
            self.target_give_backs(q)
        usual = self.usual_rooms()
        self.moved_ghosts(usual)
        self.cancelled_ghosts(usual)
        self.standing_moves()
        for q, _, _ in QUARTERS:
            self.target_moves(q)
            self.target_ghosts(q, usual)
            if self.G.peak_moved(FRT, q):
                self.target_ghosts(q, usual, against="true")
        self.standing_cancellations(usual)
        self.lift_own_counts()
        self.guest_calls()
        self.lift_guest_counts()
        for o in (ADL, FRT):
            for q, _, _ in QUARTERS:
                assert self.G.referee_ok(o, q), ("close-out busiest moment differs between readings", o, q)
        return self


def plan(W, seed=114):
    P = Planner(W, seed).run()
    W.device_log = dict(P.log)
    W.device_grid = P.G
    return P
