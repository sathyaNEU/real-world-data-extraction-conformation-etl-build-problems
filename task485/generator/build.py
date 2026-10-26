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

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
sys.path.insert(0, HERE)

import pack_read as PR    # noqa: E402
import world as W         # noqa: E402

NAMES = dict(extract=PR.EXTRACT, archive=PR.ARCHIVE, crosswalk=PR.XWALK, sectors=PR.SECTORS,
             parishes="parish_codes.csv", policy="population_policy_2024_2028_sector_allowances.pdf",
             methods="long_term_migration_methods_2026.pdf", spec="population_register_extract_specification.pdf",
             published="long_term_immigration_by_sector_2023_24.xlsx",
             passengers="port_passenger_movements_2024_2026.xlsx", census="census_2021_population_by_parish.xlsx")
GOLD = dict(workbook="provisional_long_term_immigration_2025_26.xlsx", chart="long_term_immigration_by_sector_2025_26.png")
UNIT = "Esklett Statistics Unit"
OWNERS = {
    "published": dict(creator="Migration Statistics", last_by="Migration Statistics", created="2025-10-06T09:41:00Z",
                      modified="2025-10-15T16:12:00Z", company=UNIT),
    "passengers": dict(creator="Ports Authority", last_by="Statistics Desk", created="2024-02-07T10:15:00Z",
                       modified="2026-09-09T08:57:00Z", company="Esklett Ports Authority"),
    "census": dict(creator="Census Team", last_by="Census Team", created="2022-05-23T13:30:00Z",
                   modified="2022-06-29T11:04:00Z", company=UNIT),
}
STAMPS = {"policy": b"D:20240409100000+00'00'", "methods": b"D:20260901093000+00'00'",
          "spec": b"D:20260901141500+00'00'"}


def t(k):
    return os.path.join(TARGET, NAMES[k])


def pack():
    import docs as DOC
    import pack as PK
    import postprocess as PP
    for d in (TARGET, GOLDEN):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    w = W.build()
    n = PK.register_files({k: t(k) for k in ("extract", "archive", "crosswalk")}, w)
    n["sectors"] = PK.sector_json(t("sectors"))
    n["parishes"] = PK.parish_csv(t("parishes"))
    PK.published_2023_24(t("published"), w)
    n["passengers"] = PK.passengers(t("passengers"))
    n["census"] = PK.census_2021(t("census"))
    DOC.policy(t("policy"))
    DOC.methods(t("methods"))
    DOC.specification(t("spec"))
    for k in OWNERS:
        PP.normalize_ooxml(t(k), excel=True, **OWNERS[k])
    for k, stamp in STAMPS.items():
        PP.normalize_pdf(t(k), stamp, stamp)
    return w, n


def gpath(k):
    return os.path.join(GOLDEN, GOLD[k])


def main():
    w, n = pack()
    import goldfiles as GF
    import postprocess as PP
    figs = GF.write(gpath)
    PP.normalize_ooxml(gpath("workbook"), "Jean Grant", "Jean Grant", "2026-10-05T08:52:00Z", "2026-10-07T16:38:00Z",
                       title="Provisional long-term immigration by employment sector, year to 30 June 2026",
                       excel=True, company=UNIT)
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    import writeup
    writeup.main()
    import metadata
    metadata.main()
    cut_zip()
    print("built: %d files in target/, %d in golden/" % (len(os.listdir(TARGET)), len(os.listdir(GOLDEN))))
    print(json.dumps(n))
    return w


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
        w, n = pack()
        print(json.dumps(n, indent=1))
    else:
        main()
