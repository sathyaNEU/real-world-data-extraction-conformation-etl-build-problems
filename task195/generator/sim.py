"""The clean truth: every specimen of the parallel run, its two screen calls and its panel verdict.

Nothing here knows about mess, documents or the write-up. The roles and the band counts come from
world.py, and every figure the build grades is computed forward from the records this module writes.
"""
import datetime as dt
import math
import random

import world as W

BANDS = ["ge050", "b3050", "b2030", "b1520", "b1015", "lt010"]
LIMITS = {"ge050": (0.0501, 0.3600), "b3050": (0.0301, 0.0499), "b2030": (0.0201, 0.0299),
          "b1520": (0.0151, 0.0199), "b1015": (0.0101, 0.0149), "lt010": (0.0002, 0.0099)}


def _band_counts(only_service, only_candidate, detect):
    """Specimens per mixture-fraction band, split by whether the screen in service flags them.

    The cutoffs are nested, so the band counts follow from the per-cutoff discordance: among the
    events the screen in service flags, the number the candidate misses at each cutoff is its
    `only_service` count, and among the events it misses, the number the candidate catches is
    `only_candidate`.
    """
    flagged, missed = [], []
    for i in range(len(W.CUTOFFS)):
        hi_s = only_service[i] - (only_service[i+1] if i+1 < len(only_service) else 0)
        hi_c = only_candidate[i] - (only_candidate[i-1] if i else 0)
        flagged.append(hi_s)
        missed.append(hi_c)
    # flagged[i] is the count whose estimate sits in the band below cutoff i (and above cutoff i+1)
    out_flagged = [detect - only_service[0]] + list(reversed(flagged[:]))
    out_missed = [missed[0]] + missed[1:] + [0]
    return out_flagged, out_missed


def _estimate(rng, band):
    lo, hi = LIMITS[band]
    if band == "lt010":
        # ordinary allele-balance noise: a long right tail, no floor
        v = min(hi, max(0.0001, math.exp(rng.gauss(math.log(0.0021), 0.62))))
    elif band == "ge050":
        v = min(hi, max(lo, 0.0501 + abs(rng.gauss(0.0, 0.085))))
    else:
        v = rng.uniform(lo, hi)
    return round(v, 4)


def receipt_days(first, last, n, seed):
    """One receipt day per specimen, in order: working days only, the laboratory's own weekday
    profile, and a catch-up on the first day back after a closure."""
    drng = random.Random(seed)
    days = [first + dt.timedelta(days=i) for i in range((last - first).days + 1)]
    days = [d for d in days if d.weekday() < 5 and d not in W.HOLIDAYS]
    weights, closed = [], False
    for d in days:
        prev = d - dt.timedelta(days=1)
        while prev.weekday() > 4 or prev in W.HOLIDAYS:
            closed = closed or prev in W.HOLIDAYS
            prev -= dt.timedelta(days=1)
        w = W.DAY_WEIGHT[d.weekday()] * (1.24 if closed else 1.0) * (0.93 + 0.14 * drng.random())
        closed = False
        weights.append(w)
    total = sum(weights)
    out, carry = [], 0.0
    for d, w in zip(days, weights):
        carry += w * n / total
        while len(out) < min(n, int(round(carry))):
            out.append(d)
    while len(out) < n:
        out.append(days[-1])
    return out


