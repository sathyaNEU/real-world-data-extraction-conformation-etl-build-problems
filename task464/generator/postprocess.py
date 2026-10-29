"""task464 architecture 10: scrub the toolchain out of the containers and fix every embedded timestamp.

reportlab stamps its name into each PDF's Producer and openpyxl its own into the workbook properties; both are writer
signatures (leak.py sweep 10, reduce-house-fixes H1). The PDF fix is an equal-length, case-preserving replacement, so
every cross-reference offset stays valid. Each file gets the date its author would have saved it, which also makes two
rebuilds byte identical.
"""
import hashlib
import os
import re
import shutil
import zipfile

NEUTRAL_PDF = "docmaster"          # same length as "reportlab"
SAVED = {
    "losses_programme_2027-28_brief.pdf": "20261118101500",
    "hv_conductor_data_EDS-02-0310.pdf": "20240903142000",
    "iis_reporting_definitions_2025-26.pdf": "20260514093000",
    "line_loss_factors_2025-26.pdf": "20250228120000",
    "hv_network_model.xlsx": "2026-06-12T07:42:00Z",
    "generator_hire_2025-26.xlsx": "2026-04-09T15:05:00Z",
    "losses_programme_2027.xlsx": "2026-11-30T16:20:00Z",
}
AUTHOR = {"hv_network_model.xlsx": b"NMS export service",
          "generator_hire_2025-26.xlsx": b"Generation team, Marchway Power Networks",
          "losses_programme_2027.xlsx": b"Network losses strategy"}


def scrub_pdf(path):
    b = open(path, "rb").read()
    name = os.path.basename(path)
    stamp = SAVED[name].encode()

    def rep(m):
        s = m.group(0).decode("latin-1")
        return "".join(n.upper() if ch.isupper() else n for ch, n in zip(s, NEUTRAL_PDF)).encode("latin-1")
    nb = re.sub(rb"[Rr][Ee][Pp][Oo][Rr][Tt][Ll][Aa][Bb]", rep, b)
    nb = re.sub(rb"D:\d{14}", b"D:" + stamp, nb)
    did = hashlib.md5(("mpn:" + name).encode()).hexdigest().encode()
    nb = re.sub(rb"/ID\s*\[\s*<([0-9a-fA-F]{32})>\s*<([0-9a-fA-F]{32})>\s*\]",
                lambda m: b"/ID [<" + did + b"> <" + did + b">]", nb)
    assert len(nb) == len(b), (len(nb), len(b))
    if nb != b:
        open(path, "wb").write(nb)
    return True


def scrub_xlsx(path):
    name = os.path.basename(path)
    stamp = SAVED[name].encode()
    y, mo, d = (int(x) for x in stamp[:10].decode().split("-"))
    hh, mm = int(stamp[11:13]), int(stamp[14:16])
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        data = {n: z.read(n) for n in names}
    who = AUTHOR.get(name, b"Marchway Power Networks")
    for n in list(data):
        if n.startswith("docProps/") or n.endswith(".xml") or n.endswith(".rels"):
            t = data[n]
            nt = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Excel</Application>", t)
            nt = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", nt)
            nt = re.sub(rb"(<dc:creator[^>]*>)[^<]*(</dc:creator>)", rb"\g<1>" + who + rb"\g<2>", nt)
            if b"<dc:creator" in nt and b"lastModifiedBy" not in nt:
                nt = nt.replace(b"</cp:coreProperties>", b"<cp:lastModifiedBy>" + who + b"</cp:lastModifiedBy></cp:coreProperties>")
            nt = re.sub(rb"[Oo]pen[Pp]yxl", b"Microsoft Excel", nt)
            nt = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>" + stamp + rb"\g<2>", nt)
            nt = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + stamp + rb"\g<2>", nt)
            data[n] = nt
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            zi = zipfile.ZipInfo(n, date_time=(y, mo, d, hh, mm, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data[n])
    shutil.move(tmp, path)
    return True


def run(folder):
    out = []
    for n in sorted(os.listdir(folder)):
        p = os.path.join(folder, n)
        if n.endswith(".pdf"):
            out.append((n, scrub_pdf(p)))
        elif n.endswith(".xlsx"):
            out.append((n, scrub_xlsx(p)))
    return out
