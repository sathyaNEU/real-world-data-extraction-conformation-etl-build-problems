"""The network for each season: every route direction as a Leg, with the gauge each date flies."""
import datetime as dt

import world as W
from sim import Leg


def target_seats(season, station):
    def f(d):
        if season in ("S24", "S25"):
            return W.SEATS["319"]
        sw = W.TARGET_SWITCH.get(station)
        if sw is not None and d < sw:
            return W.SEATS["319"]
        return W.SEATS["32Q"]
    return f


def build_season(season, purpose="pack", targets_only=False):
    legs = []
    for st, freq, df, amp, ns in W.TARGETS:
        for outbound in (True, False):
            o, d = ("LIN", st) if outbound else (st, "LIN")
            legs.append(Leg(season, o, d, freq, target_seats(season, st), df, amp, ns, "target", outbound,
                            growth=W.GROWTH[season], mu_seats=W.SEATS["319"], purpose=purpose))
    if targets_only:
        return legs
    for base, st, freq, t_old, t_new, df, amp, ns in W.PAST:
        typ = t_old if season == "S24" else t_new
        for outbound in (True, False):
            o, d = (base, st) if outbound else (st, base)
            legs.append(Leg(season, o, d, freq, (lambda s: (lambda _d: s))(W.SEATS[typ]), df, amp, ns, "past",
                            outbound, growth=W.GROWTH[season], mu_seats=W.SEATS[t_old], purpose=purpose))
    for base, st, freq, typ, df, amp, ns in W.REF:
        for outbound in (True, False):
            o, d = (base, st) if outbound else (st, base)
            legs.append(Leg(season, o, d, freq, (lambda s: (lambda _d: s))(W.SEATS[typ]), df, amp, ns, "ref",
                            outbound, growth=W.GROWTH[season], mu_seats=W.SEATS[typ], purpose=purpose))
    return legs
