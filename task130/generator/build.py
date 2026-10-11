"""Build task130's evidence pack into <out>/target and the golden deliverables into <out>/golden.

    python3 build.py                 build into the task folder (target/, target.zip, golden/, metadata.json)
    python3 build.py --out DIR       build into DIR/target, DIR/target.zip and DIR/golden (a scratch rebuild for the
                                     identity check)
"""
import argparse
import datetime as dt
import json
import os
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W
import sim as SM
import acuity as AC
import extracts as X
import containers as C
import docs as D
import estimators as E

TASK = os.path.dirname(HERE)
FILES = {
    "med": "medical_claim_lines_2025-01_2027-02.csv",
    "rx": "pharmacy_claims_2025-01_2027-02.csv",
    "elig": "eligibility_spans_2027-02.csv",
    "xwalk": "tpa_conversion_crosswalk_2025-01-01.csv",
    "final": "northcourt_stratification_2026_claims_final.xlsx",
    "draft": "northcourt_stratification_2026_claims_draft.xlsx",
    "bid": "northcourt_rfp_2025-07_stratification_2024_claims.xlsx",
    "agreement": "care_management_services_agreement_schedule_c.pdf",
    "renewal": "renewal_letter_2027-28.pdf",
    "rebates": "pbm_rebate_report_2026.xlsx",
    "stoploss": "stop_loss_policy_2027.pdf",
    "plan": "northcourt_implementation_plan_2027-28.pdf",
    "readme": "warehouse_readme_2027-03.txt",
}
DISTRACTORS = ["draft", "rebates", "stoploss", "plan"]
# local (Central) time each file was last written, in the fiction
MTIMES = {
    "med": (2027, 3, 3, 7, 14), "rx": (2027, 3, 2, 6, 41), "elig": (2027, 3, 1, 6, 5), "xwalk": (2025, 1, 6, 15, 22),
    "final": (2027, 3, 5, 9, 48), "draft": (2027, 1, 14, 11, 20), "bid": (2025, 3, 6, 15, 12),
    "agreement": (2027, 2, 17, 10, 42), "renewal": (2027, 2, 26, 16, 5), "rebates": (2027, 2, 19, 8, 31),
    "stoploss": (2026, 12, 18, 9, 12), "plan": (2027, 3, 8, 14, 27), "readme": (2027, 3, 8, 16, 58),
}


def stamp(path, t):
    d = dt.datetime(*t)
    ts = d.replace(tzinfo=C.central(d)).timestamp()
    os.utime(path, (ts, ts))


def adjust(comp, delta):
    """a component with its allowed amount moved by delta cents: a facility claim's rate moves on its largest line,
    a pharmacy claim's ingredient cost moves"""
    ct, npi, amt, lag, rlag, lines, bt, pos, dx1, dx2 = comp
    if lines:
        k = max(range(len(lines)), key=lambda i: lines[i][4])
        ls = [list(l) for l in lines]
        ls[k][5] += delta
        assert 0 < ls[k][5] < ls[k][4], "an adjusted line stays under its charge"
        lines = tuple(tuple(l) for l in ls)
    return (ct, npi, round(amt + delta / 100.0, 2), lag, rlag, lines, bt, pos, dx1, dx2)


def apply_tune(S, table):
    """bin centring: move a handful of facility and pharmacy claims by a few per cent so that no graded figure sits near
    a rounding boundary (the table is written by tune.py and asserted by checks.py)"""
    done = set()
    for i, ev in enumerate(S.events):
        pid, d0, d1, ben, kind, comps, info = ev
        for ci, comp in enumerate(comps):
            key = (pid, d0.isoformat(), kind, ci, int(round(comp[2] * 100)))
            if key in table:
                c = list(comps)
                c[ci] = adjust(comp, table[key])
                S.events[i] = (pid, d0, d1, ben, kind, tuple(c), info)
                done.add(key)
    assert done == set(table), "tuning table out of date: %d of %d keys found" % (len(done), len(table))


