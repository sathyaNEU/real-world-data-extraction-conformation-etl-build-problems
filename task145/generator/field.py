"""The asks' world, fiscal 2025-26 (April 2025 to March 2026): the brokerage desks' staff and their moves between desks,
every shift and overtime segment they worked, call-backs, and the contract broker Brandmoor's transmissions and monthly
statements. Nothing here is read by the main call."""
from __future__ import annotations

import datetime as dt
import math
from dataclasses import dataclass, field

import numpy as np

import common as K

TA_START = dt.date(2025, 4, 1)
TA_LEGACY_END = dt.date(2025, 10, 31)
TA_NEW_FROM = dt.date(2025, 10, 27)        # the migration carried the open timecards of 27 to 31 October
TA_END = dt.date(2026, 9, 30)
TA_LEGACY_PULL = dt.date(2025, 10, 31)
TA_NEW_PULL = dt.date(2026, 10, 6)
HR_PULL = dt.date(2026, 10, 6)


@dataclass
class Staff:
    k: int
    first: str
    last: str
    legacy_id: str
    emp_no: str
    position: str
    licence: str
    hired: dt.date
    left: dt.date | None
    desks: list = field(default_factory=list)       # [(from_date, desk)] in order
    ot_rate: float = 1.0
    cb_rate: float = 1.0

    def desk_on(self, d):
        cur = None
        for f, g in self.desks:
            if f <= d:
                cur = g
        return cur


@dataclass
class TALine:
    emp: int
    day: dt.date
    code: str                   # REG, OT15, OT20, CB, VAC, SCK, TRN, STAT
    hours: float                # hours the line pays
    t_in: dt.datetime | None
    t_out: dt.datetime | None
    worked: float               # hours between the punches (call-back: the time worked)


# ---------------------------------------------------------------------------------------------------- staff
# desk, position, (move date, new desk) or None; the seven movers of the year and the months after it
ROSTER = [
    ("YYZ", "Senior Customs Broker", None), ("YYZ", "Senior Customs Broker", None), ("YYZ", "Customs Broker", None),
    ("YYZ", "Customs Broker", (dt.date(2025, 10, 20), "YWG")), ("YYZ", "Customs Broker", (dt.date(2026, 5, 18), "YUL")),
    ("YYZ", "Customs Broker", None), ("YYZ", "Broker Trainee", None),
    ("YUL", "Senior Customs Broker", None), ("YUL", "Customs Broker", None),
    ("YUL", "Customs Broker", (dt.date(2025, 9, 1), "YYZ")), ("YUL", "Customs Broker", None),
    ("YUL", "Broker Trainee", None),
    ("YVR", "Senior Customs Broker", None), ("YVR", "Senior Customs Broker", None),
    ("YVR", "Customs Broker", (dt.date(2025, 7, 14), "YYC")), ("YVR", "Customs Broker", None),
    ("YVR", "Customs Broker", None), ("YVR", "Broker Trainee", None),
    ("YYC", "Senior Customs Broker", None), ("YYC", "Customs Broker", (dt.date(2026, 1, 12), "YVR")),
    ("YYC", "Customs Broker", None),
    ("YWG", "Senior Customs Broker", None), ("YWG", "Customs Broker", (dt.date(2025, 9, 29), "YUL")),
    ("YWG", "Customs Broker", (dt.date(2026, 6, 2), "YYC")),
]
# a departure and two hires inside the year
LEAVERS = {8: dt.date(2026, 2, 13)}                 # a Dorval broker leaves in February 2026
JOINERS = [("YWG", "Broker Trainee", dt.date(2025, 8, 18)), ("YYZ", "Customs Broker", dt.date(2026, 3, 2))]

