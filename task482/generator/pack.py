"""Cut task482's pack (architecture 14) from the world's truth: each payer's October feed in its own layout (claims,
eligibility, attribution runs, care coordination remittances), the network's clinician roster and master patient
index, the payers' 2026 E&M fee schedules, the qualifying services code list and two out-of-scope files."""
import csv
import datetime as dt
import io
import json
import math

import numpy as np
import openpyxl
from openpyxl.styles import Font

import world as W

D = dt.date
FEED_DATE = {"B": D(2026, 10, 7), "M": D(2026, 10, 9), "T": D(2026, 10, 12)}
PAYER_ABBR = {"B": "MLH", "M": "KBP", "T": "PMH"}


def _csv(path, header, rows, delim=",", crlf=True):
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=delim, lineterminator="\r\n" if crlf else "\n")
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())


def shared_rows(w, ids):
    """The claims each payer shares under the data agreement: 2025 claims (paid through the feed date) of the members on
    its final 2025 attribution, and 2026 claims incurred through September and paid by 30 September of the members on its
    October 2026 run. Returns {payer: [claim index]}, {payer: {pid}} for each year."""
    col, att = w["claims"], w["att"]
    members = {(p, 2025): set(att[("final", p, 2025)]) for p in W.PAYERS}
    members.update({(p, 2026): set(att[("run", p, 10)]) for p in W.PAYERS})
    out = {p: [] for p in W.PAYERS}
    pay, yr, pid, svc, paid = col["payer"], col["year"], col["pid"], col["svc"], col["paid"]
    for i in range(len(pid)):
        p, y = pay[i], yr[i]
        if pid[i] not in members[(p, y)]:
            continue
        if paid[i] > W.FEED_PAID:
            continue
        if y == 2026 and svc[i] > D(2026, 9, 30):
            continue
        out[p].append(i)
    return out, members


def versions(w, idx, payer):
    """Adjusted claims: a small share of each payer's claims were reprocessed after first payment. Returns rows of
    (claim index, version tag, allowed, paid date) where the final allowed equals the world's allowed."""
    col = w["claims"]
    g = W.rng(41, W.PAYERS.index(payer))
    out = []
    for i in idx:
        if col["ctype"][i] in ("PROF", "OUTPT", "INPT") and g.random() < 0.013:
            first = round(col["allowed"][i] * float(g.choice([0.82, 0.9, 1.08, 1.15])), 2)
            later = col["paid"][i] + dt.timedelta(days=int(g.integers(18, 75)))
            if later > W.FEED_PAID:
                out.append((i, "orig", col["allowed"][i], col["paid"][i]))
                continue
            out.append((i, "first", first, col["paid"][i]))
            out.append((i, "adjusted", col["allowed"][i], later))
        else:
            out.append((i, "orig", col["allowed"][i], col["paid"][i]))
    return out


CTYPE = {"B": {"PROF": "PROF", "OUTPT": "OUTP", "INPT": "INPT", "RX": "PHRM"},
         "M": {"PROF": "1500", "OUTPT": "UB04", "INPT": "UB04", "RX": "NCPDP"},
         "T": {"PROF": "professional", "OUTPT": "institutional_outpatient", "INPT": "institutional_inpatient", "RX": "pharmacy"}}


def mlh_icns(w, vs):
    """Merrinlake's internal control numbers: region, two-digit year and Julian day of receipt, then the day's running
    count; a pharmacy claim is received the day it is filled, any other a few days before its first payment and never
    before its last day of service, and a void and its replacement are numbered on the day before the reprocessed
    payment."""
    col = w["claims"]
    want = []
    for (i, tag, amt, paid) in vs:
        cid = int(col["cid"][i])
        if tag in ("orig", "first"):
            got = paid if col["ctype"][i] == "RX" else max(col["end"][i], paid - dt.timedelta(days=2 + cid % 7))
            want.append((got, cid, "A"))
        else:
            want.append((paid - dt.timedelta(days=1), cid, "V"))
            want.append((paid - dt.timedelta(days=1), cid, "R"))
    out, count = {}, {}
    for day, cid, kind in sorted(want):
        n = count.get(day, 10000 + (day.toordinal() * 37) % 900) + 1 + cid % 3
        count[day] = n
        out[(cid, kind)] = "4%02d%03d%07d" % (day.year % 100, day.timetuple().tm_yday, n)
    return out


