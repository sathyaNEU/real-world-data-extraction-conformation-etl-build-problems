"""The pack's data files, each written as the system that keeps it writes it."""
import csv
import datetime as dt
import io
import re
import zipfile

import numpy as np
import openpyxl
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import world as W

FILES = {
    "programme": "medicines_safety_programme_2027.pdf",
    "protocols": "deprescribing_review_protocols_2026.pdf",
    "closeout": "clun_valley_pilot_close_out_2026.pdf",
    "pilot": "deprescribing_pilot_outcome_log_2026.csv",
    "register": "member_practice_register_2026.csv",
    "registrations": "patient_registrations_2020-2026.parquet",
    "courses": "repeat_medication_courses_2026-12-31.csv",
    "issues": "prescribing_issues_2025-07_2026-12.parquet",
    "problems": "problem_list_extract_2026-12-31.csv",
    "letters": "trust_medicine_letters_feed_2019-2026.csv",
    "lookup": "trust_hospital_number_lookup.csv",
    "workflow": "practice_document_workflow_2026.csv",
    "hub": "pharmacist_hub_appointments_2026.csv",
    "groups": "hub_group_session_register_2026.xlsx",
    "activity": "clinical_system_pharmacist_activity_2026.csv",
    "lists": "registered_list_sizes_2026.csv",
    "epact": "epact2_prescribing_summary_2025-26.xlsx",
    "falls": "emergency_admissions_falls_65plus_2025-2026.csv",
}
DISTRACTORS = ["epact", "falls"]
ISSUES_FROM = dt.date(2025, 7, 1)


def _csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def _d(i):
    return "" if i is None or i == -1 else W.dd(i).isoformat()


def _uk(d):
    return d.strftime("%d/%m/%Y")


def write_register(path):
    rows = []
    for c, name, pc, _n, _o, merged in W.PRACTICES:
        rows.append([c, name, W.PCN_NAME[pc], W.POSTCODE[pc], "Active" if not merged else "Closed",
                     "" if not merged else W.MERGE_DATE.isoformat(), merged or ""])
    rows.sort(key=lambda x: (x[2], x[0]))
    return _csv(path, ["ods_code", "practice_name", "primary_care_network", "postcode_district", "status",
                       "closed_date", "successor_ods_code"], rows)


def write_registrations(T, path):
    S = T.S.sort_values(["pid", "start", "end"])
    P = T.P
    bym = ["%04d-%02d" % (y, m) for y, m in zip(P["birth_year"].values, P["birth_month"].values)]
    pidx = S["p"].values
    death = P["death"].values
    t = pa.table({
        "patient_pseudonym": pa.array(S["pid"].values.tolist(), pa.string()),
        "birth_month": pa.array([bym[i] for i in pidx], pa.string()),
        "sex": pa.array(P["sex"].values[pidx].tolist(), pa.string()),
        "date_of_death": pa.array([W.dd(death[i]) if death[i] != -1 else None for i in pidx], pa.date32()),
        "practice_code": pa.array(S["prac"].values.tolist(), pa.string()),
        "registration_start": pa.array([W.dd(x) for x in S["start"].values], pa.date32()),
        "registration_end": pa.array([W.dd(x) if x != -1 else None for x in S["end"].values], pa.date32()),
        "end_reason": pa.array([x if x else None for x in S["reason"].values], pa.string()),
    })
    pq.write_table(t, path, compression="snappy", use_dictionary=True, write_statistics=False, store_schema=False)
    _drop_created_by(path)
    return len(S)


def _course_practice(T, c):
    lst = T.spells_by_p[int(c.p)][-1]
    return W.survivor(lst[2], W.AS_OF)


def write_courses(T, path):
    rows = []
    pid = T.P["pid"].values
    for c in T.C.sort_values(["p", "start", "cid"]).itertuples(index=False):
        last = c.last
        if last is None or (isinstance(last, float) and np.isnan(last)):
            continue
        ended = c.end != -1 or (W.dd(int(last)) < W.dd(W.di(W.AS_OF) - 60))
        rows.append([c.cid, pid[c.p], _course_practice(T, c), c.vmp, W.PROD[c.vmp]["name"], _d(c.start), _d(int(last)),
                     int(c.n_issues), "Ended" if ended else "Current"])
    rows.sort(key=lambda x: (x[2], x[1], x[5], x[0]))
    return _csv(path, ["course_id", "patient_pseudonym", "practice_code", "dmd_vmp_code", "medicine",
                       "first_issue_date", "last_issue_date", "issues_to_date", "course_status"], rows)


