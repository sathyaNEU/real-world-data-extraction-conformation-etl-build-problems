#!/usr/bin/env python3
"""precut.py, the paper gate between design (stage 2) and build (stage 3).

    python3 .claude/skills/stumping/precut.py taskNN [--quiet]

Reads <task>/DESIGN_NOTE.md and refuses to open stage 3 until the design is argued on paper the way
`stumping` Part 5 sets out: the default competent path written and ending on a wrong answer, the stump
sentence naming that answer, the three rules answered, the readability screen with the decisive rung
silent, the semantic fork table with every alternative ruled out, the 22-axis closure table, the
literal-reader line, the oracles listed, the ask sheet with its pair ceiling and cracker sheet, and
`## Tried and rejected` present. It also runs the prompt gate (voice-check.py) on prompt.txt.

Exit status: 0 every check passed (WARNs allowed), 1 at least one FAIL, 2 the note or the task is missing.
It reads files and runs one script; it spawns no agent and costs nothing.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
VOICE = os.path.join(REPO, ".claude", "skills", "guide-to-prompt", "references", "voice-check.py")
CARDS = os.path.join(REPO, ".claude", "skills", "fingerprint", "cards")

REQUIRED = ["Draw", "Default path", "Stump sentence", "Three rules", "Readability screen",
            "Semantic fork table", "Ladder", "Closure table", "Literal reader", "Oracles", "Ask sheet",
            "Tried and rejected"]
PAIR_CEILING = 40.0
AXES = set(range(1, 23))
STOP = {"the", "and", "with", "from", "that", "this", "than", "into", "over", "under", "about", "ends",
        "golden", "answer", "figure", "candidate", "navigators", "per", "cent"}


def resolve(arg):
    if os.path.isdir(arg):
        return os.path.abspath(arg)
    m = re.fullmatch(r"(?:task)?(\d+)", arg.strip())
    if m:
        return os.path.join(REPO, "task%s" % m.group(1))
    return os.path.abspath(arg)


def sections(text):
    """H2 heading -> body, headings matched case-insensitively on their stripped text."""
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m and not line.startswith("###"):
            if cur is not None:
                out[cur] = "\n".join(buf)
            cur, buf = re.sub(r"[`*]", "", m.group(1)).strip().lower(), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf)
    return out


def section(secs, name):
    key = name.lower()
    if key in secs:
        return secs[key]
    for k, v in secs.items():   # a heading that starts with the name ("## Ladder (targets)")
        if k.startswith(key):
            return v
    return None


def tables(body):
    """Every markdown table in a body as a list of rows (lists of cells), header first, separators dropped."""
    out, cur = [], []
    for line in body.splitlines():
        if line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                continue
            cur.append(cells)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def labelled(body, label):
    m = re.search(r"^\s*(?:[-*]\s*)?\**%s\**\s*:?\**\s*(.+?)\s*$" % re.escape(label), body, re.M | re.I)
    return m.group(1).strip() if m else None


def norm_number(s):
    return re.sub(r"[,\s]", "", s)


def tokens(value):
    nums = [norm_number(n) for n in re.findall(r"\d[\d,]*(?:\.\d+)?", value)]
    words = [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z'-]{3,}", value) if w.lower() not in STOP]
    return nums, words


def names_value(sentence, value):
    nums, words = tokens(value)
    flat = norm_number(sentence)
    if any(n and n in flat for n in nums):
        return True
    low = sentence.lower()
    return any(w in low for w in words) if (words and not nums) else False


def check_note(task_dir, note_text):
    rows = []
    secs = sections(note_text)
    task = os.path.basename(task_dir)

    def row(check, ok, detail, warn=False):
        rows.append((check, "PASS" if ok else ("WARN" if warn else "FAIL"), detail))

    for name in REQUIRED:
        row("section %s" % name, section(secs, name) is not None,
            "## %s present" % name if section(secs, name) is not None else "## %s missing" % name)

    # Draw: the card exists, and the data-native sentence is written somewhere in the note.
    card = os.path.join(CARDS, task + ".json")
    row("card registered", os.path.exists(card), card if os.path.exists(card) else "no card under fingerprint/cards/")
    row("data-native sentence", bool(re.search(r"data[- ]native", note_text, re.I)),
        "named in the note" if re.search(r"data[- ]native", note_text, re.I) else "no data-native sentence found", warn=True)

    # Default path: ends on a wrong answer.
    dp = section(secs, "Default path") or ""
    ends, gold = labelled(dp, "Ends on"), labelled(dp, "Golden")
    row("default path ends on", bool(ends), ends or "no `Ends on:` line")
    row("default path golden", bool(gold), gold or "no `Golden:` line")
    if ends and gold:
        same = norm_number(ends).lower() == norm_number(gold).lower()
        row("default path differs from golden", not same,
            "the default path is not the golden" if not same else "the default path ends on the golden: there is no stump")
    steps = len(re.findall(r"^\s*\d+[.)]\s+\S", dp, re.M))
    row("default path steps", steps >= 2, "%d numbered steps" % steps if steps >= 2 else "fewer than two numbered steps", warn=steps >= 1)

    # Stump sentence names the default path's answer.
    ss = (section(secs, "Stump sentence") or "").strip()
    ss_text = re.sub(r"\s+", " ", ss)
    row("stump sentence", bool(ss_text), ss_text[:140] + ("..." if len(ss_text) > 140 else "") if ss_text else "empty")
    if ss_text and ends:
        row("stump sentence names the default answer", names_value(ss_text, ends),
            "names %r" % ends if names_value(ss_text, ends) else "does not name the default path's answer %r" % ends)

    # Three rules.
    tr = section(secs, "Three rules") or ""
    for label in ("Domain test", "Analyst test", "Layer 1", "Layer 2"):
        v = labelled(tr, label)
        row("three rules: %s" % label, bool(v), (v or "missing")[:120])

    # Readability screen.
    rs = section(secs, "Readability screen") or ""
    tbs = [t for t in tables(rs) if len(t) >= 2]
    if not tbs:
        row("readability screen table", False, "no table with a header and at least one rung")
    else:
        t = tbs[0]
        verdicts = [(r[0], r[-1].strip().lower().strip("`*")) for r in t[1:] if r]
        bad = [r for r, v in verdicts if v not in ("silent", "readable")]
        row("readability verdicts", not bad, "every row silent or readable" if not bad else "verdict not silent/readable on: " + ", ".join(bad))
        dec = [(r, v) for r, v in verdicts if "decisive" in r.lower()]
        row("decisive rung marked", bool(dec), "%d rung(s) marked (decisive)" % len(dec) if dec else "no rung marked (decisive)")
        if dec:
            row("decisive rung silent", all(v == "silent" for _, v in dec),
                "the decisive rung is silent" if all(v == "silent" for _, v in dec) else "the decisive rung is readable: it is dead")

    # Semantic fork table.
    sf = section(secs, "Semantic fork table") or ""
    sf_rows = [r for t in tables(sf) for r in t[1:] if r and re.fullmatch(r"SF\d+", r[0].strip("`* "))]
    row("semantic fork rows", bool(sf_rows), "%d rows" % len(sf_rows) if sf_rows else "no SFn rows")
    empty = [r[0] for r in sf_rows if not r[-1].strip() or r[-1].strip() in ("...", "-", "?")]
    row("semantic forks ruled out", not empty, "every alternative ruled out or convergent" if not empty else "empty `Ruled out by` on: " + ", ".join(empty))
    checks = os.path.join(task_dir, "generator", "checks.py")
    if sf_rows and os.path.exists(checks):
        src = open(checks, encoding="utf-8", errors="replace").read()
        missing = [r[0].strip("`* ") for r in sf_rows if r[0].strip("`* ") not in src]
        row("semantic forks asserted", not missing, "every SF id appears in generator/checks.py" if not missing else "not in checks.py: " + ", ".join(missing))
    elif sf_rows:
        row("semantic forks asserted", True, "generator/checks.py not written yet; each SF id must appear in it", warn=True)

    # Closure table: 22 axes.
    ct = section(secs, "Closure table") or ""
    axes, blank = set(), []
    for t in tables(ct):
        for r in t[1:]:
            m = re.match(r"^\s*(\d{1,2})\b", r[0])
            if m:
                n = int(m.group(1))
                axes.add(n)
                if len(r) < 2 or not r[-1].strip():
                    blank.append(n)
    missing_axes = sorted(AXES - axes)
    row("closure table 22 axes", not missing_axes, "22 of 22 axes" if not missing_axes else "missing axes: " + ", ".join(map(str, missing_axes)))
    row("closure moves filled", not blank, "every axis closed" if not blank else "empty closure on axes: " + ", ".join(map(str, blank)))

    # Literal reader and oracles: present and non-empty.
    for name in ("Literal reader", "Oracles"):
        body = (section(secs, name) or "").strip()
        row("%s written" % name.lower(), bool(body), body.splitlines()[0][:120] if body else "empty")

    # Ask sheet: pair ceiling and the cracker sheet.
    ask = section(secs, "Ask sheet") or ""
    pc = labelled(ask, "Pair ceiling")
    num = re.search(r"\d+(?:\.\d+)?", pc or "")
    if not num:
        row("pair ceiling", False, "no `Pair ceiling:` figure")
    else:
        v = float(num.group(0))
        row("pair ceiling", v <= PAIR_CEILING, "%.1f (ceiling %.0f)" % (v, PAIR_CEILING))
    cr = [t for t in tables(ask) if any("cracker" in c.lower() for c in t[0])]
    if not cr:
        row("cracker sheet", False, "no table whose header names the cracker")
    else:
        verdict = [(r[0], r[-1].strip().lower().strip("`*")) for t in cr for r in t[1:] if r]
        hits = [a for a, v in verdict if v not in ("miss", "misses", "yes", "outside")]
        row("cracker misses every ask", bool(verdict) and not hits,
            "%d ask rows, all missed" % len(verdict) if verdict and not hits else "cracker keeps: " + ", ".join(hits or ["(no rows)"]))

    return rows


def prompt_gate(task_dir):
    """The prompt gate on <task>/prompt.txt, run through voice-check.py with the task's card for the personas."""
    if not os.path.exists(VOICE):
        return ("prompt gate", "WARN", "voice-check.py not found at %s" % VOICE)
    prompt = os.path.join(task_dir, "prompt.txt")
    if not os.path.exists(prompt):
        legacy = os.path.exists(os.path.join(task_dir, "prompt.md"))
        return ("prompt gate", "FAIL", "no prompt.txt" + (" (a prompt.md is a build from before the rule)" if legacy else ""))
    r = subprocess.run([sys.executable, VOICE, "--file", prompt, "--task", os.path.basename(task_dir)],
                       capture_output=True, text=True)
    tail = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith(("FAIL", "WARN"))]
    if r.returncode == 0:
        return ("prompt gate", "PASS", "voice-check.py exit 0" + ("; " + "; ".join(tail) if tail else ""))
    return ("prompt gate", "FAIL", "voice-check.py exit %d: " % r.returncode + "; ".join(tail)[:400])


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    quiet = "--quiet" in argv
    if not args:
        print(__doc__)
        return 2
    task_dir = resolve(args[0])
    note = os.path.join(task_dir, "DESIGN_NOTE.md")
    if not os.path.isdir(task_dir):
        print("no task folder at %s" % task_dir)
        return 2
    if not os.path.exists(note):
        print("no DESIGN_NOTE.md in %s" % task_dir)
        return 2
    rows = check_note(task_dir, open(note, encoding="utf-8", errors="replace").read())
    rows.append(prompt_gate(task_dir))
    fails = [r for r in rows if r[1] == "FAIL"]
    for check, level, detail in rows:
        if quiet and level == "PASS":
            continue
        print("%-4s  %-40s %s" % (level, check, detail))
    print("%s  %s: %d checks, %d FAIL, %d WARN" % ("PASS" if not fails else "FAIL", os.path.basename(task_dir), len(rows),
                                                 len(fails), sum(1 for r in rows if r[1] == "WARN")))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
