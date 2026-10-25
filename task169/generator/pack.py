"""task169 pack: the agencies' extracts as the Commission received them, written from the records.

Each file carries the mess its own system produces (two movement-code vocabularies across the Department's 2022
upgrade, admission rows beside transfer and court-writ rows, the Bureau's and the Department's two formats of the
state ID, amended court rows and cases still open at the cut, the Board's two case systems across its January 2026
go-live, holds whose end the legacy system never wrote when the person went to the Department)."""
from __future__ import annotations

import datetime as dt
import math
import os

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

import common as C
import records as R
import world as W

CHECK = "ABCDEFGHJKLMNPQRTUVWXYZ"


def _sbi(n):
    s = "%07d" % n
    return s + CHECK[sum((i + 2) * int(c) for i, c in enumerate(s)) % 23]


def _xw_sbi(s):
    return s[:7] + "-" + s[7]


def _doc_prefix(d):
    return "R" if d.year < 2021 else "T" if d.year < 2024 else "W"


def mdy(d):
    return "" if d is None else "%02d/%02d/%04d" % (d.month, d.day, d.year)


class Identity:
    """numbers and fixed attributes per person"""

    def __init__(self, ppl, cohort):
        rng = C.stream("ids")
        self.p = {}
        seen_doc, seen_sbi = set(), set()
        allp = list(ppl) + [p for p in cohort if not p["inrecord"]]
        for p in allp:
            pid = p["pid"]
            if pid in self.p:
                continue
            while True:
                commit = C.add(p["rel0"], -int(rng.integers(200, 2600)))
                doc = _doc_prefix(commit) + "%06d" % int(rng.integers(100000, 999999))
                if doc not in seen_doc:
                    break
            while True:
                sbi = _sbi(int(rng.integers(1200000, 9899999)))
                if sbi not in seen_sbi:
                    break
            seen_doc.add(doc)
            seen_sbi.add(sbi)
            county = C.COUNTIES[p["dist"]][rng.choice(3, p=C.COUNTY_W)]
            birth = C.add(p["rel0"], -int(p["age0"] * 365.25))
            self.p[pid] = dict(doc=doc, sbi=sbi, county=county, birth=birth, sex="F" if p["female"] else "M",
                               off=p["off"], dist=p["dist"], priors=p["priors"])


def _county_of(dist, rng):
    return C.COUNTIES[dist][rng.choice(3, p=C.COUNTY_W)]


def write_releases(path, book, ident, ppl):
    """one row per release movement out of Department custody"""
    rng = C.stream("pack/releases")
    by = {p["pid"]: p for p in ppl}
    commits_before = {}
    nc = {}
    for pid, ad, atype, otn, vid in book.admissions:
        if atype == "NC":
            nc.setdefault(pid, []).append(ad)
    rows = []
    for pid, rd, rtype, maxd, dist, rno in sorted(book.releases, key=lambda r: (r[1], r[0], r[5])):
        if rd > C.CUT:
            continue
        p = by[pid]
        I = ident.p[pid]
        priors = p["priors"] + sum(1 for a in nc.get(pid, []) if a < rd)
        age = p["age0"] + C.days(p["rel0"], rd) / 365.25
        q = dict(p, age0=age, priors=priors)
        score = W.risk_score(q, rng)
        new = rd >= C.OMS_UPGRADE
        code = {"PAROLE": ("PAROLE", "PAR"), "REPAROLE": ("REPAROLE", "RPR"), "EXPIRATION": ("MAX EXP", "EXP")}[rtype][new]
        fac = C.FACILITIES[int(rng.integers(0, len(C.FACILITIES)))] if rng.random() < 0.93 else "CCC-" + I["county"][:3].upper()
        prat_date = C.add(rd, -int(rng.integers(14, 150)))
        rows.append((I["doc"], mdy(rd), code, fac, I["county"].upper(), mdy(I["birth"]), I["sex"], p["off"].upper(),
                     priors, score, mdy(prat_date), mdy(maxd) if maxd is not None else ""))
    head = ("doc_number", "release_date", "movement_code", "facility", "county_of_commitment", "birth_date", "sex",
            "governing_offense", "prior_commitments", "prat_total", "prat_date", "max_expiration_date")
    return C.write_csv(path, head, rows)


