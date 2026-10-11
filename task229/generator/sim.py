"""Simulate the fleet, its firmware history, the week's interval reads and the MDM deliveries.

Everything is generated forward from installations, meters and communications events; no figure is
authored. The MDM rows, the head-end history and the register are views of one simulated world.
"""
import datetime as dt
import hashlib

import numpy as np

import world as W


def rng(name):
    h = int(hashlib.sha256(("%d:%s" % (W.SEED, name)).encode()).hexdigest()[:16], 16)
    return np.random.default_rng(h)


def nmi_checksum(nmi):
    """AEMO NMI checksum: double the ASCII value of every second character from the right, sum
    the digits of every value, and take the distance to the next multiple of ten."""
    total, double = 0, True
    for ch in reversed(nmi):
        v = ord(ch) * (2 if double else 1)
        double = not double
        total += sum(int(d) for d in str(v))
    return str((10 - total % 10) % 10)


# ------------------------------------------------------------------ the fleet

class Inst:
    __slots__ = ("nmi", "profile", "group", "build_start", "build_end", "meters", "move", "blocks",
                 "parent", "since", "recover", "evblocks", "wave8", "exchange", "rows", "net_group", "dnsp")

    def __init__(self, nmi, profile, group, b0, b1):
        self.nmi, self.profile, self.group = nmi, profile, group
        self.build_start, self.build_end = b0, b1
        self.meters = []          # [(serial, model, module, installed_local, removed_local)]
        self.move = None          # dict for a Wave 7 move
        self.blocks = []          # [(start_slot, end_slot, cls)] cls 1 precut, 2 post, 3 never
        self.exchange = None
        self.wave8 = None
        self.parent = None        # the collector (EM3) or access point (PX5) the meter reports through
        self.since = None         # when the installation's meter joined that parent (naive local time)
        self.recover = {}         # read-date index -> AEST time the parent's backlog reached the MDM
        self.evblocks = []        # network-event blocks, kept apart from the meter's own
        self.net_group = None


MODEL = {"EM3": ["M1PH-E3A", "M1PH-E3B", "M3PH-E3"], "PX5": ["M1PH-P5", "M3PH-P5", "MCT-P5"]}


def make_fleet():
    r = rng("fleet")
    used_nmi, used_serial = set(), set()

    def new_nmi():
        while True:
            pre = "4103" if r.random() < 0.62 else "4310"
            n = pre + "%06d" % r.integers(0, 10 ** 6)
            if n not in used_nmi:
                used_nmi.add(n)
                return n

    def new_serial(module):
        while True:
            if module == "EM3":
                lead = "0" if r.random() < 0.38 else str(r.integers(1, 3))
            else:
                lead = str(r.integers(6, 8))
            s = lead + "%07d" % r.integers(0, 10 ** 7)
            if s not in used_serial:
                used_serial.add(s)
                return s

    insts = []

    def add(profile, group, b0, b1):
        i = Inst(new_nmi(), profile, group, b0, b1)
        i.dnsp = "Ausgrid" if i.nmi.startswith("4103") else "Endeavour Energy"
        module = W.MODULE[b0]
        model = MODEL[module]
        cls = W.PROFILES[profile][2]
        m = model[2] if cls == "SME" else (model[1] if profile in W.HEAVY else model[0])
        y = int(r.integers(2019, 2026)) if module == "EM3" else int(r.integers(2021, 2026))
        inst_dt = dt.datetime(y, int(r.integers(1, 13)), int(r.integers(1, 28)), int(r.integers(8, 16)),
                              int(r.integers(0, 60)))
        i.meters.append([new_serial(module), m, module, inst_dt, None])
        insts.append(i)
        return i

    for b, mix in W.FULL_WEEK.items():
        for prof in sorted(mix):
            for _ in range(mix[prof]):
                add(prof, "full", b, b)
    for frm, to, mix, night in W.WAVE7:
        for prof in sorted(mix):
            for _ in range(mix[prof]):
                i = add(prof, "w7", frm, to)
                i.move = {"night": night}
    # mid-week meter exchanges on EM3.12.0 and EM3.11.4 installations
    for k in range(W.EXCHANGES):
        b0 = "EM3.12.0" if k % 3 else "EM3.11.4"
        prof = ["R30A", "R30B", "R30C", "R5B"][k % 4]
        i = add(prof, "exch", b0, "EM3.12.2")
        day = 3 + (k % 2)                      # Thursday 8 or Friday 9 October, local business hours
        t = dt.datetime(2026, 10, 5 + day, int(r.integers(9, 15)), int(r.integers(0, 60)), tzinfo=W.AEDT)
        i.exchange = t
        i.meters[0][4] = t.replace(tzinfo=None)
        i.meters.append([new_serial("EM3"), i.meters[0][1], "EM3", (t + dt.timedelta(minutes=int(r.integers(35, 80)))).replace(tzinfo=None), None])
    # the Tuesday movers off EM3.12.0 that failed, rolled back and went again on Wednesday
    tue = [i for i in insts if i.group == "w7" and i.move["night"] == "tue"]
    pick = r.choice(len(tue), W.WAVE7_ROLLBACK_RETRY, replace=False)
    for j in sorted(pick):
        tue[j].move["retry"] = True
    assign_network(insts)
    order = r.permutation(len(insts))
    return [insts[j] for j in order]


