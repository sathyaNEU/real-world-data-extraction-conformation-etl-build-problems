"""task446 world: a UK bank's obligor universe, its GLEIF hierarchy over five quarter-ends, and its
three booking systems. Deterministic (numpy default_rng(446)). Nothing here reads target/."""
import datetime as dt
import string
import numpy as np

SEED = 446
QE = [dt.date(2025, 9, 30), dt.date(2025, 12, 31), dt.date(2026, 3, 31), dt.date(2026, 6, 30),
      dt.date(2026, 9, 30)]
PROJ_DATE = QE[-1]
ARCHIVE_DATES = QE
LOUS = {"GB": "213800WAVVOPS85N2205", "US": "5493001KJTIIGC8Y1R12", "DE": "529900T8BM49AURSDO55",
        "NL": "5493001KJTIIGC8Y1R12", "IE": "635400AKJBGNS5WNQL34", "LU": "222100T6ICDIY8V4VX70",
        "FR": "969500Q2MA9VBQ8BG884"}
ALNUM = string.ascii_uppercase + string.digits
CCF_COMMITTED = 0.5

# ---------------------------------------------------------------- identifiers

def lei_check(body18):
    num = int("".join(str(int(c, 36)) for c in body18 + "00"))
    return "%02d" % (98 - num % 97)


def make_lei(rng, prefix, used):
    while True:
        body = prefix + "".join(rng.choice(list(ALNUM), 14))
        lei = body + lei_check(body)
        if lei not in used:
            used.add(lei)
            return lei


def isin_check(body11):
    digits = "".join(str(int(c, 36)) for c in body11)
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return str((10 - total % 10) % 10)


def make_isin(rng, cc, used):
    while True:
        body = cc + "".join(rng.choice(list(ALNUM), 9))
        isin = body + isin_check(body)
        if isin not in used:
            used.add(isin)
            return isin


# ---------------------------------------------------------------- names
PLACES = """Ashcombe Blackmoor Carrow Dunmere Elstow Farley Gillow Hatherden Ickford Jarrow Kettleby
Lindale Marrick Nettlecombe Ottery Padley Quarrington Rathmell Skelwith Thursby Upwey Varley Wenlock
Yarford Allerdale Bramwith Coldridge Denholme Eskdale Fenwick Garside Holbeck Ingleby Kirkham Langbar
Maltby Newbold Orrell Pickering Redmire Saltash Tadley Ulverley Walbury Aysgarth Birtley Cleeve
Dallow Easby Fulwood Grassby Hensall Kilnsey Ludworth Melling Norland Oxley Penrose Rudby Silsden
Tollard Uffington Wharram Arkholme Bolsover Cawood Draycott Embsay Fewston Glaisdale Hornby Lowther
Middridge Nunthorpe Osmotherley Preston Ravensworth Sedbergh Thornaby Wycliffe Asenby Brompton
Crayke Dalby Ellerby Flaxby Gilling Hovingham Kepwick Lastingham Marton Nunnington Oswaldkirk
Pockley Ryton Scackleton Terrington Welburn Yearsley Ampleforth Brandsby Coxwold Dalton Easingwold
Fadmoor Hawnby Kilburn Laskill Murton""".split()
SECTORS = [("Engineering", "28"), ("Foods", "10"), ("Logistics", "49"), ("Construction", "41"),
           ("Plastics", "22"), ("Packaging", "17"), ("Healthcare", "86"), ("Retail", "47"),
           ("Software", "62"), ("Property", "68"), ("Energy", "35"), ("Chemicals", "20"),
           ("Textiles", "13"), ("Hotels", "55"), ("Brewing", "11"), ("Printing", "18"),
           ("Metals", "24"), ("Facilities", "81"), ("Telecom", "61"), ("Marine", "50")]
SUFFIX_SUB = ["Ltd", "Ltd", "Ltd", "Limited", "Services Ltd", "Operations Ltd", "UK Ltd"]
DE_WORDS = ["Werke", "Technik", "Systeme", "Antriebe", "Logistik", "Industrie"]


class World:
    def __init__(self):
        self.rng = np.random.default_rng(SEED)
        self.used_lei = set()
        self.used_isin = set()
        self.ent = {}       # lei -> dict
        self.rel = []       # relationship records
        self.repex = []     # reporting exceptions (lei, category, reason)
        self.fac = []       # facilities
        self.sec = []       # securities issues held
        self.drv = []       # derivative netting sets
        self.groups = {}    # group key -> dict(name, top, sector)
        self.customer_id = {}
        self.agenda = []
        self._cust_seq = 100231

    # ----- entity helpers
    def new_entity(self, name, country="GB", category="GENERAL", reg=None, sector=None):
        rng = self.rng
        prefix = LOUS[country][:4] if country in LOUS else "5493"
        lei = make_lei(rng, prefix, self.used_lei)
        if reg is None:
            reg = dt.date(2013, 1, 1) + dt.timedelta(days=int(rng.integers(0, 3800)))
        self.ent[lei] = dict(lei=lei, name=name, country=country, category=category,
                             initial=reg, lapse_from=None, merged_on=None, successor=None,
                             lou=LOUS.get(country, LOUS["US"]), sector=sector)
        return lei

    def add_rel(self, child, parent, rtype, start, end=None, lapsed_from=None, reg=None):
        if reg is None:
            reg = max(start, self.ent[child]["initial"]) + dt.timedelta(days=int(self.rng.integers(5, 60)))
        self.rel.append(dict(child=child, parent=parent, type=rtype, start=start, end=end,
                             lapsed_from=lapsed_from, reg=reg))

    def consolidate(self, child, parent, top, start, end=None, lapsed_from=None, reg=None):
        self.add_rel(child, parent, "IS_DIRECTLY_CONSOLIDATED_BY", start, end, lapsed_from, reg)
        if top is not None:
            self.add_rel(child, top, "IS_ULTIMATELY_CONSOLIDATED_BY", start, end, lapsed_from, reg)

    def cust(self, lei):
        if lei not in self.customer_id:
            self._cust_seq += int(self.rng.integers(3, 40))
            self.customer_id[lei] = "C%07d" % self._cust_seq
        return self.customer_id[lei]


