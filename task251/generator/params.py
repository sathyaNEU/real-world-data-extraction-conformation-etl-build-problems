"""The world's fixed facts: the agency, its NOx network, the converters, the titrations, the services and the bench."""
import datetime as dt

ORG = "Agenzia per la Qualità dell'Aria della Bassa Padana"
ORG_SHORT = "AQBP"
NETWORK = "Rete di rilevamento della qualità dell'aria della Bassa Padana"
DOMAIN = "aqbassapadana.it"
LAB = "Laboratorio Regionale di Taratura Strumenti Ambientali"
CONTRACTOR_A = "Tecnoaria Servizi S.r.l."           # titrations until June 2026
CONTRACTOR_B = "Delta Strumentazione S.n.c."       # titrations from July 2026

# people (guard.py names --geo Italy --seed 251)
HEAD = ("Livia Saracino", "responsabile strumentazione")
LAB_CONTACT = ("Patrizio Gilardoni", "coordinatore del banco convertitori")
FIELD_LEAD = ("Jolanda Stefanelli", "capotecnico, Delta Strumentazione")

START = dt.date(2024, 12, 1)       # the network-wide overhaul began on 2 December 2024; the archive opens with it
END = dt.date(2027, 12, 31)
DAYS = (END - START).days + 1
Y28 = dt.date(2028, 1, 1)

THRESHOLD = 0.95                    # EN 14211: a converter below 95 per cent is spent
FORCED_LAG = (3, 9)                 # days between a titration below 95 per cent and the converter's change
UGM3_PER_PPB_NO2 = 1.91             # NO2 at 20 degrees C and 101.3 kPa
UGM3_PER_PPB_NO = 1.25
LIMIT_1H = 200.0                    # the NO2 hourly limit, micrograms per cubic metre

# the converter: efficiency against the NO2 it has reduced since installation, D in ppm-hours
ETA0 = 0.996
ETA_SLOPE = 0.00004                 # per ppm-hour
ETA_KNEE = 90.0                     # ppm-hours where the molybdenum's loss begins to steepen
ETA_CURV = 7.0e-6                   # per (ppm-hour) squared beyond the knee
TITRATION_SD = 0.0035               # one titration's error in efficiency
CONVERTER_SD = 0.02                 # each converter's own life, a lognormal spread on its D scale

SEED = 5100
ASK_SEED = 32
