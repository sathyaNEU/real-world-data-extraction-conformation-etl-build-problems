"""Builds task171's pack into target/ and the golden deliverables into golden/, writes generator/figures.json, and
cuts target.zip; two runs are byte-identical.

    python3 task171/generator/build.py          # the whole build
    python3 task171/generator/build.py pack     # the pack only
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

import common as K        # noqa: E402


def t(name):
    return os.path.join(TARGET, name)


def pack():
    import events as E
    import pack as PK
    import world as WD
    for d in (TARGET, GOLDEN):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    W = WD.simulate()
    PK.ids(W)
    T = PK.infusion_times(W)
    eps = E.adverse_events(W)
    A = E.ada(W)
    D = E.diaries(W)
    PK.efficacy(W)
    n = {}
    n[K.SITES] = K.write_csv(t(K.SITES), ["site_number", "country", "city", "time_zone", "activated", "status"], PK.site_rows(W))
    n[K.RAND] = K.write_csv(t(K.RAND), ["randomisation_number", "site_subject", "randomised_on", "stratum", "treatment"],
                            PK.rand_rows(W))
    n[K.BASE] = K.write_csv(t(K.BASE), ["site_subject", "age", "sex", "weight_kg", "modified_mayo_score",
                                        "normal_stool_frequency", "prior_advanced_therapy_failure"], PK.base_rows(W))
    n[K.DOSE] = K.write_csv(t(K.DOSE), ["site_subject", "visit", "infusion_start_local", "infusion_end_local", "planned_volume_ml",
                                        "delivered_volume_ml", "interrupted"], PK.infusion_rows(W, T), crlf=True)
    n[K.CONC] = K.write_csv(t(K.CONC), ["sample_id", "randomisation_number", "visit", "timepoint", "collected_utc",
                                        "analyte", "run_id", "result", "unit", "reportable", "comment"], PK.conc_rows(W, T))
    eff_cols = ["site_subject", "visit", "endoscopic_subscore", "stool_frequency_subscore", "rectal_bleeding_subscore",
                "modified_mayo_score", "clinical_remission", "nri_reason", "endoscopy_read"]
    n[K.EFF_LOCK] = K.write_csv(t(K.EFF_LOCK), eff_cols, PK.eff_rows(W))
    n[K.EFF_TOP] = K.write_csv(t(K.EFF_TOP), eff_cols, PK.eff_rows(W, topline=True))
    n[K.LAB] = K.write_csv(t(K.LAB), ["site_subject", "visit", "collected_utc", "test", "result", "unit", "laboratory"],
                           PK.lab_rows(W))
    n[K.ENDO] = K.write_csv(t(K.ENDO), ["site_subject", "visit", "procedure_date", "local_read", "central_reader_1",
                                        "central_reader_2", "adjudicated", "final_central"], PK.endo_rows(W))
    ada, runs = PK.ada_rows(W, A)
    n[K.ADA] = K.write_csv(t(K.ADA), ["sample_id", "randomisation_number", "collection_date", "manifest_visit", "run_id", "tier", "result",
                                      "cut_point"], ada)
    n[K.ADA_RUNS] = K.write_csv(t(K.ADA_RUNS), ["run_id", "run_date", "assay", "plate_acceptance", "reason"], runs, crlf=True)
    disp, assign = PK.devices(W)
    n[K.DEVICES] = K.write_csv(t(K.DEVICES),
                                                         ["handset_serial", "site_subject", "dispensed_on", "returned_on",
                                                          "app_version_at_dispensing"], disp)
    n[K.DIARY] = K.write_csv(t(K.DIARY), ["entry_id", "handset_serial", "diary_date", "recorded_at", "stool_frequency",
                                          "rectal_bleeding"], PK.diary_rows(W, D, assign))
    n[K.AE] = K.write_csv(t(K.AE), ["site_subject", "ae_number", "recorded_at_visit", "verbatim_term", "preferred_term",
                                    "system_organ_class", "onset_date", "end_date", "ongoing", "serious", "severity",
                                    "related"], PK.ae_rows(W, eps))
    n[K.VISITS] = K.write_csv(t(K.VISITS), ["site_subject", "visit", "visit_date"], PK.visit_rows(W))
    n[K.CONMED] = K.write_csv(t(K.CONMED),
                                                               ["site_subject", "medication", "route", "start_date",
                                                                "stop_date", "indication"], PK.conmed_rows(W))
    import docs as DOC
    import postprocess as PP
    DOC.write_charter(t(K.CHARTER))
    DOC.write_sap(t(K.SAP))
    DOC.write_ib(t(K.IB))
    DOC.write_phase1(t(K.PHASE1))
    PP.normalize_ooxml(t(K.PHASE1), "Bryan Castro", "Bryan Castro", "2024-03-11T13:20:00Z", "2024-03-18T10:05:00Z",
                       title="HV-101 PK summary", excel=True, company="Corvane Therapeutics")
    for nm, stamp in ((K.CHARTER, b"D:20260609141500-04'00'"), (K.SAP, b"D:20260402110000-04'00'"),
                      (K.IB, b"D:20260115090000-05'00'")):
        PP.normalize_pdf(t(nm), stamp, stamp)
    return W, n, eps, A, D


def gpath(name):
    return os.path.join(GOLDEN, name)


def main():
    W, n, eps, A, D = pack()
    import golden as G
    import goldfiles as GF
    import postprocess as PP
    F = G.compute(TARGET)
    GF.chart(gpath(K.CHART), F)
    GF.tables(gpath(K.TABLES), F)
    GF.memo(gpath(K.MEMO), F)
    PP.normalize_ooxml(gpath(K.TABLES), "Kathy Harvey", "Kathy Harvey", "2026-10-12T14:10:00Z", "2026-10-21T17:32:00Z",
                       title="Phase 2b induction tables", excel=True, company="Corvane Therapeutics")
    PP.normalize_docx(gpath(K.MEMO), "Kathy Harvey", "Bryan Castro", "2026-10-13T09:05:00Z", "2026-10-21T18:02:00Z", 7,
                      214, 171, title="Phase 3 induction dose", company="Corvane Therapeutics")
    json.dump(G.flat(F), open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    import writeup
    writeup.main()
    import metadata
    metadata.main()
    cut_zip()
    print("built: %d files in target/, %d in golden/" % (len(os.listdir(TARGET)), len(os.listdir(GOLDEN))))
    print(json.dumps(n))


def cut_zip():
    import hashlib
    import metadata
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for nm in sorted(os.listdir(TARGET)):
            y, mo, d = (int(x) for x in metadata.SOURCES[nm][1].split("-"))
            h = int(hashlib.md5(nm.encode()).hexdigest(), 16)
            zi = zipfile.ZipInfo(nm, date_time=(y, mo, d, 7 + h % 11, (h // 11) % 60, ((h // 660) % 30) * 2))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, nm), "rb").read())


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "pack":
        W, n, eps, A, D = pack()
        print(json.dumps(n, indent=1))
    else:
        main()
