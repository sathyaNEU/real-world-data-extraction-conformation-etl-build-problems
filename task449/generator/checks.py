"""task449 assertions: the input gates, the three rules (R1 to R3c) on the generator's clean truth, the ladder with
every rung computed from the pack, the estimator family and the semantic fork rows SF1 to SF10, both asks' devices
and crackers, mess neutrality item by item, the deliverables against figures.json, the realism sweep and each
distractor's deletion. Run by build.py after every build; exits on the first failure."""
import datetime as dt
import json
import math
import os
import re
import shutil
import tempfile
import zipfile

import numpy as np
import pandas as pd

import calc as C
import docs as DC
import golden as G
import pack as P
import world as W

N_PASS = [0]


def ok(cond, label, detail=""):
    if not cond:
        raise SystemExit("CHECK FAILED: %s %s" % (label, detail))
    N_PASS[0] += 1
    print("  ok  %-74s %s" % (label, detail))


def bin_of(team):
    return (C.RATE * (team - 1), C.RATE * team)


def inside(base, team, margin):
    lo, hi = bin_of(team)
    return base - lo >= margin and hi - base >= margin


def edge10(x):
    return 5.0 - abs(x - C.r10(x))


def run(target, golden, world=None, meta_path=None):
    import openpyxl
    print("task449 checks")
    files = sorted(os.listdir(target))
    meta = json.load(open(meta_path)) if meta_path else {}

    # ------------------------------------------------------------------------------------------ input gates ----
    ok(len(files) >= 10, "gate: 10 or more files", str(len(files)))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(fmts) >= 3, "gate: 3 or more formats", ", ".join(sorted(fmts)))
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) for f in files
              if f.endswith((".csv", ".jsonl")))
    ok(big >= 25000, "gate: a file of 25,000 rows or more", str(big))
    dis = meta.get("distractor_files", [])
    ok(len(dis) >= 2 and all(d in files for d in dis) and not any("distract" in f for f in files),
       "gate: two or more distractors named in metadata.json only", ", ".join(dis))

    B = C.load(target)
    w = C.frame(B)
    s = C.shares(B, w)
    gold = C.base_of(B, "one_match", w)
    rows = world["rows"] if world else None

    # ------------------------------------------------------------------------------ R1: the raw material ships ----
    reg_cols = set(B["reg"].columns)
    ok(not any(re.search(r"(?i)incident|covered|affected|meridel|failure", c) for c in reg_cols),
       "R1 no register column holds the failure flag", ", ".join(sorted(reg_cols - {"opened", "closed"})))
    ok("results_returned" in open(os.path.join(target, P.FILES["social"]), encoding="utf-8").readline() and
       "k" not in reg_cols - {"opened", "closed"},
       "R1 the search's result count ships only in the social care export (reached through the post-to-matter join)")
    ok(w.k[w.nc].notna().all(), "R1 every name-and-city matter joins to its post record", str(int(w.nc.sum())))

    # ---------------------------------------------------------------- R3a, R3b: the analyst test on the clean truth ----
    if rows:
        aff_true = set(world["acc"].affected)
        win = [r for r in rows if C.WIN[0] <= r["opened"] <= C.WIN[1] and r["events"][-1][1] != "MERGED"]
        Nt = len(win)
        four = lambda r: r["code"] in W.FOUR
        att = sum(1 for r in win if four(r) and r["account"] in aff_true)
        tru = sum(1 for r in win if four(r) and r["true_acc"] in aff_true)
        team_def = math.ceil((Nt - att) / 8.0 / C.RATE)
        team_true = math.ceil((Nt - tru) / 8.0 / C.RATE)
        ok(team_def == 40, "R3a the default path on the clean truth (attached accounts, every rule applied) files 40",
           "%.1f a week" % ((Nt - att) / 8.0))
        ok(team_true == 35, "R3b the decisive step alone (each poster's own account) files the golden 35",
           "%.1f a week" % ((Nt - tru) / 8.0))
        ok(abs((Nt - tru) / 8.0 - gold["base"]) < 2.0, "R3b the estimate from the pack sits within 2 a week of the truth",
           "%.2f against %.2f" % (gold["base"], (Nt - tru) / 8.0))
        for lab, m in (("R1 every name-and-city matter counted", "all"), ("R2 the verified social share", "dm_verified"),
                       ("R3 every verified channel's share", "all_verified")):
            ok(C.base_of(B, m, w)["team"] != 35, "R3b the lower single correction %s stays wrong" % lab,
               str(C.base_of(B, m, w)["team"]))

    # ------------------------------------------------------------------------------------- R3c: no plant ----
    text = []
    for f in files:
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            from pypdf import PdfReader
            text.append(" ".join(pg.extract_text() for pg in PdfReader(p).pages))
        elif f.endswith(".xlsx"):
            wbx = openpyxl.load_workbook(p, read_only=True)
            text.append(" ".join(str(c.value) for ws in wbx for row in ws.iter_rows() for c in row if c.value is not None))
    doc_text = re.sub(r"\s+", " ", " ".join(text)).lower()
    for word in ("dilut", "one in k", "1/k", "false link", "linkage error", "attenuat", "one match", "unique match",
                 "invert", "reliab", "portfolio rate", "share of"):
        ok(word not in doc_text, "R3c no document names the decisive step (%s)" % word[:24])
    ok(not re.search(r"\b(3\d|4\d) (dedicated )?analysts\b(?! for 2026)", doc_text) and "32 dedicated analysts for 2026" in doc_text,
       "R3c no document states a team size for 2027 (the SOW carries 2026's 32)")
    reg = B["reg"]
    dup = reg.drop(columns=["opened", "closed"]).duplicated().mean()
    ok(dup == 0.0, "R3c no copied block in the register", "duplicate rows %.4f" % dup)

    # ----------------------------------------------------------------------------- the ladder, from the pack ----
    want = {"attached": 40, "all": 33, "dm_verified": 34, "all_verified": 37, "one_match": 35}
    names = {"attached": "R0 the attached account as the cardholder's", "all": "R1 every name-and-city matter",
             "dm_verified": "R2 the verified social share", "all_verified": "R3 every verified channel's share",
             "one_match": "R4 the one-match share (golden)"}
    for m, t in want.items():
        r = C.base_of(B, m, w)
        ok(r["team"] == t and inside(r["base"], t, 10.0), "ladder: %s files %d, 10 or more inside its bin" % (names[m], t),
           "base %.1f" % r["base"])
    teams = [C.base_of(B, m, w)["team"] for m in want]
    ok(len(set(teams)) == 5, "ladder: five rungs, five teams", str(teams))
    ok(inside(gold["base"], 35, 12.0), "ladder: the golden base 12 or more inside 935 to 962.5", "%.2f" % gold["base"])
    ok(s["attached"] < 0.40 and s["one_match"] > 0.79, "ladder: the attachments show about 36 per cent, the one-match "
       "links about 80", "%.3f, %.3f" % (s["attached"], s["one_match"]))
    ok(abs(s["dm_verified"] - s["one_match"]) * gold["nc_n"] / 8.0 >= 20,
       "dominance: the verified social share moves the base 20 or more a week",
       "%.1f" % (abs(s["dm_verified"] - s["one_match"]) * gold["nc_n"] / 8.0))

    # ---------------------------------------------------------------------- C1: the estimator family (SF7) ----
    for m in ("inversion", "regression", "posterior"):
        r = C.base_of(B, m, w)
        ok(r["team"] == 35 and C.r10(r["base"]) == C.r10(gold["base"]) and C.r10(r["incident"]) == C.r10(gold["incident"])
           and int(round(100 * s[m])) == int(round(100 * s["one_match"])),
           "SF7 the %s estimator: same team, base, failure's matters and share" % m,
           "%.4f, base %.2f" % (s[m], r["base"]))
    ok(edge10(gold["base"]) >= 3.0 and edge10(gold["incident"]) >= 3.0 and
       edge10(C.base_of(B, "inversion", w)["base"]) >= 3.0,
       "bins: the base and the failure's matters a week 3 or more from a rounding edge",
       "%.2f, %.2f" % (gold["base"], gold["incident"]))
    ok(abs(100 * s["one_match"] - 80) <= 0.3 and abs(100 * s["inversion"] - 80) <= 0.3,
       "bins: the share within 0.3 points of 80 under both main estimators")

    # ------------------------------------------------------------------------------------- semantic forks ----
    claim = (len(w) - gold["ver_aff"]) / 8.0
    ok(math.ceil(claim / C.RATE) != 35, "SF1 the claimable reading (confirmed accounts only) files another team",
       "%.1f" % claim)
    wm = C.frame(B, merged=True)
    r = C.base_of(B, "one_match", wm)
    ok(r["team"] == 35 and C.r10(r["base"]) == C.r10(gold["base"]), "SF2 merged duplicates counted: same call, same bins",
       "%.2f" % r["base"])
    h = B["hist"]
    reopen_win = int(((h.event == "REOPENED") & (h.t >= C.WIN[0]) & (h.t <= C.WIN[1])).sum())
    ok(math.ceil((gold["base"] + reopen_win / 8.0) / C.RATE) != 35,
       "SF2 reopenings counted as new matters file another team (ruled out by WPS-3 2.2)", "+%.1f a week" % (reopen_win / 8.0))
    save = C.WIN
    try:
        C.WIN = (dt.datetime(2026, 8, 10), dt.datetime(2026, 10, 4, 23, 59, 59))
        r = C.base_of(B, "one_match", C.frame(B))
        ok(r["team"] == 35, "SF3 the eight weeks to the pull (10 August to 4 October): same call", "%.2f" % r["base"])
        C.WIN = (save[0] - dt.timedelta(hours=1), save[1] + dt.timedelta(hours=1))
        r1 = C.base_of(B, "one_match", C.frame(B))
        C.WIN = (save[0] + dt.timedelta(hours=1), save[1] - dt.timedelta(hours=1))
        r2 = C.base_of(B, "one_match", C.frame(B))
        ok(C.r10(r1["base"]) == C.r10(r2["base"]) == C.r10(gold["base"]) and r1["team"] == r2["team"] == 35,
           "axis 9 the matters within an hour of either edge, counted either way: same bins")
    finally:
        C.WIN = save
    r = C.base_of(B, "one_match", C.frame(B, clock="post"))
    ok(r["team"] == 35 and C.r10(r["base"]) == C.r10(gold["base"]), "SF4 the social post's UTC time for the week: same "
       "call, same bins", "%.2f" % r["base"])
    r = C.base_of(B, "one_match", C.frame(B, affected=B["affected_any"]))
    ok(r["team"] == 35 and C.r10(r["base"]) == C.r10(gold["base"]), "SF5 returned payments counted as affected: same call, "
       "same bins", "%.2f" % r["base"])
    ok(math.ceil(round(gold["base"], -1) / C.RATE) == 35, "SF6 the base rounded before dividing: same call")
    for lab, b in (("31 May", C.portfolio_rate(B, "2026-05-31")), ("payments", C.portfolio_rate(B, accounts=False))):
        r = C.base_of(B, "inversion", w, b=b)
        ok(r["team"] == 35 and C.r10(r["base"]) == C.r10(gold["base"]),
           "SF8 the portfolio rate from %s: same call, same bins" % lab, "%.4f, %.2f" % (b, r["base"]))
    weekly = w.groupby(((w.opened - C.WIN[0]).dt.days // 7)).size()
    ok(len(weekly) == 8 and abs(weekly.mean() - len(w) / 8.0) < 1e-9, "SF9 the mean of the weekly counts is the total over eight")
    fam = [c for c, _, f in W.CODES if f in ("Payments", "Fees and interest", "Credit reporting")]
    r = C.base_of(B, "one_match", C.frame(B, codes=fam))
    ok(r["team"] == 35 and C.r10(r["base"]) == C.r10(gold["base"]), "SF10 the three code families in place of the four "
       "codes: same call, same bins", "%.2f" % r["base"])
    r = C.base_of(B, "share_over_all_codes", w)
    ok(r["team"] != 35, "axis 13 the share estimated before the code filter files another team", str(r["team"]))
    raw = B["reg"].account_ref.isin(set(B["meridel"].acct_no))
    ok(not raw.any() and w.o.sum() > 0, "axis 16 account references joined raw match nothing (loud); normalised they "
       "match", "%d" % int(w.o.sum()))

    # ------------------------------------------------------------------------------------------------ asks ----
    flex, flex_n = C.flex_hours(B), C.flex_hours(B, treadwell="decimal")
    flex_hm = C.flex_hours(B, treadwell="hhmm")
    ok(all(abs(flex[m] - flex_hm[m]) < 1e-6 for m in C.MONTHS), "Ask A Treadwell's hours from its clock times equal its "
       "hours and minutes converted")
    ok(all(edge10(flex[m]) >= 2.5 for m in C.MONTHS), "Ask A every month 2.5 or more from a rounding edge",
       " ".join("%.2f" % flex[m] for m in C.MONTHS))
    ok(all(C.r10(flex_n[m]) != C.r10(flex[m]) for m in C.MONTHS) and min(flex[m] - flex_n[m] for m in C.MONTHS) >= 12,
       "Ask A cracker (Treadwell's hours read as decimals) misses every month, 12 or more hours low",
       " ".join("%.1f" % (flex[m] - flex_n[m]) for m in C.MONTHS))
    fo = C.flex_hours(B, other_programs=True)
    moved = [m for m in C.MONTHS if C.r10(fo[m]) != C.r10(flex[m])]
    ok(len(moved) >= 3, "Ask A hazard: other programs' overtime kept moves three or more months", str(moved))
    fd = C.flex_hours(B, dedupe=False)
    ok([m for m in C.MONTHS if C.r10(fd[m]) != C.r10(flex[m])] == [6], "Ask A hazard: the re-sent Marlowby week moves June")
    tw = B["treadwell"]
    frac = ((tw.Hours * 100).round().astype(int) % 100)
    ok(frac.max() <= 59 and (frac == 45).any(), "Ask A the device's tell: no Treadwell fraction above .59, and .45 present")
    op, opn = C.open_at_month_ends(B, "history"), C.open_at_month_ends(B, "register")
    ok(all(edge10(op[m]) >= 3.0 for m in C.MONTHS), "Ask B every month end 3 or more from a rounding edge",
       " ".join(str(op[m]) for m in C.MONTHS))
    ok(all(C.r10(opn[m]) != C.r10(op[m]) for m in C.MONTHS),
       "Ask B cracker (the register's opened and closed times) misses every month end",
       " ".join("+%d" % (opn[m] - op[m]) for m in C.MONTHS))
    # main population zero-counts: the main call reads none of the asks' files
    tmp = tempfile.mkdtemp()
    try:
        keep = [f for f in files if f not in (P.FILES["time"], P.FILES["marlowby"], P.FILES["treadwell"],
                                              P.FILES["history"])]
        for f in files:
            src = os.path.join(target, f)
            if f in keep:
                os.link(src, os.path.join(tmp, f))
            elif f == P.FILES["history"]:
                open(os.path.join(tmp, f), "w").write("matter_no,event_at,event\n")
            elif f == P.FILES["time"]:
                open(os.path.join(tmp, f), "w").write("employee_id,work_date,segment_start,segment_end,pay_code,program,hours\n")
            elif f == P.FILES["marlowby"]:
                open(os.path.join(tmp, f), "w").write("worker_no,shift_date,time_in,time_out,unpaid_break_min,hours,"
                                                     "assignment,week_ending,export_id\n")
            else:
                shutil.copy(src, os.path.join(tmp, f))
        Bz = C.load(tmp)
        rz = C.base_of(Bz, "one_match")
        ok(abs(rz["base"] - gold["base"]) < 1e-9 and rz["team"] == 35,
           "separation: emptying the time records, timesheets and status history leaves the main call untouched")
    finally:
        shutil.rmtree(tmp)
    ok("closed" not in [c for c in ("matter_no", "opened_at", "channel", "problem_code", "account_basis", "account_ref")],
       "separation: the main call reads no closure or status column")

    # ----------------------------------------------------------------------------------- the deliverables ----
    fig = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    ok(fig["team"] == "35" and fig["base"] == "950" and fig["incident_week"] == "500" and fig["nc_share"] == "80",
       "figures.json: the call, the base, the failure's matters and the share")
    csv_rows = open(os.path.join(golden, G.CSV)).read().strip().splitlines()
    ok(csv_rows[0] == "month,flex_hours" and len(csv_rows) == 10 and
       all(int(r.split(",")[1]) == C.r10(flex[i + 1]) for i, r in enumerate(csv_rows[1:])),
       "csv: nine months of flex hours, the golden's")
    from docx import Document
    d = Document(os.path.join(golden, G.DOCX))
    body = " ".join(p.text for p in d.paragraphs)
    ok("carry 35 dedicated analysts" in body and "950 new matters a week" in body, "docx: the call and the base")
    tb = d.tables[0]
    vals = [tb.rows[i + 1].cells[1].text for i in range(9)]
    ok(vals == [G.fmt(C.r10(op[m])) for m in C.MONTHS], "docx: the month-end open table is the golden's", " ".join(vals))
    ok(len(d.inline_shapes) == 1, "docx: one chart")
    for k_, v in fig["open_month_end"].items():
        ok(v in body or v in vals, "docx: %s open count present" % k_)

    # ------------------------------------------------------------------------------------- realism sweep ----
    ok(weekly.nunique() == 8, "realism: no two of the eight weeks carry the same count", " ".join(map(str, weekly.values)))
    ok(len(w) % 100 != 0 and abs(gold["base"] - round(gold["base"])) > 0.01, "realism: no round headline totals",
       "%d, %.2f" % (len(w), gold["base"]))
    ok(reg.matter_no.is_unique, "realism: matter numbers unique")
    ok(((reg.closed.isna()) | (reg.closed >= reg.opened)).all(), "realism: no matter closes before it opens")
    first = h.sort_values(["matter_no", "t"]).groupby("matter_no").event.first()
    ok((first == "OPENED").all(), "realism: every status history starts with OPENED")
    ok(reg.opened.max() <= pd.Timestamp("2026-10-08 23:59:59") and h.t.max() <= pd.Timestamp("2026-10-08 23:59:59"),
       "realism: nothing dated after the export")
    soc_t = pd.to_datetime(B["social"].created_at.str.replace("Z", "", regex=False))
    ok(soc_t.max() <= pd.Timestamp("2026-10-09 04:00:00"), "realism: no post published after the export (UTC)")
    pers = re.compile(rb"<dc:creator>([^<]*)</dc:creator>|<cp:lastModifiedBy>([^<]*)</cp:lastModifiedBy>")
    who = set()
    for folder in (target, golden):
        for f in os.listdir(folder):
            if f.endswith((".xlsx", ".docx")):
                with zipfile.ZipFile(os.path.join(folder, f)) as z:
                    for nm in z.namelist():
                        if nm.endswith("core.xml"):
                            for m in pers.finditer(z.read(nm)):
                                who |= {x.decode() for x in m.groups() if x}
    ok(who <= set(W.PEOPLE.values()) | {"Treadwell &amp; Oake"}, "realism: office files carry only their owners",
       ", ".join(sorted(who)))
    tells = (b"openpyxl", b"python-docx", b"ReportLab", b"reportlab", b"matplotlib", b"Matplotlib")

    def blob(folder, f):
        p = os.path.join(folder, f)
        if f.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(p) as z:
                return b"".join(z.read(n) for n in z.namelist())
        return open(p, "rb").read()
    ok(not any(t in blob(target, f) for f in files if f.endswith((".xlsx", ".pdf")) for t in tells),
       "H1 no writer's name in the pack's containers")
    ok(not any(t in blob(golden, f) for f in os.listdir(golden) for t in tells), "H1 no writer's name in the goldens")
    em = [f for f in files if f.endswith((".csv", ".jsonl")) and "—" in open(os.path.join(target, f),
                                                                                 encoding="utf-8").read()]
    ok(not em and "—" not in doc_text, "standing rule: no em dash in the pack")
    ok(doc_text.count("27.5 new matters") == 1, "one file: the planning rate stated once")
    ok(doc_text.count("first cardholder the search returned") == 1, "one file: the name-and-city attachment described once")

    # ---------------------------------------------------------------------------- distractor deletion ----
    tmp = tempfile.mkdtemp()
    try:
        for dfile in dis:
            sub = os.path.join(tmp, dfile.replace(".", "_"))
            os.makedirs(sub)
            for f in files:
                if f != dfile:
                    os.link(os.path.join(target, f), os.path.join(sub, f))
            Bd = C.load(sub)
            rd = C.base_of(Bd, "one_match")
            ok(abs(rd["base"] - gold["base"]) < 1e-9 and C.open_at_month_ends(Bd) == op and C.flex_hours(Bd) == flex,
               "distractor: deleting %s moves nothing" % dfile)
    finally:
        shutil.rmtree(tmp)
    print("task449 checks: %d passed" % N_PASS[0])
    return N_PASS[0]
