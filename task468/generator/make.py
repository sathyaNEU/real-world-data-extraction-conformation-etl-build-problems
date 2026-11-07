"""Build task468's pack, goldens, figures.json, submission.md and metadata.json; rebuild into a scratch folder and
require byte-identical output; cut target.zip; then run the checks and the independent verifier on the cut.

    python3 task468/generator/make.py
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen as G       # noqa: E402
import golden as GD   # noqa: E402
import pack as K      # noqa: E402
import solve as SV    # noqa: E402
import writeup as WU  # noqa: E402

TASK = os.path.dirname(HERE)
STAMP = (2027, 1, 12, 9, 0, 0)


def build(root):
    target, golden = os.path.join(root, "target"), os.path.join(root, "golden")
    for d in (target, golden):
        shutil.rmtree(d, ignore_errors=True)
    K.build(target)
    R = SV.solve(target)
    GD.write_all(R, golden)
    fig = WU.figures(R)
    json.dump(fig, open(os.path.join(root, "figures.json"), "w"), indent=1, sort_keys=True)
    WU.submission(fig, os.path.join(root, "submission.md"))
    WU.metadata(os.path.join(root, "metadata.json"), G.FILES, G.DISTRACTORS)
    return R


def digest(root):
    h = {}
    for base, _, files in os.walk(root):
        for f in sorted(files):
            p = os.path.join(base, f)
            h[os.path.relpath(p, root)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def cut_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())


def main():
    scratch = tempfile.mkdtemp(prefix="t468_")
    a = os.path.join(scratch, "a")
    b = os.path.join(scratch, "b")
    for r in (a, b):
        os.makedirs(r)
        build(r)
    same = digest(a) == digest(b)
    print("two builds byte-identical: %s (%d files)" % (same, len(digest(a))))
    if not same:
        sys.exit(1)
    for d in ("target", "golden"):
        shutil.rmtree(os.path.join(TASK, d), ignore_errors=True)
        shutil.copytree(os.path.join(a, d), os.path.join(TASK, d))
    shutil.copy(os.path.join(a, "figures.json"), os.path.join(HERE, "figures.json"))
    shutil.copy(os.path.join(a, "submission.md"), os.path.join(TASK, "submission.md"))
    shutil.copy(os.path.join(a, "metadata.json"), os.path.join(TASK, "metadata.json"))
    cut_zip(os.path.join(TASK, "target"), os.path.join(TASK, "target.zip"))
    print("target.zip sha256 %s" % hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest())
    shutil.rmtree(scratch)
    rc = 0
    for s in ("checks.py", "verify.py"):
        rc |= subprocess.call([sys.executable, os.path.join(HERE, s)])
    sys.exit(rc)


if __name__ == "__main__":
    main()
