"""The estimators of a household's income over the twelve full calendar months before the month it applied, and the
measure the criteria file, each computed on conformed application rows.

A row carries the hospital, its region, the main earner's kind of work, the household (one key across the hubs), its
size, the month it applied (1 to 12), the income the 2025 policy recorded for the three months before (times four, the
policy's yearly figure), the year and date of the decision and the share of the balance written off (100, 75, 50, 25
or 0 for a denial).

The calendar estimators read, for a cell of applications (a region's households in one kind of work, say), how the
policy's yearly figure moves with the month of application: the figure for an application in month m is the household's
level times the mean of the calendar over the three months before m, so the months' relative levels, scaled to average
one over the twelve months, are the factors that put each quarter on a yearly basis. A household's twelve-month income
is then the policy's figure divided by its month's factor. Each month is counted once in the year, so the factors
average one arithmetically over the twelve months."""
import collections

import numpy as np

FPL25 = (15650, 5500)
LIMIT = 200.0
SEASONAL = ("FIELD", "PACK", "FISH", "RESORT", "WOODS", "BUILD")


def fpl25(size):
    return FPL25[0] + FPL25[1] * (size - 1)


def pct(row, income):
    return income / fpl25(row["size"]) * 100.0


# ------------------------------------------------------------------------------------------- calendars
def _norm(f):
    f = np.asarray(f, float)
    return f / f.mean()


def cal_cross(rows, key, logs=False):
    """Each cell's factor by month of application: the mean of the policy's yearly figure (as a share of the guideline)
    over the cell's applications in that month, scaled to average one. logs reads the geometric mean in each month."""
    acc = collections.defaultdict(lambda: np.zeros((12, 2)))
    for x in rows:
        k = key(x)
        if k is None:
            continue
        v = pct(x, x["annual"])
        acc[k][x["month"] - 1] += (np.log(v) if logs else v, 1)
    out = {}
    for k, a in acc.items():
        if (a[:, 1] == 0).any():
            continue
        m = a[:, 0] / a[:, 1]
        out[k] = _norm(np.exp(m) if logs else m)
    return out


def cal_fe(rows, key, iters=60):
    """Each cell's factor from the households seen in more than one month: log of the yearly figure on a household
    effect and a month effect, the month effects exponentiated and scaled to average one."""
    cells = collections.defaultdict(list)
    for x in rows:
        k = key(x)
        if k is not None:
            cells[k].append(x)
    out = {}
    for k, xs in cells.items():
        hh = np.array([x["hh"] for x in xs])
        mo = np.array([x["month"] - 1 for x in xs])
        y = np.log([pct(x, x["annual"]) for x in xs])
        u, hidx = np.unique(hh, return_inverse=True)
        n = np.bincount(hidx)
        keep = n[hidx] >= 2
        if keep.sum() < 24:
            continue
        hidx = np.unique(hidx[keep], return_inverse=True)[1]
        mo, y = mo[keep], y[keep]
        if len(set(mo.tolist())) < 12:
            continue
        me = np.zeros(12)
        cnt_h = np.bincount(hidx)
        cnt_m = np.bincount(mo, minlength=12)
        for _ in range(iters):
            he = np.bincount(hidx, y - me[mo]) / cnt_h
            me = np.bincount(mo, y - he[hidx], minlength=12) / np.maximum(cnt_m, 1)
            me -= me.mean()
        out[k] = _norm(np.exp(me))
    return out


# ------------------------------------------------------------------------------------------- the measure
OWING = 50     # a decision leaves the household owing more than half its balance when it writes off less than this


def share(rows, est, year=2025):
    """Each hospital's share, in percent, of its first-review decisions in the year on households within the limit on
    est's twelve-month income that left the household owing more than half its balance (a denial or a 25 percent
    discount)."""
    num, den = collections.Counter(), collections.Counter()
    for x in rows:
        if x["year"] != year:
            continue
        if pct(x, est(x)) <= LIMIT:
            den[x["code"]] += 1
            if x["writeoff"] < OWING:
                num[x["code"]] += 1
    return {c: 100.0 * num[c] / den[c] for c in den}


