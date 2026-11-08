"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files (a hit is the same figure at
the asked rounding: whole charges, MWh to one decimal), and the pair priced on the planning weights (38 for the call
and its components, 7 for instruction-following, 55 for the asks).

    python3 task156/generator/ceiling.py [target]

Rows: the cracker lands the call and runs the hygiene battery on the export (one copy of each session number,
failed starts out, records with one token on one connector less than half an hour apart merged, the energy column
summed). The mirror files the rate route's set and handles the asks the same way, since they carry nothing from the
call. The full includer also joins every record that opens above the last one's closing register and takes energy
from the registers (a stress row); the register-advance row takes each unit's register advance for energy; the careful
row joins both kinds of split record exactly as the golden does and leaves only the load bank tests in."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A   # noqa: E402


def main(target, quiet=False):
    gn, ge, _ = A.golden(target)
    n = len(gn) + len(ge)
    cn, ce = A.cracker(target)
    fn, fe = A.full_includer(target)
    rn, re_ = A.register_advance(target)
    kn, ke = A.careful(target)
    crack = A.kept(cn, gn) + A.kept(ce, ge)
    care = A.kept(kn, gn) + A.kept(ke, ge)
    full = A.kept(fn, gn) + A.kept(fe, ge)
    radv = A.kept(rn, gn) + A.kept(re_, ge)
    lc = crack / float(n)
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    if not quiet:
        print("cracker (lands the call, runs the battery): keeps %d of %d ask figures (charges %d of %d, energy %d of %d), "
              "response %.1f" % (crack, n, A.kept(cn, gn), len(gn), A.kept(ce, ge), len(ge), c))
        print("mirror (the rate route's set, the same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
        print("full includer (register merge, register energy; stress row): keeps %d of %d (charges %d, energy %d), response %.1f"
              % (full, n, A.kept(fn, gn), A.kept(fe, ge), 38 + 7 + 55 * full / float(n)))
        print("register advance (each unit's register advance for energy; stress row): keeps %d of %d" % (radv, n))
        print("careful register-joined analyst (both splits joined as the golden joins them, the load bank tests left in; "
              "stress row): keeps %d of %d (charges %d, energy %d), response %.1f" % (care, n, A.kept(kn, gn), A.kept(ke, ge),
                                                                              38 + 7 + 55 * care / float(n)))
        print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return {"cracker": c, "mirror": s, "pair": (c + s) / 2, "leak": 100 * lc, "crack": crack, "full": full, "n": n}


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
