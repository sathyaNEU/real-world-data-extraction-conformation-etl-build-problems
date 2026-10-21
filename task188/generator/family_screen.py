"""The three pre-design screens, on the generator's clean truth, in one command.

    python3 task188/generator/family_screen.py [redraws]     (default 20)

Screen 1, the estimator family. Once the filed WHAT is read (protocol 3.1, 3.2, 3.6 and 4.1 and the
prompt's "per CO2 trap-night" fix the population, outcome, window, unit and comparison), the only thing
left open is how the infected share of a pooled-tested population is estimated. This enumerates every
construction a competent analyst would use for that and prints all four graded figures under each. A
spread of zero on the designation means the step is a reflex whatever the documents say.

Screen 2, the algebra. The one-group-by route to the call, in one line:

    index(z) = sum over the two species of (CO2 pools / CO2 trap-nights) times (- ln(share of pools negative))

no pool size anywhere. With tested females T = m * nbar and pools of one size n the maximum likelihood
estimate solves (1 - p)^n = 1 - q exactly, so T * p_hat = m * n * (1 - (1 - q)^(1/n)) tends to
m * (- ln(1 - q)) as n grows: the pool size cancels out of the leading term, so the infected-female count
a zone's pools imply turns on how many pools it ran and what share came back negative, not on how big the
pools were. This prints the correlation, the departure and the designation of that route against the
designed construction.

Screen 3, the lever against the ceiling, over redraws of the night-level world: the separation the
decisive step buys on the graded quantity against the spread the licensed family itself puts on the same
figure.

Two runs of this file give byte-identical output.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import cases as C                      # noqa: E402
import records as R                    # noqa: E402
import world as W                      # noqa: E402
from scipy.integrate import quad       # noqa: E402
from scipy.optimize import brentq      # noqa: E402

Z = W.ZONES
VEC = W.VECTORS
UNIT = 0.1          # the printed unit of the two zone figures, from the prompt's closing sentence


# ---------------------------------------------------------------- the pooled likelihood
def _score(pools, p):
    u = 0.0
    for m, x in pools:
        q = (1.0 - p) ** m
        d1 = m * (1.0 - p) ** (m - 1)
        u += (d1 / (1.0 - q)) if x else (-d1 / q)
    return u


def _parts(pools, p):
    u = i = di = k = 0.0
    for m, x in pools:
        q = (1.0 - p) ** m
        pi = 1.0 - q
        d1 = m * (1.0 - p) ** (m - 1)
        d2 = -m * (m - 1) * (1.0 - p) ** (m - 2)
        u += (d1 / pi) if x else (-d1 / q)
        den = pi * q
        i += d1 * d1 / den
        di += (2.0 * d1 * d2 * den - d1 * d1 * d1 * (1.0 - 2.0 * pi)) / (den * den)
        k += d1 * d2 / den - d1 ** 3 * (1.0 / pi ** 2 - 1.0 / q ** 2)
    return u, i, di, k


def _loglik(pools, p):
    t = 0.0
    for m, x in pools:
        q = (1.0 - p) ** m
        t += math.log1p(-q) if x else math.log(q)
    return t


def _solve(f, lo=1e-12, hi=0.6):
    try:
        return brentq(f, lo, hi, xtol=1e-15)
    except ValueError:
        return float("nan")


def _empty(pools):
    return not any(x for m, x in pools)


def mle(pools):
    """1 Maximum likelihood for pools of unequal size (Walter, Hughes and Gu). The build's golden estimator."""
    if _empty(pools):
        return 0.0
    if all(x for m, x in pools):
        return float("nan")
    return _solve(lambda p: _score(pools, p))


def firth(pools):
    """2 Firth bias-corrected maximum likelihood (modified score)."""
    if _empty(pools):
        return 0.0
    return _solve(lambda p: _parts(pools, p)[0] - (_parts(pools, p)[3] - _parts(pools, p)[2]) /
                  (2.0 * _parts(pools, p)[1]))


def jeffreys(pools):
    """3 Jeffreys-penalised likelihood."""
    if _empty(pools):
        return 0.0

    def f(p):
        u, i, di, k = _parts(pools, p)
        return u + 0.5 * di / i
    return _solve(f)


