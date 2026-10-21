"""Harmonic tide prediction: astronomical arguments and nodal factors after Schureman, the method harbour tide tables use."""
import numpy as np

D2R = np.pi / 180.0

# Doodson multipliers (tau, s, h, p, N', p1) and phase offset (deg)
CONST = {
    'Sa':  ((0, 0, 1, 0, 0, 0), 0),
    'Ssa': ((0, 0, 2, 0, 0, 0), 0),
    'Q1':  ((1, -2, 0, 1, 0, 0), -90),
    'O1':  ((1, -1, 0, 0, 0, 0), -90),
    'P1':  ((1, 1, -2, 0, 0, 0), -90),
    'K1':  ((1, 1, 0, 0, 0, 0), 90),
    '2N2': ((2, -2, 0, 2, 0, 0), 0),
    'mu2': ((2, -2, 2, 0, 0, 0), 0),
    'N2':  ((2, -1, 0, 1, 0, 0), 0),
    'nu2': ((2, -1, 2, -1, 0, 0), 0),
    'M2':  ((2, 0, 0, 0, 0, 0), 0),
    'L2':  ((2, 1, 0, -1, 0, 0), 180),
    'T2':  ((2, 2, -3, 0, 0, 1), 0),
    'S2':  ((2, 2, -2, 0, 0, 0), 0),
    'K2':  ((2, 2, 0, 0, 0, 0), 0),
    'M4':  ((4, 0, 0, 0, 0, 0), 0),
    'MS4': ((4, 2, -2, 0, 0, 0), 0),
    'MN4': ((4, -1, 0, 1, 0, 0), 0),
    'M6':  ((6, 0, 0, 0, 0, 0), 0),
}


def astro(t_hours_since_j2000):
    """Mean longitudes (deg) at times given in hours since 2000-01-01 12:00 UT."""
    T = t_hours_since_j2000 / (24.0 * 36525.0)
    s = 218.3164 + 481267.8812 * T
    h = 280.4661 + 36000.7698 * T
    p = 83.3535 + 4069.0137 * T
    N = 125.0445 - 1934.1363 * T
    p1 = 282.9384 + 1.7195 * T
    # lunar time tau = 15 * UT hour + h - s ; UT hour from t
    ut = (t_hours_since_j2000 + 12.0) % 24.0
    tau = 15.0 * ut + h - s
    return tau, s, h, p, N, p1


def nodal(N, p):
    """Return dict of (f, u_deg) for each constituent given node N and perigee p (deg)."""
    n = N * D2R
    out = {}
    fM2 = 1.0004 - 0.0373 * np.cos(n) + 0.0002 * np.cos(2 * n)
    uM2 = -2.14 * np.sin(n)
    fK1 = 1.0060 + 0.1150 * np.cos(n) - 0.0088 * np.cos(2 * n) + 0.0006 * np.cos(3 * n)
    uK1 = -8.86 * np.sin(n) + 0.68 * np.sin(2 * n) - 0.07 * np.sin(3 * n)
    fO1 = 1.0089 + 0.1871 * np.cos(n) - 0.0147 * np.cos(2 * n) + 0.0014 * np.cos(3 * n)
    uO1 = 10.80 * np.sin(n) - 1.34 * np.sin(2 * n) + 0.19 * np.sin(3 * n)
    fK2 = 1.0241 + 0.2863 * np.cos(n) + 0.0083 * np.cos(2 * n) - 0.0015 * np.cos(3 * n)
    uK2 = -17.74 * np.sin(n) + 0.68 * np.sin(2 * n) - 0.04 * np.sin(3 * n)
    # L2 (Schureman approx with P = p)
    P = p * D2R
    a = 1 - 0.2505 * np.cos(2 * P) - 0.1102 * np.cos(2 * P - n) - 0.0156 * np.cos(2 * P - 2 * n) - 0.037 * np.cos(n)
    b = -0.2505 * np.sin(2 * P) - 0.1102 * np.sin(2 * P - n) - 0.0156 * np.sin(2 * P - 2 * n) - 0.037 * np.sin(n)
    fL2 = np.sqrt(a * a + b * b)
    uL2 = np.arctan2(b, a) / D2R
    one = np.ones_like(n)
    zero = np.zeros_like(n)
    out['Sa'] = (one, zero)
    out['Ssa'] = (one, zero)
    out['Q1'] = (fO1, uO1)
    out['O1'] = (fO1, uO1)
    out['P1'] = (one, zero)
    out['K1'] = (fK1, uK1)
    out['2N2'] = (fM2, uM2)
    out['mu2'] = (fM2, uM2)
    out['N2'] = (fM2, uM2)
    out['nu2'] = (fM2, uM2)
    out['M2'] = (fM2, uM2)
    out['L2'] = (fL2, uL2)
    out['T2'] = (one, zero)
    out['S2'] = (one, zero)
    out['K2'] = (fK2, uK2)
    out['M4'] = (fM2 ** 2, 2 * uM2)
    out['MS4'] = (fM2, uM2)
    out['MN4'] = (fM2 ** 2, 2 * uM2)
    out['M6'] = (fM2 ** 3, 3 * uM2)
    return out


def predict(t_hours, consts, z0=0.0):
    """consts: dict name -> (amplitude m, phase lag deg, Greenwich). Returns levels (m).
    Nodal factors evaluated at each time (fine for multi-year spans)."""
    tau, s, h, p, N, p1 = astro(t_hours)
    nf = nodal(N, p)
    lvl = np.full_like(t_hours, z0, dtype=float)
    for name, (A, G) in consts.items():
        d, off = CONST[name]
        V = d[0] * tau + d[1] * s + d[2] * h + d[3] * p + d[4] * (-N) + d[5] * p1 + off
        f, u = nf[name]
        lvl += f * A * np.cos((V + u - G) * D2R)
    return lvl