TIME_STREAM = 218
OT_INTENSITY = {"YYZ": 1.00, "YUL": 1.18, "YVR": 0.86, "YYC": 1.22, "YWG": 0.80}
SEASON_OT = {4: 0.85, 5: 0.90, 6: 0.95, 7: 0.85, 8: 0.90, 9: 1.00, 10: 1.10, 11: 1.35, 12: 1.30, 1: 0.95, 2: 0.95,
             3: 1.05}


def names(n):
    from faker import Faker
    out, firsts, lasts = [], set(), set()
    pools = [("en_CA", Faker("en_CA")), ("fr_CA", Faker("fr_CA"))]
    for _, f in pools:
        f.seed_instance(K.SEED + 3)
    i = 0
    while len(out) < n:
        loc, f = pools[0] if i % 3 else pools[1]
        i += 1
        first, last = f.first_name(), f.last_name()
        if first in firsts or last in lasts or " " in last:
            continue
        if first in {"Laura", "Robin", "Wanda", "Brian", "Clémence", "Theresa"} or \
                last in {"Parks", "Larson", "Armstrong", "Stewart", "Sirois", "Rowe"}:
            continue
        firsts.add(first)
        lasts.add(last)
        out.append((first, last))
    return out


def build_staff():
    r = K.rng("staff")
    nm = names(len(ROSTER) + len(JOINERS))
    staff = []
    used_leg, used_new = set(), set()

    def ids():
        while True:
            a = "E%05d" % int(r.integers(10000, 69999))
            b = "LX%06d" % int(r.integers(100000, 899999))
            if a not in used_leg and b not in used_new:
                used_leg.add(a)
                used_new.add(b)
                return a, b
    for k, (g, pos, move) in enumerate(ROSTER):
        a, b = ids()
        hired = dt.date(2008, 1, 7) + dt.timedelta(days=int(r.integers(0, 5600)))
        if pos == "Broker Trainee":
            hired = dt.date(2024, 9, 3) + dt.timedelta(days=int(r.integers(0, 200)))
        lic = "" if pos == "Broker Trainee" else "CB%05d" % int(r.integers(10000, 39999))
        desks = [(dt.date(2000, 1, 1), g)]
        if move:
            desks.append(move)
        s = Staff(k=k, first=nm[k][0], last=nm[k][1], legacy_id=a, emp_no=b, position=pos, licence=lic, hired=hired,
                  left=LEAVERS.get(k), desks=desks, ot_rate=float(np.exp(r.normal(0, 0.22))),
                  cb_rate=float(np.exp(r.normal(0, 0.30))))
        if move:
            s.ot_rate *= 1.35          # the movers are the desks' busiest brokers, sent where the work was
        staff.append(s)
    for j, (g, pos, d) in enumerate(JOINERS):
        k = len(ROSTER) + j
        a, b = ids()
        lic = "" if pos == "Broker Trainee" else "CB%05d" % int(r.integers(10000, 39999))
        staff.append(Staff(k=k, first=nm[k][0], last=nm[k][1], legacy_id=a, emp_no=b, position=pos, licence=lic,
                           hired=d, left=None, desks=[(d, g)], ot_rate=float(np.exp(r.normal(0, 0.22))),
                           cb_rate=float(np.exp(r.normal(0, 0.30)))))
    return staff


def employed(s, d):
    return s.hired <= d and (s.left is None or d < s.left)


# ---------------------------------------------------------------------------------------------------- time
def shift_start(s, d):
    """Desk shifts: day 06:00, mid 10:00, late 14:00; each broker on one rota, weeks alternating."""
    rota = (s.k + d.isocalendar()[1]) % 3
    return [6, 10, 14][rota]


