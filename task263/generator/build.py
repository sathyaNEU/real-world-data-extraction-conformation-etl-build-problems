"""Build task263: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task263/generator/build.py              everything
    python3 task263/generator/build.py --out DIR    the pack only, into DIR
    python3 task263/generator/build.py --golden     the pack and the goldens, no checks"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import argparse      # noqa: E402
import hashlib       # noqa: E402
import json          # noqa: E402
import shutil        # noqa: E402
import sys           # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K         # noqa: E402
import docs as D           # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = 1788347520          # 2 September 2026 09:12 local, the department's send


def world():
    S, conns = W.statewide()
    R.assign(S)
    X = W.samples([s for s in S if s["eps"]])
    R.number_samples(X)
    R.revisions(X)
    ops = W.operations_2025(S, conns, X)
    M = R.meters(S)
    return dict(S=S, conns=conns, X=X, ops=ops, M=M)


def build(out):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    T = world()
    S = T["S"]
    counts = dict(results=R.write_results(p("results"), S, T["X"]), records=R.write_collection(p("records"), S, T["X"]),
                  inventory=R.write_inventory(p("inventory"), S), mor=R.write_mor(p("mor"), S, T["ops"], T["M"]),
                  meters=R.write_meters(p("meters"), T["M"]), register=R.write_register(p("register"), S),
                  connections=R.write_connections(p("connections"), S, T["conns"]), labs=R.write_labs(p("labs")),
                  survey=R.write_survey(p("survey"), S), private=R.write_private(p("private")))
    listed = [s for s in S if s["listed"]]
    listed.sort(key=lambda s: s["rank"])
    D.write_iup(p("iup"), listed)
    D.write_guide(p("guide"))
    open(p("notes"), "w", encoding="utf-8").write(D.data_notes(K.FILES, counts))
    PP.COMPANY = K.DEPT
    PP.normalize_ooxml(p("inventory"), "SDWIS Reports", K.PEOPLE["lead"], "2026-09-01T13:05:22Z",
                       "2026-09-02T14:01:37Z", excel=True)
    PP.normalize_pdf(p("iup"), b"D:20260929161204-05'00'", b"D:20260930083340-05'00'")
    PP.normalize_pdf(p("guide"), b"D:20231211101532-06'00'", b"D:20231218144907-06'00'")
    for f in sorted(os.listdir(out)):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    return T, counts


def tree_digest(d):
    h = hashlib.sha256()
    for f in sorted(os.listdir(d)):
        h.update(f.encode())
        h.update(open(os.path.join(d, f), "rb").read())
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--golden", action="store_true")
    a = ap.parse_args()
    if a.out:
        build(a.out)
        return
    target = os.path.join(TASK, "target")
    T, counts = build(target)
    print("pack:", {k: v for k, v in counts.items()})
    import deliver
    deliver.write(target, os.path.join(TASK, "golden"), T)
    if a.golden:
        return
    import checks
    checks.run(target, T)
    r = os.system("python3 %s %s" % (os.path.join(HERE, "verify.py"), target))
    assert r == 0, "verify failed"
    scratch = os.path.join(TASK, ".rebuild")
    build(scratch)
    same = tree_digest(scratch) == tree_digest(target)
    shutil.rmtree(scratch)
    assert same, "second build differs"
    print("rebuild byte-identical")
    zp = os.path.join(TASK, "target.zip")
    if os.path.exists(zp):
        os.remove(zp)
    import zipfile
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo("target/" + f, date_time=(2026, 9, 2, 9, 12, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    print("target.zip cut")


if __name__ == "__main__":
    main()
