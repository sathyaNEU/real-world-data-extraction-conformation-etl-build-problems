"""task485's world, the clean truth before any export is written: a state employees' self-funded health plan, its
four participating employer accounts, its pharmacy benefit manager, the brand drugs its members fill and the rebates
the manufacturers pay on them. Everything is drawn from fixed seeds, so two runs give the same world."""
import datetime as dt
import math

import numpy as np

SEED = 4850
FY_START, FY_END = dt.date(2025, 7, 1), dt.date(2026, 6, 30)
EXTRACT_DATE = dt.date(2026, 10, 9)          # the PBM's paid-claims extract, paid through 30 September 2026
PAID_THROUGH = dt.date(2026, 9, 30)
RENUMBER = dt.date(2026, 1, 1)               # the PBM's account restructure: new group codes and cardholder ids
NETWORK_MOVE = dt.date(2026, 3, 1)           # three hospital outpatient pharmacies join the specialty network

# fiscal quarters of FY2026 and the calendar quarter each is invoiced as
FQ = [("FQ1", dt.date(2025, 7, 1), dt.date(2025, 9, 30), "2025Q3"),
      ("FQ2", dt.date(2025, 10, 1), dt.date(2025, 12, 31), "2025Q4"),
      ("FQ3", dt.date(2026, 1, 1), dt.date(2026, 3, 31), "2026Q1"),
      ("FQ4", dt.date(2026, 4, 1), dt.date(2026, 6, 30), "2026Q2")]
# the PBM invoices a quarter's claims adjudicated by the 45th day after its end; later claims and reversals are
# remitted as prior-period adjustments on the next statement (Exhibit C, C.2)
CUTOFF = {"2025Q2": dt.date(2025, 8, 14), "2025Q3": dt.date(2025, 11, 14), "2025Q4": dt.date(2026, 2, 14),
          "2026Q1": dt.date(2026, 5, 15), "2026Q2": dt.date(2026, 8, 14)}
REMITTED = {"2025Q2": dt.date(2025, 9, 19), "2025Q3": dt.date(2025, 12, 19), "2025Q4": dt.date(2026, 3, 20),
            "2026Q1": dt.date(2026, 6, 19), "2026Q2": dt.date(2026, 9, 18)}
CAL_Q = ["2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2"]

# participating employer accounts: old group code, new group code, name, members, age profile
ACCOUNTS = [("STA", "100", "SEB01", "State Agencies", 14820, 44.0),
            ("HED", "200", "SEB02", "Higher Education", 9140, 38.5),
            ("LOC", "300", "SEB03", "Local Government", 6390, 46.5),
            ("RET", "400", "SEB04", "Non-Medicare Retirees", 3610, 60.5)]
ACC = [a[0] for a in ACCOUNTS]

PBM = "Halcroft Pharmacy Solutions"
PLAN = "Employees' Group Health Plan"
OFFICE = "Office of Employee Benefits"

# manufacturers: key, name on the product file (labeler), name on the remittance statements, labeler code
MFR = [("M1", "Arvelle Pharmaceuticals, Inc.", "ARVELLE PHARMACEUTICALS INC", "71584"),
       ("M2", "Brennick Therapeutics LLC", "BRENNICK THERAPEUTICS", "63097"),
       ("M3", "Castellan Pharma USA, Inc.", "CASTELLAN PHARMA USA", "58126"),
       ("M4", "Quorvia Inc.", "QUORVIA INC", "70451"),
       ("M5", "Teravian Pharmaceuticals, Inc.", "TERAVIAN PHARMACEUTICALS", "66273"),
       ("M6", "Ombrel Laboratories, Inc.", "OMBREL LABORATORIES", "51938"),
       ("M7", "Pellard Pharma US LLC", "PELLARD PHARMA US", "69620"),
       ("M8", "Vantrel Biosciences, Inc.", "VANTREL BIOSCIENCES", "73019"),
       ("M9", "Kelvarin Biologics LLC", "KELVARIN BIOLOGICS", "55870"),
       ("M10", "Dorvane Pharma Inc.", "DORVANE PHARMA", "68342"),
       ("M11", "Elsmere Therapeutics, Inc.", "ELSMERE THERAPEUTICS", "62714"),
       ("M12", "Fenwick Laboratories LLC", "FENWICK LABORATORIES", "57409")]

CLASSES = [("GLP1", "GLP-1 receptor agonists"), ("SGLT2", "SGLT2 inhibitors"), ("BASAL", "Long-acting insulins"),
           ("DOAC", "Direct oral anticoagulants"), ("ICS", "Inhaled corticosteroid and LABA combinations"),
           ("ADA", "Adalimumab products")]
