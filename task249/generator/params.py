"""World constants for task249 (architecture 3): an industrial-organisational assessment firm's common online
aptitude test, its 2028 campus season, the 2028 verification equivalence study and the clients' 2029 plans.

Everything here is fiction: the firm, its client employers, the colleges and the people. The psychometric model is
standard: an adaptive test's score is ability plus an error whose spread is the test's conditional standard error,
which widens where the item bank thins; a second sitting brings a retest gain that fades with the days between."""
import datetime as dt

SEED = 249
FIRM = "Medhavi Assessment Labs Pvt Ltd"
FIRM_SHORT = "Medhavi"
PRODUCER = "Medhavi Labs"
TEST = "MAT-R"            # the common online test: Medhavi Aptitude Test, Reasoning (adaptive, 16 items)
VTEST = "MAT-V"           # the proctored verification test (adaptive, 12 items, secure bank)
CITY = "Bengaluru"
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
UTC = dt.timezone.utc

# -- scale: the client-facing scale score is 50 plus 10 per logit, reported whole
SCALE_MID, SCALE_PER_LOGIT = 50.0, 10.0

# -- the online test's conditional standard error (logits), by ability: flat in the middle, wider where the bank
#    thins above about 0.85 and slightly wider at the very bottom
def se_online(t):
    import numpy as np
    t = np.asarray(t, dtype=float)
    return 0.355 + 0.24 * np.clip(t - 0.85, 0, None) ** 1.3 + 0.07 * np.clip(-t - 1.5, 0, None)


def se_verify(t):
    import numpy as np
    t = np.asarray(t, dtype=float)
    return 0.40 + 0.22 * np.clip(t - 0.85, 0, None) ** 1.3 + 0.07 * np.clip(-t - 1.5, 0, None)


def retest_gain(days):
    """the ability-free lift a second sitting brings, in logits, by days since the first"""
    import numpy as np
    return 0.03 + 0.30 * np.exp(-np.asarray(days, dtype=float) / 18.0)


BAND_Z = 1.96             # refer when online > verification + 1.96 x verification SE (upper limit of the 95% band)
CAP = 0.15                # an account's genuine referrals may not exceed 15 per cent of its genuine shortlisted
SEASON = 2028
SITTING_OPEN, SITTING_CLOSE = dt.date(2028, 7, 1), dt.date(2028, 8, 31)

# -- college tiers: ability distribution of final-year candidates (logits) and number of colleges
TIERS = {
    "T1": dict(mu=0.86, sd=0.66, n=26, size=(260, 620)),
    "T2": dict(mu=0.30, sd=0.78, n=92, size=(180, 470)),
    "T3": dict(mu=-0.22, sd=0.84, n=168, size=(140, 420)),
    "T4": dict(mu=-0.62, sd=0.86, n=134, size=(90, 330)),
}