def write_admissions(path, book, ident):
    """admission movements into Department custody, with the transfers out of reception and court-writ movements the
    offender management system writes into the same table"""
    rng = C.stream("pack/admissions")
    wrng = C.stream("pack/writs")
    rels = {}
    for pid, rd, rtype, maxd, dist, rno in book.releases:
        rels.setdefault(pid, []).append(rd)
    import tables as T
    rows = []
    writs = {}
    lags = {}
    for pid, ad, atype, otn, vid in book.admissions:
        if ad > C.CUT:
            continue
        doc = ident.p[pid]["doc"]
        out = min([r for r in rels.get(pid, []) if r > ad], default=dt.date(2099, 1, 1))
        t = "%02d:%02d" % (int(rng.integers(8, 18)), int(rng.integers(0, 60)))
        reason = "NEW COMMITMENT" if atype == "NC" else "PAROLE VIOLATOR"
        county = ident.p[pid]["county"].upper()
        rows.append((doc, "%s %s" % (ad.isoformat(), t), "ADM", reason, C.RECEPTION, county))
        lag = int(rng.integers(6, 48))
        tr = C.add(ad, lag)
        if tr < out:
            lags[(pid, ad)] = lag
        if tr < out and tr <= C.CUT:
            fac = T.facility_of(pid, ad)
            rows.append((doc, "%s %02d:%02d" % (tr.isoformat(), int(rng.integers(5, 11)), int(rng.integers(0, 60))),
                         "TRN", "CLASSIFICATION", fac, county))
            # trips out to court on a writ: the institution writes WRO when the person leaves and WRI on return; a
            # person the court releases (a sentence that ran out, a conviction vacated) never comes back, so the trip
            # ends in the release movement and has no WRI
            last = min(out, C.add(C.CUT, 1))
            t0 = C.add(tr, 5)
            while True:
                t0 = C.add(t0, int(wrng.exponential(300)))
                dur = int(wrng.integers(1, 13))
                if C.add(t0, dur + 8) >= last:
                    break
                wo_ = (doc, "%s %02d:%02d" % (t0.isoformat(), int(wrng.integers(5, 8)), int(wrng.integers(0, 60))),
                       "WRO", "COURT WRIT", fac, county)
                t0 = C.add(t0, dur)
                wi_ = (doc, "%s %02d:%02d" % (t0.isoformat(), int(wrng.integers(15, 21)), int(wrng.integers(0, 60))),
                       "WRI", "COURT WRIT", fac, county)
                writs.setdefault(doc, []).append((wo_[1], wi_[1], wo_, wi_))
            if out <= C.CUT and C.days(tr, out) > 20 and wrng.random() < 0.12:
                wo = C.add(out, -int(wrng.integers(1, 7)))
                if all(not (w[2][1][:10] >= wo.isoformat() or w[1][:10] >= wo.isoformat()) for w in writs.get(doc, [])[-6:]):
                    wo_ = (doc, "%s %02d:%02d" % (wo.isoformat(), int(wrng.integers(5, 8)), int(wrng.integers(0, 60))),
                           "WRO", "COURT WRIT", fac, county)
                    writs.setdefault(doc, []).append((wo_[1], out.isoformat() + " 00:00", wo_, None))
    # one body is on one court trip at a time: where a person's two admissions without a release between them would
    # put a second trip out before the first came back, the later trip is not written
    for doc, ws in writs.items():
        end = ""
        for start, stop, wo_, wi_ in sorted(ws):
            if start < end:
                continue
            rows.append(wo_)
            if wi_ is not None:
                rows.append(wi_)
            end = stop
    rows.sort(key=lambda r: (r[1], r[0]))
    head = ("doc_number", "movement_datetime", "movement_type", "movement_reason", "location", "county_of_commitment")
    return C.write_csv(path, head, rows), lags


GRADES = {"F1": (("FA", 0.35), ("FB", 0.65)), "F2": (("FC", 0.38), ("FD", 0.40), ("FE", 0.22)),
          "M": (("M1", 0.42), ("M2", 0.38), ("M3", 0.20))}
