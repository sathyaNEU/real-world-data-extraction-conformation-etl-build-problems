# Cuts the two platform zips with the v1 zips' layout: files at the root, deflated, the inputs stamped
# 12 January 2028 09:00 and the golden deliverables 16 January 2028 11:50.
# Usage: python3 -I zips.py <inputs dir> <deliverables dir> <out dir>
import os, sys, zipfile
IN, DLV, OUT = sys.argv[1:4]

def cut(src, dst, stamp):
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(src)):
            info = zipfile.ZipInfo(f, date_time=stamp)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, open(os.path.join(src, f), "rb").read())

cut(IN, os.path.join(OUT, "mkt-01_brannvik_plus_reach_2027_input_files.zip"), (2028, 1, 12, 9, 0, 0))
cut(DLV, os.path.join(OUT, "mkt-01_brannvik_plus_reach_2027_golden_deliverables.zip"), (2028, 1, 16, 11, 50, 0))
print("zips cut")