# -- client accounts: code, name, sector, group, tier mix of applicants (shares), application rate at covered
#    campuses, 2028 format, 2029 format, 2029 shortlist size (set against expected applicants in tune)
#    formats: D1 = day-one campus drive (online sitting on drive day, selection day two to four days later),
#             S  = first-company campus drive at a campus with no earlier company (same week as the sitting),
#             L  = later campus drive using the season's earlier result (selection day in September),
#             C  = assessment centre in Bengaluru, Pune or Hyderabad (selection days in October and November)
ACCOUNTS = [
    # code, name, sector, group, tiers, 2028 fmt, 2029 fmt, 2029 shortlist share
    ("KSP", "Kshitijpath Strategy Partners", "management consulting", "E", {"T1": 0.88, "T2": 0.12}, "D1", "D1", 0.022),
    ("VRD", "Vardhanmaan Capital", "investment banking", "E", {"T1": 0.86, "T2": 0.14}, "C", "D1", 0.018),
    ("ANV", "Anvayam Analytics", "analytics", "E", {"T1": 0.80, "T2": 0.20}, "C", "C", 0.030),
    ("PRM", "Pramaanika Advisory", "risk advisory", "E", {"T1": 0.78, "T2": 0.22}, "C", "C", 0.045),
    ("SQR", "Sumedhika Quant Research", "quantitative research", "E", {"T1": 0.92, "T2": 0.08}, "C", "C", 0.033),
    ("ABH", "Abhyudayam Securities", "securities", "E", {"T1": 0.90, "T2": 0.10}, "D1", "D1", 0.020),
    ("MTL", "Mitralekha Consulting", "technology consulting", "E", {"T1": 0.84, "T2": 0.16}, "C", "C", 0.038),
    ("TJM", "Tejomaya Asset Management", "asset management", "E", {"T1": 0.90, "T2": 0.10}, "C", "C", 0.040),
    ("NVK", "Navakar Fintech", "fintech", "M", {"T1": 0.30, "T2": 0.55, "T3": 0.15}, "D1", "D1", 0.16),
    ("SHY", "Sahyagiri Foods", "packaged foods", "M", {"T1": 0.28, "T2": 0.52, "T3": 0.20}, "C", "C", 0.075),
    ("UJB", "Ujjwalan Bank", "retail banking", "M", {"T1": 0.18, "T2": 0.57, "T3": 0.25}, "D1", "D1", 0.12),
    ("TRG", "Tarangini Telecom", "telecom", "M", {"T1": 0.30, "T2": 0.50, "T3": 0.20}, "C", "C", 0.065),
    ("PBH", "Prabhatam Motors", "automotive", "M", {"T1": 0.22, "T2": 0.55, "T3": 0.23}, "L", "L", 0.055),
    ("KVR", "Kaverika Life Sciences", "pharmaceuticals", "M", {"T1": 0.25, "T2": 0.50, "T3": 0.25}, "C", "C", 0.070),
    ("OJS", "Ojasvini Consumer Brands", "consumer goods", "M", {"T1": 0.12, "T2": 0.58, "T3": 0.30}, "D1", "D1", 0.16),
    ("RNJ", "Ranjitgarh Energy", "power utilities", "M", {"T1": 0.15, "T2": 0.55, "T3": 0.30}, "L", "L", 0.060),
    ("CHT", "Chaitanyam Insurance", "insurance", "M", {"T1": 0.14, "T2": 0.56, "T3": 0.30}, "C", "C", 0.080),
    ("LVN", "Lavanyam Retail", "retail", "M", {"T1": 0.12, "T2": 0.53, "T3": 0.35}, "L", "L", 0.070),
    ("IDP", "Indrapath Tech Services", "IT services", "V", {"T2": 0.12, "T3": 0.50, "T4": 0.38}, "L", "L", 0.50),
    ("RNG", "Rangoliya Global Services", "business process services", "V", {"T2": 0.10, "T3": 0.50, "T4": 0.40}, "S", "S", 0.40),
    ("EKD", "Ekadanta Infosystems", "IT services", "V", {"T2": 0.12, "T3": 0.48, "T4": 0.40}, "L", "L", 0.55),
    ("PGT", "Pragatishil Business Solutions", "IT services", "V", {"T2": 0.20, "T3": 0.50, "T4": 0.30}, "C", "C", 0.52),
    ("AKR", "Aksharva IT Services", "IT services", "V", {"T2": 0.10, "T3": 0.52, "T4": 0.38}, "S", "S", 0.35),
    ("BHM", "Bhoomija Digital", "digital services", "V", {"T2": 0.08, "T3": 0.42, "T4": 0.50}, "L", "L", 0.48),
    ("KTV", "Kartavyam Systems", "engineering services", "V", {"T2": 0.25, "T3": 0.50, "T4": 0.25}, "C", "C", 0.58),
    ("UDN", "Udayanta Process Services", "business process services", "V", {"T2": 0.22, "T3": 0.48, "T4": 0.30}, "S", "S", 0.38),
    ("VKT", "Vikatara Tech Labs", "IT services", "V", {"T2": 0.06, "T3": 0.40, "T4": 0.54}, "L", "L", 0.50),
    ("MDN", "Medinika Infotech", "IT services", "V", {"T2": 0.10, "T3": 0.46, "T4": 0.44}, "S", "S", 0.42),
]
# Navakar Fintech took over Paisaghar Lending in July 2028; Paisaghar's campus list ran under its own code (PGL) until
# the client record moved in September, so 2028 shows both codes.
MERGED = {"PGL": ("Paisaghar Lending", "NVK")}
INTERNAL = {"MAL-QA": "Medhavi internal quality assurance", "MAL-DEMO": "Medhavi sales demonstrations"}

# applicant pool sizes (2028), by group
POOL_SIZE = {"E": (3400, 8200), "M": (7000, 19000), "V": (14000, 36000)}

PEOPLE = {
    "head": "Vasudha Padmanabhan",       # head of assessment integrity, who asks
    "psychometrician": "Abhiram Sarin",  # ran the equivalence study
    "client": "Rachita Sunder",          # client services
    "ops": "Nachiket Sarna",             # selection-day operations
    "data": "Ishwar Tella",              # platform data engineer
}
ASOF = dt.date(2029, 5, 14)
