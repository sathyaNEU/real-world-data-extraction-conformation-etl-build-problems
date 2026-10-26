"""The routine schedule's own organs, which the release-event call never reads: each battery's pneumatic devices
and their 2026 history, and the wells whose casing gas vents, with their vent tests and producing hours."""
import datetime as dt

import numpy as np

FACTOR = {"continuous high-bleed": 0.62, "continuous low-bleed": 0.04, "intermittent": 0.25,
          "chemical injection pump": 0.45}       # m3 of supply gas an hour (the directive's Table 3)
MODELS = {"continuous high-bleed": [("Fisher", "2500-249"), ("Fisher", "4150K"), ("Kimray", "PC-HB")],
          "continuous low-bleed": [("Fisher", "L2sj"), ("Fisher", "4195KA-LB")],
          "intermittent": [("Norriseal", "1001A"), ("Kimray", "SNAP-ACT"), ("Fisher", "L2e")],
          "chemical injection pump": [("Texsteam", "5100"), ("Williams", "P125"), ("Bruin", "BR5000")]}
SERVICE = {"LC": ["separator level", "treater oil level", "treater water level", "FWKO water level",
                  "test separator level"],
           "PC": ["separator back pressure", "fuel gas pressure", "treater pressure"],
           "CP": ["methanol injection", "corrosion inhibitor", "demulsifier injection"]}


def pick(r, xs):
    return xs[int(r.integers(0, len(xs)))]


def pneumatics(w):
    r = w.arng
    devs = []
    air_now = set(b["code"] for b in w.bats if r.random() < .12)
    converts = {}
    for b in w.bats:
        if b["code"] in air_now and r.random() < .3:
            converts[b["code"]] = dt.date(2026, 4, 1) + dt.timedelta(days=int(r.integers(0, 180)))
    for b in w.bats:
        n_lc = int(r.integers(2, 5)) if b["cls"] != "mwf" else int(r.integers(1, 3))
        n_pc = int(r.integers(1, 3))
        n_cp = int(r.choice([0, 1, 1, 2])) if r.random() < .65 else 0
        kinds = ["LC"] * n_lc + ["PC"] * n_pc + ["CP"] * n_cp
        num = 0
        for k in kinds:
            num += 1
            if k == "CP":
                cls = "chemical injection pump"
            else:
                cls = str(r.choice(["continuous high-bleed", "continuous low-bleed", "intermittent"],
                                   p=[.36, .22, .42] if k == "LC" else [.25, .35, .40]))
            mk, md = pick(r, MODELS[cls])
            d = dict(bat=b["code"], tag="%s-%s-%02d" % ("CIP" if k == "CP" else k, b["code"][3:], num), kind=k,
                     service=pick(r, SERVICE[k]), cls=cls, make=mk, model=md, installed=None, removed=None,
                     retrofit=None, new_cls=None, new_make=None, new_model=None)
            devs.append(d)
    # 2026 changes: high-bleed controllers retrofitted under their own tags, removals with decommissioned vessels,
    # devices added with new vessels
    gas = [d for d in devs if d["bat"] not in air_now or d["bat"] in converts]
    for d in gas:
        if d["cls"] == "continuous high-bleed" and r.random() < .62:
            d["retrofit"] = dt.date(2026, 2, 16) + dt.timedelta(days=int(r.integers(0, 250)))
            d["new_cls"] = "continuous low-bleed" if r.random() < .7 else "intermittent"
            d["new_make"], d["new_model"] = pick(r, MODELS[d["new_cls"]])
    for route in sorted(set(b["area"] for b in w.bats)):
        cand = [d for d in gas if d["retrofit"] is None and w.by[d["bat"]]["area"] == route]
        for i in r.choice(len(cand), size=int(r.integers(2, 5)), replace=False):
            cand[i]["removed"] = dt.date(2026, 1, 20) + dt.timedelta(days=int(r.integers(0, 290)))
    adds = []
    first_on_route = {}
    for b in w.bats:
        first_on_route.setdefault(b["area"], b["code"])
    for b in w.bats:
        if r.random() < .12 or first_on_route[b["area"]] == b["code"]:
            k = "LC" if r.random() < .7 else "CP"
            cls = "chemical injection pump" if k == "CP" else str(r.choice(["continuous low-bleed", "intermittent"]))
            mk, md = pick(r, MODELS[cls])
            num = 1 + max(int(x["tag"].split("-")[-1]) for x in devs if x["bat"] == b["code"])
            adds.append(dict(bat=b["code"], tag="%s-%s-%02d" % ("CIP" if k == "CP" else k, b["code"][3:], num),
                             kind=k, service=pick(r, SERVICE[k]), cls=cls, make=mk, model=md,
                             installed=dt.date(2026, 3, 9) + dt.timedelta(days=int(r.integers(0, 230))),
                             removed=None, retrofit=None, new_cls=None, new_make=None, new_model=None))
    devs += adds
    w.devices = devs
    w.air_now = air_now
    w.air_converts = converts
    w.fuel_ch4 = {b["code"]: round(float(np.clip(r.normal(81.5, 3.2), 72, 90)), 2) for b in w.bats}


