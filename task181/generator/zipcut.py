"""Cut target.zip from target/: members flat, in name order, with the export's timestamp, and every member's
bytes asserted equal to the tree's file, so the archive is reproducible and never stale.

    python3 task181/generator/zipcut.py
"""
import hashlib
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import FILE_MTIME, TARGET  # noqa: E402

ZIP = os.path.join(os.path.dirname(TARGET), "target.zip")


def cut():
    names = sorted(n for n in os.listdir(TARGET) if os.path.isfile(os.path.join(TARGET, n)) and not n.startswith("."))
    tmp = ZIP + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            zi = zipfile.ZipInfo(n, date_time=FILE_MTIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(TARGET, n), "rb") as f:
                z.writestr(zi, f.read())
    os.replace(tmp, ZIP)
    with zipfile.ZipFile(ZIP) as z:
        assert z.namelist() == names, "archive members differ from target/"
        for n in names:
            assert z.read(n) == open(os.path.join(TARGET, n), "rb").read(), "stale member %s" % n
    md5 = hashlib.md5(open(ZIP, "rb").read()).hexdigest()
    print("target.zip: %d members, %d bytes, md5 %s" % (len(names), os.path.getsize(ZIP), md5))
    return md5


if __name__ == "__main__":
    cut()
