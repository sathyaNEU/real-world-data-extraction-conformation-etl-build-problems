"""World and physics for task488: Windrell International Airport's fuel farm, hydrant, truck rack and refuellers
from Monday 12 October to the Wednesday 14 October 2026 05:30 suspension.

Integer arithmetic throughout: litres, seconds from Tuesday 13 October 2026 00:00 local time (PDT, UTC-7), and
SplitMix64 streams. The hydrant is always full, so fuel in a segment moves only while a draw point downstream of it
draws; each segment is a FIFO of labelled runs: 'aged' (the August batch J-26-1102 in the dead legs), 'old' (Tank 2,
batch J-26-1171, before the line-up), 'batch' (Tank 3, batch J-26-1187) and 'new' (Tank 1, batch J-26-1179).
"""
from collections import deque

DAY = 86400
H = 3600
M = 60
T0 = 6 * H                       # Tank 3 lined up to the hydrant pumps and the rack, Tue 06:00
T_RACK = 12 * H + 20 * M         # rack pump moved to Tank 1, Tue 12:20
T1 = 15 * H + 40 * M             # hydrant pumps moved to Tank 1, Tue 15:40
T_RECALL = DAY + 5 * H + 12 * M  # the supplier's recall notice, Wed 05:12
T_SUSP = DAY + 5 * H + 30 * M    # hydrant and refueller fuelling suspended, Wed 05:30
T_OPEN = -DAY                    # Mon 12 Oct 00:00, where the agents' exports open
UTC_OFFSET = 7 * H               # PDT: UTC = local + 7 h
LABELS = ("aged", "old", "batch", "new")


def line_fill(length_m, id_mm):
    """Litres held by a pipe: pi/4 * d^2 * L with pi = 355/113, rounded half up (the register's arithmetic)."""
    num = 355 * id_mm * id_mm * length_m
    den = 113 * 4000
    return (2 * num + den) // (2 * den)


# ---------------------------------------------------------------- the register's network
SEGMENTS = [  # (segment, section, from node, to node, length m, internal diameter mm)
    ("HS-01", "FARM", "P", "N0", 185, 387),
    ("HM-01", "MAIN", "N0", "J1", 1430, 333),
    ("HM-02", "MAIN", "J1", "J2", 395, 333),
    ("HM-03", "MAIN", "J2", "J3", 270, 284),
]
PITS = []  # (draw point, node, stand or None, section): hydrant pits and each branch's end-of-line low point drain
SECTIONS = ["FARM", "MAIN", "A", "B", "C", "E", "F", "G"]
BRANCHES = ["A", "B", "C", "E", "F", "G"]
SECTION_NAMES = {"FARM": "Farm header", "MAIN": "Hydrant main", "A": "Pier A", "B": "Pier B",
                 "C": "International apron", "E": "Cargo apron", "F": "Remote stands", "G": "Maintenance base"}
JUNCTION = {}


def _branch(sec, junction, lengths, idmm, dead_len, stands):
    JUNCTION[sec] = junction
    prev = junction
    for k, stand in enumerate(stands, 1):
        node = "%s%d" % (sec, k)
        SEGMENTS.append(("H%s-%02d" % (sec, k - 1), sec, prev, node, lengths[k - 1], idmm))
        PITS.append(("P-%s%02d" % (sec, k), node, stand, sec))
        prev = node
    SEGMENTS.append(("H%s-%02d" % (sec, len(stands)), sec, prev, sec + "X", dead_len, idmm))
    PITS.append(("LPD-%s" % sec, sec + "X", None, sec))


_branch("A", "J1", [112, 61, 58, 64, 60, 59, 63, 62, 57], 254, 22, ["11", "12", "13", "14", "15", "16", "17", "18", "19"])
_branch("B", "J2", [143, 66, 64, 69, 65, 67, 63, 67], 254, 24, ["21", "22", "23", "24", "25", "26", "27", "28"])
_branch("C", "J3", [96, 88, 92, 85, 94, 90], 305, 31, ["31", "32", "33", "34", "35", "36"])
_branch("E", "J2", [1062, 72, 74, 71], 254, 28, ["51", "52", "53", "54"])
_branch("F", "J3", [431, 55, 57, 54, 56], 203, 21, ["61", "62", "63", "64", "65"])
_branch("G", "J1", [366, 43], 152, 16, ["M1", "M2"])

