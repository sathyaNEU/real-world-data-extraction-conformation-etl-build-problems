"""The EOS-80 relations the generator writes the record with: potential temperature (Bryden 1973, Fofonoff and Millard
1983), its inverse, and depth from pressure (Saunders 1981)."""
import numpy as np


def _atg(s, t, p):
    """adiabatic lapse rate, deg C per dbar"""
    ds = s - 35.0
    return (((-2.1687e-16 * t + 1.8676e-14) * t - 4.6206e-13) * p
            + ((2.7759e-12 * t - 1.1351e-10) * ds + ((-5.4481e-14 * t + 8.733e-12) * t - 6.7795e-10) * t
               + 1.8741e-8)) * p + (-4.2393e-8 * t + 1.8932e-6) * ds + ((6.6228e-10 * t - 6.836e-8) * t
                                                                          + 8.5258e-6) * t + 3.5803e-5


def ptmp(s, t, p, pr=0.0):
    """potential temperature (ITS-90 in and out) referred to pr dbar, by the Runge-Kutta step"""
    s, t, p = np.asarray(s, float), np.asarray(t, float) * 1.00024, np.asarray(p, float)
    h = pr - p
    xk = h * _atg(s, t, p)
    t = t + 0.5 * xk
    q = xk
    p = p + 0.5 * h
    xk = h * _atg(s, t, p)
    t = t + 0.29289322 * (xk - q)
    q = 0.58578644 * xk + 0.121320344 * q
    xk = h * _atg(s, t, p)
    t = t + 1.707106781 * (xk - q)
    q = 3.414213562 * xk - 4.121320344 * q
    p = p + 0.5 * h
    xk = h * _atg(s, t, p)
    t = t + (xk - 2.0 * q) / 6.0
    return t / 1.00024


def in_situ(theta, s, p):
    """in-situ temperature (ITS-90) of water of potential temperature theta and salinity s at pressure p"""
    theta, s, p = np.asarray(theta, float), np.asarray(s, float), np.asarray(p, float)
    t = theta + p * 1.0e-4
    for _ in range(4):
        t = t + (theta - ptmp(s, t, p))
    return t


def depth_from_pres(p, lat):
    """depth (m) from pressure (dbar), Saunders (1981)"""
    c1 = 5.92e-3 + np.sin(np.radians(lat)) ** 2 * 5.25e-3
    return (1 - c1) * np.asarray(p, float) - 2.21e-6 * np.asarray(p, float) ** 2


def pres_from_depth(z, lat):
    """pressure (dbar) from depth (m), Saunders (1981)"""
    c1 = 5.92e-3 + np.sin(np.radians(lat)) ** 2 * 5.25e-3
    return ((1 - c1) - np.sqrt((1 - c1) ** 2 - 8.84e-6 * np.asarray(z, float))) / 4.42e-6
