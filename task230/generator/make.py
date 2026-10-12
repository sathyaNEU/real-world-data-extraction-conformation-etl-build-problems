"""Build the pack, run the checks, write the goldens, the owed figures and metadata.json, run the independent
verifier, rebuild into a scratch folder and require byte-identical output, then cut target.zip.

    python3 task230/generator/make.py            (full: two builds, the zip)
    python3 task230/generator/make.py --once     (one build, no zip)
"""
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as AN
import build as B
import checks as C
import golden as G
import pack as PK
import verify as V
import world as W

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMP = (2026, 10, 28, 9, 30, 0)

SOURCES = {
    "spine": "Capture platform first-pass verification log, shift-days 1 July to 30 September 2026",
    "edits": "Capture platform field edits on submitted first-pass screens, Q3 2026",
    "audit": "QA tool blind re-key audit of first-pass output, Q3 2026",
    "workforce": "HRMS export: employees, badge allocation and the Q3 queue rota",
    "streams": "Stream register",
    "plan": "November 2026 operating plan of record, version 3",
    "qcp": "Controlled procedure QCP-04 First-pass quality control, version 5.0",
    "schedules": "Client quality schedules extract, 2026",
    "pilot": "Hollings & Pryce pilot report, 6 October 2026",
    "sessions": "Second-pass workflow export, September 2026",
    "labour": "Second-pass labour planning note, revised 19 October 2026",
    "forms": "Form specifications: versions and key fields",
    "fc_kba": "Kessington Benefit Administrators volume forecast revisions for November 2026",
    "fc_us": "Northgate, Brightmoor and Harbison volume forecast revisions for November 2026",
    "fc_au": "Wattlebird Health and Coolabah volume forecast revisions, FY27 weeks, with the FY27 calendar",
    "fc_uk": "Whinfell Pet Cover and Thistlecombe Motor volume forecast revisions",
    "fc_hpy": "Hollings & Pryce volume forecast revisions in bundles",
    "ca_kba": "Kessington client audit findings, Q3 2026 deliveries",
    "ca_us": "Northgate, Brightmoor and Harbison client audit returns, Q3 2026",
    "ca_au": "Wattlebird and Coolabah client audit returns, Q3 2026",
    "ca_uk": "Whinfell and Thistlecombe partner portal audit export, Q3 2026",
    "manifests": "SFTP gateway delivery manifests, 25 June to 3 October 2026",
    "index": "SFTP gateway delivery index, one row per document delivered, 25 June to 3 October 2026",
    "ocr": "OCR engine confidence summary by stream, field and month, Q3 2026",
    "keys": "Desktop agent keystroke telemetry by badge and login date, Q3 2026",
    "notes": "MIS extract notes: data dictionary and provenance",
}


def rows_of(path):
    if path.endswith(".parquet"):
        import pyarrow.parquet as pq
        return pq.ParquetFile(path).metadata.num_rows
    if path.endswith(".csv"):
        return sum(1 for _ in open(path)) - 1
    return None


def answers(out):
    A = out["asks"]
    L = out["limits"]
    call = AN.designate(out["R"]["golden"], L)
    return dict(call=call, limits=L, hours=A["A"]["golden"], client_audit=A["C"]["golden"], chart_order=A["order"])


