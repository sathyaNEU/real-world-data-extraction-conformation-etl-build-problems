"""The New York Stock Exchange's trading calendar: its holidays under the exchange's own observance rules, the two
unscheduled closures in the window, and the 1:00 p.m. early closes."""
import datetime as dt

SPECIAL_CLOSURES = {
    dt.date(2018, 12, 5): "National Day of Mourning for President George H. W. Bush",
    dt.date(2025, 1, 9): "National Day of Mourning for President Jimmy Carter",
}


def easter(y):
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    month = (h + l_ - 7 * m + 114) // 31
    day = (h + l_ - 7 * m + 114) % 31 + 1
    return dt.date(y, month, day)


def nth_weekday(y, m, wd, n):
    d = dt.date(y, m, 1)
    d += dt.timedelta(days=(wd - d.weekday()) % 7)
    return d + dt.timedelta(weeks=n - 1)


def last_weekday(y, m, wd):
    d = dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)
    return d - dt.timedelta(days=(d.weekday() - wd) % 7)


def observed(d):
    if d.weekday() == 5:
        return d - dt.timedelta(days=1)
    if d.weekday() == 6:
        return d + dt.timedelta(days=1)
    return d


def holidays(y):
    """{date: name} for one year. New Year's Day falling on a Saturday is not observed on the Friday before."""
    h = {}
    nyd = dt.date(y, 1, 1)
    if nyd.weekday() == 6:
        h[nyd + dt.timedelta(days=1)] = "New Year's Day (observed)"
    elif nyd.weekday() < 5:
        h[nyd] = "New Year's Day"
    h[nth_weekday(y, 1, 0, 3)] = "Martin Luther King, Jr. Day"
    h[nth_weekday(y, 2, 0, 3)] = "Washington's Birthday"
    h[easter(y) - dt.timedelta(days=2)] = "Good Friday"
    h[last_weekday(y, 5, 0)] = "Memorial Day"
    if y >= 2022:
        j = dt.date(y, 6, 19)
        h[observed(j)] = "Juneteenth National Independence Day" + (" (observed)" if observed(j) != j else "")
    j4 = dt.date(y, 7, 4)
    h[observed(j4)] = "Independence Day" + (" (observed)" if observed(j4) != j4 else "")
    h[nth_weekday(y, 9, 0, 1)] = "Labor Day"
    h[nth_weekday(y, 11, 3, 4)] = "Thanksgiving Day"
    x = dt.date(y, 12, 25)
    h[observed(x)] = "Christmas Day" + (" (observed)" if observed(x) != x else "")
    for d, why in SPECIAL_CLOSURES.items():
        if d.year == y:
            h[d] = why
    return h


def early_closes(y):
    out = {nth_weekday(y, 11, 3, 4) + dt.timedelta(days=1): "Day after Thanksgiving"}
    j3 = dt.date(y, 7, 3)
    if j3.weekday() <= 3:
        out[j3] = "Independence Day eve"
    c24 = dt.date(y, 12, 24)
    if c24.weekday() <= 3:
        out[c24] = "Christmas Eve"
    return out


def trading_days(start, end):
    hol = {}
    for y in range(start.year, end.year + 1):
        hol.update(holidays(y))
    out, d = [], start
    while d <= end:
        if d.weekday() < 5 and d not in hol:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def settlement_holidays(y):
    """Days securities do not settle: the exchange's holidays and the two bank holidays it trades through."""
    h = set(holidays(y))
    h.add(nth_weekday(y, 10, 0, 2))
    vd = dt.date(y, 11, 11)
    h.add(vd + dt.timedelta(days=1) if vd.weekday() == 6 else vd)
    return h


def settle_date(trade, n):
    d = trade
    while n > 0:
        d += dt.timedelta(days=1)
        if d.weekday() < 5 and d not in settlement_holidays(d.year):
            n -= 1
    return d
