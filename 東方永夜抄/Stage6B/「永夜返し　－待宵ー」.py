# -*- coding: utf-8 -*-

veclist = objvertices("ico.obj", 3)

def phase0():
    def shot_dia():
        for vec in veclist:
            shot = EntityShot(WORLD, "DIA", 0x000080)
            shot.Velocity = vec * 3
            shot.LivingLimit = 320
            shot()
    WORLD.AddTask(shot_dia, 8, 20, 0)
WORLD.AddTask(phase0, 240, 3, 0)

def phase1(task):
    shot = EntityShot(WORLD, "M", 0xA00000)
    shot.Velocity = Vector3.UnitX * (task.ExecutedCount % 2 * 2 - 1) * 3
    shot.LivingLimit = 300
    shot()

    def turn():
        shot.Velocity = +(TARGET_BONE.WorldPos - shot.Pos) * 3
    shot.AddTask(turn, 0, 1, 60)
WORLD.AddTask(phase1, 8, 75, 90, True)
