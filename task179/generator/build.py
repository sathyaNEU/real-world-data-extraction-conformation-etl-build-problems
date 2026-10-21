"""Build task179: the pack into <task>/target, the golden deliverables into <task>/golden, figures.json,
metadata.json and submission.md; then the checks and the independent verifier, a second full build in a scratch
copy compared byte for byte, and target.zip cut from the final build.

    python3 task179/generator/build.py          everything
    python3 task179/generator/build.py --once   one build, no checks (used for the second build)
    python3 task179/generator/build.py --fast   one build with the checks and the verifier, no second build or zip
"""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import warnings
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")
TASK = os.path.dirname(HERE)


def everything():
    import json
    import pack
    import deliver
    import metadata
    import submission
    pack.build()
    F, g = deliver.figures()
    with open(os.path.join(HERE, "figures.json"), "w") as f:
        json.dump(F, f, indent=1, ensure_ascii=False)
        f.write("\n")
    if os.path.isdir(deliver.GOLDEN):
        shutil.rmtree(deliver.GOLDEN)
    deliver.workbook(F, g)
    deliver.chart(g)
    metadata.write(pack.TARGET, os.path.join(TASK, "metadata.json"))
    submission.write()


def digest(root):
    out = {}
    for sub in ("target", "golden"):
        d = os.path.join(root, sub)
        for f in sorted(os.listdir(d)):
            out["%s/%s" % (sub, f)] = hashlib.sha256(open(os.path.join(d, f), "rb").read()).hexdigest()
    for f in ("metadata.json", "submission.md", os.path.join("generator", "figures.json")):
        out[f] = hashlib.sha256(open(os.path.join(root, f), "rb").read()).hexdigest()
    return out


def cut_zip():
    import util
    folder = os.path.join(TASK, "target")
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(name, date_time=util.FIXED)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    with zipfile.ZipFile(zp) as z:
        inside = {i.filename: hashlib.sha256(z.read(i.filename)).hexdigest() for i in z.infolist()}
    mine = {k.split("/", 1)[1]: v for k, v in digest(TASK).items() if k.startswith("target/")}
    if inside != mine:
        raise SystemExit("target.zip differs from target/")
    return zp, hashlib.sha256(open(zp, "rb").read()).hexdigest()


def main(argv):
    everything()
    if "--once" in argv:
        return 0
    import checks
    import verify
    ok = checks.run()
    ok = verify.main() and ok
    if "--fast" in argv:
        return 0 if ok else 1
    tmp = tempfile.mkdtemp()
    try:
        twin = os.path.join(tmp, "task179")
        shutil.copytree(HERE, os.path.join(twin, "generator"), ignore=shutil.ignore_patterns("__pycache__", "figures.json"))
        r = subprocess.run([sys.executable, os.path.join(twin, "generator", "build.py"), "--once"], capture_output=True, text=True)
        if r.returncode:
            raise SystemExit("second build failed: %s" % r.stderr[-800:])
        a, b = digest(TASK), digest(twin)
        diff = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
        if diff:
            raise SystemExit("second build differs: %s" % diff)
        print("two builds byte-identical: %d files (target/, golden/, metadata.json, submission.md, figures.json)" % len(a))
    finally:
        shutil.rmtree(tmp)
    zp, h = cut_zip()
    print("target.zip cut from this build: %d files, each identical to target/ (sha256 %s)" % (
        len(os.listdir(os.path.join(TASK, "target"))), h[:16]))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
