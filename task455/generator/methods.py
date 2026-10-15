"""Every reading of the bundle the design names, computed from the shipped files alone: the golden (new accounts
first employing in the year, less the register's filed successorships and the accounts whose first-quarter workforce
came mostly from one account that then stopped reporting), each rung of the ladder, the variants the fork table
asserts, and the two asks."""
import os
import re
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

import world as W

QS = W.QUARTERS
NM = 3 * len(QS)                        # 27 months, October 2024 to December 2026
M2025 = range(3, 15)                    # January to December 2025
M2026 = range(15, 27)


def load(target):
    reg = pd.read_csv(os.path.join(target, W.FILES["register"]), dtype=str, keep_default_na=False)
    q = pd.read_csv(os.path.join(target, W.FILES["qcew"]), dtype={"account_no": str, "county_code": str,
                                                                  "naics_code": str, "own_code": str})
    wr = pd.read_csv(os.path.join(target, W.FILES["wages"]), sep="|", dtype={"worker_key": str, "account_no": str})
    return {"reg": reg, "q": q, "w": wr}


class Bundle:
    def __init__(self, target):
        b = load(target)
        self.reg, self.q, self.w = b["reg"], b["q"], b["w"]
        q = self.q
        q["qi"] = [QS.index((y, k)) for y, k in zip(q["year"], q["qtr"])]
        accts = sorted(set(self.reg["account_no"]))
        self.accts = accts
        self.ai = {a: i for i, a in enumerate(accts)}
        emp = np.zeros((len(accts), NM), dtype=np.int64)
        wag = np.zeros((len(accts), len(QS)))
        rows = q["account_no"].map(self.ai).to_numpy()
        for k, col in enumerate(("month1_emplvl", "month2_emplvl", "month3_emplvl")):
            emp[rows, 3 * q["qi"].to_numpy() + k] = q[col].to_numpy()
        wag[rows, q["qi"].to_numpy()] = q["total_qtrly_wages"].to_numpy()
        self.emp, self.wag = emp, wag
        self.reg_by = self.reg.set_index("account_no")
        self.county = self.reg_by["county_code"].to_dict()
        self.qcounty = {(a, qi): c for a, qi, c in zip(q["account_no"], q["qi"], q["county_code"])}
        has = emp > 0
        self.first_m = np.where(has.any(1), has.argmax(1), -1)
        self.last_m = np.where(has.any(1), NM - 1 - has[:, ::-1].argmax(1), -1)
        w = self.w
        w["qi"] = [QS.index((y, k)) for y, k in zip(w["year"], w["qtr"])]
        self.payers = defaultdict(set)          # (worker, qi) -> accounts paying
        self.paid = defaultdict(set)            # (account, qi) -> workers paid
        for wk, ac, qi in zip(w["worker_key"], w["account_no"], w["qi"]):
            self.payers[(wk, qi)].add(ac)
            self.paid[(ac, qi)].add(wk)
        self.pred = {r["account_no"]: r["predecessor_account"] for _, r in self.reg.iterrows()
                     if r["predecessor_account"]}

    # ------------------------------------------------------------- populations
    def new_accounts(self, year, liability=True):
        """Accounts whose first month with employment falls in `year` and that reported none before it. With
        `liability`, the register's liability date (the first payroll) must also fall in `year` or later."""
        months = M2026 if year == 2026 else M2025
        out = []
        for a, i in self.ai.items():
            fm = self.first_m[i]
            if fm in months:
                if liability:
                    ld = self.reg_by.at[a, "liability_date"]
                    if ld and ld < "%d-01-01" % year:
                        continue
                out.append(a)
        return out

    def base(self, qi, county_from="register"):
        """Establishments with employment in at least one month of quarter `qi`, by county."""
        c = Counter()
        for a, i in self.ai.items():
            if self.emp[i, 3 * qi:3 * qi + 3].max() > 0:
                c[self.county[a] if county_from == "register" else self.qcounty[(a, qi)]] += 1
        return c

    def first_quarter(self, a):
        return int(self.first_m[self.ai[a]]) // 3

    def stopped_by(self, src, qi):
        """The account reported no employment in quarter `qi` or later."""
        return self.emp[self.ai[src], 3 * qi:].max() == 0

    def links(self, a):
        """Every account that paid `a`'s first-quarter workers the quarter before or in that quarter, with: the
        number of `a`'s first-quarter workers it paid the quarter before, that number as a share of `a`'s first-quarter
        workers, the share of its own workers in its last quarter with employment that `a` paid then or the quarter
        after, and its last month with employment."""
        qi = self.first_quarter(a)
        ws = self.paid.get((a, qi), set())
        out = {}
        if not ws:
            return qi, ws, out
        prev = Counter()
        cands = set()
        for wk in ws:
            for p in self.payers.get((wk, qi - 1), ()) if qi > 0 else ():
                if p != a:
                    prev[p] += 1
                    cands.add(p)
            for p in self.payers.get((wk, qi), ()):
                if p != a:
                    cands.add(p)
        for p in cands:
            lm = int(self.last_m[self.ai[p]])
            lq = lm // 3 if lm >= 0 else -1
            own = self.paid.get((p, lq), set()) if lq >= 0 else set()
            here = self.paid.get((a, lq), set()) | self.paid.get((a, lq + 1), set())
            moved = len(own & here) / len(own) if own else 0.0
            out[p] = (prev[p], prev[p] / len(ws), moved, lm)
        return qi, ws, out

    def flow(self, a, qi=None):
        """The account that paid most of `a`'s first-quarter workers the quarter before: (account, count, workers,
        share, stopped, share of the source's workers that moved)."""
        fq, ws, ls = self.links(a)
        if not ls or not any(v[0] for v in ls.values()):
            return (None, 0, len(ws), 0.0, False, 0.0)
        top = sorted((p for p in ls if ls[p][0]), key=lambda p: (-ls[p][0], p))[0]
        v = ls[top]
        return (top, v[0], len(ws), v[1], self.stopped_by(top, fq), v[2])

    def continuing(self, a, rule="P", threshold=0.5, stop="month"):
        """Whether new account `a` goes on from a business under another account. `rule` P (the golden): most of
        the workers an account paid in its last quarter with employment moved to `a`; S: most of `a`'s first-quarter
        workers came from one account the quarter before; both, either. `stop`: month (the account's last month with
        employment before `a`'s first), quarter (none in `a`'s first quarter or later), none."""
        fq, ws, ls = self.links(a)
        fm = int(self.first_m[self.ai[a]])

        def stopped(p):
            lm = ls[p][3]
            return True if stop == "none" else (lm < fm if stop == "month" else lm < 3 * fq)
        if not ls:
            return False, None
        top = sorted((p for p in ls if ls[p][0]), key=lambda p: (-ls[p][0], p))
        s_src = top[0] if top else None
        s_ok = s_src is not None and ls[s_src][1] > threshold and stopped(s_src)
        p_hits = sorted((p for p in ls if ls[p][2] > threshold and stopped(p)), key=lambda p: (-ls[p][2], p))
        p_src = p_hits[0] if p_hits else None
        if rule == "P":
            return p_src is not None, p_src
        if rule == "S":
            return s_ok, s_src if s_ok else None
        if rule == "both":
            ok = s_ok and ls[s_src][2] > threshold
            return ok, s_src if ok else None
        if rule == "either":
            return (p_src is not None or s_ok), (p_src or (s_src if s_ok else None))
        raise ValueError(rule)

    def classify(self, year, rule="P", threshold=0.5, stop="month", liability=True):
        """The year's new accounts: 'filed' (a predecessor in the register), 'workforce' (continuing by `rule`) or
        'birth'."""
        out = {}
        self._src = getattr(self, "_src", {})
        for a in self.new_accounts(year, liability=liability):
            if a in self.pred:
                out[a] = "filed"
                continue
            cont, src = self.continuing(a, rule=rule, threshold=threshold, stop=stop)
            out[a] = "workforce" if cont else "birth"
            if cont and rule == "P" and threshold == 0.5 and stop == "month":
                self._src[a] = src
        return out

    def rates(self, cls, base, kind="birth"):
        n = Counter(self.county[a] for a, k in cls.items() if k == kind)
        return {c: 100.0 * n.get(c, 0) / base[c] for c in base}, n

    # ------------------------------------------------------------------- golden
    def golden(self):
        cls = self.classify(2026)
        base = self.base(QS.index((2025, 4)))
        rates, births = self.rates(cls, base)
        order = sorted(rates, key=lambda c: -rates[c])
        setaside = Counter(self.county[a] for a, k in cls.items() if k != "birth")
        new = Counter(self.county[a] for a in cls)
        return {"cls": cls, "base": base, "rates": rates, "births": births, "order": order, "top3": order[:3],
                "runner_up": order[3], "gap": rates[order[2]] - rates[order[3]], "setaside": setaside, "new": new,
                "filed": Counter(self.county[a] for a, k in cls.items() if k == "filed"),
                "workforce": Counter(self.county[a] for a, k in cls.items() if k == "workforce")}

    def sources(self, rule="P", stop="month"):
        """Accounts whose business went on under a new account: the register's predecessors and the sources the
        continuity rule finds for both years' new accounts."""
        out = set(self.pred.values())
        for y in (2025, 2026):
            for a in self.new_accounts(y):
                if a in self.pred:
                    continue
                cont, src = self.continuing(a, rule=rule, stop=stop)
                if cont:
                    out.add(src)
        return out

    def went_on(self, a, quarters=1):
        """Share of the workers `a` paid in its last quarter with employment that one other account paid the quarter
        after (or within `quarters` quarters after)."""
        i = self.ai[a]
        lm = int(self.last_m[i])
        lq = lm // 3
        own = self.paid.get((a, lq), set())
        if not own:
            return 0.0, None
        c = Counter()
        for wk in own:
            seen = set()
            for k in range(1, quarters + 1):
                for p in self.payers.get((wk, lq + k), ()):
                    if p != a and p not in seen:
                        seen.add(p)
            for p in seen:
                c[p] += 1
        if not c:
            return 0.0, None
        p, n = sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[0]
        return n / len(own), p

    def ask_a(self, liability=True, county_from="register", rule="P", stop="month"):
        cls = self.classify(2025, liability=liability, rule=rule, stop=stop)
        base = self.base(0, county_from=county_from)
        if county_from == "register":
            births = Counter(self.county[a] for a, k in cls.items() if k == "birth")
        else:
            births = Counter(self.qcounty[(a, self.first_quarter(a))] for a, k in cls.items() if k == "birth")
        rates = {c: 100.0 * births.get(c, 0) / base[c] for c in base}
        return {"births": births, "base": base, "rates": rates, "cls": cls}

    def stoppers_2025(self, by="employment"):
        out = []
        for a, i in self.ai.items():
            if by == "employment":
                lm = self.last_m[i]
                if lm < 0 or lm not in M2025 or self.emp[i, 15:].max() > 0:
                    continue
            else:
                qw = np.nonzero(self.wag[i] > 0)[0]
                if not len(qw) or not (1 <= qw[-1] <= 4):
                    continue
            out.append(a)
        return out

    def deaths_2025(self, county_from="register", mode="golden", by="employment", threshold=0.5, quarters=1):
        """2025 deaths. mode golden: less the register's predecessors and every account most of whose last-quarter
        workers one other account paid the quarter after; new_keyed: less the predecessors and the sources of the new
        accounts the P rule continues (quarter-level stop when mode is new_keyed_q); S: the sources the S rule finds;
        filed: the register's predecessors only."""
        if mode == "golden":
            gone = set(self.pred.values())
        elif mode == "new_keyed":
            gone = self.sources(rule="P")
        elif mode == "new_keyed_q":
            gone = self.sources(rule="P", stop="quarter")
        elif mode == "S":
            gone = self.sources(rule="S", stop="quarter")
        elif mode == "filed":
            gone = set(self.pred.values())
        else:
            raise ValueError(mode)
        out = Counter()
        for a in self.stoppers_2025(by=by):
            if a in gone:
                continue
            if mode == "golden" and self.went_on(a, quarters=quarters)[0] > threshold:
                continue
            i = self.ai[a]
            if county_from == "register":
                out[self.county[a]] += 1
            else:
                lq = int(self.last_m[i]) // 3 if by == "employment" else int(np.nonzero(self.wag[i] > 0)[0][-1])
                out[self.qcounty[(a, lq)]] += 1
        return out

    def ask_b(self, county_from="register", mode="golden", by="employment", threshold=0.5, quarters=1):
        deaths = self.deaths_2025(county_from=county_from, mode=mode, by=by, threshold=threshold, quarters=quarters)
        base = self.base(0, county_from=county_from)
        return {"deaths": deaths, "base": base, "rates": {c: 100.0 * deaths.get(c, 0) / base[c] for c in base}}

    # -------------------------------------------------------------------- rungs
    def rung_rates(self, setaside):
        """Rates when the new 2026 accounts in `setaside` are not births."""
        base = self.base(QS.index((2025, 4)))
        n = Counter(self.county[a] for a in self.new_accounts(2026) if a not in setaside)
        rates = {c: 100.0 * n.get(c, 0) / base[c] for c in base}
        return rates, sorted(rates, key=lambda c: -rates[c])

    def closed_before(self, a):
        """Accounts that reported their last employment before `a`'s first month."""
        fm = self.first_m[self.ai[a]]
        return fm

    def norm_addr(self, s):
        s = s.upper().replace(",", " ").replace(".", " ")
        for full, ab in [(d[0].upper(), d[1]) for d in W.DIRECTIONS] + [(t[0].upper(), t[1]) for t in W.STREET_TYPES] + [
                ("SUITE", "STE"), ("SQUARE", "SQ"), ("HIGHWAY", "HWY")]:
            s = re.sub(r"\b%s\b" % full, ab, s)
        return re.sub(r"\s+", " ", s).strip()

    def address_matches(self, suites=True, same_industry=False, adjacent=False):
        """New 2026 accounts at the worksite address of an account that stopped reporting before they started."""
        key = {}
        for a, r in self.reg_by.iterrows():
            ad = self.norm_addr(r["worksite_address"])
            if not suites:
                ad = re.sub(r"\s+STE\s+\S+$", "", ad)
            key[a] = (ad, r["worksite_zip"])
        by = defaultdict(list)
        for a, k in key.items():
            by[k].append(a)
        naics = self.q.groupby("account_no")["naics_code"].last().to_dict()
        out = set()
        for a in self.new_accounts(2026):
            fm = self.first_m[self.ai[a]]
            for b in by[key[a]]:
                if b == a:
                    continue
                lm = self.last_m[self.ai[b]]
                if lm < 0 or lm >= fm:
                    continue
                if same_industry and naics.get(b) != naics.get(a):
                    continue
                if adjacent and lm // 3 != fm // 3 - 1:
                    continue
                out.add(a)
                break
        return out

    def name_matches(self):
        def norm(s):
            s = re.sub(r"[^A-Z0-9 ]", " ", s.upper().replace("'S ", " "))
            s = re.sub(r"\b(LLC|INC|CO|CORP|PC|PLLC|LLP|OF TOLBECK|OF THE VALLEY|II)\b", " ", s)
            return re.sub(r"\s+", " ", s).strip()
        trade = defaultdict(list)
        for a, r in self.reg_by.iterrows():
            trade[norm(r["trade_name"])].append(a)
        out = set()
        for a in self.new_accounts(2026):
            fm = self.first_m[self.ai[a]]
            for b in trade[norm(self.reg_by.at[a, "trade_name"])]:
                if b != a and 0 <= self.last_m[self.ai[b]] < fm:
                    out.add(a)
                    break
        return out

    def attribute_matches(self, cross_county=False, tol=0.25):
        """Same industry, the old account's last quarter the one before, first-quarter employment within `tol` of the
        old account's last-quarter peak: one old account per new account, nearest size first."""
        naics = self.q.groupby("account_no")["naics_code"].last().to_dict()
        ended = defaultdict(list)
        for a, i in self.ai.items():
            lm = self.last_m[i]
            if lm >= 0 and lm < NM - 1:
                lq = lm // 3
                ended[(lq, naics.get(a), None if cross_county else self.county[a])].append(a)
        used = set()
        out = set()
        for a in sorted(self.new_accounts(2026), key=lambda x: (self.first_m[self.ai[x]], x)):
            if a in self.pred:
                continue
            i = self.ai[a]
            fq = self.first_m[i] // 3
            size = self.emp[i, 3 * fq:3 * fq + 3].max()
            best = None
            for b in ended.get((fq - 1, naics.get(a), None if cross_county else self.county[a]), []):
                if b in used:
                    continue
                j = self.ai[b]
                bsize = self.emp[j, 3 * (fq - 1):3 * fq].max()
                if bsize and abs(size - bsize) <= tol * bsize:
                    d = abs(size - bsize)
                    if best is None or d < best[0]:
                        best = (d, b)
            if best:
                used.add(best[1])
                out.add(a)
        return out

    def any_overlap(self):
        """New 2026 accounts with at least one first-quarter worker paid the quarter before by an account that then
        stopped reporting."""
        out = set()
        for a in self.new_accounts(2026):
            qi = self.first_quarter(a)
            for wk in self.paid.get((a, qi), ()):
                if any(p != a and self.stopped_by(p, qi) for p in self.payers.get((wk, qi - 1), ())):
                    out.add(a)
                    break
        return out

    def ladder(self):
        filed = set(self.pred) & set(self.new_accounts(2026))
        g = self.golden()
        flowc = {a for a, k in g["cls"].items() if k == "workforce"}
        addr = self.address_matches()
        out = {
            "R0 every new account": self.rung_rates(set()),
            "R0 default (net of filed)": self.rung_rates(filed),
            "R1 address match": self.rung_rates(filed | addr),
            "R1 address, same industry, adjacent": self.rung_rates(filed | self.address_matches(same_industry=True,
                                                                                               adjacent=True)),
            "R1 address without suites": self.rung_rates(filed | self.address_matches(suites=False)),
            "name match": self.rung_rates(filed | self.name_matches()),
            "address or name": self.rung_rates(filed | addr | self.name_matches()),
            "R2 attributes, same county": self.rung_rates(filed | self.attribute_matches()),
            "R2 attributes, any county": self.rung_rates(filed | self.attribute_matches(cross_county=True)),
            "R2 attributes or address": self.rung_rates(filed | addr | self.attribute_matches(cross_county=True)),
            "address and workforce": self.rung_rates(filed | addr | flowc),
            "any worker from a closed account": self.rung_rates(filed | self.any_overlap()),
            "R2 new account's share (more than half)": self.rung_rates(filed | self.cont_set("S", 0.5, "quarter")),
            "R2 new account's share, 80 per cent": self.rung_rates(filed | self.cont_set("S", 0.8, "quarter")),
            "R2 new account's share, no stop test": self.rung_rates(filed | self.cont_set("S", 0.5, "none")),
            "R2 both shares (more than half)": self.rung_rates(filed | self.cont_set("both", 0.5, "month")),
            "R2 both shares, 80 per cent": self.rung_rates(filed | self.cont_set("both", 0.8, "month")),
            "either share": self.rung_rates(filed | self.cont_set("either", 0.5, "month")),
            "R3 workforce (golden)": self.rung_rates(filed | flowc),
        }
        return out

    def cont_set(self, rule, threshold, stop, year=2026):
        return {a for a, k in self.classify(year, rule=rule, threshold=threshold, stop=stop).items() if k == "workforce"}
