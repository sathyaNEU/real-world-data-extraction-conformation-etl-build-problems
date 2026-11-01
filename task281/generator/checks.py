"""The generator's assertions on the installed pack (target/) and the clean truth (world.py).

    python3 task281/generator/checks.py          # exit 1 on any FAIL

Labels: G input gates, R1 to R3 the client's three rules executed on the clean truth, SF the design note's fork
table, M mess neutrality per Layer 1 item, S the realism sweep, E each graded figure's distance to its bin edge, L
the ladder's separation, W the pack against the world, C the ask ceiling."""
import csv
import datetime as dt
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import params as PR  # noqa: E402
import world as W  # noqa: E402
from deliver import rnd  # noqa: E402

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%-4s %-58s %s" % ("PASS" if ok else "FAIL", label, detail))


def edge(x, step=1.0):
    """Distance of x from the nearest rounding edge at the given step."""
    r = (x / step) % 1.0
    return abs(r - 0.5) * step


def picks_of(L, rung="golden"):
    return {c: L[rung][c][1] for c in L[rung]}


def main():
    P = A.Pack(TARGET)
    G = A.golden(P)
    L = G["ladder"]
    gold = G["picks"]
    files = sorted(os.listdir(TARGET))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))

    # ---------------------------------------------------------------- input gates
    check("G1 ten or more files", len(files) >= 10, "%d files" % len(files))
    fmts = {os.path.splitext(f)[1] for f in files}
    check("G2 three or more formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    big = max((sum(1 for _ in open(os.path.join(TARGET, f))) - 1, f) for f in files if f.endswith(".csv"))
    check("G3 a file of 25,000 rows or more", big[0] >= 25000, "%s %d rows" % (big[1], big[0]))
    dis = meta.get("distractor_files", [])
    check("G4 two or more distractors named in metadata.json, shipped", len(dis) >= 2 and all(d in files for d in dis),
          ", ".join(dis))
    bad_names = [f for f in files if re.search(r"readme|dictionary|notes|manifest|schema|codebook|about", f, re.I)]
    from openpyxl import load_workbook
    sheets = []
    for f in files:
        if f.endswith(".xlsx"):
            sheets += load_workbook(os.path.join(TARGET, f), read_only=True).sheetnames
    bad_sheets = [s for s in sheets if re.search(r"readme|notes|about|dictionary|how to", s, re.I)]
    check("G5 no file or sheet describes the data", not bad_names and not bad_sheets, "sheets: " + ", ".join(sheets))
    author = [f for f in files if re.search(r"test_|trap|decoy|stump|device|golden|distractor|answer", f, re.I)]
    check("G6 no file name carries the author's words", not author, ", ".join(author))
    meta_ok = all(set(v) >= {"source", "date", "license"} for v in meta["files"].values()) and set(meta["files"]) == set(files)
    check("G7 every file has source, date and license in metadata.json", meta_ok, "%d entries" % len(meta["files"]))

    # ---------------------------------------------------------------- the clean truth
    w = W.World(PR.SEED)
    W.make_ask_records(w)
    truth_by = Counter()
    clinic_model = Counter()
    for s in w.screens:
        truth_by[s["clinic"]] += 1
        clinic_model[(s["clinic"], s["model"])] += 1
    val = w.validation

    def tsens(rows, cut):
        rr = [v for v in rows if v["patient"]["ref"]]
        return sum(v["ungradable"] or v["score"] >= cut for v in rr) / len(rr)

    t_model = {m: {nm: tsens([v for v in val if v["model"] == m], cut) for nm, cut in PR.OPS} for m in ("NR-40", "NR-70")}
    t_pool = {nm: tsens(val, cut) for nm, cut in PR.OPS}

    def tpick(cells):
        for nm, cut in PR.OPS:
            if cells[nm] >= PR.FLOOR:
                return nm
        return None

    t_gold = {}
    for c in truth_by:
        sh = clinic_model[(c, "NR-40")] / truth_by[c]
        t_gold[c] = tpick({nm: sh * t_model["NR-40"][nm] + (1 - sh) * t_model["NR-70"][nm] for nm, _ in PR.OPS})
    t_pooled = {c: tpick(t_pool) for c in truth_by}

    # ---------------------------------------------------------------- the three rules
    vr = P.validation
    check("R1 the field's raw material ships: image-level reference grades and DR scores",
          len(vr) > 3000 and all(v["final_level"] for v in vr) and
          all(r["DR Score"] or r["Result"] == "Ungradable" for r in P.results),
          "%d validation images, %d screenings" % (len(vr), len(P.results)))
    sens_cols = []
    for f in files:
        if f.endswith(".csv"):
            head = open(os.path.join(TARGET, f)).readline().lower()
            if "sensitiv" in head or "specific" in head:
                sens_cols.append(f)
    for f in files:
        if f.endswith(".xlsx"):
            wb = load_workbook(os.path.join(TARGET, f), read_only=True)
            for ws in wb:
                for row in ws.iter_rows(max_row=3, values_only=True):
                    if any(isinstance(x, str) and "sensitiv" in x.lower() for x in row):
                        sens_cols.append(f + ":" + ws.title)
    pdf_text = {f: A.pdf_text(os.path.join(TARGET, f)) for f in files if f.endswith(".pdf")}
    figure_sens = [f for f, t in pdf_text.items()
                   if re.search(r"sensitivity (?:of|was|is|at|reached|came to)\s[^.]{0,30}\d+(?:\.\d+)? ?(?:%|per cent)",
                                t, re.I)]
    check("R1b no shipped file states a sensitivity figure (the quantity is the analyst's to estimate)",
          not sens_cols and not figure_sens, ", ".join(sens_cols + figure_sens))
    check("R2a Layer 1 is present: UTC stamps, three naming systems, unprefixed serials, site letters",
          all(r["Captured (UTC)"].endswith("Z") for r in P.results) and
          len({d["portal_site"] for d in P.directory} - {d["ehr_department"] for d in P.directory}) == 12 and
          any(not str(r[1]).startswith("HO-") and "NR" in str(r[1]) for r in P.history) and
          {v["site"] for v in vr} == {"A", "B", "C"}, "")
    wrong_pooled = sorted(c for c in t_gold if t_pooled[c] != t_gold[c])
    check("R2b the stump is Layer 2: on the clean truth the pooled route files the wrong point",
          len(wrong_pooled) >= 4, "wrong at %s" % ", ".join(wrong_pooled))
    dash = load_workbook(os.path.join(TARGET, PR.FILES["dashboard"]), read_only=True)
    dash_head = [x for ws in dash for row in ws.iter_rows(max_row=3, values_only=True) for x in row if x]
    proto_pct = re.findall(r"\d+(?:\.\d+)? per cent", pdf_text[PR.FILES["protocol"]])
    check("R3a no decoy: no file ranks the points by clinic, the protocol carries no results, no memo argues a point",
          not any("sensitiv" in str(x).lower() for x in dash_head) and
          all(p in ("10 per cent", "90 per cent", "95 per cent") for p in proto_pct), "protocol: %s" % proto_pct)
    check("R3b not semantics: with every camera known exactly, the default route still lands wrong",
          t_pooled != t_gold and t_gold == gold, "clean-truth golden equals the pack's golden")
    named = []
    for f, t in pdf_text.items():
        for sent in re.split(r"(?<=[.;])\s+", t):
            low = sent.lower()
            if re.search(r"nr-?40|nr-?70|halvard", low) or (
                    "camera" in low and re.search(r"sensitiv|perform|accura|result|score", low)):
                named.append(f)
    check("R3c not rule application: no filed document ties the camera to the AI's performance",
          not named, ", ".join(sorted(set(named))))
    cheap = {r: picks_of(L, r) for r in ("pooled", "casemix", "worst_subgroup", "snapshot")}
    landing = [r for r, pk in cheap.items() if pk == gold]
    check("R3d analyst test: none of the cheap routes lands the call", not landing,
          "; ".join("%s wrong at %d" % (r, sum(pk[c] != gold[c] for c in gold)) for r, pk in cheap.items()))

    # ---------------------------------------------------------------- semantic fork table
    var = {"utc": A.ladder(P, dating="utc"), "days": A.ladder(P, weights="days"),
           "gradable": A.ladder(P, weights="gradable"), "age": A.ladder(P, stratify="age")}
    check("SF1 reference year and camera join by local date or by UTC date: same call",
          picks_of(var["utc"]) == gold, "")
    # sensitivity among gradable referable screenings only (Ungradable left out of the denominator)
    vrows = P.val_rows()
    by_m = {m: [r for r in vrows if r["model"] == m] for m in ("NR-40", "NR-70")}

    def picks_with(sensfn):
        out = {}
        for c in P.codes:
            wts = L["golden"][c][2]
            cells = {nm: sum(wts[m] * sensfn(by_m[m], cut) for m in wts) for nm, cut in P.ops}
            out[c] = A.pick_point(P, cells)
        return out

    def sens_gradable(rows, cut):
        rr = [r for r in rows if r["ref"] and not r["ung"]]
        return sum(r["score"] >= cut for r in rr) / len(rr)

    alt2 = picks_with(sens_gradable)
    check("SF2 Ungradable left out of sensitivity: ruled out by CAI-03 2.4 (it refers), and the call holds",
          "Ungradable result" in pdf_text[PR.FILES["standard"]] and alt2 == gold,
          "%d clinics differ" % sum(alt2[c] != gold[c] for c in gold))
    g1 = []
    for v in P.validation:
        r = dict(ref=v["grader1_level"] in A.REFERABLE_LEVELS or v["grader1_dme"] == "Y")
        g1.append(r)
    for r, base in zip(g1, vrows):
        for k in ("ung", "score", "model"):
            r[k] = base[k]
    by_m_g1 = {m: [r for r in g1 if r["model"] == m] for m in ("NR-40", "NR-70")}
    alt3 = {}
    for c in P.codes:
        wts = L["golden"][c][2]
        cells = {nm: sum(wts[m] * P.sens(by_m_g1[m], cut) for m in wts) for nm, cut in P.ops}
        alt3[c] = A.pick_point(P, cells)
    check("SF3 referable by one grader instead of the final grade: ruled out by CAI-03 2.3 and the protocol's "
          "reference standard (the adjudicated level stands)",
          "reference standard of the network's local validation study" in pdf_text[PR.FILES["standard"]] and
          "adjudicated level stands" in pdf_text[PR.FILES["protocol"]],
          "grader 1 alone moves %d clinics" % sum(alt3[c] != gold[c] for c in gold))
    # the clinic's screenings read as its home patients (visitors moved to their home clinic)
    home = {}
    reg = {r["MRN"]: P.code_of_ehr[r["HOME_DEPARTMENT"]] for r in P.registry}
    acc_mrn = {o["ACCESSION"]: o["MRN"] for o in P.orders if o["PROC_CODE"] == "IMG92229"}
    scr = P.screens()
    hc = Counter()
    for s in scr:
        hc[(reg.get(acc_mrn.get(s["acc"]), s["code"]), s["model"])] += 1
    alt4 = {}
    for c in P.codes:
        n = hc[(c, "NR-40")] + hc[(c, "NR-70")]
        wts = {"NR-40": hc[(c, "NR-40")] / n, "NR-70": hc[(c, "NR-70")] / n}
        cells = {nm: sum(wts[m] * L["by_model"][m][nm] for m in wts) for nm, _ in P.ops}
        alt4[c] = A.pick_point(P, cells)
    check("SF4 a clinic's screenings as its home patients' screenings: ruled out by CAI-03 2.2, and the call holds",
          alt4 == gold, "")
    check("SF5 camera weights by clinic days instead of screenings: same call", picks_of(var["days"]) == gold, "")
    check("SF6 camera by age-group stratified transport: same call", picks_of(var["age"]) == gold, "")
    check("SF7 least sensitive point is the highest DR score threshold (the guide: a lower threshold refers more)",
          "lower threshold refers more" in pdf_text[PR.FILES["opspec"]] and [nm for nm, _ in P.ops][0] == "Standard",
          "")
    check("SF8 the floor compares the estimate as it stands, not a confidence bound (CAI-03 3.1)",
          "compared with the floor as it stands" in pdf_text[PR.FILES["standard"]], "")
    cancelled_ref = sum(1 for o in P.orders if o["PROC_CODE"] == "REF7734" and o["ORDER_STATUS"] == "Cancelled")
    check("SF9 referrals counted as referred screenings or net of cancelled referral orders: within capacity both",
          G["referrals"] <= P.capacity and G["referrals"] - cancelled_ref <= P.capacity,
          "%d and %d against %d" % (G["referrals"], G["referrals"] - cancelled_ref, P.capacity))
    near_floor = [(c, nm) for c in P.codes for nm, _ in P.ops if 84.5 <= 100 * L["golden"][c][0][nm] < 85.5]
    check("SF10 estimate rounded to a whole per cent before the comparison: same call", not near_floor, str(near_floor))
    by_ver = Counter((r["Software Version"]) for r in P.results)
    check("SF11 software 4.2 and 4.3 on one score scale (the guide), and both versions in every clinic's year",
          "same scale" in pdf_text[PR.FILES["opspec"]] and len(by_ver) == 2, str(dict(by_ver)))
    oc_case, oq_case = A.ask_overreads(P, scope="ai", pair=False)
    check("SF12 a reading center referral is one referral order however many cases (agreement 1.2 and 2.1)",
          "same referral" in pdf_text[PR.FILES["agreement"]] and
          any(oc_case[c][0] != G["overreads_clinic"][c][0] for c in P.codes), "")
    check("SF13 overreads grouped by the quarter the screening was captured (CAI-03 4.1)",
          "screenings captured in the quarter" in pdf_text[PR.FILES["standard"]], "")
    check("SF14 a fault's lost days are days with no screening captured, so the fault day is not one (CAI-03 4.2)",
          "scheduled screening day on which the clinic screened no one" in pdf_text[PR.FILES["standard"]] and
          all(v["days"] < u["days"] for v, u in zip(G["downtime"].values(), A.ask_downtime(P, "cancel_days").values())),
          "")
    check("SF15 days counted between Pacific calendar dates (CAI-03 4.1), not elapsed UTC time",
          "calendar days" in pdf_text[PR.FILES["standard"]], "")

    # ---------------------------------------------------------------- mess neutrality (Layer 1)
    check("M1 UTC capture stamps: Pacific or UTC dating gives the same points and the same referrals by clinic",
          picks_of(var["utc"]) == gold and A.referrals(P, gold) == G["referrals"], "")
    tag_spans = {}
    for r in P.history:
        tag_spans.setdefault(r[0], set()).add(str(r[1]).replace("HO-", ""))
    check("M2 serials typed with and without the maker's prefix: one asset tag per camera serial either way",
          all(len(v) == 1 for k, v in tag_spans.items()), "")
    sites = Counter(r["Site"] for r in P.reads)
    check("M3 the reading center's site codes, the portal's site names and the EHR departments map one to one",
          len(sites) == 12 and len(P.code_of_portal) == 12 and len(P.code_of_ehr) == 12, "")
    check("M4 the validation study's site letters resolve through the protocol to three pilot clinics",
          len(P.pilot) == 3 and all(v in P.code_of_portal for v in P.pilot.values()), str(P.pilot))
    check("M5 visiting patients leave the call unchanged (SF4)", alt4 == gold, "")
    check("M6 merged charts: no MRN in the main call's files (results and validation)",
          "MRN" not in open(os.path.join(TARGET, PR.FILES["results"])).readline() and
          "MRN" not in open(os.path.join(TARGET, PR.FILES["validation"])).readline(), "")
    res_acc = {r["Accession"] for r in P.results}
    other = [r for r in P.reads if r["Accession"] not in res_acc]
    check("M7 re-photographs and teleretinal reads: no row in the result export (zero device rows in the call's "
          "population)", len(other) > 0 and not any(r["Accession"] in res_acc for r in other),
          "%d log cases outside the export" % len(other))
    canc_acc = [o for o in P.orders if o["ORDER_STATUS"] == "Cancelled" and o["ACCESSION"] in res_acc and
                o["PROC_CODE"] == "IMG92229"]
    check("M8 cancelled screening orders carry no screening in the export", not canc_acc, "")

    # ---------------------------------------------------------------- realism sweep
    n_by = Counter(r["Site"] for r in P.results)
    check("S1 no two clinics with the same screening count", len(set(n_by.values())) == len(n_by), "")
    rounds = [f for f, n in meta["row_counts"].items() if n % 100 == 0]
    check("S2 no round row count in any file", not rounds, ", ".join(rounds))
    card = json.load(open(os.path.join(TASK, "..", ".claude", "skills", "fingerprint", "cards", "task281.json")))
    check("S3 personas from the guard's names, as on the card", set(PR.PEOPLE.values()) <= set(card["world"]["people"]),
          ", ".join(PR.PEOPLE.values()))
    sig = []
    for f in files:
        b = open(os.path.join(TARGET, f), "rb").read()
        if re.search(rb"(?i)reportlab|openpyxl|matplotlib|python", b):
            sig.append(f)
        if f.endswith(".xlsx"):
            import zipfile
            with zipfile.ZipFile(os.path.join(TARGET, f)) as z:
                for n in z.namelist():
                    if re.search(rb"(?i)openpyxl|python|pptx|docx", z.read(n)):
                        sig.append(f + ":" + n)
    check("S4 no writer signature in any shipped file", not sig, ", ".join(sig))
    late = []
    asof = PR.ASOF
    for f in files:
        if f.endswith((".csv", ".json")):
            txt = open(os.path.join(TARGET, f)).read()
            for m in re.finditer(r"\b(20\d\d)-(\d\d)-(\d\d)", txt):
                if dt.date(*map(int, m.groups())) > asof:
                    late.append(f)
                    break
            for m in re.finditer(r"\b(\d{1,2})/(\d{1,2})/(20\d\d)\b", txt):
                if dt.date(int(m.group(3)), int(m.group(1)), int(m.group(2))) > asof:
                    late.append(f)
                    break
    check("S5 no date after the fiction's as-of date (%s)" % asof, not late, ", ".join(sorted(set(late))))
    cap = {r["Accession"]: r["Captured (UTC)"] for r in P.results}
    check("S6 the reading center's receipt stamps are its own (every receipt after its own capture, none equal)",
          all(A.utc(r["Received (UTC)"]) > A.utc(cap[r["Accession"]]) for r in P.reads if r["Accession"] in cap), "")
    cam_rows = sum(1 for r in P.history if "NR" in str(r[1]))
    check("S7 camera moves are a minority of the location history", cam_rows < 0.6 * len(P.history),
          "%d of %d" % (cam_rows, len(P.history)))
    prev = sum(r["ref"] for r in vrows) / len(vrows)
    check("S8 validation prevalence realistic and site counts not round", 0.08 <= prev <= 0.14 and
          all(n % 10 for n in Counter(v["site"] for v in vr).values()), "%.3f" % prev)

    # ---------------------------------------------------------------- graded figures against their bin edges
    per_l, per_u = Counter(), Counter()
    cut = dict(P.ops)
    for s in P.screens():
        if s["ung"] or (s["score"] is not None and s["score"] >= cut[gold[s["code"]]]):
            per_l[s["code"]] += 1
    for s in P.screens(dating="utc"):
        if s["day"] <= dt.date(2026, 9, 30) and (s["ung"] or (s["score"] is not None and s["score"] >= cut[gold[s["code"]]])):
            per_u[s["code"]] += 1
    check("E1 referrals by clinic and in total identical under Pacific and UTC dating", per_l == per_u,
          "total %d" % sum(per_l.values()))
    e2 = min(edge(100 * s) for n, s in G["overreads_clinic"].values())
    check("E2 every confirmed-referable share at least 0.05 points from its rounding edge", e2 >= 0.05, "%.3f" % e2)
    e3 = min(edge(v, 0.1) for v in G["overreads_quarter"].values())
    check("E3 every quarter's average days at least 0.005 from its rounding edge", e3 >= 0.005, "%.4f" % e3)
    sh = [100 * L["golden"][c][2].get("NR-40", 0.0) for c in P.codes] + \
         [100 * var["utc"]["golden"][c][2].get("NR-40", 0.0) for c in P.codes]
    e5 = min(edge(x) for x in sh if 0 < x < 100)
    check("E5 every NR-40 share at least 0.15 points from its rounding edge, Pacific and UTC", e5 >= 0.15, "%.3f" % e5)
    fam = [L] + list(var.values())
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    vc = figs["validation_by_model_counts"]
    exact = all(vc[m][nm]["referred"] == round(L["by_model"][m][nm] * L["counts"][m][1]) and
                vc[m][nm]["referable"] == L["counts"][m][1] for m in vc for nm in vc[m])
    check("E6 the write-up states validation sensitivity as referred over referable counts, exact", exact, "")
    # the estimator family a biostatistician would use, each carried to every clinic (SF16)
    est = A.estimators(P)
    labels = list(next(iter(est.values())).keys())
    worst_all = 1.0
    for lab in labels:
        pk = {c: A.pick_point(P, est[c][lab]) for c in P.codes}
        m = min(A.decisive_margin(P, est[c][lab], gold[c]) for c in P.codes)
        worst_all = min(worst_all, m)
        check("F %s: the golden's point at every clinic, decisive cells 1.5 points or more from the floor" % lab,
              pk == gold and m >= 0.015, "%d clinics differ, tightest %.2f points" %
              (sum(pk[c] != gold[c] for c in gold), 100 * m))
    check("SF16 sensitivity by a smoothed calibration of referable status on the DR score: same call",
          all({c: A.pick_point(P, est[c][lab]) for c in P.codes} == gold for lab in labels if "calibration" in lab
              or "logistic" in lab), "tightest decisive cell across the family %.2f points" % (100 * worst_all))
    e7 = min(edge(100 * v, 0.1) for m in L["by_model"].values() for v in m.values())
    check("E7 validation sensitivity by model at least 0.005 from its one-decimal edge", e7 >= 0.005, "%.4f" % e7)
    margin = min(abs(100 * F["golden"][c][0][nm] - 85) for F in fam for c in P.codes for nm, _ in P.ops)
    check("E8 every cell of every family member at least 1.5 points from the floor", margin >= 1.5, "%.2f" % margin)
    e9 = edge(G["referrals"] / 1.0, 1.0)
    check("E9 the referral counts are exact counts (no rounding at stake)", isinstance(G["referrals"], int), "")

    # ---------------------------------------------------------------- the ladder
    for r, pk in cheap.items():
        check("L1 %s rung differs from the golden at two or more clinics" % r,
              sum(pk[c] != gold[c] for c in gold) >= 2, "%d" % sum(pk[c] != gold[c] for c in gold))
    hi = A.referrals(P, {c: "High" for c in P.codes})
    check("L2 the golden is within capacity and High at every clinic is not", G["referrals"] <= P.capacity < hi,
          "%d, %d against %d" % (G["referrals"], hi, P.capacity))
    check("L3 headroom under capacity of 300 or more", P.capacity - G["referrals"] >= 300,
          "%d" % (P.capacity - G["referrals"]))

    # ---------------------------------------------------------------- the pack against the world
    acc_model = {s["acc"]: s["model"] for s in w.screens} if "acc" in w.screens[0] else None
    pack_model = {s["acc"]: s["model"] for s in scr}
    if acc_model is None:
        # world objects carry the accession only after pack.py ran; rebuild the map by order
        acc_model = {}
    check("W1 the register's camera equals the world's camera for every screening",
          clinic_model == Counter((s["code"], s["model"]) for s in scr), "")
    check("W2 the register's camera equals the world's camera for every validation image",
          Counter(v["model"] for v in val) == Counter(r["model"] for r in vrows), "")
    check("W3 the clean-truth golden equals the pack's golden", t_gold == gold, "")

    # ---------------------------------------------------------------- the ask ceiling
    import ceiling
    pc, leak = ceiling.main(TARGET)
    check("C1 pair ceiling at or under 60", pc <= 60, "%.1f" % pc)
    check("C2 mirror leakage under 50 per cent of the ask weight", leak < 50, "%.1f" % leak)

    fails = [r for r in RESULTS if not r[1]]
    print("%s: %d checks, %d FAIL" % ("PASS" if not fails else "FAIL", len(RESULTS), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
