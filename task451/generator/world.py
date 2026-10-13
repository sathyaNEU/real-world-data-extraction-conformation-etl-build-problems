"""The fiction behind task451: a London-based donor collaborative for maternal and newborn health, its six member
foundations, the two pooled funds they give through, the organisations those funds and members pay, and the other
publishers whose activities a country-and-sector query of the IATI Datastore also returns."""
import datetime as dt

SEED = 451
D = dt.date

COLLAB = "Cardew Collaborative for Maternal and Newborn Health"
COLLAB_SHORT = "Cardew Collaborative"
SECRETARIAT = "Cardew Collaborative secretariat"
PEOPLE = {"data": ("Lesley Hunter", "Head of Data and Learning"),
          "director": ("Lee Sykes", "Director of the Secretariat"),
          "chair": ("Gail Dobson", "Chair of the Members' Council"),
          "finance": ("Kieran Patel", "Finance and Operations Manager")}

PULL = dt.datetime(2026, 10, 5, 7, 14, 52)          # the Datastore query, UTC
EXTRACT_FROM, EXTRACT_TO = D(2023, 1, 1), D(2026, 9, 30)
REGISTER_ASOF = D(2026, 9, 1)
FX_TO = D(2026, 9, 30)
PIPELINE_DATE = D(2026, 6, 30)
YEAR = 2025

# country, ISO code, local currency, region
COUNTRIES = [("Kenya", "KE", "KES", "East Africa"), ("Uganda", "UG", "UGX", "East Africa"),
             ("Tanzania", "TZ", "TZS", "East Africa"), ("Ethiopia", "ET", "ETB", "East Africa"),
             ("Rwanda", "RW", "RWF", "East Africa"), ("Niger", "NE", "XOF", "Sahel"), ("Mali", "ML", "XOF", "Sahel"),
             ("Burkina Faso", "BF", "XOF", "Sahel"), ("Chad", "TD", "XAF", "Sahel"), ("Senegal", "SN", "XOF", "Sahel"),
             ("Nepal", "NP", "NPR", "South Asia"), ("Bangladesh", "BD", "BDT", "South Asia"),
             ("Pakistan", "PK", "PKR", "South Asia")]
NAMES = [c[0] for c in COUNTRIES]
ISO = {c[0]: c[1] for c in COUNTRIES}
NAME_OF = {c[1]: c[0] for c in COUNTRIES}
LOCAL = {c[0]: c[2] for c in COUNTRIES}
REGION = {c[0]: c[3] for c in COUNTRIES}
SAHEL = [c[0] for c in COUNTRIES if c[3] == "Sahel"]

# units of currency per US dollar on 1 January 2023, and the drift to 30 September 2026 (a shock date and size for
# the birr's float in July 2024)
FX0 = {"GBP": (0.829, 0.745), "EUR": (0.937, 0.853), "NOK": (9.86, 10.02), "CHF": (0.925, 0.797),
       "KES": (123.4, 129.2), "UGX": (3712.0, 3480.0), "TZS": (2331.0, 2455.0), "ETB": (53.4, 141.8),
       "RWF": (1069.0, 1447.0), "XOF": (614.6, 559.5), "XAF": (614.6, 559.5), "NPR": (131.8, 140.9),
       "BDT": (103.6, 121.9), "PKR": (226.4, 281.6)}
CURRENCIES = ["USD"] + sorted(FX0)

# members: key, name, IATI identifier now, previous identifier, registered in, reporting currency
MEMBERS = [
    ("ASH", "Ashwell Family Foundation", "US-EIN-814472906", None, "United States", "USD"),
    ("MER", "Merriton Fund", "US-EIN-462208153", None, "United States", "USD"),
    ("TRE", "Tremaine Trust", "GB-CHC-1093318", None, "United Kingdom", "GBP"),
    ("FJE", "Stiftelsen Fjellrev", "NO-BRC-918774203", "XI-IATI-FJR", "Norway", "NOK"),
    ("ZIL", "Stichting Zilverlinde", "NL-KVK-41187705", None, "Netherlands", "EUR"),
    ("SEE", "Seelisberg Stiftung", "CH-FDJP-CHE-113.947.226", None, "Switzerland", "CHF"),
]
MEMBER_KEYS = [m[0] for m in MEMBERS]
M = {m[0]: dict(key=m[0], name=m[1], ref=m[2], prev=m[3], country=m[4], ccy=m[5]) for m in MEMBERS}
# the member that moved identifier: its old dataset was last updated on this date and never withdrawn
OLD_DATASET_UPDATED = dt.datetime(2024, 6, 14, 9, 41, 7)
NEW_ID_FROM = D(2024, 7, 1)

