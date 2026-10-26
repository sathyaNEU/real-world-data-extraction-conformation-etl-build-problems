"""The generator's assertions on the clean truth and on the cut pack: the input gates, the three rules (R1 to R3c),
the ladder and its margins, every semantic fork row (SF1 to SF14), the separation line, the asks' devices and stops,
the realism sweep and each distractor's deletion test.

    python3 checks.py            # needs target/ and figures.json from build.py
"""
import collections
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as BD      # noqa: E402
import golden as GD     # noqa: E402
import pack as PK       # noqa: E402
import world as WD      # noqa: E402

TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
RESULTS = []


def check(label, cond, detail=""):
    RESULTS.append((label, bool(cond), detail))
    print(("ok    " if cond else "FAIL  ") + label + ("  (" + detail + ")" if detail else ""))


def cell(x, b=250):
    return int(np.floor(x / b + 0.5)) * b


def edge(x, b=250):
    return b / 2 - abs(x - cell(x, b))


def in_one_cell(xs, b=250):
    return len({cell(x, b) for x in xs}) == 1


def text_of(path):
    """Every shipped document's text through one extractor (docx and xlsx parts unzipped, pdf through pypdf)."""
    if path.endswith(".pdf"):
        import pypdf
        return "\n".join(p.extract_text() or "" for p in pypdf.PdfReader(path).pages)
    if path.endswith((".docx", ".xlsx")):
        with zipfile.ZipFile(path) as z:
            return "\n".join(re.sub(r"<[^>]+>", " ", z.read(n).decode("utf-8", "replace")) for n in z.namelist()
                             if n.endswith(".xml"))
    return open(path, encoding="utf-8", errors="replace").read()


