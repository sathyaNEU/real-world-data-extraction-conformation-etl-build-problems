"""Assertions on the build: the input gates, the golden reproduced from the cut pack and from the generator's clean
truth (R1 the raw material ships, R2 each Layer 1 item neutral, R3a the analyst test, R3b the decisive step alone),
the ladder, every shortcut a reader might take, the callback model's family on the four and the five graded percents,
the semantic forks (SFn), the two ask devices on the careful path and the mirror's, the separation of the asks from
the call, the documents, the containers and the realism sweep."""
import datetime as dt
import json
import os
import re
import shutil
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as AN     # noqa: E402
import asks as AK         # noqa: E402
import common as K        # noqa: E402
import cracker as CR      # noqa: E402
import models as M        # noqa: E402
import pack as P          # noqa: E402
import routes as RT       # noqa: E402
import world as W         # noqa: E402

FAILS = []
COUNT = [0]
GOLD_NAMES = ("Pierce", "Spokane", "King", "Thurston-Mason")
BELOW = "Greater Columbia"
NAIVE_NAMES = ("Pierce", "North Sound", "King", "Spokane")


def check(label, ok, detail=""):
    COUNT[0] += 1
    if not ok:
        FAILS.append(label)
    print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [%s]" % (detail,)) if detail != "" else ""))


def pct(x):
    return int(np.floor(100 * float(x) + 0.5))


def four(v):
    return RT.four(v)


def names(ix):
    return tuple(sorted(K.NAME[K.CODES[i]] for i in ix))


def edge(x):
    """Distance of a share (in points) from the nearest half-point rounding boundary."""
    v = 100 * float(x)
    return abs(v - np.floor(v) - 0.5)


