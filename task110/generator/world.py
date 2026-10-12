"""The Yacaaba Radiology world: the register as it really stands (with the legacy truth attached),
the capital approvals, the Bremer transfer, the verification events. Deterministic from params.SEED."""
import datetime as dt
import random
from decimal import Decimal

import ledger as L
from params import SEED, SITES

D = Decimal


def money(rng, lo, hi):
    return D(int(rng.uniform(lo, hi))) + D(rng.randint(0, 99)) / 100


def rdate(rng, a, b):
    return a + dt.timedelta(days=rng.randint(0, (b - a).days))


def day(y, m, d):
    return dt.date(y, m, d)


# ------------------------------------------------------------------------------- the fleet
# major imaging systems: key -> (site, description, acquired, cost range, supplier, serial prefix)
HOSTS = [
    ("MAI-MRI", "MAI", "MRI 1.5T - MAGNETOM Aera", day(2016, 11, 14), (1.96e6, 2.04e6), "Siemens Healthcare Pty Ltd", "AE"),
    ("CHA-CT", "CHA", "CT 128-slice - SOMATOM Definition AS+", day(2017, 1, 19), (1.16e6, 1.24e6), "Siemens Healthcare Pty Ltd", "CT"),
    ("CHA-FL", "CHA", "Fluoroscopy room - Luminos dRF", day(2017, 1, 24), (0.58e6, 0.63e6), "Siemens Healthcare Pty Ltd", "LU"),
    ("MAI-XR0", "MAI", "General X-ray room - DigitalDiagnost", day(2016, 11, 9), (0.29e6, 0.32e6), "Philips Electronics Australia", "DD"),
    ("CHA-XR1", "CHA", "General X-ray room 1 - DigitalDiagnost", day(2016, 12, 6), (0.30e6, 0.33e6), "Philips Electronics Australia", "DD"),
    ("MAI-CT", "MAI", "CT 64-slice - Revolution EVO", day(2017, 3, 8), (0.81e6, 0.86e6), "GE Healthcare Australia", "RE"),
    ("MAI-MG", "MAI", "Mammography - Senographe Pristina", day(2017, 8, 2), (0.41e6, 0.44e6), "GE Healthcare Australia", "SP"),
    ("CHA-MG", "CHA", "Mammography - MAMMOMAT Revelation", day(2018, 2, 6), (0.43e6, 0.47e6), "Siemens Healthcare Pty Ltd", "MR"),
    ("CES-CT", "CES", "CT 64-slice - Revolution EVO", day(2018, 11, 21), (0.79e6, 0.85e6), "GE Healthcare Australia", "RE"),
    ("CHA-MRI3", "CHA", "MRI 3T - MAGNETOM Vida", day(2019, 4, 11), (3.12e6, 3.28e6), "Siemens Healthcare Pty Ltd", "VI"),
    ("CHA-XR2", "CHA", "General X-ray room 2 - Ysio Max", day(2019, 6, 17), (0.34e6, 0.37e6), "Siemens Healthcare Pty Ltd", "YM"),
    ("CES-XR", "CES", "General X-ray room - Ysio Max", day(2020, 2, 12), (0.33e6, 0.36e6), "Siemens Healthcare Pty Ltd", "YM"),
    ("RAY-CT", "RAY", "CT 32-slice - Aquilion Lightning", day(2021, 5, 17), (0.63e6, 0.68e6), "Canon Medical Systems ANZ", "AL"),
    ("RAY-XR", "RAY", "General X-ray room - Radrex-i", day(2022, 7, 25), (0.34e6, 0.36e6), "Canon Medical Systems ANZ", "RX"),
]

# upgrades fitted to a system: (host key, description, acquired, cost range)
# the legacy ledger spread each over the months its host had left
UPGRADES = [
    ("MAI-MRI", "Coil package - 18ch body, 32ch head and spine", day(2023, 3, 16), (372e3, 392e3)),
    ("MAI-MRI", "Software upgrade syngo MR XA51 with BioMatrix tuners", day(2023, 9, 7), (158e3, 168e3)),
    ("CHA-CT", "Detector and reconstruction upgrade - Stellar / ADMIRE", day(2023, 2, 2), (532e3, 556e3)),
    ("CHA-FL", "Imaging chain upgrade - flat detector and dose package", day(2023, 4, 20), (247e3, 259e3)),
    ("MAI-XR0", "DR detector retrofit - wireless flat panel", day(2023, 1, 23), (126e3, 134e3)),
    ("CHA-XR1", "DR detector retrofit - wireless flat panel", day(2023, 5, 11), (127e3, 134e3)),
    ("MAI-CT", "Dose management and iterative recon software (ASiR-V)", day(2022, 7, 14), (181e3, 189e3)),
    ("CHA-MG", "Tomosynthesis upgrade - 50 degree wide angle", day(2022, 10, 4), (154e3, 163e3)),
    ("CES-CT", "Detector upgrade - 64-row to 128-slice reconstruction", day(2022, 11, 23), (441e3, 458e3)),
    ("CHA-MRI3", "Coil package - 60ch head/neck, ultra-flex coils", day(2022, 11, 8), (402e3, 418e3)),
    ("CHA-MRI3", "Deep Resolve AI reconstruction licence and hardware", day(2023, 8, 17), (311e3, 329e3)),
    ("RAY-CT", "Software upgrade - AIDR 3D Enhanced and SURE Exposure", day(2022, 11, 29), (209e3, 219e3)),
    ("RAY-CT", "Spectral and cardiac imaging package", day(2023, 11, 14), (441e3, 458e3)),
    ("RAY-XR", "Long-length imaging (stitching) upgrade", day(2023, 9, 26), (102e3, 109e3)),
    ("CES-XR", "Wireless detector and auto-stitch upgrade", day(2022, 8, 18), (126e3, 134e3)),
    ("CHA-XR2", "Second wireless detector and table upgrade", day(2022, 9, 6), (127e3, 134e3)),
]


