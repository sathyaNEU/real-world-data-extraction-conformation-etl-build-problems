"""The world before any file is written: Corriven's private-car and van book by month, every claim arising on it from
2019 to September 2026 with who notified it and when, the claimant representatives, and the policy book in force on 30
September 2026 with its mid-term changes. One random stream per component, so tuning one leaves the others alone."""
import datetime as dt

import numpy as np

import common as K

# earned car-years in 2025 by region, private car; vans are a share of it
CY2025 = {"Mersey": 61870.0, "Pennine": 40590.0, "Wessex": 38140.0, "Fenland": 23910.0, "Severn": 47230.0}
VAN_SHARE = {"Mersey": 0.12, "Pennine": 0.14, "Wessex": 0.10, "Fenland": 0.16, "Severn": 0.11}
COVER_MIX = {"Mersey": (0.74, 0.18, 0.08), "Pennine": (0.76, 0.17, 0.07), "Wessex": (0.81, 0.14, 0.05),
             "Fenland": (0.83, 0.13, 0.04), "Severn": (0.79, 0.15, 0.06)}
COVERS = ("COMP", "TPFT", "TPO")
GROWTH = 0.016
# per 100 earned car-years, private car: OD, TPPD, TPI, THEFT, FIRE, GLASS
FREQ = {"Mersey": (3.05, 2.55, 1.32, 0.88, 0.07, 1.02), "Pennine": (2.70, 2.20, 1.00, 0.52, 0.06, 0.93),
        "Wessex": (2.62, 2.12, 0.98, 0.45, 0.05, 0.96), "Fenland": (2.18, 1.70, 0.74, 0.30, 0.06, 0.82),
        "Severn": (3.02, 2.47, 1.06, 0.56, 0.06, 1.01)}
VAN_FREQ = (3.9, 3.4, 1.2, 1.1, 0.08, 1.3)
SEASON = np.array([1.12, 1.05, 0.98, 0.93, 0.95, 0.95, 0.97, 0.96, 0.98, 1.03, 1.06, 1.10])
COVID = {2020: np.array([1, 1, 0.82, 0.52, 0.60, 0.74, 0.86, 0.90, 0.92, 0.90, 0.80, 0.86]),
         2021: np.array([0.74, 0.78, 0.86, 0.92, 0.95, 0.97, 0.98, 0.98, 0.99, 1, 1, 1])}
# route mix of each head's notifications: PH, TPD, INS, SOL, CMC
MIX = {"OD": (1, 0, 0, 0, 0), "THEFT": (1, 0, 0, 0, 0), "FIRE": (1, 0, 0, 0, 0), "GLASS": (1, 0, 0, 0, 0),
       "TPPD": (0.62, 0.10, 0.28, 0, 0)}
TPI_MIX = {2019: (0.31, 0.03, 0.13, 0.28, 0.25), 2020: (0.31, 0.03, 0.13, 0.28, 0.25),
           2021: (0.30, 0.06, 0.12, 0.27, 0.25), 2022: (0.30, 0.08, 0.12, 0.25, 0.25),
           2023: (0.30, 0.08, 0.12, 0.25, 0.25), 2024: (0.30, 0.08, 0.12, 0.25, 0.25),
           2025: (0.30, 0.08, 0.12, 0.25, 0.25), 2026: (0.30, 0.08, 0.12, 0.25, 0.25)}
# claims-management waves: (region, accident year) -> extra CMC injury claimants per 100 car-years, and the firm
WAVES = {("Wessex", 2022): (0.78, "CMC_W"), ("Pennine", 2025): (0.55, "CMC_P"), ("Pennine", 2026): (0.58, "CMC_P")}
LAG = {"PH": ("phx", 3.0), "TPD": ("gamma", 1.6, 25.0), "INS": ("gamma", 2.0, 16.0),
       "SOL": ("lognormal", 190.0, 0.75), "CMC": ("lognormal", 600.0, 0.45)}
TWIN_RATE = {"OD": 0.07, "TPPD": 0.12, "TPI": 0.32, "THEFT": 0.09, "FIRE": 0.07, "GLASS": 0.04}
BLANK_TP = {"TPPD": 0.08, "TPI": 0.20}   # policyholder reports with the third party not yet identified
DEFAULT_P = {"w_CMC_W": 1.28, "w_CMC_P": 1.545, "sev_od": 0.93}   # the tuned waves and Severn's own-damage rate


