"""The main-call files: the property management system's reservation extract of 06:12 on 1 July 2027 (one row per room
reserved), its amendment log, its code lists and export notes, the night audit's daily statistics, the festival's
programme history and the sales office's events diary. Everything is written from the world's accepted reservations;
nothing is re-drawn here except the guest attributes the booking engine records (adults, children, country)."""
from __future__ import annotations

import datetime as dt
import hashlib
import json

import numpy as np

import cast as CA
import common as K
import world as WD

F_EXTRACT = "pms_reservations_extract_2027-07-01.csv"
F_AMEND = "pms_amendment_log_2027-07-01.csv"
F_NOTES = "pms_export_notes.txt"
F_CODES = "pms_code_lists.xlsx"
F_AUDIT = "night_audit_statistics_2022-2027.xlsx"
F_FEST = "festival_programme_dates.json"
F_DIARY = "sales_events_diary_2022-2027.xlsx"

EXTRACT_COLS = ["confirmation_no", "booking_ref", "created_utc", "arrival", "departure", "nights", "adults", "children",
                "rate_code", "rate_eur", "market", "channel", "status", "cancelled_utc", "group_code", "country"]
AMEND_COLS = ["confirmation_no", "changed_utc", "field", "old_value", "new_value", "changed_by"]

FIRST_ARR = K.di(K.FIRST_ARRIVAL)
EXTRACT_DAY = K.di(K.EXTRACT_LOCAL.date())
CHANNEL_REVIEW = dt.date(2025, 4, 1)

# ---------------------------------------------------------------------------------------------------- codes
RATE_CODES = [
    ("BAR", "Best available rate, room only", "Free cancellation until 14:00 two days before arrival", "None", "LEI"),
    ("BARBB", "Best available rate, bed and breakfast", "Free cancellation until 14:00 two days before arrival",
     "None", "LEI"),
    ("CORP", "Corporate negotiated rate, room only", "Free cancellation until 14:00 two days before arrival", "None",
     "COR"),
    ("SAV14", "Semi-flexible saver, room only", "Free cancellation until 14 days before arrival",
     "First night charged at 14 days", "LEI"),
    ("ADV", "Advance purchase, room only", "Non-refundable", "Full stay charged at booking", "LEI"),
    ("ADVBB", "Advance purchase, bed and breakfast", "Non-refundable", "Full stay charged at booking", "LEI"),
    ("EVT", "Event rate, room only (event dates)", "Non-refundable", "Full stay charged at booking", "LEI"),
    ("GRP", "Group and tour series", "Rooms released without charge up to 21 days before arrival",
     "Per group contract", "GRT"),
    ("COMP", "Complimentary", "Not applicable", "None", "CMP"),
    ("HSE", "House use (staff on call, contractors)", "Not applicable", "None", "HSE"),
    ("DAY", "Day use, 09:00 to 17:00", "Free cancellation until 12:00 the day before", "None", "COR"),
]
FACTOR = {"BAR": 1.0, "BARBB": 1.0, "CORP": 0.90, "SAV14": 0.94, "ADV": 0.88, "ADVBB": 0.88, "GRP": 0.62}
BB = {"BARBB": 18.0, "ADVBB": 18.0}

