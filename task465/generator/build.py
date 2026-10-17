"""Build task465: the pack into <task>/target, the goldens into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder inside
the task compared byte for byte, and target.zip cut from the final build.

    python3 task465/generator/build.py              everything
    python3 task465/generator/build.py --out DIR    the pack only, into DIR
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

import coop as C         # noqa: E402
import methods as M      # noqa: E402
import pack as P         # noqa: E402
import sim as S          # noqa: E402
import world as W        # noqa: E402

TASK = os.path.dirname(HERE)
CENTRAL = dt.timezone(dt.timedelta(hours=-6))
STAMP = dt.datetime(2026, 11, 2, 16, 25, tzinfo=CENTRAL)      # the folder as the risk manager assembled it


def world():
    x = S.world()
    cty, dist = S.current(x)
    x["terms"] = M.term_sheet(cty, x["pub"])
    x["members"] = C.roster()
    x["enrol"] = C.center_enrolment(C.enrolment(x["members"]), x["terms"], W.QUOTES)
    x["tickets"], x["transfers"] = C.tickets(x["members"], x)
    x["tickets"] = C.center_tickets(x["tickets"], x)
    x["prior"] = C.prior_covers(x)
    x["drought"] = C.drought_weeks(x)
    return x


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    x = x or world()
    n = {}
    n["pull24"] = P.write_csv(f("pull24"), P.EXPORT_COLS, P.export_rows(x, "old"))
    n["pull26"] = P.write_csv(f("pull26"), P.EXPORT_COLS, P.export_rows(x, "new"))
    n["enrol"] = P.write_csv(f("enrol"), P.ENROL_COLS, P.enrol_rows(x["enrol"]))
    n["tickets"] = P.write_csv(f("tickets"), P.TICKET_COLS, P.ticket_rows(x["tickets"]))
    n["transfers"] = P.write_csv(f("transfers"), P.TRANSFER_COLS, P.transfer_rows(x["transfers"]))
    n["drought"] = P.write_csv(f("drought"), P.DROUGHT_COLS, P.drought_rows(x["drought"]))
    P.quote_workbook(f("quotes"), x["terms"])
    P.roster_workbook(f("roster"), x["members"])
    P.prior_workbook(f("prior"), x["prior"])
    n["roster"] = len(x["members"])
    n["prior"] = len(x["prior"])
    DC.write_methods(f("methods"))
    DC.write_terms(f("terms"), x["terms"])
    DC.write_policy(f("policy"))
    DC.write_notice(f("notice"))
    n["dict"] = DC.write_dictionary(f("dict"))
    n["register"] = DC.write_register(f("register"), n)
    PP.normalize_ooxml(f("quotes"), "Quillfield Re", "Quillfield Re", "2026-10-09T14:20:00Z", "2026-10-14T16:02:41Z",
                       excel=True, company=W.REINSURER)
    PP.normalize_ooxml(f("roster"), "Member Services", "Member Services", "2019-02-11T15:00:00Z",
                       "2026-09-30T21:14:08Z", excel=True, company=W.ORG)
    PP.normalize_ooxml(f("prior"), W.PEOPLE["risk"], W.PEOPLE["risk"], "2026-10-05T19:40:00Z", "2026-10-06T14:31:52Z",
                       excel=True, company=W.ORG)
    PP.normalize_pdf(f("methods"), b"D:20260326100000-05'00'", b"D:20260326100000-05'00'")
    PP.normalize_pdf(f("terms"), b"D:20261014153000-05'00'", b"D:20261014153000-05'00'")
    PP.normalize_pdf(f("policy"), b"D:20260122090000-06'00'", b"D:20260122090000-06'00'")
    ts = STAMP.timestamp()
    for k in W.FILES:
        os.utime(f(k), (ts, ts))
    if not quiet:
        print("pack: %d files, largest %s (%d rows)" % (len(W.FILES), W.FILES["pull24"], n["pull24"]))
    return n, x


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2026, 11, 2, 16, 25, 0)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(name, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, quiet=False):
    import golden as GO
    import metadata as MD
    import postprocess as PP
    import writeup as WU
    n, x = build(os.path.join(root, "target"), quiet=quiet)
    gdir = os.path.join(root, "golden")
    if os.path.exists(gdir):
        shutil.rmtree(gdir)
    fig = os.path.join(root, "generator", "figures.json")
    GO.main(os.path.join(root, "target"), gdir, fig)
    PP.normalize_ooxml(os.path.join(gdir, W.GOLDEN["workbook"]), W.PEOPLE["risk"], W.PEOPLE["risk"],
                       "2026-11-03T14:05:00Z", "2026-11-09T22:48:16Z", excel=False, company=W.ORG)
    ts = dt.datetime(2026, 11, 9, 16, 48, tzinfo=CENTRAL).timestamp()
    for fn in os.listdir(gdir):
        os.utime(os.path.join(gdir, fn), (ts, ts))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"), n)
    WU.write(fig, os.path.join(root, "submission.md"))
    if not quiet:
        print("built %s: %d pack files, %d golden files" % (root, len(os.listdir(os.path.join(root, "target"))),
                                                           len(os.listdir(gdir))))
    return x


def main():
    import tempfile
    import zipfile
    import checks as CK
    import verify as V
    x = everything(TASK)
    good = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), x=x,
                  meta_path=os.path.join(TASK, "metadata.json"), fig_path=os.path.join(HERE, "figures.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
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
            raise SystemExit("second build differs: target %s %s, golden %s, %s" % (same_t, bad, same_g, same))
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
    args = ap.parse_args()
    if args.out:
        build(args.out)
        print("pack written to", args.out)
    else:
        main()
