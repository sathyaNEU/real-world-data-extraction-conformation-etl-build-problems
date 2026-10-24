"""task179 world: Corriemoor University (fictional, Republic of Aldmark).

Every student who entered from 2015 to 2026, followed census by census to 1 October 2026; the first-time entrants of
2019 to 2026 in full (attributes, Semester 1 classes at the census, week-6 progress ratings, whether each is enrolled
at the next census); the Semester 1 2026 class timetable; the programme transfers of 2025-26.

The process the record carries and the decision turns on: until 2025 the Registry's allocation run placed most
full-time entrants in a group of 28 who took UNIV101 and their faculty's two first-year papers together; from 2026
(the ARC cutover) entrants enrolled themselves in classes, and only the halls' living-learning communities were still
placed together. An entrant's chance of not being enrolled at the next census falls steeply with the number of other
entrants met in two or more of the entrant's own classes. Nothing in the record names it."""
from __future__ import annotations

import datetime as dt

import numpy as np
import scipy.sparse as sp

import common as C

TRUTH = dict(icpt=-0.95, asc=-0.42, fif=0.30, pt=0.38, mature=0.22, hard=0.18, prisk=0.62, beta=1.05, mid=7.0, width=1.8)
N0 = 7900          # 2019 first-time entrants (before growth)
FIRST = 2019
CHURN = 0.07       # an allocated entrant moved out of the group in one paper at add/drop
EXTRA_FORWARD = 160   # the 2026 offer round took in more entrants than the trend
GROWTH = 0.0105
ALLOC_DAY = (7, 20)  # the allocation run's date each July (history)


def ties_from_classes(n, pairs):
    """pairs: list of (student index, class key). Returns the number of other students each student meets in two or
    more of the student's own classes, and that count at three or more."""
    keys = {}
    rows, cols = [], []
    for s, k in pairs:
        j = keys.setdefault(k, len(keys))
        rows.append(s)
        cols.append(j)
    A = sp.csr_matrix((np.ones(len(rows)), (np.array(rows), np.array(cols))), shape=(n, len(keys)))
    M = (A @ A.T).tocsr()
    M.setdiag(0)
    M.eliminate_zeros()
    t2 = np.asarray((M >= 2).sum(1)).ravel().astype(int)
    t3 = np.asarray((M >= 3).sum(1)).ravel().astype(int)
    return t2, t3


def peer(t):
    """the share of the protection a group gives that an entrant meeting t others in two or more classes has"""
    T = TRUTH
    z0 = 1 / (1 + np.exp(T["mid"] / T["width"]))
    return (1 / (1 + np.exp(-(np.asarray(t, float) - T["mid"]) / T["width"])) - z0) / (1 - z0)


class Cohort:
    pass


