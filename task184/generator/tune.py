"""Set world.INF_TUNE: each infected house's infection size such that every graded figure (each infected farm's and
each of its houses' birds the infection killed, to the nearest ten) sits at least 2.5 birds (houses) and 3.5 birds
(farms) inside its bin under every member of the defensible family. Run once; the result is pasted into world.py."""
import datetime as dt
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B   # noqa: E402
import calc as C    # noqa: E402
import sim as S     # noqa: E402
import world as W   # noqa: E402


def edge(v, u=10.0):
    return u / 2 - abs(v - round(v / u) * u)


def main():
    tmp = tempfile.mkdtemp(prefix="t184tune_")
    B.build_pack(tmp)
    p = C.Pack(tmp)
    members = {m: C.family_member(p, m) for m in C.FAMILY}
    pack_hc = {(h["farm"], h["house"]): h for h in p.house_crops() if any(x[0] in C.WINDOW for x in h["days"])}
    infected = [code for code, d in W.DESIGN.items() if d.get("inf")]
    choice = {}
    grid = [round(0.80 + 0.01 * k, 2) for k in range(41)]
    for fc in infected:
        f = [x for x in S.build_world() if x.code == fc][0]
        crop = [c for c in f.crops if c.place == W.DESIGN[fc]["place"]][0]
        per_house = {}
        for hcode, hc in crop.houses.items():
            ph = pack_hc[(fc, hcode)]
            d0 = hc.infection[0]
            base_e0 = W.DESIGN[fc]["inf"][1]
            g = W.DESIGN[fc]["inf"][2]
            # sim truth alive at d0 and pack alive at d0 are both unchanged by the infection size
            sim_days = {x[0]: x for x in hc.days}
            pk_days = {x[0]: x for x in ph["days"]}
            opts = []
            for m in grid:
                alive_t = sim_days[d0][2]
                alive_p = pk_days[d0][2]
                days = []
                for x in hc.days:
                    if x[0] < d0:
                        continue
                    d, a, _, _, _, post = x
                    hz = W.course(a) * (W.THINNED_FACTOR if post else 1.0)
                    lam = alive_t * hz / 1000.0 + alive_t * base_e0 * m * (g ** (d - d0).days) / 1000.0
                    dr = S.R("day", fc, hcode, d.isoformat())
                    deaths = int(min(alive_t, dr.poisson(lam)))
                    culls = int(min(alive_t - deaths, dr.poisson(alive_t * W.cull_rate(a) / 1000.0)))
                    days.append((d, a, alive_p, deaths, culls, post))
                    alive_t -= deaths + culls
                    alive_p -= deaths + culls
                win = [x for x in days if x[0] in C.WINDOW]
                obs = sum(x[3] for x in win)
                vals = {mm: obs - C.expected(members[mm], fc, win) for mm in C.FAMILY}
                opts.append((m, vals))
            per_house[hcode] = opts
        # houses first: the multipliers keeping each house's figure 2.5 inside its bin under every member
        ok = {h: [(m, v) for (m, v) in opts if min(edge(x) for x in v.values()) >= 2.5
                  and len({round(x / 10) for x in v.values()}) == 1] for h, opts in per_house.items()}
        hs = sorted(ok)
        best = None
        import itertools
        pools = [sorted(ok[h], key=lambda mv: abs(mv[0] - 1.0))[:6] for h in hs]
        for combo in itertools.product(*pools):
            tot = {mm: sum(v[mm] for (_, v) in combo) for mm in C.FAMILY}
            if min(edge(x) for x in tot.values()) >= 3.5 and len({round(x / 10) for x in tot.values()}) == 1:
                score = sum(abs(m - 1.0) for (m, _) in combo)
                if best is None or score < best[0]:
                    best = (score, combo, tot)
        assert best is not None, fc
        for h, (m, v) in zip(hs, best[1]):
            choice[(fc, h)] = m
        print(fc, {h: m for h, (m, _) in zip(hs, best[1])}, {k: round(x, 1) for k, x in best[2].items()})
    print("INF_TUNE =", repr(choice))


if __name__ == "__main__":
    main()
