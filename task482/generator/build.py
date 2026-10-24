"""Builds task482's pack into target/ and the golden deliverables into golden/, writes generator/figures.json, and
cuts target.zip; two runs are byte-identical.

    python3 task482/generator/build.py
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

import world as W          # noqa: E402
import pack as P           # noqa: E402
import docs as D           # noqa: E402
import postprocess as PP   # noqa: E402

NAMES = dict(residents="quillmere_county_population_estimates_2024_2026.csv",
             edmr="edmr_dmr_export_quillmere_basin_2025-01_2026-09.csv",
             ponds="ruddmere_pinehold_ponds_operating_reports_2025_2026.xlsx",
             meters="narrows_joint_member_meters_2025_2026.csv",
             params="edmr_parameter_codes.csv",
             facilities="quillmere_basin_wastewater_facilities.pdf",
             returns="lake_protection_fee_returns_2025-07_2026-09.csv",
             returns_layout="lake_protection_fee_returns_field_list.txt",
             lakeward="lakeward_stays_remittance_detail_2025-07_2026-09.csv",
             kettlepine="kettle_and_pine_remittance_report_2025-07_2026-09.csv",
             statute="seasonal_communities_aid_act.pdf",
             ordinance="lake_protection_fee_ordinance.pdf",
             traffic="quillmere_county_traffic_counts_2024_2026.csv",
             weather="sorrelton_coop_station_daily_2025_2026.csv")
GOLD = dict(workbook="seasonal_communities_aid_2027_certification.xlsx", chart="busiest_month_population_2026.png")


def t(k):
    return os.path.join(TARGET, NAMES[k])


def gpath(k):
    return os.path.join(GOLDEN, GOLD[k])


def pack():
    for d in (TARGET, GOLDEN):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    w = W.build()
    mor, meters = W.mor()
    P.residents_csv(t("residents"))
    P.edmr_csv(t("edmr"), mor)
    P.ponds_xlsx(t("ponds"), mor)
    P.meters_csv(t("meters"), meters)
    P.parameter_codes_csv(t("params"))
    P.returns_csv(t("returns"), w["props"], w["lodge_nights"])
    P.returns_layout_txt(t("returns_layout"))
    P.lakeward_csv(t("lakeward"), w["listings"], w["bookings"])
    P.kettlepine_csv(t("kettlepine"), w["listings"], w["bookings"])
    P.traffic_csv(t("traffic"))
    P.weather_csv(t("weather"))
    D.statute_pdf(t("statute"))
    D.ordinance_pdf(t("ordinance"))
    D.facilities_pdf(t("facilities"))
    PP.normalize_ooxml(t("ponds"), "Northwoods Utility Services", "Northwoods Utility Services", "2025-02-11T14:20:00Z",
                       "2026-10-09T16:05:00Z", excel=True, company="Northwoods Utility Services")
    for k, stamp in (("statute", b"D:20251104090000-06'00'"), ("ordinance", b"D:20250612100000-05'00'"),
                     ("facilities", b"D:20260317110000-05'00'")):
        PP.normalize_pdf(t(k), stamp, stamp)
    return dict(world=w, mor=mor, meters=meters)


def main():
    world = pack()
    import golden as G
    import goldfiles as GF
    p = G.load(TARGET)
    figs = GF.write(gpath, p)
    PP.normalize_ooxml(gpath("workbook"), W.PEOPLE["estimates"], W.PEOPLE["lead"], "2026-10-26T15:10:00Z",
                       "2026-11-18T20:42:00Z", excel=True, company=W.OFFICE)
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    import writeup
    writeup.main()
    import metadata
    metadata.main()
    cut_zip()
    print("built: %d files in target/, %d in golden/" % (len(os.listdir(TARGET)), len(os.listdir(GOLDEN))))
    return world


def cut_zip():
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for n in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo(n, date_time=(2026, 10, 19, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, n), "rb").read())


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "pack":
        pack()
    else:
        main()
