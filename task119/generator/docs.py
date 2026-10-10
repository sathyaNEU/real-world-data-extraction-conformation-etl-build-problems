"""The constructed documents and workbooks, written through writers.py."""
import datetime as dt

import numpy as np

import texts as T
import writers as WR
import corpus
from common import rng, PEOPLE

PROVENANCE = {
    "referrals": ("Constructed: regional critical care referral log, platform and migrated legacy rows", "2026-08-14"),
    "stays": ("Constructed: network level-3 unit feed", "2026-08-14"),
    "returns": ("Constructed: daily 08:00 bed returns computed from the unit feed", "2026-08-14"),
    "episodes": ("Constructed: admitted patient care episodes with linked date of death", "2026-08-14"),
    "register": ("Constructed: effective-dated unit register", "2026-08-14"),
    "capacity": ("Constructed: network monthly capacity report computed from the returns and referral log", "2026-08-20"),
    "remit": ("Constructed: board terms of reference for the review", "2026-09-17"),
    "guide": ("Constructed: extract field guide and folder contents", "2026-09-28"),
    "reviewlog": ("Constructed: national programme log of closed reviews, computed from the review records", "2026-03-31"),
    "reviewdb": ("Constructed: national programme review records (SQLite)", "2026-03-31"),
    "levels": ("Constructed: legacy referral level entries", "2024-04-01"),
    "legacyspec": ("Constructed: legacy export specification", "2024-02-12"),
    "links": ("Constructed: patient key links", "2026-08-14"),
    "apcspec": ("Constructed: episode extract specification", "2026-08-14"),
    "boardpaper": ("Constructed: network board paper", "2023-11-21"),
    "transfers": ("Constructed: inter-hospital transfer audit", "2026-08-14"),
    "theatre": ("Constructed: theatre case extract for referred and unit patients", "2026-08-14"),
    "thread": ("Constructed: correspondence", "2026-09-25"),
    "l2returns": ("Constructed: level-2 unit bed returns", "2026-08-14"),
    "ambulance": ("Constructed: ambulance handover extract", "2026-08-14"),
}

FILE_TABLE = {
    "referrals": ("Regional referral platform", "Decisions to admit 1 July 2023 to 30 June 2026, levels 2 and 3, all "
                                                "eight trusts, with the migrated CCRS referrals"),
    "stays": ("Network unit feed", "Stays at the level 3 units present on 1 June 2023 or admitted to 30 June 2026"),
    "returns": ("Network daily bed returns", "Level 3 units, 1 June 2023 to 30 June 2026"),
    "register": ("Network unit register", "Every row"),
    "episodes": ("Regional data service", "Episodes of referred patients; see the extract specification"),
    "apcspec": ("Regional data service", "Specification for the episode and theatre extracts"),
    "links": ("Regional data service", "Patient key links"),
    "theatre": ("Regional data service", "Theatre cases of referred and unit patients; see the extract specification"),
    "levels": ("CCRS, exported at switch-off", "Referral level entries"),
    "legacyspec": ("CCRS application support", "Export specification used for the migration"),
    "transfers": ("Network transfer audit", "Every transfer between trusts to a critical care unit"),
    "capacity": ("Network manager", "Monthly capacity report as refreshed on 20 August 2026"),
    "boardpaper": ("Network board", "Paper ACCN/23/41, November 2023"),
    "remit": ("Wenmarsh Regional Health Board", "Paper WRHB/26/097, terms of reference"),
    "reviewlog": ("National Rapid Review Programme", "Closed escalation reviews in the four neighbouring regions"),
    "reviewdb": ("National Rapid Review Programme", "Review database: the reviewed years' referrals, unit stays, "
                                                    "bed returns and patient outcomes"),
    "thread": ("Correspondence", "September 2026"),
    "l2returns": ("Network daily bed returns", "Level 2 units, July 2025 to June 2026"),
    "ambulance": ("Ambulance service", "Hospital handover extract, July 2025 to June 2026"),
}


