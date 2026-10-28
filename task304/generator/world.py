"""The clean world for task304 architecture 2: people, their hepatitis C histories, the four settings' arrivals,
the peer team's tests, the regional laboratory's results, the network's treatment register, the prison health
provider's course log and the 2018-19 pilot. Nothing here is messy: records.py writes the shipped files from it.

Every person's history is drawn once, forward in time, and every record is derived from that history, so each file
holds what its own producer could see: the regional laboratory never sees a prison sample (the prisons send theirs to
the prison provider's contracted laboratory), the network register holds only courses its own clinics ran, the prison
log only courses given inside, and the peer team only what it tested."""
import datetime as dt
import hashlib

import numpy as np

import params as P

D = dt.date
DAY = dt.timedelta(days=1)


def _d(x):
    return D.fromordinal(int(x))


class World:
    def __init__(self, seed=P.SEED):
        self.rng = np.random.default_rng(seed)
        self.people = {}          # pid -> dict(sex, birth_year)
        self.lab = []             # dict rows: pid, sample_date, requester, test (AB/RNA), result, vl
        self.register = []        # network courses
        self.prison = []          # prison provider courses
        self.prison_tests = []    # prison reception blood-borne virus tests (positives)
        self.arrivals = []        # pid, setting, arrival_date
        self.peer = []            # pid, setting/venue, test_date, result
        self.pilot = []           # pilot caseload
        self.truth = {}           # (pid, setting, plan_year) -> state at first arrival that year
        self._ids = set()
        self._ord_seq = 0

    # ---------------------------------------------------------------- identities
    def pid(self):
        while True:
            h = hashlib.sha256(("%d-%d" % (P.SEED, self._ord_seq)).encode()).hexdigest().upper()
            self._ord_seq += 1
            x = h[:10]
            if x[0].isalpha() and x not in self._ids:
                self._ids.add(x)
                return x

    def person(self, sex=None, by=None):
        p = self.pid()
        r = self.rng
        self.people[p] = dict(sex=sex or ("M" if r.random() < 0.72 else "F"),
                              birth_year=int(by if by else r.integers(1960, 2003)))
        return p

    def rdate(self, a, b):
        a, b = a.toordinal(), b.toordinal()
        if b <= a:
            return _d(a)
        return _d(self.rng.integers(a, b + 1))

    # ---------------------------------------------------------------- laboratory events
    def lab_ab(self, pid, when, requester, reactive):
        self.lab.append(dict(pid=pid, sample_date=when, requester=requester, test="AB",
                             result="Reactive" if reactive else "Non-reactive", vl=None))

    def lab_rna(self, pid, when, requester, detected):
        r = self.rng
        vl = None
        if detected:
            vl = float(10 ** r.normal(5.6, 0.8)) if r.random() > 0.03 else 9.0   # a few detected below 15
        self.lab.append(dict(pid=pid, sample_date=when, requester=requester, test="RNA",
                             result="Detected" if detected else "Not detected", vl=vl))

    def diagnose_in_lab(self, pid, when, requester, chronic):
        """first lab diagnosis: antibody, reflex RNA on the same sample a few days later"""
        self.lab_ab(pid, when, requester, True)
        self.lab_rna(pid, when + dt.timedelta(days=int(self.rng.integers(0, 9))), requester, chronic)

    # ---------------------------------------------------------------- courses
    def network_course(self, pid, start, clinic, svr_in_lab=True, route=None, cure=None):
        """a course the network's clinics run; returns (cured, svr_date)"""
        r = self.rng
        weeks = 8 if r.random() < 0.46 else 12
        regimen = "glecaprevir/pibrentasvir" if weeks == 8 else "sofosbuvir/velpatasvir"
        if start < D(2017, 6, 1) and r.random() < 0.5:
            regimen, weeks = "ledipasvir/sofosbuvir", 12
        planned_end = start + dt.timedelta(weeks=weeks)
        u = r.random()
        if u < 0.035:
            outcome, stopped = "Stopped", start + dt.timedelta(days=int(r.integers(14, weeks * 7 - 7)))
        elif u < 0.055:
            outcome, stopped = "Lost to follow-up", None
        else:
            outcome, stopped = "Completed", None
        end = stopped or planned_end
        if cure is None:
            cure = r.random() < (P.SVR_RATE if outcome == "Completed" else 0.55)
        no_test = r.random() < (P.NO_SVR_TEST if outcome == "Completed" else 0.45)
        svr_date = end + dt.timedelta(days=int(r.integers(86, 150)))
        # end-of-treatment test in the lab for most courses
        if svr_in_lab and outcome != "Lost to follow-up" and r.random() < 0.7:
            self.lab_rna(pid, end + dt.timedelta(days=int(r.integers(0, 27))), clinic_req(clinic), False)
        keyed = True
        if no_test:
            res = None
        else:
            res = "Not detected" if cure else "Detected"
            if svr_in_lab:
                self.lab_rna(pid, svr_date, clinic_req(clinic), not cure)
        row = dict(pid=pid, clinic=clinic, route=route or clinic_route(clinic, r), start=start, regimen=regimen,
                   weeks=weeks, planned_end=planned_end, outcome=outcome, stopped=stopped,
                   svr_date=None if res is None else svr_date, svr_result=res, keyed=keyed, cure=cure and not no_test,
                   true_cure=cure)
        self.register.append(row)
        return (cure, svr_date, row)

    def reception_test(self, pid, prison, prisoner_no, when, viraemic):
        """opt-out blood-borne virus test at a prison reception, run by Corvane's own laboratory"""
        self.prison_tests.append(dict(pid=pid, prison=prison, prisoner_no=prisoner_no, test_date=when,
                                      ab="Reactive", rna="Detected" if viraemic else "Not detected"))

    def prison_course(self, pid, start, prison, prisoner_no, release=None, cure=None):
        r = self.rng
        weeks = 8 if r.random() < 0.55 else 12
        regimen = "glecaprevir/pibrentasvir" if weeks == 8 else "sofosbuvir/velpatasvir"
        end = start + dt.timedelta(weeks=weeks)
        released_mid = release is not None and release < end
        if cure is None:
            cure = r.random() < P.SVR_RATE
        no_test = r.random() < P.NO_SVR_TEST + (0.10 if released_mid else 0.0)
        svr_date = end + dt.timedelta(days=int(r.integers(86, 140)))
        res = None if no_test else ("Not detected" if cure else "Detected")
        self.prison.append(dict(pid=pid, prison=prison, prisoner_no=prisoner_no, start=start, regimen=regimen,
                                weeks=weeks, end=end, released_mid=released_mid,
                                release=release if released_mid else None,
                                svr_date=None if res is None else svr_date, svr_result=res, true_cure=cure))
        return (cure, svr_date)


