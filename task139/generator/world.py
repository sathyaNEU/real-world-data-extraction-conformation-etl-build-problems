"""The world before any file is written: Haverline's claims from January 2021 to September 2026, the ERN pilot's
draw, assignment and outcomes, the nurses' files, Kellerman Pryce's verification sample, the 2026 indemnity
payments and their bank returns. Every quantity is generated forward from the claims' own latent courses; the files
are rendered from this state by records.py and docs.py.

Each pilot segment's outcome stream is chosen once, by search, as the first stream index whose realised pilot sits
within tolerance of the segment's design economics (the ladder in the design note); nothing is fitted afterwards."""
from __future__ import annotations

import datetime as dt
import math
from dataclasses import dataclass, field

import numpy as np
from scipy.stats import norm

import common as K

# ---- outcome parameters per segment -------------------------------------------------------------------------
# aww: mean average weekly wage; med/sig: lognormal days off work (UH) for intakes not back within the waiting period;
# short: share back within three days under usual handling; saw: share of intakes an ERN nurse keeps at work on
# suitable duties; tau: how steeply that falls with the natural length of the disability; red: ERN's factor on the
# days off of the intakes it does not keep at work; ppd/ppdw: permanent partial disability incidence and weeks;
# kmod: modified-duty length of a kept intake as a share of its natural disability; tpd: temporary partial share.
PARAMS = {
    "HC-SS": dict(aww=780, med=28, sig=0.62, short=0.15, saw=0.25, tau=90, red=0.93, ppd=0.12, ppdw=13, kmod=0.45, tpd=0.06),
    "HC-OT": dict(aww=780, med=46, sig=0.58, short=0.08, saw=0.03, tau=90, red=0.855, ppd=0.26, ppdw=20, kmod=0.55, tpd=0.05),
    "RW-SS": dict(aww=700, med=26, sig=0.62, short=0.16, saw=0.27, tau=90, red=0.93, ppd=0.11, ppdw=12, kmod=0.30, tpd=0.06),
    "RW-OT": dict(aww=730, med=54, sig=0.58, short=0.09, saw=0.03, tau=90, red=0.888, ppd=0.27, ppdw=21, kmod=0.55, tpd=0.05),
    "MF-SS": dict(aww=940, med=28, sig=0.62, short=0.14, saw=0.20, tau=90, red=0.93, ppd=0.13, ppdw=13, kmod=0.45, tpd=0.06),
    "MF-OT": dict(aww=940, med=48, sig=0.58, short=0.08, saw=0.03, tau=90, red=0.87, ppd=0.29, ppdw=21, kmod=0.55, tpd=0.05),
    "CN-SS": dict(aww=1250, med=30, sig=0.62, short=0.12, saw=0.05, tau=90, red=0.95, ppd=0.14, ppdw=14, kmod=0.55, tpd=0.04),
    "CN-OT": dict(aww=1250, med=64, sig=0.58, short=0.06, saw=0.02, tau=90, red=0.885, ppd=0.31, ppdw=24, kmod=0.60, tpd=0.03),
    "TR-SS": dict(aww=980, med=27, sig=0.72, short=0.13, saw=0.0, tau=90, red=1.0, ppd=0.15, ppdw=18, kmod=0.5, tpd=0.04),
    "TR-OT": dict(aww=980, med=50, sig=0.66, short=0.07, saw=0.0, tau=90, red=1.0, ppd=0.33, ppdw=27, kmod=0.5, tpd=0.03),
    "GN-AL": dict(aww=820, med=30, sig=0.80, short=0.14, saw=0.0, tau=90, red=1.0, ppd=0.18, ppdw=20, kmod=0.5, tpd=0.05),
}
# intakes a year at the 2023 level, the growth a year, the share of later indemnity conversions per intake
VOLUME = {"HC-SS": 1500, "HC-OT": 800, "RW-SS": 905, "RW-OT": 750, "MF-SS": 1350, "MF-OT": 770, "CN-SS": 1100,
          "CN-OT": 650, "TR-SS": 520, "TR-OT": 400, "GN-AL": 760}
