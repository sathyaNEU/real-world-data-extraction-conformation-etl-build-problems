"""The commercial side of the Ravelmond world: the screens and their media players, the content system's player
health, the autumn bookings and their billing. Clean truth only; pack.py writes the files."""
import datetime as dt
import math

import params as P

LOCAL_OFFSET_BEFORE = 2     # CEST, hours ahead of UTC until 03:00 local on 25 October 2026
LOCAL_OFFSET_AFTER = 1      # CET


def utc_offset(local_dt):
    switch = dt.datetime(2026, 10, 25, 3, 0)
    return LOCAL_OFFSET_BEFORE if local_dt < switch else LOCAL_OFFSET_AFTER


def to_utc(local_dt):
    return local_dt - dt.timedelta(hours=utc_offset(local_dt))


def opening(day):
    """Station opening hours on a calendar day, as local datetimes (the metro closes at 00:30 after the day)."""
    wd = day.weekday()
    start = {5: dt.time(6, 30), 6: dt.time(7, 0)}.get(wd, dt.time(5, 45))
    return dt.datetime.combine(day, start), dt.datetime.combine(day + dt.timedelta(days=1), dt.time(0, 30))


def overlap_hours(a0, a1, b0, b1):
    s, e = max(a0, b0), min(a1, b1)
    return max(0.0, (e - s).total_seconds() / 3600.0)


LOC_NAMES = {}


class Screen:
    def __init__(self, tag, loc, pos, pkg, hung, down=None):
        self.tag, self.loc, self.pos, self.pkg, self.hung, self.down = tag, loc, pos, pkg, hung, down


