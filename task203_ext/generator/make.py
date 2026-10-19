"""Build task203_ext/target/: a raw, unconformed benchmark-evaluation corpus.

This is a dataset drop, not a task. There is no prompt, no golden, no design note and no
fingerprint card, and nothing in here is designed to be got wrong: no decisive step, no ladder, no
devices aimed at a wrong answer, no planted defect, no decoy, no withheld rule.

What it is: the raw exports a small applied-ML evaluation group would actually hold after two years
of benchmark sweeps. It is unconformed on purpose, in the sense that nobody has conformed it yet,
and every one of those rough edges is listed in target/MANIFEST.md rather than hidden. The point is
that a later reader can conform it themselves; the point is not that they will trip over anything.

Deterministic: one seed, no clock reads, so two runs are byte-identical.

    python3 -I generator/make.py        # from the task203_ext directory
"""

import csv
import hashlib
import zipfile
import json
import random
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "target"
SEED = 20261019

# ----------------------------------------------------------------- the world

GROUP = "Benchmark & Evaluation Group, Institute for Applied Computation"
SHORT = "BEG"

USERS = ["a.okonkwo", "r.vasquez", "m.lindqvist", "t.haruna", "p.dubois",
         "s.mehta", "beg-ci", "beg-nightly", "k.oyelaran", "j.farkas"]

MODELS = [
    ("mdl-aurora-base", "aurora", "base", 1.3),
    ("mdl-aurora-wide", "aurora", "wide", 3.1),
    ("mdl-aurora-deep", "aurora", "deep", 6.8),
    ("mdl-tessel-s", "tessel", "s", 0.4),
    ("mdl-tessel-m", "tessel", "m", 1.1),
    ("mdl-tessel-l", "tessel", "l", 2.9),
    ("mdl-corvid-7", "corvid", "7", 7.2),
    ("mdl-corvid-13", "corvid", "13", 13.4),
    ("mdl-pellan-mix", "pellan", "mix", 4.5),
]

# task_type decides which metric keys a run carries, which is why the metrics object is
# heterogeneous in the raw export. Nothing hinges on it; it is just how the tracker stores runs.
DATASETS = [
    ("ds-clf-newswire", "classification", ["accuracy", "macro_f1", "loss"]),
    ("ds-clf-reviews", "classification", ["accuracy", "macro_f1", "loss"]),
    ("ds-clf-intents", "classification", ["accuracy", "macro_f1", "loss"]),
    ("ds-gen-summaries", "generation", ["rouge_l", "bleu", "loss"]),
    ("ds-gen-dialogue", "generation", ["rouge_l", "bleu", "loss"]),
    ("ds-rank-passages", "ranking", ["ndcg_10", "mrr", "loss"]),
    ("ds-rank-products", "ranking", ["ndcg_10", "mrr", "loss"]),
    ("ds-reg-demand", "regression", ["rmse", "mae", "r2"]),
    ("ds-tab-credit", "tabular", ["accuracy", "auroc", "loss"]),
    ("ds-tab-churn", "tabular", ["accuracy", "auroc", "loss"]),
]

# Host names are written three ways across the corpus because three systems wrote them, which is
# the ordinary state of a raw export.
HOSTS_CANON = ["gpu-node-01", "gpu-node-02", "gpu-node-03", "gpu-node-04", "gpu-node-05",
               "gpu-node-06", "gpu-node-07", "gpu-node-08", "cpu-node-01", "cpu-node-02"]

GPU_BY_HOST = {
    "gpu-node-01": "A40", "gpu-node-02": "A40", "gpu-node-03": "A40", "gpu-node-04": "L40S",
    "gpu-node-05": "L40S", "gpu-node-06": "L40S", "gpu-node-07": "H100", "gpu-node-08": "H100",
    "cpu-node-01": None, "cpu-node-02": None,
}

DATASET_VERSIONS = {
    "ds-clf-newswire": ["v1.2", "v1.3", "1.3.0"],
    "ds-clf-reviews": ["v2.0", "2.0.1"],
    "ds-clf-intents": ["v1.0"],
    "ds-gen-summaries": ["2025-11-rev1", "2026-03-rev2"],
    "ds-gen-dialogue": ["v0.9", "v1.0"],
    "ds-rank-passages": ["v3.1", "3.1.0", "v3.2"],
    "ds-rank-products": ["v1.1"],
    "ds-reg-demand": ["2025-09", "2026-02"],
    "ds-tab-credit": ["v4.0", "v4.1"],
    "ds-tab-churn": ["v1.0", "v1.1"],
}

