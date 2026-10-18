"""task246 tuning, run by hand, never by make.py: the searches that fixed the generator's keys and the zones' means.

    python3 task246/generator/tune.py shifts      a trial shift of every zone's mean from -0.25 to +0.25 mm; for each
                                                  zone, the shift that keeps its readings' figure on one printed value
                                                  under either divisor and its published figure clear of a band edge
    python3 task246/generator/tune.py keys A B    the death-place and mover keys from A to B: the pairs under which the
                                                  household form's version 4 codes, read on every row, move every
                                                  zone's response and death rates, and the lazier paths keep least
"""
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import estim as E
import params as P
import solve


def _edge(v, u=0.1):
    return u / 2 - abs(v - round(v / u) * u)


def _band(x):
    return sum(round(x, 1) >= lo for lo, _n in P.BANDS[1:])


def shifts(lo=-25, hi=25):
    tmp = tempfile.mkdtemp()
    res = {}
    try:
        for i in range(lo, hi + 1):
            d = i / 100.0
            P.ZONE_SHIFT = {z: d for z in P.ZCODES}
            shutil.rmtree(tmp, ignore_errors=True)
            B.run(tmp)
            A = solve.answer(tmp, B.FILES)
            ZF, df = A["ZF"], A["df"]
            for z in P.ZCODES:
                dd = df[df.zone == z]
                x = dd[~dd.oedema].muac.values
                f1 = ZF[z]["readings"]
                f0 = E.figure(x.mean(), x.var(ddof=0), len(x), int(dd.oedema.sum()))
                pts = [E.points(ZF[z], k) for k in E.VARIANTS]
                res.setdefault(z, []).append((d, f1, f0, A["lo"][z], A["hi"][z], min(pts, key=abs), max(pts, key=abs)))
    finally:
        P.ZONE_SHIFT = {}
        shutil.rmtree(tmp, ignore_errors=True)
    gold = {"NP", "NL", "CP", "LT", "EP", "WP", "WR"}
    best = {}
    for z, rows in res.items():
        cands = []
        for d, f1, f0, lo_, hi_, pmin, pmax in rows:
            if round(f1, 1) != round(f0, 1):
                continue
            if z in gold:
                okb = _band(lo_) == _band(hi_) and min(abs(pmin), abs(pmax)) >= 2.4
                pub = lo_
            else:
                okb = max(abs(pmin), abs(pmax)) <= 1.6
                pub = f1
            clear_band = min(abs(round(pub, 1) - e) for e in (5.0, 10.0, 15.0)) >= 0.2
            if okb:
                cands.append((min(_edge(f1), _edge(f0), 0.03), clear_band, -abs(d), d))
        cands.sort(reverse=True)
        best[z] = cands[0][3]
        print(z, "shift %+.2f, clearance %.3f, band clear %s" % (cands[0][3], cands[0][0], cands[0][1]))
    print(best)
    return best


def keys(a, b, mover=21):
    tmp = tempfile.mkdtemp()
    try:
        for away in range(a, b):
            P.AWAY_SALT, P.MOVER_SALT = away, mover
            shutil.rmtree(tmp, ignore_errors=True)
            B.run(tmp)
            F = B.FILES
            gr, gm = solve.response(tmp, F), solve.mortality(tmp, F)
            v4r = solve.response(tmp, F, codes="v4")
            paths = {"cracker": solve.mortality(tmp, F, codes="v4"),
                     "status": solve.mortality(tmp, F, codes="v4", away=False),
                     "nobirths": solve.mortality(tmp, F, codes="v4", births_module=False)}
            hits = {k: sum(round(m[z][i], 2) == round(gm[z][i], 2) for z in P.ZCODES for i in (0, 1))
                    for k, m in paths.items()}
            rh = sum(round(v4r[z], 1) == round(gr[z], 1) for z in P.ZCODES)
            print(away, mover, "response kept", rh, hits, flush=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    if sys.argv[1] == "shifts":
        shifts()
    else:
        keys(int(sys.argv[2]), int(sys.argv[3]))
