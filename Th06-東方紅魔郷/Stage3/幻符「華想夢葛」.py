# -*- coding: utf-8 -*-

veclist = objvertices("ico.obj", 0)

def shot_s(task):
    distance = 20 + sin(RAD * task.ExecutedCount * 60) * 80

    for pos in veclist:
        mat = Matrix3.RotationAxis(randomvec(), RAD * 30)

        for vec in veclist:
            shot = EntityShot(WORLD, "S", 0x0000A0)
            shot.Pos = pos * distance
            shot.Velocity = vec * mat * 6
            shot.LivingLimit = 160
            shot()
WORLD.AddTask(shot_s, 10, 30, 0, True)
