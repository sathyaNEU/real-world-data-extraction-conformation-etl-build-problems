"""Records beside the decision that it does not use: the customer contact log and the spring 2026 delay
attribution. Both are the operator's real exports and both are about the same months."""
import datetime as dt
import common as K
import world as W

CATS = ["Crowding", "Delays and cancellations", "Staff", "Fares and tickets", "Cleanliness", "Facilities", "Other"]


def contacts():
    """Customer contacts by day, channel and category, March 2025 to September 2026. Each contact is one
    passenger getting in touch; categories are the contact centre's first-level codes."""
    head = ["contact_ref", "received", "channel", "category", "service_group"]
    rows = []
    d = dt.date(2025, 3, 1)
    n = 0
    while d <= dt.date(2026, 9, 30):
        rg = W.rng_for("contacts", d.isoformat())
        after_host = d >= dt.date(2026, 2, 8)
        after_tt = d >= K.TIMETABLE_CHANGE
        base = [2.1, 3.4, 1.6, 2.2, 0.9, 1.1, 1.3]
        if after_host:
            base[2] *= 2.4
        if after_tt:
            base[1] *= 1.35
            base[0] *= 1.5
        if d.month == 1 and d.year == 2026:
            base[3] *= 1.8
        for ci, lam in enumerate(base):
            for _ in range(int(rg.poisson(lam * (0.7 if d.weekday() >= 5 else 1.0)))):
                n += 1
                ch = rg.choice(["Phone", "Web form", "Email", "Social media"], p=[.31, .38, .13, .18])
                g = rg.choice(K.GROUP_ORDER, p=[.27, .24, .21, .07, .21])
                rows.append(["CC%07d" % (2500000 + n * 3 + int(rg.integers(0, 3))), d.isoformat(), ch, CATS[ci],
                             K.GROUPS[g]["name"]])
        d += dt.timedelta(days=1)
    return head, rows


def delays(w):
    """Delay minutes the spring 2026 wave's trains lost, by service group and the cause the train delay
    attribution process assigned."""
    head = ["period", "service_group", "cause", "incidents", "delay_minutes"]
    rows = []
    causes = ["Fleet", "Infrastructure", "Train crew", "Station operations", "External", "Weather"]
    days = set(K.WINDOWS["w2026"])
    for g in K.GROUP_ORDER:
        mins = sum(max(0.0, r["acts"][-1][1] - r["t"]["calls"][-1][1]) for r in w.runs
                   if r["date"] in days and r["group"] == g and r["cancel"] is None and r["acts"][-1][1] is not None)
        rg = W.rng_for("delays", g)
        share = rg.dirichlet([5, 6, 3, 2, 2, 1])
        for c, s in zip(causes, share):
            m = int(round(mins * s))
            rows.append(["Spring 2026 wave (2 March to 12 April 2026)", K.GROUPS[g]["name"], c,
                         int(max(1, round(m / rg.uniform(6, 11)))), m])
    return head, rows
