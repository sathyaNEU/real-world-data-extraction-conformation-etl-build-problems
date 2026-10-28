"""Assertions on the built pack: the input gates, the three rules (R1 to R3c) on the shipped files, the ladder and its
margins, the cheap routes, every semantic fork row (SF), each mess item's neutrality, every graded figure's distance
to its bin edge, the ask's separation and its cracker, the distractors and the realism sweep."""
import csv
import datetime as dt
import io
import os
import re
import shutil
import sys
import tempfile

from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P  # noqa: E402
import solve as SV  # noqa: E402

N = [0]


def ok(label, cond, detail=""):
    N[0] += 1
    if not cond:
        raise AssertionError("CHECK FAIL %s %s" % (label, detail))


def pdf(target, key):
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(os.path.join(target, P.FILES[key])).pages))


def same_bins(a, b):
    return all(SV.r10(a["found"][s]) == SV.r10(b["found"][s]) and SV.r10(a["starts"][s]) == SV.r10(b["starts"][s])
               for s in P.SETTINGS)


def margin(d):
    v = sorted(d.values(), reverse=True)
    return v[0] / v[1]


def main(target):
    S = SV.solve(target)
    W = SV.winner

    # ---------------------------------------------------------------- input gates
    files = sorted(os.listdir(target))
    ok("gate: ten or more files", len(files) >= 10, len(files))
    ok("gate: three or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) for f in files if f.endswith(".csv"))
    ok("gate: a file of 25,000 rows or more", big >= 25000, big)
    ok("gate: two distractors", len(P.DISTRACTORS) >= 2)
    ok("gate: no file describes the data", not any(re.search(r"readme|dictionary|notes|manifest|schema", f, re.I)
                                                   for f in files))
    ok("gate: every named file ships", set(P.FILES.values()) == set(files))

    # ---------------------------------------------------------------- R1, the field's raw material
    van = list(csv.DictReader(open(os.path.join(target, P.FILES["van"]), encoding="utf-8")))
    ok("R1 person-level van contacts with offers, tests and results", {"test_outcome", "antibody_result", "rna_result",
                                                                       "client_pseudonym"} <= set(van[0]))
    ok("R1 the hostel lists are person-level", S["census"] > 800, S["census"])
    ok("R1 no shipped column names who the van tested or which pharmacies test and treat",
       not any(re.search(r"van|tested|treat|pilot", h, re.I) for k in ("pharmacies", "hostel_returns", "nsp_reg")
               for h in next(csv.reader(open(os.path.join(target, P.FILES[k]), encoding="utf-8")))))
    ok("R1 the decisive join reads the residents lists against the van's tests", 600 < S["T"] < S["census"], S["T"])

    # ---------------------------------------------------------------- R3: the analyst test and the decisive steps
    L = S["ladder"]
    ok("R3a the default path (2026 rates on each 2027 pool) files the needle exchange", W(L["R0"]) == "NSP")
    ok("R3a its margin over the hostels is 1.15 or more", margin(L["R0"]) >= 1.15, margin(L["R0"]))
    ok("R3b the rollout alone files the hostels", W(L["A_only"]) == "HH" and W(L["A_only_census_only"]) == "HH")
    ok("R3b ... by 1.15 or more on either hostel pool", min(margin(L["A_only"]), margin(L["A_only_census_only"])) >= 1.15,
       (margin(L["A_only"]), margin(L["A_only_census_only"])))
    ok("R3b the first round alone leaves the needle exchange", W(L["B_only"]) == "NSP" and margin(L["B_only"]) >= 1.15)
    ok("R3b both together file Fenwold Recovery's new entrants", W(L["golden"]) == "DS")
    ok("R3b the golden clears the runner-up by 1.2 or more", margin(L["golden"]) >= 1.2, margin(L["golden"]))
    ok("R3b the default path ranks the golden 3rd of 4", sorted(L["R0"], key=lambda s: -L["R0"][s]).index("DS") == 2)
    plan = pdf(target, "plan")
    nums = {int(x) for x in re.findall(r"\d+", plan)}
    ok("R3c the plan states no figure for any setting beyond places, dates and the pharmacies' count",
       nums <= {1, 2, 3, 4, 5, 6, 12, 24, 25, 30, 110, 920, 2026, 2027}, sorted(nums))
    for w in ("recommend", "first round", "already tested", "pilot", "test and treat", "yield"):
        ok("R3c the plan carries no steer: %s" % w, w not in plan.lower())
    intent = pdf(target, "intentions")
    ok("R3c the commissioning intentions never name a pilot or the van", "pilot" not in intent.lower()
       and "van" not in intent.lower().replace("relevant", ""))

    # ---------------------------------------------------------------- cheap routes on the clean record
    C, by = S["C"], SV.start_dates(SV.register(target))
    raw = {s: sum(1 for c in C if c["setting"] == s and c["found"] and SV.started12(c, by)) for s in P.SETTINGS}
    days = {"HH": 70, "NSP": 37, "DS": 38, "AP": 38}
    from world import rota_days
    days = {s: len(v) for s, v in rota_days().items()}
    perday = {s: raw[s] / days[s] for s in P.SETTINGS}
    yld = {s: S["R"][s]["F"] for s in P.SETTINGS}
    spt = {s: S["R"][s]["F"] * S["ST"][s] for s in P.SETTINGS}
    cheap = {"raw 2026 starts": raw, "starts per rota day": perday, "found per test": yld, "starts per test": spt,
             "2026 rates on the 2027 pools": L["R0"]}
    for k, d in cheap.items():
        ok("route: %s lands off the call" % k, W(d) != "DS", (k, W(d)))
    k = S["R"]["HH"]["A"] * S["R"]["HH"]["F"] * S["ST"]["HH"]
    arr_only = dict(L["A_only"], HH=S["pools"]["hh_arrivals"] * k,
                    AP=S["pools"]["ap_arrivals"] * S["R"]["AP"]["A"] * S["R"]["AP"]["F"] * S["ST"]["AP"])
    ok("route: arrivals alone for every setting with the rollout reaches the call only against the plan's section 5",
       W(arr_only) == "DS" and "residents of the approved premises and of the hostels on 30 September 2026" in plan)
    landing = [k for k, d in cheap.items() if W(d) == "DS"]
    ok("route: no single-reflex route lands the call", not landing, landing)

    # ---------------------------------------------------------------- semantic fork table
    G = S
    ok("SF1 the setting is the most people started in 2027; most found gives the same call", W(G["found"]) == "DS")
    ok("SF2 the van's own starts, gross (plan 4)", "only the people the van itself tests, finds and starts" in plan)
    ok("SF3 calendar 2027 from 4 January (plan 1)", "From Monday 4 January 2027" in plan)
    ok("SF4 residents on 30 September and twelve months' arrivals (plan 5)",
       "twelve months to 30 September 2026 as its arrivals in 2027" in plan)
    reis = SV.solve(target, include_reissues=True)
    ok("SF5 new registrants are first registrations; counting every 'New' row keeps the call", W(reis["starts"]) == "DS"
       and "for the first time" in plan)
    ok("SF6 found is RNA detected (plan 4)", "found when the van's RNA test shows an active infection" in plan)
    ok("SF7 started within twelve weeks of the test (plan 4)", "within twelve weeks of the van's test" in plan)
    km = SV.solve(target, st_method="km")
    ok("SF8 the start share over people found by 8 July against Kaplan-Meier: same printed figures", same_bins(S, km),
       ({s: round(km["starts"][s], 1) for s in P.SETTINGS}))
    refs = [r["contact_ref"] for r in van]
    ok("SF9 acceptance per person offered: each double-synced contact once", len(refs) > len(set(refs)) and
       sum(S["R"][s]["offered"] for s in P.SETTINGS) == len(set(refs)), (len(refs), len(set(refs))))
    ok("SF10 test and treat from 1 April 2027 (PH-12)", "1 April 2027" in intent and "PH-12" in intent)
    ok("SF11 every needle exchange pharmacy: the 24 on the list", len(list(csv.DictReader(open(os.path.join(
        target, P.FILES["pharmacies"]), encoding="utf-8")))) == 24)
    pooled = SV.solve(target, nsp_q1="pooled")
    ok("SF12 January to March at each pharmacy's own rate or the pooled rate: same printed figures", same_bins(S, pooled))
    fonly = SV.solve(target, transport="test")
    ok("SF13 the three pharmacies' found per test carried alone, or with their acceptance: same printed figures",
       same_bins(S, fonly))
    for sc in (0.0, 2.0, 4.0):
        v = SV.solve(target, inc_scale=sc)
        ok("SF14 hostel residents who tested negative at %.0fx the clinic's rate: same printed figures" % sc,
           same_bins(S, v))
    ok("SF15 the van does not test again anyone it has found (plan 2)", "does not test again anyone it has already found"
       in plan)
    ok("SF16 each setting at the van's own rates there (plan 4)", "Each setting is sized at the van's own rates there"
       in plan)
    ok("SF17 no tie: the golden's margin", margin(L["golden"]) >= 1.2)
    ok("SF18 rounding once at the end: every printed figure is the rounded unrounded figure",
       all(S["found10"][s] == SV.r10(S["found"][s]) for s in P.SETTINGS))
    ok("SF19 people are distinct: one van contact per person per setting",
       len({(c["pid"], c["setting"]) for c in C}) == len(C))
    ok("SF20 the tablet's clock is UTC: its column says so", "recorded_at_utc" in van[0])

    # ---------------------------------------------------------------- R2, each mess item neutral to the call
    tmp = tempfile.mkdtemp()
    try:
        def variant(edit_key, fn):
            t2 = os.path.join(tmp, edit_key)
            shutil.copytree(target, t2)
            fn(t2)
            return SV.solve(t2)

        def dup_syncs_kept(t2):
            p = os.path.join(t2, P.FILES["van"])
            rows = list(csv.reader(open(p, encoding="utf-8")))
            for i, r in enumerate(rows[1:]):
                r[0] = r[0] + "-%d" % i            # every row its own reference, so no double sync is dropped
            with open(p, "w", newline="", encoding="utf-8") as fh:
                csv.writer(fh, lineterminator="\r\n").writerows(rows)
        v = variant("dups", dup_syncs_kept)
        ok("R2a the tablet's double syncs kept: same call and printed starts", W(v["starts"]) == "DS"
           and v["starts10"] == S["starts10"])
        hh_sites = {c["site"] for c in C if c["setting"] == "HH"}
        ok("R2b the hostels' site names shortened in May leave the residents join alone (it runs on the pseudonym)",
           len(hh_sites) > 9 and S["T"] == sum(p in {c["pid"] for c in C if c["setting"] == "HH" and c["accepted"]}
                                                 for p in SV.census(target)), len(hh_sites))
        utc = SV.solve(target, clock="utc")
        ok("R2c the tablet's UTC clock taken as the local date: same printed figures", same_bins(S, utc))
        ok("R2d reissued registrations kept: same call", W(reis["starts"]) == "DS")
        ok("R2e the laboratory's re-sent results: the new-infection rate is read per person and date",
           S["inc_events"] == SV.incidence(target)[1])
        ok("R2f the two hostel lists' layouts: both sheets read", S["census"] == len(set(SV.census(target))))
        reg = SV.register(target)
        exact = {}
        for r in reg:
            if r["referral_source"] == "Brannock Trust van":
                exact.setdefault(r["pseudonym"], []).append(SV.iso(r["start_date"]))
        st_exact = {s: sum(1 for c in C if c["setting"] == s and c["found"] and c["day"] <= SV.MATURE and SV.started12(c, exact))
                    / max(1, S["R"][s]["mature"]) for s in P.SETTINGS}
        ex = {s: S["found"][s] * st_exact[s] for s in P.SETTINGS}
        ok("R2g the register's three spellings of the van as a source: a one-spelling filter keeps the call", W(ex) == "DS",
           {s: round(x, 1) for s, x in ex.items()})
        codes = {r["clinic_code"] for r in reg}
        ok("R2h the register's clinic codes are the five old, the five new and the pharmacists'", codes ==
           set(P.CLINICS) | set(P.CLINIC_OLD.values()) | {"PHARM"}, sorted(codes))

        # ---------------------------------------------------------------- the distractors
        t3 = os.path.join(tmp, "nodistract")
        shutil.copytree(target, t3)
        for kd in P.DISTRACTORS:
            os.remove(os.path.join(t3, P.FILES[kd]))
        d3 = SV.solve(t3)
        ok("distractors deleted: same call and figures", same_bins(S, d3) and W(d3["starts"]) == "DS")
        ok("distractors deleted: same cures", SV.cures(t3) == SV.cures(target))
    finally:
        shutil.rmtree(tmp)

    # ---------------------------------------------------------------- graded figures mid-bin
    for s in P.SETTINGS:
        ok("bin: %s found %.2f is 1.25 or more from an edge" % (s, S["found"][s]), SV.edge(S["found"][s]) >= 1.25)
        ok("bin: %s starts %.2f is 1.25 or more from an edge" % (s, S["starts"][s]), SV.edge(S["starts"][s]) >= 1.25)

    # ---------------------------------------------------------------- the ask: separation and its devices
    cs = SV.courses(target)
    ok("ask separation: no course the van started ends in the ask's window",
       not any(c["start"] >= P.ROTA_START and SV.H1[0] <= c["last"] <= SV.H2[1] for c in cs))
    g = SV.cures(target)
    cr = SV.cures(target, last_dose="register")
    mi = SV.cures(target, last_dose="register", merge=False, cure_words=("Not detected", "Detected <12 IU/mL"))
    for key in g:
        ok("ask device: the register's end date as the last dose misses %s (%d against %d)" % (key, cr[key], g[key]),
           cr[key] != g[key])
        ok("ask device: the mirror misses %s" % key, mi[key] != g[key])
    disp = {}
    for r in csv.DictReader(open(os.path.join(target, P.FILES["dispensing"]), encoding="utf-8")):
        disp.setdefault(r["course_ref"], []).append(SV.iso(r["dispensed_on"]))
    late = sum(1 for r in reg if r["course_ref"] in disp and r["end_date"] and SV.iso(r["end_date"]) > max(disp[r["course_ref"]])
               + dt.timedelta(days=27 + 14))
    ok("ask forcing: the register's end date falls two weeks or more after the last pack ran out on %d courses" % late,
       late >= 20, late)
    ok("ask determinism: every cell is a whole count of one rule", all(isinstance(v, int) for v in g.values()))

    # ---------------------------------------------------------------- realism sweep
    for key, col in (("van", "contact_ref"), ("nsp_reg", "registration_id"), ("lab", "lab_number")):
        vals = [r[col] for r in csv.DictReader(open(os.path.join(target, P.FILES[key]), encoding="utf-8"))][:400]
        nums = [int(re.sub(r"\D", "", v) or 0) for v in vals]
        steps = {b - a for a, b in zip(nums, nums[1:])}
        ok("realism: %s is not an arithmetic sequence" % col, len(steps) > 5)
    hr = list(csv.DictReader(open(os.path.join(target, P.FILES["hostel_returns"]), encoding="utf-8")))
    ok("realism: hostel arrivals vary month to month", len({r["arrivals"] for r in hr}) > 5)
    names = [r["pharmacy"] for r in csv.DictReader(open(os.path.join(target, P.FILES["pharmacies"]), encoding="utf-8"))]
    ok("realism: pharmacy names take several shapes", len({n.split()[-1] for n in names}) > 3)
    for k in ("plan", "pathway", "intentions"):
        txt = pdf(target, k)
        ok("realism: %s reads back and carries no em or en dash" % k, len(txt) > 500 and "—" not in txt
           and "–" not in txt)
    sub = open(os.path.join(os.path.dirname(HERE), "submission.md")).read()
    cited = set(re.findall(r"[a-z0-9_\-]+\.(?:csv|xlsx|pdf)", sub)) - {"clinic_cures_2024-25.xlsx"}
    ok("H8 every file the write-up names ships under that name", cited <= set(files), sorted(cited - set(files)))
    for k in ("plan", "pathway", "intentions"):
        strict = " ".join(p.extract_text() for p in PdfReader(os.path.join(target, P.FILES[k]), strict=True).pages)
        ok("H25 %s reads the same under the strict reader" % k, re.sub(r"\s+", " ", strict) == pdf(target, k))
    ok("realism: the personas come from the seeded list", {P.DIRECTOR, P.TEAM_LEAD, P.CLIN_LEAD} <= {
        "Stephanie Davis", "Alison Hartley", "Duncan Jackson", "Arthur Murray", "Nicholas Hodgson", "Bradley Birch",
        "Gavin Gordon", "Oliver O'Brien", "Patricia Richardson", "Angela Roberts"})
    print("checks: %d assertions passed" % N[0])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
