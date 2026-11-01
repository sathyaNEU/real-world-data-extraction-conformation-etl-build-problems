"""Write the whole target/ pack for task146 architecture 3 into a folder."""
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs as D    # noqa: E402
import pack as PK   # noqa: E402
import world as W   # noqa: E402

FILE_TIMES = {"sap": (2026, 8, 12, 16, 33), "cdp": (2026, 6, 4, 17, 5), "email": (2026, 11, 16, 8, 41),
              "feas": (2026, 10, 31, 16, 47), "sites": (2025, 8, 20, 9, 14)}
EXPORT = (2026, 9, 18, 15, 20)


def build_pack(out):
    os.makedirs(out, exist_ok=True)
    f = lambda k: os.path.join(out, PK.FILES[k])
    w = W.World()
    R = PK.Records(w)
    n = {"subjects": PK.write_subjects(R, f("subjects")), "dosing": PK.write_dosing(R, f("dosing")),
         "pasi": PK.write_pasi(R, f("pasi")), "pk": PK.write_pk(R, f("pk")), "cm": PK.write_cm(R, f("cm")),
         "epro": PK.write_epro(R, f("epro")), "ae": PK.write_ae(R, f("ae")), "dlqi": PK.write_dlqi(R, f("dlqi")),
         "sites": PK.write_sites(R, f("sites")), "feas": PK.write_feas(R, f("feas"))}
    D.sap(f("sap"))
    D.cdp(f("cdp"))
    D.email(f("email"))
    for k in PK.FILES:
        t = dt.datetime(*(FILE_TIMES.get(k) or EXPORT)).timestamp()
        os.utime(f(k), (t, t))
    return w, R, n


if __name__ == "__main__":
    w, R, n = build_pack(sys.argv[1])
    print(n)