def main():
    T = BD.make_world()
    W, C, rows, files, hc, close = T["W"], T["C"], T["rows"], T["files"], T["hc"], T["close"]
    R = GD.figures(TGT)
    M, A, B = R["M"], R["A"], R["B"]
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    names = sorted(os.listdir(TGT))
    a, p, lk, al = GD.load(TGT)

    # ---------------------------------------------------------------- input gates
    check("G1 ten or more files", len(names) >= 10, "%d files" % len(names))
    check("G2 three or more formats", len({os.path.splitext(n)[1] for n in names}) >= 3,
          ", ".join(sorted({os.path.splitext(n)[1] for n in names})))
    check("G3 a file of 25,000 rows or more", len(a) >= 25000 and len(p) >= 25000, "%d arrests, %d crimes" % (len(a), len(p)))
    dis = [os.path.basename(x) for x in meta["distractor_files"]]
    check("G4 two or more distractors, each shipped", len(dis) >= 2 and all(d in names for d in dis), ", ".join(dis))
    check("G5 no file name names a distractor or the stump",
          not any(re.search(r"distract|btp|transport|missing|hidden|known_issue", n, re.I) for n in names))
    check("G6 every mtime is the fiction's", all(os.path.getmtime(os.path.join(TGT, n)) <
                                                 dt.datetime(2026, 10, 21).timestamp() for n in names))

    # ---------------------------------------------------------------- R1: the field's raw material ships
    check("R1a the call reads row-level records: arrests and BTP's own crime rows",
          M["own_2025"] == int((a[a.ward.isin(M["hub"])].fy == 2025).sum()) and M["btp_hub_crimes"] > 1000)
    heads = " ".join(open(os.path.join(TGT, n), encoding="utf-8").readline().lower() for n in names if n.endswith(".csv"))
    check("R1b no shipped column holds the deciding quantity",
          not re.search(r"btp_arrest|detentions_2027|demand_2027|planning", heads))
    # ---------------------------------------------------------------- R2: every mess item neutral on the call
    hub = M["hub"]
    ah = a[a.ward.isin(hub)].copy()
    t_utc = pd.to_datetime(ah.arrested_utc, utc=True)
    ah["fy_utc"] = np.where(t_utc.dt.month >= 4, t_utc.dt.year, t_utc.dt.year - 1)
    byw_utc = ah.groupby(["ward", "fy_utc"]).size().unstack(fill_value=0)
    f1_utc = GD.model(byw_utc, 2025, 2)
    check("R2a UTC financial years instead of UK time: same call", cell(f1_utc + M["B"]["B2 per-type rates with the warrant share"]) == M["golden"],
          "%.1f" % f1_utc)
    booked = a[a.custody_suite.isin(["Northgate", "Eastmoor"]) & a.ward.isin(hub)]
    byw_bk = booked.groupby(["ward", "fy"]).size().unstack(fill_value=0)
    check("R2b counting the wards' arrests booked at their own suites only: same call",
          cell(GD.model(byw_bk, 2025, 2) + M["B"]["B2 per-type rates with the warrant share"]) == M["golden"])
    near = ah.drop_duplicates(["arrested_utc", "ward", "offence_group", "age_band", "sex"]).groupby(["ward", "fy"]).size().unstack(fill_value=0)
    check("R2c co-arrests that look alike (same minute, ward, offence, age band and sex) dropped as duplicates: same call",
          cell(GD.model(near, 2025, 2) + M["B"]["B2 per-type rates with the warrant share"]) == M["golden"],
          "%d dropped" % (len(ah) - len(ah.drop_duplicates(["arrested_utc", "ward", "offence_group", "age_band", "sex"]))))
    one = ah.drop_duplicates(["arrested_utc", "ward", "offence_group"]).groupby(["ward", "fy"]).size().unstack(fill_value=0)
    check("R2d warrants left out of BTP's sizing: same call", cell(M["G"]["F1 + B1"]) == M["golden"])
    check("R2e the April to September 2026 rows: the model reads full years, the last twelve months print the same",
          cell(M["G"]["F6 + B2"]) == M["golden"])
    pl = p.merge(lk[["lsoa21_code", "ward"]], left_on="LSOA code", right_on="lsoa21_code", how="left")
    check("R2f every street-level row has a ward through the lookup", pl.ward.notna().all())
    check("R2g the closures and overflow move no arrest between wards", len(a) == sum(len(x) for x in [a]) and
          a.ward.isin(WD.WARDS).all())
    # ---------------------------------------------------------------- R3: the analyst test on the clean truth
    clean = WD.routes_agg(W, C)
    check("R3a the default path on the clean truth files the wrong answer (every frame member at 3,750)",
          in_one_cell(clean["F"].values()) and cell(clean["F"]["F1"]) == M["default"],
          "%.1f to %.1f" % (min(clean["F"].values()), max(clean["F"].values())))
    check("R3a' the default path on the pack files 3,750 too", in_one_cell(M["F"].values()) and M["default"] == 3750)
    check("R3b the decisive step alone files the golden; the share-scaling correction does not",
          cell(clean["F"]["F1"] + clean["B"]["B2"]) == M["golden"] and cell(clean["R"]["R1"]) == M["default"]
          and cell(M["R"]["R1 scaled by BTP's share of the street-level file"]) == M["default"])
    check("R3b' the world's expected 2027-28 detentions sit in the golden's cell", cell(clean["truth"]["total"]) == M["golden"],
          "%.1f" % clean["truth"]["total"])
    docs_text = {n: text_of(os.path.join(TGT, n)) for n in names if n.endswith((".docx", ".pdf", ".xlsx"))}
    check("R3c no document states a figure for the hub or argues for one",
          not any(re.search(r"\b(3,?750|4,?000|3,?754|4,?036)\b", t) for t in docs_text.values()))
    dup = a.duplicated(["custody_suite", "booked_in_utc", "ward", "offence_group", "age_band", "sex", "detention_hhmm"]).sum()
    check("R3c' no copied block of arrests (identical rows beyond co-arrest coincidence)", dup <= 3, "%d" % dup)

    # ---------------------------------------------------------------- the ladder and its margins
    fr, go = list(M["F"].values()), list(M["G"].values())
    check("L1 every frame member prints 3,750 with 30 or more to spare", in_one_cell(fr) and min(edge(x) for x in fr) >= 30,
          "%.1f" % min(edge(x) for x in fr))
    check("L2 every golden-family member prints 4,000 with 30 or more to spare", in_one_cell(go) and cell(go[0]) == M["golden"]
          and min(edge(x) for x in go) >= 30, "%.1f" % min(edge(x) for x in go))
    check("L3 the share-scaled rung stays on 3,750", cell(M["R"]["R1 scaled by BTP's share of the street-level file"]) == 3750)
    check("L4 the golden sits clear of its edge", edge(M["golden_raw"]) >= 50, "%.1f" % edge(M["golden_raw"]))
    val = BD.validation_rows(rows)
    check("L5 the model's back-test holds within 4 per cent at every suite", all(0.96 <= v[3] <= 1.04 for v in val),
          ", ".join("%s %.3f" % (v[0], v[3]) for v in val))
    check("L6 the cap binds no hub ward (the model with and without it agree)",
          abs(M["F"]["F1 the model as filed"] - M["F"]["F7 the model without its cap"]) < 1e-9)

    # ---------------------------------------------------------------- semantic fork table
    check("SF1 the hub's detentions are everyone booked there: the force's arrests alone print 3,750, not the golden",
          M["default"] != M["golden"])
    check("SF2 2027-28 is 1 April 2027 to 31 March 2028: the model carries 2025-26 two years",
          abs(M["F"]["F1 the model as filed"] - GD.model(ah.groupby(["ward", "fy"]).size().unstack(fill_value=0), 2025, 2)) < 1e-9)
    check("SF3 the six wards are the allocation's Tanner Street rows",
          sorted(hub) == sorted(WD.HUB))
    check("SF4 financial years by the UK date of arrest (model 2.2); UTC dating gives the same call", True if cell(f1_utc + M["B"]["B2 per-type rates with the warrant share"]) == M["golden"] else False)
    f1_one = GD.model(ah.groupby(["ward", "fy"]).size().unstack(fill_value=0), 2025, 1)
    check("SF5 one year ahead instead of two: same call", cell(f1_one + M["B"]["B2 per-type rates with the warrant share"]) == M["golden"],
          "%.1f" % f1_one)
    check("SF6 the cap does not bind (same call with or without it)", cell(M["G"]["F1 + B2"]) == M["golden"])
    check("SF7 the nearest 250", M["golden"] % 250 == 0)
    check("SF8 BTP's 2025-26 crimes are the street-level file's year", sorted(p.Month.unique())[0] == "2025-04" and
          sorted(p.Month.unique())[-1] == "2026-03")
    st = M["btp_hub_by_station"]
    check("SF9 BTP's crimes in the six wards are the two stations' (lookup best fit)",
          set(s.replace("On or near ", "").replace(" (station)", "") for s in st) == {"Calderwick", "Kingsway"})
    check("SF10 the BTP sizing family (per type, overall, hub rate, with or without warrants) prints the golden",
          all(cell(M["F"]["F1 the model as filed"] + v) == M["golden"] for v in M["B"].values()))
    check("SF11 every BTP crime in the force area at the overall rate (the over-reach) still prints the golden, but the county "
          "stations' detainees go to Southfields and Wendle Cross (allocation note 2)",
          cell(M["R"]["R2 every BTP crime in the force area at the overall rate"]) == M["golden"])
    check("SF12 a detention is a person booked in: collapsing each incident to one arrest is the wrong unit, ruled out by "
          "'one row per arrest' (it prints 3,750)",
          cell(GD.model(one, 2025, 2) + M["B"]["B2 per-type rates with the warrant share"]) == M["default"])
    check("SF13 the force's own 2025-26 rates from its whole area, not the six wards' (B4 the six wards' rate): same call",
          cell(M["G"]["F1 + B4"]) == M["golden"])
    check("SF14 warrant, recall or breach arrests counted in the model (the records hold them): same call either way",
          cell(GD.model(ah[ah.offence_group != GD.WARRANT].groupby(["ward", "fy"]).size().unstack(fill_value=0), 2025, 2) / (1 - 0.05)
               + M["B"]["B2 per-type rates with the warrant share"]) == M["golden"])

    # ---------------------------------------------------------------- separation: no ask device moves the call
    with tempfile.TemporaryDirectory() as td:
        for n in names:
            if n not in (BD.F_CJU, BD.F_HC):
                os.symlink(os.path.join(TGT, n), os.path.join(td, n))
        a2, p2, lk2, al2 = GD.load(td)
        M2 = GD.main_call(a2, p2, lk2, al2)
    check("S1 the call recomputes without the remand and healthcare files", M2["golden_raw"] == M["golden_raw"])
    check("S2 no ask device row is in the call's population: the CJU and healthcare files carry no arrest row of their own",
          set(pd.read_csv(os.path.join(TGT, BD.F_CJU)).linked_arrest) <= set(a.arrest_ref))
    check("S3 the closures move bookings, never wards: the six wards' counts are the same by ward or by any suite",
          int((a.ward.isin(hub) & (a.fy == 2025)).sum()) == M["own_2025"])

    # ---------------------------------------------------------------- ask A: remand holds
    c, d, orphans = GD.remand_defendants(a, TGT)
    d25 = d[d.fy == 2025]
    truth = collections.defaultdict(lambda: [0.0, 0])
    for r in rows:
        if r["out"] != "Charged - remanded in custody" or "handover" not in r:
            continue
        ch = PK.charge_utc(r)
        if PK.fy_local(PK.to_local(ch)) != 2025:
            continue
        hand = PK.to_utc(r["handover"])
        truth[r["suite"]][0] += (hand - ch).total_seconds() / 3600
        truth[r["suite"]][1] += (hand - PK.to_utc(r["t_book"])).total_seconds() > 24 * 3600
    check("A1 ask A's golden reproduces the generator's truth at every suite",
          all(round(truth[s][0]) == A[s]["cell_hours"] and truth[s][1] == A[s]["over_24"] for s in GD.SUITES))
    check("A2 every remanded arrest charged in the extract's window belongs to exactly one file", R["A_info"]["orphans_in_window"] == 0
          and d.ref.is_unique)
    check("A3 every file links an arrest the records hold, and a file keyed to a first arrest links an earlier release in "
          "the same ward and offence group",
          all(x.linked_book < x.book for x in d[d.rearrest & d.lead].itertuples()) and (d.rearrest & d.lead).sum() > 50)
    hrs = (d25.hand - d25.book).dt.total_seconds() / 60
    check("A4 no hold within a minute of 24 hours", int(((hrs - 1440).abs() <= 1).sum()) == 0)
    ed = {s: 0.5 - abs(A[s]["cell_hours_raw"] - round(A[s]["cell_hours_raw"])) for s in GD.SUITES}
    check("A5 every cell-hours figure 0.1 hours or more from its rounding edge", min(ed.values()) >= 0.1,
          ", ".join("%s %.2f" % kv for kv in ed.items()))
    amb = 0
    for col in ("charged", "handed_to_escort"):
        for s_ in c[col]:
            t = dt.datetime.strptime(s_, "%d/%m/%Y %H:%M")
            if (t.replace(tzinfo=PK.UK, fold=0).utcoffset() != t.replace(tzinfo=PK.UK, fold=1).utcoffset() or
                    PK.to_local(PK.to_utc(t)) != t):
                amb += 1
    check("A6 no remand file time in the hour the clocks repeat or skip", amb == 0, "%d" % amb)
    stops_a = R["A_stops"]
    for k in ("each file's linked arrest", "files with co-defendants at the file's charge time",
              "the case's own detentions, co-defendants left out", "every file in the extract"):
        check("A7 stop '%s' misses all eight figures" % k,
              all(stops_a[k][s]["cell_hours"] != A[s]["cell_hours"] and stops_a[k][s]["over_24"] != A[s]["over_24"]
                  for s in GD.SUITES))
    for k in ("co-defendants on their own clocks, linked arrest's booking", "detention clock for the 24 hours"):
        check("A8 stop '%s' misses all four over-24 counts" % k,
              all(stops_a[k][s]["over_24"] != A[s]["over_24"] for s in GD.SUITES))
    check("A9 the remand file read as UTC misses all four cell-hours figures",
          all(stops_a["remand file times read as UTC"][s]["cell_hours"] != A[s]["cell_hours"] for s in GD.SUITES))
    check("A10 every suite carries co-defendants and files keyed to a first arrest",
          all(A[s]["codefendants"] >= 5 and A[s]["rearrests"] >= 5 for s in GD.SUITES))

    # ---------------------------------------------------------------- ask B: initial health assessments
    tb = collections.Counter()
    for r in hc:
        if r["kind"] == "Initial health assessment" and r["part"] != 2:
            tb[(r["place"], "day" if 7 <= r["start"].hour < 19 else "night")] += 1
    check("B1 ask B's golden reproduces the generator's truth (place and assessment) in all eight cells",
          all(tb[(s, k)] == B[s][k] for s in GD.SUITES for k in GD.SHIFTS))
    cl = GD.closures(a, al)
    check("B2 the arrest records show exactly the two closures, at the generator's moves",
          sorted(cl) == ["Eastmoor", "Wendle Cross"] and all(cl[s]["last"] + dt.timedelta(minutes=1) == close[s] for s in cl)
          and all(cl[s]["host"] == PK.CLOSURES[s][2] for s in cl))
    edge_lines = [r for r in hc if r["team"] in cl and (cl[r["team"]]["last"] <= r["start"] < close[r["team"]] or
                                                         PK.CLOSURES[r["team"]][1] <= r["start"] < cl[r["team"]]["first"])]
    check("B3 no closed suite's line starts between its last booking and the move, or between its reopening and its first "
          "booking", not edge_lines, "%d" % len(edge_lines))
    pre = [r for r in hc if r["kind"] == "Initial health assessment" and r["booked"] in cl and r["place"] != r["booked"]
           and r["t_book"] <= cl[r["booked"]]["last"]]
    check("B4 no assessment of a detainee booked before a closure falls after it (pre-closure episodes read either way: C1)",
          not pre, "%d" % len(pre))
    ih = [r for r in hc if r["kind"] == "Initial health assessment"]
    check("B5 every continuation starts at 07:00 or 19:00 on its predecessor's end; no repeat after the emergency "
          "department does", all(r["start"].minute == 0 and r["start"].hour in (7, 19) for r in ih if r["part"] == 2)
          and R["B_info"]["continuations"] == sum(1 for r in ih if r["part"] == 2))
    stops_b = R["B_stops"]
    for k in ("every line by its suite", "handover lines joined, suite as labelled", "closures moved, handover lines kept",
              "one assessment an episode, closures moved", "one assessment an episode, suite as labelled"):
        check("B6 stop '%s' misses all eight figures" % k,
              all(stops_b[k][s][x] != B[s][x] for s in GD.SUITES for x in GD.SHIFTS))
    check("B7 finding one closure only keeps at most half the figures",
          sum(stops_b["only the Wendle Cross refit moved"][s][x] == B[s][x] for s in GD.SUITES for x in GD.SHIFTS) <= 4 and
          sum(stops_b["only the Eastmoor closure moved"][s][x] == B[s][x] for s in GD.SUITES for x in GD.SHIFTS) <= 4)

    # ---------------------------------------------------------------- realism sweep
    yrs = [M["fy_hub"][y] for y in sorted(M["fy_hub"])]
    check("X1 no repeated yearly totals in the six wards", len(set(yrs)) == len(yrs), str(yrs))
    check("X2 no round headline components", all(v % 50 for v in (M["own_2025"], M["btp_hub_crimes"])) and
          all(A[s]["cell_hours"] % 100 for s in GD.SUITES) and all(B[s][k] % 100 for s in GD.SUITES for k in GD.SHIFTS))
    wm = a[a.fy == 2025].groupby(["ward", "ym"]).size()
    check("X3 no ward with the same count every month", (wm.groupby(level=0).nunique() > 1).all())
    card = json.load(open(os.path.join(os.path.dirname(TASK), ".claude", "skills", "fingerprint", "cards", "task137.json")))
    named = set()
    for n in names:
        if n.endswith((".docx", ".xlsx")):
            core = zipfile.ZipFile(os.path.join(TGT, n)).read("docProps/core.xml").decode()
            named |= set(re.findall(r"<dc:creator>([^<]+)</dc:creator>", core))
            named |= set(re.findall(r"<cp:lastModifiedBy>([^<]+)</cp:lastModifiedBy>", core))
        named |= set(re.findall(r"(?:To|From): ([A-Z][a-z]+ [A-Z][a-z]+)", docs_text.get(n, "")))
    people = {x for x in named if re.fullmatch(r"[A-Z][a-z]+ [A-Z][a-z]+", x)} - {"Custody Services"}
    check("X4 every person named in the pack is on the card", bool(people) and people <= set(card["world"]["people"]),
          ", ".join(sorted(people)))
    toolchain = [n for n, t in docs_text.items() if re.search(r"openpyxl|python-docx|ReportLab|reportlab|matplotlib", t)]
    check("X5 no container names the library that wrote it", not toolchain, ", ".join(toolchain))
    last_arrest = pd.to_datetime(a.arrested_utc, utc=True).max()
    check("X6 every record is before its file's pull", last_arrest < pd.Timestamp("2026-10-01", tz="UTC") and
          pd.to_datetime(pd.read_csv(os.path.join(TGT, BD.F_HC)).started).max() < pd.Timestamp("2026-04-01"))
    dash = [n for n in names if re.search("[\\u2013\\u2014]", text_of(os.path.join(TGT, n)))]
    check("X7 no em or en dash in any shipped file", not dash, ", ".join(dash))
    check("X8 the custody fact is filed once, in the allocation notes, and no document names the railway force",
          sum("whichever force or agency" in t for t in docs_text.values()) == 1 and
          not any("British Transport" in t or "BTP" in t for t in docs_text.values()))
    check("X9 positive controls: the extractor reads each document", all(len(t) > 400 for t in docs_text.values()) and
          "capped at 10 per cent" in docs_text[BD.F_MODEL].replace("\n", " ") and "opens on 1 April 2027" in docs_text[BD.F_BRIEF])

    brief_files = set(re.findall(r"[\w.-]+\.(?:csv|xlsx|pdf|json|docx)", docs_text[BD.F_BRIEF]))
    check("X10 the brief's file notes name every other shipped file and nothing else (H9)",
          brief_files == set(names) - {BD.F_BRIEF}, ", ".join(sorted(brief_files ^ (set(names) - {BD.F_BRIEF}))))
    inc_n = ah.groupby(["arrested_utc", "ward", "offence_group"]).size()
    homes = dict(zip(al.ward, al.suite_to_31_march_2027))
    pl_h = pl[pl.ward.isin(hub)]
    check("X11 the design note's figures: 12.2 per cent of the six wards' arrests in incidents of two or more, 2,780 "
          "bookings away from the ward's suite, BTP 1.28 per cent of the area's crime and one crime in fourteen in the six "
          "wards", round(inc_n[inc_n > 1].sum() / len(ah), 3) == 0.122 and int((a.custody_suite != a.ward.map(homes)).sum()) == 2780
          and round(100 * M["share"], 2) == 1.28 and round(len(pl_h) / (pl_h["Reported by"] == "British Transport Police").sum()) == 14)

    # ---------------------------------------------------------------- distractors: each deleted, nothing moves
    for dname in dis:
        with tempfile.TemporaryDirectory() as td:
            for n in names:
                if n != dname:
                    os.symlink(os.path.join(TGT, n), os.path.join(td, n))
            R2 = GD.figures(td)
        check("D1 deleting %s moves no figure" % dname, GD.flat(R2) == GD.flat(R))

    # ---------------------------------------------------------------- figures.json is the golden
    check("F1 figures.json carries the call and every ask figure", fig == GD.flat(R) and len(fig) >= 30, "%d keys" % len(fig))

    bad = [r for r in RESULTS if not r[1]]
    print("%d assertions, %d failed" % (len(RESULTS), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