GROWTH = {"HC": 0.024, "RW": 0.018, "MF": 0.012, "CN": 0.020, "TR": 0.010, "GN": 0.008}
CONV = {"SS": 0.135, "OT": 0.105, "AL": 0.12}
SEASON = {   # January to December
    "HC": [1.03, 0.99, 1.00, 0.98, 0.99, 0.98, 1.00, 1.01, 1.00, 1.01, 0.99, 1.02],
    "RW": [0.97, 0.95, 0.97, 0.98, 0.99, 0.99, 1.00, 1.00, 1.00, 1.02, 1.06, 1.07],
    "MF": [0.99, 0.98, 1.01, 1.01, 1.02, 1.01, 0.97, 1.02, 1.02, 1.01, 0.98, 0.98],
    "CN": [0.90, 0.91, 0.98, 1.03, 1.07, 1.08, 1.06, 1.08, 1.05, 1.02, 0.96, 0.86],
    "TR": [1.02, 1.00, 0.99, 0.98, 0.99, 1.00, 1.00, 1.01, 1.00, 1.00, 1.01, 1.00],
    "GN": [1.01, 1.00, 1.00, 0.99, 1.00, 0.99, 0.98, 1.00, 1.01, 1.01, 1.00, 1.01],
}
WEEKDAY = [1.36, 1.18, 1.12, 1.07, 1.02, 0.17, 0.08]   # Monday to Sunday, reports received
OFFICE_STL = {"HC": 0.62, "RW": 0.47, "MF": 0.55, "CN": 0.57, "TR": 0.44, "GN": 0.60}
# Missouri's maximum weekly rates by the fiscal year of injury (1 July to 30 June)
TTD_MAX = {2020: 1009.43, 2021: 1047.55, 2022: 1099.01, 2023: 1148.04, 2024: 1192.18, 2025: 1231.62, 2026: 1273.10}
PPD_MAX = {2020: 528.62, 2021: 548.62, 2022: 575.37, 2023: 601.06, 2024: 624.17, 2025: 644.82, 2026: 666.53}
REVIEW_N = 100
PILOT_DRAW = 1.0 / 3.0

# design economics each pilot segment's realised stream is held to (per team-year at the golden basis, the default
# basis and the mixed basis; the per-intake saving): the model's own expectation from 80,000 simulated pilot intakes
# a segment (generator/design.py), rounded
DESIGN = {
    "HC-SS": dict(V=288900, Vd=39000, Vic=212500, D=850),
    "HC-OT": dict(V=188900, Vd=161600, Vic=172900, D=1001),
    "RW-SS": dict(V=288800, Vd=32400, Vic=198400, D=731),
    "RW-OT": dict(V=133700, Vd=109200, Vic=120900, D=857),
    "MF-SS": dict(V=283400, Vd=52400, Vic=218500, D=865),
    "MF-OT": dict(V=208000, Vd=174700, Vic=190200, D=1172),
    "CN-SS": dict(V=117600, Vd=56600, Vic=102400, D=436),
    "CN-OT": dict(V=201100, Vd=178600, Vic=188300, D=1569),
}


def fiscal(d):
    return d.year if d.month >= 7 else d.year - 1


