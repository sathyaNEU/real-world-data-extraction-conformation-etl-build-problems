"""The providers the plan's members use, as billing NPIs: the regional hospitals and the tertiary centres in the Twin
Cities and Rochester, ambulatory surgery centres, dialysis units and skilled nursing facilities; the clinics,
specialty groups, hospital-based groups (emergency medicine, hospitalists, anesthesia, radiology, pathology),
therapists, laboratories, ambulance services and suppliers; and a tail of out-of-area providers seen on travel.
Every NPI carries a valid check digit and belongs to no real provider.

Members are sticky the way they are in a real plan: a family has a home clinic, a home hospital and a home pharmacy,
and a member who sees a specialty keeps seeing the same group."""
import math
import zlib

import numpy as np

import catalog as K
import world as W


def h(*parts):
    return zlib.crc32("|".join(str(x) for x in parts).encode())


def u01(*parts):
    return (h(*parts) + 0.5) / 2 ** 32


# specialty -> (local groups, out-of-area groups)
PROFESSIONAL = {
    "family": (9, 14), "internal": (4, 0), "pediatrics": (5, 2), "obgyn": (5, 0), "urgent": (4, 10), "emergency": (0, 12),
    "hospitalist": (0, 0), "anesthesia": (6, 2), "radiology": (5, 2), "pathology": (3, 0), "cardiology": (4, 1),
    "gastro": (3, 0), "ortho": (5, 1), "gensurg": (4, 0), "ophth": (5, 0), "ent": (3, 0), "derm": (4, 0), "endo": (2, 0),
    "rheum": (2, 0), "nephro": (2, 0), "pulm": (3, 0), "neuro": (3, 0), "neurosurg": (2, 0), "urology": (3, 0),
    "oncology": (4, 0), "radonc": (2, 0), "hematology": (1, 0), "psychiatry": (3, 0), "therapist": (20, 0), "pt": (9, 0),
    "allergy": (2, 0), "podiatry": (2, 0), "ctsurg": (2, 0), "transplant": (2, 0), "neonatology": (2, 0), "id": (1, 0),
    "pmr": (2, 0), "vascular": (1, 0), "plastic": (1, 0), "peds_sub": (3, 0), "optometry": (2, 0), "audiology": (1, 0),
    "acupuncture": (2, 0), "massage": (1, 0), "ambulance": (3, 4), "lab": (2, 0), "imaging": (2, 0), "dme": (3, 0),
}
# facilities: role -> (outpatient share of charges, inpatient charge markup, charge factor)
HOSPITALS = {"regional": (0.50, 3.0, 1.00), "community": (0.54, 2.8, 0.94), "cah1": (0.66, 2.2, 0.82),
             "cah2": (0.67, 2.3, 0.84), "tertiary_tc": (0.47, 3.6, 1.18), "childrens": (0.49, 3.4, 1.12),
             "tertiary_r": (0.46, 3.3, 1.15)}
N_TRAVEL_HOSP = 14
OTHER_FAC = {"asc": 5, "dialysis": 3, "snf": 4, "irf": 2, "homehealth": 3, "hosp_lab": 1}


class Provider:
    __slots__ = ("npi", "role", "spec", "local", "contract", "charge", "pct", "markup", "weight", "hosp")

    def __init__(self, npi, role, spec, local, contract, charge, pct=None, markup=None, weight=1.0, hosp=None):
        self.npi, self.role, self.spec, self.local = npi, role, spec, local
        self.contract, self.charge, self.pct, self.markup, self.weight, self.hosp = contract, charge, pct, markup, weight, hosp


