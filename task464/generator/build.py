"""task464 architecture 12: build the pack, the goldens and the write-up from the seed.

    python3 generator/build.py            # target/, golden/, figures.json, submission.md, metadata.json, target.zip

Every file under target/ and golden/ is written from world.SEED; two runs are byte identical.
"""
import os
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import sim          # noqa: E402
import pack         # noqa: E402
import docs         # noqa: E402
import postprocess  # noqa: E402
import answers      # noqa: E402


def main():
    t0 = time.time()
    tgt = os.path.join(BASE, "target")
    gold = os.path.join(BASE, "golden")
    for d in (tgt, gold):
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)
    h = sim.simulate()
    st = pack.write_all(h, tgt)
    docs.main(tgt, h)
    postprocess.run(tgt)
    print("  pack written in %.1fs: %s" % (time.time() - t0, st))
    fig = answers.figures(write=True)
    try:
        import golden
        import writeup
        import meta
        import cut
    except ImportError as e:
        print("  stopped after figures.json:", e)
        return
    golden.main(fig)
    postprocess.run(gold)
    writeup.main(fig)
    meta.main()
    cut.main()
    print("  built in %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
