"""The register's own extracts: the press monitor's item log, the two report files, the gazetteer,
the import log, the route control totals, the crawler configuration and the extract manifest."""
import csv
import datetime as dt
import json
import os
import random

import sim
import world as W

# the press monitor stamps every item with its collection server's UTC clock; the partner portal
# stamps deliveries in UTC; the public line stamps in the association's own local clock.
REJECT = [("fora_do_ambito", 44), ("sem_acao_coletiva", 27), ("duplicado_de_item", 9),
          ("desporto_ou_espetaculo", 11), ("texto_insuficiente", 9)]
RELOAD_ARRIVED = dt.date(2026, 9, 14)


def write_csv(path, head, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(head)
        w.writerows(rows)
    return len(rows)


def local_offset(district, day):
    """Hours the local clock of a district is ahead of UTC on a local calendar day. Summer time ends
    on 25 October 2026; the Azores run an hour behind the mainland and Madeira all year."""
    summer = day < W.DST_BACK
    pair = W.OFFSET_AZORES if district == W.AZORES_DISTRICT else W.OFFSET_MAINLAND
    return pair[0] if summer else pair[1]


WORK_HOURS = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
WORK_WEIGHTS = [9, 14, 15, 12, 7, 6, 10, 11, 9, 7, 5, 3]


def work_moment(day, rng):
    """A moment inside a partner organisation's own working day."""
    return dt.datetime.combine(day, dt.time(rng.choices(WORK_HOURS, weights=WORK_WEIGHTS)[0],
                                            rng.randrange(0, 60)))


def snap_working(local_moment, rng):
    """A partner organisation delivers through the portal in its own working hours, so a report
    whose turn comes outside them waits for the next working day."""
    for _ in range(4):
        if local_moment.weekday() >= 5 and rng.random() < 0.74:
            local_moment = work_moment(local_moment.date() + dt.timedelta(days=1), rng)
            continue
        if local_moment.hour < 8:
            return work_moment(local_moment.date(), rng)
        if local_moment.hour >= 20:
            local_moment = work_moment(local_moment.date() + dt.timedelta(days=1), rng)
            continue
        return local_moment
    return local_moment


def stamp(district, day_off, start_h, start_m, lag_min):
    """The action's start in the local clock of its place, and the report's moment in UTC."""
    start = dt.datetime.combine(sim.d(day_off), dt.time(start_h, start_m))
    start_utc = start - dt.timedelta(hours=local_offset(district, start.date()))
    recv_utc = start_utc + dt.timedelta(minutes=lag_min)
    return start, recv_utc


def place_text(loc, rng):
    if loc["former"] and rng.random() < 0.45:
        return loc["former"]
    return loc["name"]


def intake_window(local_moment, rng):
    """The monitor's collection and the public line both run on the association's own intake hours,
    06:00 to 23:00: whatever lands outside them is written at the next intake."""
    if local_moment.hour >= W.INTAKE_TO:
        local_moment = dt.datetime.combine(local_moment.date() + dt.timedelta(days=1),
                                           dt.time(W.INTAKE_FROM, rng.randrange(0, 56)))
    elif local_moment.hour < W.INTAKE_FROM:
        local_moment = dt.datetime.combine(local_moment.date(),
                                           dt.time(W.INTAKE_FROM, rng.randrange(0, 56)))
    return local_moment


def build_reports(reps, locs, rng):
    """Add the dates, stamps and place text every report file needs."""
    cap = dt.datetime.combine(W.EXTRACT, dt.time(20, 30))   # the record was pulled that evening
    for r in reps:
        a = r["action"]
        dist = a["district"]
        start, recv_utc = stamp(dist, a["day"], r["start_h"], r["start_m"], r["lag_min"])
        if r["route"] == "PAR":
            own = recv_utc + dt.timedelta(hours=local_offset(dist, recv_utc.date()))
            own = snap_working(own, rng)
            recv_utc = own - dt.timedelta(hours=local_offset(dist, own.date()))
        recv_lisbon = recv_utc + dt.timedelta(hours=local_offset("Lisboa", recv_utc.date()))
        if r["route"] != "PAR":
            own = intake_window(recv_lisbon, rng)
            if own != recv_lisbon:
                recv_lisbon = own
                recv_utc = own - dt.timedelta(hours=local_offset("Lisboa", own.date()))
        if recv_utc > cap:                                 # a report that had not arrived is not in it
            recv_utc = max(start - dt.timedelta(hours=local_offset(dist, start.date()))
                           + dt.timedelta(minutes=12),
                           cap - dt.timedelta(minutes=r["lag_min"] % 97))
            recv_lisbon = recv_utc + dt.timedelta(hours=local_offset("Lisboa", recv_utc.date()))
        r["start"] = start
        r["recv_lisbon"] = recv_lisbon
        r["recv_local"] = recv_lisbon
        r["recv_utc"] = recv_utc
        r["place"] = place_text(a["loc"], rng)
    return reps


def exceptions(rng, n_imp=151, n_par=63, n_lin=94):
    """Reports the association received and could not place: they never became actions."""
    bogus = ["Zona Industrial (sem localidade)", "A25 km 42", "Barragem do Vale Grande",
             "Terminal Portuario Norte", "Estrada Nacional 125, Pocinho", "Area de Servico do Pinhal",
             "Fronteira de Vilar Formoso", "Nao indicado", "Centro Coordenador (indefinido)",
             "Parque Eolico da Cumeada"]
    reasons = ["localidade_nao_encontrada", "texto_insuficiente", "fora_do_territorio"]
    out = []
    for route, n, base in (("IMP", n_imp, 900000), ("PAR", n_par, 900000), ("LIN", n_lin, 900000)):
        for i in range(n):
            off = rng.randrange(0, (W.PERIOD_TO - W.PERIOD_FROM).days + 6)
            recv = dt.datetime.combine(sim.d(off), dt.time(rng.randrange(7, 22),
                                                               rng.choice([5, 15, 25, 40, 55])))
            out.append(dict(route=route, ident="%s-2026-%06d" % (route, base + i + 1),
                            recv=recv, place=rng.choice(bogus), theme=rng.choice([t for t, _, _, _, o in W.THEMES if o is None]),
                            reason=rng.choices(reasons, weights=[62, 23, 15])[0]))
    out.sort(key=lambda e: (e["recv"], e["ident"]))
    return out


def write_item_log(target, reps, rng):
    """One row per item the press monitor matched. The items of one action share the report the
    monitor filed and the code its classifier put on that report."""
    items, n_rep = [], 0
    for r in reps:
        if r["route"] != "IMP":
            continue
        n_rep += 1
        a = r["action"]
        for k, title in enumerate(r["titles"]):
            drift = dt.timedelta(minutes=rng.choice([0, 7, 19, 34, 56, 88, 121]) * (1 if k else 0))
            items.append((r["recv_utc"] + drift, dict(
                estado="aceite", motivo="", ident=r["ident"], orgao=title, tema=a["theme"],
                codigo=r["code"], place=r["place"], ocorr=sim.d(a["day"]), start=r["start"],
                recv=r["recv_utc"] + drift)))
    titles = [o[0] for o in W.OUTLETS]
    weights = [o[3] for o in W.OUTLETS]
    for i in range(19900):
        off = rng.randrange(0, (W.EXTRACT - W.PERIOD_FROM).days + 1)
        recv = dt.datetime.combine(sim.d(off), dt.time(rng.randrange(6, 23), rng.randrange(0, 60)))
        items.append((recv, dict(
            estado="rejeitado", motivo=rng.choices([r for r, _ in REJECT],
                                                   weights=[w for _, w in REJECT])[0],
            ident="", orgao=rng.choices(titles, weights=weights)[0], tema="", codigo="",
            place="", ocorr=None, start=None, recv=recv)))
    items.sort(key=lambda t: (t[0], t[1]["orgao"], t[1]["ident"]))
    rows = []
    for i, (_, it) in enumerate(items, 1):
        rows.append(["IT-2026-%07d" % i, it["recv"].date().isoformat(), it["orgao"], it["estado"],
                     it["motivo"], it["ident"], it["tema"], it["codigo"], it["place"],
                     it["ocorr"].isoformat() if it["ocorr"] else "",
                     it["start"].strftime("%Y-%m-%d %H:%M") if it["start"] else "",
                     it["recv"].strftime("%Y-%m-%d %H:%M")])
    head = ["id_item", "data_recolha", "orgao", "estado", "motivo_rejeicao", "id_relato", "tema",
            "codigo_acao", "local_texto", "data_ocorrencia", "inicio_acao", "carimbo_recepcao"]
    return write_csv(os.path.join(target, "registo_itens_imprensa.csv"), head, rows), n_rep


def write_double_coding(target, dc):
    """The coding desk's hand-coding worksheet, one row per press report drawn."""
    rows = []
    for x in dc:
        r = x["report"]
        a = r["action"]
        rows.append([r["ident"], sim.d(a["day"]).isoformat(), a["theme"], x["machine"], x["hand"],
                     x["coder"], x["coded_day"].isoformat(), x["round_name"], x["second"],
                     x["decision"], x["note"]])
    head = ["id_relato", "data_ocorrencia", "tema", "codigo_monitor", "codigo_manual",
            "codificador", "data_codificacao", "ronda", "revisto_por", "decisao_da_mesa", "nota"]
    return write_csv(os.path.join(target, "amostra_dupla_codificacao.csv"), head, rows)


def write_partner_reports(target, reps):
    """The partner network's filings, with the August extract as both of its two loads."""
    rows = []
    for r in reps:
        if r["route"] != "PAR":
            continue
        a = r["action"]
        recv_utc = r["recv_utc"]
        load = "C2026%02d01" % sim.d(a["day"]).month
        rows.append([r["ident"], load, r["src"], a["theme"], r["code"], r["place"],
                     sim.d(a["day"]).isoformat(), r["start"].strftime("%Y-%m-%d %H:%M"),
                     recv_utc.strftime("%Y-%m-%dT%H:%MZ")])
    # The second load is the August file sent again after the receiving server failed, so the portal
    # stamped its rows on the day it arrived rather than on the day the network first delivered
    # them: fresh stamps on old content, which is what counts the month twice.
    extra = [list(x) for x in rows if x[6][:7] == "2026-08"]
    for e in extra:
        e[1] = "C20260802"                      # the second load of the same month
        e[8] = (dt.datetime.combine(RELOAD_ARRIVED, dt.time(8, 12))
                + dt.timedelta(minutes=int(e[0][-5:]) % 287)).strftime("%Y-%m-%dT%H:%MZ")
    rows = rows + extra
    rows.sort(key=lambda x: (x[1], x[0]))
    head = ["id_relato", "id_carga", "codigo_parceiro", "tema", "codigo_acao", "local_texto",
            "data_ocorrencia", "inicio_acao", "carimbo_entrega_utc"]
    return write_csv(os.path.join(target, "relatos_rede_parceiros.csv"), head, rows), len(extra)


def write_public_line(target, reps, rng):
    rows = []
    for r in reps:
        if r["route"] != "LIN":
            continue
        a = r["action"]
        rows.append([r["ident"], rng.choices(["web", "telefone"], weights=[68, 32])[0], a["theme"],
                     r["code"], r["place"], sim.d(a["day"]).isoformat(),
                     r["start"].strftime("%Y-%m-%d %H:%M"),
                     r["recv_local"].strftime("%Y-%m-%d %H:%M")])
    rows.sort(key=lambda x: (x[7], x[0]))
    head = ["id_relato", "canal", "tema", "codigo_acao", "local_texto", "data_ocorrencia",
            "inicio_acao", "carimbo_recepcao"]
    return write_csv(os.path.join(target, "relatos_linha_publica.csv"), head, rows)


def write_gazetteer(target, muni, locs):
    by_code = {m["code"]: m for m in muni}
    rows = []
    for l in locs:
        m = by_code[l["muni"]]
        rows.append([l["code"], l["name"], "atual", m["code"], m["name"], m["district"], m["region"]])
        if l["former"]:
            rows.append([l["code"], l["former"], "anterior", m["code"], m["name"], m["district"],
                         m["region"]])
    rows.sort(key=lambda r: (r[0], r[2]))
    head = ["codigo_localidade", "nome", "estado_nome", "codigo_municipio", "municipio", "distrito",
            "regiao"]
    return write_csv(os.path.join(target, "gazeteiro_localidades.csv"), head, rows)


def write_import_log(target, rows_par, dup_rows):
    rows, months = [], [(2026, m) for m in range(5, 12)]
    for y, m in months:
        first = dt.date(y, m, 1)
        last = min(dt.date(y + (m == 12), (m % 12) + 1, 1) - dt.timedelta(days=1), W.EXTRACT)
        for route, label in (("IMP", "itens_imprensa"), ("PAR", "relatos_parceiros"),
                             ("LIN", "linha_publica")):
            load = "C2026%02d01" % m
            done = min(last + dt.timedelta(days=2), W.EXTRACT)
            state = "concluida" if last < W.EXTRACT else "em curso"
            rows.append([load, route, "%s_%04d%02d.csv" % (label, y, m), "%s a %s" % (first, last),
                         done.isoformat(), state, ""])
    rows.append(["C20260802", "PAR", "relatos_parceiros_202608.csv", "2026-08-01 a 2026-08-31",
                 "2026-09-14", "concluida",
                 "reposicao do mes de agosto apos falha no servidor de recepcao"])
    rows.sort(key=lambda r: (r[4], r[0], r[1]))
    head = ["id_carga", "via", "ficheiro", "periodo_coberto", "concluida_em", "estado", "nota"]
    return write_csv(os.path.join(target, "registo_importacoes.csv"), head, rows)


def write_route_totals(target, reps, exc):
    """The association's own daily count of reports received on each route, in local time, with the
    reports it could not place included."""
    counts = {}
    seen = set()
    for r in reps:
        if r["ident"] in seen:
            continue
        seen.add(r["ident"])
        counts[(r["recv_local"].date(), r["route"])] = counts.get((r["recv_local"].date(), r["route"]), 0) + 1
    for e in exc:
        counts[(e["recv"].date(), e["route"])] = counts.get((e["recv"].date(), e["route"]), 0) + 1
    # the counter is written by the ingest process as each delivery arrives, so the second load of
    # the reposted August month is counted again on the day it arrived
    again = sum(1 for r in reps if r["route"] == "PAR"
                and r["action"]["day"] is not None
                and sim.d(r["action"]["day"]).year == W.REIMPORT_MONTH[0]
                and sim.d(r["action"]["day"]).month == W.REIMPORT_MONTH[1])
    counts[(RELOAD_ARRIVED, "PAR")] = counts.get((RELOAD_ARRIVED, "PAR"), 0) + again
    rows = [[day.isoformat(), route, n] for (day, route), n in sorted(counts.items())]
    head = ["data", "via", "relatos_recebidos"]
    return write_csv(os.path.join(target, "totais_por_via.csv"), head, rows)


def write_exceptions(target, exc):
    rows = [[e["ident"], e["route"], e["recv"].strftime("%Y-%m-%d %H:%M"), e["place"], e["theme"],
             e["reason"]] for e in exc]
    head = ["id_relato", "via", "carimbo_recepcao", "local_texto", "tema", "motivo"]
    return write_csv(os.path.join(target, "excecoes_geocodificacao.csv"), head, rows)


def write_config(target):
    cfg = {
        "versao": "4.2",
        "atualizado_em": "2026-04-28",
        "janela_de_recolha": {"inicio": "2026-05-01", "cadencia": "horaria",
                              "horas": "06:00 as 23:00, hora local do servidor; o que chega fora "
                                       "destas horas e escrito na recolha seguinte"},
        "orgaos": [{"codigo": o[0], "titulo": o[1], "distritos": o[2],
                    "peso_de_circulacao": o[3]} for o in W.OUTLETS],
        "regra_de_aceitacao": ("um item e aceite quando o classificador identifica uma acao coletiva "
                               "com local e data; os restantes ficam no registo com o motivo da rejeicao"),
        "palavras_chave": ["manifestacao", "concentracao", "bloqueio", "greve", "paralisacao",
                           "ocupacao", "vigilia", "marcha", "protesto", "corte de via"],
        "classificador": {"modelo": "vn-codificador-1.3", "treinado_em": W.CLS_TRAINED.isoformat(),
                          "alteracoes_no_periodo": "nenhuma",
                          "saida": "um codigo de acao do protocolo 2.2 por relato aceite"},
        "nota_de_relogio": ("o carimbo_recepcao de cada item vem no relogio UTC do servidor de "
                            "recolha; o inicio_acao vem no relogio local do local da acao, pelo "
                            "distrito do gazeteiro"),
        "fusos_horarios": {
            "continente_e_madeira": ("UTC+01:00 ate 25 de outubro de 2026 as 01:00 UTC e "
                                     "UTC+00:00 a partir desse momento"),
            "acores": ("UTC+00:00 ate 25 de outubro de 2026 as 01:00 UTC e UTC-01:00 a partir "
                       "desse momento"),
            "nota": ("o fuso de uma acao e o do distrito que o gazeteiro da a sua localidade; os "
                     "Acores e a Madeira sao distritos distintos no gazeteiro"),
        },
    }
    path = os.path.join(target, "config_monitor.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(cfg, fh, ensure_ascii=False, indent=1, sort_keys=False)
        fh.write("\n")
    return path


def write_notifications(target, muni, rng):
    """Notifications of public gatherings filed with the municipal authorities (a distractor)."""
    promoters = ["Associacao de Moradores", "Sindicato dos Transportes", "Comissao de Utentes",
                 "Juventude Operaria", "Associacao de Pais", "Nucleo de Agricultores",
                 "Grupo de Cidadaos", "Federacao Desportiva", "Associacao Comercial"]
    rows = []
    for i in range(1123):
        m = rng.choice(muni)
        day = W.PERIOD_FROM + dt.timedelta(days=rng.randrange(0, (W.EXTRACT - W.PERIOD_FROM).days + 20))
        rows.append(["NT-2026-%05d" % (i + 1), day.isoformat(), m["name"], m["district"],
                     "%s de %s" % (rng.choice(promoters), m["name"]),
                     rng.choice([30, 50, 80, 120, 150, 200, 250, 400, 600, 900, 1500]),
                     rng.choice(["concentracao", "marcha", "vigilia", "desfile", "concentracao"])])
    rows.sort(key=lambda r: (r[1], r[0]))
    head = ["id_notificacao", "data_prevista", "municipio", "distrito", "promotor",
            "participantes_previstos", "tipo_declarado"]
    return write_csv(os.path.join(target, "notificacoes_reuniao_publica.csv"), head, rows)


def write_coverage(target):
    rows = []
    for o in W.OUTLETS:
        for dist in (list(W.DISTRICTS) if "*" in o[2] else o[2]):
            rows.append([o[0], o[1], dist, "%.2f" % o[3]])
    rows.sort(key=lambda r: (r[0], r[2]))
    head = ["orgao", "titulo", "distrito", "peso_de_circulacao"]
    return write_csv(os.path.join(target, "cobertura_meios.csv"), head, rows)


def write_tension_index(target, rng):
    rows = []
    for dist in W.DISTRICTS:
        for m in range(5, 11):
            rows.append([dist, "2026-%02d" % m, "%.1f" % (rng.uniform(18, 74)),
                         rng.choice(["estavel", "em subida", "em descida"])])
    head = ["distrito", "mes", "indice_de_tensao", "tendencia"]
    return write_csv(os.path.join(target, "indice_tensao_distrital.csv"), head, rows)


def write_manifest(target, counts):
    rows = []
    for name, n, first, last, note in counts:
        rows.append([name, n, first, last, W.EXTRACT.isoformat(), note])
    head = ["ficheiro", "linhas", "primeiro_registo", "ultimo_registo", "extraido_em", "nota"]
    return write_csv(os.path.join(target, "manifesto_extracao.csv"), head, rows)
