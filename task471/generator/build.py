"""Build task471: the pack into <task>/target, the golden files into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder inside
the task compared byte for byte, and target.zip cut from the final build.

    python3 task471/generator/build.py              everything
    python3 task471/generator/build.py --out DIR    the pack only, into DIR
    python3 task471/generator/build.py --fast       one build with the checks, no second build or zip
"""
import argparse
import datetime as dt
import hashlib
import os
import shutil
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import pack as P         # noqa: E402
import world as W        # noqa: E402

TASK = os.path.dirname(HERE)
LOCAL = dt.timezone(dt.timedelta(hours=1))

PDF_STAMPS = {
    "regulation": (b"D:20260630102214+01'00'", b"D:20260630102214+01'00'"),
    "report": (b"D:20260917163008+01'00'", b"D:20260918090412+01'00'"),
    "layouts": (b"D:20260302111545+01'00'", b"D:20260302111545+01'00'"),
}
OOXML = {   # creator, last modified by, created, modified, company, excel
    "spec": (W.PEOPLE["ministry"], W.PEOPLE["ministry"], "2026-09-24T08:41:00Z", "2026-10-01T07:12:44Z",
             "%s, %s" % (W.MINISTRY, W.DIRECTORATE), False),
    "codes": ("Data Services", "Data Services", "2026-01-02T09:05:00Z", "2026-01-02T09:22:31Z", W.BUREAU, True),
    "pilot": (W.PEOPLE["method"], W.PEOPLE["method"], "2024-11-12T13:30:00Z", "2024-11-14T10:02:18Z", W.BUREAU, True),
}
AS_OF = {   # each file's date as its source dated it
    "register": "2026-01-05", "events": "2026-01-05", "sample": "2026-01-14", "visits": "2026-06-05",
    "sample_events": "2026-01-14", "messages": "2026-01-08", "acks": "2026-01-08", "nonres": "2026-01-05",
    "regulation": "2026-06-30", "report": "2026-09-18", "layouts": "2026-03-02", "spec": "2026-10-01",
    "codes": "2026-01-02", "countries": "2026-01-02", "pilot": "2024-11-14", "levy": "2026-02-10",
}


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    x = x or P.everything()
    n = {}
    n["register"] = P.write_register(f("register"), P.register_rows(x))
    n["events"] = P.write_csv(f("events"), P.EVENT_COLS, P.event_rows([p for c in sorted(W.CODES) for p in x["reg"][c]]))
    n["sample"] = P.write_csv(f("sample"), P.SAMPLE_COLS, P.sample_rows(x))
    n["visits"] = P.write_csv(f("visits"), P.VISIT_COLS, P.visit_rows(x))
    n["sample_events"] = P.write_csv(f("sample_events"), P.EVENT_COLS,
                                     P.event_rows(sorted(x["sample"], key=lambda p: p["audit_no"])))
    msgs, acks = P.message_rows(x)
    n["messages"] = P.write_csv(f("messages"), P.MESSAGE_COLS, msgs)
    n["acks"] = P.write_csv(f("acks"), P.ACK_COLS, acks)
    n["nonres"] = P.write_csv(f("nonres"), P.NONRES_COLS, P.nonres_rows(x))
    n["countries"] = P.write_csv(f("countries"), P.COUNTRY_COLS, P.country_rows())
    n["levy"] = P.write_csv(f("levy"), P.LEVY_COLS, P.levy_rows(x))
    national = {}
    for p in x["sample"]:
        national[p["result"]] = national.get(p["result"], 0) + 1
    for c in ("10", "11", "50", "20", "30", "40"):
        national.setdefault(c, 0)
    DC.write_regulation(f("regulation"))
    DC.write_report(f("report"), national)
    DC.write_layouts(f("layouts"))
    DC.write_spec(f("spec"))
    DC.write_codes(f("codes"))
    DC.write_pilot(f("pilot"))
    for k, (c, m) in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), c, m)
    for k, (cr, lb, c0, m0, co, xl) in OOXML.items():
        PP.normalize_ooxml(f(k), cr, lb, c0, m0, excel=xl, company=co)
    for i, k in enumerate(P.FILES):
        y, m, d = (int(v) for v in AS_OF[k].split("-"))
        ts = dt.datetime(y, m, d, 9 + (i * 7) % 8, (i * 13) % 60, tzinfo=LOCAL).timestamp()
        os.utime(f(k), (ts, ts))
    if not quiet:
        big = max(n, key=lambda k: n[k])
        print("pack: %d files, largest %s (%d rows)" % (len(P.FILES), P.FILES[big], n[big]))
    return n, x


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            t = dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(folder, name)), LOCAL)
            zi = zipfile.ZipInfo(name, date_time=(t.year, t.month, t.day, t.hour, t.minute, t.second))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, x=None, quiet=False):
    import golden as GO
    import metadata as MD
    import writeup as WU
    n, x = build(os.path.join(root, "target"), x=x, quiet=quiet)
    gdir = os.path.join(root, "golden")
    if os.path.exists(gdir):
        shutil.rmtree(gdir)
    fig = os.path.join(root, "generator", "figures.json")
    GO.main(os.path.join(root, "target"), gdir, fig)
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"), sorted(os.listdir(gdir)), n)
    WU.write(fig, os.path.join(root, "submission.md"))
    if not quiet:
        print("built %s: %d pack files, %d golden files" % (root, len(os.listdir(os.path.join(root, "target"))),
                                                           len(os.listdir(gdir))))
    return x


def main(fast=False):
    import tempfile
    import zipfile
    import checks as CK
    import verify as V
    x = everything(TASK)
    good = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), x=x,
                  meta_path=os.path.join(TASK, "metadata.json"), fig_path=os.path.join(HERE, "figures.json"))
    good &= bool(V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden")))
    if fast:
        if not good:
            raise SystemExit("checks failed")
        return
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        os.makedirs(os.path.join(tmp, "generator"))
        everything(tmp, quiet=True)
        same_t = digest(os.path.join(TASK, "target")) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        same = {fn: open(os.path.join(TASK, fn), "rb").read() == open(os.path.join(tmp, fn), "rb").read()
                for fn in ("metadata.json", "submission.md", os.path.join("generator", "figures.json"))}
        if not (same_t and same_g and all(same.values())):
            bad = [k for k, v in digest(os.path.join(TASK, "target")).items()
                   if digest(os.path.join(tmp, "target")).get(k) != v]
            badg = [k for k, v in digest(os.path.join(TASK, "golden")).items()
                    if digest(os.path.join(tmp, "golden")).get(k) != v]
            raise SystemExit("second build differs: target %s %s, golden %s %s, %s" % (same_t, bad, same_g, badg, same))
    finally:
        shutil.rmtree(tmp)
    print("two builds byte-identical: %d target files, %d golden files, metadata.json, submission.md, figures.json" % (
        len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden")))))
    zp = cut_zip(TASK)
    with zipfile.ZipFile(zp) as z:
        inside = {i.filename: hashlib.sha256(z.read(i.filename)).hexdigest() for i in z.infolist()}
    if inside != digest(os.path.join(TASK, "target")):
        raise SystemExit("target.zip differs from target/")
    print("target.zip cut from this build: %d files, each identical to target/ (sha256 %s)" % (
        len(inside), hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16]))
    if not good:
        raise SystemExit("checks failed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    ap.add_argument("--fast", action="store_true")
    args = ap.parse_args()
    if args.out:
        build(args.out)
        print("pack written to", args.out)
    else:
        main(fast=args.fast)
