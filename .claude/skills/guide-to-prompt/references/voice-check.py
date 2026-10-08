#!/usr/bin/env python3
"""Measure prompt voice and structure across builds, so variety is checked rather than asserted.

    python3 .claude/skills/guide-to-prompt/references/voice-check.py            # last 12 builds
    python3 .claude/skills/guide-to-prompt/references/voice-check.py task84     # one draft against the rest
    python3 .claude/skills/guide-to-prompt/references/voice-check.py --all

Run from the repo root. Read `prompt-voice.md` for what the numbers mean and what to do about
them. Nothing here is a pass or fail on its own: a phrase repeated in three of twelve builds is a
habit forming, and the same phrase in eight of twelve is what the reviewer sees when they read the
batch in one sitting.
"""

import collections
import glob
import os
import re
import statistics
import sys

WINDOW = 12

# Opening moves, keyed to the table in prompt-voice.md. Best effort on the first two sentences:
# the classifier exists to show the spread across a batch, not to grade one prompt.
MOVES = [
    ("role-first",        r"^(?:I |We )(?:run|lead|direct|plan|own|manage|chair|head|administer|"
                          r"supervise|coordinate|look after|am the|am head|sit with)\b"),
    ("deliverable-first", r"^(?:Start with|Build|Give me|Hand |Draft|Open with|Write|Put |Lead with)\b"),
    ("question-first",    r"^(?:Which|Who|What|How|Where|When|Whether|Do we|Should we)\b.*\?"),
    ("options-first",     r"^[A-Z][^.?!]{0,60}?,\s+[^.?!]{0,60}?,?\s+or\s+[^.?!]{0,40}?[:.]"),
    ("number-first",      r"^The (?:number|figure|one number|count|total|answer)\b"),
    ("rule-first",        r"^(?:The (?:rule|standard|test|protocol|policy|framework|contract|"
                          r"roster rule|screen|scoring)|Under the|A [a-z ]+ only)\b"),
    ("constraint-first",  r"^(?:The [a-z ]+ can only|Only so many|[A-Z][a-z]+ can take on|"
                          r"One [a-z ]+ (?:crew|team|does)|We can (?:only|run))\b"),
    ("evidence-first",    r"^(?:A (?:year|season|month|quarter)[^.]{0,60}(?:sits|is sitting)|"
                          r"[A-Z][^.]{0,60}(?:sits|sit) in the (?:folder|pack|share))\b"),
    ("stakes-first",      r"^(?:Miss(?:ing)? |Every [a-z ]+ that |Buying |[A-Z][^.]{0,60}"
                          r"is not a (?:paperwork|small))\b"),
    ("calendar-first",    r"^(?:The [a-z ]+ (?:board|council|committee|review|vote)s?\b|"
                          r"On \d|In (?:January|February|March|April|May|June|July|August|"
                          r"September|October|November|December)\b)"),
]

# The left column is spec and must survive; the right column is the wording we reach for.
# See the requirement-against-carrier table in prompt-voice.md.
CARRIERS = [
    ("hands the pack over",      r"[Ee]verything (?:my|our) [a-z ]+ works? from is in"),
    ("hands the pack over",      r"is in the (?:folder|pack|share)\b"),
    ("commissions a text file",  r"\bWrite it up as\b"),
    ("commissions a workbook",   r"\bHand the workings over as\b"),
    ("commissions a chart",      r"\b(?:Then chart it|chart it so)\b"),
    ("justifies the workbook",   r"rather than take my word for it"),
    ("asks for a chart title",   r"and a title that states"),
    ("asks for a marked line",   r"drawn (?:as|across as) a labelled (?:line|horizontal line)"),
    ("asks the table to tie",    r"total row that ties"),
    ("says the visual is quick", r"(?:reads|sees|see) it at a glance"),
    ("plants a decoy belief",    r"has been working on the basis that"),
    ("demands one value",        r"no range(?:s)? and no\b"),
    ("frames the rest as prop",  r"(?:is|are) there to stand (?:that|the) (?:one )?(?:number|figure|call)"),
    ("prefers a number",         r"rather (?:meet it|than an argument|point at)"),
]

FAMILIES = {
    "Data": ("csv", "tsv", "json", "xlsx", "parquet"),
    "Visual": ("pptx", "png", "svg", "html", "jpg"),
    "Text": ("pdf", "docx"),
    "Code": ("py", "ipynb", "sql", "r"),
}
EXTS = tuple(e for group in FAMILIES.values() for e in group)