CHARGES = {"FA": ("Aggravated assault", "Robbery, armed", "Burglary of a residence, occupied"),
           "FB": ("Robbery", "Aggravated assault", "Burglary of a residence", "Possession with intent, schedule I"),
           "FC": ("Burglary", "Theft over 2000", "Possession with intent", "Unlawful possession of a firearm"),
           "FD": ("Theft over 500", "Receiving stolen property", "Fleeing an officer", "Forgery"),
           "FE": ("Possession of a controlled substance", "Theft by deception", "Criminal mischief over 1000"),
           "M1": ("Simple assault", "Retail theft", "Driving under the influence", "Resisting arrest"),
           "M2": ("Possession of a small amount", "Criminal trespass", "Driving while suspended"),
           "M3": ("Disorderly conduct", "Harassment", "Public drunkenness")}


def arrest_grades(book):
    rng = C.stream("pack/grades")
    out = {}
    for pid, d, otn, cls, onsup in book.arrests:
        gs = GRADES[cls]
        g = gs[rng.choice(len(gs), p=[x[1] for x in gs])][0]
        out[otn] = (g, CHARGES[g][int(rng.integers(0, len(CHARGES[g])))])
    return out


def _otn(n):
    return "T%08d" % (40_000_000 + n * 7 + n % 7)


def write_arrests(path, book, ident, grades):
    rng = C.stream("pack/arrests")
    sbi, otn, date, ori, grade, desc = [], [], [], [], [], []
    county_ori = {}
    for dist, cs in C.COUNTIES.items():
        for i, c in enumerate(cs):
            county_ori[c] = ("PB%03d00" % (10 + 10 * list(C.DISTRICTS).index(dist) + i))
    for pid, d, o, cls, onsup in sorted(book.arrests, key=lambda r: (r[1], r[2])):
        if d > C.CUT:
            continue
        I = ident.p[pid]
        u = rng.random()
        agency = "PBSP%04d" % int(rng.integers(1, 40)) if u < 0.22 else county_ori[I["county"]][:5] + "%02d" % int(rng.integers(0, 12))
        sbi.append(I["sbi"]); otn.append(_otn(o)); date.append(d); ori.append(agency)
        grade.append(grades[o][0]); desc.append(grades[o][1])
    t = pa.table({"sbi_no": pa.array(sbi, pa.string()), "otn": pa.array(otn, pa.string()),
                  "arrest_date": pa.array(date, pa.date32()), "arresting_ori": pa.array(ori, pa.string()),
                  "top_charge_grade": pa.array(grade, pa.string()), "top_charge": pa.array(desc, pa.string())})
    pq.write_table(t, path, compression="snappy", use_dictionary=True, write_statistics=False)
    return len(sbi)


def write_crosswalk(path, ident):
    rows = sorted((_xw_sbi(v["sbi"]), v["doc"]) for v in ident.p.values())
    return C.write_csv(path, ("sbi", "doc_number"), rows)


def write_cases(path, book, ident, grades):
    """the courts' case table: one row per docket, a later row where a disposition was amended"""
    rng = C.stream("pack/cases")
    rows = []
    seq = {}
    for otn, pid, adate, route, disp, dd, sent, sd in sorted(book.cases, key=lambda r: (r[2], r[0])):
        if adate > C.CUT:
            continue
        I = ident.p[pid]
        county = I["county"]
        filed = C.add(adate, int(rng.integers(1, 22)))
        if filed > C.CUT:
            filed = None
        y = (filed or adate).year
        seq[(county, y)] = seq.get((county, y), 0) + 1
        docket = "CR-%s-%d-%05d" % (county[:3].upper(), y, seq[(county, y)] * 3 + int(rng.integers(0, 3)))
        g = grades[otn][0]
        if dd is None or dd > C.CUT:
            rows.append((docket, _otn(otn), county + " County", g, filed.isoformat() if filed else "", "OPEN", "", "", "", "",
                         C.CUT.isoformat()))
            continue
        if route == "BOARD":
            code = "NP"
        elif disp == "CONVICTED":
            code = "GP" if rng.random() < 0.91 else "GT"
        elif disp == "ACQUITTED":
            code = "AQ"
        else:
            code = "NP" if rng.random() < 0.08 else "DM"
        st = {"PRISON": "DOC", "JAIL": "CJ", "PROBATION": "PROB", "": ""}[sent]
        sdays = ""
        if st == "DOC":
            sdays = str(int(rng.lognormal(math.log(900), 0.5)))
        elif st == "CJ":
            sdays = str(int(rng.integers(30, 365)))
        elif st == "PROB":
            sdays = str(int(rng.choice([365, 540, 730, 1095])))
        entry = C.add(dd, int(rng.integers(0, 6)))
        if entry > C.CUT:
            entry = C.CUT
        rows.append((docket, _otn(otn), county + " County", g, filed.isoformat() if filed else adate.isoformat(), code,
                     dd.isoformat(), st, (sd.isoformat() if sd else dd.isoformat()) if st else "", sdays, entry.isoformat()))
        if st == "DOC" and rng.random() < 0.035:
            e2 = C.add(entry, int(rng.integers(40, 300)))
            if e2 <= C.CUT:
                rows.append((docket, _otn(otn), county + " County", g, filed.isoformat() if filed else adate.isoformat(), code,
                             dd.isoformat(), st, sd.isoformat(), str(int(int(sdays) * rng.uniform(0.55, 0.9))), e2.isoformat()))
    rows.sort(key=lambda r: (r[10], r[0]))
    head = ("docket_no", "otn", "county", "charge_grade", "filed_date", "disposition", "disposition_date",
            "sentence_type", "sentence_date", "sentence_days", "entry_date")
    return C.write_csv(path, head, rows)