def _prac_on(T, p, x):
    for a, b, pr, _ in T.spells_by_p[p]:
        if a <= x and (b == -1 or x < b):
            return W.survivor(pr, W.dd(x))
    return W.survivor(T.spells_by_p[p][-1][2], W.dd(x))


def write_issues(T, path):
    cp = dict(zip(T.C["cid"].values, T.C["p"].values))
    cv = dict(zip(T.C["cid"].values, T.C["vmp"].values))
    I = T.I[T.I["date"] >= W.di(ISSUES_FROM)].copy()
    I = I.sort_values(["date", "cid"])
    pid = T.P["pid"].values
    r = W.rng("issue_ids")
    ids, prac, pseud, vmp, name, qty, kind = [], [], [], [], [], [], []
    n = 4400000
    for cid, x, seq in zip(I["cid"].values, I["date"].values, I["seq"].values):
        n += int(r.integers(1, 40))
        ids.append("IS%08d" % n)
        p = int(cp[cid])
        prac.append(_prac_on(T, p, int(x)))
        pseud.append(pid[p])
        v = cv[cid]
        vmp.append(v)
        name.append(W.PROD[v]["name"])
        qty.append(W.PROD[v]["qty"])
        kind.append("Acute" if seq == 1 else "Repeat")
    t = pa.table({
        "issue_id": pa.array(ids, pa.string()),
        "issue_date": pa.array([W.dd(x) for x in I["date"].values], pa.date32()),
        "practice_code": pa.array(prac, pa.string()),
        "patient_pseudonym": pa.array(pseud, pa.string()),
        "course_id": pa.array(I["cid"].values.tolist(), pa.string()),
        "dmd_vmp_code": pa.array(vmp, pa.string()),
        "medicine": pa.array(name, pa.string()),
        "quantity": pa.array(qty, pa.int32()),
        "issue_type": pa.array(kind, pa.string()),
    })
    pq.write_table(t, path, compression="snappy", use_dictionary=True, write_statistics=False, store_schema=False)
    _drop_created_by(path)
    return len(ids)


def write_problems(T, path):
    pid = T.P["pid"].values
    rows = []
    for rec in T.DX.itertuples(index=False):
        code, term = W.DX[rec.dx]
        d = W.dd(int(rec.date))
        prac = None
        for a, b, pr, _ in T.spells_by_p[int(rec.p)]:
            if a <= W.di(W.AS_OF) and (b == -1 or W.di(W.AS_OF) < b):
                prac = W.survivor(pr, W.AS_OF)
        prac = prac or W.survivor(T.spells_by_p[int(rec.p)][-1][2], W.AS_OF)
        rows.append([pid[int(rec.p)], prac, code, term, d.isoformat()])
    rows.sort(key=lambda x: (x[1], x[0], x[4], x[2]))
    return _csv(path, ["patient_pseudonym", "practice_code", "snomed_code", "term", "recorded_date"], rows)


def write_letters(T, path):
    pid = T.P["pid"].values
    rows = []
    for x in sorted(T.L, key=lambda z: (z["date"], z["ref"])):
        d, enc = W.dd(x["date"]), W.dd(x["enc"])
        fmt = (lambda v: v.isoformat()) if x["trust"] == "WTH" else _uk
        for k, (txt, rec) in enumerate(x["lines"], 1):
            rows.append([x["ref"], k, W.TRUST_NAME[x["trust"]], x["service"], fmt(enc), fmt(d),
                         "" if x["hn_only"] else pid[x["p"]], x["hn"], x["addressed"], txt, rec])
    return _csv(path, ["letter_reference", "line", "sender", "service", "encounter_date", "letter_date",
                       "patient_pseudonym", "hospital_number", "gp_practice_code", "medicine_line", "recommendation"],
                rows)


def write_lookup(T, path):
    pid = T.P["pid"].values
    rows = sorted([W.TRUST_NAME[t], h, pid[p]] for (p, t), h in T.hn.items())
    return _csv(path, ["trust", "hospital_number", "patient_pseudonym"], rows)


DOC_TYPE = {"Emergency Department": "Emergency Department attendance", "Acute Medicine": "Discharge summary",
            "Care of the Elderly": "Discharge summary", "Orthopaedics": "Discharge summary",
            "Spinal Surgery": "Discharge summary", "Renal Medicine": "Outpatient letter"}


def doc_type(trust, service):
    if trust == "MMH":
        return "Mental health letter"
    if service in DOC_TYPE:
        return DOC_TYPE[service]
    if service in ("Pathology report", "Radiology report", "Outpatient letter", "Emergency Department attendance"):
        return service
    return "Outpatient letter"


