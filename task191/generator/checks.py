"""Assertions on the cut pack and the clean world: the three rules, the call and every rung of the ladder, the fork
rows, the history window held at every defensible value, the asks' devices and their separation from the call, the
documents, the realism sweep and the input gates.

    python3 task191/generator/checks.py
"""
import csv
import datetime as dt
import json
import os
import re
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402
import common as C     # noqa: E402
import pack as Pk      # noqa: E402
import world as Wd     # noqa: E402

GOLD = ["CRY-OFF", "CSH-VEL", "DRM-REA", "PRF-DEV"]
TRAPS = ["MER-RND", "MUL-INF", "RMF-P2P"]
DEFAULT = sorted(GOLD + TRAPS)
Q = ["2025 Q4", "2026 Q1", "2026 Q2", "2026 Q3"]
M = ["2026-%02d" % m for m in range(1, 11)]
FAILS = []
N = [0]


def check(label, ok, detail=""):
    N[0] += 1
    print(("PASS  " if ok else "FAIL  ") + label + ("" if ok else "   " + str(detail)))
    if not ok:
        FAILS.append(label)


# ------------------------------------------------------------------ the clean truth (the world before any record)
def clean_year(W):
    """The tuning year's alerts in the clean world: no re-run copies, every alert under its own scenario and business
    date, its state on the extract read from the world's own clocks."""
    X = C.EXTRACT_UTC
    case = {c["case_id"]: c for c in W["cases"]}
    out = {c: [] for c in C.CODES}
    hist = {c: [] for c in C.CODES}
    for a in W["alerts"]:
        if a["dup"] or a["bdate"] < C.DATA0:
            continue
        if a["triage"] == "NSA":
            dec = a["triage_end"]
        else:
            dec = case[a["case"]]["decided"]
        done = dec <= X
        r = dict(sar=a["outcome"] == "SAR", decided=done, age=int((X - a["gen"]).total_seconds() // 86400),
                 dage=int((dec - a["gen"]).total_seconds() // 86400), inv=a["triage"] == "ESC")
        if r["age"] >= 330 and done:
            hist[a["scenario"]].append((r["dage"], r["sar"]))
        if C.P0 <= a["bdate"] <= C.P1:
            out[a["scenario"]].append(r)
    return out, hist


def clean_reads(W):
    year, hist = clean_year(W)
    res = {}
    for code in C.CODES:
        al = year[code]
        n = len(al)
        sar = sum(r["sar"] and r["decided"] for r in al)
        dec = sum(r["decided"] for r in al)
        und = [r for r in al if not r["decided"]]
        h = sorted(hist[code])

        def f(age):
            later = [s for d, s in h if d > age]
            return sum(later) / len(later) if later else 1.0
        inv = [r for r in hist[code] if True]
        res[code] = {"decided_only": 100.0 * sar / dec, "open_as_no": 100.0 * sar / n,
                     "project": 100.0 * (sar + len(und) * sar / dec) / n,
                     "golden": 100.0 * (sar + sum(f(r["age"]) for r in und)) / n,
                     "truth": 100.0 * sum(r["sar"] for r in al) / n}
    return res


def call_of(d, key):
    return sorted(c for c in C.CODES if d[c][key] < C.FLOOR)


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    P = A.Pack(C.TARGET)
    W = Wd.build()
    gold, prod = P.call("golden")

    # ---------------------------------------------------------------- R: the three rules, executed
    hdr = open(os.path.join(C.TARGET, Pk.FILES["alerts"]), encoding="utf-8").readline()
    check("R1 the pack ships each alert's raise and triage stamps and each investigation's opening and decision",
          all(k in hdr for k in ("created_at_utc", "triage_closed_at_utc", "case_id"))
          and all({"opened_at", "decided_at", "status", "disposition"} <= set(c) for c in P.cases.values()))
    heads = []
    for k, fn in Pk.FILES.items():
        if fn.endswith(".csv"):
            heads.append(open(os.path.join(C.TARGET, fn), encoding="utf-8").readline().lower())
    check("R1 no shipped column holds a productivity, conversion or SAR rate",
          not any(re.search(r"productivity|conversion|sar_rate|sar_share|hit_rate", h) for h in heads)
          and not any(b"roductivity" in z.read(n) for fn in (Pk.FILES["catalogue"], Pk.FILES["capacity"])
                      for z in [zipfile.ZipFile(os.path.join(C.TARGET, fn))] for n in z.namelist()))
    cr = clean_reads(W)
    check("R3a the analyst test: the decided-alert reading on the clean world files the default answer",
          call_of(cr, "decided_only") == DEFAULT, call_of(cr, "decided_only"))
    check("R3a the undecided projected at the decided share on the clean world files the default answer",
          call_of(cr, "project") == DEFAULT, call_of(cr, "project"))
    check("R3b the decisive step alone (each undecided alert read by how alerts undecided at its age ended) files the "
          "golden on the clean world", call_of(cr, "golden") == GOLD, call_of(cr, "golden"))
    check("R3b the undecided read as not ending in a SAR stays on a wrong answer on the clean world",
          call_of(cr, "open_as_no") != GOLD, call_of(cr, "open_as_no"))
    check("R3b the clean world's truth is the golden", call_of(cr, "truth") == GOLD, call_of(cr, "truth"))
    for label, kw in (("R2 UTC dates for business dates", {"by": "utc"}),
                      ("R2 the Eastern calendar date for the business date", {"by": "eastern"}),
                      ("R2 the re-run copies kept", {"dups": True}),
                      ("R2 alerts added to an investigation they did not open read as no SAR", {"opener_only": True})):
        st, _ = P.call("golden", **kw)
        check(label + ": the call stands", st == gold, st)
    check("R2 the replaced scenario read apart: XB-HRJ and XB-HRJ2 each above the floor",
          all(P.productivity(c, "golden", apart=True) > C.FLOOR + 0.5 for c in ("XB-HRJ", "XB-HRJ2")))
    th = open(os.path.join(C.TARGET, Pk.FILES["thread"]), encoding="utf-8").read()
    pdf = subprocess.run(["pdftotext", "-layout", os.path.join(C.TARGET, Pk.FILES["procedure"]), "-"],
                         capture_output=True, text=True).stdout
    check("R3c no document names a scenario or quotes a scenario's figure",
          not any(c in th or c in pdf for c in C.CODES + ["XB-HRJ2"]))
    rows = list(csv.DictReader(open(os.path.join(C.TARGET, Pk.FILES["alerts"]), encoding="utf-8")))
    seq = [(r["scenario_code"], r["customer_no"], r["alert_score"]) for r in rows if r["triage_outcome"] != "DUP"]
    blocks = {}
    rep = 0
    for i in range(0, len(seq) - 6):
        k = tuple(seq[i:i + 6])
        if k in blocks:
            rep += 1
        blocks[k] = i
    check("R3c no copied block of alert rows outside the re-run's duplicates", rep == 0, rep)

    # ---------------------------------------------------------------- the call and the ladder
    check("the golden tuning set", gold == GOLD, gold)
    check("figures.json carries the golden", fig["call"]["tuning"] == GOLD)
    check("the golden is the world's truth", sorted(c for c in C.CODES if fig["truth"][c] < C.FLOOR) == GOLD)
    check("every golden productivity at least half a point from the floor",
          min(abs(prod[c] - C.FLOOR) for c in C.CODES) >= 0.5, min(abs(prod[c] - C.FLOOR) for c in C.CODES))
    check("every true productivity at least half a point from the floor",
          min(abs(fig["truth"][c] - C.FLOOR) for c in C.CODES) >= 0.5)
    lad = fig["ladder"]
    names = list(lad)
    for k in names[:4]:
        check("ladder %s files a wrong answer with every trap in" % k.split()[0],
              lad[k]["tuning"] != GOLD and set(TRAPS) <= set(lad[k]["tuning"]), lad[k]["tuning"])
    check("ladder R0 is the default answer, each trap at least 0.25 below the floor",
          lad[names[0]]["tuning"] == DEFAULT and max(lad[names[0]]["productivity"][t] for t in TRAPS) <= C.FLOOR - 0.25)
    check("ladder R4 is the golden", lad[names[4]]["tuning"] == GOLD)
    check("the traps are the scenarios with the slowest SAR decisions",
          sorted(sorted(C.SCEN, key=lambda s: -s[5])[i][0] for i in range(3)) == TRAPS)

    # ---------------------------------------------------------------- the fork rows
    st, _ = P.call("golden", by="utc")
    st2, _ = P.call("golden", by="eastern")
    check("SF1 business date, UTC date and Eastern date file one call", st == gold and st2 == gold)
    check("SF2 the re-run copies dropped or kept file one call", P.call("golden", dups=True)[0] == gold)
    check("SF3 the replaced scenario together or apart stays out of the tuning",
          "XB-HRJ" not in gold and P.productivity("XB-HRJ", "golden", apart=True) > C.FLOOR
          and P.productivity("XB-HRJ2", "golden", apart=True) > C.FLOOR)
    check("SF4 an alert added to an investigation ends with it; read as no SAR the call is unchanged",
          P.call("golden", opener_only=True)[0] == gold)
    sar_cases = {s["case_id"] for s in P.sars}
    closed = {cid for cid, c in P.cases.items() if c["status"] == "CLOSED" and c["decided_at"] >= "2025-07-01"}
    check("SF5 the SAR log and the case manager agree on which investigations filed (continuing reports and "
          "corrections add no SAR)",
          all((c in sar_cases) == (P.cases[c]["disposition"] == "SAR filed") for c in closed))
    check("SF6 the twelve months by business date hold every run from 1 October 2025 to 30 September 2026",
          sum(1 for r in P.runs.values() if C.P0.isoformat() <= r["business_date"] <= C.P1.isoformat()
              and r["run_type"] == "SCHEDULED") == (C.P1 - C.P0).days + 1)
    check("SF7 strict or inclusive floor, and rounding to one decimal before comparing, file one call",
          sorted(c for c in C.CODES if round(prod[c], 1) <= C.FLOOR) == gold)
    held = [m for m in range(120, 451, 15) if P.call("golden", min_age=m)[0] == gold]
    check("SF8 the history window holds the call at every age from 120 to 450 days", len(held) == 23, held)
    check("SF8 the mature-cohort reading holds the call from 4 to 9 months",
          all(P.call("mature", months=mo)[0] == gold for mo in (4, 5, 6, 7, 8, 9)))
    check("SF8 a prior-quarter or every-open-investigation reading files the same call",
          P.call("prior_quarter")[0] == gold and P.call("all_open_investigations_sar")[0] == gold)
    check("SF9 no alert of the year is still in triage on the extract",
          sum(1 for a in P.alerts if a["triage"] == "OPEN" and C.P0 <= a["bdate"] <= C.P1) == 0)
    late = [c for c in P.cases.values() if c["decided_at"] and "2026-11-02T11:00:00Z" < c["decided_at"]]
    check("SF10 nothing is decided between the alert extract and the case export", not late, len(late))
    check("SF11 the only duplicates are the re-run's copies, one per alert of its night",
          sum(1 for a in P.alerts if a["outcome"] == "DUP") == int(P.runs["TMR-20260310-02"]["alerts_raised"])
          and all(a["run"] == "TMR-20260310-02" for a in P.alerts if a["outcome"] == "DUP"))

    # ---------------------------------------------------------------- the asks
    ga = P.ask_investigations()
    cells = [(c, q) for c in C.CODES for q in Q]
    hits = lambda o: sum(1 for k in cells if o.get(k, 0) == ga.get(k, 0))
    by_case = {}
    for a in P.alerts:
        if a["case"]:
            by_case.setdefault(a["case"], []).append(a)
    win = [c for c in P.cases.values()
           if C.P0 <= C.to_eastern(A._t(c["opened_at"])).date() <= C.P1]
    first_esc = all(min(by_case[c["case_id"]], key=lambda a: a["tclosed"])["tclosed"] == A._t(c["opened_at"])
                    and sum(1 for a in by_case[c["case_id"]] if a["tclosed"] == A._t(c["opened_at"])) == 1 for c in win)
    check("SF12 each investigation's opening alert is unique and is its earliest escalation", first_esc)
    check("SF12 the case's lowest alert number is another scenario's alert in many investigations (ask A cracker "
          "keeps at most 6 of 56 cells)", hits(P.ask_investigations(attribute="lowest_id")) <= 6,
          hits(P.ask_investigations(attribute="lowest_id")))
    check("ask A every scenario among an investigation's alerts keeps no cell",
          hits(P.ask_investigations(attribute="every")) == 0)
    check("ask A the quarter of the alert's business date keeps at most 3 cells",
          hits(P.ask_investigations(quarter="alert")) <= 3)
    check("SF13 the opening's UTC and Eastern dates give one quarter table", P.ask_investigations(clock="utc") == ga)
    check("SF16 XB-HRJ's row differs from its old code alone, so the replacement is read with it",
          sum(1 for a in P.alerts if a["code"] == "XB-HRJ2" and a["opener"]) > 0)
    check("ask A every cell is a count of 40 or more", min(ga[k] for k in cells) >= 40, min(ga[k] for k in cells))
    gb = P.ask_sars()
    bc = [(m, k) for m in M for k in ("initial", "continuing")]
    hb = lambda o: sum(1 for k in bc if o.get(k, 0) == gb.get(k, 0))
    check("SF14 the prior-report field read alone (the ask B cracker) keeps no cell", hb(P.ask_sars(read="field")) == 0)
    check("ask B every filing citing a prior read as continuing keeps no cell", hb(P.ask_sars(read="prior_only")) == 0)
    kinds = P.sar_kinds()
    blank = {}
    corr = {}
    for s in P.sars:
        d = C.to_eastern(A._t(s["filed_at_utc"])).date()
        if d.year == 2026 and d.month <= 10:
            if kinds[s["bsa_id"]] == "continuing" and not s["prior_bsa_id"]:
                blank[d.month] = blank.get(d.month, 0) + 1
            if kinds[s["bsa_id"]] == "correction":
                corr[d.month] = corr.get(d.month, 0) + 1
    check("ask B every month holds continuing activity reports with an empty prior-report field",
          all(blank.get(m, 0) >= 2 for m in range(1, 11)), blank)
    check("ask B every month holds a correction", all(corr.get(m, 0) >= 1 for m in range(1, 11)), corr)
    check("ask B no correction or initial report has an empty prior field where it cites one",
          all(s["prior_bsa_id"] for s in P.sars if kinds[s["bsa_id"]] == "correction"))
    check("SF15 the filing's UTC and Eastern dates give one month table", P.ask_sars(clock="utc") == gb)
    pc = {s["bsa_id"]: s for s in P.sars}
    check("ask B every empty-field continuing report follows an earlier filing on its investigation in the log",
          all(any(t["case_id"] == s["case_id"] and t["filed_at_utc"] < s["filed_at_utc"] for t in P.sars)
              for s in P.sars if not s["prior_bsa_id"] and kinds[s["bsa_id"]] == "continuing"))
    P2 = A.Pack(C.TARGET)
    P2.sars = []
    check("separation: the call reads nothing from the SAR log", P2.call("golden")[0] == gold
          and all(abs(P2.productivity(c) - prod[c]) < 1e-12 for c in C.CODES))
    check("separation: the call is unchanged whichever alert an investigation is credited to",
          P.call("golden")[0] == P.call("golden", opener_only=False)[0])

    # ---------------------------------------------------------------- the goldens' quoted facts
    for t in TRAPS:
        f = P.p_sar_given_open(t)
        check("%s: an alert undecided at 60 days has mostly ended in a SAR" % t, f(60) > 0.5, f(60))
    check("the paper's undecided counts are the figures'", all(fig["counts"][t]["undecided_in_investigation"]
                                                              == P.counts(t)["undecided_in_investigation"] for t in TRAPS))

    # ---------------------------------------------------------------- documents and realism
    data = open(os.path.join(C.TARGET, Pk.FILES["procedure"]), "rb").read()
    check("procedure PDF scrubbed of its writer", b"ReportLab" not in data and b"reportlab" not in data)
    cd = re.search(rb"/CreationDate \(D:(\d{14})", data).group(1)
    md = re.search(rb"/ModDate \(D:(\d{14})", data).group(1)
    check("procedure PDF created before modified, both before the extract", cd < md < b"20261102000000", (cd, md))
    wide = [l for l in pdf.splitlines() if len(l) > 120]
    check("procedure PDF reads back with no line past the margin", not wide, wide[:2])
    stamps = []
    for fn in (Pk.FILES["catalogue"], Pk.FILES["capacity"]):
        core = zipfile.ZipFile(os.path.join(C.TARGET, fn)).read("docProps/core.xml").decode()
        c0 = re.search(r"<dcterms:created[^>]*>([^<]+)<", core).group(1)
        m0 = re.search(r"<dcterms:modified[^>]*>([^<]+)<", core).group(1)
        stamps.append((c0, m0))
    check("each workbook created before modified, stamps distinct per workbook",
          all(c0 < m0 for c0, m0 in stamps) and len(set(stamps)) == len(stamps), stamps)
    ids = [int(r["alert_id"][1:]) for r in rows]
    steps = {b - a for a, b in zip(ids, ids[1:])}
    check("alert numbers rise by varying steps, in the order the alerts were raised",
          len(steps) >= 3 and all(b > a for a, b in zip(ids, ids[1:])), sorted(steps)[:6])
    cs = sorted(int(c[4:]) for c in P.cases)
    check("investigation numbers rise by varying steps", len({b - a for a, b in zip(cs, cs[1:])}) >= 2)
    bs = [int(s["bsa_id"]) for s in sorted(P.sars, key=lambda s: (s["filed_at_utc"], s["bsa_id"]))]
    check("BSA IDs rise in filing order by varying steps",
          all(b > a for a, b in zip(bs, bs[1:])) and len({b - a for a, b in zip(bs, bs[1:])}) > 50)
    secs = {r["started_at_utc"][-3:-1] for r in P.runs.values()} | {r["completed_at_utc"][-3:-1] for r in P.runs.values()}
    check("run start and completion times carry varied seconds", len(secs) > 30)
    check("every run completes after its last alert", all(
        max(a["gen"] for a in P.alerts if a["run"] == rid) < A._t(r["completed_at_utc"]) for rid, r in P.runs.items()))
    stamp_cols = []
    for fn, cols in ((Pk.FILES["alerts"], ("created_at_utc", "triage_closed_at_utc")),
                     (Pk.FILES["sars"], ("filed_at_utc",)), (Pk.FILES["runs"], ("started_at_utc", "completed_at_utc"))):
        for r in csv.DictReader(open(os.path.join(C.TARGET, fn), encoding="utf-8")):
            stamp_cols.extend(r[c] for c in cols if r[c])
    for c in P.cases.values():
        stamp_cols.extend(e["at"] for e in c["events"])
    check("no record dated after the case export", max(stamp_cols) <= "2026-11-02T11:20:00Z", max(stamp_cols))
    check("no round totals: the year's alert counts are not multiples of ten",
          sum(fig["counts"][c]["alerts"] % 10 == 0 for c in C.CODES) <= 2)

    per_run = {}
    for r in rows:
        per_run[r["run_id"]] = per_run.get(r["run_id"], 0) + 1
    check("the run log's alerts raised tie to the alert export run by run",
          all(per_run.get(rid, 0) == int(r["alerts_raised"]) for rid, r in P.runs.items()))
    share = {c: fig["counts"][c]["undecided"] / float(fig["counts"][c]["alerts"]) for c in C.CODES}
    top = sorted(C.CODES, key=lambda c: -share[c])[:3]
    check("the traps are not the scenarios with the most undecided alerts for their size", sorted(top) != TRAPS, top)

    # ---------------------------------------------------------------- input gates
    files = sorted(os.listdir(C.TARGET))
    meta = json.load(open(os.path.join(C.TASK, "metadata.json"), encoding="utf-8"))
    check("ten or more files", len(files) >= 10, len(files))
    check("three or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    check("one file of 25,000 rows or more", len(rows) >= 25_000, len(rows))
    check("two or more distractors named in metadata.json", len(meta["distractors"]) >= 2)
    src = open(os.path.join(HERE, "analysis.py"), encoding="utf-8").read() + open(os.path.join(HERE, "verify.py"),
                                                                                  encoding="utf-8").read()
    check("no distractor is read by the golden or the verifier",
          not any(Pk.FILES[k] in src or ('"%s"' % k) in src for k in Pk.DISTRACTORS))
    check("no file name carries the word distractor", not any("distract" in f for f in files))
    zp = os.path.join(C.TASK, "target.zip")
    if os.path.exists(zp):
        check("target.zip holds exactly target/", sorted(zipfile.ZipFile(zp).namelist()) == files)
    print("%d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
