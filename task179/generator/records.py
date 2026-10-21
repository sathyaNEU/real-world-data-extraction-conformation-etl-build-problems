"""Case, link and duplicate records built from the clean world. Every row is derived from the simulated
outbreak; the mess applied here is the surveillance system's own (duplicates across zones, date entry formats,
a few reclassified rows, pending suspects)."""
import numpy as np
import pandas as pd
import world as W

ZCODE = {"Tamberlow": "TAM", "Quillmarsh": "QUI", "Threlmarren": "THM", "Wendlecombe": "WEN", "Brindlecourt": "BRI",
         "Kettlebank North": "KBN", "Kettlebank South": "KBS"}
# treatment centre that admits a district's confirmed cases: the organisation's two centres and the directorate's two
CENTRE = {"Tamberlow": [("Tamberlow TC", 0.92), ("Kettlebank General IU", 0.08)],
          "Quillmarsh": [("Tamberlow TC", 0.88), ("Kettlebank General IU", 0.12)],
          "Threlmarren": [("Threlmarren TC", 0.85), ("Kettlebank North TC", 0.15)],
          "Wendlecombe": [("Threlmarren TC", 0.90), ("Kettlebank North TC", 0.10)],
          "Brindlecourt": [("Kettlebank North TC", 0.60), ("Kettlebank General IU", 0.40)],
          "Kettlebank North": [("Kettlebank North TC", 0.62), ("Kettlebank General IU", 0.38)],
          "Kettlebank South": [("Kettlebank North TC", 0.45), ("Kettlebank General IU", 0.55)]}


def build(seed=W.SEED):
    o = W.simulate(seed)
    on, src, zone = o["onset"], o["src"], o["zone"]
    n = len(on)
    link_rng = np.random.default_rng(seed + 500)
    linked_draw = link_rng.random(n) < W.P_LINKED          # same stream as the screens
    rng = np.random.default_rng(seed + 1000)
    probable = rng.random(n) < 0.13
    # notification delay: confirmed 0..4 days, most 1 to 3; probable 1..4 (community deaths reported by the burial teams)
    dconf = rng.choice(np.arange(5), size=n, p=[0.10, 0.27, 0.31, 0.21, 0.11])
    dprob = rng.choice(np.arange(1, 5), size=n, p=[0.18, 0.34, 0.30, 0.18])
    notif = on + np.where(probable, dprob, dconf)
    in_list = notif <= W.EXTRACT_DAY
    sex = np.where(rng.random(n) < 0.53, "F", "M")
    age = np.clip(np.where(rng.random(n) < 0.24, rng.integers(0, 15, n),
                           np.round(rng.gamma(6.5, 5.2, n)).astype(int) + 12), 0, 89)
    # outcome
    died = np.where(probable, True, rng.random(n) < 0.49)
    out_day = np.where(died, on + rng.integers(6, 15, n), on + rng.integers(18, 31, n))
    centre = np.array([""] * n, dtype=object)
    adm_day = np.full(n, -1)
    for i in range(n):
        if probable[i] or rng.random() > 0.84:
            continue
        opts = CENTRE[W.ZONES[zone[i]]]
        u = rng.random()
        acc = 0.0
        for name, p in opts:
            acc += p
            if u <= acc:
                centre[i] = name
                break
        adm_day[i] = max(notif[i] - rng.integers(0, 2), on[i] + 1)
    cases = pd.DataFrame({"true_id": np.arange(n), "onset": on, "notif": notif, "zone": [W.ZONES[z] for z in zone],
                          "probable": probable, "sex": sex, "age": age, "died": died, "out_day": out_day,
                          "centre": centre, "adm_day": adm_day, "src": src, "linked": linked_draw & (src >= 0)})
    cases = cases[in_list].copy()
    # case numbers by zone in notification order
    cases = cases.sort_values(["notif", "onset", "true_id"], kind="stable")
    serial = {}
    nums = []
    for z in cases["zone"]:
        serial[z] = serial.get(z, 0) + 1
        nums.append("DMW-%s-26-%04d" % (ZCODE[z], serial[z]))
    cases["numero_cas"] = nums
    # laboratory sample numbers for confirmed cases: the field laboratory at Tamberlow tests Tamberlow's and
    # Quillmarsh's samples, the public health laboratory at Kettlebank the rest
    lab_serial = {"KPL": 3100, "TFL": 600}
    sample = []
    for z, p in zip(cases["zone"], cases["probable"]):
        if p:
            sample.append("")
            continue
        pre = "TFL" if z in ("Tamberlow", "Quillmarsh") else "KPL"
        lab_serial[pre] += int(rng.integers(1, 4))   # alerts that tested negative take the numbers between
        sample.append("%s-26-%05d" % (pre, lab_serial[pre]))
    cases["id_echantillon"] = sample
    return cases, o


if __name__ == "__main__":
    c, o = build()
    print(len(c), c["probable"].mean(), (c["onset"] <= W.COMPLETE_LAST).sum(), c["linked"].sum())
    print(c.head())
