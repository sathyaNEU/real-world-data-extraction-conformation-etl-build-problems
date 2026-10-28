"""task464 architecture 9: the orchestrator. Wipes target/ and rebuilds the pack, the goldens and the write-up."""
import os, shutil, sys, time
os.environ["TZ"] = "UTC"; time.tzset()  # the PDFs stamp their dates in local time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
BASE = os.path.dirname(HERE)
OUT = os.environ.get("T464_TARGET") or os.path.join(BASE, "target")
import world as W
import sim as S
import pack, extras


def build_pack(seed=None):
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    t0 = time.time()
    w = S.simulate(seed if seed is not None else S.SEED)
    st = pack.write(w)
    pids = set(r["pid"] for r in w.issues if W.EXTRACT_FROM <= r["t"] <= W.ASOF)
    st.update(extras.write_all(w, pids))
    return w, st, time.time() - t0


def main():
    w, st, dt = build_pack()
    print("pack written in %.0fs" % dt, st)
    import docs; docs.main()
    import answers; answers.main()
    import family; family.main()
    import golden; golden.main()
    import meta; meta.main()
    import writeup; writeup.main()
    import postprocess
    for folder in ("target", "golden"):
        d = os.path.join(BASE, folder)
        if os.path.isdir(d):
            postprocess.run(d)
    import cut; cut.main()
    import ceiling; ceiling.main()


if __name__ == "__main__":
    main()