SWEEPS = [
    ("sweep_aurora_lr_2026q1", "aurora", "learning rate and warmup", 2026, 1),
    ("sweep_tessel_width_2026q2", "tessel", "width and depth trade-off", 2026, 2),
    ("sweep_corvid_ctx_2026q3", "corvid", "context length", 2026, 3),
    ("sweep_mixed_seeds_2026q4", "all", "seed variance at fixed config", 2026, 4),
]


def host_as_written(rng, canon):
    """The same host, written the way one of three systems writes it."""
    r = rng.random()
    if r < 0.70:
        return canon
    if r < 0.88:
        return canon.upper()
    return canon + ".beg.internal"


def cfg_sha(model_id, dataset_id, seed, lr, bs):
    raw = "%s|%s|%d|%.6f|%d" % (model_id, dataset_id, seed, lr, bs)
    return hashlib.sha1(raw.encode()).hexdigest()[:12]


def metric_values(rng, dataset_id, keys, params_b, lr):
    """Plausible metric values. Scale helps a little, learning rate has an interior optimum.

    No relationship here is a trap. It is just enough structure that the corpus is not noise.
    """
    size_term = 0.055 * (params_b ** 0.5)
    lr_term = -0.9 * (abs(lr - 0.00025) / 0.00025) ** 1.5 * 0.02
    base = {"classification": 0.74, "generation": 0.31, "ranking": 0.52,
            "regression": 0.0, "tabular": 0.79}
    kind = next(k for d, k, _ in DATASETS if d == dataset_id)
    out = {}
    if kind == "regression":
        rmse = max(0.4, 3.1 - size_term * 2.0 - lr_term * 8 + rng.gauss(0, 0.11))
        out["rmse"] = round(rmse, 4)
        out["mae"] = round(rmse * rng.uniform(0.70, 0.80), 4)
        out["r2"] = round(max(0.0, min(0.99, 1.0 - (rmse / 3.6) ** 2 + rng.gauss(0, 0.012))), 4)
        return out
    centre = min(0.97, base[kind] + size_term + lr_term + rng.gauss(0, 0.014))
    for k in keys:
        if k == "loss":
            out[k] = round(max(0.08, 2.4 - 1.9 * centre + rng.gauss(0, 0.05)), 4)
        elif k in ("macro_f1", "mrr"):
            out[k] = round(max(0.0, min(0.995, centre - rng.uniform(0.01, 0.05))), 4)
        elif k == "auroc":
            out[k] = round(max(0.5, min(0.998, centre + rng.uniform(0.05, 0.11))), 4)
        elif k == "bleu":
            out[k] = round(max(0.0, centre * rng.uniform(0.55, 0.72)), 4)
        else:
            out[k] = round(max(0.0, min(0.995, centre)), 4)
    return out