class World:
    def __init__(self):
        self.cohorts = {y: self._cohort(y) for y in C.INTAKES}
        self._flows()
        self._transfers()
        self._timetable()

    # ------------------------------------------------------------------ first-time entrants
    def _cohort(self, y):
        g = C.stream("cohort/%d" % y)
        n = int(round(N0 * (1 + GROWTH) ** (y - FIRST))) + (EXTRA_FORWARD if y == C.FORWARD else 0)
        c = Cohort()
        c.y, c.n = y, n
        fac = g.choice(C.FAC_CODES, size=n, p=[C.FAC_SHARE[f] for f in C.FAC_CODES])
        prog = np.empty(n, dtype=object)
        prog2 = np.full(n, "", dtype=object)
        for f in C.FAC_CODES:
            idx = np.where(fac == f)[0]
            ps = [p for p in C.PROGRAMMES if p[2] == f]
            prog[idx] = g.choice([p[0] for p in ps], size=len(idx), p=[p[4] for p in ps])
        # conjoint entrants, about 3 per cent, the first-listed programme in its own faculty
        conj = g.random(n) < 0.03
        for i in np.where(conj)[0]:
            opts = [cj for cj in C.CONJOINTS if C.PROG[cj[0]][2] == fac[i]]
            if not opts:
                conj[i] = False
                continue
            a, b = opts[g.integers(len(opts))]
            prog[i], prog2[i] = a, b
        c.fac, c.prog, c.prog2, c.conj = fac, prog, prog2, conj
        c.asc = np.clip(np.round(g.normal(186, 34, n)), 90, 300).astype(int)
        c.ascz = (c.asc - c.asc.mean()) / c.asc.std()
        c.fif = (g.random(n) < 0.31).astype(int)
        age = np.where(g.random(n) < 0.12, g.integers(21, 46, n), g.choice([17, 18, 18, 18, 19, 19, 20], size=n))
        c.mature = (age >= 21).astype(int)
        c.dob = [dt.date(y - int(a), 1, 1) + dt.timedelta(days=int(g.integers(0, 365))) for a in age]
        c.pt = ((g.random(n) < np.where(c.mature == 1, 0.42, 0.045))).astype(int)
        c.hard = (g.random(n) < np.where(c.fif == 1, 0.36, 0.15)).astype(int)
        c.sex = g.choice(["F", "M", "X"], size=n, p=[0.56, 0.435, 0.005])
        c.region = g.choice(["Corriemoor", "Westray", "Halden", "Northmoor", "Kelso Bay", "Upper Tarn", "Ruthven",
                             "Overseas"], size=n, p=[0.34, 0.14, 0.12, 0.11, 0.09, 0.08, 0.07, 0.05])
        # acceptance dates: December of the year before to late August
        start = dt.date(y - 1, 12, 1)
        days = np.clip(np.round(g.gamma(4.2, 31, n)), 0, 268).astype(int)
        c.accepted = [start + dt.timedelta(days=int(d)) for d in days]
        alloc = dt.date(y, *ALLOC_DAY)
        c.late = np.array([a > alloc for a in c.accepted], dtype=int)
        hall_p = np.where((c.mature == 0) & (c.pt == 0), np.where(c.region == "Corriemoor", 0.18, 0.52), 0.03)
        c.hall = (g.random(n) < hall_p).astype(int)
        c.hall_name = np.where(c.hall == 1, g.choice(C.HALLS, size=n), "")
        c.lc = ((c.hall == 1) & (g.random(n) < 0.33) & (c.late == 0)).astype(int)
        # papers
        papers = []
        for i in range(n):
            # the fourth paper is a first-year elective from the university's schedule, open to every faculty
            ppaper = C.ELECTIVES[int(g.integers(len(C.ELECTIVES)))]
            if c.pt[i]:
                papers.append([C.UNIV, ppaper])
            else:
                f1, f2 = C.FAC_PAPERS[fac[i]]
                papers.append([C.UNIV, f1, f2, ppaper])
        c.papers = papers
        self._classes(c, g)
        c.ties, c.ties3 = ties_from_classes(n, [(s, k) for s in range(n) for k in c.classes[s]])
        self._progress(c, g)
        self._outcome(c, g)
        return c

    def _classes(self, c, g):
        """Semester 1 class at the census for each paper each entrant takes. Class keys are (paper, class number)."""
        n, y = c.n, c.y
        history = y < C.FORWARD
        if history:
            blocked = (c.pt == 0) & (c.late == 0) & (g.random(n) >= 0.05)
            blocked |= c.lc == 1
        else:
            blocked = c.lc == 1
        c.blocked = blocked
        assign = [dict() for _ in range(n)]
        core = {}
        for i in range(n):
            for p in c.papers[i]:
                core.setdefault(p, []).append(i)
        # blocks within faculty: living-learning community floors first, then the allocation run's groups
        blocks = []
        for f in C.FAC_CODES:
            for flag in (1, 0):
                idx = np.where(blocked & (c.fac == f) & (c.lc == flag))[0]
                if flag == 0:
                    order = sorted(idx, key=lambda i: (c.prog[i], g.random()))
                else:
                    order = sorted(idx, key=lambda i: (c.hall_name[i], g.random()))
                for b in range(0, len(order), C.BLOCK):
                    blocks.append((f, order[b:b + C.BLOCK]))
        c.nblocks = len(blocks)
        for p, takers in core.items():
            takers = np.array(takers)
            ncls = int(np.ceil(len(takers) / 27.0)) + 1
            fill = {}
            k = 0
            is_core = p == C.UNIV or any(p in v for v in C.FAC_PAPERS.values())
            if is_core:
                for f, members in blocks:
                    mem = [i for i in members if p in c.papers[i]]
                    if not mem:
                        continue
                    k += 1
                    for i in mem:
                        assign[i][p] = k
                    fill[k] = len(mem)
            ncls = max(ncls, k + int(np.ceil(sum(1 for i in takers if p not in assign[i]) / 27.0)) + 1)
            free = [i for i in takers if p not in assign[i]]
            g.shuffle(free)
            # friend pairs in the forward cohort: about a tenth enrol together where seats allow
            pairs = {}
            if not history:
                fr = [i for i in free]
                npair = int(0.05 * len(fr))
                for a, b in zip(fr[:npair], fr[npair:2 * npair]):
                    pairs[b] = a
            for i in free:
                choice = None
                if i in pairs and p in assign[pairs[i]] and g.random() < 0.6:
                    cand = assign[pairs[i]][p]
                    if fill.get(cand, 0) < C.CLASS_CAP:
                        choice = cand
                if choice is None:
                    opts = [j for j in range(1, ncls + 1) if fill.get(j, 0) < C.CLASS_CAP]
                    choice = opts[g.integers(len(opts))]
                assign[i][p] = choice
                fill[choice] = fill.get(choice, 0) + 1
            # add/drop moves before the census (history: a clash moves an allocated student out of the group)
            if history and is_core:
                for i in takers:
                    if blocked[i] and c.lc[i] == 0 and g.random() < CHURN:
                        opts = [j for j in range(1, ncls + 1) if fill.get(j, 0) < C.CLASS_CAP and j != assign[i][p]]
                        new = opts[g.integers(len(opts))]
                        fill[assign[i][p]] -= 1
                        assign[i][p] = new
                        fill[new] = fill.get(new, 0) + 1
            c.__dict__.setdefault("nclasses", {})[p] = ncls
        c.assign = assign
        c.classes = [[(p, assign[i][p]) for p in c.papers[i]] for i in range(n)]

    def _progress(self, c, g):
        n = c.n
        ability = 0.55 * c.ascz + g.normal(0, 0.85, n)
        c.ratings = []
        risk = np.zeros(n)
        for i in range(n):
            rr = []
            for p in c.papers[i]:
                r = ability[i] + g.normal(0, 0.7)
                code = "R" if r < -1.3 else ("C" if r < -0.45 else "S")
                if g.random() < 0.04:
                    code = ""
                rr.append(code)
            c.ratings.append(rr)
            vals = [{"S": 0, "C": 1, "R": 2}[x] for x in rr if x]
            risk[i] = np.mean(vals) if vals else 0.5
        c.prisk = risk

    def _outcome(self, c, g):
        T = TRUTH
        s = peer(c.ties)
        fe = np.array([C.FAC_EFFECT[f] for f in c.fac])
        lin = (T["icpt"] + T["asc"] * c.ascz + T["fif"] * c.fif + T["pt"] * c.pt + T["mature"] * c.mature
               + T["hard"] * c.hard + T["prisk"] * c.prisk + fe - T["beta"] * s)
        c.p = 1 / (1 + np.exp(-lin))
        c.gone = (g.random(c.n) < c.p).astype(int)        # not enrolled at the next census
        c.on_leave = ((c.gone == 1) & (g.random(c.n) < 0.07)).astype(int)

    # ------------------------------------------------------------------ the whole student body, census by census
    def _flows(self):
        """Every student's census rows 2019 to 2026. Students are dicts; first-time entrants of 2019 to 2026 carry
        their cohort index."""
        g = C.stream("flows")
        self.students = []
        sid = 0
        for y in C.PRE + C.INTAKES:
            if y in self.cohorts:
                c = self.cohorts[y]
                for i in range(c.n):
                    self.students.append(dict(sid=sid, intake=y, basis="FT1", cohort=y, ci=i, fac=c.fac[i],
                                              prog=c.prog[i], prog2=c.prog2[i], pt=int(c.pt[i])))
                    sid += 1
            else:
                n = int(round(N0 * (1 + GROWTH) ** (y - FIRST)))
                fac = g.choice(C.FAC_CODES, size=n, p=[C.FAC_SHARE[f] for f in C.FAC_CODES])
                for i in range(n):
                    ps = [p for p in C.PROGRAMMES if p[2] == fac[i]]
                    pr = ps[g.choice(len(ps), p=[p[4] for p in ps])][0]
                    pr2 = ""
                    if g.random() < 0.03:
                        opts = [cj for cj in C.CONJOINTS if C.PROG[cj[0]][2] == fac[i]]
                        if opts:
                            pr, pr2 = opts[g.integers(len(opts))]
                    self.students.append(dict(sid=sid, intake=y, basis="FT1", cohort=None, ci=None, fac=fac[i],
                                              prog=pr, prog2=pr2, pt=int(g.random() < 0.09)))
                    sid += 1
            # entrants with credit from another institution, entering at year of study 2
            ntr = int(round(430 * (1 + GROWTH) ** (y - FIRST)))
            fac = g.choice(C.FAC_CODES, size=ntr, p=[C.FAC_SHARE[f] for f in C.FAC_CODES])
            for i in range(ntr):
                ps = [p for p in C.PROGRAMMES if p[2] == fac[i]]
                pr = ps[g.choice(len(ps), p=[p[4] for p in ps])][0]
                self.students.append(dict(sid=sid, intake=y, basis="TRC", cohort=None, ci=None, fac=fac[i],
                                          prog=pr, prog2="", pt=int(g.random() < 0.15)))
                sid += 1
        # census by census
        for s in self.students:
            s["rows"] = {}           # census year -> (status, year_of_study)
            y = s["intake"]
            yos = 2 if s["basis"] == "TRC" else 1
            done = 0.0               # full-time years completed
            status = "EN"
            dur = C.PROG[s["prog"]][3] + (1 if s["prog2"] else 0)
            if s["basis"] == "TRC":
                done = 1.0
            cy = y
            first = True
            while cy <= 2026:
                if cy >= FIRST:
                    s["rows"][cy] = (status, min(yos, 4))
                # move to the next census
                if status == "EN":
                    done += 0.5 if s["pt"] else 1.0
                if first and s["basis"] == "FT1" and s["cohort"] is not None:
                    c = self.cohorts[s["cohort"]]
                    gone = c.gone[s["ci"]]
                    leave = c.on_leave[s["ci"]]
                    if gone and not leave:
                        break
                    status = "LV" if leave else "EN"
                    if not leave:
                        yos += 1
                    first = False
                    cy += 1
                    continue
                first = False
                if status == "LV":
                    if g.random() < 0.62:
                        status = "EN"
                        cy += 1
                        continue
                    break
                if done >= dur and g.random() < 0.82:
                    break                                    # completed
                if yos == 1:
                    cont = 0.755
                elif yos == 2:
                    cont = 0.885
                else:
                    cont = 0.925
                r = g.random()
                if r < cont:
                    status = "EN"
                    if not s["pt"] or g.random() < 0.5:
                        yos += 1
                elif r < cont + 0.025:
                    status = "LV"
                else:
                    break
                cy += 1
        self._ids()

    def _ids(self):
        """SIRIUS student numbers for every student admitted before the cutover; ARC ids for every student with a
        census row in 2026 and every 2026 entrant."""
        g = C.stream("ids")
        legacy = g.choice(np.arange(2100000, 2999999), size=len(self.students), replace=False)
        arc = g.choice(np.arange(10100000, 10999999), size=len(self.students), replace=False)
        for s, a, b in zip(self.students, legacy, arc):
            s["legacy"] = int(a) if s["intake"] < 2026 else None
            s["arc"] = "C%d" % b if (2026 in s["rows"] or s["intake"] == 2026 or self._active_at_cutover(s)) else None

    @staticmethod
    def _active_at_cutover(s):
        st = s["rows"].get(2025)
        return st is not None

    # ------------------------------------------------------------------ programme transfers 2025-26
    # programme transfers approved after the cutover between faculties, by year of study: (from, to, how many).
    # Most are moves into the second programme of an approved conjoint combination (BA to LLB, BSc to BCom ...).
    STALE = {2: [("BA", "LLB", 2), ("BA", "BSC", 1), ("BSC", "BCOM", 3), ("BENGH", "BCOM", 1), ("BCOMPSC", "BSC", 1),
                 ("BHSC", "BCOM", 2), ("BSPEX", "BCOM", 1), ("BNURS", "BSOCSC", 1), ("BFA", "BBUS", 1)],
             3: [("BA", "LLB", 1), ("BA", "BSC", 2), ("BSC", "BCOM", 2), ("BENGH", "BCOM", 2), ("BCOMPSC", "BSC", 1),
                 ("BHSC", "BCOM", 1), ("BSPEX", "BCOM", 2), ("BHSC", "BCOMPSC", 1), ("BSOCSC", "BHSC", 1)],
             4: [("BA", "LLB", 3), ("BA", "BSC", 1), ("BSC", "BCOM", 1), ("BENGH", "BCOM", 2), ("BCOMPSC", "BSC", 2),
                 ("BHSC", "BCOM", 1), ("BSPEX", "BCOM", 1), ("BBUS", "BCOMPSC", 1)]}

    def _transfers(self):
        """Transfers approved between 1 October 2025 and 30 September 2026. Those approved after the cutover left
        the old programme attempt active in ARC (the discontinuation was keyed in SIRIUS in its last days and did
        not carry across). No 2025 first-time entrant is among the transfers after the cutover."""
        g = C.stream("transfers")
        self.transfers = []
        cand = [s for s in self.students if 2026 in s["rows"] and s["rows"][2026][0] == "EN"
                and s["rows"][2026][1] >= 2 and not s["prog2"]]
        main = [s for s in cand if not (s["basis"] == "FT1" and s["intake"] == 2025) and s["basis"] != "TRC"
                and not (s["intake"] == 2026)]
        order = sorted(main, key=lambda s: s["sid"])
        g.shuffle(order)
        used = set()
        F = C.FAC_CODES
        for yv in (2, 3, 4):
            for p_from, p_to, k in self.STALE[yv]:
                for j in range(k):
                    pool = [s for s in order if s["sid"] not in used and min(s["rows"][2026][1], 4) == yv
                            and s["prog"] == p_from]
                    assert pool, (p_from, yv)
                    s = pool[0]
                    used.add(s["sid"])
                    day = C.CUTOVER + dt.timedelta(days=int(g.integers(3, 112)))
                    self.transfers.append(dict(s=s, old=p_from, new=p_to, approved=day, stale=True))
                    s["stale_old"] = p_from
                    s["prog_before"] = p_from
                    s["prog"], s["fac"] = p_to, C.PROG[p_to][2]
        # transfers before the cutover (discontinued in SIRIUS, one attempt in ARC) and within-faculty ones after it
        rest = sorted([s for s in cand if s["sid"] not in used and s["intake"] < 2026], key=lambda s: s["sid"])
        g.shuffle(rest)
        for s in rest[:310]:
            day = dt.date(2025, 10, 6) + dt.timedelta(days=int(g.integers(0, 330)))
            same = g.random() < 0.45
            ps = [p for p in C.PROGRAMMES if (p[2] == s["fac"]) == same and p[0] != s["prog"]]
            new = ps[int(g.integers(len(ps)))][0]
            if day >= C.CUTOVER and (not same or (s["basis"] == "FT1" and s["intake"] == 2025)):
                day = C.CUTOVER - dt.timedelta(days=int(g.integers(1, 60)))
            stale_same = day >= C.CUTOVER
            self.transfers.append(dict(s=s, old=s["prog"], new=new, approved=day, stale=stale_same))
            if stale_same:
                s["stale_old"] = s["prog"]
            s["prog_before"] = s["prog"]
            s["prog"], s["fac"] = new, C.PROG[new][2]
        self.transfers.sort(key=lambda t: (t["approved"], t["s"]["sid"]))

    # ------------------------------------------------------------------ Semester 1 2026 timetable
    def _timetable(self):
        """One record per class; meetings are laid out in pack.py. First-year classes come from the 2026 entrants'
        classes; upper-level papers from the continuing students' faculties and years. Some 300-level papers are
        taught together with a 400-level paper: one teacher, one room, one time."""
        g = C.stream("timetable")
        c = self.cohorts[C.FORWARD]
        classes = []
        counts = {}
        for i in range(c.n):
            for key in c.classes[i]:
                counts[key] = counts.get(key, 0) + 1
        for p, ncls in sorted(c.nclasses.items()):
            fac = self._paper_fac(p)
            for k in range(1, ncls + 1):
                classes.append(dict(paper=p, k=k, fac=fac, level=100, enrolled=counts.get((p, k), 0), pair=None))
        head = {}
        for s in self.students:
            r = s["rows"].get(2026)
            if r and r[0] == "EN" and r[1] >= 2:
                head[(s["fac"], min(r[1], 4))] = head.get((s["fac"], min(r[1], 4)), 0) + 1
        stems = {"ASS": ["HIST", "ENGL", "POLS", "PHIL", "SOCI", "PSYC", "FINE", "LING", "ANTH", "MUSC"],
                 "BUS": ["ACCT", "MKTG", "MGMT", "ECON", "FINC", "LAWS", "INFS"],
                 "SCI": ["BIOL", "CHEM", "PHYS", "STAT", "MATH", "GEOL", "BMED", "ENVS"],
                 "ENG": ["ENGR", "COMP", "ELEC", "MECH", "CIVL", "SOFT"],
                 "HLT": ["NURS", "HSCI", "SPEX", "PUBH", "NUTR"]}
        used_codes = set(x["paper"] for x in classes)
        self.pairs = []

        def code_for(stem, lev):
            while True:
                cd = "%s%d" % (stem, lev + int(g.integers(1, 99)))
                if cd not in used_codes:
                    used_codes.add(cd)
                    return cd
        for f in C.FAC_CODES:
            nst = len(stems[f])
            for lev, yv, npap in ((200, 2, 46), (300, 3, 42)):
                tot = head.get((f, yv), 0) * 3.3 + (head.get((f, 4), 0) * 1.4 if lev == 300 else 0)
                nsm = int(0.3 * npap)
                small_sz = g.integers(6, 30, nsm)
                w = g.gamma(1.1, 1.0, npap - nsm)
                rest = max(tot - small_sz.sum(), 30 * (npap - nsm))
                sizes = np.concatenate([small_sz, np.maximum(30, np.round(rest * w / w.sum()))]).astype(int)
                g.shuffle(sizes)
                for j in range(npap):
                    cd = code_for(stems[f][j % nst], lev)
                    sz = int(sizes[j])
                    nk = 1 if sz <= 180 else 2
                    for k in range(1, nk + 1):
                        classes.append(dict(paper=cd, k=k, fac=f, level=lev, enrolled=int(sz // nk + (k <= sz % nk)),
                                            pair=None))
            # papers taught together, at 200 level (two 200-level papers in one class) and at 300 level (a 300-level
            # paper and an honours paper): per faculty and level, five combinations set up in ARC Scheduling (three
            # over 30 students, two at 30 or under), whose census enrolment ARC writes as the combination's on each
            # class, and three carried from SIRIUS as separate classes sharing the room and slot, which show their own
            # enrolments (over 30 together with unequal and with equal halves, and one at 30 or under)
            kinds = [("arc", True, 0), ("arc", True, 0), ("arc", True, 0), ("arc", False, 0), ("arc", False, 0),
                     ("sirius", True, 0), ("sirius", True, 1), ("sirius", False, 0)]
            for lev in (200, 300):
                pool = sorted([x for x in classes if x["fac"] == f and x["level"] == lev and x["k"] == 1
                               and x.get("pair") is None and x["enrolled"] <= 60], key=lambda x: x["paper"])
                g.shuffle(pool)
                for kind, over, equal in kinds:
                    m = pool.pop()
                    if lev == 300:
                        cd = code_for(stems[f][int(g.integers(nst))], 400)
                        rec = dict(paper=cd, k=1, fac=f, level=400, enrolled=0, pair=None)
                        classes.append(rec)
                    else:
                        rec = pool.pop()
                    if equal:
                        v = int(g.integers(16, 21))
                        m["enrolled"], rec["enrolled"] = v, v
                    else:
                        total = int(g.integers(31, 41)) if over else int(g.integers(21, 31))
                        hi = 16 if lev == 300 else total - 5
                        r = int(g.integers(5, min(hi, total - 5) + 1))
                        if kind == "sirius" and 2 * r == total:
                            r -= 1
                        m["enrolled"], rec["enrolled"] = total - r, r
                    for x, y in ((m, rec), (rec, m)):
                        x["pair"] = (y["paper"], y["k"])
                        x["combined"] = kind == "arc"
                    self.pairs.append((m, rec))
            # honours papers taught on their own
            for j in range(4):
                cd = code_for(stems[f][j % nst], 400)
                classes.append(dict(paper=cd, k=1, fac=f, level=400, enrolled=int(g.integers(5, 17)), pair=None))
        # On their own stream, so every draw above stands. Two of each faculty and level's pairs carried from SIRIUS
        # share only their lecture and keep a workshop each: the unequal pair over 30 (now a paper over 30 with a
        # small partner) and the pair at 30 or under. Two single classes a faculty and level stand just over 30 on
        # ARC Scheduling's figure.
        gd = C.stream("tt_devices")
        for f in C.FAC_CODES:
            for lev in (200, 300):
                sir = [(m, r) for (m, r) in self.pairs if m["fac"] == f and m["level"] == lev and not m.get("combined")]
                for m, r in sir:
                    if m["enrolled"] == r["enrolled"]:
                        continue
                    if m["enrolled"] + r["enrolled"] > 30:
                        m["enrolled"], r["enrolled"] = int(gd.integers(31, 37)), int(gd.integers(5, 13))
                    m["partial"] = r["partial"] = True
                lv = (lev,) if lev == 200 else (300,)
                pool = sorted([x for x in classes if x["fac"] == f and x["level"] in lv and x["k"] == 1
                               and x.get("pair") is None and 30 <= x["enrolled"] <= 60
                               and not any(y["paper"] == x["paper"] and y["k"] == 2 for y in classes)],
                              key=lambda x: x["paper"])
                for j in gd.permutation(len(pool))[:2]:
                    pool[j]["enrolled"] = int(gd.integers(32, 35))
                    pool[j]["flip"] = True
        self.classes = classes

    @staticmethod
    def _paper_fac(p):
        if p == C.UNIV:
            return "ASS"
        for f, v in C.FAC_PAPERS.items():
            if p in v:
                return f
        for pr in C.PROGRAMMES:
            if p in pr[5]:
                return pr[2]
        raise KeyError(p)
