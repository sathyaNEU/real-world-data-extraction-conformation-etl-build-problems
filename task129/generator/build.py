"""task129 generator: build the evidence pack.

    python3 task129/generator/build.py [--out DIR] [--record FILE]

Writes DIR/target/ and DIR/metadata.json (DIR defaults to the task folder), asserts every check in
checks.py on the files as written, scrubs container metadata, normalises mtimes, and fails loudly
at the first assertion that does not hold."""
import argparse
import json
import os
import shutil
import sys
from datetime import datetime

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, ".claude", "skills", "reduce-house-fixes", "scripts"))

import params as P          # noqa: E402
import spine                # noqa: E402
import ship                 # noqa: E402
import docs                 # noqa: E402
import cdn                  # noqa: E402
import golden as G          # noqa: E402
from golden import F        # noqa: E402

PRODUCER = "Sonderaa Medier Digital"

# in-fiction write time of each file (local)
MTIME = {
    "spine": "2026-09-05 06:40", "release": "2026-09-04 17:02", "rollout": "2026-08-04 09:12",
    "changes": "2026-09-04 16:20", "registry": "2026-09-01 08:30", "subs": "2026-09-05 06:55",
    "editions": "2026-03-16 10:05", "sla": "2025-12-10 14:30", "paywall": "2026-01-05 09:00",
    "closeout": "2026-09-04 11:05", "crawl": "2026-08-19 07:48", "crawlcfg": "2026-06-01 12:10",
    "assets": "2026-08-04 15:30", "roster": "2026-02-03 09:40", "cdn": "2026-09-02 05:15",
    "cdnapp": "2026-06-12 13:20", "guide": "2026-09-04 15:42", "thread": "2026-09-02 11:03",
    "manifest": "2026-09-05 07:10", "desktop": "2026-09-04 11:20", "amp": "2026-09-03 10:00",
    "news": "2026-09-01 07:00",
}
PDF_STAMP = {"sla": "2025-12-10", "paywall": "2026-01-05", "cdnapp": "2026-06-12"}


def rngk(k):
    return np.random.default_rng([P.SEED, k])


def write_pack(out):
    tgt = os.path.join(out, "target")
    if os.path.isdir(tgt):
        shutil.rmtree(tgt)
    os.makedirs(tgt)
    p = lambda k: os.path.join(tgt, F[k])
    R = spine.build(np.random.default_rng(P.SEED))
    ship.spine(R["S"], p("spine"))
    ship.registry(p("registry"))
    ship.editions(p("editions"))
    rel = ship.release_log(rngk(1), R["dep"], p("release"))
    ship.rollout_log(rel, p("rollout"))
    ship.subscriptions(rngk(2), R["dev"], p("subs"))
    ship.change_register(rel, p("changes"))
    L0 = {"spine": pd.read_parquet(p("spine"))}
    for k in ["release", "registry", "subs", "editions"]:
        L0[k] = pd.read_csv(p(k), keep_default_na=False, dtype=str)
    v = G.views(L0)
    ship.closeout(ship.closeout_table(v), p("closeout"))
    ship.crawl_files(rngk(3), tgt)
    daily = v.groupby(v.day.dt.date).w.sum()
    ship.cdn_file(cdn.delivery_log(rngk(4), daily), p("cdn"))
    ship.roster(rngk(5), p("roster"))
    docs.service_level(p("sla"))
    docs.paywall(p("paywall"))
    docs.vendor_appendix(p("cdnapp"))
    docs.field_guide(p("guide"))
    docs.thread(p("thread"))
    docs.desktop_summary(rngk(6), p("desktop"))
    docs.amp_report(rngk(7), p("amp"))
    docs.newsletter_sends(rngk(8), p("news"))
    names = [F[k] for k in F]
    docs.manifest(p("manifest"), names)
    scrub(tgt)
    return tgt, R


def scrub(tgt):
    import scrub_producer_metadata as S
    for k, stamp in PDF_STAMP.items():
        S.scrub_pdf(os.path.join(tgt, F[k]), PRODUCER, stamp, floor="2025-11-01",
                    ceiling="2026-09-07")


def set_mtimes(tgt):
    for k, when in MTIME.items():
        ts = pd.Timestamp(when).tz_localize(P.TZ).timestamp()
        os.utime(os.path.join(tgt, F[k]), (ts, ts))


def metadata(out, tgt):
    files = []
    fmts = set()
    biggest, rows = None, 0
    for name in sorted(os.listdir(tgt)):
        ext = name.rsplit(".", 1)[1]
        fmts.add(ext)
        path = os.path.join(tgt, name)
        n = None
        if ext == "parquet":
            import pyarrow.parquet as pq
            n = pq.ParquetFile(path).metadata.num_rows
        elif ext == "csv":
            n = sum(1 for _ in open(path, encoding="utf-8")) - 1
        if n and n > rows:
            biggest, rows = name, n
        files.append({"path": name, "format": ext, "bytes": os.path.getsize(path), "rows": n,
                      "source": "Constructed for this task: fictional regional news group "
                                "Sønderå Medier; no third-party data",
                      "date": "2026-09-05", "license": "CC0-1.0 (original work)"})
    meta = {
        "task": "task129",
        "title": "Which shipped change the operations squad fixes in Q4",
        "domain": "Business & Operations Analytics",
        "subdomain": "service-operations-sla",
        "objective": "Root-Cause Analysis",
        "prompt_shape": "11 (before and after with a control)",
        "as_of": P.AS_OF.isoformat(),
        "deliverables": ["q4_squad_call.pptx", "q4_squad_call_cohort_effects.xlsx"],
        "distractor_files": [F[k] for k in G.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted(fmts), "largest_file": biggest,
                        "largest_file_rows": rows},
        "files": files,
    }
    with open(os.path.join(out, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
        f.write("\n")
    return meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.abspath(os.path.join(HERE, "..")))
    ap.add_argument("--record", default=None)
    ap.add_argument("--no-checks", action="store_true")
    a = ap.parse_args()
    tgt, R = write_pack(a.out)
    meta = metadata(a.out, tgt)
    if not a.no_checks:
        import checks
        rec = checks.run(a.out, tgt, R, meta)
        if a.record:
            with open(a.record, "w") as f:
                json.dump(rec, f, indent=1, default=str)
    set_mtimes(tgt)
    print("build ok:", tgt)


if __name__ == "__main__":
    main()
