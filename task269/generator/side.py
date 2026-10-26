"""The world beyond the call's own records: the detail of every gold-auditor session (its time, auditor, and the moment,
health care worker group and action of each moment), the night sessions and the other audited areas; the year's
positive blood cultures with the admissions and ward transfers of the patients they came from and the midnight census;
the hand rub bottles issued to the wards and the refills the cleaning contractor fitted to their dispensers; the patient
experience survey and the staff influenza programme. Generator truth: nothing here ships as it stands."""
import collections
import datetime as dt
import numpy as np

import common as K

HCW = ["Nurse/Midwife", "Medical", "Allied health", "Personal care staff", "Support services", "Student"]
HCW_P = {"ward": [0.60, 0.15, 0.09, 0.08, 0.04, 0.04], "ED": [0.52, 0.27, 0.05, 0.05, 0.07, 0.04],
         "OT": [0.46, 0.30, 0.10, 0.04, 0.06, 0.04], "DSU": [0.58, 0.20, 0.06, 0.06, 0.06, 0.04],
         "RDU": [0.70, 0.08, 0.06, 0.07, 0.05, 0.04], "OPC": [0.40, 0.30, 0.18, 0.02, 0.06, 0.04],
         "MI": [0.20, 0.16, 0.50, 0.04, 0.06, 0.04]}
HCW_ADJ = np.array([0.02, -0.07, 0.0, -0.03, -0.10, 0.03])
MOMENT_P = np.array([0.30, 0.10, 0.10, 0.34, 0.16])
MOMENT_ADJ = np.array([-0.06, 0.02, 0.05, 0.05, -0.04])
AREA_BASE = {"ED": 0.80, "OT": 0.83, "DSU": 0.88, "RDU": 0.90, "OPC": 0.84, "MI": 0.79}
AREA_SESSIONS = {"ED": 150, "OT": 80, "DSU": 70, "RDU": 75, "OPC": 90, "MI": 60}
AREA_MOMENTS = {"ED": 14, "OT": 12, "DSU": 11, "RDU": 13, "OPC": 9, "MI": 8}
RENAME_DATE = dt.date(2026, 1, 1)      # the application's local name for personal care staff from this date

# recognised pathogens and the common commensals of the surveillance definitions
PATHOGENS = [("Staphylococcus aureus", 0.20), ("Escherichia coli", 0.24), ("Klebsiella pneumoniae", 0.12),
             ("Enterococcus faecalis", 0.10), ("Pseudomonas aeruginosa", 0.08), ("Candida albicans", 0.06),
             ("Enterobacter cloacae complex", 0.06), ("Serratia marcescens", 0.04), ("Proteus mirabilis", 0.05),
             ("Enterococcus faecium", 0.05)]
COMMENSALS = ["Staphylococcus epidermidis", "Staphylococcus hominis", "Micrococcus luteus",
              "Corynebacterium striatum", "Cutibacterium acnes"]
HOBSI_RATE = {"AMU": 14.0, "ESSU": 9.0, "4A": 16.0, "7A": 18.0, "5A": 15.0, "6A": 9.0, "6B": 11.0, "7B": 24.0,
              "8A": 30.0, "9A": 6.0, "9B": 12.0, "PCU": 8.0, "CCU": 20.0, "ICU": 42.0}   # per 10,000 bed days
# where a patient whose event is on the ward was admitted to first, and how often
FIRST_WARD = {"4A": ("AMU", 0.55), "7A": ("AMU", 0.50), "6B": ("ESSU", 0.35), "7B": ("AMU", 0.30),
              "9B": ("AMU", 0.45), "9A": ("4A", 0.60), "5A": ("ESSU", 0.20), "6A": ("ESSU", 0.15),
              "8A": ("AMU", 0.15), "CCU": ("ESSU", 0.40), "PCU": ("8A", 0.40), "ICU": ("AMU", 0.25)}
# patients moved a few hours before the culture was taken, the culture requested on the ward they left:
# (the ward that requested it, the ward it was collected on)
REQUEST_MOVES = [("AMU", "4A"), ("AMU", "4A"), ("AMU", "4A"), ("AMU", "7A"), ("AMU", "9B"), ("AMU", "7B"),
                 ("ESSU", "6B"), ("ESSU", "6B"), ("ESSU", "5A"), ("ESSU", "CCU"), ("4A", "ICU"), ("7A", "ICU"),
                 ("5A", "ICU"), ("5A", "ICU"), ("6A", "ICU"), ("6B", "CCU"), ("6B", "CCU"), ("CCU", "6B"),
                 ("7B", "ICU"), ("7B", "ICU"), ("8A", "ICU"), ("8A", "ICU"), ("8A", "PCU"), ("9A", "9B"),
                 ("9B", "PCU"), ("ICU", "7A")]

# hand rub items the store issues: code, description, unit of issue, litres a unit of issue
HAND_RUB = [("114502", "HAND RUB ALCOHOL 70% GEL 500ML PUMP", "EA", 0.5),
            ("114519", "HAND RUB ALCOHOL 70% GEL 100ML PERSONAL CTN 24", "CTN", 2.4),
            ("114533", "HAND RUB ALCOHOL 70% FOAM 1L DISPENSER REFILL", "EA", 1.0),
            ("114541", "HAND SOAP LIQUID PH NEUTRAL 500ML PUMP", "EA", 0.5),
            ("114547", "HAND SOAP LIQUID 800ML DISPENSER CARTRIDGE", "EA", 0.8)]
