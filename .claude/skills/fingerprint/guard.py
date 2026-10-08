#!/usr/bin/env python3
"""
guard.py, the draw-time half of the fingerprint system.

Every build in this repo has a fingerprint card in cards/taskNN.json: what kind of project it is
(domain, subdomain, objective, shape, decision, world, spine, deliverables) and what drives its
difficulty (gap, pattern, generators, Gate G mechanism, calibration form, the driver sentence). A
new build writes its card when the draw is fixed, before the ladder is written and before any data
is cut, and this script checks it against every card already on file.

  guard.py recent [--n 12]            the last builds in draw order, one line each
  guard.py coverage                   what is spent and what has never been drawn
  guard.py suggest [--n 3] [--seed S] independent draws pushed toward fresh territory
  guard.py new taskNN                 print a blank card to fill (redirect it to a file)
  guard.py check <card.json>          BLOCK, WARN or PASS for a proposed draw
  guard.py register <card.json>       check, then file the card under cards/
  guard.py validate [taskNN ...]      every filed card against vocab.json
  guard.py show taskNN                one card, readable
  guard.py nearest taskNN|<card.json> the closest drivers in the corpus
  guard.py surface taskNN             after the pack is cut: clone-check's mechanical screen, then people
  guard.py names --geo <place> --seed N   draw fresh personas from that locale's name pool
  guard.py people [taskNN]            the corpus name index, or one build's personas checked against it

Run from anywhere. Exit status: 0 for PASS or WARN, 1 for BLOCK or an invalid card, 2 for a usage
error. Nothing here spawns an agent or calls a model, so it costs nothing and it runs on every draw.
The cards record identity only. Whether a build stumped is the shipped ledger's business, and
nothing in this script writes to the ledger.
"""

import argparse
import importlib.util
import json
import math
import os
import random
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
REPO = SKILL_DIR.parent.parent.parent
# FINGERPRINT_CARDS points the guard at another folder of cards, for testing a rule change.
CARDS_DIR = Path(os.environ.get("FINGERPRINT_CARDS") or (SKILL_DIR / "cards"))
VOCAB_PATH = SKILL_DIR / "vocab.json"
LEDGER = REPO / ".claude" / "skills" / "stumping" / "references" / "shipped-ledger.md"
CLONE_FP = REPO / ".claude" / "skills" / "clone-check" / "fingerprint.py"
VOICE = REPO / ".claude" / "skills" / "guide-to-prompt" / "references" / "voice-check.py"
PEOPLE_CACHE = SKILL_DIR / ".cache" / "people.json"
sys.path.insert(0, str(SKILL_DIR))
import business  # noqa: E402  (people and business furniture)

# How far back the bans reach. RECENT is "your last build" widened to three, because builds are
# often drawn two or three at a time and a reviewer reads them as one batch. WINDOW is the batch a
# reviewer holds, which is what overuse is measured against.
RECENT = 3
WINDOW = 12

# Driver-sentence similarity (TF-IDF cosine over content words and word pairs). At BLOCK_SIM the
# card must carry a one-line differentiation against that build; at WARN_SIM the build is listed so
# the author reads it. Calibrated on the 2026-10-02 backfill: across pairs of drivers from different
# slots the 99.9th percentile sits under 0.10 and the only pair above 0.19 was a byte-identical
# rebuild (0.88). Text similarity separates same-mechanism pairs only weakly (AUC about 0.6), so it
# is a near-duplicate catcher; the mechanism check is the structural signature in test.same_puzzle.
BLOCK_SIM = 0.30
WARN_SIM = 0.12
NICHE_SIM = 0.50

# Canonical objective per shape, from guide-to-prompt/references/shapes/README.md. The shape does
# not fix the tag; suggest uses this only to prefer a natural fit.
SHAPE_OBJECTIVE = {
    "01": "descriptive-distribution", "02": "forecasting", "03": "etl", "04": "descriptive-distribution",
    "05": "descriptive-distribution", "06": "descriptive-distribution", "07": "experiment-causal",
    "08": "descriptive-distribution", "09": "descriptive-distribution", "10": "descriptive-distribution",
    "11": "experiment-causal", "12": "root-cause", "13": "forecasting", "14": "descriptive-distribution",
    "15": "etl", "16": "descriptive-distribution", "17": "anomaly-detection", "18": "root-cause",
}

# What each shape naturally decides, so suggest does not pair a dial with an allocation.
SHAPE_DECISIONS = {
    "01": {"ranked_slate_under_cap"}, "02": {"quantity_figure", "date_or_period"},
    "03": {"quantity_figure"}, "04": {"dial_setting"}, "05": {"allocation_to_total"},
    "06": {"schedule_or_sequence", "date_or_period"}, "07": {"pick_one_of_n", "go_hold_or_stop"},
    "08": {"dial_setting", "quantity_figure"}, "09": {"pick_one_of_n", "quantity_figure"},
    "10": {"designation_set", "go_hold_or_stop"}, "11": {"go_hold_or_stop", "pick_one_of_n"},
    "12": {"root_cause_named"}, "13": {"date_or_period", "go_hold_or_stop", "dial_setting"},
    "14": {"dial_setting", "quantity_figure"}, "15": {"conformed_dataset"},
    "16": {"ranked_slate_under_cap", "pick_one_of_n"}, "17": {"date_or_period", "designation_set"},
    "18": {"root_cause_named"},
}
# Gate G mechanisms that only make sense under one objective.
GATE_OBJECTIVE = {"etl_conformance": {"etl"}, "forecasting": {"forecasting"}}

LIVE_DOMAINS = None      # filled from vocab: the six, without the legacy keys
LIVE_OBJECTIVES = None
DRAWABLE_GATE_G = ["forecasting", "method_or_model_selection", "binding_constraint",
                   "decomposition_attribution", "signal_vs_noise_or_hold", "confirm_surface_read",
                   "etl_conformance"]

EM_DASH = chr(0x2014)


# ------------------------------------------------------------------ loading

def load_vocab():
    global LIVE_DOMAINS, LIVE_OBJECTIVES
    v = json.loads(VOCAB_PATH.read_text())
    LIVE_DOMAINS = [k for k in v["domains"] if not k.startswith("legacy")]
    LIVE_OBJECTIVES = [k for k in v["objectives"] if not k.startswith("legacy")]
    return v


def task_num(task):
    m = re.search(r"(\d+)", str(task or ""))
    return int(m.group(1)) if m else 0


def load_cards(cards_dir=CARDS_DIR):
    cards = []
    for p in sorted(Path(cards_dir).glob("task*.json")):
        try:
            c = json.loads(p.read_text())
        except Exception as e:
            sys.stderr.write("unreadable card %s: %s\n" % (p.name, e))
            continue
        c["_path"] = str(p)
        c["_num"] = task_num(c.get("task") or p.stem)
        cards.append(c)
    return sorted(cards, key=draw_key)


def draw_key(c):
    return (c.get("drawn") or "0000-00-00", c.get("_num", task_num(c.get("task"))))


