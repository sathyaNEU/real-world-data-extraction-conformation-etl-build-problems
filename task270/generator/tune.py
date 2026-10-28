"""Set each area's mortality level so its golden life expectancy at 85, computed from the shipped files, sits in the
middle of its one-decimal cell and on the side of the line the design puts it, with every rebuild in the standing
family printing the same cell. Writes the levels into common.py.

    python3 task270/generator/tune.py <scratch dir> [rounds]"""
from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build    # noqa: E402
import calc     # noqa: E402
import common as K  # noqa: E402

FAMILY = ("G", "G_nosplit", "G_bysex", "G_dropdob", "G_ax45", "G_floor")
MIN_EDGE = 0.022


def score(out):
    bad = {}
    for a, r in out.items():
        g = r["G"]
        cell = round(g, 1)
        edge = 0.05 - abs(g - cell)
        fam_ok = all(round(r[k], 1) == cell for k in FAMILY)
        side_ok = (g < K.LINE) == (K.TARGET[a] < K.LINE) and abs(g - K.LINE) > 0.08
        if edge < MIN_EDGE or not fam_ok or not side_ok:
            bad[a] = g - K.TARGET[a]
    return bad


def main(argv):
    scratch = argv[0]
    rounds = int(argv[1]) if len(argv) > 1 else 6
    levels = dict(K.LEVELS)
    step = {a: 1.0 for a in levels}
    last = {}
    for it in range(rounds):
        K.LEVELS.clear()
        K.LEVELS.update(levels)
        A, P, Y = build.world()
        build.write_pack(scratch, A, P, Y, say=lambda *a: None)
        out, *_ = calc.rungs(scratch)
        bad = score(out)
        print("round", it, "off:", {a: round(out[a]["G"], 3) for a in bad}, flush=True)
        if not bad:
            break
        for a, err in bad.items():
            if a in last and (last[a] > 0) != (err > 0):
                step[a] /= 2.0          # the error changed sign: the level sits between two cells, take smaller steps
            last[a] = err
            levels[a] *= float(2.718281828 ** (step[a] * err / 5.5))
    src = open(os.path.join(HERE, "common.py")).read()
    block = "LEVELS = {\n" + "".join('    "%s": %.6f,\n' % (k, v) for k, v in sorted(levels.items())) + "}\n"
    src = re.sub(r"LEVELS = \{\n.*?\n\}\n", block, src, flags=re.S)
    open(os.path.join(HERE, "common.py"), "w").write(src)
    print(json.dumps({a: round(out[a]["G"], 3) for a in out}, indent=1))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
