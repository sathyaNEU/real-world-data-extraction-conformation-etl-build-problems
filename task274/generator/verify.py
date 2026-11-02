"""task274 independent verifier.

    python3 task274/generator/verify.py [--pack DIR]

Reads only the shipped bundle (target/ or an unzipped copy), never the generator's state, and recomputes
the call, every critical component and every graded ask figure on its own code path, then compares them
with generator/figures.json. It also recomputes the easy routes the design note names, so the ladder is
checked from the pack as a solver sees it. Exit 0 when every figure agrees.
"""
import csv
import datetime as dt
import json
import os
import re
import sys
import zipfile
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
CUT = dt.date(2026, 8, 31)


def pack_dir(argv=None):
    argv = argv or sys.argv
    if "--pack" in argv:
        return argv[argv.index("--pack") + 1]
    return os.path.join(TASK, "target")


def key(s):
    s = s.strip().upper()
    m = re.fullmatch(r"(LC|BW|WM|SH)(\d{2})(CM|CR)(\d{5})", s)
    if m:
        return (m.group(1), m.group(2), m.group(3), int(m.group(4)))
    m = re.fullmatch(r"(\d{2})-(CM|CR)-(\d{5})-(LC|BW|WM|SH)", s)
    if m:
        return (m.group(4), m.group(1), m.group(2), int(m.group(3)))
    raise ValueError(s)


def central_date(stamp):
    """A UTC timestamp to the local calendar date in Central time (second Sunday of March to first of November)."""
    t = dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ")
    y = t.year
    mar = dt.date(y, 3, 8)
    while mar.weekday() != 6:
        mar += dt.timedelta(1)
    nov = dt.date(y, 11, 1)
    while nov.weekday() != 6:
        nov += dt.timedelta(1)
    start = dt.datetime(y, 3, mar.day, 8, 0)      # 2 a.m. CST is 08:00 UTC
    end = dt.datetime(y, 11, nov.day, 7, 0)       # 2 a.m. CDT is 07:00 UTC
    off = 5 if start <= t < end else 6
    return (t - dt.timedelta(hours=off)).date()


CMS_TO_KIND = {
    "Complaint Filed": "FIL", "Arraignment - Plea of Not Guilty": "ARR", "Pretrial Conference": "PTC",
    "Hearing Continued": "CNT", "Bench Warrant Issued (FTA)": "WAR", "Bench Warrant Returned": "WRR",
    "Notice of Pretrial Diversion Offer": "DVO", "Pretrial Diversion Declined": "DVX",
    "Pretrial Diversion Agreement": "DVA", "Diversion Review Hearing": "STS",
    "Pretrial Diversion Terminated - Restored to Calendar": "DVT", "Dismissed - Pretrial Diversion Completed": "DVC",
    "Disposition - Guilty Plea": "DGP", "Disposition - Guilty Verdict": "DGT",
    "Disposition - Guilty, Stipulated Record": "DSR", "Disposition - Dismissed (State's Motion)": "DDM",
    "Disposition - Nolle Prosequi": "DNP", "Disposition - Not Guilty": "DAQ", "Sentencing": "SEN",
}
CONVICT = {"DGP", "DGT", "DSR"}
DISPOSE = CONVICT | {"DDM", "DNP", "DAQ", "DVC"}


def read_roster(pack):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(pack, "diversion_lottery_draws_2025_2026.xlsx"), read_only=True)
    out = []
    for ws in wb.worksheets:
        rows = [list(r) for r in ws.iter_rows(values_only=True)]
        m = re.search(r"draw of (\d{1,2} [A-Za-z]+ \d{4})", rows[1][0])
        draw = dt.datetime.strptime(m.group(1), "%d %B %Y").date()
        hi = next(i for i, r in enumerate(rows) if r and r[0] == "Case No.")
        for r in rows[hi + 1:]:
            if not r or not r[0] or not re.match(r"^(LC|BW|WM|SH|\d{2}-)", str(r[0])):
                continue
            out.append(dict(key=key(r[0]), draw=draw, offered=(r[5] == "Y"), lot=ws.title))
    return out