CHANNELS = [
    # code, description, valid from, valid to, replaced by
    ("GDS", "Global distribution systems (travel management companies)", "2015-01-01", "", ""),
    ("CORP", "Direct corporate (account managers, company booking tool)", "2015-01-01", "", ""),
    ("WEB", "Hotel website booking engine", "2015-01-01", "", ""),
    ("VOICE", "Reservations office, telephone and email", "2015-01-01", "2025-03-31", "CRO"),
    ("IDS1", "Internet distribution, merchant online travel agents", "2015-01-01", "2025-03-31", "OTAM"),
    ("IDS2", "Internet distribution, agency online travel agents", "2015-01-01", "2025-03-31", "OTAA"),
    ("IDS3", "Internet distribution, bed banks and wholesalers", "2017-06-01", "2025-03-31", "WHSL"),
    ("TOUR", "Tour operators and group series", "2015-01-01", "2025-03-31", "GRPT"),
    ("HOUSE", "House (complimentary and house use)", "2015-01-01", "", ""),
    ("CRO", "Central reservations office, telephone and email", "2025-04-01", "", ""),
    ("OTAM", "Online travel agents, merchant model", "2025-04-01", "", ""),
    ("OTAA", "Online travel agents, agency model", "2025-04-01", "", ""),
    ("WHSL", "Bed banks and wholesalers", "2025-04-01", "", ""),
    ("GRPT", "Tour operators and group series", "2025-04-01", "", ""),
]
CHAN_OLD = {"GDS": "GDS", "CORP": "CORP", "WEB": "WEB", "PHONE": "VOICE", "OTA1": "IDS1", "OTA2": "IDS2",
            "OTA3": "IDS3", "GROUP": "TOUR", "HOUSE": "HOUSE"}
CHAN_NEW = {"GDS": "GDS", "CORP": "CORP", "WEB": "WEB", "PHONE": "CRO", "OTA1": "OTAM", "OTA2": "OTAA",
            "OTA3": "WHSL", "GROUP": "GRPT", "HOUSE": "HOUSE"}
MARKETS = [("COR", "Corporate transient"), ("LEI", "Leisure transient"), ("GRT", "Group tour"),
           ("CMP", "Complimentary"), ("HSE", "House use")]
SEG_MARKET = {"BUS": "COR", "LEIS": "LEI", "FWK": "LEI", "FSH": "LEI", "EVT": "LEI", "GRP": "GRT", "COMP": "CMP",
              "HSE": "HSE"}

MONTH_BAR = {1: 109, 2: 112, 3: 125, 4: 132, 5: 139, 6: 149, 7: 159, 8: 165, 9: 149, 10: 139, 11: 125, 12: 119}
YEAR_F = {2021: 0.88, 2022: 0.90, 2023: 0.95, 2024: 0.98, 2025: 1.0, 2026: 1.03, 2027: 1.06, 2028: 1.09}
EVENT_NIGHTS = {n for _, ns, _, _ in WD.EVENTS for n in ns}


def bar(d):
    """The best available rate for the night of d, whole euros."""
    f = MONTH_BAR[d.month] * YEAR_F[d.year]
    if d.weekday() in (4, 5):
        f *= 1.18
    k = (d - K.fest_open(d.year)).days
    if -1 <= k <= 22:
        f *= 1.35
    if d in EVENT_NIGHTS:
        f *= 1.9
    return int(round(f))


_B0 = K.di(dt.date(2021, 1, 1))
_BAR = np.array([bar(K.dd(i)) for i in range(_B0, K.di(dt.date(2029, 1, 1)))], dtype=float)
_BARC = np.concatenate([[0.0], np.cumsum(_BAR)])


def uniforms(key, n):
    """n uniforms on [0, 1) from the key alone (one hash per eight)."""
    out = []
    i = 0
    while len(out) < n:
        h = hashlib.blake2b(("%s|u%d" % (key, i)).encode(), digest_size=64).digest()
        out += [int.from_bytes(h[8 * j:8 * j + 8], "big") / 18446744073709551616.0 for j in range(8)]
        i += 1
    return out[:n]


def pick(u, codes, weights):
    c = 0.0
    tot = float(sum(weights))
    for code, w in zip(codes, weights):
        c += w / tot
        if u < c:
            return code
    return codes[-1]


def stamp(t):
    """A simulation time (local clock) as the PMS writes it, in UTC to the second."""
    u = K.local_to_utc(K.to_local(t))
    return u.replace(microsecond=0).strftime("%Y-%m-%d %H:%M:%S")


def code6(key, used):
    al = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    n = 0
    while True:
        h = int.from_bytes(hashlib.blake2b(("%s|%d" % (key, n)).encode(), digest_size=8).digest(), "big")
        s = "".join(al[(h >> (5 * i)) & 31] for i in range(6))
        if s not in used:
            used.add(s)
            return s
        n += 1


