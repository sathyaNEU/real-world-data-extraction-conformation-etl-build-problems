"""Builds task133 (architecture 4) twice in fresh interpreters, asserts the two builds are byte-identical, and installs target/,
golden/, submission.md, generator/figures.json, metadata.json and target.zip.

    python3 task133/generator/build.py
"""
import filecmp
import hashlib
import io
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

import params as P  # noqa: E402

ZIP_DT = (2026, 10, 20, 8, 40, 0)


def run(*args):
    r = subprocess.run([sys.executable] + list(args), cwd=HERE, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("failed: %s\n%s\n%s" % (" ".join(args), r.stdout[-2000:], r.stderr[-4000:]))
    return r.stdout


def same_dirs(a, b):
    fa, fb = sorted(os.listdir(a)), sorted(os.listdir(b))
    assert fa == fb, (set(fa) ^ set(fb))
    for f in fa:
        assert filecmp.cmp(os.path.join(a, f), os.path.join(b, f), shallow=False), "differs between builds: " + f
    return fa


def zip_dir(d):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(d)):
            zi = zipfile.ZipInfo("target/" + f, date_time=ZIP_DT)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(d, f), "rb").read())
    return buf.getvalue()


def main():
    tmp = tempfile.mkdtemp(prefix="t133_")
    try:
        b1, b2 = os.path.join(tmp, "b1"), os.path.join(tmp, "b2")
        run("make_pack.py", b1)
        run("make_pack.py", b2)
        files = same_dirs(b1, b2)
        g1, g2 = os.path.join(tmp, "g1"), os.path.join(tmp, "g2")
        run("golden.py", b1, g1)
        run("golden.py", b2, g2)
        same_dirs(g1, g2)
        z1, z2 = zip_dir(b1), zip_dir(b2)
        assert z1 == z2, "target.zip differs between builds"
        print("two builds byte-identical: %d target files, %d golden files, target.zip" % (len(files), len(os.listdir(g1))))

        tdir = os.path.join(TASK, "target")
        if os.path.exists(tdir):
            shutil.rmtree(tdir)
        shutil.copytree(b1, tdir)
        from io_util import set_mtime
        for f in os.listdir(tdir):
            set_mtime(os.path.join(tdir, f))
        gdir = os.path.join(TASK, "golden")
        if os.path.exists(gdir):
            shutil.rmtree(gdir)
        shutil.copytree(g1, gdir)
        with open(os.path.join(TASK, "target.zip"), "wb") as f:
            f.write(z1)
        sha = hashlib.sha256(z1).hexdigest()

        import writeup
        writeup.emit(tdir, TASK)
        import provenance
        meta = provenance.metadata(tdir)
        with open(os.path.join(TASK, "metadata.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=1, ensure_ascii=False)
            f.write("\n")
        print("installed target/, golden/, submission.md, generator/figures.json, metadata.json")
        print("target.zip sha256 %s" % sha)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
