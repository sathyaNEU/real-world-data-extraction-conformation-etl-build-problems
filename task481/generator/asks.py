"""task481 asks, built on the simulation's victims.

A. The Gun Violence Reduction Unit's shooting log (every person struck by gunfire the department attended) and the
   Medical Examiner's homicide list. The log moved into the new records system on 1 October 2024 with everything
   before it. The old database's analyst updated a victim's outcome when the Medical Examiner's list showed the death
   within the unit's 30-day review of the shooting; the new system records the outcome when the shooting is entered,
   so a victim shot from October 2024 who died days or weeks later stays WOUNDED, and so does one who died more than
   30 days after an earlier shooting or after the move. The old database marked a shooting
   inside the city by the patrol beat, and the department's beats include North Ellsmere Township, which it patrols
   under contract; the new system marks it from the address, so the same township blocks are Y before October 2024
   and N, with the township named, after it. When the department moved records systems, the summer 2024 shootings
   still under investigation were entered again under the same report number. A few multi-victim shootings carry one
   report per victim.
B. The State UCR Program's repository as it stood at its 2025 data freeze (13 March 2026, 23:59 state time), which its
   published 2025 figure counts: aggravated assault victims by the incident date submitted. The department counts by
   month reported, from its October 2026 extract. Between them: report and occurrence years, acceptance after the
   freeze, deletions after it, offenses changed after it, and incidents the state holds twice because the March 2025
   renumbering re-sent open incidents under their new numbers without deleting the old."""
import bisect
import collections
import datetime as dt

import numpy as np

import bundle as B

FREEZE = dt.datetime(2026, 3, 13, 23, 59, 59)
REFORMAT = B.REFORMAT
GUNS = ("11", "12", "13", "15")
STREETS = ("MAPLE AVE", "CEDAR ST", "LINCOLN BLVD", "RIVER RD", "MARKET ST", "OAK ST", "PARK AVE", "WASHINGTON ST",
           "ELM ST", "HIGHLAND DR", "MILL ST", "CHURCH ST", "GRAND AVE", "UNION ST", "LAKE ST", "SPRING ST",
           "FRANKLIN AVE", "BROAD ST", "WALNUT ST", "PINE ST", "COLLEGE AVE", "DIVISION ST", "PROSPECT AVE",
           "HARRISON ST", "FULTON ST", "ASH ST", "KING DR", "BELMONT AVE")
OTHER_TOWNS = ("BRAYLEY", "NORTH ELLSMERE TWP", "CASSEL", "WYNTON")
TOWNSHIP = "NORTH ELLSMERE TWP"
TOWNSHIP_BLOCKS = ("4810 BLOCK N HIGHLAND DR", "4920 BLOCK N HIGHLAND DR", "5130 BLOCK RIVER RD",
                   "4870 BLOCK N MARKET ST", "5040 BLOCK MILL ST", "4950 BLOCK N PROSPECT AVE", "5210 BLOCK LAKE ST")
OUT_TOWNS = ("BRAYLEY", "CASSEL", "WYNTON")
MIGRATION = dt.datetime(2024, 10, 1)