def wells(w):
    r = w.arng
    out = []
    used = set()
    for b in w.bats:
        n = {"twice": int(r.integers(5, 7)), "daily": int(r.integers(3, 6)), "mwf": int(r.integers(2, 4))}[b["cls"]]
        twp, rge = int(r.integers(28, 36)), int(r.integers(3, 11))
        for k in range(n):
            lsd, sec = int(r.integers(1, 17)), int(r.integers(1, 37))
            while (lsd, sec, twp, rge) in used:
                lsd, sec = int(r.integers(1, 17)), int(r.integers(1, 37))
            used.add((lsd, sec, twp, rge))
            uwi = "100/%02d-%02d-%03d-%02dW7" % (lsd, sec, twp, rge)
            out.append(dict(bat=b["code"], loc=uwi, seq="00", vented=r.random() < .36, recomp=None, tiein=None,
                            rate=float(r.lognormal(np.log(4.2), .7)), tests=[], hours={}))
    # wells re-completed in 2026 take a new event sequence; a few vented wells tied in during the year
    for route in sorted(set(b["area"] for b in w.bats)):
        cand = [x for x in out if x["vented"] and w.by[x["bat"]]["area"] == route]
        for x in [cand[i] for i in r.choice(len(cand), size=3, replace=False)]:
            x["recomp"] = dt.date(2026, 3, 1) + dt.timedelta(days=int(r.integers(0, 200)))
            x["rate2"] = float(x["rate"] * r.lognormal(0, .35))
    for x in out:
        if x["vented"] and x["recomp"] is None and r.random() < .05:
            x["tiein"] = dt.date(2026, int(r.integers(4, 11)), 1)
    # vent tests: the contractor's measured volume over a timed test; a test before 2026 carries in
    for x in out:
        if not x["vented"]:
            continue
        dates = [dt.date(2025, 9, 1) + dt.timedelta(days=int(r.integers(0, 110)))]
        for lo in (dt.date(2026, 4, 6), dt.date(2026, 9, 14)):
            if r.random() < .8:
                dates.append(lo + dt.timedelta(days=int(r.integers(0, 50))))
        if x["recomp"]:
            dates.append(x["recomp"] + dt.timedelta(days=int(r.integers(10, 40))))
        if x["tiein"]:
            dates = [d for d in dates if d < x["tiein"]]
        for d in sorted(set(dates)):
            after = x["recomp"] is not None and d >= x["recomp"]
            base = x["rate2"] if after else x["rate"]
            q = base * r.lognormal(0, .12)
            mins = int(r.integers(2, 9)) * 60 + int(r.choice([0, 10, 15, 20, 30, 40, 45, 50]))
            vol = q * mins / 60 / 24
            x["tests"].append(dict(date=d, seq="02" if after else "00", minutes=mins, vol=round(float(vol), 3)))
    # producing hours by month and event: wells follow their battery's hours, with their own downtime
    for x in out:
        prod = {p["day"]: p["hours"] for p in w.prod[x["bat"]]}
        own_down = set()
        for _ in range(int(r.poisson(1.5))):
            d0 = dt.date(2026, 1, 1) + dt.timedelta(days=int(r.integers(0, 360)))
            for k in range(int(r.integers(1, 6))):
                own_down.add(d0 + dt.timedelta(days=k))
        for m in range(1, 13):
            for seq in ("00", "02"):
                hrs = 0.0
                d = dt.date(2026, m, 1)
                while d.month == m:
                    live = seq == "00" if x["recomp"] is None or d < x["recomp"] else seq == "02"
                    if live and d not in own_down:
                        hrs += prod.get(d, 24.0)
                    d += dt.timedelta(days=1)
                if hrs > 0:
                    x["hours"][(m, seq)] = round(hrs, 1)
    w.wells = out
    w.casing_ch4 = {b["code"]: round(float(np.clip(r.normal(78.0, 4.0), 66, 88)), 2) for b in w.bats}


