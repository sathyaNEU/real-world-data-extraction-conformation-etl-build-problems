"""The payment world: every published payment over 500 pounds, April 2023 to the 25 February 2027 run,
the Tenancy Sustainment case ledger from July 2021, and the 2027/28 plan year simulated forward from
the same mechanics (never shipped; checks.py compares the shipped-data constructions against it).

Amounts are held in integer pence. A payment is a tuple:
  (dept, service_area, expense_type, supplier, vendor_no, date, net_p, vat_p, kind)
where kind tags the generating stream for the generator's own assertions (never written out).
"""
import datetime as dt
import math
import random
import zlib

import params as PR

DEPTS = {
    # code: (name, vat-bearing, invoices in range per year, decade weights (1k, 10k, 100k))
    "ASC": ("Adult Social Care", False, 21000, (0.74, 0.24, 0.02)),
    "HS": ("Housing Support", False, 3100, (0.62, 0.34, 0.04)),
    "CS": ("Children's Services", False, 6200, (0.60, 0.36, 0.04)),
    "PH": ("Public Health", False, 1500, (0.55, 0.38, 0.07)),
    "ED": ("Education & Skills", False, 3000, (0.58, 0.36, 0.06)),
    "HT": ("Highways & Transport", True, 7600, (0.50, 0.38, 0.12)),
    "WE": ("Waste & Environment", True, 11000, (0.62, 0.33, 0.05)),
    "PF": ("Property & Facilities", True, 11000, (0.55, 0.38, 0.07)),
    "CR": ("Corporate Resources", True, 4000, (0.60, 0.34, 0.06)),
    "FR": ("Fire & Rescue", True, 2100, (0.60, 0.34, 0.06)),
}
DEPT_ORDER = list(DEPTS)
VAT_MIX = {"HT": (0.80, 0.17, 0.03), "WE": (0.86, 0.12, 0.02), "PF": (0.78, 0.18, 0.04),
           "CR": (0.70, 0.27, 0.03), "FR": (0.75, 0.22, 0.03)}       # P(20%), P(0%), P(5%)
FLAGGED_2526 = {("ASC", 14), ("HS", 14), ("HT", 49), ("HT", 99), ("PF", 12)}

# Cell shape for each department's invoices: multiplies the Benford weight. Zero in its own flagged cells.
SHAPE = {d: {} for d in DEPTS}
for c in range(26, 39):
    SHAPE["ASC"][c] = 0.50
SHAPE["ASC"].update({13: 0.62, 15: 0.80, 16: 0.62, 18: 0.90, 20: 0.90, 30: 0.42, 32: 0.36, 35: 0.42, 45: 0.80})
SHAPE["WE"][11] = 1.15
SHAPE["PF"].update({15: 0.30, 16: 0.30, 18: 0.25, 19: 0.60})
for dept, c in FLAGGED_2526:
    SHAPE[dept][c] = 0.0
STEADY = {("WE", 11)}          # the run log's extra cell: held at its shape, no year-to-year noise