def run(task, b, fig, res):
    target = os.path.join(task, "target")
    w, A, H = b["w"], b["A"], b["H"]
    c = res["c"]
    GOLD = four(c["share"])
    graded = list(c["order"][:4])
    # ---------------------------------------------------------------- input gates
    files = sorted(os.listdir(target))
    check("GATE ten or more files", len(files) >= 10, len(files))
    exts = {f.rsplit(".", 1)[1] for f in files}
    check("GATE three or more formats", len(exts) >= 3, sorted(exts))
    big = max(b["counts"].values())
    check("GATE a file of 25,000 rows or more", big >= 25000, big)
    meta = json.load(open(os.path.join(task, "metadata.json")))
    check("GATE two distractors named in metadata.json", len(meta["distractors"]) >= 2 and
          all(d in files for d in meta["distractors"]), meta["distractors"])
    check("GATE every file has provenance", set(meta["provenance"]) == set(files), len(meta["provenance"]))
    contents = open(os.path.join(target, K.FILES["contents"])).read()
    check("GATE contents lists every other file", all(f in contents for f in files if f != K.FILES["contents"]))
    check("GATE no file named after the stump",
          not any(re.search(r"callback|attempt|nonresp|window|contact|propens|weight|evening", f) for f in files))
    check("GATE the shipped file set is the generator's", set(files) == set(K.FILES.values()), sorted(files))
    # ---------------------------------------------------------------- the golden from the pack and from the truth
    th = W.histories(w)
    order = {cno: i for i, cno in enumerate(w["det"]["case_no"])}
    cids = sorted(c["S"])
    hp = {order[x]: h for x, h in zip(cids, c["hist"])}
    mism = [i for i in range(len(th)) if tuple(th[i][:5]) != tuple(hp[i][:5]) or
            [cc for cc, _ in th[i][5]] != [cc for cc, _ in hp[i][5]]]
    check("GOLDEN the pack's call histories equal the clean truth's for every sampled member", not mism, len(mism))
    tS = M.summarise(th)
    tshare = M.em(tS)[0]
    tsh = np.zeros(10)
    for r in range(10):
        tsh[r] = tshare[r]
    check("GOLDEN the pack's shares equal the clean truth's model in every region",
          float(np.abs(np.sort(tsh) - np.sort(c["share"])).max()) < 1e-9 and four(tshare) == GOLD,
          float(np.abs(np.sort(tsh) - np.sort(c["share"])).max()))
    check("GOLDEN the four are Pierce, Spokane, King and Thurston-Mason", names(GOLD) == tuple(sorted(GOLD_NAMES)),
          fig["call"]["regions"])
    check("GOLDEN the first region below is Greater Columbia", fig["call"]["first_below"] == BELOW,
          fig["call"]["first_below"])
    srt = np.sort(c["share"])
    check("LADDER golden: the fifth region sits 1.2 points or more above the fourth", srt[4] - srt[3] >= 0.012,
          round(100 * (srt[4] - srt[3]), 2))
    for i in graded:
        check("LADDER golden: %s's share sits 0.15 point or more inside its whole-percent bin" % K.NAME[K.CODES[i]],
              edge(c["share"][i]) >= 0.15, round(100 * c["share"][i], 3))
    # ---------------------------------------------------------------- R1 the raw material ships
    calls_per = [len(c["S"][x]["calls"]) for x in cids]
    check("R1 every sampled member's calls ship with their times, centre and outcome (every case called)",
          min(calls_per) >= 1, min(calls_per))
    check("R1 the decisive computation reads all 15,000 sampled members' histories, reached or not",
          len(c["hist"]) == 15000 and int((c["SS"]["out"] == 0).sum()) > 2000, int((c["SS"]["out"] == 0).sum()))
    for f in files:
        if f.endswith(".csv") or f.endswith(".txt"):
            head = open(os.path.join(target, f)).readline().strip().lower()
            for wd in ("window", "class", "weight", "propensity", "contact_rate", "posterior", "imputed"):
                check("R1 no shipped column names the deciding quantity (%s, %s)" % (f, wd), wd not in head)
    # ---------------------------------------------------------------- R3 on the clean truth
    cases = w["cases"]
    true_share = np.array([cases[cases[:, 1] == r, 4].mean() for r in range(10)])
    check("R3 the sampled members' true shares name the golden four", four(true_share) == GOLD,
          [round(100 * x, 1) for x in true_share])
    known = tS["y"] >= 0
    cells = np.zeros(10)
    for r in range(10):
        m = tS["reg"] == r
        tot = 0.0
        for a in range(3):
            for s in range(2):
                cell = m & (tS["age"] == a) & (tS["sex"] == s)
                tot += cell.sum() * tS["y"][cell & known].mean()
        cells[r] = tot / m.sum()
    check("R3a the analyst test: age and sex adjustment cells on the clean truth (every field read correctly, every "
          "filed rule applied) file Pierce, North Sound, King and Spokane", names(four(cells)) == tuple(sorted(NAIVE_NAMES)),
          names(four(cells)))
    check("R3b the decisive step alone (the callback model on the same truth) files the golden four", four(tshare) == GOLD)
    # ---------------------------------------------------------------- the ladder's routes on the pack
    R = RT.run(c)
    for k, v in R.items():
        if k == "callback model, one answer rate per class":
            check("ROUTE %s names the golden four (recorded: the expert route without windows lands)" % k,
                  four(v) == GOLD, names(four(v)))
            continue
        check("SHORTCUT %s does not name the golden four" % k, four(v) != GOLD, names(four(v)))
    check("SHORTCUT the respondents' four is the default path's", names(four(R["respondents (interviews)"])) ==
          tuple(sorted(NAIVE_NAMES)), names(four(R["respondents (interviews)"])))
    # ---------------------------------------------------------------- the family
    F = RT.family(c)
    for k, v in F.items():
        bad = [K.NAME[K.CODES[i]] for i in graded if pct(v[i]) != pct(c["share"][i])]
        check("FAMILY %s names the golden four and prints the four graded whole percents" % k,
              four(v) == GOLD and not bad, bad)
        other = [K.NAME[K.CODES[i]] for i in range(10) if pct(v[i]) != pct(c["share"][i])]
        print("      (%s: ungraded regions whose whole percent differs: %s)" % (k, ", ".join(other) or "none"))
    # ---------------------------------------------------------------- semantic forks
    sf(target, c, fig)
    # ---------------------------------------------------------------- Layer 1 neutral
    layer1(target, c, GOLD)
    # ---------------------------------------------------------------- asks
    asks_checks(target, b, fig, res)
    # ---------------------------------------------------------------- separation
    tmp = os.path.join(task, "_sep_check")
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    shutil.copytree(target, tmp)
    for k in ("roster", "changes", "cases", "regions", "cahps", "pilot"):
        os.remove(os.path.join(tmp, K.FILES[k]))
    c2 = AN.call(tmp)
    shutil.rmtree(tmp)
    check("SEPARATION the call is identical with the enrollment files, the extract, the regions, CAHPS and the pilot "
          "memo removed", float(np.abs(c2["share"] - c["share"]).max()) == 0.0)
    documents(target)
    containers(task)
    realism(target, b, c)
    print("\n%d checks, %d failed" % (COUNT[0], len(FAILS)))
    for f in FAILS:
        print("  FAILED:", f)
    return 0 if not FAILS else 1


