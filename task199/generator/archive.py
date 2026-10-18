"""task199 archive. Cuts target.zip from the tree as it stands, deterministically.

    python3 task199/generator/archive.py

Members are the bundle's files at the archive root, in sorted order, with a fixed stamp, so the
archive is byte identical across runs and agrees with the tree by content.
"""
import hashlib
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
OUT = os.path.join(TASK, "target.zip")


def digest_tree(path):
    h = hashlib.md5()
    for name in sorted(os.listdir(path)):
        h.update(("%s %s\n" % (name, hashlib.md5(
            open(os.path.join(path, name), "rb").read()).hexdigest())).encode())
    return h.hexdigest()


def main():
    names = sorted(os.listdir(TARGET))
    if os.path.exists(OUT):
        os.remove(OUT)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for name in names:
            zi = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, name), "rb").read())
    os.utime(OUT, (1762333200, 1762333200))
    # the archive agrees with the tree by content, member for member
    with zipfile.ZipFile(OUT) as z:
        assert z.namelist() == names, "archive members differ from the tree"
        for name in names:
            assert z.read(name) == open(os.path.join(TARGET, name), "rb").read(), name
    print("target.zip: %d members, md5 %s, tree digest %s"
          % (len(names), hashlib.md5(open(OUT, "rb").read()).hexdigest(), digest_tree(TARGET)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
