"""Everything the generator draws, in memory, from fixed random streams: the households the region's homeless services
served across FY2025 and FY2026, the identity each source holds for each person, every activity row (HMIS enrollments,
exits, move-ins and night-by-night bed nights, the coalition's shelter stays, the clinic's encounters, the outreach
team's contacts), and the State Data Linkage Unit's comparisons of records from different sources with per-field
agreement, scores and findings.

Identity (names, full dates of birth, the last four of a Social Security number) never ships: the sources sent it hashed
to the unit, and the pack carries record keys, birth years, codes and dates. So the generator may tune identity to keep
the world honest: every person's records link to one another, and every finding that joins two different people sits
where a source's own one-record-per-person grain shows it (a record linked to two clients one source keeps apart). A
wrong join nothing in the files could reveal would leave the people served unknowable, so it is redrawn."""
import collections
import datetime as dt
import itertools

import numpy as np

import names as N
import world as W

DAY = dt.timedelta(days=1)
NICK = {"Robert": "Bob", "William": "Bill", "James": "Jim", "Michael": "Mike", "Richard": "Rick", "Joseph": "Joe",
        "Thomas": "Tom", "Charles": "Charlie", "Christopher": "Chris", "Daniel": "Danny", "Anthony": "Tony",
        "Elizabeth": "Liz", "Jennifer": "Jen", "Katherine": "Kathy", "Patricia": "Pat", "Margaret": "Peggy",
        "Jessica": "Jess", "Rebecca": "Becky", "Deborah": "Debbie", "Kimberly": "Kim", "Jose": "Pepe",
        "Francisco": "Paco", "Guadalupe": "Lupe", "Jesus": "Chuy", "Eduardo": "Lalo", "Alejandro": "Alex",
        "Roberto": "Beto", "Ignacio": "Nacho", "Enrique": "Kike", "Rosa": "Rosie", "Maria": "Mari", "Ana": "Anita",
        "Manuel": "Manny", "Antonio": "Tony", "Gerardo": "Jerry", "Guillermo": "Memo", "Ricardo": "Rick",
        "Fernando": "Nando", "Javier": "Javi", "Ramon": "Moncho"}
CHILD_F = ("Sophia", "Isabella", "Mia", "Emma", "Camila", "Valentina", "Olivia", "Ava", "Aaliyah", "Mila",
           "Ximena", "Natalia", "Zoe", "Layla", "Luna", "Aria", "Nevaeh", "Abigail", "Emily", "Victoria")
CHILD_M = ("Liam", "Noah", "Mateo", "Santiago", "Ethan", "Elijah", "Jayden", "Sebastian", "Aiden", "Lucas",
           "Diego", "Leonardo", "Josiah", "Isaiah", "Gael", "Julian", "Adrian", "Dylan", "Angel", "Jacob")

# HMIS project types (FY2024 and later data standards): 0 ES entry/exit, 1 ES night by night, 2 TH, 3 PSH, 4 SO, 8 SH,
# 13 RRH
PROJECTS = {
    "CAL": [(1012, 0, "Calvera Mission Men's Shelter"), (1015, 0, "Harbor Street Family Shelter"),
            (1019, 0, "Lantern House Women's Shelter"), (1023, 0, "Calvera Navigation Center"),
            (1027, 1, "Calvera Winter Respite"), (1031, 4, "Calvera County Street Outreach"),
            (1034, 4, "Downtown Outreach Collaborative"), (1038, 8, "Riverside Safe Haven"),
            (1042, 2, "New Hope Transitional Housing"), (1046, 2, "Second Street Youth Transitional"),
            (1051, 13, "Calvera Rapid Re-Housing"), (1055, 13, "Families First Rapid Re-Housing"),
            (1058, 13, "Calvera Veterans Rapid Re-Housing"), (1062, 3, "Ridgeway Apartments"),
            (1066, 3, "Calvera Scattered Site Supportive Housing"), (1069, 3, "Mercy Commons")],
    "MAR": [(311, 0, "Mardell County Shelter"), (314, 0, "Lighthouse Family Shelter"), (318, 4, "Mardell Outreach"),
            (322, 2, "Gateway Transitional Housing"), (326, 13, "Mardell Rapid Re-Housing"),
            (329, 13, "Housing Now Rapid Re-Housing"), (333, 3, "Mardell Supportive Housing"),
            (337, 3, "Oak Terrace")],
    "OST": [(5104, 0, "Ostry Emergency Shelter"), (5108, 0, "Ostry Family Center"), (5113, 4, "Ostry Outreach"),
            (5117, 13, "Ostry Rapid Re-Housing"), (5119, 13, "Ostry Youth and Family Rapid Re-Housing"),
            (5121, 3, "Ostry Supportive Housing")],
    "PEL": [(7203, 0, "Pellam Shelter"), (7205, 0, "Pellam Family Shelter"), (7207, 4, "Pellam Outreach"),
            (7211, 13, "Pellam Rapid Re-Housing"), (7213, 13, "Pellam County Rapid Re-Housing (ESG)"),
            (7215, 3, "Pellam Supportive Housing")],
}
TYPE_NAME = {0: "ES", 1: "NBN", 2: "TH", 3: "PSH", 4: "SO", 8: "SH", 13: "RRH"}
LENGTH = {"ES": (3.3, 1.0), "NBN": (3.6, 0.9), "SO": (4.6, 0.8), "TH": (5.3, 0.5), "RRH": (5.2, 0.6),
          "PSH": (6.4, 0.6), "SH": (4.2, 0.8)}      # lognormal stay length in days