@dataclass
class Claim:
    cid: int                       # internal index
    seg: str
    office: str
    klass: str
    injury: dt.date
    report: dt.date
    intake: bool                   # first report records time lost
    dis_began: dt.date | None      # first day of lost time (None: never)
    triage: dt.date | None = None
    pilot: bool = False
    arm: str = ""                  # "E" Early Return Nursing, "U" usual handling (pilot only)
    pref: str = ""                 # pilot reference
    # outcome
    aww: float = 0.0
    days_off: int = 0              # days off work from dis_began
    kept: bool = False
    ttd: float = 0.0
    tpd: float = 0.0
    ppd: float = 0.0
    ttd_rate: float = 0.0
    ttd_days: int = 0
    tpd_weekly: float = 0.0
    tpd_weeks: int = 0
    ppd_rate: float = 0.0
    ppd_award: dt.date | None = None
    ppd_lump: bool = True
    ppd_atty: bool = False
    cadence: int = 7
    eft: bool = False
    first_ind: dt.date | None = None
    closed: dt.date | None = None
    reopened: dt.date | None = None
    # numbering
    legacy_no: str = ""
    claim_no: str = ""
    dup_of: int = -1               # cutover duplicate: the converted copy of claim cid
    native: bool = False           # reported in the parallel run and carried on in the new system
    # nurse file
    files: list = field(default_factory=list)   # [(opened, closed, reason)]

    @property
    def indemnity(self):
        return self.ttd + self.tpd + self.ppd

    @property
    def ind(self):
        return self.indemnity > 0.005


def _lat(rg, n):
    """The latent draws one claim's course is built from (one block per claim, same layout for every stream)."""
    return dict(u=rg.random(n), awwz=rg.normal(0, 1, n), short3=rg.random(n), ppdu=rg.random(n),
                ppdg=rg.gamma(4.0, 1.0, n), tpdu=rg.random(n), tpdw=rg.uniform(2, 8, n), tpdl=rg.uniform(0.2, 0.4, n),
                nE=rg.normal(0, 0.06, n), modn=rg.normal(0, 0.25, n), fcl=rg.integers(0, 4, n),
                sh=rg.integers(1, 6, n), k3=rg.random(n), keep=rg.random(n), lit=rg.random(n), mmi=rg.random(n),
                reo=rg.random(n), reog=rg.integers(5, 41, n), reol=rg.integers(4, 13, n), award=rg.integers(45, 121, n),
                lump=rg.random(n), atty=rg.random(n), cad=rg.random(n), eft=rg.random(n), close=rg.integers(12, 61, n),
                ppdclose=rg.integers(25, 75, n), tpdgap=rg.integers(0, 3, n), firstpay=rg.integers(12, 20, n),
                reopenc=rg.random(n), reopend=rg.integers(30, 300, n))


def _course(seg, claims, L, arms):
    """Each claim's course under its own arm: days off, kept at work, TTD, TPD, PPD, and an ERN file's place-days.
    arms[i] is 'E' or 'U'. Returns the ERN files' place-day lengths (0 for usual handling)."""
    p = K_PARAMS(seg)
    n = len(claims)
    short = L["u"] < p["short"]
    v = np.clip((L["u"] - p["short"]) / (1 - p["short"]), 1e-9, 1 - 1e-9)
    D0 = np.where(short, 1 + np.floor(3 * L["short3"]), np.maximum(4, np.exp(math.log(p["med"]) + p["sig"] * norm.ppf(v))))
    D0 = np.round(D0)
    aww = p["aww"] * np.exp(0.26 * L["awwz"] - 0.034)
    # ERN keeps an intake at work on suitable duties with a chance falling with its natural disability
    w = np.where(short | (D0 > 120), 0.0, np.exp(-D0 / p["tau"]))
    elig = w > 0
    base = p["saw"] / max(1e-9, float(np.mean(np.where(elig, w, 0.0))) if np.any(elig) else 1.0)
    pkeep = np.clip(w * base, 0, 0.95)
    files = np.zeros(n)
    for i, c in enumerate(claims):
        e = arms[i] == "E"
        kept = bool(e and elig[i] and L["keep"][i] < pkeep[i])
        if kept:
            D = int(1 + math.floor(3 * L["k3"][i]))
        elif e and not short[i]:
            D = int(max(4, round(D0[i] * p["red"] * math.exp(L["nE"][i]))))
        else:
            D = int(D0[i])
        if not c.intake:                         # a later conversion is on file because it paid indemnity
            D = max(D, 5)
        c.aww = float(aww[i])
        c.kept = kept
        c.ttd = c.tpd = c.ppd = c.tpd_weekly = c.ppd_rate = 0.0
        c.tpd_weeks = c.ttd_days = 0
        c.days_off = D if c.dis_began is not None else 0
        fy = fiscal(c.injury)
        rate = min(c.aww * 2 / 3, TTD_MAX.get(fy, 1273.10))
        paid = 0 if D <= 3 else (D - 3 if D <= 14 else D)
        c.ttd_rate = round(rate, 2)
        c.ttd_days = paid
        c.ttd = round(c.ttd_rate * paid / 7, 2)
        ppdp = min(0.9, p["ppd"] * (D / p["med"]) ** 0.8)
        if D > 14 and L["ppdu"][i] < ppdp:
            prate = min(c.aww * 2 / 3, PPD_MAX.get(fy, 666.53))
            weeks = max(4.0, round(float(L["ppdg"][i]) * p["ppdw"] / 4.0 * (0.95 if e else 1.0), 1))
            c.ppd_rate = round(prate, 2)
            c.ppd = round(c.ppd_rate * weeks, 2)
        tp = (D > 3 and L["tpdu"][i] < p["tpd"]) or (kept and L["tpdu"][i] < 0.08)
        if tp:
            c.tpd_weeks = int(round(L["tpdw"][i]))
            c.tpd_weekly = round(c.aww * float(L["tpdl"][i]) * 2 / 3, 2)
            c.tpd = round(c.tpd_weekly * c.tpd_weeks, 2)
        if e:
            files[i] = _file_length(c, L, i, p, short[i], D0[i])
    return files


