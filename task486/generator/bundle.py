"""Everything the generator draws, in memory, from fixed random streams: the census geography and truth, the release,
the county's 2026 address points, the provider areas before the 2023 redraw, and the Office on Aging's service records.
The pack writers, the checks and the ceiling all start from here."""
import datetime as dt

import numpy as np

import asks as A
import census as C
import world as W

DEATH_FILE_FIRST_RUN, DEATH_FILE_LAST_RUN = dt.date(2025, 7, 5), dt.date(2026, 10, 5)


class Bundle:
    def __init__(self):
        rng = np.random.default_rng(W.SEED)
        self.blocks = C.add_group_quarters(C.build(rng), rng)
        self.rel = C.release(self.blocks, rng)
        r2 = np.random.default_rng(W.SEED * 7 + 1)
        self.points = [b["hu"] + (int(r2.integers(4, 22)) if b["cut"] and b["side"] == "rural" and b["hu"] > 0
                                  and r2.random() < 0.25 else 0) for b in self.blocks]
        # before the July 2023 redraw the town edges were served from the towns
        self.old_area = [("Wickmoor City" if b["tract"] < "9" else "Fallowmere Town")
                         if (b["cut"] and b["side"] == "rural") else b["area"] for b in self.blocks]
        r3 = np.random.default_rng(W.SEED * 31 + 7)
        self.clients, self.episodes, self.links, kel = A.simulate(self.blocks, self.old_area, r3)
        A.place_october_deaths(self.clients, self.episodes, kel, np.random.default_rng(W.SEED * 37 + 11))
        self.all_kelvane_deaths = kel
        self.kelvane_deaths = [d for d in kel if DEATH_FILE_FIRST_RUN <= d["match_run"] <= DEATH_FILE_LAST_RUN]
        self.taken = {c["state_id"] for c in self.clients} | {l["prior_id"] for l in self.links}
        self.deaths = self.kelvane_deaths + A.statewide_noise(r3, self.taken)
        self.deliveries = A.deliveries(self.clients, self.episodes, r3)
