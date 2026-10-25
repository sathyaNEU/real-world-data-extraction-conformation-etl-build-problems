"""Builds task485's pack into target/ and the golden deliverables into golden/, writes generator/figures.json, and
cuts target.zip; two runs are byte-identical.

    python3 task485/generator/build.py          # the whole build
    python3 task485/generator/build.py pack     # the pack only
"""
import json
import os
import shutil
import sys
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
sys.path.insert(0, HERE)

import contractors as C    # noqa: E402
import golden as G         # noqa: E402
import registry as R       # noqa: E402
import world as W          # noqa: E402

NAMES = dict(
    animals="nbr_animals_2025-26.csv", movements="nbr_movements_2025-26.csv", herds="nbr_herd_register_2026-11.xlsx",
    notes="nbr_export_notes.txt", census="nso_june_livestock_census_2026.csv",
    census_pdf="nso_june_livestock_census_2026_tables.pdf", epo="epo_cattle_ammonia_factors_2025.pdf",
    survey="moa_livestock_housing_survey_2025.xlsx", arp="arp_designation_rules_2025.pdf",
    lpr="lpr_farmed_area_2026.csv", ardvale="vale_agri_jobs_2026.csv", kilbrack="countrywide_invoice_lines_2026.xlsx",
    northmoor="basin_agri_job_sheets_2026.xlsx", fert="moa_fertiliser_sales_by_region_2025-26.csv",
    milk="creamery_milk_intake_by_region_2025.csv", pigs="nso_pig_poultry_census_2026.csv")
GOLD = dict(workbook="ammonia_action_regions_2027.xlsx", chart="cattle_ammonia_per_hectare_2025-26.png")
DEPT = "Ministry of Agriculture"
OWNERS = {
    "herds": dict(creator="NBR Data Management", last_by="Noel Herity", created="2019-03-04T09:41:00Z",
                  modified="2026-11-09T06:14:00Z", company=DEPT),
    "survey": dict(creator="Livestock Surveys Unit", last_by="Livestock Surveys Unit", created="2025-06-02T10:05:00Z",
                   modified="2025-07-14T15:22:00Z", company=DEPT),
    "kilbrack": dict(creator="Countrywide Slurry Services", last_by="Accounts", created="2026-11-03T11:48:00Z",
                     modified="2026-11-03T11:52:00Z", company="Countrywide Slurry Services Ltd"),
    "northmoor": dict(creator="Basin Agri", last_by="Office", created="2026-01-12T08:30:00Z",
                      modified="2026-11-04T17:06:00Z", company="Basin Agri"),
}


def t(k):
    return os.path.join(TARGET, NAMES[k])


def truth():
    """the clean truth: the world, its identity layer, every animal's herd intervals, the golden ammonia, farmed land,
    the census and the contractors' jobs"""
    w = W.build(W.SEED)
    rng = np.random.default_rng(W.SEED + 1)
    moved = R.assign(w, rng)
    R.second_herds(w, rng)
    old = R.reissued(w, rng)
    bherd = R.birth_herds(w, rng)
    tags = R.tags(w, rng, bherd)
    IV = W.intervals(w.A, w.moves)
    T = G.Truth(w.A)
    hr = np.array([G.REGI[h["region"]] for h in w.herds])
    ivs = G.iv_arrays(IV)
    P = G.Pieces(T, ivs, hr)
    gold = G.ammonia(P)
    parcels = R.land(w, IV, G.by_region(gold), rng)
    cen = R.census(w, IV)
    cj = C.jobs(w, IV, np.random.default_rng(W.SEED + 2))
    herd_region = {h["herd_no"]: h["region"] for h in w.herds}
    land = G.farmed_land(parcels, herd_region)
    return dict(w=w, moved=moved, old=old, bherd=bherd, tags=tags, IV=IV, T=T, hr=hr, ivs=ivs, P=P, gold=gold,
                parcels=parcels, cen=cen, cj=cj, herd_region=herd_region, land=land)


def pack(tr=None):
    import docs as DOC
    import pack as PK
    import postprocess as PP
    for d in (TARGET, GOLDEN):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    tr = tr or truth()
    w = tr["w"]
    rng = np.random.default_rng(W.SEED + 3)
    n = {}
    n["animals"] = PK.animals(t("animals"), w, tr["IV"], tr["tags"], tr["bherd"])
    n["movements"] = PK.movements(t("movements"), w, tr["tags"], rng)
    n["herds"] = PK.herd_register(t("herds"), w, tr["old"], rng)
    PK.export_notes(t("notes"))
    n["census"] = PK.census_csv(t("census"), w, tr["cen"])
    n["lpr"] = PK.lpr(t("lpr"), tr["parcels"])
    PK.survey(t("survey"), w, rng)
    n["ardvale"] = PK.ardvale(t("ardvale"), tr["cj"])
    n["kilbrack"] = PK.kilbrack(t("kilbrack"), tr["cj"])
    n["northmoor"] = PK.northmoor(t("northmoor"), tr["cj"])
    n["fert"] = PK.fertiliser(t("fert"), tr["land"], rng)
    n["milk"] = PK.milk(t("milk"), w, rng)
    n["pigs"] = PK.pigs_poultry(t("pigs"), rng)
    DOC.epo_pdf(t("epo"))
    DOC.arp_pdf(t("arp"))
    DOC.census_pdf(t("census_pdf"), w, tr["cen"])
    for k in ("herds", "survey", "kilbrack", "northmoor"):
        PP.normalize_ooxml(t(k), excel=True, **OWNERS[k])
    for k, stamp in (("epo", DOC.STAMPS["epo"]), ("arp", DOC.STAMPS["arp"]), ("census_pdf", DOC.STAMPS["census"])):
        PP.normalize_pdf(t(k), stamp, stamp)
    return tr, n


def gpath(k):
    return os.path.join(GOLDEN, GOLD[k])


def main():
    tr, n = pack()
    import goldfiles as GF
    import postprocess as PP
    figs = GF.write(gpath, tr)
    PP.normalize_ooxml(gpath("workbook"), "Emily McAleer", "Emily McAleer", "2026-11-12T09:26:00Z",
                       "2026-11-18T16:41:00Z", title="Ammonia Action Regions 2027: the Unit's figures", excel=True,
                       company=DEPT)
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    import writeup
    writeup.main()
    import metadata
    metadata.main()
    cut_zip()
    print("built: %d files in target/, %d in golden/" % (len(os.listdir(TARGET)), len(os.listdir(GOLDEN))))
    print(json.dumps(n))
    return tr


def cut_zip():
    """Each file keeps the date its source produced it (metadata.SOURCES) and a working-hours time of its own."""
    import hashlib
    import metadata
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for nm in sorted(os.listdir(TARGET)):
            y, mo, d = (int(x) for x in metadata.SOURCES[nm][1].split("-"))
            h = int(hashlib.md5(nm.encode()).hexdigest(), 16)
            zi = zipfile.ZipInfo(nm, date_time=(y, mo, d, 7 + h % 11, (h // 11) % 60, ((h // 660) % 30) * 2))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, nm), "rb").read())


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "pack":
        tr, n = pack()
        print(json.dumps(n, indent=1))
    else:
        main()
