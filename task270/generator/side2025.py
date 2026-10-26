"""Gota Viva's 2025 campaign side of task270, which the asks read and the call never opens: the Portal do Dador's
booking extract for the sessions of 3 March to 29 June 2025, its extraction notes, and Meridiano Media's report on
the April 2025 youth campaign.

The new portal went live on 17 March 2025 with the old system's bookings and registrations imported, but not their
passwords. A person who had registered before the go-live and booked again in its first days often registered again:
a first-time donor under a second provisional number, and a regular donor who held a booking from the old system
under a provisional number of their own, which the portal took for someone who had never given blood. The encrypted
identity document they gave both times is the same, and nothing in the extract marks the second registration.

The extract joins each booking to its donor's record as the record stood on the day of the extraction: the donor
number, the donor's type and the date of the first donation are the record's values on 2 July 2025, so a person who
booked a first donation and gave it shows on that booking as a regular donor with a definitive number."""
import datetime as dt
import hashlib

import numpy as np

import common as K

START = dt.date(2025, 1, 20)                 # first day a booking in the extract can have been made
SESSIONS = (dt.date(2025, 3, 3), dt.date(2025, 6, 29))
GO_LIVE = dt.date(2025, 3, 17)
EXTRACTED = dt.date(2025, 7, 2)
CAMPAIGN = (dt.date(2025, 4, 7), dt.date(2025, 5, 4))
BASELINE = (dt.date(2025, 3, 10), dt.date(2025, 4, 6))
REPORT_DATE = dt.date(2025, 5, 30)
UNIVERSE_2025 = 2091000
REACH_2025 = [0.538, 0.371, 0.260, 0.183, 0.127]        # 1+ to 5+ among adults 18 to 34, the 2025 panel
SPOTS_2025 = 58
CENTRES = [("CS-PRT", "Porto", "Porto"), ("CS-BRG", "Braga", "Braga"), ("CS-VRL", "Vila Real", "Vila Real"),
           ("CS-AVR", "Aveiro", "Aveiro"), ("CS-CBR", "Coimbra", "Coimbra"), ("CS-VIS", "Viseu", "Viseu"),
           ("CS-LRA", "Leiria", "Leiria"), ("CS-LSB", "Lisboa", "Lisboa"), ("CS-STB", "Setúbal", "Setúbal"),
           ("CS-SNT", "Santarém", "Santarém"), ("CS-EVR", "Évora", "Évora"), ("CS-FAR", "Faro", "Faro")]
CENTRE_W = [0.17, 0.08, 0.03, 0.06, 0.08, 0.04, 0.05, 0.26, 0.08, 0.04, 0.04, 0.07]
CHANNELS = ["portal", "telefone", "presencial"]
FILE = "marcacoes_portal_dador_2025.csv"
NOTES = "notas_extracao_portal_dador.txt"
REPORT = "relatorio_campanha_jovens_2025.pdf"


def uplift(day):
    """first-donation bookings by adults under 35 above their usual level on a given day: the campaign's response
    builds over its first fortnight and fades over the month after it"""
    a, b = CAMPAIGN
    if day < a:
        return 0.0
    t = (day - a).days
    if day <= b:
        return 0.55 + 0.35 * min(1.0, t / 13)
    return 0.9 * np.exp(-(day - b).days / 9.0)


