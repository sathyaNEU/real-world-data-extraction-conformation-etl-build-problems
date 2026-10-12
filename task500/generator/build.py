"""Rebuild task500's evidence pack from the seeded state, then seal the containers."""
import shutil
import sys
import time
from pathlib import Path

import model
import pack

TASK = Path(__file__).resolve().parent.parent
TARGET = TASK / "target"


def build(target=TARGET):
    t0 = time.time()
    target = Path(target)
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    m = model.State().build()
    writer = pack.Writer(m, target)
    writer.run()
    import docs
    docs.run(target, m, writer)
    try:
        import seal
        seal.seal(target)
    except ImportError:
        pass
    print("built %s in %.0fs" % (target, time.time() - t0))
    return m


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    tgt = Path(args[0]) if args else TARGET
    m = build(tgt)
