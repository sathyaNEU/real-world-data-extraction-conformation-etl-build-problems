"""Member hospitals' pharmacy antidote preparation records (de-identified): the clean truth and the export rows.

Acetylcysteine for acetaminophen poisoning is prepared bag by bag: the three-bag regimen gives 150, 50 and 100 mg/kg,
the two-bag regimen 200 and 100 mg/kg; a course can be stopped after its first bag or extended by a further
100 mg/kg bag. Two hospitals moved to the two-bag regimen on a date of their own. Deferoxamine for an acute iron
poisoning runs as a continuous infusion at 15 mg/kg an hour in eight-hour bags; the hospitals with a chronic
transfusion program (every one of them) also prepare deferoxamine for transfusion-dependent children, 40 mg/kg overnight on the nights
of each transfusion admission. The export carries no patient key.
"""
import datetime as dt
import numpy as np
import world

FROM, TO = dt.date(2024, 7, 1), dt.date(2026, 10, 31)
ASK_HALVES = [("2025 H1", dt.date(2025, 1, 1), dt.date(2025, 6, 30)),
              ("2025 H2", dt.date(2025, 7, 1), dt.date(2025, 12, 31)),
              ("2026 H1", dt.date(2026, 1, 1), dt.date(2026, 6, 30))]
SWITCH = {"H23": dt.date(2025, 4, 14), "H52": dt.date(2025, 11, 3)}      # two-bag regimen from this date
NAC_RATE = {"H11": 42.0, "H23": 50.0, "H34": 61.0, "H52": 36.0}          # courses a half-year
DFO_RATE = {"H11": 2.6, "H23": 3.4, "H34": 4.0, "H52": 2.2}             # acute iron courses a half-year
CHRONIC = {"H11": [21.0, 33.5], "H23": [16.5, 23.0, 31.5], "H34": [14.0, 19.5, 27.0, 38.0],
           "H52": [12.5, 26.0]}      # transfusion-dependent children's weights
AREAS = ["Pediatric intensive care", "Pediatric ward", "Emergency department"]


def _weight(rng):
    band = rng.random()
    if band < 0.36:
        return float(rng.uniform(8.5, 18.0))
    if band < 0.52:
        return float(rng.uniform(18.0, 38.0))
    return float(rng.uniform(40.0, 82.0))


def _r10(x):
    return int(round(x / 10.0)) * 10


