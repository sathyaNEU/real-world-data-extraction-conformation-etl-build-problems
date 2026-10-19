"""The cracker and the mirror on the cut pack, scored against figures.json.

The cracker lands the call and runs the hygiene battery (key uniqueness on claim numbers, job references and policy
numbers, exact duplicates, unmatched joins through the crosswalk, amounts against units), then executes the basis
note's sections 3 and 4 as written: the partner's jobs billed to the Society, a job's lines one claim, beside the
windscreen claims of repairers the Society did not instruct (claims with no supplier), and each theft claim with a
cost dated by its loss date, net of its own salvage. The mirror stops off the call (the reported frequency) and
takes the other attractive reading of each ask: the claims exports alone for windscreen, and thefts keyed by the
police reference as written with the 2025 statements only.

Weights are the skill's: 38 for the call and its components, 7 for instruction-following, 55 for the asks, a figure
a hit within half a unit of its stated rounding."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A    # noqa: E402
import common as K      # noqa: E402
import pack as PK       # noqa: E402


def region_of(P, ref, day):
    """The region on the day, from the policy year covering it, or (a record dated after its policy year ended) the
    policy's last year before the day."""
    t = PK.term_for(P, ref, day)
    if t is None:
        cands = [t for r in (ref, P["xw"].get(ref)) for t in P["by_ref"].get(r, []) if t["start"] <= day]
        t = max(cands, key=lambda t: t["start"])
        day = min(day, t["end"] - PK.dt.timedelta(days=1))
    d, _ = PK.state_on(t, day)
    return P["rmap"].region(d, day)


def glass_by_source(P, E25c, partner=True, claims=True, supplier_split=True):
    n = {c: 0 for c in K.CODES}
    cost = {c: 0.0 for c in K.CODES}
    if partner:
        jobs = {}
        for g in P["glass"]:
            if g["billed"] != K.SHORT:
                continue
            j = jobs.setdefault(g["job"], dict(booked=g["booked"], ref=g["ref"], amount=0.0))
            j["amount"] += g["net"] + g["vat"]
        for j in jobs.values():
            if j["booked"].year == 2025:
                r = region_of(P, j["ref"], j["booked"])
                n[r] += 1
                cost[r] += j["amount"]
    if claims:
        for c in P["claims"]:
            if c["type"] != "WSC" or c["notified"].year != 2025 or c["incurred"] <= 0:
                continue
            if supplier_split and c["supplier"]:
                continue
            r = region_of(P, c["ref"], c["notified"])
            n[r] += 1
            cost[r] += c["incurred"]
    return ({c: 100.0 * n[c] / E25c[c] for c in K.CODES}, {c: cost[c] / n[c] if n[c] else 0.0 for c in K.CODES})


def theft_by_claim(P, E25):
    net = {}
    for s in P["salvage"]:
        net[s["claim"]] = net.get(s["claim"], 0.0) + s["net"]
    n = {c: 0 for c in K.CODES}
    cost = {c: 0.0 for c in K.CODES}
    for c in P["claims"]:
        if c["type"] != "THF" or c["loss"].year != 2025 or c["incurred"] <= 0:
            continue
        r = region_of(P, c["ref"], c["loss"])
        n[r] += 1
        cost[r] += c["incurred"] - net.get(c["no"], 0.0)
    return ({c: 1000.0 * n[c] / E25[c] for c in K.CODES}, {c: cost[c] / n[c] for c in K.CODES})


def theft_by_raw_reference(P, E25, years=(2025,)):
    raw = {}
    for c in P["claims"]:
        if c["type"] != "THF":
            continue
        key = c["police"] if c["sys"] == "P" else "L:" + c["police"]
        raw.setdefault(key, []).append(c)
    net = {}
    for s in P["salvage"]:
        if s["sold"].year in years:
            net[s["claim"]] = net.get(s["claim"], 0.0) + s["net"]
    n = {c: 0 for c in K.CODES}
    cost = {c: 0.0 for c in K.CODES}
    for cs in raw.values():
        first = min(cs, key=lambda c: (c["loss"], c["notified"], c["no"]))
        inc = sum(c["incurred"] for c in cs)
        if first["loss"].year != 2025 or inc <= 0:
            continue
        r = region_of(P, first["ref"], first["loss"])
        n[r] += 1
        cost[r] += inc - sum(net.get(c["no"], 0.0) for c in cs)
    return ({c: 1000.0 * n[c] / E25[c] for c in K.CODES}, {c: cost[c] / n[c] for c in K.CODES})


def hits(fig_freq, fig_avg, freq, avg):
    h = 0
    rows = []
    for c in K.CODES:
        nm = K.NAME[c]
        hf = abs(freq[c] - fig_freq[nm]) < 0.05 + 1e-9
        ha = abs(avg[c] - fig_avg[nm]) < 0.5 + 1e-9
        h += hf + ha
        rows.append((nm, round(freq[c], 2), fig_freq[nm], hf, round(avg[c], 1), fig_avg[nm], ha))
    return h, rows


def run(task, quiet=False):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    target = os.path.join(task, "target")
    P = PK.load(target)
    E25 = {k[0]: v for k, v in PK.exposure(P, (2025,)).items()}
    E25c = {k[0]: v for k, v in PK.exposure(P, (2025,), cover="COMP").items()}
    total = 32
    # the cracker
    fa, aa = glass_by_source(P, E25c)
    fb, ab = theft_by_claim(P, E25)
    ca, rows_a = hits(fig["ask_a"]["frequency"], fig["ask_a"]["average"], fa, aa)
    cb, rows_b = hits(fig["ask_b"]["frequency"], fig["ask_b"]["average"], fb, ab)
    # the mirror
    ma_f, ma_a = glass_by_source(P, E25c, partner=False, supplier_split=False)
    mb_f, mb_a = theft_by_raw_reference(P, E25)
    ma, rows_ma = hits(fig["ask_a"]["frequency"], fig["ask_a"]["average"], ma_f, ma_a)
    mb, rows_mb = hits(fig["ask_b"]["frequency"], fig["ask_b"]["average"], mb_f, mb_a)
    cracker = 38 + 7 + 55.0 * (ca + cb) / total
    mirror = 5 + 7 + 55.0 * (ma + mb) / total
    pair = (cracker + mirror) / 2
    if not quiet:
        for title, rows in (("cracker, Ask A", rows_a), ("cracker, Ask B", rows_b), ("mirror, Ask A", rows_ma),
                            ("mirror, Ask B", rows_mb)):
            print(title)
            for r in rows:
                print("   %-26s freq %7.2f golden %5.1f %-5s  avg %8.1f golden %5d %s" % r)
        print("cracker keeps %d of %d ask figures; mirror keeps %d of %d" % (ca + cb, total, ma + mb, total))
        print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f per cent of the ask weight"
              % (cracker, mirror, pair, 100.0 * (ma + mb) / total))
    return dict(cracker_hits=ca + cb, mirror_hits=ma + mb, total=total, pair=pair, cracker=cracker, mirror=mirror)


if __name__ == "__main__":
    r = run(os.path.dirname(HERE))
    sys.exit(0 if r["cracker_hits"] == 0 else 1)