class World:
    def __init__(self, tweak=None):
        self.rng = random.Random(SEED)
        self.assets = []
        self.approvals = []
        self._no = 1000
        self._tag = 1500
        self.build_register()
        # cents-level adjustments on minor assets, found by build.py so every graded figure sits mid-bin
        for no, cents in (tweak or {}).items():
            for x in self.assets:
                if x["id"] == no or x.get("duplicate_of") == no:
                    x["cost"] += D(cents) / 100

    # ----------------------------------------------------------------- ids
    def next_no(self, step=None):
        self._no += step if step else self.rng.choice([1, 1, 1, 1, 2])
        return str(self._no)

    def next_tag(self):
        self._tag += self.rng.choice([1, 1, 1, 2, 3])
        return "H%05d" % self._tag

    def serial(self, prefix):
        return "%s%06d" % (prefix, self.rng.randint(10000, 999999))

    def add(self, **k):
        k.setdefault("kind", "main")
        k.setdefault("host", None)
        k.setdefault("disposed", None)
        k.setdefault("impair", None)
        k.setdefault("capitalised", "Y")
        k.setdefault("approval", "")
        k.setdefault("notes", "")
        k.setdefault("tag", "")
        k.setdefault("serial", "")
        k.setdefault("supplier", "")
        k.setdefault("invoice", "")
        k.setdefault("status", "In use")
        self.assets.append(k)
        return k

    def invoice(self, supplier, d):
        pre = "".join(w[0] for w in supplier.split()[:2]).upper()
        return "%s%d" % (pre, self.rng.randint(100000, 999999)) if self.rng.random() < 0.8 else "INV-%05d" % self.rng.randint(1000, 99999)

    # ----------------------------------------------------------------- the register
    def build_register(self):
        rng = self.rng
        # older assets entered first, roughly in acquisition order, the way the workbook grew
        rows = []

        self.hosts = {}
        for key, site, desc, d, cr, sup, sp in HOSTS:
            rows.append(dict(key=key, site=site, description=desc, category="Medical imaging equipment",
                             acquired=d, cost=money(rng, *cr), supplier=sup, sp=sp))
        for host, desc, d, cr in UPGRADES:
            rows.append(dict(key=None, host_key=host, description=desc, category="Equipment upgrades",
                             acquired=d, cost=money(rng, *cr), kind="upgrade"))

        # other imaging equipment, some fully depreciated and still in use
        other_img = [("CHA", "Mobile X-ray unit - Mobilett Mira", day(2012, 8, 21), (104e3, 112e3), "Siemens Healthcare Pty Ltd", "MM"),
                     ("MAI", "OPG - Orthophos XG", day(2013, 5, 2), (86e3, 93e3), "Dentsply Sirona", "OX"),
                     ("CES", "OPG / CBCT - Planmeca ProMax 3D", day(2019, 6, 4), (108e3, 117e3), "Henry Schein Halas", "PM"),
                     ("RAY", "Bone densitometer - Horizon DXA", day(2020, 9, 15), (118e3, 126e3), "Hologic (Australia & New Zealand)", "HZ"),
                     ("CHA", "CT contrast injector - Stellant", day(2017, 2, 3), (42e3, 46e3), "Bayer Australia", "ST"),
                     ("MAI", "CT contrast injector - Stellant", day(2017, 3, 21), (42e3, 46e3), "Bayer Australia", "ST"),
                     ("CHA", "MR contrast injector - Spectris Solaris", day(2019, 5, 2), (58e3, 63e3), "Bayer Australia", "SS"),
                     ("CES", "CT contrast injector - Stellant FLEX", day(2018, 12, 12), (44e3, 48e3), "Bayer Australia", "ST"),
                     ("RAY", "CT contrast injector - Stellant FLEX", day(2021, 6, 9), (45e3, 49e3), "Bayer Australia", "ST"),
                     ("CHA", "MR patient monitor - Expression", day(2019, 4, 30), (38e3, 42e3), "Philips Electronics Australia", "EX"),
                     ("MAI", "Mobile X-ray unit - Mobilett Elara Max", day(2024, 2, 13), (138e3, 146e3), "Siemens Healthcare Pty Ltd", "ME"),
                     ("CHA", "Ceiling-mounted lead shield and lights", day(2016, 11, 28), (18e3, 21e3), "Rayshield Australia", "RS")]
        for site, desc, d, cr, sup, sp in other_img:
            rows.append(dict(site=site, description=desc, category="Medical imaging equipment", acquired=d,
                             cost=money(rng, *cr), supplier=sup, sp=sp))

        # stand-alone options and accessories: on the rate card's five years, nothing fitted to a system
        opts = [("CHA", "Ultrasound transducer - eL18-4 linear", day(2021, 4, 8), (12e3, 15e3)),
                ("CHA", "Ultrasound transducer - C5-1 curved", day(2021, 4, 8), (11e3, 14e3)),
                ("MAI", "Ultrasound transducer - 3D volume RM6C", day(2022, 2, 15), (16e3, 19e3)),
                ("CES", "Ultrasound transducer - eL18-4 linear", day(2023, 6, 6), (12e3, 15e3)),
                ("RAY", "Ultrasound transducer - L12-3 linear", day(2024, 3, 19), (10e3, 13e3)),
                ("CHA", "3D post-processing licence (5 concurrent)", day(2021, 11, 30), (52e3, 58e3)),
                ("MAI", "3D post-processing licence (2 concurrent)", day(2024, 8, 27), (24e3, 28e3)),
                ("CHA", "Breast biopsy attachment - stereotactic", day(2024, 5, 21), (34e3, 38e3)),
                ("CHA", "Radiation dose monitoring software (practice licence)", day(2025, 2, 11), (41e3, 45e3)),
                ("CES", "Ultrasound transducer - C5-1 curved", day(2025, 10, 7), (11e3, 14e3))]
        for site, desc, d, cr in opts:
            rows.append(dict(site=site, description=desc, category="Options & accessories", acquired=d,
                             cost=money(rng, *cr), kind="option"))

        # ultrasound systems
        us_sites = ["CHA"] * 5 + ["MAI"] * 4 + ["CES"] * 3 + ["RAY"] * 3
        us_models = [("LOGIQ E10", "GE Healthcare Australia", "LE"), ("EPIQ Elite", "Philips Electronics Australia", "EQ"),
                     ("Aplio i800", "Canon Medical Systems ANZ", "AI"), ("ACUSON Sequoia", "Siemens Healthcare Pty Ltd", "AS"),
                     ("Voluson E10", "GE Healthcare Australia", "VE")]
        for i, s in enumerate(us_sites):
            d = rdate(rng, day(2015, 3, 1), day(2026, 7, 31)) if i % 4 else rdate(rng, day(2014, 6, 1), day(2018, 6, 30))
            mdl, sup, sp = us_models[rng.randrange(len(us_models))]
            rows.append(dict(site=s, description="Ultrasound system - %s" % mdl, category="Ultrasound", acquired=d,
                             cost=money(rng, 92e3, 214e3), supplier=sup, sp=sp))

        # computer equipment
        comp = []
        for i in range(84):
            s = rng.choice(["CHA"] * 4 + ["MAI"] * 3 + ["CES"] * 2 + ["RAY"] * 2)
            kind = rng.random()
            if kind < 0.55:
                desc, cr = "Workstation - HP Z2 Tower", (2.1e3, 3.4e3)
            elif kind < 0.75:
                desc, cr = "Diagnostic reporting monitor pair - Barco Nio", (9.8e3, 13.6e3)
            elif kind < 0.9:
                desc, cr = "Laptop - HP EliteBook 840", (1.7e3, 2.6e3)
            else:
                desc, cr = "Network switch - Cisco Catalyst 9200", (4.2e3, 6.8e3)
            comp.append(dict(site=s, description=desc, category="Computer equipment",
                             acquired=rdate(rng, day(2018, 7, 1), day(2026, 8, 31)), cost=money(rng, *cr),
                             supplier=rng.choice(["Data#3 Limited", "Brennan IT", "Broadmeadow IT Services"]), sp="CZ"))
        for d, desc, cr in [(day(2019, 8, 14), "PACS server cluster - primary", (148e3, 159e3)),
                            (day(2022, 3, 9), "PACS archive expansion - 200TB", (86e3, 94e3)),
                            (day(2024, 6, 27), "RIS/PACS application server", (61e3, 67e3)),
                            (day(2025, 11, 18), "Backup appliance - Rubrik r6408", (52e3, 57e3))]:
            comp.append(dict(site="CHA", description=desc, category="Computer equipment", acquired=d,
                             cost=money(rng, *cr), supplier="Broadmeadow IT Services", sp="SV"))
        rows += comp

        # leasehold improvements (the reclassified joinery sits under furniture on the register)
        for site, desc, d, cr in [("CHA", "Fit-out Charlestown - level 1 and 2", day(2015, 9, 30), (2.31e6, 2.42e6)),
                                  ("MAI", "Fit-out Maitland", day(2016, 2, 26), (1.52e6, 1.61e6)),
                                  ("MAI", "MRI suite RF shielding and quench pipe - Maitland", day(2016, 9, 23), (0.61e6, 0.66e6)),
                                  ("CES", "Fit-out Cessnock", day(2017, 5, 18), (0.86e6, 0.93e6)),
                                  ("CHA", "MRI suite 2 shielding and plant - Charlestown", day(2019, 2, 28), (0.87e6, 0.94e6)),
                                  ("RAY", "Fit-out Raymond Terrace", day(2020, 6, 30), (1.06e6, 1.13e6)),
                                  ("RAY", "CT room lead lining and services", day(2021, 4, 29), (0.21e6, 0.24e6)),
                                  ("CHA", "Waiting room refurbishment", day(2024, 9, 12), (0.14e6, 0.16e6))]:
            rows.append(dict(site=site, description=desc, category="Leasehold improvements", acquired=d,
                             cost=money(rng, *cr), supplier=rng.choice(["Kanellos Constructions", "Glendale Fitout Co", "Medifit Interiors"]), sp="LI"))

        # furniture and fittings
        for i in range(66):
            s = rng.choice(["CHA"] * 4 + ["MAI"] * 3 + ["CES"] * 2 + ["RAY"] * 2)
            desc, cr = rng.choice([("Reception chairs (set)", (1.6e3, 4.2e3)), ("Radiologist reporting desk", (2.2e3, 3.9e3)),
                                   ("Patient change cubicle joinery", (3.1e3, 6.8e3)), ("Ultrasound bed - electric", (4.6e3, 8.9e3)),
                                   ("Staff room fit-out furniture", (2.4e3, 5.5e3)), ("Filing compactus", (5.2e3, 9.6e3))])
            rows.append(dict(site=s, description=desc, category="Furniture & fittings",
                             acquired=rdate(rng, day(2014, 7, 1), day(2026, 8, 31)), cost=money(rng, *cr),
                             supplier=rng.choice(["Officeworks Business", "Krost Business Furniture", "Medifit Interiors"]), sp="FF"))
        self.joinery_row = dict(site="CHA", description="Reception counter and joinery - Charlestown", category="Furniture & fittings",
                                acquired=day(2021, 3, 24), cost=D("47862.40"), supplier="Medifit Interiors", sp="FF")
        rows.append(self.joinery_row)

        # motor vehicles
        rows.append(dict(site="CHA", description="Toyota HiAce van (courier)", category="Motor vehicles", acquired=day(2021, 8, 19),
                         cost=D("48119.09"), supplier="Newcastle Toyota", sp="MV"))
        rows.append(dict(site="MAI", description="Toyota RAV4 Hybrid", category="Motor vehicles", acquired=day(2023, 4, 3),
                         cost=D("44270.91"), supplier="Maitland Toyota", sp="MV"))

        # order of entry: the workbook was kept roughly in acquisition order with the odd late entry
        rows.sort(key=lambda r: (r["acquired"], rng.random()))
        key_to_no = {}
        for r in rows:
            no = self.next_no()
            kind = r.get("kind", "main")
            a = self.add(id=no, description=r["description"], category=r["category"], site=r["site"] if "site" in r else None,
                         acquired=r["acquired"], cost=r["cost"], kind=kind, supplier=r.get("supplier", ""))
            if r.get("key"):
                key_to_no[r["key"]] = no
                self.hosts[r["key"]] = a
            if kind == "upgrade":
                a["host_key"] = r["host_key"]
            if kind not in ("upgrade",) and r["category"] != "Leasehold improvements":
                a["tag"] = self.next_tag()
            sp = r.get("sp")
            if sp and r["category"] in ("Medical imaging equipment", "Ultrasound", "Computer equipment"):
                a["serial"] = self.serial(sp)
            if r is self.joinery_row:
                self.joinery = a
        for a in self.assets:
            if a["kind"] == "upgrade":
                host = self.hosts[a["host_key"]]
                a["host"] = host["id"]
                a["site"] = host["site"]
                a["supplier"] = host["supplier"]
            if a["kind"] == "option":
                a["supplier"] = {"Ultrasound": "GE Healthcare Australia"}.get(a["category"], self.rng.choice(
                    ["GE Healthcare Australia", "Philips Electronics Australia", "Siemens Healthcare Pty Ltd"]))
            a["invoice"] = self.invoice(a["supplier"] or "Misc Supplier", a["acquired"])

        # the impairment written in June 2025 on the Cessnock OPG (tube failure)
        for a in self.assets:
            if a["description"].startswith("OPG / CBCT"):
                a["impair"] = (L.mi(2025, 6), D("38000.00"))
                self.opg = a

        # the Voluson that came across from Bremer on 12 February 2026 (Bremer: in service 20/09/2021,
        # depreciated from October 2021 over 72 months, none in the month it left)
        cost = D("186040.00")
        mon = L.r2(cost / 72)
        bf = mon * 52
        src_end = L.mi(2021, 10) + 72 - 1
        self.transfer = self.add(id=self.next_no(step=1), description="Ultrasound system - Voluson E10 (ex Bremer)",
                                 category="Ultrasound", site="MAI", acquired=day(2026, 2, 12), cost=cost,
                                 kind="transfer_in", supplier="Bremer Radiology (intercompany)",
                                 transfer=dict(bf_accum=bf, source_end=src_end, source_no="BRM-21455",
                                               source_in_service=day(2021, 9, 20), source_life=72),
                                 notes="Transferred from Bremer 12/02/26 (BRM-21455). Accum dep b/f per IC journal")
        self.transfer["tag"] = self.next_tag()
        self.transfer["serial"] = "VE%06d" % 418226
        self.transfer["invoice"] = "IC-BRM-0212"

        self.disposals()
        self.capitalisation_noise()
        self.net_upgrades()

    # ----------------------------------------------------------------- the upgrade invoices, netted
    def net_upgrades(self):
        """Set the upgrade invoices so that a five-year life and the host's remaining months post the same
        imaging total in every month from December 2023 to September 2026 and carry the same imaging balance
        at 30 June 2025, to the cent. No upgrade starts after November 2023 and none ends before October
        2026 on either reading, so the two readings agree on every replay month and every balance date the
        pack carries; they part only in the months before the last upgrade started, which is where the FY2024
        comparative in note 9 sits. The moves are the smallest relative ones that close both sums, then a cent
        or two."""
        from fractions import Fraction as Fr
        ups = [a for a in self.assets if a["kind"] == "upgrade"]
        eng = L.Engine(self.ledger_assets())
        life = {a["id"]: eng.host_end(a) - L.mdate(a["acquired"]) + 1 for a in ups}
        n25 = {a["id"]: L.JUN25 - L.mdate(a["acquired"]) + 1 for a in ups}

        def d(a, c=None):
            c = a["cost"] if c is None else c
            return L.r2(c / 60) - L.r2(c / life[a["id"]])

        def sums():
            return (sum((d(a) for a in ups), D(0)), sum((n25[a["id"]] * d(a) for a in ups), D(0)))

        s1, s2 = sums()
        tuners = [a for a in ups if a["acquired"] < day(2023, 7, 1) and abs(Fr(1, 60) - Fr(1, life[a["id"]])) > Fr(1, 500)]
        k = {a["id"]: Fr(1, 60) - Fr(1, life[a["id"]]) for a in tuners}
        wt = {a["id"]: Fr(a["cost"]) ** 2 for a in tuners}
        a11 = sum(wt[i] * k[i] ** 2 for i in k)
        a12 = sum(wt[i] * k[i] ** 2 * n25[i] for i in k)
        a22 = sum(wt[i] * k[i] ** 2 * n25[i] ** 2 for i in k)
        b1, b2 = -Fr(s1), -Fr(s2)
        det = a11 * a22 - a12 * a12
        l1, l2 = (b1 * a22 - b2 * a12) / det, (a11 * b2 - a12 * b1) / det
        for a in tuners:
            i = a["id"]
            dc = wt[i] * k[i] * (l1 + l2 * n25[i])
            a["cost"] = (a["cost"] + D(dc.numerator) / D(dc.denominator)).quantize(D("0.01"))
        # the last cents: nudge one or two upgrades' monthly difference by a cent or a few
        r1, r2 = (int(x * 100) for x in sums())
        if (r1, r2) != (0, 0):
            order = sorted(ups, key=lambda a: (a["acquired"] >= day(2023, 7, 1), int(a["id"])))
            plan = None
            for a in order:
                for e in (1, -1, 2, -2, 3, -3):
                    if e == -r1 and n25[a["id"]] * e == -r2:
                        plan = [(a, e)]
                        break
                if plan:
                    break
            if plan is None:
                for x in order:
                    for y in order:
                        if plan or x is y:
                            continue
                        for ex in (1, -1, 2, -2, 3, -3):
                            ey = -r1 - ex
                            if abs(ey) <= 3 and n25[x["id"]] * ex + n25[y["id"]] * ey == -r2:
                                plan = [(x, ex), (y, ey)]
                                break
                    if plan:
                        break
            for a, e in plan:
                base, want = a["cost"], d(a) + D(e) / 100
                for j in range(1, 20001):
                    hit = next((c for c in (base + D(j) / 100, base - D(j) / 100) if d(a, c) == want), None)
                    if hit is not None:
                        a["cost"] = hit
                        break
        self.netting = dict(sums=sums(), moved={a["id"]: a["cost"] for a in tuners})
        assert sums() == (0, 0), sums()

    # ----------------------------------------------------------------- disposals
    def disposals(self):
        rng = self.rng
        pool = [a for a in self.assets if a["category"] in ("Computer equipment", "Furniture & fittings", "Ultrasound")
                and a["acquired"] < day(2021, 1, 1) and a["kind"] == "main"]
        self.disposed_before = []
        self.disposed_window = []
        for a in rng.sample(pool, 22):
            if rng.random() < 0.45:
                a["disposed"] = rdate(rng, day(2023, 7, 1), day(2025, 6, 30))
                self.disposed_before.append(a)
            else:
                a["disposed"] = rdate(rng, day(2025, 7, 1), day(2026, 9, 25))
                self.disposed_window.append(a)
            a["status"] = "Disposed"
        for a in self.disposed_window + self.disposed_before:
            a["proceeds"] = D(0) if (a["category"] != "Ultrasound" or rng.random() < 0.3) else money(rng, 4e3, 11e3)

    # ----------------------------------------------------------------- what the register carries that the ledger does not
    def capitalisation_noise(self):
        rng = self.rng
        # tracked items below the threshold, carried on the workbook for the insurer, never capitalised
        self.expensed = []
        for i in range(57):
            s = rng.choice(list(SITES))
            desc, lo, hi = rng.choice([("Lead apron - full wrap", 280, 690), ("Office chair", 240, 610),
                                       ("Desk phone - Yealink T54W", 190, 290), ("Label printer", 160, 420),
                                       ("Patient wheelchair", 420, 980), ("Monitor 27in", 290, 540),
                                       ("Thyroid collar set", 180, 360), ("Step stool - two step", 140, 260),
                                       ("Barcode scanner", 230, 480), ("Blanket warmer", 1100, 1460)])
            a = self.add(id=self.next_no(), description=desc, category=rng.choice(
                ["Furniture & fittings", "Computer equipment", "Medical imaging equipment"]) if "apron" not in desc else "Medical imaging equipment",
                site=s, acquired=rdate(rng, day(2017, 1, 1), day(2026, 8, 31)), cost=money(rng, lo, hi),
                kind="expensed", capitalised="N", supplier=rng.choice(["Officeworks Business", "Medshop Australia", "JB Hi-Fi Business"]))
            a["tag"] = self.next_tag()
            a["invoice"] = self.invoice(a["supplier"], a["acquired"])
            self.expensed.append(a)
        # invoice lines keyed twice when the bookkeeper re-entered a batch
        cands = [a for a in self.assets if a["category"] in ("Computer equipment", "Furniture & fittings")
                 and a["kind"] == "main" and not a["disposed"]]
        self.duplicates = []
        for a in rng.sample(cands, 6):
            b = self.add(id=self.next_no(), description=a["description"], category=a["category"], site=a["site"],
                         acquired=a["acquired"], cost=a["cost"], kind="duplicate", supplier=a["supplier"],
                         invoice=a["invoice"], serial=a["serial"], tag="", duplicate_of=a["id"])
            self.duplicates.append(b)

    # ----------------------------------------------------------------- views
    def ledger_assets(self):
        """What the legacy ledger actually carries: capitalised, not a repeated line."""
        return [a for a in self.assets if a["kind"] not in ("expensed", "duplicate")]


