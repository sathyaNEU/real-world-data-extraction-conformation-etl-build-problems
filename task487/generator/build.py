"""Builds task487's pack into target/ and the golden deliverables into golden/, writes generator/figures.json, and
cuts target.zip; two runs are byte-identical.

    python3 task487/generator/build.py          # the whole build
    python3 task487/generator/build.py pack     # the pack only
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

import pack_read as PR    # noqa: E402
import world as W         # noqa: E402

NAMES = dict(register=PR.REGISTER, fieldlog=PR.FIELDLOG, sitelink=PR.SITELINK, sites=PR.SITES, events=PR.EVENTS,
             alarms=PR.ALARMS, production=PR.PRODUCTION, vapour=PR.VAPOUR, workorders=PR.WORKORDERS,
             ldar_surveys=PR.LDAR_SURVEYS, ldar_tags=PR.LDAR_TAGS, hauler="hauler_load_tickets_2026.csv",
             salesgas="sales_gas_meter_statements_2026.csv", directive=PR.DIRECTIVE, notes="kesmere_field_data_notes.txt")
GOLD = dict(events="release_events_2026.csv", workbook="release_levy_filing_2026.xlsx")
ORG = "Vennholt Energy Ltd."
OWNERS = {
    "events": dict(creator="EHS Office", last_by="EHS Office", created="2026-01-06T15:02:00Z",
                   modified="2027-01-11T17:48:00Z", company=ORG),
    "vapour": dict(creator="Quellmark Laboratories", last_by="Production Engineering", created="2025-07-02T10:15:00Z",
                   modified="2026-11-30T09:21:00Z", company=ORG),
    "ldar_tags": dict(creator="EHS Office", last_by="EHS Office", created="2025-09-15T21:12:00Z",
                      modified="2027-01-12T16:30:00Z", company=ORG),
}
STAMPS = {"directive": b"D:20250314090000-06'00'"}


def t(k):
    return os.path.join(TARGET, NAMES[k])


def pack():
    import docs as DOC
    import pack as PK
    import postprocess as PP
    for d in (TARGET, GOLDEN):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    w = W.build()
    n = PK.cut({k: t(k) for k in NAMES}, w)
    DOC.directive(t("directive"))
    DOC.notes(t("notes"))
    for k in OWNERS:
        PP.normalize_ooxml(t(k), excel=True, **OWNERS[k])
    for k, stamp in STAMPS.items():
        PP.normalize_pdf(t(k), stamp, stamp)
    return w, n


def gpath(k):
    return os.path.join(GOLDEN, GOLD[k])


def main():
    w, n = pack()
    import goldfiles as GF
    import postprocess as PP
    figs = GF.write(gpath)
    PP.normalize_ooxml(gpath("workbook"), "Charlene Logan", "Charlene Logan", "2027-01-14T15:20:00Z",
                       "2027-01-19T10:42:00Z", title="2026 release-event return and levy", excel=True, company=ORG)
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    import writeup
    writeup.main()
    import metadata
    metadata.main()
    cut_zip()
    print("built: %d files in target/, %d in golden/" % (len(os.listdir(TARGET)), len(os.listdir(GOLDEN))))
    print(json.dumps(n))
    return w


def cut_zip():
    """Each file keeps the date its source produced it (metadata.SOURCES) and a working-hours time of its own."""
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
        w, n = pack()
        print(json.dumps(n, indent=1))
    else:
        main()
