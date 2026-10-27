"""Builds task141's pack into target/ and the golden deliverables into golden/, writes generator/figures.json, and
cuts target.zip; two runs are byte-identical.

    python3 task141/generator/build.py          # the whole build
    python3 task141/generator/build.py pack     # the pack only
"""
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

import common as K        # noqa: E402

STAMPS = {K.ACT_PDF: b"D:20260514153000-05'00'", K.PLAN_PDF: b"D:20260708101500-05'00'",
          K.REPORT: b"D:20251015094000-05'00'"}


def t(name):
    return os.path.join(TARGET, name)


def pack():
    import docs as DOC
    import pack as PK
    import pack_read as PR
    import postprocess as PP
    import world as WD
    for d in (TARGET, GOLDEN):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    W = WD.simulate()
    PK.assign_ids(W)
    r1, r2 = PK.register_rows(W)
    n = {}
    n[K.CMS1] = K.write_csv(t(K.CMS1), PK.CMS1_COLS, r1, crlf=True)
    n[K.CMS2] = K.write_csv(t(K.CMS2), PK.CMS2_COLS, r2)
    n[K.ORDERS] = K.write_csv(t(K.ORDERS), PK.ORDER_COLS, PK.order_rows(W))
    n[K.PETITIONS] = K.write_csv(t(K.PETITIONS), PK.PET_COLS, PK.petition_rows(W))
    B = PK.bookings(W)
    W.B = B
    n[K.BOOKINGS] = K.write_csv(t(K.BOOKINGS), PK.BOOK_COLS, PK.booking_rows(W, B), crlf=True)
    n[K.PERSONS] = K.write_csv(t(K.PERSONS), PK.PERSON_COLS, PK.person_rows(W))
    n[K.HEADCOUNT] = K.write_csv(t(K.HEADCOUNT), PK.HEAD_COLS, PK.headcount_rows(W, B), crlf=True)
    DOC.write_act(t(K.ACT_PDF))
    DOC.write_plan(t(K.PLAN_PDF))
    P = PR.read(TARGET)
    DOC.write_report(t(K.REPORT), DOC.report_figures(P["cms1"], P["cms2"], P["pets"]))
    DOC.write_jms_codes(t(K.JAIL_CODES))
    DOC.write_office_codes(t(K.OFFICE_CODES))
    DOC.write_court_codes(t(K.COURT_CODES))
    PP.normalize_ooxml(t(K.COURT_CODES), "Megan Chambers", "Circuit Court Clerk's Office", "2023-05-30T14:12:00Z",
                       "2025-01-21T16:47:00Z", title="Code table", excel=True, company="Okelan County Circuit Court")
    for nm, stamp in STAMPS.items():
        PP.normalize_pdf(t(nm), stamp, stamp)
    return W, n


def gpath(name):
    return os.path.join(GOLDEN, name)


def main():
    W, n = pack()
    import golden as G
    import goldfiles as GF
    figs = GF.write(gpath, G.compute())
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    import writeup
    writeup.main()
    import metadata
    metadata.main()
    cut_zip()
    print("built: %d files in target/, %d in golden/" % (len(os.listdir(TARGET)), len(os.listdir(GOLDEN))))
    print(json.dumps(n))
    return W


def cut_zip():
    """each file keeps the date its source produced it (metadata.SOURCES) and a working-hours time of its own"""
    import hashlib
    import metadata
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for nm in sorted(os.listdir(TARGET)):
            y, mo, d = (int(x) for x in metadata.SOURCES[nm][1].split("-"))
            h = int(hashlib.md5(nm.encode()).hexdigest(), 16)
            zi = zipfile.ZipInfo(nm, date_time=(y, mo, d, 7 + h % 11, (h // 11) % 60, ((h // 660) % 30) * 2))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, nm), "rb").read())


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "pack":
        W, n = pack()
        print(json.dumps(n, indent=1))
    else:
        main()
