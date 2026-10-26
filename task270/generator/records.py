"""The pack's data files for task270, each in its own system's layout: the audience panel's viewing statements and
member file (Audimetria Lusa, UTC), the channels' as-run log of commercial spots and programme grid (local time, the
panel day from 02:00), the channel code list, the 2026 universe estimates, the Comissão de Audiometria's weekly
programme audiences, Meridiano Media's three draft schedules, Gota Viva's 2027 digital plan and its 2025 new-donor
counts."""
import csv
import datetime as dt
import hashlib

import numpy as np

import common as K

T0 = dt.datetime.combine(K.REF_START, dt.time(0, 0))
WEST_FROM = K.DST_DAY * 86400 + 120 * 60            # 29 March 2026, 02:00 local summer time = 01:00 UTC
WEEKDAY = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
SECTORS = ["Alimentação", "Bebidas", "Telecomunicações", "Automóvel", "Banca e seguros", "Distribuição",
           "Higiene e beleza", "Saúde e farmácia", "Lazer e turismo", "Media e entretenimento", "Serviços públicos",
           "Casa e decoração", "Vestuário", "Energia"]


BOOK_FMT = {"Farol Publicidade": "AP-%06d", "Vértice Comercial": "VC26.%05d", "Litoral Media Vendas": "LMV/26/%06d",
            "Arena Desporto Media": "ADM%07d"}
BOOK_START = {"Farol Publicidade": 3100, "Vértice Comercial": 12405, "Litoral Media Vendas": 50232,
              "Arena Desporto Media": 880}
LABEL = {"FP": "1.º LUGAR", "LP": "ÚLTIMO LUGAR", "FIX": "FIXO", "ROS": "ROTAÇÃO", "PROMO": "AUTOPROMOÇÃO"}


