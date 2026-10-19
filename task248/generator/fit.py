"""task248 decay fits on the paired study: the candidate forms an analyst may take, each giving k(T) per hour."""
import numpy as np


def _arrays(rows, temp="Tin"):
    t = np.array([r["tt"] for r in rows])
    T = np.array([r[temp] for r in rows])
    y = np.log(np.array([r["pl"] / r["up"] for r in rows]))       # ln of plant over upstream
    return t, T, y


def linear(rows, temp="Tin"):
    """ln ratio = -(a + b T) t, least squares"""
    t, T, y = _arrays(rows, temp)
    X = np.c_[t, t * T]
    a, b = np.linalg.lstsq(X, -y, rcond=None)[0]
    return lambda TT: a + b * np.asarray(TT)


def arrhenius(rows, temp="Tin"):
    """ln ratio = -k20 theta^(T-20) t, least squares over a fine grid then refined"""
    t, T, y = _arrays(rows, temp)
    best = None
    for th in np.linspace(1.0, 1.2, 401):
        g = t * th ** (T - 20)
        k20 = -np.sum(g * y) / np.sum(g * g)
        r = np.sum((y + k20 * g) ** 2)
        if best is None or r < best[0]:
            best = (r, k20, th)
    _, k20, th = best
    return lambda TT: k20 * th ** (np.asarray(TT) - 20)


def per_plant(rows, temp="Tin"):
    """each study plant's own ratio against temperature (ln ratio / t = -(a + b T)), averaged into one line"""
    out = []
    for s in sorted({r["site"] for r in rows}):
        rr = [r for r in rows if r["site"] == s]
        t, T, y = _arrays(rr, temp)
        A = np.c_[np.ones_like(T), T]
        a, b = np.linalg.lstsq(A, -y / t, rcond=None)[0]
        out.append((a, b))
    a, b = np.mean(out, axis=0)
    return lambda TT: a + b * np.asarray(TT)


def constant(rows, temp="Tin"):
    t, T, y = _arrays(rows, temp)
    k = -np.sum(t * y) / np.sum(t * t)
    return lambda TT: k + 0 * np.asarray(TT)


def additive(rows, temp="Tin"):
    """ln ratio = c0 + c1 t + c2 T: a temperature term beside travel time (the wrong shape); returns the correction
    function of (T, t) in ln units"""
    t, T, y = _arrays(rows, temp)
    X = np.c_[np.ones_like(t), t, T]
    c = np.linalg.lstsq(X, y, rcond=None)[0]
    return c
