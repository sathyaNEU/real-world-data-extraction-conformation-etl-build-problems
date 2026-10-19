"""The clean truth behind the pack: every discharge with an operation on the hepatobiliary system or pancreas at the
state's hospitals from 2016 to June 2026, the person behind each, the deaths the consortium links, the plan's facility
claims for its members' resections, and the two 2026 releases. The eight eligible hospitals' 2023 to 2025 resections
come from core.py on their own streams; everything here draws from streams keyed on the seed and the entity."""
import datetime as dt

import numpy as np

import common as K
import core as C

D0 = dt.date(2016, 1, 1)
SMALL = [c for c in K.CODES if c.startswith("S")]
COMMUNITY = ["C", "D", "E", "F", "G", "H"] + SMALL


def _rng(seed, *key):
    return np.random.default_rng([seed] + [int(k) for k in key])


def _day(r, a, b):
    return a + dt.timedelta(days=int(r.integers(0, (b - a).days + 1)))


class Keys:
    """The consortium's encrypted person key: one per person, sixteen hex characters."""
    def __init__(self, seed):
        self.r = _rng(seed, 7, 7)
        self.seen = set()

    def new(self):
        while True:
            k = "".join("0123456789ABCDEF"[i] for i in self.r.integers(0, 16, 16))
            if k not in self.seen:
                self.seen.add(k)
                return k


COMORB_CODES = {
    "chf": ["I50.22", "I50.32", "I50.9", "I50.42"], "ckd": ["N18.30", "N18.31", "N18.4", "N18.32"],
    "copd": ["J44.9", "J44.1"], "liver": ["K74.60", "K76.6", "K70.30", "K74.69"],
    "dm": ["E11.9", "E11.65", "E11.22", "E10.9"], "af": ["I48.91", "I48.0", "I48.20"],
    "wtloss": ["R63.4", "E44.0", "E43"],
}
BACKGROUND_DX = [("I10", "Y"), ("E78.5", "Y"), ("K21.9", "Y"), ("E66.9", "Y"), ("Z79.4", "1"), ("Z87.891", "1"),
                 ("F17.210", "Y"), ("G47.33", "Y"), ("E03.9", "Y"), ("Z79.01", "1"), ("D64.9", "U"), ("M81.0", "Y"),
                 ("F32.A", "Y"), ("Z86.73", "1"), ("E87.1", "W")]
BG_CODES = {"htn": ("I10", "Y"), "lipid": ("E78.5", "Y"), "gerd": ("K21.9", "Y"), "obese": ("E66.9", "Y"),
            "smoke": ("Z87.891", "1"), "osa": ("G47.33", "Y"), "thyroid": ("E03.9", "Y"), "depress": ("F32.A", "Y")}
NOISE_DX = [("Z79.4", "1"), ("Z79.01", "1"), ("D64.9", "U"), ("E87.1", "W"), ("M81.0", "Y"), ("Z86.73", "1")]
COMPLICATIONS = ["K91.89", "J18.9", "A41.9", "N17.9", "K65.1", "I26.99", "K63.1", "J96.01", "R65.21", "K92.2",
                 "T81.43XA", "K31.84"]
DX_MAL = {"whip": [("C25.0", .70), ("C24.1", .12), ("C24.0", .06), ("C17.0", .04), ("C25.9", .08)],
          "distal": [("C25.1", .45), ("C25.2", .45), ("C25.4", .10)],
          "tot": [("C25.8", .55), ("C25.9", .30), ("C25.0", .15)]}
DX_BEN = [("D13.6", .45), ("K86.1", .25), ("K86.2", .12), ("K86.3", .08), ("D3A.8", .10)]


def _pick(r, items):
    p = np.array([w for _, w in items], float)
    return items[int(r.choice(len(items), p=p / p.sum()))][0]