COUNTRY = {
    "BUS": (["IE", "GB", "US", "DE", "FR", "NL", "BE", "ES"], [.58, .2, .07, .05, .04, .03, .015, .015]),
    "LEIS": (["IE", "GB", "US", "DE", "FR", "NL", "IT", "ES", "CA", "AU"], [.42, .18, .11, .07, .05, .04, .04, .04, .03, .02]),
    "EVT": (["IE", "GB", "US", "DE", "FR"], [.71, .23, .03, .02, .01]),
    "GRP": (["US", "DE", "IT", "FR", "ES", "CA"], [.38, .2, .14, .1, .1, .08]),
    "COMP": (["IE"], [1.0]), "HSE": (["IE"], [1.0]),
}


class Booking:
    """One accepted booking as the PMS holds it at the extract (all of its rooms). ext: in the extract (an arrival
    from 1 January 2022); the night audit counts every booking."""
    __slots__ = ("bt", "a", "los", "rooms", "rate_code", "rate", "market", "channel", "status", "ct", "group", "ref",
                 "conf0", "adults", "children", "country", "amend", "orig", "key", "seg", "plan", "noshow", "res", "ext")


def plan_rate_code(q, u):
    if q.plan == "FLX":
        if q.seg == "BUS":
            return "CORP" if u < 0.6 else "BAR"
        return "BARBB" if u < 0.45 else "BAR"
    if q.plan == "SEMI":
        return "SAV14"
    if q.plan == "APR":
        return "ADVBB" if u < 0.3 else "ADV"
    return q.plan


def stay_rate(code, a, los):
    if code in ("COMP", "HSE"):
        return 0.0
    if code == "EVT":
        return 329.0
    m = (_BARC[a + los - _B0] - _BARC[a - _B0]) / los
    return K.round_dp(m * FACTOR[code] + BB.get(code, 0.0), 2)


def status_of(rr):
    if rr.status == "CXL":
        return "CXL"
    if rr.a >= EXTRACT_DAY:
        return "RES"
    if rr.q.noshow:
        return "NS"
    if rr.a + rr.los >= EXTRACT_DAY:
        return "INH"
    return "OUT"


def day_use():
    """Day-use bookings (no night): weekdays outside July and August, from January 2022 to June 2027."""
    out = []
    d = dt.date(2021, 12, 1)
    while d <= dt.date(2027, 6, 30):
        if d.weekday() <= 4 and d.month not in (7, 8) and d not in K.HOLIDAYS:
            r = K.rng("dayuse", d.isoformat())
            for j in range(int(r.poisson(0.45))):
                bt = K.di(d) - r.uniform(0.2, 12.0)
                ct = bt + r.uniform(0.05, max(0.1, K.di(d) - 1 - bt)) if r.uniform() < 0.08 else None
                out.append(dict(bt=bt, a=K.di(d), ct=ct, key="DAY|%s|%d" % (d.isoformat(), j),
                                chan=str(r.choice(["CORP", "WEB", "PHONE", "GDS"], p=[.4, .3, .2, .1]))))
        d += dt.timedelta(days=1)
    return out


