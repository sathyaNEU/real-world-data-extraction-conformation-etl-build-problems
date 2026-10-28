"""Build task273 (architecture 4): the evidence pack into <task>/target, the goldens into <task>/golden,
metadata.json, generator/figures.json and submission.md, then the checks and the independent verifier, then a
second build into a scratch folder inside the task (removed after) compared byte for byte, then target.zip.

    python3 task273/generator/build.py              everything
    python3 task273/generator/build.py --out DIR    the pack only, into DIR
    python3 task273/generator/build.py --golden     the pack and the goldens, no checks"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import argparse      # noqa: E402
import calendar      # noqa: E402
import hashlib       # noqa: E402
import json          # noqa: E402
import shutil        # noqa: E402
import sys           # noqa: E402
import warnings      # noqa: E402

import numpy as np   # noqa: E402

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A       # noqa: E402
import docs as DC          # noqa: E402
import params as P         # noqa: E402
import records as R        # noqa: E402
import world as Wd         # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(P.ASSEMBLED.timetuple())
FILES = {"members": "ags_member_register_2026-11-03.csv",
         "depth": "ags_register_site_depth_2026-11-03.csv",
         "calls1": "ags_phase1_calls_grch37.tsv",
         "calls2": "ags_phase2_calls_grch38.tsv",
         "register": "kgl_variant_register_2026-11-03.xlsx",
         "conditions": "ccsp_panel_review_2027-28_conditions.xlsx",
         "policy": "ccsp_panel_policy_v3.pdf",
         "methods": "ags_methods_and_quality_report_issue6.pdf",
         "programme": "ccsp_results_2025-26.csv",
         "turnaround": "kgl_ccsp_turnaround_2025-26.csv",
         "referrals": "ccsp_referrals_2023-2026.csv"}
DISTRACTORS = ("turnaround", "referrals")
GOLDEN_XLSX = "carrier_panel_review_2027-28.xlsx"
GOLDEN_DOCX = "panel_recommendation_2027-28.docx"
PDF_DATES = {"policy": (b"D:20240312104500+00'00'", b"D:20240312111800+00'00'"),
             "methods": (b"D:20261103152000+00'00'", b"D:20261104093500+00'00'")}
OOXML = {"register": (P.LAB, P.LAB, "2019-02-04T10:12:00Z", "2026-11-03T14:41:00Z", "KGL variant register"),
         "conditions": (P.PEOPLE["chair"], P.PEOPLE["chair"], "2026-09-29T08:55:00Z", "2026-10-21T16:03:00Z",
                        "Panel review 2027-28: conditions under review")}


def write_xlsx(path, sheets, widths=None):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    wb.remove(wb.active)
    for name, (head, rows) in sheets.items():
        ws = wb.create_sheet(name)
        ws.append(head)
        for c in ws[1]:
            c.font = Font(bold=True)
        for row in rows:
            ws.append([None if v == "" else v for v in row])
        for i, h in enumerate(head):
            col = ws.cell(row=1, column=i + 1).column_letter
            ws.column_dimensions[col].width = max(10, min(46, 1.1 * max(len(str(h)), *(len(str(r[i])) for r in rows[:400])) + 1)) if rows else 12
        ws.freeze_panes = "A2"
    wb.save(path)


def coverage(w):
    rows = []
    rel = ~w.qc_fail
    vals = {p: np.concatenate([w.depth[s["site_id"]][rel & (w.phase == p)] for s in w.study_sites]) for p in (1, 2)}
    rows.append(["Median reads at a site", "%d" % np.median(vals[1]), "%d" % np.median(vals[2])])
    rows.append(["Mean reads at a site", "%.1f" % vals[1].mean(), "%.1f" % vals[2].mean()])
    rows.append(["Fewest reads at a site", "%d" % vals[1].min(), "%d" % vals[2].min()])
    rows.append(["Member-sites read 20 times or more", "%.1f per cent" % (100 * (vals[1] >= 20).mean()),
                 "%.1f per cent" % (100 * (vals[2] >= 20).mean())])
    return rows


def build(out, seed=P.SEED, keep=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, FILES[k])
    w = Wd.World(seed)
    rc = R.Records(w)
    n = {}
    for key, fn, delim in (("members", rc.members, ","), ("depth", rc.depth, ","),
                           ("calls1", lambda: rc.calls(1), "\t"), ("calls2", lambda: rc.calls(2), "\t"),
                           ("programme", rc.programme_rows, ","), ("turnaround", rc.turnaround_rows, ","),
                           ("referrals", rc.referral_rows, ",")):
        head, rows = fn()
        R.write_csv(p(key), head, rows, delim=delim)
        n[key] = len(rows)
    (rh, rr), (hh, hr) = rc.register_rows()
    write_xlsx(p("register"), {"Register": (rh, rr), "Change history": (hh, hr)})
    n["register"] = len(rr)
    ch, cr = rc.conditions_rows()
    write_xlsx(p("conditions"), {"Conditions": (ch, cr)})
    n["conditions"] = len(cr)
    DC.write_policy(p("policy"))
    DC.write_methods(p("methods"), coverage(w))
    return dict(w=w if keep else None, counts=n)


def finish(out):
    import postprocess as PP
    for k, (c, m) in PDF_DATES.items():
        PP.normalize_pdf(os.path.join(out, FILES[k]), c, m)
    for k, (cr, lb, c, m, title) in OOXML.items():
        PP.normalize_ooxml(os.path.join(out, FILES[k]), cr, lb, c, m, title=title, excel=True)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))


def figures(w, S):
    names = {g: c for g, c, *_ in P.CONDITIONS}
    fr = {g: A.per_thousand(v) for g, v in S["freq"].items()}
    jn = S["joining"]
    sentence = ("Put %d conditions on the 2027/28 panel: keep the eleven on the 2026/27 panel and add %s; no condition "
                "leaves." % (len(S["panel"]), ", ".join("%s (%s)" % (names[g], g) for g in jn[:-1]) +
                                                  " and %s (%s)" % (names[jn[-1]], jn[-1])))
    fig = {
        "call": {"sentence": sentence, "panel": S["panel"], "joining": jn, "leaving": S["leaving"],
                 "panel_size": len(S["panel"])},
        "cohort": S["cohort"], "cohort_by_phase": {str(k): v for k, v in S["cohort_by_phase"].items()},
        "freq_per_1000": fr,
        "freq_exact": {g: round(v * 1000, 4) for g, v in S["freq"].items()},
        "called": {g: {str(p): c for p, c in v.items()} for g, v in S["called"].items()},
        "rungs_per_1000": {r: {g: round(S["rungs"][r][g] * 1000, 2) for g in jn} for r in S["rungs"]},
        "ask_b": {h: {g: S["ask_b"][(h, g)] for g in w.panel_genes} for h in ("H1", "H2")},
        "out_range": [min(fr[g] for g in fr if g not in S["panel"]), max(fr[g] for g in fr if g not in S["panel"])],
        "stay_min": min(fr[g] for g in S["panel_2026"]),
        "caller": {str(ph): {"k": P.CALLER[ph]["k"], "f_pct": int(round(P.CALLER[ph]["f"] * 100)),
                             "floor": P.CALLER[ph]["floor"]} for ph in (1, 2)},
        "panel_line": {"one_in": 200, "per_1000": 5, "per": "1,000"},
        "called_totals": {str(p): sum(v[p] for v in S["called"].values()) for p in (1, 2)},
        "policy_clauses": ["2.1", "2.2", "2.3", "2.4", "4.1", "4.2", "4.3"],
    }
    return fig


def write_goldens(golden, w, S, fig):
    import deliver as DV
    if os.path.exists(golden):
        shutil.rmtree(golden)
    os.makedirs(golden)
    png = DV.chart_png(S)
    DV.write_workbook(os.path.join(golden, GOLDEN_XLSX), S, fig)
    DV.write_paper(os.path.join(golden, GOLDEN_DOCX), S, fig, png)


def finish_golden(golden):
    import postprocess as PP
    PP.normalize_ooxml(os.path.join(golden, GOLDEN_XLSX), P.PEOPLE["chair"], P.PEOPLE["chair"],
                       "2026-11-19T09:40:00Z", "2026-11-27T17:22:00Z", title="Panel review 2027-28", excel=True)
    PP.normalize_ooxml(os.path.join(golden, GOLDEN_DOCX), P.PEOPLE["chair"], P.PEOPLE["chair"],
                       "2026-11-24T10:05:00Z", "2026-11-28T12:47:00Z", title="Carrier screening panel for 2027/28")
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))


SOURCES = {
    "members": "the Study's member register (phase, recruitment area, sample, genotype status, consent)",
    "depth": "the laboratory's read counts at every register site for every released member",
    "calls1": "the phase 1 calling pipeline's non-reference calls at register sites, GRCh37, 2019 transcript names",
    "calls2": "the phase 2 calling pipeline's non-reference calls at register sites, GRCh38",
    "register": "the laboratory's variant register with its change history",
    "conditions": "the Panel Review Group's list of the 30 conditions under review",
    "policy": "the programme's panel policy, version 3",
    "methods": "the laboratory's methods and quality report for the Study's two phases",
    "programme": "the programme's 2025/26 results export, one row per finding or per partner without one",
    "turnaround": "the laboratory's monthly turnaround statistics for the programme",
    "referrals": "the programme's monthly referrals by source",
}


def metadata(fig, counts):
    src = ("constructed by the task generator (seeded); %s, the %s, the %s, the places, people and records are "
           "fictional; gene and variant names follow public nomenclature" % (P.BOARD, P.STUDY, P.LAB))
    return {
        "task": "task273",
        "title": "%s: the %s's 2027/28 panel" % (P.BOARD, P.PROGRAMME),
        "domain": "Biomedical & Clinical Research (statistical genomics)",
        "objective": "Descriptive & Distribution Analysis",
        "distractor_files": ["target/" + FILES[k] for k in DISTRACTORS],
        "deliverables": [GOLDEN_XLSX, GOLDEN_DOCX],
        "provenance": {FILES[k]: {"source": "%s; %s" % (SOURCES[k], src), "date": P.EXTRACT.isoformat(),
                                  "licence": "CC0 1.0 (constructed for this task)"} for k in sorted(FILES)},
        "rows": {FILES[k]: v for k, v in sorted(counts.items())},
        "answer": fig["call"]["sentence"],
        "field_terms": [],
        "stated_inputs": ["200", "1,000"],
    }


def digest(folder):
    h = hashlib.sha256()
    for root, _, files in sorted(os.walk(folder)):
        for f in sorted(files):
            fp = os.path.join(root, f)
            h.update(os.path.relpath(fp, folder).encode())
            h.update(open(fp, "rb").read())
    return h.hexdigest()


def main_build(target, golden, seed=P.SEED):
    b = build(target, seed, keep=True)
    finish(target)
    w = b["w"]
    S = A.solve(w)
    fig = figures(w, S)
    write_goldens(golden, w, S, fig)
    finish_golden(golden)
    with open(os.path.join(HERE, "figures.json"), "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
        f.write("\n")
    import writeup as WU
    WU.write(json.load(open(os.path.join(HERE, "figures.json"))))
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(metadata(fig, b["counts"]), f, indent=1, sort_keys=True)
        f.write("\n")
    return b, S, fig


def make_zip(target, zpath):
    import zipfile
    files = sorted(os.listdir(target))
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            zi = zipfile.ZipInfo("target/" + f, date_time=P.ASSEMBLED.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--golden", action="store_true")
    a = ap.parse_args()
    if a.out:
        build(a.out)
        finish(a.out)
        print("pack written to", a.out)
        return
    target, golden = os.path.join(TASK, "target"), os.path.join(TASK, "golden")
    b, S, fig = main_build(target, golden)
    print("pack:", b["counts"])
    if a.golden:
        return
    import checks as CK
    import verify as VF
    ok = CK.run(target, golden, b["w"], S, fig)
    vok = VF.run(target, golden)
    scratch = os.path.join(TASK, ".rebuild_check")
    build(os.path.join(scratch, "target"))
    finish(os.path.join(scratch, "target"))
    same = digest(target) == digest(os.path.join(scratch, "target"))
    w2 = Wd.World(P.SEED)
    S2 = A.solve(w2)
    write_goldens(os.path.join(scratch, "golden"), w2, S2, figures(w2, S2))
    finish_golden(os.path.join(scratch, "golden"))
    same_g = digest(golden) == digest(os.path.join(scratch, "golden"))
    shutil.rmtree(scratch)
    print("rebuild byte-identical: target %s, golden %s" % (same, same_g))
    if ok and vok and same and same_g:
        make_zip(target, os.path.join(TASK, "target.zip"))
        print("target.zip", hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()[:8])
    else:
        print("NOT zipped: checks %s, verify %s, rebuild %s/%s" % (ok, vok, same, same_g))
        sys.exit(1)


if __name__ == "__main__":
    main()
