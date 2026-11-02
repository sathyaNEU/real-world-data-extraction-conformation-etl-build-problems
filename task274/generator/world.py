"""task274 world model: Larkmoor County's pre-plea diversion lottery and the records it leaves.

Everything here is deterministic. The lottery population (the main call's rows) is drawn from its own
random stream, and the seed of that stream is chosen by `pick_main_seed`, which walks seeds upward from
MAIN_SEED_BASE until every licensed route to the golden prints the same whole-per-cent figures and every
easy route clears the Board's thresholds (the construction `determinism-check` section 3 calls C1). The
rest of the world (other cases, charges, the provider's monthly reports) draws from separate streams, so
the main population never moves when they change.
"""
import datetime as dt
import math

import numpy as np

D = dt.date
CUT = D(2026, 8, 31)                 # the evaluation date: the courts' records as they stand on 31 August 2026
CUTOVER = D(2026, 3, 2)              # the courts' new case management system went live (legacy through 1 March)
RECODE = D(2026, 1, 1)               # the state criminal code's renumbering took effect
NETHERCOTE_SWITCH = D(2026, 1, 16)   # Nethercote's new participant system went live
FY_START, FY_END = D(2025, 7, 1), D(2026, 6, 30)   # the county's fiscal 2026
EXTRACT_FROM = D(2025, 4, 1)         # cases filed from 1 April 2025

DIVISIONS = ["LC", "BW", "WM", "SH"]
DIV_NAME = {"LC": "Larkmoor City", "BW": "Bramwick", "WM": "Wendmoor", "SH": "Strandham"}
DIV_SHARE = [0.40, 0.24, 0.21, 0.15]
SITES = ["Larkmoor City", "Bramwick", "Wendmoor", "Strandham"]

# Board resolution 2025-31: renewal tiers on the cut in percentage points
FULL_AT, PILOT_AT = 25, 15

# ---------------------------------------------------------------------------------------------------------
# calendar


def add_months(d, k):
    y = d.year + (d.month - 1 + k) // 12
    m = (d.month - 1 + k) % 12 + 1
    return D(y, m, 1)


def month_end(d):
    return add_months(d, 1) - dt.timedelta(1)


def first_thursday(y, m, skip=()):
    d = D(y, m, 1)
    while d.weekday() != 3 or d in skip:
        d += dt.timedelta(1)
    return d