def simulate(seed):
    rng = np.random.default_rng(seed)
    nac, dfo, bags = [], [], []
    days = (TO - FROM).days + 1
    for h, _, _, _, _ in world.HOSPITALS:
        # acetylcysteine courses
        n = rng.poisson(NAC_RATE[h] * days / 182.6)
        starts = sorted(FROM + dt.timedelta(minutes=int(m)) for m in rng.integers(0, days * 1440, n))
        weights_live = []
        for t0d in starts:
            t0 = dt.datetime.combine(t0d, dt.time(0)) + dt.timedelta(minutes=int(rng.integers(0, 1440)))
            # weights of concurrent courses at the hospital are at least 0.6 kg apart, so each bag fits one course
            for _ in range(50):
                w = round(_weight(rng), 1)
                if all(abs(w - w2) >= 0.6 for (w2, end) in weights_live if end > t0):
                    break
            two = h in SWITCH and t0.date() >= SWITCH[h]
            stopped = rng.random() < 0.05
            extended = (not stopped) and rng.random() < 0.26
            if two:
                plan = [(200, 0.0)] + ([] if stopped else [(100, rng.uniform(3.4, 4.2))])
                if extended:
                    plan.append((100, rng.uniform(19.2, 20.4)))
            else:
                plan = [(150, 0.0)] + ([] if stopped else [(50, rng.uniform(0.55, 1.1)), (100, rng.uniform(4.3, 5.2))])
                if extended:
                    plan.append((100, rng.uniform(20.0, 21.4)))
            if h == "H34" and not stopped and not two:
                # this pharmacy makes the second and third bags together once the first is up
                plan = [plan[0], (50, 0.45), (100, 0.47)] + plan[3:]
            wcap = min(w, 100.0)
            course = dict(hospital=h, start=t0, weight=w, regimen="two-bag" if two else "three-bag",
                          stopped=stopped, extended=extended, bags=[])
            for mgkg, hrs in plan:
                t = t0 + dt.timedelta(minutes=int(round(hrs * 60)) + int(rng.integers(0, 9)))
                b = dict(hospital=h, time=t, drug="Acetylcysteine", dose=_r10(mgkg * wcap), course=len(nac),
                         area=AREAS[int(rng.choice(3, p=[0.35, 0.45, 0.20]))])
                course["bags"].append(b)
                bags.append(b)
            weights_live.append((w, t0 + dt.timedelta(hours=22)))
            nac.append(course)
        # acute iron courses: 15 mg/kg/h, eight-hour bags, eight to twenty-four hours
        n = rng.poisson(DFO_RATE[h] * days / 182.6)
        for t0d in sorted(FROM + dt.timedelta(days=int(d)) for d in rng.integers(0, days, n)):
            t0 = dt.datetime.combine(t0d, dt.time(0)) + dt.timedelta(minutes=int(rng.integers(0, 1440)))
            w = round(float(rng.uniform(9.0, 19.0)), 1)
            nb = int(rng.choice([1, 2, 3], p=[0.25, 0.45, 0.30]))
            course = dict(hospital=h, start=t0, weight=w, kind="acute", bags=[])
            for j in range(nb):
                t = t0 + dt.timedelta(hours=8 * j, minutes=int(rng.integers(-25, 15)) if j else 0)
                b = dict(hospital=h, time=t, drug="Deferoxamine", dose=_r10(15 * w * 8), course=("dfo", len(dfo)),
                         area=AREAS[int(rng.choice(3, p=[0.55, 0.35, 0.10]))])
                course["bags"].append(b)
                bags.append(b)
            dfo.append(course)
        # chronic chelation during transfusion admissions: 40 mg/kg over ten hours on two or three nights
        for w in CHRONIC.get(h, []):
            day = FROM + dt.timedelta(days=int(rng.integers(0, 24)))
            while day <= TO:
                nights = int(rng.choice([2, 3], p=[0.4, 0.6]))
                for j in range(nights):
                    t = dt.datetime.combine(day + dt.timedelta(days=j), dt.time(19, 0)) + \
                        dt.timedelta(minutes=int(rng.integers(0, 110)))
                    b = dict(hospital=h, time=t, drug="Deferoxamine", dose=_r10(40 * w), course=("chronic", w),
                             area="Pediatric ward")
                    bags.append(b)
                w = round(w + float(rng.uniform(0.0, 0.25)), 2)
                day = day + dt.timedelta(days=int(rng.integers(21, 30)))
    bags.sort(key=lambda b: (b["time"], b["hospital"], b["drug"]))
    return dict(nac=nac, dfo=dfo, bags=bags)


def rows(truth, seed):
    rng = np.random.default_rng(seed)
    out = []
    for b in truth["bags"]:
        if not (FROM <= b["time"].date() <= TO):
            continue
        prod = "Acetylcysteine injection 200 mg/mL (6 g/30 mL vial)" if b["drug"] == "Acetylcysteine" else \
            "Deferoxamine mesylate for injection (2 g vial)"
        diluent = "Dextrose 5%" if b["drug"] == "Acetylcysteine" else "Sodium chloride 0.9%"
        out.append([b["hospital"], b["time"].strftime("%Y-%m-%d %H:%M"), prod, str(b["dose"]), diluent,
                    "Pharmacist" if rng.random() < 0.62 else "Pharmacy technician"])
    return out


def ask_truth(truth):
    """The ask figures from the clean truth: acetylcysteine courses and deferoxamine courses for an iron poisoning
    started, per hospital and half-year (a course falls in the half-year of its first bag)."""
    nac_courses, dfo_courses = {}, {}
    for h, _, _, _, _ in world.HOSPITALS:
        for lab, a, b in ASK_HALVES:
            nac_courses[(h, lab)] = sum(1 for c in truth["nac"] if c["hospital"] == h and a <= c["start"].date() <= b)
            dfo_courses[(h, lab)] = sum(1 for c in truth["dfo"] if c["hospital"] == h and a <= c["start"].date() <= b)
    return nac_courses, dfo_courses
