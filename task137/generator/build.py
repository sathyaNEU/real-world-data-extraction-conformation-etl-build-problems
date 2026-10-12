"""Build task137: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the pack.

    python3 task137/generator/build.py              everything
    python3 task137/generator/build.py --out DIR    the pack only, into DIR"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import book as B           # noqa: E402
import docs as DOC         # noqa: E402
import pack as PK          # noqa: E402
import postprocess as PP   # noqa: E402
import sim as S            # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)


def outlook_rows(H):
    """The treasury's monthly term deposit outlook (NZ$ millions): actuals to September 2026, forecast after."""
    r = W.rng("outlook")
    months = ["Apr-26", "May-26", "Jun-26", "Jul-26", "Aug-26", "Sep-26", "Oct-26", "Nov-26", "Dec-26", "Jan-27",
              "Feb-27", "Mar-27"]
    bal = 7412.6
    out = []
    for k, m in enumerate(months):
        mat = round(float(r.uniform(560, 760)) + (210 if m in ("Jan-27", "Feb-27", "Mar-27") else 0), 1)
        if k < 6:
            rein = round(mat * float(r.uniform(0.79, 0.86)), 1)
            basis = "Actual"
        else:
            rein = round(mat * 0.82, 1)
            basis = "Forecast"
        new = round(float(r.uniform(95, 180)), 1)
        close = round(bal + new - mat + rein, 1)
        out.append((m, (round(bal, 1), new, mat, rein, close, basis)))
        bal = close
    return out


def simulate():
    Wd = S.simulate()
    H = B.build_book(Wd)
    return Wd, H