def _variant(target, c, mutate):
    """The call re-fitted after a change to the conformed histories."""
    S = {k: dict(v) for k, v in c["S"].items()}
    mutate(S)
    hist = P.histories(S)
    SS = M.summarise(hist)
    return M.em(SS)[0]


def sf(target, c, fig):
    graded = list(c["order"][:4])
    GOLD = four(c["share"])
    import csv

    def same(v):
        return four(v) == GOLD and all(pct(v[i]) == pct(c["share"][i]) for i in graded)

    # SF1: 80 hours or more against more than 80
    rows = list(csv.DictReader(open(os.path.join(target, K.FILES["interviews"]), encoding="utf-8")))
    at80 = {r["case_id"] for r in rows if r["status"] == "Complete" and r["total_hours_march"] == "80"}

    def gt80(S):
        for cid in at80:
            if cid in S:
                S[cid]["cls"] = 0
    v = _variant(target, c, gt80)
    check("SF1 'more than 80 hours' in place of 80 or more (%d members at exactly 80) keeps the call and the graded "
          "percents" % len(at80), len(at80) > 0 and same(v), [pct(v[i]) for i in graded])
    # SF2: the respondents' share is the default path (not a reading of the criteria)
    check("SF2 the respondents' share (criteria 2.2 read as the respondents) names the default path's four",
          names(four(RT.run(c)["respondents (interviews)"])) == tuple(sorted(NAIVE_NAMES)))

    # SF3: a household member answering counted as reaching the member
    import openpyxl
    hh = set()
    for r in csv.DictReader(open(os.path.join(target, K.FILES["dialer"]), encoding="utf-8")):
        if r["disposition"] == "2320":
            hh.add((r["case_id"], P._local(r["call_start"])))

    def household_reached(S):
        for cid, s in S.items():
            new = []
            for (when, ctr, win, res) in s["calls"]:
                if res == 0 and (cid, when) in hh:
                    res = 2                      # read as a contact that did not give an interview
                new.append((when, ctr, win, res))
            s["calls"] = new
    v = _variant(target, c, household_reached)
    check("SF3 a household member answering (2320) read as reaching the member keeps the four",
          four(v) == GOLD, names(four(v)))
    # SF4: the key question's answers ignored
    SK = dict(c["SS"])
    SK["y"] = np.where(c["SS"]["out"] == 1, c["SS"]["y"], -1)
    v = M.em(SK)[0]
    check("SF4 the key question's answers ignored (declines as nonrespondents) keeps the call and the graded percents",
          same(v), [pct(v[i]) for i in graded])
    # SF6: no call between the day and evening shifts, none outside the shifts
    times = [cl[0] for s in c["S"].values() for cl in s["calls"]]
    gap = [t for t in times if t.weekday() < 5 and dt.time(16, 30) < t.time() < dt.time(17, 30)]
    out = [t for t in times if (t.weekday() == 5 and not dt.time(10) <= t.time() <= dt.time(14))
           or (t.weekday() < 5 and not (dt.time(9) <= t.time() <= dt.time(20, 30))) or t.weekday() == 6]
    check("SF6 no survey call falls between 4:30 and 5:30 p.m. or outside the filed shifts, so any split of the day "
          "from the evening classes the calls alike", not gap and not out, (len(gap), len(out)))
    # SF7: the dialer's clock read as UTC fails loudly
    eve = 0
    after_midnight = 0
    for r in csv.DictReader(open(os.path.join(target, K.FILES["dialer"]), encoding="utf-8")):
        if not r["case_id"].startswith("MW26-"):
            continue
        t = dt.datetime.fromisoformat(r["call_start"])
        if t.weekday() < 5 and t.time() >= dt.time(17, 30):
            eve += 1
            u = t.astimezone(dt.timezone.utc)
            after_midnight += u.time() < dt.time(4)
    check("SF7 read as UTC, every weekday evening call lands between midnight and 4 a.m. (a loud misreading)",
          eve > 0 and after_midnight == eve, (eve, after_midnight))
    # SF8: no tie on the unrounded shares
    s = np.sort(c["share"])
    check("SF8 the ten shares have no tie unrounded (0.1 point apart or more)", float(np.diff(s).min()) >= 0.001,
          round(100 * float(np.diff(s).min()), 3))
    # SF9: the region on the October roster for the members found there
    roster = {r["member_id"]: r["region"] for r in csv.DictReader(open(os.path.join(target, K.FILES["roster"]),
                                                                        encoding="utf-8"))}
    sample = {r["case_id"]: r["member_id"] for r in csv.DictReader(open(os.path.join(target, K.FILES["sample"]),
                                                                        encoding="utf-8"))}

    def october_region(S):
        for cid, s in S.items():
            m = sample[cid]
            if m in roster:
                s["region"] = roster[m]
    v = _variant(target, c, october_region)
    moved = sum(1 for cid, m in sample.items() if m in roster and roster[m] != c["S"][cid]["region"])
    check("SF9 each member found on the October roster placed in its October region (%d members move) keeps the four "
          "(closed by criteria 2.2, the region on 1 March 2026)" % moved, four(v) == GOLD,
          "the four's percents under it: %s" % [pct(v[i]) for i in graded])