def _payer(r, age):
    """Payer category and payer name. The plan's members sit in its commercial, Medicare Advantage and Medicaid lines."""
    u = r.random()
    if age >= 65:
        if u < .085:
            return "2", K.PLAN            # the plan's Medicare Advantage line
        if u < .62:
            return "1", "Medicare"
        if u < .74:
            return "2", "Other Medicare Advantage"
        if u < .80:
            return "3", "Medicaid"
        return "5", "Other commercial"
    if u < .11:
        return "5", K.PLAN
    if u < .19:
        return "3", "Medicaid"
    if u < .21:
        return "3", K.PLAN               # the plan's BadgerCare managed care line
    if u < .96:
        return "5", "Other commercial"
    return "9", "Self-pay"


def _resection_codes(r, kind, open_=True):
    if kind == "whip":
        base = ["0FBG0ZZ", "0DT90ZZ", "0FT40ZZ", "0F190ZB"]
        if r.random() < .7:
            base.append("0D160ZA")
        return base
    if kind == "tot":
        return ["0FTG0ZZ", "0DT90ZZ", "07TP0ZZ"] + (["0F190ZB"] if r.random() < .6 else [])
    return (["0FBG0ZZ"] if open_ else ["0FBG4ZZ"]) + (["07TP0ZZ"] if r.random() < .7 else [])


def _stay(r, adm, los_med):
    los = max(2, int(round(r.lognormal(np.log(los_med), .40))))
    return adm + dt.timedelta(days=los)


def _record(**kw):
    rec = dict(admit_type="3", admit_source="1", disposition="01", payer_cat="5", payer="Other commercial",
               dx=[], px=[], resub=None)
    rec.update(kw)
    return rec


