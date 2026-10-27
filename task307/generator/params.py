"""Fixed inputs of the Merrimont world (task307)."""
SEED = 30727
# the subarea network's lane counts (2028 no-build)
LANES = dict(millbrook_lanes=2, r9_bridge_lanes=3, ferry_lanes=2, center_lanes=1, center_dt_lanes=2)
# macro-zone shares of the west bank's AM trips, demand scale and the downtown share
W_SHARE = {"W1": 0.09, "W2": 0.08, "W3": 0.20, "W4": 0.09, "W5": 0.25, "W6": 0.35}
SCALE = 1.13
DT_SHARE = 0.51
PM_FACTOR = 0.92
COUNTER = 0.30          # counter-peak trips relative to the peak direction
LOCAL = {("W3", "W4"): 220, ("W1", "W2"): 180, ("Z_P", "Z_E"): 240, ("Z_DT2", "Z_E"): 180}
# subzones: macro zone -> zone numbers (gaps are retired zones)
SUBZONES = {"W1": [101, 102, 103, 104], "W2": [105, 106, 107, 108], "W3": [109, 110, 111, 113, 114],
            "W4": [115, 116, 117], "W5": [118, 119, 120, 121, 122, 123], "W6": [124, 125, 126, 127, 128, 130],
            "Z_DT1": [201, 202, 203, 204, 205, 206], "Z_DT2": [207, 208, 209, 210],
            "Z_E": [301, 302, 303, 304, 305, 306], "Z_P": [401, 402, 403]}
# TIP candidates: what each changes in the subarea network, and its cost (USD millions, year-of-expenditure)
PROJECTS = [
    dict(code="A", tip_id="TIP-28-014", name="Route 9 Millbrook auxiliary lane", cost_m=46.8,
         change="lanes", street="Route 9", segment="Millbrook", new_lanes=3),
    dict(code="B", tip_id="TIP-28-021", name="Ferry Street exit ramp widening", cost_m=17.7,
         change="lanes", street="Ferry Street exit", new_lanes=3),
    dict(code="C", tip_id="TIP-28-009", name="Center Street Bridge widening", cost_m=38.9,
         change="lanes", street="Center Street Bridge", new_lanes=2),
    dict(code="D", tip_id="TIP-28-030", name="Southport corridor signal and turn-lane package", cost_m=25.7,
         change="lane_capacity", streets=["Southport Bridge", "Southport Avenue"], new_lane_cap=980),
]
WEEKDAYS = 247
PEAK_EXPANSION = 2.9      # peak hour to peak period, TIP scoring guidance
ANNUAL_FACTOR = WEEKDAYS * PEAK_EXPANSION
UE_GAP = 1e-6

ORG = "Merrimont Area Metropolitan Planning Organization"
FILES = {
    "links": "MAMPO_v42_subarea_links_2028NB.csv",
    "nodes": "MAMPO_v42_subarea_nodes.csv",
    "trips": "MAMPO_v42_subarea_trips_2028.csv",
    "loaded": "MAMPO_v42_loaded_network_2028NB.csv",
    "modeldoc": "MAMPO_TDM_v4.2_documentation_ch4-6.pdf",
    "tip": "FY2028_TIP_congestion_relief_candidates.xlsx",
    "guidance": "MAMPO_TIP_project_scoring_guidance_2026.pdf",
    "atr": "ATR_hourly_volumes_2025.csv",
    "stations": "ATR_station_inventory_2025.xlsx",
    "countman": "MAMPO_traffic_count_program_manual_2024.pdf",
    "valid": "MAMPO_v42_base2025_station_volumes.csv",
    "probe": "probe_segment_travel_times_2025.parquet",
    "segs": "CMP_probe_segment_reference.csv",
    "cmp": "MAMPO_CMP_reliability_measures_2026.pdf",
    "crash": "crash_summary_by_segment_2021_2025.xlsx",
    "transit": "MRTA_route_ridership_FY2025.csv",
}
# node numbers in the subarea extract
NODE_ID = {"F1": 5001, "F2": 5002, "F3": 5003, "F4": 5004, "BN": 5005, "FX": 5006, "EF": 5007,
           "A1": 4101, "A2": 4102, "A3": 4103, "A4": 4104, "C1": 4201, "C2": 4202, "C3": 4203, "C4": 4204,
           "DT1": 4301, "DT2": 4302}
NODE_XY = {"F1": (1191400, 402300), "F2": (1191900, 410700), "F3": (1192600, 420700), "F4": (1193100, 428100),
           "BN": (1197900, 429300), "FX": (1199800, 429500), "EF": (1211300, 431000),
           "A1": (1186900, 401800), "A2": (1187300, 410100), "A3": (1187800, 419600), "A4": (1188200, 427600),
           "C1": (1201100, 401500), "C2": (1201600, 408400), "C3": (1202000, 415200), "C4": (1203300, 422100),
           "DT1": (1201900, 427300), "DT2": (1203600, 424800)}
FTYPE = {"freeway": 1, "freeway_lanedrop": 12, "bridge": 2, "ramp": 3, "arterial": 4, "collector": 5, "connector": 9}
HV_SHARE = {1: 0.11, 12: 0.11, 2: 0.10, 3: 0.07, 4: 0.05, 5: 0.03, 9: 0.0}   # base-year model heavy-vehicle shares
BASE_GROWTH = 0.935     # 2025 base trip tables relative to 2028
AS_OF = "2026-10-23"
PEOPLE = {"lead": "Krystal Cooke", "director": "Charles Cummings"}
PRODUCER = "MAMPO"
