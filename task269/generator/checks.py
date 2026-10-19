"""task269's assertions, run by build.py after the pack and the goldens are written: the golden from the generator's
truth and from the cut pack agree; the three rules executed (the easy route files the wrong count on the clean truth,
the decisive step alone files the golden); every semantic fork row; every graded figure's distance to its rounding
edge; the ladder; the separation of the asks from the call; the cracker's misses; the input gates; the house checks."""
import csv
import datetime as dt
import json
import math
import os
import re
import shutil
import sys
import unicodedata

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402
import common as K     # noqa: E402
import cracker as CR   # noqa: E402
import verify as V     # noqa: E402
import world as W      # noqa: E402

N = [0]


def ok(cond, msg):
    N[0] += 1
    assert cond, msg


def edge(v, unit):
    return unit / 2 - abs(v - round(v / unit) * unit)


def three_rules(w):
    """Executed on the generator's clean truth (dataset-generation 7.1): the true variance components, the 2026
    design's four domains of three stations. The easy route a strong analyst takes, the textbook decision study
    that treats the stations as drawn from one undivided bank and counts the examiner's stringency as error, files
    two or more stations above the golden; changing only the decisive step, the candidate-by-domain variance counted
    as true score because the blueprint fixes the domains, files the golden; the naive single-examiner route keeps 12
    or fewer."""
    s = W.SIG
    p_pool = s["p"] + 12 / 66 * s["pd"]
    ps_pool = s["ps"] + 54 / 66 * s["pd"]
    easy = A.smallest(lambda n: p_pool / (p_pool + (ps_pool + s["rs"] + s["e"]) / n))
    naive = A.smallest(lambda n: p_pool / (p_pool + (ps_pool + s["e"]) / n))
    gold = A.smallest(lambda n: A.rel_2027({"p": s["p"], "pd": s["pd"], "ps": s["ps"], "rs": s["rs"], "e": s["e"]}, n))
    ok(easy >= gold + 2, "R3a the easy route on the clean truth (%d) is not two or more above the golden (%d)"
       % (easy, gold))
    ok(naive <= 12 and naive < gold, "R3a the naive route on the clean truth (%d) is not 12 or under" % naive)
    fig = w["fig"]
    y = W.station_marks(w["marks"])
    L = A.ladder(y, w["seed"])
    G = L["golden"]["stations"]
    ok(fig["call"]["stations"] == G, "the golden on the data is not the figures' call")
    # on the data: the easy route files a different number, the decisive step alone moves it to the golden
    ok(L["R3"]["stations"] >= G + 2, "R3b the easy route on the data is not two or more above the golden")
    ok(L["R1"]["stations"] <= 12, "R3a the naive route on the data does not keep 12")
    # each lower rung's single correction leaves it on a wrong answer
    for rung in ("R0", "R1", "R1s", "R3", "abs"):
        ok(L[rung]["stations"] != G, "R3b rung %s lands the golden" % rung)
    ok(L["R2"]["stations"] != G and L["R2"]["half_stations"] != G, "R3b the random pick lands the golden")
    return L


