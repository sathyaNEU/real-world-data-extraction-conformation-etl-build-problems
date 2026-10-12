"""Build task136: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the pack.

    python3 task136/generator/build.py              everything
    python3 task136/generator/build.py --out DIR    the pack only, into DIR"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C           # noqa: E402
import common as K         # noqa: E402
import docs as DOC         # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as WD         # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT_STAMP = dt.datetime(2026, 10, 12, 0, 40, tzinfo=dt.timezone.utc)   # 10:40 am in Merindah, the hand-off


def simulate():
    W = WD.World()
    WD.build_places(W)
    WD.simulate(W)
    W.legacy = WD.legacy_rows(W)
    WD.der_register(W)
    W.realloc = WD.reallocations(W)
    return W


def program_rows(W):
    r = K.rng("program-log")
    out = []
    for c in K.CAMPAIGNS:
        ref = "SS-%s-%s" % (c["key"][-2:], c["key"][:3])
        sysapps = [a for a in W.apps if a["program"] == ref and a["type"] == "New" and a["status"] in ("Connected", "Removed")]
        cancelled = [a for a in W.apps if a["program"] == ref and a["status"] == "Withdrawn"]
        n = len(sysapps)
        letter = sum(1 for x in W.nmis if x["locality"] == c["suburb"] and x["tariff"] == "Residential")
        out.append(dict(year=c["open"].year, campaign="Solar Streets %s %s" % (c["suburb"], c["open"].year),
                        suburb=c["suburb"], open=c["open"], close=c["close"], installer=c["installer"],
                        letterboxed=letter, sessions=c["sessions"],
                        registrations=int(round(n * float(r.uniform(2.6, 3.4)))),
                        assessments=int(round(n * float(r.uniform(1.5, 1.9)))),
                        contracts=n + len(cancelled) + int(r.integers(1, 4)), systems=n,
                        kwp=round(sum(a["kwp"] for a in sysapps), 1),
                        notes={"SKO22": "Autumn campaign", "TWR21": "Resumed after the 2020 pause",
                               "PBG24": "Installer changed by tender"}.get(c["key"], "")))
    return out


def hca_table(W, base_kw, golden_add_kw):
    """The assessment's figures: hosting capacity for the 2029 case set from each feeder's base forecast and its
    target excess (YRB24's from its golden excess); the 2026 case above it; minimum demand and route length."""
    r = K.rng("hca")
    out = {}
    cust = {f: sum(1 for n in W.nmis if n["feeder"] == f and n["energised"] <= dt.date(2026, 6, 30)) for f in K.FEEDERS}
    for f in K.FEEDERS:
        if f == "YRB24":
            hc29 = round((base_kw[f] + golden_add_kw) / 1000.0 - K.TARGET_GOLDEN_YRB24, 2)
        else:
            hc29 = round(base_kw[f] / 1000.0 - K.TARGET_BASE_EXCESS[f], 2)
        hc26 = round(hc29 + float(r.uniform(0.26, 0.58)), 2)
        min29 = round(float(r.uniform(0.4, 2.2)), 2)
        min26 = round(min29 + float(r.uniform(0.25, 0.9)), 2)
        out[f] = dict(route_km=round(float(r.uniform(11, 46)), 1), customers=cust[f], min26=min26, min29=min29,
                      hc26=hc26, hc29=hc29)
    return out


def peak_table():
    r = K.rng("peak")
    out = {}
    for f in K.FEEDERS:
        rating = float(r.choice([12.0, 13.5, 15.0, 16.5]))
        p0 = rating * float(r.uniform(0.62, 0.86))
        g = float(r.uniform(0.006, 0.035))
        out[f] = [rating] + [round(p0 * (1 + g) ** k, 2) for k in range(5)]
    return out


def build(out, quiet=False, W=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda f: os.path.join(out, f)
    W = W or simulate()
    counts = {}
    counts[K.REGISTER] = K.write_csv(p(K.REGISTER), R.REGISTER_COLS, R.register_rows(W))
    counts[K.LEGACY] = K.write_csv(p(K.LEGACY), R.LEGACY_COLS, R.legacy_rows(W, W.legacy), crlf=True)
    counts[K.NETWORK] = K.write_csv(p(K.NETWORK), R.NETWORK_COLS, R.network_rows(W))
    counts[K.XREF] = K.write_csv(p(K.XREF), R.XREF_COLS, R.xref_rows(W))
    counts[K.RATES] = K.write_csv(p(K.RATES), R.RATES_COLS, R.rates_rows(W), crlf=True)
    counts[K.DER] = K.write_csv(p(K.DER), R.DER_COLS, R.der_rows(W))
    counts[K.REALLOC] = K.write_csv(p(K.REALLOC), R.REALLOC_COLS, R.realloc_rows(W.realloc))
    counts[K.REBATE] = K.write_csv(p(K.REBATE), R.REBATE_COLS, R.rebate_rows(W))
    prog = program_rows(W)
    DOC.write_program_log(p(K.PROGRAM_LOG), prog)
    letter = {s: sum(1 for x in W.nmis if x["locality"] == s and x["tariff"] == "Residential")
              for s in ("Bindarra Waters", "Wattleview")}
    DOC.write_letter(p(K.LETTER), letter)
    # the hosting capacity table is set from the base forecast computed on the written files
    L = C.load(out, partial=True)
    base = C.base_forecast(L["reg"])
    camps, pools = C.campaigns(L), C.pools_2027(L)
    lift = C.lifts(camps, pools, "untapped")
    avgkw = C.avg_new_kw(L["reg"])
    golden_add = lift["Bindarra Waters"] * avgkw["YRB24"]
    W.hca = hca_table(W, base["base"], golden_add)
    DOC.write_hca(p(K.HCA), W.hca)
    DOC.write_npp(p(K.NPP))
    DOC.write_peak(p(K.PEAK), peak_table())
    DOC.write_dictionary(p(K.DICTIONARY), counts)
    manifest = [
        (K.REGISTER, "Embedded generation connections (EGC)", "2026-09-01", counts[K.REGISTER], K.PEOPLE["connections"],
         "micro EG applications for NMIs on Yarrabin feeders, all statuses, received to 31 August 2026"),
        (K.LEGACY, "EGC legacy archive", "2019-06-29", counts[K.LEGACY], K.PEOPLE["connections"],
         "inverters of applications migrated from the pre-July-2019 system"),
        (K.NETWORK, "Network model (GIS)", "2026-09-01", counts[K.NETWORK], K.PEOPLE["gis"],
         "NMIs on Yarrabin feeders at 31 August 2026"),
        (K.XREF, "GIS NMI-to-property match", "2026-09-01", counts[K.XREF], K.PEOPLE["gis"],
         "NMIs on Yarrabin feeders to Merindah City Council property numbers"),
        (K.RATES, "Merindah City Council rating system", "2026-08-03", counts[K.RATES], "Merindah City Council",
         "2026-27 rates roll, western rating area"),
        (K.DER, "DER Register (national) via Mirrabee extraction", "2026-09-05", counts[K.DER], K.PEOPLE["connections"],
         "AC connections and devices at NMIs on Yarrabin feeders, all statuses"),
        (K.REALLOC, "Market systems (NMI standing data)", "2026-09-01", counts[K.REALLOC], K.PEOPLE["connections"],
         "NMIs replaced at Yarrabin premises since 1 July 2019"),
        (K.REBATE, "Queensland home battery rebate (state program)", "2026-07-14", counts[K.REBATE],
         K.PEOPLE["customer"], "approvals for Merindah addresses, FY2025-26"),
        (K.PROGRAM_LOG, "Merindah City Council", "2025-03-03", "", "Merindah City Council",
         "Solar Streets campaign summary 2018 to 2024, as received"),
        (K.LETTER, "Merindah City Council", "2026-08-14", "", "Merindah City Council", "letter on the 2027 campaigns"),
        (K.NPP, "Network Planning", "2026-03-02", "", K.PEOPLE["planning"], "procedure, revision 3"),
        (K.HCA, "Buchanan Power Engineering", "2026-07-24", "", K.PEOPLE["consultant"], "assessment report BPE-2026-031"),
        (K.PEAK, "Network Planning", "2026-05-12", "", K.PEOPLE["planning"], "summer peak demand forecast by feeder"),
        (K.DICTIONARY, "Network Planning", "2026-09-02", "", K.PEOPLE["analyst"], "field definitions for these extracts"),
    ]
    K.write_csv(p(K.MANIFEST), R.MANIFEST_COLS, manifest)
    PP.normalize_ooxml(p(K.PROGRAM_LOG), K.PEOPLE["council"], K.PEOPLE["council"], "2019-02-11T23:12:40Z",
                       "2025-03-03T05:31:17Z", excel=True, company=K.COUNCIL)
    PP.normalize_ooxml(p(K.DICTIONARY), K.PEOPLE["analyst"], K.PEOPLE["analyst"], "2024-05-20T01:02:11Z",
                       "2026-09-02T03:44:58Z", excel=True)
    PP.normalize_ooxml(p(K.PEAK), K.PEOPLE["planning"], K.PEOPLE["planning"], "2026-04-29T22:05:31Z",
                       "2026-05-12T06:17:09Z", excel=True)
    PP.normalize_pdf(p(K.NPP), b"D:20260226104512+10'00'", b"D:20260302083017+10'00'")
    PP.normalize_pdf(p(K.HCA), b"D:20260722161408+10'00'", b"D:20260724092251+10'00'")
    PP.normalize_pdf(p(K.LETTER), b"D:20260814111930+10'00'", b"D:20260814112406+10'00'")
    stamp = EXPORT_STAMP.timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    W.counts = counts
    W.prog = prog
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)),
                                          ", ".join("%s %d" % kv for kv in counts.items())))
    return W


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest()
            for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    when = EXPORT_STAMP.timetuple()[:6]
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(f, date_time=when)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(folder, f), "rb") as fh:
                z.writestr(zi, fh.read())
    return zp


