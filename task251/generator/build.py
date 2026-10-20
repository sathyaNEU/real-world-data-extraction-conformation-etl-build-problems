"""Write the pack: every file under target/, from the seeded world.   B.run(target) -> the world and the records"""
import os

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

import docs
import params as P
import postprocess
import records as RC
import sim

SEED = P.SEED
FILES = dict(
    procedure="POCT-GLU-02_glucometri_rev3.pdf",
    export="GlyLink_risultati_2026-2027.csv",
    pairs="GlyLink_abbinamenti_laboratorio_2026-2027.xlsx",
    plan="piano_abbinamenti_glucometri_2026-2027.xlsx",
    register="anagrafica_glucometri.xlsx",
    note="nota_laboratorio_cambio_analizzatore_glicemia.pdf",
    service="Corvenza_rapporto_taratura_gennaio_2027.pdf",
    mail="Corvenza_visita_taratura_gennaio_2028.eml",
    dictionary="dizionario_dati_POCT.md",
    strips="strisce_consegnate_reparti_2027.xlsx",
    veq="VEQ_glicemia_laboratorio_2027.xlsx",
)
PACK = list(FILES)
DISTRACTORS = ["strips", "veq"]
CONTEXT = ["mail"]
STAMP_PDF = {"procedure": "2026-04-14T16:02:00", "note": "2027-09-07T11:37:00", "service": "2027-01-22T17:48:00"}


def _sheets(path, sheets):
    """sheets: [(title, DataFrame, widths, {col: number_format})]"""
    wb = Workbook()
    for k, (title, df, widths, fmts) in enumerate(sheets):
        ws = wb.active if k == 0 else wb.create_sheet()
        ws.title = title
        ws.append(list(df.columns))
        for r in df.itertuples(index=False):
            ws.append([None if (v is None or (isinstance(v, float) and v != v)) else v for v in r])
        for row in ws.iter_rows(min_row=2):
            for j, fmt in fmts.items():
                row[j].number_format = fmt
        for j, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(j)].width = w
        for c in ws[1]:
            c.font = Font(bold=True)
        ws.freeze_panes = "A2"
    wb.save(path)


def world():
    W = sim.world(SEED)
    R = RC.build(W, SEED)
    return W, R


def run(target):
    os.makedirs(target, exist_ok=True)
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    W, R = world()
    R["dms"].to_csv(F["export"], sep=";", index=False, encoding="utf-8")
    pr = R["pairs"].copy()
    _sheets(F["pairs"], [("Abbinamenti", pr, [13, 12, 17, 17, 15, 17, 18, 10, 9], {})])
    _sheets(F["plan"], [("Piano", R["plan"], [12, 34, 12, 12], {2: "dd/mm/yyyy", 3: "dd/mm/yyyy"}),
                        ("Festività", R["holidays"], [12, 26], {0: "dd/mm/yyyy"})])
    _sheets(F["register"], [("Glucometri", R["register"], [12, 12, 14, 24, 9, 12, 14, 8],
                                         {5: "dd/mm/yyyy", 6: "dd/mm/yyyy"}),
                            ("Storico ubicazioni", R["history"], [12, 10, 9, 12, 12], {3: "dd/mm/yyyy",
                                                                                       4: "dd/mm/yyyy"})])
    _sheets(F["strips"], [("Consegne 2027", R["strips"], [24, 9, 10, 12, 22], {})])
    _sheets(F["veq"], [("VEQ 2027", R["veq"], [9, 12, 10, 14, 22, 16, 9], {1: "dd/mm/yyyy", 4: "0.0", 6: "0.00"})])
    docs.procedure(F["procedure"], FILES)
    docs.lab_note(F["note"], FILES)
    docs.service_report(F["service"], FILES, R["service"])
    docs.vendor_mail(F["mail"], FILES)
    docs.dictionary(F["dictionary"], FILES)
    postprocess.scrub(F["procedure"], "Microsoft Word 2019", STAMP_PDF["procedure"])
    postprocess.scrub(F["note"], "Microsoft Word 2019", STAMP_PDF["note"])
    postprocess.scrub(F["service"], "Microsoft Word 2016", STAMP_PDF["service"])
    for k in ("pairs", "plan", "register", "strips", "veq"):
        postprocess.scrub(F[k], P.ORG, "2028-01-03")
        postprocess.finish_office(F[k], "2028-01-03T10:05:00Z", "2028-01-03T10:11:00Z", P.ORG)
    return {"W": W, "R": R}
