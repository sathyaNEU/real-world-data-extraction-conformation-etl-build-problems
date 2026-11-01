"""The clean truth of the Corrowan Valley world: cameras and their placements, the validation study, the
reference year's screenings, and the records the asks read. Nothing here is written to target/; pack.py does that.

Every draw comes from one numpy Generator per stream, seeded from params.SEED, so two builds are identical."""
import datetime as dt
import math

import numpy as np

import params as P

D = dt.date


def logistic(x):
    return 1.0 / (1.0 + math.exp(-x))


def daterange(a, b):
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)


def is_clinic_day(d, code):
    """Retinal screening runs Monday to Friday, closed on the network's holidays."""
    if d.weekday() >= 5:
        return False
    return d not in HOLIDAYS


HOLIDAYS = {D(2025, 1, 1), D(2025, 1, 20), D(2025, 5, 26), D(2025, 6, 19), D(2025, 7, 4), D(2025, 9, 1),
            D(2025, 11, 11), D(2025, 11, 27), D(2025, 11, 28), D(2025, 12, 25), D(2026, 1, 1), D(2026, 1, 19),
            D(2026, 5, 25), D(2026, 6, 19), D(2026, 7, 3), D(2026, 9, 7)}

# ---------------------------------------------------------------------------------------------------------------
# The camera fleet. Each placement is (serial, location code, from, to or None, reason). Swaps happen on a Saturday
# or a holiday, so a placement's last day and the next one's first day never carry a screening.
CAMERAS = [
    # serial            model    purchased        status at 2026-09-30
    ("HO-NR40-180317", "NR-40", D(2018, 4, 9)),
    ("HO-NR40-180322", "NR-40", D(2018, 4, 9)),
    ("HO-NR40-180355", "NR-40", D(2018, 5, 21)),
    ("HO-NR40-180381", "NR-40", D(2018, 5, 21)),
    ("HO-NR40-181014", "NR-40", D(2018, 11, 5)),
    ("HO-NR40-181027", "NR-40", D(2018, 11, 5)),
    ("HO-NR40-190208", "NR-40", D(2019, 3, 18)),
    ("HO-NR40-190219", "NR-40", D(2019, 3, 18)),
    ("HO-NR40-190466", "NR-40", D(2019, 8, 12)),
    ("HO-NR40-190470", "NR-40", D(2019, 8, 12)),
    ("HO-NR40-190502", "NR-40", D(2019, 9, 30)),
    ("HO-NR40-190533", "NR-40", D(2019, 9, 30)),
    ("HO-NR40-190547", "NR-40", D(2019, 10, 14)),
    ("HO-NR70-241188", "NR-70", D(2024, 11, 25)),
    ("HO-NR70-241193", "NR-70", D(2024, 11, 25)),
    ("HO-NR70-250240", "NR-70", D(2025, 1, 27)),
    ("HO-NR70-250251", "NR-70", D(2025, 1, 27)),
    ("HO-NR70-250677", "NR-70", D(2025, 6, 30)),
    ("HO-NR70-250689", "NR-70", D(2025, 6, 30)),
    ("HO-NR70-250694", "NR-70", D(2025, 6, 30)),
    ("HO-NR70-250912", "NR-70", D(2025, 9, 15)),
    ("HO-NR70-250931", "NR-70", D(2025, 9, 15)),
    ("HO-NR70-251130", "NR-70", D(2025, 10, 6)),
]
MODEL = {s: m for s, m, _ in CAMERAS}

