"""Build the pack into a folder: python3 build.py <folder> (default ../target)."""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs as D    # noqa: E402
import pack as P    # noqa: E402
import world as W   # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
FILE_TIME = (2026, 10, 9, 8, 40, 0)


def build(folder=TARGET):
    if os.path.isdir(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)
    S = W.simulate()
    P.lab_and_runs(S, folder)
    P.ec_loggers(S, folder)
    P.gauges(S, folder)
    P.register(folder)
    P.mines(S, folder)
    P.distractors(S, folder)
    D.schedule(os.path.join(folder, P.FILES["schedule"]))
    import datetime as dt
    t = dt.datetime(*FILE_TIME).timestamp()
    for f in os.listdir(folder):
        os.utime(os.path.join(folder, f), (t, t))
    return S


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else TARGET)
    print("built", sorted(os.listdir(sys.argv[1] if len(sys.argv) > 1 else TARGET)))