# the floors the cleaning contractor's handhelds cover, one handheld a floor
FLOORS = {"G": ("AMU", "ESSU", "ED", "MI"), "2": ("ICU", "CCU", "OT"), "4": ("4A", "DSU"), "5": ("5A", "OPC"),
          "6": ("6A", "6B"), "7": ("7A", "7B"), "8": ("8A", "PCU"), "9": ("9A", "9B"), "S1": ("S1A", "RDU")}
# the days a handheld sent the rounds it held since its last synchronisation a second time, after a battery change,
# and how many days of rounds it held
RESENDS = [("G", dt.date(2025, 8, 19), 12), ("6", dt.date(2025, 9, 23), 15), ("8", dt.date(2025, 11, 4), 11),
           ("2", dt.date(2025, 12, 9), 9), ("7", dt.date(2026, 1, 20), 13), ("9", dt.date(2026, 3, 3), 14),
           ("4", dt.date(2026, 4, 28), 10), ("5", dt.date(2026, 5, 19), 12), ("S1", dt.date(2026, 6, 9), 16)]
SOAP_USE = {"AMU": 14.0, "ESSU": 12.5, "4A": 11.0, "7A": 11.5, "5A": 10.5, "6A": 9.5, "6B": 10.0, "7B": 13.5,
            "8A": 15.0, "9A": 12.0, "9B": 13.0, "PCU": 11.0, "CCU": 16.0, "ICU": 24.0}   # litres of soap a 1,000 OBD
SPEC_USE = {"AMU": 52, "ESSU": 48, "4A": 38, "7A": 41, "5A": 33, "6A": 31, "6B": 36, "7B": 44, "8A": 55,
            "9A": 27, "9B": 30, "PCU": 25, "CCU": 68, "ICU": 118}   # litres of hand rub a 1,000 occupied bed days


def ward_of(code, d):
    """the code a ward carries in the hospital's systems on day d"""
    if code == K.MOVED[0] and d >= K.MOVE_DATE:
        return K.MOVED[1]
    return code


def canon(unit):
    return K.MOVED[0] if unit == K.MOVED[1] else unit


def hcw_label(h, d):
    if h == "Personal care staff" and d >= RENAME_DATE:
        return "Assistant in nursing"
    return h


