"""The world-seed screen behind the design note's world selection: each seed is built into target/ and kept only
when every step route files the golden on the cut pack with margins of 12 inside and 6 outside the trigger (3.5
outside at a half share). Run from the task folder; it rebuilds the shipped seed at the end, so target/ and the
goldens are left as shipped.

    python3 task181/generator/seeds.py 0 1 2 3
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build  # noqa: E402
import reader  # noqa: E402
import routes as R  # noqa: E402

GOLD = ["Bagumbayan", "Maligaya", "San Roque"]
IN_MIN, OUT_MIN, HALF_MIN = 12.0, 6.0, 3.5


def screen(seed):
    build.WORLD_SEED = seed
    try:
        build.build()
    except AssertionError as e:
        return "seed %d: the clean truth fails the design (%s)" % (seed, str(e)[:70])
    L = reader.load()
    res, hist, pop, emp, W, names = L["res"], L["hist"], L["pop"], L["emp"], L["W"], L["names"]
    gold = {names.index(n) for n in GOLD}
    worst_in, worst_out, off = 1e9, 1e9, []
    for k, f in R.ROUTES_STEP.items():
        c = f(res, hist, pop, emp, W)
        m = R.margins(c, gold)
        if R.flagged(c) != gold:
            off.append(k)
        worst_in = min(worst_in, m[0])
        if k != "fractional_0.5":
            worst_out = min(worst_out, m[1])
    half = R.margins(R.fractional(res, hist, pop, emp, W, phi=0.5), gold)[1]
    meets = not off and worst_in >= IN_MIN and worst_out >= OUT_MIN and half >= HALF_MIN
    return "seed %d: routes off the golden %s; margins inside %.1f, outside %.1f, outside at a half share %.1f: %s" % (
        seed, off or "none", worst_in, worst_out, half, "meets the design" if meets else "rejected")


if __name__ == "__main__":
    shipped = build.WORLD_SEED
    for s in [int(x) for x in sys.argv[1:]]:
        print(screen(s), flush=True)
    subprocess.run([sys.executable, os.path.join(HERE, "build.py")], check=True, stdout=subprocess.DEVNULL)
    print("rebuilt the shipped seed %d" % shipped)
