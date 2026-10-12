"""Assemble the world: the corridor's days drawn and herded, the route's vehicle classes, the staff and the
reassignment workbook."""
import asks as A
import world


def build():
    W = world.build(world.SEED, world.P)
    W = world.herd(W)
    W = world.add_classes(W, world.SEED)
    S = A.staff_world(world.SEED)
    return W, S