REVIEWED = [c for c, _ in CLASSES]

# products: key, mfr, class, proprietary name, nonproprietary name and strength, package, units per package,
# package size unit, units per 30-day supply (Appendix B), WAC per package (USD), rebate share of WAC, channel profile
# channel profile: R (retail), M (mail heavy), S (specialty only)
PRODUCTS = [
    ("GLP_A", "M1", "GLP1", "Velantro", "semaglutide 1 mg/0.75 mL pen", "1 pen", 1, "EA", 1.0, 1008.40, 0.48, "R"),
    ("GLP_B", "M2", "GLP1", "Dulmira", "dulaglutide 1.5 mg/0.5 mL pen", "4 pens", 4, "EA", 4.0, 964.10, 0.34, "R"),
    ("GLP_C", "M3", "GLP1", "Liraquent", "liraglutide 18 mg/3 mL pen", "3 pens", 9, "ML", 9.0, 1041.70, 0.41, "R"),
    ("SGL_A", "M2", "SGLT2", "Empriva", "empagliflozin 25 mg tablet", "30 tablets", 30, "EA", 30.0, 609.30, 0.56, "R"),
    ("SGL_B", "M4", "SGLT2", "Daplexa", "dapagliflozin 10 mg tablet", "30 tablets", 30, "EA", 30.0, 595.80, 0.40, "R"),
    ("SGL_C", "M5", "SGLT2", "Canivo", "canagliflozin 300 mg tablet", "30 tablets", 30, "EA", 30.0, 568.90, 0.33, "R"),
    ("INS_A", "M1", "BASAL", "Glarvia", "insulin glargine 100 units/mL pen", "5 pens", 15, "ML", 15.0, 390.20, 0.72, "R"),
    ("INS_B", "M3", "BASAL", "Deglutra", "insulin degludec 100 units/mL pen", "5 pens", 15, "ML", 15.0, 359.40, 0.47, "R"),
    ("INS_C", "M6", "BASAL", "insulin glargine-qmrt", "insulin glargine-qmrt 100 units/mL pen", "5 pens", 15, "ML",
     15.0, 267.10, 0.20, "R"),
    ("DOA_A", "M5", "DOAC", "Apiqor", "apixaban 5 mg tablet", "60 tablets", 60, "EA", 60.0, 585.60, 0.35, "R"),
    ("DOA_B", "M7", "DOAC", "Ravelta", "rivaroxaban 20 mg tablet", "30 tablets", 30, "EA", 30.0, 568.30, 0.20, "R"),
    ("ICS_A", "M4", "ICS", "Brezara", "budesonide 160 mcg/formoterol 4.5 mcg inhaler", "1 inhaler, 120 actuations",
     10.2, "GM", 10.2, 426.10, 0.52, "R"),
    ("ICS_B", "M6", "ICS", "Vilaro", "fluticasone furoate 100 mcg/vilanterol 25 mcg inhaler", "1 inhaler, 30 doses",
     1, "EA", 1.0, 389.30, 0.35, "R"),
    ("ICS_C", "M8", "ICS", "Saltiva", "fluticasone propionate 250 mcg/salmeterol 50 mcg inhaler", "1 inhaler, 60 doses",
     1, "EA", 1.0, 338.70, 0.20, "R"),
    ("ADA_A", "M8", "ADA", "Adalvane", "adalimumab 40 mg/0.4 mL pen", "2 pens", 2, "EA", 2.0, 6852.00, 0.43, "S"),
    ("ADA_B", "M3", "ADA", "Advelis", "adalimumab-cstl 40 mg/0.4 mL pen", "2 pens", 2, "EA", 2.0, 5684.00, 0.38, "S"),
    ("ADA_C", "M9", "ADA", "adalimumab-kvrn", "adalimumab-kvrn 40 mg/0.4 mL pen", "2 pens", 2, "EA", 2.0, 1205.00,
     0.02, "S"),
    # products outside the reviewed classes, paid for under the same manufacturer agreements
    ("ONC_1", "M1", "ONC", "Trivoleta", "talzenacor 150 mg capsule", "30 capsules", 30, "EA", 30.0, 15390.00, 0.02, "S"),
    ("MS_1", "M2", "MS", "Ambrelis", "ozanimod-like 0.92 mg capsule", "30 capsules", 30, "EA", 30.0, 8340.00, 0.07, "S"),
    ("HIV_1", "M4", "HIV", "Virelda", "bictegravir/emtricitabine/tenofovir AF tablet", "30 tablets", 30, "EA", 30.0,
     3910.00, 0.05, "R"),
    ("HCV_1", "M5", "HCV", "Hepravo", "sofosbuvir/velpatasvir tablet", "28 tablets", 28, "EA", 28.0, 11280.00, 0.14,
     "S"),
    ("MIG_1", "M6", "MIG", "Migrelta", "galcanezumab 120 mg/mL pen", "1 pen", 1, "EA", 1.0, 781.20, 0.44, "R"),
    ("ONC_2", "M7", "ONC", "Ostralix", "palbociclib 125 mg tablet", "21 tablets", 21, "EA", 21.0, 16680.00, 0.01, "S"),
    ("PSO_1", "M9", "PSO", "Risenta", "risankizumab 150 mg/mL pen", "1 pen", 1, "EA", 1.0, 7390.00, 0.18, "S"),
    ("AST_1", "M3", "AST", "Benrova", "benralizumab 30 mg/mL pen", "1 pen", 1, "EA", 1.0, 3640.00, 0.12, "S"),
]
# the tail of other brands in the extract, from manufacturers with no product in a reviewed class
OTHER = [
    ("OTH_01", "M10", "Lunzari", "lisdexamfetamine 40 mg capsule", 30, 389.00, 0.18),
    ("OTH_02", "M10", "Ecliva", "ethinyl estradiol/drospirenone tablet", 28, 162.00, 0.25),
    ("OTH_03", "M10", "Ophtavel", "netarsudil 0.02% ophthalmic solution", 2.5, 318.00, 0.30),
    ("OTH_04", "M11", "Epirex", "epinephrine 0.3 mg auto-injector", 2, 612.00, 0.15),
    ("OTH_05", "M11", "Torvanza", "ezetimibe/rosuvastatin tablet", 30, 142.00, 0.32),
    ("OTH_06", "M11", "Dermalyn", "crisaborole 2% ointment", 60, 742.00, 0.22),
    ("OTH_07", "M12", "Nexoril", "esomeprazole 40 mg capsule", 30, 286.00, 0.12),
    ("OTH_08", "M12", "Sumivex", "rimegepant 75 mg ODT", 8, 1012.00, 0.26),
    ("OTH_09", "M12", "Thyrelle", "levothyroxine 100 mcg capsule", 30, 88.00, 0.05),
    ("OTH_10", "M10", "Glauvex", "latanoprostene bunod 0.024% solution", 5, 296.00, 0.28),
    ("OTH_11", "M11", "Asmerin", "montelukast 10 mg granules", 30, 191.00, 0.10),
    ("OTH_12", "M12", "Zolvera", "zolmitriptan 5 mg nasal spray", 6, 418.00, 0.08),
]