def build():
    rng = random.Random(W.SEED)
    days = (W.RUN_TO - W.RUN_FROM).days + 1
    weekdays = [W.RUN_FROM + dt.timedelta(days=d) for d in range(days)
                if (W.RUN_FROM + dt.timedelta(days=d)).weekday() < 5]

    rest = (["mixed"] * W.N_MIXED + ["clean"] * W.N_CONCORDANT + ["scope"] * W.OUT_OF_SCOPE
            + ["noread"] * W.NO_ACCEPTED_READ + ["noest"] * W.NO_ESTIMATE
            + ["inconclusive"] * W.INCONCLUSIVE)
    rng.shuffle(rest)
    n = len(rest) + W.PENDING_VERDICT
    # a verdict is outstanding because the panel runs three weeks behind the laboratory, so the
    # specimens without one are the late receipts
    tail = rng.sample(range(n - 520, n), W.PENDING_VERDICT)
    pend = set(tail)
    roles, it = [], iter(rest)
    for i in range(n):
        roles.append("pending" if i in pend else next(it))

    # mixture-fraction bands, forward from the per-cutoff discordance
    flag_bands = {}
    miss_bands = {}
    for i, band in enumerate(BANDS):
        if i == 0:
            flag_bands[band] = W.INC_DETECT - W.ONLY_SERVICE[0]
            miss_bands[band] = W.ONLY_CANDIDATE[0]
        elif i < len(W.CUTOFFS):
            flag_bands[band] = W.ONLY_SERVICE[i-1] - W.ONLY_SERVICE[i]
            miss_bands[band] = W.ONLY_CANDIDATE[i] - W.ONLY_CANDIDATE[i-1]
        else:
            flag_bands[band] = W.ONLY_SERVICE[-1]
            miss_bands[band] = (W.N_MIXED - W.INC_DETECT) - W.ONLY_CANDIDATE[-1]
    clean_bands = {"ge050": W.CAND_FALSE[0]}
    for i in range(1, len(W.CUTOFFS)):
        clean_bands[BANDS[i]] = W.CAND_FALSE[i] - W.CAND_FALSE[i-1]
    clean_bands["lt010"] = W.N_CONCORDANT - W.CAND_FALSE[-1]

    mixed_plan = ([("flag", b) for b in BANDS for _ in range(flag_bands[b])]
                  + [("miss", b) for b in BANDS for _ in range(miss_bands[b])])
    clean_plan = [b for b in BANDS for _ in range(clean_bands[b])]
    rng.shuffle(mixed_plan)
    rng.shuffle(clean_plan)
    # the screen in service's false calls: mostly specimens with an ordinary estimate
    false_slots = ([i for i, b in enumerate(clean_plan) if b == "ge050"][:15]
                   + [i for i, b in enumerate(clean_plan) if b in ("b3050", "b2030", "b1520", "b1015")][:6])
    rest = [i for i, b in enumerate(clean_plan) if b == "lt010"]
    rng.shuffle(rest)
    false_slots += rest[:W.INC_FALSE - len(false_slots)]
    false_set = set(false_slots)

    specimens = []
    arrivals = receipt_days(W.RUN_FROM, W.RUN_TO, n, W.SEED + 61)
    # the accession counter is shared with every other project the laboratory books in, so the
    # cohort service's accessions step irregularly. Drawn on its own stream: no other draw moves.
    srng = random.Random(W.SEED + 907)
    hrng = random.Random(W.SEED + 923)       # het excess, DNA input and depth: measurement shapes
    rsrng = random.Random(W.SEED + 929)      # the read-set counter's own stride
    serials, serial = [], 104000
    for _ in range(n):
        serials.append(serial)
        serial += srng.choice([1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5, 6, 8, 11, 17])
    mi = ci = 0
    projects = [p[0] for p in W.PROJECTS]
    weights = [p[2] for p in W.PROJECTS]
    for i, role in enumerate(roles):
        received = arrivals[i]
        # the day the panel's turnaround is counted from, as the register recorded it
        panel_from = weekdays[int(i * len(weekdays) / n)]
        sid = "NFG27-%06d" % serials[i]
        if role == "scope":
            project, agreement = W.CONTRACT[i % len(W.CONTRACT)]
        else:
            project, agreement = rng.choices(projects, weights)[0], ""
        rec = {"specimen_id": sid, "role": role, "project": project, "agreement": agreement,
               "received": received, "panel_from": panel_from, "extraction": rng.choices(W.EXTRACTION, [0.62, 0.27, 0.11])[0],
               "instrument": None if rng.random() < 0.54 else None,
               "depth": round(rng.uniform(26.0, 71.0), 1)}      # reshaped below, draw kept in place
        if role == "mixed":
            side, band = mixed_plan[mi]
            mi += 1
            rec["verdict"] = "MIXED"
            rec["service_flag"] = side == "flag"
            rec["estimate"] = _estimate(rng, band)
        elif role == "clean":
            band = clean_plan[ci]
            rec["verdict"] = "CONCORDANT"
            rec["service_flag"] = ci in false_set
            rec["estimate"] = _estimate(rng, band)
            ci += 1
        else:
            rec["verdict"] = {"inconclusive": "INCONCLUSIVE", "pending": None}.get(role, "CONCORDANT")
            if role == "scope":
                rec["verdict"] = "CONCORDANT" if rng.random() < 0.94 else "MIXED"
            rec["service_flag"] = rng.random() < 0.028
            rec["estimate"] = _estimate(rng, "ge050" if rng.random() < 0.02 else "lt010")
        if role == "noread":
            rec["service_flag"] = None          # every read voided, so no call was ever recorded
        if role in ("scope", "noest"):
            rec["estimate"] = None if role == "noest" else None
        # the screen in service's het-excess value: the signal its threshold rule reads, against the
        # control threshold the specimen's own batch held, which the run log records. The recorded
        # call follows the rule except where the duty bioinformatician reviewed the specimen.
        thr = 36.50 if rec["received"] >= dt.date(2027, 4, 12) else 36.60
        if rec["service_flag"]:
            rng.gauss(37.70, 0.84)           # the old draw, kept so the stream does not move
            rec["het"] = round(thr + 0.01 + abs(hrng.gauss(0.0, 0.62)), 2)
        else:
            rng.gauss(34.05 + (0.9 if rec["verdict"] == "MIXED" else 0.0), 1.05)
            spread = abs(hrng.gauss(0.0, 1.15)) * (0.72 if rec["verdict"] == "MIXED" else 1.0)
            rec["het"] = round(thr - 0.01 - spread, 2)
        # DNA input is an extraction yield, so it is right-skewed, and the depth a run reaches
        # follows the input it was given
        rng.uniform(11.5, 184.0)             # the old draw, kept so the stream does not move
        conc = min(184.0, max(6.2, math.exp(hrng.gauss(math.log(62.0), 0.52))))
        rec["conc"] = round(conc, 1)
        lift = 1.0 + 0.26 * (math.log(conc) - math.log(62.0))
        if rec["role"] == "noest":           # the read set the pipeline could not estimate on
            rec["depth"] = round(max(5.4, min(19.6, 13.5 * lift + hrng.gauss(0.0, 2.6))), 1)
        else:
            rec["depth"] = round(max(24.2, 47.5 * lift + hrng.gauss(0.0, 7.4)), 1)
        specimens.append(rec)

    # which sequencer a specimen ran on. GSQ-A is the older instrument and carries a higher
    # het-excess background, so the screen in service flags more of its reads; the draw sits on its
    # own stream and moves no call, no estimate and no verdict.
    irng = random.Random(W.SEED + 911)
    for rec in specimens:
        p_a = 0.62 if rec["service_flag"] else 0.515
        rec["instrument"] = W.INSTRUMENTS[0] if irng.random() < p_a else W.INSTRUMENTS[1]

    # the duty bioinformatician's reviews. The recorded call does not move: what moves is the
    # het-excess value behind it, so the threshold rule no longer reproduces the recorded call on the
    # specimens that were reviewed, which is why KVAL-07 3.4 files the recorded flag.
    for s in specimens:
        s["call_source"] = "AUTO"
    flagged = [s for s in specimens if s["service_flag"]]
    cleared = [s for s in specimens if s["service_flag"] is False]
    rng.shuffle(flagged)
    rng.shuffle(cleared)
    # the overturned calls are taken from receipts the comparison does not hold, so no override can
    # move the screen in service's detections or its false calls
    out = lambda s: s["role"] not in ("mixed", "clean")
    over_f = [s for s in flagged if out(s)][:11]
    over_c = [s for s in cleared if out(s)][:4]
    for s in over_f:                        # reviewed and flagged on a mixture signal the rule misses
        rng.uniform(34.9, 36.3)             # the old draw, kept so the stream does not move
        thr = 36.50 if s["received"] >= dt.date(2027, 4, 12) else 36.60
        s["call_source"] = "REVIEWED"
        s["het"] = round(thr - 0.02 - abs(hrng.gauss(0.0, 0.17)), 2)
    for s in over_c:                        # reviewed and cleared, the het excess explained by ancestry
        rng.uniform(36.7, 37.4)             # the old draw, kept so the stream does not move
        thr = 36.50 if s["received"] >= dt.date(2027, 4, 12) else 36.60
        s["call_source"] = "REVIEWED"
        s["het"] = round(thr + 0.02 + abs(hrng.gauss(0.0, 0.17)), 2)
    done = {id(s) for s in over_f + over_c}
    agree = [s for s in flagged if id(s) not in done][:24] + [s for s in cleared if id(s) not in done][:138]
    for s in agree:
        s["call_source"] = "REVIEWED"       # reviewed, the recorded call agrees with the rule

    # plates and wells, in receipt order
    order = sorted(specimens, key=lambda r: (r["received"], r["specimen_id"]))
    wells = ["%s%02d" % (r, c) for r in "ABCDEFGH" for c in range(1, 13)]
    for k, s in enumerate(order):
        s["plate"] = "GKP-27%02d-%s%02d" % (s["received"].month, "ABCD"[(k // 96) % 4], (k // 96) // 4 + 1)
        s["well"] = wells[k % 96]

    # read sets: a depth top-up gives a second library, and the laboratory accepts one of them
    comparison = [s for s in specimens if s["role"] in ("mixed", "clean")]
    rng.shuffle(comparison)
    for s in specimens:
        s["read_sets"] = []
    rs_serial = [210000]
    for k, s in enumerate(sorted(specimens, key=lambda r: r["specimen_id"])):
        if s["estimate"] is None:
            continue
        rs_serial[0] += rsrng.choice([1, 1, 1, 2, 2, 2, 3, 3, 4, 5, 7, 11])
        rid = "RS27-%06d" % rs_serial[0]
        s["read_sets"].append({"read_set": rid, "accepted": True, "estimate": s["estimate"],
                               "depth": s["depth"]})
    for s in comparison[:W.TWO_READ_SETS]:
        lo, hi = _band_of(s["estimate"])
        second = round(min(hi, max(lo, s["estimate"] + (0.0007 if s["estimate"] < 0.05 else 0.0061))), 4)
        s["read_sets"].append({"read_set": s["read_sets"][0]["read_set"].replace("RS27-", "RS27-9"),
                               "accepted": False, "estimate": second,
                               "depth": round(s["depth"] * 0.41, 1)})
    # the biobank's request register: one request per specimen, a few covering a family group
    qrng = random.Random(W.SEED + 91)
    serial, last = 40231, None
    for s in sorted(specimens, key=lambda r: (r["received"], r["specimen_id"])):
        if last is not None and qrng.random() < 0.014:
            s["request_id"] = last
        else:
            serial += qrng.randint(1, 3)
            s["request_id"] = "REQ-2027-%05d" % serial
            last = s["request_id"]

    for s in specimens:
        s["replated"] = False
    for s in comparison[W.TWO_READ_SETS:W.TWO_READ_SETS + W.REPLATED]:
        s["replated"] = True
    return sorted(specimens, key=lambda r: r["specimen_id"])


def _band_of(est):
    """The band an estimate sits in, as the cutoffs cut it, so a second read set stays in it."""
    for band in BANDS:
        lo, hi = LIMITS[band]
        if lo <= est <= hi:
            return lo, hi
    return 0.0002, 0.0099


if __name__ == "__main__":
    sp = build()
    mixed = [s for s in sp if s["role"] == "mixed"]
    clean = [s for s in sp if s["role"] == "clean"]
    print("specimens", len(sp), "mixed", len(mixed), "clean", len(clean))
    print("service detects", sum(1 for s in mixed if s["service_flag"]),
          "false calls", sum(1 for s in clean if s["service_flag"]))
    for cut in W.CUTOFFS:
        det = sum(1 for s in mixed if s["estimate"] is not None and s["estimate"] >= cut)
        b = sum(1 for s in mixed if s["estimate"] is not None and s["estimate"] >= cut and not s["service_flag"])
        c = sum(1 for s in mixed if s["estimate"] is not None and s["estimate"] < cut and s["service_flag"])
        fp = sum(1 for s in clean if s["estimate"] is not None and s["estimate"] >= cut)
        print("  %.3f detect %3d only-candidate %2d only-service %2d false %3d" % (cut, det, b, c, fp))
