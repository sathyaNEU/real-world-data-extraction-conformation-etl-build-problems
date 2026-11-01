"""task229 generator: the shipped files' headers as the systems that write them name them.

The generator works on plain internal names; ship.py writes each file under its source system's own field names
(the hydrometric database export, the gauging software export, the register and tracker workbooks, the visit log
and the grab-sample sheet), and every reader in the generator maps them back on load. The readings a solver needs
from these files are filed in the files' own form (received_utc, measured_utc, gh_m, unit, q_meas, rating_no) or
in the network's documents (the data plan's section 1, the standard's sections 2, 5 and 7), never in a file that
describes the pack (reduce-house-fixes H9)."""

SHIPPED = {
    "daily": {"station": "stn_no", "date": "obs_date", "platform": "platform_type"},
    "gaugings": {"station": "stn_no", "discharge": "q_meas", "rating": "rating_no"},
    "register": {"station": "stn_no"},
    "migration": {"station": "stn_no"},
    "visits": {"station": "stn_no", "date": "visit_date"},
    "quality": {"station": "stn_no", "date": "sample_date"},
}


def name(key, col):
    """the shipped header for an internal column name"""
    return SHIPPED[key].get(col, col)


def out(df, key):
    """a frame with internal names, renamed to the shipped headers"""
    return df.rename(columns=SHIPPED[key])


def back(df, key):
    """a frame read from the pack, renamed to the internal names"""
    return df.rename(columns={v: k for k, v in SHIPPED[key].items()})


def dtype(key, d):
    """a read_csv dtype map keyed by internal names, keyed by the shipped headers"""
    return {name(key, k): v for k, v in d.items()}
