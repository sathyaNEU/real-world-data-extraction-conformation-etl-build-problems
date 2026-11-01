"""task125: the 2026 patrol roster and calls for service (the city and the contracted Township of Elmvale), and the
paid-duty bookings 2022 to 2027. Drawn after world.py's objects, from the same generator."""
import datetime as dt
import math

import numpy as np

import world as W

_TZ = None


def tz():
    global _TZ
    if _TZ is None:
        import zoneinfo
        _TZ = zoneinfo.ZoneInfo("America/Toronto")
    return _TZ


HOUR = np.array([2.2, 1.8, 1.5, 1.1, 0.8, 0.7, 0.9, 1.6, 2.6, 3.0, 3.2, 3.3, 3.5, 3.6, 3.7, 3.9, 4.2, 4.4, 4.5,
                 4.4, 4.2, 3.9, 3.4, 2.8])
HOUR = HOUR / HOUR.sum()
P1_TYPES = ["ASSAULT IN PROGRESS", "WEAPONS CALL", "ROBBERY IN PROGRESS", "BREAK AND ENTER IN PROGRESS",
            "DOMESTIC IN PROGRESS", "MVC PERSONAL INJURY", "PERSON IN CRISIS - WEAPON", "ALARM - HOLDUP"]
OTHER_TYPES = ["NOISE COMPLAINT", "THEFT REPORT", "SUSPICIOUS PERSON", "MVC PROPERTY DAMAGE", "TRESPASS",
               "UNWANTED PERSON", "CHECK WELFARE", "ALARM - INTRUSION", "MISCHIEF REPORT", "TRAFFIC COMPLAINT",
               "FRAUD REPORT", "DISTURBANCE", "ANIMAL COMPLAINT", "FOUND PROPERTY", "BYLAW ASSIST"]
WARD_TRAVEL = {1: 4.7, 2: 5.2, 3: 4.9, 4: 5.6, 5: 5.9, 6: 6.4, 7: 6.1, 8: 6.7}
ZONE = {w: "ABCDEFGH"[w - 1] for w in range(1, 9)}
NEIGHBOUR = {1: (2, 3), 2: (1, 6), 3: (1, 4), 4: (3, 8), 5: (6, 7), 6: (5, 2), 7: (5, 8), 8: (7, 4)}
CITY_UNITS = ["%s%d" % (ZONE[w], k) for w in range(1, 9) for k in (1, 2)]
ALL_UNITS = CITY_UNITS + ["S1", "S2", "T1", "T2"]


def badges(r):
    return sorted(int(b) for b in r.choice(np.arange(310, 2980), size=212, replace=False))


# ----------------------------------------------------------------------------------------------- the patrol roster
def roster(r, bdg):
    """The 2026 tours: day tours 07:00 to 19:00 and night tours 19:00 to 07:00, each dated the day it starts, with
    each unit's crew. Night tours on Fridays and Saturdays are two-officer cars; other nights vary car by car."""
    out = {}
    d = dt.date(2025, 12, 31)
    while d <= dt.date(2026, 12, 31):
        for shift in ("D", "N"):
            if d.year == 2025 and shift == "D":
                continue
            pool = list(r.permutation(bdg))
            k = 0
            for u in ALL_UNITS:
                if shift == "D":
                    n = 2 if (u in CITY_UNITS and r.random() < 0.10) else 1
                else:
                    if u in ("S1", "S2"):
                        n = 1
                    elif d.weekday() in (4, 5):
                        n = 2 if r.random() < 0.95 else 1
                    else:
                        n = 2 if r.random() < 0.56 else 1
                out[(d, shift, u)] = [int(x) for x in pool[k:k + n]]
                k += n
        d += dt.timedelta(1)
    return out


def tour_of(t_local):
    """The tour (its date and letter) covering a local time."""
    h = t_local.hour + t_local.minute / 60.0
    d = t_local.date()
    if 7 <= h < 19:
        return d, "D"
    if h >= 19:
        return d, "N"
    return d - dt.timedelta(1), "N"


def tour_end(t):
    """The end of the tour covering an instant, as an aware datetime (07:00 and 19:00 exist on every date)."""
    z = tz()
    d, s = tour_of(t.astimezone(z))
    if s == "D":
        return dt.datetime(d.year, d.month, d.day, 19, 0, tzinfo=z)
    e = d + dt.timedelta(1)
    return dt.datetime(e.year, e.month, e.day, 7, 0, tzinfo=z)


UTC = dt.timezone.utc
QUIET = (dt.datetime(2026, 3, 9, 0, 0), dt.datetime(2026, 3, 9, 1, 0))


