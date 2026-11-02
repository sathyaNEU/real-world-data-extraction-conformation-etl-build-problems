"""Every number task485 grades, computed from the shipped files in target/ alone: the claims conformed (reversals
netted, both export layouts, the account renumbering), each product's fiscal 2026 net cost per 30-day supply with its
manufacturer's remittances traced to the product, the rungs below it, the rebate guarantee check and the members by
class and account."""
import collections
import csv
import datetime as dt
import os
import re

import numpy as np
from openpyxl import load_workbook

import pdftext

FILES = dict(claims="pbm_paid_claims_fy2026.csv", drug="pbm_drug_file_202610.xlsx",
             network="pharmacy_network_202610.txt", roster="member_roster_20261009.csv",
             policy="pdl_policy_eb-rx-04.pdf", review="clinical_review_2027_pdl.pdf",
             exhibit="pbm_agreement_exhibit_c.pdf", emails="pdl_2027_implementation_messages.pdf", rec25="rebate_guarantee_reconciliation_fy2025.pdf")
STMT_Q = ["2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2"]
for q in STMT_Q:
    FILES["stmt_" + q] = "rebate_remittance_%s.xlsx" % q

FQS = [("FQ1", dt.date(2025, 7, 1), dt.date(2025, 9, 30), "Jul-Sep 2025"),
       ("FQ2", dt.date(2025, 10, 1), dt.date(2025, 12, 31), "Oct-Dec 2025"),
       ("FQ3", dt.date(2026, 1, 1), dt.date(2026, 3, 31), "Jan-Mar 2026"),
       ("FQ4", dt.date(2026, 4, 1), dt.date(2026, 6, 30), "Apr-Jun 2026")]
SVC_FQ = {f[3]: f[0] for f in FQS}
ACCOUNTS = {"100": "State Agencies", "SEB01": "State Agencies", "200": "Higher Education", "SEB02": "Higher Education",
            "300": "Local Government", "SEB03": "Local Government", "400": "Non-Medicare Retirees",
            "SEB04": "Non-Medicare Retirees"}
ACC_ORDER = ["State Agencies", "Higher Education", "Local Government", "Non-Medicare Retirees"]
CHANNELS = ["RETAIL30", "RETAIL90", "MAIL", "SPECIALTY"]
CLASS_ORDER = ["GLP-1 receptor agonists", "SGLT2 inhibitors", "Long-acting insulins", "Direct oral anticoagulants",
               "Inhaled corticosteroid and LABA combinations", "Adalimumab products"]


def p(target, k):
    return os.path.join(target, FILES[k])


def parse_date(s):
    s = s.strip()
    if "/" in s:
        m, d, y = s.split("/")
        return dt.date(int(y), int(m), int(d))
    return dt.date.fromisoformat(s)


def ndc11(s):
    s = s.strip()
    if "-" in s:
        a, b, c = s.split("-")
        return a.zfill(5) + b.zfill(4) + c.zfill(2)
    return s.zfill(11)


def fq_of(d):
    for k, a, b, _ in FQS:
        if a <= d <= b:
            return k
    return None


def norm_mfr(name):
    s = re.sub(r"[^A-Z ]", " ", name.upper())
    drop = {"INC", "LLC", "USA", "US", "CORP", "CO", "LTD", "PHARMA", "PHARMACEUTICALS", "THERAPEUTICS", "LABORATORIES",
            "BIOSCIENCES", "BIOLOGICS"}
    return " ".join(t for t in s.split() if t not in drop)


