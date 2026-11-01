"""Writes the whole of target/ for task133 architecture 4 into a directory."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import docs  # noqa: E402
import pack  # noqa: E402
import world  # noqa: E402
from io_util import set_mtime  # noqa: E402

FILES = sorted([pack.WB, pack.SC, pack.FLEET, pack.PLAN, pack.INV, pack.DOCK, pack.MWB, pack.PRICES, pack.VESSELS,
                pack.CLOSURES, docs.BASIS, docs.APPROVAL, docs.GRADESPEC])
DISTRACTORS = [pack.PRICES, pack.VESSELS, pack.CLOSURES]


def make(out):
    os.makedirs(out, exist_ok=True)
    W = world.make()
    pack.write_weighbridge(W, out)
    pack.write_scaling(W, out)
    pack.write_fleet(W, out)
    pack.write_plan(W, out)
    pack.write_invoices(W, out)
    pack.write_mills(W, out)
    pack.write_distractors(W, out)
    docs.write_basis(out)
    docs.write_approval(out)
    docs.write_gradespec(out)
    present = sorted(os.listdir(out))
    assert present == FILES, set(present) ^ set(FILES)
    for f in present:
        set_mtime(os.path.join(out, f))
    return W


if __name__ == "__main__":
    make(sys.argv[1])
