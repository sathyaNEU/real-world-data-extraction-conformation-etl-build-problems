"""Builds task484's pack into target/ and the golden deliverables into golden/, writes generator/figures.json, and
cuts target.zip; two runs are byte-identical.

    python3 task484/generator/build.py
"""
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
sys.path.insert(0, HERE)

import world as W          # noqa: E402
import pack as P           # noqa: E402
import golden as G         # noqa: E402
import goldfiles as GF     # noqa: E402
import postprocess as PP   # noqa: E402

NAMES = dict(registry="wood_device_registry_2026-06-30.csv", survey="household_wood_survey_2024_25.csv",
             apps="changeout_applications_2015_2025.csv", plan="maintenance_plan_rwc_base_year_2014.xlsx",
             provision="contingency_provisions_rwc.pdf", methods="rwc_inventory_methods_appendix_2025_26.pdf",
             factors="emission_factors_rwc_2023.csv", scc="scc_crosswalk_rwc.csv", parcels="parcel_area_crosswalk.csv",
             acs1923="acs_b25040_blockgroups_2019_2023.csv", acs2024="acs_b25040_blockgroups_2020_2024.csv",
             assessor="assessor_housing_units_by_block_group_2025.csv", tool="state_rwc_tool_method_note.pdf",
             relationship="census_bg2020_bg2010_relationship_wa.csv",
             hdd="heating_degree_days_2025_26.csv", curtail="curtailment_log_2025_26.csv",
             monitor="pm25_monitor_daily_2025_26.csv", permits="firewood_permits_by_district.csv")
GOLD = dict(inventory="rwc_periodic_inventory_2025_26.xlsx", determinations="contingency_determinations_2026_27.csv")


def t(k):
    return os.path.join(TARGET, NAMES[k])


def gpath(k):
    return os.path.join(GOLDEN, GOLD[k])


def main():
    for d in (TARGET, GOLDEN):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    devs, apps = W.build()
    resp = W.survey(devs)
    rem = W.remainder()
    ev = G.evaluate(devs, apps, resp)
    aa, ab = G.ask_a(devs), G.ask_b(rem)
    P.registry_csv(t("registry"), devs)
    P.survey_csv(t("survey"), resp)
    P.applications_csv(t("apps"), apps, devs)
    P.plan_workbook(t("plan"), [(c, ev[c]["county"], cl, ev[c]["cls"][cl]["n14"]) for c in W.CODES for cl in W.CL])
    P.provision_pdf(t("provision"))
    P.methods_pdf(t("methods"))
    P.tool_pdf(t("tool"))
    P.factors_csv(t("factors"))
    P.scc_crosswalk_csv(t("scc"))
    P.crosswalk_csv(t("parcels"), devs)
    P.acs_csv(t("acs1923"), rem, "1923")
    P.acs_csv(t("acs2024"), rem, "2024")
    P.assessor_csv(t("assessor"), rem)
    P.relationship_csv(t("relationship"), rem)
    P.distractor_csvs(t, devs)
    figs = GF.write(gpath, ev, aa, ab)
    PP.normalize_ooxml(t("plan"), W.PEOPLE["inventory"], W.PEOPLE["inventory"], "2016-11-18T17:20:00Z",
                       "2016-11-21T22:05:00Z", excel=True)
    PP.normalize_ooxml(gpath("inventory"), W.PEOPLE["inventory"], W.PEOPLE["inventory"], "2026-07-20T16:00:00Z",
                       "2026-07-24T21:40:00Z", excel=True)
    for k, stamp in (("provision", b"D:20161209100000-08'00'"), ("methods", b"D:20260715090000-07'00'"),
                     ("tool", b"D:20231102090000-07'00'")):
        PP.normalize_pdf(t(k), stamp, stamp)
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    import writeup
    writeup.main()
    cut_zip()
    print("built: %d files in target/, %d in golden/" % (len(os.listdir(TARGET)), len(os.listdir(GOLDEN))))
    return 0


def cut_zip():
    import zipfile
    path = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(path, "w") as z:
        for name in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo(name, date_time=(2026, 7, 24, 16, 30, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(TARGET, name), "rb") as f:
                z.writestr(zi, f.read())


if __name__ == "__main__":
    raise SystemExit(main())
