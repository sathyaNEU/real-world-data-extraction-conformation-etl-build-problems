"""The fixed world behind the Watch register's first full reporting period.

Observatorio de Acao Coletiva, a Portuguese non-profit monitoring association. Its Vigilancia
Nacional register opened on 1 May 2026; the reporting period is 1 May to 30 October 2026 and the
record was extracted on 6 November 2026. Two actions in three reach the register only through the
press monitor, whose classifier assigns the action code; the coding desk measures that classifier
against hand coding twice a year.
"""
import datetime as dt

SEED = 215                                 # the action layer, measured in the design note
SEED_PACK = 410                             # a separate stream for reports, mess and the asks

ASSOCIATION = "Observatorio de Acao Coletiva"
REGISTER = "Vigilancia Nacional"
PEOPLE = {"officer": "Rafaela Carvalho",    # coding and methods desk
          "data": "Joel Branco"}            # data manager
CODERS = ["RC", "JB", "MM", "LS"]           # the desk's hand coders, by initials

OPEN_DAY = dt.date(2026, 5, 1)
PERIOD_FROM = dt.date(2026, 5, 1)
PERIOD_TO = dt.date(2026, 10, 30)
EXTRACT = dt.date(2026, 11, 6)
TRUSTEES = dt.date(2026, 11, 19)
SURGE_FROM = dt.date(2026, 9, 5)
DST_BACK = dt.date(2026, 10, 25)


def fortnights():
    out, start, n = [], PERIOD_FROM, 1
    while start <= PERIOD_TO:
        end = min(start + dt.timedelta(days=13), PERIOD_TO)
        if (PERIOD_TO - end).days < 7:
            end = PERIOD_TO
        out.append(("Q%d" % n, start, end))
        start, n = end + dt.timedelta(days=1), n + 1
    return out


THEMES = [
    ("TRM", "transporte rodoviario de mercadorias", 1.25),
    ("AGR", "agricultura e pecuaria", 1.10),
    ("SAU", "saude", 0.80),
    ("EDU", "educacao", 0.70),
    ("HAB", "habitacao", 1.05),
    ("CVD", "combustiveis e custo de vida", 1.20),
    ("PES", "pescas", 1.00),
    ("SMU", "servicos municipais", 0.85),
]
SURGE_THEMES = ["TRM", "AGR", "CVD"]

ACTION_CODES = [
    ("CO", "concentracao", False),
    ("MA", "marcha ou desfile", False),
    ("BL", "bloqueio de via", False),
    ("OC", "ocupacao", False),
    ("PA", "paralisacao", False),
    ("CF", "confronto com forcas de seguranca", True),
    ("RF", "remocao forcada", True),
    ("DP", "dano patrimonial", True),
]
CONFRONTATIONAL = [c for c, _, f in ACTION_CODES if f]
ORDINARY = [c for c, _, f in ACTION_CODES if not f]

ROUTES = [("IMP", "monitor de imprensa"),
          ("PAR", "rede de parceiros"),
          ("LIN", "linha de participacao publica")]

# how an action reaches the register
P_PRESS = 0.90          # the press monitor files a report on the action
P_PARTNER = 0.26        # a partner organisation files one, inside its own region
P_LINE = 0.17           # the public line receives one

# the press classifier, measured by the desk's hand coding
CLS_RECALL = 0.44       # confrontational actions it codes as confrontational
CLS_FALSE_MARK = 0.0125  # ordinary actions it codes as confrontational
CONF_RATE = 0.051      # the share of actions that are confrontational
SAMPLE_SIZE = 2600      # press reports hand coded over the period's two rounds
SAMPLE_ROUNDS = [(dt.date(2026, 7, 20), 1100), (dt.date(2026, 11, 3), 1500)]

PARTNERS = [
    ("P01", "Nucleo de Estudos do Trabalho do Minho", "Norte", 6.40),
    ("P02", "Associacao Civica do Mondego", "Centro", 5.80),
    ("P03", "Plataforma de Bairros da Margem Sul", "A.M. Lisboa", 7.10),
    ("P04", "Observatorio Rural do Alentejo Central", "Alentejo", 5.25),
    ("P05", "Liga dos Direitos do Barlavento", "Algarve", 6.75),
    ("P06", "Centro de Estudos Insulares", "Acores e Madeira", 8.20),
    ("P07", "Nucleo de Acompanhamento do Douro", "Norte", 6.40),
]
AMENDED = ("P04", dt.date(2026, 8, 1), 6.15)
MERGED = ("P07", "P12")

