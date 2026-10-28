"""task179 world: the clean truth before any export layout, code or clock is applied.

Region 4 of the Merrow Department of Corrections supervises felony probationers and parolees in Darrow County
(with the City of Halverton) and Keswick County. The simulation runs by month from 2013 to 2027: intakes, terms,
closures, the bookings of supervisees into the two county jails, the violent victimizations the Halverton police
record (of supervisees and of everyone else in the city), the risk assessments, the programme referrals and the
GPS devices Belvantis runs for the Region. 2027 is simulated only to check the forecast against an outcome nobody
ships.

Generator truth, never shipped: a supervisee recorded as the victim of a violent incident is booked on violent
and firearm charges at a raised rate for about two years, starting about two months after the incident, and from
July 2026 a conflict among young men on the caseload in Halverton raised their victimization several times over,
tapering by December."""
from __future__ import annotations

import datetime as dt

import numpy as np

import codes as K
import common as C
import names as NM

P = dict(
    intake=290.0, n0=7400, male=0.83, parole=0.27, darrow=0.72, city_in_darrow=0.80,
    hr_vw=10.0, hr_other=1.3, lag=3, elev=24,
    surge=(8.0, 12.0, 8.0, 1.5), surge_m0=9, net_age=42, net_share=0.90,
    b_other=-4.42, b_vw=-6.88, b_vict=-5.62,
    revoke_new=0.28, revoke_vw=0.40, tech=0.0028, early=0.012, out_region=0.0012, county_move=0.0020,
    death=0.0003, reentry=0.35, concurrent=0.04,
)
TREND = {2013: 1.0, 2014: 1.0, 2015: 1.0, 2016: 0.99, 2017: 1.0, 2018: 1.0, 2019: 1.02, 2020: 1.12, 2021: 1.24,
         2022: 1.18, 2023: 1.08, 2024: 1.02, 2025: 0.98, 2026: 0.95, 2027: 0.95}
SEASON = np.array([0.86, 0.82, 0.92, 0.97, 1.05, 1.10, 1.16, 1.14, 1.05, 1.00, 0.95, 0.98])
SEASON = SEASON / SEASON.mean()
FAMILIES = ["VIOLENT", "WEAPON", "PROPERTY", "DRUG", "DUI", "OTHER"]
FAM_P = [0.20, 0.07, 0.27, 0.26, 0.08, 0.12]
OFF_O = np.array([0.25, 0.30, 0.20, 0.15, -0.35, 0.0])
OFF_V = np.array([0.55, 0.60, -0.10, -0.05, -0.50, 0.0])
DIST_P = [0.28, 0.24, 0.18, 0.17, 0.13]
M_END = C.month_index(dt.date(2027, 12, 1))
M0 = C.month_index(C.SIM_START)


def covid(mi):
    y, m = mi // 12, mi % 12 + 1
    if y == 2020 and m in (4, 5):
        return 0.55
    if y == 2020 and m in (6, 7):
        return 0.80
    return 1.0