PLACEMENTS = [
    # Wendmere (pilot A): the NR-40 until the NR-70 went in on Saturday 8 February 2025
    ("HO-NR40-180317", "WM", D(2018, 4, 23), D(2025, 2, 8), "Replaced"),
    ("HO-NR70-250240", "WM", D(2025, 2, 8), None, "New installation"),
    # Quarry Hill (pilot B): NR-70 from December 2024, out for repair 12 April to 3 May 2025 with an NR-40 loaner
    ("HO-NR40-180322", "QH", D(2018, 4, 23), D(2024, 12, 14), "Replaced"),
    ("HO-NR70-241188", "QH", D(2024, 12, 14), D(2025, 4, 12), "Out for repair"),
    ("HO-NR40-190547", "QH", D(2025, 4, 12), D(2025, 5, 3), "Loaner"),
    ("HO-NR70-241188", "QH", D(2025, 5, 3), None, "Returned from repair"),
    # Yarrowby (pilot C): NR-40 to 22 February 2025, NR-70 after, an NR-40 loaner 7 to 21 June 2025 and 9 to 30 May 2026
    ("HO-NR40-180355", "YB", D(2018, 6, 4), D(2025, 2, 1), "Replaced"),
    ("HO-NR70-250251", "YB", D(2025, 2, 1), D(2025, 6, 7), "Out for repair"),
    ("HO-NR40-190547", "YB", D(2025, 6, 7), D(2025, 6, 21), "Loaner"),
    ("HO-NR70-250251", "YB", D(2025, 6, 21), D(2026, 5, 9), "Returned from repair"),
    ("HO-NR40-190502", "YB", D(2026, 5, 9), D(2026, 5, 30), "Loaner"),
    ("HO-NR70-250251", "YB", D(2026, 5, 30), None, "Returned from repair"),
    # Orrin Falls: NR-70 from July 2025; an NR-40 loaner 14 February to 7 March 2026
    ("HO-NR40-180381", "OF", D(2018, 6, 4), D(2025, 7, 19), "Replaced"),
    ("HO-NR70-250677", "OF", D(2025, 7, 19), D(2026, 2, 14), "Out for repair"),
    ("HO-NR40-190502", "OF", D(2026, 2, 14), D(2026, 3, 7), "Loaner"),
    ("HO-NR70-250677", "OF", D(2026, 3, 7), None, "Returned from repair"),
    # Thistlebrook: NR-70 from September 2025
    ("HO-NR40-181014", "TB", D(2018, 11, 19), D(2025, 9, 20), "Replaced"),
    ("HO-NR70-250912", "TB", D(2025, 9, 20), None, "New installation"),
    # Pellsbury: NR-70 from July 2025; an NR-40 loaner 13 June to 18 July 2026
    ("HO-NR40-181027", "PB", D(2018, 11, 19), D(2025, 7, 26), "Replaced"),
    ("HO-NR70-250689", "PB", D(2025, 7, 26), D(2026, 6, 13), "Out for repair"),
    ("HO-NR40-190466", "PB", D(2026, 6, 13), D(2026, 7, 18), "Loaner"),
    ("HO-NR70-250689", "PB", D(2026, 7, 18), None, "Returned from repair"),
    # Rookwood: still on its NR-40 (replacement deferred to FY2027)
    ("HO-NR40-190208", "RW", D(2019, 4, 1), None, "New installation"),
    # Sallow Creek: NR-40 to 8 November 2025, NR-70 after; an NR-40 loaner 4 to 25 April 2026
    ("HO-NR40-190219", "SC", D(2019, 4, 1), D(2025, 10, 18), "Replaced"),
    ("HO-NR70-251130", "SC", D(2025, 10, 18), D(2026, 4, 4), "Out for repair"),
    ("HO-NR40-190470", "SC", D(2026, 4, 4), D(2026, 4, 25), "Loaner"),
    ("HO-NR70-251130", "SC", D(2026, 4, 25), None, "Returned from repair"),
    # Veldane: NR-70 from July 2025; failed 10 March 2026, on an NR-40 loaner since 14 March (board on back-order)
    ("HO-NR40-190466", "VD", D(2019, 8, 26), D(2025, 7, 19), "Replaced"),
    ("HO-NR70-250694", "VD", D(2025, 7, 19), D(2026, 5, 2), "Out for repair"),
    ("HO-NR40-190533", "VD", D(2026, 5, 2), None, "Loaner"),
    # Brackenfield: still on its NR-40
    ("HO-NR40-190470", "BF", D(2019, 8, 26), D(2026, 4, 4), "Moved"),
    ("HO-NR40-180381", "BF", D(2026, 4, 4), None, "Moved"),
    # Kestle Road: NR-70 from September 2025; failed 7 February 2026, on an NR-40 loaner since
    ("HO-NR40-190502", "KN", D(2019, 10, 14), D(2025, 9, 20), "Replaced"),
    ("HO-NR70-250931", "KN", D(2025, 9, 20), D(2026, 4, 25), "Out for repair"),
    ("HO-NR40-181014", "KN", D(2026, 4, 25), None, "Loaner"),
    # Hollinmoor: still on its NR-40
    ("HO-NR40-180355", "HM", D(2025, 2, 1), None, "Moved"),
]


