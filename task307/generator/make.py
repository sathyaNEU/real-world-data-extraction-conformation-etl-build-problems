"""The whole build in order: python3 task307/generator/make.py [--zip]. Cuts the pack, writes figures.json, runs
the checks and the independent verifier, renders the goldens and the write-up, measures the ask sheet, and with
--zip writes target.zip from the pack."""
import os
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")


def run(script, *args):
    r = subprocess.run([sys.executable, os.path.join(HERE, script)] + list(args), cwd=TASK)
    if r.returncode:
        sys.exit("%s failed" % script)


def zip_pack():
    path = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(TARGET)):
            info = zipfile.ZipInfo("target/" + f, date_time=(2026, 10, 27, 16, 20, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(os.path.join(TARGET, f), "rb") as fh:
                z.writestr(info, fh.read())
    return path


if __name__ == "__main__":
    run("build.py", TARGET)
    run("figs.py", TARGET)
    run("checks.py", TARGET)
    if "--fast" not in sys.argv:
        run("verify.py", TARGET)
    run("golden.py", os.path.join(TASK, "golden"))
    run("writeup.py")
    run("pair.py", TARGET)
    if "--zip" in sys.argv:
        print("zip", zip_pack())