# ------------------------------------------------------------------------------------------ capacity report
def capacity_report(path, occ_rows, wait_rows):
    when = dt.datetime(2026, 8, 20, 11, 5)
    wb = WR.xlsx_book(path, "Monthly capacity report", "Maria Reynolds", "Wenmarsh Adult Critical Care Network", when)
    bold = wb.add_format({"bold": True})
    hd = wb.add_format({"bold": True, "bottom": 1, "text_wrap": True, "valign": "top"})
    one = wb.add_format({"num_format": "0.0"})
    ws = wb.add_worksheet("Read me")
    ws.set_column(0, 0, 118)
    for i, line in enumerate(T.CAPACITY_NOTES):
        ws.write_string(i, 0, line, bold if i == 0 else None)
    ws2 = wb.add_worksheet("Occupancy 0800")
    cols = ["month", "unit", "days", "beds_open", "occupied_0800_mean", "occupancy_0800_pct"]
    heads = ["Month", "Unit", "Days reported", "Beds open (mean)", "Occupied at 08:00 (mean)", "Occupancy at 08:00 (%)"]
    for j, h in enumerate(heads):
        ws2.write_string(0, j, h, hd)
    for i, r in enumerate(occ_rows, start=1):
        ws2.write_string(i, 0, r["month"])
        ws2.write_string(i, 1, r["unit"])
        ws2.write_number(i, 2, r["days"])
        ws2.write_number(i, 3, r["beds_open"], one)
        ws2.write_number(i, 4, r["occupied_0800_mean"], one)
        ws2.write_number(i, 5, r["occupancy_0800_pct"], one)
    ws2.set_column(0, 1, 11)
    ws2.set_column(2, 5, 15)
    ws2.freeze_panes(1, 0)
    ws3 = wb.add_worksheet("Referral waits")
    heads = ["Month", "Referring trust", "Level 3 referrals", "Waiting over 4 hours from receipt"]
    for j, h in enumerate(heads):
        ws3.write_string(0, j, h, hd)
    for i, r in enumerate(wait_rows, start=1):
        ws3.write_string(i, 0, r["month"])
        ws3.write_string(i, 1, r["trust"])
        ws3.write_number(i, 2, r["level3_referrals"])
        ws3.write_number(i, 3, r["over_4h_from_receipt"])
    ws3.set_column(0, 1, 14)
    ws3.set_column(2, 3, 18)
    ws3.freeze_panes(1, 0)
    WR.close_xlsx(wb, path, "Wenmarsh Adult Critical Care Network", when)
    return len(occ_rows) + len(wait_rows)


# ------------------------------------------------------------------------------------------ review log and records
def review_meta(revs):
    r = rng("reviewlog")
    seq = {}
    meta = []
    for rev in revs:
        closed_year = rev["year"] + 1
        seq[closed_year] = seq.get(closed_year, 0) + 1
    order = sorted(range(len(revs)), key=lambda i: (revs[i]["year"], revs[i]["region"], revs[i]["trust"]))
    counter = {}
    for i in order:
        rev = revs[i]
        cy = rev["year"] + 1
        counter[cy] = counter.get(cy, 0) + 1
        ref = "NRR-ESC-%02d-%02d" % (cy % 100, counter[cy])
        opened = dt.date(cy, 2, 15) + dt.timedelta(days=int(r.integers(0, 110)))
        closed = opened + dt.timedelta(days=int(r.integers(70, 130)))
        attempts = [{"attempt": 1, "opened": opened, "closed": closed,
                     "sampled": max(12, rev["n"] + int(r.integers(6, 16))), "confirmed": rev["n"]}]
        if rev["n"] == 0:
            o2 = closed + dt.timedelta(days=int(r.integers(20, 45)))
            c2 = o2 + dt.timedelta(days=int(r.integers(55, 90)))
            attempts.append({"attempt": 2, "opened": o2, "closed": c2, "sampled": attempts[0]["sampled"] * 2,
                             "confirmed": 0})
        meta.append((i, ref, attempts))
    return meta


