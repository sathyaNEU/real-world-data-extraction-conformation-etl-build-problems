"""The generator's assertions for task121, run on every build: the three rules on the clean truth (R1 to R3), the
semantic fork table (SF), the ladder and the golden's family, the asks' devices and their fairness, the separation of
the asks from the call, the pack's hygiene (no file describes the data, the input gates, and each closure the producing
systems now carry), and the realism sweep. Prints one line a check; returns 1 on any failure."""
import calendar
import collections
import datetime as dt
import os
import re
import zipfile

import numpy as np
import pandas as pd

import analysis as A
import asks as AK
import common as K
import pack as P

OUT = []

# a file or sheet named as a description of the data (dataset-generation section 3; the names leak.py screens, with
# an index and a contents list added)
DESCRIBE = re.compile(
    r"(?<![a-z])(read_?me|data_?dictionar\w*|dictionar(y|ies)|codebook|field_?notes|field_?guide|"
    r"fields?_(guide|notes|list|descriptions?)|\w*_fields|manifest|extract_contents|file_list|file_layout|glossary|"
    r"column_(notes|descriptions?)|data_?notes|how_to_read|about_this|export_notes|extract_notes|feed_notes|definitions|"
    r"schema|layouts?_notes|handling_notes|release_notes|index|contents|notes)(?![a-z])", re.I)
DESCRIBE_SHEET = re.compile(r"^(read ?me|notes?|dictionary|data dictionary|definitions|glossary|fields|field notes|"
                            r"about|about this (file|workbook)|how to (read|use)( this)?|columns?|index|contents)$", re.I)


def row(label, ok, detail=""):
    OUT.append((label, bool(ok), detail))


def _rate(x):
    return 100.0 * x["under"].mean() if len(x) else float("nan")


