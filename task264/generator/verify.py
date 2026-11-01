"""Independent verifier on its own code path (csv, json, openpyxl, zlib; no pandas, no import of the
generator): reads every shipped format back, recomputes the call and every ask figure from target/, and
compares them with golden/ and figures.json. Exit 1 on any mismatch."""
import base64
import csv
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile
import zlib
from collections import defaultdict
from openpyxl import load_workbook

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def half_up(x):
    return int(math.floor(x + 0.5))


def d_dmy(s):
    return dt.datetime.strptime(s, "%d/%m/%Y").date() if s else None


def d_iso(s):
    return dt.date.fromisoformat(s[:10]) if s else None


def pdf_strings(path):
    data = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", data, re.S):
        raw = m.group(1).strip()
        try:
            if raw.endswith(b"~>"):
                raw = base64.a85decode(raw[:-2] if not raw.startswith(b"<~") else raw[2:-2])
            raw = zlib.decompress(raw)
        except Exception:
            continue
        for s in re.findall(rb"\(((?:\\.|[^\\)])*)\)\s*Tj", raw):
            out.append(s.replace(rb"\(", b"(").replace(rb"\)", b")").replace(rb"\\", b"\\").decode("latin-1"))
    return " ".join(out)


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main(target):
    T = lambda f: os.path.join(target, f)
    fails = []

    def check(label, ok, detail=""):
        print(("PASS  " if ok else "FAIL  ") + label + ("" if ok else "   " + str(detail)[:300]))
        if not ok:
            fails.append(label)

    # --- the policy, read from its own PDF streams
    pol = pdf_strings(T("spinal_contracting_policy_2027-28.pdf"))
    check("policy PDF decodes (ASCII85 and Flate) and carries Appendix B", "Appendix B" in pol and "Constant" in pol)
    def coef(label):
        return float(re.search(re.escape(label) + r"\s+([+-]?[0-9.]+)", pol).group(1))
    C = dict(k=coef("Constant"), pre=coef("Per point of pre-operative ODI score, measured from 45"),
             age=coef("Per year of age on admission, measured from 55"), fem=coef("Female"), smk=coef("Current smoker"),
             prev=coef("Previous lumbar spinal surgery"), symp=coef("Symptoms for more than 12 months"),
             disc=coef("Disc herniation (primary diagnosis M51.1 or M51.2)"))
    appx = set(c.replace(".", "") for c in re.findall(r"\b(V\d\d\.\d)\b", pol))
    check("Appendix A lists seven procedure codes", len(appx) == 7, appx)
    floor = 14.5 if "at least 14.5 points" in pol else None
    volume = 1250 if "1,250" in pol else None
    check("the floor and the volume are filed", floor and volume)

    # --- reference files
    prov = rows(T("provider_reference_2026-09.csv"))
    unit = {r["provider_code"]: (r["predecessor_provider_code"] or r["provider_code"]) for r in prov}
    site_unit = {r["mossgill_site_code"]: unit[r["provider_code"]] for r in prov if r["mossgill_site_code"]}
    ods_unit = {r["ods_site_code"]: unit[r["provider_code"]] for r in prov}
    codes = rows(T("code_lookup.csv"))
    emerg = {r["code"] for r in codes if r["code_system"] == "Admission method" and r["description"].startswith("Emergency")}
    elect = {r["code"] for r in codes if r["code_system"] == "Admission method" and r["description"].startswith("Elective")}
    check("the code lookup gives elective and emergency admission methods", emerg and elect)

    # --- spells: latest submission of each spell
    best = {}
    raw = rows(T("apc_spells_lumbar_cohort_2022-26.csv"))
    for r in raw:
        k = (r["pseudo_nhs_number"], r["provider_code"], r["admission_date"])
        if k not in best or (r["sus_submitted"], r["spell_id"]) > (best[k]["sus_submitted"], best[k]["spell_id"]):
            best[k] = r
    sp = list(best.values())
    check("the cohort extract holds at least 25,000 rows", len(raw) >= 25000, len(raw))
    by_pat = defaultdict(list)
    for r in sp:
        r["adm"], r["dis"], r["opd"] = d_dmy(r["admission_date"]), d_dmy(r["discharge_date"]), d_dmy(r["procedure_date"])
        by_pat[r["pseudo_nhs_number"]].append(r)
    index = []
    for r in sp:
        if r["admission_method"] in elect and r["primary_procedure"] in appx:
            prior = [x for x in by_pat[r["pseudo_nhs_number"]] if x["primary_procedure"] in appx and x["opd"]
                     and 0 < (r["opd"] - x["opd"]).days <= 365]
            if not prior:
                index.append(r)

    # --- questionnaires: the xlsx (item answers) and the csv (section totals)
    wb = load_workbook(T("mossgill_spinal_proms_2022-04_to_2025-03.xlsx"), read_only=True)
    ws = wb["Questionnaires"]
    it = ws.iter_rows(values_only=True)
    for _ in range(3):
        next(it)
    head = list(next(it))
    Q = []
    dur = {"Less than 3 months": 1, "3 to 12 months": 2, "1 to 2 years": 3, "More than 2 years": 4}
    for v in it:
        v = list(v) + [None] * (len(head) - len(v))
        r = dict(zip(head, v))
        ans = [r["ODI%d" % i] for i in range(1, 11) if r["ODI%d" % i] is not None]
        Q.append(dict(ref=r["PatientRef"], site=r["Site"], op=r["OperationDate"].date(), done=r["Completed"].date(),
                      pre=r["Questionnaire"] == "Pre-operative", yob=int(r["BirthYear"]), sex=2 if r["Sex"] == "F" else 1,
                      smk=r["Smoker"] == "Yes", prev=r["PreviousSpinalSurgery"] == "Yes", dur=dur.get(r["SymptomDuration"]),
                      n=len(ans), tot=sum(ans)))
    for r in rows(T("mossgill_spinal_proms_2025-04_to_2026-09.csv")):
        Q.append(dict(ref=r["patient_ref"], site=r["site_code"], op=d_dmy(r["operation_date"]), done=d_iso(r["completed_date"]),
                      pre=r["questionnaire"] == "PREOP", yob=int(r["birth_year"]), sex=int(r["sex"]), smk=r["smoker"] == "Y",
                      prev=r["previous_spinal_surgery"] == "Y", dur=int(r["symptom_duration"]) if r["symptom_duration"] else None,
                      n=int(r["odi_sections_answered"]), tot=float(r["odi_raw_score"])))
    link = {r["patient_ref"]: r["pseudo_nhs_number"] for r in rows(T("mossgill_nhs_number_link_2026-09.csv"))}
    for q in Q:
        q["pseudo"] = link.get(q["ref"], "")
        q["score"] = q["tot"] / (5.0 * q["n"]) * 100.0 if q["n"] >= 8 else None
    pre_by, m12_by = defaultdict(list), defaultdict(list)
    for q in Q:
        if q["pseudo"] and q["score"] is not None:
            (pre_by if q["pre"] else m12_by)[q["pseudo"]].append(q)
    death = {}
    for r in rows(T("cohort_deaths_linked_2026-09.csv")):
        dd = d_iso(r["date_of_death"])
        death[r["pseudo_nhs_number"]] = min(dd, death.get(r["pseudo_nhs_number"], dd))

    # --- the eligible population and each operation's change
    el = []
    for r in index:
        if not (dt.date(2023, 4, 1) <= r["opd"] <= dt.date(2025, 3, 31)):
            continue
        p = r["pseudo_nhs_number"]
        pres = [q for q in pre_by[p] if 0 <= (r["opd"] - q["done"]).days <= 89]
        if not pres:
            continue
        if p in death and death[p] <= r["opd"] + dt.timedelta(days=365):
            continue
        pq = max(pres, key=lambda q: q["done"])
        ms = sorted([q for q in m12_by[p] if 336 <= (q["done"] - r["opd"]).days <= 448], key=lambda q: q["done"])
        E = (C["k"] + C["pre"] * (pq["score"] - 45) + C["age"] * (int(r["age_on_admission"]) - 55) + C["fem"] * (r["sex"] == "2")
             + C["smk"] * pq["smk"] + C["prev"] * pq["prev"] + C["symp"] * ((pq["dur"] or 0) >= 3)
             + C["disc"] * (r["primary_diagnosis"] in ("M511", "M512")))
        later = [x for x in by_pat[p] if x["adm"] > r["adm"] and x["admission_method"] in emerg and r["dis"]
                 and 0 < (x["adm"] - r["dis"]).days <= 90]
        el.append(dict(u=unit[r["provider_code"]], E=E, resp=bool(ms), d=(pq["score"] - ms[0]["score"] - E) if ms else None,
                       flag=bool(later)))
    netE = sum(x["E"] for x in el) / len(el)
    out = {}
    for u in sorted({x["u"] for x in el}):
        g = [x for x in el if x["u"] == u]
        tot = 0.0
        for f in (False, True):
            c = [x for x in g if x["flag"] == f]
            a = [x["d"] for x in c if x["resp"]]
            tot += sum(a) + (sum(a) / len(a)) * (len(c) - len(a))
        out[u] = netE + tot / len(g)
    wbc = load_workbook(T("spinal_capacity_returns_2027-28.xlsx"), read_only=True)
    cap = {}
    for v in list(wbc["Returns"].iter_rows(values_only=True))[5:]:
        if v and v[1]:
            cap[ods_unit[v[1]]] = int(v[6])
    order = sorted([u for u in out if out[u] >= floor], key=lambda u: -out[u])
    left, placed = volume, {}
    for u in order:
        placed[u] = min(cap[u], left)
        left -= placed[u]
    print("verifier outcomes:", {u: round(v, 2) for u, v in out.items()})
    print("verifier placement:", placed, "held", volume - sum(placed.values()))

    # --- Ask A, the waiting list on 31 March 2026
    tri = json.load(open(T("msk_triage_referrals_2023-06_to_2026-03.json")))["referrals"]
    idx = defaultdict(list)
    for t in tri:
        if t["outcome"] == "Surgical opinion - spinal" and t["routed_to"]:
            idx[(t["birth_year"], 2 if t["sex"] == "F" else 1, t["postcode_district"], t["gp_practice"],
                 ods_unit[t["routed_to"]])].append((d_iso(t["outcome_date"]), d_iso(t["received"])))
    rem = rows(T("ptl_spinal_removals_2025-11_to_2026-04.csv"))
    moved = [r for r in rem if r["removal_reason"] == "Transferred to another provider"]
    snap = dt.date(2026, 3, 31)
    gone = {(r["provider_code"], r["pathway_id"]) for r in moved if d_dmy(r["removal_date"]) <= snap}

    def tclock(u, by, sx, dist, gp, rec):
        c = [x for od, x in idx.get((by, sx, dist, gp, u), []) if od <= rec <= od + dt.timedelta(days=10)]
        return c[0] if len(c) == 1 else None
    A = defaultdict(lambda: [0, 0, 0])
    for r in rows(T("ptl_spinal_month_end_2026-01_to_2026-03.csv")):
        if r["snapshot_date"] != "2026-03-31" or (r["provider_code"], r["pathway_id"]) in gone:
            continue
        u = unit[r["provider_code"]]
        rec = d_dmy(r["referral_received"])
        clock = d_dmy(r["rtt_clock_start"])
        key = (int(r["birth_year"]), int(r["sex"]), r["postcode_district"], r["gp_practice"])
        if r["referral_route"] == "MSK triage":
            clock = tclock(u, *key, rec) or clock
        elif r["referral_route"] == "Transfer":
            o = [x for x in moved if x["pseudo_nhs_number"] == r["pseudo_nhs_number"] and d_dmy(x["removal_date"]) == rec]
            if len(o) == 1:
                o = o[0]
                clock = d_dmy(o["rtt_clock_start"])
                if o["referral_route"] == "MSK triage":
                    clock = tclock(unit[o["provider_code"]], *key, d_dmy(o["referral_received"])) or clock
        days = (snap - clock).days
        A[u][0] += 1
        A[u][1] += days > 364
        A[u][2] += days <= 126

    # --- Ask B, 2025-26 participation
    linked = {r["pseudo_nhs_number"] for r in index} & set(link.values())
    yr = [r for r in index if dt.date(2025, 4, 1) <= r["opd"] <= dt.date(2026, 3, 31)]
    ok = set()
    for r in yr:
        if any(0 <= (r["opd"] - q["done"]).days <= 89 for q in pre_by[r["pseudo_nhs_number"]]):
            ok.add(r["spell_id"])
    free = [r for r in index if r["pseudo_nhs_number"] not in linked]
    for q in Q:
        if not q["pre"] or q["pseudo"] or q["score"] is None:
            continue
        u = site_unit[q["site"]]
        cand = []
        for r in free:
            if unit[r["provider_code"]] != u or int(r["sex"]) != q["sex"]:
                continue
            a = int(r["age_on_admission"])
            if not (r["adm"].year - a - 1 <= q["yob"] <= r["adm"].year - a):
                continue
            gap = (r["opd"] - q["op"]).days
            if -30 <= gap <= 120:
                cand.append((abs(gap), r["spell_id"], r))
        if cand:
            r = sorted(cand)[0][2]
            if dt.date(2025, 4, 1) <= r["opd"] <= dt.date(2026, 3, 31) and 0 <= (r["opd"] - q["done"]).days <= 89:
                ok.add(r["spell_id"])
    B = defaultdict(lambda: [0, 0])
    for r in yr:
        u = unit[r["provider_code"]]
        B[u][0] += 1
        B[u][1] += r["spell_id"] in ok

    # --- against the goldens and figures.json
    gold = rows(os.path.join(TASK, "golden", "spinal_volume_2027-28.csv"))
    for g in gold:
        if not g["provider_code"]:
            check("held volume in the golden csv", int(g["operations_placed"]) == volume - sum(placed.values()))
            continue
        u = unit[g["provider_code"]]
        check("golden csv %s: outcome and placement" % g["provider"],
              int(g["outcome_points"]) == half_up(out[u]) and int(g["operations_placed"]) == placed.get(u, 0),
              (g["outcome_points"], round(out[u], 2), g["operations_placed"], placed.get(u, 0)))
    figs = json.load(open(os.path.join(TASK, "generator", "figures.json")))
    nm = {unit[g["provider_code"]]: g["provider"] for g in gold if g["provider_code"]}
    for a in figs["askA"]:
        u = [k for k, v in nm.items() if v == a["provider"]][0]
        check("Ask A %s: over 52 weeks and within 18 weeks" % a["provider"],
              a["over52"] == A[u][1] and a["within18_pct"] == half_up(100.0 * A[u][2] / A[u][0]),
              (a, A[u]))
    for b in figs["askB"]:
        u = [k for k, v in nm.items() if v == b["provider"]][0]
        check("Ask B %s: participation" % b["provider"], b["participation_pct"] == half_up(100.0 * B[u][1] / B[u][0]),
              (b, B[u]))
    # the board paper's tables, read from its XML
    with zipfile.ZipFile(os.path.join(TASK, "golden", "spinal_volume_board_paper.docx")) as z:
        xml = z.read("word/document.xml").decode("utf-8")
        check("the board paper embeds its chart", any(n.startswith("word/media/") for n in z.namelist()))
    text = re.sub(r"<[^>]+>", " ", xml)
    for g in gold:
        if g["provider_code"]:
            check("board paper names %s" % g["provider"], g["provider"] in text)
    check("board paper states the placement and the volume held",
          ("%s" % format(sum(placed.values()), ",")) in text and str(volume - sum(placed.values())) in text)
    print("\nverify: %d failures" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")))
