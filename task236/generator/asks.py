"""What the gateway's person matching and the laboratories' two reporting systems do to the rows the asks read and the
call does not: rows of people whose every result was collected outside their region's change windows (weeks 14 to 25,
the weeks after each window and week 36) and reached the gateway by the week 36 cut-off.

A laboratory sends a preliminary positive from its rapid result interface with the details on the request, and the
final report from its information system once the specimen is registered against its own patient record. Where the
two sets of details differ, the gateway's person matching can key the final to a second person, and the preliminary
can go out with no residential address and with the requesting service the patient attended, which may sit in the next
region. An infant registered under its mother's details is keyed to the mother. A person's age at collection goes up
by one on a birthday between two specimens. None of it moves a person, a case or a region in the clean truth
(`Records.positives`), and none of it touches a row in any region's change window."""
import datetime as dt
import hashlib

import numpy as np

import params as P

CUT = "2027-09-12T23:00:00Z"            # 09:00 on Monday 13 September 2027 at UTC+10
W36 = "2027-09-06"                      # Monday of report week 36
ZERO = ("NGD", "STH")                   # services that write 0000 where the request has no address
KINDS = ("two_keys", "infant", "birthday", "address")


def windows():
    out = {}
    for code, (d, kind, text) in P.CHANGES.items():
        cw = d.isocalendar()[1]
        out[code] = set(range(cw - P.WINDOW, cw + P.WINDOW))
    return out


def positive(result):
    t = result.str.lower()
    return ~(t.str.contains("not detected") | t.str.startswith("negative") | t.str.contains("no influenza"))


def week(iso):
    return dt.date.fromisoformat(iso).isocalendar()[1]


def eligible(res, R):
    """people whose every row sits outside their region's window, in one of the eight regions, with a recorded
    in-state residential postcode that the boundary review did not move, every result received by the cut-off"""
    win = windows()
    pc = res.residential_postcode
    reg = pc.map(R.region_of)
    wk = np.array([week(d) for d in res.collection_date])
    free = np.array([r in win and w not in win[r] for r, w in zip(reg, wk)])
    df = res.assign(_reg=reg, _week=wk, _free=free, _pos=positive(res.result).values,
                    _moved=pc.isin(list(R.moved)).values, _late=(res.received_utc > CUT).values)
    g = df.groupby("patient_key")
    ok = (g._free.all() & ~g._moved.any() & ~g._late.any() & g._pos.any() & (g._reg.nunique() == 1)
          & g._reg.first().isin(list(win)))
    return df[df.patient_key.isin(ok[ok].index)]


def profile(df):
    """one line per eligible person: region, first positive day, specimens, the positive specimen with a positive
    preliminary and a positive final (the first by accession), the setting of the first row, positive days"""
    pos = df[df._pos]
    sp = pos.groupby(["patient_key", "specimen_id"]).result_status.agg(lambda s: ("P" in set(s)) and ("F" in set(s)))
    pf = sp[sp].reset_index().groupby("patient_key").specimen_id.first()
    g = df.groupby("patient_key", sort=True)
    gp = pos.groupby("patient_key")
    reg, n_spec = g._reg.first(), g.specimen_id.nunique()
    first, n_pos = gp.collection_date.min(), gp.specimen_id.nunique()
    days = gp.collection_date.agg(lambda s: sorted(set(s)))
    first_row = df.sort_values(["patient_key", "received_utc", "result_id"]).groupby("patient_key").first()
    return {k: dict(region=reg[k], first=first[k], n_spec=int(n_spec[k]), n_pos=int(n_pos[k]), pf=pf.get(k),
                    setting=first_row.requester_setting[k], age=int(first_row.age_years[k]), days=days[k])
            for k in reg.index}


