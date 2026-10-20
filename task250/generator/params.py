"""The world's fixed facts: the consortium, its stations' districts, the quality control's rule and the 2028 change."""
import datetime as dt

ORG = "Consorcio Agroclimático del Ebro Medio"
ORG_SHORT = "the Consorcio"
DOMAIN = "agroclimaebro.es"
NETWORK = "Red Agroclimática del Ebro Medio"
PROGRAMME = "the rural development programme 2021-2027"
OLD_CONTRACTOR = "Talleres Electrónicos Monegrillo SL"
NEW_CONTRACTOR = "Servicios Técnicos Alcanadre SA"
CONTRACT_SWITCH = dt.date(2027, 7, 1)

# people (guard.py names --geo Spain --seed 250)
COORDINATOR = ("Celia Hernando", "network quality coordinator")
FIELD_LEAD = ("Teodoro Falcó", "field team lead")
QC_ADMIN = ("Inés Dávila", "quality-control software")

# districts (comarcas) and their share of the stations, west to east
DISTRICTS = [
    ("CV", "Cinco Villas"), ("RA", "Ribera Alta del Ebro"), ("VJ", "Valdejalón"), ("HH", "Hoya de Huesca"),
    ("MO", "Monegros"), ("SB", "Somontano de Barbastro"), ("CM", "Cinca Medio"), ("BC", "Bajo Cinca"),
]

# the quality control (procedure QC-02 v4)
RADIUS_KM = 75.0
N_NEIGHBOURS = 3
WINDOW = 14
MIN_IN_WINDOW = 10
HOLD_DAYS = 14
SETTING_2025_2027 = 3.0
SETTINGS = (3.0, 3.5, 4.0, 4.5)
BUDGET_YEAR = 28             # the visits the 2028 field plan leaves for drift alerts
TOLERANCE_C = 0.3            # a sensor within 0.3 degrees of the transfer standard is in tolerance

START = dt.date(2025, 1, 1)
DAYS = 3 * 365               # 2025, 2026, 2027 (none a leap year)
N_PROGRAMME = 34
N_CLOSING = 17               # the programme's stations no irrigation community takes over
