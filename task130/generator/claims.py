"""The claims world: every medical incident that brought a claim against a Corvane clinician from January 2012 to
September 2026, by the route it came in on, the claim numbers risk management opened for it, what each cost, the
precautionary notices sent to the carriers, and the carriers' own records of the same matters.

Incidents arise month by month from each clinician position's paid FTE. Since September 2015 a patient harmed by care
can ask for compensation through the Early Resolution Program: those requests come a few months after the incident
and mostly settle small; a request that is declined can turn into a suit, which risk management opens as a new claim
number pointing back at the request. Demand letters and suits that come in directly arrive a year or more after the
incident and carry the defence costs and the large indemnity payments."""
from __future__ import annotations

import datetime as dt
import math
from dataclasses import dataclass, field

import numpy as np

import common as K
import world as WD

F_DIRECT = {"OB": 0.070, "SUR": 0.045, "EM": 0.031, "AN": 0.024, "HM": 0.016, "PC": 0.011, "APC": 0.006}
F_ERP = {"OB": 0.084, "SUR": 0.062, "EM": 0.051, "AN": 0.036, "HM": 0.027, "PC": 0.020, "APC": 0.011}
F_RESIDENT = 0.012
ESCALATE = 0.065
DIVERT = 0.75             # direct demands and suits at the Program's hospitals, against the Stoneleigh entities
ERP_LAG_MEDIAN = {"OB": 96, "SUR": 90, "EM": 84, "AN": 86, "HM": 90, "PC": 88, "APC": 86}
ERP_LAG_SIGMA = 0.50
DIRECT_LAG_MEDIAN = {"OB": 800, "SUR": 520, "EM": 470, "AN": 500, "HM": 520, "PC": 560, "APC": 500}
DIRECT_LAG_SIGMA = 0.55
ERP_IND = {"OB": 32000, "SUR": 22000, "EM": 14000, "AN": 15000, "HM": 14000, "PC": 10000, "APC": 8500}
SUIT_IND = {"OB": 500000, "SUR": 290000, "EM": 230000, "AN": 250000, "HM": 230000, "PC": 175000, "APC": 150000}
DIRECT_IND = {"OB": 620000, "SUR": 310000, "EM": 250000, "AN": 270000, "HM": 250000, "PC": 190000, "APC": 155000}
CAP_2020 = 1_200_000

ALLEGATIONS = {
    "OB": ["Birth injury", "Delay in delivery", "Failure to monitor fetal status", "Postpartum hemorrhage management",
           "Surgical complication", "Delay in diagnosis"],
    "SUR": ["Surgical complication", "Improper performance of procedure", "Retained foreign object",
            "Wrong-site procedure", "Post-operative infection", "Failure to monitor", "Delay in diagnosis"],
    "EM": ["Failure to diagnose", "Delay in diagnosis", "Improper discharge", "Medication error", "Failure to monitor"],
    "AN": ["Anesthesia complication", "Airway injury", "Dental injury during intubation", "Positioning injury",
           "Medication error"],
    "HM": ["Delay in diagnosis", "Medication error", "Failure to monitor", "Procedure complication",
           "Failure to treat", "Fall with injury"],
    "PC": ["Delay in diagnosis", "Failure to diagnose", "Medication error", "Failure to refer", "Communication/consent"],
    "APC": ["Medication error", "Delay in diagnosis", "Procedure complication", "Failure to monitor",
            "Communication/consent", "Anesthesia complication"],
}
SPECIALTY_TEXT = {
    "OBG": ["Obstetrics/Gynecology", "OB/GYN"], "OBL": ["OB Hospitalist", "Obstetrics - Laborist"],
    "MFM": ["Maternal-Fetal Medicine"], "GSU": ["General Surgery"], "ORT": ["Orthopaedic Surgery", "Orthopedics"],
    "URO": ["Urology"], "ENT": ["Otolaryngology", "ENT"], "VAS": ["Vascular Surgery"],
    "EMR": ["Emergency Medicine"], "ANE": ["Anesthesiology"], "HOS": ["Hospital Medicine", "Hospitalist"],
    "CCM": ["Critical Care", "Pulm/Critical Care"], "CAR": ["Cardiology"], "GAS": ["Gastroenterology", "GI"],
    "ONC": ["Hematology/Oncology", "Oncology"], "NEU": ["Neurology"], "RAD": ["Radiology", "Diagnostic Radiology"],
    "PSY": ["Psychiatry"], "FAM": ["Family Medicine", "Family Practice"], "INT": ["Internal Medicine"],
    "PED": ["Pediatrics"], "NP": ["Nurse Practitioner", "NP"], "PA": ["Physician Assistant", "PA-C"],
    "CRNA": ["CRNA", "Nurse Anesthetist"], "CNM": ["Nurse Midwife", "CNM"], "RES": ["Resident"],
    "FEL": ["Fellow"], "CTR": ["Radiology (contracted)", "Hospitalist (locum)", "Emergency Medicine (locum)",
                               "Anesthesiology (contracted)"],
}
RELATED = {
    "OBG": ["CNM", "ANE", "OBL"], "OBL": ["OBG", "CNM", "ANE"], "MFM": ["OBG", "OBL"],
    "GSU": ["ANE", "CRNA", "PA"], "ORT": ["ANE", "CRNA", "PA"], "URO": ["ANE", "CRNA"], "ENT": ["ANE", "CRNA"],
    "VAS": ["ANE", "CRNA", "PA"], "EMR": ["HOS", "NP", "PA", "RAD"], "ANE": ["CRNA", "GSU", "ORT"],
    "HOS": ["NP", "PA", "RAD", "CCM"], "CCM": ["HOS", "NP"], "CAR": ["NP", "HOS"], "GAS": ["ANE", "CRNA"],
    "ONC": ["NP", "PA"], "NEU": ["NP", "HOS"], "RAD": ["EMR", "HOS"], "PSY": ["NP"], "FAM": ["NP", "PA"],
    "INT": ["NP", "PA"], "PED": ["NP"], "NP": ["FAM", "INT", "HOS"], "PA": ["ORT", "GSU", "FAM"],
    "CRNA": ["ANE"], "CNM": ["OBG", "OBL"],
}


