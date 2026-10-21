"""The personas the built task carries, checked by guard.py people against the corpus name index: every name in the
pack and the goldens is one guard.py names drew for this build."""
import os
import re
import subprocess
import sys

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
GUARD = os.path.join(HERE, "..", "..", ".claude", "skills", "fingerprint", "guard.py")


def found():
    r = subprocess.run([sys.executable, GUARD, "people", "task480"], capture_output=True, text=True)
    m = re.search(r"personas found in task480: (.*)", r.stdout)
    names = {p.strip() for p in m.group(1).split(",")} if m and m.group(1).strip() != "none" else set()
    return r.returncode, names


def ok():
    rc, names = found()
    allowed = {v[0] for v in W.PEOPLE.values()}
    return rc == 0 and names <= allowed, sorted(names - allowed)