SERVICE = {
    "ASC": [("Residential & Nursing Care", "Residential care - independent sector", 0.30),
            ("Residential & Nursing Care", "Nursing care - independent sector", 0.18),
            ("Home Care", "Home care - framework providers", 0.24),
            ("Supported Living", "Supported living - spot purchase", 0.14),
            ("Day Opportunities", "Day services - external", 0.08),
            ("Equipment & Adaptations", "Community equipment", 0.06)],
    "HS": [("Supported Housing", "Supported accommodation - spot", 0.55),
           ("Homelessness Prevention", "Prevention fund payments", 0.30),
           ("Floating Support", "Floating support - spot", 0.15)],
    "CS": [("Children's Placements", "Independent fostering agencies", 0.35),
           ("Children's Placements", "Residential placements - external", 0.25),
           ("Early Help", "Commissioned early help services", 0.20),
           ("Fostering & Adoption", "Inter-agency adoption fees", 0.20)],
    "PH": [("Public Health", "Sexual health services", 0.40), ("Public Health", "Substance misuse services", 0.35),
           ("Public Health", "Health checks - GP practices", 0.25)],
    "ED": [("Education & Skills", "Independent special school fees", 0.45),
           ("Education & Skills", "Alternative provision", 0.30),
           ("Education & Skills", "Adult learning providers", 0.25)],
    "HT": [("Highways Maintenance", "Highways term contract - works orders", 0.45),
           ("Highways Maintenance", "Street lighting energy and maintenance", 0.15),
           ("Transport Services", "Supported bus services", 0.20),
           ("Highways Capital", "Capital works - contractors", 0.20)],
    "WE": [("Waste Disposal", "Waste disposal contract", 0.35), ("Waste Disposal", "Recycling credits", 0.25),
           ("Household Waste Recycling Centres", "HWRC operation", 0.25),
           ("Countryside & Environment", "Grounds and rights of way", 0.15)],
    "PF": [("Facilities Management", "Repairs and maintenance", 0.45), ("Facilities Management", "Utilities", 0.20),
           ("Estates", "Rents and service charges", 0.20), ("Property Capital", "Capital works - contractors", 0.15)],
    "CR": [("ICT", "Software licences and support", 0.40), ("Finance", "Professional fees", 0.20),
           ("HR & Payroll", "Agency staff", 0.25), ("Legal Services", "Counsel and external legal", 0.15)],
    "FR": [("Fire & Rescue", "Vehicles and equipment", 0.45), ("Fire & Rescue", "Training", 0.25),
           ("Fire & Rescue", "Premises", 0.30)],
}
REDACTED = "REDACTED - PERSONAL DATA"

_SYL_A = ["Quen", "Vell", "Tarn", "Wyss", "Orl", "Brend", "Caul", "Hesk", "Merr", "Skel", "Thwen", "Yeld", "Ferr",
          "Drax", "Lusk", "Pell", "Garn", "Ostr", "Kerr", "Wend", "Ambr", "Corv", "Halv", "Isk"]
_SYL_B = ["ingham", "ow", "ey", "stead", "mere", "brook", "holme", "ridge", "acre", "gate", "wold", "thorpe"]
_NOUN = {"ASC": ["Care", "Care Homes", "Homecare", "Living", "Healthcare", "Lodge"],
         "HS": ["Housing", "Homes Trust", "Housing Association", "Support"],
         "CS": ["Fostering", "Children's Homes", "Family Services", "Care"],
         "PH": ["Health", "Wellbeing", "Recovery Services", "Medical Practice"],
         "ED": ["School", "Learning", "College", "Education"],
         "HT": ["Civils", "Surfacing", "Highways", "Coaches", "Traffic Systems", "Plant Hire"],
         "WE": ["Recycling", "Haulage", "Environmental", "Waste Services", "Composting"],
         "PF": ["Facilities", "Building Services", "Electrical", "Cleaning", "Estates", "Energy"],
         "CR": ["Consulting", "Systems", "Recruitment", "Chambers", "Software"],
         "FR": ["Fire Engineering", "Safety", "Fleet", "Training"]}
_SUFFIX = ["Ltd", "Limited", "Ltd", "LLP", "Ltd", "CIC", "Ltd"]