@dataclass
class Defendant:
    clinician_id: str
    job: str                 # payroll job key, or CTR for contracted
    role: str
    line: str                # coverage line
    share: float             # share of the claim number's amounts (0 for contracted rows)
    specialty: str


@dataclass
class ClaimNo:
    made: dt.date
    matter_type: str
    defendants: list
    indemnity: float         # ultimate, nominal
    defense: float
    close: dt.date
    prior: "ClaimNo | None" = None
    reopen: dt.date | None = None
    reopen_reserve: float = 0.0
    claim_no: str = ""
    report: dt.date | None = None    # reported to the carrier
    v: dict = field(default_factory=dict)   # amounts at valuation (filled in valuation())
    cap: float = 0.0                 # the policy limit at the incident's cost level (adjusters reserve within it)


@dataclass
class Incident:
    date: dt.date
    entity: str
    cls: str | None          # class of the first covered clinician (None: no covered clinician)
    route: str               # ERP, DIRECT
    claims: list
    allegation: str
    notice: dt.date | None = None
    incident_no: str = ""
    notice_no: str = ""
    rm_opened: dt.date | None = None
    seed_tag: str = ""


def bday(d):
    """Risk management logs receipts, closings and notices on business days: a weekend date moves to Monday."""
    wd = d.weekday()
    return d + dt.timedelta(days=(7 - wd)) if wd >= 5 else d


def clinic_day(d):
    """The medical group's clinics and surgery centre see patients on weekdays: Saturday is Friday, Sunday Monday."""
    wd = d.weekday()
    return d - dt.timedelta(days=1) if wd == 5 else (d + dt.timedelta(days=1) if wd == 6 else d)


def _lognormal(rng, median, sigma):
    return float(median * math.exp(sigma * rng.standard_normal()))


def _day_in(rng, p, y, m):
    dim = K.days_in_month(y, m)
    a = max(p.start, dt.date(y, m, 1))
    b = min(p.end, dt.date(y, m, dim)) if p.end is not None else dt.date(y, m, dim)
    return a + dt.timedelta(days=int(rng.integers(0, (b - a).days + 1)))


def _active(index, entity, jobs, d):
    out = []
    for j in jobs:
        for p in index.get((entity, j), ()):
            if p.start <= d and (p.end is None or p.end >= d) and (d.year, d.month) not in p.leave:
                out.append(p)
    return out


def _role(job):
    if job in ("NP", "PA", "CRNA", "CNM"):
        return "Advanced practice clinician"
    if job == "RES":
        return "Resident physician"
    if job == "FEL":
        return "Clinical fellow"
    return "Attending physician"


def _spec(rng, job):
    opts = SPECIALTY_TEXT[job]
    return opts[0] if len(opts) == 1 or rng.random() < 0.75 else opts[1]


def _shares(rng, n):
    if n == 1:
        return [1.0]
    base = [(0.7, 0.3), (0.6, 0.4), (0.8, 0.2), (0.75, 0.25)][int(rng.integers(0, 4))]
    if n == 2:
        return list(base)
    return [base[0] - 0.1, base[1], 0.1]


def _cost_level(year):
    return (1 + K.TREND) ** (year - 2020)


