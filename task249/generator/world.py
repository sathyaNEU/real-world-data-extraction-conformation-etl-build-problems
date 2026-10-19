"""The clean truth for task249: colleges, candidates and their abilities, the 2028 season's applications, sittings,
shortlists and selection days, the 2028 equivalence study, the 2029 plans, and the exposure log.

Nothing here is written to a file; records.py writes the exports from this truth with each system's own mess."""
import datetime as dt
import numpy as np
import params as P

STATES = ["Karnataka", "Tamil Nadu", "Maharashtra", "Telangana", "Andhra Pradesh", "Kerala", "Gujarat",
          "Uttar Pradesh", "Delhi", "West Bengal", "Rajasthan", "Madhya Pradesh", "Odisha", "Punjab", "Haryana"]
STATE_W = np.array([14, 13, 14, 10, 8, 6, 5, 8, 5, 5, 4, 3, 2, 2, 1], float)


class World:
    def __init__(self, seed=P.SEED):
        self.rng = np.random.default_rng(seed)
        self._colleges()
        self._candidates()
        self._applications()
        self._calendar()
        self._sittings()
        self._shortlists()
        self._study()
        self._plans()

    # ------------------------------------------------------------------ colleges and candidates
    def _colleges(self):
        r = self.rng
        rows = []
        k = 0
        for tier, d in P.TIERS.items():
            for i in range(d["n"]):
                k += 1
                st = r.choice(len(STATES), p=STATE_W / STATE_W.sum())
                size = int(r.integers(d["size"][0], d["size"][1] + 1))
                aishe = "C-%05d" % int(r.integers(10000, 59999))
                rows.append(dict(cid=k, tier=tier, state=STATES[st], size=size, aishe=aishe,
                                 short="%s%03d" % (tier, i + 1)))
        # AISHE-style codes unique
        seen = set()
        for c in rows:
            while c["aishe"] in seen:
                c["aishe"] = "C-%05d" % int(r.integers(10000, 59999))
            seen.add(c["aishe"])
        self.colleges = rows
        self.col_by_id = {c["cid"]: c for c in rows}

    def _candidates(self):
        r = self.rng
        cid, tier, th = [], [], []
        for c in self.colleges:
            d = P.TIERS[c["tier"]]
            n = c["size"]
            cid += [c["cid"]] * n
            tier += [c["tier"]] * n
            th.append(r.normal(d["mu"], d["sd"], n))
        self.cand_college = np.array(cid)
        self.cand_tier = np.array(tier)
        self.theta = np.concatenate(th)
        self.N = len(self.theta)

    # ------------------------------------------------------------------ applications
    def _applications(self):
        """each account draws applicants from its tiers' campuses; a candidate may apply to several accounts"""
        r = self.rng
        self.acc = {}
        apps = []          # (cand, account code)
        tier_idx = {t: np.where(self.cand_tier == t)[0] for t in P.TIERS}
        for code, name, sector, grp, mix, f28, f29, q29 in P.ACCOUNTS:
            lo, hi = P.POOL_SIZE[grp]
            target = int(r.integers(lo, hi + 1))
            # covered campuses: a share of each tier's colleges
            cover = {}
            members = []
            for t, share in mix.items():
                cols = [c["cid"] for c in self.colleges if c["tier"] == t]
                frac = {"E": 0.85, "M": 0.6, "V": 0.55}[grp]
                m = max(3, int(round(len(cols) * frac)))
                chosen = sorted(r.choice(cols, size=min(m, len(cols)), replace=False).tolist())
                cover[t] = chosen
                pool = tier_idx[t][np.isin(self.cand_college[tier_idx[t]], chosen)]
                want = int(round(target * share))
                want = min(want, len(pool))
                # students apply with a pull toward ability inside covered campuses (elite accounts more so)
                tilt = {"E": 0.9, "M": 0.35, "V": -0.05}[grp]
                w = np.exp(tilt * self.theta[pool])
                pick = r.choice(pool, size=want, replace=False, p=w / w.sum())
                members.append(pick)
            mem = np.sort(np.concatenate(members))
            self.acc[code] = dict(code=code, name=name, sector=sector, grp=grp, mix=mix, f28=f28, f29=f29,
                                  q29=q29, cover=cover, members=mem)
            apps += [(int(i), code) for i in mem]
        self.apps = apps
        applied = np.zeros(self.N, bool)
        applied[[a for a, _ in apps]] = True
        self.applied = applied

    # ------------------------------------------------------------------ the season calendar
    def _calendar(self):
        """each college's test week falls in July (top-tier campuses early, as the day-one companies come first);
        D1 and S drives hold the selection day on day 3 of the week, later drives in September, assessment centres
        in October and November"""
        r = self.rng
        starts = [dt.date(2028, 7, 3), dt.date(2028, 7, 10), dt.date(2028, 7, 17), dt.date(2028, 7, 24)]
        wp = {"T1": [0.7, 0.3, 0, 0], "T2": [0.4, 0.4, 0.2, 0], "T3": [0.15, 0.35, 0.35, 0.15], "T4": [0, 0.1, 0.4, 0.5]}
        self.test_week = {c["cid"]: starts[int(r.choice(4, p=wp[c["tier"]]))] for c in self.colleges}

    # ------------------------------------------------------------------ sittings (2028)
    def _sittings(self):
        r = self.rng
        n = self.N
        # proxies: a small share of sittings were taken by someone else, concentrated in T3 and T4 campuses
        p_proxy = np.select([self.cand_tier == "T1", self.cand_tier == "T2", self.cand_tier == "T3"], [0.001, 0.003, 0.008], 0.012)
        self.proxy = (r.random(n) < p_proxy) & self.applied
        ab_sit = np.where(self.proxy, r.normal(1.25, 0.35, n), self.theta)
        e = r.normal(0, 1, n) * P.se_online(ab_sit)
        est = ab_sit + e
        se = P.se_online(est) * np.exp(r.normal(0, 0.025, n))
        self.u_est = np.round(est, 3)
        self.u_se = np.round(se, 3)
        # sitting day and time inside the college's test week window (Monday 00:00 to Tuesday 23:59 IST): campus
        # lab sittings at day-one and first-company campuses in office hours on the Monday, home sittings across
        # the two days, some just after midnight
        lab = np.zeros(n, bool)
        for code, a in self.acc.items():
            if a["f28"] in ("D1", "S"):
                lab[a["members"]] = True
        self.lab = lab
        day = np.where(lab, 0, (r.random(n) < 0.38).astype(int))
        self.sit_date = np.array([self.test_week[c] + dt.timedelta(days=int(d)) for c, d in zip(self.cand_college, day)])
        home_min = np.where(r.random(n) < 0.09, r.integers(0, 150, n), r.integers(8 * 60, 23 * 60 + 50, n))
        self.sit_minute = np.where(lab, r.integers(9 * 60 + 30, 16 * 60 + 30, n), home_min)
        # restarts: an interrupted attempt abandoned, then the completed attempt under the same booking; the device
        # is drawn in records (lab sittings run on the college's desktops), so the restart chance is set there
        self.restart_u = r.random(n)
        self.restart_items = r.integers(3, 13, n)

    # ------------------------------------------------------------------ 2028 shortlists and selection days
    def _shortlists(self):
        r = self.rng
        self.short28 = {}
        for code, a in self.acc.items():
            mem = a["members"]
            q28 = a["q29"] * (1.0 if a["grp"] != "E" else r.uniform(0.9, 1.15))
            n_sl = max(12, int(round(len(mem) * q28)))
            order = mem[np.argsort(-self.u_est[mem], kind="stable")]
            self.short28[code] = order[:n_sl]

    # ------------------------------------------------------------------ the equivalence study (Oct to Dec 2028)
    def _study(self):
        r = self.rng
        part = [c for c in self.colleges if c["tier"] in ("T1", "T2", "T3", "T4")]
        chosen = sorted(r.choice([c["cid"] for c in part], size=14, replace=False).tolist())
        # volunteers: 2,412 students at 14 partner colleges, abilities from their tiers
        sizes = r.multinomial(2412, np.ones(14) / 14)
        th, col = [], []
        for cid, s in zip(chosen, sizes):
            d = P.TIERS[self.col_by_id[cid]["tier"]]
            th.append(r.normal(d["mu"], d["sd"], s))
            col += [cid] * s
        th = np.concatenate(th)
        m = len(th)
        gaps = np.array([1, 2, 3, 7, 14, 21, 28, 42, 56, 70, 84])
        g = r.choice(gaps, m)
        u = th + r.normal(0, 1, m) * P.se_online(th)
        v = th + P.retest_gain(g) + r.normal(0, 1, m) * P.se_verify(th)
        self.study = dict(col=np.array(col), theta=th, gap=g, u=np.round(u, 3),
                          u_se=np.round(P.se_online(u) * np.exp(r.normal(0, 0.025, m)), 3),
                          v=np.round(v, 3), v_se=np.round(P.se_verify(v) * np.exp(r.normal(0, 0.025, m)), 3),
                          attended=r.random(m) > 0.078, partners=chosen)

    # ------------------------------------------------------------------ 2029 plans
    def _plans(self):
        r = self.rng
        self.plan = {}
        for code, a in self.acc.items():
            n28 = len(a["members"]) + (len(self.acc_pgl) if code == "NVK" and hasattr(self, "acc_pgl") else 0)
            growth = r.uniform(0.96, 1.08)
            exp_app = int(round(n28 * growth, -1))
            sl = int(round(exp_app * a["q29"]))
            self.plan[code] = dict(expected=exp_app, shortlist=sl, fmt=a["f29"])
