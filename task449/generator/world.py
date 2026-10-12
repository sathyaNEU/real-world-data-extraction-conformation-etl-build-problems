"""The world behind task449: Fenwright Contact Services runs the card complaint desk of Bellcroft Bank under an annual
statement of work; Bellcroft's ACH processor, Meridel Payment Systems, posted the payments of 8 to 10 May 2026 late;
from 18 May the social care desk opened a matter on every complaint post and attached the first cardholder its
name-and-city search returned. Every figure the pack carries is simulated from these parameters."""
import datetime as dt

SEED = 449
ISSUER = "Bellcroft Bank"
BPO = "Fenwright Contact Services"
PROCESSOR = "Meridel Payment Systems"
AGENCY_A = "Marlowby Staffing"                 # surge placements, decimal hours
AGENCY_B = "Treadwell & Oake"                  # evening cover all year, hours and minutes after a point
OTHER_CLIENT = "Wrexley Energy"               # Fenwright's other program on the same site

GO_LIVE = dt.date(2025, 10, 1)                 # the case system's first matter
PULL = dt.date(2026, 10, 9)                    # the workforce planning pull for the October budget
LAST_DAY = dt.date(2026, 10, 8)                # last full day in the export
FAILURE = (dt.date(2026, 5, 8), dt.date(2026, 5, 10))
SOCIAL_PRACTICE = dt.date(2026, 5, 18)         # matters opened on every complaint post from this day
REMEDIATION = (dt.date(2026, 7, 20), dt.date(2026, 7, 24))
WIN = (dt.date(2026, 8, 3), dt.date(2026, 9, 27))
COMMITTEE = dt.date(2026, 10, 15)
RATE = 27.5                                    # matters per analyst-week, WPS-3 section 4.1
TEAM_2026 = 32

CHANNELS = ["Phone", "Digital", "CFPB", "State", "Executive", "Social"]
FOUR = ["PAY-01", "FEE-01", "FEE-02", "CRB-01"]
CODES = [  # code, description, family
    ("PAY-01", "Payment not credited or credited late", "Payments"),
    ("PAY-02", "Payment amount, allocation or returned payment", "Payments"),
    ("FEE-01", "Late fee charged", "Fees and interest"),
    ("FEE-02", "Interest or finance charge", "Fees and interest"),
    ("FEE-03", "Annual, foreign transaction or other fee", "Fees and interest"),
    ("CRB-01", "Late payment reported to a credit bureau", "Credit reporting"),
    ("CRB-02", "Other credit reporting error", "Credit reporting"),
    ("DSP-01", "Transaction dispute or chargeback", "Disputes and fraud"),
    ("FRD-01", "Fraud or unauthorized use", "Disputes and fraud"),
    ("RWD-01", "Rewards earned or redeemed", "Rewards"),
    ("SVC-01", "Statement, card or address servicing", "Account servicing"),
    ("LIM-01", "Credit line increase or decrease", "Account servicing"),
    ("CLS-01", "Account closure", "Account servicing"),
    ("COL-01", "Collections contact or hardship", "Collections"),
    ("AGT-01", "Agent conduct or service quality", "Service"),
    ("APP-01", "Application or credit decision", "Applications"),
    ("OTH-99", "Other", "Other"),
]
# the mix of a non-incident complaint's code, by channel kind (four-code complaints are drawn separately)
OTHER_MIX = {"PAY-02": 0.07, "FEE-03": 0.06, "CRB-02": 0.05, "DSP-01": 0.20, "FRD-01": 0.12, "RWD-01": 0.10,
             "SVC-01": 0.11, "LIM-01": 0.06, "CLS-01": 0.04, "COL-01": 0.05, "AGT-01": 0.07, "APP-01": 0.04,
             "OTH-99": 0.03}
FOUR_MIX_INCIDENT = {"PAY-01": 0.36, "FEE-01": 0.33, "FEE-02": 0.16, "CRB-01": 0.15}
FOUR_MIX_ROUTINE = {"PAY-01": 0.30, "FEE-01": 0.34, "FEE-02": 0.24, "CRB-01": 0.12}
PRODUCTS = [("Bellcroft Cash Back Visa", 0.42), ("Bellcroft Travel Rewards Mastercard", 0.21),
            ("Bellcroft Platinum Low Rate Visa", 0.19), ("Bellcroft Secured Visa", 0.08),
            ("Bellcroft Business Card", 0.04), ("Bellcroft Student Visa", 0.06)]