def simulate(W):
    """Every incident with a claim from January 2012 to September 2026 (claims made after the valuation date are
    kept: they are the incidents' futures, never written to the register)."""
    rng = K.claims_stream("incidents")
    index = {}
    for p in W.positions:
        index.setdefault((p.entity, p.job), []).append(p)
    for v in index.values():
        v.sort(key=lambda p: p.pid)
    incidents = []
    pm = WD.position_months(W, K.WORLD_FIRST, K.HCM_LAST)
    erp_start = K.ERP_START
    for (p, y, m, f) in pm:
        cls = K.CLASS_OF_JOB[p.job]
        if f <= 0:
            continue
        if cls is None:
            if p.job == "RES" or p.job == "FEL":
                n = rng.poisson(f * F_RESIDENT / 12.0)
                for _ in range(int(n)):
                    incidents.append(_resident_incident(rng, index, p, y, m))
            continue
        d0 = dt.date(y, m, 1)
        # the Program has met the Quillan hospitals' patients since September 2015 and resolves some of the matters
        # that would otherwise have come in later as demands or suits; Stoneleigh adjusts its insureds' claims itself
        program = p.entity in K.ERP_ENTITIES and d0 >= dt.date(erp_start.year, erp_start.month, 1)
        lam_d = f * F_DIRECT[cls] / 12.0 * (DIVERT if program else 1.0)
        lam_e = f * F_ERP[cls] / 12.0 if program else 0.0
        nd, ne = rng.poisson(lam_d), rng.poisson(lam_e)
        for route, n in (("DIRECT", nd), ("ERP", ne)):
            for _ in range(int(n)):
                d = _day_in(rng, p, y, m)
                if p.entity == "CMG":
                    d2 = clinic_day(d)
                    if p.start <= d2 and (p.end is None or d2 <= p.end) and (d2.year, d2.month) not in p.leave:
                        d = d2
                if route == "ERP" and d < erp_start:
                    route_i = "DIRECT"
                else:
                    route_i = route
                incidents.append(_covered_incident(rng, index, p, cls, d, route_i))
    # claims naming only contracted clinicians (locums, teleradiology, contracted anesthesia)
    rc = K.claims_stream("contracted")
    for (y, m) in K.months(K.WORLD_FIRST, K.HCM_LAST):
        for e, rate in (("TFH", 1.2), ("AMC", 1.4), ("BCH", 0.8)):
            if e == "BCH" and dt.date(y, m, 1) < K.ENTITIES["BCH"]["joined"]:
                continue
            for _ in range(int(rc.poisson(rate / 12.0))):
                d = dt.date(y, m, int(rc.integers(1, K.days_in_month(y, m) + 1)))
                incidents.append(_contracted_incident(rc, e, d))
    incidents.sort(key=lambda i: (i.date, i.entity, i.claims[0].made))
    _carrier_timing(incidents)
    notice_only = _notice_only(W)
    gl = _gl_matters()
    _dup_incidents(incidents)
    _numbering(incidents, notice_only, gl)
    return incidents, notice_only, gl


def _codefendants(rng, index, p, d, erp):
    out = []
    if rng.random() < (0.09 if erp else 0.18):
        rel = RELATED.get(p.job, [])
        cands = [q for q in _active(index, p.entity, rel, d) if q.emp != p.emp]
        if cands:
            q = cands[int(rng.integers(0, len(cands)))]
            out.append(q)
    return out


def _covered_incident(rng, index, p, cls, d, route):
    co = _codefendants(rng, index, p, d, route == "ERP")
    defendants = [(p.emp, p.job)] + [(q.emp, q.job) for q in co]
    res_p = 0.0
    if p.entity == "AMC" and cls in ("OB", "SUR", "EM", "HM", "AN"):
        res_p = 0.12
    elif p.entity == "TFH" and cls in ("OB", "EM", "HM") and d >= dt.date(2018, 7, 1):
        res_p = 0.08
    if rng.random() < res_p * (0.5 if route == "ERP" else 1.0):
        res = _active(index, p.entity, ["RES"] if cls != "HM" or rng.random() < 0.7 else ["FEL", "RES"], d)
        if res:
            r = res[int(rng.integers(0, len(res)))]
            defendants.append((r.emp, r.job))
    ctr = rng.random() < 0.03 and route == "DIRECT"
    allegation = ALLEGATIONS[cls][int(rng.integers(0, len(ALLEGATIONS[cls])))]
    inc = Incident(d, p.entity, cls, route, [], allegation)
    _claims_for(rng, inc, defendants, cls, ctr)
    return inc


def _resident_incident(rng, index, p, y, m):
    d = _day_in(rng, p, y, m)
    defendants = [(p.emp, p.job)]
    cls = None
    if rng.random() < 0.7:
        jobs = ["HOS", "EMR", "OBG", "GSU", "FAM"] if p.entity == "AMC" else ["HOS", "EMR", "OBG"]
        cands = _active(index, p.entity, jobs, d)
        if cands:
            q = cands[int(rng.integers(0, len(cands)))]
            defendants.append((q.emp, q.job))
            cls = K.CLASS_OF_JOB[q.job]
    route = "DIRECT" if d < K.ERP_START or rng.random() < 0.55 else "ERP"
    al_cls = cls or "HM"
    inc = Incident(d, p.entity, cls, route, [], ALLEGATIONS[al_cls][int(rng.integers(0, len(ALLEGATIONS[al_cls])))])
    _claims_for(rng, inc, defendants, al_cls, False)
    return inc


