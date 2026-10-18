"""task165 records: the spreader passes of five winters, rendered the way each system records them, and the yards'
own material records. The clean truth (each segment's salt in each event and pass) is kept on the Sim object."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K
import world as Wd

SPEED_KMH = {"ART": 28.0, "C": 24.0, "S": 26.0, "H": 18.0}


class Sim:
    """Every pass of every circuit in every declared event, with each segment's salt in it (tonnes)."""

    def __init__(self, W: Wd.World):
        self.W = W
        self.rng = np.random.default_rng(W.seed + 10)
        self.passes = []      # one dict per (circuit, event, pass index): unit, start, rows
        self.truth = {}       # (segment_id, winter) -> tonnes in season
        self.patrols = []     # arterial frost patrols outside the storm log
        self._run()

    def circuit_of(self, s, winter):
        pr = self.W.priority(s, winter)
        if s["pool"] in ("MOVE", "NEW"):
            return s["route_code_p1"] if pr == 1 else s["route_code_p2"]
        if s["pool"] == "P2":
            return s["route_code_p2"]
        return s["route_code"]

    def _run(self):
        W, rng = self.W, self.rng
        segs = [s for s in W.segments]
        for w in K.WINTERS:
            # circuit membership this winter
            members = {}
            for s in segs:
                rc = self.circuit_of(s, w)
                if rc in W.contract_circuits:
                    members.setdefault(rc, []).append(s)
                    continue
                members.setdefault(rc, []).append(s)
            for e in W.events[w]:
                pts = e["points"]
                for rc, ss in sorted(members.items()):
                    c = W.circuits[rc]
                    kind = c["kind"]
                    if kind == "H" and pts < 1.2:
                        continue
                    if kind == "ART":
                        n = int(min(9, 2 + rng.poisson(0.55 * pts)))
                        t_a, t_b = 0.3, e["hours"] + 2.5
                    elif kind == "C":
                        n = int(min(7, 1 + rng.poisson(0.42 * pts)))
                        t_a, t_b = 0.5, e["hours"] + 3.0
                    elif kind == "S":
                        n = 1 + int(rng.random() < 0.22 + 0.04 * pts)
                        t_a, t_b = 0.45 * e["hours"], e["hours"] + 6.0
                    else:
                        n = 1
                        t_a, t_b = 0.6 * e["hours"], e["hours"] + 5.0
                    wts = rng.dirichlet(np.full(n, 3.0))
                    starts = sorted(rng.uniform(t_a, t_b, n))
                    seg_salt = {}
                    for s in ss:
                        exp_t = W.rate(s, w) * s["lane_km"] * s["m"] * (pts / K.PLANNING_SEVERITY) * (1 + W.shock[w])
                        seg_salt[s["segment_id"]] = exp_t * max(0.3, 1 + rng.normal(0, Wd.EVENT_CV))
                    unit = c.get("unit")
                    prev_end = None
                    for k in range(n):
                        t0 = e["start"] + dt.timedelta(hours=float(starts[k]))
                        if prev_end is not None and t0 < prev_end + dt.timedelta(minutes=8):
                            t0 = prev_end + dt.timedelta(minutes=8)       # one truck: a pass starts after the last
                        rows = []
                        clock = t0
                        for s in ss:
                            if kind == "S" and s["pool"] in ("MOVE", "NEW") and W.priority(s, w) == 1:
                                continue
                            share = wts[k] * (1 + rng.normal(0, 0.05))
                            amt = max(0.0, seg_salt[s["segment_id"]] * share)
                            dur = s["centreline_km"] / SPEED_KMH[kind] * (1 + rng.normal(0, 0.12))
                            t1 = clock + dt.timedelta(hours=max(0.01, dur))
                            rows.append({"segment_id": s["segment_id"], "entry": clock, "exit": t1, "t": amt})
                            clock = t1 + dt.timedelta(minutes=float(rng.uniform(0.2, 1.6)))
                        prev_end = clock
                        # renormalise so each segment's passes sum to its event salt
                        self.passes.append({"winter": w, "event": e["event_no"], "route_code": rc, "unit": unit,
                                            "kind": kind, "k": k, "rows": rows,
                                            "contract": rc in W.contract_circuits})
                    # exact event totals per segment
                    tot = {}
                    for p in self.passes[-n:]:
                        for r in p["rows"]:
                            tot[r["segment_id"]] = tot.get(r["segment_id"], 0.0) + r["t"]
                    for p in self.passes[-n:]:
                        for r in p["rows"]:
                            if tot[r["segment_id"]] > 0:
                                r["t"] *= seg_salt[r["segment_id"]] / tot[r["segment_id"]]
            # truth per segment and winter
        for p in self.passes:
            for r in p["rows"]:
                key = (r["segment_id"], p["winter"])
                self.truth[key] = self.truth.get(key, 0.0) + r["t"]
        # frost patrols on arterials at the season edges (not declared events): Lakeshore on the evening of
        # 31 October 2024 (before the season) and Ridge on the evening of 31 March 2026 (inside it)
        for day, yard, start_h in ((dt.date(2024, 10, 31), "LKS", 21.4), (dt.date(2026, 3, 31), "RDG", 21.2)):
            rcs = sorted(rc for rc, c in W.circuits.items() if c["kind"] == "ART" and c["yard"] == yard
                         and rc not in W.contract_circuits)[:3]
            for j, rc in enumerate(rcs):
                c = W.circuits[rc]
                clock = dt.datetime.combine(day, dt.time(0, 0)) + dt.timedelta(hours=start_h + 0.3 * j)
                rows = []
                for sid in c["segments"]:
                    s = W.by_id[sid]
                    amt = 0.045 * s["lane_km"] * (1 + rng.normal(0, 0.1))
                    dur = s["centreline_km"] / SPEED_KMH["ART"]
                    t1 = clock + dt.timedelta(hours=dur)
                    rows.append({"segment_id": sid, "entry": clock, "exit": t1, "t": amt})
                    clock = t1 + dt.timedelta(minutes=0.6)
                w = K.winter_of(day)
                self.patrols.append({"winter": w, "event": None, "route_code": rc, "unit": c["unit"],
                                     "kind": "ART", "k": 0, "rows": rows, "contract": False, "day": day})

    # ----------------------------------------------------------------------------------------- truths
    def seg_winter(self, sid, w):
        return self.truth.get((sid, w), 0.0)
