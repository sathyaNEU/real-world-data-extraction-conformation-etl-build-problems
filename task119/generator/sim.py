"""Turn each unit's event list into stays.

A unit starts full. A turnover discharges one occupant and admits the next patient in the same minute;
a gap opening discharges without replacement; a gap closing admits into the empty bed. The occupant who
leaves is the one most overdue against a length-of-stay target, never one inside a hold, and a patient
designed to die within the window leaves before a deadline. Legacy bed moves (two occupants exchange beds)
split both stays into contiguous bed-episode rows.
"""
import datetime as dt

import numpy as np

from common import (BEDS, FEED_UNITS, FEED0, RECORD1, WINTER0, WINTER1, lm, day_of, own_unit, unit_open,
                    is_bst, rng, LETTERS, DST_WINDOWS)
from world import LEGACY_END
import plan

PEL_OPEN = lm(dt.date(2023, 12, 4), 0, 0)
PEL_FILL = [lm(dt.date(2023, 12, 4), 9, 20), lm(dt.date(2023, 12, 4), 10, 5), lm(dt.date(2023, 12, 4), 11, 40)]
PEL_CLOSE = [lm(dt.date(2024, 3, 31), 9, 30), lm(dt.date(2024, 3, 31), 10, 10), lm(dt.date(2024, 3, 31), 10, 50)]
PEL_END = lm(dt.date(2024, 4, 1), 0, 0)
END_OF_FEED = lm(dt.date(2026, 7, 1), 0, 0)
LAST_DISCHARGE = lm(dt.date(2026, 8, 9), 18, 0)


def unit_windows(world):
    """Fixed gaps from the winter unit's opening and closing, registered before any wait is placed."""
    U = world.units["PEL-W3"]
    for t in PEL_FILL:
        world.gap_windows.append(("PEL-W3", PEL_OPEN, t))
    for t in PEL_CLOSE:
        world.gap_windows.append(("PEL-W3", t, PEL_END))
    U.frozen.append((PEL_OPEN, PEL_FILL[-1]))
    U.frozen.append((PEL_CLOSE[0], PEL_END))
    for t in PEL_FILL + PEL_CLOSE:
        U.add_event(t)


class Patients:
    """Registry of patients known to the generator (designed, background, planned, initial)."""

    def __init__(self):
        self.p = {}
        self.n = 0

    def new(self, **kw):
        pid = self.n
        self.n += 1
        d = {"pid": pid}
        d.update(kw)
        self.p[pid] = d
        return pid


GO = lm(dt.date(2024, 4, 2), 0, 0)


def legacy_transit_room(world, u, t, kind):
    """Room after a legacy bed allocation at minute t for the patient's arrival (plan.TRANSIT) before 08:00, the
    next frozen interval at the unit and any clock-change window."""
    if kind != "bg":
        return False
    hi = plan.TRANSIT[1]
    d8 = lm(day_of(t), 8, 0)
    nxt8 = d8 if t < d8 else d8 + 1440
    hi = min(hi, nxt8 - t - 1)
    for a, b in sorted(world.units[u].frozen):
        if a > t:
            hi = min(hi, a - t - 1)
            break
    for a, b in DST_WINDOWS:
        if t < b and t + hi > a:
            hi = min(hi, a - t - 1)
    return hi >= plan.TRANSIT[0] + 8


