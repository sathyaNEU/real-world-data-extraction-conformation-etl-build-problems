"""task177 goldens: the forecast workbook, the aftermath note, generator/figures.json and submission.md, every figure
computed once from the shipped files (calc.py) and carried."""
from __future__ import annotations

import datetime as dt
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as K           # noqa: E402
import common as C         # noqa: E402
import postprocess as PP   # noqa: E402

F_BOOK = "assistant_share_forecast_mar_apr_2027.xlsx"
F_NOTE = "assistant_first_aftermath_note.docx"
MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December")
FRACTION = {2: "a half", 3: "a third", 4: "a quarter", 5: "a fifth", 6: "a sixth", 7: "a seventh"}


def figures(target):
    Q = K.solve(target)
    fits = Q["fits"]
    sp = fits["split"]["P"]
    ratio = sp["a_forced"] / sp["a_free"]
    F = dict(
        call_share=C.pct5(Q["share"]),
        share_unrounded=round(Q["share"], 4),
        share_af=C.pct(Q["share_af"]),
        share_one_rate=C.pct5(Q["share_one_rate"]),
        share_teach_nothing=C.pct5(Q["share_teach_nothing"]),
        share_last8=C.pct(Q["share_last8"]),
        share_no_persev=C.pct5(Q["share_split_no_persev"]),
        share_persev_exp=C.pct5(Q["share_split_persev_exp"]),
        release=Q["filed"]["release"],
        n_pop=Q["n_pop"],
        n_contacts=Q["n_contacts"],
        n_calls=Q["n_calls"],
        n_conversations=Q["n_conversations"],
        n_redirects=Q["n_redirects"],
        ratio=round(ratio, 2),
        ratio_words="about " + FRACTION[int(round(1 / ratio))],
        a_free=round(sp["a_free"], 2),
        q0=round(float(sp["q0b"]), 2),
        a_forced=round(sp["a_forced"], 2),
        ll_gain_one_rate=int(round(fits["split"]["ll"] - fits["one_rate"]["ll"])),
        ll_gain_floor=Q["ll_gain_floor"],
        ll_gain_teach_nothing=int(round(fits["split"]["ll"] - fits["teach_nothing"]["ll"])),
        ll_gain_persev_exp=int(round(fits["split"]["ll"] - fits["split_persev_exp"]["ll"])),
        ll_gain_no_persev=int(round(fits["split"]["ll"] - fits["split_no_persev"]["ll"])),
        bt_one_rate_pred=C.pct(Q["backtest"]["one_rate"]["pred"]),
        bt_split_pred=C.pct(Q["backtest"]["split"]["pred"]),
        bt_observed=C.pct(Q["backtest"]["split"]["obs"]),
        bt_ll_gain=int(round(Q["backtest"]["split"]["ll"] - Q["backtest"]["one_rate"]["ll"])),
        bt_n="{:,}".format(Q["backtest"]["split"]["n"]),
        p_new_pct=round(100 * Q["filed"]["p_new"], 1),
        cycle=Q["filed"]["cycle"],
        bn=Q["filed"]["bn"],
        vendor_bn=Q["filed"]["vendor_bn"],
        n_day_cut=Q["n_day_cut"],
        accept_resolved=Q["filed"]["accept_resolved"],
        accept_n=Q["filed"]["accept_n"],
        p_phone_pct=round(100 * Q["aux"]["p_phone"], 1),
        p_over_pct=round(100 * Q["aux"]["p_over"], 1),
        monthly_share={MONTHS[m - 1]: C.pct(v) for m, v in Q["monthly_share"].items()},
        next_choice={k: (round(100 * v[0], 1), v[1]) for k, v in sorted(Q["next_choice"].items())},
        ask_employers={MONTHS[i]: v for i, v in enumerate(Q["ask_employers"])},
        ask_own={MONTHS[i]: v for i, v in enumerate(Q["ask_own"])},
        fits={k: dict(ll=float(v["ll"]), **{p: round(float(x), 6) for p, x in v["P"].items()})
              for k, v in fits.items()},
    )
    return F, Q