def apply(res, R, plan):
    """rewrite the rows of the people the plan picks; returns the rows and a manifest of every instance"""
    rng = np.random.default_rng(P.RECORD_SEED * 100 + 9)
    df = eligible(res, R)
    prof = profile(df)
    rows_of = df.groupby("patient_key").groups
    used = set()
    man = {k: [] for k in KINDS}
    out = res.copy()
    col = {c: out.columns.get_loc(c) for c in out.columns}

    def put(idx, field, value):
        out.iloc[out.index.get_indexer(list(idx)), col[field]] = value

    def pick(cands, n):
        cands = sorted(c for c in cands if c not in used)
        if n <= 0 or not cands:
            return []
        idx = rng.choice(len(cands), size=min(n, len(cands)), replace=False)
        return [cands[i] for i in sorted(idx)]

    def in36(k):
        return prof[k]["first"] >= W36

    for code in sorted(plan):
        pl = plan[code]
        mine = sorted(k for k, v in prof.items() if v["region"] == code)
        # ---------------------------------------------------------------- a birthday between two specimens
        for zone, n in zip(("w36", "other"), pl["birthday"]):
            cands = []
            for k in mine:
                v = prof[k]
                if v["n_pos"] < 2 or v["age"] < 2 or len(v["days"]) < 2:
                    continue
                d0, d1 = dt.date.fromisoformat(v["days"][0]), dt.date.fromisoformat(v["days"][1])
                if (dt.date.fromisoformat(v["days"][-1]) - d0).days >= 14 or (v["days"][1] >= W36) != (zone == "w36"):
                    continue
                cands.append(k)
            for k in pick(cands, n):
                v = prof[k]
                bday = v["days"][1]
                g = df.loc[rows_of[k]]
                put(g[g.collection_date >= bday].index, "age_years", v["age"] + 1)
                used.add(k)
                man["birthday"].append(dict(region=code, key=k, birthday=bday, week=week(bday)))
        # ---------------------------------------------------------------- one specimen, two gateway keys
        for zone, n in zip(("w36", "other"), pl["two_keys"]):
            cands = [k for k in mine if prof[k]["pf"] and in36(k) == (zone == "w36")]
            for k in pick(cands, n):
                g = df.loc[rows_of[k]]
                s = prof[k]["pf"]
                fin = g[(g.specimen_id == s) & (g.result_status == "F")]
                t_fin, svc = fin.received_utc.min(), fin.service_code.iloc[0]
                rows = g[(g.service_code == svc) & (g.received_utc >= t_fin)].index
                k2 = hashlib.sha256(("%d-%s-%s-lis" % (R.seed, code, k)).encode()).hexdigest()[:16]
                put(rows, "patient_key", k2)
                used.add(k)
                man["two_keys"].append(dict(region=code, key=k, key2=k2, specimen=s, rows=len(rows),
                                            week=week(prof[k]["first"])))
        # ---------------------------------------------------------------- an infant under its mother's key
        for zone, n in zip(("w36", "other"), pl["infant"]):
            single = [k for k in mine if prof[k]["n_spec"] == 1 and prof[k]["n_pos"] == 1]
            babies = [k for k in single if in36(k) == (zone == "w36")
                      and prof[k]["setting"] in ("emergency department", "general practice")]
            for k in pick(babies, n):
                d0 = dt.date.fromisoformat(prof[k]["first"])
                mums = [m for m in single if m != k
                        and abs((dt.date.fromisoformat(prof[m]["first"]) - d0).days) <= 6]
                got = pick(mums, 1)
                if not got:
                    continue
                m = got[0]
                g, gm = df.loc[rows_of[k]], df.loc[rows_of[m]]
                put(g.index, "patient_key", m)
                put(g.index, "age_years", 0)
                put(g.index, "residential_postcode", gm.residential_postcode.iloc[0])
                put(gm.index, "sex", "F")
                if not 19 <= prof[m]["age"] <= 44:
                    put(gm.index, "age_years", int(rng.integers(22, 41)))
                used.update((k, m))
                man["infant"].append(dict(region=code, infant=k, mother=m,
                                          week=min(week(prof[x]["first"]) for x in (k, m))))
        # ---------------------------------------------------------------- the preliminary with no address
        for to, n in pl["address"]:
            cands = [k for k in mine if prof[k]["n_spec"] == 1 and prof[k]["pf"] and in36(k)]
            pcs = R.postcodes[to]
            w = np.array([e for _, e in pcs], dtype=float)
            for k in pick(cands, n):
                g = df.loc[rows_of[k]]
                s = prof[k]["pf"]
                pre = g[(g.specimen_id == s) & (g.result_status == "P")]
                svc = pre.service_code.iloc[0]
                put(pre.index, "residential_postcode", "0000" if svc in ZERO else "")
                req = pcs[int(rng.choice(len(pcs), p=w / w.sum()))][0]
                put(g[g.specimen_id == s].index, "requester_postcode", req)
                used.add(k)
                man["address"].append(dict(region=code, to=to, key=k, specimen=s, requester=req))
    return out, man