def assign_admissions(world, P):
    """Decide who is admitted at every slot before the simulation runs."""
    r = rng("admissions")
    wait_pid = {}
    second = {"DV2b2", "DV7b"}          # a patient's second long wait carries the first wait's patient
    for w in world.waits:
        if w["tags"] & second:
            continue
        pid = P.new(kind="wait", letter=w["letter"], wid=w["wid"])
        wait_pid[w["wid"]] = pid
        w["pid"] = pid
    for w in world.waits:
        if w["tags"] & second:
            w["pid"] = world.waits_by_id[w["pair"]]["pid"]
    readmit = {}
    adm = {u: [] for u in FEED_UNITS}
    for u, U in world.units.items():
        own_letter = [k for k, v in {"A": "RIS-ACC", "C": "BRK-ACC", "D": "STN-ACC", "G": "PRW-ACC",
                                     "F": "ELL-ACC", "H": "PEL-W3"}.items() if v == u][0]
        for s in U.slots:
            t = s["t"]
            if s["kind"] == "tx_in":
                # a patient from a trust without its own level-3 unit, placed here by the bed bureau: a planned
                # post-operative transfer from that trust's theatre recovery, or an unplanned transfer
                d = day_of(t)
                pool = ["E", "B"] + (["F"] if own_unit("F", d) is None else []) + \
                       (["H"] if own_unit("H", d) is None else [])
                pp = np.array([{"E": 0.5, "B": 0.22, "F": 0.16, "H": 0.12}[x] for x in pool])
                letter = str(r.choice(pool, p=pp / pp.sum()))
                planned = world.waits_by_id[s["ref"]].get("tx_kind") == "planned"
                pid = P.new(kind="bg", letter=letter, level=3, unit=u, tx_for=s["ref"], planned_tx=planned)
                src = "01" if planned else ("06" if r.random() < 0.74 else "04")
                adm[u].append({"t": t, "pid": pid, "type": "03" if planned else "02", "src": src,
                               "mode": "turn", "wid": None, "leaver": None, "bg": True})
                continue
            if s["kind"] in ("wait_end", "gap_close_wait"):
                w = world.waits_by_id[s["ref"]]
                adm[u].append({"t": t, "pid": w["pid"], "type": "01" if w["letter"] == own_letter else "02",
                               "src": "06" if r.random() < 0.78 else "04", "mode": "close" if s["kind"] == "gap_close_wait" else "turn",
                               "wid": w["wid"], "leaver": s.get("leaver")})
                continue
            # background referral admission
            d = day_of(t)
            if u == "PEL-W3":
                letter = "H"
            elif u == "ELL-ACC":
                letter = "F" if r.random() < 0.9 else str(r.choice(["B", "E", "H"]))
            else:
                if r.random() < 0.82:
                    letter = own_letter
                else:
                    pool = ["E", "B"] + (["F"] if own_unit("F", d) is None else []) + \
                           (["H"] if own_unit("H", d) is None else [])
                    pp = np.array([{"E": 0.45, "B": 0.2, "F": 0.2, "H": 0.15}[x] for x in pool])
                    letter = str(r.choice(pool, p=pp / pp.sum()))
            own = (own_unit(letter, d) == u)
            if not own and t < GO and not legacy_transit_room(world, u, t, s["kind"]):
                # a legacy transfer here would arrive after 08:00 or into a wait at this unit's own trust: the bed
                # goes to one of the trust's own patients instead
                letter, own = own_letter, True
            level = 3 if (not own or r.random() < 0.6) else 2
            if u == "PEL-W3":
                level = 3
            if own and u in ("RIS-ACC", "BRK-ACC", "STN-ACC", "PRW-ACC") and r.random() < 0.08:
                pid = P.new(kind="theatre_emerg", letter=letter, level=3, unit=u)
                adm[u].append({"t": t, "pid": pid, "type": "01", "src": "01",
                               "mode": "close" if s["kind"] == "gap_close_bg" else "turn", "wid": None,
                               "leaver": s.get("leaver")})
                continue
            pid = P.new(kind="bg", letter=letter, level=level, unit=u)
            adm[u].append({"t": t, "pid": pid, "type": "01" if own else "02",
                           "src": "06" if r.random() < 0.74 else "04",
                           "mode": "close" if s["kind"] == "gap_close_bg" else "turn", "wid": None,
                           "leaver": s.get("leaver"), "bg": True})
        for p in U.planned:
            if p.get("ref") is not None and p["tag"] == "first":
                pid = P.new(kind="planned", unit=u)
                readmit[p["ref"]] = pid
                adm[u].append({"t": p["t"], "pid": pid, "type": "04", "src": "01", "mode": "turn", "wid": p["wid"],
                               "hold_until": p.get("hold_until"), "planned": True})
        for p in U.planned:
            if p.get("ref") is not None and p["tag"] == "first":
                continue
            if p.get("readmit"):
                pid = readmit[p["ref"]]
            elif u == "STN-ACC":
                # Stennock's planned surgery runs at its elective centre: the patient comes over as a planned transfer
                # in, referred by Stennock from the centre's recovery
                pid = P.new(kind="planned", unit=u, letter="D", ec=True,
                            inside_wid=p.get("wid") if p["tag"] == "inside" else None,
                            booked_wid=p.get("wid") if p["tag"] == "booked" else None,
                            booked_arrive=p.get("arrive"))
            else:
                pid = P.new(kind="planned", unit=u)
            typ = "03" if u == "STN-ACC" and not p.get("readmit") else "04"
            adm[u].append({"t": p["t"], "pid": pid, "type": typ, "src": "01", "mode": "turn", "wid": p.get("wid"),
                           "hold_until": p.get("hold_until"), "planned": True})
        for f in U.forced:
            adm[u].append({"t": f["t"], "pid": None, "mode": "forced", "leaver_pid": readmit[f["pid"]]})
    # the winter unit opens with three admissions and closes with three step-downs
    for t in PEL_FILL:
        pid = P.new(kind="bg", letter="H", level=3, unit="PEL-W3")
        adm["PEL-W3"].append({"t": t, "pid": pid, "type": "01", "src": "06", "mode": "close", "wid": None, "bg": True})
    for t in PEL_CLOSE:
        adm["PEL-W3"].append({"t": t, "pid": None, "mode": "gap_open"})
    for u, U in world.units.items():
        for g in U.gaps:
            if g["kind"] in ("cmorning", "own", "spe", "dv4", "dv5"):
                adm[u].append({"t": g["open"], "pid": None, "mode": "gap_open"})
        for s in U.swaps:
            adm[u].append({"t": s["t"], "pid": None, "mode": "swap", "need": s["need"], "ref": s["ref"]})
    return adm


