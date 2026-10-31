"""The independent verifier: reads only target/ (and the goldens it checks), on its own code path (pandas and an
Aalen-Johansen estimate of each scenario's SAR and no-SAR incidence by alert age, where the generator reads a
look-up of older alerts), and recomputes the call, both asks and the figures every golden carries.

    python3 task191/generator/verify.py
"""
import email
import json
import os
import re
import subprocess
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
G = os.path.join(TASK, "golden")
FAILS = []


def check(label, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + label + ("" if ok else "   " + str(detail)))
    if not ok:
        FAILS.append(label)


def eastern(ts):
    """UTC timestamps to US Eastern wall-clock time (pandas' own zone rules, not the generator's)."""
    return ts.dt.tz_localize("UTC").dt.tz_convert("America/New_York").dt.tz_localize(None)


def read():
    D = {}
    D["runs"] = pd.read_csv(os.path.join(T, "tm_monitoring_runs_2025-07_2026-10.csv"), dtype=str)
    D["alerts"] = pd.read_csv(os.path.join(T, "tm_alerts_2025-07_2026-10.csv"), dtype=str, keep_default_na=False)
    D["sars"] = pd.read_csv(os.path.join(T, "sar_filings_2025-07_2026-10.csv"), dtype=str, keep_default_na=False)
    D["cases"] = json.load(open(os.path.join(T, "fcm_cases_export_2026-11-02.json"), encoding="utf-8"))
    cat = pd.read_excel(os.path.join(T, "tm_scenario_catalogue_2026.xlsx"), sheet_name=0, dtype=str).fillna("")
    D["catalogue"] = cat
    msg = email.message_from_bytes(open(os.path.join(T, "tuning_2027_thread.eml"), "rb").read())
    D["thread"] = msg.get_payload(decode=True).decode("utf-8")
    D["thread_date"] = msg["Date"]
    D["procedure"] = subprocess.run(["pdftotext", "-layout", os.path.join(T, "aml_alert_handling_procedure_2026.pdf"), "-"],
                                    capture_output=True, text=True).stdout
    return D


def filed(D):
    """The filed WHAT, read from the thread and the procedure (positive controls on each document's extractor)."""
    th = re.sub(r"\s+", " ", D["thread"])
    pr = re.sub(r"\s+", " ", D["procedure"])
    floor = re.search(r"falls below (\d+) per cent", th)
    check("thread: the floor is read from the planning thread", floor is not None and floor.group(1) == "3", floor)
    check("thread: the window is the twelve months to 30 September", "twelve months to 30 September" in th)
    check("thread: every alert counts by how it will end", "by how they will end" in th)
    check("thread: duplicates are not alerts of their scenario", "closed as a duplicate of another is not an alert" in th)
    check("thread: the alert belongs to its run's business date", "business date of the run that raised it" in th)
    check("thread: dated the morning of the extract", "02 Nov 2026" in D["thread_date"], D["thread_date"])
    check("procedure: the business day ends at 22:00 Eastern", "22:00 Eastern" in pr)
    check("procedure: an alert added to an open investigation opens none of its own", "opens no investigation of its own" in pr)
    check("procedure: a continuing activity report covers the activity since the previous report",
          "covering the activity since the previous report" in pr)
    check("procedure: a correction cites the report it corrects and covers the same activity",
          "cites the report it corrects and covers the same activity" in pr)
    return float(floor.group(1)) if floor else 3.0


def alerts_frame(D):
    cat = D["catalogue"]
    rep = {r["scenario_code"]: r["replaced_by"] for _, r in cat.iterrows() if r["replaced_by"]}
    check("catalogue: one replacement, XB-HRJ by XB-HRJ2", rep == {"XB-HRJ": "XB-HRJ2"}, rep)
    back = {v: k for k, v in rep.items()}
    a = D["alerts"].copy()
    a["scenario"] = a["scenario_code"].map(lambda s: back.get(s, s))
    bd = dict(zip(D["runs"]["run_id"], D["runs"]["business_date"]))
    a["bdate"] = pd.to_datetime(a["run_id"].map(bd))
    a["gen"] = pd.to_datetime(a["created_at_utc"].str.replace("Z", ""))
    a["tclosed"] = pd.to_datetime(a["triage_closed_at_utc"].str.replace("Z", "").replace("", None))
    cases = pd.DataFrame([{k: c[k] for k in ("case_id", "status", "disposition", "decided_at", "opened_at")}
                          for c in D["cases"]["cases"]])
    cases["decided"] = pd.to_datetime(cases["decided_at"].str.replace("Z", ""))
    a = a.merge(cases[["case_id", "status", "disposition", "decided"]], how="left", on="case_id")
    esc = a["triage_outcome"] == "ESC"
    a["event"] = 0
    a.loc[a["triage_outcome"] == "NSA", "event"] = 2
    a.loc[esc & (a["status"] == "CLOSED") & (a["disposition"] == "SAR filed"), "event"] = 1
    a.loc[esc & (a["status"] == "CLOSED") & (a["disposition"] == "No SAR"), "event"] = 2
    a["end"] = a["tclosed"].where(a["triage_outcome"] == "NSA", a["decided"])
    x = pd.Timestamp("2026-11-02 11:00:00")
    a.loc[a["event"] == 0, "end"] = x
    a["t"] = (a["end"] - a["gen"]).dt.total_seconds() / 86400.0
    a["age"] = (x - a["gen"]).dt.total_seconds() / 86400.0
    a = a[a["triage_outcome"] != "DUP"]
    check("every escalated alert of the export has its investigation in the case export",
          int((esc & a["status"].isna()).sum()) == 0)
    return a


