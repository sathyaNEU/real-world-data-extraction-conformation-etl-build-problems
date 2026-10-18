"""The independent verifier: reads only the shipped bundle (pandas for the tables, pdftotext for the documents,
openpyxl for the workbook, python-docx for the brief), on its own code path, and recomputes the call, every candidate's
trips and passengers, the gap and the default path; then compares them with the golden files."""
import csv
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
FAILS = []


def ok(label, cond, detail=""):
    print("%s  verify: %s%s" % ("ok  " if cond else "FAIL", label, ("  [%s]" % detail) if not cond else ""))
    if not cond:
        FAILS.append(label)


def text(path, layout=False):
    args = ["pdftotext", "-layout" if layout else "-raw", path, "-"]
    return subprocess.run(args, capture_output=True, text=True, check=True).stdout


MONTHS = {m: i + 1 for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                          "September", "October", "November", "December"])}


def recompute(target):
    p = lambda f: os.path.join(target, f)
    cards = pd.read_csv(p("brennick_parking_survey_2026_cards.csv"), dtype=str)
    n_raw = len(cards)
    cards = cards.drop_duplicates()
    assert cards["card_no"].is_unique
    zips = pd.read_csv(p("kvr_service_area_zip_codes.csv"), dtype=str)
    sa_zips = set(zips["zip_code"])
    mk = pd.read_csv(p("bureau_city_markets.csv"), dtype=str)
    to_mkt = dict(zip(mk["code"], mk["market_code"]))
    name_of = dict(zip(mk["market_code"], mk["city_market"]))
    verb = pd.read_csv(p("brennick_parking_survey_2026_verbatims.csv"), dtype=str)
    q4 = verb[verb["question"] == "Q4"].set_index("card_no")["as_written"]

    def people(s):
        s = s.strip()
        lead = re.match(r"^([0-9]+)(\s*\(|\s+incl)", s)
        if s.isdigit() or lead:
            return int(re.match(r"^[0-9]+", s).group())
        if s.startswith("me + "):
            return 1 + int(s[5:])
        nums = [int(v) for v in re.findall(r"[0-9]+", s)]
        assert len(nums) == 2 and ("+" in s or "adult" in s), s
        return nums[0] + nums[1]
    # the handout log: one line per day and plaza
    log = text(p("brennick_parking_survey_2026_handout_log.pdf"))
    rows = re.findall(r"^\w{3} (\d+)/(\d+)/(\d{4}) Plaza ([CDL]) (\d{7}) (\d{7}) ([\d,]+)$", log, re.M)
    hl = pd.DataFrame([dict(date=pd.Timestamp(int(y), int(m), int(d)), plaza=pl, first=int(a), last=int(b),
                            n=int(c.replace(",", ""))) for m, d, y, pl, a, b, c in rows])
    hl["wave"] = hl["first"] // 1000000
    hl["day"] = hl.groupby("wave")["date"].transform(lambda s: (s - s.min()).dt.days + 1)
    # the methods report: each wave's last box collection
    meth = re.sub(r"\s+", " ", text(p("brennick_parking_survey_2026_methods_report.pdf")))
    close = {int(w): pd.Timestamp(2026, MONTHS[mo], int(d)) for w, d, mo in
             re.findall(r"\b([1-4]) \d+ \w+ to \d+ \w+ 2026 Night of (\d+) (\w+) 2026", meth)}
    # each card's handout day and weight
    cards["no"] = cards["card_no"].astype(int)
    cards["wave"] = cards["wave"].astype(int)
    cards["nights"] = cards["nights"].astype(int)
    hl_sorted = hl.sort_values("first")
    idx = np.searchsorted(hl_sorted["first"].values, cards["no"].values, side="right") - 1
    cards["day"] = hl_sorted["day"].values[idx]
    cards["plaza"] = hl_sorted["plaza"].values[idx]
    start = hl.groupby("wave")["date"].min()
    cdays = {w: (close[w] - start[w]).days + 1 for w in close}
    per_day = hl.groupby(["wave", "day"])["n"].sum()
    weight = {}
    for w in cdays:
        s = per_day.loc[w]
        for L in range(0, 29):
            weight[(w, L)] = s.sum() / s[s.index <= cdays[w] - L].sum()
    cards["w_collect"] = [weight[(w, L)] for w, L in zip(cards["wave"], cards["nights"])]
    cards["w_raw"] = 1.0
    cards["zip5"] = cards["home_zip"].str.replace(r"\D", "", regex=True).str[:5]
    cards["sa"] = cards["zip5"].isin(sa_zips)
    cards["mkt"] = cards["destination_code"].map(to_mkt)
    cards["people"] = cards["card_no"].map(q4).map(people)
    cards["coded"] = cards["party"].astype(int)
    # the register
    E = {}
    for q in (1, 2, 3, 4):
        r = pd.read_csv(p("brennick_parcs_daily_entries_2026q%d.csv" % q), dtype=str)
        if "Lot" in r:
            E[q] = r.loc[r["Lot"].isin(["ECONOMY C", "ECONOMY D", "LONG TERM"]), "Transient Entries"].astype(int).sum()
        else:
            E[q] = r.loc[r["facility"].isin(["EC", "ED", "LT"]), "transient_entries"].astype(int).sum()
    # the candidates
    sched = text(p("kvr_nonstop_schedule_2027.pdf"))
    served = {to_mkt[a] for a in re.findall(r"\((ORD|MDW|CLT|DTW|SFB|MCO|[A-Z]{3})\)", sched) if a in to_mkt}
    std_raw = text(p("bureau_air_service_pitch_standard_2027.pdf"))
    std = re.sub(r"\s+", " ", std_raw)
    app = std_raw.split("Appendix A. Shortlist")[1]
    shortlist = [m for name, m, aps in re.findall(r"^([A-Z][a-z]+(?: [A-Z][a-z]+)*) ([A-Z]{3}) ([A-Z]{3}(?:, [A-Z]{3})*)$",
                                                     app, re.M)]
    cand = [m for m in shortlist if m not in served]

    def est(wcol, unit=None):
        out = {}
        for w, grp in cards.groupby("wave"):
            S = grp[wcol].sum()
            sa = grp[grp["sa"]]
            v = sa[wcol] * (sa[unit] if unit else 1.0)
            for m, val in v.groupby(sa["mkt"]).sum().items():
                out[m] = out.get(m, 0.0) + E[w] * val / S
        return out
    return dict(cand=cand, trips=est("w_collect"), pax=est("w_collect", "people"), raw=est("w_raw"),
                served=sorted(served), name=name_of, n_raw=n_raw, n=len(cards), std=std, meth=meth,
                cracker=est("w_collect", "coded"))