def figures(out, ans):
    """the figures the write-up owes, as it states them"""
    R = out["R"]
    L = out["limits"]
    Qr, sc = out["Qr"], out["sc"]
    q3 = {q: v for q, v in Qr.monthly_pool().items()}
    q3q = {}
    for q in ("D", "N"):
        f = Qr.scr[Qr.scr.queue == q].groupby("day").key_fields.sum()
        p = Qr.pool.xs(q, level="queue")
        q3q[q] = float((p * f).sum() / f.sum())
    nov = out["nov_rate"]
    fig = {
        "call": [W.SID[c] for c in ans["call"]],
        "q3_rate_pct": {q: f"{100 * v:.1f}" for q, v in q3q.items()},
        "nov_rate_pct": {q: f"{100 * v:.1f}" for q, v in nov.items()},
        "slope": f"{out['slope'][0]:.2f}",
        "ratio_over": "1.1",
        "ratio_under": "0.9",
        "ratio_golden": {W.SID[c]: f"{R['golden'][c] / L[c]:.2f}" for c in W.ORDER},
        "ratio_default": {W.SID[c]: f"{R['R1'][c] / L[c]:.2f}" for c in W.ORDER},
        "forecast": {W.SID[c]: f"{R['golden'][c]:.1f}" for c in W.ORDER},
        "limit": {W.SID[c]: (f"{L[c]:.2f}" if c == "D6" else f"{L[c]:.1f}") for c in W.ORDER},
        "hours": {W.SID[c]: f"{ans['hours'][c]:,}" for c in W.ORDER},
        "client_audit": {W.SID[c]: f"{v:.2f}" for c, v in ans["client_audit"].items()},
        "rates": {k: f"{v:.3f}" for k, v in out["asks"]["rates"][("document", "all")].items()},
        "leader": W.SID[ans["chart_order"][0]],
        "chart_order": [W.SID[c] for c in ans["chart_order"]],
        "heldout_ratio": f"{min(v for k, v in out['heldout'].items() if k != 'golden') / out['heldout']['golden']:.2f}",
    }
    with open(os.path.join(HERE, "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=1)
        fh.write("\n")
    return fig


def metadata(target):
    files = []
    for k, f in PK.FILES.items():
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[k], "date": "2026-10-28",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task230",
        "title": "Which client streams go on second-pass verification in November at an insurance-claims capture centre",
        "domain": "Human Factors & Ergonomics",
        "subdomain": "human reliability assessment (first-pass human verification of OCR-captured key fields)",
        "objective": "Data Quality Monitoring & Alerting",
        "prompt_shape": "07 (grid of cells): eleven client streams by the second-pass call, second-pass hours and the "
                        "client-audited third-quarter residual, plus a chart of the hours",
        "as_of": "2026-10-28",
        "deliverables": [G.WORKBOOK, G.SLIDE],
        "distractor_files": [PK.FILES[k] for k in PK.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task230/generator/make.py (seeded, deterministic) around a fictional "
                               "Kolkata claims-capture centre (Tamralipta Data Services) and fictional clients; no real person, "
                               "claimant, organisation or contract is depicted.",
                     "date": "2026-10-28", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-11",
        "generator": "task230/generator/make.py",
        "files": files,
    }
    with open(os.path.join(TASK, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")


def stamp(folder):
    t = dt.datetime(*STAMP, tzinfo=dt.timezone.utc).timestamp()
    for f in os.listdir(folder):
        os.utime(os.path.join(folder, f), (t, t))


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip():
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo(f, date_time=STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, f), "rb").read())
    return zp


def one(target, golden_dir):
    B.build(target)
    stamp(target)
    out = C.run(target)
    ans = answers(out)
    G.write(ans, golden_dir)
    stamp(golden_dir)
    return out, ans


def main(second=True):
    out, ans = one(TARGET, GOLDEN)
    fig = figures(out, ans)
    metadata(TARGET)
    V.main(TARGET, GOLDEN)
    n = len(out["checks"])
    print(f"checks: {n} passed")
    if os.environ.get("CHECKS_OUT"):
        with open(os.environ["CHECKS_OUT"], "w") as fh:
            json.dump(out["checks"], fh, indent=1)
    if second:
        tmp = tempfile.mkdtemp(dir=os.environ.get("TMPBUILD"))
        t2, g2 = os.path.join(tmp, "target"), os.path.join(tmp, "golden")
        B.build(t2)
        stamp(t2)
        G.write(ans, g2)
        stamp(g2)
        assert digest(TARGET) == digest(t2), [f for f in digest(TARGET) if digest(TARGET)[f] != digest(t2).get(f)]
        assert digest(GOLDEN) == digest(g2), "golden differs between builds"
        shutil.rmtree(tmp)
        zp = cut_zip()
        print("byte-identical; target.zip sha256", hashlib.sha256(open(zp, "rb").read()).hexdigest())
    return out, ans, fig


if __name__ == "__main__":
    main(second="--once" not in sys.argv)