def _file_length(c, L, i, p, short, D0):
    """Place-days the ERN file holds, opened at triage and closed when the worker is back at full duty (inclusive)."""
    if short:
        return int(L["sh"][i])
    if c.kept:
        return int(max(4, round((D0 - 3) * p["kmod"] * math.exp(L["modn"][i]))))
    back = c.dis_began + dt.timedelta(days=c.days_off)
    f = (back - c.triage).days + int(L["fcl"][i]) + 1
    if c.ind and L["lit"][i] < 0.025:            # an attorney appears: the file goes back to the adjuster
        f = min(f, 10 + int(30 * L["lit"][i] / 0.025))
    if c.days_off > 150 and L["mmi"][i] < 0.6:   # closed at maximum medical improvement
        f = min(f, 120 + int(60 * L["mmi"][i]))
    return int(max(1, min(f, 300)))


def K_PARAMS(seg):
    return PARAMS[seg]


@dataclass
class World:
    claims: list
    by_seg: dict
    pilot_ids: list
    review: dict                   # (seg, arm) -> list of claim ids sampled
    payments: list
    returns: list
    stream: dict                   # seg -> chosen pilot stream index
    realised: dict                 # seg -> realised pilot metrics (as the golden reads them)
    survey: list
    counts: dict = field(default_factory=dict)


def _arrivals():
    """Every claim reported 1 January 2021 to 30 September 2026 that recorded time lost at first report or later paid
    indemnity, by segment, with office, class, dates."""
    claims = []
    for seg, legacy, name, ind, cls in K.ALL_SEGMENTS:
        rg = K.rng("arrivals", seg)
        codes, wts = zip(*K.CLASS_CODES[ind])
        wts = np.array(wts) / sum(wts)
        for d in K.daterange(K.EXTRACT_START, K.EXTRACT_END):
            yrs = (d - dt.date(2023, 7, 1)).days / 365.25
            lam = VOLUME[seg] / 365.25 * (1 + GROWTH[ind]) ** yrs * SEASON[ind][d.month - 1] * WEEKDAY[d.weekday()] * 7 / sum(WEEKDAY)
            if d in K.HOLIDAYS:
                lam *= 0.3
            n_in = rg.poisson(lam)
            n_cv = rg.poisson(lam * CONV[cls])
            for k in range(n_in + n_cv):
                intake = k < n_in
                u = rg.random()
                lag = 0 if u < 0.12 else (int(rg.integers(1, 4)) if u < 0.72 else (int(rg.integers(4, 15)) if u < 0.94
                                                                                   else int(rg.integers(15, 91))))
                inj = d - dt.timedelta(days=lag)
                if intake:
                    db = inj + dt.timedelta(days=0 if rg.random() < 0.7 else 1)
                    if db > d:
                        db = d
                else:
                    db = d + dt.timedelta(days=int(3 + rg.gamma(2.0, 9.0)))
                office = "STL" if rg.random() < OFFICE_STL[ind] else "KC"
                klass = str(rg.choice(codes, p=wts))
                claims.append(Claim(cid=len(claims), seg=seg, office=office, klass=klass, injury=inj, report=d,
                                    intake=intake, dis_began=db))
    for c in claims:
        if c.intake:
            c.triage = K.next_working(c.report)
    return claims


