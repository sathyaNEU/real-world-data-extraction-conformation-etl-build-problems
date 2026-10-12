"""Cut target.zip from target/: python3 zip_pack.py [task_dir]

One member per shipped file, sorted by name, no enclosing folder, each dated at its file's write time on the
newsroom's clock (AEST), so the archive carries what the folder carries and two cuts are byte-identical.
"""
import datetime as dt
import hashlib
import os
import sys
import zipfile
from pathlib import Path

AEST = dt.timedelta(hours=10)


def cut(task):
    target, out = Path(task) / "target", Path(task) / "target.zip"
    names = sorted(p.name for p in target.iterdir() if p.is_file())
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            p = target / n
            t = dt.datetime(1970, 1, 1) + dt.timedelta(seconds=int(p.stat().st_mtime)) + AEST
            zi = zipfile.ZipInfo(n, date_time=(t.year, t.month, t.day, t.hour, t.minute, t.second))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, p.read_bytes())
    with zipfile.ZipFile(out) as z:
        same = z.namelist() == names and all(z.read(n) == (target / n).read_bytes() for n in names)
    assert same, "target.zip does not match target/"
    print("target.zip: %d bytes, %d members, sha256 %s" % (out.stat().st_size, len(names),
                                                            hashlib.sha256(out.read_bytes()).hexdigest()[:16]))


if __name__ == "__main__":
    cut(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent)
