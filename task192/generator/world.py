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
SEED_DESK = 1                               # the coding desk's own stream: its calendar and its draw

ASSOCIATION = "Observatorio de Acao Coletiva"
REGISTER = "Vigilancia Nacional"
PEOPLE = {"officer": "Rafaela Carvalho",    # coding and methods desk
          "data": "Joel Branco"}            # data manager
# The desk's hand coders. `sits` is how often the coder is on the rota, `pace` how many reports a
# sitting gets through, and `style` how often the coder reads an ambiguous report as a neighbouring
# code of the same kind: concentracao against marcha, bloqueio against paralisacao. The protocol's
# confrontation classes (2.2) are the one boundary it defines sharply, so a coder's own style never
# crosses it.
CODERS = [("RC", 0.86, 1.22, 0.07), ("JB", 0.63, 1.00, 0.17),
          ("MM", 0.58, 0.88, 0.22), ("LS", 0.41, 0.95, 0.11)]
CODER_PACE = [2, 3, 4, 5, 6, 7, 9, 11, 13, 16, 19, 23]
CODER_PACE_W = [7, 9, 11, 12, 11, 10, 9, 8, 7, 6, 6, 4]
# the share of a sitting's working days the desk actually sat with a batch, by month: August is the
# association's holiday month and the desk thins out rather than stopping
DESK_WORKED = {5: 0.72, 6: 0.78, 7: 0.70, 8: 0.38, 9: 0.80}
DESK_SATURDAY = 0.09
DESK_SIT = 0.85         # how much of a coder's rota share is a sitting on a day the desk worked
# a second coder reads a report when the first coder flags it, which happens far more often on the
# ambiguous reports the classifier also tends to get wrong
ADJ_AGREE = 0.052
ADJ_DISAGREE = 0.44
ADJ_CHANGED_AGREE = 0.13
ADJ_CHANGED_DISAGREE = 0.52
UNCODABLE = 0.011                           # reports the desk could not fix a code for at all
NOTE_REVIEWED = 0.55                        # reviewed rows the coder left a note on

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
CLS_DECAY = 1.95        # how fast the confusion falls away with distance in the code order
CLS_TRAINED = dt.date(2026, 3, 18)

# the share of actions that were confrontational falls across the period: the spring and summer
# disputes over evictions and road haulage were confrontational, the autumn mobilisation that
# trebles the volume is overwhelmingly peaceful
CONF_RATE_HI = 0.1674
CONF_RATE_LO = CONF_RATE_HI / 4.2
CONF_RAMP_FROM = dt.date(2026, 8, 9)
CONF_RAMP_TO = dt.date(2026, 9, 18)

# the coding desk's rounds: the close, the window of action dates the round drew from, and the size
# the coding desk's rounds: the close, the window of action dates the round drew from, and the day
# the desk opened the batch, which is the day after the previous round closed
SAMPLE_ROUNDS = [("R1", dt.date(2026, 6, 20), dt.date(2026, 5, 1), dt.date(2026, 6, 19),
                  dt.date(2026, 5, 4)),
                 ("R2", dt.date(2026, 9, 10), dt.date(2026, 6, 20), dt.date(2026, 8, 31),
                  dt.date(2026, 6, 22))]

PARTNERS = [
    ("P01", "Nucleo de Estudos do Trabalho do Minho", "Norte", 6.35),
    ("P02", "Associacao Civica do Mondego", "Centro", 5.95),
    ("P03", "Plataforma de Bairros da Margem Sul", "A.M. Lisboa", 7.20),
    ("P04", "Observatorio Rural do Alentejo Central", "Alentejo", 5.45),
    ("P05", "Liga dos Direitos do Barlavento", "Algarve", 6.90),
    ("P06", "Centro de Estudos Insulares", "Acores e Madeira", 8.10),
    ("P07", "Nucleo de Acompanhamento do Douro", "Norte", 6.10),
]
AMENDED = ("P04", dt.date(2026, 8, 1), 6.30)
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

