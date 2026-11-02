"""Estimators of each cremation's amalgam-restored teeth from the survey's published tables, and the regulation's
arithmetic. Used by the goldens, the checks and the ceiling; verify.py has its own."""
import math

import numpy as np

import world as W


def band(tab, y, s, a):
    """The wave's published mean for the band holding age a (an age under 18 reads the youngest band)."""
    for (yy, ss, lo), cell in tab.items():
        if yy == y and ss == s and cell["lo"] <= max(a, 18) <= cell["hi"]:
            return cell["amalgam"]
    raise KeyError((y, s, a))


def interp(tab, y, s, a):
    """The wave's band means read at single years of age (linear between band midpoints, flat beyond the ends)."""
    pts = sorted((cell["lo"] + (min(cell["hi"], cell["lo"] + 4) - cell["lo"]) / 2.0 if cell["hi"] < 100 else cell["lo"] + 2.5,
                  cell["amalgam"]) for (yy, ss, lo), cell in tab.items() if yy == y and ss == s)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    if y == 1996:
        xs = [cell_mid for cell_mid in xs]
    return float(np.interp(max(a, 18), xs, ys))


def _cohort_add(tab, a, s, lag=10, rd=band):
    c16 = rd(tab, 2016, s, a - lag)
    c06 = rd(tab, 2006, s, a - lag - 10)
    return max(0.0, 2 * c16 - c06)


def teeth(tab, a, s, form):
    """Teeth restored with amalgam for a person cremated in 2026 at age a (completed years), sex s."""
    if a < 18 and not form.startswith("child_"):
        return 0.0                                    # the regulation's schedule: nil under 18
    if form == "count":
        return 1.0
    if form == "age2016":
        return band(tab, 2016, s, a)
    if form == "age2016_interp":
        return interp(tab, 2016, s, a)
    if form == "age2006":
        return band(tab, 2006, s, a)
    if form == "age_trend":                           # each age band's change between the last two waves, repeated
        return max(0.0, 2 * band(tab, 2016, s, a) - band(tab, 2006, s, a))
    if form == "age_trend3":                          # each age band's line through the three waves, to 2026
        ys = np.array([band(tab, 1996, s, a), band(tab, 2006, s, a), band(tab, 2016, s, a)])
        b1 = np.polyfit(np.array([-20.0, -10.0, 0.0]), ys, 1)
        return max(0.0, b1[0] * 10 + b1[1])
    if form == "age_trend_prop":
        v16, v06 = band(tab, 2016, s, a), band(tab, 2006, s, a)
        return v16 * v16 / v06 if v06 > 0 else v16
    c16 = band(tab, 2016, s, a - 10)
    c06 = band(tab, 2006, s, a - 20)
    if form == "cohort_noage":                        # the cohort's 2016 value, not carried
        return c16
    if form == "cohort_along_2016":                   # carried along the 2016 cross-section (equals age2016)
        return c16 + (band(tab, 2016, s, a) - band(tab, 2016, s, a - 10))
    if form == "cohort_add":
        return max(0.0, 2 * c16 - c06)
    if form == "cohort_prop":
        return c16 * c16 / c06 if c06 > 0 else c16
    if form == "cohort_logit":
        L = lambda p: math.log(p / (1 - p))
        x = 2 * L(max(c16, 0.05) / 32) - L(max(c06, 0.05) / 32)
        return 32 / (1 + math.exp(-x))
    if form == "cohort_age_specific":                 # the decade's change at these ages, from the cohort before
        aa = min(a, 89)                               # the open top band holds no decade of one cohort
        return max(0.0, c16 + (band(tab, 2016, s, aa) - band(tab, 2006, s, aa - 10)))
    if form == "cohort_mean_decrement":               # the mean within-cohort decade change over cohorts aged 45+
        return max(0.0, c16 + mean_decrement(tab, s))
    if form in ("cohort_line3", "cohort_logline3"):
        c96 = band(tab, 1996, s, a - 30)
        t, ys = np.array([-20.0, -10.0, 0.0]), np.array([c96, c06, c16])
        if form == "cohort_line3":
            b1 = np.polyfit(t, ys, 1)
            return max(0.0, b1[0] * 10 + b1[1])
        b1 = np.polyfit(t, np.log(np.maximum(ys, 0.05)), 1)
        return math.exp(b1[0] * 10 + b1[1])
    if form == "cohort_quad3":                        # a quadratic through the three waves (ruled out: SF23)
        c96 = band(tab, 1996, s, a - 30)
        return max(0.0, 3 * c16 - 3 * c06 + c96)
    if form == "cohort_pooled_sex":
        return 0.5 * (_cohort_add(tab, a, "M") + _cohort_add(tab, a, "F"))
    if form == "cohort_interp":                       # single years of age read off the band midpoints
        return _cohort_add(tab, a, s, rd=interp)
    if form == "cohort_lag9":                         # the survey a year later in the decedent's life
        return _cohort_add(tab, a, s, lag=9)
    if form == "cohort_lag11":
        return _cohort_add(tab, a, s, lag=11)
    if form == "cohort_split":                        # half the decedents a year younger at the survey
        return 0.5 * (_cohort_add(tab, a, s, lag=10) + _cohort_add(tab, a, s, lag=11))
    if form == "cohort_lagmix":                       # age at the survey by single years: deaths and fieldwork mid-year
        return (0.125 * _cohort_add(tab, a, s, lag=9) + 0.75 * _cohort_add(tab, a, s, lag=10) +
                0.125 * _cohort_add(tab, a, s, lag=11))
    if form == "cohort_young_profile":                # cohorts not surveyed as adults in 2006 read at age at death
        return band(tab, 2016, s, a) if a - 20 < 18 else max(0.0, 2 * c16 - c06)
    if form == "cohort_young_zero":
        return 0.0 if a - 20 < 18 else max(0.0, 2 * c16 - c06)
    if form == "cohort_young_noage":
        return c16 if a - 20 < 18 else max(0.0, 2 * c16 - c06)
    raise ValueError(form)


