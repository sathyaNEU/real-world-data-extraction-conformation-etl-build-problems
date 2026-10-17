"""The fixed world behind the Watch register's first full reporting period.

Observatorio de Acao Coletiva, a Portuguese non-profit monitoring association. Its Vigilancia
Nacional register opened on 1 May 2026; the reporting period is 1 May to 30 October 2026 and the
record was extracted on 6 November 2026. Two actions in three reach the register only through the
press monitor, whose classifier assigns the action code. The coding desk double codes a batch of the
monitor's reports twice per reporting period, each round drawing from the reports that arrived since
the previous round closed, so the audited window is the opening of the period and the autumn
mobilisation that follows the surge has no audited reports in it.
"""
import datetime as dt

SEED = 248                                 # the action layer, measured in the design note
SEED_PACK = 599                             # a separate stream for reports, mess and the asks

ASSOCIATION = "Observatorio de Acao Coletiva"
REGISTER = "Vigilancia Nacional"
PEOPLE = {"officer": "Rafaela Carvalho",    # coding and methods desk
          "data": "Joel Branco"}            # data manager
# the desk's hand coders, by initials, with the share of each round's batch each one worked
CODERS = [("RC", 0.34), ("JB", 0.26), ("MM", 0.23), ("LS", 0.17)]

OPEN_DAY = dt.date(2026, 5, 1)
PERIOD_FROM = dt.date(2026, 5, 1)
PERIOD_TO = dt.date(2026, 10, 30)
EXTRACT = dt.date(2026, 11, 6)
TRUSTEES = dt.date(2026, 11, 19)
SURGE_FROM = dt.date(2026, 9, 5)
DST_BACK = dt.date(2026, 10, 25)            # summer time ends at 01:00 UTC
FORTNIGHT_DAYS = 14

# the mainland and Madeira keep one clock, the Azores run an hour behind it
OFFSET_MAINLAND = (1, 0)                    # (summer, winter) hours ahead of UTC
OFFSET_AZORES = (0, -1)
AZORES_DISTRICT = "Acores"


def offset_hours(district, utc_moment):
    """Hours the local clock of a district is ahead of UTC at a UTC moment."""
    summer = (utc_moment.date() < DST_BACK or
              (utc_moment.date() == DST_BACK and utc_moment.hour < 1))
    pair = OFFSET_AZORES if district == AZORES_DISTRICT else OFFSET_MAINLAND
    return pair[0] if summer else pair[1]


def fortnights():
    """Fourteen-day blocks from 1 May; the days left over at the end of the period go into the
    last block, which therefore has fifteen days (protocol 3.4)."""
    out, start, n = [], PERIOD_FROM, 1
    while start <= PERIOD_TO:
        end = min(start + dt.timedelta(days=FORTNIGHT_DAYS - 1), PERIOD_TO)
        if (PERIOD_TO - end).days < FORTNIGHT_DAYS:
            end = PERIOD_TO
        out.append(("Q%d" % n, start, end))
        start, n = end + dt.timedelta(days=1), n + 1
    return out


# dispute themes the protocol monitors. opens_on is the first day a theme can appear in the
# register: the autumn wave brings two disputes the register had not seen before.
THEMES = [
    ("TRM", "transporte rodoviario de mercadorias", 1.25, 1.20, None),
    ("AGR", "agricultura e pecuaria", 1.10, 1.05, None),
    ("SAU", "saude", 0.80, 0.70, None),
    ("EDU", "educacao", 0.70, 0.65, None),
    ("HAB", "habitacao", 1.05, 1.45, None),
    ("CVD", "combustiveis e custo de vida", 1.20, 1.00, None),
    ("PES", "pescas", 0.95, 0.90, None),
    ("SMU", "servicos municipais", 0.85, 0.80, None),
    ("AGU", "agua e saneamento", 0.45, 0.95, None),
    ("RES", "residuos e tratamento", 0.40, 1.10, None),
    ("PEN", "pensoes e seguranca social", 0.55, 0.60, None),
    ("ADM", "administracao publica", 0.60, 0.55, None),
    ("ENE", "energia e redes", 0.90, 0.85, SURGE_FROM),
    ("FLO", "florestas e fogos", 0.75, 0.75, SURGE_FROM),
]
SURGE_THEMES = ["TRM", "AGR", "CVD", "ENE", "FLO"]
LATE_THEMES = [t for t, _, _, _, o in THEMES if o is not None]