# ------------------------------------------------------------------------------- capital approvals
APPROVAL_TYPES = {"upgrade": "Upgrade", "option": "New equipment"}


def build_approvals(w):
    """Yacaaba's capital requests (its own log to February 2024, the group's capex system after),
    as the migration team combined them. An upgrade names the system it is fitted to in its request
    text only; Existing Asset is filled for replacements, which retire an asset."""
    rng = w.rng
    rows = []
    n_old, n_new = [100], [2400]
    by_id = {a["id"]: a for a in w.assets}

    def ref(d):
        if d < day(2024, 3, 1):
            n_old[0] += rng.choice([1, 1, 2])
            return "CR-%d-%03d" % (d.year, n_old[0] % 1000)
        n_new[0] += rng.choice([1, 2, 3, 5])
        return "QIG-CX-%04d" % n_new[0]

    def approve_date(acq):
        return acq - dt.timedelta(days=rng.randint(35, 160))

    eligible = [a for a in w.assets if a["kind"] in ("main", "upgrade", "option", "transfer_in")
                and a["acquired"] >= day(2018, 1, 1)
                and (a["category"] in ("Medical imaging equipment", "Equipment upgrades", "Options & accessories", "Ultrasound", "Leasehold improvements",
                                       "Motor vehicles") or a["cost"] >= 40000)]
    # ultrasound replacements name the unit they replaced
    old_us = [a for a in w.assets if a["category"] == "Ultrasound" and a["kind"] == "main" and a["disposed"]]
    for a in sorted(eligible, key=lambda x: x["acquired"]):
        if a["kind"] == "transfer_in":
            continue
        d = approve_date(a["acquired"])
        typ, existing = "New equipment", ""
        if a["kind"] == "upgrade":
            typ = "Upgrade"            # the system is named in the request text; the capex log keys only retirements
        elif a["kind"] == "option":
            typ = "Software" if "licence" in a["description"] or "software" in a["description"].lower() else "New equipment"
        elif a["category"] == "Ultrasound" and old_us and rng.random() < 0.5:
            old = old_us.pop(0)
            if old["disposed"] and old["disposed"] >= a["acquired"] - dt.timedelta(days=120):
                typ, existing = "Replacement", old["id"]
        elif a["category"] == "Leasehold improvements":
            typ = "Fit-out"
        elif a["category"] == "Computer equipment":
            typ = "IT"
        elif a["category"] == "Motor vehicles":
            typ = "Vehicle"
        amt = (a["cost"] * D(rng.uniform(0.985, 1.06))).quantize(D("1"))
        r = dict(ref=ref(d), approved=d, site=a["site"], type=typ, description=_request_text(a, by_id),
                 existing=existing, amount=amt, supplier=a["supplier"], status="Completed",
                 completed=a["acquired"], asset=a["id"])
        a["approval"] = r["ref"]
        rows.append(r)
    # requests that never became an asset, and the open ones
    extra = [(day(2021, 5, 4), "MAI", "Replacement", "Replace mammography unit with DBT-capable system", "", 498000, "Declined"),
             (day(2022, 2, 22), "CES", "New equipment", "Second ultrasound room fit and system", "", 214000, "Withdrawn"),
             (day(2023, 10, 30), "CHA", "Upgrade", "MRI 3T cardiac package", "", 286000, "Deferred"),
             (day(2025, 4, 9), "RAY", "Fit-out", "Second X-ray room shielding", "", 148000, "Declined"),
             (day(2026, 8, 11), "MAI", "Replacement", "Replace MRI 1.5T with 1.5T wide-bore system (delivery April 2027)",
              w.hosts["MAI-MRI"]["id"], 2385000, "Approved - PO raised"),
             (day(2026, 9, 1), "CHA", "Replacement", "Replace CT 128 (delivery May 2027)", w.hosts["CHA-CT"]["id"], 1290000,
              "Approved - awaiting quote")]
    for d, site, typ, txt, existing, amt, status in extra:
        rows.append(dict(ref=ref(d), approved=d, site=site, type=typ, description=txt, existing=existing,
                         amount=D(amt), supplier="", status=status, completed=None, asset=""))
    rows.sort(key=lambda r: (r["approved"], r["ref"]))
    return rows


