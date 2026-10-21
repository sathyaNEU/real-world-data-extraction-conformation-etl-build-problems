"""Tables shipped in the pack, as the surveillance, tracing, laboratory and treatment-centre systems export them."""
import datetime as dt
import numpy as np
import pandas as pd
import world as W
import records
import asks_records

UTC_OFFSET_H = 1          # Orvanthe Standard Time is UTC+1; the field laboratory's analyser clock runs on UTC
RUN_MIN = 92              # TVD PCR cartridge run, minutes


def d_fr(day):
    return W.date_of(day).strftime("%d/%m/%Y")


def d_iso(day):
    return W.date_of(day).isoformat()


def build_all(seed=W.SEED, c_off=None, l_off=None):
    import offsets
    c_off = offsets.C_OFF if c_off is None else c_off
    l_off = offsets.L_OFF if l_off is None else l_off
    cases, o = records.build(seed)
    rng = np.random.default_rng(seed + 4000)
    reg = asks_records.contacts(cases, seed, c_off)
    # ---- known contacts on the line list (listed before onset, from the registry's "became a case" rows)
    became = reg[reg["statut"] == "Devenu cas"].drop_duplicates("numero_cas_devenu")
    known = dict(zip(became["numero_cas_devenu"], became["id_contact"]))
    # ---- laboratory records (both laboratories) and each confirmed case's local result date
    labrows, res_date = lab_records(cases, np.random.default_rng(seed + 4500 + l_off))
    # ---- the line list
    ll = []
    for r in cases.itertuples():
        unit, age = "ans", int(r.age)
        if age == 0:
            unit, age = "mois", int(rng.integers(3, 12))
        lab_fed = (not r.probable) and r.zone in ("Tamberlow", "Quillmarsh") and rng.random() < 0.18
        onset_s = d_iso(r.onset) if lab_fed else d_fr(r.onset)
        cls = "Probable" if r.probable else "Confirmed"
        if r.out_day <= W.EXTRACT_DAY:
            issue, d_iss = ("Died", d_fr(r.out_day)) if r.died else ("Recovered", d_fr(r.out_day))
        else:
            issue, d_iss = ("In treatment", "") if r.centre else ("Unknown", "")
        adm = d_fr(r.adm_day) if (r.centre and 0 <= r.adm_day <= W.EXTRACT_DAY) else ""
        ctr = r.centre if adm else ""
        kc = known.get(r.numero_cas, "")
        ll.append({"numero_cas": r.numero_cas, "zone_sante": r.zone, "sexe": r.sex, "age": age, "unite_age": unit,
                   "date_debut_symptomes": onset_s, "date_notification": d_fr(r.notif), "classification": cls,
                   "id_echantillon": r.id_echantillon, "date_resultat_labo": res_date.get(r.id_echantillon, ""),
                   "centre_prise_en_charge": ctr, "date_admission": adm, "issue": issue, "date_issue": d_iss,
                   "contact_connu": "Yes" if kc else "No", "id_contact": kc,
                   "date_saisie": d_fr(min(W.EXTRACT_DAY, r.notif + int(rng.integers(0, 3)))),
                   "_true": int(r.true_id), "_onset": int(r.onset), "_kind": "case"})
    ll = pd.DataFrame(ll)
    # ---- a confirmed case notified a second time from a neighbouring zone under a new number (same sample)
    near = {"Kettlebank North": "Kettlebank South", "Kettlebank South": "Kettlebank North", "Brindlecourt": "Kettlebank North", "Tamberlow": "Quillmarsh", "Quillmarsh": "Tamberlow",
            "Threlmarren": "Wendlecombe", "Wendlecombe": "Threlmarren"}
    dups = []
    serial = {z: int((ll["zone_sante"] == z).sum()) for z in W.ZONES}
    cand = ll[(ll["classification"] == "Confirmed")]
    pick = cand.sample(frac=0.011, random_state=seed)
    for row0 in pick.to_dict("records"):
        z2 = near[row0["zone_sante"]]
        serial[z2] += 1
        nd = dt.datetime.strptime(row0["date_notification"], "%d/%m/%Y").date() + dt.timedelta(days=int(rng.integers(1, 4)))
        if (nd - W.DAY0).days > W.EXTRACT_DAY:
            continue
        row = dict(row0)
        row.update({"numero_cas": "DMW-%s-26-%04d" % (records.ZCODE[z2], serial[z2]), "zone_sante": z2,
                    "date_notification": nd.strftime("%d/%m/%Y"), "date_saisie": nd.strftime("%d/%m/%Y"),
                    "centre_prise_en_charge": "", "date_admission": "", "issue": "Unknown", "date_issue": "",
                    "contact_connu": "No", "id_contact": "", "_kind": "dup"})
        dups.append(row)
    # ---- probable cases reclassified after a negative post-mortem sample (not cases)
    nonc = []
    for k in range(int(len(ll) * 0.021)):
        z = W.ZONES[int(rng.choice(7, p=[0.3, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1]))]
        serial[z] += 1
        on = int(rng.integers(30, W.EXTRACT_DAY - 6))
        nd = on + int(rng.integers(1, 7))
        nonc.append({"numero_cas": "DMW-%s-26-%04d" % (records.ZCODE[z], serial[z]), "zone_sante": z,
                     "sexe": "F" if rng.random() < 0.5 else "M", "age": int(rng.integers(1, 80)), "unite_age": "ans",
                     "date_debut_symptomes": d_fr(on), "date_notification": d_fr(nd), "classification": "Not a case",
                     "id_echantillon": "", "date_resultat_labo": "", "centre_prise_en_charge": "", "date_admission": "",
                     "issue": "Died", "date_issue": d_fr(nd), "contact_connu": "No", "id_contact": "",
                     "date_saisie": d_fr(nd + 2), "_true": -1, "_onset": on, "_kind": "noncase"})
    # ---- alerts notified in the last days, awaiting a result
    pend = []
    for k in range(int(rng.integers(38, 55))):
        z = W.ZONES[int(rng.choice(7, p=[0.3, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1]))]
        serial[z] += 1
        nd = int(rng.integers(W.EXTRACT_DAY - 2, W.EXTRACT_DAY + 1))
        on = nd - int(rng.integers(1, 5))
        pend.append({"numero_cas": "DMW-%s-26-%04d" % (records.ZCODE[z], serial[z]), "zone_sante": z,
                     "sexe": "F" if rng.random() < 0.5 else "M", "age": int(rng.integers(1, 80)), "unite_age": "ans",
                     "date_debut_symptomes": d_fr(on), "date_notification": d_fr(nd), "classification": "Suspected",
                     "id_echantillon": "", "date_resultat_labo": "", "centre_prise_en_charge": "", "date_admission": "",
                     "issue": "In treatment", "date_issue": "", "contact_connu": "No", "id_contact": "",
                     "date_saisie": d_fr(nd), "_true": -1, "_onset": on, "_kind": "pending"})
    ll = pd.concat([ll, pd.DataFrame(dups), pd.DataFrame(nonc), pd.DataFrame(pend)], ignore_index=True)
    # a result validated after the extract is not in it: the case is still a suspected case awaiting its result
    after = [bool(v) and (dt.datetime.strptime(v, "%d/%m/%Y").date() - W.DAY0).days > W.EXTRACT_DAY
             for v in ll["date_resultat_labo"]]
    ll.loc[after, "classification"] = "Suspected"
    ll.loc[after, "date_resultat_labo"] = ""
    ll.loc[after, "id_echantillon"] = ""
    ll = ll.sort_values(["zone_sante", "numero_cas"], kind="stable").reset_index(drop=True)
    # ---- transmission links
    num_of = dict(zip(cases["true_id"], cases["numero_cas"]))
    notif_of = dict(zip(cases["true_id"], cases["notif"]))
    dup_num = {r["_true"]: r["numero_cas"] for r in dups}
    chains = []
    k = 0
    for r in cases.itertuples():
        if not r.linked or r.src not in num_of:
            continue
        created = int(r.notif + rng.choice([0, 0, 0, 1]))
        if created > W.EXTRACT_DAY:
            continue
        tgt = r.numero_cas
        if r.true_id in dup_num and rng.random() < 0.35:
            tgt = dup_num[r.true_id]
        srcn = num_of[r.src]
        if r.src in dup_num and rng.random() < 0.35:
            srcn = dup_num[r.src]
        k += 1
        et = rng.choice(["Household", "Funeral", "Health facility", "Community", "Unknown"],
                        p=[0.46, 0.17, 0.12, 0.19, 0.06])
        cert = rng.choice(["High", "Medium", "Low"], p=[0.58, 0.25, 0.17])
        chains.append({"relationship_id": "", "source_case_number": srcn, "target_case_number": tgt,
                       "exposure_type": et, "certainty_level": cert, "created_on": d_iso(created), "_created": created,
                       "_src": int(r.src), "_tgt": int(r.true_id)})
    # links entered for alerts later classed non-cases
    nc = [x for x in nonc if x["_onset"] > 60]
    for x in rng.choice(len(nc), size=min(len(nc), int(len(chains) * 0.012)), replace=False):
        row = nc[int(x)]
        s = cases[(cases["onset"] < row["_onset"] - 3) & (cases["onset"] > row["_onset"] - 30)]
        if not len(s):
            continue
        srow = s.iloc[int(rng.integers(len(s)))]
        cr = dt.datetime.strptime(row["date_notification"], "%d/%m/%Y").date()
        chains.append({"relationship_id": "", "source_case_number": srow["numero_cas"], "target_case_number": row["numero_cas"],
                       "exposure_type": "Community", "certainty_level": "Low", "created_on": cr.isoformat(),
                       "_created": (cr - W.DAY0).days, "_src": int(srow["true_id"]), "_tgt": -1})
    chains = pd.DataFrame(chains).sort_values(["_created", "target_case_number"], kind="stable").reset_index(drop=True)
    chains["relationship_id"] = ["REL-%06d" % (731 + 3 * i + int(rng.integers(0, 3))) for i in range(len(chains))]
    return {"cases": cases, "world": o, "ll": ll, "chains": chains, "reg": reg, "lab": labrows}