def layer1(target, c, GOLD):
    import csv
    sample = {r["case_id"] for r in csv.DictReader(open(os.path.join(target, K.FILES["sample"]), encoding="utf-8"))}
    pilot = {r["case_id"] for r in csv.DictReader(open(os.path.join(target, K.FILES["dialer"]), encoding="utf-8"))
             if not r["case_id"].startswith("MW26-")}
    check("R2 the pilot's and the test calls' cases are not in the sample (they cannot enter a sampled member's "
          "history)", not (pilot & sample) and len(pilot) > 0, len(pilot))
    tests = {r["case_id"] for r in csv.DictReader(open(os.path.join(target, K.FILES["interviews"]), encoding="utf-8"))
             if r["case_id"].startswith("TEST")}
    check("R2 the test interviews are not sampled cases", tests and not (tests & sample), len(tests))
    # the member services centre's other outreach counted as failed survey calls
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, K.FILES["crm"]), read_only=True)
    rows = list(wb["Activity"].iter_rows(values_only=True))
    other = {}
    for row in rows[1:]:
        if row[3] not in ("MWIS outbound call", "MWIS case transfer"):
            other.setdefault(row[0], []).append(row)
    by_member = {s["member"]: cid for cid, s in []}
    import pack as PK
    S0 = PK.survey(target)
    mem = {}
    for r in csv.DictReader(open(os.path.join(target, K.FILES["sample"]), encoding="utf-8")):
        mem[r["member_id"]] = r["case_id"]

    def outreach(S):
        for m, rr in other.items():
            cid = mem.get(m)
            if cid is None:
                continue
            reached = [cl for cl in S[cid]["calls"] if cl[3]]
            cut = reached[0][0] if reached else None
            extra = []
            for row in rr:
                d = row[1].date() if isinstance(row[1], dt.datetime) else row[1]
                when = PK._ampm(d, row[2])
                if cut is None or when < cut:
                    extra.append((when, 0, 0, 0))
            S[cid]["calls"] = sorted(S[cid]["calls"] + extra, key=lambda x: (x[0], x[1]))
    v = _variant(target, c, outreach)
    check("R2 the member services centre's other outreach counted as failed survey calls keeps the four",
          four(v) == GOLD, names(four(v)))
    # transferred cases' vendor calls in the transfer queue: read through the call's own time, as every other
    xfer = sum(1 for r in csv.DictReader(open(os.path.join(target, K.FILES["dialer"]), encoding="utf-8"))
               if r["queue"] == "MWIS-XFER")
    check("R2 the transfer queue's calls carry their own times (the window comes from the time, not the queue)",
          xfer > 0, xfer)


