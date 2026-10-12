"""The numeric world: schools, regions, cohorts, school and year-group effects and the Year 5 reading scores of
participating students at the three sittings. Everything else in the pack is laid on top of this with its
own random streams, so filler never moves the core."""
import numpy as np

REGIONS = ["MN", "MS", "NO", "WE", "SO", "CO"]           # two metropolitan, four regional
N_SCHOOLS = {"MN": 58, "MS": 52, "NO": 41, "WE": 36, "SO": 43, "CO": 34}
METRO = {"MN", "MS"}
# region centres (km on a local grid) and spreads
CENTRE = {"MN": (34.0, 52.0), "MS": (40.0, 4.0), "NO": (115.0, 195.0), "WE": (195.0, 25.0),
          "SO": (115.0, -125.0), "CO": (25.0, 440.0)}
SPREAD = {"MN": (15.0, 13.0), "MS": (17.0, 13.0), "NO": (55.0, 50.0), "WE": (55.0, 55.0),
          "SO": (45.0, 40.0), "CO": (34.0, 135.0)}
SITTINGS = [2024, 2025, 2026]
MU, SD_SCHOOL, SD_GROUP, SD_STUDENT = 497.0, 17.0, 10.0, 70.0


def _normal_quantiles(k):
    # Blom positions on the inverse normal, no scipy: Acklam's rational approximation
    p = (np.arange(1, k + 1) - 0.375) / (k + 0.25)
    return np.array([_ppf(x) for x in p])


def _ppf(p):
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02, 1.383577518672690e+02,
         -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02, 6.680131188771972e+01,
         -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00, -2.549671010173219e+00,
         4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00, 3.754408661907416e+00]
    lo = 0.02425
    if p < lo:
        q = np.sqrt(-2 * np.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
            ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    if p > 1 - lo:
        return -_ppf(1 - p)
    q = p - 0.5
    r = q * q
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / \
        (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)


def draw(seed, shift=0.0, sd_group=SD_GROUP):
    rng = np.random.default_rng(seed)
    region = np.concatenate([[r] * N_SCHOOLS[r] for r in REGIONS])
    S = len(region)
    metro = np.array([r in METRO for r in region])
    # location
    xy = np.zeros((S, 2))
    for r in REGIONS:
        m = region == r
        xy[m] = np.array(CENTRE[r]) + rng.normal(size=(m.sum(), 2)) * np.array(SPREAD[r])
    # 2026 Year 5 enrolment: metropolitan schools larger
    n5 = np.where(metro, np.exp(rng.normal(np.log(60), 0.45, S)), np.exp(rng.normal(np.log(23), 0.60, S)))
    # coastal schools away from the towns are small
    co = region == "CO"
    n5[co] = np.exp(rng.normal(np.log(12), 0.55, co.sum()))
    n5 = np.clip(np.round(n5), 5, 168)
    # cohort trend per year level (younger cohorts larger in the city, smaller in the regions)
    g = np.where(metro, rng.uniform(1.030, 1.040, S), rng.uniform(0.945, 0.958, S))
    # school effects: shuffled normal quantiles
    u = _normal_quantiles(S) * SD_SCHOOL
    u = u[rng.permutation(S)]
    enrol = np.zeros((S, 3), int)
    for j, yr in enumerate(SITTINGS):
        base = n5 / g ** (2 - j)          # earlier sittings' Year 5 cohorts follow the trend
        enrol[:, j] = np.maximum(4, rng.poisson(base))
    # participation
    part = np.zeros((S, 3), int)
    for j in range(3):
        rate = rng.beta(60, 3.2, S)
        part[:, j] = np.maximum(4, rng.binomial(enrol[:, j], rate))
    v = rng.normal(0, sd_group, (S, 3))
    scores = []
    for j in range(3):
        for i in range(S):
            e = rng.normal(0, SD_STUDENT, part[i, j])
            y = MU + shift + u[i] + v[i, j] + e
            y = np.round(y, 1) if j == 0 else np.round(y)
            scores.append((i, j, y))
    return {"shift": shift, "region": region, "metro": metro, "xy": xy, "n5": n5, "g": g, "u": u, "v": v,
            "enrol": enrol, "part": part, "scores": scores, "S": S}


def frame(w):
    import pandas as pd
    s = np.concatenate([[i] * len(y) for i, j, y in w["scores"]])
    t = np.concatenate([[j] * len(y) for i, j, y in w["scores"]])
    y = np.concatenate([y for i, j, y in w["scores"]])
    return pd.DataFrame({"school": s, "sitting": t, "score": y})
