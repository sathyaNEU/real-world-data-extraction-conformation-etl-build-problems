"""Simulate the people in the registry extract and everything the registries record about them, 2018 to
30 June 2026: who they are, the conditions their hospital contacts record, when they start each medicine,
every dispensing and return, every hospital contact with its diagnoses, deaths and migrations.

The only causal effect in the world is corinurad's: acute kidney injury runs at 2.5 times the person's own
rate in days 1 to 30 after a new user's first dispensing. Everything else that separates the medicines is who
starts them: latent multipliers on each person's event rates (never recorded anywhere), the conditions a
person carries (recorded on their contacts, some only late or never), and two ways an event moves a start
(a fall admission raises the chance of starting a sleep medicine in the following month; an acute kidney
injury lowers the chance of starting corinurad for six weeks)."""
import numpy as np

import world as W

YEAR = 365.25
BIG = 10 ** 7
COHORT_IDS = {c: i for i, c in enumerate(list(W.COHORTS) + ["comparator"])}
COHORT_OF = {i: c for c, i in COHORT_IDS.items()}
EVENTS = ("fall", "aki", "pancreatitis")


# ------------------------------------------------------------------ helpers

def year_start(y):
    return W.day(W.dt.date(y, 1, 1))


def sample_uptake(r, cohort, n, lo=None):
    """Days from the cohort's uptake curve between its launch (or 1 January 2022) and the end of the data."""
    c = W.COHORTS[cohort]
    launch = W.SUBSTANCES[cohort]["launch"]
    first = W.day(launch) if launch else year_start(2022)
    years, weights, lows, highs = [], [], [], []
    for y, w in sorted(c["uptake"].items()):
        a = max(first, year_start(y))
        b = min(W.D_END, year_start(y + 1) - 1)
        if b < a:
            continue
        years.append(y)
        lows.append(a)
        highs.append(b)
        weights.append(w * (b - a + 1))
    weights = np.array(weights) / np.sum(weights)
    k = r.choice(len(years), size=n, p=weights)
    lo_ = np.array(lows)[k]
    hi_ = np.array(highs)[k]
    return lo_ + np.floor(r.random(n) * (hi_ - lo_ + 1)).astype(np.int64)


def truncnorm(r, mean, sd, lo, hi, n):
    out = r.normal(mean, sd, n)
    bad = (out < lo) | (out > hi)
    while bad.any():
        out[bad] = r.normal(mean, sd, bad.sum())
        bad = (out < lo) | (out > hi)
    return out


def age_at(P, d):
    return (np.asarray(d, float) - P["birth_day"]) / YEAR


# ------------------------------------------------------------------ people

def new_people(cohort, n, birth_year, female, r, kind):
    return dict(cohort=np.full(n, COHORT_IDS[cohort if kind == "user" else "comparator"], np.int8),
                kind=np.full(n, 0 if kind == "user" else 1, np.int8),
                birth_year=birth_year.astype(np.int16), female=female.astype(bool),
                birth_day=(np.array([W.day(W.dt.date(int(y), 1, 1)) for y in birth_year]) +
                           np.floor(r.random(n) * 365)).astype(np.int64))


def conditions(P, cohort_names, r):
    """Present conditions (bool) and the day each is first recorded in the patient registry (NaN never)."""
    n = len(P["cohort"])
    age22 = age_at(P, W.day(W.dt.date(2022, 6, 30)))
    present = np.zeros((n, len(W.COND_NAMES)), bool)
    rec = np.full((n, len(W.COND_NAMES)), np.nan)
    for j, c in enumerate(W.COND_NAMES):
        p0, slope, ffac, _, _ = W.CONDITIONS[c]
        p = p0 * np.exp(slope * (age22 - 70.0)) * np.where(P["female"], ffac, 1.0)
        mult = np.array([W.COHORT_COND.get(cn, {}).get(c, 1.0) for cn in cohort_names])
        p = np.minimum(0.9, p * mult)
        present[:, j] = r.random(n) < p
        # first record: spread from 2011 to beyond the data, so part of what is present is not yet on file
        rec[:, j] = np.where(present[:, j], r.uniform(W.day(W.dt.date(2011, 1, 1)), W.D_END + 900, n), np.nan)
    return present, rec


def latent(cohort_names, r):
    out = {}
    for e in EVENTS:
        m = np.array([W.LATENT[cn][e] for cn in cohort_names])
        k = W.LATENT_SHAPE[e]
        out[e] = r.gamma(k, m / k)
    return out


def event_multiplier(present, e):
    m = np.ones(present.shape[0])
    for c, f in W.EVENT_MULT[e].items():
        m *= np.where(present[:, W.COND_NAMES.index(c)], f, 1.0)
    return m


# ------------------------------------------------------------------ event processes

def poisson_process(P, idx, e, lo, hi, r):
    """Events of type e for persons idx over [lo, hi) (days), at each person's base rate for their age and
    sex times their condition and latent multipliers, in yearly pieces. Returns (person, day)."""
    out_p, out_d = [], []
    mult = P["mult_" + e][idx]
    for y in range(2018, 2027):
        a = np.maximum(lo, year_start(y))
        b = np.minimum(hi, year_start(y + 1))
        ok = b > a
        if not ok.any():
            continue
        ii, aa, bb = idx[ok], a[ok], b[ok]
        mid = (aa + bb) / 2.0
        rate = W.base_rate(e, age_at({"birth_day": P["birth_day"][ii]}, mid), P["female"][ii]) * mult[ok]
        mu = rate * (bb - aa) / YEAR
        k = r.poisson(mu)
        if k.sum() == 0:
            continue
        rep = np.repeat(np.arange(len(ii)), k)
        d = aa[rep] + np.floor(r.random(len(rep)) * (bb[rep] - aa[rep])).astype(np.int64)
        out_p.append(ii[rep])
        out_d.append(d)
    if not out_p:
        return np.zeros(0, np.int64), np.zeros(0, np.int64)
    return np.concatenate(out_p), np.concatenate(out_d)


