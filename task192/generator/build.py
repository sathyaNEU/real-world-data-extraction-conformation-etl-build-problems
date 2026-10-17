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
          ("id_relato", "texto", "identificador do relato que o item aceite produz; vazio nos rejeitados"),
          ("tema", "texto", "tema de disputa do protocolo; vazio nos rejeitados"),
          ("codigo_acao", "texto", "codigo de acao do protocolo 2.2; vazio nos rejeitados"),
          ("local_texto", "texto", "localidade tal como o relato a da, com o nome atual ou o nome anterior do gazeteiro"),
          ("data_ocorrencia", "data", "dia de calendario local da acao, tal como o registo o fixa"),
          ("inicio_acao", "data e hora", "hora local a que a acao comecou"),
          ("carimbo_recepcao", "data e hora", "momento em que o item entrou no monitor, no relogio UTC do servidor de recolha")]),
        ("relatos_rede_parceiros", "Um registo por relato entregue por uma organizacao parceira. "
         "O mesmo relato aparece em duas cargas quando um mes foi reposto; o id_relato e o mesmo.",
         [("id_relato", "texto", "identificador do relato"),
          ("id_carga", "texto", "carga de importacao que trouxe a linha; ver registo_importacoes"),
          ("codigo_parceiro", "texto", "codigo de entrega da organizacao parceira"),
          ("tema", "texto", "tema de disputa do protocolo"),
          ("codigo_acao", "texto", "codigo de acao do protocolo 2.2"),
          ("local_texto", "texto", "localidade tal como o relato a da"),
          ("data_ocorrencia", "data", "dia de calendario local da acao"),
          ("inicio_acao", "data e hora", "hora local a que a acao comecou"),
          ("carimbo_entrega_utc", "data e hora", "momento da entrega no portal de parceiros, em UTC")]),
        ("relatos_linha_publica", "Um registo por relato recebido na linha de participacao publica.",
         [("id_relato", "texto", "identificador do relato"),
          ("canal", "texto", "web ou telefone"),
          ("tema", "texto", "tema de disputa do protocolo"),
          ("codigo_acao", "texto", "codigo de acao do protocolo 2.2"),
          ("local_texto", "texto", "localidade tal como o relato a da"),
          ("data_ocorrencia", "data", "dia de calendario local da acao"),
          ("inicio_acao", "data e hora", "hora local a que a acao comecou"),
          ("carimbo_recepcao", "data e hora", "momento da recepcao, na hora local")]),
        ("gazeteiro_localidades", "Uma linha por nome de localidade. Uma localidade com nome novo "
         "fica com duas linhas, a atual e a anterior, ambas com o mesmo codigo_localidade.",
         [("codigo_localidade", "texto", "codigo da localidade no gazeteiro de 2024"),
          ("nome", "texto", "nome da localidade"),
          ("estado_nome", "texto", "atual ou anterior"),
          ("codigo_municipio", "texto", "codigo do municipio"),
          ("municipio", "texto", "nome do municipio"),
          ("distrito", "texto", "distrito"), ("regiao", "texto", "regiao de monitorizacao")]),
        ("excecoes_geocodificacao", "Um registo por relato recebido que o gazeteiro nao fixou. Nao "
         "produz acao (protocolo 2.5) e nao entra nos ficheiros de relatos.",
         [("id_relato", "texto", "identificador do relato"),
          ("via", "texto", "via de acesso que recebeu o relato"),
          ("carimbo_recepcao", "data e hora", "momento da recepcao, na hora local"),
          ("local_texto", "texto", "texto de localidade que nao foi fixado"),
          ("tema", "texto", "tema de disputa declarado"),
          ("motivo", "texto", "motivo pelo qual a localidade nao foi fixada")]),
        ("totais_por_via", "Uma linha por dia e por via: os relatos que a via recebeu nesse dia, na "
         "hora local, incluindo os que o gazeteiro nao fixou.",
         [("data", "data", "dia de recepcao, na hora local"),
          ("via", "texto", "via de acesso"),
          ("relatos_recebidos", "inteiro", "relatos recebidos nesse dia nessa via")]),
        ("registo_importacoes", "Uma linha por carga de importacao.",
         [("id_carga", "texto", "codigo da carga"), ("via", "texto", "via de acesso"),
          ("ficheiro", "texto", "ficheiro de origem"),
          ("periodo_coberto", "texto", "periodo que a carga cobre"),
          ("concluida_em", "data", "dia em que a carga terminou"),
          ("estado", "texto", "estado da carga"), ("nota", "texto", "nota de operacao")]),
        ("outros ficheiros", "Os restantes ficheiros da extracao.",
         [("config_monitor.json", "json", "configuracao do monitor de imprensa: orgaos, palavras-chave, regra de aceitacao e nota de relogio"),
          ("notificacoes_reuniao_publica.csv", "csv", "notificacoes de reuniao e manifestacao entregues nas camaras municipais"),
          ("cobertura_meios.csv", "csv", "cobertura declarada de cada orgao por distrito"),
          ("indice_tensao_distrital.csv", "csv", "indice de tensao da associacao, por distrito e mes"),
          ("manifesto_extracao.csv", "csv", "linhas, intervalo e data de extracao de cada ficheiro"),
          ("protocolo_vigilancia_v4.pdf", "pdf", "protocolo da Vigilancia Nacional, versao 4"),
          ("acordos_dados_parceiros.pdf", "pdf", "acordos de dados com as organizacoes parceiras e adenda"),
          ("relatorios_mensais_parceiros_2026.pdf", "pdf", "relatorios mensais de entrega das organizacoes parceiras"),
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
    eps = sim.episodes()
    rng = random.Random(W.SEED_PACK)
    muni, locs = sim.geography(rng)
    sim.plan(eps, rng)
    sim.assign(eps, muni, rng)
    acts = sim.actions(eps, locs, rng)
    reps = sim.reports(acts, rng)
    PK.build_reports(reps, locs, rng)
    exc = PK.exceptions(rng)

    n_items, n_acc = PK.write_item_log(target, reps, rng)
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
                "relatos_rede_parceiros.csv": "relatos das organizacoes parceiras, por linha de carga",
                "relatos_linha_publica.csv": "relatos da linha de participacao publica",
                "gazeteiro_localidades.csv": "gazeteiro de 2024, uma linha por nome",
                "excecoes_geocodificacao.csv": "relatos sem localidade fixada",
                "totais_por_via.csv": "contagem diaria da associacao, por via",
                "registo_importacoes.csv": "cargas de importacao",
                "notificacoes_reuniao_publica.csv": "notificacoes entregues nas camaras",
                "cobertura_meios.csv": "cobertura declarada dos orgaos",
                "indice_tensao_distrital.csv": "indice de tensao por distrito e mes",
                "config_monitor.json": "configuracao do monitor de imprensa",
                "protocolo_vigilancia_v4.pdf": "protocolo da Vigilancia Nacional, versao 4",
                "acordos_dados_parceiros.pdf": "acordos de dados e adenda",
                "relatorios_mensais_parceiros_2026.pdf": "relatorios mensais das parceiras",
                "boletins_anteriores_2026.pdf": "boletins mensais publicados",
                "dicionario_dados.xlsx": "dicionario de dados"}.get(name, "")
        rows.append((name, n, first, last, note))
    PK.write_manifest(target, rows)
    return dict(items=n_items, accepted=n_acc, par=n_par, dup=n_dup, lin=n_lin, gaz=n_gaz,
                imports=n_imp, exceptions=n_exc, totals=n_tot, notifications=n_not,
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
    DL.chart(os.path.join(gold, "acoes_por_quinzena.png"), g)
    PP.normalize_ooxml(os.path.join(gold, "boletim_vigilancia_2026S2.xlsx"), W.PEOPLE["officer"],
                       W.PEOPLE["officer"], "2026-11-09T09:30:00Z", "2026-11-13T16:45:00Z",
                       title="Boletim da Vigilancia Nacional, periodo de maio a outubro de 2026",
                       excel=True)
    MD.write(TASK, g)
    FG.write(HERE, g)
    import checks as CK
    import verify as VF
    n = CK.run(target, g)
    k = VF.run(target, os.path.join(HERE, "figures.json"))
    print("generator assertions", n, "independent checks", k)
    print("cohort %d episodes | recorded %d | closed quiet %d | still open %d"
          % (g["cohort"], g["recorded"], g["closed_quiet"], g["still_open"]))
    print("call    : %d per cent, %d episodes (raw %.3f episodes, %.3f per cent)"
          % (g["rate_pct"], g["episodes"], g["raw_episodes"], g["raw_rate"]))
    print("rung 0  : %d per cent, %d episodes" % (g["rung0_pct"], g["rung0_episodes"]))
    print("rung 1  : %d per cent, %d episodes" % (g["rung1_pct"], g["rung1_episodes"]))
    print("rung 2  : %d per cent, %d episodes" % (g["rung2_pct"], g["rung2_episodes"]))
    print("variants: weekly %.3f fortnightly %.3f projected %.3f"
          % (g["weekly_episodes"], g["fortnightly_episodes"], g["projected_episodes"]))
    print("pack    :", counts)
