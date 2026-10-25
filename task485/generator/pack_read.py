"""Read the cut pack's ask files back into rows (ceiling.py runs on the cut pack, never on the generator's memory);
falls back to the generator's exports before the pack is cut."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")


def ash_exports():
    import ash as A
    import coal
    import world as W
    if os.path.exists(os.path.join(TARGET, "whinmoss_invoice_lines_2026.xlsx")):
        import pack_ash_read
        return pack_ash_read.read(TARGET)
    w = W.build()
    lots = coal.deliveries(w)
    W.flows(w)
    jobs = A.collections(w, A.produce(w, lots))
    return A.exports(w, jobs)
