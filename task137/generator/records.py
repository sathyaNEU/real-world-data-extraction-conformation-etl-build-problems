"""Visit-level records written from the day-grain world: each patient's practice or clinic, request date, arrival,
call and completion; the turned-away patients' arrival times; the old kiosk's tickets and the new system's events."""
import datetime as dt
import numpy as np
import params as P

SPEC = {s[0]: s for s in P.SPECIALTIES}
SPEC_NAMES = [s[0] for s in P.SPECIALTIES]


def practice_weights(d):
    """Each practice's share of its group's arrivals on day d, by list size."""
    yrs = (d - P.START).days / 365.25
    out = {"P": [], "N": []}
    for code, name, size, g, own in P.PRACTICES:
        out["P" if own else "N"].append((code, size * (1 + g) ** yrs))
    res = {}
    for k, v in out.items():
        tot = sum(s for _, s in v)
        res[k] = [(c, s / tot) for c, s in v]
    return res


def visit_code(code, d):
    if code == P.MERGED_FROM and d >= P.MERGER:
        return P.MERGED_INTO
    return code


def clinic_code(spec, issued):
    s = SPEC[spec]
    return s[3] if issued < P.CODES_RENUMBERED else s[4]


def request_issue_date(rng, d, spec, days_index, prog_window=None):
    """The clinic session that issued a hospital request: one of the specialty's clinic weekdays before or on d."""
    wds = SPEC[spec][1]
    lag = int(min(rng.geometric(0.22) - 1, 34))
    x = d - dt.timedelta(lag)
    for _ in range(14):
        if x.weekday() in wds and x not in P.BH and (prog_window is None or prog_window[0] <= x):
            return x
        x -= dt.timedelta(1)
    x = d
    while x.weekday() not in wds or x in P.BH:
        x -= dt.timedelta(1)
    return x


def gp_issue_date(rng, d):
    lag = int(min(rng.geometric(0.16) - 1, 40))
    x = d - dt.timedelta(lag)
    while x.weekday() >= 5 or x in P.BH:
        x -= dt.timedelta(1)
    return x


def arrival_minutes(rng, k):
    seg = rng.choice(5, size=k, p=[0.20, 0.27, 0.25, 0.18, 0.10])
    lo = np.array([435, 480, 540, 630, 750])
    hi = np.array([480, 540, 630, 750, 900])
    return np.sort(lo[seg] + rng.random(k) * (hi[seg] - lo[seg]))