def clinic_req(clinic):
    return {"HEP": "HOSPITAL", "COMM": "COMMUNITY_CLINIC", "FRC": "DRUG_SERVICE", "PHARM": "PHARMACY_CLINIC",
            "OUT": "OUTREACH_CLINIC"}[clinic]


def clinic_route(clinic, r):
    return {"HEP": "GP referral", "COMM": "GP referral", "FRC": "Drug service", "PHARM": "Pharmacy",
            "OUT": "Outreach"}[clinic]


def prisoner_no(r):
    letters = "ABCDEFGHJKLMNPRSTVWXYZ"
    return "%s%04d%s%s" % (letters[r.integers(0, len(letters))], r.integers(1000, 9999),
                           letters[r.integers(0, len(letters))], letters[r.integers(0, len(letters))])


def plan_year(d):
    if P.POOL_START <= d <= D(2025, 9, 30):
        return 1
    if D(2025, 10, 1) <= d <= P.AS_OF:
        return 2
    if P.ARRIVALS_START <= d < P.POOL_START:
        return 0
    return None


def build(seed=P.SEED):
    W = World(seed)
    r = W.rng
    _background(W)
    _settings(W)
    _pilot(W)
    _prison_background(W)
    return W


# -------------------------------------------------------------------- background laboratory and network courses
def _background(W):
    r = W.rng
    years = range(2015, 2027)
    for y in years:
        frac = 0.75 if y == 2026 else 1.0
        for req, (n, pos) in P.LAB_REQUESTERS.items():
            scale = 1.0 + 0.035 * (y - 2015) if req in ("GP", "SEXUAL_HEALTH") else 1.0
            if req == "OUTREACH_CLINIC" and y < 2018:
                continue
            k = int(r.normal(n * scale * frac, n * 0.03))
            for _ in range(k):
                pid = W.person(sex="F" if req == "ANTENATAL" else None,
                               by=(r.integers(1982, 2005) if req == "ANTENATAL" else None))
                when = W.rdate(D(y, 1, 1), min(D(y, 12, 31), P.AS_OF))
                if r.random() < pos:
                    chronic = r.random() < P.VIRAEMIC_NEVER_TREATED
                    W.diagnose_in_lab(pid, when, req, chronic)
                    if chronic and r.random() < _treat_prob(y):
                        start = when + dt.timedelta(days=int(r.integers(35, 200)))
                        if start <= P.AS_OF - dt.timedelta(days=10):
                            clinic = _clinic_for(req, start, r)
                            cure, svr_date, row = W.network_course(pid, start, clinic)
                            _maybe_reinfect(W, pid, svr_date, cure, req)
                else:
                    W.lab_ab(pid, when, req, False)
                # some background people are tested again for antibody years later (still negative)
                if r.random() < 0.05:
                    later = when + dt.timedelta(days=int(r.integers(200, 1500)))
                    if later <= P.AS_OF:
                        W.lab_ab(pid, later, req, False)


