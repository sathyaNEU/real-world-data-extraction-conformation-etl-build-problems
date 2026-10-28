"""task464 architecture 8: cut target.zip from target/, files at the root, sorted, one fixed timestamp."""
import os, zipfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAMP = (2026, 11, 18, 9, 0, 0)


def main():
    src = os.path.join(BASE, "target")
    out = os.path.join(BASE, "target.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n in sorted(os.listdir(src)):
            zi = zipfile.ZipInfo(n, date_time=STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(src, n), "rb").read())
    print("  target.zip, %d files" % len(os.listdir(src)))


if __name__ == "__main__":
    main()