def _pilot(claims):
    """The triage screen drew one in three of each day's intakes in the eight segments into the pilot at random and
    assigned each segment's drawn intakes in pairs, in triage order: one of each pair to ERN at random."""
    ids = []
    for seg in K.PROG:
        rg = K.rng("pilot-draw", seg)
        pool = [c for c in claims if c.seg == seg and c.intake and K.PILOT_START <= c.triage <= K.PILOT_END]
        pool.sort(key=lambda c: (c.triage, c.report, c.cid))
        drawn = [c for c in pool if rg.random() < PILOT_DRAW]
        for k in range(0, len(drawn), 2):
            pair = drawn[k:k + 2]
            first_e = rg.random() < 0.5
            for j, c in enumerate(pair):
                c.pilot = True
                c.arm = "E" if (j == 0) == first_e else "U"
                if len(pair) == 1:
                    c.arm = "E" if first_e else "U"
                ids.append(c.cid)
    return ids


def _realise(seg, pclaims, k):
    """Run one candidate stream for a segment's pilot: courses, files, the review's sample, the golden's metrics."""
    rg = K.rng("pilot-course", seg, k)
    L = _lat(rg, len(pclaims))
    arms = [c.arm for c in pclaims]
    flen = _course(seg, pclaims, L, arms)
    files = []
    for i, c in enumerate(pclaims):
        if c.arm != "E":
            continue
        f = int(flen[i])
        opened = c.triage
        closedd = opened + dt.timedelta(days=f - 1)
        rows = [(opened, closedd, f)]
        if L["reo"][i] < 0.012:
            ro = closedd + dt.timedelta(days=int(L["reog"][i]))
            rows.append((ro, ro + dt.timedelta(days=int(L["reol"][i]) - 1), int(L["reol"][i])))
        files.append((c.cid, rows))
    rs = K.rng("review-sample", seg, k)
    sample = {}
    for arm in ("E", "U"):
        frame = sorted([c for c in pclaims if c.arm == arm and c.ind], key=lambda c: c.cid)
        pick = rs.choice(len(frame), size=min(REVIEW_N, len(frame)), replace=False)
        sample[arm] = sorted(frame[j].cid for j in pick)
    by = {c.cid: c for c in pclaims}
    fl = {cid: sum(r[2] for r in rows) for cid, rows in files}
    m = {}
    for arm in ("E", "U"):
        n_int = sum(1 for c in pclaims if c.arm == arm)
        n_ind = sum(1 for c in pclaims if c.arm == arm and c.ind)
        sev = float(np.mean([by[cid].indemnity for cid in sample[arm]]))
        m[arm] = dict(n=n_int, n_ind=n_ind, p=n_ind / n_int, sev=sev)
    e_ids = [c.cid for c in pclaims if c.arm == "E"]
    e_ind = [c.cid for c in pclaims if c.arm == "E" and c.ind]
    L_all = float(np.mean([fl[i] for i in e_ids]))
    L_cl = float(np.mean([fl[i] for i in e_ind]))
    delta = m["U"]["p"] * m["U"]["sev"] - m["E"]["p"] * m["E"]["sev"]
    d = m["U"]["sev"] - m["E"]["sev"]
    met = dict(nU=m["U"]["n"], nE=m["E"]["n"], indU=m["U"]["n_ind"], indE=m["E"]["n_ind"], pU=m["U"]["p"],
               pE=m["E"]["p"], sevU=m["U"]["sev"], sevE=m["E"]["sev"], L_all=L_all, L_cl=L_cl, delta=delta, d=d,
               V=K.TEAM_PLACE_DAYS * delta / L_all, Vd=K.TEAM_PLACE_DAYS * d / L_cl, Vic=K.TEAM_PLACE_DAYS * delta / L_cl)
    return L, files, sample, met


