"""The ask sheet's stops, run on the cut pack. The cracker lands the call (it measures each hospital against the same
days' determinations in any order), runs the hygiene battery (exact duplicates dropped, one key per row, every
application and account joined) and executes every filed rule (the guide's codes, the criteria's population, the
extract's cut); it sums the adjustments as the extract gives them and reads the reason codes by the guide's list. The
mirror stops on the call's easy route (each counsellor-day held) and reads the asks the same way. Every other stop is a
complete pipeline at a value of its own; the golden is analysis.ask_a and analysis.ask_b."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A     # noqa: E402
import common as K       # noqa: E402
import models as M       # noqa: E402
import pack as PK        # noqa: E402


def ask_a(target, rows_, mode="golden"):
    """mode: golden (each approval's write-off once, reversals each), every_line (every FAWO line summed, the extract
    as given), no_dedupe (every line, the twice-loaded December lines too), with_presumptive (every line, the
    presumptive screening's approvals too), gross (each approval once, reversals ignored), amount_dedupe (one line per
    application, code and amount, reversals of equal amount on one approval merged)."""
    if mode == "golden":
        return A.ask_a(target, rows_)
    if mode in ("golden_dups", "golden_presumptive"):
        # the golden's handling with one hazard mishandled: the twice-loaded lines kept, or the screening kept
        approved = A.counsellor_approvals(rows_)
        if mode == "golden_presumptive":
            approved |= {(r["code"], r["app"]) for r in rows_ if r["outcome"] == "approve" and r["user"] in PK.SYSTEM}
        wo, rev = {}, {}
        for line in PK.ledger(target, dedupe=(mode != "golden_dups")):
            key = (line["hospital_code"], line["application_id"])
            if key not in approved:
                continue
            if line["adjustment_code"] == "FAWO":
                wo.setdefault(key, float(line["amount"]))
            else:
                rev[key] = rev.get(key, 0.0) + float(line["amount"])
        out = {c: 0.0 for c in K.CODES}
        for (c, _), v in wo.items():
            out[c] += v
        for (c, _), v in rev.items():
            out[c] -= v
        return {c: round(v, 2) for c, v in out.items()}
    approved = A.counsellor_approvals(rows_)
    if mode == "with_presumptive":
        approved |= {(r["code"], r["app"]) for r in rows_ if r["outcome"] == "approve" and r["user"] in PK.SYSTEM}
    L = PK.ledger(target, dedupe=(mode != "no_dedupe"))
    out = {c: 0.0 for c in K.CODES}
    seen = set()
    for line in L:
        key = (line["hospital_code"], line["application_id"])
        if key not in approved:
            continue
        v = float(line["amount"])
        if mode == "gross":
            if line["adjustment_code"] == "FAWO" and key not in seen:
                seen.add(key)
                out[key[0]] += v
            continue
        if mode == "amount_dedupe":
            k2 = key + (line["adjustment_code"], line["amount"])
            if k2 in seen:
                continue
            seen.add(k2)
        out[key[0]] += v if line["adjustment_code"] == "FAWO" else -v
    return {c: round(v, 2) for c, v in out.items()}


def ask_b(target, rows_, mode="golden"):
    """mode: golden (version 1 to 30 June, version 2 from 1 July), guide_list (the guide's list for the whole year),
    first_list (version 1 for the whole year), reopened (denials a later reconsideration reopened), initial_only."""
    if mode == "golden":
        return A.ask_b(target, rows_)
    reopened = {(r["code"], r["app"]) for r in rows_ if r["type"] == "RECON"}
    out = {c: 0 for c in K.CODES}
    for r in rows_:
        if r["outcome"] != "deny" or r["user"] in PK.SYSTEM or r["when"].year != K.YEAR:
            continue
        if mode == "guide_list":
            hit = r["reason"] == 1
        elif mode == "first_list":
            hit = r["reason"] == 2
        elif mode == "reopened":
            hit = r["type"] == "INITIAL" and (r["code"], r["app"]) in reopened
        elif mode == "initial_only":
            hit = r["type"] == "INITIAL" and r["reason"] == A.documents_code(r["when"].date())
        else:
            raise ValueError(mode)
        out[r["code"]] += hit
    return out


def call_stops(target, rows_):
    days = PK.counsellor_days(target, rows_)
    out = {}
    for name, f in [("golden", M.excess), ("day_fe", M.day_fe), ("per_day", M.per_day), ("pooled", M.pooled),
                    ("counsellor_fe", M.counsellor_fe), ("day_rate", M.day_rate)]:
        out[name] = sorted(c for c in K.CODES if f(M._arr(days[c])) >= K.THRESHOLD)
    return out


def stops(target):
    rows_ = PK.conformed(target)
    th = lambda d: {c: round(v / 1000.0, 1) for c, v in d.items()}
    out = {"golden": (th(ask_a(target, rows_)), ask_b(target, rows_))}
    out["cracker"] = (th(ask_a(target, rows_, "every_line")), ask_b(target, rows_, "guide_list"))
    out["mirror"] = out["cracker"]
    for m in ("no_dedupe", "with_presumptive", "gross", "amount_dedupe", "golden_dups", "golden_presumptive"):
        out["a_" + m] = (th(ask_a(target, rows_, m)), out["golden"][1])
    for m in ("first_list", "reopened", "initial_only"):
        out["b_" + m] = (out["golden"][0], ask_b(target, rows_, m))
    return out, call_stops(target, rows_)


def pair_ceiling(st, gold, r_miss=5.0, instr=7.0, call=38.0, ask_weight=55.0):
    """The cracker lands the call; the mirror does not. Each ask figure carries an equal share of the ask weight and is
    kept only when it equals the golden at the asked rounding."""
    n = 2 * len(K.CODES)
    per = ask_weight / n

    def kept(pair):
        return sum(pair[0][c] == gold[0][c] for c in K.CODES) + sum(pair[1][c] == gold[1][c] for c in K.CODES)
    c = call + instr + per * kept(st["cracker"])
    m = r_miss + instr + per * kept(st["mirror"])
    return dict(cracker=round(c, 1), mirror=round(m, 1), pair=round((c + m) / 2, 1), cracker_kept=kept(st["cracker"]),
                mirror_kept=kept(st["mirror"]), mirror_leak=round(100 * per * kept(st["mirror"]) / ask_weight, 1))


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    st, cs = stops(target)
    g = st["golden"]
    for k, (a, b) in st.items():
        ma = sum(a[c] != g[0][c] for c in K.CODES)
        mb = sum(b[c] != g[1][c] for c in K.CODES)
        da = [round(a[c] - g[0][c], 1) for c in K.CODES]
        db = [b[c] - g[1][c] for c in K.CODES]
        print("%-20s A misses %2d of 31 (deltas %s to %s)   B misses %2d of 31 (deltas %s to %s)" % (
            k, ma, min(da), max(da), mb, min(db), max(db)))
    for k, v in cs.items():
        print("call %-14s %2d %s" % (k, len(v), v))
    print(pair_ceiling(st, g))
