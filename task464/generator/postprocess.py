"""task464 architecture 8: scrub the toolchain out of the containers.

reportlab stamps its name into every PDF's Producer and openpyxl stamps its own into the workbook properties.
Both are writer signatures (leak.py sweep 10, reduce-house-fixes H1). The PDF fix is an equal-length,
case-preserving replacement so every byte offset in the cross-reference table stays valid. The workbook fix
rewrites the zip with fixed member timestamps, which also makes two rebuilds byte identical.
"""
import os, re, zipfile, shutil

NEUTRAL_PDF = "docmaster"          # same length as "reportlab"
FIXED_TIME = (2026, 11, 18, 0, 0, 0)


def scrub_pdf(path):
    b = open(path, "rb").read()
    def rep(m):
        s = m.group(0).decode("latin-1")
        out = []
        for ch, n in zip(s, NEUTRAL_PDF):
            out.append(n.upper() if ch.isupper() else n)
        return "".join(out).encode("latin-1")
    nb = re.sub(rb"[Rr][Ee][Pp][Oo][Rr][Tt][Ll][Aa][Bb]", rep, b)
    # reportlab stamps a creation time and a document id derived from it, so two builds differ. Both are
    # replaced with fixed values of exactly the same length, which keeps every xref offset valid.
    nb = re.sub(rb"D:\d{14}", b"D:20261118090000", nb)
    nb = re.sub(rb"/ID\s*\[\s*<([0-9a-fA-F]{32})>\s*<([0-9a-fA-F]{32})>\s*\]",
                lambda m: b"/ID [<" + b"4a7c1e05b3d94f2286ae01cf37bd5e90" + b"> <"
                          + b"4a7c1e05b3d94f2286ae01cf37bd5e90" + b">]", nb)
    assert len(nb) == len(b), (len(nb), len(b))
    if nb != b:
        open(path, "wb").write(nb)
        return True
    return False


def scrub_xlsx(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        data = {n: z.read(n) for n in names}
    changed = False
    for n in list(data):
        if n.startswith("docProps/") or n.endswith(".xml") or n.endswith(".rels"):
            t = data[n]
            nt = re.sub(rb"[Oo]pen[Pp]yxl", b"Workbook", t)
            # openpyxl writes the build time into the document properties
            nt = re.sub(rb"<dcterms:created[^>]*>[^<]*</dcterms:created>",
                        b'<dcterms:created xsi:type="dcterms:W3CDTF">2026-11-18T09:00:00Z</dcterms:created>', nt)
            nt = re.sub(rb"<dcterms:modified[^>]*>[^<]*</dcterms:modified>",
                        b'<dcterms:modified xsi:type="dcterms:W3CDTF">2026-11-18T09:00:00Z</dcterms:modified>', nt)
            if nt != t:
                data[n] = nt
                changed = True
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            zi = zipfile.ZipInfo(n, date_time=FIXED_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data[n])
    shutil.move(tmp, path)
    return changed


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
            for n, k, ch in run(d):
                print("  %-8s %-46s %s" % (folder, n, "scrubbed" if ch else "already clean"))
