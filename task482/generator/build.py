"""Builds task482's pack (architecture 14) into target/ and the golden deliverables into golden/, writes
generator/figures.json, and cuts target.zip; two runs are byte-identical.

    python3 task482/generator/build.py          # the whole build
    python3 task482/generator/build.py pack     # the pack only
"""
import json
import os
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
sys.path.insert(0, HERE)

import world as W          # noqa: E402
import pack as P           # noqa: E402

NAMES = dict(
    mlh_claims="mlh_tcoc_claims_2025-01_2026-09.csv", mlh_elig="mlh_eligibility_2025_2026.csv",
    mlh_attr="mlh_attribution_runs_py2025_py2026.csv", mlh_ccf="mlh_care_coordination_remittance_2026.csv",
    kbp_claims="KBP_CLAIMS_LPN_20261009.txt", kbp_elig="KBP_ELIG_LPN_20261009.txt",
    kbp_attr="KBP_ATTRIBUTION_PY2025F_PY2026R10.xlsx", kbp_ccf="KBP_CCF_REMIT_2026.xlsx",
    pmh_claims="pmh_partner_claims_2026-10-12.json", pmh_members="pmh_members_2026-10-12.csv",
    pmh_attr="pmh_attribution_py2025_py2026.csv", pmh_ccf="pmh_ccf_payments_2026.csv",
    roster="lpn_primary_care_roster_2026-10.xlsx", mpi="lpn_master_patient_index.csv",
    fees="payer_em_fee_schedules_2026.xlsx", qualifying="qualifying_primary_care_services.csv",
    cf="payer_completion_factors_2026-09.csv", standard="lpn_performance_standard_2026.pdf",
    resolution="lpn_board_resolution_2026-07.pdf", statements="payer_settlement_statements_py2025.pdf",
    guide="lpn_payer_feed_field_guide.txt", ma="kbp_medicare_advantage_attribution_2026.xlsx",
    quality="lpn_quality_composite_2025.csv")
GOLD = dict(workbook="two_sided_track_elections_2027.xlsx", chart="practice_cost_vs_benchmark_2026.png")


def t(k):
    return os.path.join(TARGET, NAMES[k])


def gpath(k):
    return os.path.join(GOLDEN, GOLD[k])


def pack(with_docs=True):
    for d in (TARGET, GOLDEN):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    w = W.build()
    ids = W.member_ids(w["people"])
    idx, members = P.shared_rows(w, ids)
    P.claims_mlh(t("mlh_claims"), w, ids, idx["B"])
    P.claims_kbp(t("kbp_claims"), w, ids, idx["M"])
    P.claims_pmh(t("pmh_claims"), w, ids, idx["T"])
    P.eligibility_files(t, w, ids, members)
    P.attribution_files(t, w, ids)
    lines = P.remittance_files(t, w)
    P.roster_file(t, w)
    P.mpi_file(t, w, ids, members)
    P.fee_schedule_file(t)
    P.qualifying_codes_file(t)
    cf = W.completion_factors(w["claims"])
    P.completion_factor_file(t("cf"), cf)
    if with_docs:
        import docs as Dc
        import postprocess as PP
        Dc.write_all(t, w, ids, cf)
        P.distractor_files(t, w, ids)
        for k in ("kbp_attr", "kbp_ccf", "roster", "fees", "ma"):
            PP.normalize_ooxml(t(k), excel=True, **PP.OWNERS[k])
        for k, stamp in Dc.STAMPS.items():
            PP.normalize_pdf(t(k), stamp, stamp)
    return dict(world=w, ids=ids, members=members, remit=lines, cf=cf)


def main():
    built = pack()
    import golden as G
    import goldfiles as GF
    p = G.load(TARGET)
    figs = GF.write(gpath, p)
    import postprocess as PP
    PP.normalize_ooxml(gpath("workbook"), W.PEOPLE["analytics"], W.PEOPLE["analytics"], "2026-10-26T14:05:00Z",
                       "2026-10-27T21:40:00Z", title="Two-sided track elections 2027", excel=True)
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    import writeup
    writeup.main()
    import metadata
    metadata.main()
    cut_zip()
    print("built: %d files in target/, %d in golden/" % (len(os.listdir(TARGET)), len(os.listdir(GOLDEN))))
    return built


def cut_zip():
    """Each file keeps the date its source produced it (metadata.SOURCES) and a working-hours time of its own."""
    import hashlib
    import metadata
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for n in sorted(os.listdir(TARGET)):
            y, mo, d = (int(x) for x in metadata.SOURCES[n][1].split("-"))
            h = int(hashlib.md5(n.encode()).hexdigest(), 16)
            zi = zipfile.ZipInfo(n, date_time=(y, mo, d, 7 + h % 11, (h // 11) % 60, ((h // 660) % 30) * 2))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, n), "rb").read())


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "pack":
        pack(with_docs="nodocs" not in sys.argv)
    else:
        main()