def build(rng, net):
    """Screens, players, cabling, health, bookings, billing."""
    A = type("Asks", (), {})()
    A.rng = rng
    # ------------------------------------------------------------ screens
    locs = sorted({l for code in P.PACKAGE_ORDER for l in P.PACKAGES[code][1]})
    tags = set()

    def new_tag():
        while True:
            t = "SB%05d" % rng.randrange(10000, 99999)
            if t not in tags:
                tags.add(t)
                return t
    screens = []
    pos_counter = {}
    hung_base = dt.date(2023, 3, 1)
    for code in P.PACKAGE_ORDER:
        for loc in P.PACKAGES[code][1]:
            n = rng.choice((2, 3, 3, 4)) if loc.endswith("-OV") or loc.startswith("CEN") else rng.choice((1, 2, 2, 3, 3))
            for _ in range(n):
                k = pos_counter.get(loc, 0) + 1
                pos_counter[loc] = k
                pos = "%s-%s%02d" % (loc, "ABCD"[k % 4], k)
                hung = hung_base + dt.timedelta(days=rng.randrange(0, 1100))
                screens.append(Screen(new_tag(), loc, pos, code, hung))
    A.screens = screens
    # ------------------------------------------------------------ players: 2 to 4 screens at one location
    by_loc = {}
    for s in screens:
        by_loc.setdefault(s.loc, []).append(s)
    players = {}
    cabling = []         # (tag, player, from local datetime, to local datetime or None)
    pid = set()

    def new_player():
        while True:
            p = "MP-%03X%d" % (rng.randrange(256, 4095), rng.randrange(10))
            if p not in pid:
                pid.add(p)
                return p
    for loc in sorted(by_loc):
        ss = sorted(by_loc[loc], key=lambda s: s.pos)
        i = 0
        while i < len(ss):
            k = min(len(ss) - i, rng.choice((2, 3, 3, 4)))
            if i == 0 and len(ss) >= 3:
                k = min(k, len(ss) - 1)
            p = new_player()
            players[p] = loc
            for s in ss[i:i + k]:
                cabling.append([s.tag, p, dt.datetime.combine(s.hung, dt.time(4, 0)), None])
            i += k
    A.players = players
    # failures during the flights: for each autumn booking one media player behind some of its package's screens
    # dies, and its screens are re-cabled to a working player at the same place a day or two later; the register
    # records the move when the work order is closed, one to six days after the job
    failures = []
    loc_players = {}
    for t, pl, a0, b0 in cabling:
        loc_players.setdefault(players[pl], set()).add(pl)
    pkg_of_tag = {s.tag: s.pkg for s in screens}
    used_locs = set()
    for ref, ai, pkg, (m0, d0), (m1, d1), price in BOOKINGS:
        f0, f1 = dt.date(2026, m0, d0), dt.date(2026, m1, d1)
        cands = [l for l in P.PACKAGES[pkg][1] if len(loc_players.get(l, ())) >= 2 and l not in used_locs
                 and l != "WLH-H"]
        if not cands:
            continue
        loc = cands[rng.randrange(len(cands))]
        used_locs.add(loc)
        ps = sorted(loc_players[loc])
        dead = [p for p in ps if any(c[1] == p and pkg_of_tag[c[0]] == pkg for c in cabling)][0]
        alive = [p for p in ps if p != dead][rng.randrange(len(ps) - 1)]
        span = (f1 - f0).days
        day = f0 + dt.timedelta(days=1 + rng.randrange(0, max(1, span - 9)))
        fail_at = dt.datetime.combine(day, dt.time(rng.randrange(7, 15), rng.randrange(0, 60)))
        recable_at = (fail_at + dt.timedelta(hours=rng.uniform(20, 52))).replace(second=0, microsecond=0)
        logged_at = dt.datetime.combine(recable_at.date() + dt.timedelta(days=rng.randint(1, 6)),
                                        dt.time(rng.randrange(14, 18), rng.randrange(0, 60)))
        moved = sorted(c[0] for c in cabling if c[1] == dead and c[3] is None)
        for c in cabling:
            if c[1] == dead and c[3] is None:
                c[3] = recable_at
        for t in moved:
            cabling.append([t, alive, recable_at, None])
        failures.append({"dead": dead, "alive": alive, "fail_at": fail_at, "recable_at": recable_at,
                         "logged_at": logged_at, "loc": loc, "tags": moved, "booking": ref})
    A.failures = failures
    # a hall refurbishment: Wilgenhof's screens come down on 19 October, the player is removed from the system
    refurb_day = dt.date(2026, 10, 19)
    taken = [s for s in screens if s.loc == "WLH-H"]
    for s in taken:
        s.down = dt.datetime.combine(refurb_day, dt.time(5, 10))
    A.refurb = ("WLH-H", refurb_day)
    for c in cabling:
        if c[0] in {s.tag for s in taken} and c[3] is None:
            c[3] = dt.datetime.combine(refurb_day, dt.time(5, 10))
    # the register's copy of the cabling: a re-cabling is entered when its work order is closed
    relog = {f["recable_at"]: f["logged_at"] for f in failures}
    A.cabling_register = [[t, p, relog.get(a, a), relog.get(b, b) if b is not None else None]
                          for t, p, a, b in cabling]
    A.cabling = cabling
    # ------------------------------------------------------------ health: offline spells per player (local)
    spells = []          # (player, start local, end local or None)
    t0 = dt.datetime.combine(P.EXTRACT_START, dt.time(0, 0))
    t1 = dt.datetime.combine(P.EXTRACT_END + dt.timedelta(days=1), dt.time(0, 0))
    span_h = (t1 - t0).total_seconds() / 3600
    removed = {c[1] for c in cabling if c[0] in {s.tag for s in taken}}
    for p in sorted(players):
        n = min(8, int(rng.expovariate(1 / 3.4)))
        for _ in range(n):
            st = t0 + dt.timedelta(hours=rng.uniform(0, span_h))
            st = st.replace(second=0, microsecond=0)
            dur = math.exp(rng.gauss(math.log(2.4), 1.1))
            dur = min(max(dur, 0.25), 42.0)
            en = (st + dt.timedelta(hours=dur)).replace(second=0, microsecond=0)
            if any(f["alive"] == p and st < f["logged_at"] + dt.timedelta(days=1) and
                   en > f["fail_at"] - dt.timedelta(days=1) for f in failures):
                continue      # the receiving player stayed up around the job
            spells.append((p, st, en))
    for f in failures:
        spells.append((f["dead"], f["fail_at"], None))      # the dead player never reports again
    # the removed player's last report is the morning of the refurbishment; nothing after
    A.removed_players = removed
    spells = [s for s in spells if not (s[0] in removed and s[1] >= dt.datetime.combine(refurb_day, dt.time(5, 0)))]
    spells.sort(key=lambda s: (s[1], s[0]))
    # merge overlapping spells of one player
    merged = {}
    for p, st, en in spells:
        merged.setdefault(p, []).append([st, en])
    out = []
    for p, lst in merged.items():
        lst.sort(key=lambda x: x[0])
        cur = None
        for st, en in lst:
            if cur is None:
                cur = [st, en]
            elif cur[1] is None or st <= cur[1]:
                if cur[1] is not None and (en is None or en > cur[1]):
                    cur[1] = en
            else:
                out.append((p, cur[0], cur[1]))
                cur = [st, en]
        out.append((p, cur[0], cur[1]))
    out.sort(key=lambda s: (s[1], s[0]))
    A.spells = out
    A.cms = cms_events(A, t0, t1)
    return A


