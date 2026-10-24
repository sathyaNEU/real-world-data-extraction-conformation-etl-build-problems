# Cuts the two v2 zips with the v1 zips' layout: files at the root, deflated, stamped 12 January 2028 09:00.
# Usage: python3 -I zips.py <v2 inputs dir> <deliverables dir> <out dir>
import os, sys, zipfile
IN, DLV, OUT = sys.argv[1:4]

def cut(src, dst, stamp):
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(src)):
            info = zipfile.ZipInfo(f, date_time=stamp)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, open(os.path.join(src, f), "rb").read())

cut(IN, os.path.join(OUT, "Brannvik Plus Reach 2027 Input Files.zip"), (2028, 1, 12, 9, 0, 0))
cut(DLV, os.path.join(OUT, "Brannvik Plus Reach 2027 Deliverables.zip"), (2028, 1, 16, 11, 50, 0))
print("zips cut")
