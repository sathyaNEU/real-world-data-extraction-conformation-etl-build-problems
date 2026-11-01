"""Office files are zip archives whose entries carry the writer's clock. Rewrite each with its own save time, the
application an office user's copy would name, and the created and modified stamps in its core properties."""
import io
import re
import zipfile

APPS = {"xlsx": b"Microsoft Excel", "pptx": b"Microsoft Office PowerPoint"}


def _core(data, created, modified):
    data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)",
                  b"\\g<1>" + created.strftime("%Y-%m-%dT%H:%M:%SZ").encode() + b"\\g<2>", data)
    data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                  b"\\g<1>" + modified.strftime("%Y-%m-%dT%H:%M:%SZ").encode() + b"\\g<2>", data)
    return data


def _rewrite(raw, kind, created, modified):
    src = zipfile.ZipFile(io.BytesIO(raw))
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for info in sorted(src.infolist(), key=lambda i: i.filename):
            data = src.read(info.filename)
            if info.filename == "docProps/app.xml":
                if b"<Application>" in data:
                    data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>" + APPS[kind] +
                                  b"</Application>", data)
            if info.filename == "docProps/core.xml":
                data = _core(data, created, modified)
            if info.filename.endswith(".xlsx"):
                data = _rewrite(data, "xlsx", created, modified)
            zi = zipfile.ZipInfo(info.filename, date_time=modified.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)
    return out.getvalue()


def save(doc, path, kind, created, modified):
    buf = io.BytesIO()
    doc.save(buf)
    open(path, "wb").write(_rewrite(buf.getvalue(), kind, created, modified))
