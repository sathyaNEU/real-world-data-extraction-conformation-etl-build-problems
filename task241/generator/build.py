"""Write the task241 pack into a target folder from the simulated world, and return the world for the checks."""
import os

import numpy as np
import pandas as pd

import params as P
import postprocess
import sim

FILES = {
    "inbound": "inbound_switch_2026.csv",
    "samples": "case_records_2026.csv",
    "zones": "state_time_zones.csv",
    "register": "project_register_2027.xlsx",
    "policy": "dialer_policy_2027.docx",
    "spec": "larkspur_amd_release6.pdf",
    "listening": "amd_listening_audit_2025.xlsx",
    "invoices": "client_invoices_2026.xlsx",
    "hours_h1": "interviewer_hours_2026_h1.csv",
    "hours_h2": "interviewer_hours_2026_h2.csv",
    "consent": "mobile_consent_log_2026.csv",
    "qa": "qa_monitoring_scores_2026.csv",
}
EXPORT_DIR = "dialer_exports"
DISTRACTORS = ["consent", "qa", "invoices"]
VENDOR = "Larkspur Telephony"
OLD = dict(COMPLETE="C", PARTIAL="P", REFUSAL="R", CALLBACK="B", INELIGIBLE="I", LANGUAGE="L", HANGUP="H", DNC="D",
           AMD_MACHINE="A", ABANDONED="X", AGENT_MACHINE="AA")


def export_name(m):
    return os.path.join(EXPORT_DIR, f"kr_dialer_{P.YEAR}-{m:02d}.csv")


def _fmt_old(t):
    return t.dt.strftime("%m/%d/%Y %H:%M:%S").where(t.notna(), "")


def _fmt_new(t):
    return t.dt.strftime("%Y-%m-%d %H:%M:%S").where(t.notna(), "")


def dialer_rows(W):
    c = W["calls"].copy()
    c["reopen"] = False
    r = W["reopen"].copy()
    rng = np.random.default_rng(P.SEED + 7)
    r["call_id"] = c["call_id"].max() + 1000 + np.arange(len(r)) * 3 + rng.integers(0, 3, len(r))
    hh = rng.integers(9 * 3600, 16 * 3600, len(r))
    r["placed"] = r["placed"].dt.normalize() + pd.to_timedelta(hh, unit="s")
    r.loc[sim.on_the_hour(r["placed"].values, r["state"].values), "placed"] += pd.Timedelta(seconds=7)
    r["answered"] = r["placed"] + pd.Timedelta(seconds=1)
    r["connected"] = r["answered"]
    r["ended"] = r["answered"] + pd.to_timedelta(r["talk"], unit="s")
    r = r[r["placed"].dt.normalize().isin(sim.OPEN)]
    allc = pd.concat([c, r], ignore_index=True).sort_values(["placed", "call_id"]).reset_index(drop=True)
    allc["case"] = np.where(allc["placed"] < pd.Timestamp(P.UPGRADE), allc["case_old"], allc["case_new"])
    return allc


