"""task482 architecture 17: writes the pack under target/ from the truth (world.py) and the bank runs (core.py)."""
import csv
import datetime as dt
import json
import os
from email.message import EmailMessage
from email.utils import format_datetime

import numpy as np
import openpyxl
from openpyxl.styles import Font

import core as C
import docs as D
import golden as G
import params as P
import postprocess as PP
import rasch as RA
import world as W

UTC = dt.timezone.utc
VARIANTS = {"U1": ["Matter and reactions", "Chemistry: matter", "Particles and reactions", "Matter"],
            "U2": ["Cells and body systems", "Cells & systems", "Body systems", "Life processes"],
            "U3": ["Electricity and magnetism", "Electricity", "Circuits and magnets", "Electricity & magnetism"],
            "U4": ["Space and the solar system", "Space", "Solar system", "Astronomy"],
            "U5": ["Forces and motion", "Motion and forces", "Forces", "Mechanics: forces and motion", "Forces & motion"],
            "U6": ["Earth's systems", "Dynamic Earth", "Earth systems", "Plate tectonics and the rock cycle",
                   "Our changing Earth"]}
FILES = ["y10sci_aug2026_responses.csv", "y10sci_aug2026_sessions.csv", "corlinn_item_bank_2026.xlsx",
         "bank_calibration_runs.csv", "item_renumbering_2025.csv", "y10sci_2027_drafts.xlsx",
         "y10sci_paper_specification_2027.pdf", "standard_setting_record_y10sci.pdf", "council_minute_2026_10_14.pdf",
         "y10sci_course_review_2026.pdf", "member_schools.csv", "paper_choice_request.eml",
         "entries_register_aug2026.xlsx", "makeup_roster_aug2026.pdf", "makeup_scripts_keyed.csv",
         "candidate_survey_2026.csv", "member_bell_times_2026.json"]


def _csv(path, head, rows):
    with open(path, "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\r\n")
        wr.writerow(head)
        wr.writerows(rows)


def _utc(t):
    return t.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _xlsx(path, sheets, creator, created, modified, widths=None):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for name, head, rows in sheets:
        ws = wb.create_sheet(name)
        if head:
            ws.append(head)
            for c in ws[1]:
                c.font = Font(bold=True)
        for r in rows:
            ws.append(r)
        for j, wd in enumerate((widths or {}).get(name, [])):
            ws.column_dimensions[openpyxl.utils.get_column_letter(j + 1)].width = wd
        if head:
            ws.freeze_panes = "A2"
    wb.save(path)
    PP.normalize_ooxml(path, creator, creator, created, modified, excel=True, company=P.TRUST)


def _d(d, fmt):
    return d.strftime(fmt).replace(" 0", " ").lstrip("0")


