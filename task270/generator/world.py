"""Kleerwissel's world, day by day: every consumer who signs up is simulated once, set aside in the year's global
holdout or routed through the three onboarding layers into whichever experiment and arm the platform assigns, and
shaped by every onboarding change shipped before their sign-up. The scorecards, the holdout's rows and the 2025 cohort
table are all summaries of these same users, so the pack's files agree with each other the way real exports do.

Each user carries an engagement factor u that drives six-month retention, and each candidate metric a latent score
that loads on u by RU (how the metric tracks retention user by user). Each change shifts the latent scores and the
retention threshold; its shifts on the candidates correlate with its retention shift by RT (how the metric's effects
track retention's effects change by change). RU and RT are set apart on purpose: active days and sessions follow
retention user by user, first purchase is moved by the changes that move retention."""
import datetime as dt
import math

import numpy as np

import common as K

DEFAULT = dict(
    RU=(0.80, 0.80, 0.18, 0.15, 0.50),       # loading of each candidate's latent score on u
    RT=(0.00, 0.30, 0.62, 0.20, 0.05),       # correlation of each candidate's shifts with the retention shift
    TS=(0.022, 0.022, 0.045, 0.030, 0.030),  # spread of the changes' latent shifts
    TY=0.010,                                # spread of the changes' retention shifts (threshold units / 3)
    BASE=1520.0,                             # consumer sign-ups a day, January 2024
    LAUNCH=0.30,                             # share of a change's experiment effect its launch keeps
)
WEEKDAY = (1.03, 0.95, 0.94, 0.95, 0.99, 1.10, 1.15)                       # Monday first
MONTH = (1.14, 1.04, 1.00, 0.98, 0.96, 0.92, 0.88, 0.90, 1.04, 1.01, 1.06, 1.10)


def days(a, b):
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


class Experiment:
    __slots__ = ("idx", "eid", "layer", "team", "start", "end", "planned_end", "arms", "control", "status", "srm",
                 "late", "shifts", "changes", "decision", "ship", "title", "two_week_at", "six_month_at", "labels")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