def visible_columns(rev):
    pats = rev["patients"]
    l3 = [p for p in pats if p["level_dec"] == 3]
    screen = sum(1 for p in l3 if p["outcome"] != "stood_down"
                 and ((p["assigned"] if p["assigned"] is not None else p["end"]) - p["received"]) > 240)
    d30 = sum(1 for p in l3 if p["death"] is not None and (p["death"] - corpus.to_date(p["dta"])).days <= 30)
    occ = round(float(np.mean([x[2] for x in rev["returns"]])), 1)
    return len(pats), screen, occ, d30


def review_files(xlsx_path, db_path, revs):
    meta = review_meta(revs)
    when = dt.datetime(2026, 3, 31, 15, 20)
    wb = WR.xlsx_book(xlsx_path, "Thematic escalation reviews closed 2021 to 2025", "Sharon Banks",
                      "National Rapid Review Programme", when)
    hd = wb.add_format({"bold": True, "bottom": 1, "text_wrap": True, "valign": "top"})
    dfmt = wb.add_format({"num_format": "yyyy-mm-dd"})
    one = wb.add_format({"num_format": "0.0"})
    ws = wb.add_worksheet("Reviews")
    heads = ["Review ref", "Region", "Trust", "Trust type", "Level 3 beds", "Year reviewed", "Referrals in year",
             "Level 3 referrals waiting over 4h from receipt", "Mean beds occupied at 08:00",
             "Level 3 referrals: deaths within 30 days (all causes)", "Attempts", "First opened", "Closed",
             "Deaths confirmed avoidable"]
    for j, h in enumerate(heads):
        ws.write_string(0, j, h, hd)
    rows = sorted(meta, key=lambda m: m[1])
    for k, (i, ref, att) in enumerate(rows, start=1):
        rev = revs[i]
        nref, screen, occ, d30 = visible_columns(rev)
        vals = [ref, rev["region"], rev["trust"], rev["type"], rev["beds"], rev["year"], nref, screen, occ, d30,
                len(att)]
        for j, v in enumerate(vals):
            if isinstance(v, str):
                ws.write_string(k, j, v)
            elif j == 8:
                ws.write_number(k, j, v, one)
            else:
                ws.write_number(k, j, v)
        ws.write_datetime(k, 11, dt.datetime.combine(att[0]["opened"], dt.time()), dfmt)
        ws.write_datetime(k, 12, dt.datetime.combine(att[-1]["closed"], dt.time()), dfmt)
        ws.write_number(k, 13, att[-1]["confirmed"])
    ws.set_column(0, 0, 14)
    ws.set_column(1, 3, 16)
    ws.set_column(4, 13, 13)
    ws.freeze_panes(1, 0)
    ws2 = wb.add_worksheet("Attempts")
    heads = ["Review ref", "Attempt", "Opened", "Closed", "Case notes sampled", "Deaths confirmed avoidable", "Note"]
    for j, h in enumerate(heads):
        ws2.write_string(0, j, h, hd)
    k = 1
    for i, ref, att in rows:
        for a in att:
            ws2.write_string(k, 0, ref)
            ws2.write_number(k, 1, a["attempt"])
            ws2.write_datetime(k, 2, dt.datetime.combine(a["opened"], dt.time()), dfmt)
            ws2.write_datetime(k, 3, dt.datetime.combine(a["closed"], dt.time()), dfmt)
            ws2.write_number(k, 4, a["sampled"])
            ws2.write_number(k, 5, a["confirmed"])
            note = ""
            if len(att) > 1 and a["attempt"] == 1:
                note = "Nothing confirmed; reopened with a doubled case-note sample"
            elif a["attempt"] == 2:
                note = "Nothing confirmed on the doubled sample; closed"
            ws2.write_string(k, 6, note)
            k += 1
    ws2.set_column(0, 0, 14)
    ws2.set_column(1, 5, 13)
    ws2.set_column(6, 6, 58)
    ws3 = wb.add_worksheet("About")
    ws3.set_column(0, 0, 112)
    about = [
        "National Rapid Review Programme: thematic escalation reviews",
        "Closed reviews in the Haskminster, Isterdale, Tevermouth and Morrowcombe regions, 2021 to 2025.",
        "Each review examined one trust's adult referrals for critical care over one calendar year and reports the "
        "deaths its reviewers confirmed as avoidable.",
        "The reviewed years' records are in the programme's review database (nrr_review_records.sqlite).",
        "Coordinator: Sharon Banks. Issued 31 March 2026.",
    ]
    for i, line in enumerate(about):
        ws3.write_string(i, 0, line)
    WR.close_xlsx(wb, xlsx_path, "National Rapid Review Programme", when)
    # ---- the database
    schema = [
        "CREATE TABLE reviews (review_ref TEXT PRIMARY KEY, region TEXT, trust TEXT, unit_code TEXT, "
        "level3_beds INTEGER, period_start TEXT, period_end TEXT)",
        "CREATE TABLE referrals (review_ref TEXT, referral_ref TEXT, received_at TEXT, decision_at TEXT, "
        "level_requested INTEGER, level_decided INTEGER, outcome TEXT, bed_assigned_at TEXT, arrived_at TEXT, "
        "outcome_at TEXT)",
        "CREATE TABLE unit_stays (review_ref TEXT, stay_ref TEXT, referral_ref TEXT, admitted_at TEXT, "
        "discharged_at TEXT, admission_type TEXT)",
        "CREATE TABLE bed_returns (review_ref TEXT, return_date TEXT, beds_open INTEGER, beds_occupied_0800 INTEGER)",
        "CREATE TABLE patient_outcomes (review_ref TEXT, referral_ref TEXT, hospital_discharge_date TEXT, "
        "date_of_death TEXT)",
    ]
    t_rev, t_ref, t_st, t_ret, t_out = [], [], [], [], []
    for i, ref, att in rows:
        rev = revs[i]
        code = rev["trust"][:3].upper() + "-ICU"
        t_rev.append((ref, rev["region"], rev["trust"], code, rev["beds"], "%d-01-01" % rev["year"],
                      "%d-12-31" % rev["year"]))
        order = sorted(range(len(rev["patients"])), key=lambda k: (rev["patients"][k]["received"], k))
        rr = {}
        for n_, k in enumerate(order, start=1):
            p = rev["patients"][k]
            rid = "%s/%05d" % (ref[-5:], n_ * 3 + (k % 3))
            rr[k] = rid
            outc = {"admitted": "admitted", "died": "died before admission", "stood_down": "stood down"}[p["outcome"]]
            t_ref.append((ref, rid, corpus.to_str(p["received"]), corpus.to_str(p["dta"]), p["level_req"],
                          p["level_dec"], outc, corpus.to_str(p["assigned"]) if p["assigned"] is not None else None,
                          corpus.to_str(p["arrived"]) if p["arrived"] is not None else None, corpus.to_str(p["end"])))
            t_out.append((ref, rid, p["hosp_out"].isoformat(), p["death"].isoformat() if p["death"] else None))
        for k, s in enumerate(sorted(rev["stays"], key=lambda s: (s["admit"], str(s["key"]))), start=1):
            t_st.append((ref, "%s/S%05d" % (ref[-5:], k), rr.get(s["key"]) if s["key"] >= 0 else None,
                         corpus.to_str(s["admit"]), corpus.to_str(s["discharge"]), s["type"]))
        for d, beds, occ in rev["returns"]:
            t_ret.append((ref, d.isoformat(), beds, occ))
    t_ref.sort(key=lambda x: (x[0], x[2], x[1]))
    t_out.sort(key=lambda x: (x[0], x[1]))
    WR.write_sqlite(db_path, schema, [
        ("reviews", ["review_ref", "region", "trust", "unit_code", "level3_beds", "period_start", "period_end"], t_rev),
        ("referrals", ["review_ref", "referral_ref", "received_at", "decision_at", "level_requested", "level_decided",
                       "outcome", "bed_assigned_at", "arrived_at", "outcome_at"], t_ref),
        ("unit_stays", ["review_ref", "stay_ref", "referral_ref", "admitted_at", "discharged_at", "admission_type"],
         t_st),
        ("bed_returns", ["review_ref", "return_date", "beds_open", "beds_occupied_0800"], t_ret),
        ("patient_outcomes", ["review_ref", "referral_ref", "hospital_discharge_date", "date_of_death"], t_out)])
    return len(rows), len(t_ref)


