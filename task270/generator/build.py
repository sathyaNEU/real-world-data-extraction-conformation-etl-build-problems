"""task270 build: the world, the 2026 operations, the pack under target/, the goldens, figures.json, metadata.json and
submission.md.

    python3 task270/generator/build.py [--out <dir>] [--no-docs] [--quiet]"""
from __future__ import annotations

import hashlib
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K      # noqa: E402
import docs as DOC      # noqa: E402
import ops as O         # noqa: E402
import postprocess as PP  # noqa: E402
import records as R     # noqa: E402
import sheets as SH     # noqa: E402
import world as W       # noqa: E402

TASK = os.path.dirname(HERE)


def build(out, docs=True, quiet=False):
    t0 = time.time()
    say = (lambda *a: None) if quiet else (lambda *a: print(*a, flush=True))
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        os.remove(os.path.join(out, f))
    Wd = W.build()
    sim = O.simulate(Wd)
    R.number_incidents(sim)
    say("world and operations %.0fs" % (time.time() - t0))
    J = lambda f: os.path.join(out, f)
    n = K.write_csv(J(K.F_ADDR), ["uprn", "easting", "northing", "class_code", "output_area"], R.address_rows(Wd))
    say("addresses", n)
    K.write_csv(J(K.F_NODES), ["node_id", "easting", "northing"], R.node_rows(Wd))
    K.write_csv(J(K.F_LINKS), ["link_id", "from_node", "to_node", "road_class", "length_m", "drive_time_s", "one_way"],
                R.link_rows(Wd))
    n = K.write_csv(J(K.F_LOG), ["time_utc", "call_sign", "event", "status_code", "status", "off_run_reason",
                                 "incident_number", "easting", "northing", "speed_kmh"], R.log_rows(Wd, sim))
    say("resource log rows", n)
    n = K.write_csv(J(K.F_BOOK), ["booking_ref", "staff_number", "station_code", "available_from", "available_to",
                                  "entered"], R.booking_rows(Wd, sim))
    say("booking rows", n)
    inc = R.incident_rows(Wd, sim)
    n = K.write_csv(J(K.F_INC), ["incident_number", "call_time", "closed_time", "classification", "cause", "uprn",
                                 "easting", "northing", "output_area"], [r[:9] for r in inc])
    say("incident rows", n)
    SH.fleet(Wd, J(K.F_FLEET))
    SH.oa_lookup(Wd, J(K.F_OALOOK))
    SH.crew_register(Wd, sim, J(K.F_CREW))
    SH.codes(J(K.F_CODES))
    SH.population(Wd, J(K.F_POP))
    SH.establishment(Wd, sim, J(K.F_ESTAB))
    if docs:
        DOC.write_standard(J(K.F_STANDARD))
        DOC.write_policy(J(K.F_POLICY))
        DOC.write_cabinet(J(K.F_CABINET))
    normalize(out, docs)
    say("pack written %.0fs" % (time.time() - t0))
    return Wd, sim, inc


def normalize(out, docs=True):
    p = lambda f: os.path.join(out, f)
    owner = {K.F_FLEET: ("2026-12-30T16:20:00Z", "2027-01-12T09:05:00Z"),
             K.F_OALOOK: ("2023-03-21T10:00:00Z", "2023-03-21T10:00:00Z"),
             K.F_CREW: ("2026-01-05T08:40:00Z", "2027-01-12T09:12:00Z"),
             K.F_CODES: ("2024-03-14T11:30:00Z", "2024-03-14T11:30:00Z"),
             K.F_POP: ("2026-09-24T09:30:00Z", "2026-09-24T09:30:00Z"),
             K.F_ESTAB: ("2026-01-02T10:15:00Z", "2026-01-02T10:15:00Z")}
    for f, (c, m) in owner.items():
        PP.normalize_ooxml(p(f), K.SERVICE, K.SERVICE, c, m, excel=True, company=K.SERVICE)
    if docs:
        PP.normalize_pdf(p(K.F_STANDARD), b"D:20261102150000+00'00'", b"D:20261102150000+00'00'")
        PP.normalize_pdf(p(K.F_POLICY), b"D:20250318110000+00'00'", b"D:20250318110000+00'00'")
        PP.normalize_pdf(p(K.F_CABINET), b"D:20270213101500+00'00'", b"D:20270213101500+00'00'")


def goldens(task_dir, target):
    import deliver as DL
    import metadata as MD
    import writeup as WU
    golden = os.path.join(task_dir, "golden")
    fig = os.path.join(HERE, "figures.json")
    X, F = DL.main(target, golden, fig)
    PP.normalize_ooxml(os.path.join(golden, K.G_BOOK), K.PEOPLE["review"], K.PEOPLE["review"], "2027-02-17T09:10:00Z",
                       "2027-02-18T16:42:00Z", excel=True, company=K.SERVICE)
    WU.write(task_dir, F)
    MD.write(task_dir)
    return X, F


def cut_zip(root):
    import zipfile
    target = os.path.join(root, "target")
    zpath = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=(2027, 2, 16, 9, 30, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(target, f), "rb") as fh:
                z.writestr(zi, fh.read())
    return zpath


def digest(folder):
    h = hashlib.sha256()
    for f in sorted(os.listdir(folder)):
        h.update(f.encode())
        with open(os.path.join(folder, f), "rb") as fh:
            h.update(fh.read())
    return h.hexdigest()


def main(argv):
    out = os.path.join(TASK, "target")
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    build(out, docs="--no-docs" not in argv, quiet="--quiet" in argv)
    if "--out" not in argv:
        goldens(TASK, out)
        cut_zip(TASK)


if __name__ == "__main__":
    main(sys.argv[1:])