def build(W, seed=P.SEED, rseed=None):
    rr = np.random.default_rng([P.RECORDS_SEED if rseed is None else rseed, 3])    # who, which practice or clinic, request dates
    rt = np.random.default_rng([seed, 4])    # times, service, bays
    days = W["days"]
    phleb_speed = 9.6 * np.exp(rt.normal(0, 0.12, size=P.POSTS))     # each post's mean draw time in minutes
    visits, away_rows = [], []
    for i, d in enumerate(days):
        if d > P.REC_END:
            break
        seen = {g: int(W["seen"][g][i]) for g in "PNH"}
        away = {g: int(W["away"][g][i]) for g in "PNH"}
        tot_seen, tot_away = sum(seen.values()), sum(away.values())
        mins = arrival_minutes(rt, tot_seen + tot_away)
        if tot_away:
            # tickets run out at the last seen arrival; everyone after is turned away
            seen_m, away_m = mins[:tot_seen], mins[tot_seen:]
        else:
            seen_m, away_m = mins, np.array([])
        lab = np.array(["P"] * seen["P"] + ["N"] * seen["N"] + ["H"] * seen["H"])
        rr.shuffle(lab)
        # hospital programme patients: which specialty
        pw = practice_weights(d)
        base_h = np.array([SPEC[s][2] for s in SPEC_NAMES])
        prog = W["prog_spec"][i]
        hmix = base_h * W["lam"]["H"][i] / base_h.sum()
        for sp, v in prog.items():
            hmix[SPEC_NAMES.index(sp)] += v
        hmix = hmix / hmix.sum()
        # staff on the floor: substantive posts that worked, then bank
        posts = [p for p in range(P.POSTS) if W["status"][i, p] == "CLIN"]
        speeds = [phleb_speed[p] for p in posts] + [11.2] * int(W["bank"][i])
        bays = [p + 1 for p in posts] + ["B%d" % (k + 1) for k in range(int(W["bank"][i]))]
        free = 450.0 + rt.uniform(-1.5, 4.0, size=len(speeds))
        for j, m in enumerate(seen_m):
            g = lab[j]
            fasting = m < 600 and rt.random() < 0.26
            if g == "H":
                sp = SPEC_NAMES[rr.choice(len(SPEC_NAMES), p=hmix)]
                pr = None
                for spx, a, b, v in P.PROGRAMMES:
                    if spx == sp and a <= d <= b + dt.timedelta(10) and rr.random() < prog.get(sp, 0) / max(hmix[SPEC_NAMES.index(sp)] * sum(W["A"][x][i] for x in "H"), 1e-9):
                        pr = (a, b)
                issued = request_issue_date(rr, d, sp, i, pr)
                org = clinic_code(sp, issued)
                practice = None
            else:
                codes, wts = zip(*pw[g])
                practice = codes[rr.choice(len(codes), p=np.array(wts))]
                org = visit_code(practice, d)
                issued = gp_issue_date(rr, d)
                sp = None
            k = int(np.argmin(free))
            called = max(m, free[k]) + rt.uniform(0.2, 1.4)
            dur = rt.lognormal(np.log(speeds[k]), 0.35)
            if rt.random() < 0.04:
                dur += rt.uniform(10, 22)
            if fasting:
                dur *= 1.08
            done = called + dur
            free[k] = done + rt.uniform(0.3, 1.8)
            recall = None
            if rt.random() < 0.021:
                recall = called + rt.uniform(6, 19)
                done = done + (recall - called)
                free[k] = done + 0.5
            visits.append((d, g, sp, practice, org, issued, m, called, recall, done, bays[k], fasting))
        if tot_away:
            alab = np.array(["P"] * away["P"] + ["N"] * away["N"] + ["H"] * away["H"])
            rr.shuffle(alab)
            for j, m in enumerate(away_m):
                away_rows.append((d, alab[j], m))
    return visits, away_rows, phleb_speed

def pas_relabel(V, seed=P.SEED):
    """From 16 March 2026 request forms carry the new PAS's clinic codes; from 1 April 2026 the clinics run to their
    2026-27 templates, so a request issued from then on falls on one of the clinic's new weekdays. Only hospital requests
    move; the draws come from their own stream, so no other record changes."""
    rq = np.random.default_rng([seed, 7])
    out = []
    for v in V:
        d, g, sp, prac, org, issued = v[:6]
        if g == "H":
            if issued >= P.TEMPLATES_FROM:
                issued = new_template_day(rq, sp, issued)
            org = P.NEW_CLINIC[sp][0] if issued >= P.PAS_LIVE else SPEC[sp][3]
        out.append((d, g, sp, prac, org, issued) + tuple(v[6:]))
    return out


def new_template_day(rq, sp, issued):
    """A session of the clinic's 2026-27 template in the week up to the drawn issue date; where the template has none
    since 1 April, the clinic's last session under the old one."""
    wds = P.NEW_CLINIC[sp][1]
    cand = [issued - dt.timedelta(k) for k in range(7)]
    cand = [x for x in cand if x >= P.TEMPLATES_FROM and x.weekday() in wds and x not in P.BH]
    if cand:
        return cand[int(rq.integers(len(cand)))]
    x = min(issued, P.TEMPLATES_FROM - dt.timedelta(1))
    while x.weekday() not in SPEC[sp][1] or x in P.BH:
        x -= dt.timedelta(1)
    return x