def quarter(d):
    return "%dQ%d" % (d.year, (d.month - 1) // 3 + 1)


QUARTERS = tuple("%dQ%d" % (y, q) for y in (2023, 2024, 2025) for q in (1, 2, 3, 4))


class Shootings:
    def __init__(self, b):
        r = np.random.default_rng(b.seed * 29 + 11)
        self.r = r
        people = []
        for v in b.victims:
            inc = b.inc[v["iid"]]
            at = inc["occurred"]
            if at < dt.datetime(2023, 1, 1) or at > dt.datetime(2026, 9, 30, 23, 59):
                continue
            if v["weapon"] not in GUNS:
                continue
            struck = (v["kind"] in ("fire_hit", "hom_extra")
                      or (v["kind"] == "rob_extra" and v["injury"] not in ("N", "M"))
                      or (v["kind"] == "dv_weapon" and v["injury"] in ("B", "L", "I", "U", "T", "O")))
            if v["kind"] == "homicide":
                people.append({"v": v, "inc": inc, "at": at, "circ": "ASSAULT", "dead": True})
            elif struck:
                people.append({"v": v, "inc": inc, "at": at, "circ": "ASSAULT", "dead": False})
        for y in range(2023, 2027):
            for m in range(1, 13):
                if (y, m) > (2026, 9):
                    break
                for circ, lam in (("SELF-INFLICTED", 3.4), ("UNINTENTIONAL", 2.1), ("POLICE", 0.45)):
                    for _ in range(int(r.poisson(lam))):
                        at = dt.datetime(y, m, int(r.integers(1, 29)), int(r.integers(0, 24)), int(r.integers(0, 60)))
                        dead = r.random() < (0.55 if circ == "SELF-INFLICTED" else (0.3 if circ == "POLICE" else 0.08))
                        people.append({"v": None, "inc": None, "at": at, "circ": circ, "dead": bool(dead),
                                       "age": int(np.clip(r.gamma(5, 6) + 10, 12, 85)),
                                       "sex": "M" if r.random() < 0.82 else "F"})
        tr = np.random.default_rng(b.seed * 47 + 23)
        post = [t for t in b.township if t["occurred"] >= MIGRATION]
        for t in b.township:
            # every block the township's shootings come from before the move recurs after it
            first = [i for i, u in enumerate(post[:len(TOWNSHIP_BLOCKS)]) if u is t]
            block = (TOWNSHIP_BLOCKS[first[0]] if first else
                     TOWNSHIP_BLOCKS[int(tr.choice(len(TOWNSHIP_BLOCKS), p=[0.24, 0.12, 0.18, 0.14, 0.12, 0.10, 0.10]))])
            ages = set()
            for j in range(t["victims"]):
                age = int(np.clip(tr.gamma(4.2, 5.5) + 13, 14, 70))
                while age in ages:
                    age += 1
                ages.add(age)
                dead = bool(tr.random() < 0.13)
                people.append({"v": None, "inc": t, "at": t["occurred"], "circ": "ASSAULT", "dead": dead, "age": age,
                               "sex": "M" if tr.random() < 0.86 else "F", "township": True, "tblock": block})
        people.sort(key=lambda p: (p["at"], p["v"]["age"] if p["v"] else p["age"]))
        # who died later: a share of the dead were alive when the shooting was logged
        blocks, used = {}, {True: set(TOWNSHIP_BLOCKS), False: set(TOWNSHIP_BLOCKS)}
        for p in people:
            if p["v"] is not None:
                p["age"], p["sex"] = p["v"]["age"], p["v"]["sex"]
            p["later"] = bool(p["dead"] and r.random() < (0.36 if p["circ"] == "ASSAULT" else 0.15))
            p["death"] = (p["at"] + dt.timedelta(days=int(r.integers(1, 58)), hours=int(r.integers(0, 20)))
                          if p["later"] else (p["at"] + dt.timedelta(minutes=int(r.integers(5, 95))) if p["dead"] else None))
            key = p["inc"]["iid"] if p["inc"] else ("x", id(p))
            p.setdefault("township", False)
            if key not in blocks:
                # the place belongs to the shooting: everyone struck in it was struck there, and a block is in the city
                # or out of it whoever is shot on it
                inside = (not p["township"]) and (r.random() < 0.96 if p["inc"] is None else r.random() >= 0.026)
                block = p["tblock"] if p["township"] else self._block()
                while not p["township"] and block in used[not inside]:
                    block = self._block()
                used[inside].add(block)
                blocks[key] = (block, inside)
            p["block"], p["inside"] = blocks[key]
            p["town"] = TOWNSHIP if p["township"] else OUT_TOWNS[sum(map(ord, p["block"])) % 3]
        # after the move, a few victims in every quarter who were shot in the evening died days later
        fr = np.random.default_rng(b.seed * 53 + 31)
        size = collections.Counter(p["inc"]["iid"] for p in people if p["inc"] is not None)
        for q in ("2024Q4", "2025Q1", "2025Q2", "2025Q3", "2025Q4"):
            cand = [p for p in people if p["circ"] == "ASSAULT" and p["inside"] and p["dead"] and p["inc"] is not None
                    and quarter(p["at"]) == q and p["at"] >= MIGRATION and 19 <= p["at"].hour <= 23
                    and size[p["inc"]["iid"]] == 1]
            need = max(0, 3 - sum(1 for c in cand if c["later"]))
            for p in [c for c in cand if not c["later"]][:need]:
                p["later"] = True
                p["death"] = p["at"] + dt.timedelta(days=int(fr.integers(2, 40)), hours=int(fr.integers(0, 20)))
        self.people = people
        self._log(b)
        self._me()

    def _block(self):
        r = self.r
        return "%d%02d BLOCK %s%s" % (int(r.integers(1, 48)), int(r.integers(0, 10)) * 10,
                                      ("N ", "S ", "E ", "W ", "")[int(r.integers(0, 5))],
                                      STREETS[int(r.integers(0, len(STREETS)))])

    def _log(self, b):
        r = self.r
        rows = []
        for p in self.people:
            inc = p["inc"]
            number = ""
            if inc is not None:
                number = inc["old_number"] if (inc.get("old_number") and p["at"] < REFORMAT) else inc["number"]
            # the old database's analyst marked a death as the Medical Examiner reported it while the shooting was on
            # the unit's 30-day review, up to the move; the new system keeps the outcome entered with the shooting
            known = p["dead"] and (not p["later"] or (p["death"] < MIGRATION
                                                      and p["death"] - p["at"] <= dt.timedelta(days=30)))
            rows.append({"p": p, "number": number, "entered": p["at"] + dt.timedelta(hours=int(r.integers(5, 70))),
                         "outcome": "DECEASED" if known else "WOUNDED", "kind": "first"})
        # one report per victim: in some multi-victim shootings a later victim carries its own report number
        by_inc = collections.defaultdict(list)
        for row in rows:
            if row["p"]["inc"] is not None:
                by_inc[row["p"]["inc"]["iid"]].append(row)
        # the later victim's own report is the hospital notification the records system numbered when it came in
        note_at = [n_["reported"] for n_ in b.notes]
        used = set()
        for iid, grp in by_inc.items():
            if len(grp) > 1 and r.random() < 0.35:
                row = grp[-1]
                rep = row["p"]["inc"]["reported"] + dt.timedelta(minutes=15)
                k = bisect.bisect_left(note_at, rep)
                while k in used:
                    k += 1
                used.add(k)
                note = b.notes[k]
                row["number"] = note["old_number"] if (note.get("old_number") and rep < REFORMAT) else note["number"]
                row["kind"] = "split"
        # the summer 2024 shootings still under investigation entered again when the case moved to the new system,
        # under the same report number
        again = []
        for row in rows:
            p = row["p"]
            if (p["inc"] is not None and not p["township"] and dt.datetime(2024, 7, 1) <= p["at"] < MIGRATION
                    and not (p["dead"] and not p["later"]) and r.random() < 0.24):
                entered = dt.datetime(2024, 10, 2) + dt.timedelta(days=int(r.integers(0, 55)), hours=int(r.integers(8, 17)))
                again.append({"p": p, "number": row["number"], "entered": entered, "outcome": "WOUNDED",
                              "kind": "again"})
        rows += again
        rows.sort(key=lambda row: (row["entered"], row["p"]["at"]))
        seq = collections.Counter()
        for row in rows:
            seq[row["entered"].year] += 1
            row["gvr"] = "GVR-%d-%04d" % (row["entered"].year, seq[row["entered"].year])
        self.log = rows

    def _me(self):
        """The Medical Examiner's homicide list for the county: every death by another's hand (police shootings
        included), by date of death, with the date and place of injury."""
        r = self.r
        rows = []
        for p in self.people:
            if not p["dead"] or p["circ"] in ("SELF-INFLICTED", "UNINTENTIONAL"):
                continue
            rows.append({"p": p, "cause": "GUNSHOT WOUND(S)"})
        # homicides by other means and outside the city, which the list also carries
        for y in range(2023, 2027):
            for m in range(1, 13):
                if (y, m) > (2026, 9):
                    break
                for cause, lam in (("SHARP FORCE INJURIES", 0.9), ("BLUNT FORCE INJURIES", 0.7), ("ASPHYXIA", 0.2),
                                   ("GUNSHOT WOUND(S)", 0.8)):
                    for _ in range(int(r.poisson(lam))):
                        at = dt.datetime(y, m, int(r.integers(1, 29)), int(r.integers(0, 24)), int(r.integers(0, 60)))
                        rows.append({"p": {"at": at, "death": at + dt.timedelta(hours=int(r.integers(0, 30))),
                                           "age": int(np.clip(r.gamma(5.5, 6) + 8, 1, 90)),
                                           "sex": "M" if r.random() < 0.8 else "F",
                                           "block": None, "inside": cause != "GUNSHOT WOUND(S)" and r.random() < 0.5,
                                           "town": OTHER_TOWNS[int(r.integers(0, len(OTHER_TOWNS)))]},
                                     "cause": cause})
        rows.sort(key=lambda row: row["p"]["death"])
        self.me = rows

    def truth(self):
        """Non-fatal shooting victims (struck in an assault in the city, survived) and the shootings they were hurt in,
        by quarter shot."""
        vic, shoot = collections.Counter(), collections.defaultdict(set)
        for p in self.people:
            if p["circ"] != "ASSAULT" or not p["inside"] or p["dead"]:
                continue
            q = quarter(p["at"])
            vic[q] += 1
            shoot[q].add(p["inc"]["iid"])
        return {q: vic[q] for q in QUARTERS}, {q: len(shoot[q]) for q in QUARTERS}


class StateFreeze:
    """The state repository at the freeze and the reconciliation's lines."""

    def __init__(self, b):
        r = np.random.default_rng(b.seed * 31 + 3)
        self.b = b
        lines = collections.Counter()
        snap = []
        dept = 0
        go = dt.datetime(2024, 10, 1)
        by_inc = collections.defaultdict(list)
        for v in b.victims:
            by_inc[v["iid"]].append(v)
        meta = {}
        for iid, vs in by_inc.items():
            inc = b.inc[iid]
            rep, occ = inc["reported"], inc["occurred"]
            if rep < go or rep > dt.datetime(2026, 9, 30, 23, 59, 59):
                continue
            # first acceptance by the state: approval lag, a few backlogged, a few rejected and corrected later; the
            # backlog, the deletions and the re-sending touch only incidents that occurred and were reported in 2025
            both = occ.year == 2025 and rep.year == 2025
            u = r.random()
            accept = rep + dt.timedelta(days=int(r.integers(1, 13)), hours=int(r.integers(0, 10)))
            rejected = False
            if both and u < 0.03:
                accept = rep + dt.timedelta(days=int(r.integers(40, 260)))
            elif both and u < 0.055:
                rejected = True
                accept = rep + dt.timedelta(days=int(r.integers(12, 220)))
            unfound = None
            if inc["unfounded"]:
                unfound = rep + dt.timedelta(days=int(r.integers(8, 250)))
                if not both or accept > FREEZE:
                    unfound = min(unfound, FREEZE - dt.timedelta(days=1)) if accept <= FREEZE else unfound
            meta[iid] = {"accept": accept, "rejected": rejected, "unfound": unfound, "both": both,
                         "resent": bool(both and rep < REFORMAT and accept < REFORMAT and not inc["unfounded"]
                                        and r.random() < 0.08)}
        self.meta = meta
        # offenses changed after first submission: a few aggravated assaults downgraded, a few simple assaults upgraded
        change = {}
        for iid, vs in by_inc.items():
            if iid not in meta:
                continue
            mt = meta[iid]
            if not mt["both"] or mt["resent"] or b.inc[iid]["unfounded"] or mt["accept"] > FREEZE:
                continue
            for v in vs:
                if v["nibrs"] == "13B" and r.random() < 0.006:
                    change[id(v)] = ("13A", b.inc[iid]["reported"] + dt.timedelta(days=int(r.integers(40, 330))))
                elif v["nibrs"] == "13A" and v["kind"] not in ("rob_extra", "hom_extra") and r.random() < 0.007:
                    change[id(v)] = ("13B", b.inc[iid]["reported"] + dt.timedelta(days=int(r.integers(30, 300))))
        self.change = change
        self.rows = []
        for iid, vs in by_inc.items():
            if iid not in meta:
                continue
            inc, mt = b.inc[iid], meta[iid]
            rep, occ = inc["reported"], inc["occurred"]
            for seq, v in enumerate(vs, 1):
                was = v["nibrs"]
                if id(v) in change and change[id(v)][1] > FREEZE:
                    was = change[id(v)][0]
                in_state = (occ.year == 2025 and was == "13A" and mt["accept"] <= FREEZE
                            and not (mt["unfound"] is not None and mt["unfound"] <= FREEZE))
                in_dept = (rep.year == 2025 and v["nibrs"] == "13A" and not inc["unfounded"])
                if in_dept:
                    dept += 1
                if in_state:
                    number = inc["old_number"] if (inc.get("old_number") and mt["accept"] < REFORMAT) else inc["number"]
                    snap.append((inc, seq, v, number, mt["accept"]))
                    if mt["resent"]:
                        snap.append((inc, seq, v, inc["number"], REFORMAT + dt.timedelta(hours=int(r.integers(1, 30)))))
                        lines["held twice"] += 1
                # the reason each victim is on one side only
                if in_state and not in_dept:
                    if rep.year == 2026:
                        lines["reported in 2026"] += 1
                    elif inc["unfounded"]:
                        lines["deleted after the freeze"] += 1
                    elif v["nibrs"] != "13A":
                        lines["no longer aggravated"] += 1
                    else:
                        lines["?state"] += 1
                elif in_dept and not in_state:
                    if occ.year < 2025:
                        lines["occurred before 2025"] += 1
                    elif mt["accept"] > FREEZE:
                        lines["accepted after the freeze"] += 1
                    elif was != "13A":
                        lines["aggravated only after the freeze"] += 1
                    else:
                        lines["?dept"] += 1
        self.snapshot = sorted(snap, key=lambda t: (t[4], t[0]["number"], t[1]))
        self.dept = dept
        self.published = len(snap)
        self.lines = lines
