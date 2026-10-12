"""Room bookings. Each office's platform books a room for a meeting when two or more of its non-declined
internal invitees are in that office that day; client meetings take a client room, town halls the event
space, and some people book a room alone for a call. This module assigns rooms and produces the rows each
platform exports, including the behaviours of each platform that a careless read gets wrong.
"""
import datetime as dt
from collections import defaultdict

from world import CLOSURE, HOLIDAYS, OFFICES, D, T, employed

ADL, FRT = 1, 2


def iso_minutes(day, minutes):
    return T(day.year, day.month, day.day) + dt.timedelta(minutes=int(minutes))


class Rooms:
    """Per office and day, which physical rooms are held when."""

    def __init__(self, R):
        self.R = R
        self.held = defaultdict(list)  # (code, day) -> [(s, e)]

    def free(self, code, day, s, e):
        return all(e <= a or b <= s for a, b in self.held[(code, day)])

    def hold(self, code, day, s, e):
        self.held[(code, day)].append((s, e))

    def candidates(self, office, day, rtype):
        out = []
        for r in self.R:
            if r["office"] != OFFICES[office] or r["room_type"] != rtype:
                continue
            if r["valid_from"] <= day and (r["valid_to"] is None or day <= r["valid_to"]):
                out.append(r)
        return sorted(out, key=lambda r: (r["seats"], r["room_code"]))

    def pick(self, office, day, s, e, n, rtype, rng=None):
        """Smallest free room of the type with seats for n; combined rooms only when no single room fits."""
        singles = [r for r in self.candidates(office, day, rtype) if "+" not in r["room_code"]]
        fit = [r for r in singles if r["seats"] >= n and self.free(r["room_code"], day, s, e)]
        if fit:
            best = fit[0]["seats"]
            same = [r for r in fit if r["seats"] == best]
            r = same[0] if rng is None else same[int(rng.integers(len(same)))]
            self.hold(r["room_code"], day, s, e)
            return r["room_code"], []
        for r in self.candidates(office, day, rtype):
            if "+" not in r["room_code"] or r["seats"] < n:
                continue
            halves = r["combinable_with"].split(";")
            if all(self.free(h, day, s, e) for h in halves):
                for h in halves:
                    self.hold(h, day, s, e)
                return r["room_code"], halves
        return None, []


def counts(W, m, i):
    """Non-declined internal invitees present in each office that day."""
    na = nb = 0
    for q, typ, resp in m["att"]:
        if resp == "declined":
            continue
        o = W.pres[q, i]
        if o == ADL:
            na += 1
        elif o == FRT:
            nb += 1
    return na, nb


def build(W, rng):
    di = {d: i for i, d in enumerate(W.work)}
    rooms = Rooms(W.rooms)
    bookings = []  # one per platform row before export formatting
    moved_ghost_candidates = []
    # requests per day, assigned in start order with bigger meetings first at a tie
    req = defaultdict(list)
    for k, m in enumerate(W.meetings):
        i = di[m["day"]]
        na, nb = counts(W, m, i)
        m["na"], m["nb"] = na, nb
        if m["cancelled"]:
            # the organiser had booked; the platform keeps the cancelled row
            home = W.people[m["org"]]["office"]
            req[m["day"]].append((m["start"], -2, "cancelled", k, home, 2))
            continue
        if na >= 2:
            req[m["day"]].append((m["start"], -na, "meeting", k, ADL, na))
        if nb >= 2:
            req[m["day"]].append((m["start"], -nb, "meeting", k, FRT, nb))
        # Adelaide organisers book ahead; when fewer than two turn up the platform releases the room
        org = W.people[m["org"]]
        if org["office"] == ADL and na < 2 and m["kind"] in ("team", "work", "prog") and m["noshow_draw"] < 0.35:
            exp = sum(1 for q, typ, resp in m["att"] if resp != "declined" and W.people[q]["office"] == ADL)
            if exp >= 2 and W.pres[m["org"], i] != FRT:
                req[m["day"]].append((m["start"], -exp, "noshow", k, ADL, exp))
    for k, c in enumerate(W.client):
        req[c["day"]].append((c["start"], -(len(c["att"]) + c["ext"]), "client", k, c["office"],
                              len(c["att"]) + c["ext"]))
    for k, e in enumerate(W.events):
        for office in (ADL, FRT):
            req[e["day"]].append((e["start"], -100, "townhall", k, office, 60))
    for k, s in enumerate(W.solo):
        req[s["day"]].append((s["start"], -1, "solo", k, s["office"], 1))
    fails = []
    for day in W.work:
        for st, negn, kind, k, office, n in sorted(req[day], key=lambda x: (x[0], x[1], x[2], x[3], x[4])):
            if kind in ("meeting", "noshow", "cancelled"):
                m = W.meetings[k]
                s, e = m["start"], m["start"] + m["dur"]
                held_until = s + 15 if kind == "noshow" else e
                if kind == "cancelled":
                    code, halves = _peek(rooms, office, day, s, e, n)
                else:
                    code, halves = rooms.pick(office, day, s, held_until, n, "meeting", rng)
                if code is None:
                    fails.append((day, kind, office, n, s))
                    continue
                bookings.append(dict(day=day, office=office, room=code, halves=halves, s=s, e=e, kind=kind,
                                     n=n, org=m["org"], meeting=k, series=m["series"],
                                     pattern=m.get("pattern_start"), released=(s + 15 if kind == "noshow" else None)))
            elif kind == "client":
                c = W.client[k]
                code = None
                for shift in [0, 30, -30, 60, -60, 90, -90, 120, -120, 150, -150, 180, -180, 240, -240]:
                    s, e = c["start"] + shift, c["start"] + shift + c["dur"]
                    if s < 8 * 60 or e > 18 * 60 + 30:
                        continue
                    code, halves = rooms.pick(office, day, s, e, n, "client", rng)
                    if code is not None:
                        c["start"] = s
                        break
                if code is None:
                    fails.append((day, kind, office, n, c["start"]))
                    continue
                bookings.append(dict(day=day, office=office, room=code, halves=[], s=s, e=e, kind="client", n=n,
                                     org=c["org"], meeting=k, series="", pattern=None, released=None))
            elif kind == "townhall":
                ev = W.events[k]
                s, e = ev["start"], ev["start"] + ev["dur"]
                code = "AD-1.00" if office == ADL else "FR-3.00"
                rooms.hold(code, day, s, e)
                bookings.append(dict(day=day, office=office, room=code, halves=[], s=s, e=e, kind="townhall",
                                     n=0, org=ev["org"], meeting=k, series="", pattern=None, released=None))
            else:
                so = W.solo[k]
                s, e = so["start"], so["start"] + so["dur"]
                code, halves = rooms.pick(office, day, s, e, 1, "meeting", rng)
                if code is None:
                    continue  # nothing free: the call is taken at a desk
                bookings.append(dict(day=day, office=office, room=code, halves=[], s=s, e=e, kind="solo", n=1,
                                     org=so["org"], meeting=k, series=so["series"], pattern=so["pattern_start"],
                                     released=None, outlook=so["outlook"]))
    W.bookings = bookings
    W.book_fails = fails
    W.rooms_held = rooms
    return bookings


def _peek(rooms, office, day, s, e, n):
    """A cancelled booking named a room without holding it."""
    singles = [r for r in rooms.candidates(office, day, "meeting") if "+" not in r["room_code"] and r["seats"] >= n]
    return (singles[0]["room_code"] if singles else None), []