# --------------------------------------------------------------------------------------------------- the workbook
def write_workbook(path, F):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    head = PatternFill("solid", fgColor="DCE6F1")
    bold = Font(bold=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "Forecast"
    rows = [
        ("Ask Prairie Works: share of jobseekers' own contacts, 1 March to 25 April 2027", None),
        ("Digital Channels, prepared 5 January 2027 for the March and April usage tier", None),
        (None, None),
        ("Forecast share started in Ask Prairie Works (nearest 5 per cent)", F["call_share"]),
        ("Jobseekers on the register on 3 January 2027", F["n_pop"]),
        ("Their share in the last eight weeks of 2026 (whole per cent)", F["share_last8"]),
        (None, None),
        ("Inputs", None),
        ("Release 4.0 resolved in the acceptance test (per cent)", F["p_new_pct"]),
        ("Calls an adviser or the queue resolved in 2026 (per cent)", F["p_phone_pct"]),
        ("Claimant-line calls the overflow transferred to the assistant in 2026 (per cent)", F["p_over_pct"]),
        ("Check-ins", "every 14 days from the claim's opening (rollout plan 4.1)"),
        ("Other contacts", "at the 2026 rate per jobseeker-day, all jobseekers alike"),
        (None, None),
        ("Learning from contacts the jobseeker did not choose", None),
        ("An overflow transfer moves the assistant's value", F["ratio_words"] + " as far as a chosen conversation"),
        ("Learning rate, contacts the jobseeker chose", F["a_free"]),
        ("Learning rate, overflow transfers", F["a_forced"]),
        ("One learning rate for every contact would give (nearest 5 per cent)", F["share_one_rate"]),
    ]
    for i, (a, b) in enumerate(rows, 1):
        if a is not None:
            ws.cell(row=i, column=1, value=a)
        if b is not None:
            ws.cell(row=i, column=2, value=b)
    fmt = {"Jobseekers on the register on 3 January 2027": "#,##0",
           "Release 4.0 resolved in the acceptance test (per cent)": "0.0",
           "Calls an adviser or the queue resolved in 2026 (per cent)": "0.0",
           "Claimant-line calls the overflow transferred to the assistant in 2026 (per cent)": "0.0",
           "Learning rate, contacts the jobseeker chose": "0.00", "Learning rate, overflow transfers": "0.00"}
    for i, (a, b) in enumerate(rows, 1):
        if a in fmt:
            ws.cell(row=i, column=2).number_format = fmt[a]
    ws.cell(row=1, column=1).font = Font(bold=True, size=13)
    for r in (4, 8, 15):
        ws.cell(row=r, column=1).font = bold
    ws.cell(row=4, column=2).font = Font(bold=True, size=13)
    ws.column_dimensions["A"].width = 86
    ws.column_dimensions["B"].width = 44

    ws2 = wb.create_sheet("Model comparison")
    hdr = ("Model", "Log-likelihood", "Split model ahead by", "Rate, chosen", "Rate, transfers", "Choice weight",
           "Lean", "Pull to last choice", "Forecast share (nearest 5 per cent)")
    names = (("split", "Separate rate for overflow transfers (used)", F["call_share"]),
             ("one_rate", "One rate for every contact", F["share_one_rate"]),
             ("teach_nothing", "Overflow transfers teach nothing", F["share_teach_nothing"]),
             ("split_no_persev", "Separate rate, no pull to the last choice", F["share_no_persev"]),
             ("split_persev_exp", "Separate rate, pull to the last channel met", F["share_persev_exp"]))
    for j, h in enumerate(hdr, 1):
        c = ws2.cell(row=1, column=j, value=h)
        c.font = bold
        c.fill = head
        c.alignment = Alignment(wrap_text=True, vertical="top")
    base = F["fits"]["split"]["ll"]
    fmts = (None, "#,##0.0", "#,##0", "0.00", "0.00", "0.00", "0.00", "0.00", "0")
    for i, (k, label, share) in enumerate(names, 2):
        f = F["fits"][k]
        vals = (label, round(f["ll"], 1), int(round(base - f["ll"])), round(f["a_free"], 2), round(f["a_forced"], 2),
                round(f["beta"], 2), round(f["bias"], 2), round(f["kappa"], 2), share)
        for j, v in enumerate(vals, 1):
            if v is not None:
                c = ws2.cell(row=i, column=j, value=v)
                if fmts[j - 1]:
                    c.number_format = fmts[j - 1]
    ws2.cell(row=8, column=1, value="Fitted by maximum likelihood to each jobseeker's own contacts from 5 January 2026 "
                                    "to 3 January 2027 (calls to the claimant line by case number, conversations in "
                                    "the app or on the web by linked account).")
    ws2.cell(row=10, column=1, value="Back-test: fitted to January to October 2026, November and December scored").font = bold
    for j, h in enumerate(("Model", "Predicted share in the assistant (whole per cent)", "Observed (whole per cent)",
                           "Held-out log-likelihood behind the split"), 1):
        c = ws2.cell(row=11, column=j, value=h)
        c.font = bold
        c.fill = head
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, (label, pr, gap) in enumerate((("Separate rate for overflow transfers", F["bt_split_pred"], 0),
                                          ("One rate for every contact", F["bt_one_rate_pred"], F["bt_ll_gain"])), 12):
        ws2.cell(row=i, column=1, value=label)
        ws2.cell(row=i, column=2, value=pr)
        ws2.cell(row=i, column=3, value=F["bt_observed"])
        ws2.cell(row=i, column=4, value=gap).number_format = "#,##0"
    for col, w in zip("ABCDEFGHI", (46, 15, 14, 12, 14, 13, 9, 12, 16)):
        ws2.column_dimensions[col].width = w

    ws3 = wb.create_sheet("Record 2026")
    for j, h in enumerate(("Month", "Own contacts started in Ask Prairie Works (whole per cent)"), 1):
        c = ws3.cell(row=1, column=j, value=h)
        c.font = bold
        c.fill = head
    for i, (m, v) in enumerate(F["monthly_share"].items(), 2):
        ws3.cell(row=i, column=1, value=m)
        ws3.cell(row=i, column=2, value=v)
    r0 = len(F["monthly_share"]) + 3
    for j, h in enumerate(("The next contact after", "Share started in Ask Prairie Works (per cent)", "Contacts"), 1):
        c = ws3.cell(row=r0, column=j, value=h)
        c.font = bold
        c.fill = head
    labels = {"after_chosen_resolved": "a conversation the jobseeker opened, resolved",
              "after_chosen_unresolved": "a conversation the jobseeker opened, not resolved",
              "after_transfer_resolved": "an overflow transfer, resolved",
              "after_transfer_unresolved": "an overflow transfer, not resolved",
              "after_call_resolved": "a call an adviser answered, resolved",
              "after_call_unresolved": "a call not resolved"}
    for i, k in enumerate(("after_chosen_resolved", "after_chosen_unresolved", "after_transfer_resolved",
                           "after_transfer_unresolved", "after_call_resolved", "after_call_unresolved"), r0 + 1):
        v, n = F["next_choice"][k]
        ws3.cell(row=i, column=1, value=labels[k])
        ws3.cell(row=i, column=2, value=v)
        ws3.cell(row=i, column=3, value=n)
    ws3.column_dimensions["A"].width = 52
    ws3.column_dimensions["B"].width = 34
    ws3.column_dimensions["C"].width = 12

    ws4 = wb.create_sheet("Employers and own use")
    for j, h in enumerate(("Month (2026, Manitoba time)", "Employers' conversations",
                           "Our own staff and test conversations"), 1):
        c = ws4.cell(row=1, column=j, value=h)
        c.font = bold
        c.fill = head
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, m in enumerate(MONTHS, 2):
        ws4.cell(row=i, column=1, value=m)
        ws4.cell(row=i, column=2, value=F["ask_employers"][m]).number_format = "#,##0"
        ws4.cell(row=i, column=3, value=F["ask_own"][m]).number_format = "#,##0"
    ws4.cell(row=14, column=1, value="2026").font = bold
    c = ws4.cell(row=14, column=2, value=sum(F["ask_employers"].values()))
    c.number_format = "#,##0"
    c.font = bold
    c = ws4.cell(row=14, column=3, value=sum(F["ask_own"].values()))
    c.number_format = "#,##0"
    c.font = bold
    ws4.cell(row=16, column=1, value="A conversation counts once, in the month its first session started, Manitoba "
                                     "time. The test employers registered to our own business number are our own use; "
                                     "the employer widget writes UTC, moved here to Manitoba time, and closes the "
                                     "sessions open at midnight UTC, carrying each on as a new conversation from the "
                                     "same account, counted here once. Riverlot's support "
                                     "desk works in the staff console under accounts registered to Riverlot's business "
                                     "number; those conversations are the vendor's and are not counted.")
    for col, w in zip("ABC", (30, 24, 34)):
        ws4.column_dimensions[col].width = w
    ws5 = wb.create_sheet("Notes")
    notes = [
        ("As of", "Exports pulled 4 January 2027; the record runs 5 January 2026 to 3 January 2027."),
        ("Population", "Jobseekers with a claim open on 3 January 2027 (claims_register_2026.csv). Nobody whose claim "
                       "opens later is in the forecast."),
        ("Contact", "A call to the claimant line keyed with a case number, or a conversation opened in the app or on "
                    "the web (rollout plan 5.1). A call the overflow transferred to the voice service is a call."),
        ("Conversation", "Counted once however many sessions it ran to (rollout plan 5.2); its outcome is its last "
                         "session's end state."),
        ("Window", "1 March to 25 April 2027, after the assistant-first weeks of 4 January to 28 February."),
        ("Release 4.0", "Resolving 2,041 of the acceptance test's 2,400 conversations."),
        ("Rounding", "The forecast shares to the nearest 5 per cent, rounded once from the unrounded forecast; the "
                     "2026 record's shares to the whole per cent; counts whole."),
        ("Sources", "contact_legs_2026.csv, assistant_sessions_2026.jsonl, contact_details_crosswalk.csv, "
                    "claims_register_2026.csv, %s, %s, %s." % (C.F_PLAN, C.F_ACCEPT, C.F_ORDER)),
    ]
    for i, (a, b) in enumerate(notes, 1):
        ws5.cell(row=i, column=1, value=a).font = bold
        ws5.cell(row=i, column=2, value=b).alignment = Alignment(wrap_text=True, vertical="top")
    ws5.column_dimensions["A"].width = 16
    ws5.column_dimensions["B"].width = 110
    for s in (ws2, ws3, ws4):
        s.freeze_panes = "A2"
    wb.save(path)
    PP.normalize_ooxml(path, "Sabrina Ward", "Sabrina Ward", "2027-01-04T21:10:00Z", "2027-01-05T18:42:00Z",
                       excel=True, company=C.ORG)


# ------------------------------------------------------------------------------------------------------- the note
def chart_png(F):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams["svg.hashsalt"] = "task177"
    fig, ax = plt.subplots(figsize=(6.4, 2.9), dpi=150)
    months = list(F["monthly_share"].keys())
    vals = list(F["monthly_share"].values())
    xs = list(range(len(months)))
    ax.plot(xs, vals, color="#1c4e80", marker="o", lw=1.8, label="2026, every jobseeker's own contacts")
    x_af, x_win = len(months) + 0.6, len(months) + 2.4
    ax.bar([x_af], [F["share_af"]], width=1.2, color="#9fb7d4", label="Jan to Feb 2027, assistant-first (forecast)")
    ax.bar([x_win], [F["call_share"]], width=1.2, color="#1c4e80", label="1 Mar to 25 Apr 2027 (forecast)")
    ax.plot([x_win - 0.6, x_win + 0.6], [F["share_one_rate"]] * 2, color="#b5442f", lw=1.6, ls="--",
            label="one learning rate for every contact")
    ax.text(x_win, F["call_share"] + 1.0, "%d%%" % F["call_share"], ha="center", fontsize=8.5, color="#1c4e80")
    ax.text(x_win, F["share_one_rate"] + 1.0, "%d%%" % F["share_one_rate"], ha="center", fontsize=8.5,
            color="#b5442f")
    ax.set_xticks(xs + [x_af, x_win])
    ax.set_xticklabels([m[:3] for m in months] + ["Jan-Feb", "Mar-Apr"], fontsize=7.5)
    ax.set_ylabel("Started in the assistant (%)", fontsize=8)
    ax.set_ylim(0, max(F["share_one_rate"], max(vals)) + 8)
    ax.tick_params(axis="y", labelsize=7.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(fontsize=6.8, frameon=False, loc="upper right", ncol=2)
    ax.set_title("The assistant-first weeks lift the share to %d per cent, not %d" % (F["call_share"],
                                                                                      F["share_one_rate"]),
                 fontsize=9, loc="left")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def note_paragraphs(F):
    return [
        ("h", "Jobseekers will start %d per cent of their own contacts in Ask Prairie Works in March and April"
              % F["call_share"]),
        ("p", "To: Loretta Rodgers, Head of Contact Services\nFrom: Sabrina Ward, Digital Channels\nDate: 5 January "
              "2027\nSubject: the March and April usage tier, due with the vendor on 8 January"),
        ("b", "Jobseekers on the register on 3 January 2027 will start %d per cent of the contacts they make themselves "
              "between 1 March and 25 April 2027 in Ask Prairie Works." % F["call_share"]),
        ("p", "That is up from %d per cent in the last eight weeks of 2026, and well short of the %d per cent a "
              "learning model with one rate for every contact gives once release 4.0 has answered every claimant-line "
              "call for eight weeks." % (F["share_last8"], F["share_one_rate"])),
        ("h2", "Why the assistant-first weeks convert fewer jobseekers than they appear to"),
        ("p", "In 2026 each jobseeker's channel choice followed what the two channels had done for them: a resolved "
              "conversation made the next one more likely, an unresolved one less. The calls the overflow transferred "
              "to the voice service are the only contacts in the record where a jobseeker who picked the phone met the "
              "assistant instead, %s of them. In a learning model fitted to every jobseeker's 2026 contacts, those "
              "moved the jobseeker's later choices %s as far as a conversation they had opened themselves (the "
              "workbook's Model comparison sheet has the fitted rates)."
              % ("{:,}".format(F["n_redirects"]), F["ratio_words"])),
        ("p", "The assistant-first weeks are eight weeks of exactly that kind of contact. A model that learns from them "
              "at the chosen rate still looks right on 2026: fitted to January to October it predicts %d per cent of "
              "November and December's own contacts in the assistant, and %d per cent is what happened, because "
              "transfers are a small part of the record. Carried through the assistant-first weeks it gives %d per cent. "
              "The separate rate predicts those %s November and December choices better by %s log-likelihood units, "
              "fits the whole record better by %s, and beats treating transfers as teaching nothing by %s."
              % (F["bt_one_rate_pred"], F["bt_observed"], F["share_one_rate"], F["bt_n"],
                 "{:,}".format(F["bt_ll_gain"]), "{:,}".format(F["ll_gain_one_rate"]),
                 "{:,}".format(F["ll_gain_teach_nothing"]))),
        ("table", None),
        ("chart", None),
        ("h2", "What the forecast rests on"),
        ("p", "Release 4.0 resolving the conversations it takes as it resolved %s of the acceptance test's %s; calls "
              "an adviser takes resolving as in 2026; check-ins every %d days from each claim's opening; other "
              "questions at the 2026 rate; the overflow transfer back on from 1 March. Jobseekers whose claims close "
              "before March drop out without changing the share."
              % ("{:,}".format(F["accept_resolved"]), "{:,}".format(F["accept_n"]), F["cycle"])),
        ("h2", "For the order"),
        ("p", "The March and April chat tiers carry employers and our own staff and test use as well as jobseekers. "
              "The workbook has their 2026 conversations month by month, counted the way the forecast counts "
              "jobseekers' contacts."),
        ("p", "Attached: %s (the forecast, the model comparison, the 2026 record and the monthly counts)." % F_BOOK),
        ("foot", "Shares are of contacts, not of jobseekers. A call the overflow transferred to the voice service "
                 "counts as a call, as rollout plan 5.1 has it."),
    ]


def write_note(path, F):
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    sec = d.sections[0]
    fp = sec.footer.paragraphs[0]
    fp.text = "Prairie Works Manitoba, Digital Channels. Internal."
    fp.runs[0].font.size = Pt(8)
    for kind, text in note_paragraphs(F):
        if kind == "table":
            rows = (("Model of 2026", "Behind the split model, log-likelihood units", "1 March to 25 April"),
                    ("Separate rate for transfers (used)", "0", "%d%%" % F["call_share"]),
                    ("One rate for every contact", "{:,}".format(F["ll_gain_one_rate"]), "%d%%" % F["share_one_rate"]),
                    ("Transfers teach nothing", "{:,}".format(F["ll_gain_teach_nothing"]),
                     "%d%%" % F["share_teach_nothing"]))
            tb = d.add_table(rows=len(rows), cols=3)
            tb.style = "Light List Accent 1"
            for i, r in enumerate(rows):
                for j, v in enumerate(r):
                    tb.cell(i, j).text = v
            src_ = d.add_paragraph("Source: %s and %s, 5 January 2026 to 3 January 2027." % (C.F_LEGS, C.F_CONV))
            src_.runs[0].font.size = Pt(8.5)
            src_.runs[0].font.color.rgb = RGBColor(0x5D, 0x64, 0x6D)
            continue
        if kind == "foot":
            p = d.add_paragraph(text)
            p.runs[0].font.size = Pt(8.5)
            p.runs[0].font.color.rgb = RGBColor(0x5D, 0x64, 0x6D)
            continue
        if kind == "h":
            p = d.add_heading(text, level=1)
        elif kind == "h2":
            d.add_heading(text, level=2)
        elif kind == "b":
            p = d.add_paragraph()
            r = p.add_run(text)
            r.bold = True
        elif kind == "chart":
            d.add_picture(io.BytesIO(chart_png(F)), width=Inches(6.2))
            cap = d.add_paragraph("Share of jobseekers' own contacts started in Ask Prairie Works: 2026 by month, and "
                                  "the forecast for 2027.")
            cap.runs[0].font.size = Pt(8.5)
            cap.runs[0].font.color.rgb = RGBColor(0x5D, 0x64, 0x6D)
        else:
            d.add_paragraph(text)
    d.save(path)
    PP.normalize_docx(path, "Sabrina Ward", "Sabrina Ward", "2027-01-05T15:20:00Z", "2027-01-05T18:55:00Z",
                      revision=4, total_time=96, seed="task177/note",
                      title="Ask Prairie Works after the assistant-first weeks", company=C.ORG)


# --------------------------------------------------------------------------------------------- figures.json, write-up
def write_figures(path, F):
    out = dict(F)
    out.pop("fits")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")


def write_submission(path, F):
    emp, own = F["ask_employers"], F["ask_own"]
    lines = [
        "## Tags",
        "",
        "**Domain:** Psychology and behavioural science (decision-making and computational behavioural modelling).",
        "**Analytical objective:** Forecasting and predictive modelling.",
        "",
        "## 1. Final Recommendation",
        "",
        "**Jobseekers on the register on 3 January 2027 will start %d per cent of their own contacts between 1 March "
        "and 25 April 2027 in Ask Prairie Works.**" % F["call_share"],
        "Not the %d per cent one learning rate for every contact gives: overflow transfers, the record's only contacts "
        "a jobseeker did not choose, teach %s as much as a chosen conversation, and the assistant-first weeks are made "
        "of such contacts. Not the %d per cent of the last eight weeks of 2026, which ignores what the assistant-first "
        "weeks teach." % (F["share_one_rate"], F["ratio_words"], F["share_last8"]),
        "",
        "## 2. Critical Components",
        "",
        "1. An overflow transfer moves a jobseeker's later choices **%s** as far as a conversation they opened" %
        F["ratio_words"],
        "2. The 2026 record holds **%s** overflow transfers, the only contacts a jobseeker did not choose, among %s "
        "contacts" % ("{:,}".format(F["n_redirects"]), "{:,}".format(F["n_contacts"])),
        "",
        "## 3. Step-by-Step Solution",
        "",
        "1. Built each jobseeker's contacts from %s (claimant-line calls by the case number on the first leg, overflow "
        "transfers as the calls they came from with the voice session's end state) and %s (app and web conversations "
        "through the accounts in %s, a conversation's outcome its last session's end state): %s contacts, %s of them "
        "transfers." % (C.F_LEGS, C.F_CONV, C.F_XWALK, "{:,}".format(F["n_contacts"]), "{:,}".format(F["n_redirects"])),
        "2. Fitted by maximum likelihood a reinforcement-learning model of each jobseeker's choices (each channel's "
        "value starting at %s and moved toward the outcome, 1 resolved or 0 not, of each contact that met it; the "
        "choice a logistic of the value gap with a lean and a pull to the last channel chosen) with a separate "
        "learning rate for transfers: the transfers' rate is %s of the chosen rate, and the model fits the whole record "
        "more than %s log-likelihood units better than one rate." % (F["q0"], F["ratio_words"],
                                                                     "{:,}".format(F["ll_gain_floor"])),
        "3. Took the jobseekers with a claim open on 3 January 2027 in %s, each from the end state of their own "
        "record." % C.F_CLAIMS,
        "4. Simulated 4 January to 25 April 2027 per %s: every call met by release %s resolving %s of %s as in %s to 28 "
        "February, then the line back to advisers with the 2026 transfer share, check-ins every %d days from each "
        "claim's opening and other contacts at the 2026 rate: %d per cent of their own contacts in the window started "
        "in the assistant." % (
            C.F_PLAN, F["release"], "{:,}".format(F["accept_resolved"]), "{:,}".format(F["accept_n"]), C.F_ACCEPT,
            F["cycle"], F["call_share"]),
        "5. Counted the conversations in %s once each, in the month their first session started: employer-widget "
        "times (written in UTC, as their hours and the employer line's calls a few minutes later show) moved to "
        "Manitoba time, and each widget session closed at 00:00:00 UTC joined, as one conversation, to the session its "
        "account opened at that second under a new conversation id (%s such pairs); the employer accounts registered "
        "to Prairie Works Manitoba's own business number (%s, on %s) and the accounts the vendor re-typed as staff on "
        "14 September counted as our own use for the whole year; and the staff-console accounts registered to "
        "Riverlot's business number (%s, its GST/HST number on %s) left out as the vendor's own support desk: the "
        "monthly counts below." % (C.F_CONV, F["n_day_cut"], F["bn"], C.F_ORDER, F["vendor_bn"], C.F_INVOICES),
        "",
        "## 4. Deliverable Answers",
        "",
        "### %s" % F_BOOK,
        "",
        "1. Share of their own contacts jobseekers on the register on 3 January 2027 start in Ask Prairie Works, 1 "
        "March to 25 April 2027: %d per cent" % F["call_share"],
        "2. Employers' conversations with Ask Prairie Works, by month of 2026:",
    ]
    for m in MONTHS:
        lines.append("   - %s: %s" % (m, "{:,}".format(emp[m])))
    lines.append("3. Our own staff and test accounts' conversations, by month of 2026:")
    for m in MONTHS:
        lines.append("   - %s: %s" % (m, "{:,}".format(own[m])))
    lines += ["", "### %s" % F_NOTE, "",
              "1. The forecast of %d per cent with the reason it is below the one-rate figure of %d per cent, the "
              "chart of the 2026 monthly share against both forecasts, and the inputs it rests on."
              % (F["call_share"], F["share_one_rate"]), ""]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))


def main(target, golden, figures_path, submission):
    os.makedirs(golden, exist_ok=True)
    F, Q = figures(target)
    write_workbook(os.path.join(golden, F_BOOK), F)
    write_note(os.path.join(golden, F_NOTE), F)
    write_figures(figures_path, F)
    write_submission(submission, F)
    return F
