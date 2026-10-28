"""task270 calibration on the simulation's own minute arrays (fast; the shipped-file golden is calc.py's): every rung
of the ladder by district, and the on-call availability profile.

    python3 tune.py [key=value ...]     KEYSH_<district>=, REMSH_<district>=, CREW_<key>=, OPS_<key>="""
from __future__ import annotations

import copy
import sys
import time

import numpy as np
from scipy.spatial import cKDTree

import common as K
import ops as O
import world as W


def dials_from(argv):
    dials = copy.deepcopy(W.DIALS)
    for a in argv:
        k, v = a.split("=")
        if k.startswith("KEYSH_") or k.startswith("REMSH_"):
            dials[k[:5]][k[6:]] = float(v)
        elif k.startswith("CREW_"):
            O.CREW[k[5:]] = type(O.CREW[k[5:]])(float(v)) if not isinstance(O.CREW[k[5:]], tuple) else \
                tuple(float(x) for x in v.split(","))
        elif k.startswith("OPS_"):
            O.OPS[k[4:]] = type(O.OPS[k[4:]])(float(v))
        elif k == "SAT_R":
            dials["SAT_R"] = float(v)
    return dials


def homes_matrix(Wd):
    res = Wd.akind == "R"
    an = Wd.anode[res]
    ad = Wd.adist[res]
    dnodes = np.unique(an)
    didx = np.full(Wd.N, -1); didx[dnodes] = np.arange(len(dnodes))
    HD = np.zeros((len(dnodes), len(K.DISTRICTS)))
    np.add.at(HD, (didx[an], ad), 1.0)
    return dnodes, HD


def cover(Wd, freem, posm, dnodes, HD, turn_s=None):
    turn_s = Wd.turn_s if turn_s is None else turn_s
    R = {}
    for ts in np.unique(turn_s):
        R[ts] = (Wd.D[:, dnodes] + ts) <= K.STANDARD_MIN * 60.0
    S = np.where(freem, posm, -1).astype(np.int32)
    u, cnt = np.unique(S, axis=0, return_counts=True)
    out = np.zeros(len(K.DISTRICTS))
    for s0 in range(0, len(u), 2000):
        blk = u[s0:s0 + 2000]
        cov = np.zeros((len(blk), len(dnodes)), bool)
        for e in range(Wd.nE):
            p = blk[:, e]; m = p >= 0
            if m.any():
                cov[m] |= R[turn_s[e]][p[m]]
        out += (cnt[s0:s0 + 2000, None] * (cov.astype(np.float32) @ HD)).sum(0)
    return out / K.MINUTES / HD.sum(0) * 100


def rungs(Wd, free, pos):
    dnodes, HD = homes_matrix(Wd)
    M = K.MINUTES
    homeM = np.broadcast_to(Wd.home, (M, Wd.nE))
    snodes = np.unique([s["node"] for s in Wd.stations])
    at_home = pos == homeM
    at_station = np.isin(pos, snodes)
    res = {}
    res["R0 static"] = cover(Wd, np.ones_like(free), homeM, dnodes, HD)
    a = free.mean(0)
    r1 = []
    for d in range(len(K.DISTRICTS)):
        m = HD[:, d] > 0
        pc = np.ones(m.sum())
        for e in range(Wd.nE):
            reach = (Wd.D[Wd.home[e], dnodes[m]] + Wd.turn_s[e]) <= 600.0
            pc *= np.where(reach, 1 - a[e], 1.0)
        r1.append(((1 - pc) * HD[m, d]).sum() / HD[:, d].sum() * 100)
    res["R1 independent"] = np.array(r1)
    res["R2 station replay"] = cover(Wd, free, homeM, dnodes, HD)
    res["R2b zero when away"] = cover(Wd, free & at_home, homeM, dnodes, HD)
    res["P1 standby credited"] = cover(Wd, free, np.where(at_station, pos, homeM), dnodes, HD)
    res["P3 stations only"] = cover(Wd, free & at_station, pos, dnodes, HD)
    t = cKDTree(Wd.nodes[snodes])
    snap = snodes[t.query(Wd.nodes[pos.ravel()])[1]].reshape(pos.shape)
    res["P4 nearest station"] = cover(Wd, free, snap, dnodes, HD)
    res["R3 positions"] = cover(Wd, free, pos, dnodes, HD)
    return res


def main(argv):
    t0 = time.time()
    dials = dials_from(argv)
    Wd = W.build(dials)
    sim = O.simulate(Wd)
    free, pos, kind = O.minute_arrays(Wd, sim)
    res = rungs(Wd, free, pos)
    print("%-22s" % "district", " ".join("%6s" % d[:6] for d in K.DISTRICTS))
    for k, v in res.items():
        print("%-22s" % k, " ".join("%6.2f" % x for x in v), " below:",
              ",".join(K.DISTRICTS[i][:4] for i in np.where(v < K.LINE)[0]))
    wt = np.where(Wd.ewt)[0]
    oc = np.where(~Wd.ewt)[0]
    rural = [e for e in oc if Wd.stations[Wd.engines[e]["station"]]["district"] in K.RURAL]
    hod = (np.arange(K.MINUTES) % 1440) / 60.0
    day = np.arange(K.MINUTES) // 1440
    wk = np.array([O.weekday_doy(d) for d in range(365)])[day] & (hod >= 7) & (hod < 19)
    print("away (wholetime minutes): training %.2f visits %.2f standby %.2f incident %.2f returning %.2f" %
          tuple(100 * (kind[:, wt] == k).mean() for k in (1, 2, 3, 4, 5)))
    print("free: wholetime %.3f on-call %.3f; rural on-call weekday day %.3f other %.3f; town on-call day %.3f  %.0fs" %
          (free[:, wt].mean(), free[:, oc].mean(), free[wk][:, rural].mean(), free[~wk][:, rural].mean(),
           free[wk][:, [e for e in oc if e not in rural]].mean(), time.time() - t0))


if __name__ == "__main__":
    main(sys.argv[1:])
