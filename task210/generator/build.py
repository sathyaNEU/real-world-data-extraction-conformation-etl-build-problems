"""Cut the bundle, compute the golden from it, write the deliverables, figures.json, metadata.json and submission.md,
then run the generator's assertions and the independent verifier, and zip target/.

    python3 build.py            the whole chain (the only entry point that writes figures.json)
    python3 build.py --cut      the pack only
"""
import json
import os
import shutil
import sys
import time
import zipfile

import docs
import pack as PK
import postprocess as PP
import sim
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
GOLD = os.path.join(TASK, "golden")
ZIP_STAMP = (2027, 1, 15, 9, 12, 0)
MTIME = time.mktime((2027, 1, 15, 9, 12, 0, 0, 0, 0))


def cut():
    if os.path.isdir(TGT):
        shutil.rmtree(TGT)
    os.makedirs(TGT)
    S = sim.run()
    info = PK.cut(TGT, S)
    docs.build(TGT, PK.FILES)
    PP.normalize_pdf(os.path.join(TGT, PK.FILES["procedure"]), b"D:20251103091500+00'00'", b"D:20251103142200+00'00'")
    PP.normalize_ooxml(os.path.join(TGT, PK.FILES["assets"]), "Network Asset Information", W.PEOPLE["network"],
                       "2016-05-09T08:31:00Z", "2027-01-14T16:05:00Z", title="Marsh and Wolds wastewater assets",
                       excel=True, company=W.COMPANY)
    PP.normalize_ooxml(os.path.join(TGT, PK.FILES["plan"]), "Wastewater Planning", "Wastewater Planning",
                       "2024-07-02T10:12:00Z", "2026-11-27T11:48:00Z", title="Storm overflow improvement plan 2025-2030",
                       excel=True, company=W.COMPANY)
    for root, _, files in os.walk(TGT):
        for f in files:
            os.utime(os.path.join(root, f), (MTIME, MTIME))
    return S, info


def zip_target():
    path = os.path.join(TASK, "target.zip")
    names = []
    for root, _, files in os.walk(TGT):
        for f in files:
            names.append(os.path.relpath(os.path.join(root, f), TASK))
    names.sort()
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            zi = zipfile.ZipInfo(n.replace(os.sep, "/"), date_time=ZIP_STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TASK, n), "rb").read())
    return path


def main():
    S, info = cut()
    if "--cut" in sys.argv:
        print(json.dumps({k: v for k, v in info.items() if k != "comms"}, indent=1))
        return
    import golden as G
    import deliver
    import figures as FG
    import metadata as MD
    import writeup as WU
    import routes as RT
    g = G.compute(TGT)
    g["routes"] = RT.ladder(g, TGT)
    os.makedirs(GOLD, exist_ok=True)
    deliver.write(g, GOLD)
    figs = FG.figures(g, info)
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    MD.write(TASK, info)
    WU.write(TASK, figs)
    import checks as CK
    import verify as VF
    n = CK.run(TGT, S, g, info, figs)
    k = VF.run(TGT, os.path.join(HERE, "figures.json"))
    import ceiling as CL
    m = CL.measure(TGT, g, g["routes"])
    assert m["pair"] <= 60 and m["mirror_leakage"] < 50, m
    zp = zip_target()
    print("generator assertions %d, independent checks %d" % (n, k))
    print("ceiling: pair %.1f, cracker %.1f, mirror %.1f, cracker keep %.1f, mirror leakage %.1f, full keep %.1f, "
          "cracker device keep %s, digest %s" % (m["pair"], m["cracker_score"], m["mirror_score"], m["cracker_keep"],
                                                 m["mirror_leakage"], m["full_keep"], m["cracker_device_keep"],
                                                 m["pack_digest"]))
    print("ceiling rows:", m["rows"])
    print("call:", g["call"], " delivered:", g["delivered"][g["call_code"]], " pff:", g["pff"][g["call_code"]])
    print("zip", zp)


if __name__ == "__main__":
    main()
