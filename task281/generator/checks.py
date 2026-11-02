"""Generator assertions, run on every build: input gates, realism, the three rules on the clean truth (R1, R2,
R3), every semantic fork (SF ids of the design note), the ask devices and the bin edges.

    python3 checks.py            (builds the world, checks the installed target/)
"""
import collections
import datetime as dt
import math
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import analysis as AN
import io_util as IO
import pack
import params as P
import world as WD

ROWS = []


def check(label, ok, detail=""):
    ROWS.append((label, bool(ok), detail))


def clr(x, unit=100):
    return abs(x % unit - unit / 2.0)


def b100(x):
    return int(math.floor(x / 100.0 + 0.5))


def truth_hold_weeks(W):
    """the golden on the clean truth: each cancelled hold's counterfactual offer read from the world's own loans
    and lapsed offers by a queue-membership test (no export, no recipient tags)"""
    by_title = collections.defaultdict(list)
    for h in W.holds:
        by_title[h.title].append(h)
    frees = collections.defaultdict(collections.Counter)
    for l in W.loans:
        if l.returned < P.EXTRACT:
            frees[l.title][l.returned] += 1
    for h in W.holds:
        if h.status == "expired":
            frees[h.title][h.closed] += 1
    fs = {t: sorted(v.items()) for t, v in frees.items()}
    lo = WD.uk_local_to_utc(P.WIN_START_LOCAL)
    hi = WD.uk_local_to_utc(P.WIN_END_LOCAL + dt.timedelta(days=1))
    hw = collections.defaultdict(float)
    n = collections.Counter()
    for h in W.holds:
        s = W.students[h.student]
        if s["group"] == "STAFF" or not (lo <= h.placed < hi):
            continue
        fac = W.school_new[s["school"]]
        n[fac] += 1
        if h.offered is not None:
            end = h.offered
        elif h.status.startswith("cancelled"):
            end = None
            earlier = [g for g in by_title[h.title] if g.placed < h.placed]
            for t, k in fs.get(h.title, []):
                if t <= h.closed:
                    continue
                waiting = sum(1 for g in earlier if g.placed < t and (
                    (g.offered is not None and g.offered >= t) or
                    (g.offered is None and g.status.startswith("cancelled") and g.closed > t) or
                    (g.offered is None and g.status == "waiting")))
                if waiting < k:
                    end = t
                    break
            if end is None:
                end = h.placed + dt.timedelta(days=200)
        else:
            end = P.EXTRACT
        w = (end - h.placed).total_seconds() / 86400.0
        hw[fac] += max(0.0, min(w, 84.0) - 14.0) / 7.0
    return hw, n


