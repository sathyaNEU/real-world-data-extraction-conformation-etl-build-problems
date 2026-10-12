"""Build the pack, the golden deliverable and metadata.json, run every check and the independent
verifier, build a second time into a scratch folder and require byte-identical output, then cut
target.zip.

    python3 task447/generator/make.py
"""
import csv
import filecmp
import json
import os
import shutil
import sys
import tempfile
import time
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import checks as C
import deliver as DL
import docs as DC
import golden as G
import pack as PK
import sim as S
import verify as V

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMP = (2025, 10, 21, 8, 30, 0)
DISTRACTORS = [PK.FILES["hcris"], PK.FILES["ma"]]

DESCRIPTIONS = {
    PK.FILES["fac24"]: ("Commercial outpatient facility claims, layout 3.1, dates of service 2024, paid through 31 August 2025",
                        "Wisconsin APCD, request OHCCR-MO-2025-031", "2025-09-15"),
    PK.FILES["fachist"]: ("Commercial outpatient facility claims referred by physicians of practices acquired 2021 to 2023, layout 2.4",
                          "Wisconsin APCD, acquisition review extract", "2024-08-12"),
    PK.FILES["prof24"]: ("Commercial professional claims performed in Manitowoc and Kewaunee counties, layout 3.1, 2024",
                         "Wisconsin APCD, request OHCCR-MO-2025-031", "2025-09-15"),
    PK.FILES["elig"]: ("Eligibility spans 2021 to 2024 for members with a line in the claim files",
                       "Wisconsin APCD, request OHCCR-MO-2025-031", "2025-09-15"),
    PK.FILES["prodref"]: ("Carrier product reference", "Wisconsin APCD", "2025-09-15"),
    PK.FILES["ma"]: ("Medicare Advantage outpatient facility claims referred by Manitowoc and Kewaunee county physicians, 2024, layout 3.1",
                     "Wisconsin APCD, request OHCCR-MO-2025-031", "2025-09-15"),
    PK.FILES["tiers"]: ("Network tier placements of the three hospital systems in each tiered product, plan years 2020 to 2026",
                        "OHCCR market oversight unit, from carrier form filings", "2025-09-26"),
    PK.FILES["register"]: ("Provider ownership register (notices of material change and annual registrations)",
                           "OHCCR provider registry", "2025-10-01"),
    PK.FILES["reassign"]: ("NPI reassignment history: physician and practitioner billing relationships",
                           "OHCCR provider registry, from PECOS reassignments and carrier rosters", "2025-10-01"),
    PK.FILES["provfile"]: ("Carrier provider files, providers in network 2019 to 2025", "Wisconsin APCD provider submissions",
                           "2025-09-15"),
    PK.FILES["facdir"]: ("Outpatient facility directory, northeast region", "OHCCR provider registry", "2025-10-01"),
    PK.FILES["medicare"]: ("CY2025 Medicare OPPS and CLFS amounts, Wisconsin wage-adjusted, CBSA 24580",
                           "CMS addenda as compiled by OHCCR", "2025-02-14"),
    PK.FILES["exhibit"]: ("Exhibit C to notice N25-014: Ledgestone Health rates", "Ledgestone Health (filer)", "2025-10-07"),
    PK.FILES["hcris"]: ("Hospital cost report extract, outpatient lines, fiscal year 2023", "CMS HCRIS as compiled by OHCCR",
                        "2025-03-31"),
    DC.RULE: ("Rule OHCCR 4, preliminary review of notices of material change", "OHCCR", "2023-02-14"),
    DC.APPENDIX: ("Market oversight technical appendix, revision 3", "OHCCR market oversight unit", "2025-06-02"),
    DC.DICTIONARY: ("APCD extract data dictionary, request OHCCR-MO-2025-031", "Wisconsin APCD", "2025-09-16"),
    DC.NOTICE: ("Notice of material change N25-014 with exhibits A and B", "Ledgestone Health and Brightwater Medical Group",
                "2025-10-06"),
}


def build(target, golden_dir):
    shutil.rmtree(target, ignore_errors=True)
    shutil.rmtree(golden_dir, ignore_errors=True)
    wd = S.build()
    packed = PK.write_all(wd, target)
    DC.write_docs(target, wd)
    manifest(target)
    g = G.compute(target)
    path, figs = DL.write(g, golden_dir)
    return wd, packed, g, figs


