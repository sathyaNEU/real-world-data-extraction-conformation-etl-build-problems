"""Builds task482's pack under target/, the golden under golden/, generator/figures.json, submission.md and
metadata.json.

    python3 task482/generator/build.py
"""
import json
import os
import shutil
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import world as W          # noqa: E402
import records as R        # noqa: E402
import pd as PD            # noqa: E402
import billing as BL       # noqa: E402
import files as F          # noqa: E402
import docs as D           # noqa: E402
import golden as G         # noqa: E402
import goldwb as GW        # noqa: E402
import irt                 # noqa: E402
import postprocess as PP   # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")

NAMES = {
    "msa": "lumenfold_msa_v4_2025.docx",
    "orders": "order_forms_2025_26.xlsx",
    "elig": "guarantee_eligibility_2025_26.csv",
    "roster": "district_roster_uploads_spring2026.xlsx",
    "xwalk": "student_id_crosswalk_2025_26.csv",
    "sessions": "lsoa_spring2026_sessions.csv",
    "responses": "lsoa_spring2026_item_responses.csv",
    "items": "caldrith_item_parameters_2024.csv",
    "pv": "caldrith_plausible_values_2026.csv",
    "report": "caldrith_lsoa_technical_report_2026.pdf",
    "pd": "pd_sessions_2025_26.csv",
    "catalog": "professional_learning_catalog_2025_26.pdf",
    "invoices": "billing_invoices_2026_27.csv",
    "layout": "credit_memo_import_layout.pdf",
    "survey": "teacher_implementation_survey_spring2026.csv",
    "renewals": "renewal_forecast_2026_27.xlsx",
}
DELIVERABLES = {"settlement": "lumenfold_guarantee_settlement_2025_26.xlsx",
                "memos": "guarantee_credit_memos_2026.csv"}


def report_figures(v, V):
    """What the technical report states: counts, the population model's coefficients, results from the plausible
    values (every student with a submitted session)."""
    T = {"n_tested": int(len(v["g"]))}
    T["counts"] = {st: [int(((v["state"] == W.STATES.index(st)) & (v["g"] == k)).sum()) for k in range(3)]
                   for st in W.STATES}
    T["n_dist"] = {st: sum(1 for dd in W.DISTRICTS if dd["state"] == st) for st in W.STATES}
    g = V["gamma"] * W.SCALE_B
    rows = [("Grade", "Grade %d" % W.GRADES[k], W.SCALE_A + g[k]) for k in range(3)]
    rows += [("State", W.STATE_NAME[st], g[3 + i]) for i, st in enumerate(W.STATES[1:])]
    rows += [("Prior state-test band", lab, g[8 + i]) for i, lab in enumerate(("Band 2", "Band 3", "Band 4",
                                                                                   "No prior result"))]
    rows += [("Economically disadvantaged", "Yes", g[12]), ("English learner", "Yes", g[13]),
             ("Students with disabilities", "Yes", g[14])]
    T["gamma_rows"] = rows
    T["resid_sd"] = float(np.sqrt(V["s2"]) * W.SCALE_B)
    pv = V["pv"]
    cut = np.array(W.CUT_SCALE)[v["g"]]

    def res(mask, label):
        pct = float(np.mean([(p[mask] >= cut[mask] - 1e-9).mean() for p in pv]) * 100)
        mean = float(np.mean([p[mask].mean() for p in pv]))
        return (label, int(mask.sum()), pct, mean)

    out = [res(np.ones(len(v["g"]), bool), "All students")]
    out += [res(v["g"] == k, "Grade %d" % W.GRADES[k]) for k in range(3)]
    out += [res(v["state"] == i, W.STATE_NAME[st]) for i, st in enumerate(W.STATES)]
    out += [res(v["ed"] == 1, "Economically disadvantaged"), res(v["ed"] == 0, "Not economically disadvantaged"),
            res(v["el"] == 1, "English learner"), res(v["iep"] == 1, "Students with disabilities")]
    out += [res(v["band"] == b, lab) for b, lab in enumerate(("Prior band 1", "Prior band 2", "Prior band 3",
                                                              "Prior band 4", "No prior result"))]
    T["results"] = out
    return T


def finish(t, gold):
    """Office files carry their owners and saved stamps, PDFs their issue dates; two builds are byte-identical."""
    PP.normalize_ooxml(t("msa"), "Legal", "Legal", "2025-05-28T20:40:00Z", "2025-05-28T20:40:00Z")
    PP.normalize_ooxml(t("orders"), "Partnerships Operations", W.PEOPLE["requester"], "2026-11-02T14:05:00Z",
                       "2026-11-02T14:05:00Z", excel=True)
    PP.normalize_ooxml(t("roster"), "Data Services", "Data Services", "2026-04-10T13:20:00Z",
                       "2026-04-10T13:20:00Z", excel=True)
    PP.normalize_ooxml(t("renewals"), "Partnerships Operations", "Partnerships Operations", "2026-09-14T15:00:00Z",
                       "2026-11-06T18:42:00Z", excel=True)
    PP.normalize_ooxml(gold("settlement"), W.PEOPLE["controller"], W.PEOPLE["controller"], "2026-11-23T15:10:00Z",
                       "2026-11-24T21:35:00Z", excel=True)
    PP.normalize_pdf(t("report"), b"D:20260619110000-04'00'", b"D:20260619110000-04'00'")
    PP.normalize_pdf(t("catalog"), b"D:20250714093000-04'00'", b"D:20250714093000-04'00'")
    PP.normalize_pdf(t("layout"), b"D:20260804101500-04'00'", b"D:20260804101500-04'00'")


