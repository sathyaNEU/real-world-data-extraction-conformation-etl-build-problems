"""task310 constants: the office, the network, the panel, the programme and its battery, the files and the people."""

ORG = "State Energy Office"
ORG_SHORT = "the Energy Office"
NETWORK = "Southmark Networks"
PROGRAMME = "Home Battery Programme"
PANEL = "Home Energy Monitoring Panel"
PEOPLE = {"director": "Brianna Parrish", "connections": "Keith Ruiz", "panel": "Katelyn Acosta"}
TITLES = {"director": "Director, Home Battery Programme", "connections": "Manager, Customer Connections",
          "panel": "Panel Data Manager"}
BRIEF_DATE = "2026-11-12"
YEAR = 2025

# regions: code, name
REGIONS = {"WEN": "Sandhaven Coast", "BEL": "Eastbrook Metro", "YAR": "Yarrandale Valley", "TAR": "Tarrock Highlands"}
REGION_ORDER = ["WEN", "BEL", "YAR", "TAR"]
ROUND_YEARS = [2027, 2028, 2029, 2030]
ROUND_BATTERIES = 2400

# the programme battery (guideline appendix A)
BAT_USABLE_KWH = 10.0
BAT_POWER_KW = 5.0
BAT_CHARGE_EFF = 0.95
BAT_DISCHARGE_EFF = 0.95

# market time is UTC+10 all year; the local clock adds an hour from the first Sunday in October to the first Sunday
# in April
DST_END_2025 = "2025-04-06 03:00"     # local clock goes back to 02:00
DST_START_2025 = "2025-10-05 02:00"   # local clock goes forward to 03:00

SEED = 310

FILES = {
    "register": "hemp_panel_register_2025.csv",
    "systems": "hemp_solar_systems_2025.xlsx",
    "velkora": "velkora_portal_hourly_2025.parquet",
    "ondrava": "ondrava_cloud_counters_2025.csv",
    "meter": "southmark_meter_halfhours_2025.parquet",
    "connections": "southmark_connection_register_panel.csv",
    "guideline": "home_battery_programme_guideline_2027-2030.pdf",
    "standard": "southmark_ES-114_micro_embedded_generation.pdf",
    "guide": "hemp_data_guide_2025.pdf",
    "tariffs": "standing_offer_tariffs_2025-26.xlsx",
    "survey": "hemp_household_survey_2024.csv",
    "der": "southmark_der_register_2026-09-30.csv",
    "standing": "southmark_nmi_standing_data_2026-09-30.csv",
    "booster": "battery_booster_claims_2021-2023.xlsx",
    "telemetry": "norvane_pilot_battery_telemetry_2025.parquet",
    "pilot_sites": "pilot_round_2024_sites.xlsx",
    "accreditation": "installer_accreditation_register_2026-10.csv",
    "certificates": "battery_installation_certificates_2025.csv",
    "amendments": "battery_installation_certificate_amendments_2025.csv",
}