def camera_on(code, d):
    """The serial in place at clinic `code` on date `d` (a screening day, never a swap day)."""
    hits = [s for s, c, a, b, _ in PLACEMENTS if c == code and a <= d and (b is None or d < b)]
    assert len(hits) == 1, (code, d, hits)
    return hits[0]


FAULTS = [
    # (serial, location, fault date (a clinic day), swap Saturday the loaner went in, repair note)
    ("HO-NR70-250677", "OF", D(2026, 2, 10), D(2026, 2, 14), "Flash module fault"),
    ("HO-NR70-250694", "VD", D(2026, 4, 23), D(2026, 5, 2), "Sensor board failure, part on back-order"),
    ("HO-NR70-250931", "KN", D(2026, 4, 15), D(2026, 4, 25), "Sensor board failure, part on back-order"),
    ("HO-NR70-251130", "SC", D(2026, 3, 30), D(2026, 4, 4), "Joystick and focus drive fault"),
    ("HO-NR70-250251", "YB", D(2026, 5, 1), D(2026, 5, 9), "Flash module fault"),
    ("HO-NR70-250689", "PB", D(2026, 6, 3), D(2026, 6, 13), "Chin rest motor and alignment"),
]


# ---------------------------------------------------------------------------------------------------------------
AGE_BANDS = ["18-44", "45-64", "65-74", "75+"]
A1C_BANDS = ["<7.0", "7.0-8.9", "9.0+"]
ETHN = ["Hispanic or Latino", "Not Hispanic or Latino", "Declined"]


