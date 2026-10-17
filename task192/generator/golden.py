"""Everything the bulletin owes, computed from the shipped bundle and nothing else.

The register is rebuilt from the three access routes the way the protocol says, the period's cohort
of dispute episodes is taken off it, and the confrontation rate is estimated four ways: the episodes
that have already recorded a confrontational action, the share among the episodes whose outcome is
known, a product-limit survival of the time to a confrontational action, and the cumulative share
with a quiet close treated as the other way an episode ends.
"""
import csv
import datetime as dt
import json
import os
import statistics

import world as W

CONF = set(W.CONFRONTATIONAL)
PERIOD = (W.PERIOD_FROM, W.PERIOD_TO)


def read(target, name):
    with open(os.path.join(target, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def pdate(s):
    return dt.date.fromisoformat(s[:10])


def pts(s):
    s = s.strip().rstrip("Z").replace("T", " ")
    return dt.datetime.strptime(s[:16], "%Y-%m-%d %H:%M")


def lisbon(utc_moment):
    """UTC to local: Lisbon keeps summer time until 25 October 2026."""
    off = 1 if (utc_moment + dt.timedelta(hours=1)).date() < W.DST_BACK else 0
    return utc_moment + dt.timedelta(hours=off)


def load(target):
    gaz, muni_of = {}, {}
    for r in read(target, "gazeteiro_localidades.csv"):
        gaz[r["nome"]] = r["codigo_localidade"]
        muni_of[r["codigo_localidade"]] = (r["codigo_municipio"], r["municipio"], r["distrito"],
                                           r["regiao"])
    reports = []
    for r in read(target, "registo_itens_imprensa.csv"):
        if r["estado"] != "aceite":
            continue
        reports.append(dict(route="IMP", ident=r["id_relato"], src=r["orgao"], theme=r["tema"],
                            code=r["codigo_acao"], place=r["local_texto"],
                            day=pdate(r["data_ocorrencia"]), start=pts(r["inicio_acao"]),
                            recv=lisbon(pts(r["carimbo_recepcao"]))))
    for r in read(target, "relatos_rede_parceiros.csv"):
        reports.append(dict(route="PAR", ident=r["id_relato"], src=r["codigo_parceiro"],
                            theme=r["tema"], code=r["codigo_acao"], place=r["local_texto"],
                            day=pdate(r["data_ocorrencia"]), start=pts(r["inicio_acao"]),
                            recv=lisbon(pts(r["carimbo_entrega_utc"])), load=r["id_carga"]))
    for r in read(target, "relatos_linha_publica.csv"):
        reports.append(dict(route="LIN", ident=r["id_relato"], src="LIN", theme=r["tema"],
                            code=r["codigo_acao"], place=r["local_texto"],
                            day=pdate(r["data_ocorrencia"]), start=pts(r["inicio_acao"]),
                            recv=pts(r["carimbo_recepcao"])))
    for r in reports:
        r["loc"] = gaz.get(r["place"], "")
        r["muni"] = muni_of.get(r["loc"], ("", "", "", ""))[0]
    exc = [dict(route=r["via"], ident=r["id_relato"], recv=pts(r["carimbo_recepcao"]),
                reason=r["motivo"]) for r in read(target, "excecoes_geocodificacao.csv")]
    totals = read(target, "totais_por_via.csv")
    return dict(gaz=gaz, muni_of=muni_of, reports=reports, exceptions=exc, totals=totals)


def actions(reports):
    """The protocol's action grain: one theme at one locality on one calendar day, however many
    reports or routes recorded it."""
    acts = {}
    for r in reports:
        if not r["loc"]:
            continue
        k = (r["theme"], r["loc"], r["day"])
        a = acts.setdefault(k, dict(theme=r["theme"], loc=r["loc"], day=r["day"],
                                    muni=r["muni"], codes=set(), routes=set(), reports=[]))
        a["codes"].add(r["code"])
        a["routes"].add(r["route"])
        a["reports"].append(r)
    return sorted(acts.values(), key=lambda a: (a["day"], a["loc"], a["theme"]))


def register(acts):
    """The dispute episodes the protocol's peace interval builds, one municipality and one theme."""
    by = {}
    for a in acts:
        by.setdefault((a["muni"], a["theme"]), []).append(a)
    eps = []
    for (muni, theme), aa in sorted(by.items()):
        aa.sort(key=lambda a: a["day"])
        cur = None
        for a in aa:
            if cur is None or (a["day"] - cur["last"]).days > W.QUIET_DAYS:
                cur = dict(muni=muni, theme=theme, open=a["day"], last=a["day"], conf=None,
                           actions=0)
                eps.append(cur)
            cur["last"] = a["day"]
            cur["actions"] += 1
            if a["codes"] & CONF and cur["conf"] is None:
                cur["conf"] = a["day"]
    for e in eps:
        e["closed"] = (W.EXTRACT - e["last"]).days >= W.QUIET_DAYS
        if e["conf"] is not None:
            e["t"], e["cause"] = (e["conf"] - e["open"]).days, 1
        elif e["closed"]:
            e["t"], e["cause"] = (e["last"] - e["open"]).days, 2
        else:
            e["t"], e["cause"] = (W.EXTRACT - e["open"]).days, 0
    return sorted(eps, key=lambda e: (e["open"], e["muni"], e["theme"]))


def curves(rows):
    """One pass over the ordered event times: the cumulative share with a quiet close as the other
    end of an episode, the event-free share, and the product-limit survival that carries a quiet
    close as an observation that stops."""
    times = sorted({t for t, c in rows if c in (1, 2)})
    S, cif, km = 1.0, 0.0, 1.0
    cifc, sc, kmc = [(-1, 0.0)], [(-1, 1.0)], [(-1, 0.0)]
    for t in times:
        n = sum(1 for tt, c in rows if tt >= t)
        d1 = sum(1 for tt, c in rows if tt == t and c == 1)
        d2 = sum(1 for tt, c in rows if tt == t and c == 2)
        if n:
            cif += S * d1 / n
            km *= 1 - d1 / n
            S *= 1 - (d1 + d2) / n
        cifc.append((t, cif))
        sc.append((t, S))
        kmc.append((t, 1 - km))
    return cifc, sc, kmc


def at(curve, t):
    v = curve[0][1]
    for tt, vv in curve:
        if tt <= t:
            v = vv
        else:
            break
    return v


def weekly_cif(rows, width):
    """The same estimate read on intervals instead of day by day."""
    mx = max(t for t, c in rows)
    S, cif = 1.0, 0.0
    for lo in range(0, ((mx // width) + 1) * width, width):
        hi = lo + width
        at_risk = sum(1 for t, c in rows if t >= hi)
        d1 = sum(1 for t, c in rows if lo <= t < hi and c == 1)
        d2 = sum(1 for t, c in rows if lo <= t < hi and c == 2)
        cen = sum(1 for t, c in rows if lo <= t < hi and c == 0)
        n = at_risk + d1 + d2 + cen - 0.5 * cen
        if n > 0:
            cif += S * d1 / n
            S *= 1 - (d1 + d2) / n
    return cif


def fortnight_of(day):
    for label, a, b in W.fortnights():
        if a <= day <= b:
            return label
    return None


def compute(target):
    b = load(target)
    acts = actions(b["reports"])
    eps = register(acts)
    cohort = [e for e in eps if PERIOD[0] <= e["open"] <= PERIOD[1]]
    rows = [(e["t"], e["cause"]) for e in cohort]
    n = len(rows)
    E = sum(1 for t, c in rows if c == 1)
    C = sum(1 for t, c in rows if c == 2)
    Z = n - E - C
    cifc, sc, kmc = curves(rows)
    cif, kmf = cifc[-1][1], kmc[-1][1]
    g = dict(cohort=n, recorded=E, closed_quiet=C, still_open=Z,
             rate_pct=round(100 * cif), episodes=round(cif * n),
             raw_episodes=cif * n, raw_rate=100 * cif,
             rung0_episodes=E, rung0_pct=round(100 * E / n),
             rung1_episodes=round(E / (E + C) * n), rung1_pct=round(100 * E / (E + C)),
             rung2_episodes=round(kmf * n), rung2_pct=round(100 * kmf),
             raw_rung1=E / (E + C) * n, raw_rung2=kmf * n,
             weekly_episodes=weekly_cif(rows, 7) * n,
             fortnightly_episodes=weekly_cif(rows, 14) * n,
             actions_total=len(acts), reports_total=len(b["reports"]),
             last_conf_day=max((t for t, c in rows if c == 1), default=0),
             at_risk_at_last=sum(1 for t, c in rows if t >= max((tt for tt, cc in rows if cc == 1),
                                                                default=0)))
    # the same estimate taken episode by episode: each open episode's own remaining chance
    proj = float(E)
    for t, c in rows:
        if c != 0:
            continue
        s = at(sc, t)
        proj += (cif - at(cifc, t)) / s if s > 1e-12 else 0.0
    g["projected_episodes"] = proj

    # ---- A1, per fortnight
    a1 = {}
    for label, a, bb in W.fortnights():
        inside = [x for x in acts if a <= x["day"] <= bb]
        par = [x for x in inside if "PAR" in x["routes"]]
        a1[label] = dict(start=a.isoformat(), end=bb.isoformat(), actions=len(inside),
                         municipalities=len({x["muni"] for x in inside}),
                         partner_share=round(100.0 * len(par) / len(inside), 1) if inside else 0.0,
                         confrontational=len([x for x in inside if x["codes"] & CONF]))
    g["a1"] = a1

    # ---- A2, per access route
    a2 = {}
    for route, _ in W.ROUTES:
        placed, seen = [], set()
        for r in b["reports"]:
            if r["route"] != route or r["ident"] in seen:
                continue
            seen.add(r["ident"])
            placed.append(r)
        in_period = [r for r in placed if PERIOD[0] <= r["recv"].date() <= PERIOD[1]]
        exc = [e for e in b["exceptions"]
               if e["route"] == route and PERIOD[0] <= e["recv"].date() <= PERIOD[1]]
        mins = sorted((r["recv"] - r["start"]).total_seconds() / 60.0 for r in in_period)
        k = len(mins) // 2
        pair_equal = bool(mins) and (len(mins) % 2 == 1 or mins[k - 1] == mins[k])
        a2[route] = dict(received=len(in_period) + len(exc), unplaceable=len(exc),
                         median_minutes=round(statistics.median(mins), 1) if mins else 0.0,
                         placed=len(in_period), median_pair_equal=pair_equal)
        g.setdefault("a2_debug", {})[route] = len(placed)
    g["a2"] = a2

    # ---- A3, per partner organisation
    rate_of = {p[0]: p[3] for p in W.PARTNERS}
    code_to_partner = {p[0]: p[0] for p in W.PARTNERS}
    code_to_partner[W.MERGED[1]] = W.MERGED[0]
    a3 = {}
    par_seen = {}
    for r in b["reports"]:
        if r["route"] != "PAR":
            continue
        par_seen.setdefault(r["ident"], r)            # the re-imported month carries each one twice
    for code, name, region, rate in W.PARTNERS:
        mine = [r for r in par_seen.values() if code_to_partner.get(r["src"]) == code
                and PERIOD[0] <= r["day"] <= PERIOD[1]]
        late = [r for r in mine if r["recv"].date() > PERIOD[1]]
        paid = 0.0
        for r in mine:
            if r["recv"].date() > PERIOD[1]:
                continue
            use = rate
            if code == W.AMENDED[0] and r["recv"].date() >= W.AMENDED[1]:
                use = W.AMENDED[2]
            paid += use
        a3[code] = dict(name=name, filed=len(mine), after_close=len(late),
                        euros=round(paid), raw_euros=paid)
    g["a3"] = a3

    # ---- the monthly series the earlier bulletins published
    series, months = [], ["maio", "junho", "julho", "agosto", "setembro"]
    for i, label in enumerate(months, 5):
        inside = [x for x in acts if x["day"].month == i and x["day"].year == 2026]
        series.append((label, len(inside), len({x["muni"] for x in inside}),
                       len({x["loc"] for x in inside})))
    g["monthly"] = series
    return g


def partner_returns_table(g):
    """What each partner's own monthly return states: the reports it filed, by the month of the
    action they are about. The merged partner's return counts both delivery codes."""
    table = {}
    for code, name, region, rate in W.PARTNERS:
        for m in range(5, 12):
            table[(code, m)] = (0, "")
    return table
