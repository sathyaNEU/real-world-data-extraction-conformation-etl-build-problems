"""task464 architecture 9: scrub the toolchain out of the containers and fix every embedded timestamp.

reportlab stamps its name into each PDF's Producer and openpyxl its own into the workbook properties; both are
writer signatures (leak.py sweep 10, reduce-house-fixes H1). The PDF fix is an equal-length, case-preserving
replacement, so every cross-reference offset stays valid. Each file gets the date its author would have saved it,
which also makes two rebuilds byte identical.
"""
import os, re, zipfile, shutil

NEUTRAL_PDF = "docmaster"          # same length as "reportlab"
SAVED = {
    "statin_continuity_sessions_brief.pdf": "20261203101500",
    "icb_cvd_repeat_return_2025_spec.pdf": "20260715143000",
    "pcn_practice_profiles_2026.xlsx": "2026-10-05T11:20:00Z",
    "statin_sessions_2027.xlsx": "2026-12-04T16:40:00Z",
}
AUTHOR = {"pcn_practice_profiles_2026.xlsx": b"Hensey Vale PCN network manager",
          "statin_sessions_2027.xlsx": b"Hensey Vale PCN data and digital"}
DEFAULT_PDF = "20261203101500"
DEFAULT_XLSX = "2026-12-04T16:40:00Z"


def scrub_pdf(path):
    b = open(path, "rb").read()
    stamp = SAVED.get(os.path.basename(path), DEFAULT_PDF).encode()

    def rep(m):
        s = m.group(0).decode("latin-1")
        return "".join(n.upper() if ch.isupper() else n for ch, n in zip(s, NEUTRAL_PDF)).encode("latin-1")
    nb = re.sub(rb"[Rr][Ee][Pp][Oo][Rr][Tt][Ll][Aa][Bb]", rep, b)
    nb = re.sub(rb"D:\d{14}", b"D:" + stamp, nb)
    did = b"5c2e9a07d41b38f6a90e7c13b8d2f461" if "brief" in os.path.basename(path) else b"0b7f13c95ae24d6081c3f7a2de649b58"
    nb = re.sub(rb"/ID\s*\[\s*<([0-9a-fA-F]{32})>\s*<([0-9a-fA-F]{32})>\s*\]",
                lambda m: b"/ID [<" + did + b"> <" + did + b">]", nb)
    assert len(nb) == len(b), (len(nb), len(b))
    if nb != b:
        open(path, "wb").write(nb)
        return True
    return False


def scrub_xlsx(path):
    stamp = SAVED.get(os.path.basename(path), DEFAULT_XLSX).encode()
    y, mo, d = (int(x) for x in stamp[:10].decode().split("-"))
    hh, mm = int(stamp[11:13]), int(stamp[14:16])
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        data = {n: z.read(n) for n in names}
    for n in list(data):
        if n.startswith("docProps/") or n.endswith(".xml") or n.endswith(".rels"):
            t = data[n]
            nt = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Excel</Application>", t)
            nt = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", nt)
            nt = re.sub(rb"(<dc:creator[^>]*>)[^<]*(</dc:creator>)", rb"\g<1>" + AUTHOR.get(os.path.basename(path), b"Hensey Vale PCN")
                        + rb"\g<2>", nt)
            if b"<dc:creator" in nt and b"lastModifiedBy" not in nt:
                nt = nt.replace(b"</cp:coreProperties>", b"<cp:lastModifiedBy>" + AUTHOR.get(os.path.basename(path), b"Hensey Vale PCN")
                                + b"</cp:lastModifiedBy></cp:coreProperties>")
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
            out.append((n, "pdf", scrub_pdf(p)))
        elif n.endswith(".xlsx"):
            out.append((n, "xlsx", scrub_xlsx(p)))
    return out


if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for folder in ("target", "golden"):
        d = os.path.join(base, folder)
        if os.path.isdir(d):
            print(folder, run(d))