def build(out, verbose=True, tune=True):
    t0 = time.time()
    tgt = os.path.join(out, "target")
    if os.path.exists(tgt):
        shutil.rmtree(tgt)
    os.makedirs(tgt)
    S = SM.simulate()
    L = AC.lists(S)
    if tune:
        import tune_table
        apply_tune(S, tune_table.TUNE)
        L2 = AC.lists(S)
        for k in ("bid", "draft", "final"):
            assert [r[:5] for r in L2[k]] == [r[:5] for r in L[k]], "centring moved the %s list" % k
    protect = set(r[1] for k in ("bid", "draft", "final") for r in L[k])
    P = X.Pack(S, W.SEED, protect)
    P.price()
    P.medical_versions()
    P.pharmacy_rows()
    p = lambda k: os.path.join(tgt, FILES[k])
    X.write_csv(p("med"), X.MED_COLS, P.medical_rows())
    X.write_csv(p("rx"), X.PBM_COLS, P.pbm_rows())
    X.write_csv(p("elig"), X.ELIG_COLS, P.eligibility_rows())
    X.write_csv(p("xwalk"), X.XW_COLS, P.crosswalk_rows(set(r[1] for r in L["bid"])))
    D.stratification_xlsx(p("bid"), "bid", L["bid"], S)
    D.stratification_xlsx(p("draft"), "draft", L["draft"], S)
    D.stratification_xlsx(p("final"), "final", L["final"], S)
    D.agreement_pdf(p("agreement"))
    F = E.Files(tgt)
    D.renewal_pdf(p("renewal"), E.letter_figures(F))
    D.rebate_xlsx(p("rebates"), E.rebate_figures(F))
    D.stoploss_pdf(p("stoploss"), E.stoploss_census(F))
    D.implementation_pdf(p("plan"))
    D.readme_txt(p("readme"))
    for k in FILES:
        stamp(p(k), MTIMES[k])
    if verbose:
        print("pack built in %.0fs" % (time.time() - t0))
    return S, L, P


def write_metadata():
    meta = {
        "task": "task130",
        "title": "Red Cedar Valley Schools: the Northcourt care management baseline for 2027-28",
        "domain": "Actuarial Science & Insurance",
        "task_type": "claims-frequency-severity",
        "objective": "Forecasting & Predictive Modeling",
        "as_of": W.ASOF.isoformat(),
        "deliverables": ["cohort_baseline_2027.xlsx", "baseline_certification_memo.docx"],
        "input_files": [{"path": FILES[k], "format": FILES[k].rsplit(".", 1)[1]} for k in sorted(FILES, key=lambda k: FILES[k])],
        "distractor_files": [FILES[k] for k in DISTRACTORS],
        "sources": [{"path": FILES[k], "source": "synthetic, generated by task130/generator from a simulated self-insured "
                                                  "school district health plan", "date": "2026-10-11",
                     "license": "CC BY 4.0, constructed for this task"} for k in sorted(FILES, key=lambda k: FILES[k])],
        "provenance": "Fully constructed pack (dataset-generation section 2). The claims, PBM, eligibility and conversion "
                      "extracts are generated member by member from a simulation of a fictional Minnesota school "
                      "district's health plan, January 2023 to March 2028; the documents were written for the fiction and "
                      "converted to PDF with LibreOffice (the agreement and the renewal letter) or printed to PDF from HTML "
                      "with headless Chromium (the stop-loss schedule and the implementation plan). ICD-10-CM, CPT, HCPCS, "
                      "NUBC revenue, bill type and place of "
                      "service codes are the real published code sets; fee schedule and charge amounts are constructed. "
                      "NDCs are in 5-4-2 form on the real labeler codes of the manufacturers named; their product and "
                      "package segments are constructed and are not checked against the FDA NDC Directory. NPIs and NCPDP "
                      "IDs carry valid formats and check digits but belong to no real provider. No real person's or "
                      "organisation's data.",
        "license": "Constructed data, released with the task (CC BY 4.0).",
        "created": "2026-10-11",
    }
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")


def cut_zip(out):
    """target.zip beside target/: the thirteen files at the archive's top level, in name order, each entry dated with
    its file's own export time, so the archive rebuilds byte for byte with the tree it is cut from"""
    import zipfile
    tgt = os.path.join(out, "target")
    when = {FILES[k]: MTIMES[k] + (0,) for k in FILES}
    with zipfile.ZipFile(os.path.join(out, "target.zip"), "w") as z:
        for name in sorted(os.listdir(tgt)):
            zi = zipfile.ZipInfo(name, date_time=when[name])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            zi.create_system = 3
            with open(os.path.join(tgt, name), "rb") as f:
                z.writestr(zi, f.read())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=TASK)
    ap.add_argument("--no-golden", action="store_true")
    a = ap.parse_args()
    S, L, P = build(a.out)
    if not a.no_golden:
        import golden as G
        G.write(a.out, os.path.join(a.out, "target"), S, L)
    cut_zip(a.out)
    if os.path.abspath(a.out) == os.path.abspath(TASK):
        write_metadata()
    print("built", a.out)
