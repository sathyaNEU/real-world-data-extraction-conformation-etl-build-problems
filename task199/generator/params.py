"""Fixed parameters of the Tawi Bank world (task199, architecture 2).

Everything a rebuild needs is here or derived from SEED; nothing reads the clock.
"""
import datetime as dt

SEED = 199_2026
EXPORT_DATE = dt.date(2026, 10, 16)          # the in-fiction pull of every export
EXPORT_MTIME = dt.datetime(2026, 10, 16, 17, 40, 0)
YEAR_START = dt.date(2025, 10, 1)            # review year, by value date
YEAR_END = dt.date(2026, 9, 30)
CUTOVER = dt.date(2026, 4, 1)                # legacy core -> T24
LOG_START = dt.date(2025, 9, 1)              # SWIFT and gateway logs start here
LOG_END = dt.date(2026, 10, 15)

# Kenyan public holidays inside the logs' span (no CBK rate, no clearing)
HOLIDAYS = {
    dt.date(2025, 10, 10), dt.date(2025, 10, 20), dt.date(2025, 12, 12), dt.date(2025, 12, 25),
    dt.date(2025, 12, 26), dt.date(2026, 1, 1), dt.date(2026, 3, 20), dt.date(2026, 4, 3),
    dt.date(2026, 4, 6), dt.date(2026, 5, 1), dt.date(2026, 6, 1),
}

BANK = "Tawi Bank Limited"
BANK_BIC = "TAWIKENA"
PROCEDURE_ID = "FCC-07"

# Large cash reporting threshold (procedure 5.1)
CASH_THRESHOLD_USD = 10_000

# The twelve customers on the EDD register.
# expected: declared expected annual turnover in KES (profile)
# tp: target third-party receipts in KES millions (forward drivers, not a fixed answer)
CUSTOMERS = [
    dict(code="C01", cif="0041872", name="Baraka Motors (K) Ltd", legacy_name="BARAKA MOTORS (K) LTD",
         sector="Motor vehicle importer and dealer", branch=("MSA", "Mombasa Moi Avenue", 214),
         expected=640_000_000, tp=1494, fcy=["USD"], collection=False,
         countries="Japan, United Arab Emirates, Uganda", kra="P051188742K"),
    dict(code="C02", cif="0057213", name="Kifaru Energies Limited", legacy_name="KIFARU ENERGIES LIMITED",
         sector="Petroleum products dealer (retail stations)", branch=("IND", "Industrial Area", 118),
         expected=900_000_000, tp=1005, fcy=[], collection=True,
         countries="Kenya", kra="P051397120M"),
    dict(code="C03", cif="0060158", name="Jabali Builders & Civil Works Ltd",
         legacy_name="JABALI BUILDERS & CIVIL WORKS LT", sector="Building and civil engineering contractor",
         branch=("WST", "Westlands", 131), expected=1_150_000_000, tp=402, fcy=[], collection=False,
         countries="Kenya", kra="P051602337D"),
    dict(code="C04", cif="0063941", name="Tumaini General Trading Ltd", legacy_name="TUMAINI GENERAL TRADING LTD",
         sector="General merchandise importer and wholesaler", branch=("RVR", "River Road", 106),
         expected=1_400_000_000, tp=336, fcy=["USD"], collection=False,
         countries="China, Hong Kong, South Sudan, Uganda", kra="P051733481H"),
    dict(code="C05", cif="0066507", name="Pwani Freight and Clearing Limited",
         legacy_name="PWANI FREIGHT AND CLEARING LIMIT", sector="Freight forwarding and customs clearing",
         branch=("MSA", "Mombasa Moi Avenue", 214), expected=520_000_000, tp=575, fcy=["USD"], collection=False,
         countries="United Arab Emirates, India, Uganda", kra="P051820964B"),
    dict(code="C06", cif="0068230", name="Mlima Highlands Tea Company Ltd", legacy_name="MLIMA HIGHLANDS TEA CO LTD",
         sector="Tea processor and exporter", branch=("KER", "Kericho", 322), expected=2_300_000_000, tp=2600,
         fcy=["USD"], collection=False, countries="Pakistan, Egypt, United Kingdom", kra="P051904415Q"),
    dict(code="C07", cif="0071144", name="Savanna Blooms (Naivasha) Limited", legacy_name="SAVANNA BLOOMS NAIVASHA LTD",
         sector="Cut flower grower and exporter", branch=("NVS", "Naivasha", 337), expected=780_000_000, tp=640,
         fcy=["EUR"], collection=False, countries="Netherlands, Germany", kra="P052011876T"),
    dict(code="C08", cif="0072619", name="Lango Digital Electronics Ltd", legacy_name="LANGO DIGITAL ELECTRONICS LTD",
         sector="Consumer electronics importer and retailer", branch=("RVR", "River Road", 106),
         expected=350_000_000, tp=560, fcy=["USD"], collection=True,
         countries="China, United Arab Emirates", kra="P052146690W"),
    dict(code="C09", cif="0075302", name="Neema Pharmaceutical Distributors Ltd",
         legacy_name="NEEMA PHARMACEUTICAL DISTRIBUTO", sector="Pharmaceutical importer and distributor",
         branch=("IND", "Industrial Area", 118), expected=610_000_000, tp=700, fcy=["USD"], collection=False,
         countries="India", kra="P052230158F"),
    dict(code="C10", cif="0077468", name="Imara Gold & Minerals Ltd", legacy_name="IMARA GOLD & MINERALS LTD",
         sector="Gold and gemstone dealer", branch=("NBI", "Kenyatta Avenue", 101), expected=260_000_000, tp=445,
         fcy=["USD"], collection=False, countries="United Arab Emirates", kra="P052315542A"),
    dict(code="C11", cif="0079925", name="Bahari Coast Hotels Limited", legacy_name="BAHARI COAST HOTELS LIMITED",
         sector="Hotels and resorts", branch=("MSA", "Mombasa Moi Avenue", 214), expected=430_000_000, tp=300,
         fcy=[], collection=True, countries="Kenya", kra="P052407781L"),
    dict(code="C12", cif="0081736", name="Sokoni Hardware and Steel Mart Ltd",
         legacy_name="SOKONI HARDWARE AND STEEL MART", sector="Hardware and steel wholesaler",
         branch=("ELD", "Eldoret", 351), expected=300_000_000, tp=390, fcy=["USD"], collection=True,
         countries="China, Turkey", kra="P052591027S"),
]