def asks_checks(target, b, fig, res):
    A, H = b["A"], b["H"]
    ta, tb = AK.truth(A, H)
    for code in K.CODES:
        n = K.NAME[code]
        check("ASK A the golden equals the clean truth (%s)" % n, fig["ask_a"][n] == ta[code], (fig["ask_a"][n], ta[code]))
        check("ASK B the golden equals the clean truth (%s)" % n, fig["ask_b"][n] == tb[code], (fig["ask_b"][n], tb[code]))
    cr = CR.run(target, fig)
    for code in K.CODES:
        n = K.NAME[code]
        check("ASK A device: the careful path (roster begun by 1 October, leavers restored) misses %s" % n,
              cr["cracker"]["a"][code] != fig["ask_a"][n], (cr["cracker"]["a"][code], fig["ask_a"][n]))
        check("ASK B device: the extract's own count of children under 14 misses %s" % n,
              cr["cracker"]["b"][code] != fig["ask_b"][n], (cr["cracker"]["b"][code], fig["ask_b"][n]))
        check("ASK B device: the careful population with the children's own dates misses %s" % n,
              cr["cracker"]["b_dates"][code] != fig["ask_b"][n], (cr["cracker"]["b_dates"][code], fig["ask_b"][n]))
        check("ASK the mirror (the roster as it stands, the extract's count) misses %s's two figures" % n,
              cr["mirror"]["a"][code] != fig["ask_a"][n] and cr["mirror"]["b"][code] != fig["ask_b"][n])
    # the golden population with the extract's count: the column's own device
    people = AN.covered_oct1(target)
    colb = CR.column_parents(target, people)
    for code in K.CODES:
        n = K.NAME[code]
        check("ASK B device: the golden population with the extract's count misses %s" % n, colb[code] != fig["ask_b"][n],
              (colb[code], fig["ask_b"][n]))
    churn = {}
    for m in A["members"]:
        if m["kind"] == "churn":
            churn[AK.REGION_OF[m["county1"]]] = churn.get(AK.REGION_OF[m["county1"]], 0) + 1
    check("ASK A device mass: every region holds members covered on 1 October who ended and enrolled again in October",
          all(churn.get(cc, 0) >= 5 for cc in K.CODES), churn)
    check("CRACKER keeps none of the 20 ask figures", cr["cracker_hits"] == 0, cr["cracker_hits"])
    check("CRACKER the mirror keeps under 35 per cent of the ask figures", cr["mirror_hits"] < 0.35 * cr["total"],
          cr["mirror_hits"])
    check("CRACKER the pair ceiling is 40 or under", cr["pair"] <= 40.0, round(cr["pair"], 1))
    vals = [fig["ask_a"][K.NAME[cc]] for cc in K.CODES]
    check("ASK A no two regions share a figure", len(set(vals)) == len(vals))
    vals = [fig["ask_b"][K.NAME[cc]] for cc in K.CODES]
    check("ASK B no two regions share a figure", len(set(vals)) == len(vals))


LEAK = ["callback", "call-back", "nonresponse", "non-response", "not at random", "propensity", "weighting",
        "weighted", "adjust", "bias", "hard to reach", "hard-to-reach", "evening calls", "level of effort", "paradata",
        "latent", "imput", "people in work are", "members in work are", "less likely to answer", "harder to reach"]


def documents(target):
    from pypdf import PdfReader
    for k in ("criteria", "methods", "guide", "pilot"):
        txt = " ".join(pg.extract_text() for pg in PdfReader(os.path.join(target, K.FILES[k])).pages).lower()
        txt = re.sub(r"\s+", " ", txt)
        for wd in LEAK:
            check("DOC %s does not say '%s'" % (k, wd), wd not in txt)
        check("DOC %s states no region's share in work (no per cent figure)" % k, not re.search(r"\d+(\.\d+)? ?%", txt)
              and not re.search(r"\d+(\.\d+)? per ?cent", txt))
    txt = open(os.path.join(target, K.FILES["contents"])).read().lower()
    for wd in LEAK:
        check("DOC contents does not say '%s'" % wd, wd not in txt)


def containers(task):
    """H1 and H16: no writer's name in any shipped container, and no stamp outside the fiction's band."""
    import importlib.util
    path = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts",
                        "scrub_producer_metadata.py")
    spec = importlib.util.spec_from_file_location("scrub_producer_metadata", path)
    sm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sm)
    for folder, floor, ceiling in (("target", "2024-01-01", K.ASSEMBLED.date().isoformat()),
                                   ("golden", "2026-10-20", "2026-10-31")):
        d = os.path.join(task, folder)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            r = sm.audit(os.path.join(d, f), floor, ceiling)
            check("CONTAINER %s/%s carries no writer's name and no stamp outside %s to %s" % (folder, f, floor, ceiling),
                  r is None or not (r[0] or r[1]), r)


