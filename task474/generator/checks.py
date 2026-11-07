"""The generator's assertions, run on the cut pack under target/ against figures.json.

    python3 task474/generator/checks.py
"""
import datetime as dt
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import figs as F      # noqa: E402
import pack as K      # noqa: E402
import params as P    # noqa: E402
import routes as R    # noqa: E402
import world as W     # noqa: E402

FAILS = []
N = [0]


def ok(label, cond, detail=""):
    N[0] += 1
    print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  [%s]" % (detail,)) if detail != "" else ""))
    if not cond:
        FAILS.append(label)


def pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join((pg.extract_text() or "") for pg in PdfReader(path).pages))


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    meta = json.load(open(os.path.join(TASK, "metadata.json"), encoding="utf-8"))
    files = sorted(os.listdir(TARGET))
    # ---------------------------------------------------------------- input gates
    ok("H1 ten or more files", len(files) >= 10, len(files))
    ok("H2 three or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3, sorted({f.rsplit(".", 1)[1] for f in files}))
    rows = sum(1 for _ in open(os.path.join(TARGET, K.FILES["brindle"]), encoding="utf-8")) - 1
    ok("H3 a file of 25,000 rows or more", rows >= 25000, rows)
    ok("H4 two or more distractors named in metadata.json, none in a file name",
       len(meta["distractors"]) >= 2 and not any("distract" in f for f in files), meta["distractors"])
    ok("H5 the pack is exactly the declared files", files == sorted(K.FILES.values()), files[:3])
    # ---------------------------------------------------------------- the call and the ladder
    people, reg = F.load(TARGET)
    att = R.attempts(people)
    gold = fig["call"]["pass_mark"]
    ok("R0 the golden pass mark recomputes from the cut pack", R.r_matched(att)[0] == gold, gold)
    c = fig["call"]
    ok("R0 the equivalent share sits inside its step with a margin of at least 0.025 on both sides",
       c["share_below_mark"] - c["p_equivalent"] >= 0.025 and c["p_equivalent"] - c["share_at_mark"] >= 0.025,
       (c["share_below_mark"], c["p_equivalent"], c["share_at_mark"]))
    for name, v in fig["ladder"].items():
        if name != "retakes matched on the first score":
            ok("R1 the route '%s' files another mark" % name, v != gold, v)
    ok("R1 the default (same months a year earlier) and the half before the switch both file higher marks",
       fig["ladder"]["same months a year earlier"] > gold and fig["ladder"]["the half before the switch"] > gold)
    ok("R1 no two easy routes average to the golden except across directions",
       (fig["ladder"]["same months a year earlier"] + fig["ladder"]["the half before the switch"]) / 2 != gold)
    # the facts the ladder's rungs die to, read on the unchanged old paper
    import numpy as np

    def ft_rate(d0, d1):
        x = np.array(R.first_timers(att, "old", d0, d1))
        return 100.0 * (x >= P.OLD_PASS).mean()
    gaps = [ft_rate(dt.date(y, 4, 1), dt.date(y, 9, 30)) - ft_rate(dt.date(y - 1, 10, 1), dt.date(y, 3, 31))
            for y in range(2021, 2025)] + [ft_rate(dt.date(2020, 4, 1), dt.date(2020, 9, 30)) -
                                           ft_rate(dt.date(2020, 10, 1), dt.date(2021, 3, 31))]
    ok("R2 the summer half's first-time pass rate sits 3 or more points above the winter half in 2020 to 2024",
       min(gaps) >= 3.0, [round(g, 1) for g in gaps])
    rise = ft_rate(dt.date(2025, 10, 1), dt.date(2026, 3, 31)) - ft_rate(dt.date(2024, 10, 1), dt.date(2025, 3, 31))
    ok("R3 the winter half before the switch sits 4 or more points above the one a year earlier (the intake moved)",
       rise >= 4.0, round(rise, 1))
    yr = [100.0 * v["passed"] / v["first_time"] for v in fig["ask_b"].values()]
    ok("R4 the yearly first-time pass rate stays within 2 points from 2021 to 2025", max(yr) - min(yr) <= 2.0,
       [round(v, 1) for v in yr])
    # the standing family converges (SF4, SF5, SF6)
    for band in (1, 2, 5):
        ok("SF5 first scores matched in bands of %d: same mark" % band, R.r_matched(att, band=band)[0] == gold)
    for d0 in (dt.date(2020, 1, 1), dt.date(2021, 1, 1), dt.date(2023, 1, 1)):
        ok("SF4 the resit history from %d: same mark" % d0.year, R.r_matched(att, d0=d0)[0] == gold)
    ok("SF4 the resit history to the switch (fails to March 2026): same mark",
       R.r_matched(att, d1=dt.date(2026, 3, 31))[0] == gold)
    ok("SF6 every resit, not only resits of a first sitting: same mark", R.r_matched(att, first_only=False)[0] == gold)
    # SF2: reaches 65 means at or above; SF3: the lowest mark with no larger share is also the nearest share
    cs = [y for _, y in R.cross_switch(att)]
    import numpy as np
    a = np.array(cs)
    shares = {y: float((a >= y).mean()) for y in range(30, 46)}
    near = min(shares, key=lambda y: abs(shares[y] - c["p_equivalent"]))
    ok("SF3 the mark whose share is nearest the equivalent share is the same mark", near == gold, near)
    # clean truth: one latent scale, equal reliability, so every equivalent group gives the same mark
    old_cut = (P.OLD_PASS - 0.5 - P.OLD_A) / P.OLD_B
    truth = min(y for y in range(0, 61) if (y - 0.5 - P.NEW_A) / P.NEW_B >= old_cut)
    ok("T1 the latent model's equivalence (any equivalent group) gives the golden", truth == gold, truth)
    world = W.build()
    watt = R.attempts({i: p["sittings"] for i, p in enumerate(world)})
    ok("T2 the matched route on the world's own sittings gives the golden", R.r_matched(watt)[0] == gold)
    ok("T3 the default route on the world's own sittings files the wrong mark", R.r_same_months(watt)[0] != gold)
    # SF8: UK date against the UTC date; SF9: board numbers against persons
    p_utc, _ = F.load(TARGET, zone="utc")
    ok("SF8 remote sittings dated by UTC: same mark", R.r_matched(R.attempts(p_utc))[0] == gold)
    p_board, _ = F.load(TARGET, identity="board")
    ok("SF9 each board number taken as a candidate: same mark", R.r_matched(R.attempts(p_board))[0] == gold)
    # ---------------------------------------------------------------- the asks and their device
    a_g, b_g = F.ask_a(people), F.ask_b2(people)
    a_c, b_c = F.ask_a(p_board), F.ask_b2(p_board)
    moved_a = sum(a_g[k][i] != a_c[k][i] for k in a_g for i in (0, 1))
    moved_b = sum(b_g[k][i] != b_c[k][i] for k in b_g for i in (0, 1))
    ok("SF10 board numbers as candidates move at least 15 of the 18 monthly figures", moved_a >= 15, moved_a)
    ok("SF10 board numbers as candidates move at least 8 of the 10 yearly figures", moved_b >= 8, moved_b)
    ok("SF11 the asks recompute from the cut pack", {k: {"first_time": v[0], "resitting": v[1]} for k, v in a_g.items()}
       == fig["ask_a"] and {k: {"first_time": v[0], "passed": v[1]} for k, v in b_g.items()} == fig["ask_b"])
    # SF1: an equivalent group (AP-3 section 2) and SF7: what a sitting is (AP-3 section 4)
    ap3 = pdf_text(os.path.join(TARGET, K.FILES["ap3"]))
    ok("SF1 AP-3 files the estimand: the lowest raw mark no larger share of an equivalent group reaches",
       "lowest raw mark that no larger share of an equivalent group" in ap3 and "whichever paper it sat" in ap3)
    ok("SF7 AP-3 files what a sitting is (a voided or unattended booking is not one)", "is not a sitting of the paper" in ap3)
    ok("SF2 AP-3 reads 'reaches 65' (at or above) and the golden counts 65 as reached",
       "reaches 65" in ap3 and c["p_equivalent"] > 0)
    # ---------------------------------------------------------------- leaks and hygiene
    docs = " ".join(pdf_text(os.path.join(TARGET, K.FILES[k])) for k in ("ap3", "notice"))
    docs += open(os.path.join(TARGET, K.FILES["request"]), encoding="utf-8").read()
    plant = re.compile(r"retest|practice|\bgains?\b|regression|matched|second sitting|reads higher|equipercentile|cohort",
                       re.I)
    ok("L1 no document names a retest gain, matching or the cohort", not plant.findall(docs), plant.findall(docs))
    ok("L2 the documents read under pypdf (positive control)", "Harrowgate" in docs and len(docs) > 1500)
    js = json.load(open(os.path.join(TARGET, K.FILES["harrowgate"]), encoding="utf-8"))["sittings"]
    ok("L3 no Harrowgate sitting after 30 September 2026", max(s["started_at"] for s in js) < "2026-10-01")
    ok("L4 no register row after the extract", max(g["registered_on"] for g in reg) <= P.EXTRACT.isoformat())
    names = [(g["surname"], g["initials"], g["date_of_birth"]) for g in reg]
    ok("L5 the register carries re-registered candidates (one person, two board numbers)",
       len(names) - len(set(names)) >= 300, len(names) - len(set(names)))
    print("%d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
