"""Fenmoor Rail Operating Centre (the Wyvern route): the network each workstation controls, the display data's
button positions, the ARS sub-areas, the signallers and the calendar. Everything here is the clean truth; the
pack writers in pack.py apply the systems' own conventions."""
import datetime as dt
import math

import numpy as np

SEED = 399
ORG = "Wyvern Route"
ROC = "Fenmoor Rail Operating Centre"

WINDOW_START = dt.date(2025, 10, 1)
WINDOW_END = dt.date(2026, 9, 30)
SIM_START = dt.date(2025, 4, 1)          # the FY2025/26 register opens on 1 April 2025
SIM_END = dt.date(2026, 9, 30)
TT_CHANGE = dt.date(2025, 12, 14)        # the December 2025 timetable
RELEASE_A = dt.datetime(2026, 3, 17, 2, 14, 0)   # UTC: server A takes control system release 8.2
RELEASE_B = dt.datetime(2026, 4, 7, 2, 31, 0)    # UTC: server B takes it three weeks later
EXPORT_DATE = dt.date(2026, 10, 9)

# workstation number, desk name, signal prefix, relative traffic
WORKSTATIONS = [("W01", "FENMOOR", "FM", 1.10), ("W02", "CALLOWBY", "CY", 0.85), ("W03", "HATHERBY", "HT", 1.45),
                ("W04", "TOLLINGHURST", "TL", 0.95), ("W05", "KESTROW", "KW", 0.80), ("W06", "WELLANBY", "WL", 0.90)]
WS_IDS = [w[0] for w in WORKSTATIONS]
DESK = {w[0]: w[1] for w in WORKSTATIONS}
PREFIX = {w[0]: w[2] for w in WORKSTATIONS}
TRAFFIC = {w[0]: w[3] for w in WORKSTATIONS}

JUNCTIONS = {
    "W01": ["Fenmoor North Jn", "Fenmoor station", "Fenmoor South Jn", "Brackle Lane Jn", "Fenmoor Up Sidings"],
    "W02": ["Callowby Jn", "Callowby station", "Pellow Loop", "Ingham Road Jn"],
    "W03": ["Hatherby West Jn", "Hatherby station", "Hatherby East Jn", "Sowley Jn", "Hatherby Down Loop"],
    "W04": ["Tollinghurst Jn", "Tollinghurst station", "Marrick Lane", "Coldharbour Jn"],
    "W05": ["Kestrow Jn", "Kestrow Yard", "Kestrow station", "Thornbury Lane"],
    "W06": ["Wellanby Jn", "Wellanby station", "Sellack Loop", "Ravenhurst Jn"],
}
SUBAREAS = {"W01": ["FM-A", "FM-B", "FM-C"], "W02": ["CY-A", "CY-B"], "W03": ["HT-A", "HT-B", "HT-C"],
            "W04": ["TL-A", "TL-B"], "W05": ["KW-A", "KW-B"], "W06": ["WL-A", "WL-B", "WL-C"]}
# the sub-area codes the control system carried before release 8.2
OLD_SUBAREA = {"FM-A": "FENM N", "FM-B": "FENM C", "FM-C": "FENM S", "CY-A": "CALL 1", "CY-B": "CALL 2",
               "HT-A": "HATH W", "HT-B": "HATH C", "HT-C": "HATH E", "TL-A": "TOLL 1", "TL-B": "TOLL 2",
               "KW-A": "KEST 1", "KW-B": "KEST 2", "WL-A": "WELL 1", "WL-B": "WELL 2", "WL-C": "WELL 3"}

SCREEN_W, SCREEN_H = 1920, 1200
CLOSE_MAX, FAR_MIN = 12.0, 36.0      # the display's two populations of exit spacing (asserted, never filed)


def rng(k):
    return np.random.default_rng(SEED * 1000 + k)


def _signal_numbers(r, n, base):
    """Signal numbers rise along the line with gaps, odd on the down lines and even on the up."""
    nums, cur = [], base + int(r.integers(1, 9))
    for _ in range(n):
        cur += int(r.choice([2, 2, 2, 4, 4, 6, 8, 10, 12]))
        nums.append(cur)
    return nums