def bookings(W):
    """Every accepted booking with an arrival from 1 January 2022, and the day-use bookings, with their confirmation
    numbers (one per room, in booking order; bookings before 2022 arrivals use numbers too, so the extract has gaps)."""
    used = set()
    dus = day_use()
    items = [(rr.q.bt, 0, i) for i, rr in enumerate(W.res)] + [(du["bt"], 1, j) for j, du in enumerate(dus)]
    items.sort()
    conf = 1183407
    out = []
    grp_seq = {}
    for bt, kind, i in items:
        if kind == 0:
            rr = W.res[i]
            q = rr.q
            n = q.rooms
            b = Booking()
            u = uniforms(q.key, 2 + 2 * n)
            b.res, b.key, b.seg, b.plan, b.noshow = rr, q.key, q.seg, q.plan, q.noshow
            b.bt, b.a, b.los, b.rooms = q.bt, rr.a, rr.los, n
            b.rate_code = plan_rate_code(q, u[0])
            b.rate = stay_rate(b.rate_code, rr.a, rr.los)
            b.market = SEG_MARKET[q.seg]
            cdate = K.to_local(q.bt).date()
            b.channel = (CHAN_NEW if cdate >= CHANNEL_REVIEW else CHAN_OLD)[q.chan]
            b.status = status_of(rr)
            b.ct = rr.ct if rr.status == "CXL" else None
            if q.seg == "GRP":
                ad = K.dd(rr.orig_a)
                k = "%s" % ad.strftime("%y%m%d")
                grp_seq[k] = grp_seq.get(k, 0) + 1
                b.group = "GT%s-%02d" % (k, grp_seq[k])
            else:
                b.group = ""
            b.ref = code6(q.key, used)
            seg = q.seg if q.seg in COUNTRY else ("LEIS" if q.seg in ("FWK", "FSH") else q.seg)
            cs, cw = COUNTRY[seg]
            b.country = pick(u[1], cs, cw)
            ua, uc = u[2:2 + n], u[2 + n:2 + 2 * n]
            if q.seg == "BUS":
                b.adults = [1 if x < 0.86 else 2 for x in ua]
                b.children = [0] * n
            elif q.seg in ("COMP", "HSE"):
                b.adults, b.children = [1] * n, [0] * n
            elif q.seg == "GRP":
                b.adults = [2 if x < 0.78 else 1 for x in ua]
                b.children = [0] * n
            else:
                b.adults = [pick(x, [1, 2, 3], [.18, .76, .06]) for x in ua]
                b.children = [pick(x, [0, 1, 2], [.84, .09, .07]) for x in uc]
            b.amend = rr.amended
            b.conf0 = conf
            b.ext = rr.a >= FIRST_ARR
            conf += n
            out.append(b)
        else:
            du = dus[i]
            b = Booking()
            u = uniforms(du["key"], 1)
            b.res, b.key, b.seg, b.plan, b.noshow = None, du["key"], "BUS", "DAY", False
            b.bt, b.a, b.los, b.rooms = du["bt"], du["a"], 0, 1
            b.rate_code, b.rate, b.market = "DAY", 89.0 if K.dd(du["a"]).year < 2025 else 95.0, "COR"
            cdate = K.to_local(du["bt"]).date()
            b.channel = (CHAN_NEW if cdate >= CHANNEL_REVIEW else CHAN_OLD)[du["chan"]]
            b.status = "CXL" if du["ct"] is not None else "OUT"
            b.ct = du["ct"]
            b.group = ""
            b.ref = code6(du["key"], used)
            b.country = "IE" if u[0] < 0.8 else "GB"
            b.adults, b.children = [1], [0]
            b.amend = None
            b.ext = du["a"] >= FIRST_ARR
            b.conf0 = conf
            conf += 1
            out.append(b)
    return out


def adults_changes(B):
    """Guest-count changes the reservations office keyed (texture: they move no night)."""
    out = {}
    for b in B:
        if b.res is None or b.seg in ("COMP", "HSE", "GRP"):
            continue
        u = uniforms("adults|" + b.key, 2)
        if u[0] < 0.02:
            hi = b.a - 0.2
            if hi <= b.bt + 0.1:
                continue
            t = b.bt + 0.05 + u[1] * (hi - b.bt - 0.05)
            old = b.adults[0] + (1 if b.adults[0] == 1 else -1)
            out[b.key] = (t, old)
    return out


def agent_login(u, kind):
    if kind in ("WEB", "OTAM", "OTAA", "WHSL", "IDS1", "IDS2", "IDS3"):
        return "IFC.CHANNEL"
    if kind == "GDS":
        return "IFC.GDS"
    return CA.login_of(CA.RES_AGENTS[min(len(CA.RES_AGENTS) - 1, int(u * len(CA.RES_AGENTS)))])


