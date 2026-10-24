"""The latent world behind task280: Tollard Cable's nodes in the eight hubs and their evening load, the panel's
1,140 households with their plans and their own use of the line, the hourly download tests the panel units ran or
skipped, and the truth the Schedule asks for (each hub's share of weekday evening peak quarter-hours in which a
panel household's connection delivered under 80 per cent of its plan)."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K

QH0 = K.FILING_FROM * 4                       # quarter-hour grid from 16:00 local to 01:00
NQ = (K.FILING_TO - K.FILING_FROM) * 4        # 36
S0 = K.EXTRACT_FROM * 12                      # five-minute grid from 17:00 local to midnight
NS = (K.EXTRACT_TO - K.EXTRACT_FROM) * 12     # 84
PEAK_Q = np.arange(NQ)[(np.arange(NQ) >= (K.PEAK_FROM - K.FILING_FROM) * 4) &
                       (np.arange(NQ) < (K.PEAK_TO - K.FILING_FROM) * 4)]      # 12..27
OVER = {"E100": 1.20, "P300": 1.15, "M600": 1.10, "G1000": 1.06}             # provisioned rate over the plan


def profile(hours, shape="bell"):
    """evening demand relative to the late-evening top, by local clock hour (16 to 25)"""
    t = np.asarray(hours, dtype=float)
    if shape == "plateau":
        rise = 1 / (1 + np.exp(-(t - 18.5) / 0.35))
        fall = 1 / (1 + np.exp(-(t - 23.6) / 0.35))
        return 0.42 + 0.58 * rise * (1 - 0.55 * fall)
    return 0.40 + 0.60 * np.exp(-0.5 * ((t - 21.25) / 1.9) ** 2)


def avail(cap, u):
    """download throughput a new test can take on a node of capacity cap at utilisation u (Mbit/s)"""
    return cap * ((1.0 - u) * 0.94 + 0.035 * u ** 6)


class World:
    def __init__(self, seed=K.SEED, P=None):
        P = {**dict(DS=0.08, AS=0.05, GAM=2.6, BASE=0.30, RHO=0.95, LEVEL=(0.47, 0.67), NODE_SD=0.12, Q_SD=0.04,
                    PROF="plateau", EV=2.0), **(P or {})}
        self.P = P
        rng = np.random.default_rng(seed)
        self.rng = rng
        D = K.DAYS
        self.dates = [K.day(i) for i in range(D)]
        self.wkday = np.array([d.weekday() < 5 for d in self.dates])
        self.dow = np.array([d.weekday() for d in self.dates])

        # the evening's shared drivers: the night itself (games, an election, a premiere, the weather) and the town
        shock = rng.lognormal(0.0, P["DS"], D)
        ev = np.ones(D)
        for i, d in enumerate(self.dates):
            if d.weekday() == 0:
                ev[i] *= rng.uniform(1.06, 1.14)                  # Monday night football
            if d.weekday() == 3:
                ev[i] *= rng.uniform(1.04, 1.10)                  # Thursday night football
        series = [dt.date(2026, 10, 23), dt.date(2026, 10, 24), dt.date(2026, 10, 26), dt.date(2026, 10, 27),
                  dt.date(2026, 10, 28), dt.date(2026, 10, 30), dt.date(2026, 10, 31)]
        for d in series:
            ev[(d - K.WINDOW_START).days] *= rng.uniform(1.22, 1.40)
        ev[(dt.date(2026, 11, 3) - K.WINDOW_START).days] *= 1.32  # election night
        for i in rng.choice(np.where(self.wkday)[0], 4, replace=False):
            ev[i] *= rng.uniform(1.12, 1.22)                      # premieres and storm nights
        self.night = shock * ev ** P["EV"]
        self.town = rng.lognormal(0.0, P["AS"], (len(K.HUB), D))

        # nodes: each hub's nodes serving panel households
        nodes = []
        for a, (code, _) in enumerate(K.HUBS):
            n = int(rng.integers(20, 29))
            lvl = rng.uniform(*P["LEVEL"])
            mix = rng.dirichlet([2.0, 4.0, 3.0])
            for j in range(n):
                cls = rng.choice(["D30-24", "D30-32", "D31"], p=mix)
                nodes.append(dict(hub=a, cls=str(cls), cap=float(K.NODE_CLASSES[cls][1]),
                                  level=float(np.clip(lvl * rng.lognormal(0, P["NODE_SD"]), 0.25, 0.97))))
        self.nodes = nodes
        NN = len(nodes)
        self.node_hub = np.array([nd["hub"] for nd in nodes])
        self.node_cap = np.array([nd["cap"] for nd in nodes])
        self.node_level = np.array([nd["level"] for nd in nodes])
        qh = (QH0 + np.arange(NQ)) / 4.0
        self.qprof = profile(qh + 0.125, P["PROF"])
        eps = np.zeros((NN, D, NQ))
        e = rng.normal(0, P["Q_SD"], (NN, D))
        for q in range(NQ):
            e = 0.6 * e + np.sqrt(1 - 0.36) * rng.normal(0, P["Q_SD"], (NN, D))
            eps[:, :, q] = e
        drv = self.qprof[None, None, :] * self.night[None, :, None] * self.town[self.node_hub][:, :, None]
        self.U = np.clip(self.node_level[:, None, None] * drv * np.exp(eps), 0.02, 0.985)

        # households
        NH = 1140
        w = rng.uniform(0.6, 1.4, NN)
        hn = rng.choice(NN, NH, p=w / w.sum())
        for j in range(NN):                                   # every node serves at least two panel households
            if (hn == j).sum() < 2:
                idx = rng.choice(np.where(np.bincount(hn, minlength=NN)[hn] > 4)[0], 2 - (hn == j).sum(),
                                 replace=False)
                hn[idx] = j
        self.hh_node = hn
        self.NH = NH
        # plans as Tollard sells them: Max 600 only where a node has 32 channels or more, Gig 1000 only on DOCSIS 3.1
        offer = {"D31": (["E100", "P300", "M600", "G1000"], [0.14, 0.36, 0.26, 0.24]),
                 "D30-32": (["E100", "P300", "M600"], [0.30, 0.48, 0.22]),
                 "D30-24": (["E100", "P300"], [0.42, 0.58])}
        plans = []
        for h in range(NH):
            names, pp = offer[self.nodes[hn[h]]["cls"]]
            plans.append(str(rng.choice(names, p=pp)))
        tier = {"E100": 0, "P300": 1, "M600": 2, "G1000": 3}
        pr = np.array([[0.55, 0.35, 0.10], [0.35, 0.50, 0.15], [0.20, 0.50, 0.30], [0.12, 0.43, 0.45]])
        self.inten = np.array([rng.choice([0.35, 0.80, 1.40], p=pr[tier[p]]) for p in plans])
        self.over_hh = rng.normal(1.0, 0.012, NH)
        # plan in force each day: about one household in twenty changes plan once in the window, within what its
        # node is sold
        self.plan_day = np.array([[p] * D for p in plans], dtype=object)
        self.changes = []
        for h in rng.choice(NH, 57, replace=False):
            p0 = plans[h]
            names = offer[self.nodes[hn[h]]["cls"]][0]
            i0 = names.index(p0)
            p1 = names[i0 + 1] if i0 + 1 < len(names) and rng.uniform() < 0.8 else names[max(i0 - 1, 0)]
            if p1 == p0:
                p1 = names[i0 + 1]
            on = int(rng.integers(6, D - 6))
            self.plan_day[h, on:] = p1
            self.changes.append((int(h), p0, p1, on))
        self.down = np.vectorize(K.PLAN_DOWN.get)(self.plan_day).astype(float)        # (NH, D)
        over = np.vectorize(OVER.get)(self.plan_day).astype(float)
        self.rate = self.down * over * self.over_hh[:, None]                           # provisioned Mbit/s

        # truth: each quarter-hour's delivered speed and whether it falls under the standard
        cap = self.node_cap[hn][:, None, None]
        self.speed = np.minimum(self.rate[:, :, None], avail(cap, self.U[hn]))         # (NH, D, NQ)
        self.below = self.speed < K.STANDARD * self.down[:, :, None]
        pk = self.below[:, self.wkday][:, :, PEAK_Q]
        self.truth_hh = pk.reshape(NH, -1).mean(axis=1)
        self.hh_hub = self.node_hub[hn]
        self.truth_hub = np.array([100 * self.truth_hh[self.hh_hub == a].mean() for a in range(len(K.HUB))])

        # the household's own use of the line, five minutes at a time, and the hourly tests it lets run
        sh = (S0 + np.arange(NS)) / 12.0
        sprof = profile(sh + 1 / 24, P["PROF"])
        dd = self.night[None, :, None] * self.town[self.hh_hub][:, :, None] * sprof[None, None, :]
        pa = np.clip(self.inten[:, None, None] * P["BASE"] * dd ** P["GAM"], 0.01, 0.92)
        busy = np.zeros((NH, D, NS), bool)
        busy[:, :, 0] = rng.uniform(size=(NH, D)) < pa[:, :, 0]
        rho = P["RHO"]
        for s in range(1, NS):
            p = pa[:, :, s]
            stay = np.where(busy[:, :, s - 1], rho + (1 - rho) * p, rho + (1 - rho) * (1 - p))
            busy[:, :, s] = np.where(rng.uniform(size=(NH, D)) < stay, busy[:, :, s - 1], ~busy[:, :, s - 1])
        self.busy = busy
        NHR = K.EXTRACT_TO - K.EXTRACT_FROM                                            # 7 scheduled tests a night
        minute = rng.integers(0, 45, (NH, D, NHR))
        k_ran = np.full((NH, D, NHR), -1)
        for k in range(4):
            slot = np.arange(NHR)[None, None, :] * 12 + (minute + 5 * k) // 5
            idle = ~np.take_along_axis(busy, slot, axis=2)
            k_ran = np.where((k_ran < 0) & idle, k, k_ran)
        self.minute = minute
        self.k_ran = k_ran                                                             # -1: skipped
        self.sec = rng.integers(0, 60, (NH, D, NHR))
        self.noise = rng.lognormal(0.0, P.get("TN", 0.035), (NH, D, NHR))

    def tests(self):
        """every test that ran: household, day, hour index (0 = 17:00), start minute, quarter-hour index on the
        16:00 grid, measured Mbit/s"""
        h, d, r = np.nonzero(self.k_ran >= 0)
        m = self.minute[h, d, r] + 5 * self.k_ran[h, d, r]
        q = (K.EXTRACT_FROM - K.FILING_FROM + r) * 4 + m // 15
        mbps = self.speed[h, d, q] * self.noise[h, d, r]
        return h, d, r, m, q, mbps