def _screen_tracks(r, squeezed):
    """The running lines drawn across one screen, top to bottom; with `squeezed`, one line added later and drawn
    between two others, eight to eleven pixels from its upper neighbour."""
    ys = []
    y = float(r.uniform(170, 236))
    while y < 1050 and len(ys) < 10:
        ys.append(y)
        y += float(r.uniform(56, 96))
    pair = None
    if squeezed and len(ys) >= 3:
        k = int(r.integers(0, len(ys) - 1))
        ys.insert(k + 1, ys[k] + float(r.uniform(8.3, 10.6)))
        pair = (k, k + 1)
    return ys, pair


def build_network():
    """Signals, routes and the display's drawing per workstation.

    Each screen draws its running lines as horizontal tracks; an entrance's exits stand at one location on
    parallel tracks, so two exits are as far apart on the screen as their tracks. On a few screens of every
    workstation one line was added later and squeezed in eight to eleven pixels from its neighbour, and every
    entrance whose exits include both of those lines has two exits drawn that close. Nothing in the export
    marks which."""
    r = rng(1)
    signals, routes, tracks = {}, [], []
    close_pairs = []
    for wi, (ws, desk, pre, traffic) in enumerate(WORKSTATIONS):
        jn_list = JUNCTIONS[ws]
        sub = SUBAREAS[ws]
        n_ent_multi = int(r.integers(24, 31))
        n_ent_plain = int(r.integers(26, 36))
        need = 5 * n_ent_multi + 2 * n_ent_plain + 10
        nums = [int(v) for v in r.choice(np.arange(101, 999), size=need, replace=False)]
        used = set()

        def take():
            for k in nums:
                if k not in used:
                    used.add(k)
                    return k
            raise RuntimeError("out of signal numbers")

        sq = [bool(r.random() < 0.5) for _ in range(4)]
        if not any(sq):
            sq[int(r.integers(0, 4))] = True
        scr = {s + 1: _screen_tracks(r, sq[s]) for s in range(4)}
        for s, (ys, pair) in scr.items():
            for k, y in enumerate(ys):
                x1 = float(r.uniform(96, 160)) if not (pair and k == pair[1]) else float(r.uniform(420, 760))
                x2 = float(r.uniform(1760, 1830)) if not (pair and k == pair[1]) else float(r.uniform(1180, 1560))
                tracks.append(dict(ws=ws, screen=s, x1=round(x1), y1=round(y), x2=round(x2), y2=round(y)))
        squeezed_screens = [s for s in scr if scr[s][1]]
        n_close = int(r.integers(5, 7)) + (5 if ws == "W03" else 0)   # Hatherby's screens took the most additions
        close_slots = set(r.choice(n_ent_multi, size=n_close, replace=False).tolist())
        for e in range(n_ent_multi):
            jn = jn_list[e % len(jn_list)] if r.random() < 0.7 else jn_list[int(r.integers(0, len(jn_list)))]
            close = e in close_slots
            if close:
                screen = squeezed_screens[int(r.integers(0, len(squeezed_screens)))]
            else:
                screen = int(r.integers(1, 5))
            ys, pair = scr[screen]
            nex = int(r.choice([2, 2, 2, 3, 3, 4]))
            ent = "%s%d" % (pre, take())
            ex_ids = ["%s%d" % (pre, take()) for _ in range(nex)]
            if close:
                x_e = float(r.uniform(pair and 470 or 200, 1180))
                chosen = [pair[0], pair[1]]
                rest = [k for k in range(len(ys)) if k not in pair and abs(k - pair[0]) <= 3]
                r.shuffle(rest)
                chosen += rest[:nex - 2]
                t_e = chosen[int(r.integers(0, len(chosen)))]
            else:
                x_e = float(r.uniform(150, 1450))
                t_e = int(r.integers(0, len(ys)))
                while pair and t_e == pair[1]:
                    t_e = int(r.integers(0, len(ys)))
                cand = [k for k in range(len(ys)) if abs(k - t_e) <= 3]
                r.shuffle(cand)
                chosen = []
                for k in cand:
                    if pair and k == pair[1]:
                        continue
                    chosen.append(k)
                    if len(chosen) == nex:
                        break
                nex = len(chosen)
                ex_ids = ex_ids[:nex]
                if nex < 2:
                    chosen.append([k for k in range(len(ys)) if k not in chosen and not (pair and k in pair)][0])
                    ex_ids.append("%s%d" % (pre, take()))
                    nex = 2
            sa = sub[int(r.integers(0, len(sub)))]
            signals[ent] = dict(ws=ws, screen=screen, x=round(x_e), y=round(ys[t_e]), junction=jn, subarea=sa)
            x_x = x_e + float(r.uniform(130, 330))
            for k, tk in enumerate(chosen):
                jit = float(r.uniform(-2.0, 2.0))
                signals[ex_ids[k]] = dict(ws=ws, screen=screen, x=round(x_x + jit), y=round(ys[tk]), junction=jn,
                                          subarea=sa)
                if tk != t_e:
                    tracks.append(dict(ws=ws, screen=screen, x1=round(x_e + 24), y1=round(ys[t_e]),
                                       x2=round(x_x - 30), y2=round(ys[tk])))
            if close:
                close_pairs.append((ent, ex_ids[0], ex_ids[1]))
            letters = list("ABCD")[:nex]
            r.shuffle(letters)
            for k in range(nex):
                routes.append(dict(route_id="%s%s" % (ent, letters[k]), ws=ws, entrance=ent, exit=ex_ids[k],
                                   junction=jn, multi=True, close=close and k in (0, 1)))
        for e in range(n_ent_plain):
            jn = jn_list[int(r.integers(0, len(jn_list)))]
            screen = int(r.integers(1, 5))
            ys, pair = scr[screen]
            t = int(r.integers(0, len(ys)))
            while pair and t == pair[1]:
                t = int(r.integers(0, len(ys)))
            ent = "%s%d" % (pre, take())
            ex = "%s%d" % (pre, take())
            x0 = float(r.uniform(150, 1500))
            sa = sub[int(r.integers(0, len(sub)))]
            signals[ent] = dict(ws=ws, screen=screen, x=round(x0), y=round(ys[t]), junction=jn, subarea=sa)
            signals[ex] = dict(ws=ws, screen=screen, x=round(x0 + float(r.uniform(110, 330))), y=round(ys[t]),
                               junction=jn, subarea=sa)
            routes.append(dict(route_id="%s%s" % (ent, "A" if r.random() < 0.85 else "M"), ws=ws, entrance=ent,
                               exit=ex, junction=jn, multi=False, close=False))
    # nearest-neighbour separation among exits of one entrance, measured on the rounded positions
    by_ent = {}
    for rt in routes:
        by_ent.setdefault(rt["entrance"], []).append(rt)
    for ent, rts in by_ent.items():
        for rt in rts:
            others = [o for o in rts if o is not rt]
            if not others:
                rt["sep"] = None
                continue
            a = signals[rt["exit"]]
            rt["sep"] = min(math.hypot(a["x"] - signals[o["exit"]]["x"], a["y"] - signals[o["exit"]]["y"])
                            for o in others)
            rt["neighbour"] = min(others, key=lambda o: math.hypot(a["x"] - signals[o["exit"]]["x"],
                                                                   a["y"] - signals[o["exit"]]["y"]))["route_id"]
    return dict(signals=signals, routes=routes, close_pairs=close_pairs, by_ent=by_ent, tracks=tracks)