def aalen_johansen(t, e):
    """Cumulative incidence of event 1 and the overall event-free survival, right-continuous step functions."""
    df = pd.DataFrame({"t": t, "e": e}).sort_values("t")
    times = np.sort(df.loc[df["e"] > 0, "t"].unique())
    n_at = len(df) - np.searchsorted(np.sort(df["t"].values), times, side="left")
    d1 = df[df["e"] == 1].groupby("t").size().reindex(times, fill_value=0).values
    d = df[df["e"] > 0].groupby("t").size().reindex(times, fill_value=0).values
    S, F1 = 1.0, 0.0
    s_out, f_out = [], []
    for k in range(len(times)):
        F1 += S * d1[k] / n_at[k]
        S *= 1.0 - d[k] / n_at[k]
        s_out.append(S)
        f_out.append(F1)
    return times, np.array(s_out), np.array(f_out)


def productivity(a, floor):
    year = a[(a["bdate"] >= "2025-10-01") & (a["bdate"] <= "2026-09-30")]
    out = {}
    for code, g in year.groupby("scenario"):
        allg = a[a["scenario"] == code]
        times, S, F1 = aalen_johansen(allg["t"].values, allg["event"].values)
        F1_inf = F1[-1]
        und = g[g["event"] == 0]
        idx = np.searchsorted(times, und["age"].values, side="right") - 1
        s_a = np.where(idx >= 0, S[np.clip(idx, 0, None)], 1.0)
        f_a = np.where(idx >= 0, F1[np.clip(idx, 0, None)], 0.0)
        p = np.where(s_a > 0, (F1_inf - f_a) / np.maximum(s_a, 1e-12), 1.0)
        out[code] = 100.0 * (int((g["event"] == 1).sum()) + float(p.sum())) / len(g)
    return out