# ---------------------------------------------------------------- leak detection and repair
# leak-prone points by equipment: (name, leaks a year while sound, share whose repair needs a shutdown, deferred-size)
POINTS = [("stuffing box", .34, .02, False), ("casing valve", .06, .10, False)]
PLANT = [("Inlet header flange", .07, .45, True), ("Inlet header ESD valve stem", .06, .50, True),
         ("Separator %d dump valve packing", .20, .14, False), ("Separator %d inlet flange", .06, .45, True),
         ("Separator %d PSV seat", .05, .60, True), ("Separator %d sight glass fitting", .10, .05, False),
         ("Fuel gas scrubber drain valve", .08, .10, False), ("Fuel gas line threaded connection", .12, .03, False),
         ("Meter run orifice fitting", .06, .30, True), ("Instrument gas header fitting", .10, .03, False),
         ("Chemical pump skid tubing fitting", .10, .03, False)]
TREATER = [("Treater burner valve", .08, .20, True), ("Treater fuel gas regulator", .10, .05, False),
           ("Treater dump valve packing", .16, .14, False)]
COMBUSTOR = [("Combustor knockout drain valve", .07, .10, False)]
SPRING25 = dt.date(2025, 5, 12)          # the last survey before the file opens; every leak it tagged was repaired


def survey_days(r, start, gap_lo, gap_hi):
    """a crew's working days through the twelve routes, a few days a route, in an order of its own"""
    order = list(r.permutation(12))
    days = {}
    d = start
    for ri in order:
        span = int(r.integers(3, 5))
        n = 0
        while n < span:
            if d.weekday() < 5 and d not in (dt.date(2025, 10, 13), dt.date(2025, 11, 11), dt.date(2026, 5, 18),
                                             dt.date(2026, 9, 7), dt.date(2026, 10, 12), dt.date(2026, 11, 11)):
                days.setdefault(ri, []).append(d)
                n += 1
            d += dt.timedelta(days=1)
        d += dt.timedelta(days=int(r.integers(gap_lo, gap_hi)))
    return days


def workday(d):
    import world as W
    while d.weekday() >= 5 or d in W.HOL:
        d += dt.timedelta(days=1)
    return d