def write_exports(target, rows):
    os.makedirs(os.path.join(target, EXPORT_DIR), exist_ok=True)
    rows = rows.copy()
    rows["day"] = rows["placed"].dt.normalize()
    rows["m"] = rows["placed"].dt.month
    for m in range(1, 13):
        cur = rows[rows["m"] == m]
        if m > 1:
            prev_last = rows[rows["m"] == m - 1]["day"].max()
            cur = pd.concat([rows[rows["day"] == prev_last], cur])
        new = m >= int(P.UPGRADE[5:7])
        if not new:
            out = pd.DataFrame({
                "CallID": cur["call_id"], "JobNo": cur["job"], "Phone": cur["phone"], "CaseID": cur["case"],
                "CallStart": _fmt_old(cur["placed"]), "AnswerTime": _fmt_old(cur["answered"]),
                "AMD": np.where(cur["outcome"].eq("AMD_MACHINE"), "M", "H"),
                "AgentConnect": _fmt_old(cur["connected"]), "AgentID": cur["agent"].fillna(""),
                "Disp": cur["outcome"].map(OLD), "TalkSec": cur["talk"], "WrapSec": cur["wrap"],
                "CallEnd": _fmt_old(cur["ended"])})
        else:
            ph = cur["phone"]
            out = pd.DataFrame({
                "call_id": cur["call_id"], "job": cur["job"],
                "dialed_number": "(" + ph.str[:3] + ") " + ph.str[3:6] + "-" + ph.str[6:],
                "case_number": cur["case"], "placed_at": _fmt_new(cur["placed"]),
                "answered_at": _fmt_new(cur["answered"]),
                "amd_result": np.where(cur["outcome"].eq("AMD_MACHINE"), "MACHINE", "LIVE"),
                "agent_connected_at": _fmt_new(cur["connected"]), "agent": cur["agent"].fillna(""),
                "outcome": cur["outcome"], "talk_seconds": cur["talk"], "wrap_seconds": cur["wrap"],
                "ended_at": _fmt_new(cur["ended"])})
        out.to_csv(os.path.join(target, export_name(m)), index=False, lineterminator="\n" if new else "\r\n")


INB_AGENTS = [f"I{x:02d}" for x in range(1, 10)]
RETURN_WRAP = (["QUESTION", "CALLBACK-SET", "REFUSED", "OPT-OUT", "MESSAGE"], [0.38, 0.30, 0.14, 0.08, 0.10])


def inbound_rows(W):
    rng = np.random.default_rng(P.SEED + 11)
    inb = W["inbound"].copy().sort_values(["started", "caller", "kind"]).reset_index(drop=True)
    n = len(inb)
    wrap = np.empty(n, dtype=object)
    k = inb["kind"].values
    ret = np.isin(k, ["prompt", "late", "screen", "voicemail"])
    wrap[ret] = rng.choice(RETURN_WRAP[0], size=ret.sum(), p=RETURN_WRAP[1])
    for kind, code in [("complete", "COMPLETE"), ("question", "QUESTION"), ("optout", "OPT-OUT"),
                       ("callback_set", "CALLBACK-SET"), ("test", "TEST")]:
        wrap[k == kind] = code
    talk = np.where(wrap == "COMPLETE", rng.integers(800, 1600, n), rng.integers(35, 260, n))
    talk = np.where(wrap == "TEST", rng.integers(10, 40, n), talk)
    inb["switch_call_id"] = 880000 + np.arange(n) * 2 + rng.integers(0, 2, n)
    inb["leg"] = 1
    inb["queue"] = np.where(wrap == "TEST", "QA", "Main")
    inb["agent"] = np.where(wrap == "TEST", "QA1", rng.choice(INB_AGENTS, n))
    inb["wrap_code"] = wrap
    inb["talk_seconds"] = talk
    # a transferred call: the desk answers on leg 1 and hands it on; the leg that ends the call carries its outcome
    p_tr = np.where(k == "complete", P.INBOUND_TRANSFER_COMPLETE, 0.08)
    t2 = (rng.random(n) < p_tr) & (wrap != "TEST")
    l2 = inb[t2].copy()
    l2["leg"] = 2
    desk_talk = rng.integers(25, 90, len(l2))
    l2["started"] = l2["started"] + pd.to_timedelta(desk_talk + rng.integers(5, 40, len(l2)), unit="s")
    interview = l2["kind"].eq("complete").values
    l2["queue"] = np.where(interview, "Interviewing", "Supervisor")
    l2["agent"] = np.where(interview, rng.choice(["I10", "I11", "I12", "I13", "I14"], len(l2)),
                           rng.choice(["S01", "S02"], len(l2)))
    l2["talk_seconds"] = np.where(interview, l2["talk_seconds"].values, rng.integers(40, 400, len(l2)))
    inb.loc[t2, "wrap_code"] = "TRANSFER"
    inb.loc[t2, "talk_seconds"] = desk_talk
    t3 = l2[(rng.random(len(l2)) < 0.12) & ~interview].copy()
    l2.loc[t3.index, "wrap_code"] = "TRANSFER"
    t3["leg"] = 3
    t3["started"] = t3["started"] + pd.to_timedelta(t3["talk_seconds"] + 9, unit="s")
    t3["queue"] = "Main"
    t3["agent"] = rng.choice(INB_AGENTS, len(t3))
    t3["talk_seconds"] = rng.integers(20, 120, len(t3))
    legs = [inb, l2, t3]
    out = pd.concat(legs, ignore_index=True).sort_values(["started", "switch_call_id", "leg"]).reset_index(drop=True)
    out["caller_fmt"] = np.where(out["kind"].eq("test"), "6517", "+1" + out["caller"].astype(str))
    out["dialed_line"] = out["job"].map(sim.LINES)
    out["line_name"] = out["job"].map(sim.LINE_NAMES)
    return out


