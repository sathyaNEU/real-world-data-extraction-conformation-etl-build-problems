"""task250 architecture 4: the evidence pack, written the way the institute's systems export it.

target/ holds the files the analyst receives; metadata.json (beside target/) holds provenance. Parquet is written
from arrays, never through a data-frame library, so no schema metadata block names a library; workbooks are saved
and their packages rewritten with the saver's docProps and fixed member times; PDFs come from docs.py."""
import csv
import datetime as dt
import io
import json
import os
import shutil
import sys

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import params as P
import world as Wm
import records as Rm
import officedoc as od

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")

REL_NAMES = {"R": "respondente", "C": "cônjuge ou companheiro(a)", "F": "filho(a)", "P": "pai ou mãe",
             "O": "outro familiar", "N": "não familiar"}
CTT_REASONS = {"01": "Endereço insuficiente", "02": "Endereço inexistente", "03": "Destinatário desconhecido",
               "04": "Mudou-se", "05": "Recusado", "06": "Não reclamado", "07": "Falecido", "08": "Outro"}
OLD_CODES = [("110", "Completo (web)"), ("120", "Completo (papel)"), ("210", "Parcial (web)"),
             ("310", "Recusa (contacto)"), ("320", "Recusa (questionário devolvido em branco)"),
             ("430", "Devolvido pelos CTT: endereço inexistente ou insuficiente"),
             ("440", "Devolvido pelos CTT: outro motivo"), ("510", "Sem resposta")]
NEW_CODES = [("C-W", "Completo (web)"), ("C-P", "Completo (papel)"), ("P", "Parcial (web)"),
             ("R-C", "Recusa (contacto)"), ("R-B", "Recusa (questionário em branco)"),
             ("NE-D", "Devolvido: endereço inexistente ou insuficiente"), ("U-D", "Devolvido: outro motivo"),
             ("U", "Sem resposta")]
OLD_TO_NEW = dict(zip([c for c, _ in OLD_CODES], [c for c, _ in NEW_CODES]))


def write_parquet(path, cols, types):
    arrays, fields = [], []
    for name, typ in types:
        arrays.append(pa.array(cols[name], type=typ))
        fields.append(pa.field(name, typ))
    table = pa.Table.from_arrays(arrays, schema=pa.schema(fields))
    pq.write_table(table, path, compression="snappy", store_schema=False, write_statistics=True)


def write_csv(path, header, rows, delim=",", bom=False):
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=delim, lineterminator="\r\n" if delim == ";" else "\n")
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    data = buf.getvalue().encode("utf-8")
    if bom:
        data = b"\xef\xbb\xbf" + data
    with open(path, "wb") as fh:
        fh.write(data)


def xlsx_finish(path, title, subject, creator, last_by, created, modified, sheets):
    core = od.core_xml(title, subject, creator, last_by, created, modified)
    app = od.app_xml_excel(sheets, P.INSTITUTE_SHORT)
    od.repack(path, core, app, modified.replace(tzinfo=None))


def lisbon(t):
    return t.replace(tzinfo=dt.timezone(dt.timedelta(hours=1 if dt.datetime(2026, 3, 29, 1) <= t < dt.datetime(
        2026, 10, 25, 2) else 0)))


def relations(mem, r):
    """each member's relation to the respondent, from the household's ages and sexes"""
    out = []
    ra = mem[r][1]
    partner = None
    for i, m in enumerate(mem):
        if i != r and m[0] != mem[r][0] and abs(m[1] - ra) <= 12 and partner is None and i < 2 and r < 2:
            partner = i
    for i, m in enumerate(mem):
        if i == r:
            out.append("R")
        elif i == partner:
            out.append("C")
        elif ra - m[1] >= 17:
            out.append("F")
        elif m[1] - ra >= 17:
            out.append("P")
        else:
            out.append("O" if (i < 2 or (abs(m[1] - ra) < 30)) else "N")
    return out


