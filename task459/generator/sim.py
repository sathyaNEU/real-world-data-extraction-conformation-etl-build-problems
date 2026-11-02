"""Services for task459's world: every medical, pharmacy and in-home support service the plan paid for in 2025.

Each service is generated from where the member actually was that day (world.Member.timeline) and from where
the member's regular care sits (the assigned primary care practice). The events here are clean: one row per
service with its true date, provider and amounts. pack.py adds the claim-system texture (multi-line claims,
replacements, voids, denials, reversals, the PBM's identifiers and date layouts).
"""
import datetime as dt

import numpy as np

import world as W

# Procedure codes and allowed amounts (Medicare-like 2025 rates, Arizona locality).
PCP_CODES = [("99213", 92.40), ("99214", 131.20), ("99215", 183.10), ("99397", 162.00)]
AWV = ("G0439", 133.50)
UC_CODES = [("99213", 96.80), ("99214", 138.40), ("99203", 112.60)]
SPEC_CODES = [("99243", 172.50), ("99244", 233.40), ("99214", 131.20), ("99215", 183.10)]
PT_CODES = [("97110", 31.60), ("97140", 28.90), ("97530", 35.20), ("97161", 104.70)]
LAB_PANELS = [[("80053", 11.20), ("85025", 8.10)], [("83036", 9.70)], [("80061", 13.40), ("84443", 17.60)],
              [("82570", 6.30), ("82043", 7.40)], [("85610", 4.30)]]
IMG_CODES = [("71046", 31.20), ("73721", 228.40), ("70553", 384.70), ("77080", 39.80), ("93306", 211.30)]
ER_CODES = [("99284", 268.90), ("99285", 391.40)]
TELE_CODES = [("99213", 92.40), ("99214", 131.20)]
HOME_CODES = [("T1019", 6.85), ("S5130", 6.10), ("S5150", 5.90)]  # per 15 minutes

DRUGS = [  # (ndc, name, strength, cost per 30 days)
    ("00093505698", "ATORVASTATIN CALCIUM", "20 MG TAB", 4.10), ("68180051301", "LISINOPRIL", "10 MG TAB", 2.20),
    ("00093104801", "METFORMIN HCL", "500 MG TAB", 2.90), ("00093317156", "AMLODIPINE BESYLATE", "5 MG TAB", 2.40),
    ("00378180001", "LEVOTHYROXINE SODIUM", "50 MCG TAB", 6.80), ("62175011843", "OMEPRAZOLE DR", "20 MG CAP", 5.60),
    ("68180037703", "LOSARTAN POTASSIUM", "50 MG TAB", 3.70), ("55111046705", "METOPROLOL SUCC ER", "25 MG TAB", 6.20),
    ("00228273611", "TAMSULOSIN HCL", "0.4 MG CAP", 5.90), ("00003089321", "ELIQUIS", "5 MG TAB", 541.00),
    ("16729002010", "DONEPEZIL HCL", "10 MG TAB", 4.60), ("00172208380", "HYDROCHLOROTHIAZIDE", "25 MG TAB", 1.90),
    ("68382013610", "GABAPENTIN", "300 MG CAP", 5.10), ("00088221905", "LANTUS SOLOSTAR", "100 UNIT/ML", 312.00),
    ("00006027731", "JANUVIA", "100 MG TAB", 518.00), ("00597014030", "JARDIANCE", "10 MG TAB", 566.00),
]
ACUTE = [("00093310901", "AMOXICILLIN", "500 MG CAP", 7.20), ("00781506131", "CIPROFLOXACIN", "500 MG TAB", 6.40),
         ("00093085001", "PREDNISONE", "10 MG TAB", 3.10), ("59762332401", "AZITHROMYCIN", "250 MG TAB", 9.80)]


class Svc:
    __slots__ = ("mid", "date", "npi", "pos", "lines", "kind", "here")

    def __init__(self, mid, date, npi, pos, lines, kind, here):
        self.mid = mid
        self.date = date
        self.npi = npi
        self.pos = pos
        self.lines = lines        # [(code, units, allowed)]
        self.kind = kind
        self.here = here          # region where the member was that day (truth)