# 30-day supplies per 1,000 members a month, by class and account (STA, HED, LOC, RET)
CLASS_RATE = {"GLP1": (18.0, 11.0, 16.0, 21.0), "SGLT2": (13.0, 8.0, 12.0, 24.0), "BASAL": (7.0, 4.0, 7.0, 16.0),
              "DOAC": (6.0, 3.0, 6.0, 22.0), "ICS": (11.0, 10.0, 10.0, 13.0), "ADA": (0.9, 0.7, 0.8, 1.0),
              "ONC": None}
SHARE = {"GLP_A": (.40, .46, .38, .33), "GLP_B": (.36, .30, .37, .40), "GLP_C": (.24, .24, .25, .27),
         "SGL_A": (.44, .40, .46, .48), "SGL_B": (.35, .38, .33, .30), "SGL_C": (.21, .22, .21, .22),
         "INS_A": (.46, .41, .47, .52), "INS_B": (.31, .36, .30, .27), "INS_C": (.23, .23, .23, .21),
         "DOA_A": (.62, .58, .63, .66), "DOA_B": (.38, .42, .37, .34),
         "ICS_A": (.40, .44, .41, .36), "ICS_B": (.33, .30, .34, .37), "ICS_C": (.27, .26, .25, .27),
         "ADA_A": (.52, .47, .55, .58), "ADA_B": (.30, .33, .28, .26), "ADA_C": (.18, .20, .17, .16)}
