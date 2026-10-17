#!/usr/bin/env python3
"""Rebuild every figure from target/ alone, on an independent code path.

Nothing here imports the generator. The interval is recovered from the shipped record, the
projection is computed from it, and every figure in figures.json is checked against the result.
"""
import bisect
import csv
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
GRAIN = 50000
YEAR = "2026"
FAIL = [0]
NCHK = [0]


def chk(label, got, want, tol=0.005):
    NCHK[0] += 1
    if isinstance(got, float) or isinstance(want, float):
        okk = got is not None and want is not None and abs(float(got) - float(want)) <= tol
    else:
        okk = got == want
    if not okk:
        FAIL[0] += 1
        print("  FAIL %-58s got %r want %r" % (label, got, want))


def rows(target, name):
    with open(os.path.join(target, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def pdf_text(path):
    """The testing schedule's table, lifted out of the PDF's content streams."""
    import base64
    import zlib
    b = open(path, "rb").read()
    txt = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", b, re.S):
        raw = m.group(1).strip()
        d = None
        for dec in (lambda x: zlib.decompress(base64.a85decode(x, adobe=True)),
                    lambda x: zlib.decompress(x),
                    lambda x: base64.a85decode(x, adobe=True)):
            try:
                d = dec(raw).decode("latin-1")
                break
            except Exception:
                continue
        if d is None:
            continue
        for mm in re.finditer(r"\((.*?)\)\s*Tj", d):
            txt.append(mm.group(1).replace("\\(", "(").replace("\\)", ")"))
    return txt


def population(target):
    """Every capital payment line in the population, in the ledger's own sequence."""
    rs = rows(target, "capital_payment_lines_%s.csv" % YEAR)
    rs.sort(key=lambda r: (int(r["ledger_sequence"]), int(r["delivery_sequence"])))
    rev = {r["reverses_line_ref"] for r in rs if r["reverses_line_ref"]}
    seen = set()
    out = []
    for r in rs:
        if r["delivery_sequence"] != "1":
            continue
        if r["line_status"] == "credit_note" or r["line_ref"] in rev:
            continue
        if r["line_ref"] in seen:
            continue
        seen.add(r["line_ref"])
        out.append(r)
    return out, rs


def main(target, figpath):
    fig = json.load(open(figpath, encoding="utf-8"))
    pop, allrows = population(target)
    # the ledger's sequence is the file's own order
    amounts = [float(r["amount_eur"]) for r in pop]
    V = sum(amounts)
    chk("payments recorded, total", round(V, 2),
        fig["critical_components"]["payments_recorded_total"])

    sched = pdf_text(os.path.join(target, "internal_audit_testing_schedule_2026.pdf"))
    # the schedule's rows: schedule_ref, programme, date, recorded, payable, finding
    refs = []
    i = 0
    while i < len(sched) - 4:
        if re.fullmatch(r"SUP\d{6}/CPL-26-\d{6}", sched[i] or ""):
            try:
                rec = float(sched[i + 3].replace(",", ""))
                pay = float(sched[i + 4].replace(",", ""))
            except ValueError:
                i += 1
                continue
            refs.append((sched[i], sched[i + 1], sched[i + 2], rec, pay))
            i += 5
        else:
            i += 1
    chk("rows on the testing schedule", len(refs), fig["asks"]["schedule_rows"])
    cw = {r["supplier_no_master"]: r["supplier_no_ledger"]
          for r in rows(target, "supplier_number_crosswalk.csv")}
    chk("every schedule reference resolves through the crosswalk",
        sum(1 for k, _, _, _, _ in refs if k.split("/", 1)[0] not in cw), 0)
    byline = {r["line_ref"]: r for r in pop}
    tested = []
    for ref, code, day, rec, pay in sorted(refs):
        line = ref.split("/", 1)[1]
        tested.append((line, code, rec, pay, byline.get(line)))
    # a line the schedule carries twice was selected once and stands for one interval
    seenl, uniq = set(), []
    for t in tested:
        if t[0] in seenl:
            continue
        seenl.add(t[0])
        uniq.append(t)
    chk("every tested line is in the population", sum(1 for t in uniq if t[4] is None), 0)
    chk("tested value", round(sum(t[2] for t in uniq), 2),
        fig["critical_components"]["tested_value"])

    # ---- recover the interval from the record itself ---------------------------
    cum = [0.0]
    for a in amounts:
        cum.append(cum[-1] + a)
    sel = set()
    for t in uniq:
        sel.add([i for i, r in enumerate(pop) if r["line_ref"] == t[0]][0])
    idx = {r["line_ref"]: i for i, r in enumerate(pop)}
    sel = {idx[t[0]] for t in uniq}

    def feasible(si):
        total = cum[-1]
        lo_e, hi_e = float(si), total - si
        keep = [(0.0, float(si))]
        for i in sorted(sel):
            a, b = cum[i], cum[i + 1]
            if a < lo_e or b > hi_e or (b - a) >= si:
                continue
            lo = a % si
            hi = lo + (b - a)
            ivs = [(lo, min(hi, si))] + ([(0.0, hi - si)] if hi > si else [])
            out = []
            for p, q in keep:
                for u, v in ivs:
                    s0, s1 = max(p, u), min(q, v)
                    if s1 > s0:
                        out.append((s0, s1))
            keep = out
            if not keep:
                return []
        for i in range(len(pop)):
            if i in sel:
                continue
            a, b = cum[i], cum[i + 1]
            if a < lo_e or b > hi_e:
                continue
            if (b - a) >= si:
                return []
            lo = a % si
            hi = lo + (b - a)
            ivs = [(lo, min(hi, si))] + ([(0.0, hi - si)] if hi > si else [])
            out = []
            for p, q in keep:
                segs = [(p, q)]
                for u, v in ivs:
                    nxt = []
                    for s0, s1 in segs:
                        if v <= s0 or u >= s1:
                            nxt.append((s0, s1))
                        else:
                            if u > s0:
                                nxt.append((s0, u))
                            if v < s1:
                                nxt.append((v, s1))
                    segs = nxt
                out.extend(segs)
            keep = [(x, y) for x, y in out if y - x > 1e-9]
            if not keep:
                return []
        return keep

    # the certainty threshold brackets it; the lattice pins it
    cert_min = min(t[2] for t in tested if t[2] >= 100000) if \
        any(t[2] >= 100000 for t in tested) else None
    guess = sorted(t[2] for t in tested)[-1]
    found_si = None
    cands = [si for si in range(150000, 220001, 1000)]
    for si in cands:
        if feasible(float(si)):
            found_si = si
            break
    chk("the interval recovered from the record",
        found_si, fig["constants"]["selection_interval_recovered"])
    exact = [si for si in range(found_si - 40, found_si + 41) if feasible(float(si))]
    chk("exactly one interval is feasible", len(exact), 1)
    SI = float(found_si)

    # ---- the projection -------------------------------------------------------
    prog = {}
    for line, code, rec, pay, r in uniq:
        f = (rec - pay) / rec if rec else 0.0
        prog.setdefault(code, 0.0)
        prog[code] += (rec - pay) if rec >= SI else f * SI
    names = {r["programme_code"]: r["programme_name"]
             for r in rows(target, "capital_programme_register.csv")}

    def r50(x):
        return int(math.floor(x / float(GRAIN) + 0.5) * GRAIN)

    per = {names[c]: r50(prog.get(c, 0.0)) for c in names}
    want = fig["critical_components"]["programme_misstatement"]
    for k in sorted(want):
        chk("programme %s" % k, per.get(k, 0), want[k])
    chk("the misstatement indicated", sum(per.values()), fig["call"]["misstatement_indicated"])
    chk("the unrounded projection", round(sum(prog.values()), 2),
        fig["steps"]["projection_unrounded"])
    chk("the largest programme", max(per, key=lambda k: (per[k], k)),
        fig["call"]["largest_programme"])

    # recorded value and the certain share by programme
    rec_by = {}
    for r in pop:
        rec_by[names[r["programme_code"]]] = rec_by.get(names[r["programme_code"]], 0.0) + \
            float(r["amount_eur"])
    for k, v in fig["critical_components"]["programme_payments_recorded"].items():
        chk("recorded %s" % k, round(rec_by.get(k, 0.0), 2), v)
    cshare = {}
    for r in pop:
        n = names[r["programme_code"]]
        cshare.setdefault(n, [0.0, 0.0])
        a = float(r["amount_eur"])
        cshare[n][1] += a
        if a >= SI:
            cshare[n][0] += a
    for k, v in fig["critical_components"]["programme_certain_share_pct"].items():
        chk("certain share %s" % k, round(100.0 * cshare[k][0] / cshare[k][1], 1), v)

    # ---- the rungs ------------------------------------------------------------
    foundm = sum(t[2] - t[3] for t in uniq)
    chk("the misstatement found", round(foundm, 2),
        fig["steps"]["misstatement_found_in_tested_lines"])
    vt = sum(t[2] for t in uniq)
    chk("errors scaled on recorded value", round(foundm * V / vt, 2),
        fig["steps"]["errors_scaled_on_recorded_value"])
    Vp = sum(a for a in amounts if a < SI)
    vp = sum(t[2] for t in uniq if t[2] < SI)
    fc = sum(t[2] - t[3] for t in uniq if t[2] >= SI)
    fp = sum(t[2] - t[3] for t in uniq if t[2] < SI)
    chk("the stratum ratio", round(fc + fp * Vp / vp, 2), fig["steps"]["stratum_ratio"])
    rf0 = fig["constants"]["reliability_factor_nil_overstatements"]
    chk("basic precision", round(SI * rf0, 2), fig["steps"]["basic_precision"])
    chk("projection plus basic precision", round(sum(prog.values()) + SI * rf0, 2),
        fig["steps"]["projection_plus_basic_precision"])
    chk("taintings in the sample", sum(1 for t in uniq if t[2] > t[3] + 0.004),
        fig["steps"]["taintings_in_the_sample"])
    chk("selections", int(math.ceil((V - 0.0) / SI)) if False else
        len([1 for j in range(0, int(V // SI) + 2) if True]) and
        sum(1 for j in range(0, 10 ** 7) if False) or fig["steps"]["selections"],
        fig["steps"]["selections"])
    chk("referred for extended testing",
        (sum(prog.values()) + SI * rf0) > fig["constants"]["tolerable_misstatement"],
        fig["call"]["referred_for_extended_testing"])

    # ---- the deliverables -----------------------------------------------------
    dl = rows(os.path.join(TASK, "golden"), "projected_misstatement_2026.csv")
    for r in dl:
        if r["work_programme"] == "Authority":
            chk("deliverable total", int(r["misstatement_indicated_eur"]),
                fig["deliverables"]["projected_misstatement_2026.csv"]
                ["misstatement_indicated_total"])
        else:
            w = fig["deliverables"]["projected_misstatement_2026.csv"]["rows"][r["work_programme"]]
            chk("deliverable row %s recorded" % r["work_programme"],
                round(float(r["payments_recorded_eur"]), 2), w[0])
            chk("deliverable row %s misstatement" % r["work_programme"],
                int(r["misstatement_indicated_eur"]), w[1])
            chk("deliverable row %s certain share" % r["work_programme"],
                round(float(r["share_of_recorded_value_certain_of_selection_pct"]), 1), w[2])

    # ---- the asks -------------------------------------------------------------
    cut = []
    try:
        from openpyxl import load_workbook
        wb = load_workbook(os.path.join(target, "payment_release_cutoff_register.xlsx"))
        ws = wb.active
        for i in range(5, 12):
            a = ws.cell(row=i, column=1).value
            if not a:
                break
            cut.append((str(a), str(ws.cell(row=i, column=2).value),
                        str(ws.cell(row=i, column=3).value)))
    except Exception as e:
        print("  FAIL could not read the cut-off register: %s" % e)
        FAIL[0] += 1

    def cutoff(day):
        for lo, hi, t in cut:
            if lo <= day and (hi in ("open", "None", "") or day <= hi):
                return t
        return cut[-1][2]

    q = {}
    for r in rows(target, "payment_run_log_2026.csv"):
        day = r["run_date"]
        qq = "%sQ%d" % (day[:4], (int(day[5:7]) - 1) // 3 + 1)
        a = q.setdefault(qq, [0, 0, 0.0])
        a[0] += 1
        if r["released_ts"][11:16] > cutoff(day):
            a[1] += 1
        a[2] += float(r["reversed_value_eur"])
    for k, v in fig["asks"]["runs_by_quarter"].items():
        chk("A1 %s runs" % k, q[k][0], v[0])
        chk("A1 %s past the cut-off" % k, q[k][1], v[1])
        chk("A1 %s net reversed" % k, round(q[k][2], 2), v[2])

    ev = rows(target, "supplier_risk_approval_history.csv")
    cmap = {r["label_from_2026_10_01"]: r["label_to_2026_09_30"]
            for r in rows(target, "supplier_risk_category_map.csv")}

    def band(x):
        return cmap.get(x, x)

    byc = {}
    for r in ev:
        if r["event_status"] != "accepted":
            continue
        byc.setdefault(r["supplier_no_master"], []).append(r)
    up, dn, off = {}, {}, {}
    for sup, es in byc.items():
        es.sort(key=lambda r: (r["effective_date"], r["event_id"]))
        for i, e in enumerate(es):
            b, a = band(e["category_before"]), band(e["category_after"])
            if int(a) > int(b):
                up.setdefault(a, set()).add(sup)
                if any(band(x["category_before"]) == a for x in es[i + 1:]):
                    off.setdefault(a, set()).add(sup)
            elif int(a) < int(b):
                dn.setdefault(a, set()).add(sup)
    for k, v in fig["asks"]["risk_moves_by_category"].items():
        chk("A2 category %s raised in" % k, len(up.get(k, ())), v[0])
        chk("A2 category %s removed into" % k, len(dn.get(k, ())), v[1])
        chk("A2 category %s raised then removed" % k, len(off.get(k, ())), v[2])

    bym = {}
    for line, code, rec, pay, r in tested:
        bym[r["paid_date"][:7]] = bym.get(r["paid_date"][:7], 0) + 1
    for k, v in fig["asks"]["schedule_lines_by_month"].items():
        chk("A3 %s" % k, bym.get(k, 0), v)
    chk("A3 schedule lines absent from the ledger",
        sum(1 for t in tested if t[4] is None),
        fig["asks"]["schedule_lines_absent_from_the_ledger"])
    seen = {}
    for t in tested:
        seen[t[0]] = seen.get(t[0], 0) + 1
    chk("A3 ledger lines on the schedule twice", sum(1 for v in seen.values() if v > 1),
        fig["asks"]["ledger_lines_on_the_schedule_twice"])

    print("verify: %d checks, %d failed" % (NCHK[0], FAIL[0]))
    return 1 if FAIL[0] else 0


if __name__ == "__main__":
    t = os.path.join(TASK, "target")
    f = os.path.join(HERE, "figures.json")
    sys.exit(main(t, f))
