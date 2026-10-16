"""The late shift's arrival levels. The board's FY2028 forecast is built so the golden's compliance sits on its whole
per cent in every month (the design's targets); the history's Friday and Saturday late-shift levels are the same
forecast less the Halvorsen move, taken back to fiscal 2026 by the volume trend. forecast.py re-centres the board's
cells on the parameters the history actually yields."""
from __future__ import annotations

import datetime as dt

from scipy.optimize import brentq

import common as K
import model as M

TARGET_INT = {7: 88, 8: 89, 9: 91, 10: 93, 11: 94, 12: 93, 1: 94, 2: 95, 3: 94, 4: 93, 5: 91, 6: 89}
# where inside its whole per cent each month's golden sits (a forecast lands where it lands; every one at least
# 0.38 from a rounding edge and 0.9 from the standard)
OFFSET = {7: 0.07, 8: -0.09, 9: 0.11, 10: -0.04, 11: 0.06, 12: -0.12, 1: 0.02, 2: -0.06, 3: 0.09, 4: -0.10,
          5: 0.04, 6: -0.03}
TARGET = {m: TARGET_INT[m] + OFFSET[m] for m in TARGET_INT}
# the board's estimate of Halvorsen's calls per Friday and Saturday late-shift hour from July 2027
HALV_LATE = {7: 6.62, 8: 6.41, 9: 5.86, 10: 5.43, 11: 5.21, 12: 5.48, 1: 5.12, 2: 4.97, 3: 5.27, 4: 5.44, 5: 5.86,
             6: 6.31}


def cell_factor(dow, h):
    """Late-shift cell shape: the hour profile times the night factor (the night started the day before for 00:00
    and 01:00)."""
    night_dow = dow if h >= 22 else (dow - 1) % 7
    return K.HOUR_PROFILE[h] * K.NIGHT_FACTOR[night_dow]


def solve_level(y, m, target, mu, th):
    f = lambda L: M.month_compliance(y, m, lambda dow, h: L * cell_factor(dow, h), mu, th)[0] - target / 100.0
    return brentq(f, 5.0, 80.0, xtol=1e-10)


NOMINAL_MU = 3600.0 / K.AHT
NOMINAL_TH = 3600.0 / K.PATIENCE
FY28_LEVEL = {m: solve_level(y, m, TARGET[m], NOMINAL_MU, NOMINAL_TH) for y, m in K.fy_months(2028)}
LATE_LEVEL = {m: (FY28_LEVEL[m] - HALV_LATE[m]) / K.trend(dt.date(y, m, 15)) for y, m in K.fy_months(2028)}
