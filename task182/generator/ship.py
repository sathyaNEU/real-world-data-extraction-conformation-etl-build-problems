"""Cut target.zip with deterministic entries: fixed timestamps, deflate, sorted names."""
import os
import sys
import zipfile

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def cut(task=TASK):
    target = os.path.join(task, "target")
    out = os.path.join(task, "target.zip")
    names = sorted(os.listdir(target))
    if os.path.exists(out):
        os.remove(out)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            zi = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(target, n), "rb") as fh:
                z.writestr(zi, fh.read())
    return out, names


if __name__ == "__main__":
    p, names = cut()
    print("cut %s with %d entries, %.1f MB" % (p, len(names), os.path.getsize(p) / 1e6))
