"""Builds task482's pack (architecture 15) into target/ and the golden deliverables into golden/, writes
generator/figures.json, submission.md and metadata.json, and cuts target.zip; two runs are byte-identical.

    python3 task482/generator/build.py          # the whole build
    python3 task482/generator/build.py pack     # the pack only
"""
import hashlib
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
    legacy_claims="rba_classic_claims_2024-01_2025-06.csv",
    new_claims="rba_nexus_claim_lines_2025-07_2026-10.csv",
    legacy_predets="rba_classic_predeterminations_2024-01_2025-06.csv",
    new_predets="rba_nexus_estimates_2025-06_2026-09.csv",
    legacy_accum="rba_classic_accumulators_2024-01_2025-06.csv",
    new_accum="rba_nexus_accumulators_2025-07_2026-09.csv",
    legacy_elig="rba_classic_eligibility_2025-06-30.csv",
    new_elig="rba_nexus_eligibility_2026-10-09.csv",
    crosswalk="rba_member_crosswalk_2025-07-01.csv",
    fees="ridgeline_ppo_fee_schedule_2024-2027.xlsx",
    ortho_cases="rba_ortho_case_schedule_2026-09-30.csv",
    ortho_payments="rba_ortho_payments_2024-01_2026-09.csv",
    spd="pembrook_dental_plan_spd_2025.pdf",
    costing="pembrook_benefit_costing_standard_f17.pdf",
    mandate="pembrook_board_bargaining_mandate_2026-09-28.pdf",
    schedule_c="ridgeline_aso_agreement_schedule_c.pdf",
    renewal="ridgeline_plan_review_2025_renewal_2026.pdf",
    network="ridgeline_network_access_2026q2.xlsx",
    admin_fees="rba_admin_fee_invoices_2025-01_2026-09.csv",
)
GOLD = dict(member_year="pembrook_dental_member_year_2025.csv", memo="pembrook_dental_maximum_2027.pdf",
            chart="pembrook_dental_maximum_2027.svg")


def t(k):
    return os.path.join(TARGET, NAMES[k])


def gpath(k):
    return os.path.join(GOLDEN, GOLD[k])


def pack(with_docs=True):
    for d in (TARGET, GOLDEN):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    w = W.build()
    ids = P.identities(w)
    P.write_claims(t, w, ids)
    P.write_predets(t, w, ids)
    P.write_accumulators(t, w, ids)
    P.write_eligibility(t, w, ids)
    P.write_crosswalk(t, w, ids)
    P.write_fees(t)
    P.write_ortho(t, w, ids)
    P.write_distractors(t, w)
    if with_docs:
        import docs as Dc
        import postprocess as PP
        Dc.write_all(t, w)
        for k in ("fees", "network"):
            PP.normalize_ooxml(t(k), excel=True, **PP.OWNERS[k])
        for k, stamp in Dc.STAMPS.items():
            PP.normalize_pdf(t(k), stamp, stamp)
    return dict(world=w, ids=ids)


def main():
    built = pack()
    import golden as G
    import goldfiles as GF
    res = G.solve(TARGET)
    figs = GF.write(gpath, res)
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
