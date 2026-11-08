"""task197: cut target.zip from target/. Each entry keeps its folder inside the pack (no leading target/), the date its
source issued or extracted it (metadata.json) and a working-hours time of its own, so two cuts are byte-identical."""
import os, sys, json, hashlib, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")


def main():
    meta = {f["path"]: f["issued_or_extracted"] for f in json.load(open(os.path.join(TASK, "metadata.json")))["files"]}
    names = []
    for root, _, files in os.walk(TGT):
        for f in files:
            names.append(os.path.relpath(os.path.join(root, f), TGT).replace(os.sep, "/"))
    out = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for nm in sorted(names):
            y, mo, d = (int(x) for x in meta["target/" + nm].split("-"))
            h = int(hashlib.md5(nm.encode()).hexdigest(), 16)
            zi = zipfile.ZipInfo(nm, date_time=(y, mo, d, 8 + h % 9, (h // 9) % 60, ((h // 540) % 30) * 2))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(TGT, nm), "rb") as fh:
                z.writestr(zi, fh.read())
    print("target.zip: %d entries, %s" % (len(names), hashlib.md5(open(out, "rb").read()).hexdigest()))


if __name__ == "__main__":
    main()