def simulate_time(staff, holidays):
    r = K.rng("time", TIME_STREAM)
    lines = []
    day = TA_START
    while day <= TA_END:
        for s in staff:
            if not employed(s, day):
                continue
            g = s.desk_on(day)
            if g is None:
                continue
            wd = day.weekday()
            hol = day in holidays
            if hol and wd < 5:
                lines.append(TALine(s.k, day, "STAT", 7.5, None, None, 0.0))
                continue
            sat_rota = (s.k + day.isocalendar()[1]) % 4 == 0
            works = wd < 5 or (wd == 5 and sat_rota)
            if wd == 5 and not sat_rota:
                works = False
            if wd == 6:
                works = False
            if not works:
                # a Saturday overtime shift when the desk is busy
                if wd == 5 and r.random() < 0.10 * OT_INTENSITY[g] * SEASON_OT[day.month] * s.ot_rate:
                    h = float(r.choice([4.0, 5.0, 6.0, 7.5]))
                    t0 = dt.datetime.combine(day, dt.time(8, 0))
                    lines.append(TALine(s.k, day, "OT15", h, t0, t0 + dt.timedelta(hours=h), h))
                continue
            if wd == 5 and sat_rota and r.random() < 0.5:
                pass
            # leave
            u = r.random()
            if u < 0.035:
                lines.append(TALine(s.k, day, "VAC", 7.5, None, None, 0.0))
                continue
            if u < 0.047:
                lines.append(TALine(s.k, day, "SCK", 7.5, None, None, 0.0))
                continue
            st = shift_start(s, day)
            t_in = dt.datetime.combine(day, dt.time(st, 0)) + dt.timedelta(minutes=int(r.integers(-6, 7)))
            t_out = t_in + dt.timedelta(hours=8)          # 7.5 paid, a 30-minute meal break
            code = "TRN" if (s.position == "Broker Trainee" and r.random() < 0.06) else "REG"
            lines.append(TALine(s.k, day, code, 7.5, t_in, t_out, 7.5))
            # overtime straight after the shift
            p_ot = 0.16 * OT_INTENSITY[g] * SEASON_OT[day.month] * s.ot_rate
            if r.random() < p_ot:
                mins = int(r.choice([30, 45, 60, 75, 90, 105, 120, 150, 180, 210, 240, 270],
                                    p=[.12, .09, .14, .08, .12, .07, .12, .07, .08, .05, .04, .02]))
                mins += 3 * int(r.integers(-1, 2))      # the legacy clock keeps hundredths of an hour exact
                h = round(mins / 60.0, 2)
                o_in = t_out
                o_out = t_out + dt.timedelta(minutes=mins)
                if h > 3.5:
                    lines.append(TALine(s.k, day, "OT15", 3.5, o_in, o_in + dt.timedelta(hours=3.5), 3.5))
                    lines.append(TALine(s.k, day, "OT20", round(h - 3.5, 4), o_in + dt.timedelta(hours=3.5), o_out,
                                        round(h - 3.5, 4)))
                else:
                    lines.append(TALine(s.k, day, "OT15", round(h, 4), o_in, o_out, round(h, 4)))
            # a call-back in the evening: paid at least three hours
            if s.position != "Broker Trainee" and r.random() < 0.022 * OT_INTENSITY[g] * SEASON_OT[day.month] * s.cb_rate:
                worked = int(r.choice([35, 50, 65, 80, 100, 125, 150, 205], p=[.16, .18, .18, .14, .12, .10, .07, .05]))
                c_in = dt.datetime.combine(day, dt.time(int(r.integers(19, 23)), int(r.integers(0, 60))))
                c_out = c_in + dt.timedelta(minutes=worked)
                h = worked / 60.0
                lines.append(TALine(s.k, day, "CB", max(3.0, round(h, 4)), c_in, c_out, round(h, 4)))
        day += dt.timedelta(days=1)
    return lines


def round_quarter(t):
    """The new time and attendance system rounds every punch to the nearest quarter hour."""
    base = t.replace(minute=0, second=0, microsecond=0)
    q = int(math.floor((t.minute + t.second / 60.0) / 15.0 + 0.5))
    return base + dt.timedelta(minutes=15 * q)


