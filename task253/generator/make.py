"""Build the pack and the goldens, write metadata.json and figures.json, run every check and the independent
verifier, build a second time into a scratch folder and require byte-identical output, then cut target.zip.

    python3 task253/generator/make.py
"""
import filecmp
import json
import os
import shutil
import sys
import tempfile
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as AN
import build as B
import checks as C
import docs as D
import golden as GD
import pack as P
import verify as V
import world as WD

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")

SOURCES = {
    "r2024": "NAPLAN 2024 results, legacy results system extract: one row per student per test, Years 3 and 5",
    "r2025": "NAPLAN 2025 results-portal download: a sheet per year level, one row per student per test",
    "r2026": "NAPLAN 2026 results, data-platform export: one row per student per test, Years 3 and 5",
    "register": "School register as refreshed 3 March 2026, primary schools and secondary colleges",
    "census": "August 2026 enrolment census, headcount by school and year level",
    "directory": "Facilities service directory, annual refresh of 16 February 2026, sites and servicing hubs",
    "plan": "Hub coordinators' 2027 school servicing plan, version of 6 November 2026, a sheet per hub",
    "road": "Routing service one-way road distances and drive times, primary schools to the hubs that could serve them",
    "standard": "Analysis standard LT-AS-04 version 3, Analysing school results in NAPLAN (12 February 2026)",
    "guidelines": "Reading Partnership 2027 programme guidelines (October 2026)",
    "notes": "System data team notes on the extracts and their fields (9 November 2026)",
    "rates": "Panel provider's 2027 schedule of rates for specialist literacy services",
    "pl": "Professional learning register for literacy courses, 2026 school year to date",
}


def docs_text():
    return {"standard": "\n".join(t for _, t in D.STANDARD), "guidelines": "\n".join(t for _, t in D.GUIDE),
            "notes": open(os.path.join(TARGET, P.FILES["notes"])).read()}


def rows_of(path):
    if path.endswith(".csv"):
        return sum(1 for _ in open(path)) - 1
    return None


def write_all(target, golden):
    if os.path.isdir(target):
        shutil.rmtree(target)
    W, tables, fd = B.build()
    names, hubs = P.write(W, tables, target)
    D.standard_pdf(os.path.join(target, P.FILES["standard"]))
    D.guidelines_docx(os.path.join(target, P.FILES["guidelines"]))
    D.notes_txt(os.path.join(target, P.FILES["notes"]), P.FILES)
    points = (fd["mean"] < 480).astype(float)
    figs = AN.asks(W, fd["p"], points)
    GD.write(golden, W, fd, figs, names, hubs)
    for f in os.listdir(target):
        os.utime(os.path.join(target, f), (1794268800, 1794268800))      # 10 November 2026
    return W, tables, fd, figs, names, hubs, points


def metadata(W, tables):
    files = []
    for k, f in P.FILES.items():
        pth = os.path.join(TARGET, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(pth), "rows": rows_of(pth),
                      "source": "Constructed: " + SOURCES[k], "date": "2026-11-10",
                      "license": "CC BY 4.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task253",
        "title": "How many 2027 Reading Partnership places a Catholic school system needs, one per primary school "
                 "whose underlying Year 5 reading average is below 480",
        "domain": "Education & Learning Sciences",
        "subdomain": "student growth and value-added modelling (school-effects estimation)",
        "objective": "Descriptive & Distribution Analysis",
        "prompt_shape": "14 (cuts of a distribution): the number of schools below the floor, its cut by region, and "
                        "the students and hub travel the places carry",
        "as_of": "2026-11-10",
        "deliverables": [GD.XLSX, GD.PNG],
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task253/generator/make.py (seeded, deterministic) "
                               "around a fictional state Catholic school system; NAPLAN is named as the real "
                               "national assessment; every school, locality, hub, region and person is invented, "
                               "and no real school's results are depicted.",
                     "date": "2026-11-10", "license": "CC BY 4.0 (original work)"}],
        "created": "2026-10-11",
        "generator": "task253/generator/make.py",
        "files": files,
    }
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=1)
        f.write("\n")


