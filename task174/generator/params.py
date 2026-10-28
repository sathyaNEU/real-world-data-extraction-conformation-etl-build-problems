"""Every constant of the task174 world, in one place. Nothing here ships."""
import datetime as dt

SEED = 174_2026
TZ = "America/New_York"
AS_OF = dt.date(2026, 10, 23)          # the roll date and the last day of the fall export
PLAN_DATE = dt.date(2026, 10, 21)
PLACES = 4100                           # reteach places the board funded for Units 4 to 7
LENGTHS = (6, 8, 10)                    # the set lengths the period allows
CHECK = 5                               # check problems after the set
PASS_AT = 3                             # three of five right passes
CAP = 10                                # homework problems a skill builder allows a day
STREAK = 3                              # three right in a row completes a skill builder
RHO = 0.40                              # share of an earlier sitting's gain a student keeps

# Seventh-grade skill builders: (code, unit, title, easiness a, learning slope g). Fall units carry two skill
# builders each, the four spring units one each.
SKILL_BUILDERS = [
    ("1A", 1, "Adding and Subtracting Rational Numbers", -0.90, 0.18),
    ("1B", 1, "Multiplying and Dividing Rational Numbers", -1.20, 0.16),
    ("2A", 2, "Combining Like Terms", -1.00, 0.15),
    ("2B", 2, "Expanding and Factoring Expressions", -1.30, 0.13),
    ("3A", 3, "Unit Rates", -0.30, 0.12),
    ("3B", 3, "Proportional Relationships", -0.60, 0.13),
    ("4", 4, "Percent Problems", -2.26, 0.296),
    ("5", 5, "Equations and Inequalities", -0.657, 0.06),
    ("6", 6, "Angles, Area and Volume", -1.00, 0.167),
    ("7", 7, "Probability and Sampling", -0.70, 0.139),
]
UNIT_TITLES = {1: "Rational Numbers", 2: "Expressions", 3: "Ratios and Proportions", 4: "Percent",
               5: "Equations and Inequalities", 6: "Geometry", 7: "Probability"}
SPRING = ("4", "5", "6", "7")
FALL = ("1A", "1B", "2A", "2B", "3A", "3B")

YEARS = ("2025-26", "2026-27")
# Skill-builder windows (open, close inclusive); 2026-27 holds the four skill builders that closed by the as-of date.
WINDOWS = {
    "2025-26": {"1A": ("2025-09-01", "2025-09-12"), "1B": ("2025-09-15", "2025-09-26"),
                "2A": ("2025-09-29", "2025-10-10"), "2B": ("2025-10-13", "2025-10-24"),
                "3A": ("2025-11-03", "2025-11-14"), "3B": ("2025-11-17", "2025-12-05"),
                "4": ("2026-01-20", "2026-02-02"), "5": ("2026-02-23", "2026-03-06"),
                "6": ("2026-03-30", "2026-04-10"), "7": ("2026-05-04", "2026-05-15")},
    "2026-27": {"1A": ("2026-08-31", "2026-09-11"), "1B": ("2026-09-14", "2026-09-25"),
                "2A": ("2026-09-28", "2026-10-09"), "2B": ("2026-10-12", "2026-10-23")},
}
YEAR_START = {"2025-26": "2025-08-25", "2026-27": "2026-08-24"}
YEAR_END = {"2025-26": "2026-06-10", "2026-27": "2027-06-09"}
EXPORT_DAY = {"legacy": "2026-01-09", "2025-26": "2026-10-19", "2026-27": "2026-10-23"}
LEGACY_UNTIL = "2026-01-01"     # the 2025-26 problems before this day sit in the legacy export
SPRING_2027 = {4: ("2027-01-05", "2027-02-05"), 5: ("2027-02-08", "2027-03-12"), 6: ("2027-03-15", "2027-04-23"),
               7: ("2027-04-26", "2027-05-28")}

# Twelve middle schools: code, name, seventh graders at the start of a year, school ability offset, WIN period minutes.
SCHOOLS = [
    ("TCS-338", "Arrowmere Middle School", 245, 0.25, 40),
    ("TCS-316", "Calderwick Middle", 207, -0.10, 45),
    ("TCS-372", "Dovering Magnet Middle School", 170, -0.35, 35),
    ("TCS-304", "Elmswade Academy (6-8)", 267, 0.40, 40),
    ("TCS-351", "Fallowmere STEM Middle School", 176, -0.20, 45),
    ("TCS-322", "Gorsedale Middle School", 225, 0.05, 40),
    ("TCS-379", "Hollisgrove Middle", 196, -0.15, 35),
    ("TCS-342", "Ivelbrook Middle School", 149, -0.45, 45),
    ("TCS-308", "Juniper Shoals Middle School", 215, 0.15, 40),
    ("TCS-364", "Kettlewyn Middle School", 188, 0.00, 40),
    ("TCS-331", "Larkmoor Leadership Academy", 202, -0.05, 35),
    ("TCS-356", "Quillon Heights Middle School", 161, 0.30, 45),
]
COHORT_SHIFT = {"2025-26": 0.00, "2026-27": -0.06}
THETA_SD = 0.95

# Enrollment movement inside a school year (shares of the starting roll).
P_TRANSFER = 0.045      # moves to another district middle school during the year
P_LEAVE = 0.050         # leaves the district during the year
P_RETURN = 0.30         # of leavers, share who come back later the same year (a second Pellmore account)
P_ARRIVE = 0.050        # arrives from outside the district during the year
P_NO_HOMEWORK = 0.012   # never opens a homework skill builder

PEOPLE = {
    "cao": ("Tara Richardson", "Chief Academic Officer"),
    "coordinator": ("Linda Ramos", "Mathematics Coordinator, Grades 6 to 12"),
    "analyst": ("Heidi Ortega", "Accountability and Data Analyst"),
    "interventions": ("Claire Montoya", "Interventions Program Manager"),
    "budget": ("Gregory Griffin", "Budget Director"),
}
DISTRICT = "Tamberlin County Schools"
VENDOR = "Pellmore Learning"
PRODUCT = "Pellmore Math"
