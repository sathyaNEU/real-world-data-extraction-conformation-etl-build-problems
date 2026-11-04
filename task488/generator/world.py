"""The days' schedules: hydrant uplifts, the low point drain round, idle-pit flushes and every check sample;
refueller uplifts, rack loads, couplings and the one transfer; and the refuellers' tanks."""
from collections import deque
from fractions import Fraction
import sim
from sim import H, M, DAY, T0, T1, T_RACK, T_SUSP, T_OPEN, Uplift, dur_for, STAND_PIT, AGENT_OF

RACK_HEADER = sim.line_fill(86, 250)     # the rack pump's header from the farm valves to the loading arms

PIER_AIRLINES = {
    "A": ["Orvelle Airways", "Orvelle Airways", "Brightwing Airlines", "Brightwing Airlines", "Tallowmere Air"],
    "B": ["Northcove Air", "Northcove Air", "Sablewood Air", "Orvelle Airways"],
    "C": ["Tamarind Air", "Vireo Airlines", "Vireo Airlines", "Halyard Air", "Orvelle Airways"],
}
DISPENSERS = {"Corbel": ["HD-0%d" % k for k in range(1, 9)], "Northgarth": ["ND-%d" % k for k in range(1, 6)]}
STAND_CLOSED = {"27": 15 * H, "28": 15 * H}   # Pier B's far stands closed for apron resurfacing, Tue 15:00
SHIFT_STARTS = [-DAY + 5 * H, -DAY + 17 * H, 5 * H, 17 * H, DAY + 4 * H]
IDLE = 12 * H                                 # a pit idle this long is flushed and sampled before it is used
LPD_ROUND = [("A", -DAY + 9 * H + 12 * M), ("B", -DAY + 9 * H + 31 * M), ("C", -DAY + 9 * H + 55 * M),
             ("E", -DAY + 10 * H + 26 * M), ("F", -DAY + 10 * H + 49 * M), ("G", -DAY + 11 * H + 8 * M)]
PC_PIT = "P-A01"                              # where the Operator samples after a line-up change