def displays(A, p, when):
    return sum(1 for t, pp, a, b in A.cabling if pp == p and a <= when and (b is None or when < b))


def cms_events(A, t0, t1):
    """The content system's log in local time: a player going offline and back online (reporting the displays it
    drives when it comes back), and a change in the displays a running player drives (a re-cabling, or a screen
    unplugged for a few minutes during the night cleaning)."""
    rng = A.rng
    ev = []
    for p, st, en in A.spells:
        ev.append((st, p, "OFFLINE", ""))
        if en is not None:
            ev.append((en, p, "ONLINE", displays(A, p, en)))
    for f in A.failures:
        ev.append((f["recable_at"], f["alive"], "DISPLAYS",
                   displays(A, f["alive"], f["recable_at"])))
    removed_after = dt.datetime.combine(A.refurb[1], dt.time(5, 0))
    for p in sorted(A.removed_players):       # the screens unplugged and taken down; the player is then removed
        ev.append((dt.datetime.combine(A.refurb[1], dt.time(5, 10)), p, "DISPLAYS", 0))
    busy = {}
    for p, st, en in A.spells:
        busy.setdefault(p, []).append((st - dt.timedelta(hours=1), (en or t1) + dt.timedelta(hours=1)))
    for f in A.failures:
        busy.setdefault(f["alive"], []).append((f["fail_at"] - dt.timedelta(days=1), f["logged_at"] + dt.timedelta(days=1)))
        busy.setdefault(f["dead"], []).append((f["fail_at"] - dt.timedelta(hours=2), t1))
    for p in sorted(A.players):
        if p in A.removed_players:
            busy.setdefault(p, []).append((removed_after - dt.timedelta(hours=2), t1))
        for _ in range(rng.choice((0, 0, 1, 1, 2, 3))):
            night = t0.date() + dt.timedelta(days=rng.randrange(0, (t1 - t0).days - 1))
            a = dt.datetime.combine(night, dt.time(1, 0)) + dt.timedelta(minutes=rng.randrange(0, 210))
            b = a + dt.timedelta(minutes=rng.randrange(5, 75))
            if any(x < b and a < y for x, y in busy.get(p, ())):
                continue
            k = displays(A, p, a)
            if k < 1:
                continue
            ev.append((a, p, "DISPLAYS", k - 1))
            ev.append((b, p, "DISPLAYS", k))
            busy.setdefault(p, []).append((a - dt.timedelta(hours=1), b + dt.timedelta(hours=1)))
    ev.sort(key=lambda e: (e[0], e[1], e[2]))
    return ev


def player_of(A, tag, when):
    for t, p, a, b in A.cabling:
        if t == tag and a <= when and (b is None or when < b):
            return p
    return None


