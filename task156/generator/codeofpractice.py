"""The figures the council's Code of Practice for Land Development and Subdivision (Wastewater, July 2022) files: the
design occupancy, the design flow a person, and the diurnal table a new connection's flow follows. docs.py prints them;
the golden and the generator read them from here so the document and the arithmetic cannot drift."""
import numpy as np

OCCUPANCY = 2.7             # persons a dwelling
LPD = 200.0                 # litres a person a day, average dry weather
PDWF_FACTOR = 2.5           # peak dry weather factor (shown in the code; the replay uses the hourly table)
# hourly factors on the average dry weather flow, hour beginning, local time (Table 5.2)
TABLE_5_2 = [0.45, 0.38, 0.34, 0.33, 0.37, 0.52, 0.98, 1.55, 1.80, 1.62, 1.38, 1.20,
             1.10, 1.03, 0.97, 0.95, 1.00, 1.10, 1.26, 1.36, 1.27, 1.05, 0.82, 0.57]


def profile_factors():
    t = np.array(TABLE_5_2, dtype=float)
    return t / t.mean()