def r1_r2_r3c(t, w):
    """R1 the field's raw material ships and no column holds the deciding quantity; R2 every Layer 1 item on the
    call's path, mishandled the natural way, leaves the call and every printed reliability where they were;
    R3c no plant: no repeated block of item marks beyond the genre's own rate."""
    import openpyxl
    with open(os.path.join(t, K.FILES["marks"]), encoding="utf-8") as f:
        head = f.readline().strip().split(",")
    ok(head == ["exam_no", "exam_day", "round", "station", "examiner", "role", "item", "response", "recorded_at"],
       "R1 the marks export's layout")
    bad = re.compile(r"reliab|variance|alpha|generaliz|stringen|hawk|dove", re.I)
    for f in os.listdir(t):
        path = os.path.join(t, f)
        if f.endswith(".csv"):
            with open(path, encoding="utf-8") as fh:
                ok(not bad.search(fh.readline()), "R1 a deciding quantity's column in %s" % f)
        if f.endswith(".xlsx"):
            wb = openpyxl.load_workbook(path, data_only=True)
            for ws in wb.worksheets:
                for row in ws.iter_rows(values_only=True):
                    for c in row:
                        ok(not (isinstance(c, str) and bad.search(c)), "R1 a deciding quantity in %s" % f)
    for f in (K.FILES["policy"], K.FILES["minutes"], K.FILES["migration"], K.FILES["feedback"]):
        txt = V.pdf_text(os.path.join(t, f))
        ok(len(txt) > 300, "R1 %s not read" % f)
        rx = r"stringen|hawk|dove|leniency|lenient|generaliz|Spearman|alpha|examiner effect"
        if f != K.FILES["policy"]:
            rx += "|variance"      # policy 4.3 defines the reliability as a share of the variance (the estimand)
        ok(not re.search(rx, txt, re.I), "R1 %s names the decisive relation" % f)
    ptxt = V.docx_text(os.path.join(t, K.FILES["plan"]))
    ok("Each station will have one examiner in each circuit" in ptxt, "R1 plan positive control")
    ok(not re.search(r"stringen|hawk|dove|lenien|variance|generaliz|Spearman|alpha|calibrat", ptxt, re.I),
       "R1 the plan names the decisive relation")
    # R2: per Layer 1 item on the call's path, the natural mishandling
    base = A.ladder(W.station_marks(w["marks"]), w["seed"])["golden"]
    for kw, item in (({"include_withdrawn": True}, "withdrawn item kept on day 1"),
                     ({"na_as_zero": True}, "items not applicable scored zero")):
        g = A.ladder(W.station_marks(w["marks"], **kw), w["seed"])["golden"]
        ok(g["stations"] == base["stations"] and all(abs(g["at"][n] - base["at"][n]) < 0.006 for n in K.SETTINGS)
           and g["at"][base["stations"] - 1] < K.STANDARD, "R2 %s moves the call" % item)
    # the global grades sit in their own table, so no reading of the marks export takes them as an item
    with open(os.path.join(t, K.FILES["marks"]), encoding="utf-8") as fh:
        items = {line.split(",")[6] for line in fh.readlines()[1:]}
    ok(all(x.isdigit() for x in items), "R2 a non-checklist row in the marks export")
    # R3c: no item block repeated beyond the genre's rate
    import collections
    dup = tot = 0
    for st in K.STATIONS26:
        c = collections.Counter()
        for i in range(84):
            for ro in (0, 1):
                v = w["marks"]["rec"][(i, st[0], ro)]["items"]
                vec = tuple(v[k] for k in sorted(v))
                if 0 < sum(vec) < 2 * len(vec):
                    c[vec] += 1
        dup += sum(n - 1 for n in c.values() if n > 1)
        tot += sum(c.values())
    ok(dup / tot < 0.02, "R3c repeated item blocks: %d of %d" % (dup, tot))