class World:
    def __init__(self):
        self.rng = random.Random(PR.SEED)
        self.pay = []           # spine payments (published: net >= 500 or credit with |net| >= 500)
        self.tsp = []           # Tenancy Sustainment ledger rows
        self.carers = []        # (vendor_no, combo)
        self.vendor_seq = {"sup": 100230, "ind": 700410}
        self.suppliers = {d: [] for d in DEPTS}
        self.counters = {}

    def stream(self, name):
        """A separate seeded stream per component, so tuning one component never reshuffles another."""
        self.rng = random.Random(PR.SEED * 1000003 + zlib.crc32(name.encode()))
        return self.rng

    # ---------------------------------------------------------------- identities
    def new_vendor(self, kind):
        self.vendor_seq[kind] += self.rng.choice((1, 1, 2, 3, 7))
        return "%06d" % self.vendor_seq[kind]

    def build_suppliers(self):
        self.stream("suppliers")
        used = set()
        for d in DEPT_ORDER:
            n = {"ASC": 260, "WE": 120, "HT": 110, "PF": 120, "CS": 110, "CR": 90}.get(d, 60)
            while len(self.suppliers[d]) < n:
                nm = "%s%s %s %s" % (self.rng.choice(_SYL_A), self.rng.choice(_SYL_B), self.rng.choice(_NOUN[d]),
                                     self.rng.choice(_SUFFIX))
                if nm in used:
                    continue
                used.add(nm)
                self.suppliers[d].append((nm, self.new_vendor("sup")))

    def supplier(self, d):
        s = self.suppliers[d]
        # a long tail: a few suppliers carry most lines
        i = int(len(s) * (self.rng.random() ** 2.2))
        return s[i]

    # ---------------------------------------------------------------- helpers
    def add(self, dept, area, exp, sup, ven, date, gross_p, rate, kind):
        net = int(round(gross_p / (1 + rate)))
        vat = gross_p - net
        self.pay.append((dept, area, exp, sup, ven, date, net, vat, kind))

    def gross_in_cell(self, c, decade_w):
        j = self.rng.choices((2, 3, 4), weights=decade_w)[0]
        lo = c * 10 ** j * 100 + 7
        hi = (c + 1) * 10 ** j * 100 - 7
        return int(round(math.exp(self.rng.uniform(math.log(lo), math.log(hi)))))

    def vat_rate(self, dept):
        if not DEPTS[dept][1]:
            return 0.0
        p20, p0, p5 = VAT_MIX[dept]
        u = self.rng.random()
        return 0.20 if u < p20 else (0.0 if u < p20 + p0 else 0.05)

    def area(self, dept):
        rows = SERVICE[dept]
        r = self.rng.choices(rows, weights=[w for _, _, w in rows])[0]
        return r[0], r[1]

    # ---------------------------------------------------------------- streams
    def build_streams(self):
        a, b = PR.SPINE_FROM, PR.SPINE_TO
        rng = self.stream("carers")
        # Shared Lives carers
        for combo, n in PR.COMBOS:
            for _ in range(n):
                self.carers.append((self.new_vendor("ind"), combo))
        rng.shuffle(self.carers)
        self.sl_runs = PR.sl_runs(a, b)
        for d in self.sl_runs:
            for ven, combo in self.carers:
                self.add("ASC", "Shared Lives", "Shared Lives carer payments", REDACTED, ven, d,
                         100 * PR.carer_amount(combo, d), 0.0, "SL")
        # Shared Lives short-break claims: nights x nightly rate, kept out of cell 14
        rng = self.stream("short-breaks")
        self.sb_vendors = [self.new_vendor("ind") for _ in range(140)]
        for d in PR.creditor_runs(a, b):
            for _ in range(rng.choice((4, 5, 5, 6, 7))):
                while True:
                    rate = rng.choice(PR.SHORT_BREAK_NIGHTLY)
                    nights = rng.randint(7, 30)
                    amt = round(rate * nights, 2)
                    if PR.cell_of(amt) != 14 and amt >= 500:
                        break
                self.add("ASC", "Shared Lives", "Shared Lives short breaks", REDACTED, rng.choice(self.sb_vendors), d,
                         int(round(amt * 100)), 0.0, "SB")
        # Direct payments: 115 recipients in cell 14, and 420 others at fixed amounts away from the SL cells
        rng = self.stream("direct-payments")
        dp14 = [(self.new_vendor("ind"), rng.randint(140001, 149999)) for _ in range(PR.STREAMS["ASC_DP14"]["n"])]
        ok_cells = [c for c in range(10, 100) if c not in (13, 14, 15, 16, 18, 20) and not 26 <= c <= 38
                    and c != 45]
        w = [PR.P[c] for c in ok_cells]
        dpo = []
        ex = {c: 420 * x / sum(w) for c, x in zip(ok_cells, w)}
        nper = {c: int(e) for c, e in ex.items()}
        for c in sorted(ex, key=lambda c: -(ex[c] - nper[c]))[:420 - sum(nper.values())]:
            nper[c] += 1
        for c in ok_cells:
            for _ in range(nper[c]):
                dpo.append((self.new_vendor("ind"), rng.randint(c * 10000 + 7, (c + 1) * 10000 - 7)))
        for (y, m) in PR.months(a, b):
            d = PR.dp_date(y, m)
            if d > b:
                continue
            for ven, p in dp14:
                self.add("ASC", "Direct Payments", "Direct payments", REDACTED, ven, d, p, 0.0, "DP14")
            for ven, p in dpo:
                self.add("ASC", "Direct Payments", "Direct payments", REDACTED, ven, d, p, 0.0, "DPO")
        self.dp14, self.dpo = dp14, dpo
        # contract streams in the other flagged cells
        rng = self.stream("contracts")
        self.contracts = {}
        names = {"HS_FS14": ("HS", "Floating Support", "Floating support - block contracts"),
                 "HT_V49": ("HT", "Highways Maintenance", "Parish highway maintenance contracts"),
                 "HT_S99": ("HT", "Transport Services", "Traffic signal and ITS maintenance"),
                 "PF_C12": ("PF", "Facilities Management", "Cleaning contract - sites")}
        for key, (dept, area, exp) in names.items():
            s = PR.STREAMS[key]
            lst = []
            for _ in range(s["n"]):
                sup, ven = self.supplier(dept)
                lst.append((sup, ven, rng.randint(int(s["lo"] * 100) + 7, int(s["hi"] * 100) - 7)))
            self.contracts[key] = lst
            for (y, m) in PR.months(a, b):
                d = PR.contract_date(y, m, s["day"])
                if d > b:
                    continue
                for sup, ven, g in lst:
                    self.add(dept, area, exp, sup, ven, d, g, s["vat"], key)
        # Waste haulage per-load invoices in cell 11 until September 2024
        rng = self.stream("haulage")
        haul = [self.supplier("WE") for _ in range(3)]
        for (y, m) in PR.months(a, PR.WE_HAULAGE_END):
            runs = [d for d in PR.creditor_runs(dt.date(y, m, 1), PR.last_wd(y, m))]
            for i in range(52):
                sup, ven = haul[i % 3]
                self.add("WE", "Waste Disposal", "Bulk haulage - transfer stations", sup, ven, runs[i % len(runs)],
                         rng.randint(110007, 119993), 0.20, "HAUL")
        # Utility bills: net 1,500 to 1,599.99 at three VAT rates
        rng = self.stream("utilities")
        util = [self.supplier("PF") for _ in range(4)]
        for d0, d1 in [PR.FY[y] for y in ("2023/24", "2024/25", "2025/26", "2026/27")]:
            d1 = min(d1, b)
            runs = PR.creditor_runs(d0, d1)
            share = len(runs) / len(PR.creditor_runs(*PR.FY["2025/26"]))
            for rate, nb in ((0.0, 240), (0.05, 360), (0.20, 330)):
                for _ in range(int(round(nb * share))):
                    net = rng.randint(150007, 159993)
                    sup, ven = rng.choice(util)
                    self.pay.append(("PF", "Facilities Management", "Utilities", sup, ven, rng.choice(runs), net,
                                     int(round(net * rate)), "UTIL"))
        # payments of a million pounds or more
        rng = self.stream("large")
        pens = ("Wealdmoor Pension Fund", self.new_vendor("sup"))
        for (y, m) in PR.months(a, b):
            d = PR.contract_date(y, m, 19)
            if d <= b:
                self.add("CR", "Finance", "Pension fund contributions", pens[0], pens[1], d,
                         rng.randint(112000000, 138000000), 0.0, "BIG")
        for fy in ("2023/24", "2024/25", "2025/26", "2026/27"):
            d0, d1 = PR.FY[fy]
            runs = PR.creditor_runs(d0, min(d1, b))
            for dept, n in (("HT", 3), ("PF", 2)):
                for _ in range(n):
                    while True:
                        g = rng.randint(105000000, 420000000)
                        if (dept, PR.cell_of(g / 100)) not in FLAGGED_2526:
                            break
                    sup, ven = self.supplier(dept)
                    self.add(dept, "Highways Capital" if dept == "HT" else "Property Capital",
                             "Capital works - contractors", sup, ven, rng.choice(runs), g, 0.20, "BIG")
        # credit notes
        rng = self.stream("credits")
        for fy in ("2023/24", "2024/25", "2025/26", "2026/27"):
            d0, d1 = PR.FY[fy]
            runs = PR.creditor_runs(d0, min(d1, b))
            for _ in range(60):
                sup, ven = self.supplier("PF")
                net = -rng.randint(150007, 159993)
                self.pay.append(("PF", "Facilities Management", "Utilities", sup, ven, rng.choice(runs), net,
                                 int(round(net * 0.2)), "CRN"))
            for dept in DEPT_ORDER:
                if dept == "PF":
                    continue
                for _ in range(rng.randint(3, 8)):
                    sup, ven = self.supplier(dept)
                    area, exp = self.area(dept)
                    if DEPTS[dept][1]:
                        net = -rng.randint(50007, 82993)
                        self.pay.append((dept, area, exp, sup, ven, rng.choice(runs), net, int(round(net * 0.2)),
                                         "CRN"))
                    else:
                        self.add(dept, area, exp, sup, ven, rng.choice(runs), -rng.randint(50007, 99993), 0.0, "CRN")

    # ---------------------------------------------------------------- Tenancy Sustainment
    def build_tsp(self):
        rng = self.stream("tsp")
        self.households = []      # (case_ref, vendor, round, approved_on, amount_p, first (y, m))
        for label, cfg, tag in (("2021", PR.TSP_2021, "TS21"), ("2024-25", PR.TSP_2024, "TS24")):
            y, m = cfg["first"]
            k = 0
            for _ in range(cfg["months"]):
                for _ in range(cfg["per_month"]):
                    k += 1
                    appr = dt.date(y, m, rng.randint(1, 9))
                    while not PR.is_wd(appr):
                        appr += dt.timedelta(days=1)
                    self.households.append(("%s-%04d" % (tag, k + rng.randint(0, 3) * 0), self.new_vendor("ind"),
                                            label, appr, rng.randint(142000, 149000), (y, m)))
                m += 1
                if m == 13:
                    y, m = y + 1, 1
        for case, ven, label, appr, amt, (y, m) in self.households:
            for i in range(PR.TSP_TERM):
                d = PR.tsp_date(y, m)
                if d > PR.SPINE_TO:
                    break
                self.tsp.append((case, ven, label, appr, d, amt))
                if d >= PR.SPINE_FROM:
                    self.add("HS", "Tenancy Sustainment", "Tenancy sustainment payments", REDACTED, ven, d, amt,
                             0.0, "TSP")
                m += 1
                if m == 13:
                    y, m = y + 1, 1

    # ---------------------------------------------------------------- background invoices
    def build_background(self):
        ref_runs = len(PR.creditor_runs(*PR.FY["2025/26"]))
        existing = {}
        for p in self.pay:          # recurring background already placed (other direct payments, short breaks)
            if p[8] in ("DPO", "SB") and p[6] + p[7] >= 100000:
                k = (PR.fy_of(p[5]), p[0])
                c = PR.cell_of((p[6] + p[7]) / 100)
                existing.setdefault(k, {})
                existing[k][c] = existing[k].get(c, 0) + 1
        for fy in ("2023/24", "2024/25", "2025/26", "2026/27"):
            d0, d1 = PR.FY[fy]
            d1 = min(d1, PR.SPINE_TO)
            runs = PR.creditor_runs(d0, d1)
            share = len(runs) / ref_runs
            for dept in DEPT_ORDER:
                name, vat, n_inv, decw = DEPTS[dept]
                n = int(round(n_inv * share * (1 + 0.03 * (SCREEN_IDX.get(fy, 3) - 1))))
                rng = self.stream("noise-%s-%s" % (fy, dept))
                wts = {}
                for c in range(10, 100):
                    s = SHAPE[dept].get(c, 1.0)
                    if s > 0:
                        g = min(0.18, max(-0.40, rng.gauss(0, 0.16)))
                        wts[c] = PR.P[c] * s * (1.0 if (dept, c) in STEADY else math.exp(g))
                tot = sum(wts.values())
                have = existing.get((fy, dept), {})
                ntot = n + sum(have.values())
                exact = {c: max(0.0, ntot * w / tot - have.get(c, 0)) for c, w in wts.items()}
                scale = n / sum(exact.values())
                exact = {c: e * scale for c, e in exact.items()}
                cnt = {c: int(e) for c, e in exact.items()}
                rest = n - sum(cnt.values())
                for c in sorted(exact, key=lambda c: -(exact[c] - cnt[c]))[:rest]:
                    cnt[c] += 1
                rng = self.stream("invoices-%s-%s" % (fy, dept))
                for c in sorted(cnt):
                    for _ in range(cnt[c]):
                        g = self.gross_in_cell(c, decw)
                        sup, ven = self.supplier(dept)
                        area, exp = self.area(dept)
                        self.add(dept, area, exp, sup, ven, rng.choice(runs), g, self.vat_rate(dept), "INV")
                # published lines under 1,000 pounds gross (net 500 or more)
                for _ in range(int(round(0.20 * n))):
                    r = self.vat_rate(dept)
                    lo = int(50000 * (1 + r)) + 7
                    g = int(round(math.exp(rng.uniform(math.log(lo), math.log(99993)))))
                    sup, ven = self.supplier(dept)
                    area, exp = self.area(dept)
                    self.add(dept, area, exp, sup, ven, rng.choice(runs), g, r, "SUB")

    # ---------------------------------------------------------------- transaction references
    def finalise(self):
        self.pay.sort(key=lambda p: (p[5], DEPT_ORDER.index(p[0]), p[4], p[6]))
        rng = random.Random(PR.SEED * 7 + 1)
        ref = 5104471200
        out = []
        for p in self.pay:
            ref += rng.choice((1, 1, 1, 2, 3))
            out.append(p + (str(ref),))
        self.pay = out           # (dept, area, exp, supplier, vendor, date, net_p, vat_p, kind, ref)

    # ---------------------------------------------------------------- the plan year, simulated forward
    def plan_year(self, sl_rule="closure", hs_rule="runoff"):
        """Every 2027/28 payment in the flagged-cell streams (the world's own mechanics). Returns a list of
        (dept, gross_p, date, kind)."""
        a, b = PR.FY[PR.PLAN]
        out = []
        for d in PR.sl_runs(a, b):
            for ven, combo in self.carers:
                amt = PR.carer_amount(combo, d) if sl_rule == "closure" else PR.carer_amount(combo)
                if amt:
                    out.append(("ASC", 100 * amt, d, "SL"))
        for (y, m) in PR.months(a, b):
            for ven, p in self.dp14:
                out.append(("ASC", p, PR.dp_date(y, m), "DP14"))
            for ven, p in self.dpo:
                out.append(("ASC", p, PR.dp_date(y, m), "DPO"))
            for key, lst in self.contracts.items():
                s = PR.STREAMS[key]
                for sup, ven, g in lst:
                    out.append((s["dept"], g, PR.contract_date(y, m, s["day"]), key))
        for case, ven, label, appr, amt, (y, m) in self.households:
            for i in range(PR.TSP_TERM):
                d = PR.tsp_date(y, m)
                if a <= d <= b:
                    out.append(("HS", amt, d, "TSP"))
                m += 1
                if m == 13:
                    y, m = y + 1, 1
        return out

    def build(self):
        self.build_suppliers()
        self.build_streams()
        self.build_tsp()
        self.build_background()
        self.finalise()
        return self


SCREEN_IDX = {"2023/24": 0, "2024/25": 1, "2025/26": 2, "2026/27": 3}
