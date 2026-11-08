"""task127 architecture 4: Ruahine Bank's business book, 2021 to 2026, as one deterministic truth.

Every record the pack carries is drawn here from one seed: customers and their accounts, the 2023 core migration's
renumbering, the payment relations between customers (who pays whom, and how much of each customer's receipts),
defaults with their triggers and cures, the December 2024 and December 2026 IFRS 9 runs, the security register and
the guarantees. Nothing here knows the answer; golden.py computes it from the shipped files.
"""
import datetime as dt
import random
import zlib

SEED = 1272027
D = dt.date
ASOF = D(2027, 1, 22)
MIGRATION = D(2023, 6, 17)
RUN26 = D(2026, 12, 31)
RUN26_PUBLISHED = D(2027, 1, 15)
RUN24 = D(2024, 12, 31)
RUN24_CUTOFF = D(2024, 12, 20)
RUN24_PUBLISHED = D(2025, 1, 14)
START = D(2021, 1, 1)
END = D(2026, 12, 31)
ENVELOPE = 6_000_000
BANK = "47"

REGIONS = ["Manawatū-Whanganui", "Hawke's Bay", "Wellington", "Taranaki"]
SECTORS = {
    "A": "Agriculture, Forestry and Fishing", "C": "Manufacturing", "E": "Construction",
    "F": "Wholesale Trade", "G": "Retail Trade", "I": "Transport, Postal and Warehousing",
    "N": "Administrative and Support Services",
}
SECTOR_KEYS = list(SECTORS)

FIRST = ["Kinloch", "Ridgeway", "Marlowe", "Selwyn", "Brightwater", "Coastline", "Northgate", "Fernhill",
         "Glenmore", "Westbrook", "Ashworth", "Holloway", "Linwood", "Mangrove", "Oakridge", "Pinecrest",
         "Redcliffe", "Stonebridge", "Thornton", "Wexford", "Ashgrove", "Bellmont", "Carrick", "Dunmore",
         "Elmswood", "Fairlie", "Greystone", "Hatfield", "Ironbark", "Juniper", "Kilburn", "Larchmont",
         "Marlow", "Netherby", "Ormond", "Penrose", "Quarry Hill", "Rosedale", "Sandown", "Tamworth",
         "Upland", "Valebrook", "Waverley", "Yarrow", "Alderley", "Birchgrove", "Castlerock", "Denholm",
         "Eastfield", "Foxton Road", "Gladstone", "Highbury", "Inglewood Road", "Jarrow", "Kingsgate",
         "Lowther", "Milbrook", "Norwood", "Overton", "Parkhurst", "Ravensworth", "Southgate", "Tolworth",
         "Underwood", "Verity", "Whitmore", "Ashbourne", "Brackenridge", "Clearwater", "Driftwood",
         "Evergreen", "Fenwick", "Goldfield", "Harbourside", "Ivydale", "Kestrel", "Lakeview", "Moorfield",
         "Newstead", "Orchard Lane", "Pemberton", "Riverbend", "Silverdale", "Tidewater", "Woodstock"]
TRADE = {
    "A": ["Orchards", "Dairy Farms", "Contracting", "Forestry", "Growers", "Agricultural Services"],
    "C": ["Engineering", "Precast", "Joinery", "Foods", "Packaging", "Plastics", "Print", "Fabrication",
          "Metalworks", "Pallets", "Labels"],
    "E": ["Construction", "Builders", "Civil", "Roofing", "Plumbing", "Electrical", "Drainage"],
    "F": ["Distributors", "Wholesale", "Supplies", "Trading", "Imports"],
    "G": ["Motor Group", "Hardware", "Outdoor", "Furniture", "Retail", "Garden Centre"],
    "I": ["Freight", "Transport", "Haulage", "Cold Storage", "Logistics", "Couriers"],
    "N": ["Cleaning", "Labour Hire", "Security", "Facilities", "Staffing", "Waste Services"],
}

