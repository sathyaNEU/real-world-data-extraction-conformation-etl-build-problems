"""task464 architecture 10: build the pack, the goldens and the write-up from the seed.

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

import sim
import rel
import pack
import docs
import postprocess
import answers
import golden
import writeup
import meta
import cut


def storm_circuits(w):
    names = {f["code"]: f["name"] for f in w["feeders"]}
    return [names[f["code"]] for f in w["feeders"]
            if any(sim.W.CONDUCTORS[s.code][1] == "OH" for s in w["sections"] if s.feeder == f["code"])]


def main():
    t0 = time.time()
    tgt = os.path.join(BASE, "target")
    gold = os.path.join(BASE, "golden")
    for d in (tgt, gold):
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)
    w = sim.simulate()
    r = w["rel"]
    st = pack.write_all(w, r, tgt)
    docs.main(w, tgt, storm_circuits(w))
    postprocess.run(tgt)
    print("  pack written in %.1fs: %s" % (time.time() - t0, st))
    fig = answers.figures(write=True)
    golden.main(fig)
    postprocess.run(gold)
    writeup.main(fig)
    meta.main()
    cut.main()
    print("  built in %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
