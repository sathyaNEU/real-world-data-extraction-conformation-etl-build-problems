"""Every figure the build asserts, computed from the files in target/ as shipped, and the three
deliverables the prompt names.

One parameterised pipeline covers the golden path, the natural path (each device mishandled), the
over-corrections and the main ladder's rungs and grid cells, so a figure and its stops come from the same
code. The independent verifier (verify.py) recomputes the load-bearing figures on its own code path.

Run as a script (python3 golden.py [--target DIR] [--out DIR]) it reads only target/, writes
external_review_placement_2027-28.docx, review_placement_workings.xlsx and review_placement_by_trust.png
into golden/, and prints the figures the critical components name.
"""
import bisect
import datetime as dt
import zoneinfo
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

TZ = zoneinfo.ZoneInfo("Europe/London")
UTC = dt.timezone.utc
LETTER_OF = {"RIS": "A", "TAN": "B", "BRK": "C", "STN": "D", "LAT": "E", "ELL": "F", "PRW": "G", "PEL": "H"}
CODES = ["RIS", "TAN", "BRK", "STN", "LAT", "ELL", "PRW", "PEL"]
YEARS = {1: (dt.date(2023, 7, 1), dt.date(2024, 6, 30)), 2: (dt.date(2024, 7, 1), dt.date(2025, 6, 30)),
         3: (dt.date(2025, 7, 1), dt.date(2026, 6, 30))}
DEVICES = ("DV1", "DV2", "DV3", "DV4", "DV5", "DV7", "DV8", "DV9", "HZ1", "HZ2")
TRANSFER_TYPES = ("02", "03", "06")
# readings of "an admission the trust placed itself": the admitted patient's referring trust (the golden), the bureau's
# audit, and the admission-type and queue readings the construction layer prices
READINGS = ("referral", "audit", "local", "t04", "planned", "not02", "queue")
EPOCH = dt.datetime(2023, 1, 1)