def _days(y):
    return (dt.date(y + 1, 1, 1) - dt.date(y, 1, 1)).days


class World:
    def __init__(self, seed=K.SEED, P=None):
        self.P = dict(DEFAULT_P)
        self.P.update(P or {})
        self.ss = np.random.SeedSequence(seed)
        streams = self.ss.spawn(9)
        self.r_book, self.r_claims, self.r_lag, self.r_reps, self.r_amt, self.r_pol, self.r_chg, self.r_id, \
            self.r_twin = [np.random.default_rng(s) for s in streams]
        self.r_blank = np.random.default_rng(self.ss.spawn(1)[0])
        self.book()
        self.representatives()
        self.claims()
        self.policies()

    # ---------------------------------------------------------------- the book, by month
    def book(self):
        r = self.r_book
        rows = []
        for y in range(2019, 2026):
            for reg in K.REG:
                base = CY2025[reg] * (1 + GROWTH) ** (y - 2025)
                for prod in ("PC", "LCV"):
                    tot = base * (1 if prod == "PC" else VAN_SHARE[reg])
                    w = np.array([_days_in(y, m) for m in range(1, 13)], float) * (1 + r.normal(0, 0.004, 12))
                    w = w / w.sum()
                    mix = np.array(COVER_MIX[reg]) * (1 + r.normal(0, 0.01, 3))
                    mix = mix / mix.sum()
                    for m in range(12):
                        for ci, cov in enumerate(COVERS):
                            rows.append((y, m + 1, reg, prod, cov, round(tot * w[m] * mix[ci], 2)))
        # the mart's stored figures: the earned exposure as the pricing mart computed it from policy days, a hair off
        # the generation's own (each year, region and product on its own fixed draw, outside every stream)
        out = []
        for (y, m, reg, prod, cov, v) in rows:
            j = np.random.default_rng(y * 100 + K.REG.index(reg) * 10 + (prod == "LCV")).uniform(-0.0009, 0.0009)
            out.append((y, m, reg, prod, cov, round(v * (1 + j), 2)))
        self.exposure = out
        tgt = {}
        for y, m, reg, prod, cov, v in rows:
            tgt[(y, reg, prod)] = tgt.get((y, reg, prod), 0) + v
            tgt[(y, m, reg, prod)] = tgt.get((y, m, reg, prod), 0) + v
        self.cy = tgt
        # 2026 to September for the claims (the workbook stops at 2025)
        for reg in K.REG:
            for prod in ("PC", "LCV"):
                base = CY2025[reg] * (1 + GROWTH) * (1 if prod == "PC" else VAN_SHARE[reg])
                for m in range(1, 13):
                    self.cy[(2026, m, reg, prod)] = base * _days_in(2026, m) / 365

    # ---------------------------------------------------------------- claimant representatives
    def representatives(self):
        r = self.r_reps
        sol_names = ["Hartley Beck", "Ashworth Kemp", "Fairbrother Lyle", "Ormerod Shaw", "Pickersgill & Co",
                     "Tolland Rees", "Garside Whitworth", "Brennan Moult", "Coldwell Ince", "Ramsbottom Hale",
                     "Lindqvist Barr", "Prendergast Ellery", "Cheadle Royce", "Morland Tate", "Fenwick Sayer",
                     "Holroyd Bassett", "Underhill Crane", "Wetherall Dunn", "Kilbride Moss", "Ashdown Penrose",
                     "Carrick Lowe", "Stanmore Pryce", "Thackray Iles", "Bellamy Strand", "Quarmby Fitch",
                     "Grimshaw Ord", "Merriman Vale", "Sutcliffe Hanley", "Ellison Crook", "Tremlett Ash",
                     "Hargreaves Lund", "Bairstow Kent", "Duckworth Sale", "Pemberton Quay", "Lockwood Tyrer",
                     "Rushworth Gale", "Fothergill Wren", "Calloway Brice", "Northam Pell", "Iveson Clough",
                     "Mallinson Drew", "Jessop Harker"]
        sol_forms = ["Solicitors", "LLP", "Solicitors LLP", "Law", "Legal Services Ltd", "Solicitors Limited"]
        cmc_names = ["Ardley Claims Ltd", "Redwick Accident Claims Ltd", "Corran Claims Ltd",
                     "Hollin Injury Assist Ltd", "Tarrant Claims Ltd", "Elmore Claims Direct Ltd",
                     "Wyre Accident Line Ltd", "Brightholme Accident Services Ltd", "Ashby Claims Bureau Ltd",
                     "Pinmoor Injury Claims Ltd", "Motorvale Claims Ltd", "Harbourside Claims Group Ltd",
                     "Solent Claim Assist Ltd", "Kestrel Claims Management Ltd"]
        towns = {"Mersey": ["Liverpool", "Birkenhead", "Warrington", "Southport", "St Helens"],
                 "Pennine": ["Bradford", "Halifax", "Huddersfield", "Oldham", "Blackburn", "Burnley"],
                 "Wessex": ["Southampton", "Bournemouth", "Poole", "Salisbury", "Dorchester"],
                 "Fenland": ["Peterborough", "Cambridge", "Norwich", "King's Lynn", "Wisbech"],
                 "Severn": ["Gloucester", "Cheltenham", "Worcester", "Newport", "Cardiff", "Hereford"],
                 None: ["Manchester", "Leeds", "Birmingham", "London", "Sheffield", "Nottingham", "Bolton", "Preston"]}
        reps = []
        ids = r.choice(np.arange(1100, 9800), size=80, replace=False)
        k = 0
        home = []
        for i, nm in enumerate(sol_names):
            reg = K.REG[i % 5] if i < 35 else None
            town = towns[reg][int(r.integers(len(towns[reg])))]
            form = sol_forms[int(r.integers(len(sol_forms)))]
            reps.append(dict(ref="REP%04d" % ids[k], name="%s %s" % (nm, form), type="Solicitor practice",
                             regulator="SRA", number=str(int(r.integers(52000, 830000))), town=town, home=reg,
                             route="SOL"))
            k += 1
        for i, nm in enumerate(cmc_names):
            town = towns[None][int(r.integers(len(towns[None])))]
            key = None
            if nm.startswith("Solent"):
                town, key = "Southampton", "CMC_W"
            if nm.startswith("Kestrel"):
                town, key = "Halifax", "CMC_P"
            reps.append(dict(ref="REP%04d" % ids[k], name=nm, type="Claims management company", regulator="FCA",
                             number=str(int(r.integers(830000, 990000))), town=town, home=None, route="CMC",
                             wave=key))
            k += 1
        self.reps = reps
        self.rep_by_wave = {rp.get("wave"): rp["ref"] for rp in reps if rp.get("wave")}
        self._rw = {}

    def _rep_weights(self, reg, route):
        key = (reg, route)
        if key in self._rw:
            return self._rw[key]
        out = []
        for rp in self.reps:
            if rp["route"] != route or rp.get("wave"):
                out.append(0.0)
                continue
            if route == "SOL":
                out.append(3.0 if rp["home"] == reg else (0.25 if rp["home"] else 1.0))
            else:
                out.append(1.0 + 0.4 * ((K.REG.index(reg) + len(rp["name"])) % 3))
        w = np.array(out)
        self._rw[key] = w / w.sum()
        return self._rw[key]

    # ---------------------------------------------------------------- claims
    def _lag(self, route, n):
        r = self.r_lag
        spec = LAG[route]
        if spec[0] == "phx":
            v = r.exponential(spec[1], n) + (r.random(n) < 0.03) * r.exponential(45, n)
            return np.minimum(np.round(v), 900).astype(int)
        if spec[0] == "gamma":
            return np.minimum(np.round(r.gamma(spec[1], spec[2], n)), 1000).astype(int)
        med = self.P.get("cmc_med", spec[1]) if route == "CMC" else self.P.get("sol_med", spec[1])
        return np.minimum(np.round(r.lognormal(np.log(med), spec[2], n)), K.LIMITATION_DAYS).astype(int)

    def claims(self):
        r = self.r_claims
        out = []           # dicts, one per claim (claimant and head)
        for ay in K.ACCIDENT_YEARS:
            months = 12 if ay < 2026 else 9
            for reg in K.REG:
                for prod in ("PC", "LCV"):
                    fr = FREQ[reg] if prod == "PC" else VAN_FREQ
                    for hi, head in enumerate(K.HEADS):
                        f = fr[hi]
                        if prod == "PC" and head == "TPI":
                            f = f * self.P.get("tpi_" + reg, 1.0)
                        if prod == "PC" and head == "OD" and reg == "Severn":
                            f = f * self.P.get("sev_od", 1.0)
                        for m in range(1, months + 1):
                            lam = f / 100 * self.cy[(ay, m, reg, prod)] * SEASON[m - 1] * COVID.get(ay, np.ones(12))[m - 1]
                            if head == "TPI":
                                lam = lam / 1.28           # accidents; claimants per accident average 1.28
                            elif head == "TPPD":
                                lam = lam / 1.06
                            n = int(r.poisson(lam))
                            if not n:
                                continue
                            self._accidents(out, ay, m, reg, prod, head, n, r)
                        if prod == "PC" and head == "TPI" and (reg, ay) in WAVES:
                            per100, key = WAVES[(reg, ay)]
                            tot = sum(self.cy[(ay, m, reg, prod)] for m in range(1, months + 1))
                            n = int(r.poisson(per100 * self.P.get("w_" + key, 1.0) / 100 * tot / 1.28))
                            self._accidents(out, ay, None, reg, prod, head, n, r, wave=key)
        for i, c in enumerate(out):
            c["idx"] = i
        self.all_claims = out
        self.twins = []
        self._amounts()

    def _accidents(self, out, ay, m, reg, prod, head, n, r, wave=None):
        if m is None:
            months = 12 if ay < 2026 else 9
            mm = r.choice(np.arange(1, months + 1), size=n, p=SEASON[:months] / SEASON[:months].sum())
        else:
            mm = np.full(n, m)
        days = np.array([int(r.integers(_days_in(ay, int(x)))) for x in mm])
        acc = [dt.date(ay, int(x), 1) + dt.timedelta(days=int(d)) for x, d in zip(mm, days)]
        if head == "TPI":
            k = r.choice([1, 2, 3, 4], size=n, p=[0.80, 0.14, 0.05, 0.01])
            mix = TPI_MIX[ay]
        elif head == "TPPD":
            k = r.choice([1, 2], size=n, p=[0.94, 0.06])
            mix = MIX[head]
        else:
            k = np.ones(n, int)
            mix = MIX[head]
        if wave:
            routes = np.full(n, 4)
        else:
            routes = r.choice(5, size=n, p=np.array(mix) / np.sum(mix))
        for i in range(n):
            route = K.ROUTES[int(routes[i])]
            lag0 = int(self._lag(route, 1)[0])
            rep = None
            if route in ("SOL", "CMC"):
                if wave:
                    rep = self.rep_by_wave[wave]
                else:
                    w = self._rep_weights(reg, route)
                    rep = self.reps[int(r.choice(len(self.reps), p=w))]["ref"]
            blank = head in BLANK_TP and route == "PH" and int(k[i]) == 1 and self.r_blank.random() < BLANK_TP[head]
            for c in range(int(k[i])):
                lag = lag0 if c == 0 else min(lag0 + int(r.integers(0, 12)), K.LIMITATION_DAYS)
                if route == "PH" and c > 0:
                    lag = lag0
                cl = (c + 1) if head in ("TPI", "TPPD") and not blank else None
                out.append(dict(ay=ay, region=reg, product=prod, head=head, route=route, rep=rep, acc=acc[i],
                                lag=lag, claimant=cl, k=int(k[i]), accident=(ay, reg, prod, head, i, len(out) - c),
                                wave=wave))

    def _twins(self):
        """the online journey's abandoned first notifications, from 2 March 2026, for accidents in the last 30 days"""
        r = self.r_twin
        tw = []
        for c in self.all_claims:
            if c["route"] != "PH" or c["acc"] < K.ONLINE_FROM - dt.timedelta(days=0):
                continue
            note = c["acc"] + dt.timedelta(days=c["lag"])
            if note < K.ONLINE_FROM + dt.timedelta(days=2) or note >= K.EXTRACT or c["lag"] > 30:
                continue
            if c["head"] in ("TPI", "TPPD") and c.get("claimant") != 1:
                continue
            if c["head"] not in ("TPI", "TPPD") and c.get("claimant") is not None:
                continue
            if r.random() < TWIN_RATE[c["head"]]:
                d = dict(c)
                d["twin_of"] = c["idx"]
                d["route"] = "PH"
                d["claimant"] = None
                d["twin_hours"] = float(r.uniform(0.3, 46.0))
                tw.append(d)
                c["has_twin"] = True
        self.twins = tw

    def _amounts(self):
        r = self.r_amt
        sev = {"OD": (7.55, 0.85), "TPPD": (7.75, 0.8), "TPI": (8.6, 0.9), "THEFT": (8.9, 0.7), "FIRE": (8.7, 0.8),
               "GLASS": (5.55, 0.35)}
        nil = {"OD": 0.10, "TPPD": 0.15, "TPI": 0.18, "THEFT": 0.12, "FIRE": 0.10, "GLASS": 0.03}
        settle = {"OD": 45, "TPPD": 90, "TPI": 420, "THEFT": 70, "FIRE": 80, "GLASS": 12}
        for c in self.all_claims:
            note = c["acc"] + dt.timedelta(days=c["lag"])
            c["notified"] = note
            mu, sd = sev[c["head"]]
            amt = float(np.exp(r.normal(mu, sd)))
            isnil = r.random() < nil[c["head"]]
            dur = int(r.gamma(1.5, settle[c["head"]] / 1.5)) + 3
            closed = note + dt.timedelta(days=dur)
            if closed > K.EXTRACT:
                c["status"], c["closed_on"] = "Open", None
                paid = 0.0 if isnil else round(amt * float(r.uniform(0.0, 0.6)), 2)
                c["paid"], c["outstanding"] = paid, round(max(amt - paid, 250.0), 2)
            else:
                c["status"] = "Closed nil" if isnil else "Closed"
                c["closed_on"] = closed
                c["paid"], c["outstanding"] = (0.0 if isnil else round(amt, 2)), 0.0
        for t in self.twins:
            hrs = t.pop("twin_hours")
            t["twin_hours"] = hrs
            t["status"], t["paid"], t["outstanding"] = "Closed nil", 0.0, 0.0

    # ---------------------------------------------------------------- the policy book on 30 September 2026
    def policies(self):
        r, rc = self.r_pol, self.r_chg
        snap = K.EXTRACT
        vehicles, changes = [], []
        pol_no = 0
        moves = {"Mersey": (0.0, 0.34, 0.10, 0.08, 0.48), "Pennine": (0.46, 0.0, 0.12, 0.12, 0.30),
                 "Wessex": (0.10, 0.12, 0.0, 0.18, 0.60), "Fenland": (0.20, 0.25, 0.30, 0.0, 0.25),
                 "Severn": (0.30, 0.24, 0.30, 0.16, 0.0)}
        for reg in K.REG:
            for prod in ("PC", "LCV"):
                cars = CY2025[reg] * (1 + GROWTH) ** 1.75 * (1 if prod == "PC" else VAN_SHARE[reg])
                npol = int(round(cars / 1.085))
                starts = r.integers(0, 365, npol)
                for i in range(npol):
                    pol_no += 1
                    ts = dt.date(2025, 10, 1) + dt.timedelta(days=int(starts[i]))
                    te = dt.date(ts.year + 1, ts.month, ts.day) if not (ts.month == 2 and ts.day == 29) else dt.date(ts.year + 1, 3, 1)
                    cover = COVERS[int(r.choice(3, p=COVER_MIX[reg]))]
                    dist = DIST_PICK(r, reg)
                    nveh = int(r.choice([1, 2, 3], p=[0.93, 0.06, 0.01]))
                    canc = None
                    if r.random() < 0.065:
                        canc = ts + dt.timedelta(days=int(r.integers(1, 360)))
                        if canc >= te:
                            canc = None
                    pref = ("PC" if prod == "PC" else "CV") + "%07d" % (3100000 + pol_no * 7 % 6899999)
                    chan = ("Direct", "Aggregator", "Broker")[int(r.choice(3, p=[0.38, 0.49, 0.13]))]
                    prem = round(float(np.exp(r.normal(6.45 if prod == "PC" else 6.85, 0.35))), 2)
                    for v in range(nveh):
                        on = ts
                        vrm = VRM(r)
                        off = None
                        if r.random() < 0.045:
                            sub = ts + dt.timedelta(days=int(r.integers(5, 350)))
                            if sub <= snap:
                                off = sub
                                vehicles.append(dict(policy=pref, ts=ts, te=te, product=prod, cover=cover, dist=dist,
                                                     vrm=vrm, on=on, off=off, canc=canc, channel=chan, prem=prem))
                                changes.append(dict(policy=pref, type="VEHICLE", eff=sub, proc=sub - dt.timedelta(days=int(rc.integers(0, 4))),
                                                    old_vrm=vrm, new_vrm=None))
                                vrm2 = VRM(r)
                                changes[-1]["new_vrm"] = vrm2
                                vrm, on, off = vrm2, sub, None
                        vehicles.append(dict(policy=pref, ts=ts, te=te, product=prod, cover=cover, dist=dist, vrm=vrm,
                                             on=on, off=off, canc=canc, channel=chan, prem=prem))
                    # mid-term changes
                    if rc.random() < 0.058:
                        eff = ts + dt.timedelta(days=int(rc.integers(3, 340)))
                        if eff < te:
                            to = reg
                            if rc.random() < 0.31:
                                to = K.REG[int(rc.choice(5, p=moves[reg]))]
                            nd = DIST_PICK(rc, to, avoid=dist)
                            proc = eff - dt.timedelta(days=int(rc.integers(-6, 45)))
                            if proc <= snap:
                                changes.append(dict(policy=pref, type="ADDRESS", eff=eff, proc=proc, district=nd))
                                if rc.random() < 0.12:
                                    eff2 = eff + dt.timedelta(days=int(rc.integers(20, 200)))
                                    proc2 = eff2 - dt.timedelta(days=int(rc.integers(0, 15)))
                                    if eff2 < te and proc2 <= snap:
                                        to2 = to if rc.random() < 0.7 else K.REG[int(rc.choice(5, p=moves[to]))]
                                        changes.append(dict(policy=pref, type="ADDRESS", eff=eff2, proc=proc2,
                                                            district=DIST_PICK(rc, to2, avoid=nd)))
                    if rc.random() < 0.027:
                        eff = ts + dt.timedelta(days=int(rc.integers(10, 340)))
                        if eff < te:
                            new = {"COMP": "TPFT", "TPFT": "COMP", "TPO": "TPFT"}[cover]
                            if cover == "COMP" and rc.random() < 0.2:
                                new = "TPO"
                            proc = eff - dt.timedelta(days=int(rc.integers(-3, 30)))
                            if proc <= snap:
                                changes.append(dict(policy=pref, type="COVER", eff=eff, proc=proc, cover=new))
                    if rc.random() < 0.13:
                        eff = ts + dt.timedelta(days=int(rc.integers(1, 360)))
                        proc = eff - dt.timedelta(days=int(rc.integers(0, 10)))
                        if eff < te and proc <= snap:
                            changes.append(dict(policy=pref, type="DRIVER", eff=eff, proc=proc,
                                                detail=("Add named driver", "Remove named driver",
                                                        "Change main driver")[int(rc.choice(3, p=[0.55, 0.35, 0.10]))]))
        self.vehicles, self.changes = vehicles, changes