def count_rows(p):
    if p.endswith(".csv"):
        with open(p, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    return ""


def manifest(target):
    rows = []
    for f in sorted(DESCRIPTIONS):
        desc, src, run = DESCRIPTIONS[f]
        rows.append([f, desc, src, run, count_rows(os.path.join(target, f))])
    with open(os.path.join(target, "export_manifest.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["file_name", "description", "source", "produced", "rows"])
        for r in rows:
            w.writerow(r)


def metadata(target):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        ext = os.path.splitext(f)[1].lstrip(".")
        files.append({"path": f, "format": ext, "bytes": os.path.getsize(p), "rows": count_rows(p) or None,
                      "source": "Constructed: " + (DESCRIPTIONS[f][0] if f in DESCRIPTIONS else "export manifest"),
                      "date": DESCRIPTIONS[f][2] if f in DESCRIPTIONS else "2025-10-21",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    return {
        "task": "task447",
        "title": "Whether notice N25-014 (Ledgestone Health buying Brightwater Medical Group) proceeds to a cost and market impact review",
        "domain": "Healthcare Delivery & Health Economics",
        "subdomain": "Payment, claims & health-plan analytics",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "07 (grid of cells): the call and the projected 2026 increase, then the review's two standing exhibits: the commercial imaging, endoscopy and arthroscopy services each lakeshore county's residents received in 2024 with Brightwater's referred share (county by line), and Brightwater's and Ledgestone's shares of the two counties' office visits by specialty",
        "as_of": "2025-10-21",
        "deliverables": [DL.OUT],
        "distractor_files": DISTRACTORS,
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task447/generator/make.py (seeded, deterministic) on the layout "
                               "of a state all-payer claims database extract; every carrier, system, practice, physician, "
                               "member key and figure is invented. County names, ZIP codes, CPT codes, NUCC taxonomy codes "
                               "and place-of-service codes are the real public vocabularies.",
                     "date": "2025-10-21", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-11",
        "generator": "task447/generator/make.py",
        "files": files,
    }


def owed_figures(g, figs):
    """Every figure submission.md states, as it states it (figures_check.py reads this file): the graded
    figures of the deliverable, the critical components and the step results, and the filed references the
    steps cite (rule sections, layout versions, the threshold)."""
    out = json.loads(json.dumps(figs))
    out["write_up"] = {
        "threshold_m": "%.1f" % (G.THRESHOLD / 1e6),
        "professional_prices": "{:,}".format(int(round(g["P"] / 1e4)) * 10000),
        "referred_services": "{:,}".format(int(round(g["referred"] / 1e4)) * 10000),
        "tier_one_share_pct": "%d" % round(100 * g["c1"]),
        "tier_two_share_pct": "%d" % round(100 * g["c2"]),
        "rule_sections_cited": ["4.03", "4.04", "4.05", "4.06"],
        "claims_layouts": ["2.4", "3.1"],
        "office_visit_codes": ["99202", "99215"],
    }
    # the periods and the rounding unit the prompt fixes, as the answers name them
    out["prompt_parameters"] = {"baseline_year": "2024", "projection_year": "2026"}
    return out


def stamp_tree(root):
    t = time.mktime(STAMP + (0, 0, -1))
    for dp, dns, fns in os.walk(root):
        for fn in fns:
            os.utime(os.path.join(dp, fn), (t, t))


def zip_target(target, out):
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            p = os.path.join(target, fn)
            zi = zipfile.ZipInfo(fn, date_time=STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(p, "rb").read())


def main():
    t0 = time.time()
    wd, packed, g, figs = build(TARGET, GOLDEN)
    meta = metadata(TARGET)
    with open(os.path.join(TASK, "metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(owed_figures(g, figs), fh, indent=1, sort_keys=True)
        fh.write("\n")
    n, L, bt = C.run(TARGET, TASK, wd, packed, g)
    C.submission_check(TASK, json.loads(json.dumps(figs)), g)
    C.house_checks(TARGET, TASK, g)
    n = C.N[0]
    v = V.run(TARGET)
    V.compare(v, json.loads(json.dumps(figs)))
    # second build, byte-identical
    tmp = tempfile.mkdtemp()
    t2, g2 = os.path.join(tmp, "target"), os.path.join(tmp, "golden")
    build(t2, g2)
    for a, b in ((TARGET, t2), (GOLDEN, g2)):
        for fn in sorted(os.listdir(a)):
            assert filecmp.cmp(os.path.join(a, fn), os.path.join(b, fn), shallow=False), "not byte-identical: " + fn
    shutil.rmtree(tmp)
    stamp_tree(TARGET)
    zip_target(TARGET, os.path.join(TASK, "target.zip"))
    # the archive is the tree, member for member and byte for byte (H4, H7), with a receipt (H19)
    import hashlib
    with zipfile.ZipFile(os.path.join(TASK, "target.zip")) as z:
        names = z.namelist()
        assert sorted(names) == sorted(os.listdir(TARGET)) and all("/" not in n for n in names)
        for n_ in names:
            assert z.read(n_) == open(os.path.join(TARGET, n_), "rb").read(), n_
    zp = os.path.join(TASK, "target.zip")
    print("target.zip: %d bytes, %d members, sha256 %s" % (os.path.getsize(zp), len(names),
                                                          hashlib.sha256(open(zp, "rb").read()).hexdigest()))
    print("checks %d green; verifier agrees; two builds byte-identical; %s; %.0fs" % (n, meta["input_gates"], time.time() - t0))
    print("answer: %s, increase %.0f (P %.0f, referred %.0f), c1 %.5f" % (g["call"], g["total"], g["P"], g["referred"], g["c1"]))
    for k, val in L["rungs"].items():
        print("  %-30s %12.0f" % (k, val))
    for k, val in bt.items():
        print("  back-test %-22s worst miss %.4f, %d groups" % (k, val[0], C.REPORT["groups"][k]))
    for k, (lo1, hi1, lo2, hi2, n) in C.REPORT["refinements"].items():
        print("  refinement %-24s tier one %.4f to %.4f, tier two %.4f to %.4f, %d cells" % (k, lo1, hi1, lo2, hi2, n))
    print("  Norbridge Tiered EPO at Wolf River by plan year: %s" % ", ".join(
        "plan years %s %.4f (%d services)" % (py, v, n) for py, (v, n) in sorted(C.REPORT["switch"].items())))
    h = g["hist"]
    for tin in sorted(h["prac_tin"].unique()):
        f = G.fit_models(h[h["prac_tin"] == tin])
        print("  practice %s (%s): all referrals %.3f, tier one %.4f" % (tin, h.loc[h["prac_tin"] == tin, "acq_sys"].iloc[0],
                                                                       f["pooled"]["all"], f["tier"]["1"]))
    print("  shares stated: employed group %.2f, lakeshore affiliate %.2f, pooled Ledgestone %.2f, pooled all %.2f"
          % (L["c_lmg"], L["c_mfp"], L["fit_ldg"]["pooled"]["all"], G.whole(g["fit"]["pooled"]["all"])))
    print("  R4 product by product, by line: %s" % ", ".join("%s %.0f" % (k, L["famr4"][k]) for k in sorted(L["famr4"])))
    print("  answer by line: %s" % ", ".join("%s %.0f" % (k, g["fam"][k]) for k in sorted(g["fam"])))
    print("  carrier shares (Ledgestone's purchases): %s" % ", ".join("%s %.2f" % kv for kv in sorted(L["fit_ldg"]["carrier"].items())))
    for k, (c1, c2, tot) in C.REPORT["corridor"].items():
        if k == "tier by service line":
            print("  corridor %-36s tier one %.5f to %.5f by line, unrounded projection %.0f" % (k, c1, c2, tot))
        else:
            print("  corridor %-36s tier one %.5f, tier two %.5f, unrounded projection %.0f" % (k, c1, c2, tot))
    for (m, pr, b), val in L["grid"].items():
        print("  grid %-32s %-10s %-8s %.3f" % (m, pr, b, val / 1e6))
    lab1 = lambda k: "%s %s" % (k[0], {"IMG": "imaging", "ENDO": "endoscopy", "ARTH": "arthroscopy"}[k[1]])
    for k, (tot, b, sh) in g["ex1"].items():
        print("  Exhibit 1 %-24s %5d services, Brightwater %5d, %.3f%%" % (lab1(k), tot, b, sh))
    for k, v in g["ex2"].items():
        print("  Exhibit 2 %-24s %5d visits, Brightwater %5d (%.3f%%), Ledgestone %4d (%.3f%%)" % (k, v[0], v[1], v[3], v[2], v[4]))
    for name, cells in C.REPORT["ex1_stops"].items():
        print("  Exhibit 1 stop %-50s %s" % (name, "; ".join("%+d %+.2f" % cells[k] for k in g["ex1"])))
    for name, cells in C.REPORT["ex2_stops"].items():
        print("  Exhibit 2 stop %-50s %s" % (name, "; ".join("%+.2f %+.2f" % cells[k] for k in g["ex2"])))
    print("  combinations: nearest landing to a bin it left, Exhibit 1 %.3f, Exhibit 2 %.3f" % tuple(C.REPORT["combo_worst"]))


if __name__ == "__main__":
    main()