class World:
    def __init__(self, seed=P.SEED):
        self.seed = seed
        ss = np.random.SeedSequence(seed)
        kids = ss.spawn(14)
        self.rng = {k: np.random.default_rng(s) for k, s in zip(
            ["val", "dep", "pat", "grade", "orders", "reads", "registry", "outside", "tickets", "dash", "survey",
             "misc", "manual", "extra"], kids)}
        self.clinic = {c[0]: c for c in P.CLINICS}
        self.make_patients()
        self.make_validation()
        self.make_screenings()

    # patients: each clinic's registered patients with diabetes; a stable identity across files
    def make_patients(self):
        r = self.rng["pat"]
        self.patients = []
        mrn_used = set()
        for code, _, _, _, screens, prev in P.CLINICS:
            n = int(screens * 1.37)          # registry larger than the year's screens
            for i in range(n):
                while True:
                    mrn = int(r.integers(1_020_000, 1_980_000))
                    if mrn not in mrn_used:
                        mrn_used.add(mrn)
                        break
                age = r.choice(AGE_BANDS, p=[0.17, 0.52, 0.19, 0.12])
                self.patients.append({
                    "mrn": mrn, "clinic": code, "age": str(age),
                    "sex": "F" if r.random() < 0.53 else "M",
                    "dtype": "Type 1" if r.random() < 0.06 else "Type 2",
                    "a1c": str(r.choice(A1C_BANDS, p=[0.38, 0.41, 0.21])),
                    "eth": str(r.choice(ETHN, p=[0.36, 0.58, 0.06])),
                    "ref": bool(r.random() < prev),
                })
        self.by_clinic = {}
        for p in self.patients:
            self.by_clinic.setdefault(p["clinic"], []).append(p)

    def ai_read(self, r, model, referable, age):
        """Return (ungradable, score) for one screening on camera `model`. Exactly two draws per read whatever
        the model, so moving a screening between cameras changes that read alone and no later draw."""
        u = r.random()
        z = r.normal(0.0, 1.0)
        if u < P.UNGRADABLE[model]:
            return True, None
        if referable:
            lat = P.MU_REF[model] + (P.MU_REF_AGE75 if age == "75+" else 0.0) + P.SD_REF * z
        else:
            lat = P.MU_NON + z
        score = int(round(100 * logistic(lat)))
        return False, min(max(score, 0), 100)

    def make_validation(self):
        r = self.rng["val"]
        days = {lab: [d for d in daterange(P.VAL_START, P.VAL_END) if is_clinic_day(d, code)]
                for lab, code in P.PILOTS.items()}
        n_by = {"A": 1176, "B": 1114, "C": 1121}
        self.validation = []
        sid = 0
        for lab in ["A", "B", "C"]:
            code = P.PILOTS[lab]
            pool = self.by_clinic[code]
            idx = r.permutation(len(pool))[:n_by[lab]]
            dd = sorted(r.choice(len(days[lab]), size=n_by[lab], replace=True))
            for k, (j, di) in enumerate(zip(idx, dd)):
                p = pool[j]
                d = days[lab][di]
                ser = camera_on(code, d)
                model = MODEL[ser]
                ung, score = self.ai_read(r, model, p["ref"], p["age"])
                sid += 1
                self.validation.append({"sid": sid, "site": lab, "clinic": code, "date": d, "patient": p,
                                        "serial": ser, "model": model, "ungradable": ung, "score": score})
        # reference grading: the truth is the patient's referable state; graders' levels are drawn around it
        g = self.rng["grade"]
        for v in self.validation:
            ref = v["patient"]["ref"]
            if ref:
                lvl = g.choice(["moderate NPDR", "severe NPDR", "PDR"], p=[0.71, 0.19, 0.10])
                dme = bool(g.random() < 0.31) if lvl != "moderate NPDR" else bool(g.random() < 0.18)
                if g.random() < 0.09:          # referable on macular edema alone
                    lvl, dme = str(g.choice(["no DR", "mild NPDR"], p=[0.35, 0.65])), True
            else:
                lvl = g.choice(["no DR", "mild NPDR"], p=[0.74, 0.26])
                dme = False
            v["adjudicated"] = str(lvl)
            v["dme"] = dme
            # two independent graders; a disagreement on referability goes to adjudication
            g1, g2 = str(lvl), str(lvl)
            if g.random() < 0.07:
                g1 = self._neighbour(g, str(lvl))
            if g.random() < 0.07:
                g2 = self._neighbour(g, str(lvl))
            v["g1"], v["g2"] = g1, g2
            v["adjudicated_flag"] = (self._refgrade(g1, dme) != self._refgrade(g2, dme))
            order = ["no DR", "mild NPDR", "moderate NPDR", "severe NPDR", "PDR"]
            if g1 == g2:
                v["final"] = g1                       # agreement stands
            elif not v["adjudicated_flag"]:
                v["final"] = max(g1, g2, key=order.index)   # same referability: the more severe level
            else:
                v["final"] = str(lvl)                 # the retina specialist's adjudicated level
            v["quality"] = None

    @staticmethod
    def _refgrade(lvl, dme):
        return dme or lvl in ("moderate NPDR", "severe NPDR", "PDR")

    @staticmethod
    def _neighbour(g, lvl):
        order = ["no DR", "mild NPDR", "moderate NPDR", "severe NPDR", "PDR"]
        i = order.index(lvl)
        j = i + (1 if (i == 0 or (i < 4 and g.random() < 0.5)) else -1)
        return order[max(0, min(4, j))]

    def make_screenings(self):
        """Every AI screening in the reference year. A patient is screened at most once a year, a few twice."""
        r = self.rng["dep"]
        self.screens = []
        acc = 0
        for code, _, _, _, n, prev in P.CLINICS:
            days = [d for d in daterange(P.REF_START, P.REF_END) if is_clinic_day(d, code)]
            pool = self.by_clinic[code]
            idx = r.permutation(len(pool))[:n]
            dd = sorted(r.choice(len(days), size=n, replace=True))
            for j, di in zip(idx, dd):
                p = pool[j]
                d = days[di]
                ser = camera_on(code, d)
                model = MODEL[ser]
                ung, score = self.ai_read(r, model, p["ref"], p["age"])
                # local clinic time of the capture: 7:40 to 17:50 Pacific, weighted to the morning
                mins = int(np.clip(r.normal(11.3 * 60, 150), 7 * 60 + 40, 17 * 60 + 50))
                acc += 1
                self.screens.append({"clinic": code, "date": d, "minute": mins, "patient": p, "serial": ser,
                                     "model": model, "ungradable": ung, "score": score})
        # patients screened away from their home clinic (a visit at a nearer or open clinic); the read is redrawn for
        # the visiting patient from its own stream, so no other screening's draw moves
        m = self.rng["misc"]
        partner = {"SC": "KN", "KN": "SC", "TB": "QH", "QH": "TB", "OF": "WM", "WM": "OF", "PB": "BF", "BF": "PB",
                   "RW": "VD", "VD": "RW", "YB": "HM", "HM": "YB"}
        codes = [c[0] for c in P.CLINICS]
        for s in self.screens:
            if m.random() < P.VISIT_SHARE:
                other = partner[s["clinic"]] if m.random() < 0.7 else codes[int(m.integers(0, len(codes)))]
                if other == s["clinic"]:
                    other = partner[s["clinic"]]
                pool = self.by_clinic[other]
                p = pool[int(m.integers(0, len(pool)))]
                s["patient"] = p
                s["ungradable"], s["score"] = self.ai_read(m, s["model"], p["ref"], p["age"])
        # a camera fault stops screening at the clinic from the next clinic day until the loaner goes in on the
        # Saturday; the screenings booked on those days were cancelled and rebooked (they become cancelled orders)
        down = set()
        for serial, loc, fault, swap, note in FAULTS:
            d = fault + dt.timedelta(days=1)
            while d < swap:
                if is_clinic_day(d, loc):
                    down.add((loc, d))
                d += dt.timedelta(days=1)
        self.downdays = down
        # on the fault day itself the camera failed at 13:00; later screenings that day were cancelled too
        faultday = {(loc, fault) for serial, loc, fault, swap, note in FAULTS}
        keep, self.cancelled = [], []
        for s in self.screens:
            if (s["clinic"], s["date"]) in down or ((s["clinic"], s["date"]) in faultday and s["minute"] >= 13 * 60):
                self.cancelled.append(s)
            else:
                keep.append(s)
        self.screens = keep
        self.screens.sort(key=lambda s: (s["date"], s["minute"], s["clinic"]))
        for i, s in enumerate(self.screens):
            s["k"] = i


