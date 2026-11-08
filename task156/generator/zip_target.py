"""Cuts task156/target.zip from target/: the files at the archive's root, in name order, each stamped with the
export time, so two cuts of the same pack are byte-identical. python3 task156/generator/zip_target.py"""
import hashlib
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def main(task=TASK):
    target = os.path.join(task, "target")
    out = os.path.join(task, "target.zip")
    with zipfile.ZipFile(out, "w") as z:
        for name in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(name, date_time=(2026, 11, 2, 7, 40, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            zi.create_system = 3
            z.writestr(zi, open(os.path.join(target, name), "rb").read())
    h = hashlib.sha256(open(out, "rb").read()).hexdigest()
    print("target.zip sha256 %s, %d bytes" % (h, os.path.getsize(out)))
    return h


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else TASK)