def _post(pools, a, b, want):
    lo, hi = 1e-12, 0.6
    mx = max(_loglik(pools, lo + i * (hi - lo) / 400) for i in range(401))

    def dens(p):
        return math.exp(_loglik(pools, p) - mx) * p ** (a - 1.0) * (1.0 - p) ** (b - 1.0)
    norm = quad(dens, lo, hi, limit=200)[0]
    if want == "mean":
        return quad(lambda p: p * dens(p), lo, hi, limit=200)[0] / norm
    return _solve(lambda t: quad(dens, lo, t, limit=200)[0] / norm - 0.5, lo + 1e-9, hi)


def bayes_unif_mean(pools):
    """4 Posterior mean, uniform Beta(1,1) prior."""
    return 0.0 if _empty(pools) else _post(pools, 1.0, 1.0, "mean")


def bayes_jeff_mean(pools):
    """5 Posterior mean, Jeffreys Beta(0.5,0.5) prior."""
    return 0.0 if _empty(pools) else _post(pools, 0.5, 0.5, "mean")


def bayes_unif_median(pools):
    """6 Posterior median, uniform Beta(1,1) prior."""
    return 0.0 if _empty(pools) else _post(pools, 1.0, 1.0, "median")


def equalsize_mean(pools):
    """7 The equal-pool-size closed form at the mean pool size."""
    m = len(pools)
    if not m:
        return 0.0
    q = sum(1 for n, x in pools if x) / m
    nbar = sum(n for n, x in pools) / m
    return float("nan") if q >= 1.0 else 1.0 - (1.0 - q) ** (1.0 / nbar)


def cloglog(pools):
    """8 The Poisson / complementary log-log approximation."""
    m = len(pools)
    if not m:
        return 0.0
    q = sum(1 for n, x in pools if x) / m
    nbar = sum(n for n, x in pools) / m
    return float("nan") if q >= 1.0 else -math.log(1.0 - q) / nbar


def size_stratified(pools):
    """9 Chiang and Reeves: the equal-size form inside each distinct pool size, combined by mosquitoes tested."""
    by = {}
    for n, x in pools:
        by.setdefault(n, []).append(x)
    num = den = 0.0
    for n, xs in by.items():
        y = sum(1 for x in xs if x)
        q = y / len(xs)
        if q >= 1.0:
            q = (y - 0.5) / len(xs)
        w = n * len(xs)
        num += w * (1.0 - (1.0 - q) ** (1.0 / n))
        den += w
    return num / den if den else 0.0


def glm_cloglog(pools):
    """10 A binomial GLM, complementary log-log link, log(pool size) offset, intercept only. The textbook
    regression route to a pooled prevalence, and numerically the maximum likelihood estimate."""
    if _empty(pools):
        return 0.0
    b = -3.0
    for _ in range(200):
        g = h = 0.0
        for n, x in pools:
            e = math.exp(b + math.log(n))
            mu = min(max(-math.expm1(-e), 1e-15), 1 - 1e-15)
            d = e * math.exp(-e)
            g += (x - mu) * d / (mu * (1 - mu))
            h += d * d / (mu * (1 - mu))
        if h <= 0:
            break
        step = g / h
        b += step
        if abs(step) < 1e-14:
            break
    return -math.expm1(-math.exp(b))


def mle_full_only(pools):
    """11 Maximum likelihood on the full pools only, the remainder pools dropped."""
    if not pools:
        return 0.0
    nmax = max(n for n, x in pools)
    sub = [(n, x) for n, x in pools if n == nmax]
    if _empty(sub) or all(x for n, x in sub):
        return mle(pools)
    return _solve(lambda p: _score(sub, p))


def mir(pools):
    """R Minimum infection rate, positive pools over mosquitoes tested: protocol 4.1's pools of up to 50
    are what a reader quotes against it."""
    tested = sum(n for n, x in pools)
    return (sum(1 for n, x in pools if x) / tested) if tested else 0.0


FAMILY = [("1 MLE unequal pool sizes (golden)", mle), ("2 Firth bias-corrected MLE", firth),
          ("3 Jeffreys-penalised likelihood", jeffreys), ("4 Bayes mean, uniform prior", bayes_unif_mean),
          ("5 Bayes mean, Jeffreys prior", bayes_jeff_mean), ("6 Bayes median, uniform prior", bayes_unif_median),
          ("7 equal-size form at mean size", equalsize_mean), ("8 cloglog/Poisson approximation", cloglog),
          ("9 Chiang-Reeves size-stratified", size_stratified), ("10 binomial GLM, cloglog, size offset", glm_cloglog),
          ("11 MLE on full pools only", mle_full_only), ("12 MLE by size stratum, recombined", size_stratified)]