def load_candidate(arg, cards):
    """A path to a JSON card, or a task id already on file."""
    p = Path(arg)
    if p.is_file():
        c = json.loads(p.read_text())
        c["_path"] = str(p)
        c["_num"] = task_num(c.get("task"))
        return c
    for c in cards:
        if c.get("task") == arg:
            return c
    raise SystemExit("no card file or filed task called %s" % arg)


def ledger_status():
    """The strongest ledger status per task, for severity only. Reuses clone-check's parser so the
    two tools can never disagree about what a row says."""
    try:
        spec = importlib.util.spec_from_file_location("clone_fp", str(CLONE_FP))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        rows = mod.parse_ledger(str(LEDGER))
        out = {}
        for task, lst in rows.items():
            best = (0, "unknown")
            for r in lst:
                rk = mod.status_rank(r.get("status"))
                if rk[0] > best[0]:
                    best = rk
            out[task] = best[1]
        return out
    except Exception:
        return {}


# ------------------------------------------------------------------ text similarity

STOP = set("""a an and are as at be been being but by can could did do does doing for from had has
have having he her here hers him his how i if in into is it its itself just me more most my no nor
not of off on once only or other our out over own same she should so some such than that the their
them then there these they this those through to too under until up very was we were what when where
which while who whom why will with would you your one two three each every any all both either
neither whole new old also per via onto upon within without across against between among because
before after above below during whether rather instead yet still even ever never much many few lot
less least made make makes making gets get got set sets""".split())


def stem(w):
    for suf, rep, minlen in (("ies", "y", 5), ("sses", "ss", 5), ("es", "", 5), ("s", "", 4),
                             ("ing", "", 6), ("ed", "", 5)):
        if w.endswith(suf) and len(w) >= minlen:
            return w[: -len(suf)] + rep
    return w


def terms(text):
    words = [stem(w) for w in re.findall(r"[a-z]+", (text or "").lower()) if w not in STOP and len(w) > 2]
    return words + ["%s_%s" % (a, b) for a, b in zip(words, words[1:])]