def write_workflow(T, path):
    pid = T.P["pid"].values
    rows = []
    for z in T.W:
        rows.append([z["prac"], "D%08d" % z["doc_id"], z["recv_at"].strftime("%Y-%m-%d %H:%M:%S"),
                     W.TRUST_NAME[z["trust"]], doc_type(z["trust"], z["service"]), z["docdate"].isoformat(),
                     pid[z["p"]], z["ext"]])
    return _csv(path, ["practice_code", "document_id", "received", "sender", "document_type", "document_date",
                       "patient_pseudonym", "sender_reference"], rows)


def _utc(t):
    bst = dt.datetime(2026, 3, 29, 1, 0) <= t - dt.timedelta(hours=1) < dt.datetime(2026, 10, 25, 1, 0)
    return (t - dt.timedelta(hours=1 if bst else 0)).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_hub(T, path):
    pid = T.P["pid"].values
    rows = []
    for h in T.hub:
        rows.append([h["aid"], W.HUBS[h["site"]][0], _utc(h["t"]), h["dur"], h["ph"], h["ctype"], pid[h["p"]],
                     h["outcome"]])
    for g in T.groups:
        rows.append([g["aid"], W.HUBS[g["site"]][0], _utc(g["t"]), g["dur"], g["ph"], "Group medicines review", "",
                     "Attended"])
    rows.sort(key=lambda x: (x[2], x[0]))
    return _csv(path, ["appointment_id", "hub", "slot_start_utc", "slot_minutes", "pharmacist", "appointment_type",
                       "patient_pseudonym", "outcome"], rows)


def write_activity(T, path):
    pid = T.P["pid"].values
    rows = []
    for c in T.prac_cons:
        rows.append([c["code"], c["cid"], c["t"].date().isoformat(), c["t"].strftime("%H:%M"), c["ph"], c["ctype"],
                     pid[c["p"]]])
    rows.sort(key=lambda x: (x[2], x[3], x[0], x[1]))
    return _csv(path, ["practice_code", "consultation_id", "consultation_date", "consultation_time", "clinician",
                       "consultation_type", "patient_pseudonym"], rows)


def write_groups(T, path):
    pid = T.P["pid"].values
    rows = [["Session", "Date", "Hub", "Topic", "Lead pharmacist", "Patient", "Attended"]]
    for g in sorted(T.groups, key=lambda z: z["t"]):
        for p, att in g["attendees"]:
            rows.append([g["aid"], g["t"].date(), W.HUBS[g["site"]][0], g["topic"], g["ph"], pid[p], att])
    created = dt.datetime(2026, 1, 9, 9, 12, 0)
    modified = dt.datetime(2027, 1, 5, 16, 41, 0)
    xlsx(path, [("Register", rows, [12, 12, 20, 34, 15, 14, 10])], "Marches Primary Care Collaborative", created,
         modified, date_cols={"Register": [2]})
    return len(rows) - 1


def write_lists(T, path):
    rows = [[r_.practice, r_.date.isoformat(), int(r_.patients)] for r_ in T.LS.itertuples(index=False)]
    rows.sort(key=lambda x: (x[1], x[0]))
    return _csv(path, ["practice_code", "extract_date", "registered_patients"], rows)


def write_pilot(T, path):
    pid = T.P["pid"].values
    r = W.rng("pilot_log")
    rows = []
    for cls in W.REVIEWS:
        res, died = T.pilot_res[cls]
        for x in res + died:
            c = x["c"]
            prac = W.survivor(T.spells_by_p[int(c["p"])][-1][2], W.AS_OF)
            for a, b, pr, _ in T.spells_by_p[int(c["p"])]:
                if a <= W.di(x["review"]) and (b == -1 or W.di(x["review"]) < b):
                    prac = W.survivor(pr, x["review"])
            ph = "CP0%d" % int(r.integers(1, 4)) if cls != "GB" else "CP0%d" % int(r.integers(3, 6))
            rows.append([pid[c["p"]], prac, cls, "Review", x["review"].isoformat(), x["outcome"], ph])
            if x["status"]:
                fu = x["review"] + dt.timedelta(days=W.OFF_DAYS + int(r.integers(0, 6)))
                rows.append([pid[c["p"]], prac, cls, "Six-month follow-up", fu.isoformat(),
                             "Off medicine" if x["status"] == "Off" else "On medicine", ph])
    rows.sort(key=lambda z: (z[4], z[1], z[0], z[3]))
    labels = {"AP": "Antipsychotics 65+", "BZ": "Benzodiazepines and Z-drugs 65+", "GB": "Gabapentinoid with opioid"}
    rows = [[a, b, labels[c], d, e, f, g] for a, b, c, d, e, f, g in rows]
    return _csv(path, ["patient_pseudonym", "practice_code", "review", "record_type", "record_date", "outcome",
                       "pharmacist"], rows)