def realism(t):
    """No library signature or build clock in the containers; document control dates after the events they
    describe; no identical counts across sites and sessions; the distractors deletable."""
    import zipfile
    for f in os.listdir(t):
        path = os.path.join(t, f)
        raw = open(path, "rb").read()
        ok(b"openpyxl" not in raw and b"python-docx" not in raw and b"ReportLab" not in raw
           and b"reportlab" not in raw, "H1 a writer's signature in %s" % f)
        if f.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(path) as z:
                core = z.read("docProps/core.xml").decode()
                app = z.read("docProps/app.xml").decode()
                ok("Microsoft" in app and "2026" in core or "2025" in core or "2019" in core, "H1 %s stamps" % f)
                for m in re.findall(r"<dcterms:\w+ [^>]*>([^<]+)<", core):
                    ok("2019-01-01" <= m[:10] <= K.PACK_DATE.isoformat(), "H1 %s stamp %s" % (f, m))
    # document control dates: the minutes after the sitting, the report after the cut-over and switch-off,
    # the plan before the form closes, the policy before the 2026-27 session's first allocation
    mig = V.pdf_text(os.path.join(t, K.FILES["migration"]))
    ok("2 December 2025" in mig and "28 November 2025" in mig, "the migration report's date and the switch-off")
    ok("closes on 27 November" in V.docx_text(os.path.join(t, K.FILES["plan"])), "the plan's tense on the form")
    # H25: every PDF reads the same to a strict and a lenient parser and to an independent extractor
    import io
    import warnings
    import pypdf
    from pdfminer.high_level import extract_text
    for f in sorted(os.listdir(t)):
        if f.endswith(".pdf"):
            raw = open(os.path.join(t, f), "rb").read()
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                strict = "".join(pg.extract_text() for pg in pypdf.PdfReader(io.BytesIO(raw), strict=True).pages)
            lenient = "".join(pg.extract_text() for pg in pypdf.PdfReader(io.BytesIO(raw)).pages)
            miner = " ".join(extract_text(io.BytesIO(raw)).split())
            ok(strict == lenient and not caught and "Callowfield" in miner, "H25 %s" % f)
            if f == K.FILES["policy"]:
                ok("with a reliability of at least 0.80" in miner, "H25 the standard unreadable to pdfminer")
    b = V.ask_b(t)
    ok(len(set(b.values())) >= 8, "ask B counts too uniform")
    # training sessions run on a Tuesday, Wednesday or Thursday outside the holidays; the initial training dates
    # before the log likewise; a Mr or Ms agrees with the forename
    with open(os.path.join(t, K.FILES["training"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d = dt.date.fromisoformat(r["session_date"])
            ok(W._working_day(d) == d, "a training session on %s" % d)
    for r in V.rows_xlsx(os.path.join(t, K.FILES["register"])):
        d = V.bank_date(r["Examiner training"])
        ok(W._working_day(d) == d, "initial training on %s" % d)
        if r["Title"] in ("Mr", "Ms"):
            ok(W._gender(r["Forename"]) == {"Mr": "M", "Ms": "F"}[r["Title"]], "%s %s" % (r["Title"], r["Forename"]))
    # each distractor deletable: the call and both asks unchanged without it
    tmp = os.path.join(os.path.dirname(t), ".dis")
    for d in (K.FILES["sp_invoices"], K.FILES["feedback"], K.FILES["global"]):
        if os.path.exists(tmp):
            shutil.rmtree(tmp)
        shutil.copytree(t, tmp)
        os.remove(os.path.join(tmp, d))
        ok(V.call(tmp)["stations"] == V.call(t)["stations"] and V.ask_a(tmp) == V.ask_a(t)
           and V.ask_b(tmp) == V.ask_b(t), "deleting %s moves an answer" % d)
        shutil.rmtree(tmp)


def ladder(L):
    g = L["golden"]
    G = g["stations"]
    ok(12 < G < K.ROOMS27, "the golden is not inside the rooms and above the current twelve")
    ok(g["at"][G] - K.STANDARD >= 0.004 and K.STANDARD - g["at"][G - 1] >= 0.004,
       "the bar's neighbours within 0.004 of 0.80")
    # SF6 the call on the unrounded coefficient; the setting below prints under 0.80 at two decimals too
    ok(round(g["at"][G - 1], 2) < K.STANDARD, "SF6 the setting below prints 0.80 at two decimals")
    for n in K.SETTINGS:
        # seven settings a station apart step about one printed cell each, so no world clears every edge by more
        # than about 0.001; the figures are held instead by every licensed estimator printing the same (C1)
        ok(edge(g["at"][n], 0.01) >= 0.0003, "reliability at %d stations within 0.0003 of its rounding edge" % n)
        # the estimator family the data does not close prints the same figure (C1)
        ok(round(g["multivariate"][n], 2) == round(g["at"][n], 2), "the multivariate study prints %d otherwise" % n)
    ok(A.smallest(lambda n: g["multivariate"][n] if n in g["multivariate"] else 0) == G,
       "the multivariate study files another call")
    ok(L["abs"]["stations"] > K.ROOMS27, "the absolute coefficient within the rooms")
    # the write-up's formula on the components as printed (two decimals) prints every reliability the same
    vr = {k: round(float(L["v"][k]), 2) for k in ("p", "pd", "ps", "rs", "e")}
    for n in K.SETTINGS:
        ok(round(A.rel_2027(vr, n), 2) == round(g["at"][n], 2), "the printed components print %d otherwise" % n)


def forks(w):
    """SF1 to SF14 (design note, semantic fork table)."""
    y = W.station_marks(w["marks"])
    L = A.ladder(y, w["seed"])
    v = L["v"]
    G = L["golden"]["stations"]
    # SF1 reliability for ranking (relative) against the absolute coefficient: the absolute one files no setting
    ok(L["abs"]["stations"] > K.ROOMS27, "SF1 absolute coefficient reaches 0.80 within the rooms")
    # SF2 the total mark is the sum of the station marks, each out of 20, filed in policy 3.2
    pol = V.pdf_text(os.path.join(os.path.dirname(HERE), "target", K.FILES["policy"]))
    ok("A candidate's total mark is the sum of their station marks" in pol and "expressed out of 20" in pol,
       "SF2 policy 3.2 not filed")
    # SF3 items not applicable counted as zero: same call; SF4 the withdrawn item kept on day 1: same call
    for kw, sf in (({"na_as_zero": True}, "SF3"), ({"include_withdrawn": True}, "SF4")):
        g = A.ladder(W.station_marks(w["marks"], **kw), w["seed"])["golden"]
        ok(g["stations"] == G, "%s moves the call" % sf)
    # SF5 the 2027 arrangement: with the examiner shared by a circuit session's candidates (twelve groups) the
    # expected coefficient over the groups files the same number
    ok(A.smallest(lambda n: A.rel_2027(v, n, 11 / 12)) == G, "SF5 the examiner groups move the call")
    # SF7 the 2026 sitting's marks: every candidate of both days (84), every station's two examiners
    ok(y.shape == (84, 12, 2), "SF7 the 2026 sitting is not 84 by 12 by 2")
    # SF8 station marks as the system prints them (one decimal): the same call and the same printed figures
    g1 = A.ladder(np.round(y, 1), w["seed"])["golden"]
    ok(g1["stations"] == G and all(round(g1["at"][n], 2) == round(L["golden"]["at"][n], 2) for n in K.SETTINGS),
       "SF8 station marks at one decimal move a figure")
    # SF9 the order of the rows and of the candidates changes nothing
    perm = np.random.default_rng(5).permutation(84)
    ok(A.ladder(y[perm], w["seed"])["golden"]["stations"] == G, "SF9 order moves the call")
    # SF10 the examiner roles (lead, second) exchanged at every station: same components
    v2, _ = A.gstudy(y[:, :, ::-1])
    ok(all(abs(v2[k] - v[k]) < 1e-9 for k in v), "SF10 roles exchanged move the components")
    # SF11 every component positive, so REML on the balanced design gives the expected-mean-square components
    ok(all(v[k] > 0 for k in v), "SF11 a negative component")
    # SF12 whole stations 12 to 18, the smallest reaching the bar
    ok(sorted(K.SETTINGS) == list(range(12, 19)), "SF12 settings")
    # SF13 the blueprint's remainder drawn in policy 4.2's order: the pooled study with domains is order-free and
    # the multivariate study takes the policy's order (both asserted in ladder())
    # SF14 the univariate study with domains and the multivariate study by domain print the same (asserted in ladder)


def separation(t, w):
    """No ask file is read by the call: the call computes identically from a pack without them; no device row sits
    in the call's files (they hold no case bank, register, form or training row)."""
    tmp = os.path.join(os.path.dirname(t), ".sep")
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    os.makedirs(tmp)
    keep = [K.FILES[k] for k in ("marks", "stations", "examiners26", "minutes", "policy", "plan")]
    for f in keep:
        shutil.copy(os.path.join(t, f), tmp)
    a, b = V.call(t), V.call(tmp)
    shutil.rmtree(tmp)
    ok(a["stations"] == b["stations"] and all(abs(a["reliability"][n] - b["reliability"][n]) < 1e-12
                                              for n in K.SETTINGS), "the call reads an ask file")


def asks(t, w):
    # Ask B's window: the plan files the allocation's date, three years after which the training must fall
    plan = V.docx_text(os.path.join(t, K.FILES["plan"]))
    ok("allocates examiners on Monday 7 December" in plan and K.ALLOCATION == dt.date(2026, 12, 7)
       and K.ALLOCATION.weekday() == 0 and K.TRAINED_FROM == dt.date(2023, 12, 7), "ask B: the allocation date")
    a = V.ask_a(t)
    b = V.ask_b(t)
    fig = w["fig"]
    for d in K.DOMAINS:
        ok(tuple(fig["ask_a"][d]) == a[d], "ask A %s pack against truth" % d)
    for k, n in b.items():
        ok(fig["ask_b"]["%s %s" % k] == n, "ask B %s pack against truth" % (k,))
        ok(n >= K.ROOMS27, "ask B %s under the room limit: the plan's examiners would not staff 18 stations" % (k,))
    # every domain carries the device on both figures; every site and session carries it
    bank = w["bank"]
    exposed = {u["code"] for u in bank["usage"] if u["date"].year in K.EXPOSURE_YEARS}
    for d in K.DOMAINS:
        dev = [c for c in bank["cases"] if c["domain"] == d and c["cat"] == "device"]
        ok(len(dev) == 3 and all(c["origin"] in exposed for c in dev), "ask A device rows in %s" % d)
        ok(any(c["resources"] in W.SP_NEED for c in dev), "ask A device misses %s's simulated patient count" % d)
        twin = [c for c in bank["cases"] if c["domain"] == d and c["cat"] == "twin_new"]
        ok(len(twin) == 1 and twin[0]["resources"] in W.SP_NEED, "ask A over-cleaning half in %s" % d)
        namesake = [c for c in bank["cases"] if c["cat"] == "retired_twin_old" and c["title"] == twin[0]["title"]]
        ok(len(namesake) == 1 and namesake[0]["specialty"] == twin[0]["specialty"]
           and twin[0]["created"].year == 2026 and twin[0]["version"] == 1 and twin[0]["reviewed"] > K.BANK_MIGRATION,
           "ask A: the newer case of a retired title, written in 2026 at version 1")
        dev = [c for c in bank["cases"] if c["domain"] == d and c["cat"] == "device"]
        ok(sum(c["title"] in W.REVISED_TITLE.values() for c in dev) == 2, "ask A: two of three re-created cases renamed")
    # the bank's records are coherent: a re-created record carries its old one's domain, specialty and resources,
    # its version one on and a review the group signed off in 2026; a retired record was last reviewed before it was
    # retired; beside each re-created record's old record sits a retired record of the same specialty, and the first
    # eligible re-created record shares its specialty and resources with the case retired after its 2025 sitting
    by_code = {c["code"]: c for c in bank["cases"]}
    pairs = V.recreated_pairs(V.rows_xlsx(os.path.join(t, K.FILES["bank"]), "Cases"))
    ok(pairs == {c["code"]: c["origin"] for c in bank["cases"] if c["origin"]}, "ask A: the version link files "
       "another old record")
    for c in bank["cases"]:
        if c["origin"]:
            o = by_code[c["origin"]]
            ok(c["title"] in (o["title"], W.REVISED_TITLE.get(o["title"]))
               and (o["domain"], o["specialty"], o["resources"]) == (c["domain"], c["specialty"], c["resources"])
               and c["version"] == o["version"] + 1 and o["status"] == "Retired" and o["reviewed"] < K.BANK_MIGRATION
               and dt.date(2026, 1, 1) <= c["reviewed"] <= K.BANK_EXPORT and c["reviewed"].weekday() < 5,
               "re-created record %s against %s" % (c["code"], o["code"]))
            same = [x for x in bank["cases"] if x is not o and x["status"] == "Retired" and x["domain"] == o["domain"]
                    and x["specialty"] == o["specialty"]]
            if c["cat"] == "device":
                ok(any(x["cat"] == "decoy" and x["reviewed"] > o["reviewed"] for x in same),
                   "ask A: %s's old record is its specialty's last-reviewed retired record" % c["code"])
        if c["status"] == "Retired":
            ok(c["reviewed"] < K.BANK_MIGRATION, "retired record %s reviewed after the cut-over" % c["code"])
        ok(c["specialty"] in W.SPECIALTY_OF[c["title"]] and c["resources"] in W.resources_of(c["title"]),
           "specialty or resources of %s" % c["code"])
    for d in K.DOMAINS:
        first = [c for c in bank["cases"] if c["domain"] == d and c["cat"] == "recreated_clean"]
        tw = [c for c in bank["cases"] if c["domain"] == d and c["cat"] == "retired_twin_old"][0]
        ok(any((c["specialty"], c["resources"]) == (tw["specialty"], tw["resources"]) for c in first),
           "ask A: the case retired after its 2025 sitting shares no re-created record's specialty in %s" % d)
    # legacy codes run with the order the cases were written; the new bank's numbers are not evenly spaced
    for d in K.DOMAINS:
        leg = sorted([c for c in bank["cases"] if c["domain"] == d and not c["code"].startswith("CV-")
                      and c["cat"] != "set_2026"], key=lambda c: c["created"])
        ok([c["code"] for c in leg] == sorted(c["code"] for c in leg), "legacy codes out of order in %s" % d)
        cv = sorted(int(c["code"][-4:]) for c in bank["cases"] if c["domain"] == d and c["code"].startswith("CV-25"))
        ok(len({b - a for a, b in zip(cv, cv[1:])}) > 2, "CV-25 codes evenly spaced in %s" % d)
    e = w["examiners"]
    resp = {x["staff"]: x for x in e["responses"]}
    for site in [s[0] for s in K.SITES27]:
        for s in [x[0] for x in K.SESSIONS]:
            n_dev = sum(1 for st, si in e["device"].items() if si == site and resp[st]["ticks"][s])
            ok(n_dev >= 2, "ask B device thin at %s %s" % (site, s))
            n_ns = sum(1 for st, (si, _) in e["namesake"].items() if si == site and resp[st]["ticks"][s])
            ok(n_ns >= 1, "ask B namesake device misses %s %s" % (site, s))
    # each namesake: an active GP trainer, lapsed before the window, whose name one newly appointed hospital or
    # Fennabeg trainee shares, that trainee's attendance inside the window; no other trainee shares a register name
    people = {p["staff"]: p for p in e["people"]}
    reg_names = {}
    for p in e["people"]:
        reg_names.setdefault(V.norm_name("%s %s" % (p["fore"], p["sur"])), []).append(p["staff"])
    shared = {}
    for tr in e["trainees"]:
        hit = reg_names.get(V.norm_name("%s %s" % tr["name"]), [])
        if hit:
            shared.setdefault(hit[0], []).append(tr)
    ok(set(shared) == set(e["namesake"]), "ask B: trainees sharing register names %s" % sorted(shared))
    # whose number a sign-in row carries: H only for the hospital's own staff at its sessions, F only for Fennabeg's
    # at theirs; everyone else, GP trainers included, signs in there under a University number
    with open(os.path.join(t, K.FILES["training"]), newline="", encoding="utf-8") as f:
        log = list(csv.DictReader(f))
    alt_of = {p["alt"][0]: p for p in e["people"] if "alt" in p}
    trainee_nos = {tr["no"] for tr in e["trainees"]}
    ok(not any(p["base"] == "Callowfield" and "alt" in p for p in e["people"]), "a University academic holds an H "
       "or F number")
    for r in log:
        no = r["staff_no"]
        if no[0] in "HF":
            want = {"H": ("CUH", W.VENUES[1]), "F": ("Fennabeg", W.VENUES[2])}[no[0]]
            ok(r["venue"] == want[1] and (no in trainee_nos or alt_of[no]["base"] == want[0]),
               "sign-in row %s %s" % (no, r["venue"]))
    gp_e = [r for r in log if r["staff_no"][0] == "E" and r["venue"] != W.VENUES[0]
            and r["staff_no"] in people and people[r["staff_no"]]["base"] == "General practice"]
    ok(len(gp_e) >= 3, "GP trainers' rows at the hospital's or Fennabeg's sessions (the write-up's step 8)")
    for st, (site, kind) in e["namesake"].items():
        p = people[st]
        ok(site != {"CUH": "CUH", "Fennabeg": "FCS"}[kind], "ask B namesake %s offers its trainee's site" % st)
        ok(p["grade"] == "GP Trainer" and p["base"] == "General practice" and p["status"] == "Active"
           and p["last_attended"] < K.TRAINED_FROM, "ask B namesake %s eligible or not a GP trainer" % st)
        trs = shared[st]
        ok(len(trs) == 1 and trs[0]["no"][0] == W.HOME_VENUE[kind][1] and trs[0]["att"] == "Attended"
           and trs[0]["session"]["date"] >= K.TRAINED_FROM, "ask B namesake trainee for %s" % st)
    # the cracker and the mirror miss every ask figure; every route the devices aim at misses nearly all
    res = CR.run(t, quiet=True)
    ok(res["routes"][CR.CRACKER] == [], "the cracker hits an ask figure")
    ok(res["pair"] <= 30 and res["leak"] < 5, "pair ceiling or leakage")
    for name, hits in res["routes"].items():
        ok(len(hits) <= 2, "route %s keeps %d ask figures" % (name, len(hits)))
    return res


def gates(t, golden):
    files = sorted(os.listdir(t))
    ok(len(files) >= 10, "fewer than ten files")
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "fewer than three formats")
    with open(os.path.join(t, K.FILES["marks"]), encoding="utf-8") as f:
        ok(sum(1 for _ in f) - 1 >= 25000, "no file of 25,000 rows")
    meta = json.load(open(os.path.join(os.path.dirname(t), "metadata.json")))
    dis = [d.split("/", 1)[1] for d in meta["distractor_files"]]
    ok(len(dis) >= 2 and all(d in files for d in dis) and sorted(dis) == sorted(meta["distractor_notes"]),
       "distractors")
    ok(sorted(meta["call_files"] + meta["ask_files"] + dis + [K.FILES["contents"]]) == files, "file roles")
    ok(sorted(os.listdir(golden)) == ["osce2027_reliability_chart.png", "osce2027_station_plan.xlsx"], "goldens")
    # no em or en dash in any text the pack carries
    for f in files:
        if f.endswith((".csv", ".txt")):
            s = open(os.path.join(t, f), encoding="utf-8").read()
            ok("—" not in s and "–" not in s, "dash in %s" % f)
    # dates: nothing after the pack's date except the 2027 plan's own dates and booked training sessions
    with open(os.path.join(t, K.FILES["training"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d = dt.date.fromisoformat(r["session_date"])
            ok(d <= K.PACK_DATE or r["outcome"] == "Booked", "training row past the pack date not a booking")
    with open(os.path.join(t, K.FILES["availability"]), encoding="utf-8") as f:
        rd = csv.reader(f)
        next(rd)
        for r in rd:
            ok(K.FORM_OPENED < dt.datetime.strptime(r[0], "%d/%m/%Y %H:%M:%S") <= K.FORM_CLOSED,
               "a response outside the form's dates")
    # register names unique without accents or punctuation (the name match is determinate)
    reg = V.rows_xlsx(os.path.join(t, K.FILES["register"]))
    names = [V.norm_name("%s %s" % (r["Forename"], r["Surname"])) for r in reg]
    ok(len(names) == len(set(names)), "register names not unique once normalised")
    ok(not any(p in " ".join("%s %s" % (r["Forename"], r["Surname"]) for r in reg) for p in K.PEOPLE.values()),
       "a persona on the register")


def run(t, w):
    golden = os.path.join(os.path.dirname(t), "golden")
    w["fig"] = json.load(open(os.path.join(HERE, "figures.json")))
    L = three_rules(w)
    r1_r2_r3c(t, w)
    ladder(L)
    forks(w)
    c = V.call(t)
    ok(c["stations"] == w["fig"]["call"]["stations"] and c["candidates"] == 84, "the pack's call against truth")
    for n in K.SETTINGS:
        # the bundle-only reader of the pack agrees with the generator's truth to the last digit, not only the print
        ok(abs(c["reliability"][n] - L["golden"]["at"][n]) < 1e-12 and
           "%.2f" % c["reliability"][n] == w["fig"]["reliability"][str(n)], "the pack's reliability at %d" % n)
    separation(t, w)
    res = asks(t, w)
    gates(t, golden)
    realism(t)
    print("checks: %d assertions passed; pair ceiling %.1f, mirror leakage %.1f" % (N[0], res["pair"], res["leak"]))
