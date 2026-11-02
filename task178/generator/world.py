"""The clean truth of task178 architecture 4, before any export is written or any mess applied.

Ermida Aerotécnica's Hangar 3 has run Cotovia's A320-family C-checks since 2023 with one standing crew per aircraft
working today's phase sequence: every work area opens up together, is inspected, repaired, closed up and tested, so
check length follows the work package. Each card's sessions sit in a work area and a shift; each session's chance of
leaving a check-related defect rises with the other sessions worked in its area in the same shift (teams disturbing
each other's work). The 2027 programme carries three schedules from Planning: A (fourteen days, today's sequence), B
(ten days, today's sequence with larger crews) and C (ten days, the same crews sequencing the aircraft area by area).
"""
import datetime as dt
import math
from collections import Counter, defaultdict

import numpy as np

import params as P

AREA_NAMES = [a[0] for a in P.AREAS]
AREA_LEGACY = {a[0]: a[1] for a in P.AREAS}
# Where routine and non-routine work falls, by work area.
AW_ROUTINE = np.array([.08, .07, .07, .13, .13, .12, .12, .08, .12, .08])
AW_NRC = np.array([.07, .14, .14, .06, .06, .10, .10, .06, .07, .20])
AW_ROUTINE = AW_ROUTINE / AW_ROUTINE.sum()
AW_NRC = AW_NRC / AW_NRC.sum()
TRADE_P_ROUTINE = np.array([.30, .15, .20, .12, .15, .08])
TRADE_P_NRC = np.array([.35, .45, .05, .05, .10, .00])
ROUTINE_PHASES = ["OPEN-UP", "INSPECT", "CLOSE-UP", "TEST"]
ROUTINE_PHASE_P = np.array([.32, .33, .23, .12])
# ATA chapters by trade (the chapter a card's task sits under).
ATA_BY_TRADE = {
    "AIRFRAME": [21, 25, 26, 27, 28, 29, 30, 32, 35, 36, 38, 52],
    "STRUCTURES": [51, 53, 54, 55, 57],
    "AVIONICS": [22, 23, 24, 31, 33, 34, 45, 46],
    "POWERPLANT": [49, 70, 71, 72, 73, 75, 77, 78, 80],
    "CABIN": [25, 33, 38, 44],
    "NDT": [51, 53, 54, 55, 57],
}


def streams(seed):
    ss = np.random.SeedSequence(seed)
    names = ["fleet", "tasks", "checks", "packages", "sched", "defects", "plan", "times", "asks", "attend", "mess",
             "distract", "docs"]
    return {n: np.random.default_rng(s) for n, s in zip(names, ss.spawn(len(names)))}


class World:
    pass


def build_fleet(rng):
    fleet = []
    for f in P.FLEET:
        typ = "A321-200" if f in P.A321 else "A320-200"
        built = int(rng.integers(2008, 2020))
        fleet.append({"fleet_no": f, "type": typ, "built": built})
    return fleet


def build_tasks(rng):
    """The maintenance programme's routine C-check tasks: number, ATA chapter, area, trade, phase, standard hours and
    the check packages (C1 to C4) each task falls due in."""
    tasks = []
    used = set()
    n = 1640
    for i in range(n):
        tr = P.TRADES[int(rng.choice(6, p=TRADE_P_ROUTINE))]
        ata = int(rng.choice(ATA_BY_TRADE[tr]))
        area = AREA_NAMES[int(rng.choice(10, p=AW_ROUTINE))]
        ph = ROUTINE_PHASES[int(rng.choice(4, p=ROUTINE_PHASE_P))]
        while True:
            num = "%02d%02d%02d-%02d" % (ata, int(rng.integers(10, 60)), int(rng.integers(1, 40)), int(rng.integers(1, 4)))
            if num not in used:
                used.add(num)
                break
        std = float(np.clip(rng.lognormal(math.log(P.PH_MH[ph]), 0.40), 0.25, 14.0))
        # every task falls due at C2 and C4 packages more often (structural and zonal programmes)
        mask = [bool(rng.random() < p) for p in (0.56, 0.66, 0.56, 0.70)]
        if not any(mask):
            mask[int(rng.integers(0, 4))] = True
        tasks.append({"task_no": num, "ata": ata, "area": area, "trade": tr, "phase": ph, "std_h": round(std, 2),
                      "due": mask})
    return tasks


