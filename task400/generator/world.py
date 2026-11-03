"""The clean truth for task400: Mount Bracken's haul fleet, shift by shift, from 1 January 2025 to 31 October 2026.

Everything a pack file shows is cut from this state in pack.py; nothing here is written to target/. One RNG stream
per concern, so a parameter change in one concern leaves the others' draws where they were.
"""
import datetime as dt
import numpy as np

SEED = 400
START = dt.date(2025, 1, 1)
END = dt.date(2026, 10, 31)
DAYS = [START + dt.timedelta(days=i) for i in range((END - START).days + 1)]
AWST = dt.timedelta(hours=8)

CIRCUITS = ["SP-ORE", "NP-ORE", "SP-WST", "NP-WST"]
MIX_BEFORE = np.array([0.36, 0.24, 0.26, 0.14])
MIX_AFTER = np.array([0.26, 0.24, 0.16, 0.34])          # North pit stage 3 cutback from 1 June 2026
STAGE3 = dt.date(2026, 6, 1)
LAMBDA_CONFLICT = {"SP-ORE": 0.55, "NP-ORE": 0.62, "SP-WST": 0.45, "NP-WST": 1.30}
NIGHT_FACTOR = 0.90
CONFLICT_LOC = {
    "SP-ORE": (["CRU", "SHR", "SRP"], [0.38, 0.37, 0.25]),
    "NP-ORE": (["CRU", "NHR", "NRP"], [0.30, 0.40, 0.30]),
    "SP-WST": (["SWD", "SHR", "SRP"], [0.45, 0.35, 0.20]),
    "NP-WST": (["NRJ", "NWD", "NHR", "WKR"], [0.48, 0.22, 0.20, 0.10]),
}
NUIS_LOC = (["CRU", "GOL", "SHR", "NHR", "NRJ", "WKR"], [0.30, 0.25, 0.15, 0.15, 0.10, 0.05])
P_ESCALATE = 0.82                    # a real conflict closes into the critical zone
LAMBDA_NUIS_WARN = 2.4               # per truck-shift, unchanged across the window
LAMBDA_NUIS_CRIT = 0.55
P_RESP_CRIT = {"v4": (0.93, 0.80), "v5": (0.36, 0.28)}    # (real, nuisance) by firmware family
P_RESP_WARN = (0.33, 0.22)
P_INC = {"crit_resp": 0.0035, "crit_none": 0.029, "warn_only": 0.0015}
UNTAGGED_PER_MONTH = 1.4
P_COLLISION = 0.16
AVAILABILITY = 0.86
ROLLOUT_START = dt.date(2026, 6, 2)
ROLLOUT_END = dt.date(2026, 6, 23)
INCIDENT_STREAM = "incident-87"   # the incident draw: a representative realisation of the rates above (checks.py R3d)


def rng(name):
    return np.random.default_rng([SEED, sum(ord(c) * (i + 1) for i, c in enumerate(name))])


def build_fleet():
    r = rng("fleet")
    nums = sorted(r.choice(np.arange(401, 466), size=30, replace=False).tolist())
    trucks = ["DT%d" % n for n in nums]
    # CAS units: one per truck at the start, a few hardware swaps later
    serials = set()

    def serial():
        while True:
            s = "PX3-%06d" % r.integers(100000, 999999)
            if s not in serials:
                serials.add(s)
                return s
    units = []   # (serial, truck, installed_date, removed_date or None)
    for t in trucks:
        units.append([serial(), t, dt.date(2023, 1, 1) + dt.timedelta(days=int(r.integers(0, 600))), None])
    # hardware swaps: about six over the window, the replacement carrying whatever firmware is current
    for _ in range(6):
        t = trucks[int(r.integers(0, len(trucks)))]
        d = START + dt.timedelta(days=int(r.integers(30, len(DAYS) - 30)))
        cur = [u for u in units if u[1] == t and u[3] is None][0]
        if d <= cur[2]:
            continue
        cur[3] = d
        units.append([serial(), t, d, None])
    # firmware: every unit on 4.3.11, 4.3.14 from November 2025, 5.0.2 at the truck's service in the rollout window
    upd = {}
    span = (ROLLOUT_END - ROLLOUT_START).days
    order = r.permutation(len(trucks))
    for k, i in enumerate(order):
        frac = (k + r.uniform(-0.4, 0.4)) / (len(trucks) - 1)
        upd[trucks[i]] = ROLLOUT_START + dt.timedelta(days=int(round(min(max(frac, 0), 1) * span)))
    v414 = {t: dt.date(2025, 11, 3) + dt.timedelta(days=int(r.integers(0, 24))) for t in trucks}
    return dict(trucks=trucks, units=units, v5_date=upd, v414_date=v414)


def firmware(fleet, truck, day):
    if day >= fleet["v5_date"][truck]:
        return "5.0.2"
    if day >= fleet["v414_date"][truck]:
        return "4.3.14"
    return "4.3.11"


def unit_on(fleet, truck, day):
    for s, t, a, b in fleet["units"]:
        if t == truck and a <= day and (b is None or day < b):
            return s
    raise KeyError((truck, day))


def build_crews():
    r = rng("crews")
    ops = []
    used = set()
    for crew in "ABCD":
        for _ in range(36):
            while True:
                badge = int(r.integers(10200, 49999))
                if badge not in used:
                    used.add(badge)
                    break
            ops.append(dict(badge=badge, crew=crew, factor=float(np.clip(r.normal(1.0, 0.04), 0.88, 1.08))))
    return ops


