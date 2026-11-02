"""Simulate the world and write the pack into a directory (default: generator/out/target)."""
import os, sys, shutil
import world, pack


def make(target):
    if os.path.exists(target):
        shutil.rmtree(target)
    os.makedirs(target)
    o = world.simulate()
    idm = pack.build(target, o)
    scrub(target)
    return o, idm


# each document's own date: FS-3 revision 6 was approved on 14 September 2026, the onboarding letter is dated 3 December
PDF_DATES = {"FS-3_fuel_systems_standard.pdf": "2026-09-14", "wetstock_onboarding_2027.pdf": "2026-12-03"}


def scrub(folder, pdf_dates=PDF_DATES):
    """the writers' names out of every binary's metadata, byte for byte (never a re-save), and each PDF's dates set to
    the document's own date"""
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".claude", "skills",
                                    "reduce-house-fixes", "scripts"))
    import scrub_producer_metadata as SC
    for fn in sorted(os.listdir(folder)):
        p = os.path.join(folder, fn)
        if fn.endswith(".xlsx"):
            SC.scrub_ooxml(p, "Highbank Marinas", "2027-01-11", ceiling="2027-01-11")
        elif fn.endswith(".pdf"):
            SC.scrub_pdf(p, "Highbank Marinas", pdf_dates[fn], floor="2026-01-01", ceiling="2027-01-12")


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "target")
    make(tgt)
    print("written", tgt)
