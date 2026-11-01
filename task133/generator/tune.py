"""Places each graded segment figure at the centre of its 0.1 million bin by the segment's exposure scale (the size of
the book in that segment), measured on a written pack. Prints the scale to file in params.EXPOSURE_SCALE."""
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

TARGET = {"Construction": 2.5, "Manufacturing": 1.3, "Trade and logistics": 2.4,
          "Hospitality, retail and leisure": 3.4, "Business and property services": 1.5,
          "Health, education and personal services": 0.4}


def main(rounds=3):
    import importlib
    import params as P
    for i in range(rounds):
        import analysis as A
        import make_pack
        tmp = tempfile.mkdtemp()
        try:
            make_pack.make(tmp)
            pk, res = A.ladder(tmp)
        finally:
            shutil.rmtree(tmp)
        t, seg, _ = res["golden"]
        print("round", i, round(t / 1e6, 4), {s[:12]: round(seg[s] / 1e6, 4) for s in TARGET})
        new = {s: round(P.EXPOSURE_SCALE[s] * TARGET[s] / (seg[s] / 1e6), 4) for s in TARGET}
        if all(abs(seg[s] / 1e6 - TARGET[s]) < 0.002 for s in TARGET):
            break
        src = open(os.path.join(HERE, "params.py")).read()
        start = src.index("EXPOSURE_SCALE = {")
        end = src.index("}", start) + 1
        body = "EXPOSURE_SCALE = {\n" + "".join(f'    "{s}": {v},\n' for s, v in new.items()) + "}"
        open(os.path.join(HERE, "params.py"), "w").write(src[:start] + body + src[end:])
        for m in ("params", "world", "world_asks", "pack", "pack_asks", "docs", "make_pack", "analysis"):
            if m in sys.modules:
                importlib.reload(sys.modules[m])
        import params as P  # noqa: F811


if __name__ == "__main__":
    main()