def dark_hours(A, tag, f0, f1, how="golden"):
    """Hours the screen was dark within station opening hours from f0 to f1 (dates, inclusive).
    golden: the player cabled to the screen at each moment, and the screen not hanging after it came down."""
    s = {x.tag: x for x in A.screens}[tag]
    total = 0.0
    day = f0
    while day <= f1:
        o0, o1 = opening(day)
        # not hanging
        if s.down is not None and s.down < o1:
            total += overlap_hours(o0, o1, max(o0, s.down), o1)
            o1 = min(o1, s.down) if s.down > o0 else o0
        if o1 > o0:
            for p, st, en in A.spells:
                en2 = en or dt.datetime(2027, 1, 1)
                if en2 <= o0 or st >= o1:
                    continue
                # pieces of the spell during which this player drove this screen
                for t, pp, a, b in A.cabling:
                    if t != tag or pp != p:
                        continue
                    b2 = b or dt.datetime(2027, 1, 1)
                    lo, hi = max(st, a, o0), min(en2, b2, o1)
                    if lo < hi:
                        total += (hi - lo).total_seconds() / 3600.0
        day += dt.timedelta(days=1)
    return total


# ---------------------------------------------------------------- bookings and billing
ADVERTISERS = [
    ("Duinvalk Zorgverzekeraar", "Windroos Media"), ("Brouwerij De Ravel", None), ("Klaverstad Makelaars", None),
    ("Polderlicht Energie", "Noordlicht Mediaplanning"), ("Stadsschouwburg Ravelmond", None),
    ("Hoogland Opleidingen", "Windroos Media"), ("Belzo Mobiel", "Bureau Overdiep"),
    ("Kaasmakerij Ten Haeve", "Bureau Overdiep"), ("Ravelmondse Tandartsen", "Noordlicht Mediaplanning"),
    ("Fietsmakerij Velo Oost", "Bureau Overdiep"),
]
AGENCY_RATE = {"Windroos Media": 0.135, "Noordlicht Mediaplanning": 0.125, "Bureau Overdiep": 0.175}
BOOKINGS = [
    # ref, advertiser index, package, flight start, flight end, net price per screen-week (EUR)
    ("SB-26-0411", 0, "OVP", (10, 5), (11, 1), 236.7),
    ("SB-26-0414", 1, "CEN", (10, 5), (10, 18), 262.0),
    ("SB-26-0415", 2, "NRD", (10, 5), (11, 1), 140.5),
    ("SB-26-0419", 3, "OST", (10, 12), (11, 1), 150.6),
    ("SB-26-0422", 4, "BNS", (10, 5), (10, 25), 173.9),
    ("SB-26-0424", 5, "ZDT", (10, 5), (11, 1), 145.2),
    ("SB-26-0429", 6, "CEN", (10, 19), (11, 1), 265.7),
    ("SB-26-0430", 7, "WST", (10, 12), (10, 25), 116.7),
    ("SB-26-0434", 8, "RNG", (10, 5), (11, 1), 107.4),
    ("SB-26-0437", 9, "EIN", (10, 5), (11, 1), 126.5),
]
MAKE_GOOD_ALLOWANCE = 0.005


def bookings(A):
    out = []
    for ref, ai, pkg, (m0, d0), (m1, d1), price in BOOKINGS:
        f0, f1 = dt.date(2026, m0, d0), dt.date(2026, m1, d1)
        tags = sorted(s.tag for s in A.screens if s.pkg == pkg and s.hung <= f0 and (s.down is None or s.down.date() > f0))
        hours = 0.0
        day = f0
        while day <= f1:
            o0, o1 = opening(day)
            hours += (o1 - o0).total_seconds() / 3600.0
            day += dt.timedelta(days=1)
        booked = round(hours * len(tags), 2)
        weeks = ((f1 - f0).days + 1) / 7.0
        adv, agency = ADVERTISERS[ai]
        out.append({"ref": ref, "advertiser": adv, "agency": agency, "package": pkg, "start": f0, "end": f1,
                    "tags": tags, "booked_hours": booked, "weeks": weeks,
                    "net_value": round(price * len(tags) * weeks, 2)})
    A.bookings = out
    return out


def make_good(A, b, dark_fn=None):
    dark = sum((dark_fn or dark_hours)(A, t, b["start"], b["end"]) for t in b["tags"])
    allowance = MAKE_GOOD_ALLOWANCE * b["booked_hours"]
    return dark, max(0, math.ceil(round(dark - allowance, 6))) if dark > allowance else 0