def build(out, quiet=False, state=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda f: os.path.join(out, f)
    Wd, H = state or simulate()
    counts = {}
    counts[W.F_LIST_FWD] = W.write_csv(p(W.F_LIST_FWD), PK.LISTS_2026_COLS, PK.list_fwd_rows(Wd))
    counts[W.F_LISTS_2025] = W.write_csv(p(W.F_LISTS_2025), PK.LISTS_2025_COLS, PK.lists_2025_rows(Wd), crlf=True)
    counts[W.F_LISTS_2026] = W.write_csv(p(W.F_LISTS_2026), PK.LISTS_2026_COLS, PK.lists_2026_rows(Wd))
    counts[W.F_RELEASE] = W.write_csv(p(W.F_RELEASE), PK.RELEASE_COLS, PK.release_rows(Wd))
    counts[W.F_DIALS] = W.write_csv(p(W.F_DIALS), PK.DIAL_COLS, PK.dial_rows(Wd))
    counts[W.F_CLOSEOUT] = W.write_csv(p(W.F_CLOSEOUT), PK.CLOSE_COLS, PK.closeout_rows(Wd))
    counts[W.F_CONTACTS] = W.write_csv(p(W.F_CONTACTS), PK.CONTACT_COLS, PK.contact_rows(Wd))
    counts[W.F_DNC] = W.write_csv(p(W.F_DNC), PK.DNC_COLS, PK.dnc_rows(Wd))
    counts[W.F_EVENTS] = W.write_csv(p(W.F_EVENTS), PK.EVENT_COLS, PK.event_rows(Wd))
    counts[W.F_TRANSFERS] = W.write_csv(p(W.F_TRANSFERS), PK.TRANSFER_COLS, PK.transfer_rows(Wd))
    counts[W.F_HOLDINGS] = W.write_csv(p(W.F_HOLDINGS), PK.HOLD_COLS, PK.holdings_rows(H))
    counts[W.F_KIP] = W.write_csv(p(W.F_KIP), PK.KIP_COLS, PK.kip_rows(H), crlf=True)
    counts[W.F_BATCHES] = W.write_csv(p(W.F_BATCHES), PK.BATCH_COLS, PK.batch_rows(H))
    issued = {"2025Q1": "2024-11-18", "2025Q2": "2025-02-17", "2025Q3": "2025-05-19", "2025Q4": "2025-08-18",
              "2026Q1": "2025-11-17", "2026Q2": "2026-02-16", "2026Q3": "2026-05-18", "2027Q1": "2026-11-03"}
    import datetime as dt
    for q in W.PAST + [W.FWD]:
        n = len(Wd.campaigns[q]["listed"])
        DOC.write_brief(p(W.brief_name(q)), q, n, dt.date.fromisoformat(issued[q]), draft=(q == W.FWD))
    DOC.write_sow(p(W.F_SOW))
    DOC.write_proposal(p(W.F_PROPOSAL))
    DOC.write_procedure(p(W.F_PROCEDURE))
    DOC.write_thread(p(W.F_THREAD))
    DOC.write_notes(p(W.F_NOTES))
    DOC.write_outlook(p(W.F_OUTLOOK), outlook_rows(H))
    # containers true to the fiction
    PP.normalize_ooxml(p(W.F_PROCEDURE), W.PEOPLE["product"], W.PEOPLE["product"], "2026-07-21T22:14:03Z",
                       "2026-08-02T21:40:51Z", title="Term Deposit Retention Procedure v4")
    PP.normalize_ooxml(p(W.F_OUTLOOK), W.PEOPLE["treasury"], W.PEOPLE["treasury"], "2026-04-14T03:22:10Z",
                       "2026-10-26T23:57:36Z", excel=True)
    stamps = {"2025Q1": ("20241118101422", "20241118101907"), "2025Q2": ("20250217093310", "20250217094102"),
              "2025Q3": ("20250519111502", "20250519112230"), "2025Q4": ("20250818100941", "20250818101528"),
              "2026Q1": ("20251117095518", "20251117100344"), "2026Q2": ("20260216104026", "20260216104811"),
              "2026Q3": ("20260518093147", "20260518093902"), "2027Q1": ("20261103141209", "20261103142755")}
    for q, (c, m) in stamps.items():
        tz = b"+13'00'" if (q[-1] in "14" or q in ("2026Q1",)) else b"+12'00'"
        PP.normalize_pdf(p(W.brief_name(q)), b"D:" + c.encode() + tz, b"D:" + m.encode() + tz)
    PP.normalize_pdf(p(W.F_SOW), b"D:20241121163005+13'00'", b"D:20241122094418+13'00'")
    PP.normalize_pdf(p(W.F_PROPOSAL), b"D:20261008154012+13'00'", b"D:20261009090551+13'00'")
    stamp = W.EXPORT_STAMP.timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)),
                                          ", ".join("%s %d" % kv for kv in counts.items())))
    return Wd, H, counts


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest()
            for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    when = W.EXPORT_STAMP.timetuple()[:6]
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
    import golden as GD
    state = simulate()
    Wd, H, counts = build(os.path.join(root, "target"), quiet=quiet, state=state)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    GD.main(os.path.join(root, "target"), os.path.join(root, "golden"), os.path.join(root, "generator", "figures.json"),
            os.path.join(root, "metadata.json"))
    return Wd, H, counts


def main():
    import checks as CK
    import verify as V
    Wd, H, counts = everything(TASK)
    import writeup as WU
    WU.main(os.path.join(TASK, "generator", "figures.json"), os.path.join(TASK, "submission.md"))
    CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), Wd=Wd, H=H,
           meta_path=os.path.join(TASK, "metadata.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        os.makedirs(os.path.join(tmp, "generator"))
        everything(tmp, quiet=True)
        same_t = digest(os.path.join(TASK, "target")) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        same = {}
        for f in ("metadata.json", os.path.join("generator", "figures.json")):
            same[f] = open(os.path.join(TASK, f), "rb").read() == open(os.path.join(tmp, f), "rb").read()
        same["target.zip"] = open(cut_zip(TASK), "rb").read() == open(cut_zip(tmp), "rb").read()
        if not (same_t and same_g and all(same.values())):
            raise SystemExit("second build differs: target %s, golden %s, %s" % (same_t, same_g, same))
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
