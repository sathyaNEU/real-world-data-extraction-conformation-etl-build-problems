"""Generator-side analysis over the shipped tables (as read back from target/): conformance of the
returns, the forward roll, every rung of the ladder, the two asks and their stops.

Rungs: R0 latest lodgement whole; R1 versions applied; R2 conformed 30 June picture; R3 rolled with
deeds and agreed sales; R4 takeovers on agreed dates; R4p takeovers from commitment; R5 takeovers on
the 120-day clock; R6 R5 plus the dwellings of holders inscribed after 30 June 2026 with no return yet. The independent verifier (verify.py) recomputes all of this on its own code path.
"""
import csv
import datetime as dt
import re
from decimal import Decimal

D = dt.date
P = dt.date.fromisoformat


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


class Cadastre:
    def __init__(self, rows):
        self.sec, self.parcel, self.by_unit = {}, {}, {}
        self.res = set()
        self.N = {}
        for r in rows:
            ref = r["referencia_cadastral"]
            self.sec[ref] = r["seccio_censal"]
            self.parcel[ref] = r["parcela"]
            self.by_unit[(r["parcela"], int(r["carrec"]))] = ref
            if r["us"] == "Residencial":
                self.res.add(ref)
                self.N[r["seccio_censal"]] = self.N.get(r["seccio_censal"], 0) + 1
        self.parcel_sec = {p: self.sec[ref] for ref, p in self.parcel.items()}
        self.by18 = {}
        for ref in self.sec:
            self.by18.setdefault(ref[:18], []).append(ref)

    def repair(self, raw):
        x = re.sub(r"[\s\-]", "", raw).upper()
        if x in self.sec:
            return x
        hits = self.by18.get(x[:18], [])
        return hits[0] if len(hits) == 1 else None


