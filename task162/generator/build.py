"""Build task162: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
compared byte for byte (and deleted), then target.zip cut from the pack.

    python3 task162/generator/build.py              everything
    python3 task162/generator/build.py --out DIR    the pack only, into DIR"""
from __future__ import annotations

import argparse
import calendar
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C            # noqa: E402
import common as K          # noqa: E402
import docs as DOC          # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402
import sheets as SH         # noqa: E402
import world as W           # noqa: E402

TASK = os.path.dirname(HERE)
SCRATCH = os.environ.get("TASK162_SCRATCH", "/tmp")
PULL_DONE = (2026, 11, 2, 9, 41, 0)
MTIME = calendar.timegm((2026, 11, 2, 9, 41, 0, 0, 0, 0))


def commissioning():
    """Coldbeck's commissioning programme: the crews' route through the phase, one to three valves a week, none in the
    week of 15 February 2027 (the half-term shutdown)."""
    r = K.rng("commissioning")
    weeks = ["w/c 11 Jan 2027", "w/c 18 Jan 2027", "w/c 25 Jan 2027", "w/c 1 Feb 2027", "w/c 8 Feb 2027",
             "w/c 22 Feb 2027", "w/c 1 Mar 2027", "w/c 8 Mar 2027", "w/c 15 Mar 2027", "w/c 22 Mar 2027"]
    per = [1, 2, 3, 2, 3, 2, 2, 3, 2, 2]
    order = [W.PHASE3[i] for i in r.permutation(len(W.PHASE3))]
    out, i = {}, 0
    for w, n in zip(weeks, per):
        for c in order[i:i + n]:
            out[c] = w
        i += n
    assert len(out) == len(W.PHASE3)
    return out


COMMISSIONING = commissioning()


def n1_of(T):
    return {p["code"]: p["n1"] for p in T["P"]}


def settings_of(T):
    return {p["code"]: p["setting"] for p in T["P"] if p["phase"] == 3}


def build(out, quiet=False):
    os.makedirs(out, exist_ok=True)
    p = lambda f: os.path.join(out, f)
    T = W.simulate()
    n = {}
    F, inl, zon = R.logger_series(T)
    n[R.F_INLET] = K.write_csv(p(R.F_INLET), R.INLET_COLS, inl)
    n[R.F_ZONE] = K.write_csv(p(R.F_ZONE), R.ZONE_COLS, zon)
    n[R.F_LOGGERS] = K.write_csv(p(R.F_LOGGERS), R.LOGGER_COLS, R.logger_register_rows(F))
    n[R.F_DISTRICTS] = K.write_csv(p(R.F_DISTRICTS), R.DISTRICT_COLS, R.district_rows(T))
    n[R.F_CODES] = K.write_csv(p(R.F_CODES), R.CODE_COLS, R.CODE_HISTORY)
    props = R.properties(T)
    n[R.F_PROPS] = K.write_csv(p(R.F_PROPS), R.PROP_COLS, R.property_rows(props))
    bills = R.bills(T, props)
    n[R.F_BILLS] = K.write_csv(p(R.F_BILLS), R.BILL_COLS, bills)
    n[R.F_OUTLET] = K.write_csv(p(R.F_OUTLET), R.OUTLET_COLS, R.outlet_daily(T, bills))
    n[R.F_CONTACTS] = K.write_csv(p(R.F_CONTACTS), R.CONTACT_COLS, R.contact_rows(T))
    n[R.F_MILL] = K.write_csv(p(R.F_MILL), R.MILL_COLS, R.mill_rows(T))
    # documents
    N1, S = n1_of(T), settings_of(T)
    DOC.write_method(p(DOC.F_METHOD), [[x["code"], x["name"], x["n1"]] for x in T["P"]])
    DOC.write_schedule(p(DOC.F_SCHEDULE), [(x["code"], x["name"]) for x in T["P"] if x["phase"] == 3])
    DOC.write_certificate(p(DOC.F_CERT))
    DOC.write_note(p(DOC.F_NOTE))
    # the assessment export and the valve schedule, computed from the written records
    P = C.Pack(out, N1, S)
    monthly, yearly, vrows = [], [], []
    names = {x["code"]: x["name"] for x in T["P"]}
    for code in W.PHASE3:
        m, t, ok = P.assess(code)
        hh = P.households_by_day(code)
        nhh = P.households_by_day(code, cls="non-household")
        for mi, mo in enumerate(K.MONTHS):
            sel = P.month_mask(mi, ok)
            monthly.append([code, mo.strftime("%Y-%m"), int(sel.sum()), float(hh[sel].mean()), float(nhh[sel].mean()),
                            float(t["mnf"][sel].mean()), float(t["allow"][sel].mean()), float(t["nnf"][sel].mean()),
                            float(t["aznp"][sel].mean()), float(t["ndf"][sel].mean()), float(m[mi])])
        yearly.append([code, names[code], float(m.mean())])
        pin_n = P.pin[code][ok, K.NIGHT_HOUR]
        az_n = P.azp[code][ok, K.NIGHT_HOUR]
        after = float(np.mean(az_n - (pin_n - np.minimum(pin_n, S[code]))))
        peak = float(np.nanpercentile(P.flow[code], 99.5))
        size = 80 if peak < 9 else 100 if peak < 15 else 150 if peak < 30 else 200
        vrows.append([code, names[code], size, int(S[code]), float(np.mean(az_n)), after, COMMISSIONING[code]])
    SH.write_export(p(R.F_EXPORT), monthly, yearly)
    n[R.F_EXPORT] = len(monthly)
    SH.write_valves(p(DOC.F_VALVES), vrows)
    n[DOC.F_VALVES] = len(vrows)
    normalize(out)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    if not quiet:
        for f in sorted(os.listdir(out)):
            print("  %-48s %10d bytes %s" % (f, os.path.getsize(os.path.join(out, f)), ("%d rows" % n[f]) if f in n else ""))
    return T, n