# The eight borrowers on the January 2027 watch list: (key, legal name, sector, region, date added, PD, line).
WATCH = [
    ("KIN", "Kinloch Engineering Limited", "C", "Manawatū-Whanganui", D(2026, 3, 18), 0.3807, 2_800_000),
    ("RID", "Ridgeway Precast Limited", "C", "Manawatū-Whanganui", D(2026, 5, 20), 0.4392, 2_500_000),
    ("MAT", "Matai Valley Foods Limited", "A", "Manawatū-Whanganui", D(2026, 8, 19), 0.4213, 3_000_000),
    ("HAR", "Marlowe Packhouse Limited", "A", "Hawke's Bay", D(2025, 11, 19), 0.3086, 3_400_000),
    ("SEL", "Selwyn Joinery Limited", "C", "Wellington", D(2026, 6, 17), 0.3611, 1_900_000),
    ("BRI", "Brightwater Motor Group Limited", "G", "Taranaki", D(2026, 9, 16), 0.2896, 1_400_000),
    ("COA", "Coastline Aggregates Limited", "E", "Taranaki", D(2026, 10, 21), 0.3304, 1_100_000),
    ("NOR", "Northgate Print Limited", "C", "Hawke's Bay", D(2026, 11, 18), 0.2712, 900_000),
]
WATCH_FACILITIES = {   # (product, limit, drawn, LGD); EAD = drawn for loans, drawn + 0.6 undrawn for revolving
    "KIN": [("Term loan", 4_200_000, 4_131_862.43, 0.45), ("Overdraft", 2_500_000, 2_093_418.77, 0.52),
            ("Equipment finance", 2_360_000, 2_309_774.15, 0.48)],
    "RID": [("Term loan", 3_900_000, 3_842_116.08, 0.47), ("Overdraft", 1_500_000, 1_371_640.52, 0.55),
            ("Equipment finance", 1_250_000, 1_221_387.90, 0.52)],
    "MAT": [("Term loan", 2_400_000, 2_361_905.31, 0.44), ("Revolving credit", 1_800_000, 1_547_233.86, 0.53)],
    "HAR": [("Commercial property loan", 4_300_000, 4_246_512.74, 0.40),
            ("Seasonal facility", 3_000_000, 2_871_055.20, 0.58)],
    "SEL": [("Term loan", 2_300_000, 2_262_448.96, 0.47), ("Overdraft", 1_700_000, 1_577_302.41, 0.52)],
    "BRI": [("Floor plan facility", 2_600_000, 2_336_917.65, 0.50), ("Term loan", 600_000, 589_213.08, 0.46)],
    "COA": [("Equipment finance", 1_400_000, 1_371_559.47, 0.49), ("Overdraft", 750_000, 603_184.19, 0.52)],
    "NOR": [("Term loan", 1_150_000, 1_141_806.52, 0.48), ("Overdraft", 600_000, 522_749.31, 0.52)],
}
# Ruahine borrowers that take most of their receipts from a watch-list borrower in 2026 (payer key: specs).
WATCH_PAYEES = {
    "MAT": [("Packaging", "C", 1_900_000, 0.50, 0.64), ("Cold Storage", "I", 2_600_000, 0.32, 0.71),
            ("Haulage", "I", 2_400_000, 0.45, 0.58), ("Cleaning", "N", 600_000, 0.62, 0.83),
            ("Engineering", "C", 1_100_000, 0.52, 0.52), ("Labour Hire", "N", 800_000, 0.65, 0.77),
            ("Labels", "C", 1_300_000, 0.50, 0.61), ("Pallets", "C", 1_300_000, 0.48, 0.55)],
    "RID": [("Haulage", "I", 520_000, 0.48, 0.53)],
}
WATCH_NONBORROWER_PAYEES = {"MAT": 2}
SEC_NUDGE = {"KIN": 5_000}      # keeps each security value clear of its thousand-dollar edge

# Payers whose default the record holds, with the payees that took most of their receipts from them.
ANCHORS = [  # (first trigger date, payees, payees defaulting after, months after for each default)
    (D(2022, 3, 9), 4, [3, 6]),
    (D(2022, 9, 21), 5, [2, 4, 7]),
    (D(2023, 2, 15), 4, [5]),
    (D(2023, 8, 30), 5, [3, 4]),
    (D(2024, 4, 17), 4, [2, 6]),
    (D(2024, 11, 6), 5, [4, 8]),
    (D(2025, 6, 11), 4, [3]),
]
# which of each payer's payees defaulted after it, by position in its payee list (default rate flat in receipt share)
ANCHOR_DEFAULTERS = [(1, 3), (1, 3, 4), (2,), (0, 4), (1, 3), (1, 3), (3,)]
N_SURVIVOR_PAYERS = 10
SURVIVOR_PAYEES = [4, 3, 4, 3, 4, 4, 3, 4, 3, 4]    # 36 payees
SURVIVOR_PAYEE_DEFAULTS = 5                          # over 2022-2025 dependent-years
N_ORDINARY = 300


def months(a, b):
    y, m = a.year, a.month
    out = []
    while (y, m) <= (b.year, b.month):
        out.append((y, m))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


MONTHS = months(START, END)


