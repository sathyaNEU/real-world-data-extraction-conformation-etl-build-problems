"""The clean truth for task266: every admission the college's records hold from fall 2020 to spring 2027, simulated
term by term from each program's rates of the award, transfer out and withdrawal, before any export is written. The
review's three entering classes (fall 2023, 2024 and 2025) are drawn on their own random streams, so nothing built
after them (the other admissions, the fall 2026 term, the schedule) can move the call. `rungs` computes every rung of
the ladder on the clean truth for checks.py (R3a, R3b) and for the seed search."""
import numpy as np

import common as K

SEED = 3001

# per program: entering students per fall class, part-time share, share transferring in, campus mix (QNL, TRV, HOL),
# the chance of the award at the end of each term counted from entry (full-time, first-time student), the chance of a
# transfer out at a fall or spring census in the first, second and later years, and of a withdrawal at the census of
# the first spring, the second fall and later fall or spring terms
P = {
    "GS": dict(n=520, pt=.44, tr=.12, camp=(.52, .27, .21),
               aw=[0, 0, 0, .04, .19, .05, .09, .21, .06, .08, .15], to=(.055, .095, .085), wd=(.165, .085, .060)),
    "BIO": dict(n=150, pt=.30, tr=.14, camp=(.64, .21, .15),
                aw=[0, 0, 0, .04, .19, .05, .09, .22, .07, .08, .15], to=(.050, .090, .080), wd=(.155, .080, .058)),
    "BUS": dict(n=240, pt=.43, tr=.13, camp=(.50, .28, .22),
                aw=[0, 0, 0, .05, .21, .05, .10, .23, .07, .08, .15], to=(.045, .085, .075), wd=(.155, .075, .055)),
    "PSY": dict(n=170, pt=.40, tr=.12, camp=(.55, .25, .20),
                aw=[0, 0, 0, .04, .20, .05, .09, .22, .07, .08, .15], to=(.050, .090, .080), wd=(.165, .080, .058)),
    "MA": dict(n=130, pt=.33, tr=.08, camp=(.42, .30, .28),
               aw=[0, 0, 0, .05, .21, .05, .06, .12, .05, .06, .09], to=(.008, .012, .012), wd=(.205, .095, .080)),
    "ECE": dict(n=110, pt=.70, tr=.07, camp=(.38, .30, .32),
                aw=[0, 0, 0, .02, .09, .04, .07, .14, .07, .08, .12], to=(.005, .008, .008), wd=(.070, .030, .022)),
    "CJ": dict(n=160, pt=.40, tr=.10, camp=(.48, .26, .26),
               aw=[0, 0, 0, .05, .24, .06, .11, .25, .08, .08, .14], to=(.020, .035, .030), wd=(.165, .075, .055)),
    "HVR": dict(n=90, pt=.35, tr=.06, camp=(.30, .45, .25),
                aw=[0, 0, 0, .06, .29, .08, .10, .25, .09, .08, .12], to=(.004, .008, .008), wd=(.150, .070, .050)),
    "NUR": dict(n=140, pt=.24, tr=.18, camp=(.70, .30, .00),
                aw=[0, 0, 0, .02, .15, .06, .13, .38, .10, .10, .14], to=(.010, .015, .015), wd=(.120, .060, .045)),
}
PT_AWARD, PT_WD = .45, 1.15
TR_AWARD = (1.9, 1.2)                 # transferring in: terms 4 and 5, later terms
GP_WD = {2: .52, 4: .80}              # guided pathways advising from fall 2024: first spring and second fall
P_DEATH = .00025
SWITCH = {"GS": ("BUS", "PSY", "BIO"), "BIO": ("NUR", "GS"), "BUS": ("GS", "PSY"), "PSY": ("GS", "ECE"),
          "MA": ("NUR", "GS"), "ECE": ("PSY", "GS"), "CJ": ("GS", "PSY"), "HVR": ("GS",), "NUR": ("BIO", "MA", "GS")}
P_SWITCH = {True: .022, False: .012}
P_READMIT = .11
OBS = {c: K.index_of(K.fall(c), K.LAST) for c in K.CLASSES}     # terms observed at the extract: 11, 8, 5


def is_fs(code):
    return K.TERM[code]["season"] in ("FA", "SP")


def rates(prog, cls, t, code, pt, tr_in):
    """(award, transfer out, withdrawal) chances at term `code`, the admission's term index t."""
    p = P[prog]
    aw = p["aw"][t - 1] if t <= len(p["aw"]) else p["aw"][-1] * .8
    if pt:
        aw *= PT_AWARD
    if tr_in:
        aw *= TR_AWARD[0] if t in (4, 5) else TR_AWARD[1]
    to = wd = 0.0
    if t >= 2 and is_fs(code):
        yr = 0 if t <= 3 else (1 if t <= 6 else 2)
        to = p["to"][yr]
        wd = p["wd"][0] if t == 2 else (p["wd"][1] if t == 4 else p["wd"][2])
        if pt:
            wd *= PT_WD
        if cls and cls >= 2024:
            wd *= GP_WD.get(t, 1.0)
    return min(aw, .95), to, wd