def write_deaths(path, book, ident):
    rng = C.stream("pack/deaths")
    rows = []
    for pid, d in sorted(book.deaths, key=lambda r: (r[1], r[0])):
        if d > C.CUT:
            continue
        I = ident.p[pid]
        score = int(rng.integers(91, 100)) if rng.random() < 0.9 else int(rng.integers(80, 91))
        rows.append((I["sbi"], I["doc"], d.isoformat(), mdy(I["birth"]), I["county"] + " County", score))
    head = ("sbi_no", "doc_number", "date_of_death", "birth_date", "county_of_death", "match_score")
    return C.write_csv(path, head, rows)


# ---------------------------------------------------------------- the Board's two systems
COND = {"report": "03", "residence": "04", "drugs": "07", "curfew": "09", "program": "11", "travel": "05"}
COND_TEXT = {"03": "Report as directed", "04": "Maintain approved residence", "07": "Refrain from controlled substances",
             "09": "Observe curfew", "11": "Attend required program", "05": "Do not leave the state without permission",
             "01": "Obey all laws"}


def _jail_draw(vid):
    import hashlib
    return int(hashlib.sha256(("jail/%d" % vid).encode()).hexdigest()[:8], 16) / 0xFFFFFFFF


def board_frames(book, ident):
    """split the Board's violation records into the legacy system and the new one, with the migration and the
    January 2026 parallel run"""
    rng = C.stream("pack/board")
    adm_of = {}
    for pid, d, atype, otn, vid_ in book.admissions:
        adm_of.setdefault(pid, []).append(d)
    holds = {}
    for vid, pid, lodged, lifted, admitted in book.holds:
        if lifted is not None:
            # a parolee the courts sent to the Department while the Board's detainer was still lodged left the county
            # jail on the day of the admission, and the Board lifted the detainer that day
            inside = [d for d in adm_of.get(pid, ()) if lodged <= d < lifted]
            if inside:
                lifted = min(inside)
        holds[vid] = (lodged, lifted, admitted)
    resc = {vid: d for vid, pid, d in book.rescinds}
    companion_of = {}
    legacy, new = [], []
    nlegacy = {}
    officers = {d: ["%s%02d" % (C.OFFICE[d], k) for k in range(1, 7)] for d in C.DISTRICTS}
    # a second report taken up at the same hearing: a supplemental report on the same arrest, or a conditions report
    # filed while the parolee was held; the Board decides both cases at one hearing with one recommitment term
    crng = C.stream("pack/board_companions")
    viols = list(book.violations)
    comp = []
    for vid, pid, rep, vtype, otn, hd, decision, term in viols:
        if decision != "REVOKED" or vid not in holds or C.days(rep, hd) < 6 or crng.random() >= 0.11:
            continue
        crep = C.add(rep, int(crng.integers(2, C.days(rep, hd) - 2)))
        cvid = 50_000_000 + vid
        if vtype == "N" and crng.random() < 0.55:
            comp.append((cvid, pid, crep, "N", otn, hd, decision, term))
        else:
            comp.append((cvid, pid, crep, "C", "", hd, decision, term))
        h = holds[vid]
        holds[cvid] = (crep, h[1], h[2])
        if vid in resc:
            resc[cvid] = resc[vid]
        companion_of[cvid] = vid
    for vid, pid, rep, vtype, otn, hd, decision, term in sorted(viols + comp, key=lambda r: (r[2], r[0])):
        if rep > C.CUT:
            continue
        I = ident.p[pid]
        dist = I["dist"]
        conds = []
        if vtype == "N":
            conds.append("01")
            if rng.random() < 0.3:
                conds.append(COND[["report", "drugs", "curfew", "residence"][int(rng.integers(0, 4))]])
        else:
            k = 1 + int(rng.random() < 0.45) + int(rng.random() < 0.15)
            pool = list(COND.values())
            idx = rng.permutation(len(pool))[:k]
            conds = sorted(pool[i] for i in idx)
        h = holds.get(vid)
        jail = None
        if h:
            jail = ident.p[pid]["county"] if (_jail_draw(companion_of.get(vid, vid)) < 0.9) else C.COUNTIES[dist][0]
        decided = hd if hd <= C.CUT else None
        officer = officers[dist][int(rng.integers(0, 6))]
        rec = dict(vid=vid, doc=I["doc"], office=C.OFFICE[dist], rep=rep, otn=_otn(otn) if otn else "", conds=conds,
                   hold=h, jail=jail, decided=decided, decision=decision if decided else "", term=term,
                   rescind=resc.get(vid), officer=officer)
        if rep <= C.BOARD_MIGRATE_CUT:
            yr = rep.year
            nlegacy[yr] = nlegacy.get(yr, 0) + 1
            rec["case_no"] = "PB-%d-%05d" % (yr, nlegacy[yr] * 2 + int(rng.integers(0, 2)))
            if decided is not None and decided <= C.BOARD_MIGRATE_CUT:
                legacy.append(rec)
            else:
                # open at the close of 2 January 2026: migrated; the new system decides it, and the legacy system
                # also took the decision while entry ran in parallel
                new.append(dict(rec, migrated=True))
                if decided is not None and C.BOARD_GOLIVE <= decided <= C.BOARD_PARALLEL_END:
                    legacy.append(dict(rec, parallel=True))
                elif decided is None or decided > C.BOARD_PARALLEL_END:
                    legacy.append(dict(rec, decided=None, decision="", open_at_migration=True))
        else:
            new.append(dict(rec, migrated=False))
    return legacy, new