def add_months(d, k):
    y, m = d.year, d.month + k
    while m > 12:
        y, m = y + 1, m - 12
    while m < 1:
        y, m = y - 1, m + 12
    last = [31, 29 if y % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]
    return D(y, m, min(d.day, last))


class World:
    def __init__(self):
        self.r = random.Random(SEED)
        self.customers = {}       # cid -> dict
        self.used_names = set()
        self.next_cid = 104311
        self.next_acct = 0
        self.links = []           # payment relations: dict(payer, payee, share or weight, start, end)
        self.defaults = []        # dict(cid, first, triggers=[(kind, date)], cure)
        self.build()

    # ---- identities ------------------------------------------------------------------------------------
    def new_name(self, sector, base=None, trade=None):
        r = self.r
        for _ in range(500):
            b = base or r.choice(FIRST)
            t = trade or r.choice(TRADE[sector])
            k = r.random()
            if k < 0.58:
                n = "%s %s Limited" % (b, t)
            elif k < 0.68:
                n = "%s %s Ltd" % (b, t)
            elif k < 0.82:
                n = "%s %s (%d) Limited" % (b, t, r.randint(2003, 2019))
            elif k < 0.90:
                n = "%s & %s %s Limited" % (b, r.choice(FIRST), t)
            elif k < 0.95:
                n = "%s %s Limited" % (r.choice(["McKay", "Patel", "Hohaia", "Van Dyk", "Ferris", "Tuilagi", "Brennan",
                                                 "Okafor", "Sorensen", "Whitaker"]), r.choice(["Brothers", "and Sons", "Family"]) + " " + t)
            else:
                n = "%s %s Co-operative Limited" % (b, t)
            if n not in self.used_names:
                self.used_names.add(n)
                return n
            base = None
        raise RuntimeError("names exhausted")

    def nzbn(self):
        return "9429" + "".join(str(self.r.randint(0, 9)) for _ in range(9))

    def new_customer(self, name, sector, region, since, role, pd=None):
        cid = "C%06d" % self.next_cid
        self.next_cid += self.r.randint(3, 41)
        r = self.r
        import re as _re
        trading = _re.sub(r" \(\d{4}\)", "", name.replace(" Limited", "").replace(" Ltd", ""))
        if r.random() < 0.18:
            trading = trading.split(" ")[0] + " " + r.choice(["Group", "Services", "Co", "& Sons", "NZ"])
        c = dict(cid=cid, name=name, trading=trading, sector=sector, region=region, since=since, role=role,
                 nzbn=self.nzbn(), company_no=str(r.randint(1_000_000, 8_999_999)), pd=pd, former=[],
                 accounts=[], facilities=[], exit=None, turnover=None)
        self.customers[cid] = c
        self.open_accounts(c)
        return c

    def acct_numbers(self):
        self.next_acct += 1
        r = self.r
        old_branch = r.choice(["0610", "0612", "0615", "0618", "0622", "0630"])
        new_branch = {"0610": "1201", "0612": "1202", "0615": "1204", "0618": "1206", "0622": "1207",
                      "0630": "1209"}[old_branch]
        old = "%s-%s-%07d-%02d" % (BANK, old_branch, r.randint(100000, 9999999), r.choice([0, 0, 0, 1, 2]))
        new = "%s-%s-%07d-%03d" % (BANK, new_branch, r.randint(100000, 9999999), r.choice([0, 0, 0, 1, 2]))
        return old, new

    def open_accounts(self, c):
        r = self.r
        kinds = ["Business cheque"] + (["Business savings"] if r.random() < 0.55 else []) + \
                (["Tax holding"] if r.random() < 0.30 else [])
        for k in kinds:
            old, new = self.acct_numbers()
            opened = c["since"] if k == "Business cheque" else max(c["since"], add_months(c["since"], r.randint(0, 30)))
            c["accounts"].append(dict(kind=k, old=old if opened < MIGRATION else None, new=new, opened=opened,
                                      closed=None))

    # ---- the book --------------------------------------------------------------------------------------
    def build(self):
        r = self.r
        self.watch = {}
        for key, name, sec, reg, added, pd, line in WATCH:
            self.used_names.add(name)
            c = self.new_customer(name, sec, reg, D(2009 + r.randint(0, 9), r.randint(1, 12), r.randint(1, 27)),
                                  "watch", pd)
            c["key"], c["added"], c["line"] = key, added, line
            c["turnover"] = {"KIN": 19e6, "RID": 14e6, "MAT": 21e6, "HAR": 24e6, "SEL": 9e6, "BRI": 31e6,
                             "COA": 7e6, "NOR": 5e6}[key]
            self.watch[key] = c
        # watch-list payees (borrowers dependent on a watch-list borrower in 2026)
        self.watch_payees = {}
        for key, specs in WATCH_PAYEES.items():
            lst = []
            for trade, sec, ead, lgd, share in specs:
                nm = self.new_name(sec, trade=trade)
                c = self.new_customer(nm, sec, self.watch[key]["region"],
                                      D(2012 + r.randint(0, 9), r.randint(1, 12), r.randint(1, 27)), "payee",
                                      pd=round(r.uniform(0.020, 0.030), 4))
                c["target_ead"], c["target_lgd"], c["share"] = ead, lgd, share
                c["turnover"] = ead * r.uniform(1.6, 2.6)
                self.links.append(dict(payer=self.watch[key]["cid"], payee=c["cid"], share=share,
                                       start=max(START, c["since"]), end=END))
                lst.append(c)
            self.watch_payees[key] = lst
        for key, n in WATCH_NONBORROWER_PAYEES.items():
            for _ in range(n):
                sec = r.choice(["N", "I"])
                c = self.new_customer(self.new_name(sec), sec, self.watch[key]["region"], D(2016, r.randint(1, 12), 3),
                                      "nonborrower")
                c["share"] = round(r.uniform(0.55, 0.8), 2)
                c["turnover"] = r.uniform(0.4e6, 1.2e6)
                self.links.append(dict(payer=self.watch[key]["cid"], payee=c["cid"], share=c["share"], start=START, end=END))
        # anchors and their payees
        self.anchors = []
        for ai, (first, npay, dmonths) in enumerate(ANCHORS):
            sec = r.choice(["C", "F", "E", "I"])
            a = self.new_customer(self.new_name(sec), sec, r.choice(REGIONS),
                                  D(2006 + r.randint(0, 8), r.randint(1, 12), r.randint(1, 27)), "anchor",
                                  pd=round(r.uniform(0.05, 0.12), 4))
            a["turnover"] = r.uniform(12e6, 30e6)
            pays = []
            for i in range(npay):
                ps = r.choice(SECTOR_KEYS)
                p = self.new_customer(self.new_name(ps), ps, a["region"],
                                      D(2010 + r.randint(0, 9), r.randint(1, 12), r.randint(1, 27)), "apayee",
                                      pd=round(r.uniform(0.025, 0.045), 4))
                p["share"] = round(r.uniform(0.49, 0.84), 2)
                p["turnover"] = r.uniform(0.6e6, 4e6)
                self.links.append(dict(payer=a["cid"], payee=p["cid"], share=p["share"],
                                       start=max(START, p["since"]), end=first))
                pays.append(p)
            self.anchors.append(dict(c=a, first=first, payees=pays, dmonths=dmonths))
            self.add_default(a["cid"], first, kind="anchor", utp_first=True)
            for k, mo in enumerate(dmonths):
                p = pays[ANCHOR_DEFAULTERS[ai][k]]
                self.add_default(p["cid"], add_months(first, mo) + dt.timedelta(days=r.randint(-6, 6)), kind="contagion", utp_first=True)
        # survivor payers and their payees
        self.survivors = []
        for i in range(N_SURVIVOR_PAYERS):
            sec = r.choice(["C", "F", "E", "I", "A"])
            s = self.new_customer(self.new_name(sec), sec, r.choice(REGIONS),
                                  D(2004 + r.randint(0, 10), r.randint(1, 12), r.randint(1, 27)), "survivor",
                                  pd=round(r.uniform(0.008, 0.03), 4))
            s["turnover"] = r.uniform(15e6, 45e6)
            pays = []
            for j in range(SURVIVOR_PAYEES[i]):
                ps = r.choice(SECTOR_KEYS)
                p = self.new_customer(self.new_name(ps), ps, s["region"],
                                      D(2010 + r.randint(0, 9), r.randint(1, 12), r.randint(1, 27)), "spayee",
                                      pd=round(r.uniform(0.025, 0.045), 4))
                p["share"] = round(r.uniform(0.49, 0.84), 2)
                p["turnover"] = r.uniform(0.6e6, 4e6)
                self.links.append(dict(payer=s["cid"], payee=p["cid"], share=p["share"],
                                       start=max(START, p["since"]), end=END))
                pays.append(p)
            self.survivors.append(dict(c=s, payees=pays))
        allsp = [p for s in self.survivors for p in s["payees"]]
        picks = r.sample(allsp, SURVIVOR_PAYEE_DEFAULTS)
        years = [2022, 2023, 2024, 2025, 2023]
        for p, y in zip(picks, years):
            self.add_default(p["cid"], D(y, r.choice([3, 4, 5, 6, 7, 8, 9]), r.randint(2, 26)), kind="baseline_payee", utp_first=True)
        # ordinary borrowers
        for i in range(N_ORDINARY):
            sec = SECTOR_KEYS[i % len(SECTOR_KEYS)]
            c = self.new_customer(self.new_name(sec), sec, r.choice(REGIONS),
                                  D(2003 + r.randint(0, 20), r.randint(1, 12), r.randint(1, 27)), "ordinary",
                                  pd=self.draw_pd())
            if c["since"] > D(2024, 6, 30):
                c["since"] = D(2019, c["since"].month, c["since"].day)
                c["accounts"] = []
                self.open_accounts(c)
            c["turnover"] = r.lognormvariate(14.6, 0.75)
        self.remap_ids()
        self.ordinary_defaults()
        self.device_defaults()
        self.cures()
        self.exits()
        self.facilities()
        self.securities()
        self.guarantees()
        self.name_changes()

    def remap_ids(self):
        """Customer numbers were issued as customers joined the bank, so they carry no order of this build: every
        number is redrawn from the same range at random."""
        r = self.r
        old = sorted(self.customers)
        pool = sorted(set(r.sample(range(100_311, 196_000), len(old))))
        r.shuffle(pool)
        m = {o: "C%06d" % n for o, n in zip(old, pool)}
        new = {}
        for o in old:
            c = self.customers[o]
            c["cid"] = m[o]
            new[m[o]] = c
        self.customers = new
        for l in self.links:
            l["payer"], l["payee"] = m[l["payer"]], m[l["payee"]]
        for df in self.defaults:
            df["cid"] = m[df["cid"]]

    def draw_pd(self):
        r = self.r
        g = r.choices([0.004, 0.008, 0.015, 0.025, 0.04, 0.07, 0.12], [8, 16, 24, 24, 15, 9, 4])[0]
        return round(g * r.uniform(0.85, 1.15), 4)

    def add_default(self, cid, first, kind, utp_first=None, gap=None):
        r = self.r
        gap = gap if gap is not None else r.randint(12, 55)
        if utp_first is None:
            utp_first = r.random() < 0.45
        if utp_first:
            trig = [("UTP", first), ("90DPD", first + dt.timedelta(days=gap))]
        else:
            trig = [("90DPD", first)] + ([("UTP", first + dt.timedelta(days=gap))] if r.random() < 0.6 else [])
        self.defaults.append(dict(cid=cid, first=first, triggers=trig, cure=None, kind=kind))

    def ordinary_defaults(self):
        """Ordinary borrowers default at about their PD a year, never in the last three weeks of a year or the first
        five of the next (the turn of each year belongs to the sector table's own records), and never a payee."""
        r = self.r
        ords = [c for c in self.customers.values() if c["role"] == "ordinary"]
        self.ord_defaulted = set()
        for y in range(2021, 2027):
            for c in ords:
                if c["cid"] in self.ord_defaulted or c["since"] > D(y, 1, 1):
                    continue
                if r.random() < c["pd"] * 0.92:
                    while True:
                        d = D(y, r.randint(1, 12), r.randint(1, 28))
                        if not ((d.month == 12 and d.day >= 8) or (d.month == 1 and d.day <= 31) or
                                (d.month == 2 and d.day <= 4)):
                            break
                    self.add_default(c["cid"], d, kind="ordinary")
                    self.ord_defaulted.add(c["cid"])

    def device_defaults(self):
        """The sector table's own records at the turn of each year: unlikely-to-pay met in the last fortnight of a
        December with 90 days past due in the January after, one borrower per sector at the end of 2024 and four at
        the end of 2025."""
        r = self.r
        ords = sorted([c for c in self.customers.values() if c["role"] == "ordinary" and c["cid"] not in self.ord_defaulted
                       and c["since"] < D(2023, 1, 1)], key=lambda c: c["cid"])
        r.shuffle(ords)
        self.dev_c1 = []
        used = set()
        for sec in SECTOR_KEYS:
            c = next(x for x in ords if x["sector"] == sec and x["cid"] not in used)
            used.add(c["cid"])
            d = D(2024, 12, r.randint(21, 30))
            self.add_default(c["cid"], d, kind="device_c1", utp_first=True, gap=r.randint(26, 40))
            c["pd"] = round(r.uniform(0.09, 0.16), 4)
            self.dev_c1.append(c["cid"])
            self.ord_defaulted.add(c["cid"])
        self.dev_c1b = []
        for sec in r.sample(SECTOR_KEYS, 4):
            c = next(x for x in ords if x["sector"] == sec and x["cid"] not in used)
            used.add(c["cid"])
            d = D(2025, 12, r.randint(17, 30))
            self.add_default(c["cid"], d, kind="device_c1b", utp_first=True, gap=r.randint(26, 40))
            self.dev_c1b.append(c["cid"])
            self.ord_defaulted.add(c["cid"])
        self.dev_c3 = []
        for sec in SECTOR_KEYS:
            c = next(x for x in ords if x["sector"] == sec and x["cid"] not in used)
            used.add(c["cid"])
            d = D(2025, r.randint(2, 10), r.randint(2, 26))
            self.defaults.append(dict(cid=c["cid"], first=d, triggers=[("90DPD", d)], cure=None, kind="device_c3",
                                      loan_first=True))
            self.dev_c3.append(c["cid"])
            self.ord_defaulted.add(c["cid"])
        self.dev_used = used

    def cures(self):
        """About one default in six cures after a probation period. Every sector holds a borrower in default at the
        end of 2023 that cured during 2024, three of whom default again in 2025."""
        r = self.r
        ords = sorted([c for c in self.customers.values() if c["role"] == "ordinary" and c["cid"] not in self.ord_defaulted
                       and c["since"] < D(2022, 1, 1)], key=lambda c: c["cid"])
        r.shuffle(ords)
        self.dev_c2 = []
        for i, sec in enumerate(SECTOR_KEYS):
            c = next(x for x in ords if x["sector"] == sec and x["cid"] not in self.dev_used)
            self.dev_used.add(c["cid"])
            d = D(2023, r.randint(3, 10), r.randint(2, 26))
            self.add_default(c["cid"], d, kind="device_c2")
            cure = D(2024, r.randint(3, 10), r.randint(2, 26))
            self.defaults[-1]["cure"] = cure
            c["pd"] = round(r.uniform(0.06, 0.11), 4)
            self.dev_c2.append(c["cid"])
            self.ord_defaulted.add(c["cid"])
            if i in (1, 4, 5):
                d2 = D(2025, r.randint(3, 9), r.randint(2, 26))
                self.add_default(c["cid"], d2, kind="device_c2_redefault")
        # other cures among ordinary defaults (not at a year turn, not in 2024's book): realism
        for df in self.defaults:
            if df["kind"] == "ordinary" and df["cure"] is None and r.random() < 0.16 and df["first"] < D(2025, 6, 1):
                cure = df["first"] + dt.timedelta(days=r.randint(200, 420))
                if not ((cure.month == 12 and cure.day > 10) or (cure.month == 1)) and cure < D(2026, 11, 30):
                    df["cure"] = cure

    def exits(self):
        """A borrower in default and not cured leaves the book within a year (written off or repaid by sale)."""
        r = self.r
        for df in self.defaults:
            if df["cure"] is None:
                c = self.customers[df["cid"]]
                last = max(t[1] for t in df["triggers"])
                ex = last + dt.timedelta(days=r.randint(60, 330))
                if ex <= END:
                    c["exit"] = ex if c["exit"] is None else min(c["exit"], ex)
        for c in self.customers.values():
            if c["exit"]:
                for a in c["accounts"]:
                    a["closed"] = c["exit"]

    # ---- facilities and runs -----------------------------------------------------------------------------
    def facilities(self):
        r = self.r
        self.fac_seq = 2_204_117
        order = sorted(self.customers.values(), key=lambda x: x["cid"])
        r.shuffle(order)
        for c in order:
            if c["role"] == "nonborrower":
                continue
            if c["role"] == "watch":
                for prod, lim, drawn, lgd in WATCH_FACILITIES[c["key"]]:
                    self.add_fac(c, prod, lim, drawn, lgd)
                continue
            if c["role"] == "payee":
                ead, lgd = c["target_ead"], c["target_lgd"]
                h = zlib.crc32(c["cid"].encode())
                paid = 0.88 + 0.1 * ((h % 1000) / 1000.0)          # share of the original term loan still owed
                drawn1 = round(ead * 0.62 + (h % 9973) / 100.0, 2)
                lim1 = round(drawn1 / paid / 1000) * 1000
                self.add_fac(c, r.choice(["Term loan", "Equipment finance"]), lim1, drawn1, lgd)
                rest = ead - drawn1
                lim2 = round(rest / 0.94 / 1000) * 1000
                drawn2 = round((rest - 0.6 * lim2) / 0.4, 2)
                drawn2 = max(0, min(lim2, drawn2))
                self.add_fac(c, "Overdraft", lim2, drawn2, lgd)
                continue
            size = (c["turnover"] or 2e6) * r.uniform(0.15, 0.45)
            n = r.choice([1, 1, 2, 2, 3])
            prods = r.sample(["Term loan", "Overdraft", "Equipment finance", "Commercial property loan",
                              "Revolving credit"], n)
            if any(df["cid"] == c["cid"] and df.get("loan_first") for df in self.defaults) and \
                    not any(p in ("Term loan", "Equipment finance") for p in prods):
                prods = ["Term loan"] + prods[:2]
            for p in prods:
                lim = max(50_000, round(size / n * r.uniform(0.6, 1.4) / 1000) * 1000)
                h = zlib.crc32(("%s|%s" % (c["cid"], p)).encode())
                drawn = round(lim * (0.55 + 0.42 * (h % 10007) / 10007.0), 2) \
                    if p in ("Term loan", "Equipment finance", "Commercial property loan") else \
                    round(lim * r.uniform(0.2, 0.95) + (h % 9973) / 100.0 - 50.0, 2)
                lgd = {"Commercial property loan": r.uniform(0.25, 0.38), "Term loan": r.uniform(0.40, 0.52),
                       "Equipment finance": r.uniform(0.42, 0.55), "Overdraft": r.uniform(0.50, 0.62),
                       "Revolving credit": r.uniform(0.48, 0.60)}[p]
                self.add_fac(c, p, lim, drawn, round(lgd, 3))

    def add_fac(self, c, prod, lim, drawn, lgd):
        self.fac_seq += self.r.randint(7, 97)
        revolving = prod in ("Overdraft", "Revolving credit", "Seasonal facility", "Floor plan facility")
        ead = drawn + 0.6 * (lim - drawn) if revolving else drawn
        c["facilities"].append(dict(fid="F%07d" % self.fac_seq, product=prod, limit=lim, drawn=drawn,
                                    lgd=lgd, ead=round(ead, 2), revolving=revolving))

    # ---- security and guarantees -------------------------------------------------------------------------
    def securities(self):
        r = self.r
        self.props = []
        seq = 30_118
        valuers = ["Telfer Young", "Colliers", "JLL", "Bayleys Valuations", "Knight Frank", "Blackmore"]
        districts = {"Manawatū-Whanganui": "WN", "Hawke's Bay": "HBP", "Wellington": "WN", "Taranaki": "TN"}
        wl_props = {"KIN": 3, "RID": 2, "MAT": 2, "HAR": 3, "SEL": 1, "BRI": 2, "COA": 2, "NOR": 1}
        for c in sorted(self.customers.values(), key=lambda x: x["cid"]):
            if c["role"] == "nonborrower" or not c["facilities"]:
                continue
            if c["role"] == "watch":
                n = wl_props[c["key"]]
            elif r.random() < 0.55:
                n = r.choice([1, 1, 1, 2])
            else:
                continue
            for k in range(n):
                seq += r.randint(3, 29)
                ptype = r.choice(["Industrial", "Industrial", "Commercial"])
                # the date the valuation was made
                if c["role"] == "watch" and k == 0:
                    made = D(r.randint(2017, 2022), r.randint(1, 12), r.randint(1, 28))
                else:
                    made = D(r.randint(2016, 2026), r.randint(1, 12), r.randint(1, 28))
                    if made > D(2026, 10, 31):
                        made = D(2026, 6, made.day)
                amount = round(r.uniform(0.6e6, 4.5e6) / 5000) * 5000
                if c["role"] == "watch" and k == 0:
                    amount += SEC_NUDGE.get(c["key"], 0)
                valuer = r.choice(valuers)
                if r.random() < 0.6:
                    title = "%s%d%s/%d" % (districts[c["region"]], r.randint(10, 60), r.choice("ABCD"), r.randint(1, 999))
                else:
                    title = str(r.randint(100000, 999999))
                self.props.append(dict(sid="S%06d" % seq, cid=c["cid"], title=title, ptype=ptype,
                                       region=c["region"], amount=amount, made=made, valuer=valuer,
                                       address="%d %s %s" % (r.randint(2, 480), r.choice(FIRST),
                                                             r.choice(["Road", "Street", "Drive", "Place", "Avenue"])),
                                       priority=r.choice(["1st", "1st", "1st", "2nd"]),
                                       discharged=None, registered=made - dt.timedelta(days=r.randint(5, 60))))
        # properties sold in 2026: the mortgage discharged at Land Information, the register not updated
        wl_dis = {"RID": 1, "HAR": 1, "BRI": 1}
        for c in self.watch.values():
            if c["key"] in wl_dis:
                ps = [p for p in self.props if p["cid"] == c["cid"]]
                ps[-1]["discharged"] = D(2026, r.randint(3, 10), r.randint(2, 26))
        others = [p for p in self.props if self.customers[p["cid"]]["role"] not in ("watch",)]
        for p in r.sample(others, 9):
            p["discharged"] = D(2026, r.randint(2, 11), r.randint(2, 26))

    def guarantees(self):
        r = self.r
        self.guars = []
        self.deedlog = []
        seq = 7_412
        borrowers = sorted([c for c in self.customers.values() if c["facilities"] and c["role"] != "watch"],
                           key=lambda x: x["cid"])
        # each watch-list borrower's guarantees given: (guaranteed is a borrower; kind; amount; deed date; device)
        plan = {
            "KIN": [("unlimited", None, D(2014, 8, 12), "former"), ("limited", 400_000, D(2021, 3, 4), None)],
            "RID": [("limited", 650_000, D(2019, 5, 28), "released")],
            "MAT": [("limited", 750_000, D(2015, 10, 7), "former"), ("limited", 300_000, D(2022, 7, 19), None)],
            "HAR": [("unlimited", None, D(2018, 2, 26), "released"), ("limited", 500_000, D(2020, 9, 9), None)],
            "SEL": [("limited", 350_000, D(2013, 6, 18), "former")],
            "BRI": [("limited", 900_000, D(2017, 11, 21), "released"), ("unlimited", None, D(2023, 4, 3), None)],
            "COA": [("unlimited", None, D(2015, 3, 30), "former")],
            "NOR": [("limited", 250_000, D(2020, 1, 22), "released")],
        }
        self.guar_device = {}
        for c in self.watch.values():
            for kind, amt, deed, dev in plan[c["key"]]:
                g = r.choice([b for b in borrowers if b["region"] == c["region"] and len(b["facilities"]) <= 2])
                seq += r.randint(2, 17)
                gid = "G%05d" % seq
                rel = D(2026, r.randint(2, 10), r.randint(2, 26)) if dev == "released" else None
                self.guars.append(dict(gid=gid, guarantor=c["cid"], guaranteed=g["cid"], kind=kind, amount=amt,
                                       deed=deed, released=rel, device=dev))
                self.guar_device[gid] = dev
        # the rest of the book's guarantees (directors' companies), some released over the years
        for _ in range(130):
            a, b = r.sample(borrowers, 2)
            seq += r.randint(2, 17)
            deed = D(r.randint(2010, 2026), r.randint(1, 12), r.randint(1, 28))
            if deed > D(2026, 11, 30):
                deed = D(2026, 5, 4)
            kind = r.choice(["limited", "limited", "unlimited"])
            amt = round(r.uniform(100_000, 1_500_000) / 25_000) * 25_000 if kind == "limited" else None
            rel = None
            if r.random() < 0.18:
                rel = deed + dt.timedelta(days=r.randint(200, 2400))
                if rel > D(2026, 12, 15):
                    rel = None
            self.guars.append(dict(gid="G%05d" % seq, guarantor=a["cid"], guaranteed=b["cid"], kind=kind,
                                   amount=amt, deed=deed, released=rel, device=None))

    def name_changes(self):
        """Watch-list borrowers whose guarantee predates a change of name carry the former name on the deed; other
        companies changed name too."""
        r = self.r
        former = {"KIN": ("Kinloch Fabrication Limited", D(2017, 5, 2)),
                  "MAT": ("Matai Valley Meats Limited", D(2018, 9, 14)),
                  "SEL": ("Selwyn Kitchens Limited", D(2016, 2, 11)),
                  "COA": ("Coastline Quarries Limited", D(2019, 7, 8))}
        for key, (fn, chg) in former.items():
            self.watch[key]["former"].append((fn, chg))
        for c in r.sample(sorted(self.customers.values(), key=lambda x: x["cid"]), 24):
            if c["role"] == "watch" or c["former"]:
                continue
            b = c["name"].split(" ")[0]
            fn = "%s %s Limited" % (b, r.choice(["Holdings", "Enterprises", "Group", "Trading", "Services"]))
            if fn in self.used_names:
                continue
            self.used_names.add(fn)
            c["former"].append((fn, D(r.randint(2012, 2024), r.randint(1, 12), r.randint(1, 28))))


def build():
    return World()


if __name__ == "__main__":
    w = build()
    roles = {}
    for c in w.customers.values():
        roles[c["role"]] = roles.get(c["role"], 0) + 1
    print(roles, len(w.defaults), len(w.props), len(w.guars))
