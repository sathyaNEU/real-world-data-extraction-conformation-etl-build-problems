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
    pl, an, _ = sim.no_straddle(r["placed"].values, r["answered"].values, r["state"].values)
    r["placed"], r["answered"] = pl, an
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


ZONE_ROWS = [  # state, name, zone of the state (or of most of it), parts of the state on another zone
    ("AL", "Alabama", "Central", ""), ("AK", "Alaska", "Alaska", "Aleutian Islands west of 169 30 W on Hawaii-Aleutian time"),
    ("AZ", "Arizona", "Mountain (Arizona)", ""), ("AR", "Arkansas", "Central", ""), ("CA", "California", "Pacific", ""),
    ("CO", "Colorado", "Mountain", ""), ("CT", "Connecticut", "Eastern", ""), ("DE", "Delaware", "Eastern", ""),
    ("DC", "District of Columbia", "Eastern", ""),
    ("FL", "Florida", "Eastern", "western Panhandle (west of the Apalachicola River) on Central time"),
    ("GA", "Georgia", "Eastern", ""), ("HI", "Hawaii", "Hawaii-Aleutian", ""),
    ("ID", "Idaho", "Mountain", "northern Idaho (the Panhandle) on Pacific time"), ("IL", "Illinois", "Central", ""),
    ("IN", "Indiana", "Eastern", "six northwestern and six southwestern counties on Central time"),
    ("IA", "Iowa", "Central", ""), ("KS", "Kansas", "Central", "four western counties on Mountain time"),
    ("KY", "Kentucky", "Eastern", "western Kentucky on Central time"), ("LA", "Louisiana", "Central", ""),
    ("ME", "Maine", "Eastern", ""), ("MD", "Maryland", "Eastern", ""), ("MA", "Massachusetts", "Eastern", ""),
    ("MI", "Michigan", "Eastern", "four Upper Peninsula counties bordering Wisconsin on Central time"),
    ("MN", "Minnesota", "Central", ""), ("MS", "Mississippi", "Central", ""), ("MO", "Missouri", "Central", ""),
    ("MT", "Montana", "Mountain", ""), ("NE", "Nebraska", "Central", "western Nebraska on Mountain time"),
    ("NV", "Nevada", "Pacific", ""), ("NH", "New Hampshire", "Eastern", ""), ("NJ", "New Jersey", "Eastern", ""),
    ("NM", "New Mexico", "Mountain", ""), ("NY", "New York", "Eastern", ""), ("NC", "North Carolina", "Eastern", ""),
    ("ND", "North Dakota", "Central", "southwestern North Dakota on Mountain time"), ("OH", "Ohio", "Eastern", ""),
    ("OK", "Oklahoma", "Central", ""), ("OR", "Oregon", "Pacific", "most of Malheur County on Mountain time"),
    ("PA", "Pennsylvania", "Eastern", ""), ("RI", "Rhode Island", "Eastern", ""), ("SC", "South Carolina", "Eastern", ""),
    ("SD", "South Dakota", "Central", "western South Dakota on Mountain time"),
    ("TN", "Tennessee", "Central", "eastern Tennessee on Eastern time"),
    ("TX", "Texas", "Central", "El Paso and Hudspeth counties on Mountain time"), ("UT", "Utah", "Mountain", ""),
    ("VT", "Vermont", "Eastern", ""), ("VA", "Virginia", "Eastern", ""), ("WA", "Washington", "Pacific", ""),
    ("WV", "West Virginia", "Eastern", ""), ("WI", "Wisconsin", "Central", ""), ("WY", "Wyoming", "Mountain", ""),
]
ZONE_OFFSETS = {"Eastern": -5, "Central": -6, "Mountain": -7, "Mountain (Arizona)": -7, "Pacific": -8, "Alaska": -9,
                "Hawaii-Aleutian": -10}


