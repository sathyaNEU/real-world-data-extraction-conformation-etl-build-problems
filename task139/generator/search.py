"""Find each pilot segment's outcome stream (world.search_streams) and the payment register's stream, and print the
STREAMS and PAY_STREAM values world.py carries.

    python3 task139/generator/search.py           both
    python3 task139/generator/search.py --pay     the payment stream only (the pilot streams as world.py has them)"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K     # noqa: E402
import payments as PAY  # noqa: E402
import world as W      # noqa: E402

if "--pay" not in sys.argv:
    claims = W._arrivals()
    ids = W._pilot(claims)
    pcs_of = {seg: sorted([claims[i] for i in ids if claims[i].seg == seg], key=lambda c: c.cid) for seg in K.PROG}
    st = W.search_streams(claims, pcs_of)
    print("STREAMS = {%s}" % ", ".join('"%s": %d' % (s, st[s]) for s in K.PROG))
    W.STREAMS = st
W.PAY_STREAM = -1
orig = PAY.payments
orig_clear = PAY.clear
found = {}


def probe(claims, stream=0):
    for k in range(0, 400):
        pays, rets = orig(claims, k)
        if orig_clear(pays):
            found["k"] = k
            return pays, rets
    raise SystemExit("no payment stream")


PAY.payments = probe
PAY.clear = lambda pays: True
W.simulate()
print("PAY_STREAM = %d" % found["k"])