def _nrc_cards(rng, age, wo_tag):
    n = int(max(140, rng.normal(200 + 24 * age, 40)))
    cards = []
    for k in range(n):
        tr = P.TRADES[int(rng.choice(6, p=TRADE_P_NRC))]
        area = AREA_NAMES[int(rng.choice(10, p=AW_NRC))]
        ata = int(rng.choice(ATA_BY_TRADE[tr]))
        mh = float(np.clip(rng.lognormal(math.log(P.PH_MH["REPAIR"]), 0.40), 0.25, 18.0))
        cards.append({"kind": "NRC", "seq": k + 1, "task_no": "", "ata": ata, "area": area, "trade": tr,
                      "phase": "REPAIR", "mh": round(mh, 2)})
    return cards


def work_package(rng, tasks, check_type, age):
    ci = ["C1", "C2", "C3", "C4"].index(check_type)
    cards = []
    seq = 0
    for t in tasks:
        if t["due"][ci]:
            seq += 1
            mh = float(np.clip(t["std_h"] * rng.lognormal(0.0, 0.22), 0.25, 18.0))
            cards.append({"kind": "RTN", "seq": seq, "task_no": t["task_no"], "ata": t["ata"], "area": t["area"],
                          "trade": t["trade"], "phase": t["phase"], "mh": round(mh, 2)})
    cards += _nrc_cards(rng, age, None)
    return cards


def split_sessions(mh):
    k = max(1, int(math.ceil(mh / P.SESSION_MAX_H - 1e-9)))
    base = round(mh / k, 2)
    parts = [base] * (k - 1) + [round(mh - base * (k - 1), 2)]
    return parts


def level(rng, areas, shifts, ns, cap):
    cnt = Counter(zip(areas, shifts))
    for i in rng.permutation(len(shifts)):
        k = (areas[i], shifts[i])
        if cnt[k] > cap:
            for d in (1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6):
                s2 = shifts[i] + d
                if 0 <= s2 < ns and cnt[(areas[i], s2)] < cap:
                    cnt[k] -= 1
                    shifts[i] = s2
                    cnt[(areas[i], s2)] += 1
                    break
    return shifts


