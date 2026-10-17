"""Cut the bundle, compute the goldens from it, write figures.json, then check and verify."""
import datetime as dt
import os
import shutil
import sys
import time

import deliver as DL
import docs
import figures as FG
import golden as G
import metadata as MD
import pack as PK
import postprocess as PP
import sim
import world as W

EXPORT_STAMP = dt.datetime(2027, 3, 5, 17, 40, 0)


def cut(target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    design = sim.design_ratios(W.UNITS)
    rows, expected, inscope = sim.episodes(W.UNITS)
    allsep = {}
    for r in rows:
        allsep[(r["unit"], r["q"])] = allsep.get((r["unit"], r["q"]), 0) + 1
    targets = sim.record_targets(expected, allsep, design, W.UNITS)
    observed = sim.assign_complications(rows, expected, design, W.UNITS, targets)
    detail = sim.complications(rows, W.UNITS)
    replays = sim.add_replays(rows, W.UNITS)
    allrows = PK.write_extract(target, rows, replays)
    PK.write_detail(target, rows, detail)
    PK.write_series(target, expected, observed, inscope)
    PK.write_summary(target, rows)
    PK.write_plan(target)
    PK.write_units(target)
    PK.write_sites(target)
    PK.write_bands(target)
    PK.write_strata(target)
    PK.write_catlist(target)
    PK.write_placements(target)
    PK.write_dashboard(target, expected, observed, inscope, rows)
    PK.write_distractors(target)
    PK.write_dictionary(target)
    docs.charter(target)
    docs.specification(target)
    docs.thread(target)
    PK.write_manifest(target)
    PP.normalize_pdf(os.path.join(target, "improvement_partnership_charter_v3.pdf"),
                     b"D:20240617093000+11'00'", b"D:20240617093000+11'00'")
    PP.normalize_pdf(os.path.join(target, "hac_indicator_specification_v4.pdf"),
                     b"D:20240624141500+11'00'", b"D:20240624141500+11'00'")
    PP.normalize_ooxml(os.path.join(target, PK.FILES["dashboard"]), "Nicholas Fields", "Nicholas Fields",
                       "2027-03-05T06:12:00Z", "2027-03-05T06:40:00Z",
                       title="Inpatient quality indicators, quarter ended 31 December 2026", excel=True)
    stamp = time.mktime(EXPORT_STAMP.timetuple())
    for name in sorted(os.listdir(target)):
        os.utime(os.path.join(target, name), (stamp, stamp))
    return dict(rows=rows, allrows=allrows, expected=expected, observed=observed, inscope=inscope,
                allsep=allsep, detail=detail, replays=replays, design=design, targets=targets)


def zip_pack(target, path):
    """target.zip from the cut bundle: entries sorted, one fixed timestamp, deflated, so the archive is a
    function of the bundle's bytes and nothing else."""
    import zipfile
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(os.listdir(target)):
            info = zipfile.ZipInfo("target/" + name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(os.path.join(target, name), "rb") as fh:
                z.writestr(info, fh.read())
    return path


if __name__ == "__main__":
    task = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gendir = os.path.dirname(os.path.abspath(__file__))
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(task, "target")
    state = cut(tgt)
    g = G.compute(tgt)
    gold = os.path.join(task, "golden")
    os.makedirs(gold, exist_ok=True)
    chart_png = os.path.join(gendir, "_chart.png")
    DL.chart(chart_png, g)
    DL.workbook(os.path.join(gold, "embed_placement_2027q4.xlsx"), g)
    DL.brief(os.path.join(gold, "embed_placement_brief.pdf"), g, chart_png)
    PP.normalize_ooxml(os.path.join(gold, "embed_placement_2027q4.xlsx"), "Katherine Klein",
                       "Katherine Klein", "2027-03-17T23:15:00Z", "2027-03-18T04:05:00Z",
                       title="Cycle IP-09 placement", excel=True)
    PP.normalize_pdf(os.path.join(gold, "embed_placement_brief.pdf"),
                     b"D:20270318151000+11'00'", b"D:20270318151000+11'00'")
    MD.write(task, g)
    FG.write(gendir, g)
    import checks as CK
    import verify as VF
    n = CK.run(tgt, g, state)
    k = VF.run(tgt, os.path.join(gendir, "figures.json"))
    print("generator assertions", n, "independent checks", k)
    print("call    : %s %s, %d avoided" % (g["answer"]["unit"], g["answer"]["name"],
                                           round(g["answer"]["avoided"])))
    print("closest : %s %s, %d avoided, gap %d, margin %.3fx" % (
        g["runner"]["unit"], g["runner"]["name"], round(g["runner"]["avoided"]), g["gap"], g["margin"]))
    print("share   : %.4f of a unit's standing excess, over %d closed placements"
          % (g["share"], len(g["record"])))
    print("rung 0  : %s files %d avoided, rung 1 %s, rung 2 %s" % (
        g["rung0"]["unit"], round(g["share"] * g["rung0"]["last_excess"]), g["rung1"]["unit"],
        g["rung2"]["unit"]))
    if tgt == os.path.join(task, "target"):
        zip_pack(tgt, os.path.join(task, "target.zip"))
        print("zip     : %s" % os.path.join(task, "target.zip"))