# Bellcroft's footprint: cities and their weight among cardholders (posters say their city)
CITIES = [("Columbus", "OH", 0.090), ("Cleveland", "OH", 0.060), ("Cincinnati", "OH", 0.058), ("Toledo", "OH", 0.030),
          ("Akron", "OH", 0.026), ("Dayton", "OH", 0.030), ("Canton", "OH", 0.012), ("Youngstown", "OH", 0.010),
          ("Indianapolis", "IN", 0.070), ("Fort Wayne", "IN", 0.022), ("Evansville", "IN", 0.012),
          ("South Bend", "IN", 0.010), ("Louisville", "KY", 0.050), ("Lexington", "KY", 0.028),
          ("Bowling Green", "KY", 0.008), ("Pittsburgh", "PA", 0.055), ("Erie", "PA", 0.010),
          ("Detroit", "MI", 0.060), ("Grand Rapids", "MI", 0.026), ("Lansing", "MI", 0.014), ("Ann Arbor", "MI", 0.012),
          ("Huntington", "WV", 0.008), ("Charleston", "WV", 0.009), ("Morgantown", "WV", 0.005)]

# Weekly matters before the failure, by channel and kind (other codes, routine four-code complaints).
BASE = {"Phone": (396, 82), "Digital": (229, 47), "CFPB": (44, 13), "State": (17, 5), "Executive": (11, 3),
        "Social": (9, 6)}
# month factor on background volumes
SEASON = {1: 1.05, 2: 1.01, 3: 1.02, 4: 1.00, 5: 1.00, 6: 0.99, 7: 0.98, 8: 1.00, 9: 1.01, 10: 1.00, 11: 0.98,
          12: 0.91}
# the incident: affected four-code matters a week on the phone, by week (Monday); the other channels scale
INCIDENT_PHONE = {
    dt.date(2026, 5, 4): 520, dt.date(2026, 5, 11): 1340, dt.date(2026, 5, 18): 1060, dt.date(2026, 5, 25): 770,
    dt.date(2026, 6, 1): 565, dt.date(2026, 6, 8): 425, dt.date(2026, 6, 15): 335, dt.date(2026, 6, 22): 268,
    dt.date(2026, 6, 29): 214, dt.date(2026, 7, 6): 178, dt.date(2026, 7, 13): 151, dt.date(2026, 7, 20): 142,
    dt.date(2026, 7, 27): 176, dt.date(2026, 8, 3): 150, dt.date(2026, 8, 10): 133, dt.date(2026, 8, 17): 121,
    dt.date(2026, 8, 24): 111, dt.date(2026, 8, 31): 103, dt.date(2026, 9, 7): 96, dt.date(2026, 9, 14): 90,
    dt.date(2026, 9, 21): 85, dt.date(2026, 9, 28): 80, dt.date(2026, 10, 5): 76}
INCIDENT_SCALE = {"Phone": 1.0, "Digital": 0.50, "CFPB": 0.27, "State": 0.11, "Executive": 0.065, "Social": 0.42}
CFPB_LAG_WEEKS = 2                             # the CFPB forwards complaints after its own intake
NAME_CITY_SCALE = 2.18                         # name-and-city incident matters a week per phone incident matter
NAME_CITY_ROUTINE = 60                         # routine four-code name-and-city matters a week once the practice runs
NAME_CITY_OTHER = 45                           # other-code name-and-city matters a week
SURGE_NAME_CITY_ROUTINE = 0.18                 # extra routine four-code posts per incident post in the surge

# The window's exact totals over the eight weeks (each category spread over the weeks with noise).
WIN_TOTALS = {
    ("Phone", "aff"): 883, ("Phone", "routine"): 686, ("Phone", "other"): 3050,
    ("Digital", "aff"): 441, ("Digital", "routine"): 381, ("Digital", "other"): 1781,
    ("CFPB", "aff"): 239, ("CFPB", "routine"): 113, ("CFPB", "other"): 353,
    ("State", "aff"): 97, ("State", "routine"): 41, ("State", "other"): 137,
    ("Executive", "aff"): 57, ("Executive", "routine"): 24, ("Executive", "other"): 88,
    ("Social", "aff"): 369, ("Social", "routine"): 47, ("Social", "other"): 66,      # verified by direct message
    ("NameCity", "four"): 2397, ("NameCity", "other"): 359,
}
WIN_K1 = (597, 478)                            # name-and-city four-code matters whose search returned one cardholder,
                                               # and how many of them arise from the failure