def task_no(path):
    m = re.search(r"task(\d+)", path)
    return int(m.group(1)) if m else -1


def body(path):
    """The prompt as the solver reads it: markdown headings and code fences stripped."""
    raw = open(path, encoding="utf-8", errors="replace").read()
    raw = re.sub(r"^```.*?^```", "", raw, flags=re.M | re.S)
    raw = re.sub(r"^\s*#.*$", "", raw, flags=re.M)
    raw = re.sub(r"^\s*>.*$", "", raw, flags=re.M)
    return raw.strip()


def first_sentence(text):
    flat = re.sub(r"\s+", " ", text).strip()
    m = re.match(r".{0,240}?[.?!](?:\s|$)", flat)
    return (m.group(0) if m else flat[:240]).strip()


def classify(text):
    opening = first_sentence(text)
    for name, pattern in MOVES:
        if re.match(pattern, opening):
            return name
    return "other"


def deliverables(text):
    names = re.findall(r"`?\b([A-Za-z0-9_\-]+\.(?:%s))\b`?" % "|".join(EXTS), text, re.I)
    return sorted({n.lower() for n in names})


def _overlap(a, b, run=4):
    """True when two n-grams share a word run, so one family prints one row."""
    aw, bw = a.split(), b.split()
    aruns = {" ".join(aw[i:i + run]) for i in range(len(aw) - run + 1)}
    return any(" ".join(bw[i:i + run]) in aruns for i in range(len(bw) - run + 1))


def ngrams(text, n):
    words = re.findall(r"[a-z']+", re.sub(r"`[^`]*`", " FILE ", text).lower())
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


COMMISSION = ("build", "give", "write", "put", "send", "make", "produce", "draft",
              "create", "prepare", "deliver", "generate", "provide", "pull", "add")

# Economy. See prompt-economy.md for what these mean and what to do about a breach.
# BENCH is the median over 25 prompts the client paid out on, measured once and recorded here as a
# number. Nothing from that set is stored in this repo and none of it is ever copied into a build.
# LIMIT is the paid-out set's own p90 or observed maximum, so a flag means the draft sits outside
# anything that has been paid out rather than merely above their average. The two distributions
# overlap on wps, longest and ctx%, which is why those limits are loose on purpose.
BENCH = {"words": 227, "wps": 21.6, "ctxpct": 22.4, "longest": 90, "tags": 0, "because": 0}
LIMIT = {"words": 330, "wps": 33.0, "ctxpct": 46.0, "longest": 180, "tags": 3, "because": 2}

ROUNDING_TAG = (r"whole (?:number|tonne|unit|dollar|pound|euro|case|household|record|USD|GBP|EUR)s?"
                r"|(?:one|two|three|\d+) decimal places?|a decimal place|to the nearest \w+"
                r"|at full precision|percentage points? to")
# A convention sentence sets rounding for a block of figures rather than for one figure, which is
# what H12 asks for. It needs a rounding word and a word that gives it scope.
CONV_SCOPE = (r"\bunless\b|\bexcept\b|\bthroughout\b|\beverywhere\b|\bfor reporting\b"
              r"|\bby default\b|\ball figures\b|\bevery figure\b|\bcounts are\b"
              r"|\bwhere I ask\b|\bunless I\b")


def sentences(text):
    """Flattened, and not split on a list marker, which would read as a very short sentence."""
    flat = re.sub(r"\s+", " ", text).strip()
    return [s.strip() for s in re.split(r"(?<![0-9])(?<=[.!?])\s+", flat) if s.strip()]


def economy(text):
    """The rows in prompt-economy.md section 5, measured off one prompt."""
    sents = sentences(text)
    paras = paragraphs(text)
    wc = len(re.findall(r"[A-Za-z']+", text))
    tags = re.findall(ROUNDING_TAG, text, re.I)
    convention = any(re.search(ROUNDING_TAG, s, re.I) and re.search(CONV_SCOPE, s, re.I)
                     for s in sents)
    ctx = len(paras[0].split()) if paras else 0
    return {
        "words": wc,
        "wps": round(wc / max(len(sents), 1), 1),
        "context": ctx,
        # A share, not a word count: ours and theirs run at the same share (22.8 against 22.4),
        # so the absolute number only tracks total length and would flag by construction. A
        # single-paragraph prompt is trivially 100 per cent and is not judged on this row.
        "ctxpct": round(100.0 * ctx / max(wc, 1), 1) if len(paras) > 1 else 0.0,
        "longest": max((len(p.split()) for p in paras), default=0),
        "short": any(len(s.split()) < 8 for s in sents),
        "tags": len(tags),
        "conv": convention,
        "because": len(re.findall(r"\bbecause\b", text, re.I)),
    }