def _accept(seg, met):
    """A candidate stream is kept when its realised pilot sits near the segment's design economics, the per-claim
    saving stays positive, and each graded per-team saving sits clear of its rounding edge."""
    t = DESIGN[seg]
    ok = abs(met["V"] / t["V"] - 1) < 0.03 and abs(met["Vic"] / t["Vic"] - 1) < 0.04 and abs(met["delta"] / t["D"] - 1) < 0.04
    ok = ok and met["d"] > 0 and abs(met["Vd"] - t["Vd"]) < max(0.15 * t["Vd"], 9000)
    ok = ok and K.edge_distance(met["V"], 10000) > 1800
    return ok


def _outcomes_other(claims, pilot_set):
    """Courses for every claim outside the pilot (usual handling), one stream per segment."""
    for seg, *_ in K.ALL_SEGMENTS:
        cs = [c for c in claims if c.seg == seg and c.cid not in pilot_set]
        rg = K.rng("course", seg)
        L = _lat(rg, len(cs))
        _course(seg, cs, L, ["U"] * len(cs))
        _dates(cs, L)


def _dates(cs, L):
    """Payment cadence and method, the first indemnity date, the PPD award, closing and reopening."""
    for i, c in enumerate(cs):
        c.cadence = 7 if L["cad"][i] < 0.55 else 14
        c.eft = bool(L["eft"][i] < 0.6)
        back = (c.dis_began + dt.timedelta(days=c.days_off)) if c.dis_began is not None else c.report
        firsts = []
        if c.ttd > 0:
            firsts.append(max(c.dis_began + dt.timedelta(days=int(L["firstpay"][i])), c.report + dt.timedelta(days=5)))
        if c.tpd > 0:
            firsts.append(back + dt.timedelta(days=14 + int(L["tpdgap"][i])))
        if c.ppd > 0:
            c.ppd_award = back + dt.timedelta(days=int(L["award"][i]))
            c.ppd_lump = bool(L["lump"][i] < 0.6)
            c.ppd_atty = bool(c.ppd_lump and L["atty"][i] < 0.45)
            firsts.append(c.ppd_award + dt.timedelta(days=3))
        c.first_ind = min(firsts) if firsts else None
        last = back
        if c.tpd > 0:
            last = max(last, back + dt.timedelta(days=7 * c.tpd_weeks + 14))
        if c.ppd > 0:
            if c.ppd_lump:
                last = max(last, c.ppd_award + dt.timedelta(days=int(L["ppdclose"][i])))
            else:
                weeks = c.ppd / max(c.ppd_rate, 1.0)
                last = max(last, c.ppd_award + dt.timedelta(days=int(7 * weeks) + int(L["ppdclose"][i])))
        c.closed = last + dt.timedelta(days=int(L["close"][i]))
        if c.closed <= K.PULL_DATE and L["reopenc"][i] < 0.018:
            ro = c.closed + dt.timedelta(days=int(L["reopend"][i]))
            if ro <= K.PULL_DATE:
                c.reopened = ro