# ---------------------------------------------------------------- the clean truth
class Truth:
    def __init__(self, w):
        sim, flat = w["sim"], w["flat"]
        self.tn = [(r, c) for r, c in zip(sim["tn"], sim["catches"])
                   if r["year"] == 2026 and r["week"] == 32 and r["origin"] == "field"]
        self.pools = [p for p in flat if p["year"] == 2026 and p["week"] == 32]

    def _run(self, z):
        return [(r, c) for r, c in self.tn if r["zone"] == z and r["trap_type"] == "CO2" and r["status"] == "OK"]

    def abundance(self, z):
        t = self._run(z)
        return {sp: sum(n for r, c in t for s, sex, n in c if s == sp and sex == "F") / len(t) for sp in VEC}

    def ntn(self, z):
        return len(self._run(z))

    def pl(self, z, which="CO2"):
        out = {sp: [] for sp in VEC}
        for p in self.pools:
            if p["zone"] == z and (which == "ALL" or p["trap_type"] == "CO2"):
                out[p["species"]].append((p["females"], p["final"] == "POS"))
        return out

    def index(self, z, est, which="CO2"):
        ab, pl = self.abundance(z), self.pl(z, which)
        return sum(ab[sp] * est(pl[sp]) for sp in VEC)


def cheap(T, z):
    """Screen 2's one-group-by route: pools per trap-night times minus the log of the negative share."""
    tn, pl, out = T.ntn(z), T.pl(z), 0.0
    for sp in VEC:
        pools = pl[sp]
        if not pools:
            continue
        q = sum(1 for n, x in pools if x) / len(pools)
        if q >= 1.0:
            return float("nan")
        out += (len(pools) / tn) * (-math.log(1.0 - q))
    return out


def positive_pools_per_tn(T, z):
    return sum(1 for sp in VEC for n, x in T.pl(z)[sp] if x) / T.ntn(z)


def corr(a, b):
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    sa = math.sqrt(sum((x - ma) ** 2 for x in a))
    sb = math.sqrt(sum((x - mb) ** 2 for x in b))
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb) if sa and sb else float("nan")


def world(k=None):
    if k is not None:
        W.SALT = {z: 1000 + 97 * k + 13 * i for i, z in enumerate(Z)}
    sim = R.simulate()
    return dict(sim=sim, flat=R.number_pools(sim), cases=C.build())


def screen1(T):
    print("=" * 104)
    print("SCREEN 1  the estimator family the filed rules leave open")
    print("=" * 104)
    print("%-40s %-14s %6s %-14s %6s %6s" % ("construction", "call", "fig", "runner-up", "fig", "flip"))
    out = []
    for name, est in FAMILY + [("R minimum infection rate", mir)]:
        idx = {z: T.index(z, est) for z in Z}
        order = sorted(Z, key=lambda z: -idx[z])
        call, second = order[0], order[1]
        flip = idx[second] / sum(T.abundance(call).values()) * 1000.0
        print("%-40s %-14s %6.1f %-14s %6.1f %6d" % (
            name, call, round(idx[call], 1), second, round(idx[second], 1), round(flip)))
        out.append({"name": name, "call": call, "cf": idx[call], "second": second, "sf": idx[second], "flip": flip})
    fam = out[:len(FAMILY)]
    calls = {r["call"] for r in fam}
    print("-" * 104)
    print("  designated zone : %d distinct %s" % (len(calls), sorted(calls)))
    print("  call figure     : %d distinct printed values %s, exact spread %.4f = %.1f x the printed unit" % (
        len({round(r["cf"], 1) for r in fam}), sorted({round(r["cf"], 1) for r in fam}),
        max(r["cf"] for r in fam) - min(r["cf"] for r in fam),
        (max(r["cf"] for r in fam) - min(r["cf"] for r in fam)) / UNIT))
    print("  runner-up figure: %d distinct printed values %s, exact spread %.4f" % (
        len({round(r["sf"], 1) for r in fam}), sorted({round(r["sf"], 1) for r in fam}),
        max(r["sf"] for r in fam) - min(r["sf"] for r in fam)))
    print("  flip rate       : %d distinct printed values %s, exact spread %.3f" % (
        len({round(r["flip"]) for r in fam}), sorted({round(r["flip"]) for r in fam}),
        max(r["flip"] for r in fam) - min(r["flip"] for r in fam)))
    return fam