def write_csv(path, head, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(head)
        w.writerows(rows)


def local(s):
    return T0 + dt.timedelta(seconds=int(s))


def utc(s):
    return T0 + dt.timedelta(seconds=int(s) - (3600 if s >= WEST_FROM else 0))


def tvday(s):
    """the panel day of a local wall-clock second: the day runs from 02:00 to 26:00"""
    return (int(s) - 7200) // 86400


def code(ch, day):
    return K.NEW_CODE.get(ch, ch) if day >= K.RENAME_DAY else ch


def name(ch, day):
    return K.NEW_NAME.get(ch, K.CH_NAME[ch]) if day >= K.RENAME_DAY else K.CH_NAME[ch]


def hid(prefix, n, salt, width):
    h = int(hashlib.sha1(("%s|%d" % (salt, n)).encode()).hexdigest()[:8], 16)
    return "%s%0*d" % (prefix, width, h % (10 ** width))


class Records:
    def __init__(self, w):
        self.w = w
        n = len(w.age)
        ids, used = [], set()
        for i in range(n):
            k = 0
            while True:
                x = hid("I", i * 7 + k, "membro", 5)
                if x not in used:
                    break
                k += 1
            used.add(x)
            ids.append(x)
        self.mid = ids
        hids, usedh = {}, set()
        for h in sorted(set(w.hh.tolist())):
            k = 0
            while True:
                x = hid("L", h * 5 + k, "lar", 4)
                if x not in usedh:
                    break
                k += 1
            usedh.add(x)
            hids[h] = x
        self.hid = hids
        rng = np.random.default_rng(31)
        self.adv = ["A%04d" % int(x) for x in rng.choice(np.arange(100, 9999), 340, replace=False)]
        self.adv_sector = {a: SECTORS[int(rng.integers(0, len(SECTORS)))] for a in self.adv}
        self.adv_of = {}
        for b in w.breaks:
            for s in b["spots"]:
                self.adv_of[(b["bid"], s["pos"])] = self.adv[int(rng.integers(0, len(self.adv)))]
        # the sales houses' booking numbers, issued in order of booking date
        rng2 = np.random.default_rng(37)
        items = []
        for b in w.breaks:
            for s in b["spots"]:
                if s["kind"] == "PROMO":
                    continue
                day = s["booked"][0] if s["kind"] == "ROS" else b["day"]
                lead = int(rng2.integers(2, 45)) if s["kind"] == "ROS" else int(rng2.integers(4, 64))
                items.append((K.SALES[b["ch"]], K.REF_DAYS[day] - dt.timedelta(days=lead), float(rng2.random()), b, s,
                              day))
        items.sort(key=lambda x: (x[0], x[1], x[2]))
        seq = {}
        self.bk = {}
        for house, bdate, _, b, s, day in items:
            n = seq.get(house, BOOK_START[house]) + 1
            seq[house] = n
            self.bk[(b["bid"], s["pos"])] = dict(house=house, ref=BOOK_FMT[house] % n, date=bdate, day=day, b=b, s=s)

    # ---------------------------------------------------------------- panel
    def panel_rows(self):
        w = self.w
        rows = []
        for i in range(len(w.age)):
            days = K.NDAYS - len(w.out_days.get(i, ()))
            rows.append([self.mid[i], self.hid[int(w.hh[i])], w.sex[i], w.age[i], w.region[i],
                         "%.1f" % w.wt[i], days])
        rows.sort(key=lambda r: (r[1], r[0]))
        return ["id_individuo", "id_lar", "sexo", "escalao_etario", "regiao", "peso_28d", "dias_em_amostra"], rows

    def viewing_rows(self):
        w = self.w
        rows = []
        for (i, c, s0, s1) in w.live.tolist():
            rows.append((self.hid[int(w.hh[i])], self.mid[i], code(K.CH[c], tvday(s0)), s0, s1, s0, "AO VIVO", "N"))
        for (i, c, s0, s1, b0) in w.play.tolist():
            rows.append((self.hid[int(w.hh[i])], self.mid[i], code(K.CH[c], tvday(b0)), s0, s1, b0, "DIFERIDO", "N"))
        for (h, c, s0, s1) in w.guests:
            rows.append((self.hid[h], self.hid[h] + "-C1", code(K.CH[c], tvday(s0)), s0, s1, s0, "AO VIVO", "S"))
        rows.sort(key=lambda r: (r[0], r[1], r[3], r[2]))
        out = []
        f = "%Y-%m-%dT%H:%M:%SZ"
        for (lar, ind, ch, s0, s1, b0, modo, conv) in rows:
            out.append([lar, ind, K.REF_DAYS[tvday(s0)].isoformat(), ch, utc(s0).strftime(f), utc(s1).strftime(f),
                        utc(b0).strftime(f), modo, conv])
        return ["id_lar", "id_individuo", "dia_tv", "canal", "inicio_utc", "fim_utc", "emissao_utc", "modo",
                "convidado"], out

    # ---------------------------------------------------------------- as-run log and grid
    def asrun_rows(self):
        w = self.w
        rows = []
        seq = {}
        for b in sorted(w.breaks, key=lambda x: (x["ch"], x["t0"])):
            d = b["day"]
            k = seq.get((b["ch"], d), 0) + 1
            seq[(b["ch"], d)] = k
            brk = "%s-%s-%03d" % (code(b["ch"], d), K.REF_DAYS[d].strftime("%Y%m%d"), k)
            for s in b["spots"]:
                lt = local(s["t0"])
                if s["kind"] == "PROMO":
                    adv, sector, ref = "", "", ""
                else:
                    adv = self.adv_of[(b["bid"], s["pos"])]
                    sector, ref = self.adv_sector[adv], self.bk[(b["bid"], s["pos"])]["ref"]
                rows.append([code(b["ch"], d), name(b["ch"], d), K.REF_DAYS[d].isoformat(), lt.date().isoformat(),
                             lt.strftime("%H:%M:%S"), brk, b["title"], b["no"], s["pos"], b["n"], s["t1"] - s["t0"],
                             adv, sector, LABEL[s["kind"]], ref])
        return ["canal", "nome_canal", "dia_tv", "data", "hora_inicio", "id_intervalo", "programa",
                "intervalo_no_programa", "posicao", "spots_no_intervalo", "duracao_s", "anunciante", "setor",
                "colocacao", "id_reserva"], rows

    def booking_rows(self):
        """the sales houses' bookings for the reference weeks: what was sold, for which day and on what terms"""
        rows = []
        for (bid, pos), k in self.bk.items():
            b, s, day = k["b"], k["s"], k["day"]
            if s["kind"] == "ROS":
                prog, brk, win = "", "", K.WINDOW_NAME[s["booked"][2]]
            else:
                prog, brk, win = b["title"], b["no"], ""
            rows.append([k["house"], k["ref"], k["date"].isoformat(), self.adv_of[(bid, pos)], code(b["ch"], day),
                         K.REF_DAYS[day].isoformat(), LABEL[s["kind"]], prog, brk, win, s["t1"] - s["t0"]])
        rows.sort(key=lambda r: (r[0], r[1]))
        return ["casa_comercial", "id_reserva", "data_reserva", "anunciante", "canal", "dia_tv", "colocacao", "programa",
                "intervalo_no_programa", "janela", "duracao_s"], rows

    def epg_rows(self):
        w = self.w
        genre = {"reality": "Entretenimento", "drama": "Ficção", "football": "Desporto", "sporttalk": "Desporto",
                 "series": "Ficção", "comedy": "Entretenimento", "talk": "Entretenimento", "news": "Informação",
                 "magazine": "Entretenimento", "game": "Concurso", "film": "Cinema", "music": "Música",
                 "docs": "Documentário", "sport": "Desporto", "kids": "Infantil", "sitcom": "Ficção"}
        rows = []
        for pr in sorted(w.progs, key=lambda x: (x["ch"], x["t0"])):
            d = pr["day"]
            rows.append([code(pr["ch"], d), name(pr["ch"], d), K.REF_DAYS[d].isoformat(), pr["title"],
                         genre[pr["genre"]], local(pr["t0"]).strftime("%Y-%m-%d %H:%M"),
                         local(pr["t1"]).strftime("%Y-%m-%d %H:%M")])
        return ["canal", "nome_canal", "dia_tv", "programa", "genero", "inicio", "fim"], rows

    def channel_rows(self):
        rows = []
        for c, n, s in K.CHANNELS:
            if c in K.NEW_CODE:
                rows.append([c, n, s, "2019-09-01", "2026-03-15"])
                rows.append([K.NEW_CODE[c], K.NEW_NAME[c], s, "2026-03-16", ""])
            else:
                rows.append([c, n, s, "2004-01-01" if c != "ARN" else "2011-08-12", ""])
        return ["codigo", "nome", "comercializacao", "em_vigor_desde", "em_vigor_ate"], rows

    def universe_rows(self):
        rows = [[a, s, g, v] for (a, s, g), v in sorted(self.w.universe.items())]
        return ["escalao_etario", "sexo", "regiao", "populacao"], rows

    def ratings_rows(self):
        """the Comissão's weekly programme audiences: average audience over each programme's airings (thousands)"""
        w = self.w
        acc = {}
        for pr in w.progs:
            wk = pr["day"] // 7 + 1
            secs = w.seconds(pr["ch"], pr["t0"], pr["t1"])
            dur = pr["t1"] - pr["t0"]
            yng = sum(w.wt[i] * v for i, v in secs.items() if w.young[i]) / dur
            adl = sum(w.wt[i] * v for i, v in secs.items()) / dur
            k = (wk, pr["ch"], pr["title"])
            a = acc.setdefault(k, [0, 0.0, 0.0])
            a[0] += 1
            a[1] += yng
            a[2] += adl
        rows = []
        for (wk, ch, title), (n, y, a) in sorted(acc.items()):
            if ch in ("FAR2",) and a / n < 40000:
                continue
            day = (wk - 1) * 7
            rows.append(["2026-S%02d" % (9 + wk), code(ch, day + 6), title, n, "%.1f" % (y / n / 1000),
                         "%.2f" % (100 * y / n / K.UNIVERSE_YOUNG), "%.1f" % (a / n / 1000),
                         "%.2f" % (100 * a / n / K.UNIVERSE_ADULT)])
        return ["semana", "canal", "programa", "emissoes", "audiencia_media_18_34_milhares", "rat_18_34_pct",
                "audiencia_media_adultos_milhares", "rat_adultos_pct"], rows

    # ---------------------------------------------------------------- schedules
    def schedule_lines(self, s):
        out = []
        for ln in self.w.sched[s]:
            date = K.CAMPAIGN_START + dt.timedelta(days=7 * (ln["week"] - 1) + ln["wd"])
            if ln["kind"] == "ROS":
                prog, brk, place = "Rotação %s" % K.WINDOW_NAME[ln["brk"]].lower(), None, "Rotação"
            else:
                prog, brk = ln["title"], ln["brk"]
                place = "1.º lugar no intervalo" if ln["kind"] == "FP" else "Último lugar no intervalo"
            out.append([ln["week"], date.isoformat(), WEEKDAY[date.weekday()], K.CH_NAME[ln["ch"]] if ln["ch"] != "PLS"
                        else "Pulsar+", prog, brk, place, 30, ln["price"]])
        return out

    # ---------------------------------------------------------------- distractors and context
    def digital_rows(self):
        rows = [["YouTube", "TrueView in-stream", "2027-04-05", "2027-05-02", "18-34", 4200000, 0.011, 38500],
                ["Instagram", "Reels", "2027-04-05", "2027-05-02", "18-34", 3600000, 0.0068, 21800],
                ["TikTok", "In-feed", "2027-04-12", "2027-05-02", "18-24", 5100000, 0.0042, 19600],
                ["Spotify", "Audio 30s", "2027-04-05", "2027-04-25", "18-34", 1250000, 0.0095, 9800],
                ["Meta", "Lead form (inscrição)", "2027-04-19", "2027-05-16", "18-44", 900000, 0.0185, 14200]]
        return ["plataforma", "formato", "inicio", "fim", "publico", "impressoes_previstas", "cpm_eur_por_impressao",
                "orcamento_eur"], rows

    def donor_rows(self):
        rng = np.random.default_rng(55)
        base = {"18-24": 0.21, "25-34": 0.24, "35-44": 0.2, "45-54": 0.17, "55-64": 0.13, "65+": 0.05}
        rows = []
        for g, gw in zip(K.REGIONS, [0.33, 0.24, 0.29, 0.06, 0.08]):
            for a, aw in base.items():
                for s in ("F", "M"):
                    n = int(round(14630 * gw * aw * (0.54 if s == "F" else 0.46) * float(np.exp(rng.normal(0, 0.08)))))
                    rows.append([2025, g, a, s, n])
        return ["ano", "regiao", "escalao_etario", "sexo", "novos_dadores"], rows
