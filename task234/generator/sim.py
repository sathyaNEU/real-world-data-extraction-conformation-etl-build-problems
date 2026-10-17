"""The epidemic world behind the reports: each population's positivity by virus and week, and each stream's weekly
tests and positives (what the laboratories' aggregate reports count) from MMWR 2022-W40 to 2027-W03."""
import datetime as dt

import numpy as np

import params as P


def weeks():
    out, d = [], P.FIRST_WEEK
    while d <= P.CUR_WEEK:
        out.append(d)
        d += dt.timedelta(weeks=1)
    return out


def season_week(d):
    for yy in (2026, 2025, 2024, 2023, 2022):
        s40 = P.mmwr_start(yy) + dt.timedelta(weeks=39)
        if d >= s40:
            return (d - s40).days // 7, yy
    raise ValueError(d)


def mmwr_label(d):
    for y in (d.year + 1, d.year, d.year - 1):
        s = P.mmwr_start(y)
        if d >= s:
            return y, (d - s).days // 7 + 1


def holiday_factor(d):
    end = d + dt.timedelta(days=6)
    hs = [dt.date(y, 12, 25) for y in range(2022, 2027)] + [dt.date(y, 1, 1) for y in range(2023, 2028)]
    hs += [dt.date(y, 11, 1) + dt.timedelta(days=(3 - dt.date(y, 11, 1).weekday()) % 7 + 21) for y in range(2022, 2027)]
    return 0.84 if any(d <= h <= end for h in hs) else 1.0


class World:
    def __init__(self, seed=P.WORLD_SEED):
        self.seed = seed
        self.W = weeks()
        self.NW = len(self.W)
        self.cur = self.NW - 1
        self.SW = [season_week(d) for d in self.W]
        self.HOL = np.array([holiday_factor(d) for d in self.W])

    def curve(self, v, g):
        tab = dict(zip((2022, 2023, 2024, 2025), P.HIST[(v, g)]))
        tab[2026] = P.CUR[(v, g)]
        arr = np.full(self.NW, P.FLOOR[v])
        for i in range(self.NW):
            w, sy = self.SW[i]
            for yy, (pk, a, wd) in tab.items():
                off = w + (sy - yy) * 52
                arr[i] += (a - P.FLOOR[v]) * np.exp(-0.5 * ((off - pk) / wd) ** 2)
        return np.minimum(arr, 0.6)

    def build(self):
        rng = np.random.default_rng(self.seed)
        C = {(v, g): self.curve(v, g) for v in P.VIRUSES for g in P.POPS}
        self.PI, self.T, self.Pos = {}, {}, {}
        t = np.arange(self.NW) / 52.18
        for code, name, kind, mix, bases, tr, acc, grain, fac in P.LABS:
            for v, b in bases.items():
                pi = sum(m * C[(v, g)] for m, g in zip(mix, P.POPS))
                gam = P.GAMMA.get((code, v), P.GAMMA_DEFAULT[v])
                mu = b * (1 + tr) ** t * self.HOL * np.exp(gam * (pi - P.FLOOR[v]))
                T = rng.negative_binomial(P.NB_SIZE, P.NB_SIZE / (P.NB_SIZE + mu))
                self.PI[(code, v)] = pi
                self.T[(code, v)] = T
                self.Pos[(code, v)] = rng.binomial(T, pi)
        self.rng = rng
        return self