FUNDS = {"G": dict(key="G", name="Pelorus Maternal Health Fund", ref="GB-CHC-1184417", short="Pelorus Fund"),
         "S": dict(key="S", name="Sahel Maternal Survival Fund", ref="XI-IATI-SMSF", short="Sahel Fund")}
PARTNERS = {"WEX": dict(name="Wexcombe Foundation", ref="US-EIN-271559304"),
            "KIY": dict(name="Kiyose Global Health Foundation", ref="XI-IATI-KGHF")}
REGIONAL = dict(key="TAM", name="Tamesna Development Facility", ref="XI-IATI-TDF")

# the global fund's collections, received in October to December of each year and paid out the following year:
# members' and partners' totals in US dollars (members at 28.9, 31.7 and 74.64 per cent)
G_COLLECTION = {2023: {"ASH": 3.18, "MER": 2.94, "TRE": 2.71, "ZIL": 2.73, "WEX": 15.05, "KIY": 13.39},
                2024: {"ASH": 5.32, "MER": 4.96, "TRE": 4.86, "ZIL": 4.831, "WEX": 22.73, "KIY": 20.299},
                2025: {"ASH": 5.48, "MER": 32.67, "TRE": 4.71, "ZIL": 4.76, "WEX": 15.24, "KIY": 0.94}}
# the Sahel fund's January rounds (the global fund's part paid from what it held), in US dollars
S_ROUND = {2024: {"G": 10.20, "TAM": 23.80}, 2025: {"G": 17.84, "FJE": 2.61, "SEE": 1.98, "TAM": 7.37},
           2026: {"G": 18.10, "FJE": 1.62, "SEE": 1.20, "TAM": 10.13}}

# design targets for 2025, millions of US dollars (design note, Ladder): members' direct spending E, members' direct
# payments P, the global fund's grants G and the Sahel fund's grants S by country
TARGET = {
    "Kenya": (7.61, 8.09, 0.00, 0.00), "Uganda": (0.98, 1.02, 14.80, 0.00), "Tanzania": (5.05, 4.67, 2.17, 0.00),
    "Ethiopia": (2.74, 2.88, 3.51, 0.00), "Rwanda": (15.05, 17.02, 4.82, 0.00), "Niger": (1.97, 2.00, 2.68, 7.42),
    "Mali": (1.40, 1.50, 0.88, 15.90), "Burkina Faso": (2.32, 2.55, 2.57, 1.97), "Chad": (2.50, 2.57, 3.10, 2.54),
    "Senegal": (2.40, 2.53, 4.13, 2.17), "Nepal": (3.81, 8.54, 2.23, 0.00), "Bangladesh": (3.46, 3.71, 2.20, 0.00),
    "Pakistan": (2.25, 2.40, 4.36, 0.00)}

SECTORS = [("13020", "Reproductive health care"), ("12220", "Basic health care"),
           ("12281", "Health personnel development"), ("13030", "Family planning")]