class World:
    def __init__(self, params=None):
        self.p = dict(P)
        if params:
            self.p.update(params)
        self.r_people = C.stream("people")
        self.r_month = C.stream("months")
        self.r_days = C.stream("days")
        self._people()
        self._simulate()
        self._episodes_table()

    # ------------------------------------------------------------------ people
    def _people(self):
        p, r = self.p, self.r_people
        starts = []
        n0 = p["n0"]
        starts += list(M0 - r.integers(0, 48, n0))
        for mi in range(M0, M_END + 1):
            starts += [mi] * int(r.poisson(p["intake"]))
        n = len(starts)
        self.N = n
        self.first_start = np.array(starts)
        self.male = r.random(n) < p["male"]
        age0 = np.minimum(18 + r.gamma(2.1, 6.5, n), 72.0)
        self.age0 = age0
        race = r.choice(4, n, p=[0.48, 0.36, 0.12, 0.04])
        self.race = race
        self.hispanic = race == 2
        self.priors = r.negative_binomial(1.3, 0.30, n)
        self.fam = r.choice(6, n, p=FAM_P)
        self.parole0 = r.random(n) < p["parole"]
        u = r.random(n)
        self.county0 = np.where(u < p["darrow"], 0, 1)
        self.city = (self.county0 == 0) & (r.random(n) < p["city_in_darrow"])
        self.dist = np.where(self.city, r.choice(5, n, p=DIST_P) + 1, 0)
        self.frail = r.normal(0, 0.55, n)
        self.fv = 0.6 * self.frail + r.normal(0, 0.40, n)
        # dates of birth: the intake day less the age at intake
        day0 = np.array([C.month_start(m) for m in starts], dtype="datetime64[D]") + r.integers(0, 28, n)
        self.dob = day0 - (age0 * 365.25).astype(int)
        self.net_u = r.random(n)
        self.sub_u = r.random(n)          # residence and name variation draws
        lead = []
        for i in range(n):
            fam = FAMILIES[self.fam[i]]
            lead.append(K.BY_FAMILY[fam][r.integers(len(K.BY_FAMILY[fam]))])
        self.lead0 = lead

    def age_at(self, mi):
        return self.age0 + (mi - self.first_start) / 12.0

    # ------------------------------------------------------------------ months
    def _simulate(self):
        p, r = self.p, self.r_month
        n = self.N
        start = self.first_start.copy()
        active = np.zeros(n, bool)
        sched_end = np.zeros(n, int)
        parole = self.parole0.copy()
        county = self.county0.copy()
        ep_no = np.zeros(n, int)
        pending = np.full(n, -1)          # month a re-entry episode starts
        last_v = np.full(n, -10 ** 6)
        prev_s = np.full(n, -10 ** 6)
        prev_e = np.full(n, -10 ** 6)
        close_at = np.full(n, 10 ** 9)    # month a decided closure takes effect
        close_why = np.array([""] * n, dtype=object)
        self.vict = []        # (person, month)
        self.book = []        # (person, month, kind) kind: VW, NC (new charge, not B), WT, PV
        self.epis = []        # (person, ep_no, start_m, end_m, why, county, parole, sched_end)
        self.moves = []       # (person, month, from_county, to_county)
        net_ok = self.city & self.male & ((self.fam == 0) | (self.fam == 1) | (self.priors >= 1))
        self.net_ok = net_ok
        open_ep = {}
        for mi in range(M0 - 48, M_END + 1):
            y, mo = mi // 12, mi % 12 + 1
            # starts
            st = np.where(((start == mi) & (ep_no == 0)) | (pending == mi))[0]
            for i in st:
                if pending[i] == mi:
                    parole[i] = True
                    pending[i] = -1
                active[i] = True
                if parole[i]:
                    term = int(r.integers(12, 37))
                else:
                    term = int(r.choice([24, 36, 48, 60], p=[0.35, 0.35, 0.15, 0.15]))
                sched_end[i] = mi + term
                ep_no[i] += 1
                close_at[i] = 10 ** 9
                open_ep[i] = (mi, county[i], parole[i], mi + term, ep_no[i])
            idx = np.where(active)[0]
            if len(idx) == 0:
                continue
            age = self.age_at(mi)[idx]
            fam = self.fam[idx]
            lpri = np.log1p(self.priors[idx])
            # victimization
            vl = (p["b_vict"] + 0.35 * self.male[idx] - 0.040 * (age - 30) + 0.15 * lpri
                  + np.where((fam == 0) | (fam == 1), 0.35, 0.0) + self.fv[idx]
                  + np.log(TREND.get(y, 1.0) * SEASON[mo - 1]) + np.where(self.city[idx] & (county[idx] == 0), 0.0, -0.9))
            if y == 2026 and mo >= p["surge_m0"]:
                k = mo - p["surge_m0"]
                if k < len(p["surge"]):
                    net = net_ok[idx] & (age < p["net_age"]) & (self.net_u[idx] < p["net_share"]) & (county[idx] == 0)
                    vl = vl + np.where(net, np.log(p["surge"][k]), 0.0)
            hit = idx[r.random(len(idx)) < 1 - np.exp(-np.exp(vl))]
            for i in hit:
                self.vict.append((i, mi))
            # raised booking hazard from earlier victimizations
            dl = mi - last_v[idx]
            elev = ((dl >= p["lag"]) & (dl < p["lag"] + p["elev"])) | ((mi >= prev_s[idx]) & (mi < prev_e[idx]))
            # update victimization trackers after reading this month's elevation
            if len(hit):
                ps = last_v[hit] + p["lag"]
                pe = last_v[hit] + p["lag"] + p["elev"]
                keep = prev_e[hit] > ps
                prev_s[hit] = np.where(keep, np.minimum(prev_s[hit], ps), ps)
                prev_e[hit] = np.maximum(prev_e[hit], pe)
                last_v[hit] = mi
            tos = mi - np.array([open_ep[i][0] for i in idx])
            tos_t = np.where(tos < 6, 0.35, np.where(tos < 12, 0.15, 0.0))
            cv = covid(mi)
            lo = (p["b_other"] + 0.50 * self.male[idx] - 0.030 * (age - 30) + 0.28 * lpri + OFF_O[fam] + 0.12 * parole[idx]
                  + np.where(self.city[idx] & (county[idx] == 0), 0.10, np.where(county[idx] == 0, -0.10, 0.0))
                  + self.frail[idx] + tos_t + np.where(elev, np.log(p["hr_other"]), 0.0))
            lv = (p["b_vw"] + 0.80 * self.male[idx] - 0.045 * (age - 30) + 0.30 * lpri + OFF_V[fam] + 0.10 * parole[idx]
                  + np.where(self.city[idx] & (county[idx] == 0), 0.20, np.where(county[idx] == 0, -0.10, 0.0))
                  + self.frail[idx] + 0.85 * tos_t + np.where(elev, np.log(p["hr_vw"]), 0.0))
            po = (1 - np.exp(-np.exp(lo))) * cv
            pv = (1 - np.exp(-np.exp(lv))) * cv
            u = r.random(len(idx))
            vw = idx[u < pv]
            nc = idx[(u >= pv) & (u < pv + po)]
            for i in vw:
                self.book.append((i, mi, "VW"))
            for i in nc:
                self.book.append((i, mi, "NC"))
            # bookings that are not new charges
            u2 = r.random(len(idx))
            wt = idx[u2 < 0.0040 * cv]
            pvh = idx[(u2 >= 0.0040 * cv) & (u2 < 0.0092 * cv)]
            for i in wt:
                self.book.append((i, mi, "WT"))
            for i in pvh:
                self.book.append((i, mi, "PV"))
            # closures decided this month
            rv = np.concatenate([vw[r.random(len(vw)) < p["revoke_vw"]], nc[r.random(len(nc)) < p["revoke_new"]]])
            for i in rv:
                if close_at[i] > mi + 1:
                    close_at[i] = mi + 1 + int(r.integers(0, 4))
                    close_why[i] = "REVOKED"
            tech = pvh[r.random(len(pvh)) < 0.35]
            for i in tech:
                if close_at[i] > mi + 1:
                    close_at[i] = mi + 1 + int(r.integers(0, 2))
                    close_why[i] = "REVOKED"
            u3 = r.random(len(idx))
            for i in idx[u3 < p["tech"]]:
                if close_at[i] > mi + 1:
                    close_at[i] = mi + 1
                    close_why[i] = "REVOKED"
            half = (mi - np.array([open_ep[i][0] for i in idx])) * 2 >= (sched_end[idx] - np.array([open_ep[i][0] for i in idx]))
            u4 = r.random(len(idx))
            for i in idx[(~parole[idx]) & half & (u4 < p["early"])]:
                if close_at[i] > mi:
                    close_at[i] = mi
                    close_why[i] = "DISCHARGED EARLY"
            u5 = r.random(len(idx))
            for i in idx[u5 < p["out_region"]]:
                if close_at[i] > mi:
                    close_at[i] = mi
                    close_why[i] = "TRANSFER OUT"
            for i in idx[(u5 >= p["out_region"]) & (u5 < p["out_region"] + p["death"])]:
                if close_at[i] > mi:
                    close_at[i] = mi
                    close_why[i] = "DECEASED"
            u6 = r.random(len(idx))
            for i in idx[u6 < p["county_move"]]:
                if close_at[i] > mi + 1 and sched_end[i] > mi + 2:
                    self.moves.append((i, mi, county[i], 1 - county[i]))
                    county[i] = 1 - county[i]
            # end of month: close what is due
            due = idx[(sched_end[idx] <= mi + 1) & (close_at[idx] > mi)]
            for i in due:
                close_at[i] = mi
                close_why[i] = "EXPIRED"
            done = idx[close_at[idx] <= mi]
            for i in done:
                s, c0, par, se, k = open_ep.pop(i)
                self.epis.append((i, k, s, mi, close_why[i], par, se))
                active[i] = False
                if close_why[i] == "REVOKED" and r.random() < p["reentry"] and k < 3:
                    pending[i] = mi + int(r.integers(6, 31))
                close_at[i] = 10 ** 9
                close_why[i] = ""
        for i, (s, c0, par, se, k) in open_ep.items():
            self.epis.append((i, k, s, 10 ** 9, "", par, se))
        self.vict = np.array(self.vict, dtype=int).reshape(-1, 2)
        self.book = [(int(a), int(b), c) for a, b, c in self.book]

    # ------------------------------------------------------------------ episodes and days
    def _episodes_table(self):
        """day-level supervision spells per person: start and end dates, closure reasons, county segments"""
        r = self.r_days
        eps = []
        for (i, k, s, e, why, par, se) in sorted(self.epis, key=lambda t: (t[0], t[1])):
            sd = C.month_start(s) + dt.timedelta(days=int(r.integers(0, C.month_days(s))))
            if e >= 10 ** 9:
                ed = None
            elif why == "EXPIRED":
                exp = C.month_start(se) + dt.timedelta(days=int(r.integers(0, C.month_days(se))))
                ed = exp - dt.timedelta(days=1)
            else:
                ed = C.month_start(e) + dt.timedelta(days=int(r.integers(0, C.month_days(e))))
            if ed is not None and ed <= sd:
                ed = sd + dt.timedelta(days=1)
            exp_date = C.month_start(se) + dt.timedelta(days=int(r.integers(0, C.month_days(se))))
            if ed is not None and why == "EXPIRED":
                exp_date = ed + dt.timedelta(days=1)
            eps.append(dict(p=i, k=k, start=sd, end=ed, why=why, parole=bool(par), expires=exp_date,
                            sm=s, em=e))
        self.spells = eps
        # county segments: county moves split an episode at a day inside the move month
        moves = {}
        for (i, mi, a, b) in self.moves:
            moves.setdefault(i, []).append((mi, a, b))
        self.move_days = {}
        for i, lst in moves.items():
            days = []
            for (mi, a, b) in lst:
                d = C.month_start(mi) + dt.timedelta(days=int(r.integers(0, C.month_days(mi) - 1)))
                days.append((d, a, b))
            self.move_days[i] = days

    # helpers used by the pack and the checks
    def spell_of(self, i, d):
        for e in self.spells:
            if e["p"] == i and e["start"] <= d and (e["end"] is None or d <= e["end"]):
                return e
        return None