# the eight action codes, in the order the protocol prints them: the classifier confuses a code
# with its neighbours in that order far more often than with a distant one
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
CODE_MIX = {"CO": 26, "MA": 18, "BL": 24, "OC": 12, "PA": 20}
CONF_MIX = {"CF": 46, "RF": 30, "DP": 24}

ROUTES = [("IMP", "monitor de imprensa"),
          ("PAR", "rede de parceiros"),
          ("LIN", "linha de participacao publica")]

# how an action reaches the register
P_PRESS = 0.76          # the press monitor files a report on the action
P_PARTNER = 0.26        # a partner organisation files one, inside its own region
P_LINE = 0.17           # the public line receives one

# the press classifier. its two error rates are properties of the model, which was trained before
# the register opened and not retrained inside the period.
CLS_RECALL = 0.46       # confrontational actions it codes as confrontational
CLS_FALSE_MARK = 0.0295  # ordinary actions it codes as confrontational
CLS_DIAGONAL = 7.0      # weight on the code itself against its neighbours
CLS_DECAY = 1.15        # how fast the confusion falls away with distance in the code order
CLS_TRAINED = dt.date(2026, 3, 18)

# the share of actions that were confrontational falls across the period: the spring and summer
# disputes over evictions and road haulage were confrontational, the autumn mobilisation that
# trebles the volume is overwhelmingly peaceful
CONF_RATE_HI = 0.1480
CONF_RATE_LO = CONF_RATE_HI / 4.2
CONF_RAMP_FROM = dt.date(2026, 8, 9)
CONF_RAMP_TO = dt.date(2026, 9, 18)

# the coding desk's rounds: the close, the window of action dates the round drew from, and the size
SAMPLE_ROUNDS = [("R1", dt.date(2026, 6, 20), dt.date(2026, 5, 1), dt.date(2026, 6, 19), 420),
                 ("R2", dt.date(2026, 9, 10), dt.date(2026, 6, 20), dt.date(2026, 8, 31), 580)]
ADJUDICATED = 0.085     # share of coded rows a second coder looked at

PARTNERS = [
    ("P01", "Nucleo de Estudos do Trabalho do Minho", "Norte", 6.40),
    ("P02", "Associacao Civica do Mondego", "Centro", 5.95),
    ("P03", "Plataforma de Bairros da Margem Sul", "A.M. Lisboa", 7.25),
    ("P04", "Observatorio Rural do Alentejo Central", "Alentejo", 5.45),
    ("P05", "Liga dos Direitos do Barlavento", "Algarve", 6.75),
    ("P06", "Centro de Estudos Insulares", "Acores e Madeira", 8.15),
    ("P07", "Nucleo de Acompanhamento do Douro", "Norte", 6.40),
]
AMENDED = ("P04", dt.date(2026, 8, 1), 6.20)
MERGED = ("P07", "P12", dt.date(2026, 9, 10))

OUTLETS = [
    ("DNO", "Diario do Noroeste", ["Braga", "Viana do Castelo", "Porto"], 1.00),
    ("JLN", "Jornal do Litoral Norte", ["Porto", "Aveiro", "Braga"], 1.10),
    ("CBI", "Correio da Beira Interior", ["Viseu", "Guarda", "Castelo Branco"], 0.70),
    ("GMO", "Gazeta do Mondego", ["Coimbra", "Leiria", "Aveiro"], 0.85),
    ("CGL", "Correio da Grande Lisboa", ["Lisboa", "Setubal", "Santarem"], 1.25),
    ("DPL", "Diario da Planicie", ["Beja", "Evora", "Portalegre", "Setubal"], 0.80),
    ("NLS", "Noticiario do Litoral Sul", ["Faro"], 0.75),
    ("ATP", "Atlantico Diario", ["Acores", "Madeira"], 0.65),
    ("ATE", "Atlantico Daily", ["Acores", "Madeira"], 0.65),
    ("AGN", "Agencia Nacional de Noticias", ["*"], 1.40),
    ("SIN", "Servico Iberico de Noticias", ["*"], 0.55),
]
TWIN_FEED = ("ATP", "ATE")
REIMPORT_MONTH = (2026, 8)

