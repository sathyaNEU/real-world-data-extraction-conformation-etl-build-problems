"""task198 architecture 3 generating process: the clean truth the pack is cut from.

Stratified two-stage design. Dwellings within primary sampling units (meshblocks), units within
strata, strata within region. Each unit is worked by one interviewer and each interviewer works
units across every stratum of the region, so the interviewer groups cut across the replication
groups the design supplies: the 84 replicate groups are formed on units within strata without
regard to who collected them, so deleting a group never varies a region's interviewer composition.

The recorded damp-or-mould outcome carries an area effect at unit level and a probing differential
at interviewer level, the differential redrawn each quarter. The named region's population rate
rises in the field quarter; its measured rise also carries its four-interviewer panel's draw.
"""
import collections
import math
import numpy as np

QUARTERS = ["2025Q3", "2025Q4", "2026Q1", "2026Q2", "2026Q3", "2026Q4"]
LAYOUT_A = ["2025Q3", "2025Q4"]            # the earlier questionnaire layout
LAYOUT_B = ["2026Q1", "2026Q2", "2026Q3", "2026Q4"]
CUR, CMP = "2026Q4", "2025Q4"
NAMED = "Manawatu-Whanganui"
N_REP = 84                                  # supplied replicate groups, formed on units
PSU_SIZE = 10
SIG_INT = 0.100                             # between-interviewer probing differential, SD
SIG_AREA = 0.050                            # between-unit area effect, SD
SEED = 32191656
QEND = {"2025Q3": "2025-09-30", "2025Q4": "2025-12-31", "2026Q1": "2026-03-31",
        "2026Q2": "2026-06-30", "2026Q3": "2026-09-30", "2026Q4": "2026-12-31"}

# region: (prevalence, rise in points applied in CUR only, strata, units per stratum, interviewers)
REGIONS = collections.OrderedDict([
    (NAMED,            (0.224, 3.0, 4, 35,  4)),
    ("Auckland",       (0.168, 3.3, 6, 40, 24)),
    ("Canterbury",     (0.159, 3.6, 5, 32, 16)),
    ("Wellington",     (0.173, 3.4, 4, 30, 12)),
    ("Waikato",        (0.197, 3.8, 4, 28, 11)),
    ("Bay of Plenty",  (0.216, 3.5, 3, 26,  9)),
    ("Otago",          (0.181, 3.9, 3, 22,  8)),
    ("Northland",      (0.243, 3.4, 3, 20,  7)),
    ("Hawke's Bay",    (0.231, 3.2, 3, 18,  7)),
    ("Taranaki",       (0.189, 3.5, 2, 18,  6)),
    ("Southland",      (0.206, 3.6, 2, 16,  5)),
    ("Gisborne",       (0.262, 3.7, 2, 12,  4)),
])
# the named region's territorial authorities; TA-MW4 transferred in at the 2026 amalgamation, so
# the pre-amalgamation base for the region excludes it.
NAMED_TAS = ["TA-MW1", "TA-MW2", "TA-MW3", "TA-MW4"]
TRANSFERRED_IN = "TA-MW4"
# The named region's field panel was consolidated at the start of the field quarter: six of its ten
# interviewers left and the remaining four carried the whole quarter. Its earlier quarters are
# therefore collected by a dispersed panel and its own history cannot stand in for this quarter's
# spread, which is why the interval has to be computed from this quarter's own workload.
PANEL_NAMED = {q: 4 for q in QUARTERS}


def _roster():
    """(interviewer_id, region, index within region). Ids are allocated in region order."""
    out = []
    nxt = 1000
    for r in REGIONS:
        ni = REGIONS[r][4]
        for j in range(ni):
            out.append((nxt, r, j))
            nxt += 1
    return out


def build(seed=SEED, sig_int=SIG_INT):
    rng = np.random.default_rng(seed)
    roster = _roster()
    reg_ints = collections.OrderedDict()
    for iid, r, j in roster:
        reg_ints.setdefault(r, []).append(iid)

    # units: one owner each, owners cutting across every stratum of the region
    units = []                      # (region, stratum, unit_id, interviewer, ta)
    uid = 50000
    for r in REGIONS:
        p0, rise, ns, npsu, ni = REGIONS[r]
        ids = reg_ints[r]
        t = 0
        for h in range(ns):
            for j in range(npsu):
                owner = ids[(h * npsu + j) % ni]
                ta = (TRANSFERRED_IN if t % 18 == 5 else
                      NAMED_TAS[t % 3]) if r == NAMED else None
                units.append((r, h, uid, owner, ta))
                uid += 1
                t += 1

    # replicate groups: assigned to units within stratum, round robin, ignoring who collected them
    grp = {}
    cnt = collections.Counter()
    for (r, h, u, owner, ta) in units:
        g = cnt[(r, h)] % N_REP
        grp[u] = g
        cnt[(r, h)] += 1

    dwellings = []                  # (quarter, region, stratum, unit, interviewer, ta, mode, damp, order)
    workload = []                   # (quarter, interviewer, region, unit, completed)
    uorder = collections.Counter()
    seq = {}
    for (r, h, u, owner, ta) in units:
        seq[u] = uorder[r]; uorder[r] += 1
    for q in QUARTERS:
        d = {iid: rng.normal(0.0, sig_int) for iid, r, j in roster}
        for (r, h, u, owner0, ta) in units:
            if r == NAMED:
                pool = reg_ints[NAMED][:PANEL_NAMED[q]]
                owner = pool[seq[u] % len(pool)]
            else:
                owner = owner0
            p0, rise, ns, npsu, ni = REGIONS[r]
            p = p0 + (rise / 100.0 if q == CUR else 0.0)
            a = rng.normal(0.0, SIG_AREA)
            pi = min(max(p + a + d[owner], 0.01), 0.95)
            y = rng.binomial(1, pi, PSU_SIZE)
            # mode is independent of the outcome, so the mode-mix rival dies on the data
            m = rng.random(PSU_SIZE)
            for k in range(PSU_SIZE):
                dwellings.append((q, r, h, u, owner, ta,
                                  "TEL" if m[k] < 0.18 else "F2F", int(y[k]),
                                  float(rng.random())))
            workload.append((q, owner, r, u, PSU_SIZE))
    return dict(dwellings=dwellings, units=units, roster=roster, reg_ints=reg_ints,
                grp=grp, workload=workload)