DEAD_LEGS = {s[0] for s in SEGMENTS if s[3].endswith("X")}
PIT_STAND = {p[0]: p[2] for p in PITS if p[2]}
PIT_SECTION = {p[0]: p[3] for p in PITS}
STAND_PIT = {p[2]: p[0] for p in PITS if p[2]}
LPD = {p[3]: p[0] for p in PITS if p[2] is None}


class Network:
    """The topology a simulation runs on: segments as FIFOs, draw points at nodes, the initial labels."""

    def __init__(self, segments, pits, init):
        self.segments = [s[0] for s in segments]
        self.fill = {s[0]: line_fill(s[4], s[5]) if len(s) == 6 else s[4] for s in segments}
        self.seg_section = {s[0]: s[1] for s in segments}
        self.seg_from = {s[0]: s[2] for s in segments}
        self.seg_to = {s[0]: s[3] for s in segments}
        self.seg_into = {s[3]: s[0] for s in segments}
        self.pit_node = {p[0]: p[1] for p in pits}
        self.node_pits = {}
        for p in pits:
            self.node_pits.setdefault(p[1], []).append(p[0])
        self.children = {}
        for s in segments:
            self.children.setdefault(s[2], []).append(s[0])
        self.seg_pits = {s[0]: self._below(s[3]) for s in segments}
        self.topo = []
        self._topo("P")
        self.init = {s: init(s) for s in self.segments}

    def _below(self, node):
        out = list(self.node_pits.get(node, []))
        for seg in self.children.get(node, []):
            out += self._below(self.seg_to[seg])
        return out

    def _topo(self, node):
        for seg in self.children.get(node, []):
            self.topo.append(seg)
            self._topo(self.seg_to[seg])

    def path(self, pit):
        node, out = self.pit_node[pit], []
        while node in self.seg_into:
            seg = self.seg_into[node]
            out.append(seg)
            node = self.seg_from[seg]
        return list(reversed(out))

    def path_fill(self, pit):
        return sum(self.fill[s] for s in self.path(pit))

    def section_fill(self, sec):
        return sum(v for s, v in self.fill.items() if self.seg_section[s] == sec)


def initial_label(seg):
    """What each segment held when the exports open on Monday 12 October: Tank 2's batch J-26-1171 wherever draw
    points have drawn since it was lined up on Thursday 8 October, and the August batch J-26-1102 in the dead legs
    past each branch's last pit, where nothing but the weekly low point drain has moved since the hydrant was refilled
    from Tank 4 after the August pressure test."""
    return "aged" if seg in DEAD_LEGS else "old"


GOLD = Network(SEGMENTS, PITS, initial_label)
FILL = GOLD.fill
SEG_SECTION = GOLD.seg_section
TOTAL_FILL = sum(FILL.values())


def path_fill(pit):
    return GOLD.path_fill(pit)


def section_fill(sec):
    return GOLD.section_fill(sec)


def lumped_network():
    """Each branch section taken as one pipe of its register line fill, every pit of it at its far end; the farm
    header and the main as they are. The section-by-section reckoning of R5."""
    segs = [s for s in SEGMENTS if s[1] in ("FARM", "MAIN")]
    pits = []
    for sec in BRANCHES:
        segs.append(("L-" + sec, sec, JUNCTION[sec], sec + "*", section_fill(sec)))
        pits += [(p[0], sec + "*", p[2], sec) for p in PITS if p[3] == sec]
    return Network(segs, pits, lambda s: "old")


# ---------------------------------------------------------------- airlines, aircraft, agents
AIRLINES = [
    # name, agent, account at the agent, registration style, member of the corporation
    ("Orvelle Airways", "Corbel", "C-1047", "CF", True),
    ("Brightwing Airlines", "Corbel", "C-1062", "CG", True),
    ("Tallowmere Air", "Corbel", "C-1089", "CF", True),
    ("Tamarind Air", "Corbel", "C-1103", "9V", True),
    ("Halyard Air", "Corbel", "C-1125", "CG", False),
    ("Northcove Air", "Northgarth", "NG0213", "N", True),
    ("Sablewood Air", "Northgarth", "NG0236", "N", True),
    ("Vireo Airlines", "Northgarth", "NG0251", "VH", True),
    ("Ironbark Air Cargo", "Northgarth", "NG0278", "CF", True),
    ("Calverin Cargo", "Northgarth", "NG0294", "CG", False),
]
AGENT_OF = {a[0]: a[1] for a in AIRLINES}
ACCOUNT_OF = {a[0]: a[2] for a in AIRLINES}