CONTRACTED_GROUPS = [("Radiology (contracted)", ["Failure to diagnose", "Delay in diagnosis"]),
                     ("Hospitalist (locum)", ["Delay in diagnosis", "Medication error", "Failure to monitor"]),
                     ("Emergency Medicine (locum)", ["Failure to diagnose", "Improper discharge"]),
                     ("Anesthesiology (contracted)", ["Anesthesia complication", "Airway injury"])]


def _contracted_incident(rng, e, d):
    """A claim naming only clinicians engaged by contract: one, or two from the same group."""
    spec, allegations = CONTRACTED_GROUPS[int(rng.integers(0, len(CONTRACTED_GROUPS)))]
    n = 1 if rng.random() < 0.75 else 2
    ids = sorted({"CTR-%04d" % int(rng.integers(100, 990)) for _ in range(n)})
    inc = Incident(d, e, None, "DIRECT", [], allegations[int(rng.integers(0, len(allegations)))])
    lag = int(min(3200, max(45, round(_lognormal(rng, 520, DIRECT_LAG_SIGMA)))))
    made = bday(d + dt.timedelta(days=lag))
    suit = rng.random() < 0.55
    defs = [Defendant(c, "CTR", "Contracted physician", "CONTRACT", 0.0, spec) for c in ids]
    close = bday(made + dt.timedelta(days=int(rng.integers(480, 1601) if suit else rng.integers(150, 901))))
    inc.claims = [ClaimNo(made, "Suit" if suit else "Claim", defs, 0.0, 0.0, close)]
    return inc


def _defs(rng, entity, defendants, ctr):
    line = K.ENTITIES[entity]["line"]
    paying = [(c, j) for c, j in defendants if j != "CTR"]
    shares = _shares(rng, len(paying)) if paying else []
    out, k = [], 0
    for c, j in defendants:
        if j == "CTR":
            out.append(Defendant(c, "CTR", "Contracted physician", "CONTRACT", 0.0, _spec(rng, "CTR")))
        else:
            out.append(Defendant(c, j, _role(j), line, shares[k], _spec(rng, j)))
            k += 1
    if ctr:
        out.append(Defendant("CTR-%04d" % int(rng.integers(100, 990)), "CTR", "Contracted physician", "CONTRACT", 0.0,
                             _spec(rng, "CTR")))
    return out


def _cap(ind, dfn, level):
    cap = CAP_2020 * level
    if ind + dfn > cap:
        ind = max(0.0, cap - dfn)
    return ind, dfn


def _claims_for(rng, inc, defendants, cls, ctr):
    level = _cost_level(inc.date.year) * float(np.exp(0.04 * rng.standard_normal()))
    defs = _defs(rng, inc.entity, defendants, ctr)
    cap = CAP_2020 * level
    if inc.route == "ERP":
        lag = int(min(330, max(12, round(_lognormal(rng, ERP_LAG_MEDIAN[cls], ERP_LAG_SIGMA)))))
        made = bday(inc.date + dt.timedelta(days=lag))
        if rng.random() < ESCALATE:
            req_close = bday(made + dt.timedelta(days=int(rng.integers(30, 151))))
            req = ClaimNo(made, "Claim", defs, 0.0, _lognormal(rng, 1600, 0.6) * level, req_close)
            suit_made = bday(made + dt.timedelta(days=int(rng.integers(180, 601))))
            sdefs = [Defendant(d.clinician_id, d.job, d.role, d.line, d.share, d.specialty) for d in defs]
            if rng.random() < 0.62:
                ind = _lognormal(rng, SUIT_IND[cls], 0.6) * level
                dfn = _lognormal(rng, 90000, 0.5) * level
            else:
                ind, dfn = 0.0, _lognormal(rng, 65000, 0.6) * level
            ind, dfn = _cap(ind, dfn, level)
            suit = ClaimNo(suit_made, "Suit", sdefs, ind, dfn,
                           bday(suit_made + dt.timedelta(days=int(rng.integers(420, 1501)))), prior=req)
            inc.claims = [req, suit]
        else:
            ind = 0.0 if rng.random() < 0.24 else min(250000 * level, _lognormal(rng, ERP_IND[cls], 0.85) * level)
            dfn = _lognormal(rng, 1600, 0.6) * level
            inc.claims = [ClaimNo(made, "Claim", defs, ind, dfn, bday(made + dt.timedelta(days=int(rng.integers(20, 161)))))]
    else:
        lag = int(min(3200, max(45, round(_lognormal(rng, DIRECT_LAG_MEDIAN[cls], DIRECT_LAG_SIGMA)))))
        made = bday(inc.date + dt.timedelta(days=lag))
        suit = rng.random() < 0.55
        if rng.random() < 0.40:
            ind = _lognormal(rng, DIRECT_IND[cls], 0.7) * level
            dfn = _lognormal(rng, 95000, 0.5) * level
        else:
            ind = 0.0
            dfn = _lognormal(rng, 40000 if suit else 12000, 0.65) * level
        ind, dfn = _cap(ind, dfn, level)
        close = bday(made + dt.timedelta(days=int(rng.integers(480, 1601) if suit else rng.integers(150, 901))))
        c = ClaimNo(made, "Suit" if suit else "Claim", defs, ind, dfn, close)
        if rng.random() < 0.03:
            c.reopen = bday(close + dt.timedelta(days=int(rng.integers(60, 501))))
            c.reopen_reserve = float(rng.choice([5000, 10000, 15000, 25000, 40000]))
        inc.claims = [c]
    for c in inc.claims:
        c.cap = cap
    # a precautionary notice to the carrier for serious events, sent before any claim
    p_notice = 0.35 if inc.route == "DIRECT" else 0.05
    if inc.cls is not None or any(d.line != "CONTRACT" for d in defs):
        if rng.random() < p_notice:
            nd = bday(inc.date + dt.timedelta(days=int(rng.integers(4, 81))))
            if nd < inc.claims[0].made:
                inc.notice = nd


