"""The golden and the easy routes for the call: which sections hold the batch at the suspension and which hydrant
uplifts took it. Each route reads only what a solver could build from the shipped records, and each predicts the
fuel standing at every shipped sample, so the samples can be scored against it."""
import sim
from sim import T0, T1, T_SUSP, T_OPEN, TOTAL_FILL, SECTIONS, BRANCHES, PIT_SECTION, path_fill, section_fill

DRAWS = sim.DRAWS


def pumped_between(ups, a, b):
    """Litres through the pump station's meter between two local seconds: every draw on the hydrant."""
    return sum(u.cum(b) - u.cum(a) for u in ups if u.kind in DRAWS)


def when_pumped(ups, a, target):
    """First local second after a by which the pump station has delivered `target` litres."""
    lo, hi = a, T_SUSP
    if pumped_between(ups, a, hi) < target:
        return None
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if pumped_between(ups, a, mid) >= target:
            hi = mid
        else:
            lo = mid
    return hi


def window_label(t, a, b):
    if a is None or t < a:
        return "old"
    if b is None or t < b:
        return "batch"
    return "new"


def _window_took(ups, windows):
    """Batch litres each uplift takes when its pit carries the batch inside a window (pit -> (start, end))."""
    took = {}
    for u in ups:
        if u.kind != "hydrant" or u.end <= T_OPEN:
            continue
        w = windows.get(u.pit)
        if not w or w[0] is None:
            continue
        a, b = w
        b = b if b is not None else T_SUSP
        lo, hi = max(u.start, a), min(u.end, b)
        if hi > lo:
            v = u.cum(hi) - u.cum(lo)
            if v > 0:
                took[u.uid] = v
    return took


def _labels(samples, windows):
    out = {}
    for s in samples:
        a, b = windows(s["pit"])
        out[(s["time"], s["pit"])] = window_label(s["time"], a, b)
    return out


def golden(ups, samples=(), litres="gross", edges=(T0, T1), kinds=DRAWS):
    probes = [(s["time"], s["pit"]) for s in samples]
    got, contents, seen = sim.simulate_hydrant(ups, litres=litres, edges=edges, probes=probes, kinds=kinds)
    return {"standing": sim.standing(contents), "took": {k: v["batch"] for k, v in got.items() if v["batch"] > 0},
            "got": got, "contents": contents, "labels": seen}


def route_window(ups, samples=()):
    """R0: the batch reaches every pit while Tank 3 is lined up, and the hydrant is clear once it is off line."""
    pits = {u.pit for u in ups if u.kind == "hydrant"}
    win = lambda p: (T0, T1)
    return {"standing": {s: 0 for s in SECTIONS}, "took": _window_took(ups, {p: win(p) for p in pits}),
            "labels": _labels(samples, win)}


def route_line_fill(ups, samples=()):
    """R1: one line fill of the whole hydrant through the pump station's meter after each change moves every pit
    onto the next tank's fuel (the product change reckoning)."""
    a = when_pumped(ups, T0, TOTAL_FILL)
    b = when_pumped(ups, T1, TOTAL_FILL)
    pits = {u.pit for u in ups if u.kind == "hydrant"}
    stand = {s: 0 for s in SECTIONS}
    if b is None:
        stand = {s: section_fill(s) for s in SECTIONS}
    win = lambda p: (a, b)
    return {"standing": stand, "took": _window_took(ups, {p: win(p) for p in pits}), "edges": (a, b),
            "labels": _labels(samples, win)}


def route_path(ups, samples=()):
    """R2: a pit is on the batch from when the pump station has delivered the pit's own path volume after 06:00
    until it has delivered it again after 15:40."""
    cache = {}

    def win(p):
        if p not in cache:
            pv = path_fill(p)
            cache[p] = (when_pumped(ups, T0, pv), when_pumped(ups, T1, pv))
        return cache[p]
    pits = {u.pit for u in ups if u.kind == "hydrant"}
    took = _window_took(ups, {p: win(p) for p in pits})
    labels = _labels(samples, win)
    stand = {s: 0 for s in SECTIONS}
    return {"standing": stand, "took": took, "labels": labels}


def route_section_turnover(ups, samples=()):
    """R3: a branch still holds the batch if its own pits drew less than its own line fill after 15:40 (the
    branch's turnover), and then holds its whole line fill; the notices and samples follow R2."""
    drew = {s: 0 for s in SECTIONS}
    for u in ups:
        if u.kind in DRAWS:
            drew[PIT_SECTION[u.pit]] += u.cum(T_SUSP) - u.cum(T1)
    stand = {s: (section_fill(s) if s in BRANCHES and drew[s] < section_fill(s) else 0) for s in SECTIONS}
    r2 = route_path(ups, samples)
    return {"standing": stand, "took": r2["took"], "labels": r2["labels"], "drew": drew}


def route_lumped(ups, samples=()):
    """R5: the farm header and the main tracked as FIFOs and each branch as one pipe of its section line fill,
    every pit of it drawing from its far end (the section-by-section reckoning)."""
    net = sim.lumped_network()
    probes = [(s["time"], s["pit"]) for s in samples]
    got, contents, seen = sim.simulate_hydrant(ups, probes=probes, net=net)
    stand = sim.standing(contents, net=net)
    return {"standing": stand, "took": {k: v["batch"] for k, v in got.items() if v["batch"] > 0}, "labels": seen}


def heuristic_low_use(ups):
    """H1: the branches whose pits the agents flush as idle hold the batch (the idle-pit flushes mark them)."""
    return {"standing_sections": ["E", "F", "G"]}


def heuristic_closed(ups):
    """H2: only the stands closed during the batch's time hold it."""
    return {"standing_sections": ["B"]}


def heuristic_last_uplift(ups):
    """H3: a branch holds the batch if its last uplift before the suspension took the batch on R2's windows."""
    r2 = route_path(ups)
    last = {}
    for u in sorted([u for u in ups if u.kind == "hydrant" and u.start < T_SUSP], key=lambda x: x.start):
        last[PIT_SECTION[u.pit]] = u
    return {"standing_sections": sorted(s for s, u in last.items() if u.uid in r2["took"])}


ROUTES = {"R0": route_window, "R1": route_line_fill, "R2": route_path, "R3": route_section_turnover,
          "R5": route_lumped}
HEURISTICS = {"H1": heuristic_low_use, "H2": heuristic_closed, "H3": heuristic_last_uplift}