def _hm(rng, lo, hi):
    """a time of day between lo and hi hours, to the minute"""
    m = int(rng.integers(int(round(lo * 60)), int(round(hi * 60)) + 1))
    return dt.time(m // 60, m % 60)


class Side:
    def __init__(self, world, seed=K.SEED):
        self.w = world
        self.seed = seed
        self._auditors()
        self._ward_sessions()
        self._other_sessions()
        self._session_ids()
        self._census()
        self._bsi()
        self._hand_rub()
        self._survey()
        self._flu()

    # ------------------------------------------------------------------ the audits
    def _auditors(self):
        rng = np.random.default_rng([269, self.seed, 20])
        self.auditors = {}
        k = 0
        for a in K.WARD + K.AREA:
            self.auditors[a] = []
            for _ in range(int(rng.integers(2, 5))):
                k += int(rng.integers(1, 9))
                self.auditors[a].append("GA%04d" % (1000 + k))

    def _labels(self, rng, outcomes, kind, d, base):
        """a moment number, health care worker group and action for each outcome: the group and moment drawn given
        whether hand hygiene was performed, so each group's and each moment's compliance differs as it does in the field
        while the session's count performed stays the one the world drew"""
        hp = np.array(HCW_P[kind])
        q = np.clip(base + HCW_ADJ[:, None] + MOMENT_ADJ[None, :], 0.05, 0.99)
        joint = hp[:, None] * MOMENT_P[None, :]
        out = []
        for ok in outcomes:
            pr = joint * (q if ok else 1 - q)
            pr = (pr / pr.sum()).ravel()
            i = int(rng.choice(pr.size, p=pr))
            h, mo = divmod(i, 5)
            act = ("Hand rub" if rng.random() < 0.88 else "Hand wash") if ok else "Missed"
            out.append((mo + 1, hcw_label(HCW[h], d), act))
        return out

    def _ward_sessions(self):
        rng = np.random.default_rng([269, self.seed, 21])
        base = {w[0]: w[4] for w in K.WARDS}
        self.sessions = []
        for s in self.w.sessions:
            code, d = s["ward"], s["date"]
            t = _hm(rng, 7.67, 12.33) if s["shift"] == "AM" else _hm(rng, 15.83, 20.5)
            aud = self.auditors[code]
            wts = np.arange(len(aud), 0, -1, dtype=float)
            a = aud[int(rng.choice(len(aud), p=wts / wts.sum()))]
            mom = self._labels(rng, s["outcomes"], "ward", d, float(s["c"]) / s["m"])
            self.sessions.append(dict(area=code, unit=ward_of(code, d), date=d, start=t, shift=s["shift"],
                                      auditor=a, moments=mom, kind="ward"))
        for code in K.WARD:
            for _ in range(int(rng.integers(2, 6))):
                d = K.DAYS[int(rng.integers(1, len(K.DAYS) - 1))]
                t = _hm(rng, 22.17, 23.9) if rng.random() < 0.6 else _hm(rng, 0.25, 5.33)
                n = max(3, int(rng.poisson(9)))
                ok = (rng.random(n) < base[code] - 0.02).tolist()
                aud = self.auditors[code]
                self.sessions.append(dict(area=code, unit=ward_of(code, d), date=d, start=t, shift="ND",
                                          auditor=aud[int(rng.integers(0, len(aud)))],
                                          moments=self._labels(rng, ok, "ward", d, base[code] - 0.02), kind="ward_nd"))

    def _other_sessions(self):
        rng = np.random.default_rng([269, self.seed, 22])
        hours = {"OT": (7.67, 17.0), "DSU": (7.67, 15.0), "RDU": (7.0, 19.0), "OPC": (8.5, 16.5), "MI": (8.0, 17.0)}
        for a in K.AREA:
            for _ in range(AREA_SESSIONS[a]):
                while True:
                    d = K.DAYS[int(rng.integers(0, len(K.DAYS)))]
                    if a == "ED" or d.weekday() < 5:
                        break
                if a == "ED":
                    r = rng.random()
                    t = (_hm(rng, 7.67, 12.33) if r < 0.55 else
                         (_hm(rng, 15.83, 20.5) if r < 0.92 else _hm(rng, 22.17, 23.9)))
                else:
                    t = _hm(rng, *hours[a])
                n = max(3, int(rng.poisson(AREA_MOMENTS[a])))
                ok = (rng.random(n) < AREA_BASE[a]).tolist()
                aud = self.auditors[a]
                self.sessions.append(dict(area=a, unit=a, date=d, start=t, shift=None,
                                          auditor=aud[int(rng.integers(0, len(aud)))],
                                          moments=self._labels(rng, ok, a, d, AREA_BASE[a]), kind="area"))

    def _session_ids(self):
        """session numbers in the order the sessions were saved: on the day, except the sessions recorded on paper while
        the application was down, which their auditors keyed in the days after it returned"""
        rng = np.random.default_rng([269, self.seed, 23])
        back = K.OUTAGE[1] + dt.timedelta(days=1)
        order = sorted(range(len(self.sessions)),
                       key=lambda i: (self.sessions[i]["date"], self.sessions[i]["start"], self.sessions[i]["area"]))
        stamp = {}
        for i in order:
            d = self.sessions[i]["date"]
            stamp[i] = back + dt.timedelta(days=int(rng.integers(0, 5))) if K.OUTAGE[0] <= d <= K.OUTAGE[1] else d
        seq = sorted(order, key=lambda i: (stamp[i], self.sessions[i]["date"], self.sessions[i]["start"],
                                            self.sessions[i]["area"]))
        n = 48210
        for i in seq:
            n += int(rng.integers(1, 4))
            self.sessions[i]["sid"] = n

    # ------------------------------------------------------------------ census and bloodstream infections
    def _census(self):
        rng = np.random.default_rng([269, self.seed, 30])
        self.census = {}
        for code in K.WARD:
            for d in K.DAYS:
                pm = self.w.shifts[(code, d, "PM")]["npts"]
                self.census[(code, d)] = max(0, pm - int(rng.binomial(2, 0.25)))
        self.bed_days = {c: sum(self.census[(c, d)] for d in K.DAYS) for c in K.WARD}

    @staticmethod
    def _dt(d, rng, lo=0.0, hi=23.98):
        return dt.datetime.combine(d, _hm(rng, lo, hi))

    def _bsi(self):
        rng = np.random.default_rng([269, self.seed, 31])
        self.patients = []
        self.mrn_next = 4100000
        moves_for = {c: [] for c in K.WARD}
        idx = list(range(len(REQUEST_MOVES)))
        rng.shuffle(idx)
        for i in idx:
            moves_for[REQUEST_MOVES[i][1]].append(REQUEST_MOVES[i][0])

        def person():
            self.mrn_next += int(rng.integers(3, 41))
            dob = dt.date(1931, 1, 1) + dt.timedelta(days=int(rng.integers(0, 365 * 72)))
            return self.mrn_next, dob, ("F" if rng.random() < 0.47 else "M")

        def org():
            return PATHOGENS[int(rng.choice(len(PATHOGENS), p=[p for _, p in PATHOGENS]))][0]

        for code in K.WARD:
            n_ev = max(int(rng.poisson(HOBSI_RATE[code] * self.bed_days[code] / 10000.0)), len(moves_for[code]) + 2)
            for e in range(n_ev):
                mrn, dob, sex = person()
                cd = K.DAYS[int(rng.integers(20, len(K.DAYS) - 20))]
                coll = self._dt(cd, rng, 0.5, 23.5)
                req_from = moves_for[code][e] if e < len(moves_for[code]) else None
                if req_from is not None:
                    move_t = coll - dt.timedelta(minutes=int(rng.integers(40, 421)))
                    first = req_from
                    adm = move_t - dt.timedelta(hours=float(rng.uniform(60, 240)))
                    moves = [(move_t, code)]
                else:
                    fw = FIRST_WARD.get(code)
                    if fw and rng.random() < fw[1]:
                        first = fw[0]
                        move_t = coll - dt.timedelta(hours=float(rng.uniform(30, 300)))
                        adm = move_t - dt.timedelta(hours=float(rng.uniform(4, 60)))
                        moves = [(move_t, code)]
                    else:
                        first, moves = code, []
                        adm = coll - dt.timedelta(hours=float(rng.uniform(54, 420)))
                if (coll - adm).total_seconds() < 54 * 3600:
                    adm = coll - dt.timedelta(hours=54 + float(rng.uniform(0, 30)))
                adm = adm.replace(second=0, microsecond=0)
                moves = [(t.replace(second=0, microsecond=0), w) for t, w in moves]
                o = org()
                cultures = [(coll, o, req_from if req_from else code)]
                if rng.random() < 0.42:      # the same organism again inside fourteen days, on the same ward
                    cultures.append((coll + dt.timedelta(days=int(rng.integers(1, 12)), hours=int(rng.integers(0, 10)),
                                                         minutes=int(rng.integers(0, 60))), o, code))
                dis = max(c[0] for c in cultures) + dt.timedelta(days=int(rng.integers(2, 12)),
                                                                   hours=int(rng.integers(0, 10)))
                self.patients.append(dict(mrn=mrn, dob=dob, sex=sex, adm=adm, dis=dis, first=first, moves=moves,
                                          cultures=cultures, kind="event", ward=code))
        # the same organism again more than fourteen days later in one admission: two events
        for code in ("ICU", "8A", "7B"):
            mrn, dob, sex = person()
            coll = self._dt(K.DAYS[int(rng.integers(40, len(K.DAYS) - 60))], rng, 1, 22)
            adm = (coll - dt.timedelta(hours=float(rng.uniform(80, 200)))).replace(second=0, microsecond=0)
            o = org()
            t2 = coll + dt.timedelta(days=int(rng.integers(17, 26)), hours=int(rng.integers(0, 8)))
            self.patients.append(dict(mrn=mrn, dob=dob, sex=sex, adm=adm, dis=t2 + dt.timedelta(days=int(rng.integers(3, 10))),
                                      first=code, moves=[], cultures=[(coll, o, code), (t2, o, code)], kind="event2",
                                      ward=code))
        # community onset on the wards, cultures taken in the emergency department before admission, commensal singles
        # and pairs, and the cultures of people not admitted
        for _ in range(430):
            code = K.WARD[int(rng.integers(0, len(K.WARD)))]
            mrn, dob, sex = person()
            adm = self._dt(K.DAYS[int(rng.integers(5, len(K.DAYS) - 20))], rng).replace(second=0)
            kind = str(rng.choice(["community", "community_ed", "commensal_single", "commensal_pair"],
                                  p=[0.40, 0.25, 0.25, 0.10]))
            if kind == "community":
                cultures = [(adm + dt.timedelta(hours=float(rng.uniform(1, 40))), org(), code)]
            elif kind == "community_ed":
                cultures = [(adm - dt.timedelta(minutes=int(rng.integers(30, 300))), org(), "ED")]
            else:
                coll = adm + dt.timedelta(hours=float(rng.uniform(56, 300)))
                c0 = COMMENSALS[int(rng.integers(0, len(COMMENSALS)))]
                cultures = [(coll, c0, code)]
                if kind == "commensal_pair":
                    cultures.append((coll + dt.timedelta(hours=float(rng.uniform(0.3, 30))), c0, code))
            cultures = [(t.replace(second=0, microsecond=0), o, l) for t, o, l in cultures]
            dis = max(c[0] for c in cultures) + dt.timedelta(days=int(rng.integers(1, 9)), hours=int(rng.integers(0, 12)))
            self.patients.append(dict(mrn=mrn, dob=dob, sex=sex, adm=adm, dis=dis, first=code, moves=[],
                                      cultures=cultures, kind=kind, ward=code if kind == "commensal_pair" else None))
        for _ in range(170):
            mrn, dob, sex = person()
            loc = "ED" if rng.random() < 0.8 else ("OPC" if rng.random() < 0.6 else "RDU")
            coll = self._dt(K.DAYS[int(rng.integers(0, len(K.DAYS)))], rng)
            o = org() if rng.random() < 0.7 else COMMENSALS[int(rng.integers(0, len(COMMENSALS)))]
            self.patients.append(dict(mrn=mrn, dob=dob, sex=sex, adm=None, dis=None, first=None, moves=[],
                                      cultures=[(coll, o, loc)], kind="unadmitted", ward=None))
        for p in self.patients:
            p["cultures"] = [(t.replace(second=0, microsecond=0), o, l) for t, o, l in p["cultures"]]
        # the patients' other ward transfers, after their last culture (step-down, rehabilitation, aged care, a bed
        # found on the specialty's own ward)
        r2 = np.random.default_rng([269, self.seed, 32])
        onward = {"ICU": ("4A", "7A", "5A", "6B", "7B", "8A"), "CCU": ("6B", "4A"), "AMU": ("4A", "7A", "7B", "9B", "6B"),
                  "ESSU": ("4A", "5A", "6A", "6B", "9B"), "4A": ("9A", "9B", "7A"), "7A": ("9A", "9B", "4A"),
                  "5A": ("9A", "6A"), "6A": ("9A",), "6B": ("9B", "4A"), "7B": ("9B", "4A"), "8A": ("PCU", "4A"),
                  "9A": ("9B",), "9B": ("PCU", "9A"), "PCU": ("9B",)}
        for p in self.patients:
            if p["adm"] is None:
                continue
            if r2.random() >= (0.25 if p["kind"] in ("event", "event2") else 0.45):
                continue
            cur = p["moves"][-1][1] if p["moves"] else p["first"]
            t = max(max(c[0] for c in p["cultures"]), p["adm"])
            if p["moves"]:
                t = max(t, p["moves"][-1][0])
            for _ in range(1 if r2.random() < 0.7 else 2):
                t = (t + dt.timedelta(hours=float(r2.uniform(3, 96)))).replace(second=0, microsecond=0)
                if t >= p["dis"] - dt.timedelta(hours=2):
                    break
                nxt = onward[cur][int(r2.integers(0, len(onward[cur])))]
                p["moves"] = p["moves"] + [(t, nxt)]
                cur = nxt
        # the patient master index merge of 1 March 2026: patients registered twice, whose cultures before it were
        # reported under the record that was retired
        cand = [i for i, p in enumerate(self.patients)
                if p["kind"] == "event" and p["cultures"][0][0].date() < K.MPI_MERGE]
        self.retired = {}
        for j in sorted(int(x) for x in rng.choice(len(cand), size=12, replace=False)):
            self.retired[self.patients[cand[j]]["mrn"]] = 2900000 + int(rng.integers(10000, 99999))
        self._stays(person, org)

    def _stays(self, person, org):
        """patients whose stay is two admissions, or who were admitted again soon after going home: a change of care
        type (acute to rehabilitation, aged care, palliative or maintenance care) closes the admission and opens
        another at the same minute, on the ward the patient moves to or the same one; and patients discharged home
        who came back within a day. Each ward holds both, with the culture inside 48 hours of the second admission,
        and their benign twins: a culture more than 48 hours after it, and earlier admissions weeks before."""
        rng = np.random.default_rng([269, self.seed, 33])
        upstream = {"9A": ("4A", "5A", "6A", "7A"), "9B": ("AMU", "4A", "7A", "7B"), "PCU": ("8A", "4A", "7B")}

        def when(lo=25, hi=25):
            return self._dt(K.DAYS[int(rng.integers(lo, len(K.DAYS) - hi))], rng, 0.5, 23.5)

        for code in K.WARD:
            n_chain = 1 + int(rng.random() < 0.45)
            n_back = 1 + int(rng.random() < 0.35)
            for j in range(n_chain + 2):
                mrn, dob, sex = person()
                tc = when()
                first0 = upstream[code][int(rng.integers(0, len(upstream[code])))] if code in upstream else code
                a0 = tc - dt.timedelta(hours=float(rng.uniform(72, 300)))
                x = float(rng.uniform(8, 40)) if j < n_chain else float(rng.uniform(54, 200))
                coll = tc + dt.timedelta(hours=x)
                o = org()
                cultures = [(coll, o, code)]
                dis = coll + dt.timedelta(days=int(rng.integers(2, 14)), hours=int(rng.integers(0, 10)))
                self.patients.append(dict(mrn=mrn, dob=dob, sex=sex, adm=tc, dis=dis, first=code, moves=[],
                                          cultures=cultures, kind="chain" if j < n_chain else "chain_late", ward=code,
                                          pre=[dict(adm=a0, dis=tc, first=first0, moves=[])]))
            for j in range(n_back + 1):
                mrn, dob, sex = person()
                back = when()
                gap = float(rng.uniform(3, 20))
                d0 = back - dt.timedelta(hours=gap)
                prev = upstream[code][int(rng.integers(0, len(upstream[code])))] if code in upstream else (
                    code if rng.random() < 0.6 else K.WARD[int(rng.integers(0, len(K.WARD)))])
                a0 = d0 - dt.timedelta(hours=float(rng.uniform(60, 260)))
                x = float(rng.uniform(4, 40)) if j < n_back else float(rng.uniform(54, 200))
                coll = back + dt.timedelta(hours=x)
                o = org()
                dis = coll + dt.timedelta(days=int(rng.integers(2, 12)), hours=int(rng.integers(0, 10)))
                self.patients.append(dict(mrn=mrn, dob=dob, sex=sex, adm=back, dis=dis, first=code, moves=[],
                                          cultures=[(coll, o, code)], kind="back" if j < n_back else "back_late",
                                          ward=code, pre=[dict(adm=a0, dis=d0, first=prev, moves=[])]))
        # patients readmitted inside an episode: a hospital-onset culture in one admission, home, and the same organism
        # grown more than 48 hours into a readmission days later but under 14 days after the episode's first culture
        # (the same episode); and their twins, the same organism 15 days or more after it (a new episode)
        for code in K.WARD:
            n_rep = 1 + int(rng.random() < 0.4)
            for j in range(n_rep + 1):
                mrn, dob, sex = person()
                o = org()
                for _try in range(50):
                    c1 = when(30, 40)
                    span = float(rng.uniform(6.0, 13.3)) if j < n_rep else float(rng.uniform(15.5, 24.0))
                    c2 = c1 + dt.timedelta(days=span)
                    back = c2 - dt.timedelta(hours=float(rng.uniform(52, 100)))
                    d0 = back - dt.timedelta(hours=float(rng.uniform(36, 120)))
                    if d0 >= c1 + dt.timedelta(hours=36) and c2.date() <= K.YEAR_END:
                        break
                u = K.WARD[int(rng.integers(0, len(K.WARD)))] if rng.random() < 0.5 else code
                a0 = c1 - dt.timedelta(hours=float(rng.uniform(60, 220)))
                dis = c2 + dt.timedelta(days=int(rng.integers(2, 10)), hours=int(rng.integers(0, 10)))
                self.patients.append(dict(mrn=mrn, dob=dob, sex=sex, adm=back, dis=dis, first=code, moves=[],
                                          cultures=[(c1, o, u), (c2, o, code)],
                                          kind="repeat" if j < n_rep else "repeat_late", ward=code,
                                          pre=[dict(adm=a0, dis=d0, first=u, moves=[])]))
        # earlier admissions weeks or months before, for patients of every kind
        for p in self.patients:
            if p["adm"] is None or p.get("pre") or rng.random() >= 0.16:
                continue
            d1 = p["adm"] - dt.timedelta(days=float(rng.uniform(9, 150)))
            a1 = d1 - dt.timedelta(hours=float(rng.uniform(20, 240)))
            if a1.date() < K.YEAR_START - dt.timedelta(days=60):
                continue
            w1 = p["first"] if rng.random() < 0.5 else K.WARD[int(rng.integers(0, len(K.WARD)))]
            p["pre"] = [dict(adm=a1, dis=d1, first=w1, moves=[])]
        for p in self.patients:
            for r in p.get("pre", []):
                r["adm"] = r["adm"].replace(second=0, microsecond=0)
                r["dis"] = r["dis"].replace(second=0, microsecond=0)
            if p["adm"] is not None:
                p["adm"] = p["adm"].replace(second=0, microsecond=0)
            p["cultures"] = [(t.replace(second=0, microsecond=0), o, l) for t, o, l in p["cultures"]]

    # ------------------------------------------------------------------ hand rub
    def _hand_rub(self):
        """bottles issued to each ward's cost centre from the store, and the refills the cleaning contractor fitted to
        each dispenser on its rounds, with the days a floor's handheld sent its stored week again"""
        rng = np.random.default_rng([269, self.seed, 40])
        self.dispensers = []        # (id, unit, location, installed, removed)
        k = 0
        floor_of = {u: fl for fl, units in FLOORS.items() for u in units}
        for u in K.WARD + [K.MOVED[1]] + K.AREA:
            beds = K.BEDS.get(canon(u), 14)
            n = int(beds * 0.7) + (7 if u == K.MOVED[1] else 6)
            frm = K.MOVE_DATE if u == K.MOVED[1] else dt.date(2019, 3, 1)
            to = K.MOVE_DATE if u == K.MOVED[0] else None
            for _ in range(n):
                k += int(rng.integers(1, 4))
                self.dispensers.append(("D%05d" % (20000 + k), u, floor_of[u], frm, to))
        # the sinks' soap dispensers, numbered in the same asset series
        self.disp_type = {x[0]: "Hand rub" for x in self.dispensers}
        for u in K.WARD + [K.MOVED[1]]:
            beds = K.BEDS.get(canon(u), 14)
            frm = K.MOVE_DATE if u == K.MOVED[1] else dt.date(2019, 3, 1)
            to = K.MOVE_DATE if u == K.MOVED[0] else None
            for _ in range(int(beds * 0.3) + 3):
                k += int(rng.integers(1, 4))
                did = "D%05d" % (20000 + k)
                self.dispensers.append((did, u, floor_of[u], frm, to))
                self.disp_type[did] = "Hand soap"
        self.dispensers.sort(key=lambda x: x[0])
        self.unit_of_d = {x[0]: x[1] for x in self.dispensers}
        live = {}
        for did, u, fl, f, t in self.dispensers:
            if self.disp_type[did] == "Hand rub":
                live.setdefault(u, []).append((did, f, t))
        wall_share = {c: float(np.clip(rng.normal(0.62, 0.06), 0.48, 0.75)) for c in K.WARD}
        self.refills = []           # (dispenser, fitted, floor, kind)
        used = {}                   # a dispenser's rounds fall on the same minute of the day only weeks apart
        for code in K.WARD:
            for d in K.DAYS:
                use = SPEC_USE[code] * self.census[(code, d)] / 1000.0 * float(rng.lognormal(0, 0.18))
                u = ward_of(code, d)
                dl = [x[0] for x in live[u] if x[1] <= d and (x[2] is None or d < x[2])]
                for _ in range(int(rng.poisson(use * wall_share[code]))):
                    did = dl[int(rng.integers(0, len(dl)))]
                    self.refills.append((did, dt.datetime.combine(d, self._minute(rng, did, used, d)), floor_of[u],
                                         "genuine"))
        # a busy dispenser refilled again later the same day: every ward has some
        for code in K.WARD:
            mine = [(did, t) for did, t, f, kind in self.refills if canon(self.unit_of_d[did]) == code
                    and self.disp_type[did] == "Hand rub"]
            days = collections.Counter((did, t.date()) for did, t in mine)
            have = sum(1 for v in days.values() if v > 1)
            for j in range(max(0, 2 - have)):
                did, t = mine[int(rng.integers(0, len(mine)))]
                again = dt.datetime.combine(t.date(), self._minute(rng, did, used, t.date()))
                self.refills.append((did, again, floor_of[self.unit_of_d[did]], "genuine"))
        for a in K.AREA:
            for d in K.DAYS:
                for _ in range(int(rng.poisson(2.4 if a in ("ED", "OT") else 0.8))):
                    did = live[a][int(rng.integers(0, len(live[a])))][0]
                    self.refills.append((did, dt.datetime.combine(d, self._minute(rng, did, used, d)), floor_of[a],
                                         "genuine"))
        # the contractor's soap cartridges on the sinks' dispensers
        srng = np.random.default_rng([269, self.seed, 41])
        soap_live = {}
        for did, u, fl, f, t in self.dispensers:
            if self.disp_type[did] == "Hand soap":
                soap_live.setdefault(u, []).append((did, f, t))
        self.soap_wall = {c: float(np.clip(srng.normal(0.70, 0.05), 0.6, 0.8)) for c in K.WARD}
        for code in K.WARD:
            for d in K.DAYS:
                use = SOAP_USE[code] * self.census[(code, d)] / 1000.0 * float(srng.lognormal(0, 0.2))
                u = ward_of(code, d)
                dl = [x[0] for x in soap_live[u] if x[1] <= d and (x[2] is None or d < x[2])]
                for _ in range(int(srng.poisson(use * self.soap_wall[code] / 0.8))):
                    did = dl[int(srng.integers(0, len(dl)))]
                    self.refills.append((did, dt.datetime.combine(d, self._minute(srng, did, used, d)), floor_of[u],
                                         "genuine"))
        # terminal cleans: when a patient in isolation leaves, the contractor discards the soap at the isolation room's
        # sinks and fits a new cartridge to each, on a job raised for the room; the handheld writes the job's quantity
        # on each of its records
        rooms = {}
        for u, lst in soap_live.items():
            ids = [x[0] for x in lst]
            pick = [str(x) for x in srng.permutation(ids)]
            rooms[u] = []
            for _ in range(1 + int(srng.integers(0, 3))):
                k = 2 if srng.random() < 0.6 else 3
                rooms[u].append(tuple(sorted(pick[:k])))
                pick = pick[k:]
        jobs = []
        held = {}
        for fl, day, h in RESENDS:
            held.setdefault(fl, []).append((day - dt.timedelta(days=h), day))
        for code in K.WARD:
            for _ in range(2 + int(srng.poisson(K.BEDS[code] * 0.18))):
                # a terminal clean's records synchronise from the floor supervisor's handheld, outside the batches the
                # floor handhelds re-sent
                while True:
                    d = K.DAYS[int(srng.integers(0, len(K.DAYS)))]
                    u = ward_of(code, d)
                    if not any(a <= d < b for a, b in held.get(floor_of[u], [])):
                        break
                room = rooms[u][int(srng.integers(0, len(rooms[u])))]
                t0 = dt.datetime.combine(d, _hm(srng, 7.5, 19.5))
                lines = []
                for did in room:
                    t0 += dt.timedelta(minutes=int(srng.integers(1, 4)))
                    while not self._free(did, used, t0.time(), d):
                        t0 += dt.timedelta(minutes=1)
                    used.setdefault(did, {}).setdefault(t0.time(), []).append(d)
                    lines.append((did, t0))
                    self.refills.append((did, t0, floor_of[u], "genuine"))
                jobs.append(lines)
        self.jobs = {}
        n = 30410
        for lines in sorted(jobs, key=lambda x: x[0][1]):
            n += int(srng.integers(1, 9))
            for did, t in lines:
                self.jobs[(did, t)] = ("TC%06d" % n, len(lines))
        self.unit_of = {x[0]: x[1] for x in self.dispensers}
        # by chance a dispenser is refilled at the same minute of the day weeks apart; every ward has such a pair on
        # its hand rub and on its soap dispensers
        for code in K.WARD:
            for kind_of in ("Hand rub", "Hand soap"):
                mine = [i for i, (did, t, f, kind) in enumerate(self.refills) if kind == "genuine"
                        and canon(self.unit_of[did]) == code and self.disp_type[did] == kind_of
                        and (did, t) not in self.jobs]
                by = collections.defaultdict(list)
                for i in mine:
                    by[(self.refills[i][0], self.refills[i][1].time())].append(i)
                if any(len(v) > 1 for v in by.values()):
                    continue
                order = [mine[int(j)] for j in srng.permutation(len(mine))]
                done = False
                for i in order:
                    did, t, f, kind = self.refills[i]
                    for k in order:
                        d2, t2, f2, kind2 = self.refills[k]
                        if d2 != did or (t2.date() - t.date()).days <= 30:
                            continue
                        if all(abs((t2.date() - x).days) > 30 for x in used[did].get(t.time(), [])):
                            used[did][t2.time()].remove(t2.date())
                            used[did].setdefault(t.time(), []).append(t2.date())
                            self.refills[k] = (d2, dt.datetime.combine(t2.date(), t.time()), f2, kind2)
                            done = True
                            break
                    if done:
                        break
        self.resent = []
        for fl, day, held in RESENDS:
            for did, t, f, kind in self.refills:
                if f == fl and kind == "genuine" and day - dt.timedelta(days=held) <= t.date() < day:
                    self.resent.append((did, dt.datetime.combine(day, t.time()), f, "resend"))
        self.refills = self.refills + self.resent
        # where a ward's genuine second refills in a day number exactly its re-sent records, one more busy day
        # outside its floor's re-sends
        for code in K.WARD:
            fl = floor_of[ward_of(code, K.YEAR_END)]
            win = [(day - dt.timedelta(days=held), day) for f0, day, held in RESENDS if f0 in (fl, floor_of[code])]
            while True:
                mine = [(did, t) for did, t, f, kind in self.refills if kind == "genuine" and
                        canon(self.unit_of_d[did]) == code and self.disp_type[did] == "Hand rub"]
                per = collections.Counter((did, t.date()) for did, t in mine)
                second = sum(v - 1 for v in per.values())
                copies = sum(1 for did, t, f, kind in self.resent if canon(self.unit_of_d[did]) == code
                             and self.disp_type[did] == "Hand rub")
                if second != copies:
                    break
                cand = [(did, t) for did, t in mine if not any(a <= t.date() <= b for a, b in win)]
                did, t = cand[int(rng.integers(0, len(cand)))]
                again = dt.datetime.combine(t.date(), self._minute(rng, did, used, t.date()))
                self.refills.append((did, again, floor_of[self.unit_of_d[did]], "genuine"))
        # bottles: weekly imprest top-ups to each ward's cost centre, and the pump batch recalled in October 2025
        self.bottles = []           # (issue date, ward, item, quantity in units of issue; a return negative)
        for code in K.WARD:
            owed = 0.0          # personal bottles are ordered by the carton once a carton's worth is used
            for wk in range(53):
                d = K.YEAR_START + dt.timedelta(days=7 * wk + int(rng.integers(0, 3)))
                days = [x for x in (K.YEAR_START + dt.timedelta(days=7 * wk + j) for j in range(7)) if x <= K.YEAR_END]
                if d > K.YEAR_END or not days:
                    continue
                use = sum(SPEC_USE[code] * self.census[(code, x)] / 1000.0 for x in days)
                bl = use * (1 - wall_share[code]) * float(rng.lognormal(0, 0.15))
                pumps = int(round(bl * 0.7 / 0.5))
                owed += bl * 0.3 / 2.4
                ctn = int(owed)
                owed -= ctn
                if pumps:
                    self.bottles.append((d, code, "114502", pumps))
                if ctn:
                    self.bottles.append((d, code, "114519", ctn))
        recall = dt.date(2025, 10, 14)
        litres = {"114502": 0.5, "114519": 2.4}
        for code in K.WARD:
            back = int(rng.integers(2, 9))
            # a ward returned one pump more where its year's litres a bed day would print on a rounding edge
            wall = sum(1 for did, t, f, kind in self.refills if kind == "genuine" and canon(self.unit_of[did]) == code
                       and self.disp_type[did] == "Hand rub")
            got = sum(q * litres[it] for d0, c0, it, q in self.bottles if c0 == code)
            while True:
                rate = (got - 0.5 * back + wall) / self.bed_days[code] * 1000.0
                if abs(rate * 10 - np.floor(rate * 10) - 0.5) > 0.05:
                    break
                back += 1
            self.bottles.append((recall + dt.timedelta(days=int(rng.integers(0, 4))), code, "114502", -back))
        for code in K.WARD:
            for wk in range(53):
                d = K.YEAR_START + dt.timedelta(days=7 * wk + int(srng.integers(0, 4)))
                days = [x for x in (K.YEAR_START + dt.timedelta(days=7 * wk + j) for j in range(7)) if x <= K.YEAR_END]
                if d > K.YEAR_END or not days:
                    continue
                use = sum(SOAP_USE[code] * self.census[(code, x)] / 1000.0 for x in days)
                pumps = int(round(use * (1 - self.soap_wall[code]) * float(srng.lognormal(0, 0.15)) / 0.5))
                if pumps:
                    self.bottles.append((d, code, "114541", pumps))
            cart = sum(1 for did, t, f, kind in self.refills if kind == "genuine" and canon(self.unit_of[did]) == code
                       and self.disp_type[did] == "Hand soap")
            while True:
                got = sum(q * 0.5 for d0, c0, it, q in self.bottles if c0 == code and it == "114541")
                rate = (got + 0.8 * cart) / self.bed_days[code] * 1000.0
                if abs(rate * 10 - np.floor(rate * 10) - 0.5) > 0.05:
                    break
                d = K.YEAR_START + dt.timedelta(days=int(srng.integers(0, len(K.DAYS))))
                self.bottles.append((d, code, "114541", 1))
        self.bottles.sort(key=lambda b: (b[0], K.WARD.index(b[1]), b[2]))

    @staticmethod
    def _free(did, used, t, d):
        """no round of the dispenser at this minute of the day within thirty days of d"""
        return all(abs((d - d0).days) > 30 for d0 in used.get(did, {}).get(t, []))

    @staticmethod
    def _minute(rng, did, used, d):
        while True:
            t = _hm(rng, 6.0, 21.5)
            if Side._free(did, used, t, d):
                used.setdefault(did, {}).setdefault(t, []).append(d)
                return t

    # ------------------------------------------------------------------ distractors
    def _survey(self):
        rng = np.random.default_rng([269, self.seed, 50])
        self.survey = []
        for code in K.WARD:
            for y, m in ((2025, 7), (2025, 8), (2025, 9), (2025, 10), (2025, 11), (2025, 12), (2026, 1), (2026, 2),
                         (2026, 3), (2026, 4), (2026, 5), (2026, 6)):
                n = int(rng.integers(5, 23))
                yes = int(rng.binomial(n, 0.93))
                dk = int(rng.binomial(n - yes, 0.6))
                self.survey.append((code, dt.date(y, m, 1), n, yes, n - yes - dk, dk))

    def _flu(self):
        rng = np.random.default_rng([269, self.seed, 51])
        self.flu = []
        k = 0
        for code in K.WARD:
            for _ in range(int(K.BEDS[code] * 1.4)):
                k += int(rng.integers(1, 6))
                vac = rng.random() < 0.78
                d = dt.date(2025, 4, 7) + dt.timedelta(days=int(rng.integers(0, 120))) if vac else None
                self.flu.append(("%06d" % (310000 + k), code, d))
