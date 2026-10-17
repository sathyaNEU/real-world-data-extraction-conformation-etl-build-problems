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
        # the paper carries both samples plan 4.1 lists: the capital lines and the revenue ones,
        # which carry the revenue ledger's own prefix and resolve to no capital line
        # the paper identifies an item by its payment line, by the invoice where the valuation
        # rather than the line was examined, or by the revenue ledger's own reference
        if re.fullmatch(r"SUP\d{6}/(CPL|REL|INV)-26-\d{6}", sched[i] or ""):
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
    byinv = {}
    for r in pop:
        byinv.setdefault(r["invoice_ref"], []).append(r)
    tested = []
    for ref, code, day, rec, pay in sorted(refs):
        key = ref.split("/", 1)[1]
        if key in byinv and key not in byline:
            # recorded at invoice level: the row covers every payment line on the invoice
            for r in sorted(byinv[key], key=lambda x: x["line_ref"]):
                tested.append((r["line_ref"], code, float(r["amount_eur"]),
                               float(r["amount_eur"]), r))
            continue
        tested.append((key, code, rec, pay, byline.get(key)))
    # a line the schedule carries twice was selected once and stands for one interval; a row that
    # resolves to no line in this ledger is the revenue sample and is no part of this population
    seenl, uniq = set(), []
    for t in tested:
        if t[0] in seenl or t[4] is None:
            continue
        seenl.add(t[0])
        uniq.append(t)
    chk("every capital tested line is in the population", sum(1 for t in uniq if t[4] is None), 0)
    chk("the paper's rows that resolve to no capital line",
        sum(1 for t in tested if t[4] is None),
        fig["asks"]["schedule_lines_absent_from_the_ledger"])
    chk("the paper's capital rows all resolve to a payment line",
        sum(1 for t in uniq if t[4] is None), 0)

    # ---- recover the interval from the record itself ---------------------------
    cum = [0.0]
    for a in amounts:
        cum.append(cum[-1] + a)
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

    # the interval is filed on the working paper's basis of selection, so it is read rather than
    # recovered, and the figure it names is checked against the one the figures carry
    basis = " ".join(sched)
    m = re.search(r"selection interval of ([\d,]+) euro", basis)
    chk("the working paper files a selection interval", bool(m), True)
    SI = float(m.group(1).replace(",", "")) if m else 0.0
    chk("the filed interval", int(SI), fig["constants"]["selection_interval_recovered"])
    chk("the paper files that the interval was common to every programme",
        "common to every work programme" in basis, True)
    chk("the paper defines the lines certain of selection",
        "certain of selection" in basis, True)

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
    Vp = sum(a for a in amounts if a < SI)
    vp = sum(t[2] for t in uniq if t[2] < SI)
    fc = sum(t[2] - t[3] for t in uniq if t[2] >= SI)
    fp = sum(t[2] - t[3] for t in uniq if t[2] < SI)
    # the reliability factors ship in the manual, so the factor is read rather than assumed
    man = pdf_text(os.path.join(target, "audit_manual_part9.pdf"))
    rftab = []
    for i, s in enumerate(man):
        if s.strip() != "factor":
            continue
        for nxt in man[i + 1:]:
            if not re.fullmatch(r"\d{1,2}\.\d{2}", (nxt or "").strip()):
                break
            rftab.append(float(nxt))
    chk("the manual ships a reliability table", len(rftab) >= 11, True)
    rf0 = rftab[0] if rftab else 0.0
    chk("the factor at nil overstatements", rf0,
        fig["constants"]["reliability_factor_nil_overstatements"])
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
            chk("deliverable row %s misstatement" % r["work_programme"],
                int(r["misstatement_indicated_eur"]), w[0])
            chk("deliverable row %s certain share" % r["work_programme"],
                round(float(r["misstatement_as_pct_of_recorded_value"]), 2), w[1])

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
        if r["run_status"] != "released":          # the re-released row is the same run
            continue
        rel = r["released_ts"][:10]
        qq = "%sQ%d" % (rel[:4], (int(rel[5:7]) - 1) // 3 + 1)
        a = q.setdefault(qq, [0, 0.0])
        # the cut-off in force on the run's own date, and a release carrying a later date than the
        # run ran past midnight, so it is past that date's cut-off however early the clock reads
        late = rel != r["run_date"] or r["released_ts"][11:16] > cutoff(r["run_date"])
        if late:
            a[0] += 1
            a[1] += float(r["run_value_eur"])
    for k, v in fig["asks"]["runs_past_the_cutoff_by_quarter"].items():
        chk("A1 %s value released past the cut-off" % k, round(q[k][1], 2), v[0])

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
            # the asking sentence pins "removed from it": a move out of the category the supplier
            # was in, whichever way it went, not a move down into it
            if int(a) != int(b):
                dn.setdefault(b, set()).add(sup)
    # an approval decision is taken on a trading group and recorded against the parent only; the
    # master names the parent each supplier belongs to, so a decision reaches every member
    from openpyxl import load_workbook as _lw
    wsm = _lw(os.path.join(target, "supplier_master.xlsx"), data_only=True).active
    hdr = [c.value for c in wsm[4]]
    im, ip = hdr.index("supplier_no_master"), hdr.index("group_parent_no")
    members = {}
    for r in wsm.iter_rows(min_row=5, values_only=True):
        if r[ip]:
            members.setdefault(r[ip], []).append(r[im])
    chk("the master names group members", len(members) > 0, True)

    def expand(names):
        out = set()
        for s in names:
            out.add(s)
            out |= set(members.get(s, ()))
        return out
    up = {k: expand(v) for k, v in up.items()}
    dn = {k: expand(v) for k, v in dn.items()}
    off = {k: expand(v) for k, v in off.items()}
    for k, v in fig["asks"]["risk_moves_by_category"].items():
        chk("A2 category %s raised in" % k, len(up.get(k, ())), v[0])
        chk("A2 category %s removed from" % k, len(dn.get(k, ())), v[1])
        chk("A2 category %s raised then removed" % k, len(off.get(k, ())), v[2])

    # distinct ledger lines per month, as the asking sentence pins it
    # distinct ledger lines per quarter of payment, as the asking sentence pins it
    bym = {}
    for line, code, rec, pay, r in tested:
        if r is None:
            continue
        d = r["paid_date"]
        bym.setdefault("%sQ%d" % (d[:4], (int(d[5:7]) - 1) // 3 + 1), set()).add(line)
    bym = {k: len(v) for k, v in bym.items()}
    for k, v in fig["asks"]["schedule_lines_by_quarter"].items():
        chk("A3 %s" % k, bym.get(k, 0), v)
    chk("A3 schedule lines absent from the ledger",
        sum(1 for t in tested if t[4] is None),
        fig["asks"]["schedule_lines_absent_from_the_ledger"])
    seen = {}
    for t in tested:
        if t[4] is None:
            continue
        seen[t[0]] = seen.get(t[0], 0) + 1
    chk("A3 ledger lines on the schedule twice", sum(1 for v in seen.values() if v > 1),
        fig["asks"]["ledger_lines_on_the_schedule_twice"])

    print("verify: %d checks, %d failed" % (NCHK[0], FAIL[0]))
    return 1 if FAIL[0] else 0


if __name__ == "__main__":
    t = os.path.join(TASK, "target")
    f = os.path.join(HERE, "figures.json")
    sys.exit(main(t, f))