ACTIONS_BASE, ACTIONS_SURGE = 18.0, 2.45    # actions a day, before and after the surge
# the register's own week: fewer actions at the weekend than on a working day
WEEKDAY_FACTOR = [1.14, 1.12, 1.10, 1.13, 1.08, 0.74, 0.52]

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
    "Acores": ["Angra do Heroismo", "Ponta Delgada", "Praia da Vitoria"],
    "Madeira": ["Funchal", "Machico", "Camara de Lobos"],
}
REGION_OF = {
    "Viana do Castelo": "Norte", "Braga": "Norte", "Porto": "Norte", "Vila Real": "Norte",
    "Braganca": "Norte", "Aveiro": "Centro", "Viseu": "Centro", "Guarda": "Centro",
    "Coimbra": "Centro", "Castelo Branco": "Centro", "Leiria": "Centro", "Santarem": "Centro",
    "Lisboa": "A.M. Lisboa", "Setubal": "A.M. Lisboa", "Portalegre": "Alentejo",
    "Evora": "Alentejo", "Beja": "Alentejo", "Faro": "Algarve", "Acores": "Acores e Madeira",
    "Madeira": "Acores e Madeira",
}
COASTAL = {"Viana do Castelo", "Porto", "Aveiro", "Leiria", "Lisboa", "Setubal", "Faro", "Acores",
           "Madeira"}

LOC_PREFIX = ["Sao Martinho", "Santa Marta", "Sao Miguel", "Santa Luzia", "Sao Bartolomeu",
              "Nossa Senhora da Graca", "Vila Nova", "Vila Cha", "Quinta do Lago", "Casal Novo",
              "Ribeira Brava", "Fonte Boa", "Alto da Serra", "Vale de Cambra", "Carvalhal",
              "Sobreiro", "Pinheiro Manso", "Varzea", "Lourical", "Cabeco da Vinha",
              "Barroca", "Azinhaga", "Lagoa Nova", "Monte Redondo", "Senhora da Hora"]
RENAMES = 14
# median minutes from the start of an action to the report, by route, and the shape of the spread
LAG_BASE = {"IMP": 112, "PAR": 652, "LIN": 94}
LAG_SIGMA = {"IMP": 0.62, "PAR": 0.46, "LIN": 0.70}


def confusion():
    """The classifier's code-to-code confusion: a strong diagonal, neighbours in the protocol's
    code order next, and exactly CLS_RECALL of the confrontational mass kept confrontational and
    CLS_FALSE_MARK of the ordinary mass pushed into it."""
    codes = [c for c, _, _ in ACTION_CODES]
    conf_idx = [i for i, (_, _, f) in enumerate(ACTION_CODES) if f]
    ord_idx = [i for i, (_, _, f) in enumerate(ACTION_CODES) if not f]
    out = {}
    for i, (code, _, is_conf) in enumerate(ACTION_CODES):
        w = [CLS_DIAGONAL if j == i else CLS_DECAY ** (-abs(i - j)) for j in range(len(codes))]
        mass_conf = CLS_RECALL if is_conf else CLS_FALSE_MARK
        row = [0.0] * len(codes)
        sc = sum(w[j] for j in conf_idx)
        so = sum(w[j] for j in ord_idx)
        for j in conf_idx:
            row[j] = mass_conf * w[j] / sc
        for j in ord_idx:
            row[j] = (1.0 - mass_conf) * w[j] / so
        out[code] = (codes, row)
    return out
