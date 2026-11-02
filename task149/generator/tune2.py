"""Tuning aid for the re-cut (never ships a figure): zone boardings under every estimator, arrival shares, station
ratios.  python3 tune2.py <scratch_target>"""
import sys
import analysis as A


def dist(x, step):
    q = x / step
    return abs((q - int(q)) - 0.5) * step


def main(tgt):
    R = A.run(tgt)
    V = R["variants"]
    print("golden %.1f  census %.1f  pooled %.1f  net %.1f  lsg %.1f" % (R["golden"], R["census_daily"], R["pooled_route"],
                                                                       R["network_route"], R["lisnagry_route"]))
    for z in sorted(R["boardings"]):
        if R["shares"].get(z, 0) <= 0:
            continue
        vals = [V[k]["rows"][z] for k in V if k != "with_midterm"] + [R["boardings"][z]]
        same = len({round(v / 10) for v in vals}) == 1
        print(z, "%.2f" % R["boardings"][z], "min %.2f max %.2f" % (min(vals), max(vals)),
              "edge %.2f" % min(dist(v, 10) for v in vals), "SAME" if same else "SPLIT", "f %.4f" % R["freq"][z])
    print({k: round(v["total"], 1) for k, v in V.items()})
    for nm in ("arrivals", "arrivals_long", "arrivals_exclusive", "arrivals_utc"):
        print(nm, {z: round(100 * R[nm][z], 2) for z in sorted(R[nm]) if R["shares"].get(z, 0) >= 0.10})
    print("st", {k: round(100 * v, 2) for k, v in R["station_ratios"].items()})


if __name__ == "__main__":
    main(sys.argv[1])