def company_name(rng, sector_word, kind="top"):
    p = rng.choice(PLACES)
    if kind == "top":
        return f"{p} {sector_word} Group plc" if rng.random() < 0.5 else f"{p} {sector_word} Holdings Ltd"
    return f"{p} {sector_word} {rng.choice(SUFFIX_SUB)}"


# ---------------------------------------------------------------- facilities

def D(y, m, d):
    return dt.date(y, m, d)


class Fac:
    __slots__ = ("ref", "lei", "ftype", "ccy", "limit", "drawn", "start", "maturity", "booking",
                 "migrated_from", "sector")

    def __init__(self, ref, lei, ftype, ccy, limit, drawn, start, maturity, booking=None,
                 migrated_from=None):
        self.ref, self.lei, self.ftype, self.ccy = ref, lei, ftype, ccy
        self.limit = list(limit)      # per QE, None = not on book
        self.drawn = list(drawn)
        self.start, self.maturity = start, maturity
        self.booking = booking or ["CWB-LDN"] * 5
        self.migrated_from = migrated_from


def build_world():
    w = World()
    rng = w.rng
    fac_seq = [41000387]

    def fref(prefix="LN"):
        fac_seq[0] += int(rng.integers(7, 300))
        return "%s%09d" % (prefix, fac_seq[0])

    def facility(lei, ftype, ccy, limit, drawn, start=None, maturity=None, booking=None,
                 migrated_from=None, prefix="LN"):
        if isinstance(limit, (int, float)):
            limit = [float(limit)] * 5
        start = start or D(2020, 1, 1) + dt.timedelta(days=int(rng.integers(0, 1800)))
        maturity = maturity or D(2027, 6, 30) + dt.timedelta(days=int(rng.integers(0, 1500)))
        f = Fac(fref(prefix), lei, ftype, ccy, limit, drawn, start, maturity, booking, migrated_from)
        w.fac.append(f)
        w.cust(lei)
        return f

    def noisy(vals, sd=0.004):
        return [None if v is None else round(v * 1e6 * (1 + rng.normal(0, sd)), 2) for v in vals]

    # ================= AGENDA GROUP X: Kelderby (main call) =================
    XP = w.new_entity("Kelderby Group plc", "GB", reg=D(2014, 3, 11), sector="81")
    X1 = w.new_entity("Kelderby Facilities Ltd", "GB", reg=D(2014, 5, 2), sector="81")
    X2 = w.new_entity("Kelderby Engineering Ltd", "GB", reg=D(2015, 1, 19), sector="28")
    Y = w.new_entity("Tarrant Hydraulics Ltd", "GB", reg=D(2016, 7, 4), sector="28")
    YP = w.new_entity("Tarrant Holdings Ltd", "GB", reg=D(2016, 7, 4), sector="28")
    Z = w.new_entity("Norbeck Coatings Ltd", "GB", reg=D(2017, 2, 14), sector="20")
    w.groups["X"] = dict(top=XP, name="Kelderby Group plc", sector="81")
    for c in (X1, X2):
        w.consolidate(c, XP, XP, D(2014, 6, 30), reg=D(2018, 5, 1))
    ACQ_Y = D(2026, 4, 14)
    SALE_Z = D(2026, 2, 20)
    # Tarrant: owned by Tarrant Holdings (founder-owned, NATURAL_PERSONS) until Kelderby buys the shares
    w.consolidate(Y, YP, YP, D(2016, 7, 4), end=ACQ_Y, reg=D(2018, 6, 1))
    w.consolidate(Y, XP, XP, ACQ_Y, reg=D(2026, 5, 6))
    w.repex.append((YP, "ULTIMATE_ACCOUNTING_CONSOLIDATION_PARENT", "NATURAL_PERSONS"))
    # Norbeck: Kelderby subsidiary until sold to Meridale on 20 Feb 2026
    w.consolidate(Z, XP, XP, D(2017, 2, 14), end=SALE_Z, reg=D(2018, 5, 1))
    xf = {}
    xf["XP_RCF"] = facility(XP, "RCF", "GBP", 40.0, noisy([6.2, 9.1, 7.4, 11.6, 13.9]), D(2021, 9, 1))
    xf["X1_TERM"] = facility(X1, "TERM", "GBP", [55.0, 53.6, 52.2, 50.8, 49.4],
                              [55.0e6, 53.6e6, 52.2e6, 50.8e6, 49.4e6], D(2022, 3, 31))
    xf["X2_RCF"] = facility(X2, "RCF", "GBP", 35.0, noisy([10.2, 15.0, 20.6, 25.8, 31.0]), D(2021, 11, 15))
    xf["Y_TERM"] = facility(Y, "TERM", "GBP", [28.0, 27.3, 26.6, 25.9, 25.2],
                             [28.0e6, 27.3e6, 26.6e6, 25.9e6, 25.2e6], D(2023, 6, 30))
    xf["Y_RCF"] = facility(Y, "RCF", "GBP", 15.0, noisy([6.4, 7.2, 5.1, 8.3, 9.0]), D(2023, 6, 30))
    xf["Z_TERM"] = facility(Z, "TERM", "GBP", [16.0, 15.6, 15.2, 14.8, 14.4],
                             [16.0e6, 15.6e6, 15.2e6, 14.8e6, 14.4e6], D(2022, 8, 31))
    w.X = dict(XP=XP, X1=X1, X2=X2, Y=Y, Z=Z, YP=YP, fac=xf)

    # ================= AGENDA GROUP W: Meridale (bought Norbeck) =================
    WP = w.new_entity("Meridale Holdings Ltd", "GB", reg=D(2015, 10, 8), sector="17")
    W1 = w.new_entity("Meridale Packaging Ltd", "GB", reg=D(2015, 10, 8), sector="17")
    W2 = w.new_entity("Meridale Nederland B.V.", "NL", reg=D(2018, 2, 26), sector="17")
    w.groups["W"] = dict(top=WP, name="Meridale Holdings Ltd", sector="17")
    w.consolidate(W1, WP, WP, D(2015, 10, 8), reg=D(2018, 4, 20))
    w.consolidate(W2, WP, WP, D(2018, 2, 26), reg=D(2018, 4, 20))
    w.consolidate(Z, WP, WP, SALE_Z, reg=D(2026, 3, 12))
    w.repex.append((WP, "ULTIMATE_ACCOUNTING_CONSOLIDATION_PARENT", "NATURAL_PERSONS"))
    wf = {}
    wf["WP_TERM"] = facility(WP, "TERM", "GBP", [24.0, 23.0, 22.0, 21.0, 20.0],
                              [24.0e6, 23.0e6, 22.0e6, 21.0e6, 20.0e6], D(2022, 12, 20))
    wf["W1_RCF"] = facility(W1, "RCF", "GBP", 20.0, noisy([7.9, 9.4, 8.8, 10.6, 11.3]), D(2022, 4, 4))
    # two equal tranches of one acquisition loan, booked as separate facilities on the same day
    twin = [6.0, 5.85, 5.7, 5.55, 5.4]
    wf["W1_TERM_A"] = facility(W1, "TERM", "GBP", twin, [x * 1e6 for x in twin], D(2023, 9, 29))
    wf["W1_TERM_B"] = facility(W1, "TERM", "GBP", twin, [x * 1e6 for x in twin], D(2023, 9, 29))
    # Dutch subsidiary's EUR revolver, moved from the London book to the Dublin book in June 2026:
    # the receiving facility carries migrated_from, the London one stays on the source ledger to July close
    lim_w2 = [18.0, 18.0, 18.0, 18.0, None]
    dr_w2 = [x * 1e6 for x in [9.6, 11.2, 10.4, 12.8]] + [None]
    wf["W2_RCF_LDN"] = facility(W2, "RCF", "EUR", lim_w2, dr_w2, D(2021, 5, 17))
    wf["W2_RCF_DUB"] = facility(W2, "RCF", "EUR", [None, None, None, 18.0, 18.0],
                                 [None, None, None, 12.8e6, 13.5e6], D(2026, 6, 22),
                                 booking=["CWB-DUB"] * 5, migrated_from=wf["W2_RCF_LDN"].ref)
    w.W = dict(WP=WP, W1=W1, W2=W2, fac=wf)

    # ================= AGENDA GROUP A: Brauneck (UK branch) =================
    AP = w.new_entity("Brauneck Holding SE", "DE", reg=D(2014, 9, 1), sector="28")
    A1 = w.new_entity("Brauneck Antriebstechnik AG", "DE", reg=D(2014, 9, 1), sector="28")
    AB = w.new_entity("Brauneck Antriebstechnik AG, London Branch", "GB", category="BRANCH",
                      reg=D(2019, 11, 6), sector="28")
    A2 = w.new_entity("Brauneck Drives UK Ltd", "GB", reg=D(2017, 3, 30), sector="28")
    w.groups["A"] = dict(top=AP, name="Brauneck Holding SE", sector="28")
    w.consolidate(A1, AP, AP, D(2014, 9, 1), reg=D(2017, 12, 1))
    w.consolidate(A2, A1, AP, D(2017, 3, 30), reg=D(2018, 2, 9))
    w.add_rel(AB, A1, "IS_INTERNATIONAL_BRANCH_OF", D(2019, 11, 6), reg=D(2019, 11, 6))
    w.repex.append((AP, "ULTIMATE_ACCOUNTING_CONSOLIDATION_PARENT", "NO_KNOWN_PERSON"))
    af = {}
    af["A1_TERM"] = facility(A1, "TERM", "EUR", [45.0, 45.0, 45.0, 45.0, 45.0], [45.0e6] * 5, D(2023, 1, 31),
                            booking=["CWB-DUB"] * 5)
    af["AB_RCF"] = facility(AB, "RCF", "GBP", 30.0, noisy([17.5, 19.2, 18.1, 21.4, 22.9]), D(2020, 2, 28))
    af["A2_OVD"] = facility(A2, "OVD", "GBP", 2.5, noisy([0.8, 1.3, 0.4, 1.1, 1.6], 0.02), D(2018, 1, 10),
                            prefix="OD")
    AH = w.new_entity("Hollins Gear Ltd", "GB", reg=D(2016, 3, 9), sector="28")
    AHP = w.new_entity("Hollins Family Holdings Ltd", "GB", reg=D(2016, 3, 9), sector="64")
    ACQ_AH = D(2026, 1, 8)
    w.consolidate(AH, AHP, AHP, D(2016, 3, 9), end=ACQ_AH, reg=D(2018, 3, 1))
    w.consolidate(AH, A2, AP, ACQ_AH, reg=D(2026, 2, 2))
    w.repex.append((AHP, "ULTIMATE_ACCOUNTING_CONSOLIDATION_PARENT", "NATURAL_PERSONS"))
    af["AH_TERM"] = facility(AH, "TERM", "GBP", [12.0, 11.7, 11.4, 11.1, 10.8],
                              [12.0e6, 11.7e6, 11.4e6, 11.1e6, 10.8e6], D(2022, 5, 31))
    af["AH_RCF"] = facility(AH, "RCF", "GBP", 6.0, noisy([2.9, 3.6, 3.1, 4.2, 3.8]), D(2022, 5, 31))
    w.A = dict(AP=AP, A1=A1, AB=AB, A2=A2, AH=AH, AHP=AHP, fac=af)

    # ================= AGENDA GROUP B: Corrin (merged predecessor still keyed) =================
    BP = w.new_entity("Corrin Logistics Group plc", "GB", reg=D(2013, 11, 20), sector="49")
    B1 = w.new_entity("Corrin Freight Ltd", "GB", reg=D(2013, 12, 2), sector="49")
    B2 = w.new_entity("Corrin Warehousing Ltd", "GB", reg=D(2015, 4, 16), sector="52")
    B3 = w.new_entity("Corrin Operations Ltd", "GB", reg=D(2019, 8, 1), sector="49")
    w.groups["B"] = dict(top=BP, name="Corrin Logistics Group plc", sector="49")
    MERGE_B = D(2026, 3, 1)
    w.consolidate(B1, BP, BP, D(2013, 12, 2), reg=D(2017, 11, 3))
    w.consolidate(B2, BP, BP, D(2015, 4, 16), end=MERGE_B, reg=D(2017, 11, 3))
    w.consolidate(B3, BP, BP, D(2019, 8, 1), reg=D(2019, 9, 2))
    w.ent[B2]["merged_on"] = MERGE_B
    w.ent[B2]["successor"] = B3
    w.repex.append((BP, "ULTIMATE_ACCOUNTING_CONSOLIDATION_PARENT", "NO_KNOWN_PERSON"))
    bf = {}
    bf["BP_TERM"] = facility(BP, "TERM", "GBP", [40.0, 38.5, 37.0, 35.5, 34.0],
                              [40.0e6, 38.5e6, 37.0e6, 35.5e6, 34.0e6], D(2022, 9, 30))
    bf["B1_RCF"] = facility(B1, "RCF", "GBP", 25.0, noisy([11.3, 12.9, 13.8, 12.2, 14.6]), D(2021, 7, 1))
    bf["B2_TERM"] = facility(B2, "TERM", "GBP", [21.0, 20.4, 19.8, 19.2, 18.6],
                              [21.0e6, 20.4e6, 19.8e6, 19.2e6, 18.6e6], D(2021, 3, 31))
    bf["B3_RCF"] = facility(B3, "RCF", "GBP", 12.0, noisy([3.2, 4.1, 5.7, 4.9, 6.3]), D(2022, 2, 1))
    B4 = w.new_entity("Corrin Cold Chain Ltd", "GB", reg=D(2018, 6, 12), sector="52")
    SALE_B4 = D(2026, 5, 29)
    w.consolidate(B4, BP, BP, D(2018, 6, 12), end=SALE_B4, reg=D(2018, 8, 1))
    bf["B4_TERM"] = facility(B4, "TERM", "GBP", [14.0, 13.5, 13.0, 12.5, 12.0],
                              [14.0e6, 13.5e6, 13.0e6, 12.5e6, 12.0e6], D(2021, 12, 17))
    w.B = dict(BP=BP, B1=B1, B2=B2, B3=B3, B4=B4, fac=bf)

    # ================= AGENDA GROUP C: Pellow (subsidiary reports only its direct parent) =================
    CP = w.new_entity("Pellow Foods Group plc", "GB", reg=D(2013, 6, 4), sector="10")
    CM = w.new_entity("Pellow Bakeries Holdings Ltd", "GB", reg=D(2014, 2, 27), sector="10")
    C1 = w.new_entity("Pellow Bakeries Ltd", "GB", reg=D(2014, 2, 27), sector="10")
    C2 = w.new_entity("Pellow Distribution Ltd", "GB", reg=D(2016, 10, 3), sector="49")
    w.groups["C"] = dict(top=CP, name="Pellow Foods Group plc", sector="10")
    w.consolidate(CM, CP, CP, D(2014, 2, 27), reg=D(2017, 11, 18))
    # the bakery reports its direct parent only; its ultimate parent is reached through the holding company
    w.add_rel(C1, CM, "IS_DIRECTLY_CONSOLIDATED_BY", D(2014, 2, 27), reg=D(2017, 11, 18))
    w.consolidate(C2, CP, CP, D(2016, 10, 3), reg=D(2017, 11, 18))
    w.repex.append((CP, "ULTIMATE_ACCOUNTING_CONSOLIDATION_PARENT", "NO_KNOWN_PERSON"))
    cf = {}
    cf["C1_RCF"] = facility(C1, "RCF", "GBP", 30.0, noisy([16.1, 18.3, 15.2, 19.7, 21.2]), D(2021, 10, 8))
    cf["C1_TERM"] = facility(C1, "TERM", "GBP", [18.0, 17.25, 16.5, 15.75, 15.0],
                              [18.0e6, 17.25e6, 16.5e6, 15.75e6, 15.0e6], D(2023, 3, 31))
    cf["C2_TERM"] = facility(C2, "TERM", "GBP", [12.0, 11.6, 11.2, 10.8, 10.4],
                              [12.0e6, 11.6e6, 11.2e6, 10.8e6, 10.4e6], D(2022, 6, 30))
    CF = w.new_entity("Fenwick Bakery Supplies Ltd", "GB", reg=D(2017, 9, 25), sector="46")
    CFP = w.new_entity("Fenwick Holdings Ltd", "GB", reg=D(2017, 9, 25), sector="64")
    ACQ_CF = D(2025, 11, 27)
    w.consolidate(CF, CFP, CFP, D(2017, 9, 25), end=ACQ_CF, reg=D(2018, 1, 15))
    w.consolidate(CF, CM, CP, ACQ_CF, reg=D(2025, 12, 19))
    w.repex.append((CFP, "ULTIMATE_ACCOUNTING_CONSOLIDATION_PARENT", "NATURAL_PERSONS"))
    cf["CF_RCF"] = facility(CF, "RCF", "GBP", 10.0, noisy([5.6, 6.3, 7.1, 6.8, 7.4]), D(2021, 1, 29))
    cf["CF_TERM"] = facility(CF, "TERM", "GBP", [7.0, 6.65, 6.3, 5.95, 5.6],
                              [7.0e6, 6.65e6, 6.3e6, 5.95e6, 5.6e6], D(2022, 10, 31))
    w.C = dict(CP=CP, CM=CM, C1=C1, C2=C2, CF=CF, CFP=CFP, fac=cf)

    # ================= AGENDA GROUP D: Stannard (asset manager with managed funds) =================
    DP = w.new_entity("Stannard Capital Group plc", "GB", reg=D(2014, 1, 15), sector="66")
    D1 = w.new_entity("Stannard Capital Partners LLP", "GB", reg=D(2014, 1, 15), sector="66")
    D2 = w.new_entity("Stannard Capital Management Ltd", "GB", reg=D(2016, 5, 12), sector="66")
    w.groups["D"] = dict(top=DP, name="Stannard Capital Group plc", sector="66")
    w.consolidate(D1, DP, DP, D(2014, 1, 15), reg=D(2017, 12, 14))
    w.consolidate(D2, DP, DP, D(2016, 5, 12), reg=D(2017, 12, 14))
    w.repex.append((DP, "ULTIMATE_ACCOUNTING_CONSOLIDATION_PARENT", "NO_KNOWN_PERSON"))
    funds = []
    for nm, reg in [("Stannard Infrastructure Fund III LP", D(2019, 3, 8)),
                    ("Stannard Credit Opportunities Fund II LP", D(2021, 6, 22)),
                    ("Stannard Real Estate Partners IV SCSp", D(2022, 9, 5))]:
        cc = "LU" if nm.endswith("SCSp") else "GB"
        f = w.new_entity(nm, cc, category="FUND", reg=reg, sector="64")
        w.add_rel(f, D1, "IS_FUND-MANAGED_BY", reg, reg=reg + dt.timedelta(days=14))
        w.repex.append((f, "DIRECT_ACCOUNTING_CONSOLIDATION_PARENT", "NON_CONSOLIDATING"))
        w.repex.append((f, "ULTIMATE_ACCOUNTING_CONSOLIDATION_PARENT", "NON_CONSOLIDATING"))
        funds.append(f)
    df = {}
    df["DP_TERM"] = facility(DP, "TERM", "GBP", [15.0, 14.5, 14.0, 13.5, 13.0],
                              [15.0e6, 14.5e6, 14.0e6, 13.5e6, 13.0e6], D(2023, 2, 28))
    df["D2_RCF"] = facility(D2, "RCF", "GBP", 10.0, noisy([2.4, 3.1, 2.2, 3.8, 4.4]), D(2022, 7, 15))
    df["F1_SUB"] = facility(funds[0], "RCF", "GBP", 35.0, noisy([14.2, 9.8, 18.6, 12.1, 16.4]), D(2020, 1, 20))
    df["F2_SUB"] = facility(funds[1], "RCF", "GBP", 25.0, noisy([8.3, 11.6, 6.9, 13.2, 10.1]), D(2021, 8, 2))
    df["F3_SUB"] = facility(funds[2], "RCF", "EUR", 20.0, noisy([4.1, 7.7, 9.3, 5.6, 8.2]), D(2022, 11, 7))
    w.D = dict(DP=DP, D1=D1, D2=D2, funds=funds, fac=df)

    w.agenda_groups = ["X", "W", "A", "B", "C", "D"]
    build_background(w, fref, facility)
    w.ent[CM]["lapse_from"] = D(2025, 7, 14)
    # the buyer of Corrin Cold Chain: an existing GB group of the bank
    buyer = [g for g in w.bg_groups if g["cc"] == "GB" and len(g["members"]) >= 3 and
             w.ent[g["top"]]["lapse_from"] is None][5]
    w.consolidate(B4, buyer["top"], buyer["top"], SALE_B4, reg=D(2026, 6, 24))
    w.B["buyer"] = buyer["key"]
    return w


