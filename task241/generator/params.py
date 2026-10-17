"""task241 constants: the Instituto Oceânico do Atlântico's Iberian Basin Float Array and its 2027 delayed-mode
salinity release."""
import datetime as dt

SEED = 241

INSTITUTE = "Instituto Oceânico do Atlântico"
ARRAY = "Iberian Basin Float Array"

YEAR = 2027
REF_FROZEN = dt.date(2027, 12, 15)
ASOF = dt.date(2028, 1, 7)
DUE = dt.date(2028, 1, 21)
EPOCH = dt.datetime(1950, 1, 1)                 # profile times are days since this, UTC

TOL = 0.010                                     # salinity offset (PSS-78) beyond which a float's salinity is adjusted
LAYER = (1400.0, 1900.0)                        # dbar

# the basin box
LON = (-20.0, -9.5)
LAT = (37.0, 43.0)
FLOAT_LON = (-19.3, -11.0)                      # the array's floats stay in the basin's recirculation
FLOAT_LAT = (37.6, 42.4)
LON0 = -14.5                                    # where the reference water's salinity on a temperature level is its basin mean

# the deep water's structure below the Mediterranean water
TH_DEEP, TH_AMP, TH_SCALE = 3.2, 8.0, 500.0     # theta(z) = TH_DEEP + TH_AMP exp(-(z - 1000) / TH_SCALE) below 1000 m
S_A, S_B = 0.100, 0.008                         # S(theta) = 35.00 + S_A (theta - 3.5) + S_B (theta - 3.5)^2
GAMMA = 0.0060                                  # salinity on a temperature level falls by this per degree west, at theta 6.8
H_2027 = 13.0                                   # metres: the 2027 layer sits this much deeper than the reference years' mean
EDDY_SD, EDDY_PHI = 30.0, 0.85                  # each float's eddy displacement, an AR(1) over its 10-day cycles

N_FLOATS = 24