def follow(rng, prog, cls, pt, tr_in, start_t, start_code, last_code, readmitted=False):
    """Simulate one admission from its term start_code (term index start_t): returns (reason, exit code or None,
    switches), switches a list of (code, new program). A readmitted student is enrolled in the readmission term."""
    cur = prog
    switches = []
    t, code = start_t, start_code
    first = True
    while True:
        aw, to, wd = rates(prog, cls, t, code, pt, tr_in)
        if rng.random() < P_DEATH:
            return "DC", code, switches
        if t >= 2 and is_fs(code) and not (readmitted and first):
            u = rng.random()
            if u < wd:
                return "WD", code, switches
            if u < wd + to:
                return "TO", code, switches
            if t in (2, 4, 5) and rng.random() < P_SWITCH[prog in K.TRANSFER]:
                opts = SWITCH[cur]
                new = opts[int(rng.integers(len(opts)))]
                if new != cur:
                    switches.append((code, new))
                    cur = new
        if rng.random() < aw:
            return "GR", code, switches
        first = False
        if code >= last_code:
            break
        code = K.nth(code, 1)
        t += 1
    return None, None, switches


def entering(seed):
    """The three entering classes: one record per entering student, with the admission's ending and any readmission
    that followed a withdrawal."""
    out = []
    for cls in K.CLASSES:
        for prog in K.CODES:
            rng = np.random.default_rng([seed, cls, K.CODES.index(prog)])
            p = P[prog]
            grow = {2023: 1.0, 2024: 1.03, 2025: 1.055}[cls]
            n = int(round(p["n"] * grow * rng.uniform(.93, 1.07)))
            for i in range(n):
                pt = rng.random() < p["pt"]
                tr_in = rng.random() < p["tr"]
                campus = ["QNL", "TRV", "HOL"][int(rng.choice(3, p=p["camp"]))]
                reason, code, sw = follow(rng, prog, cls, pt, tr_in, 1, K.fall(cls), K.LAST)
                rec = dict(cls=cls, prog=prog, pt=pt, tr_in=tr_in, campus=campus, reason=reason, exit=code,
                           switches=sw, readmit=None, age=int(rng.integers(0, 10**6)), pell=rng.random() < .46)
                if reason == "WD" and rng.random() < P_READMIT:
                    k = int(rng.integers(1, 4))
                    later = [c for c in K.CODES_IN_ORDER if c > code and is_fs(c)][:k]
                    if later and later[-1] <= K.LAST:
                        back = later[-1]
                        cur = sw[-1][1] if sw else prog
                        rprog = cur if rng.random() < .65 else "GS"
                        t0 = K.index_of(K.fall(cls), code)
                        r_reason, r_code, r_sw = follow(rng, rprog, None, pt, tr_in, max(t0, 2), back, K.LAST, readmitted=True)
                        rec["readmit"] = dict(term=back, prog=rprog, reason=r_reason, exit=r_code, switches=r_sw,
                                              t0=max(t0, 2))
                out.append(rec)
    return out


# ---------------------------------------------------------------------------------------------- the estimators
def spells(recs, mode="golden"):
    """(event index or None, kind, last observed index) per record, kind one of GR, X (another ending), C (censored).
    mode: golden; person (followed across a readmission); redate (exits one fall or spring term earlier);
    dc_compete (deaths as an ending)."""
    out = []
    for r in recs:
        obs = OBS[r["cls"]]
        reason, code = r["reason"], r["exit"]
        if mode == "person" and r["readmit"] and reason == "WD":
            ra = r["readmit"]
            if ra["reason"] is None:
                reason, code = None, None
            else:
                reason, code = ra["reason"], ra["exit"]
        if reason == "DC":
            if mode == "dc_compete":
                out.append((K.index_of(K.fall(r["cls"]), code), "X", obs))
            elif mode == "dc_censor":
                out.append((None, "C", K.index_of(K.fall(r["cls"]), code)))
            continue
        if reason is None:
            out.append((None, "C", obs))
            continue
        t = K.index_of(K.fall(r["cls"]), code)
        if mode == "redate" and reason in ("TO", "WD"):
            back = [c for c in K.CODES_IN_ORDER if c < code and is_fs(c) and c >= K.fall(r["cls"])]
            t = K.index_of(K.fall(r["cls"]), back[-1]) if back else t
        out.append((t, "GR" if reason == "GR" else ("X" + reason), obs))
    return out