def index_details(seed, ix, keys):
    """Dates, codes, payers and the earlier admissions of the eight hospitals' 2023 to 2025 resections."""
    recs, persons, deaths, earlier = [], [], [], []
    hi_of = {h: i for i, h in enumerate(C.H)}
    for (h, yr), grp in ix.groupby(["h", "year"], sort=False):
        r = _rng(seed, 5000 + hi_of[h], yr)
        r2 = _rng(seed, 6000 + hi_of[h], yr)
        for _, o in grp.iterrows():
            key = keys.new()
            op = _day(r, dt.date(yr, 1, 2), dt.date(yr, 12, 22))
            if o.urg:
                adm = op - dt.timedelta(days=int(r.integers(1, 9)))
                atype = "1" if r.random() < .3 else "2"
                asrc = "7" if r.random() < .6 else "1"
            else:
                adm = op - dt.timedelta(days=int(r.random() < .15))
                atype, asrc = "3", "1"
            kind = "tot" if o.tot else ("whip" if o.whip else "distal")
            sex = "M" if o.male else "F"
            age = float(o.age)
            dob = op - dt.timedelta(days=int(age * 365.25) + int(r.integers(0, 365)))
            los_med = 9 if kind != "distal" else 6
            dis = _stay(r, op, los_med + (6 if o.comp else 0))
            disp = "01"
            death_day = None
            if o.dead:
                if r.random() < .38:
                    death_day = int(r.integers(2, 41))
                    dis = op + dt.timedelta(days=death_day)
                    disp = "20"
                else:
                    dis = min(dis, op + dt.timedelta(days=60))
                    death_day = int(r.integers((dis - op).days + 3, 91))
                    disp = ["50", "51", "06", "03", "01"][int(r.choice(5, p=[.25, .15, .2, .25, .15]))]
            else:
                u = r.random()
                disp = "01" if u < .52 else "06" if u < .82 else "03" if u < .93 else "62" if u < .98 else "02"
            if yr == 2025 and dis > dt.date(2025, 12, 31):
                # the 2025 file closes on 31 December: a late-December stay that ran into January would sit in the
                # 2026 release, so the world keeps the window's stays inside its files
                if disp == "20":
                    disp, dis = "50", dt.date(2025, 12, 31)
                    death_day = max(death_day, (dis - op).days + 1)
                else:
                    dis = dt.date(2025, 12, 31)
            pcat, payer = _payer(r, age)
            pdx = _pick(r, DX_MAL[kind] if o.mal else DX_BEN)
            if o.redo and not o.mal and r.random() < .6:
                pdx = "K86.1"
            dx = [(pdx, "Y")]
            for c in ["chf", "ckd", "copd", "liver", "dm", "af", "wtloss"]:
                if o[c]:
                    codes = COMORB_CODES[c]
                    dx.append((codes[int(r.integers(0, len(codes)))], "Y"))
            for c in C.BACKGROUND:
                if o[c]:
                    dx.append(BG_CODES[c])
            for code, poa in NOISE_DX:
                if r.random() < .08:
                    dx.append((code, poa))
            if o.comp:
                for code in r.choice(COMPLICATIONS, size=int(r.integers(1, 4)), replace=False):
                    dx.append((str(code), "N"))
            if o.stent:
                dx.append(("Z95.828", "1") if r.random() < .5 else ("K83.1", "Y"))
            px = [(c, op) for c in _resection_codes(r, kind, open_=(r.random() < .78 or h not in ("A", "B")))]
            rec = _record(key=key, hosp=h, admit=adm, discharge=dis, op=op, sex=sex, dob=dob, admit_type=atype,
                          admit_source=asrc, disposition=disp, payer_cat=pcat, payer=payer, dx=dx, px=px,
                          index=True, kind=kind, core=(h, int(yr), int(o.k)))
            recs.append(rec)
            persons.append(dict(key=key, sex=sex, dob=dob))
            if death_day is not None:
                deaths.append(dict(key=key, date=op + dt.timedelta(days=death_day)))
            elif r.random() < (.30 if o.mal else .06):
                # later deaths of the patients who lived past 90 days
                deaths.append(dict(key=key, date=op + dt.timedelta(days=int(r.integers(120, 1100)))))
            # the earlier admissions: the operation a re-operation follows, a gallbladder removal, a stent
            if o.redo:
                eh = (h if r2.random() < .35 else COMMUNITY[int(r2.integers(0, len(COMMUNITY)))]) if h in ("A", "B") \
                    else (h if r2.random() < .5 else COMMUNITY[int(r2.integers(0, len(COMMUNITY)))])
                eh = "G2" if eh == "G" and r2.random() < .3 else eh
                last = min(op - dt.timedelta(days=150), dt.date(2022, 12, 20))
                # most re-operations follow an operation of the last few years; a few go back to 2016 to 2018
                if r2.random() < .12:
                    ed = _day(r2, dt.date(2016, 2, 1), dt.date(2018, 12, 15))
                else:
                    ed = _day(r2, dt.date(2019, 1, 7), last)
                code = ["0FBG0ZZ", "0FBG4ZZ", "0F1D0ZB", "0F190ZB", "0F190Z3", "0FB90ZZ", "0FCG0ZZ", "0FC90ZZ"][
                    int(r2.choice(8, p=[.20, .08, .15, .17, .08, .10, .15, .07]))]
                edx = {"0FBG0ZZ": "D13.6", "0FBG4ZZ": "D13.6", "0F1D0ZB": "K86.1", "0F190ZB": "K83.1",
                       "0F190Z3": "K83.1", "0FB90ZZ": "K83.09", "0FCG0ZZ": "K85.11", "0FC90ZZ": "K80.50"}[code]
                if code in ("0FBG0ZZ", "0FBG4ZZ") and r2.random() < .4:
                    edx = "C25.1"
                earlier.append(_record(key=key, hosp=eh, admit=ed - dt.timedelta(days=int(r2.random() < .2)),
                                       discharge=_stay(r2, ed, 7), op=ed, sex=sex, dob=dob, dx=[(edx, "Y")],
                                       px=[(code, ed)], payer_cat=pcat, payer=payer, index=False, kind="earlier"))
            if o.chole:
                cd = _day(r2, dt.date(2016, 1, 10), min(op - dt.timedelta(days=60), dt.date(2025, 6, 1)))
                earlier.append(_record(key=key, hosp=COMMUNITY[int(r2.integers(0, len(COMMUNITY)))], admit=cd,
                                       discharge=cd + dt.timedelta(days=int(r2.integers(1, 4))), op=cd, sex=sex,
                                       dob=dob, dx=[("K80.20" if r2.random() < .6 else "K81.0", "Y")],
                                       px=[("0FT44ZZ" if r2.random() < .9 else "0FT40ZZ", cd)], admit_type="2",
                                       payer_cat=pcat, payer=payer, index=False, kind="chole"))
            if o.stent:
                sd = op - dt.timedelta(days=int(r2.integers(10, 61)))
                sh = h if r2.random() < .6 else COMMUNITY[int(r2.integers(0, len(COMMUNITY)))]
                earlier.append(_record(key=key, hosp=sh, admit=sd, discharge=sd + dt.timedelta(days=int(r2.integers(2, 6))),
                                       op=sd, sex=sex, dob=dob, dx=[(pdx if pdx.startswith("C") else "K83.1", "Y"),
                                                                    ("K83.09" if r2.random() < .4 else "R17", "Y")],
                                       px=[("0F798DZ", sd)] + ([("0FC98ZZ", sd)] if r2.random() < .4 else []),
                                       admit_type="2", payer_cat=pcat, payer=payer, index=False, kind="ercp"))
    return recs, persons, deaths, earlier


