"""Builds task248 twice from nothing, checks the two builds are byte-identical, then installs target/, golden/,
metadata.json, submission.md, generator/figures.json and target.zip.

    python3 task248/generator/build.py
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import make  # noqa: E402
import analysis  # noqa: E402
import golden  # noqa: E402
import writeup  # noqa: E402

ZIP_STAMP = (2027, 1, 11, 16, 40, 0)


def digest(folder):
    h = {}
    for root, _d, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            h[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def one_build(base):
    target, gold = os.path.join(base, "target"), os.path.join(base, "golden")
    make.make(target)
    res, pk = analysis.analyse(target)
    golden.write(gold, res, pk)
    figs = writeup.figures(res, pk)
    with open(os.path.join(base, "figures.json"), "w", encoding="utf-8") as f:
        json.dump(figs, f, indent=1)
    with open(os.path.join(base, "submission.md"), "w", encoding="utf-8") as f:
        f.write(writeup.submission(res, pk, figs))
    with open(os.path.join(base, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(writeup.metadata(target, res), f, indent=1, sort_keys=True)
    return digest(base)


def cut_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=ZIP_STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, fn), "rb").read())


def main():
    a, b = tempfile.mkdtemp(), tempfile.mkdtemp()
    da, db = one_build(a), one_build(b)
    if da != db:
        print("NOT byte-identical:", sorted(k for k in set(da) | set(db) if da.get(k) != db.get(k)))
        sys.exit(1)
    print("two builds byte-identical over %d files" % len(da))
    for sub in ("target", "golden"):
        dst = os.path.join(TASK, sub)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(a, sub), dst)
    shutil.copy(os.path.join(a, "figures.json"), os.path.join(HERE, "figures.json"))
    shutil.copy(os.path.join(a, "metadata.json"), os.path.join(TASK, "metadata.json"))
    shutil.copy(os.path.join(a, "submission.md"), os.path.join(TASK, "submission.md"))
    cut_zip(os.path.join(TASK, "target"), os.path.join(TASK, "target.zip"))
    z = hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()
    print("target.zip", z[:8])
    shutil.rmtree(a)
    shutil.rmtree(b)


if __name__ == "__main__":
    main()