VAT = 0.21
CREDITS = [
    # booking ref, share of the booking's net value credited, the reason line, issued after the flight's last week
    ("SB-26-0415", 0.18, "Prijsaanpassing schermen Wilgenhof (renovatie stationshal vanaf 19-10)", False),
    ("SB-26-0414", 0.10, "Correctie tarief Centraal najaar", False),
    ("SB-26-0437", 0.25, "Gedeeltelijke annulering week 44", True),
    ("SB-26-0422", 0.12, "Compensatie storing Overstap Centraal oktober", False),
    ("SB-26-0424", 0.15, "Compensatie uitval schermen Zuidtak oktober", True),
    ("SB-26-0434", 0.20, "Compensatie Ringlijn oktober, afspraak accountmanager", True),
]
OTHER_DEBTORS = ["Windroos Media", "Noordlicht Mediaplanning", "Bureau Overdiep", "Gemeente Ravelmond",
                 "Hogeschool Ravelmond", "Autobedrijf Van Deursen", "Zorggroep Ravelstroom", "Bakkerij Meijerhof",
                 "Stichting Museum Ravelmond", "Ravelmond Marketing", "Brouwerij De Ravel", "Klaverstad Makelaars",
                 "Woonstichting Kanaalzone", "Sportschool Ravelfit", "Optiek Verhagen", "Belzo Mobiel"]


def billing(A):
    """Invoices in two billing systems (the legacy system to 14 October, the new system from 15 October), credit
    notes in the new system, and each agency's commission statement of 31 October."""
    rng = A.rng
    legacy, new, credits = [], [], []
    inv_of = {}
    # the year's other bookings (before and after the autumn flights) as they appear in the two systems
    early = []
    ref_no = 3
    day = dt.date(2026, 1, 6)
    while day < dt.date(2026, 10, 1):
        day += dt.timedelta(days=rng.randrange(1, 5))
        ref_no += rng.randrange(1, 5)
        if ref_no >= 410:
            break
        net = round(rng.uniform(900, 11500), 2)
        early.append({"date": day, "ref": "SB-26-%04d" % ref_no, "debtor": rng.choice(OTHER_DEBTORS), "net": net})
    pend = []
    for b in A.bookings:
        if b["start"] >= dt.date(2026, 10, 19):
            issued = b["start"] - dt.timedelta(days=rng.randrange(2, 5))
        else:
            issued = b["start"] - dt.timedelta(days=rng.randrange(8, 16))
        pend.append({"date": issued, "ref": b["ref"], "debtor": b["agency"] or b["advertiser"], "net": b["net_value"]})
    later_ref = 441
    day = dt.date(2026, 10, 16)
    while day < dt.date(2026, 11, 12):
        day += dt.timedelta(days=rng.randrange(1, 4))
        if day > dt.date(2026, 11, 12):
            break
        pend.append({"date": day, "ref": "SB-26-%04d" % later_ref, "debtor": rng.choice(OTHER_DEBTORS),
                     "net": round(rng.uniform(1200, 9800), 2)})
        later_ref += rng.randrange(1, 3)
    allinv = sorted(early + pend, key=lambda x: (x["date"], x["ref"]))
    seq_l = 4000 + rng.randrange(0, 40)
    seq_n = 100300 + rng.randrange(0, 200)
    for x in allinv:
        vat = round(x["net"] * VAT, 2)
        if x["date"] < dt.date(2026, 10, 15):
            seq_l += rng.randrange(1, 4)
            no = "SBM-2026-%05d" % seq_l
            legacy.append({"no": no, "date": x["date"], "ref": x["ref"], "debtor": x["debtor"],
                           "gross": round(x["net"] + vat, 2)})
        else:
            seq_n += rng.randrange(5, 40)
            no = "F%d" % seq_n
            new.append({"no": no, "date": x["date"], "ref": x["ref"], "debtor": x["debtor"], "kind": "factuur",
                        "net": x["net"], "vat": vat, "reference": ""})
        inv_of[x["ref"]] = no
    A.invoice_net = {x["ref"]: x["net"] for x in allinv}
    crs = []
    for ref, share, why, after in CREDITS:
        b = [x for x in A.bookings if x["ref"] == ref][0]
        if after:      # settled once the flight is over
            date = b["end"] + dt.timedelta(days=rng.randrange(1, 4))
        else:
            date = max(dt.date(2026, 10, 15), b["start"]) + dt.timedelta(days=rng.randrange(3, 12))
        crs.append((date, ref, round(-b["net_value"] * share, 2), why, b["agency"] or b["advertiser"]))
    # two credit notes on summer bookings, settled in the new system against their legacy invoices
    for x in rng.sample([e for e in early if dt.date(2026, 6, 1) <= e["date"] <= dt.date(2026, 9, 15)], 2):
        crs.append((dt.date(2026, 10, 15) + dt.timedelta(days=rng.randrange(2, 20)), x["ref"],
                    round(-x["net"] * rng.choice((0.1, 0.15, 0.2)), 2), "Correctie facturatie zomercampagne", x["debtor"]))
    crs.sort()
    for date, ref, net, why, debtor in crs:
        seq_n += rng.randrange(5, 40)
        credits.append({"no": "C%d" % seq_n, "date": date, "ref": "", "debtor": debtor, "kind": "creditnota",
                        "net": net, "vat": round(net * VAT, 2), "reference": inv_of[ref], "why": why, "booking": ref})
    A.legacy, A.new_invoices, A.credits, A.inv_of = legacy, new, credits, inv_of
    # each agency's statement of 31 October: commission at its own rate on the net invoiced value of its autumn
    # bookings, less the credit notes issued by then
    stm = []
    sdate = dt.date(2026, 10, 31)
    for ag in sorted(AGENCY_RATE):
        bs = [b for b in A.bookings if b["agency"] == ag]
        refs = {b["ref"] for b in bs}
        base = sum(b["net_value"] for b in bs) + sum(c["net"] for c in credits if c["booking"] in refs and c["date"] <= sdate)
        stm.append({"agency": ag, "base": round(base, 2), "commission": round(base * AGENCY_RATE[ag], 2),
                    "bookings": len(bs), "date": sdate})
    A.statements = stm
    return A


