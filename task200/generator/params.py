"""Every constant the world is drawn from. Nothing here is a graded figure: the graded figures are computed forward
from the records the world produces (solve.py), and checks.py asserts them against the clean truth."""
import datetime as dt

SEED = 20027
ORG = "Brackenford Airport Ltd"
AIRPORT = "Brackenford Airport"

TEAMS = ["Arden", "Brook", "Cleve", "Dene", "Esk", "Fell"]
# probability that a member finds a threat image on a first meeting, at an image of average difficulty
NOVEL = {"Arden": 0.845, "Brook": 0.716, "Cleve": 0.878, "Dene": 0.712, "Esk": 0.800, "Fell": 0.650}
SKILL_SD = 0.28                      # spread of members' own skill on the logit scale
FAMILIARITY = 1.65                   # logit lift on an image met many times before
FAM_HALF = 0.5                       # f(k) = 1 - FAM_HALF ** k for k earlier meetings with the image
DIFF_SD = 0.50                       # images' own difficulty on the logit scale
CATEGORY = {"IED": 0.35, "Firearm": -0.10, "Knife": -0.25, "Other": 0.10}
CATEGORY_MIX = [("IED", 0.30), ("Firearm", 0.25), ("Knife", 0.30), ("Other", 0.15)]
CANCEL_P = 0.028                     # projections cancelled before display (bag pulled back, belt reversed)

# team sizes on the 31 December 2026 roster, members who left during the years, starters
SIZE = {"Arden": 18, "Brook": 17, "Cleve": 19, "Dene": 16, "Esk": 18, "Fell": 15}
STARTERS_2026 = {"Arden": 2, "Brook": 2, "Cleve": 1, "Dene": 2, "Esk": 1, "Fell": 0}
LEAVERS = {"Arden": 2, "Brook": 3, "Cleve": 1, "Dene": 2, "Esk": 2, "Fell": 1}   # left at some point 2024-2026

# screens and libraries
CT_START = dt.date(2024, 3, 4)       # Central Search CT lanes and their remote screening room in service
PB_START = dt.date(2023, 9, 11)      # Pier B legacy library loaded
PB_ADD = dt.date(2026, 4, 20)        # sixty images added to the Pier B library
N_CT_IMAGES = 6000
N_PB_IMAGES = 420
N_PB_ADD = 60
END = dt.date(2026, 12, 31)

# the working pattern
CYCLE = 8                            # four on, four off
TEAM_OFFSET = {"Arden": 0, "Brook": 2, "Cleve": 4, "Dene": 6, "Esk": 1, "Fell": 3}
LEAVE_DAYS = 26                      # annual leave and absence days a year, drawn per person
SESSIONS_PER_SHIFT = (5, 8)          # screen sessions a shift, inclusive
SESSION_MIN = (17.0, 2.1)            # minutes at a screen, mean and sd, truncated to 9 to 20 (SPS-04 5.1)
HOURS_EDGE_TARGET = 0.03          # every team's 2026 screen time at least this far (hours) from a tenth-of-an-hour edge
GAP_MIN = (38.0, 9.0)                # minutes off the screen between sessions
TIP_PER_HOUR = 1.22                  # projections a screen-hour
REJECT_PER_HOUR = {"Arden": 1.55, "Brook": 1.10, "Cleve": 1.45, "Dene": 1.70, "Esk": 2.75, "Fell": 1.60}
FIND_SHARE = 0.17                    # share of rejected trays in which the search finds a prohibited or restricted item
ESK_PIERB_PER_DAY = (0, 0)           # no other team covers Pier B: the pier is Fell's
MULTIPLEX_P = 0.31                   # share of Central sessions on a two-lane queue (one row per lane)

# Pier B legacy screen event behaviour
PB_PROMPT_MIN = 20                   # minutes after a Pier B log-on at which the screen prompts the operator to log off
PB_LOGOFF_P = 0.56                   # sessions ended by the operator's own log-off
PB_SHUTDOWN_P = 0.08                 # sessions ended by the screen's end-of-day shutdown (the rest end at the next log-on)

# certification
CERT_YEARS = 3
CERT_CUTOFF = dt.date(2027, 7, 1)
EXTERNAL_P = 0.38                    # recertifications sat at the external assessment centre
ENTRY_LAG = (16, 75)                 # days from an external assessment to the LMS entry, uniform
LMS_EXPORT = dt.date(2027, 1, 11)    # the LMS export: entries keyed after it are not in it
EARLY_RENEWALS = 2                   # renewals booked at the centre in December 2026, ahead of a spring 2027 expiry

# the pack
EXPORT_DATE = dt.date(2027, 1, 15)
EXPORT_STAMP = (2027, 1, 15, 8, 40, 0)
