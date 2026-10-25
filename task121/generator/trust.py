"""The trust's own records for the paper's annexes, a different population from the borough file's 2022 to 2024
cohorts: every pupil on roll at the eight academies in 2025/26 with their attendance by half-term, the year's in-year
admissions, leavers and moves between academies, and the examination results of the summer 2025 and summer 2026
series (the 2026 cohort's year 10 early entries sit in the 2025 series). Every draw is keyed on what it describes."""
import datetime as dt
import numpy as np
import common as K
import world as W

D = dt.date
HALF_TERMS = ["Au1", "Au2", "Sp1", "Sp2", "Su1", "Su2"]
# each academy's half-term starts (the trust sets one calendar; two academies keep their own INSET days)
HT_START = [D(2025, 9, 3), D(2025, 11, 3), D(2026, 1, 5), D(2026, 2, 23), D(2026, 4, 13), D(2026, 6, 8)]
HT_DAYS = [36, 34, 30, 29, 34, 33]          # school days in each half-term, before INSET adjustments
INSET = {"FRN": [0, 0, 1, 0, 0, 1], "WRF": [1, 0, 0, 0, 1, 0]}

# year 7 to year 11 cohort sizes at each academy in 2025/26
ROLL = {"HAL": 182, "BPK": 248, "FRN": 196, "CDW": 214, "MSG": 168, "SLM": 176, "RDH": 226, "WRF": 158}

SUBJECTS = {
    # code: (title, discount code, kind) kind: ENGL, ENGT, MAT, SCI2 (combined double), SCI, EBH (humanity), EBL
    # (language), OPEN (GCSE outside the EBacc), TECH (technical award, graded L1P to L2D*)
    "ENL": ("English Language", "FK2", "ENGL"), "ENT": ("English Literature", "FK3", "ENGT"),
    "MAT": ("Mathematics", "2210", "MAT"), "CSD": ("Combined Science", "RA1E", "SCI2"),
    "BIO": ("Biology", "1010", "SCI"), "CHE": ("Chemistry", "1110", "SCI"), "PHY": ("Physics", "1210", "SCI"),
    "CMP": ("Computer Science", "CK1", "SCI"), "HIS": ("History", "DB", "EBH"), "GEO": ("Geography", "DE", "EBH"),
    "FRE": ("French", "FK", "EBL"), "SPA": ("Spanish", "FKC", "EBL"), "URD": ("Urdu", "FKU", "EBL"),
    "POL": ("Polish", "FKP", "EBL"), "ART": ("Art and Design", "JA2", "OPEN"), "MUS": ("Music", "LF", "OPEN"),
    "DRA": ("Drama", "LH", "OPEN"), "RES": ("Religious Studies", "V1", "OPEN"), "STA": ("Statistics", "2610", "OPEN"),
    "FPN": ("Food Preparation and Nutrition", "NB", "OPEN"), "DTE": ("Design and Technology", "9600", "OPEN"),
    "BUS": ("Business", "3210", "OPEN"), "PEG": ("Physical Education", "XA1", "OPEN"),
    "TSP": ("Technical Award in Sport", "XA1", "TECH"), "THS": ("Technical Award in Health and Social Care", "AT1",
                                                                     "TECH"),
    "TIM": ("Technical Award in Creative iMedia", "CN1", "TECH"), "TEN": ("Technical Award in Enterprise", "3210",
                                                                           "TECH"),
}
TECH_POINTS = {"L2D*": 8.5, "L2D": 7.0, "L2M": 5.5, "L2P": 4.0, "L1D*": 3.0, "L1D": 2.0, "L1M": 1.5, "L1P": 1.25,
               "U": 0.0}
