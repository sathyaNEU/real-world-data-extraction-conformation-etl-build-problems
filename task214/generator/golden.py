"""Golden figures from the clean truth, and the rivals the checks assert against."""
import datetime as dt
import statistics

import world
import pack

D0 = world.D0
CASE_FROM, CASE_TO = dt.date(2027, 9, 1), dt.date(2027, 10, 18)
EXP_FROM, EXP_TO = dt.date(2027, 8, 20), dt.date(2027, 10, 17)
ASSETS = list(world.RES) + list(world.ICS)


def di(date):
    return (date - D0).days


def zone_residents(mbs):
    out = {z: 0 for z in world.ZONES}
    for m in mbs:
        out[m['zone']] += m['pop']
    return out


def normal_paths():
    P = world.paths([])
    return P


def asset_rates(P, zres, case_rows, kmin=1, kmax=12, exp_from=EXP_FROM, exp_to=EXP_TO):
    rd = {a: 0 for a in ASSETS}
    for d in range(di(exp_from), di(exp_to) + 1):
        for z, pth in P[d].items():
            if pth:
                for a in pth:
                    if a in rd:
                        rd[a] += zres[z]
    cases = {a: 0 for a in ASSETS}
    for c in case_rows:
        if c['status'] != 'Confirmed' or not c['zkey'] or not (CASE_FROM <= c['onset'] <= CASE_TO):
            continue
        hit = set()
        for k in range(kmin, kmax + 1):
            d = di(c['onset']) - k
            pth = P[d][c['zkey']] if 0 <= d < len(P) else None
            if pth:
                hit.update(a for a in pth if a in cases)
        for a in hit:
            cases[a] += 1
    rate = {a: (cases[a] / rd[a] * 1e5 if rd[a] else 0.0) for a in ASSETS}
    return cases, rd, rate


MIN_CASES = 5     # terms of reference 4: assets whose water reached fewer than five cases are not ranked


def ranked(rate, cases, min_cases=MIN_CASES):
    return sorted([a for a in rate if cases[a] >= min_cases], key=lambda a: -rate[a])


def main_figures(W, mbs, case_rows):
    zres = zone_residents(mbs)
    cases, rd, rate = asset_rates(W['P'], zres, case_rows)
    order = ranked(rate, cases)
    call, second = order[0], order[1]
    # forward: residents whose water passes through the call during the renewal (planned operations)
    fwd_zones = renewal_zones(call)
    return dict(zres=zres, cases=cases, rd=rd, rate=rate, call=call, runner_up=second,
                gap=rate[call] / rate[second], forward_residents=sum(zres[z] for z in fwd_zones), fwd_zones=fwd_zones)


def renewal_zones(asset):
    """Zones supplied through an asset under the renewal's planned arrangement (FM11 and LM12 shut,
    BM3 and BM7 open)."""
    reps = [('FM11', 0, 0, 'BM3'), ('LM12', 0, 0, 'BM7')]
    P = world.paths([(m, 0, 0, bf) for m, f, l, bf in reps])
    return sorted(z for z, pth in P[0].items() if pth and asset in pth)


def register_figures(mbs, case_rows):
    zres = zone_residents(mbs)
    return asset_rates(normal_paths(), zres, case_rows)


def onset_day_figures(W, mbs, case_rows):
    """Rival: each case placed on the supply its zone had on the onset day only."""
    zres = zone_residents(mbs)
    P = W['P']
    cases, rd, _ = asset_rates(P, zres, [], 1, 1)
    cases = {a: 0 for a in ASSETS}
    for c in case_rows:
        if c['status'] == 'Confirmed' and c['zkey'] and CASE_FROM <= c['onset'] <= CASE_TO:
            pth = P[di(c['onset'])][c['zkey']] or ()
            for a in pth:
                if a in cases:
                    cases[a] += 1
    return {a: (cases[a] / rd[a] * 1e5 if rd[a] else 0.0) for a in ASSETS}


# ---------------------------------------------------------------- ask 1
TYPING_PERIODS = [(dt.date(2027, 7, 1), dt.date(2027, 10, 17), '1 July to 17 October')]


def lab_figures(lab_rows, ref_rows):
    tested = []
    parvum = []
    hominis = []
    for a, b, _ in pack.MONTHS:
        people = {id(r['person']) for r in lab_rows if r['person']['resident'] and a <= r['collected'] <= b}
        tested.append(len(people))
    for a, b, _ in TYPING_PERIODS:
        par = hom = 0
        for x in ref_rows:
            if x['person']['resident'] and a <= x['true_collected'] <= b:
                if x['result'] == 'Cryptosporidium parvum':
                    par += 1
                elif x['result'] == 'Cryptosporidium hominis':
                    hom += 1
        parvum.append(par)
        hominis.append(hom)
    return dict(tested=tested, parvum=parvum, hominis=hominis)


# ---------------------------------------------------------------- ask 2
def connections_at(reg, end):
    return sum(1 for r in reg if r['supply'] == 'Networked' and (r['connected'] is None or r['connected'] <= end))


def complaint_figures(crm, web, reg):
    out = {}
    for a, b, label in pack.PERIODS:
        conn = connections_at(reg, b)
        row = {}
        for cat in pack.CATS:
            n = 0
            for c in crm:
                if c['cat'] != cat or c['prop']['supply'] != 'Networked':
                    continue
                t = c['received']
                if c['rekey_of']:
                    w = [x for x in web if x['wid'] == c['rekey_of']][0]
                    t = w['submitted']
                if a <= t.date() <= b:
                    n += 1
            for w in web:
                if w['cat'] == cat and not w['crm'] and a <= w['submitted'].date() <= b:
                    if not any(c['rekey_of'] == w['wid'] for c in crm):
                        n += 1
            row[cat] = n / conn * 1000.0
        out[label] = dict(rates=row, connections=conn)
    return out


# ---------------------------------------------------------------- ask 3
CALL_MONTHS = [(dt.date(2027, 7, 1), dt.date(2027, 7, 31), 'July'), (dt.date(2027, 8, 1), dt.date(2027, 8, 31), 'August'),
               (dt.date(2027, 9, 1), dt.date(2027, 9, 30), 'September')]


def callout_figures(srs):
    out = {}
    for a, b, label in CALL_MONTHS:
        u_att, u_res, n_att, n_res = [], [], [], []
        for s in srs:
            if not (a <= s['true_notice'].date() <= b):
                continue
            att = (s['attend'] - s['true_notice']).total_seconds() / 60.0
            res = (s['resolve'] - s['true_notice']).total_seconds() / 60.0
            if s['priority'] == 'Urgent':
                u_att.append(att)
                u_res.append(res)
            else:
                n_att.append(att / 60.0)
                n_res.append(res / 60.0)
        out[label] = dict(urgent_attend=statistics.median(u_att), urgent_resolve=statistics.median(u_res),
                          nonurgent_attend=statistics.median(n_att), nonurgent_resolve=statistics.median(n_res),
                          n_urgent=len(u_att), n_nonurgent=len(n_att))
    return out
