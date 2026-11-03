"""task402 world: a charity-run NHS Talking Therapies service, April 2024 to March 2026.

Simulates referrals, assessments, stepped-care courses, every care contact with its practitioner,
session-by-session PHQ-9 and GAD-7, the high-intensity workforce (employed and agency) and the agency
booking blocks. Returns the clean truth as pandas frames; pack.py writes the shipped files from it and
adds the Layer 1 forms (record migration, item-level scores, booking extensions as new rows).

Mechanisms (none stated anywhere in the pack):
  A  agency high-intensity cover from May 2025 on 12-week blocks renewed with p=RENEW; when a block lapses
     the therapist leaves and each open course is reallocated to an employed therapist after a gap; the
     patient then disengages with p=Q_HANDOVER, and a patient who stays loses DELTA_HANDOVER of recovery.
     Agency cover takes the longest waiters on the step 3 list.
  B  telephone-first step 2 from 1 April 2025: telephone guided self-help loses PHONE_DELTA of recovery.
  C  the step 3 wait: patients leave the list at WAIT_HAZARD per week waited; no direct effect on a course
     once it has started (WAIT_DIRECT per week, zero by default).
  D  the digital platform switched on 1 July 2025: DIGITAL_DELTA of recovery on courses started after it.
  E  stress management groups withdrawn from 1 September 2025: those patients go to telephone 1:1.
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
COVER_END = date(2025, 12, 19)     # the initiative's funding ends; no block runs past it
PHONE_FIRST = date(2025, 4, 1)
DIGITAL_SWITCH = date(2025, 7, 1)
GROUPS_END = date(2025, 9, 1)

P = dict(
    weekly_referrals=255,
    p_attend_assessment=0.88,
    p_step3=0.30, p_step2=0.55,
    WAIT_HAZARD=0.0030, WAIT_DIRECT=0.0,
    RENEW=0.33, BLOCK_WEEKS=12, AGENCY_CONCURRENT=16,
    Q_HANDOVER=0.60, DELTA_HANDOVER=0.06,
    PHONE_DELTA=0.004, DIGITAL_DELTA=0.050, GROUP_DELTA=0.0,
    s3_dropout_per_session=0.010, s2_dropout_per_session=0.035,
    s3_base_rec=0.585, s2_base_rec=0.535,
)


def _d(x):
    return D0 + timedelta(days=int(x))


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

    # ---------------------------------------------------------------- workforce
    def build_workforce(self):
        r = self.rng
        prac = []
        # step 2 practitioners (psychological wellbeing practitioners)
        for i in range(30):
            prac.append(dict(pid=f"S2-{i:02d}", step=2, kind="employed", start=D0, leave=None))
        # step 3 employed high-intensity therapists; one leaver in FY24 and one in FY25
        for i in range(22):
            prac.append(dict(pid=f"S3E-{i:02d}", step=3, kind="employed", start=D0, leave=None))
        prac[30 + 3]["leave"] = date(2024, 11, 29)
        prac[30 + 11]["leave"] = date(2025, 9, 26)
        # replacements start a month later
        prac.append(dict(pid="S3E-22", step=3, kind="employed", start=date(2025, 1, 6), leave=None))
        prac.append(dict(pid="S3E-23", step=3, kind="employed", start=date(2025, 11, 3), leave=None))
        # one long-standing locum, renewed block after block throughout both years
        blocks = []
        agency = []
        for j, (st, end) in enumerate([(date(2023, 9, 4), None)]):
            pid = f"S3A-{j:02d}"
            agency.append(pid)
            prac.append(dict(pid=pid, step=3, kind="agency", start=st, leave=end))
            # blocks of 12 weeks until leave or beyond FY25
            b0 = st
            k = 0
            while True:
                b1 = b0 + timedelta(weeks=self.p["BLOCK_WEEKS"]) - timedelta(days=1)
                last = end is not None and b1 >= end
                blocks.append(dict(pid=pid, block=k, start=b0, end=min(b1, end) if end else b1))
                if last or b0 > EXTRACT:
                    break
                b0 = b1 + timedelta(days=1)
                k += 1
        # FY25 agency cover: keep AGENCY_CONCURRENT active from AGENCY_START; 12-week blocks renewed with p
        active = {}
        nxt = 1
        day = AGENCY_START
        bw = timedelta(weeks=self.p["BLOCK_WEEKS"])
        while active or day <= COVER_END:
            # top up until four weeks before the programme ends; a block never runs past its end
            while len(active) < self.p["AGENCY_CONCURRENT"] and day + timedelta(weeks=4) <= COVER_END:
                pid = f"S3A-{nxt:02d}"
                nxt += 1
                st = day + timedelta(days=int(r.integers(0, 10)))
                active[pid] = dict(start=st, block_start=st, k=0)
                agency.append(pid)
                prac.append(dict(pid=pid, step=3, kind="agency", start=st, leave=None))
            # advance a week; close blocks that end before it
            day = day + timedelta(weeks=1)
            for pid in list(active):
                a = active[pid]
                bend = min(a["block_start"] + bw - timedelta(days=1), COVER_END)
                if bend < day:
                    blocks.append(dict(pid=pid, block=a["k"], start=a["block_start"], end=bend))
                    renew = r.random() < self.p["RENEW"] and bend < COVER_END
                    if renew:
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
        s3e = [x for x in self.prac.itertuples() if x.step == 3 and x.kind == "employed"]
        s2 = [x.pid for x in self.prac.itertuples() if x.step == 2]
        nweeks = (date(2026, 3, 31) - D0).days // 7 + 1
        ref = 0
        for w in range(nweeks):
            wk = D0 + timedelta(weeks=w)
            season = 1.0 + 0.10 * np.sin(2 * np.pi * (wk.timetuple().tm_yday - 30) / 365.0)
            growth = 1.0 + 0.03 * max(0.0, (wk - date(2025, 4, 1)).days / 365.0)
            n = r.poisson(p["weekly_referrals"] * season * growth)
            for _ in range(n):
                ref += 1
                self.one_referral(ref, wk + timedelta(days=int(r.integers(0, 7))), s2, s3e)
        self.contacts = pd.DataFrame(self.contacts)
        self.scores = pd.DataFrame(self.scores)
        self.referrals = pd.DataFrame(self.referrals)
        self.truth = pd.DataFrame(self.truth)
        return self

    def wait_weeks(self, d):
        """Step 3 wait from assessment to first treatment, by assessment date."""
        r = self.rng
        if d < date(2025, 1, 1):
            m, k = 8.5, 10.0
        elif d < date(2025, 4, 15):
            m, k = 9.0 + 21.0 * (d - date(2025, 1, 1)).days / 104.0, 9.0
        elif d < date(2025, 6, 10):
            m, k = 30.0 - 21.0 * (d - date(2025, 4, 15)).days / 56.0, 9.0
        else:
            m, k = 9.0, 10.0
        return max(2, int(round(r.gamma(k, m / k))))

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
        truth = dict(ref=ref, step=None, wait=None, start=None, pid0=None, agency0=False, broken=False,
                     broken_kind=None, broken_at=None, handover_date=None, cf_rec=None, rec=False,
                     left_list=False, end=None, end_reason=None, n_treat=0, case_first=None, modality=None)
        a_date = rdate + timedelta(days=int(r.integers(6, 29)))
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
        W = self.wait_weeks(a_date)
        truth.update(step=3, wait=W)
        # leaving the list while waiting
        p_start = (1 - p["WAIT_HAZARD"]) ** W
        if r.random() > p_start:
            left = a_date + timedelta(weeks=int(r.integers(2, max(3, W))))
            truth.update(left_list=True, end=left + timedelta(days=14), end_reason="left_waiting_list")
            return
        start = a_date + timedelta(weeks=W)
        # allocation: from May 2025 agency cover takes the longest waiters
        cover = [pid for pid, k in self.kind.items()
                 if k == "agency" and pid != "S3A-00" and self.active_on(pid, start)]
        long_wait = W >= 18
        pid = None
        if long_wait and cover and start >= AGENCY_START and r.random() < 0.99:
            # the waiting list initiative: agency cover takes the backlog
            pid = r.choice(cover)
        elif not long_wait and r.random() < 0.05:
            # the long-standing locum carries an ordinary caseload
            pid = "S3A-00"
        if pid is None:
            emp = [x.pid for x in s3e if self.active_on(x.pid, start)]
            pid = r.choice(emp)
        n_plan = int(np.clip(round(r.normal(11.5, 2.5)), 7, 18))
        base = p["s3_base_rec"] - 0.011 * (phq - 15) - p["WAIT_DIRECT"] * W
        phq1 = int(np.clip(round(phq + r.normal(-0.06 * W, 2.2)), 0, 27))
        gad1 = int(np.clip(round(gad + r.normal(-0.05 * W, 2.0)), 0, 21))
        rec_latent = r.random() < np.clip(base, 0.05, 0.95)
        truth.update(start=start, pid0=pid, agency0=self.kind[pid] == "agency")
        self.course(ref, start, n_plan, 7, "face_to_face" if r.random() < 0.55 else "video", pid, 3,
                    phq1, gad1, rec_latent, truth, p["s3_dropout_per_session"], handover=True)

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
        while i < n_plan:
            # handover check: the therapist leaves before this appointment
            if handover and self.leave.get(cur) is not None and d > self.leave[cur] and not broken:
                lv = self.leave[cur]
                broken = True
                kind = self.kind[cur]
                truth.update(broken=True, broken_kind=kind, broken_at=len(attended), handover_date=lv)
                # counterfactual recovery had the course continued (common random numbers)
                cf = rec_latent if (r.random() > 0) else rec_latent
                emp = [x for x in self.prac.itertuples()
                       if x.step == 3 and x.kind == "employed" and self.active_on(x.pid, lv + timedelta(days=21))]
                cur = r.choice([x.pid for x in emp])
                if kind == "agency":
                    # an agency block lapses at its end date: no joint session, a gap before the new therapist
                    d = lv + timedelta(days=int(r.integers(9, 22)))
                    q, dl = p["Q_HANDOVER"], p["DELTA_HANDOVER"]
                else:
                    # an employed therapist works a notice period and hands over in a joint session
                    d = lv + timedelta(days=int(r.integers(3, 8)))
                    q, dl = 0.03, 0.0
                if r.random() < q:
                    dis_after = True
                elif rec and dl > 0 and r.random() < dl / 0.6:
                    rec = False
            if dis_after:
                # booked with the new therapist, does not attend twice, discharged
                self.add_contact(ref, d, "treatment", mod, "dna", cur, step)
                self.add_contact(ref, d + timedelta(days=7), "treatment", mod, "dna", cur, step)
                end = d + timedelta(days=21)
                truth.update(end=end, end_reason="dropped_out", n_treat=len(attended))
                self.close(truth, attended, phq1, gad1, False, cf)
                return
            # ordinary attendance and dropout
            if r.random() < drop and i > 0:
                self.add_contact(ref, d, "treatment", mod, "dna", cur, step)
                end = d + timedelta(days=21)
                truth.update(end=end, end_reason="dropped_out", n_treat=len(attended))
                self.close(truth, attended, phq1, gad1, False, cf)
                return
            if r.random() < 0.08:
                # cancelled and rebooked a week later
                self.add_contact(ref, d, "treatment", mod, "cancelled_patient", cur, step)
                d = d + timedelta(days=7)
            c = self.add_contact(ref, d, "treatment", mod, "attended", cur, step)
            attended.append(c)
            d = d + timedelta(days=gap)
            i += 1
        end = d - timedelta(days=gap) + timedelta(days=int(r.integers(1, 10)))
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
