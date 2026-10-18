"""Names, identifiers and people for task169 (every person drawn with guard.py names --geo "United Kingdom" --seed 169)."""
CITY = "Calvermouth"
COUNCIL = "Calvermouth City Council"
COMMITTEE_NAME = "Transport and Environment Committee"

PEOPLE = {
    "atl": ("Eleanor Phillips", "Active Travel Team Leader"),
    "tmo": ("Conor Reynolds", "Traffic Monitoring Officer"),
    "hde": ("Judith Hughes", "Principal Engineer, Highways Design"),
    "hts": ("Kevin Hale", "Head of Transport Strategy"),
    "vol": ("Adrian Hill", "Count Coordinator, Calvermouth Cycle Forum"),
}

# current platform counter ids (structured: CVC-, site block, unit number) and the legacy site names
COUNTER_IDS = {
    "TR1": "CVC-1104", "TR2": "CVC-2117", "TR3": "CVC-2121", "TR4": "CVC-2126",
    "BF1": "CVC-1108", "BF2": "CVC-2203", "BF3": "CVC-2208",
    "EP1": "CVC-1112", "EP2": "CVC-2305", "EP3": "CVC-2311", "EP4": "CVC-2314",
    "WP1": "CVC-1116", "WP2": "CVC-2402", "WP3": "CVC-2409",
    "MS1": "CVC-1207", "MS2": "CVC-2502", "MS3": "CVC-2506", "MS4": "CVC-2513", "MS5": "CVC-2518",
    "SF1": "CVC-1120", "SF2": "CVC-2604", "SF3": "CVC-2610",
}
MS1_OLD_ID = "CVC-0388"      # the Corn Exchange unit replaced in March 2025
LEGACY_NAMES = {
    "TR1": "Tolland Rd - Cathedral Green", "TR2": "Tolland Rd - St Annes Gate", "TR3": "Tolland Bridge",
    "TR4": "Mill Ln (Ashby)", "BF1": "Brickfields - Station Sq", "BF2": "Gasworks Lane",
    "BF3": "Kiln St", "EP1": "Quayside", "EP2": "Boardwalk", "EP3": "Saltings", "EP4": "Heron Point",
    "WP1": "Wardle Park - Exchange St", "WP2": "Lido Gate", "WP3": "Bandstand",
    "MS1": "Corn Exchange", "MS2": "Butter Market", "MS3": "Guild St", "MS4": "Tanners Row",
    "MS5": "Haymarket Steps", "SF1": "Southgate", "SF2": "Belvoir Rd", "SF3": "Fenn Common Br",
}
# legacy channel 1 direction: most sites logged towards the centre on channel 1; two loggers were wired the other way
CH1_IN = {k: True for k in COUNTER_IDS}
CH1_IN["EP3"] = False
CH1_IN["MS4"] = False
TECH = {k: ("inductive loop" if k[2] in "123" and k not in ("EP2", "SF3", "TR3") else "radar") for k in COUNTER_IDS}
TECH.update({"TR3": "radar (deck mounted)", "EP2": "radar (deck mounted)", "SF3": "radar (deck mounted)",
             "TR1": "inductive loop", "BF1": "inductive loop", "EP1": "inductive loop", "WP1": "inductive loop",
             "MS1": "inductive loop", "SF1": "inductive loop"})
CONTRACTOR = "Ferrand Signal Services"
WEATHER_STATION = "Civic Centre roof (CVM-WX1)"
FORUM = "Calvermouth Cycle Forum"