def normalize(out):
    p = lambda f: os.path.join(out, f)
    PP.normalize_ooxml(p(R.F_EXPORT), K.PEOPLE["leakage"], K.PEOPLE["leakage"], "2026-05-14T08:12:00Z",
                       "2026-05-14T08:31:00Z", excel=True, company=K.COMPANY)
    PP.normalize_ooxml(p(DOC.F_VALVES), K.PEOPLE["modeller"], K.PEOPLE["modeller"], "2026-08-11T10:02:00Z",
                       "2026-10-09T15:47:00Z", excel=True, company=K.PARTNER)
    PP.normalize_pdf(p(DOC.F_METHOD), b"D:20250320101500+00'00'", b"D:20250320101500+00'00'")
    PP.normalize_pdf(p(DOC.F_SCHEDULE), b"D:20260902163000+01'00'", b"D:20260902163000+01'00'")
    PP.normalize_pdf(p(DOC.F_CERT), b"D:20251114112000+00'00'", b"D:20251114112000+00'00'")


def digest(folder):
    h = {}
    for root, _, files in os.walk(folder):
        for f in sorted(files):
            fp = os.path.join(root, f)
            h[os.path.relpath(fp, folder)] = hashlib.sha256(open(fp, "rb").read()).hexdigest()
    return h


def cut_zip(root):
    target = os.path.join(root, "target")
    zpath = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=PULL_DONE)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    return zpath


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--no-rebuild", action="store_true")
    a = ap.parse_args()
    if a.out:
        build(a.out)
        return
    target = os.path.join(TASK, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    T, n = build(target)
    import deliver
    deliver.main(target, os.path.join(TASK, "golden"), os.path.join(HERE, "figures.json"))
    import metadata
    metadata.write(TASK)
    r1 = subprocess.run([sys.executable, os.path.join(HERE, "checks.py")])
    r2 = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), target])
    same = same_g = same_f = True
    if not a.no_rebuild:
        tmp = tempfile.mkdtemp(prefix="b162_", dir=SCRATCH)
        try:
            build(os.path.join(tmp, "target"), quiet=True)
            deliver.main(os.path.join(tmp, "target"), os.path.join(tmp, "golden"), os.path.join(tmp, "figures.json"))
            same = digest(target) == digest(os.path.join(tmp, "target"))
            same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
            same_f = open(os.path.join(HERE, "figures.json"), "rb").read() == open(os.path.join(tmp, "figures.json"), "rb").read()
            print("rebuild byte-identical: target %s, golden %s, figures %s" % (same, same_g, same_f))
        finally:
            shutil.rmtree(tmp)
    z = cut_zip(TASK)
    print("zip", z, hashlib.sha256(open(z, "rb").read()).hexdigest())
    if r1.returncode or r2.returncode or not (same and same_g and same_f):
        sys.exit(1)


if __name__ == "__main__":
    main()
