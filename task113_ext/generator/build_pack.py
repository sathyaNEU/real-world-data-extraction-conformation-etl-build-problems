"""Build task113_ext: the data bundle into task113_ext/target and metadata.json, the independent checks on the
written files, a second full build compared byte for byte, and target.zip cut from the final build.

    python3 task113_ext/generator/build_pack.py           everything
    python3 task113_ext/generator/build_pack.py --fast    one build with the checks, no second build or zip
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import docs as DC          # noqa: E402
import pack as P           # noqa: E402
import postprocess as PP   # noqa: E402
import world as W          # noqa: E402

ROOT = os.path.dirname(HERE)
EASTERN = dt.timezone(dt.timedelta(hours=-5))
PDF_STAMPS = {"dict_px": b"D:20240108101522-05'00'", "spec_ca": b"D:20230612143010-04'00'",
              "guide_fund": b"D:20250317091204-04'00'", "method_idx": b"D:20250214160845-05'00'",
              "fees": b"D:20250210112233-05'00'"}
OOXML = {"delist": ("Merriden Market Data", "Merriden Market Data", "2026-10-07T13:02:00Z", "2026-10-07T13:44:10Z",
                    "Merriden Market Data"),
         "recon": ("Northcote Indices", "Northcote Indices", "2026-07-09T15:20:00Z", "2026-07-10T08:05:31Z",
                   "Northcote Indices")}


def build(out, x=None, quiet=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    x = x or P.everything()
    n = {}
    n["px_old"] = P.write_csv(f("px_old"), P.OLD_COLS, P.old_rows(x), crlf=True)
    n["px_new"] = P.write_parquet(f("px_new"), P.new_table(x))
    n["secmaster"] = P.write_csv(f("secmaster"), P.SM_COLS, P.secmaster_rows(x))
    n["ca"] = P.write_ca(f("ca"), x["ca"])
    n["fund"] = P.write_csv(f("fund"), P.FUND_COLS, P.fund_rows(x))
    n["earn"] = P.write_jsonl(f("earn"), x["earn"])
    n["levels"] = P.write_csv(f("levels"), P.LEVEL_COLS, P.level_rows(x))
    n["si"] = P.write_csv(f("si"), P.SI_COLS, P.si_rows(x), delimiter="|")
    n["sweep"] = P.write_csv(f("sweep"), P.SWEEP_COLS, P.sweep_rows(x))
    n["orders"] = P.write_csv(f("orders"), P.ORDER_COLS, P.order_rows(x))
    n["fills"] = P.write_csv(f("fills"), P.FILL_COLS, P.fill_rows(x))
    DC.write_delistings(f("delist"), x["delist"])
    n["delist"] = len(x["delist"])
    DC.write_recons(f("recon"), x["recons"], x["changes"])
    n["recon"] = sum(len(r["rows"]) for r in x["recons"])
    DC.write_dictionary(f("dict_px"))
    DC.write_ca_spec(f("spec_ca"))
    DC.write_fund_guide(f("guide_fund"))
    DC.write_methodology(f("method_idx"))
    DC.write_fees(f("fees"))
    DC.write_readme(f("readme"), n)
    for k, stamp in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), stamp, stamp)
    for k, (cr, lb, c0, m0, co) in OOXML.items():
        PP.normalize_ooxml(f(k), cr, lb, c0, m0, excel=True, company=co)
    for i, k in enumerate(W.FILES):
        y, m, d = (int(v) for v in W.AS_OF[k].split("-"))
        ts = dt.datetime(y, m, d, 8 + (i * 5) % 9, (i * 17) % 60, tzinfo=EASTERN).timestamp()
        os.utime(f(k), (ts, ts))
    if not quiet:
        big = max((k for k in n if k not in ("recon", "delist")), key=lambda k: n[k])
        print("pack: %d files, largest %s (%d rows)" % (len(W.FILES), W.FILES[big], n[big]))
    return n, x


def metadata(n, path):
    fmt = lambda name: name.rsplit(".", 1)[-1]
    files = []
    origin = {"px_old": "an end-of-day equity pricing vendor's legacy history file",
              "px_new": "the same vendor's current-platform Parquet delivery",
              "secmaster": "the vendor's security master history", "ca": "the vendor's corporate actions feed",
              "delist": "the vendor's delisting workbook", "fund": "a point-in-time fundamentals vendor's file",
              "earn": "the fundamentals vendor's earnings calendar log", "recon": "an index provider's "
              "reconstitution workbook", "levels": "the index provider's daily levels",
              "si": "exchange semi-monthly short interest files", "sweep": "a custodian's daily sweep rate",
              "orders": "an asset manager's order management system export",
              "fills": "a broker's execution report", "dict_px": "the pricing vendor's data dictionary",
              "spec_ca": "the corporate actions feed specification", "guide_fund": "the fundamentals vendor's user "
              "guide", "method_idx": "the index methodology summary", "fees": "the broker's commission schedule",
              "readme": "the research data team's extract notes"}
    for k, name in W.FILES.items():
        files.append(dict(file=name, format=fmt(name), rows=n.get(k), as_of=W.AS_OF[k],
                          layout=origin[k]))
    meta = dict(
        task="task113_ext",
        kind="input dataset only: no question, draw, ladder, stump, golden or fingerprint card",
        domain="Quantitative Finance",
        subdomain_intended="strategy-backtesting-evaluation (the bundle also carries what event-study, "
                           "factor-return-attribution, market-microstructure-execution-cost and "
                           "portfolio-construction-risk work needs)",
        objective="not fixed; the draw picks it",
        as_of="2026-10-09",
        input_gates=dict(files=len(W.FILES), formats=sorted(set(fmt(v) for v in W.FILES.values())),
                         largest_file=W.FILES["px_old"], largest_file_rows=n["px_old"]),
        distractor_files="named at the draw, against the question it files",
        files=files,
        sources=[dict(files="all files under target/",
                      origin="constructed for this bundle by task113_ext/generator/build_pack.py (seeded, "
                             "deterministic) in the layouts of US equity data vendors, an index provider, exchange "
                             "short interest files, a custodian, an order management system and a broker; the "
                             "companies, vendors, index, broker, custodian and asset manager are fictional; the "
                             "exchange calendar (holidays, the 2018 and 2025 closures, early closes) is the real one",
                      date="2026-10-09",
                      license="original work for this bundle; no third-party data")],
    )
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(meta, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            t = dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(folder, name)), EASTERN)
            zi = zipfile.ZipInfo(name, date_time=(t.year, t.month, t.day, t.hour, t.minute, t.second))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, quiet=False):
    n, x = build(os.path.join(root, "target"), quiet=quiet)
    metadata(n, os.path.join(root, "metadata.json"))
    return n, x


def main(fast=False):
    import zipfile
    import checks as CK
    n, x = everything(ROOT)
    good = CK.run(os.path.join(ROOT, "target"))
    if fast:
        if not good:
            raise SystemExit("checks failed")
        return
    tmp = tempfile.mkdtemp(dir=ROOT, suffix=".tmp")
    try:
        everything(tmp, quiet=True)
        same_t = digest(os.path.join(ROOT, "target")) == digest(os.path.join(tmp, "target"))
        same_m = open(os.path.join(ROOT, "metadata.json"), "rb").read() == open(os.path.join(tmp, "metadata.json"),
                                                                                "rb").read()
        if not (same_t and same_m):
            bad = [k for k, v in digest(os.path.join(ROOT, "target")).items()
                   if digest(os.path.join(tmp, "target")).get(k) != v]
            raise SystemExit("second build differs: %s, metadata %s" % (bad, same_m))
    finally:
        shutil.rmtree(tmp)
    print("two builds byte-identical: %d target files and metadata.json" % len(os.listdir(os.path.join(ROOT, "target"))))
    zp = cut_zip(ROOT)
    with zipfile.ZipFile(zp) as z:
        inside = {i.filename: hashlib.sha256(z.read(i.filename)).hexdigest() for i in z.infolist()}
    if inside != digest(os.path.join(ROOT, "target")):
        raise SystemExit("target.zip differs from target/")
    print("target.zip cut from this build: %d files (sha256 %s, %.1f MB)" % (
        len(inside), hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16], os.path.getsize(zp) / 1e6))
    if not good:
        raise SystemExit("checks failed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    main(fast=ap.parse_args().fast)
