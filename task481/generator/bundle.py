"""task481 bundle: the department's records as its systems hold them, built from the simulation. Report times become
local and UTC stamps, incidents get the numbers each system gave them, the Return A forms are tallied by month reported,
the October to December 2024 victims carry the clerks' summary class beside their NIBRS offense, and the Domestic
Violence Unit logs every domestic victim it receives."""
import collections
import datetime as dt

import numpy as np

import sim as S
import world as W

UTC = dt.timezone.utc
REFORMAT = dt.datetime(2025, 3, 17, 6, 0)     # the records system's numbering change, local time

RA_LINES = ("1A", "1B", "2", "3A", "3B", "3C", "3D", "4A", "4B", "4C", "4D", "4E", "5A", "5B", "5C", "6", "7A", "7B",
            "7C")
CLEAR = {"1A": 0.56, "1B": 0.80, "2": 0.30, "3A": 0.24, "3B": 0.30, "3C": 0.28, "3D": 0.27, "4A": 0.38, "4B": 0.58,
         "4C": 0.55, "4D": 0.62, "4E": 0.48, "5A": 0.11, "5B": 0.13, "5C": 0.10, "6": 0.13, "7A": 0.09, "7B": 0.11,
         "7C": 0.10}
JUV = {"1A": 0.08, "1B": 0.05, "2": 0.14, "3A": 0.18, "3B": 0.15, "3C": 0.15, "3D": 0.22, "4A": 0.10, "4B": 0.11,
       "4C": 0.12, "4D": 0.16, "4E": 0.15, "5A": 0.16, "5B": 0.12, "5C": 0.14, "6": 0.17, "7A": 0.20, "7B": 0.18,
       "7C": 0.19}
DVU_REL = {"BG": "Intimate partner (current)", "SE": "Intimate partner (current)", "CS": "Intimate partner (current)",
           "XR": "Intimate partner (former)", "XS": "Intimate partner (former)", "PA": "Parent or guardian",
           "SP": "Parent or guardian", "CH": "Child", "SC": "Child", "CF": "Child", "SB": "Sibling", "SS": "Sibling",
           "GP": "Other family or household", "GC": "Other family or household", "IL": "Other family or household",
           "OF": "Other family or household"}
LEGACY_DESC = {"4A": "AGG ASSLT - FIREARM", "4B": "AGG ASSLT - KNIFE/CUTTING INST", "4C": "AGG ASSLT - OTHER WEAPON",
               "4D": "AGG ASSLT - HANDS/FISTS/FEET", "4E": "OTHER ASSLT - SIMPLE"}
NIBRS_DESC = {"13A": "Aggravated Assault", "13B": "Simple Assault", "13C": "Intimidation", "90Z": "All Other Offenses",
              "290": "Destruction/Damage/Vandalism of Property", "220": "Burglary/Breaking & Entering"}


def to_utc(local_naive):
    return local_naive.replace(tzinfo=W.TZ).astimezone(UTC)


def ym(d):
    return d.year, d.month