# ------------------------------------------------------------------ the two mesh networks

def network_ids():
    """Collector and access point ids, grouped by the wave that takes (or took) their meters."""
    r = rng("network_ids")
    out = {}
    used = set()
    for fam, groups, pre in (("EM3", W.EM_COLLECTORS, "EMC"), ("PX5", W.PX_APS, "PXA")):
        for g in groups:
            ids = []
            while len(ids) < groups[g]:
                x = "%s-%04d" % (pre, r.integers(1000, 10000))
                if x not in used:
                    used.add(x)
                    ids.append(x)
            out[(fam, g)] = ids
    return out


# where each population's installations sit, as group weights (the remainder after any wave takes)
NET_MIX = {
    "EM3.10.9": {"old": 0.75, "new": 0.10, "pilot": 0.05, "w7": 0.05, "w8": 0.05},
    "EM3.12.1": {"old": 1.0},
    "EM3.12.0": {"new": 0.70, "pilot": 0.20, "old": 0.10},
    "EM3.11.4": {"old": 0.85, "pilot": 0.10, "new": 0.05},
    "PX5.3.0": {"other": 0.8, "pilot": 0.2},
    "PX5.2.7": {"other": 0.7, "pilot": 0.15, "w8": 0.15},
}


def assign_network(insts):
    r = rng("network")
    ids = network_ids()
    pool = sorted(insts, key=lambda x: x.nmi)

    def put(i, fam, g, k=None):
        lst = ids[(fam, g)]
        i.parent = lst[k] if k is not None else lst[int(r.integers(0, len(lst)))]
        i.net_group = g

    def mix(i, fam, weights):
        gs = sorted(weights)
        p = np.array([weights[g] for g in gs], float)
        put(i, fam, gs[int(r.choice(len(gs), p=p / p.sum()))])

    # the Wave 8 sources behind the Wave 8 collectors and access points
    w8_full = set()
    for b, n in list(W.WAVE8_EM_FULL.items()) + list(W.WAVE8_PX_FULL.items()):
        full = [i for i in pool if i.group == "full" and i.build_start == b]
        for j in sorted(r.choice(len(full), n, replace=False)):
            w8_full.add(full[j].nmi)
    w7em = [i for i in pool if i.group == "w7" and W.MODULE[i.build_start] == "EM3"]
    w7px = [i for i in pool if i.group == "w7" and W.MODULE[i.build_start] == "PX5"]
    pulled = {w7em[j].nmi for j in r.choice(len(w7em), W.WAVE8_PULLED_FORWARD, replace=False)}
    pulled |= {w7px[j].nmi for j in r.choice(len(w7px), W.WAVE8_PX_PULLED_FORWARD, replace=False)}
    exch = [i for i in pool if i.group == "exch"]
    exch_w8 = {exch[j].nmi for j in r.choice(len(exch), W.WAVE8_EXCHANGED, replace=False)}
    for i in pool:
        fam = W.MODULE[i.build_start]
        if i.group == "w7":
            if i.nmi in pulled:
                put(i, fam, "w8", 0)
            else:
                put(i, fam, "w7")
        elif i.group == "exch":
            put(i, fam, "w8" if i.nmi in exch_w8 else "new")
        elif i.nmi in w8_full:
            put(i, fam, "w8")
        elif i.build_start in ("EM3.12.2", "PX5.3.1"):
            put(i, fam, "pilot")
        else:
            mix(i, fam, NET_MIX[i.build_start])
        # the meter joined its parent when it was commissioned, or when the parent's area was re-homed
        inst_t = i.meters[0][3]
        since = inst_t + dt.timedelta(minutes=int(r.integers(25, 240)))
        if r.random() < 0.08:
            lo = max(inst_t.date(), dt.date(2024, 3, 1))
            span = (dt.date(2026, 6, 30) - lo).days
            if span > 30:
                d0 = lo + dt.timedelta(days=int(r.integers(10, span)))
                since = dt.datetime(d0.year, d0.month, d0.day, int(r.integers(9, 16)), int(r.integers(0, 60)))
        i.since = since