def build(target):
    os.makedirs(target, exist_ok=True)
    for f in os.listdir(target):
        os.remove(os.path.join(target, f))
    res = G.compute()
    w, pl, sch, a = res["w"], res["w"]["pool"], res["w"]["schools"], res["w"]["asks"]
    items = pl["items"]
    b_bank = res["b_bank"]
    g = np.random.default_rng(P.SEED + 11)
    code_of = {i: it["code"] for i, it in enumerate(items)}
    t = lambda f: os.path.join(target, f)

    # ---- the response export and the session log
    _csv(t("y10sci_aug2026_responses.csv"), ["session_id", "entry_no", "item_code", "score"],
         [("S%07d" % sid, entry, code_of[i], int(v)) for sid, entry, i, v in w["rows"]])
    _csv(t("y10sci_aug2026_sessions.csv"),
         ["session_id", "entry_no", "school_code", "form", "started_utc", "ended_utc", "status"],
         [("S%07d" % s["sid"], s["entry"], s["school"], "F%d" % (s["form"] + 1), _utc(s["start"]), _utc(s["end"]),
           s["status"]) for s in w["sessions"]])

    # ---- the bank, its runs and the renumbering
    _, thb = C.bank_run(w)
    infit, outfit = RA.fit_stats(w["R"], w["M"], thb, b_bank)
    p = RA.sig(thb[:, None] - b_bank[None, :])
    se = 1.0 / np.sqrt(np.maximum((p * (1 - p) * w["M"]).sum(0), 1e-9))
    n = w["M"].sum(0)
    order = sorted(range(len(items)), key=lambda i: items[i]["code"])
    rows = [[items[i]["code"], items[i]["unit"], items[i]["strand"], "MC" if items[i]["mc"] else "SA",
             "Y" if items[i]["anchor"] else "N", round(float(b_bank[i]), 3), round(float(se[i]), 3), int(n[i]),
             round(float(infit[i]), 2), round(float(outfit[i]), 2)] for i in order]
    notes = [["Year 10 Science item bank: final 2026 calibration, run 7 September 2026 on every online response of the "
              "August 2026 sitting."],
             ["Difficulties are Rasch logits on the bank scale. The scale is held by the anchor block (anchor = Y) at its "
              "banked values, set in 2024."],
             ["The final run supersedes the preliminary run of 21 August 2026 (sessions to 19 August); both are in the "
              "calibration runs file."],
             ["Units U1 to U6 are the core units of the course outline. Fit is information-weighted (infit) and "
              "unweighted (outfit) mean square."]]
    _xlsx(t("corlinn_item_bank_2026.xlsx"),
          [("Bank", ["item_code", "unit", "strand", "type", "anchor", "difficulty", "se", "responses_2026", "infit",
                     "outfit"], rows), ("Notes", None, notes)],
          "Jeremy York", "2026-09-07T03:40:00Z", "2026-09-08T22:15:00Z",
          {"Bank": [11, 6, 24, 6, 7, 10, 7, 14, 7, 7], "Notes": [120]})
    b_pre, _ = C.bank_run(w, upto=P.PRELIM_CUTOFF)
    g25 = np.random.default_rng(P.POOL_SEED + 25)
    runs = []
    for i in order:
        it = items[i]
        if it["anchor"]:
            v25 = float(pl["b"][i])
        elif g25.random() < (0.6 if it["term"] < 3 else 0.5):
            v25 = round(float(b_bank[i] + g25.normal(0, 0.06)), 3)
        else:
            v25 = None
        if v25 is not None:
            runs.append(("2025 final", it["code"], "%.3f" % v25))
    for i in order:
        runs.append(("2026 preliminary", items[i]["code"], "%.3f" % b_pre[i]))
    for i in order:
        runs.append(("2026 final", items[i]["code"], "%.3f" % b_bank[i]))
    _csv(t("bank_calibration_runs.csv"), ["run", "item_code", "difficulty"], runs)
    used = {it["card"] for it in items}
    retired = []
    while len(retired) < 18:
        c = int(g.integers(1040, 4990))
        if c not in used and c not in retired:
            retired.append(c)
    ren = [(it["card"], it["code"], "2025-02-01", "renumbered") for it in items] + \
          [(c, "", "2025-02-01", "retired") for c in retired]
    ren.sort()
    _csv(t("item_renumbering_2025.csv"), ["card_no", "item_code", "effective_from", "status"], ren)

    # ---- the drafts (card numbers, the panels' unit words)
    sheets = []
    for d in ("A", "B", "C"):
        ix = sorted(res["drafts"][d], key=lambda i: (items[i]["strand"], items[i]["unit"], items[i]["card"]))
        sheets.append(("Paper %s" % d, ["Q", "Card", "Unit", "Marks"],
                       [[q + 1, items[i]["card"], VARIANTS[items[i]["unit"]][0], 1] for q, i in enumerate(ix)]))
    _xlsx(t("y10sci_2027_drafts.xlsx"), sheets, "Paul Shailer", "2026-10-28T01:20:00Z", "2026-11-02T20:05:00Z",
          {"Paper %s" % d: [5, 8, 30, 7] for d in "ABC"})

    # ---- governing documents
    D.specification(t("y10sci_paper_specification_2027.pdf"))
    cuts = []
    for f in range(P.N_FORMS):
        bf = b_bank[pl["forms"][f]]
        for r in range(P.PAPER_LEN + 1):
            if r == 0 or r == P.PAPER_LEN:
                continue
            th = 0.0
            for _ in range(40):
                pp = RA.sig(th - bf)
                th += (r - pp.sum()) / max((pp * (1 - pp)).sum(), 1e-9)
            if th >= P.THETA_ACHIEVED:
                cuts.append((f, r))
                break
    D.standards(t("standard_setting_record_y10sci.pdf"), cuts)
    D.minute(t("council_minute_2026_10_14.pdf"))

    # ---- the course review with the member schools' sequences
    seq = []
    for s in sorted(sch, key=lambda s: s["name"]):
        ts, te = s["term_start"], s["term_end"]
        nwk = W.week_of_term(te, ts)
        k = s["week_end1"]
        n1, n2 = VARIANTS[s["first"]][int(g.integers(len(VARIANTS[s["first"]])))], \
            VARIANTS[s["second"]][int(g.integers(len(VARIANTS[s["second"]])))]
        fmt = int(g.integers(3))
        if fmt == 0:
            t3 = "Wks 1-%d %s; Wks %d-%d %s" % (k, n1, k + 1, nwk, n2)
        elif fmt == 1:
            t3 = "%d/%d to %d/%d %s; %d/%d to %d/%d %s" % (ts.day, ts.month, s["end1"].day, s["end1"].month, n1,
                                                            (s["end1"] + dt.timedelta(days=3)).day,
                                                            (s["end1"] + dt.timedelta(days=3)).month, te.day, te.month, n2)
        else:
            t3 = "Weeks 1 to %d: %s. Weeks %d to %d: %s." % (k, n1, k + 1, nwk, n2)
        u12 = ["U1", "U2"] if g.random() < 0.5 else ["U2", "U1"]
        u34 = ["U3", "U4"] if g.random() < 0.5 else ["U4", "U3"]
        nm = lambda u: VARIANTS[u][int(g.integers(len(VARIANTS[u])))]
        t12 = "T1: %s, %s. T2: %s, %s." % (nm(u12[0]), nm(u12[1]), nm(u34[0]), nm(u34[1]))
        start = [ts.strftime("%d %b").lstrip("0"), ts.strftime("%a %d %B").replace(" 0", " "),
                 ts.strftime("%d/%m/%Y")][int(g.integers(3))]
        seq.append([s["name"], start, t12, t3])
    D.course_review(t("y10sci_course_review_2026.pdf"), sch, seq)

    # ---- member schools
    moe = g.choice(np.arange(1100, 9800), len(sch), replace=False)
    _csv(t("member_schools.csv"), ["school_code", "school_name", "region", "moe_number"],
         sorted([(s["code"], s["name"], s["region"], int(m)) for s, m in zip(sch, moe)]))

    # ---- the request
    msg = EmailMessage()
    msg["From"] = "Paul Shailer <p.shailer@corlinn.org.nz>"
    msg["To"] = "Jeremy York <j.york@corlinn.org.nz>"
    msg["Cc"] = "Theo Stevens <t.stevens@corlinn.org.nz>"
    msg["Date"] = format_datetime(dt.datetime(2026, 11, 6, 16, 42, tzinfo=D.NZDT))
    msg["Subject"] = "2027 Year 10 science paper"
    msg["Message-ID"] = "<20261106164200.4821@corlinn.org.nz>"
    msg.set_content(
        "Hi Jeremy,\n\nThe Council meets on 2 December to set the 2027 Year 10 science paper. The three "
        "drafts came back from the panels last week and are in the drafts workbook, with the 2027 specification.\n\n"
        "Could you work up the recommendation for the Council? Theo would like the working in a workbook he can "
        "pass round. For the Council's annual report, could the same workbook carry the August sitting's entries "
        "and sittings by region, and the make-up sitting's numbers and marks?\n\nEverything from the August sitting "
        "is in the shared folder.\n\nThanks\n\nPaul Shailer\nHead of Assessment\n%s\n" % P.TRUST)
    with open(t("paper_choice_request.eml"), "wb") as fh:
        fh.write(bytes(msg))

    # ---- the entries register
    ent = sorted(a["entries"], key=lambda e: (e["entered"], e["school"], e["entry"]))
    _xlsx(t("entries_register_aug2026.xlsx"),
          [("Entries", ["Entry no", "NSN", "Surname", "First name", "Date of birth", "Gender", "School code",
                        "Entered on", "Source", "Status"],
            [[e["entry"], e["nsn"], e["surname"], e["first"], e["dob"], e["gender"], e["school"], e["entered"],
              e["source"], e["status"]] for e in ent]),
           ("Notes", None, [["Entries for the August 2026 Year 10 Science Benchmark, as at 31 August 2026."],
                            ["Status: E entered; W withdrawn by the school before the sitting (a withdrawn entry is not "
                             "a candidate)."],
                            ["Source: school upload, or office (taken by the office from a school's email or phone "
                             "call; the office form does not record the NSN)."]])],
          "Corlinn Trust Office", "2026-05-18T21:10:00Z", "2026-08-30T23:52:00Z",
          {"Entries": [10, 11, 14, 12, 12, 7, 11, 12, 13, 7], "Notes": [110]})
    for path in [t("entries_register_aug2026.xlsx")]:
        pass

    # ---- the make-up sitting
    by_code = {s["code"]: s for s in sch}
    blocks = []
    for reg in ("Northern", "Central", "Southern"):
        h = a["hosts"][reg]
        rows = []
        for x in sorted([x for x in a["roster"] if x["host"] == h], key=lambda x: (x["day"], x["surname"], x["first"])):
            rows.append([x["day"].strftime("%a %d %b").replace(" 0", " "), x["script"] or "", x["entry"],
                         "%s, %s" % (x["surname"], x["first"]), sch[x["home"]]["code"], "Yes" if x["attended"] else "No"])
        blocks.append((sch[h]["name"], sch[h]["code"], rows))
    D.roster(t("makeup_roster_aug2026.pdf"), blocks)
    _csv(t("makeup_scripts_keyed.csv"), ["batch", "script_no", "school_code", "entry_no", "mark", "keyed_on",
                                         "keyed_by"],
         [(x["batch"], x["script"], x["school"], x["entry"], x["keyed_mark"], x["keyed"].isoformat(), x["by"])
          for x in a["scripts"]])

    # ---- distractors: the attitude survey and the bell times
    srows = []
    for s in w["sessions"]:
        if s["status"] != "submitted" or g.random() > 0.7:
            continue
        done = s["end"] + dt.timedelta(minutes=int(g.integers(2, 11)))
        srows.append([s["entry"], s["school"], _utc(done)] + [int(g.integers(1, 6)) for _ in range(8)])
    _csv(t("candidate_survey_2026.csv"), ["entry_no", "school_code", "completed_utc"] +
         ["q%d" % k for k in range(1, 9)], srows)
    bells = []
    for s in sorted(sch, key=lambda s: s["code"]):
        per = []
        for k, (hh, mm) in enumerate(P.PERIODS):
            st = dt.datetime(2026, 8, 3, hh, mm)
            ln = int(g.choice([55, 60, 50]))
            per.append({"period": k + 1, "start": st.strftime("%H:%M"),
                        "end": (st + dt.timedelta(minutes=ln)).strftime("%H:%M")})
        bells.append({"school_code": s["code"], "term": "2026 T3", "periods": per})
    with open(t("member_bell_times_2026.json"), "w") as fh:
        json.dump({"exported": "2026-08-31T02:10:00Z", "schools": bells}, fh, indent=1)
        fh.write("\n")
    assert sorted(os.listdir(target)) == sorted(FILES), set(os.listdir(target)) ^ set(FILES)
    return res
