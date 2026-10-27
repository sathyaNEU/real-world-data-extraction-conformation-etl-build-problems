#!/usr/bin/env python3
"""precut.py, the paper gate between design (stage 2) and build (stage 3).

    python3 .claude/skills/stumping/precut.py taskNN [--quiet]

Reads <task>/DESIGN_NOTE.md and refuses to open stage 3 until the design is argued on paper the way
`stumping` Part 5 sets out: the default competent path written and ending on a wrong answer, the stump
sentence naming that answer, the three rules answered, the readability screen with the decisive rung
silent, the semantic fork table with every alternative ruled out, the 22-axis closure table, the
literal-reader line, the oracles listed, the ask sheet with its pair ceiling, mirror leakage and cracker
sheet, and `## Tried and rejected` present. It also runs the prompt gate (voice-check.py) on prompt.txt.

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
VOCAB = os.path.join(REPO, ".claude", "skills", "fingerprint", "vocab.json")
# The client's check before a build ships, one label per point (stumping 1.1).
THREE_RULES = ("Task type", "Domain test", "Swap", "Layer 1", "Layer 2", "Decisive step", "Not semantics",
               "Not rule application", "Analyst test", "Estimand", "No decoy", "No certified replay", "Lesson")
PAIR_CEILING = 60.0    # the build target under the bar of 70 (supplemental Part 0)
MIRROR_CEILING = 50.0   # per cent of ask weight the best response off the call may keep, target two fifths (supplemental Part 1.1)
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


def sections(text, dupes=None):
    """H2 heading -> body, headings matched case-insensitively on their stripped text.

    A repeated heading used to overwrite the earlier one silently, so a note carrying a duplicated or
    half-spliced section passed every check on whichever copy came last. task199's note reached a
    committed state with two "the judge's FIX_NOW, answered" headings and a "tried and rejected`) |"
    heading sitting inside a table cell, and this gate read it as clean. Repeats are collected into
    `dupes` for the caller to fail on.
    """
    out, cur, buf, seen = {}, None, [], []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m and not line.startswith("###"):
            if cur is not None:
                out[cur] = "\n".join(buf)
            cur, buf = re.sub(r"[`*]", "", m.group(1)).strip().lower(), []
            if cur in seen and dupes is not None:
                dupes.append(cur)
            seen.append(cur)
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


# The field's named methods, grouped into families so that two lines naming the same method with different
# wording ("the hazard of a violation", "the hazard by time on supervision") still collide.
METHOD_FAMILIES = {
    "test linking": ("concordance", "equipercentile", "equating", "linking", "percentile match",
                     "vertical scale", "score conversion"),
    "regression prediction": ("regression", "ordinary least squares", " ols ", "logistic", "predicted value"),
    "survival and hazard": ("hazard", "survival curve", "survival function", "kaplan", "proportional hazards",
                            "life table", "left truncation", "time to event"),
    "likelihood fitting": ("maximum likelihood", " mle ", "likelihood ratio"),
    "resampling": ("bootstrap", "cross-validation", "jackknife", "permutation test"),
    "shrinkage": ("credibility weighting", "shrinkage", "empirical bayes", "partial pooling"),
    "standardisation": ("standardisation", "standardization", "reweighting", "direct adjustment", "z-score"),
    "causal design": ("propensity", "difference in differences", "instrumental variable", "regression discontinuity",
                      "synthetic control"),
    "triangle development": ("chain ladder", "development triangle", "loss development", "run-off"),
    "extreme value": ("log-pearson", "extreme value", "generalised pareto", "return period"),
    "time series": ("arima", "exponential smoothing", "state space", "seasonal decomposition"),
    "flow balance": ("stock and flow", "max flow", "balance identity"),
    "backtest selection": ("backtest", "back-test", "out-of-sample selection"),
    # A field's own named PROCEDURE collides as surely as its named statistic. Two independent reconnaissance
    # passes found the statistical list alone clears the colliding lines it was built to catch, so the domain
    # procedures go in beside them.
    "audit sampling": ("attribute sample", "attribute sampling", "deviation rate", "sampling unit",
                       "tolerable rate", "monetary unit sampling", "sampling risk"),
    "record linkage": ("record linkage", "entity resolution", "probabilistic linkage", "fellegi",
                       "match weight", "blocking key", "clerical review"),
    "coverage estimation": ("capture-recapture", "dual system", "dual-system", "coverage estimation",
                            "post-enumeration"),
    "mass balance": ("mass balance", "material balance", "conservation identity", "closure error"),
    "emission inventory": ("emission factor", "tier 2 method", "tier-2 method", "activity data"),
    "occupancy and capacity": ("concurrency", "occupancy ceiling", "queueing", "erlang",
                               "utilisation standard", "capacity factor"),
    "seasonal adjustment": ("seasonal adjustment", "x-13", "x-12", "trading day adjustment"),
    "risk adjustment": ("risk adjustment", "case mix", "case-mix", "hierarchical condition"),
    "limit compliance testing": ("delegated authority", "authority schedule", "limit compliance",
                                 "segregation of duties", "three-way match"),
    "reserve measurement": ("loss reserve", "provision measurement", "ibnr", "incurred but not reported"),
}


def method_terms(line):
    """The families of field-named methods a Three-rules line mentions.

    Families, not raw strings: the same method named two ways in two lines must still collide.
    """
    low = " " + (line or "").lower() + " "
    return {fam for fam, pats in METHOD_FAMILIES.items() if any(pat in low for pat in pats)}


def labelled(body, label):
    """The text after `Label:`, with its wrapped continuation lines, up to a blank line, a new bullet, a table row,
    a heading or the next `Label:` line."""
    m = re.search(r"^\s*(?:[-*]\s*)?\**%s\**\s*:?\**\s*(.+?)\s*$" % re.escape(label), body, re.M | re.I)
    if not m:
        return None
    parts = [m.group(1).strip()]
    for line in body[m.end():].splitlines()[1:]:
        s = line.strip()
        if (not s or re.match(r"^([-*]\s|\d+[.)]\s|\||#)", s)
                or re.match(r"^\**[A-Z][A-Za-z0-9 ]{0,30}\**\s*:", s)):
            break
        parts.append(s)
    return " ".join(parts)


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


def build_status(task_dir):
    try:
        import json
        return json.load(open(os.path.join(task_dir, "pipeline.json"))).get("status") or ""
    except Exception:
        return ""


def task_type_serves(task, line):
    """Rule 1: the task type the note names is one of the card's domain's task types and serves its objective.
    Returns (True | False | None, detail); None when the card or vocabulary cannot be read."""
    import json
    try:
        card = json.load(open(os.path.join(CARDS, task + ".json")))
        vocab = json.load(open(VOCAB))
    except Exception:
        return None, "card or vocab.json unreadable; Task type line not checked"
    client = vocab.get("client_domains", {})
    obj, dom = card.get("objective"), card.get("domain")
    doms = [dom] if dom in client else ([card.get("client_domain")] if card.get("client_domain") else
                                        (vocab.get("house_domains", {}).get(dom, {}).get("maps_to") or []))
    low = re.sub(r"[^a-z0-9]+", " ", line.lower())
    named = []
    for d in doms:
        for key, objs in client.get(d, {}).get("task_types", {}).items():
            if key.replace("-", " ") in low:
                named.append((d, key, objs))
    if not named:
        return False, "names none of %s's task types (guide-to-prompt/references/domains/README.md)" % (", ".join(d for d in doms if d) or dom)
    hit = [(d, k) for d, k, objs in named if obj in objs]
    if hit:
        return True, "%s/%s serves %s" % (hit[0][0], hit[0][1], obj)
    return False, "%s serves %s, not %s" % (named[0][1], ", ".join(named[0][2]), obj)


def check_note(task_dir, note_text):
    rows = []
    dupes = []
    secs = sections(note_text, dupes)
    task = os.path.basename(task_dir)

    def row(check, ok, detail, warn=False):
        rows.append((check, "PASS" if ok else ("WARN" if warn else "FAIL"), detail))

    row("no repeated H2 heading", not dupes,
        "each H2 appears once" if not dupes
        else "repeated, so the earlier copy is unread and unchecked: %s"
             % ", ".join(sorted(set(dupes))))

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

    # Three rules: one labelled line per point of the client's own pre-ship check (stumping 1.1). A build that
    # has shipped meets a missing line as a WARN; a build being designed or repaired is refused.
    tr = section(secs, "Three rules") or ""
    shipped = build_status(task_dir) in ("SHIPPED", "SHIPPED_APPROVED", "RETIRED")
    for label in THREE_RULES:
        v = labelled(tr, label)
        ok = bool(v) and len(v) >= 20
        row("three rules: %s" % label, ok, (v or "missing")[:120] if ok else (v or "missing") + " (one line, 20 characters or more)",
            warn=shipped and label not in ("Domain test", "Analyst test", "Layer 1", "Layer 2"))
    at = labelled(tr, "Analyst test")
    if at and ends:
        row("analyst test names the default answer", names_value(at, ends),
            "names %r" % ends if names_value(at, ends) else "the analyst test does not name the default path's answer %r" % ends,
            warn=shipped)
    tt = labelled(tr, "Task type")
    if tt:
        ok, detail = task_type_serves(task, tt)
        row("task type serves the objective", ok, detail, warn=shipped or ok is None)

    # The reflex collision: if the field's own named method for the deciding quantity IS the decisive step,
    # the readability screen's test 3 is failed by construction and a competent analyst reaches the golden.
    # Three builds died this way (a domain's reflex estimator, a textbook weight, a test concordance).
    dt, ds = labelled(tr, "Domain test"), labelled(tr, "Decisive step")
    if dt and ds:
        shared = method_terms(dt) & method_terms(ds)
        row("the field's method is not the decisive step", not shared,
            "the Domain test and Decisive step lines share no method term"
            if not shared else
            "both lines name %s: if the field's own method for the deciding quantity is the golden, a competent "
            "analyst applies it by reflex and the screen's test 3 cannot be silent"
            % ", ".join(sorted(shared)), warn=True)

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
        want = [r[0].strip("`* ") for r in sf_rows]
        # Whole-token matching: a bare substring test passes SF1 on a file that only carries SF15.
        missing = [i for i in want if not re.search(r"\b%s\b" % re.escape(i), src)]
        # A re-rooted build whose checks.py still belongs to the dead architecture passes every id by
        # coincidence, because the old file carries a longer SF run for entirely different forks. The
        # signature is an SF id asserted in checks.py that the note does not carry.
        asserted = set(re.findall(r"\bSF\d{1,3}\b", src))
        orphans = sorted(asserted - set(want), key=lambda x: int(x[2:]))
        if missing:
            row("semantic forks asserted", False, "not in checks.py: " + ", ".join(missing))
        elif orphans:
            row("semantic forks asserted", False,
                "checks.py asserts %d SF id(s) the fork table does not carry (%s), so it was written for another "
                "architecture and every id above matched by coincidence; this build's forks owe real assertions"
                % (len(orphans), ", ".join(orphans)))
        else:
            row("semantic forks asserted", True, "every SF id appears in generator/checks.py as its own token")
    elif sf_rows:
        ids = ", ".join(r[0].strip("`* ") for r in sf_rows)
        row("semantic forks asserted", False,
            "generator/checks.py not written yet, so this check is not run: %d rows still owe an assertion (%s)"
            % (len(sf_rows), ids), warn=True)

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

    # Ask sheet: pair ceiling, mirror leakage and the cracker sheet.
    ask = section(secs, "Ask sheet") or ""
    pc = labelled(ask, "Pair ceiling")
    num = re.search(r"\d+(?:\.\d+)?", pc or "")
    if not num:
        row("pair ceiling", False, "no `Pair ceiling:` figure")
    else:
        v = float(num.group(0))
        row("pair ceiling", v <= PAIR_CEILING, "%.1f (ceiling %.0f)" % (v, PAIR_CEILING))
    ml = labelled(ask, "Mirror leakage")
    mnum = re.search(r"\d+(?:\.\d+)?", ml or "")
    if not mnum:
        row("mirror leakage", False, "no `Mirror leakage:` figure (supplemental-stumping Part 7)", warn=True)
    else:
        v = float(mnum.group(0))
        row("mirror leakage", v < MIRROR_CEILING, "%.1f per cent of ask weight (under %.0f)" % (v, MIRROR_CEILING))
    # The ceiling and the leakage have to come from code run on the cut pack, not from prose.
    # Two builds in one wave shipped a sheet whose figure was the complement or the mirror of the
    # truth (supplemental-stumping Part 7), and this gate reads the sheet, so the sheet has to name
    # the script that produced the numbers.
    mb = labelled(ask, "Measured by")
    script = (mb or "").strip()
    found = ""
    if script:
        for cand in re.findall(r"[\w./-]+\.py", script):
            for base in (os.path.join(task_dir, cand), os.path.join(task_dir, "generator", os.path.basename(cand)), cand):
                if os.path.exists(base):
                    found = base
                    break
            if found:
                break
    row("ceiling measured by a script", bool(found),
        ("%s" % found) if found else
        ("names no existing script: %r" % script if script else
         "no `Measured by:` line naming the script that ran the cracker on the cut pack"))

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