# ---------------------------------------------------------------------------------------------------------------
# Records the asks read. They share the patients and screenings above but none of them is read by the main call.


def make_ask_records(w):
    # registry patients who were never in a clinic's screening pool (patients new to the network, patients who are
    # seen rarely); their share differs by clinic
    x = w.rng["extra"]
    used = set(p["mrn"] for p in w.patients)
    for code, _, _, _, n, prev in P.CLINICS:
        k = int(round(n * P.REGISTRY_EXTRA[code]))
        for i in range(k):
            while True:
                mrn = int(x.integers(1_020_000, 1_980_000))
                if mrn not in used:
                    used.add(mrn)
                    break
            w.patients.append({
                "mrn": mrn, "clinic": code, "age": str(x.choice(AGE_BANDS, p=[0.21, 0.50, 0.18, 0.11])),
                "sex": "F" if x.random() < 0.52 else "M", "dtype": "Type 1" if x.random() < 0.05 else "Type 2",
                "a1c": str(x.choice(A1C_BANDS, p=[0.33, 0.40, 0.27])), "eth": str(x.choice(ETHN, p=[0.38, 0.55, 0.07])),
                "ref": bool(x.random() < prev), "extra": True})
    r = w.rng["registry"]
    # registry at 30 Sep 2026: active patients with diabetes by home clinic. A few charts were merged during the
    # year: the surviving MRN is the registry's, the retired MRN stays on documents filed before the merge.
    w.merges = []
    retired_used = set(p["mrn"] for p in w.patients)
    for p in w.patients:
        p["active"] = bool(r.random() > 0.035)
        p["retired_mrn"] = None
        if r.random() < 0.028:
            while True:
                old = int(r.integers(1_020_000, 1_980_000))
                if old not in retired_used:
                    retired_used.add(old)
                    break
            md = D(2025, 10, 1) + dt.timedelta(days=int(r.integers(20, 350)))
            p["retired_mrn"] = old
            p["merge_date"] = md
            w.merges.append((old, p["mrn"], md))
    screened = {}
    for s in w.screens:
        screened.setdefault(s["patient"]["mrn"], []).append(s)
    # patients with retinopathy already diagnosed are not screened by the AI; their clinic photographs them for a
    # teleretinal read by the reading center instead (a routine read, ordered as retinal photography)
    mr = w.rng["manual"]
    w.manual = []
    for code, _, _, _, n, prev in P.CLINICS:
        pool = [p for p in w.by_clinic[code] if p["mrn"] not in screened]
        k = int(round(P.MANUAL_SHARE * n * (0.85 + 0.3 * mr.random())))
        pick = mr.permutation(len(pool))[:k]
        days = [d for d in daterange(P.REF_START, P.REF_END) if is_clinic_day(d, code)]
        for j in pick:
            p = pool[j]
            p["known_dr"] = True
            d = days[int(mr.integers(0, len(days)))]
            mins = int(np.clip(mr.normal(11.0 * 60, 140), 7 * 60 + 40, 17 * 60 + 30))
            w.manual.append({"patient": p, "clinic": code, "date": d, "minute": mins,
                             "grade": str(mr.choice(["Referable", "Not referable", "Insufficient for grading"],
                                                    p=[0.68, 0.29, 0.03])),
                             "lag": int(mr.choice([5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 19, 23]))})
    # outside eye examinations (optometrists, ophthalmologists) for patients not screened by the AI this year,
    # plus a few for screened patients; each faxed report is indexed by HIM on receipt
    o = w.rng["outside"]
    w.outside = []
    for p in w.patients:
        base = 0.55 if p.get("known_dr") else (P.OUTSIDE_RATE[p["clinic"]] if p["mrn"] not in screened else 0.04)
        u, off, lag = o.random(), int(o.integers(0, 455)), int(o.integers(3, 41))     # three draws per patient
        if u < base:
            exam = D(2025, 8, 1) + dt.timedelta(days=off)
            recv = exam + dt.timedelta(days=lag)
            filed_under = p["mrn"]
            if p["retired_mrn"] is not None and recv < p["merge_date"]:
                filed_under = p["retired_mrn"]
            w.outside.append({"patient": p, "exam": exam, "received": recv, "mrn": filed_under})
    # the reading center: every AI referral (Referable or Ungradable at the Standard point) is sent for an overread
    # unless the referral is cancelled first. An "insufficient for grading" read sends the patient back to be
    # re-photographed; the new photographs are a new reading-center case under the same referral order.
    rd = w.rng["reads"]
    cut = dict(P.OPS)["Standard"]
    w.cases = []
    w.unread = []
    case_no = 400_000
    order_no = 7_100_000
    for s in w.screens:
        ref = s["ungradable"] or (s["score"] is not None and s["score"] >= cut)
        s["referred"] = bool(ref)
        if not ref:
            continue
        order_no += int(rd.integers(1, 9))
        s["ref_order"] = order_no
        truth = s["patient"]["ref"]
        lag = int(rd.choice([1, 2, 2, 3, 3, 4, 5, 6, 8, 11]))
        insufficient = rd.random() < (0.25 if s["ungradable"] else 0.04)
        if rd.random() < P.NOT_READ:
            s["ref_cancel"] = str(rd.choice(["Patient seen by outside ophthalmology", "Patient declined",
                                             "Duplicate referral"], p=[0.6, 0.3, 0.1]))
            w.unread.append(s)
            continue
        case_no += int(rd.integers(1, 7))
        first = {"case": case_no, "screen": s, "order": order_no, "opened": s["date"], "kind": "ai",
                 "result_date": s["date"] + dt.timedelta(days=lag), "clinic": s["clinic"],
                 "grade": "Insufficient for grading" if insufficient else ("Referable" if truth else "Not referable"),
                 "reimage_of": None}
        w.cases.append(first)
        if insufficient:
            # recalled and re-photographed 9 to 40 days later at the same clinic; the second case closes the referral
            gap = int(rd.integers(9, 41))
            d2 = s["date"] + dt.timedelta(days=gap)
            while not is_clinic_day(d2, s["clinic"]):
                d2 += dt.timedelta(days=1)
            lag2 = int(rd.choice([1, 2, 2, 3, 4, 6]))
            case_no += int(rd.integers(1, 7))
            w.cases.append({"case": case_no, "screen": None, "order": order_no, "opened": d2, "kind": "reimage",
                            "result_date": d2 + dt.timedelta(days=lag2), "clinic": s["clinic"],
                            "grade": "Referable" if truth else "Not referable", "reimage_of": first["case"],
                            "minute": int(rd.integers(8 * 60, 16 * 60))})
    # the teleretinal reads join the same case sequence in date order
    for mcase in sorted(w.manual, key=lambda x: (x["date"], x["minute"], x["clinic"])):
        w.cases.append({"case": None, "screen": None, "order": None, "opened": mcase["date"], "kind": "manual",
                        "result_date": mcase["date"] + dt.timedelta(days=mcase["lag"]), "clinic": mcase["clinic"],
                        "grade": mcase["grade"], "reimage_of": None, "minute": mcase["minute"],
                        "patient": mcase["patient"]})
    w.cases.sort(key=lambda c: (c["opened"], c["case"] if c["case"] is not None else 10**9))
    seq = 400_000
    remap = {}
    for c in w.cases:
        seq += int(rd.integers(1, 7))
        if c["case"] is not None:
            remap[c["case"]] = seq
        c["case"] = seq
    for c in w.cases:
        if c["reimage_of"] is not None:
            c["reimage_of"] = remap[c["reimage_of"]]
    # biomed service tickets: every asset class at every location; camera faults carry the dates in FAULTS
    t = w.rng["tickets"]
    w.tickets = []
    tno = 52_000
    for serial, loc, fault, swap, note in FAULTS:
        tno += int(t.integers(3, 40))
        back = [b for s_, c, a, b, rsn in PLACEMENTS if s_ == serial and c == loc and a <= fault and
                (b is None or fault < b)]
        ret = [a for s_, c, a, b, rsn in PLACEMENTS if s_ == serial and c == loc and a > fault]
        closed = ret[0] if ret else None
        w.tickets.append({"ticket": tno, "serial": serial, "loc": loc, "opened": fault, "closed": closed,
                          "class": "Retinal camera, non-mydriatic", "note": note})
    return w
