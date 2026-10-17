"""An independent read of the shipped bundle: nothing from the generator, its own code path.

Rebuilds the register day by day instead of event by event, walks the whole timeline rather than the
observed event times, and checks every figure in figures.json against what the files give.
"""
import csv
import datetime as dt
import json
import os

CONF = {"CF", "RF", "DP"}
QUIET = 21
P0, P1 = dt.date(2026, 5, 1), dt.date(2026, 10, 30)
EXTRACT = dt.date(2026, 11, 6)
DST = dt.date(2026, 10, 25)
PARTNER_RATE = {"P01": 6.40, "P02": 5.80, "P03": 7.10, "P04": 5.25, "P05": 6.75, "P06": 8.20,
                "P07": 6.40}
N = 0


def ok(label, cond, detail=""):
    global N
    N += 1
    if not cond:
        raise AssertionError("verify %s failed %s" % (label, detail))


def table(target, name):
    with open(os.path.join(target, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def to_local(moment, in_utc):
    if not in_utc:
        return moment
    shift = 1 if (moment + dt.timedelta(hours=1)).date() < DST else 0
    return moment + dt.timedelta(hours=shift)


def moment(s):
    s = s.strip().rstrip("Z").replace("T", " ")
    return dt.datetime(int(s[0:4]), int(s[5:7]), int(s[8:10]), int(s[11:13]), int(s[14:16]))


def run(target, figures):
    global N
    N = 0
    f = json.load(open(figures))
    place_to_loc, loc_to_muni = {}, {}
    for r in table(target, "gazeteiro_localidades.csv"):
        place_to_loc[r["nome"]] = r["codigo_localidade"]
        loc_to_muni[r["codigo_localidade"]] = r["codigo_municipio"]

    recs = []
    for r in table(target, "registo_itens_imprensa.csv"):
        if r["estado"] == "aceite":
            recs.append(("IMP", r["id_relato"], r["orgao"], r["tema"], r["codigo_acao"],
                         r["local_texto"], dt.date.fromisoformat(r["data_ocorrencia"]),
                         moment(r["inicio_acao"]), to_local(moment(r["carimbo_recepcao"]), True)))
    for r in table(target, "relatos_rede_parceiros.csv"):
        recs.append(("PAR", r["id_relato"], r["codigo_parceiro"], r["tema"], r["codigo_acao"],
                     r["local_texto"], dt.date.fromisoformat(r["data_ocorrencia"]),
                     moment(r["inicio_acao"]), to_local(moment(r["carimbo_entrega_utc"]), True)))
    for r in table(target, "relatos_linha_publica.csv"):
        recs.append(("LIN", r["id_relato"], "LIN", r["tema"], r["codigo_acao"], r["local_texto"],
                     dt.date.fromisoformat(r["data_ocorrencia"]), moment(r["inicio_acao"]),
                     to_local(moment(r["carimbo_recepcao"]), False)))

    # the protocol's action grain, reached from the other side: a set of keys
    seen_action, routes_of, codes_of = {}, {}, {}
    for route, ident, src, theme, code, place, day, start, recv in recs:
        loc = place_to_loc.get(place)
        if loc is None:
            continue
        key = (theme, loc, day)
        seen_action[key] = loc_to_muni[loc]
        routes_of.setdefault(key, set()).add(route)
        codes_of.setdefault(key, set()).add(code)
    ok("actions", len(seen_action) > 0)

    # the register, walked day by day inside each municipality and theme
    tracks = {}
    for (theme, loc, day), muni in seen_action.items():
        tracks.setdefault((muni, theme), []).append((day, codes_of[(theme, loc, day)]))
    episodes = []
    for (muni, theme), days in tracks.items():
        days.sort()
        open_day, last, conf = None, None, None
        for day, codes in days:
            if open_day is None or (day - last).days > QUIET:
                if open_day is not None:
                    episodes.append((open_day, last, conf))
                open_day, last, conf = day, day, None
            last = day
            if codes & CONF and conf is None:
                conf = day
        if open_day is not None:
            episodes.append((open_day, last, conf))
    cohort = [e for e in episodes if P0 <= e[0] <= P1]
    ok("cohort", len(cohort) == f["cohort_episodes"], "%d" % len(cohort))

    rows = []
    for open_day, last, conf in cohort:
        if conf is not None:
            rows.append(((conf - open_day).days, 1))
        elif (EXTRACT - last).days >= QUIET:
            rows.append(((last - open_day).days, 2))
        else:
            rows.append(((EXTRACT - open_day).days, 0))
    n = len(rows)
    rec = sum(1 for t, c in rows if c == 1)
    closed = sum(1 for t, c in rows if c == 2)
    ok("recorded", rec == f["recorded_confrontational"], "%d" % rec)
    ok("closed", closed == f["closed_without"], "%d" % closed)
    ok("open", n - rec - closed == f["still_open"])

    # walk every day of the timeline, not only the days something happened
    horizon = max(t for t, c in rows)
    surv, cum, prod = 1.0, 0.0, 1.0
    for t in range(0, horizon + 1):
        at_risk = sum(1 for tt, c in rows if tt >= t)
        d1 = sum(1 for tt, c in rows if tt == t and c == 1)
        d2 = sum(1 for tt, c in rows if tt == t and c == 2)
        if at_risk and (d1 or d2):
            cum += surv * d1 / at_risk
            prod *= 1.0 - d1 / at_risk
            surv *= 1.0 - (d1 + d2) / at_risk
    ok("call.rate", round(100 * cum) == f["call_rate_pct"], "%.4f" % (100 * cum))
    ok("call.episodes", round(cum * n) == f["call_episodes"], "%.4f" % (cum * n))
    ok("call.raw", abs(cum * n - f["raw_episodes"]) < 0.01, "%.4f" % (cum * n))
    ok("rung0", rec == f["rung0_episodes"] and round(100 * rec / n) == f["rung0_pct"])
    ok("rung1", round(rec / (rec + closed) * n) == f["rung1_episodes"]
       and round(100 * rec / (rec + closed)) == f["rung1_pct"])
    ok("rung2", round((1 - prod) * n) == f["rung2_episodes"]
       and round(100 * (1 - prod)) == f["rung2_pct"])
    ok("ladder.order", rec < cum * n < rec / (rec + closed) * n < (1 - prod) * n)

    # the fortnights the protocol counts from 1 May, the last ending with the period
    bounds, start, k = [], P0, 1
    while start <= P1:
        end = min(start + dt.timedelta(days=13), P1)
        if (P1 - end).days < 7:
            end = P1
        bounds.append(("Q%d" % k, start, end))
        start, k = end + dt.timedelta(days=1), k + 1
    ok("fortnights", len(bounds) == len(f["fortnights"]))
    total_actions = 0
    for label, a, b in bounds:
        inside = [key for key in seen_action if a <= key[2] <= b]
        exp = f["fortnights"][label]
        ok("a1.%s.actions" % label, len(inside) == exp["actions"], "%d" % len(inside))
        ok("a1.%s.muni" % label, len({seen_action[k2] for k2 in inside}) == exp["municipalities"])
        par = [k2 for k2 in inside if "PAR" in routes_of[k2]]
        share = round(100.0 * len(par) / len(inside), 1)
        ok("a1.%s.share" % label, abs(share - exp["partner_share_pct"]) < 0.051, "%.1f" % share)
        conf = [k2 for k2 in inside if codes_of[k2] & CONF]
        ok("a1.%s.conf" % label, len(conf) == exp["confrontational_actions"])
        total_actions += len(inside)
    ok("a1.total", total_actions == f["actions_in_period"])

    # the routes
    exc = table(target, "excecoes_geocodificacao.csv")
    for route in ("IMP", "PAR", "LIN"):
        placed, ids = [], set()
        for r in recs:
            if r[0] != route or r[1] in ids:
                continue
            ids.add(r[1])
            if P0 <= r[8].date() <= P1 and place_to_loc.get(r[5]):
                placed.append(r)
            elif P0 <= r[8].date() <= P1:
                placed.append(r)
        unplaceable = [e for e in exc
                       if e["via"] == route and P0 <= moment(e["carimbo_recepcao"]).date() <= P1]
        got = f["routes"][route]
        ok("a2.%s.received" % route, len(placed) + len(unplaceable) == got["received"],
           "%d" % (len(placed) + len(unplaceable)))
        ok("a2.%s.unplaceable" % route, len(unplaceable) == got["unplaceable"])
        mins = sorted((r[8] - r[7]).total_seconds() / 60.0 for r in placed)
        mid = (mins[len(mins) // 2] if len(mins) % 2 else
               (mins[len(mins) // 2 - 1] + mins[len(mins) // 2]) / 2.0)
        ok("a2.%s.median" % route, abs(mid - got["median_minutes"]) < 0.051, "%.1f" % mid)

    # the partners
    first = {}
    for r in recs:
        if r[0] == "PAR":
            first.setdefault(r[1], r)
    for code, rate in sorted(PARTNER_RATE.items()):
        mine = [r for r in first.values()
                if (r[2] if r[2] in PARTNER_RATE else "P07") == code and P0 <= r[6] <= P1]
        late = [r for r in mine if r[8].date() > P1]
        euros = 0.0
        for r in mine:
            if r[8].date() > P1:
                continue
            use = rate
            if code == "P04" and r[8].date() >= dt.date(2026, 8, 1):
                use = 6.15
            euros += use
        got = f["partners"][code]
        ok("a3.%s.filed" % code, len(mine) == got["filed"], "%d" % len(mine))
        ok("a3.%s.late" % code, len(late) == got["after_close"])
        ok("a3.%s.euros" % code, round(euros) == got["euros"], "%.2f" % euros)

    # the input gates, read off the bundle
    files = sorted(os.listdir(target))
    ok("gate.files", len(files) >= 10, "%d" % len(files))
    ok("gate.formats", len({os.path.splitext(x)[1] for x in files}) >= 3)
    big = max(sum(1 for _ in open(os.path.join(target, x), encoding="utf-8")) - 1
              for x in files if x.endswith(".csv"))
    ok("gate.bulk", big >= 25000, "%d" % big)
    return N