# Where the register's contention stands before the autumn. The industrial belt and the two metro
# areas carry most of it and the interior districts carry little, so the spring and summer months
# never touch every municipality in the gazetteer.
DISTRICT_INTENSITY = {
    "Lisboa": 2.00, "Porto": 1.90, "Setubal": 1.60, "Braga": 1.20, "Aveiro": 1.10,
    "Leiria": 0.95, "Faro": 0.90, "Coimbra": 0.85, "Santarem": 0.80, "Viana do Castelo": 0.50,
    "Viseu": 0.34, "Evora": 0.30, "Beja": 0.27, "Vila Real": 0.26, "Castelo Branco": 0.24,
    "Guarda": 0.19, "Portalegre": 0.19, "Braganca": 0.14, "Acores": 0.28, "Madeira": 0.24,
}
DISTRICT_GROUP = {
    "Lisboa": "metro", "Setubal": "metro", "Porto": "metro", "Braga": "metro",
    "Viana do Castelo": "litoral", "Aveiro": "litoral", "Coimbra": "litoral",
    "Leiria": "litoral", "Santarem": "litoral", "Faro": "litoral",
    "Vila Real": "interior", "Braganca": "interior", "Viseu": "interior", "Guarda": "interior",
    "Castelo Branco": "interior", "Portalegre": "interior", "Evora": "interior", "Beja": "interior",
    "Acores": "ilhas", "Madeira": "ilhas",
}
# which territory each dispute falls on. The two themes the autumn brings are disputes over the
# transmission network and over the fire season, and both of them are interior disputes, so the
# mobilisation reaches ground the first four months of the register never did.
THEME_GROUND = {
    "TRM": {"metro": 1.30, "litoral": 1.30, "interior": 0.55, "ilhas": 0.15},
    "AGR": {"metro": 0.30, "litoral": 1.05, "interior": 2.10, "ilhas": 0.80},
    "SAU": {"metro": 0.90, "litoral": 1.00, "interior": 1.25, "ilhas": 1.10},
    "EDU": {"metro": 1.10, "litoral": 1.00, "interior": 0.85, "ilhas": 0.90},
    "HAB": {"metro": 2.20, "litoral": 0.80, "interior": 0.22, "ilhas": 0.95},
    "CVD": {"metro": 1.05, "litoral": 1.00, "interior": 0.95, "ilhas": 1.00},
    "PES": {"metro": 1.00, "litoral": 1.40, "interior": 0.00, "ilhas": 1.90},
    "SMU": {"metro": 1.05, "litoral": 1.00, "interior": 0.95, "ilhas": 1.05},
    "AGU": {"metro": 0.65, "litoral": 1.00, "interior": 1.70, "ilhas": 1.20},
    "RES": {"metro": 1.40, "litoral": 1.10, "interior": 0.55, "ilhas": 0.85},
    "PEN": {"metro": 0.95, "litoral": 1.00, "interior": 1.30, "ilhas": 1.05},
    "ADM": {"metro": 1.25, "litoral": 1.00, "interior": 1.10, "ilhas": 1.00},
    "ENE": {"metro": 0.35, "litoral": 0.85, "interior": 2.80, "ilhas": 0.55},
    "FLO": {"metro": 0.18, "litoral": 0.95, "interior": 3.20, "ilhas": 0.45},
}
# how much of a district's contention each of its municipalities carries: the district capital most,
# a long tail of small ones that the register reaches only when the volume rises
MUNI_SIZE = [1.00, 0.42, 0.68, 0.22, 1.35, 0.30, 0.85, 0.16, 0.55, 0.25, 1.10, 0.36]
CAPITAL_SIZE = 2.30

LOC_PREFIX = ["Sao Martinho", "Santa Marta", "Sao Miguel", "Santa Luzia", "Sao Bartolomeu",
              "Nossa Senhora da Graca", "Vila Nova", "Vila Cha", "Quinta do Lago", "Casal Novo",
              "Ribeira Brava", "Fonte Boa", "Alto da Serra", "Vale de Cambra", "Carvalhal",
              "Sobreiro", "Pinheiro Manso", "Varzea", "Lourical", "Cabeco da Vinha",
              "Barroca", "Azinhaga", "Lagoa Nova", "Monte Redondo", "Senhora da Hora"]
RENAMES = 14
# median minutes from the start of an action to the report, by route, and the shape of the spread
LAG_BASE = {"IMP": 112, "PAR": 652, "LIN": 94}
LAG_SIGMA = {"IMP": 0.62, "PAR": 0.46, "LIN": 0.70}

# The hour an action starts, by the route that reported it. The three routes see different hours of
# the day: the press monitor's titles cover the set-piece daytime actions, a partner organisation
# writes up what its own people were at during their working day, and the public line is where the
# evening and night-time blockades and occupations arrive, often from a passer-by.
START_HOURS = {
    "IMP": [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
    "PAR": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    "LIN": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
}
START_WEIGHTS = {
    "IMP": [2, 7, 11, 14, 11, 5, 4, 12, 13, 10, 7, 4, 2, 1, 1],
    "PAR": [5, 12, 14, 12, 7, 6, 11, 13, 10, 6, 3, 1, 1],
    "LIN": [1, 2, 3, 4, 5, 5, 4, 3, 3, 5, 6, 7, 9, 11, 12, 10, 7, 5, 3],
}


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