class Fleet:
    def __init__(self, rng):
        r = rng.fork("fleet")
        self.r = r
        seen = set()
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        def reg(style):
            while True:
                if style in ("CF", "CG"):
                    s = "C-%s%s" % (style[1], "".join(r.choice(letters) for _ in range(3)))
                elif style == "N":
                    s = "N%d%s" % (r.between(201, 989), "".join(r.choice(letters) for _ in range(2)))
                elif style == "9V":
                    s = "9V-S%s" % "".join(r.choice(letters) for _ in range(2))
                else:
                    s = "VH-%s" % "".join(r.choice(letters) for _ in range(3))
                if s not in seen:
                    seen.add(s)
                    return s

        sizes = {"Orvelle Airways": (24, 4), "Brightwing Airlines": (15, 0), "Tallowmere Air": (9, 0),
                 "Tamarind Air": (0, 5), "Halyard Air": (0, 3), "Northcove Air": (11, 0), "Sablewood Air": (9, 0),
                 "Vireo Airlines": (4, 6), "Ironbark Air Cargo": (2, 3), "Calverin Cargo": (2, 1)}
        self.nb, self.wb = {}, {}
        style = {a[0]: a[3] for a in AIRLINES}
        for name, (nnb, nwb) in sizes.items():
            self.nb[name] = [reg(style[name]) for _ in range(nnb)]
            self.wb[name] = [reg(style[name]) for _ in range(nwb)]
        self.flights = {}

    def pick(self, r, airlines, cls):
        airline = r.choice(airlines)
        pool = self.nb[airline] if cls == "nb" else self.wb[airline]
        return airline, r.choice(pool)

    def flight(self, r, airline):
        base = {"Orvelle Airways": 100, "Brightwing Airlines": 300, "Tallowmere Air": 2200, "Tamarind Air": 30,
                "Halyard Air": 600, "Northcove Air": 1400, "Sablewood Air": 820, "Vireo Airlines": 70,
                "Ironbark Air Cargo": 9100, "Calverin Cargo": 450}[airline]
        while True:
            n = base + r.between(1, 899 if base >= 100 else 60)
            key = (airline, n)
            if key not in self.flights:
                self.flights[key] = 1
                return str(n)


# ---------------------------------------------------------------- uplifts
class Uplift:
    __slots__ = ("uid", "pit", "stand", "start", "dur", "gross", "airline", "flight", "reg", "agent", "equip",
                 "temp10", "kind", "maint", "ticket")

    def __init__(self, **kw):
        self.maint = False
        self.ticket = None
        for k, v in kw.items():
            setattr(self, k, v)

    @property
    def end(self):
        return self.start + self.dur

    def cum(self, t):
        """Gross litres delivered by local second t, the floor of a straight line from start to end."""
        if t <= self.start:
            return 0
        if t >= self.end:
            return self.gross
        return self.gross * (t - self.start) // self.dur

    @property
    def net(self):
        return net_litres(self.gross, self.temp10)


def vcf_ptt(temp10):
    """Volume correction to 15 C in parts per ten thousand for a fuel temperature in tenths of a degree: about
    8.3 per ten thousand per degree, the slope of the jet fuel table near 15 C."""
    return (83 * (temp10 - 150) + (50 if temp10 >= 150 else -50)) // 100


def net_litres(gross, temp10):
    """Litres at 15 C, rounded half up, as the meters' registers print them."""
    num = gross * (10000 - vcf_ptt(temp10))
    return (2 * num + 10000) // 20000