HOLIDAYS = {D(2026, 1, 1)}
LOTTERY_DATES = [first_thursday(2025 + (5 + i) // 12, (5 + i) % 12 + 1, HOLIDAYS) for i in range(12)]


def months_elapsed(term_start):
    """Whole programme months a term starting on term_start has run by the evaluation date."""
    if term_start > CUT:
        return 0
    return (CUT.year - term_start.year) * 12 + CUT.month - term_start.month + 1


# ---------------------------------------------------------------------------------------------------------
# the state criminal code, 2025 numbering and the 2026 renumbering, with the programme's eligible classes

# (offence, eligible class or None, 2025 code, 2026 code, share of filings, misdemeanour or felony)
OFFENCES = [
    ("Retail theft", "A", "418.05", "423.01", 0.120, "CM"),
    ("Theft, property under 1,000", "A", "418.02", "423.02", 0.050, "CM"),
    ("Theft of services", "A", "424.01", "423.04", 0.016, "CM"),
    ("Issuing a bad check", "A", "418.07", "423.11", 0.010, "CM"),
    ("Criminal mischief, under 1,000", "B", "416.02", "424.01", 0.050, "CM"),
    ("Graffiti", "B", "416.04", "424.03", 0.012, "CM"),
    ("Possession of a controlled substance", "C", "434.08", "434.01", 0.060, "CR"),
    ("Possession of drug paraphernalia", "C", "434.15", "434.05", 0.040, "CM"),
    ("Possession of marijuana over the civil limit", "C", "434.05", "434.02", 0.015, "CM"),
    ("Disorderly conduct", "D", "429.04", "418.02", 0.050, "CM"),
    ("Criminal trespass", "D", "415.02", "428.02", 0.040, "CM"),
    ("Obstructing a public way", "D", "429.06", "428.05", 0.010, "CM"),
    ("False reporting to a law enforcement agency", "D", "429.07", "418.05", 0.008, "CM"),
    ("Driving on a suspended license", "E", "834.73", "834.01", 0.070, "CM"),
    ("Driving without a license", "E", "831.51", "834.02", 0.020, "CM"),
    ("Driving under the influence", None, "813.81", "813.01", 0.090, "CM"),
    ("Aggravated driving under the influence", None, "834.01", "834.73", 0.015, "CR"),
    ("Assault", None, "423.01", "412.01", 0.050, "CM"),
    ("Assault, domestic violence", None, "436.01", "412.05", 0.060, "CM"),
    ("Violation of a protection order", None, "428.10", "412.20", 0.020, "CM"),
    ("Harassment", None, "429.21", "429.04", 0.020, "CM"),
    ("Resisting arrest", None, "425.08", "426.01", 0.015, "CM"),
    ("Aggravated assault", None, "412.04", "412.10", 0.020, "CR"),
    ("Burglary, third degree", None, "415.06", "415.02", 0.020, "CR"),
    ("Possession of a dangerous drug for sale", None, "434.01", "434.08", 0.020, "CR"),
    ("Theft, property 1,000 or more", None, "418.14", "423.05", 0.020, "CR"),
    ("Misconduct involving weapons", None, "431.02", "431.01", 0.015, "CR"),
    ("Criminal damage, 1,000 or more", None, "416.03", "416.04", 0.010, "CR"),
    ("Fraudulent schemes", None, "423.10", "423.20", 0.010, "CR"),
]
CLASS_NAME = {
    "A": "Theft and fraud",
    "B": "Criminal damage",
    "C": "Drug possession",
    "D": "Public order",
    "E": "License and driving",
}
OLD2NEW = {o[2]: o[3] for o in OFFENCES}
NEW_CLASS = {o[3]: o[1] for o in OFFENCES}
NEW_NAME = {o[3]: o[0] for o in OFFENCES}
OLD_NAME = {o[2]: o[0] for o in OFFENCES}
ELIGIBLE_OFFENCES = [o for o in OFFENCES if o[1]]


def code_tables_ok():
    olds = [o[2] for o in OFFENCES]
    news = [o[3] for o in OFFENCES]
    assert len(set(olds)) == len(olds) and len(set(news)) == len(news)
    shared = sorted(set(olds) & set(news))
    return shared


# ---------------------------------------------------------------------------------------------------------
# the lottery population (the main call)

MAIN = dict(
    n_mean=300,           # eligible defendants on each month's list
    p_decline=0.12,       # offered defendants who decline and are prosecuted in the ordinary way
    conv_not_offered=0.56,
    conv_declined=0.50,
    conv_terminated=0.91,  # a terminated case is tried on the stipulated record the agreement carries
    disp_median=95, disp_sigma=0.45,       # days from the draw to disposition, ordinary prosecution
    post_median=90, post_sigma=0.45,       # days from termination to disposition
    hazard=[0.060, 0.050, 0.040, 0.030, 0.010, 0.008, 0.008, 0.008, 0.008, 0.008, 0.008, 0.200],
)
MAIN_SEED_BASE = 274000


def draw_main(seed, p=MAIN):
    """One draw of the lottery population: each defendant's arm, path and dated outcome."""
    rng = np.random.default_rng(seed)
    rows = []
    for m, ld in enumerate(LOTTERY_DATES):
        n = int(rng.poisson(p["n_mean"]))
        order = rng.permutation(n)
        offered = np.zeros(n, bool)
        offered[order[: n // 2]] = True
        for i in range(n):
            r = dict(lot=m, draw=ld, offered=bool(offered[i]), idx=i)
            if not offered[i] or rng.uniform() < p["p_decline"]:
                r["path"] = "not_offered" if not offered[i] else "declined"
                if offered[i]:
                    r["declined_on"] = ld + dt.timedelta(int(rng.integers(5, 21)))
                r["disp"] = ld + dt.timedelta(int(round(rng.lognormal(math.log(p["disp_median"]), p["disp_sigma"]))))
                rate = p["conv_not_offered"] if not offered[i] else p["conv_declined"]
                r["convicted"] = bool(rng.uniform() < rate)
            else:
                agree = ld + dt.timedelta(int(rng.integers(14, 36)))
                ts = add_months(agree, 1)
                r.update(agree=agree, term_start=ts, term_end=month_end(add_months(ts, 11)))
                k = None
                for j in range(12):
                    if rng.uniform() < p["hazard"][j]:
                        k = j + 1
                        break
                if k is None:
                    r.update(path="completed", k=None, term_date=None, convicted=False)
                    r["disp"] = r["term_end"] + dt.timedelta(int(rng.integers(7, 22)))
                else:
                    ms = add_months(ts, k - 1)
                    me = month_end(ms)
                    if k < 12:
                        td = ms + dt.timedelta(int(rng.integers(0, (me - ms).days + 1)))
                    else:
                        td = me - dt.timedelta(int(rng.integers(0, 7)))
                    r.update(path="terminated", k=k, term_date=td)
                    r["disp"] = td + dt.timedelta(int(round(rng.lognormal(math.log(p["post_median"]), p["post_sigma"]))))
                    r["convicted"] = bool(rng.uniform() < p["conv_terminated"])
            rows.append(r)
    return rows


# ---------------------------------------------------------------------------------------------------------
# the routes: the golden family (every licensed construction of the filed estimand) and the easy routes


def aj_cif(times, causes, horizon):
    """Aalen-Johansen cumulative incidence of cause 1 (cause 2 competing, 0 censored) at the horizon."""
    o = np.argsort(times, kind="stable")
    t = np.asarray(times)[o]
    c = np.asarray(causes)[o]
    n = len(t)
    S, F, i = 1.0, 0.0, 0
    while i < n and t[i] <= horizon:
        j = i
        while j < n and t[j] == t[i]:
            j += 1
        at = n - i
        d1 = int((c[i:j] == 1).sum())
        d2 = int((c[i:j] == 2).sum())
        F += S * d1 / at
        S *= 1 - (d1 + d2) / at
        i = j
    return F


def life_table(parts):
    """Termination chance over the twelve-month term by programme month, every participant's months."""
    S, rows = 1.0, []
    for j in range(1, 13):
        risk = d = 0
        for r in parts:
            if months_elapsed(r["term_start"]) >= j and (r["path"] == "completed" or r["k"] >= j):
                risk += 1
                if r["path"] == "terminated" and r["k"] == j:
                    d += 1
        h = d / risk if risk else 0.0
        rows.append((j, risk, d, h))
        S *= 1 - h
    return 1 - S, rows


def routes(rows):
    """Every route's figures on one lottery population, observed only as the records at the cut show it."""
    o = {}
    disposed = [r["disp"] <= CUT for r in rows]
    conv_rec = [r["convicted"] and d for r, d in zip(rows, disposed)]
    arm = np.array([1 if r["offered"] else 0 for r in rows])
    dis = np.array(disposed)
    crec = np.array(conv_rec)
    conv = np.array([r["convicted"] for r in rows])
    lot = np.array([r["lot"] for r in rows])
    path = np.array([r["path"] for r in rows])
    fu = np.array([(CUT - r["draw"]).days for r in rows])
    tdays = np.array([(r["disp"] - r["draw"]).days for r in rows])

    def pct(x):
        return 100.0 * x

    o["truth"] = pct(conv[arm == 0].mean() - conv[arm == 1].mean())
    o["naive"] = pct(crec[arm == 0].mean() - crec[arm == 1].mean())
    o["recorded_not_offered"] = pct(crec[arm == 0].mean())
    o["recorded_offered"] = pct(crec[arm == 1].mean())
    o["complete_case"] = pct(conv[dis & (arm == 0)].mean() - conv[dis & (arm == 1)].mean())
    early = lot <= 2
    o["matured_lotteries_at_cut"] = pct(crec[early & (arm == 0)].mean() - crec[early & (arm == 1)].mean())
    for H in (365, 425, int(fu.max())):
        c = []
        for a in (0, 1):
            idx = np.where(arm == a)[0]
            T = np.where(dis[idx], tdays[idx], fu[idx])
            C = np.where(dis[idx], np.where(conv[idx], 1, 2), 0)
            c.append(aj_cif(T, C, H))
        o["cif_%d" % H] = pct(c[0] - c[1])
    o["cif_max"] = o["cif_%d" % int(fu.max())]
    off = arm == 1
    p_dec = (path[off] == "declined").mean()
    c_dec = conv[dis & (path == "declined")].mean()
    c_no = conv[dis & (arm == 0)].mean()

    def aj_ratio(mask):
        idx = np.where(mask)[0]
        T = np.where(dis[idx], tdays[idx], fu[idx])
        a = aj_cif(T, np.where(dis[idx], np.where(conv[idx], 1, 2), 0), 10 ** 6)
        b = aj_cif(T, np.where(dis[idx], np.where(conv[idx], 2, 1), 0), 10 ** 6)
        return a / (a + b)

    c_no_aj = aj_ratio(arm == 0)
    c_dec_aj = aj_ratio(path == "declined")
    full_lots = [L for L in range(12) if all(r["disp"] <= CUT for r in rows if r["lot"] == L and not r["offered"])]
    c_no_mat = conv[(arm == 0) & np.isin(lot, full_lots)].mean() if full_lots else float("nan")
    parts = [r for r in rows if r["path"] in ("terminated", "completed")]
    p_term, lt = life_table(parts)
    mat = [r for r in parts if months_elapsed(r["term_start"]) >= 12]
    p_term_mat = np.mean([r["path"] == "terminated" for r in mat])
    termd = [r for r in parts if r["path"] == "terminated" and r["term_date"] <= CUT and r["disp"] <= CUT]
    c_term = np.mean([r["convicted"] for r in termd])
    T, C1, C2 = [], [], []
    for r in parts:
        if r["path"] == "terminated" and r["term_date"] <= CUT:
            if r["disp"] <= CUT:
                T.append((r["disp"] - r["term_date"]).days)
                C1.append(1 if r["convicted"] else 2)
                C2.append(2 if r["convicted"] else 1)
            else:
                T.append((CUT - r["term_date"]).days)
                C1.append(0)
                C2.append(0)
    a, b = aj_cif(T, C1, 10 ** 6), aj_cif(T, C2, 10 ** 6)
    c_term_aj = a / (a + b)

    def offered_share(pd_, cd_, pt_, ct_):
        return pd_ * cd_ + (1 - pd_) * pt_ * ct_

    def eff(cn, pd_, cd_, pt_, ct_):
        return pct(cn - offered_share(pd_, cd_, pt_, ct_))

    o["golden"] = eff(c_no, p_dec, c_dec, p_term, c_term)
    o["fam_matured_term"] = eff(c_no, p_dec, c_dec, p_term_mat, c_term)
    o["fam_aalen_johansen"] = eff(c_no_aj, p_dec, c_dec_aj, p_term, c_term_aj)
    o["fam_matured_not_offered"] = eff(c_no_mat, p_dec, c_dec, p_term, c_term)
    o["fam_all_matured"] = eff(c_no_mat, p_dec, c_dec, p_term_mat, c_term)
    # each lottery's own contrast, weighted by the lottery's size
    num = den = 0.0
    for L in range(12):
        m_ = lot == L
        cn_L = conv[m_ & (arm == 0) & dis].mean()
        pd_L = (path[m_ & off] == "declined").mean()
        num += m_.sum() * (cn_L - offered_share(pd_L, c_dec, p_term, c_term))
        den += m_.sum()
    o["fam_by_lottery"] = pct(num / den)
    # the case-by-case completion (identical to the arm-level construction by the product-limit identity)
    S12 = 1 - p_term
    surv = {0: 1.0}
    s = 1.0
    for (j, risk, d, h) in lt:
        s *= 1 - h
        surv[j] = s
    acc = 0.0
    for r in rows:
        if not r["offered"]:
            continue
        if r["path"] == "declined":
            acc += (1.0 if r["convicted"] else 0.0) if r["disp"] <= CUT else c_dec
        elif r["path"] == "terminated" and r["term_date"] <= CUT:
            acc += (1.0 if r["convicted"] else 0.0) if r["disp"] <= CUT else c_term
        elif r["path"] == "completed" and r["disp"] <= CUT:
            acc += 0.0
        else:
            k_done = months_elapsed(r["term_start"])
            acc += (1 - S12 / surv[min(k_done, 12)]) * c_term if k_done < 12 else 0.0
    n_off = int(off.sum())
    # not-offered and declined cases still open complete at their arm's disposed rate
    acc_no = sum((1.0 if r["convicted"] else 0.0) if r["disp"] <= CUT else c_no for r in rows if not r["offered"])
    o["fam_case_by_case"] = pct(acc_no / int((arm == 0).sum()) - acc / n_off)
    # easy completions
    t_sofar = np.mean([r["path"] == "terminated" and r["term_date"] <= CUT for r in parts])
    o["terminated_so_far"] = eff(c_no, p_dec, c_dec, t_sofar, c_term)
    o["terminated_like_not_offered"] = eff(c_no, p_dec, c_dec, p_term, c_no)
    pm = sum(x[1] for x in lt)
    dd = sum(x[2] for x in lt)
    o["constant_monthly_rate"] = eff(c_no, p_dec, c_dec, 1 - (1 - dd / pm) ** 12, c_term)
    S11 = float(np.prod([1 - x[3] for x in lt[:11]]))
    o["term_without_final_review"] = eff(c_no, p_dec, c_dec, 1 - S11, c_term)
    term_seen = [r for r in parts if r["path"] == "terminated" and r["term_date"] <= CUT]
    o["terminated_convicted_so_far"] = eff(c_no, p_dec, c_dec, p_term, np.mean([r["convicted"] and r["disp"] <= CUT for r in term_seen]))
    exits = [r for r in parts if (r["path"] == "terminated" and r["term_date"] <= CUT) or (r["path"] == "completed" and r["disp"] <= CUT)]
    o["exits_so_far"] = eff(c_no, p_dec, c_dec, np.mean([r["path"] == "terminated" for r in exits]), c_term)
    o["participants_only"] = pct(c_no - p_term * c_term)
    # components
    o.update(
        p_term=pct(p_term), p_term_matured=pct(p_term_mat), c_term=pct(c_term), c_term_aj=pct(c_term_aj),
        not_offered=pct(c_no), not_offered_aj=pct(c_no_aj), not_offered_matured=pct(c_no_mat),
        offered=pct(offered_share(p_dec, c_dec, p_term, c_term)),
        offered_matured=pct(offered_share(p_dec, c_dec, p_term_mat, c_term)),
        offered_aj=pct(offered_share(p_dec, c_dec_aj, p_term, c_term_aj)),
        p_decline=pct(p_dec), c_declined=pct(c_dec), final_review_rate=pct(lt[11][3]),
        months_1_to_3=pct(1 - float(np.prod([1 - x[3] for x in lt[:3]]))),
        n=len(rows), n_offered=n_off, n_not_offered=int((arm == 0).sum()), n_participants=len(parts),
        n_matured=len(mat), n_terminated_disposed=len(termd), full_lotteries=len(full_lots),
        open_offered=int((off & ~dis).sum()), open_not_offered=int(((arm == 0) & ~dis).sum()),
    )
    o["life_table"] = lt
    return o


FAMILY = ("golden", "fam_matured_term", "fam_aalen_johansen", "fam_matured_not_offered", "fam_all_matured",
          "fam_by_lottery", "fam_case_by_case")
SHARE_FAMILIES = (
    ("not_offered", "not_offered_aj", "not_offered_matured"),
    ("offered", "offered_matured", "offered_aj"),
    ("p_term", "p_term_matured"),
    ("c_term", "c_term_aj"),
)
FULL_ROUTES = ("naive", "cif_365", "cif_425", "cif_max", "terminated_so_far", "terminated_like_not_offered",
               "term_without_final_review", "terminated_convicted_so_far", "matured_lotteries_at_cut")
LAPSE_ROUTES = ("complete_case", "exits_so_far")
CLEAR = 0.15     # least distance of a graded figure from its whole-per-cent edge


def edge(v):
    return 0.5 - abs(v - round(v))


def main_seed_ok(o):
    fam = [o[k] for k in FAMILY]
    if len({round(x) for x in fam}) != 1 or min(edge(x) for x in fam) < CLEAR:
        return False
    if not (18 <= round(o["golden"]) <= 22):
        return False
    for grp in SHARE_FAMILIES:
        vals = [o[k] for k in grp]
        if len({round(x) for x in vals}) != 1 or min(edge(x) for x in vals) < CLEAR:
            return False
    if min(o[k] for k in FULL_ROUTES) < FULL_AT + 2.0:
        return False
    if max(o[k] for k in LAPSE_ROUTES) > PILOT_AT - 4.0:
        return False
    if FULL_AT - 0.75 <= o["constant_monthly_rate"] <= FULL_AT + 0.75:
        return False
    return True


def pick_main_seed(limit=4000):
    for s in range(MAIN_SEED_BASE, MAIN_SEED_BASE + limit):
        rows = draw_main(s)
        o = routes(rows)
        if main_seed_ok(o):
            return s, rows, o
    raise RuntimeError("no main seed in range")


if __name__ == "__main__":
    print("shared code strings:", code_tables_ok())
    print("lotteries:", LOTTERY_DATES)
    s, rows, o = pick_main_seed()
    print("seed", s)
    for k, v in o.items():
        if k != "life_table":
            print("  %-30s %s" % (k, round(v, 3) if isinstance(v, float) else v))
    for row in o["life_table"]:
        print("  month", row)
