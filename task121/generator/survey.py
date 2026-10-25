"""The Customer Satisfaction Tracker: the agency samples trains by service group and time band, a fieldworker
rides part of each sampled train and hands a questionnaire to the passengers aboard in the units covered, and the
passengers who return one answer the overall question and ten attribute ratings about the journey they were on.
Each respondent's journey is one of the train's own passenger journeys; the conditions it ran under (load against
seats on its legs, lateness at the respondent's station, crew, the ticket's fare change) are read from the same
operating records the pack ships, and the overall verdict depends on them alone. The ratings carry the verdict:
each is the respondent's experience of the attribute plus the verdict's halo."""
import numpy as np
import common as K
import world as W

QUOTA = {   # sampled train segments per wave, by service group and time band (am, inter, pm, evening, weekend)
    "MAIN": [44, 52, 40, 14, 40], "VALE": [44, 52, 40, 14, 40], "COAST": [34, 44, 32, 12, 36],
    "BRANCH": [16, 22, 16, 8, 18], "LINK": [40, 48, 38, 14, 36]}
RETURN_P = 0.235


def variants(code):
    """How passengers write a station: the name, a short form, a slip, or the three-letter code."""
    name = K.STATIONS[code]
    out = [name, name, name, name.upper(), name.lower()]
    short = {"Marlvale Central": ["Marlvale", "Marlvale Cent", "M'vale Central", "Marlvale C."],
             "Ashcombe Parkway": ["Ashcombe Pkwy", "Ashcombe"], "St Cleer Road": ["St. Cleer Rd", "St Cleer"],
             "Marlvale North": ["Marlvale Nth"], "Marlvale South": ["Marlvale Sth"], "Holbeck Lane": ["Holbeck"],
             "Farnley Green": ["Farnley"], "Wexley Cross": ["Wexley X"], "Trevose Quay": ["Trevose"],
             "Pennick Bay": ["Pennick"], "Carrow Sands": ["Carrow"], "Radley Moor": ["Radley"]}.get(name, [])
    out += short
    if len(name) > 6:
        i = 3
        out.append(name[:i] + name[i + 1:])          # a dropped letter
    out.append(code)
    return out