def dur_for(gross, lpm):
    """Whole minutes at the delivery rate, five at least."""
    return max(5, (gross + lpm // 2) // lpm) * M


# ---------------------------------------------------------------- the hydrant's plug flow
def _split(runs, q, total):
    """q litres taken from a stream of runs totalling `total`, the same share of every run, by floors of the
    cumulative, so the part sums exactly to q."""
    if total <= 0 or q <= 0:
        return []
    out, cum, prev = [], 0, 0
    for lab, v in runs:
        cum += v
        upto = q * cum // total
        if upto > prev:
            out.append([lab, upto - prev])
        prev = upto
    return out


DRAWS = ("hydrant", "drain")


def simulate_hydrant(ups, t_lo=T_OPEN, t_hi=T_SUSP, edges=(T0, T1), litres="gross", probes=(), net=None,
                     kinds=DRAWS):
    """Every segment's contents as FIFO runs from the export window's opening to t_hi.

    edges: the times the farm header's fuel changes from Tank 2 to Tank 3 and from Tank 3 to Tank 1.
    litres: 'gross' moves each draw's litres at fuel temperature (what a pipe holds); 'net' moves its litres at
    15 C, the misreading the generator asserts inert. kinds: which draws move fuel ('drain' is the low point drains
    and the idle-pit flushes). Returns per-draw litres by label, every segment's runs at t_hi (downstream end
    first) and the label standing at each probed draw point at each probed time."""
    net = net or GOLD
    contents = {seg: deque([[net.init[seg], net.fill[seg]]]) for seg in net.segments}
    events = {t_lo, t_hi, edges[0], edges[1]}
    probe_at = {}
    for pt, pit in probes:
        if t_lo < pt <= t_hi:
            events.add(pt)
            probe_at.setdefault(pt, []).append(pit)
    seen = {}
    live = [u for u in ups if u.kind in kinds and u.end > t_lo and u.start < t_hi]
    for u in live:
        events.add(max(t_lo, u.start))
        events.add(min(t_hi, u.end))
    times = sorted(e for e in events if t_lo <= e <= t_hi)
    got = {u.uid: {"aged": 0, "old": 0, "batch": 0, "new": 0} for u in live}
    by_pit = {}
    for u in live:
        by_pit.setdefault(u.pit, []).append(u)

    def moved(u, a, b):
        g = u.cum(b) - u.cum(a)
        if litres == "net":
            g = net_litres(g, u.temp10)
        return g

    def record(b):
        for pit in probe_at.get(b, []):
            seen[(b, pit)] = contents[net.seg_into[net.pit_node[pit]]][0][0]

    for a, b in zip(times, times[1:]):
        label = "old" if a < edges[0] else ("batch" if a < edges[1] else "new")
        draw, users = {}, {}
        for pit, lst in by_pit.items():
            for u in lst:
                if u.start < b and u.end > a:
                    v = moved(u, a, b)
                    if v > 0:
                        draw[pit] = draw.get(pit, 0) + v
                        users.setdefault(pit, []).append((u, v))
        if not draw:
            record(b)
            continue
        flow = {seg: sum(draw.get(p, 0) for p in net.seg_pits[seg]) for seg in net.topo}
        total = sum(draw.values())
        arriving = {"P": ([[label, total]], total)}
        for seg in net.topo:
            q = flow[seg]
            if q <= 0:
                continue
            stream, tot = arriving[net.seg_from[seg]]
            dq = contents[seg]
            for lab, v in _split(stream, q, tot):
                if dq and dq[-1][0] == lab:
                    dq[-1][1] += v
                else:
                    dq.append([lab, v])
            out, need = [], q
            while need > 0:
                lab, v = dq[0]
                if v <= need:
                    dq.popleft()
                    out.append([lab, v])
                    need -= v
                else:
                    dq[0][1] = v - need
                    out.append([lab, need])
                    need = 0
            node = net.seg_to[seg]
            arriving[node] = (out, q)
            here = [(u, v) for p in net.node_pits.get(node, []) for (u, v) in users.get(p, [])]
            d_here = sum(v for _, v in here)
            if d_here > 0:
                part = _split(out, d_here, q)
                for u, v in here:
                    for lab, x in _split(part, v, d_here):
                        got[u.uid][lab] += x
        record(b)
    return got, {seg: [tuple(run) for run in contents[seg]] for seg in contents}, seen


def standing(contents, label="batch", net=None):
    """Litres of a label standing in each section."""
    net = net or GOLD
    out = {sec: 0 for sec in SECTIONS}
    for seg, runs in contents.items():
        out[net.seg_section[seg]] += sum(v for lab, v in runs if lab == label)
    return out
