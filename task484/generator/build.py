"""Builds task484's pack into target/ and the golden deliverables into golden/, writes generator/figures.json, and
cuts target.zip; two runs are byte-identical.

    python3 task484/generator/build.py
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

NAMES = dict(registry="solid_fuel_device_registry_2026-05-15.csv", zones="burn_zone_parcels_2025.csv",
             scc="device_code_scc_crosswalk.csv", survey="heating_survey_2024_25_responses.csv",
             survey_methods="heating_survey_2024_25_methods.pdf", d1_acct="wapiti_propane_accounts.csv",
             d1_tickets="wapiti_propane_tickets_2023-07_2026-06.csv",
             d2_export="coldwater_activity_export_2023-07_2026-06.txt", d2_layout="coldwater_export_record_layout.txt",
             d3="halvard_coop_propane_by_month_2023_2026.xlsx", temps="khlv_daily_temperatures_2023-07_2026-06.csv",
             fuel="heating_fuel_equivalents.csv", factors="emission_factors_2023.csv",
             plan="maintenance_plan_chapter4_rwc.pdf", tool="montana_rwc_tool_documentation_2023.pdf",
             acs1923="acs5_2019_2023_b25040_halvard_bg.csv", acs2024="acs5_2020_2024_b25040_halvard_bg.csv",
             assessor="assessor_housing_units_by_block_group_2025.csv",
             relationship="tab2020_tab2010_bg_relationship_halvard.csv",
             curtail="burn_curtailment_calls_2023_2026.csv", permits="forest_firewood_permits_2019_2025.csv")
GOLD = dict(inventory="rwc_inventory_2025_26.xlsx", determinations="zone_determinations_2026_27.csv")


def t(k):
    return os.path.join(TARGET, NAMES[k])


def gpath(k):
    return os.path.join(GOLDEN, GOLD[k])


def pack():
    for d in (TARGET, GOLDEN):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    homes, devices = W.build()
    temps = W.temperatures()
    acc = W.accounts(homes, temps)
    tk = W.tickets(acc, temps)
    resp = W.survey(devices)
    rem = W.remainder()
    P.registry_csv(t("registry"), devices)
    P.zone_parcels_csv(t("zones"), homes, acc)
    P.scc_csv(t("scc"))
    P.survey_csv(t("survey"), resp)
    P.wapiti(dict(acct=t("d1_acct"), tickets=t("d1_tickets")), acc, tk)
    P.coldwater(dict(export=t("d2_export"), layout=t("d2_layout")), acc, tk)
    P.cooperative(t("d3"), acc, tk)
    P.temperatures_csv(t("temps"), temps)
    P.fuel_equivalents_csv(t("fuel"))
    P.factors_csv(t("factors"))
    P.acs_csv(t("acs1923"), rem, "1923")
    P.acs_csv(t("acs2024"), rem, "2024")
    P.assessor_csv(t("assessor"), rem)
    P.relationship_csv(t("relationship"), rem)
    P.distractor_csvs(dict(curtail=t("curtail"), permits=t("permits")), temps)
    D.plan_pdf(t("plan"))
    D.survey_methods_pdf(t("survey_methods"))
    D.tool_pdf(t("tool"))
    PP.normalize_ooxml(t("d3"), "Propane Division", "Propane Division", "2026-07-06T15:12:00Z", "2026-07-08T19:41:00Z",
                       excel=True, company=P.D3_NAME)
    for k, stamp in (("plan", b"D:20230314100000-06'00'"), ("survey_methods", b"D:20250819090000-06'00'"),
                     ("tool", b"D:20231116090000-07'00'")):
        PP.normalize_pdf(t(k), stamp, stamp)
    return dict(homes=homes, devices=devices, temps=temps, acc=acc, tk=tk, resp=resp, rem=rem)


def main():
    world = pack()
    import golden as G
    import goldfiles as GF
    p = G.load(TARGET)
    figs = GF.write(gpath, p)
    PP.normalize_ooxml(gpath("inventory"), W.PEOPLE["inventory"], W.PEOPLE["lead"], "2026-07-21T16:00:00Z",
                       "2026-07-27T21:40:00Z", excel=True, company=W.PROGRAM)
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
            zi = zipfile.ZipInfo(n, date_time=(2026, 7, 28, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, n), "rb").read())


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "pack":
        pack()
    else:
        main()