class Fill:
    __slots__ = ("mid", "date", "ncpdp", "ndc", "name", "strength", "days", "qty", "cost", "here")

    def __init__(self, mid, date, ncpdp, ndc, name, strength, days, qty, cost, here):
        self.mid, self.date, self.ncpdp, self.ndc, self.name = mid, date, ncpdp, ndc, name
        self.strength, self.days, self.qty, self.cost, self.here = strength, days, qty, cost, here


class Visit:
    __slots__ = ("mid", "date", "start", "npi", "code", "units", "here")

    def __init__(self, mid, date, start, npi, code, units, here):
        self.mid, self.date, self.start, self.npi, self.code, self.units, self.here = mid, date, start, npi, code, units, here


def spans(tl):
    out = []
    s = 0
    for i in range(1, len(tl) + 1):
        if i == len(tl) or tl[i] != tl[s]:
            out.append((s, i - 1, int(tl[s])))
            s = i
    return out


def pcp_on(m, d):
    p = m.pcp_hist[0][1]
    for when, npi in sorted(m.pcp_hist):
        if when <= d:
            p = npi
    return p


def simulate(wd):
    provs, byr, lab = wd["provs"], wd["by_region"], wd["lab"]
    ph_byr, mail, spec = wd["ph_by_region"], wd["mail"], wd["spec"]
    rng = W.stream("services")
    rng_rx = W.stream("pharmacy_fills")
    rng_hv = W.stream("home_visits")
    svcs, fills, visits = [], [], []
    spec_all = [p for p in provs.values() if p.kind == "spec"]

    def pick(lst, local_seed=None):
        return lst[int(rng.integers(0, len(lst)))]

    def add_svc(m, d_idx, kind, region_code, npi=None):
        d = W.day(d_idx)
        here = W.REGION_CODES[int(m.timeline[d_idx])] if 0 <= d_idx < W.NDAYS else None
        if kind in ("pcp", "awv", "tele") and npi is None and provs[pcp_on(m, d)].region != here:
            # the assigned practice is in another region on this day: the member is seen where they are
            kind, region_code = "dpcp", here
        if kind == "pcp":
            if npi is None:
                npi = pcp_on(m, d)
            code = PCP_CODES[int(rng.choice(4, p=[0.38, 0.47, 0.12, 0.03]))]
            lines = [(code[0], 1, code[1])]
            pos = "11"
        elif kind == "awv":
            npi = npi or pcp_on(m, d)
            lines = [(AWV[0], 1, AWV[1])]
            pos = "11"
        elif kind == "uc":
            p = pick(byr[region_code]["uc"])
            npi = p.npi
            code = UC_CODES[int(rng.choice(3, p=[0.5, 0.35, 0.15]))]
            lines = [(code[0], 1, code[1])]
            pos = "20"
        elif kind == "dpcp":  # a primary care visit away from the assigned practice
            p = pick(byr[region_code]["pcp"])
            npi = p.npi
            code = PCP_CODES[int(rng.choice(3, p=[0.5, 0.4, 0.1]))]
            lines = [(code[0], 1, code[1])]
            pos = "11"
        elif kind == "spec":
            if npi:
                p = provs[npi]
            else:
                # specialists practising in that region on that day (a practice that moved counts where it is)
                cand = [q for q in spec_all if q.region_on(d) == region_code]
                p = pick(cand)
            npi = p.npi
            code = SPEC_CODES[int(rng.choice(4, p=[0.3, 0.2, 0.35, 0.15]))]
            lines = [(code[0], 1, code[1])]
            pos = "11" if rng.random() < 0.8 else "22"
        elif kind == "pt":
            npi = npi or pick(byr[region_code]["pt"]).npi
            lines = []
            for c in PT_CODES[:3]:
                if rng.random() < 0.75:
                    lines.append((c[0], int(rng.integers(1, 4)), c[1]))
            if not lines:
                lines = [(PT_CODES[0][0], 2, PT_CODES[0][1])]
            pos = "11"
        elif kind == "lab_ref":
            npi = lab.npi
            panel = LAB_PANELS[int(rng.integers(0, len(LAB_PANELS)))]
            lines = [(c, 1, a) for c, a in panel]
            pos = "81"
        elif kind == "lab_hosp":
            p = pick(byr[region_code]["hosp"])
            npi = p.npi
            panel = LAB_PANELS[int(rng.integers(0, len(LAB_PANELS)))]
            lines = [(c, 1, round(a * 1.6, 2)) for c, a in panel]
            pos = "22"
        elif kind == "img":
            p = pick(byr[region_code]["img"])
            npi = p.npi
            code = IMG_CODES[int(rng.integers(0, len(IMG_CODES)))]
            lines = [(code[0], 1, code[1])]
            pos = "24" if rng.random() < 0.6 else "22"
        elif kind == "er":
            p = pick(byr[region_code]["hosp"])
            npi = p.npi
            code = ER_CODES[int(rng.choice(2, p=[0.7, 0.3]))]
            lines = [(code[0], 1, code[1])]
            pos = "23"
        elif kind == "tele":
            npi = pcp_on(m, d)
            code = TELE_CODES[int(rng.choice(2, p=[0.6, 0.4]))]
            lines = [(code[0], 1, code[1])]
            pos = "10"
        else:
            raise ValueError(kind)
        svcs.append(Svc(m.mid, d, npi, pos, lines, kind, here))

    def poisson_days(lo, hi, mean_gap, offset_rng=rng):
        out = []
        t = lo + float(offset_rng.exponential(mean_gap)) * 0.6
        while t <= hi:
            out.append(int(t))
            t += max(4.0, float(offset_rng.exponential(mean_gap)))
        return out

    def enrolled_days(m):
        s, e = m.enroll[0]
        lo = max(0, W.doy(s)) if s > W.YEAR_START else 0
        hi = W.NDAYS - 1
        if e is not None and e < W.YEAR_END:
            hi = W.doy(e)
        if m.dod is not None:
            hi = min(hi, W.doy(m.dod))
        return lo, hi

    for m in wd["members"]:
        lo, hi = enrolled_days(m)
        if hi < lo:
            continue
        young = m.kind == "young"
        sp = [(a, b, r) for a, b, r in spans(m.timeline) if b >= lo and a <= hi]
        sp = [(max(a, lo), min(b, hi), r) for a, b, r in sp]
        pt_series = rng.random() < (0.2 if not young else 0.1)
        pt_done = False
        for (a, b, ridx) in sp:
            span_start = len(svcs)
            rc = W.REGION_CODES[ridx]
            d_mid = W.day((a + b) // 2)
            care_region = provs[pcp_on(m, d_mid)].region
            home_care = rc == care_region
            length = b - a + 1
            if home_care:
                n_before = len(svcs)
                # Regular care: the assigned practice, specialists, therapy, laboratory and imaging.
                pcp_gap = 115 if not young else 200
                if m.kind == "long":
                    pcp_gap = 30
                for t in poisson_days(a, b, pcp_gap):
                    if rng.random() < (0.12 if m.kind not in ("long",) else 0.0) and m.kind != "short":
                        add_svc(m, t, "tele", rc)
                    else:
                        add_svc(m, t, "pcp", rc)
                if rng.random() < 0.55 and length > 60:
                    add_svc(m, a + int(rng.integers(5, max(6, length - 5))), "awv", rc)
                spec_gap = 260 if not young else 420
                if m.kind == "long":
                    spec_gap = 40
                for t in poisson_days(a, b, spec_gap):
                    add_svc(m, t, "spec", rc)
                lab_gap = 300 if not young else 480
                if m.kind == "long":
                    lab_gap = 45
                for t in poisson_days(a, b, lab_gap):
                    add_svc(m, t, "lab_hosp", rc)
                if pt_series and not pt_done and length > 50:
                    start = a + int(rng.integers(3, max(4, length - 45)))
                    pnpi = pick(byr[rc]["pt"]).npi
                    for k in range(int(rng.integers(6, 11))):
                        tt = start + k * int(rng.integers(3, 6))
                        if tt <= b:
                            add_svc(m, tt, "pt", rc, pnpi)
                    pt_done = True
                if rng.random() < (0.22 if m.kind == "long" else 0.12) * min(1.0, length / 120):
                    add_svc(m, a + int(rng.integers(0, length)), "img", rc)
                # High-country stayers see a specialist in the Valley or Tucson now and then: a day's drive.
                if rc in W.HIGH and m.kind in ("stay", "young") and len(svcs) - n_before >= 6 and rng.random() < 0.22:
                    tert = "MAR" if rng.random() < 0.75 else "SAZ"
                    for _ in range(int(rng.integers(1, 3))):
                        tt = a + int(rng.integers(25, max(26, length - 25)))
                        if tt > b - 25:
                            continue
                        # the referral visit before the drive and the follow-up after it, at the home practice
                        add_svc(m, tt - int(rng.integers(3, 18)), "pcp", rc)
                        add_svc(m, tt, "spec", tert)
                        add_svc(m, tt + int(rng.integers(3, 18)), "pcp", rc)
            else:
                # Away from the regular practice: urgent care, a local practice now and then, the odd test.
                uc_gap = 75 if m.kind == "long" else 95
                for t in poisson_days(a, b, uc_gap):
                    add_svc(m, t, "uc" if rng.random() < 0.6 else "dpcp", rc)
                if rng.random() < 0.5 * min(1.0, length / 120):
                    add_svc(m, a + int(rng.integers(0, length)), "lab_hosp", rc)
            # Independent reference laboratory work: the specimen is drawn at an office visit and the Phoenix
            # laboratory bills it under its own address, so the claim carries the visit's date.
            visit_days = [x.date for x in svcs[span_start:] if x.mid == m.mid and x.pos in ("11", "20", "22")]
            for dd in visit_days:
                if rng.random() < (0.14 if not young else 0.1):
                    add_svc(m, W.doy(dd), "lab_ref", rc)
            if rng.random() < 0.035 * length / 365:
                add_svc(m, a + int(rng.integers(0, length)), "er", rc)

        # Members who live part of the year away see someone on each side of every move: a visit or test in
        # the days before they leave and in the days after they arrive.
        if m.kind in ("long", "short", "summer", "early_mover", "late_mover") or (m.kind == "young" and m.notes):
            for i in range(1, len(sp)):
                prev_b = sp[i - 1][1]
                nxt_a = sp[i][0]
                prc = W.REGION_CODES[sp[i - 1][2]]
                nrc = W.REGION_CODES[sp[i][2]]
                tb = prev_b - int(rng.integers(3, 16))
                ta = nxt_a + int(rng.integers(3, 16))
                if tb >= lo:
                    care = provs[pcp_on(m, W.day(tb))].region
                    add_svc(m, tb, "pcp" if prc == care else ("uc" if rng.random() < 0.5 else "lab_hosp"), prc)
                if ta <= hi:
                    care = provs[pcp_on(m, W.day(ta))].region
                    add_svc(m, ta, "pcp" if nrc == care else ("uc" if rng.random() < 0.55 else "dpcp"), nrc)

        # Pharmacy: maintenance drugs refilled at a local pharmacy, or by mail; long-stayers take a 90-day supply
        # with them in the autumn and fill by mail in the desert.
        nmeds = int(rng_rx.choice([0, 1, 2, 3, 4, 5], p=[0.26, 0.33, 0.24, 0.11, 0.05, 0.01])) if not young else \
            int(rng_rx.choice([0, 1, 2, 3], p=[0.42, 0.33, 0.17, 0.08]))
        meds = [DRUGS[int(i)] for i in rng_rx.choice(len(DRUGS), size=nmeds, replace=False)] if nmeds else []
        home_ph = {}
        for r in W.REGION_CODES:
            lst = ph_byr[r]
            home_ph[r] = lst[int(rng_rx.integers(0, len(lst)))]
        mail_ph = mail[int(rng_rx.integers(0, len(mail)))]
        for med in meds:
            supply90 = rng_rx.random() < 0.93
            t = lo + int(rng_rx.integers(0, 30))
            while t <= hi:
                r_here = W.REGION_CODES[int(m.timeline[t])]
                care = provs[pcp_on(m, W.day(t))].region
                away = r_here != care
                if m.mail_order and (m.kind != "long" or away):
                    ph, days = mail_ph, 90
                elif m.kind == "long" and away:
                    ph, days = mail_ph, 90
                else:
                    ph = home_ph[r_here]
                    days = 90 if supply90 else 30
                    if m.kind == "long" and not away:
                        days = 30
                        # the autumn supply to take south
                        nxt_away = [k for k in range(t + 1, min(hi, t + 30) + 1) if W.REGION_CODES[int(m.timeline[k])] != care]
                        if nxt_away:
                            days = 90
                qty = days * (2 if med[1] in ("METFORMIN HCL", "GABAPENTIN") else 1)
                if med[1] in ("LANTUS SOLOSTAR",):
                    qty = 15 if days >= 90 else 5
                cost = round(med[3] * days / 30.0 * (1 + float(rng_rx.normal(0, 0.03))), 2)
                fills.append(Fill(m.mid, W.day(t), ph.ncpdp, med[0], med[1], med[2], days, qty, cost, r_here))
                t += days - int(rng_rx.integers(0, 6))
        # Acute fills at a local pharmacy, wherever the member is.
        for t in poisson_days(lo, hi, 420 if not young else 600, rng_rx):
            r_here = W.REGION_CODES[int(m.timeline[t])]
            med = ACUTE[int(rng_rx.integers(0, len(ACUTE)))]
            fills.append(Fill(m.mid, W.day(t), home_ph[r_here].ncpdp, med[0], med[1], med[2], 10, 20,
                              round(med[3] * (1 + float(rng_rx.normal(0, 0.05))), 2), r_here))

    # In-home support: a share of members receive regular visits from the agency serving the region they are in.
    for m in wd["members"]:
        lo, hi = enrolled_days(m)
        if hi < lo:
            continue
        p_recv = 0.032 if m.kind not in ("young",) else 0.03
        if rng_hv.random() >= p_recv:
            continue
        per_week = int(rng_hv.choice([1, 2, 3], p=[0.68, 0.26, 0.06]))
        twice_daily = rng_hv.random() < 0.08
        first = lo + int(rng_hv.integers(0, 120))
        last = hi - int(rng_hv.integers(0, 60))
        for wk in range(first, last, 7):
            for k in range(per_week):
                t = wk + int(rng_hv.integers(0, 7))
                if t > hi or t < lo:
                    continue
                rc = W.REGION_CODES[int(m.timeline[t])]
                if rc != m.home and m.kind not in ("early_mover", "late_mover") and not (m.kind == "young" and m.notes):
                    continue  # agencies visit at the address they serve
                ag = byr[rc]["home"]
                npi = ag[0].npi if rng_hv.random() < 0.7 else ag[1].npi
                code = HOME_CODES[int(rng_hv.choice(3, p=[0.62, 0.23, 0.15]))]
                units = int(rng_hv.choice([4, 6, 8, 10, 12, 16, 20, 24], p=[0.2, 0.18, 0.2, 0.12, 0.1, 0.1, 0.06, 0.04]))
                start = "%02d:%02d" % (8 + int(rng_hv.integers(0, 4)), int(rng_hv.choice([0, 15, 30, 45])))
                visits.append(Visit(m.mid, W.day(t), start, npi, code[0], units, rc))
                if twice_daily:
                    start2 = "%02d:%02d" % (15 + int(rng_hv.integers(0, 3)), int(rng_hv.choice([0, 15, 30, 45])))
                    visits.append(Visit(m.mid, W.day(t), start2, npi, code[0], int(rng_hv.choice([4, 6, 8])), rc))
    return svcs, fills, visits
