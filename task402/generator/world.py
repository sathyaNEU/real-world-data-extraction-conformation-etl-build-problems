"""task402 world: a charity-run NHS Talking Therapies service, October 2023 to March 2026.

Simulates referrals, assessments, stepped-care courses, every care contact with its practitioner,
session-by-session PHQ-9 and GAD-7, the high-intensity workforce (employed and agency) and the agency
booking blocks. Returns the clean truth as pandas frames; pack.py writes the shipped files from it and
adds the Layer 1 forms (record migration, item-level scores, booking extensions as new rows).

Mechanisms (none stated anywhere in the pack):
  A  agency high-intensity cover from May 2025 on 12-week blocks renewed with p=RENEW while a renewed
     block would end by COVER_LAST_END; no new cover after TOPUP_END. When a block lapses the therapist
     leaves and each open course is reallocated to an employed therapist after a gap; the patient then
     disengages with p=Q_HANDOVER, and a patient who stays loses DELTA_HANDOVER of recovery.
     Agency cover takes the backlog cohort (step 3 patients assessed October 2024 to early April 2025
     whose wait ran past 18 weeks), cleared longest-first between INTAKE_START and INTAKE_END.
  B  telephone-first step 2 from 1 April 2025: telephone guided self-help loses PHONE_DELTA of recovery.
  C  the step 3 wait: patients leave the list at WAIT_HAZARD per week waited; no direct effect on a course
     once it has started (WAIT_DIRECT per week, zero by default; score drift while waiting is independent
     of the wait's length).
  D  the digital platform switched on 1 July 2025: DIGITAL_DELTA of recovery on courses started after it.
  E  stress management groups withdrawn from 1 September 2025: those patients go to telephone 1:1.
  Season: appointments in the two weeks either side of the new year carry HOLIDAY_MULT times the
  ordinary dropout hazard, in both years and at both steps.
"""
import numpy as np
import pandas as pd
from datetime import date, timedelta

SEED = 402
D0 = date(2023, 10, 2)            # first referral date simulated (a Monday)
FY24 = (date(2024, 4, 1), date(2025, 3, 31))
FY25 = (date(2025, 4, 1), date(2026, 3, 31))
EXTRACT = date(2026, 5, 6)
MIGRATION = date(2025, 10, 13)
AGENCY_START = date(2025, 5, 5)
INTAKE_START = date(2025, 5, 12)    # first allocation of the backlog cohort to agency cover
INTAKE_END = date(2025, 8, 22)      # last allocation (the backlog is cleared)
TOPUP_END = date(2025, 8, 22)       # no new agency therapist starts after this
COVER_LAST_END = date(2025, 11, 14) # no block is renewed to end after this
COVER_END = date(2025, 12, 19)      # the initiative's funding end; no block reaches it
COH_A0 = date(2024, 10, 7)          # backlog cohort: first assessment date
COH_A1 = date(2025, 4, 4)           # backlog cohort: last assessment date
PHONE_FIRST = date(2025, 4, 1)
DIGITAL_SWITCH = date(2025, 7, 1)
GROUPS_END = date(2025, 9, 1)
HOLIDAYS = [(date(2023, 12, 18), date(2024, 1, 14)), (date(2024, 12, 16), date(2025, 1, 12)),
            (date(2025, 12, 15), date(2026, 1, 11))]

P = dict(
    weekly_referrals=255,
    p_attend_assessment=0.88,
    p_step3=0.30, p_step2=0.55,
    WAIT_HAZARD=0.0030, WAIT_HAZARD_LONG=0.020, WAIT_DIRECT=0.0,
    RENEW=0.45, BLOCK_WEEKS=12, AGENCY_CONCURRENT=32, N_S3E=40,
    LOCUM_SHARE=0.025, SURGE=0.45, COHORT_PEAK=0.42, COVER_SHARE=0.996, FIFO=True, RENEW_FIRST=0.4, ALLOC_WIN=84, ALLOC_TRAIL=True,
    intake_end=INTAKE_END, topup_end=TOPUP_END, cover_last_end=COVER_LAST_END, stagger=70,
    Q_HANDOVER=0.62, DELTA_HANDOVER=0.06,
    PHONE_DELTA=0.004, DIGITAL_DELTA=0.050, GROUP_DELTA=0.0,
    s3_dropout_per_session=0.003, s2_dropout_per_session=0.035, s3_first_dna=0.07,
    HOLIDAY_MULT=7.0,
    s3_base_rec=0.585, s2_base_rec=0.535,
)