def extract_rows(B):
    rows = []
    for b in B:
        if not b.ext:
            continue
        arr = K.dd(b.a)
        dep = K.dd(b.a + b.los)
        cu = stamp(b.bt)
        cx = stamp(b.ct) if b.ct is not None else ""
        for j in range(b.rooms):
            rows.append([b.conf0 + j, b.ref, cu, arr.isoformat(), dep.isoformat(), b.los, b.adults[j], b.children[j],
                         b.rate_code, "%.2f" % b.rate, b.market, b.channel, b.status, cx, b.group, b.country])
    rows.sort(key=lambda r: r[0])
    return rows


def amendment_rows(B):
    ach = adults_changes(B)
    rows = []
    for b in B:
        if not b.ext or (b.amend is None and b.key not in ach):
            continue
        u = uniforms("amendlog|" + b.key, 2)
        if b.amend is not None:
            t, oa, ol, na, nl = b.amend
            who = agent_login(u[0], b.channel)
            for j in range(b.rooms):
                if oa != na:
                    rows.append([b.conf0 + j, stamp(t), "ARRIVAL", K.dd(oa).isoformat(), K.dd(na).isoformat(), who])
                if oa + ol != na + nl:
                    rows.append([b.conf0 + j, stamp(t), "DEPARTURE", K.dd(oa + ol).isoformat(),
                                 K.dd(na + nl).isoformat(), who])
        if b.key in ach:
            t, old = ach[b.key]
            if b.ct is None or t < b.ct:
                who = agent_login(u[1], "VOICE")
                rows.append([b.conf0, stamp(t), "ADULTS", str(old), str(b.adults[0]), who])
    rows.sort(key=lambda r: (r[1], r[0], r[2]))
    return rows


# ---------------------------------------------------------------------------------------------------- night audit
def night_audit(B):
    """Each night's statistics as the night audit closed them, 1 January 2022 to 30 June 2027."""
    n0, n1 = K.di(dt.date(2022, 1, 1)), K.di(dt.date(2027, 6, 30))
    L = n1 - n0 + 1
    z = lambda: np.zeros(L, dtype=np.int64)
    occ, comp, hse, dayu, arr, dep, ns = z(), z(), z(), z(), z(), z(), z()
    rev = np.zeros(L)
    for b in B:
        if b.status == "CXL":
            continue
        if b.los == 0:
            if n0 <= b.a <= n1:
                dayu[b.a - n0] += b.rooms
            continue
        if b.status == "NS":
            if n0 <= b.a <= n1:
                ns[b.a - n0] += b.rooms
            continue
        if b.status not in ("OUT", "INH"):
            continue
        if n0 <= b.a <= n1:
            arr[b.a - n0] += b.rooms
        if n0 <= b.a + b.los <= n1:
            dep[b.a + b.los - n0] += b.rooms
        for n in range(max(b.a, n0), min(b.a + b.los, n1 + 1)):
            j = n - n0
            occ[j] += b.rooms
            if b.rate_code == "COMP":
                comp[j] += b.rooms
            elif b.rate_code == "HSE":
                hse[j] += b.rooms
            else:
                rev[j] += b.rate * b.rooms
    out = []
    for j in range(L):
        d = K.dd(n0 + j)
        out.append(dict(date=d, occ=int(occ[j]), comp=int(comp[j]), hse=int(hse[j]), dayuse=int(dayu[j]),
                        arr=int(arr[j]), dep=int(dep[j]), ns=int(ns[j]), rev=K.round_dp(rev[j], 2)))
    return out