T_NAMECITY = 0.80                              # the share of name-and-city four-code matters arising from the failure
# k: the cardholders a display-name-and-city search returns; bands and their shares (k = 1 handled by WIN_K1)
K_BANDS = [((2, 2), 0.140), ((3, 3), 0.100), ((4, 4), 0.080), ((5, 6), 0.100), ((7, 10), 0.120), ((11, 20), 0.110),
           ((21, 60), 0.100)]
PORTFOLIO_OPEN = {  # open card accounts at each month end
    dt.date(2025, 9, 30): 1601877, dt.date(2025, 10, 31): 1603142, dt.date(2025, 11, 30): 1603990,
    dt.date(2025, 12, 31): 1602415, dt.date(2026, 1, 31): 1604238, dt.date(2026, 2, 28): 1605574,
    dt.date(2026, 3, 31): 1606903, dt.date(2026, 4, 30): 1607912, dt.date(2026, 5, 31): 1608156,
    dt.date(2026, 6, 30): 1607344, dt.date(2026, 7, 31): 1608821, dt.date(2026, 8, 31): 1610067,
    dt.date(2026, 9, 30): 1611480}
AFFECTED_ACCOUNTS = 64318                      # accounts with a payment of 8 to 10 May that posted late
RETURNED_ONLY = 912                            # accounts whose only payment of those days was returned unpaid
TWO_PAYMENTS = 0.031                           # affected accounts with two payments in the file

# handling: median days to close by channel, before the surge multiplier; reopen behaviour
HANDLE_DAYS = {"Phone": 2.6, "Digital": 3.4, "CFPB": 10.5, "State": 17.0, "Executive": 12.0, "Social": 2.2}
REOPEN = 0.043
REOPEN_TWICE = 0.10                            # of reopened matters, the share reopened again
MERGED = 0.0011

# Ask A: flex hours. Fenwright's overtime on the Bellcroft program by month, the floaters' overtime on the other
# client's program, and the agencies' placements.
OT_BCF = {1: 138, 2: 117, 3: 162, 4: 128, 5: 1446, 6: 1183, 7: 947, 8: 702, 9: 561}
OT_OTHER = {1: 42, 3: 28, 7: 55, 8: 36}
MARLOWBY = (dt.date(2026, 5, 12), dt.date(2026, 9, 30))
MARLOWBY_HEADS = {5: 11, 6: 13, 7: 11, 8: 8, 9: 6}
MARLOWBY_RESENT_WEEK = dt.date(2026, 6, 13)    # week ending; re-sent inside the export of 27 June
TREADWELL_HEADS = {1: 5, 2: 5, 3: 5, 4: 5, 5: 7, 6: 7, 7: 6, 8: 6, 9: 6}

PEOPLE = {"planning": "Catherine Schneider", "social": "Stacy Fernandez"}