def build_runs(rng, year, n):
    """One run record per sweep trial, in the tracker's own internal shape."""
    runs = []
    start = datetime(year, 1, 6, 7, 0, tzinfo=timezone.utc)
    for i in range(n):
        model_id, family, variant, params_b = rng.choice(MODELS)
        dataset_id, kind, keys = rng.choice(DATASETS)
        seed = rng.choice([0, 1, 2, 3, 7, 11, 13, 17, 42, 101, 1234, 2026])
        lr = rng.choice([5e-5, 1e-4, 2e-4, 2.5e-4, 3e-4, 5e-4, 1e-3])
        bs = rng.choice([8, 16, 32, 64, 128])
        host = rng.choice(HOSTS_CANON)
        offset = timedelta(minutes=rng.randint(0, 525000))
        submitted = start + offset
        queue_min = rng.choice([0, 1, 2, 4, 7, 15, 31, 64, 140])
        began = submitted + timedelta(minutes=queue_min)
        dur_min = max(3, int(rng.gauss(42 + params_b * 11, 18)))
        finished = began + timedelta(minutes=dur_min)

        r = rng.random()
        if r < 0.031:
            status = rng.choice(["crashed", "oom", "killed"])
        elif r < 0.047:
            status = "running"
        else:
            status = "completed"

        rec = {
            "run_id": "%s-%d-%06d" % (SHORT.lower(), year, i + 1),
            "submitted_at": submitted.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "started_at": began.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "finished_at": None if status == "running" else finished.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "submitted_by": rng.choice(USERS),
            "model_id": model_id,
            "model_family": family,
            "model_revision": "r%d" % rng.randint(1, 9),
            "params_b": params_b,
            "dataset_id": dataset_id,
            "dataset_version": rng.choice(DATASET_VERSIONS[dataset_id]),
            "task_type": kind,
            "seed": seed,
            "hyperparams": {"learning_rate": lr, "batch_size": bs,
                            "warmup_steps": rng.choice([0, 100, 500, 1000]),
                            "epochs": rng.choice([1, 2, 3, 5])},
            "config_sha": cfg_sha(model_id, dataset_id, seed, lr, bs),
            "status": status,
            "host": host_as_written(rng, host),
            "gpu_hours": None if status in ("crashed", "oom", "killed", "running")
                         else round(dur_min / 60.0 * (1 if GPU_BY_HOST[host] else 0), 3),
            "metrics": {} if status != "completed" else metric_values(rng, dataset_id, keys, params_b, lr),
        }
        if rng.random() < 0.06:
            rec["notes"] = rng.choice([
                "rerun after scheduler restart", "shared node, timings not comparable",
                "config copied from previous sweep", "eval harness v2", "manual submission",
            ])
        runs.append(rec)
    return runs


def write_jsonl(path, records):
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for r in records:
            fh.write(json.dumps(r, separators=(",", ":"), sort_keys=True) + "\n")


def write_2025_csv(path, runs):
    """The 2025 export, in the layout the tracker used before the 2026 schema change.

    Different column names, a different order, local wall-clock timestamps with no zone, and the
    metrics flattened into three fixed columns that only fit classification and tabular runs.
    """
    cols = ["id", "ts_start", "ts_end", "who", "model", "rev", "data", "data_ver", "rng",
            "kind", "cfg", "state", "metric_a", "metric_b", "loss", "node", "gpu_h"]
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in runs:
            m = r["metrics"]
            keys = [k for k in m if k != "loss"]
            a = m.get(keys[0]) if keys else ""
            b = m.get(keys[1]) if len(keys) > 1 else ""
            # local wall clock, Europe/Helsinki in winter is UTC+2; written without a zone, as the
            # old exporter wrote it
            st = datetime.strptime(r["started_at"], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=2)
            en = (datetime.strptime(r["finished_at"], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=2)
                  if r["finished_at"] else None)
            w.writerow([
                r["run_id"], st.strftime("%Y-%m-%d %H:%M:%S"),
                en.strftime("%Y-%m-%d %H:%M:%S") if en else "",
                r["submitted_by"], r["model_id"], r["model_revision"], r["dataset_id"],
                r["dataset_version"], r["seed"], r["task_type"], r["config_sha"], r["status"],
                a, b, m.get("loss", ""), r["host"],
                "" if r["gpu_hours"] is None else r["gpu_hours"],
            ])


def write_sweep_configs(outdir, rng):
    outdir.mkdir(parents=True, exist_ok=True)
    for name, family, what, year, q in SWEEPS:
        lines = [
            "# %s" % name,
            "# %s sweep over %s" % (family, what),
            "",
            "[sweep]",
            'name = "%s"' % name,
            'family = "%s"' % family,
            'quarter = "%dQ%d"' % (year, q),
            'harness = "beg-eval %s"' % rng.choice(["1.4.2", "1.5.0", "2.0.0"]),
            "",
            "[grid]",
            "learning_rate = [5e-05, 0.0001, 0.0002, 0.00025, 0.0003, 0.0005, 0.001]",
            "batch_size = [8, 16, 32, 64, 128]",
            "seed = [0, 1, 2, 3, 7, 11, 13, 17, 42, 101, 1234, 2026]",
            "",
            "[resources]",
            'partition = "%s"' % rng.choice(["gpu-short", "gpu-long", "mixed"]),
            "max_parallel = %d" % rng.choice([4, 6, 8, 12]),
            "timeout_minutes = %d" % rng.choice([120, 240, 480]),
        ]
        (outdir / (name + ".toml")).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_metrics_dictionary(path):
    """Partial, as a real dictionary is: it documents what someone got round to documenting."""
    rows = [
        ("accuracy", "classification, tabular", "fraction of examples with the predicted label equal to the reference label", "0 to 1"),
        ("macro_f1", "classification", "unweighted mean of the per-class F1 scores", "0 to 1"),
        ("auroc", "tabular", "area under the receiver operating characteristic curve", "0.5 to 1"),
        ("loss", "all except regression", "mean evaluation loss on the held-out split", "0 and up"),
        ("rouge_l", "generation", "longest common subsequence overlap with the reference", "0 to 1"),
        ("ndcg_10", "ranking", "normalised discounted cumulative gain at rank 10", "0 to 1"),
        ("rmse", "regression", "root mean squared error in the target's own units", "0 and up"),
        ("r2", "regression", "coefficient of determination against the held-out mean", "up to 1"),
    ]
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["metric_key", "applies_to", "definition", "range"])
        w.writerows(rows)


