"""Build task114's bundle: simulate, write target/, recompute the golden from target/, assert, render.

    python3 build.py            # from task114/generator
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

import book
import devices
import pack
import world

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "target"
SEED = 114


def simulate():
    W = world.World()
    rng = np.random.default_rng(SEED)
    W.rooms = world.rooms()
    world.build_people(W, rng)
    world.build_presence(W, rng)
    world.build_meetings(W, rng)
    world.build_client_and_events(W, rng)
    book.build(W, rng)
    assert not W.book_fails, W.book_fails[:5]
    devices.plan(W, SEED)
    return W


def main(stage="all"):
    t0 = time.time()
    W = simulate()
    if TARGET.exists():
        for p in TARGET.iterdir():
            if p.is_file():
                p.unlink()
    sizes = pack.write_data(W, TARGET, SEED)
    print("data written", sizes, round(time.time() - t0, 1), "s")
    if stage == "data":
        return W
    import docs
    docs.write_docs(W, TARGET)
    import golden as G
    out = G.golden(TARGET)
    import asserts
    n = asserts.run(W, out, TARGET)
    out["assertions"] = n
    (Path(__file__).parent / "golden_figures.json").write_text(json.dumps(out, indent=1, sort_keys=True, default=str))
    import seal
    seal.seal(TARGET)
    import deliver
    deliver.main()
    seal.bundle(ROOT)
    print("assertions green:", n, round(time.time() - t0, 1), "s")
    return W, out


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "all")
