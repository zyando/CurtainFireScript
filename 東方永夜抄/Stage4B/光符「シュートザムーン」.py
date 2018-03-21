# -*- coding: utf-8 -*-
import random

veclist = objvertices("ico.obj", 1)

def phase0():
    for vec in veclist:
        target_vec = +(TARGET_BONE.WorldPos - CENTER_BONE.WorldPos)

        if vec * target_vec < 0.5: continue

        for i in range(2):
            shot = EntityShot(WORLD, "STAR_S", 0xA0A000)
            shot.Pos = CENTER_BONE.WorldPos
            shot.Velocity = vec * (2 + (i * 2))
            shot.LivingLimit = 400 - i * 200
            shot()
WORLD.AddTask(phase0, 5, 40, 30)

poslist = [v * 240 + -Vector3.UnitY * 320 for v in objvertices("ico.obj", 3) if v.y <= 0]

def phase1(task):
    posstack = poslist[:]
    random.shuffle(posstack)

    laser_color = 0xA00000 if task.ExecutedCount % 2 == 0 else 0x0000A0

    def shot_mgc_circle():
        if len(posstack) == 0: return True

        mgc = EntityShot(WORLD, "MAGIC_CIRCLE", 0x808000)
        mgc.Pos = CENTER_BONE.WorldPos
        mgc.Velocity = posstack.pop() * VEC_BONE.WorldMat * (1.0 / 30)
        mgc.LivingLimit = 50

        def pause(): mgc.Velocity *= 0
        mgc.AddTask(pause, 0, 1, 30)

        def shot_laser():
            shot = EntityShot(WORLD, "DIA", laser_color, Vector3(0.5, 0.5, 20))
            shot.Pos = mgc.Pos
            shot.Velocity = Vector3.UnitY * VEC_BONE.WorldMat * 20 * Matrix3.RotationAxis(randomvec(), RAD * 20)
            shot.LivingLimit = 100
            shot()
        mgc.AddTask(shot_laser, 0, 1, 45)
        mgc()
    WORLD.AddTask(lambda: [shot_mgc_circle() for i in range(16)], 0, len(posstack) / 16, 0)
WORLD.AddTask(phase1, 75, 4, 0, True)