def apply_new_system(lines):
    """From 1 November 2025 the new system records the punches rounded to the quarter hour and pays an overtime
    segment or a call-back on the rounded punches; a call-back still pays at least three hours."""
    out = []
    for ln in lines:
        if ln.day >= K.TA_MIGRATION and ln.code in ("OT15", "OT20", "CB") and ln.t_in is not None:
            a, b = round_quarter(ln.t_in), round_quarter(ln.t_out)
            if b <= a:
                b = a + dt.timedelta(minutes=15)
            w = (b - a).total_seconds() / 3600.0
            paid = max(3.0, w) if ln.code == "CB" else w
            out.append(TALine(ln.emp, ln.day, ln.code, paid, a, b, w))
        elif ln.day >= K.TA_MIGRATION and ln.code == "REG" and ln.t_in is not None:
            out.append(TALine(ln.emp, ln.day, ln.code, ln.hours, round_quarter(ln.t_in), round_quarter(ln.t_out),
                              ln.worked))
        else:
            out.append(ln)
    return out


# ---------------------------------------------------------------------------------------------------- Brandmoor
FEES = {2025: dict(std=18.40, ogd=27.60, rush=6.25, minimum=1850.00),
        2026: dict(std=19.10, ogd=28.65, rush=6.50, minimum=1900.00)}
TAX = {"YYZ": [("HST", 0.13)], "YUL": [("GST", 0.05), ("QST", 0.09975)], "YVR": [("GST", 0.05)],
       "YYC": [("GST", 0.05)], "YWG": [("GST", 0.05)]}
CLIENT_CODE = {"YYZ": "LXC-0411", "YUL": "LXC-0412", "YVR": "LXC-0415", "YYC": "LXC-0418", "YWG": "LXC-0419"}
OVERFLOW = {"YYZ": 265, "YUL": 190, "YVR": 165, "YYC": 170, "YWG": 125}       # entries a month at the season's mean
OVERFLOW_SEASON = {3: 0.75, 4: 0.55, 5: 0.40, 6: 0.65, 7: 0.30, 8: 0.50, 9: 0.95, 10: 1.40, 11: 2.10, 12: 1.95,
                   1: 0.85, 2: 0.45}


@dataclass
class BEntry:
    gw: str
    t: dt.datetime              # transmitted, Eastern time
    entry: str
    service: str                # STD or OGD
    rush: bool


@dataclass
class Statement:
    number: str
    gw: str
    month: tuple                # (y, m) of the transmissions it bills
    issued: dt.date
    entries: list
    std: int = 0
    ogd: int = 0
    rush: int = 0
    std_rate: float = 0.0
    ogd_rate: float = 0.0
    rush_rate: float = 0.0
    minimum_adj: float = 0.0
    net: float = 0.0
    taxes: list = field(default_factory=list)
    total: float = 0.0
    reissue_of: str = ""
    credit_memo: tuple | None = None    # (number, date) reversing this statement
    portal_rates: tuple = ()


def first_business_day(y, m, holidays):
    d = dt.date(y, m, 1)
    while d.weekday() >= 5 or d in holidays:
        d += dt.timedelta(days=1)
    return d


BRANDMOOR_LAST = dt.date(2026, 8, 31)     # the last transmissions month billed by the AP register's end