def screen2(T):
    des = {z: T.index(z, mle) for z in Z}
    ch = {z: cheap(T, z) for z in Z}
    mi = {z: T.index(z, mir) for z in Z}
    pp = {z: positive_pools_per_tn(T, z) for z in Z}
    order = sorted(Z, key=lambda z: -des[z])
    print()
    print("=" * 104)
    print("SCREEN 2  the cheapest licensed construction, and the algebra")
    print("=" * 104)
    print("%-16s %9s %9s %8s %9s %9s" % ("zone", "designed", "cheap", "ratio", "pos/tn", "MIR index"))
    for z in order:
        print("%-16s %9.4f %9.4f %8.5f %9.4f %9.4f" % (z, des[z], ch[z], ch[z] / des[z], pp[z], mi[z]))
    a, b = [des[z] for z in Z], [ch[z] for z in Z]
    print("-" * 104)
    print("  corr(designed, one-group-by route)            = %+.6f" % corr(a, b))
    print("  designation: one-group-by %s, designed %s" % (max(Z, key=lambda z: ch[z]), order[0]))
    print("  corr(MIR index, positive pools per trap-night) = %+.6f, max |difference| %.3e (an identity)" % (
        corr([mi[z] for z in Z], [pp[z] for z in Z]), max(abs(mi[z] - pp[z]) for z in Z)))
    return des, ch


def screen3(n):
    print()
    print("=" * 104)
    print("SCREEN 3  the lever against the ceiling, %d redraws" % n)
    print("=" * 104)
    print("%4s %-14s %-14s %7s %8s %8s %6s %-14s" % (
        "draw", "call", "runner-up", "lever", "ceiling", "lev/ceil", "agree", "cheap route"))
    rows = []
    for k in range(n):
        T = Truth(world(k))
        live = {}
        for name, est in FAMILY:
            try:
                live[name] = {z: T.index(z, est) for z in Z}
            except Exception:
                pass
        g = live["1 MLE unequal pool sizes (golden)"]
        order = sorted(Z, key=lambda z: -g[z])
        call, second = order[0], order[1]
        named = {max(Z, key=lambda z: v[z]) for v in live.values()}
        figs = [v[call] for v in live.values()]
        ch = {z: cheap(T, z) for z in Z}
        r = {"call": call, "lever": g[call] - g[second], "ceiling": max(figs) - min(figs),
             "distinct": len(named), "agree": sum(1 for v in live.values() if max(Z, key=lambda z: v[z]) == call),
             "n": len(live), "cheap": max(Z, key=lambda z: ch[z])}
        rows.append(r)
        print("%4d %-14s %-14s %7.3f %8.3f %8.2f %4d/%-2d %-14s" % (
            k, call, second, r["lever"], r["ceiling"], r["lever"] / r["ceiling"] if r["ceiling"] else 0,
            r["agree"], r["n"], r["cheap"]))
    t = len(rows)
    print("-" * 104)
    print("  redraws where the family splits on the designation  : %d of %d (mean %.2f distinct zones)" % (
        sum(1 for r in rows if r["distinct"] > 1), t, sum(r["distinct"] for r in rows) / t))
    print("  redraws where the one-group-by route names the call : %d of %d" % (
        sum(1 for r in rows if r["cheap"] == r["call"]), t))
    print("  lever   mean %.3f, range %.3f to %.3f" % (
        sum(r["lever"] for r in rows) / t, min(r["lever"] for r in rows), max(r["lever"] for r in rows)))
    print("  ceiling mean %.3f (%.1f x the printed unit), range %.3f to %.3f" % (
        sum(r["ceiling"] for r in rows) / t, sum(r["ceiling"] for r in rows) / t / UNIT,
        min(r["ceiling"] for r in rows), max(r["ceiling"] for r in rows)))
    rat = [r["lever"] / r["ceiling"] for r in rows if r["ceiling"]]
    print("  lever over ceiling mean %.2f, range %.2f to %.2f" % (sum(rat) / len(rat), min(rat), max(rat)))


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    T = Truth(world())
    screen1(T)
    screen2(T)
    screen3(n)


if __name__ == "__main__":
    main()
