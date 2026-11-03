"""Cut target.zip from a built target folder: every file at the archive root, sorted by name, with a
fixed timestamp and mode, so two cuts of the same pack are byte-identical."""
import hashlib
import os
import sys
import zipfile


def cut(target, out):
    names = sorted(f for f in os.listdir(target) if os.path.isfile(os.path.join(target, f)))
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name in names:
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            info.create_system = 3
            with open(os.path.join(target, name), "rb") as fh:
                z.writestr(info, fh.read(), compresslevel=9)
    with open(out, "rb") as fh:
        return names, hashlib.sha256(fh.read()).hexdigest()


if __name__ == "__main__":
    task = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(task, "target")
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(task, "target.zip")
    names, digest = cut(tgt, out)
    print("%s: %d files, sha256 %s" % (out, len(names), digest))
