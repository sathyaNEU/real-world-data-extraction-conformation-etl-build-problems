"""task163 build: world, pack, the containers made reproducible, the golden from the shipped files, the deliverables,
the checks, the independent verifier, the ceiling and metadata.json.

    python3 task163/generator/build.py            # writes target/, golden/, generator/figures.json, metadata.json
"""
from __future__ import annotations

import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import common as K          # noqa: E402
import pack as PK           # noqa: E402
import postprocess as PP    # noqa: E402
import world as W           # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")

STAMPS = {
    PK.F_PLAN: ("Uphall Engineering", "Brian Cook", "2026-09-21T09:14:00Z", "2026-10-14T15:52:00Z",
                "Aubrine shelving re-slot plan 2027"),
    PK.F_CLAIMS: ("Aubrine Customer Care", "Aubrine Customer Care", "2026-10-30T16:58:00Z", "2026-10-30T16:58:00Z",
                  None),
    PK.F_TRAIN: ("Lathmor HR Uphall", "Lathmor HR Uphall", "2023-01-16T10:03:00Z", "2026-10-22T13:41:00Z", None),
}
PDF_STAMPS = {
    PK.F_SCHED: (b"D:20250106114100+00'00'", b"D:20250106114100+00'00'"),
    PK.F_PBSOP: (b"D:20250512091600+01'00'", b"D:20250512091600+01'00'"),
    PK.F_RBSOP: (b"D:20250318150200+00'00'", b"D:20250318150200+00'00'"),
    PK.F_RAV: (b"D:20261005082300+01'00'", b"D:20261005082300+01'00'"),
}


def normalise(t):
    for f, (creator, last, c, m, title) in STAMPS.items():
        PP.normalize_ooxml(os.path.join(t, f), creator, last, c, m, title=title, excel=True,
                           company="Aubrine Ltd" if f == PK.F_CLAIMS else K.COMPANY)
    for f, (c, m) in PDF_STAMPS.items():
        PP.normalize_pdf(os.path.join(t, f), c, m)


def zip_target():
    """target.zip: the pack's files flat, in name order, each stamped at the extract's close."""
    import zipfile
    path = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(path, "w") as z:
        for fn in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo(fn, date_time=(2026, 10, 30, 17, 30, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(TARGET, fn), "rb") as fh:
                z.writestr(zi, fh.read())


def main():
    for d in (TARGET, GOLDEN):
        if os.path.isdir(d):
            shutil.rmtree(d)
    w = W.build()
    counts = PK.write_all(TARGET, w)
    normalise(TARGET)
    import calc
    fig = calc.figures(TARGET)
    with open(os.path.join(HERE, "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True, default=str)
        fh.write("\n")
    import deliver
    deliver.write_all(GOLDEN, fig, TASK)
    import metadata
    metadata.write(TASK, counts)
    zip_target()
    print("built: %d files in target/" % len(os.listdir(TARGET)))
    for k, v in sorted(counts.items()):
        print("  %-34s %s" % (k, v))
    return w, fig


if __name__ == "__main__":
    main()
