"""task464 architecture 9: every figure, computed from the shipped files under target/ and nothing else.

The main call: for each practice, the expected number of its patients issued a statin from 1 September to 30
November 2026 who, still registered with it on 30 June 2027, will have had no statin issued from 1 March to 30
June 2027. The golden runs each patient forward to the review their current repeat set reaches (the request
after its last authorised issue) and applies the record's rates: the share of statin repeats that ran out and
were not re-authorised, and the stops between reviews per 28 days of supply. The default path is a persistence
curve on months since the patient's first statin issue.

The asks: the 2025 return's ACE inhibitor and ARB adherence and its ticagrelor-after-a-heart-attack indicator.
"""
import csv, json, os, re, collections, decimal, datetime as dt
import world as W

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.environ.get("T464_TARGET") or os.path.join(BASE, "target")
FIG = os.path.join(BASE, "generator", "figures.json")

CODE_KEY = {p["code"]: p["key"] for p in W.PRACTICES}


def dnum(s):
    if "/" in s:
        d, m, y = s.split("/"); return (dt.date(int(y), int(m), int(d)) - W.D0).days
    return (dt.date.fromisoformat(s) - W.D0).days


_LOOK = None


def lookup():
    global _LOOK
    if _LOOK is None:
        a, b = {}, {}
        with open(os.path.join(T, "cvd_product_lookup.csv"), encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                rec = (r["vtm"], r["strength"], r["form"], r["bnf_class"])
                a[r["system_a_drug"]] = rec; b[r["system_b_product"]] = rec
        _LOOK = (a, b)
    return _LOOK


def load_issues():
    la, lb = lookup()
    out = []
    with open(os.path.join(T, "repeat_issues_system_a_2024-01_to_2026-11.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            v, s, f, c = la[r["Drug"]]
            out.append(dict(code=r["Practice Code"], pid=r["Patient Ref"], t=dnum(r["Issue Date"]), vtm=v, strength=s,
                            form=f, cls=c, qty=int(r["Quantity"].split()[0]), acute=r["Course"] == "Acute",
                            ref=r["Repeat Ref"] or None, eps=r["EPS Prescription ID"]))
    with open(os.path.join(T, "repeat_issues_system_b_2024-01_to_2026-11.jsonl"), encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            v, s, f, c = lb[r["product"]]
            out.append(dict(code=r["org"], pid=r["patient_pseudo"], t=dnum(r["issued"]), vtm=v, strength=s, form=f,
                            cls=c, qty=int(r["qty"]), acute=r["course"] == "acute", ref=r["authorisation"],
                            eps=r["eps_id"]))
    return out


def load_templates():
    la, lb = lookup()
    out = {}
    with open(os.path.join(T, "repeat_authorisations_system_a.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            v, s, f, c = la[r["Drug"]]
            q = int(r["Quantity"].split()[0])
            out[r["Repeat Ref"]] = dict(code=r["Practice Code"], pid=r["Patient Ref"], ref=r["Repeat Ref"], vtm=v,
                                        strength=s, form=f, cls=c, directions=r["Dosage"],
                                        qty=q, L=int(round(q / doses_per_day(r["Dosage"]))),
                                        M=int(r["Authorised Issues"]), start=dnum(r["Authorised Date"]),
                                        end=dnum(r["End Date"]) if r["End Date"] else None)
    with open(os.path.join(T, "repeat_authorisations_system_b.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            v, s, f, c = lb[r["product"]]
            q = int(r["qty_per_issue"])
            out[r["authorisation"]] = dict(code=r["org"], pid=r["patient_pseudo"], ref=r["authorisation"], vtm=v,
                                           strength=s, form=f, cls=c, directions=r["directions"],
                                           qty=q, L=int(round(q / doses_per_day(r["directions"]))),
                                           M=int(r["issues_authorised"]), start=dnum(r["start_date"]),
                                           end=dnum(r["end_date"]) if r["end_date"] else None)
    return out


def load_register():
    eps = collections.defaultdict(list)
    with open(os.path.join(T, "patient_register_2026-12-01.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            eps[r["patient_ref"]].append((r["practice_code"], dnum(r["registered"]),
                                          dnum(r["deregistered"]) if r["deregistered"] else None,
                                          r["deregistration_reason"]))
    return eps


def load_cancellations():
    s = set()
    with open(os.path.join(T, "eps_item_cancellations_2024-2026.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            s.add((r["prescription_id"], r["item"]))
    return s


def registered_at(eps, pid, code, t):
    for c, a, b, why in eps.get(pid, []):
        if c == code and a <= t and (b is None or t < b):
            return True
    return False


class Data:
    def __init__(self):
        self.issues = load_issues()
        self.tpl = load_templates()
        self.reg = load_register()
        canc = load_cancellations()
        la, lb = lookup()
        inv = {v: k for k, v in la.items()}
        for r in self.issues:
            name = inv.get((r["vtm"], r["strength"], r["form"], r["cls"]))
            r["cancelled"] = (r["eps"], name) in canc
        self.statin = [r for r in self.issues if r["cls"] == "Statin" and not r["cancelled"]]
        by = collections.defaultdict(list)
        for r in self.statin:
            by[r["pid"]].append(r)
        for v in by.values():
            v.sort(key=lambda r: (r["t"], r["ref"] or ""))
        self.statin_by = by
        self.made = collections.Counter(r["ref"] for r in self.statin if r["ref"])
        tb = collections.defaultdict(list)
        for ref, tp in self.tpl.items():
            if tp["cls"] == "Statin":
                tb[tp["pid"]].append(tp)
        for v in tb.values():
            v.sort(key=lambda tp: (tp["start"], tp["ref"]))
        self.statin_tpl = tb


# ---------------------------------------------------------------------------------------------- the population
def population(D):
    pop = {}
    for pid, rows in D.statin_by.items():
        for c in sorted({r["code"] for r in rows}):
            if any(r["code"] == c and W.POP_FROM <= r["t"] <= W.ASOF for r in rows) and registered_at(D.reg, pid, c, W.ASOF):
                pop[pid] = c
    return pop


# ---------------------------------------------------------------------------------------------- the record's rates
def reauth_rate(D, lo=None, hi=None, per=False, follow=60, drop_left=True):
    lo = W.EXTRACT_FROM if lo is None else lo
    hi = W.ASOF - 150 if hi is None else hi
    n = collections.Counter(); f = collections.Counter()
    for pid, tl in D.statin_tpl.items():
        for i, tp in enumerate(tl):
            if tp["start"] < W.EXTRACT_FROM or D.made[tp["ref"]] < tp["M"]:
                continue
            last = max(r["t"] for r in D.statin_by[pid] if r["ref"] == tp["ref"])
            if not (lo <= last <= hi): continue
            end = last + tp["L"]
            if drop_left and not registered_at(D.reg, pid, tp["code"], end + follow):
                continue
            n[tp["code"]] += 1
            nxt = [x for x in tl[i + 1:] if x["start"] >= last]
            if not (nxt and nxt[0]["start"] <= end + follow):
                f[tp["code"]] += 1
    pool = sum(f.values()) / sum(n.values())
    if per:
        return {c: f[c] / n[c] for c in n}, n, f
    return {c: pool for c in n}, n, f


def first_statin(D, pid):
    return D.statin_by[pid][0]["t"]


def stop_rates(D, per=False, split=True, gap=150):
    """Stops between reviews: a statin repeat left with issues unused and no statin issued for 150 days after its
    last issue, per 28 days of statin supply issued on repeats, early (first 182 days from the patient's first
    statin issue in the extract, for a patient whose first issue there is acute) and late."""
    ex = collections.defaultdict(lambda: [0.0, 0.0]); st = collections.defaultdict(lambda: [0, 0])
    for pid, rows in D.statin_by.items():
        new_start = rows[0]["acute"] and rows[0]["t"] >= W.EXTRACT_FROM + 30
        t0 = rows[0]["t"]
        for r in rows:
            if r["acute"] or r["t"] > W.ASOF - gap: continue
            k = 0 if (split and new_start and r["t"] - t0 < 182) else 1
            ex[r["code"]][k] += D.tpl[r["ref"]]["L"] / 28 if r["ref"] in D.tpl else 1
        for tp in D.statin_tpl.get(pid, []):
            if tp["start"] < W.EXTRACT_FROM: continue
            mm = D.made[tp["ref"]]
            if mm == 0 or mm >= tp["M"]: continue
            last = max(r["t"] for r in rows if r["ref"] == tp["ref"])
            if last > W.ASOF - gap: continue
            if any(last < r["t"] <= last + gap for r in rows): continue
            if not registered_at(D.reg, pid, tp["code"], last + tp["L"] + 60): continue
            k = 0 if (split and new_start and last - t0 < 182) else 1
            st[tp["code"]][k] += 1
    def rate(e, s):
        return (s[0] / e[0] if e[0] else 0.0, s[1] / e[1] if e[1] else 0.0)
    if per:
        return {c: rate(ex[c], st[c]) for c in ex}
    E = [sum(v[0] for v in ex.values()), sum(v[1] for v in ex.values())]
    S = [sum(v[0] for v in st.values()), sum(v[1] for v in st.values())]
    pr = rate(E, S)
    if not split:
        pr = ((S[0] + S[1]) / (E[0] + E[1]),) * 2
    return {c: pr for c in ex}


def pacing(D):
    gaps = []
    for pid, rows in D.statin_by.items():
        for a, b in zip(rows, rows[1:]):
            if a["ref"] and a["ref"] == b["ref"] and b["t"] <= W.ASOF:
                g = b["t"] - a["t"] - D.tpl[a["ref"]]["L"]
                if -10 < g < 40: gaps.append(g)
    return sum(gaps) / len(gaps), sorted(gaps)[len(gaps) // 2]


def stay_share(D):
    """Share of the statin patients on a practice's register at the start of a seven-month window still on the
    same register at its end, over the record's windows from January 2024."""
    n = s = 0
    starts = [W.day(x) for x in ("2024-01-01", "2024-04-01", "2024-07-01", "2024-10-01", "2025-01-01",
                                "2025-04-01")]
    span = W.OUT - W.ASOF
    for t0 in starts:
        t1 = t0 + span
        for pid in D.statin_by:
            for c, a, b, why in D.reg[pid]:
                if a <= t0 and (b is None or t0 < b):
                    n += 1
                    if b is None or b > t1:
                        s += 1
    return s / n


def current_state(D, pid, code):
    """The patient's current statin repeat at the practice: its issues made, authorised issues, issue length and
    the last statin issue; None when the patient's latest statin issue is acute (the repeat not yet set up)."""
    rows = [r for r in D.statin_by[pid] if r["code"] == code and r["t"] <= W.ASOF]
    last = rows[-1]
    if last["acute"]:
        return dict(kind="acute", last=last["t"], L=28, first=rows[0]["t"])
    tp = D.tpl[last["ref"]]
    made = sum(1 for r in rows if r["ref"] == tp["ref"])
    return dict(kind="repeat", last=last["t"], L=tp["L"], M=tp["M"], made=made, start=tp["start"],
                first=rows[0]["t"], new=rows[0]["acute"] and rows[0]["t"] >= W.EXTRACT_FROM + 30)


def golden(D, pop, rate, bg, pace, stay, pending="lapsed"):
    out = collections.Counter()
    for pid, code in pop.items():
        s = current_state(D, pid, code)
        if s["kind"] == "acute":
            # a new start waiting for its repeat: its review is a year away, only a stop can intervene
            t = s["last"]; prob = 0.0; alive = 1.0; last_issue = t
            while True:
                req = t + 28 + pace
                q = bg[code][0]
                if last_issue < W.W0: prob += alive * q
                alive *= 1 - q
                if req >= W.W0: break
                t = req; last_issue = req
            out[code] += prob * stay
            continue
        L = s["L"]; left = s["M"] - s["made"]
        t = s["last"]; last_issue = t; prob = 0.0; alive = 1.0
        while True:
            req = t + L + pace
            early = s["new"] and t - s["first"] < 182
            q = (bg[code][0] if early else bg[code][1]) * L / 28
            if last_issue < W.W0: prob += alive * q
            alive *= 1 - q
            if left <= 0:
                if req <= W.ASOF - 21:
                    prob += alive * (1.0 if pending == "lapsed" else rate[code])
                elif last_issue < W.W0:
                    prob += alive * rate[code]
                break
            if req >= W.W0: break
            t = req; last_issue = req; left -= 1
        out[code] += min(prob, 1.0) * stay
    return out


# ---------------------------------------------------------------------------------------------- the reflexes
def km_reflex(D, pop, stay, gap=122):
    """Kaplan-Meier on months since the patient's first statin issue in the record, a stop being a statin issue
    followed by 122 days without one; each patient now on a statin carried to the end of February 2027."""
    ev = collections.defaultdict(collections.Counter); ex = collections.defaultdict(collections.Counter)
    for pid, rows in D.statin_by.items():
        ts = [r["t"] for r in rows if r["t"] <= W.ASOF]
        code = rows[-1]["code"]
        if not ts: continue
        a = ts[0]; epis = []
        end_obs = W.ASOF - gap
        for c, ra, rb, why in D.reg[pid]:
            if c == code and rb is not None: end_obs = min(end_obs, rb)
        stops = [ts[i] for i in range(len(ts) - 1) if ts[i + 1] - ts[i] >= gap]
        if ts[-1] + gap <= end_obs + gap and ts[-1] <= end_obs: stops.append(ts[-1])
        for s0 in stops:
            epis.append((a, s0, 1)); nx = [t for t in ts if t > s0]
            if not nx: a = None; break
            a = nx[0]
        if a is not None and end_obs > a: epis.append((a, end_obs, 0))
        for (a0, b, e) in epis:
            m1 = (b - a0) // 30
            for m in range(0, m1 + 1):
                sl, sh = a0 + m * 30, min(b, a0 + (m + 1) * 30)
                if sh > sl: ex[code][min(m, 30)] += (sh - sl) / 30
            if e: ev[code][min(m1, 30)] += 1
    out = collections.Counter()
    for pid, code in pop.items():
        ts = [r["t"] for r in D.statin_by[pid] if r["t"] <= W.ASOF]
        a = (W.ASOF - ts[0]) // 30; surv = 1.0
        for m in range(a, a + (W.W0 - W.ASOF) // 30 + 1):
            mm = min(m, 30)
            e1 = ev[code][mm]; x1 = ex[code][mm]
            surv *= 1 - (e1 / x1 if x1 else 0.0)
        out[code] += (1 - surv) * stay
    return out


def last_year_rate(D, pop):
    A1, O1, W1 = W.day("2025-11-30"), W.day("2026-06-30"), W.day("2026-03-01")
    num = collections.Counter(); den = collections.Counter()
    for pid, rows in D.statin_by.items():
        for c in sorted({r["code"] for r in rows}):
            if not any(r["code"] == c and A1 - 90 < r["t"] <= A1 for r in rows): continue
            if not registered_at(D.reg, pid, c, A1): continue
            if not registered_at(D.reg, pid, c, O1): continue
            den[c] += 1
            if not any(W1 <= r["t"] <= O1 for r in rows): num[c] += 1
    npop = collections.Counter(pop.values())
    return {c: num[c] / den[c] * npop[c] for c in den}


def trailing_stops(D, pop, gap=122):
    """Statin stops (an issue followed by 122 days without one) in the twelve months to the end of July 2026,
    scaled to the patients now on a statin."""
    lo, hi = W.ASOF - 365 - gap, W.ASOF - gap
    st = collections.Counter(); base = collections.Counter()
    for pid, rows in D.statin_by.items():
        ts = [r["t"] for r in rows]
        code = rows[-1]["code"]
        if any(lo - 90 < t <= lo for t in ts): base[code] += 1
        for i, t in enumerate(ts):
            nxt = ts[i + 1] if i + 1 < len(ts) else None
            if lo <= t <= hi and (nxt is None or nxt - t >= gap): st[code] += 1
    npop = collections.Counter(pop.values())
    return {c: st[c] / base[c] * npop[c] * (W.W0 - W.ASOF) / 365 for c in base}


# ---------------------------------------------------------------------------------------------- the asks
DOSE_WORDS = {"one": 1, "1": 1, "two": 2, "2": 2, "half": 0.5}


def doses_per_day(text):
    s = text.lower()
    n = None
    for w0, v in DOSE_WORDS.items():
        if re.search(r"\b%s\b" % re.escape(w0), s):
            n = v; break
    if n is None: n = 1
    if "twice" in s or re.search(r"\bbd\b", s): n *= 2
    return n


def directions_at(D, changes, ref, t):
    """The directions in force for a repeat on a day: the current directions, walked back through the change log."""
    cur = D.tpl[ref]["directions"]
    for (when, old, new) in sorted(changes.get(ref, []), reverse=True):
        if when > t:
            cur = old
    return cur


def load_changes():
    ch = collections.defaultdict(list)
    with open(os.path.join(T, "repeat_changes_2024-01_to_2026-11.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["field"] == "Dosage":
                ch[r["repeat_ref"]].append((dnum(r["changed_on"]), r["old_value"], r["new_value"]))
    return ch


def ask_a(D, use_history=True, drop_cancelled=True, dedup_days=None, fixed_days=None):
    """ACE inhibitor or ARB adherence, 2025: patients registered with the practice throughout 2025 and issued one
    in each quarter, and the share whose 2025 issues covered 80 per cent or more of the year's 365 days."""
    changes = load_changes() if use_history else {}
    y0, y1 = W.day("2025-01-01"), W.day("2025-12-31")
    qs = [(W.day("2025-01-01"), W.day("2025-03-31")), (W.day("2025-04-01"), W.day("2025-06-30")),
          (W.day("2025-07-01"), W.day("2025-09-30")), (W.day("2025-10-01"), W.day("2025-12-31"))]
    by = collections.defaultdict(list)
    for r in D.issues:
        if r["cls"] in ("ACE inhibitor", "Angiotensin II receptor antagonist") and r["t"] <= y1:
            if drop_cancelled and r["cancelled"]: continue
            by[(r["pid"], r["code"])].append(r)
    res = collections.defaultdict(lambda: [0, 0, 0.0])
    for (pid, code), rows in by.items():
        if not any(c == code and a <= y0 and (b is None or b > y1) for c, a, b, why in D.reg[pid]):
            continue
        if not all(any(lo <= r["t"] <= hi for r in rows) for lo, hi in qs):
            continue
        rows.sort(key=lambda r: (r["t"], r["eps"]))
        if dedup_days is not None:
            # the hygiene reflex: a second issue of the same drug within a few days read as a duplicate
            kept, last = [], {}
            for r in rows:
                if r["vtm"] in last and r["t"] - last[r["vtm"]] <= dedup_days:
                    continue
                kept.append(r); last[r["vtm"]] = r["t"]
            rows = kept
        covered = set(); run_end = {}
        for r in rows:
            if r["ref"] and r["ref"] in D.tpl:
                d = directions_at(D, changes, r["ref"], r["t"]) if use_history else D.tpl[r["ref"]]["directions"]
            else:
                d = "ONE daily"
            days = fixed_days if fixed_days else int(round(r["qty"] / doses_per_day(d)))
            start = max(r["t"], run_end.get(r["vtm"], r["t"]))
            end = start + days
            run_end[r["vtm"]] = end
            for x in range(max(start, y0), min(end, y1 + 1)):
                covered.add(x)
        res[code][0] += 1
        if len(covered) >= 0.8 * 365:
            res[code][1] += 1
        res[code][2] += len(covered) / 365.0
    return {c: (v[0], v[1], 100.0 * v[2] / v[0]) for c, v in res.items()}


def load_events():
    ev = collections.defaultdict(list)
    with open(os.path.join(T, "cvd_clinical_events_2023-2026.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            ev[r["patient_ref"]].append((dnum(r["event_date"]), r["practice_code"], r["snomed_concept_id"], r["term"]))
    return ev


def anniversary(t):
    d = W.date_of(t)
    try:
        a = d.replace(year=d.year + 1)
    except ValueError:
        a = d.replace(year=d.year + 1, day=28)
    return (a - W.D0).days


def ask_b(D, anchor="hospital", any_strength=False):
    """Ticagrelor 90mg after a heart attack: patients who started it between 1 July 2024 and 30 June 2025, and how
    many were issued it after the anniversary of the day they started it."""
    lo, hi = W.day("2024-07-01"), W.day("2025-06-30")
    tic = collections.defaultdict(list)
    for r in D.issues:
        if r["vtm"] == "Ticagrelor" and (any_strength or r["strength"] == "90mg") and not r["cancelled"]:
            tic[r["pid"]].append(r)
    res = collections.defaultdict(lambda: [0, 0])
    if anchor == "hospital":
        ev = load_events()
        for pid, rows in ev.items():
            starts = [(t, c) for (t, c, code, term) in rows if code == "1290071000000109"]
            mi = [t for (t, c, code, term) in rows if code == "22298006"]
            for t, c in starts:
                near = [m for m in mi if abs(t - m) <= 3]
                if not (lo <= t <= hi) or not near or not (lo <= near[0] <= hi): continue
                res[c][0] += 1
                if any(r["t"] > anniversary(t) for r in tic.get(pid, [])): res[c][1] += 1
    else:
        for pid, rows in tic.items():
            rows.sort(key=lambda r: r["t"])
            t = rows[0]["t"]; c = rows[0]["code"]
            if not (lo <= t <= hi): continue
            res[c][0] += 1
            if any(r["t"] > anniversary(t) for r in rows): res[c][1] += 1
    return {c: tuple(v) for c, v in res.items()}


# ---------------------------------------------------------------------------------------------- figures
def rnd(v, u=W.ROUND_TO):
    return int(round(v / u) * u)


def pct(num, den, places):
    """A percentage rounded half up, as a return's arithmetic does it, never to the even neighbour."""
    q = decimal.Decimal(100 * num) / decimal.Decimal(den)
    return float(q.quantize(decimal.Decimal(1).scaleb(-places), rounding=decimal.ROUND_HALF_UP))


def figures(D=None, write=True):
    D = D or Data()
    pop = population(D)
    npop = collections.Counter(pop.values())
    rate, n_rev, f_rev = reauth_rate(D)
    bg = stop_rates(D)
    pace_mean, pace_med = pacing(D)
    stay = stay_share(D)
    g = golden(D, pop, rate, bg, pace_mean, stay)
    order = sorted(g, key=lambda c: -g[c])
    call, second = order[0], order[1]
    km = km_reflex(D, pop, stay)
    ly = last_year_rate(D, pop)
    tr = trailing_stops(D, pop)
    a = ask_a(D)
    b = ask_b(D)
    name = {p["code"]: p["name"] for p in W.PRACTICES}
    pool_rate = list(rate.values())[0]
    # the patients whose current statin repeat is six 56-day issues authorised in February or March 2026
    six56 = collections.Counter()
    for pid, c in pop.items():
        s = current_state(D, pid, c)
        if s["kind"] == "repeat" and s["M"] == 6 and s["L"] == 56 and W.day("2026-02-01") <= s["start"] <= W.day("2026-03-31"):
            six56[c] += 1
    F = dict(
        call=call, call_name=name[call], runner_up=second, runner_up_name=name[second], ranking=order,
        expected={c: g[c] for c in g}, expected_rounded={c: rnd(g[c]) for c in g},
        call_expected=rnd(g[call]), runner_up_expected=rnd(g[second]), gap=rnd(g[call]) - rnd(g[second]),
        population=dict(npop), reauth_fail_pct=round(100 * pool_rate, 1), reauth_fail_whole=int(round(100 * pool_rate)),
        reviews_measured=sum(n_rev.values()), reviews_not_renewed=sum(f_rev.values()),
        stop_rate_late_per_28d=list(bg.values())[0][1], stop_rate_early_per_28d=list(bg.values())[0][0],
        pace_mean=pace_mean, stay=stay, stay_pct=round(100 * stay, 1),
        stop_rate_early_pct=round(100 * list(bg.values())[0][0], 2), stop_rate_late_pct=round(100 * list(bg.values())[0][1], 2),
        stop_gap_days=150, reauth_follow_days=60, return_year=W.RETURN_YEAR, population_total=sum(npop.values()),
        default_km={c: km[c] for c in km}, default_pick=max(km, key=km.get), default_pick_name=name[max(km, key=km.get)],
        last_year={c: ly[c] for c in ly}, last_year_pick=max(ly, key=ly.get),
        trailing={c: tr[c] for c in tr}, trailing_pick=max(tr, key=tr.get),
        largest_practice=max(npop, key=npop.get), six_56day_feb_mar_2026={c: six56[c] for c in npop},
        ask_a={c: dict(patients=a[c][0], at_80=a[c][1], pct=pct(a[c][1], a[c][0], 1)) for c in a},
        ask_b={c: dict(started=b[c][0], overrun=b[c][1], pct=pct(b[c][1], b[c][0], 0)) for c in b},
        ask_a_network=dict(patients=sum(v[0] for v in a.values()), at_80=sum(v[1] for v in a.values()),
                           pct=pct(sum(v[1] for v in a.values()), sum(v[0] for v in a.values()), 1)),
        ask_b_network=dict(started=sum(v[0] for v in b.values()), overrun=sum(v[1] for v in b.values()),
                           pct=pct(sum(v[1] for v in b.values()), sum(v[0] for v in b.values()), 0)),
    )
    if write:
        with open(FIG, "w", encoding="utf-8") as fh:
            json.dump(F, fh, indent=1, sort_keys=True)
    return F


def main():
    F = figures()
    print("  figures.json: call %s %d, runner-up %s %d" % (F["call_name"], F["call_expected"], F["runner_up_name"],
                                                         F["runner_up_expected"]))


if __name__ == "__main__":
    main()
