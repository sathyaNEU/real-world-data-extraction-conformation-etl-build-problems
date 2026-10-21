"""Contact registry and laboratory records for the asks. Built from the case records; no row here is read by
the main call (asserted in checks.py)."""
import numpy as np
import pandas as pd
import world as W
from records import ZCODE as ZC

LETTERS = "AABBCDDEFGHJKKLLMMMNNOPRRSSTTW"   # first letters of given and family names in the province, weighted


def initials(rng):
    return "%s.%s." % (LETTERS[rng.integers(len(LETTERS))], LETTERS[rng.integers(len(LETTERS))])


def contacts(cases, seed=W.SEED, offset=0):
    """One row per listing of a person as a contact of a case notified from epi week 36 on (day 98) to the
    extract. A person exposed to two cases is listed twice, once per source case. The organisation's tablet
    teams took over follow-up from the directorate's teams in weeks 37 to 39, and for the cases both teams
    visited the directorate's paper list was entered as well: the same person under a second id, the age as
    the paper form estimated it, the status the directorate's team closed the line with."""
    rng = np.random.default_rng(seed + 2000 + offset)
    rows = []
    serial = {"LMR": 10450, "PHD": 22870}
    persons = []   # (household, initials, sex, age, zone)
    hh_serial = {}
    c = cases.sort_values("notif", kind="stable")
    by_true = {int(t): r for t, r in zip(c["true_id"], c.itertuples())}
    # infectees of each case among the cases, for "became a case"
    infectees = {}
    for r in c.itertuples():
        if r.src >= 0:
            infectees.setdefault(int(r.src), []).append(r)
    pool_by_zone = {}
    for r in c.itertuples():
        if r.notif < 98 or r.notif > W.EXTRACT_DAY:
            continue
        z = r.zone
        zc = ZC[z]
        hh_serial[zc] = hh_serial.get(zc, 0) + 1
        own_hh = "%s-M%05d" % (zc, 4000 + hh_serial[zc] * 3 + int(rng.integers(0, 3)))
        rural = z in ("Tamberlow", "Quillmarsh", "Threlmarren", "Wendlecombe")
        n = int(rng.poisson(9.5 if rural else 6.5)) + 1
        team = "LMR" if (z in ("Tamberlow", "Quillmarsh") and r.notif >= 105) or (z in ("Kettlebank North", "Brindlecourt") and rng.random() < 0.5) else "PHD"
        listed = []
        # infected contacts who were listed before their onset
        for inf in infectees.get(int(r.true_id), []):
            if rng.random() < 0.72 and inf.onset > r.notif + 1:
                listed.append(("case", inf))
        pool = pool_by_zone.setdefault(z, [])
        for k in range(n):
            recent = [q for q in pool[-60:] if abs(q[5] - r.notif) <= 3]
            if recent and rng.random() < 0.06:        # a person already listed for another case in the same days
                listed.append(("again", recent[int(rng.integers(len(recent)))]))
            else:
                listed.append(("new", None))
        for kind, obj in listed:
            if kind == "case":
                hh = own_hh if rng.random() < 0.6 else "%s-M%05d" % (zc, 4000 + int(rng.integers(1, 3 * hh_serial[zc] + 3)))
                p = (hh, initials(rng), obj.sex, int(obj.age), z, int(r.notif))
            elif kind == "again":
                p = obj
            else:
                hh = own_hh if rng.random() < 0.55 else "%s-M%05d" % (zc, 4000 + int(rng.integers(1, 3 * hh_serial[zc] + 3)))
                p = (hh, initials(rng), "F" if rng.random() < 0.54 else "M", int(min(85, rng.gamma(2.2, 13))), z, int(r.notif))
                pool.append(p)
            listing = int(r.notif + rng.choice([0, 1, 1, 2, 3]))
            if listing > W.EXTRACT_DAY:
                continue
            last_exp = int(min(r.notif, r.onset + rng.integers(0, 6)))
            end = last_exp + 21
            serial[team] += 1
            cid = "%s-%s-%06d" % (team, zc, serial[team])
            if kind == "case":
                status, sday, seen = "Devenu cas", int(obj.notif), max(0, int(obj.onset - listing))
                became = obj.numero_cas
            else:
                became = ""
                if end > W.EXTRACT_DAY:
                    status, sday = "En suivi", W.EXTRACT_DAY
                    seen = int(max(0, (W.EXTRACT_DAY - listing) * rng.uniform(0.75, 1.0)))
                else:
                    u = rng.random()
                    if u < 0.80:
                        status, sday, seen = "Suivi termine", end, int(min(21, end - listing + 1) - rng.integers(0, 3))
                    elif u < 0.92:
                        sday = int(listing + rng.integers(3, 15))
                        status, seen = "Perdu de vue", int((sday - listing) * rng.uniform(0.5, 0.9))
                    elif u < 0.97:
                        sday = int(listing + rng.integers(2, 12))
                        status, seen = "Deplace hors zone", int((sday - listing) * rng.uniform(0.5, 0.9))
                    else:
                        status, sday, seen = "Refus", int(listing + rng.integers(0, 3)), 0
            rows.append([cid, team, z, r.numero_cas, p[0], p[1], p[2], p[3], listing, last_exp, end, seen, status, sday, became])
            # the directorate's paper list entered beside the tablet list during the takeover
            dup_p = 0.15 if z in ("Tamberlow", "Quillmarsh") else (0.11 if z in ("Kettlebank North", "Brindlecourt") else 0.0)
            if team == "LMR" and 105 <= r.notif <= 125 and kind != "case" and rng.random() < dup_p:
                serial["PHD"] += 1
                did = "PHD-%s-%06d" % (zc, serial["PHD"])
                age2 = p[3] + int(rng.choice([-2, -1, 1, 2, 3])) if p[3] > 3 else p[3] + 1
                dl = listing + int(rng.integers(-1, 2))
                d_s = int(dl + rng.integers(3, 9))
                rows.append([did, "PHD", z, r.numero_cas, p[0], p[1], p[2], age2, dl, last_exp, end,
                             int((d_s - dl) * rng.uniform(0.4, 0.8)), "Perdu de vue", d_s, ""])
    df = pd.DataFrame(rows, columns=["id_contact", "equipe", "zone_sante", "numero_cas_source", "code_menage",
                                     "initiales", "sexe", "age", "listing", "last_exp", "end", "jours_vus", "statut",
                                     "status_day", "numero_cas_devenu"])
    return df