# ---------------------------------------------------------------------------------------------------- festival
def festival():
    eds = []
    launch_day = {2015: 19, 2016: 17, 2017: 23, 2018: 22, 2019: 21, 2020: 19, 2021: 25, 2022: 24, 2023: 23,
                  2024: 21, 2025: 20, 2026: 19, 2027: 18}
    for i, y in enumerate(range(2015, 2028)):
        e = {"year": y, "edition": 34 + i}
        if y == 2020:
            e.update({"opening_night": None, "first_day": None, "last_day": None,
                      "launch": "%d-03-%02d" % (y, launch_day[y]), "status": "cancelled"})
        else:
            e.update({"opening_night": K.opening_night(y).isoformat(), "first_day": K.fest_open(y).isoformat(),
                      "last_day": (K.fest_open(y) + dt.timedelta(days=K.FEST_LEN - 1)).isoformat(),
                      "launch": "%d-03-%02d" % (y, launch_day[y]),
                      "status": "outdoor programme only" if y == 2021 else "held"})
            if y == 2027:
                e["status"] = "programme published"
        eds.append(e)
    return {"festival": K.FESTIVAL, "source": "Festival office, programme history (festival dates by edition)",
            "updated": "2027-03-18", "opening_night_note": "The festival opens with a preview night on the Thursday "
            "before its first Friday; the full programme runs from the first Friday of August for twenty-four days.",
            "editions": eds}


def write_festival(path):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(festival(), fh, indent=2, ensure_ascii=False)
        fh.write("\n")


# ---------------------------------------------------------------------------------------------------- diary
def diary():
    """The sales office's diary of city events, 2022 to 2027 (dates, venue, what is known; no figures)."""
    D = dt.date
    rows = []
    acts = {D(2023, 5, 19): "Lumenhart", D(2024, 6, 28): "Pellisand", D(2025, 5, 2): "Corvane",
            D(2025, 9, 26): "Lumenhart", D(2026, 6, 5): "Pellisand"}
    for ann, ns, _, lab in WD.EVENTS:
        fri = ns[0]
        if lab == "rugby":
            rows.append((ns[1], ns[1], "Rugby international", K.STADIUM, "Sport", ann,
                         "Kick-off 17:30"))
        elif lab == "conference":
            rows.append((ns[0] - dt.timedelta(days=1), ns[1], "International dairy science congress",
                         K.CONVENTION, "Conference", ann, "Thursday to Saturday; delegates book direct"))
        elif fri.year == 2027:
            rows.append((ns[0], ns[1], "%s, two concerts" % K.BAND, K.STADIUM, "Concert", ann,
                         "Tickets on sale Friday 18 June 09:00"))
        else:
            rows.append((ns[0], ns[1], "%s, two concerts" % acts[fri], K.STADIUM, "Concert", ann, ""))
    launch = {e["year"]: dt.date.fromisoformat(e["launch"]) for e in festival()["editions"]}
    for y in range(2022, 2028):
        rows.append((K.opening_night(y), K.fest_open(y) + dt.timedelta(days=K.FEST_LEN - 1), K.FESTIVAL,
                     "City centre", "Festival", launch[y], "Programme launch; preview night on the Thursday"))
    # events that did not fill the city's hotels
    other = [
        (D(2022, 4, 9), D(2022, 4, 10), "Spring trade fair", K.CONVENTION, "Trade fair", D(2021, 11, 2), ""),
        (D(2022, 10, 23), D(2022, 10, 23), "Callowfort Marathon", "City centre", "Sport", D(2022, 1, 20), ""),
        (D(2022, 12, 7), D(2022, 12, 9), "University conferring", "University", "Academic", D(2022, 9, 1), ""),
        (D(2023, 3, 17), D(2023, 3, 17), "St Patrick's Day parade", "City centre", "Civic", D(2022, 12, 1), ""),
        (D(2023, 4, 22), D(2023, 4, 23), "Spring trade fair", K.CONVENTION, "Trade fair", D(2022, 11, 8), ""),
        (D(2023, 10, 22), D(2023, 10, 22), "Callowfort Marathon", "City centre", "Sport", D(2023, 1, 19), ""),
        (D(2023, 12, 6), D(2023, 12, 8), "University conferring", "University", "Academic", D(2023, 9, 4), ""),
        (D(2024, 4, 13), D(2024, 4, 14), "Spring trade fair", K.CONVENTION, "Trade fair", D(2023, 11, 6), ""),
        (D(2024, 9, 14), D(2024, 9, 14), "Hurling league final", K.STADIUM, "Sport", D(2024, 7, 2), ""),
        (D(2024, 10, 27), D(2024, 10, 27), "Callowfort Marathon", "City centre", "Sport", D(2024, 1, 22), ""),
        (D(2024, 12, 4), D(2024, 12, 6), "University conferring", "University", "Academic", D(2024, 9, 2), ""),
        (D(2025, 4, 5), D(2025, 4, 6), "Spring trade fair", K.CONVENTION, "Trade fair", D(2024, 11, 4), ""),
        (D(2025, 10, 26), D(2025, 10, 26), "Callowfort Marathon", "City centre", "Sport", D(2025, 1, 21), ""),
        (D(2025, 12, 3), D(2025, 12, 5), "University conferring", "University", "Academic", D(2025, 9, 1), ""),
        (D(2026, 4, 18), D(2026, 4, 19), "Spring trade fair", K.CONVENTION, "Trade fair", D(2025, 11, 3), ""),
        (D(2026, 9, 12), D(2026, 9, 12), "Hurling league final", K.STADIUM, "Sport", D(2026, 7, 7), ""),
        (D(2026, 10, 25), D(2026, 10, 25), "Callowfort Marathon", "City centre", "Sport", D(2026, 1, 20), ""),
        (D(2026, 12, 2), D(2026, 12, 4), "University conferring", "University", "Academic", D(2026, 9, 7), ""),
        (D(2027, 4, 10), D(2027, 4, 11), "Spring trade fair", K.CONVENTION, "Trade fair", D(2026, 11, 2), ""),
        (D(2027, 9, 18), D(2027, 9, 18), "Hurling league final", K.STADIUM, "Sport", D(2027, 6, 1), "Date confirmed"),
        (D(2027, 10, 24), D(2027, 10, 24), "Callowfort Marathon", "City centre", "Sport", D(2027, 1, 18), ""),
    ]
    rows += other
    rows.sort(key=lambda r: (r[0], r[2]))
    return rows