def ldar(w):
    """the licensee's OGI surveys of every battery (autumn 2025, spring and autumn 2026) and every leak they tagged:
    a leak arises on a sound point, the next survey tags it, and it is repaired within weeks, or at the battery's next
    shutdown when the repair needs one; a crew that finds a deferred leak still venting tags it again, and the
    shutdown's work order closes the newest tag"""
    r = w.lrng
    rounds = [survey_days(r, dt.date(2025, 9, 15), 0, 3), survey_days(r, dt.date(2026, 4, 20), 0, 3),
              survey_days(r, dt.date(2026, 9, 14), 0, 3)]
    by_route = {}
    for b in w.bats:
        by_route.setdefault(b["area"], []).append(b)
    surveys = {}
    for k, rd in enumerate(rounds):
        for ri, ds in rd.items():
            bs = by_route[ROUTES_[ri]]
            for i, b in enumerate(bs):
                surveys.setdefault(b["code"], []).append(ds[min(len(ds) - 1, i * len(ds) // len(bs))])
    wells_of = {}
    for x in w.wells:
        wells_of.setdefault(x["bat"], []).append(x["loc"])
    turn = {}
    for b in w.bats:
        turn[b["code"]] = (dt.date(2026, 6, 8) + dt.timedelta(days=int(r.integers(0, 145)))) if r.random() < .45 else None
    # a maintainer repairs a survey's routine leaks at a battery on one visit; a part on order takes a later one
    batch = {(c, d): int(r.integers(2, 23)) for c in sorted(surveys) for d in sorted(surveys[c])}
    leaks = []
    for b in w.bats:
        pts = []
        for u in wells_of.get(b["code"], []):
            lsd = u[4:9]
            for name, lam, dfr, big in POINTS:
                pts.append(("Wellhead %s %s" % (lsd, name), lam, dfr, big))
        nsep = 2 if b["cls"] == "twice" else 1
        for name, lam, dfr, big in PLANT:
            for s in range(1, nsep + 1) if "%d" in name else [None]:
                pts.append((name % s if s else name, lam, dfr, big))
        if b["cls"] != "mwf":
            pts += TREATER
        if b["comb"]:
            pts += COMBUSTOR
        sv = sorted(surveys[b["code"]])
        for name, lam, dfr, big in pts:
            t, again = SPRING25, None
            while True:
                t = again if again is not None else t + dt.timedelta(days=float(r.exponential(365 / lam)))
                again = None
                nxt = [s for s in sv if s > t]
                if not nxt:
                    break
                true = float(np.clip(r.lognormal(np.log(95 if big else 34), .8), 4, 1400))
                deferred = r.random() < dfr
                found = nxt[0]
                if deferred:
                    tn = turn[b["code"]]
                    fix = tn if tn is not None and tn > found else None
                else:
                    lag = batch[(b["code"], found)] if r.random() < .86 else int(r.integers(24, 58))
                    fix = workday(found + dt.timedelta(days=lag))
                seen = [s for s in sv if s >= found and (fix is None or s < fix)]
                leaks.append(dict(bat=b["code"], point=name, arose=t, true=true, deferred=deferred, fix=fix,
                                  seen=seen, rates=[round(float(true * r.lognormal(0, .3))) for _ in seen]))
                if fix is None:
                    break
                t = fix
                # a packing or stuffing box that was only tightened often leaks again within months
                if not deferred and ("packing" in name or "stuffing" in name) and r.random() < REPEAT:
                    again = fix + dt.timedelta(days=float(r.uniform(12, 110)))
    w.ldar = dict(surveys=surveys, turnaround=turn, leaks=leaks)


# ---------------------------------------------------------------- who repaired, and when the system completed it
CONTRACT = .70           # the share of a survey's routine repair visits that go to the mechanical contractor
CONTRACT_OFF = dt.date(2026, 12, 1)      # the contractor's crews left the field at the end of November
SESSION = (30, 75)       # days from the tracker closing a visit's tags to the camera crew's re-check of their points


def approval(d):
    """the day the maintenance system completes a contract work order: the field foreman approves each month's field
    tickets on the 10th of the next month, or the next working day"""
    return workday(dt.date(d.year + (d.month == 12), d.month % 12 + 1, 10))


def contract(w):
    """a survey's routine repairs at a battery are done on one visit, by the field's own maintainer or by the mechanical
    contractor's crew; the shutdowns' repairs are the turnaround contractor's. The tracker closes a visit's tags when its
    work order is completed: the day of the work for the field's own maintainers, the approval for contract work"""
    import world as W
    r = np.random.default_rng(W.SEED + CON_SEED)
    con = {}
    for lk in w.ldar["leaks"]:
        if lk["fix"] is None:
            continue
        k = (lk["bat"], lk["fix"], "shutdown" if lk["deferred"] else "routine")
        if k not in con:
            u = r.random()
            con[k] = lk["deferred"] or (u < CONTRACT and lk["fix"] < CONTRACT_OFF)
    w.ldar["contract"] = con
    w.ldar["closure"] = {k: (approval(k[1]) if c else k[1]) for k, c in con.items()}


def sessions(w):
    """the camera crew re-checks the points of each closed visit of routine repairs on a later trip to the battery, 30 to
    75 days after the tracker closed their tags, unless the battery's next survey comes first; the session screens each
    repaired point and the fittings beside it and tags nothing"""
    import world as W
    r = np.random.default_rng(W.SEED + SES_SEED)
    out = {}
    for k in sorted(w.ldar["contract"]):
        b, fix, kind = k
        g = int(r.integers(SESSION[0], SESSION[1] + 1))
        if kind != "routine":
            continue
        d = workday(w.ldar["closure"][k] + dt.timedelta(days=g))
        sv = sorted(w.ldar["surveys"][b])
        nxt = [s for s in sv if s > fix]
        if d > dt.date(2026, 12, 18) or (nxt and d >= nxt[0] - dt.timedelta(days=7)) or \
                any(abs((s - d).days) <= 7 for s in sv):
            continue
        out.setdefault((b, d), []).append(k)
    w.ldar["sessions"] = out


# ---------------------------------------------------------------- repairs that did not hold
FAIL = dict(stuffing=.45, packing=.30, other=.10)


def recheck(w):
    """some of the field's own maintainers' routine repairs did not hold: the camera crew's re-check found the point
    still leaking and the maintainer repaired it again that day, under a work order of its own; the tracker had already
    closed the tag on the first repair's work order"""
    import world as W
    r = np.random.default_rng(W.SEED + FAIL_SEED)
    leaks = w.ldar["leaks"]
    by_pt = {}
    for i, lk in enumerate(leaks):
        by_pt.setdefault((lk["bat"], lk["point"]), []).append(i)
    day_of = {k: d for (b, d), ks in w.ldar["sessions"].items() for k in ks}
    for i, lk in enumerate(leaks):
        u = r.random()
        if lk["deferred"] or lk["fix"] is None:
            continue
        k = (lk["bat"], lk["fix"], "routine")
        if w.ldar["contract"].get(k) or k not in day_of:
            continue
        pt = lk["point"]
        q = FAIL["stuffing"] if "stuffing" in pt else FAIL["packing"] if ("packing" in pt or "stem" in pt) else \
            FAIL["other"]
        if u >= q:
            continue
        rc = day_of[k]
        ks = by_pt[(lk["bat"], pt)]
        nxt = ks[ks.index(i) + 1] if ks.index(i) + 1 < len(ks) else None
        if rc.year != 2026 or (nxt is not None and leaks[nxt]["arose"] <= rc):
            continue
        lk["closed"], lk["fix"] = lk["fix"], rc


def fugitive_truth(w):
    """each battery's 2026 fugitive methane by half, in tonnes: every leak from the start of the day of its battery's
    last survey before it was first found to the day it was repaired, at the rate the tracker records for that find"""
    out = {}
    halves = (("h1", dt.date(2026, 1, 1), dt.date(2026, 7, 1)), ("h2", dt.date(2026, 7, 1), dt.date(2027, 1, 1)))
    for lk in w.ldar["leaks"]:
        prev = [s for s in sorted(w.ldar["surveys"][lk["bat"]]) if s < lk["seen"][0]]
        a = prev[-1] if prev else dt.date(2026, 1, 1)
        e = lk["fix"] if lk["fix"] is not None else dt.date(2027, 1, 1)
        for h, lo, hi in halves:
            n = max(0, (min(e, hi) - max(a, lo)).days)
            out[(lk["bat"], h)] = out.get((lk["bat"], h), 0.0) + max(1, int(lk["rates"][0])) * 24 * n / 1e6
    return out


# ---------------------------------------------------------------- the runs, redrawn twice
PAIRS_H2 = [("R01", "R06"), ("R02", "R11"), ("R04", "R07"), ("R05", "R12"), ("R08", "R10"), ("R03", "R09")]
PAIRS_27 = [("R01", "R11"), ("R02", "R07"), ("R04", "R12"), ("R05", "R10"), ("R06", "R08"), ("R03", "R09")]


# the batteries each redraw traded, one pair for each pair of runs, at the same place in the two runs' days
SWAPS_H2 = [("BT-0103", "BT-0601"), ("BT-0209", "BT-1105"), ("BT-0402", "BT-0714"), ("BT-0502", "BT-1214"),
            ("BT-0809", "BT-1014"), ("BT-0306", "BT-0904")]
SWAPS_27 = [("BT-0101", "BT-1106"), ("BT-0207", "BT-0706"), ("BT-0407", "BT-1211"), ("BT-0503", "BT-1007"),
            ("BT-0607", "BT-0806"), ("BT-0302", "BT-0911")]


def redraw(w):
    """the field redrew its runs with the check-in app on 1 July 2026 and again for 2027 on 4 January: each redraw
    trades one battery between two runs at the same place in their day, so every lease operator's day keeps its
    shape (the pilot runs R03 and R09 trade only with each other). The register exported on 8 January carries the
    2027 runs."""
    code = {b["code"]: b for b in w.bats}
    run = {c: b["route"] for c, b in code.items()}
    for swaps, pairs in ((SWAPS_H2, PAIRS_H2), (SWAPS_27, PAIRS_27)):
        for (a, c), (ra, rb) in zip(swaps, pairs):
            assert (run[a], run[c]) == (ra, rb) and code[a]["pos"] == code[c]["pos"], (a, c)
            run[a], run[c] = run[c], run[a]
        if swaps is SWAPS_H2:
            after_h2 = dict(run)
    for c, b in code.items():
        b["run_h2"], b["run27"] = after_h2[c], run[c]
    w.redraws = dict(h2=list(SWAPS_H2), y2027=list(SWAPS_27))


ROUTES_ = ["R%02d" % i for i in range(1, 13)]
REPEAT = .22
ASK_SEED = 14
LDAR_SEED = 72
FAIL_SEED = 117
CON_SEED = 136
SES_SEED = 139


def build(w, k=None):
    """the routine schedule's organs draw from their own stream, so nothing in them moves the release events"""
    import world as W
    w.arng = np.random.default_rng(W.SEED + (ASK_SEED if k is None else k))
    pneumatics(w)
    wells(w)
    w.lrng = np.random.default_rng(W.SEED + LDAR_SEED)
    ldar(w)
    contract(w)
    sessions(w)
    recheck(w)
    redraw(w)
