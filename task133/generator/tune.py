"""Sets params.PLAN_GRADE_ADJ (the plan's compartment yields by grade, applied in the planning step) so that, under every
convention analysis.Pack.conventions() computes, each grade's FY2028 loads sit inside one 100-load bin and the total inside
one 500-load bin, with the spread of the conventions centred in the bin. Measured on a written pack."""
import importlib
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def measure():
    import analysis as A
    import make_pack
    tmp = tempfile.mkdtemp()
    try:
        make_pack.make(tmp)
        conv = A.Pack(tmp).conventions()
    finally:
        shutil.rmtree(tmp)
    grades = list(next(iter(conv.values())))
    lo = {g: min(v[g] for v in conv.values()) for g in grades}
    hi = {g: max(v[g] for v in conv.values()) for g in grades}
    tl = min(sum(v.values()) for v in conv.values())
    th = max(sum(v.values()) for v in conv.values())
    return lo, hi, tl, th


def nearest(x, step):
    return round(x / step) * step


def write_adj(adj):
    src = open(os.path.join(HERE, "params.py")).read()
    a = src.index("PLAN_GRADE_ADJ = {")
    b = src.index("}", a) + 1
    src = src[:a] + "PLAN_GRADE_ADJ = {" + ", ".join(f'"{k}": {v}' for k, v in adj.items()) + "}" + src[b:]
    open(os.path.join(HERE, "params.py"), "w").write(src)


def main(rounds=8):
    import params as P
    target = None
    best = None
    for i in range(rounds):
        lo, hi, tl, th = measure()
        mid = {g: (lo[g] + hi[g]) / 2 for g in lo}
        tmid = (tl + th) / 2
        print("round", i, "total %.1f to %.1f" % (tl, th), {g: "%.1f-%.1f" % (lo[g], hi[g]) for g in lo})
        if target is not None:
            margin = min(min(lo[g] - target[g] + 50, target[g] + 50 - hi[g]) for g in lo)
            if best is None or margin > best[0]:
                best = (margin, dict(P.PLAN_GRADE_ADJ))
        if target is None:
            T = nearest(tmid, 500)
            target = {g: nearest(m, 100) for g, m in mid.items()}
            while sum(target.values()) != T:
                if sum(target.values()) < T:
                    g = max(target, key=lambda k: mid[k] - target[k])
                    target[g] += 100
                else:
                    g = min(target, key=lambda k: mid[k] - target[k])
                    target[g] -= 100
            print("targets", T, target)
            margin = min(min(lo[g] - target[g] + 50, target[g] + 50 - hi[g]) for g in lo)
            best = (margin, dict(P.PLAN_GRADE_ADJ))
        if all(abs(mid[g] - target[g]) < 3 for g in mid):
            break
        # move each grade by a share of its distance from the bin centre (the plan's 100-tonne cells quantise the step)
        new = {g: round(P.PLAN_GRADE_ADJ[g] * (1 + 0.7 * (target[g] / mid[g] - 1)), 5) for g in mid}
        write_adj(new)
        for m in ("params", "world", "pack", "docs", "make_pack", "analysis"):
            if m in sys.modules:
                importlib.reload(sys.modules[m])
        import params as P  # noqa: F811
    write_adj(best[1])
    print("kept", best[1], "tightest grade margin %.1f" % best[0])


if __name__ == "__main__":
    main()