# ---------------------------------------------------------------------------------------------------- notes
NOTES_TEXT = """THE WEIGHHOUSE HOTEL - PROPERTY MANAGEMENT SYSTEM
Reservation extract: notes on the export

File:     pms_reservations_extract_2027-07-01.csv
Taken:    01/07/2027 06:12 (after the night audit of 30/06/2027)
Holds:    every reservation with an arrival date from 01/01/2022, cancelled and no-show reservations included
Sort:     confirmation_no

One row per room reserved. Rooms reserved together on one booking share the booking reference.
Times (created_utc, cancelled_utc) are UTC. Arrival and departure are the hotel's local dates.
A reservation's nights run from its arrival date to the night before its departure date. A day-use reservation has no night.
The extract carries each reservation's current dates and guest count. Changes to them are in the amendment log
(pms_amendment_log_2027-07-01.csv, one row per field changed, for the reservations in this extract).
The hotel has 480 rooms.

Fields
confirmation_no   PMS confirmation number of the room reservation
booking_ref       booking reference (shared by the rooms of one booking)
created_utc       time the reservation was made
arrival           arrival date
departure         departure date
nights            nights reserved (departure less arrival)
adults, children  guests in the room
rate_code         rate code (pms_code_lists.xlsx, sheet Rate codes)
rate_eur          average nightly room rate, EUR, VAT included; 0.00 for complimentary and house use
market            market segment (pms_code_lists.xlsx, sheet Market segments)
channel           booking channel (pms_code_lists.xlsx, sheet Channel codes)
status            RES reserved, INH in house, OUT checked out, CXL cancelled, NS no-show
cancelled_utc     time the reservation was cancelled (CXL only)
group_code        group or tour series code (rate code GRP)
country           guest's country of residence (ISO 3166-1 alpha-2)

Room numbers are assigned at check-in and are not in this extract.
Channel codes were revised on 01/04/2025; reservations made before then keep the codes they were made under.
"""


def write_notes(path):
    with open(path, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write(NOTES_TEXT)