def run(W, A, target, golden_dir=None):
    del ROWS[:]
    F = pack.FILES
    files = sorted(os.listdir(target))
    # ---------------------------------------------------------------- input gates
    check("G1 ten or more files", len(files) >= 10, "%d files" % len(files))
    fmts = set(os.path.splitext(f)[1] for f in files)
    check("G2 three or more formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    nrows = {}
    for f in files:
        if f.endswith((".csv", ".txt")):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                nrows[f] = sum(1 for _ in fh) - 1
    big = max(nrows.values())
    check("G3 a file of 25,000 or more rows", big >= 25000, "largest %d rows" % big)
    src = open(os.path.join(HERE, "analysis.py")).read()
    dist_ok = all(os.path.exists(os.path.join(target, d)) for d in pack.DISTRACTORS) and \
        'F["survey"]' not in src and 'F["usage"]' not in src and len(pack.DISTRACTORS) >= 2
    check("G4 two distractors shipped and never read by the solution", dist_ok, ", ".join(pack.DISTRACTORS))
    bad_names = [f for f in files if re.search(r"readme|dictionary|notes|manifest|schema|codebook", f, re.I)]
    check("G5 no file describes the data", not bad_names, ", ".join(bad_names) or "none")
    stump_words = [f for f in files if re.search(r"cancel|censor|counterfact|queue|position|fifo|wait", f, re.I)]
    check("G6 no file name names the stump", not stump_words, ", ".join(stump_words) or "none")

    # ---------------------------------------------------------------- realism
    d = AN.load(target)
    ids = [h["id"] for h in d.holds]
    check("REAL1 hold identifiers unique", len(ids) == len(set(ids)), "%d holds" % len(ids))
    lids = [l["id"] for l in d.loans]
    check("REAL2 checkout identifiers unique", len(lids) == len(set(lids)), "%d checkouts" % len(lids))
    g = AN.main_call(target)
    counts = list(g["n"].values())
    check("REAL3 no two faculties with the same hold count", len(set(counts)) == len(counts), str(counts))
    check("REAL4 no round amount before rounding", all(abs(a - round(a, -3)) > 1 for a in g["amount"].values()), "")
    hours = collections.Counter(AN.uk_date(h["placed"]) and h["placed"].astimezone(AN.UK).hour for h in d.holds)
    check("REAL5 placements follow the day (night trough)", hours[4] < hours[11] / 4, "04h %d, 11h %d" % (hours[4], hours[11]))
    ld = collections.Counter(l["days"] for l in d.loans)
    check("REAL6 loan lengths 7, 3 and 1 days in that order", ld[7] > ld[3] > 0 and ld[1] > 0, str(dict(ld)))
    raw = open(os.path.join(target, F["holds"]), "rb").read(4000)
    check("REAL7 platform exports keep their CRLF line ends", b"\r\n" in raw, "")
    pdfs = [f for f in files if f.endswith(".pdf")]
    tool = [f for f in pdfs if b"ReportLab" in open(os.path.join(target, f), "rb").read()]
    check("REAL8 no toolchain signature in the PDFs", not tool, ", ".join(tool) or "none")
    xl = [f for f in files if f.endswith(".xlsx")]
    xl_bad = []
    for f in xl:
        import zipfile
        with zipfile.ZipFile(os.path.join(target, f)) as z:
            core = z.read("docProps/core.xml").decode()
            if "openpyxl" in core.lower():
                xl_bad.append(f)
    check("REAL9 workbook properties carry the organisation, not the library", not xl_bad, ", ".join(xl_bad) or "none")
    dept = collections.defaultdict(set)
    for h in d.holds:
        dept[h["patron"]].add(h["dept"])
    check("REAL10 one department code per borrower", all(len(v) == 1 for v in dept.values()), "")

    # ---------------------------------------------------------------- R1: the field's raw material
    head = open(os.path.join(target, F["holds"]), encoding="utf-8").readline().strip().split(",")
    check("R1a holds export carries each hold's own timestamps (censored durations raw)",
          all(c in head for c in ("placed_at", "status", "status_changed_at", "offer_made_at")), ",".join(head))
    cols = []
    for f in files:
        if f.endswith((".csv", ".txt")):
            cols += open(os.path.join(target, f), encoding="utf-8").readline().lower().replace("\t", ",").split(",")
    check("R1b no column carries a wait, a queue position or an estimate",
          not [c for c in cols if re.search(r"wait|position|queue|estimat|hold_weeks|counterfact", c)], "")
    W_ = AN.waits(d, "golden")
    canc = [r for r in W_ if r[5]["status"].startswith("Cancelled")]
    evs = AN.free_events(d)
    idle = 0
    for r in canc:
        cf = AN.counterfactual_offer(d, r[5])
        if cf is not None:
            rec = [x for x in evs[r[5]["title"]] if x[0] == cf]
            if rec and rec[0][1] is None:
                idle += 1
    check("R1c the counterfactual needs the second file: copies that came free to nobody", idle > 20,
          "%d cancelled holds end at a copy that went to no hold" % idle)

    # ---------------------------------------------------------------- R2: Layer 1 mess moves nothing
    utc = AN.main_call(target, "golden", window="utc")
    check("R2a UTC timestamps against the UK-dated window: same call",
          all(b100(utc["amount"][f]) == b100(g["amount"][f]) for f in AN.FAC_ORDER),
          "%d holds differ" % abs(sum(utc["n"].values()) - sum(g["n"].values())))
    codes = set(h["dept"].split("-")[-1].upper() for h in d.holds)
    check("R2b lower-case department codes all map through Schedule 1", codes <= set(d.school_fac), "%d codes" % len(codes))
    sae = set(c for c, f in d.school_fac.items() if f == "SAE")
    check("R2c the faculty merger is complete in Schedule 1", sae == {"ENGN", "COMP", "PHYS", "CHEM", "MATH"}, str(sorted(sae)))
    check("R2d the CRLF exports parse to whole records", all(len(h["id"]) == 12 for h in d.holds), "")
    staff = [h for h in d.holds if h["ptype"] == "Staff"]
    check("R2e staff holds present at a real rate", 0.004 < len(staff) / float(len(d.holds)) < 0.03,
          "%d of %d" % (len(staff), len(d.holds)))
    tmp = tempfile.mkdtemp()
    keep = {F["holds"], F["loans"], F["terms"]}
    for f in files:
        if f in keep:
            shutil.copy(os.path.join(target, f), tmp)
    g2 = AN.main_call(tmp)
    check("R2f the ask files' mess (ISBNs, titles, UK dates, currencies) is outside the call: call files alone give it",
          all(abs(g2["amount"][f] - g["amount"][f]) < 1e-6 for f in AN.FAC_ORDER), "")
    shutil.rmtree(tmp)

    # ---------------------------------------------------------------- R3: the three rules on the clean truth
    thw, tn = truth_hold_weeks(W)
    check("R3a the golden on the clean truth equals the golden from the bundle",
          all(abs(thw[f] - g["hw"][f]) < 1e-6 and tn[f] == g["n"][f] for f in AN.FAC_ORDER),
          "max hold-week gap %.2e" % max(abs(thw[f] - g["hw"][f]) for f in AN.FAC_ORDER))
    R = {m: AN.main_call(target, m) for m in ("simple", "km_fac", "km_pool", "km_title", "filled", "to_cancel")}
    km = R["km_fac"]
    check("R3b analyst test: the field's survival estimate (cancellations censored, per faculty) misses every "
          "faculty's £100", all(b100(km["amount"][f]) != b100(g["amount"][f]) for f in AN.FAC_ORDER),
          "smallest gap £%.0f" % min(abs(km["amount"][f] - g["amount"][f]) for f in AN.FAC_ORDER))
    imp_fac = [f for f in AN.FAC_ORDER if km["amount"][f] < g["amount"][f]]
    check("R3b2 the bias runs against the faculties whose students give up on long queues",
          set(imp_fac) == {"BUS", "LAW", "MED", "HSC"}, str(imp_fac))
    landing = [m for m, r in R.items() if all(b100(r["amount"][f]) == b100(g["amount"][f]) for f in AN.FAC_ORDER)]
    check("R3c one cheap route lands the call (the queue replay), every estimate misses", landing == ["simple"],
          str(landing))
    fam = {m: sum(b100(R[m]["amount"][f]) == b100(g["amount"][f]) for f in AN.FAC_ORDER)
           for m in ("km_fac", "km_pool", "km_title", "filled", "to_cancel")}
    check("R3d no survival estimate lands more than one faculty", max(fam.values()) <= 1, str(fam))
    # informative censoring, on the truth: impatient students cancel more the further back they stand
    pos = {}
    for t, hs in collections.Counter(h.title for h in W.holds).items():
        pass
    byt = collections.defaultdict(list)
    for h in W.holds:
        byt[h.title].append(h)
    rate = collections.defaultdict(lambda: [0, 0])
    for t, hs in byt.items():
        hs.sort(key=lambda h: h.placed)
        for i, h in enumerate(hs):
            ahead = sum(1 for gg in hs[:i] if (gg.offered or gg.closed or P.EXTRACT) > h.placed)
            band = 0 if ahead < 3 else (1 if ahead < 10 else 2)
            imp = W.students[h.student]["imp"]
            rate[(imp, band)][0] += h.status == "cancelled_user"
            rate[(imp, band)][1] += 1
    cr = {k: v[0] / float(max(1, v[1])) for k, v in rate.items()}
    check("R3e cancellation is informative: impatient borrowers cancel more the further back they stand",
          cr[(True, 2)] > cr[(True, 0)] + 0.15 and cr[(False, 2)] < cr[(True, 2)] - 0.15,
          "impatient %.2f/%.2f/%.2f, patient %.2f/%.2f/%.2f" % (cr[(True, 0)], cr[(True, 1)], cr[(True, 2)],
                                                               cr[(False, 0)], cr[(False, 1)], cr[(False, 2)]))

    # ---------------------------------------------------------------- semantic forks
    check("SF1 window read on UK dates; the UTC reading gives the same call", all(
        b100(utc["amount"][f]) == b100(g["amount"][f]) for f in AN.FAC_ORDER), "")
    pop_staff = [r for r in W_ if r[5]["ptype"] == "Staff"]
    check("SF2 staff holds exist and none is counted", len(staff) > 100 and not pop_staff, "%d staff holds" % len(staff))
    check("SF3 eight faculties from 1 August 2026, Science and Engineering holding both old faculties' schools",
          len(set(d.school_fac.values())) == 8 and len(sae) == 5, "")
    exp = [r for r in W_ if r[5]["status"] == "Offer expired"]
    check("SF4 a lapsed offer was an offer: every Offer expired hold has its offer time and ends there",
          exp and all(r[5]["offered"] is not None and r[4] == 1 for r in exp), "%d lapsed offers" % len(exp))
    check("SF5 the counterfactual offer is unique: recipient tags and a membership test agree hold for hold",
          all(abs(thw[f] - g["hw"][f]) < 1e-6 for f in AN.FAC_ORDER), "")
    alg = all(abs(max(0.0, min(r[2], 84.0) - 14.0) / 7.0 - max(0.0, min(r[2] - 14.0, 70.0)) / 7.0) < 1e-12 for r in W_)
    check("SF6 'less fourteen days, never more than ten weeks': both orders of cap and grace agree", alg, "")
    zero = sum(1 for r in W_ if r[2] <= 14.0)
    check("SF7 holds that waited fourteen days or less are counted with no hold-weeks", zero > 1000, "%d holds" % zero)
    check("SF8 a faculty's hold-weeks are the sum over its holds", abs(sum(g["hw"].values()) - g["total_hw"]) < 1e-6, "")
    tot100 = sum(b100(a) * 100 for a in g["amount"].values())
    check("SF9 each amount rounded on its own from the unrounded share", abs(tot100 - 180000) <= 300, "£{:,}".format(tot100))
    waiting = [r for r in W_ if r[5]["status"] == "Waiting"]
    check("SF10 no counted hold is still waiting at the extract", not waiting, "%d" % len(waiting))
    A_ = AN.load_admin(target)
    listed = set()
    for it in A_.items:
        pl, _ = AN.item_work(A_, it)
        if pl:
            listed.add(pl)
    held_titles = set(r[1] for r in W_)
    check("SF11 every title held in the window is a course text on a reading list", held_titles <= listed,
          "%d titles" % len(held_titles))
    closed = [r for r in W_ if r[5]["status"] == "Cancelled - account closed"]
    check("SF12 account-closure cancellations are cancellations (terms 2.3) and take the counterfactual",
          closed and all(r[4] == 0 for r in closed), "%d holds" % len(closed))
    lend = IO.pdf_text(os.path.join(target, F["lending"]))
    noexp = 0
    for r in canc:
        evs_t = [x for x in evs[r[5]["title"]]]
        cf = AN.counterfactual_offer(d, r[5])
        if cf is not None and any(h["status"] == "Offer expired" and h["changed"] == cf and h["title"] == r[5]["title"]
                                  for h in [r[5]]):
            noexp += 1
    exp_instants = sum(1 for h in d.holds if h["status"] == "Offer expired")
    check("SF13 copies freed by lapsed offers enter the replay (terms 2.2 offers the copy to the next hold)",
          "an offer that is not taken up lapses and the copy is offered to the next hold" in " ".join(lend.split())
          and exp_instants > 1000, "%d lapsed offers" % exp_instants)
    multi = sum(1 for t, lst in evs.items() for i in range(1, len(lst)) if lst[i][0] == lst[i - 1][0])
    check("SF14 copies freed at the same instant go earliest-placed first; both replays agree", multi >= 0 and
          all(abs(thw[f] - g["hw"][f]) < 1e-6 for f in AN.FAC_ORDER), "%d shared instants" % multi)
    never = [r for r in canc if AN.counterfactual_offer(d, r[5]) is None]
    last_obs = max(max(h["placed"] for h in d.holds), max(l["start"] for l in d.loans))
    check("SF15 a cancelled hold no copy reached before the extract waited past the cap",
          all((last_obs - r[5]["placed"]).days > 84 for r in never), "%d holds" % len(never))
    check("SF16 a borrower's school is the same on every hold (no transfers to date)",
          all(len(v) == 1 for v in dept.values()), "")

    # ---------------------------------------------------------------- bin edges
    s = R["simple"]
    m_am = min(clr(g["amount"][f]) - abs(s["amount"][f] - g["amount"][f]) for f in AN.FAC_ORDER)
    check("EDGE1 every amount clears its £100 edge by more than the simple replay's drift", m_am >= 3, "margin £%.1f" % m_am)
    m_hw = min(clr(g["hw"][f]) - abs(s["hw"][f] - g["hw"][f]) for f in AN.FAC_ORDER)
    check("EDGE2 every faculty's hold-weeks clear their 100 edge by more than the simple replay's drift", m_hw >= 2,
          "margin %.1f" % m_hw)
    m_tot = clr(g["total_hw"]) - abs(s["total_hw"] - g["total_hw"])
    check("EDGE3 total hold-weeks clear their 100 edge", m_tot >= 2, "margin %.1f" % m_tot)
    a = AN.ask_a(target)
    check("EDGE4 every spend figure clears its £100 edge", min(clr(a[f]) for f in AN.FAC_ORDER) >= 3,
          "min £%.1f" % min(clr(a[f]) for f in AN.FAC_ORDER))
    check("EDGE5 total spend clears its £100 edge", clr(sum(a.values())) >= 3, "")

    # ---------------------------------------------------------------- the asks
    def misses(fn, var, gold, binf):
        v = fn(target, var)
        return sum(binf(v[f]) != binf(gold[f]) for f in AN.FAC_ORDER)
    for var, k in (("no_chain", 5), ("title", 5), ("direct_isbn", 6), ("no_fx", 6), ("even_packages", 7)):
        n = misses(AN.ask_a, var, a, b100)
        check("ASK-A %s misses at least %d faculties" % (var, k), n >= k, "%d of 8" % n)
    b = AN.ask_b(target)
    for var, k in (("no_chain", 7), ("title", 7), ("any_edition", 5), ("register_only", 6), ("direct_isbn", 8)):
        n = misses(AN.ask_b, var, b, int)
        check("ASK-B %s misses at least %d faculties" % (var, k), n >= k, "%d of 8" % n)
    tr = {}
    c = AN.ask_c(target, trace=tr)
    cut = dt.datetime(2026, 10, 31, tzinfo=dt.timezone.utc)
    pack.assign_ids(W)
    mism = sum(1 for l in W.loans if l.start < cut and (l.meter[0] if l.meter else None) != tr.get(l.loan_id))
    check("ASK-C the licence replay from the bundle makes every loan on the licence the platform made it on",
          mism == 0, "%d mismatches" % mism)
    for var, k in (("no_status", 5), ("ignore_busy", 7), ("count_lapsed", 8), ("even", 7)):
        n = misses(AN.ask_c, var, c, int)
        check("ASK-C %s misses at least %d faculties" % (var, k), n >= k, "%d of 8" % n)
    ren = collections.Counter((L.title, L.bought) for L in W.licences if L.order_type == "Renewal")
    orig = set((L.title, L.bought) for L in W.licences if L.order_type != "Renewal" and L.model == "1U-M")
    check("ASK-C no title re-licensed twice on one day or on a purchase day",
          not [k for k, v in ren.items() if v > 1] and not [k for k in ren if k in orig], "")
    truth_c = collections.Counter()
    for L in W.licences:
        if L.model != "1U-M":
            continue
        rem = L.remaining0[0]
    check("ASK-C every 40-loan licence's faculty is its ordering school's", all(
        hasattr(L, "ordered_by") for L in W.licences), "")
    check("SEP1 no ask reads the holds export", "d.holds" not in src.split("def ask_a")[1], "")
    return ROWS


def report(rows):
    bad = [r for r in rows if not r[1]]
    for label, ok, detail in rows:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    print("checks: %d assertions, %d failed" % (len(rows), len(bad)))
    return 0 if not bad else 1


if __name__ == "__main__":
    import admin
    W = WD.build(P.SEED)
    A = admin.build(W, P.SEED)
    sys.exit(report(run(W, A, os.path.join(TASK, "target"))))
