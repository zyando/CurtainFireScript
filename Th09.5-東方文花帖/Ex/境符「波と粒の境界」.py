# -*- coding: utf-8 -*-

veclist = objvertices("ico.obj", 1)

def shot_dia(rot = [Quaternion.Identity, Quaternion.Identity, Quaternion.RotationAxis(randomvec(), RAD * 1), Quaternion.RotationAxis(randomvec(), RAD * 1)]):
    for vec in veclist:
        shot = EntityShot(WORLD, "DIA", 0xFF40FF)
        shot.Velocity = vec * rot[0] * 8
        shot.LivingLimit = 80
        shot()
    rot[2] = rot[2] * rot[3]
    rot[1] = (rot[1] * rot[2]) ^ 0.1
    rot[0] *= rot[1]
WORLD.AddTask(shot_dia, 0, 420, 0)
