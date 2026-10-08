#!/usr/bin/env python3
"""Grade an independent solver's answers against submission.md with the rubric's own weights.

    python3 .claude/skills/solver-round/grade.py task100 <solver_output.json> [--label "round 1, plain"]

The solver output is the StructuredOutput the /solve command collects:

    {"main_call": "...", "deliverables": [{"file": "x.xlsx", "answers": [{"ask": 1, "value": "..."}]}],
     "path": ["..."], "confidence": "...", "notes": "..."}

The golden is read from submission.md: block 1's bold sentence is the main call, block 4's numbered
items under each `### file` heading are the asks, each item's figures (numbers and capitalised
names) being the gradable tokens. Weights: recommendation 35, instruction-following 7, asks 58 split
equally across block 4 items. A miss on the main call keeps 5 of the 35 (the rubric's surviving
components). An item counts as cracked at 80 per cent of its tokens.

The score is a proxy for the portal's grade, read for one purpose: did this solver land the main
call, and which asks did it keep. Writes <task>/solver_rounds/<label>.md and prints the summary;
appends one row to <task>/pipeline.json under solver_rounds.
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
W_REC, W_IF, W_ASK, R_SURVIVE = 35.0, 7.0, 58.0, 5.0
LANDED_OVERRIDE = None
NUM = re.compile(r"(?<![\w.])[-+]?\d{1,3}(?:,\d{3})+(?:\.\d+)?|(?<![\w.,])[-+]?\d+\.\d+|(?<![\w.,])\d+(?![\w.,])")
STOP = set("the a an and or of to in on at by for with from as is are was were be been not no yes per each every all any both first second third last next out into over under about above below than that this these those which who whom whose where when while because so if then its it their there here they them we our you your up down off back".split())


def tokens(text):
    nums, names = [], []
    for n in NUM.findall(text):
        s = n.replace(",", "").lstrip("+")
        try:
            v = float(s)
        except ValueError:
            continue
        if "." not in s and (abs(v) < 3 or 1900 <= v <= 2100):
            continue  # list indices and years
        nums.append((n, v, len(s.split(".")[1]) if "." in s else 0))
    for m in re.finditer(r"\b([A-Z][a-zA-Z'’]+(?:[ -][A-Z][a-zA-Z'’]+){0,4})\b", text):
        w = m.group(1)
        if w.split()[0].lower() in STOP or len(w) < 4 or w in ("Deliverable Answers", "Final Recommendation"):
            continue
        names.append(w)
    return nums, list(dict.fromkeys(names))


def num_hit(golden, dp, text):
    """A number in the solver text equal to the golden within half a unit of its last decimal place,
    or 0.5 per cent, whichever is wider."""
    tol = max(0.5 * 10 ** (-dp), 0.005 * abs(golden))
    for n in NUM.findall(text):
        try:
            v = float(n.replace(",", "").lstrip("+"))
        except ValueError:
            continue
        if abs(v - golden) <= tol + 1e-9:
            return True
    return False


def name_hit(name, text):
    return re.search(re.escape(name), text, re.I) is not None


def parse_submission(sub):
    b1 = re.search(r"## 1\..*?(?=\n## 2\.)", sub, re.S)
    b1 = b1.group(0) if b1 else ""
    call = re.search(r"\*\*(.+?)\*\*", b1, re.S)
    call = re.sub(r"\s+", " ", call.group(1)) if call else b1
    b4 = re.search(r"## 4\..*", sub, re.S)
    b4 = b4.group(0) if b4 else ""
    files, cur = {}, None
    for line in b4.split("\n"):
        m = re.match(r"^### (.+)$", line.strip())
        if m:
            cur = m.group(1).strip().strip("`")
            files[cur] = []
            continue
        if cur is None:
            continue
        if re.match(r"^\d+\.\s", line.strip()):
            files[cur].append(line.strip())
        elif line.startswith((" ", "\t")) and files[cur] and line.strip():
            files[cur][-1] += "\n" + line.strip()
    return call, files


def solver_text(out, file=None):
    parts = []
    for d in out.get("deliverables", []):
        if file is None or d.get("file", "").lower().strip("`") == file.lower() or Path(d.get("file", "")).name.lower() == Path(file).name.lower():
            for a in d.get("answers", []):
                parts.append("%s: %s" % (a.get("ask", ""), a.get("value", "")))
    return "\n".join(parts)


def grade(task, out, label):
    sub = (task / "submission.md").read_text(errors="ignore")
    call, files = parse_submission(sub)
    # recommendation
    c_nums, c_names = tokens(call)
    s_call = out.get("main_call", "") or ""
    c_hits = sum(1 for _, v, dp in c_nums if num_hit(v, dp, s_call)) + sum(1 for n in c_names if name_hit(n, s_call))
    c_total = len(c_nums) + len(c_names)
    landed = c_total > 0 and c_hits >= max(1, int(round(0.8 * c_total)))
    if LANDED_OVERRIDE is not None:
        landed = LANDED_OVERRIDE  # the reader's call outranks the token match: a wrong set can share most names
    rec_pts = W_REC if landed else R_SURVIVE * (c_hits / c_total if c_total else 0)
    # instruction following: an answer set for every deliverable
    files_answered = {Path(d.get("file", "")).name.lower() for d in out.get("deliverables", [])}
    if_frac = (sum(1 for f in files if Path(f).name.lower() in files_answered) / len(files)) if files else 0
    if_pts = W_IF * if_frac
    # asks
    items = [(f, i, it) for f, its in files.items() for i, it in enumerate(its, 1)]
    per_item = W_ASK / len(items) if items else 0
    rows, ask_pts, cracked = [], 0.0, 0
    whole = solver_text(out) + "\n" + s_call + "\n" + " ".join(out.get("path", []) or [])
    for f, i, it in items:
        nums, names = tokens(it)
        text = solver_text(out, f) or whole
        hits = sum(1 for _, v, dp in nums if num_hit(v, dp, text)) + sum(1 for n in names if name_hit(n, text))
        total = len(nums) + len(names)
        frac = hits / total if total else 0.0
        if frac >= 0.8:
            cracked += 1
        ask_pts += per_item * frac
        rows.append((f, i, hits, total, frac))
    score = rec_pts + if_pts + ask_pts
    lines = ["# solver round: %s" % label, "",
             "**Proxy score %.1f / 100** (recommendation %.1f of %.0f, instruction %.1f of %.0f, asks %.1f of %.0f). Main call %s. %d of %d ask items cracked (80 per cent of tokens)." % (
                 score, rec_pts, W_REC, if_pts, W_IF, ask_pts, W_ASK, "LANDED" if landed else "missed", cracked, len(items)),
             "", "## Main call", "", "golden: %s" % call, "", "solver: %s" % s_call, "",
             "tokens matched %d of %d (%s)" % (c_hits, c_total, ", ".join([n for n, _, _ in c_nums] + c_names)[:300]), "",
             "## Asks", "", "| file | item | tokens hit | of | share |", "|---|---|---|---|---|"]
    for f, i, h, t, fr in rows:
        lines.append("| %s | %d | %d | %d | %.0f%% |" % (f, i, h, t, 100 * fr))
    lines += ["", "## Solver's path", ""] + ["%d. %s" % (k, p) for k, p in enumerate(out.get("path", []) or [], 1)]
    lines += ["", "confidence: %s" % out.get("confidence", ""), "", "notes: %s" % out.get("notes", ""), ""]
    for d in out.get("deliverables", []):
        lines.append("### %s (solver's answers)" % d.get("file", ""))
        for a in d.get("answers", []):
            lines.append("- %s: %s" % (a.get("ask", ""), str(a.get("value", ""))[:600]))
        lines.append("")
    rdir = task / "solver_rounds"
    rdir.mkdir(exist_ok=True)
    safe = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-") or "round"
    (rdir / ("%s.md" % safe)).write_text("\n".join(lines))
    state_p = task / "pipeline.json"
    state = json.loads(state_p.read_text()) if state_p.exists() else {"task": task.name}
    state.setdefault("solver_rounds", []).append({"label": label, "date": date.today().isoformat(), "score": round(score, 1),
                                                   "landed": landed, "cracked": cracked, "items": len(items)})
    state_p.write_text(json.dumps(state, indent=1))
    print("%s: %.1f  main call %s  asks cracked %d/%d  ->  %s" % (label, score, "LANDED" if landed else "missed", cracked, len(items), rdir / ("%s.md" % safe)))
    return score, landed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("task")
    ap.add_argument("output", help="solver output JSON")
    ap.add_argument("--label", default="round")
    ap.add_argument("--landed", choices=["yes", "no"], help="override the token match on the main call after reading both sentences")
    a = ap.parse_args()
    global LANDED_OVERRIDE
    LANDED_OVERRIDE = {"yes": True, "no": False}.get(a.landed)
    task = Path(a.task)
    if not task.is_dir():
        t = a.task if a.task.startswith("task") else "task" + a.task
        task = REPO / t
    out = json.loads(Path(a.output).read_text())
    score, landed = grade(task, out, a.label)
    return 2 if landed else (1 if score >= 40 else 0)


if __name__ == "__main__":
    sys.exit(main())