def net_revenue(A):
    """Net revenue per package: invoiced value excluding VAT, less credit notes, less the agency commission due
    at the agency's contract rate on the value net of credit notes (terms 8.2 and 8.3)."""
    per_booking = {}
    for b in A.bookings:
        cr = sum(c["net"] for c in A.credits if c["booking"] == b["ref"])
        per_booking[b["ref"]] = b["net_value"] + cr
    comm = {}
    for b in A.bookings:
        if b["agency"]:
            comm[b["ref"]] = AGENCY_RATE[b["agency"]] * per_booking[b["ref"]]
    out = {}
    for b in A.bookings:
        out[b["package"]] = out.get(b["package"], 0.0) + per_booking[b["ref"]] - comm.get(b["ref"], 0.0)
    return out


# ---------------------------------------------------------------- the register after the window (for 2027 sales)
def register_rows(A):
    """The screen register as the screen operations team keeps it: one row per hanging of a screen (asset tag,
    place, position, package, hung, taken down, status). A screen moved to another place gets a new row and its
    old row is not always closed; a refurbished hall's screens are re-hung under new asset tags while the old
    tags stay open. Returns rows and the truth of what hangs on 1 January 2027 by package."""
    rng = A.rng
    rows = []
    for s in A.screens:
        rows.append({"tag": s.tag, "loc": s.loc, "pos": s.pos, "pkg": s.pkg, "hung": s.hung,
                     "down": s.down.date() if s.down else None, "status": "verwijderd" if s.down else "in bedrijf"})
    tags = {s.tag for s in A.screens}

    def new_tag():
        while True:
            t = "SB%05d" % rng.randrange(10000, 99999)
            if t not in tags:
                tags.add(t)
                return t
    # 1. the supplier's 2026 replacement programme swapped the screens of eight halls and passages for new units
    #    from 3 to 5 November; the new units came in under new tags and the old tags' rows were never closed
    swap = {"CEN-HZ": 3, "KNO-H": 3, "HDH-OV": 4, "STP-H": 4, "MZT-H": 4, "TWB-H": 5, "VLH-H": 5, "OSE-H": 5}
    kno = [r for r in rows if r["loc"] in swap and r["down"] is None]
    for r in kno:
        rows.append({"tag": new_tag(), "loc": r["loc"], "pos": r["pos"], "pkg": r["pkg"],
                     "hung": dt.date(2026, 11, swap[r["loc"]]), "down": None, "status": "in bedrijf"})
    A.retagged = [r["pos"] for r in kno]
    # 2. screens moved between halls in November (same tag, a new row; the old row left open on two of three)
    movers = []
    for src in ("TNS-H", "ZDV-H", "HTM-H"):
        cand = [r for r in rows if r["loc"] == src and r["down"] is None]
        if cand:
            movers.append(cand[0])
    moves = []
    dests = {"TNS-H": ("SPL-H", "RNG"), "ZDV-H": ("UNI-H", "ZDT"), "HTM-H": ("KST-H", None)}
    for i, r in enumerate(movers):
        dest, pkg = dests[r["loc"]]
        if pkg is None:   # moved out of the packages to a hall no package lists (Kaaistraat), held for 2027
            pkg = "-"
        day = dt.date(2026, 11, 9 + 2 * i)
        rows.append({"tag": r["tag"], "loc": dest, "pos": "%s-M%02d" % (dest, 10 + i),
                     "pkg": pkg, "hung": day, "down": None, "status": "in bedrijf"})
        if i == 1:
            r["down"] = day
            r["status"] = "verplaatst"
        moves.append((r["tag"], r["loc"], dest, day))
    A.moves = moves
    # 3. planned: new screens in December at Universiteit and Oosterpoort; Zoutpannen's old screens out on 14 December;
    #    Wilgenhof's screens back on 1 February 2027
    for loc, pkg, k in (("UNI-H", "ZDT", 2), ("OSP-H", "OST", 3), ("TRV-H", "NRD", 2), ("NOP-H", "EIN", 1)):
        for i in range(k):
            rows.append({"tag": new_tag(), "loc": loc, "pos": "%s-N%02d" % (loc, 20 + i),
                         "pkg": pkg, "hung": dt.date(2026, 12, 7 + i), "down": None, "status": "gepland"})
    for r in rows:
        if r["loc"] in ("ZTP-H", "WSK-H") and r["down"] is None and r["hung"] < dt.date(2026, 11, 1):
            r["down"] = dt.date(2026, 12, 14) if r["loc"] == "ZTP-H" else dt.date(2026, 12, 21)
            r["status"] = "in bedrijf"      # the take-down is booked, the screen still hangs today
    for s in A.screens:
        if s.loc == "WLH-H":
            rows.append({"tag": new_tag(), "loc": "WLH-H", "pos": s.pos, "pkg": s.pkg,
                         "hung": dt.date(2027, 2, 1), "down": None, "status": "gepland"})
    A.register = rows
    # truth on 1 January 2027: each tag's latest hanging on or before the date, still up; one screen per position
    day = dt.date(2027, 1, 1)
    latest = {}
    for r in rows:
        if r["hung"] <= day:
            if r["tag"] not in latest or r["hung"] > latest[r["tag"]]["hung"]:
                latest[r["tag"]] = r
    up = [r for r in latest.values() if (r["down"] is None or r["down"] > day) and r["pkg"] != "-"]
    by_pos = {}
    for r in up:
        k = (r["loc"], r["pos"])
        if k not in by_pos or r["hung"] > by_pos[k]["hung"]:
            by_pos[k] = r
    count = {}
    for r in by_pos.values():
        count[r["pkg"]] = count.get(r["pkg"], 0) + 1
    A.screens_2027 = {code: count.get(code, 0) for code in P.PACKAGE_ORDER}
    return rows
