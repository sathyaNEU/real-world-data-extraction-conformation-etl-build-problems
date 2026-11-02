"""task237 ask layer against the careful solver's routes, on the cut pack.

    python3 task237/generator/ceiling.py [pack]

pack is target.zip (the default, the archive that ships) or a folder holding the pack's files. The script reads the
pack only (plain csv and workbook reading, the documents through the verifier's own reader), modifies nothing and never
runs inside the build.

The asks are the release table's two figures per version: Ask A, each version's valid pilot completes (TAS-4 s.4), and
Ask B, each version's pilot mean score to two decimals (s.5): 20 figures, a figure kept only when it is exact. Every
route below is a complete pipeline over the vendors' files, the register and the documents.

The cracker is the careful solver, never a narrowed one: it lands the call (the trait's share of each version's score
variance from a model with the negatively worded items' wording factor, on its own full answerers), runs the hygiene
battery (exact duplicates, the export against the ledger both ways, the ledger's merged rows followed to the account
they name, the panel's UTC clock against the register's Eastern dates and the hour profile, the long file one row per
interview and variable, the back-check log against the interviews on every field it carries, the vendors' status and
RESULT labels checked against the items each record reached, the codes off the five-point scale against the vendors'
own labels) and executes every filed rule as worded: s.4's age, window, the end of the module reached in the version,
a panel member once at the first valid complete, an interview the back-check reports not confirmed out and the rest
kept; s.5's reversals, non-answers and prorating. The mirror stops at the default path (Cronbach's alpha: six versions
wrong) and is scored twice, on the careful ask route (the asks do not depend on the call) and on the natural read
without the battery (the vendors' status, the back-check joined on its case, the ledger's accounts as they stand, the
dates read off the UTC stamp). The full includer is the golden handling and has to give back figures.json exactly,
or the script exits 1. The stops are the design note's other wrong paths, each scored as a route.

The pair is the ask sheet's formula: 38 recommendation and components, 7 instruction following, 55 asks over 25 ask
criteria (the 20 figures and the chart's 5 parts: every version plotted, the bands drawn, each version's decision, each
version's deciding estimate, the file as named), a response off the call keeping r = 10 (its four right decisions).
The cracker keeps the chart's 5 parts (they follow the call); the mirror keeps 3 (the frame, the bands, the file)."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile
from decimal import Decimal, ROUND_HALF_UP

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import verify as V   # noqa: E402  (the bundle-only readers, the verifier's own model fit)

TASK = os.path.dirname(HERE)
CODES = V.CODES
FILES = {
    "online": "ncp_bcs12_pilot_export_wave6.csv", "ledger": "ncp_incentive_ledger_bcs12_pilot.csv",
    "ncp_labels": "ncp_bcs12_pilot_value_labels.csv", "capi": "flr_bcs12_pilot_interviews_long.csv",
    "bc": "flr_backcheck_log_bcs12_pilot.csv", "flr_labels": "flr_bcs12_pilot_value_labels.csv",
    "reg": "bcs12_translation_register_wave6.xlsx", "std": "translation_adaptation_standard_TAS-4.pdf",
    "manual": "bcs12_technical_manual_english.pdf",
}
REC, INS, ASK, OFF = 38.0, 7.0, 55.0, 10.0
CHART_CRACKER, CHART_MIRROR, CHART = 5, 3, 5
EASTERN = dt.timedelta(hours=-5)

# a route: how each clause and each field is read (the golden handling first)
GOLDEN = dict(module="items", bc_join="case and interviewer", merges=True, clock="eastern", window=True, retakes=False,
              switchers=False, inside=False, pretest=False, unconfirmed=False, unreached_kept=True, prorate=True,
              codes_missing=True)
CRACKER = dict(GOLDEN)          # the careful solver's route: every filed rule as worded, every field by its plain meaning
NATURAL = dict(GOLDEN, module="status", bc_join="case", merges=False, clock="utc")
STOPS = {
    "the narrowed cracker the sheet recorded (the vendors' status; the back-check on its case)":
        dict(module="status", bc_join="case"),
    "the vendors' status for the module's end": dict(module="status"),
    "the back-check joined on its case alone": dict(bc_join="case"),
    "the ledger's accounts as they stand (merges not followed)": dict(merges=False),
    "the online window read off the UTC stamp": dict(clock="utc"),
    "no window for the online pilots": dict(window=False),
    "panel retakes counted": dict(retakes=True),
    "switchers to English counted": dict(switchers=True),
    "partials inside the module counted": dict(inside=True),
    "pretest interviews counted": dict(pretest=True),
    "unconfirmed interviews counted": dict(unconfirmed=True),
    "unreached back-checks dropped": dict(unreached_kept=False),
    "no prorating (B)": dict(prorate=False),
    "codes 9, -8 and -9 read as answers (B)": dict(codes_missing=False),
}


def pack_dir(arg):
    """The pack as a folder: target.zip unpacked into a scratch folder (removed after), or the folder given."""
    src = arg or os.path.join(TASK, "target.zip")
    if os.path.isdir(src):
        files = sorted(os.listdir(src))
        h = hashlib.sha256("".join(hashlib.sha256(open(os.path.join(src, f), "rb").read()).hexdigest()
                                   for f in files).encode()).hexdigest()
        return src, None, "folder %s (%d files, sha256 of the file digests %s)" % (src, len(files), h[:16])
    tmp = tempfile.mkdtemp(prefix="ceiling237-")
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    inner = os.path.join(tmp, "target")
    folder = inner if os.path.isdir(inner) else tmp
    md5 = hashlib.md5(open(src, "rb").read()).hexdigest()
    return folder, tmp, "%s (%d files, md5 %s)" % (src, len(os.listdir(folder)), md5)


def load(folder):
    P = {k: V.rows(os.path.join(folder, f)) for k, f in FILES.items() if f.endswith(".csv")}
    P["reg"] = V.register(os.path.join(folder, FILES["reg"]))
    return P


def eastern_date(utc, clock):
    t = dt.datetime.strptime(utc, "%Y-%m-%dT%H:%M:%SZ")
    return ((t + EASTERN) if clock == "eastern" else t).date().isoformat()


def in_window(reg, v, day):
    return str(reg[v]["pilot_start"])[:10] <= day <= str(reg[v]["pilot_end"])[:10]


def online(P, how):
    reg = P["reg"]
    member = {r["respondent_id"]: r["panel_member_id"] for r in P["ledger"] if r["respondent_id"]}
    merged = {r["panel_member_id"]: r["merged_into"] for r in P["ledger"] if r["outcome"] == "merged"}

    def root(a):
        seen = set()
        while how["merges"] and a in merged and a not in seen:
            seen.add(a)
            a = merged[a]
        return a
    code = {k.upper(): k for k in reg}
    best, extra = {}, []
    for r in P["online"]:
        v = code[r["survey_code"].split("CCS6-BCS-")[1]]
        if r["status"] == "screened out" or int(r["age"]) < 18:
            continue
        reached = all(r[c] != "" for c in CODES)
        if how["module"] == "status":
            if r["status"] != "complete":
                continue
        elif not (reached or how["inside"]):
            continue
        if not how["switchers"] and r["ui_language_at_end"] != v:
            continue
        if how["window"] and not in_window(reg, v, eastern_date(r["start_utc"], how["clock"])):
            continue
        ans = [r[c] for c in CODES]
        if how["retakes"]:
            extra.append((v, ans))
            continue
        key, t = (v, root(member[r["respondent_id"]])), r["end_utc"] or r["start_utc"]
        if key not in best or t < best[key][0]:
            best[key] = (t, ans)
    return [(v, a) for (v, _), (_, a) in best.items()] + extra


def capi(P, how):
    reg = P["reg"]
    by_pair = {(r["case_id"], r["interviewer_id"]): r["outcome"] for r in P["bc"]}
    by_case = {}
    for r in P["bc"]:                     # the log's own order: its earliest check of the case
        by_case.setdefault(r["case_id"], r["outcome"])
    iv = {}
    for r in P["capi"]:
        iv.setdefault((r["case_id"], r["version"], r["interviewer_id"], r["interview_date"]), {})[r["variable"]] = r["value"]
    out = []
    for (case, v, who, day), d in iv.items():
        if int(d["AGE"]) < 18:
            continue
        if how["module"] == "status":
            if d["RESULT"] != "1":
                continue
        elif not (all(c in d for c in CODES) or how["inside"]):
            continue
        if not how["pretest"] and not in_window(reg, v, day):
            continue
        outcome = by_case.get(case, "") if how["bc_join"] == "case" else by_pair.get((case, who), "")
        if outcome == "not confirmed" and not how["unconfirmed"]:
            continue
        if outcome == "not reached" and not how["unreached_kept"]:
            continue
        out.append((v, [d.get(c, "") for c in CODES]))
    return out


def item_scores(ans, how):
    out = []
    for i, a in enumerate(ans):
        if a == "" or (how["codes_missing"] and int(a) in V.MISSING):
            out.append(None)
        else:
            out.append(6 - int(a) if i in V.NEG else int(a))
    return out


def total(items, how):
    got = [x for x in items if x is not None]
    if len(got) == 12 or (how["prorate"] and len(got) >= 10):
        return sum(got) / len(got) * 12
    return None


def half_up(x):
    return Decimal(repr(float(x))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def route(P, how):
    comp = online(P, how) + capi(P, how)
    out = {}
    for v in P["reg"]:
        sc = [item_scores(a, how) for x, a in comp if x == v]
        tot = [t for t in (total(s, how) for s in sc) if t is not None]
        full = np.array([s for s in sc if None not in s], dtype=float)
        out[v] = dict(A=len(sc), B="%.2f" % half_up(np.mean(tot)), full=full)
    return out


def calls(r, estimator):
    out = {}
    for v, x in r.items():
        S = np.cov(x["full"], rowvar=False)
        out[v] = V.band(V.bifactor_share(S) if estimator == "trait share" else V.alpha(S))
    return out


def kept(r, gold):
    a = sum(r[v]["A"] == gold[v]["valid_pilot_completes"] for v in gold)
    b = sum(r[v]["B"] == gold[v]["pilot_mean_score"] for v in gold)
    return a, b


def pair(kc, km, n):
    c = REC + INS + ASK * (kc + CHART_CRACKER) / (n + CHART)
    s = OFF + INS + ASK * (km + CHART_MIRROR) / (n + CHART)
    return c, s, (c + s) / 2.0


def battery(folder, P):
    """the hygiene battery a careful analyst runs before counting: (check, finding)"""
    out = []
    for k in ("online", "ledger", "capi", "bc"):
        rows = [tuple(r.values()) for r in P[k]]
        out.append(("exact duplicate rows, %s" % FILES[k], "%d of %d" % (len(rows) - len(set(rows)), len(rows))))
    ids = [r["respondent_id"] for r in P["online"]]
    led = {r["respondent_id"] for r in P["ledger"] if r["respondent_id"]}
    out.append(("export against ledger, both ways", "%d entries without a ledger row, %d ledger rows without an entry, "
                "%d entry ids repeated" % (len(set(ids) - led), len(led - set(ids)), len(ids) - len(set(ids)))))
    mg = [r for r in P["ledger"] if r["outcome"] == "merged"]
    accounts = {r["panel_member_id"] for r in P["ledger"] if r["respondent_id"]}
    out.append(("ledger merges followed to the account they name", "%d merged rows, every merged_into an account with "
                "entries: %s" % (len(mg), all(r["merged_into"] in accounts for r in mg))))
    hours = [(dt.datetime.strptime(r["start_utc"], "%Y-%m-%dT%H:%M:%SZ") + EASTERN).hour for r in P["online"]]
    out.append(("the panel's clock: hour profile of entry starts read in Eastern time", "%d to %d h, UTC stamps "
                "converted for the register's Eastern dates" % (min(hours), max(hours))))
    keys = [(r["case_id"], r["interviewer_id"], r["interview_date"], r["variable"]) for r in P["capi"]]
    out.append(("long file one row per interview and variable", "%d repeats" % (len(keys) - len(set(keys)))))
    iv = {(r["case_id"], r["interviewer_id"]) for r in P["capi"]}
    cases = {}
    for c, w in iv:
        cases.setdefault(c, set()).add(w)
    bc = [(r["case_id"], r["interviewer_id"]) for r in P["bc"]]
    out.append(("back-check log against the interviews on case and interviewer", "%d of %d log rows match one interview; "
                "%d cases hold two interviewers' interviews" % (sum(b in iv for b in bc), len(bc),
                                                                sum(len(w) > 1 for w in cases.values()))))
    past_on = sum(r["status"] == "partial" and all(r[c] != "" for c in CODES) for r in P["online"])
    w = {}
    for r in P["capi"]:
        w.setdefault((r["case_id"], r["interviewer_id"], r["interview_date"]), {})[r["variable"]] = r["value"]
    past_fl = sum(d["RESULT"] == "2" and all(c in d for c in CODES) for d in w.values())
    out.append(("the vendors' status and RESULT checked against the items reached", "%d online partials and %d RESULT 2 "
                "interviews reached BCS12, the end of the module" % (past_on, past_fl)))
    F = V.filed(folder, dict(FILES, std=FILES["std"], manual=FILES["manual"]))
    out.append(("codes off the five-point scale against the vendors' labels", "non-answers %s, items reversed %s" % (
        sorted(F["missing"]), [i + 1 for i in F["neg"]])))
    return out, F


def main(arg=None):
    folder, scratch, stamp = pack_dir(arg)
    try:
        return run(folder, stamp)
    finally:
        if scratch:
            shutil.rmtree(scratch)


def run(folder, stamp):
    print("pack: " + stamp)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    gold = {r["version"]: r for r in figs["deliverables"]["bcs12_wave6_release_decisions.csv"]}
    n = 2 * len(gold)
    P = load(folder)
    bat, F = battery(folder, P)
    V.NEG, V.MISSING = F["neg"], F["missing"]
    print("\nthe cracker's hygiene battery:")
    for check, finding in bat:
        print("  %-78s %s" % (check, finding))

    full = route(P, GOLDEN)
    kf = kept(full, gold)
    if sum(kf) != n:
        print("CONTROL FAILED: the full includer keeps %d of %d, the route code does not reproduce figures.json" % (sum(kf), n))
        return 1
    crk = route(P, CRACKER)
    c_call = calls(crk, "trait share")
    m_call = calls(crk, "alpha")
    gcall = {r["version"]: r["decision"] for r in gold.values()}
    on_call = c_call == gcall
    off = [v for v in gcall if m_call[v] != gcall[v]]
    print("\ncracker's call (the trait's share with the wording factor separated): %s" % (
        "lands all ten decisions" if on_call else "MISSES %s" % [v for v in gcall if c_call[v] != gcall[v]]))
    print("mirror's call (Cronbach's alpha, the default path): %d of 10 decisions wrong (%s)" % (len(off), ", ".join(off)))
    if not on_call or len(off) < 4:
        print("the rows below assume the cracker on the call and the mirror off it: they are not")
        return 1

    nat = route(P, NATURAL)
    kc, km, kn = kept(crk, gold), kept(crk, gold), kept(nat, gold)
    print("\nAsk A valid pilot completes and Ask B pilot mean score, by version (figures.json in brackets):")
    for v in gold:
        print("  %-8s cracker A %4d (%4d) B %s (%s) | natural read without the battery A %4d B %s" % (
            v, crk[v]["A"], gold[v]["valid_pilot_completes"], crk[v]["B"], gold[v]["pilot_mean_score"], nat[v]["A"], nat[v]["B"]))
    print("\nper route, ask figures kept of %d (Ask A, Ask B):" % n)
    print("  %-90s %2d (%d, %d)" % ("cracker: the careful solver, every filed rule, the battery, every field's plain meaning",
                                    sum(kc), kc[0], kc[1]))
    print("  %-90s %2d (%d, %d)" % ("mirror on the careful ask route (the asks do not depend on the call)", sum(km), km[0], km[1]))
    print("  %-90s %2d (%d, %d)" % ("mirror on the natural read without the battery", sum(kn), kn[0], kn[1]))
    for name, ch in STOPS.items():
        k = kept(route(P, dict(GOLDEN, **ch)), gold)
        print("  %-90s %2d (%d, %d)" % ("stop: " + name, sum(k), k[0], k[1]))
    print("  %-90s %2d (control, figures.json reproduced)" % ("full includer", sum(kf)))

    c, s, p = pair(sum(kc), sum(km), n)
    c2, s2, p2 = pair(sum(kc), sum(kn), n)
    print("\nthe sheet's formula (38, 7, 55 over %d ask criteria; r = 10): cracker %.1f, mirror %.1f, pair %.1f" % (
        n + CHART, c, s, p))
    print("  with the mirror on the natural read without the battery: mirror %.1f, pair %.1f" % (s2, p2))
    print("  two careful responses on the call: %.1f" % c)
    worst = max(p, p2)
    whole = [a for a, k in (("A", km[0]), ("B", km[1])) if k == len(gold)]
    print("\nCracker keeps: %d of %d ask figures" % (sum(kc), n))
    print("Mirror leakage: %.1f per cent of ask weight (asks kept whole by the mirror: %s)" % (
        100.0 * (sum(km) + CHART_MIRROR) / (n + CHART), ", ".join(whole) or "none"))
    print("Pair ceiling: %.1f (the worst of the two mirror rows)" % worst)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
