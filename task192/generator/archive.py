"""Cut target.zip from the tree, with entry timestamps the rebuild cannot move."""
import os
import sys
import zipfile


def cut(target, out):
    names = []
    for root, _, files in os.walk(target):
        for f in files:
            p = os.path.join(root, f)
            names.append((os.path.relpath(p, os.path.dirname(target)), p))
    names.sort()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for arc, p in names:
            info = zipfile.ZipInfo(arc, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(p, "rb") as fh:
                z.writestr(info, fh.read())
    return out, len(names)


if __name__ == "__main__":
    task = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out, n = cut(os.path.join(task, "target"), os.path.join(task, "target.zip"))
    print("%s, %d members" % (out, n))
