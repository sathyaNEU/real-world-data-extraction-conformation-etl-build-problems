"""task165 architecture 2: the world's constants. Quessling Sewer Authority (fictional), Pennsylvania; every
quantity in million gallons (MG), million gallons a day (MGD), inches and feet unless named otherwise."""
import datetime as dt

SEED = 16502
STORM_SCALE = 0.51
UTC = dt.timezone.utc
EST = dt.timezone(dt.timedelta(hours=-5))

# The record the consent decree evaluates: 1 January 2014 to 31 December 2025, Eastern time.
START_UTC = dt.datetime(2014, 1, 1, 5, 0, tzinfo=UTC)          # 00:00 EST
END_UTC = dt.datetime(2026, 1, 1, 5, 0, tzinfo=UTC)
STEP_MIN = 15
YEARS = 12
PULL = dt.datetime(2026, 1, 16, 9, 40)                           # local (EST) time of the data pull

# The Outfall 014 (Clay Street) catchment.
O14_DWF = 4.6           # MGD, dry weather flow, mean
O14_REG = 26.0          # MGD, the regulator's diversion to the Southside interceptor
O14_RUNOFF = 17.0       # MG of combined flow per inch of rain over the combined area
# The Outfall 006 (Northside tank) catchment.
O06_DWF = 2.1
O06_REG = 7.5
O06_RUNOFF = 9.9

# Southside and Northside water reclamation plants (hourly influent).
SS_CAP = 140.0          # MGD, Southside headworks hydraulic limit
SS_BASE = 73.0
SS_FAST = 150.0         # MGD of fast inflow per inch an hour of rain
SS_RDII = 88.0          # MGD per inch of groundwater store at the full spring factor
SS_HALF_LIFE_H = 60.0   # hours, the groundwater store's half life
NS_CAP = 125.0
NS_BASE = 41.0
NS_FAST = 60.0
NS_RDII = 9.0

# The Clay Street alternatives in TM-7: (label, volume MG, dewatering pump station firm capacity MGD, cost USD M).
ALTERNATIVES = [("A", 19.0, 23.0, 78.6), ("B", 26.0, 31.0, 96.0), ("C", 38.0, 45.0, 128.5), ("D", 50.0, 60.0, 158.9)]
LIMIT_EVENTS = 4.0
EVENT_GAP_H = 24.0

# The Northside tank (Outfall 006), in service 1 May 2020.
NT_START_LOCAL = dt.datetime(2020, 5, 1, 0, 0)
NT_VOL = 8.0            # MG at the overflow crest, 22.0 ft
NT_CREST_FT = 22.0
NT_HOPPER_FT = 3.0      # the sloped floor's depth
NT_HOPPER_MG = 0.42     # MG held below 3.0 ft
NT_NAMEPLATE = 4.0      # MGD per pump
NT_CURVE = {1: 4.0, 2: 7.4, 3: 10.2}          # the station's tested curve with original pumps (O&M manual)
NT_P2_OUT_LOCAL = dt.datetime(2023, 3, 6, 9, 30)
NT_P2_REBUILT_LOCAL = dt.datetime(2023, 3, 14, 13, 0)
NT_CLEANOUT_LOCAL = (dt.datetime(2023, 8, 14, 7, 0), dt.datetime(2023, 8, 23, 11, 0))
NT_CURVE_P2 = {("P2",): 3.3, ("P1", "P2"): 6.9, ("P2", "P3"): 6.9, ("P1", "P2", "P3"): 9.6}
NT_HOLD_MGD = 1.0        # the station is held off while storm flow enters the tank (O&M 4.3)
NT_START_FT = 1.0        # the lead pump starts at 1.0 ft when the station is idle
# SG-600's seals failing: (from, to, MGD of dry weather flow passing into the tank), local times
NT_LEAKS = [(dt.datetime(2022, 6, 20, 8, 0), dt.datetime(2023, 2, 14, 11, 0), 0.27),
            (dt.datetime(2023, 9, 5, 8, 0), dt.datetime(2024, 1, 30, 14, 0), 0.31),
            (dt.datetime(2024, 7, 15, 8, 0), dt.datetime(2025, 3, 18, 10, 0), 0.29),
            (dt.datetime(2025, 8, 4, 8, 0), dt.datetime(2025, 12, 31, 23, 45), 0.36)]
NT_TRANSDUCER_LOCAL =dt.datetime(2023, 8, 23, 11, 0)
NT_TRANSDUCER_OFFSET = 0.45   # ft the re-mounted transducer reads above the water's depth

# Rain gauges: id, site, logger replaced (local date) to a cellular logger that stamps UTC, or None.
GAUGES = [("RG-1", "Northside WRP", None), ("RG-2", "Clay Street pump station", None),
          ("RG-3", "Southside WRP", dt.datetime(2024, 5, 7, 11, 20)),
          ("RG-4", "Midtown public works yard", dt.datetime(2024, 5, 8, 9, 50))]
TIP_IN = 0.01
TIP_02MM_IN = 0.2 / 25.4
CONTRACT_START = dt.date(2025, 7, 1)    # the field maintenance contract's monthly visits begin
MECH_SWAPS = {"RG-1": dt.datetime(2025, 7, 8, 10, 5), "RG-2": dt.datetime(2025, 7, 9, 13, 40),
              "RG-3": dt.datetime(2025, 7, 15, 9, 15), "RG-4": dt.datetime(2025, 7, 22, 11, 30)}
ORIFICE_IN = 8.0

# The Outfall 014 meter replacement.
METER_OLD_END_LOCAL = dt.datetime(2019, 6, 9, 14, 0)       # the old logger's last reading (EST)
METER_NEW_START_LOCAL = dt.datetime(2019, 6, 2, 10, 0)      # the new logger's first reading (local)
CFS_TO_MGD = 0.646317