# implementing organisations the members and the funds pay. A device organisation re-registered in 2024 under a new
# identifier and name and keeps its older activities under the old one: key, country, name now, identifier now,
# name before, identifier before, re-registered on, reporting currency
DEVICE_ORGS = [
    ("KE1", "Kenya", "Mtandao wa Mama Salama", "KE-NCB-218051110347", "Mama Salama Network", "XI-IATI-MSN", D(2024, 3, 11), "KES"),
    ("UG1", "Uganda", "Kigezi Mothers' Health Network", "XI-IATI-KMHN", "Kisoro Safe Births Association", "XI-IATI-KSBA", D(2024, 5, 2), "UGX"),
    ("TZ1", "Tanzania", "Taasisi ya Uzazi Bora Tanzania", "XI-IATI-TUBT", "Uzazi Bora Foundation", "XI-IATI-UBF", D(2024, 2, 19), "TZS"),
    ("ET1", "Ethiopia", "Lehulum Yenatoch Tena Mahber", "XI-IATI-LYTM", "Lehulum Maternal Health Association", "XI-IATI-LMHA", D(2024, 8, 6), "ETB"),
    ("RW1", "Rwanda", "Umuryango Ubuzima Bwiza", "RW-RGB-0012874", "Ubuzima Bwiza Rwanda", "XI-IATI-UBR", D(2024, 4, 23), "RWF"),
    ("NE1", "Niger", "ONG Tanadi Niger", "XI-IATI-OTN", "Association Tanadi pour la Sante Maternelle", "XI-IATI-ATSM", D(2024, 6, 17), "XOF"),
    ("ML1", "Mali", "ONG Musow Keneya Mali", "XI-IATI-OMKM", "Association Musow Keneya", "XI-IATI-AMK", D(2024, 1, 29), "XOF"),
    ("BF1", "Burkina Faso", "ONG Wend-Panga Burkina", "XI-IATI-OWPB", "Association Wend-Panga Sante", "XI-IATI-AWPS", D(2024, 7, 8), "XOF"),
    ("TD1", "Chad", "ONG Hadjer Sante Tchad", "XI-IATI-OHST", "Association Hadjer Sante Mere-Enfant", "XI-IATI-AHSME", D(2024, 3, 25), "XAF"),
    ("SN1", "Senegal", "Association Ndeyu Mbedd Senegal", "XI-IATI-ANMS", "Reseau Ndeyu Mbedd", "XI-IATI-RNM", D(2024, 9, 2), "XOF"),
    ("NP1", "Nepal", "Aama Swasthya Sewa Kendra", "NP-SWC-35824", "Aama Health Service Nepal", "XI-IATI-AHSN", D(2024, 2, 5), "NPR"),
    ("BD1", "Bangladesh", "Shishu Matri Kalyan Sangstha", "BD-NAB-2471", "SMKS Bangladesh", "XI-IATI-SMKS", D(2024, 6, 3), "BDT"),
    ("PK1", "Pakistan", "Sehat-e-Maa Welfare Society", "XI-IATI-SEMWS", "Sehat Maa Foundation", "XI-IATI-SMF", D(2024, 4, 15), "PKR"),
]
# other implementing organisations in the network: key, countries, name, identifier, type, reporting currency
NET_ORGS = [
    ("KE2", ["Kenya"], "Afya Mashinani Trust", "KE-NCB-218051140912", "24", "USD"),
    ("UG2", ["Uganda"], "Bunyoro Midwives Collective", "XI-IATI-BMWC", "24", "USD"),
    ("TZ2", ["Tanzania"], "Kilimanjaro Maternal Care Trust", "XI-IATI-KMCT", "24", "USD"),
    ("ET2", ["Ethiopia"], "Abay Basin Health Partners", "XI-IATI-ABHP", "24", "USD"),
    ("RW2", ["Rwanda"], "Kivu Mothers and Newborns", "RW-RGB-0031552", "24", "USD"),
    ("NE2", ["Niger"], "Zinder Sante Communautaire", "XI-IATI-ZSC", "24", "USD"),
    ("ML2", ["Mali"], "Segou Sages-Femmes Solidaires", "XI-IATI-SSFS", "24", "USD"),
    ("BF2", ["Burkina Faso"], "Centre Kaya pour la Mere et l'Enfant", "XI-IATI-CKME", "24", "USD"),
    ("TD2", ["Chad"], "Mayo-Kebbi Accoucheuses Unies", "XI-IATI-MKAU", "24", "USD"),
    ("SN2", ["Senegal"], "Casamance Sante Maternelle", "XI-IATI-CSMA", "24", "USD"),
    ("NP2", ["Nepal"], "Karnali Birthing Centres Trust", "NP-SWC-41907", "24", "USD"),
    ("BD2", ["Bangladesh"], "Haor Mothers' Health Initiative", "BD-NAB-3315", "24", "USD"),
    ("PK2", ["Pakistan"], "Thar Midwifery Alliance", "XI-IATI-TMA", "24", "USD"),
    ("IN1", ["Kenya", "Uganda", "Ethiopia", "Nepal"], "Fernhill Health International", "GB-CHC-1102855", "21", "GBP"),
    ("IN2", ["Rwanda", "Tanzania", "Bangladesh", "Pakistan", "Uganda"], "Northbridge Global Health", "US-EIN-205118846", "21", "USD"),
    ("IN3", ["Niger", "Mali", "Burkina Faso", "Chad", "Senegal"], "Stichting Moederzorg Wereldwijd", "NL-KVK-34229180", "21", "EUR"),
    ("IN4", ["Pakistan", "Bangladesh", "Chad", "Senegal", "Ethiopia"], "Corvane Maternal Health", "GB-CHC-1164032", "21", "GBP"),
]

# a grant the member stopped: (member, organisation) -> date stopped (the unpaid commitment reversed that day)
CANCELLED = {("ZIL", "ML2"): D(2025, 11, 14)}
