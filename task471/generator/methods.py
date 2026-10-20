"""The ways of applying the audit to a municipality's register, each a set of post-strata: the golden and the rungs a
competent analyst stops at. Every method reads a person's features as the shipped files give them (see bundle.py),
fits the audit's absence rate in each stratum and gives each registered person the rate of their stratum."""
import collections

LINE = 5000


def addr_band(y):
    return 0 if y == 0 else 1 if y <= 4 else 2 if y <= 9 else 3


def band(y):
    return None if y is None else 0 if y == 0 else 1 if y <= 4 else 2 if y <= 9 else 3


# feature tuple fields: stay (completed years since the latest settlement from abroad, None if never settled from
# abroad), left (1 if the person left the country before that settlement), first (years since the first settlement),
# addr (completed years at the current address), abroad (born abroad), foreign (foreign nationality), age, sex
RUNGS = {
    "R1 one audit rate": lambda f: 0,
    "R2a born abroad": lambda f: f["abroad"],
    "R2a' foreign nationality": lambda f: f["foreign"],
    "R2b born abroad x years at the address": lambda f: (f["abroad"], addr_band(f["addr"])),
    "R2c current stay": lambda f: band(f["stay"]),
    "R2d first settlement x left before": lambda f: (band(f["first"]), f["left"]),
    "R2e left before": lambda f: (f["stay"] is None, f["left"]),
    "R2f years at the address x left before": lambda f: (f["stay"] is None, addr_band(f["addr"]), f["left"]),
    "R2g age and sex": lambda f: (min(f["age"] // 10, 8), f["sex"]),
    "G current stay x left before": lambda f: (band(f["stay"]), f["left"]),
}
GOLDEN = "G current stay x left before"
VARIANTS = {   # the golden's own family: any partition that carries the stay band and the earlier departure
    "Gy single years x left before": lambda f: (None if f["stay"] is None else min(f["stay"], 10), f["left"]),
    "Gb bands x left before x born abroad": lambda f: (band(f["stay"]), f["left"], f["abroad"]),
    "Gs bands x left before x sex": lambda f: (band(f["stay"]), f["left"], f["sex"]),
}


def fit(audit, key):
    """audit: list of (features, absent). Returns the stratum rates and the pooled rate."""
    c = collections.defaultdict(lambda: [0, 0])
    for f, a in audit:
        k = key(f)
        c[k][0] += a
        c[k][1] += 1
    pooled = sum(a for _, a in audit) / len(audit)
    return {k: a / n for k, (a, n) in c.items()}, pooled


def expected_absent(pop, rates, pooled, key):
    return sum(rates.get(key(f), pooled) for f in pop)


def adjusted(audit, pops, key):
    """municipality -> adjusted resident population (unrounded) under one method"""
    rates, pooled = fit(audit, key)
    return {m: len(pop) - expected_absent(pop, rates, pooled, key) for m, pop in pops.items()}


def qualifying(adj):
    return sorted(m for m, v in adj.items() if round(v) < LINE)