GAP_FIRST = dt.date(2026, 9, 24)     # claims received from this Thursday go in the 2 October carrier report


def carrier_report_date(made):
    """Claims received by risk management through Wednesday go to the carriers in that week's Friday report."""
    wd = made.weekday()
    return made + dt.timedelta(days=(4 - wd) if wd <= 2 else (11 - wd))


def _open_at(c, V):
    if c.made > V:
        return False
    if c.close > V:
        return True
    return c.reopen is not None and c.reopen <= V


def _carrier_timing(incidents):
    """When each matter reaches its carrier, and the constructed facts the carrier reconciliation rests on: no
    escalated suit and no noticed matter is first made in the last week of September 2026, two requests handled in
    house in 2026 never reached the carrier, and each entity has open matters that began as precautionary notices."""
    rng = K.claims_stream("carrier-timing")
    V = K.VALUATION
    for inc in incidents:
        for c in inc.claims:
            if c.prior is not None and GAP_FIRST <= c.made <= V:
                c.made = bday(V + dt.timedelta(days=int(rng.integers(5, 20))))
            c.report = carrier_report_date(c.made)
        if inc.notice is not None and GAP_FIRST <= inc.claims[0].made <= V:
            inc.notice = None
        inc.unreported = False
    on_line = lambda inc: any(d.line != "CONTRACT" for d in inc.claims[0].defendants)
    # two Early Resolution Program requests from 2026 that were settled in house and never reported
    cands = [inc for inc in incidents if inc.route == "ERP" and on_line(inc) and inc.entity in ("AMC", "TFH")
             and len(inc.claims) == 1 and dt.date(2026, 3, 1) <= inc.claims[0].made <= dt.date(2026, 8, 31)
             and _open_at(inc.claims[0], V) and inc.notice is None]
    for e in ("AMC", "TFH"):
        ce = [inc for inc in cands if inc.entity == e]
        if ce:
            pick = ce[int(rng.integers(0, len(ce)))]
            pick.unreported = True
            for c in pick.claims:
                c.report = None
    # each entity has at least two open matters that began as precautionary notices
    for e in K.ENTITY_ORDER:
        opened = [inc for inc in incidents if inc.entity == e and on_line(inc) and inc.route == "DIRECT"
                  and any(_open_at(c, V) for c in inc.claims) and inc.claims[0].made < GAP_FIRST]
        have = [inc for inc in opened if inc.notice is not None]
        rest = [inc for inc in opened if inc.notice is None]
        while len(have) < 2 and rest:
            inc = rest.pop(int(rng.integers(0, len(rest))))
            nd = bday(inc.date + dt.timedelta(days=int(rng.integers(4, 61))))
            if nd < inc.claims[0].made:
                inc.notice = nd
                have.append(inc)


def _notice_only(W):
    """Precautionary notices for serious events that never became claims: risk management notifies the carrier and
    the matter stays an incident on the carrier's records."""
    rng = K.claims_stream("notice-only")
    rate = {"AMC": 1.5, "TFH": 0.6, "CMG": 1.0, "BCH": 0.35}
    out = []
    for (y, m) in K.months(K.WORLD_FIRST, K.HCM_LAST):
        for e in K.ENTITY_ORDER:
            if K.ENTITIES[e]["joined"] and dt.date(y, m, 1) < K.ENTITIES[e]["joined"]:
                continue
            for _ in range(int(rng.poisson(rate[e]))):
                d = dt.date(y, m, int(rng.integers(1, K.days_in_month(y, m) + 1)))
                if e == "CMG":
                    d = clinic_day(d)
                nd = bday(d + dt.timedelta(days=int(rng.integers(3, 61))))
                if nd > K.VALUATION:
                    continue
                cls = ["OB", "SUR", "EM", "AN", "HM", "PC", "APC"][int(rng.integers(0, 7))]
                inc = Incident(d, e, None, "NOTICE", [], ALLEGATIONS[cls][int(rng.integers(0, len(ALLEGATIONS[cls])))],
                               notice=nd)
                inc.unreported = False
                out.append(inc)
    return out


