"""Constants for task270 architecture 6: Associação Gota Viva's spring 2027 television campaign for young donors,
the audience panel's four reference weeks of March 2026, the channels, the people, the dates and the pack's files."""
import datetime as dt
from decimal import Decimal, ROUND_HALF_UP

SEED = 4
REF_START = dt.date(2026, 3, 2)            # Monday; the four reference weeks run to Sunday 29 March 2026
NDAYS = 28
REF_DAYS = [REF_START + dt.timedelta(d) for d in range(NDAYS)]
DST_DAY = 27                               # 29 March 2026: clocks go forward at 01:00 UTC (02:00 to 03:00 local)
TV_DAY_START = 120                         # the panel's day runs 02:00 to 26:00 local
CAMPAIGN_START = dt.date(2027, 4, 5)       # Monday; campaign week n is read in reference week n
RENAME_DAY = 14                            # 16 March 2026: Pulsar becomes Pulsar+ (code PLSP)
PANEL_DELIVERED = dt.date(2026, 4, 14)
RATES_ISSUED = dt.date(2026, 10, 15)
BRIEF_DATE = dt.date(2026, 10, 28)
SCHEDULES_DATE = dt.date(2026, 11, 17)
ASSEMBLED = dt.datetime(2026, 11, 24, 10, 15)
DECISION_DATE = dt.date(2026, 12, 2)
BOOKING_DEADLINE = dt.date(2026, 12, 11)
BUDGET = 230000
ROS_DISCOUNT = 0.37
PREMIUM = {"FP": 1.15, "LP": 1.10, "FIX": 1.00}
CPM_YOUNG = 62.0                           # euros per thousand adults 18 to 34 at a break's first place
ARENA_PREMIUM = 1.35
UNIVERSE_YOUNG = 2104000
UNIVERSE_ADULT = 8712000

ORG = "Associação Gota Viva"
ORG_SHORT = "Gota Viva"
AGENCY = "Meridiano Media"
PANEL_CO = "Audimetria Lusa"
JIC = "Comissão de Audiometria"
REQUESTER = "Lara Gomes"          # Gota Viva, head of donor marketing
PLANNER = "Helena Gaspar"         # Meridiano Media, planning director
PANEL_CONTACT = "Dinis Vaz"       # Audimetria Lusa, client methods

# channel code, name, sales house
CHANNELS = [("FAR1", "Farol", "Farol Publicidade"), ("FAR2", "Farol 2", "Farol Publicidade"),
            ("VRT", "Vértice", "Vértice Comercial"), ("LIT", "Litoral", "Litoral Media Vendas"),
            ("PLS", "Pulsar", "Litoral Media Vendas"), ("ARN", "Arena", "Arena Desporto Media")]
CH = [c[0] for c in CHANNELS]
CH_NAME = {c[0]: c[1] for c in CHANNELS}
SALES = {c[0]: c[2] for c in CHANNELS}
NEW_CODE = {"PLS": "PLSP"}
NEW_NAME = {"PLS": "Pulsar+"}

# windows of the day by channel (minutes from midnight of the panel day, local); a rotation spot is placed
# by the channel anywhere in its window
WINDOWS = {"day": (420, 1020), "access": (1020, 1200), "prime": (1200, 1470), "late": (1470, 1560)}
WINDOW_NAME = {"day": "Dia (07:00-17:00)", "access": "Acesso (17:00-20:00)", "prime": "Horário nobre (20:00-00:30)",
               "late": "Noite (00:30-02:00)"}

AGE_BANDS = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
YOUNG = ("18-24", "25-34")
REGIONS = ["Norte", "Centro", "Área Metropolitana de Lisboa", "Alentejo", "Algarve"]

FILES = dict(
    viewing="audimetria_visionamentos_2026-03.csv",
    panel="audimetria_individuos_2026-03.csv",
    asrun="emissao_publicitaria_2026-03.csv",
    bookings="reservas_publicidade_2026-03.csv",
    epg="grelha_programacao_2026-03.csv",
    channels="canais_codigos.csv",
    universe="universo_2026.csv",
    ratings="audiencias_programas_semanais_2026-03.csv",
    schedules="esquemas_campanha_2027.xlsx",
    rates="tabelas_precos_2T2027.pdf",
    brief="briefing_campanha_jovens_2027.pdf",
    method="audimetria_nota_metodologica.pdf",
    digital="plano_digital_2027.csv",
    donors="dadores_novos_2025.csv",
    dictionary="dicionario_dados.csv",
    portal="marcacoes_portal_dador_2025.csv",
    portal_notes="notas_extracao_portal_dador.txt",
    report2025="relatorio_campanha_jovens_2025.pdf",
)
DISTRACTORS = ["digital", "donors"]
BOOK = "plano_tv_jovens_2027.xlsx"
DECK = "recomendacao_esquema_tv_2027.pptx"
SCHED = ["A", "B", "C"]
SCHED_NAME = {"A": "Esquema A, primeiro lugar no horário nobre jovem",
              "B": "Esquema B, rotação em horário nobre",
              "C": "Esquema C, desporto e noite, último lugar"}


def r(x, n=0):
    """half-up rounding at n decimals"""
    return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP))


def pct(x, n=1):
    return r(100 * x, n)
