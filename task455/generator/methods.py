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

    def flow(self, a, qi=None):
        """The account that paid most of `a`'s first-quarter workers the quarter before: (account, count, workers,
        share, stopped, share of the source's workers that moved)."""
        qi = self.first_quarter(a) if qi is None else qi
        ws = self.paid.get((a, qi), set())
        if not ws or qi == 0:
            return (None, 0, len(ws), 0.0, False, 0.0)
        c = Counter()
        for wk in ws:
            for p in self.payers.get((wk, qi - 1), ()):
                if p != a:
                    c[p] += 1
        if not c:
            return (None, 0, len(ws), 0.0, False, 0.0)
        top, n = sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[0]
        src_ws = self.paid.get((top, qi - 1), set())
        return (top, n, len(ws), n / len(ws), self.stopped_by(top, qi), n / len(src_ws) if src_ws else 0.0)

    def classify(self, year, threshold=0.5, need_stop=True, two_sided=False, liability=True, wages_quarter=True):
        """Golden classification of the year's new accounts: 'filed', 'workforce' (continuing per the flow test) or
        'birth'."""
        out = {}
        for a in self.new_accounts(year, liability=liability):
            if a in self.pred:
                out[a] = "filed"
                continue
            top, n, nw, share, stopped, src_share = self.flow(a)
            cont = top is not None and share > threshold and (stopped or not need_stop)
            if two_sided:
                cont = cont and src_share > 0.5
            out[a] = "workforce" if cont else "birth"
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

    def sources(self):
        """Accounts whose business went on under a new account: the register's predecessors and the flow test's
        sources, for both years' new accounts."""
        out = set(self.pred.values())
        for y in (2025, 2026):
            for a, k in self.classify(y).items():
                if k == "workforce":
                    out.add(self.flow(a)[0])
        return out

    def ask_a(self, liability=True, county_from="register"):
        cls = self.classify(2025, liability=liability)
        base = self.base(0, county_from=county_from)
        if county_from == "register":
            births = Counter(self.county[a] for a, k in cls.items() if k == "birth")
        else:
            births = Counter(self.qcounty[(a, self.first_quarter(a))] for a, k in cls.items() if k == "birth")
        rates = {c: 100.0 * births.get(c, 0) / base[c] for c in base}
        return {"births": births, "base": base, "rates": rates, "cls": cls}

    def deaths_2025(self, county_from="register", continuation=True, by="employment"):
        src = self.sources() if continuation else set(self.pred.values())
        out = Counter()
        for a, i in self.ai.items():
            if by == "employment":
                lm = self.last_m[i]
                if lm < 0 or lm not in M2025 or self.emp[i, 15:].max() > 0:
                    continue
            else:
                qw = np.nonzero(self.wag[i] > 0)[0]
                if not len(qw) or not (1 <= qw[-1] <= 4):
                    continue
            if a in src:
                continue
            if county_from == "register":
                out[self.county[a]] += 1
            else:
                lq = int(self.last_m[i]) // 3 if by == "employment" else int(np.nonzero(self.wag[i] > 0)[0][-1])
                out[self.qcounty[(a, lq)]] += 1
        return out

    def ask_b(self, county_from="register", continuation=True, by="employment"):
        deaths = self.deaths_2025(county_from=county_from, continuation=continuation, by=by)
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
            "R3 workforce (golden)": self.rung_rates(filed | flowc),
        }
        return out
