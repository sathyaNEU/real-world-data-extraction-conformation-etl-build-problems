"""Build task199 twice, assert byte-identical, install target/, golden/, metadata.json, figures.json and target.zip.

    python3 generator/build.py            # full build, checks, verifier, ceiling, write-up
    python3 generator/build.py --fast     # one build, no install (development)
"""
import filecmp
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

FIXED = (2026, 10, 16, 17, 40, 0)


def one_build(out_dir):
    for m in ("world", "pack", "analysis", "golden"):
        sys.modules.pop(m, None)
    import world
    import pack
    import golden
    import analysis
    analysis._CACHE.clear()
    w = world.World()
    target = os.path.join(out_dir, "target")
    files = pack.build(w, target)
    gdir = os.path.join(out_dir, "golden")
    gen = os.path.join(out_dir, "gen")
    os.makedirs(gen, exist_ok=True)
    golden.build(target, gdir, gen)
    return files


def tree_digest(d):
    h = hashlib.md5()
    for root, _, fns in sorted(os.walk(d)):
        for fn in sorted(fns):
            p = os.path.join(root, fn)
            h.update(os.path.relpath(p, d).encode())
            h.update(open(p, "rb").read())
    return h.hexdigest()


def same_tree(a, b):
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.funny_files:
        return False
    for fn in cmp.common_files:
        if open(os.path.join(a, fn), "rb").read() != open(os.path.join(b, fn), "rb").read():
            return False
    return all(same_tree(os.path.join(a, s), os.path.join(b, s)) for s in cmp.common_dirs)


def make_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo("target/" + fn, date_time=FIXED)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, fn), "rb").read())


def main():
    fast = "--fast" in sys.argv
    tmp = tempfile.mkdtemp(prefix="t199_")
    a, b = os.path.join(tmp, "a"), os.path.join(tmp, "b")
    files = one_build(a)
    if fast:
        print("fast build in", a)
        return 0
    one_build(b)
    ok_t = same_tree(os.path.join(a, "target"), os.path.join(b, "target"))
    ok_g = same_tree(os.path.join(a, "golden"), os.path.join(b, "golden"))
    ok_f = open(os.path.join(a, "gen", "figures.json"), "rb").read() == open(os.path.join(b, "gen", "figures.json"), "rb").read()
    print("byte-identical rebuild: target %s, golden %s, figures %s" % (ok_t, ok_g, ok_f))
    if not (ok_t and ok_g and ok_f):
        return 1
    # install
    for sub in ("target", "golden"):
        dst = os.path.join(TASK, sub)
        shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(os.path.join(a, sub), dst)
    shutil.copy(os.path.join(a, "gen", "figures.json"), os.path.join(HERE, "figures.json"))
    import metadata
    metadata.write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"), files)
    make_zip(os.path.join(TASK, "target"), os.path.join(TASK, "target.zip"))
    zmd5 = hashlib.md5(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()
    print("target digest %s golden digest %s target.zip md5 %s (%d members)" % (
        tree_digest(os.path.join(TASK, "target")), tree_digest(os.path.join(TASK, "golden")), zmd5,
        len(os.listdir(os.path.join(TASK, "target")))))
    shutil.rmtree(tmp)
    rc = 0
    for script in ("checks.py", "verify.py", "ceiling.py", "writeup.py"):
        r = subprocess.run([sys.executable, os.path.join(HERE, script)], cwd=TASK)
        print("%s exit %d" % (script, r.returncode))
        rc = rc or r.returncode
    return rc


if __name__ == "__main__":
    sys.exit(main())
