"""Sets params.PLAN_GRADE_ADJ (the plan's compartment yields by grade) so each grade's FY2028 loads sit at the centre of
its 50-load bin and the total at the centre of its 100-load bin, measured on a written pack."""
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
        pk, res = A.ladder(tmp)
    finally:
        shutil.rmtree(tmp)
    return res["golden"]


def main(rounds=4):
    import params as P
    for i in range(rounds):
        g = measure()
        tot = sum(g.values())
        print("round", i, round(tot), {k: round(v, 1) for k, v in g.items()})
        target = {k: round(v / 50) * 50 for k, v in g.items()}
        # the total's 100-load bin centre: nudge the largest grade by 50 if the sum of centres sits on an odd 50
        if sum(target.values()) % 100 != 0:
            big = max(target, key=lambda k: target[k])
            target[big] += 50 if g[big] > target[big] else -50
        if all(abs(g[k] - target[k]) < 4 for k in g) and abs(tot - sum(target.values())) < 8:
            break
        new = {k: round(P.PLAN_GRADE_ADJ[k] * target[k] / g[k], 5) for k in g}
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
