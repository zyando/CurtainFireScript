# -*- coding: utf-8 -*-

veclist = objvertices("ico.obj", 0)

divide_velist = [Vector3.UnitZ] + [Vector3(cos(angle) * x, 0, sin(angle)) for x in [-1, 1] for angle in [RAD * 45, RAD * 60]]

UNIT_VECTORS = [Vector3.UnitX, Vector3.UnitY, Vector3.UnitZ]

def divide(orgn, props):
    mat = Matrix3.LookAt(orgn.Velocity, props[0][1])

    for vec in divide_velist:
        shot = EntityShot(WORLD, "SCALE", props[0][0])
        shot.Pos = orgn.Pos
        shot.Velocity = vec * mat * 8

        if len(props) > 1:
            shot.LifeSpan = 45
            shot.AddTask(lambda s = shot: divide(s, props[1:]), 0, 1, shot.LifeSpan)
        else:
            shot.LifeSpan = 300
        shot()


def shot_scale(axis, props):
    for vec in veclist:
        shot = EntityShot(WORLD, "SCALE", 0x0000FF)
        shot.Pos = vec * 100
        shot.Velocity = vec * 8
        shot.LifeSpan = 45

        shot.AddTask(lambda s = shot: divide(s, props), 0, 1, shot.LifeSpan)
        shot()

COLORS = 0xFFFFFF, 0xFF0000, 0x00FF00

for i in range(3):
    axis = UNIT_VECTORS[i]
    props = zip(COLORS, [UNIT_VECTORS[(i + j) % 3] for j in range(3)])
    WORLD.AddTask(lambda a = axis, p = props: shot_scale(a, p), 0, 1, 0)
