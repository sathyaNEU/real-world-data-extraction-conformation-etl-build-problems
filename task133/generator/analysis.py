"""Every rung and variant of the main call, computed from target/ alone (task133 architecture 3)."""
import csv
import os
import re
from collections import defaultdict

import params as P

NON_SALES_TYPES = {"TFR", "INT", "LN"}


def norm(s):
    s = s.upper().replace(" LIMITED", " LTD").replace("&", "AND")
    s = re.sub(r"[^A-Z0-9 ()']", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s[:20].rstrip()


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class Pack:
    def __init__(self, tdir, scenario=None):
        self.tdir = tdir
        self.book = read_csv(os.path.join(tdir, "business_lending_book_2026-09-30.csv"))
        self.cred = read_csv(os.path.join(tdir, "operating_account_credits_2025-10_to_2026-09.csv"))
        self.reg = read_csv(os.path.join(tdir, "nzbn_extract_canterbury_otago_southland_2026-10-12.csv"))
        self.scen = scenario or dict(P.SCENARIO_CHANGE)
        self.by_nzbn = {r["nzbn"]: r for r in self.reg}
        legal, trade = {}, {}
        for r in self.reg:
            legal.setdefault(norm(r["entity_name"]), []).append(r)
            for t in filter(None, (x.strip() for x in r["trading_names"].split(";"))):
                trade.setdefault(norm(t), []).append(r)
        self.legal, self.trade = legal, trade
        cust = {}
        for f in self.book:
            c = cust.setdefault(f["customer_no"], dict(cust=f["customer_no"], name=f["customer_name"],
                                                        nzbn=f["nzbn"], code=f["industry_code"],
                                                        grade=f["risk_grade"], facs=[]))
            c["facs"].append(f)
        for c in cust.values():
            c["div"] = self.by_nzbn[c["nzbn"]]["bic_code"][0]
            c["bic"] = self.by_nzbn[c["nzbn"]]["bic_code"]
            c["own_party"] = norm(c["name"].replace(" Ltd", " Limited"))
        self.cust = cust

    # ------------------------------------------------------------------ classification of credits
    def classify(self, r, c, trading=True, acquirer_as_payer=False):
        """Return (kind, division) for a credit: kind in sales source or None for a credit that is not a sale."""
        tt = r["tran_type"]
        party = r["other_party"]
        part = r["particulars"].upper()
        if tt in NON_SALES_TYPES:
            return None, None
        if tt == "MS":
            if acquirer_as_payer:
                m = self.legal.get(norm(party + " LIMITED")) or self.legal.get(party)
                m = m or [x for k, v in self.legal.items() if k.startswith(party[:12]) for x in v]
                return "B2B", m[0]["bic_code"][0] if m else c["div"]
            return "HH", c["div"]
        if tt == "DEP":
            return "HH", c["div"]
        if party == "INLAND REVENUE DEPT" or part.startswith("GST REFUND"):
            return None, None
        if part.startswith("CLAIM"):
            return None, None
        if party == c["own_party"] or party == norm(c["name"]):
            return None, None
        m = self.legal.get(party)
        if not m and trading:
            m = self.trade.get(party)
        if m:
            if len(m) != 1:
                raise RuntimeError("ambiguous payer " + party)
            return "B2B", m[0]["bic_code"][0]
        return "PRIV", c["div"]

    def mixes(self, months=None, weight="value", trading=True, acquirer_as_payer=False, nonsales_in=False,
              private_out=False):
        """Sales by source division for each performing borrower."""
        out = defaultdict(lambda: defaultdict(float))
        for r in self.cred:
            c = self.cust.get(r["customer_no"])
            if c is None:
                continue
            if months:
                d, m, y = r["posted_date"].split("/")
                key = int(y) * 12 + int(m)
                if key < months:
                    continue
            kind, div = self.classify(r, c, trading=trading, acquirer_as_payer=acquirer_as_payer)
            if kind is None:
                if not nonsales_in:
                    continue
                kind, div = "HH", c["div"]
            if kind == "PRIV":
                if private_out:
                    continue
                kind = "HH"
            amt = float(r["amount_nzd"]) if weight == "value" else 1.0
            out[c["cust"]][(kind, div)] += amt
        return out

    # ------------------------------------------------------------------ the stress
    def ead(self, f):
        lim, dr = float(f["limit_nzd"]), float(f["drawn_nzd"])
        if f["product"] in P.REVOLVING:
            return dr + P.CCF_REVOLVING * max(0.0, lim - dr)
        return dr

    def change_from_mix(self, mix, c):
        tot = sum(mix.values())
        if tot <= 0:
            return self.scen[c["div"]]
        return sum(v * self.scen[d] for (k, d), v in mix.items()) / tot

    def loss(self, change_of, by="total"):
        tot = 0.0
        seg = defaultdict(float)
        per = {}
        for c in self.cust.values():
            if c["grade"] == "D":
                continue
            ch = change_of(c)
            m = P.multiplier(-ch)
            pd = min(1.0, P.GRADE_PD[int(c["grade"])] / 100.0 * m)
            l = sum(pd * P.LGD[f["security_code"]] * self.ead(f) for f in c["facs"])
            tot += l
            seg[P.SEG_OF[c["div"]]] += l
            per[c["cust"]] = (ch, m, l)
        return tot, dict(seg), per


def ladder(tdir, scenario=None):
    pk = Pack(tdir, scenario)
    res = {}
    mx = pk.mixes()
    res["golden"] = pk.loss(lambda c: pk.change_from_mix(mx[c["cust"]], c))
    res["R0_own_division"] = pk.loss(lambda c: pk.scen[c["div"]])
    # division-average mix (the book's heat map by own division)
    agg = defaultdict(lambda: defaultdict(float))
    for c in pk.cust.values():
        for k, v in mx[c["cust"]].items():
            agg[c["div"]][k[1] if k[0] == "B2B" else "HH"] += v
    def divavg(c):
        a = agg[c["div"]]
        t = sum(a.values())
        return sum(v * (pk.scen[c["div"]] if k == "HH" else pk.scen[k]) for k, v in a.items()) / t
    res["R1_division_average_mix"] = pk.loss(divavg)
    # class-level average mix (BIC class)
    aggc = defaultdict(lambda: defaultdict(float))
    for c in pk.cust.values():
        for k, v in mx[c["cust"]].items():
            aggc[c["bic"]][k[1] if k[0] == "B2B" else "HH"] += v
    def clsavg(c):
        a = aggc[c["bic"]]
        t = sum(a.values())
        return sum(v * (pk.scen[c["div"]] if k == "HH" else pk.scen[k]) for k, v in a.items()) / t
    res["V_class_average_mix"] = pk.loss(clsavg)
    mxc = pk.mixes(weight="count")
    res["V_count_weights"] = pk.loss(lambda c: pk.change_from_mix(mxc[c["cust"]], c))
    mxn = pk.mixes(nonsales_in=True)
    res["V_nonsales_included"] = pk.loss(lambda c: pk.change_from_mix(mxn[c["cust"]], c))
    mxa = pk.mixes(acquirer_as_payer=True)
    res["R2_acquirer_as_payer"] = pk.loss(lambda c: pk.change_from_mix(mxa[c["cust"]], c))
    mxt = pk.mixes(trading=False)
    res["V_legal_names_only"] = pk.loss(lambda c: pk.change_from_mix(mxt[c["cust"]], c))
    mx6 = pk.mixes(months=2026 * 12 + 4)
    res["V_last_six_months"] = pk.loss(lambda c: pk.change_from_mix(mx6[c["cust"]], c))
    mx3 = pk.mixes(months=2026 * 12 + 7)
    res["V_last_quarter"] = pk.loss(lambda c: pk.change_from_mix(mx3[c["cust"]], c))
    # government payers all read as public administration
    def govO(c):
        mixx = mx[c["cust"]]
        tot = sum(mixx.values())
        acc = 0.0
        for (k, d), v in mixx.items():
            acc += v * pk.scen["O" if (k == "B2B" and d in "KQ" and False) else d]
        return acc / tot
    gov_names = {norm(r["entity_name"]) for r in pk.reg if r["entity_type"] in ("Local Authority", "Crown Entity", "Government Department")}
    mxg = defaultdict(lambda: defaultdict(float))
    for r in pk.cred:
        c = pk.cust.get(r["customer_no"])
        if c is None:
            continue
        kind, div = pk.classify(r, c)
        if kind is None:
            continue
        if kind == "PRIV":
            kind = "HH"
        if r["other_party"] in gov_names:
            div = "O"
        mxg[c["cust"]][(kind, div)] += float(r["amount_nzd"])
    res["V_government_as_O"] = pk.loss(lambda c: pk.change_from_mix(mxg[c["cust"]], c))
    # the legacy 1993 code letters read as 2006 divisions for the borrower's own households
    def own_from_book(c):
        code = c["code"]
        if code and len(code) == 5:
            return code[0]
        return c["div"]
    def legacy(c):
        od = own_from_book(c)
        mixx = mx[c["cust"]]
        tot = sum(mixx.values())
        return sum(v * pk.scen[od if k == "HH" else d] for (k, d), v in mixx.items()) / tot
    res["V_legacy_letters"] = pk.loss(legacy)
    res["R3_more_severe_of_two"] = pk.loss(lambda c: min(pk.scen[c["div"]], pk.change_from_mix(mx[c["cust"]], c)))
    # households' spending read at the retail path whatever the borrower sells
    def hh_retail(c):
        mixx = mx[c["cust"]]
        tot = sum(mixx.values())
        return sum(v * pk.scen["G" if k == "HH" else d] for (k, d), v in mixx.items()) / tot
    res["V_households_at_retail"] = pk.loss(hh_retail)
    # private payers left out of the mix (only firms, card settlements and cash)
    mxp = pk.mixes(private_out=True)
    res["V_private_payers_left_out"] = pk.loss(lambda c: pk.change_from_mix(mxp[c["cust"]], c))
    return pk, res


if __name__ == "__main__":
    import sys
    pk, res = ladder(sys.argv[1])
    for k, (t, seg, per) in res.items():
        print(f"{k:28s} {t/1e6:8.3f}  " + "  ".join(f"{s[:12]}:{seg.get(s,0)/1e6:6.3f}" for s, _ in P.SEGMENTS))


# ====================================================================== the asks
def _d(s):
    import datetime as dt
    return dt.datetime.strptime(s, "%d/%m/%Y").date()


def _xlsx_rows(path, header_row):
    from openpyxl import load_workbook
    ws = load_workbook(path, data_only=True).active
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[header_row - 1]
    return [dict(zip(hdr, r)) for r in rows[header_row:] if any(v is not None for v in r)]


def half(d):
    if P.H1[0] <= d <= P.H1[1]:
        return "H1"
    if P.H2[0] <= d <= P.H2[1]:
        return "H2"
    return None


def ask_a(tdir, guarantors=True, agency_upload=False, pre_writeoff=False, reg=None):
    """Net credit losses on the business book by segment and half, NZD (written off less recovered)."""
    import datetime as dt
    reg = reg or read_csv(os.path.join(tdir, "nzbn_extract_canterbury_otago_southland_2026-10-12.csv"))
    by_nzbn = {r["nzbn"]: r for r in reg}
    cm = {r["customer_no"]: r for r in read_csv(os.path.join(tdir, "customer_master_extract_2026-10-09.csv"))}
    wo = [r for r in read_csv(os.path.join(tdir, "write_offs_2023-10_to_2026-09.csv")) if r["portfolio"] == "Business"]
    first = {}
    for r in wo:
        d = _d(r["posting_date"])
        first[r["customer_no"]] = min(first.get(r["customer_no"], d), d)
    cases = {r["case_no"]: r["customer_no"] for r in read_csv(os.path.join(tdir, "collections_cases_open_2026-09-30.csv"))}
    gmap = {r["guarantor_customer_no"]: r["guaranteed_customer_no"]
            for r in read_csv(os.path.join(tdir, "guarantees_register_2026-09-30.csv"))}

    def seg(c):
        return P.SEG_OF[by_nzbn[cm[c]["nzbn"]]["bic_code"][0]]
    net = {(s, h): 0.0 for s, _ in P.SEGMENTS for h in ("H1", "H2")}
    for r in wo:
        h = half(_d(r["posting_date"]))
        if h:
            net[(seg(r["customer_no"]), h)] += float(r["amount_nzd"])
    for r in _xlsx_rows(os.path.join(tdir, "collections_receipts_FY2026.xlsx"), 3):
        d = r["Receipt Date"].date() if hasattr(r["Receipt Date"], "date") else r["Receipt Date"]
        h = half(d)
        if not h:
            continue
        if r["Receipt Type"] == "Agency collection" and not agency_upload:
            continue
        owner = cases[r["Case No"]]
        if cm[owner]["customer_type"] == "Personal":
            if not guarantors or owner not in gmap:
                continue
            owner = gmap[owner]
        if owner not in first:
            continue
        if not pre_writeoff and d < first[owner]:
            continue
        net[(seg(owner), h)] -= float(r["Amount (NZD)"])
    return net


def ask_b(tdir, group_by_facility=True, rural=True, merges=True, overrides=True):
    """For each risk-grade band at 30 September 2025: borrowers, defaults in the following year, share."""
    import datetime as dt
    snap = read_csv(os.path.join(tdir, "risk_grade_snapshot_2025-09-30.csv"))
    grade = {r["customer_no"]: int(r["model_grade"]) for r in snap if r["model_grade"].isdigit()}
    asof = dt.date(2025, 9, 30)
    if overrides:
        for o in _xlsx_rows(os.path.join(tdir, "grade_overrides_2024-2026.xlsx"), 1):
            ap = o["Approved"].date() if hasattr(o["Approved"], "date") else o["Approved"]
            rm = o["Removed"].date() if hasattr(o["Removed"], "date") and o["Removed"] else None
            c = str(o["Customer No"])
            if c in grade and ap <= asof and (rm is None or rm > asof):
                grade[c] = int(o["Override Grade"])
    book = {r["facility_no"]: r["customer_no"] for r in read_csv(os.path.join(tdir, "business_lending_book_2026-09-30.csv"))}
    surv = {}
    if merges:
        surv = {r["surviving_customer_no"]: r["retired_customer_no"]
                for r in read_csv(os.path.join(tdir, "customer_merge_log_2026-03-14.csv"))}
    regs = ["default_register_business_FY2026.csv"] + (["default_register_rural_FY2026.csv"] if rural else [])
    dflt = set()
    lo, hi = dt.date(2025, 10, 1), dt.date(2026, 9, 30)
    for f in regs:
        for r in read_csv(os.path.join(tdir, f)):
            d = _d(r["default_date"])
            if not (lo <= d <= hi):
                continue
            c = r["customer_no"]
            if group_by_facility and r["facility_no"] in book:
                c = book[r["facility_no"]]
            c = surv.get(c, c)
            dflt.add(c)
    out = {}
    for b, (lo, hi) in enumerate([(1, 3), (4, 4), (5, 5), (6, 6), (7, 9)]):
        n = sum(1 for c, gg in grade.items() if lo <= gg <= hi)
        k = sum(1 for c, gg in grade.items() if lo <= gg <= hi and c in dflt)
        out[b] = (n, k, round(100.0 * k / n, 1) if n else None)
    return out