def by_calendar(cals, key):
    def est(x):
        k = key(x)
        f = cals.get(k) if k is not None else None
        return x["annual"] if f is None else x["annual"] / f[x["month"] - 1]
    return est


# The keys: which applications share a calendar.
def k_region_kind(x):
    return (x["region"], x["kind"])


def k_region_kind_seasonal(x):
    return (x["region"], x["kind"]) if x["kind"] in SEASONAL else None


def k_hospital_kind(x):
    return (x["code"], x["kind"])


def k_kind(x):
    return x["kind"]


def k_seasonal(x):
    return "seasonal" if x["kind"] in SEASONAL else None


def k_region_seasonal(x):
    return x["region"] if x["kind"] in SEASONAL else None


def k_hospital_seasonal(x):
    return x["code"] if x["kind"] in SEASONAL else None


def calendar_rows(rows):
    """The rows a calendar is read from: every first-review decision in either year."""
    return rows


def golden(rows):
    cals = cal_cross(calendar_rows(rows), k_region_kind)
    return share(rows, by_calendar(cals, k_region_kind))


FAMILY = {
    "region_kind_mean": lambda rows: share(rows, by_calendar(cal_cross(rows, k_region_kind), k_region_kind)),
    "region_kind_log": lambda rows: share(rows, by_calendar(cal_cross(rows, k_region_kind, logs=True), k_region_kind)),
    "region_kind_fe": lambda rows: share(rows, by_calendar(_fe_or_cross(rows), k_region_kind)),
    "region_kind_seasonal_only": lambda rows: share(rows, by_calendar(cal_cross(rows, k_region_kind_seasonal),
                                                                      k_region_kind_seasonal)),
    "hospital_kind_mean": lambda rows: share(rows, by_calendar(cal_cross(rows, k_hospital_kind), k_hospital_kind)),
    "region_kind_2025_only": lambda rows: share(rows, by_calendar(cal_cross([x for x in rows if x["year"] == 2025],
                                                                            k_region_kind), k_region_kind)),
}


def _fe_or_cross(rows):
    """The households-seen-twice calendar where the cell identifies one (every month among its repeat households), the
    cell's own month means where it does not."""
    out = cal_cross(rows, k_region_kind)
    out.update(cal_fe(rows, k_region_kind))
    return out


def _own_average(rows):
    """Each household's yearly figure averaged over its applications within the twelve months before (a partial fix)."""
    byh = collections.defaultdict(list)
    for x in rows:
        byh[x["hh"]].append(x)

    def est(x):
        xs = [y for y in byh[x["hh"]] if 0 <= (x["mindex"] - y["mindex"]) < 12]
        return float(np.mean([y["annual"] for y in xs]))
    return est


REFLEXES = {
    "policy_quarter": lambda rows: share(rows, lambda x: x["annual"]),
    "one_seasonal_calendar": lambda rows: share(rows, by_calendar(cal_cross(rows, k_seasonal), k_seasonal)),
    "kind_calendar": lambda rows: share(rows, by_calendar(cal_cross(rows, k_kind), k_kind)),
    "region_calendar": lambda rows: share(rows, by_calendar(cal_cross(rows, k_region_seasonal), k_region_seasonal)),
    "hospital_calendar": lambda rows: share(rows, by_calendar(cal_cross(rows, k_hospital_seasonal),
                                                              k_hospital_seasonal)),
    "own_applications": lambda rows: share(rows, _own_average(rows)),
    "drop_seasonal": lambda rows: share([x for x in rows if x["kind"] not in SEASONAL], lambda x: x["annual"]),
    "geometric_scale": lambda rows: share(rows, by_calendar(_geo(cal_cross(rows, k_region_kind, logs=True)),
                                                            k_region_kind)),
}


def _geo(cals):
    """The execution error: factors scaled to a geometric mean of one rather than an arithmetic mean."""
    return {k: f / np.exp(np.log(f).mean()) for k, f in cals.items()}


def family(rows, names=None):
    return {n: f(rows) for n, f in FAMILY.items() if names is None or n in names}


def reflexes(rows, names=None):
    return {n: f(rows) for n, f in REFLEXES.items() if names is None or n in names}