# --------------------------------------------------------------------------------------
# Estimation helpers: the supplied replication and the one re-formed over the field workload.
# --------------------------------------------------------------------------------------

def region_rate(dw, region, quarter, base="new"):
    n = y = 0
    for (q, r, h, u, i, ta, md, v, o) in dw:
        if r != region or q != quarter:
            continue
        if base == "old" and ta == TRANSFERRED_IN:
            continue
        n += 1
        y += v
    return 100.0 * y / n, n


def rep_rates(dw, grp, region, quarter):
    """the region's rate under each supplied replicate: delete a group within each stratum and
    scale the survivors in that stratum, which is what the shipped replicate weights encode."""
    cells = collections.defaultdict(lambda: [0, 0])
    for (q, r, h, u, i, ta, md, v, o) in dw:
        if r != region or q != quarter:
            continue
        cells[(h, u)][0] += 1
        cells[(h, u)][1] += v
    byh = collections.defaultdict(list)
    for (h, u), c in cells.items():
        byh[h].append((u, c))
    out = []
    for g in range(N_REP):
        num = den = 0.0
        for h, lst in byh.items():
            keep = [(u, c) for u, c in lst if grp[u] != g]
            if not keep or len(keep) == len(lst):
                sc = 1.0
                keep = lst
            else:
                sc = float(len(lst)) / len(keep)
            for u, c in keep:
                den += c[0] * sc
                num += c[1] * sc
        out.append(100.0 * num / den)
    return out


def var_supplied(dw, grp, region, quarter):
    th, _ = region_rate(dw, region, quarter)
    rr = rep_rates(dw, grp, region, quarter)
    k = float(N_REP)
    return (k - 1.0) / k * sum((x - th) ** 2 for x in rr)


def sigma_interviewer(dw, exclude_region):
    """between-interviewer SD of the recorded rate, in points, from the whole workforce outside
    the named region. Method of moments; anova and reml agree to 0.15 per cent on this record."""
    agg = collections.defaultdict(lambda: [0, 0])
    tot = collections.defaultdict(lambda: [0, 0])
    for (q, r, h, u, i, ta, md, v, o) in dw:
        if r == exclude_region:
            continue
        agg[(q, r, i)][0] += 1
        agg[(q, r, i)][1] += v
        tot[(q, r)][0] += 1
        tot[(q, r)][1] += v
    res = []
    ms = []
    pv = []
    for (q, r, i), (n, y) in agg.items():
        if n < 20:
            continue
        p = tot[(q, r)][1] / float(tot[(q, r)][0])
        res.append(y / float(n) - p)
        ms.append(float(n))
        pv.append(p)
    res = np.array(res)
    ms = np.array(ms)
    pv = np.array(pv)
    within = float(np.mean(pv * (1 - pv) / ms))
    return 100.0 * math.sqrt(max(float(res.var(ddof=1)) - within, 1e-12)), len(res)


def workload_shares(dw, region, quarter):
    w = collections.defaultdict(float)
    for (q, r, h, u, i, ta, md, v, o) in dw:
        if r == region and q == quarter:
            w[i] += 1.0
    tot = sum(w.values())
    return sorted(x / tot for x in w.values())


def verdict(dw, grp, region=NAMED, cur=CUR, cmp_=CMP):
    """both routes on the filed estimand: the supplied replication and the one re-formed over
    the field workload. Returns the change, both standard errors and both z values."""
    rc, _ = region_rate(dw, region, cur)
    rp, _ = region_rate(dw, region, cmp_)
    delta = rc - rp
    vs = var_supplied(dw, grp, region, cur) + var_supplied(dw, grp, region, cmp_)
    sb, _ = sigma_interviewer(dw, region)
    s2 = sum(x * x for x in workload_shares(dw, region, cur)) + \
         sum(x * x for x in workload_shares(dw, region, cmp_))
    vg = vs + sb * sb * s2
    return dict(delta=delta, se_supplied=math.sqrt(vs), se_correct=math.sqrt(vg),
                z_supplied=delta / math.sqrt(vs), z_correct=delta / math.sqrt(vg),
                sigma_int=sb, shares_sq=s2, f=math.sqrt(vg / vs))
