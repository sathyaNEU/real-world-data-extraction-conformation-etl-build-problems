"""The generator's assertions on the cut pack (task255/target) and the clean truth: the three-rules block (R1 to R3c),
the ladder, every semantic fork (SF1 to SF21), mess neutrality, the asks, the input gates, the realism sweep and the
leak sweep. Exit 1 on any failure."""
import collections
import datetime as dt
import json
import os
import random
import re
import shutil
import statistics
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import analysis as AN  # noqa: E402
import asks_world as AW  # noqa: E402
import io_util as IO  # noqa: E402
import pack  # noqa: E402
import params as P  # noqa: E402
import world  # noqa: E402

T = os.path.join(TASK_DIR, "target")
GOLDEN = ["041219", "041236", "041248", "041275", "041307", "041322"]
RUNG_DDD = ["041236", "041263"]
RUNG_ONE_A_DAY = ["041219", "041224", "041236", "041248", "041251", "041275", "041282", "041322", "041334"]
RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


def truth_status(pt, rate):
    stock_end = 0.0
    for d, k, pk in pt.runs:
        x = (d - pt.start).days
        if x >= P.HORIZON_DAYS:
            break
        if x - stock_end > P.GRACE_DAYS:
            return False
        stock_end = max(stock_end, x) + k * pk / rate
    return P.HORIZON_DAYS - stock_end <= P.GRACE_DAYS


def joins_from(status, cohort):
    n, k = collections.Counter(), collections.Counter()
    for pt in cohort:
        n[pt.practice] += 1
        k[pt.practice] += status[pt.id]
    return sorted(c for c in n if 100.0 * k[c] / n[c] < P.PROGRAMME_LINE), {c: 100.0 * k[c] / n[c] for c in n}


def with_rows(filter_fn, mutate=None):
    """The main call recomputed on the cut pack with some dispensing rows dropped or changed (mess neutrality)."""
    D = AN.load(T)
    saved = D["disp"]
    new = {}
    for pid, ds in saved.items():
        keep = [dict(d) for d in ds if filter_fn(d)]
        if mutate:
            keep = [mutate(d) for d in keep]
        keep.sort(key=lambda x: (x["date"], x["product"]))
        if keep:
            new[pid] = keep
    D["disp"] = new
    try:
        return AN.main_call(T)
    finally:
        D["disp"] = saved


def cu_hosp_drop(target):
    D = AN.load(target)
    saved = D["disp"]
    D["disp"] = {pid: [d for d in ds if d["prescriber"].isdigit()] for pid, ds in saved.items()}
    D["disp"] = {k: v for k, v in D["disp"].items() if v}
    try:
        return AN.continuing_users(target)
    finally:
        D["disp"] = saved


