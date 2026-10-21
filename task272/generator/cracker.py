"""The ask sheet's stops, run on the cut pack. The cracker lands the call (each household's twelve-month income through
its region's calendar for its kind of work), runs the hygiene battery (exact duplicates dropped, one write-off per
application where an application's lines repeat one amount, every application and account joined) and executes every
filed rule (the guide's codes, the criteria's population, the extract's cut); it joins each adjustment to the approval
whose number it carries and reads the reason codes by the guide's list. The mirror stops on the call's easy route (the
2025 policy's yearly figure) and reads the asks the same way. Every other stop is a complete pipeline at a value of its
own; the golden is analysis.ask_a and analysis.ask_b."""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A     # noqa: E402
import common as K       # noqa: E402
import models as M       # noqa: E402
import pack as PK        # noqa: E402


def _approved_2025(rows_, presumptive=False):
    out = {k for k, v in A.counsellor_approvals(rows_).items() if v["when"].year == K.YEAR}
    if presumptive:
        out |= {(r["code"], r["app"]) for r in rows_
                if r["outcome"] == "approve" and r["user"] in PK.SYSTEM and r["when"].year == K.YEAR}
    return out


def ask_a(target, rows_, mode="golden"):
    """mode: golden; per_app_once (each application's write-off once, joined by the number it posted under);
    event_by_app (one amount per number and posting date, joined by that number); every_line (every line as the
    extract gives it, joined by number); posted_year (every write-off posted in 2025 under an approval's number,
    whenever approved); golden_dups, golden_presumptive, golden_gross (the golden's attribution with one hazard
    mishandled: the twice-loaded lines kept, the presumptive screening kept, reversals ignored)."""
    if mode == "golden":
        return A.ask_a(target, rows_)
    if mode.startswith("golden_"):
        lines = PK.ledger(target, dedupe=(mode != "golden_dups"))
        approved = _approved_2025(rows_, presumptive=(mode == "golden_presumptive"))
        ev, rv = A.attribute(target, rows_, lines)
        out = {c: 0.0 for c in K.CODES}
        for e in ev.values():
            if e["approval"] in approved:
                out[e["approval"][0]] += e["amount"]
        if mode != "golden_gross":
            for v in rv:
                if v["approval"] in approved:
                    out[v["approval"][0]] -= v["amount"]
        return {c: round(v, 2) for c, v in out.items()}
    L = PK.ledger(target)
    out = collections.Counter({c: 0.0 for c in K.CODES})
    if mode == "posted_year":
        allappr = set(A.counsellor_approvals(rows_))
        ev, rev = {}, collections.Counter()
        for line in L:
            key = (line["hospital_code"], line["application_id"])
            if line["posted_date"][:4] != str(K.YEAR) or key not in allappr:
                continue
            if line["adjustment_code"] == "FAWO":
                ev.setdefault(key + (line["posted_date"],), float(line["amount"]))
            else:
                rev[key[0]] += float(line["amount"])
        for k, v in ev.items():
            out[k[0]] += v
        for c, v in rev.items():
            out[c] -= v
        return {c: round(out[c], 2) for c in K.CODES}
    approved = _approved_2025(rows_)
    seen = set()
    for line in L:
        key = (line["hospital_code"], line["application_id"])
        if key not in approved:
            continue
        v = float(line["amount"])
        if line["adjustment_code"] == "FAWR":
            out[key[0]] -= v
            continue
        if mode == "per_app_once":
            if key in seen:
                continue
            seen.add(key)
        elif mode == "event_by_app":
            k2 = key + (line["posted_date"],)
            if k2 in seen:
                continue
            seen.add(k2)
        out[key[0]] += v
    return {c: round(out[c], 2) for c in K.CODES}


def ask_b(target, rows_, mode="golden"):
    """mode: golden (version 1 to 30 June, version 2 from 1 July), guide_list (the guide's list for the whole year),
    first_list (version 1 for the whole year), initial_only (first-review denials only), both_years (2024 too)."""
    if mode == "golden":
        return A.ask_b(target, rows_)
    out = {c: 0 for c in K.CODES}
    for r in rows_:
        if r["outcome"] != "deny" or r["user"] in PK.SYSTEM:
            continue
        if mode != "both_years" and r["when"].year != K.YEAR:
            continue
        if mode == "guide_list":
            hit = r["reason"] == 1
        elif mode == "first_list":
            hit = r["reason"] == 2
        elif mode == "initial_only":
            hit = r["type"] == "INITIAL" and r["reason"] == A.documents_code(r["when"].date())
        elif mode == "both_years":
            hit = r["reason"] == A.documents_code(r["when"].date())
        else:
            raise ValueError(mode)
        out[r["code"]] += hit
    return out


def call_stops(target, rows_):
    fr = PK.first_reviews(target, rows_)
    out = {"golden": sorted(c for c, v in M.golden(fr).items() if v >= K.THRESHOLD)}
    for k, v in M.reflexes(fr).items():
        out[k] = sorted(c for c in K.CODES if v.get(c, 0) >= K.THRESHOLD)
    return out


def stops(target):
    rows_ = PK.conformed(target)
    th = lambda d: {c: round(v / 1000.0, 1) for c, v in d.items()}
    out = {"golden": (th(ask_a(target, rows_)), ask_b(target, rows_))}
    out["cracker"] = (th(ask_a(target, rows_, "per_app_once")), ask_b(target, rows_, "guide_list"))
    out["mirror"] = out["cracker"]
    for m in ("every_line", "event_by_app", "posted_year", "golden_dups", "golden_presumptive", "golden_gross"):
        out["a_" + m] = (th(ask_a(target, rows_, m)), out["golden"][1])
    for m in ("first_list", "initial_only", "both_years"):
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
        print("%-22s A misses %2d of 31 (deltas %s to %s)   B misses %2d of 31 (deltas %s to %s)" % (
            k, ma, min(da), max(da), mb, min(db), max(db)))
    for k, v in cs.items():
        print("call %-26s %2d %s" % (k, len(v), v))
    print(pair_ceiling(st, g))