def write_epact(T, path):
    """ePACT2 items dispensed by practice, financial quarter and BNF section (a share of issues go undispensed)."""
    r = W.rng("epact")
    cp = dict(zip(T.C["cid"].values, T.C["p"].values))
    cc = dict(zip(T.C["cid"].values, T.C["cls"].values))
    I = T.I[(T.I["date"] >= W.di(dt.date(2025, 4, 1))) & (T.I["date"] < W.di(dt.date(2026, 10, 1)))]
    sect = {"AP": "0402010 Antipsychotic drugs", "BZ": "0401010 Hypnotics; 0401020 Anxiolytics",
            "GB": "0408010 Control of the epilepsies: gabapentin and pregabalin", "OP": "0407020 Opioid analgesics"}
    agg = {}
    for cid, x in zip(I["cid"].values, I["date"].values):
        d = W.dd(int(x))
        prac = _prac_on(T, int(cp[cid]), int(x))
        fy = d.year if d.month >= 4 else d.year - 1
        q = (d.month - 4) % 12 // 3 + 1
        key = (prac, "%d/%02d Q%d" % (fy, (fy + 1) % 100, q), sect[cc[cid]])
        agg[key] = agg.get(key, 0) + 1
    rows = [["Practice code", "Financial quarter", "BNF section", "Items", "Items per 1,000 patients"]]
    lists = T.LS.set_index(["practice", "date"])["patients"]
    for (prac, fq, s), n in sorted(agg.items()):
        items = int(round(n * (0.955 + 0.03 * r.random())))
        fy, q = int(fq[:4]), int(fq[-1])
        m = 4 + 3 * (q - 1)
        y = fy if m <= 12 else fy + 1
        m = m if m <= 12 else m - 12
        dref = dt.date(max(y, 2026), m if y >= 2026 else 1, 1)
        pts = int(lists.get((prac, dref), lists.xs(prac, level=0).iloc[0]))
        rows.append([prac, fq, s, items, round(1000 * items / pts, 1)])
    created = dt.datetime(2026, 11, 20, 10, 2, 0)
    xlsx(path, [("Items by quarter", rows, [13, 17, 44, 9, 22])], "NHS Severn Marches ICB Medicines Optimisation",
         created, created)
    return len(rows) - 1


def write_falls(T, path):
    r = W.rng("falls")
    rows = []
    for pc, name in W.PCNS:
        base = {"CV": 13200, "WC": 11400, "WN": 9500, "TV": 10900, "SG": 8600}[pc]
        for y in (2025, 2026):
            for q in range(1, 5):
                pop = int(base * (1 + 0.012 * (y - 2025) + 0.003 * q) + r.integers(-40, 40))
                rate = 0.0215 * (1.18 if q == 1 else (1.08 if q == 4 else 0.94)) / 4
                n = int(r.poisson(pop * rate))
                rows.append([name, "%d Q%d" % (y, q), n, pop])
    return _csv(path, ["primary_care_network", "quarter", "emergency_admissions_falls_65plus",
                       "registered_patients_65plus"], rows)


# ------------------------------------------------------------------------------------------------------------------
# containers
# ------------------------------------------------------------------------------------------------------------------
def xlsx(path, sheets, creator, created, modified, date_cols=None):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for title, rows, widths in sheets:
        ws = wb.create_sheet(title)
        for row in rows:
            ws.append(list(row))
        for col, wd in zip("ABCDEFGHIJ", widths):
            ws.column_dimensions[col].width = wd
        for c in ws[1]:
            c.font = openpyxl.styles.Font(bold=True)
        for j in (date_cols or {}).get(title, []):
            for row in ws.iter_rows(min_row=2, min_col=j, max_col=j):
                for c in row:
                    c.number_format = "dd/mm/yyyy"
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = created
    wb.properties.modified = modified
    buf = io.BytesIO()
    wb.save(buf)
    src = zipfile.ZipFile(io.BytesIO(buf.getvalue()))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename == "docProps/app.xml":
                titles = [t for t, _r, _w in sheets]
                parts = "".join("<vt:lpstr>%s</vt:lpstr>" % t for t in titles)
                data = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
                        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
                        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
                        '<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity>'
                        '<ScaleCrop>false</ScaleCrop><HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant>'
                        '<vt:lpstr>Worksheets</vt:lpstr></vt:variant><vt:variant><vt:i4>%d</vt:i4></vt:variant>'
                        '</vt:vector></HeadingPairs><TitlesOfParts><vt:vector size="%d" baseType="lpstr">%s'
                        '</vt:vector></TitlesOfParts><Company>%s</Company><LinksUpToDate>false</LinksUpToDate>'
                        '<SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged>'
                        '<AppVersion>16.0300</AppVersion></Properties>'
                        % (len(titles), len(titles), parts, creator)).encode("utf-8")
            if info.filename == "docProps/core.xml":
                data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                              b"\\g<1>" + modified.strftime("%Y-%m-%dT%H:%M:%SZ").encode() + b"\\g<2>", data)
                data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)",
                              b"\\g<1>" + created.strftime("%Y-%m-%dT%H:%M:%SZ").encode() + b"\\g<2>", data)
            zi = zipfile.ZipInfo(info.filename, date_time=modified.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)


