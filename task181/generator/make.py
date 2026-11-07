"""Build the pack, the figures and the goldens; rebuild into a scratch folder and require byte-identical output; cut
target.zip; run the checks and the independent verifier.

    python3 task181/generator/make.py
"""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C    # noqa: E402


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
    T, n = build.build()
    deliver.make(n)
    out = {"target/" + k: v for k, v in digest(C.TARGET).items()}
    out.update({"golden/" + k: v for k, v in digest(C.GOLDEN).items()})
    for f in ("submission.md", "metadata.json"):
        out[f] = hashlib.sha256(open(os.path.join(C.TASK, f), "rb").read()).hexdigest()
    out["generator/figures.json"] = hashlib.sha256(open(os.path.join(HERE, "figures.json"), "rb").read()).hexdigest()
    return out


def main():
    first = once()
    tmp = tempfile.mkdtemp(prefix="t181_")
    shutil.copytree(C.TARGET, os.path.join(tmp, "target"))
    second = once()
    same = first == second
    print("two builds byte-identical" if same else "BUILDS DIFFER: %s" % sorted(k for k in first if first[k] != second.get(k)))
    shutil.rmtree(tmp)
    import zipcut
    zipcut.cut()
    print("target.zip sha256", hashlib.sha256(open(os.path.join(C.TASK, "target.zip"), "rb").read()).hexdigest())
    rc = subprocess.call([sys.executable, os.path.join(HERE, "checks.py")])
    rv = subprocess.call([sys.executable, os.path.join(HERE, "verify.py")])
    print("checks exit %d, verify exit %d" % (rc, rv))
    return 0 if same and rc == 0 and rv == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