def expected_count(P, idx, e, lo, hi):
    tot = 0.0
    mult = P["mult_" + e][idx]
    for y in range(2018, 2027):
        a = np.maximum(lo, year_start(y))
        b = np.minimum(hi, year_start(y + 1))
        ok = b > a
        if not ok.any():
            continue
        mid = (a[ok] + b[ok]) / 2.0
        rate = W.base_rate(e, age_at({"birth_day": P["birth_day"][idx[ok]]}, mid), P["female"][idx[ok]]) * mult[ok]
        tot += (rate * (b[ok] - a[ok]) / YEAR).sum()
    return tot


def segment(P, idx, e, lo, hi, name, select):
    """Events over one window per person, from its own stream; for a selected window the variant whose count
    sits closest to the expected count is kept (variance control)."""
    lo = np.maximum(np.asarray(lo, np.int64), P["entry"][idx].astype(np.int64))
    hi = np.minimum(np.asarray(hi, np.int64), W.D_END + 1)
    if not select:
        return poisson_process(P, idx, e, lo, hi, W.rng(*name))
    ex = expected_count(P, idx, e, lo, hi)
    best = None
    for v in range(VARIANTS):
        out = poisson_process(P, idx, e, lo, hi, W.rng(*(name + (v,))))
        score = abs(len(out[0]) - ex)
        if best is None or score < best[0]:
            best = (score, out)
    return best[1]


def joint_segments(P, idx, e, segs, name):
    """Events over several windows per person, all from one variant of a stream; the variant whose weighted
    chi-square distance from the expected counts, over the scored windows together, is smallest is kept."""
    prepared = []
    for lo, hi, wt in segs:
        lo = np.maximum(np.asarray(lo, np.int64), P["entry"][idx].astype(np.int64))
        hi = np.minimum(np.asarray(hi, np.int64), W.D_END + 1)
        prepared.append((lo, hi, wt, expected_count(P, idx, e, lo, hi) if wt > 0 else 0.0))
    fixed = {k: poisson_process(P, idx, e, lo, hi, W.rng(*(name + (k, 0))))
             for k, (lo, hi, wt, ex) in enumerate(prepared) if wt == 0}
    best = None
    for v in range(JOINT_VARIANTS):
        outs, score = [], 0.0
        for k, (lo, hi, wt, ex) in enumerate(prepared):
            if wt == 0:
                outs.append(fixed[k])
                continue
            out = poisson_process(P, idx, e, lo, hi, W.rng(*(name + (k, v))))
            outs.append(out)
            score += wt * (len(out[0]) - ex) ** 2 / max(ex, 1e-9)
        if best is None or score < best[0]:
            best = (score, outs)
    return best[1]


def start_year(d):
    return (np.datetime64("2018-01-01") + np.asarray(d).astype("timedelta64[D]")).astype("datetime64[Y]").astype(int)


