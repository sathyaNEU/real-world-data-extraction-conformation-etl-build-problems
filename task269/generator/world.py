"""The world before any export: every patient's stay on every ward bed, the care hours each needs on each AM and PM
shift, the nursing hours worked on each shift, the hand hygiene moments that arise and whether staff perform hand
hygiene at each, and the gold auditors' sessions. Generator truth only; nothing here ships as it stands."""
import datetime as dt
import numpy as np

import common as K

MID = 1.15       # required over worked hours at which half the shortfall effect has set in
WIDTH = 0.035    # how sharply it sets in
DROP = 0.30      # compliance lost on a shift whose hours fall far short of its care
MOMENTS_PER_CARE_HOUR = 0.85     # moments arising per hour of required care on a shift (whole ward)
AUDIT_K = 4.0    # how strongly the ward's auditors avoid shifts whose hours fall short


def p_of_v(base, v):
    return base - DROP / (1.0 + np.exp(-(np.asarray(v, float) - MID) / WIDTH))


class World:
    def __init__(self, seed=K.SEED):
        self.seed = seed
        rng = np.random.default_rng([269, seed, 1])
        self.shifts = {}      # (ward, date, shift) -> dict(req, worked, v, npts, patients=[(key, bed, hours)])
        self.stays = {}       # ward -> list of (key, bed, start shift index, end shift index, mean hours)
        nshift = len(K.DAYS) * 2
        for code, name, spec, beds, base, nhpp, sshare, sadd, buf, los, kind in K.WARDS:
            wr = np.random.default_rng([269, seed, 2, K.WARD.index(code)])
            # surge days: the ward runs extra beds and sicker patients; winter weighs on the medical wards
            surge = np.zeros(len(K.DAYS), bool)
            for i, d in enumerate(K.DAYS):
                doy = (d - dt.date(d.year, 1, 1)).days
                winter = np.exp(-((doy - 190) / 42.0) ** 2) if d.year == 2026 or d.month >= 7 else 0.0
                pr = sshare * (1 + 0.9 * winter) if kind == "surge" else sshare
                surge[i] = wr.random() < min(0.95, pr)
            # stays bed by bed, in shift units (two day shifts a day)
            stays = []
            key = 0
            for b in range(1, beds + 1):
                t = -int(wr.integers(40, 120))         # the year opens on a full ward: stays begun before 1 July
                while t < nshift:
                    n = max(1, int(round(wr.gamma(1.6, los * 2 / 1.6))))
                    hm = float(nhpp * wr.lognormal(0.0, 0.28))
                    key += 1
                    if t + n > 0:
                        stays.append((f"{code}{key:05d}", b, t, min(nshift, t + n), hm))
                    t = t + n + int(wr.geometric(0.40)) - 1
            # escalation beds opened on surge days (corridor and chair spaces), short stays
            extra_beds = max(2, int(round(beds * sadd * 0.15)))
            for i, d in enumerate(K.DAYS):
                if not surge[i]:
                    continue
                for e in range(extra_beds):
                    if wr.random() < 0.75:
                        n = int(wr.integers(1, 4))
                        key += 1
                        hm = float(nhpp * wr.lognormal(0.12, 0.28))
                        stays.append((f"{code}{key:05d}", 100 + e, 2 * i + int(wr.integers(0, 2)),
                                      min(nshift, 2 * i + 2 + n), hm))
            self.stays[code] = stays
            occ = [[] for _ in range(nshift)]
            for k, b, s0, s1, hm in stays:
                for s in range(max(0, s0), s1):
                    occ[s].append((k, b, hm, s - s0))
            rows = []
            for i, d in enumerate(K.DAYS):
                for j, s in enumerate(("AM", "PM")):
                    idx = 2 * i + j
                    pts = []
                    for k, b, hm, age in occ[idx]:
                        h = hm * (1.35 if age == 0 else 1.0) * (1.06 if s == "PM" else 1.0)
                        if surge[i]:
                            h *= 1 + sadd * 0.35
                        h = float(np.round(max(0.4, h * wr.lognormal(0.0, 0.10)), 1))
                        pts.append((k, b, h))
                    rows.append((d, s, pts, float(round(sum(p[2] for p in pts), 1)), bool(surge[i])))
            # the roster is flexed to the acuity system's forecast for each day shift (its patients' last entries)
            # by extra shifts and redeployment; a shift runs short when sick leave and bank requests go unfilled
            for d, s, pts, req, sg in rows:
                worked = req * wr.lognormal(0.0, 0.035) * buf
                if wr.random() < K.SHORT[code]:
                    worked *= wr.uniform(0.62, 0.84)
                worked = float(max(8.0, round(worked / 4.0) * 4.0))
                # the acuity entries are tenths of an hour and the shifts whole hours: a total landing exactly on a
                # twentieth of the worked hours is nudged a tenth, so no shift sits on the edge of a band
                while pts and any(abs(req * 10 - round(c * worked * 10)) < 1e-6 for c in np.arange(0.50, 2.01, 0.05)):
                    k0, b0, h0 = pts[0]
                    pts = [(k0, b0, round(h0 + 0.1, 1))] + pts[1:]
                    req = float(round(sum(p[2] for p in pts), 1))
                self.shifts[(code, d, s)] = dict(req=req, worked=worked, v=req / worked, npts=len(pts),
                                                 patients=pts, surge=sg)
        self._compliance()
        self._audits(rng)

    def _compliance(self):
        base = {w[0]: w[4] for w in K.WARDS}
        self.truth = {}
        for code in K.WARD:
            num = den = 0.0
            for d in K.DAYS:
                for s in ("AM", "PM"):
                    x = self.shifts[(code, d, s)]
                    x["p"] = float(p_of_v(base[code], x["v"]))
                    m = x["req"] * MOMENTS_PER_CARE_HOUR
                    num += m * x["p"]
                    den += m
            self.truth[code] = num / den

    def _audits(self, rng):
        """each ward's gold auditors' sessions: weekdays, mostly AM, released when the shift's hours cover its care"""
        self.sessions = []
        for code in K.WARD:
            ar = np.random.default_rng([269, self.seed, 3, K.WARD.index(code)])
            cand = [(d, s) for d in K.DAYS for s in ("AM", "PM") if d.weekday() < 5]
            w = np.array([np.exp(-AUDIT_K * max(0.0, self.shifts[(code, d, s)]["v"] - 0.98)) *
                          (1.0 if s == "AM" else 0.30) for d, s in cand])
            # each ward aims at the program's 100 moments a month, some wards more keenly; December and January,
            # the leave months, run lighter
            pick = []
            for mo in sorted(set((d.year, d.month) for d, _ in cand)):
                idx = [i for i, (d, s) in enumerate(cand) if (d.year, d.month) == mo]
                rate = np.mean([8.0 * self.shifts[(code, cand[i][0], cand[i][1])]["req"] /
                                max(1, self.shifts[(code, cand[i][0], cand[i][1])]["npts"]) for i in idx])
                target = 100 * K.KEEN[code] * (0.75 if mo[1] in (12, 1) else 1.0) * ar.uniform(0.85, 1.25)
                n = max(2, int(round(target / rate)))
                ww = w[idx] / w[idx].sum()
                pick += [idx[j] for j in ar.choice(len(idx), size=min(n, len(idx)), replace=False, p=ww)]
            pick = sorted(pick)
            for i in pick:
                d, s = cand[i]
                x = self.shifts[(code, d, s)]
                rate = 8.0 * (x["req"] / max(1, x["npts"]))
                m = max(3, int(ar.poisson(rate)))
                ok = ar.random(m) < x["p"]
                self.sessions.append(dict(ward=code, date=d, shift=s, v=x["v"], m=m, c=int(ok.sum()),
                                          outcomes=ok.tolist()))

    def audited(self, code):
        a = [x for x in self.sessions if x["ward"] == code]
        return sum(x["c"] for x in a) / sum(x["m"] for x in a)
