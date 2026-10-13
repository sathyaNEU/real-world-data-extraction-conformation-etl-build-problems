"""task131 generator: the trial households, their accounts and what happened to them.

1,600 Home Plan households with an interval meter, drawn by the load research team and placed in matched blocks
of four by their 2024-25 summer evening use and rooftop PV, one of each block to each arm. During the trial some
households asked to return to the Home Plan (by phone or online), one per design withdrew a request inside the
cooling-off period, the corporation moved life-support registrations back, households left Murrandi, and after the
last hot workday some moved within the town, a few keeping their design under a new account. Rooftop PV
installations replaced meters part-way through a day; a few meters are configured at 15 minutes."""
from datetime import date, timedelta

import numpy as np

import params as P
import knobs as K
import weather as WX

HOT = set(WX.HOT_WORKDAYS)


def _ids(rng, n, prefix, width, taken):
    out = []
    while len(out) < n:
        x = prefix + "".join(str(v) for v in rng.integers(0, 10, width))
        if x not in taken:
            taken.add(x)
            out.append(x)
    return out


def _pick_dates(rng, n, lo, hi, avoid=(), workdays_only=True):
    pool = [lo + timedelta(i) for i in range((hi - lo).days + 1)]
    pool = [d for d in pool if (P.workday(d) or not workdays_only) and d not in avoid]
    idx = rng.choice(len(pool), size=n, replace=False)
    return sorted(pool[i] for i in idx)