def write_dataset_registry(path, rng):
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["dataset_id", "task_type", "versions_in_use", "eval_split_rows",
                    "licence", "registered_on"])
        for ds, kind, _ in DATASETS:
            w.writerow([ds, kind, ";".join(DATASET_VERSIONS[ds]),
                        rng.choice([1200, 2500, 4000, 5000, 8000, 12000]),
                        rng.choice(["CC-BY-4.0", "CC-BY-SA-4.0", "MIT", "internal"]),
                        "202%d-%02d-%02d" % (rng.choice([4, 5]), rng.randint(1, 12), rng.randint(1, 28))])


def write_hardware_inventory(path):
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["hostname", "accelerator", "accelerator_count", "host_memory_gb", "in_service_from"])
        rows = [
            ("gpu-node-01", "A40", 4, 256, "2024-02-01"), ("gpu-node-02", "A40", 4, 256, "2024-02-01"),
            ("gpu-node-03", "A40", 4, 256, "2024-06-14"), ("gpu-node-04", "L40S", 8, 512, "2025-01-20"),
            ("gpu-node-05", "L40S", 8, 512, "2025-01-20"), ("gpu-node-06", "L40S", 8, 512, "2025-09-02"),
            ("gpu-node-07", "H100", 8, 1024, "2026-01-12"), ("gpu-node-08", "H100", 8, 1024, "2026-01-12"),
            ("cpu-node-01", "", 0, 128, "2023-11-03"), ("cpu-node-02", "", 0, 128, "2023-11-03"),
        ]
        w.writerows(rows)


def write_scheduler_log(path, runs, rng):
    lines = []
    for r in runs:
        jid = int(r["run_id"].rsplit("-", 1)[1]) + 400000
        lines.append("%s SUBMIT job=%d user=%s part=%s" % (
            r["submitted_at"].replace("T", " ").rstrip("Z"), jid, r["submitted_by"],
            rng.choice(["gpu-short", "gpu-long", "mixed"])))
        lines.append("%s START  job=%d node=%s" % (
            r["started_at"].replace("T", " ").rstrip("Z"), jid, r["host"]))
        if r["finished_at"]:
            lines.append("%s END    job=%d state=%s" % (
                r["finished_at"].replace("T", " ").rstrip("Z"), jid, r["status"].upper()))
    lines.sort()
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


FIXED_ZIP_DATE = (2026, 10, 19, 9, 0, 0)
WORKBOOK_CREATOR = "beg-eval"
WORKBOOK_STAMP = "2026-11-04T16:21:00Z"