OUTLETS = [
    ("DNO", "Diario do Noroeste", ["Braga", "Viana do Castelo", "Porto"], 1.00),
    ("JLN", "Jornal do Litoral Norte", ["Porto", "Aveiro", "Braga"], 1.10),
    ("CBI", "Correio da Beira Interior", ["Viseu", "Guarda", "Castelo Branco"], 0.70),
    ("GMO", "Gazeta do Mondego", ["Coimbra", "Leiria", "Aveiro"], 0.85),
    ("CGL", "Correio da Grande Lisboa", ["Lisboa", "Setubal", "Santarem"], 1.25),
    ("DPL", "Diario da Planicie", ["Beja", "Evora", "Portalegre", "Setubal"], 0.80),
    ("NLS", "Noticiario do Litoral Sul", ["Faro"], 0.75),
    ("ATP", "Atlantico Diario", ["Ilhas"], 0.65),
    ("ATE", "Atlantico Daily", ["Ilhas"], 0.65),
    ("AGN", "Agencia Nacional de Noticias", ["*"], 1.40),
    ("SIN", "Servico Iberico de Noticias", ["*"], 0.55),
]
TWIN_FEED = ("ATP", "ATE")
REIMPORT_MONTH = (2026, 8)

ACTIONS_BASE, ACTIONS_SURGE = 18.0, 2.45    # actions a day, before and after the surge

DISTRICTS = {
    "Viana do Castelo": ["Arcos de Valdevez", "Ponte de Lima", "Viana do Castelo", "Valenca"],
    "Braga": ["Barcelos", "Braga", "Guimaraes", "Vila Nova de Famalicao", "Fafe", "Esposende"],
    "Porto": ["Amarante", "Felgueiras", "Gondomar", "Maia", "Matosinhos", "Penafiel", "Porto",
              "Santo Tirso", "Valongo", "Vila do Conde", "Pacos de Ferreira"],
    "Vila Real": ["Chaves", "Peso da Regua", "Vila Real", "Murca"],
    "Braganca": ["Braganca", "Mirandela", "Macedo de Cavaleiros"],
    "Aveiro": ["Agueda", "Aveiro", "Ilhavo", "Oliveira de Azemeis", "Ovar", "Sao Joao da Madeira",
               "Vagos", "Estarreja"],
    "Viseu": ["Lamego", "Mangualde", "Sao Pedro do Sul", "Viseu", "Tondela"],
    "Guarda": ["Gouveia", "Guarda", "Seia", "Trancoso"],
    "Coimbra": ["Cantanhede", "Coimbra", "Figueira da Foz", "Lousa", "Montemor-o-Velho", "Penacova"],
    "Castelo Branco": ["Castelo Branco", "Covilha", "Fundao", "Idanha-a-Nova", "Serta"],
    "Leiria": ["Alcobaca", "Caldas da Rainha", "Leiria", "Marinha Grande", "Nazare", "Pombal",
               "Peniche"],
    "Santarem": ["Abrantes", "Almeirim", "Cartaxo", "Rio Maior", "Santarem", "Tomar", "Torres Novas"],
    "Lisboa": ["Amadora", "Cascais", "Lisboa", "Loures", "Mafra", "Odivelas", "Oeiras", "Sintra",
               "Torres Vedras", "Vila Franca de Xira", "Alenquer"],
    "Setubal": ["Alcochete", "Almada", "Barreiro", "Moita", "Palmela", "Santiago do Cacem",
                "Seixal", "Sesimbra", "Setubal", "Sines"],
    "Portalegre": ["Elvas", "Portalegre", "Ponte de Sor", "Campo Maior"],
    "Evora": ["Estremoz", "Evora", "Montemor-o-Novo", "Vendas Novas", "Reguengos de Monsaraz"],
    "Beja": ["Beja", "Ferreira do Alentejo", "Moura", "Odemira", "Serpa"],
    "Faro": ["Albufeira", "Faro", "Lagos", "Loule", "Olhao", "Portimao", "Silves", "Tavira"],
    "Ilhas": ["Angra do Heroismo", "Ponta Delgada", "Praia da Vitoria", "Funchal", "Machico",
              "Camara de Lobos"],
}
REGION_OF = {
    "Viana do Castelo": "Norte", "Braga": "Norte", "Porto": "Norte", "Vila Real": "Norte",
    "Braganca": "Norte", "Aveiro": "Centro", "Viseu": "Centro", "Guarda": "Centro",
    "Coimbra": "Centro", "Castelo Branco": "Centro", "Leiria": "Centro", "Santarem": "Centro",
    "Lisboa": "A.M. Lisboa", "Setubal": "A.M. Lisboa", "Portalegre": "Alentejo",
    "Evora": "Alentejo", "Beja": "Alentejo", "Faro": "Algarve", "Ilhas": "Acores e Madeira",
}
COASTAL = {"Viana do Castelo", "Porto", "Aveiro", "Leiria", "Lisboa", "Setubal", "Faro", "Ilhas"}

LOC_PREFIX = ["Sao Martinho", "Santa Marta", "Sao Miguel", "Santa Luzia", "Sao Bartolomeu",
              "Nossa Senhora da Graca", "Vila Nova", "Vila Cha", "Quinta do Lago", "Casal Novo",
              "Ribeira Brava", "Fonte Boa", "Alto da Serra", "Vale de Cambra", "Carvalhal",
              "Sobreiro", "Pinheiro Manso", "Varzea", "Lourical", "Cabeco da Vinha",
              "Barroca", "Azinhaga", "Lagoa Nova", "Monte Redondo", "Senhora da Hora"]
RENAMES = 14
LAG_BASE = {"IMP": 112, "PAR": 652, "LIN": 94}