# pancreatic resections before the window, by hospital and year (means), and the small hospitals' throughout
EARLY_RES = {
    "A": [104, 111, 117, 123, 98, 129, 137], "B": [80, 85, 90, 95, 81, 100, 108], "C": [58, 62, 66, 70, 59, 76, 82],
    "D": [41, 45, 50, 55, 46, 60, 66], "E": [35, 38, 42, 46, 39, 52, 57], "F": [30, 33, 36, 40, 34, 45, 50],
    "G": [17, 19, 22, 25, 21, 30, 36], "G2": [12, 11, 10, 9, 7, 8, 6], "H": [20, 22, 25, 28, 23, 33, 38],
}
SMALL_RES = 5.0          # a small hospital's resections a year
H1_RES = dict(A=76, B=63, C=47, D=40, E=33, F=30, G=28, H=24)   # January to June 2026, means
# other operations on the hepatobiliary system and pancreas a year, by hospital size
OTHER = dict(chole=1500, ercp=820, liver=110, duct=55, biopsy=70, drain=60)


def background(seed, keys):
    """Every other discharge in the file: the resections before the window and at the small hospitals, the
    gallbladder removals, the endoscopic procedures, the liver and duct operations, biopsies and drainages."""
    recs, persons, deaths = [], [], []
    size = {"A": 3.2, "B": 2.8, "C": 2.0, "D": 1.6, "E": 1.4, "F": 1.3, "G": 1.1, "G2": .5, "H": 1.0}
    for s in SMALL:
        size[s] = .45
    tot = sum(size.values())
    hosp_index = {c: i for i, c in enumerate(K.CODES)}
    for yr in range(2016, 2027):
        last = dt.date(yr, 12, 31) if yr < 2026 else dt.date(2026, 6, 30)
        for code in K.CODES:
            if code == "G2" and yr > 2024:
                continue
            r = _rng(seed, 9000 + hosp_index[code], yr)
            n_res = 0
            if yr <= 2022 and code in EARLY_RES:
                n_res = int(r.poisson(EARLY_RES[code][yr - 2016]))
            elif code in SMALL:
                n_res = int(r.poisson(SMALL_RES))
            elif yr == 2026 and code in H1_RES:
                n_res = int(r.poisson(H1_RES[code]))
            if code == "G2" and yr >= 2023:
                n_res = 0
            frac = (1.0 if yr < 2026 else .5) * size[code] / tot
            counts = {k: int(r.poisson(v * frac)) for k, v in OTHER.items()}
            counts["res"] = n_res
            for kind, n in counts.items():
                for _ in range(n):
                    key = keys.new()
                    age = float(np.clip(r.normal(58 if kind == "chole" else 66, 15 if kind == "chole" else 11), 18, 97))
                    adm = _day(r, dt.date(yr, 1, 1), last - dt.timedelta(days=8))
                    sex = "M" if r.random() < (.40 if kind == "chole" else .52) else "F"
                    dob = adm - dt.timedelta(days=int(age * 365.25) + int(r.integers(0, 365)))
                    pcat, payer = _payer(r, age)
                    if kind == "res":
                        sub = "whip" if r.random() < .62 else ("tot" if r.random() < .12 else "distal")
                        mal = r.random() < .72
                        op = adm + dt.timedelta(days=int(r.random() < .15))
                        dx = [(_pick(r, DX_MAL[sub] if mal else DX_BEN), "Y")]
                        px = [(c, op) for c in _resection_codes(r, sub, open_=r.random() < .8)]
                        dis = _stay(r, op, 9 if sub != "distal" else 6)
                        dead = r.random() < .075
                    elif kind == "chole":
                        op = adm + dt.timedelta(days=int(r.integers(0, 3)))
                        dx = [("K80.20" if r.random() < .5 else "K81.0" if r.random() < .5 else "K80.10", "Y")]
                        px = [("0FT44ZZ" if r.random() < .93 else "0FT40ZZ", op)]
                        dis = _stay(r, op, 2)
                        dead = r.random() < .006
                    elif kind == "ercp":
                        op = adm + dt.timedelta(days=int(r.integers(0, 3)))
                        dx = [("K80.50" if r.random() < .45 else "K83.1" if r.random() < .5 else "C25.0", "Y")]
                        px = [("0F798DZ" if r.random() < .55 else "0FC98ZZ", op)]
                        dis = _stay(r, op, 4)
                        dead = r.random() < .02
                    elif kind == "liver":
                        op = adm
                        dx = [("C78.7" if r.random() < .5 else "C22.0" if r.random() < .5 else "D13.4", "Y")]
                        px = [(["0FB00ZZ", "0FT00ZZ", "0FB04ZZ", "0FB24ZZ"][int(r.integers(0, 4))], op)]
                        dis = _stay(r, op, 6)
                        dead = r.random() < .03
                    elif kind == "duct":
                        op = adm
                        dx = [("K83.1" if r.random() < .5 else "K80.50", "Y")]
                        px = [(["0F190ZB", "0F190Z3", "0FB90ZZ", "0FC90ZZ", "0F1D0ZB"][int(r.integers(0, 5))], op)]
                        dis = _stay(r, op, 7)
                        dead = r.random() < .03
                    elif kind == "biopsy":
                        op = adm
                        dx = [("C25.0" if r.random() < .7 else "C25.9", "Y")]
                        px = [(["0FBG0ZX", "0FBG3ZX", "0FBG8ZX"][int(r.choice(3, p=[.35, .45, .2]))], op)]
                        dis = _stay(r, op, 4)
                        dead = r.random() < .05
                    else:   # drainage of the pancreas or a collection
                        op = adm + dt.timedelta(days=int(r.integers(0, 4)))
                        dx = [("K85.11" if r.random() < .5 else "K86.3", "Y")]
                        px = [("0F9G30Z" if r.random() < .6 else "0F9G00Z", op)]
                        dis = _stay(r, op, 8)
                        dead = r.random() < .04
                    for c, poa in BACKGROUND_DX:
                        if r.random() < .12:
                            dx.append((c, poa))
                    disp = "20" if dead and r.random() < .5 else ("01" if r.random() < .7 else "06")
                    rec = _record(key=key, hosp=code, admit=adm, discharge=dis, op=op, sex=sex, dob=dob, dx=dx, px=px,
                                  disposition=disp, payer_cat=pcat, payer=payer, index=False, kind=kind,
                                  admit_type="3" if kind in ("res", "liver") else "2")
                    recs.append(rec)
                    persons.append(dict(key=key, sex=sex, dob=dob))
                    if disp == "20":
                        deaths.append(dict(key=key, date=dis))
                    elif r.random() < (.18 if kind in ("res", "biopsy", "liver") else .04):
                        deaths.append(dict(key=key, date=dis + dt.timedelta(days=int(r.integers(5, 1500)))))
    return recs, persons, deaths