def build_background(w, fref, facility):
    rng = w.rng
    countries = ["GB"] * 16 + ["DE", "NL", "IE", "FR", "LU", "US"]
    used_names = set(e["name"] for e in w.ent.values())

    def uname(maker):
        for _ in range(50):
            n = maker()
            if n not in used_names:
                used_names.add(n)
                return n
        n = maker() + " (No.2)"
        used_names.add(n)
        return n

    def sector():
        return SECTORS[int(rng.integers(0, len(SECTORS)))]

    def rand_drawn(limit, kind):
        if kind == "TERM":
            amort = rng.uniform(0.0, 0.03)
            return [limit * (1 - amort * i) * 1e6 for i in range(5)], [limit * (1 - amort * i) for i in range(5)]
        u = rng.uniform(0.05, 0.85)
        path = []
        for i in range(5):
            u = min(0.98, max(0.0, u + rng.normal(0, 0.08)))
            path.append(round(limit * u * 1e6, 2))
        return path, [limit] * 5

    def add_facilities(lei, scale, ccy="GBP"):
        n = int(rng.integers(1, 4))
        kinds = rng.choice(["TERM", "RCF", "OVD"], n, p=[0.45, 0.4, 0.15])
        for k in kinds:
            lim = float(np.round(np.exp(rng.normal(np.log(scale), 0.8)), 1))
            lim = max(0.3, min(lim, 90.0))
            if k == "OVD":
                lim = max(0.2, min(lim / 6, 5.0))
            drawn, limits = rand_drawn(lim, k)
            c = ccy if rng.random() < 0.85 else rng.choice(["GBP", "EUR", "USD"])
            bk = ["CWB-DUB"] * 5 if (c == "EUR" and rng.random() < 0.45) else None
            facility(lei, k, c, limits, drawn, booking=bk, prefix="OD" if k == "OVD" else "LN")

    groups = []
    # corporate groups
    for gi in range(560):
        sw, sic = sector()
        cc = countries[int(rng.integers(0, len(countries)))]
        if cc == "DE":
            top_name = uname(lambda: f"{rng.choice(PLACES)} {rng.choice(DE_WORDS)} Holding GmbH")
        elif cc in ("NL",):
            top_name = uname(lambda: f"{rng.choice(PLACES)} {sw} Holding B.V.")
        elif cc == "FR":
            top_name = uname(lambda: f"{rng.choice(PLACES)} {sw} SAS")
        elif cc == "US":
            top_name = uname(lambda: f"{rng.choice(PLACES)} {sw} Inc.")
        elif cc == "LU":
            top_name = uname(lambda: f"{rng.choice(PLACES)} {sw} S.a r.l.")
        elif cc == "IE":
            top_name = uname(lambda: f"{rng.choice(PLACES)} {sw} Holdings DAC")
        else:
            top_name = uname(lambda: company_name(rng, sw, "top"))
        top = w.new_entity(top_name, cc, sector=sic)
        key = "G%04d" % gi
        w.groups[key] = dict(top=top, name=top_name, sector=sic)
        r = rng.random()
        if r < 0.55:
            w.repex.append((top, "ULTIMATE_ACCOUNTING_CONSOLIDATION_PARENT",
                            rng.choice(["NO_KNOWN_PERSON", "NATURAL_PERSONS", "NON_PUBLIC"], p=[0.6, 0.3, 0.1])))
        nsub = int(rng.choice([0, 1, 1, 2, 2, 3, 4, 5, 7]))
        members = [top]
        mid = None
        if nsub >= 3 and rng.random() < 0.35:
            mid = w.new_entity(uname(lambda: f"{rng.choice(PLACES)} {sw} Midco Ltd"), "GB", sector=sic)
            w.consolidate(mid, top, top, w.ent[mid]["initial"])
            members.append(mid)
        for s in range(nsub):
            sub_cc = cc if rng.random() < 0.7 else "GB"
            sn = uname(lambda: company_name(rng, sw, "sub"))
            sub = w.new_entity(sn, sub_cc, sector=sic)
            parent = mid if (mid is not None and rng.random() < 0.6) else top
            st = max(w.ent[sub]["initial"], w.ent[parent]["initial"])
            w.consolidate(sub, parent, top, st)
            members.append(sub)
        groups.append(dict(key=key, top=top, members=members, sic=sic, cc=cc))
        borrowers = [m for m in members if rng.random() < 0.6] or [members[-1]]
        scale = float(np.exp(rng.normal(np.log(6.0), 0.9)))
        for b in borrowers:
            add_facilities(b, scale, "EUR" if w.ent[b]["country"] in ("DE", "NL", "IE", "FR", "LU") else
                           ("USD" if w.ent[b]["country"] == "US" else "GBP"))

    # fund managers and their funds (subscription lines)
    for mi in range(22):
        sw, sic = ("Capital", "66")
        mgr_top = w.new_entity(uname(lambda: f"{rng.choice(PLACES)} Capital Group Ltd"), "GB", sector="66")
        mgr = w.new_entity(uname(lambda: f"{rng.choice(PLACES)} Capital Partners LLP"), "GB", sector="66")
        w.consolidate(mgr, mgr_top, mgr_top, w.ent[mgr]["initial"])
        w.repex.append((mgr_top, "ULTIMATE_ACCOUNTING_CONSOLIDATION_PARENT", "NATURAL_PERSONS"))
        key = "M%03d" % mi
        w.groups[key] = dict(top=mgr_top, name=w.ent[mgr_top]["name"], sector="66")
        if rng.random() < 0.6:
            add_facilities(mgr_top, 4.0)
        base = w.ent[mgr]["name"].split(" Capital")[0]
        for fi in range(int(rng.integers(2, 7))):
            roman = ["I", "II", "III", "IV", "V", "VI", "VII"][fi]
            strat = rng.choice(["Growth", "Infrastructure", "Credit", "Real Estate", "Buyout", "Secondaries"])
            cc = "LU" if rng.random() < 0.3 else "GB"
            nm = f"{base} {strat} Fund {roman} " + ("SCSp" if cc == "LU" else "LP")
            f = w.new_entity(uname(lambda: nm), cc, category="FUND", sector="64")
            w.add_rel(f, mgr, "IS_FUND-MANAGED_BY", w.ent[f]["initial"])
            w.repex.append((f, "ULTIMATE_ACCOUNTING_CONSOLIDATION_PARENT", "NON_CONSOLIDATING"))
            w.groups["%s_F%d" % (key, fi)] = dict(top=f, name=w.ent[f]["name"], sector="64")
            if rng.random() < 0.7:
                lim = float(np.round(rng.uniform(8, 45), 1))
                drawn, limits = rand_drawn(lim, "RCF")
                facility(f, "RCF", "GBP" if cc == "GB" else "EUR", limits, drawn)

    # international branches of foreign groups borrowing in London
    foreign = [g for g in groups if g["cc"] in ("DE", "NL", "FR", "US", "IE", "LU")]
    for g in rng.choice(foreign, size=min(24, len(foreign)), replace=False):
        head = g["members"][0] if len(g["members"]) == 1 else g["members"][int(rng.integers(0, len(g["members"])))]
        br = w.new_entity(w.ent[head]["name"] + ", London Branch", "GB", category="BRANCH", sector=g["sic"])
        w.add_rel(br, head, "IS_INTERNATIONAL_BRANCH_OF", w.ent[br]["initial"])
        add_facilities(br, 5.0)

    # registration lapses (entity) at realistic rates, intermediate holdcos included
    allleis = [l for l in w.ent if w.ent[l]["category"] != "BRANCH"]
    for l in rng.choice(allleis, size=int(len(allleis) * 0.11), replace=False):
        if l in (w.X["XP"], w.X["X1"], w.X["X2"], w.X["Y"], w.X["Z"]):
            continue
        w.ent[l]["lapse_from"] = D(2024, 1, 1) + dt.timedelta(days=int(rng.integers(0, 990)))
    # relationship record lapses
    for r in w.rel:
        if r["lapsed_from"] is None and rng.random() < 0.05 and r["child"] not in w.X.values():
            r["lapsed_from"] = D(2024, 6, 1) + dt.timedelta(days=int(rng.integers(0, 800)))

    # ownership changes during the window: share acquisitions and disposals between groups
    movers = []
    cands = [g for g in groups if len(g["members"]) >= 2 and g["cc"] == "GB"]
    for i in range(26):
        src = cands[int(rng.integers(0, len(cands)))]
        dst = cands[int(rng.integers(0, len(cands)))]
        if src is dst:
            continue
        subs = [m for m in src["members"][1:] if not any(m == x["lei"] for x in movers)]
        if not subs:
            continue
        sub = subs[int(rng.integers(0, len(subs)))]
        when = D(2025, 10, 15) + dt.timedelta(days=int(rng.integers(0, 330)))
        # end the old links
        for r in w.rel:
            if r["child"] == sub and r["end"] is None and r["type"].startswith("IS_") and "CONSOLIDATED" in r["type"]:
                r["end"] = when
        w.consolidate(sub, dst["top"], dst["top"], when, reg=when + dt.timedelta(days=int(rng.integers(10, 45))))
        src["members"].remove(sub)
        dst["members"].append(sub)
        movers.append(dict(lei=sub, src=src["key"], dst=dst["key"], when=when))
    w.movers = movers

    # legal mergers inside groups: predecessor retired, successor named; some still keyed in the loan book
    mg = [g for g in groups if len(g["members"]) >= 3]
    w.merged_keyed = []
    for g in rng.choice(mg, size=min(18, len(mg)), replace=False):
        subs = [m for m in g["members"][1:] if w.ent[m]["merged_on"] is None and w.ent[m]["category"] == "GENERAL"]
        if len(subs) < 2:
            continue
        pred, succ = subs[0], subs[1]
        when = D(2025, 11, 1) + dt.timedelta(days=int(rng.integers(0, 300)))
        w.ent[pred]["merged_on"] = when
        w.ent[pred]["successor"] = succ
        for r in w.rel:
            if r["child"] == pred and r["end"] is None:
                r["end"] = when
        w.merged_keyed.append(pred)

    # non-customer reference universe (issuers not held, prospects, relatives)
    for i in range(3600):
        sw, sic = sector()
        cc = countries[int(rng.integers(0, len(countries)))]
        nm = uname(lambda: company_name(rng, sw, "sub" if rng.random() < 0.6 else "top"))
        e = w.new_entity(nm, cc, sector=sic)
        if rng.random() < 0.12:
            w.ent[e]["lapse_from"] = D(2023, 6, 1) + dt.timedelta(days=int(rng.integers(0, 1100)))
    # a few entities registered inside the window
    for i in range(140):
        sw, sic = sector()
        nm = uname(lambda: company_name(rng, sw, "sub"))
        w.new_entity(nm, "GB", reg=D(2025, 10, 1) + dt.timedelta(days=int(rng.integers(0, 360))), sector=sic)

    w.bg_groups = groups
    # agenda groups carry only the lapses designed for them
    agenda_leis = set()
    for k in ("X", "W", "A", "B", "C", "D"):
        for v in getattr(w, k).values():
            if isinstance(v, str) and v in w.ent:
                agenda_leis.add(v)
            if isinstance(v, list):
                agenda_leis.update(x for x in v if isinstance(x, str) and x in w.ent)
    for l in agenda_leis:
        w.ent[l]["lapse_from"] = None
    for r in w.rel:
        if r["child"] in agenda_leis and not (r["child"] == w.C["C1"]):
            r["lapsed_from"] = None
    w.agenda_leis = agenda_leis