class Bookings:
    def __init__(self, seed=K.SEED):
        self.rng = np.random.default_rng(seed + 3000)
        self.people = []          # one per registration: the person behind it, their attributes, the record's state
        self.rows = []            # dicts, one per booking
        self._people_and_bookings()
        self._go_live()
        self._next_donations()
        self._records()
        self._ids()

    def _person(self, young, first):
        rng = self.rng
        if first:
            age = int(rng.integers(18, 35)) if young else int(rng.integers(35, 66))
        else:
            age = int(rng.integers(19, 35)) if young else int(rng.integers(35, 66))
        born = dt.date(2025 - age, 1, 1) + dt.timedelta(days=int(rng.integers(0, 365)))
        sex = "F" if rng.random() < (0.57 if first else 0.48) else "M"
        c = int(rng.choice(len(CENTRES), p=CENTRE_W))
        given = None
        if not first:
            # a regular donor's first donation, some day between their eighteenth birthday and the end of 2024
            adult = dt.date(born.year + 18, born.month, min(born.day, 28))
            given = adult + dt.timedelta(days=int(rng.integers(0, max(1, (dt.date(2024, 12, 31) - adult).days))))
        pid = len(self.people)
        self.people.append(dict(pid=pid, person=pid, first=first, born=born, sex=sex, centre=c,
                                district=CENTRES[c][2], since=None, given=given))
        return pid

    def _registration(self, pid, made):
        """the donor number a booking made on this day is made under: a provisional registration from before the
        go-live is usually not carried into the portal by its holder, who registers again"""
        p = self.people[pid]
        if not p["first"] or made < GO_LIVE or p["since"] is None or p["since"] >= GO_LIVE:
            if p["since"] is None:
                p["since"] = made
            return pid
        if p.get("new_reg") is None:
            if self.rng.random() < 0.82:
                q = dict(p, pid=len(self.people), since=made)
                self.people.append(q)
                p["new_reg"] = q["pid"]
            else:
                p["new_reg"] = pid
        return p["new_reg"]

    def _book(self, pid, made, hour, after=None):
        """one booking: the session one to five weeks on, at the person's centre; its outcome, and for a
        cancellation the day it was cancelled; a cancelled or missed first donation is often booked again, for a
        later session than the one given up"""
        rng, p = self.rng, self.people[pid]
        session = made + dt.timedelta(days=int(rng.integers(4, 36)))
        if after is not None and session <= after:
            session = after + dt.timedelta(days=int(rng.integers(1, 15)))
        if session < SESSIONS[0] or session > SESSIONS[1]:
            return None
        reg = self._registration(pid, made)
        fate = rng.random()
        state = "realizada" if fate < (0.66 if p["first"] else 0.84) else ("falta" if fate < 0.86 else "cancelada")
        row = dict(pid=reg, made=dt.datetime.combine(made, dt.time(0, 0)) + dt.timedelta(minutes=hour),
                   session=session, centre=p["centre"], state=state,
                   channel=CHANNELS[int(rng.choice(3, p=[0.71, 0.21, 0.08]))])
        self.rows.append(row)
        if state == "cancelada":
            again = made + dt.timedelta(days=int(rng.integers(1, max(2, (session - made).days))))
            p_again = 0.45
        elif state == "falta" and p["first"]:
            again = session + dt.timedelta(days=int(rng.integers(1, 15)))
            p_again = 0.37
        else:
            return row
        # at the go-live, people holding an old-system booking often cancelled it to book again in the portal
        if made < GO_LIVE <= session and state != "realizada":
            p_again = 0.6
        if rng.random() < p_again and again <= SESSIONS[1] - dt.timedelta(days=5):
            self._book(pid, max(again, made), int(np.clip(rng.normal(20 * 60, 160), 7 * 60, 24 * 60 - 1)),
                       after=session)
        return row

    def _people_and_bookings(self):
        rng = self.rng
        day = START
        while day <= SESSIONS[1]:
            wd = day.weekday()
            wk = [1.12, 1.08, 1.02, 1.0, 0.92, 0.84, 1.02][wd]
            for young, first, base, resp in ((True, True, 20.3, 1.0), (False, True, 13.0, 0.25),
                                             (True, False, 26.0, 0.0), (False, False, 88.0, 0.0)):
                lam = base * wk * (1.0 + resp * uplift(day)) * float(np.exp(rng.normal(0, 0.05)))
                for _ in range(int(rng.poisson(lam))):
                    pid = self._person(young, first)
                    # the time of day a booking is made: evenings for the portal, office hours for the phone
                    hour = int(np.clip(rng.normal(20.5 * 60, 150) if rng.random() < 0.7 else
                                       rng.normal(12 * 60, 140), 6 * 60, 24 * 60 - 1))
                    self._book(pid, day, hour)
            day += dt.timedelta(days=1)

    def _go_live(self):
        """the go-live: people holding an old-system booking for a session after 17 March who, in the portal's
        first days, cancelled it (or let it lapse) and booked again there; a first-time donor kept their own
        registration or opened a second one as above, a regular donor who could not reach their account opened a
        provisional registration of their own"""
        rng = self.rng
        for row in list(self.rows):
            p = self.people[row["pid"]]
            if row["made"].date() >= GO_LIVE or row["session"] < GO_LIVE + dt.timedelta(days=2):
                continue
            if row["state"] == "cancelada":
                continue
            young = (GO_LIVE.year - p["born"].year - ((GO_LIVE.month, GO_LIVE.day) <
                                                      (p["born"].month, p["born"].day))) <= 34
            if p["first"]:
                if rng.random() >= 0.38:
                    continue
                row["state"] = "cancelada"
                made = GO_LIVE + dt.timedelta(days=int(rng.integers(0, 12)))
                if made >= row["session"]:
                    continue
                reg = self._registration(p["person"], made)
            else:
                if rng.random() >= (0.12 if young else 0.06):
                    continue
                made = GO_LIVE + dt.timedelta(days=int(rng.integers(0, 12)))
                if made >= row["session"]:
                    continue
                row["state"] = "cancelada" if rng.random() < 0.7 else "falta"
                q = dict(p, pid=len(self.people), since=made, given=None)
                self.people.append(q)
                reg = q["pid"]
            fate = rng.random()
            self.rows.append(dict(pid=reg, made=dt.datetime.combine(made, dt.time(0, 0)) +
                                  dt.timedelta(minutes=int(np.clip(rng.normal(20 * 60, 160), 7 * 60, 24 * 60 - 1))),
                                  session=row["session"] + dt.timedelta(days=int(rng.integers(0, 15))),
                                  centre=row["centre"], state="realizada" if fate < 0.72 else
                                  ("falta" if fate < 0.9 else "cancelada"), channel="portal"))

    def _next_donations(self):
        """a first donation is often followed, three months on for a man and four for a woman, by a booking for the
        next one"""
        rng = self.rng
        firsts = {}
        for r in self.rows:
            p = self.people[r["pid"]]
            if p["first"] and r["state"] == "realizada" and (r["pid"] not in firsts or
                                                             r["session"] < firsts[r["pid"]]["session"]):
                firsts[r["pid"]] = r
        for pid in sorted(firsts):
            r = firsts[pid]
            if rng.random() >= 0.35:
                continue
            session = r["session"] + dt.timedelta(days=(90 if self.people[pid]["sex"] == "M" else 120) +
                                                  int(rng.integers(0, 30)))
            made = session - dt.timedelta(days=int(rng.integers(5, 31)))
            if session > SESSIONS[1] or made <= r["session"]:
                continue
            fate = rng.random()
            self.rows.append(dict(pid=pid, made=dt.datetime.combine(made, dt.time(0, 0)) +
                                  dt.timedelta(minutes=int(np.clip(rng.normal(19.5 * 60, 190), 7 * 60, 24 * 60 - 1))),
                                  session=session, centre=r["centre"], state="realizada" if fate < 0.86 else
                                  ("falta" if fate < 0.93 else "cancelada"),
                                  channel=CHANNELS[int(rng.choice(3, p=[0.74, 0.1, 0.16]))]))

    def _records(self):
        """each registration's record on the extraction day: a first donation turns a provisional number into a
        definitive one and records its day"""
        given = {}
        for r in self.rows:
            if self.people[r["pid"]]["given"] is None and r["state"] == "realizada":
                if r["pid"] not in given or r["session"] < given[r["pid"]]:
                    given[r["pid"]] = r["session"]
        for p in self.people:
            p["record"] = p["given"] if p["given"] is not None else given.get(p["pid"])

    def _ids(self):
        """booking numbers in order of creation; donor numbers as the record holds them on the extraction day:
        provisional for a registration that has not given blood, definitive once it has"""
        rng = np.random.default_rng(K.SEED + 3100)
        self.rows.sort(key=lambda r: (r["made"], r["pid"], r["session"]))
        for k, r in enumerate(self.rows):
            r["ref"] = "PD%07d" % (2051337 + k * 3 + int(rng.integers(0, 3)))
        used, self.donor = set(), {}
        for p in self.people:
            while True:
                x = ("D%07d" % int(rng.integers(1000000, 9999999))) if p["record"] else \
                    ("P%06d" % int(rng.integers(100000, 999999)))
                if x not in used:
                    break
            used.add(x)
            self.donor[p["pid"]] = x
        self.doc = {}
        for p in self.people:
            if p["person"] not in self.doc:
                self.doc[p["person"]] = hashlib.sha256(("gv-doc|%d" % p["person"]).encode()).hexdigest()[:16].upper()

    def table(self):
        head = ["id_marcacao", "criada_em", "canal", "id_dador", "documento_hash", "data_nascimento", "sexo",
                "distrito", "centro", "data_sessao", "tipo_dadiva", "data_primeira_dadiva", "estado"]
        out = []
        for r in self.rows:
            p = self.people[r["pid"]]
            out.append([r["ref"], r["made"].strftime("%Y-%m-%d %H:%M:%S"), r["channel"], self.donor[r["pid"]],
                        self.doc[p["person"]], p["born"].isoformat(), p["sex"], p["district"], CENTRES[r["centre"]][0],
                        r["session"].isoformat(), "regular" if p["record"] else "primeira",
                        p["record"].isoformat() if p["record"] else "", r["state"]])
        out.sort(key=lambda x: x[0])
        return head, out

    # ---------------------------------------------------------------- the truth the asks are scored on
    def first_bookings(self, by="person", drop_cancelled=False):
        """each first-time donor's (or each donor number's) earliest booking, the booking of a first donation, aged
        18 to 34 on the day it was made; a regular donor's booking under a second registration is no first donation"""
        first = {}
        for r in self.rows:
            p = self.people[r["pid"]]
            if not p["first"] or (drop_cancelled and r["state"] == "cancelada"):
                continue
            key = p["person"] if by == "person" else r["pid"]
            if key not in first or r["made"] < first[key][0]:
                first[key] = (r["made"], p["born"])
        out = []
        for key, (made, born) in first.items():
            d = made.date()
            age = d.year - born.year - ((d.month, d.day) < (born.month, born.day))
            if 18 <= age <= 34:
                out.append(d)
        return out


def weekly(days, start, weeks):
    counts = [0] * weeks
    for d in days:
        k = (d - start).days // 7
        if 0 <= k < weeks:
            counts[k] += 1
    return counts


def response(bk, by="person", drop_cancelled=False):
    """the 2025 campaign's response as the extract notes define it"""
    days = bk.first_bookings(by, drop_cancelled)
    base = weekly(days, BASELINE[0], 4)
    camp = weekly(days, CAMPAIGN[0], 4)
    avg = sum(base) / 4.0
    above = [c - avg for c in camp]
    reached3 = UNIVERSE_2025 * REACH_2025[2] / 1000.0
    return dict(base=base, avg=avg, camp=camp, above=above, extra=sum(above), reached3=reached3,
                per_thousand=sum(above) / reached3)