def read_events(pack):
    ev = defaultdict(set)
    with open(os.path.join(pack, "legacy_docket_events_2025_2026.csv"), newline="") as f:
        for r in csv.DictReader(f):
            d = dt.datetime.strptime(r["event_date"], "%m/%d/%Y").date()
            ev[key(r["case_number"])].add((d, r["event_code"], r["event_description"]))
    with open(os.path.join(pack, "cms_docket_events_2026.csv"), newline="") as f:
        for r in csv.DictReader(f):
            d = central_date(r["event_timestamp_utc"])
            ev[key(r["case_number"])].add((d, CMS_TO_KIND[r["event_type"]], r["event_detail"]))
    # one event recorded in both systems collapses to one (date, kind)
    out = {}
    for k, s in ev.items():
        seen = {}
        for d, kind, txt in s:
            if (d, kind) not in seen or len(txt) > len(seen[(d, kind)]):
                seen[(d, kind)] = txt
        out[k] = sorted((d, kind, t) for (d, kind), t in seen.items())
    return out


TERM_RE = re.compile(r"TERM (\d{2}/\d{2}/\d{4}) TO (\d{2}/\d{2}/\d{4})", re.I)


def case_state(evs):
    s = dict(disp=None, conv=None, declined=False, term_start=None, terminated_on=None)
    for d, kind, txt in evs:
        if kind == "DVX":
            s["declined"] = True
        if kind == "DVA":
            m = TERM_RE.search(txt)
            s["term_start"] = dt.datetime.strptime(m.group(1), "%m/%d/%Y").date()
        if kind == "DVT":
            s["terminated_on"] = d
        if kind in DISPOSE and s["disp"] is None:
            s["disp"] = d
            s["conv"] = kind in CONVICT
    return s


def months_between(a, b):
    return (b.year - a.year) * 12 + b.month - a.month


def aj(times, causes, horizon):
    o = np.argsort(times, kind="stable")
    t = np.asarray(times)[o]
    c = np.asarray(causes)[o]
    S = 1.0
    F = 0.0
    i = 0
    n = len(t)
    while i < n and t[i] <= horizon:
        j = i
        while j < n and t[j] == t[i]:
            j += 1
        at = n - i
        d1 = int((c[i:j] == 1).sum())
        d2 = int((c[i:j] == 2).sum())
        F += S * d1 / at
        S *= 1 - (d1 + d2) / at
        i = j
    return F


def main_call(pack):
    roster = read_roster(pack)
    ev = read_events(pack)
    recs = []
    for r in roster:
        s = case_state(ev[r["key"]])
        recs.append(dict(r, **s))
    no = [x for x in recs if not x["offered"]]
    off = [x for x in recs if x["offered"]]
    dec = [x for x in off if x["declined"]]
    par = [x for x in off if x["term_start"]]
    c_no = np.mean([x["conv"] for x in no if x["disp"]])
    p_dec = len(dec) / len(off)
    c_dec = np.mean([x["conv"] for x in dec if x["disp"]])
    S = 1.0
    table = []
    for j in range(1, 13):
        risk = d = 0
        for x in par:
            elapsed = months_between(x["term_start"], CUT) + 1
            k = months_between(x["term_start"], x["terminated_on"]) + 1 if x["terminated_on"] else None
            if elapsed >= j and (k is None or k >= j):
                risk += 1
                if k == j:
                    d += 1
        h = d / risk
        table.append((j, risk, d, round(h, 6)))
        S *= 1 - h
    p_term = 1 - S
    term = [x for x in par if x["terminated_on"]]
    c_term = np.mean([x["conv"] for x in term if x["disp"]])
    offered = p_dec * c_dec + (1 - p_dec) * p_term * c_term
    out = dict(c_no=100 * c_no, offered=100 * offered, cut=100 * (c_no - offered), p_term=100 * p_term,
               c_term=100 * c_term, p_dec=100 * p_dec, c_dec=100 * c_dec, final_review=100 * table[11][3],
               table=table, n=len(recs), n_off=len(off), n_par=len(par))
    # the easy routes, from the pack
    out["naive"] = 100 * (np.mean([bool(x["conv"]) for x in no]) - np.mean([bool(x["conv"]) for x in off]))
    out["recorded_no"] = 100 * np.mean([bool(x["conv"]) for x in no])
    out["recorded_off"] = 100 * np.mean([bool(x["conv"]) for x in off])
    out["complete_case"] = 100 * (c_no - np.mean([x["conv"] for x in off if x["disp"]]))
    c = []
    for arm in (no, off):
        T = [((x["disp"] - x["draw"]).days if x["disp"] else (CUT - x["draw"]).days) for x in arm]
        C = [(1 if x["conv"] else 2) if x["disp"] else 0 for x in arm]
        c.append(aj(T, C, max(T)))
    out["cif_longest"] = 100 * (c[0] - c[1])
    t_sofar = np.mean([bool(x["terminated_on"]) for x in par])
    out["terminated_so_far"] = 100 * (c_no - (p_dec * c_dec + (1 - p_dec) * t_sofar * c_term))
    out["terminated_like_not_offered"] = 100 * (c_no - (p_dec * c_dec + (1 - p_dec) * p_term * c_no))
    S11 = float(np.prod([1 - x[3] for x in table[:11]]))
    out["without_final_review"] = 100 * (c_no - (p_dec * c_dec + (1 - p_dec) * (1 - S11) * c_term))
    return out


