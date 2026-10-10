"""The docket world: every examination docket opened FY2011 to the 30 September 2026 extract (FY2011 to FY2015
are burn-in and only reach the pack through last year's published series and through links to their successors).

A docket is one examiner's file on one application from docketing to close. A refused docket whose file passes
to a new docket closes on its refusal date with end code CX; the successor is either a re-examination of the
same application (route 1) or a continuing application filed on the transferred file (route 2). Nothing on a
docket, action or link records the route: only the production ledger's credit class on the successor's first
action on the merits does (1R or 1N).
"""
import math
import random
import sys

import params as P

sys.setrecursionlimit(10000)


def wd(o):
    w = (o - 1) % 7          # Monday = 0
    return o + 2 if w == 5 else (o + 1 if w == 6 else o)


def wd_back(o):
    w = (o - 1) % 7
    return o - 1 if w == 5 else (o - 2 if w == 6 else o)


class Structure:
    """Art units, their groups before and after the re-cut, their examiners and their pendency multipliers."""

    def __init__(self):
        R = random.Random(P.GROUP_SEED)
        self.aus, self.old_group, self.cur_group, self.mult = [], {}, {}, {}
        for g in P.GROUPS:
            for s in sorted(R.sample(range(10, 99), P.AUS_PER_GROUP)):
                au = g[:2] + "%02d" % s
                self.aus.append(au)
                self.old_group[au] = g
        while True:
            moved = sorted(R.sample(self.aus, len(self.aus) // 2))
            pool = [g for g in P.GROUPS for _ in range(len(moved) // len(P.GROUPS))]
            R.shuffle(pool)
            cur = dict(self.old_group)
            ok = True
            for au, g in zip(moved, pool):
                if g == self.old_group[au]:
                    ok = False
                    break
                cur[au] = g
            if ok and all(sum(1 for a in self.aus if cur[a] == g) >= 5 for g in P.GROUPS):
                break
        self.cur_group = cur
        self.moved = moved
        for au in self.aus:
            self.mult[au] = P.GMULT[cur[au]] * math.exp(R.gauss(0, 0.04))
        self.by_cur = {g: [a for a in self.aus if cur[a] == g] for g in P.GROUPS}
        self.examiners = {}
        used = set()
        for au in self.aus:
            ex = []
            for _ in range(R.randint(*P.EXAMINERS_PER_AU)):
                while True:
                    e = "E%05d" % R.randint(10000, 99999)
                    if e not in used:
                        used.add(e)
                        break
                ex.append(e)
            self.examiners[au] = ex
        # Examiner home art unit at the extract: about one in ten has moved since.
        self.home = {}
        for au in self.aus:
            for e in self.examiners[au]:
                self.home[e] = au if R.random() > 0.10 else R.choice(self.aus)
        self.R = R


class World:
    FIELDS = ("start", "kind", "parent", "depth", "prog", "route", "au_dock", "ex_dock", "au_close", "ex_close",
              "xfer", "code", "dec", "grant", "status", "close", "fa", "child", "app_start", "twin", "fpos",
              "nmid")

    def __init__(self, **over):
        self.p = {k: getattr(P, k) for k in dir(P) if k.isupper()}
        self.p.update(over)
        self.S = Structure()
        for f in self.FIELDS:
            setattr(self, f, [])
        self.R = random.Random(self.p["SEED"])

    def n(self):
        return len(self.start)

    # ---------------------------------------------------------------------------------------------- dockets
    def make(self, start, kind, parent, depth, prog, route, au, ex, app_start=None):
        p, R, S = self.p, self.R, self.S
        first_kind = kind != 1
        z = R.gauss(0, 1)
        u = R.random()
        f_pos = R.uniform(0.30, 0.55)
        lag = R.randint(*p["GRANT_LAG"])
        cx_gap, cx_draw, route_draw = R.randint(*p["CX_GAP"]), R.random(), R.random()
        cn_draw, cn_t, cn_type = R.random(), R.random(), R.random()
        x_draw, x_pos, x_same, x_pick = R.random(), R.random(), R.random(), R.random()
        e_pick, sfa_gap, nmid = R.random(), R.randint(*p["SUCC_FA_GAP"]), R.choice((0, 1, 1, 2, 2, 3))
        med, sig = (p["D1_MED"], p["D1_SIG"]) if first_kind else (p["D2_MED"], p["D2_SIG"])
        pa, pr = (p["P_ALW"], p["P_REF"]) if first_kind else (p["P2_ALW"], p["P2_REF"])
        code = "A" if u < pa else ("R" if u < pa + pr else "B")
        d = med * S.mult[au] * math.exp(sig * z)
        d *= p["REF_MULT"] if code == "R" else (p["ALW_MULT"] if code == "A" else 1.0)
        d = max(int(d), 75)
        dec = wd(start + d)
        if kind == 1:
            fa = wd(start + sfa_gap)
            if fa >= dec:
                fa = wd_back(dec - 7)
        else:
            fa = wd(start + max(21, int(d * f_pos)))
            if fa >= dec:
                fa = wd_back(dec - 7)
        i = self.n()
        app = start if (kind != 1 or route == 2) else app_start
        for f, v in (("start", start), ("kind", kind), ("parent", parent), ("depth", depth), ("prog", prog),
                     ("route", route), ("au_dock", au), ("ex_dock", ex), ("au_close", au), ("ex_close", ex),
                     ("xfer", None), ("code", code), ("dec", dec), ("grant", None), ("status", ""),
                     ("close", None), ("fa", fa), ("child", -1), ("app_start", app), ("twin", 0),
                     ("fpos", f_pos), ("nmid", nmid)):
            getattr(self, f).append(v)
        X = p["EXTRACT"] if "EXTRACT" in p else P.EXTRACT
        if dec > X:
            self.status[i], self.close[i] = "", None
        elif code == "A":
            g = wd(dec + lag)
            self.grant[i] = g
            if g <= X:
                self.status[i], self.close[i] = "ALW", g
        elif code == "B":
            self.status[i], self.close[i] = "ABN", dec
        else:
            self.status[i], self.close[i] = "REF", dec
        # transfer between art units while the docket is open
        if x_draw < p["P_XFER"]:
            end_t = self.close[i] if self.close[i] is not None else X
            if end_t - start > 30:
                xd = wd(start + 1 + int(x_pos * (end_t - start - 10)))
                if start < xd < end_t and xd <= X:
                    if x_same < 0.6:
                        cands = [a for a in S.by_cur[S.cur_group[au]] if a != au]
                    else:
                        cands = [a for a in S.aus if a != au]
                    to = cands[int(x_pick * len(cands))]
                    exs = S.examiners[to]
                    self.xfer[i] = xd
                    self.au_close[i] = to
                    self.ex_close[i] = exs[int(e_pick * len(exs))]
        # CN / DV children filed while a first-kind docket is open
        if first_kind and cn_draw < p["P_CNDV"]:
            t = wd(start + 90 + int(cn_t * max(d - 90, 1)))
            if t <= X and t < dec:
                k = 2 if cn_type < 0.6 else 3
                held = self.au_close[i] if (self.xfer[i] is not None and self.xfer[i] < t) else au
                hex_ = self.ex_close[i] if held != au else ex
                self.make(t, k, i, 0, False, 0, held, hex_)
        # refusal: the file passes to a new docket, or the refusal stands
        if code == "R" and dec <= X:
            pcx = p["P_CX1"] if first_kind else p["P_CX2"]
            s2 = wd(dec + cx_gap)
            if depth < p["MAX_DEPTH"] and cx_draw < pcx and s2 <= X:
                r = 1 if (prog or route_draw >= p["P_CONT"]) else 2
                mark = self.n()
                c = self.make(s2, 1, i, depth + 1, prog, r, self.au_close[i], self.ex_close[i],
                              app_start=self.app_start[i])
                # A transfer whose successor has no first action by the extract would leave an FY2022
                # application's status undetermined; such a refusal stands instead.
                lo, hi = P.FY22
                if self.fa[c] > X and lo <= self.app_start[i] <= hi:
                    for f in self.FIELDS:
                        del getattr(self, f)[mark:]
                else:
                    self.child[i] = c
                    self.status[i] = "CX"
        return i

    def build(self):
        p, R = self.p, self.R
        S = self.S
        gw = [p["GWEIGHT"][g] for g in P.GROUPS]
        cum = [sum(gw[:k + 1]) for k in range(len(gw))]
        for fy in range(P.FIRST_FY, P.LAST_FY + 1):
            lo, hi = P.fy_bounds(fy)
            n = int(p["N0"] * (1 + p["GROWTH"]) ** (fy - 2016))
            starts = sorted(wd(R.randint(lo, hi)) for _ in range(n))
            for s in starts:
                if s > hi:
                    s = wd_back(hi)
                ug, ua, ue, up = R.random(), R.random(), R.random(), R.random()
                g = P.GROUPS[next(k for k in range(len(cum)) if ug * cum[-1] <= cum[k])]
                au = S.by_cur[g][int(ua * len(S.by_cur[g]))]
                ex = S.examiners[au][int(ue * len(S.examiners[au]))]
                prog = p["PROG_FY"][0] <= fy <= p["PROG_FY"][1] and up < p["P_PROG"]
                self.make(s, 0, -1, 0, prog, 0, au, ex)
            if fy == 2022:
                self.add_twins()
        self.hole_fix()
        return self

    def add_twins(self):
        """Two applications identical on every docket, action and continuity column; only the credit class
        on the successor's first action differs (route 1 against route 2)."""
        T, S = self.p["TWIN"], self.S
        au = S.by_cur["2400"][0]
        ex = S.examiners[au][0]
        for route in (1, 2):
            i = self.n()
            vals = dict(start=T["start"].toordinal(), kind=0, parent=-1, depth=0, prog=False, route=0,
                        au_dock=au, ex_dock=ex, au_close=au, ex_close=ex, xfer=None, code="R",
                        dec=T["ref"].toordinal(), grant=None, status="CX", close=T["ref"].toordinal(),
                        fa=T["fa"].toordinal(), child=i + 1, app_start=T["start"].toordinal(), twin=route,
                        fpos=None, nmid=-1)
            for f in self.FIELDS:
                getattr(self, f).append(vals[f])
            s2 = T["succ"].toordinal()
            vals = dict(start=s2, kind=1, parent=i, depth=1, prog=False, route=route, au_dock=au, ex_dock=ex,
                        au_close=au, ex_close=ex, xfer=None, code="A", dec=T["noa"].toordinal(),
                        grant=T["grant"].toordinal(), status="ALW", close=T["grant"].toordinal(),
                        fa=T["succ_fa"].toordinal(), child=-1,
                        app_start=(s2 if route == 2 else T["start"].toordinal()), twin=route, fpos=None, nmid=-1)
            for f in self.FIELDS:
                getattr(self, f).append(vals[f])

    # ---------------------------------------------------------------------------------------- applications
    def app_final(self, i):
        """Final decision date of the application whose filing docket is i (route-aware), or None."""
        while True:
            c = self.child[i]
            if c >= 0 and self.route[c] == 1:
                i = c
                continue
            if c >= 0:                      # continuing application filed: this application ended at refusal
                return i, self.dec[i]
            if self.status[i] in ("ALW", "ABN", "REF") or (self.code[i] == "A" and self.dec[i] <= P.EXTRACT):
                return i, self.dec[i]
            return i, None

    def app_roots(self):
        return [i for i in range(self.n()) if self.kind[i] != 1 or self.route[i] == 2]

    def hole_fix(self):
        """No FY2022 application is finally decided 1,095 or 1,096 days after filing, so 'within 36 months'
        selects the same applications under the day count, the calendar month and inclusive counting."""
        lo, hi = P.FY22
        moved = 0
        for i in self.app_roots():
            if not (lo <= self.start[i] <= hi):
                continue
            j, e = self.app_final(i)
            if e is not None and e - self.start[i] in (1095, 1096):
                nd = wd(self.start[i] + 1097)
                shift = nd - self.dec[j]
                self.dec[j] = nd
                if self.code[j] == "A":
                    self.grant[j] = wd(self.grant[j] + shift)
                    ok = self.grant[j] <= P.EXTRACT
                    self.status[j], self.close[j] = ("ALW", self.grant[j]) if ok else ("", None)
                elif self.status[j] != "CX":
                    self.close[j] = nd
                else:
                    self.close[j] = nd
                    assert self.start[self.child[j]] > nd
                moved += 1
        self.hole_moved = moved