def last_before(ev_p, ev_d, p, t):
    """For each (p, t): the latest event day of person p strictly before t, or -10**9."""
    key = ev_p.astype(np.int64) * 10 ** 6 + ev_d
    order = np.argsort(key, kind="stable")
    key = key[order]
    q = np.asarray(p, np.int64) * 10 ** 6 + np.asarray(t, np.int64)
    pos = np.searchsorted(key, q, side="left") - 1
    out = np.full(len(q), -10 ** 9, np.int64)
    ok = pos >= 0
    hit = ok.copy()
    hit[ok] = (key[pos[ok]] // 10 ** 6) == np.asarray(p, np.int64)[ok]
    out[hit] = key[pos[hit]] % 10 ** 6
    return out


def choose_starts(r, cohort, idx, base_ev, entry):
    """Start days for the cohort's users: the uptake curve, made event dependent by rejection."""
    n = len(idx)
    s = np.full(n, -1, np.int64)
    todo = np.arange(n)
    rounds = 0
    while len(todo):
        rounds += 1
        prop = sample_uptake(r, cohort, len(todo))
        prop = np.maximum(prop, entry[todo] + 1)
        acc = np.ones(len(todo), bool)
        if cohort in ("tasorexant", "zopiclone"):
            ep, ed = base_ev["fall"]
            lb = last_before(ep, ed, idx[todo], prop - 2)
            inwin = (prop - lb >= 3) & (prop - lb <= 33)
            acc = r.random(len(todo)) < np.where(inwin, 1.0, 1.0 / W.FALL_START_FACTOR)
        elif cohort == "corinurad":
            ep, ed = base_ev["aki"]
            lb = last_before(ep, ed, idx[todo], prop)
            inwin = (prop - lb >= 0) & (prop - lb <= W.AKI_START_DAYS)
            acc = r.random(len(todo)) < np.where(inwin, W.AKI_START_FACTOR, 1.0)
        s[todo[acc]] = prop[acc]
        todo = todo[~acc]
        if rounds > 200:
            raise RuntimeError("start sampling did not converge")
    return s


def exits_after(P, idx, t0, cohort_names, r):
    """Death and emigration (and a return for some emigrants), all after day t0."""
    n = len(idx)
    age0 = age_at({"birth_day": P["birth_day"][idx]}, t0)
    mf = np.array([W.MORTALITY_FACTOR[c] for c in cohort_names])
    # Gompertz death time by inversion: h(a) = exp(c0 + g a) * mf
    c0, g = -10.3, 0.092
    u = r.random(n)
    h0 = np.exp(c0 + g * age0) * mf
    tdeath = np.log1p(-g * np.log(u) / h0) / g * YEAR
    death = t0 + np.floor(tdeath).astype(np.int64) + 1
    emig_rate = np.where(age0 < 45, 0.007, np.where(age0 < 65, 0.0035, 0.0018))
    temig = r.exponential(1.0 / emig_rate) * YEAR
    emig = t0 + np.floor(temig).astype(np.int64) + 1
    big = 10 ** 7
    death = np.where(death > W.D_END, big, death)
    emig = np.where((emig > W.D_END) | (emig >= death), big, emig)
    ret = np.where((emig < big) & (r.random(n) < 0.3), emig + r.integers(150, 900, n), big)
    ret = np.where((ret > W.D_END) | (ret >= death), big, ret)
    return death, emig, ret

SIGNAL = {"tasorexant": "fall", "zopiclone": "fall", "corinurad": "aki", "allopurinol": "aki",
          "velaglutide": "pancreatitis", "orlistat": "pancreatitis"}
VARIANTS = 16
JOINT_VARIANTS = 80
# a cohort-year whose stream after the start carries a salt (chosen so the graded figures sit clear of their rounding
# edges; the stream is as random as any other)
STREAM_SALT = {("corinurad", 2022): (1,)}
# windows after a user's start (days, inclusive; None runs to the end of the data) and their weight in the joint
# variance control (0: drawn but not scored)
POST_SEGMENTS = [(0, 0, 0.0), (1, 30, 4.0), (31, 60, 1.0), (61, 180, 2.0), (181, 365, 1.0), (366, None, 0.0)]
# windows around a comparator's index day (None from entry or to the end of the data)
COMPARATOR_SEGMENTS = [(None, -366, 0.0), (-365, -1, 1.0), (0, 0, 0.0), (1, 30, 4.0), (31, 365, 1.0),
                       (366, None, 0.0)]


def window_counts(ev_p, ev_d, pid, lo, hi):
    key = np.sort(ev_p.astype(np.int64) * 10 ** 6 + ev_d)
    a = np.searchsorted(key, pid * 10 ** 6 + lo, side="left")
    b = np.searchsorted(key, pid * 10 ** 6 + hi, side="right")
    return b - a


def discrepancy(P, idx, e, ev, anchor, windows):
    """Chi-square distance between realised and expected event counts in windows around each person's anchor day."""
    score = 0.0
    idx = np.asarray(idx, np.int64)
    anchor = np.asarray(anchor, np.int64)
    for a, b, wt in windows:
        lo = np.maximum(anchor + a, P["entry"][idx])
        hi = np.minimum(anchor + b, W.D_END)
        t = np.maximum(0, hi - lo + 1)
        ok = t > 0
        o = window_counts(ev[0], ev[1], idx[ok], lo[ok], hi[ok]).sum()
        mid = (lo[ok] + hi[ok]) / 2.0
        rate = W.base_rate(e, age_at({"birth_day": P["birth_day"][idx[ok]]}, mid), P["female"][idx[ok]]) * \
            P["mult_" + e][idx[ok]]
        ex = (rate * t[ok] / YEAR).sum()
        score += wt * (o - ex) ** 2 / max(ex, 1e-9)
    return score


# ------------------------------------------------------------------ dispensings

def episode(r, substance, start, n_fills, deathcut):
    """Dispensing days, package numbers and package counts for one episode."""
    packs = [v for v, p in W.PACK.items() if p["substance"] == substance]
    days, vnrs, apks = [], [], []
    t = start
    for k in range(n_fills):
        if t > deathcut or t > W.D_END:
            break
        if substance == "velaglutide":
            steps = ["503318", "503329", "503330", "503341", "503352"]
            v = steps[min(k, 4)]
            apk = 1
        elif substance == "tasorexant":
            v = "412087" if (k == 0 and r.random() < 0.55) else "412098"
            apk = 1
        elif substance == "corinurad":
            v = "186311" if k == 0 and r.random() < 0.6 else ("186333" if r.random() < 0.3 else "186322")
            apk = 1 if v != "186322" or r.random() < 0.8 else 2
        elif substance == "zopiclone":
            v = "027516" if k == 0 and r.random() < 0.6 else ("027538" if r.random() < 0.2 else "027527")
            apk = 1
        elif substance == "allopurinol":
            v = "054712" if k == 0 and r.random() < 0.7 else "054723"
            apk = 1 if r.random() < 0.85 else 2
        else:
            v = "093245"
            apk = 1 if r.random() < 0.8 else 2
        days.append(int(t))
        vnrs.append(v)
        apks.append(apk)
        dur = W.PACK[v]["days"] * apk
        t = t + int(max(5, round(dur * r.uniform(0.85, 1.45))))
    return days, vnrs, apks


def clear_of_boundaries(t, entry=None, last=None):
    """Move a new episode's first dispensing clear of the one-year boundaries the analysis draws: a year after an
    immigration (residence) and a year after the previous dispensing (the washout)."""
    for _ in range(4):
        moved = False
        if entry is not None and abs(t - 365 - entry) <= 18:
            t += 40
            moved = True
        if last is not None and 325 <= t - last <= 405:
            t += 100
            moved = True
        if not moved:
            break
    return t


MEAN_FILLS = {"tasorexant": 3.6, "zopiclone": 2.6, "corinurad": 6.5, "allopurinol": 8.0, "velaglutide": 5.5,
              "orlistat": 2.6}


def fills(r, substance):
    return int(r.geometric(1.0 / MEAN_FILLS[substance]))


def simulate():
    rp = W.rng("people")
    people = []
    # ---------------- the users of the six medicines
    for cohort, c in W.COHORTS.items():
        n = c["n"]
        r = W.rng("users", cohort)
        mean, sd, lo, hi = c["age"]
        age = truncnorm(r, mean, sd, lo, hi, n)
        female = r.random(n) < c["female"]
        s0 = sample_uptake(r, cohort, n)
        by = np.floor(W.EPOCH.year + s0 / YEAR - age).astype(np.int64)
        P = new_people(cohort, n, by, female, r, "user")
        P["s0"] = s0
        P["user_of"] = np.full(n, list(W.COHORTS).index(cohort), np.int8)
        people.append(P)
    U = {k: np.concatenate([p[k] for p in people]) for k in people[0]}
    nU = len(U["cohort"])
    cohort_names = [COHORT_OF[i] for i in U["cohort"]]
    U["present"], U["rec"] = conditions(U, cohort_names, W.rng("conditions", "users"))
    lat = latent(cohort_names, W.rng("latent", "users"))
    for e in EVENTS:
        U["mult_" + e] = event_multiplier(U["present"], e) * lat[e]
        U["latent_" + e] = lat[e]
    # entry: most were resident before 2018; a few immigrated in the years before their start
    r = W.rng("immigration", "users")
    imm = r.random(nU) < 0.018
    gap = r.integers(40, 1300, nU)
    gap = np.where((gap >= 330) & (gap <= 400), gap + 90, gap)
    arrival = U["s0"] - gap
    # an arrival before the extract opens is resident throughout; its date stays on the civil record
    U["old_imm"] = np.where(imm & (arrival < 1), arrival, BIG)
    imm = imm & (arrival >= 1)
    U["entry"] = np.where(imm, arrival, 0)
    U["immigrated"] = imm
    # returned-only users (dispensed once, returned, never started): a small share of the new medicines
    r = W.rng("returned_only")
    U["returned_only"] = np.isin(U["user_of"], [0, 2, 4]) & (r.random(nU) < 0.006) & ~imm
    # each cohort's signal event: the whole timeline from a few variants of one stream decides the start (the
    # variant whose year before the start sits closest to expectation is kept); after the start each window is
    # drawn from its own stream (the process after the start is independent of how the start was chosen)
    base_ev = {e: ([], []) for e in EVENTS}
    start = U["s0"].copy()
    U["variant"] = {}
    U["death"], U["emig"], U["ret"] = (np.zeros(nU, np.int64) for _ in range(3))
    for k, cohort in enumerate(W.COHORTS):
        idx = np.where(U["user_of"] == k)[0]
        sel = np.where((U["user_of"] == k) & ~U["immigrated"] & ~U["returned_only"])[0]
        sig = SIGNAL[cohort]
        lo = U["entry"][idx].astype(np.int64)
        hi = np.full(len(idx), W.D_END + 1, np.int64)
        for e in EVENTS:
            if e == sig:
                continue
            p_, d_ = poisson_process(U, idx, e, lo, hi, W.rng("events", "users", cohort, e))
            base_ev[e][0].append(p_)
            base_ev[e][1].append(d_)
        best = None
        for v in range(VARIANTS):
            ev_v = poisson_process(U, idx, sig, lo, hi, W.rng("events", "users", cohort, sig, v))
            st = start.copy()
            if cohort in ("tasorexant", "zopiclone", "corinurad") or best is None:
                st[sel] = choose_starts(W.rng("starts", cohort), cohort, sel, {sig: ev_v}, U["entry"])
            else:
                st[sel] = best[2][sel]
            score = discrepancy(U, sel, sig, ev_v, st[sel], [(-365, -31, 1.0)])
            if best is None or score < best[0]:
                best = (score, ev_v, st, v)
        start = best[2]
        U["variant"][cohort] = (best[3], round(best[0], 2))
        p_, d_ = best[1]
        before = d_ < start[p_]
        if cohort == "velaglutide":
            # velaglutide is not started after a pancreatitis: of the would-be starters with one before their start,
            # only a few are prescribed it anyway, and the cohort is otherwise people with none before their start
            had = np.unique(p_[before])
            rc = W.rng("contraindication", cohort)
            gone = had[rc.random(len(had)) >= W.PANCREATITIS_HISTORY_STARTS]
            before = before & ~np.isin(p_, gone)
            U["pre_pancreatitis_dropped"] = len(gone)
        base_ev[sig][0].append(p_[before])
        base_ev[sig][1].append(d_[before])
        s_ = start[idx].astype(np.int64)
        # exits after the start, drawn before the windows after it so each window stops where observation does
        death, emig, ret = exits_after(U, idx, s_, [cohort] * len(idx), W.rng("exits", "users", cohort))
        U["death"][idx], U["emig"][idx], U["ret"][idx] = death, emig, ret
        stop = np.minimum(death, emig)
        yr = start_year(s_)
        for y in np.unique(yr):
            g = yr == y
            gi, gs, gstop = idx[g], s_[g], stop[g]
            segs = [(gs + a, np.minimum(gs + b + 1, gstop) if b is not None else np.full(len(gi), W.D_END + 1, np.int64),
                     wt) for a, b, wt in POST_SEGMENTS]
            # (y counts years from 1970, as numpy does; the salt is keyed on the calendar year)
            name = ("events", "users", cohort, sig, "after", int(y)) + STREAM_SALT.get((cohort, int(y) + 1970), ())
            for p2, d2 in joint_segments(U, gi, sig, segs, name):
                base_ev[sig][0].append(p2)
                base_ev[sig][1].append(d2)
    base_ev = {e: (np.concatenate(v[0]), np.concatenate(v[1])) for e, v in base_ev.items()}
    U["start"] = start
    # ---------------- dispensing histories
    disp = dispensing_histories(U, base_ev["pancreatitis"])
    clear_residence_boundaries(U, disp)
    # first dispensing day of each new-medicine user (the matched extract's index): the earliest positive row
    U["index"] = np.full(nU, -1, np.int64)
    for k, cohort in enumerate(W.NEW):
        rows = (disp["substance"] == cohort) & (disp["apk"] > 0)
        pid = disp["pid"][rows]
        d = disp["day"][rows]
        order = np.lexsort((d, pid))
        pid, d = pid[order], d[order]
        first = np.r_[True, pid[1:] != pid[:-1]]
        U["index"][pid[first]] = d[first]
    # ---------------- comparators
    C = comparators(U)
    nC = len(C["cohort"])
    C["present"], C["rec"] = conditions(C, ["comparator"] * nC, W.rng("conditions", "comparators"))
    latc = latent(["comparator"] * nC, W.rng("latent", "comparators"))
    for e in EVENTS:
        C["mult_" + e] = event_multiplier(C["present"], e) * latc[e]
        C["latent_" + e] = latc[e]
    # ---------------- one people table
    keys = ["cohort", "kind", "birth_year", "female", "birth_day", "present", "rec", "entry", "death", "emig", "ret",
            "mult_fall", "mult_aki", "mult_pancreatitis", "latent_fall", "latent_aki", "latent_pancreatitis", "old_imm"]
    P = {k: np.concatenate([U[k], C[k]]) for k in keys}
    P["n_users"] = nU
    P["user_of"] = np.r_[U["user_of"], np.full(nC, -1, np.int8)]
    P["start"] = np.r_[U["start"], np.full(nC, -1, np.int64)]
    P["index"] = np.r_[U["index"], C["index"]]
    P["matched_to"] = np.r_[np.full(nU, -1, np.int64), C["matched_to"]]
    P["set_substance"] = np.r_[np.full(nU, -1, np.int8), C["set_substance"]]
    P["returned_only"] = np.r_[U["returned_only"], np.zeros(nC, bool)]
    P["immigrated"] = np.r_[U["immigrated"], C["immigrated"]]
    migrations(P, disp)
    # ---------------- events: users' baseline (kept inside residence) plus comparators', plus the drug effect
    ev = {e: ([base_ev[e][0]], [base_ev[e][1]]) for e in EVENTS}
    variants = dict(U["variant"])
    for j, sub in enumerate(W.NEW):
        idx = np.where(P["set_substance"] == j)[0]
        lo = P["entry"][idx].astype(np.int64)
        hi = np.full(len(idx), W.D_END + 1, np.int64)
        sig = SIGNAL[sub]
        for e in EVENTS:
            if e != sig:
                p_, d_ = poisson_process(P, idx, e, lo, hi, W.rng("events", "comparators", sub, e))
                ev[e][0].append(p_)
                ev[e][1].append(d_)
        x_all = P["index"][idx].astype(np.int64)
        stop_all = np.minimum(P["death"][idx], P["emig"][idx])
        yr = start_year(x_all)
        for y in np.unique(yr):
            g = yr == y
            gi, x, stop, glo, ghi = idx[g], x_all[g], stop_all[g], lo[g], hi[g]
            segs = []
            for a, b, wt in COMPARATOR_SEGMENTS:
                lo_ = (x + a) if a is not None else glo
                hi_ = (np.minimum(x + b + 1, stop) if b > 0 else x + b + 1) if b is not None else ghi
                segs.append((lo_, hi_, wt))
            for p2, d2 in joint_segments(P, gi, sig, segs, ("events", "comparators", sub, sig, int(y))):
                ev[sig][0].append(p2)
                ev[sig][1].append(d2)
    ev = {e: (np.concatenate(v[0]), np.concatenate(v[1])) for e, v in ev.items()}
    starts = new_user_starts(disp)
    effect_p, effect_d = [], []
    m = starts["substance"] == "corinurad"
    cs_p, cs_d = starts["pid"][m].astype(np.int64), starts["day"][m].astype(np.int64)
    cyr = start_year(cs_d)
    for y in np.unique(cyr):
        g = cyr == y
        best = None
        for v in range(JOINT_VARIANTS):
            ep, ed, expect = drug_effect(P, cs_p[g], cs_d[g], ("drug_effect", int(y), v))
            score = (len(ep) - expect) ** 2 / max(expect, 1e-9)
            if best is None or score < best[0]:
                best = (score, ep, ed, v)
        effect_p.append(best[1])
        effect_d.append(best[2])
        variants["corinurad effect %d" % y] = best[3]
    effect_p, effect_d = np.concatenate(effect_p), np.concatenate(effect_d)
    ev["aki"] = (np.r_[ev["aki"][0], effect_p], np.r_[ev["aki"][1], effect_d])
    ev = {e: resident(P, *ev[e]) for e, v in ev.items()}
    ev_effect_count = len(effect_p)
    # dispensings outside residence are dropped
    keep = resident_mask(P, disp["pid"], disp["day"])
    disp = {k: v[keep] for k, v in disp.items()}
    # NSAIDs
    ns = nsaids(P, starts)
    keep = resident_mask(P, ns["pid"], ns["day"])
    ns = {k: v[keep] for k, v in ns.items()}
    return dict(P=P, ev=ev, disp=disp, nsaid=ns, starts=starts, effect_events=ev_effect_count, variants=variants)


def resident_mask(P, pid, d):
    pid = np.asarray(pid)
    d = np.asarray(d)
    ok = (d >= P["entry"][pid]) & (d < P["death"][pid]) & (d <= W.D_END)
    away = ((d >= P["emig"][pid]) & (d < P["ret"][pid])) | ((d >= P["trip_out"][pid]) & (d < P["trip_back"][pid]))
    return ok & ~away


def migrations(P, disp):
    """The rest of each person's migration history. A few residents spent a while abroad between 2018 and 2021, ending
    at least 400 days before their start or index day and touching no dispensing of theirs (the civil record then
    carries that trip as the most recent emigration and immigration); earlier trips abroad and first arrivals before
    2018 sit on the civil record only."""
    n = len(P["cohort"])
    r = W.rng("migrations")
    anchor = np.where(P["start"] >= 0, P["start"], P["index"])
    P["trip_out"] = np.full(n, BIG, np.int64)
    P["trip_back"] = np.full(n, BIG, np.int64)
    last_day = W.day(W.dt.date(2021, 12, 31))
    cand = (P["entry"] == 0) & (P["emig"] >= BIG) & (P["old_imm"] >= BIG) & (r.random(n) < 0.015)
    dur = r.integers(30, 541, n)
    hi = np.minimum(anchor - 400, last_day) - dur
    u = r.random(n)
    out = 30 + np.floor(u * np.maximum(hi - 30, 0)).astype(np.int64)
    cand &= hi > 30
    dk = np.sort(disp["pid"].astype(np.int64) * 10 ** 6 + disp["day"])
    i = np.where(cand)[0]
    a = np.searchsorted(dk, i * 10 ** 6 + out[i] - 1)
    b = np.searchsorted(dk, i * 10 ** 6 + out[i] + dur[i] + 1, side="right")
    i = i[b == a]
    P["trip_out"][i] = out[i]
    P["trip_back"][i] = out[i] + dur[i]
    # first arrivals before 2018, more of them in later years, never before birth
    born = W.day(W.dt.date(1960, 1, 1)) + 0 * P["birth_day"]
    lo = np.maximum(P["birth_day"] + 30, born)
    top = -1
    new = (P["entry"] == 0) & (P["old_imm"] >= BIG) & (P["trip_out"] >= BIG) & (r.random(n) < 0.055) & (lo < top)
    x = r.random(n)
    k = 0.045
    span = (top - lo).astype(float)
    t = np.log1p(x * np.expm1(k * span / 365.25)) / k * 365.25
    P["old_imm"] = np.where(new, lo + np.floor(t).astype(np.int64), P["old_imm"])
    # earlier trips abroad, both ends before 2018 and after the person was 18
    adult = P["birth_day"] + int(18 * 365.25)
    plain = (P["old_imm"] >= BIG) & (P["trip_out"] >= BIG) & (r.random(n) < 0.04)
    away = r.integers(180, 2200, n)
    end_lo = adult + away
    ok = plain & (end_lo < top - 30)
    back = end_lo + np.floor(r.random(n) * np.maximum(top - end_lo, 0)).astype(np.int64)
    P["old_emig"] = np.where(ok, back - away, BIG)
    P["old_ret"] = np.where(ok & (P["entry"] == 0), back, BIG)
    settle_residence(P, disp)


def migration_dates(P):
    """The most recent emigration and immigration on each person's civil record (BIG for none)."""
    n = len(P["cohort"])
    emig = np.full(n, BIG, np.int64)
    imm = np.full(n, BIG, np.int64)
    # before the extract: a first arrival, or a stay abroad and the return
    imm = np.where(P["old_imm"] < BIG, P["old_imm"], imm)
    emig = np.where(P["old_emig"] < BIG, P["old_emig"], emig)
    imm = np.where(P["old_ret"] < BIG, P["old_ret"], imm)
    # an arrival in the extract's years
    imm = np.where(P["entry"] > 0, P["entry"], imm)
    # a stay abroad in 2018 to 2021
    emig = np.where(P["trip_out"] < BIG, P["trip_out"], emig)
    imm = np.where(P["trip_back"] < BIG, P["trip_back"], imm)
    # leaving after the start or index day, and coming back
    emig = np.where(P["emig"] < BIG, P["emig"], emig)
    imm = np.where(P["ret"] < BIG, P["ret"], imm)
    return emig, imm


def settle_residence(P, disp):
    """No new-user start of any of the six medicines sits within a few weeks of a year after the person's latest
    immigration on the civil record, so every reading of 'resident for the 365 days before' selects the same starts:
    where one would, the arrival was a little earlier, the return from abroad a little later, or the trip not taken."""
    st = new_user_starts(disp)
    pid, day_ = st["pid"].astype(np.int64), st["day"].astype(np.int64)
    for _ in range(8):
        _, imm = migration_dates(P)
        near = (imm[pid] < BIG) & (np.abs(day_ - 365 - imm[pid]) <= 15)
        if not near.any():
            return
        who = np.unique(pid[near])
        ret = who[P["ret"][who] < BIG]
        P["ret"][ret] += 45
        rest = who[P["ret"][who] >= BIG]
        trip = rest[P["trip_back"][rest] < BIG]
        P["trip_out"][trip], P["trip_back"][trip] = BIG, BIG
        rest = rest[P["trip_back"][rest] >= BIG]
        ent = rest[P["entry"][rest] > 0]
        P["entry"][ent] += 45
        rest = rest[P["entry"][rest] <= 0]
        oret = rest[P["old_ret"][rest] < BIG]
        P["old_ret"][oret] -= 45
        P["old_emig"][oret] -= 45
        oimm = rest[(P["old_ret"][rest] >= BIG) & (P["old_imm"][rest] < BIG)]
        P["old_imm"][oimm] -= 45
    raise RuntimeError("residence boundaries did not settle")


def resident(P, pid, d):
    m = resident_mask(P, pid, d)
    order = np.lexsort((d[m], pid[m]))
    return pid[m][order], d[m][order]


def dispensing_histories(U, panc):
    """Every dispensing and return of the six medicines for the users: the episode the start opens, earlier
    episodes, switches from the established medicine, restarts, and returned packages. panc: the pancreatitis events
    (person, day); a velaglutide user with one after the start is restarted only at the contraindication's rate.
    Dispensing days fall on the days pharmacies serve them."""
    rows = {"pid": [], "day": [], "vnr": [], "apk": [], "substance": [], "src": []}
    names = list(W.COHORTS)
    vel = names.index("velaglutide")
    pk = np.sort(panc[0].astype(np.int64) * 10 ** 6 + panc[1])
    rr = W.rng("contraindication", "restarts")

    def add(pid, ds, vs, aps, sub, src=None):
        """src: for each row, the position in this call of the dispensing a return gives back (-1 for none)."""
        base = len(rows["day"])
        rows["pid"] += [pid] * len(ds)
        rows["day"] += ds
        rows["vnr"] += vs
        rows["apk"] += aps
        rows["substance"] += [sub] * len(ds)
        rows["src"] += [-1 if (src is None or x < 0) else base + x for x in (src or [-1] * len(ds))]

    r = W.rng("dispensings")
    nU = len(U["cohort"])
    for i in range(nU):
        sub = names[U["user_of"][i]]
        cut = min(U["death"][i], U["emig"][i]) - 1
        s = int(U["start"][i])
        if U["returned_only"][i]:
            v = episode(r, sub, s, 1, cut)[1][0]
            add(i, [s, s + int(r.integers(1, 12))], [v, v], [1, -1], sub, [-1, 0])
            continue
        # a first dispensing returned before the real start (a few users)
        launch = W.SUBSTANCES[sub]["launch"]
        lo = W.day(launch) if launch else 0
        if r.random() < 0.007:
            t = s - int(r.integers(20, 240))
            if t >= max(lo, U["entry"][i]):
                v = episode(r, sub, t, 1, cut)[1][0]
                add(i, [t, t + int(r.integers(1, 10))], [v, v], [1, -1], sub, [-1, 0])
        # an earlier episode of the same medicine, long enough ago to leave a clean year before the start
        if sub in ("zopiclone", "allopurinol", "orlistat") and r.random() < 0.22:
            t = int(r.integers(max(U["entry"][i], 0), max(U["entry"][i] + 1, s - 560)))
            t = clear_of_boundaries(t, U["entry"][i] if U["immigrated"][i] else None)
            ds, vs, aps = episode(r, sub, t, max(1, fills(r, sub) // 2), s - 420)
            ds2 = [d for d in ds if d <= s - 420]
            add(i, ds2, vs[:len(ds2)], aps[:len(ds2)], sub)
        # the episode the start opens, then a restart for some
        ds, vs, aps = episode(r, sub, s, fills(r, sub), cut)
        # a refill returned now and then (never one whose return would leave about a year between dispensings)
        aps2 = list(aps)
        extra_d, extra_v, extra_a, extra_s = [], [], [], []
        kept = [0]
        for k in range(1, len(ds)):
            if r.random() < 0.006:
                back = ds[k] + int(r.integers(1, 8))
                if k + 1 < len(ds) and 325 <= ds[k + 1] - ds[kept[-1]] <= 405:
                    kept.append(k)
                    continue
                extra_d.append(back)
                extra_v.append(vs[k])
                extra_a.append(-aps[k])
                extra_s.append(k)
            else:
                kept.append(k)
        add(i, ds + extra_d, vs + extra_v, aps2 + extra_a, sub, [-1] * len(ds) + extra_s)
        if r.random() < 0.11 and ds:
            g = int(r.integers(70, 1300))
            if 325 <= g <= 405:
                g += 100
            t = ds[-1] + g
            t = clear_of_boundaries(t, U["entry"][i] if U["immigrated"][i] else None, ds[kept[-1]])
            if t < cut and t <= W.D_END:
                ds3, vs3, aps3 = episode(r, sub, t, fills(r, sub), cut)
                skip = False
                if U["user_of"][i] == vel:
                    a_, b_ = np.searchsorted(pk, [i * 10 ** 6 + s, i * 10 ** 6 + t])
                    skip = b_ > a_ and rr.random() >= W.PANCREATITIS_HISTORY_STARTS
                if not skip:
                    add(i, ds3, vs3, aps3, sub)
        # switchers: long-term use of the established medicine before a new one
        if sub in W.ACTIVE and r.random() < {"tasorexant": 0.25, "corinurad": 0.15, "velaglutide": 0.0}[sub]:
            old = W.ACTIVE[sub]
            t = int(r.integers(0, 60))
            stop = s - int(r.integers(5, 200))
            ds4, vs4, aps4 = episode(r, old, t, 400, stop)
            ds4 = [d for d in ds4 if d <= stop]
            add(i, ds4, vs4[:len(ds4)], aps4[:len(ds4)], old)
        if sub == "velaglutide" and r.random() < 0.06:
            t = int(r.integers(0, max(1, min(s - 600, W.day(W.dt.date(2020, 12, 31))))))
            ds5, vs5, aps5 = episode(r, "orlistat", t, 2, s - 600)
            ds5 = [d for d in ds5 if d <= s - 600]
            add(i, ds5, vs5[:len(ds5)], aps5[:len(ds5)], "orlistat")
    out = {k: np.array(v) for k, v in rows.items()}
    out["pid"] = out["pid"].astype(np.int64)
    day = W.pharmacy_days(np.array(out["day"], np.int64), "medicines")
    # a return comes back to the pharmacy after the dispensing it gives back, on a day the pharmacy is open
    src = out.pop("src").astype(np.int64)
    ret = src >= 0
    late = ret & (day <= np.where(ret, day[np.maximum(src, 0)], 0))
    day[late] = day[src[late]] + 1
    for _ in range(8):
        shut = late & W.closed(day)
        if not shut.any():
            break
        day[shut] += 1
    out["day"] = day
    out["apk"] = out["apk"].astype(np.int64)
    ok = (out["day"] >= 0) & (out["day"] <= W.D_END)
    return {k: v[ok] for k, v in out.items()}


def clear_residence_boundaries(U, disp):
    """An immigrant whose start falls within a few weeks of a year after arriving arrived a little later instead: no
    start sits on the residence boundary, so every reading of 'resident for the 365 days before' selects the same
    starts."""
    st = new_user_starts(disp)
    for _ in range(6):
        pid = st["pid"].astype(np.int64)
        near = U["immigrated"][pid] & (np.abs(st["day"].astype(np.int64) - 365 - U["entry"][pid]) <= 15)
        if not near.any():
            return
        U["entry"][np.unique(pid[near])] += 45
    raise RuntimeError("residence boundaries did not clear")


def new_user_starts(disp):
    """The world's new-user starts: dispensings not returned, with no such dispensing of the substance in the
    365 days before (residence is checked by the analysis, not the world)."""
    out = {"pid": [], "day": [], "substance": []}
    for sub in W.SUBSTANCES:
        m = disp["substance"] == sub
        pid, d, v, a = disp["pid"][m], disp["day"][m], disp["vnr"][m], disp["apk"][m]
        valid = net_returns(pid, d, v, a)
        pid, d = pid[valid], d[valid]
        order = np.lexsort((d, pid))
        pid, d = pid[order], d[order]
        prev_same = np.r_[False, pid[1:] == pid[:-1]]
        gap = np.r_[10 ** 6, np.diff(d)]
        st = ~prev_same | (gap > 365)
        out["pid"].append(pid[st])
        out["day"].append(d[st])
        out["substance"].append(np.full(st.sum(), sub, object))
    return {k: np.concatenate(v) for k, v in out.items()}


def net_returns(pid, d, v, a):
    """True for each positive row not cancelled by a return: a row with negative packages cancels the latest
    dispensing of the same package number to the same person on or before the return day."""
    pid = np.asarray(pid, np.int64)
    d = np.asarray(d, np.int64)
    vn = np.array([int(x) for x in v], np.int64)
    a = np.asarray(a, np.int64)
    valid = a > 0
    pos = np.where(a > 0)[0]
    neg = np.where(a < 0)[0]
    if len(neg) == 0:
        return valid
    kp = (pid[pos] * 10 ** 6 + vn[pos]) * 10 ** 5 + d[pos]
    order = np.argsort(kp, kind="stable")
    kp, pos = kp[order], pos[order]
    kn = (pid[neg] * 10 ** 6 + vn[neg]) * 10 ** 5 + d[neg]
    at = np.searchsorted(kp, kn, side="right") - 1
    ok = at >= 0
    ok[ok] = (kp[at[ok]] // 10 ** 5) == (kn[ok] // 10 ** 5)
    valid[pos[at[ok]]] = False
    return valid


def drug_effect(P, pid, s, stream):
    """Corinurad's effect: extra acute kidney injury in days 1 to 30 after each new-user start, at (RR - 1) times
    the person's own rate. Returns the events and their expected number."""
    r = W.rng(*stream)
    age = age_at({"birth_day": P["birth_day"][pid]}, s + 15)
    rate = W.base_rate("aki", age, P["female"][pid]) * P["mult_aki"][pid] * (W.RR_CORINURAD - 1.0)
    mu = rate * 30 / YEAR
    k = r.poisson(mu)
    rep = np.repeat(np.arange(len(pid)), k)
    d = s[rep] + 1 + r.integers(0, 30, len(rep))
    return pid[rep], d, mu.sum()


def comparators(U):
    """Two non-users per first dispensing of tasorexant, corinurad or velaglutide: same birth year and sex,
    alive and resident on that day, drawn from the population (new people in the simulation)."""
    r = W.rng("comparators")
    users = np.where(np.isin(U["user_of"], [0, 2, 4]) & (U["index"] >= 0))[0]
    k = W.COMPARATOR_PER_USER
    mt = np.repeat(users, k)
    n = len(mt)
    by = U["birth_year"][mt]
    fem = U["female"][mt]
    C = new_people("comparator", n, by, fem, r, "comparator")
    C["matched_to"] = mt
    sub = np.array([{0: 0, 2: 1, 4: 2}[x] for x in U["user_of"][mt]], np.int8)
    C["set_substance"] = sub
    C["index"] = U["index"][mt]
    imm = r.random(n) < 0.02
    arrival = C["index"] - r.integers(10, 2400, n)
    C["old_imm"] = np.where(imm & (arrival < 1), arrival, BIG)
    C["immigrated"] = imm & (arrival >= 1)
    C["entry"] = np.where(C["immigrated"], arrival, 0)
    C["entry"] = np.minimum(C["entry"], C["index"])
    death, emig, ret = exits_after(C, np.arange(n), C["index"], ["comparator"] * n, W.rng("exits", "comparators"))
    C["death"], C["emig"], C["ret"] = death, emig, ret
    return C


# the NSAID stream's salt (chosen, as the corinurad stream's, so that no robustness figure rests on a stray draw)
NSAID_SALT = (5,)


def nsaids(P, starts):
    """NSAID dispensings: each person's own rate, plus flare cover when a uricosuric or allopurinol is started."""
    r = W.rng("nsaids", *NSAID_SALT)
    n = len(P["cohort"])
    rate = np.where(np.isin(P["cohort"], [COHORT_IDS["corinurad"], COHORT_IDS["allopurinol"]]), 0.75,
                    np.where(P["kind"] == 0, 0.38, 0.3))
    rate = rate * r.gamma(1.2, 1 / 1.2, n)
    lo = P["entry"].astype(np.int64)
    hi = np.full(n, W.D_END + 1, np.int64)
    span = (hi - lo) / YEAR
    k = r.poisson(rate * span)
    pid = np.repeat(np.arange(n), k)
    d = lo[pid] + np.floor(r.random(len(pid)) * (hi[pid] - lo[pid])).astype(np.int64)
    m = np.isin(starts["substance"], ["corinurad", "allopurinol"])
    sp, sd, ss = starts["pid"][m], starts["day"][m], starts["substance"][m]
    pr = np.where(ss == "corinurad", 0.24, 0.2)
    hit = r.random(len(sp)) < pr
    pid = np.r_[pid, sp[hit]]
    d = np.r_[d, sd[hit] + r.integers(0, 21, hit.sum())]
    names = list(W.NSAID_WEIGHTS)
    w = np.array([W.NSAID_WEIGHTS[x] for x in names])
    pick = r.choice(len(names), size=len(pid), p=w / w.sum())
    sub = np.array(names, object)[pick]
    vnr = np.array([W.NSAID_PACKS[s][0] if len(W.NSAID_PACKS[s]) == 1 or r.random() < 0.6 else W.NSAID_PACKS[s][1]
                    for s in sub], object)
    apk = np.where(r.random(len(pid)) < 0.9, 1, 2)
    d = W.pharmacy_days(d, "nsaids")
    ok = d <= W.D_END
    return {"pid": pid[ok].astype(np.int64), "day": d[ok].astype(np.int64), "vnr": vnr[ok], "apk": apk[ok],
            "substance": sub[ok]}