def claims_mlh(path, w, ids, idx):
    col = w["claims"]
    rows = []
    first_amt = {}
    vs = versions(w, idx, "B")
    icn = mlh_icns(w, vs)
    for (i, tag, amt, paid) in vs:
        cid = int(col["cid"][i])
        base = icn[(cid, "A")]
        common = [ids[(col["pid"][i], "B")], CTYPE["B"][col["ctype"][i]], col["svc"][i].isoformat(), col["end"][i].isoformat()]
        tail = [col["code"][i], col["mod"][i], col["pos"][i], col["rev"][i], col["ndc"][i], col["npi"][i]]
        days = col["days"][i] if col["ctype"][i] == "RX" else ""
        if tag == "orig":
            rows.append([base] + common + [paid.isoformat()] + tail + ["%.2f" % amt, days, "", ""])
        elif tag == "first":
            first_amt[base] = "%.2f" % amt
            rows.append([base] + common + [paid.isoformat()] + tail + ["%.2f" % amt, days, "", ""])
        else:
            rows.append([icn[(cid, "V")]] + common + [paid.isoformat()] + tail + ["-" + first_amt[base], days, "VOID", base])
            rows.append([icn[(cid, "R")]] + common + [paid.isoformat()] + tail + ["%.2f" % amt, days, "REPL", base])
    rows.sort(key=lambda r: (r[5], r[0]))
    _csv(path, ["CLM_ID", "MBR_ID", "CLM_TYP", "SVC_FROM_DT", "SVC_THRU_DT", "PD_DT", "PROC_CD", "PROC_MOD", "POS_CD", "REV_CD",
                "NDC_11", "REND_NPI", "ALLOWED_AMT", "DAYS_SUPPLY", "ADJ_TYP", "ORIG_CLM_ID"], rows)
    return len(rows)


def kbp_split(w, i, amt):
    """Kesselcrest's claim lines for one current claim: the service line, and where Kesselcrest adjusts at the claim, a
    line with no procedure or revenue code carrying the adjustment. A level 5 visit its level review paid at the level 4
    rate keeps the code's rate on its line, the difference on the claim; an outpatient facility claim its case rate cut
    carries the cut the same way. Returns [(cents, is_adjustment)], summing to the claim's allowed."""
    col = w["claims"]
    cents = int(round(amt * 100))
    ct, code, pos = col["ctype"][i], col["code"][i], col["pos"][i]
    if ct == "PROF" and code == "99215" and col["year"][i] == 2026:
        f = W.FEES[("M", 2026)]
        rate = f["fa"] if pos in ("19", "22") else f["nf"]
        if abs(amt - rate[3]) < 0.005:
            full = int(round(rate[4] * 100))
            return [(full, False), (cents - full, True)]
    if ct == "OUTPT":
        g = W.rng(46, col["cid"][i] % 100003)
        if g.random() < 0.075:
            cut = int(round(cents * float(g.uniform(0.06, 0.31))))
            return [(cents + cut, False), (-cut, True)]
    return [(cents, False)]


def receipt_numbers(w, vs, fmt, step):
    """A payer's claim numbers in the order its claims were first paid, each year's count running on from a base with
    the gaps of claims numbered and never paid to the partner."""
    col = w["claims"]
    first = {}
    for (i, tag, amt, paid) in vs:
        if tag in ("orig", "first"):
            first[int(col["cid"][i])] = paid
    out, n = {}, {}
    for cid, paid in sorted(first.items(), key=lambda kv: (kv[1], kv[0])):
        n[paid.year] = n.get(paid.year, 0) + 1 + cid % step
        out[cid] = fmt(paid.year, n[paid.year])
    return out


