"""Writes the whole of target/ for task134 architecture 4 into a directory."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import docs  # noqa: E402
import pack  # noqa: E402
import world  # noqa: E402
from io_util import set_mtime  # noqa: E402

FILES = sorted([pack.SURV_A, pack.SURV_B, pack.CERTS, pack.LOADS, pack.REVISION, pack.SAMPLING, pack.LAB, pack.TIDE,
                pack.FLOW, pack.CALLS, docs.NOTICE, docs.LICENCE, docs.BASIS])
DISTRACTORS = [pack.TIDE, pack.FLOW, pack.CALLS]


def make(out):
    os.makedirs(out, exist_ok=True)
    W = world.make()
    pack.write_surveys(W, out)
    pack.write_certificates(W, out)
    pack.write_loads(W, out)
    pack.write_sampling(W, out)
    pack.write_lab(W, out)
    pack.write_distractors(W, out)
    docs.write_notice(out)
    docs.write_licence(out)
    docs.write_basis(out)
    present = sorted(os.listdir(out))
    assert present == FILES, set(present) ^ set(FILES)
    for f in present:
        set_mtime(os.path.join(out, f))
    return W


if __name__ == "__main__":
    make(sys.argv[1])