# share drift through the year, by fiscal quarter (new starts on Velantro, the biosimilar switch in adalimumab, ...)
DRIFT = {"GLP_A": (-.06, -.02, .03, .06), "GLP_B": (.04, .01, -.02, -.04), "ADA_A": (.10, .03, -.05, -.10),
         "ADA_C": (-.10, -.03, .06, .11), "ICS_A": (-.02, .04, .03, -.05), "INS_C": (-.05, -.01, .02, .05),
         "SGL_C": (.03, .0, -.01, -.03), "DOA_B": (.04, .01, -.02, -.03), "INS_B": (.02, .03, -.02, -.03),
         "GLP_C": (.02, .0, -.01, -.02), "SGL_B": (-.03, .0, .02, .03)}
SEASON = {"ICS": (0.84, 1.06, 1.16, 0.94)}
# products outside the reviewed classes: 30-day supplies per 1,000 members a month by account, and a quarterly trend
OUT_RATE = {"ONC_1": (0.62, 0.30, 0.55, 1.05), "MS_1": (0.30, 0.27, 0.29, 0.18), "HIV_1": (0.88, 0.78, 0.80, 0.52),
            "HCV_1": (0.62, 0.45, 0.58, 0.90), "MIG_1": (5.4, 6.3, 5.0, 3.1), "ONC_2": (0.18, 0.10, 0.17, 0.30),
            "PSO_1": (0.13, 0.11, 0.12, 0.09), "AST_1": (1.05, 0.98, 0.94, 1.12)}
OUT_TREND = {"ONC_1": (0.86, 0.97, 1.06, 1.14), "MIG_1": (0.90, 0.97, 1.04, 1.09), "HCV_1": (1.25, 1.05, 0.90, 0.80),
             "PSO_1": (0.92, 0.98, 1.03, 1.07), "AST_1": (1.08, 1.02, 0.97, 0.93)}
OTHER_RATE = (52.0, 47.0, 50.0, 41.0)     # 30-day supplies per 1,000 members a month, the whole tail

# brand ingredient cost terms (AWP = WAC x 1.2): AWP less 18% retail, 21% mail, 16% specialty
AWP_FACTOR = 1.2
DISCOUNT = {"RETAIL": 0.18, "MAIL": 0.21, "SPECIALTY": 0.16}
FEE = {"RETAIL30": 1.25, "RETAIL90": 0.75, "MAIL": 0.0, "SPECIALTY": 0.0}
GUARANTEE = {"RETAIL30": 236.0, "RETAIL90": 642.0, "MAIL": 668.0, "SPECIALTY": 1170.0}   # Exhibit C, per brand claim


def luhn_npi(base9):
    """A 10-digit NPI: nine digits and the check digit over the 80840 prefix (the NPPES rule)."""
    digits = [int(c) for c in "80840" + base9]
    total = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return base9 + str((10 - total % 10) % 10)


class World:
    pass


def fq_of(d):
    for k, a, b, cq in FQ:
        if a <= d <= b:
            return k
    return None


