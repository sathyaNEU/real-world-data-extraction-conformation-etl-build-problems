"""task127: the golden, computed from the shipped files in target/ only (plus the watch list's lines, which
docs.py prints from the same table). Every rival route the ladder and the checks price is here too."""
import csv
import datetime as dt
import itertools
import os
import re
from collections import defaultdict

import openpyxl

D = dt.date
ENVELOPE = 6_000_000


def digits(s):
    return re.sub(r"\D", "", s or "")


def pdate(s):
    if isinstance(s, dt.datetime):
        return s.date()
    if isinstance(s, dt.date):
        return s
    return dt.date.fromisoformat(s)


def add_months(d, k):
    y, m = d.year, d.month + k
    while m > 12:
        y, m = y + 1, m - 12
    while m < 1:
        y, m = y - 1, m + 12
    last = [31, 29 if y % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]
    return D(y, m, min(d.day, last))


def rcsv(target, name):
    with open(os.path.join(target, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


class Pack:
    def __init__(self, target, watch_lines):
        self.t = target
        self.watch_lines = watch_lines            # {customer_no: proposed line}
        wb = openpyxl.load_workbook(os.path.join(target, "customer_master_2026-12.xlsx"), read_only=True)
        self.cust = {}
        for r in list(wb["Customers"].iter_rows(values_only=True))[1:]:
            self.cust[r[0]] = dict(name=r[1], trading=r[2], nzbn=str(r[3]), sector=r[4], region=r[6])
        self.acct = {}
        self.accts_of = defaultdict(set)
        for r in list(wb["Accounts"].iter_rows(values_only=True))[1:]:
            self.acct[digits(r[1])] = r[0]
            self.accts_of[r[0]].add(digits(r[1]))
        for r in rcsv(target, "account_number_crosswalk_2023.csv"):
            cid = self.acct.get(digits(r["new_account"]))
            if cid:
                self.acct[digits(r["legacy_account"])] = cid
                self.accts_of[cid].add(digits(r["legacy_account"]))
        self.run26 = rcsv(target, "ifrs9_facility_run_2026-12-31.csv")
        self.run24 = rcsv(target, "ifrs9_facility_run_2024-12-31.csv")
        self.episodes = self._episodes()
        self._receipts()

    # ---- defaults ------------------------------------------------------------------------------------
    def _loan_accounts(self):
        """A Ruahine loan account belongs to the customer whose cheque account repays it (the ledger's LN rows)."""
        m = {}
        with open(os.path.join(self.t, "business_account_transactions_2021-2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["txn_code"] == "LN":
                    cid = self.acct.get(digits(r["account_number"]))
                    if cid:
                        m[digits(r["other_party_account"])] = cid
        return m

    def _episodes(self, keys="all"):
        loans = self._loan_accounts() if keys == "all" else {}
        trig = defaultdict(list)
        self.unkeyed = 0
        for r in rcsv(self.t, "default_register_2021-2026.csv"):
            ref = r["reference"]
            if ref.startswith("C"):
                cid = ref
            elif keys == "utp":
                cid = None
            else:
                cid = self.acct.get(digits(ref)) or loans.get(digits(ref))
            if not cid:
                self.unkeyed += 1
                continue
            trig[cid].append(pdate(r["trigger_date"]))
        cures = defaultdict(dict)
        for r in rcsv(self.t, "default_cures_2021-2026.csv"):
            cures[r["customer_no"]][pdate(r["default_date"])] = pdate(r["cure_date"])
        eps = defaultdict(list)
        for cid, ds in trig.items():
            ds.sort()
            open_ep = None
            for d in ds:
                if open_ep and (open_ep[1] is None or d < open_ep[1]):
                    continue
                cure = cures[cid].get(d)
                open_ep = (d, cure)
                eps[cid].append(open_ep)
        return eps

    def in_default(self, cid, day):
        return any(s <= day and (c is None or c > day) for s, c in self.episodes.get(cid, []))

    def starts(self, cid):
        return [s for s, _ in self.episodes.get(cid, [])]

    # ---- receipts ------------------------------------------------------------------------------------
    def _receipts(self):
        """Monthly receipts per customer: the total (own-account transfers and Ruahine lending left out) and the
        part from each other Ruahine customer."""
        self.tot = defaultdict(float)          # (cid, ym) -> total
        self.frm = defaultdict(float)          # (payee, payer, ym) -> amount
        self.raw_tot = defaultdict(float)      # totals with own transfers and lending kept
        with open(os.path.join(self.t, "business_account_transactions_2021-2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["dr_cr"] != "CR":
                    continue
                cid = self.acct.get(digits(r["account_number"]))
                if not cid:
                    continue
                ym = r["posting_date"][:7]
                amt = float(r["amount_nzd"])
                self.raw_tot[(cid, ym)] += amt
                oa = digits(r["other_party_account"])
                if oa and oa in self.accts_of[cid]:
                    continue
                if oa.startswith("471299"):
                    continue
                self.tot[(cid, ym)] += amt
                payer = self.acct.get(oa)
                if payer and payer != cid:
                    self.frm[(cid, payer, ym)] += amt
        self.payers_of = defaultdict(set)
        for (p, a, ym) in self.frm:
            self.payers_of[p].add(a)

    def share(self, payee, payer, a, b, raw=False):
        """Share of payee's receipts from payer over months [a, b) (dates, first of month)."""
        yms = []
        d = D(a.year, a.month, 1)
        while d < b:
            yms.append("%04d-%02d" % (d.year, d.month))
            d = add_months(d, 1)
        tot = sum((self.raw_tot if raw else self.tot)[(payee, ym)] for ym in yms)
        if tot <= 0:
            return 0.0
        return sum(self.frm[(payee, payer, ym)] for ym in yms) / tot

    # ---- the main call -----------------------------------------------------------------------------------
    def borrowers26(self):
        out = defaultdict(list)
        for r in self.run26:
            out[r["customer_no"]].append(r)
        return out

    def own(self, cid, pdcol="pd_12m"):
        return sum(float(r[pdcol]) * float(r["lgd"]) * float(r["ead_nzd"]) for r in self.borrowers26()[cid])

    def lgd_ead(self, cid):
        return sum(float(r["lgd"]) * float(r["ead_nzd"]) for r in self.borrowers26()[cid])

    def pd(self, cid, col="pd_12m"):
        return float(self.borrowers26()[cid][0][col])

    def dependents(self, payer, T=0.30, raw=False, a=D(2026, 1, 1), b=D(2027, 1, 1)):
        b26 = self.borrowers26()
        out = []
        for p in sorted(b26):
            if p == payer or b26[p][0]["stage"] == "3":
                continue
            if payer in self.payers_of[p] and self.share(p, payer, a, b, raw) >= T:
                out.append(p)
        return out

    def borrower_universe(self):
        u = set(r["customer_no"] for r in self.run26) | set(r["customer_no"] for r in self.run24)
        u |= set(self.episodes)
        return u

    def p1(self, T=0.30, window=12, raw=False, lookback=12):
        U = self.borrower_universe()
        n = k = 0
        pairs = []
        for a, eps in self.episodes.items():
            for s, _ in eps:
                if not (D(2022, 1, 1) <= s <= D(2025, 12, 31)):
                    continue
                for p in sorted(U):
                    if p == a or a not in self.payers_of[p]:
                        continue
                    if self.share(p, a, add_months(D(s.year, s.month, 1), -lookback), D(s.year, s.month, 1), raw) < T:
                        continue
                    if self.in_default(p, s):
                        continue
                    n += 1
                    hit = any(s < t <= add_months(s, window) for t in self.starts(p))
                    k += hit
                    pairs.append((a, p, s, hit))
        return (k / n if n else 0.0), k, n, pairs

    def p0(self, T=0.30, raw=False, years=(2022, 2023, 2024, 2025)):
        U = self.borrower_universe()
        n = k = 0
        for Y in years:
            y0, y1 = D(Y, 1, 1), D(Y + 1, 1, 1)
            for p in sorted(U):
                for a in self.payers_of[p]:
                    if self.share(p, a, D(Y - 1, 1, 1), y0, raw) < T:
                        continue
                    if self.in_default(a, y0) or any(y0 <= t < y1 for t in self.starts(a)):
                        continue
                    if self.in_default(p, y0):
                        continue
                    if not self._active(p, Y):
                        continue
                    n += 1
                    k += any(y0 <= t < y1 for t in self.starts(p))
        return (k / n if n else 0.0), k, n

    def _active(self, p, Y):
        return any(self.tot[(p, "%04d-%02d" % (Y, m))] > 0 for m in (1, 2, 3))

    def values(self, uplift, T=0.30, pdcol="pd_12m", baseline=None):
        """Each watch-list borrower's write-off kept off the book: own plus its PD x uplift x each dependant's
        LGD x EAD. baseline: None uses the uplift as given; 'model' uses p1 less each dependant's own PD."""
        out = {}
        for cid in self.watch_lines:
            v = self.own(cid, pdcol)
            pdb = self.pd(cid, pdcol)
            for s in self.dependents(cid, T):
                if baseline is None:
                    v += pdb * uplift * self.lgd_ead(s)
                else:
                    v += pdb * max(0.0, baseline - self.pd(s)) * self.lgd_ead(s)
            out[cid] = v
        return out

    def best_set(self, vals):
        ids = sorted(self.watch_lines)
        best = None
        for k in range(1, len(ids) + 1):
            for comb in itertools.combinations(ids, k):
                if sum(self.watch_lines[i] for i in comb) <= ENVELOPE:
                    tot = sum(vals[i] for i in comb)
                    if best is None or tot > best[1] + 1e-6:
                        best = (comb, tot)
        ranked = []
        for k in range(1, len(ids) + 1):
            for comb in itertools.combinations(ids, k):
                if sum(self.watch_lines[i] for i in comb) <= ENVELOPE:
                    ranked.append((sum(vals[i] for i in comb), comb))
        ranked.sort(reverse=True)
        runner = next(c for t, c in ranked if c != best[0])
        return best[0], best[1], runner, dict((c, t) for t, c in ranked)[runner]

    # ---- ask A -------------------------------------------------------------------------------------------
    MON = {m: i + 1 for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct",
                                            "nov", "dec"])}

    def made_quarter(self, ref):
        s = ref.strip()
        m = re.search(r"val (\d{2})/(\d{2})/(\d{4})", s)
        if m:
            return int(m.group(3)), (int(m.group(2)) - 1) // 3 + 1
        m = re.search(r"inspected \d{1,2} ([A-Za-z]{3}) (\d{4})", s)
        if m:
            return int(m.group(2)), (self.MON[m.group(1).lower()] - 1) // 3 + 1
        m = re.search(r"JLL \d{4}/\d+ \(([A-Za-z]+) (\d{4})\)", s)
        if m:
            return int(m.group(2)), (self.MON[m.group(1)[:3].lower()] - 1) // 3 + 1
        m = re.search(r"BV-(\d{2})(\d{2})-", s)
        if m:
            return 2000 + int(m.group(1)), (int(m.group(2)) - 1) // 3 + 1
        m = re.search(r"KF (\d{2})\.(\d{2})\.(\d{2})", s)
        if m:
            return 2000 + int(m.group(3)), (int(m.group(2)) - 1) // 3 + 1
        m = re.search(r"desktop ([A-Za-z]{3})-(\d{2})", s)
        if m:
            return 2000 + int(m.group(2)), (self.MON[m.group(1).lower()] - 1) // 3 + 1
        raise ValueError(ref)

    def index(self, latest=True):
        idx = {}
        rows = rcsv(self.t, "commercial_property_index_2015-2026.csv")
        for r in rows:
            k = (r["region"], r["property_type"], r["quarter"])
            rank = 1 if r["release"] == "Revised" else 0
            if not latest:
                rank = -rank
            if k not in idx or rank > idx[k][0]:
                idx[k] = (rank, float(r["index_value"]))
        return {k: v for k, (_, v) in idx.items()}

    def titles_held(self):
        held = {}
        for r in rcsv(self.t, "title_instruments_2026-12.csv"):
            if r["mortgagee"] != "Ruahine Bank Limited":
                continue
            key = re.sub(r"^[A-Z]+", "", r["title_reference"])
            dis = r["discharged_date"]
            held[key] = not (dis and pdate(dis) <= D(2026, 12, 31))
        return held

    def security(self, use_made=True, drop_discharged=True, latest=True):
        wb = openpyxl.load_workbook(os.path.join(self.t, "security_register_2026-12.xlsx"), read_only=True)
        idx = self.index(latest)
        held = self.titles_held()
        out = defaultdict(float)
        for r in list(wb["Properties"].iter_rows(values_only=True))[1:]:
            sid, cid, title, addr, ptype, region, amt, vdate, valuer, ref = r[:10]
            if cid not in self.watch_lines:
                continue
            key = re.sub(r"^[A-Z]+", "", str(title))
            if drop_discharged and not held.get(key, True):
                continue
            if use_made:
                y, q = self.made_quarter(ref)
            else:
                vd = pdate(vdate)
                y, q = vd.year, (vd.month - 1) // 3 + 1
            out[cid] += float(amt) * idx[(region, ptype, "2026Q4")] / idx[(region, ptype, "%dQ%d" % (y, q))]
        return {c: out[c] for c in self.watch_lines}

    # ---- ask B -------------------------------------------------------------------------------------------
    WORDS = {"two hundred and fifty thousand": 250_000, "three hundred thousand": 300_000,
             "three hundred and fifty thousand": 350_000, "four hundred thousand": 400_000,
             "five hundred thousand": 500_000, "six hundred and fifty thousand": 650_000,
             "seven hundred and fifty thousand": 750_000, "nine hundred thousand": 900_000}

    def limit_amount(self, text):
        m = re.search(r"\$([\d,]+)", text)
        if m:
            return float(m.group(1).replace(",", ""))
        low = text.lower()
        for k, v in sorted(self.WORDS.items(), key=lambda kv: -len(kv[0])):
            if low.startswith(k):
                return float(v)
        raise ValueError(text)

    def name_index(self, former=True):
        ix = {}
        for r in rcsv(self.t, "companies_register_extract_2026-12.csv"):
            ix[r["entity_name"].upper()] = r["nzbn"]
            if former and r["previous_names"]:
                for part in r["previous_names"].split("; "):
                    ix[re.sub(r" \(to .*\)$", "", part).upper()] = r["nzbn"]
        return ix

    def commitment(self, former=True, drop_released=True):
        wb = openpyxl.load_workbook(os.path.join(self.t, "security_register_2026-12.xlsx"), read_only=True)
        nz2c = {v["nzbn"]: k for k, v in self.cust.items()}
        ix = self.name_index(former)
        released = set()
        for r in list(wb["Deed log"].iter_rows(values_only=True))[1:]:
            if r[2] == "Released" and pdate(r[3]) <= D(2026, 12, 31):
                released.add(r[1])
        lim = defaultdict(float)
        for r in self.run26:
            lim[r["customer_no"]] += float(r["limit_nzd"])
        out = {c: lim[c] for c in self.watch_lines}
        for r in list(wb["Guarantees"].iter_rows(values_only=True))[1:]:
            gid, gname, gnzbn, gdcid, gdname, gtype, limit, deed, status = r
            cid = nz2c.get(str(gnzbn)) if gnzbn else None
            if cid is None:
                nz = ix.get(str(gname).upper())
                cid = nz2c.get(nz) if nz else None
            if cid not in self.watch_lines:
                continue
            if drop_released and gid in released:
                continue
            out[cid] += lim[gdcid] if gtype == "Unlimited" else self.limit_amount(str(limit))
        return out

    # ---- ask C -------------------------------------------------------------------------------------------
    def sector_table(self, use_register=True, use_cures=True, keys="all"):
        by = {}
        for r in self.run24:
            by.setdefault(r["customer_no"], r)
        eps_saved = self.episodes
        if keys != "all":
            self.episodes = self._episodes(keys)
        if not use_cures:
            self.episodes = {c: [(s, None) for s, _ in e] for c, e in self.episodes.items()}
        out = defaultdict(lambda: [0, 0, 0.0])
        for cid, r in by.items():
            if use_register:
                perf = not self.in_default(cid, D(2024, 12, 31))
            else:
                perf = r["stage"] != "3"
            if not perf:
                continue
            o = out[r["anzsic_division"]]
            o[0] += 1
            o[1] += any(D(2025, 1, 1) <= t <= D(2025, 12, 31) for t in self.starts(cid))
            o[2] += float(r["pd_12m"])
        self.episodes = eps_saved
        return {s: (100.0 * v[1] / v[0], 100.0 * v[2] / v[0], v[0], v[1]) for s, v in sorted(out.items())}