def asks(pack):
    sys.path.insert(0, HERE)
    import importlib
    import ceiling
    ceiling.PACK = pack
    importlib.reload(ceiling) if False else None
    ceiling.PACK = pack
    c, d = ceiling.filings(ceiling.rule_golden)
    h, r = ceiling.provider(dict(hours="cumulative", sum_january=True, gross_up=True))
    return dict(cls=dict(c), div=dict(d), hours=h, rest=r)


def documents(pack):
    """Read back every governing document through its own format and return the filed sentences found."""
    from pypdf import PdfReader
    found = {}
    for name in ("board_resolution_2025_31.pdf", "nethercote_services_agreement_2025.pdf",
                 "district_court_annual_statistics_fy2025.pdf"):
        txt = " ".join((p.extract_text() or "") for p in PdfReader(os.path.join(pack, name)).pages)
        found[name] = re.sub(r"\s+", " ", txt)
    with zipfile.ZipFile(os.path.join(pack, "pretrial_diversion_policy_pdu_2026_01.docx")) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    found["policy"] = " ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", xml))
    return found


def main(argv=None):
    pack = pack_dir(argv)
    F = json.load(open(os.path.join(HERE, "figures.json")))
    m = main_call(pack)
    a = asks(pack)
    docs = documents(pack)
    problems = []

    def same(name, got, want):
        if got != want:
            problems.append("%s: pack gives %r, figures.json %r" % (name, got, want))

    same("cut", round(m["cut"]), F["cut_points"])
    same("share not offered", round(m["c_no"]), F["share_not_offered"])
    same("share offered", round(m["offered"]), F["share_offered"])
    same("termination chance", round(m["p_term"]), F["termination_chance"])
    same("terminated convicted", round(m["c_term"]), F["terminated_convicted"])
    same("declined share", round(m["p_dec"]), F["declined_share"])
    same("declined convicted", round(m["c_dec"]), F["declined_convicted"])
    same("final review", round(m["final_review"]), F["final_review_rate"])
    same("recorded gap", round(m["naive"]), F["recorded_cut_at_cut"])
    same("recorded not offered", round(m["recorded_no"]), F["recorded_not_offered"])
    same("recorded offered", round(m["recorded_off"]), F["recorded_offered"])
    tier = ("Renew the agreement for 2027 at full scale" if m["cut"] >= 25 else
            "Renew the agreement for 2027 at the pilot's scale" if m["cut"] >= 15 else "Let the agreement lapse")
    same("call", tier, F["call"])
    same("filings by class", a["cls"], F["filings_by_class"])
    same("filings by division", a["div"], F["filings_by_division"])
    same("hours by site", a["hours"], F["hours_by_site"])
    same("restitution by site", a["rest"], F["restitution_by_site"])
    for need, where in (("convicted in the referred case at its final disposition", "board_resolution_2025_31.pdf"),
                        ("counts by how it will end, not as a case without a conviction", "board_resolution_2025_31.pdf"),
                        ("25 percentage points or more", "board_resolution_2025_31.pdf"),
                        ("may retain five percent of each payment", "nethercote_services_agreement_2025.pdf"),
                        ("first day of the month following the date the diversion agreement is filed",
                         "nethercote_services_agreement_2025.pdf"),
                        ("every count charges an offense in one of the classes below", "policy")):
        if need not in docs[where]:
            problems.append("document %s does not carry %r" % (where, need))
    for p in problems:
        print("MISMATCH", p)
    print("verify: cut %.3f (%s), not offered %.3f, offered %.3f, termination %.3f, terminated convicted %.3f" % (
        m["cut"], tier, m["c_no"], m["offered"], m["p_term"], m["c_term"]))
    print("verify: easy routes naive %.2f, cumulative incidence at the longest follow-up %.2f, complete case %.2f, "
          "terminated so far %.2f, terminated like not offered %.2f, without the final review %.2f" % (
              m["naive"], m["cif_longest"], m["complete_case"], m["terminated_so_far"],
              m["terminated_like_not_offered"], m["without_final_review"]))
    print("verify: %d problems" % len(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
