#!/usr/bin/env python3
"""
fingerprint.py, the mechanical half of the clone-check funnel.

Emits one fingerprint card per task build, then a ranked pair screen over the cards.

Track A (what a reviewer can see: prompt wording, file names, schemas, row counts,
fiction markers, deliverable species, submission phrasing) is computed here, in full,
deterministically, and never by a model.

Track B (mechanism: gap, pattern, decisive rung, calibration form, decision type) is
only seeded here, from the shipped ledger. The clone-auditor agent completes it by
reading the private design notes, which the ledger compresses to one cell.

Nothing in this file decides a verdict. It ranks pairs for adjudication.

Usage
  python3 fingerprint.py extract [--repo DIR] [--tasks task40,task41] [--out FILE]
  python3 fingerprint.py screen  [--cache FILE] [--focus taskNN] [--top N] [--json]
"""

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import zipfile
from collections import Counter, defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CACHE = os.path.join(REPO, ".claude", "skills", "clone-check", ".cache", "fingerprints.json")
LEDGER = os.path.join(REPO, ".claude", "skills", "stumping", "references", "shipped-ledger.md")
# Fingerprint cards (the fingerprint skill): the mechanism layer in one controlled vocabulary,
# reconciled against each build's submission. Where both builds of a pair have a card, Track B is
# read from the cards and the ledger is consulted only for status.
CARDS = os.path.join(REPO, ".claude", "skills", "fingerprint", "cards")
FP_FIELDS = ("domain", "subdomain", "objective", "shape", "decision_type", "gap", "pattern",
             "generators", "gate_g", "calibration_form", "context_artifact", "role_family", "driver")

# Folders that are backups, scratch or self-collisions. A build cannot clone itself.
EXCLUDE_DIRS = re.compile(r"(_backup|_bkp|_bk_|backup_\d{8}|^task99$)", re.I)

TABULAR = {".csv", ".tsv", ".txt", ".dat", ".psv"}
TEXTUAL = {".md", ".txt", ".json", ".jsonl", ".yaml", ".yml", ".html", ".xml", ".log"}

# Words that start sentences or carry the ask skeleton. Kept unmasked on purpose:
# the skeleton is what we are trying to detect.
COMMON = set("""
a about above across after against all also an and another any are as at
be because been before behind being below beside between both but by
can cannot commit committed common could
day days decide decision deliver
each either else end ended ending every
few first five follow following for four from
give given gives
had has have having how however
if in include includes including into is it its
just
keep
largest last leave leaving less let line list
make many may measured month months more most must
name named names need needs no none not
of off on once one only open or other others our out over
per print printed produce
rank recommend recommended report reports run runs
same say second set seven several ship should show single six so some state stated
take tell than that the their them then there these they third this those three through
to total two
under up us use used using
what when where whether which while who whole why will with within without write writes
year years yes
i im ive id we were weve my me mine you your yours it its he she they
""".split())

MONTHS = set("january february march april may june july august september october november december".split())
COMMON |= MONTHS


def sha(x, n=16):
    if isinstance(x, str):
        x = x.encode("utf-8", "replace")
    return hashlib.sha1(x).hexdigest()[:n]


# ---------------------------------------------------------------- text masking

TITLE_RUN = re.compile(r"\b[A-Z][A-Za-z&'\-]*(?:\s+(?:of|and|the|de|for)\s+)?(?:\s+[A-Z][A-Za-z&'\-]*)+\b")
TITLE_ONE = re.compile(r"\b[A-Z][A-Za-z&'\-]{2,}\b")
DATE_RE = re.compile(r"\b(?:\d{4}-\d{2}(?:-\d{2})?|\d{1,2}/\d{1,2}/\d{2,4}|(?:FY|OY|PY|Q)\s?\d{2,4}|W\d{2})\b")
NUM_RE = re.compile(r"\b\d[\d,]*(?:\.\d+)?%?\b")
CODE_RE = re.compile(r"`[^`]+`")