def _years(rec):
    return (rec["admit"] - rec["dob"]).days / 365.25


def members(seed, index):
    """The plan's members among the eight hospitals' patients, as the payer fields drew them, with two kinds of stay
    every hospital's claims hold over the three years: a Medicare Advantage stay discharged between 1 January and
    15 May 2024, and a stay long enough to be billed in interim claims. Where a hospital's draw holds neither, one
    patient of the right age whose payer category matches becomes a member (the payer fields only; nothing the call
    reads moves)."""
    win = (dt.date(2024, 1, 1), dt.date(2024, 5, 15))
    for hi, h in enumerate(C.H):
        r = _rng(seed, 8300 + hi)
        recs = sorted((x for x in index if x["hosp"] == h), key=lambda x: (x["discharge"], x["key"]))
        los = lambda x: (x["discharge"] - x["admit"]).days
        inwin = lambda x: win[0] <= x["discharge"] <= win[1]
        if not any(inwin(x) and x["payer"] == K.PLAN and x["payer_cat"] == "2" for x in recs):
            cand = [x for x in recs if inwin(x) and x["payer_cat"] == "1" and _years(x) >= 65 and los(x) <= 21]
            x = cand[int(r.integers(0, len(cand)))]
            x["payer_cat"], x["payer"] = "2", K.PLAN
        if not any(los(x) > 21 and x["payer"] == K.PLAN for x in recs):
            cand = [x for x in recs if los(x) > 21 and x["payer_cat"] in ("1", "5") and x["payer"] != K.PLAN
                    and x["discharge"].month < 12]
            x = cand[int(r.integers(0, len(cand)))]
            x["payer"] = K.PLAN
            x["payer_cat"] = "2" if x["payer_cat"] == "1" else "5"
    return index