# ------------------------------------------------------------------------------------------ documents
def remit(path):
    WR.write_docx(path, T.REMIT_TITLE, T.REMIT, "Andrea Davey", dt.datetime(2026, 9, 17, 16, 40),
                  "Wenmarsh Regional Health Board")


def field_guide(path, F, n, distractors):
    blocks = [("p", x) for x in T.GUIDE_INTRO]
    blocks.append(("h", "1. Files in this folder"))
    rows = [["File", "From", "Covers"]]
    for k, name in F.items():
        if k == "guide":
            continue
        src, cov = FILE_TABLE[k]
        rows.append([name, src, cov])
    blocks.append(("table", {"rows": rows, "widths": [228, 96, 146]}))
    sec = 2
    for fname, fields in T.GUIDE_FIELDS.items():
        blocks.append(("h", "%d. %s" % (sec, fname)))
        tab = [["Field", "Definition"]] + [[a, b] for a, b in fields]
        blocks.append(("table", {"rows": tab, "widths": [110, 360]}))
        sec += 1
    blocks.append(("small", "Questions on this extract to Diana Smith, Information Manager."))
    WR.write_pdf(path, T.GUIDE_TITLE, T.GUIDE_SUB, T.GUIDE_BY, blocks, "Diana Smith",
                 dt.datetime(2026, 9, 28, 15, 10), "Wenmarsh Regional Health Board")