def build():
    rng = np.random.default_rng(P.SEED)
    n = P.N_HH
    hh = {}
    hh["pv0"] = rng.random(n) < 0.38
    extra = int(hh["pv0"].sum()) % 4            # blocks of four share a rooftop PV status
    if extra:
        hh["pv0"][np.where(hh["pv0"])[0][-extra:]] = False
    hh["e2"] = rng.random(n) < 0.33
    hh["size"] = np.exp(rng.normal(0.0, 0.28, n))
    hh["ac"] = np.clip(rng.normal(4.4, 1.0, n), 2.4, 7.8)
    hh["pvkw"] = np.where(hh["pv0"], np.round(rng.choice([3.0, 4.0, 5.0, 6.6, 8.0], n, p=[.12, .2, .28, .3, .1]), 1), 0.0)
    # 2024-25 summer evening use, the blocking variable
    prior = hh["size"] * 0.75 + hh["ac"] * 0.42 + rng.normal(0, K.PRIOR_SD, n) - hh["pv0"] * 0.05
    hh["prior_kw"] = np.round(prior, 3)
    order = np.lexsort((prior, hh["pv0"]))
    arm = np.empty(n, dtype=object)
    block = np.empty(n, dtype=int)
    for b in range(n // 4):
        members = order[4 * b:4 * b + 4]
        perm = rng.permutation(4)
        for j, m in enumerate(members):
            arm[m] = P.ARMS[perm[j]]
            block[m] = b + 1
    hh["arm"] = arm
    hh["block"] = block
    hh["resp"] = (rng.random(n) < K.RESP_SHARE).astype(float)
    hh["w"] = hh["ac"] / hh["ac"].mean()
    hh["mtr15"] = rng.random(n) < 0.0         # trial premises read at 30 minutes; new premises' meters at 15

    taken = set()
    hh["trial_id"] = np.array(["SPT25-%04d" % (i + 1) for i in range(n)])
    hh["account"] = np.array(_ids(rng, n, "71", 8, taken))
    hh["customer"] = np.array(_ids(rng, n, "C0", 6, taken))
    hh["nmi"] = np.array(_ids(rng, n, "8090", 6, taken))
    hh["serial"] = np.array(_ids(rng, n, "2116", 6, taken))

    ev = events(rng, hh, taken)
    return hh, ev


def events(rng, hh, taken):
    """account history events, per household index"""
    n = P.N_HH
    ev = {i: [] for i in range(n)}
    dsg = {a: [i for i in range(n) if hh["arm"][i] == a] for a in P.ARMS}
    used = set()

    def take(pool, k):
        free = [i for i in pool if i not in used]
        out = [free[j] for j in rng.choice(len(free), size=k, replace=False)]
        used.update(out)
        return out

    trial = [P.START + timedelta(i) for i in range((P.END - P.START).days + 1)]
    for a in P.DESIGNS:
        q = K.EVENTS[a]
        # returns at the household's own request
        for i in take(dsg[a], q["return"]):
            d = _pick_dates(rng, 1, date(2025, 12, 3), date(2026, 2, 24), workdays_only=False)[0]
            how = "SELF SERVICE" if rng.random() < 0.27 else "CUSTOMER REQUEST"
            ev[i].append(("return", d, how))
        # a request withdrawn within the cooling-off period
        for i in take(dsg[a], q["withdrawn"]):
            d = _pick_dates(rng, 1, date(2025, 12, 15), date(2026, 1, 30))[0]
            ev[i].append(("withdrawn", d, "CUSTOMER REQUEST"))
        # moved back by the corporation after a life-support registration
        for i in take(dsg[a], q["lifesupport"]):
            d = _pick_dates(rng, 1, date(2025, 12, 8), date(2026, 1, 28))[0]
            ev[i].append(("lifesupport", d, "INELIGIBLE - LIFE SUPPORT"))
        # left Murrandi: at most one before the last hot workday
        early = take(dsg[a], q["leave_early"])
        for i in early:
            d = _pick_dates(rng, 1, date(2025, 12, 5), date(2025, 12, 19))[0]
            ev[i].append(("leave", d, ["MOVE OUT", "FINAL READ - VACATED", "CLOSED"][int(rng.integers(0, 3))]))
        for i in take(dsg[a], q["leave"]):
            d = _pick_dates(rng, 1, P.LAST_HOT + timedelta(2), date(2026, 2, 26), workdays_only=False)[0]
            ev[i].append(("leave", d, ["MOVE OUT", "FINAL READ - VACATED", "CLOSED"][int(rng.integers(0, 3))]))
        # returned at own request, then left Murrandi
        for i in take(dsg[a], q["return_leave"]):
            d1 = _pick_dates(rng, 1, date(2025, 12, 10), date(2026, 1, 30))[0]
            d2 = _pick_dates(rng, 1, P.LAST_HOT + timedelta(2), date(2026, 2, 25), workdays_only=False)[0]
            ev[i].append(("return", d1, "CUSTOMER REQUEST"))
            ev[i].append(("leave", d2, "MOVE OUT"))
        # in-town moves after the last hot workday
        for kind, k in (("move_keep", q["move_keep"]), ("move_home", q["move_home"]), ("return_move", q["return_move"])):
            for i in take(dsg[a], k):
                d = _pick_dates(rng, 1, P.LAST_HOT + timedelta(3), date(2026, 2, 24))[0]
                if kind == "return_move":
                    d0 = _pick_dates(rng, 1, date(2025, 12, 12), date(2026, 1, 29))[0]
                    ev[i].append(("return", d0, "CUSTOMER REQUEST" if rng.random() < 0.6 else "SELF SERVICE"))
                ev[i].append((kind, d, "MOVE OUT"))
    # controls move and leave too
    for i in take(dsg["CTRL"], K.EVENTS["CTRL"]["leave"]):
        d = _pick_dates(rng, 1, P.LAST_HOT + timedelta(2), date(2026, 2, 26), workdays_only=False)[0]
        ev[i].append(("leave", d, ["MOVE OUT", "FINAL READ - VACATED", "CLOSED"][int(rng.integers(0, 3))]))
    for i in take(dsg["CTRL"], K.EVENTS["CTRL"]["leave_early"]):
        d = _pick_dates(rng, 1, date(2025, 12, 5), date(2025, 12, 19))[0]
        ev[i].append(("leave", d, "MOVE OUT"))
    for i in take(dsg["CTRL"], K.EVENTS["CTRL"]["move_home"]):
        d = _pick_dates(rng, 1, P.LAST_HOT + timedelta(3), date(2026, 2, 24))[0]
        ev[i].append(("move_home", d, "MOVE OUT"))
    for i in range(n):
        ev[i].sort(key=lambda e: e[1])
    return ev


def new_premises(rng_seed, hh, ev, taken_ids):
    """account, NMI and meter serial for each in-town move, and the new occupant's account at the old NMI"""
    rng = np.random.default_rng(rng_seed)
    taken = set(taken_ids)
    out = {}
    for i, es in ev.items():
        for kind, d, _ in es:
            if kind in ("move_keep", "move_home", "return_move"):
                acc = _ids(rng, 1, "71", 8, taken)[0]
                nmi = _ids(rng, 1, "8090", 6, taken)[0]
                ser = _ids(rng, 1, "2116", 6, taken)[0]
                out[i] = {"date": d, "kind": kind, "account": acc, "nmi": nmi, "serial": ser}
    occ = {}
    for i, es in ev.items():
        for kind, d, _ in es:
            if kind in ("leave", "move_keep", "move_home", "return_move"):
                occ[i] = {"date": d, "account": _ids(rng, 1, "71", 8, taken)[0],
                          "customer": _ids(rng, 1, "C0", 6, taken)[0]}
    return out, occ


def exchanges(rng_seed, hh, ev):
    """meter exchanges during the data window: rooftop PV installations and a few faults, never on a hot workday or
    the days either side, never after a household has left its premise"""
    rng = np.random.default_rng(rng_seed)
    n = P.N_HH
    gone = {}
    for i, es in ev.items():
        for kind, d, _ in es:
            if kind in ("leave", "move_keep", "move_home", "return_move"):
                gone[i] = d
    avoid = set()
    for d in WX.HOT_WORKDAYS:
        avoid.update({d - timedelta(1), d, d + timedelta(1)})
    pool_pv = [i for i in range(n) if not hh["pv0"][i]]
    out = {}
    picks = rng.choice(pool_pv, size=K.N_PV_INSTALL, replace=False)
    for i in picks:
        hi = min(gone.get(i, P.DATA_TO) - timedelta(3), date(2026, 2, 20))
        d = _pick_dates(rng, 1, date(2025, 11, 4), hi, avoid=avoid)[0]
        out[int(i)] = {"date": d, "why": "PV", "cut": int(rng.integers(19, 33))}
    rest = [i for i in range(n) if i not in out]
    for i in rng.choice(rest, size=K.N_FAULT, replace=False):
        hi = min(gone.get(int(i), P.DATA_TO) - timedelta(3), date(2026, 2, 20))
        d = _pick_dates(rng, 1, date(2025, 11, 4), hi, avoid=avoid)[0]
        out[int(i)] = {"date": d, "why": "FAULT", "cut": int(rng.integers(19, 31))}
    return out