# each academy's early-entry habit for its year 10s: subject and share entered
EARLY = {"HAL": [("URD", 0.07), ("POL", 0.04), ("STA", 0.16)], "BPK": [("STA", 0.42), ("SPA", 0.05)],
         "FRN": [("FRE", 0.10), ("STA", 0.26)], "CDW": [("URD", 0.05), ("STA", 0.32)], "MSG": [("POL", 0.06),
         ("STA", 0.24)], "SLM": [("STA", 0.36), ("URD", 0.04)], "RDH": [("FRE", 0.08), ("URD", 0.03), ("STA", 0.20)],
         "WRF": [("SPA", 0.09), ("STA", 0.30)]}


def rr(*key):
    return W.rng_for("trust", *key)


def upn(k, yr, i):
    """A unique pupil number in the Department's pattern: check letter, LA, school, year issued, serial."""
    est = {"HAL": 4001, "BPK": 4002, "FRN": 4003, "CDW": 4004, "MSG": 4005, "SLM": 4006, "RDH": 4007,
           "WRF": 4008}[k]
    body = "%s%04d%02d%03d" % (K.LA_CODE, est, (2019 - yr + 11 + 7) % 100, i % 1000)
    letters = "ABCDEFGHJKLMNPQRTUVWXYZ"
    w = sum((n + 2) * int(c) for n, c in enumerate(body))
    return letters[w % 23] + body