def fuel_temp(r, t):
    """Fuel temperature at the dispenser in tenths of a degree: the buried hydrant runs near 13 C in October,
    a little warmer through the afternoon."""
    hour = (t // H) % 24
    warm = 6 if 12 <= hour <= 18 else (3 if 9 <= hour <= 20 else 0)
    return 128 + warm + r.between(0, 12)


def odd_litres(r, v):
    """A dispenser stops a few litres either side of the fuel order: litres are never round."""
    x = v + r.between(-46, 46)
    if x % 10 == 0:
        x += r.choice([-3, 3, 7, -7])
    return x


def hydrant_schedule(rng, fleet):
    r = rng.fork("hydrant")
    ups = []

    def add(stand, start, gross, lpm, airline, reg, flight, maint=False):
        ups.append(Uplift(uid=None, pit=STAND_PIT[stand], stand=stand, start=start, dur=dur_for(gross, lpm),
                          gross=gross, airline=airline, flight=flight, reg=reg, agent=AGENT_OF[airline], equip=None,
                          temp10=fuel_temp(r, start), kind="hydrant", maint=maint))

    def pier(sec, stands, n_lo, n_hi, first, last, v_lo, v_hi, lpm, cls):
        for stand in stands:
            closed = STAND_CLOSED.get(stand)
            for day in (-1, 0):
                base = day * DAY
                n = r.between(n_lo, n_hi)
                gap = (last - first) // n // M * M
                phase = r.between(0, gap // M) * M      # each stand's turns run on its own offset through the day
                prev_end = base
                for k in range(n):
                    slot = base + first + phase + k * gap
                    t = slot + r.between(-20, 20) * M
                    t = max(t, prev_end + 50 * M, base + first)
                    if t > base + last + 30 * M:
                        break
                    airline, reg = fleet.pick(r, PIER_AIRLINES[sec], cls)
                    gross = odd_litres(r, r.between(v_lo, v_hi))
                    if closed is not None and day == 0 and t + dur_for(gross, lpm) > closed:
                        break
                    add(stand, t, gross, lpm, airline, reg, fleet.flight(r, airline))
                    prev_end = t + dur_for(gross, lpm)
            if closed is not None:
                continue
            if r.chance(3, 5):      # the first wave on Wednesday, before the suspension
                t = DAY + 4 * H + 25 * M + r.between(0, 35) * M
                airline, reg = fleet.pick(r, PIER_AIRLINES[sec], cls)
                gross = odd_litres(r, r.between(v_lo, v_hi))
                if t + dur_for(gross, lpm) < T_SUSP - 3 * M:
                    add(stand, t, gross, lpm, airline, reg, fleet.flight(r, airline))

    pier("A", ["11", "12", "13", "14", "15", "16", "17", "18", "19"], 5, 7, 5 * H + 35 * M, 22 * H + 20 * M,
         4600, 13600, 1100, "nb")
    pier("B", ["21", "22", "23", "24", "25", "26", "27", "28"], 4, 6, 5 * H + 45 * M, 22 * H + 50 * M,
         11200, 24400, 1350, "nb")
    pier("C", ["31", "32", "33", "34", "35", "36"], 2, 3, 6 * H + 50 * M, 21 * H + 40 * M,
         42000, 108000, 2800, "wb")

    def jit(minutes):
        return r.between(-minutes, minutes) * M

    cargo = ["Ironbark Air Cargo", "Ironbark Air Cargo", "Calverin Cargo"]
    remote = ["Brightwing Airlines", "Tallowmere Air", "Sablewood Air", "Orvelle Airways"]
    maint = ["Orvelle Airways", "Brightwing Airlines"]

    def low(stand, start, gross, lpm, pool, cls, maint_run=False):
        gross = odd_litres(r, gross)
        airline, reg = fleet.pick(r, pool, cls)
        flight = "MX" if maint_run else fleet.flight(r, airline)
        add(stand, start, gross, lpm, airline, reg, flight, maint_run)

    # Monday: the low-use sections' ordinary traffic
    low("52", -DAY + 2 * H + 10 * M + jit(10), 61000, 2600, cargo, "wb")
    low("53", -DAY + 14 * H + jit(10), 24500, 1500, cargo, "nb")
    low("51", -DAY + 23 * H + 20 * M + jit(10), 58000, 2600, cargo, "wb")
    low("62", -DAY + 9 * H + jit(15), 11800, 1100, remote, "nb")
    low("64", -DAY + 17 * H + 30 * M + jit(15), 13400, 1100, remote, "nb")
    low("M1", -DAY + 13 * H + 15 * M + jit(15), 3600, 600, maint, "nb", True)
    # Tuesday and the small hours of Wednesday
    low("53", 3 * H + 40 * M + jit(8), 23800, 1500, cargo, "nb")
    low("52", 13 * H + 55 * M + jit(8), 64000, 2600, cargo, "wb")
    low("54", 16 * H + 20 * M + jit(6), 31500, 1500, cargo, "nb")
    low("51", 23 * H + 35 * M + jit(8), 26400, 1500, cargo, "nb")
    low("51", DAY + 2 * H + 40 * M + jit(8), 47500, 2600, cargo, "wb")
    low("62", 7 * H + 20 * M + jit(10), 9600, 1100, remote, "nb")
    low("64", 13 * H + 25 * M + jit(10), 12375, 1100, remote, "nb")
    low("61", 16 * H + 5 * M + jit(5), 8200, 1100, remote, "nb")
    low("63", 19 * H + 30 * M + jit(10), 11200, 1100, remote, "nb")
    low("61", 21 * H + 45 * M + jit(10), 9800, 1100, remote, "nb")

    ups.sort(key=lambda u: (u.start, u.pit))
    # dispensers: each agent's first free unit, in a fixed order of preference
    free = {d: T_OPEN for ag in DISPENSERS for d in DISPENSERS[ag]}
    for u in ups:
        units = DISPENSERS[u.agent]
        avail = [d for d in units if free[d] <= u.start - 20 * M]
        d = avail[0] if avail else min(units, key=lambda x: free[x])
        u.equip = d
        free[d] = u.end + 6 * M
    return ups


def last_use_sunday(rng):
    """When each pit last drew on Sunday 11 October, before the exports open (piers late in the evening, the
    low-use sections hours or days earlier); it decides only which Monday uplifts the idle-pit rule catches."""
    r = rng.fork("sunday")
    out = {}
    for pit, stand in sorted(sim.PIT_STAND.items()):
        sec = sim.PIT_SECTION[pit]
        if sec in ("A", "B", "C"):
            out[pit] = -DAY - 2 * H - r.between(0, 90) * M
        else:
            out[pit] = -DAY - r.between(16, 40) * H
    return out


def drains_and_checks(ups, rng):
    """The Monday low point drain round, the idle-pit flushes before uplifts and each dispenser's shift-start
    check. Returns the drain draws (kind 'drain') and the check samples; a sample's label is read off the
    simulation at its time."""
    r = rng.fork("checks")
    drains, checks = [], []
    for sec, t in LPD_ROUND:
        litres = r.between(34, 47)
        d = Uplift(uid=None, pit=sim.LPD[sec], stand=None, start=t, dur=3 * M, gross=litres, airline=None,
                   flight=None, reg=None, agent="Pellacre", equip="LPD", temp10=fuel_temp(r, t), kind="drain")
        drains.append(d)
        checks.append({"who": "Pellacre", "kind": "lpd", "pit": d.pit, "time": d.end + M, "drain": d,
                       "section": sec, "litres": litres})
    last = last_use_sunday(rng)
    hyd = sorted([u for u in ups if u.kind == "hydrant"], key=lambda u: (u.start, u.pit))
    flushed = set()
    for u in hyd:
        prev = last[u.pit]
        if u.start - prev >= IDLE:
            litres = r.between(36, 44)
            fs = u.start - r.between(12, 16) * M
            d = Uplift(uid=None, pit=u.pit, stand=u.stand, start=fs, dur=4 * M, gross=litres, airline=None,
                       flight=None, reg=None, agent=u.agent, equip=u.equip, temp10=u.temp10, kind="drain")
            drains.append(d)
            checks.append({"who": u.agent, "kind": "idle", "pit": u.pit, "time": d.end + M, "drain": d,
                           "disp": u.equip, "up": u, "idle_h": (u.start - prev) // H, "litres": litres})
            flushed.add(id(u))
        last[u.pit] = u.end
    for agent, units in DISPENSERS.items():
        for disp in units:
            mine = [u for u in hyd if u.equip == disp]
            for ss in SHIFT_STARTS:
                nxt = [u for u in mine if ss + 10 * M <= u.start < ss + 4 * H]
                if not nxt or id(nxt[0]) in flushed:
                    continue
                u = nxt[0]
                checks.append({"who": agent, "kind": "shift", "pit": u.pit, "time": u.start - r.between(5, 11) * M,
                               "disp": disp, "up": u, "litres": 0})
    checks.sort(key=lambda c: (c["time"], c["pit"]))
    return drains, checks


def product_change_checks(ups, drains):
    """After each line-up change the Operator samples at P-A05 once one hydrant line fill has passed the pump
    station's meter since the change."""
    import routes
    out = []
    for t_change, k in ((T0, 13), (T1, 17)):
        t = routes.when_pumped(ups + drains, t_change, sim.TOTAL_FILL)
        out.append({"who": "Pellacre", "kind": "product_change", "pit": PC_PIT, "time": (t // M + k) * M,
                    "change": t_change, "metered_at": t})
    return out


# ---------------------------------------------------------------- refuellers
TANKS = {   # tank id: (agent, capacity litres, plate)
    "RF-21": ("Corbel", 22700, "WFL 4821"),
    "RF-22": ("Corbel", 22700, "WFL 4822"),
    "RF-23": ("Corbel", 22700, "WFL 5307"),
    "RF-24": ("Corbel", 15100, "WFL 3916"),
    "T-31": ("Northgarth", 37800, "TRL 7731"),
    "T-32": ("Northgarth", 37800, "TRL 7732"),
    "T-35": ("Northgarth", 37800, "TRL 8135"),
    "N-12": ("Northgarth", 11400, "NGA 1202"),
}
RIGID = {"RF-21", "RF-22", "RF-23", "RF-24", "N-12"}      # a rigid refueller's ticket names its own tank
TRACTORS = {"N-7": "NGA 0707", "N-8": "NGA 0708"}
REGISTER_PAIRING = {"N-7": "T-31", "N-8": "T-32"}         # the fleet list as last updated, 5 October
COUPLINGS = [   # (local second, tractor, trailer coupled); a tractor pulls its trailer until its next coupling
    (-DAY + 4 * H + 50 * M, "N-7", "T-31"),
    (-DAY + 4 * H + 55 * M, "N-8", "T-32"),
    (11 * H + 58 * M, "N-7", "T-35"),
]
T31_OFF = 11 * H + 52 * M      # T-31 uncoupled at the workshop (an axle bearing running hot)
RF23_OFF = 13 * H + 6 * M      # RF-23 into the workshop (hose reel bearing) after pumping most of its load to RF-24
TRUCK_STANDS = ["71", "72", "73", "74", "75", "76"]
TRUCK_AIRLINES = {"Corbel": ["Orvelle Airways", "Brightwing Airlines", "Tallowmere Air"],
                  "Northgarth": ["Northcove Air", "Sablewood Air", "Vireo Airlines"]}


def trailer_of(tractor, t, couplings=COUPLINGS):
    cur = None
    for when, trac, trl in couplings:
        if trac == tractor and when <= t:
            cur = trl
    return cur


def tank_of(veh, t, couplings=COUPLINGS):
    return veh if veh in RIGID else trailer_of(veh, t, couplings)


def refueller_schedule(rng, fleet, tag="refuellers"):
    """Refueller uplifts on the north apron and the rack loads that keep the tanks topped up, from Tuesday's
    05:00 handover to the Wednesday suspension, worked to a plan with jittered times and litres.

    Corbel's RF-23 loads first after the 06:00 line-up, works two turns and at 12:52 pumps most of what it holds
    into RF-24 before going to the workshop; Northgarth's N-7 runs T-31 down, loads it on the batch at 07:36,
    leaves it at the workshop at 11:52 and couples the spare trailer T-35, which loads first after the rack moves
    to Tank 1. Every other load is outside the batch's time at the rack."""
    r = rng.fork(tag)
    opening = {"RF-21": odd_litres(r, 9400), "RF-22": odd_litres(r, 15800), "RF-23": odd_litres(r, 6100),
               "RF-24": odd_litres(r, 11900), "T-31": odd_litres(r, 21600), "T-32": odd_litres(r, 12900),
               "T-35": odd_litres(r, 7200), "N-12": odd_litres(r, 4300)}
    contents = dict(opening)
    ups, loads, transfers = [], [], []
    rot = {"Corbel": 0, "Northgarth": 0}
    busy = {}
    reserve = {}      # RF-24 runs no lower than the transferred litres above its usual top-up point

    def airline_for(agent, given=None):
        if given:
            return given
        pool = TRUCK_AIRLINES[agent]
        a = pool[rot[agent] % len(pool)]
        rot[agent] += 1 + r.below(2)
        return a

    def do_load(veh, t, frac_lo=90, frac_hi=95):
        tank = tank_of(veh, t)
        cap = TANKS[tank][1]
        vol = odd_litres(r, cap * r.between(frac_lo, frac_hi) // 100 - contents[tank])
        loads.append({"tank": tank, "veh": veh, "start": t, "dur": dur_for(vol, 2200), "net": vol})
        contents[tank] += vol
        assert contents[tank] <= cap, (tank, contents[tank])
        busy[veh] = t + dur_for(vol, 2200)
        return t + dur_for(vol, 2200)

    def do_uplift(veh, agent, t, litres, airline=None, auto=True):
        """An uplift; a vehicle short of fuel for it first tops up at the rack, never while the batch is there."""
        tank = tank_of(veh, t)
        t = max(t, busy.get(veh, 0) + 8 * M)
        if contents[tank] < litres + 900 + reserve.get(tank, 0) and auto:
            lt = max(t - 40 * M, busy.get(veh, 0) + 6 * M)
            assert not (T0 - 15 * M <= lt <= T_RACK + 30 * M), (veh, lt)
            t = max(t, do_load(veh, lt) + r.between(10, 18) * M)
        if t + dur_for(litres, 750) > T_SUSP - 2 * M:
            return None
        airline = airline_for(agent, airline)
        airline, reg = fleet.pick(r, [airline], "nb")
        assert contents[tank] >= litres + 600, (veh, tank, t, contents[tank], litres)
        u = Uplift(uid=None, pit=None, stand=r.choice(TRUCK_STANDS), start=t, dur=dur_for(litres, 750),
                   gross=litres, airline=airline, flight=fleet.flight(r, airline), reg=reg, agent=agent, equip=veh,
                   temp10=fuel_temp(r, t) + r.between(-10, 20), kind="refueller")
        contents[tank] -= litres
        ups.append(u)
        busy[veh] = u.end
        return u.end

    def j(minutes):
        return r.between(0, minutes) * M

    C, N = "Corbel", "Northgarth"
    # Corbel RF-21 and RF-22: early loads on Tank 2's fuel, afternoon and night loads on Tank 1's
    do_load("RF-21", 5 * H + 14 * M + j(6))
    for t, v in ((6 * H + 5 * M, 4200), (7 * H + 40 * M, 3900), (9 * H + 35 * M, 5100), (11 * H + 20 * M, 4400)):
        do_uplift("RF-21", C, t + j(12), odd_litres(r, v))
    do_load("RF-21", 12 * H + 48 * M + j(6))
    for t, v in ((13 * H + 30 * M, 3300), (15 * H + 40 * M, 4700), (17 * H + 50 * M, 3600), (19 * H + 45 * M, 5200), (22 * H + 10 * M, 4100),
                 (DAY + 4 * H + 30 * M, 3800)):
        do_uplift("RF-21", C, t + j(12), odd_litres(r, v))
    for t, v in ((5 * H + 50 * M, 5600), (8 * H + 15 * M, 4300), (10 * H + 30 * M, 3700)):
        do_uplift("RF-22", C, t + j(12), odd_litres(r, v))
    do_load("RF-22", 13 * H + 5 * M + j(10))
    for t, v in ((14 * H + 20 * M, 4600), (16 * H + 35 * M, 3900), (18 * H + 55 * M, 5300), (21 * H + 5 * M, 4200),
                 (23 * H + 40 * M, 3500)):
        do_uplift("RF-22", C, t + j(12), odd_litres(r, v))
    # RF-23: the first load after the line-up, two turns, the transfer to RF-24, the workshop
    do_load("RF-23", 7 * H + 2 * M + j(6), 93, 95)
    do_uplift("RF-23", C, 8 * H + 50 * M + j(10), odd_litres(r, 6300))
    do_uplift("RF-23", C, 11 * H + 15 * M + j(10), odd_litres(r, 4900))
    for t, v in ((6 * H + 30 * M, 2900), (9 * H + 50 * M, 2400)):      # RF-24's light morning
        do_uplift("RF-24", C, t + j(12), odd_litres(r, v))
    xs = 12 * H + 50 * M + j(4)
    xfer = odd_litres(r, 3800)
    transfers.append({"from": "RF-23", "to": "RF-24", "start": xs, "dur": dur_for(xfer, 900), "litres": xfer})
    contents["RF-23"] -= xfer
    contents["RF-24"] += xfer
    reserve["RF-24"] = xfer + 700
    # RF-24: then the transferred fuel to each of Corbel's three north-apron airlines
    for t, v, a in ((13 * H + 25 * M, 3400, "Brightwing Airlines"), (14 * H + 40 * M, 2900, "Tallowmere Air")):
        do_uplift("RF-24", C, t + j(8), odd_litres(r, v), a)
    do_load("RF-24", 15 * H + 30 * M + j(8))
    for t, v, a in ((16 * H + 30 * M, 3100, "Orvelle Airways"), (19 * H + 10 * M, 3600, None),
                    (22 * H + 40 * M, 2800, None), (DAY + 4 * H + 20 * M, 3300, "Tallowmere Air")):
        do_uplift("RF-24", C, t + j(10), odd_litres(r, v), a)
    # Northgarth N-7: T-31 run down on Tank 2's fuel, loaded on the batch, two turns, the workshop; then T-35
    do_uplift("N-7", N, 5 * H + 38 * M + j(6), odd_litres(r, 8100))
    do_uplift("N-7", N, 6 * H + 40 * M + j(6), odd_litres(r, 9400))
    do_load("N-7", 7 * H + 36 * M + j(6), 93, 95)
    do_uplift("N-7", N, 8 * H + 25 * M + j(10), odd_litres(r, 11200))
    do_uplift("N-7", N, 10 * H + 10 * M + j(10), odd_litres(r, 7700))
    do_load("N-7", 12 * H + 24 * M + j(4), 89, 91)
    for t, v, a in ((13 * H + 20 * M, 6800, "Northcove Air"), (16 * H + 45 * M, 5900, "Sablewood Air"),
                    (21 * H + 40 * M, 2700, "Vireo Airlines")):
        do_uplift("N-7", N, t + j(10), odd_litres(r, v), a)
    # N-8 on T-32 and the rigid N-12, loaded before the line-up and after the rack's change
    do_load("N-8", 5 * H + 26 * M + j(4), 90, 93)
    for t, v in ((6 * H + 15 * M, 9300), (8 * H + 5 * M, 7800), (10 * H + 45 * M, 8800), (13 * H + 50 * M, 6900)):
        do_uplift("N-8", N, t + j(12), odd_litres(r, v))
    do_load("N-8", 15 * H + 55 * M + j(8))
    for t, v in ((17 * H + 15 * M, 8400), (19 * H + 35 * M, 7600), (22 * H + 20 * M, 9100), (DAY + 4 * H + 40 * M, 6200)):
        do_uplift("N-8", N, t + j(12), odd_litres(r, v))
    do_load("N-12", 5 * H + 5 * M + j(4), 88, 92)
    for t, v in ((5 * H + 55 * M, 3000), (9 * H + 20 * M, 2600), (13 * H + 10 * M, 3100)):
        do_uplift("N-12", N, t + j(12), odd_litres(r, v))
    do_load("N-12", 16 * H + 10 * M + j(8))
    for t, v in ((17 * H + 40 * M, 3400), (20 * H + 25 * M, 2800), (DAY + 0 * H + 50 * M, 3300)):
        do_uplift("N-12", N, t + j(12), odd_litres(r, v))
    ups.sort(key=lambda u: (u.start, u.equip))
    loads.sort(key=lambda ld: ld["start"])
    return ups, loads, transfers, opening


MONDAY_DIP = -DAY + 5 * H      # the weekly refueller stock dip, Mondays at the 05:00 handover


def monday_refuellers(rng, fleet, opening):
    """Monday's refueller day on Tank 2's fuel, from the weekly 05:00 dip to Tuesday's 05:00 state, built backward so
    the dip, Monday's loads and Monday's uplifts reconcile exactly to what each tank held at Tuesday 05:00. Each
    vehicle works a turn or two, tops up at the rack once around midday and works the afternoon and evening; T-35
    stood spare all Monday. Returns the uplifts, the loads and the dips."""
    r = rng.fork("monday-refuellers")
    agent = {"RF-21": "Corbel", "RF-22": "Corbel", "RF-23": "Corbel", "RF-24": "Corbel", "N-7": "Northgarth",
             "N-8": "Northgarth", "N-12": "Northgarth"}
    size = {"Corbel": (2600, 5400), "Northgarth": (6200, 10400)}
    ups, loads, dips = [], [], {"T-35": opening["T-35"]}
    for k, veh in enumerate(["RF-21", "RF-22", "RF-23", "RF-24", "N-7", "N-8", "N-12"]):
        tank = tank_of(veh, -DAY + 6 * H)
        cap = TANKS[tank][1]
        lo, hi = size[agent[veh]] if veh != "N-12" else (2500, 3600)
        t_load = -DAY + 10 * H + 20 * M + k * 37 * M + r.between(0, 20) * M
        target = cap * r.between(86, 95) // 100 - opening[tank]      # drawn off between Monday's load and Tuesday
        after, left = [], target
        while left > hi + lo:
            v = odd_litres(r, r.between(lo, hi))
            after.append(v)
            left -= v
        if left > 0:
            after.append(left)
        before = [odd_litres(r, r.between(lo, hi)) for _ in range(1 + r.below(2))]
        x = odd_litres(r, sum(before) + 1400 + r.between(300, 3000))   # the Monday 05:00 dip
        level = opening[tank] + sum(after)
        vol = level - (x - sum(before))
        assert 0 < x <= cap and 1500 < vol and level <= cap, (veh, x, vol, level)
        dips[tank] = x
        times = []
        t = -DAY + 5 * H + 40 * M + r.between(0, 30) * M
        for v in before:
            times.append((t, "up", v))
            t += r.between(70, 140) * M
        assert t < t_load, (veh, t, t_load)
        times.append((t_load, "load", vol))
        span = (-DAY + 23 * H) - (t_load + 50 * M)
        for i, v in enumerate(after):
            times.append((t_load + 50 * M + (span * i // max(1, len(after))) // M * M + r.between(0, 25) * M, "up", v))
        for t, kd, v in times:
            if kd == "up":
                airline = r.choice(TRUCK_AIRLINES[agent[veh]])
                airline, reg = fleet.pick(r, [airline], "nb")
                ups.append(Uplift(uid=None, pit=None, stand=r.choice(TRUCK_STANDS), start=t, dur=dur_for(v, 750),
                                  gross=v, airline=airline, flight=fleet.flight(r, airline), reg=reg,
                                  agent=agent[veh], equip=veh, temp10=fuel_temp(r, t) + r.between(-10, 20),
                                  kind="refueller"))
            else:
                loads.append({"tank": tank, "veh": veh, "start": t, "dur": dur_for(v, 2200), "net": v})
    ups.sort(key=lambda u: (u.start, u.equip))
    loads.sort(key=lambda ld: ld["start"])
    return ups, loads, dips


def simulate_rack_and_tanks(loads, ups, opening, transfers=(), edges=(T0, T_RACK), header=RACK_HEADER,
                            couplings=COUPLINGS, with_transfers=True, mixing=True):
    """The rack header as a FIFO and each refueller tank well mixed, in exact rationals.

    edges: when the rack pump's fuel changes from Tank 2 to Tank 3 and from Tank 3 to Tank 1. Each load's litres
    come off the header's downstream end while the header refills from the tank in service (header=0 reads every
    load as the tank in service at its start). A transfer pumps litres from one tank into another at the first
    tank's mix. couplings: how a ticket's tractor maps to the trailer whose fuel it delivered (the fleet list's
    standing pairing is the shortcut). with_transfers=False leaves the transfer out; mixing=False draws a tank's
    uplifts from its latest load alone. Returns the batch litres each uplift delivered, the batch litres each load
    carried, every tank's (batch, other) litres at the suspension and the least and most each tank held."""
    hdr = deque([["old", header]]) if header else deque()
    events = []
    for i, ld in enumerate(loads):
        events.append((ld["start"], 0, i, "load"))
    if with_transfers:
        for i, x in enumerate(transfers):
            events.append((x["start"], 1, i, "xfer"))
    for u in ups:
        events.append((u.start, 2, u.uid, "up"))
    events.sort()
    tanks = {k: [Fraction(0), Fraction(v)] for k, v in opening.items()}    # [batch, other], exact
    latest = {k: [Fraction(0), Fraction(v)] for k, v in opening.items()}
    load_batch, delivered = {}, {}
    up_by_id = {u.uid: u for u in ups}
    extremes = {k: [v[0] + v[1], v[0] + v[1]] for k, v in tanks.items()}

    def note(key):
        tot = tanks[key][0] + tanks[key][1]
        lo, hi = extremes.setdefault(key, [tot, tot])
        extremes[key] = [min(lo, tot), max(hi, tot)]

    def rack_label(t):
        return "old" if t < edges[0] else ("batch" if t < edges[1] else "new")

    for t, _, ref, kind in events:
        if kind == "load":
            ld = loads[ref]
            need = ld["net"]
            got_b = 0
            if header:
                hdr.append([rack_label(t), need])
                while need > 0:
                    lab, v = hdr[0]
                    take = min(v, need)
                    if lab == "batch":
                        got_b += take
                    if take == v:
                        hdr.popleft()
                    else:
                        hdr[0][1] = v - take
                    need -= take
            else:
                got_b = need if rack_label(t) == "batch" else 0
            load_batch[ref] = got_b
            tk = tanks.setdefault(ld["tank"], [Fraction(0), Fraction(0)])
            tk[0] += got_b
            tk[1] += ld["net"] - got_b
            latest[ld["tank"]] = [Fraction(got_b), Fraction(ld["net"] - got_b)]
            note(ld["tank"])
        elif kind == "xfer":
            x = transfers[ref]
            src = tanks.setdefault(x["from"], [Fraction(0), Fraction(0)])
            dst = tanks.setdefault(x["to"], [Fraction(0), Fraction(0)])
            tot = src[0] + src[1]
            b = Fraction(x["litres"]) * src[0] / tot if tot > 0 else Fraction(0)
            src[0] -= b
            src[1] -= x["litres"] - b
            dst[0] += b
            dst[1] += x["litres"] - b
            note(x["from"])
            note(x["to"])
        else:
            u = up_by_id[ref]
            key = tank_of(u.equip, u.start, couplings)
            tk = tanks.setdefault(key, [Fraction(0), Fraction(0)])
            tot = tk[0] + tk[1]
            if mixing:
                b = Fraction(u.gross) * tk[0] / tot if tot > 0 else Fraction(0)
            else:
                lb, lo = latest.get(key, [Fraction(0), Fraction(1)])
                b = Fraction(u.gross) * lb / (lb + lo) if lb + lo > 0 else Fraction(0)
            b = max(Fraction(0), min(b, tk[0]))
            tk[0] -= b
            tk[1] -= u.gross - b
            delivered[ref] = b
            note(key)
    return delivered, load_batch, {k: tuple(v) for k, v in tanks.items()}, extremes