def calq(d):
    return "%dQ%d" % (d.year, (d.month - 1) // 3 + 1)


def _ndc(labeler, i, pk):
    return "%s-%04d-%02d" % (labeler, 1100 + 37 * i + (i * i) % 29, pk)


def _people(rng, w):
    """Members: subscribers and dependants per account, each with an old cardholder number and person code (before
    1 January 2026) and a new one (from it), the new person codes ordered by relationship and birth date."""
    names_used = set()
    persons = []
    for acc, old, new, name, n_members, mean_age in ACCOUNTS:
        n_sub = int(round(n_members / 1.92))
        old_base = {"STA": 4802, "HED": 3317, "LOC": 2268, "RET": 1593}[acc]
        new_base = {"STA": 7731, "HED": 7184, "LOC": 7562, "RET": 7019}[acc]
        olds = rng.choice(np.arange(10000, 99999), size=n_sub, replace=False)
        news = rng.choice(np.arange(100000, 999999), size=n_sub, replace=False)
        for s in range(n_sub):
            age = float(np.clip(rng.normal(mean_age, 9.5 if acc != "RET" else 3.2), 22 if acc != "RET" else 52, 64.9))
            dob = dt.date(2026, 1, 1) - dt.timedelta(days=int(age * 365.25 + rng.integers(0, 365)))
            fam = [("E", dob, "M" if rng.random() < 0.47 else "F")]
            if rng.random() < (0.55 if acc != "RET" else 0.62):
                sp_age = age + rng.normal(-1.5, 4.0)
                fam.append(("S", dt.date(2026, 1, 1) - dt.timedelta(days=int(sp_age * 365.25 + rng.integers(0, 365))),
                            "F" if fam[0][2] == "M" else "M"))
            if acc != "RET":
                for _ in range(int(rng.choice([0, 0, 1, 1, 2, 2, 3], p=[.18, .14, .17, .14, .2, .1, .07]))):
                    c_age = float(np.clip(rng.normal(max(2, age - 30), 6), 0.3, 25.5))
                    fam.append(("D", dt.date(2026, 1, 1) - dt.timedelta(days=int(c_age * 365.25 + rng.integers(0, 365))),
                                "M" if rng.random() < 0.5 else "F"))
            # old person codes: employee 01, then the others in the order they were enrolled
            others = fam[1:]
            order_old = list(range(len(others)))
            rng.shuffle(order_old)
            old_codes = {0: "01"}
            for rank, idx in enumerate(order_old):
                old_codes[idx + 1] = "%02d" % (rank + 2)
            # new person codes: employee 01, spouse 02, children 03 onward by birth date, oldest first
            kids = sorted([i for i, f in enumerate(fam) if f[0] == "D"], key=lambda i: fam[i][1])
            new_codes = {0: "01"}
            for i, f in enumerate(fam):
                if f[0] == "S":
                    new_codes[i] = "02"
            for rank, i in enumerate(kids):
                new_codes[i] = "%02d" % (rank + 3)
            old_card = "%s%05d" % (old, int(olds[s]))
            new_card = "%s%06d" % (new[-2:], int(news[s]))
            for i, (rel, dob_i, sex) in enumerate(fam):
                persons.append(dict(acc=acc, rel=rel, dob=dob_i, sex=sex, old_card=old_card, old_pc=old_codes[i],
                                    new_card=new_card, new_pc=new_codes[i], fam=old_card))
    # a share of members leave before 1 January 2026 (only old ids) and join after it (only new ids)
    for p in persons:
        r = rng.random()
        p["term"] = None
        p["start"] = FY_START
        if r < 0.045:
            p["term"] = FY_START + dt.timedelta(days=int(rng.integers(20, 170)))
        elif r < 0.09:
            p["start"] = RENUMBER + dt.timedelta(days=int(rng.integers(0, 150)))
    return persons


def build():
    rng = np.random.default_rng(SEED)
    w = World()
    w.mfr = {k: dict(name=n, stmt=s, labeler=l) for k, n, s, l in MFR}
    w.products = {}
    for i, p in enumerate(PRODUCTS):
        (key, m, c, brand, inn, pkg, units, uom, per30, wac, share, prof) = p
        w.products[key] = dict(key=key, mfr=m, cls=c, brand=brand, inn=inn, pkg=pkg, units=units, uom=uom,
                               per30=per30, wac_pkg=wac, rshare=share, prof=prof,
                               ndc=_ndc(w.mfr[m]["labeler"], i, 1 if prof != "S" else 21))
    for j, (key, m, brand, inn, units, wac, share) in enumerate(OTHER):
        w.products[key] = dict(key=key, mfr=m, cls="OTH", brand=brand, inn=inn, pkg="%s units" % units, units=units,
                               uom="EA", per30=units, wac_pkg=wac, rshare=share, prof="R",
                               ndc=_ndc(w.mfr[m]["labeler"], 60 + j, 11))
    # the rebate per package: a share of WAC, cents; per 30-day supply it is the same per unit of quantity
    for p in w.products.values():
        p["rebate_pkg"] = round(p["wac_pkg"] * p["rshare"], 2)
        p["rebate_unit"] = p["rebate_pkg"] / p["units"]
    w.persons = _people(rng, w)
    w.pharmacies = _pharmacies(rng)
    w.claims = _claims(rng, w)
    w.statements = _statements(rng, w)
    return w


def _pharmacies(rng):
    chains = ["Walgreens", "CVS Pharmacy", "Kroger Pharmacy", "Walmart Pharmacy", "Rite Aid", "Costco Pharmacy",
              "Publix Pharmacy", "Meijer Pharmacy"]
    indep = ["Main Street Pharmacy", "Family Drug Center", "Hillcrest Apothecary", "Northside Pharmacy",
             "Valley Health Pharmacy", "Medicine Shoppe", "Corner Drug", "Parkview Pharmacy", "Riverside Drug",
             "Westgate Pharmacy", "Lakeshore Pharmacy", "Union Avenue Drug"]
    out = []
    used = set()

    def npi():
        while True:
            b = "1" + "".join(str(int(x)) for x in rng.integers(0, 10, 8))
            n = luhn_npi(b)
            if n not in used:
                used.add(n)
                return n
    for k in range(96):
        nm = chains[k % len(chains)] if k < 64 else indep[(k - 64) % len(indep)]
        store = int(rng.integers(1000, 19999))
        out.append(dict(npi=npi(), name="%s #%d" % (nm, store) if k < 64 else nm, channel="RETAIL", c340b=False,
                        since=dt.date(2019, 1, 1)))
    out.append(dict(npi=npi(), name="Halcroft Home Delivery Pharmacy", channel="MAIL", c340b=False, since=dt.date(2019, 1, 1)))
    out.append(dict(npi=npi(), name="Halcroft Specialty Pharmacy", channel="SPECIALTY", c340b=False,
                    since=dt.date(2019, 1, 1)))
    out.append(dict(npi=npi(), name="Halcroft Specialty Pharmacy - Southeast", channel="SPECIALTY", c340b=False,
                    since=dt.date(2021, 7, 1)))
    # hospital outpatient pharmacies: retail until 1 March 2026, then the specialty network
    for nm, c3 in (("University Medical Center Outpatient Pharmacy", True), ("St. Brigid Health Outpatient Pharmacy", False),
                   ("Mercy Ridge Hospital Pharmacy", True)):
        out.append(dict(npi=npi(), name=nm, channel="SPECIALTY", c340b=c3, since=NETWORK_MOVE, before="RETAIL"))
    # two community health center pharmacies registered as 340B covered entities, retail network
    for nm in ("Eastside Community Health Pharmacy", "Lincoln Family Health Center Pharmacy"):
        out.append(dict(npi=npi(), name=nm, channel="RETAIL", c340b=True, since=dt.date(2019, 1, 1)))
    return out


def channel_on(ph, d):
    if ph.get("before") and d < ph["since"]:
        return ph["before"]
    return ph["channel"]


def _claims(rng, w):
    """Every brand fill in FY2026 for every product: users persist across months so a member's history is real, fill
    sizes follow the channel (30-day retail, 90-day retail or mail, specialty for the specialty drugs), and a small
    share of fills are reversed or paid late."""
    persons_by_acc = {a: [p for p in w.persons if p["acc"] == a] for a in ACC}
    ph = w.pharmacies
    retail = [p for p in ph if p["channel"] == "RETAIL" and not p["c340b"]]
    c340 = [p for p in ph if p["channel"] == "RETAIL" and p["c340b"]]
    hosp = [p for p in ph if p.get("before")]
    mail = [p for p in ph if p["channel"] == "MAIL"]
    spec = [p for p in ph if p["channel"] == "SPECIALTY" and not p.get("before")]
    claims = []
    months = [(dt.date(2025, 7, 1) if m == 0 else None) for m in range(12)]
    month_starts = [dt.date(2025 + (6 + m) // 12, (6 + m) % 12 + 1, 1) for m in range(12)]
    cno = [900000000 + int(rng.integers(0, 50000))]

    def new_claim_no():
        cno[0] += int(rng.integers(1, 9))
        return cno[0]

    keys = list(w.products)
    for key in keys:
        p = w.products[key]
        for a_i, acc in enumerate(ACC):
            members = ACCOUNTS[a_i][4]
            pool = persons_by_acc[acc]
            # monthly 30-day supplies by fiscal month
            target = []
            for m in range(12):
                q = m // 3
                mm = members / 1000.0
                if p["cls"] in REVIEWED:
                    v = mm * CLASS_RATE[p["cls"]][a_i] * SHARE[key][a_i] * (1 + DRIFT.get(key, (0, 0, 0, 0))[q])
                    v *= SEASON.get(p["cls"], (1, 1, 1, 1))[q]
                elif p["cls"] == "OTH":
                    v = mm * OTHER_RATE[a_i] / len(OTHER) * (0.6 + 0.8 * ((keys.index(key) * 7 + a_i * 3) % 10) / 10.0)
                else:
                    v = mm * OUT_RATE[key][a_i] * OUT_TREND.get(key, (1, 1, 1, 1))[q]
                target.append(v)
            mean_monthly = float(np.mean(target))
            # users: enough that each fills about every month (90-day fills count three)
            n_users = max(1, int(round(mean_monthly * (1.12 if p["prof"] != "S" else 1.05))))
            ages = np.array([(dt.date(2026, 1, 1) - x["dob"]).days / 365.25 for x in pool])
            wgt = np.clip(ages - 18, 0.5, None) ** (2.2 if p["cls"] in ("DOAC", "BASAL", "SGLT2", "ONC") else 1.2)
            if p["cls"] in ("ICS", "OTH", "MIG"):
                wgt = np.clip(ages, 3, None) ** 0.6
            wgt = wgt / wgt.sum()
            users = rng.choice(len(pool), size=n_users, replace=False, p=wgt)
            for u_i, u in enumerate(users):
                person = pool[int(u)]
                # channel habit of this user
                if p["prof"] == "S":
                    hab = "SPECIALTY"
                else:
                    r = rng.random()
                    hab = "MAIL" if r < 0.17 else ("RETAIL90" if r < 0.31 else "RETAIL30")
                ph_user = None
                if hab == "SPECIALTY":
                    ph_user = spec[int(rng.integers(0, len(spec)))] if rng.random() < 0.86 else hosp[int(rng.integers(0, len(hosp)))]
                elif hab == "MAIL":
                    ph_user = mail[0]
                else:
                    rr = rng.random()
                    if rr < 0.022:
                        ph_user = c340[int(rng.integers(0, len(c340)))]
                    elif rr < 0.040 and p["cls"] in ("GLP1", "BASAL", "DOAC", "ICS", "HCV", "AST", "MIG"):
                        ph_user = hosp[int(rng.integers(0, len(hosp)))]
                    else:
                        ph_user = retail[int(rng.integers(0, len(retail)))]
                # the months this user fills: a start and a stop inside the year, weighted to the quarter's target
                start_m = int(rng.choice(12, p=_month_weights(target, "start")))
                if rng.random() < 0.62:
                    start_m = 0
                stop_m = 11 if rng.random() < 0.78 else int(rng.integers(start_m, 12))
                span = 3 if hab in ("MAIL", "RETAIL90") else 1
                m = start_m
                day = int(rng.integers(1, 28))
                rx = int(rng.integers(1000000, 9999999))
                fill_no = int(rng.integers(0, 4))
                while m <= stop_m:
                    first = month_starts[m]
                    if person["term"] and first > person["term"]:
                        break
                    if first < person["start"] - dt.timedelta(days=31):
                        m += span
                        continue
                    if rng.random() < _keep_prob(target, m, mean_monthly):
                        d = first + dt.timedelta(days=min(day + int(rng.integers(-3, 4)), 27) - 1)
                        if d < FY_START:
                            d = FY_START
                        packs = span * (1 if p["prof"] == "S" or p["units"] >= 4 else 1)
                        qty = round(p["per30"] * span * (1.0 if key != "GLP_A" else 1.0), 3)
                        ds = {1: 30, 3: 90}[span]
                        if key in ("GLP_A",):
                            ds = 28 * span
                        if key in ("ADA_A", "ADA_B", "ADA_C"):
                            ds = 28
                        if p["cls"] == "BASAL":
                            ds = int(rng.choice([25, 30, 34, 38, 45, 50])) * span
                        claims.append(dict(key=key, acc=acc, person=person, ph=ph_user, d=d, qty=qty, ds=ds,
                                           hab=hab if hab != "SPECIALTY" else "SPECIALTY", rx=rx, fill=fill_no))
                        fill_no += 1
                    m += span
    # paid dates, reversals and late payment
    for c in claims:
        c["paid"] = c["d"] + dt.timedelta(days=int(rng.choice([0, 0, 0, 1, 1, 2, 3])))
        r = rng.random()
        c["rev"] = None
        if r < 0.034:
            c["rev"] = c["paid"] + dt.timedelta(days=int(rng.choice([0, 1, 2, 5, 9, 16])))
        elif r < 0.040:
            c["rev"] = c["paid"] + dt.timedelta(days=int(rng.integers(50, 110)))    # reversed after the invoice cut-off
        if rng.random() < 0.0085:
            c["paid"] = c["d"] + dt.timedelta(days=int(rng.integers(70, 120)))         # paid late
        if c["paid"] > PAID_THROUGH:
            c["paid"] = None                                                            # not yet paid at the extract
        if c["rev"] and (c["paid"] is None or c["rev"] > PAID_THROUGH):
            c["rev"] = None
        c["no"] = new_claim_no()
        c["rev_no"] = new_claim_no() if c["rev"] else None
    claims = [c for c in claims if c["paid"] is not None and FY_START <= c["d"] <= FY_END]
    # pricing
    for c in claims:
        p = w.products[c["key"]]
        ch = channel_on(c["ph"], c["d"])
        disc = DISCOUNT["SPECIALTY" if ch == "SPECIALTY" else ("MAIL" if ch == "MAIL" else "RETAIL")]
        unit_wac = p["wac_pkg"] / p["units"]
        c["ingr"] = round(unit_wac * AWP_FACTOR * (1 - disc) * c["qty"], 2)
        c["chan"] = ch
        fee_key = "SPECIALTY" if ch == "SPECIALTY" else ("MAIL" if ch == "MAIL" else ("RETAIL90" if c["ds"] >= 84 else "RETAIL30"))
        c["fee"] = FEE[fee_key]
        c["fee_key"] = fee_key
        thirty = c["qty"] / p["per30"]
        if p["cls"] == "BASAL":
            pay = min(35.0 * max(1, round(thirty)), c["ingr"])
        elif ch == "SPECIALTY" or p["prof"] == "S":
            pay = min(round(0.2 * c["ingr"], 2), 250.0)
        else:
            pay = (40.0 if c["ds"] < 84 else 100.0)
        c["pay"] = min(round(pay, 2), round(c["ingr"] + c["fee"], 2))
        c["plan"] = round(c["ingr"] + c["fee"] - c["pay"], 2)
        c["eligible"] = not c["ph"]["c340b"]
        c["rebate"] = round(p["rebate_unit"] * c["qty"], 2) if c["eligible"] else 0.0
    return claims


def _month_weights(target, kind):
    t = np.array(target)
    t = t / t.sum()
    return t


def _keep_prob(target, m, mean):
    return float(np.clip(0.80 * target[m] / mean, 0.35, 0.995))


def _statements(rng, w):
    """The PBM's quarterly rebate remittances: for each calendar quarter, each manufacturer and each account, the
    rebates on claims filled in the quarter and adjudicated by the invoice cut-off (current), and adjustments for
    earlier quarters' claims paid or reversed after their cut-off (prior period)."""
    acc_new = {a[0]: a[2] for a in ACCOUNTS}
    lines = []   # (statement quarter, kind, service quarter, mfr, acc, amount)
    by = {}
    for c in w.claims:
        if not c["eligible"]:
            continue
        sq = calq(c["d"])
        m = w.products[c["key"]]["mfr"]
        # the claim's rebate is earned when it is invoiced
        inv_q = sq if c["paid"] <= CUTOFF[sq] else _next_q(sq)
        kind = "CUR" if inv_q == sq else "PPA"
        by.setdefault((inv_q, kind, sq, m, c["acc"]), 0.0)
        by[(inv_q, kind, sq, m, c["acc"])] += c["rebate"]
        if c["rev"]:
            rq = sq if (kind == "CUR" and c["rev"] <= CUTOFF[sq]) else None
            if rq is None:
                rev_inv = _next_q(sq) if c["rev"] <= CUTOFF.get(_next_q(sq), dt.date(2099, 1, 1)) else _next_q(_next_q(sq))
                if kind == "PPA" and c["rev"] <= CUTOFF[_next_q(sq)]:
                    rev_inv = _next_q(sq)
                by.setdefault((rev_inv, "PPA", sq, m, c["acc"]), 0.0)
                by[(rev_inv, "PPA", sq, m, c["acc"])] -= c["rebate"]
            else:
                by[(inv_q, kind, sq, m, c["acc"])] -= c["rebate"]
    for k, v in by.items():
        lines.append(dict(stmt=k[0], kind=k[1], svc=k[2], mfr=k[3], acc=k[4], amount=round(v, 2)))
    # FY2025 claims (outside the extract): the April to June 2025 statement and late adjustments on the next one
    fy25 = {}
    for m in w.mfr:
        for a_i, acc in enumerate(ACC):
            base = sum(l["amount"] for l in lines if l["mfr"] == m and l["acc"] == acc and l["svc"] == "2025Q3"
                       and l["kind"] == "CUR")
            if base == 0:
                continue
            fy25[(m, acc)] = base * float(rng.uniform(0.93, 0.99))
            lines.append(dict(stmt="2025Q2", kind="CUR", svc="2025Q2", mfr=m, acc=acc, amount=round(fy25[(m, acc)], 2)))
            lines.append(dict(stmt="2025Q2", kind="PPA", svc="2025Q1", mfr=m, acc=acc,
                              amount=round(fy25[(m, acc)] * float(rng.uniform(-0.004, 0.012)), 2)))
            lines.append(dict(stmt="2025Q3", kind="PPA", svc="2025Q2", mfr=m, acc=acc,
                              amount=round(fy25[(m, acc)] * float(rng.uniform(-0.003, 0.014)), 2)))
    lines = [l for l in lines if l["stmt"] in CAL_Q and abs(l["amount"]) >= 0.005]
    return lines


def _next_q(q):
    y, k = int(q[:4]), int(q[-1])
    return "%dQ%d" % (y + (k == 4), 1 if k == 4 else k + 1)
