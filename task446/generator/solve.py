"""The golden path for task446, reading only target/. Also the independent verifier: it shares no code
with world.py, truth.py or make.py. Options switch on the wrong paths the ladder and the ask stops use."""
import csv
import math
import os
import re
from collections import defaultdict

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "..", "target")
QES = ["2025-09-30", "2025-12-31", "2026-03-31", "2026-06-30", "2026-09-30"]
PROJ = QES[-1]


def rcsv(name, target):
    with open(os.path.join(target, name), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def dmy(s):  # 30/09/2026 -> 2026-09-30
    d, m, y = s.split("/")
    return "%s-%s-%s" % (y, m, d)


MON = {m: i + 1 for i, m in enumerate("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split())}


def dmon(s):  # 30-SEP-2026
    d, m, y = s.split("-")
    return "%s-%02d-%s" % (y, MON[m.upper()], d)


class Pack:
    def __init__(self, target=TARGET):
        self.target = target
        self.loans_main = rcsv("loan_book_qe_extracts.csv", target)
        self.loans_late = rcsv("loan_book_cwb_dub_20251231_late.csv", target)
        self.loans = self.loans_main + self.loans_late
        self.secs = rcsv("treasury_investment_positions_qe.csv", target)
        self.csa = rcsv("csa_collateral_held_qe.csv", target)
        self.fx = {(r["rate_date"], r["quote_currency"]): float(r["rate"]) for r in
                   rcsv("treasury_fx_closing_rates.csv", target)}
        self.l1 = defaultdict(dict)
        for r in rcsv("gleif_lei_records_qe_archive.csv", target):
            self.l1[r["archive_date"]][r["LEI"]] = r
        self.rr = defaultdict(list)
        for r in rcsv("gleif_relationship_records_qe_archive.csv", target):
            self.rr[r["archive_date"]].append(r)
        self.isin = {}
        for r in rcsv("isin_lei_20260930.csv", target):
            self.isin[r["ISIN"]] = r["LEI"]
        wb = openpyxl.load_workbook(os.path.join(target, "ccr_netting_set_exposure_qe.xlsx"), read_only=True)
        self.drv, self.drv_first = {}, {}
        for ws in wb.worksheets:
            title = ws.title.split(" ")
            d, m, y = title[0].split(".")
            date = "%s-%s-%s" % (y, m, d)
            rows = list(ws.iter_rows(values_only=True))
            hi = [i for i, r in enumerate(rows) if r and r[0] == "Netting set"][0]
            hdr = rows[hi]
            recs = [dict(zip(hdr, r)) for r in rows[hi + 1:] if r and r[0]]
            if len(title) > 1:          # rerun: the record for that close
                self.drv[date] = recs
            else:
                self.drv_first[date] = recs
                self.drv.setdefault(date, recs)
        wb = openpyxl.load_workbook(os.path.join(target, "house_limit_register_20260930.xlsx"), read_only=True)
        rows = list(wb.active.iter_rows(values_only=True))
        hi = [i for i, r in enumerate(rows) if r and r[0] == "Ultimate parent LEI"][0]
        self.limits = {r[0]: float(r[2]) for r in rows[hi + 1:] if r and r[0]}
        self.requests = self._agenda()

    def _agenda(self):
        from docx import Document
        doc = Document(os.path.join(self.target, "credit_committee_agenda_20261104.docx"))
        t = doc.tables[0]
        out = []
        for row in t.rows[1:]:
            c = [x.text for x in row.cells]
            lei = re.search(r"LEI ([A-Z0-9]{20})", c[1]).group(1)
            amt = float(re.search(r"GBP ([0-9.]+)m", c[4]).group(1))
            out.append(dict(item=c[0], borrower=c[1].split(" (LEI")[0], lei=lei, relationship=c[2],
                            ftype=c[3], amount=amt))
        return out


class Groups:
    """Obligor-group resolution from one GLEIF archive, membership at date d."""

    def __init__(self, pack, archive, d, follow_funds=False, keep_lapsed_rr=True, branches=True,
                 successors=True, keep_lapsed_entities=True):
        self.l1 = pack.l1[archive]
        self.parent, self.direct, self.branch, self.fund = {}, {}, {}, {}
        for r in pack.rr[archive]:
            if r["Relationship.RelationshipStatus"] != "ACTIVE":
                continue
            if not keep_lapsed_rr and r["Registration.RegistrationStatus"] == "LAPSED":
                continue
            st = r["Relationship.Period.1.startDate"][:10]
            en = r["Relationship.Period.1.endDate"][:10]
            if st > d or (en and en <= d):
                continue
            c, p, ty = r["Relationship.StartNode.NodeID"], r["Relationship.EndNode.NodeID"], r["Relationship.RelationshipType"]
            if not keep_lapsed_entities:
                if self.l1.get(p, {}).get("Registration.RegistrationStatus") == "LAPSED":
                    continue
            if ty == "IS_ULTIMATELY_CONSOLIDATED_BY":
                self.parent[c] = p
            elif ty == "IS_DIRECTLY_CONSOLIDATED_BY":
                self.direct[c] = p
            elif ty == "IS_INTERNATIONAL_BRANCH_OF":
                self.branch[c] = p
            elif ty == "IS_FUND-MANAGED_BY":
                self.fund[c] = p
        self.follow_funds, self.branches, self.successors = follow_funds, branches, successors

    def top(self, lei):
        seen = set()
        cur = lei
        while cur and cur not in seen:
            seen.add(cur)
            rec = self.l1.get(cur)
            if self.successors and rec and rec["Registration.RegistrationStatus"] == "MERGED" and \
                    rec["Entity.SuccessorEntity.SuccessorLEI"]:
                cur = rec["Entity.SuccessorEntity.SuccessorLEI"]
                continue
            if self.branches and cur in self.branch:
                cur = self.branch[cur]
                continue
            if cur in self.parent:
                cur = self.parent[cur]
                continue
            if cur in self.direct:
                cur = self.direct[cur]
                continue
            if self.follow_funds and cur in self.fund:
                cur = self.fund[cur]
                continue
            return cur
        return cur


def exposures(pack, qe, assign, opt):
    """Exposure by group top and book at quarter-end qe. assign(lei, row) -> group key."""
    out = defaultdict(lambda: defaultdict(float))
    rate = lambda c: 1.0 if c == "GBP" else (pack.fx[(qe, c)] if not opt.get("fx_multiply") else 1.0 / pack.fx[(qe, c)])
    if opt.get("no_fx"):
        rate = lambda c: 1.0
    src = pack.loans_main if opt.get("no_late_file") else pack.loans
    rows = [r for r in src if r["extract_date"] == qe]
    receiving_src = {r["migrated_from"] for r in rows if r["migrated_from"]}
    seen = set()
    for r in rows:
        if opt.get("dedup_migration", True) and r["facility_ref"] in receiving_src:
            continue
        if opt.get("lazy_dedup"):
            k = (r["customer_id"], r["facility_type"], r["currency"], r["facility_limit"], r["drawn_balance"])
            if k in seen:
                continue
            seen.add(k)
        g = assign(r["customer_lei"] or ("CUST:" + r["customer_id"]), r)
        rt = rate(r["currency"])
        drawn = float(r["drawn_balance"]) / rt
        und = max(0.0, float(r["facility_limit"]) - float(r["drawn_balance"])) / rt
        out[g]["loans_drawn"] += drawn
        if opt.get("drawn_only"):
            continue
        if r["committed"] == "Y":
            out[g]["undrawn"] += opt.get("ccf", 0.5) * und
        elif opt.get("ccf_uncommitted"):
            out[g]["undrawn"] += 0.5 * und
    if not opt.get("loans_only"):
        for r in pack.secs:
            if dmy(r["position_date"]) != qe:
                continue
            lei = r["issuer_lei"] or ("" if opt.get("drop_blank_issuer") else pack.isin.get(r["isin"], ""))
            if not lei:
                continue
            out[assign(lei, r)]["securities"] += float(r["carrying_value"]) / rate(r["currency"])
        cash = defaultdict(float)
        for r in pack.csa:
            if dmon(r["valuation_date"]) == qe and r["collateral_type"] == "CASH":
                cash[r["csa_reference"]] += float(r["amount_held"]) / rate(r["currency"])
            elif dmon(r["valuation_date"]) == qe and opt.get("all_collateral"):
                cash[r["csa_reference"]] += float(r["amount_held"]) / rate(r["currency"])
        for r in (pack.drv_first[qe] if opt.get("first_run") else pack.drv[qe]):
            m = float(r["Net MTM"]) * (1.0 if opt.get("mtm_units") else 1000.0)
            c = 0.0 if opt.get("ignore_collateral") else cash.get(r["CSA reference"] or "", 0.0)
            v = max(0.0, m - c)
            if v:
                out[assign(r["Counterparty LEI"], r)]["derivatives"] += v
    return out


def ls_slope(y):
    return sum((x - 3.0) * (v - sum(y) / 5.0) for x, v in zip([1, 2, 3, 4, 5], y)) / 10.0


def approvable(limit_m, projected, req_m, ftype):
    ccf = 0.5 if ftype.lower().startswith("revolving") else 1.0
    room = limit_m * 1e6 - projected
    if room <= 0:
        return 0.0
    return min(req_m, math.floor(round(room / ccf / 1e5, 9)) / 10.0)


def run(pack, mode="restated", opt=None, group_opt=None):
    """mode: restated (every quarter on the 30 Sep 2026 archive), pit (each quarter on its own archive),
    rmcode (the customer master's group code at each extract), union / addonly variants for the ladder."""
    opt = opt or {}
    group_opt = group_opt or {}
    G30 = Groups(pack, PROJ, PROJ, **group_opt)
    req_top = {}
    for rq in pack.requests:
        req_top[rq["item"]] = G30.top(rq["lei"])
    series = {}
    books = {}
    for i, qe in enumerate(QES):
        if mode == "restated":
            assign = lambda lei, row: G30.top(lei)
        elif mode == "pit":
            Gq = Groups(pack, qe, qe, **group_opt)
            assign = lambda lei, row, Gq=Gq: Gq.top(lei)
        elif mode == "pit_current_archive_dates":
            Gq = Groups(pack, PROJ, qe, **group_opt)  # 30 Sep archive, membership at each quarter-end
            assign = lambda lei, row, Gq=Gq: Gq.top(lei)
        elif mode == "rmcode":
            code30 = {}
            for r in pack.loans:
                if r["extract_date"] == PROJ:
                    code30[r["customer_lei"]] = r["rm_group_code"]
            def assign(lei, row):
                if "rm_group_code" in row:
                    return row["rm_group_code"]
                return G30.top(lei)
        else:
            raise ValueError(mode)
        ex = exposures(pack, qe, assign, opt)
        for k, parts in ex.items():
            series.setdefault(k, [0.0] * 5)[i] = sum(parts.values())
            books.setdefault(k, [None] * 5)[i] = dict(parts)
    res = []
    for rq in pack.requests:
        top = req_top[rq["item"]]
        key = top
        if mode == "rmcode":
            key = [r["rm_group_code"] for r in pack.loans if r["extract_date"] == PROJ and r["customer_lei"] == rq["lei"]][0]
        y = series.get(key, [0.0] * 5)
        b = ls_slope(y)
        proj = y[-1] + b
        lim = pack.limits.get(top)
        res.append(dict(item=rq["item"], borrower=rq["borrower"], top=top, key=key, series=y, slope=b,
                        latest=y[-1], projected=proj, limit=lim, utilisation=proj / (lim * 1e6),
                        request=rq["amount"], ftype=rq["ftype"],
                        approvable=approvable(lim, proj, rq["amount"], rq["ftype"]),
                        books=books.get(key, [None] * 5)[-1]))
    return res


if __name__ == "__main__":
    p = Pack()
    for mode in ("restated", "pit", "rmcode"):
        print("==", mode)
        for r in run(p, mode):
            print("%-4s %-34s lim %6.1f  series %s  slope %7.3f  proj %8.3f  util %.4f  appr %5.1f" % (
                r["item"], r["borrower"][:34], r["limit"], [round(x / 1e6, 3) for x in r["series"]],
                r["slope"] / 1e6, r["projected"] / 1e6, r["utilisation"], r["approvable"]))