def figures_json(figs, grid, fam, hubs):
    R = WD.REGION_NAME
    out = {
        "places": figs["places"],
        "shares_pct": {R[r]: "%.1f" % v for r, v in figs["shares"].items()},
        "students_region": {R[r]: "{:,}".format(int(round(v))) for r, v in figs["students_region"].items()},
        "students_total": "{:,}".format(int(round(figs["students_total"]))),
        "students_hub": {hubs[h]: "{:,}".format(int(round(v))) for h, v in figs["students_hub"].items()},
        "km_hub": {hubs[h]: "{:,}".format(int(round(v))) for h, v in figs["km_hub"].items()},
        "km_total": "{:,}".format(int(round(figs["km_total"]))),
        "chart_order": [hubs[h] for h in figs["chart_order"]],
        "chart_title_hub": hubs[figs["chart_title_hub"]],
        "contrasts": {
            "probability_sum": "%.2f" % figs["places_exact"],
            "point_count": grid["R1_points"],
            "three_year_average_count": grid["R0_raw_points"],
            "confident_count_90": grid["R2_bound90"],
            "school_level_points": grid["R3_points"],
            "school_level_probs": "%.1f" % grid["R3_probs"],
            "mass_above_among_below": "%.1f" % grid["mass_above_among_below"],
            "mass_below_among_above": "%.1f" % grid["mass_below_among_above"],
            "sd_predictions": "%.1f" % grid["sd_predictions"],
            "sd_underlying": "%.1f" % grid["sd_underlying"],
            "year5_readers": None,
        },
        "family": {k: ("%.2f" % v if isinstance(v, float) else v) for k, v in fam.items() if k != "ml_fit"},
    }
    return out