def simulate_brandmoor(holidays):
    r = K.rng("brandmoor")
    entries = []
    seq = 7710000
    for (y, m) in K.months(dt.date(2025, 3, 1), BRANDMOOR_LAST):
        for g in K.GATEWAYS:
            lam = OVERFLOW[g] * OVERFLOW_SEASON[m] * math.exp(r.normal(0, 0.25))
            n = int(r.poisson(lam))
            for _ in range(n):
                d = dt.date(y, m, int(r.integers(1, K.days_in(y, m) + 1)))
                t = dt.datetime.combine(d, dt.time(int(r.integers(7, 23)), int(r.integers(0, 60))))
                seq += int(r.integers(1, 4))
                entries.append(BEntry(gw=g, t=t, entry="13947%09d" % (900000000 + seq),
                                      service="OGD" if r.random() < 0.11 else "STD", rush=bool(r.random() < 0.16)))
    entries.sort(key=lambda e: (e.t, e.gw))
    stmts = []
    num = 25041
    for (y, m) in K.months(dt.date(2025, 3, 1), BRANDMOOR_LAST):
        ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
        issued = first_business_day(ny, nm, holidays)
        for g in K.GATEWAYS:
            es = [e for e in entries if e.gw == g and (e.t.year, e.t.month) == (y, m)]
            if not es:
                continue
            fee = FEES[2026] if issued >= dt.date(2026, 2, 1) else FEES[2025]
            st = Statement(number="BCS-%d-%05d" % (ny, num), gw=g, month=(y, m), issued=issued, entries=es)
            num += int(r.integers(3, 9))
            st.std = sum(1 for e in es if e.service == "STD")
            st.ogd = sum(1 for e in es if e.service == "OGD")
            st.rush = sum(1 for e in es if e.rush)
            st.std_rate, st.ogd_rate, st.rush_rate = fee["std"], fee["ogd"], fee["rush"]
            charges = round(st.std * fee["std"] + st.ogd * fee["ogd"] + st.rush * fee["rush"], 2)
            # the client portal shows every line at the contract rate in force when it is viewed
            st.portal_rates = (FEES[2026]["std"], FEES[2026]["ogd"], FEES[2026]["rush"])
            st.minimum_adj = round(max(0.0, fee["minimum"] - charges), 2)
            st.net = round(charges + st.minimum_adj, 2)
            st.taxes = [(nme, round(st.net * rt, 2)) for nme, rt in TAX[g]]
            st.total = round(st.net + sum(v for _, v in st.taxes), 2)
            stmts.append(st)
    # Mississauga's statement for February 2026: 64 entries flagged rush in error, disputed, re-issued in March
    orig = [s for s in stmts if s.gw == "YYZ" and s.month == (2026, 2)][0]
    flagged = [e for e in orig.entries if not e.rush][:64]
    re = Statement(number=orig.number + "-R1", gw="YYZ", month=(2026, 2), issued=dt.date(2026, 3, 23),
                   entries=orig.entries, std=orig.std, ogd=orig.ogd, rush=orig.rush, std_rate=orig.std_rate,
                   ogd_rate=orig.ogd_rate, rush_rate=orig.rush_rate, reissue_of=orig.number,
                   portal_rates=orig.portal_rates)
    orig.rush = orig.rush + len(flagged)        # as first issued, with the erroneous rush flags
    fee = FEES[2026] if orig.issued >= dt.date(2026, 2, 1) else FEES[2025]
    ch_o = round(orig.std * fee["std"] + orig.ogd * fee["ogd"] + orig.rush * fee["rush"], 2)
    orig.minimum_adj = round(max(0.0, fee["minimum"] - ch_o), 2)
    orig.net = round(ch_o + orig.minimum_adj, 2)
    orig.taxes = [(n, round(orig.net * rt, 2)) for n, rt in TAX["YYZ"]]
    orig.total = round(orig.net + sum(v for _, v in orig.taxes), 2)
    ch_r = round(re.std * fee["std"] + re.ogd * fee["ogd"] + re.rush * fee["rush"], 2)
    re.minimum_adj = round(max(0.0, fee["minimum"] - ch_r), 2)
    re.net = round(ch_r + re.minimum_adj, 2)
    re.taxes = [(n, round(re.net * rt, 2)) for n, rt in TAX["YYZ"]]
    re.total = round(re.net + sum(v for _, v in re.taxes), 2)
    orig.credit_memo = ("BCM-2026-00118", dt.date(2026, 4, 6))
    stmts.append(re)
    return entries, stmts, flagged