GL_RATE = {"TFH": 1.3, "AMC": 2.6, "CMG": 0.9, "BCH": 0.9}     # claims against an entity alone, a year
GL_ALLEGATIONS = {
    "hosp": ["Fall with injury", "Medication error", "Failure to monitor", "Pressure injury", "Birth injury",
             "Hospital-acquired infection", "Equipment failure", "Delay in treatment", "Communication/consent"],
    "clinic": ["Fall with injury", "Medication error", "Communication/consent", "Delay in diagnosis",
               "Procedure complication", "Equipment failure"],
}


def _gl_matters():
    """Claims against an entity alone (nursing and facility care, equipment, falls, premises): risk management keeps
    them in the general liability register, not the clinician claims register, and reports them to the entity's
    carrier under the entity's own policy; a serious event is noticed to the carrier first."""
    rng = K.claims_stream("gl-matters")
    out = []
    for (y, m) in K.months(K.WORLD_FIRST, K.HCM_LAST):
        for e in K.ENTITY_ORDER:
            if K.ENTITIES[e]["joined"] and dt.date(y, m, 1) < K.ENTITIES[e]["joined"]:
                continue
            for _ in range(int(rng.poisson(GL_RATE[e] / 12.0))):
                d = dt.date(y, m, int(rng.integers(1, K.days_in_month(y, m) + 1)))
                if e == "CMG":
                    d = clinic_day(d)
                lag = int(min(2400, max(30, round(_lognormal(rng, 330, 0.7)))))
                made = bday(d + dt.timedelta(days=lag))
                suit = rng.random() < 0.45
                level = _cost_level(d.year)
                if rng.random() < 0.45:
                    ind = _lognormal(rng, 120000, 0.8) * level
                    dfn = _lognormal(rng, 45000, 0.5) * level
                else:
                    ind, dfn = 0.0, _lognormal(rng, 18000 if suit else 6000, 0.6) * level
                close = bday(made + dt.timedelta(days=int(rng.integers(300, 1301) if suit else rng.integers(90, 721))))
                opts = GL_ALLEGATIONS["clinic" if e == "CMG" else "hosp"]
                inc = Incident(d, e, None, "GL", [], opts[int(rng.integers(0, len(opts)))])
                inc.claims = [ClaimNo(made, "Suit" if suit else "Claim", [], ind, dfn, close)]
                if rng.random() < 0.5:
                    nd = bday(d + dt.timedelta(days=int(rng.integers(3, 61))))
                    if nd < made and not (GAP_FIRST <= made <= K.VALUATION):
                        inc.notice = nd
                for c in inc.claims:
                    c.report = carrier_report_date(c.made)
                inc.unreported = False
                out.append(inc)
    # each entity has at least one open claim against it alone that the carrier first heard of as a notice: where none
    # is, the entity's most recent claim against it alone made before the last week of September is still open (a
    # suit takes years) and was noticed first
    V = K.VALUATION
    for e in K.ENTITY_ORDER:
        opn = [inc for inc in out if inc.entity == e and inc.claims[0].made < GAP_FIRST and _open_at(inc.claims[0], V)]
        if any(inc.notice is not None for inc in opn):
            continue
        spare = [inc for inc in opn if (inc.claims[0].made - inc.date).days >= 20]
        if not spare:
            recent = sorted((inc for inc in out if inc.entity == e and inc.claims[0].made < GAP_FIRST -
                             dt.timedelta(days=14) and (inc.claims[0].made - inc.date).days >= 20),
                            key=lambda i: (i.claims[0].made, i.date))
            if not recent:
                continue
            inc = recent[-1]
            c = inc.claims[0]
            c.matter_type = "Suit"
            c.close = bday(V + dt.timedelta(days=int(rng.integers(200, 601))))
            spare = [inc]
        inc = spare[int(rng.integers(0, len(spare)))]
        gap = (inc.claims[0].made - inc.date).days
        nd = bday(inc.date + dt.timedelta(days=int(rng.integers(3, min(61, gap - 5)))))
        if nd < inc.claims[0].made:
            inc.notice = nd
    return out


def _dup_incidents(incidents):
    """Noticed matters whose claim risk management registered under a new incident record when it came in, instead of
    the record opened at the notice: the claims register carries the new incident number on every claim number of the
    matter, and the notice log keeps the one given at the notice. Each entity has at least one such matter open at the
    valuation date. The register's grouping of claim numbers by incident is untouched; only the notice log's incident
    number for the notice differs from the register's."""
    rng = K.claims_stream("dup-incidents")
    V = K.VALUATION
    on_line = lambda inc: any(d.line != "CONTRACT" for d in inc.claims[0].defendants)
    for inc in incidents:
        inc.dup = False
    for e in K.ENTITY_ORDER:
        base = [inc for inc in incidents if inc.entity == e and on_line(inc)
                and inc.claims[0].made < GAP_FIRST and any(_open_at(c, V) for c in inc.claims)
                and not getattr(inc, "unreported", False)]
        cands = [inc for inc in base if inc.notice is not None]
        if not cands:
            spare = [inc for inc in base if inc.notice is None and (inc.claims[0].made - inc.date).days >= 20]
            if not spare:
                continue
            inc = spare[int(rng.integers(0, len(spare)))]
            gap = (inc.claims[0].made - inc.date).days
            nd = bday(inc.date + dt.timedelta(days=int(rng.integers(4, min(61, gap - 5)))))
            if nd >= inc.claims[0].made:
                continue
            inc.notice = nd
            cands = [inc]
        cands.sort(key=lambda i: (i.date, i.claims[0].made))
        k = 2 if (len(cands) >= 3 and rng.random() < 0.5) else 1
        for i in sorted(int(x) for x in rng.choice(len(cands), size=k, replace=False)):
            cands[i].dup = True