def _scan_export_devices(w, eng, tagged, outcome, moves, scans, nil_sep, has_h2):
    """Two devices in the handheld export, drawn on their own stream so no outcome above changes.
    A label on the wrong unit: the Voluson that moved from Maitland to Charlestown is scanned once, wearing the
    tag of a Charlestown ultrasound with its own rating plate keyed beside it; the Charlestown unit, its label
    gone, is sighted on its plate. HH-07's clock: its battery went flat on Wednesday night and it ran on its
    factory clock through Thursday, so Thursday's Cessnock scans read 1 January 2025; one asset sighted only
    then is at nil and loads, one moved in from Charlestown is sighted only then. Trial scans on Friday
    25 September at Maitland, before the window, include an asset at nil that is never sighted in it."""
    drng = random.Random(SEED + 211)
    byid = {a["id"]: a for a in w.assets}
    local = lambda t: t + dt.timedelta(hours=11) if t >= dt.datetime(2026, 10, 3, 16) else t + dt.timedelta(hours=10)

    def at(day_, h0=9, h1=15):
        return utc_from_local(dt.datetime.combine(day_, dt.time(drng.randint(h0, h1), drng.randint(0, 59), drng.randint(0, 59))))
    dev = {}
    # 1. the label on the wrong unit
    twin = lambda b: sorted((a for a in tagged if a["site"] == "CHA" and outcome[a["id"]] == ("found", "CHA") and a["serial"]
                             and a["description"] == b["description"] and a["kind"] == "main"), key=lambda a: int(a["id"]))
    b = max((a for a, frm, to in moves if to == "CHA" and a["serial"] and has_h2[a["id"]] and twin(a)), key=lambda a: eng.h2(a))
    a_ = twin(b)[0]
    scans = [s for s in scans if s[0] is not b]
    scans = [(s[0], s[1], s[2], "", a_["serial"]) if s[0] is a_ else s for s in scans]
    swap_day = dt.date(2026, 10, 6)
    scans.append((b, "CHA", at(swap_day), a_["tag"], b["serial"]))
    scans.append((a_, "CHA", at(swap_day), "", a_["serial"]))
    dev["label_on"], dev["label_off"] = b, a_
    # 2. HH-07's clock on Thursday 8 October
    thu = dt.date(2026, 10, 8)
    m = max((a for a, frm, to in moves if to == "CES" and frm != "MAI" and has_h2[a["id"]]), key=lambda a: eng.nbv(a, L.SEP26))
    n = min((a for a in tagged if a["site"] == "CES" and outcome[a["id"]] == ("found", "CES") and nil_sep[a["id"]]
             and a["kind"] == "main"), key=lambda a: int(a["id"]))
    for x in (m, n):
        k = len([s for s in scans if s[0] is x]) or 1
        scans = [s for s in scans if s[0] is not x] + [(x, "CES", at(thu), x["tag"], "") for _ in range(k)]
    # a witness: something Cessnock bought after the factory date is scanned that Thursday too
    wit = min((a for a in tagged if a["site"] == "CES" and outcome[a["id"]] == ("found", "CES")
               and a["acquired"] >= dt.date(2025, 3, 1)), key=lambda a: a["acquired"])
    scans.append((wit, "CES", at(thu), wit["tag"], ""))
    scans.append((wit, "CES", utc_from_local(dt.datetime(2026, 10, 9, 7, 46, 52)), wit["tag"], ""))   # Friday's first read
    power_on = utc_from_local(dt.datetime(2026, 10, 8, 7, 52, 17))
    clock = {}
    for s in scans:
        if s[1] == "CES" and local(s[2]).date() == thu:
            clock[(s[0]["id"] if s[0] else None, s[2])] = CLOCK_RESET_UTC + (s[2] - power_on)
    dev["clock_only"], dev["clock_nil"], dev["clock_witness"] = m, n, wit
    # 3. trial scans before the window, at Maitland
    trial = dt.date(2026, 9, 25)
    t_ = min((a for a in tagged if a["site"] == "MAI" and outcome[a["id"]] == ("missing", "MAI") and nil_sep[a["id"]]
              and a["kind"] == "main"), key=lambda a: int(a["id"]))
    scans.append((t_, "MAI", at(trial, 10, 14), t_["tag"], ""))
    others = [a for a in tagged if a["site"] == "MAI" and outcome[a["id"]] == ("found", "MAI")]
    for a in sorted(others, key=lambda a: int(a["id"]))[:: max(1, len(others) // 7)][:7]:
        scans.append((a, "MAI", at(trial, 10, 14), a["tag"], ""))
    dev["trial_only"] = t_
    return scans, clock, dev


def _request_text(a, by_id):
    d = a["description"]
    if a["kind"] == "upgrade":
        host = by_id[a["host"]]
        return "%s for %s, %s" % (d, host["description"].split(" - ")[0], SITES[host["site"]])
    return d


# ------------------------------------------------------------------------------- verification
WINDOW_START_LOCAL = dt.datetime(2026, 9, 28, 0, 0)
CLOCK_RESET_UTC = dt.datetime(2025, 1, 1, 0, 0, 0)       # HH-07's factory clock after its battery went flat


def utc_from_local(t):
    """NSW local wall time to UTC: AEST (+10) to 2:00 am on 4 October 2026, AEDT (+11) after."""
    if t >= dt.datetime(2026, 10, 4, 3, 0):
        return t - dt.timedelta(hours=11)
    return t - dt.timedelta(hours=10)


def build_verification(w, eng):
    """Scans for Charlestown, Maitland and Cessnock; Raymond Terrace on a paper count sheet.
    Every outcome is decided here, with the truth it implies."""
    rng = w.rng
    tagged = [a for a in w.assets if a["tag"] and a["status"] != "Disposed"]
    nil = {a["id"]: (a["kind"] != "expensed" and eng.nbv(a, L.DEC26) == 0) for a in tagged}
    # write-off candidates are already at nil on 30 September, so the site walk has one reading
    nil_sep = {a["id"]: (a["kind"] != "expensed" and eng.nbv(a, L.SEP26) == 0) for a in tagged}
    has_h2 = {a["id"]: (a["kind"] != "expensed" and eng.h2(a) > 0) for a in tagged}
    outcome = {}

    # relocations (site of record moves), chosen so every site gains or loses a charge-bearing asset
    moves = []
    def pick(site, pred, k):
        c = [a for a in tagged if a["site"] == site and pred(a) and a["id"] not in outcome]
        rng.shuffle(c)
        return c[:k]
    plan = [("CHA", "RAY", lambda a: a["category"] == "Ultrasound" and has_h2[a["id"]], 1),
            ("MAI", "CES", lambda a: a is w.transfer, 1),
            ("CES", "CHA", lambda a: a["category"] == "Computer equipment" and has_h2[a["id"]], 2),
            ("RAY", "MAI", lambda a: a["category"] == "Computer equipment" and has_h2[a["id"]], 1),
            ("CHA", "MAI", lambda a: a["category"] == "Medical imaging equipment" and has_h2[a["id"]] and a["cost"] < 70000, 1),
            ("MAI", "CHA", lambda a: a["category"] == "Ultrasound" and has_h2[a["id"]], 1),
            ("CHA", "CES", lambda a: a["category"] == "Furniture & fittings" and has_h2[a["id"]], 2),
            ("MAI", "RAY", lambda a: a["category"] == "Furniture & fittings", 1),
            ("CES", "MAI", lambda a: a["category"] == "Ultrasound" and nil[a["id"]], 1),
            ("CHA", "MAI", lambda a: a["category"] == "Computer equipment" and nil[a["id"]], 2)]
    for frm, to, pred, k in plan:
        for a in pick(frm, pred, k):
            outcome[a["id"]] = ("moved", to)
            moves.append((a, frm, to))
    # late-only scans (after 5:00 pm on Friday 9 October): nil assets, and two would-be moves
    late = []
    for site, k in (("CHA", 2), ("MAI", 2), ("CES", 1)):
        for a in pick(site, lambda a: nil_sep[a["id"]] and a["kind"] == "main", k):
            outcome[a["id"]] = ("late", site)
            late.append(a)
    for frm, to, cat in (("CES", "MAI", "Ultrasound"), ("MAI", "CHA", "Computer equipment")):
        for a in pick(frm, lambda a: a["category"] == cat and has_h2[a["id"]] and a["kind"] == "main", 1):
            outcome[a["id"]] = ("late", to)
            late.append(a)
    # serial-only scans (tag label damaged), mostly old equipment
    for site, k in (("CHA", 3), ("MAI", 3), ("CES", 2)):
        for a in pick(site, lambda a: nil_sep[a["id"]] and a["serial"] and a["kind"] == "main", k):
            outcome[a["id"]] = ("serial", site)
    # genuinely not found
    for site, k_nil, k_bv in (("CHA", 3, 1), ("MAI", 2, 1), ("CES", 2, 0), ("RAY", 2, 1)):
        for a in pick(site, lambda a: (nil_sep[a["id"]] or a["kind"] == "expensed") and a["kind"] in ("main", "expensed"), k_nil):
            outcome[a["id"]] = ("missing", site)
        for a in pick(site, lambda a: (not nil[a["id"]]) and a["kind"] == "main" and a["cost"] < 15000, k_bv):
            outcome[a["id"]] = ("missing", site)
    for a in tagged:
        outcome.setdefault(a["id"], ("found", a["site"]))
    # RAY counted on paper on 7 October; everything else scanned
    scans, sheet = [], []
    devices = {"CHA": ["HH-02", "HH-03"], "MAI": ["HH-05"], "CES": ["HH-07"]}
    users = {"CHA": ["kmorgan", "jtan", "pnguyen"], "MAI": ["dramirez", "sali"], "CES": ["bcole", "rsingh"],
             "RAY": ["kwhite"]}
    def stamp(local_day):
        h = rng.choice([8, 9, 10, 11, 12, 13, 14, 15, 16])
        return dt.datetime.combine(local_day, dt.time(h, rng.randint(0, 59), rng.randint(0, 59)))
    count_days = [day(2026, 9, 28) + dt.timedelta(days=k) for k in range(12)]
    count_days = [d for d in count_days if d.weekday() < 5]
    for a in tagged:
        kind, where = outcome[a["id"]]
        if where == "RAY" or (a["site"] == "RAY" and kind in ("found", "missing")):
            if kind != "missing":
                sheet.append((a, where))
            continue
        if kind == "missing":
            continue
        n = rng.choice([1, 1, 1, 2, 2, 3])
        if kind == "late":
            for j in range(rng.choice([1, 1, 2])):
                t = dt.datetime(2026, 10, 9, 17, rng.randint(6, 52), rng.randint(0, 59))
                scans.append((a, where, utc_from_local(t), a["tag"], ""))
            continue
        for j in range(n):
            t = stamp(rng.choice(count_days))
            if kind == "serial":
                scans.append((a, where, utc_from_local(t), "", a["serial"]))
            else:
                scans.append((a, where, utc_from_local(t), a["tag"], a["serial"] if rng.random() < 0.18 else ""))
    # a few valid Friday-afternoon scans either side of the old clock, so the hour is not empty
    friday = [s for s in scans if s[2].date() == dt.date(2026, 10, 9)]
    # stray reads: tags that belong to nothing on this register (group loan stock)
    for k in range(9):
        t = stamp(rng.choice(count_days))
        scans.append((None, rng.choice(["CHA", "MAI", "CES"]), utc_from_local(t), "Q%06d" % rng.randint(100000, 999999), ""))
    scans, clock, scan_dev = _scan_export_devices(w, eng, tagged, outcome, moves, scans, nil_sep, has_h2)
    scans.sort(key=lambda s: s[2])
    w.verification = dict(outcome=outcome, scans=scans, sheet=sheet, moves=moves, late=late, nil=nil,
                          devices=devices, users=users, clock=clock, scan_devices=scan_dev)
    return w.verification
