"""Build task311: the pack into <task>/target, the goldens into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks, the independent verifier, a second full build into a scratch folder
compared byte for byte, and target.zip cut from the final build.

    python3 task311/generator/build.py              everything
    python3 task311/generator/build.py --out DIR    the pack only, into DIR
"""
import argparse
import numpy as np
import hashlib
import json
import os
import shutil
import sys
import warnings
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import docs as D        # noqa: E402
import estim as E       # noqa: E402
import golden as G      # noqa: E402
import pack as P        # noqa: E402
import solve as S       # noqa: E402
import world as W       # noqa: E402

TASK = os.path.dirname(HERE)
STAMP = (2026, 11, 2, 21, 41, 0)        # the folder as the centre assembled it for the foundation


def figures(w):
    m = S.main_call(w)
    tab, res = m["tab"], m["res"]
    regions = {}
    for r in (1, 2, 3, 4, 5):
        rows = tab[r]
        q = res[r]["_"]
        icc = q["icc_pub"]                  # the report's Table 2 correlation, three decimals
        a = E.shares_a(rows)
        mm = np.array([len(x["y"]) for x in rows], float)
        v25 = float((a ** 2 * (icc + (1 - icc) / mm)).sum())
        pub = [p for p in m["published"] if p["region"] == W.RNAME[r]][0]
        share = res[r][S.GOLDEN]
        regions[r] = dict(areas=len(rows), completes=sum(x["m_all"] for x in rows), add=int(round(q["add"])),
                          between_share=float(icc * (a ** 2).sum() / v25), share=float(share),
                          share_pct=int(round(100 * share)), n=pub["n"], est=pub["est"], se=pub["se"],
                          deff=pub["deff"], deffw=E.deff_w(rows), deffw_boost=E.deff_w(rows, q["add"]),
                          rho=icc, routes={k: float(v) for k, v in res[r].items() if k != "_"})
    cv = tab[2]
    a_cv = E.shares_a(cv)
    supp = np.array([x["stratum"] == "2S" for x in cv])
    w_supp = np.mean([x["w"] for x in cv if x["stratum"] == "2S"])
    w_core = np.mean([x["w"] for x in cv if x["stratum"] != "2S"])
    regions[2]["supp_share"] = float(a_cv[supp].sum())
    regions[2]["weight_ratio"] = float(w_supp / w_core)
    ask = S.ask_2024(w)
    F = dict(call=m["call"], runner=m["runner"], rank_order=m["order"], regions=regions,
             flip_per_area=m["flip_per_area"], flip_interviews=m["flip_interviews"],
             flip_below=m["flip_below"], flip_at=m["flip_at"], published=m["published"], design=m["design"],
             ask=ask["golden"], ask_all=ask, rr_text=S.response_rate_text(w))
    return F


def build_pack(out, w, F):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    counts = {}
    counts["northmark"] = P.write_csv(f("northmark"), P.NM_COLS, P.northmark_rows(w))
    counts["ostrander"] = P.write_ostrander(f("ostrander"), P.ostrander_rows(w))
    counts["weights"] = P.write_csv(f("weights"), P.W_COLS, P.weights_rows(w))
    counts["crosswalk"] = P.write_crosswalk(f("crosswalk"), w)
    counts["regions"] = P.write_csv(f("regions"), ["region", "region_name", "abbreviation"], P.regions_rows())
    open(f("nm_codes"), "w", encoding="utf-8", newline="\r\n").write(P.NM_CODES_TXT)
    open(f("os_codes"), "w", encoding="utf-8", newline="\r\n").write(P.OS_CODES_TXT)
    counts["pharmacy"] = P.write_csv(f("pharmacy"), P.P_COLS, P.pharmacy_rows(w))
    P.write_quotes(f("quotes"))
    D.technical_report(f("report"), dict(design=F["design"], published=F["published"], rr_text=F["rr_text"]))
    D.boost_terms(f("terms"))
    import postprocess as PP
    for k in ("crosswalk", "quotes"):
        PP.normalize_ooxml(f(k), creator={"ostrander": "Ostrander Data Collection", "crosswalk": "Health System Planning",
                                          "quotes": "Jason Clarke"}[k],
                           last_by={"ostrander": "Ostrander Data Collection", "crosswalk": "Health System Planning",
                                    "quotes": "Jason Clarke"}[k],
                           created={"ostrander": "2025-06-17T14:02:00Z", "crosswalk": "2024-03-12T15:15:00Z",
                                    "quotes": "2026-10-01T14:40:00Z"}[k],
                           modified={"ostrander": "2025-06-17T14:09:00Z", "crosswalk": "2024-03-14T16:30:00Z",
                                     "quotes": "2026-10-03T15:12:00Z"}[k], excel=True,
                           company={"ostrander": "Ostrander Data Collection Inc.", "crosswalk": "Ministry of Health",
                                    "quotes": "Halvorsen University"}[k])
    stamp(out)
    return counts


def stamp(folder):
    import time
    t = time.mktime(STAMP + (0, 0, -1))
    for root, _, files in os.walk(folder):
        for name in files:
            os.utime(os.path.join(root, name), (t, t))


def digest(folder):
    h = hashlib.sha256()
    for root, _, files in sorted(os.walk(folder)):
        for name in sorted(files):
            p = os.path.join(root, name)
            h.update(os.path.relpath(p, folder).encode())
            h.update(open(p, "rb").read())
    return h.hexdigest()


def write_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo("target/" + name, date_time=STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, name), "rb").read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    args = ap.parse_args()
    w = W.world()
    F = figures(w)
    if args.out:
        build_pack(args.out, w, F)
        return
    target = os.path.join(TASK, "target")
    counts = build_pack(target, w, F)
    gold = os.path.join(TASK, "golden")
    if os.path.exists(gold):
        shutil.rmtree(gold)
    os.makedirs(gold)
    G.workbook(os.path.join(gold, "boost_region_2027.xlsx"), F)
    G.memo(os.path.join(gold, "boost_memo_2027.pdf"), F)
    stamp(gold)
    import writeup as WU
    figs = WU.figures_json(F)
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8").write(WU.submission(F))
    import metadata as MD
    json.dump(MD.metadata(counts), open(os.path.join(TASK, "metadata.json"), "w"), indent=1)
    # a second build, byte for byte
    scratch = os.path.join(TASK, ".rebuild")
    build_pack(scratch, W.world(), F)
    d1, d2 = digest(target), digest(scratch)
    shutil.rmtree(scratch)
    assert d1 == d2, "rebuild differs: %s %s" % (d1, d2)
    write_zip(target, os.path.join(TASK, "target.zip"))
    print("target digest %s, zip sha256 %s" % (d1[:16], hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()[:16]))
    print("rows: " + ", ".join("%s %d" % kv for kv in counts.items() if kv[1]))


if __name__ == "__main__":
    main()
