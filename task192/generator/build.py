"""Cut the bundle, compute the bulletin's figures, write the deliverables and figures.json."""
import csv
import datetime as dt
import os
import random
import shutil
import sys

import docs
import golden as G
import pack as PK
import postprocess as PP
import sim
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def dictionary_sheets():
    return [
        ("registo_itens_imprensa", "Um registo por item que a lista de palavras-chave apanhou, "
         "aceite ou rejeitado. Uma acao e unica por tema, localidade e dia (protocolo 2.1), pelo "
         "que varios itens podem respeitar a mesma acao.",
         [("id_item", "texto", "identificador do item no monitor de imprensa"),
          ("data_recolha", "data", "dia em que o item foi recolhido, no relogio UTC do servidor"),
          ("orgao", "texto", "codigo do orgao de imprensa; os titulos estao em config_monitor.json"),
          ("estado", "texto", "aceite ou rejeitado pelo classificador"),
          ("motivo_rejeicao", "texto", "motivo da rejeicao; vazio nos itens aceites"),
          ("id_relato", "texto", "relato que o monitor filou com os itens da mesma acao; vazio nos itens rejeitados"),
          ("tema", "texto", "tema de disputa do protocolo; vazio nos rejeitados"),
          ("codigo_acao", "texto", "codigo de acao que o classificador atribuiu ao relato (protocolo 4.2); igual em todos os itens do mesmo relato"),
          ("local_texto", "texto", "localidade tal como o relato a da, com o nome atual ou o nome anterior do gazeteiro"),
          ("data_ocorrencia", "data", "dia de calendario local da acao, tal como o registo o fixa"),
          ("inicio_acao", "data e hora", "hora a que a acao comecou, no relogio local do local da "
                                         "acao; o fuso de cada distrito do gazeteiro esta em "
                                         "config_monitor.json"),
          ("carimbo_recepcao", "data e hora", "momento em que o item entrou no monitor, no relogio "
                                              "UTC do servidor de recolha; um relato reune os itens "
                                              "da mesma acao e o relato entrou no monitor com o "
                                              "primeiro deles")]),
        ("relatos_rede_parceiros", "Um registo por relato entregue por uma organizacao parceira. "
         "O mesmo relato aparece em duas cargas quando um mes foi reposto; o id_relato e o mesmo.",
         [("id_relato", "texto", "identificador do relato"),
          ("id_carga", "texto", "carga de importacao que trouxe a linha; ver registo_importacoes"),
          ("codigo_parceiro", "texto", "codigo de entrega da organizacao parceira"),
          ("tema", "texto", "tema de disputa do protocolo"),
          ("codigo_acao", "texto", "codigo de acao do protocolo 2.2"),
          ("local_texto", "texto", "localidade tal como o relato a da"),
          ("data_ocorrencia", "data", "dia de calendario local da acao"),
          ("inicio_acao", "data e hora", "hora a que a acao comecou, no relogio local do local da acao"),
          ("carimbo_entrega_utc", "data e hora", "momento da entrega no portal de parceiros, em UTC")]),
        ("relatos_linha_publica", "Um registo por relato recebido na linha de participacao publica.",
         [("id_relato", "texto", "identificador do relato"),
          ("canal", "texto", "web ou telefone"),
          ("tema", "texto", "tema de disputa do protocolo"),
          ("codigo_acao", "texto", "codigo de acao do protocolo 2.2"),
          ("local_texto", "texto", "localidade tal como o relato a da"),
          ("data_ocorrencia", "data", "dia de calendario local da acao"),
          ("inicio_acao", "data e hora", "hora a que a acao comecou, no relogio local do local da acao"),
          ("carimbo_recepcao", "data e hora", "momento da recepcao na linha, no relogio local de "
                                              "Lisboa da associacao")]),
        ("amostra_dupla_codificacao", "Folha de trabalho da mesa de codificacao: uma linha por "
         "relato do monitor de imprensa que a mesa tirou para o lote da ronda e codificou a mao "
         "(protocolo 4.5). Cada ronda tira o lote dos relatos aceites entrados desde o fecho da "
         "ronda anterior. Nao ha linhas de outras vias.",
         [("id_relato", "texto", "relato do monitor de imprensa que foi codificado a mao"),
          ("data_ocorrencia", "data", "dia de calendario local da acao do relato"),
          ("tema", "texto", "tema de disputa do relato"),
          ("codigo_monitor", "texto", "codigo de acao que o classificador do monitor atribuiu ao relato"),
          ("codigo_manual", "texto", "codigo de acao da codificacao manual, depois da decisao da "
                                     "mesa nas linhas que foram a segunda codificacao"),
          ("codificador", "texto", "iniciais de quem codificou a mao"),
          ("data_codificacao", "data", "dia em que a codificacao manual foi feita; a mesa trabalha o "
                                       "lote nos seus dias de trabalho anteriores ao fecho da "
                                       "ronda, com dias de recuperacao ao fim de semana quando o "
                                       "lote o exige"),
          ("ronda", "texto", "ronda de codificacao, com o seu corte e o seu fecho: R1, corte em 19 "
                             "de junho e fecho em 20 de junho de 2026, sobre os relatos de 1 de "
                             "maio a 19 de junho; R2, corte em 31 de agosto e fecho em 10 de "
                             "setembro de 2026, sobre os relatos de 20 de junho a 31 de agosto"),
          ("revisto_por", "texto", "iniciais de quem fez a segunda codificacao; vazio nas linhas "
                                   "que nao foram revistas"),
          ("decisao_da_mesa", "texto", "mantido ou alterado, nas linhas que foram revistas"),
          ("nota", "texto", "nota de codificacao, quando quem codificou deixou uma")]),
        ("gazeteiro_localidades", "Uma linha por nome de localidade. Uma localidade com nome novo "
         "fica com duas linhas, a atual e a anterior, ambas com o mesmo codigo_localidade.",
         [("codigo_localidade", "texto", "codigo da localidade no gazeteiro de 2024"),
          ("nome", "texto", "nome da localidade"),
          ("estado_nome", "texto", "atual ou anterior"),
          ("codigo_municipio", "texto", "codigo do municipio"),
          ("municipio", "texto", "nome do municipio"),
          ("distrito", "texto", "distrito do gazeteiro; os Acores e a Madeira sao distritos "
                                "distintos e config_monitor.json da o fuso de cada um"),
          ("regiao", "texto", "regiao de monitorizacao")]),
        ("excecoes_geocodificacao", "Um registo por relato recebido que o gazeteiro nao fixou. Nao "
         "produz acao (protocolo 2.5) e nao entra nos ficheiros de relatos.",
         [("id_relato", "texto", "identificador do relato"),
          ("via", "texto", "via de acesso que recebeu o relato"),
          ("carimbo_recepcao", "data e hora", "momento da recepcao, na hora local"),
          ("local_texto", "texto", "texto de localidade que nao foi fixado"),
          ("tema", "texto", "tema de disputa declarado"),
          ("motivo", "texto", "motivo pelo qual a localidade nao foi fixada")]),
        ("totais_por_via", "Uma linha por dia e por via: o contador que o processo de importacao "
         "escreve a medida que as entregas chegam, na hora local de Lisboa, incluindo os relatos "
         "que o gazeteiro nao fixou. O contador conta cada chegada, pelo que uma carga reposta e "
         "contada outra vez no dia em que chegou.",
         [("data", "data", "dia de recepcao, na hora local de Lisboa"),
          ("via", "texto", "via de acesso"),
          ("relatos_recebidos", "inteiro", "chegadas contadas nesse dia nessa via")]),
        ("registo_importacoes", "Uma linha por carga de importacao.",
         [("id_carga", "texto", "codigo da carga"), ("via", "texto", "via de acesso"),
          ("ficheiro", "texto", "ficheiro de origem"),
          ("periodo_coberto", "texto", "periodo que a carga cobre"),
          ("concluida_em", "data", "dia em que a carga terminou"),
          ("estado", "texto", "estado da carga"), ("nota", "texto", "nota de operacao")]),
        ("convencoes", "Convencoes de leitura dos quadros do boletim.",
         [("mediana", "regra", "num conjunto com um numero par de valores a mediana e a media dos "
                               "dois valores centrais"),
          ("percentagem", "regra", "uma percentagem e arredondada uma vez, a uma decimal, a partir "
                                   "do valor exato, e nao truncada nem arredondada por etapas"),
          ("quinzena", "regra", "as quinzenas tem catorze dias e contam-se a partir de 1 de maio; "
                                "os dias que sobram no fim do periodo entram na ultima, que tem "
                                "quinze dias (protocolo 3.4)"),
          ("acao", "regra", "uma acao e um tema numa localidade num dia (protocolo 2.1), qualquer "
                            "que seja o numero de relatos"),
          ("acao relatada por uma via", "regra", "uma acao e relatada por uma via quando essa via "
                                                 "entregou relato dela, ainda que outras vias "
                                                 "tambem o tenham feito, e conta uma vez"),
          ("relato recebido", "regra", "um relato conta uma vez na via que o recebeu, qualquer que "
                                       "seja o numero de cargas de importacao que o trouxeram"),
          ("relatos recebidos no periodo", "regra", "os relatos que cada via recebeu entre 1 de "
                                                    "maio e 30 de outubro; sao estes que o quadro "
                                                    "de vias conta e sobre estes que a mediana se "
                                                    "calcula, e os recebidos depois do fecho do "
                                                    "periodo entram no boletim seguinte"),
          ("minutos do inicio ao relato", "regra", "a diferenca entre o momento do relato e o "
                                                   "inicio da acao, com cada momento no fuso que "
                                                   "config_monitor.json da ao distrito da acao"),
          ("relatos de um parceiro", "regra", "os relatos que a organizacao entregou sobre acoes "
                                              "datadas no periodo de relato"),
          ("codigo de entrega", "regra", "os codigos de entrega de um mesmo acordo contam juntos; "
                                         "as adendas aos acordos estao em acordos_dados_parceiros")]),
        ("outros ficheiros", "Os restantes ficheiros da extracao.",
         [("config_monitor.json", "json", "configuracao do monitor de imprensa: orgaos, palavras-chave, regra de aceitacao e nota de relogio"),
          ("notificacoes_reuniao_publica.csv", "csv", "notificacoes de reuniao e manifestacao entregues nas camaras municipais"),
          ("cobertura_meios.csv", "csv", "cobertura declarada de cada orgao por distrito"),
          ("indice_tensao_distrital.csv", "csv", "indice de tensao da associacao, por distrito e mes"),
          ("manifesto_extracao.csv", "csv", "linhas, intervalo e data de extracao de cada ficheiro"),
          ("protocolo_vigilancia_v4.pdf", "pdf", "protocolo da Vigilancia Nacional, versao 4"),
          ("acordos_dados_parceiros.pdf", "pdf", "acordos de dados com as organizacoes parceiras e adenda"),
          ("relatorios_mensais_parceiros_2026.pdf", "pdf", "relatorios mensais de entrega das "
           "organizacoes parceiras; cada organizacao conta os relatos pelo mes da acao, nao pelo "
           "mes da entrega no portal"),
          ("boletins_anteriores_2026.pdf", "pdf", "boletins mensais publicados de maio a setembro")]),
    ]