class Tfidf:
    def __init__(self, docs):
        self.df = Counter()
        for d in docs:
            self.df.update(set(terms(d)))
        self.n = max(1, len(docs))

    def vec(self, text):
        tf = Counter(terms(text))
        v = {t: (1 + math.log(c)) * math.log(1 + self.n / (1 + self.df.get(t, 0))) for t, c in tf.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {t: x / norm for t, x in v.items()}

    def sim(self, a, b):
        va, vb = self.vec(a), self.vec(b)
        return sum(x * vb.get(t, 0.0) for t, x in va.items())


# ------------------------------------------------------------------ card helpers

def first(lst):
    for x in lst or []:
        if x and x != "none":
            return x
    return None


def decisive_mech(c):
    """The pattern that carried the decisive rung, or the decisive generator when no A to E pattern
    did. This is the thing Part 6.1 bans reusing."""
    pats = [x for x in (c.get("pattern") or []) if x]
    if pats and pats[0] != "none":
        return pats[0]
    # "none" written first means no A to E pattern carried the decisive rung, so the decisive
    # G-code did, and a pattern listed after it is only the frame.
    return first(c.get("generators")) or (first(pats) if pats else None)


def label(c):
    arch = c.get("architecture")
    show = arch not in (None, "", "only") and (c.get("lineage") or arch not in ("v1",))
    return "%s%s" % (c.get("task"), (" (%s)" % arch) if show else "")


def drivers_of(c):
    """The card's own driver, plus every lineage driver, as (who, text, entry) for the corpus."""
    out = []
    if c.get("driver"):
        out.append((label(c), c["driver"], c))
    for e in c.get("lineage") or []:
        if e.get("driver"):
            who = "%s (%s, lineage)" % (c.get("task"), e.get("architecture") or "earlier")
            merged = dict(e)
            merged.setdefault("task", c.get("task"))
            out.append((who, e["driver"], merged))
    return out


def norm_names(c):
    names = (c.get("world") or {}).get("invented_names") or []
    return {re.sub(r"\s+", " ", n.strip().lower()) for n in names if n and len(n.strip()) > 3 and " " in n.strip()}


def fmt_set(c):
    exts = []
    for d in c.get("deliverables") or []:
        m = re.search(r"\.([A-Za-z0-9]+)$", d.strip())
        if m:
            exts.append(m.group(1).lower())
    return tuple(sorted(set(exts)))


def spine_key(c):
    s = c.get("spine") or {}
    ent = re.sub(r"[^a-z ]", " ", (s.get("entity") or "").lower()).split()
    grn = re.sub(r"[^a-z ]", " ", (s.get("grain") or "").lower()).split()
    return (" ".join(stem(w) for w in ent if w not in STOP), " ".join(stem(w) for w in grn if w not in STOP))


def real_source(c):
    src = ((c.get("spine") or {}).get("source") or "").strip().lower()
    if not src or src.startswith("synthetic") or src in ("none", "n/a"):
        return None
    return src


# ------------------------------------------------------------------ validation

def validate_card(c, vocab, strict=False):
    errs, warns = [], []
    t = c.get("task", "")
    if not re.fullmatch(r"task\d+", t or ""):
        errs.append("task must read taskNN, got %r" % t)
    if c.get("_path") and Path(c["_path"]).parent.resolve() == CARDS_DIR.resolve():
        if Path(c["_path"]).stem != t:
            errs.append("file name %s does not match task %s" % (Path(c["_path"]).name, t))

    def enum(field, allowed, value, required=True):
        if value in (None, "", []):
            if required:
                errs.append("%s is empty" % field)
            return
        if value not in allowed:
            errs.append("%s=%r is not in vocab.json" % (field, value))

    enum("domain", vocab["domains"], c.get("domain"))
    dom = c.get("domain")
    if dom in vocab["subdomains"]:
        enum("subdomain", vocab["subdomains"][dom], c.get("subdomain"))
    enum("objective", vocab["objectives"], c.get("objective"))
    enum("shape", vocab["shapes"], c.get("shape"))
    enum("decision_type", vocab["decision_types"], c.get("decision_type"))
    enum("answer_unit", vocab["answer_units"], c.get("answer_unit"), required=strict)
    enum("gate_g", vocab["gate_g"], c.get("gate_g"))
    enum("calibration_form", vocab["calibration_forms"], c.get("calibration_form"), required=strict)
    enum("context_artifact", vocab["context_artifacts"], c.get("context_artifact"), required=strict)
    enum("role_family", vocab["role_families"], c.get("role_family"), required=strict)
    enum("scoring_unit", vocab["scoring_units"], c.get("scoring_unit"), required=False)
    if c.get("opening_move"):
        enum("opening_move", vocab["opening_moves"], c.get("opening_move"))
    enum("forum", vocab["forums"], c.get("forum"), required=strict)
    enum("forcing_event", vocab["forcing_events"], c.get("forcing_event"), required=strict)
    enum("org_family", vocab["org_families"], c.get("org_family"), required=strict)
    if strict and not ((c.get("world") or {}).get("people")):
        errs.append("world.people is empty: draw the personas with guard.py names before the pack exists")
    for g in c.get("gap") or []:
        enum("gap", vocab["gaps"], g)
    for p in c.get("pattern") or []:
        enum("pattern", vocab["patterns"], p)
    for g in c.get("generators") or []:
        enum("generators", vocab["generators"], g)
    for i, e in enumerate(c.get("lineage") or []):
        for f, allowed in (("domain", vocab["domains"]), ("objective", vocab["objectives"]),
                           ("gate_g", vocab["gate_g"]), ("decision_type", vocab["decision_types"])):
            if e.get(f) and e[f] not in allowed:
                errs.append("lineage[%d].%s=%r is not in vocab.json" % (i, f, e[f]))
        for g in e.get("gap") or []:
            if g not in vocab["gaps"]:
                errs.append("lineage[%d].gap %r is not in vocab.json" % (i, g))
        for p in e.get("pattern") or []:
            if p not in vocab["patterns"]:
                errs.append("lineage[%d].pattern %r is not in vocab.json" % (i, p))
    if not (c.get("driver") or "").strip():
        errs.append("driver is empty: one sentence, the decisive move with domain nouns stripped")
    if not ((c.get("world") or {}).get("geography") or "").strip():
        errs.append("world.geography is empty")
    if strict:
        if not c.get("gap"):
            errs.append("gap is empty: a draw names its decisive gap")
        if not (first(c.get("pattern")) or first(c.get("generators"))):
            errs.append("pattern and generators are both empty: a draw names the decisive pattern or G-code")
        if not (c.get("stump") or "").strip():
            errs.append("stump is empty: name the wrong committed answer a competent solver files, and the step that lands them there")
        if not (c.get("niche") or "").strip():
            errs.append("niche is empty")
        if not ((c.get("spine") or {}).get("entity") or "").strip():
            errs.append("spine.entity is empty: say what one row of the spine is")
    diff = c.get("differentiation")
    if diff is not None and not isinstance(diff, dict):
        errs.append("differentiation must be an object {taskNN: one line}")

    def walk(x, path="card"):
        if isinstance(x, str):
            if EM_DASH in x:
                errs.append("em dash in %s" % path)
        elif isinstance(x, dict):
            for k, v in x.items():
                if not str(k).startswith("_"):
                    walk(v, "%s.%s" % (path, k))
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk(v, "%s[%d]" % (path, i))
    walk(c)
    if c.get("domain", "").startswith("legacy") or c.get("objective", "") == "legacy-retired":
        warns.append("legacy domain or objective: fine on an old card, never on a new draw")
    return errs, warns


# ------------------------------------------------------------------ the check

def check(cand, cards, vocab, status=None):
    """Every rule names the axis to redraw. BLOCK rules come from stumping Part 6.1's standing bans
    and similarity test, clone-check's hard tells, and the spec's legality gates. WARN rules are
    overuse across the batch a reviewer reads in one sitting."""
    status = status or {}
    findings = []

    def add(level, rule, msg, against=(), fix=""):
        findings.append({"level": level, "rule": rule, "msg": msg, "against": list(against), "fix": fix})

    errs, _ = validate_card(cand, vocab, strict=True)
    for e in errs:
        add("BLOCK", "card", e, fix="fill the card from the design note's DRAW block")

    me = cand.get("task")
    others = [c for c in cards if c.get("task") != me]
    own = [c for c in cards if c.get("task") == me]
    # This slot's own history: the filed card when the candidate is a re-root replacing it, every
    # lineage entry on file, and the lineage the draft itself lists. Never the candidate itself.
    own_entries, seen_txt = [], set()
    for c in own + [cand]:
        for who, txt, e in drivers_of(c):
            if e is cand or txt in seen_txt or (txt == cand.get("driver") and e.get("architecture") == cand.get("architecture")):
                continue
            seen_txt.add(txt)
            own_entries.append((who, txt, e))
    ordered = sorted(others, key=draw_key)
    recent = ordered[-RECENT:]
    window = ordered[-WINDOW:]
    last = ordered[-1:] if ordered else []
    diff = {k: v for k, v in (cand.get("differentiation") or {}).items() if (v or "").strip()}

    def tasks(cs):
        return [label(c) + (" [%s]" % status.get(c.get("task")) if status.get(c.get("task")) else "") for c in cs]

    # Legality, which is spec rather than taste.
    if cand.get("domain") not in (LIVE_DOMAINS or []):
        add("BLOCK", "legal.domain", "domain %r is not one of the six accepted domains" % cand.get("domain"),
            fix="draw one of the six")
    if cand.get("objective") not in (LIVE_OBJECTIVES or []):
        add("BLOCK", "legal.objective", "objective %r is not one of the six Axis 1 objectives" % cand.get("objective"),
            fix="draw one of the six")
    if cand.get("gate_g") in ("legacy_surface_read",):
        add("BLOCK", "legal.gate_g", "a surface-read rejection is banned at any depth (Gate G v3)",
            fix="draw one of the seven FINE-numbers mechanisms")
    if cand.get("gate_g") == "statistical_rigor":
        add("BLOCK", "legal.gate_g", "statistical_rigor is supporting only and never the sole defence",
            fix="pair it under one of the seven FINE-numbers mechanisms and name that one")

    # Part 6.1 standing bans, against the builds a reviewer reads alongside this one.
    hit = [c for c in recent if (c.get("domain"), c.get("objective")) == (cand.get("domain"), cand.get("objective"))]
    if hit:
        add("BLOCK", "ban.pairing", "domain plus objective pairing repeats a recent build", tasks(hit),
            "redraw the domain or the objective")
    hit = [c for c in recent if c.get("domain") == cand.get("domain") and c.get("subdomain") == cand.get("subdomain")
           and cand.get("subdomain") not in (None, "", "other")]
    if hit:
        add("BLOCK", "ban.subdomain", "domain and subdomain both repeat a recent build", tasks(hit),
            "draw a subdomain you have not used recently")
    dm = decisive_mech(cand)
    hit = [c for c in recent if dm and decisive_mech(c) == dm]
    if hit:
        add("BLOCK", "ban.pattern", "the decisive pattern %s repeats a recent build" % dm, tasks(hit),
            "redraw the pattern that carries the decisive rung")
    cf = cand.get("calibration_form")
    hit = [c for c in recent if cf and cf not in ("none", "other") and c.get("calibration_form") == cf]
    if hit:
        add("BLOCK", "ban.calibration", "calibration form %s repeats a recent build" % cf, tasks(hit),
            "redraw the calibration form")
    rf = cand.get("role_family")
    hit = [c for c in recent if rf and rf != "other" and c.get("role_family") == rf]
    if hit:
        add("BLOCK", "ban.role", "stakeholder role family %s repeats a recent build" % rf, tasks(hit),
            "redraw the stakeholder role")
    ca = cand.get("context_artifact")
    hit = [c for c in recent if ca and ca not in ("none", "other") and c.get("context_artifact") == ca]
    if hit:
        add("BLOCK", "ban.artifact", "context-artifact type %s repeats a recent build" % ca, tasks(hit),
            "redraw the context-artifact type")
    sk = spine_key(cand)
    hit = [c for c in recent if sk[0] and spine_key(c) == sk]
    if hit:
        add("BLOCK", "ban.spine", "spine entity and grain (%s / %s) repeat a recent build" % sk, tasks(hit),
            "redraw what one row of the spine is")
    rs = real_source(cand)
    if rs:
        hit = [c for c in others if real_source(c) == rs]
        if hit:
            near = [c for c in hit if c in recent]
            add("BLOCK" if near else "WARN", "ban.source",
                "the spine derives from the same real dataset (%s)" % rs, tasks(hit),
                "draw a different source dataset")
    sh = cand.get("shape")
    hit = [c for c in ordered[-2:] if sh and sh not in ("other", "single-figure") and c.get("shape") == sh]
    if hit:
        add("BLOCK", "ban.shape", "prompt shape %s repeats one of the last two builds" % sh, tasks(hit),
            "pick a different shape, the shape is visible in the prompt and the deliverables")

    # Two structural signatures. The first is Part 6.1's similarity test: gap, pattern and decision
    # type all repeating is the same puzzle in new clothes. The second is clone-check's Template
    # tier, "the gap, the pattern and the decisive rung line up": the same gap and pattern defeating
    # the solver through the same Gate G mechanism is the same driver even when the decision is cut
    # differently. On the 2026-10-02 backfill each collides on under 4 per cent of card pairs, and
    # only the second catches the one Template clone on record (task86 v1 against task72 v2).
    def struct_test(rule, label, key):
        mine = key(cand)
        if not all(mine):
            return
        same = []
        for c in others:
            for who, _, e in drivers_of(c):
                if key(e) == mine:
                    same.append((c, who))
        in_win = sorted({who for c, who in same if c in window})
        older = sorted({who for c, who in same if c not in window})
        if in_win:
            add("BLOCK", rule, "%s all repeat inside the batch (%s)" % (label, ", ".join(str(m) for m in mine)),
                in_win, "redraw the gap or the pattern, a new world does not fix this")
        undiffed = [w for w in older if w.split(" ")[0] not in diff]
        if undiffed:
            spent = len({who.split(" ")[0] for _, who in same})
            fix = ("this signature is spent in %d earlier builds, so redrawing the gap or the pattern is cheaper "
                   "than %d differentiation lines" % (spent, spent) if spent >= 4 else
                   "add differentiation {taskNN: one line naming how the driver differs} or redraw")
            add("BLOCK", rule + "_older", "%s all repeat an older build, and the card carries no differentiation for it"
                % label, undiffed, fix)
        elif older:
            add("NOTE", rule + "_older", "%s repeat an older build, differentiated" % label, older)
        # A re-root that lands back on its own dead architecture repeats the failure it was meant to fix.
        if me not in diff:
            for who, _, e in own_entries:
                if key(e) == mine:
                    add("BLOCK", "test.own_lineage",
                        "this slot already tried the same %s (%s)" % (label, e.get("fate") or "an earlier architecture"),
                        [who], "a re-root has to move the decisive rung, or add differentiation {%s: one line}" % me)

    struct_test("test.same_puzzle", "decisive gap, decisive pattern and decision type",
                lambda c: (first(c.get("gap")), decisive_mech(c), c.get("decision_type") or None))
    struct_test("test.same_driver", "decisive gap, decisive pattern and Gate G mechanism",
                lambda c: (first(c.get("gap")), decisive_mech(c), c.get("gate_g") or None))

    # Driver sentences, the reskinned clone that no axis can see.
    corpus = []
    for c in others:
        corpus.extend((c, who, txt) for who, txt, _ in drivers_of(c))
    for who, txt, e in own_entries:
        corpus.append((e, who + " [this slot]", txt))
    tf = Tfidf([t for _, _, t in corpus] + [cand.get("driver") or ""])
    sims = sorted(((tf.sim(cand.get("driver") or "", txt), c, who, txt) for c, who, txt in corpus),
                  key=lambda x: -x[0])
    blocked = [(s, who) for s, c, who, _ in sims if s >= BLOCK_SIM and who.split(" ")[0] not in diff]
    for s, who in blocked:
        add("BLOCK", "driver.text", "driver sentence reads as the same insight (similarity %.2f)" % s, [who],
            "redraw the decisive move, or add differentiation {%s: one line}" % who.split(" ")[0])
    for s, c, who, _ in sims:
        if WARN_SIM <= s < BLOCK_SIM or (s >= BLOCK_SIM and who.split(" ")[0] in diff):
            add("WARN" if who.split(" ")[0] not in diff else "NOTE", "driver.near",
                "driver sentence is close (similarity %.2f)%s" % (s, ", differentiated" if who.split(" ")[0] in diff else ""),
                [who], "read that build's design note before writing the ladder")

    # Hard tells from clone-check: a shared invented name is never produced by two independent draws.
    mine = norm_names(cand)
    for c in others:
        shared = mine & norm_names(c)
        if shared:
            add("BLOCK", "tell.names", "shares invented names: %s" % ", ".join(sorted(shared)), [label(c)],
                "rename the fiction")

    # People. Ordinary names that are not recycled, drawn from a locale pool rather than invented.
    idx = business.load_index(REPO, PEOPLE_CACHE)
    for lvl, rule, msg, against in business.check_people((cand.get("world") or {}).get("people"), idx,
                                                         [c.get("task") for c in window], me):
        add(lvl, rule, msg, against, "draw replacements with guard.py names --geo <geography> --seed <task number>")

    # Business furniture: who decides, under what deadline, in what kind of organisation. Cards
    # written before these fields existed are read off their prompt.
    def forums_of(c):
        return {c["forum"]} if c.get("forum") else set(business.derived_elements(REPO, c.get("task"))["forums"])

    def events_of(c):
        return {c["forcing_event"]} if c.get("forcing_event") else set(business.derived_elements(REPO, c.get("task"))["events"])

    fo, ev, of = cand.get("forum"), cand.get("forcing_event"), cand.get("org_family")
    if fo and fo != "other":
        hit = [c for c in recent if fo in forums_of(c)]
        if hit:
            add("BLOCK", "ban.forum", "the deciding forum (%s) repeats a recent build" % fo, tasks(hit),
                "put the call in front of a different forum, or with no formal forum at all")
        n_fo = sum(1 for c in others if fo in forums_of(c))
        if n_fo >= max(5, int(0.15 * len(others))):
            add("WARN", "overuse.forum", "%s decides in %d builds already" % (fo, n_fo),
                fix="see guard.py coverage for the forums that are rarely used")
    if ev and ev != "other":
        hit = [c for c in recent if ev in events_of(c)]
        if hit:
            add("BLOCK", "ban.forcing_event", "the forcing event (%s) repeats a recent build" % ev, tasks(hit),
                "force the call with a different kind of event")
        n_ev = sum(1 for c in others if ev in events_of(c))
        if n_ev >= max(8, int(0.25 * len(others))):
            add("WARN", "overuse.forcing_event", "%s forces the call in %d builds already" % (ev, n_ev))
    if of and of != "other":
        hit = [c for c in recent if business.org_family(c) == of]
        if hit:
            add("BLOCK", "ban.org_family", "the organisation family (%s) repeats a recent build" % of, tasks(hit),
                "set the build inside a different kind of organisation")
        n_of = sum(1 for c in others if business.org_family(c) == of)
        if n_of >= max(6, int(0.12 * len(others))):
            add("WARN", "overuse.org_family", "%s is the organisation in %d builds already" % (of, n_of))

    # Overuse across the batch, and the softer Part 6.1 axes.
    def count(field, value, cs):
        return sum(1 for c in cs if value and c.get(field) == value)

    n_dom = count("domain", cand.get("domain"), window)
    if n_dom >= 4:
        add("WARN", "overuse.domain", "domain used in %d of the last %d builds" % (n_dom, len(window)),
            fix="prefer an under-used domain, see coverage")
    n_obj = count("objective", cand.get("objective"), window)
    if n_obj >= (6 if cand.get("objective") == "forecasting" else 4):
        add("WARN", "overuse.objective", "objective used in %d of the last %d builds" % (n_obj, len(window)))
    n_sh = count("shape", sh, window) if sh not in ("other", "single-figure") else 0
    if n_sh >= 3:
        add("WARN", "overuse.shape", "shape used in %d of the last %d builds" % (n_sh, len(window)))
    gg = cand.get("gate_g")
    hit = [c for c in ordered[-2:] if gg and c.get("gate_g") == gg]
    if hit:
        add("WARN", "repeat.gate_g", "Gate G mechanism %s repeats one of the last two builds" % gg, tasks(hit),
            "vary the FINE-numbers mechanism across the batch")
    n_gg = count("gate_g", gg, window)
    if n_gg >= 5:
        add("WARN", "overuse.gate_g", "Gate G mechanism used in %d of the last %d builds" % (n_gg, len(window)))
    dt = cand.get("decision_type")
    hit = [c for c in last if dt and c.get("decision_type") == dt]
    if hit:
        add("WARN", "repeat.decision", "decision type %s repeats the last build" % dt, tasks(hit),
            "vary the answer type")
    fs = fmt_set(cand)
    hit = [c for c in recent if fs and fmt_set(c) == fs]
    if hit:
        add("WARN", "repeat.deliverables", "deliverable format set %s repeats a recent build" % "+".join(fs), tasks(hit))
    if "pdf" in fs:
        n_pdf = sum(1 for c in window if "pdf" in fmt_set(c))
        if n_pdf >= 0.75 * max(1, len(window)):
            add("WARN", "overuse.pdf", "a PDF ships in %d of the last %d builds" % (n_pdf, len(window)),
                fix="pick the file a real analyst would produce for this decision")
    om = cand.get("opening_move")
    hit = [c for c in ordered[-2:] if om and om != "other" and c.get("opening_move") == om]
    if hit:
        add("WARN", "repeat.opening", "opening move %s repeats one of the last two prompts" % om, tasks(hit),
            "see prompt-voice.md section 3")
    geo = ((cand.get("world") or {}).get("geography") or "").strip().lower()
    hit = [c for c in recent if geo and geo != "fictional" and ((c.get("world") or {}).get("geography") or "").strip().lower() == geo]
    if hit:
        add("WARN", "repeat.geography", "geography %r repeats a recent build" % geo, tasks(hit))
    tfn = Tfidf([c.get("niche") or "" for c in others] + [cand.get("niche") or ""])
    for c in others:
        s = tfn.sim(cand.get("niche") or "", c.get("niche") or "")
        if s >= NICHE_SIM:
            add("WARN", "repeat.niche", "niche reads close (similarity %.2f): %r" % (s, c.get("niche")), [label(c)])
    return findings, sims[:5]


def verdict(findings):
    lv = {f["level"] for f in findings}
    return "BLOCK" if "BLOCK" in lv else "WARN" if "WARN" in lv else "PASS"


def print_check(cand, findings, nearest):
    v = verdict(findings)
    print("%s  %s  %s/%s  shape %s  gap %s  pattern %s  gate_g %s  decision %s" % (
        v, cand.get("task"), cand.get("domain"), cand.get("objective"), cand.get("shape"),
        first(cand.get("gap")), decisive_mech(cand), cand.get("gate_g"), cand.get("decision_type")))
    for lvl in ("BLOCK", "WARN", "NOTE"):
        for f in [f for f in findings if f["level"] == lvl]:
            ag = (" against " + ", ".join(f["against"])) if f["against"] else ""
            print("  %-5s %-24s %s%s" % (lvl, f["rule"], f["msg"], ag))
            if f["fix"] and lvl != "NOTE":
                print("        fix: %s" % f["fix"])
    print("  nearest drivers:")
    for s, c, who, txt in nearest:
        print("    %.2f  %-30s %s" % (s, who, (txt or "")[:110]))
    return v


# ------------------------------------------------------------------ views

def cmd_recent(args):
    vocab = load_vocab()
    cards = load_cards()
    status = ledger_status()
    print("last %d builds in draw order (oldest first). Bans reach the last %d, overuse the last %d.\n"
          % (args.n, RECENT, WINDOW))
    for c in cards[-args.n:]:
        print("%-7s %-10s %-26s %-24s sh %-12s gap %-10s pat %-4s %-26s %-24s %-20s %s" % (
            c.get("task"), c.get("drawn") or "?", "%s/%s" % (c.get("domain"), c.get("subdomain")),
            c.get("objective"), c.get("shape"), first(c.get("gap")) or "-", decisive_mech(c) or "-",
            c.get("gate_g") or "-", c.get("calibration_form") or "-", c.get("role_family") or "-",
            status.get(c.get("task"), "")))
    return 0


def cmd_coverage(args):
    vocab = load_vocab()
    cards = [c for c in load_cards() if c.get("domain")]
    live = [c for c in cards if not str(c.get("domain")).startswith("legacy")]
    window = cards[-WINDOW:]
    print("%d cards on file, %d in the six live domains. Counts are over every card; the bracket is the last %d.\n"
          % (len(cards), len(live), WINDOW))
    objs = LIVE_OBJECTIVES
    short = {"forecasting": "FCST", "root-cause": "RCA", "anomaly-detection": "ANOM",
             "experiment-causal": "EXP", "descriptive-distribution": "DESC", "etl": "ETL",
             "opportunity-sizing-decision": "OPPS", "data-quality-monitoring": "DQM"}
    print("domain x objective (count, newest task)   '.' means never built")
    print("%-28s" % "" + "".join("%-13s" % short[o] for o in objs))
    for d in LIVE_DOMAINS:
        row = "%-28s" % d
        for o in objs:
            cs = [c for c in live if c.get("domain") == d and c.get("objective") == o]
            row += "%-13s" % (("%d t%d" % (len(cs), max(c["_num"] for c in cs))) if cs else ".")
        print(row)
    empty = [(d, o) for d in LIVE_DOMAINS for o in objs
             if not any(c.get("domain") == d and c.get("objective") == o for c in live)]
    print("\nnever-built pairings (%d): %s" % (len(empty), "; ".join("%s x %s" % e for e in empty) or "none"))

    def axis(title, field, allowed, multi=False):
        cnt, win = Counter(), Counter()
        for c in cards:
            vals = (c.get(field) or [])[:1] if multi else [c.get(field)]
            for v in vals:
                if v:
                    cnt[v] += 1
        for c in window:
            vals = (c.get(field) or [])[:1] if multi else [c.get(field)]
            for v in vals:
                if v:
                    win[v] += 1
        print("\n%s" % title)
        for k in allowed:
            if str(k).startswith("legacy"):
                continue
            print("   %-34s %3d  [%d]%s" % (k, cnt.get(k, 0), win.get(k, 0), "   never drawn" if not cnt.get(k) else ""))

    sub = Counter((c.get("domain"), c.get("subdomain")) for c in live)
    print("\nsubdomains never drawn:")
    for d in LIVE_DOMAINS:
        unused = [s for s in vocab["subdomains"][d] if s != "other" and not sub.get((d, s))]
        if unused:
            print("   %-28s %s" % (d, ", ".join(unused)))
    axis("shape (decides where the 25 criteria come from)", "shape", vocab["shapes"])
    axis("decisive gap", "gap", vocab["gaps"], multi=True)
    axis("decisive pattern", "pattern", vocab["patterns"], multi=True)
    axis("decisive generator", "generators", vocab["generators"], multi=True)
    axis("Gate G mechanism", "gate_g", vocab["gate_g"])
    axis("decision type", "decision_type", vocab["decision_types"])
    axis("calibration form", "calibration_form", vocab["calibration_forms"])
    axis("context-artifact type", "context_artifact", vocab["context_artifacts"])
    axis("stakeholder role family", "role_family", vocab["role_families"])
    axis("opening move", "opening_move", vocab["opening_moves"])
    fm = Counter("+".join(fmt_set(c)) for c in window if fmt_set(c))
    print("\ndeliverable format sets in the last %d: %s" % (WINDOW, ", ".join("%s x%d" % kv for kv in fm.most_common())))
    geo = Counter(((c.get("world") or {}).get("geography") or "?").split(",")[0].strip() for c in live)
    print("geographies (first token): %s" % ", ".join("%s x%d" % kv for kv in geo.most_common(12)))
    fo, ev, of = Counter(), Counter(), Counter()
    for c in cards:
        d = business.derived_elements(REPO, c.get("task"))
        fo.update({c["forum"]} if c.get("forum") else set(d["forums"]))
        ev.update({c["forcing_event"]} if c.get("forcing_event") else set(d["events"]))
        of[business.org_family(c) or "unclassified"] += 1
    print("\ndeciding forum (builds whose prompt names it): %s" % ", ".join(
        "%s %d" % (k, fo.get(k, 0)) for k in vocab["forums"]))
    print("forcing event: %s" % ", ".join("%s %d" % (k, ev.get(k, 0)) for k in vocab["forcing_events"]))
    print("organisation family: %s" % ", ".join("%s %d" % kv for kv in of.most_common()))
    idx = business.load_index(REPO, PEOPLE_CACHE)
    f, _, _ = business.usage(idx)
    print("most recycled first names: %s" % ", ".join(
        "%s %d" % (k, len(v)) for k, v in sorted(f.items(), key=lambda kv: -len(kv[1]))[:8]))
    return 0


def cmd_suggest(args):
    vocab = load_vocab()
    cards = [c for c in load_cards() if c.get("domain")]
    rng = random.Random(args.seed if args.seed is not None else len(cards))
    recent = cards[-RECENT:]
    window = cards[-WINDOW:]

    def weights(field, values, multi=False, boost=None):
        tot, win = Counter(), Counter()
        for c in cards:
            vs = (c.get(field) or [])[:1] if multi else [c.get(field)]
            tot.update(v for v in vs if v)
        for c in window:
            vs = (c.get(field) or [])[:1] if multi else [c.get(field)]
            win.update(v for v in vs if v)
        w = []
        for v in values:
            x = 1.0 / (1.0 + tot.get(v, 0) + 3.0 * win.get(v, 0))
            if boost:
                x *= boost(v)
            w.append(x)
        return w

    def pick(values, w):
        return rng.choices(values, weights=w, k=1)[0]

    spent_puzzles, spent_drivers = set(), set()
    for c in cards:
        for _, _, e in drivers_of(c):
            spent_puzzles.add((first(e.get("gap")), decisive_mech(e), e.get("decision_type")))
            spent_drivers.add((first(e.get("gap")), decisive_mech(e), e.get("gate_g")))
    out = []
    tries = 0
    while len(out) < args.n and tries < 5000:
        tries += 1
        d = pick(LIVE_DOMAINS, weights("domain", LIVE_DOMAINS))
        o = pick(LIVE_OBJECTIVES, weights("objective", LIVE_OBJECTIVES,
                                          boost=lambda v: 1.5 if v == "forecasting" else 1.0))
        subs = [s for s in vocab["subdomains"][d] if s != "other"]
        sub = pick(subs, [1.0 / (1.0 + sum(1 for c in cards if c.get("domain") == d and c.get("subdomain") == s)) for s in subs])
        shapes = [k for k in vocab["shapes"] if re.fullmatch(r"\d\d", k)]
        sh = pick(shapes, weights("shape", shapes, boost=lambda v: 3.0 if SHAPE_OBJECTIVE.get(v) == o else 1.0))
        gaps = list(vocab["gaps"])
        gp = pick(gaps, weights("gap", gaps, multi=True))
        pats = [p for p in vocab["patterns"] if p != "none"]
        pt = pick(pats, weights("pattern", pats, multi=True))
        gg = pick(DRAWABLE_GATE_G, weights("gate_g", DRAWABLE_GATE_G,
                                           boost=lambda v: 0.0 if v in GATE_OBJECTIVE and o not in GATE_OBJECTIVE[v]
                                           else 3.0 if v in GATE_OBJECTIVE else 1.0))
        cals = [k for k in vocab["calibration_forms"] if k not in ("none", "other")]
        cf = pick(cals, weights("calibration_form", cals))
        arts = [k for k in vocab["context_artifacts"] if k not in ("none", "other")]
        ca = pick(arts, weights("context_artifact", arts))
        roles = [k for k in vocab["role_families"] if k != "other"]
        rf = pick(roles, weights("role_family", roles))
        dts = sorted(SHAPE_DECISIONS.get(sh) or vocab["decision_types"])
        dt = pick(dts, weights("decision_type", dts))
        draw = {"domain": d, "subdomain": sub, "objective": o, "shape": sh, "gap": gp, "pattern": pt,
                "gate_g": gg, "calibration_form": cf, "context_artifact": ca, "role_family": rf,
                "decision_type": dt}
        bad = False
        for c in recent:
            if (c.get("domain"), c.get("objective")) == (d, o) or decisive_mech(c) == pt \
                    or c.get("calibration_form") == cf or c.get("role_family") == rf \
                    or c.get("context_artifact") == ca or (c.get("domain"), c.get("subdomain")) == (d, sub):
                bad = True
        if any(c.get("shape") == sh for c in cards[-2:]):
            bad = True
        # A suggestion never lands on a spent structural signature, anywhere in the corpus or its
        # lineage, so it never draws a BLOCK from test.same_puzzle or test.same_driver.
        if (gp, pt, dt) in spent_puzzles or (gp, pt, gg) in spent_drivers:
            bad = True
        if bad or draw in out:
            continue
        out.append(draw)

    pair_count = Counter((c.get("domain"), c.get("objective")) for c in cards)
    print("Independent draws, each dimension weighted toward what has been used least, and none of them")
    print("breaking a standing ban against the last %d builds. They are starting points for the DRAW block,"
          % RECENT)
    print("not a decision: the driver, the world and the stump sentence are still yours to design.\n")
    for i, d in enumerate(out, 1):
        print("draw %d" % i)
        print("   domain      %s / %s   (pairing with %s built %d times)" % (
            d["domain"], d["subdomain"], d["objective"], pair_count.get((d["domain"], d["objective"]), 0)))
        print("   objective   %s" % d["objective"])
        print("   shape       %s %s" % (d["shape"], vocab["shapes"][d["shape"]]))
        print("   gap         %s      pattern %s (%s)" % (d["gap"], d["pattern"], vocab["patterns"][d["pattern"]]))
        print("   gate_g      %s" % d["gate_g"])
        print("   decision    %s      calibration %s" % (d["decision_type"], d["calibration_form"]))
        print("   role        %s      context artifact %s\n" % (d["role_family"], d["context_artifact"]))
    if len(out) < args.n:
        print("only %d draws satisfied the bans after %d tries" % (len(out), tries))
    return 0


TEMPLATE_KEYS = ["task", "architecture", "drawn", "slot_note", "domain", "subdomain", "niche", "objective",
                 "forum", "forcing_event", "org_family",
                 "shape", "decision_type", "answer_unit", "answer", "answer_source", "gap", "pattern",
                 "generators", "gate_g", "calibration_form", "context_artifact", "stakeholder_role",
                 "role_family", "scoring_unit", "spine", "world", "deliverables", "opening_move", "driver",
                 "driver_concrete", "stump", "mechanism_source", "differentiation", "lineage", "notes"]


def cmd_new(args):
    t = args.task if args.task.startswith("task") else "task" + args.task
    card = {
        "task": t, "architecture": "v1", "drawn": date.today().isoformat(), "slot_note": "",
        "domain": "<vocab domains key>", "subdomain": "<vocab subdomains[domain] item>",
        "niche": "<the unusual sub-function inside the subdomain, in this build's nouns>",
        "objective": "<vocab objectives key>", "shape": "<vocab shapes key>",
        "decision_type": "<vocab decision_types key>", "answer_unit": "<vocab answer_units item>",
        "answer": "", "answer_source": "",
        "gap": ["<decisive gap first>"], "pattern": ["<decisive pattern first, or none>"],
        "generators": ["<decisive G-code first>"], "gate_g": "<vocab gate_g key>",
        "calibration_form": "<vocab calibration_forms key>", "context_artifact": "<vocab context_artifacts key>",
        "stakeholder_role": "<as the prompt will state it>", "role_family": "<vocab role_families key>",
        "scoring_unit": "<vocab scoring_units item>",
        "spine": {"file": "", "rows": 0, "entity": "<one row is one ...>", "grain": "<e.g. member x month>",
                  "source": "synthetic"},
        "forum": "<vocab forums key>", "forcing_event": "<vocab forcing_events key>",
        "org_family": "<vocab org_families key>",
        "world": {"geography": "<country, state or region>", "currency": "<ISO>", "org_type": "<short>",
                  "invented_names": [], "people": ["<drawn with guard.py names, never typed from memory>"]},
        "deliverables": ["<file names the prompt will ask for>"], "opening_move": "<vocab opening_moves item>",
        "driver": "<ONE sentence, the decisive move with every domain noun stripped>",
        "driver_concrete": "<ONE sentence, the decisive move in this build's own terms>",
        "stump": "<ONE sentence, the wrong committed answer a competent solver files and the step that lands them there>",
        "mechanism_source": "design_note", "differentiation": {}, "lineage": [], "notes": "",
    }
    print(json.dumps(card, indent=2, ensure_ascii=False))
    return 0


def cmd_check(args):
    vocab = load_vocab()
    cards = load_cards()
    cand = load_candidate(args.card, cards)
    findings, nearest = check(cand, cards, vocab, ledger_status())
    v = print_check(cand, findings, nearest)
    return 1 if v == "BLOCK" else 0


def cmd_register(args):
    vocab = load_vocab()
    cards = load_cards()
    cand = load_candidate(args.card, cards)
    findings, nearest = check(cand, cards, vocab, ledger_status())
    v = print_check(cand, findings, nearest)
    if v == "BLOCK" and not args.force:
        print("\nnot filed: clear every BLOCK first (or --force with the reason written in the card's notes)")
        return 1
    if v == "BLOCK" and args.force and not (cand.get("notes") or "").strip():
        print("\nnot filed: --force needs the reason in the card's notes")
        return 1
    out = CARDS_DIR / ("%s.json" % cand["task"])
    clean = {k: v for k, v in cand.items() if not k.startswith("_")}
    out.write_text(json.dumps(clean, indent=2, ensure_ascii=False) + "\n")
    print("\nfiled %s" % out)
    return 0


def cmd_validate(args):
    vocab = load_vocab()
    cards = load_cards()
    if args.tasks:
        cards = [c for c in cards if c.get("task") in args.tasks]
    bad = 0
    for c in cards:
        errs, warns = validate_card(c, vocab)
        if errs:
            bad += 1
            print("%s: %s" % (c.get("task"), "; ".join(errs)))
        elif warns and args.verbose:
            print("%s: note: %s" % (c.get("task"), "; ".join(warns)))
    seen = Counter(c.get("task") for c in cards)
    for t, n in seen.items():
        if n > 1:
            bad += 1
            print("%s: %d cards claim this task" % (t, n))
    print("%d cards, %d invalid" % (len(cards), bad))
    return 1 if bad else 0


def cmd_show(args):
    cards = load_cards()
    c = load_candidate(args.task, cards)
    clean = {k: v for k, v in c.items() if not k.startswith("_")}
    print(json.dumps(clean, indent=2, ensure_ascii=False))
    return 0


def cmd_nearest(args):
    load_vocab()
    cards = load_cards()
    cand = load_candidate(args.card, cards)
    corpus = []
    for c in cards:
        if c.get("task") == cand.get("task"):
            continue
        corpus.extend((c, who, txt) for who, txt, _ in drivers_of(c))
    tf = Tfidf([t for _, _, t in corpus] + [cand.get("driver") or ""])
    sims = sorted(((tf.sim(cand.get("driver") or "", txt), who, txt) for c, who, txt in corpus), key=lambda x: -x[0])
    print("driver: %s\n" % cand.get("driver"))
    for s, who, txt in sims[:args.n]:
        print("%.2f  %-30s %s" % (s, who, txt[:140]))
    return 0


def cmd_heart(args):
    """The /approve check: the heart of the stump against every build on file. Reads the card's
    driver, driver_concrete and stump sentences and compares them against every card's driver, every
    lineage driver, every card's stump and every shipped-ledger row, then runs the structural bans
    (check) on the card. Spawns nothing. Exit 1 on BLOCK, so /approve can stop on it."""
    vocab = load_vocab()
    cards = load_cards()
    cand = load_candidate(args.task, cards)
    others = [c for c in cards if c.get("task") != cand.get("task")]
    heart = " ".join(x for x in (cand.get("driver"), cand.get("driver_concrete"), cand.get("stump")) if x)
    if not heart.strip():
        print("BLOCK  the card for %s carries no driver and no stump sentence; fill them before /approve" % cand.get("task"))
        return 1
    corpus = []
    for c in others:
        for who, txt, _ in drivers_of(c):
            corpus.append(("card driver", who, txt))
        if c.get("stump"):
            corpus.append(("card stump", label(c), c["stump"]))
    try:
        spec = importlib.util.spec_from_file_location("clone_fp", str(CLONE_FP))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for task, rows in mod.parse_ledger(str(LEDGER)).items():
            if task == cand.get("task"):
                continue
            for r in rows:
                cl = r.get("_clean", {})
                txt = " ".join(cl.get(k, "") for k in ("gap", "pattern", "mechanism", "calibration", "artifact", "decision_type"))
                if len(txt) > 40:
                    corpus.append(("ledger row", "%s %s" % (task, (cl.get("variant") or "")[:30]), txt))
    except Exception as e:
        print("note: ledger not read (%s)" % e)
    tf = Tfidf([t for _, _, t in corpus] + [heart])
    scored = sorted(((tf.sim(heart, t), kind, who, t) for kind, who, t in corpus), key=lambda x: -x[0])
    print("== HEART OF THE STUMP, %s ==" % cand.get("task"))
    print("driver: %s" % (cand.get("driver") or "")[:300])
    print("stump:  %s\n" % (cand.get("stump") or "")[:300])
    print("nearest on file (driver + stump text against every card, lineage and ledger row):")
    worst = 0.0
    for s, kind, who, t in scored[:args.n]:
        worst = max(worst, s)
        flag = "BLOCK" if s >= BLOCK_SIM else ("WARN " if s >= WARN_SIM else "     ")
        print("  %s %.2f  %-12s %-34s %s" % (flag, s, kind, who[:34], re.sub(r"\s+", " ", t)[:110]))
    print()
    findings, nearest = check(cand, cards, vocab, status=ledger_status())
    print_check(cand, findings, nearest)
    v = verdict(findings)
    if worst >= BLOCK_SIM and not any(f["rule"] == "driver.text" for f in findings):
        print("BLOCK  heart text similarity %.2f at or above %.2f" % (worst, BLOCK_SIM))
        v = "BLOCK"
    print("\nHEART VERDICT: %s" % v)
    return 1 if v == "BLOCK" else 0


def cmd_surface(args):
    """After the pack is cut: clone-check's mechanical screen, focused on this build. It profiles
    files, schemas, row counts, numeric signatures and masked prompt wording, and spawns nothing.
    The adjudicated /clone-check stays author-triggered."""
    t = args.task if args.task.startswith("task") else "task" + args.task
    r = subprocess.run([sys.executable, str(CLONE_FP), "extract"], cwd=str(REPO))
    if r.returncode:
        return r.returncode
    rc = subprocess.run([sys.executable, str(CLONE_FP), "screen", "--focus", t], cwd=str(REPO)).returncode
    print("\n== PEOPLE IN THE CUT PACK (generators introduce names the card never planned) ==")
    return max(rc, people_report(t))


def people_report(t):
    load_vocab()
    cards = load_cards()
    idx = business.load_index(REPO, PEOPLE_CACHE, refresh=True)
    found = ["%s %s" % fl for fl in business.people_in_build(REPO / t)]
    ordered = [c.get("task") for c in sorted(cards, key=draw_key) if c.get("task") != t][-WINDOW:]
    issues = business.check_people(found, idx, ordered, t)
    print("personas found in %s: %s" % (t, ", ".join(found) or "none"))
    for lvl, rule, msg, against in issues:
        print("  %-5s %-14s %s%s" % (lvl, rule, msg, (" against " + ", ".join(against)) if against else ""))
    planned = set(((next((c for c in cards if c.get("task") == t), {}) or {}).get("world") or {}).get("people") or [])
    unplanned = [n for n in found if n not in planned]
    if unplanned:
        print("  NOTE  not on the card: %s (add them to world.people)" % ", ".join(unplanned))
    return 1 if any(i[0] == "BLOCK" for i in issues) else 0


def cmd_people(args):
    """The corpus name index, or one build's personas checked against it."""
    if args.task:
        return people_report(args.task if args.task.startswith("task") else "task" + args.task)
    idx = business.load_index(REPO, PEOPLE_CACHE, refresh=args.refresh)
    f, l, full = business.usage(idx)
    top = lambda d, n: ", ".join("%s %d" % (k, len(v)) for k, v in sorted(d.items(), key=lambda kv: -len(kv[1]))[:n])
    print("%d personas across %d builds that name anyone\n" % (len(full), sum(1 for v in idx["builds"].values() if v)))
    print("first names by builds: %s\n" % top(f, 30))
    print("surnames by builds: %s\n" % top(l, 20))
    print("full names by builds: %s" % top(full, 12))
    return 0


def cmd_names(args):
    """Draw personas from the locale's own name pool, skipping every name the check would block."""
    load_vocab()
    cards = sorted(load_cards(), key=draw_key)
    idx = business.load_index(REPO, PEOPLE_CACHE)
    loc = args.locale or business.locale_for(args.geo)
    recent = [c.get("task") for c in cards][-WINDOW:]
    names = business.suggest_people(idx, recent, loc, args.n, args.seed)
    print("locale %s, seed %d. Paste the ones you use into world.people.\n" % (loc, args.seed))
    for nm in names:
        print("  " + nm)
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("recent"); s.add_argument("--n", type=int, default=WINDOW); s.set_defaults(fn=cmd_recent)
    s = sub.add_parser("coverage"); s.set_defaults(fn=cmd_coverage)
    s = sub.add_parser("suggest"); s.add_argument("--n", type=int, default=3); s.add_argument("--seed", type=int)
    s.set_defaults(fn=cmd_suggest)
    s = sub.add_parser("new"); s.add_argument("task"); s.set_defaults(fn=cmd_new)
    s = sub.add_parser("check"); s.add_argument("card"); s.set_defaults(fn=cmd_check)
    s = sub.add_parser("register"); s.add_argument("card"); s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_register)
    s = sub.add_parser("validate"); s.add_argument("tasks", nargs="*"); s.add_argument("--verbose", action="store_true")
    s.set_defaults(fn=cmd_validate)
    s = sub.add_parser("show"); s.add_argument("task"); s.set_defaults(fn=cmd_show)
    s = sub.add_parser("nearest"); s.add_argument("card"); s.add_argument("--n", type=int, default=8)
    s.set_defaults(fn=cmd_nearest)
    s = sub.add_parser("surface"); s.add_argument("task"); s.set_defaults(fn=cmd_surface)
    s = sub.add_parser("heart"); s.add_argument("task"); s.add_argument("--n", type=int, default=10)
    s.set_defaults(fn=cmd_heart)
    s = sub.add_parser("people"); s.add_argument("task", nargs="?"); s.add_argument("--refresh", action="store_true")
    s.set_defaults(fn=cmd_people)
    s = sub.add_parser("names"); s.add_argument("--geo", default=""); s.add_argument("--locale", default="")
    s.add_argument("--n", type=int, default=10); s.add_argument("--seed", type=int, required=True)
    s.set_defaults(fn=cmd_names)
    a = ap.parse_args()
    sys.exit(a.fn(a))


if __name__ == "__main__":
    main()