def mins(t):
    return int((t - EPOCH).total_seconds() // 60)


def p_ts(s):
    return None if (s is None or s == "" or (isinstance(s, float))) else dt.datetime.strptime(s, "%Y-%m-%d %H:%M")


def utc_to_local(t):
    return t.replace(tzinfo=UTC).astimezone(TZ).replace(tzinfo=None)


def local_to_utc(t):
    return t.replace(tzinfo=TZ).astimezone(UTC).replace(tzinfo=None)


def year_of(d):
    for y, (a, b) in YEARS.items():
        if a <= d <= b:
            return y
    return None


class Data:
    """The shipped files, parsed once."""

    def __init__(self, target, F):
        T = Path(target)
        self.F = F
        self.ref = pd.read_csv(T / F["referrals"], dtype=str, keep_default_na=False)
        self.lev = pd.read_csv(T / F["levels"], dtype=str, keep_default_na=False)
        self.links = pd.read_csv(T / F["links"], dtype=str, keep_default_na=False)
        st = pd.read_parquet(T / F["stays"])
        st["referral_id"] = st["referral_id"].fillna("")
        self.stays = st
        self.ret = pd.read_csv(T / F["returns"], dtype={"beds_open": int, "beds_occupied_0800": int})
        self.reg = pd.read_csv(T / F["register"], dtype=str, keep_default_na=False)
        ep = pd.read_parquet(T / F["episodes"], columns=["patient_key", "date_of_death", "discharge_method",
                                                        "discharge_date", "spell_id"])
        self.ep = ep
        dod = ep.dropna(subset=["date_of_death"]).groupby("patient_key")["date_of_death"].min()
        self.dod = {k: v for k, v in dod.items()}
        self.temp = dict(zip(self.links["temporary_key"], self.links["verified_key"]))
        self.merged_verified = set(self.links["verified_key"])
        # deaths recorded only as a spell ending in death (discharge method 4), per key as linked
        died = ep[ep["discharge_method"] == "4"].dropna(subset=["discharge_date"])
        dm = {}
        for k, d in zip(died["patient_key"], died["discharge_date"]):
            for kk in {k, self.temp.get(k, k)}:
                if kk not in dm or d < dm[kk]:
                    dm[kk] = d
        self.dmeth = dm
        self.tx = pd.read_csv(T / F["transfers"], dtype=str, keep_default_na=False)
        # decision level and the set of levels entered, per migrated referral
        dec = self.lev[self.lev["entry"] == "DECISION"]
        self.dec_level = dict(zip(dec["referral_id"], dec["level"].astype(int)))
        self.levels_seen = self.lev.groupby("referral_id")["level"].nunique().to_dict()
        # returns and register
        self.beds_on = {(r.unit_code, r.return_date): r.beds_open for r in self.ret.itertuples()}
        self.occ0800 = {(r.unit_code, r.return_date): r.beds_occupied_0800 for r in self.ret.itertuples()}
        self.reg_rows = [(r.unit_code, r.trust_code, int(r.care_level), int(r.commissioned_beds),
                          dt.date.fromisoformat(r.valid_from), dt.date.fromisoformat(r.valid_to) if r.valid_to else None)
                         for r in self.reg.itertuples()]
        self.unit_trust = {r[0]: r[1] for r in self.reg_rows}
        self.ref_trust = dict(zip(self.ref["referral_id"], self.ref["referring_trust"]))
        self._prep_stays()
        self._prep_refs()

    # ------------------------------------------------------------------------ stays and census
    def _prep_stays(self):
        st = self.stays.sort_values(["unit_code", "patient_key", "admitted_at", "stay_id"]).reset_index(drop=True)
        raw, legacy = [], []
        for r in st.itertuples(index=False):
            raw.append((r.unit_code, r.patient_key, mins(r.admitted_at.to_pydatetime()),
                        mins(r.discharged_at.to_pydatetime()), r.admission_type, r.referral_id))
            legacy.append(r.stay_id.startswith("LB"))
        res = lambda k: self.temp.get(k, k)
        # the bureau's audit: a legacy transfer's row begins at the arrival, its bed was allocated earlier
        held, self.audit_at = {}, set()
        transit = []
        for r in self.tx.itertuples(index=False):
            conf, arr = mins(p_ts(r.bed_confirmed_at)), mins(p_ts(r.arrived_at))
            self.audit_at.add((r.to_unit, res(r.patient_key), conf))
            if conf < GO_MIN:
                held[(r.to_unit, res(r.patient_key), arr)] = conf
                transit.append(arr - conf)
        self.median_transit = int(pd.Series(transit).median()) if transit else 0
        handled, over = [], []
        prev_end = {}
        for (u, k, a, b, typ, rid), lg in zip(raw, legacy):
            a2 = held.get((u, res(k), a), a) if (lg and rid) else a
            handled.append((u, k, a2, b, typ, rid))
            start = lg and prev_end.get((u, k)) != a          # an admission, not a move to another bed
            over.append((u, k, a - self.median_transit if start else a, b, typ, rid))
            prev_end[(u, k)] = b
        self.n_held = sum(1 for x, y in zip(raw, handled) if x[2] != y[2])
        self.units = sorted({r[0] for r in raw})
        self.views = {}
        for name, rows in (("handled", handled), ("raw", raw), ("over", over)):
            assign_of = {}
            for u, k, a, b, typ, rid in rows:
                if rid and (rid not in assign_of or a < assign_of[rid][1]):
                    assign_of[rid] = (u, a)
            merged = self.merge_rows(rows, gap=0)
            self.views[name] = {"rows": rows, "assign_of": assign_of, "merged": merged,
                                "census": {u: self.occ_series(merged, u) for u in self.units}}
        V = self.views["handled"]
        self.stay_rows, self.assign_of, self.merged, self.census = V["rows"], V["assign_of"], V["merged"], V["census"]

    def view(self, handle, over=None):
        """The unit feed as read: legacy transfers dated from the bureau's allocation (DV8 handled), as shipped
        (from the arrival), or every legacy admission moved back by the audit's median transit (over-correction)."""
        if over == "DV8":
            return self.views["over"]
        return self.views["handled" if "DV8" in handle else "raw"]

    def death(self, person, handle=None, over=None):
        """Date of death: the linked date of death; where none is linked, a spell ending in death (DV9 handled);
        the over-correction reads every death from the discharge method alone."""
        handle = DEVICES if handle is None else handle
        if over == "DV9":
            return self.dmeth.get(person)
        d = self.dod.get(person)
        if d is None and "DV9" in handle:
            d = self.dmeth.get(person)
        return d

    @staticmethod
    def merge_rows(rows, gap=0):
        """Contiguous rows of one patient in one unit become one stay (gap in minutes allowed)."""
        out = []
        by = defaultdict(list)
        for r in rows:
            by[(r[0], r[1])].append(r)
        for key in sorted(by):
            lst = sorted(by[key], key=lambda x: (x[2], x[3]))
            cur = list(lst[0])
            for r in lst[1:]:
                if r[2] - cur[3] <= gap and r[2] >= cur[3]:
                    cur[3] = max(cur[3], r[3])
                else:
                    out.append(tuple(cur))
                    cur = list(r)
            out.append(tuple(cur))
        return out

    @staticmethod
    def occ_series(rows, u):
        ev = defaultdict(int)
        for r in rows:
            if r[0] != u:
                continue
            ev[r[2]] += 1
            ev[r[3]] -= 1
        ts, vs, c = [], [], 0
        for t in sorted(ev):
            c += ev[t]
            ts.append(t)
            vs.append(c)
        return ts, vs

    def beds_at(self, u, t, fallback=None):
        d = (EPOCH + dt.timedelta(minutes=t)).date().isoformat()
        b = self.beds_on.get((u, d))
        if b is None and fallback is not None:
            return fallback
        return b

    def empty_during(self, u, a, b, census=None, fallback=None, mode="any"):
        """True when the unit held an empty staffed bed during [a, b): any moment, or every moment."""
        ts, vs = (census or self.census)[u]
        i = bisect.bisect_right(ts, a) - 1
        occ = vs[i] if i >= 0 else 0
        pts = [(a, occ)]
        j = i + 1
        while j < len(ts) and ts[j] < b:
            pts.append((ts[j], vs[j]))
            j += 1
        flags = []
        for t, o in pts:
            beds = self.beds_at(u, t, fallback)
            if beds is None:
                flags.append(False)
            else:
                flags.append(o < beds)
        return any(flags) if mode == "any" else all(flags)

    def hourly_empty(self, u, a, b):
        t = (a // 60 + 1) * 60
        while t < b:
            ts, vs = self.census[u]
            i = bisect.bisect_right(ts, t) - 1
            o = vs[i] if i >= 0 else 0
            beds = self.beds_at(u, t)
            if beds is not None and o < beds:
                return True
            t += 60
        return False

    def admissions(self, rows):
        by = defaultdict(list)
        for u, k, a, b, typ, rid in rows:
            by[(u, typ)].append(a)
        for v in by.values():
            v.sort()
        return by

    def is_transfer_op(self, u, rid):
        """A stay is a transfer between trusts when another trust referred the patient."""
        t = self.ref_trust.get(rid) if rid else None
        return t is not None and t != self.unit_trust.get(u)

    def adm_index(self, rows):
        """Per unit: admission minutes of every stay ("all") and of the stays each reading takes as the trust's own
        placement: not referred by another trust (referral, the golden), not in the bureau's audit (audit), by
        the admission type (local 01/04/05, t04, planned 03/04/05, not02), and the queue reading's pairs
        (admission minute, the admitted patient's decision or None)."""
        res = lambda k: self.temp.get(k, k)
        tmp = defaultdict(lambda: {k: [] for k in ("all",) + READINGS})
        for u, k, a, b, typ, rid in rows:
            m = tmp[u]
            m["all"].append(a)
            if not self.is_transfer_op(u, rid):
                m["referral"].append(a)
            if (u, res(k), a) not in self.audit_at:
                m["audit"].append(a)
            if typ in ("01", "04", "05"):
                m["local"].append(a)
            if typ == "04":
                m["t04"].append(a)
            if typ in ("03", "04", "05"):
                m["planned"].append(a)
            if typ != "02":
                m["not02"].append(a)
            m["queue"].append((a, self.ref_dta_local.get(rid) if rid else None))
        for m in tmp.values():
            for k in m:
                m[k].sort(key=lambda v: v if isinstance(v, int) else (v[0], -1 if v[1] is None else v[1]))
            m["queue_t"] = [t for t, q in m["queue"]]
            m["queue_q"] = [q for t, q in m["queue"]]
        return dict(tmp)

    # ------------------------------------------------------------------------ referrals
    def _prep_refs(self):
        R = self.ref
        out = []
        for r in R.itertuples(index=False):
            out.append({"id": r.referral_id, "legacy": r.referral_id.startswith("CC"), "rec": p_ts(r.received_at),
                        "dta": p_ts(r.dta_at), "trust": r.referring_trust, "ward": r.referred_from,
                        "key": r.patient_key, "level": int(r.level_of_care), "outcome": r.outcome,
                        "out": p_ts(r.outcome_at), "unit": r.admitting_unit})
        self.refs = out
        self.ref_dta_local = {x["id"]: mins(utc_to_local(x["dta"]) if x["legacy"] else x["dta"]) for x in out
                              if x["dta"] is not None}
        # parallel-run pairs: a platform row a few minutes after a CCRS row for the same patient and trust
        cc = defaultdict(list)
        for x in out:
            if x["legacy"] and x["dta"] is not None:
                cc[(x["key"], x["trust"])].append(x["dta"])
        self.copies = set()
        for x in out:
            if x["legacy"] or x["dta"] is None or not (dt.date(2024, 2, 19) <= x["dta"].date() <= dt.date(2024, 4, 1)):
                continue
            for t0 in cc.get((x["key"], x["trust"]), []):
                if dt.timedelta(0) <= x["dta"] - t0 <= dt.timedelta(minutes=30):
                    self.copies.add(x["id"])
                    break

    def own_units(self, trust, d, current_only=False, any_date=False):
        res = []
        for (u, t, lv, beds, a, z) in self.reg_rows:
            if t != trust or lv != 3:
                continue
            if current_only:
                if z is None:
                    res.append(u)
            elif any_date:
                res.append(u)
            elif a <= d and (z is None or d <= z):
                res.append(u)
        return sorted(set(res))

    def l3_units(self, d):
        return sorted({u for (u, t, lv, beds, a, z) in self.reg_rows if lv == 3 and a <= d and (z is None or d <= z)})

    def reg_beds(self, u):
        return max(b for (x, t, lv, b, a, z) in self.reg_rows if x == u and lv == 3)


# ================================================================================ the pipeline
CHANGE_EVES = {dt.date(2023, 10, 28), dt.date(2023, 10, 29), dt.date(2024, 3, 30), dt.date(2024, 3, 31),
               dt.date(2024, 10, 26), dt.date(2024, 10, 27), dt.date(2025, 3, 29), dt.date(2025, 3, 30),
               dt.date(2025, 10, 25), dt.date(2025, 10, 26), dt.date(2026, 3, 28), dt.date(2026, 3, 29)}
GO_MIN = mins(dt.datetime(2024, 4, 2))


def waits(D, handle=None, over=None):
    """One record per referral that could be a long wait: decision level, local decision time, end,
    patient, death. handle: devices handled (default all). over: one over-correction name or None."""
    handle = set(DEVICES if handle is None else handle)
    V = D.view(handle, over)
    out = []
    shift_all = over == "DV1"
    for r in D.refs:
        dta, rec, end = r["dta"], r["rec"], r["out"]
        dta_utc = end_utc = None
        if r["legacy"]:
            if "DV1" in handle:
                if shift_all:
                    dta = dta + dt.timedelta(hours=1)
                    rec = rec + dt.timedelta(hours=1)
                    end = end + dt.timedelta(hours=1) if end is not None else None
                else:
                    dta_utc, end_utc = dta, end
                    dta, rec = utc_to_local(dta), utc_to_local(rec)
                    end = utc_to_local(end) if end is not None else None
            if r["outcome"] == "Admitted":
                a = V["assign_of"].get(r["id"])
                end = (EPOCH + dt.timedelta(minutes=a[1])) if a else None
                end_utc = None
            level = D.dec_level.get(r["id"], r["level"]) if "DV4" in handle else r["level"]
            if over == "DV4" and D.levels_seen.get(r["id"], 1) > 1:
                continue
        else:
            level = r["level"]
        if over == "DV5" and dta is not None and dta.date() in CHANGE_EVES:
            continue
        key = r["key"]
        if over == "DV2" and (key in D.temp or key in D.merged_verified):
            continue              # every referral of a patient whose identity was ever merged, dropped
        person = D.temp.get(key, key) if "DV2" in handle else key
        out.append({"id": r["id"], "legacy": r["legacy"], "trust": r["trust"], "dta": dta, "rec": rec, "end": end,
                    "dta_utc": dta_utc, "end_utc": end_utc, "level": level, "outcome": r["outcome"],
                    "person": person, "key": key, "unit": r["unit"]})
    if over == "HZ2":
        seen = set()
        keep = []
        for w in sorted(out, key=lambda x: (x["rec"], x["id"])):
            k = (w["person"], w["dta"].date())
            if k in seen:
                continue
            seen.add(k)
            keep.append(w)
        out = keep
    return out


def wait_minutes(w, handle):
    """Length of the wait: elapsed time (DV5 handled) or the difference of the clock readings."""
    if "DV5" in handle:
        sa = w["dta_utc"] if w["dta_utc"] is not None else local_to_utc(w["dta"])
        sb = w["end_utc"] if w["end_utc"] is not None else local_to_utc(w["end"])
        return mins(sb) - mins(sa)
    return mins(w["end"]) - mins(w["dta"])


def _inside(lst, a, b):
    i = bisect.bisect_right(lst, a)
    return i < len(lst) and lst[i] < b


def classify(D, ws, handle=None, over=None, construction="decisive", scope="own", basis="census"):
    """Mark each long wait with its death and own-care readings: an empty staffed bed (census), any admission
    to the unit during the wait (alloc_any), an admission the unit's trust placed itself (alloc: the admitted
    patient's referring trust), and the other readings of own placement (alloc_<reading>)."""
    handle = set(DEVICES if handle is None else handle)
    V = D.view(handle, over)
    vname = "over" if over == "DV8" else ("handled" if "DV8" in handle else "raw")
    hz1 = (vname, "HZ1" in handle, over == "HZ1")
    cache = D.__dict__.setdefault("_idx_cache", {})
    if hz1 not in cache:
        if "HZ1" in handle:
            rows = V["merged"] if over != "HZ1" else D.merge_rows(V["rows"], gap=24 * 60)
        else:
            rows = V["rows"]
        cache[hz1] = D.adm_index(rows)
    idx = cache[hz1]
    census = V["census"]
    res = []
    for w in ws:
        if w["level"] != 3 or w["outcome"] == "Stood down" or w["end"] is None:
            continue
        if wait_minutes(w, handle) <= 240:
            continue
        a, b = mins(w["dta"]), mins(w["end"])
        d = w["dta"].date()
        death = D.death(w["person"], handle, over)
        died = False
        if death is not None:
            off = (death - d).days
            died = 0 <= off <= 30
        if "DV3" in handle:
            if over == "DV3":
                own = D.own_units(w["trust"], d, any_date=True)
            else:
                own = D.own_units(w["trust"], d)
        else:
            own = D.own_units(w["trust"], d, current_only=True)
        units = own if scope == "own" else D.l3_units(d)
        if over == "DV3" and scope == "own":
            units = own
        empty = False
        alloc_any = False
        flags = {rd: False for rd in READINGS}
        v0800 = False
        for u in units:
            if u not in census:
                if over == "DV3":
                    empty = True
                continue
            fb = D.reg_beds(u) if over == "DV3" else None
            if D.empty_during(u, a, b, census=census, fallback=fb):
                empty = True
            m = idx.get(u)
            if m is not None:
                if _inside(m["all"], a, b):
                    alloc_any = True
                for rd in READINGS:
                    if rd == "queue":
                        j = bisect.bisect_right(m["queue_t"], a)
                        while j < len(m["queue_t"]) and m["queue_t"][j] < b:
                            q = m["queue_q"][j]
                            if q is None or q > a:
                                flags["queue"] = True
                                break
                            j += 1
                    elif _inside(m[rd], a, b):
                        flags[rd] = True
            k = (u, d.isoformat())
            if k in D.occ0800 and D.occ0800[k] < D.beds_on[k]:
                v0800 = True
        res.append(dict(w, died=died, has_own=bool(own), empty=empty, alloc=flags["referral"], alloc_any=alloc_any,
                        v0800=v0800, a=a, b=b, year=year_of(d),
                        **{"alloc_" + rd: flags[rd] for rd in READINGS[1:]}))
    return res


CLS_DEV = frozenset(("DV1", "DV2", "DV3", "DV4", "DV5", "DV8", "DV9", "HZ1"))


def classified(D, handle, over=None):
    """classify() over waits(), cached on the devices that change either (the counting devices DV7 and HZ2
    act in asks())."""
    key = (frozenset(set(handle) & CLS_DEV), over)
    cache = D.__dict__.setdefault("_cl_cache", {})
    if key not in cache:
        cache[key] = classify(D, waits(D, handle, over), handle, over)
    return cache[key]


def confirmable(x, construction):
    if construction == "decisive":
        return x["empty"] or x["alloc"]
    if construction == "census":
        return x["empty"]
    if construction == "any":
        return x["empty"] or x["alloc_any"]
    if construction in READINGS[1:]:
        return x["empty"] or x["alloc_" + construction]
    raise ValueError(construction)


def asks(D, handle=None, over=None, construction="decisive", per_referral_deaths=None, years=(1, 2, 3)):
    """3a, 3b, 3c per trust (and total) over the given years. DV7 mishandled counts referral rows instead of
    patients in every column, parallel-run copies dropped where HZ2 is handled; HZ2 mishandled counts deaths per
    referral row, copies included, while patients are still counted as people. per_referral_deaths overrides."""
    handle = set(DEVICES if handle is None else handle)
    if per_referral_deaths is None:
        per_referral_deaths = not {"HZ2", "DV7"} <= handle
    cl = classified(D, handle, over)
    if over == "DV7":
        n = Counter((x["trust"], x["person"]) for x in cl if x["id"] not in D.copies)
        cl = [x for x in cl if n[(x["trust"], x["person"])] == 1]
    a3 = defaultdict(set)
    b3 = defaultdict(set)
    c3 = defaultdict(set)
    for x in cl:
        if x["year"] not in years:
            continue
        t = x["trust"]
        if "DV7" in handle:
            a3[t].add(x["person"])
        elif not ("HZ2" in handle and x["id"] in D.copies):
            a3[t].add(x["id"])
        tag = x["id"] if per_referral_deaths else x["person"]
        if per_referral_deaths and "HZ2" in handle and x["id"] in D.copies:
            tag = None
        if x["died"] and tag is not None:
            b3[t].add(tag)
            if confirmable(x, construction):
                c3[t].add(tag)
    out = {t: (len(a3[t]), len(b3[t]), len(c3[t])) for t in CODES}
    out["total"] = tuple(sum(out[t][i] for t in CODES) for i in range(3))
    return out


RUNGS = ("raw", "0800", "census", "any", "decisive")


def ladder(D, year=3):
    """The main call's rungs on the latest four quarters: deaths per trust. 0 every long-wait death; 1 the own
    unit's 08:00 return showed an empty staffed bed that day; 2 the census shows an empty staffed bed during the
    wait; 3 an empty bed or any admission to the own unit during the wait; 4 an empty bed or an admission the
    trust placed itself (the decisive construction)."""
    ws = waits(D)
    cl = [x for x in classify(D, ws) if x["year"] == year]
    rung = {k: defaultdict(set) for k in range(5)}
    for x in cl:
        if not x["died"]:
            continue
        t, p = x["trust"], x["person"]
        rung[0][t].add(p)
        if x["has_own"]:
            if x["v0800"]:
                rung[1][t].add(p)
            if x["empty"]:
                rung[2][t].add(p)
            if x["empty"] or x["alloc_any"]:
                rung[3][t].add(p)
            if x["empty"] or x["alloc"]:
                rung[4][t].add(p)
    return {k: {t: len(rung[k][t]) for t in CODES} for k in range(5)}, cl


def year_table(D, year=3):
    ws = waits(D)
    cl = [x for x in classify(D, ws) if x["year"] == year]
    pats, deaths, conf = defaultdict(set), defaultdict(set), defaultdict(set)
    for x in cl:
        pats[x["trust"]].add(x["person"])
        if x["died"]:
            deaths[x["trust"]].add(x["person"])
            if x["empty"] or x["alloc"]:
                conf[x["trust"]].add(x["person"])
    return {t: (len(pats[t]), len(deaths[t]), len(conf[t])) for t in CODES}


def grid(D, year=3):
    """Eighteen cells: occupancy basis (none, 08:00, census) by unit scope (own, network) by allocation
    reading (ignored, any admission, an admission the trust placed itself)."""
    ws = waits(D)
    cells = {}
    cl_own = [x for x in classify(D, ws, scope="own") if x["year"] == year and x["died"]]
    cl_net = [x for x in classify(D, ws, scope="network") if x["year"] == year and x["died"]]
    for basis in ("none", "0800", "census"):
        for scope, cl in (("own", cl_own), ("network", cl_net)):
            for alloc in ("ignored", "any", "placed"):
                cnt = defaultdict(set)
                for x in cl:
                    if scope == "own" and not x["has_own"]:
                        continue
                    extra = (alloc == "any" and x["alloc_any"]) or (alloc == "placed" and x["alloc"])
                    if basis == "none":
                        ok = True
                    elif basis == "0800":
                        ok = x["v0800"] or extra
                    else:
                        ok = x["empty"] or extra
                    if ok:
                        cnt[x["trust"]].add(x["person"])
                cells[(basis, scope, alloc)] = {t: len(cnt[t]) for t in CODES}
    return cells


def readings(D, year=3):
    """Deaths per trust on the latest four quarters under each reading of own placement (an empty staffed bed in
    the own unit during the wait, or an admission the reading takes as the trust's own), and under any admission."""
    cl = [x for x in classify(D, waits(D)) if x["year"] == year and x["died"] and x["has_own"]]
    out = {}
    for rd in ("any",) + READINGS:
        cnt = defaultdict(set)
        for x in cl:
            ok = x["empty"] or (x["alloc_any"] if rd == "any" else x["alloc"] if rd == "referral" else x["alloc_" + rd])
            if ok:
                cnt[x["trust"]].add(x["person"])
        out[rd] = {t: len(cnt[t]) for t in CODES}
    return out


def leader(counts):
    s = sorted(((v, k) for k, v in counts.items()), reverse=True)
    (v1, k1), (v2, k2) = s[0], s[1]
    return k1, v1, k2, v2, (v1 / v2 if v2 else float("inf"))


# ================================================================================ the deliverables
FILES = dict(
    transfers="interhospital_transfer_audit_202307_202606.csv",
    referrals="critical_care_referrals_202307_202606.csv",
    stays="acc_unit_stays_202306_202606.parquet",
    returns="acc_bed_return_0800_202306_202606.csv",
    episodes="apc_episodes_referred_patients_2022-2026.parquet",
    register="acc_unit_register.csv",
    levels="ccrs_referral_levels_202307_202604.csv",
    links="pas_patient_key_links_2023-2026.csv",
)
NAME = {"RIS": "Ristenholm Teaching Hospitals NHS Foundation Trust", "TAN": "Tannerby Hospital NHS Trust",
        "BRK": "Brackenford Hospitals NHS Foundation Trust",
        "STN": "Stennock University Hospitals NHS Foundation Trust", "LAT": "Lathingbury Hospitals NHS Trust",
        "ELL": "Ellerdyke Hospitals NHS Trust", "PRW": "Prideswick Hospitals NHS Foundation Trust",
        "PEL": "Pellowham Hospitals NHS Trust"}
SHORT = {"RIS": "Ristenholm", "TAN": "Tannerby", "BRK": "Brackenford", "STN": "Stennock", "LAT": "Lathingbury",
         "ELL": "Ellerdyke", "PRW": "Prideswick", "PEL": "Pellowham"}
DELIVERABLES = ("external_review_placement_2027-28.docx", "review_placement_workings.xlsx",
                "review_placement_by_trust.png")
PAPER_DATE = dt.date(2026, 10, 2)
BOARD = "Wenmarsh Regional Health Board"
INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df", "#fcfcfb"
CONF_COL, REST_COL = "#2a78d6", "#cfcdc6"


def figures(D):
    """Everything the three deliverables quote, from one pass over the shipped files."""
    R, cl = ladder(D)
    y3 = year_table(D)
    rec = asks(D)
    by_year = {y: asks(D, years=(y,)) for y in (1, 2, 3)}
    call, cv, run, rv, _ = leader(R[4])
    # what held each latest-year long wait behind a death, per trust
    held = {t: {"empty": 0, "alloc": 0, "bureau": 0, "capacity": 0, "no_l3": 0} for t in CODES}
    waits_l3 = {t: 0 for t in CODES}
    for x in cl:
        if not x["has_own"]:
            if x["died"]:
                held[x["trust"]]["no_l3"] += 1
            continue
        waits_l3[x["trust"]] += 1
        if x["died"]:
            k = ("empty" if x["empty"] else "alloc" if x["alloc"] else "bureau" if x["alloc_any"] else "capacity")
            held[x["trust"]][k] += 1
    stn_waits_alloc = sum(1 for x in cl if x["trust"] == call and x["alloc"] and not x["empty"])
    # the statements the paper makes in words, back-tested on the record
    assert stn_waits_alloc == y3[call][0] and all(x["dta"].weekday() < 5 for x in cl if x["trust"] == call)
    assert not any(x["alloc"] for x in cl if x["trust"] != call and not x["empty"])
    assert R[3]["RIS"] == held["RIS"]["empty"] + held["RIS"]["bureau"] and R[3]["RIS"] > R[3][call]
    # the paper's table splits these trusts' deaths into what held the waits: the parts tie to the row
    for t in ("RIS", "PRW"):
        assert sum(held[t][k] for k in ("empty", "alloc", "bureau", "capacity")) == y3[t][1]
    # every bed the full unit gave away during a Ristenholm wait went to a patient referred by a trust that held
    # no level 3 beds on that date (the paper says so)
    rows = sorted((u, a, rid) for u, k, a, b, typ, rid in D.merged if u == "RIS-ACC")
    ref_by = {r["id"]: r for r in D.refs}
    typ_at = {(u, a): typ for u, k, a, b, typ, rid in D.merged}
    key_at = {(u, a): k for u, k, a, b, typ, rid in D.merged}
    n_planned = 0
    for x in cl:
        if x["trust"] != "RIS" or not x["alloc_any"] or x["empty"]:
            continue
        inside = [(a, rid) for u, a, rid in rows if x["a"] < a < x["b"]]
        assert inside and all(D.is_transfer_op("RIS-ACC", rid) and
                              not D.own_units(ref_by[rid]["trust"], ref_by[rid]["dta"].date()) for a, rid in inside)
        if x["died"] and any(typ_at[("RIS-ACC", a)] == "03" for a, rid in inside):
            n_planned += 1
    # "many of those patients came in as planned transfers"
    assert 2 * n_planned > held["RIS"]["bureau"], (n_planned, held["RIS"]["bureau"])
    # "the unit feed codes these patients as planned transfers in, but each was referred by Stennock itself and none
    # passed through the network's bed bureau"
    stn_rows = sorted((a, rid) for u, k, a, b, typ, rid in D.merged if u == "STN-ACC")
    for x in cl:
        if x["trust"] != call:
            continue
        inside = [(a, rid) for a, rid in stn_rows if x["a"] < a < x["b"]]
        assert inside and all(typ_at[("STN-ACC", a)] == "03" and rid and ref_by[rid]["trust"] == call and
                              ref_by[rid]["ward"] == "REC" and
                              ("STN-ACC", D.temp.get(key_at[("STN-ACC", a)], key_at[("STN-ACC", a)]), a)
                              not in D.audit_at for a, rid in inside)
    assert all(x["dta"].hour >= 18 and not x["empty"] for x in cl if x["trust"] == "BRK")
    ret = D.ret[(D.ret.unit_code == "BRK-ACC") & (D.ret.return_date >= "2025-07-01") &
                (D.ret.return_date <= "2026-06-30")]
    assert (ret.beds_occupied_0800 < ret.beds_open).sum() * 2 > len(ret)
    # "at weekends no Stennock referral waited more than four hours": every level, open waits included
    for w in waits(D):
        if w["trust"] == call and w["dta"].weekday() >= 5 and year_of(w["dta"].date()) == 3:
            assert w["end"] is not None and w["end"] - w["dta"] <= dt.timedelta(hours=4)
    # "the most confirmable deaths in each four-quarter year", with Prideswick second each year
    for y in (1, 2, 3):
        yr = sorted(CODES, key=lambda t: -by_year[y][t][2])
        assert yr[0] == call and yr[1] == run and by_year[y][call][2] > by_year[y][run][2]
    # chart order: confirmable deaths, then deaths inside the remit, then name
    order = sorted(CODES, key=lambda t: (-y3[t][2], -y3[t][1], SHORT[t]))
    assert order[0] == call and order[1] == run
    assert cv == y3[call][2] and rv == y3[run][2]
    assert rec["total"] == tuple(sum(rec[t][i] for t in CODES) for i in range(3))
    assert all(by_year[3][t] == y3[t] for t in CODES)
    return dict(R=R, y3=y3, rec=rec, by_year=by_year, call=call, cv=cv, run=run, rv=rv, gap=cv - rv,
                held=held, waits=y3, stn_waits_alloc=stn_waits_alloc, order=order,
                y3_total=tuple(sum(y3[t][i] for t in CODES) for i in range(3)))


# ---------------------------------------------------------------------------------------- chart
def chart_png(fx, path=None):
    import io
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch

    y3, order, call, run = fx["y3"], fx["order"], fx["call"], fx["run"]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5})
    fig, ax = plt.subplots(figsize=(7.4, 4.5), dpi=200)
    fig.patch.set_facecolor(SURF)
    ax.set_facecolor(SURF)
    n = len(order)
    ys = {t: n - 1 - i for i, t in enumerate(order)}
    h = 0.56
    for t in order:
        deaths, conf = y3[t][1], y3[t][2]
        if deaths > conf:
            ax.barh(ys[t], deaths - conf, left=conf, height=h, color=REST_COL, zorder=2, lw=0)
        if conf:
            ax.barh(ys[t], conf, height=h, color=CONF_COL, zorder=3, lw=0)
            if deaths > conf:   # surface gap between the two parts
                ax.plot([conf, conf], [ys[t] - h / 2, ys[t] + h / 2], color=SURF, lw=1.6, zorder=3.5)
            if conf >= 8:
                ax.text(conf - 0.7, ys[t], "{:,}".format(conf), ha="right", va="center", fontsize=8,
                        color="#ffffff", fontweight="bold", zorder=4)
            else:
                ax.text(conf + 0.6, ys[t], "{:,}".format(conf), ha="left", va="center", fontsize=7.5,
                        color=INK, zorder=4)
        ax.text(deaths + 0.8, ys[t], "{:,}".format(deaths), ha="left", va="center", fontsize=8, color=INK2,
                zorder=4)
    # the gap between the recommended trust and the runner-up, on the confirmable part
    cv, rv = y3[call][2], y3[run][2]
    yc, yr = ys[call], ys[run]
    xb = 62
    ax.plot([y3[call][1] + 4.5, xb], [yc, yc], color=MUTED, lw=0.8, ls=(0, (2, 2)), zorder=1)
    ax.plot([y3[run][1] + 4.5, xb], [yr, yr], color=MUTED, lw=0.8, ls=(0, (2, 2)), zorder=1)
    ax.plot([xb, xb + 1.2, xb + 1.2, xb], [yc, yc, yr, yr], color=INK2, lw=1, zorder=4)
    ax.text(xb + 2.0, (yc + yr) / 2, "gap: {:,} deaths\n({:,} against {:,})".format(cv - rv, cv, rv),
            ha="left", va="center", fontsize=8, color=INK)
    labels = []
    for t in order:
        tag = "  (recommended)" if t == call else "  (runner-up)" if t == run else ""
        labels.append(SHORT[t] + tag)
    ax.set_yticks([ys[t] for t in order])
    ax.set_yticklabels(labels)
    for lab, t in zip(ax.get_yticklabels(), order):
        lab.set_color(INK if t in (call, run) else INK2)
        if t == call:
            lab.set_fontweight("bold")
    ax.set_xlim(0, 80)
    ax.set_xticks(range(0, 61, 10))
    ax.set_ylim(-0.6, n - 0.4)
    ax.set_xlabel("Deaths inside the review's remit, July 2025 to June 2026 (patients)", color=INK2)
    ax.grid(axis="x", color=GRID, lw=0.6, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", colors=INK2, length=0)
    ax.legend(handles=[Patch(color=CONF_COL, label="deaths the reviewers could confirm in the trust's own care"),
                       Patch(color=REST_COL, label="other deaths inside the remit")],
              loc="lower left", bbox_to_anchor=(-0.01, 1.0), ncol=1, frameon=False, fontsize=7.5,
              handlelength=1.2, handleheight=0.9)
    fig.suptitle("{}: {:,} deaths a year of review could confirm, {:,} more than {}"
                 .format(SHORT[call], cv, cv - rv, SHORT[run]),
                 x=0.02, ha="left", y=0.985, fontsize=10.5, fontweight="bold", color=INK)
    fig.text(0.02, 0.015, "Latest four complete quarters, the period the placement rests on (terms of reference, "
             "section 5). Trusts ordered by confirmable deaths.\nSource: network referral record, unit feed and daily "
             "bed returns; regional data service episodes (extract of 14 August 2026).", fontsize=6.8, color=MUTED)
    fig.subplots_adjust(left=0.25, right=0.98, top=0.80, bottom=0.20)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor=SURF, metadata={"Software": None})
    plt.close(fig)
    data = buf.getvalue()
    if path:
        Path(path).write_bytes(data)
    return data


