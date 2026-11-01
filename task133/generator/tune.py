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


def main(rounds=6):
    import params as P
    target = None
    for i in range(rounds):
        lo, hi, tl, th = measure()
        mid = {g: (lo[g] + hi[g]) / 2 for g in lo}
        tmid = (tl + th) / 2
        print("round", i, "total %.1f to %.1f" % (tl, th), {g: "%.1f-%.1f" % (lo[g], hi[g]) for g in lo})
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
        if all(abs(mid[g] - target[g]) < 3 for g in mid):
            break
        new = {g: round(P.PLAN_GRADE_ADJ[g] * target[g] / mid[g], 5) for g in mid}
        src = open(os.path.join(HERE, "params.py")).read()
        a = src.index("PLAN_GRADE_ADJ = {")
        b = src.index("}", a) + 1
        src = src[:a] + "PLAN_GRADE_ADJ = {" + ", ".join(f'"{k}": {v}' for k, v in new.items()) + "}" + src[b:]
        open(os.path.join(HERE, "params.py"), "w").write(src)
        for m in ("params", "world", "pack", "docs", "make_pack", "analysis"):
            if m in sys.modules:
                importlib.reload(sys.modules[m])
        import params as P  # noqa: F811


if __name__ == "__main__":
    main()
