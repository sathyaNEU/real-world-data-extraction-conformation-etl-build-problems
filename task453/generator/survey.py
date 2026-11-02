"""The national adult oral health survey: the truth (teeth restored with amalgam per adult, by birth year, age and sex)
and the three waves' published tables. Amalgam is carried by cohort: those born in the late 1940s to late 1950s hold
the most, earlier cohorts lost their teeth, later ones grew up with fluoride and resin; within a cohort the count
falls by about a tooth a decade from middle age."""
import math
import numpy as np

K = 0.100                                # teeth restored with amalgam lost per year of age after 45 (every cohort)
G_OLD, W_OLD = 5.6, 12.0                 # the cohorts born before the peak: their floor and how fast they fall to it


def gamma(b, s):
    if b <= 1952:
        g = G_OLD + (9.5 - G_OLD) * math.exp(-((b - 1952) / W_OLD) ** 2)
    else:
        g = 3.6 + 5.9 * math.exp(-((b - 1952) / 13.0) ** 2)
    return g + (0.25 if s == "F" else -0.25)


def truth(b, a, s):
    """Mean teeth restored with amalgam per adult (no natural teeth counted as none) for birth year b at age a."""
    return max(0.0, gamma(b, s) - K * max(0, a - 45)) if a >= 45 else gamma(b, s) - 0.06 * (45 - a)


def edentulous(b, a):
    m = 101 + 0.35 * (b - 1930)
    return 1 / (1 + math.exp(-(a - m) / 7.5))


WAVES = (1996, 2006, 2016)
BANDS = {1996: [(18, 24)] + [(lo, lo + 4) for lo in range(25, 80, 5)] + [(80, 104)],
         2006: [(18, 24)] + [(lo, lo + 4) for lo in range(25, 90, 5)] + [(90, 104)],
         2016: [(18, 24)] + [(lo, lo + 4) for lo in range(25, 90, 5)] + [(90, 104)]}


def band_label(lo, hi):
    return "%d and over" % lo if hi >= 100 else "%d to %d" % (lo, hi)


DEFF = 1.3                               # design effect of the clustered household sample


def sample_size(rng, y, lo, hi):
    """Adults examined in a band and sex: older adults sampled at a higher rate from 2006."""
    scale = 0.62 if y == 1996 else 1.0
    if hi >= 100:
        base = rng.integers(95, 165)
    elif lo >= 85:
        base = rng.integers(170, 260)
    elif lo >= 45:
        base = rng.integers(560, 780)
    else:
        base = rng.integers(240, 360)
    return int(base * scale)


def tables(seed):
    """Published means to one decimal per wave, band and sex, each with its sampling error, and the adults examined."""
    rng = np.random.default_rng(seed)
    out = {}
    for y in WAVES:
        for lo, hi in BANDS[y]:
            ages = np.arange(lo, hi + 1)
            w = np.exp(-np.maximum(0, ages - 86) / 4.0) * np.exp(-np.maximum(0, 30 - ages) / 40.0)
            for s in "MF":
                v = float(np.average([truth(y - a, a, s) for a in ages], weights=w))
                e = float(np.average([edentulous(y - a, a) for a in ages], weights=w))
                n = sample_size(rng, y, lo, hi)
                sd = math.sqrt(1.0 + 1.6 * v)                        # an over-dispersed count of teeth
                se = DEFF * sd / math.sqrt(n)
                vv = round(max(0.0, v + rng.normal(0, se)), 1)
                ee = round(min(99.0, max(0.0, 100 * e + rng.normal(0, 100 * DEFF * math.sqrt(max(e * (1 - e), 0.0004) / n)))), 1)
                out[(y, s, lo)] = {"lo": lo, "hi": hi, "amalgam": vv, "se": round(se, 2), "edentulous_pct": ee, "n": n}
        for lo, hi in BANDS[y]:
            m, f = out[(y, "M", lo)], out[(y, "F", lo)]
            nn = m["n"] + f["n"]
            out[(y, "A", lo)] = {"lo": lo, "hi": hi, "amalgam": round((m["amalgam"] * m["n"] + f["amalgam"] * f["n"]) / nn, 1),
                                 "se": round(math.sqrt((m["se"] * m["n"]) ** 2 + (f["se"] * f["n"]) ** 2) / nn, 2),
                                 "edentulous_pct": round((m["edentulous_pct"] * m["n"] + f["edentulous_pct"] * f["n"]) / nn, 1),
                                 "n": nn}
    return out
