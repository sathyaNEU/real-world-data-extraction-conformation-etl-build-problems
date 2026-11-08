"""task482: Rasch estimation on a persons-by-items matrix. R holds the summed scores of a cell's responses and M
their count (0 where the candidate never met the item), so R is zero wherever M is."""
import numpy as np

CLIP = 4.5


def sig(x):
    return 1.0 / (1.0 + np.exp(-x))


def fit_theta(R, M, b, it=30, wle=False):
    """Maximum likelihood (or Warm's weighted likelihood) person estimates with item difficulties fixed."""
    th = np.zeros(R.shape[0])
    for _ in range(it):
        p = sig(th[:, None] - b[None, :])
        q = p * (1 - p) * M
        g = (R - p * M).sum(1)
        info = q.sum(1)
        if wle:
            g = g + (q * (1 - 2 * p)).sum(1) / np.maximum(2 * info, 1e-9)
        th = np.clip(th + g / np.maximum(info, 1e-9), -CLIP, CLIP)
    return th


def fit_b(R, M, th, it=30, b0=None):
    """Maximum likelihood item difficulties with person estimates fixed; items with no responses stay NaN."""
    b = np.zeros(R.shape[1]) if b0 is None else np.nan_to_num(b0.copy())
    n = M.sum(0)
    for _ in range(it):
        p = sig(th[:, None] - b[None, :])
        g = (p * M - R).sum(0)
        info = (p * (1 - p) * M).sum(0)
        b = np.clip(b + g / np.maximum(info, 1e-9), -CLIP, CLIP)
    b[n == 0] = np.nan
    return b


def calibrate(R, M, fixed, it=40):
    """Joint calibration holding the items in `fixed` ({index: value}) at their values; returns (theta, b)."""
    I = R.shape[1]
    idx = np.array(sorted(fixed))
    vals = np.array([fixed[i] for i in idx])
    b = np.zeros(I)
    b[idx] = vals
    free = np.setdiff1d(np.arange(I), idx)
    th = np.zeros(R.shape[0])
    for _ in range(it):
        th = fit_theta(R, M, b, it=4)
        bf = fit_b(R[:, free], M[:, free], th, it=4, b0=b[free])
        b[free] = bf
        b[idx] = vals
    th = fit_theta(R, M, b, it=20)
    return th, b


def expected_mark(b_items, theta):
    return float(sig(theta - np.asarray(b_items)).sum())


def fit_stats(R, M, th, b):
    p = sig(th[:, None] - b[None, :])
    v = p * (1 - p)
    z2 = (R - p) ** 2
    n = M.sum(0)
    outfit = (z2 / np.maximum(v, 1e-9) * M).sum(0) / np.maximum(n, 1)
    infit = (z2 * M).sum(0) / np.maximum((v * M).sum(0), 1e-9)
    return infit, outfit