def write_inbound(target, inb):
    out = pd.DataFrame({"switch_call_id": inb["switch_call_id"], "leg": inb["leg"],
                        "started": inb["started"].dt.strftime("%Y-%m-%d %H:%M:%S"),
                        "caller": inb["caller_fmt"], "dialed_line": inb["dialed_line"], "line_name": inb["line_name"],
                        "queue": inb["queue"], "agent": inb["agent"], "wrap_code": inb["wrap_code"],
                        "talk_seconds": inb["talk_seconds"]})
    out.to_csv(os.path.join(target, FILES["inbound"]), index=False, lineterminator="\n")


def write_samples(target, W):
    fr = W["frame"].sort_values(["job", "released", "case_new"]).reset_index(drop=True)
    ph = fr["phone"]
    out = pd.DataFrame({"job": fr["job"], "case_number": fr["case_new"],
                        "phone": ph.str[:3] + "-" + ph.str[3:6] + "-" + ph.str[6:], "address_state": fr["state"],
                        "released": fr["released"].dt.strftime("%Y-%m-%d")})
    out.to_csv(os.path.join(target, FILES["samples"]), index=False, lineterminator="\n")


def write_zones(target):
    rows = []
    std = {"America/New_York": -5, "America/Chicago": -6, "America/Denver": -7, "America/Phoenix": -7,
           "America/Los_Angeles": -8}
    name = {"America/New_York": "Eastern", "America/Chicago": "Central", "America/Denver": "Mountain",
            "America/Phoenix": "Mountain (Arizona)", "America/Los_Angeles": "Pacific"}
    for st, tz in sorted(P.STATE_TZ.items()):
        rows.append(dict(state=st, time_zone=name[tz], utc_offset_standard=std[tz],
                         observes_daylight_time="no" if tz == "America/Phoenix" else "yes"))
    pd.DataFrame(rows).to_csv(os.path.join(target, FILES["zones"]), index=False, lineterminator="\n")


def _xlsx_finish(path, author, created, modified):
    postprocess.scrub(path, author, created[:10])
    postprocess.finish_office(path, created, modified, P.COMPANY)