class World:
    def __init__(self, seed=K.SEED, params=None, last_day=None):
        self.seed = seed
        self.p = dict(DEFAULT, **(params or {}))
        self.RU = np.array(self.p["RU"])
        self.RT = np.array(self.p["RT"])
        self.TS = np.array(self.p["TS"])
        self.last_day = last_day or K.LAST_DAY
        self.schedule()
        self.effects()
        self.simulate()

    # ----------------------------------------------------------------------------------------------------- schedule
    def schedule(self):
        """each layer starts a new experiment every few days, at most four live at once; most run three weeks"""
        exps = []
        for li, layer in enumerate(K.LAYERS):
            rng = np.random.default_rng([270, self.seed, 1, li])
            d = K.FIRST_DAY + dt.timedelta(days=int(rng.integers(0, 4)))
            live = []
            while d <= K.LAST_DAY + dt.timedelta(days=24):
                live = [e for e in live if e.end >= d]
                if len(live) < 4 and d.weekday() < 5:
                    dur = int(rng.choice([14, 21, 28], p=[0.25, 0.5, 0.25]))
                    arms = 3 if rng.random() < 0.22 else 2
                    e = Experiment(layer=layer, team=str(rng.choice(K.TEAMS[layer])), start=d,
                                   planned_end=d + dt.timedelta(days=dur - 1), arms=arms, status="completed",
                                   srm=False, late=False)
                    e.end = e.planned_end
                    u = rng.random()
                    if u < 0.03:
                        e.status = "stopped_early"
                        e.end = d + dt.timedelta(days=dur // 2 - 1)
                    elif u < 0.055:
                        e.srm = True
                    exps.append(e)
                    live.append(e)
                    d += dt.timedelta(days=int(rng.choice([2, 3, 4, 5, 6, 7, 8], p=[.1, .2, .2, .2, .15, .1, .05])))
                else:
                    d += dt.timedelta(days=1)
        exps.sort(key=lambda e: (e.start, K.LAYERS.index(e.layer)))
        for i, e in enumerate(exps):
            e.idx = i
            e.eid = "OB-%d-%03d" % (e.start.year % 100, 1 + sum(1 for f in exps[:i] if f.start.year == e.start.year))
            e.two_week_at = e.end + dt.timedelta(days=15)
            e.six_month_at = e.end + dt.timedelta(days=181)
            e.late = (e.layer != "notifications" and K.LATE_EVENTS[0] <= e.two_week_at <= K.LATE_EVENTS[1])
        self.experiments = exps

    # ------------------------------------------------------------------------------------------------------ effects
    def effects(self):
        """every treatment arm is a change: latent shifts on the five candidates, the retention threshold and the
        two guardrails"""
        RT, TS = self.RT, self.TS
        for e in self.experiments:
            rng = np.random.default_rng([270, self.seed, 2, e.idx])
            e.changes = []
            for a in range(e.arms - 1):
                z = rng.standard_normal(6)
                sh = np.zeros(8)
                sh[:5] = TS * (RT * z[0] + np.sqrt(1 - RT ** 2) * z[1:])
                sh[5] = self.p["TY"] * z[0]
                sh[6] = 0.06 * rng.standard_normal() + (0.45 if e.status == "stopped_early" else 0.0)
                sh[7] = 0.05 * rng.standard_normal()
                e.changes.append(sh)
            e.shifts = [np.zeros(8)] + e.changes          # arm 0 is the control
            e.decision, e.ship = None, None

    # ---------------------------------------------------------------------------------------------------- the users
    def metrics(self, n, shift, rng, ios):
        """the five candidates, retention and the guardrails for n users carrying latent shifts (n x 8)"""
        RU = self.RU
        u = rng.standard_normal(n)
        w = rng.standard_normal((n, 5))
        L = RU[None, :] * u[:, None] + np.sqrt(1 - RU ** 2)[None, :] * w + shift[:, :5]
        out = np.empty((n, 8))
        out[:, 0] = 1 + rng.binomial(13, sigmoid(-0.45 + 1.45 * L[:, 0]))
        out[:, 1] = rng.poisson(np.exp(1.95 + 0.50 * L[:, 1]))
        out[:, 2] = (rng.random(n) < sigmoid(-1.25 + 1.35 * L[:, 2])).astype(float)
        out[:, 3] = rng.poisson(np.exp(0.55 + 0.60 * L[:, 3]))
        push_on = rng.random(n) < np.where(ios, 0.56, 0.74)
        out[:, 4] = np.where(push_on, rng.poisson(np.exp(1.10 + 0.45 * L[:, 4])), 0)
        out[:, 5] = ((0.9 * u + 0.44 * rng.standard_normal(n)) > 0.30 - 3.0 * shift[:, 5]).astype(float)
        out[:, 6] = (rng.random(n) < sigmoid(-2.05 - 0.55 * u + shift[:, 6])).astype(float)
        out[:, 7] = rng.poisson(0.055 * np.exp(0.25 * rng.standard_normal(n) + shift[:, 7]))
        return out, u

    def volume(self, d, rng):
        g = 1.0 + 0.085 * ((d - dt.date(2024, 1, 1)).days / 365.25)
        lam = self.p["BASE"] * g * WEEKDAY[d.weekday()] * MONTH[d.month - 1]
        return int(rng.poisson(lam))

    def simulate(self):
        E = self.experiments
        nm = 8
        self.sums = {}                  # (exp idx, arm) -> [n, sum x (8), sum x^2 (8)]
        self.sums_late = {}             # the first computation of the late-events experiments
        self.holdout_rows = []
        self.cohort = {}                # (date, platform, country) -> [users, holdout users, sums (6), holdout sums (6)]
        self.business = {}
        self.converted = {}             # (date, platform, country) -> [users who later became business, sums (6)]
        shipped = []                    # (ship date, layer, shift)
        cum = np.zeros(nm)
        frozen = {}
        by_start = {}
        for e in E:
            by_start.setdefault(e.start, []).append(e)
        live = {layer: [] for layer in K.LAYERS}
        decide_on = {}
        for e in E:
            decide_on.setdefault(e.end + dt.timedelta(days=15), []).append(e)
        ship_on = {}
        for d in days(K.FIRST_DAY, self.last_day):
            for e in decide_on.get(d, []):
                self.decide(e)
                if e.ship:
                    for a, ch in enumerate(e.changes):
                        if e.decision[a] == "shipped":
                            ship_on.setdefault(e.ship, []).append(self.p["LAUNCH"] * ch)
            if d == dt.date(d.year, 1, 1) or d == K.FIRST_DAY:
                frozen[d.year] = cum.copy()
            for ch in ship_on.get(d, []):
                cum = cum + ch
            for e in by_start.get(d, []):
                live[e.layer].append(e)
            for layer in K.LAYERS:
                live[layer] = [e for e in live[layer] if e.end >= d]
            rng = np.random.default_rng([270, self.seed, 3, d.toordinal()])
            n = self.volume(d, rng)
            ios = rng.random(n) < 0.46
            be = rng.random(n) < 0.28
            hold_share = K.HOLDOUT_YEARS.get(d.year, 0.0)
            hold = rng.random(n) < hold_share
            shift = np.tile(cum, (n, 1))
            if hold.any():
                shift[hold] = frozen.get(d.year, cum)
            assign = {}
            for layer in K.LAYERS:
                L = live[layer]
                if not L:
                    continue
                pick = rng.integers(0, len(L), n)
                arm = np.zeros(n, dtype=int)
                for j, e in enumerate(L):
                    m = (pick == j) & ~hold
                    arm[m] = rng.integers(0, e.arms, int(m.sum()))
                    for a in range(1, e.arms):
                        ma = m & (arm == a)
                        shift[ma] += e.shifts[a]
                assign[layer] = (pick, arm)
            X, u = self.metrics(n, shift, rng, ios)
            # the experiments' sums
            for layer, (pick, arm) in assign.items():
                for j, e in enumerate(live[layer]):
                    m = (pick == j) & ~hold
                    for a in range(e.arms):
                        ma = m & (arm == a)
                        if e.srm and a > 0:
                            # the new flow crashed for some low-engagement users before their assignment logged
                            lost = ma & (u < -1.1) & (rng.random(n) < 0.3)
                            ma = ma & ~lost
                        self._add(self.sums, (e.idx, a), X[ma])
                        if e.late:
                            Y = X[ma].copy()
                            io = ios[ma]
                            Y[io, 1] = rng.binomial(Y[io, 1].astype(int), 0.955)
                            Y[io, 4] = rng.binomial(Y[io, 4].astype(int), 0.94)
                            dec = io & (Y[:, 0] > 1) & (rng.random(len(Y)) < 0.06)
                            Y[dec, 0] -= 1
                            self._add(self.sums_late, (e.idx, a), Y)
            # the 2025 holdout's rows and the 2025 cohort table
            if d.year == 2025:
                hid = np.flatnonzero(hold)
                for i in hid:
                    self.holdout_rows.append((d, bool(ios[i]), bool(be[i])) + tuple(X[i, :6]))
                # consumers who later upgrade to a business (seller) account, the keenest sellers among them; drawn
                # on their own stream so the rest of the world is untouched
                cr = np.random.default_rng([270, self.seed, 5, d.toordinal()])
                conv = cr.random(n) < sigmoid(-4.55 + 0.055 * X[:, 1] + 0.30 * X[:, 3])
                for pi in (True, False):
                    for ci in (False, True):
                        m = (ios == pi) & (be == ci)
                        key = (d, pi, ci)
                        acc = self.cohort.setdefault(key, np.zeros(14))
                        acc[0] += m.sum()
                        acc[1] += (m & hold).sum()
                        acc[2:8] += X[m, :6].sum(0)
                        acc[8:14] += X[m & hold, :6].sum(0)
                        cv = self.converted.setdefault(key, np.zeros(7))
                        cv[0] += (m & conv).sum()
                        cv[1:7] += X[m & conv, :6].sum(0)
                self.business_day(d, rng)
        self.cum_end = cum
        self.frozen = frozen

    def business_day(self, d, rng):
        """sellers' business accounts: outside the consumer onboarding, its experiments and its holdout"""
        n = int(rng.poisson(0.032 * self.p["BASE"] * WEEKDAY[d.weekday()]))
        ios = rng.random(n) < 0.38
        be = rng.random(n) < 0.24
        sh = np.zeros((n, 8))
        sh[:, :5] = (0.9, 0.7, -0.6, -0.3, 0.2)
        X, _ = self.metrics(n, sh, rng, ios)
        for pi in (True, False):
            for ci in (False, True):
                m = (ios == pi) & (be == ci)
                acc = self.business.setdefault((d, pi, ci), np.zeros(7))
                acc[0] += m.sum()
                acc[1:7] += X[m, :6].sum(0)

    @staticmethod
    def _add(store, key, X):
        acc = store.get(key)
        if acc is None:
            acc = store[key] = np.zeros(1 + 2 * X.shape[1] if X.size else 17)
        if len(X):
            acc[0] += len(X)
            acc[1:9] += X.sum(0)
            acc[9:17] += (X ** 2).sum(0)

    def arm_stats(self, e, a, late=False):
        """users, means and standard deviations (n - 1) of the eight metrics"""
        acc = (self.sums_late if late else self.sums).get((e.idx, a))
        if acc is None or acc[0] < 2:
            return None
        n = acc[0]
        mean = acc[1:9] / n
        var = (acc[9:17] - n * mean ** 2) / (n - 1)
        return int(n), mean, np.sqrt(np.maximum(var, 0))

    def decide(self, e):
        """the two-week read as the teams read it before a proxy was set: a change shipped when sessions or first
        purchase rose clearly and uninstalls did not"""
        e.decision = []
        c = self.arm_stats(e, 0)
        for a in range(1, e.arms):
            t = self.arm_stats(e, a)
            if c is None or t is None or e.srm or e.status == "stopped_early":
                e.decision.append("not_shipped")
                continue
            z = (t[1] - c[1]) / np.sqrt(t[2] ** 2 / t[0] + c[2] ** 2 / c[0])
            ok = (z[1] > 2.4 or z[2] > 2.4) and z[6] < 1.0 and z[0] > -1.0
            e.decision.append("shipped" if ok else "not_shipped")
        if "shipped" in e.decision:
            e.ship = e.end + dt.timedelta(days=21 + 7 * (e.idx % 2))
            if e.decision.count("shipped") == 2:
                # a three-arm test ships its better arm only
                c = self.arm_stats(e, 0)
                zs = []
                for a in (1, 2):
                    t = self.arm_stats(e, a)
                    zs.append(((t[1] - c[1]) / np.sqrt(t[2] ** 2 / t[0] + c[2] ** 2 / c[0]))[1])
                worse = 1 + int(zs[0] >= zs[1])
                e.decision[worse - 1] = "not_shipped"

    # ------------------------------------------------------------------------------------------------- the truth
    def expected(self, shift):
        """each metric's expected mean across all users for latent shifts (8), by Gauss-Hermite quadrature: the
        latent scores are standard normal plus the shift"""
        x, w = np.polynomial.hermite_e.hermegauss(96)
        w = w / w.sum()
        p_on = 0.46 * 0.56 + 0.54 * 0.74
        m = np.empty(6)
        m[0] = 1 + 13 * (w * sigmoid(-0.45 + 1.45 * (x + shift[0]))).sum()
        m[1] = math.exp(1.95 + 0.50 * shift[1] + 0.50 ** 2 / 2)
        m[2] = (w * sigmoid(-1.25 + 1.35 * (x + shift[2]))).sum()
        m[3] = math.exp(0.55 + 0.60 * shift[3] + 0.60 ** 2 / 2)
        m[4] = p_on * math.exp(1.10 + 0.45 * shift[4] + 0.45 ** 2 / 2)
        from statistics import NormalDist
        m[5] = 1 - NormalDist().cdf((0.30 - 3.0 * shift[5]) / math.sqrt(0.81 + 0.44 ** 2))
        return m

    def true_effects(self):
        """each change's effect on the six metrics' means across all users at the 2024 baseline: the world's own
        answer, never shipped"""
        m0 = self.expected(np.zeros(8))
        return {(e.idx, a): self.expected(ch) - m0 for e in self.experiments for a, ch in enumerate(e.changes, 1)}
