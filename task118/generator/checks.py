"""checks: the three rules executed on the clean truth (R1 to R3c), the ladder by name and margin, every semantic fork
row (SF1 to SF22), mess neutrality, the asks' devices, separation, the distractors, the input gates and realism.

    python3 task118/generator/checks.py [target]
"""
import collections
import csv
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model as M  # noqa: E402
import params as P  # noqa: E402
import solve as SV  # noqa: E402
import sus as S  # noqa: E402
import world as W  # noqa: E402

D = dt.timedelta
NAMES = {c: n for c, n, _, _ in P.LOCALITIES}


def top(v):
    o = sorted(v, key=lambda k: -v[k])
    return o[0], o[1], v[o[0]] / v[o[1]]


def whole(x):
    return int(x + 0.5)


def pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(path).pages))


def routes_in_memory(seed):
    """the world at another seed, routed in memory: (golden, extract, prevalent-28, current template) by locality"""
    old = P.SEED
    P.SEED = seed
    try:
        prs = W.practices()
        us = W.users(prs)
        cur, leg, move = W.templates(us, prs)
        disp = W.dispensing(us)
    finally:
        P.SEED = old
    loc = {p["code"]: p["locality"] for p in prs}
    first, inq, yob, where = {}, set(), {}, {}
    for r in disp:
        first.setdefault(r["patient_pseudo_id"], r["dispensed_date"])
        if P.CURRENT_FROM <= r["dispensed_date"] <= P.CURRENT_TO:
            inq.add(r["patient_pseudo_id"])
            where[r["patient_pseudo_id"]] = loc[r["practice_code"]]
        yob[r["patient_pseudo_id"]] = r["year_of_birth"]
    users = [p for p in inq if yob[p] <= 1961]
    truth = {u["pid"]: u["start"] for u in us}
    out = {}
    for name, f in (("golden", lambda p: truth[p]), ("extract", lambda p: first[p]),
                    ("prevalent", lambda p: first[p] if first[p] >= P.EXTRACT_FROM + D(days=28) else dt.date(2020, 1, 1))):
        out[name] = SV.by_locality(users, where, f)
    return out


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    res = []

    def ok(label, cond, detail=""):
        res.append((label, bool(cond), detail))

    fig = json.load(open(os.path.join(HERE, "figures.json")))
    c = SV.call(target)
    R = c["routes"]
    g = R["golden"]
    w, r = c["winner"], c["runner"]

    # ------------------------------------------------------------------ the clean truth
    prs = W.practices()
    us = W.users(prs)
    truth = {u["pid"]: u["start"] for u in us}
    cls = {u["pid"]: u["cls"] for u in us}
    st = c["starts"]

    # R1: the field's raw material ships, the deciding quantity does not
    ok("R1a every current user's start, rebuilt from the template chains, is the true first start",
       all(st["golden"][p] == truth[p] or (truth[p] < dt.date(2024, 4, 1) and st["golden"][p] < dt.date(2025, 4, 1))
           for p in c["users"]), "chains whose first template predates the export started before April 2024")
    ok("R1b no current user's start is missing", not c["missing"], "%d missing" % len(c["missing"]))
    exact = sum(1 for p in c["users"] if c["first"][p] == truth[p])
    ok("R1c the extract's first dispensing is no column of first starts", exact < 0.25 * len(c["users"]),
       "%d of %d equal" % (exact, len(c["users"])))
    exact = sum(1 for p in c["users"] if st["current_template"][p] == truth[p])
    ok("R1d the latest template's date is no column of first starts", exact < 0.25 * len(c["users"]),
       "%d of %d equal" % (exact, len(c["users"])))
    tm_cols = next(csv.reader(open(os.path.join(target, P.FILES["templates"]))))
    ok("R1e no shipped column names a first start or an excess", not any(
        re.search(r"first|excess|avoid|risk|rate_ratio", h, re.I) for h in tm_cols), str(tm_cols))

    # R2: each Layer 1 item, mishandled, leaves the call, the runner-up and the gap where they were
    def same_call(v):
        a, b, _ = top(v)
        return a == w and b == r and whole(v[a] - v[b]) == fig["gap_r"]

    ok("R2a the moved practice read off the current system alone (its re-created templates' dates)",
       same_call(R["current_system_root"]), "%s" % {k: round(v, 2) for k, v in R["current_system_root"].items()})
    ok("R2b the moved practice followed one hop into its previous system", same_call(R["previous_system_one_hop"]))
    ok("R2c the chains followed to the earliest template across both exports (one group-by)",
       same_call(R["earliest_both_systems"]) and all(abs(R["earliest_both_systems"][k] - g[k]) < 1e-9 for k in g))
    # the previous system's dates read month-first where they parse
    tm = SV.read(os.path.join(target, P.FILES["templates"]))
    lg = SV.read(os.path.join(target, P.FILES["legacy"]))

    def us_day(s):
        a, b, y = s.split("/")
        try:
            return dt.date(int(y), int(b), int(a)) if int(b) > 12 else dt.date(int(y), int(a), int(b))
        except ValueError:
            return dt.date(int(y), int(b), int(a))
    swapped = dict(st["golden"])
    leg = {t["TemplateRef"]: t for t in lg}
    for t in tm:
        if t["migration_source_ref"]:
            lt = leg[t["migration_source_ref"]]
            while lt["SupersededRef"] in leg:
                lt = leg[lt["SupersededRef"]]
            swapped[t["patient_pseudo_id"]] = us_day(lt["StartDate"])
    ok("R2d the previous system's day-first dates read month-first", same_call(
        SV.by_locality(c["users"], c["where"], lambda p: swapped[p])))
    # the extract's other rows kept: under-65s and patients not dispensed in July to September
    reg, loc = SV.register(target)
    disp = SV.read(os.path.join(target, P.FILES["dispensing"]))
    allp, where_all = set(), {}
    for x in disp:
        allp.add(x["patient_pseudo_id"])
        where_all[x["patient_pseudo_id"]] = loc[x["practice_code"]]
    tstart = st["golden"]
    ok("R2e the extract's under-65s and stopped patients kept with the current users", same_call(
        SV.by_locality(sorted(p for p in allp if p in tstart), where_all, lambda p: tstart[p])))
    ok("R2f processing_month agrees with dispensed_date on every row (either window selects the same users)",
       all(x["processing_month"] == x["dispensed_date"][:7].replace("-", "") for x in disp))

    # R3a: the analyst test, every filed rule applied, the start from the extract
    a, b, lead = top(R["extract_first_dispensing"])
    ok("R3a the easy route (each start from the extract's first dispensing) files Corvenham Central",
       a == "CC" and R["extract_first_dispensing"]["CC"] / R["extract_first_dispensing"][w] >= 1.15,
       "%s %.2f against %s %.2f" % (a, R["extract_first_dispensing"][a], w, R["extract_first_dispensing"][w]))
    # R3b: the decisive step alone moves it to the golden; each lower rung's single correction does not
    ok("R3b the easy route with only the start taken from the template chain files the golden", top(g)[0] == w == "SC")
    for k in (21, 28, 35, 56):
        v = R["prevalent_long_term_%d" % k]
        a2 = top(v)[0]
        ok("R3b prevalent users taken as long-term (washout %d days) files %s, not the golden" % (k, NAMES[a2]),
           a2 != w and v[a2] / v[w] >= 1.15, "%s %.2f against %s %.2f" % (a2, v[a2], w, v[w]))
    a2 = top(R["current_template"])[0]
    ok("R3b each start from the latest template's date files Corvenham Central", a2 == "CC" and
       R["current_template"]["CC"] / R["current_template"][w] >= 1.15)
    ok("R3b the users counted flat file Corvenham Central", top(R["users"])[0] == "CC" and
       R["users"]["CC"] / R["users"][w] >= 1.15)
    # R3c: no plant
    th = open(os.path.join(target, P.FILES["thread"]), encoding="utf-8").read()
    pol = pdf_text(os.path.join(target, P.FILES["policy"]))
    ok("R3c the thread names no locality and no figure for the placement",
       not any(n in th for n in NAMES.values()) and not re.search(r"\b\d+ (admissions|falls)\b", th))
    ok("R3c the policy names no locality", not any(n in pol for n in NAMES.values()))
    seqs = collections.defaultdict(list)
    for x in disp:
        seqs[x["practice_code"]].append(x["dispensed_date"])
    ok("R3c no practice's dispensing dates copy another's", len({tuple(v[:200]) for v in seqs.values()}) == len(seqs))

    # ------------------------------------------------------------------ the ladder
    ok("L1 the golden: Saltreach Coast leads Hethermoss by 1.15 or more", w == "SC" and r == "HM" and g[w] / g[r] >= 1.15,
       "%.3f" % (g[w] / g[r]))
    for name, need in (("users", "CC"), ("extract_first_dispensing", "CC"), ("current_template", "CC"),
                       ("prevalent_long_term_28", "HM")):
        v = R[name]
        ok("L2 %s names %s" % (name, NAMES[need]), top(v)[0] == need, "%s" % top(v)[0])
    ok("L3 Saltreach Coast tops no wrong route", all(top(R[k])[0] != "SC" for k in R if k not in (
        "golden", "earliest_both_systems", "current_system_root", "previous_system_one_hop")))
    for k, v in (("avoided", fig["avoided"]), ("runner_avoided", fig["runner_avoided"]), ("gap", fig["gap"])):
        dist = abs((v % 1) - 0.5)
        ok("L4 %s %.3f sits 0.15 or more inside its whole-number bin" % (k, v), dist >= 0.15, "%.3f" % dist)
    ok("L5 the gap rounds the same either way", whole(g[w] - g[r]) == whole(g[w]) - whole(g[r]) == fig["gap_r"])
    for seed in (P.SEED + 1, P.SEED + 2):
        v = routes_in_memory(seed)
        a, b, lead = top(v["golden"])
        ok("L6 at seed %d the golden is Saltreach Coast over Hethermoss by 1.15 and the easy routes miss it" % seed,
           a == "SC" and b == "HM" and lead >= 1.15 and top(v["extract"])[0] == "CC" and top(v["prevalent"])[0] != "SC",
           "%s %s %.3f" % (a, b, lead))

    # ------------------------------------------------------------------ the semantic fork table (the call)
    def call_of(v):
        a, b, _ = top(v)
        return a, b, whole(v[a]), whole(v[b]), whole(v[a] - v[b])
    gold_call = call_of(g)
    yob = {}
    for x in disp:
        yob[x["patient_pseudo_id"]] = int(x["year_of_birth"])
    inq62 = sorted({x["patient_pseudo_id"] for x in disp if "2026-07-01" <= x["dispensed_date"] <= "2026-09-30"
                    and int(x["year_of_birth"]) <= 1962})
    ok("SF1 aged 65 on 1 January 2027 read as 65 during 2027 (born 1962 kept): same call and figures",
       call_of(SV.by_locality(inq62, where_all, lambda p: tstart[p])) == gold_call)
    in_ex = sorted({x["patient_pseudo_id"] for x in disp if "2026-07-01" < x["dispensed_date"] < "2026-09-30"
                    and int(x["year_of_birth"]) <= 1961})
    ok("SF2 the July to September window read without its end days: same call and figures",
       call_of(SV.by_locality(in_ex, where_all, lambda p: tstart[p])) == gold_call)
    ok("SF3 the chain's root equals the earliest start across both exports for every current user",
       all(st["golden"][p] == st["earliest"][p] for p in c["users"]))
    ok("SF4 a chain whose first template predates the export, dated anywhere before April 2025: same figures",
       call_of(SV.by_locality(c["users"], c["where"], lambda p: dt.date(2001, 1, 1) if st["golden"][p] < dt.date(
           2024, 4, 1) else st["golden"][p])) == gold_call)

    def days_months(d, m):
        return d + D(days=round(m * 30.4375))
    alt = collections.defaultdict(float)
    for p in c["users"]:
        alt[c["where"][p]] += M.excess_years(st["golden"][p], months=days_months)
    alt = {k: P.STOP * P.BASE / 100 * v for k, v in alt.items()}
    ok("SF5 months as 30.4375 days rather than calendar months: same call and figures", call_of(alt) == gold_call)
    ok("SF6 days over 365.25 rather than 365: same call and figures",
       call_of({k: v * 365 / 365.25 for k, v in g.items()}) == gold_call)
    ok("SF7 the window as three quarters of a year rather than 275 days: same call and figures",
       call_of({k: v * 0.75 / (275 / 365) for k, v in g.items()}) == gold_call)

    def strict(d, m):
        return M.add_months(d, m) + D(days=1)
    alt = collections.defaultdict(float)
    for p in c["users"]:
        alt[c["where"][p]] += M.excess_years(st["golden"][p], months=strict)
    alt = {k: P.STOP * P.BASE / 100 * v for k, v in alt.items()}
    ok("SF8 the 24-month boundary counted inclusive: same call and figures", call_of(alt) == gold_call)
    first_tm = {}
    for t in tm:
        if not t["replaces_template_id"] and not t["migration_source_ref"]:
            first_tm[t["patient_pseudo_id"]] = t["authorised_from"]
    starters = [p for p in c["users"] if st["golden"][p] >= P.EXTRACT_FROM]
    ok("SF9 a start inside the extract: the first template's date is the first dispensing's (%d users)" % len(starters),
       all(c["first"][p] == st["golden"][p] for p in starters))
    tm_prac = {t["patient_pseudo_id"]: t["practice_code"] for t in tm}
    ok("SF10 every current user's practice in the templates is the practice in the extract",
       all(loc[tm_prac[p]] == c["where"][p] for p in c["users"]))
    ok("SF11 the gap rounds the same from the exact figures and from the rounded ones", whole(g[w] - g[r]) ==
       whole(g[w]) - whole(g[r]))
    ok("SF12 the stop share applied per user or to the total: linear, same figures", abs(
        sum(g.values()) - P.STOP * P.BASE / 100 * sum(M.excess_years(st["golden"][p]) for p in c["users"])) < 1e-6)
    ok("SF13 no current user is under 6 months on the drug on 1 April 2027, so the first band never applies",
       all(M.add_months(st["golden"][p], 6) <= P.OFF_FROM for p in c["users"]))
    ok("SF14 every migration_source_ref resolves in the previous system's export",
       all(t["migration_source_ref"] in leg for t in tm if t["migration_source_ref"]))

    # ------------------------------------------------------------------ the asks
    asks = SV.asks(target)
    g_sus = S.build(prs)
    ok("A1 the 24 falls figures rebuilt from the pack equal the stays the world made", asks == S.truth(g_sus, prs))
    ok("A1 figures.json carries them", fig["asks"] == asks)
    fields = ("falls_65_79", "falls_80", "bed_days", "readmitted")

    def hits(v):
        return sum(1 for k in asks for f in fields if v[k][f] == asks[k][f])
    ok("SF15 stays joined across a gap of up to two days rather than one: same 24 figures",
       SV.asks(target, gap=2) == asks)
    ok("SF16 a stay may not start with 2B or 81 here (every such spell is a move in): 2B counted as emergency or not, "
       "same figures", SV.asks(target, emergency=SV.EMERGENCY) == asks)
    for name, kw, most in (("shift: sorted by admission date, joined to the next row", dict(link="shift"), 3),
                           ("joined only where the receiving source is a hospital", dict(link="dest_src"), 3),
                           ("joined only where the receiving method is 2B or 81", dict(link="dest_method"), 3),
                           ("joined where the receiving source or method says so", dict(link="dest_either"), 3),
                           ("joined only on the same day", dict(link="dest", gap=0), 4),
                           ("every spell beginning within a day of the last merged", dict(link="consecutive"), 2),
                           ("spells counted as admissions", dict(link="none"), 2),
                           ("spells counted, every emergency method", dict(link="none", emergency=SV.EMERGENCY), 2)):
        h = hits(SV.asks(target, **kw))
        ok("A2 device: %s keeps %d of 24 (at most %d)" % (name, h, most), h <= most)
    nopred = {x["Practice code"]: x["Locality code"] for x in reg}
    v = SV.asks(target, loc=nopred)
    ok("A3 the retired practice code unmatched moves Fenmarsh's four figures and nothing else",
       all(v[k] == asks[k] for k in asks if k != "FM") and all(v["FM"][f] != asks["FM"][f] for f in fields))
    v = SV.asks(target, readmit_from="first")
    ok("A3 the readmission clock from the first hospital's discharge misses every locality's readmissions",
       all(v[k]["readmitted"] != asks[k]["readmitted"] for k in asks))
    sp = SV.spells(target)
    stays = SV.stays(sp)
    ok("A4 every 2B or 81 spell is a move in, inside a stay", all(s["method"] not in SV.TRANSFER_IN for s in stays))
    by_loc = collections.defaultdict(lambda: collections.Counter())
    pid_loc = {}
    for s in stays:
        pid_loc[s["pid"]] = loc.get(s["practice"])
    for s in stays:
        L = pid_loc[s["pid"]]
        for a_, b_ in zip(s["spells"], s["spells"][1:]):
            if a_["adm"] == a_["dis"] == b_["adm"]:
                by_loc[L]["same-day move on the day of admission"] += 1
            if (b_["adm"] - a_["dis"]).days == 1:
                by_loc[L]["move admitted the next day"] += 1
            if b_["method"] not in SV.TRANSFER_IN or b_["source"] not in SV.HOSPITAL_SOURCE:
                by_loc[L]["move coded as a fresh admission"] += 1
    per_p = collections.defaultdict(list)
    for s in stays:
        per_p[s["pid"]].append(s)
    for p, ss in per_p.items():
        ss.sort(key=lambda s: s["start"])
        for a_, b_ in zip(ss, ss[1:]):
            if a_["fall"] and 0 <= (b_["start"] - a_["end"]).days <= 1 and b_["method"] in SV.EMERGENCY:
                by_loc[pid_loc[p]]["readmitted the day of leaving or the next"] += 1
    for k in NAMES:
        for dev, need in (("same-day move on the day of admission", 5), ("move admitted the next day", 5),
                          ("move coded as a fresh admission", 5), ("readmitted the day of leaving or the next", 3)):
            ok("A5 %s: %s %d (5 or more)" % (NAMES[k], dev, by_loc[k][dev]), by_loc[k][dev] >= need)
    q = sum(1 for x in SV.read(os.path.join(target, P.FILES["sus"])) if x["gp_practice_code"] == P.MERGED[0])
    ok("A5 the retired code Q80117 on %d episodes, none after 30 September 2025" % q, q >= 50 and all(
        x["episode_start_date"] < "2025-10-01" for x in SV.read(os.path.join(target, P.FILES["sus"]))
        if x["gp_practice_code"] == P.MERGED[0]))
    ok("A6 no ask figure is a round hundred", all(asks[k][f] % 100 for k in asks for f in fields))
    fd = pdf_text(os.path.join(target, P.FILES["falls_def"]))
    for sf, phrase in (("SF17", "on the day they left or in the 30 days after it"),
                       ("SF18", "the patient's age at the start of the admission"),
                       ("SF19", "the day of leaving is not counted"),
                       ("SF20", "of the patient's registered practice at the start of the admission"),
                       ("SF21", "A patient discharged to another hospital is still in hospital care"),
                       ("SF22", "alive on leaving hospital care")):
        ok("%s the falls definitions file it: %r" % (sf, phrase), phrase in fd)

    # ------------------------------------------------------------------ separation and distractors
    tmp = tempfile.mkdtemp()
    try:
        for f in os.listdir(target):
            if f not in (P.FILES["sus"], P.FILES["falls_def"], P.FILES["providers"], P.FILES["dashboard"],
                         P.FILES["referrals"]):
                shutil.copy(os.path.join(target, f), tmp)
        c2 = SV.call(tmp)
        ok("S1 the call reads none of the SUS cohort, the falls definitions or the site list", c2["routes"]["golden"] == g)
        for f in (P.FILES["sus"], P.FILES["falls_def"], P.FILES["providers"]):
            shutil.copy(os.path.join(target, f), tmp)
        ok("D1 the two distractors deleted: the call and the 24 figures unchanged", SV.asks(tmp) == asks and
           SV.call(tmp)["routes"]["golden"] == g)
    finally:
        shutil.rmtree(tmp)
    call_text = "".join(open(os.path.join(target, P.FILES[k]), encoding="utf-8").read()
                        for k in ("dispensing", "templates", "legacy"))
    ok("S2 the retired code is in no file the call reads", P.MERGED[0] not in call_text)

    # ------------------------------------------------------------------ input gates and realism
    files = sorted(os.listdir(target))
    meta = json.load(open(os.path.join(os.path.dirname(HERE), "metadata.json")))
    ok("G1 twelve files", len(files) == 12 and set(files) == set(P.FILES.values()))
    ok("G2 four formats", {f.rsplit(".", 1)[1] for f in files} == {"csv", "xlsx", "pdf", "eml"})
    rows = {f: sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv")}
    ok("G3 a file of 25,000 rows or more", max(rows.values()) >= 25000, "%s" % rows)
    ok("G4 the distractors are named in metadata.json and present", sorted(meta["distractor_files"]) ==
       sorted(P.FILES[k] for k in P.DISTRACTORS))
    ok("G5 no notes, readme or dictionary under target/", not any(re.search(r"note|readme|dictionar|distract", f, re.I)
                                                                  for f in files))
    dash = "—–"
    texts = [open(os.path.join(target, f), encoding="utf-8").read() for f in files if f.endswith((".csv", ".eml"))]
    texts += [pdf_text(os.path.join(target, P.FILES[k])) for k in ("policy", "falls_def")]
    ok("RS1 no em or en dash in any shipped text", not any(ch in t for t in texts for ch in dash))
    ok("RS2 no locality's current users a round hundred", all(v % 100 for v in c["n_users"].values()),
       "%s" % c["n_users"])
    ok("RS3 every dispensing date inside April to September 2026", all(
        "2026-04-01" <= x["dispensed_date"] <= "2026-09-30" for x in disp))
    ok("RS4 every template authorised on or before 1 October 2026", all(t["authorised_from"] <= "2026-10-01" for t in tm))
    words = r"first dispens|left[- ]trunc|prevalent|chain|root|depletion"
    docs_text = th + " " + pol + " " + fd
    ok("RS5 no document names the decisive step", not re.search(words, docs_text, re.I),
       "; ".join(sorted(set(m.group(0) for m in re.finditer(words, docs_text, re.I)))))
    for phrase in ("aged 65 or over on 1 January 2027 with a benzodiazepine or Z-drug dispensed between 1 July and 30 "
                   "September 2026", "45 in every 100", "from 1 April 2027 to 31 December 2027",
                   "the time since the patient first started a benzodiazepine or Z-drug", "4.0 per 100 patients a year"):
        ok("DOC the policy files %r" % phrase[:60], phrase in pol)

    bad = [x for x in res if not x[1]]
    for label, good, detail in res:
        if not good or "-v" in sys.argv:
            print("%s  %s%s" % ("PASS" if good else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    print("checks: %d of %d passed" % (len(res) - len(bad), len(res)))
    return len(bad)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    sys.exit(1 if main(args[0] if args else None) else 0)
