"""Build task501: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte. target.zip is cut from the final build with --zip.

    python3 task501/generator/build.py              everything
    python3 task501/generator/build.py --zip        everything, then target.zip
    python3 task501/generator/build.py --out DIR    the pack only, into DIR"""
import argparse
import hashlib
import os
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np        # noqa: E402

import callsim as CS      # noqa: E402
import docs as DOC        # noqa: E402
import pack as PK         # noqa: E402
import post as PP         # noqa: E402
import sim as S           # noqa: E402
import world as W         # noqa: E402

TASK = os.path.dirname(HERE)
STAMP = (2027, 7, 12, 9, 30, 0)


def simulate():
    nat = CS.national_2023()
    reg = CS.regional_2028()
    reg_total = sum(reg[c] for c in W.COUNTIES)
    prof, basis = CS.profile()
    parts, contacts = CS.survey(nat)
    opts = CS.options_paper(reg_total, prof)
    people, events, practices, merges = S.register(reg_total)
    gp = S.references(np.random.default_rng(W.SEED + 110), people, events, practices)
    rows = S.queries(people, events, gp)
    other = S.other_queries(len(rows))
    log = S.finish_register(people, events, rows, other)
    cases, lab = S.cases()
    return dict(nat=nat, reg=reg, reg_total=reg_total, prof=prof, parts=parts, contacts=contacts, opts=opts,
                people=people, events=events, merges=merges, log=log, cases=cases, lab=lab, stock=S.stock())


def write_pack(out, w):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, PK.FILES[k])
    n = {}
    n["profile"] = PK.write_profile(p("profile"))
    n["projection"] = PK.write_projection(p("projection"), w["reg"])
    prow, crow = PK.survey_rows(w["parts"], w["contacts"])
    n["participants"] = PK.write_participants(p("participants"), prow)
    n["contacts"] = PK.write_contacts(p("contacts"), crow)
    PK.write_codebook(p("codebook"), w["nat"], len(prow), len(crow))
    n["people"] = PK.write_people(p("people"), w["people"], S.ACTIVE)
    n["events"] = PK.write_events(p("events"), w["events"])
    n["merges"] = PK.write_merges(p("merges"), w["merges"])
    n["queries"] = PK.write_queries(p("queries"), w["log"])
    n["lho"] = PK.write_lho(p("lho"))
    n["cases"] = PK.write_cases(p("cases"), w["cases"])
    n["lab"] = PK.write_lab(p("lab"), w["lab"])
    n["stock"] = PK.write_stock(p("stock"), w["stock"])
    DOC.standard(p("standard"))
    DOC.options(p("options"), w["opts"], w["reg_total"])
    DOC.circular(p("circular"))
    DOC.guidelines(p("guidelines"))
    DOC.uptake(p("uptake"))
    DOC.extract_notes(p("notes"))
    DOC.fields(p("fields"))
    PK.write_transmittal(p("transmittal"), n)
    # containers: owners and saved stamps from the fiction, no library banners
    PP.normalize_ooxml(p("codebook"), "NSCS survey team", "NSCS survey team", "2024-02-19T10:14:00Z",
                       "2024-03-08T16:02:00Z", excel=True)
    PP.normalize_ooxml(p("notes"), W.PEOPLE["register"], W.PEOPLE["register"], "2027-07-04T15:21:00Z",
                       "2027-07-05T08:47:00Z", title="Register extract notes")
    PP.normalize_pdf(p("standard"), b"D:20260306141822+00'00'", b"D:20260310092611+00'00'")
    PP.normalize_pdf(p("options"), b"D:20270608163405+01'00'", b"D:20270609081944+01'00'")
    PP.normalize_pdf(p("circular"), b"D:20240411120336+01'00'", b"D:20240412090218+01'00'")
    PP.normalize_pdf(p("guidelines"), b"D:20251120103010+00'00'", b"D:20251124144725+00'00'")
    PP.normalize_pdf(p("uptake"), b"D:20270618154402+01'00'", b"D:20270620071535+01'00'")
    set_mtimes(out)
    return n


def set_mtimes(folder):
    import time
    t = time.mktime(STAMP + (0, 0, -1))
    for root, _, files in os.walk(folder):
        for f in files:
            os.utime(os.path.join(root, f), (t, t))


def digest(folder):
    h = {}
    for root, _, files in os.walk(folder):
        for f in sorted(files):
            fp = os.path.join(root, f)
            h[os.path.relpath(fp, folder)] = hashlib.sha256(open(fp, "rb").read()).hexdigest()
    return h


def cut_zip(target, zpath):
    if os.path.exists(zpath):
        os.remove(zpath)
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--zip", action="store_true")
    ap.add_argument("--no-rebuild", action="store_true")
    a = ap.parse_args()
    if a.out:
        write_pack(a.out, simulate())
        return
    import golden as G
    import checks as K
    target = os.path.join(TASK, "target")
    gold = os.path.join(TASK, "golden")
    w = simulate()
    counts = write_pack(target, w)
    figs = G.build(target, gold, os.path.join(HERE, "figures.json"), w)
    G.metadata(os.path.join(TASK, "metadata.json"), target, counts)
    import writeup as WU
    WU.main()
    K.run(target, gold, w, figs)
    import verify as V
    V.main([target, os.path.join(HERE, "figures.json")])
    if not a.no_rebuild:
        scratch = os.path.join(TASK, ".rebuild")
        write_pack(scratch, simulate())
        G.build(scratch, os.path.join(scratch, "_golden"), os.path.join(scratch, "_figures.json"), simulate())
        d1 = digest(target)
        d2 = {k: v for k, v in digest(scratch).items() if not k.startswith("_")}
        g1 = digest(gold)
        g2 = digest(os.path.join(scratch, "_golden"))
        f1 = hashlib.sha256(open(os.path.join(HERE, "figures.json"), "rb").read()).hexdigest()
        f2 = hashlib.sha256(open(os.path.join(scratch, "_figures.json"), "rb").read()).hexdigest()
        shutil.rmtree(scratch)
        assert d1 == d2, sorted(k for k in set(d1) | set(d2) if d1.get(k) != d2.get(k))
        assert g1 == g2, sorted(k for k in set(g1) | set(g2) if g1.get(k) != g2.get(k))
        assert f1 == f2, "figures.json differs between builds"
        print("REBUILD  byte-identical: %d pack files, %d goldens, figures.json" % (len(d1), len(g1)))
    if a.zip:
        cut_zip(target, os.path.join(TASK, "target.zip"))
        print("ZIP      %s" % os.path.join(TASK, "target.zip"))


if __name__ == "__main__":
    main()