def lab_records(cases, rng):
    """Both laboratories' results, epi weeks 36 to 42. The field laboratory (Tamberlow and Quillmarsh samples) writes
    the analyser's clock, which runs on UTC; the public health laboratory's LIMS writes Orvanthe Standard Time."""
    rows = []
    res_date = {}
    asr = {"KPL": 0, "TFL": 0}

    def times(lab, zone, coll_day):
        if rng.random() < 0.3:
            ch = rng.uniform(0, 24)
        else:
            ch = rng.uniform(7.5, 17.5)
        coll = dt.datetime.combine(W.date_of(coll_day), dt.time()) + dt.timedelta(hours=ch)
        if lab == "TFL":
            tr = rng.uniform(0.8, 5.0) if zone == "Tamberlow" else rng.uniform(5.0, 30.0)
        else:
            tr = rng.uniform(1.5, 9.0) if zone in ("Kettlebank North", "Kettlebank South", "Brindlecourt") else rng.uniform(8.0, 40.0)
        rec = coll + dt.timedelta(hours=tr)
        # inactivation and preparation in the glovebox, then the queue for a free module; a few samples from
        # critically ill patients are prepared at once
        if rng.random() < 0.03:
            prep = rng.uniform(0.2, 0.45)
        else:
            prep = rng.uniform(1.0, 1.6) + rng.exponential(2.2 if lab == "TFL" else 3.6)
        res = rec + dt.timedelta(minutes=RUN_MIN + rng.uniform(1, 9)) + dt.timedelta(hours=prep)
        return coll, rec, res

    def add(lab, sid, who, motif, coll_day, zone, result):
        coll, rec, res = times(lab, zone, coll_day)
        rerun = rng.random() < 0.04
        if rerun:
            rows.append([lab, sid, who, motif, coll, rec, res, "Indeterminate"])
            res = res + dt.timedelta(hours=rng.uniform(1.0, 4.0)) + dt.timedelta(minutes=RUN_MIN + rng.uniform(2, 14))
        rows.append([lab, sid, who, motif, coll, rec, res, result])
        return res

    for r in cases.itertuples():
        if r.probable or not r.id_echantillon:
            continue
        lab = r.id_echantillon[:3]
        coll_day = int(max(r.onset + 1, r.notif - 1))
        if coll_day < 98 or coll_day > W.EXTRACT_DAY:
            res_date[r.id_echantillon] = d_fr(min(W.EXTRACT_DAY, coll_day + 1)) if coll_day < 98 else ""
            continue
        res = add(lab, r.id_echantillon, r.numero_cas, "Diagnostic", coll_day, r.zone, "Positive")
        res_date[r.id_echantillon] = res.strftime("%d/%m/%Y")
        for k in range(int(rng.poisson(2.4))):
            asr[lab] += 1
            d = int(np.clip(coll_day + rng.integers(-3, 4), 98, W.EXTRACT_DAY))
            add(lab, "%s-26-A%05d" % (lab, asr[lab]), "ALR-%s-%05d" % (lab, asr[lab]), "Diagnostic", d, r.zone, "Negative")
        # discharge controls for survivors treated in a centre
        if r.centre and not r.died and 98 <= r.out_day - 3 <= W.EXTRACT_DAY:
            for back in (3, 1):
                add(lab, "%s-26-C%05d" % (lab, 3 * len(rows) + back), r.numero_cas, "Discharge control", int(r.out_day - back), r.zone, "Negative")
    df = pd.DataFrame(rows, columns=["lab", "id_echantillon", "numero", "motif", "coll", "rec", "res_true", "resultat"])
    return df, res_date


if __name__ == "__main__":
    p = build_all()
    print(len(p["ll"]), p["ll"]["_kind"].value_counts().to_dict(), len(p["chains"]), len(p["reg"]), len(p["lab"]))
    print(p["lab"].groupby("lab").size())