def write_board_legacy(path, legacy, admissions_by_doc):
    """the legacy case system's action table, one sheet per calendar year of the report: one row per action, a
    rescission as a later row on the same case; a hold that ended in a Department admission has no lift date, as
    the system recorded lifts only when it released the person itself"""
    import xlsxwriter
    import postprocess as PP
    import numpy as _np
    rng = C.stream("pack/legacy_postpone")
    sheets = {}
    for r in legacy:
        rows = sheets.setdefault(r["rep"].year, [])
        lodged = lifted = ""
        if r["hold"] and r["decided"] is not None and C.days(r["rep"], r["decided"]) > 12 and rng.random() < 0.3:
            # a hearing postponed before the decision: the action row repeats the case's detainer columns
            pd_ = C.add(r["rep"], int(rng.integers(5, C.days(r["rep"], r["decided"]) - 4)))
            rows.append([r["case_no"], r["doc"], r["office"], r["rep"], ",".join(r["conds"]), r["otn"], r["hold"][0], "",
                         (r["jail"] + " CJ") if r["jail"] else "", pd_, "POSTPONE", "", r["officer"]])
        if r["hold"]:
            lodged = r["hold"][0]
            lifted = r["hold"][1] if (r["hold"][1] is not None and r["decided"] is not None) else ""
        act = {"REVOKED": "REVOKE", "CONTINUED": "CONTINUE", "": ""}[r["decision"]]
        rows.append([r["case_no"], r["doc"], r["office"], r["rep"], ",".join(r["conds"]), r["otn"], lodged, lifted,
                     (r["jail"] + " CJ") if r["jail"] else "", r["decided"] or "", act,
                     r["term"] if act == "REVOKE" else "", r["officer"]])
        if r["rescind"] is not None and r["decided"] is not None and r["rescind"] <= C.BOARD_MIGRATE_CUT:
            rows.append([r["case_no"], r["doc"], r["office"], r["rep"], ",".join(r["conds"]), r["otn"], "", "", "",
                         r["rescind"], "RESCIND", "", r["officer"]])
    head = ["case_no", "doc_number", "office", "report_date", "conditions", "arrest_otn", "hold_lodged", "hold_lifted",
            "hold_facility", "action_date", "action", "term_days", "hearing_officer"]
    wb = xlsxwriter.Workbook(path, {"default_date_format": "mm/dd/yyyy", "strings_to_numbers": False})
    hf = wb.add_format({"bold": True, "bg_color": "#D9E1F2", "border": 1})
    df = wb.add_format({"num_format": "mm/dd/yyyy"})
    n = 0
    for yr in sorted(sheets):
        ws = wb.add_worksheet(str(yr))
        ws.freeze_panes(1, 0)
        for j, h in enumerate(head):
            ws.write(0, j, h, hf)
        widths = [14, 11, 7, 11, 14, 11, 11, 11, 14, 11, 9, 9, 10]
        for j, w in enumerate(widths):
            ws.set_column(j, j, w)
        rows = sorted(sheets[yr], key=lambda x: (x[3], x[0], str(x[9])))
        for i, row in enumerate(rows, start=1):
            for j, v in enumerate(row):
                if isinstance(v, dt.date):
                    ws.write_datetime(i, j, dt.datetime(v.year, v.month, v.day), df)
                elif v == "":
                    continue
                else:
                    ws.write(i, j, v)
        n += len(rows)
    wb.close()
    return n