class Trust:
    def __init__(self):
        self.pupils, self.att, self.moves = [], [], []
        self.roll()
        self.attendance()
        self.results()

    def possible(self, k, h):
        return 2 * (HT_DAYS[h] - INSET.get(k, [0] * 6)[h])

    def roll(self):
        n = 0
        for k in K.TRUST_KEYS:
            rg = rr("roll", k)
            dep = {"HAL": 0.47, "SLM": 0.36, "CDW": 0.31, "MSG": 0.38, "WRF": 0.33, "FRN": 0.30, "RDH": 0.24,
                   "BPK": 0.19}[k]
            for yg in range(7, 12):
                size = int(ROLL[k] * rg.uniform(0.92, 1.04))
                for i in range(size):
                    n += 1
                    dis = rg.random() < dep
                    sen = "E" if rg.random() < 0.03 else ("K" if rg.random() < 0.12 + 0.05 * dis else "N")
                    eal = rg.random() < (0.22 if k in ("HAL", "CDW", "RDH") else 0.10)
                    base = float(np.clip(rg.gamma(1.8, 2.4) + 2.8 * dis + 2.2 * (sen != "N") + 0.5 * (yg - 7)
                                         + {"HAL": 1.1, "SLM": 0.5, "MSG": 0.7}.get(k, 0.0), 0.0, 80.0))
                    if rg.random() < 0.012 + 0.012 * dis + 0.01 * (sen != "N"):
                        base = float(rg.uniform(38.0, 85.0))      # school refusal, long illness: severe absence
                    self.pupils.append(dict(id=n, academy=k, yg=yg, dis=dis, sen=sen, eal=eal, rate=base,
                                            upn=upn(k, yg, n), adm=None, enrol=[]))
        # admission numbers: each academy's own series, issued in order of entry
        for k in K.TRUST_KEYS:
            seq = rr("adm", k).integers(1200, 2600)
            for p in self.pupils:
                if p["academy"] == k:
                    seq += 1
                    p["adm"] = "%s%05d" % (k[0], seq) if k not in ("FRN", "WRF") else "%06d" % seq
        self._seq = {k: 9000 for k in K.TRUST_KEYS}

    def attendance(self):
        """Each pupil's enrolments: most stay all year; some join or leave the trust at a half-term boundary, and
        some move between two academies (managed moves and in-year transfers) at a half-term boundary."""
        NEIGH = {"HAL": ["SLM", "CDW"], "SLM": ["HAL", "RDH"], "CDW": ["HAL", "BPK", "MSG"], "BPK": ["CDW", "FRN"],
                 "FRN": ["WRF", "BPK"], "MSG": ["CDW", "WRF"], "RDH": ["SLM", "FRN"], "WRF": ["FRN", "MSG"]}
        for p in self.pupils:
            rg = rr("enrol", p["id"])
            k = p["academy"]
            u = rg.random()
            mover = u < 0.025 + 0.02 * (p["rate"] > 15) + 0.25 * (p["rate"] > 38)
            if mover:
                h = int(rg.integers(1, 6 if p["yg"] < 11 else 3))    # year 11 moves land before the January census
                to = NEIGH[k][int(rg.integers(len(NEIGH[k])))]
                self._seq[to] += 1
                adm2 = "%s%05d" % (to[0], self._seq[to]) if to not in ("FRN", "WRF") else "%06d" % self._seq[to]
                p["enrol"] = [(k, p["adm"], 0, h), (to, adm2, h, 6)]
                self.moves.append(dict(upn=p["upn"], kind="Transfer within trust", from_k=k, to_k=to, half=h,
                                       reason=("Managed move" if rg.random() < 0.55 else "In-year transfer")))
            elif u < 0.075:
                h = int(rg.integers(1, 6))
                p["enrol"] = [(k, p["adm"], 0, h)]
                self.moves.append(dict(upn=p["upn"], kind="Leaver", from_k=k, to_k=None, half=h,
                                       reason=rg.choice(["Moved out of the area", "Moved to another school",
                                                         "Elective home education", "Moved abroad"],
                                                        p=[0.45, 0.35, 0.12, 0.08])))
            elif u < 0.115 and p["yg"] < 11:
                h = int(rg.integers(1, 6))
                p["enrol"] = [(k, p["adm"], h, 6)]
                self.moves.append(dict(upn=p["upn"], kind="In-year admission", from_k=None, to_k=k, half=h,
                                       reason=rg.choice(["Moved into the area", "From another school in the borough",
                                                         "Fair access protocol"], p=[0.5, 0.35, 0.15])))
            else:
                p["enrol"] = [(k, p["adm"], 0, 6)]
            on_roll = p["enrol"][-1][3] == 6 and p["yg"] < 11
            p["yg_now"] = p["yg"] + 1 if on_roll else p["yg"]
            p["status"] = "On roll" if on_roll else "Left"
            # sessions by half-term
            for (ak, adm, h0, h1) in p["enrol"]:
                for h in range(h0, h1):
                    if p["yg"] == 11 and h == 5:
                        continue                    # year 11 have left by the last half-term
                    poss = self.possible(ak, h)
                    fresh = len(p["enrol"]) > 1 and ak != k
                    rate = p["rate"] * (0.75 if fresh else (1.2 if len(p["enrol"]) > 1 else 1.0))
                    rate *= 1.3 if h >= 4 else 1.0          # term-time holidays in the summer term
                    rate *= float(rg.uniform(0.6, 1.4))
                    if p["yg"] == 11 and h == 4:
                        rate += 18.0 * float(rg.uniform(0.6, 1.2))    # study leave and the examination weeks
                    miss = int(min(poss, round(poss * min(rate, 95.0) / 100.0)))
                    unauth = int(round(miss * float(np.clip(rg.beta(2, 5) + 0.12 * p["dis"], 0, 1))))
                    aea = int(rg.random() < 0.06) * int(rg.integers(1, 5))
                    aea = min(aea, poss - miss)
                    self.att.append(dict(id=p["id"], upn=p["upn"], academy_now=p["enrol"][-1][0], academy=ak,
                                         adm=adm, yg=p["yg"], yg_now=p["yg_now"], status=p["status"], half=h,
                                         possible=poss, auth=miss - unauth,
                                         unauth=unauth, aea=aea, present=poss - miss - aea))

    def results(self):
        """The summer 2025 and summer 2026 series at the trust's centres: the 2025 cohort's year 11 entries, the
        2026 cohort's year 10 early entries (2025) and its year 11 entries (2026)."""
        self.res = []
        for p in self.pupils:
            if p["yg"] != 11 or p["enrol"][-1][3] < 5:
                continue                            # not in year 11, or left before the examinations
            self.entries(p, p["enrol"][-1][0], 2026)
        rg0 = rr("cohort2025")
        n = 0
        for k in K.TRUST_KEYS:                      # the 2025 cohort (year 11 in 2024/25), results only
            for i in range(int(ROLL[k] * rg0.uniform(0.9, 1.02))):
                n += 1
                dis = rg0.random() < 0.33
                q = dict(id=900000 + n, academy=k, yg=11, dis=dis, sen="N", eal=rg0.random() < 0.14,
                         rate=float(rg0.gamma(2.0, 3.0)), upn=upn(k, 12, 900000 + n), adm=None,
                         enrol=[(k, None, 0, 6)])
                self.entries(q, k, 2025)

    def entries(self, p, k, cohort):
        rg = rr("entries", cohort, p["id"])
        m = float(np.clip(rg.normal(4.6 - 0.7 * p["dis"] - 0.9 * (p["sen"] != "N") - 0.06 * (p["rate"] - 8)
                                    + {"BPK": 0.5, "RDH": 0.3, "HAL": -0.4, "MSG": -0.2}.get(k, 0.0), 1.45), 0.4, 8.6))

        def g():
            return int(np.clip(round(m + rg.normal(0, 0.9)), 1, 9))

        rows = []
        series = "June %d" % cohort
        yg = 11
        rows += [("ENL", g()), ("MAT", g())]
        if rg.random() < 0.93:
            rows.append(("ENT", g()))
        if m > 5.6 and rg.random() < 0.55:
            rows += [("BIO", g()), ("CHE", g()), ("PHY", g())]
        else:
            a, b = g(), g()
            rows.append(("CSD", "%d-%d" % (max(a, b), min(a, b))))
        if rg.random() < 0.18:
            rows.append(("CMP", g()))
        rows.append((["HIS", "GEO"][int(rg.random() < 0.45)], g()))
        if rg.random() < 0.35:
            rows.append((["FRE", "SPA"][int(rg.random() < 0.4)], g()))
        opts = ["ART", "MUS", "DRA", "RES", "FPN", "DTE", "BUS", "PEG", "TSP", "THS", "TIM", "TEN"]
        for s in rg.choice(opts, int(rg.integers(1, 4)), replace=False):
            if SUBJECTS[s][2] == "TECH":
                pts = list(TECH_POINTS)
                v = m + rg.normal(0, 1.0)
                grade = "L2D*" if v > 7.6 else "L2D" if v > 6.2 else "L2M" if v > 4.8 else "L2P" if v > 3.6 else \
                    "L1D*" if v > 2.7 else "L1D" if v > 2.0 else "L1M" if v > 1.4 else "L1P"
                rows.append((s, grade))
            else:
                rows.append((s, g()))
        for (s, gr) in rows:
            self.res.append(dict(id=p["id"], upn=p["upn"], academy=k, cohort=cohort, yg=yg, series=series, subj=s,
                                 grade=gr))
        if cohort == 2026:                          # year 10 early entries in the summer 2025 series
            for (s, share) in EARLY[k]:
                if (s in ("URD", "POL") and p["eal"] and rg.random() < 0.45) or \
                        (s not in ("URD", "POL") and rg.random() < share * (1.4 if m > 5 else 0.6)):
                    g10 = int(np.clip(round(m + rg.normal(0.6 if s in ("URD", "POL", "STA") else -0.3, 0.9)), 1, 9))
                    self.res.append(dict(id=p["id"], upn=p["upn"], academy=k, cohort=2026, yg=10,
                                         series="June 2025", subj=s, grade=g10))
                    if s not in ("STA",) and rg.random() < 0.35:   # some sit it again in year 11
                        self.res.append(dict(id=p["id"], upn=p["upn"], academy=k, cohort=2026, yg=11,
                                             series="June 2026", subj=s, grade=int(min(9, g10 + rg.integers(0, 2)))))
