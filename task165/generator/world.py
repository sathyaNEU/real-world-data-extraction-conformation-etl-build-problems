"""task165 world: the road network, each segment's service history and coverage, the circuits and fleet, and the
storm events of five winters. Everything here is the clean truth; records.py turns it into the systems' exports.

Coverage (h) is the share of a collector's lane-km Priority 2 trucks salt (its intersection approaches, hills and
curves). It is drawn independently of yard, lanes, length, circuit and street, and it never ships."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K

# ----------------------------------------------------------------------------------------------- parameters
# tonnes of rock salt per lane-km in a winter at the planning severity (61.7 WSI points)
R_MID = 6.297     # Priority 1 over a collector's length
R_HAZ1 = 9.697    # Priority 1 on a collector's hazard lane-km (its full pass plus the blasts there)
R_HAZ2 = 10.23    # Priority 2 on a collector's hazard lane-km (spot treatment, heavier once ice has formed)
R_ART = 12.05     # Priority 1 arterials
ART_YARD = {"KLV": 1.03, "MPF": 0.98, "RDG": 1.06, "LKS": 0.95}
R_LOCAL_SS = 1.10  # sand-salt on Priority 3 hill locals (tonnes of mix per lane-km), material SS
M_SD = 0.035       # a segment's own persistent multiplier
EVENT_CV = 0.16    # a segment's salt in one event about its expectation
SHOCK_SD = 0.003   # a winter's effect the index does not carry

# coverage by pool (mean, concentration of a beta draw)
H_NEW = (0.155, 16.0)
H_REASON = {"hill": (0.58, 4.0), "school": (0.44, 4.0), "hospital": (0.40, 4.0), "transit": (0.37, 4.0)}
H_FLAT = (0.13, 12.0)   # the flat streets each reason also brought in (three in ten)
TRANSIT_OPEN = 0.75     # share of a transit-move street's untreated length kept from its draw
H_INNER = (0.45, 8.0)
H_P2 = (0.33, 6.0)
BATCH_MIX = {"A": {"hill": 40, "school": 18}, "B": {"transit": 20, "school": 20, "hospital": 12},
             "C": {"hill": 30, "hospital": 12, "school": 8}, "D": {"transit": 22, "school": 12, "hill": 8}}

NEW_LANE_KM = 424.00

# ----------------------------------------------------------------------------------------------- street names
_BASES_ART = [
    "Kelvin", "Mapleford", "Ridge", "Lakeshore", "Dundalk", "Talbot", "Garrow", "Wexley Line", "Cardigan", "Huron",
    "Stanhope", "Ossory", "Bellwood", "Fennimore", "Northcote", "Brennan", "Carrick", "Montague", "Highfield",
    "Pinecrest", "Wardell", "Glengarry", "Ashgrove", "Thornhill Side", "Larchmont", "Castlefield", "Peel Line",
    "Denholm", "Rowan", "Sutherland", "Kingsmere", "Old Mill", "Dorset", "Hallam", "Tremont", "Belgrave",
    "Concession 4", "Waverley", "Elgin", "Fairbank", "Lansdown", "Ridgeback", "Queensway", "Harbour",
]
_SFX_ART = ["Road", "Road", "Road", "Boulevard", "Avenue", "Street", "Parkway", "Drive"]
_BASES_COL = [
    "Abbott", "Alderson", "Applewood", "Archer", "Arden", "Ashby", "Aspen", "Auburn", "Avonlea", "Balsam", "Bancroft",
    "Barclay", "Barrow", "Bayview", "Beacon", "Beckett", "Beechwood", "Birch", "Blackburn", "Blair", "Bolton",
    "Bramble", "Brant", "Briar", "Bridgeport", "Brock", "Bruce", "Buckingham", "Burnside", "Cambrian", "Camden",
    "Canterbury", "Carlisle", "Carlton", "Cedar", "Chalmers", "Chapel", "Charlton", "Chester", "Clarence",
    "Clifton", "Cobden", "Colborne", "Coleridge", "Conant", "Cornwall", "Coronation", "Cotswold", "Cromwell",
    "Cumberland", "Dalhousie", "Dawson", "Deerfield", "Delaware", "Devon", "Dorchester", "Douglas", "Dufferin",
    "Dunbar", "Durham", "Eastwood", "Edgewater", "Edison", "Eglinton", "Elmwood", "Emerson", "Essex", "Everett",
    "Fairfield", "Falcon", "Farrell", "Fenwick", "Ferndale", "Fleming", "Forest Glen", "Foxwood", "Franklin",
    "Fraser", "Gardner", "Garfield", "Gibson", "Gladstone", "Glenview", "Gordon", "Grafton", "Granville",
    "Greenbank", "Greenwood", "Grey", "Grove", "Haddon", "Halton", "Hamilton", "Harcourt", "Harding", "Harmony",
    "Hartley", "Hastings", "Hawthorne", "Hazel", "Heather", "Hemlock", "Heritage", "Hickory", "Hillcrest",
    "Holland", "Hollis", "Howard", "Hudson", "Hunter", "Inglewood", "Ironwood", "Jarvis", "Juniper", "Keats",
    "Kensington", "Kent", "Kerr", "Kingsley", "Kipling", "Knox", "Lambton", "Lancaster", "Laurel", "Lawrence",
    "Leeds", "Lennox", "Lincoln", "Linden", "Livingston", "Locke", "Lockhart", "Lorne", "Lyndhurst", "Macdonald",
    "Mackenzie", "Madison", "Manor", "Maplewood", "Marlborough", "Marshall", "Mayfair", "McCormick", "Meadowvale",
    "Melrose", "Merritt", "Milford", "Millbrook", "Milton", "Minto", "Mohawk", "Monarch", "Moore", "Morris",
    "Mountbatten", "Murray", "Nelson", "Newbury", "Norfolk", "Norwood", "Oak Ridge", "Oakdale", "Orchard",
    "Osler", "Oxford", "Palmer", "Park Lawn", "Parkside", "Pembroke", "Percy", "Pleasant", "Poplar", "Portage",
    "Prince Albert", "Prospect", "Quarry", "Radcliffe", "Raglan", "Ramsay", "Redwood", "Regent", "Richmond",
    "Rideau", "Riverside", "Robson", "Rockwood", "Rosedale", "Rossland", "Russell", "Rutherford", "Sandford",
    "Scarlett", "Selkirk", "Seneca", "Shaftesbury", "Sheridan", "Sherwood", "Simcoe", "Somerset", "Southgate",
    "Spencer", "Spring Garden", "Spruce", "Stafford", "Stirling", "Stratford", "Summit", "Sunnyside", "Sydenham",
    "Tamarack", "Tecumseh", "Thistle", "Thompson", "Tiffany", "Trafalgar", "Trillium", "Tudor", "Union",
    "Valleyview", "Vaughan", "Victoria Park", "Walker", "Walnut", "Warwick", "Waterloo", "Wellesley", "Westmount",
    "Whitney", "Wildwood", "Willow", "Wilson", "Windermere", "Winston", "Woodbine", "Woodlawn", "York", "Yorkshire",
    "Allan", "Ardagh", "Baird", "Bennett", "Cairns", "Dempsey", "Doherty", "Elliot", "Finch", "Galloway", "Hagen",
    "Irving", "Jameson", "Keegan", "Lister", "Maitland", "Nash", "O'Connor", "Pritchard", "Quinlan", "Reid",
    "Sinclair", "Tobin", "Upton", "Vance", "Whitfield",
]
_SFX_COL = ["Street", "Street", "Avenue", "Avenue", "Drive", "Road", "Crescent", "Boulevard", "Way", "Line"]


def _street_names(rng, bases, sfx, n):
    out, seen = [], set()
    order = rng.permutation(len(bases))
    i = 0
    while len(out) < n:
        b = bases[order[i % len(bases)]]
        s = sfx[rng.integers(0, len(sfx))]
        name = b if b.startswith("Concession") or b.endswith("Line") or b.endswith("Side") else "%s %s" % (b, s)
        if i >= len(bases):
            if " " not in name:
                name = "%s %s" % (b, ["East", "West", "North", "South"][rng.integers(0, 4)])
            else:
                name = "%s %s" % (name, ["East", "West", "North", "South"][K.stable_int(b, i) % 4])
        if name not in seen:
            seen.add(name)
            out.append(name)
        i += 1
    return out


class World:
    def __init__(self, seed=K.SEED):
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.segments = []      # dicts
        self.circuits = {}      # route_code -> dict
        self.units = []         # fleet
        self.events = {}        # winter -> list of event dicts
        self.shock = {}
        self._build_network()
        self._build_circuits_and_fleet()
        self._build_events()

    # ------------------------------------------------------------------------------------------- network
    def _seg_id(self, k):
        return "RS%06d" % k

    def _build_network(self):
        rng = np.random.default_rng(self.seed + 1)
        art_streets = _street_names(rng, _BASES_ART, _SFX_ART, 44)
        col_streets = _street_names(rng, _BASES_COL, _SFX_COL, 300)
        cross = list(col_streets)
        idgen = iter(sorted(rng.choice(np.arange(100000, 899999), size=9000, replace=False)))
        segs = []

        def add(street, yard, func, pool, lanes, cl, h, reason=None, batch=None):
            s = {"segment_id": self._seg_id(int(next(idgen))), "street": street, "yard": yard, "func_class": func,
                 "pool": pool, "lanes": lanes, "centreline_km": round(float(cl), 2),
                 "h": float(h), "m": float(math.exp(rng.normal(0, M_SD))), "reason": reason, "batch": batch}
            s["lane_km"] = round(s["lanes"] * s["centreline_km"], 2)
            segs.append(s)
            return s

        # arterials: 44 streets, each split over one to three yards in runs of segments
        for st in art_streets:
            nseg = int(rng.integers(11, 20))
            yard_seq = rng.choice(K.YARDS, size=int(rng.integers(1, 3)), replace=False)
            lanes = int(rng.choice([4, 6, 2], p=[0.62, 0.32, 0.06]))
            for i in range(nseg):
                yard = yard_seq[min(i * len(yard_seq) // nseg, len(yard_seq) - 1)]
                add(st, yard, "ARTERIAL", "ART", lanes, rng.uniform(0.55, 1.45), 0.0)
        # inner-city frequent collectors, Priority 1 throughout
        self._collector_block(rng, col_streets[0:20], "P1IN", 85, add, H_INNER)
        # the earlier moves, batch by batch, reason by reason
        cursor = 20
        for b in "ABCD":
            for reason, n in BATCH_MIX[b].items():
                nst = max(2, n // 4)
                self._collector_block(rng, col_streets[cursor:cursor + nst], "MOVE", n, add, H_REASON[reason],
                                      reason=reason, batch=b)
                cursor += nst
        # the redesign's frequent network collectors (424.0 lane-km)
        new_streets = col_streets[cursor:cursor + 34]
        cursor += 34
        self._collector_block(rng, new_streets, "NEW", 216, add, H_NEW)
        # the rest of the Priority 2 collectors
        self._collector_block(rng, col_streets[cursor:cursor + 150], "P2", 780, add, H_P2)
        cursor += 150
        # Priority 3 hill locals salted with sand-salt
        for i in range(64):
            st = col_streets[cursor + (i % 40)] if cursor + 40 < len(col_streets) else col_streets[i % 40]
            add(st, K.YARDS[i % 4], "LOCAL", "P3", 2, rng.uniform(0.15, 0.45), 0.0)
        self._fit_new_lane_km(segs)
        # cross streets: from / to along each street in order
        by_street = {}
        for s in segs:
            by_street.setdefault(s["street"], []).append(s)
        for st, ss in by_street.items():
            names = [c for c in cross if c != st]
            pick = rng.choice(len(names), size=len(ss) + 1, replace=False)
            for i, s in enumerate(ss):
                s["from_street"], s["to_street"] = names[pick[i]], names[pick[i + 1]]
        self.segments = segs
        self.by_id = {s["segment_id"]: s for s in segs}
        self._legacy_ids(rng, idgen)

    def _legacy_ids(self, rng, idgen):
        """The 2023 GIS re-segmentation split some long arterial and Priority 2 segments at new intersections:
        each such pair of current segments carried one legacy id before October 2023."""
        for s in self.segments:
            s["legacy_id"] = s["segment_id"]
        self.splits = []
        for pool, n in (("ART", 26), ("P2", 22)):
            by_street = {}
            for s in self.segments:
                if s["pool"] == pool:
                    by_street.setdefault(s["street"], []).append(s)
            cands = []
            for st, ss in sorted(by_street.items()):
                for i in range(0, len(ss) - 1, 2):
                    if ss[i]["yard"] == ss[i + 1]["yard"] and ss[i]["lanes"] == ss[i + 1]["lanes"]:
                        cands.append((ss[i], ss[i + 1]))
            pick = rng.choice(len(cands), size=n, replace=False)
            for j in sorted(pick):
                a, b = cands[j]
                old = self._seg_id(int(next(idgen)))
                a["legacy_id"] = b["legacy_id"] = old
                tot = a["centreline_km"] + b["centreline_km"]
                self.splits.append({"old": old, "new": [a["segment_id"], b["segment_id"]],
                                    "share": [round(a["centreline_km"] / tot, 4), round(b["centreline_km"] / tot, 4)]})

    def _collector_block(self, rng, streets, pool, n, add, hpar, reason=None, batch=None):
        mean, k = hpar
        per = np.full(len(streets), n // len(streets))
        per[: n - per.sum()] += 1
        for st, cnt in zip(streets, per):
            yard = K.YARDS[int(rng.integers(0, 4))]
            lanes = 4 if rng.random() < 0.08 else 2
            for _ in range(int(cnt)):
                flat = pool == "MOVE" and rng.random() < 0.30
                if flat:
                    h = rng.beta(H_FLAT[0] * H_FLAT[1], (1 - H_FLAT[0]) * H_FLAT[1])
                else:
                    h = rng.beta(mean * k, (1 - mean) * k)
                    if reason == "transit":
                        # the earlier transit upgrades ran on inner-suburb streets, an intersection every block
                        h = 1.0 - (1.0 - h) * TRANSIT_OPEN
                add(st, yard, "COLLECTOR", pool, lanes, rng.uniform(0.45, 1.35), h, reason, batch)

    def _fit_new_lane_km(self, segs):
        """Scale the redesign segments' lengths so their lane-km sum to exactly 424.00 after rounding."""
        new = [s for s in segs if s["pool"] == "NEW"]
        tot = sum(s["lanes"] * s["centreline_km"] for s in new)
        f = NEW_LANE_KM / tot
        for s in new:
            s["centreline_km"] = round(s["centreline_km"] * f, 2)
            s["lane_km"] = round(s["lanes"] * s["centreline_km"], 2)
        diff = round(NEW_LANE_KM - sum(s["lane_km"] for s in new), 2)
        # absorb the rounding residue on two-lane segments, 0.02 lane-km (0.01 km) at a time
        two = [s for s in new if s["lanes"] == 2]
        i = 0
        while abs(diff) > 1e-9:
            step = 0.01 if diff > 0 else -0.01
            s = two[i % len(two)]
            s["centreline_km"] = round(s["centreline_km"] + step, 2)
            s["lane_km"] = round(2 * s["centreline_km"], 2)
            diff = round(diff - 2 * step, 2)
            i += 1
        assert abs(sum(s["lane_km"] for s in new) - NEW_LANE_KM) < 1e-6

    # ------------------------------------------------------------------------------------------- service history
    def priority(self, s, winter):
        """The segment's priority in a winter (season start)."""
        p = s["pool"]
        if p in ("ART", "P1IN"):
            return 1
        if p == "P3":
            return 3
        if p == "MOVE":
            return 1 if K.WINTERS.index(winter) >= K.WINTERS.index(K.FIRST_P1_WINTER[s["batch"]]) else 2
        return 2   # NEW and P2 were Priority 2 through 2025-26

    def rate(self, s, winter):
        """Expected rock salt per lane-km in a winter at the planning severity, before the segment multiplier."""
        pr = self.priority(s, winter)
        if s["pool"] == "ART":
            return R_ART * ART_YARD[s["yard"]]
        if s["pool"] == "P3":
            return R_LOCAL_SS
        h = s["h"]
        if pr == 1:
            return R_MID * (1 - h) + R_HAZ1 * h
        return R_HAZ2 * h

    def gain_truth(self, s):
        """Expected gain per lane-km at the planning severity on moving Priority 2 to Priority 1."""
        h = s["h"]
        return (R_MID * (1 - h) + R_HAZ1 * h - R_HAZ2 * h)

    # ------------------------------------------------------------------------------------------- circuits and fleet
    def _build_circuits_and_fleet(self):
        rng = np.random.default_rng(self.seed + 2)
        counters = {}

        def code(yard, letter):
            counters[(yard, letter)] = counters.get((yard, letter), 0) + 1
            return "%s-%s%02d" % (yard, letter, counters[(yard, letter)])

        # arterial circuits: consecutive segments of a street within a yard, about 9 to 13 per circuit
        by_key = {}
        for s in self.segments:
            if s["pool"] == "ART":
                by_key.setdefault((s["yard"], s["street"]), []).append(s)
        art_runs = {y: [] for y in K.YARDS}
        for (y, st), ss in sorted(by_key.items()):
            art_runs[y].extend(ss)
        for y in K.YARDS:
            ss = art_runs[y]
            i = 0
            while i < len(ss):
                n = int(rng.integers(9, 14))
                chunk = ss[i:i + n]
                if len(ss) - (i + n) < 5:
                    chunk = ss[i:]
                rc = code(y, "A")
                for s in chunk:
                    s["route_code"] = rc
                self.circuits[rc] = {"route_code": rc, "yard": y, "kind": "ART", "segments": [s["segment_id"] for s in chunk]}
                i += len(chunk)
        # collector circuits by priority in each winter: P1 collector circuits (C) and Priority 2 spot circuits (S)
        for y in K.YARDS:
            for pool_set, letter in ((("P1IN",), "C"), (("MOVE", "NEW", "P2"), "S"), (("P3",), "H")):
                ss = [s for s in self.segments if s["yard"] == y and s["pool"] in pool_set]
                ss.sort(key=lambda s: (s["street"], s["segment_id"]))
                size = 14 if letter == "S" else (10 if letter == "C" else 8)
                for i in range(0, len(ss), size):
                    rc = code(y, letter)
                    for s in ss[i:i + size]:
                        s["route_code_p2"] = rc if letter == "S" else None
                        if letter != "S":
                            s["route_code"] = rc
                    self.circuits[rc] = {"route_code": rc, "yard": y, "kind": letter,
                                         "segments": [s["segment_id"] for s in ss[i:i + size]]}
        # each move batch joins Priority 1 collector circuits in its yard from its first Priority 1 winter
        for y in K.YARDS:
            for b in "ABCD":
                ss = [s for s in self.segments if s["yard"] == y and s["pool"] == "MOVE" and s["batch"] == b]
                ss.sort(key=lambda s: (s["street"], s["segment_id"]))
                for i in range(0, len(ss), 10):
                    rc = code(y, "C")
                    for s in ss[i:i + 10]:
                        s["route_code_p1"] = rc
                    self.circuits[rc] = {"route_code": rc, "yard": y, "kind": "C",
                                         "segments": [s["segment_id"] for s in ss[i:i + 10]], "from": K.MOVE_DATES[b]}
            ss = [s for s in self.segments if s["yard"] == y and s["pool"] == "NEW"]
            ss.sort(key=lambda s: (s["street"], s["segment_id"]))
            for i in range(0, len(ss), 10):
                rc = code(y, "C")
                for s in ss[i:i + 10]:
                    s["route_code_p1"] = rc
                self.circuits[rc] = {"route_code": rc, "yard": y, "kind": "C",
                                     "segments": [s["segment_id"] for s in ss[i:i + 10]], "from": K.REDESIGN}
        for s in self.segments:
            if s["pool"] in ("MOVE", "NEW", "P2"):
                s["route_code"] = s.get("route_code_p1") if s["pool"] in ("MOVE", "NEW") else s["route_code_p2"]
        # fleet: one unit per circuit plus spares; tandems on arterial circuits, single axles on collector circuits
        self.units = []
        num = {"T": 5100, "S": 5240}
        for rc, c in sorted(self.circuits.items()):
            kind = "T" if c["kind"] == "ART" else "S"
            num[kind] += int(rng.integers(1, 4))
            u = {"unit_id": str(num[kind]), "yard": c["yard"], "class": "TANDEM" if kind == "T" else "SINGLE AXLE",
                 "home_circuit": rc}
            if kind == "T":
                u["controller"], u["retrofit"] = "M720", None
            else:
                u["controller"] = "M720"
                u["retrofit"] = None
            c["unit"] = u["unit_id"]
            self.units.append(u)
        # the three oldest tandems at each yard still carry the M410 controller; the first of them at each yard
        # was refitted with an M720 in the summer of 2025
        for k, y in enumerate(K.YARDS):
            tand = sorted((u for u in self.units if u["yard"] == y and u["class"] == "TANDEM"),
                          key=lambda u: int(u["unit_id"]))
            for j, u in enumerate(tand[:3]):
                u["controller"] = "M410"
                u["retrofit"] = dt.date(2025, 7, 7) + dt.timedelta(days=9 * k + 2) if j == 0 else None
        self.unit_by_id = {u["unit_id"]: u for u in self.units}
        # contractor circuits (Kettlewood Road Services) at Kelvin Road and Mapleford
        art_c = sorted(rc for rc, c in self.circuits.items() if c["kind"] == "ART")
        self.contract_circuits = [rc for rc in art_c if rc.startswith("KLV")][-2:] + \
                                 [rc for rc in art_c if rc.startswith("MPF")][-1:]
        # the 1 July 2026 realignment: two Mapleford arterial circuits pass to Kelvin Road
        self.realigned = [rc for rc in art_c if rc.startswith("MPF") and rc not in self.contract_circuits][:2]
        klv_n = max(int(rc.split("-A")[1]) for rc in art_c if rc.startswith("KLV"))
        self.realigned_codes = {rc: "KLV-A%02d" % (klv_n + 1 + i) for i, rc in enumerate(self.realigned)}

    def controller_on(self, unit_id, day: dt.date):
        u = self.unit_by_id[unit_id]
        if u["controller"] == "M410":
            return "M410" if (u["retrofit"] is None or day < u["retrofit"]) else "M720"
        return "M720"

    # ------------------------------------------------------------------------------------------- weather
    def _build_events(self):
        rng = np.random.default_rng(self.seed + 3)
        for w in K.WINTERS:
            self.shock[w] = float(rng.normal(0, SHOCK_SD))
            a, b = K.SEASON[w]
            n = int(rng.integers(36, 45))
            days = (b - a).days
            # event starts spread through the season, none in the first or last 10 hours
            starts = sorted(rng.uniform(0.6, days - 1.2, n))
            # keep at least 26 hours between starts
            evs = []
            last = -9
            for x in starts:
                if x - last < 1.1:
                    continue
                last = x
                t0 = dt.datetime.combine(a, dt.time(0, 0)) + dt.timedelta(days=float(x))
                t0 = t0.replace(minute=(t0.minute // 5) * 5, second=0, microsecond=0)
                typ = rng.choice(["SN", "SN", "SN", "FZ", "MX", "IC"], p=[0.3, 0.2, 0.1, 0.15, 0.15, 0.1])
                pts = float(rng.gamma(2.2, 0.62))
                dur = float(np.clip(rng.normal(6 + 4.5 * pts, 3), 3, 40))
                evs.append({"start": t0, "hours": dur, "type": str(typ), "raw_pts": pts})
            tot = sum(e["raw_pts"] for e in evs)
            target = K.WSI_TARGET[w]
            run = 0.0
            for i, e in enumerate(evs):
                if i < len(evs) - 1:
                    p = round(e["raw_pts"] * target / tot, 1)
                    p = max(p, 0.2)
                else:
                    p = round(target - run, 1)
                run = round(run + p, 1)
                e["points"] = p
                e["end"] = e["start"] + dt.timedelta(hours=e["hours"])
                e["end"] = e["end"].replace(minute=(e["end"].minute // 5) * 5, second=0, microsecond=0)
                snow = 0.0 if e["type"] in ("FZ", "IC") else round(max(0.2, p * rng.uniform(2.6, 4.2)), 1)
                fz = round(p * rng.uniform(0.8, 2.2), 1) if e["type"] in ("FZ", "MX") else 0.0
                e["snow_cm"], e["fzra_mm"] = snow, fz
                e["min_pave_c"] = round(float(rng.uniform(-13, -1)), 1)
            # season end: the last event and its clean-up clear 31 March by 18:00
            limit = dt.datetime.combine(b, dt.time(18, 0))
            for e in evs:
                if e["end"] + dt.timedelta(hours=4) > limit:
                    e["end"] = limit - dt.timedelta(hours=4)
                    e["hours"] = (e["end"] - e["start"]).total_seconds() / 3600.0
            assert abs(sum(e["points"] for e in evs) - target) < 1e-6, (w, sum(e["points"] for e in evs))
            for i, e in enumerate(evs):
                e["event_no"] = i + 1
            self.events[w] = evs
