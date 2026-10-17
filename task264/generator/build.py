"""Build task264: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task264/generator/build.py              everything
    python3 task264/generator/build.py --out DIR    the pack only, into DIR
    python3 task264/generator/build.py --golden     the pack and the goldens, no checks"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import argparse      # noqa: E402
import hashlib       # noqa: E402
import shutil        # noqa: E402
import sys           # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K         # noqa: E402
import docs as D           # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = 1796594160          # 7 December 2026 08:56 AEDT, the team's export


def build(out):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    T = W.world()
    loads = R.plan_loads(T)
    per_load = {}
    n_mv, resub_store, resub_id = R.write_movement(p("movement"), T, loads, per_load)
    n_ss, doubled = R.write_store_sales(p("totals"), T, loads, per_load)
    agreement = R.panel_from(T)
    counts = dict(movement=n_mv, totals=n_ss, register=R.write_register(p("register"), T),
                  items=R.write_items(p("items"), T), log=R.write_log(p("log"), loads, per_load),
                  calendar=R.write_calendar(p("calendar")), audit=R.write_audit(p("audit"), T),
                  method=1, terms=1, partners=len(K.CHAIN_CODES), dictionary=len(D.DICTIONARY), household=len(K.CATS))
    D.write_method(p("method"))
    D.write_terms(p("terms"))
    D.write_partners(p("partners"), agreement)
    D.write_dictionary(p("dictionary"))
    D.write_household(p("household"))
    D.write_manifest(p("manifest"), K.FILES, counts)
    PP.COMPANY = K.FIRM
    PP.normalize_ooxml(p("partners"), K.PEOPLE["feeds"], K.PEOPLE["feeds"], "2024-02-19T23:12:05Z",
                       "2026-12-06T22:31:48Z", excel=True)
    PP.normalize_ooxml(p("dictionary"), K.PEOPLE["feeds"], K.PEOPLE["head"], "2023-08-08T01:44:30Z",
                       "2026-12-06T21:57:12Z", excel=True)
    PP.normalize_ooxml(p("household"), "Consumer Panels", "Consumer Panels", "2026-11-09T23:20:41Z",
                       "2026-11-09T23:26:03Z", excel=True)
    PP.normalize_pdf(p("method"), b"D:20260128101532+11'00'", b"D:20260128104907+11'00'")
    PP.normalize_pdf(p("terms"), b"D:20261104163012+11'00'", b"D:20261105091541+11'00'")
    for f in sorted(os.listdir(out)):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    T["loads"] = loads
    T["resub_store"], T["resub_id"], T["doubled"] = resub_store, resub_id, doubled
    T["agreement"] = agreement
    return T, counts


def tree_digest(d):
    h = hashlib.sha256()
    for f in sorted(os.listdir(d)):
        h.update(f.encode())
        h.update(open(os.path.join(d, f), "rb").read())
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--golden", action="store_true")
    a = ap.parse_args()
    if a.out:
        build(a.out)
        return
    target = os.path.join(TASK, "target")
    T, counts = build(target)
    print("pack:", counts)
    import deliver
    deliver.write(target, os.path.join(TASK, "golden"), T)
    if a.golden:
        return
    import checks
    checks.run(target, T)
    r = os.system("python3 %s %s" % (os.path.join(HERE, "verify.py"), target))
    assert r == 0, "verify failed"
    scratch = os.path.join(TASK, ".rebuild")
    build(scratch)
    same = tree_digest(scratch) == tree_digest(target)
    shutil.rmtree(scratch)
    assert same, "second build differs"
    print("rebuild byte-identical")
    zp = os.path.join(TASK, "target.zip")
    if os.path.exists(zp):
        os.remove(zp)
    import zipfile
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo("target/" + f, date_time=(2026, 12, 7, 8, 56, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    print("target.zip cut")


if __name__ == "__main__":
    main()