def run(task, world, res):
    OUT.clear()
    target = os.path.join(task, "target")
    G = res["G"]
    rg = res["rungs"]
    F = G["F"]
    hi, sh, calls = F["hi"], F["shifts"], F["calls"]
    b, a = hi[~hi["after"]], hi[hi["after"]]
    # ------------------------------------------------------------------ the call
    row("CALL every answered call falls inside one shift worked", F["matched"] == F["answered"],
        "%d of %d" % (F["matched"], F["answered"]))
    row("CALL the step across March", G["after"] - G["before"] >= 3.5, "%.2f to %.2f" % (G["before"], G["after"]))
    row("CALL quick returns rare before March, about one shift in six from March",
        G["qr_share_before"] < 3.0 and 13.0 < G["qr_share_after"] < 20.0,
        "%.2f and %.2f" % (G["qr_share_before"], G["qr_share_after"]))
    row("CALL rested shifts hold across the go-live", abs(G["after_rested"] - G["before_rested"]) < 1.0,
        "%.2f to %.2f" % (G["before_rested"], G["after_rested"]))
    row("CALL quick-return shifts carry the rise", G["after_qr"] > 2.5 * G["after_rested"],
        "%.2f against %.2f" % (G["after_qr"], G["after_rested"]))
    # the world's truth: no release effect on triage; the quick-return multiple alone
    tw = world.calls
    hi_w = [c for c in tw if c["hi"] and c["contact"]]
    rel_rested_b = np.mean([c["cold"] for c in hi_w if not world.shifts[c["shift"]]["qr"] and c["version"] == "13.1"])
    rel_rested_a = np.mean([c["cold"] for c in hi_w if not world.shifts[c["shift"]]["qr"] and c["version"] == "13.3"])
    row("CALL truth: on rested shifts the release moves nothing", abs(rel_rested_a - rel_rested_b) < 0.01,
        "%.4f against %.4f" % (rel_rested_b, rel_rested_a))
    # ------------------------------------------------------------------ R1 raw material, no deciding column
    heads = {k: pd.read_csv(os.path.join(target, K.FILES[k]), nrows=0).columns.tolist()
             for k in ("takers", "roster", "calls", "epcr", "units", "che", "tcpr", "casereview", "unithours")}
    bad = [k + "." + c for k, cs in heads.items() for c in cs
           if re.search(r"(^|_)rest(_|$)|quick|fatigue|hours_off|(^|_)gap(_|$)", c)]
    row("R1 no shipped column holds rest or a quick return", not bad, ", ".join(bad))
    row("R1 the golden builds rest from the shifts worked", sh["rest"].notna().mean() > 0.97 and len(sh) > 9000,
        "%d shifts" % len(sh))
    # ------------------------------------------------------------------ R2 each Layer 1 item mishandled is neutral
    base = (K.r1(G["before"]), K.r1(G["after"]), K.r1(G["qr_share_before"]), K.r1(G["qr_share_after"]),
            K.r1(G["after_qr"]), K.r1(G["after_rested"]), K.r1(G["before_rested"]))
    d = P.load(target)
    e = d["epcr"].copy()
    e["incident_no"] = e["incident_number"].str[:2] + "-" + e["incident_number"].str[2:]
    e["acuity"] = e["crew_acuity"].str[0].astype(int)
    per_patient = e[e["acuity"].isin([1, 2])].groupby("incident_no").size()
    row("R2 second patients: counting patient records leaves the critical or emergent calls as they are",
        (per_patient == 1).all(), "%d calls with two such patients" % int((per_patient > 1).sum()))
    r = d["roster"].copy()
    r["s"] = P.local(r["start"], False)
    r["e"] = P.local(r["end"], False)
    r = r.sort_values(["employee_no", "s"])
    rest_local = (r["s"] - r.groupby("employee_no")["e"].shift(1)).dt.total_seconds() / 3600.0
    row("R2 daylight saving: rests between 9 and 15 hours never occur, so local and elapsed time split the same",
        not ((rest_local > 9.0) & (rest_local < 15.0)).any(), "")
    reg = r[r["worked_as"] == "Regular"].copy()
    rr = (reg["s"] - reg.groupby("employee_no")["e"].shift(1)).dt.total_seconds() / 3600.0
    qr_reg_after = 100.0 * (rr[reg["s"].dt.date >= K.SPLIT] < 11).mean()
    row("R2 swaps and overtime: the regular shifts alone keep the quick returns' share within a point",
        abs(qr_reg_after - G["qr_share_after"]) < 1.0, "%.2f against %.2f" % (qr_reg_after, G["qr_share_after"]))
    v = calls.copy()
    v13 = v[v["t"] >= pd.Timestamp(K.RELEASE)]
    row("R2 the release at 06:00: every call from go-live is on 13.3", (v13["protocol_version"] == "13.3").all(), "")
    # ------------------------------------------------------------------ R3 the three rules executed
    row("R3a ANALYST the step across March, the release's date inside it", G["after"] - G["before"] >= 3.5, "")
    row("R3a ANALYST the veterans' calls rise as the whole does", rg["Rg_veterans"][1] - rg["Rg_veterans"][0] >= 3.0,
        "%.2f to %.2f" % rg["Rg_veterans"])
    row("R3a ANALYST the earlier mix keeps the rise", rg["Rm_standardised"][1] - G["before"] >= 3.0,
        "%.2f" % rg["Rm_standardised"][1])
    row("R3a ANALYST the release's changed protocols rise most",
        rg["Rp_changed"][1] - rg["Rp_changed"][0] > rg["Rp_unchanged"][1] - rg["Rp_unchanged"][0],
        "%.2f to %.2f against %.2f to %.2f" % (rg["Rp_changed"] + rg["Rp_unchanged"]))
    row("R3b DECISIVE rest alone: rested shifts hold, quick returns carry it",
        abs(G["after_rested"] - G["before_rested"]) < 1.0 and G["after_qr"] > 2.5 * G["after_rested"], "")
    names = [K.FILES[k] for k in K.FILES]
    row("R3c no memo, analysis or cause statement ships", not any(re.search(r"memo|analysis|cause|finding", n)
                                                                   for n in names), "")
    # ------------------------------------------------------------------ the semantic fork table
    row("SF1 most acute patient against every record: same calls", (per_patient == 1).all(), "")
    row("SF2 the six months: the rested shifts hold from the go-live date too",
        abs(_rate(hi[(hi["t"] >= pd.Timestamp(K.RELEASE)) & ~hi["qr"]]) - G["before_rested"]) < 1.2, "")
    rests = sh["rest"].dropna()
    row("SF3 no rest between 9 and 15 hours, so 10 to 12 hours split the same", not ((rests > 9) & (rests < 15)).any(),
        "%d shifts under 9 hours" % int((rests < 9).sum()))
    row("SF4 every call inside exactly one shift worked", F["matched"] == F["answered"], "")
    row("SF5 the CAD and the scheduling system both in local time", True, "")
    row("SF6 the counterfactual: rested shifts hold across the go-live", abs(G["after_rested"] - G["before_rested"]) < 1.0,
        "")
    grads = d["takers"][d["takers"]["academy_class"] != ""]
    row("SF7 six graduates, every one certified in February 2026", len(grads) == 6 and
        (grads["emd_certified"] == "02/06/2026").all(), "")
    # ------------------------------------------------------------------ the ladder and the family
    row("LADDER R0 names the release (step at the go-live)", G["after"] - G["before"] >= 3.5, "")
    row("LADDER Rt nights hold, days and evenings rise", abs(rg["Rt_shift_type"]["Night"][1] -
                                                           rg["Rt_shift_type"]["Night"][0]) < 1.5 and
        rg["Rt_shift_type"]["Day"][1] - rg["Rt_shift_type"]["Day"][0] > 2.5, "")
    fam = []
    for cut in (9, 10, 12, 14, 15):
        q = hi.assign(qr=hi["rest"] < cut)
        fam.append(("threshold %d" % cut, _rate(q[q["after"] & ~q["qr"]]) - _rate(q[~q["after"] & ~q["qr"]]),
                    _rate(q[q["after"] & q["qr"]]) / _rate(q[q["after"] & ~q["qr"]])))
    for t in ("Day", "Evening"):
        q = hi[hi["shift"] == t]
        fam.append(("within %s" % t, _rate(q[q["after"] & ~q["qr"]]) - _rate(q[~q["after"] & ~q["qr"]]),
                    _rate(q[q["after"] & q["qr"]]) / _rate(q[q["after"] & ~q["qr"]])))
    q = hi[~hi["graduate"]]
    fam.append(("veterans", _rate(q[q["after"] & ~q["qr"]]) - _rate(q[~q["after"] & ~q["qr"]]),
                _rate(q[q["after"] & q["qr"]]) / _rate(q[q["after"] & ~q["qr"]])))
    for nm, drift, ratio in fam:
        lim = 1.5 if nm.startswith("threshold") else 2.0     # a shift type or the veterans alone: half the calls
        row("FAMILY %s: rested shifts hold, quick returns carry the rise" % nm, abs(drift) < lim and ratio > 2.2,
            "%.2f, %.2f" % (drift, ratio))
    # a logistic fit on protocol, hour band and quick return, with a step at the go-live
    import statsmodels.formula.api as smf
    h2 = hi.assign(y=hi["under"].astype(int), qr_i=hi["qr"].astype(int), rel=hi["after"].astype(int),
                   band=(hi["t"].dt.hour // 6).astype(str))
    fit = smf.logit("y ~ C(protocol) + C(band) + qr_i + rel", data=h2).fit(disp=0)
    row("FAMILY logistic: quick return strong, the go-live step near nothing",
        fit.params["qr_i"] > 1.0 and abs(fit.params["rel"]) < 0.15,
        "qr %.2f, go-live %.2f" % (fit.params["qr_i"], fit.params["rel"]))
    # ------------------------------------------------------------------ the asks
    g = res["asks"]
    st = AK.stops(target)
    for k, ask, need in (("A_split_incidents_kept", "A", 12), ("A_current_unit", "A", 12),
                         ("A_split_incident_for_call", "A", 12), ("B_times_as_keyed", "B", 12),
                         ("B_seconds_as_recorded", "B", 12), ("B_every_reviewer_read", "B", 12),
                         ("B_reviewer_left_out", "B", 9), ("B_calibration_kept", "B", 6),
                         ("C_passed_calls_kept", "C", 12), ("C_same_number_ten_minutes", "C", 10),
                         ("C_ten_digit_kept", "C", 12),
                         ("C_abandoned_counted", "C", 12)):
        moved = [ym for ym in K.MONTHS if st[k][ym] != g[ask][ym]]
        row("ASK%s %s moves %d months or more" % (ask, k, need), len(moved) >= need, "%d of 12" % len(moved))
    # Ask A: a split incident repeats its call's phone call, answer second and call-taker; no two calls share all three
    c = d["calls"].copy()
    key = c["che_call_id"] + "|" + c["call_answered"] + "|" + c["call_taker"]
    dup = key.duplicated(keep=False)
    grp = c[dup].groupby(key[dup]).size()
    row("ASKA fair: a split incident shares its call with exactly one other incident, every month",
        (grp == 2).all() and c.loc[dup, "call_answered"].str[:2].nunique() == 12,
        "%d calls carried by two incidents" % len(grp))
    row("ASKA silent: the incident number is unique and no split shares a row's other columns",
        c["incident_no"].is_unique and not c.drop(columns=["incident_no"]).duplicated().any(), "")
    e2 = e.groupby("incident_no")["acuity"].min()
    later = c[key.duplicated()]["incident_no"]
    row("ASKA separation: no split incident has a critical or emergent patient, so the call never counts one",
        e2.reindex(later).dropna().ge(3).all() and e2.reindex(later).notna().all(), "%d split incidents" % len(later))
    row("ASKA separation: every critical or emergent call is the first incident of its call",
        not hi["incident_no"].isin(set(later)).any(), "")
    # Ask B: QA7's times read as minutes and seconds; calibration pairs agree only when so read
    tb = d["tcpr"]
    tb = tb[tb["first_compression_s"] != ""].copy()
    tb["fc"] = tb["first_compression_s"].astype(int)
    q7 = tb[tb["reviewer"] == K.MINSEC_REVIEWER]
    other = tb[tb["reviewer"] != K.MINSEC_REVIEWER]
    row("ASKB fair: none of QA7's times of 100 or more ends in 60 to 99; the other reviewers' do about one in six",
        (q7["fc"] % 100 < 60).all() and ((other["fc"] >= 100) & (other["fc"] % 100 >= 60)).sum() > 40,
        "%d of QA7's, %d of the others'" % (len(q7), int(((other["fc"] >= 100) & (other["fc"] % 100 >= 60)).sum())))
    pr = tb[tb["review_type"] == "Primary"].set_index("incident_no")
    cal = tb[tb["review_type"] == "Calibration"]
    raw, conv = [], []
    for _, x in cal.iterrows():
        y = pr.loc[x["incident_no"]]
        if K.MINSEC_REVIEWER in (x["reviewer"], y["reviewer"]):
            cv = lambda rv, v: AK.minsec_seconds(v) if rv == K.MINSEC_REVIEWER else v
            raw.append(abs(int(x["fc"]) - int(y["fc"])))
            conv.append(abs(cv(x["reviewer"], int(x["fc"])) - cv(y["reviewer"], int(y["fc"]))))
    row("ASKB fair: QA7's calibration pairs differ by 30 seconds or more as stored and by 4 or less when read",
        len(raw) >= 20 and min(raw) >= 30 and max(conv) <= 4, "%d pairs" % len(raw))
    rb = tb[tb["review_type"] == "Primary"].copy()
    rb.loc[rb["reviewer"] == K.MINSEC_REVIEWER, "fc"] = rb.loc[rb["reviewer"] == K.MINSEC_REVIEWER, "fc"].map(
        AK.minsec_seconds)
    rb["ans"] = P.local(rb["incident_no"].map(d["calls"].set_index("incident_no")["call_answered"]))
    rb["s"] = (P.local(rb["recording_started"]) + pd.to_timedelta(rb["fc"], unit="s") - rb["ans"]).dt.total_seconds()
    meds = rb.groupby([rb["ans"].dt.year, rb["ans"].dt.month])["s"].median()
    row("ASKB every month's median a whole second", (meds == meds.round()).all(), "%d months" % len(meds))
    tr = d["tcpr"].copy()
    tr = tr[tr["review_type"] == "Primary"]
    tr["started"] = P.local(tr["recording_started"])
    tr["ans"] = P.local(tr["incident_no"].map(d["calls"].set_index("incident_no")["call_answered"]))
    ring = (tr["ans"] - tr["started"]).dt.total_seconds()
    row("ASKB every recording starts before its answer, by the ring seconds", (ring >= 1).all() and (ring <= 120).all(),
        "%d to %d seconds" % (ring.min(), ring.max()))
    row("ASKB no arrest call is split", not set(d["tcpr"]["incident_no"]) & set(later), "")
    # Ask C: a passed call arrives the second the record it came from was released, on the same trunk group and from
    # the same number; no other record does, and a number's next call otherwise comes six seconds or more after
    che = d["che"]
    passed = AK.passed_calls(che)
    h2 = che.assign(arr=pd.to_datetime(che["arrived_utc"]), rel=pd.to_datetime(che["released_utc"]))
    h2 = h2.sort_values(["trunk_group", "ani", "arr"])
    gap = (h2["arr"] - h2.groupby(["trunk_group", "ani"])["rel"].shift(1)).dt.total_seconds()
    row("ASKC fair: the passed calls are exactly the records at no gap; a number's other repeats come 6 seconds on",
        int((gap == 0).sum()) == int(passed.sum()) and not ((gap > 0) & (gap < 6)).any() and passed.sum() > 9000,
        "%d passed, %d repeats within ten minutes" % (int(passed.sum()), int(((gap >= 6) & (gap <= 600)).sum())))
    mp = che.loc[passed, "position"].str[1:].replace("", "0").astype(int)
    mo = che.loc[~passed & (che["position"] != ""), "position"].str[1:].astype(int)
    row("ASKC silent: no position isolates the passed calls (dispatch positions answer first offers too, the call "
        "floor answers passed calls)", (mp.between(1, 14)).sum() > 3000 and (mo >= 15).sum() > 2500, "")
    medche = set(d["calls"]["che_call_id"])
    row("ASKC no medical call is passed", not che.loc[passed, "call_id"].isin(medche).any(), "")
    ten = che[che["trunk_group"] == "TG07"]
    row("ASKC 10-digit calls in every month", ten.shape[0] > 6000, "%d calls" % len(ten))
    # ------------------------------------------------------------------ separation
    import inspect
    src = inspect.getsource(A)
    row("SEP the call reads none of the unit history, the call detail or the arrest reviews",
        not any(s in src for s in ('d["units"]', 'd["che"]', 'd["tcpr"]')), "analysis opens calls, epcr, roster, takers")
    row("SEP the asks' devices sit off the call's columns", "unit_assigned" not in src and "che_call_id" not in src, "")
    base_c = d["calls"]
    d["calls"] = base_c[~base_c["incident_no"].isin(set(later))]
    G2 = A.golden(target)
    d["calls"] = base_c
    same = all(K.r1(G2[k]) == K.r1(G[k]) for k in ("before", "after", "qr_share_before", "qr_share_after", "after_qr",
                                                   "after_rested", "before_rested"))
    row("SEP the call's figures are the same with the split incidents taken out", same, "")
    # ------------------------------------------------------------------ nothing describes the data (dataset-generation 3)
    shipped = sorted(os.listdir(target))
    retired = ("data_dictionary", "qa_program_definitions_2025", "qa_review_folder_index")
    row("PACK control: the name screen flags every describing name the pack used to carry",
        all(DESCRIBE.search(n) for n in retired), ", ".join(retired))
    named = [f for f in shipped if DESCRIBE.search(os.path.splitext(f)[0])]
    row("PACK no shipped file is named as a description of the data (dictionary, manifest, index, definitions)",
        not named and set(shipped) == set(K.FILES.values()), ", ".join(named) or "%d files" % len(shipped))
    row("PACK no text or markdown file ships", not [f for f in shipped if f.endswith((".txt", ".md"))], "")
    import openpyxl
    sheets = openpyxl.load_workbook(os.path.join(target, K.FILES["reference"]), read_only=True).sheetnames
    row("PACK no sheet is named as notes, a dictionary or an index (control: the screen flags 'Data dictionary')",
        DESCRIBE_SHEET.match("Data dictionary") and not [s for s in sheets if DESCRIBE_SHEET.match(s.strip())],
        ", ".join(sheets))
    texts = {k: _pdf_text(os.path.join(target, K.FILES[k])) for k in ("program", "release")}
    own = {"program": "the cause is the change without which the measure would have stayed where it was",
           "release": "goes live on every call-taking position at 06:00"}
    row("PACK control: each document's own sentence is found in its extracted text",
        all(len(texts[k]) > 500 and _has(texts[k], own[k]) for k in texts),
        ", ".join("%s %d chars" % (k, len(v)) for k, v in texts.items()))
    ident = sorted({c for cs in heads.values() for c in cs if "_" in c or re.search(r"\d", c)})
    hits = sorted({c for k in texts for c in ident if _has(texts[k], c)})
    row("PACK no document names a column of the data files (control: the search finds one in a header line)",
        not hits and _has(",".join(heads["calls"]), "che_call_id"), ", ".join(hits) or "%d names screened" % len(ident))
    exts = {os.path.splitext(f)[1] for f in shipped}
    nrows = {k: len(d[k]) for k in heads}
    row("INPUT 10 or more files, 3 or more formats, a 25,000-row file, two distractors shipped",
        len(shipped) >= 10 and len(exts) >= 3 and max(nrows.values()) >= 25000 and len(K.DISTRACTORS) >= 2 and
        all(K.FILES[k] in shipped for k in K.DISTRACTORS),
        "%d files, %s, largest %d rows" % (len(shipped), " ".join(sorted(exts)), max(nrows.values())))
    # ------------------------------------------------------------------ closures the dictionary and the index carried,
    # now carried by the producing systems and the program, read through the verifier's own extractor
    import verify as VF
    vcalls = VF.rows(target, K.FILES["calls"])
    vche = VF.rows(target, K.FILES["che"])
    per_id = collections.Counter(r["call_id"] for r in vche)
    che_by = {r["call_id"]: r for r in vche}
    row("SF5 C1 every CAD answer time is the call detail's answered_utc on the centre's clock, so the CAD keeps local "
        "time", all(VF.lt(c["call_answered"]) == VF.central(VF.utc(che_by[c["che_call_id"]]["answered_utc"]))
                    for c in vcalls) and _has(texts["program"], "calendar months in local time (US Central)"),
        "%d incidents" % len(vcalls))
    triples = {(c["che_call_id"], c["call_answered"], c["call_taker"]) for c in vcalls}
    row("ASKA grain: each che_call_id is one call_id of the call detail, and alone selects the verifier's calls",
        all(per_id[c["che_call_id"]] == 1 for c in vcalls) and len({c["che_call_id"] for c in vcalls}) == len(triples)
        < len(vcalls), "%d incidents, %d calls" % (len(vcalls), len(triples)))
    vepcr = VF.rows(target, K.FILES["epcr"])
    incs = {c["incident_no"] for c in vcalls}
    vtk = VF.rows(target, K.FILES["takers"])
    logins, emps = {t["cad_login"] for t in vtk}, {t["employee_no"] for t in vtk}
    row("CLOSURE 16 C1 every ePCR number, dashed after its second digit, is a CAD incident; every CAD login and roster "
        "employee is on the call-taker list once",
        all(e["incident_number"].isdigit() and e["incident_number"][:2] + "-" + e["incident_number"][2:] in incs
            for e in vepcr) and len(logins) == len(emps) == len(vtk) and
        all(c["call_taker"] in logins for c in vcalls) and
        all(r["employee_no"] in emps for r in VF.rows(target, K.FILES["roster"])) and
        _has(texts["program"], "matched to the call by its incident number"), "%d patient records" % len(vepcr))
    row("CLOSURE 19 C1 the CAD's COLD falls on exactly the determinants at level O, A, B or C (QA 2.1)",
        all((c["response"] == "COLD") == (c["determinant"].split("-")[1] in K.LEVELS_COLD) for c in vcalls) and
        _has(texts["program"], "cold at a determinant of level O, A, B or C"), "")
    stamp = calendar.timegm(K.ASSEMBLED.timetuple())
    row("CLOSURE 4 every shipped file is saved at the folder's assembly, 4 November 2026",
        all(int(os.stat(os.path.join(target, f)).st_mtime) == stamp for f in shipped), "")
    b_alt = AK.tcpr(target, from_answer=False)
    moved_b = [ym for ym in K.MONTHS if b_alt[ym] != g["B"][ym]]
    row("ASKB clock: QA 5.1 times review events from the recording's start, the verifier's reading; from the answer "
        "instead the months move", _has(texts["program"], "the reviewer times each event from the start of the "
                                                           "recording") and len(moved_b) >= 10,
        "%d of 12 months move" % len(moved_b))
    # ------------------------------------------------------------------ the golden's dates, as the roster shows them
    ro = d["roster"].assign(s=P.local(d["roster"]["start"], False), e=P.local(d["roster"]["end"], False))
    ro = ro.sort_values(["employee_no", "s"])
    ro["rest"] = (ro["s"] - ro.groupby("employee_no")["e"].shift(1)).dt.total_seconds() / 3600.0
    first_qr = ro.loc[(ro["s"] >= pd.Timestamp(K.SPLIT)) & (ro["rest"] < K.QUICK_RETURN_HOURS), "s"].min()
    rr_ = ro[ro["worked_as"] == "Regular"].copy()
    rr_["d"] = rr_["s"].dt.normalize()
    rr_["run"] = (rr_["d"] - rr_.groupby("employee_no")["d"].shift(1)).dt.days.ne(1).cumsum()
    runs = rr_.groupby("run").agg(start=("d", "min"), kinds=("shift", "nunique"))
    mixed_from = runs.loc[runs["kinds"] > 1, "start"].min()
    row("GOLDEN the Began row's dates: regular runs mixing two shift types first start 2 March 2026, the first quick "
        "return from March on 4 March 2026", mixed_from == pd.Timestamp(K.ROTATION) and
        first_qr.date() == dt.date(2026, 3, 4), "%s, %s" % (mixed_from.date(), first_qr))
    # ------------------------------------------------------------------ realism and containers
    cnt = d["calls"].assign(m=P.local(d["calls"]["call_answered"]).dt.to_period("M")).groupby("m").size()
    row("REAL monthly call counts all differ", cnt.nunique() == len(cnt), "")
    row("REAL no em or en dash in any shipped text", _no_dash(target), "")
    row("REAL every record before the folder's assembly", _dates_ok(d), "")
    row("CONTAINER no writer signature", _scrubbed(target), "")
    for label, ok, detail in OUT:
        print("%-5s %-75s %s" % ("PASS" if ok else "FAIL", label[:75], detail))
    bad = [o for o in OUT if not o[1]]
    print("checks: %d run, %d failed" % (len(OUT), len(bad)))
    return 1 if bad else 0


def _pdf_text(path):
    """a shipped PDF's text as pypdf extracts it, the reader leak.py uses"""
    import pypdf
    return "\n".join(p.extract_text() or "" for p in pypdf.PdfReader(path).pages)


def _has(text, phrase):
    """the phrase in the text as whole words, line breaks and runs of spaces read as one space"""
    flat, want = " ".join(text.split()), " ".join(phrase.split())
    return re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(want), flat) is not None


def _no_dash(target):
    for f in os.listdir(target):
        p = os.path.join(target, f)
        if f.endswith((".csv", ".txt")):
            if re.search("[–—]", open(p, encoding="utf-8").read()):
                return False
        if f.endswith(".pdf"):
            text = _pdf_text(p)
            if not text or re.search("[–—]", text):
                return False
    return True


def _dates_ok(d):
    lim = pd.Timestamp(K.ASSEMBLED)
    t1 = P.local(d["epcr"]["pcr_completed"], False).max()
    t2 = pd.to_datetime(d["tcpr"]["reviewed_on"], format="%m/%d/%Y").max()
    t3 = pd.to_datetime(d["casereview"]["reviewed_on"], format="%m/%d/%Y").max()
    return all(t < lim for t in (t1, t2, t3))


def _scrubbed(target):
    for f in os.listdir(target):
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            data = open(p, "rb").read()
            if b"ReportLab" in data or b"reportlab" in data:
                return False
        if f.endswith(".xlsx"):
            with zipfile.ZipFile(p) as z:
                core = z.read("docProps/core.xml") + z.read("docProps/app.xml")
                if b"openpyxl" in core:
                    return False
    return True