def _treat_prob(y):
    return {2015: 0.18, 2016: 0.35, 2017: 0.5, 2018: 0.62, 2019: 0.7, 2020: 0.55, 2021: 0.66, 2022: 0.7,
            2023: 0.68, 2024: 0.66, 2025: 0.62, 2026: 0.45}[y]


def _clinic_for(req, start, r):
    if req in ("DRUG_SERVICE",):
        return "FRC" if r.random() < 0.8 else "OUT"
    if req == "OUTREACH_CLINIC":
        return "OUT" if r.random() < 0.75 else "PHARM"
    if req == "HOSPITAL":
        return "HEP"
    u = r.random()
    if start >= D(2019, 1, 1) and u < 0.12:
        return "PHARM"
    return "COMM" if u < 0.62 else "HEP"


def _maybe_reinfect(W, pid, svr_date, cure, req):
    r = W.rng
    if cure and req in ("DRUG_SERVICE", "OUTREACH_CLINIC") and r.random() < 0.07:
        when = svr_date + dt.timedelta(days=int(r.integers(200, 1400)))
        if when <= P.AS_OF - dt.timedelta(days=60):
            W.lab_rna(pid, when, req, True)
            if r.random() < 0.6:
                start = when + dt.timedelta(days=int(r.integers(30, 120)))
                if start <= P.AS_OF - dt.timedelta(days=10):
                    W.network_course(pid, start, "FRC" if req == "DRUG_SERVICE" else "OUT")


# -------------------------------------------------------------------- the four settings
def _settings(W):
    r = W.rng
    years = [(0, P.ARRIVALS_START, D(2024, 9, 30)), (1, P.POOL_START, D(2025, 9, 30)), (2, D(2025, 10, 1), P.AS_OF)]
    carry = {s: [] for s in P.SETTINGS}       # people who come back the next year
    for s in P.SETTINGS:
        w = P.WORLD[s]
        for (yi, a, b) in years:
            n = int(round(r.normal(w["arrive"], w["arrive"] * 0.035)))
            back = [p for p in carry[s] if r.random() < 0.5]
            new = n - len(back)
            pids = back + [(_in_course_person(W, a, b) if (s == "AP" and yi >= 1 and r.random() < 0.015)
                            else _arrival_person(W, s, a)) for _ in range(max(new, 0))]
            nxt = []
            for pid in pids:
                first = W.people[pid].pop("fixed_arrival", None) or W.rdate(a, b)
                W.arrivals.append(dict(pid=pid, setting=s, arrival_date=first))
                if r.random() < 0.06:          # a second stay in the same plan year
                    again = first + dt.timedelta(days=int(r.integers(20, 160)))
                    if again <= b:
                        W.arrivals.append(dict(pid=pid, setting=s, arrival_date=again))
                state = _state_at(W, pid, first)
                W.truth[(pid, s, yi)] = dict(state, arrival=first)
                if yi >= 1:
                    _peer_and_after(W, pid, s, first, state)
                if r.random() < 0.08:
                    nxt.append(pid)
            carry[s] = nxt