def normalise_xlsx(path):
    """Rewrite the workbook container so two builds are byte-identical and it carries no
    writing-library signature.

    openpyxl stamps docProps/core.xml with the wall clock and writes dc:creator as its own name,
    and every zip member carries the build's clock. Both make a rebuild differ from the last one
    and the second is a toolchain tell. The container is re-serialised member by member rather than
    patched at a byte offset, so the central directory is rebuilt and no offset can drift.
    """
    src = zipfile.ZipFile(path)
    members = [(i.filename, src.read(i.filename)) for i in src.infolist()]
    src.close()

    core = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<cp:coreProperties '
        'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<dc:creator>%s</dc:creator>'
        '<cp:lastModifiedBy>%s</cp:lastModifiedBy>'
        '<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created>'
        '<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified>'
        '</cp:coreProperties>'
    ) % (WORKBOOK_CREATOR, WORKBOOK_CREATOR, WORKBOOK_STAMP, WORKBOOK_STAMP)

    app = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Properties '
        'xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        '<Application>%s</Application>'
        '</Properties>'
    ) % WORKBOOK_CREATOR

    replace = {"docProps/core.xml": core.encode("utf-8"),
               "docProps/app.xml": app.encode("utf-8")}

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as out:
        for name, data in members:
            info = zipfile.ZipInfo(name, date_time=FIXED_ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            out.writestr(info, replace.get(name, data))


def write_handkept_workbook(path, runs_2026):
    """A spreadsheet one person maintained by hand and stopped updating part-way through Q4.

    It does not tie exactly to the tracker, which is what a hand-kept sheet does.
    """
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "by model"
    ws.append(["model_id", "runs logged by hand", "best accuracy seen", "note"])
    seen = {}
    for r in runs_2026:
        if r["status"] != "completed":
            continue
        q = int(r["submitted_at"][5:7])
        if q >= 11:        # the hand-kept sheet stops in early November
            continue
        a = r["metrics"].get("accuracy")
        d = seen.setdefault(r["model_id"], [0, None])
        d[0] += 1
        if a is not None and (d[1] is None or a > d[1]):
            d[1] = a
    for mid, (n, best) in sorted(seen.items()):
        ws.append([mid, n, best if best is not None else "",
                   "accuracy only, so generation and ranking runs are not counted here"])
    ws2 = wb.create_sheet("notes")
    for line in [
        ["This sheet is kept by hand and is not the system of record."],
        ["The tracker export is. Counts here cover submissions up to early November 2026 only."],
        ["Accuracy is the only metric recorded, so runs that do not report accuracy are absent."],
        ["Columns were added as they were needed, which is why the older rows are sparser."],
    ]:
        ws2.append(line)
    wb.save(path)
    normalise_xlsx(path)


def write_annotation_sample(path, rng):
    """A small double-annotated sample the group keeps so measurement error can be estimated."""
    recs = []
    for i in range(1400):
        ds = rng.choice(["ds-clf-newswire", "ds-clf-reviews", "ds-clf-intents"])
        truth = rng.randint(0, 3)
        a1 = truth if rng.random() < 0.88 else rng.randint(0, 3)
        a2 = truth if rng.random() < 0.85 else rng.randint(0, 3)
        rec = {
            "item_id": "%s-item-%05d" % (ds.split("-")[-1], i + 1),
            "dataset_id": ds,
            "annotator_a": "ann-%02d" % rng.randint(1, 9),
            "label_a": a1,
            "annotator_b": "ann-%02d" % rng.randint(10, 18),
            "label_b": a2,
            "adjudicated": None if rng.random() < 0.45 else (truth if rng.random() < 0.9 else rng.randint(0, 3)),
        }
        if rng.random() < 0.04:
            rec["label_b"] = None        # the second annotator did not reach every item
        recs.append(rec)
    write_jsonl(path, recs)


def write_ops_notes(path):
    path.write_text("""# Evaluation platform notes

Kept by whoever is on rota. Newest first.

## 2026-10-02
Tracker schema change landed in January is now the only export path. The 2025 CSV export in this
folder is the last one the old exporter produced and its column names do not match the 2026 feed.

## 2026-09-18
gpu-node-07 and gpu-node-08 came into service in January. Timings from before that date are not
comparable with timings after it on the same partition.

## 2026-08-05
Re-ran the Q2 export after a tracker upgrade. Some runs appear twice across the two export files;
the payloads are identical and the run_id is the join key.

## 2026-06-11
Reminder that the hand-kept workbook is not the system of record and is behind. Use the tracker
export for anything that has to tie.

## 2026-04-27
Host names reach us three ways depending on which system wrote the row: lower case from the
tracker, upper case from the scheduler on some partitions, and fully qualified from the inventory
sync. They are the same machines.

## 2026-02-14
Dataset versions are written inconsistently by submitters (v1.2, 1.2.0, and a date-and-revision
form for the generation sets). The registry lists which strings are in use for each dataset.

## 2025-12-03
The old exporter flattens metrics into metric_a, metric_b and loss, which only fits the
classification and tabular runs. Generation and ranking metrics are not in the 2025 CSV at all.

## 2025-10-20
Scheduler writes wall-clock local time. The tracker writes UTC. Both are in this folder.
""", encoding="utf-8")


def write_manifest(path, counts):
    """target/MANIFEST.md: the group's own compile note.

    This file ships inside the bundle, so it says only what the group would say about its own
    export: who compiled it, when, under what licence, what each file holds and which rough edges
    a reader should expect. Everything about how the corpus came to exist belongs in the folder's
    README, one level up and outside the bundle.
    """
    path.write_text("""# Benchmark and evaluation corpus, 2025 to 2026

Compiled by the %(group)s on 19 October 2026 for internal reuse. Free to reuse within the group.
The experiment tracker export is the system of record for anything that has to tie.

## Files

| file | format | rows | what it holds |
|---|---|---|---|
| `runs_2026.jsonl` | JSON Lines | %(n2026)s | the tracker's 2026 feed, one object per run, metrics nested |
| `runs_2025_export.csv` | CSV | %(n2025)s | the old exporter's 2025 feed, older column layout, metrics flattened |
| `scheduler.log` | text | %(nsched)s | submit, start and end lines from the job scheduler |
| `annotation_disagreement_sample.jsonl` | JSON Lines | %(nann)s | a double-annotated item sample, partly adjudicated |
| `sweeps/*.toml` | TOML | 4 files | the sweep definitions behind the 2026 runs |
| `metrics_dictionary.csv` | CSV | 8 | definitions for the metric keys that have been documented |
| `dataset_registry.csv` | CSV | 10 | datasets, the version strings in use, split sizes and licences |
| `hardware_inventory.csv` | CSV | 10 | hosts, accelerators and in-service dates |
| `eval_tracker_handkept.xlsx` | XLSX | 2 sheets | one person's hand-kept summary, behind the tracker |
| `ops_notes.md` | Markdown | - | the platform rota's running notes |

## What to expect before you join any of it up

Nothing here has been conformed. These are the things that have caught people out, listed so they
do not have to be rediscovered.

1. **Two layouts for the same thing.** The 2026 feed nests metrics under `metrics` and names its
   columns in full. The 2025 export flattens them into `metric_a`, `metric_b` and `loss` and
   abbreviates the column names. The two feeds do not share a schema.
2. **The 2025 export cannot carry generation or ranking metrics at all**, because three fixed
   metric columns do not fit them. Those runs are present with blank metric cells.
3. **Two clocks.** The tracker writes UTC with a trailing `Z`. The old export and the scheduler log
   write local wall-clock time with no zone marker, two hours ahead of UTC in winter.
4. **A run carries only the metrics its task type reports**, so `accuracy` is absent from
   generation runs and `rouge_l` from tabular runs. That is how the tracker stores them.
5. **Host names reach us in three spellings**: lower case from the tracker, upper case from some
   scheduler partitions, fully qualified from the inventory sync. The inventory holds the canonical
   form and they are the same machines.
6. **Dataset version strings are inconsistent**, because submitters type them: `v1.2`, `1.3.0` and
   a date-and-revision form all occur. The registry lists which strings are in use per dataset.
7. **Some runs have no metrics.** About three in a hundred ended `crashed`, `oom` or `killed`, and
   a few were still `running` at export, so the metrics object is empty and `gpu_hours` is null.
8. **Some runs appear twice.** The Q2 re-export after the tracker upgrade emitted part of the
   quarter a second time. The payloads are identical and `run_id` is the join key.
9. **The hand-kept workbook does not tie.** It stops in early November 2026, counts only runs that
   report `accuracy`, and is not the system of record.
10. **The annotation sample is only partly adjudicated**, and a few items are missing the second
    annotator's label.
11. **The CPU nodes have no accelerator**, so `gpu_hours` is zero for runs that landed there.
""" % counts, encoding="utf-8")


def write_readme(path, counts):
    """README.md at the folder root, outside target/.

    Everything that would be a leak inside the bundle lives here: that the corpus is synthetic, how
    to regenerate it, and the fact that nothing in it is designed to be got wrong.
    """
    path.write_text("""# task203_ext

A **raw dataset drop**, not a task.

| field | value |
|---|---|
| domain | General Statistics & Data Science |
| task type | benchmarking-and-ablations |
| contents | `target/` only, 14 files, 6 formats |
| largest file | `runs_2026.jsonl`, %(n2026)s records |
| provenance | synthetic, written by `generator/make.py` at seed %(seed)d |
| determinism | two consecutive builds are byte-identical, workbook container included |
| licence | internal; nothing here is derived from a third-party dataset |

## What it deliberately does not have

There is **no stump**. Nothing in this corpus was placed to be got wrong, and the pipeline
machinery that exists to enforce a stump does not apply:

- no `prompt.txt`, no question, no committed call
- no `submission.md`, no golden deliverable, no `figures.json`
- no design note, no default path, no ladder, no readability screen, no fork table
- no supplementary asks and no devices
- no planted defect, no decoy, no withheld rule, no distractors
- no fingerprint card registered, so `guard.py` holds no axis on this number and it bans nothing

The rough edges in the data are the ordinary unconformed state of a real export, not traps: layouts
that changed between exporters, two clocks, heterogeneous metric keys, three spellings of the same
host, inconsistent version strings, crashed runs with no metrics, a re-export that repeated part of
a quarter, and a hand-kept spreadsheet that is behind the system of record. All eleven are listed
in `target/MANIFEST.md` in the group's own words, so a reader can conform the corpus without
guessing, and anyone who later wants to build a task on top of this starts from scratch.

## Regenerating

    cd task203_ext && python3 -I generator/make.py

The generator reads no clock and takes one seed, so the rebuild is byte-identical. The workbook is
re-serialised after openpyxl writes it, which fixes the zip member dates and replaces the
library's own `dc:creator` stamp, since otherwise every rebuild would differ and the file would
carry a writing-library signature.
""" % counts, encoding="utf-8")


def cut_archive(zip_path, src):
    """target.zip, cut deterministically: sorted members, one fixed date, no host metadata.

    The folder's target/ is gitignored like every other build's, so the archive is what the
    repository actually carries. Fixing the member dates is what makes two cuts of the same corpus
    hash the same, which is the only way the archive can be checked against a rebuild.
    """
    members = sorted((p for p in src.rglob("*") if p.is_file()),
                     key=lambda p: str(p.relative_to(src)))
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as out:
        for p in members:
            info = zipfile.ZipInfo(str(p.relative_to(src)), date_time=FIXED_ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            out.writestr(info, p.read_bytes())


def main():
    rng = random.Random(SEED)
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    runs_2026 = build_runs(rng, 2026, 26400)
    runs_2025 = build_runs(rng, 2025, 9100)

    # The Q2 re-export: a slice of 2026 runs the upgrade emitted a second time, payload identical.
    repeats = [dict(r) for r in runs_2026[4000:4380]]
    feed_2026 = runs_2026 + repeats

    write_jsonl(OUT / "runs_2026.jsonl", feed_2026)
    completed_2025 = [r for r in runs_2025 if r["status"] == "completed"]
    write_2025_csv(OUT / "runs_2025_export.csv", completed_2025)
    write_sweep_configs(OUT / "sweeps", rng)
    write_metrics_dictionary(OUT / "metrics_dictionary.csv")
    write_dataset_registry(OUT / "dataset_registry.csv", rng)
    write_hardware_inventory(OUT / "hardware_inventory.csv")
    sched_src = [r for r in runs_2026 if r["finished_at"]][:9000]
    write_scheduler_log(OUT / "scheduler.log", sched_src, rng)
    write_handkept_workbook(OUT / "eval_tracker_handkept.xlsx", runs_2026)
    write_annotation_sample(OUT / "annotation_disagreement_sample.jsonl", rng)
    write_ops_notes(OUT / "ops_notes.md")

    nsched = len((OUT / "scheduler.log").read_text().splitlines())
    counts = {
        "group": GROUP, "seed": SEED,
        "n2026": "{:,}".format(len(feed_2026)),
        "n2025": "{:,}".format(len(completed_2025)),
        "nsched": "{:,}".format(nsched),
        "nann": "1,400",
    }
    write_manifest(OUT / "MANIFEST.md", counts)
    write_readme(ROOT / "README.md", counts)

    cut_archive(ROOT / "target.zip", OUT)

    files = sorted(p for p in OUT.rglob("*") if p.is_file())
    print("target/ built: %d files" % len(files))
    for p in files:
        print("  %-42s %9d bytes" % (str(p.relative_to(OUT)), p.stat().st_size))


if __name__ == "__main__":
    main()