def paragraphs(text):
    return [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def last_sentence(text):
    parts = re.findall(r"[^.?!]+[.?!]", re.sub(r"\s+", " ", text).strip())
    return parts[-1].strip() if parts else text.strip()


def main(argv):
    paths = sorted(glob.glob("task*/prompt.md"), key=task_no)
    if not paths:
        sys.exit("no task*/prompt.md found. Run from the repo root.")

    args = [a for a in argv if not a.startswith("-")]
    if args:
        wanted = {re.sub(r"[^0-9]", "", a) for a in args}
        focus = [p for p in paths if str(task_no(p)) in wanted]
        found = {str(task_no(p)) for p in focus}
        missing = sorted(wanted - found, key=lambda n: int(n or 0))
        if missing:
            # A named build with no prompt on disk would otherwise fall back to the window
            # silently, and the per-build gate would pass having checked nothing.
            sys.stderr.write(
                "voice-check: no prompt found for " + ", ".join("task" + m for m in missing)
                + "\n  looked for: " + ", ".join(f"task{m}/prompt.md" for m in missing)
                + "\n  the draft has to be on disk at that path before the per-build check"
                  " means anything.\n")
            return 2
        window = paths[-WINDOW:]
        selected = sorted(set(window) | set(focus), key=task_no)
    elif "--all" in argv:
        selected, focus = paths, []
    else:
        selected, focus = paths[-WINDOW:], []

    texts = {p: body(p) for p in selected}
    names = ", ".join(os.path.dirname(p) for p in selected)
    print(f"voice-check over {len(selected)} builds: {names}\n")

    # 1. Opening move spread.
    print("OPENING MOVE".ljust(22) + "builds")
    moves = collections.Counter(classify(t) for t in texts.values())
    for move, count in moves.most_common():
        bar = "#" * count
        flag = "  <-- concentrated" if count > max(2, len(selected) // 3) else ""
        print(f"  {move:<20}{count:>2}  {bar}{flag}")
    print(f"  {len(moves)} distinct moves across {len(selected)} builds\n")

    # 2. Where the role sits, and the literal opening verb.
    print("OPENING CLAUSE")
    for path, text in texts.items():
        mark = "*" if path in focus else " "
        print(f" {mark}{os.path.dirname(path):<9} [{classify(text):<17}] {first_sentence(text)[:88]}")
    print()

    # 3. Carrier wording, the phrases that are ours rather than the spec's.
    print("CARRIER WORDING".ljust(46) + "builds")
    for label, pattern in CARRIERS:
        hits = [p for p, t in texts.items() if re.search(pattern, t)]
        if not hits:
            continue
        flag = "  <-- calcified" if len(hits) >= max(3, len(selected) // 3) else ""
        shown = pattern if len(pattern) < 40 else pattern[:37] + "..."
        print(f"  {label:<26}/{shown:<40}/ {len(hits):>2}{flag}")
        if len(hits) >= max(3, len(selected) // 3):
            print(f"    {', '.join(os.path.dirname(p) for p in hits)}")
    print()

    # 4. Anything else repeating that the carrier list has not caught yet.
    print(f"UNLISTED REPEATS (6+ word runs shared by a third of the batch)")
    shared = collections.Counter()
    for path, text in texts.items():
        for g in ngrams(text, 6):
            shared[g] += 1
    floor = max(3, len(selected) // 3)
    rows = [(c, g) for g, c in shared.items() if c >= floor]
    rows.sort(key=lambda r: (-r[0], -len(r[1]), r[1]))
    printed, seen = 0, []
    for count, gram in rows:
        # one row per family of overlapping runs, and nothing the carrier list already names
        if any(gram in s or s in gram or _overlap(gram, s) for s in seen):
            continue
        if re.search(r"whole number|decimal place|decimal places|whole (?:usd|gbp|cad|dollars)", gram):
            continue
        if any(re.search(pat, gram, re.I) for _, pat in CARRIERS):
            continue
        seen.append(gram)
        print(f"  {count:>2}  \"{gram}\"")
        printed += 1
        if printed >= 12:
            break
    if not printed:
        print("  none")
    print()

    # 5. Structural variety: length, file count, format mix.
    print("SHAPE OF THE ASK")
    lengths, counts = [], []
    fam_counter, ext_counter = collections.Counter(), collections.Counter()
    for path, text in texts.items():
        words = len(re.findall(r"[A-Za-z']+", text))
        files = deliverables(text)
        lengths.append(words)
        counts.append(len(files))
        for f in files:
            ext = f.rsplit(".", 1)[-1]
            ext_counter[ext] += 1
            for fam, exts in FAMILIES.items():
                if ext in exts:
                    fam_counter[fam] += 1
        mark = "*" if path in focus else " "
        print(f" {mark}{os.path.dirname(path):<9} {words:>4} words  {len(files)} files  "
              f"{', '.join(files)}")
    print(f"\n  words   median {statistics.median(lengths):.0f}, "
          f"range {min(lengths)} to {max(lengths)}")
    print(f"  files   median {statistics.median(counts):.0f}; "
          f"one-file builds {sum(1 for c in counts if c == 1)} of {len(counts)}; "
          f"at the three-file ceiling {sum(1 for c in counts if c >= 3)}")
    print("  formats " + ", ".join(f".{e} {c}/{len(selected)}" for e, c in ext_counter.most_common()))
    unused = [e for e in EXTS if e not in ext_counter]
    print("  unused  " + (", ".join("." + e for e in unused) if unused else "none"))
    for fam in FAMILIES:
        if fam not in fam_counter:
            print(f"  <-- no {fam} deliverable anywhere in this batch")
    for ext, c in ext_counter.items():
        if c == len(selected):
            print(f"  <-- every build in this batch ships a .{ext}")

    # 6. Economy. The budget and what a breach means are in prompt-economy.md.
    print()
    print("ECONOMY".ljust(12) + "words  w/sent  ctx%  longest  <8w  tags conv  because")
    econ = {p: economy(t) for p, t in texts.items()}
    for path, e in econ.items():
        mark = "*" if path in focus else " "
        over = [k for k in ("words", "wps", "ctxpct", "longest", "tags", "because")
                if e[k] > LIMIT[k]]
        if "tags" in over and e["conv"]:
            over.remove("tags")          # H12 is satisfied by a stated convention
        if not e["short"]:
            over.append("no short sentence")
        print(f" {mark}{os.path.dirname(path):<10}{e['words']:>5} {e['wps']:>7} {e['ctxpct']:>5}"
              f" {e['longest']:>8} {'yes' if e['short'] else ' no':>4} {e['tags']:>5}"
              f" {'yes' if e['conv'] else ' no':>4} {e['because']:>8}"
              + ("   <-- " + ", ".join(over) if over else ""))
    med = {k: statistics.median([e[k] for e in econ.values()])
           for k in ("words", "wps", "ctxpct", "longest", "tags", "because")}
    print(f"  {'median':<10}{med['words']:>5.0f} {med['wps']:>7.1f} {med['ctxpct']:>5.1f}"
          f" {med['longest']:>8.0f} {sum(e['short'] for e in econ.values()):>3}/{len(econ)}"
          f" {med['tags']:>5.0f} {sum(e['conv'] for e in econ.values()):>3}/{len(econ)}"
          f" {med['because']:>8.0f}")
    print(f"  {'paid-out':<10}{BENCH['words']:>5} {BENCH['wps']:>7} {BENCH['ctxpct']:>5}"
          f" {BENCH['longest']:>8} {'18/25':>7} {BENCH['tags']:>5} {'  n/a':>4}"
          f" {BENCH['because']:>8}    <-- median over 25 paid-out prompts")
    print(f"  {'flag over':<10}{LIMIT['words']:>5} {LIMIT['wps']:>7} {LIMIT['ctxpct']:>5}"
          f" {LIMIT['longest']:>8} {'':>7} {LIMIT['tags']:>5} {'':>4} {LIMIT['because']:>8}"
          "    <-- the paid-out p90 or max, not their median")

    # 7. The hierarchy read (H13 / P1). Inputs only, the judgement is yours.
    for path in sorted(focus, key=task_no):
        paras = paragraphs(texts[path])
        if len(paras) < 2:
            continue
        print(f"\nHIERARCHY READ  {os.path.dirname(path)}   (judge these, the script does not)")
        print("  context ends on   " + last_sentence(paras[0])[:150])
        print("  then each paragraph opens")
        for para in paras[1:]:
            head = " ".join(para.split()[:9])
            bare = para.split()[0].strip('`"\'').lower() in COMMISSION
            print(f"    {'<--' if bare else '   '} {head}")
        if any(p.split()[0].strip('`"\'').lower() in COMMISSION for p in paras[1:]):
            print("  <-- a paragraph opens on a bare commissioning verb, so it reads as")
            print("      one output among several rather than as support for the call")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
