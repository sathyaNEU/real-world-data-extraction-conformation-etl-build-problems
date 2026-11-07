"""Cut the bundle, compute the golden from it, write the deliverables, figures.json, metadata.json and submission.md,
then run the generator's assertions, the independent verifier and the ceiling, and zip target/.

    python3 build.py            the whole chain (the only entry point that writes figures.json)
    python3 build.py --cut      the pack and the golden only, printed
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
ZIP_STAMP = (2026, 10, 9, 8, 40, 0)
MTIME = time.mktime((2026, 10, 9, 8, 40, 0, 0, 0, 0))
PDF_STAMPS = {
    "procedure": (b"D:20250602101500+01'00'", b"D:20250602101500+01'00'"),
    "agreement": (b"D:20240321143000+00'00'", b"D:20240325091200+00'00'"),
    "certs": (b"D:20190321112000+00'00'", b"D:20260827154400+01'00'"),
    "national": (b"D:20260311160500+00'00'", b"D:20260316094000+00'00'"),
    "gammaspec": (b"D:20261006153000+01'00'", b"D:20261007101100+01'00'"),
}
OOXML = {
    "register": ("Network Manager", W.PEOPLE["manager"], "2014-02-17T09:22:00Z", "2026-07-01T08:05:00Z",
                 "Station register"),
    "visits": (W.PEOPLE["eng_a"], W.PEOPLE["eng_b"], "2026-07-01T07:58:00Z", "2026-09-30T15:41:00Z",
               "Source check visits Q3 2026"),
    "field": (W.PEOPLE["eng_a"], W.PEOPLE["eng_a"], "2026-06-30T08:31:00Z", "2026-09-29T11:52:00Z",
              "Air sampler field sheets Q3 2026"),
    "beta": ("LIMS export", W.PEOPLE["chem"], "2026-07-15T13:20:00Z", "2026-10-08T14:06:00Z", "Gross beta results"),
}


def cut():
    if os.path.isdir(TGT):
        shutil.rmtree(TGT)
    os.makedirs(TGT)
    T = sim.run()
    info = PK.cut(TGT, T)
    docs.build(TGT, PK.FILES, PK.extras(T))
    for key, (c, m) in PDF_STAMPS.items():
        PP.normalize_pdf(os.path.join(TGT, PK.FILES[key]), c, m)
    for key, (creator, last, created, modified, title) in OOXML.items():
        company = W.LAB_GB if key == "beta" else W.UNIVERSITY
        PP.normalize_ooxml(os.path.join(TGT, PK.FILES[key]), creator, last, created, modified, title=title,
                           excel=True, company=company)
    for root, _, files in os.walk(TGT):
        for f in files:
            os.utime(os.path.join(root, f), (MTIME, MTIME))
    return T, info


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
    T, info = cut()
    import golden as G
    g = G.compute(TGT)
    if "--cut" in sys.argv:
        for c in g["call_codes"]:
            print("call", c, [d.isoformat() for d in g["call"][c]["dates"]], "peak", g["call"][c]["peak"])
        print("sessions", [(s["code"], s["date"].isoformat()) for s in T["sessions"]])
        print("checks", {c: (round(v["pct"], 2), v["passed"]) for c, v in sorted(g["checks"].items())})
        print("air", {k: round(v["conc"], 4) for k, v in sorted(g["air"].items())})
        print("timely", {c: round(v["pct"], 3) for c, v in sorted(g["timely"].items())})
        print(json.dumps({k: v for k, v in info.items() if k != "reference"}, indent=1))
        return
    import routes as RT
    import deliver
    import figures as FG
    import metadata as MD
    import writeup as WU
    g["routes"] = RT.ladder(g, TGT)
    os.makedirs(GOLD, exist_ok=True)
    deliver.write(g, GOLD)
    figs = FG.figures(g, info)
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    MD.write(TASK, info)
    WU.write(TASK, figs)
    import checks as CK
    import verify as VF
    n = CK.run(TGT, T, g, info, figs)
    k = VF.run(TGT, os.path.join(HERE, "figures.json"))
    import ceiling as CL
    m = CL.measure(TGT, g)
    assert m["pair"] <= 60 and m["mirror_leakage"] < 50, m
    zp = zip_target()
    print("generator assertions %d, independent checks %d" % (n, k))
    print("ceiling: pair %.1f, cracker %.1f, mirror %.1f, cracker keep %.1f, mirror leakage %.1f, digest %s"
          % (m["pair"], m["cracker_score"], m["mirror_score"], m["cracker_keep"], m["mirror_leakage"], m["pack_digest"]))
    print("ceiling rows:", m["rows"])
    print("call:", g["call_codes"])
    print("zip", zp)


if __name__ == "__main__":
    main()
