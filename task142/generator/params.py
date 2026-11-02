"""Fixed parameters of the task142 world (architecture 3): Stichting Primair Onderwijs Veenhaven's school De Kwikstaart
in Veenhaven-Noord, its catchment's children in the municipal population register, and the 1 October counts the
school's accommodation request rests on. All names are invented."""
import datetime as dt

SEED = 142
D = dt.date

ASOF = D(2026, 10, 19)
COUNT_YEARS = list(range(2020, 2027))          # 1 October counts on file (2020-21 to 2026-27)
FORECAST_YEARS = [2027, 2028, 2029]            # the counts forecast (2027-28 to 2029-30)
INTAKE_YEARS = [2022, 2023, 2024, 2025, 2026]  # the last five intakes (CT procedure 3.3)

BOARD = "Stichting Primair Onderwijs Veenhaven"
BOARD_SHORT = "SPOV"
SCHOOL = "Basisschool De Kwikstaart"
CITY = "Veenhaven"
DISTRICT = "Veenhaven-Noord"
PROVIDER = "Kinderopvang Het Klavertje"
GRIDOP = "Gasnet Veenstreek"

PEOPLE = {
    "planner": "Annemijn Verhaar",   # beleidsmedewerker huisvesting, SPOV
    "head": "Raf Romijn",            # directeur De Kwikstaart
    "provider": "Norah Bresé",  # locatiemanager, the childcare provider
}

WIJKEN = {"Molenwijk": "3841", "Rietveld": "3842", "De Akkers": "3843", "Noorderpark": "3844"}
CATCHMENT = ("3841", "3842")

FILES = {
    "brp": "brp_uittreksel_veenhaven_noord_2026-10-01.csv",
    "roll": "leerlingtellingen_kwikstaart_1okt_2020-2026.csv",
    "procedure": "spov_procedure_leerlingenprognose_v2.pdf",
    "accommodation": "huisvestingsplan_kwikstaart_2026.pdf",
    "district": "wijkprofiel_veenhaven_noord_2026.pdf",
    "schools": "scholenoverzicht_veenhaven_noord_2026.xlsx",
    "gasreads": "gas_telemetrie_kwikstaart_2023-2026.csv",
    "gasmaster": "meterstamgegevens_gas_kwikstaart_2026-10-01.xlsx",
    "bso_att": "bso_aanwezigheid_oktober_2026.csv",
    "bso_loc": "bso_locaties_contracten_2026-10.xlsx",
    "request": "aanvraag_huisvesting_2028_concept.docx",
    "calendar": "schoolkalender_kwikstaart_2026-2027.pdf",
}
DISTRACTORS = ["district", "calendar"]