def expand_units(text):
    out = []
    for part in text.split(","):
        if "-" in part:
            a, b = part.split("-")
            out += list(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out


def picture(returns, quarter, cutoff, cad, mode):
    """Large-holder rows for a quarter. mode 'R0', 'R1' or 'R2'. Returns a list of
    (holder_nif, ref_or_key, section, scheduled) where scheduled = (date, buyer, price) or None."""
    lod = {}
    for r in returns:
        if r["data_presentacio"] > cutoff:
            continue
        lod.setdefault((r["nif_declarant"], r["trimestre"]), {}).setdefault(r["id_declaracio"], []).append(r)
    qorder = sorted({q for _, q in lod})
    holders = sorted({h for h, _ in lod})
    out = []
    for h in holders:
        if mode == "R0":
            if (h, quarter) not in lod:
                continue
            versions = lod[(h, quarter)]
            latest = max(versions, key=lambda i: (versions[i][0]["data_presentacio"], i))
            rows = versions[latest]
        else:
            qs = [q for q in qorder if q <= quarter and (h, q) in lod]
            if not qs:
                continue
            versions = lod[(h, qs[-1])]
            rows = []
            for vid in sorted(versions, key=lambda i: (versions[i][0]["data_presentacio"], i)):
                v = versions[vid]
                t = v[0]["tipus_declaracio"]
                if t in ("O", "S"):
                    rows = list(v)
                else:
                    rows = rows + list(v)
        for r in rows:
            code = r["codi_tinenca"]
            sch = (r["data_transmissio_prevista"], r["nif_adquirent_previst"], r["preu_convingut"]) \
                if r["data_transmissio_prevista"] else None
            raw = r["referencia_cadastral"]
            if mode in ("R0", "R1"):
                if r["unitats"]:
                    if mode == "R0" or raw not in cad.parcel_sec:
                        continue
                    out.append((h, raw + "#" + r["id_declaracio"], cad.parcel_sec[raw], sch, code))
                    continue
                if raw not in cad.sec:
                    continue
                out.append((h, raw, cad.sec[raw], sch, code))
                continue
            if code != "PD":
                continue
            if r["unitats"]:
                parcel = re.sub(r"\s", "", raw).upper()
                for u in expand_units(r["unitats"]):
                    ref = cad.by_unit[(parcel, u)]
                    out.append((h, ref, cad.sec[ref], sch, code))
            else:
                ref = cad.repair(raw)
                assert ref is not None, raw
                out.append((h, ref, cad.sec[ref], sch, code))
    return out


def counts(rows, sections):
    c = {s: 0 for s in sections}
    for _, _, sec, _, _ in rows:
        if sec in c:
            c[sec] += 1
    return c


def holdings(rows):
    """dwelling -> holder NIF (R2 rows only), with scheduled info per dwelling."""
    own, sch = {}, {}
    for h, ref, sec, s, code in rows:
        assert ref not in own, ("dwelling on two pictures", ref)
        own[ref] = h
        if s:
            sch[ref] = s
    return own, sch


def roll(own, sch, deeds, lh, start, end_deeds, reg_cut, target, takeover=None, mode="R3"):
    """Holder of each dwelling on `target`. deeds executed in (start, end_deeds] and registered by
    reg_cut apply first; then scheduled sales with agreed dates in (end_deeds, target]; `takeover`
    maps ref -> (commit_date, completion_date) for the agency's commitments."""
    cur = dict(own)
    for d in sorted(deeds, key=lambda d: (d["data_atorgament"], d["num_entrada"])):
        if not (start < d["data_atorgament"] <= end_deeds and d["data_inscripcio"] <= reg_cut):
            continue
        ref = d["referencia_cadastral"]
        cur[ref] = d["nif_adquirent"] if d["nif_adquirent"] in lh else None
    for ref, (date, buyer, price) in sorted(sch.items()):
        if cur.get(ref) is None or date <= end_deeds:
            continue
        tk = (takeover or {}).get(ref)
        if tk and mode != "R3":
            when = {"R4": date, "R4p": tk[0], "R5": tk[1]}[mode]
            if when <= target:
                cur[ref] = None
            continue
        if date <= target:
            cur[ref] = buyer if buyer in lh else None
    return {r: h for r, h in cur.items() if h}


def registrant_holdings(tit, returns, deeds, cut):
    """Holders inscribed in the register (no baixa) that have lodged no return: each dwelling whose last
    deed executed and registered by `cut` names one of them as buyer."""
    declared = {r["nif_declarant"] for r in returns}
    reg = {r["nif"] for r in tit if not r["data_baixa"]} - declared
    last = {}
    for d in sorted(deeds, key=lambda d: (d["data_atorgament"], d["num_entrada"])):
        if d["data_atorgament"] <= cut and d["data_inscripcio"] <= cut:
            last[d["referencia_cadastral"]] = d["nif_adquirent"]
    return {ref: h for ref, h in last.items() if h in reg}


def with_registrants(own, extra):
    assert not set(own) & set(extra), "a registrant's dwelling already on a return"
    out = dict(own)
    out.update(extra)
    return out


def section_counts(own, cad, sections):
    c = {s: 0 for s in sections}
    for ref in own:
        s = cad.sec.get(ref)
        if s in c:
            c[s] += 1
    return c


def share(n, N):
    return Decimal(n) * 100 / Decimal(N)


def designated(c, cad, sections):
    return sorted(s for s in sections if share(c[s], cad.N[s]) >= 25)


TK_RE = re.compile(r"RC (\w{20})\.? .*?prevista (\d\d)/(\d\d)/(\d{4})")


def ledger_takeovers(ledger, interval):
    """ref -> (commitment date, completion date) from the first-offer commitments (phase D)."""
    out = {}
    for r in ledger:
        if r["programa"] != "PPO" or r["fase"] != "D":
            continue
        m = TK_RE.search(r["concepte"])
        if not m:
            continue
        c = P(r["data_comptable"])
        out[m.group(1)] = (c.isoformat(), (c + dt.timedelta(days=interval)).isoformat())
    return out


# ---- ask B: the largest large-holder group per section ------------------------------------------
def links_at(links, day):
    out = {}
    for r in links:
        if r["data_efecte_inici"] <= day and (not r["data_efecte_fi"] or day <= r["data_efecte_fi"]):
            out[r["nif"]] = r["codi_grup"]
    return out


def stored_codes(returns, quarter, cutoff):
    """Group code and lodgement date on the return each holder's picture for `quarter` stands on."""
    best = {}
    for r in returns:
        if r["trimestre"] > quarter or r["data_presentacio"] > cutoff:
            continue
        k = (r["trimestre"], r["data_presentacio"], r["id_declaracio"])
        if r["nif_declarant"] not in best or k > best[r["nif_declarant"]][0]:
            best[r["nif_declarant"]] = (k, r["codi_grup"], r["data_presentacio"])
    return {h: (v[1], v[2]) for h, v in best.items()}


def largest(own, cad, sections, member, codes, names):
    """member: nif -> group code or ''; codes: code -> (name, alta). Returns sec -> (name, n, runner_n)."""
    out = {}
    for s in sections:
        c = {}
        for ref, h in own.items():
            if cad.sec.get(ref) != s:
                continue
            g = member.get(h) or ""
            key = ("G", g) if g else ("H", h)
            c[key] = c.get(key, 0) + 1
        ranked = sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))
        (k, n), runner = ranked[0], (ranked[1][1] if len(ranked) > 1 else 0)
        name = codes[k[1]][0] if k[0] == "G" else names[k[1]]
        out[s] = (name, n, runner)
    return out