# ---------------------------------------------------------------------------------------- workbook
def write_xlsx(fx, path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

    rec, y3 = fx["rec"], fx["y3"]
    rows = sorted(CODES, key=lambda t: SHORT[t])
    wb = Workbook()
    thin = Side(style="thin", color="BFBFBF")
    head_fill = PatternFill("solid", fgColor="23395B")
    head_font = Font(name="Arial", bold=True, color="FFFFFF", size=9)
    pick_fill = PatternFill("solid", fgColor="E8F0FA")

    def header(ws, row, cols, widths):
        for j, (hd, w) in enumerate(zip(cols, widths), 1):
            c = ws.cell(row=row, column=j, value=hd)
            c.font, c.fill = head_font, head_fill
            c.alignment = Alignment(horizontal="left" if j <= 2 else "right", vertical="center", wrap_text=True)
            ws.column_dimensions[c.column_letter].width = w
        ws.row_dimensions[row].height = 40

    def body(ws, r, vals, fmts, bold=False, fill=None, top=False):
        for j, (v, f) in enumerate(zip(vals, fmts), 1):
            c = ws.cell(row=r, column=j, value=v)
            c.font = Font(name="Arial", size=9, bold=bold)
            c.border = Border(top=Side(style="thin", color="23395B") if top else None, bottom=thin)
            if f:
                c.number_format = f
                c.alignment = Alignment(horizontal="right")
            if fill:
                c.fill = fill

    # ---- the record
    ws = wb.active
    ws.title = "Record by trust"
    ws["A1"] = "Deaths after delayed escalation to critical care: the network's record by referring trust"
    ws["A1"].font = Font(name="Arial", bold=True, size=11)
    ws["A2"] = "Decisions to admit 1 July 2023 to 30 June 2026. Each patient counted once per trust."
    ws["A2"].font = Font(name="Arial", italic=True, size=8.5, color="595959")
    cols = ["Referring trust", "Code", "Patients inside the remit", "Deaths inside the remit",
            "Deaths the reviewers could have confirmed"]
    header(ws, 4, cols, [46, 7, 15, 15, 19])
    fmts = [None, None, "#,##0", "#,##0", "#,##0"]
    for i, t in enumerate(rows):
        body(ws, 5 + i, [NAME[t], t] + list(rec[t]), fmts, bold=(t == fx["call"]),
             fill=pick_fill if t == fx["call"] else None)
    tr = 5 + len(rows)
    body(ws, tr, ["All eight trusts", ""] + list(rec["total"]), fmts, bold=True, top=True)
    ws.freeze_panes = "C5"
    ws.auto_filter.ref = "A4:E%d" % (tr - 1)
    ws.print_title_rows = "4:4"
    note = tr + 2
    for k, line in enumerate([
            "Inside the remit: an adult referred from a ward or the emergency department for a level 3 bed who waited "
            "more than four hours from the decision to admit to the assignment of a bed (terms of reference, section 2).",
            "Deaths: death within 30 days of the decision to admit, from the linked date of death on the regional "
            "data service episodes.",
            "Could have confirmed: deaths after a wait during which the referring trust's own level 3 unit either held "
            "an empty staffed bed or assigned a bed to a patient the trust referred itself (sections 3 and 4). Beds "
            "the network's bed bureau allocated to patients referred by other trusts are not the trust's own decision, "
            "planned transfers included.",
            "Waits are elapsed time: a wait across a night when the clocks went forward is an hour shorter than "
            "its clock readings. A patient with two long waits at a trust is one patient.",
            "Before 2 April 2024 the record is migrated CCRS data: decision level from the CCRS level entries, "
            "CCRS times converted from UTC, a transfer's bed from the audit's bed_confirmed_at (the CCRS bed list "
            "started the row when the patient arrived), temporary patient keys resolved through the key links, "
            "parallel-run copies counted once, unit levels as registered on the date of the wait. A death that no "
            "registration links to a temporary key is dated by the spell that ended in death."]):
        c = ws.cell(row=note + k, column=1, value=line)
        c.font = Font(name="Arial", size=8, color="595959")

    # ---- the placement year, the chart's figures
    ws2 = wb.create_sheet("Placement year")
    ws2["A1"] = "Latest four complete quarters, July 2025 to June 2026 (the placement basis)"
    ws2["A1"].font = Font(name="Arial", bold=True, size=11)
    ws2["A2"] = "Ordered as in review_placement_by_trust.png."
    ws2["A2"].font = Font(name="Arial", italic=True, size=8.5, color="595959")
    header(ws2, 4, cols, [46, 7, 15, 15, 19])
    for i, t in enumerate(fx["order"]):
        body(ws2, 5 + i, [NAME[t], t] + list(y3[t]), fmts, bold=(t == fx["call"]),
             fill=pick_fill if t == fx["call"] else None)
    tr2 = 5 + len(CODES)
    body(ws2, tr2, ["All eight trusts", ""] + list(fx["y3_total"]), fmts, bold=True, top=True)
    ws2.freeze_panes = "C5"
    c = ws2.cell(row=tr2 + 2, column=1, value="Recommended: {}, {:,} confirmable deaths. Runner-up {}, {:,}. Gap {:,} "
                 "deaths.".format(SHORT[fx["call"]], fx["cv"], SHORT[fx["run"]], fx["rv"], fx["gap"]))
    c.font = Font(name="Arial", size=9, bold=True)

    # ---- notes
    ws3 = wb.create_sheet("Notes")
    ws3.column_dimensions["A"].width = 26
    ws3.column_dimensions["B"].width = 96
    notes = [
        ("Prepared by", "Quality surveillance, Wenmarsh Regional Health Board, for the placement paper to the "
                        "Board meeting of 26 November 2026"),
        ("Extract", "Network referral record, unit feed, daily bed returns, unit register and regional data "
                    "service episodes, extract of 14 August 2026"),
        ("Record", "Decisions to admit 1 July 2023 to 30 June 2026"),
        ("Placement basis", "Latest four complete quarters, 1 July 2025 to 30 June 2026 (terms of reference, "
                            "section 5)"),
        ("Long wait", "More than four hours of elapsed time from dta_at to the assignment of a level 3 bed (the "
                      "stay's admitted_at; for a CCRS-era transfer the audit's bed_confirmed_at), or to death before "
                      "a bed was assigned"),
        ("Death", "Date of death within 30 days of the decision to admit; registrations reach the regional data "
                  "service within 14 days, so decisions to 30 June 2026 are complete. Where no date of death links "
                  "to a temporary key, the discharge date of the spell that ended in death (discharge method 4)"),
        ("Own unit", "The level 3 unit the referring trust ran on the date of the decision, per the unit "
                     "register's effective dates"),
        ("Empty staffed bed", "Census rebuilt minute by minute from admitted_at and discharged_at against the day's "
                              "staffed beds (beds_open)"),
        ("Own placement", "An admission to the referring trust's own unit of a patient the trust referred itself "
                          "(the admitted patient's referring_trust). Stennock's planned patients from theatre "
                          "recovery count, though the unit feed codes them 03. A patient referred by another trust "
                          "is a transfer whose bed the network's bed bureau allocated, whatever the admission type. "
                          "Contiguous bed rows of one patient in one unit read as one stay"),
        ("Counting", "Whole patients; a patient appears once per trust in each column"),
    ]
    for i, (k, v) in enumerate(notes, 1):
        a = ws3.cell(row=i, column=1, value=k)
        a.font = Font(name="Arial", size=9, bold=True)
        a.alignment = Alignment(vertical="top")
        b = ws3.cell(row=i, column=2, value=v)
        b.font = Font(name="Arial", size=9)
        b.alignment = Alignment(wrap_text=True, vertical="top")
    for w in (ws, ws2, ws3):
        w.sheet_view.showGridLines = False
        w.page_setup.orientation = "landscape" if w.title != "Notes" else "portrait"
        w.page_setup.fitToWidth = 1
        w.page_setup.fitToHeight = 0
        w.sheet_properties.pageSetUpPr.fitToPage = True
    stamp = dt.datetime.combine(PAPER_DATE, dt.time(9, 0))
    wb.properties.creator = "Quality surveillance, " + BOARD
    wb.properties.lastModifiedBy = "Quality surveillance, " + BOARD
    wb.properties.title = "External review placement 2027-28: workings"
    wb.properties.created = stamp
    wb.properties.modified = stamp
    wb.save(path)


# ---------------------------------------------------------------------------------------- the paper
def write_docx(fx, path, png):
    import io
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor

    call, run, cv, rv, gap = fx["call"], fx["run"], fx["cv"], fx["rv"], fx["gap"]
    y3, held, rec, by = fx["y3"], fx["held"], fx["rec"], fx["by_year"]
    tot = fx["y3_total"]
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10)
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    sec.left_margin = sec.right_margin = Cm(2.3)
    sec.top_margin, sec.bottom_margin = Cm(2.0), Cm(2.0)

    def para(text="", size=10, bold=False, italic=False, after=6, color=None, align=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(after)
        if align:
            p.alignment = align
        if text:
            r = p.add_run(text)
            r.font.size, r.bold, r.italic = Pt(size), bold, italic
            if color:
                r.font.color.rgb = RGBColor.from_string(color)
        return p

    def runs(p, parts, size=10):
        for t in parts:
            bold = isinstance(t, list)
            sup = isinstance(t, tuple)
            r = p.add_run(t[0] if (bold or sup) else t)
            r.font.size = Pt(size)
            r.bold = bold
            r.font.superscript = sup
        return p

    def heading(text):
        p = para(text, size=11, bold=True, after=4, color="23395B")
        p.paragraph_format.space_before = Pt(10)
        return p

    def shade(cell, hexfill):
        tcPr = cell._tc.get_or_add_tcPr()
        sh = OxmlElement("w:shd")
        sh.set(qn("w:val"), "clear")
        sh.set(qn("w:color"), "auto")
        sh.set(qn("w:fill"), hexfill)
        tcPr.append(sh)

    # footer with page number
    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fr = fp.add_run("Wenmarsh Regional Health Board | Board, 26 November 2026 | Page ")
    fr.font.size = Pt(7.5)
    fr.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
    r = fp.add_run()
    r.font.size = Pt(7.5)
    for tag, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if tag:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), tag)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = text
        r._r.append(el)

    para(BOARD.upper(), size=8.5, bold=True, after=0, color="23395B")
    para("Board meeting, 26 November 2026. For decision.", size=8.5, after=0, color="595959")
    para("From: Andrea Davey, Head of Quality Surveillance. 2 October 2026.", size=8.5, after=10, color="595959")
    para("External review of deaths after delayed escalation to critical care, 2027-28: place the review at {}"
         .format(SHORT[call]), size=14, bold=True, after=8)

    p = para(after=6)
    runs(p, ["The Board is asked to place the 2027-28 external review at ", [NAME[call]], "."], size=11)
    p = para(after=6)
    runs(p, ["A year of review at {} could confirm ".format(SHORT[call]), ["{:,} deaths".format(cv)],
             " as avoidable in the trust's own care. The trust that comes closest is {}, at {:,}, so {} leads by "
             .format(NAME[run], rv, SHORT[call]), ["{:,} deaths".format(gap)], "."])
    para("The engagement is judged on the deaths its reviewers confirm as avoidable because of problems in the "
         "reviewed trust's own care, and the terms of reference count a trust's decisions about the use of its own "
         "beds and staff as part of that care (WRHB/26/097, sections 3 and 4). The placement rests on the latest "
         "four complete quarters, July 2025 to June 2026 (section 5).", after=6)

    heading("Why Stennock")
    p = para(after=6)
    runs(p, ["In the placement year {:,} Stennock patients waited more than four hours for a level 3 bed and {:,} "
             "of them died within 30 days of the decision to admit.".format(y3[call][0], y3[call][1]),
             ("1",), " Stennock's unit was full at every hour of every one of those waits, which is consistent with "
             "the network's view that it is full every morning. What filled it matters. Through each of the {:,} "
             "waits the unit was assigning beds to Stennock's own planned surgical patients, referred by Stennock "
             "from theatre recovery on weekdays during the elective lists. At weekends, with no lists running, no "
             "Stennock referral waited more than four hours.".format(fx["stn_waits_alloc"])])
    para("The unit feed codes these patients as planned transfers in, but each was referred by Stennock itself and "
         "none passed through the network's bed bureau. A bed the trust gives to a planned patient of its own is the "
         "trust's decision about the use of its own beds. Under the methodology note every one of those {:,} deaths "
         "therefore falls inside Stennock's own care, and they are the deaths a review can examine and confirm."
         .format(y3[call][2]), after=6)
    para("The pattern is not a one-year effect. Across the network's record Stennock has the most confirmable "
         "deaths in each four-quarter year ({:,}, {:,} and {:,}, against Prideswick's {:,}, {:,} and {:,}), so the "
         "latest year is a fair guide to 2027-28."
         .format(by[1][call][2], by[2][call][2], by[3][call][2], by[1][run][2], by[2][run][2], by[3][run][2]),
         after=6)

    heading("Why not the others")
    para("The Chair's starting point, sending the reviewers to wherever the most patients die waiting, points to "
         "Lathingbury, which has the most deaths inside the remit ({:,} of {:,}). Lathingbury runs no level 3 beds, "
         "so each of its patients was waiting for another trust's bed, and a review there would confirm none of "
         "them as Lathingbury's own care. The programme screen Sharon Banks will present counts referrals waiting "
         "from receipt and is not the measure the engagement is judged on.".format(y3["LAT"][1], tot[1]), after=6)
    tbl_order = fx["order"]
    tb = doc.add_table(rows=1, cols=4)
    tb.style = "Table Grid"
    hdr = ["Trust", "Deaths inside the remit", "Confirmable in own care", "What held the waits"]
    reason = {
        "STN": "Own unit admitting Stennock's own planned surgical patients from theatre recovery throughout each wait",
        "PRW": "{:,} after waits beside its own empty staffed beds; {:,} after waits through which its full unit "
               "took transfers the bed bureau placed; {:,} with the unit full and no admission".format(
                   held["PRW"]["empty"], held["PRW"]["bureau"], held["PRW"]["capacity"]),
        "RIS": "{:,} after waits through which its full unit took transfers the bed bureau placed; {:,} with the "
               "unit full and no admission; {:,} beside an empty staffed bed".format(
                   held["RIS"]["bureau"], held["RIS"]["capacity"], held["RIS"]["empty"]),
        "LAT": "No level 3 beds: every wait was for another trust's bed",
        "BRK": "Empty beds at 08:00 on most mornings, but full at every hour of each long wait, all of which began "
               "in the evening",
        "ELL": "No level 3 beds since April 2024",
        "TAN": "No level 3 beds",
        "PEL": "No level 3 beds since the winter beds closed in March 2024",
    }
    for j, hd in enumerate(hdr):
        c = tb.rows[0].cells[j]
        c.text = ""
        rr = c.paragraphs[0].add_run(hd)
        rr.bold, rr.font.size = True, Pt(8.5)
        rr.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        shade(c, "23395B")
    for t in tbl_order:
        cells = tb.add_row().cells
        vals = [SHORT[t], "{:,}".format(y3[t][1]), "{:,}".format(y3[t][2]), reason[t]]
        for j, v in enumerate(vals):
            cells[j].text = ""
            rr = cells[j].paragraphs[0].add_run(v)
            rr.font.size = Pt(8.5)
            rr.bold = (t == call and j < 3)
            if j in (1, 2):
                cells[j].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if t == call:
                shade(cells[j], "E8F0FA")
    cells = tb.add_row().cells
    for j, v in enumerate(["All eight trusts", "{:,}".format(tot[1]), "{:,}".format(tot[2]), ""]):
        cells[j].text = ""
        rr = cells[j].paragraphs[0].add_run(v)
        rr.font.size, rr.bold = Pt(8.5), True
        if j in (1, 2):
            cells[j].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    widths = [Cm(2.6), Cm(2.3), Cm(2.6), Cm(8.9)]
    tb.autofit = False
    for j, w in enumerate(widths):
        tb.columns[j].width = w
    for row in tb.rows:
        for j, w in enumerate(widths):
            row.cells[j].width = w
    para("Placement year, July 2025 to June 2026. Source: network referral record, unit feed and daily bed returns; "
         "regional data service episodes.", size=7.5, italic=True, after=8, color="595959")
    para("Prideswick is the real alternative. Its unit still holds weekend admissions until the on-call consultant "
         "intensivist has seen the patient on site, and {:,} of its patients died after waiting beside its own empty "
         "staffed beds. That is a smaller yield than Stennock's, {:,} deaths fewer, and the Board can raise the "
         "weekend rule with Prideswick through the network without a twelve-month review."
         .format(rv, gap), after=6)
    para("Ristenholm's unit gave beds to other patients during the waits behind {:,} of its {:,} deaths in the "
         "placement year, many of them planned transfers, which can read as Ristenholm putting other patients first. "
         "Every one of those patients was referred by a trust without level 3 beds, and the network's bed bureau "
         "allocates the bed for each transfer between trusts, so those waits are the network's capacity rather than "
         "Ristenholm's own decisions. Brackenford's morning returns show empty beds most days, which is what the "
         "network manager has in mind, but its unit was full at every hour of each of its long waits, all of which "
         "began in the evening.".format(held["RIS"]["bureau"], y3["RIS"][1]), after=6)

    heading("The record behind the placement")
    para("Across the network's whole record, July 2023 to June 2026, {:,} patients waited inside the remit and "
         "{:,} died; the reviewers could have confirmed {:,} of those deaths, {:,} of them at Stennock. The figures "
         "by trust are in review_placement_workings.xlsx.".format(rec["total"][0], rec["total"][1],
                                                               rec["total"][2], rec[call][2]), after=6)
    doc.add_picture(io.BytesIO(png), width=Cm(16.2))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    heading("Recommendation")
    para("That the Board places the 2027-28 external review at {}, and informs the eight trusts in December 2026 "
         "as the terms of reference set out.".format(NAME[call]), after=10)

    fn = para(after=0)
    runs(fn, [("1",), " Deaths are counted from the linked date of death on the regional data service episodes, "
                      "within 30 days of the decision to admit. Death registrations reach the service within 14 days "
                      "and the extract was taken on 14 August 2026, so the placement year is complete. Each patient "
                      "is counted once."], size=7.5)
    for r_ in fn.runs:
        r_.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

    cp = doc.core_properties
    cp.author = "Andrea Davey"
    cp.last_modified_by = "Andrea Davey"
    cp.title = "External review placement 2027-28"
    cp.comments = ""
    stamp = dt.datetime.combine(PAPER_DATE, dt.time(9, 0))
    cp.created = stamp
    cp.modified = stamp
    cp.revision = 1
    doc.save(path)


