"""Builds task482's pack under target/, the golden under golden/ and generator/figures.json.

    python3 task482/generator/build.py
"""
import datetime as dt
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import world as W
import records as R
import pack
import files as F
import docs as D
import golden as Gd
import postprocess as PP

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")

NAMES = {
    "extract": "medicare_hospice_benefit_periods_20270105.txt",
    "emr": "wendleglen_emr_admissions.csv",
    "legacy": "fallowmere_census_register_20250228.xlsx",
    "crosswalk": "hicn_mbi_crosswalk.csv",
    "dx": "diagnosis_groups.csv",
    "claims": "wendleglen_claim_lines_fy2026.csv",
    "remit": "remittance_register_fy2026.csv",
    "policy": "wendleglen_cap_liability_policy.docx",
    "census": "census_report_december_2026.pdf",
    "rates": "fy2026_hospice_payment_rates.pdf",
    "register": "provider_numbers.json",
    "notes": "revenue_cycle_file_notes.pdf",
    "quality": "hospice_quality_measures_2026.xlsx",
    "budget": "fy2027_operating_budget.xlsx",
}


def census_figures(P):
    """ADC, admissions and discharges by program from the EMR export (all payers)."""
    emr = P["tb"]["emr"]
    y0, y1 = dt.date(2026, 1, 1), dt.date(2026, 12, 31)
    dec0 = dt.date(2026, 12, 1)
    adc, adm, dis = {}, {}, {}
    for code in W.CODES:
        ccn = R.CCN[code]
        rows = [r for r in emr if r["provider_number"] == ccn]
        def census(a, z):
            tot = 0
            for r in rows:
                s = max(r["admit_date"], a)
                e = min(r["discharge_date"] or dt.date(2027, 1, 1), z + dt.timedelta(days=1))
                tot += max(0, (e - s).days)
            return tot / ((z - a).days + 1)
        adc[ccn] = (census(dec0, y1), census(y0, y1))
        adm[ccn] = sum(1 for r in rows if y0 <= r["admit_date"] <= y1 and r["admission_type"] != "Conversion")
        dis[ccn] = (sum(1 for r in rows if r["discharge_date"] and y0 <= r["discharge_date"] <= y1 and r["discharge_reason"] == "Expired"),
                    sum(1 for r in rows if r["discharge_date"] and y0 <= r["discharge_date"] <= y1
                        and r["discharge_reason"] in ("Revoked", "No longer terminally ill", "Moved out of service area")))
    return adc, adm, dis


def finish(t, golden_xlsx):
    """Office files carry their owners and saved stamps, PDFs their issue dates; two builds are byte-identical."""
    PP.normalize_ooxml(t("legacy"), "FHI Census", "FHI Census", "2025-03-01T04:41:00Z", "2025-03-01T04:41:00Z",
                       excel=True, company="Fallowmere Hospice Inc")
    PP.normalize_ooxml(t("quality"), "Quality", "Quality", "2026-11-03T19:05:00Z", "2026-11-03T19:05:00Z", excel=True)
    PP.normalize_ooxml(t("budget"), "Finance", "J. Cortez", "2026-10-21T14:30:00Z", "2026-12-02T21:48:00Z", excel=True)
    PP.normalize_ooxml(t("policy"), "B. Graham", "B. Graham", "2023-09-12T13:02:00Z", "2026-11-18T14:12:00Z")
    PP.normalize_ooxml(golden_xlsx, "B. Graham", "B. Graham", "2027-01-08T15:20:00Z", "2027-01-11T22:02:00Z", excel=True)
    PP.normalize_pdf(t("census"), b"D:20270106081500-05'00'", b"D:20270106081500-05'00'")
    PP.normalize_pdf(t("rates"), b"D:20250814102200-04'00'", b"D:20250814102200-04'00'")
    PP.normalize_pdf(t("notes"), b"D:20270107160400-05'00'", b"D:20270107160400-05'00'")


def main():
    P = pack.build()
    for d in (TARGET, GOLDEN):
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)
    tb = P["tb"]
    t = lambda k: os.path.join(TARGET, NAMES[k])
    F.extract_txt(t("extract"), tb["extract"])
    F.emr_csv(t("emr"), tb["emr"])
    F.legacy_xlsx(t("legacy"), tb["legacy"])
    F.crosswalk_csv(t("crosswalk"), tb["crosswalk"])
    F.dx_csv(t("dx"), tb["dx"])
    n_lines = F.claim_lines_csv(t("claims"), P["claims"])
    n_remit = F.remittance_csv(t("remit"), P["remit"])
    F.register_json(t("register"), P["wi"])
    D.policy_docx(t("policy"))
    adc, adm, dis = census_figures(P)
    D.census_pdf(t("census"), P["people"], P["book"].closed_2026, adc, adm, dis)
    D.rates_pdf(t("rates"))
    D.file_notes_pdf(t("notes"), len(tb["extract"]))
    D.quality_xlsx(t("quality"))
    D.budget_xlsx(t("budget"), adc)
    import goldwb
    figs = goldwb.write(P, os.path.join(GOLDEN, "fy2026_hospice_cap_accrual.xlsx"))
    finish(t, os.path.join(GOLDEN, "fy2026_hospice_cap_accrual.xlsx"))
    figs["files"] = {k: NAMES[k] for k in NAMES}
    figs["rows"] = {"extract": len(tb["extract"]), "emr": len(tb["emr"]), "legacy": len(tb["legacy"]),
                    "claim_lines": n_lines, "remittance": n_remit}
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
            zi = zipfile.ZipInfo(name, date_time=(2027, 1, 7, 16, 4, 0))
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