def _arrival_person(W, s, window_start):
    """draw a person and their whole hepatitis C history up to the end of the record.

    An infection is chronic (the field's three quarters) or clears by itself. A person may have been tested at a
    prison reception (Corvane's own laboratory, recorded in its workbook) and in the community (Fenwold Pathology);
    a chronic infection found at either is treated with that setting's coverage, inside by Corvane or outside by the
    network. Community testing, where it happened, came first. A cure can be followed by a new infection."""
    r = W.rng
    w = P.WORLD[s]
    pid = W.person(by=r.integers(1966, 2004))
    pos = r.random() < w["ab"]
    hist = dict(pos=pos, cured=False, chronic=False, reinfected=False, where=None, reinf_date=None,
                cure_date=None, in_lab=False)
    W.people[pid]["hist"] = hist
    if not pos:
        if r.random() < 0.35:   # tested negative in the community at some point
            when = W.rdate(D(2015, 3, 1), window_start - dt.timedelta(days=60))
            W.lab_ab(pid, when, "DRUG_SERVICE" if s in ("DS", "NSP") else "GP", False)
        return pid
    chronic = r.random() < P.VIRAEMIC_NEVER_TREATED
    hist["chronic"] = chronic
    latest = window_start - dt.timedelta(days=150)
    comm_dx = r.random() < w["comm_dx"]
    prison_dx = r.random() < w["prison_dx"]
    t_comm = W.rdate(D(2015, 2, 1), latest - dt.timedelta(days=400)) if comm_dx else None
    receptions = []
    if prison_dx:
        k = 1 + int(r.random() < 0.45) + int(r.random() < 0.2)
        lo = max(D(2017, 4, 1), (t_comm + dt.timedelta(days=60)) if t_comm else D(2017, 4, 1))
        receptions = sorted(W.rdate(lo, latest - dt.timedelta(days=120)) for _ in range(k))
    prison = ["TAM", "SAL"][int(r.integers(0, 2))] if W.people[pid]["sex"] == "M" else "HAV"
    pno = prisoner_no(r)
    cured_at = None
    if comm_dx:
        W.diagnose_in_lab(pid, t_comm, "DRUG_SERVICE" if r.random() < 0.55 else "GP", chronic)
        hist["in_lab"] = True
        if chronic and r.random() < w["cov_comm"]:
            start = t_comm + dt.timedelta(days=int(r.integers(40, 320)))
            if not receptions or start < receptions[0]:
                clinic = "FRC" if r.random() < 0.45 else ("COMM" if r.random() < 0.6 else "HEP")
                cure, svr, row = W.network_course(pid, start, clinic, cure=True)
                if row["svr_result"] is None:
                    row["svr_result"], row["svr_date"] = "Not detected", svr
                    W.lab_rna(pid, svr, clinic_req(clinic), False)
                cured_at, hist["where"] = svr, "network"
    if receptions:
        hist["prison_tested"] = True
    for i, rec in enumerate(receptions):
        viraemic = chronic and (cured_at is None or rec < cured_at)
        W.reception_test(pid, prison, pno, rec, viraemic if cured_at is None else False)
        if viraemic and cured_at is None and r.random() < w["cov_prison"]:
            start = rec + dt.timedelta(days=int(r.integers(18, 70)))
            cure, svr = W.prison_course(pid, start, prison, pno, cure=True)
            if W.prison[-1]["svr_result"] is None:     # every cure of a setting arrival is on record
                W.prison[-1]["svr_result"], W.prison[-1]["svr_date"] = "Not detected", svr
            cured_at, hist["where"] = svr, "prison"
    if cured_at is not None:
        hist["cured"], hist["cure_date"] = True, cured_at
        if r.random() < w["reinf"]:
            hist["reinfected"] = True
            rd = W.rdate(cured_at + dt.timedelta(days=180), window_start - dt.timedelta(days=40))
            hist["reinf_date"] = rd
            if hist["in_lab"] and r.random() < w["reinf_lab"]:
                W.lab_rna(pid, rd + dt.timedelta(days=int(r.integers(30, 200))),
                          "DRUG_SERVICE" if r.random() < 0.6 else "OUTREACH_CLINIC", True)
                hist["reinf_in_lab"] = True
    return pid