def _numbers(claims):
    """Legacy numbers (office letter, year, sequence) for claims reported before the upgrade; new numbers for all,
    converted claims first in legacy order, then claims keyed on the new system in report order."""
    seq = {}
    old = sorted([c for c in claims if c.report < K.UPGRADE and not c.native and c.dup_of < 0], key=lambda c: (c.report, c.cid))
    for c in old:
        key = (c.office[0], c.report.year)
        seq[key] = seq.get(key, 0) + 1 + (1 if K.rng("legacy-gap", c.cid).random() < 0.04 else 0)
        c.legacy_no = "%s%02d-%06d" % ("S" if c.office == "STL" else "K", c.report.year % 100, seq[key])
    n = 10000000
    for c in old:
        n += 1
        c.claim_no = "WC%d" % n
    n2 = 20000000
    new = sorted([c for c in claims if (c.report >= K.UPGRADE or c.native) and c.dup_of < 0], key=lambda c: (c.report, c.cid))
    for c in new:
        n2 += 1 + (1 if K.rng("new-gap", c.cid).random() < 0.03 else 0)
        c.claim_no = "WC%d" % n2


def _cutover_duplicates(claims):
    """First reports received 29 May to 1 June 2025 were keyed in both systems: the legacy copy was converted with the
    rest, the new-system copy carried on. The converted copy closed with no activity."""
    dups = []
    a, b = K.PARALLEL
    rg = K.rng("cutover")
    for c in [c for c in claims if a <= c.report <= b]:
        if rg.random() < 0.93:
            d = Claim(cid=len(claims) + len(dups), seg=c.seg, office=c.office, klass=c.klass, injury=c.injury,
                      report=c.report, intake=c.intake, dis_began=c.dis_began, triage=c.triage)
            d.dup_of = c.cid
            d.closed = c.report + dt.timedelta(days=int(rg.integers(16, 30)))
            c.native = True
            dups.append(d)
    return dups


def intakes_window(claims, seg, a, b):
    """True intakes (first report records time lost) reported a to b, the cutover's converted copies left out."""
    return sum(1 for c in claims if c.seg == seg and c.intake and c.dup_of < 0 and a <= c.report <= b)


def allocate(value, cap):
    """Seventeen teams, at most three a unit and no more than a unit's intakes keep in use, to the highest value per
    team-year first."""
    order = sorted(K.PROG, key=lambda s: (-value[s], s))
    teams, left = {s: 0 for s in K.PROG}, K.TEAMS
    for s in order:
        t = min(K.MAX_TEAMS, cap[s], left)
        teams[s] = t
        left -= t
    return teams


def golden_of(realised, claims):
    v12 = {s: intakes_window(claims, s, dt.date(2025, 10, 1), K.EXTRACT_END) for s in K.PROG}
    cap = {s: min(K.MAX_TEAMS, int(v12[s] * realised[s]["L_all"] / K.TEAM_PLACE_DAYS)) for s in K.PROG}
    value = {s: realised[s]["V"] for s in K.PROG}
    teams = allocate(value, cap)
    total = sum(teams[s] * value[s] for s in K.PROG)
    return teams, total, cap


def _total_ok(total):
    """The booked credit sits well inside its 100,000 bin and does not land on a half-million."""
    r = K.round_to(total, 100000)
    return K.edge_distance(total, 100000) > 20000 and r % 500000 != 0


# the payment register's stream (check-number gaps, ACH returns, voids): the first whose segment totals each sit at
# least 150 dollars from a rounding edge at the nearest 1,000 (search.py)
PAY_STREAM = 30

# each pilot segment's outcome stream: the first stream index whose realised pilot _accept()s, then advanced one
# segment at a time, in a fixed order, until the booked credit sits clear of its rounding edge (search.py)
STREAMS = {"HC-SS": 171, "HC-OT": 179, "RW-SS": 552, "RW-OT": 401, "MF-SS": 173, "MF-OT": 135, "CN-SS": 854, "CN-OT": 285}