class Directory:
    def __init__(self, seed=52311):
        r = np.random.default_rng(seed)
        used = set()

        def npi():
            while True:
                base = "1" + "%08d" % r.integers(0, 10 ** 8)
                if base not in used:
                    used.add(base)
                    return W.make_npi(base)

        self.all = []
        self.by_spec = {}
        self.hosp = {}
        for role, (pct, mk, cf) in HOSPITALS.items():
            p = Provider(npi(), role, "hospital", True, 1.0, cf * float(r.lognormal(0, 0.04)), pct, mk)
            self.hosp[role] = p
            self.all.append(p)
        self.travel_hosp = []
        for i in range(N_TRAVEL_HOSP):
            p = Provider(npi(), "travel_hosp", "hospital", False, 1.0, float(r.lognormal(math.log(1.05), 0.12)),
                         float(r.uniform(0.55, 0.68)), float(r.uniform(2.6, 3.4)), weight=1.0 / (i + 1))
            self.travel_hosp.append(p)
            self.all.append(p)
        for kind, n in OTHER_FAC.items():
            lst = []
            for i in range(n):
                p = Provider(npi(), kind, kind, True, 1.0, float(r.lognormal(0, 0.08)),
                             float(r.uniform(0.44, 0.56)) if kind == "asc" else float(r.uniform(0.5, 0.62)),
                             float(r.uniform(2.0, 2.8)), weight=1.0 / (i + 1) ** 0.9)
                lst.append(p)
                self.all.append(p)
            self.by_spec[kind] = lst
        # one emergency medicine, hospitalist, anesthesia and radiology group per local hospital
        for role in HOSPITALS:
            for spec in ("emergency", "hospitalist"):
                p = Provider(npi(), role, spec, True, float(r.normal(1.06, 0.04)), float(r.lognormal(math.log(2.3), 0.15)),
                             hosp=role)
                self.by_spec.setdefault(spec, []).append(p)
                self.all.append(p)
        for spec, (n_local, n_travel) in PROFESSIONAL.items():
            lst = self.by_spec.setdefault(spec, [])
            for i in range(n_local):
                indep = r.random() < 0.3
                contract = float(r.normal(0.98, 0.05)) if indep else float(r.normal(1.07, 0.05))
                charge = float(r.lognormal(math.log(2.05), 0.30))
                if indep and r.random() < 0.35:
                    charge = float(r.uniform(1.0, 1.25))          # a practice that bills close to the schedule
                p = Provider(npi(), "local", spec, True, contract, max(1.0, charge), weight=1.0 / (i + 1) ** 1.05)
                lst.append(p)
                self.all.append(p)
            for i in range(n_travel):
                p = Provider(npi(), "travel", spec, False, float(r.normal(1.22, 0.07)),
                             float(r.lognormal(math.log(2.4), 0.25)), weight=1.0 / (i + 1))
                lst.append(p)
                self.all.append(p)
        # hospital-based groups for anesthesia and radiology follow the hospital; pathology serves everyone
        loc = lambda s: [p for p in self.by_spec[s] if p.local]
        hroles = list(HOSPITALS)
        for i, role in enumerate(hroles):
            for spec in ("anesthesia", "radiology"):
                g = loc(spec)[i % len(loc(spec))]
                if g.hosp is None:
                    g.hosp = role
        self.npis = {p.npi for p in self.all}

    # ---------------------------------------------------------------- choices
    def local(self, spec):
        return [p for p in self.by_spec[spec] if p.local]

    def travel(self, spec):
        return [p for p in self.by_spec[spec] if not p.local]

    @staticmethod
    def pick(lst, u):
        tot = sum(p.weight for p in lst)
        acc = 0.0
        for p in lst:
            acc += p.weight / tot
            if u < acc:
                return p
        return lst[-1]

    def sticky(self, spec, key, local=True):
        """the group a member (or family) keeps seeing for a specialty"""
        lst = self.local(spec) if local else self.travel(spec)
        if not lst:
            lst = self.by_spec[spec]
        return self.pick(lst, u01("sticky", spec, key))

    def home_hospital(self, fid):
        u = u01("home_hosp", fid)
        role = "regional" if u < 0.58 else "community" if u < 0.82 else "cah1" if u < 0.92 else "cah2"
        return self.hosp[role]

    def hospital_group(self, spec, hosp):
        """the emergency, hospitalist, anesthesia or radiology group working at a hospital"""
        if not hosp.local:
            return self.pick(self.travel(spec) or self.by_spec[spec], u01("tg", spec, hosp.npi))
        for p in self.by_spec[spec]:
            if p.hosp == hosp.role:
                return p
        return self.local(spec)[h(spec, hosp.role) % len(self.local(spec))]

    def travel_hospital(self, u):
        return self.pick(self.travel_hosp, u)


# ------------------------------------------------------------------ pharmacies
class Pharmacies:
    def __init__(self, seed=52323):
        r = np.random.default_rng(seed)
        used, used_nc = set(), set()
        self.rows = []          # (npi, ncpdp, group, weight)
        for group, n, state, wt in K.PHARMACY_GROUPS:
            for i in range(n):
                while True:
                    base = "1" + "%08d" % r.integers(0, 10 ** 8)
                    if base not in used:
                        used.add(base)
                        break
                st = state or K.TRAVEL_STATES[i % len(K.TRAVEL_STATES)]
                while True:
                    nc = st + "%05d" % r.integers(10000, 99999)
                    if nc not in used_nc:
                        used_nc.add(nc)
                        break
                self.rows.append((W.make_npi(base), nc, group, wt / (i + 1) ** 0.8 if wt else 1.0 / (i + 1)))
        self.local = [i for i, x in enumerate(self.rows) if x[2] not in ("travel", "mail", "specialty")]
        self.travel = [i for i, x in enumerate(self.rows) if x[2] == "travel"]
        self.mail = [i for i, x in enumerate(self.rows) if x[2] == "mail"][0]
        self.specialty = [i for i, x in enumerate(self.rows) if x[2] == "specialty"][0]

    def home(self, fid):
        u = u01("home_pharm", fid)
        tot = sum(self.rows[i][3] for i in self.local)
        acc = 0.0
        for i in self.local:
            acc += self.rows[i][3] / tot
            if u < acc:
                return i
        return self.local[-1]

    def second(self, fid, k):
        return self.local[h("alt_pharm", fid, k) % len(self.local)]
