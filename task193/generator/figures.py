"""generator/figures.json: every number the write-up states."""
import json
import os


def write(gen_dir, g):
    with open(os.path.join(gen_dir, "figures.json"), "w") as f:
        json.dump(g, f, indent=1, sort_keys=True)
        f.write("\n")