def _numbering(incidents, notice_only, gl=()):
    """Claim numbers by the year a claim is made, incident numbers by the year risk management opened the incident,
    notice numbers by the year a notice went out, each in date order with the gaps the other lines of business
    leave."""
    rng = K.claims_stream("numbers")
    allc = []
    for i, inc in enumerate(incidents):
        inc.rm_opened = inc.notice or (inc.date + dt.timedelta(days=int(rng.integers(1, 15)))
                                       if inc.route == "ERP" or rng.random() < 0.3 else inc.claims[0].made)
        if inc.rm_opened > inc.claims[0].made:
            inc.rm_opened = inc.claims[0].made
        for k, c in enumerate(inc.claims):
            allc.append((c.made, inc.date, i, k, c))
    allc.sort(key=lambda t: t[:4])
    seq = {}
    for made, _, _, _, c in allc:
        y = made.year
        seq[y] = seq.get(y, 0) + int(rng.integers(1, 7))
        c.claim_no = "CL-%d-%04d" % (y, seq[y])
    for inc in notice_only:
        inc.rm_opened = inc.date + dt.timedelta(days=int(rng.integers(0, 4)))
    rg = K.claims_stream("numbers-gl")
    for inc in gl:
        inc.rm_opened = inc.notice or min(inc.claims[0].made, inc.date + dt.timedelta(days=int(rg.integers(1, 15))))
    gseq = {}
    for inc in sorted(gl, key=lambda i: (i.claims[0].made, i.date, i.entity)):
        y = inc.claims[0].made.year
        gseq[y] = gseq.get(y, 0) + int(rg.integers(1, 5))
        inc.claims[0].claim_no = "GL-%d-%04d" % (y, gseq[y])
    tagged = [(inc.rm_opened, inc.date, 0, i, inc, "incident_no") for i, inc in enumerate(incidents)] + \
             [(inc.rm_opened, inc.date, 1, i, inc, "incident_no") for i, inc in enumerate(notice_only)] + \
             [(inc.rm_opened, inc.date, 2, i, inc, "incident_no") for i, inc in enumerate(gl)] + \
             [(inc.claims[0].made, inc.date, 3, i, inc, "reg_incident_no") for i, inc in enumerate(incidents)
              if getattr(inc, "dup", False)]
    tagged.sort(key=lambda t: t[:4])
    iseq = {}
    for opened, _, _, _, inc, attr in tagged:
        y = opened.year
        iseq[y] = iseq.get(y, 0) + int(rng.integers(3, 40))
        setattr(inc, attr, "IR-%d-%05d" % (y, iseq[y]))
    noticed = sorted(((inc.notice, inc.date, t, i, inc) for t, group in enumerate((incidents, notice_only, gl))
                      for i, inc in enumerate(group) if inc.notice is not None), key=lambda t: t[:4])
    nseq = {}
    for *_, inc in noticed:
        y = inc.notice.year
        nseq[y] = nseq.get(y, 0) + int(rng.integers(1, 4))
        inc.notice_no = "RMN-%02d-%04d" % (y % 100, nseq[y])


def _round_to(x, step):
    return float(int(x / step + 0.5) * step)


def valuation(incidents, V=K.VALUATION, key="v", stream="valuation"):
    """Paid and case reserves for every claim number made by V, as risk management records them on V: closed claims
    paid out, open claims with the defence paid so far and the adjuster's reserves, reopened claims with a fresh
    defence reserve."""
    rng = K.claims_stream(stream, V.isoformat())
    for inc in incidents:
        for c in inc.claims:
            if c.made > V:
                c.__dict__.setdefault("vals", {})[key] = None
                continue
            noise = float(np.exp(0.35 * rng.standard_normal()))
            u1, u2 = float(rng.uniform(0.55, 0.95)), float(rng.uniform(0.9, 1.3))
            nominal = float(rng.choice([0, 10000, 25000, 50000]))
            if c.close <= V:
                if c.reopen is not None and c.reopen <= V:
                    st = dict(status="REOPENED", closed=c.close, paid_ind=c.indemnity, paid_def=c.defense,
                              res_ind=0.0, res_def=c.reopen_reserve)
                else:
                    st = dict(status="CLOSED", closed=c.close, paid_ind=c.indemnity, paid_def=c.defense, res_ind=0.0,
                              res_def=0.0)
            else:
                f = (V - c.made).days / max(1, (c.close - c.made).days)
                paid_def = c.defense * f * u1
                if c.indemnity > 0:
                    est = c.indemnity * noise
                    res_ind = _round_to(est, 5000 if est > 50000 else 1000)
                elif c.matter_type == "Suit" or c.prior is not None:
                    res_ind = nominal
                else:
                    res_ind = 0.0
                res_def = max(0.0, _round_to(c.defense * u2 - paid_def, 1000))
                if c.cap and paid_def + res_ind + res_def > c.cap:
                    res_ind = max(0.0, math.floor((c.cap - paid_def - res_def) / 1000.0) * 1000.0)
                st = dict(status="OPEN", closed=None, paid_ind=0.0, paid_def=paid_def, res_ind=res_ind,
                          res_def=res_def)
            c.__dict__.setdefault("vals", {})[key] = st
    return incidents