def search_streams(claims, pcs_of, quiet=True):
    found = {}

    def next_stream(seg, start):
        for k in range(start, start + 8000):
            met = _realise(seg, pcs_of[seg], k)[3]
            if _accept(seg, met):
                return k, met
        raise SystemExit("no stream for %s" % seg)

    for seg in K.PROG:
        found[seg] = next_stream(seg, 0)
    order = ["HC-OT", "CN-OT", "MF-OT", "HC-SS", "MF-SS", "RW-SS", "RW-OT", "CN-SS"]
    step = 0
    while not _total_ok(golden_of({s: found[s][1] for s in K.PROG}, claims)[1]):
        seg = order[step % len(order)]
        found[seg] = next_stream(seg, found[seg][0] + 1)
        step += 1
        if step > 64:
            raise SystemExit("no total clear of its edge")
    return {s: found[s][0] for s in K.PROG}


def simulate(streams=None):
    claims = _arrivals()
    pilot_ids = _pilot(claims)
    pilot_set = set(pilot_ids)
    pcs_of = {seg: sorted([claims[i] for i in pilot_ids if claims[i].seg == seg], key=lambda c: c.cid) for seg in K.PROG}
    streams = streams or STREAMS or search_streams(claims, pcs_of)
    realised, review, nurse_files = {}, {}, {}
    for seg in K.PROG:
        L, files, sample, met = _realise(seg, pcs_of[seg], streams[seg])
        assert _accept(seg, met), (seg, streams[seg])
        realised[seg] = met
        review[(seg, "E")] = sample["E"]
        review[(seg, "U")] = sample["U"]
        _dates(pcs_of[seg], L)
        for cid, rows in files:
            nurse_files[cid] = rows
    assert _total_ok(golden_of(realised, claims)[1])
    _outcomes_other(claims, pilot_set)
    for cid, rows in nurse_files.items():
        claims[cid].files = rows
    dups = _cutover_duplicates(claims)
    _numbers(claims)
    claims.extend(dups)
    _number_dups(claims, dups)
    by_seg = {}
    for c in claims:
        by_seg.setdefault(c.seg, []).append(c.cid)
    import payments as PAY
    pays, rets = PAY.payments(claims, PAY_STREAM)
    assert PAY.clear(pays), PAY_STREAM
    survey = _survey(claims)
    return World(claims=claims, by_seg=by_seg, pilot_ids=pilot_ids, review=review, payments=pays, returns=rets,
                 stream=dict(streams), realised=realised, survey=survey)


def _number_dups(claims, dups):
    """The converted copies take legacy numbers in the legacy system's late-May sequence and new numbers among the
    converted claims (after the last converted number)."""
    last = max(int(c.claim_no[2:]) for c in claims if c.claim_no.startswith("WC1"))
    seqs = {}
    for c in claims:
        if c.legacy_no and c.dup_of < 0 and c.report.year == 2025:
            key = c.legacy_no[0]
            seqs[key] = max(seqs.get(key, 0), int(c.legacy_no[-6:]))
    for d in sorted(dups, key=lambda x: (x.report, x.cid)):
        key = "S" if d.office == "STL" else "K"
        seqs[key] = seqs.get(key, 0) + 1
        d.legacy_no = "%s25-%06d" % (key, seqs[key])
        last += 1
        d.claim_no = "WC%d" % last


def _survey(claims):
    """ERN pilot workers' satisfaction survey (sent at file closure; about half answered)."""
    rg = K.rng("survey")
    out = []
    for c in sorted([c for c in claims if c.pilot and c.arm == "E"], key=lambda c: c.files[0][1] if c.files else c.report):
        if not c.files or rg.random() > 0.52:
            continue
        sent = c.files[-1][1] + dt.timedelta(days=int(rg.integers(1, 6)))
        if sent > dt.date(2025, 8, 1):
            continue
        back = sent + dt.timedelta(days=int(rg.integers(2, 25)))
        sc = lambda m: int(min(5, max(1, round(rg.normal(m, 0.8)))))
        out.append(dict(cid=c.cid, sent=sent, back=back, q1=sc(4.3), q2=sc(4.1), q3=sc(3.9), q4=sc(4.2),
                        rtw=str(rg.choice(["Yes", "Yes", "Yes", "Partly", "No"]))))
    return out
