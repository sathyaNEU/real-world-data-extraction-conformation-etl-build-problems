"""task464 architecture 8: the orchestrator. Wipes target/ and rebuilds the whole pack from the generator."""
import os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(os.path.dirname(HERE), "target")
import world as W
import sim as S
import pack, docs, extras, postprocess


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    sim = S.simulate()
    enr, wmeta = pack.build(sim)
    rows = pack.write(sim, enr, wmeta)
    docs.main()
    rows += extras.write_all()
    import golden as _g
    _g.main()
    for n, k, ch in postprocess.run(OUT):
        pass
    for n, k, ch in postprocess.run(os.path.join(os.path.dirname(HERE), "golden")):
        pass
    print()
    names = sorted(os.listdir(OUT))
    exts = sorted({os.path.splitext(n)[1] for n in names})
    big = max((os.path.getsize(os.path.join(OUT, n)), n) for n in names)
    import csv as _csv
    maxrows = 0
    for n in names:
        if n.endswith(".csv"):
            with open(os.path.join(OUT, n), encoding="utf-8") as fh:
                maxrows = max(maxrows, sum(1 for _ in fh) - 1)
    print("pack: %d files, %d formats %s" % (len(names), len(exts), exts))
    print("largest file %s at %.1f MB, largest csv row count %d" % (big[1], big[0] / 1e6, maxrows))
    for n in names:
        print("   %-46s %9d bytes" % (n, os.path.getsize(os.path.join(OUT, n))))


if __name__ == "__main__":
    main()
