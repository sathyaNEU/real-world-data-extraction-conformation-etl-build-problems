#!/usr/bin/env python3
"""freeze.py: prove a targeted repair touched only what it was allowed to touch.

    python3 .claude/skills/build-pipeline/freeze.py snapshot taskNN
    python3 .claude/skills/build-pipeline/freeze.py check taskNN --mode determinism|rubric [--allow KEY,...]

`snapshot` is taken before the first edit of a /fix-determinism or /fix-rubric run and writes
<task>/.freeze.json (git-ignored). `check` runs after the rebuild and compares the build against it.

What is frozen, by mode:

  both modes   the main side: every number in submission.md blocks 1 and 2 (Final Recommendation,
               Critical Components), every figures.json value that equals one of them, the stump
               sentence (pipeline.json `stump`, the card's `stump` and `driver`) and the design note's
               ladder and default-path sections.
  determinism  also the ask side: every number in block 4 (Deliverable Answers), file by file, and every
               other figures.json value. A determinism repair closes a reading; it moves no graded figure.
               The prompt may gain a closing clause; its first question sentence may not change.
  rubric       the ask side is expected to move. The prompt's first question sentence (the call) is
               frozen; the ask sentences may change.

--allow names figures.json keys (dotted paths) the author has accepted moving, each with its reason in
the design note's `## Tried and rejected` or fork table. Exit 0 when nothing frozen moved, 1 when
something did (each change printed), 2 on a usage error or a missing snapshot.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CARDS = os.path.join(REPO, ".claude", "skills", "fingerprint", "cards")

NUM = re.compile(r"(?<![\w./-])[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?![\w/])")
ISO = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
FILE = re.compile(r"\b[\w-]+\.(?:xlsx|csv|pptx|docx|pdf|png|svg|json|md|py|ipynb|sql|parquet|tsv|txt|html|jpg)\b", re.I)


def task_dir(arg):
    t = arg if arg.startswith("task") else "task" + arg
    d = os.path.join(REPO, t)
    if not os.path.isdir(d):
        sys.exit("freeze.py: no folder %s" % d)
    return t, d


def read(path):
    try:
        return open(path, encoding="utf-8").read()
    except OSError:
        return ""


def numbers(text):
    text = FILE.sub(" ", ISO.sub(" ", text))
    return sorted(n.replace(",", "").lstrip("+") for n in NUM.findall(text))


def blocks(sub):
    """submission.md split into its graded blocks; Deliverable Answers kept per file."""
    out, cur, buf, files, curfile = {}, None, [], {}, None
    for line in sub.splitlines():
        if line.startswith("## "):
            if cur:
                out[cur] = "\n".join(buf)
            h = line.lower()
            cur = ("rec" if "final recommendation" in h else "cc" if "critical component" in h else
                   "steps" if "step" in h else "answers" if "deliverable answer" in h else h[3:].strip())
            buf, curfile = [], None
            continue
        if cur == "answers" and line.startswith("### "):
            curfile = line[4:].strip()
            files[curfile] = []
            continue
        buf.append(line)
        if cur == "answers" and curfile:
            files[curfile].append(line)
    if cur:
        out[cur] = "\n".join(buf)
    out["answers_by_file"] = {k: "\n".join(v) for k, v in files.items()}
    return out


def flatten(x, pre=""):
    out = {}
    if isinstance(x, dict):
        for k, v in x.items():
            out.update(flatten(v, "%s%s." % (pre, k)))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            out.update(flatten(v, "%s%d." % (pre, i)))
    else:
        out[pre[:-1]] = str(x)
    return out


def norm(v):
    m = NUM.findall(str(v))
    return m[0].replace(",", "").lstrip("+") if len(m) == 1 else str(v).strip()


def section(note, words):
    """The text of every design-note section whose heading carries one of the words."""
    out, keep = [], False
    for line in note.splitlines():
        if line.startswith("#"):
            keep = any(w in line.lower() for w in words)
        if keep:
            out.append(line)
    return hashlib.sha256("\n".join(out).encode()).hexdigest()[:16] if out else ""


def first_question(prompt):
    sents = re.split(r"(?<=[.?!])\s+", prompt.strip())
    for s in sents[:3]:
        if "?" in s:
            return s.strip()
    return sents[0].strip() if sents else ""


def take(t, d):
    sub = read(os.path.join(d, "submission.md"))
    b = blocks(sub)
    figs_path = os.path.join(d, "generator", "figures.json")
    figs = flatten(json.load(open(figs_path))) if os.path.exists(figs_path) else {}
    main_nums = set(numbers(b.get("rec", "")) + numbers(b.get("cc", "")))
    main_keys = sorted(k for k, v in figs.items() if norm(v) in main_nums)
    prompt = read(os.path.join(d, "prompt.txt")) or read(os.path.join(d, "prompt.md"))
    pipe = {}
    if os.path.exists(os.path.join(d, "pipeline.json")):
        try:
            pipe = json.load(open(os.path.join(d, "pipeline.json")))
        except ValueError:
            pipe = {}
    card = {}
    if os.path.exists(os.path.join(CARDS, t + ".json")):
        card = json.load(open(os.path.join(CARDS, t + ".json")))
    note = read(os.path.join(d, "DESIGN_NOTE.md"))
    return {
        "task": t,
        "rec": numbers(b.get("rec", "")),
        "cc": numbers(b.get("cc", "")),
        "answers": {k: numbers(v) for k, v in b.get("answers_by_file", {}).items()},
        "figures": figs,
        "main_keys": main_keys,
        "call_sentence": first_question(prompt),
        "prompt_chars": len(prompt),
        "stump": pipe.get("stump", ""),
        "card_stump": card.get("stump", ""),
        "card_driver": card.get("driver", ""),
        "ladder": section(note, ("ladder", "rung")),
        "default_path": section(note, ("default path",)),
    }


def snapshot(t, d):
    snap = take(t, d)
    json.dump(snap, open(os.path.join(d, ".freeze.json"), "w"), indent=1)
    print("snapshot %s: %d main-call figures (%d figures.json keys), %d ask files, call sentence frozen"
          % (t, len(set(snap["rec"]) | set(snap["cc"])), len(snap["main_keys"]), len(snap["answers"])))
    return 0


def check(t, d, mode, allow):
    p = os.path.join(d, ".freeze.json")
    if not os.path.exists(p):
        print("freeze.py: no snapshot; run `freeze.py snapshot %s` before the first edit" % t)
        return 2
    old, new = json.load(open(p)), take(t, d)
    bad, notes = [], []

    def frozen(label, a, b):
        if a != b:
            bad.append("%s moved:\n    before %s\n    after  %s" % (label, str(a)[:300], str(b)[:300]))

    frozen("Final Recommendation numbers", old["rec"], new["rec"])
    frozen("Critical Components numbers", old["cc"], new["cc"])
    for k in old["main_keys"]:
        if k in allow:
            continue
        frozen("main-call figure %s" % k, old["figures"].get(k), new["figures"].get(k))
    frozen("stump sentence (pipeline.json)", old["stump"], new["stump"])
    frozen("card stump", old["card_stump"], new["card_stump"])
    frozen("card driver", old["card_driver"], new["card_driver"])
    frozen("design note ladder sections", old["ladder"], new["ladder"])
    frozen("design note default path", old["default_path"], new["default_path"])
    frozen("prompt call sentence", old["call_sentence"], new["call_sentence"])

    ask_moves = []
    for f in sorted(set(old["answers"]) | set(new["answers"])):
        a, b = old["answers"].get(f), new["answers"].get(f)
        if a != b:
            ask_moves.append(f)
    fig_moves = sorted(k for k in set(old["figures"]) | set(new["figures"])
                       if k not in old["main_keys"] and old["figures"].get(k) != new["figures"].get(k))
    if mode == "determinism":
        for f in ask_moves:
            bad.append("Deliverable Answers for %s moved (a determinism repair moves no graded figure)" % f)
        for k in fig_moves:
            if k in allow or old["figures"].get(k) is None:
                continue
            frozen("figure %s" % k, old["figures"].get(k), new["figures"].get(k))
    else:
        notes.append("ask files that moved: %s" % (", ".join(ask_moves) or "none"))
        notes.append("ask figures that moved: %d" % len(fig_moves))
        if not ask_moves and not fig_moves:
            notes.append("WARN nothing on the ask side moved: a rubric repair that changes no ask figure changed nothing graded")
    if new["prompt_chars"] >= 1000:
        bad.append("prompt is %d characters (ceiling 999)" % new["prompt_chars"])

    print("freeze check %s, mode %s" % (t, mode))
    for n in notes:
        print("  " + n)
    if bad:
        print("FAIL: %d frozen item(s) moved" % len(bad))
        for b in bad:
            print("  - " + b)
        return 1
    print("PASS: the main call, the stump and every frozen figure are unchanged")
    return 0


def main(argv):
    if len(argv) < 3 or argv[1] not in ("snapshot", "check"):
        print(__doc__)
        return 2
    t, d = task_dir(argv[2])
    if argv[1] == "snapshot":
        return snapshot(t, d)
    mode, allow = None, set()
    for i, a in enumerate(argv):
        if a == "--mode" and i + 1 < len(argv):
            mode = argv[i + 1]
        if a == "--allow" and i + 1 < len(argv):
            allow = {x.strip() for x in argv[i + 1].split(",") if x.strip()}
    if mode not in ("determinism", "rubric"):
        print("freeze.py check: --mode determinism or --mode rubric")
        return 2
    return check(t, d, mode, allow)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