BANK = {date(2023, 12, 25), date(2023, 12, 26), date(2024, 1, 1), date(2024, 3, 29), date(2024, 4, 1),
        date(2024, 5, 6), date(2024, 5, 27), date(2024, 8, 26), date(2024, 12, 25), date(2024, 12, 26),
        date(2025, 1, 1), date(2025, 4, 18), date(2025, 4, 21), date(2025, 5, 5), date(2025, 5, 26),
        date(2025, 8, 25), date(2025, 12, 25), date(2025, 12, 26), date(2026, 1, 1)}
WEEK = (0, 1, 2, 3, 4)
PATTERNS = [((0, 1, 2, 3, 4), 0.62), ((0, 1, 2, 3), 0.22), ((1, 2, 3, 4), 0.16)]


def in_holiday(d):
    return any(a <= d <= b for a, b in HOLIDAYS)


class World:
    def __init__(self, seed=SEED, **over):
        self.p = dict(P)
        self.p.update(over)
        self.rng = np.random.default_rng(seed)
        self.contacts = []      # dicts
        self.scores = []
        self.referrals = []
        self.truth = []         # per referral truth row
        self.cid = 0
        self.alloc = {}
        self.pattern = {}

    # ---------------------------------------------------------------- workforce
    def build_workforce(self):
        r = self.rng
        p = self.p
        prac = []
        # step 2 practitioners (psychological wellbeing practitioners)
        for i in range(34):
            prac.append(dict(pid=f"S2-{i:02d}", step=2, kind="employed", start=D0, leave=None))
        # step 3 employed high-intensity therapists; one leaver in each year, each replaced
        n3 = p["N_S3E"]
        for i in range(n3):
            prac.append(dict(pid=f"S3E-{i:02d}", step=3, kind="employed", start=D0, leave=None))
        prac[34 + 3]["leave"] = date(2024, 11, 29)
        prac[34 + 11]["leave"] = date(2025, 9, 26)
        prac.append(dict(pid=f"S3E-{n3:02d}", step=3, kind="employed", start=date(2025, 1, 6), leave=None))
        prac.append(dict(pid=f"S3E-{n3 + 1:02d}", step=3, kind="employed", start=date(2025, 11, 3), leave=None))
        blocks = []
        agency = []
        # one long-standing locum, renewed block after block throughout both years
        pid = "S3A-00"
        agency.append(pid)
        st = date(2023, 9, 4)
        prac.append(dict(pid=pid, step=3, kind="agency", start=st, leave=None))
        b0, k = st, 0
        while b0 <= EXTRACT:
            b1 = b0 + timedelta(weeks=p["BLOCK_WEEKS"]) - timedelta(days=1)
            blocks.append(dict(pid=pid, block=k, start=b0, end=b1))
            b0, k = b1 + timedelta(days=1), k + 1
        # the 2025-26 waiting list initiative: keep AGENCY_CONCURRENT active, starts staggered over the
        # first six weeks; 12-week blocks renewed with p while the renewed block ends by COVER_LAST_END
        bw = timedelta(weeks=p["BLOCK_WEEKS"])
        active = {}
        nxt = 1
        day = AGENCY_START
        first_wave = True
        while active or day <= p["topup_end"]:
            while len(active) < p["AGENCY_CONCURRENT"] and day <= p["topup_end"]:
                pid = f"S3A-{nxt:02d}"
                nxt += 1
                lo, hi = (0, p["stagger"]) if first_wave else (3, 17)
                wkdays = [day + timedelta(days=k) for k in range(lo, hi)
                          if (day + timedelta(days=k)).weekday() < 5 and (day + timedelta(days=k)) not in BANK]
                st = wkdays[int(r.integers(0, len(wkdays)))]       # bookings start on a working day
                u = r.random()
                acc = 0.0
                for pat, w in PATTERNS:
                    acc += w
                    if u < acc:
                        break
                self.pattern[pid] = pat
                active[pid] = dict(block_start=st, k=0)
                agency.append(pid)
                prac.append(dict(pid=pid, step=3, kind="agency", start=st, leave=None))
            first_wave = False
            day = day + timedelta(weeks=1)
            for pid in list(active):
                a = active[pid]
                bend = a["block_start"] + bw - timedelta(days=1)
                if bend < day:
                    blocks.append(dict(pid=pid, block=a["k"], start=a["block_start"], end=bend))
                    nend = bend + bw
                    pr_renew = p["RENEW_FIRST"] if a["k"] == 0 else p["RENEW"]
                    if r.random() < pr_renew and nend <= p["cover_last_end"]:
                        a["block_start"] = bend + timedelta(days=1)
                        a["k"] += 1
                    else:
                        for pr in prac:
                            if pr["pid"] == pid:
                                pr["leave"] = bend
                        del active[pid]
        self.prac = pd.DataFrame(prac)
        self.blocks = pd.DataFrame(blocks)
        self.leave = {row.pid: row.leave for row in self.prac.itertuples()}
        self.kind = {row.pid: row.kind for row in self.prac.itertuples()}
        self.start = {row.pid: row.start for row in self.prac.itertuples()}

    def shift(self, d, pid=None):
        """The next day on or after d that the practitioner works (bank holidays excepted)."""
        pat = self.pattern.get(pid, WEEK)
        while d.weekday() not in pat or d in BANK:
            d = d + timedelta(days=1)
        return d

    def active_on(self, pid, d):
        lv = self.leave[pid]
        return self.start[pid] <= d and (lv is None or d <= lv)

    # ---------------------------------------------------------------- one referral
    def add_contact(self, ref, d, ctype, modality, attend, pid, step):
        self.cid += 1
        hh = int(self.rng.choice([9, 10, 11, 12, 13, 14, 15, 16, 17]))
        self.contacts.append(dict(cid=self.cid, ref=ref, date=d, hour=hh, ctype=ctype, modality=modality,
                                  attend=attend, pid=pid, step=step))
        return self.cid

    def run(self):
        r = self.rng
        p = self.p
        self.build_workforce()
        self.intake_weights()
        s3e =[x for x in self.prac.itertuples() if x.step == 3 and x.kind == "employed"]
        s2 = [x.pid for x in self.prac.itertuples() if x.step == 2]
        nweeks = (date(2026, 3, 31) - D0).days // 7 + 1
        ref = 0
        for w in range(nweeks):
            wk = D0 + timedelta(weeks=w)
            season = 1.0 + 0.10 * np.sin(2 * np.pi * (wk.timetuple().tm_yday - 30) / 365.0)
            growth = 1.0 + 0.03 * max(0.0, (wk - date(2025, 4, 1)).days / 365.0)
            n = r.poisson(p["weekly_referrals"] * season * growth * self.surge(wk))
            for _ in range(n):
                ref += 1
                self.one_referral(ref, wk + timedelta(days=int(r.integers(0, 7))), s2, s3e)
        self.contacts = pd.DataFrame(self.contacts)
        self.scores = pd.DataFrame(self.scores)
        self.referrals = pd.DataFrame(self.referrals)
        self.truth = pd.DataFrame(self.truth)
        return self

    def surge(self, wk):
        """The winter's rise in referrals (self-referral publicity from October 2024), easing through March."""
        a, b, c, d = date(2024, 9, 23), date(2024, 11, 4), date(2025, 2, 17), date(2025, 4, 14)
        if wk < a or wk > d:
            return 1.0
        x = 1.0 if b <= wk <= c else ((wk - a).days / (b - a).days if wk < b else (d - wk).days / (d - c).days)
        return 1.0 + self.p["SURGE"] * x

    def intake_weights(self):
        """Initiative starts per day follow the agency therapists in post that day (allocation meetings
        fill the slots the cover has); a cohort member's chance of a long wait follows the slots open to
        them between 18 and 33 weeks after assessment, so the wait is independent of the start date."""
        p = self.p
        days = (p["intake_end"] - INTAKE_START).days + 1
        cover = [x for x, k in self.kind.items() if k == "agency" and x != "S3A-00"]
        wt = np.array([sum(1 for x in cover if self.active_on(x, INTAKE_START + timedelta(days=i)))
                       for i in range(days)], dtype=float)
        self.iw = wt
        self.iw_cum = np.concatenate([[0.0], np.cumsum(wt)])
        a0 = INTAKE_START - timedelta(weeks=33)
        a1 = p["intake_end"] - timedelta(weeks=18)
        best = 0.0
        d = a0
        while d <= a1:
            best = max(best, self.window_weight(d)[2])
            d += timedelta(days=1)
        self.iw_best = best

    def window_weight(self, d):
        lo = max(INTAKE_START, d + timedelta(weeks=18))
        hi = min(self.p["intake_end"], d + timedelta(weeks=33))
        if lo > hi:
            return None, None, 0.0
        i0, i1 = (lo - INTAKE_START).days, (hi - INTAKE_START).days
        return i0, i1, float(self.iw_cum[i1 + 1] - self.iw_cum[i0])

    def wait_weeks(self, d):
        """Step 3 wait in weeks from assessment to first treatment, and whether the patient is in the
        backlog cohort the initiative clears (no wait past 33 weeks)."""
        r = self.rng
        p = self.p
        if p["FIFO"]:
            # the longest waiters first: cohort members start in assessment order, the intake following
            # the slots the cover has; nobody waits past 33 weeks
            a0 = INTAKE_START - timedelta(weeks=33)
            a1 = p["intake_end"] - timedelta(weeks=18)
            if a0 <= d <= a1 and r.random() < p["COHORT_PEAK"]:
                x = (d - a0).days / (a1 - a0).days
                tgt = x * self.iw_cum[-1]
                j = int(np.searchsorted(self.iw_cum, tgt))
                s = INTAKE_START + timedelta(days=max(0, j - 1) + int(r.integers(-5, 6)))
                s = min(max(s, INTAKE_START), p["intake_end"])
                wk = (s - d).days / 7.0
                if 18 <= wk <= 33:
                    return int(round(wk)), True, s
        i0, i1, wsum = self.window_weight(d) if not p["FIFO"] else (None, None, 0.0)
        if wsum > 0 and r.random() < p["COHORT_PEAK"] * wsum / self.iw_best:
            seg = self.iw[i0:i1 + 1]
            j = int(r.choice(len(seg), p=seg / seg.sum()))
            s = INTAKE_START + timedelta(days=i0 + j)
            return int(round((s - d).days / 7.0)), True, s
        m = 8.5 if d < date(2025, 1, 1) else 9.0
        while True:
            W = max(2, int(round(r.gamma(10.0, m / 10.0))))
            if W <= 17:
                return W, False, None

    def pick(self, pool, start):
        """Allocate to the practitioner in the pool with the fewest courses starting within twelve weeks
        either side (the allocation meeting balances caseloads); ties broken at random."""
        best, cands = None, []
        for pid in pool:
            lst = self.alloc.setdefault(pid, [])
            hi = 0 if self.p["ALLOC_TRAIL"] else self.p["ALLOC_WIN"]
            n = sum(1 for s in lst if -self.p["ALLOC_WIN"] <= (s - start).days <= hi)
            if best is None or n < best:
                best, cands = n, [pid]
            elif n == best:
                cands.append(pid)
        pid = cands[int(self.rng.integers(0, len(cands)))]
        self.alloc[pid].append(start)
        return pid

    def scores_at(self, phq0, gad0, t, n, rec, first_case):
        """Trajectory value at treatment index t of n (0-based) ending recovered or not."""
        r = self.rng
        if n <= 1:
            frac = 0.0
        else:
            frac = t / (n - 1)
        if rec:
            phq_end = int(r.integers(2, 10))
            gad_end = int(r.integers(1, 8))
        else:
            # at least one measure at or above caseness at the end
            phq_end = int(r.integers(9, 19))
            gad_end = int(r.integers(7, 16))
            if phq_end < 10 and gad_end < 8:
                gad_end = 8 + int(r.integers(0, 4))
        phq = phq0 + (phq_end - phq0) * frac + r.normal(0, 1.2) * (0 < t < n - 1)
        gad = gad0 + (gad_end - gad0) * frac + r.normal(0, 1.0) * (0 < t < n - 1)
        return int(np.clip(round(phq), 0, 27)), int(np.clip(round(gad), 0, 21))

    def one_referral(self, ref, rdate, s2, s3e):
        r = self.rng
        p = self.p
        patient = int(r.integers(10 ** 9, 10 ** 10 - 1))
        age = int(np.clip(r.normal(39, 14), 18, 89))
        phq = int(np.clip(round(r.normal(15.5, 4.8)), 0, 27))
        gad = int(np.clip(round(0.62 * phq + r.normal(4.0, 3.0)), 0, 21))
        rowref = dict(ref=ref, patient=patient, received=rdate, age=age)
        truth = dict(ref=ref, step=None, wait=None, cohort=False, start=None, pid0=None, agency0=False,
                     broken=False, broken_kind=None, broken_at=None, handover_date=None, cf_rec=None,
                     cf_end=None, rec=False, left_list=False, left_date=None, a_date=None, end=None,
                     end_reason=None, n_treat=0, case_first=None, modality=None)
        a_date = self.shift(rdate + timedelta(days=int(r.integers(6, 29))))
        truth["a_date"] = a_date
        if r.random() > p["p_attend_assessment"]:
            self.add_contact(ref, a_date, "assessment", "phone", "dna", r.choice(s2), 2)
            end = a_date + timedelta(days=21)
            truth.update(end=end, end_reason="assessment_dna")
            self.finish(rowref, truth)
            return
        pa = r.choice(s2)
        c = self.add_contact(ref, a_date, "assessment", "phone", "attended", pa, 2)
        self.scores.append(dict(cid=c, phq9=phq, gad7=gad))
        u = r.random()
        if u < p["p_step3"] or phq >= 21:
            self.step3(ref, a_date, phq, gad, truth, s3e)
        elif u < p["p_step3"] + p["p_step2"]:
            self.step2(ref, a_date, phq, gad, truth, s2)
        else:
            truth.update(end=a_date + timedelta(days=int(r.integers(1, 15))), end_reason="signposted")
        self.finish(rowref, truth)

    def finish(self, rowref, truth):
        rowref["end"] = truth["end"]
        rowref["end_reason"] = truth["end_reason"]
        self.referrals.append(rowref)
        self.truth.append(truth)

    # ---------------------------------------------------------------- step 2
    def step2(self, ref, a_date, phq, gad, truth, s2):
        r = self.rng
        p = self.p
        start = a_date + timedelta(weeks=int(r.integers(2, 8)))
        u = r.random()
        if start >= PHONE_FIRST:
            if u < 0.17:
                mod = "digital"
            elif u < 0.24:
                # groups until September 2025, then telephone 1:1
                mod = "group" if start < GROUPS_END else "phone"
            elif u < 0.42:
                mod = r.choice(["video", "face_to_face"])
            else:
                mod = "phone"
        else:
            if u < 0.16:
                mod = "digital"
            elif u < 0.24:
                mod = "group"
            elif u < 0.52:
                mod = "phone"
            else:
                mod = r.choice(["video", "face_to_face"])
        n_plan = {"digital": int(r.integers(4, 7)), "group": 6}.get(mod, int(r.integers(5, 8)))
        gap = 14 if mod == "digital" else 7
        pid = r.choice(s2)
        base = p["s2_base_rec"] - 0.012 * (phq - 15)
        if mod == "phone" and start >= PHONE_FIRST:
            base -= p["PHONE_DELTA"]
        if mod == "digital" and start >= DIGITAL_SWITCH:
            base -= p["DIGITAL_DELTA"]
        # first-treatment scores drift a little during the short wait
        phq1 = int(np.clip(round(phq + r.normal(-0.6, 2.0)), 0, 27))
        gad1 = int(np.clip(round(gad + r.normal(-0.5, 1.8)), 0, 21))
        rec_latent = r.random() < np.clip(base, 0.05, 0.95)
        self.course(ref, start, n_plan, gap, mod, pid, 2, phq1, gad1, rec_latent, truth,
                    p["s2_dropout_per_session"], handover=None)
        truth.update(step=2, modality=mod, start=start, pid0=pid)

    # ---------------------------------------------------------------- step 3
    def step3(self, ref, a_date, phq, gad, truth, s3e):
        r = self.rng
        p = self.p
        W, cohort, s = self.wait_weeks(a_date)
        truth.update(step=3, wait=W, cohort=cohort)
        # leaving the list while waiting: a weekly hazard, heavier once the wait passes 18 weeks
        for wk in range(1, W):
            h = p["WAIT_HAZARD"] if wk < 18 else p["WAIT_HAZARD_LONG"]
            if r.random() < h:
                left = a_date + timedelta(weeks=wk, days=int(r.integers(0, 7)))
                truth.update(left_list=True, left_date=left, end=left + timedelta(days=14),
                             end_reason="left_waiting_list")
                return
        start = s if cohort else a_date + timedelta(weeks=W)
        mod = "face_to_face" if r.random() < 0.55 else "video"
        pid = None
        start = self.shift(start)
        cover = [x for x, k in self.kind.items() if k == "agency" and x != "S3A-00" and self.active_on(x, start)
                 and start.weekday() in self.pattern.get(x, WEEK)]
        if cohort and cover and r.random() < p["COVER_SHARE"]:
            # the waiting list initiative: agency cover takes the backlog cohort
            pid = self.pick(cover, start)
        elif not cohort and r.random() < p["LOCUM_SHARE"]:
            # the long-standing locum carries an ordinary caseload
            pid = "S3A-00"
        if pid is None:
            emp = [x.pid for x in s3e if self.active_on(x.pid, start)]
            pid = self.pick(emp, start)
        # booked first treatment appointment not attended: discharged, never entered treatment
        start = self.shift(start, pid)
        if r.random() < p["s3_first_dna"]:
            self.add_contact(ref, start, "treatment", mod, "dna", pid, 3)
            truth.update(start=start, pid0=pid, end=start + timedelta(days=21), end_reason="not_entered",
                         n_treat=0)
            return
        n_plan = int(np.clip(round(r.normal(11.5, 2.5)), 7, 18))
        base = p["s3_base_rec"] - 0.011 * (phq - 15) - p["WAIT_DIRECT"] * W
        phq1 = int(np.clip(round(phq + r.normal(-0.5, 2.2)), 0, 27))
        gad1 = int(np.clip(round(gad + r.normal(-0.4, 2.0)), 0, 21))
        rec_latent = r.random() < np.clip(base, 0.05, 0.95)
        truth.update(start=start, pid0=pid, agency0=self.kind[pid] == "agency")
        self.course(ref, start, n_plan, 7, mod, pid, 3, phq1, gad1, rec_latent, truth,
                    p["s3_dropout_per_session"], handover=True)

    # ---------------------------------------------------------------- a course
    def course(self, ref, start, n_plan, gap, mod, pid, step, phq1, gad1, rec_latent, truth, drop, handover):
        r = self.rng
        p = self.p
        d = start
        attended = []
        cur = pid
        broken = False
        dis_after = False
        rec = rec_latent
        i = 0
        cf = None
        last = d
        while i < n_plan:
            dd = self.shift(d, cur)
            # handover check: the therapist leaves before this appointment
            if handover and self.leave.get(cur) is not None and dd > self.leave[cur] and not broken:
                lv = self.leave[cur]
                broken = True
                kind = self.kind[cur]
                # the counterfactual end had the course run on with its own therapist
                cf_end = dd + timedelta(days=gap * (n_plan - i - 1)) + timedelta(days=5)
                truth.update(broken=True, broken_kind=kind, broken_at=len(attended), handover_date=lv,
                             cf_end=cf_end)
                cf = rec_latent
                emp = [x.pid for x in self.prac.itertuples()
                       if x.step == 3 and x.kind == "employed" and self.active_on(x.pid, lv + timedelta(days=21))]
                cur = self.pick(emp, lv)
                if kind == "agency":
                    # an agency block lapses at its end date: no joint session, a gap before the new therapist
                    d = lv + timedelta(days=int(r.integers(9, 22)))
                    q, dl = p["Q_HANDOVER"], p["DELTA_HANDOVER"]
                else:
                    # an employed therapist works a notice period and hands over in a joint session
                    d = lv + timedelta(days=int(r.integers(3, 8)))
                    q, dl = 0.03, 0.0
                dd = self.shift(d, cur)
                if r.random() < q:
                    dis_after = True
                elif rec and dl > 0 and r.random() < dl / 0.6:
                    rec = False
            if dis_after:
                # booked with the new therapist, does not attend twice, discharged
                self.add_contact(ref, dd, "treatment", mod, "dna", cur, step)
                self.add_contact(ref, self.shift(d + timedelta(days=7), cur), "treatment", mod, "dna", cur, step)
                end = dd + timedelta(days=21)
                truth.update(end=end, end_reason="dropped_out", n_treat=len(attended))
                self.close(truth, attended, phq1, gad1, False, cf)
                return
            # ordinary attendance and dropout (more of it over the new year)
            dr = drop * (p["HOLIDAY_MULT"] if in_holiday(dd) else 1.0)
            if r.random() < dr and i > 0:
                self.add_contact(ref, dd, "treatment", mod, "dna", cur, step)
                end = dd + timedelta(days=21)
                truth.update(end=end, end_reason="dropped_out", n_treat=len(attended))
                self.close(truth, attended, phq1, gad1, False, cf)
                return
            if r.random() < 0.08:
                # cancelled and rebooked a week later
                self.add_contact(ref, dd, "treatment", mod, "cancelled_patient", cur, step)
                d = d + timedelta(days=7)
                dd = self.shift(d, cur)
                if handover and self.leave.get(cur) is not None and dd > self.leave[cur] and not broken:
                    continue
            c = self.add_contact(ref, dd, "treatment", mod, "attended", cur, step)
            attended.append(c)
            last = dd
            d = d + timedelta(days=gap)
            i += 1
        end = last + timedelta(days=int(r.integers(1, 10)))
        truth.update(end=end, end_reason="completed", n_treat=len(attended))
        self.close(truth, attended, phq1, gad1, rec, cf)

    def close(self, truth, attended, phq1, gad1, rec, cf):
        n = len(attended)
        truth["n_treat"] = n
        truth["rec"] = bool(rec) and n >= 2
        truth["cf_rec"] = cf
        truth["case_first"] = (phq1 >= 10 or gad1 >= 8) if n >= 1 else None
        # scores at each attended treatment appointment
        for t, c in enumerate(attended):
            if t == 0:
                ph, ga = phq1, gad1
            else:
                ph, ga = self.scores_at(phq1, gad1, t, n, rec and (phq1 >= 10 or gad1 >= 8), True)
            self.scores.append(dict(cid=c, phq9=ph, gad7=ga))


def simulate(seed=SEED, **over):
    return World(seed, **over).run()


if __name__ == "__main__":
    import time
    t = time.time()
    w = simulate()
    print("referrals", len(w.referrals), "contacts", len(w.contacts), "scores", len(w.scores),
          "agency", (w.prac.kind == "agency").sum(), "blocks", len(w.blocks), "secs", round(time.time() - t, 1))
