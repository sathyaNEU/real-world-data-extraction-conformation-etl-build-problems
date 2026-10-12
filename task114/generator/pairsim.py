"""Part 8 audit for the ask layer: which of Ask A's criteria a solver files right, by the conventions it reads.

The generated rubric grades each office's four quarters as one criterion per measure (hours, call hours, busiest
moment), then rooms on 30 September and the room count its own bookings justify. Portal weights read off the rubric:
room count 7, hours 4, call hours 4; busiest moment and rooms on 30 September are taken at 4 until a rubric shows them.
The legacy reading is the convention set the portal's first top responses filed: release keyed on status, combined rows
dropped with their half rows kept, cancelled rows filtered before the series rows are folded, the fold keyed on the
room, client meetings in meeting rooms left in the room count, people read from the headcount, and every one-person
booking read as a call. Each other profile fixes one family or more.

    python3 pairsim.py
"""
import json
from pathlib import Path

import pandas as pd

import golden as G

WEIGHTS = {"hours": 4, "solo_hours": 4, "peak": 4, "rooms_30_sep": 4, "own_rule": 7}
QS = ("Q1", "Q2", "Q3", "Q4")
TOTAL = 2 * sum(WEIGHTS.values())


def figures(L, ah, fh, client_out):
    return {"A": G.office_figures(L, ah, "A", client_out=client_out),
            "F": G.office_figures(L, fh, "F", client_out=client_out)}


def passed(v, base):
    out = []
    for o in ("A", "F"):
        for k in ("hours", "solo_hours", "peak"):
            if all(v[o][q][k] == base[o][q][k] for q in QS):
                out.append("%s %s" % (o, k))
        for k in ("rooms_30_sep", "own_rule"):
            if v[o][k] == base[o][k]:
                out.append("%s %s" % (o, k))
    return out


def points(v, base):
    return sum(WEIGHTS[c.split(" ", 1)[1]] for c in passed(v, base))


def by_subject(L, H, office, pattern):
    """People read from the headcount, but an item whose subject matches pattern also taken as one person's call."""
    ev = L["events"]
    H = H.copy()
    if office == "A":
        subj = H.outlook_event_id.map(dict(zip(ev.event_id, ev.subject))).fillna("")
        base = H.headcount == "1"
        focus = H.outlook_event_id.isin(L["focus_eid"])
    else:
        subj = H.ical_uid.map(dict(zip(ev.ical_uid, ev.subject))).fillna("")
        base = H.attendee_count.astype(int) == 2
        focus = H.ical_uid.isin(L["focus_uid"])
    H["one"] = base | subj.str.contains(pattern, case=False, regex=True)
    H["solo"] = H["one"] & ~focus
    return H


def profiles(L):
    LA, LF = G.legacy_adelaide_holds(L), G.legacy_front_holds(L)
    A, F = G.adelaide_holds(L), G.front_holds(L)
    Ah, Fh = G.adelaide_holds(L, solo_reading="headcount"), G.front_holds(L, solo_reading="room_included")
    Af, Ff = G.adelaide_holds(L, focus_as_call=True), G.front_holds(L, focus_as_call=True)
    Fhf = G.front_holds(L, solo_reading="room_included", fold="room_key")
    return {
        "every representation device handled, focus blocks read as calls, client meetings kept": figures(L, Af, Ff, False),
        "everything handled but the focus blocks": figures(L, Af, Ff, True),
        "legacy (the portal's first conventions)": figures(L, LA, LF, False),
        "legacy, give-backs read": figures(L, G.adelaide_holds(L, shadows="drop_combined", solo_reading="headcount"), LF,
                                           False),
        "legacy, combined bookings expanded": figures(L, G.adelaide_holds(L, released="status", solo_reading="headcount"),
                                                      LF, False),
        "legacy, fold over every status": figures(L, LA, G.front_holds(L, fold="room_key", solo_reading="room_included"),
                                                  False),
        "legacy, fold across rooms": figures(L, LA, G.front_holds(L, fold="status_first", solo_reading="room_included"),
                                             False),
        "legacy, client meetings out of the room count": figures(L, LA, LF, True),
        "every Adelaide device handled": figures(L, A, LF, True),
        "every Front Street device handled": figures(L, LA, F, True),
        "everything handled but the client meetings": figures(L, A, F, False),
        "everything handled but the calls with an outside party": figures(L, Ah, Fh, True),
        "everything handled, calls told by a subject that is Call": figures(
            L, by_subject(L, Ah, "A", r"^Call$"), by_subject(L, Fh, "F", r"^Call$"), True),
        "everything handled, calls told by a subject that says call": figures(
            L, by_subject(L, Ah, "A", "call"), by_subject(L, Fh, "F", "call"), True),
        "portal run 3 (Adelaide right, Front Street fold keyed on the room, people from the headcount)": figures(
            L, Ah, Fhf, True),
        "portal run 3, the one-person rule read right": figures(L, A, G.front_holds(L, fold="room_key"), True),
        "everything handled": figures(L, A, F, True),
    }


def run(T):
    L = G.load(T)
    pr = profiles(L)
    base = pr["everything handled"]
    return {k: {"points": points(v, base), "of": TOTAL, "passed": passed(v, base)} for k, v in pr.items()}


if __name__ == "__main__":
    print(json.dumps(run(Path(__file__).resolve().parent.parent / "target"), indent=1))