class Bundle:
    def __init__(self, seed=W.SEED):
        self.seed = seed
        self.victims, self.incidents = S.simulate(seed)
        self.others = S.other_offenses(seed)
        self.inc = {i["iid"]: i for i in self.incidents}
        self.township = self._township(np.random.default_rng(seed * 17 + 9))
        self.notes = self._notes(np.random.default_rng(seed * 19 + 3))
        r = np.random.default_rng(seed * 11 + 5)
        self._number_incidents(r)
        self._dvu(np.random.default_rng(seed * 13 + 7))

    # ------------------------------------------------------------------ numbering
    @staticmethod
    def _township(r):
        """Shootings the department attended in North Ellsmere Township, which it patrols under contract and reports
        under the township's own identifier: at least one a quarter at a handful of addresses beyond the city line."""
        out = []
        for y in range(2023, 2027):
            for q in range(4):
                if (y, q) > (2026, 2):
                    break
                start = dt.datetime(y, 3 * q + 1, 1)
                days = ((dt.datetime(y + (q == 3), (3 * q + 3) % 12 + 1, 1)) - start).days
                for _ in range(1 + int(r.poisson(1.8))):
                    at = start + dt.timedelta(days=int(r.integers(0, days)), hours=int(r.choice(
                        [0, 1, 2, 3, 13, 15, 17, 18, 19, 20, 21, 22, 23])), minutes=int(r.integers(0, 60)))
                    out.append({"occurred": at, "reported": at + dt.timedelta(minutes=int(r.integers(2, 25))),
                                "victims": int(r.choice([1, 1, 1, 1, 1, 1, 2, 2, 3]))})
        out.sort(key=lambda t: t["reported"])
        for k, t in enumerate(out):
            t["iid"] = ("T", k)
        return out

    @staticmethod
    def _notes(r):
        """Reports the records system numbers that carry no offense (hospital notifications, found property, welfare
        checks), so they are not in the extract: a couple of hours apart through every day."""
        out = []
        t = dt.datetime(2021, 1, 1, 0, 0)
        end = dt.datetime(2026, 9, 30, 23, 59)
        while True:
            t = t + dt.timedelta(minutes=int(r.integers(20, 200)))
            if t > end:
                break
            out.append({"reported": t})
        return out

    def _number_incidents(self, r):
        """Legacy numbers YY-NNNNNN in report order each year; the new system's EPyy-NNNNN until its March 2025 upgrade
        and yyyy-NNNNNN after it, every incident it held renumbered to the new form."""
        go = dt.datetime(W.GO_LIVE.year, W.GO_LIVE.month, W.GO_LIVE.day)
        items = [(i["reported"], "A", i["iid"]) for i in self.incidents]
        items += [(o["reported"], "O", n) for n, o in enumerate(self.others)]
        items += [(t["reported"], "T", k) for k, t in enumerate(self.township)]
        items += [(t["reported"], "N", k) for k, t in enumerate(self.notes)]
        items.sort()
        seq_legacy, seq_new = collections.Counter(), collections.Counter()
        for rep, typ, key in items:
            if rep < go:
                seq_legacy[rep.year] += 1 + int(r.integers(0, 3))
                num = "%02d-%06d" % (rep.year % 100, 10000 + seq_legacy[rep.year])
                old = None
            else:
                seq_new[rep.year] += 1
                num = "%d-%06d" % (rep.year, seq_new[rep.year])
                old = ("EP%02d-%05d" % (rep.year % 100, seq_new[rep.year])) if rep < REFORMAT else None
            target = {"A": self.inc, "O": self.others, "T": self.township, "N": self.notes}[typ][key]
            target["number"], target["old_number"] = num, old

    # ------------------------------------------------------------------ views
    def active(self):
        """Victims whose incident was not unfounded."""
        return [v for v in self.victims if not self.inc[v["iid"]]["unfounded"]]

    def reported(self, v):
        return self.inc[v["iid"]]["reported"]

    def return_a(self):
        """{(year, month): {line: [reported, unfounded, actual, cleared, cleared_juvenile]}} for 2021 to 2024, by month
        reported. Assault lines count victims; robbery counts incidents; homicide counts victims."""
        r = np.random.default_rng(self.seed * 17 + 1)
        tally = collections.defaultdict(lambda: collections.Counter())
        for v in self.victims:
            if v["kind"] in ("rob_extra", "hom_extra"):
                continue
            rep = self.reported(v)
            if rep.year < W.FIRST_YEAR or rep.year > 2024:
                continue
            key = ym(rep)
            tally[key][(v["line"], "rep")] += 1
            if self.inc[v["iid"]]["unfounded"]:
                tally[key][(v["line"], "unf")] += 1
        for o in self.others:
            rep = o["reported"]
            if not o["line"] or rep.year < W.FIRST_YEAR or rep.year > 2024:
                continue
            tally[ym(rep)][(o["line"], "rep")] += 1
            if o["unfounded"]:
                tally[ym(rep)][(o["line"], "unf")] += 1
        out = {}
        for key in sorted(tally):
            if key[0] < W.FIRST_YEAR:
                continue
            row = {}
            for line in RA_LINES:
                rep = tally[key][(line, "rep")]
                unf = tally[key][(line, "unf")]
                act = rep - unf
                cl = int(r.binomial(act, CLEAR[line])) if act else 0
                juv = int(r.binomial(cl, JUV[line])) if cl else 0
                row[line] = [rep, unf, act, cl, juv]
            out[key] = row
        return out

    # ------------------------------------------------------------------ the Domestic Violence Unit
    def _dvu(self, r):
        rows = []
        for v in self.victims:
            if not v["dv"]:
                continue
            i = self.inc[v["iid"]]
            rows.append({"v": v, "inc": i, "kind": "assault"})
        for o in self.others:
            if o["dv"]:
                rows.append({"v": None, "inc": o, "kind": o["code"]})
        rows.sort(key=lambda d: (d["inc"]["reported"], d["inc"]["number"]))
        self.dvu = rows