def _in_course_person(W, a, b):
    """a person released part-way through a prison course, arriving at the approved premises; the network
    carries the course on (a register row from the handover)"""
    r = W.rng
    pid = W.person(sex="M", by=r.integers(1966, 2004))
    h = dict(pos=True, cured=False, chronic=True, reinfected=False, where=None, reinf_date=None, cure_date=None,
             in_lab=False, in_course=True)
    W.people[pid]["hist"] = h
    first = W.rdate(a, b)
    W.people[pid]["fixed_arrival"] = first
    release = first - dt.timedelta(days=int(r.integers(0, 4)))
    start = release - dt.timedelta(days=int(r.integers(12, 50)))
    pr = ["TAM", "SAL"][int(r.integers(0, 2))]
    pno = prisoner_no(r)
    W.reception_test(pid, pr, pno, start - dt.timedelta(days=int(r.integers(20, 60))), True)
    W.prison_course(pid, start, pr, pno, release=release, cure=True)
    weeks_left = max(1, W.prison[-1]["weeks"] - (release - start).days // 7)
    cure, svr, row = W.network_course(pid, first + dt.timedelta(days=int(r.integers(1, 6))), "OUT",
                                      route="Prison handover", cure=True)
    row.update(weeks=weeks_left, planned_end=row["start"] + dt.timedelta(weeks=weeks_left), regimen=W.prison[-1]["regimen"])
    h["post_cure"] = svr
    h["in_course_until"] = row["planned_end"]
    return pid


def _state_at(W, pid, when):
    h = W.people[pid].get("hist")
    if not h or not h["pos"]:
        return dict(pos=False, active=False, cat="neg")
    if h.get("in_course"):
        return dict(pos=True, active=False, cat="in_course")
    if h.get("post_cure") and h["post_cure"] <= when:
        return dict(pos=True, active=False, cat="cured_after")
    if h["cured"]:
        if h["reinfected"] and h["reinf_date"] <= when:
            return dict(pos=True, active=True, cat="reinfected_" + h["where"], reinf_lab=h.get("reinf_in_lab", False))
        return dict(pos=True, active=False, cat="cured_" + h["where"])
    return dict(pos=True, active=h["chronic"], cat="untreated_chronic" if h["chronic"] else "cleared")


def _peer_and_after(W, pid, s, first, state):
    r = W.rng
    if r.random() >= P.PEER_TEST_SHARE:
        return
    # one test per person in twelve months
    last = W.people[pid].get("last_peer")
    td = first + dt.timedelta(days=int(r.integers(0, 42)))
    td = min(td, P.AS_OF)
    if last is not None and (td - last).days < 365:
        return
    W.people[pid]["last_peer"] = td
    W.peer.append(dict(pid=pid, setting=s, test_date=td, result="Reactive" if state["pos"] else "Non-reactive"))
    if not state["pos"]:
        return
    h0 = W.people[pid]["hist"]
    if state["cat"].startswith("cured_") or state["cat"] in ("cured_after", "in_course"):
        return       # they know they were treated (or are on a course), and do not come to clinic for an RNA test
    if state["cat"] == "cleared" and (h0.get("in_lab") or h0.get("prison_tested")):
        return       # told at an earlier test that the virus had cleared
    if r.random() >= P.ATTEND:
        return
    when = td + dt.timedelta(days=int(r.integers(14, 75)))
    if when > P.AS_OF:
        return
    h = W.people[pid]["hist"]
    req = "OUTREACH_CLINIC" if r.random() < 0.5 else "COMMUNITY_CLINIC"
    if h.get("in_lab"):
        W.lab_rna(pid, when, req, state["active"])          # a known positive is tested for RNA only
    else:
        W.diagnose_in_lab(pid, when, req, state["active"])
        h["in_lab"] = True
    if state["active"] and r.random() < 0.8:
        start = when + dt.timedelta(days=int(r.integers(21, 70)))
        if start <= P.AS_OF - dt.timedelta(days=7):
            clinic = "OUT" if req == "OUTREACH_CLINIC" else "COMM"
            cure, svr, row = W.network_course(pid, start, clinic)
            if cure:
                h["post_cure"] = svr


# -------------------------------------------------------------------- the 2018-19 pilot
def _pilot(W):
    r = W.rng
    for site, n in P.PILOT["arrive"].items():
        ab = P.PILOT["ab"][site]
        for _ in range(n):
            pid = W.person(by=r.integers(1960, 2001))
            arr = W.rdate(P.PILOT_START, P.PILOT_END)
            pos = r.random() < ab
            cured = pos and r.random() < P.PILOT["cured"]
            chronic = pos and not cured and r.random() < P.VIRAEMIC_NEVER_TREATED
            tested = r.random() < P.PILOT["test"]
            row = dict(pid=pid, site=site, arrival=arr, tested=tested, test_date=None, ab=None, rna=None,
                       started=False, start_date=None)
            if tested:
                off = int(r.integers(0, 35))
                left = (P.PILOT_END - arr).days
                if off > left:
                    off = off % (left + 1)     # the van left the two sites at the end of September 2019
                td = arr + dt.timedelta(days=off)
                row.update(test_date=td, ab="Reactive" if pos else "Non-reactive")
                if pos:
                    row["rna"] = "Detected" if chronic else "Not detected"
                    if chronic and r.random() < P.PILOT["start12"] / 0.93:
                        delay = int(r.integers(10, 84)) if r.random() < 0.93 else int(r.integers(90, 200))
                        row.update(started=True, start_date=td + dt.timedelta(days=delay))
            W.pilot.append(row)


# -------------------------------------------------------------------- prison courses for people not in the settings
def _prison_background(W):
    """people tested positive at a reception who never arrive in the four settings: their reception results and the
    courses Corvane gave them"""
    r = W.rng
    for y in range(2017, 2027):
        n = {2017: 150, 2018: 230, 2019: 420, 2020: 330, 2021: 380, 2022: 390, 2023: 300, 2024: 260,
             2025: 230, 2026: 140}[y]
        n = int(r.normal(n, n * 0.05))
        for _ in range(n):
            pr = ["TAM", "SAL", "HAV"][int(r.choice(3, p=[0.5, 0.33, 0.17]))]
            pid = W.person(sex="F" if pr == "HAV" else "M", by=r.integers(1962, 2004))
            pno = prisoner_no(r)
            rec = W.rdate(D(y, 1, 1), min(D(y, 12, 31), P.AS_OF - dt.timedelta(days=30)))
            chronic = r.random() < P.VIRAEMIC_NEVER_TREATED
            W.reception_test(pid, pr, pno, rec, chronic)
            if chronic and r.random() < (0.55 if y < 2019 else 0.9):
                start = rec + dt.timedelta(days=int(r.integers(18, 80)))
                if start > P.AS_OF - dt.timedelta(days=20):
                    continue
                release = None
                if r.random() < 0.16:
                    release = start + dt.timedelta(days=int(r.integers(7, 80)))
                W.prison_course(pid, start, pr, pno, release=release)
