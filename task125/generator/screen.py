"""The digit screen, the statements, every rung and the correction grid, computed from the payment
records the pack ships (the generator's own path; verify.py recomputes all of it from the bytes)."""
from collections import Counter, defaultdict

import params as PR

BASES = [(amt, rng, cr) for amt in ("net", "gross") for rng in ("pub", "dec", "unc") for cr in ("excl", "abs")]
CORRECT = ("gross", "dec", "excl")


def basis_amount(p, amt, cr):
    """p: (dept, date, net_p, vat_p). Returns the screened amount in pence, or None when not screened."""
    v = p[2] if amt == "net" else p[2] + p[3]
    if v < 0:
        if cr == "excl":
            return None
        v = -v
    return v


def in_range(v, rng):
    if rng == "pub":
        return v > 0
    if rng == "dec":
        return 100000 <= v <= 99999999
    return v >= 100000


def cell_p(v):
    return int(str(v // 100)[:2])


def screen_counts(pays, basis):
    """counts[(fy, dept)][cell] for the screen years."""
    amt, rng, cr = basis
    out = defaultdict(Counter)
    for p in pays:
        fy = PR.fy_of(p[1])
        if fy not in PR.SCREEN_YEARS:
            continue
        v = basis_amount(p, amt, cr)
        if v is None or not in_range(v, rng):
            continue
        out[(fy, p[0])][cell_p(v)] += 1
    return out


def mad(cnt):
    n = sum(cnt.values())
    return sum(abs(cnt.get(c, 0) / n - PR.P[c]) for c in range(10, 100)) / 90


def flags(cnt):
    n = sum(cnt.values())
    out = {}
    for c in range(10, 100):
        e = PR.P[c] * n
        thr = max(1.5 * e, e + 30)
        k = cnt.get(c, 0)
        out[c] = (k > 1.5 * e and k - e >= 30, k / thr)
    return out


def statements(counts, depts):
    """The published figures: per year, the council-wide MAD and each department's payments tested and MAD."""
    st = {}
    for fy in PR.SCREEN_YEARS:
        pooled = Counter()
        for d in depts:
            c = counts.get((fy, d), Counter())
            pooled.update(c)
            st[(fy, d, "tested")] = sum(c.values())
            st[(fy, d, "mad")] = "%.5f" % mad(c) if c else "n/a"
        st[(fy, "ALL", "mad")] = "%.5f" % mad(pooled)
    return st


def flagged_cells(counts, fy, depts):
    out = set()
    for d in depts:
        for c, (f, _) in flags(counts.get((fy, d), Counter())).items():
            if f:
                out.add((d, c))
    return out


def routed_in(pays, cells, basis, fy="2025/26"):
    """Payments of 1,000 pounds or more (on the basis amount) dated in fy whose department-cell is flagged."""
    amt, rng, cr = basis
    n = 0
    by = Counter()
    for p in pays:
        if PR.fy_of(p[1]) != fy:
            continue
        v = p[2] if amt == "net" else p[2] + p[3]
        if v < 100000:
            continue
        k = (p[0], cell_p(v))
        if k in cells:
            n += 1
            by[k] += 1
    return n, by
