"""Choose the ask records' stream offsets so that every graded ask figure clears its bin edge by a fifth of the bin.
Run once; the chosen offsets are written to offsets.py. The call's figures do not depend on these streams."""
import os
import sys
import tempfile
import calc
import pack


def margin(v, unit):
    return unit / 2 - abs(v - round(v / unit) * unit)


def r1(v):
    return round(v + 1e-9, 1)


def ok_contacts(tmp):
    g = calc.ask_contacts(tmp)
    m = min(margin(s, 0.1) for n, s in g.values())
    for alt in (calc.ask_contacts(tmp, mode="exact"), calc.ask_contacts(tmp, mode="loose"), calc.ask_contacts(tmp, mode="ids"),
                calc.ask_contacts(tmp, mode="exact", per_record=True)):
        for z in g:
            if alt[z][0] == g[z][0] or r1(alt[z][1]) == r1(g[z][1]):
                return -1
    return m


def ok_lab(tmp):
    g = calc.ask_lab(tmp)
    a = calc.ask_lab(tmp, shift_h=0)
    for w in g:
        if r1(a[w][0]) == r1(g[w][0]) or r1(a[w][1]) == r1(g[w][1]):
            return -1
    return min(min(margin(m, 0.1), margin(p, 0.1)) for m, p, n in g.values())


if __name__ == "__main__":
    tmp = tempfile.mkdtemp()
    best = None
    for c in range(int(os.environ.get('C_START', 0)), 200):
        pack.build(out=tmp, c_off=c, l_off=0)
        m = ok_contacts(tmp)
        if m >= 0.02:
            best_c = c
            break
    for l in range(int(os.environ.get('L_START', 0)), 200):
        pack.build(out=tmp, c_off=best_c, l_off=l)
        m = ok_lab(tmp)
        if m >= 0.02:
            best_l = l
            break
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "offsets.py"), "w") as f:
        f.write('"""Stream offsets for the ask records, set by recentre.py so every graded ask figure sits clear of its bin edge."""\n'
                "C_OFF = %d\nL_OFF = %d\n" % (best_c, best_l))
    print("C_OFF", best_c, "L_OFF", best_l)