def main():
    PD.crm_names()
    P = R.build()
    v = R.tested_view(P["c"])
    V = R.contractor(v)
    pd_rows, pd_truth = PD.build()
    inv = BL.build()
    for d in (TARGET, GOLDEN):
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)
    t = lambda k: os.path.join(TARGET, NAMES[k])
    gold = lambda k: os.path.join(GOLDEN, DELIVERABLES[k])
    D.msa_docx(t("msa"))
    F.order_forms_xlsx(t("orders"))
    n = {}
    n["elig"] = F.eligibility_csv(t("elig"), P["elig"])
    n["roster"] = F.roster_xlsx(t("roster"), P["roster"])
    n["xwalk"] = F.crosswalk_csv(t("xwalk"), P["xwalk"])
    n["sessions"] = F.sessions_csv(t("sessions"), P["sessions"])
    n["responses"] = F.responses_csv(t("responses"), P["responses"])
    F.item_params_csv(t("items"), P["item_id"])
    n["pv"] = F.pv_csv(t("pv"), v, V["pv"])
    T = report_figures(v, V)
    D.tech_report_pdf(t("report"), T)
    n["pd"] = F.pd_csv(t("pd"), pd_rows)
    D.catalog_pdf(t("catalog"))
    n["invoices"] = F.invoices_csv(t("invoices"), inv)
    D.layout_pdf(t("layout"))
    F.survey_csv(t("survey"))
    F.renewal_xlsx(t("renewals"))
    rows, memos, share = G.settle(v, pd_truth, inv)
    GW.workbook(gold("settlement"), rows)
    GW.memos_csv(gold("memos"), memos)
    finish(t, gold)
    owed = [x for x in rows if x["result"] == "Not met"]
    figs = {
        "call": {"owed": sorted(x["partner_id"] for x in owed), "n_owed": len(owed),
                 "og_total": round(sum(x["og"] for x in rows), 2)},
        "districts": {x["partner_id"]: {k: x[k] for k in ("name", "state", "benchmark", "result", "credit_pct", "fee",
                                                           "og", "pd_contract", "pd_delivered", "pd_short", "pl",
                                                           "invoice", "account", "assessed")} for x in rows},
        "share_golden": {x["partner_id"]: round(x["share"], 3) for x in rows},
        "pl_total": round(sum(x["pl"] for x in rows), 2),
        "n_pl": sum(1 for x in rows if x["pl"] > 0),
        "credit_total": round(sum(x["og"] + x["pl"] for x in rows), 2),
        "memos": memos,
        "memo": {m["memo_reference"]: {"customer_account": m["customer_account"], "amount": m["credit_amount"],
                                       "apply": m["apply_to_invoice"] if m["refund_method"] == "APPLY" else "CHECK"}
                 for m in memos},
        "memo_row": {m["memo_reference"]: "%s|%.2f|%s" % (m["customer_account"], m["credit_amount"],
                                                           m["apply_to_invoice"] if m["refund_method"] == "APPLY" else "CHECK")
                     for m in memos},
        "n_check": sum(1 for m in memos if m["refund_method"] == "CHECK"),
        "rows": n,
        "files": dict(NAMES),
        "deliverables": dict(DELIVERABLES),
        "n_tested": T["n_tested"],
        "n_districts": len(W.DISTRICTS),
        "n_assessed": int(sum(x["assessed"] for x in rows)),
        "cuts": list(W.CUT_SCALE),
    }
    with open(os.path.join(HERE, "figures.json"), "w") as f:
        json.dump(figs, f, indent=1, sort_keys=True)
    import writeup
    import metadata
    writeup.write(os.path.join(HERE, "figures.json"), os.path.join(TASK, "submission.md"))
    metadata.write(figs, NAMES, os.path.join(TASK, "metadata.json"))
    cut_zip()
    print("built:", ", ".join(sorted(os.listdir(TARGET))))
    return 0


def cut_zip():
    """target.zip from the build just made: the shipped files at the archive's root in name order, each stamped with
    the pack's compile date, so two builds cut byte-identical archives (house fixes H4 and H7)."""
    import zipfile
    path = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(path, "w") as z:
        for name in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo(name, date_time=(2026, 11, 20, 17, 30, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(TARGET, name), "rb") as f:
                z.writestr(zi, f.read())
    with zipfile.ZipFile(path) as z:
        members = z.namelist()
        assert members == sorted(os.listdir(TARGET)), "target.zip members differ from target/"
        for name in members:
            with open(os.path.join(TARGET, name), "rb") as f:
                assert z.read(name) == f.read(), name


if __name__ == "__main__":
    raise SystemExit(main())
