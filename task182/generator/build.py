"""Cut the bundle, compute the golden, write the deliverables, figures.json and metadata.json."""
import hashlib
import os
import shutil
import sys

import deliver as DL
import docs as DC
import figures as FG
import golden as G
import metadata as MD
import pack as PK
import postprocess as PP
import sim as SM
import world as W

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.dirname(os.path.abspath(__file__))


def cut(target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    deps, series = SM.build()
    counts = {}
    _, counts["levels"], dup = PK.write_levels(target, series)
    PK.write_deployments(target, deps)
    counts["deployments"] = len(deps)
    PK.write_positions(target)
    DC.plan(target)
    DC.notes(target)
    counts["events"] = sum(1 for _ in open(os.path.join(target, PK.FILES["events"]), encoding="utf-8")) - 1 \
        if os.path.exists(os.path.join(target, PK.FILES["events"])) else 0
    PK.write_events(target)
    counts["events"] = _rows(target, PK.FILES["events"])
    PK.write_scada(target)
    counts["scada"] = _rows(target, PK.FILES["scada"])
    PK.write_weather(target)
    counts["weather"] = _rows(target, PK.FILES["weather"])
    PK.write_bands(target, series)
    counts["bands"] = _rows(target, PK.FILES["bands"])
    PK.write_calibration(target)
    PK.write_complaints(target)
    counts["complaints"] = sum(W.COMPLAINTS.values())
    PK.write_effluent(target)
    counts["effluent"] = _rows(target, PK.FILES["effluent"])
    dupdep = [d for d in deps if (d["code"], d["k"]) == W.DUP_DEPLOYMENT][0]
    counts["dup_dep"] = int(dupdep["id"][1:])
    PK.write_manifest(target, counts)
    PP.normalize_ooxml(os.path.join(target, PK.FILES["positions"]), W.PEOPLE["engineer"][0],
                       W.PEOPLE["engineer"][0], "2026-06-08T09:12:00Z", "2026-09-02T16:41:00Z",
                       title="Noise monitoring positions", excel=True)
    PP.normalize_ooxml(os.path.join(target, PK.FILES["complaints"]), W.PEOPLE["engineer"][0],
                       W.PEOPLE["engineer"][0], "2026-01-09T10:05:00Z", "2026-10-02T11:58:00Z",
                       title="Noise complaints 2026", excel=True)
    PP.normalize_pdf(os.path.join(target, PK.FILES["plan"]), b"D:20260529142200+01'00'",
                     b"D:20260529142200+01'00'")
    PK.set_mtimes(target)
    return deps, series, dup, counts


def _rows(target, name):
    with open(os.path.join(target, name), encoding="utf-8") as fh:
        return sum(1 for _ in fh) - 1


def digest(paths):
    h = hashlib.sha256()
    for p in sorted(paths):
        h.update(os.path.basename(p).encode())
        with open(p, "rb") as fh:
            h.update(fh.read())
    return h.hexdigest()


def tree_digest(target, golddir, task):
    paths = [os.path.join(target, f) for f in sorted(os.listdir(target))]
    paths += [os.path.join(golddir, f) for f in sorted(os.listdir(golddir))]
    paths += [os.path.join(task, "metadata.json")]
    return digest(paths)


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    deps, series, dup, counts = cut(target)
    g = G.compute(target, series, dup)
    golddir = os.path.join(TASK, "golden")
    if os.path.isdir(golddir):
        shutil.rmtree(golddir)
    os.makedirs(golddir)
    DL.table(os.path.join(golddir, "specific_sound_levels.csv"), g)
    png = os.path.join(GEN, "_chart.png")
    DL.chart(png, g)
    DL.note(os.path.join(golddir, "mitigation_shortlist.pdf"), g, png)
    PP.normalize_pdf(os.path.join(golddir, "mitigation_shortlist.pdf"),
                     b"D:20261016172500+01'00'", b"D:20261016172500+01'00'")
    os.remove(png)
    MD.write(TASK, g)
    FG.write(GEN, g)
    import submission as SB
    SB.write(TASK, GEN)
    print("call     : the October slot covers %s" % ", ".join(g["slate_ordered"]))
    print("sixth    : %s at %.1f dB, %.1f dB below the fifth" % (g["sixth"], g["sixth_level"],
                                                                 g["margin_db"]))
    print("levels   : %s" % ", ".join("%s %.1f" % (r["position"], r["specific_db"]) for r in g["rows"]))
    print("rungs    :")
    for k, v in g["slates"].items():
        print("   %-18s %s  margin %.2f  next %s" % (k, ",".join(v[0]), v[1], v[2]))
    print("counts   : %s" % counts)
    import checks as CK
    n = CK.run(target, g)
    import verify as VF
    k = VF.run(target, os.path.join(GEN, "figures.json"))
    print("generator assertions %d, independent checks %d" % (n, k))
    print("digest   : %s" % tree_digest(target, golddir, TASK)[:16])
    return g


if __name__ == "__main__":
    main()
