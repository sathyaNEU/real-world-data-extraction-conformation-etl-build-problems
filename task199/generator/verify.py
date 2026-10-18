"""task199 independent verifier. Reads only the shipped bundle, on its own code path.

    python3 task199/generator/verify.py            # exit 0 when every check passes

It imports nothing from the generator and holds no parameter of the world: it rebuilds the register
from the three exports, the exposure from the delivery log and the population from the workbook, then
recomputes the designation, every rung and every graded figure. Each shipped format is read back
through this file's own extractor with a positive control on the same code path and a non-zero
extraction length check, so a document whose text changed cannot leave a gate green.
"""
import csv
import io
import json
import os
import re
import sys
import zipfile
from datetime import date, datetime, timedelta

TARGET = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
PANEL = ["Valledupar", "Barrancabermeja", "Aguachica", "Ocana", "Tibu", "Sardinata", "El Tarra",
         "Convencion", "Teorama", "San Calixto", "Hacari"]
WIN = (date(2026, 4, 1), date(2026, 9, 30))
BASE = (date(2024, 1, 1), date(2025, 12, 31))
PASS, FAIL = [], []


def ok(cond, label, detail=""):
    (PASS if cond else FAIL).append(label)
    if not cond:
        print("  FAIL %-60s %s" % (label, detail))


