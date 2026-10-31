"""Build the pack, the figures and the goldens; rebuild and require byte-identical output; cut target.zip; run the
checks and the independent verifier.

    python3 task191/generator/make.py
"""
import hashlib
import os
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C    # noqa: E402

ZIP = os.path.join(C.TASK, "target.zip")


def digest(folder):
    h = {}
    for root, _, files in os.walk(folder):
        for f in sorted(files):
            p = os.path.join(root, f)
            h[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def once():
    import importlib
    import build
    import deliver
    importlib.reload(build)
    importlib.reload(deliver)
    W, P, fig, n = build.build()
    deliver.make(fig)
    out = {"target/" + k: v for k, v in digest(C.TARGET).items()}
    out.update({"golden/" + k: v for k, v in digest(C.GOLDEN).items()})
    for f in ("submission.md", "metadata.json"):
        out[f] = hashlib.sha256(open(os.path.join(C.TASK, f), "rb").read()).hexdigest()
    out["generator/figures.json"] = hashlib.sha256(open(os.path.join(HERE, "figures.json"), "rb").read()).hexdigest()
    return out, fig


def cut():
    names = sorted(n for n in os.listdir(C.TARGET) if os.path.isfile(os.path.join(C.TARGET, n)))
    tmp = ZIP + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            zi = zipfile.ZipInfo(n, date_time=C.FILE_MTIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(C.TARGET, n), "rb").read())
    os.replace(tmp, ZIP)
    with zipfile.ZipFile(ZIP) as z:
        assert z.namelist() == names
        for n in names:
            assert z.read(n) == open(os.path.join(C.TARGET, n), "rb").read()
    return hashlib.sha256(open(ZIP, "rb").read()).hexdigest()


def main():
    first, fig = once()
    second, _ = once()
    same = first == second
    print("two builds byte-identical" if same else "BUILDS DIFFER: %s" % sorted(k for k in first if first[k] != second.get(k)))
    sha = cut()
    print("target.zip sha256", sha)
    print("tuning", fig["call"]["tuning"], "traps", fig["traps"])
    rc = subprocess.call([sys.executable, os.path.join(HERE, "checks.py")])
    rv = subprocess.call([sys.executable, os.path.join(HERE, "verify.py")])
    rl = subprocess.call([sys.executable, os.path.join(HERE, "ceiling.py")])
    print("checks exit %d, verify exit %d, ceiling exit %d" % (rc, rv, rl))
    return 0 if same and rc == 0 and rv == 0 and rl == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