def main():
    W, tables, fd, figs, names, hubs, points = write_all(TARGET, GOLDEN)
    metadata(W, tables)
    grid = AN.rungs_and_grid(fd)
    fam, fam_probs = AN.family(fd)
    st = AN.stops(W, fd["p"], points)
    fj = figures_json(figs, grid, fam, hubs)
    fj["contrasts"]["year5_readers"] = "{:,}".format(int(fd["N"]))
    fj["contrasts"]["floor"] = 480
    fj["conventions"] = {"tested_year_level": 5, "served_year_levels_2027": [3, 6], "census_year_levels_2026": [2, 5],
                         "census_year_levels_rolled_schools": [3, 6], "rolled_school_census_levels": [1, 7],
                         "programme_year": 2027,
                         "standard_clauses": ["3.1", "3.2", "3.4"]}
    fj["contrasts"]["census_rolled_schools"] = int(W["rolled"].sum())
    # the census device as built (A2, the design note's ask sheet): the rolled schools by region, their share and
    # their correlation with the schools' chances; each census read's students against the golden, on the plan's
    # hubs, with the point count beside them
    import asks as AK
    import core as CO
    rl = W["rolled"]
    fj["census_device"] = {
        "rolled_by_region": {WD.REGION_NAME[r]: int((rl & (W["region"] == r)).sum()) for r in CO.REGIONS},
        "rolled_share_pct": "%.1f" % (100 * rl.mean()),
        "rolled_corr_with_chance": "%.2f" % np.corrcoef(rl.astype(float), fd["p"])[0, 1],
        "rolled_census_rows": int(7 * rl.sum()),
        "reads": {}}
    for read in AK.READS[1:] + ["point_count"]:
        key = ("golden", "plan", "points", 2) if read == "point_count" else (read, "plan", "probs", 2)
        s1 = st[key]
        fj["census_device"]["reads"][read] = {
            "students_total": "{:,}".format(int(round(s1["students_total"]))),
            "minus_golden_region": {WD.REGION_NAME[r]: "%+.1f" % (s1["students_region"][r] - figs["students_region"][r])
                                    for r in CO.REGIONS},
            "minus_golden_region_pct": {WD.REGION_NAME[r]: "%+.1f" % (100 * (s1["students_region"][r] -
                                        figs["students_region"][r]) / figs["students_region"][r]) for r in CO.REGIONS},
            "minus_golden_hub": {hubs[h]: "%+.1f" % (s1["students_hub"][h] - figs["students_hub"][h]) for h in AK.HUBS},
            "minus_golden_total": "%+.1f" % (s1["students_total"] - figs["students_total"])}
    fj["contrasts"]["primary_schools"] = int(fd["n"].shape[0])
    f = fd["fit"]
    fj["contrasts"]["components_sd"] = {"school": "%.1f" % f["tu"] ** 0.5, "year_group": "%.1f" % f["tv"] ** 0.5,
                                        "student": "%.1f" % f["s2"] ** 0.5, "mean": "%.1f" % f["beta"][0]}
    # how far each golden-method variant moves the ask figures (all but REML at the fitted values are ruled
    # out by filed text: ML by 3.2, a sitting effect by 2.2, a residual per school by 3.1, the rest by 3.4)
    spread = {}
    for k, q in fam_probs.items():
        if k == "reml":
            continue
        a = AN.asks(W, q, points)
        spread[k] = {
            "students_region": "%.1f" % max(abs(a["students_region"][r] - figs["students_region"][r]) for r in a["shares"]),
            "students_hub": "%.1f" % max(abs(a["students_hub"][h] - figs["students_hub"][h]) for h in a["km_hub"]),
            "km_hub": "%.1f" % max(abs(a["km_hub"][h] - figs["km_hub"][h]) for h in a["km_hub"]),
            "shares": "%.2f" % max(abs(a["shares"][r] - figs["shares"][r]) for r in a["shares"])}
    fj["variant_ask_shift_max"] = spread
    with open(os.path.join(HERE, "figures.json"), "w") as fh:
        json.dump(fj, fh, indent=1)
        fh.write("\n")
    n, cells = C.run(W, tables, fd, figs, grid, fam, fam_probs, st, TARGET, TASK, docs_text())
    print("checks: %d assertions green (%d composition cells)" % (n, cells))
    # independent verifier
    v = V.run(TARGET)
    inv = {WD.REGION_NAME[r]: r for r in WD.REGION_NAME}
    hinv = {hubs[h]: h for h in hubs}
    assert v["places"] == figs["places"] and abs(v["places_exact"] - figs["places_exact"]) < 1e-5
    for k in ("tu", "tv", "s2"):
        assert abs(v["components"][k] - f[k]) / f[k] < 1e-6, (k, v["components"][k], f[k])
    for rn, x in v["shares"].items():
        assert round(x, 1) == round(figs["shares"][inv[rn]], 1)
    for rn, x in v["students_region"].items():
        assert round(x) == round(figs["students_region"][inv[rn]])
    for hn, x in v["students_hub"].items():
        assert round(x) == round(figs["students_hub"][hinv[hn]])
    for hn, x in v["km_hub"].items():
        assert round(x) == round(figs["km_hub"][hinv[hn]])
    assert round(v["students_total"]) == round(figs["students_total"]) and round(v["km_total"]) == round(figs["km_total"])
    assert [hinv[h] for h in v["chart_order"]] == figs["chart_order"]
    assert v["rolled"] == int(W["rolled"].sum())
    print("verifier: green (REML by EM, %d iterations)" % v["components"]["em_iterations"])
    # second build, byte for byte
    if "--once" not in sys.argv:
        tmp = tempfile.mkdtemp(dir=os.path.join(TASK, "..", ".work", "notes", "agent-scratch")
                               if os.path.isdir(os.path.join(TASK, "..", ".work")) else None)
        t2, g2 = os.path.join(tmp, "target"), os.path.join(tmp, "golden")
        write_all(t2, g2)
        for a, b in ((TARGET, t2), (GOLDEN, g2)):
            fa, fb = sorted(os.listdir(a)), sorted(os.listdir(b))
            assert fa == fb
            for x in fa:
                assert filecmp.cmp(os.path.join(a, x), os.path.join(b, x), shallow=False), x
        shutil.rmtree(tmp)
        print("second build: byte-identical (%d pack files, %d goldens)" % (len(os.listdir(TARGET)),
                                                                          len(os.listdir(GOLDEN))))
    # target.zip
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for x in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo(x, date_time=(2026, 11, 10, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, open(os.path.join(TARGET, x), "rb").read())
    print("target.zip cut")


if __name__ == "__main__":
    main()
