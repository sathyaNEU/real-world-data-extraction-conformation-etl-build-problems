"""Cut target.zip from the final rebuild, deterministically."""
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def cut(target=None, out=None):
    target = target or os.path.join(TASK, "target")
    out = out or os.path.join(TASK, "target.zip")
    names = sorted(os.listdir(target))
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for name in names:
            zi = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(target, name), "rb") as fh:
                z.writestr(zi, fh.read())
    return out, len(names)


if __name__ == "__main__":
    p, n = cut()
    print("%s: %d members, %d bytes" % (os.path.basename(p), n, os.path.getsize(p)))