def write_register(target):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill
    wb = Workbook()
    ws = wb.active
    ws.title = "2027 projects"
    ws.append(["Kettle River Research, telephone centre: 2027 project setup register"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([])
    head = ["Job", "Project", "Client", "Sample frame", "Caller-ID line", "Detection 2026", "Detection 2027",
            "Calling days 2027"]
    ws.append(head)
    for c in ws[3]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE6F0")
    frames = {"KR-2611": "landline RDD", "KR-2614": "landline RDD", "KR-2617": "landline RDD",
              "KR-2615": "client list (households)", "KR-2613": "business list", "KR-2621": "business list",
              "KR-2623": "provider list"}
    for job, name, client, *_ in P.PROJECTS:
        ws.append([job, name, client, frames.get(job, "client list (landline numbers)"), sim.LINES[job][2:],
                   "On (balanced)", None, "Mon to Sat"])
    for col, w in zip("ABCDEFGH", [10, 42, 40, 30, 15, 15, 15, 17]):
        ws.column_dimensions[col].width = w
    p = os.path.join(target, FILES["register"])
    wb.save(p)
    _xlsx_finish(p, P.DIRECTOR, "2026-11-18T15:02:00Z", "2026-12-04T10:41:00Z")


def write_policy(target):
    import docx
    from docx.shared import Pt
    doc = docx.Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)
    h = doc.add_paragraph()
    r = h.add_run("Telephone centre dialer policy, 2027 project year")
    r.bold = True
    r.font.size = Pt(14)
    doc.add_paragraph("Kettle River Research, telephone operations. Owner: Hailey Mullins, director of telephone "
                      "operations. Issued 20 November 2026; replaces the 2026 policy.")
    paras = [
        ("1. Scope.", "This policy sets the predictive dialer for every recurring project in the 2027 project year. "
         "Settings are entered for each project at project setup in January and hold for the year unless this policy "
         "is reissued."),
        ("2. Calling hours.", "Calls ring only between 8 am and 9 pm in the called household's own local time, Monday "
         "to Saturday, and never on the centre's holidays. A call that rings outside those hours is an exception and "
         "is reported to the director."),
        ("3. Answering machine detection.", "The dialer listens to the start of every answered call. A call it "
         "classes as an answering machine hears the project's recorded message and is closed without reaching an "
         "interviewer. A live answer for which no interviewer is free within two seconds is abandoned and hears the "
         "same recorded message. Detection stays on for a project in 2027 only while fewer than one in ten of the "
         "calls the dialer classed as answering machines on that project in 2026 had in fact been answered by a "
         "person; on any other project it is switched off and interviewers handle every answered call."),
        ("4. Do-not-call requests.", "A request not to be called, made to an interviewer or to the inbound desk, is "
         "honoured from the moment it is made, for every project."),
        ("5. Interviews and hours.", "An interview counts once, when it is completed. Interviewer hours are charged "
         "to the projects the interviewer worked in each shift, in proportion to each project's talk and wrap time "
         "in that shift; a shift with no calls is not charged to a project."),
    ]
    for lead, text in paras:
        p = doc.add_paragraph()
        p.add_run(lead + " ").bold = True
        p.add_run(text)
        p.paragraph_format.space_after = Pt(6)
    doc.core_properties.author = P.DIRECTOR
    doc.core_properties.title = "Telephone centre dialer policy, 2027 project year"
    path = os.path.join(target, FILES["policy"])
    doc.save(path)
    postprocess.scrub(path, P.DIRECTOR, "2026-11-20")
    postprocess.finish_office(path, "2026-11-12T14:20:00Z", "2026-11-20T09:05:00Z", P.COMPANY)


def write_spec(target):
    from reportlab import rl_config
    rl_config.invariant = 1                  # no build clock or random document id in the file
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    path = os.path.join(target, FILES["spec"])
    ss = getSampleStyleSheet()
    doc = SimpleDocTemplate(path, pagesize=letter, title="AMD release 6 test results", author=VENDOR, creator=VENDOR,
                            subject="Answering machine detection, release 6")
    rows = [["Setting", "Live answers classed as machine", "Machines classed as live", "Median decision time"],
            ["Conservative", "0.8%", "14.2%", "2.6 s"], ["Balanced (default)", "2.1%", "6.5%", "2.3 s"],
            ["Aggressive", "4.7%", "2.9%", "1.9 s"]]
    t = Table(rows, colWidths=[110, 150, 130, 110])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF4")),
                           ("FONTSIZE", (0, 0), (-1, -1), 9)]))
    story = [Paragraph("Larkspur Telephony", ss["Title"]),
             Paragraph("Answering machine detection, release 6: test results", ss["Heading2"]),
             Paragraph("Detection decides from the first seconds of audio after the line is answered, on the cadence "
                       "of speech and silence, and returns LIVE or MACHINE to the dialer.", ss["Normal"]),
             Spacer(1, 10), t, Spacer(1, 10),
             Paragraph("Measured on the Larkspur reference set: 12,000 recorded answers from residential lines (6,000 "
                       "live answers and 6,000 answering machines and voicemail greetings), collected in 2023.",
                       ss["Normal"]),
             Paragraph("Release 6, published March 2024.", ss["Normal"])]
    doc.build(story)
    postprocess.scrub(path, VENDOR, "2024-03-11")