def claims_kbp(path, w, ids, idx):
    col = w["claims"]
    rows = []
    vs = versions(w, idx, "M")
    num_of = receipt_numbers(w, vs, lambda y, k: "E%02d%08d" % (y % 100, 41000000 + k), 4)
    for (i, tag, amt, paid) in vs:
        no = num_of[int(col["cid"][i])]
        ct = col["ctype"][i]
        bill = {"INPT": "0111", "OUTPT": "0131"}.get(ct, "")
        line = [ids[(col["pid"][i], "M")], CTYPE["M"][ct], bill, col["svc"][i].strftime("%m/%d/%Y"),
                col["end"][i].strftime("%m/%d/%Y")]
        tail = [col["code"][i], col["mod"][i], col["pos"][i], col["rev"][i], col["ndc"][i], col["npi"][i]]
        cents = int(round(amt * 100))
        if tag == "first":
            rows.append([no, "1"] + line + [paid.strftime("%m/%d/%Y")] + tail + [str(cents), "A"])
            continue
        num = no if tag == "orig" else no + "-01"
        for n, (c, adj) in enumerate(kbp_split(w, i, amt)):
            rows.append([num, str(n + 1)] + line + [paid.strftime("%m/%d/%Y")] + (["", "", "", "", "", ""] if adj else tail) +
                        [str(c), "P"])
    rows.sort(key=lambda r: (r[7][-4:] + r[7][:2] + r[7][3:5], r[0]))
    _csv(path, ["CLAIM_NO", "LINE_NO", "MEMBER_NO", "CLAIM_FORM", "BILL_TYPE", "FIRST_DOS", "LAST_DOS", "PAID_DATE", "PROCEDURE",
                "MODIFIER", "PLACE_OF_SVC", "REVENUE", "NDC", "RENDERING_PROV_NPI", "ALLOWED_CENTS", "CLAIM_STATUS"], rows, delim="|",
         crlf=False)
    return len(rows)


def claims_pmh(path, w, ids, idx):
    col = w["claims"]
    recs = []
    vs = versions(w, idx, "T")
    num_of = receipt_numbers(w, vs, lambda y, k: "C%08X" % ((k * 2654435761 + 0x5BD1E995 * (y - 2024)) % 2 ** 32), 1)
    for (i, tag, amt, paid) in vs:
        ct = col["ctype"][i]
        r = {"claimId": num_of[int(col["cid"][i])], "memberId": ids[(col["pid"][i], "T")], "type": CTYPE["T"][ct],
             "serviceStart": col["svc"][i].isoformat(), "serviceEnd": col["end"][i].isoformat(),
             "adjudicated": paid.isoformat()}
        if ct == "PROF":
            r.update({"cpt": col["code"][i], "pos": col["pos"][i], "renderingNpi": col["npi"][i]})
            if col["mod"][i]:
                r["modifier"] = col["mod"][i]
        elif ct == "RX":
            r.update({"ndc": col["ndc"][i], "daysSupply": col["days"][i]})
        else:
            r.update({"revenueCode": col["rev"][i]})
        if tag == "first":
            r.update({"allowed": round(amt, 2), "version": 1})
        elif tag == "adjusted":
            r.update({"allowed": round(amt, 2), "version": 2})
        else:
            r.update({"allowed": round(amt, 2), "version": 1})
        recs.append(r)
    recs.sort(key=lambda r: (r["adjudicated"], r["claimId"], r["version"]))
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write('{"source":"Pemberglen Mutual Health","extract":"value-based partner claims","partner":"' + W.NETWORK +
                '","runDate":"2026-10-12","records":[\n')
        f.write(",\n".join(json.dumps(r, separators=(",", ":")) for r in recs))
        f.write("\n]}\n")
    return len(recs)


def eligibility(w, ids, members):
    """Coverage spans by payer for the members each payer shares; an October 2026 feed does not know a coverage end
    still to come, so a 2026 span ending after September shows open."""
    ppl = {q.pid: q for q in w["people"]}
    out = {p: [] for p in W.PAYERS}
    for p in W.PAYERS:
        pids = sorted(members[(p, 2025)] | members[(p, 2026)])
        for pid in pids:
            q = ppl[pid]
            spans = []
            for y in W.YEARS:
                if q.payer[y] != p or q.span[y] is None or pid not in members[(p, y)] and not (y == 2025 and pid in members[(p, 2026)]):
                    continue
                s, e = q.span[y]
                start = D(y, s + 1, 1)
                end = D(y, e, W.month_days(y, e))
                if y == 2026 and e > 9:
                    end = None
                spans.append([start, end])
            merged = []
            for sp in spans:
                if merged and merged[-1][1] is not None and (sp[0] - merged[-1][1]).days == 1:
                    merged[-1][1] = sp[1]
                else:
                    merged.append(sp)
            for sp in merged:
                out[p].append((pid, sp[0], sp[1]))
    return out