def aj(sp, horizon=K.WINDOW, compete=("XTO", "XWD", "X"), curve=False):
    """Discrete-time cumulative incidence of GR with the kinds in compete as endings; any other kind censored at its
    term; open records censored after their last observed term."""
    S, F, path = 1.0, 0.0, []
    for t in range(1, horizon + 1):
        n = sum(1 for e, k, o in sp if (e is not None and e >= t) or (e is None and o >= t))
        a = sum(1 for e, k, o in sp if e == t and k == "GR")
        d = sum(1 for e, k, o in sp if e == t and (k == "GR" or k in compete))
        if n:
            F += S * a / n
            S *= 1 - d / n
        path.append(100 * F)
    return path if curve else 100 * F


def km(sp, horizon=K.WINDOW, exits_first=False):
    """One minus Kaplan-Meier of GR with every other ending censored at its term (at risk in that term unless
    exits_first, when an exit at a census leaves the risk set before that term's awards)."""
    S = 1.0
    for t in range(1, horizon + 1):
        n = sum(1 for e, k, o in sp if (e is not None and e >= t) or (e is None and o >= t))
        a = sum(1 for e, k, o in sp if e == t and k == "GR")
        if exits_first:
            n -= sum(1 for e, k, o in sp if e == t and k != "GR")
        if n:
            S *= 1 - a / n
    return 100 * (1 - S)


def crude(sp, horizon=K.WINDOW):
    return 100 * sum(1 for e, k, o in sp if k == "GR" and e <= horizon) / len(sp)


def complete_case(sp, horizon=K.WINDOW):
    closed = [(e, k) for e, k, o in sp if e is not None and e <= min(o, horizon)]
    return 100 * sum(1 for e, k in closed if k == "GR") / len(closed)


def stratified(recs, prog):
    """Class by class: each class's own term rates where it was observed, the other classes' pooled rates beyond,
    weighted by class size."""
    by = {c: spells([r for r in recs if r["prog"] == prog and r["cls"] == c]) for c in K.CLASSES}
    total, num = 0, 0.0
    for c in K.CLASSES:
        S, F = 1.0, 0.0
        for t in range(1, K.WINDOW + 1):
            pool = by[c] if OBS[c] >= t else [x for cc in K.CLASSES if OBS[cc] >= t for x in by[cc]]
            n = sum(1 for e, k, o in pool if (e is not None and e >= t) or (e is None and o >= t))
            a = sum(1 for e, k, o in pool if e == t and k == "GR")
            d = sum(1 for e, k, o in pool if e == t)
            if n:
                F += S * a / n
                S *= 1 - d / n
        num += F * len(by[c])
        total += len(by[c])
    return 100 * num / total


def final_program(r):
    return r["switches"][-1][1] if r["switches"] else r["prog"]


def by_final(recs):
    """Each record placed in its program at the ending (or now), not the program entered."""
    return [dict(r, prog=final_program(r)) for r in recs]


def own_degree(recs):
    """Only the entered program's own degree counts: an award in another program becomes another ending."""
    out = []
    for r in recs:
        if r["reason"] == "GR" and final_program(r) != r["prog"]:
            r = dict(r, reason="WD")
        out.append(r)
    return out


def rungs(recs):
    R = {}
    fin, own = by_final(recs), own_degree(recs)
    for p in K.CODES:
        rs = [r for r in recs if r["prog"] == p]
        sp = spells(rs)
        R[p] = dict(
            golden=aj(sp), op=km(sp), op_exits_first=km(sp, exits_first=True), crude=crude(sp),
            complete=complete_case(sp), closed2023=crude(spells([r for r in rs if r["cls"] == 2023])),
            half_wd=aj(sp, compete=("XWD",)), half_to=aj(sp, compete=("XTO",)), strat=stratified(recs, p),
            person=aj(spells(rs, "person")), redate=aj(spells(rs, "redate")), dc_compete=aj(spells(rs, "dc_compete")),
            dc_censor=aj(spells(rs, "dc_censor")), n=len(sp),
            final=aj(spells([r for r in fin if r["prog"] == p])), own=aj(spells([r for r in own if r["prog"] == p])))
    return R


def review(R, rung):
    return [p for p in K.CODES if R[p][rung] < K.FLOOR]


if __name__ == "__main__":
    import sys
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else SEED
    recs = entering(seed)
    R = rungs(recs)
    keys = ["crude", "complete", "op", "op_exits_first", "closed2023", "half_wd", "half_to", "strat", "golden"]
    print("%-4s %5s " % ("", "n") + " ".join("%8s" % k[:8] for k in keys))
    for p in K.CODES:
        print("%-4s %5d " % (p, R[p]["n"]) + " ".join("%8.2f" % R[p][k] for k in keys))
    for k in keys + ["person", "redate", "dc_compete", "dc_censor", "final", "own"]:
        print(k, review(R, k))
