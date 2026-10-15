"""The survey's estimators as its user guide sets them out: an estimate on each implicate with the household weight,
averaged; its sampling variance from the 200 replicate weights on implicate 1; its imputation variance from the five
implicates; the total at sampling plus (1 + 1/5) times imputation."""
from __future__ import annotations

import numpy as np

import common as K


def wmedian(x, w):
    """Weighted median of x under each row of weights w (2-D: one row per weighting): the first value, in ascending
    order, at which the cumulative weight reaches half the total."""
    w = np.atleast_2d(w)
    o = np.argsort(x, kind="stable")
    xs = x[o]
    c = np.cumsum(w[:, o], axis=1)
    return xs[(c >= c[:, -1:] / 2).argmax(1)]


class Survey:
    """The public-use arrays: net worth by implicate (5 x N), weight (N), replicate weights (200 x N)."""

    def __init__(self, nw, w, R):
        self.nw, self.w, self.R = np.asarray(nw, float), np.asarray(w, float), np.asarray(R, float)

    def median(self, mask):
        """The estimate per implicate (5), the replicate estimates on implicate 1 (200)."""
        est = np.array([wmedian(self.nw[m][mask], self.w[mask])[0] for m in range(K.IMPLICATES)])
        rep = wmedian(self.nw[0][mask], self.R[:, mask])
        return est, rep

    @staticmethod
    def combine(est, rep):
        """Point estimate, sampling variance, imputation variance, total variance, standard error."""
        u = float(((rep - est[0]) ** 2).mean())
        b = float(est.var(ddof=1))
        t = u + (1 + 1 / K.IMPLICATES) * b
        return float(est.mean()), u, b, t, float(np.sqrt(t))