def crew_on(day, shift):
    """Four crews on an eight-day cycle: two days, two nights, four off; crew offsets of two days."""
    k = (day - START).days
    for i, crew in enumerate("ABCD"):
        pos = (k + 2 * i) % 8
        if shift == "D" and pos in (0, 1):
            return crew
        if shift == "N" and pos in (2, 3):
            return crew
    raise RuntimeError


def simulate():
    fleet = build_fleet()
    ops = build_crews()
    by_crew = {c: [o for o in ops if o["crew"] == c] for c in "ABCD"}
    r_ts, r_c, r_a, r_s, r_i = rng("truckshift"), rng("conflict"), rng("alarm"), rng("speed"), rng(INCIDENT_STREAM)
    shifts, alarms, incidents = [], [], []
    for day in DAYS:
        mix = MIX_AFTER if day >= STAGE3 else MIX_BEFORE
        for shift in ("D", "N"):
            crew = crew_on(day, shift)
            avail = [t for t in fleet["trucks"] if r_ts.random() < AVAILABILITY]
            pool = list(by_crew[crew])
            r_ts.shuffle(pool)
            for j, t in enumerate(avail):
                op = pool[j % len(pool)]
                circ = CIRCUITS[int(r_ts.choice(4, p=mix))]
                fw = firmware(fleet, t, day)
                fam = "v5" if fw.startswith("5") else "v4"
                start = dt.datetime.combine(day, dt.time(6 if shift == "D" else 18))
                sid = len(shifts)
                hrs = float(np.clip(r_ts.normal(10.6, 0.7), 7.5, 11.6))
                shifts.append(dict(sid=sid, day=day, shift=shift, truck=t, badge=op["badge"], crew=crew,
                                   circuit=circ, firmware=fw, op_hours=hrs, start=start))
                lam = LAMBDA_CONFLICT[circ] * (NIGHT_FACTOR if shift == "N" else 1.0)
                n_conf = r_c.poisson(lam)
                locs, w = CONFLICT_LOC[circ]
                for _ in range(n_conf):
                    loc = locs[int(r_c.choice(len(locs), p=w))]
                    tsec = float(r_c.uniform(300, hrs * 3600))
                    onset = start + dt.timedelta(seconds=tsec)
                    esc = r_c.random() < P_ESCALATE
                    warn_resp = r_a.random() < P_RESP_WARN[0] * op["factor"]
                    alarms.append(dict(sid=sid, real=True, level="WARN", onset_local=onset, loc=loc,
                                       responded=warn_resp, fw=fw))
                    resp = None
                    if esc:
                        pr = P_RESP_CRIT[fam][0] * op["factor"]
                        resp = r_a.random() < pr
                        alarms.append(dict(sid=sid, real=True, level="CRIT",
                                           onset_local=onset + dt.timedelta(seconds=float(r_a.uniform(2.0, 7.0))),
                                           loc=loc, responded=resp, fw=fw))
                    p = P_INC["warn_only"] if not esc else (P_INC["crit_resp"] if resp else P_INC["crit_none"])
                    if r_i.random() < p:
                        incidents.append(dict(sid=sid, loc=loc, kind="tagged",
                                               when_local=onset + dt.timedelta(seconds=float(r_i.uniform(9, 40))),
                                               collision=bool(r_i.random() < P_COLLISION), esc=esc, resp=resp))
                # nuisance alarms (parked or passing tagged vehicles)
                nlocs, nw = NUIS_LOC
                for level, lamn in (("WARN", LAMBDA_NUIS_WARN), ("CRIT", LAMBDA_NUIS_CRIT)):
                    for _ in range(r_a.poisson(lamn)):
                        loc = nlocs[int(r_a.choice(len(nlocs), p=nw))]
                        onset = start + dt.timedelta(seconds=float(r_a.uniform(120, hrs * 3600)))
                        if level == "CRIT":
                            pr = P_RESP_CRIT[fam][1] * op["factor"]
                        else:
                            pr = P_RESP_WARN[1] * op["factor"]
                        alarms.append(dict(sid=sid, real=False, level=level, onset_local=onset, loc=loc,
                                           responded=bool(r_a.random() < pr), fw=fw))
    # incidents with no tagged other party (a visitor's vehicle, an untagged hire vehicle)
    months = sorted({(d.year, d.month) for d in DAYS})
    for (y, m) in months:
        for _ in range(r_i.poisson(UNTAGGED_PER_MONTH)):
            ds = [d for d in DAYS if (d.year, d.month) == (y, m)]
            day = ds[int(r_i.integers(0, len(ds)))]
            cands = [s for s in shifts if s["day"] == day]
            s = cands[int(r_i.integers(0, len(cands)))]
            loc = CONFLICT_LOC[s["circuit"]][0][0]
            incidents.append(dict(sid=s["sid"], loc=loc, kind="untagged",
                                  when_local=s["start"] + dt.timedelta(seconds=float(r_i.uniform(600, 39000))),
                                  collision=bool(r_i.random() < P_COLLISION), esc=None, resp=None))
    return dict(fleet=fleet, ops=ops, shifts=shifts, alarms=alarms, incidents=incidents)


if __name__ == "__main__":
    import collections
    S = simulate()
    print(len(S["shifts"]), "truck-shifts;", len(S["alarms"]), "alarms;", len(S["incidents"]), "incidents")
    sh = S["shifts"]
    inc = S["incidents"]
    def win(d, y):
        return d.year == y and 7 <= d.month <= 10
    for y in (2025, 2026):
        n = sum(1 for i in inc if win(sh[i["sid"]]["day"], y))
        print(y, "Jul-Oct incidents", n)
    c = collections.Counter((sh[i["sid"]]["day"].year, sh[i["sid"]]["day"].month) for i in inc)
    print(sorted(c.items()))