def load(target):
    """The conformed pack."""
    D = {}
    # drug file
    wb = load_workbook(p(target, "drug"), read_only=True)
    ws = wb["Drug File"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[0]
    drug = {}
    for r in rows[1:]:
        rec = dict(zip(hdr, r))
        drug[str(rec["NDC"]).zfill(11)] = rec
    D["drug"] = drug
    # clinical review: the products compared and their 30-day supply
    D["review"] = review_tables(p(target, "review"), drug)
    # pharmacies (the network file is the network on 1 October 2026)
    net = {}
    with open(p(target, "network"), encoding="utf-8") as f:
        rd = csv.DictReader(f, delimiter="|")
        for r in rd:
            net[r["NPI"]] = r
    D["network"] = net
    # claims, reversals netted
    paid, rev = {}, {}
    with open(p(target, "claims"), encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            rec = dict(no=r["claim_number"], status=r["claim_status"], rev_of=r["reversal_of"],
                       dos=parse_date(r["date_of_service"]), paid=parse_date(r["date_paid"]), group=r["group_id"],
                       card=r["cardholder_id"], pc=r["person_code"], dob=parse_date(r["patient_dob"]),
                       sex=r["patient_gender"], npi=r["pharmacy_npi"], ndc=ndc11(r["ndc"]),
                       qty=float(r["quantity_dispensed"]), ds=int(r["days_supply"]),
                       compound=r["compound_code"] == "2", ingr=float(r["ingredient_cost_paid"]),
                       fee=float(r["dispensing_fee_paid"]), pay=float(r["patient_pay_amount"]),
                       plan=float(r["plan_paid_amount"]))
            if rec["status"] == "R":
                rev[rec["rev_of"]] = rec
            else:
                paid[rec["no"]] = rec
    D["claims_all"] = list(paid.values())
    D["reversed"] = set(rev)
    D["claims"] = [c for c in paid.values() if c["no"] not in rev]
    for c in D["claims_all"]:
        c["acct"] = ACCOUNTS[c["group"]]
        c["fq"] = fq_of(c["dos"])
        d = drug[c["ndc"]]
        c["labeler"] = d["Labeler Name"]
        c["brand"] = d["Proprietary Name"]
    # remittance statements
    D["stmt"] = []
    for q in STMT_Q:
        wb = load_workbook(p(target, "stmt_" + q), read_only=True)
        ws = wb["Remittance"]
        rows = list(ws.iter_rows(values_only=True))
        h = [i for i, r in enumerate(rows) if r and r[0] == "Manufacturer"][0]
        for r in rows[h + 1:]:
            if not r or not r[0] or r[0] == "Total remitted":
                continue
            D["stmt"].append(dict(stmt=q, mfr=r[0], code=str(r[1]), acct=ACCOUNTS[str(r[1])], kind=r[3], svc=r[4],
                                  amount=float(r[5])))
    # manufacturer names: statement name -> labeler name on the drug file
    labs = {norm_mfr(v["Labeler Name"]): v["Labeler Name"] for v in drug.values()}
    D["mfr_map"] = {l["mfr"]: labs[norm_mfr(l["mfr"])] for l in D["stmt"]}
    for l in D["stmt"]:
        l["labeler"] = D["mfr_map"][l["mfr"]]
        l["fq"] = SVC_FQ.get(l["svc"])
    # roster
    with open(p(target, "roster"), encoding="utf-8") as f:
        D["roster"] = list(csv.DictReader(f))
    return D


def review_tables(path, drug):
    """Table 1 (class, products compared) and Table 2 (product, 30-day supply) from the clinical review's text."""
    ls = pdftext.lines(path)
    txt = " ".join(ls)
    brands = {v["Proprietary Name"]: v for v in drug.values()}
    classes = ["GLP-1 receptor agonists", "SGLT2 inhibitors", "Long-acting insulins", "Direct oral anticoagulants",
               "Inhaled corticosteroid and LABA combinations", "Adalimumab products"]
    t1 = txt[txt.index("Products compared"):txt.index("2. The 30-day supply")]
    pos = [(t1.index(c), c) for c in classes]
    pos.sort()
    compared = {}
    for i, (at, c) in enumerate(pos):
        seg = t1[at: pos[i + 1][0] if i + 1 < len(pos) else len(t1)]
        compared[c] = [b for b in brands if re.search(r"(?<![\w-])%s \(" % re.escape(b), seg)]
    t2 = txt[txt.index("30-day supply (quantity)"):]
    per30 = {}
    for b in sorted(brands, key=len, reverse=True):
        m = re.search(r"(?<![\w-])%s\s+(.+?)\s+([\d.]+)\s+(each|mL|g)\b" % re.escape(b), t2)
        if m and b not in per30:
            per30[b] = float(m.group(2))
    return dict(compared=compared, per30=per30)


def thirty(c, per30):
    return c["qty"] / per30[c["brand"]]


def exhibit_rates(target):
    """Exhibit C, C.4: the guaranteed rebate per brand claim by channel, read from the agreement's table."""
    txt = pdftext.text(p(target, "exhibit"))
    pats = dict(RETAIL30=r"Retail, days supply under 84\s+([\d,]+\.\d\d)", RETAIL90=r"Retail, days supply 84 or more\s+([\d,]+\.\d\d)",
                MAIL=r"Mail order\s+([\d,]+\.\d\d)", SPECIALTY=r"Specialty\s+([\d,]+\.\d\d)")
    return {k: float(re.search(v, txt).group(1).replace(",", "")) for k, v in pats.items()}


STMT_FQ = {"2025Q3": "FQ1", "2025Q4": "FQ2", "2026Q1": "FQ3", "2026Q2": "FQ4"}     # a statement's own invoice quarter
LAG_FQ = {"2025Q2": "FQ1", "2025Q3": "FQ2", "2025Q4": "FQ3", "2026Q1": "FQ4"}      # the fiscal quarter it was remitted in


class Pack:
    """The conformed pack. setup() sets the conventions every figure is built under; the defaults are the golden's,
    and checks.py calls it with one convention changed at a time to show what each moves."""

    def __init__(self, target):
        self.D = load(target)
        D = self.D
        self.per30 = D["review"]["per30"]
        self.classes = D["review"]["compared"]
        self.compared = [b for c in self.classes.values() for b in c]
        self.labeler_of = {v["Proprietary Name"]: v["Labeler Name"] for v in D["drug"].values()}
        # a 30-day supply for every brand the claims carry: the review's quantity for the compared products, the
        # package quantity for the rest (they enter only the attribution, never a graded figure)
        self.units30 = dict(self.per30)
        for v in D["drug"].values():
            self.units30.setdefault(v["Proprietary Name"], float(v["Package Quantity"]))
        self.setup()

    def setup(self, netting="net", cost="ingr", units="review", window="dos", remit="service", accounts="mapped",
              compounds="out"):
        D = self.D
        self.opts = dict(netting=netting, cost=cost, units=units, window=window, remit=remit, accounts=accounts,
                         compounds=compounds)
        claims = D["claims"] if netting == "net" else D["claims_all"]
        if window == "paid":
            claims = [c for c in claims if dt.date(2025, 7, 1) <= c["paid"] <= dt.date(2026, 6, 30)]
        self.claims = claims
        self.accts = list(ACC_ORDER) if accounts == "mapped" else sorted(set(ACCOUNTS))

        def acct(c):
            return c["acct"] if accounts == "mapped" else c["group"]

        def costv(c):
            return dict(ingr=c["ingr"], ingr_fee=c["ingr"] + c["fee"], plan=c["plan"],
                        ingr_less_pay=c["ingr"] - c["pay"])[cost]

        def unitv(c):
            if units == "review":
                return c["qty"] / self.units30[c["brand"]]
            if units == "days":
                return c["ds"] / 30.0
            return 1.0
        # per brand: cost and 30-day supplies on the fiscal year's claims
        self.ingr = collections.defaultdict(float)
        self.u30 = collections.defaultdict(float)
        self.cell = collections.defaultdict(float)          # (brand, account, fq) -> 30-day supplies invoiced
        self.cell_cost = collections.defaultdict(float)
        for c in claims:
            u = unitv(c)
            if c["fq"] is None:
                continue
            self.ingr[c["brand"]] += costv(c)
            self.u30[c["brand"]] += u
            if not c["compound"] or compounds == "in":
                self.cell[(c["brand"], acct(c), c["fq"])] += u
                self.cell_cost[(c["brand"], acct(c), c["fq"])] += costv(c)
        # rebates by manufacturer, account and fiscal quarter
        self.reb = collections.defaultdict(float)
        for l in D["stmt"]:
            a = l["acct"] if accounts == "mapped" else l["code"]
            if remit == "service":
                f = l["fq"]
            elif remit == "cur":
                f = l["fq"] if l["kind"] == "Current Quarter" else None
            elif remit == "fy25":
                f = l["fq"] or ("FQ1" if l["stmt"] in ("2025Q2", "2025Q3") else None)
            elif remit == "statement":
                f = STMT_FQ.get(l["stmt"])
            elif remit == "received":
                f = LAG_FQ.get(l["stmt"])
            if f is None:
                continue
            self.reb[(l["labeler"], a, f)] += l["amount"]
        self.labelers = sorted({l["labeler"] for l in D["stmt"]})
        self.brands_of = collections.defaultdict(list)
        for b in sorted(self.u30):
            self.brands_of[self.labeler_of[b]].append(b)
        return self

    # ---- attribution of each manufacturer's remittances to its products ----
    def fit(self, basis="units", accounts=True, brands=None):
        """Least squares of each manufacturer's remittances (per account and fiscal quarter of service) on its
        products' 30-day supplies (or ingredient cost) in the same cells; returns each product's fiscal-year rebate
        dollars and its rebate per unit of basis."""
        out, rate = {}, {}
        fqs = [f[0] for f in FQS]
        for lab in self.labelers:
            bs = [b for b in self.brands_of[lab] if (brands is None or b in brands)]
            if not bs:
                continue
            cells = [(a, f) for a in self.accts for f in fqs] if accounts else [(None, f) for f in fqs]
            src = self.cell if basis == "units" else self.cell_cost

            def xv(b, a, f):
                return sum(src[(b, aa, f)] for aa in (self.accts if a is None else [a]))

            def yv(a, f):
                return sum(self.reb[(lab, aa, f)] for aa in (self.accts if a is None else [a]))
            X = np.array([[xv(b, a, f) for b in bs] for a, f in cells])
            Y = np.array([yv(a, f) for a, f in cells])
            beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
            for b, be in zip(bs, beta):
                tot = sum(src[(b, a, f)] for a in self.accts for f in fqs)
                out[b] = float(be * tot)
                rate[b] = float(be)
        return out, rate

    def prorata(self, basis="cost", cellwise=False):
        """Each manufacturer's fiscal-year remittances spread over its products in proportion to their ingredient
        cost (or 30-day supplies), the attribution a rebate report uses."""
        out = collections.defaultdict(float)
        fqs = [f[0] for f in FQS]
        for lab in self.labelers:
            bs = self.brands_of[lab]
            if not bs:
                continue
            if not cellwise:
                R = sum(self.reb[(lab, a, f)] for a in self.accts for f in fqs)
                wts = {b: (self.ingr[b] if basis == "cost" else self.u30[b]) for b in bs}
                s = sum(wts.values())
                for b in bs:
                    out[b] += R * wts[b] / s
            else:
                for a in self.accts:
                    for f in fqs:
                        R = self.reb[(lab, a, f)]
                        wts = {b: self.cell_cost[(b, a, f)] for b in bs}
                        s = sum(wts.values())
                        for b in bs:
                            out[b] += R * wts[b] / s if s else 0.0
        return dict(out)

    def net(self, rebates):
        return {b: (self.ingr[b] - rebates.get(b, 0.0)) / self.u30[b] for b in self.compared}

    def picks(self, net):
        out = {}
        for c, bs in self.classes.items():
            s = sorted(bs, key=lambda b: net[b])
            out[c] = dict(pick=s[0], runner=s[1], gap=net[s[1]] - net[s[0]], ratio=net[s[1]] / net[s[0]])
        return out

    def golden(self):
        reb, rate = self.fit()
        net = self.net(reb)
        return dict(rebates=reb, rate=rate, net=net, picks=self.picks(net))

    # ---- the rebate guarantee check (Exhibit C, C.4) ----
    def guarantee(self, rates, channel=None, remit="service"):
        channel = channel or self.channel
        out = {}
        for k, a, b, svc in FQS:
            n = collections.Counter()
            for c in self.claims:
                if c["fq"] != k or c["compound"]:
                    continue
                n[channel(c)] += 1
            g = sum(n[ch] * rates[ch] for ch in CHANNELS)
            if remit == "service":
                rem = sum(l["amount"] for l in self.D["stmt"] if l["fq"] == k)
            else:
                rem = sum(l["amount"] for l in self.D["stmt"] if STMT_FQ.get(l["stmt"]) == k)
            out[k] = dict(n={ch: n[ch] for ch in CHANNELS}, guarantee=round(g, 2), remitted=round(rem, 2),
                          shortfall=round(max(0.0, g - rem), 2))
        return out

    def channel(self, c):
        """The network of the dispensing pharmacy on the date of service (Exhibit C, C.5). The network file holds each
        pharmacy's network on 1 October 2026; a claim adjudicated in the retail network carries the retail dispensing
        fee, which is how a pharmacy's earlier network shows where it has since moved."""
        net = self.D["network"][c["npi"]]["NETWORK"]
        if c["fee"] > 0:
            net = "RETAIL"
        if net == "RETAIL":
            return "RETAIL90" if c["ds"] >= 84 else "RETAIL30"
        return net

    def channel_file(self, c):
        """The network file read as the network on every date of service."""
        net = self.D["network"][c["npi"]]["NETWORK"]
        if net == "RETAIL":
            return "RETAIL90" if c["ds"] >= 84 else "RETAIL30"
        return net

    # ---- members with a paid claim in each class, by account ----
    def persons(self):
        roster = self.D["roster"]
        by_legacy = {}
        fam = collections.defaultdict(list)
        for r in roster:
            fam[r["cardholder_id"]].append(r)
            if r["legacy_cardholder_id"]:
                by_legacy[r["legacy_cardholder_id"]] = r["cardholder_id"]
        ident = {}
        for c in self.D["claims_all"]:
            if c["dos"] >= dt.date(2026, 1, 1):
                ident[c["no"]] = ("N", c["card"], c["pc"])
                continue
            new = by_legacy.get(c["card"])
            hit = None
            if new:
                for r in fam[new]:
                    if parse_date(r["birth_date"]) == c["dob"] and r["gender"] == c["sex"]:
                        hit = ("N", new, r["person_code"])
                        break
            ident[c["no"]] = hit or ("O", c["card"], c["pc"])
        return ident

    def members(self, ident=None):
        ident = ident or self.persons()
        out = {}
        for cname, bs in self.classes.items():
            for a in ACC_ORDER:
                s = {ident[c["no"]] for c in self.claims if c["brand"] in bs and c["acct"] == a}
                out[(cname, a)] = len(s)
        return out