def partner_table(target):
    """What each partner's own monthly return states, by the month of the action."""
    b = G.load(target)
    seen = {}
    for r in b["reports"]:
        if r["route"] == "PAR":
            seen.setdefault(r["ident"], r)
    code_to = {p[0]: p[0] for p in W.PARTNERS}
    code_to[W.MERGED[1]] = W.MERGED[0]
    table = {}
    for code, name, region, rate in W.PARTNERS:
        for m in range(5, 12):
            n = sum(1 for r in seen.values()
                    if code_to.get(r["src"]) == code and r["day"].month == m and r["day"].year == 2026)
            note = ""
            if code == "P02" and m == 7:
                note = "entrega semanal interrompida de 13 a 19 de julho por avaria no portal"
            if code == "P06" and m == 6:
                note = "equipa de terreno em formacao na primeira semana"
            table[(code, m)] = (n, note)
    return table


def cut(target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    rng = random.Random(W.SEED_PACK)
    muni, locs = sim.geography(rng)
    acts = sim.actions(muni, locs)
    sim.routes(acts, rng)
    reps = sim.reports(acts, rng)
    dc = sim.double_coding(acts, reps, rng)
    PK.build_reports(reps, locs, rng)
    exc = PK.exceptions(rng)

    n_items, n_press = PK.write_item_log(target, reps, rng)
    n_dc = PK.write_double_coding(target, dc)
    n_par, n_dup = PK.write_partner_reports(target, reps)
    n_lin = PK.write_public_line(target, reps, rng)
    n_gaz = PK.write_gazetteer(target, muni, locs)
    n_imp = PK.write_import_log(target, n_par, n_dup)
    n_exc = PK.write_exceptions(target, exc)
    n_tot = PK.write_route_totals(target, reps, exc)
    PK.write_config(target)
    n_not = PK.write_notifications(target, muni, rng)
    n_cov = PK.write_coverage(target)
    n_ten = PK.write_tension_index(target, rng)

    docs.protocol(target)
    docs.agreements(target)
    docs.partner_returns(target, partner_table(target))
    b = G.load(target)
    acts_b = G.actions(b["reports"])
    series = []
    for i, label in enumerate(["maio", "junho", "julho", "agosto", "setembro"], 5):
        inside = [x for x in acts_b if x["day"].month == i and x["day"].year == 2026]
        series.append((label, len(inside), len({x["muni"] for x in inside}),
                       len({x["loc"] for x in inside})))
    docs.bulletins(target, series)
    docs.dictionary(target, dictionary_sheets())

    for name, stampdate in (("protocolo_vigilancia_v4.pdf", b"D:20260424103000+00'00'"),
                            ("acordos_dados_parceiros.pdf", b"D:20260724154500+00'00'"),
                            ("relatorios_mensais_parceiros_2026.pdf", b"D:20261104091500+00'00'"),
                            ("boletins_anteriores_2026.pdf", b"D:20261012113000+00'00'")):
        PP.normalize_pdf(os.path.join(target, name), stampdate, stampdate)
    PP.normalize_ooxml(os.path.join(target, "dicionario_dados.xlsx"), W.PEOPLE["data"],
                       W.PEOPLE["data"], "2026-05-04T08:40:00Z", "2026-11-06T18:05:00Z",
                       title="Dicionario de dados da Vigilancia Nacional", excel=True)

    rows = []
    for name in sorted(os.listdir(target)):
        path = os.path.join(target, name)
        if name.endswith(".csv"):
            with open(path, encoding="utf-8") as fh:
                rr = list(csv.reader(fh))
            n = len(rr) - 1
            cols = [i for i, h in enumerate(rr[0]) if h.startswith("data") or h.startswith("carimbo")]
            vals = sorted(r[c][:10] for r in rr[1:] for c in cols[:1] if len(r) > c and r[c])
            first, last = (vals[0], vals[-1]) if vals else ("", "")
        else:
            n, first, last = "", "", ""
        note = {"registo_itens_imprensa.csv": "itens do monitor de imprensa, por item",
                "amostra_dupla_codificacao.csv": "folha de trabalho da mesa de codificacao",
                "relatos_rede_parceiros.csv": "relatos das organizacoes parceiras, por linha de carga",
                "relatos_linha_publica.csv": "relatos da linha de participacao publica",
                "gazeteiro_localidades.csv": "gazeteiro de 2024, uma linha por nome",
                "excecoes_geocodificacao.csv": "relatos sem localidade fixada",
                "totais_por_via.csv": "contador diario do processo de importacao, por via",
                "registo_importacoes.csv": "cargas de importacao",
                "notificacoes_reuniao_publica.csv": "notificacoes entregues nas camaras",
                "cobertura_meios.csv": "cobertura declarada dos orgaos",
                "indice_tensao_distrital.csv": "indice de tensao por distrito e mes",
                "config_monitor.json": "configuracao do monitor de imprensa",
                "protocolo_vigilancia_v4.pdf": "protocolo da Vigilancia Nacional, versao 4",
                "acordos_dados_parceiros.pdf": "acordos de dados e adenda",
                "relatorios_mensais_parceiros_2026.pdf": "relatorios mensais das parceiras, "
                                                          "contados pelo mes da acao",
                "boletins_anteriores_2026.pdf": "boletins mensais publicados",
                "dicionario_dados.xlsx": "dicionario de dados"}.get(name, "")
        rows.append((name, n, first, last, note))
    PK.write_manifest(target, rows)
    return dict(items=n_items, press_reports=n_press, sample=n_dc, par=n_par, dup=n_dup, lin=n_lin,
                gaz=n_gaz, imports=n_imp, exceptions=n_exc, totals=n_tot, notifications=n_not,
                coverage=n_cov, tension=n_ten)


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    counts = cut(target)
    g = G.compute(target)
    g["pack"] = counts
    gold = os.path.join(TASK, "golden")
    os.makedirs(gold, exist_ok=True)
    import deliver as DL
    import figures as FG
    import metadata as MD
    DL.workbook(os.path.join(gold, "boletim_vigilancia_2026S2.xlsx"), g)
    chart_png = os.path.join(HERE, "_acoes_por_quinzena.png")
    DL.chart(chart_png, g)
    DL.bulletin(os.path.join(gold, "boletim_confrontos_2026S2.pdf"), g, chart_png)
    PP.normalize_ooxml(os.path.join(gold, "boletim_vigilancia_2026S2.xlsx"), W.PEOPLE["officer"],
                       W.PEOPLE["officer"], "2026-11-09T09:30:00Z", "2026-11-13T16:45:00Z",
                       title="Boletim da Vigilancia Nacional, maio a outubro de 2026", excel=True)
    PP.normalize_pdf(os.path.join(gold, "boletim_confrontos_2026S2.pdf"),
                     b"D:20261113164500+00'00'", b"D:20261113164500+00'00'")
    os.remove(chart_png)
    MD.write(TASK, g)
    import checks as CK
    import verify as VF
    n = CK.run(target, g)
    FG.write(HERE, g)
    k = VF.run(target, os.path.join(HERE, "figures.json"))
    print("generator assertions", n, "independent checks", k)
    print("actions %d | press reported %d | other %d" % (g["actions_in_period"], g["press_only"],
                                                         g["filed_by_hand"]))
    print("call    : %d confrontational actions (raw %.3f, to the nearest %d)"
          % (g["total"], g["raw_total"], g["grain"]))
    print("routes  : codes as filed %d, false marks out %d, hand where audited %d, audited "
          "shares %d, recall only %d, audited prevalence %d"
          % (g["rung0"], g["rung1"], g["rung5"], g["rung3"], g["rung2"], g["rung4"]))
    print("sample  : %d rows, %d/%d/%d/%d, recall %.4f, false mark %.4f, months %s"
          % (g["sample_rows"], g["tp"], g["fn"], g["fp"], g["tn"], g["recall"], g["false_mark"],
             g["audit_covers"]))
    print("mix     : audited prevalence %.4f against the record's %.4f"
          % (g["audit_prevalence"], g["record_prevalence"]))
    print("variants: continuity %.2f hybrid %.2f matrix %.2f rg-fb-month %.2f rg-fb-theme %.2f"
          % (g["variant_continuity"], g["variant_hybrid"], g["variant_matrix_inverse"],
             g["variant_rg_fb_month"], g["variant_rg_fb_theme"]))
    print("dead    : %s" % {k: v["broken"] for k, v in sorted(g["dead"].items())})
    if "boot" in g:
        print("noise   : sd of the call %.1f, sd of the gap %.1f, mean gap %.1f"
              % (g["boot"]["sd_rg"], g["boot"]["sd_gap"], g["boot"]["mean_gap"]))
    print("pack    :", counts)