FIRST = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", "David", "Elizabeth",
         "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Christopher", "Karen",
         "Charles", "Lisa", "Daniel", "Nancy", "Matthew", "Betty", "Anthony", "Sandra", "Mark", "Margaret", "Donald",
         "Ashley", "Steven", "Kimberly", "Andrew", "Emily", "Kenneth", "Donna", "Joshua", "Michelle", "Kevin",
         "Carol", "Brian", "Amanda", "George", "Melissa", "Timothy", "Deborah", "Ronald", "Rebecca", "Jason",
         "Laura", "Ryan", "Cynthia", "Jacob", "Kathleen", "Gary", "Amy", "Nicholas", "Angela", "Eric", "Shirley",
         "Jonathan", "Brenda", "Larry", "Pamela", "Justin", "Emma", "Scott", "Nicole", "Brandon", "Helen",
         "Benjamin", "Samantha", "Samuel", "Katherine", "Gregory", "Christine", "Alexander", "Debra", "Patrick",
         "Rachel", "Frank", "Carolyn", "Raymond", "Janet", "Jack", "Maria", "Dennis", "Olivia", "Jerry", "Heather",
         "Tyler", "Diane", "Aaron", "Julie", "Jose", "Joyce", "Adam", "Victoria", "Nathan", "Kelly", "Henry",
         "Christina", "Zachary", "Lauren", "Douglas", "Joan", "Peter", "Evelyn", "Kyle", "Judith", "Noah", "Megan",
         "Ethan", "Andrea", "Jeremy", "Cheryl", "Walter", "Hannah", "Christian", "Jacqueline", "Keith", "Martha",
         "Roger", "Gloria", "Terry", "Teresa", "Austin", "Ann", "Sean", "Sara", "Gerald", "Madison", "Carl",
         "Frances", "Harold", "Kathryn", "Dylan", "Janice", "Arthur", "Jean", "Lawrence", "Abigail", "Jordan",
         "Alice", "Jesse", "Judy", "Bryan", "Sophia", "Billy", "Grace", "Bruce", "Denise", "Gabriel", "Amber",
         "Joe", "Doris", "Logan", "Marilyn", "Alan", "Danielle", "Juan", "Beverly", "Albert", "Isabella", "Willie",
         "Theresa", "Elijah", "Diana", "Wayne", "Natalie", "Randy", "Brittany", "Vincent", "Charlotte", "Mason",
         "Marie", "Roy", "Kayla", "Ralph", "Alexis", "Bobby", "Lori", "Russell", "Tiffany", "Bradley", "Tammy"]
LAST = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson",
        "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson", "Thompson", "White",
        "Lopez", "Lee", "Gonzalez", "Harris", "Clark", "Lewis", "Robinson", "Walker", "Perez", "Hall", "Young",
        "Allen", "Sanchez", "Wright", "King", "Scott", "Green", "Baker", "Adams", "Nelson", "Hill", "Ramirez",
        "Campbell", "Mitchell", "Roberts", "Carter", "Phillips", "Evans", "Turner", "Torres", "Parker", "Collins",
        "Edwards", "Stewart", "Flores", "Morris", "Nguyen", "Murphy", "Rivera", "Cook", "Rogers", "Morgan",
        "Peterson", "Cooper", "Reed", "Bailey", "Bell", "Gomez", "Kelly", "Howard", "Ward", "Cox", "Diaz",
        "Richardson", "Wood", "Watson", "Brooks", "Bennett", "Gray", "James", "Reyes", "Cruz", "Hughes", "Price",
        "Myers", "Long", "Foster", "Sanders", "Ross", "Morales", "Powell", "Sullivan", "Russell", "Ortiz", "Jenkins",
        "Gutierrez", "Perry", "Butler", "Barnes", "Fisher", "Henderson", "Coleman", "Simmons", "Patterson",
        "Jordan", "Reynolds", "Hamilton", "Graham", "Kim", "Gonzales", "Alexander", "Ramos", "Wallace", "Griffin",
        "West", "Cole", "Hayes", "Chavez", "Gibson", "Bryant", "Ellis", "Stevens", "Murray", "Ford", "Marshall",
        "Owens", "McDonald", "Harrison", "Ruiz", "Kennedy", "Wells", "Alvarez", "Woods", "Mendoza", "Castillo",
        "Olson", "Webb", "Washington", "Tucker", "Freeman", "Burns", "Henry", "Vasquez", "Snyder", "Simpson",
        "Crawford", "Jimenez", "Porter", "Mason", "Shaw", "Gordon", "Wagner", "Hunter", "Romero", "Hicks", "Dixon",
        "Hunt", "Palmer", "Robertson", "Black", "Holmes", "Stone", "Meyer", "Boyd", "Mills", "Warren", "Fox",
        "Rose", "Rice", "Moreno", "Schmidt", "Patel", "Ferguson", "Nichols", "Herrera", "Medina", "Ryan", "Lambert",
        "Weaver", "Daniels", "Stephens", "Gardner", "Payne", "Kelley", "Dunn", "Pierce", "Arnold", "Tran", "Spencer",
        "Peters", "Hawkins", "Grant", "Hansen", "Castro", "Hoffman", "Hart", "Elliott", "Cunningham", "Knight",
        "Bradley", "Kowalski", "Brennan", "Lindqvist", "Okafor", "Szymanski", "Delgado", "Abernathy", "Vukovich"]