def _hearing_time(doc, d):
    import hashlib
    h = int(hashlib.sha256(("hearing/%s/%s" % (doc, d.isoformat())).encode()).hexdigest()[:8], 16)
    return 9 + h % 8, (h // 8) % 60


def write_board_new(path, new):
    """the new case system's decisions export: one row per case, migrated cases flagged by where they opened; a
    rescinded revocation keeps its row with the rescission date; hold dates as the jail reported them"""
    rng = C.stream("pack/boardnew")
    rows = []
    seq = 0
    for r in sorted(new, key=lambda x: (x["rep"], x["vid"])):
        seq += 1
        case_id = "VR%07d" % (2604000 + seq * 3 + int(rng.integers(0, 3)))
        hs = he = ""
        if r["hold"]:
            hs = r["hold"][0].isoformat()
            end = r["hold"][1] if r["hold"][1] is not None else r["hold"][2]
            if end is not None and end <= C.CUT:
                he = end.isoformat()
        dec = r["decision"]
        rdate = ""
        if dec == "REVOKED" and r["rescind"] is not None and r["rescind"] <= C.CUT:
            rdate = r["rescind"].isoformat()
        conds = "; ".join(COND_TEXT[c] for c in r["conds"])
        rows.append((case_id, r["doc"], r["office"], "LEGACY" if r["migrated"] else "NEW", r["rep"].isoformat(), r["otn"],
                     conds, (r["jail"] + " County Jail") if r["jail"] else "", hs, he,
                     dec, (r["decided"].isoformat() + "T%02d:%02d:00-05:00" % _hearing_time(r["doc"], r["decided"]))
                     if r["decided"] else "", r["term"] if dec == "REVOKED" else "", rdate, r["officer"]))
    head = ("case_id", "doc_number", "office", "opened_in", "report_date", "arrest_otn", "conditions_cited",
            "hold_facility", "hold_start", "hold_end", "decision", "decision_ts", "revocation_term_days",
            "rescinded_date", "hearing_officer")
    return C.write_csv(path, head, rows)


def write_projection(path, cohort, ident, book):
    rng = C.stream("pack/projection")
    rows = []
    newid = {}
    for p in cohort:
        if p["inrecord"]:
            I = ident.p[p["pid"]]
        else:
            I = ident.p[p["pid"]]
        q = dict(p)
        score = W.risk_score(q, rng)
        mv = "RPR" if p["rtype"] == "REPAROLE" else "PAR"
        maxd = C.add(p["rel0"], p["term0"])
        rows.append((I["doc"], p["rel0"].isoformat(), mv, mdy(I["birth"]), I["sex"], I["county"].upper(), p["off"].upper(),
                     p["priors"], score, maxd.isoformat()))
    rows.sort(key=lambda r: (r[1], r[0]))
    head = ("doc_number", "projected_release_date", "projected_movement", "birth_date", "sex", "county_of_commitment",
            "governing_offense", "prior_commitments", "prat_total", "max_expiration_date")
    return C.write_csv(path, head, rows)