def mask(text):
    """Strip everything a reskin would change, keep the sentence machinery.

    Entity names, dates, numbers and backticked file names all become placeholders,
    so a prompt rewritten into a new industry with new companies still collides with
    its parent on the shape of its sentences. That is the whole point: templating
    survives reskinning, and only masked text can see it.
    """
    t = CODE_RE.sub(" <F> ", text)
    t = DATE_RE.sub(" <D> ", t)
    t = TITLE_RUN.sub(" <E> ", t)
    t = TITLE_ONE.sub(lambda m: m.group(0) if m.group(0).lower() in COMMON else " <E> ", t)
    t = NUM_RE.sub(" <N> ", t)
    t = re.sub(r"[^\w<>\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip().lower()


def tokens(text):
    return [w for w in text.split() if w]


def shingles(text, n=5, cap=4000):
    tk = tokens(text)
    out = {sha(" ".join(tk[i:i + n]), 10) for i in range(max(0, len(tk) - n + 1))}
    return sorted(out)[:cap]


def sentences(text):
    body = re.sub(r"\s+", " ", text)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z`])", body) if len(s.strip()) > 12]


def entities(text, keep=80):
    """Fiction markers, split by how much a shared one is worth.

    A multi-token Title Case run is an invented name (an operator, a facility, a
    filed standard). Two builds drawn independently share none of those, so one
    overlap is damning on its own. A single capitalised token is ambiguous: it is
    as likely to be a business noun the regex caught mid-sentence, so a shared one
    is reported and never scored. Sentence-initial-only tokens are dropped outright.
    """
    starts = set()
    for m in re.finditer(r"(?:^|[.!?:;\n]\s*|^\s*[-*\u2022]\s*|^\s*\d+[.)]\s*)([A-Z])", text, re.M):
        starts.add(m.start(1))
    multi, single = Counter(), Counter()
    for m in TITLE_RUN.finditer(text):
        s0 = m.group(0).strip()
        toks = s0.split()
        if len(toks) >= 2 and not all(w.lower() in COMMON for w in toks):
            multi[s0] += 1
    covered = " | ".join(multi)
    for m in TITLE_ONE.finditer(text):
        s0 = m.group(0)
        if s0.lower() in COMMON or len(s0) <= 3 or m.start() in starts:
            continue
        if s0 in covered:
            continue          # already counted inside a multi-token name
        single[s0] += 1
    return ([w for w, _ in multi.most_common(keep)],
            [w for w, _ in single.most_common(keep)])


def jaccard(a, b):
    sa, sb = set(a), set(b)
    return len(sa & sb) / len(sa | sb) if (sa or sb) else 0.0


# ---------------------------------------------------------------- file readers

def read_text(path, cap=400000):
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext == ".pdf":
            try:
                from pypdf import PdfReader
                return "\n".join((p.extract_text() or "") for p in PdfReader(path).pages)[:cap]
            except Exception:
                return ""
        if ext in (".xlsx", ".xlsm"):
            try:
                import openpyxl
                wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
                out = []
                for ws in wb.worksheets:
                    out.append(ws.title)
                    for i, row in enumerate(ws.iter_rows(max_row=40, values_only=True)):
                        out.append(" ".join(str(c) for c in row if c is not None))
                wb.close()
                return "\n".join(out)[:cap]
            except Exception:
                return ""
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read(cap)
    except Exception:
        return ""


def numeric_signature(cols):
    """A fingerprint of the values, not the labels.

    Two files generated from one seed keep this signature through a rename, a column
    reorder and a change of fiction. It is the only axis that catches a reskinned
    regeneration of the same underlying data.
    """
    sig = []
    for name, vals in cols:
        nums = []
        for v in vals:
            try:
                nums.append(float(str(v).replace(",", "").replace("$", "").strip()))
            except Exception:
                pass
        if len(nums) >= 20 and len(nums) >= 0.6 * len(vals):
            sig.append((len(nums), round(sum(nums), 4), round(min(nums), 6), round(max(nums), 6)))
    sig.sort()
    return sha(json.dumps(sig)) if sig else None


def profile_delimited(path, ext):
    out = {"rows": None, "cols": None, "header": [], "schema_hash": None, "numeric_sig": None}
    delim = "\t" if ext == ".tsv" else ","
    try:
        with open(path, "r", encoding="utf-8", errors="replace", newline="") as fh:
            head = fh.readline()
            if head.count("\t") > head.count(","):
                delim = "\t"
            if delim not in head and "|" in head:
                delim = "|"
            fh.seek(0)
            rd = csv.reader(fh, delimiter=delim)
            try:
                header = next(rd)
            except StopIteration:
                return out
            if len(header) < 2:
                return out
            cols = [[] for _ in header]
            n = 0
            for row in rd:
                n += 1
                if n <= 5000:
                    for i, cell in enumerate(row[:len(header)]):
                        cols[i].append(cell)
            out["rows"] = n
            out["cols"] = len(header)
            out["header"] = [h.strip().lower() for h in header][:60]
            out["schema_hash"] = sha(",".join(sorted(out["header"])))
            out["numeric_sig"] = numeric_signature(list(zip(out["header"], cols)))
    except Exception:
        pass
    return out


def profile_xlsx(path):
    out = {"rows": 0, "cols": 0, "header": [], "schema_hash": None, "numeric_sig": None, "sheets": []}
    try:
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        heads, cols_all, total = [], [], 0
        for ws in wb.worksheets:
            out["sheets"].append(ws.title)
            rows = ws.iter_rows(values_only=True)
            try:
                header = next(rows)
            except StopIteration:
                continue
            hdr = [str(c).strip().lower() for c in header if c is not None]
            heads += hdr
            cols = [[] for _ in hdr]
            n = 0
            for row in rows:
                n += 1
                if n <= 5000:
                    for i, cell in enumerate(row[:len(hdr)]):
                        cols[i].append(cell)
            total += n
            cols_all += list(zip(hdr, cols))
        wb.close()
        out["rows"] = total
        out["cols"] = len(heads)
        out["header"] = heads[:60]
        out["schema_hash"] = sha(",".join(sorted(heads))) if heads else None
        out["numeric_sig"] = numeric_signature(cols_all)
    except Exception:
        pass
    return out


# ---------------------------------------------------------------- the card

DELIV_RE = re.compile(r"`([A-Za-z0-9_\-./]+\.(?:py|csv|xlsx|pdf|md|json|txt|html|pptx|docx|png|svg|sql|ipynb))`")


def prompt_card(text):
    sents = sentences(text)
    delivs, seen = [], set()
    for m in DELIV_RE.finditer(text):
        f = m.group(1)
        if f not in seen:
            seen.add(f)
            delivs.append(f)
    bullets = [b.strip("-* ").strip() for b in re.findall(r"^\s*[-*]\s+(.+)$", text, re.M)]
    ask = ""
    for s in sents:
        if re.match(r"^\s*(Recommend|Name|Give me|Tell me|Decide|Choose|Commit|Identify|State|Select|Determine|Pick|Which)\b", s):
            ask = s
            break
    masked = mask(text)
    return {
        "words": len(tokens(text)),
        "sentence_count": len(sents),
        "ask_sentence": ask,
        "ask_masked": mask(ask) if ask else "",
        "deliverables": delivs,
        "deliverable_exts": [os.path.splitext(d)[1].lstrip(".") for d in delivs],
        "bullet_count": len(bullets),
        "bullets_masked": [mask(b) for b in bullets],
        # Sentence openings are the sharpest templating tell: an author reuses the
        # first six words of a construction long after changing everything else.
        "openings": [" ".join(tokens(mask(s))[:6]) for s in sents],
        "shingles_masked": shingles(masked, 5),
        "shingles_masked_short": shingles(masked, 3),
        "shingles_raw": shingles(re.sub(r"\s+", " ", text.lower()), 6),
        "entities_multi": entities(text)[0],
        "entities_single": entities(text)[1],
    }


def submission_card(text):
    def block(title):
        m = re.search(r"^##\s*(?:\d+\.\s*)?" + title + r".*?$(.*?)(?=^##\s|\Z)", text, re.M | re.S | re.I)
        return m.group(1).strip() if m else ""

    steps_raw = block("Step-?[ -]?by-?[ -]?Step")
    steps = [s.strip() for s in re.findall(r"^\s*\d+\.\s+(.+?)(?=^\s*\d+\.\s|\Z)", steps_raw, re.M | re.S)]
    steps = [re.sub(r"\s+", " ", s).strip() for s in steps]
    comps_raw = block("Critical Components")
    comps = [re.sub(r"\s+", " ", c).strip() for c in re.findall(r"^\s*\d+\.\s+(.+?)(?=^\s*\d+\.\s|\Z)", comps_raw, re.M | re.S)]
    dom = re.search(r"\*\*Domain:\*\*\s*(.+)", text)
    obj = re.search(r"\*\*Analytical objective:\*\*\s*(.+)", text)
    return {
        "domain_tag": dom.group(1).strip() if dom else "",
        "objective_tag": obj.group(1).strip() if obj else "",
        "step_count": len(steps),
        "steps": steps,
        "steps_masked": [mask(s) for s in steps],
        "step_openings": [" ".join(tokens(mask(s))[:6]) for s in steps],
        "critical_components": comps,
        "shingles_masked": shingles(mask(block("Justification") + " " + steps_raw), 5),
        "recommendation": re.sub(r"\s+", " ", block("Final Recommendation"))[:900],
    }


def target_card(tdir):
    files, formats = [], Counter()
    if not os.path.isdir(tdir):
        return {"present": False, "file_count": 0, "formats": {}, "layout": [], "files": []}
    for root, dirs, names in os.walk(tdir):
        dirs[:] = [d for d in dirs if not EXCLUDE_DIRS.search(d) and d != "__pycache__"]
        for nm in sorted(names):
            if nm.startswith("."):
                continue
            p = os.path.join(root, nm)
            rel = os.path.relpath(p, tdir)
            ext = os.path.splitext(nm)[1].lower()
            formats[ext.lstrip(".") or "none"] += 1
            rec = {"rel": rel, "base": os.path.splitext(nm)[0].lower(), "ext": ext.lstrip("."),
                   "bytes": os.path.getsize(p)}
            try:
                with open(p, "rb") as fh:
                    rec["content_hash"] = sha(fh.read())
            except Exception:
                rec["content_hash"] = None
            if ext in TABULAR and rec["bytes"] > 200:
                rec.update(profile_delimited(p, ext))
            elif ext in (".xlsx", ".xlsm"):
                rec.update(profile_xlsx(p))
            files.append(rec)
    layout = sorted({os.path.dirname(f["rel"]).split(os.sep)[0] for f in files if os.path.dirname(f["rel"])})
    return {"present": True, "file_count": len(files), "formats": dict(formats),
            "layout": layout or ["<flat>"], "files": files}


def parse_ledger(path):
    """One ledger row per drawn build. Tasks with several rows are lineage:
    a build and its own retired ancestors, which are never a clone finding."""
    rows = defaultdict(list)
    if not os.path.exists(path):
        return rows
    cols = ["task", "status", "domain", "objective", "gap", "pattern",
            "mechanism", "calibration", "artifact", "decision_type"]
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 4 or not re.match(r"^\*?\*?\d+", cells[0]):
                continue
            num = re.match(r"^\*?\*?(\d+)", cells[0]).group(1)
            rec = dict(zip(cols, cells + [""] * (len(cols) - len(cells))))
            rec["variant"] = cells[0]
            rec["_clean"] = {k: re.sub(r"\*+", "", v).strip() for k, v in rec.items() if isinstance(v, str)}
            rows["task" + num].append(rec)
    return rows


def build_card(repo, task, ledger):
    d = os.path.join(repo, task)
    prompt = read_text(os.path.join(d, "prompt.md"))
    sub = read_text(os.path.join(d, "submission.md"))
    # Design notes ship under several names, and the live one is not always at the
    # root (task40's is REBUILD_DESIGN.md, task64's is build/DESIGN_NOTE.md, task80
    # and task46 use DATASET_NOTES.md). Try the names in priority order, nested one
    # level, and take the first hit, so the mechanism layer is not under-counted.
    note = ""
    for sub_dir in ("", "build", "generator"):
        for name in ("DESIGN_NOTE.md", "REBUILD_DESIGN.md", "DATASET_NOTES.md"):
            note = read_text(os.path.join(d, sub_dir, name) if sub_dir
                             else os.path.join(d, name))
            if note:
                break
        if note:
            break
    lrows = ledger.get(task, [])
    fp = None
    fp_path = os.path.join(CARDS, task + ".json")
    if os.path.exists(fp_path):
        try:
            with open(fp_path, encoding="utf-8") as fh:
                raw = json.load(fh)
            fp = {k: raw.get(k) for k in FP_FIELDS}
        except Exception:
            fp = None
    card = {
        "task": task,
        "num": int(re.sub(r"\D", "", task) or 0),
        "path": d,
        "has": {"prompt": bool(prompt), "submission": bool(sub),
                "design_note": bool(note), "target": os.path.isdir(os.path.join(d, "target"))},
        "ledger_rows": [r["_clean"] for r in lrows],
        "fp": fp,
        # The mechanism layer is unavailable for builds with no card, no design note and
        # no ledger row, and back-fitted (label approximate, mechanism accurate) for
        # everything up to task36. Never infer a gap or pattern letter from a prompt.
        "mechanism_layer": ("card" if fp and (fp.get("gap") or fp.get("pattern")) else
                            "ledger+note" if (lrows and note) else
                            "ledger-only" if lrows else
                            "note-only" if note else "unavailable"),
        "mechanism_label_reliability": "back-fitted" if int(re.sub(r"\D", "", task) or 0) <= 36 else "native",
        "prompt": prompt_card(prompt) if prompt else None,
        "submission": submission_card(sub) if sub else None,
        "target": target_card(os.path.join(d, "target")),
        "design_note_present": bool(note),
        "design_note_words": len(tokens(note)),
    }
    return card


def cmd_extract(args):
    repo = args.repo
    ledger = parse_ledger(LEDGER)
    if args.tasks:
        tasks = [t.strip() for t in args.tasks.split(",") if t.strip()]
    else:
        tasks = sorted((d for d in os.listdir(repo)
                        if re.fullmatch(r"task\d+", d) and os.path.isdir(os.path.join(repo, d))
                        and not EXCLUDE_DIRS.search(d)),
                       key=lambda x: int(re.sub(r"\D", "", x)))
    cards = []
    for t in tasks:
        sys.stderr.write("  fingerprinting %s\n" % t)
        sys.stderr.flush()
        cards.append(build_card(repo, t, ledger))
    # Builds fingerprinted on another checkout are not on this disk; keep their cached cards so the
    # screen still compares a new build against the whole corpus.
    if os.path.exists(args.out):
        try:
            cached = json.load(open(args.out)).get("cards", [])
        except (OSError, ValueError):
            cached = []
        have = {c["task"] for c in cards}
        cards = sorted(cards + [c for c in cached if c.get("task") not in have],
                       key=lambda c: c.get("num") or int(re.sub(r"\D", "", c.get("task", "")) or 0))
    out = {"repo": repo, "count": len(cards), "cards": cards}
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    # Written to a temporary file and renamed, so two builds screening at once can never leave a
    # half-written cache behind.
    tmp = "%s.%d.tmp" % (args.out, os.getpid())
    with open(tmp, "w") as fh:
        json.dump(out, fh)
    os.replace(tmp, args.out)
    kept = [c for c in cards if c["has"]["prompt"] or c["target"]["file_count"]]
    print("extracted %d cards (%d with prompt or target) -> %s" % (len(cards), len(kept), args.out))
    return 0


# ---------------------------------------------------------------- the screen

def idf_weights(cards):
    df = Counter()
    for c in cards:
        for nm in {f["base"] for f in c["target"]["files"]}:
            df[nm] += 1
    n = max(1, len(cards))
    import math
    return {nm: math.log(1 + n / v) for nm, v in df.items()}, df


def weighted_jaccard(a, b, w):
    sa, sb = set(a), set(b)
    inter = sum(w.get(x, 1.0) for x in sa & sb)
    union = sum(w.get(x, 1.0) for x in sa | sb)
    return inter / union if union else 0.0


def opening_overlap(a, b, ow=None, rare_at=4):
    """Shared sentence constructions, weighted by how rare each one is.

    A construction the author uses in every build says nothing about a pair, so
    it is nearly free here and gets reported under corpus habits instead. A
    construction two builds share and nobody else uses is the templating signal.
    """
    sa = {o for o in a if len(o.split()) >= 4}
    sb = {o for o in b if len(o.split()) >= 4}
    if not sa or not sb:
        return 0.0, []
    ow = ow or {}
    shared = sa & sb
    num = sum(ow.get(o, 1.0) for o in shared)
    den = min(sum(ow.get(o, 1.0) for o in sa), sum(ow.get(o, 1.0) for o in sb))
    rare = sorted(o for o in shared if ow.get(o, 99) >= rare_at)
    return (num / den if den else 0.0), rare


def track_a(x, y, ctx):
    """Everything a final_verdict reviewer can see without the private notes."""
    w, ent_stop, ow = ctx["fname_w"], ctx["ent_stop"], ctx["open_w"]
    ax = {}
    ev = []
    tx, ty = x["target"], y["target"]
    fx = [f["base"] for f in tx["files"]]
    fy = [f["base"] for f in ty["files"]]
    ax["filenames"] = weighted_jaccard(fx, fy, w)
    shared_names = sorted(set(fx) & set(fy))
    if shared_names:
        rare = [n for n in shared_names if w.get(n, 0) > 2.0]
        if rare:
            ev.append("shared rare target file names: " + ", ".join(rare[:8]))

    hx = {f["content_hash"] for f in tx["files"] if f.get("content_hash")}
    hy = {f["content_hash"] for f in ty["files"] if f.get("content_hash")}
    ident = hx & hy
    ax["identical_files"] = len(ident)
    if ident:
        ev.append("%d byte-identical target files" % len(ident))

    sx = {f.get("schema_hash") for f in tx["files"] if f.get("schema_hash")}
    sy = {f.get("schema_hash") for f in ty["files"] if f.get("schema_hash")}
    ax["schema_collisions"] = len(sx & sy)
    if sx & sy:
        ev.append("%d tables with an identical column set" % len(sx & sy))

    nx = {f.get("numeric_sig") for f in tx["files"] if f.get("numeric_sig")}
    ny = {f.get("numeric_sig") for f in ty["files"] if f.get("numeric_sig")}
    ax["same_seed_tables"] = len(nx & ny)
    if nx & ny:
        ev.append("%d tables whose numeric values are identical under a rename (same-seed tell)" % len(nx & ny))

    ax["layout"] = jaccard(tx["layout"], ty["layout"])
    ax["formats"] = jaccard(list(tx["formats"]), list(ty["formats"]))

    px, py = x.get("prompt"), y.get("prompt")
    if px and py:
        ax["prompt_masked"] = jaccard(px["shingles_masked"], py["shingles_masked"])
        ax["prompt_raw"] = jaccard(px["shingles_raw"], py["shingles_raw"])
        ov, shared_open = opening_overlap(px["openings"], py["openings"], ow)
        ax["ask_skeleton"] = ov
        if shared_open:
            ev.append("shared rare sentence constructions: " + " | ".join('"%s"' % s for s in shared_open[:4]))
        if px["ask_masked"] and px["ask_masked"] == py["ask_masked"]:
            ax["ask_identical"] = 1.0
            ev.append("Main Ask sentence is identical once entities and figures are masked")
        else:
            a4 = " ".join(tokens(px["ask_masked"])[:7])
            b4 = " ".join(tokens(py["ask_masked"])[:7])
            ax["ask_identical"] = 1.0 if (a4 and a4 == b4) else 0.0
            if a4 and a4 == b4:
                ev.append('Main Ask opens on the same construction: "%s"' % a4)
        em = (set(px["entities_multi"]) & set(py["entities_multi"])) - ent_stop
        es = (set(px["entities_single"]) & set(py["entities_single"])) - ent_stop
        ax["entities"] = len(em)
        ax["entities_weak"] = len(es)
        if em:
            ev.append("shared invented names, which independent draws never produce: "
                      + ", ".join(sorted(em)[:8]))
        if len(es) >= 3:
            ev.append("shared capitalised terms (weak, may be business vocabulary): "
                      + ", ".join(sorted(es)[:8]))
        ax["deliverable_species"] = 1.0 if px["deliverable_exts"] and px["deliverable_exts"] == py["deliverable_exts"] else 0.0
    else:
        for k in ("prompt_masked", "prompt_raw", "ask_skeleton", "ask_identical", "entities", "entities_weak", "deliverable_species"):
            ax[k] = 0.0

    sxb, syb = x.get("submission"), y.get("submission")
    if sxb and syb:
        ax["submission_masked"] = jaccard(sxb["shingles_masked"], syb["shingles_masked"])
        ov2, shared2 = opening_overlap(sxb["step_openings"], syb["step_openings"], ctx["step_w"])
        ax["step_skeleton"] = ov2
        if shared2:
            ev.append("shared solution-step constructions: " + " | ".join('"%s"' % s for s in shared2[:3]))
    else:
        ax["submission_masked"] = ax["step_skeleton"] = 0.0

    score = (0.20 * ax["filenames"] + 0.16 * ax["prompt_masked"] + 0.14 * ax["ask_skeleton"]
             + 0.10 * ax["submission_masked"] + 0.08 * ax["step_skeleton"] + 0.06 * ax["layout"]
             + 0.04 * ax["formats"] + 0.06 * ax["deliverable_species"] + 0.06 * ax["ask_identical"]
             + 0.10 * min(1.0, ax["schema_collisions"] / 3.0))
    # Hard tells are not averaged away. Identical bytes, same-seed values or a shared
    # invented proper noun each carry a pair on their own.
    # A hard tell is not averaged away, but it has to be real: one byte-identical
    # decisive file, one same-seed table, or two invented proper nouns nobody else uses.
    hard = max(min(1.0, ax["identical_files"] / 2.0),
               min(1.0, ax["same_seed_tables"] / 2.0),
               1.0 if ax["entities"] >= 1 else 0.0)
    return round(max(score, hard), 4), {k: (round(v, 4) if isinstance(v, float) else v) for k, v in ax.items()}, ev



# A task carries one ledger row per architecture it has been through, in file order
# rather than chronological order, so the last row is not the live one. Severity has
# to come from the strongest row a task holds, because a collision against an approved
# build is the exclusion and a collision against a retired one is a note. Dead is
# checked before live on purpose: "rebuilt, architecture retired" is dead.
STATUS_RANKS = [
    (3, "delivered or approved", r"approved|delivered|determinism pass deterministic"),
    (1, "retired or failed", r"retired|failed|exhausted|solved on a first pass|both solved"),
    (2, "live", r"rebuilt|built |hardened|awaiting|drawing|contested|valid stump"),
]


def status_rank(status):
    t = (status or "").lower()
    if not t:
        return 0, "unknown"
    for r, label, pat in STATUS_RANKS:
        if re.search(pat, t):
            return r, label
    return 0, "unknown"


def live_row(card):
    """The strongest row the task holds, which is the one severity is judged on."""
    rows = card.get("ledger_rows") or []
    if not rows:
        return None, (0, "no ledger row")
    best, bestr = rows[0], status_rank(rows[0].get("status"))
    for r in rows[1:]:
        rr = status_rank(r.get("status"))
        if rr[0] >= bestr[0]:
            best, bestr = r, rr
    return best, bestr


# ------------------------------------------------- mechanism-cell normalisation
#
# The ledger's mechanism columns are free prose, so raw token overlap between two
# cells is near zero even when the two builds decide the same kind of thing. These
# collapse each cell to a family drawn from the vocabulary the ledger actually uses,
# which is what makes a Track B collision detectable at all.

CELL_STOP = set("""a an and are as at be by for from in into is it its of on onto or over per
the their there they this to under up was were which with without that than then so""".split())

DECISION_FAMILIES = [
    ("which_of_n", r"\bwhich\b|\bwhere to place\b|gets the one|\bto name\b|\bnominates\b|\bto lapse\b|\bto certify\b|\bto scale\b|\bto adopt\b|\bto commit\b"),
    ("certified_figure", r"\bone [a-z-]+ (figure|quantity|volume|amount|number)\b|\bhow much\b|\bhow many\b|\bfigure the\b|\bobligation figure\b|\bto resource\b"),
    ("structural_verdict", r"\bverdict\b|\bcharacterisation\b|\bwhich structure\b|\bposture\b"),
]
DECISION_MODIFIERS = [
    ("no_candidate_list", r"no candidate list"),
    ("forward_window", r"has not opened|coming (year|programme year|program year|quarter|cycle)|before a cycle"),
    ("hold_licensed", r"non-pick|none of them|to hold at base|licensed on the same footing"),
]

CALIBRATION_FAMILIES = [
    ("closed_decision_corpus", r"determination|close-?out|closed (prior-year |)review|closed directions|allowability|escalation review|closed campaign|close-?outs|ledger of the revolving|drawdown|(review|determination|dispute) register"),
    ("realised_outcome_roster", r"roster|enrol|attendance|outcome log|field-deployment|draw among acceptors|completion files|cohorts"),
    ("parallel_source_overlap", r"parallel-run|mirror statistic|gold-standard|subsample|control total|two sided|reconciliation|two sources"),
    ("counterparty_settlement", r"counterparty|settlement|settled statements|service-credit|acknowledg|dispute settlement|payout runs"),
    ("certified_matrix", r"certified .*matrix|\d+ cells|by division matrix|pilot with filed"),
    ("physical_verification", r"scan-verified|lot-trace|condition survey|interchange survey|audit drill|inspection"),
    ("censored_or_lagged", r"censored|two cycle lag|released on a"),
]


def _fam(cell, table, want_all=False):
    """Classify a free-prose ledger cell into one family.

    Where more than one family fits, the cell is ambiguous and the classifier says so
    instead of taking the first row of the table. A calibration cell describes both the
    corpus and the checks run against it, so incidental vocabulary from the checks can
    match a family the corpus is not, and silently picking one produces a Track B
    collision that is not there.
    """
    t = (cell or "").lower()
    if not t:
        return (None, []) if want_all else None
    hits = [name for name, pat in table if re.search(pat, t)]
    if want_all:
        return (hits[0] if len(hits) == 1 else None), hits
    return hits[0] if len(hits) == 1 else ("ambiguous" if len(hits) > 1 else "other")


def decision_family(cell):
    t = (cell or "").lower()
    fam = _fam(cell, DECISION_FAMILIES)
    mods = {n for n, pat in DECISION_MODIFIERS if re.search(pat, t)}
    return fam, mods


def artifact_family(cell):
    """`none by design (Gate G v3)` is the spec, not a choice, so two builds sharing
    it are complying rather than cloning. It never counts as a collision."""
    t = (cell or "").lower()
    if not t or t.startswith("none by design"):
        return None
    return re.sub(r"[^a-z ]", " ", t).split()[0] if t else None


def norm_cell(s):
    return [w for w in re.sub(r"[^a-z ]", " ", (s or "").lower()).split()
            if w not in CELL_STOP and len(w) > 2]


def norm_pattern(cell):
    """The pattern column is letters, so the content-word normaliser erases it.

    Returns the set of patterns named and the decisive one. Cells read `A`, `B over A`,
    `G11 filed eligibility over D`, so the pattern written first is the one carrying the
    decisive rung, and that is the one Part 6.1 bans reusing. The rest of the set is
    context, worth a weaker signal.
    """
    t = (cell or "").strip()
    if not t:
        return set(), None
    toks = re.findall(r"\bG\d{1,2}\b|\b[A-E]\b", t)
    if not toks:
        return set(), None
    # `none of A to E decisive` enumerates a range rather than naming one.
    if re.search(r"none of [A-E] to [A-E]", t):
        m = re.search(r"\bnone of [A-E] to [A-E][^;]*;\s*([A-EG]\d*)", t)
        return set(toks), (m.group(1) if m else None)
    return set(toks), toks[0]


def norm_gap(cell):
    """Gap cells read `time`, `objective over population`, `time into population`.
    The gap named first is the decisive one."""
    words = norm_cell(cell)
    return set(words), (words[0] if words else None)


def _fp_decisive(fp):
    """The pattern written first, or the first G-code when the card says no A to E pattern
    carried the decisive rung (a pattern listed after "none" is only the frame)."""
    pats = [p for p in (fp.get("pattern") or []) if p]
    if pats and pats[0] != "none":
        return pats[0]
    for g in fp.get("generators") or []:
        if g:
            return g
    return next((p for p in pats if p != "none"), None)


def track_b_cards(x, y):
    """Track B from the fingerprint cards, which carry the mechanism in one vocabulary, so
    collisions are exact string matches rather than regex families over free prose. Status
    still comes from the ledger. A card with no ledger row is a build on disk that the portal
    has not spoken on, so it counts as live."""
    fx, fy = x["fp"], y["fp"]
    _, sx = live_row(x)
    _, sy = live_row(y)
    rx = sx[0] or 2
    ry = sy[0] or 2
    lab_x = sx[1] if sx[0] else "live (card, no ledger row)"
    lab_y = sy[1] if sy[0] else "live (card, no ledger row)"
    ev = []
    gx, gy = (fx.get("gap") or [None])[0], (fy.get("gap") or [None])[0]
    px, py = _fp_decisive(fx), _fp_decisive(fy)
    best = {"decision_mods": [], "calibration_ambiguous": None}
    best["gap_decisive"] = best["gap"] = 1.0 if gx and gx == gy else 0.0
    best["pattern_decisive"] = best["pattern"] = 1.0 if px and px == py else 0.0
    dt = fx.get("decision_type")
    best["decision_family"] = best["decision_type"] = 1.0 if dt and dt == fy.get("decision_type") else 0.0
    cf = fx.get("calibration_form")
    best["calibration_family"] = cf if cf and cf not in ("none", "other") and cf == fy.get("calibration_form") else None
    ca = fx.get("context_artifact")
    best["artifact_family"] = ca if ca and ca not in ("none", "other") and ca == fy.get("context_artifact") else None
    same_pair = fx.get("domain") and (fx.get("domain"), fx.get("objective")) == (fy.get("domain"), fy.get("objective"))
    best["pairing_rows"] = (min(rx, ry), "card", "card", lab_x, lab_y) if same_pair else None
    best["pairing_live"] = bool(same_pair and min(rx, ry) >= 2)
    best["gap_pattern_rows"] = ((min(rx, ry), "card", "card", lab_x, lab_y)
                                if best["gap_decisive"] and best["pattern_decisive"] else None)
    best["mechanism"] = round(jaccard(norm_cell(fx.get("driver")), norm_cell(fy.get("driver"))), 3)
    if best["gap_decisive"] and best["pattern_decisive"]:
        ev.append("the decisive gap (%s) and the decisive pattern (%s) are both the same on the cards, "
                  "which is Part 6.1's similarity test failing on the two axes that matter" % (gx, px))
    elif best["gap_decisive"]:
        ev.append("same decisive gap on the cards (%s)" % gx)
    elif best["pattern_decisive"]:
        ev.append("same decisive pattern on the cards (%s)" % px)
    if fx.get("gate_g") and fx.get("gate_g") == fy.get("gate_g") and best["gap_decisive"] and best["pattern_decisive"]:
        ev.append("and the same Gate G mechanism (%s), which is the fingerprint guard's same-driver signature, "
                  "the one that caught the task86 v1 against task72 v2 Template" % fx.get("gate_g"))
    if best["decision_family"]:
        ev.append("same decision type on the cards (%s)" % dt)
    if same_pair:
        ev.append("same domain and objective pairing on the cards (%s x %s)" % (fx.get("domain"), fx.get("objective")))
    if best["calibration_family"]:
        ev.append("same calibration form on the cards (%s), which Part 6.1 bans reusing" % cf)
    if best["artifact_family"]:
        ev.append("same context-artifact type on the cards (%s)" % ca)
    if best["mechanism"] >= CARD_DRIVER_OVERLAP:
        ev.append("the cards' driver sentences overlap on content words (%.2f), read both design notes closely"
                  % best["mechanism"])
    best["_core_collisions"] = (int(best["gap_decisive"]) + int(best["pattern_decisive"])
                                + int(best["decision_family"]))
    best["same_driver"] = bool(best["gap_decisive"] and best["pattern_decisive"] and fx.get("gate_g")
                               and fx.get("gate_g") == fy.get("gate_g"))
    best["_source"] = "cards"
    return best, ev


# Driver sentences are written with the domain nouns stripped, so they share more abstract
# vocabulary than ledger prose does, and the overlap that means "read this pair" sits higher.
CARD_DRIVER_OVERLAP = 0.40


def track_b(x, y):
    """Mechanism. Read from the fingerprint cards when both builds have one, otherwise
    seeded from the ledger, deliberately coarse, because the ledger compresses a whole
    ladder into one cell. The agent reads the design notes and decides. What this does is
    guarantee that a pair colliding on gap, pattern and decision family is adjudicated no
    matter how far apart its surfaces sit, which is the failure mode a surface screen cannot
    see: a true clone, fully reskinned.
    """
    if x.get("fp") and y.get("fp") and (x["fp"].get("gap") or x["fp"].get("pattern")) \
            and (y["fp"].get("gap") or y["fp"].get("pattern")):
        return track_b_cards(x, y)
    ev = []
    if not x["ledger_rows"] or not y["ledger_rows"]:
        return None, ["mechanism layer unavailable on at least one side, the agent must read the design notes or record the gap"]
    best, extras = {}, {"decision_family": 0.0, "decision_mods": [], "calibration_family": None,
                        "artifact_family": None, "gap_pattern_rows": None, "pairing_rows": None,
                        "calibration_ambiguous": None}
    for rx in x["ledger_rows"]:
        for ry in y["ledger_rows"]:
            # Which architectures collided matters as much as that they did. Two dead
            # architectures sharing a gap and a pattern is history, not a finding.
            gxa, gxd = norm_gap(rx.get("gap"))
            gya, gyd = norm_gap(ry.get("gap"))
            pxa, pxd = norm_pattern(rx.get("pattern"))
            pya, pyd = norm_pattern(ry.get("pattern"))
            # The domain-plus-objective ban is checked per row pair too, because a
            # pairing that collides only with an architecture the author already
            # abandoned is a record of the redraw working, not a finding against it.
            if (norm_cell(rx.get("objective")) and norm_cell(rx.get("objective")) == norm_cell(ry.get("objective"))
                    and jaccard(norm_cell(rx.get("domain")), norm_cell(ry.get("domain"))) >= 0.6):
                sxp, syp = status_rank(rx.get("status")), status_rank(ry.get("status"))
                cp = (min(sxp[0], syp[0]), rx.get("variant", ""), ry.get("variant", ""), sxp[1], syp[1])
                if extras["pairing_rows"] is None or cp[0] > extras["pairing_rows"][0]:
                    extras["pairing_rows"] = cp
            if gxd and gxd == gyd and pxd and pxd == pyd:
                sx_, sy_ = status_rank(rx.get("status")), status_rank(ry.get("status"))
                cand = (min(sx_[0], sy_[0]), rx.get("variant", ""), ry.get("variant", ""), sx_[1], sy_[1])
                if extras["gap_pattern_rows"] is None or cand[0] > extras["gap_pattern_rows"][0]:
                    extras["gap_pattern_rows"] = cand
            for k in ("calibration", "artifact", "objective", "domain", "mechanism"):
                a, b = norm_cell(rx.get(k)), norm_cell(ry.get(k))
                if not a or not b:
                    continue
                best[k] = max(best.get(k, 0.0), round(jaccard(a, b), 3))
            for k, fn in (("gap", norm_gap), ("pattern", norm_pattern)):
                (sa_, da_), (sb_, db_) = fn(rx.get(k)), fn(ry.get(k))
                if not sa_ or not sb_:
                    continue
                best[k] = max(best.get(k, 0.0), round(1.0 if sa_ == sb_ else jaccard(sorted(sa_), sorted(sb_)), 3))
                if da_ and da_ == db_:
                    best[k + "_decisive"] = 1.0
            fx, mx = decision_family(rx.get("decision_type"))
            fy, my = decision_family(ry.get("decision_type"))
            if fx and fx == fy and fx != "other":
                extras["decision_family"] = 1.0
                extras["decision_mods"] = sorted(mx & my)
            cx, hx = _fam(rx.get("calibration"), CALIBRATION_FAMILIES, want_all=True)
            cy, hy = _fam(ry.get("calibration"), CALIBRATION_FAMILIES, want_all=True)
            if cx and cx == cy:
                extras["calibration_family"] = cx
            elif len(hx) > 1 or len(hy) > 1:
                shared = sorted(set(hx) & set(hy))
                if shared:
                    extras["calibration_ambiguous"] = shared
            ax_, ay_ = artifact_family(rx.get("artifact")), artifact_family(ry.get("artifact"))
            if ax_ and ax_ == ay_:
                extras["artifact_family"] = ax_
    best.update(extras)
    best["pairing_live"] = bool(extras["pairing_rows"] and extras["pairing_rows"][0] >= 2)
    best["decision_type"] = extras["decision_family"]
    if best.get("gap_decisive") and best.get("pattern_decisive"):
        gp = extras["gap_pattern_rows"]
        where = (" (rows %s and %s, %s against %s)" % (gp[1], gp[2], gp[3], gp[4])) if gp else ""
        ev.append("the decisive gap and the decisive pattern are both the same, which is Part 6.1's "
                  "similarity test failing on the two axes that matter" + where)
        if gp and gp[0] <= 1:
            ev.append("both colliding rows are retired or failed architectures, so this is history rather than a live clone")
    if extras["decision_family"]:
        m = (", sharing " + " and ".join(extras["decision_mods"])) if extras["decision_mods"] else ""
        ev.append("same decision family" + m)
    if extras["pairing_rows"]:
        pr = extras["pairing_rows"]
        ev.append("same domain and objective pairing, banned outright between consecutive builds "
                  "(rows %s and %s, %s against %s)" % (pr[1], pr[2], pr[3], pr[4]))
        if pr[0] <= 1:
            ev.append("that pairing collides only with a retired or failed architecture, so the redraw "
                      "already answered it")
    if extras["calibration_family"]:
        ev.append("same calibration family (%s), which Part 6.1 bans reusing" % extras["calibration_family"])
    elif extras["calibration_ambiguous"]:
        ev.append("calibration cells overlap on %s but at least one classifies more than one way, so the "
                  "design notes decide whether the form is actually shared"
                  % " and ".join(extras["calibration_ambiguous"]))
    if extras["artifact_family"]:
        ev.append("same rung-0 artifact species")
    if best.get("mechanism", 0) >= 0.30:
        ev.append("ledger mechanism sentences overlap on content words, read both design notes closely")
    core = (sum(1 for k in ("gap_decisive", "pattern_decisive") if best.get(k))
            + (1 if extras["decision_family"] else 0))
    best["_core_collisions"] = core
    return best, ev


def cmd_screen(args):
    data = json.load(open(args.cache))
    cards = [c for c in data["cards"] if c["has"]["prompt"] or c["target"]["file_count"] >= 3]
    w, df = idf_weights(cards)

    import math
    n = max(1, len(cards))

    # An "entity" that turns up across a fifth of the corpus is a word the regex
    # mistook for a name, not a fiction marker. Frequency retires it, so the hard
    # tell stays hard without hand-maintaining a word list.
    ent_df = Counter()
    for c in cards:
        if c.get("prompt"):
            for e in set(c["prompt"]["entities_multi"]) | set(c["prompt"]["entities_single"]):
                ent_df[e] += 1
    ent_cut = max(3, int(0.15 * n))
    ent_stop = {e for e, v in ent_df.items() if v >= ent_cut}

    open_df, step_df = Counter(), Counter()
    for c in cards:
        if c.get("prompt"):
            for o in set(c["prompt"]["openings"]):
                open_df[o] += 1
        if c.get("submission"):
            for o in set(c["submission"]["step_openings"]):
                step_df[o] += 1
    open_w = {o: math.log(1 + n / v) for o, v in open_df.items()}
    step_w = {o: math.log(1 + n / v) for o, v in step_df.items()}
    ctx = {"fname_w": w, "ent_stop": ent_stop, "open_w": open_w, "step_w": step_w}

    focus = args.focus

    # The batch is a rolling window: the last N builds ending at the newest one, or
    # at a build the author names. Pairs are kept when at least one side sits inside
    # it, because a batch has two different exposures and they need different repairs.
    # Two builds inside the window colliding is a thing to fix before it ships, and a
    # build inside colliding with an approved one already delivered is the exclusion.
    nums = sorted(c["num"] for c in cards)
    through = None
    if args.through:
        through = int(re.sub(r"\D", "", args.through) or 0)
    elif focus:
        through = int(re.sub(r"\D", "", focus) or 0)
    else:
        through = nums[-1] if nums else 0
    if args.all or focus:
        window = set(nums)
    else:
        eligible = [n for n in nums if n <= through]
        window = set(eligible[-args.window:]) if eligible else set()

    # Every pair is scored, always, even in focus mode. A raw surface score means
    # nothing on its own (this corpus runs a mean of about 0.06 and a maximum of
    # about 0.21), so a pair is judged against the corpus baseline, not a threshold
    # invented in advance. That also keeps the pre-flight mode honest: a new build
    # is ranked against how similar these builds normally are to each other.
    scored = []
    for i in range(len(cards)):
        for j in range(i + 1, len(cards)):
            x, y = cards[i], cards[j]
            if x["num"] == y["num"]:
                continue  # lineage, a build is not a clone of its own retired ancestor
            sa, ax, ev = track_a(x, y, ctx)
            tb, evb = track_b(x, y)
            scored.append({"x": x, "y": y, "track_a": sa, "axes": ax,
                           "evidence_a": ev, "track_b": tb, "evidence_b": evb})
    order = sorted(range(len(scored)), key=lambda k: scored[k]["track_a"])
    for rank, k in enumerate(order):
        scored[k]["track_a_pct"] = round(rank / max(1, len(order) - 1), 4)

    pairs = []
    for rec in scored:
        x, y = rec["x"], rec["y"]
        if focus and focus not in (x["task"], y["task"]):
            continue
        inx, iny = x["num"] in window, y["num"] in window
        if not focus and not args.all and not (inx or iny):
            continue
        scope = "in batch" if (inx and iny) else "batch against an earlier build"
        sa, ax, tb = rec["track_a"], rec["axes"], rec["track_b"]
        pct = rec["track_a_pct"]
        lx, ly = live_row(x), live_row(y)
        adjacent = abs(x["num"] - y["num"]) == 1     # Part 6.1 bans are written against "your last build"
        consecutive = abs(x["num"] - y["num"]) <= 2  # near enough that the draw should have seen it
        core = (tb or {}).get("_core_collisions", 0)
        promote = []
        if ax["identical_files"]:
            promote.append("byte-identical target files")
        if ax["same_seed_tables"]:
            promote.append("same-seed tables")
        if ax["entities"]:
            promote.append("shared invented name")
        if pct >= 0.99:
            promote.append("surface similarity in the corpus top 1 percent")
        elif pct >= 0.97 and consecutive:
            promote.append("surface similarity in the top 3 percent of consecutive builds")
        backfit = "back-fitted" in (x["mechanism_label_reliability"], y["mechanism_label_reliability"])
        if core >= 3:
            # The ledger's own header says the labels up to task36 were fitted after the
            # fact, accurate about the mechanism and approximate about the name, so a
            # collision that rests on one of those is a shared guess until a reader opens
            # both design notes. It is still worth adjudicating, it is just not a finding yet.
            promote.append("gap, pattern and decision family all collide, which is a clone signature even "
                           "with no surface overlap" +
                           (", but at least one side carries a back-fitted label so the design notes decide it"
                            if backfit else ""))
        elif core >= 2 and consecutive:
            promote.append("two of three mechanism axes collide between consecutive builds, which Part 6.1 bans directly")
        if tb and tb.get("same_driver") and core < 3:
            promote.append("gap, pattern and Gate G mechanism all collide on the cards, the same-driver signature, "
                           "which carries a Template finding even when the decision is cut differently")
        if tb and tb.get("pattern_decisive") and adjacent:
            promote.append("the decisive pattern repeats from the immediately previous build, which Part 6.1 bans by name")
        elif tb and tb.get("pattern_decisive") and consecutive:
            promote.append("the decisive pattern repeats from a build two back, close enough that the draw should have caught it")
        pr = (tb or {}).get("pairing_rows")
        if pr and consecutive and pr[0] >= 2:
            promote.append("domain and objective pairing repeated between consecutive builds, both sides live")
        if tb and tb.get("_source") == "cards":
            if tb.get("mechanism", 0) >= CARD_DRIVER_OVERLAP:
                promote.append("card driver sentences overlap")
        elif tb and tb.get("mechanism", 0) >= 0.30:
            promote.append("ledger mechanism sentences overlap")
        if tb and tb.get("calibration_family") and consecutive:
            promote.append("calibration form reused between consecutive builds")
        if tb is None and pct >= 0.985:
            promote.append("mechanism unknown and surface unusually high, read it")
        pairs.append({
            "pair": [x["task"], y["task"]],
            "track_a": sa, "track_a_pct": pct, "axes": ax, "evidence_a": rec["evidence_a"],
            "track_b": tb, "evidence_b": rec["evidence_b"],
            "consecutive": consecutive,
            "adjacent": adjacent,
            "scope": scope,
            "mechanism_layer": [x["mechanism_layer"], y["mechanism_layer"]],
            "label_reliability": [x["mechanism_label_reliability"], y["mechanism_label_reliability"]],
            "label_caveat": backfit,
            "status": [(lx[0].get("status", "") if lx[0] else "no ledger row")[:60],
                       (ly[0].get("status", "") if ly[0] else "no ledger row")[:60]],
            "status_rank": [lx[1], ly[1]],
            # Severity is about exposure, meaning whether both sides can actually end up
            # in front of a reviewer. A retired architecture never ships, so a collision
            # touching one is history however clean the match is. Among the pairs that
            # can ship, the hit against an already delivered build is the exclusion,
            # because that is the comparison the cross-batch check actually runs, and it
            # does not need the other side to be delivered too.
            "severity": ("history, at least one side is retired or failed" if min(lx[1][0], ly[1][0]) <= 1
                         and min(lx[1][0], ly[1][0]) >= 1 else
                         "status unknown on at least one side" if min(lx[1][0], ly[1][0]) == 0 else
                         "exclusion level, both sides delivered" if min(lx[1][0], ly[1][0]) >= 3 else
                         "exclusion risk, a shippable build collides with a delivered one"
                         if max(lx[1][0], ly[1][0]) >= 3 else
                         "in flight, both sides still shippable, fix before the batch goes"),
            "promote": promote,
        })
    sev_order = {"exclusion level, both sides delivered": 4,
                 "exclusion risk, a shippable build collides with a delivered one": 3,
                 "in flight, both sides still shippable, fix before the batch goes": 2,
                 "status unknown on at least one side": 1,
                 "history, at least one side is retired or failed": 0}
    pairs.sort(key=lambda p: (sev_order.get(p["severity"], 0), len(p["promote"]),
                              p["consecutive"], p["track_a"]), reverse=True)

    habits = {
        "ubiquitous_target_filenames": [[n, c] for n, c in df.most_common(14) if c >= 3],
        "repeated_ask_openings": Counter(),
        "repeated_deliverable_ext_pairs": Counter(),
    }
    for c in cards:
        if c.get("prompt"):
            a = " ".join(tokens(c["prompt"]["ask_masked"])[:7])
            if a:
                habits["repeated_ask_openings"][a] += 1
            e = "+".join(c["prompt"]["deliverable_exts"][:2])
            if e:
                habits["repeated_deliverable_ext_pairs"][e] += 1
    habits["repeated_ask_openings"] = [[k, v] for k, v in habits["repeated_ask_openings"].most_common(10) if v > 1]
    habits["ubiquitous_constructions"] = [[k, v] for k, v in open_df.most_common(40)
                                          if v >= max(3, int(0.12 * n)) and len(k.split()) >= 5][:10]
    habits["ubiquitous_step_constructions"] = [[k, v] for k, v in step_df.most_common(30)
                                               if v >= max(3, int(0.12 * n)) and len(k.split()) >= 5][:6]
    habits["repeated_deliverable_ext_pairs"] = [[k, v] for k, v in habits["repeated_deliverable_ext_pairs"].most_common(8) if v > 1]

    promoted = [p for p in pairs if p["promote"]]
    # In pre-flight (one build against the corpus) a clean screen is the expected
    # result and an empty page is useless, so the nearest neighbours are always shown.
    # They are labelled "not promoted" so nobody reads proximity as a finding.
    nearest = []
    if focus:
        nearest = sorted((p for p in pairs if not p["promote"]),
                         key=lambda p: p["track_a"], reverse=True)[:6]
    win = sorted(window)
    result = {"scanned": len(cards),
              "window": ("all builds" if (args.all or focus) else
                         "task%d to task%d (%d builds)" % (win[0], win[-1], len(win)) if win else "empty"),
              "pairs_total": len(pairs),
              "promoted": promoted[:args.top], "nearest_not_promoted": nearest,
              "habits": habits,
              "mechanism_coverage": {c["task"]: c["mechanism_layer"] for c in cards}}
    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print("window: %s" % result["window"])
    print("screened %d builds, %d pairs in scope, %d promoted for adjudication\n"
          % (len(cards), len(pairs), len(promoted)))
    print("== PROMOTED PAIRS (highest first) ==")
    for p in promoted[:args.top]:
        print("\n%s vs %s   surface=%.3f (corpus pct %.0f)%s" % (
            p["pair"][0], p["pair"][1], p["track_a"], 100 * p["track_a_pct"],
            "   [BACK TO BACK]" if p["adjacent"] else "   [TWO APART]" if p["consecutive"] else ""))
        print("   scope: %s" % p["scope"])
        print("   severity: %s" % p["severity"])
        print("   status: [%s] %s | [%s] %s" % (p["status_rank"][0][1], p["status"][0],
                                                p["status_rank"][1][1], p["status"][1]))
        print("   mechanism layer: %s / %s%s" % (
            p["mechanism_layer"][0], p["mechanism_layer"][1],
            "   (labels back-fitted, treat gap/pattern as approximate)"
            if "back-fitted" in p["label_reliability"] else ""))
        print("   promoted by: " + "; ".join(p["promote"]))
        for e in p["evidence_a"]:
            print("   A: " + e)
        for e in p["evidence_b"]:
            print("   B: " + e)
    if focus and nearest:
        print("\n== NEAREST NEIGHBOURS, NOT PROMOTED (proximity is not a finding) ==")
        for p in nearest:
            tb = p["track_b"] or {}
            print("   %s vs %s  surface=%.3f (pct %.0f)%s  gap=%.2f pattern=%.2f decision_family=%s"
                  % (p["pair"][0], p["pair"][1], p["track_a"], 100 * p["track_a_pct"],
                     " CONSEC" if p["consecutive"] else "",
                     tb.get("gap", 0), tb.get("pattern", 0),
                     "yes" if tb.get("decision_family") else "no"))

    print("\n== CORPUS HABITS (not pairwise, these are authorial idiom) ==")
    for n, c in habits["ubiquitous_target_filenames"]:
        print("   filename '%s' appears in %d builds" % (n, c))
    for k, v in habits["repeated_ask_openings"]:
        print("   Main Ask opens '%s' in %d builds" % (k, v))
    for k, v in habits["repeated_deliverable_ext_pairs"]:
        print("   deliverable pair '%s' in %d builds" % (k, v))
    for k, v in habits["ubiquitous_constructions"]:
        print("   prompt construction '%s...' in %d builds" % (k, v))
    for k, v in habits["ubiquitous_step_constructions"]:
        print("   solution step opens '%s...' in %d builds" % (k, v))
    print("\n== MECHANISM COVERAGE ==")
    cov = Counter(result["mechanism_coverage"].values())
    for k, v in cov.most_common():
        print("   %-14s %d builds" % (k, v))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("extract")
    e.add_argument("--repo", default=REPO)
    e.add_argument("--tasks", default=None)
    e.add_argument("--out", default=CACHE)
    e.set_defaults(fn=cmd_extract)
    s = sub.add_parser("screen")
    s.add_argument("--cache", default=CACHE)
    s.add_argument("--focus", default=None, help="pre-flight: one build against every other")
    s.add_argument("--window", type=int, default=15,
                   help="batch size, the last N builds ending at --through (default 15)")
    s.add_argument("--through", default=None, help="newest build in the batch, default the highest numbered")
    s.add_argument("--all", action="store_true", help="ignore the window, screen the whole corpus")
    s.add_argument("--top", type=int, default=25)
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_screen)
    a = ap.parse_args()
    sys.exit(a.fn(a))


if __name__ == "__main__":
    main()