def soundex(s):
    s = "".join(c for c in s.upper() if c.isalpha())
    if not s:
        return ""
    codes = {**dict.fromkeys("BFPV", "1"), **dict.fromkeys("CGJKQSXZ", "2"), **dict.fromkeys("DT", "3"), "L": "4",
             **dict.fromkeys("MN", "5"), "R": "6"}
    out, last = s[0], codes.get(s[0], "")
    for c in s[1:]:
        d = codes.get(c, "")
        if d and d != last:
            out += d
        if c not in "HW":
            last = d
    return (out + "000")[:4]


def _pick(rng, lst):
    return lst[0][rng.choice(len(lst[0]), p=lst[1])]


def project_rows():
    out = []
    for coc, items in PROJECTS.items():
        for pid, t, name in items:
            out.append({"id": pid, "coc": coc, "ptype": t, "kind": TYPE_NAME[t], "name": name})
    return out


class World:
    def __init__(self, seed=W.SEED, n_households=24000):
        self.seed = seed
        self.projects = project_rows()
        self.by_kind = collections.defaultdict(list)
        for p in self.projects:
            self.by_kind[(p["coc"], p["kind"])].append(p)
        self.people, self.households = self._people(np.random.default_rng(seed), n_households)
        self._histories(np.random.default_rng(seed + 1))
        self.records = self._records(np.random.default_rng(seed + 2))
        self.tidy()

    # ------------------------------------------------------------------------------------------------ people
    def _person(self, rng, pid, home, sex, hisp, by, role, ln=None, ln2=None):
        if role == "child":
            fn = (CHILD_F if sex == "F" else CHILD_M)[int(rng.integers(20))]
        else:
            fl = (N.HISP_FEMALE if sex == "F" else N.HISP_MALE) if hisp else \
                (N.OTHER_FEMALE if sex == "F" else N.OTHER_MALE)
            fn = _pick(rng, fl)
        ll = N.HISP_LAST if hisp else N.OTHER_LAST
        return {"pid": pid, "home": home, "sex": sex, "hisp": hisp, "fn": fn,
                "ln": ln or _pick(rng, ll), "ln2": ln2 if ln2 is not None else (_pick(rng, ll) if hisp else ""),
                "by": by, "bm": int(rng.integers(1, 13)), "bd": int(rng.integers(1, 29)),
                "ssn4": int(rng.integers(0, 10000)) if rng.random() < (0.66 if role != "child" else 0.45) else None,
                "role": role}

    def _people(self, rng, n_hh):
        hisp_share = {"CAL": 0.68, "MAR": 0.46, "OST": 0.32, "PEL": 0.26}
        coc_w = np.array([0.47, 0.24, 0.17, 0.12])
        people, households = [], []
        for h in range(n_hh):
            home = W.COCS[rng.choice(4, p=coc_w)]
            hisp = rng.random() < hisp_share[home]
            family = rng.random() < 0.13
            sex = "F" if rng.random() < (0.78 if family else 0.30) else "M"
            by = int(np.clip(round(2025 - rng.normal(36 if family else 42, 11 if family else 13.5)), 1938, 2006))
            hoh = self._person(rng, len(people), home, sex, hisp, by, "hoh")
            people.append(hoh)
            members = [hoh["pid"]]
            if family:
                if rng.random() < 0.3:
                    sp = self._person(rng, len(people), home, "M" if sex == "F" else "F", hisp,
                                      int(np.clip(by + rng.integers(-6, 7), 1938, 2006)), "adult", ln=hoh["ln"])
                    people.append(sp)
                    members.append(sp["pid"])
                for c in range(int(1 + rng.poisson(0.9))):
                    cb = int(np.clip(by + 20 + rng.integers(0, 17), 2008, 2025))
                    ch = self._person(rng, len(people), home, "F" if rng.random() < 0.5 else "M", hisp, cb, "child",
                                      ln=hoh["ln"], ln2=hoh["ln2"])
                    people.append(ch)
                    members.append(ch["pid"])
            street = (not family) and rng.random() < (0.46 if home == "CAL" else 0.28)
            dv = rng.random() < ((0.22 if family else 0.07) if sex == "F" else 0.02)
            households.append({"hid": h, "home": home, "family": family, "members": members, "street": street,
                               "dv": dv, "dv_only": dv and rng.random() < 0.55})
            for m in members:
                people[m]["hh"] = h
        return people, households

    # ------------------------------------------------------------------------------------------------ activity
    def _choose(self, rng, coc, kind):
        pool = self.by_kind.get((coc, kind))
        if not pool:
            pool = self.by_kind[(coc, "ES")]
        if kind == "ES" and len(pool) > 1:
            # family households go to the family shelters, single adults to the others
            pass
        return pool[int(rng.integers(len(pool)))]

    def _histories(self, rng):
        last = W.FY26[1]
        span = (last - W.HISTORY_START).days
        enr, beds, dv, enc, con = [], [], [], [], []
        eid = [400000]

        def add(hh, coc, proj, entry, exit_, move_in=None):
            eid[0] += int(rng.integers(1, 9))
            hid = "%s-H%07d" % (coc, eid[0] * 3 + 11)
            for k, m in enumerate(hh["members"]):
                rel = 1 if k == 0 else (3 if self.people[m]["role"] == "adult" else 2)
                enr.append({"eid": eid[0] * 10 + k, "pid": m, "coc": coc, "project": proj["id"],
                            "kind": proj["kind"], "entry": entry, "exit": exit_, "hh_id": hid, "rel": rel,
                            "move_in": move_in if k == 0 else None, "hh": hh["hid"]})
            return eid[0]

        for hh in self.households:
            start = W.HISTORY_START + dt.timedelta(days=int(rng.integers(0, span - 10)))
            hh["start"] = start
            cocs = [hh["home"]]
            if rng.random() < 0.11:
                other = [c for c in W.COCS if c != hh["home"]]
                cocs.append(other[rng.choice(3, p=np.array([0.5, 0.3, 0.2]))])
            k = 0 if hh["dv_only"] else int(min(5, 1 + rng.poisson(0.8)))
            day = start
            force_es = None
            for e in range(k):
                coc = cocs[0] if (len(cocs) == 1 or e == 0 or rng.random() < 0.5) else cocs[1]
                if e == k - 1 and len(cocs) > 1 and all(x["coc"] != cocs[1] for x in enr[-3:]):
                    coc = cocs[1]
                if hh["family"]:
                    kind = rng.choice(["ES", "RRH", "TH", "PSH"], p=[0.48, 0.30, 0.12, 0.10])
                elif hh["street"]:
                    kind = rng.choice(["SO", "ES", "NBN", "SH", "RRH", "PSH"], p=[0.38, 0.27, 0.10, 0.07, 0.12, 0.06])
                else:
                    kind = rng.choice(["ES", "NBN", "TH", "RRH", "PSH", "SO"], p=[0.42, 0.06, 0.13, 0.25, 0.09, 0.05])
                if kind == "NBN" and coc != "CAL":
                    kind = "ES"
                if force_es is not None:
                    coc, kind = force_es, "ES"
                    force_es = None
                proj = self._choose(rng, coc, kind)
                kind = proj["kind"]
                mu, sg = LENGTH[kind]
                length = max(1, int(round(rng.lognormal(mu, sg))))
                entry = day
                if entry > last:
                    break
                exit_ = entry + dt.timedelta(days=length)
                if exit_ > W.PULL - dt.timedelta(days=16):
                    exit_ = None
                move_in = None
                if kind in ("RRH", "PSH"):
                    wait = int(round(rng.lognormal(3.6 if kind == "RRH" else 2.6, 0.7)))
                    if kind == "PSH" and rng.random() < 0.25:
                        wait = 0
                    mi = entry + dt.timedelta(days=wait)
                    if (exit_ is None or mi < exit_) and mi <= last:
                        move_in = mi
                    # a transfer to another rapid re-housing project before the household moves in
                    if kind == "RRH" and move_in is not None and wait > 20 and rng.random() < 0.14:
                        pool = [p for p in self.by_kind[(coc, "RRH")] if p["id"] != proj["id"]]
                        if pool:
                            x = entry + dt.timedelta(days=int(rng.integers(6, wait - 6)))
                            add(hh, coc, proj, entry, x, None)
                            proj = pool[int(rng.integers(len(pool)))]
                            entry = x
                if kind == "NBN":
                    nights = [entry + dt.timedelta(days=d) for d in range(length) if rng.random() < 0.68 or d == 0]
                    nights = [n for n in nights if n <= last]
                    exit_ = nights[-1] + DAY if nights[-1] + dt.timedelta(days=31) <= W.PULL else None
                    eid_ = add(hh, coc, proj, entry, exit_, None)
                    for n in nights:
                        for k2, m in enumerate(hh["members"]):
                            beds.append({"eid": eid_ * 10 + k2, "pid": m, "coc": coc, "date": n})
                else:
                    add(hh, coc, proj, entry, exit_, move_in)
                # a shelter stay left open after the client moved on: the next entry comes before the exit
                gap = int(rng.integers(3, 160))
                if kind == "ES" and exit_ is not None and e < k - 1 and rng.random() < 0.09:
                    gap = -int(rng.integers(1, min(22, length) + 1))
                    force_es = coc
                day = (exit_ or (entry + dt.timedelta(days=length))) + dt.timedelta(days=gap)
            if hh["dv"]:
                d0 = start + dt.timedelta(days=int(rng.integers(-40, 120)))
                for s in range(int(1 + rng.poisson(0.4))):
                    if d0 > last or d0 < W.HISTORY_START:
                        break
                    ln = max(2, int(round(rng.lognormal(3.3, 0.8))))
                    for m in hh["members"]:
                        dv.append({"pid": m, "start": d0, "end": d0 + dt.timedelta(days=ln)})
                    d0 = d0 + dt.timedelta(days=ln + int(rng.integers(20, 300)))
            adult = hh["members"][0]
            if not hh["dv_only"] and rng.random() < (0.36 if hh["street"] else 0.17):
                for v in range(int(1 + rng.poisson(2.2))):
                    d = start + dt.timedelta(days=int(rng.integers(0, 420)))
                    if d <= last:
                        enc.append({"pid": adult, "date": d, "site": self._site(hh, rng),
                                    "status": rng.choice(["Street", "Shelter", "Transitional"], p=[0.5, 0.4, 0.1])})
            if hh["street"] and hh["home"] == "CAL" and not hh["dv_only"] and rng.random() < 0.72:
                for v in range(int(1 + rng.poisson(3.0))):
                    d = start + dt.timedelta(days=int(rng.integers(-30, 300)))
                    if W.HISTORY_START <= d <= last:
                        minute = int(rng.integers(6 * 60, 23 * 60))
                        if (d.month, d.day) == (9, 30) and minute >= 16 * 60:
                            minute -= 8 * 60                    # no late-evening contact on a year's last day
                        con.append({"pid": adult, "date": d, "minute": minute})
        self.enrollments, self.bed_nights, self.dv_stays, self.encounters, self.contacts = enr, beds, dv, enc, con
        # Ostry's HMIS vendor writes the household's move-in date on every member's enrollment, not only the head's
        hoh_mi = {(e["hh_id"]): e["move_in"] for e in enr if e["rel"] == 1 and e["move_in"] is not None}
        self.member_move_in = {e["eid"]: hoh_mi[e["hh_id"]] for e in enr
                               if e["rel"] != 1 and e["coc"] == "OST" and e["hh_id"] in hoh_mi}

    @staticmethod
    def _site(hh, rng):
        sites = {"CAL": ["VSM-01", "VSM-02", "VSM-05"], "MAR": ["VSM-03"], "OST": ["VSM-04"], "PEL": ["VSM-MP"]}
        lst = sites[hh["home"]]
        return lst[int(rng.integers(len(lst)))]

    # ------------------------------------------------------------------------------------------------ records
    def _records(self, rng):
        srcs = collections.defaultdict(set)
        for e in self.enrollments:
            srcs[e["pid"]].add("HMIS-" + e["coc"])
        for s in self.dv_stays:
            srcs[s["pid"]].add("DVC")
        for e in self.encounters:
            srcs[e["pid"]].add("VSM")
        for c in self.contacts:
            srcs[c["pid"]].add("HOT")
        recs = []
        for p in self.people:
            for s in sorted(srcs[p["pid"]]):
                recs.append(self._present({"src": s, "pid": p["pid"]}, p, rng))
        return recs

    def _present(self, r, p, rng):
        s = r["src"]
        hh = self.households[p["hh"]]
        if s == "DVC":
            full = False                                    # the coalition sends birth year only, by policy
        elif s == "HOT":
            full = rng.random() < 0.15                      # most give an age, a few a date of birth
        elif s == "VSM":
            full = True
        else:
            approx = (0.52 if p["home"] == "CAL" else 0.24) if hh["street"] else 0.04
            full = not (rng.random() < approx)
        ssn = None
        if p["ssn4"] is not None and ((s.startswith("HMIS") and rng.random() < 0.62) or
                                      (s == "VSM" and rng.random() < 0.88)):
            ssn = p["ssn4"]
        fn = p["fn"]
        if rng.random() < 0.06 and fn in NICK:
            fn = NICK[fn]
        ln = p["ln"]
        if p["hisp"] and p["ln2"] and rng.random() < 0.10:
            ln = p["ln"] + " " + p["ln2"]
        r.update(fn=fn, ln=ln, by=p["by"], bm=p["bm"] if full else None, bd=p["bd"] if full else None, ssn=ssn,
                 sex=p["sex"], full=full)
        return r

    # ------------------------------------------------------------------------------------------------ the unit
    WEIGHTS = {"fn": {"A": 4.5, "P": 2.0, "D": -2.5}, "ln": {"A": 5.0, "P": 2.5, "D": -3.0},
               "by": {"A": 2.0}, "bm": {"A": 2.0, "D": -3.0, "M": 0.0}, "bd": {"A": 2.5, "D": -3.5, "M": 0.0},
               "sex": {"A": 0.5, "D": -2.0}, "ssn": {"A": 6.0, "D": -4.0, "M": 0.0}}

    @classmethod
    def agree(cls, a, b):
        """Per-field agreement codes the unit reports (A agree, P partial, D disagree, M missing) and the score."""
        fa = "A" if a["fn"] == b["fn"] else ("P" if NICK.get(a["fn"]) == b["fn"] or NICK.get(b["fn"]) == a["fn"]
                                              else "D")
        la = "A" if a["ln"] == b["ln"] else ("P" if a["ln"].split()[0] == b["ln"].split()[0] else "D")
        ma = "M" if (a["bm"] is None or b["bm"] is None) else ("A" if a["bm"] == b["bm"] else "D")
        da = "M" if (a["bd"] is None or b["bd"] is None) else ("A" if a["bd"] == b["bd"] else "D")
        sa = "A" if a["sex"] == b["sex"] else "D"
        na = "M" if (a["ssn"] is None or b["ssn"] is None) else ("A" if a["ssn"] == b["ssn"] else "D")
        codes = {"fn": fa, "ln": la, "by": "A", "bm": ma, "bd": da, "sex": sa, "ssn": na}
        score = sum(cls.WEIGHTS[k][v] for k, v in codes.items())
        return codes, round(score, 1)

    def compare(self):
        blocks = collections.defaultdict(list)
        for i, r in enumerate(self.records):
            blocks[(soundex(r["ln"].split()[0]), r["by"])].append(i)
        pairs = []
        for key in sorted(blocks):
            idx = blocks[key]
            for i, j in itertools.combinations(idx, 2):
                if self.records[i]["src"] == self.records[j]["src"]:
                    continue
                codes, sc = self.agree(self.records[i], self.records[j])
                pairs.append((i, j, sc, codes))
        return pairs

    # ------------------------------------------------------------------------------------------------ honesty
    def tidy(self, rounds=60):
        """Redraw identity until (1) every person's records link to one another directly, (2) every link between two
        people's records sits where a source's grain shows it, so resolving the findings within each source's grain
        recovers the people, and (3) the resolution's people and recipients do not depend on how a tie between equal
        links is broken and match the people actually served."""
        import methods as MT
        rng = np.random.default_rng(self.seed * 13 + 5)
        self.tidy_log = []
        for it in range(rounds):
            pairs = self.compare()
            links = [(i, j, s) for i, j, s, c in pairs if s >= W.THRESHOLD]
            linked = {(i, j) for i, j, s in links}
            f1 = f2 = f3 = 0
            by_person = collections.defaultdict(list)
            for i, r in enumerate(self.records):
                by_person[r["pid"]].append(i)
            for pid, idx in by_person.items():
                for i, j in itertools.combinations(sorted(idx), 2):
                    if (i, j) not in linked:
                        p = self.people[pid]
                        for k in (i, j):
                            self.records[k]["fn"], self.records[k]["ln"] = p["fn"], p["ln"]
                        f1 += 1
            if f1:
                self.tidy_log.append((it, f1, 0, 0))
                continue
            comps = MT.components(len(self.records), links)
            where = {}
            for k, comp in enumerate(comps):
                for i in comp:
                    where[i] = k
            by_comp = collections.defaultdict(list)
            for l in links:
                if l[0] in where:
                    by_comp[where[l[0]]].append(l)
            victims = set()
            for k, comp in enumerate(comps):
                people = {self.records[i]["pid"] for i in comp}
                if len(people) == 1:
                    continue
                if len(people) > 4 or len(comp) > 12:
                    cnt = collections.Counter(self.records[i]["pid"] for i in comp)
                    victims |= {q for q, n in cnt.items() if q != cnt.most_common(1)[0][0]}
                    continue
                order = sorted(by_comp[k], key=lambda t: (-t[2], t[0], t[1]))
                gold = MT._local_resolve(self.records, comp, by_comp[k], order)
                clusters = collections.defaultdict(list)
                for i in comp:
                    clusters[gold[i]].append(self.records[i]["pid"])
                for members in clusters.values():
                    cnt = collections.Counter(members)
                    if len(cnt) > 1:
                        top = cnt.most_common(1)[0][0]
                        victims |= {q for q in cnt if q != top}
            for q in sorted(victims):
                self._rename(q, rng)
            f2 = len(victims)
            if f2:
                self.tidy_log.append((it, 0, f2, 0))
                continue
            bad = MT.tie_sensitive(self, links)
            for q in sorted(set(bad)):
                self._rename(q, rng)
            f3 = len(set(bad))
            self.tidy_log.append((it, 0, 0, f3))
            if not f3:
                self.pairs, self.links, self.tidy_rounds = pairs, links, it
                return
        raise SystemExit("tidy did not converge: %s" % self.tidy_log[-6:])

    def _rename(self, pid, rng):
        """Redraw a person's identity where it collides: a new first name and date of birth (adults also a birth year
        one or two years away), on every record of theirs, keeping each record's own completeness."""
        p = self.people[pid]
        if p["role"] == "child":
            p["fn"] = (CHILD_F if p["sex"] == "F" else CHILD_M)[int(rng.integers(20))] + "a"
        else:
            fl = (N.OTHER_FEMALE if p["sex"] == "F" else N.OTHER_MALE)
            p["fn"] = fl[0][int(rng.integers(len(fl[0])))]
            p["by"] = int(np.clip(p["by"] + int(rng.choice([-2, -1, 1, 2])), 1938, 2006))
        p["bm"], p["bd"] = int(rng.integers(1, 13)), int(rng.integers(1, 29))
        if getattr(self, "_ri", None) is None:
            self._ri = collections.defaultdict(list)
            for k, r in enumerate(self.records):
                self._ri[r["pid"]].append(k)
        for k in self._ri.get(pid, ()):
            r = self.records[k]
            r["fn"], r["by"] = p["fn"], p["by"]
            if r["bm"] is not None:
                r["bm"], r["bd"] = p["bm"], p["bd"]
