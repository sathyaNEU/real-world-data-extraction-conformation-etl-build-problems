"""The pack's tabular files, as the study's systems write them.

Keys: the eCRF and the e-diary vendor know a patient by site-subject number (1043-012), the bioanalytical and
immunogenicity laboratories by randomisation number (R0417), the randomisation log carries both. Times: the eCRF
records infusions in site local time; the central and bioanalytical laboratories accession every sample in UTC."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K
import events as E

CITIES = {"US": ["Boston", "Cleveland", "Houston", "Denver", "Atlanta", "Phoenix", "Seattle", "Chicago", "Tampa", "Omaha"],
          "CA": ["Toronto", "Montreal", "Calgary", "Hamilton"], "PL": ["Warszawa", "Krakow", "Lodz", "Wroclaw", "Poznan", "Gdansk"],
          "HU": ["Budapest", "Debrecen", "Szeged", "Pecs", "Gyor"]}
LLOQ = 0.100


def ids(W):
    W.ssid = ["%d-%03d" % (W.site[i], W.subj[i]) for i in range(W.N)]
    W.rno = ["R%04d" % (W.randno[i] + 100) for i in range(W.N)]
    W.rdate = [K.day_date(W.rday[i]) for i in range(W.N)]
    info = site_info(W)
    W.zone = [K.ZONE[info[int(W.site[i])][0]] for i in range(W.N)]


def sdate(W, i, d):
    return W.rdate[i] + dt.timedelta(days=int(d))


def site_closures(W):
    """sites closed during the study (the investigator left): closing date and the site in the same country that took
    the patients on. The patients took their handsets with them and the e-diary vendor registered each at the new site
    under that site's next subject number, while the trial database kept the patient's original number"""
    r = K.rng('closures')
    close = {}
    for site, when in ((None, ("US", dt.date(2025, 7, 14))), (1025, dt.date(2025, 9, 15)), (1114, dt.date(2025, 12, 1)),
                       (None, ("HU", dt.date(2025, 12, 1)))):
        if site is None:
            c, when = when
            site = sorted({s for s, cc in W.sites if cc == c},
                          key=lambda s: (-sum(1 for i in range(W.N) if W.site[i] == s and
                                              sdate(W, i, -14) < when < sdate(W, i, int(W.disc[i] or W.vis[i, 3]))), s))[0]
        c = dict(W.sites)[site]
        to = [s for s, cc in W.sites if cc == c and s != site and s not in close][int(r.integers(0, 3))]
        close[site] = (when, to)
    return close


def site_info(W):
    """each site's city and activation date"""
    r = K.rng('site_rows')
    out = {}
    for sid, c in W.sites:
        city = CITIES[c][int(r.integers(0, len(CITIES[c])))]
        out[sid] = (city, dt.date(2024, 11, 1) + dt.timedelta(days=int(r.integers(0, 120))))
    return out


def site_rows(W):
    close = site_closures(W)
    info = site_info(W)
    rows = []
    for sid, c in W.sites:
        city, act = info[sid]
        rows.append(dict(site_number=sid, country=c, city=city, time_zone=K.ZONE[city], activated=str(act),
                         status="closed %s" % close[sid][0] if sid in close else "active"))
    return rows


def rand_rows(W):
    rows = []
    for i in np.argsort(W.randno):
        rows.append(dict(randomisation_number=W.rno[i], site_subject=W.ssid[i], randomised_on=str(W.rdate[i]),
                         stratum="prior advanced therapy failure" if W.biol[i] else "advanced therapy naive",
                         treatment="dovikizumab 600 mg IV" if W.act[i] else "placebo IV"))
    return rows


def base_rows(W):
    rows = []
    for i in range(W.N):
        rows.append(dict(site_subject=W.ssid[i], age=int(W.age[i]), sex=W.sex[i], weight_kg="%.1f" % W.wt[i],
                         modified_mayo_score=int(W.mmayo0[i]), normal_stool_frequency=int(W.sf_normal[i]),
                         prior_advanced_therapy_failure="Y" if W.biol[i] else "N"))
    return rows


def infusion_times(W):
    """local start and end of each infusion (study days 0, 28, 56), minutes after local midnight"""
    r = K.rng('infusion')
    T = {}
    for i in range(W.N):
        for d in (0, 28, 56):
            if W.disc[i] and d > W.disc[i]:
                continue
            st = int(r.integers(8 * 60 + 30, 14 * 60))
            du = int(r.integers(30, 46))
            T[(i, d)] = (st, st + du)
    return T


