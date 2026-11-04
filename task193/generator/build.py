"""Cut the bundle, compute the golden from it, write the deliverables, figures.json, metadata.json and submission.md,
then run the generator's assertions and the independent verifier, and zip target/."""
import json
import os
import shutil
import sys
import zipfile

import docs
import golden as G
import pack as PK
import postprocess as PP
import sim
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
GOLD = os.path.join(TASK, "golden")
ZIP_STAMP = (2026, 11, 3, 7, 40, 0)


def cut():
    if os.path.isdir(TGT):
        shutil.rmtree(TGT)
    os.makedirs(TGT)
    S = sim.run()
    info = PK.cut(TGT, S)
    docs.build(TGT, PK.FILES)
    PP.normalize_pdf(os.path.join(TGT, PK.FILES["sap"]), b"D:20180322101500-05'00'", b"D:20180524083000-05'00'")
    PP.normalize_pdf(os.path.join(TGT, PK.FILES["approval"]), b"D:20170911141000-05'00'", b"D:20170911141000-05'00'")
    PP.normalize_pdf(os.path.join(TGT, PK.FILES["fieldproc"]), b"D:20210208093000-06'00'", b"D:20210208093000-06'00'")
    PP.normalize_ooxml(os.path.join(TGT, PK.FILES["points"]), W.PEOPLE["hydrogeologist"], W.PEOPLE["hydrogeologist"],
                       "2014-07-21T15:02:00Z", "2024-06-11T14:47:00Z", title="Marten Creek monitoring points", excel=True,
                       company="Fieldstone Hydrogeology, LLC")
    PP.normalize_ooxml(os.path.join(TGT, PK.FILES["inspect"]), W.PEOPLE["manager"], W.PEOPLE["manager"],
                       "2024-01-23T16:10:00Z", "2026-10-16T20:31:00Z", title="Site inspections", excel=True)
    return S, info


def zip_target():
    path = os.path.join(TASK, "target.zip")
    names = sorted(os.listdir(TGT))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            zi = zipfile.ZipInfo("target/" + n, date_time=ZIP_STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TGT, n), "rb").read())
    return path


def main():
    S, info = cut()
    g = G.compute(TGT, PK.FILES)
    import deliver
    import figures as FG
    import metadata as MD
    import writeup as WU
    os.makedirs(GOLD, exist_ok=True)
    deliver.write(g, GOLD)
    figs = FG.figures(g, info)
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    MD.write(TASK)
    WU.write(TASK, figs)
    import checks as CK
    import verify as VF
    n = CK.run(TGT, S, g, info, figs)
    k = VF.run(TGT, os.path.join(HERE, "figures.json"))
    zp = zip_target()
    print("generator assertions %d, independent checks %d" % (n, k))
    print("resample:", g["resample"], " limits:", {kk: round(v, 2) for kk, v in g["golden"].items()},
          " n:", g["golden_n"])
    print("rows: edd A %d, edd B %d, gauging %d, purge %d" % (info["edd_a_rows"], info["edd_b_rows"],
                                                             info["gauging_rows"], info["purge_rows"]))
    print("zip", zp)


if __name__ == "__main__":
    main()