class Survey:
    def __init__(self, w):
        self.w = w
        self.batches, self.resp = [], []
        for wave in (2025, 2026):
            self.field(wave)
        self.weights()

    def field(self, wave):
        w = self.w
        days = set(K.WINDOWS["w%d" % wave])
        rs = [r for r in w.runs if r["date"] in days and r["cancel"] is None]
        by = {}
        for r in rs:
            if r["t"]["calls"][-1][1] > 23 * 60 + 45:
                continue                    # fieldworkers do not ride trains due at their last station after 23:45
            by.setdefault((r["group"], W.time_band(r["date"], r["t"]["start"], True)), []).append(r)
        nb = 0
        for g in K.GROUP_ORDER:
            for band in range(5):
                pool = sorted(by.get((g, band), []), key=lambda r: (r["date"], r["t"]["start"], r["uid"]))
                rg = W.rng_for("sample", wave, g, band)
                take = min(QUOTA[g][band], len(pool))
                for i in sorted(rg.choice(len(pool), take, replace=False)):
                    nb += 1
                    self.segment(wave, pool[i], nb, band)

    def segment(self, wave, r, nb, band):
        rg = W.rng_for("seg", wave, r["date"].isoformat(), r["uid"])
        calls = [c[0] for c in r["t"]["calls"]]
        n = len(calls)
        a = int(rg.integers(0, max(1, n - 2)))
        b = int(rg.integers(a + 2, n)) if a + 2 < n else n - 1
        covered = 1 if len(r["units"]) == 1 else int(rg.choice([1, 2], p=[0.7, 0.3]))
        share = covered / len(r["units"])
        od = r["od"]
        pairs = [(i, j) for i in range(n - 1) for j in range(i + 1, n) if i < b and j > a and od[i, j]]
        handed = []
        for (i, j) in pairs:
            k = int(rg.binomial(od[i, j], share))
            handed += [(i, j)] * k
        cap = int(rg.integers(38, 66))
        if len(handed) > cap:
            idx = rg.choice(len(handed), cap, replace=False)
            handed = [handed[x] for x in sorted(idx)]
        bid = "B%02d-%04d" % (wave % 100, nb)
        back = [hj for hj in handed if rg.random() < RETURN_P]
        post = 0
        for k, (i, j) in enumerate(back):
            mode = "post" if rg.random() < 0.72 else "online"
            post += mode == "post"
            self.respondent(wave, r, bid, k, i, j, mode, band, rg)
        self.batches.append(dict(batch=bid, wave=wave, date=r["date"], headcode=r["headcode"], uid=r["uid"],
                                 origin=calls[0], dep=r["t"]["calls"][0][2], group=r["group"], band=band,
                                 fw_board=calls[a], fw_alight=calls[b], units_covered=covered, issued=len(handed),
                                 post=post, online=len(back) - post))

    def respondent(self, wave, r, bid, k, i, j, mode, band, rg):
        calls = r["t"]["calls"]
        crowded = any(r["load"][x] > r["seats"] for x in range(i, j))
        arr_sched = calls[j][1]
        arr_act = r["acts"][j][1]
        late = (int(round(arr_act)) - arr_sched) >= K.LATE_MIN
        unstaffed = not r["staffed"]
        peak = band in (0, 2)
        tt = rg.choice(4, p=[.55, .30, .10, .05] if peak else [.12, .20, .45, .23])
        ticket = K.TICKETS[tt]
        fare = W.fare_change(calls[i][0], calls[j][0], ticket) if wave == 2026 else 0.0
        purpose = rg.choice(["Commuting", "Business", "Leisure"], p=[.70, .15, .15] if peak else [.20, .15, .65])
        p = K.P_BASE + K.EFFECT["crowded"] * crowded + K.EFFECT["late"] * late + K.EFFECT["unstaffed"] * unstaffed \
            + K.EFFECT["fare"] * fare
        u = rg.random()
        sat = u < p
        mood = (p - u) * 2.2 + rg.normal(0, 0.35)
        if sat:
            overall = 5 if mood > 0.45 else 4
        else:
            overall = 1 if mood < -0.9 else (2 if mood < -0.35 else 3)

        def rate(own, halo=0.9, sd=0.75):
            z = own + halo * mood + rg.normal(0, sd)
            return int(np.digitize(z, [-1.4, -0.6, 0.2, 1.1]) + 1)
        R = {"q5a": rate(1.0 - 1.1 * late), "q5b": rate(0.8 - 0.5 * late), "q5c": rate(0.55),
             "q5d": rate(0.55 - 0.25 * crowded), "q5e": rate(0.70 - 0.30 * crowded),
             "q5f": rate(1.05 - 1.55 * unstaffed - 0.45 * crowded, halo=1.25),
             "q5g": rate(1.00 - 0.90 * unstaffed - 0.20 * crowded, halo=1.20),
             "q5h": rate(0.60 - 0.35 * unstaffed), "q5i": rate(0.25 - 0.06 * fare),
             "q5j": rate(0.85 - 0.30 * unstaffed - 0.15 * crowded)}
        if wave == 2026:
            R["q5k"] = rate(0.30)
        if unstaffed and rg.random() < 0.55:
            R["q5g"] = 9            # no staff seen: helpfulness not applicable
        elif rg.random() < 0.05:
            R["q5g"] = 9
        for q in list(R):
            if R[q] != 9 and rg.random() < 0.018:
                R[q] = None         # item left blank
        stb, sta = calls[i][0], calls[j][0]
        vb, va = variants(stb), variants(sta)
        self.resp.append(dict(wave=wave, batch=bid, k=k, mode=mode, date=r["date"], uid=r["uid"], group=r["group"],
                              band=band, i=i, j=j, board=stb, alight=sta, board_text=vb[int(rg.integers(len(vb)))],
                              alight_text=va[int(rg.integers(len(va)))], ticket=ticket, purpose=purpose,
                              crowded=crowded, late=late, unstaffed=unstaffed, fare=fare, p=p, sat=sat,
                              overall=overall, R=R, age=rg.choice(["16-25", "26-34", "35-44", "45-54", "55-64", "65+"],
                                                                 p=[.14, .19, .2, .19, .16, .12]),
                              freq=rg.choice(["5 or more days a week", "1-4 days a week", "1-3 times a month",
                                              "Less often"], p=[.38, .27, .19, .16] if peak else [.12, .24, .32, .32])))

    def weights(self):
        """The agency weights each wave's respondents to the passenger journeys of their service group and time
        band in the fieldwork weeks (from the operator's counts), scaled to the wave's achieved sample."""
        w = self.w
        for wave in (2025, 2026):
            days = set(K.WINDOWS["w%d" % wave])
            jour = {}
            for r in w.runs:
                if r["date"] in days and r["cancel"] is None:
                    key = (r["group"], W.time_band(r["date"], r["t"]["start"], True))
                    jour[key] = jour.get(key, 0) + int(r["od"].sum())
            rs = [x for x in self.resp if x["wave"] == wave]
            n = {}
            for x in rs:
                n[(x["group"], x["band"])] = n.get((x["group"], x["band"]), 0) + 1
            tot_j, tot_n = sum(jour.values()), len(rs)
            for x in rs:
                key = (x["group"], x["band"])
                x["weight"] = round((jour[key] / tot_j) / (n[key] / tot_n), 4)