def fmt_local(day, minutes):
    return "%s %02d:%02d" % (day, minutes // 60, minutes % 60)


def infusion_rows(W, T):
    r = K.rng('infusion_rows')
    rows = []
    for i in range(W.N):
        for k, d in enumerate((0, 28, 56)):
            if (i, d) not in T:
                continue
            st, en = T[(i, d)]
            planned = 250
            interrupted = r.random() < 0.025
            delivered = planned if not interrupted else int(planned * r.uniform(0.80, 0.97))
            rows.append(dict(site_subject=W.ssid[i], visit="Week %d" % (4 * k), infusion_start_local=fmt_local(sdate(W, i, d), st),
                             infusion_end_local=fmt_local(sdate(W, i, d), en + (12 if interrupted else 0)),
                             planned_volume_ml=planned, delivered_volume_ml=delivered,
                             interrupted="Y" if interrupted else "N"))
    W.delivered = {(row['site_subject'], row['visit']): row['delivered_volume_ml'] for row in rows}
    return rows


def to_utc_str(W, i, day, minutes):
    t = K.local_to_utc(W.zone[i], dt.datetime.combine(day, dt.time(0, 0)) + dt.timedelta(minutes=minutes))
    return t.strftime("%Y-%m-%dT%H:%MZ")


def conc_rows(W, T):
    """one row per sample and analytical run; pre-dose samples a few minutes before the infusion, a few drawn after it
    started; week 12 at the visit; the intensive substudy's first-interval samples"""
    r = K.rng('conc')
    sub = set(r.choice(np.where(W.act)[0], 36, replace=False).tolist())
    W.substudy = sub
    samples = []
    for i in range(W.N):
        for k, d in enumerate((0, 28, 56)):
            if (i, d) not in T:
                continue
            st, en = T[(i, d)]
            late = d > 0 and r.random() < 0.035
            m = st + int(r.integers(6, 26)) if late else st - int(r.integers(5, 55))
            if not W.act[i] or d == 0:
                c = 0.0
            else:
                c = float(W.s['tr28' if d == 28 else 'tr56'][i])
                if late:
                    frac = (m - st) / (en - st)
                    c += 600.0 * frac / float(W.V[i])
            samples.append((i, "Week %d" % (4 * k), "PRE", sdate(W, i, d), m, c))
        if not (W.disc[i] and W.disc[i] < 84):
            d = int(W.vis[i, 3])
            m = int(r.integers(8 * 60, 15 * 60))
            c = float(W.s['d84'][i]) if W.act[i] else 0.0
            samples.append((i, "Week 12", "VISIT", sdate(W, i, d), m, c))
        if i in sub:
            st, en = T[(i, 0)]
            for tag, day_ in (("1H POST", 0), ("DAY 3", 3), ("DAY 7", 7), ("DAY 14", 14), ("DAY 21", 21)):
                if tag == "1H POST":
                    m = en + 60 + int(r.integers(-5, 10))
                    tt = (m - st) / 1440.0
                else:
                    m = int(r.integers(8 * 60, 12 * 60))
                    tt = day_ + (m - st) / 1440.0
                c = WD_conc(W, i, tt) * float(np.exp(r.normal(0, 0.12)))
                samples.append((i, "Week 0", tag, sdate(W, i, day_), m, c))
    # runs: chronological batches of about 80; reassays for about 4 per cent; one batch reported in ng/mL
    samples.sort(key=lambda s: (s[3], s[4], s[0]))
    rows = []
    run = 0
    ngml_run = None
    for n, (i, vis, tag, day_, m, c) in enumerate(samples):
        if n % 80 == 0:
            run += 1
            if day_ >= dt.date(2025, 9, 1) and ngml_run is None:
                ngml_run = run
        sid = "BWB-%06d" % (310000 + n * 7 % 1000003)
        def res(x, ng=False):
            if x < LLOQ:
                return "<%.3f" % LLOQ if not ng else "<%d" % int(LLOQ * 1000)
            return ("%.3f" % x) if not ng else ("%d" % round(x * 1000))
        ng = run == ngml_run
        base = dict(sample_id=sid, randomisation_number=W.rno[i], visit=vis, timepoint=tag,
                    collected_utc=to_utc_str(W, i, day_, m), analyte="dovikizumab", unit="ng/mL" if ng else "ug/mL")
        if r.random() < 0.04 and c > LLOQ:
            first = c * float(np.exp(r.normal(0, 0.35)))
            rows.append(dict(base, run_id="DVK-%03d" % run, result=res(first, ng), reportable="N",
                             comment="haemolysed, reassay requested"))
            rows.append(dict(base, run_id="DVK-%03d" % (run + 3), result=res(c), reportable="Y", comment="reassay",
                             unit="ug/mL"))
        else:
            rows.append(dict(base, run_id="DVK-%03d" % run, result=res(c, ng), reportable="Y", comment=""))
    return rows


def WD_conc(W, i, t):
    import world as WD
    return WD.conc_at(W, i, t)


def efficacy(W):
    """week-12 subscores consistent with the remission draw; non-responder imputation reasons"""
    r = K.rng('efficacy')
    E_ = {}
    for i in range(W.N):
        if W.disc[i] and W.disc[i] < 84:
            E_[i] = dict(es=None, sf=None, rb=None, rem=False, nri="discontinued before week 12")
            continue
        if W.rem[i]:
            es = int(r.random() < 0.55)
            sf = int(r.random() < 0.45)
            rb = 0
            if es + sf > 2:
                sf = 1
        else:
            es = int(r.choice([1, 2, 2, 3])) if not W.resp[i] else int(r.choice([1, 2]))
            sf = int(r.choice([1, 2, 3])) if not W.resp[i] else int(r.choice([0, 1, 2]))
            rb = int(r.choice([0, 1, 1, 2]))
            if es <= 1 and sf <= 1 and rb == 0:       # would read as remission: move one subscore
                es = 2
        nri = "rescue therapy before week 12" if W.rescue[i] else ""
        E_[i] = dict(es=es, sf=sf, rb=rb, rem=bool(W.rem[i]), nri=nri)
    W.eff = E_
    return E_


def eff_rows(W, topline=False):
    r = K.rng('eff_rows', topline)
    rows = []
    for i in range(W.N):
        e = W.eff[i]
        wk12 = sdate(W, i, int(W.vis[i, 3]))
        if topline and wk12 > K.TOPLINE - dt.timedelta(days=10):
            continue
        es = e['es']
        if topline and es is not None and r.random() < 0.09:
            es = int(np.clip(es + (1 if r.random() < 0.5 else -1), 0, 3))      # the site's local read
        if e['es'] is None:
            mm, rem = "", "N"
        else:
            mm = es + e['sf'] + e['rb']
            ok = (not e['nri']) and es <= 1 and e['sf'] <= 1 and e['rb'] == 0 and mm <= 2
            rem = "Y" if ok else "N"
        rows.append(dict(site_subject=W.ssid[i], visit="Week 12", endoscopic_subscore="" if es is None else es,
                         stool_frequency_subscore="" if e['sf'] is None else e['sf'],
                         rectal_bleeding_subscore="" if e['rb'] is None else e['rb'], modified_mayo_score=mm,
                         clinical_remission=rem, nri_reason=e['nri'],
                         endoscopy_read="local" if topline else "central adjudicated"))
    return rows


def lab_rows(W):
    r = K.rng('lab')
    rows = []
    idx = lambda day: int(round(day / 0.25))
    for i in range(W.N):
        us = W.country[i] in ("US", "CA")
        crp0 = float(W.crp[i])
        for k, d in enumerate((0, 28, 56, 84)):
            if W.disc[i] and d > W.disc[i]:
                break
            day_ = sdate(W, i, d if d < 84 else int(W.vis[i, 3]))
            alb = float(W.alb_t[min(idx(d), W.alb_t.shape[0] - 1), i]) + r.normal(0, 0.8)
            heal = 0.0 if d < W.onset[i] else 1.0
            crp = crp0 * (1 - 0.7 * heal * (W.rem[i] or W.resp[i])) * float(np.exp(r.normal(0, 0.25)))
            m = int(r.integers(8 * 60, 13 * 60))
            when = to_utc_str(W, i, day_, m)
            lab = "Meridian Central Laboratory, Indianapolis" if us else "Meridian Central Laboratory, Leuven"
            rows.append(dict(site_subject=W.ssid[i], visit="Week %d" % (4 * k) if k < 3 else "Week 12", collected_utc=when,
                             test="ALBUMIN", result=("%.1f" % (alb / 10)) if us else ("%.0f" % alb), unit="g/dL" if us else "g/L",
                             laboratory=lab))
            rows.append(dict(site_subject=W.ssid[i], visit="Week %d" % (4 * k) if k < 3 else "Week 12", collected_utc=when,
                             test="CRP", result=("%.2f" % (crp / 10)) if us else ("%.1f" % crp), unit="mg/dL" if us else "mg/L",
                             laboratory=lab))
    return rows


def endo_rows(W):
    r = K.rng('endo')
    rows = []
    for i in range(W.N):
        for vis, d in (("Screening", -7), ("Week 12", int(W.vis[i, 3]))):
            e = W.eff[i]
            if vis == "Week 12" and e['es'] is None:
                continue
            true = e['es'] if vis == "Week 12" else int(r.choice([2, 3], p=[0.6, 0.4]))
            c1 = true if r.random() < 0.88 else int(np.clip(true + r.choice([-1, 1]), 0, 3))
            c2 = true if r.random() < 0.88 else int(np.clip(true + r.choice([-1, 1]), 0, 3))
            adj = true
            loc = true if r.random() < 0.85 else int(np.clip(true + r.choice([-1, 1]), 0, 3))
            rows.append(dict(site_subject=W.ssid[i], visit=vis, procedure_date=str(sdate(W, i, d)), local_read=loc,
                             central_reader_1=c1, central_reader_2=c2, adjudicated=adj if c1 != c2 else "",
                             final_central=adj))
    return rows


# ---- Ask B: anti-drug antibodies, results by run and the run log -----------------------------------------------
def ada_rows(W, A):
    """the bioanalytical laboratory's tiered workflow: each draw is split into aliquots A and B; aliquot A is screened
    in a screening run of about 90 samples; screen positives from an accepted screening run go to a confirmatory and
    titer run, on aliquot A or, where aliquot A was used up, on the backup aliquot B; a rejected run's samples are
    re-tested in a later run of the same assay; some accepted results are repeated later for sample management in a
    run that failed"""
    r = K.rng('ada_rows')
    samples = []
    for x in A:
        i = x['i']
        d = x['day'] if x['visit'] < 3 else int(W.vis[i, 3])
        x['cdate'] = sdate(W, i, d)
        # backup aliquots kept in the site freezer travel later on a manifest that names no visit
        x['b_unsched'] = r.random() < 0.7
        samples.append((x['cdate'], i, x))
    # draws taken outside the schedule (at an infusion reaction or a flare), status as at the last visit before
    last = {}
    for x in A:
        last.setdefault(x['i'], []).append(x)
    for i in range(W.N):
        if r.random() < 0.04:
            top = int(W.disc[i] or W.vis[i, 3])
            d = int(r.integers(3, max(top, 4)))
            if d in (28, 56) or d >= top:
                continue
            prev = [x for x in last.get(i, []) if x['day'] <= d]
            if not prev:
                continue
            x = dict(prev[-1], visit=None, day=d, cdate=sdate(W, i, d), b_unsched=True)
            samples.append((x['cdate'], i, x))
    samples.sort(key=lambda s: (s[0], s[1]))
    rows, runs = [], []
    run = [0]
    def new_run(date, assay, ok):
        run[0] += 1
        runs.append(dict(run_id="ADA-%04d" % (2500 + run[0]), run_date=str(date), assay=assay,
                         plate_acceptance="accepted" if ok else "rejected",
                         reason="" if ok else ["positive control out of range", "negative control CV above 20 per cent",
                                               "plate edge effect"][int(r.integers(0, 3))]))
        return runs[-1]
    def label(x, sid):
        if x['visit'] is None or (sid == x['aliquots'][1] and x['b_unsched']):
            return "Unscheduled"
        return "Week %d" % (4 * x['visit'])
    def screen(run_id, i, x, sid, accepted):
        pos = x['pos'] if accepted else (r.random() < 0.5)
        sn = (r.uniform(1.6, 6.0) if pos else r.uniform(0.7, 1.25)) if accepted else r.uniform(0.6, 3.0)
        return [dict(sample_id=sid, randomisation_number=W.rno[i], collection_date=str(x["cdate"]), manifest_visit=label(x, sid),
                     run_id=run_id, tier="screening", result="%.2f" % sn, cut_point="1.32")]
    def confirm(run_id, i, x, sid, accepted):
        base = dict(sample_id=sid, randomisation_number=W.rno[i], collection_date=str(x["cdate"]), manifest_visit=label(x, sid),
                    run_id=run_id)
        inh = r.uniform(32, 85) if (accepted and x['pos']) else r.uniform(0, 60)
        out = [dict(base, tier="confirmatory", result="%.1f" % inh, cut_point="18.5")]
        if inh >= 18.5:
            t = x['titer'] if (accepted and x['pos']) else int(2 ** r.integers(1, 5)) * 10
            out.append(dict(base, tier="titer", result="1:%d" % max(t, 10), cut_point=""))
            if accepted:
                out.append(dict(base, tier="neutralising", result="positive" if x['nab'] else "negative", cut_point=""))
        return out
    sid_n = [0]
    def sid():
        sid_n[0] += 1
        return "BWI-%06d" % (520000 + sid_n[0] * 7919 % 479993)
    rescreen, reconfirm, repeat = [], [], []
    for n0 in range(0, len(samples), 90):
        batch = samples[n0:n0 + 90]
        cur = new_run(batch[-1][0] + dt.timedelta(days=int(r.integers(9, 30))), "screening", r.random() > 0.07)
        pending = []
        for day_, i, x in batch:
            x['aliquots'] = (sid(), sid())
            ok = cur['plate_acceptance'] == "accepted"
            rows.extend(screen(cur['run_id'], i, x, x['aliquots'][0], ok))
            if not ok:
                rescreen.append((i, x))
            else:
                if x['pos']:
                    pending.append((i, x))
                if r.random() < 0.04:
                    repeat.append((i, x))
        if pending:
            conf = new_run(dt.date.fromisoformat(cur['run_date']) + dt.timedelta(days=int(r.integers(5, 13))),
                           "confirmatory and titer", r.random() > 0.10)
            for i, x in pending:
                x['conf_aliquot'] = x['aliquots'][1] if r.random() < 0.4 else x['aliquots'][0]
                rows.extend(confirm(conf['run_id'], i, x, x['conf_aliquot'], conf['plate_acceptance'] == "accepted"))
                if conf['plate_acceptance'] != "accepted":
                    reconfirm.append((i, x))
    # the end-of-study re-test runs: rejected screening and confirmatory runs repeated in accepted runs, and the
    # sample-management repeats in a screening run that failed
    k = 0
    for i, x in rescreen:
        if k % 60 == 0:
            good = new_run(dt.date(2026, 5, 18) + dt.timedelta(days=k // 60 * 3), "screening", True)
        rows.extend(screen(good['run_id'], i, x, x['aliquots'][0], True))
        if x['pos']:
            reconfirm.append((i, x))
            x.setdefault('conf_aliquot', x['aliquots'][1] if r.random() < 0.4 else x['aliquots'][0])
        k += 1
    if reconfirm:
        good = new_run(dt.date(2026, 6, 1), "confirmatory and titer", True)
        for i, x in reconfirm:
            rows.extend(confirm(good['run_id'], i, x, x['conf_aliquot'], True))
    if repeat:
        bad = new_run(dt.date(2026, 6, 3), "screening", False)
        for i, x in repeat:
            rows.extend(screen(bad['run_id'], i, x, x['aliquots'][0], False))
    # the laboratory numbers its runs in the order they are performed
    order = sorted(runs, key=lambda x: (x['run_date'], x['run_id']))
    rename = {x['run_id']: "ADA-%04d" % (2501 + j) for j, x in enumerate(order)}
    for x in runs:
        x['run_id'] = rename[x['run_id']]
    for z in rows:
        z['run_id'] = rename[z['run_id']]
    runs.sort(key=lambda x: x['run_id'])
    rows.sort(key=lambda z: (z['run_id'], z['sample_id'], ["screening", "confirmatory", "titer", "neutralising"].index(z['tier'])))
    return rows, runs


# ---- Ask C: the e-diary, keyed by device serial, and the device dispensing log ---------------------------------
def devices(W):
    """each patient takes a device at screening; some swap mid-study; returned devices are reset and re-issued to a new
    patient at the same site; returns dispensing rows and a lookup (i, day) -> serial"""
    r = K.rng('devices')
    pool = {}                                   # site -> list of (serial, free_from_date)
    disp = []
    serial_n = 40000
    order = np.argsort(W.rday)
    assign = {}
    close = site_closures(W)
    nxt = {s: max([int(W.subj[i]) for i in range(W.N) if W.site[i] == s] or [0]) for s, _ in W.sites}
    W.transfer = {}
    for i in order:
        site = W.site[i]
        start = sdate(W, i, -14)
        end = sdate(W, i, int(W.disc[i] or W.vis[i, 3]) + 3)
        swap = int(r.integers(10, 50)) if r.random() < 0.10 else None
        cuts = [start] + ([sdate(W, i, swap)] if swap else []) + [end]
        moved = None
        if site in close and start < close[site][0] < end - dt.timedelta(days=3):
            moved = close[site][0]
            nxt[close[site][1]] += 1
            W.transfer[i] = (moved, "%d-%03d" % (close[site][1], nxt[close[site][1]]))
            cuts = sorted(set(cuts + [moved]))
        ser = None
        for a, b in zip(cuts[:-1], cuts[1:]):
            here = site if not (moved and a >= moved) else close[site][1]
            who = W.ssid[i] if not (moved and a >= moved) else W.transfer[i][1]
            if not (moved and a == moved):          # a transfer keeps the handset; a start or a swap takes one
                free = [s for s in pool.get(here, []) if s[1] <= a]
                if free and r.random() < 0.92:
                    ser = free[0][0]
                    pool[here].remove(free[0])
                else:
                    serial_n += int(r.integers(1, 9))
                    ser = "EDC-%06d" % serial_n
            app = "3.4.1" if a >= dt.date(2025, 8, 1) else "2.9.6"
            disp.append(dict(handset_serial=ser, site_subject=who, dispensed_on=str(a), returned_on=str(b),
                             app_version_at_dispensing=app))
            if not (moved and b == moved):
                pool.setdefault(here, []).append((ser, b + dt.timedelta(days=int(r.integers(2, 9)))))
            for d in range((a - W.rdate[i]).days, (b - W.rdate[i]).days):
                assign[(i, d)] = ser
    disp.sort(key=lambda z: (z['dispensed_on'], z['handset_serial']))
    return disp, assign


def diary_rows(W, D, assign):
    r = K.rng('diary_rows')
    rows = []
    n = 0
    for x in D:
        i, d = x['i'], x['day']
        if x['missed'] or (i, d) not in assign:
            continue
        ser = assign[(i, d)]
        day_ = sdate(W, i, d)
        m = int(r.integers(19 * 60, 23 * 60 + 50))
        vals = [(x['sf'], x['rb'])]
        if r.random() < 0.05:                                       # entered in error, corrected later the same evening
            vals = [(max(0, x['sf'] + int(r.choice([-3, -2, 2, 3]))), int(np.clip(x['rb'] + r.choice([-1, 1]), 0, 3)))] + vals
        for j, (sf, rb) in enumerate(vals):
            mm = min(m + 25 * j + int(r.integers(1, 20)) * j, 23 * 60 + 59)
            n += 1
            rows.append(dict(entry_id="E%07d" % (1000000 + n * 37 % 9000001), handset_serial=ser, diary_date=str(day_),
                             recorded_at="%s %02d:%02d" % (day_, mm // 60, mm % 60), stool_frequency=sf,
                             rectal_bleeding=rb))
    rows.sort(key=lambda z: (z['handset_serial'], z['recorded_at'], z['entry_id']))
    return rows


# ---- Ask A: adverse events as the eCRF records them -----------------------------------------------------------
PT_SOC = {"Infections and infestations": [t for t, _ in E.INFECT + E.SERIOUS],
          "Injury, poisoning and procedural complications": ["Infusion related reaction"],
          "General disorders and administration site conditions": ["Infusion site reaction", "Chills", "Fatigue", "Pyrexia"],
          "Immune system disorders": ["Hypersensitivity"],
          "Skin and subcutaneous tissue disorders": ["Urticaria", "Pruritus", "Rash"],
          "Vascular disorders": ["Flushing"], "Nervous system disorders": ["Headache"],
          "Musculoskeletal and connective tissue disorders": ["Arthralgia"],
          "Gastrointestinal disorders": ["Colitis ulcerative", "Nausea"], "Blood and lymphatic system disorders": ["Anaemia"]}


def ae_rows(W, eps):
    r = K.rng('ae_rows')
    rows = []
    seq = {}
    for e in sorted(eps, key=lambda z: (z['i'], z['onset'])):
        i = e['i']
        rec = E.ae_visits(W, e)
        on = sdate(W, i, e['onset'])
        # an event's severity (its worst so far) and the investigator's causality call are the event's, carried from
        # review to review; an event that worsens after the first infusion is recorded as a new event (SAP 6.3)
        sev_e = ["mild", "moderate", "severe"][int(r.choice([0, 1, 2], p=[0.55, 0.37, 0.08]))]
        if e['serious'] and sev_e == "mild":
            sev_e = "moderate"
        rel_e = ["not related", "unlikely", "possibly"][int(r.integers(0, 3))]
        soc = next((s for s, l in PT_SOC.items() if e['term'] in l), "Other")
        for k, v in enumerate(rec):
            if e['partial'] and not (e['completed'] and k > 0):
                on_s = on.strftime("%Y-%m-UN")
            elif e['mis_on'] is not None and k == 0:
                on_s = str(sdate(W, i, e['mis_on']))
            else:
                on_s = str(on)
            seq[i] = seq.get(i, 0) + 1
            resolved = e['end'] <= v
            ser = e['serious'] and (e['sday'] is None or e['sday'] <= v)
            rows.append(dict(site_subject=W.ssid[i], ae_number=seq[i], recorded_at_visit=vis_name(v, W, i),
                             verbatim_term=e['term'].lower(), preferred_term=e['term'], system_organ_class=soc,
                             onset_date=on_s, end_date=str(sdate(W, i, e['end'])) if resolved else "",
                             ongoing="N" if resolved else "Y", serious="Y" if ser else "N",
                             severity=sev_e, related=rel_e))
            if resolved:
                break
    order = {"Screening": 0, "Week 4": 1, "Week 8": 2, "Week 12": 3, "Early termination": 3}
    rows.sort(key=lambda z: (z['site_subject'], order[z['recorded_at_visit']], z['onset_date'], z['preferred_term']))
    line = {}
    for z in rows:
        line[z['site_subject']] = line.get(z['site_subject'], 0) + 1
        z['ae_number'] = line[z['site_subject']]
    return rows


def vis_name(v, W, i):
    if v < 0:
        return "Screening"
    if v == 28:
        return "Week 4"
    if v == 56:
        return "Week 8"
    if W.disc[i] and v == int(W.disc[i]):
        return "Early termination"
    return "Week 12"


def visit_rows(W):
    rows = []
    for i in range(W.N):
        rows.append(dict(site_subject=W.ssid[i], visit="Screening", visit_date=str(sdate(W, i, -14))))
        for k, d in enumerate((0, 28, 56)):
            if W.disc[i] and d > W.disc[i]:
                break
            rows.append(dict(site_subject=W.ssid[i], visit="Week %d" % (4 * k), visit_date=str(sdate(W, i, d))))
        if W.disc[i] and W.disc[i] < int(W.vis[i, 3]):
            rows.append(dict(site_subject=W.ssid[i], visit="Early termination", visit_date=str(sdate(W, i, int(W.disc[i])))))
        else:
            rows.append(dict(site_subject=W.ssid[i], visit="Week 12", visit_date=str(sdate(W, i, int(W.vis[i, 3])))))
    return rows


def conmed_rows(W):
    r = K.rng('conmed')
    meds = [("Mesalazine", "oral"), ("Prednisone", "oral"), ("Budesonide MMX", "oral"), ("Azathioprine", "oral"),
            ("Loperamide", "oral"), ("Paracetamol", "oral"), ("Iron sucrose", "IV")]
    rows = []
    for i in range(W.N):
        for m, route in meds:
            if r.random() < (0.55 if m == "Mesalazine" else 0.12):
                st = sdate(W, i, -int(r.integers(30, 900)))
                rows.append(dict(site_subject=W.ssid[i], medication=m, route=route, start_date=str(st),
                                 stop_date="" if r.random() < 0.7 else str(sdate(W, i, int(r.integers(1, 84)))),
                                 indication="ulcerative colitis" if m not in ("Paracetamol", "Iron sucrose") else "other"))
    return rows