def legacy_spec(path):
    blocks = []
    for kind, val in T.LEGACY:
        if kind == "table":
            blocks.append(("table", {"rows": val, "widths": [170, 150]}))
        else:
            blocks.append((kind, val))
    WR.write_pdf(path, T.LEGACY_TITLE, T.LEGACY_SUB, None, blocks, "CCRS application support",
                 dt.datetime(2024, 2, 12, 10, 30), "Wenmarsh network informatics")


def apc_spec(path):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(T.APC_SPEC)


def board_paper(path):
    WR.write_pdf(path, T.BOARD_PAPER_TITLE, T.BOARD_PAPER_SUB, T.BOARD_PAPER_BY, T.BOARD_PAPER, "Maria Reynolds",
                 dt.datetime(2023, 11, 14, 9, 50), "Wenmarsh Adult Critical Care Network")


EMAIL = {"requester": "andrea.davey@wenmarsh-rhb.org", "chair": "norman.scott@wenmarsh-rhb.org",
         "network": "maria.reynolds@wenmarsh-accn.org", "info": "diana.smith@wenmarsh-rhb.org",
         "programme": "sharon.banks@nrr-programme.org"}


def thread(path, F):
    def who(k):
        return "%s <%s>" % (PEOPLE[k][0], EMAIL[k])

    msgs = [
        ("requester", ["network", "info"], "Mon, 21 Sep 2026 09:12:41 +0100", "External review placement: data and papers",
         "Maria, Diana,\n\nThe board approved the terms of reference on 17 September as drafted, so the placement "
         "paper goes to the November meeting. Could you put the network data and anything else I will need in the "
         "shared folder by the end of the month? I will write the paper from there.\n\nThanks,\nAndrea\n\n-- \n"
         "Andrea Davey\nHead of Quality Surveillance\nWenmarsh Regional Health Board"),
        ("info", ["requester"], "Tue, 22 Sep 2026 16:40:07 +0100", "RE: External review placement: data and papers",
         "Andrea,\n\nThe extract is in the folder with a field guide. The referral record before April 2024 is the "
         "CCRS data that was loaded into the platform at go-live. For background, this is the notice we sent round "
         "before go-live:\n\n"
         "---------- Forwarded message ----------\n"
         "From: Wenmarsh network informatics\nDate: Wed, 14 Feb 2024 11:02\n"
         "Subject: Critical care referral platform: go-live on 2 April 2024\n\n"
         "The regional referral platform goes live for every ward on 2 April 2024. From 19 February the pilot wards "
         "(the acute medical unit and one further ward at each trust) will enter each critical care referral on both "
         "CCRS and the platform while staff are trained. At go-live the CCRS referral records will be loaded into "
         "the platform record, so the platform holds the history from July 2023, and CCRS becomes read-only.\n"
         "----------\n\nDiana\n\n-- \nDiana Smith\nInformation Manager"),
        ("network", ["requester", "info"], "Wed, 23 Sep 2026 08:05:55 +0100", "RE: External review placement: data and papers",
         "Andrea,\n\nA few notes from the network side, for what they are worth.\n\nStennock's unit is full every "
         "morning and has been for years. Brackenford reports empty beds most mornings; I have always thought it "
         "could take more of its own patients if it held on to those beds. Prideswick still only accepts weekend "
         "admissions once the on-call consultant intensivist has seen the patient on site. That is their unit's "
         "rule, not a network one, and it has come up at the network board twice.\n\nThe capacity report in the "
         "folder is as it stood on 20 August.\n\nMaria\n\n-- \nMaria Reynolds\nCritical Care Network Manager"),
        ("chair", ["requester"], "Thu, 24 Sep 2026 18:22:13 +0100", "RE: External review placement: data and papers",
         "Andrea,\n\nThanks for the update. My view hasn't changed since we spoke: send the reviewers to wherever "
         "the most patients die waiting for a bed. I would like the board to see that first.\n\nNorman"),
        ("programme", ["requester"], "Fri, 25 Sep 2026 10:47:30 +0100", "RE: External review placement: data and papers",
         "Andrea,\n\nAs promised, our log of closed escalation reviews in the four neighbouring regions and the "
         "review database behind it are now in your folder. I will bring the programme screen to the November "
         "board as agreed.\n\nBest wishes,\nSharon\n\n-- \nSharon Banks\nProgramme Coordinator, National Rapid Review "
         "Programme"),
    ]
    parts = []
    mid = 0
    for frm, to, date, subj, body in reversed(msgs):
        mid += 1
        parts.append("From: %s\nTo: %s\nDate: %s\nSubject: %s\nMessage-ID: <placement.%04d@wenmarsh-rhb.org>\n\n%s\n"
                     % (who(frm), ", ".join(who(t) for t in to), date, subj, 7300 + mid, body))
    head = ("From: %s\nTo: %s\nDate: Fri, 25 Sep 2026 10:47:30 +0100\nSubject: RE: External review placement: data "
            "and papers\nMIME-Version: 1.0\nContent-Type: text/plain; charset=utf-8\nContent-Transfer-Encoding: 8bit\n"
            "X-Folder: Quality surveillance / External review 2027-28\n\n" % (who("programme"), who("requester")))
    body = "\n-----Original message-----\n".join(parts)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(head + body + "\nWenmarsh Regional Health Board. This email is for its addressees only.\n")
