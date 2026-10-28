"""The clean world for task304 architecture 3: the four settings' people and flows, the van's 2026 rota, the starts it
led to, the network's courses with their dispensing and laboratory results, and the pharmacies' needle exchange
registrations. Nothing here is messy; pack.py writes the shipped files from it.

Each record is derived from a history drawn once, forward in time, so every file holds what its producer could see:
the van's tablet holds only its own contacts, the hostels list who lives there, the register holds the courses as the
clinic entered them (a planned end written at the start), the dispensing log holds the packs that left the pharmacy."""
import datetime as dt
import hashlib
import zoneinfo

import numpy as np

import params as P

D = dt.date
DAY = dt.timedelta(days=1)
UK = zoneinfo.ZoneInfo("Europe/London")
UTC = dt.timezone.utc


def od(x):
    return D.fromordinal(int(x))


def months(a, b):
    """(year, month) from a to b inclusive"""
    y, m = a
    out = []
    while (y, m) <= b:
        out.append((y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def month_days(y, m):
    a = D(y, m, 1)
    b = D(y + (m == 12), m % 12 + 1, 1)
    return a, b - DAY


class World:
    def __init__(self):
        self.rng = None
        self._ids, self._seq = set(), 0
        self.hostel_res, self.ap_res = [], []
        self.ds_monthly, self.ds_2026 = {}, []
        self.nsp_reg, self.nsp_2026 = [], []
        self.pharmacies = []
        self.contacts, self.starts = [], []
        self.courses, self.dispensing, self.lab = [], [], []
        self.status = {}            # pid -> 'active' | 'cleared' | 'never'
        self.conv = {}              # pid -> the day a hostel resident who tested negative became infected

    # ------------------------------------------------------------------ identities
    def pid(self):
        while True:
            h = hashlib.sha256(("fhn-%d-%d" % (P.SEED, self._seq)).encode()).hexdigest().upper()
            self._seq += 1
            x = "FHN" + "".join(c for c in h if c not in "01IO")[:7]
            if x not in self._ids:
                self._ids.add(x)
                return x

    def use(self, seed):
        self.rng = np.random.default_rng(seed)

    def rdate(self, a, b):
        a, b = a.toordinal(), b.toordinal()
        return od(a) if b <= a else od(self.rng.integers(a, b + 1))

    def stamp(self, day, lo=9.5, hi=16.6):
        """a local working-hours time on `day`, returned in UTC (the van's tablet clock)"""
        r = self.rng
        sec = int(r.uniform(lo, hi) * 3600)
        local = dt.datetime(day.year, day.month, day.day, sec // 3600, sec // 60 % 60, sec % 60, tzinfo=UK)
        return local.astimezone(UTC).replace(tzinfo=None)

    def infect(self, pid, setting, pilot=False):
        r = self.rng
        p_act = P.ACTIVE_PILOT if pilot else P.ACTIVE[setting]
        p_clr = {"AP": 0.08, "HH": 0.10, "DS": 0.07, "NSP": 0.06}[setting]
        u = r.random()
        self.status[pid] = "active" if u < p_act else ("cleared" if u < p_act + p_clr else "never")


def rota_days():
    d, out = P.ROTA_START, {"HH": [], "NSP": [], "DS": [], "AP": []}
    while d <= P.ROTA_END:
        if d.weekday() < 5 and d not in P.BANK_HOLIDAYS:
            out[{0: "HH", 1: "HH", 2: "NSP", 3: "DS", 4: "AP"}[d.weekday()]].append(d)
        d += DAY
    return out


# ---------------------------------------------------------------------------- the settings
def _beds(W, places, stay, gap, start, shape=None):
    """each bed a renewal process from `start` to the as-of date; returns occupancies (move_in, move_out or None)"""
    r = W.rng
    occ = []
    for _ in range(places):
        back = r.exponential(stay) if shape is None else r.gamma(shape, stay / shape) * r.random()
        t_in = start.toordinal() - back
        t_out = start.toordinal() + (r.exponential(stay) if shape is None else r.gamma(shape, stay / shape) * r.random())
        while True:
            occ.append((od(t_in), None if t_out > P.AS_OF.toordinal() else od(t_out)))
            if t_out > P.AS_OF.toordinal():
                break
            t_in = t_out + 1 + r.exponential(gap)
            if t_in > P.AS_OF.toordinal():
                break
            t_out = t_in + (r.exponential(stay) if shape is None else max(7.0, r.gamma(shape, stay / shape)))
    return occ


def hostels(W):
    for name, prov, places in P.HOSTELS:
        for t_in, t_out in _beds(W, places, P.HH_STAY, P.HH_GAP, D(2019, 1, 1)):
            pid = W.pid()
            W.infect(pid, "HH")
            W.hostel_res.append(dict(pid=pid, hostel=name, provider=prov, move_in=t_in, move_out=t_out))


def approved_premises(W):
    for name, places in P.AP_PREMISES:
        for t_in, t_out in _beds(W, places, P.AP_STAY, P.AP_GAP, D(2023, 1, 1), shape=4.0):
            pid = W.pid()
            W.infect(pid, "AP")
            W.ap_res.append(dict(pid=pid, premises=name, arrive=t_in, leave=t_out,
                                 engages=W.rng.random() < P.COVER["AP"]))


def recovery(W):
    r = W.rng
    for y, m in months((2023, 10), (2026, 9)):
        lam = P.DS_MONTHLY * (0.91 if m == 12 else 1.0) * (1.04 if m in (1, 3) else 1.0)
        n = int(r.poisson(lam))
        W.ds_monthly[(y, m)] = n
        if y == 2026:
            a, b = month_days(y, m)
            for _ in range(n):
                d = W.rdate(a, b)
                while d.weekday() > 4:
                    d = W.rdate(a, b)
                pid = W.pid()
                W.infect(pid, "DS")
                W.ds_2026.append(dict(pid=pid, date=d))


PHARMACY_NAMES = [
    ("FW318", "Gorse Street Pharmacy", "41 Gorse Street", "FW3"), ("FK207", "Halden Chemists", "2 Halden Parade", "FW7"),
    ("FN562", "Morrow & Pike Pharmacy", "118 Wexley Road", "FW2"), ("FA915", "Stanmoor Co-operative Pharmacy",
                                                                      "Unit 4, Stanmoor Centre", "FW9"),
    ("FC433", "Kestle Road Pharmacy", "77 Kestle Road", "FW3"), ("FD148", "Tannery Lane Chemist", "9 Tannery Lane", "FW1"),
    ("FE726", "Riverside Pharmacy", "Riverside Health Centre, Quay Street", "FW1"),
    ("FG381", "Ashworth's Pharmacy", "230 Calder Street", "FW4"), ("FH654", "Northgate Late Night Pharmacy",
                                                                    "15 Northgate", "FW1"),
    ("FJ029", "Pennant Pharmacy", "3 Pennant Way", "FW8"), ("FL870", "Hollins Chemist", "61 Hollins Lane", "FW6"),
    ("FM413", "Bridge End Pharmacy", "Bridge End Surgery, Mill Road", "FW5"),
    ("FP292", "Fenwold Central Pharmacy", "12 Market Place", "FW1"), ("FQ745", "Okeby Pharmacy", "88 Okeby Road", "FW10"),
    ("FR136", "Whitcliffe Pharmacy", "5 Whitcliffe Green", "FW11"), ("FS508", "Lowmoor Pharmacy",
                                                                     "Lowmoor Shopping Parade", "FW12"),
    ("FT967", "Dunmore & Sons Chemists", "140 Station Road", "FW2"), ("FV214", "Carrbrook Pharmacy",
                                                                       "1 Carrbrook Rise", "FW13"),
    ("FX553", "St Ann's Pharmacy", "St Ann's Medical Centre, Vale Street", "FW4"),
    ("FY380", "Moorside Pharmacy", "27 Moorside Road", "FW14"), ("FZ671", "Coldharbour Chemist",
                                                                  "Coldharbour Lane", "FW6"),
    ("FB842", "Wexley Road Pharmacy", "301 Wexley Road", "FW2"), ("FF105", "Abbeygate Pharmacy (Fenwold Station)",
                                                                   "Concourse, Fenwold Station", "FW1"),
    ("FU469", "Highfield Pharmacy", "54 Highfield Avenue", "FW15")]


def pharmacies(W):
    r = W.rng
    w = r.lognormal(0.0, 0.42, len(PHARMACY_NAMES))
    for (code, name, addr, dist), wi in zip(PHARMACY_NAMES, w):
        if code in P.PILOTS:
            wi = 2.0 * float(np.median(w))
        W.pharmacies.append(dict(code=code, name=name, address=addr, district=dist, weight=float(wi),
                                 level=("Level 2" if r.random() < 0.4 else "Level 1")))
    tot = sum(p["weight"] for p in W.pharmacies)
    for p in W.pharmacies:
        p["weight"] /= tot


def nsp(W):
    """first registrations from the system's go-live (April 2019), and the 'New' rows the system writes when a client
    whose registration lapsed (twelve months without a visit) comes back"""
    r = W.rng
    codes = [p["code"] for p in W.pharmacies]
    wts = np.array([p["weight"] for p in W.pharmacies])
    clients, seq, used = [], 0, set()
    for y, m in months((2019, 4), (2026, 9)):
        a, b = month_days(y, m)
        lam = P.NSP_MONTHLY * (0.94 if (y, m) < (2021, 1) else 1.0) * (0.85 if (y, m) in ((2020, 4), (2020, 5)) else 1)
        for _ in range(int(r.poisson(lam))):
            seq += 1
            client = "N%06d" % int(r.integers(100000, 999999))
            while client in used:
                client = "N%06d" % int(r.integers(100000, 999999))
            used.add(client)
            ph = codes[int(r.choice(len(codes), p=wts))]
            d = W.rdate(a, b)
            clients.append((client, ph, d))
            W.nsp_reg.append(dict(client=client, pharmacy=ph, date=d, first=True))
            if y == 2026 and d <= P.ROTA_END:
                pid = W.pid()
                pilot = ph in P.PILOTS and d >= P.PILOTS[ph]
                W.infect(pid, "NSP", pilot=pilot)
                W.nsp_2026.append(dict(pid=pid, pharmacy=ph, date=d, pilot=pilot))
        older = [c for c in clients if c[2] <= D(y - 1, m, 1) - 30 * DAY]
        n_re = int(r.poisson(P.NSP_MONTHLY * P.NSP_REISSUE / (1 - P.NSP_REISSUE))) if older else 0
        for _ in range(n_re):
            c = older[int(r.integers(len(older)))]
            ph = c[1] if r.random() < 0.7 else codes[int(r.choice(len(codes), p=wts))]
            W.nsp_reg.append(dict(client=c[0], pharmacy=ph, date=W.rdate(a, b), first=False))


# ---------------------------------------------------------------------------- the van's 2026 rota
def _contact(W, pid, setting, site, day):
    r = W.rng
    acc = r.random() < P.ACCEPT[setting]
    st = W.status[pid]
    if pid in W.conv and day >= W.conv[pid]:
        st = "active"
    ab = ("Reactive" if st in ("active", "cleared") else "Non-reactive") if acc else ""
    rna = ("Detected" if st == "active" else "Not detected") if acc and ab == "Reactive" else ""
    c = dict(pid=pid, setting=setting, site=site, when=W.stamp(day), accepted=acc, ab=ab, rna=rna)
    W.contacts.append(c)
    return c


def rota_hh(W):
    """the hostels: worked through in blocks, every resident present offered once in the hostel's block"""
    r = W.rng
    hh = rota_days()["HH"]
    order = [P.HOSTELS[i] for i in r.permutation(len(P.HOSTELS))]
    cap = np.array([h[2] for h in order], dtype=float)
    alloc = np.floor(cap / cap.sum() * len(hh)).astype(int)
    for i in np.argsort(-(cap / cap.sum() * len(hh) - alloc))[:len(hh) - alloc.sum()]:
        alloc[i] += 1
    pos = 0
    for (name, prov, places), k in zip(order, alloc):
        block = hh[pos:pos + k]
        pos += k
        for res in W.hostel_res:
            if res["hostel"] != name or res["move_in"] > block[-1]:
                continue
            if res["move_out"] is not None and res["move_out"] <= block[0]:
                continue
            here = [d for d in block if d >= res["move_in"] and (res["move_out"] is None or d < res["move_out"])]
            if not here or r.random() < P.HH_ABSENT:
                continue
            _contact(W, res["pid"], "HH", name, here[int(r.integers(len(here)))])


def rota_ap(W):
    """the approved premises: one premises each Friday in turn, residents offered at their first visit"""
    names = [p[0] for p in P.AP_PREMISES]
    for i, d in enumerate(rota_days()["AP"]):
        name = names[i % 3]
        for res in W.ap_res:
            if res["premises"] == name and res["engages"] and not res.get("met") and res["arrive"] <= d and (
                    res["leave"] is None or d < res["leave"]):
                res["met"] = True
                _contact(W, res["pid"], "AP", name, d)


def rota_ds(W):
    r = W.rng
    days = rota_days()["DS"]
    for e in W.ds_2026:
        nxt = [d for d in days if e["date"] <= d <= e["date"] + 6 * DAY]
        if nxt and r.random() < P.COVER["DS"]:
            _contact(W, e["pid"], "DS", "Recovery hub", nxt[0])


def rota_nsp(W):
    r = W.rng
    days = rota_days()["NSP"]
    for e in W.nsp_2026:
        nxt = [d for d in days if e["date"] <= d <= e["date"] + 27 * DAY]
        if nxt and r.random() < P.COVER["NSP"]:
            _contact(W, e["pid"], "NSP", e["pharmacy"], nxt[int(r.integers(len(nxt)))])


def starts(W, setting):
    """the nurse prescribes on the van; most who start do so within days, a few long after twelve weeks"""
    r = W.rng
    for c in [c for c in W.contacts if c["setting"] == setting and c["rna"] == "Detected"]:
        test = c["when"].date()
        if r.random() < P.START12[setting]:
            start = test + int(1 + r.gamma(1.6, 5.5)) * DAY
        elif r.random() < 0.12:
            start = test + int(r.integers(92, 220)) * DAY
        else:
            continue
        if start <= P.AS_OF:
            W.starts.append(dict(pid=c["pid"], setting=setting, test=test, start=start,
                                 clinic="HHC" if setting == "HH" else "COMM"))


# ---------------------------------------------------------------------------- courses, packs and results
def _scale(y):
    return {2015: 0.7, 2016: 1.25, 2017: 1.45, 2018: 1.5, 2019: 1.35, 2020: 0.6, 2021: 0.85, 2022: 0.95,
            2023: 1.0, 2024: 1.0, 2025: 1.0, 2026: 0.97}[y]


def _course(W, pid, clinic, start, role="Nurse", site="", source="", forced_weeks=None):
    r = W.rng
    weeks = forced_weeks or (8 if r.random() < 0.6 else 12)
    product = "Glecaprevir/pibrentasvir" if weeks == 8 else "Sofosbuvir/velpatasvir"
    n = weeks // 4
    stop = int(r.integers(1, n)) if r.random() < 0.08 else n        # packs collected before stopping
    packs, d = [], start
    for i in range(stop):
        packs.append(d)
        if r.random() < 0.3:
            d = d + int(28 + r.integers(1, 15)) * DAY
        else:
            d = d + int(28 - r.integers(0, 4)) * DAY
    last = packs[-1] + 27 * DAY
    c = dict(pid=pid, clinic=clinic, start=start, weeks=weeks, product=product, packs=packs, last=last,
             planned_end=start + (7 * weeks - 1) * DAY, early_stop=stop < n, role=role, site=site, source=source)
    W.courses.append(c)
    return c


def _outcome(W, c):
    """twelve-week result (or none), the occasional early sample, a later cure seen on an annual test"""
    r = W.rng
    cured = r.random() < (0.85 if c["early_stop"] else 0.965)
    c["cured"] = cured
    tests = []
    if r.random() < 0.07:
        tests.append(c["last"] + int(r.integers(56, 84)) * DAY)
    if r.random() < 0.80:
        tests.append(c["last"] + int(r.integers(84, 120)) * DAY)
    elif cured and r.random() < 0.25:
        tests.append(c["last"] + int(r.integers(200, 560)) * DAY)
    low = cured and r.random() < 0.035
    for t in tests:
        if t > P.AS_OF:
            continue
        if not cured:
            W.lab.append(dict(pid=c["pid"], date=t, kind="RNA", result="Detected", vl=int(r.lognormal(12.5, 1.2)),
                              loc=c["clinic"]))
        elif low and t >= P.ASSAY_CHANGE and t >= c["last"] + 84 * DAY:
            W.lab.append(dict(pid=c["pid"], date=t, kind="RNA", result="Detected <12", vl=None, loc=c["clinic"]))
            break
        else:
            W.lab.append(dict(pid=c["pid"], date=t, kind="RNA", result="Not detected", vl=None, loc=c["clinic"]))
    return cured


def network_courses(W):
    r = W.rng
    for clinic in P.CLINICS:
        for y in range(2015, 2027):
            lam = P.CLINIC_YEARLY[clinic] * _scale(y) * (0.75 if y == 2026 else 1.0)
            for _ in range(int(r.poisson(lam))):
                start = W.rdate(D(y, 1, 1), min(D(y, 12, 31), P.AS_OF - 20 * DAY))
                pid = W.pid()
                W.status[pid] = "active"
                W.lab.append(dict(pid=pid, date=start - int(r.integers(14, 70)) * DAY, kind="RNA", result="Detected",
                                  vl=int(r.lognormal(13.0, 1.1)), loc=clinic))
                c = _course(W, pid, clinic, start, role="Consultant" if clinic == "HEP" and r.random() < 0.5 else
                            "Nurse", source=str(r.choice(["GP", "Drug service", "Self", "Sexual health", "Prison",
                                                           "Hospital", "Outreach"])))
                if not _outcome(W, c) and r.random() < 0.7:
                    s2 = c["last"] + int(r.integers(150, 300)) * DAY
                    if s2 < P.AS_OF - 20 * DAY:
                        c2 = _course(W, pid, "HEP", s2, role="Consultant", source="Re-treatment", forced_weeks=12)
                        _outcome(W, c2)
    for s in W.starts:
        c = _course(W, s["pid"], s["clinic"], s["start"], source="Brannock Trust van")
        _outcome(W, c)
    # community pharmacist prescribers: since each pilot's launch its pharmacist tests new registrants at registration
    for reg in W.nsp_reg:
        launch = P.PILOTS.get(reg["pharmacy"])
        if not reg["first"] or launch is None or reg["date"] < launch or reg["date"] > P.AS_OF - 14 * DAY:
            continue
        if r.random() < 0.9 * P.ACTIVE["NSP"] * 0.92:
            pid = W.pid()
            W.status[pid] = "active"
            c = _course(W, pid, "PHARM", reg["date"] + int(r.integers(0, 9)) * DAY, role="Pharmacist",
                        site=reg["pharmacy"], source="Needle exchange", forced_weeks=8)
            _outcome(W, c)


def background_lab(W):
    """antibody screens across the network, with the laboratory's RNA test on every reactive sample"""
    r = W.rng
    locs = (["GP"] * 46 + ["Drug service"] * 18 + ["Sexual health"] * 14 + ["Prison"] * 9 + ["Antenatal"] * 7 +
            ["Emergency department"] * 6)
    for y, m in months((2015, 1), (2026, 9)):
        a, b = month_days(y, m)
        for _ in range(int(r.poisson(2350 / 12 * (0.62 if (y, m) in ((2020, 4), (2020, 5)) else 1.0)))):
            pid = W.pid()
            d = W.rdate(a, b)
            loc = locs[int(r.integers(len(locs)))]
            u = r.random()
            if u < 0.024:
                W.lab.append(dict(pid=pid, date=d, kind="AB", result="Reactive", vl=None, loc=loc))
                act = r.random() < 0.55
                W.lab.append(dict(pid=pid, date=d, kind="RNA", result="Detected" if act else "Not detected",
                                  vl=int(r.lognormal(13, 1.2)) if act else None, loc=loc))
            else:
                W.lab.append(dict(pid=pid, date=d, kind="AB", result="Non-reactive", vl=None, loc=loc))


def hostel_lab(W):
    """the homeless health clinic's screens of hostel residents; new infections among those who tested negative"""
    r = W.rng
    for res in W.hostel_res:
        a = max(res["move_in"], D(2019, 1, 1))
        b = min(res["move_out"] or P.AS_OF, P.AS_OF)
        if b <= a:
            continue
        yrs = (b - a).days / 365.25
        k = int(r.poisson(0.55 * yrs))
        dates = sorted(W.rdate(a, b) for _ in range(k))
        st = W.status[res["pid"]]
        conv = None
        if st == "never":
            t = r.exponential(1 / P.HOSTEL_INCIDENCE)
            if t < yrs:
                conv = a + int(t * 365.25) * DAY
        for d in dates:
            pos = st in ("active", "cleared") or (conv is not None and d >= conv)
            W.lab.append(dict(pid=res["pid"], date=d, kind="AB", result="Reactive" if pos else "Non-reactive",
                              vl=None, loc="HHC"))
            if pos:
                act = st == "active" or conv is not None
                W.lab.append(dict(pid=res["pid"], date=d, kind="RNA", result="Detected" if act else "Not detected",
                                  vl=int(r.lognormal(12.8, 1.1)) if act else None, loc="HHC"))
        if conv is not None:
            W.conv[res["pid"]] = conv


def build(seeds=None):
    sd = dict(P.SEEDS, **(seeds or {}))
    W = World()
    W.use(sd["pharm"])
    pharmacies(W)
    W.use(sd["hh"])
    hostels(W)
    hostel_lab(W)
    rota_hh(W)
    starts(W, "HH")
    W.use(sd["ap"])
    approved_premises(W)
    rota_ap(W)
    starts(W, "AP")
    W.use(sd["ds"])
    recovery(W)
    rota_ds(W)
    starts(W, "DS")
    W.use(sd["nsp"])
    nsp(W)
    rota_nsp(W)
    starts(W, "NSP")
    W.contacts.sort(key=lambda c: c["when"])
    W.use(sd["courses"])
    network_courses(W)
    W.use(sd["lab"])
    background_lab(W)
    W.lab.sort(key=lambda x: (x["date"], x["pid"], x["kind"]))
    return W
