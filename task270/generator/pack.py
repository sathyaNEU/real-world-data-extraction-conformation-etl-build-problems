"""Write task270's evidence pack into a folder: every data file, the schedules workbook and the documents."""
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import common as K
import docs as DC
import records as R
import side2025 as S25
import world as WD


def write_schedules(path, rc):
    wb = Workbook()
    ws = wb.active
    ws.title = "Resumo"
    head = Font(bold=True, color="FFFFFF")
    fill = PatternFill("solid", fgColor="1D3557")
    ws.append(["Gota Viva, campanha de televisão para jovens dadores, abril de 2027"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["%s, rascunho para decisão da Comissão Executiva, %s" % (K.AGENCY, K.SCHEDULES_DATE.strftime("%d/%m/%Y"))])
    ws.append([])
    ws.append(["Esquema", "Descrição", "Spots", "Custo (EUR)"])
    for c in ws[4]:
        c.font, c.fill = head, fill
    for s in K.SCHED:
        lines = rc.schedule_lines(s)
        ws.append([s, K.SCHED_NAME[s], len(lines), sum(x[-1] for x in lines)])
    ws.append([])
    ws.append(["Preços das tabelas do 2.º trimestre de 2027, filme de 30 segundos, sem descontos de volume."])
    for col, wdt in zip("ABCD", (10, 62, 9, 14)):
        ws.column_dimensions[col].width = wdt
    for row in ws.iter_rows(min_row=5, max_row=7):
        row[3].number_format = "#,##0"
    for s in K.SCHED:
        sh = wb.create_sheet("Esquema %s" % s)
        sh.append(["Semana", "Data", "Dia", "Canal", "Programa ou janela", "Intervalo no programa", "Colocação",
                   "Duração (s)", "Preço (EUR)"])
        for c in sh[1]:
            c.font, c.fill = head, fill
            c.alignment = Alignment(wrap_text=True, vertical="top")
        for line in rc.schedule_lines(s):
            sh.append(line)
        n = sh.max_row
        sh.append(["Total", None, None, None, None, None, None, None, "=SUM(I2:I%d)" % n])
        sh.cell(row=n + 1, column=1).font = Font(bold=True)
        for col, wdt in enumerate((8, 11, 14, 10, 34, 11, 24, 10, 12), start=1):
            sh.column_dimensions[get_column_letter(col)].width = wdt
        for row in sh.iter_rows(min_row=2, max_row=n + 1):
            row[8].number_format = "#,##0"
        sh.freeze_panes = "A2"
    wb.save(path)


def build_pack(out, seed=K.SEED, world=None):
    os.makedirs(out, exist_ok=True)
    w = world or WD.World(seed)
    rc = R.Records(w)
    p = lambda k: os.path.join(out, K.FILES[k])
    n = {}
    for key, fn in (("viewing", rc.viewing_rows), ("panel", rc.panel_rows), ("asrun", rc.asrun_rows),
                    ("bookings", rc.booking_rows),
                    ("epg", rc.epg_rows), ("channels", rc.channel_rows), ("universe", rc.universe_rows),
                    ("ratings", rc.ratings_rows), ("digital", rc.digital_rows), ("donors", rc.donor_rows)):
        head, rows = fn()
        R.write_csv(p(key), head, rows)
        n[key] = len(rows)
    write_schedules(p("schedules"), rc)
    DC.write_brief(p("brief"))
    DC.write_method(p("method"), len(w.age), len(set(w.hh.tolist())))
    DC.write_rates(p("rates"), w.rate, w.ros_rate, w.prog_window)
    DC.write_dictionary(p("dictionary"))
    bk = S25.Bookings(seed)
    head, rows = bk.table()
    R.write_csv(p("portal"), head, rows)
    n["portal"] = len(rows)
    DC.write_notes_2025(p("portal_notes"))
    DC.write_report_2025(p("report2025"))
    return w, rc, n
