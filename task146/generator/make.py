"""Build task146's pack, goldens, figures.json, submission.md and metadata.json twice, require byte-identical output,
cut target.zip, then run the checks and the verifier.

    python3 task146/generator/make.py
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
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_pack as BP  # noqa: E402
import golden as GD      # noqa: E402
import writeup as WU     # noqa: E402

ZIP_STAMP = (2026, 11, 16, 8, 30, 0)


def digest(folder):
    h = {}
    for root, _d, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            h[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def one_build(base):
    target, golden = os.path.join(base, "target"), os.path.join(base, "golden")
    _w, _R, n = BP.build_pack(target)
    fig = GD.write_all(target, golden)
    json.dump(fig, open(os.path.join(base, "figures.json"), "w"), indent=1, sort_keys=True)
    WU.submission(fig, os.path.join(base, "submission.md"))
    WU.metadata(n, os.path.join(base, "metadata.json"))
    return digest(base), n


def cut_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=ZIP_STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, fn), "rb").read())


def main():
    a, b = tempfile.mkdtemp(), tempfile.mkdtemp()
    ha, n = one_build(a)
    hb, _ = one_build(b)
    same = ha == hb
    print("two builds byte-identical:", same, "(%d files)" % len(ha))
    if not same:
        for k in sorted(set(ha) | set(hb)):
            if ha.get(k) != hb.get(k):
                print("  differs:", k)
        sys.exit(1)
    for sub in ("target", "golden"):
        dst = os.path.join(TASK, sub)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(a, sub), dst)
    shutil.copy(os.path.join(a, "figures.json"), os.path.join(HERE, "figures.json"))
    shutil.copy(os.path.join(a, "metadata.json"), os.path.join(TASK, "metadata.json"))
    shutil.copy(os.path.join(a, "submission.md"), os.path.join(TASK, "submission.md"))
    cut_zip(os.path.join(TASK, "target"), os.path.join(TASK, "target.zip"))
    print("files", n)
    print("target.zip sha256", hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest())
    rc = 0
    for script in ("checks.py", "verify.py"):
        rc |= subprocess.call([sys.executable, os.path.join(HERE, script)])
    sys.exit(rc)


if __name__ == "__main__":
    main()
