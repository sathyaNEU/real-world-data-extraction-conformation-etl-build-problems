"""The independent verifier: reads only the shipped bundle (target/, golden/, figures.json) with the standard library,
openpyxl, pypdf and python-docx, on its own code path, and recomputes every graded figure.

    python3 task269/generator/verify.py"""
import csv
import datetime as dt
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def day(s):
    return dt.date.fromisoformat(s) if s else None


def wmedian(pairs):
    pairs = sorted(pairs)
    tot = sum(w for _, w in pairs)
    acc = 0.0
    for x, w in pairs:
        acc += w
        if acc / tot >= 0.5 - 1e-15:
            return x
    return pairs[-1][0]


def run(task):
    t = os.path.join(task, "target")
    F = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []

    def check(label, got, want):
        if got != want:
            bad.append((label, got, want))

    # ---- the files read back -------------------------------------------------------------------------------------
    from openpyxl import load_workbook
    from pypdf import PdfReader
    wb = load_workbook(os.path.join(t, "assessor_roll_2025_certified.xlsx"), read_only=True)
    ws = wb[wb.sheetnames[0]]
    r25 = {}
    for i, r in enumerate(ws.iter_rows(values_only=True)):
        if i < 4 or r[0] is None:
            continue
        r25[str(r[0])] = dict(cls=r[1], nb=r[2], total=int(r[8]))
    check("2025 roll rows read back", len(r25) > 25000, True)
    rule = " ".join(p.extract_text() for p in PdfReader(os.path.join(t, "str_rule_18-7_residential_ratio_studies.pdf")).pages)
    rule = " ".join(rule.split())
    check("rule control sentence", "Residential ratio studies" in rule, True)
    check("rule level sentence", "over every parcel of the class on the county's certified roll" in rule, True)
    memo = " ".join(p.extract_text() for p in PdfReader(os.path.join(t, "reappraisal_offer_memo.pdf")).pages)
    check("memo control sentence", "Rule 18-7" in memo, True)
    dic = open(os.path.join(t, "data_dictionary.txt"), encoding="utf-8").read()
    check("dictionary control", "validation_code" in dic, True)

    r26 = {x["parcel_id"]: x for x in rows(os.path.join(t, "assessor_roll_2026_certified.csv"))}
    xw = {x["nbhd_name"]: x for x in rows(os.path.join(t, "neighborhood_crosswalk.csv"))}
    idx = {x["period"]: float(x["index_jan2025_100"]) for x in rows(os.path.join(t, "residential_price_index_tillford.csv"))}
    deeds = rows(os.path.join(t, "recorder_deeds_2025.csv"))
    permits = rows(os.path.join(t, "building_permits_2025.csv"))
    changes = rows(os.path.join(t, "parcel_change_log_2025.csv"))
    bor = rows(os.path.join(t, "board_of_review_hearings_2025.csv"))
    jan = idx["2026-01"]
    to26 = lambda p: p.replace("-", "") + "0"

    def carry(dstr):
        d = day(dstr)
        return jan / idx["%d-%02d" % (d.year, d.month)]

    # ---- single-family ----------------------------------------------------------------------------------------------
    r1 = {k: v for k, v in r26.items() if v["class_code"] == "R1"}
    last_fin = {}
    for p in permits:
        if p["final_inspection_date"]:
            k = to26(p["parcel_no"])
            last_fin[k] = max(last_fin.get(k, ""), p["final_inspection_date"])
    chg_eff = {}
    for c in changes:
        if c["change_type"] in ("SPLIT", "COMBINE"):
            chg_eff[c["old_parcel_no"]] = max(chg_eff.get(c["old_parcel_no"], ""), c["effective_date"])
    q = [d for d in deeds if d["validation_code"] == "Q" and to26(d["parcel_no"]) in r1]
    reviewed = {to26(d["parcel_no"]) for d in q}
    study = []
    for d in q:
        k = to26(d["parcel_no"])
        f = last_fin.get(k)
        if f and d["deed_date"] < f < "2026-01-01":
            continue
        e = chg_eff.get(d["parcel_no"])
        if e and d["deed_date"] < e < "2026-01-01":
            continue
        pj = int(d["consideration"]) * carry(d["deed_date"])
        study.append(dict(k=k, pj=pj, av26=int(r1[k]["total_assessed_value"]), nb=r1[k]["nbhd_code"],
                          av25=r25[d["parcel_no"]]["total"]))
    check("study sales", len(study), F["evidence"]["study_sales"])
    ratios = [x["av26"] / x["pj"] for x in study]
    m = statistics.median(ratios)
    check("default path level", round(m, 2), F["default_path"]["level"])
    check("default path COD", round(100 * statistics.fmean(abs(r - m) for r in ratios) / m, 1), F["default_path"]["cod"])
    # changes over parcels on both rolls under one identifier
    chg_by_nb, sold_chg, unsold_chg = {}, [], []
    for k25, v in r25.items():
        if v["cls"] != "Residential single family":
            continue
        k = to26(k25)
        if k not in r1:
            continue
        c = int(r1[k]["total_assessed_value"]) / v["total"]
        if k in reviewed:
            sold_chg.append(c)
        else:
            unsold_chg.append(c)
            chg_by_nb.setdefault(r1[k]["nbhd_code"], []).append(c)
    check("sold change", round(100 * (statistics.median(sold_chg) - 1), 1), F["evidence"]["sold_change_pct"])
    check("unsold change", round(100 * (statistics.median(unsold_chg) - 1), 1), F["evidence"]["unsold_change_pct"])
    fac = {nb: statistics.median(v) for nb, v in chg_by_nb.items()}
    share = len(reviewed) / len(r1)
    check("reviewed share", round(100 * share, 1), F["evidence"]["reviewed_share_pct"])
    pairs = [(round(x["av25"] * fac[x["nb"]], -2) / x["pj"], 1 - share) for x in study] + \
            [(x["av26"] / x["pj"], share) for x in study]
    lev = wmedian(pairs)
    cod = 100 * sum(w * abs(r - lev) for r, w in pairs) / sum(w for _, w in pairs) / lev
    check("golden level", round(lev, 2), F["call"]["level"])
    check("golden COD", int(round(cod)), F["call"]["cod"])

    # ---- Ask A: the condominium class ----------------------------------------------------------------------------------
    renum = {c["old_parcel_no"]: c for c in changes if c["change_type"] in ("RENUMBER", "COMBINE")
             and c["old_parcel_no"][:3] >= "200"}
    def as26(no, when):
        c = renum.get(no)
        if c and when < c["effective_date"]:
            return c["new_parcel_id"], c["change_type"] == "COMBINE"
        return to26(no), False

    cfin = {}
    for p in permits:
        if p["final_inspection_date"] and p["parcel_no"][:3] >= "200":
            k, _ = as26(p["parcel_no"], p["issued_date"])
            cfin[k] = max(cfin.get(k, ""), p["final_inspection_date"])
    cs = []
    for d in deeds:
        if d["validation_code"] != "Q":
            continue
        k, combined = as26(d["parcel_no"], d["deed_date"])
        if combined:
            continue
        if k not in r26 or r26[k]["class_code"] != "R2":
            continue
        f = cfin.get(k)
        if f and d["deed_date"] < f < "2026-01-01":
            continue
        cs.append((int(r26[k]["total_assessed_value"]), int(d["consideration"]) * carry(d["deed_date"])))
    cr = [a / p for a, p in cs]
    cm = statistics.median(cr)
    check("condominium sales", len(cs), F["ask_a"]["sales"])
    check("condominium level", round(cm, 2), F["ask_a"]["level"])
    check("condominium COD", round(100 * statistics.fmean(abs(r - cm) for r in cr) / cm, 1), F["ask_a"]["cod"])
    agg = sum(a for a, _ in cs) / sum(p for _, p in cs)
    check("condominium aggregate ratio", round(agg, 3), F["ask_a"]["agg"])
    check("condominium PRD", round(statistics.fmean(cr) / agg, 3), F["ask_a"]["prd"])

    # ---- Ask B: the Board of Review --------------------------------------------------------------------------------------
    last = {}
    for b in bor:
        if not b["hearing_date"] or b["hearing_date"] < "2025-06-02":
            continue
        if int(b["value_before"]) != r25[b["parcel_no"]]["total"]:
            continue
        key = (b["case_no"], b["parcel_no"])
        if key not in last or b["hearing_date"] > last[key]["hearing_date"]:
            last[key] = b
    area = {}
    for b in last.values():
        if b["decision"] != "REDUCED":
            continue
        a = int(xw[r25[b["parcel_no"]]["nb"]]["market_area"])
        x = area.setdefault(a, [set(), 0])
        x[0].add(b["parcel_no"])
        x[1] += int(b["value_before"]) - int(b["value_after"])
    for a in range(1, 7):
        check("Board of Review parcels, area %d" % a, len(area[a][0]), F["ask_b"][str(a)]["parcels"])
        check("Board of Review value, area %d" % a, area[a][1], F["ask_b"][str(a)]["value_off"])

    # ---- the goldens read back -------------------------------------------------------------------------------------------
    import docx
    g = os.path.join(task, "golden")
    doc = docx.Document(os.path.join(g, "reappraisal_recommendation.docx"))
    text = " ".join(p.text for p in doc.paragraphs) + " ".join(c.text for tb in doc.tables for row in tb.rows
                                                               for c in row.cells)
    check("memo carries the level", "%.2f" % F["call"]["level"] in text, True)
    check("memo carries the COD", "dispersion is %d" % F["call"]["cod"] in text, True)
    check("memo carries the condominium PRD", "%.3f" % F["ask_a"]["prd"] in text, True)
    gb = load_workbook(os.path.join(g, "ratio_study_2026_roll.xlsx"), read_only=True)
    sm = list(gb["Summary"].iter_rows(values_only=True))
    check("workbook level", sm[4][1], F["call"]["level"])
    check("workbook condominium COD", sm[5][2], F["ask_a"]["cod"])
    bv = list(gb["Board of Review"].iter_rows(values_only=True))
    check("workbook Board of Review total", bv[7][3], F["ask_b_total"]["value_off"])

    for label, got, want in bad:
        print("  DISAGREE  %s: got %s, figures.json %s" % (label, got, want))
    print("verify: %s" % ("PASS" if not bad else "FAIL (%d)" % len(bad)))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run(os.path.dirname(HERE)))