# ------------------------------------------------------------------------------------------------ signallers

def build_signallers():
    """Rostered signallers (six to a workstation group), relief signallers, their qualification dates."""
    r = rng(2)
    staff = []
    seen = set()

    def staff_no():
        while True:
            v = int(r.integers(118000, 986000))
            if v not in seen and v % 10 != 0:
                seen.add(v)
                return "%06d" % v

    # first-two-years signallers: some qualified Oct 2023 to Sep 2024 (cross two years inside the window),
    # some later; qualification dates spread, never on a round date
    fy_dates = []
    for _ in range(4):
        fy_dates.append(dt.date(2023, 10, 1) + dt.timedelta(days=int(r.integers(9, 350))))
    for _ in range(4):
        fy_dates.append(dt.date(2024, 10, 1) + dt.timedelta(days=int(r.integers(5, 330))))
    for _ in range(2):   # qualified during the window and rostered from then on
        fy_dates.append(dt.date(2025, 11, 1) + dt.timedelta(days=int(r.integers(10, 150))))
    fy_slots = [int(v) for v in r.choice(30, size=len(fy_dates), replace=False)]
    k = 0
    for wi, ws in enumerate(WS_IDS):
        for j in range(5):
            idx = wi * 5 + j
            if idx in fy_slots:
                q = fy_dates[fy_slots.index(idx)]
            else:
                q = dt.date(int(r.integers(2006, 2023)), int(r.integers(1, 13)), int(r.integers(1, 28)))
                if q > dt.date(2023, 9, 1):
                    q = dt.date(2021, int(r.integers(1, 13)), int(r.integers(1, 28)))
            comp = [ws]
            if r.random() < 0.55:
                comp.append(WS_IDS[(wi + 1) % 6])
            if r.random() < 0.25:
                comp.append(WS_IDS[(wi + 3) % 6])
            staff.append(dict(staff_no=staff_no(), home=ws, qualified=q, competent=comp, relief=False,
                              grade="Signaller" if r.random() < 0.8 else "Senior Signaller"))
            k += 1
    for j in range(6):
        q = dt.date(int(r.integers(2009, 2022)), int(r.integers(1, 13)), int(r.integers(1, 28)))
        if j == 4:
            q = dt.date(2024, 12, 1) + dt.timedelta(days=int(r.integers(1, 120)))   # one relief signaller is newer
        staff.append(dict(staff_no=staff_no(), home=None, qualified=q, competent=list(WS_IDS), relief=True,
                          grade="Relief Signaller"))
    return staff