def build(W=None, R=None, target=TARGET):
    if W is None:
        W = Wm.build()
    if R is None:
        R = Rm.build(W)
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    rs = Wm.stream("pack")
    rs_misc = Wm.stream("pack_misc")
    n = len(W["addr_survey"])
    occ_index = {int(a): j for j, a in enumerate(W["occ"])}
    codes, case_codes = R["codes"], R["case_codes"]
    surveys = [s[0] for s in P.SURVEYS]
    # ------------------------------------------------------------ returns, in receipt order across the programme
    rets = []     # (received datetime local, case index, mode, respondent index, which: kept|second)
    for a in range(n):
        j = occ_index.get(a)
        if j is None or not W["resp"][j]:
            continue
        letter = W["addr_letter"][a]
        md = int(W["mode"][j])
        day = int(W["day"][j])
        if md == 0:
            hh = int(rs.choice([8, 10, 12, 13, 15, 18, 19, 20, 21, 22, 23], p=[.04, .06, .08, .07, .06, .1, .14, .16, .14, .1, .05]))
            t = dt.datetime.combine(letter + dt.timedelta(days=day), dt.time(hh, int(rs.integers(60)), int(rs.integers(60))))
        else:
            t = dt.datetime.combine(letter + dt.timedelta(days=day), dt.time(10, 0, 0))
        rets.append((t, a, md, int(W["respondent"][j]), "kept"))
        sec = R["second"][a]
        if sec is not None:
            md2, d2, r2 = sec
            if md2 == 0:
                t2 = dt.datetime.combine(letter + dt.timedelta(days=d2), dt.time(int(rs.integers(9, 23)), int(rs.integers(60)), int(rs.integers(60))))
            else:
                t2 = dt.datetime.combine(letter + dt.timedelta(days=d2), dt.time(10, 0, 0))
            if t2 <= t:
                t2 = t + dt.timedelta(days=1)
            rets.append((t2, a, md2, r2, "second"))
    rets.sort(key=lambda x: (x[0], x[1], x[2]))
    seq = 104217
    ret_id = {}
    for t, a, md, r, which in rets:
        seq += 1 + int(rs.integers(0, 3))        # numbers taken by partial and spoilt submissions in between
        ret_id[(a, which)] = "R%07d" % seq
    # paper scanning batches
    batch_of = {}
    # ------------------------------------------------------------ core module, web and paper
    web = {k: [] for k in ["return_id", "case_id", "survey", "submitted_utc", "access_code", "n_adults_16plus",
                           "n_persons", "resp_sex", "resp_dob", "sel_confirm", "resp_activity", "resp_education",
                           "device"]}
    paper_rows = []
    mem_cols = {k: [] for k in ["return_id", "linha", "sexo", "ano_nascimento", "relacao"]}
    children_b = {}
    for t, a, md, r, which in rets:
        j = occ_index[a]
        mem = W["hh_members"][j]
        k = len(mem)
        if a not in children_b:
            nch = int(W["hh_children"][j]) if k > 1 or mem[0][1] < 60 else 0
            children_b[a] = [(bool(rs_misc.random() < 0.49), int(rs_misc.integers(2011, 2026))) for _ in range(nch)]
        kids = children_b[a]
        f, ag, bm, bd, by = mem[r]
        dob = dt.date(by, bm, bd)
        conf = int(W["confirm"][j]) if which == "kept" else (1 if rs_misc.random() < 0.93 else 2)
        act = ("retired" if ag >= 66 and rs_misc.random() < 0.9 else
               str(rs_misc.choice(["employed", "unemployed", "student", "home", "other"],
                                  p=[0.52, 0.08, 0.30, 0.03, 0.07] if ag < 26 else [0.72, 0.07, 0.01, 0.09, 0.11])))
        edu = str(rs_misc.choice(["basic", "secondary", "tertiary"],
                                 p=[0.55, 0.27, 0.18] if ag >= 55 else [0.22, 0.42, 0.36]))
        dob_missing = rs_misc.random() < (0.008 if md == 0 else 0.014)
        rid = ret_id[(a, which)]
        if md == 0:
            web["return_id"].append(rid)
            web["case_id"].append(R["case_id"][a])
            web["survey"].append(surveys[W["addr_survey"][a]])
            web["submitted_utc"].append(lisbon(t).astimezone(dt.timezone.utc))
            cl = case_codes[a]
            web["access_code"].append(codes[cl[-1]][1] if len(cl) > 1 else codes[cl[0]][1])
            web["n_adults_16plus"].append(k)
            web["n_persons"].append(k + len(kids))
            web["resp_sex"].append("F" if f else "M")
            web["resp_dob"].append(None if dob_missing else dob)
            web["sel_confirm"].append("yes" if conf == 1 else "no_continue")
            web["resp_activity"].append(act)
            web["resp_education"].append(edu)
            web["device"].append(str(rs_misc.choice(["mobile", "desktop", "tablet"], p=[0.52, 0.41, 0.07])))
        else:
            key = (W["addr_survey"][a], (t.date() - dt.date(2026, 1, 1)).days // 3)
            if key not in batch_of:
                batch_of[key] = "L26-%04d" % (1000 + len(batch_of) * 7 + int(rs_misc.integers(0, 5)))
            dobtxt = "" if dob_missing else dob.strftime("%d/%m/%Y")
            ptxt = {1: "1", 2: "2", 0: ""}[conf]
            sit = {"employed": "1", "unemployed": "2", "student": "3", "retired": "4", "home": "5", "other": "6"}[act]
            esc = {"basic": "1", "secondary": "2", "tertiary": "3"}[edu]
            paper_rows.append([rid, R["case_id"][a], surveys[W["addr_survey"][a]], t.strftime("%d/%m/%Y"),
                               batch_of[key], str(k), str(k + len(kids)), "2" if f else "1", dobtxt, ptxt, sit, esc])
        rel = relations(mem, r)
        order = [r] + [i for i in range(k) if i != r]
        for line, i in enumerate(order, start=1):
            m = mem[i]
            mem_cols["return_id"].append(rid)
            mem_cols["linha"].append(line)
            mem_cols["sexo"].append("F" if m[0] else "M")
            yb = m[4]
            if md == 1 and i == r and rs_misc.random() < 0.004:
                yb = yb + int(rs_misc.choice([-1, 1]))        # a year misread at scanning
            mem_cols["ano_nascimento"].append(yb)
            mem_cols["relacao"].append(rel[i])
        for c_i, (cf, cy) in enumerate(kids):
            mem_cols["return_id"].append(rid)
            mem_cols["linha"].append(k + c_i + 1)
            mem_cols["sexo"].append("F" if cf else "M")
            mem_cols["ano_nascimento"].append(cy)
            mem_cols["relacao"].append("F" if mem[r][1] >= 30 else "O")
    write_parquet(os.path.join(target, "core_module_web_2026.parquet"), web, [
        ("return_id", pa.string()), ("case_id", pa.string()), ("survey", pa.string()),
        ("submitted_utc", pa.timestamp("s", tz="UTC")), ("access_code", pa.string()),
        ("n_adults_16plus", pa.int8()), ("n_persons", pa.int8()), ("resp_sex", pa.string()),
        ("resp_dob", pa.date32()), ("sel_confirm", pa.string()), ("resp_activity", pa.string()),
        ("resp_education", pa.string()), ("device", pa.string())])
    write_csv(os.path.join(target, "core_module_paper_2026.csv"),
              ["id_questionario", "id_caso", "inquerito", "data_rececao", "lote", "n_pessoas_16mais", "n_pessoas",
               "sexo", "data_nascimento", "p0_pessoa_selecionada", "situacao", "escolaridade"],
              paper_rows, delim=";", bom=True)
    write_parquet(os.path.join(target, "household_members_2026.parquet"), mem_cols, [
        ("return_id", pa.string()), ("linha", pa.int8()), ("sexo", pa.string()), ("ano_nascimento", pa.int16()),
        ("relacao", pa.string())])
    # ------------------------------------------------------------ case register (case management system)
    close = {}
    for si, s in enumerate(P.SURVEYS):
        close[si] = s[3] + dt.timedelta(days=P.CLOSE_DAYS)
    keyed_ne = {}
    keyed_other = {}
    for a, mnum, got, reason in R["returns_post"]:
        si = int(W["addr_survey"][a])
        old_system = si < 3 or (si == 3 and got < P.SYSTEM_UPGRADE)
        if si == 3 and W["addr_release"][a] == 1:
            old_system = False
        if old_system and got <= close[si]:
            if reason in ("01", "02"):
                keyed_ne[a] = min(keyed_ne.get(a, got), got)
            else:
                keyed_other[a] = min(keyed_other.get(a, got), got)
    cr = {k: [] for k in ["case_id", "survey", "release", "address_id", "region", "municipality",
                          "first_letter", "reminder_sent", "letter3_sent", "disposition", "disposition_date",
                          "kept_return_id", "returns_received"]}
    kind = R["kind"]
    for a in range(n):
        si = int(W["addr_survey"][a])
        letter = W["addr_letter"][a]
        sent = R["mailings"][a]
        new_list = si >= 3
        k = kind[a]
        j = occ_index.get(a)
        if k in ("complete_web", "complete_paper"):
            code = "110" if k == "complete_web" else "120"
            ddate = letter + dt.timedelta(days=R["kept_day"][a])
            kept = ret_id[(a, "kept")]
            nret = 2 if R["second"][a] is not None else 1
        elif k == "partial":
            code, ddate, kept, nret = "210", close[si], None, 0
        elif k == "refusal_contact":
            code, ddate, kept, nret = "310", letter + dt.timedelta(days=int(rs_misc.integers(2, 30))), None, 0
        elif k == "refusal_blank":
            code, ddate, kept, nret = "320", letter + dt.timedelta(days=int(rs_misc.integers(26, 50))), None, 0
        elif a in keyed_ne:
            code, ddate, kept, nret = "430", keyed_ne[a], None, 0
        elif a in keyed_other:
            code, ddate, kept, nret = "440", keyed_other[a], None, 0
        else:
            code, ddate, kept, nret = "510", close[si], None, 0
        if new_list:
            code = OLD_TO_NEW[code]
        cr["case_id"].append(R["case_id"][a])
        cr["survey"].append(surveys[si])
        cr["release"].append("reserva" if W["addr_release"][a] == 1 else "principal")
        cr["address_id"].append(R["address_id"][a])
        cr["region"].append(W["region_codes"][W["addr_region"][a]])
        cr["municipality"].append(W["addr_mun"][a])
        cr["first_letter"].append(letter)
        cr["reminder_sent"].append(letter + dt.timedelta(days=P.REMINDER_DAYS) if 2 in sent else None)
        cr["letter3_sent"].append(letter + dt.timedelta(days=P.PAPER_MAILING_DAYS) if 3 in sent else None)
        cr["disposition"].append(code)
        cr["disposition_date"].append(ddate)
        cr["kept_return_id"].append(kept)
        cr["returns_received"].append(nret)
    order = np.argsort(np.array(cr["case_id"]))
    cr = {k: [v[i] for i in order] for k, v in cr.items()}
    write_parquet(os.path.join(target, "case_register_2026.parquet"), cr, [
        ("case_id", pa.string()), ("survey", pa.string()), ("release", pa.string()), ("address_id", pa.string()),
        ("region", pa.string()), ("municipality", pa.string()), ("first_letter", pa.date32()),
        ("reminder_sent", pa.date32()), ("letter3_sent", pa.date32()), ("disposition", pa.string()),
        ("disposition_date", pa.date32()), ("kept_return_id", pa.string()), ("returns_received", pa.int8())])
    # ------------------------------------------------------------ access codes
    rows = []
    for ci, (a, c, iss, why) in enumerate(codes):
        rows.append([R["case_id"][a], c[:4] + "-" + c[4:], iss.isoformat(), "inicial" if why == "initial" else "substituicao"])
    rows.sort(key=lambda r: (r[0], r[2]))
    write_csv(os.path.join(target, "access_codes_2026.csv"), ["id_caso", "codigo_acesso", "emitido", "motivo"], rows)
    # ------------------------------------------------------------ web sessions
    ws = {k: [] for k in ["session_id", "access_code", "started_utc", "last_activity_utc", "last_page_answered",
                          "submitted", "client"]}
    sess = sorted(R["sessions"], key=lambda s: (s[1], str(s[0])))
    used = set()
    for ci, st, en, page, sub in sess:
        if isinstance(ci, tuple):
            c = ci[2]
        else:
            c = codes[ci][1]
        while True:
            sid = "%012x" % int(rs_misc.integers(0, 2 ** 47))
            if sid not in used:
                used.add(sid)
                break
        ws["session_id"].append(sid)
        ws["access_code"].append(c)
        ws["started_utc"].append(st.replace(tzinfo=dt.timezone.utc))
        ws["last_activity_utc"].append(en.replace(tzinfo=dt.timezone.utc))
        ws["last_page_answered"].append(page)
        ws["submitted"].append(bool(sub))
        ws["client"].append(str(rs_misc.choice(["mobile", "desktop", "tablet"], p=[0.52, 0.41, 0.07])))
    write_parquet(os.path.join(target, "web_sessions_2026.parquet"), ws, [
        ("session_id", pa.string()), ("access_code", pa.string()), ("started_utc", pa.timestamp("s", tz="UTC")),
        ("last_activity_utc", pa.timestamp("s", tz="UTC")), ("last_page_answered", pa.int8()),
        ("submitted", pa.bool_()), ("client", pa.string())])
    # ------------------------------------------------------------ postal returns register (the post room)
    rows = []
    clerks = ["CV", "RT", "SM", "HB"]
    for a, mnum, got, reason in sorted(R["returns_post"], key=lambda x: (x[2], x[0], x[1])):
        reg_day = got + dt.timedelta(days=int(rs_misc.choice([0, 0, 1, 1, 2, 3])))
        if reg_day.weekday() >= 5:
            reg_day = reg_day + dt.timedelta(days=7 - reg_day.weekday())
        rows.append([reg_day.strftime("%d-%m-%Y"), R["case_id"][a] + str(mnum), reason, CTT_REASONS[reason],
                     clerks[int(rs_misc.integers(len(clerks)))]])
    write_csv(os.path.join(target, "postal_returns_register_2026.csv"),
              ["data_registo", "codigo_barras", "motivo", "motivo_descricao", "registado_por"], rows, delim=";", bom=True)
    # ------------------------------------------------------------ address frame extract
    af = {k: [] for k in ["address_id", "region", "municipality", "parish", "building_type", "use_class",
                          "frame_version"]}
    use_p = {"occupied": (["residencial", "misto"], [0.972, 0.028]),
             "vacant": (["residencial", "misto"], [0.985, 0.015]),
             "nonresidential": (["não residencial", "misto", "residencial"], [0.70, 0.10, 0.20]),
             "communal": (["alojamento coletivo", "residencial"], [0.86, 0.14]),
             "nonexistent": (["residencial", "não residencial"], [0.90, 0.10])}
    btype = {"residencial": (["moradia", "apartamento"], [0.46, 0.54]), "misto": (["edifício misto"], [1.0]),
             "não residencial": (["comércio ou serviços", "indústria", "outro"], [0.7, 0.2, 0.1]),
             "alojamento coletivo": (["lar", "residência de estudantes", "instituição religiosa", "outro"],
                                     [0.55, 0.25, 0.1, 0.1])}
    W["frame_use"] = []
    for a in range(n):
        stt = W["status_names"][W["addr_status"][a]]
        uc, pp = use_p[stt]
        use = str(rs_misc.choice(uc, p=pp))
        W["frame_use"].append(use)
        bt, bp = btype[use]
        af["address_id"].append(R["address_id"][a])
        af["region"].append(W["region_codes"][W["addr_region"][a]])
        af["municipality"].append(W["addr_mun"][a])
        af["parish"].append(W["addr_mun"][a] + "%02d" % int(rs_misc.integers(1, 30)))
        af["building_type"].append(str(rs_misc.choice(bt, p=bp)))
        af["use_class"].append(use)
        af["frame_version"].append("2025-09")
    order = np.argsort(np.array(af["address_id"]))
    af = {k: [v[i] for i in order] for k, v in af.items()}
    write_parquet(os.path.join(target, "address_frame_extract_2025.parquet"), af, [
        (k, pa.string()) for k in ["address_id", "region", "municipality", "parish", "building_type", "use_class",
                                   "frame_version"]])
    # ------------------------------------------------------------ helpdesk contacts (distractor)
    rows = []
    cats = {"codigo_acesso": "Código de acesso", "recusa": "Não quer participar", "quem_responde":
            "Dúvida sobre quem deve responder", "pedido_papel": "Pedido de questionário em papel",
            "problema_tecnico": "Problema técnico no questionário online", "outro": "Outro assunto"}
    for i, (a, d, cat) in enumerate(sorted(R["contacts"], key=lambda x: (x[1], x[0], x[2]))):
        ch = str(rs_misc.choice(["telefone", "email", "formulário"], p=[0.58, 0.29, 0.13]))
        rows.append(["HD26-%05d" % (i + 1 + int(i * 0.07)), d.isoformat(), ch,
                     R["case_id"][a] if rs_misc.random() < 0.83 else "", surveys[W["addr_survey"][a]],
                     cats[cat], "sim" if rs_misc.random() < 0.94 else "não"])
    write_csv(os.path.join(target, "helpdesk_contacts_2026.csv"),
              ["id_contacto", "data", "canal", "id_caso", "inquerito", "assunto", "resolvido"], rows)
    # ------------------------------------------------------------ calibration totals (distractor)
    rows = []
    pop_region = {"NOR": 3_093_000, "CEN": 1_627_000, "LVT": 3_684_000, "ALE": 466_000, "ALG": 482_000,
                  "ACO": 238_000, "MAD": 256_000}
    groups = [("16-24", 0.118), ("25-34", 0.128), ("35-44", 0.155), ("45-54", 0.171), ("55-64", 0.163),
              ("65-74", 0.140), ("75+", 0.125)]
    for rc, tot in pop_region.items():
        adults = tot * 0.862
        for g, sh in groups:
            fem = 0.508 if g in ("16-24", "25-34") else (0.53 if g in ("35-44", "45-54", "55-64") else 0.575)
            jitter = 1 + (rs_misc.random() - 0.5) * 0.03
            rows.append([rc, "M", g, int(round(adults * sh * (1 - fem) * jitter / 10.0) * 10)])
            rows.append([rc, "F", g, int(round(adults * sh * fem * jitter / 10.0) * 10 + 10 * int(rs_misc.integers(0, 9)))])
    write_csv(os.path.join(target, "population_estimates_2025.csv"), ["regiao", "sexo", "grupo_etario", "residentes"], rows)
    # ------------------------------------------------------------ fieldwork calendar (workbook)
    wb = Workbook()
    ws1 = wb.active
    ws1.title = "Calendário 2026"
    head = ["Inquérito", "Designação", "Designation (EN)", "Amostra (endereços)", "1.ª carta", "Postal de lembrete",
            "3.ª carta com questionário", "Encerramento", "Reserva: envio", "Reserva: endereços"]
    ws1.append(head)
    for si, s in enumerate(P.SURVEYS):
        code, en, pt, letter, reserve, n_main, base, prof = s
        ws1.append([code, pt, en, n_main, letter, letter + dt.timedelta(days=P.REMINDER_DAYS),
                    letter + dt.timedelta(days=P.PAPER_MAILING_DAYS), letter + dt.timedelta(days=P.CLOSE_DAYS),
                    reserve[0] if reserve else None, reserve[1] if reserve else None])
    for c in ws1[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE5F0")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for row in ws1.iter_rows(min_row=2):
        for c in row:
            if isinstance(c.value, dt.date):
                c.number_format = "dd/mm/yyyy"
            elif isinstance(c.value, int):
                c.number_format = "#,##0"
    widths = [10, 34, 30, 12, 11, 12, 14, 12, 12, 11]
    for i, w in enumerate(widths, start=1):
        ws1.column_dimensions[get_column_letter(i)].width = w
    ws1.freeze_panes = "B2"
    ws1["A9"] = ("A reserva é enviada às moradas de reposição quando a amostra principal fica aquém do previsto; "
                 "cada morada da reserva recebe a sua 1.ª carta na data de envio da reserva.")
    ws1["A10"] = "Encerramento: último dia em que se aceitam respostas web; os questionários em papel recebidos até 7 dias depois são digitalizados."
    path = os.path.join(target, "fieldwork_calendar_2026.xlsx")
    wb.save(path)
    xlsx_finish(path, "Calendário do trabalho de campo 2026", "Programa de Inquéritos às Famílias",
                "Ismael Loureiro", "Ismael Loureiro",
                dt.datetime(2025, 11, 18, 10, 12, tzinfo=dt.timezone.utc),
                dt.datetime(2026, 7, 29, 15, 47, tzinfo=dt.timezone(dt.timedelta(hours=1))), ["Calendário 2026"])
    # ------------------------------------------------------------ disposition code lists (workbook)
    wb = Workbook()
    a1 = wb.active
    a1.title = "Lista até 26-07-2026"
    a1.append(["Código", "Descrição", "Grupo"])
    grp = {"110": "Completo", "120": "Completo", "210": "Parcial", "310": "Recusa", "320": "Recusa",
           "430": "Devolvido", "440": "Devolvido", "510": "Sem resposta"}
    for c, d in OLD_CODES:
        a1.append([c, d, grp[c]])
    a2 = wb.create_sheet("Lista desde 27-07-2026")
    a2.append(["Código", "Descrição", "Grupo"])
    for (c, d), (oc, _) in zip(NEW_CODES, OLD_CODES):
        a2.append([c, d, grp[oc]])
    a3 = wb.create_sheet("Correspondência")
    a3.append(["Código antigo", "Código novo"])
    for c, _ in OLD_CODES:
        a3.append([c, OLD_TO_NEW[c]])
    a3.append([])
    a3.append(["Os casos abertos em 27-07-2026 foram migrados com o código novo correspondente."])
    for wsx in (a1, a2, a3):
        for c in wsx[1]:
            c.font = Font(bold=True)
        wsx.column_dimensions["A"].width = 14
        wsx.column_dimensions["B"].width = 58
        wsx.column_dimensions["C"].width = 14
    path = os.path.join(target, "disposition_codes_2026.xlsx")
    wb.save(path)
    xlsx_finish(path, "Códigos de situação final dos casos", "Sistema de gestão de casos",
                "Madalena Nunes", "Madalena Nunes",
                dt.datetime(2024, 2, 6, 9, 30, tzinfo=dt.timezone.utc),
                dt.datetime(2026, 7, 24, 17, 5, tzinfo=dt.timezone(dt.timedelta(hours=1))),
                ["Lista até 26-07-2026", "Lista desde 27-07-2026", "Correspondência"])
    # ------------------------------------------------------------ documents
    import docs
    docs.write_all(target)
    # ------------------------------------------------------------ file times
    stamp = dt.datetime(2027, 1, 15, 9, 41).timestamp()
    for fn in os.listdir(target):
        os.utime(os.path.join(target, fn), (stamp, stamp))
    return W, R


if __name__ == "__main__":
    import time
    t = time.time()
    build()
    print("pack written to", TARGET, "%.1fs" % (time.time() - t))
