"""Cut the bundle, compute the goldens, write figures.json and run every check."""
import os
import shutil
import sys

import asks as AS
import docs as DC
import pack as PK
import sim
import world as W


def cut(target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    specimens = sim.build()
    counts = {}
    counts["qc"] = PK.write_qc(target, specimens)
    counts["mf"] = PK.write_mf(target, specimens)
    panel = PK.write_panel(target, specimens)
    counts["panel"] = len(panel)
    PK.write_crosswalk(target, specimens)
    counts["crosswalk"] = len(specimens)
    PK.write_plates(target, specimens)
    counts["plates"] = len(specimens)
    PK.write_config(target)
    PK.write_dictionary(target)
    hist_rows, released, flagged = AS.history(target)
    counts["history"] = hist_rows
    counts["volumes"] = AS.volumes(target, released)
    AS.dilution(target)
    counts["runlog"] = AS.run_log(target, specimens)
    counts["costs"] = AS.costs(target)
    for key, inst in (("qc_a", W.INSTRUMENTS[0]), ("qc_b", W.INSTRUMENTS[1])):
        with open(os.path.join(target, W.FILES[key]), encoding="utf-8") as fh:
            counts[key] = sum(1 for _ in fh) - 1
    DC.protocol(target)
    estimates = [rs["estimate"] for s in specimens for rs in s["read_sets"] if rs["accepted"]]
    DC.model_card(target, estimates)
    DC.weekly_reports(target, panel)
    DC.platform(target)
    PK.write_manifest(target, counts)
    return specimens, counts


def stamp(target):
    """Containers carry the fiction's own producer and date, never the writer's."""
    import postprocess as PP
    for name, created, modified in (
            (W.FILES["protocol"], b"D:20270219091500+01'00'", b"D:20270219091500+01'00'"),
            (W.FILES["modelcard"], b"D:20270611143000+02'00'", b"D:20270611143000+02'00'"),
            (W.FILES["weekly"], b"D:20270604161000+02'00'", b"D:20270604161000+02'00'"),
            (W.FILES["platform"], b"D:20251120103000+01'00'", b"D:20251120103000+01'00'")):
        PP.normalize_pdf(os.path.join(target, name), created, modified)
    PP.normalize_ooxml(os.path.join(target, W.FILES["dilution"]), W.PEOPLE["lead"],
                       W.PEOPLE["lead"], "2027-03-11T08:40:00Z", "2027-04-02T10:15:00Z",
                       title="Analytical sensitivity panel 2027Q1", excel=True)

def stamp_golden(path):
    """The validation file the screening lead saved, with the laboratory's own producer and dates."""
    import postprocess as PP
    PP.normalize_ooxml(path, W.PEOPLE["lead"], W.PEOPLE["quality"],
                       "2027-06-19T07:55:00Z", "2027-06-21T15:20:00Z",
                       title="Contamination screen change, 2027Q3", excel=True)


def mtimes(*dirs):
    import datetime as dt
    ts = dt.datetime(W.AS_OF.year, W.AS_OF.month, W.AS_OF.day, 17, 40).timestamp()
    for d in dirs:
        for root, _sub, files in os.walk(d):
            for f in sorted(files):
                os.utime(os.path.join(root, f), (ts, ts))


if __name__ == "__main__":
    task = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(task, "target")
    specimens, counts = cut(tgt)
    stamp(tgt)
    import golden as G
    g = G.compute(tgt)
    gold = os.path.join(task, "golden")
    os.makedirs(gold, exist_ok=True)
    import deliver as DL
    wb = os.path.join(gold, "screen_change_validation_2027q3.xlsx")
    DL.workbook(wb, g)
    DL.chart(os.path.join(gold, "detection_gain_by_cutoff.png"), g)
    stamp_golden(wb)
    import figures as FG
    import metadata as MD
    MD.write(task, g)
    FG.write(os.path.dirname(os.path.abspath(__file__)), g)
    mtimes(tgt, gold)
    import checks as CK
    import verify as VF
    n = CK.run(tgt, g)
    k = VF.run(tgt, os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json"))
    print("generator assertions", n, "independent checks", k)