def ask_a(D, a):
    al = D["alerts"]
    al = al[al["case_id"] != ""].copy()
    cat = D["catalogue"]
    back = {r["replaced_by"]: r["scenario_code"] for _, r in cat.iterrows() if r["replaced_by"]}
    al["scenario"] = al["scenario_code"].map(lambda s: back.get(s, s))
    cases = pd.DataFrame([{"case_id": c["case_id"], "opened_at": c["opened_at"]} for c in D["cases"]["cases"]])
    m = cases.merge(al, left_on=["case_id", "opened_at"], right_on=["case_id", "triage_closed_at_utc"], how="left")
    op = pd.to_datetime(m["opened_at"].str.replace("Z", ""))
    m["edate"] = eastern(op).dt.normalize()
    m = m[(m["edate"] >= "2025-10-01") & (m["edate"] <= "2026-09-30")]
    check("ask A: each investigation opened in the year has exactly one opening alert in the export",
          m["alert_id"].notna().all() and not m["case_id"].duplicated().any())
    m["q"] = m["edate"].dt.year.astype(str) + " Q" + ((m["edate"].dt.month - 1) // 3 + 1).astype(str)
    return m.groupby(["scenario", "q"]).size().to_dict()


def ask_b(D):
    s = D["sars"].copy()
    s["filed"] = pd.to_datetime(s["filed_at_utc"].str.replace("Z", ""))
    s = s.sort_values(["filed", "bsa_id"])
    period = {r.bsa_id: (r.activity_start, r.activity_end) for r in s.itertuples()}
    kind = {}
    for cid, g in s.groupby("case_id", sort=False):
        last_end = None
        for k, r in enumerate(g.itertuples()):
            if r.prior_bsa_id and r.prior_bsa_id not in period:
                kind[r.bsa_id] = "older chain"
                last_end = r.activity_end
            elif not r.prior_bsa_id and k == 0:
                kind[r.bsa_id] = "initial"
                last_end = r.activity_end
            elif r.prior_bsa_id and period[r.prior_bsa_id] == (r.activity_start, r.activity_end):
                kind[r.bsa_id] = "correction"
            else:
                kind[r.bsa_id] = "continuing" if r.activity_start > last_end else "unclear"
                last_end = max(last_end, r.activity_end)
    s["kind"] = s["bsa_id"].map(kind)
    s["edate"] = eastern(s["filed"])
    w = s[(s["edate"] >= "2026-01-01") & (s["edate"] < "2026-11-01")]
    check("ask B: every 2026 filing is an initial report, a continuing activity report or a correction",
          set(w["kind"]) <= {"initial", "continuing", "correction"}, sorted(set(w["kind"])))
    w = w[w["kind"] != "correction"]
    w["m"] = w["edate"].dt.strftime("%Y-%m")
    return w.groupby(["m", "kind"]).size().to_dict()


def goldens(fig):
    import openpyxl
    from docx import Document
    wb = openpyxl.load_workbook(os.path.join(G, "tm_alert_figures_2026.xlsx"), data_only=True)
    ws = wb["Investigations by quarter"]
    rows = {r[0]: r[1:] for r in ws.iter_rows(min_row=2, values_only=True)}
    q = ["2025 Q4", "2026 Q1", "2026 Q2", "2026 Q3"]
    ok = all(list(rows[(c + " / XB-HRJ2") if c == "XB-HRJ" else c]) == [fig["ask_investigations"][c][k] for k in q]
             for c in fig["ask_investigations"])
    check("golden workbook: investigations by quarter equal figures.json", ok)
    ws2 = wb["SARs filed 2026"]
    vals = [tuple(r) for r in ws2.iter_rows(min_row=2, values_only=True)]
    ok = [(v[1], v[2]) for v in vals] == [(fig["ask_sars"][m]["initial"], fig["ask_sars"][m]["continuing"])
                                          for m in sorted(fig["ask_sars"])]
    check("golden workbook: SARs by month equal figures.json", ok)
    doc = Document(os.path.join(G, "tuning_scenarios_2027.docx"))
    txt = "\n".join(p.text for p in doc.paragraphs)
    check("golden paper: names every scenario going into the tuning", all(c in txt for c in fig["call"]["tuning"]))
    tab = doc.tables[0]
    yes = sorted(r.cells[0].text for r in tab.rows[1:] if r.cells[5].text == "Yes")
    check("golden paper: the table marks exactly the tuning set", yes == fig["call"]["tuning"], yes)
    with zipfile.ZipFile(os.path.join(G, "tuning_scenarios_2027.docx")) as z:
        check("golden paper: carries its chart", any(n.startswith("word/media/") for n in z.namelist()))


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    D = read()
    floor = filed(D)
    a = alerts_frame(D)
    prod = productivity(a, floor)
    call = sorted(c for c, v in prod.items() if v < floor)
    check("call: the Aalen-Johansen reading files the golden tuning set", call == fig["call"]["tuning"], call)
    check("call: every scenario's productivity within 0.35 points of the generator's",
          all(abs(prod[c] - fig["productivity"][c]) < 0.35 for c in prod),
          {c: round(prod[c] - fig["productivity"][c], 3) for c in prod})
    check("call: each scenario at least half a point from the floor",
          min(abs(v - floor) for v in prod.values()) >= 0.5, min(abs(v - floor) for v in prod.values()))
    dec = {c: 100.0 * int((g["event"] == 1).sum()) / int((g["event"] > 0).sum())
           for c, g in a[(a["bdate"] >= "2025-10-01") & (a["bdate"] <= "2026-09-30")].groupby("scenario")}
    check("ladder R0: the decided-alert reading files the default answer",
          sorted(c for c, v in dec.items() if v < floor) == sorted(fig["call"]["tuning"] + fig["traps"]))
    A_ = ask_a(D, a)
    q = ["2025 Q4", "2026 Q1", "2026 Q2", "2026 Q3"]
    ok = all(A_.get((c, k), 0) == fig["ask_investigations"][c][k] for c in fig["ask_investigations"] for k in q)
    check("ask A: investigations by quarter recompute", ok)
    B_ = ask_b(D)
    ok = all(B_.get((m, k), 0) == fig["ask_sars"][m][k] for m in fig["ask_sars"] for k in ("initial", "continuing"))
    check("ask B: SARs by month recompute", ok)
    goldens(fig)
    print("verify: %d failed" % len(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
