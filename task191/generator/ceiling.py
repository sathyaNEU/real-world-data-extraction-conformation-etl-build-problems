"""The ceiling, measured on the cut pack: target.zip is unpacked and read twice, once on the cracker's route (lands
the call, runs the hygiene battery, executes every filed rule) and once on the mirror's (stops at the decided-alert
reading of the call), and every ask figure is scored against the golden.

    python3 task191/generator/ceiling.py

Weights follow supplemental-stumping Part 0: a response on the call banks 45 before any ask (recommendation and
critical components 37, instruction-following 8), one off the call 12, and the asks carry 55, scored two ways (each
figure its own criterion, and each table row one criterion that holds only when every figure in it does); the worse
of the two is reported.
"""
import hashlib
import os
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402
import common as C     # noqa: E402

ZIP = os.path.join(C.TASK, "target.zip")
Q = ["2025 Q4", "2026 Q1", "2026 Q2", "2026 Q3"]
M = ["2026-%02d" % m for m in range(1, 11)]
ON_CALL, OFF_CALL, ASKS = 45.0, 12.0, 55.0


def score(P, gold_a, gold_b, attr, quarter, read, corrections):
    a = P.ask_investigations(attribute=attr, quarter=quarter)
    b = P.ask_sars(read=read, corrections=corrections)
    cells_a = [(c, q) for c in C.CODES for q in Q]
    cells_b = [(m, k) for m in M for k in ("initial", "continuing")]
    ha = sum(a.get(k, 0) == gold_a.get(k, 0) for k in cells_a)
    hb = sum(b.get(k, 0) == gold_b.get(k, 0) for k in cells_b)
    rows_a = sum(all(a.get((c, q), 0) == gold_a.get((c, q), 0) for q in Q) for c in C.CODES)
    rows_b = sum(all(b.get((m, k), 0) == gold_b.get((m, k), 0) for k in ("initial", "continuing")) for m in M)
    per_cell = (ha + hb) / float(len(cells_a) + len(cells_b))
    per_row = (rows_a + rows_b) / float(len(C.CODES) + len(M))
    return dict(ask_a="%d of %d" % (ha, len(cells_a)), ask_b="%d of %d" % (hb, len(cells_b)),
                rows="%d of %d" % (rows_a + rows_b, len(C.CODES) + len(M)), share=max(per_cell, per_row))


def main():
    sha = hashlib.sha256(open(ZIP, "rb").read()).hexdigest()
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(ZIP) as z:
            z.extractall(tmp)
        P = A.Pack(tmp)
        gold, _ = P.call("golden")
        gold_a, gold_b = P.ask_investigations(), P.ask_sars()
        rows = []
        # the cracker: on the call; each investigation credited to its first alert; each filing typed by its
        # prior-report field (empty is initial, a cited report's own activity is a correction, left out)
        cr = score(P, gold_a, gold_b, "lowest_id", "opened", "field", False)
        st, _ = P.call("golden")
        rows.append(("cracker", st == gold, cr))
        # the mirror: the decided alerts' conversion; every investigation an escalated alert of the scenario sits
        # in; every filing citing a prior counted as continuing activity
        mi = score(P, gold_a, gold_b, "every", "opened", "prior_only", False)
        st, _ = P.call("decided_only")
        rows.append(("mirror", st == gold, mi))
    print("target.zip sha256 %s" % sha)
    out = {}
    for name, on, s in rows:
        total = (ON_CALL if on else OFF_CALL) + ASKS * s["share"]
        out[name] = dict(on_call=on, ask_a=s["ask_a"], ask_b=s["ask_b"], rows=s["rows"],
                         ask_share=round(100 * s["share"], 1), total=round(total, 1))
        print("%-8s call %-5s ask A %-9s ask B %-8s rows %-8s ask weight kept %5.1f%%  total %5.1f" % (
            name, "on" if on else "off", s["ask_a"], s["ask_b"], s["rows"], 100 * s["share"], total))
    pair = (out["cracker"]["total"] + out["mirror"]["total"]) / 2.0
    both_on = ON_CALL + ASKS * max(r[2]["share"] for r in rows)
    print("pair ceiling (cracker and mirror) %.1f; both on the call %.1f; mirror leakage %.1f%% of ask weight" % (
        pair, both_on, out["mirror"]["ask_share"]))
    return 0 if pair <= 60 and both_on <= 60 and out["mirror"]["ask_share"] < 50 else 1


if __name__ == "__main__":
    sys.exit(main())