# ---------------------------------------------------------------- securities and derivatives

def add_markets(w):
    rng = w.rng
    # securities: bonds of larger groups' tops or finance subsidiaries, carrying value per QE
    w.sec = []
    issuers = []
    for g in w.bg_groups:
        if len(g["members"]) >= 3 and rng.random() < 0.28:
            issuers.append(g["members"][0] if rng.random() < 0.7 else g["members"][1])
    def issue(lei, ccy, nominal_m, cvs, coupon, maturity, blank_from=None):
        isin = make_isin(rng, "GB" if ccy == "GBP" else "XS", w.used_isin)
        w.sec.append(dict(isin=isin, lei=lei, ccy=ccy, nominal=nominal_m, cv=cvs, coupon=coupon,
                          maturity=maturity, blank_from=blank_from))
        return isin
    for lei in issuers:
        for k in range(int(rng.integers(1, 4))):
            ccy = "GBP" if rng.random() < 0.75 else rng.choice(["EUR", "USD"])
            nom = float(rng.choice([2, 2.5, 3, 4, 5, 7.5, 10]))
            px = rng.uniform(0.93, 1.03)
            held = [True] * 5
            if rng.random() < 0.15:
                cut = int(rng.integers(1, 5))
                held = [i >= cut for i in range(5)] if rng.random() < 0.5 else [i < cut for i in range(5)]
            cvs = [round(nom * 1e6 * (px + rng.normal(0, 0.006)), 2) if h else None for h in held]
            blank = 0 if rng.random() < 0.06 else None
            issue(lei, ccy, nom, cvs, round(float(rng.uniform(1.5, 7.5)), 3),
                  D(2027, 1, 1) + dt.timedelta(days=int(rng.integers(0, 3000))), blank)
    # Pellow Foods Group plc bonds (agenda group C); the 2031s come through the custodian feed without
    # an issuer LEI
    c = w.C
    w.C["isin_a"] = issue(c["CP"], "GBP", 6.0, [5.83e6, 5.79e6, 5.91e6, 5.88e6, 5.94e6], 4.375, D(2029, 3, 15))
    w.C["isin_b"] = issue(c["CP"], "GBP", 4.0, [3.71e6, 3.76e6, 3.69e6, 3.80e6, 3.84e6], 5.125, D(2031, 9, 30),
                          blank_from=0)
    # derivatives: netting sets per counterparty, MTM in GBP thousands, CSA cash collateral in units
    w.drv = []
    cps = []
    for g in w.bg_groups:
        if rng.random() < 0.18:
            cps.append(g["members"][int(rng.integers(0, len(g["members"])))])
    nsq = [5121]
    def nset(lei, mtm_k, csa=None, coll=None, ccy="GBP"):
        nsq[0] += int(rng.integers(3, 60))
        ns = "NS-%06d" % nsq[0]
        csa_ref = None
        if csa:
            csa_ref = "CSA/%s/%04d" % ("GB" if ccy == "GBP" else ccy[:2], int(rng.integers(1000, 9999)))
        w.drv.append(dict(ns=ns, lei=lei, mtm_k=mtm_k, csa=csa_ref, coll=coll, coll_ccy=ccy,
                          trades=int(rng.integers(1, 40))))
    for lei in cps:
        base = rng.normal(0, 1800)
        mtm = [round(base + rng.normal(0, 600), 1) for _ in range(5)]
        if rng.random() < 0.6:
            coll = [max(0.0, round(m * 1000 * rng.uniform(0.4, 0.95), -4)) if m > 0 else 0.0 for m in mtm]
            nset(lei, mtm, True, coll)
        else:
            nset(lei, mtm)
    b = w.B
    nset(b["BP"], [2850.4, 3412.9, 1964.2, 2718.6, 3186.3], True,
         [1500000.0, 2000000.0, 1000000.0, 1500000.0, 2000000.0])
    nset(b["B1"], [-412.6, 118.3, -95.2, 240.7, 312.5])
    d = w.D
    nset(d["D2"], [410.2, -221.6, 383.9, 642.1, 1312.4])
    # the 30 September 2026 close was rerun on 6 October after late trade bookings: the first run is kept
    # in the workbook beside the rerun
    for n in w.drv:
        n["mtm_run1"] = n["mtm_k"][4]
    w.drv[-1]["mtm_run1"] = 518.7
    late = [n for n in w.drv[:-3]]
    for n in [late[i] for i in rng.choice(len(late), size=7, replace=False)]:
        n["mtm_run1"] = round(n["mtm_k"][4] - float(rng.normal(0, 700)), 1)
    return w


def full_world():
    w = build_world()
    add_markets(w)
    return w
