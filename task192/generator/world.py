"""The fixed world behind the Watch register's first full reporting period.

Observatorio de Acao Coletiva, a Portuguese non-profit monitoring association. Its Vigilancia
Nacional register opened on 1 May 2026; the reporting period is 1 May to 30 October 2026 and the
record was extracted on 6 November 2026.
"""
import datetime as dt

SEED = 293                                  # the episode layer's seed, measured in the design note
SEED_PACK = 2930                            # a separate stream for actions, reports and mess

ASSOCIATION = "Observatorio de Acao Coletiva"
REGISTER = "Vigilancia Nacional"
PEOPLE = {"officer": "Rafaela Carvalho",    # early-warning programme officer
          "data": "Joel Branco"}            # data manager

OPEN_DAY = dt.date(2026, 5, 1)              # the register opened; no episode is carried in
PERIOD_FROM = dt.date(2026, 5, 1)
PERIOD_TO = dt.date(2026, 10, 30)
EXTRACT = dt.date(2026, 11, 6)
TRUSTEES = dt.date(2026, 11, 19)
SURGE_FROM = dt.date(2026, 9, 5)
DST_BACK = dt.date(2026, 10, 25)            # clocks go back an hour at 02:00 local
QUIET_DAYS = 21                             # the protocol's peace interval

# the fortnights the protocol reports on: from 1 May, the last ends with the period
def fortnights():
    out, start, n = [], PERIOD_FROM, 1
    while start <= PERIOD_TO:
        end = min(start + dt.timedelta(days=13), PERIOD_TO)
        if (PERIOD_TO - end).days < 7:          # the last fortnight ends with the period
            end = PERIOD_TO
        out.append(("Q%d" % n, start, end))
        start, n = end + dt.timedelta(days=1), n + 1
    return out


# dispute themes, the protocol's codes
THEMES = [
    ("TRM", "transporte rodoviario de mercadorias"),
    ("AGR", "agricultura e pecuaria"),
    ("SAU", "saude"),
    ("EDU", "educacao"),
    ("HAB", "habitacao"),
    ("CVD", "combustiveis e custo de vida"),
    ("PES", "pescas"),
    ("SMU", "servicos municipais"),
]
SURGE_THEMES = ["TRM", "AGR", "CVD"]

# action codes; the protocol names CF, RF and DP as the confrontational ones
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

# access routes
ROUTES = [("IMP", "monitor de imprensa"),
          ("PAR", "rede de parceiros"),
          ("LIN", "linha de participacao publica")]

# partner organisations under data agreements: code, name, region, rate per accepted report in EUR
PARTNERS = [
    ("P01", "Nucleo de Estudos do Trabalho do Minho", "Norte", 6.40),
    ("P02", "Associacao Civica do Mondego", "Centro", 5.80),
    ("P03", "Plataforma de Bairros da Margem Sul", "A.M. Lisboa", 7.10),
    ("P04", "Observatorio Rural do Alentejo Central", "Alentejo", 5.25),
    ("P05", "Liga dos Direitos do Barlavento", "Algarve", 6.75),
    ("P06", "Centro de Estudos Insulares", "Acores e Madeira", 8.20),
    ("P07", "Nucleo de Acompanhamento do Douro", "Norte", 6.40),
]
# P04's agreement was amended on 1 August 2026: the rate rose to 6.15 EUR a report
AMENDED = ("P04", dt.date(2026, 8, 1), 6.15)
# P07 absorbed a smaller association in September and filed under both codes after the merger
MERGED = ("P07", "P12")

# the media monitor's outlets: code, title, publisher zone, districts covered, weight
OUTLETS = [
    ("DNO", "Diario do Noroeste", "Europe/Lisbon", ["Braga", "Viana do Castelo", "Porto"], 1.00),
    ("JPO", "Jornal do Litoral Norte", "Europe/Lisbon", ["Porto", "Aveiro", "Braga"], 1.10),
    ("CBI", "Correio da Beira Interior", "Europe/Lisbon", ["Viseu", "Guarda", "Castelo Branco"], 0.70),
    ("GMO", "Gazeta do Mondego", "Europe/Lisbon", ["Coimbra", "Leiria", "Aveiro"], 0.85),
    ("DLX", "Correio da Grande Lisboa", "Europe/Lisbon", ["Lisboa", "Setubal", "Santarem"], 1.25),
    ("PSU", "Diario da Planicie", "Europe/Lisbon", ["Beja", "Evora", "Portalegre", "Setubal"], 0.80),
    ("ALG", "Noticiario do Litoral Sul", "Europe/Lisbon", ["Faro"], 0.75),
    ("ATP", "Atlantico Diario", "Atlantic/Azores", ["Ilhas"], 0.65),
    ("ATE", "Atlantico Daily", "Atlantic/Azores", ["Ilhas"], 0.65),
    ("AGN", "Agencia Nacional de Noticias", "Europe/Lisbon", ["*"], 1.40),
    ("REU", "Servico Iberico de Noticias", "Europe/Madrid", ["*"], 0.55),
]
# the two titles of one media group that cover the same actions in two languages
TWIN_FEED = ("ATP", "ATE")
# the month the partner extract was loaded twice
REIMPORT_MONTH = (2026, 8)

# the episode classes: share, closure hazard by phase, escalation multiplier
CLASSES = {
    "flare":    dict(w=0.50, h2=(0.090, 0.050, 0.030), em=1.0),
    "campaign": dict(w=0.28, h2=(0.014, 0.026, 0.018), em=1.50),
    "standing": dict(w=0.22, h2=(0.004, 0.0045, 0.0030), em=0.30),
}
H1MAX, H1PEAK, H1TMAX = 0.0145, 12.0, 78    # the escalation hazard's hump
OPEN_BASE, OPEN_SURGE = 2.55, 2.4           # openings a day, before and after the surge

# geography: district -> municipalities. Real Portuguese municipalities; the localities inside each
# are composed from the usual Portuguese toponym elements.
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
    "Castelo Branco": ["Castelo Branco", "Covilha", "Fundao", "Idanha-a-Nova", "Sertã"],
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
# settlements whose name changed with the 2024 gazetteer revision; both names stay on file
RENAMES = 14
LAG_BASE = {"IMP": 112, "PAR": 652, "LIN": 94}
TARGET_ITEM_ROWS = 25600