def network_events():
    """The week's collection failures: (parent, read-date index, share caught, AEST time the backlog
    cleared). A collector or access point whose backhaul or power failed overnight delivers its meters'
    day only when it is back, after the delivery cut-off."""
    r = rng("events:%d" % W.NET_SALT)
    ids = network_ids()
    out = []
    for (fam, g), lst in sorted(ids.items()):
        for x in lst:
            for d in range(W.DAYS):
                if r.random() < W.EVENT_P[fam]:
                    share = float(r.uniform(*W.EVENT_SHARE))
                    rd = W.READ_DATES[d]
                    mins = int(r.integers(22, 340))
                    # the backlog clears after the MDM's 06:30 estimation run, between 07:05 and 11:40
                    back = dt.datetime(rd.year, rd.month, rd.day, tzinfo=W.AEST) + dt.timedelta(
                        days=1, hours=6, minutes=65 + (mins - 22) * 275 // 318)
                    out.append((x, d, share, back))
    return out


# ------------------------------------------------------------------ the week's communications

def slot_of(t):
    """5-minute slot index in the assessment week (market time) of an aware datetime."""
    return int((t - W.WEEK_START).total_seconds() // 60 // W.SLOT)


def night_window(r, night):
    """A Wave 7 activation time on the given local night, 23:30 to 03:30 AEDT."""
    d = {"tue": 6, "wed": 7}[night]
    start = dt.datetime(2026, 10, d, 23, 30, tzinfo=W.AEDT)
    return start + dt.timedelta(minutes=int(r.integers(0, 240)), seconds=int(r.integers(0, 60)))


# base communications behaviour and per-build departures from it
BASE = dict(gp=0.03, gdur=(20, 120), op=0.012, odur=(240, 2880))
BUILD_FX = {
    "EM3.10.9": dict(gp=0.15, op=0.07),
    "EM3.11.4": dict(gp=0.028, op=0.011),
    "EM3.12.0": dict(gp=0.074, op=0.029),
    "EM3.12.1": dict(light_extra=(0.17, 50, 115)),
    "EM3.12.2": dict(gp=0.025, op=0.009),
    "PX5.2.7": dict(drop=0.012),
    "PX5.3.0": dict(heavy_extra=(0.31, 40, 120)),
    "PX5.3.1": dict(gp=0.025, op=0.0),
}


def _cls(r, kind):
    u = r.random()
    if kind == "gap":
        return 1 if u < 0.12 else (2 if u < 0.50 else 3)
    if kind == "outage":
        return 2 if u < 0.25 else 3
    return 3


def comms_blocks(r, build, profile):
    p = dict(BASE)
    p.update({k: v for k, v in BUILD_FX.get(build, {}).items() if k in BASE})
    fx = BUILD_FX.get(build, {})
    out = []
    for d in range(W.DAYS):
        if r.random() < p["gp"]:
            s = d * W.SLOTS_PER_DAY + int(r.integers(0, W.SLOTS_PER_DAY))
            dur = int(r.integers(p["gdur"][0], p["gdur"][1])) // W.SLOT + 1
            out.append((s, s + dur, _cls(r, "gap")))
        le = fx.get("light_extra")
        if le and profile not in W.HEAVY and r.random() < le[0]:
            s = d * W.SLOTS_PER_DAY + int(r.integers(0, W.SLOTS_PER_DAY))
            out.append((s, s + int(r.integers(le[1], le[2])) // W.SLOT + 1, 3))
        he = fx.get("heavy_extra")
        if he and profile in W.HEAVY and r.random() < he[0]:
            s = d * W.SLOTS_PER_DAY + int(r.integers(0, W.SLOTS_PER_DAY))
            out.append((s, s + int(r.integers(he[1], he[2])) // W.SLOT + 1, 3))
        if fx.get("drop") and r.random() < fx["drop"]:
            # the overnight LTE-M collection session never opened: nothing for the day reaches the
            # MDM before the morning catch-up pass
            out.append((d * W.SLOTS_PER_DAY, (d + 1) * W.SLOTS_PER_DAY, 2))
    if r.random() < p["op"]:
        s = int(r.integers(0, W.WEEK_SLOTS))
        dur = int(np.exp(r.uniform(np.log(p["odur"][0]), np.log(p["odur"][1])))) // W.SLOT
        out.append((s, s + dur, _cls(r, "outage")))
    return out


def own_blocks(i):
    """The meter's own communications texture for the week (firmware and site), seeded per build salt."""
    salt = W.SALT.get(i.build_end if i.group != "full" else i.build_start, 0)
    r = rng("comms:%s:%d" % (i.nmi, salt))
    ra = rng("act:%s:%d" % (i.nmi, salt))
    blocks = []
    if i.group == "full":
        blocks = comms_blocks(r, i.build_start, i.profile)
    elif i.group == "w7":
        t = night_window(ra, "wed" if i.move.get("retry") else i.move["night"])
        if i.move.get("retry"):
            t_fail = night_window(ra, "tue")
            i.move["failed_at"] = t_fail
            s = slot_of(t_fail)
            blocks.append((s, s + int(ra.integers(2, 4)), 3))
        i.move["at"] = t
        s = slot_of(t)
        pre = comms_blocks(r, i.build_start, i.profile)
        post = comms_blocks(r, i.build_end, i.profile)
        blocks += [b for b in pre if b[0] < s] + [b for b in post if b[0] >= s]
        blocks.append((s, s + int(ra.integers(150, 300)) // W.SLOT + 1, 3))
    else:  # exchange
        s = slot_of(i.exchange)
        pre = comms_blocks(r, i.build_start, i.profile)
        post = comms_blocks(r, "EM3.12.2", i.profile)
        blocks = [b for b in pre if b[0] < s] + [b for b in post if b[0] >= s]
        blocks.append((s, s + int(ra.integers(90, 170)) // W.SLOT + 1, 3))
    return blocks


PILOT_DROP = 5     # the PX5.3.1 pilot installation (by NMI order) whose module dropped off the mesh


def simulate():
    insts = make_fleet()
    for i in insts:
        i.blocks = own_blocks(i)
    # the PX5.3.1 pilot site whose module dropped off the mesh for most of the week
    pilot = sorted([i for i in insts if i.group == "full" and i.build_start == "PX5.3.1"], key=lambda x: x.nmi)
    pilot[PILOT_DROP].blocks.append((int(2.6 * W.SLOTS_PER_DAY), int(4.9 * W.SLOTS_PER_DAY), 3))
    apply_events(insts, network_events())
    return insts


def apply_events(insts, events):
    """Every installation behind a failed parent loses that read date at the cut-off with the event's
    share as its chance (the rest re-routed through a neighbour); its day reaches the MDM when the
    parent's backlog clears."""
    r = rng("affect:%d" % W.NET_SALT)
    by_parent = {}
    for i in sorted(insts, key=lambda x: x.nmi):
        by_parent.setdefault(i.parent, []).append(i)
    for parent, d, share, back in events:
        for i in by_parent.get(parent, []):
            if r.random() < share:
                i.evblocks.append((d * W.SLOTS_PER_DAY, (d + 1) * W.SLOTS_PER_DAY, 2))
                i.recover[d] = back + dt.timedelta(minutes=int(r.integers(4, 75)), seconds=int(r.integers(0, 60)))


def slot_class(inst):
    m = np.zeros(W.WEEK_SLOTS, dtype=np.int8)
    for s, e, c in list(inst.blocks) + list(inst.evblocks):
        s, e = max(0, s), min(W.WEEK_SLOTS, e)
        if e > s:
            m[s:e] = np.maximum(m[s:e], c)
    return m


def day_counts(inst):
    """Per market day: (expected, missing precut-recovered, post-recovered, never) per data stream."""
    suff, L, _ = W.PROFILES[inst.profile]
    m = slot_class(inst)
    step = L // W.SLOT
    per = W.SLOTS_PER_DAY // step
    out = []
    for d in range(W.DAYS):
        ends = m[d * W.SLOTS_PER_DAY + step - 1:(d + 1) * W.SLOTS_PER_DAY:step]
        assert len(ends) == per
        out.append((per, int((ends == 1).sum()), int((ends == 2).sum()), int((ends == 3).sum())))
    return out