def wall(naive):
    """A real local time from a drawn wall time: a time the March change skips reads an hour later, and a time in
    the first hour of 9 March is taken an hour later too."""
    z = tz()
    t = naive.replace(tzinfo=z)
    if t.astimezone(UTC).astimezone(z).replace(tzinfo=None) != naive:
        naive = naive + dt.timedelta(hours=1)
    if QUIET[0] <= naive < QUIET[1]:
        naive = naive + dt.timedelta(hours=1)
    return naive.replace(tzinfo=z)


def quiet(t):
    """An instant in the first hour of 9 March moved an hour on, so every reading of a night tour's date agrees."""
    z = tz()
    loc = t.astimezone(z).replace(tzinfo=None)
    if QUIET[0] <= loc < QUIET[1]:
        return t + dt.timedelta(hours=1)
    return t


# ----------------------------------------------------------------------------------------------- the calls
def address(r, s):
    side = int(r.integers(2))
    lo, hi = (s["l_from"], s["l_to"]) if side == 0 else (s["r_from"], s["r_to"])
    return lo + 2 * int(r.integers(0, (hi - lo) // 2 + 1))


def cad(r, segs, twp, base, nonp):
    """The communications centre's 2026 events, the city's and Elmvale's, each with its units' times. No unit is
    still committed to a call when its tour ends: a unit dispatched in the minutes before a change clears first."""
    z = tz()
    city_w = np.array([base[s["id"]] + nonp[s["id"]] + 1.2 for s in segs])
    city_w = city_w / city_w.sum()
    events = []
    seq = 1
    d = dt.date(2026, 1, 1)
    while d <= dt.date(2026, 12, 31):
        for area, n in (("city", int(r.poisson(79))), ("twp", int(r.poisson(8.1)))):
            for _ in range(n):
                h = int(r.choice(24, p=HOUR))
                drawn = dt.datetime(d.year, d.month, d.day, h, int(r.integers(60)), int(r.integers(60)))
                t_local = wall(drawn)
                u = r.random()
                prio = 1 if u < 0.062 else (2 if u < 0.30 else (3 if u < 0.76 else 4))
                if area == "city":
                    s = segs[int(r.choice(len(segs), p=city_w))]
                    seg, district, ward = s["id"], s["ward"], s["ward"]
                    addr = "%d %s" % (address(r, s), s["street"].upper())
                else:
                    t = twp[int(r.integers(len(twp)))]
                    seg, district, ward = t["id"], t["zone"], None
                    addr = "%d %s" % (t["n0"] + 2 * int(r.integers(1, 45)), t["street"].upper())
                v = r.random()
                if prio == 1:
                    src = "911" if v < 0.71 else ("PHONE" if v < 0.85 else ("ALARM" if v < 0.92 else "OFFICER"))
                    ctype = P1_TYPES[int(r.integers(len(P1_TYPES)))]
                    if ctype == "ALARM - HOLDUP":
                        src = "ALARM"
                else:
                    src = "911" if v < 0.22 else ("PHONE" if v < 0.66 else ("ALARM" if v < 0.75 else
                                                                          ("OFFICER" if v < 0.97 else "WALK-IN")))
                    ctype = OTHER_TYPES[int(r.integers(len(OTHER_TYPES)))]
                ev = {"seq": seq, "received": t_local, "drawn": drawn, "priority": prio, "type": ctype, "source": src,
                      "address": addr, "segment": seg, "district": district, "ward": ward, "area": area,
                      "units": []}
                seq += 1
                disp = "COMPLETED"
                if src == "WALK-IN":
                    disp = "REPORT TAKEN"
                elif prio >= 3 and r.random() < 0.035:
                    disp = "MERGED"
                elif r.random() < (0.02 if prio == 1 else 0.06):
                    disp = "CANCELLED"
                ev["disposition"] = disp
                if disp not in ("MERGED", "REPORT TAKEN"):
                    _units(r, ev, prio, src, area, ward)
                events.append(ev)
        d += dt.timedelta(1)
    events.sort(key=lambda e: (e["received"].astimezone(UTC), e["seq"]))
    return events


def _units(r, ev, prio, src, area, ward):
    nunits = (2 + int(r.poisson(0.55))) if prio == 1 else (1 + int(r.random() < 0.45) if prio == 2 else 1)
    if area == "city":
        own = ["%s%d" % (ZONE[ward], k) for k in (1, 2)]
        near = ["%s%d" % (ZONE[w], k) for w in NEIGHBOUR[ward] for k in (1, 2)]
        cand = [own[int(r.integers(2))]] + list(r.permutation([u for u in own + near]))
    else:
        cand = [["T1", "T2"][int(r.integers(2))]] + list(r.permutation(["T1", "T2", "D1", "D2", "C1", "C2"]))
    if prio == 1 and r.random() < 0.3:
        cand.insert(1, ["S1", "S2"][int(r.integers(2))])
    chosen = []
    for u in cand:
        if u not in chosen:
            chosen.append(u)
        if len(chosen) == nunits:
            break
    z = tz()
    t0 = ev["received"].astimezone(UTC)
    w0 = ev["drawn"]
    delay = {1: 0.85, 2: 2.6, 3: 7.5, 4: 18.0}[prio] * math.exp(r.normal(0, 0.45))
    travel = (WARD_TRAVEL[ward] if area == "city" else 11.6) * (1.0 if prio == 1 else 1.22)
    first = travel * math.exp(r.normal(0, 0.40))
    for k, u in enumerate(chosen):
        # w_* replay the wall-clock times every draw was decided on; the stamps themselves run in UTC
        if src == "OFFICER" and k == 0:
            s1, s2 = int(r.integers(5, 40)), int(r.integers(0, 15))
            w_dsp = w0 + dt.timedelta(seconds=s1)
            w_ons = w_dsp + dt.timedelta(seconds=s2)
            dsp = quiet(t0 + dt.timedelta(seconds=s1))
            ons = dsp + dt.timedelta(seconds=s2)
        else:
            lead = delay + 0.6 * k * r.random()
            tr = first if k == 0 else first * (1.0 + 0.35 * r.random()) + r.uniform(0.5, 4.0)
            w_dsp = w0 + dt.timedelta(minutes=lead)
            w_ons = w_dsp + dt.timedelta(minutes=tr)
            dsp = quiet(t0 + dt.timedelta(minutes=lead))
            ons = dsp + dt.timedelta(minutes=tr)
        w_end = _wall_end(w_dsp)
        end = tour_end(dsp).astimezone(UTC)
        if w_ons >= w_end - dt.timedelta(minutes=2):
            s3 = int(r.integers(20, 90))
            extra = first if k == 0 else first + r.uniform(0.5, 4.0)
            w_dsp = w_end + dt.timedelta(seconds=s3)
            w_end = _wall_end(w_dsp)
            dsp = quiet(end + dt.timedelta(seconds=s3))
            ons = dsp + dt.timedelta(minutes=extra)
            end = tour_end(dsp).astimezone(UTC)
        elif ons >= end - dt.timedelta(minutes=2):
            dsp = quiet(end + dt.timedelta(seconds=55))
            ons = dsp + dt.timedelta(minutes=first)
            end = tour_end(dsp).astimezone(UTC)
        lag0 = int(r.integers(10, 75))
        w_enr = w_dsp + dt.timedelta(seconds=lag0)
        lag = min(lag0, max(0, int((ons - dsp).total_seconds()) // 2))
        enr = dsp + dt.timedelta(seconds=lag)
        if ev["disposition"] == "CANCELLED":
            g = float(r.uniform(1.5, 9.0))
            w_clr = w_enr + dt.timedelta(minutes=g)
            ons = None
            clr = enr + dt.timedelta(minutes=g)
        else:
            g = float(r.gamma(2.2, 18.0))
            w_clr = w_ons + dt.timedelta(minutes=g)
            clr = ons + dt.timedelta(minutes=g)
        if w_clr >= w_end - dt.timedelta(minutes=1):
            clr = end - dt.timedelta(seconds=int(r.integers(40, 200)))
        elif clr >= end - dt.timedelta(minutes=1):
            clr = end - dt.timedelta(seconds=90)
        if ons is not None and clr <= ons:
            clr = ons + dt.timedelta(seconds=30)
        if clr <= enr:
            clr = enr + dt.timedelta(seconds=30)
        sec = lambda x: None if x is None else x.replace(microsecond=0).astimezone(z)
        ev["units"].append({"unit": u, "dispatched": sec(dsp), "enroute": sec(enr), "onscene": sec(ons),
                            "cleared": sec(clr)})


def _wall_end(w):
    """The end of the tour covering a naive wall-clock time, as a naive wall-clock time."""
    h = w.hour + w.minute / 60.0
    d = w.date()
    if 7 <= h < 19:
        return dt.datetime(d.year, d.month, d.day, 19, 0)
    if h >= 19:
        d = d + dt.timedelta(1)
    return dt.datetime(d.year, d.month, d.day, 7, 0)


# ----------------------------------------------------------------------------------------------- paid duty
CLIENTS = {
    "TRAFFIC CONTROL": ["CITY OF MOUNTJOY - ROADS", "CITY OF MOUNTJOY - WATER SERVICES", "HYDRO MOUNTJOY",
                        "ENBRIDGE GAS", "BELL CANADA", "COGECO CONNEXION", "DUFFERIN CONSTRUCTION",
                        "KAWARTHA PAVING LTD", "TRENT VALLEY ASPHALT", "LAKEHEAD CIVIL INC"],
    "FILM": ["NORTHFIELD PICTURES INC", "LANTERN FILMS (ONT) LTD"],
    "ESCORT": ["COMSTOCK FUNERAL HOME", "NELSON-HARRIS FUNERAL HOME", "LAKELAND HEAVY HAUL"],
    "SECURITY": ["CIBC", "ROYAL BANK", "SHOPPERS DRUG MART", "NORTHGATE MALL MANAGEMENT", "LCBO"],
    "EVENT": ["MOUNTJOY RIBFEST", "DOWNTOWN MOUNTJOY BIA", "MOUNTJOY ROTARY CLUB", "SANTA CLAUS PARADE COMMITTEE",
              "MOUNTJOY HALF MARATHON", "CANADA DAY COMMITTEE"],
    "OTHER": ["MOUNTJOY HOSPITAL", "TRENTWAY BUS LINES", "ST PETER SECONDARY SCHOOL", "CITY OF MOUNTJOY - PARKS"],
}
CAT_SHARE = [("TRAFFIC CONTROL", 0.57), ("ESCORT", 0.10), ("SECURITY", 0.10), ("OTHER", 0.10), ("EVENT", 0.09),
             ("FILM", 0.04)]


def hm(x):
    return "%02d:%02d" % (int(x) // 60 % 24, int(x) % 60)


def interior_nodes(segs):
    """Grid nodes whose four segments are all in one ward, for intersection locations."""
    bk = W.by_key(segs)
    out = []
    for i in range(1, len(W.NS) - 1):
        for j in range(1, len(W.EW) - 1):
            ks = [("NS", i, j - 1), ("NS", i, j), ("EW", j, i - 1), ("EW", j, i)]
            if all(k in bk for k in ks) and len({bk[k]["ward"] for k in ks}) == 1:
                out.append((i, j, bk[("NS", i, j)]["ward"], bk[("NS", i, j)]["id"]))
    return out


def _category(r):
    u = r.random()
    acc = 0.0
    for c, p in CAT_SHARE:
        acc += p
        if u < acc:
            return c
    return CAT_SHARE[-1][0]


def _minutes(x):
    h, m = map(int, x.split(":"))
    return h * 60 + m


def bookings(r, segs, ev, bdg):
    """Every paid-duty booking 2022 to 2027 with its date, booked hours, location, client and officer lines, and
    each worked line's actual hours. The truth keeps each booking's segment and ward."""
    bk = W.by_key(segs)
    nodes = interior_nodes(segs)
    out = []
    for (d, venue, kind, client, st, en, offs) in ev:
        v = W.GARDENS if venue == "G" else W.LAKESHORE
        s = bk[v["seg"]]
        out.append({"date": d, "start": st, "end": en, "overnight": False, "category": "EVENT", "client": client,
                    "loc": "%s, %d %s" % (v["name"], v["number"], v["street"].upper()), "seg": s["id"],
                    "ward": s["ward"], "officers": offs, "venue": venue})
    weights = np.array([s["len"] for s in segs])
    weights = weights / weights.sum()
    for y in range(2022, 2027):
        n = int(r.normal(1960, 40))
        for _ in range(n):
            cat = _category(r)
            if cat == "TRAFFIC CONTROL" and r.random() > 0.3:
                doy = int(r.integers(90, 320))
            else:
                doy = int(r.integers(0, 365))
            d = dt.date(y, 1, 1) + dt.timedelta(doy)
            if d.year != y:
                continue
            night = False
            if cat == "TRAFFIC CONTROL":
                night = r.random() < (0.11 if d.month in (1, 2, 3, 12) else 0.13)
            elif cat == "FILM":
                night = r.random() < 0.35
            if night:
                st = int(r.choice([1260, 1290, 1320, 1350, 1380]))
                dur = int(r.choice([420, 450, 480, 510, 540, 600]))
            else:
                st = int(r.choice([360, 390, 420, 450, 480, 540, 600, 660, 720]))
                dur = int(r.choice([180, 210, 240, 300, 360, 420, 480, 510, 540, 600]))
                if cat == "ESCORT":
                    dur = int(r.choice([120, 150, 180]))
            en = st + dur
            s = segs[int(r.choice(len(segs), p=weights))]
            if r.random() < 0.66:
                loc = "%d %s" % (address(r, s), s["street"].upper())
                seg, ward = s["id"], s["ward"]
            else:
                i, j, ward, seg = nodes[int(r.integers(len(nodes)))]
                loc = ("%s / %s" % (W.NS[i].upper(), W.EW[j].upper()) if r.random() < 0.5 else
                       "%s / %s" % (W.EW[j].upper(), W.NS[i].upper()))
            offs = 1 + int(r.random() < 0.38) + int(r.random() < 0.10)
            client = CLIENTS[cat][int(r.integers(len(CLIENTS[cat])))]
            out.append({"date": d, "start": hm(st), "end": hm(en), "overnight": en > 1440, "category": cat,
                        "client": client, "loc": loc, "seg": seg, "ward": ward, "officers": offs, "venue": None})
    for b in out:
        lead = int(r.integers(2, 70)) if b["category"] != "EVENT" else int(r.integers(20, 110))
        b["taken"] = b["date"] - dt.timedelta(lead)
        if b["venue"] and b["date"].year == 2027 and b["client"] != "MOUNTJOY MARINERS HOCKEY CLUB":
            b["taken"] = W.AS_OF - dt.timedelta(int(r.integers(9, 120)))
        if b["client"] == "MOUNTJOY MARINERS HOCKEY CLUB":
            # the club books each half season's home dates in one batch
            b["taken"] = dt.date(b["date"].year - (1 if b["date"].month <= 6 else 0), 12, 14) \
                if b["date"].month <= 6 else dt.date(b["date"].year, 8, 18)
    for _ in range(64):
        d = W.AS_OF + dt.timedelta(int(r.integers(2, 80)))
        s = segs[int(r.choice(len(segs), p=weights))]
        cat = "TRAFFIC CONTROL" if r.random() < 0.6 else ("ESCORT" if r.random() < 0.5 else "SECURITY")
        st = int(r.choice([390, 420, 450, 480]))
        out.append({"date": d, "start": hm(st), "end": hm(st + int(r.choice([240, 360, 480]))), "overnight": False,
                    "category": cat, "client": CLIENTS[cat][int(r.integers(len(CLIENTS[cat])))],
                    "loc": "%d %s" % (address(r, s), s["street"].upper()), "seg": s["id"], "ward": s["ward"],
                    "officers": 1 + int(r.random() < 0.3), "venue": None,
                    "taken": W.AS_OF - dt.timedelta(int(r.integers(1, 40)))})
    out = [b for b in out if b["taken"] <= W.AS_OF]
    out.sort(key=lambda b: (b["taken"], b["date"], b["start"], b["loc"]))
    counters = {}
    for b in out:
        yy = b["taken"].year % 100
        counters[yy] = counters.get(yy, 0) + 1 + int(r.random() < 0.06)
        b["no"] = "PD%02d-%04d" % (yy, counters[yy])
    for b in out:
        future = b["date"] > W.AS_OF
        if future:
            b["status"] = "BOOKED"
        elif b["venue"]:
            b["status"] = "COMPLETED"
        else:
            u = r.random()
            b["status"] = "COMPLETED" if u < 0.93 else ("CANCELLED" if u < 0.975 else "CANCELLED LATE")
        pool = list(r.choice(bdg, size=b["officers"], replace=False))
        st, en = _minutes(b["start"]), _minutes(b["end"])
        if b["overnight"] or en <= st:
            en += 1440
        lines = []
        for k in range(b["officers"]):
            line = {"line": k + 1, "badge": int(pool[k]), "a_start": None, "a_end": None, "hours": 0.0}
            if future:
                line["status"] = "BOOKED"
                if r.random() > 0.55:
                    line["badge"] = None
            elif b["status"] in ("CANCELLED", "CANCELLED LATE"):
                line["status"] = b["status"]
            elif r.random() < 0.012:
                line["status"] = "NO SHOW"
            else:
                line["status"] = "WORKED"
                u = r.random()
                delta = 0
                if u < 0.12:
                    delta = -15 * int(r.integers(2, 9))
                elif u < 0.20:
                    delta = 15 * int(r.integers(1, 9))
                a_en = max(st + 60, en + delta)
                line["a_start"], line["a_end"], line["hours"] = st, a_en, (a_en - st) / 60.0
            lines.append(line)
        b["lines"] = lines
    return out
