"""Generator checks for task133 architecture 4, run on the installed target/ and the world's clean truth.

    python3 task133/generator/checks.py            # exit 1 on any failed assertion
"""
import csv
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TDIR = os.path.join(TASK, "target")
REPO = os.path.dirname(TASK)
sys.path.insert(0, HERE)

import analysis as A  # noqa: E402
import docs  # noqa: E402
import pack  # noqa: E402
import params as P  # noqa: E402
import results as R  # noqa: E402
import world  # noqa: E402
from io_util import pdf_text  # noqa: E402

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok)))
    print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [%s]" % (detail,)) if detail != "" else ""))


def docx_text(path):
    from docx import Document
    d = Document(path)
    return "\n".join([p.text for p in d.paragraphs] + [" | ".join(c.text for c in r.cells) for t in d.tables for r in t.rows])


def bins(res_entry):
    return R.nearest(sum(res_entry.values()), 100), {g: R.nearest(v, 50) for g, v in res_entry.items()}


def edge(x, step):
    return step / 2 - abs(x - R.nearest(x, step))


def main():
    files = sorted(os.listdir(TDIR))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    F = R.compute(TDIR)
    pk, res = A.ladder(TDIR)
    gold_bins = bins(res["golden"])
    basis = docx_text(os.path.join(TDIR, docs.BASIS))
    approval = pdf_text(os.path.join(TDIR, docs.APPROVAL))

    # ------------------------------------------------------------------ input gates
    check("gate: 10 or more files", len(files) >= 10, len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    check("gate: 3 or more formats", len(fmts) >= 3, sorted(fmts))
    rows = {f: sum(1 for _ in open(os.path.join(TDIR, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv")}
    check("gate: a file of 25,000 or more rows", max(rows.values()) >= 25000, max(rows.values()))
    check("gate: the bulk file is lean (under 250,000 rows)", max(rows.values()) < 250000)
    check("gate: two or more distractors named in metadata.json",
          len(meta["distractor_files"]) >= 2 and all(d["file"] in files for d in meta["distractor_files"]))
    bad = [f for f in files if re.search(r"readme|dictionar|notes|manifest|schema|test_|trap|decoy|answer|golden", f, re.I)]
    check("gate: no file describes the data or carries an author word in its name", not bad, bad)
    check("gate: the deliverables exist in golden/", all(os.path.exists(os.path.join(TASK, "golden", d)) for d in meta["deliverables"]))

    # ------------------------------------------------------------------ the three rules on the clean truth
    W = world.make()
    t_gold = world.truth_loads(W)
    t_mass = world.truth_loads(W, mass_only=True)
    hdrs = []
    for f in (pack.WB, pack.SC):
        hdrs += open(os.path.join(TDIR, f), encoding="utf-8").readline().strip().lower().split(",")
    from openpyxl import load_workbook
    hdrs += [str(c).lower() for c in list(load_workbook(os.path.join(TDIR, pack.FLEET), read_only=True)["Fleet"].iter_rows(
        min_row=3, max_row=3, values_only=True))[0]]
    check("R1 the field's raw material ships: each load's net mass on the port weighbridge, its JAS volume at the "
          "scaling station, each unit's tare and full-bunk volumes", rows[pack.WB] == len(W.loads) and rows[pack.SC] == len(W.loads))
    deciding = [h for h in hdrs if re.search(r"payload|gross|limit|cube|fy2028|density|headroom", h)]
    check("R2 the deciding quantity has no column: no file stores a load's FY2028 payload, its gross mass or which limit bound it",
          not deciding, deciding)
    check("R3a the analyst test on the clean truth: the mass-only payloads file another bin than the payloads capped by "
          "the bunks", R.nearest(sum(t_mass.values()), 100) != R.nearest(sum(t_gold.values()), 100),
          "%.0f against %.0f" % (sum(t_mass.values()), sum(t_gold.values())))
    cheap = ["R0_fleet_average_plus_six", "R1_permit_units_to_the_new_limit", "R2_loads_at_the_old_limit_only",
             "R3_one_bunk_volume_per_unit", "R4_plus_six_on_permit_units"]
    landing = [k for k in cheap if bins(res[k])[0] == gold_bins[0]]
    check("R3b cheap routes that land the call: none of the enumerated reflexes", not landing,
          {k: round(sum(res[k].values())) for k in cheap})
    honest = ["V_grade_mean_density", "V_unmapped_plates_dropped"]
    check("R3b the defensible family lands the call and every grade: per-load or grade-mean density, the two "
          "re-registered units' early loads kept or dropped", all(bins(res[k]) == gold_bins for k in honest),
          {k: round(sum(res[k].values())) for k in honest})
    leak_fig = [f for f in (docs.BASIS, docs.APPROVAL, docs.GRADESPEC)
                if re.search(r"\b2[5-9],\d{3}\b|\bloads? needed\b", docx_text(os.path.join(TDIR, f)) if f.endswith("docx")
                             else pdf_text(os.path.join(TDIR, f)))]
    check("R3c no decoy: no shipped document states FY2028 loads or a payload under the new limits", not leak_fig, leak_fig)
    check("R3c no certified replay: no file publishes a payload or load figure the method must reproduce",
          "payload" not in approval.lower())

    # ------------------------------------------------------------------ semantic fork table
    check("SF1 a load is one trip to Port Kowhai weighed on the port weighbridge: every ticket is a Matiri forest load",
          all(t["supplier"] == "MATIRI" and t["forest_code"] in P.FORESTS for t in pk.wb) and docs.S_LOAD in basis)
    check("SF2 FY2028 runs 1 July 2027 to 30 June 2028 (planning basis 2.2, the plan's own title)", docs.S_YEAR in basis)
    check("SF3 the fleet is the register at 30 June 2026: every ticket's registration is a current or previous one on it",
          all(l["unit"] is not None for l in pk.loads) and docs.S_FLEET in basis)
    over = 0
    for l in pk.loads:
        if l["grade"] in ("KI", "KIS") and l["unit"]["50MAX permit"] == "Y":
            m = P.NEW_GROSS - float(l["unit"]["Tare (t)"])
            over += m / (l["net"] / l["jas"]) > pk.cap(l["unit"], l["grade"])
    check("SF4 the FY2028 payload is what the unit can carry: letting permit units load to 50 t gross less tare would put "
          "%d short-grade loads past their full-bunk volume, which no load in FY2026 exceeds" % over,
          over > 1000 and all(l["jas"] <= pk.cap(l["unit"], l["grade"]) + 0.02 for l in pk.loads)
          and bins(res["R1_permit_units_to_the_new_limit"])[0] != gold_bins[0])
    check("SF5 permit units at 50 t gross from 1 July 2027 on every forest's route, all others at 44 t (3.2, RDC-2026-114)",
          docs.S_LIMITS in basis and "50 tonnes gross" in approval and "44 tonnes gross" in approval)
    check("SF6 FY2028 loads by grade are the plan's tonnes over the grade's average FY2028 payload (3.1)", docs.S_LOADS in basis)
    check("SF7 per-load density or the grade's mean density: same call", bins(res["V_grade_mean_density"]) == gold_bins)
    links = {}
    for win in (30, 60, 90):
        by = {}
        for s in pk.sc:
            by.setdefault(s["truck_rego"], []).append((dt.datetime.strptime(s["scaled_at"], "%Y-%m-%d %H:%M:%S"), s["scale_ref"]))
        out = []
        for t in pk.wb:
            tw = dt.datetime.strptime(t["weighed_at"], "%d/%m/%Y %H:%M")
            c = sorted(x for x in by[t["vehicle_rego"]] if tw <= x[0] <= tw + dt.timedelta(minutes=win))
            out.append(c[0][1] if c else None)
        links[win] = out
    check("SF8 each ticket links to one scaling record under any window from 30 to 90 minutes, and every record is used once",
          links[30] == links[60] == links[90] and None not in links[60] and len(set(links[60])) == len(links[60]))
    check("SF9 the two re-registered units' early loads read through their previous registrations, or dropped: same call",
          bins(res["V_unmapped_plates_dropped"]) == gold_bins)
    check("SF10 grade lengths from the 2025 grade specification match the bunk classes on the register",
          pk.length == {g: P.GRADES[g]["length"] for g in P.GRADE_ORDER})
    check("SF11 rounding: the total sits 20 or more loads from its 100-load edge and every grade 10 or more from its "
          "50-load edge, under the golden and the defensible family",
          min(edge(sum(res[k].values()), 100) for k in ["golden"] + honest) >= 20 and
          min(edge(res[k][g], 50) for k in ["golden"] + honest for g in P.GRADE_ORDER) >= 10,
          (round(min(edge(sum(res[k].values()), 100) for k in ["golden"] + honest), 1),
           round(min(edge(res[k][g], 50) for k in ["golden"] + honest for g in P.GRADE_ORDER), 1)))
    check("SF12 the plan's export sheet only: the domestic sheet is mill tonnes, outside 2.1's loads",
          abs(sum(pk.plan.values()) - F["plan_total"]) < 1)
    check("SF13 the ticket's net tonnes are the load's payload (tare from the register)",
          all(abs(l["net"] - round(l["net"], 2)) < 1e-9 for l in pk.loads))
    check("SF14 every FY2026 ticket falls in 1 July 2025 to 30 June 2026",
          all(P.FY26[0] <= l["date"] <= P.FY26[1] for l in pk.loads))
    check("SF15 the approval covers all five forests' roads", all(P.FORESTS[f]["name"].split()[0] in approval for f in P.FORESTS))
    billed = A.ask_a(TDIR, pk, by_owner=False)
    check("SF16 cartage against the carrier whose unit hauled the load (4.1): the billed code moves every carrier",
          all(R.rhu(billed[c] / 1e3, 0) != F["ask_a_k"][c] for c in P.CARRIERS) and docs.S_CART in basis)
    nocr = A.ask_a(TDIR, pk, credits=False)
    check("SF17 net of credit notes (4.1): leaving them out moves the carriers billed twice",
          any(R.rhu(nocr[c] / 1e3, 0) != F["ask_a_k"][c] for c in P.CARRIERS))
    dock = A.ask_b(TDIR, by_weighbridge=False)
    check("SF18 deliveries by delivery date (4.2): the dockets' posting dates move every mill-quarter",
          all(R.nearest(dock[k], 10) != F["ask_b_10"][k] for k in dock) and docs.S_MILL in basis)
    mwb = A.read_csv(os.path.join(TDIR, pack.MWB))
    dks = A.read_csv(os.path.join(TDIR, pack.DOCK))
    dk_t = {d["docket_no"]: float(d["tonnes"]) for d in dks}
    same = [abs(float(r["gross_t"]) - float(r["tare_t"]) - dk_t[r["supplier_docket"]]) < 0.011
            for r in mwb if r["supplier_docket"] in dk_t]
    check("SF19 tonnes delivered are the mill weighbridge's gross less tare, equal to the docket's tonnes", all(same), len(same))
    n_fy = sum(1 for m_ in W.mill_loads if P.FY26[0] <= m_["date"] <= P.FY26[1])
    check("SF20 Matiri's loads in the mills' logs carry its docket series (MFP): one row per FY2026 delivery",
          sum(1 for r in mwb if r["supplier_docket"].startswith("MFP")) == n_fy, n_fy)

    # ------------------------------------------------------------------ Layer 1 mess neutrality
    check("L1 the scaling station's own clock and reference: links hold under any window 30 to 90 minutes", links[30] == links[90])
    check("L1 two units re-registered on 1 February 2026: dropping their early loads keeps the call",
          bins(res["V_unmapped_plates_dropped"]) == gold_bins)
    dens = {}
    for l in pk.loads:
        dens.setdefault(l["grade"], []).append(l["net"] / l["jas"])
    check("L1 JAS volume beside green tonnes: every grade's mean density sits between 0.95 and 1.18 t per JAS m3",
          all(0.95 < sum(v) / len(v) < 1.18 for v in dens.values()), {g: round(sum(v) / len(v), 3) for g, v in dens.items()})
    check("L1 grade codes on tickets, grade names in the plan: every code maps through the grade specification",
          set(pk.plan) == set(P.GRADE_ORDER))
    check("L1 tickets carry net mass only, the register the tare: no FY2026 load exceeds 44 t gross",
          max(l["net"] + float(l["unit"]["Tare (t)"]) for l in pk.loads) <= 44.0 + 1e-6)

    # ------------------------------------------------------------------ ask separation and device mass
    tmp = tempfile.mkdtemp()
    try:
        main_files = [pack.WB, pack.SC, pack.FLEET, pack.PLAN, docs.GRADESPEC]
        for f in main_files:
            shutil.copy(os.path.join(TDIR, f), tmp)
        _, res2 = A.ladder(tmp)
        check("separation: the call computes from its own files alone (every ask file and distractor deleted)",
              abs(sum(res2["golden"].values()) - sum(res["golden"].values())) < 1e-6)
        for f in os.listdir(tmp):
            os.remove(os.path.join(tmp, f))
        for f in files:
            if f not in [d["file"] for d in meta["distractor_files"]]:
                shutil.copy(os.path.join(TDIR, f), tmp)
        F2 = R.compute(tmp)
        check("distractor deletion: every graded figure unchanged", F2["total_100"] == F["total_100"] and
              F2["grade_50"] == F["grade_50"] and F2["ask_a_k"] == F["ask_a_k"] and F2["ask_b_10"] == F["ask_b_10"])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    port_tickets = {t["ticket_no"] for t in pk.wb}
    inv = A.read_csv(os.path.join(TDIR, pack.INV))
    check("separation: the invoices reference only port tickets and carry no unit or registration",
          all(r["ticket_ref"] in port_tickets for r in inv) and "vehicle_rego" not in inv[0])
    check("separation: no mill docket appears among the port tickets", not ({d["docket_no"] for d in dks} & port_tickets))
    d_a = min(abs(billed[c] - F["ask_a"][c]) for c in P.CARRIERS)
    check("device A1 subcontracted units billed under the head contractor move every carrier by NZD 100 thousand or more",
          d_a >= 1e5, round(d_a))
    d_b = min(abs(dock[k] - F["ask_b"][k]) for k in dock)
    check("device B1 posting dates move every mill-quarter by 20 t or more", d_b >= 20, round(d_b, 1))
    check("edge: every cartage figure sits NZD 150 or more from its thousand-dollar edge",
          min(abs((v / 1e3) % 1 - 0.5) for v in F["ask_a"].values()) >= 0.15)
    check("edge: every mill-quarter figure sits 1 t or more from its 10-t edge",
          min(edge(v, 10) for v in F["ask_b"].values()) >= 1.0, round(min(edge(v, 10) for v in F["ask_b"].values()), 2))

    # ------------------------------------------------------------------ truth
    check("truth: the pack's loads equal the world's to within one load in total",
          abs(sum(res["golden"].values()) - sum(t_gold.values())) < 1.0, round(sum(res["golden"].values()) - sum(t_gold.values()), 3))
    ta = {c: 0.0 for c in P.CARRIERS}
    for ln in W.invoice_lines:
        ta[ln["hauler"]] += ln["amount"]
    check("truth: cartage by hauler equals the world's invoice lines to the cent", all(abs(ta[c] - F["ask_a"][c]) < 0.01 for c in ta))
    tb = {}
    for r in W.mill_loads:
        q = A.quarter(r["date"])
        if q:
            tb[(r["mill"], q)] = tb.get((r["mill"], q), 0.0) + r["net"]
    check("truth: mill-quarter tonnes equal the world's deliveries", all(abs(tb[k] - F["ask_b"][k]) < 0.05 for k in tb))

    # ------------------------------------------------------------------ realism sweep
    tk = [int(t["ticket_no"]) for t in pk.wb]
    steps = [b - a for a, b in zip(tk, tk[1:])]
    check("realism: ticket numbers rise with gaps (other suppliers' tickets between), no constant step",
          min(steps) >= 1 and len(set(steps)) > 3 and max(steps) > 1)
    regos = [u["Registration"] for u in pk.units]
    check("realism: registrations unique on the register", len(regos) == len(set(regos)))
    names = list(P.CARRIERS.values()) + list(P.MILLS.values())
    check("realism: no placeholder organisation names", not any(re.search(r"\b(Acme|Example|Test|Sample|Company [A-Z])\b", n) for n in names))
    card = json.load(open(os.path.join(REPO, ".claude", "skills", "fingerprint", "cards", "task133.json")))
    people = set(card["world"]["people"])
    creators = set()
    for f in files:
        if f.endswith((".docx", ".xlsx")):
            with zipfile.ZipFile(os.path.join(TDIR, f)) as z:
                creators |= set(re.findall(r"<dc:creator>(.*?)</dc:creator>", z.read("docProps/core.xml").decode()))
    check("realism: every document author is a persona on the card", creators <= people, sorted(creators - people))
    late = [r for r in inv if dt.datetime.strptime(r["document_date"], "%d/%m/%Y") > P.EXPORT_DATE]
    check("realism: no invoice, docket or document dated after the export date 2026-10-20", not late and
          all(dt.datetime.strptime(d["docket_date"], "%d/%m/%Y").date() <= P.FY26[1] for d in dks))
    pays = [l["net"] for l in pk.loads]
    check("realism: FY2026 payloads between 20 and 28 t", 20 <= min(pays) and max(pays) <= 28, (min(pays), max(pays)))
    for d in (TDIR, os.path.join(TASK, "golden")):
        out = subprocess.run([sys.executable, os.path.join(REPO, ".claude", "skills", "reduce-house-fixes", "scripts",
                                                          "scrub_producer_metadata.py"), d, "--floor", "2025-01-01",
                              "--ceiling", "2026-10-20"], capture_output=True, text=True).stdout
        check("H1 no writer signature or out-of-band stamp in %s" % os.path.basename(d), "clean" in out, out.strip()[-100:])
    import pypdf
    for f in (docs.APPROVAL, docs.GRADESPEC):
        strict = pypdf.PdfReader(os.path.join(TDIR, f), strict=True).pages[0].extract_text()
        lay = subprocess.run(["pdftotext", "-layout", os.path.join(TDIR, f), "-"], capture_output=True, text=True).stdout
        key = "50 tonnes gross" if f == docs.APPROVAL else "KIS"
        check("H25 %s reads under a strict parser, pdftotext and the generator's decoder" % f,
              key in strict and key in lay and key in pdf_text(os.path.join(TDIR, f)))
    with zipfile.ZipFile(os.path.join(TASK, "target.zip")) as z:
        zn = sorted(n.split("/", 1)[1] for n in z.namelist())
    check("bundle: target.zip holds exactly target/", zn == files)
    prompt = open(os.path.join(TASK, "prompt.txt"), encoding="utf-8").read()
    check("prompt names both deliverables and states no figure of the answer",
          all(d in prompt for d in meta["deliverables"]) and not re.search(r"\b2[5-9],\d{3}\b", prompt))
    check("figures.json carries the call and every ask figure", figs["call"]["fy2028_loads_nearest_100"] == F["total_100"]
          and len(figs["ask_a_cartage_nzd_k"]) == 6 and len(figs["ask_b_mill_tonnes"]) == 12)
    n_fail = sum(1 for _, ok in RESULTS if not ok)
    print("\n%d assertions, %d failed" % (len(RESULTS), n_fail))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