def target_los(P, pid, r, world):
    p = P.p[pid]
    if p["kind"] == "planned":
        return max(14 * 60, int(np.exp(r.normal(np.log(1.4 * 1440), 0.45))))
    if p["kind"] == "wait":
        w = world.waits_by_id[p["wid"]]
        if w["died"]:
            return int(r.integers(1 * 1440, 6 * 1440))
        return max(20 * 60, int(np.exp(r.normal(np.log(4.5 * 1440), 0.6))))
    if p.get("level") == 2:
        return max(12 * 60, int(np.exp(r.normal(np.log(2.2 * 1440), 0.5))))
    return max(16 * 60, int(np.exp(r.normal(np.log(3.8 * 1440), 0.65))))


def simulate(world, P):
    adm = assign_admissions(world, P)
    stays = []        # dicts: unit, pid, admit, discharge, type, src, rows=[(a, b)]
    for u in FEED_UNITS:
        r = rng("sim", u)
        N = BEDS[u]
        occ = {}

        def admit(t, pid, a):
            assert pid not in occ, ("a patient admitted twice to one unit", u, pid)
            occ[pid] = {"pid": pid, "unit": u, "admit": t, "target": t + target_los(P, pid, r, world),
                        "type": a.get("type", "01"), "src": a.get("src", "06"), "rows": [], "row0": t,
                        "hold": a.get("hold_until") or 0, "deadline": None}
            p = P.p[pid]
            if p["kind"] == "wait":
                w = world.waits_by_id[a["wid"] if a.get("wid") is not None else p["wid"]]
                if w["died"] and w["outcome"] == "admitted":
                    occ[pid]["deadline"] = w["dta"] + w.get("deadline_days", 19) * 1440

        def leave(t, pid=None):
            if pid is None:
                cands = [o for o in occ.values() if o["hold"] <= t and t - o["admit"] >= 240]
                if not cands:
                    cands = [o for o in occ.values() if o["hold"] <= t]
                assert cands, (u, t)
                urgent = [o for o in cands if o["deadline"] is not None and o["deadline"] <= t + 18 * 60]
                if urgent:
                    o = min(urgent, key=lambda o: o["deadline"])
                else:
                    o = min(cands, key=lambda o: (o["target"], o["pid"]))
            else:
                o = occ[pid]
            o["rows"].append((o["row0"], t))
            stays.append({"unit": u, "pid": o["pid"], "admit": o["admit"], "discharge": t, "type": o["type"],
                          "src": o["src"], "rows": o["rows"]})
            del occ[o["pid"]]

        # initial occupants (admitted in May 2023) for units open at the start of the feed
        t0 = lm(FEED0, 0, 0)
        if u != "PEL-W3":
            for i in range(N):
                pid = P.new(kind="initial", unit=u)
                a = t0 - int(r.integers(6 * 60, 12 * 1440))
                occ[pid] = {"pid": pid, "unit": u, "admit": a, "target": t0 + int(r.integers(4 * 60, 9 * 1440)),
                            "type": "01", "src": "06", "rows": [], "row0": a, "hold": 0, "deadline": None}
                P.p[pid]["admit"] = a
        order = {"forced": 0, "gap_open": 1, "turn": 2, "swap": 3, "close": 4}
        evs = sorted(adm[u], key=lambda a: (a["t"], order[a["mode"]], a.get("pid") or -1))
        for a in evs:
            t = a["t"]
            m = a["mode"]
            if m == "forced":
                # a named patient leaves for theatre; the bed is assigned the same minute below
                leave(t, a["leaver_pid"])
                continue
            if m == "gap_open":
                leave(t)
                continue
            if m == "swap":
                cands = [o for o in occ.values() if t - o["row0"] >= 120]
                if a["need"] == "planned":
                    first = [o for o in cands if o["type"] == "04"]
                    assert first, ("no planned patient present for a bed move", u, t)
                    o1 = sorted(first, key=lambda o: o["pid"])[0]
                else:
                    if len(cands) < 2:
                        continue
                    o1 = cands[int(r.integers(len(cands)))]
                rest = [o for o in cands if o is not o1 and (a["need"] == "planned" or o["type"] not in ("03", "04"))]
                if not rest:
                    continue
                o2 = rest[int(r.integers(len(rest)))]
                if a["need"] is None and (o1["type"] in ("03", "04") or o2["type"] in ("03", "04")):
                    continue
                for o in (o1, o2):
                    o["rows"].append((o["row0"], t))
                    o["row0"] = t
                world.swaps_done.append({"unit": u, "t": t, "pids": (o1["pid"], o2["pid"]), "ref": a["ref"]})
                continue
            if m == "turn":
                if a.get("leaver_pid") is None and len(occ) < N:
                    raise AssertionError("turnover with an empty bed: %s %s" % (u, t))
                if len(occ) >= N:
                    leave(t)
                admit(t, a["pid"], a)
                continue
            if m == "close":
                assert len(occ) < N, ("gap close into a full unit", u, t)
                admit(t, a["pid"], a)
                continue
        # remaining occupants leave after the unit's last admission (the feed's end, or the unit's change of level)
        last = max([a["t"] for a in evs] + [0])
        for o in sorted(occ.values(), key=lambda o: o["pid"]):
            if u == "ELL-ACC":
                t = max(o["target"], last + 60 + int(r.integers(0, 2880)))
            else:
                t = min(max(o["target"], END_OF_FEED + 60), LAST_DISCHARGE - int(r.integers(0, 600)))
            t = max(t, o["admit"] + 240)
            o["rows"].append((o["row0"], t))
            stays.append({"unit": u, "pid": o["pid"], "admit": o["admit"], "discharge": t, "type": o["type"],
                          "src": o["src"], "rows": o["rows"]})
    designed = {(x["unit"], x["t"]) for x in world.swaps_done if x["ref"] is not None}
    for st in stays:
        rows = st["rows"]
        if len(rows) < 2:
            continue
        out = [rows[0]]
        for a, b in rows[1:]:
            if b - a < 90 and (st["unit"], a) not in designed:
                out[-1] = (out[-1][0], b)
            else:
                out.append((a, b))
        st["rows"] = out
    return stays, adm