def main():
    import argparse
    task = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=str(task / "target"))
    ap.add_argument("--out", default=str(task / "golden"))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    D = Data(a.target, FILES)
    fx = figures(D)
    png = chart_png(fx, out / DELIVERABLES[2])
    write_xlsx(fx, out / DELIVERABLES[1])
    write_docx(fx, out / DELIVERABLES[0], png)
    # container: producer name and stamps set to the paper's date, fixed zip entry times, file times
    import os
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import writers
    when = dt.datetime.combine(PAPER_DATE, dt.time(9, 0))
    for name in DELIVERABLES[:2]:
        writers.scrub_ooxml(out / name, "Quality surveillance, " + BOARD, when)
    for name in DELIVERABLES:
        os.utime(out / name, (when.timestamp(), when.timestamp()))
    call, run = fx["call"], fx["run"]
    print("Critical components (latest four complete quarters, July 2025 to June 2026)")
    print("  deaths inside the remit, all trusts      %d" % fx["y3_total"][1])
    print("  most deaths inside the remit             %s %d (confirmable %d)"
          % (SHORT["LAT"], fx["y3"]["LAT"][1], fx["y3"]["LAT"][2]))
    print("  %s long waits with its own planned admissions  %d of %d; deaths %d"
          % (SHORT[call], fx["stn_waits_alloc"], fx["y3"][call][0], fx["y3"][call][1]))
    print("  recommended                              %s, %d confirmable deaths" % (NAME[call], fx["cv"]))
    print("  runner-up                                %s, %d" % (NAME[run], fx["rv"]))
    print("  gap                                      %d deaths" % fx["gap"])
    print("Rungs (latest year):")
    for k in range(5):
        l1, v1, l2, v2, m = leader(fx["R"][k])
        print("  rung %d  %s %d over %s %d (%.2fx)" % (k, SHORT[l1], v1, SHORT[l2], v2, m))
    print("Record, July 2023 to June 2026 (patients, deaths, confirmable):")
    for t in sorted(CODES, key=lambda t: SHORT[t]):
        print("  %-12s %5d %5d %5d" % ((SHORT[t],) + fx["rec"][t]))
    print("  %-12s %5d %5d %5d" % (("Total",) + fx["rec"]["total"]))
    print("wrote", ", ".join(DELIVERABLES), "to", out)


if __name__ == "__main__":
    main()