def realism(target, b, c):
    import csv
    w = b["w"]
    S = c["S"]
    times = [cl for s in S.values() for cl in s["calls"]]
    first, last = min(t[0] for t in times), max(t[0] for t in times)
    check("REALISM every survey call falls between the first release (13 April) and field close (29 May)",
          first.date() >= K.WAVES[0] and last.date() <= K.FIELD_CLOSE, (first, last))
    check("REALISM no call on Memorial Day or a Sunday", not any(t[0].date() in K.HOLIDAYS or t[0].weekday() == 6
                                                                   for t in times))
    check("REALISM the member services centre calls only on weekdays by day",
          all(t[0].weekday() < 5 and t[2] == 0 for t in times if t[1] == 0))
    rel = {}
    for cid, s in S.items():
        rel.setdefault(s["release"], []).append(min(cl[0] for cl in s["calls"]).date())
    check("REALISM no case is called before its release", all(min(v) >= K.WAVES[int(k[1]) - 1] for k, v in rel.items()),
          {k: str(min(v)) for k, v in rel.items()})
    reached_twice = sum(1 for s in S.values() if sum(1 for cl in s["calls"] if cl[3]) > 1)
    check("REALISM no member is called again after the call that reached them",
          all(not any(cl[3] for cl in s["calls"][:-1]) for s in S.values()), reached_twice)
    plan = {}
    for s in S.values():
        k = (s["first"], s["release"] in ("R3", "R4"))
        plan[k] = max(plan.get(k, 0), len(s["calls"]))
    check("REALISM no case exceeds the methods report's calls (6 or 4 by the centre plus up to 4 by the vendor; 8 or 6 "
          "by the vendor)", plan.get(("Trevanna MSC", False), 0) <= 10 and plan.get(("Trevanna MSC", True), 0) <= 8 and
          plan.get(("Kestrelby", False), 0) <= 8 and plan.get(("Kestrelby", True), 0) <= 6, plan)
    ages = [s["age"] for s in S.values()]
    check("REALISM every sampled member is 19 to 64 on 1 March 2026", min(ages) >= 19 and max(ages) <= 64)
    log = list(csv.DictReader(open(os.path.join(target, K.FILES["changes"]), encoding="utf-8"), delimiter="|"))
    at = [r["logged_at"][:10] for r in log]
    check("REALISM the change log runs 1 to 19 October 2026", min(at) >= "2026-10-01" and max(at) <= "2026-10-19")
    hh = list(csv.DictReader(open(os.path.join(target, K.FILES["cases"]), encoding="utf-8")))
    check("REALISM no person joins a case after the extract (15 October)", max(r["member_begin"] for r in hh) <= "2026-10-15")
    ro = list(csv.DictReader(open(os.path.join(target, K.FILES["roster"]), encoding="utf-8")))
    check("REALISM no roster enrollment begins after the export (19 October)",
          max(r["enrollment_begin"] for r in ro) <= "2026-10-19")
    check("REALISM one roster row per member", len({r["member_id"] for r in ro}) == len(ro))
    sample = list(csv.DictReader(open(os.path.join(target, K.FILES["sample"]), encoding="utf-8")))
    on = {r["member_id"] for r in ro}
    found = sum(1 for r in sample if r["member_id"] in on)
    check("REALISM most sampled members are on the October roster (80 to 92 per cent)", 0.80 <= found / 15000 <= 0.92,
          found)
    # H21: invented names away from real places
    places = [x.strip().lower() for x in open(os.path.join(HERE, "h21_reference_places.txt")) if x.strip()]
    for nm in ("Trevanna", "Kestrelby"):
        n = nm.lower()
        near = [p for p in places if edit(n, p) <= 2 or (len(p) >= 6 and p in n) or (len(n) >= 6 and n in p)]
        check("H21 %s is three or more edits from every reference place" % nm, not near, near[:3])
    check("REALISM the personas are the ones drawn", {K.PEOPLE["requester"], K.PEOPLE["vendor"]} ==
          {"Robin Fields", "Dillon Evans"})
    for f in os.listdir(target):
        bb = open(os.path.join(target, f), "rb").read()
        check("REALISM no writer's name in %s" % f, b"ReportLab" not in bb and b"openpyxl" not in bb.lower()
              and b"matplotlib" not in bb.lower())
        if f.endswith((".csv", ".txt")):
            check("REALISM no em dash in %s" % f, "—".encode() not in bb)


def edit(a, b):
    if abs(len(a) - len(b)) > 2:
        return 3
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]