def _days_in(y, m):
    return ((dt.date(y + (m == 12), m % 12 + 1, 1)) - dt.date(y, m, 1)).days


_DW = {}


def DIST_PICK(r, reg, avoid=None):
    ds = K.DISTRICTS[reg]
    if reg not in _DW:
        g = np.random.default_rng(K.REG.index(reg) + 991)
        w = g.gamma(1.4, 1.0, len(ds))
        _DW[reg] = w / w.sum()
    while True:
        d = ds[int(r.choice(len(ds), p=_DW[reg]))]
        if d != avoid:
            return d


_LET = "ABCDEFGHJKLMNOPRSTUVWXY"


def VRM(r):
    a = _LET[int(r.integers(len(_LET)))] + _LET[int(r.integers(len(_LET)))]
    age = int(r.choice([15, 65, 16, 66, 17, 67, 18, 68, 19, 69, 20, 70, 21, 71, 22, 72, 23, 73, 24, 74, 25, 75, 14,
                        64, 13, 63, 12, 62]))
    b = "".join(_LET[int(r.integers(len(_LET)))] for _ in range(3))
    if b in ("LLM", "GPT"):       # withheld from issue, like the DVLA's own barred combinations
        b = b[:2] + _LET[(_LET.index(b[2]) + 1) % len(_LET)]
    return "%s%02d %s" % (a, age, b)
