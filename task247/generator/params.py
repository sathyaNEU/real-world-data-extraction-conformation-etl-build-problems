"""task247 parameters: the reef station, its 16 sites, the seasons, and the keys every module reads."""
import datetime as dt

SEED = 0               # records and documents
SIM_SEED = 23          # the sea, the cloud and the two analyses
LOGGER_SEED = 7        # the loggers and the service trips
SURVEY_SEED = 647      # the 2023 post-bleaching survey

UNIVERSITY = "Universidad Autonoma de Punta Bocanegra"
UNIVERSITY_SHORT = "UAPB"
STATION = "Punta Bocanegra Reef Station"
WATCH = "Reef Heat Stress Watch"
FORUM = "the head of reef monitoring"

# code, name, region, pixel id
SITES = [
    ("PB01", "Bajo Pelicano", "north", "QR5-2104"),
    ("PB02", "Arrecife Las Garzas", "north", "QR5-2163"),
    ("PB03", "Cabezo Tortuga", "north", "QR5-2221"),
    ("PB04", "Punta Abanico", "north", "QR5-2280"),
    ("PB05", "Bajo del Ancla", "north", "QR5-2338"),
    ("PB06", "Arrecife Los Pargos", "central", "QR5-2457"),
    ("PB07", "Cayo Medusa", "central", "QR5-2515"),
    ("PB08", "Bajo Langosta", "central", "QR5-2574"),
    ("PB09", "Arrecife Los Ronquillos", "central", "QR5-2632"),
    ("PB10", "Punta Cascabel", "central", "QR5-2691"),
    ("PB11", "Bajo Coralillo", "south", "QR5-2810"),
    ("PB12", "Arrecife El Tiburon", "south", "QR5-2868"),
    ("PB13", "Cabezo Morena", "south", "QR5-2927"),
    ("PB14", "Bajo Rompiente", "south", "QR5-2985"),
    ("PB15", "Punta Gorgonia", "south", "QR5-3044"),
    ("PB16", "Arrecife Sargazo", "south", "QR5-3102"),
]
NSITE = len(SITES)
# each site's survey depth (m), where its logger sits and its transects are laid
SITE_DEPTH = [9.5, 10.0, 10.5, 9.0, 10.0, 11.0, 10.5, 9.5, 12.0, 10.0, 10.5, 11.5, 10.0, 9.5, 11.0, 10.5]

FIRST_DAY = dt.date(2018, 1, 1)
LAST_REP_DAY = dt.date(2026, 12, 31)       # the reprocessed record released so far
LAST_NRT_DAY = dt.date(2027, 11, 2)        # the near-real-time extract runs to the as-of
ASOF = dt.date(2027, 11, 3)
SEASON = (dt.date(2027, 6, 1), dt.date(2027, 10, 31))
SEASON_MONTHS = (6, 10)

HS_MIN = 1.0           # a HotSpot counts at a degree or more above the maximum monthly mean
WINDOW = 84            # twelve weeks of daily HotSpots
AL1, AL2 = 4.0, 8.0

# the near-real-time analysis
OBS_BIAS = 0.06        # a clear-sky day's analysis runs a little warm of the reprocessed record
OBS_SD = 0.07
TAU = 5.0              # e-folding days of the analysis's relaxation toward climatology under cloud
REP_SD = 0.03
LATE_SHARE = 0.03      # share of cloudy days re-issued as observed when a late pass arrives

# people (guard.py names --geo Mexico --seed 247)
COORDINATOR = ("Fabiola Mireles", "fabiola.mireles")       # the survey's coordinator, who asks
HEAD = ("Alfredo Montero", "alfredo.montero")               # head of reef monitoring, signs the survey list
ANALYST = ("Rocío Muñiz", "rocio.muniz")                    # remote sensing analyst, issues the bulletins
DIVE_LEAD = ("Hernán Pichardo", "hernan.pichardo")          # dive team leader
DOMAIN = "uapb.edu.mx"