def rows_of(inc, c, key="v"):
    """The register's rows for one claim number: one per named clinician, amounts split by each defendant's share
    (contracted clinicians carry none)."""
    st = c.vals[key]
    out = []
    for seq, d in enumerate(c.defendants, start=1):
        if d.line == "CONTRACT":
            amt = (None, None, None, None)
        else:
            amt = (round(st["paid_ind"] * d.share, 2), round(st["paid_def"] * d.share, 2),
                   _round_to(st["res_ind"] * d.share, 1000) if st["res_ind"] else 0.0,
                   _round_to(st["res_def"] * d.share, 1000) if st["res_def"] else 0.0)
        out.append(dict(claim_no=c.claim_no, incident_no=getattr(inc, "reg_incident_no", "") or inc.incident_no,
                        defendant_seq=seq,
                        clinician_id=d.clinician_id, defendant_role=d.role, specialty=d.specialty,
                        coverage_line=d.line, entity_at_incident=inc.entity, incident_date=inc.date,
                        claim_made_date=c.made, matter_type=c.matter_type, allegation=inc.allegation,
                        status=st["status"], closed_date=st["closed"], indemnity_paid=amt[0], defense_paid=amt[1],
                        indemnity_reserve=amt[2], defense_reserve=amt[3],
                        prior_claim_no=c.prior.claim_no if c.prior is not None else "", job=d.job))
    return out


def register(incidents, key="v", V=K.VALUATION):
    rows = []
    for inc in incidents:
        for c in inc.claims:
            if c.made <= V:
                rows.extend(rows_of(inc, c, key))
    return rows


def experience_from_rows(rows, job_of=None):
    """The main call's experience from register rows (dicts with dates as date objects): incidents in the
    experience window with a covered clinician, one Claim per incident made at its earliest claim number, its cost
    the paid and reserves on covered rows trended from the incident year. job_of(clinician_id, date) gives the
    payroll job key; rows carry it in memory."""
    lo, hi = K.EXPERIENCE
    by_inc = {}
    for r in rows:
        if not (lo <= r["incident_date"] <= hi):
            continue
        by_inc.setdefault(r["incident_no"], []).append(r)
    out = []
    for ino, rs in by_inc.items():
        def covered(r):
            if r["coverage_line"] == "CONTRACT":
                return False
            j = job_of(r["clinician_id"], r["incident_date"]) if job_of else r["job"]
            return K.CLASS_OF_JOB.get(j) is not None
        cov = [r for r in rs if covered(r)]
        if not cov:
            continue
        made = min(r["claim_made_date"] for r in rs)
        first_claim = sorted({(r["claim_made_date"], r["claim_no"]) for r in rs})[0][1]
        firsts = sorted((r for r in cov if r["claim_no"] == first_claim), key=lambda r: r["defendant_seq"])
        j = job_of(firsts[0]["clinician_id"], firsts[0]["incident_date"]) if job_of else firsts[0]["job"]
        inc_date = rs[0]["incident_date"]
        tf = K.trend_factor(inc_date.year)
        cost = sum((r["indemnity_paid"] or 0) + (r["defense_paid"] or 0) + (r["indemnity_reserve"] or 0) +
                   (r["defense_reserve"] or 0) for r in cov) * tf
        parts, parts3 = [], []
        for cno in sorted({r["claim_no"] for r in rs}):
            cr = [r for r in cov if r["claim_no"] == cno]
            pc = sum((r["indemnity_paid"] or 0) + (r["defense_paid"] or 0) + (r["indemnity_reserve"] or 0) +
                     (r["defense_reserve"] or 0) for r in cr) * tf
            pm = [r for r in rs if r["claim_no"] == cno][0]["claim_made_date"]
            parts.append(((pm - inc_date).days, pc))
            parts3.append(((pm - inc_date).days, pc, pm.year == inc_date.year))
        out.append(dict(incident_no=ino, cls=K.CLASS_OF_JOB[j], lag=(made - inc_date).days, cost=cost,
                        year=inc_date.year, same_year=made.year == inc_date.year, parts=parts, parts3=parts3,
                        n_claim_nos=len(parts), ent=rs[0]["entity_at_incident"]))
    out.sort(key=lambda c: c["incident_no"])
    return out