def main():
    W = world.build(P.SEED)
    A = AW.build(W, random.Random(P.SEED * 10 + 4))
    cohort = [pt for pt in W.patients if pt.cohort]
    G = AN.main_call(T)
    D = AN.load(T)
    meta = json.load(open(os.path.join(TASK_DIR, "metadata.json")))
    gstatus = {pt.id: world.truth_persistent(pt) for pt in cohort}
    tjoins, tshare = joins_from(gstatus, cohort)

    # ------------------------------------------------------------------ R1 to R3c, the three rules executed
    h, _ = IO.read_csv(os.path.join(T, pack.FILES["dispensings"]))
    hp, _ = IO.read_csv(os.path.join(T, pack.FILES["products"]))
    banned = re.compile(r"dose|ddd|days|supply|persist|duration", re.I)
    check("R1a raw material: dispensing rows carry dates, packs and product numbers, no dose or supply column",
          not [c for c in h + hp if banned.search(c)] and {"dispensing_date", "packs", "product_number"} <= set(h),
          ", ".join(h + hp))
    multi = sum(1 for pid, pr, st in G.cohort if len([d for d in D["disp"][pid] if d["date"] >= st]) >= 2)
    check("R1b the decisive computation reads each patient's own dispensings", multi > 0.6 * len(G.cohort),
          "%d of %d new users have two or more dispensings" % (multi, len(G.cohort)))
    names_ok = all(int(re.search(r"(\d+) mg", p.name).group(1)) == p.strength for p in W.products)
    check("R2.1 parallel imports under their own numbers: strength read from the name or the column agree", names_ok)
    M = with_rows(lambda d: d["date"] > P.OLD_SYSTEM_END)
    check("R2.2 old-system dates (day-month-year to June 2024) dropped: call and every share unchanged",
          M.joins == G.joins and M.share == G.share, "cohort %d" % len(M.cohort))

    def month_first(d):
        if d["date"] <= P.OLD_SYSTEM_END and d["date"].day <= 12:
            try:
                d["date"] = dt.date(d["date"].year, d["date"].day, d["date"].month)
            except ValueError:
                pass
        return d
    M = with_rows(lambda d: True, month_first)
    check("R2.2b old-system dates read month first: call and every share unchanged",
          M.joins == G.joins and M.share == G.share)
    M = with_rows(lambda d: d["prescriber"].isdigit())
    check("R2.3 hospital-prescribed dispensings dropped: call and every share unchanged",
          M.joins == G.joins and M.share == G.share)
    coh_ids = {pid for pid, pr, st in G.cohort}
    hosp_coh = sum(1 for pid in coh_ids for d in D["disp"][pid] if not d["prescriber"].isdigit())
    check("R2.3b no new user's dispensing carries a hospital prescriber (zero hazard rows in the call's population)",
          hosp_coh == 0, "%d rows" % hosp_coh)
    reads = set()
    for name in ("conversations", "statements", "agreement", "pharmacies"):
        reads.add(name)
    check("R2.4 late cancellations sit only in the pilot log: the call reads no pilot file",
          "conversations" not in AN.main_call.__code__.co_names)
    check("R2.5 statements drawn on each quarter's last day: ask A only (the call reads no statement)",
          "load_statements" not in AN.main_call.__code__.co_names)
    links = AN.person_links(T)
    check("R2.6 replaced personal numbers: no new user's pseudonym is joined to another (ask B only)",
          not (set(links) | set(links.values())) & coh_ids, "%d joined pseudonyms" % len(links))
    check("R2.7 list sizes per quarter: the call reads no list size", "listed" not in open(
        os.path.join(HERE, "analysis.py")).read().split("def main_call")[1].split("def load_conversations")[0])
    status_ddd = {pt.id: truth_status(pt, P.DDD_MG[pt.atc] / pt.strength) for pt in cohort}
    dj, _ = joins_from(status_ddd, cohort)
    check("R3a analyst test on the clean truth: the default path (WHO defined daily dose) files the wrong set",
          dj == RUNG_DDD and dj != tjoins, "files %s" % dj)
    check("R3b the decisive step alone: the default path with each patient's own dose files the golden",
          tjoins == GOLDEN, "files %s" % tjoins)
    s1, _ = joins_from({pt.id: truth_status(pt, 1.0) for pt in cohort}, cohort)
    check("R3b' the lower rung's single correction (one tablet a day instead of the DDD) stays wrong",
          s1 == RUNG_ONE_A_DAY and s1 != GOLDEN, "files %s" % s1)
    _, rows = IO.read_csv(os.path.join(T, pack.FILES["dispensings"]))
    dup = len(rows) - len({tuple(r) for r in rows})
    seqs = collections.Counter()
    for pid, ds in D["disp"].items():
        if len(ds) >= 6:
            seqs[tuple((d["date"], d["product"], d["tablets"]) for d in ds[:6])] += 1
    check("R3c no plant: no duplicated dispensing row and no copied refill sequence",
          dup == 0 and max(seqs.values()) == 1, "%d duplicates" % dup)
    docs = " ".join(IO.pdf_text(os.path.join(T, pack.FILES[k])) for k in ("programme", "agreement"))
    check("R3c' no plant: no memo, draft or stakeholder figure; the documents state no dose, rate or method",
          not re.search(r"defined daily|DDD|refill|rhythm|a day|per day|replaced|pseudonym|not cancelled by", docs),
          "")

    # ------------------------------------------------------------------ the ladder on the cut pack
    check("L1 golden on the cut pack equals the clean truth for every practice",
          all(abs(G.share[c] - tshare[c]) < 1e-9 for c in tshare) and G.joins == GOLDEN)
    for rule, want in (("ddd", RUNG_DDD), ("one_a_day", RUNG_ONE_A_DAY), ("product_rate", RUNG_ONE_A_DAY)):
        M = AN.main_call(T, rule)
        check("L2 rung %s on the cut pack files its stated set" % rule, M.joins == want, "%s" % M.joins)
    margin = min(abs(v - P.PROGRAMME_LINE) for v in G.share.values())
    check("L3 every practice 5 points or more from the line", margin >= 5.0, "%.2f" % margin)
    near = min((v, c) for c, v in G.share.items() if c not in G.joins)
    check("L4 nearest practice above the line", near[1] == "041358" and round(near[0]) == 65, "%s %.2f" % (near[1], near[0]))
    check("L5 every practice has 50 or more new users", min(G.n.values()) >= 50, "%d" % min(G.n.values()))
    ddd_escape = [c for c in GOLDEN if c not in RUNG_DDD]
    check("L6 dominance: the DDD rung lets five joining practices off and takes one in",
          len(ddd_escape) == 5 and [c for c in RUNG_DDD if c not in GOLDEN] == ["041263"])

    # ------------------------------------------------------------------ semantic forks
    def cohort_with(lookback=None, any_earlier=False):
        out = set()
        for pid, ds in D["disp"].items():
            fs = [d for d in ds if AN.WINDOW[0] <= d["date"] <= AN.WINDOW[1]]
            if not fs:
                continue
            f = fs[0]
            prior = [d for d in ds if d["date"] < f["date"]]
            if any_earlier and prior:
                continue
            if lookback and any((f["date"] - d["date"]).days <= lookback for d in prior):
                continue
            if f["prescriber"] in D["practices"]:
                out.add(pid)
        return out
    base = {pid for pid, pr, st in G.cohort}
    check("SF1 the window's ends inclusive or exclusive: no first dispensing on 1 July or 31 December changes the set",
          True, "first dispensings on the window's ends: %d" % sum(1 for pid, pr, st in G.cohort
                                                                   if st in (AN.WINDOW[0], AN.WINDOW[1])))
    check("SF2 lookback of 365 or 366 days, or no earlier dispensing at all: the same new users",
          cohort_with(365) == base and cohort_with(366) == base and cohort_with(any_earlier=True) == base)
    pr_last = all(D["disp"][pid][-1]["prescriber"] == pr for pid, pr, st in G.cohort)
    check("SF3 the practice of the first dispensing, the last or the most frequent: the same for every new user",
          pr_last and all(all(d["prescriber"] == pr for d in D["disp"][pid]) for pid, pr, st in G.cohort))
    worst_p, worst_n = 99.0, 99.0
    for pid, pr, st in G.cohort:
        ds = [d for d in D["disp"][pid] if d["date"] >= st]
        rate = AN.rate_overall(ds) or 1.0
        stock, gaps = 0.0, []
        for d in ds:
            x = (d["date"] - st).days
            if x >= AN.HORIZON:
                break
            gaps.append(x - stock)
            stock = max(stock, x) + d["tablets"] / rate
        gaps.append(AN.HORIZON - stock)
        if G.status[pid]:
            worst_p = min(worst_p, 30 - max(gaps))
        else:
            worst_n = min(worst_n, max(gaps) - 30)
    check("SF4 more than 30 days or 30 and more, whole or part days: every status 15 days or more from the edge",
          worst_p >= 15 and worst_n >= 15, "persistent %.1f, not persistent %.1f" % (worst_p, worst_n))
    check("SF5 the 365 days counted from day 0 or day 1, the last gap to day 364 or 365: no status within a day",
          worst_p >= 2 and worst_n >= 2)

    def no_carry(ds, start, rate):
        end = 0.0
        for d in ds:
            x = (d["date"] - start).days
            if x >= AN.HORIZON:
                break
            if x - end > AN.GRACE:
                return False
            end = x + d["tablets"] / rate
        return AN.HORIZON - end <= AN.GRACE
    flips = 0
    for pid, pr, st in G.cohort:
        ds = [d for d in D["disp"][pid] if d["date"] >= st]
        rate = AN.rate_overall(ds) or 1.0
        flips += no_carry(ds, st, rate) != G.status[pid]
    check("SF6 tablets in hand used first (3.2) against no carry-over: the filed reading; the alternative moves %d" % flips,
          True, "ruled out by programme 3.2")
    for rule in ("own_median", "own_recent", "own_horizon", "own_snapped"):
        M = AN.main_call(T, rule)
        f = sum(1 for pid in G.status if M.status[pid] != G.status[pid])
        check("SF7 the daily dose read as %s: no patient's status moves" % rule, f == 0, "%d flips" % f)
    singles = [pt for pt in cohort if len([r for r in pt.runs if (r[0] - pt.start).days < 365]) == 1]
    most = max(k * pk for pt in singles for d, k, pk in pt.runs[:1])
    check("SF8 a single dispensing runs out within the year at any dose from a third of a tablet a day",
          most / (1 / 3.0) < 335 and not any(gstatus[pt.id] for pt in singles), "largest single supply %d tablets" % most)
    check("SF9 the line on the unrounded or the rounded share: the same set", sorted(
        c for c, v in G.share.items() if round(v) < 60) == G.joins)
    edge = min(abs((v % 1) - 0.5) for v in G.share.values())
    check("SF10 half up or half to even: no share sits on a half per cent", edge > 0.01, "%.3f" % edge)
    di = h.index("dispensing_date")
    old = [r for r in rows if re.fullmatch(r"\d{2}-\d{2}-\d{4}", r[di])]
    check("SF11 the old-system dates read day first: days above 12 occur, so no other reading parses",
          bool(old) and any(int(r[di][:2]) > 12 for r in old) and
          all(dt.datetime.strptime(r[di], "%d-%m-%Y").date() <= P.OLD_SYSTEM_END for r in old),
          "%d old-format rows" % len(old))
    check("SF12 tablets are packs times the pack size of the product number (statin_products.csv)",
          all(p.pack in (30, 98, 100) for p in W.products))
    convs = AN.load_conversations(T)
    check("SF13 held in 2026: every conversation in the log is dated 2026", all(c["date"].year == 2026 for c in convs))
    check("SF14 a cancelled conversation: status aflyst exactly when a cancellation date is entered",
          all((c["status"] == "aflyst") == (c["cancelled"] is not None) for c in convs))
    pay = AN.pilot_payments(T)
    check("SF15 one rate per pharmacy: each statement over the conversations it covered gives the same whole krone",
          all(len(pay[c + ":rates"]) == 1 and pay[c + ":rates"][0] == int(pay[c + ":rates"][0])
              for c in AW.PILOT_RATE), "%s" % {c: pay[c + ":rates"] for c in AW.PILOT_RATE})
    check("SF16 no cancellation entered on a quarter's last day (the statement day)",
          not [c for c in convs if c["cancelled"] in AW.QUARTER_ENDS])
    stm = AN.load_statements(T)
    check("SF17 the statements' Danish amounts (1.234,00) parse to rate times conversations",
          len(stm) == 32 and all(s["amount"] % pay[s["pharmacy"] + ":rates"][0] == 0 for s in stm))
    l_tight = AN.person_links_inferred(T, same_line=True, same_practice=True, max_gap=120)
    l_loose = AN.person_links_inferred(T)
    check("SF18 one person under two pseudonyms: the CPR person table's previous number joins exactly the replaced "
          "numbers, and the record agrees (same birth date and sex, no overlap, same product line and practice)",
          links == l_tight == l_loose and set(links) == {r["new"] for r in A.replaced} and
          all(links[r["new"]] == r["old"] for r in A.replaced), "%d joins" % len(links))
    d26 = [d for ds in D["disp"].values() for d in ds if d["date"].year == 2026]
    check("SF19 quarters of 2026 by dispensing date: every 2026 row dated inside the year", all(
        dt.date(2026, 1, 1) <= d["date"] <= dt.date(2026, 12, 31) for d in d26))
    ties = 0
    for pid, ds in D["disp"].items():
        y = [d for d in ds if d["date"].year == 2026]
        if len(y) >= 2 and y[-1]["date"] == y[-2]["date"] and y[-1]["prescriber"] != y[-2]["prescriber"]:
            ties += 1
    check("SF20 the last dispensing of 2026 is one row: no person has two prescribers on their last day", ties == 0)
    last_h = 0
    for pid, ds in D["disp"].items():
        y = [d for d in ds if d["date"].year == 2026]
        if y and not y[-1]["prescriber"].isdigit():
            last_h += 1
    check("SF21 no person's last dispensing of 2026 prescribed at a hospital", last_h == 0)
    Mh = AN.continuing_users(T) == cu_hosp_drop(T)
    check("SF21b hospital-prescribed 2026 rows dropped moves ask B only (a hazard there, never the call)", not Mh)

    # ------------------------------------------------------------------ asks
    check("A1 entitlement equals the truth for every pharmacy and quarter",
          all(abs(pay[ph + ":q"][q] - A.payment_due_q[(ph, q)]) < 1e-6 for (ph, q) in A.payment_due_q) and
          all(abs(pay[ph] - A.payment_due[ph]) < 1e-6 for ph in A.payment_due))
    st = AN.pilot_payments(T, "statements")
    hn = AN.pilot_payments(T, "held_now")
    keep_st = sum(1 for (ph, q) in A.payment_due_q if abs(st[ph + ":q"][q] - pay[ph + ":q"][q]) < 0.5)
    keep_hn = sum(1 for (ph, q) in A.payment_due_q if abs(hn[ph + ":q"][q] - pay[ph + ":q"][q]) < 0.5)
    check("A2 device mass: the statement as the quarter's entitlement misses all 32 figures", keep_st == 0,
          "%d kept" % keep_st)
    check("A3 the rate read off a statement over the conversations standing now misses all 32 figures", keep_hn == 0,
          "%d kept" % keep_hn)
    late_q = collections.Counter()
    for cv in convs:
        if cv["cancelled"]:
            qe = AW.QUARTER_ENDS[(cv["date"].month - 1) // 3]
            if cv["cancelled"] > qe:
                late_q[(cv["pharmacy"], qe)] += 1
    check("A4 every pharmacy-quarter carries a conversation cancelled after its statement (no clean quarter to read "
          "a rate off)", len(late_q) == 32, "%d of 32, %d conversations" % (len(late_q), sum(late_q.values())))
    clawq = collections.Counter()
    for cv in convs:
        if cv["cancelled"] is None:
            clawq[(cv["pharmacy"], (cv["date"].month - 1) // 3 + 1)] += 1
        elif cv["cancelled"] > AW.QUARTER_ENDS[(cv["date"].month - 1) // 3]:
            clawq[(cv["pharmacy"], (cv["date"].month - 1) // 3 + 1)] += 1
            qc = min(4, (cv["cancelled"].month - 1) // 3 + 1) if cv["cancelled"].year == 2026 else 4
            clawq[(cv["pharmacy"], qc)] -= 1
    alt = sum(1 for (ph, q) in A.payment_due_q if pay[ph + ":rates"][0] * clawq[(ph, q)] == pay[ph + ":q"][q])
    check("SF22 a later cancellation counts against the quarter its conversation was held in, not the quarter it was "
          "entered (agreement 2.1, the ask's own wording); the booking reading moves figures", alt < 32,
          "%d of 32 agree under the booking reading" % alt)
    adopted = dt.date(2027, 1, 26)
    check("A5 one story: every cancellation in the pilot log is dated before the programme's adoption",
          max(cv["cancelled"] for cv in convs if cv["cancelled"]) < adopted)
    cu = AN.continuing_users(T)
    tc = collections.Counter()
    for pt in W.patients:
        if {(d.month - 1) // 3 for d, k, pk in pt.runs if d.year == 2026} == {0, 1, 2, 3}:
            tc[pt.practice] += 1
    check("B1 continuing users equal the truth for every practice", all(cu[c] == tc[c] for c in cu))
    cu0 = AN.continuing_users(T, "pseudonyms")
    check("B2 device mass: counting pseudonyms misses every practice", all(cu0[c] < cu[c] for c in cu),
          "%s" % {c: cu[c] - cu0[c] for c in cu})
    over = collections.Counter()
    by_key = collections.defaultdict(list)
    for pid in D["disp"]:
        by_key[D["meta"][pid]].append(pid)
    for key, pids in by_key.items():
        if len(pids) >= 2 and not set(pids) & (set(links) | set(links.values())):
            over[len(pids)] += 1
    cub = AN.continuing_users(T, "birth_sex")
    check("B3 people sharing a birth date and sex are not one person: joining them all is wrong",
          sum(over.values()) > 0 and cub != cu, "%d such groups; %d against %d" % (
              sum(over.values()), sum(cub.values()), sum(cu.values())))
    check("B4 the literal one-pseudonym reading is wrong and the linked reading unique",
          sum(cu0.values()) != sum(cu.values()) and links == l_tight,
          "pseudonyms %d, persons %d" % (sum(cu0.values()), sum(cu.values())))
    pubh, pubr = IO.read_xlsx(os.path.join(T, pack.FILES["published"]), "Statin use")
    series = collections.defaultdict(list)
    for town, qtr, v in pubr:
        series[town].append(v)
    steps = [abs(b / a - 1) for v in series.values() for a, b in zip(v, v[1:])]
    check("Z6 realism: the published town series move smoothly quarter to quarter", max(steps) < 0.06,
          "largest step %.1f per cent" % (100 * max(steps)))

    # ------------------------------------------------------------------ input gates, realism, distractors, leaks
    files = sorted(os.listdir(T))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    check("I1 ten or more files in three or more formats", len(files) >= 10 and len(fmts) >= 3, "%d files %s" % (
        len(files), sorted(fmts)))
    check("I2 one file of 25,000 rows or more", len(rows) >= 25000, "%d dispensing rows" % len(rows))
    check("I3 two or more distractors named in metadata.json", len(meta["distractor_files"]) >= 2 and all(
        f in files for f in meta["distractor_files"]), ", ".join(meta["distractor_files"]))
    tmp = tempfile.mkdtemp(prefix="t255_dx_")
    for f in files:
        if f not in meta["distractor_files"]:
            shutil.copy(os.path.join(T, f), tmp)
    AN._CACHE.pop(tmp, None)
    G2 = AN.main_call(tmp)
    check("I4 every distractor deleted: the call and every graded figure unchanged",
          G2.share == G.share and AN.pilot_payments(tmp) == pay and AN.continuing_users(tmp) == cu)
    shutil.rmtree(tmp)
    check("I5 every file carries source, date and license in metadata.json",
          all({"source", "date", "license"} <= set(f) for f in meta["files"]) and len(meta["files"]) == len(files))
    gaps = [(b["date"] - a["date"]).days for ds in D["disp"].values() for a, b in zip(ds, ds[1:])]
    check("Z1 realism: refill intervals spread (not one cycle)", statistics.pstdev(gaps) > 15 and len(set(gaps)) > 80,
          "sd %.1f, %d distinct" % (statistics.pstdev(gaps), len(set(gaps))))
    check("Z2 realism: no round or uniform counts (new users per practice all different from a round ten)",
          len(set(G.n.values())) >= 12 and sum(1 for v in G.n.values() if v % 10 == 0) <= 3)
    check("Z3 realism: statement amounts are not round hundreds", sum(1 for s in stm if s["amount"] % 100 == 0) <= 6)
    yrs = [int(m[1][:4]) for m in D["meta"].values()]
    check("Z4 realism: birth years 1932 to 1984", min(yrs) >= 1932 and max(yrs) <= 1984)
    check("Z5 realism: every product number is six digits and appears in the product list",
          all(re.fullmatch(r"\d{6}", r[h.index("product_number")]) and r[h.index("product_number")] in D["prods"]
              for r in rows))
    leak_words = re.compile(r"golden|stump|decoy|trap|own dose|daily dose they take is|refill rhythm", re.I)
    txt = " ".join(IO.pdf_text(os.path.join(T, f)) for f in files if f.endswith(".pdf"))
    check("X1 leak: no shipped document names the method or the author's intent", not leak_words.search(txt))
    check("X2 leak: no file name names the device or the trap", not re.search(r"dose|ddd_per|replace|cancel|late", " ".join(
        f for f in files if f not in ("atc_ddd_2026.xlsx", "regional_statin_use_ddd_2025.xlsx"))))
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    check("X3 figures.json carries every graded figure", all(p in figs for p in [int(round(v)) for v in G.share.values()])
          and all(int(round(v)) in figs for c in AW.PILOT_RATE for v in pay[c + ":q"].values())
          and all(v in figs for v in cu.values()))

    bad = [r for r in RESULTS if not r[1]]
    for label, ok, detail in RESULTS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    print("%d checks, %d failed" % (len(RESULTS), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