def lab(cases, seed=W.SEED):
    """Diagnostic, re-run and discharge-control results of the two laboratories, epi weeks 36 to 42."""
    rng = np.random.default_rng(seed + 3000)
    rows = []
    alert_serial = {"KPL": 0, "TFL": 0}
    for r in cases.itertuples():
        if r.probable or not r.id_echantillon:
            continue
        coll = int(max(r.onset + 1, r.notif - 1))
        if coll < 98 or coll > W.EXTRACT_DAY:
            continue
        rows.append(("diag", r.id_echantillon, r.numero_cas, coll, "Positif"))
    # negative alerts: suspects tested and discarded, about 2.4 for each confirmed case, same days and labs
    pos = [x for x in rows]
    for kind, sid, num, coll, res in pos:
        pre = sid[:3]
        for k in range(int(rng.poisson(2.4))):
            alert_serial[pre] += 1
            d = int(np.clip(coll + rng.integers(-3, 4), 98, W.EXTRACT_DAY))
            rows.append(("diag", "%s-26-A%05d" % (pre, alert_serial[pre]), "ALR-%s-%05d" % (pre, alert_serial[pre]), d, "Negatif"))
    return rows


if __name__ == "__main__":
    import records
    c, o = records.build()
    df = contacts(c)
    print(len(df), df.equipe.value_counts().to_dict(), df.statut.value_counts().to_dict())
    print(len(lab(c)))
