#!/usr/bin/env python3
"""figures_check.py: every number in submission.md blocks 1 to 4 is a figure the generator wrote.

    python3 .claude/skills/determinism-check/figures_check.py taskNN [--figures <path>] [--quiet]

The generator (or the independent verifier) writes <task>/generator/figures.json: either a list of the
owed figures, or an object whose values are the owed figures (nested objects and lists are walked).
Each value may be a number or a string carrying the figure as the write-up states it ("13,160,000",
"32.4", "AUD 13,160,000", "1,214 loans"). This script extracts every number from blocks 1 to 4 of
submission.md (Final Recommendation, Critical Components, Step-by-Step Solution, Deliverable Answers)
and fails when one is absent from figures.json: a figure the generator never computed is a figure that
was typed, and 12 of the 16 write-up findings in the judge record were typed figures or steps that do
not recompute as written.

Matching: a write-up number matches a figures.json value when the two are equal after stripping
thousands separators, or numerically within half a unit of the write-up's last shown decimal. Numbers
that are not figures are skipped: list numbering, section numbers, bare integers under 32 with no unit
or sign around them (day numbers, step counts), ISO dates, years 1900 to 2100 standing alone, and file
names. Pass --years to grade years as figures.

Exit status: 0 every figure found, 1 at least one missing, 2 submission.md or figures.json missing.
"""
import json
import os
import re
import signal
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

NUM = re.compile(r"(?<![\w./-])[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?![\w/])")
ISO = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
FILE = re.compile(r"\b[\w-]+\.(?:xlsx|csv|pptx|docx|pdf|png|svg|json|md|py|ipynb|sql|parquet|tsv|txt|html|jpg)\b", re.I)
UNIT_NEAR = re.compile(r"(%|per cent|percent|\$|£|€|AUD|USD|GBP|EUR|NZD|CAD|CHF|x\b|pp\b|points?\b|days?\b|months?\b|years?\b|tons?\b|units?\b|rows?\b|loans?\b|cases?\b)", re.I)


def resolve(arg):
    if os.path.isdir(arg):
        return os.path.abspath(arg)
    m = re.fullmatch(r"(?:task)?(\d+)", arg.strip())
    return os.path.join(REPO, "task%s" % m.group(1)) if m else os.path.abspath(arg)


def blocks_1_to_4(text):
    """The text under the H2 headings numbered 1 to 4, Tags and anything after block 4 excluded."""
    out, keep = [], False
    for line in text.splitlines():
        m = re.match(r"^##\s+(\d+)\.", line)
        if m:
            keep = 1 <= int(m.group(1)) <= 4
            continue
        if line.startswith("## "):
            keep = False
            continue
        if keep:
            out.append(line)
    return "\n".join(out)


def norm(s):
    s = s.replace(",", "").strip()
    try:
        return float(s)
    except ValueError:
        return None


def decimals(s):
    return len(s.split(".")[1]) if "." in s else 0


def writeup_figures(text, years=False):
    text = FILE.sub(" ", text)
    text = ISO.sub(" ", text)
    found = []
    for line in text.splitlines():
        body = re.sub(r"^\s*(?:[-*]|\d+[.)])\s+", "", line)      # list numbering is not a figure
        for m in NUM.finditer(body):
            raw = m.group(0)
            v = norm(raw)
            if v is None:
                continue
            start, end = m.span()
            ctx = body[max(0, start - 12):end + 12]
            bare = re.fullmatch(r"[-+]?\d+", raw) is not None
            if bare and 1900 <= abs(v) <= 2100 and not years and not UNIT_NEAR.search(body[end:end + 8]):
                continue
            if bare and abs(v) < 32 and not UNIT_NEAR.search(ctx) and "**" not in ctx:
                continue
            found.append((raw, v, decimals(raw), line.strip()))
    return found


def flatten(obj, out):
    if isinstance(obj, dict):
        for v in obj.values():
            flatten(v, out)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            flatten(v, out)
    elif isinstance(obj, bool):
        return
    elif isinstance(obj, (int, float)):
        out.append(float(obj))
    elif isinstance(obj, str):
        for m in NUM.finditer(obj):
            v = norm(m.group(0))
            if v is not None:
                out.append(v)


def matches(v, dp, values):
    tol = 0.5 * 10 ** (-dp) if dp else 0.5
    tol = max(tol, 1e-9)
    return any(abs(v - w) <= tol + 1e-9 for w in values)


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    quiet, years = "--quiet" in argv, "--years" in argv
    fig_path = None
    if "--figures" in argv:
        fig_path = argv[argv.index("--figures") + 1]
        args = [a for a in args if a != fig_path]
    if not args:
        print(__doc__)
        return 2
    task_dir = resolve(args[0])
    sub = os.path.join(task_dir, "submission.md")
    fig_path = fig_path or os.path.join(task_dir, "generator", "figures.json")
    if not os.path.exists(sub):
        print("no submission.md in %s" % task_dir)
        return 2
    if not os.path.exists(fig_path):
        print("no figures.json at %s: the generator writes every owed figure there before the write-up is drafted" % fig_path)
        return 2
    values = []
    flatten(json.load(open(fig_path, encoding="utf-8")), values)
    figs = writeup_figures(blocks_1_to_4(open(sub, encoding="utf-8", errors="replace").read()), years=years)
    missing = [(raw, line) for raw, v, dp, line in figs if not matches(v, dp, values)]
    if not quiet:
        for raw, v, dp, line in figs:
            ok = matches(v, dp, values)
            print("%-4s  %-16s %s" % ("PASS" if ok else "FAIL", raw, line[:110]))
    print("%s  %s: %d figures in blocks 1 to 4, %d absent from %s" % (
        "PASS" if not missing else "FAIL", os.path.basename(task_dir), len(figs), len(missing), os.path.relpath(fig_path, task_dir)))
    return 1 if missing else 0


if __name__ == "__main__":
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(main(sys.argv[1:]))