def eligibility_files(t, w, ids, members):
    ppl = {q.pid: q for q in w["people"]}
    spans = eligibility(w, ids, members)
    g = W.rng(43)
    rows = []
    for pid, s, e in spans["B"]:
        q = ppl[pid]
        mid = ids[(pid, "B")]
        rows.append([mid, mid[:9] + "00", "%02d" % (0 if q.age >= 26 else int(g.integers(2, 5))), q.dob.isoformat(), q.sex,
                     "PPO" if pid % 4 else "HDHP", s.isoformat(), (e or D(9999, 12, 31)).isoformat()])
    _csv(t("mlh_elig"), ["MBR_ID", "SBSCR_ID", "DEP_SFX", "BIRTH_DT", "GNDR", "PROD_CD", "COV_EFF_DT", "COV_TERM_DT"], rows)
    rows = []
    for pid, s, e in spans["M"]:
        q = ppl[pid]
        rows.append([ids[(pid, "M")], "S" + ids[(pid, "M")][1:], "18" if q.age >= 26 else "19", q.dob.strftime("%m/%d/%Y"),
                     q.sex, "G%05d" % (1000 + pid % 380), s.strftime("%m/%d/%Y"), e.strftime("%m/%d/%Y") if e else ""])
    _csv(t("kbp_elig"), ["MEMBER_NO", "SUBSCRIBER_NO", "REL_CD", "DOB", "SEX", "GROUP_NO", "EFF_DATE", "TERM_DATE"], rows,
         delim="|", crlf=False)
    rows = []
    for pid, s, e in spans["T"]:
        q = ppl[pid]
        rows.append([ids[(pid, "T")], q.dob.isoformat(), q.sex, s.isoformat(), e.isoformat() if e else "", "PMH-COMM-" + ("A" if pid % 3 else "B")])
    _csv(t("pmh_members"), ["memberId", "birthDate", "sex", "coverageStart", "coverageEnd", "planCode"], rows)
    return spans


def attribution_files(t, w, ids):
    att = w["att"]
    # Merrinlake: one csv, both runs
    rows = []
    for (run, key, y, rid, rdt) in (("final", ("final", "B", 2025), 2025, "PY2025-F", D(2026, 4, 10)),
                                    ("run", ("run", "B", 10), 2026, "PY2026-10", W.RUN_DATE)):
        for pid, (prac, nd, last) in sorted(att[key].items(), key=lambda kv: ids[(kv[0], "B")]):
            rows.append([ids[(pid, "B")], y, rid, rdt.isoformat(), W.TINS[prac].replace("-", ""), nd, last.isoformat()])
    _csv(t("mlh_attr"), ["MBR_ID", "PERF_YR", "RUN_ID", "RUN_DT", "PRACTICE_TIN", "QUAL_SVC_DAYS", "LAST_QUAL_SVC_DT"], rows)
    # Kesselcrest: a workbook, one sheet per run, with a title block above the header
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for title, key, rdt in (("PY2025 Final", ("final", "M", 2025), D(2026, 4, 14)), ("PY2026 Run 10", ("run", "M", 10), W.RUN_DATE)):
        ws = wb.create_sheet(title)
        ws.append(["Kesselcrest Benefit Partners  |  Value-Based Partner Attribution  |  " + W.NETWORK])
        ws.append(["Run date " + rdt.strftime("%m/%d/%Y")])
        ws.append([])
        ws.append(["Member No", "Attributed TIN", "Practice", "Qualifying Visit Days", "Last Qualifying Visit"])
        ws["A1"].font = Font(bold=True)
        for c in ws[4]:
            c.font = Font(bold=True)
        for pid, (prac, nd, last) in sorted(w["att"][key].items(), key=lambda kv: ids[(kv[0], "M")]):
            ws.append([ids[(pid, "M")], W.TINS[prac], W.PRACTICE_NAMES[prac], nd, last])
            ws.cell(row=ws.max_row, column=5).number_format = "mm/dd/yyyy"
        ws.column_dimensions["A"].width = 14
        ws.column_dimensions["B"].width = 14
        ws.column_dimensions["C"].width = 32
        ws.column_dimensions["D"].width = 20
        ws.column_dimensions["E"].width = 20
        ws.freeze_panes = "A5"
    wb.save(t("kbp_attr"))
    # Pemberglen: a csv, both years
    rows = []
    for (py, key, run) in ((2025, ("final", "T", 2025), "FINAL"), (2026, ("run", "T", 10), "INTERIM-10")):
        for pid, (prac, nd, last) in sorted(att[key].items(), key=lambda kv: ids[(kv[0], "T")]):
            rows.append([ids[(pid, "T")], py, run, W.TINS[prac], nd, last.isoformat()])
    _csv(t("pmh_attr"), ["memberId", "py", "run", "tin", "qualDays", "lastQualDate"], rows)