def first_two_years(person, day):
    """In the first two years since qualifying on the day in question."""
    q = person["qualified"]
    try:
        anniversary = q.replace(year=q.year + 2)
    except ValueError:
        anniversary = q.replace(year=q.year + 2, day=28)
    return q <= day < anniversary


# ------------------------------------------------------------------------------------------------ calendar

def days(a, b):
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)


def is_bst(utc):
    """UK summer time: from 01:00 UTC on the last Sunday of March to 01:00 UTC on the last Sunday of October."""
    y = utc.year

    def last_sunday(month):
        d = dt.date(y, month, 31)
        while d.weekday() != 6:
            d -= dt.timedelta(days=1)
        return dt.datetime(d.year, d.month, d.day, 1, 0)
    return last_sunday(3) <= utc < last_sunday(10)


def utc_to_local(utc):
    return utc + dt.timedelta(hours=1 if is_bst(utc) else 0)


def local_to_utc(local):
    """Local wall time to UTC (for the ambiguous autumn hour the first occurrence, BST, is taken)."""
    guess = local - dt.timedelta(hours=1)
    if is_bst(guess) and utc_to_local(guess) == local:
        return guess
    return local


def near_window_edge(utc, hours=3.0):
    """Within a few hours of the twelve months' first or last midnight, UK time (no incident falls there, so the
    window reads the same on UK time and on UTC)."""
    for d in (WINDOW_START, WINDOW_END + dt.timedelta(days=1)):
        b = local_to_utc(dt.datetime(d.year, d.month, d.day))
        if abs((utc - b).total_seconds()) < hours * 3600.0:
            return True
    return False


def railway_period(d):
    """Financial-year periods of four weeks from 1 April, P13 closing on 31 March."""
    fy = d.year if d >= dt.date(d.year, 4, 1) else d.year - 1
    start = dt.date(fy, 4, 1)
    # P01 runs to the fourth Saturday on or after 1 April's week; later periods are 28 days
    first_sat = start + dt.timedelta(days=(5 - start.weekday()) % 7)
    p01_end = first_sat + dt.timedelta(days=21)
    if d <= p01_end:
        return fy, 1
    n = 2 + (d - p01_end - dt.timedelta(days=1)).days // 28
    return fy, min(n, 13)


def period_label(d):
    fy, p = railway_period(d)
    return "%d/%02d P%02d" % (fy, (fy + 1) % 100, p)