def rows(name):
    with open(os.path.join(TARGET, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def d_iso(s):
    return date(*[int(x) for x in s.split("-")])


def d_any(s):
    s = s.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return d_iso(s)
    if re.fullmatch(r"\d{2}/\d{2}/\d{4}", s):
        dd, mm, yy = s.split("/")
        return date(int(yy), int(mm), int(dd))
    raise ValueError(s)


# ------------------------------------------------- the extractors, one per format

def text_of_pdf(name):
    """Every page's text, through one extractor, so the bundle is read one way only."""
    import pdfplumber
    with pdfplumber.open(os.path.join(TARGET, name)) as pdf:
        return "\n".join((p.extract_text() or "") for p in pdf.pages)


def sheets_of_xlsx(name):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(TARGET, name), data_only=True)
    out = {}
    for ws in wb.worksheets:
        out[ws.title] = [[c for c in row] for row in ws.iter_rows(values_only=True)]
    return out


def text_of_md(name):
    with open(os.path.join(TARGET, name), encoding="utf-8") as f:
        return f.read()


def readback(fmt, name, control, absent):
    """One assertion per shipped format and per document that carries a filed sentence: the text is
    extracted, its length asserted non-zero, the positive control asserted present through the same
    parse the absence check uses, and only then the absence asserted."""
    if fmt == "pdf":
        t = text_of_pdf(name)
    elif fmt == "xlsx":
        sh = sheets_of_xlsx(name)
        t = "\n".join(" ".join("" if c is None else str(c) for c in row)
                      for rws in sh.values() for row in rws)
    elif fmt == "md":
        t = text_of_md(name)
    else:
        t = "\n".join(",".join(r.values()) for r in rows(name))
    flat = re.sub(r"\s+", " ", t).lower()
    ok(len(flat) > 200, "readback.%s.extraction_is_not_empty" % name, "%d characters" % len(flat))
    ok(control.lower() in flat, "readback.%s.positive_control" % name, control[:50])
    for a in absent:
        ok(a.lower() not in flat, "readback.%s.absent[%s]" % (name, a[:28]), a[:40])
    return flat


# ----------------------------------------------------------------- the register

def register():
    """One row per gathering-day, from the three exports, with the preliminary extract dropped and
    the 2026 day count expanded."""
    out = []
    for r in rows("rac_acciones_2024.csv"):
        out.append((r["municipio"], d_any(r["fecha_accion"]), 1, r["action_id"]))
    for r in rows("rac_acciones_2025.csv"):
        out.append((r["municipio"], d_any(r["fecha_de_accion"]), 1, r["id_accion"]))
    for r in rows("rac_acciones_2026.csv"):
        if r["extracto"] != "definitivo":
            continue
        out.append((r["municipio"], d_any(r["fecha_accion"]), int(r["dias"]), r["action_id"]))
    return out


def action_days(reg, city, lo, hi):
    n = 0
    for c, dt, days, _ in reg:
        if c != city:
            continue
        for k in range(days):
            if lo <= dt + timedelta(days=k) <= hi:
                n += 1
    return n


def main():
    print("task199 verify, reading only target/")
    files = sorted(os.listdir(TARGET))
    exts = {os.path.splitext(f)[1] for f in files}
    ok(len(files) >= 10, "gate.files", "%d" % len(files))
    ok(len(exts) >= 3, "gate.formats", ",".join(sorted(exts)))
    big = []
    for f in files:
        if f.endswith(".csv"):
            n = sum(1 for _ in open(os.path.join(TARGET, f), encoding="utf-8")) - 1
            if n >= 25000:
                big.append((f, n))
    ok(big, "gate.a_file_of_25000_rows", str(big))

    # ---- the formats read back, each with its own positive control on this code path
    prot = readback("pdf", "protocolo_designacion.pdf",
                    "se designa un municipio por semestre",
                    ["items_entregados", "items_retenidos", "envios_resena"])
    man = readback("pdf", "manual_codificacion.pdf",
                   "existe una entrada cuando ocurrio una accion",
                   ["denominador", "cobertura por municipio"])
    bol = readback("pdf", "boletin_2026T1.pdf",
                   "boletin trimestral de accion colectiva",
                   ["designa a", "mision de verificacion ira"])
    fac = readback("pdf", "facturas_resena_andina_2025.pdf",
                   "periodo de publicacion de los items",
                   ["tibu", "sardinata"])
    dic = readback("md", "diccionario_datos.md",
                   "cuenta todo lo que el servicio remitio desde ese municipio",
                   ["designacion", "tasa ajustada"])
    pan = readback("xlsx", "panel_fuentes.xlsx", "agencia andina de prensa", ["volumen mensual"])
    pob = readback("xlsx", "proyecciones_poblacion.xlsx", "proyeccion 2026", ["designado"])

    # the filed estimand's own clauses are in the protocol, once each
    for clause in ("1 de abril al 30 de septiembre de 2026",
                   "veinticuatro meses terminados el 31 de diciembre de 2025",
                   "al menos treinta acciones", "por 100.000 habitantes",
                   "extracto definitivo del 5 de noviembre de 2026"):
        ok(prot.count(clause.lower()) >= 1, "protocol.states[%s]" % clause[:34])
    ok(man.count("una concentracion, en un dia, en un lugar") == 1, "manual.unit_stated_once")
    ok("los registros del observatorio son la evidencia de esa actividad y no su medida" in prot,
       "protocol.outcome_is_the_activity_not_the_entries")

    # ---- the population, from the workbook's units sheet
    sh = sheets_of_xlsx("proyecciones_poblacion.xlsx")
    pops = {}
    for row in sh["Proyeccion 2026 unidades"][1:]:
        pops[row[0]] = int(row[2])
    ok(len(pops) >= 11, "population.sheet_read", "%d municipalities" % len(pops))
    miles = {row[0]: row[2] for row in sh["Proyeccion 2026 miles"][1:]}
    ok(all(abs(miles[c] * 1000 - pops[c]) < 1.0 for c in pops), "population.two_sheets_agree")

    # ---- the exposure, from the delivery log
    deliv = {}
    with open(os.path.join(TARGET, "envios_resena_andina.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            dt = d_iso(r["fecha_envio"])
            city = r["municipio_fecha"]
            for span, (lo, hi) in (("b", BASE), ("w", WIN)):
                if lo <= dt <= hi:
                    key = (city, span)
                    deliv[key] = deliv.get(key, 0) + int(r["items_entregados"])
    ok(all((c, "b") in deliv and (c, "w") in deliv for c in PANEL), "exposure.every_panel_city_span")

    # ---- the citations, the volume the actions themselves produce
    cits = {}
    for r in rows("citas_rac.csv"):
        dt = d_iso(r["fecha_item"])
        for span, (lo, hi) in (("b", BASE), ("w", WIN)):
            if lo <= dt <= hi:
                cits[(r["id_accion"], span)] = span
    reg = register()
    city_of = {aid: c for c, _, _, aid in reg}
    cit_n = {}
    for (aid, span) in cits:
        base_id = aid.split("-")[0:4]
        c = city_of.get(aid) or city_of.get("-".join(base_id))
        if c:
            cit_n[(c, span)] = cit_n.get((c, span), 0) + 1

    # ---- the designation
    ad = {(c, s): action_days(reg, c, *(BASE if s == "b" else WIN)) for c in PANEL for s in "bw"}
    rate = {c: ad[(c, "w")] / pops[c] * 1e5 for c in PANEL}
    rise = {c: (ad[(c, "w")] / 6.0) / (ad[(c, "b")] / 24.0) for c in PANEL}
    dec = {c: (ad[(c, "w")] / deliv[(c, "w")]) / (ad[(c, "b")] / deliv[(c, "b")]) for c in PANEL}
    cit_route = {c: ((ad[(c, "w")] / max(cit_n.get((c, "w"), 1), 1)) /
                     (ad[(c, "b")] / max(cit_n.get((c, "b"), 1), 1))) for c in PANEL}
    o_dec = sorted(PANEL, key=lambda c: -dec[c])
    o_rise = sorted(PANEL, key=lambda c: -rise[c])
    o_cit = sorted(PANEL, key=lambda c: -cit_route[c])
    ok(o_dec[0] == "Tibu", "call.designated_city", o_dec[0])
    ok(dec["Tibu"] / dec[o_dec[1]] >= 1.15, "call.decisive_margin",
       "%.3fx over %s" % (dec["Tibu"] / dec[o_dec[1]], o_dec[1]))
    ok(o_rise[0] == "Sardinata", "ladder.default_path_names_Sardinata", o_rise[0])
    ok(o_rise.index("Tibu") + 1 in (4, 5), "ladder.golden_position_on_the_default_path",
       str(o_rise.index("Tibu") + 1))
    ok(o_cit[0] == "Teorama", "ladder.citation_route_names_Teorama", o_cit[0])
    ok(abs(round(rate["Tibu"], 1) - 91.6) < 1e-9, "call.graded_rate", "%.4f" % rate["Tibu"])
    ok(ad[("Tibu", "w")] == 138, "call.window_action_days", str(ad[("Tibu", "w")]))
    for c in PANEL:
        v = rate[c]
        edge = 0.05 - abs(v - round(v, 1))
        ok(edge >= 0.03 - 1e-9, "bin.%s" % c, "%.4f edge %.4f" % (v, edge))

    # ---- the eligibility condition, and that it removes nobody who could win
    inelig = [c for c in PANEL if ad[(c, "w")] < 30]
    ok("Tibu" not in inelig, "eligibility.golden_is_eligible", str(inelig))
    ok(all(c != o_rise[0] for c in inelig), "eligibility.removes_no_default_path_leader")

    # ---- the uncleaned read lands elsewhere
    raw26 = {}
    for r in rows("rac_acciones_2026.csv"):
        dt = d_iso(r["fecha_accion"])
        if WIN[0] <= dt <= WIN[1]:
            raw26[r["municipio"]] = raw26.get(r["municipio"], 0) + 1
    o_raw = sorted(raw26, key=lambda c: -(raw26[c] / max(ad[(c, "b")], 1)))
    ok(o_raw[0] != "Tibu", "ladder.uncleaned_export_is_not_the_golden", o_raw[0])

    # ---- the asks' devices are outside the panel
    summ = rows("resumen_mensual_rac_2025.csv")
    detail = {}
    for c, dt, days, _ in reg:
        if dt.year == 2025:
            detail[(c, dt.month)] = detail.get((c, dt.month), 0) + days
    dis = {x["municipio_sede"] for x in summ
           if int(x["acciones_dia"]) != detail.get((x["municipio_sede"], int(x["mes"])), 0)}
    ok(dis and not (dis & set(PANEL)), "ask.B_device_outside_the_panel", str(sorted(dis)[:5]))
    pubdiff = 0
    with open(os.path.join(TARGET, "envios_resena_andina.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            dt = d_iso(r["fecha_envio"])
            same = "%d-%02d" % (dt.year, dt.month)
            inside = (BASE[0] <= dt <= BASE[1]) or (WIN[0] <= dt <= WIN[1])
            if r["municipio_fecha"] in PANEL and inside and r["periodo_publicacion"] != same:
                pubdiff += 1
    ok(pubdiff == 0, "ask.A_device_never_inside_the_call", "%d exceptions" % pubdiff)

    # ---- provenance and the distractors
    man_rows = rows("manifiesto_exportacion.csv")
    ok(len(man_rows) >= 10, "provenance.manifest_covers_the_bundle", str(len(man_rows)))
    meta = json.load(open(os.path.join(os.path.dirname(TARGET), "metadata.json")))
    ok(len(meta["distractor_files"]) >= 2, "provenance.distractors_declared")
    ok(not any(re.search(r"distract|answer|golden", f, re.I) for f in files),
       "provenance.no_file_name_broadcasts_the_design")

    # ---- the containers carry no toolchain signature
    for f in files:
        b = open(os.path.join(TARGET, f), "rb").read()
        if f.endswith(".pdf"):
            ok(b"ReportLab" not in b, "hygiene.no_pdf_producer_banner.%s" % f)
        if f.endswith(".xlsx"):
            ok(b"openpyxl" not in b, "hygiene.no_xlsx_writer_banner.%s" % f)
            with zipfile.ZipFile(io.BytesIO(b)) as z:
                dates = {i.date_time for i in z.infolist()}
            ok(len(dates) == 1, "hygiene.one_zip_stamp.%s" % f, str(dates))

    print("\n%d checks, %d PASS, %d FAIL" % (len(PASS) + len(FAIL), len(PASS), len(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
