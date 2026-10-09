"""Two consecutive builds must be byte-identical: python3 reproduce.py DIR_A DIR_B

Runs build.py into each directory (checks on), then compares every file under target/ and metadata.json
by SHA-256 and by name, and the file times. Exit status 0 only when both builds are green and identical.
"""
import hashlib
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def digest(root):
    out = {}
    for p in sorted(Path(root).rglob("*")):
        if p.is_file():
            out[str(p.relative_to(root))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def main(a, b):
    for d in (a, b):
        r = subprocess.run([sys.executable, str(HERE / "build.py"), "--out", d], capture_output=True, text=True)
        tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-500:]
        print("build %s: exit %d, %s" % (d, r.returncode, tail))
        if r.returncode != 0:
            return 1
    keep = lambda k: k.startswith("target/") or k == "metadata.json"
    da = {k: v for k, v in digest(a).items() if keep(k)}
    db = {k: v for k, v in digest(b).items() if keep(k)}
    same = da == db
    for k in sorted(set(da) | set(db)):
        if da.get(k) != db.get(k):
            print("DIFFERS  %s" % k)
    mt = {Path(a, k).stat().st_mtime == Path(b, k).stat().st_mtime for k in da if k.startswith("target/")}
    print("%d files compared, byte-identical: %s, target mtimes equal: %s" % (len(da), same, mt == {True}))
    return 0 if same and mt == {True} else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