def mean_decrement(tab, s):
    """Average change in a cohort's mean between 2006 and 2016, over the 5-year cohorts aged 45 and over in 2006."""
    d = []
    for (yy, ss, lo), cell in tab.items():
        if yy == 2006 and ss == s and 45 <= lo <= 80 and cell["hi"] < 100:
            d.append(band(tab, 2016, s, lo + 10) - cell["amalgam"])
    return float(np.mean(d))


FORMS = ["cohort_add", "cohort_age_specific", "cohort_mean_decrement", "cohort_line3", "cohort_pooled_sex",
         "cohort_interp", "cohort_lagmix", "cohort_young_profile", "cohort_young_zero", "cohort_young_noage"]
SCALING = ["cohort_prop", "cohort_logit", "cohort_logline3"]   # a change that scales with the level: the waves refute it
OFF_BY_ONE = ["cohort_lag9", "cohort_lag11", "cohort_split"]
RULED_OUT = ["cohort_quad3"]                                  # untestable curvature the waves do not show (SF23)
ROUTES = ["count", "age2016", "age2016_interp", "age2006", "age_trend", "age_trend3", "age_trend_prop", "cohort_noage",
          "cohort_along_2016"]
GOLDEN_FORM = "cohort_add"


def designate(cre, tab, form):
    """cre: list of (crematorium index, age, sex, abated) for the 2026 cremations. Returns the share, the designated
    crematoria (indices, in order), the order of unabated crematoria, each crematorium's mercury in grams and the
    share after each designation."""
    n = len(W.CREMATORIA)
    hg, ab = np.zeros(n), np.zeros(n)
    cache = {}
    for ci, a, s, abt in cre:
        k = (a, s)
        if k not in cache:
            cache[k] = teeth(tab, a, s, form)
        v = cache[k] * W.HG_PER_TOOTH_G
        hg[ci] += v
        if abt:
            ab[ci] += v
    tot = hg.sum()
    share = 100 * ab.sum() / tot
    unab = [i for i, c in enumerate(W.CREMATORIA) if c[8] == "U"]
    order = sorted(unab, key=lambda i: -hg[i])
    des, cur, steps = [], ab.sum(), []
    for i in order:
        steps.append(100 * cur / tot)
        if 100 * cur / tot >= W.SHARE_REQUIRED:
            break
        des.append(i)
        cur += hg[i]
    else:
        steps.append(100 * cur / tot)
    return {"share": share, "des": des, "order": order, "hg": hg, "ab": ab, "steps": steps, "tot": tot}