def write_listening(target):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    rng = np.random.default_rng(P.SEED + 23)
    verdicts = np.array(["Answering machine greeting"] * 301 + ["Carrier voicemail"] * 82 + ["Attendant or IVR"] * 8
                        + ["Person"] * P.LISTEN_PEOPLE)
    rng.shuffle(verdicts)
    wb = Workbook()
    ws = wb.active
    ws.title = "Listening sample"
    ws.append(["Call ID", "Date", "Job", "Detector result", "Heard on the recording"])
    for c in ws[1]:
        c.font = Font(bold=True)
    days = pd.date_range("2025-10-01", "2025-10-31", freq="D")
    ids = np.sort(rng.choice(np.arange(4_700_000, 4_900_000), P.LISTEN_N, replace=False))
    for i, v in zip(ids, verdicts):
        d = days[int(rng.integers(0, len(days)))]
        ws.append([int(i), d.strftime("%Y-%m-%d"), "KR-2511", "MACHINE", v])
    s = wb.create_sheet("Summary")
    s.append(["2025 listening test, Minnesota Adult Health Survey (landline), job KR-2511"])
    s["A1"].font = Font(bold=True)
    s.append(["Recorded calls drawn at random from the job's October 2025 machine-classed calls", P.LISTEN_N])
    s.append(["Answered by a person", P.LISTEN_PEOPLE])
    s.append(["Share answered by a person", P.LISTEN_PEOPLE / P.LISTEN_N])
    s["B4"].number_format = "0.00%"
    s.append(["Listened by", P.QA_LEAD])
    ws.column_dimensions["E"].width = 30
    s.column_dimensions["A"].width = 78
    p = os.path.join(target, FILES["listening"])
    wb.save(p)
    _xlsx_finish(p, P.QA_LEAD, "2025-11-03T13:15:00Z", "2025-11-06T16:30:00Z")


def write_invoices(target, rows):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    comp = rows[rows["outcome"].eq("COMPLETE") & rows["job"].isin([s[0] for s in P.PROJECTS])]
    q = comp.groupby(["job", comp["placed"].dt.quarter]).size().unstack(fill_value=0)
    wb = Workbook()
    ws = wb.active
    ws.title = "2026"
    ws.append(["Completed interviews invoiced, 2026"])
    ws["A1"].font = Font(bold=True)
    ws.append(["Job", "Q1", "Q2", "Q3", "Q4", "Year"])
    for c in ws[2]:
        c.font = Font(bold=True)
    for job, *_ in P.PROJECTS:
        v = [int(q.loc[job].get(k, 0)) if job in q.index else 0 for k in (1, 2, 3, 4)]
        ws.append([job] + v + [sum(v)])
    p = os.path.join(target, FILES["invoices"])
    wb.save(p)
    _xlsx_finish(p, "Accounts", "2026-04-06T11:00:00Z", "2027-01-08T14:22:00Z")


