"""World constants for task138 architecture 3: Breckwater Electric Cooperative's Dunraith substation.

Everything the world draws from a seed sits here, so a rebuild from these numbers is the same pack byte for byte.
"""

WEATHER_SEED = 2138301      # the Mossford airport's summers
WEATHER_SEED_2026 = 2138527  # summer 2026 drawn on its own stream
LOAD_SEED = 2138302         # feeder load noise
MDMS_SEED = 2138303         # members' transformer meters
GT_SEED = 2138477           # the wholesale supplier's revenue meters
OTHER_SEED = 2138305        # distractors

AS_OF = "2026-10-27"        # the planning engineer's review for the 2027 construction work plan
SUMMERS = [2022, 2023, 2024, 2025, 2026]
UTC_OFFSET_H = -5           # local daylight time in summer (the SCADA historian's clock)

# eight 24.9 kV feeders: share of the substation's load and the air-conditioning weight of each
FEEDERS = ["DUN-1", "DUN-2", "DUN-3", "DUN-4", "DUN-5", "DUN-6", "DUN-7", "DUN-8"]
SHARE = [0.152, 0.121, 0.138, 0.108, 0.143, 0.093, 0.126, 0.119]
AC_WEIGHT = [1.02, 0.99, 0.97, 1.03, 1.01, 0.98, 1.00, 1.00]

# load model (MW at the 2024 load level, whole substation): load that does not depend on weather follows the
# hour-of-day profile below; air conditioning at full duty adds AC_FULL; duty rises linearly from DUTY_T0 to
# DUTY_T1 (deg F, the temperature the buildings feel, a lagged mix of the last hours), steepening as it rises
OTHER_PEAK = 22.617
AC_FULL = 88.396
DUTY_T0, DUTY_T1 = 70.0, 102.0
DUTY_EXP = 1.5
LAG_A, LAG_B = 2, 4         # hours: the buildings feel a mix of the air temperature two and four hours earlier
DESIGN_LAG_DROP = 0.4       # deg F below the day's maximum at the evening peak (for the truth only)
PEAK_HOUR = 19
# members' meters see each feeder's energy less its line and transformer losses (long rural feeders lose more)
METER_FACTOR = [0.9781, 0.9752, 0.9726, 0.9684, 0.9711, 0.9772, 0.9667, 0.9738]
GROWTH = 0.0095             # a year, the 2025 load forecast's rate for Dunraith
LOAD_NOISE = 0.003

# conservation voltage reduction: the 2025 pilot cut the voltage 3.5 per cent on three feeders, week on, week off;
# the load falls by CVR_OTHER per cent of voltage on the voltage-sensitive load and CVR_AC on air conditioning
CVR_DV = 0.035
CVR_OTHER = 1.20
CVR_AC = 0.05
PILOT_FEEDERS = ["DUN-2", "DUN-5", "DUN-7"]
PILOT_START = "2025-06-02"  # a Monday; on weeks alternate from here to the end of September
PILOT_END = "2025-09-29"

DESIGN_TEMP_F = 101.0
FIRM_RATING_MW = 104.0
BLOCK_MW = 0.5
PLAN_YEARS = [2027, 2028, 2029, 2030, 2031]