def ask_b_members(links, stored, codes, mode):
    """Membership maps for the golden and each stop."""
    if mode == "golden":
        return links_at(links, "2027-01-01")
    if mode == "stored":
        return {h: c for h, (c, d) in stored.items()}
    if mode == "stored_valid":      # hazard handled (code issued after the lodgement ignored), switches not
        return {h: (c if c and codes[c][1] <= d else "") for h, (c, d) in stored.items()}
    if mode == "links_else_stored":  # switches handled, reissued codes not
        cur = links_at(links, "2027-01-01")
        return {h: cur.get(h) or c for h, (c, d) in stored.items()} | cur
    if mode == "reissued_stored":    # switches handled, reissued codes read through the code table
        cur = links_at(links, "2027-01-01")
        for h, (c, d) in stored.items():
            if c and codes[c][1] > d:
                cur[h] = c
        return cur
    if mode == "latest_links":
        return links_at(links, "2027-12-31")
    raise ValueError(mode)


# ---- ask C: large-holder dwellings with nobody on the municipal register -------------------------
def _lapsed(r, day):
    if r["tipus_document"] not in ("TIE-T", "PAS"):
        return False
    ref = r["data_ultima_renovacio"] or r["data_alta"]
    y, m, d = (int(x) for x in ref.split("-"))
    try:
        dl = D(y + 2, m, d)
    except ValueError:
        dl = D(y + 2, m, 28)
    return dl.isoformat() < day


def occupied(jun, sep, mode):
    """Set of refs with somebody registered, under a reading of the two deliveries."""
    sep_dist = {(r["codi_municipi"], r["districte"]) for r in sep}
    occ = set()
    for which, rows, day in (("06", jun, "2026-06-01"), ("09", sep, "2026-09-01")):
        for r in rows:
            k = (r["codi_municipi"], r["districte"])
            if mode in ("golden", "lapsed_counted", "noneu_empty", "castello_rows"):
                if which == "06" and k in sep_dist:
                    continue
                if which == "09" and k not in sep_dist:
                    continue
            elif mode in ("sept_only", "sept_only_right"):
                if which == "06":
                    continue
            if r["persones"] != "":
                if mode in ("sept_only", "castello_rows") or int(r["persones"]) > 0:
                    occ.add(r["referencia_cadastral"])
                continue
            if mode in ("golden", "sept_only_right", "castello_rows") and _lapsed(r, day):
                continue
            if mode == "noneu_empty" and r["tipus_document"] not in ("DNI", "NIE"):
                continue
            occ.add(r["referencia_cadastral"])
    if mode == "noneu_empty":
        bad = {r["referencia_cadastral"] for rows in (jun, sep) for r in rows
               if r["tipus_document"] not in ("DNI", "NIE", "")}
        occ -= bad
    return occ


def vacancy(own, cad, sections, occ):
    c = {s: 0 for s in sections}
    for ref in own:
        s = cad.sec.get(ref)
        if s in c and ref not in occ:
            c[s] += 1
    return c
