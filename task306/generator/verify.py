"""An independent verifier: pandas over target/ only, written apart from analysis.py, recomputing the call, every
graded figure and both asks, and comparing them with figures.json.

    python3 task306/generator/verify.py
"""
import json
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
read = lambda n, **k: pd.read_csv(os.path.join(T, n), dtype=str, keep_default_na=False, **k)

CLASS_WORDS = {"A": ("risperidone", "quetiapine", "haloperidol", "olanzapine"),
               "B": ("diazepam", "temazepam", "lorazepam", "zopiclone", "zolpidem"),
               "C": ("pregabalin", "gabapentin"),
               "O": ("codeine", "co-codamol", "tramadol", "morphine", "oxycodone", "buprenorphine")}
KEY = {"A": "AP", "B": "BZ", "C": "GB"}


def kind(text):
    t = text.lower()
    if t.startswith("clobazam"):
        return "X"
    for k, ws in CLASS_WORDS.items():
        if any(t.startswith(w) for w in ws):
            return k
    return None


def mentions(text):
    t = text.lower()
    for k in ("A", "B", "C"):
        for w in CLASS_WORDS[k] + (("clobazam",) if k == "B" else ()):
            if re.search(r"\b%s\b" % w, t):
                return k
    return None


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    spec_rows = {}
    from pypdf import PdfReader
    spec = "\n".join(p.extract_text() for p in PdfReader(os.path.join(T, "medicines_safety_programme_2027.pdf")).pages)
    for band in ("18 to 64", "65 to 74", "75 to 84", "85 and over"):
        m = re.search(re.escape(band) + r"\s+(not in scope|[\d.]+)\s+(not in scope|[\d.]+)\s+([\d.]+)", spec)
        spec_rows[band] = [None if x == "not in scope" else float(x) for x in m.groups()]
    harm = {k: {b: v[i] for b, v in spec_rows.items() if v[i] is not None} for i, k in enumerate("ABC")}

    reg = read("member_practice_register_2026.csv")
    pcn = dict(zip(reg.ods_code, reg.primary_care_network))
    R = pd.read_parquet(os.path.join(T, "patient_registrations_2020-2026.parquet"))
    end = pd.to_datetime(R.registration_end)
    start = pd.to_datetime(R.registration_start)
    dod = pd.to_datetime(R.date_of_death)
    day = pd.Timestamp("2026-12-31")
    cur = R[(start <= day) & (end.isna() | (end > day)) & (dod.isna() | (dod > day))]
    cur = cur[cur.practice_code.map(pcn).notna() & (cur.practice_code.map(pcn) != "Clun Valley PCN")]
    age = dict(zip(cur.patient_pseudonym, 2026 - cur.birth_month.str[:4].astype(int)))
    iss = pd.read_parquet(os.path.join(T, "prescribing_issues_2025-07_2026-12.parquet"))
    iss["k"] = iss.medicine.map(kind)
    d = pd.to_datetime(iss.issue_date)
    w = iss[(d >= "2026-07-01") & (d <= "2026-12-31")]
    n = w.groupby(["patient_pseudonym", "k"]).size()
    prob = read("problem_list_extract_2026-12-31.csv")
    codes = prob.groupby("patient_pseudonym").snomed_code.apply(set).to_dict()
    pal, smi, epi = "1129481000000101", {"69322001", "58214004", "13746004"}, "84757009"
    scope = {"A": [], "B": [], "C": []}
    for p, a in age.items():
        cs = codes.get(p, set())
        if pal in cs:
            continue
        if a >= 65 and n.get((p, "A"), 0) >= 2 and not (cs & smi):
            scope["A"].append(p)
        if a >= 65 and n.get((p, "B"), 0) >= 3:
            scope["B"].append(p)
        if a >= 18 and n.get((p, "C"), 0) >= 2 and n.get((p, "O"), 0) >= 2 and epi not in cs:
            scope["C"].append(p)

    # who started the medicine: a class letter in the 60 days before the earliest class course's first issue
    cou = read("repeat_medication_courses_2026-12-31.csv")
    cou["k"] = cou.medicine.map(kind)
    first = cou[cou.k.isin(["A", "B", "C"])].assign(f=lambda x: pd.to_datetime(x.first_issue_date)) \
        .groupby(["patient_pseudonym", "k"]).f.min().to_dict()
    let = read("trust_medicine_letters_feed_2019-2026.csv")
    look = read("trust_hospital_number_lookup.csv")
    hn = dict(zip(zip(look.trust, look.hospital_number), look.patient_pseudonym))
    let["who"] = [p if p else hn.get((s, h), "") for p, s, h in zip(let.patient_pseudonym, let.sender, let.hospital_number)]
    let["when"] = [pd.Timestamp(x) if "-" in x else pd.Timestamp(x[6:] + "-" + x[3:5] + "-" + x[:2])
                   for x in let.letter_date]
    let["k"] = let.medicine_line.map(mentions)
    cl = let[let.k.notna()].groupby(["who", "k"])["when"].apply(list).to_dict()

    def started_by_specialist(p, k):
        f = first.get((p, k))
        return any(f - pd.Timedelta(days=60) <= x < f for x in cl.get((p, k), []))

    log = read("deprescribing_pilot_outcome_log_2026.csv")
    six = log[log.record_type == "Six-month follow-up"]
    lab = {"Antipsychotics 65+": "A", "Benzodiazepines and Z-drugs 65+": "B", "Gabapentinoid with opioid": "C"}
    rate = {}
    for k in "ABC":
        s = six[six.review.map(lab) == k]
        sp = s.patient_pseudonym.map(lambda p: started_by_specialist(p, k))
        off = s.outcome == "Off medicine"
        rate[(k, True)] = off[sp].mean()
        rate[(k, False)] = off[~sp].mean()
    out = {}
    for k in "ABC":
        tot_off = tot_h = 0.0
        for p in scope[k]:
            ch = rate[(k, started_by_specialist(p, k))]
            a = age[p]
            b = "18 to 64" if a < 65 else "65 to 74" if a < 75 else "75 to 84" if a < 85 else "85 and over"
            tot_off += ch
            tot_h += ch * harm[k][b] / 100
        out[k] = (len(scope[k]), tot_off, tot_h)
    order = sorted("ABC", key=lambda k: -out[k][2])
    errs = []
    if KEY[order[0]] != fig["call"] or KEY[order[1]] != fig["runner_up"]:
        errs.append("call %s runner-up %s" % (order[0], order[1]))
    for k in "ABC":
        f = fig["reviews"][KEY[k]]
        if out[k][0] != f["in_scope"] or int(round(out[k][1] / 10)) * 10 != f["off_10"] or int(round(out[k][2])) != f["harms_1"]:
            errs.append("review %s %s against %s" % (k, out[k], f))
    gap = int(round(out[order[0]][2])) - int(round(out[order[1]][2]))
    if gap != fig["gap"]:
        errs.append("gap %d" % gap)

    # ask A: letters received, by the receiving practice's network and the half of first receipt
    wf = read("practice_document_workflow_2026.csv")
    wf["at"] = pd.to_datetime(wf.received)
    letters = let.groupby("letter_reference").agg(sender=("sender", "first"), service=("service", "first"),
                                                  who=("who", "first"), when=("when", "first"),
                                                  enc=("encounter_date", "first"),
                                                  lines=("medicine_line", lambda x: tuple(x))).reset_index()
    got = wf.set_index("sender_reference")
    letters["at"] = letters.letter_reference.map(got["at"])
    letters["prac"] = letters.letter_reference.map(got["practice_code"])
    spare = wf[~wf.sender_reference.isin(set(letters.letter_reference))]
    spare = spare[spare.sender == "Wrekinside Teaching Hospitals NHS Trust"].sort_values("at")
    bucket = {}
    for r in spare.itertuples():
        bucket.setdefault((r.patient_pseudonym, r.sender), []).append((r.at, r.practice_code))
    todo = letters[letters["at"].isna() & (letters.sender == "Wrekinside Teaching Hospitals NHS Trust")]
    for i in todo.sort_values(["when", "letter_reference"]).index:
        q = bucket.get((letters.at[i, "who"], letters.at[i, "sender"]), [])
        w0 = letters.at[i, "when"]
        for j, (at, pr) in enumerate(q):
            if w0 <= at.normalize() <= w0 + pd.Timedelta(days=21):
                letters.at[i, "at"], letters.at[i, "prac"] = q.pop(j)
                break
    mmh = letters.sender == "Marches Mental Health NHS Trust"
    earlier = letters[mmh & (letters.when < "2026-04-07")]
    seen = dict(zip(zip(earlier.who, earlier.service, earlier.enc, earlier.lines), earlier.letter_reference))
    letters["one"] = letters.letter_reference
    resent = mmh & (letters.when == "2026-04-07")
    letters.loc[resent, "one"] = [seen.get(k, r) for k, r in zip(zip(letters[resent].who, letters[resent].service,
                                                                      letters[resent].enc, letters[resent].lines),
                                                                  letters[resent].letter_reference)]
    firsts = letters.dropna(subset=["at"]).sort_values("at").groupby("one").first()
    firsts = firsts[(firsts["at"] >= "2026-01-01") & (firsts["at"] < "2027-01-01")]
    firsts["net"] = firsts.prac.map(pcn)
    firsts["half"] = np.where(firsts["at"] < "2026-07-01", "H1", "H2")
    lists = pd.read_csv(os.path.join(T, "registered_list_sizes_2026.csv"), dtype={"practice_code": str})
    lists["net"] = lists.practice_code.map(pcn)
    den = lists.groupby(["net", "extract_date"]).registered_patients.sum()
    cnt = firsts.groupby(["net", "half"]).size()
    for net_ in sorted(set(pcn.values())):
        for h, dd in (("H1", "2026-01-01"), ("H2", "2026-07-01")):
            v = round(1000 * cnt.get((net_, h), 0) / den[(net_, dd)] + 1e-9, 1)
            if abs(v - fig["letters"][net_][h]["rate"]) > 1e-9:
                errs.append("letters %s %s %.1f against %.1f" % (net_, h, v, fig["letters"][net_][h]["rate"]))

    # ask B: consultations
    hub = read("pharmacist_hub_appointments_2026.csv")
    t_utc = pd.to_datetime(hub.slot_start_utc.str[:19])
    summer = (t_utc >= "2026-03-29 01:00") & (t_utc < "2026-10-25 01:00")
    hub["day"] = (t_utc + pd.to_timedelta(summer.astype(int), unit="h")).dt.normalize()
    one = hub[(hub.patient_pseudonym != "") & (hub.outcome == "Attended")]
    act = read("clinical_system_pharmacist_activity_2026.csv")
    act["day"] = pd.to_datetime(act.consultation_date)
    hol = {pd.Timestamp(x) for x in ("2026-04-03", "2026-04-06", "2026-05-04", "2026-05-25", "2026-08-31",
                                     "2026-12-25", "2026-12-28")}

    def nxt(x):
        x = x + pd.Timedelta(days=1)
        while x.weekday() >= 5 or x in hol:
            x += pd.Timedelta(days=1)
        return x
    rows_by = act.groupby(["patient_pseudonym", "clinician"]).groups
    used = set()
    for r in one.itertuples():
        for j in rows_by.get((r.patient_pseudonym, r.pharmacist), []):
            if j not in used and r.day <= act.at[j, "day"] <= nxt(r.day):
                used.add(j)
                break
    grp = pd.read_excel(os.path.join(T, "hub_group_session_register_2026.xlsx"), dtype=str)
    grp = grp[grp.Attended == "Yes"]
    reg_rows = R[R.practice_code.map(pcn).notna()]
    spells = {}
    for p, a, b, c in zip(reg_rows.patient_pseudonym, pd.to_datetime(reg_rows.registration_start),
                          pd.to_datetime(reg_rows.registration_end), reg_rows.practice_code):
        spells.setdefault(p, []).append((a, b, c))
    succ = dict(zip(reg.ods_code, reg.successor_ods_code))

    def net_on(p, x):
        for a, b, c in spells.get(p, []):
            if a <= x and (pd.isna(b) or x < b):
                return pcn[succ.get(c) or c]
    recs = [(pcn[c], x) for c, x, j in zip(act.practice_code, act.day, act.index) if j not in used]
    recs += [(net_on(p, x), x) for p, x in zip(one.patient_pseudonym, one.day)]
    recs += [(net_on(p, pd.Timestamp(x)), pd.Timestamp(x)) for p, x in zip(grp.Patient, grp.Date)]
    cdf = pd.DataFrame(recs, columns=["net", "day"])
    cdf["q"] = "Q" + cdf.day.dt.quarter.astype(str)
    cc = cdf.groupby(["net", "q"]).size()
    for net_ in sorted(set(pcn.values())):
        for q, dd in (("Q1", "2026-01-01"), ("Q2", "2026-04-01"), ("Q3", "2026-07-01"), ("Q4", "2026-10-01")):
            v = round(1000 * cc.get((net_, q), 0) / den[(net_, dd)] + 1e-9, 1)
            if abs(v - fig["consultations"][net_][q]["rate"]) > 1e-9:
                errs.append("consultations %s %s %.1f against %.1f" % (net_, q, v,
                                                                       fig["consultations"][net_][q]["rate"]))
    golden = pd.read_csv(os.path.join(TASK, "golden", "pharmacist_consultations_2026.csv"))
    for r in golden.itertuples():
        if abs(r.consultations_per_1000 - fig["consultations"][r.primary_care_network][r.quarter[-2:]]["rate"]) > 1e-9:
            errs.append("golden csv %s %s" % (r.primary_care_network, r.quarter))
    print("verify: call %s, runner-up %s, gap %d; reviews %s" % (KEY[order[0]], KEY[order[1]], gap,
                                                                {KEY[k]: (v[0], round(v[1], 2), round(v[2], 3))
                                                                 for k, v in out.items()}))
    for e in errs:
        print("MISMATCH", e)
    print("verify:", "PASS" if not errs else "FAIL (%d)" % len(errs))
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