def reoperations(seed, brec):
    """A completion pancreatectomy on readmission after a partial resection earlier in 2026, at each of the eight
    hospitals (two at the largest two): the same person, the same hospital, a second resection stay."""
    out = []
    for hi, h in enumerate(C.H):
        r = _rng(seed, 8400 + hi)
        first = [x for x in brec if x["hosp"] == h and x["kind"] == "res" and x["op"] >= dt.date(2026, 1, 1)
                 and x["discharge"] <= dt.date(2026, 5, 8) and not any(c in ("0FTG0ZZ", "0FTG4ZZ") for c, _ in x["px"])]
        first.sort(key=lambda x: (x["discharge"], x["key"]))
        picks = r.choice(len(first), size=2 if h in ("A", "B") else 1, replace=False)
        for i in sorted(int(p) for p in picks):
            x = first[i]
            adm = x["discharge"] + dt.timedelta(days=int(r.integers(5, 26)))
            op = adm + dt.timedelta(days=int(r.integers(0, 3)))
            dis = op + dt.timedelta(days=int(r.integers(7, 15)))
            mal = [c for c, _ in x["dx"] if c.startswith("C")]
            dx = [("K91.89", "Y"), (mal[0], "Y")] if mal else [("K91.89", "Y"), ("K86.89", "Y")]
            dx.append((["K65.1", "K63.1", "K92.2", "T81.43XA"][int(r.integers(0, 4))], "Y"))
            out.append(_record(key=x["key"], hosp=h, admit=adm, discharge=dis, op=op, sex=x["sex"], dob=x["dob"],
                               admit_type="1", admit_source="7", disposition=["01", "06", "03"][int(r.integers(0, 3))],
                               payer_cat=x["payer_cat"], payer=x["payer"], dx=dx,
                               px=[("0FTG0ZZ", op), ("07TP0ZZ", op)], index=False, kind="reop"))
    return out


def world(seed=C.SEED):
    keys = Keys(seed)
    ix = C.core(seed)
    irec, ipers, ideaths, earlier = index_details(seed, ix, keys)
    members(seed, irec)
    brec, bpers, bdeaths = background(seed, keys)
    brec += reoperations(seed, brec)
    deaths = [d for d in ideaths + bdeaths if d["date"] <= K.DEATHS_LINKED]
    return dict(seed=seed, ix=ix, index=irec, earlier=earlier, background=brec, persons=ipers + bpers, deaths=deaths)
