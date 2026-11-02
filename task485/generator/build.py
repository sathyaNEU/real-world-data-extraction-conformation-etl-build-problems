"""Builds task485's pack into target/, the golden deliverables into golden/, metadata.json and generator/figures.json,
twice, asserts the two builds byte-identical, and cuts target.zip.

    python3 task485/generator/build.py          # the whole build
    python3 task485/generator/build.py pack     # the pack only, once, into target/
"""
import hashlib
import json
import os
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
sys.path.insert(0, HERE)

import analysis as A      # noqa: E402
import world as W         # noqa: E402

OWNERS = {
    "drug": dict(creator="Halcroft Client Reporting", last_by="Halcroft Client Reporting", created="2026-10-01T06:10:00Z",
                 modified="2026-10-01T06:10:00Z", company="Halcroft Pharmacy Solutions"),
}
for q, mod in (("2025Q2", "2025-09-19T13:05:00Z"), ("2025Q3", "2025-12-19T12:41:00Z"), ("2025Q4", "2026-03-20T12:58:00Z"),
               ("2026Q1", "2026-06-19T13:22:00Z"), ("2026Q2", "2026-09-18T12:47:00Z")):
    OWNERS["stmt_" + q] = dict(creator="Halcroft Rebate Operations", last_by="Halcroft Rebate Operations",
                               created=mod, modified=mod, company="Halcroft Pharmacy Solutions")
STAMPS = {"policy": b"D:20240314150000+00'00'", "review": b"D:20261012194500+00'00'",
          "exhibit": b"D:20240612160000+00'00'",
          "emails": b"D:20261014131500+00'00'", "rec25": b"D:20250930141000+00'00'"}
MTIME = (2026, 10, 9, 18, 30, 0)


def t(k):
    return os.path.join(TARGET, A.FILES[k])


def fy2025_reconciliation(w):
    """The PBM's fiscal 2025 figures as its reconciliation states them: brand claims by channel and quarter about the
    fiscal 2026 level a year earlier, the remittances from the April to June 2025 statement and its neighbours."""
    import numpy as np
    rng = np.random.default_rng(W.SEED + 25)
    base = {k: [0, 0, 0, 0] for k in range(4)}
    for c in w.claims:
        if c.get("compound") or c["rev"]:
            continue
        q = [f[0] for f in W.FQ].index(W.fq_of(c["d"]))
        ch = c["fee_key"]
        base[q][["RETAIL30", "RETAIL90", "MAIL", "SPECIALTY"].index(ch)] += 1
    out = []
    labels = ["Jul-Sep 2024", "Oct-Dec 2024", "Jan-Mar 2025", "Apr-Jun 2025"]
    for q in range(4):
        n = [int(round(x * rng.uniform(0.90, 0.96))) for x in base[q]]
        g = sum(a * b for a, b in zip(n, [W.GUARANTEE[k] for k in ("RETAIL30", "RETAIL90", "MAIL", "SPECIALTY")]))
        rem = round(g * float(rng.uniform(0.985, 1.06)), 2)
        out.append(dict(q=labels[q], n=n, g=round(g, 2), rem=rem, sf=round(max(0.0, g - rem), 2)))
    return out


def pack():
    import docs as DOC
    import pack as PK
    import postprocess as PP
    shutil.rmtree(TARGET, ignore_errors=True)
    os.makedirs(TARGET)
    w = W.build()
    n = {}
    n["claims"] = PK.claims_csv(t("claims"), w)
    n["drug"] = PK.drug_file(t("drug"), w)
    n["network"] = PK.pharmacy_network(t("network"), w)
    n["roster"] = PK.member_roster(t("roster"), w)
    for q in A.STMT_Q:
        n["stmt_" + q] = PK.remittance(t("stmt_" + q), w, q)
    DOC.policy(t("policy"))
    DOC.clinical_review(t("review"), w)
    DOC.exhibit_c(t("exhibit"))
    DOC.emails(t("emails"))
    DOC.reconciliation_fy2025(t("rec25"), fy2025_reconciliation(w))
    for k, o in OWNERS.items():
        PP.normalize_ooxml(t(k), excel=True, **o)
    for k, stamp in STAMPS.items():
        PP.normalize_pdf(t(k), stamp, stamp)
    stamp_tree(TARGET)
    return w, n


def stamp_tree(root):
    import time
    ts = time.mktime(MTIME + (0, 0, -1))
    for dp, _, fs in os.walk(root):
        for f in fs:
            os.utime(os.path.join(dp, f), (ts, ts))


def digest(root):
    h = hashlib.md5()
    for dp, _, fs in sorted(os.walk(root)):
        for f in sorted(fs):
            fp = os.path.join(dp, f)
            h.update(os.path.relpath(fp, root).encode())
            h.update(open(fp, "rb").read())
    return h.hexdigest()


def cut_zip():
    zp = os.path.join(TASK, "target.zip")
    if os.path.exists(zp):
        os.remove(zp)
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo("target/" + f, date_time=MTIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, f), "rb").read())
    return hashlib.md5(open(zp, "rb").read()).hexdigest()


def full():
    import goldfiles as GF
    import metadata as MD
    w, n = pack()
    figs = GF.write(GOLDEN, TARGET)
    MD.write(os.path.join(TASK, "metadata.json"), n)
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    stamp_tree(GOLDEN)
    return digest(TARGET), digest(GOLDEN), n


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "pack":
        w, n = pack()
        print(json.dumps(n))
        return
    d1, g1, n = full()
    d2, g2, _ = full()
    assert (d1, g1) == (d2, g2), "the two builds differ"
    import writeup as WU
    WU.write(TASK)
    z = cut_zip()
    print("byte-identical: target %s golden %s; target.zip %s; files %s" % (d1, g1, z, json.dumps(n)))


if __name__ == "__main__":
    main()