def write_zones(target):
    """the centre's calling-hours reference: each state's zone, its offsets from UTC and the 2026 daylight time dates"""
    rows = []
    for st, name, zone, other in ZONE_ROWS:
        std = ZONE_OFFSETS[zone]
        dst = zone not in ("Mountain (Arizona)", "Hawaii-Aleutian")
        rows.append(dict(state=st, state_name=name, time_zone=zone, utc_offset_standard=std,
                         utc_offset_daylight=std + 1 if dst else std, observes_daylight_time="yes" if dst else "no",
                         daylight_time_begins_2026="2026-03-08 02:00" if dst else "",
                         daylight_time_ends_2026="2026-11-01 02:00" if dst else "", other_zone_areas=other))
    frame = set(P.RELABEL_STATE.get(s, s) for s in P.STATE_TZ)
    known = {r["state"]: r for r in rows}
    for s in frame:
        assert known[s]["other_zone_areas"] == "" and s in known, "the frame reaches a split state " + s
    pd.DataFrame(rows).to_csv(os.path.join(target, FILES["zones"]), index=False, lineterminator="\n")


def _xlsx_finish(path, author, created, modified):
    postprocess.scrub(path, author, created[:10])
    postprocess.finish_office(path, created, modified, P.COMPANY)


def write_register(target, rows):
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
    frames = {"KR-2604": "landline RDD", "KR-2615": "landline RDD", "KR-2626": "landline RDD",
              "KR-2618": "client list (households)", "KR-2609": "business list", "KR-2644": "business list",
              "KR-2651": "provider list"}
    for job, name, client, *_ in P.PROJECTS:
        ws.append([job, name, client, frames.get(job, "client list (landline numbers)"), sim.LINES[job][2:],
                   "On (balanced)", None, "Mon to Sat"])
    for col, w in zip("ABCDEFGH", [10, 42, 40, 30, 15, 15, 15, 17]):
        ws.column_dimensions[col].width = w
    # the jobs the centre fielded in 2026 that do not recur: kept on the register's second sheet for the year's close
    off = rows[rows["job"].eq(P.ONE_OFF[0])]
    cs = wb.create_sheet("Closed 2026 jobs")
    cs.append(["Job", "Project", "Client", "Type", "First call", "Last call", "Caller-ID line"])
    for c in cs[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE6F0")
    cs.append([P.ONE_OFF[0], P.ONE_OFF[1], P.ONE_OFF[2], "one-off study, not recurring",
               off["placed"].min().strftime("%Y-%m-%d"), off["placed"].max().strftime("%Y-%m-%d"),
               sim.LINES[P.ONE_OFF[0]][2:]])
    for col, w in zip("ABCDEFG", [10, 30, 16, 28, 12, 12, 15]):
        cs.column_dimensions[col].width = w
    p = os.path.join(target, FILES["register"])
    wb.save(p)
    _xlsx_finish(p, P.DIRECTOR, "2026-11-18T15:02:00Z", "2026-12-04T10:41:00Z")


POLICY_TITLE = "Telephone centre dialer policy, 2027 project year"
POLICY_OWNER = ("Kettle River Research, telephone operations. Owner: Hailey Mullins, director of telephone operations. "
                "Issued 20 November 2026; replaces the 2026 policy.")
POLICY_PARAS = [
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
    ("6. Call records.", "The dialer and the inbound switch stamp every call in the centre's own local time "
     "(Central time, with daylight saving time) and keep their records for three years."),
]
W_NS = ('xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" mc:Ignorable="w14"')
XML_DECL = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _policy_parts():
    """the package Word writes for a short memo in its Normal template, with only the styles the memo uses"""
    rng = np.random.default_rng(P.SEED + 51)
    rsid = ["00%06X" % int(x) for x in rng.integers(0x100000, 0xFFFFFF, 4)]
    para_id = iter("%08X" % int(x) for x in rng.integers(0x10000000, 0x7FFFFFFF, 20))

    def p(runs, after=None):
        ppr = '<w:pPr><w:spacing w:after="%d"/></w:pPr>' % after if after is not None else ""
        body = "".join('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, _esc(t)) for rpr, t in runs)
        return '<w:p w14:paraId="%s" w14:textId="77777777" w:rsidR="%s" w:rsidRDefault="%s">%s%s</w:p>' % (
            next(para_id), rsid[1], rsid[1], ppr, body)

    body = [p([('<w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>', POLICY_TITLE)]),
            p([("", POLICY_OWNER)])]
    for lead, text in POLICY_PARAS:
        body.append(p([("<w:rPr><w:b/><w:bCs/></w:rPr>", lead + " "), ("", text)], after=120))
    sect = ('<w:sectPr w:rsidR="%s"><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" '
            'w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/><w:cols w:space="720"/>'
            '<w:docGrid w:linePitch="360"/></w:sectPr>' % rsid[0])
    document = XML_DECL + '<w:document %s><w:body>%s%s</w:body></w:document>' % (W_NS, "".join(body), sect)
    styles = (XML_DECL + '<w:styles %s><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:asciiTheme="minorHAnsi" '
              'w:eastAsiaTheme="minorHAnsi" w:hAnsiTheme="minorHAnsi" w:cstheme="minorBidi"/><w:kern w:val="2"/>'
              '<w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="en-US" w:eastAsia="en-US" w:bidi="ar-SA"/>'
              '</w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="160" w:line="259" '
              'w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
              '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/>'
              '</w:style><w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont"><w:name '
              'w:val="Default Paragraph Font"/><w:uiPriority w:val="1"/><w:semiHidden/><w:unhideWhenUsed/></w:style>'
              '<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/>'
              '<w:uiPriority w:val="99"/><w:semiHidden/><w:unhideWhenUsed/><w:tblPr><w:tblInd w:w="0" w:type="dxa"/>'
              '<w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/><w:bottom w:w="0" '
              'w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style></w:styles>'
              % W_NS)
    settings = (XML_DECL + '<w:settings %s><w:zoom w:percent="100"/><w:proofState w:spelling="clean" '
                'w:grammar="clean"/><w:defaultTabStop w:val="720"/><w:characterSpacingControl w:val="doNotCompress"/>'
                '<w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word"'
                ' w:val="15"/><w:compatSetting w:name="overrideTableStyleFontSizeAndJustification" '
                'w:uri="http://schemas.microsoft.com/office/word" w:val="1"/><w:compatSetting '
                'w:name="enableOpenTypeFeatures" w:uri="http://schemas.microsoft.com/office/word" w:val="1"/>'
                '<w:compatSetting w:name="doNotFlipMirrorIndents" w:uri="http://schemas.microsoft.com/office/word" '
                'w:val="1"/></w:compat><w:rsids><w:rsidRoot w:val="%s"/>%s</w:rsids><w:themeFontLang w:val="en-US"/>'
                '<w:clrSchemeMapping w:bg1="light1" w:t1="dark1" w:bg2="light2" w:t2="dark2" w:accent1="accent1" '
                'w:accent2="accent2" w:accent3="accent3" w:accent4="accent4" w:accent5="accent5" w:accent6="accent6" '
                'w:hyperlink="hyperlink" w:followedHyperlink="followedHyperlink"/><w:decimalSymbol w:val="."/>'
                '<w:listSeparator w:val=","/></w:settings>'
                % (W_NS, rsid[0], "".join('<w:rsid w:val="%s"/>' % r for r in sorted(rsid))))
    fonts = (XML_DECL + '<w:fonts %s><w:font w:name="Calibri"><w:panose1 w:val="020F0502020204030204"/>'
             '<w:charset w:val="00"/><w:family w:val="swiss"/><w:pitch w:val="variable"/></w:font>'
             '<w:font w:name="Times New Roman"><w:panose1 w:val="02020603050405020304"/><w:charset w:val="00"/>'
             '<w:family w:val="roman"/><w:pitch w:val="variable"/></w:font><w:font w:name="Calibri Light">'
             '<w:panose1 w:val="020F0302020204030204"/><w:charset w:val="00"/><w:family w:val="swiss"/>'
             '<w:pitch w:val="variable"/></w:font></w:fonts>' % W_NS)
    import docx
    tmpl = os.path.join(os.path.dirname(docx.__file__), "templates", "default.docx")
    import zipfile
    with zipfile.ZipFile(tmpl) as z:
        theme = z.read("word/theme/theme1.xml")
    paras = [POLICY_TITLE, POLICY_OWNER] + [l + " " + t for l, t in POLICY_PARAS]
    words = sum(len(p_.split()) for p_ in paras)
    chars = sum(len(p_.replace(" ", "")) for p_ in paras)
    text = " ".join(paras)
    app = (XML_DECL + '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Template>Normal.dotm'
           '</Template><TotalTime>47</TotalTime><Pages>1</Pages><Words>%d</Words><Characters>%d</Characters>'
           '<Application>Microsoft Office Word</Application><DocSecurity>0</DocSecurity><Lines>%d</Lines>'
           '<Paragraphs>%d</Paragraphs><ScaleCrop>false</ScaleCrop><Company>%s</Company>'
           '<LinksUpToDate>false</LinksUpToDate><CharactersWithSpaces>%d</CharactersWithSpaces>'
           '<SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion>'
           '</Properties>' % (words, chars, sum(-(-len(p_) // 92) for p_ in paras), len(paras), P.COMPANY,
                              sum(len(p_) for p_ in paras)))
    core = (XML_DECL + '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/'
            'core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<dc:title>%s</dc:title><dc:creator>%s</dc:creator><cp:lastModifiedBy>%s</cp:lastModifiedBy>'
            '<cp:revision>4</cp:revision><dcterms:created xsi:type="dcterms:W3CDTF">2026-11-12T20:20:00Z'
            '</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">2026-11-20T15:05:00Z</dcterms:modified>'
            '</cp:coreProperties>' % (POLICY_TITLE, P.DIRECTOR, P.DIRECTOR))
    R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    rels = (XML_DECL + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId3" Type="%s/extended-properties" Target="docProps/app.xml"/><Relationship '
            'Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" '
            'Target="docProps/core.xml"/><Relationship Id="rId1" Type="%s/officeDocument" Target="word/document.xml"/>'
            '</Relationships>' % (R, R))
    doc_rels = (XML_DECL + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId3" Type="%s/fontTable" Target="fontTable.xml"/><Relationship Id="rId2" '
                'Type="%s/settings" Target="settings.xml"/><Relationship Id="rId1" Type="%s/styles" '
                'Target="styles.xml"/><Relationship Id="rId4" Type="%s/theme" Target="theme/theme1.xml"/>'
                '</Relationships>' % (R, R, R, R))
    W = "application/vnd.openxmlformats-officedocument.wordprocessingml"
    ctypes = (XML_DECL + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default '
              'Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default '
              'Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" '
              'ContentType="%s.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="%s.styles+xml"/>'
              '<Override PartName="/word/settings.xml" ContentType="%s.settings+xml"/><Override '
              'PartName="/word/fontTable.xml" ContentType="%s.fontTable+xml"/><Override PartName="/word/theme/'
              'theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/><Override '
              'PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
              '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.'
              'extended-properties+xml"/></Types>' % (W, W, W, W))
    return [("[Content_Types].xml", ctypes), ("_rels/.rels", rels), ("word/document.xml", document),
            ("word/_rels/document.xml.rels", doc_rels), ("word/theme/theme1.xml", theme),
            ("word/settings.xml", settings), ("word/styles.xml", styles), ("word/fontTable.xml", fonts),
            ("docProps/core.xml", core), ("docProps/app.xml", app)]


def write_policy(target):
    import zipfile
    path = os.path.join(target, FILES["policy"])
    with zipfile.ZipFile(path, "w") as z:
        for name, data in _policy_parts():
            zi = zipfile.ZipInfo(name, date_time=(2026, 11, 20, 9, 5, 12))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.create_system = 0
            z.writestr(zi, data.encode("utf-8") if isinstance(data, str) else data)
    names, bad = postprocess._scrubber().audit(path, postprocess.FLOOR, postprocess.CEILING)
    assert not names and not bad, (path, names, bad)


def write_spec(target):
    """the maker's release 6 test results, as its technical publications team exports them from Word"""
    from reportlab import rl_config
    rl_config.invariant = 1                  # no build clock or random document id in the file
    rl_config.useA85 = 0
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    fdir = "/usr/share/fonts/truetype/crosextra"
    for face, f in (("Calibri", "Carlito-Regular.ttf"), ("Calibri-Bold", "Carlito-Bold.ttf")):
        if face not in pdfmetrics.getRegisteredFontNames():
            ft = TTFont(face, os.path.join(fdir, f))
            ft.face.name = face.encode()
            pdfmetrics.registerFont(ft)
    navy = colors.HexColor("#1F3A5F")
    body = ParagraphStyle("b", fontName="Calibri", fontSize=10, leading=13.2, spaceAfter=6)
    h1 = ParagraphStyle("h1", fontName="Calibri-Bold", fontSize=18, leading=22, textColor=navy, spaceAfter=4)
    h2 = ParagraphStyle("h2", fontName="Calibri-Bold", fontSize=12, leading=15, textColor=navy, spaceBefore=8,
                        spaceAfter=4)
    small = ParagraphStyle("s", fontName="Calibri", fontSize=8, leading=10, textColor=colors.HexColor("#555555"))

    def grid(rows, widths):
        t = Table(rows, colWidths=widths)
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA5B1")),
                               ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF4")),
                               ("FONTNAME", (0, 0), (-1, 0), "Calibri-Bold"), ("FONTNAME", (0, 1), (-1, -1), "Calibri"),
                               ("FONTSIZE", (0, 0), (-1, -1), 9), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        return t

    def footer(canv, doc):
        canv.saveState()
        canv.setFont("Calibri", 7.5)
        canv.setFillColor(colors.HexColor("#555555"))
        canv.drawString(54, 36, "Larkspur Telephony, Inc.  |  LT-TR-0612 Rev. B  |  Answering machine detection, "
                                "release 6: test results")
        canv.drawRightString(558, 36, "Page %d of 2" % doc.page)
        canv.setStrokeColor(navy)
        canv.setLineWidth(1.2)
        canv.line(54, 744, 558, 744)
        canv.restoreState()

    path = os.path.join(target, FILES["spec"])
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=60, bottomMargin=56,
                            title="Answering machine detection, release 6: test results", author="Larkspur Telephony",
                            subject="LT-TR-0612 Rev. B")
    story = [Paragraph("Answering machine detection, release 6", h1),
             Paragraph("Test results for the Larkspur dialer platform, releases 6.0 to 6.2", h2),
             Paragraph("Detection decides from the first seconds of audio after the line is answered, on the cadence "
                       "of speech and silence, and returns LIVE or MACHINE to the dialer. The dialer acts on the result "
                       "according to the campaign's own settings.", body),
             Paragraph("1. Results by detection setting", h2),
             grid([["Setting", "Live answers classed as machine", "Machines classed as live", "Median decision time"],
                   ["Conservative", "0.8%", "14.2%", "2.6 s"], ["Balanced (default)", "2.1%", "6.5%", "2.3 s"],
                   ["Aggressive", "4.7%", "2.9%", "1.9 s"]], [112, 150, 130, 112]),
             Spacer(1, 8),
             Paragraph("Measured on the Larkspur reference set: 12,000 recorded answers from residential lines (6,000 "
                       "live answers and 6,000 answering machines and voicemail greetings), collected in 2023.", body),
             Paragraph("2. Reference set", h2),
             grid([["Recording type", "Recordings", "Source"],
                   ["Live answers, residential landline", "4,200", "consenting panel households, 31 states"],
                   ["Live answers, residential wireless", "1,800", "consenting panel households, 31 states"],
                   ["Answering machine greetings", "3,350", "panel households' own devices"],
                   ["Carrier voicemail greetings", "2,650", "the four national carriers and 22 regional carriers"]],
                  [190, 70, 244]),
             Spacer(1, 6),
             Paragraph("Each recording is played through the platform's media server at 8 kHz, "
                       "G.711 mu-law, with the network's own answer signalling. A recording is scored once per setting; "
                       "a result arriving after the 4.0 s analysis limit is scored as LIVE.", body),
             PageBreak(),
             Paragraph("3. Decision time", h2),
             grid([["Setting", "10th percentile", "Median", "90th percentile", "Limit"],
                   ["Conservative", "1.7 s", "2.6 s", "3.6 s", "4.0 s"], ["Balanced (default)", "1.5 s", "2.3 s", "3.3 s",
                                                                          "4.0 s"],
                   ["Aggressive", "1.2 s", "1.9 s", "2.8 s", "4.0 s"]], [112, 98, 98, 98, 98]),
             Paragraph("4. Changes in release 6", h2),
             Paragraph("6.0: new speech and silence model trained on the 2023 recordings; detection of carrier "
                       "voicemail tones moved ahead of the speech model.", body),
             Paragraph("6.1: corrected a fault in which a call answered during early media was scored on the ringback "
                       "audio; added the decision time to the dialer's call record.", body),
             Paragraph("6.2: support for G.722 trunks; no change to detection or to the results above.", body),
             Paragraph("5. Upgrading", h2),
             Paragraph("Release 6 installs over release 5.4 or later. The detection setting of each campaign is kept "
                       "through the upgrade. Sites on release 5.3 or earlier upgrade to 5.4 first.", body),
             Spacer(1, 10),
             Paragraph("Release 6, published March 2024.", body),
             Spacer(1, 18),
             Paragraph("Larkspur Telephony, Inc., technical publications. Results describe the reference set named "
                       "above and the platform's default media settings. Support: customers with a current maintenance "
                       "agreement, through the Larkspur customer portal.", small)]
    base = rl_config.canvas_basefontname
    rl_config.canvas_basefontname = "Calibri"
    try:
        doc.build(story, onFirstPage=footer, onLaterPages=footer)
    finally:
        rl_config.canvas_basefontname = base
    raw = open(path, "rb").read().replace(b"AAAAAA+Calibri-Bold", b"KJWQRF+Calibri-Bold").replace(
        b"AAAAAA+Calibri", b"BHKVOZ+Calibri")
    open(path, "wb").write(raw)
    from pypdf import PdfReader, PdfWriter
    w = PdfWriter(clone_from=PdfReader(path))
    w.add_metadata({"/Title": "Answering machine detection, release 6: test results", "/Author": "Larkspur Telephony",
                    "/Subject": "LT-TR-0612 Rev. B", "/Creator": "Microsoft Word for Microsoft 365",
                    "/Producer": "Microsoft Word for Microsoft 365",
                    "/CreationDate": "D:20240307141108-05'00'", "/ModDate": "D:20240311093627-05'00'"})
    with open(path, "wb") as fh:
        w.write(fh)
    names, bad = postprocess._scrubber().audit(path, postprocess.FLOOR, postprocess.CEILING)
    assert not names and not bad, (path, names, bad)


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
    billed = P.PROJECTS + [P.ONE_OFF]
    comp = rows[rows["outcome"].eq("COMPLETE") & rows["job"].isin([s[0] for s in billed])]
    q = comp.groupby(["job", comp["placed"].dt.quarter]).size().unstack(fill_value=0)
    wb = Workbook()
    ws = wb.active
    ws.title = "2026"
    ws.append(["Completed interviews invoiced, 2026"])
    ws["A1"].font = Font(bold=True)
    ws.append(["Job", "Q1", "Q2", "Q3", "Q4", "Year"])
    for c in ws[2]:
        c.font = Font(bold=True)
    for job, *_ in billed:
        v = [int(q.loc[job].get(k, 0)) if job in q.index else 0 for k in (1, 2, 3, 4)]
        ws.append([job] + v + [sum(v)])
    p = os.path.join(target, FILES["invoices"])
    wb.save(p)
    _xlsx_finish(p, "Accounts", "2026-01-05T15:10:00Z", "2027-01-08T14:22:00Z")   # the year's running ledger


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
        write_register(target, rows)
        write_policy(target)
        write_spec(target)
        write_listening(target)
        write_invoices(target, rows)
    W["rows"], W["inb"], W["ts"] = rows, inb, ts
    return W