# Own-account sweeps from a collection account to the main account (KES millions a year)
SWEEPS = {"C02": 1800, "C08": 70, "C11": 90, "C12": 60}

# Declared account with another institution and what moves from it in the year (KES millions)
DECLARED_ELSEWHERE = {
    "C03": dict(bank="Ufanisi Bank Limited", acct="0213047756102", flow=780),
    "C06": dict(bank="Ufanisi Bank Limited", acct="0213091184407", flow=38),
    "C09": dict(bank="Mkuu Commercial Bank Limited", acct="5502881930", flow=24),
}

# U-turn cycles on C04 (US dollars)
UTURN_CYCLES = 44
UTURN_OUT_RANGE = (118_000.0, 486_000.0)
UTURN_BENEFICIARIES = [
    ("HALDEN TRADING LIMITED", "UNIT 1207 TOWER 2 HARBOUR CENTRE", "KOWLOON HONG KONG", "HK", "KWNGHKHH"),
    ("CORVINA HOLDINGS LTD", "14 ARCH. MAKARIOS III AVENUE", "LIMASSOL CYPRUS", "CY", "LMSLCY2L"),
    ("MANGROVE TRADE AND SUPPLY LTD", "LEVEL 3 ALEXANDER HOUSE EBENE", "EBENE MAURITIUS", "MU", "EBNEMUMU"),
    ("PEARL DELTA SOURCING CO LIMITED", "FLAT B 9/F WING ON PLAZA", "TSIM SHA TSUI HONG KONG", "HK", "WNGPHKHH"),
]
UTURN_REMITTERS = [
    ("VARO COMMODITIES FZE", "PLOT S30607 JEBEL ALI FREE ZONE", "DUBAI UAE", "AE", "JBLAAEAD"),
    ("SEABROOK VENTURES LTD", "C/O ANCHOR CORPORATE SERVICES", "PORT LOUIS MAURITIUS", "MU", "PLUSMUMU"),
    ("KESTREL BAY GENERAL TRADING LLC", "OFFICE 1904 PLATINUM TOWER JLT", "DUBAI UAE", "AE", "DXBTAEAD"),
    ("ORCHID PACIFIC LIMITED", "RM 1503 15/F CHINA INSURANCE BLDG", "CENTRAL HONG KONG", "HK", "CNTRHKHH"),
]

# FX: CBK-style mean rates
FX_START = {"USD": 129.2361, "EUR": 150.2240, "GBP": 172.6105}
FX_SD = {"USD": 0.045, "EUR": 0.32, "GBP": 0.38}
FX_SPREAD = {"USD": 0.20, "EUR": 0.31, "GBP": 0.36}