def _varint(b, i):
    v = s = 0
    while True:
        c = b[i]; i += 1
        v |= (c & 0x7F) << s; s += 7
        if not c & 0x80:
            return v, i


def _skip(b, i, t):
    """Skip one compact-protocol thrift value of type t starting at b[i]."""
    if t in (1, 2):
        return i
    if t == 3:
        return i + 1
    if t in (4, 5, 6):
        return _varint(b, i)[1]
    if t == 7:
        return i + 8
    if t == 8:
        n, i = _varint(b, i)
        return i + n
    if t in (9, 10):
        h = b[i]; i += 1
        n, et = h >> 4, h & 0x0F
        if n == 15:
            n, i = _varint(b, i)
        for _ in range(n):
            i = i + 1 if et in (1, 2) else _skip(b, i, et)
        return i
    if t == 11:
        n, i = _varint(b, i)
        if n:
            kv = b[i]; i += 1
            for _ in range(n):
                i = _skip(b, i, kv >> 4)
                i = _skip(b, i, kv & 0x0F)
        return i
    if t == 12:
        while True:
            h = b[i]; i += 1
            if h == 0:
                return i
            if not h >> 4:
                i = _varint(b, i)[1]
            i = _skip(b, i, h & 0x0F)
    raise ValueError("thrift type %d" % t)


def _drop_created_by(path):
    """The export carries no writer name: FileMetaData field 6 (created_by) is left out of the footer, as the format
    allows, and the next field's header is re-based on the field before it."""
    raw = open(path, "rb").read()
    assert raw[-4:] == b"PAR1"
    n = int.from_bytes(raw[-8:-4], "little")
    meta, body = raw[-8 - n:-8], raw[:-8 - n]
    out, i, last, prev, dropped = bytearray(), 0, 0, 0, False
    while meta[i]:
        h, j = meta[i], i + 1
        if h >> 4:
            fid = last + (h >> 4)
        else:
            z, j = _varint(meta, j)
            fid = (z >> 1) ^ -(z & 1)
        t = h & 0x0F
        end = _skip(meta, j, t)
        if fid == 6:
            dropped = True
        else:
            out += bytes([((fid - prev) << 4) | t]) if 0 < fid - prev <= 15 else bytes([t]) + _zz(fid)
            out += meta[j:end]
            prev = fid
        last, i = fid, end
    out += meta[i:]
    assert dropped, "no created_by in the footer"
    open(path, "wb").write(body + bytes(out) + len(out).to_bytes(4, "little") + b"PAR1")


def _zz(v):
    z, o = (v << 1) ^ (v >> 63), bytearray()
    while True:
        if z < 0x80:
            o.append(z)
            return bytes(o)
        o.append((z & 0x7F) | 0x80); z >>= 7


def write_data(T, f):
    n = {}
    n["register"] = write_register(f("register"))
    n["registrations"] = write_registrations(T, f("registrations"))
    n["courses"] = write_courses(T, f("courses"))
    n["issues"] = write_issues(T, f("issues"))
    n["problems"] = write_problems(T, f("problems"))
    n["letters"] = write_letters(T, f("letters"))
    n["lookup"] = write_lookup(T, f("lookup"))
    n["workflow"] = write_workflow(T, f("workflow"))
    n["hub"] = write_hub(T, f("hub"))
    n["groups"] = write_groups(T, f("groups"))
    n["activity"] = write_activity(T, f("activity"))
    n["lists"] = write_lists(T, f("lists"))
    n["pilot"] = write_pilot(T, f("pilot"))
    n["epact"] = write_epact(T, f("epact"))
    n["falls"] = write_falls(T, f("falls"))
    return n
