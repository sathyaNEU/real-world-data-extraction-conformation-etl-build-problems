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

import world as W          # noqa: E402
import alterations as AL   # noqa: E402
import geo as G            # noqa: E402
import pack as P           # noqa: E402
import docs as DOC         # noqa: E402

NAMES = dict(
    ems_new="ems_property_electorate_2022-2025.csv", ems_2020="ELECTRA_PROPERTY_ELECTORATE_REV_2020.txt",
    ems_2021="ELECTRA_PROPERTY_ELECTORATE_REV_2021.txt", xref="ems_migration_property_xref_2022-03.csv",
    llpg="llpg_extract_2026-10-12.csv", completions="housing_completions_monitoring_2014-2026.xlsx",
    trajectory="housing_trajectory_2026-09-30.xlsx", pd="polling_district_review_2023_schedule.csv",
    wards="wards_councillors_2014_order.csv", notices="ELECTRA_NOTICES_OF_ALTERATION_2021-01_2022-03.txt",
    proj="snpp_2022based_lorrimere.csv", ctax="council_tax_dwellings_by_band_ward_2025-09.csv",
    guide="lorrimere_review_data_notes.txt", guidance="lgbc_electorate_forecast_guidance_2024.pdf",
    canvass="lorrimere_annual_canvass_report_2025.pdf")
GOLD = dict(workbook="ward_electorate_forecast_2032.xlsx", chart="ward_variance_2032.png")


def t(k):
    return os.path.join(TARGET, NAMES[k])


def pack():
    for d in (TARGET, GOLDEN):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    w = W.build()
    g = G.build(w)
    P.attach(w, g)
    meta = P.site_meta(w, g)
    ev = AL.events(w)
    idx = AL.by_dwelling(ev)
    w["events"], w["event_index"] = ev, idx
    n = {}
    n["ems_new"] = P.ems_new(t("ems_new"), w)
    n["ems_2020"] = P.ems_old(t("ems_2020"), w, 2020, run="04/03/2022 17:47")
    n["ems_2021"] = P.ems_old(t("ems_2021"), w, 2021, idx=idx)
    n["notices"] = P.electra_notices(t("notices"), w, ev)
    n["xref"] = P.xref(t("xref"), w)
    n["llpg"], parish = P.llpg(t("llpg"), w, g)
    n["completions"] = P.completions(t("completions"), w, meta)
    n["trajectory"] = P.trajectory(t("trajectory"), w, meta)
    n["pd"] = P.pd_schedule(t("pd"), w, g)
    n["wards"] = P.wards_file(t("wards"), g)
    n["proj"] = P.projections(t("proj"), w)
    n["ctax"] = P.council_tax(t("ctax"), w)
    P.field_guide(t("guide"), NAMES)
    dw = w["dwellings"]
    Y = W.LAST_SHIP
    onreg = [d for d in dw if d["inuse"] is None or d["inuse"] <= W.mindex(Y, 10)]
    r3 = int(round(0.0046 * len(onreg)))
    r1 = int(round(0.784 * len(onreg)))
    stats = dict(props=len(onreg), r1=r1, r3=r3, r2=len(onreg) - r1 - r3, resp=71.6,
                 lg=sum(d["count"][Y] for d in onreg), att=sum(d["attainers"][Y] for d in onreg),
                 ov=sum(d["overseas"].get(Y, 0) for d in onreg))
    DOC.guidance_pdf(t("guidance"))
    DOC.canvass_pdf(t("canvass"), stats)
    import postprocess as PP
    for k in ("completions", "trajectory"):
        PP.normalize_ooxml(t(k), excel=True, **PP.OWNERS[k])
    for k, stamp in DOC.STAMPS.items():
        PP.normalize_pdf(t(k), stamp, stamp)
    return w, g, meta, n


def gpath(k):
    return os.path.join(GOLDEN, GOLD[k])


def main():
    built = pack()
    import goldfiles as GF
    import postprocess as PP
    figs = GF.write(gpath, TARGET)
    PP.normalize_ooxml(gpath("workbook"), "Megan Stewart", "Megan Stewart", "2026-10-26T09:12:00Z", "2026-10-28T16:47:00Z",
                       title="Lorrimere electoral review: electorate forecast 2032", excel=True,
                       company="Local Government Boundary Commission")
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    import writeup
    writeup.main()
    import metadata
    metadata.main()
    cut_zip()
    print("built: %d files in target/, %d in golden/" % (len(os.listdir(TARGET)), len(os.listdir(GOLDEN))))
    return built


def cut_zip():
    """Each file keeps the date its source produced it (metadata.SOURCES) and a working-hours time of its own."""
    import hashlib
    import metadata
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for n in sorted(os.listdir(TARGET)):
            y, mo, d = (int(x) for x in metadata.SOURCES[n][1].split("-"))
            h = int(hashlib.md5(n.encode()).hexdigest(), 16)
            zi = zipfile.ZipInfo(n, date_time=(y, mo, d, 7 + h % 11, (h // 11) % 60, ((h // 660) % 30) * 2))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, n), "rb").read())


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "pack":
        w, g, meta, n = pack()
        print(json.dumps(n, indent=1))
    else:
        main()
