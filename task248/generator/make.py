"""Simulate the world and write the pack into a directory (default: generator/out/target)."""
import os, sys, shutil
import world, pack


def make(target):
    if os.path.exists(target):
        shutil.rmtree(target)
    os.makedirs(target)
    o = world.simulate()
    idm = pack.build(target, o)
    return o, idm


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "target")
    make(tgt)
    print("written", tgt)
