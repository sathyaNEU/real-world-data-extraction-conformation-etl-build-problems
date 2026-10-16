"""Build task148: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the pack.

    python3 task148/generator/build.py              everything
    python3 task148/generator/build.py --out DIR    the pack only, into DIR"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as CA           # noqa: E402
import common as K          # noqa: E402
import docs as DOC          # noqa: E402
import forecast as FC       # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)

FILES = [
    (R.F_LEGACY, "ACD call detail, legacy CAMA and ALI layout, 1 January 2025 to the cutover (wireline to 16 May 2025)."),
    (R.F_I3, "NG911 i3 call log, 13 May 2025 to 30 September 2026."),
    (R.F_ROSTER, "Floor roster: call-takers on the 911 floor by block, 31 December 2024 to 30 September 2026."),
    (R.F_FORECAST, "Tri-County Regional 911 Board, hourly 911 volume forecast for fiscal 2027 and 2028 (published 15 September 2026)."),
    (DOC.F_SOP, "SOP 2.10, call answering and answer-time reporting (revision 4, effective 1 July 2025)."),
    (DOC.F_BUDGET, "FY2028 recommended budget, communications floor staffing (budget office draft, 2 October 2026)."),
    (R.F_CHE, "Call-handling systems' location records for wireless 911 calls in the north-east, fiscal 2026."),
    (R.F_BOUNDARY, "Halvorsen Township boundary, Tavish County GIS (the ESInet routing layer from 1 July 2027)."),
    (R.F_DIRECTORY, "ESInet PSAP directory: PSAP URIs and their agencies."),
    (R.F_CALLBACK, "Callback desk tasks, 1 January to 30 June 2026."),
    (R.F_CAD, "CAD incidents opened from 911 calls on Friday and Saturday late shifts, fiscal 2026."),
    (R.F_ADMIN, "Administrative line ACD call detail, fiscal 2026."),
    (R.F_MANIFEST, "Extract log: each file's source system, record count and pull date."),
    (DOC.F_README, "This file."),
]
SYSTEMS = {
    R.F_LEGACY: "legacy ACD (CAMA/ALI) MIS", R.F_I3: "NG911 call-handling system, i3 logging", R.F_ROSTER: "scheduling system",
    R.F_FORECAST: "Tri-County Regional 911 Board", DOC.F_SOP: "agency procedures", DOC.F_BUDGET: "county budget office",
    R.F_CHE: "NG911 call-handling systems (floor and backup centre), location records", R.F_BOUNDARY: "Tavish County GIS",
    R.F_DIRECTORY: "Tri-County ESInet", R.F_CALLBACK: "callback module", R.F_CAD: "CAD",
    R.F_ADMIN: "administrative line ACD",
}


class Built:
    pass


def world():
    W = WD.simulate()
    R.call_ids(W)
    R.admin_ids(W)
    return W


def build(out, quiet=False, W=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda f: os.path.join(out, f)
    W = W or world()
    counts = {}
    counts[R.F_LEGACY] = K.write_csv(p(R.F_LEGACY), R.LEGACY_COLS, R.legacy_rows(W), crlf=True)
    lines = R.i3_lines(W)
    with open(p(R.F_I3), "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(lines) + "\n")
    counts[R.F_I3] = len(lines)
    C = CA.read_calls(out, R.F_LEGACY, R.F_I3)
    busy = CA.estimates(C)[0]
    pat, wab, nab = CA.estimates(C, C.late)[1:]     # the late shift's own callers
    tb, gold, late = FC.write(p(R.F_FORECAST), busy, pat)
    counts[R.F_FORECAST] = sum(len(v) for v in tb.values())
    counts[R.F_ROSTER] = K.write_csv(p(R.F_ROSTER), R.ROSTER_COLS, R.roster_rows(W))
    counts[R.F_CHE] = K.write_csv(p(R.F_CHE), R.CHE_COLS, R.che_rows(W))
    with open(p(R.F_BOUNDARY), "w", encoding="utf-8", newline="") as fh:
        fh.write(R.boundary_geojson())
    counts[R.F_DIRECTORY] = K.write_csv(p(R.F_DIRECTORY), R.DIRECTORY_COLS, R.directory_rows())
    counts[R.F_CALLBACK] = K.write_csv(p(R.F_CALLBACK), R.CALLBACK_COLS, R.callback_rows(W))
    counts[R.F_CAD] = K.write_csv(p(R.F_CAD), R.CAD_COLS, R.cad_rows(W))
    counts[R.F_ADMIN] = K.write_csv(p(R.F_ADMIN), R.ADMIN_COLS, R.admin_rows(W))
    DOC.write_sop(p(DOC.F_SOP))
    DOC.write_budget(p(DOC.F_BUDGET))
    man = []
    for f, d in FILES:
        if f in (R.F_MANIFEST, DOC.F_README):
            continue
        man.append({"file": f, "system": SYSTEMS[f], "description": d, "records": counts.get(f, ""),
                    "pulled": K.EXPORT_DATE.isoformat() if f not in (R.F_FORECAST, DOC.F_SOP, DOC.F_BUDGET) else ""})
    counts[R.F_MANIFEST] = K.write_csv(p(R.F_MANIFEST), ["file", "system", "description", "records", "pulled"], man)
    with open(p(DOC.F_README), "w", encoding="utf-8", newline="") as fh:
        fh.write(DOC.readme_text(FILES))
    PP.normalize_pdf(p(DOC.F_SOP), b"D:20250623143107-05'00'", b"D:20250627091822-05'00'")
    PP.normalize_pdf(p(DOC.F_BUDGET), b"D:20260929160412-05'00'", b"D:20261002083955-05'00'")
    PP.normalize_ooxml(p(R.F_FORECAST), K.PEOPLE["planner"], K.PEOPLE["planner"], "2026-08-04T19:22:51Z",
                       "2026-09-15T14:07:33Z", excel=True, company=K.BOARD)
    stamp = K.EXPORT_STAMP.timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    B = Built()
    B.W, B.C, B.counts, B.est = W, C, counts, (busy, pat, wab, nab)
    B.forecast_tables, B.forecast_gold, B.forecast_late = tb, gold, late
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return B


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    when = K.EXPORT_STAMP.timetuple()[:6]
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(f, date_time=when)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(folder, f), "rb") as fh:
                z.writestr(zi, fh.read())
    return zp


def everything(root, quiet=False):
    import deliver as DL
    import metadata as MD
    B = build(os.path.join(root, "target"), quiet=quiet)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    G = DL.main(os.path.join(root, "target"), os.path.join(root, "golden"),
                os.path.join(root, "generator", "figures.json"), B=B)
    stamp = K.EXPORT_STAMP.timestamp() + 2 * 86400
    for f in os.listdir(os.path.join(root, "golden")):
        os.utime(os.path.join(root, "golden", f), (stamp, stamp))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"), FILES)
    return B, G


def main():
    import checks as CK
    import verify as V
    B, G = everything(TASK)
    CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), B=B, G=G,
           meta_path=os.path.join(TASK, "metadata.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        os.makedirs(os.path.join(tmp, "generator"))
        everything(tmp, quiet=True)
        same_t = digest(os.path.join(TASK, "target")) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        same = {}
        for f in ("metadata.json", "submission.md", os.path.join("generator", "figures.json")):
            same[f] = open(os.path.join(TASK, f), "rb").read() == open(os.path.join(tmp, f), "rb").read()
        same["target.zip"] = open(cut_zip(TASK), "rb").read() == open(cut_zip(tmp), "rb").read()
        if not (same_t and same_g and all(same.values())):
            d1, d2 = digest(os.path.join(TASK, "target")), digest(os.path.join(tmp, "target"))
            g1, g2 = digest(os.path.join(TASK, "golden")), digest(os.path.join(tmp, "golden"))
            raise SystemExit("second build differs: target %s, golden %s, %s; %s" % (
                same_t, same_g, same, [f for f in d1 if d1[f] != d2.get(f)] + [f for f in g1 if g1[f] != g2.get(f)]))
    finally:
        shutil.rmtree(tmp)
    allh = hashlib.sha256("".join(v for _, v in sorted(digest(os.path.join(TASK, "target")).items())).encode() +
                          "".join(v for _, v in sorted(digest(os.path.join(TASK, "golden")).items())).encode())
    print("two builds byte-identical: %d target files, %d golden files, metadata.json, figures.json and target.zip "
          "(sha256 %s; target.zip sha256 %s)" % (
              len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden"))),
              allh.hexdigest()[:16], hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    else:
        main()