def r100(v):
    return int(round(v / 100.0)) * 100


def main(target, golden):
    del FAILS[:]
    R = recompute(target)
    C = R["cand"]
    order = sorted(C, key=lambda m: -R["trips"][m])
    ok("14 candidates after the served markets (%s)" % ", ".join(R["served"]), len(C) == 14 and
       R["served"] == ["CHI", "CLT", "DTT", "ORL"], C)
    ok("the three: %s; first left out %s" % (", ".join(order[:3]), order[3]), order[:3] == ["PHX", "TPA", "WAS"] and
       order[3] == "NYC")
    raw3 = sorted(C, key=lambda m: -R["raw"][m])[:3]
    ok("the default path (each wave's replies expanded to its quarter) pitches %s" % ", ".join(raw3),
       raw3 == ["WAS", "NYC", "DFW"])
    with open(os.path.join(golden, "kvr_2027_pitch_markets.csv"), encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    ok("the golden CSV's trips are the recomputed trips, nearest hundred",
       all(int(r["trips_2026"]) == r100(R["trips"][r["market_code"]]) for r in rows) and len(rows) == 14)
    ok("the golden CSV's passengers are the recomputed passengers, nearest hundred",
       all(int(r["passengers_2026"]) == r100(R["pax"][r["market_code"]]) for r in rows))
    ok("the golden CSV's order and marks follow the trips", [r["market_code"] for r in rows] == order and
       [r["market_code"] for r in rows if r["in_2027_pitch"] == "Y"] == order[:3])
    gap = R["trips"][order[2]] - R["trips"][order[3]]
    from docx import Document
    d = Document(os.path.join(golden, "kvr_2027_route_pitch_brief.docx"))
    body = "\n".join(p_.text for p_ in d.paragraphs)
    ok("the brief names the three, the first left out and the gap (%s)" % "{:,}".format(r100(gap)),
       all(R["name"][m] in body for m in order[:4]) and "{:,}".format(r100(gap)) in body)
    ok("the brief's chart is embedded", len(d.inline_shapes) == 1)
    miss = sum(r100(R["cracker"][m]) != r100(R["pax"][m]) for m in C)
    ok("the coded party misses %d of the 14 passengers figures" % miss, miss == 14)
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, "brennick_ground_access_survey_2025.xlsx"), read_only=True)
    ok("the 2025 access workbook opens and reads (its sheets %s)" % wb.sheetnames,
       wb.sheetnames == ["Mode by home area", "Party size", "About"])
    rates = re.sub(r"\s+", " ", text(os.path.join(target, "brennick_public_parking_rates_2026.pdf")))
    for label, doc, s in (("standard 2.1", R["std"], "The short-term garage is not part of the basis."),
                          ("standard 2.2", R["std"], "counted once whatever the size of its party"),
                          ("standard 2.3", R["std"], "service area ZIP list"),
                          ("standard 2.4", R["std"], "Permit holders' entries (employees and tenants) are not trips."),
                          ("standard 2.5", R["std"], "city-market table"),
                          ("standard 2.6", R["std"], "Every such trip counts, not only the trips a survey reached."),
                          ("standard 2.7", R["std"], "counted in full"),
                          ("standard 3.1", R["std"], "seasonal service included, is not a candidate"),
                          ("standard 4.1", R["std"], "the three candidates with the most trips"),
                          ("standard 4.3", R["std"], "reported to the nearest hundred"),
                          ("methods 1.2", R["meth"], "Each wave's 28 days of entries stand for its quarter."),
                          ("methods 3.2", R["meth"], "emptied for the last time on the night of the second day"),
                          ("rates", rates, "limited to 28 consecutive days")):
        ok("%s reads back: %s" % (label, s), s in doc)
    print("verify: %d failures" % len(FAILS))
    return not FAILS


if __name__ == "__main__":
    task = os.path.dirname(HERE)
    good = main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(task, "target"),
                sys.argv[2] if len(sys.argv) > 2 else os.path.join(task, "golden"))
    sys.exit(0 if good else 1)
