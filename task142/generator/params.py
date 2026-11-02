"""Fixed parameters of the task142 world: Stadswarmte Lekstede's west heat network, its OS West station, and the
Woonstichting Weidehaven blocks that leave their gas boiler rooms for the network in 2027 and 2028. All names are
invented."""
import datetime as dt

SEED = 142
D = dt.date

ASOF = D(2026, 10, 16)
METER_START = D(2025, 10, 1)          # first AMR day (UTC)
METER_END = D(2026, 9, 30)            # last AMR day (UTC)

HEATCO = "Stadswarmte Lekstede"
HEATCO_SHORT = "Stadswarmte"
NETWORK = "Warmtenet West"
STATION = "OS West"
CORP = "Woonstichting Weidehaven"
CONSULT = "Hoogland & Brak bouwfysica"
GRIDOP = "Netbeheer Rivierenland Gas"   # gas grid operator (invented)
CITY = "Lekstede"

PEOPLE = {
    "planner": "Elif Meeusen",       # network capacity planner, Stadswarmte
    "consult": "Maurits Weijland",   # heat-load engineer, Hoogland & Brak
    "corp": "Stella Gnodde",         # programme manager aardgasvrij, Weidehaven
}

CP = 1.163                 # kWh per m3 per K, the procedure's constant
TG_WINDOW = 0.0            # daily mean outdoor temperature at or below which the drop is read (procedure 3.2)
DESIGN_SUPPLY = 90.0       # network maximum supply temperature (design basis 90/50)
DESIGN_RETURN = 50.0
DESIGN_TOUT = -10.0

FILES = {
    "amr": "amr_warmtemeters_west_2025-10-01_2026-09-30.csv",
    "register": "aansluitregister_warmtenet_west_2026-10-01.xlsx",
    "weather": "weerstation_lekstede_dagwaarden_2025-2026.csv",
    "scada": "os_west_scada_uurwaarden_2025-10_2026-09.csv",
    "schedule": "weidehaven_aardgasvrij_fasering_2027-2028.xlsx",
    "revised": "warmteverliesberekening_weidehaven_rev2_2026-09-18.xlsx",
    "prelim": "warmteverliesberekening_weidehaven_concept_2026-03-27.pdf",
    "hydraulic": "hydraulische_toets_os_west_2026-10-09.pdf",
    "procedure": "procedure_capaciteitstoets_aansluitingen_v3.pdf",
    "scope": "weidehaven_aardgasvrij_scope_2027-2028.docx",
    "gasreads": "gas_telemetrie_ketelhuizen_weidehaven_2025-2026.csv",
    "gasmaster": "meterstamgegevens_gas_weidehaven_2026-10-01.xlsx",
    "tariff": "stadswarmte_tarievenblad_2026.pdf",
}
DISTRACTORS = ["prelim", "tariff"]

# headroom and phase loads are tuned in world.tune(); these are the search ranges, not the answer
HEADROOM_RANGE = (138, 166)
