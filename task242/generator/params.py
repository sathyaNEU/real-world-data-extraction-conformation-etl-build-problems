"""task242 world constants: a city corporation's 12 zones, their 2027 dengue epidemics against the post-season
household serosurvey's fieldwork, the IgM assay's detection by days since onset, and the panel that measured it."""
import datetime as dt

SEED = 242
YEAR = 2027
DAY0 = dt.date(2027, 1, 1)               # day 0; the indicator's window opens here
AS_OF = dt.date(2028, 1, 10)              # the morning the flag review is drawn
EXTRACT = dt.date(2028, 1, 8)             # the case line list's extract date
TOL_HIGH, TOL_LOW = 1.5, 2.0 / 3.0       # the misclassification flag's tolerance (quality standard)

# assay: IgM capture ELISA, detection by days since onset (rise near day 4.5, fade near day 72)
SE_MAX, SE_RISE, SE_RISE_S, SE_FADE, SE_FADE_S = 0.95, 4.5, 1.2, 72.0, 13.0
SP = 0.985

BG_SHARE = 0.05                           # the trickle between the waves, as a share of the year's infections

# zone: code, name, kind (design only), fieldwork mid-day, waves (lag before mid, mass, sd), attack, population,
# notified share of infections, households sampled
ZONES = [
    ("I", "Kadalur", "U", 290, [(42, 1.00, 15)], 0.15, 318000, 0.072, 184),
    ("II", "Thenkarai", "U", 300, [(38, 1.00, 14)], 0.12, 276000, 0.064, 180),
    ("III", "Puthanpalli", "T3", 305, [(68, 0.42, 5), (30, 0.58, 8)], 0.13, 341000, 0.069, 182),
    ("IV", "Melmangalam", "F", 330, [(86, 1.00, 13)], 0.17, 262000, 0.061, 180),
    ("V", "Vadakkupatti", "B", 326, [(120, 0.40, 10), (12, 0.55, 8)], 0.21, 297000, 0.058, 186),
    ("VI", "Kizhakkoor", "U", 310, [(36, 1.00, 13)], 0.10, 389000, 0.075, 180),
    ("VII", "Velliyanur", "T1", 316, [(84, 1.00, 6)], 0.14, 244000, 0.066, 178),
    ("VIII", "Chinnakulam", "F", 335, [(90, 1.00, 15)], 0.15, 301000, 0.063, 182),
    ("IX", "Periyamalai", "F", 318, [(84, 1.00, 12)], 0.19, 228000, 0.057, 184),
    ("X", "Kottaivayal", "U", 320, [(44, 1.00, 15), (300, 0.24, 12)], 0.10, 412000, 0.078, 180),
    ("XI", "Sengalur", "B", 335, [(116, 0.40, 10), (11, 0.55, 8)], 0.23, 255000, 0.060, 182),
    ("XII", "Aranmanai", "U", 306, [(40, 1.00, 16)], 0.11, 334000, 0.070, 180),
]
FIELD_HALF = 5                            # each zone's fieldwork runs mid-5 to mid+5

# the laboratory's verification panel: confirmed-case sera from the 2026 follow-up clinic at scheduled visits
# (visit day after onset, spread, specimens) and control sera
PANEL_VISITS = [(3, 1, 30), (7, 1, 80), (14, 1, 90), (21, 1, 75), (30, 2, 62), (45, 2, 48), (60, 2, 46), (75, 2, 46),
                (90, 3, 40), (120, 3, 24), (150, 3, 16)]
PANEL_CONTROLS = 300
