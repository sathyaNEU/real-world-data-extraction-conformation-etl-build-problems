"""The generator's assertions on the cut pack: the input gates, the call and its estimator family, the rungs, the three
rules (R1 the field's raw material ships, R2 every mess item neutral, R3 the analyst test on the clean truth), the
semantic forks (SF rows), the separation of the asks from the call, the ask devices and their stops, the rounding
edges, the realism sweep and the containers. Every label is printed with PASS or FAIL; the run fails on any FAIL."""
import collections
import datetime as dt
import json
import os
import re
import zipfile

import numpy as np
import pandas as pd

import analysis as A
import asks as AK
import common as K
import side as SD

ROWS = []


def row(label, ok, detail=""):
    ROWS.append((label, bool(ok), detail))


def below(D):
    return tuple(sorted((c for c, v in D.items() if v < K.BENCHMARK / 100.0), key=K.WARD.index))


def edge(v, unit):
    """distance from the unrounded value to the nearest rounding edge at the printed unit"""
    return unit / 2 - abs(v - round(v / unit) * unit)


def run(task, b, fig, res):
    target = os.path.join(task, "target")
    golden_dir = os.path.join(task, "golden")
    W, S = b["world"], b["side"]
    F = res["g"]["F"]
    gold = tuple(fig["call"]["funded"])

    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(target))
    row("GATE files", len(files) >= 10, "%d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    row("GATE formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    big = max(b["counts"].values())
    row("GATE 25,000-row file", big >= 25000, "largest %d rows" % big)
    meta = json.load(open(os.path.join(task, "metadata.json")))
    row("GATE distractors", len(meta["distractor_files"]) >= 2 and
        all(os.path.basename(x) in files for x in meta["distractor_files"]), ", ".join(meta["distractor_files"]))
    row("GATE provenance", set(meta["provenance"]) == set(files), "%d entries" % len(meta["provenance"]))
    row("GATE deliverables", sorted(os.listdir(golden_dir)) == sorted(K.DELIVERABLES), ", ".join(K.DELIVERABLES))

    # ------------------------------------------------------------------ the call
    truth = tuple(c for c in K.WARD if W.truth[c] < K.BENCHMARK / 100.0)
    row("CALL golden set", gold == ("AMU", "ESSU", "4A", "7A", "9B"), ", ".join(gold))
    row("CALL the world's truth names it", truth == gold, ", ".join(truth))
    row("CALL under the cap", len(gold) <= K.MAX_COACHES, "%d of %d" % (len(gold), K.MAX_COACHES))
    est = res["est"]
    row("CALL golden margins", max(est[c] for c in gold) < 0.78 and min(est[c] for c in K.WARD if c not in gold) > 0.83,
        "inside max %.2f, outside min %.2f" % (100 * max(est[c] for c in gold),
                                              100 * min(est[c] for c in K.WARD if c not in gold)))
    fam = A.family(F)
    sets = collections.Counter(below(v) for v in fam.values())
    row("FAMILY one set across %d members" % len(fam), set(sets) == {gold}, str(dict(sets)))
    filed = [v for k, v in fam.items() if not (k[0] == "bands" and k[3] == "worked")]
    ins = max(v[c] for v in filed for c in gold)
    ins_w = max(v[c] for v in fam.values() for c in gold)
    outs = min(v[c] for v in fam.values() for c in K.WARD if c not in gold)
    row("FAMILY margins", ins < 0.79 and ins_w < 0.797 and outs > 0.81,
        "inside max %.2f (worked-hour weights %.2f), outside min %.2f" % (100 * ins, 100 * ins_w, 100 * outs))
    dv, dp = A.deviance(F, "v"), A.deviance(F, "ppn")
    row("FAMILY the data prefers required care over worked hours to patients per worked hour", dv < dp - 50,
        "deviance %.1f against %.1f" % (dv, dp))

    # ------------------------------------------------------------------ the rungs
    rung = res["rungs"]
    row("RUNG Rp (patients per worked hour) files another set", below(rung["Rp"]) != gold,
        "%s" % ", ".join(below(rung["Rp"])))
    for k in ("R0", "R0d", "R1", "Rm", "Rq", "Rn"):
        row("RUNG %s files 9B alone" % k, below(rung[k]) == ("9B",),
            "%s; lowest other ward %.1f" % (", ".join(below(rung[k])), 100 * min(rung[k][c] for c in K.WARD if c != "9B")))
    # ------------------------------------------------------------------ R1 the field's raw material
    heads = {f: open(os.path.join(target, f), encoding="utf-8").readline().strip().lower()
             for f in files if f.endswith(".csv")}
    bad = [f for f, h in heads.items() if re.search(r"complian|shortfall|\bratio\b|nhppd|variance", h)]
    row("R1 no shipped column holds compliance or a shortfall", not bad, ", ".join(bad) or "none")
    row("R1 the decisive step reads the audits, the acuity extract and the roster",
        len(F["sess"]) > 1000 and F["shifts"]["req"].gt(0).all() and F["shifts"]["worked"].gt(0).all(),
        "%d audited day sessions over %d ward-shifts" % (len(F["sess"]), len(F["shifts"])))
    # ------------------------------------------------------------------ R2 every mess item neutral
    d, m = F["d"], F["m"]

    def call_of(**kw):
        Fv = A.frames(target, d=d, m=kw.pop("m", m), **kw)
        return below(A.carried(Fv))
    m_s1a = dict(m)
    m_s1a["ward"] = dict(m["ward"], **{K.MOVED[1]: K.MOVED[1]})
    m_s1a["dept"] = {k: (K.MOVED[1] if k.startswith(K.MOVED[1]) else v) for k, v in m["dept"].items()}
    for label, kw in (("S1A read as its own ward", dict(m=m_s1a)),
                      ("supernumerary shifts counted as worked hours", dict(supernumerary=True)),
                      ("escalation spaces left out of the care hours", dict(escalation=False)),
                      ("night sessions read as day sessions", dict(night=True))):
        got = call_of(**kw)
        row("R2 %s" % label, got == gold, ", ".join(got))
    wa = F["ward_audits"]
    row("R2 no ward session begins in a shift overlap", int((wa["shift"] == "overlap").sum()) == 0,
        "%d moments" % int((wa["shift"] == "overlap").sum()))
    sess_, sh_ = F["sess"], F["shifts"]
    # ------------------------------------------------------------------ R3 the analyst test on the clean truth
    clean = {}
    for c in K.WARD:
        num = den = 0.0
        for s in ("AM", "PM"):
            ss = [x for x in W.sessions if x["ward"] == c and x["shift"] == s]
            rate = sum(x["c"] for x in ss) / sum(x["m"] for x in ss)
            wgt = sum(W.shifts[(c, dd, s)]["req"] for dd in K.DAYS)
            num += rate * wgt
            den += wgt
        clean[c] = num / den
    row("R3a ANALYST the easy route on the clean truth files 9B alone", below(clean) == ("9B",),
        ", ".join(below(clean)))
    row("R3b DECISIVE the decisive step alone files the golden", below(A.carried(F)) == gold, ", ".join(gold))
    row("R3b each lower rung's single correction stays wrong",
        all(below(rung[k]) != gold for k in ("R0", "R0d", "R1", "Rm", "Rp", "Rq", "Rn")), "R0, R0d, R1, Rm, Rp, Rq, Rn")
    aud_req = {c: float((sess_[sess_["ward"] == c]["req"] * sess_[sess_["ward"] == c]["m"]).sum() /
                        sess_[sess_["ward"] == c]["m"].sum() / sh_[sh_["ward"] == c]["req"].mean()) for c in K.WARD}
    row("R3b the audited shifts' care hours sit within 5 per cent of every shift's on every ward",
        all(0.95 < v < 1.05 for v in aud_req.values()),
        "%.3f to %.3f" % (min(aud_req.values()), max(aud_req.values())))
    row("R3c no plant: no shipped figure states a ward's compliance", not bad and not any(
        "complian" in open(os.path.join(target, f), encoding="utf-8", errors="ignore").read().lower()
        for f in files if f.endswith((".csv", ".txt"))), "csv and txt swept")

    # ------------------------------------------------------------------ semantic forks
    row("SF1 ward: S1A is 6A from 2 February 2026", call_of(m=m_s1a) == gold, "same call either way")
    row("SF2 AM and PM shifts: night sessions excluded", call_of(night=True) == gold, "same call")
    sh = F["shifts"]
    row("SF3 audit year 1 July 2025 to 30 June 2026",
        sh["date"].min() == K.YEAR_START and sh["date"].max() == K.YEAR_END, "terms 2.1 files the dates")
    wsets = {wt: below(A.carried(F, weight=wt)) for wt in ("req", "shift", "worked")}
    row("SF4 moments weighted by required care hours (terms 2.2); shifts or worked hours give the same call",
        set(wsets.values()) == {gold}, str(wsets))
    rub_only = {}
    for c in K.WARD:
        x = wa[(wa["ward"] == c) & wa["shift"].isin(["AM", "PM"])]
        rub_only[c] = float((x["action"] == "Hand rub").mean())
    row("SF5 performed is hand rub or hand wash (terms 2.3); hand rub alone files another set",
        below(rub_only) != gold, ", ".join(below(rub_only)))
    row("SF6 fewer than 80 per cent: no ward within a point of the line in the family",
        ins < 0.79 and outs > 0.81, "inside max %.2f, outside min %.2f" % (100 * ins, 100 * outs))
    row("SF7 a session's shift is the roster shift it began in; no session in an overlap",
        int((wa["shift"] == "overlap").sum()) == 0, "AM 07:00 to 15:30, PM 13:00 to 21:30")
    row("SF8 worked hours leave out supernumerary shifts (extract notes); counted, the same call",
        call_of(supernumerary=True) == gold, "same call")
    row("SF9 escalation spaces carry care hours like any bed (extract notes); left out, the same call",
        call_of(escalation=False) == gold, "same call")
    row("SF10 at most six coaches: the cap does not bind", len(gold) <= 6, "%d funded" % len(gold))
    ties = 0
    for c_ in np.arange(0.5, 2.01, 0.05):
        ties += int((abs(sh["req"] * 10 - np.round(c_ * sh["worked"] * 10)) < 1e-6).sum())
    row("SF11 no ward-shift sits on a band edge", ties == 0, "%d shifts" % ties)

    # ------------------------------------------------------------------ components and their rounding edges
    comp = fig["components"]
    sess = F["sess"]
    shrt = sh["req"] > 1.1 * sh["worked"]
    ss = sess["req"] > 1.1 * sess["worked"]
    raw = dict(care=100 * sh.loc[shrt, "req"].sum() / sh["req"].sum(), mom=100 * sess.loc[ss, "m"].sum() / sess["m"].sum(),
               cs=100 * sess.loc[ss, "c"].sum() / sess.loc[ss, "m"].sum(),
               co=100 * sess.loc[~ss, "c"].sum() / sess.loc[~ss, "m"].sum())
    for k, v in raw.items():
        row("EDGE component %s" % k, edge(v, 0.1) > 0.003, "%.4f, edge %.4f" % (v, edge(v, 0.1)))
    for c in K.WARD:
        v = 100 * rung["R0d"][c]
        if c == "9B" or abs(v - comp["audits_lowest_other_ward"]) < 0.06:
            row("EDGE audits as they stand %s" % c, edge(v, 0.1) > 0.003, "%.4f" % v)

    # ------------------------------------------------------------------ separation
    row("SEP the call reads no file of either ask", True, "audits, acuity, roster and the reference workbook only")
    row("SEP no ask device row is a ward day session or a ward-shift", True,
        "devices in the laboratory, admissions, transfers, rounds and issues files (hand rub and hand soap)")

    # ------------------------------------------------------------------ Ask A
    ga = res["asks"]["A"]
    st = AK.stops(target)
    row("ASKA every ward has an episode", all(ga["n"][c] > 0 for c in K.WARD), str(ga["n"]))
    for k in ("A_request_location", "A_every_culture", "A_commensal_single"):
        moved = [c for c in K.WARD if st[k]["n"][c] != ga["n"][c] and st[k]["rate"][c] != ga["rate"][c]]
        row("ASKA %s moves every count and rate" % k, len(moved) == 14, "%d of 14" % len(moved))
    for k in ("A_episodes_within_each_admission", "A_episodes_within_each_stay", "A_each_admission_its_own_stay",
              "A_admissions_a_day_apart_joined"):
        moved = [c for c in K.WARD if st[k]["n"][c] != ga["n"][c] and st[k]["rate"][c] != ga["rate"][c]]
        row("ASKA %s moves every count and rate" % k, len(moved) == 14, "%d of 14" % len(moved))
    # fairness: a stay's admissions meet at the same minute, and no patient came back within three hours of going home
    ad = d["admissions"].assign(a=lambda x: pd.to_datetime(x["admitted"], format="%d/%m/%Y %H:%M"),
                                s=lambda x: pd.to_datetime(x["separated"], format="%d/%m/%Y %H:%M")).sort_values(["mrn", "a"])
    gaps = []
    for _, g in ad.groupby("mrn"):
        gaps += [(a - s).total_seconds() / 3600.0 for s, a in zip(g["s"].iloc[:-1], g["a"].iloc[1:])]
    gaps = np.array(gaps)
    row("ASKA a stay's admissions meet at the minute; no return inside three hours",
        ((gaps == 0) | (gaps >= 3)).all() and (gaps == 0).sum() >= 14 and ((gaps > 0) & (gaps < 24)).sum() >= 14,
        "%d joined at the minute, %d back within a day, %d later" % ((gaps == 0).sum(), ((gaps > 0) & (gaps < 24)).sum(),
                                                                    (gaps >= 24).sum()))
    moved = [c for c in K.WARD if st["A_retired_numbers_dropped"]["n"][c] != ga["n"][c]]
    row("ASKA retired record numbers left unlinked move counts", len(moved) >= 5, ", ".join(moved))
    row("ASKA S1A unmapped moves 6A", st["A_s1a_unmapped"]["n"]["6A"] != ga["n"]["6A"], "")
    # fairness: every retired-number culture links to exactly one admission by date of birth and sex
    iso, adm = AK._isolates(d, m, link_retired=True)
    unl = iso[(~iso["mrn"].isin(adm["mrn"])) & iso["location"].str.startswith("AVH-") &
              ~iso["location"].isin(["AVH-ED", "AVH-OPC", "AVH-RDU"])]
    row("ASKA every retired-number ward culture links once", unl["admission_no"].notna().all() and len(unl) >= 10,
        "%d cultures" % len(unl))
    for c in K.WARD:
        v = ga["n"][c] / ga["bed_days"][c] * 10000.0
        row("EDGE HOBSI rate %s" % c, edge(v, 0.1) > 0.002, "%.4f" % v)
    # ------------------------------------------------------------------ Ask B
    gb = res["asks"]["B"]
    for k in ("B_copies_kept", "B_one_refill_a_day", "B_same_minute_all_year", "B_returns_left_out"):
        moved = [c for c in K.WARD if st[k]["litres"][c] != gb["litres"][c] and st[k]["rate"][c] != gb["rate"][c]]
        row("ASKB %s moves every litre and rate" % k, len(moved) == 14, "%d of 14" % len(moved))
    rounds = pd.read_csv(os.path.join(target, K.FILES["rounds"]), dtype=str)
    copies = AK.resent_records(rounds)
    rr = rounds.assign(t=pd.to_datetime(rounds["fitted"], format="%d/%m/%Y %H:%M"))
    gen = collections.Counter((did, t) for did, t, f, kind in S.refills if kind == "resend")
    found = collections.Counter((x["dispenser_id"], x["t"].to_pydatetime()) for _, x in rr[rr["record_id"].isin(copies)].iterrows())
    row("ASKB the re-sent records found are exactly the re-sends", found == gen, "%d records" % len(copies))
    # fairness: outside a copy, a dispenser repeats a minute of the day only more than thirty days apart, and every
    # ward's hand rub and soap dispensers hold such a pair (the whole-year key takes them with the copies)
    own = rr[~rr["record_id"].isin(copies)].copy()
    own["hm"] = own["t"].dt.strftime("%H:%M")
    own["day"] = own["t"].dt.normalize()
    gaps = own.sort_values("t").groupby(["dispenser_id", "hm"])["day"].diff().dropna().dt.days
    row("ASKB a dispenser's minute repeats only weeks apart outside a copy", (gaps > 30).all() and len(gaps) >= 28,
        "%d genuine repeats, shortest %d days" % (len(gaps), gaps.min() if len(gaps) else -1))
    for c in K.WARD:
        v = (gb["bottles"].get(c, 0.0) + gb["wall"].get(c, 0)) / gb["bed_days"][c] * 1000.0
        row("EDGE hand rub rate %s" % c, edge(v, 0.1) > 0.002, "%.4f" % v)
    # ------------------------------------------------------------------ Ask C
    gs = res["asks"]["C"]
    for k in ("C_job_quantity_summed", "C_copies_kept_and_quantity_summed", "C_cartridge_as_a_litre"):
        moved = [c for c in K.WARD if st[k]["litres"][c] != gs["litres"][c] and st[k]["rate"][c] != gs["rate"][c]]
        row("ASKC %s moves every litre and rate" % k, len(moved) == 14, "%d of 14" % len(moved))
    for k in ("C_copies_kept", "C_same_minute_all_year"):
        moved = [c for c in K.WARD if st[k]["litres"][c] != gs["litres"][c]]
        row("ASKC %s (the shared hazard) moves every ward's litres" % k, len(moved) == 14, "%d of 14" % len(moved))
    # fairness: a job's records each carry the job's cartridges, one record a cartridge; every other record is one
    own = rounds[~rounds["record_id"].isin(copies)]
    jl = own[own["job_no"].fillna("") != ""]
    per_job = jl.groupby("job_no").agg(n=("record_id", "size"), q=("quantity", lambda q: set(q.astype(int))))
    disp_kind = dict(zip(d["dispensers"]["dispenser_id"], d["dispensers"]["type"]))
    row("ASKC every job's records carry the job's cartridges", all(v["q"] == {v["n"]} for _, v in per_job.iterrows())
        and (per_job["n"] >= 2).all() and (jl["dispenser_id"].map(disp_kind) == "Hand soap").all(),
        "%d jobs, %d records" % (len(per_job), len(jl)))
    row("ASKC every record outside a job is one", (own.loc[own["job_no"].fillna("") == "", "quantity"].astype(int) == 1).all(),
        "")
    row("ASKC S1A unmapped moves 6A", st["C_s1a_unmapped"]["litres"]["6A"] != gs["litres"]["6A"], "")
    for c in K.WARD:
        v = (gs["bottles"].get(c, 0.0) + 0.8 * gs["wall"].get(c, 0)) / gs["bed_days"][c] * 1000.0
        row("EDGE hand soap rate %s" % c, edge(v, 0.1) > 0.002, "%.4f" % v)

    # ------------------------------------------------------------------ realism and containers
    a = pd.read_csv(os.path.join(target, K.FILES["audits"]), dtype=str)
    per = a.groupby("department")["session_id"].nunique()
    row("REAL session counts vary by ward and area", per.nunique() >= 0.6 * len(per), "%d distinct of %d" % (per.nunique(), len(per)))
    row("REAL every record before the pack's assembly", _dates_ok(target), "")
    row("REAL no em or en dash in any shipped text", _no_dash(target), "")
    row("CONTAINER no writer signature", _scrubbed(target, golden_dir), "")
    fails = [r for r in ROWS if not r[1]]
    for label, ok, detail in ROWS:
        print("%s  %-70s %s" % ("PASS" if ok else "FAIL", label[:70], detail[:110]))
    print("checks: %d run, %d failed" % (len(ROWS), len(fails)))
    return 1 if fails else 0


def _dates_ok(target):
    lim = K.ASSEMBLED
    pat = re.compile(r"\b(\d{2})/(\d{2})/(\d{4})\b|\b(\d{4})-(\d{2})-(\d{2})\b")
    for f in os.listdir(target):
        if not f.endswith((".csv", ".txt")):
            continue
        txt = open(os.path.join(target, f), encoding="utf-8").read()
        for mm in pat.finditer(txt):
            if mm.group(1):
                d = dt.datetime(int(mm.group(3)), int(mm.group(2)), int(mm.group(1)))
            else:
                d = dt.datetime(int(mm.group(4)), int(mm.group(5)), int(mm.group(6)))
            if d > lim:
                return False
    return True


def _no_dash(target):
    for f in os.listdir(target):
        if f.endswith((".csv", ".txt")):
            t = open(os.path.join(target, f), encoding="utf-8").read()
            if "—" in t or "–" in t:
                return False
    return True


def _scrubbed(target, golden):
    for folder in (target, golden):
        for f in os.listdir(folder):
            p = os.path.join(folder, f)
            raw = open(p, "rb").read()
            if f.endswith(".pdf") and (b"ReportLab" in raw or b"reportlab" in raw):
                return False
            if f.endswith(".png") and (b"matplotlib" in raw.lower() or b"Software" in raw):
                return False
            if f.endswith(".xlsx"):
                with zipfile.ZipFile(p) as z:
                    for n in z.namelist():
                        if n.startswith("docProps/") and b"openpyxl" in z.read(n):
                            return False
    return True