def everything(root, quiet=False):
    import deliver as DL
    import metadata as MD
    W = build(os.path.join(root, "target"), quiet=quiet)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    DL.main(os.path.join(root, "target"), os.path.join(root, "golden"),
            os.path.join(root, "generator", "figures.json"))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    return W


def main():
    import checks as CK
    import verify as V
    W = everything(TASK)
    CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), W=W,
           meta_path=os.path.join(TASK, "metadata.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        os.makedirs(os.path.join(tmp, "generator"))
        everything(tmp, quiet=True)
        same_t = digest(os.path.join(TASK, "target")) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        same = {}
        for f in ("metadata.json", os.path.join("generator", "figures.json")):
            same[f] = open(os.path.join(TASK, f), "rb").read() == open(os.path.join(tmp, f), "rb").read()
        same["target.zip"] = open(cut_zip(TASK), "rb").read() == open(cut_zip(tmp), "rb").read()
        if not (same_t and same_g and all(same.values())):
            raise SystemExit("second build differs: target %s, golden %s, %s" % (same_t, same_g, same))
    finally:
        shutil.rmtree(tmp)
    allh = hashlib.sha256("".join(v for _, v in sorted(digest(os.path.join(TASK, "target")).items())).encode() +
                          "".join(v for _, v in sorted(digest(os.path.join(TASK, "golden")).items())).encode())
    print("two builds byte-identical: %d target files, %d golden files, metadata.json, figures.json and target.zip "
          "(sha256 %s; target.zip sha256 %s)" % (
              len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden"))),
              allh.hexdigest()[:16], hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    else:
        main()