def schedule_phase(rng, cards, ns):
    """Today's sequence: every area runs through the phases together; the card's first session's shift."""
    off = {a: float(rng.uniform(-0.04, 0.04)) for a in AREA_NAMES}
    first = []
    for c in cards:
        a, b = P.PH_WIN[c["phase"]]
        m = min(max((a + b) / 2 + off[c["area"]], a + 1e-3), b - 1e-3)
        u = float(rng.triangular(a, m, b))
        d = int(min(max(u, 0.0), 0.9999) * (ns // 2))
        first.append(2 * d + (0 if rng.random() < 0.5 else 1))
    return first


def schedule_area(rng, cards, ns):
    """Area sequence: a steady team per work area works its own queue in phase order across the whole check."""
    first = [0] * len(cards)
    order_ph = {p: i for i, p in enumerate(P.PHASES)}
    for a in AREA_NAMES:
        idx = [i for i, c in enumerate(cards) if c["area"] == a]
        if not idx:
            continue
        keys = [(order_ph[cards[i]["phase"]], float(rng.random())) for i in idx]
        idx = [i for _, i in sorted(zip(keys, idx))]
        tot = sum(cards[i]["mh"] for i in idx)
        cum = 0.0
        for i in idx:
            pos = (cum + cards[i]["mh"] / 2) / tot * (1 + float(rng.normal(0, 0.05)))
            cum += cards[i]["mh"]
            first[i] = int(min(max(pos, 0.0), 0.9999) * ns)
    return first


def sessions_from(cards, first, ns):
    """Expand each card's first shift into its sessions on consecutive shifts in the same area."""
    out = []
    for ci, (c, s0) in enumerate(zip(cards, first)):
        parts = split_sessions(c["mh"])
        s = min(s0, ns - len(parts)) if len(parts) <= ns else 0
        for j, h in enumerate(parts):
            out.append({"card": ci, "shift_idx": min(s + j, ns - 1), "hours": h})
    return out


def concurrency(sessions, cards):
    cnt = Counter((cards[s["card"]]["area"], s["shift_idx"]) for s in sessions)
    for s in sessions:
        s["n_other"] = cnt[(cards[s["card"]]["area"], s["shift_idx"])] - 1
    return sessions


def session_risk(s, c):
    return P.BASE_RATE * s["hours"] * P.TRADE_FACTOR[c["trade"]] * (1.0 + P.KAPPA * s["n_other"])


def scheduled_check(rng, cards, ns, kind):
    first = schedule_phase(rng, cards, ns) if kind == "phase" else schedule_area(rng, cards, ns)
    areas = [c["area"] for c in cards]
    first = level(rng, areas, first, ns, P.AREA_CAP)
    ses = sessions_from(cards, first, ns)
    return concurrency(ses, cards)


def build(seed=P.SEED):
    R = streams(seed)
    W = World()
    W.fleet = build_fleet(R["fleet"])
    W.tasks = build_tasks(R["tasks"])
    built = {f["fleet_no"]: f["built"] for f in W.fleet}
    # history: 46 checks, about one a month, aircraft in rotation, each on its own package in the C1-C4 cycle
    rng = R["checks"]
    order = list(rng.permutation(P.FLEET))
    pkg_of = {f: int(rng.integers(0, 4)) for f in P.FLEET}
    checks = []
    d = P.HISTORY_START
    i = 0
    while len(checks) < P.N_HISTORY_CHECKS:
        f = int(order[i % len(order)])
        i += 1
        ctype = ["C1", "C2", "C3", "C4"][pkg_of[f] % 4]
        pkg_of[f] += 1
        age = d.year - built[f]
        checks.append({"fleet_no": f, "check": ctype, "age": age, "induction": d})
        d = d + dt.timedelta(days=int(rng.integers(26, 35)))
    W.checks = checks
    # work packages, schedules (fixed crew: length follows the package), sessions and defects
    rp, rs, rd = R["packages"], R["sched"], R["defects"]
    for ch in W.checks:
        cards = work_package(rp, W.tasks, ch["check"], ch["age"])
        mh = sum(c["mh"] for c in cards)
        ns = max(20, int(round(mh / P.CREW_MH_PER_SHIFT / 2)) * 2)
        ses = scheduled_check(rs, cards, ns, "phase")
        for s in ses:
            s["risk"] = session_risk(s, cards[s["card"]])
        risk_card = defaultdict(float)
        for s in ses:
            risk_card[s["card"]] += s["risk"]
        n_def = {ci: int(rd.poisson(r)) for ci, r in sorted(risk_card.items())}
        ch.update({"cards": cards, "sessions": ses, "n_shifts": ns, "days": ns // 2, "mh": round(mh, 2),
                   "defects_true": n_def})
    # the 2027 programme: twelve aircraft with C-checks due, three schedules each
    rq = R["plan"]
    last_pkg = {}
    for ch in W.checks:
        last_pkg[ch["fleet_no"]] = ["C1", "C2", "C3", "C4"].index(ch["check"])
    due = [f for f in sorted(P.FLEET, key=lambda x: (min([c["induction"] for c in W.checks if c["fleet_no"] == x]
                                                           or [dt.date(2099, 1, 1)]), x))][:P.N_2027_CHECKS]
    plan_checks = []
    d27 = dt.date(2027, 1, 11)
    for k, f in enumerate(due):
        ctype = ["C1", "C2", "C3", "C4"][(last_pkg.get(f, 0) + 1) % 4]
        age = 2027 - built[f]
        cards = work_package(rq, W.tasks, ctype, age)
        plans = {}
        for p in ("A", "B", "C"):
            ns = 2 * P.PLAN_DAYS[p]
            plans[p] = scheduled_check(rq, cards, ns, P.PLAN_SEQUENCE[p])
            for s in plans[p]:
                s["risk"] = session_risk(s, cards[s["card"]])
        plan_checks.append({"fleet_no": f, "check": ctype, "age": age, "induction": d27, "cards": cards, "plans": plans})
        d27 = d27 + dt.timedelta(days=int(rq.integers(27, 33)))
    W.plan_checks = plan_checks
    W.R = R
    return W


if __name__ == "__main__":
    W = build()
    tot_def = sum(sum(ch["defects_true"].values()) for ch in W.checks)
    print("history checks %d, defects %d (%.1f a check), days %s" % (
        len(W.checks), tot_def, tot_def / len(W.checks), sorted(Counter(ch["days"] for ch in W.checks).items())))
    for p in ("A", "B", "C"):
        exp = sum(sum(s["risk"] for s in pc["plans"][p]) for pc in W.plan_checks) / len(W.plan_checks)
        print("plan %s expected defects per check (truth) %.2f" % (p, exp))