def timesheet_rows(W):
    sh = W["shifts"].copy()
    tr = W["training"].copy()
    rng = np.random.default_rng(P.SEED + 31)
    start = {"day": "09:00", "evening": "16:00", "weekend": "10:00"}
    sh["start"] = sh["period"].map(start)
    sh["project"] = sh["jobs"].map(lambda j: j[0])
    tr["start"] = "13:30"
    tr["project"] = tr["jobs"].map(lambda j: j[0])
    tr["agent"] = rng.choice(sorted(set(sh["agent"])), len(tr))
    out = pd.concat([sh[["date", "agent", "project", "start", "hours"]],
                     tr[["date", "agent", "project", "start", "hours"]]], ignore_index=True)
    out = out.sort_values(["date", "start", "agent", "project"]).reset_index(drop=True)
    return out


def hhmm(h):
    """hours and minutes written the timekeeping system's way, 4 hours 30 minutes as 4.30"""
    whole = (h // 1).astype(int)
    mins = ((h % 1) * 60).round().astype(int)
    return whole.astype(str) + "." + mins.astype(str).str.zfill(2)


def write_timesheets(target, ts):
    """the payroll's timekeeping export, from the old system to June and from the new one after"""
    new = ts["date"] >= pd.Timestamp(P.UPGRADE)
    old = ts[~new]
    out1 = pd.DataFrame({"Work Date": old["date"].dt.strftime("%m/%d/%Y"), "Employee": old["agent"],
                         "Job Code": old["project"].str[3:], "Time In": old["start"],
                         "Hours": old["hours"].map(lambda x: f"{x:.2f}")})
    out1.to_csv(os.path.join(target, FILES["hours_h1"]), index=False, lineterminator="\r\n")
    nw = ts[new]
    out2 = pd.DataFrame({"shift_date": nw["date"].dt.strftime("%Y-%m-%d"), "employee": nw["agent"],
                         "cost_code": nw["project"], "clock_in": nw["start"], "paid_hours": hhmm(nw["hours"])})
    out2.to_csv(os.path.join(target, FILES["hours_h2"]), index=False, lineterminator="\n")


def write_distractors(target, W):
    rng = np.random.default_rng(P.SEED + 41)
    fr = W["frame"]
    pick = fr.sample(n=2600, random_state=int(rng.integers(1e9)))
    cons = pd.DataFrame({"mobile_number": "+1" + pick["phone"].str[:3] + rng.integers(200, 990, 2600).astype(str)
                         + pick["phone"].str[6:], "job": pick["job"].values,
                         "consent_date": (pd.Timestamp("2025-06-01") + pd.to_timedelta(rng.integers(0, 540, 2600), unit="D")).strftime("%Y-%m-%d"),
                         "source": rng.choice(["web form", "prior survey", "client portal"], 2600, p=[0.5, 0.3, 0.2])})
    cons.sort_values(["consent_date", "mobile_number"]).to_csv(os.path.join(target, FILES["consent"]), index=False,
                                                               lineterminator="\n")
    agents = sorted(set(W["shifts"]["agent"]))
    q = [dict(interviewer=a, month=f"{P.YEAR}-{m:02d}", calls_monitored=int(rng.integers(4, 13)),
              score=int(np.clip(rng.normal(86, 6), 55, 100))) for a in agents for m in range(1, 13)]
    pd.DataFrame(q).to_csv(os.path.join(target, FILES["qa"]), index=False, lineterminator="\n")


def run(target, documents=True):
    os.makedirs(target, exist_ok=True)
    W = sim.make()
    rows = dialer_rows(W)
    write_exports(target, rows)
    inb = inbound_rows(W)
    write_inbound(target, inb)
    write_samples(target, W)
    write_zones(target)
    ts = timesheet_rows(W)
    write_timesheets(target, ts)
    write_distractors(target, W)
    if documents:
        write_register(target)
        write_policy(target)
        write_spec(target)
        write_listening(target)
        write_invoices(target, rows)
    W["rows"], W["inb"], W["ts"] = rows, inb, ts
    return W