def remittance_files(t, w):
    lines = W.remittances(w)
    paydate = {k: D(2026, k, 20) - dt.timedelta(days=(D(2026, k, 20).weekday() - 4) % 7) for k in range(1, max(W.RUN_MONTHS) + 1)}
    # Merrinlake: coverage month on every line
    rows = []
    for ln in [x for x in lines if x["payer"] == "B"]:
        rows.append([paydate[ln["run"]].isoformat(), "CCF2026-%02d" % ln["run"], W.TINS[ln["practice"]].replace("-", ""),
                     "2026%02d" % ln["cov"], "CUR" if ln["type"] == "CURRENT" else "RETRO", ln["members"], "%.2f" % ln["amount"]])
    _csv(t("mlh_ccf"), ["PMT_DT", "PMT_RUN", "PRACTICE_TIN", "COV_MO", "LINE_TYP", "MBR_CNT", "PMT_AMT"], rows)
    # Kesselcrest: a workbook, service period on every line
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Remittance Detail"
    ws.append(["Payment Date", "Remit No", "TIN", "Service Period", "Members", "Amount"])
    for c in ws[1]:
        c.font = Font(bold=True)
    seq = {}
    for ln in sorted([x for x in lines if x["payer"] == "M"], key=lambda x: (x["run"], W.CODES.index(x["practice"]), x["cov"])):
        seq[ln["run"]] = seq.get(ln["run"], 0) + 1
        ws.append([paydate[ln["run"]], "KR26%02d%05d" % (ln["run"], 4100 + 7 * seq[ln["run"]]),
                   W.TINS[ln["practice"]], "%d-%02d" % (2026, ln["cov"]), ln["members"], ln["amount"]])
        ws.cell(row=ws.max_row, column=1).number_format = "mm/dd/yyyy"
        ws.cell(row=ws.max_row, column=6).number_format = "#,##0.00"
    for col, wd in zip("ABCDEF", (14, 14, 13, 14, 10, 12)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A2"
    wb.save(t("kbp_ccf"))
    # Pemberglen: one line per payment, posted to the run's period; the month a line covers is in its payment reference
    rows = []
    seq = 0
    for ln in [x for x in lines if x["payer"] == "T"]:
        seq += 1
        rows.append(["2026-%02d" % ln["run"], paydate[ln["run"]].isoformat(),
                     "PMH-CCF-%s-2026%02d-%04d" % (W.TINS[ln["practice"]][-4:], ln["cov"], seq), W.TINS[ln["practice"]],
                     ln["members"], "%.2f" % ln["amount"]])
    _csv(t("pmh_ccf"), ["period", "paymentDate", "paymentRef", "tin", "memberCount", "amount"], rows)
    return lines


def roster_file(t, w):
    rows = sorted(w["clinicians"], key=lambda r: (r["practice"], r["start"], r["npi"]))
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Primary Care Roster"
    ws.append(["NPI", "Credential", "Taxonomy", "Practice", "Practice TIN", "Effective", "Terminated"])
    for c in ws[1]:
        c.font = Font(bold=True)
    g = W.rng(44)
    # an advanced practice clinician carries the NUCC taxonomy of the credential, a physician the practice's specialty
    apc = {"208000000X": "363LP0200X", "207R00000X": "363LA2200X", "207Q00000X": "363LF0000X"}
    for r in rows:
        cred = ("MD", "DO", "NP", "PA")[int(g.choice(4, p=[0.62, 0.14, 0.17, 0.07]))]
        tax = r["spec"] if cred in ("MD", "DO") else (apc[r["spec"]] if cred == "NP" else "363A00000X")
        ws.append([r["npi"], cred, tax, W.PRACTICE_NAMES[r["practice"]], W.TINS[r["practice"]], r["start"], r["end"]])
        ws.cell(row=ws.max_row, column=6).number_format = "yyyy-mm-dd"
        ws.cell(row=ws.max_row, column=7).number_format = "yyyy-mm-dd"
    for col, wd in zip("ABCDEFG", (13, 11, 13, 32, 13, 12, 12)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A2"
    wb.save(t("roster"))


def mpi_file(t, w, ids, members):
    """The network's master patient index: every member a payer has shared, with each payer identifier."""
    ppl = {q.pid: q for q in w["people"]}
    shared = {(pid, p) for (p, y), pids in members.items() for pid in pids}
    rows = []
    pids = sorted({pid for (pid, _p) in shared})
    perm = W.rng(47).permutation(len(pids))
    lpn = {pid: "LPN%07d" % (2300417 + 31 * int(perm[n]) + int(W.rng(48, pid).integers(0, 31)))
           for n, pid in enumerate(pids)}
    for (pid, payer), mid in sorted(ids.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        if (pid, payer) not in shared:
            continue
        q = ppl[pid]
        rows.append([lpn[pid], PAYER_ABBR[payer], mid, q.dob.isoformat(), q.sex])
    rows.sort(key=lambda r: (r[0], r[1]))
    _csv(t("mpi"), ["LPN_PATIENT_ID", "PAYER", "PAYER_MEMBER_ID", "BIRTH_DATE", "SEX"], rows)


def fee_schedule_file(t):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    desc = {"99211": "Office or other outpatient visit, established patient, minimal", "99212": "Office visit, established, straightforward MDM",
            "99213": "Office visit, established, low MDM", "99214": "Office visit, established, moderate MDM",
            "99215": "Office visit, established, high MDM", "99202": "Office visit, new patient, straightforward MDM",
            "99203": "Office visit, new patient, low MDM", "99204": "Office visit, new patient, moderate MDM",
            "99205": "Office visit, new patient, high MDM"}
    for payer in W.PAYERS:
        ws = wb.create_sheet(W.PAYER_NAMES[payer].split()[0])
        ws.append([W.PAYER_NAMES[payer] + " - 2026 professional fee schedule, evaluation and management (excerpt)"])
        ws.append(["Effective 1 January 2026 for " + W.NETWORK + " participating clinicians"])
        ws.append([])
        ws.append(["Code", "Description", "Non-facility", "Facility"])
        ws["A1"].font = Font(bold=True)
        for c in ws[4]:
            c.font = Font(bold=True)
        f = W.FEES[(payer, 2026)]
        for i, code in enumerate(W.EM):
            ws.append([code, desc[code], f["nf"][i], f["fa"][i]])
        for i, code in enumerate(W.NEWPT):
            ws.append([code, desc[code], f["new"][i], None])
        for r in ws.iter_rows(min_row=5, min_col=3, max_col=4):
            for c in r:
                c.number_format = "0.00"
        ws.append([])
        note = {"B": "Non-facility rates apply in the office (POS 11) and for telehealth (POS 02, 10). Facility rates apply in "
                     "an outpatient hospital department (POS 19, 22).",
                "M": "Non-facility rates apply in the office (POS 11) and for telehealth (POS 02, 10). Facility rates apply in "
                     "an outpatient hospital department (POS 19, 22).",
                "T": "Non-facility rates apply in the office (POS 11). Facility rates apply in an outpatient hospital department "
                     "(POS 19, 22) and for telehealth (POS 02, 10)."}[payer]
        ws.append(["Place of service: " + note])
        ws.column_dimensions["A"].width = 9
        ws.column_dimensions["B"].width = 58
        ws.column_dimensions["C"].width = 13
        ws.column_dimensions["D"].width = 11
    wb.save(t("fees"))


def qualifying_codes_file(t):
    rows = []
    desc = {"99202": "New patient office visit, straightforward", "99203": "New patient office visit, low", "99204": "New patient office visit, moderate",
            "99205": "New patient office visit, high", "99211": "Established patient office visit, minimal",
            "99212": "Established patient office visit, straightforward", "99213": "Established patient office visit, low",
            "99214": "Established patient office visit, moderate", "99215": "Established patient office visit, high",
            "99381": "Preventive visit, new, infant", "99382": "Preventive visit, new, 1 to 4", "99383": "Preventive visit, new, 5 to 11",
            "99384": "Preventive visit, new, 12 to 17", "99385": "Preventive visit, new, 18 to 39", "99386": "Preventive visit, new, 40 to 64",
            "99391": "Preventive visit, established, infant", "99392": "Preventive visit, established, 1 to 4",
            "99393": "Preventive visit, established, 5 to 11", "99394": "Preventive visit, established, 12 to 17",
            "99395": "Preventive visit, established, 18 to 39", "99396": "Preventive visit, established, 40 to 64",
            "99460": "Initial care, normal newborn, hospital or birthing center", "99461": "Initial care, normal newborn, other setting",
            "99462": "Subsequent care, normal newborn, per day", "99463": "Initial care, normal newborn, admitted and discharged the same day"}
    for code in sorted(desc):
        cat = "Office or other outpatient" if code[3] in "01" else ("Newborn care" if code[3] == "4" else "Preventive medicine")
        rows.append([code, desc[code], cat])
    _csv(t("qualifying"), ["code", "description", "category"], rows)


def completion_factor_file(path, cf):
    rows = []
    for payer in W.PAYERS:
        for m in range(8):
            rows.append([PAYER_ABBR[payer], W.PAYER_NAMES[payer], "2026-%02d" % (m + 1), "2026-09-30", "%.3f" % cf[payer][m]])
    _csv(path, ["payer", "payer_name", "incurred_month", "paid_through", "completion_factor"], rows)


def distractor_files(t, w, ids):
    """Two files the decision does not use: Kesselcrest's Medicare Advantage attribution of the network's practices (the
    standard covers commercial members only) and the payers' 2025 quality measure results behind their settlements."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "MA Attribution 2026"
    ws.append(["Kesselcrest Benefit Partners  |  Medicare Advantage Provider Attribution  |  " + W.NETWORK])
    ws.append(["Attribution year 2026, quarterly refresh of 07/15/2026; plurality of allowed primary care E&M charges over "
               "the 24 months to 06/30/2026"])
    ws.append([])
    ws.append(["MA Member No", "Plan", "Attributed TIN", "Practice", "Attribution Start", "RAF Score", "E&M Visits (24 mo)"])
    ws["A1"].font = Font(bold=True)
    for c in ws[4]:
        c.font = Font(bold=True)
    rows = [[r["mid"], r["plan"], W.TINS[r["practice"]], W.PRACTICE_NAMES[r["practice"]], r["start"], r["raf"], r["visits"]]
            for r in W.ma_members()]
    rows.sort(key=lambda r: r[0])
    for r in rows:
        ws.append(r)
        ws.cell(row=ws.max_row, column=5).number_format = "mm/dd/yyyy"
        ws.cell(row=ws.max_row, column=6).number_format = "0.000"
    for col, wd in zip("ABCDEFG", (15, 27, 14, 32, 16, 10, 17)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A5"
    wb.save(t("ma"))
    rows = []
    for payer, c, code, name, den, num, target in W.quality_table():
        rows.append([2025, PAYER_ABBR[payer], W.TINS[c], W.PRACTICE_NAMES[c], code, name, den, num, "%.1f" % (100.0 * num / den),
                     "%.1f" % (100.0 * target), "Y" if num / den >= target else "N"])
    _csv(t("quality"), ["measurement_year", "payer", "practice_tin", "practice_name", "measure_code", "measure_name",
                        "denominator", "numerator", "rate_pct", "target_pct", "target_met"], rows)
