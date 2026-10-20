"""The routes from the records to each district's 2026 leak methane: a surveyed leak's start taken at the find (the
record), at the previous survey (the regulatory convention), halfway between (the textbook convention), or as its
expected start under the monthly profile of leak starts the odor reports measure (the golden). Reads plain values,
so the generator and the verifier share it."""
import calendar
import datetime as dt

HOURS = 24.0


def profile(odor_dates):
    """Monthly shares of leak starts from the odor-reported leaks' report dates."""
    c = [0] * 12
    for d in odor_dates:
        c[d.month - 1] += 1
    tot = float(sum(c))
    return [x / tot for x in c]


def expected_start(prev, found, prof):
    """The expectation of a start between the previous survey (exclusive) and the find, each day weighted by its
    month's share over the month's days; returned as a datetime (noon of the fractional day)."""
    d0 = prev.date() if isinstance(prev, dt.datetime) else prev
    d1 = found.date() if isinstance(found, dt.datetime) else found
    num = den = 0.0
    t = d0 + dt.timedelta(days=1)
    i = 1
    while t <= d1:
        w = prof[t.month - 1] / calendar.monthrange(t.year, t.month)[1]
        num += w * i
        den += w
        t += dt.timedelta(days=1)
        i += 1
    off = num / den - 0.5          # a start is spread over its day
    return dt.datetime.combine(d0, dt.time(0)) + dt.timedelta(days=off)


def start_of(route, leak, prof):
    """leak: dict with how, found (datetime), prev (date of the segment's previous survey), report (odor datetime)."""
    if leak["how"] == "ODOR":
        return leak["found"]
    if route == "record":
        return leak["found"]
    if route == "full":
        return dt.datetime.combine(leak["prev"], dt.time(0)) + dt.timedelta(days=1)
    if route == "mid":
        p = dt.datetime.combine(leak["prev"], dt.time(0)) + dt.timedelta(days=1)
        return p + (leak["found"] - p) / 2
    if route == "golden":
        return expected_start(leak["prev"], leak["found"], prof)
    raise ValueError(route)


def methane(leaks, route, prof, rate, end):
    """{district: tonnes} for leaks found in the year: each leak's rate times the hours from its start to its repair
    or the end of the year."""
    out = {}
    stop_cap = dt.datetime.combine(end, dt.time(0)) + dt.timedelta(days=1)
    for L in leaks:
        st = start_of(route, L, prof)
        stop = min(L["repaired"], stop_cap) if L["repaired"] else stop_cap
        h = max(0.0, (stop - st).total_seconds() / 3600.0)
        out[L["district"]] = out.get(L["district"], 0.0) + rate[L["grade"]] * h / 1000.0
    return out
