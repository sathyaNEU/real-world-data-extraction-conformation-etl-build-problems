"""Build the pack under target/: the clean truth (sim.py), the feeds and workbooks (pack.py), the standard and the
request (docs.py), every container scrubbed of the library that wrote it."""
import os

import docs
import pack
import params as P
import postprocess
import sim

FILES = pack.FILES
PACK = list(FILES)
DISTRACTORS = pack.DISTRACTORS
CONTEXT = pack.CONTEXT
OFFICE = {"plan": ("2026-09-22T08:31:00Z", "2026-10-14T13:05:00Z"),
          "register": ("2026-10-12T06:40:00Z", "2026-11-02T07:18:00Z")}


def run(target):
    os.makedirs(target, exist_ok=True)
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    w = sim.world()
    pack.write_tables(w, target)
    docs.standard(F["standard"])
    docs.request(F["request"])
    postprocess.scrub(F["standard"], "Microsoft Word 2019", "2026-03-02")
    for k, (created, modified) in OFFICE.items():
        postprocess.scrub(F[k], P.ORG, modified[:10])
        postprocess.finish_office(F[k], created, modified, P.ORG)
    return w
