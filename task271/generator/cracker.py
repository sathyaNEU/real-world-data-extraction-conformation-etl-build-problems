"""The ask sheet's stops, run on the cut pack. The cracker lands the call, runs the hygiene battery (one row per
person, the superseded reports set aside, every join checked) and executes every filed clause of section 3; it reads
the surgical record for the removal of both breasts and keys each MRI study on the enterprise ID it carries. The mirror
stops on the call's easy route and reads the asks the same way. Every other stop is a complete pipeline at a value
of its own; the golden is analysis.asks."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A     # noqa: E402
import common as K       # noqa: E402
import pack as PK        # noqa: E402


def removed(eid, ab, pr, mode):
    """mode: golden (registry and surgical record together), surgical (the surgical record alone), registry_both
    (the registry's with-contralateral codes and the surgical record, unilateral registry codes not combined), any
    (any mastectomy at all)."""
    if mode == "golden":
        return A.both_removed(eid, ab, pr, True)
    if mode == "surgical":
        return A.both_removed(eid, ab, pr, False)
    if mode == "registry_both":
        if any(int(a["surgery_primary_site_code"]) in (42, 56) for a in ab.get(eid, [])):
            return True
        return A.both_removed(eid, ab, pr, False)
    if mode == "any":
        return any(int(a["surgery_primary_site_code"]) in (41, 42, 51, 56) for a in ab.get(eid, [])) or \
            any(q["cpt_code"] in ("19303", "19305", "19306", "19307") for q in pr.get(eid, []))
    raise ValueError(mode)


def ask_a(target, mode="golden", deaths=True):
    women = A.known_women(target)
    dead = {r["enterprise_id"] for r in PK.rows(target, "deaths")} if deaths else set()
    ab = A.by_eid(PK.rows(target, "abstracts"))
    pr = A.by_eid(PK.rows(target, "surgery"))
    out = {}
    for pid, r in women.items():
        eid = r["enterprise_id"]
        if not eid or eid in dead or r["vital_status"] != "Living":
            continue
        if not 30 <= A.age_on(PK.day(r["birth_date"]), K.PROGRAM_START) <= 74:
            continue
        if removed(eid, ab, pr, mode):
            continue
        out[pid] = r
    return out


def ask_b(target, eligible, key="merges", screening_only=True, completed_only=True):
    """key: merges (follow the merge log), mrn (the study's hospital record number through the EMPI identifiers),
    eid (the enterprise ID on the order as it stands)."""
    merged = {m["retired_enterprise_id"]: m["surviving_enterprise_id"] for m in PK.rows(target, "merges")}
    mrn = {(r["hospital"], r["mrn"]): r["enterprise_id"] for r in PK.rows(target, "empi")}
    lo, hi = K.MRI_WINDOW
    had = set()
    for x in PK.rows(target, "imaging"):
        if completed_only and x["status"] != "COMPLETED":
            continue
        if screening_only and x["indication"] != "SCREENING - HIGH RISK":
            continue
        if not lo <= PK.day(x["exam_date"]) <= hi:
            continue
        if key == "merges":
            had.add(merged.get(x["enterprise_id"], x["enterprise_id"]))
        elif key == "mrn":
            had.add(mrn[(x["hospital"], x["mrn"])])
        else:
            had.add(x["enterprise_id"])
    return {pid: r for pid, r in eligible.items() if r["enterprise_id"] not in had}


def stops(target):
    gold_a = A.ask_a(target)
    gold_b = A.ask_b(target, gold_a)
    out = {"golden": (A.count(gold_a), A.count(gold_b))}
    sur = ask_a(target, "surgical")
    out["cracker"] = (A.count(sur), A.count(ask_b(target, sur, key="eid")))
    out["mirror"] = (A.count(ask_a(target, "surgical", deaths=False)),
                     A.count(ask_b(target, ask_a(target, "surgical", deaths=False), key="eid")))
    rb = ask_a(target, "registry_both")
    out["registry_with_codes_only"] = (A.count(rb), A.count(ask_b(target, rb, key="eid")))
    anym = ask_a(target, "any")
    out["any_mastectomy"] = (A.count(anym), A.count(ask_b(target, anym, key="eid")))
    out["golden_a_eid_join"] = (A.count(gold_a), A.count(ask_b(target, gold_a, key="eid")))
    out["golden_a_any_mri"] = (A.count(gold_a), A.count(ask_b(target, gold_a, screening_only=False)))
    out["golden_a_mrn_join"] = (A.count(gold_a), A.count(ask_b(target, gold_a, key="mrn")))
    return out


def pair_ceiling(st, gold, r_miss=5.0, instr=7.0, call=38.0, ask_weight=55.0):
    """The cracker lands the call; the mirror does not. Each ask figure carries an equal share of the ask weight and
    is kept only when it equals the golden."""
    n = 2 * len(K.CODES)
    per = ask_weight / n

    def kept(pair):
        return sum(pair[0][c] == gold[0][c] for c in K.CODES) + sum(pair[1][c] == gold[1][c] for c in K.CODES)
    c = call + instr + per * kept(st["cracker"])
    m = r_miss + instr + per * kept(st["mirror"])
    return dict(cracker=round(c, 1), mirror=round(m, 1), pair=round((c + m) / 2, 1),
                cracker_kept=kept(st["cracker"]), mirror_kept=kept(st["mirror"]),
                mirror_leak=round(100 * per * kept(st["mirror"]) / ask_weight, 1))


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    st = stops(target)
    g = st["golden"]
    for k, (a, b) in st.items():
        ma = sum(a[c] != g[0][c] for c in K.CODES)
        mb = sum(b[c] != g[1][c] for c in K.CODES)
        print("%-26s A misses %2d of 10, B misses %2d of 10   A %s   B %s" % (k, ma, mb, [a[c] for c in K.CODES],
                                                                            [b[c] for c in K.CODES]))
    print(pair_ceiling(st, g))
